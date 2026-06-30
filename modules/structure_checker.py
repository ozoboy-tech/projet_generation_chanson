from typing import Dict, List


def obtenir_marqueurs(langue: str) -> Dict[str, str]:
    assert isinstance(langue, str)
    assert len(langue) > 0

    if langue == "Anglais":
        return {
            "titre": "Titre :",
            "couplet": "Verse",
            "refrain": "Chorus:",
        }

    return {
        "titre": "Titre :",
        "couplet": "Couplet",
        "refrain": "Refrain:",
    }


def normaliser_texte(texte: str) -> str:
    assert isinstance(texte, str)
    assert len(texte) >= 0

    return texte.lower().strip()


def verifier_titre(texte: str, marqueur_titre: str) -> bool:
    assert isinstance(texte, str)
    assert isinstance(marqueur_titre, str)

    texte_normalise = normaliser_texte(texte)
    return marqueur_titre.lower() in texte_normalise


def compter_refrains(texte: str, marqueur_refrain: str) -> int:
    assert isinstance(texte, str)
    assert isinstance(marqueur_refrain, str)

    texte_normalise = normaliser_texte(texte)
    return texte_normalise.count(marqueur_refrain.lower())


def compter_couplets(
    texte: str,
    marqueur_couplet: str,
    nombre_couplets_attendu: int,
) -> int:
    assert isinstance(nombre_couplets_attendu, int)
    assert 1 <= nombre_couplets_attendu <= 3

    texte_normalise = normaliser_texte(texte)
    total = 0

    for numero in range(1, 4):
        if numero <= nombre_couplets_attendu:
            marqueur = f"{marqueur_couplet} {numero}:".lower()
            if marqueur in texte_normalise:
                total += 1

    return total


def calculer_score_structure(
    titre_present: bool,
    couplets_detectes: int,
    refrains_detectes: int,
    nombre_couplets_attendu: int,
) -> int:
    assert isinstance(titre_present, bool)
    assert 1 <= nombre_couplets_attendu <= 3

    score = 0

    if titre_present:
        score += 1

    if couplets_detectes == nombre_couplets_attendu:
        score += 2

    if refrains_detectes >= nombre_couplets_attendu:
        score += 2

    return score


def generer_messages_structure(
    titre_present: bool,
    couplets_detectes: int,
    refrains_detectes: int,
    nombre_couplets_attendu: int,
) -> List[str]:
    assert isinstance(titre_present, bool)
    assert 1 <= nombre_couplets_attendu <= 3

    messages = []

    if titre_present:
        messages.append("Titre détecté.")
    else:
        messages.append("Titre manquant.")

    messages.append(
        f"Couplets détectés : {couplets_detectes}/{nombre_couplets_attendu}."
    )

    messages.append(
        f"Refrains détectés : {refrains_detectes}/{nombre_couplets_attendu}."
    )

    return messages


def verifier_structure_chanson(
    texte: str,
    nombre_couplets_attendu: int,
    langue: str,
) -> Dict[str, object]:
    assert isinstance(texte, str)
    assert 1 <= nombre_couplets_attendu <= 3

    marqueurs = obtenir_marqueurs(langue)

    titre_present = verifier_titre(texte, marqueurs["titre"])
    couplets_detectes = compter_couplets(
        texte=texte,
        marqueur_couplet=marqueurs["couplet"],
        nombre_couplets_attendu=nombre_couplets_attendu,
    )
    refrains_detectes = compter_refrains(texte, marqueurs["refrain"])

    score = calculer_score_structure(
        titre_present=titre_present,
        couplets_detectes=couplets_detectes,
        refrains_detectes=refrains_detectes,
        nombre_couplets_attendu=nombre_couplets_attendu,
    )

    messages = generer_messages_structure(
        titre_present=titre_present,
        couplets_detectes=couplets_detectes,
        refrains_detectes=refrains_detectes,
        nombre_couplets_attendu=nombre_couplets_attendu,
    )

    return {
        "score": score,
        "score_max": 5,
        "titre_present": titre_present,
        "couplets_detectes": couplets_detectes,
        "refrains_detectes": refrains_detectes,
        "nombre_couplets_attendu": nombre_couplets_attendu,
        "structure_valide": score == 5,
        "messages": messages,
    }