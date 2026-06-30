# Ordre officiel des chapitres et sous-chapitres par thème
# Correspond à l'ordre de la table des matières (voir tables_matieres.md)
#
# Structure :
#   THEME (NO, FA, ES, GM...)
#   └── CHAPITRE (= nom du dossier, ex: "Nombres naturels et décimaux")
#       └── SOUS-CHAPITRE (point détaillé, ex: "Calcul réfléchi et mental")

ORDRE_CHAPITRES = {
    "NO": [
        "Nombres naturels et décimaux",
        "Nombres relatifs",
        "Nombres rationnels",
        "Nombres réels",
        "Situations aléatoires",
    ],
    "FA": [
        "Proportionnalité",
        "Fonctions",
        "Diagrammes",
        "Calcul littéral",
        "Équations",
    ],
    "ES": [
        "Figures géométriques planes",
        "Représentation de solides",
        "Transformations géométriques",
    ],
    "GM": [
        "Lignes et surfaces",
        "Théorèmes",
        "Solides",
        "Divers mesures",
    ],
    "RS": [],
    "AU": [],
}

ORDRE_SOUS_CHAPITRES = {
    "Nombres naturels et décimaux": [
        "Calcul réfléchi et mental",
        "Critères de divisibilité",
        "Multiples et diviseurs",
        "Nombres premiers",
        "PPMC et PGDC",
        "Puissances et racines",
        "Notation scientifique",
        "Priorité des opérations",
    ],
    "Nombres relatifs": [
        "Représenter, comparer et encadrer",
        "Addition et soustraction",
        "Multiplication et division",
        "Puissances et racines",
        "Priorité des opérations",
        "Résoudre des problèmes",
    ],
    "Nombres rationnels": [
        "Représenter, comparer et encadrer",
        "Amplifier et simplifier",
        "Écritures d'un même nombre",
        "Fractions partie d'un tout",
        "Addition et soustraction",
        "Multiplication et division",
        "Priorité des opérations",
        "Résoudre des problèmes",
    ],
    "Nombres réels": [
        "Ensembles de nombres",
        "Calcul réfléchi et mental",
        "Comparer, encadrer et représenter",
        "Puissances et racines",
        "Notation scientifique",
        "Priorité des opérations",
    ],
    "Situations aléatoires": [
        "Explorer les situations aléatoires",
        "Notion de probabilité",
    ],
    "Proportionnalité": [
        "Propriétés de la proportionnalité",
        "Représenter une situation",
        "Résoudre des problèmes",
    ],
    "Fonctions": [
        "Reconnaître des situations",
        "Classes de fonctions",
        "Lire, interpréter et représenter",
        "Passer d'une représentation à une autre",
    ],
    "Diagrammes": [
        "Lire des données",
        "Lire, interpréter et réaliser",
    ],
    "Calcul littéral": [
        "Élaborer une expression littérale",
        "Règles et conventions d'écriture",
        "Valeur numérique",
        "Expressions équivalentes",
        "Réduire une expression",
        "Multiplier des monômes",
        "Additionner des polynômes",
        "Multiplier des polynômes",
        "Identités remarquables",
        "Décomposer en facteurs",
        "Résoudre des problèmes",
        "Outil de preuve",
    ],
    "Équations": [
        "Approcher les équations",
        "Exprimer une variable",
        "Premier degré à une inconnue",
        "Problèmes premier degré une inconnue",
        "Traduire une situation (1 inconnue)",
        "Systèmes à deux inconnues",
        "Problèmes systèmes deux inconnues",
        "Traduire une situation (2 inconnues)",
        "Deuxième degré à une inconnue",
        "Problèmes deuxième degré",
        "Traduire une situation (2e degré)",
    ],
    "Figures géométriques planes": [
        "Marche à suivre",
        "Droites",
        "Angles",
        "Triangles",
        "Quadrilatères",
        "Cercles",
        "Polygones",
        "Droites remarquables du triangle",
        "Déduire des valeurs d'angles",
        "Tangentes",
        "Cercle de Thalès",
        "Triangles semblables",
    ],
    "Représentation de solides": [
        "Reconnaître et décrire des solides",
        "Développement et construction",
        "Perspective",
        "Angles de vue",
    ],
    "Transformations géométriques": [
        "Frises et pavages",
        "Symétrie axiale",
        "Symétrie centrale",
        "Translation",
        "Rotation",
        "Agrandissement",
        "Homothétie",
        "Reconnaître une transformation",
        "Anticiper une position",
    ],
    "Lignes et surfaces": [
        "Triangles",
        "Quadrilatères",
        "Cercles et disques",
        "Arcs et secteurs",
        "Polygones",
        "Figures composées",
        "Grandeur manquante",
    ],
    "Théorèmes": [
        "Pythagore",
        "Trigonométrie",
        "Thalès",
        "Figures semblables",
    ],
    "Solides": [
        "Cubes",
        "Parallélépipèdes rectangles",
        "Prismes droits",
        "Cylindres",
        "Pyramides",
        "Cônes",
        "Sphères",
        "Solides composés",
        "Grandeur manquante",
    ],
    "Divers mesures": [
        "Longueur et surfaces",
        "Volumes et capacité",
        "Masse",
        "Temps",
        "Vitesse, débit et masse volumique",
    ],
}


def sort_chapitres(theme: str, chapitres: list) -> list:
    """Trie les chapitres selon l'ordre officiel."""
    ordre = ORDRE_CHAPITRES.get(theme, [])
    def key(c):
        try:
            return ordre.index(c)
        except ValueError:
            return len(ordre)
    return sorted(chapitres, key=key)


def sort_sous_chapitres(chapitre: str, subs: list) -> list:
    """Trie les sous-chapitres selon l'ordre officiel."""
    ordre = ORDRE_SOUS_CHAPITRES.get(chapitre, [])
    def key(s):
        try:
            return ordre.index(s)
        except ValueError:
            return len(ordre)
    return sorted(subs, key=key)


def ordre_chapitre_index(theme: str, chapitre: str) -> int:
    ordre = ORDRE_CHAPITRES.get(theme, [])
    try:
        return ordre.index(chapitre)
    except ValueError:
        return len(ordre)


def ordre_sous_chapitre_index(chapitre: str, sous_chapitre: str) -> int:
    ordre = ORDRE_SOUS_CHAPITRES.get(chapitre, [])
    try:
        return ordre.index(sous_chapitre)
    except ValueError:
        return len(ordre)
