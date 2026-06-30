import re
from typing import Dict, List


STYLE_KEYWORDS = {
    "Rap": ["rythme", "mots", "directs", "flow", "voix"],
    "Pop": ["mélodie", "simple", "voix", "refrain", "lumière"],
    "Afro": ["énergie", "dansante", "chaleureuse", "rythme", "voix"],
    "Traditionnel": ["sagesse", "orale", "populaire", "mémoire", "histoire"],
}


def normaliser_texte(texte: str) -> str:
    assert isinstance(texte, str)
    assert len(texte) >= 0

    return texte.lower().strip()


def extraire_mots(texte: str) -> List[str]:
    assert isinstance(texte, str)
    assert len(texte) >= 0

    texte_normalise = normaliser_texte(texte)
    mots = re.findall(r"\b[a-zA-ZÀ-ÿ']+\b", texte_normalise)

    return mots


def calculer_score_theme(texte: str, theme: str) -> int:
    assert isinstance(texte, str)
    assert isinstance(theme, str)

    texte_normalise = normaliser_texte(texte)
    theme_normalise = normaliser_texte(theme)

    if not theme_normalise:
        return 0

    occurrences = texte_normalise.count(theme_normalise)

    if occurrences >= 3:
        return 5

    if occurrences == 2:
        return 4

    if occurrences == 1:
        return 3

    return 1


def calculer_taux_repetition(mots: List[str]) -> float:
    assert isinstance(mots, list)
    assert len(mots) >= 0

    if not mots:
        return 1.0

    mots_uniques = set(mots)
    taux_repetition = 1 - (len(mots_uniques) / len(mots))

    return round(taux_repetition, 2)


def calculer_score_originalite(texte: str) -> int:
    assert isinstance(texte, str)
    assert len(texte) >= 0

    mots = extraire_mots(texte)
    taux_repetition = calculer_taux_repetition(mots)

    if taux_repetition <= 0.35:
        return 5

    if taux_repetition <= 0.45:
        return 4

    if taux_repetition <= 0.55:
        return 3

    if taux_repetition <= 0.65:
        return 2

    return 1


def calculer_score_linguistique(texte: str) -> int:
    assert isinstance(texte, str)
    assert len(texte) >= 0

    lignes = [ligne.strip() for ligne in texte.splitlines() if ligne.strip()]

    if len(lignes) >= 10:
        return 5

    if len(lignes) >= 8:
        return 4

    if len(lignes) >= 6:
        return 3

    if len(lignes) >= 4:
        return 2

    return 1


def calculer_score_style(texte: str, style: str) -> int:
    assert isinstance(texte, str)
    assert isinstance(style, str)

    texte_normalise = normaliser_texte(texte)
    mots_cles = STYLE_KEYWORDS.get(style, [])

    if not mots_cles:
        return 2

    total_detecte = 0

    for mot_cle in mots_cles:
        if mot_cle.lower() in texte_normalise:
            total_detecte += 1

    if total_detecte >= 3:
        return 5

    if total_detecte == 2:
        return 4

    if total_detecte == 1:
        return 3

    return 2


def generer_commentaires(
    score_theme: int,
    score_originalite: int,
    score_linguistique: int,
    score_style: int,
) -> List[str]:
    assert 0 <= score_theme <= 5
    assert 0 <= score_originalite <= 5

    commentaires = []

    if score_theme >= 4:
        commentaires.append("Le thème est bien présent dans les paroles.")
    else:
        commentaires.append("Le thème pourrait être davantage renforcé.")

    if score_originalite >= 4:
        commentaires.append("Les paroles sont assez variées.")
    else:
        commentaires.append("Certaines répétitions peuvent être réduites.")

    if score_linguistique >= 4:
        commentaires.append("La structure textuelle est suffisante.")
    else:
        commentaires.append("Les paroles peuvent être développées avec plus de lignes.")

    if score_style >= 4:
        commentaires.append("Le style musical choisi est globalement respecté.")
    else:
        commentaires.append("Le style musical pourrait être plus marqué.")

    return commentaires


def evaluer_paroles(texte: str, theme: str, style: str) -> Dict[str, object]:
    assert isinstance(texte, str)
    assert isinstance(theme, str)

    score_theme = calculer_score_theme(texte, theme)
    score_originalite = calculer_score_originalite(texte)
    score_linguistique = calculer_score_linguistique(texte)
    score_style = calculer_score_style(texte, style)

    score_global = (
        score_theme
        + score_originalite
        + score_linguistique
        + score_style
    )

    commentaires = generer_commentaires(
        score_theme=score_theme,
        score_originalite=score_originalite,
        score_linguistique=score_linguistique,
        score_style=score_style,
    )

    return {
        "score_theme": score_theme,
        "score_originalite": score_originalite,
        "score_linguistique": score_linguistique,
        "score_style": score_style,
        "score_global": score_global,
        "score_max": 20,
        "commentaires": commentaires,
    }