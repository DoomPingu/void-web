from level_system import level_fortschritt


TALENT_STUFEN = 7
UMLERNEN_GRUNDKOSTEN = 30

TALENT_RICHTUNGEN = {
    "klinge": "Klinge",
    "pfad": "Pfad",
    "werkstatt": "Werkstatt"
}

TALENTE = {
    # Stufe 1
    "ruhige_deckung": {
        "name": "Ruhige Deckung",
        "stufe": 1,
        "richtung": "klinge",
        "beschreibung": (
            "+5 Abwehr beim Verteidigen und "
            "+5 Paradechance in jeder Runde."
        ),
        "boni": {"verteidigung_chance": 5, "parade_chance": 5}
    },
    "faehrtenkunde": {
        "name": "Fährtenkunde",
        "stufe": 1,
        "richtung": "pfad",
        "beschreibung": (
            "Spuren in allen Jagdgebieten erkennst du "
            "schon ab Wahrnehmung 2 statt 3."
        ),
        "boni": {"wildspur_schwelle": 1}
    },
    "materialkunde": {
        "name": "Materialkunde",
        "stufe": 1,
        "richtung": "werkstatt",
        "beschreibung": (
            "Bjorns Arbeitskosten sinken um 2 Gold; "
            "Zutaten bleiben gleich."
        ),
        "boni": {"bjorn_goldrabatt": 2}
    },
    # Stufe 2
    "fokussierter_angriff": {
        "name": "Fokussierter Angriff",
        "stufe": 2,
        "richtung": "klinge",
        "beschreibung": (
            "Führt den ersten Angriff deiner Waffe mit "
            "+15 Prozentpunkten Trefferchance aus (höchstens 100 %). "
            "Bei bereits 100 % entsteht kein zusätzlicher Trefferbonus. "
            "Verbraucht eine Kampfrunde; in Runde 1 eingesetzt, "
            "ab Runde 4 wieder bereit."
        ),
        "boni": {"fokus_trefferchance": 15},
        "aktiv": True
    },
    "leiser_schritt": {
        "name": "Leiser Schritt",
        "stufe": 2,
        "richtung": "pfad",
        "beschreibung": (
            "Kampfbegegnungen auf Reisen sind etwa "
            "ein Viertel seltener. In den TIEFEN fällt "
            "das Vorbeischleichen leichter."
        ),
        "boni": {"reise_leise": 1}
    },
    "handelsgespuer": {
        "name": "Handelsgespür",
        "stufe": 2,
        "richtung": "werkstatt",
        "beschreibung": (
            "Hilda zahlt 2 Gold mehr pro Material und kauft dir "
            "auch Glutschuppen, Schieferplatten, Krebsscheren, "
            "Kreischerfedern und Hirschgeweihe ab."
        ),
        "boni": {"handel_bonus": 2}
    },
    # Stufe 3
    "zaehe_haut": {
        "name": "Zähe Haut",
        "stufe": 3,
        "richtung": "klinge",
        "beschreibung": (
            "Jeder gegnerische Treffer verursacht "
            "1 Schaden weniger."
        ),
        "boni": {"schutz": 1}
    },
    "feldverband": {
        "name": "Feldverband",
        "stufe": 3,
        "richtung": "pfad",
        "beschreibung": (
            "Heiltränke heilen 35 statt 30 Leben, "
            "ein Lagerfeuer 30 statt 25."
        ),
        "boni": {"heilung_bonus": 5}
    },
    "gute_kueche": {
        "name": "Gute Küche",
        "stufe": 3,
        "richtung": "werkstatt",
        "beschreibung": (
            "Mahlzeiten heilen 5 Leben mehr; ihre Wirkungen halten "
            "2 Schritte bzw. 1 Kampfrunde länger."
        ),
        "boni": {"mahlzeit_bonus": 5}
    },
    # Stufe 4
    "gegenschlag": {
        "name": "Gegenschlag",
        "stufe": 4,
        "richtung": "klinge",
        "beschreibung": (
            "Nach einer gelungenen Parade oder Abwehr macht dein "
            "Angriff in der nächsten Runde 25 % mehr Schaden "
            "(nicht zusätzlich zum Gegenangriff des Kriegers)."
        ),
        "boni": {"gegenschlag": 1}
    },
    "reiche_beute": {
        "name": "Reiche Beute",
        "stufe": 4,
        "richtung": "pfad",
        "beschreibung": (
            "In allen Jagdgebieten +10 Prozentpunkte "
            "Chance auf Materialien."
        ),
        "boni": {"jagd_materialchance": 10}
    },
    "geuebtes_auge": {
        "name": "Geübtes Auge",
        "stufe": 4,
        "richtung": "werkstatt",
        "beschreibung": (
            "+1 auf Wissens- und Wahrnehmungsproben beim Untersuchen "
            "und in Gesprächen. Gilt nicht für Klassenvoraussetzungen."
        ),
        "boni": {"untersuchung_bonus": 1}
    },
    # Stufe 5
    "unbeugsam": {
        "name": "Unbeugsam",
        "stufe": 5,
        "richtung": "klinge",
        "beschreibung": (
            "Einmal pro Kampf überstehst du einen "
            "tödlichen Treffer mit 1 Leben."
        ),
        "boni": {"unbeugsam": 1}
    },
    "fluchtinstinkt": {
        "name": "Fluchtinstinkt",
        "stufe": 5,
        "richtung": "pfad",
        "beschreibung": "+15 Prozentpunkte Fluchtchance.",
        "boni": {"flucht_bonus": 15}
    },
    "sorgfaeltige_pflege": {
        "name": "Sorgfältige Pflege",
        "stufe": 5,
        "richtung": "werkstatt",
        "beschreibung": (
            "Vorbereitete Waffenpflege wirkt den ganzen Kampf "
            "statt drei Angriffe."
        ),
        "boni": {"pflege_ganzer_kampf": 1}
    },
    # Stufe 6
    "standhaft": {
        "name": "Standhaft",
        "stufe": 6,
        "richtung": "klinge",
        "beschreibung": (
            "Gegner ab 120 Lebenspunkten (Revierherren, Wächter) "
            "richten 5 % weniger Schaden an."
        ),
        "boni": {"standhaft": 1}
    },
    "nachtauge": {
        "name": "Nachtauge",
        "stufe": 6,
        "richtung": "pfad",
        "beschreibung": (
            "Du bemerkst Gegner früher, und im Dunkeln wiegt der Abzug "
            "ein Drittel weniger. Seltene Entdeckungen auf Reisen "
            "zeigen sich doppelt so oft."
        ),
        "boni": {"nachtauge": 1}
    },
    "griffbereit": {
        "name": "Griffbereit",
        "stufe": 6,
        "richtung": "werkstatt",
        "beschreibung": (
            "Der erste Gegenstand in jedem Kampf kostet keine Runde; "
            "danach kannst du noch handeln."
        ),
        "boni": {"griffbereit": 1}
    },
    # Stufe 7
    "zweiter_atem": {
        "name": "Zweiter Atem",
        "stufe": 7,
        "richtung": "klinge",
        "beschreibung": (
            "Einmal pro Kampf: Senkt ein Treffer deine Leben von 30 oder "
            "mehr auf 1 bis 29, gewinnst du sofort 12 Leben zurück. "
            "Kostet keine Runde."
        ),
        "boni": {"zweiter_atem": 1}
    },
    "wachsam": {
        "name": "Wachsam",
        "stufe": 7,
        "richtung": "pfad",
        "beschreibung": (
            "Hinterhalte sind halb so häufig, und Überraschungen wiegen in "
            "der ersten Runde nur halb so schwer. Bemerkst du einen "
            "gewöhnlichen Gegner auf Reisen rechtzeitig, kannst du ihn "
            "unbemerkt umgehen (ohne Beute)."
        ),
        "boni": {"wachsam": 1}
    },
    "heilkundige_hand": {
        "name": "Heilkundige Hand",
        "stufe": 7,
        "richtung": "werkstatt",
        "beschreibung": (
            "Stoppt eine Bandage eine Blutung, heilt sie zusätzlich "
            "8 Leben. Wundsalben heilen 15 statt 8 Leben."
        ),
        "boni": {"heilkundig": 1}
    }
}


