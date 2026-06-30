import streamlit as st

from modules.lyrics_generator import generer_chanson


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

    st.subheader("Résultat généré")
    st.text_area("Paroles générées", value=chanson, height=500)


def main() -> None:
    assert len(EMOTIONS) == 5
    assert len(LANGUES) == 3

    configurer_page()
    afficher_entete()
    parametres = afficher_formulaire()
    afficher_resultat(parametres)


if __name__ == "__main__":
    main()