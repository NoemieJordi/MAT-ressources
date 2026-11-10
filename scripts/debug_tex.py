#!/usr/bin/env python3
"""
debug_tex.py — compile UN fichier et affiche les erreurs LaTeX (le "log").

Usage (depuis MAT-site/) :
  python3 scripts/debug_tex.py Labyrinthe          # un bout du nom suffit
  python3 scripts/debug_tex.py Labyrinthe --corr   # version corrigé
  python3 scripts/debug_tex.py Labyrinthe --full   # log complet (pas seulement les erreurs)

Utilise les mêmes templates, couleurs de thème et images que build.py.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import EXERCICES, extract_meta, get_template_src, make_src  # noqa: E402


def find_tex(query: str) -> Path:
    matches = [p for p in EXERCICES.rglob("*.tex") if query.lower() in p.stem.lower()]
    if not matches:
        sys.exit(f"❌ Aucun fichier .tex ne contient « {query} » dans exercices/")
    if len(matches) > 1:
        print("⚠️  Plusieurs fichiers correspondent, précise un peu plus :")
        for m in matches:
            print("   ", m.relative_to(EXERCICES))
        sys.exit(1)
    return matches[0]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)

    corrige = "--corr" in sys.argv
    full    = "--full" in sys.argv

    tex_path = find_tex(args[0])
    meta     = extract_meta(tex_path)
    content  = tex_path.read_text(encoding="utf-8")
    toggle   = "\\togglefalse{question}" if corrige else "\\toggletrue{question}"
    src      = make_src(content, meta["theme"], toggle, get_template_src(meta))

    print(f"▶ {tex_path.relative_to(EXERCICES)}")
    print(f"  thème={meta['theme']}  type={meta['type']}  version={'corrigé' if corrige else 'élève'}\n")

    tmp_dir = Path(tempfile.mkdtemp(prefix="debug_tex_"))
    tmp_tex = tmp_dir / "debug.tex"
    tmp_tex.write_text(src, encoding="utf-8")

    # Les images (IMG_...) sont cherchées dans le dossier du .tex source
    env = os.environ.copy()
    env["TEXINPUTS"] = f"{tex_path.parent}:{env.get('TEXINPUTS', '')}"
    cmd = ["lualatex", "--interaction=nonstopmode", f"--output-directory={tmp_dir}", str(tmp_tex)]

    subprocess.run(cmd, capture_output=True, text=True, env=env)            # 1re passe
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)   # 2e passe

    log_file = tmp_dir / "debug.log"
    log = log_file.read_text(encoding="utf-8", errors="replace") if log_file.exists() else result.stdout
    lines = log.splitlines()

    if full:
        print(log)
    else:
        found = False
        for i, line in enumerate(lines):
            if line.startswith("!") or ("Error" in line and "Package" in line):
                found = True
                print("\n".join(lines[i:i + 6]))
                print("-" * 60)
        if not found:
            print("Aucune ligne d'erreur trouvée dans le log.")

    if result.returncode == 0:
        print("✅ Compilation réussie.")
        shutil.rmtree(tmp_dir, ignore_errors=True)
    else:
        print(f"❌ Compilation échouée (code {result.returncode}).")
        print(f"   Log complet : {log_file}")


if __name__ == "__main__":
    main()