def talent_system_sicherstellen(spieler_daten):
    level_fortschritt(spieler_daten)
    daten = spieler_daten["entwicklung"]
    gelernt = daten.get("talente")

    if not isinstance(gelernt, list):
        gelernt = []

    bereinigt = []

    for talent_id in gelernt:
        if (
            isinstance(talent_id, str)
            and talent_id in TALENTE
            and talent_id not in bereinigt
        ):
            bereinigt.append(talent_id)

    daten["talente"] = bereinigt


def talente_der_stufe(stufe):
    return [
        talent_id
        for talent_id, daten in TALENTE.items()
        if daten["stufe"] == stufe
    ]


def talent_der_stufe(spieler_daten, stufe):
    talent_system_sicherstellen(spieler_daten)

    for talent_id in spieler_daten["entwicklung"]["talente"]:
        if TALENTE[talent_id]["stufe"] == stufe:
            return talent_id

    return None


def talentstufen_frei(spieler_daten):
    return min(
        TALENT_STUFEN,
        level_fortschritt(spieler_daten)["talentpunkte_verdient"]
    )


def talentpunkte_verfuegbar(spieler_daten):
    talent_system_sicherstellen(spieler_daten)

    return sum(
        1
        for stufe in range(1, talentstufen_frei(spieler_daten) + 1)
        if talent_der_stufe(spieler_daten, stufe) is None
    )


