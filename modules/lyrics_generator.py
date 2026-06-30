from typing import Dict


LANGUAGE_CODES: Dict[str, str] = {
    "Français": "fr",
    "Anglais": "en",
    "Bambara": "bm",
}

SUPPORTED_EMOTIONS = ["Joyeux", "Triste", "Motivant", "Nostalgique", "Romantique"]
SUPPORTED_STYLES = ["Rap", "Pop", "Afro", "Traditionnel"]


def nettoyer_theme(theme: str) -> str:
    assert isinstance(theme, str)
    assert len(theme) <= 80

    theme_nettoye = " ".join(theme.strip().split())

    if not theme_nettoye:
        return "inspiration"

    return theme_nettoye.lower()


def obtenir_code_langue(langue: str) -> str:
    assert isinstance(langue, str)
    assert len(LANGUAGE_CODES) == 3

    return LANGUAGE_CODES.get(langue, "fr")


def obtenir_signature_style(style: str, code_langue: str) -> str:
    assert isinstance(style, str)
    assert code_langue in ["fr", "en", "bm"]

    signatures = {
        "Rap": {
            "fr": "avec des mots directs et un rythme marqué",
            "en": "with sharp words and a strong rhythm",
            "bm": "ka kuma tigɛlen ni rythme barika la",
        },
        "Pop": {
            "fr": "avec une mélodie simple et des images claires",
            "en": "with a simple melody and clear images",
            "bm": "ni donkili nɔgɔman ye ka se bɛɛ ma",
        },
        "Afro": {
            "fr": "avec une énergie dansante et chaleureuse",
            "en": "with a warm and dancing energy",
            "bm": "ni fɛɛrɛ ni dɔn ye ka kanu don",
        },
        "Traditionnel": {
            "fr": "avec une couleur orale et une sagesse populaire",
            "en": "with an oral tone and folk wisdom",
            "bm": "ni kuma kɔrɔ ni hadamadenya hakili la",
        },
    }

    return signatures.get(style, signatures["Pop"])[code_langue]


def obtenir_phrase_emotion(emotion: str, code_langue: str) -> str:
    assert isinstance(emotion, str)
    assert code_langue in ["fr", "en", "bm"]

    phrases = {
        "Joyeux": {
            "fr": "la lumière revient dans les voix",
            "en": "light comes back into every voice",
            "bm": "yeelen bɛ segin ka na kanw na",
        },
        "Triste": {
            "fr": "le silence pèse mais l’espoir reste debout",
            "en": "silence is heavy but hope remains standing",
            "bm": "sunya ka gɛlɛn nka jigi bɛ yen",
        },
        "Motivant": {
            "fr": "chaque pas devient une preuve de courage",
            "en": "every step becomes proof of courage",
            "bm": "sen bɛɛ bɛ kɛ dusukun barika ye",
        },
        "Nostalgique": {
            "fr": "les souvenirs parlent doucement au présent",
            "en": "memories softly speak to the present",
            "bm": "hakilina kɔrɔw bɛ kuma sumalen na",
        },
        "Romantique": {
            "fr": "deux cœurs avancent dans le même refrain",
            "en": "two hearts move inside the same chorus",
            "bm": "dusukun fila bɛ taa kelen kan",
        },
    }

    return phrases.get(emotion, phrases["Motivant"])[code_langue]


def construire_prompt(
    theme: str,
    emotion: str,
    langue: str,
    style: str,
    nombre_couplets: int,
) -> str:
    assert isinstance(nombre_couplets, int)
    assert 1 <= nombre_couplets <= 3

    return (
        f"Générer une chanson sur le thème '{theme}', "
        f"avec une émotion '{emotion}', en langue '{langue}', "
        f"dans un style '{style}', avec {nombre_couplets} couplet(s), "
        "un titre et un refrain répété."
    )


