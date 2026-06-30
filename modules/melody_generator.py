from io import BytesIO
from typing import Dict, List

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo


EMOTION_CONFIGS = {
    "Joyeux": {
        "tempo": 120,
        "tonalite": "Do majeur",
        "notes": [60, 64, 67, 72, 67, 64, 60, 64],
    },
    "Triste": {
        "tempo": 70,
        "tonalite": "La mineur",
        "notes": [57, 60, 64, 60, 57, 55, 57, 60],
    },
    "Motivant": {
        "tempo": 100,
        "tonalite": "Ré mineur",
        "notes": [62, 65, 69, 74, 69, 65, 62, 65],
    },
    "Romantique": {
        "tempo": 80,
        "tonalite": "Sol majeur",
        "notes": [67, 71, 74, 79, 74, 71, 67, 71],
    },
    "Nostalgique": {
        "tempo": 75,
        "tonalite": "Mi mineur",
        "notes": [64, 67, 71, 76, 71, 67, 64, 62],
    },
}


STYLE_DURATIONS = {
    "Rap": 360,
    "Pop": 480,
    "Afro": 300,
    "Traditionnel": 600,
}


def obtenir_configuration_emotion(emotion: str) -> Dict[str, object]:
    assert isinstance(emotion, str)
    assert len(EMOTION_CONFIGS) == 5

    return EMOTION_CONFIGS.get(emotion, EMOTION_CONFIGS["Motivant"])


def obtenir_duree_note(style: str) -> int:
    assert isinstance(style, str)
    assert len(STYLE_DURATIONS) == 4

    return STYLE_DURATIONS.get(style, 480)


def construire_sequence_notes(notes_base: List[int], nombre_couplets: int) -> List[int]:
    assert isinstance(notes_base, list)
    assert 1 <= nombre_couplets <= 3

    sequence = []

    for _ in range(nombre_couplets + 1):
        sequence.extend(notes_base)

    return sequence


def ajouter_note(track: MidiTrack, note: int, duree: int) -> None:
    assert isinstance(note, int)
    assert 0 <= note <= 127

    velocite = 64

    track.append(Message("note_on", note=note, velocity=velocite, time=0))
    track.append(Message("note_off", note=note, velocity=velocite, time=duree))


def creer_fichier_midi(
    notes: List[int],
    tempo: int,
    duree_note: int,
) -> bytes:
    assert isinstance(notes, list)
    assert tempo > 0

    fichier_midi = MidiFile(type=0, ticks_per_beat=480)
    piste = MidiTrack()
    fichier_midi.tracks.append(piste)

    piste.append(MetaMessage("track_name", name="Melodie generee", time=0))
    piste.append(MetaMessage("set_tempo", tempo=bpm2tempo(tempo), time=0))
    piste.append(MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    piste.append(Message("program_change", channel=0, program=0, time=0))

    for note in notes:
        piste.append(Message("note_on", channel=0, note=note, velocity=80, time=0))
        piste.append(Message("note_off", channel=0, note=note, velocity=80, time=duree_note))

    piste.append(MetaMessage("end_of_track", time=0))

    buffer = BytesIO()
    fichier_midi.save(file=buffer)
    buffer.seek(0)

    return buffer.getvalue()


def normaliser_nom_fichier(emotion: str, style: str) -> str:
    assert isinstance(emotion, str)
    assert isinstance(style, str)

    nom = f"melodie_{emotion}_{style}".lower()
    nom = nom.replace(" ", "_")
    nom = nom.replace("é", "e").replace("è", "e").replace("ê", "e")
    nom = nom.replace("à", "a").replace("ù", "u").replace("ç", "c")

    return f"{nom}.mid"


def generer_melodie_midi(
    emotion: str,
    style: str,
    nombre_couplets: int,
) -> Dict[str, object]:
    assert isinstance(nombre_couplets, int)
    assert 1 <= nombre_couplets <= 3

    configuration = obtenir_configuration_emotion(emotion)
    duree_note = obtenir_duree_note(style)

    notes_base = configuration["notes"]
    tempo = int(configuration["tempo"])
    tonalite = str(configuration["tonalite"])

    assert isinstance(notes_base, list)
    assert len(notes_base) > 0

    sequence_notes = construire_sequence_notes(
        notes_base=notes_base,
        nombre_couplets=nombre_couplets,
    )

    contenu_midi = creer_fichier_midi(
        notes=sequence_notes,
        tempo=tempo,
        duree_note=duree_note,
    )

    return {
        "nom_fichier": normaliser_nom_fichier(emotion, style),
        "tempo": tempo,
        "tonalite": tonalite,
        "nombre_notes": len(sequence_notes),
        "contenu": contenu_midi,
    }