def talent_gelernt(spieler_daten, talent_id):
    talent_system_sicherstellen(spieler_daten)

    return (
        talent_id
        in spieler_daten["entwicklung"]["talente"]
    )


def talent_lernen(spieler_daten, talent_id):
    if (
        not isinstance(talent_id, str)
        or talent_id not in TALENTE
    ):
        return False

    if talent_gelernt(spieler_daten, talent_id):
        return False

    if talent_lernhindernis(spieler_daten, talent_id):
        return False

    spieler_daten["entwicklung"]["talente"].append(
        talent_id
    )

    return True


def talent_bonus(spieler_daten, bonus_id):
    talent_system_sicherstellen(spieler_daten)

    return sum(
        TALENTE[talent_id]["boni"].get(bonus_id, 0)
        for talent_id in spieler_daten["entwicklung"]["talente"]
    )



def talent_lernhindernis(spieler_daten, talent_id):
    if (
        not isinstance(talent_id, str)
        or talent_id not in TALENTE
    ):
        return "Unbekanntes Talent."

    daten = TALENTE[talent_id]
    stufe = daten["stufe"]

    if talentstufen_frei(spieler_daten) < stufe:
        return f"Benötigt Level {stufe}."

    gewaehlt = talent_der_stufe(spieler_daten, stufe)

    if gewaehlt is not None:
        return (
            f"Auf dieser Stufe hast du bereits "
            f"{TALENTE[gewaehlt]['name']} gewählt."
        )

    if talent_id == "fokussierter_angriff":
        if (
            spieler_daten.get("prolog_status")
            != "prolog_abgeschlossen"
        ):
            return "Schließe zuerst den Prolog ab."

        if spieler_daten.get("bjorn_fokus_uebung") is not True:
            return "Absolviere zuerst die Waffenübung bei Bjorn."

    return None


def talente_regel_pruefen(spieler_daten):
    """Ältere Spielstände mit mehreren Talenten derselben Stufe werden
    einmalig zurückgesetzt; danach wählt der Spieler kostenlos neu."""
    talent_system_sicherstellen(spieler_daten)
    gelernt = spieler_daten["entwicklung"]["talente"]
    stufen = [TALENTE[talent_id]["stufe"] for talent_id in gelernt]

    if len(stufen) == len(set(stufen)):
        return False

    spieler_daten["entwicklung"]["talente"] = []
    return True


def talent_neuwahlen(spieler_daten):
    talent_system_sicherstellen(spieler_daten)
    anzahl = spieler_daten["entwicklung"].get("talent_neuwahlen", 0)

    if (
        isinstance(anzahl, bool)
        or not isinstance(anzahl, int)
        or anzahl < 0
    ):
        anzahl = 0

    return anzahl


def umlernkosten(spieler_daten):
    return UMLERNEN_GRUNDKOSTEN * 2 ** talent_neuwahlen(spieler_daten)


def talente_zuruecksetzen(spieler_daten):
    """Bezahlte Neuwahl; das Gold zieht der Aufrufer ab."""
    anzahl = talent_neuwahlen(spieler_daten)
    spieler_daten["entwicklung"]["talente"] = []
    spieler_daten["entwicklung"]["talent_neuwahlen"] = anzahl + 1
    return True