# Ordre officiel des sous-chapitres par thème
# Correspond à l'ordre de la table des matières

ORDRE_SOUS_CHAPITRES = {
    "NO": [
        "NombresNaturelsDecimaux",
        "NombresRelatifs",
        "NombresRationnels",
        "NombresReels",
        "SituationsAleatoires",
    ],
    "FA": [
        "Proportionnalite",
        "Fonctions",
        "Diagrammes",
        "CalculLitteral",
        "Equations",
    ],
    "ES": [
        "FiguresGeometriquesPlanes",
        "RepresentationSolides",
        "TransformationsGeometriques",
    ],
    "GM": [
        "LignesSurfaces",
        "Theoremes",
        "Solides",
        "DiversMesures",
    ],
    "RS": [],
    "AU": [],
}

def sort_sous_chapitres(theme: str, subs: list[str]) -> list[str]:
    """Trie les sous-chapitres selon l'ordre officiel."""
    ordre = ORDRE_SOUS_CHAPITRES.get(theme, [])
    def key(s):
        try:
            return ordre.index(s)
        except ValueError:
            return len(ordre)  # inconnu → à la fin
    return sorted(subs, key=key)
