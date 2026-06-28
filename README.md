# MAT — Ressources mathématiques

Site de gestion et recherche de ressources mathématiques, compilées automatiquement via GitHub Actions et consultables depuis n'importe quel appareil.

---

## Structure du projet GitHub

```
MAT-site/
├── exercices/
│   ├── 01-NO/
│   │   ├── NombresNaturelsDecimaux/
│   │   ├── NombresRelatifs/
│   │   ├── NombresRationnels/
│   │   ├── NombresReels/
│   │   └── SituationsAleatoires/
│   ├── 02-FA/
│   │   ├── Proportionnalite/
│   │   ├── Fonctions/
│   │   ├── Diagrammes/
│   │   ├── CalculLitteral/
│   │   └── Equations/
│   ├── 03-ES/
│   │   ├── FiguresGeometriquesPlanes/
│   │   ├── RepresentationSolides/
│   │   └── TransformationsGeometriques/
│   ├── 04-GM/
│   │   ├── LignesSurfaces/
│   │   ├── Theoremes/
│   │   ├── Solides/
│   │   └── DiversMesures/
│   ├── 05-RS/
│   └── 06-AU/
├── scripts/
│   ├── build.py            ← compile les PDF et génère ressources.json
│   └── chapitres.py        ← ordre officiel des sous-chapitres
├── site/
│   ├── index.html          ← le site web (filtres + aperçu PDF)
│   ├── pdf/                ← PDFs élève (générés automatiquement)
│   └── corr/               ← PDFs corrigés (générés automatiquement)
├── template_site.tex       ← préambule LaTeX commun
├── .github/workflows/
│   └── build.yml           ← déploiement automatique sur GitHub Pages
└── README.md
```

## Structure du dossier MAT sur le Mac

```
MAT/
├── 00-Commun/              ← préambule, figures, polices
├── 00-RES/                 ← ressources externes (PAS sur GitHub)
│   ├── NO/
│   ├── FA/
│   └── ...
├── 01-NO/
│   ├── NombresNaturelsDecimaux/
│   └── ...
├── 02-FA/
├── 03-ES/
├── 04-GM/
├── 05-RS/
├── 06-AU/
└── MAT-site/               ← ce dépôt GitHub
```

---

## Thèmes

| Code | Thème | Couleur |
|------|-------|---------|
| `NO` | Nombres & Opérations | Rouge `#AE0600` |
| `FA` | Fonctions & Algèbre | Orange `#E79840` |
| `ES` | Espace | Bleu `#5698C9` |
| `GM` | Grandeurs & Mesures | Vert `#8CCB30` |
| `RS` | Recherche & Stratégies | Violet `#6C61A2` |
| `AU` | Autre | Gris `#888888` |

---

## Types de documents

| Code | Description | Corrigé |
|------|-------------|---------|
| `TH` | Théorie / Cours | Parfois |
| `EX` | Exercice | Oui |
| `JEU` | Jeu / Activité | Parfois |
| `PROJ` | Projet | Parfois |
| `REV` | Dossier de révision | Oui |
| `EVAL` | Évaluation / TS | Oui |
| `PLANIF` | Planification | Non |
| `RES` | Ressource externe | Non |

---

## Nomenclature des fichiers

```
TYPE_THEME-SousChapitre_Titre.tex
```

Exemples :
```
EX_NO-NombresNaturelsDecimaux_JeuDePiste.tex
EVAL_FA-Equations_Bilan.tex
TH_ES-FiguresGeometriquesPlanes_Cosinus.tex
JEU_NO-NombresRelatifs_BatailleNavale.tex
PROJ_GM-LignesSurfaces_MaquetteAppartement.tex
PLANIF_NO-NombresNaturelsDecimaux_Sequence1.tex
RES_NO-NombresNaturelsDecimaux_ManuelVaudois.tex  ← métadonnées seulement
```

Règles :
- Pas d'espaces, pas d'accents dans le nom de fichier
- `_` entre les grandes parties
- `-` entre thème et sous-chapitre
- CamelCase pour les titres (`JeuDePiste`, `BatailleNavale`)

---

## Ajouter une ressource LaTeX

### 1. Créer le fichier `.tex`

Ajoute un bloc de métadonnées YAML en commentaire en tête du fichier :

```latex
% ---
% titre: Jeu de piste — priorité des opérations
% theme: NO
% chapitre: Nombres naturels et décimaux
% sous_chapitre: NombresNaturelsDecimaux
% niveau: [9e]
% type: EX
% tags: [jeu, priorité]
% difficulte: 2
% corrige: true
% ---

% Contenu LaTeX ici (sans \documentclass ni \begin{document})
\header{}{Jeu de piste — priorité des opérations}
...
```

