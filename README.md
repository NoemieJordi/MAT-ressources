# MAT — Ressources mathématiques

Site de gestion et recherche de ressources mathématiques, compilées automatiquement via GitHub Actions et consultables depuis n'importe quel appareil.

---

## Structure du projet

```
MAT-site/
├── exercices/              ← tes fichiers .tex (un par ressource)
│   ├── NO/                 ← optionnel : organiser par thème
│   ├── FA/
│   └── ...
├── scripts/
│   └── build.py            ← compile les PDF et génère ressources.json
├── site/
│   ├── index.html          ← le site web (filtres + aperçu PDF)
│   ├── pdf/                ← PDFs élève (générés automatiquement)
│   └── corr/               ← PDFs corrigés (générés automatiquement)
├── template_site.tex       ← préambule LaTeX commun
├── .github/workflows/
│   └── build.yml           ← déploiement automatique sur GitHub Pages
└── README.md
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
EX_NO-PrioriteOperations_JeuDePiste.tex
EVAL_FA-Equations_Bilan.tex
TH_ES-Trigonometrie_Cosinus.tex
JEU_NO-NombresRelatifs_BatailleNavale.tex
PROJ_GM-Aires_MaquetteAppartement.tex
PLANIF_NO-NombresNaturels_Sequence1.tex
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
% sous_chapitre: Priorité des opérations
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
| `chapitre` | Texte libre | Oui |
| `sous_chapitre` | Texte libre | Oui |
| `niveau` | `[9e]` `[10e]` `[9e, 10e]` ... | Oui |
| `type` | `TH` `EX` `JEU` `PROJ` `REV` `EVAL` `PLANIF` `RES` | Oui |
| `tags` | `[jeu, simulation, ...]` | Non |
| `difficulte` | `1` (facile) `2` (moyen) `3` (difficile) | Non |
| `corrige` | `true` ou `false` | Non (automatique selon le type) |
| `source` | `latex` (défaut) ou `pdf` | Non |

Valeur automatique de `corrige` selon le type :
- Toujours `true` : `EX`, `REV`, `EVAL`
- Toujours `false` : `PLANIF`, `RES`
- À préciser : `TH`, `JEU`, `PROJ`

### 2. Placer le fichier

```
MAT-site/exercices/NO-PrioriteOperations/EX_NO-PrioriteOperations_JeuDePiste.tex
```

---

## Ajouter une ressource PDF existante (sans .tex)

Place les fichiers dans `exercices/` avec la convention de nommage :

```
EX_NO-PrioriteOperations_JeuDePiste.pdf
EX_NO-PrioriteOperations_JeuDePiste_corrige.pdf   ← optionnel
```

Et crée un fichier `.tex` minimaliste avec juste les métadonnées et `source: pdf` :

```latex
% ---
% titre: Jeu de piste — priorité des opérations
% theme: NO
% sous_chapitre: Priorité des opérations
% niveau: [9e]
% type: EX
% tags: [jeu]
% difficulte: 2
% corrige: true
% source: pdf
% ---
```

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
# Se placer dans le dossier du projet
cd ~/Documents/_Ecole/03-Cycle3/MAT/MAT-site

# Ajouter les nouveaux fichiers
git add .

# Créer un commit
git commit -m "Ajout: EX_NO-PrioriteOperations_JeuDePiste"

# Pousser — GitHub Actions compile et déploie automatiquement
git push
```

Le site est mis à jour en ~3-5 minutes après le push.

### Forcer la recompilation complète

Depuis GitHub → Actions → "Compiler LaTeX et déployer le site" → "Run workflow" → cocher "Recompiler tous les fichiers".

---

## Premier déploiement sur GitHub

```bash
cd ~/Documents/_Ecole/03-Cycle3/MAT/MAT-site

git init
git add .
git commit -m "Init MAT-site"
git remote add origin https://github.com/TON-COMPTE/MAT-ressources.git
git push -u origin main
```

Puis dans GitHub → Settings → Pages → Source : **GitHub Actions**.

Le site sera accessible à : `https://TON-COMPTE.github.io/MAT-ressources/`

---

## En-tête des PDF

L'en-tête est généré automatiquement par `\header{}{}` dans le template :
- Ligne de couleur fine (couleur du thème)
- Titre de la ressource

La couleur est injectée automatiquement par le script selon le champ `theme`.

---

## Notes

- Les fichiers auxiliaires LaTeX (`.aux`, `.log`, `.synctex.gz`) sont ignorés par git (`.gitignore`)
- Les PDFs compilés sont mis en cache entre les pushs — seuls les fichiers modifiés sont recompilés
- Les ressources externes volumineuses (`RES`) restent sur le Mac et ne sont pas committées
