#!/usr/bin/env python3
"""
build.py — compile les .tex en PDF (élève + corrigé) et génère ressources.json

Usage:
  python3 scripts/build.py              # compile tous les fichiers
  python3 scripts/build.py --changed    # compile seulement les fichiers modifiés (git diff)
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chapitres import sort_sous_chapitres

# -----------------------------------------------------------------------
# Chemins
# -----------------------------------------------------------------------
ROOT      = Path(__file__).parent.parent
EXERCICES = ROOT / "exercices"
TEMPLATE  = ROOT / "template_site.tex"
SITE      = ROOT / "site"
PDF_DIR   = SITE / "pdf"
CORR_DIR  = SITE / "corr"
JSON_OUT  = SITE / "ressources.json"

PDF_DIR.mkdir(parents=True, exist_ok=True)
CORR_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------
# Couleurs des thèmes
# -----------------------------------------------------------------------
THEME_COLORS = {
    "NO": "themeNO",
    "FA": "themeFA",
    "ES": "themeES",
    "GM": "themeGM",
    "RS": "themeRS",
    "AU": "themeAU",
}

# Types qui ont toujours un corrigé
ALWAYS_CORRIGE = {"EX", "REV", "EVAL"}
# Types qui n'ont jamais de corrigé
NEVER_CORRIGE  = {"PLANIF", "RES"}

# -----------------------------------------------------------------------
# Template
# -----------------------------------------------------------------------
TEMPLATE_SRC = TEMPLATE.read_text(encoding="utf-8")

# -----------------------------------------------------------------------
# Métadonnées
# -----------------------------------------------------------------------
def extract_meta(tex_path: Path) -> dict:
    """
    Lit le bloc YAML en tête du .tex :
    % ---
    % titre: Mon exercice
    % theme: NO
    % chapitre: Nombres naturels et décimaux
    % sous_chapitre: Priorité des opérations
    % niveau: [9e, 10e]
    % type: EX
    % tags: [jeu, simulation]
    % difficulte: 2
    % corrige: true          # optionnel — pour TH et JEU
    % source: latex          # ou: pdf
    % ---
    """
    meta = {
        "titre":         tex_path.stem,
        "theme":         "AU",
        "chapitre":      "",
        "sous_chapitre": "",
        "niveau":        [],
        "type":          "EX",
        "tags":          [],
        "difficulte":    1,
        "corrige":       None,   # None = déterminé par le type
        "source":        "latex",
        "lien":          None,
        "categorie":     None,
    }
    src  = tex_path.read_text(encoding="utf-8")
    bloc = re.search(r'%\s*---\s*\n(.*?)%\s*---', src, re.DOTALL)
    if not bloc:
        return meta

    for line in bloc.group(1).splitlines():
        m = re.match(r'%\s*([\w]+)\s*:\s*(.+)', line.strip())
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip()
        if   key == "titre":         meta["titre"]         = val
        elif key == "theme":         meta["theme"]         = val.upper()
        elif key == "chapitre":      meta["chapitre"]      = val
        elif key == "sous_chapitre": meta["sous_chapitre"] = val
        elif key == "type":          meta["type"]          = val.upper()
        elif key == "source":        meta["source"]        = val.lower()
        elif key == "lien":          meta["lien"]          = val
        elif key == "categorie":     meta["categorie"]     = val
        elif key == "difficulte":
            try: meta["difficulte"] = int(val)
            except ValueError: pass
        elif key == "corrige":
            meta["corrige"] = val.lower() in ("true", "oui", "yes", "1")
        elif key in ("niveau", "tags"):
            meta[key] = re.findall(r'[\w\u00C0-\u024F\-]+', val)

    # Détermine corrige si non explicite
    t = meta["type"]
    if meta["corrige"] is None:
        if t in ALWAYS_CORRIGE:   meta["corrige"] = True
        elif t in NEVER_CORRIGE:  meta["corrige"] = False
        else:                      meta["corrige"] = False  # TH, JEU — opt-in

    return meta

THEMES_ORDER = ["NO", "FA", "ES", "GM", "RS", "AU"]
ORDRE_THEMES = {code: i for i, code in enumerate(THEMES_ORDER)}

def ORDRE_SC(theme: str, sous_chapitre: str) -> int:
    from chapitres import ORDRE_SOUS_CHAPITRES
    ordre = ORDRE_SOUS_CHAPITRES.get(theme, [])
    try:
        return ordre.index(sous_chapitre)
    except ValueError:
        return len(ordre)

# -----------------------------------------------------------------------
# Compilation LaTeX
# -----------------------------------------------------------------------
def compile_latex(tex_src: str, out_dir: Path, stem: str) -> bool:
    tmp = out_dir / f"{stem}.tex"
    tmp.write_text(tex_src, encoding="utf-8")
    result = subprocess.run(
        ["lualatex", "--interaction=nonstopmode", f"--output-directory={out_dir}", str(tmp)],
        capture_output=True, text=True
    )
    for ext in [".aux", ".log", ".out", ".tex"]:
        p = out_dir / f"{stem}{ext}"
        if p.exists(): p.unlink()
    return result.returncode == 0

def make_src(content: str, theme: str, toggle: str) -> str:
    color_cmd = f"\\colorlet{{themeColor}}{{{THEME_COLORS.get(theme, 'themeAU')}}}"
    return (TEMPLATE_SRC
        .replace("\\toggletrue{question}   % <-- remplacé par togglefalse pour le corrigé", toggle)
        .replace("%%THEMECOLOR%%", color_cmd)
        .replace("%%CONTENT%%", content))

# -----------------------------------------------------------------------
# Traitement d'un fichier
# -----------------------------------------------------------------------
def build_resource(tex_path: Path) -> dict | None:
    stem    = tex_path.stem
    meta    = extract_meta(tex_path)
    content = tex_path.read_text(encoding="utf-8")

    if meta["source"] == "pdf":
        # Fichier PDF existant — pas de compilation
        pdf_path  = tex_path.with_suffix(".pdf")
        corr_path = tex_path.parent / f"{stem}_corrige.pdf"
        import shutil
        pdf_out = corr_out = None
        if pdf_path.exists():
            shutil.copy(pdf_path, PDF_DIR / f"{stem}.pdf")
            pdf_out = f"pdf/{stem}.pdf"
        if meta["corrige"] and corr_path.exists():
            shutil.copy(corr_path, CORR_DIR / f"{stem}.pdf")
            corr_out = f"corr/{stem}.pdf"
        meta["pdf"]         = pdf_out
        meta["corrige_pdf"] = corr_out
        meta["fichier"]     = stem
        return meta

    # Compilation LaTeX
    src_eleve = make_src(content, meta["theme"], "\\toggletrue{question}")
    ok_eleve  = compile_latex(src_eleve, PDF_DIR, stem)
    if not ok_eleve:
        print(f"  ⚠️  Échec élève : {stem}")

    ok_corr = False
    if meta["corrige"]:
        src_corr = make_src(content, meta["theme"], "\\togglefalse{question}")
        ok_corr  = compile_latex(src_corr, CORR_DIR, stem)
        if not ok_corr:
            print(f"  ⚠️  Échec corrigé : {stem}")

    meta["pdf"]         = f"pdf/{stem}.pdf"  if ok_eleve else None
    meta["corrige_pdf"] = f"corr/{stem}.pdf" if ok_corr  else None
    meta["fichier"]     = stem
    return meta

# -----------------------------------------------------------------------
# Fichiers modifiés via git
# -----------------------------------------------------------------------
def changed_tex_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True, text=True, cwd=ROOT
    )
    files = []
    for line in result.stdout.splitlines():
        p = ROOT / line.strip()
        if p.suffix == ".tex" and p.is_relative_to(EXERCICES) and p.exists():
            files.append(p)
    return files

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
def main():
    only_changed = "--changed" in sys.argv

    if only_changed:
        tex_files = changed_tex_files()
        print(f"🔍 Mode diff : {len(tex_files)} fichier(s) modifié(s)\n")
    else:
        tex_files = sorted(EXERCICES.rglob("*.tex"))
        print(f"🔍 Mode complet : {len(tex_files)} fichier(s)\n")

    # Charge le JSON existant (pour mode diff)
    existing = {}
    if JSON_OUT.exists():
        try:
            for r in json.loads(JSON_OUT.read_text(encoding="utf-8")):
                existing[r["fichier"]] = r
        except Exception:
            pass

    for tex_path in tex_files:
        print(f"▶ {tex_path.relative_to(ROOT)}")
        meta = build_resource(tex_path)
        if meta:
            existing[meta["fichier"]] = meta

    ressources = sorted(existing.values(), key=lambda r: (
        r["theme"],
        ORDRE_THEMES.get(r["theme"], 99),
        ORDRE_SC(r["theme"], r.get("sous_chapitre", "")),
        r["titre"]
    ))
    JSON_OUT.write_text(json.dumps(ressources, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ {len(ressources)} ressource(s) → {JSON_OUT}")

if __name__ == "__main__":
    main()
