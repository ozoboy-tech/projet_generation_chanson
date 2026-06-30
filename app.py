import streamlit as st

from modules.evaluator import evaluer_paroles
from modules.lyrics_generator import generer_chanson
from modules.structure_checker import verifier_structure_chanson


EMOTIONS = ["Joyeux", "Triste", "Motivant", "Nostalgique", "Romantique"]
LANGUES = ["Français", "Anglais", "Bambara"]
STYLES_MUSICAUX = ["Rap", "Pop", "Afro", "Traditionnel"]


def configurer_page() -> None:
    assert isinstance(EMOTIONS, list)
    assert isinstance(LANGUES, list)

    st.set_page_config(
        page_title="Générateur de chansons NLP",
        page_icon="🎵",
        layout="wide",
    )


def afficher_entete() -> None:
    assert len(EMOTIONS) > 0
    assert len(STYLES_MUSICAUX) > 0

    st.title("Système intelligent de génération automatique de chansons")
    st.markdown(
        "Cette application génère des paroles structurées à partir d’un thème, "
        "d’une émotion, d’une langue et d’un style musical."
    )


def afficher_formulaire() -> dict:
    assert len(LANGUES) >= 1
    assert len(STYLES_MUSICAUX) >= 1

    with st.form("formulaire_generation"):
        theme = st.text_input(
            "Thème de la chanson",
            placeholder="Exemple : réussite, amour, paix, persévérance",
        )

        col1, col2 = st.columns(2)

        with col1:
            emotion = st.selectbox("Émotion", EMOTIONS)
            langue = st.selectbox("Langue", LANGUES)

        with col2:
            style = st.selectbox("Style musical", STYLES_MUSICAUX)
            nombre_couplets = st.number_input(
                "Nombre de couplets",
                min_value=1,
                max_value=3,
                value=2,
                step=1,
            )

        bouton_generer = st.form_submit_button("Générer la chanson")

    return {
        "theme": theme.strip(),
        "emotion": emotion,
        "langue": langue,
        "style": style,
        "nombre_couplets": int(nombre_couplets),
        "bouton_generer": bouton_generer,
    }


def afficher_score_structure(resultat_structure: dict) -> None:
    assert isinstance(resultat_structure, dict)
    assert "score" in resultat_structure

    st.markdown("### Vérification de la structure")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Score de structure",
            f"{resultat_structure['score']}/{resultat_structure['score_max']}",
        )

    with col2:
        st.metric(
            "Couplets",
            f"{resultat_structure['couplets_detectes']}/"
            f"{resultat_structure['nombre_couplets_attendu']}",
        )

    with col3:
        st.metric(
            "Refrains",
            f"{resultat_structure['refrains_detectes']}/"
            f"{resultat_structure['nombre_couplets_attendu']}",
        )

    if resultat_structure["structure_valide"]:
        st.success("Structure valide.")
    else:
        st.warning("Structure incomplète ou à corriger.")

    with st.expander("Détails de la vérification"):
        for message in resultat_structure["messages"]:
            st.write(f"- {message}")


def afficher_evaluation(resultat_evaluation: dict) -> None:
    assert isinstance(resultat_evaluation, dict)
    assert "score_global" in resultat_evaluation

    st.markdown("### Évaluation automatique des paroles")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Thème", f"{resultat_evaluation['score_theme']}/5")

    with col2:
        st.metric("Originalité", f"{resultat_evaluation['score_originalite']}/5")

    with col3:
        st.metric("Linguistique", f"{resultat_evaluation['score_linguistique']}/5")

    with col4:
        st.metric("Style", f"{resultat_evaluation['score_style']}/5")

    with col5:
        st.metric(
            "Score global",
            f"{resultat_evaluation['score_global']}/"
            f"{resultat_evaluation['score_max']}",
        )

    with st.expander("Commentaires d’évaluation"):
        for commentaire in resultat_evaluation["commentaires"]:
            st.write(f"- {commentaire}")


def afficher_resultat(parametres: dict) -> None:
    assert isinstance(parametres, dict)
    assert "theme" in parametres

    if not parametres["bouton_generer"]:
        st.info("Remplis le formulaire puis clique sur le bouton de génération.")
        return

    if not parametres["theme"]:
        st.error("Le thème est obligatoire.")
        return

    chanson = generer_chanson(
        theme=parametres["theme"],
        emotion=parametres["emotion"],
        langue=parametres["langue"],
        style=parametres["style"],
        nombre_couplets=parametres["nombre_couplets"],
    )

    resultat_structure = verifier_structure_chanson(
        texte=chanson,
        nombre_couplets_attendu=parametres["nombre_couplets"],
        langue=parametres["langue"],
    )

    resultat_evaluation = evaluer_paroles(
        texte=chanson,
        theme=parametres["theme"],
        style=parametres["style"],
    )

    st.subheader("Résultat généré")
    st.text_area("Paroles générées", value=chanson, height=500)

    afficher_score_structure(resultat_structure)
    afficher_evaluation(resultat_evaluation)


def main() -> None:
    assert len(EMOTIONS) == 5
    assert len(LANGUES) == 3

    configurer_page()
    afficher_entete()
    parametres = afficher_formulaire()
    afficher_resultat(parametres)


if __name__ == "__main__":
    main()