Champs disponibles :

| Champ | Valeurs | Obligatoire |
|-------|---------|-------------|
| `titre` | Texte libre | Oui |
| `theme` | `NO` `FA` `ES` `GM` `RS` `AU` | Oui |
| `chapitre` | Texte libre (affiché sur le site) | Oui |
| `sous_chapitre` | Nom du dossier sans accents | Oui |
| `niveau` | `[9e]` `[10e]` `[9e, 10e]` ... | Oui |
| `type` | `TH` `EX` `JEU` `PROJ` `REV` `EVAL` `PLANIF` `RES` | Oui |
| `tags` | `[jeu, simulation, ...]` | Non |
| `difficulte` | `1` (facile) `2` (moyen) `3` (difficile) | Non |
| `corrige` | `true` ou `false` | Non (automatique selon le type) |
| `source` | `latex` (défaut) ou `pdf` | Non |
| `lien` | URL ou chemin local (pour `RES`) | Non |

Valeur automatique de `corrige` selon le type :
- Toujours `true` : `EX`, `REV`, `EVAL`
- Toujours `false` : `PLANIF`, `RES`
- À préciser : `TH`, `JEU`, `PROJ`

### 2. Placer le fichier

```
MAT-site/exercices/01-NO/NombresNaturelsDecimaux/EX_NO-NombresNaturelsDecimaux_JeuDePiste.tex
```

---

## Ajouter une ressource PDF existante (sans .tex)

Place les fichiers dans le bon sous-dossier de `exercices/` :

```
EX_NO-NombresNaturelsDecimaux_JeuDePiste.pdf
EX_NO-NombresNaturelsDecimaux_JeuDePiste_corrige.pdf   ← optionnel
```

Et crée un fichier `.tex` avec les métadonnées et `source: pdf` :

```latex
% ---
% titre: Jeu de piste — priorité des opérations
% theme: NO
% chapitre: Nombres naturels et décimaux
% sous_chapitre: NombresNaturelsDecimaux
% niveau: [9e]
% type: EX
% tags: [jeu]
% difficulte: 2
% corrige: true
% source: pdf
% ---
```

---

## Ajouter une ressource externe (RES)

Le fichier lourd reste dans `~/Documents/_Ecole/03-Cycle3/MAT/00-RES/` sur ton Mac (pas sur GitHub). Seul le fichier de métadonnées `.tex` va sur GitHub :

```latex
% ---
% titre: Manuel Vaudois — Nombres naturels
% theme: NO
% chapitre: Nombres naturels et décimaux
% sous_chapitre: NombresNaturelsDecimaux
% type: RES
% lien: /Users/noemiejordi/Documents/_Ecole/03-Cycle3/MAT/00-RES/NO/ManuelVaudois.pdf
% ---
```

Le site affichera un bouton **↗ Ouvrir** qui ouvre le fichier directement depuis iCloud.

---

## Commandes

### Compiler et tester en local

```bash
# Se placer dans le dossier du projet
cd ~/Documents/_Ecole/03-Cycle3/MAT/MAT-site

# Compiler tous les fichiers .tex
python3 scripts/build.py

# Compiler seulement les fichiers modifiés (mode rapide)
python3 scripts/build.py --changed

# Lancer le site en local
cd site
python3 -m http.server 8080
# Ouvrir http://localhost:8080 dans le navigateur
# Quitter avec Ctrl+C
```

### Pousser sur GitHub

```bash
cd ~/Documents/_Ecole/03-Cycle3/MAT/MAT-site

git add .
git commit -m "Ajout: EX_NO-NombresNaturelsDecimaux_JeuDePiste"
git push
```

Le site est mis à jour en ~5 minutes après le push.

### Forcer la recompilation complète

Depuis GitHub → Actions → "Compiler LaTeX et déployer le site" → "Run workflow" → cocher "Recompiler tous les fichiers".

---

## En-tête des PDF

Généré automatiquement par `\header{}{}` dans le template :
- Ligne de couleur fine (couleur du thème)
- Titre de la ressource

La couleur est injectée automatiquement selon le champ `theme`.

---

## Notes

- Les fichiers auxiliaires LaTeX (`.aux`, `.log`, `.synctex.gz`) sont ignorés par git
- Les PDFs sont mis en cache — seuls les fichiers modifiés sont recompilés à chaque push
- Les ressources externes (`00-RES/`) restent sur le Mac, jamais sur GitHub
