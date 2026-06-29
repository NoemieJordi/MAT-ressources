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
    check_meta(meta, tex_path)
    content = tex_path.read_text(encoding="utf-8")

    if meta["source"] == "pdf":
        import shutil
        pdf_out = corr_out = None

        if meta["type"] == "RES":
            # Pour les RES : le PDF est déposé manuellement dans site/pdf/
            # On vérifie juste qu'il existe, sans copier
            if (PDF_DIR / f"{stem}.pdf").exists():
                pdf_out = f"pdf/{stem}.pdf"
            if meta["corrige"] and (CORR_DIR / f"{stem}.pdf").exists():
                corr_out = f"corr/{stem}.pdf"
        else:
            # Pour les autres types : le PDF est à côté du .tex
            pdf_path  = tex_path.with_suffix(".pdf")
            corr_path = tex_path.parent / f"{stem}_corrige.pdf"
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

def check_meta(meta: dict, tex_path: Path):
    """Affiche des avertissements pour les métadonnées incomplètes."""
    warnings = []
    if meta["titre"] == tex_path.stem:
        warnings.append("titre non renseigné")
    if not meta["sous_chapitre"]:
        warnings.append("sous_chapitre manquant")
    if not meta["niveau"] and meta["type"] != "RES":
        warnings.append("niveau manquant")
    if not meta["tags"]:
        warnings.append("tags manquants")
    if meta["type"] in ("TH", "JEU", "PROJ") and meta["corrige"] is None:
        warnings.append("corrige non précisé (true/false)")
    if warnings:
        print(f"  ⚠️  Métadonnées incomplètes : {', '.join(warnings)}")
def needs_recompile(tex_path: Path) -> bool:
    """Retourne True si le .tex est plus récent que son PDF compilé."""
    stem    = tex_path.stem
    meta    = extract_meta(tex_path)

    if meta["source"] == "pdf":
        # Pas de compilation — toujours inclure dans le JSON
        return True

    pdf = PDF_DIR / f"{stem}.pdf"
    if not pdf.exists():
        return True  # Pas encore compilé

    tex_mtime = tex_path.stat().st_mtime
    pdf_mtime = pdf.stat().st_mtime
    return tex_mtime > pdf_mtime

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
# Nettoyage des orphelins
# -----------------------------------------------------------------------
def clean_orphans(valid_stems: set[str]):
    """Supprime les PDFs et entrées JSON dont le .tex n'existe plus."""
    removed = 0
    for pdf in list(PDF_DIR.glob("*.pdf")):
        if pdf.stem not in valid_stems:
            pdf.unlink()
            corr = CORR_DIR / pdf.name
            if corr.exists(): corr.unlink()
            print(f"  🗑  Orphelin supprimé : {pdf.name}")
            removed += 1
    if removed == 0:
        print("  ✓  Aucun orphelin trouvé")

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
def main():
    force_full = "--full" in sys.argv

    all_tex_files = sorted(EXERCICES.rglob("*.tex"))

    if force_full:
        tex_files = all_tex_files
        print(f"🔍 Mode complet : {len(tex_files)} fichier(s)\n")
    else:
        tex_files = [f for f in all_tex_files if needs_recompile(f)]
        skipped   = len(all_tex_files) - len(tex_files)
        print(f"🔍 Mode auto : {len(tex_files)} fichier(s) à recompiler, {skipped} inchangé(s)\n")

    # Stems valides = tous les .tex présents dans exercices/
    all_tex_stems = {p.stem for p in all_tex_files}

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

    # Supprime les entrées JSON dont le .tex n'existe plus
    orphan_keys = [k for k in existing if k not in all_tex_stems]
    for k in orphan_keys:
        print(f"  🗑  Entrée JSON supprimée : {k}")
        del existing[k]

    # Supprime les PDFs orphelins
    print("\n🧹 Nettoyage des PDFs orphelins...")
    clean_orphans(all_tex_stems)

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