def generer_titre(theme: str, emotion: str, code_langue: str) -> str:
    assert theme != ""
    assert code_langue in ["fr", "en", "bm"]

    theme_titre = theme.title()

    if code_langue == "en":
        return f"{theme_titre} Road"

    if code_langue == "bm":
        return f"{theme_titre} ka Kan"

    if emotion == "Triste":
        return f"Les traces de {theme}"

    if emotion == "Joyeux":
        return f"La lumière de {theme}"

    return f"Jusqu’à {theme}"


def generer_couplet(
    theme: str,
    emotion: str,
    style: str,
    code_langue: str,
    numero: int,
) -> str:
    assert 1 <= numero <= 3
    assert theme != ""

    signature = obtenir_signature_style(style, code_langue)
    phrase_emotion = obtenir_phrase_emotion(emotion, code_langue)

    if code_langue == "en":
        return (
            f"Verse {numero}:\n"
            f"I walk with {theme} written in my mind,\n"
            f"{phrase_emotion}, step after step I climb,\n"
            f"The song takes shape {signature},\n"
            f"And every line keeps the dream alive."
        )

    if code_langue == "bm":
        return (
            f"Couplet {numero}:\n"
            f"Ne bɛ taa ni {theme} ye n hakili la,\n"
            f"{phrase_emotion}, n bɛ taa ka kan,\n"
            f"Donkili bɛ bɔ {signature},\n"
            f"Ka jigi mara tile bɛɛ la."
        )

    return (
        f"Couplet {numero}:\n"
        f"Je marche avec {theme} gravé dans la mémoire,\n"
        f"{phrase_emotion}, même au fond du soir,\n"
        f"La chanson prend forme {signature},\n"
        f"Et chaque ligne rallume notre histoire."
    )


def generer_refrain(theme: str, emotion: str, code_langue: str) -> str:
    assert theme != ""
    assert emotion in SUPPORTED_EMOTIONS

    phrase_emotion = obtenir_phrase_emotion(emotion, code_langue)

    if code_langue == "en":
        return (
            "Chorus:\n"
            f"{theme.title()}, we keep moving on,\n"
            f"{phrase_emotion}, strong until the dawn,\n"
            "Voices rise and carry the flame,\n"
            "Every heart remembers the name."
        )

    if code_langue == "bm":
        return (
            "Refrain:\n"
            f"{theme.title()}, an bɛ taa ɲɔgɔn fɛ,\n"
            f"{phrase_emotion}, jigi bɛ yen,\n"
            "Kanw bɛ wuli ka yeelen ta,\n"
            "Dusukun bɛ to ka donkili da."
        )

    return (
        "Refrain:\n"
        f"{theme.capitalize()}, on avance encore,\n"
        f"{phrase_emotion}, plus fort que le décor,\n"
        "Nos voix montent et gardent la flamme,\n"
        "Le même refrain traverse nos âmes."
    )


def generer_chanson(
    theme: str,
    emotion: str,
    langue: str,
    style: str,
    nombre_couplets: int,
) -> str:
    assert isinstance(nombre_couplets, int)
    assert 1 <= nombre_couplets <= 3

    theme_nettoye = nettoyer_theme(theme)
    code_langue = obtenir_code_langue(langue)
    prompt = construire_prompt(theme_nettoye, emotion, langue, style, nombre_couplets)

    assert "chanson" in prompt
    assert theme_nettoye != ""

    titre = generer_titre(theme_nettoye, emotion, code_langue)
    refrain = generer_refrain(theme_nettoye, emotion, code_langue)

    sections = [f"Titre : {titre}", ""]

    for numero in range(1, nombre_couplets + 1):
        couplet = generer_couplet(
            theme=theme_nettoye,
            emotion=emotion,
            style=style,
            code_langue=code_langue,
            numero=numero,
        )
        sections.append(couplet)
        sections.append("")
        sections.append(refrain)
        sections.append("")

    return "\n".join(sections).strip()