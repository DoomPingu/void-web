import random
import time
import os

FARBEN = {
    "rot": "\033[31m",
    "gruen": "\033[32m",
    "gelb": "\033[33m",
    "blau": "\033[94m",
    "reset": "\033[0m"
}

TEXT_TEMPO = {
    "kampf": 0.3,
    "rundenwechsel": 0.5
}

def ansi_farben_aktivieren():
    if os.name != "nt":
        return True

    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)

        modus = ctypes.c_uint32()

        if not kernel32.GetConsoleMode(handle, ctypes.byref(modus)):
            return False

        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

        return bool(
            kernel32.SetConsoleMode(
                handle,
                modus.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
            )
        )

    except Exception:
        return False


ANSI_FARBEN_AKTIV = ansi_farben_aktivieren()


def farbig_ausgeben(text, farbe):
    if ANSI_FARBEN_AKTIV:
        print(FARBEN[farbe] + text + FARBEN["reset"])
    else:
        print(text)

def text_pause(art):
    time.sleep(TEXT_TEMPO[art])

def bildschirm_leeren():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )


def kampf_auswahl_trenner():
    print() 
    print("-" * 34)
    print()


def kampf_eingabe(gueltige_werte):
    gueltige_werte = tuple(
        str(wert) for wert in gueltige_werte
    )

    fehler = False

    while True:
        if fehler and ANSI_FARBEN_AKTIV:
            print(
                "\033[F\033[2K",
                end="",
                flush=True
            )

        if fehler:
            prompt = "Ungültig – erneut > "
        else:
            prompt = "> "

        eingabe = input(prompt).strip().lower()

        if eingabe in gueltige_werte:
            if fehler and ANSI_FARBEN_AKTIV:
                print(
                    "\033[F\033[2K",
                    end="",
                    flush=True
                )

                print(f"> {eingabe}")

            kampf_auswahl_trenner()

            return eingabe

        if not ANSI_FARBEN_AKTIV:
            print("Ungültige Eingabe.")

        fehler = True


# =========================
# STATUS-EFFEKTE
# =========================

def kampf_status_kopieren(status_effekte):
    if not isinstance(status_effekte, dict):
        return {}

    return {
        status_id: daten.copy()
        for status_id, daten in status_effekte.items()
        if isinstance(daten, dict)
    }


def kampf_status_modifikator(
    status_effekte,
    status_definitionen,
    wert_id,
    einheit=None
):
    gesamt = 0

    for status_id, aktiv_daten in status_effekte.items():
        if (
            einheit is not None
            and aktiv_daten.get("einheit") != einheit
        ):
            continue

        definition = status_definitionen.get(
            status_id,
            {}
        )

        modifikator = definition.get(
            "modifikatoren",
            {}
        ).get(
            wert_id,
            0
        )

        if not isinstance(
            modifikator,
            (int, float)
        ):
            continue

        stapel = max(
            1,
            aktiv_daten.get(
                "stapel",
                1
            )
        )

        gesamt += modifikator * stapel

    return gesamt


def kampf_status_bereinigen(
    status_effekte,
    status_definitionen,
    meldung=True
):
    for status_id, aktiv_daten in list(
        status_effekte.items()
    ):
        if aktiv_daten.get("einheit") != "runden":
            continue

        dauer = aktiv_daten.get(
            "dauer"
        )

        if not isinstance(
            dauer,
            (int, float)
        ):
            continue

        if dauer > 0:
            continue

        status_effekte.pop(
            status_id,
            None
        )

        if meldung:
            name = status_definitionen.get(
                status_id,
                {}
            ).get(
                "name",
                status_id
            )

            print()
            print(
                f"{name} ist abgeklungen."
            )


def kampf_status_hinzufuegen(
    status_effekte,
    status_definitionen,
    status_id,
    quelle=None
):
    definition = status_definitionen.get(
        status_id
    )

    if not definition:
        return False

    dauer = definition.get(
        "standard_dauer"
    )

    einheit = definition.get(
        "standard_einheit"
    )

    vorhanden = status_effekte.get(
        status_id
    )

    if vorhanden:
        if definition.get(
            "stapelbar",
            False
        ):
            vorhanden["stapel"] = min(
                definition.get(
                    "max_stapel",
                    1
                ),
                vorhanden.get(
                    "stapel",
                    1
                ) + 1
            )

        vorhandene_dauer = vorhanden.get(
            "dauer"
        )

        if (
            isinstance(
                dauer,
                (int, float)
            )
            and isinstance(
                vorhandene_dauer,
                (int, float)
            )
        ):
            vorhanden["dauer"] = max(
                vorhandene_dauer,
                dauer
            )

        vorhanden[
            "einheit"
        ] = einheit

        vorhanden[
            "quelle"
        ] = quelle

    else:
        status_effekte[status_id] = {
            "dauer": dauer,
            "einheit": einheit,
            "stapel": 1,
            "quelle": quelle
        }

    name = definition.get(
        "name",
        status_id
    )

    print()

    farbig_ausgeben(
        f"Status: {name}",
        "rot"
    )

    return True


def kampf_status_rundenstart(
    spieler,
    status_effekte,
    status_definitionen
):
    kampf_status_bereinigen(
        status_effekte,
        status_definitionen
    )

    schaden_bonus = kampf_status_modifikator(
        status_effekte,
        status_definitionen,
        "schaden_bonus",
        einheit="runden"
    )

    for status_id, aktiv_daten in list(
        status_effekte.items()
    ):
        if aktiv_daten.get(
            "einheit"
        ) != "runden":
            continue

        dauer = aktiv_daten.get(
            "dauer"
        )

        if (
            not isinstance(
                dauer,
                (int, float)
            )
            or dauer <= 0
        ):
            continue

        definition = status_definitionen.get(
            status_id,
            {}
        )

        tick_schaden = definition.get(
            "schaden_pro_tick",
            0
        )

        if (
            isinstance(
                tick_schaden,
                (int, float)
            )
            and tick_schaden > 0
        ):
            stapel = max(
                1,
                aktiv_daten.get(
                    "stapel",
                    1
                )
            )

            schaden = int(
                tick_schaden * stapel
            )

            spieler["hp"] = max(
                0,
                spieler["hp"] - schaden
            )

            name = definition.get(
                "name",
                status_id
            )

            farbig_ausgeben(
                f"{name}: Du erleidest "
                f"{schaden} Schaden.",
                "rot"
            )

        aktiv_daten[
            "dauer"
        ] = dauer - 1

    return schaden_bonus

def kampf_status_nach_gegnertreffer(
    gegner,
    gegner_treffer_art,
    gegner_schaden,
    gegner_krit,
    status_effekte,
    status_definitionen,
    gegner_spezialangriff=False,
    wolf_sprung=False,
    keiler_ansturm=False
):
    if gegner_schaden <= 0:
        return False

    if gegner_treffer_art not in (
        "voll",
        "streif"
    ):
        return False

    gegner_typ = gegner.get(
        "typ"
    )

    if gegner_typ == "Bandit":
        chance = 8

    elif gegner_typ == "Wolf":
        chance = 10

    elif gegner_typ == "Keiler":
        chance = 8

    else:
        return False

    if gegner_treffer_art == "streif":
        chance = 3

    if gegner_spezialangriff:
        chance += 8

    if wolf_sprung:
        chance += 8

    if keiler_ansturm:
        chance += 10

    if gegner_krit:
        chance += 5

    chance = max(
        0,
        min(
            30,
            chance
        )
    )

    if random.randint(
        1,
        100
    ) > chance:
        return False

    return kampf_status_hinzufuegen(
        status_effekte,
        status_definitionen,
        "bluten",
        quelle=f"kampf:{gegner_typ}"
    )



# =========================
# SPIELER / GEGNER
# =========================
def kampf_starten(
    lebenspunkte=100,
    heiltraenke=1,
    waffe=None,
    gegner_typ=None,
    kampfwerte=None,
    status_effekte=None,
    status_definitionen=None,
    kampf_situation=None,
    bandagen=0,
    wurfnetze=0,
    wundsalben=0,
    wundsalbe_heilung=8,
    gegengifte=0
):
    status_effekte = kampf_status_kopieren(
        status_effekte
    )

    if not isinstance(
        status_definitionen,
        dict
    ):
        status_definitionen = {}
    if not isinstance(
        kampfwerte,
        dict
    ):
        kampfwerte = {}


    speer = {
        "typ": "Speer",
        "wendigkeit": 1,
        "parade": 1,
        "reichweite": 3,
        "schaden_min": 12,
        "schaden_max": 18
    }

    schwert = {
        "typ": "Schwert",
        "wendigkeit": 2,
        "parade": 2,
        "reichweite": 1,
        "schaden_min": 10,
        "schaden_max": 16
    }

    hammer = {
        "typ": "Hammer",
        "name": "Hammer des Weges",
        "wendigkeit": 1,
        "parade": 1,
        "reichweite": 1,
        "schaden_min": 20,
        "schaden_max": 30
    }

    beil = {
        "typ": "Beil",
        "wendigkeit": 1,
        "parade": 1,
        "reichweite": 1,
        "schaden_min": 8,
        "schaden_max": 16
    }

    stab = {
        "typ": "Stab",
        "wendigkeit": 2,
        "parade": 3,
        "reichweite": 3,
        "schaden_min": 10,
        "schaden_max": 14
    }

    messer = {
        "typ": "Messer",
        "wendigkeit": 3,
        "parade": 1,
        "reichweite": 1,
        "schaden_min": 11,
        "schaden_max": 13
    }

    spieler = {
        "hp": 100,
        "max_hp": 100,

        "wahrnehmung": 1,
        "geschick": 1,
        "staerke": 1,
        "ausdauer": 1,
        "zaehigkeit": 1,
        "sensibilitaet": 0,

        "vitalitaet": 2,
        "intelligenz": 2,
        "glück": 2,

        "heiltraenke": 1,
        "waffe": speer
    }

    for wert_id in (
        "wahrnehmung",
        "geschick",
        "staerke",
        "ausdauer",
        "zaehigkeit",
        "sensibilitaet"
    ):
        wert = kampfwerte.get(
            wert_id
        )

        if (
            isinstance(
                wert,
                (int, float)
            )
            and not isinstance(
                wert,
                bool
            )
        ):
            spieler[
                wert_id
            ] = max(
                0,
                int(wert)
            )

    spieler["max_hp"] = (
        84
        + spieler["vitalitaet"]
        * 8
    )
    spieler["hp"] = max(0, min(lebenspunkte, spieler["max_hp"]))
    spieler["wurfnetze"] = max(0, wurfnetze) if type(wurfnetze) is int else 0
    spieler["wundsalben"] = max(0, wundsalben) if type(wundsalben) is int else 0
    spieler["gegengifte"] = max(0, gegengifte) if type(gegengifte) is int else 0
    spieler["heiltraenke"] = max(0, heiltraenke)
    spieler["bandagen"] = (
        max(0, bandagen)
        if isinstance(bandagen, int) and not isinstance(bandagen, bool)
        else 0
    )
    spieler["wahrnehmung"] += kampf_status_modifikator(
        status_effekte,
        status_definitionen,
        "kampf_wahrnehmung"
    )
    if waffe is not None:

        waffen_name = waffe.get(
            "name",
            "Unbekannte Waffe"
        )

        waffen_typ = waffe.get(
            "typ",
            ""
        )

        if (
            waffen_typ == "Schwert"
            or "Schwert" in waffen_name
        ):
            kampf_waffe = schwert.copy()

        elif (
            waffen_typ == "Speer"
            or "Speer" in waffen_name
        ):
            kampf_waffe = speer.copy()

        elif (
            waffen_typ == "Hammer"
            or "Hammer" in waffen_name
        ):
            kampf_waffe = hammer.copy()

        elif (
            waffen_typ == "Beil"
            or "Beil" in waffen_name
        ):
            kampf_waffe = beil.copy()

        elif (
            waffen_typ == "Stab"
            or "Stab" in waffen_name
        ):
            kampf_waffe = stab.copy()

        elif (
            waffen_typ == "Messer"
            or "Messer" in waffen_name
        ):
            kampf_waffe = messer.copy()

        else:
            raise ValueError(
                f"Unbekannter Waffentyp: {waffen_name}"
            )

        kampf_waffe["name"] = waffen_name
        kampf_waffe["schaden_min"] = waffe["min_schaden"]
        kampf_waffe["schaden_max"] = waffe["max_schaden"]

        for wert in [
            "wendigkeit",
            "parade",
            "reichweite"
        ]:
            if wert in waffe:
                kampf_waffe[wert] = waffe[wert]

        spieler["waffe"] = kampf_waffe

    bandit = {
        "typ": "Bandit", "hp": 75, "max_hp": 75, "wahrnehmung": 2, "waldkenntnis": 1, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Dolch", "wendigkeit": 3, "parade": 1, "reichweite": 0, "schaden_min": 8, "schaden_max": 13}
    }

    wolf = {
        "typ": "Wolf", "hp": 60, "max_hp": 60, "wahrnehmung": 4, "waldkenntnis": 3, "verstecken": 3,
        "angriffsart": "Nahkampf", "krit_chance": 7,
        "waffe": {"typ": "Biss", "wendigkeit": 4, "parade": 0, "reichweite": 0, "schaden_min": 7, "schaden_max": 11}
    }

    kohlenschmuggler = {
        "typ": "Kohlenschmuggler", "hp": 65, "max_hp": 65, "wahrnehmung": 3, "waldkenntnis": 2, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Knüppel", "wendigkeit": 3, "parade": 1, "reichweite": 0, "schaden_min": 7, "schaden_max": 12}
    }

    rudelloser_wolf = {
        "typ": "Rudelloser Wolf", "hp": 70, "max_hp": 70, "wahrnehmung": 4, "waldkenntnis": 3, "verstecken": 3,
        "angriffsart": "Nahkampf", "krit_chance": 6,
        "waffe": {"typ": "Biss", "wendigkeit": 4, "parade": 0, "reichweite": 0, "schaden_min": 10, "schaden_max": 14}
    }

    echohirsch = {
        "typ": "Echohirsch", "hp": 75, "max_hp": 75, "wahrnehmung": 4, "waldkenntnis": 3, "verstecken": 3,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Geweih", "wendigkeit": 3, "parade": 0, "reichweite": 1, "schaden_min": 10, "schaden_max": 14}
    }

    blasser_hirsch = {
        "typ": "Blasser Hirsch", "hp": 140, "max_hp": 140, "wahrnehmung": 5, "waldkenntnis": 4, "verstecken": 4,
        "angriffsart": "Nahkampf", "krit_chance": 6,
        "waffe": {"typ": "Geweih", "wendigkeit": 3, "parade": 0, "reichweite": 1, "schaden_min": 11, "schaden_max": 15}
    }

    aschenkoenig = {
        "typ": "Aschenkönig", "hp": 160, "max_hp": 160, "wahrnehmung": 3, "waldkenntnis": 2, "verstecken": 3,
        "angriffsart": "Nahkampf", "krit_chance": 6,
        "waffe": {"typ": "Biss", "wendigkeit": 2, "parade": 0, "reichweite": 0, "schaden_min": 12, "schaden_max": 17}
    }

    steinvater = {
        "typ": "Steinvater", "hp": 160, "max_hp": 160, "wahrnehmung": 2, "waldkenntnis": 2, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Biss", "wendigkeit": 1, "parade": 0, "reichweite": 0, "schaden_min": 11, "schaden_max": 16}
    }

    einscherer = {
        "typ": "Einscherer", "hp": 160, "max_hp": 160, "wahrnehmung": 2, "waldkenntnis": 1, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Schere", "wendigkeit": 1, "parade": 0, "reichweite": 0, "schaden_min": 12, "schaden_max": 17}
    }

    graupelz = {
        "typ": "Graupelz", "hp": 130, "max_hp": 130, "wahrnehmung": 5, "waldkenntnis": 4, "verstecken": 3,
        "angriffsart": "Nahkampf", "krit_chance": 8,
        "waffe": {"typ": "Biss", "wendigkeit": 5, "parade": 0, "reichweite": 0, "schaden_min": 10, "schaden_max": 15}
    }

    gezeitenkrebs = {
        "typ": "Gezeitenkrebs", "hp": 85, "max_hp": 85, "wahrnehmung": 2, "waldkenntnis": 1, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 4,
        "waffe": {"typ": "Schere", "wendigkeit": 1, "parade": 0, "reichweite": 0, "schaden_min": 9, "schaden_max": 13}
    }

    wrackpluenderer = {
        "typ": "Wrackplünderer", "hp": 70, "max_hp": 70, "wahrnehmung": 3, "waldkenntnis": 1, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Haken", "wendigkeit": 3, "parade": 1, "reichweite": 0, "schaden_min": 8, "schaden_max": 12}
    }

    schieferpanzer = {
        "typ": "Schieferpanzer", "hp": 95, "max_hp": 95, "wahrnehmung": 2, "waldkenntnis": 2, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 4,
        "waffe": {"typ": "Biss", "wendigkeit": 1, "parade": 0, "reichweite": 0, "schaden_min": 9, "schaden_max": 14}
    }

    kreischer = {
        "typ": "Kreischer", "hp": 70, "max_hp": 70, "wahrnehmung": 5, "waldkenntnis": 3, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 6,
        "waffe": {"typ": "Krallen", "wendigkeit": 4, "parade": 0, "reichweite": 0, "schaden_min": 10, "schaden_max": 14}
    }

    glutsalamander = {
        "typ": "Glutsalamander", "hp": 80, "max_hp": 80, "wahrnehmung": 3, "waldkenntnis": 2, "verstecken": 3,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Biss", "wendigkeit": 2, "parade": 0, "reichweite": 0, "schaden_min": 9, "schaden_max": 13}
    }

    keiler = {
        "typ": "Keiler", "hp": 90, "max_hp": 90, "wahrnehmung": 2, "waldkenntnis": 2, "verstecken": 1,
        "angriffsart": "Nahkampf", "krit_chance": 4,
        "waffe": {"typ": "Hauer", "wendigkeit": 1, "parade": 0, "reichweite": 0, "schaden_min": 10, "schaden_max": 15}
    }


    schachtflatterer = {
        "typ": "Schachtflatterer", "hp": 70, "max_hp": 70, "wahrnehmung": 4, "waldkenntnis": 0, "verstecken": 3,
        "angriffsart": "Nahkampf", "krit_chance": 6,
        "waffe": {"typ": "Krallen", "wendigkeit": 5, "parade": 0, "reichweite": 0, "schaden_min": 10, "schaden_max": 14}
    }

    schachtkriecher = {
        "typ": "Schachtkriecher", "hp": 100, "max_hp": 100, "wahrnehmung": 2, "waldkenntnis": 0, "verstecken": 4,
        "angriffsart": "Nahkampf", "krit_chance": 4,
        "waffe": {"typ": "Kiefer", "wendigkeit": 1, "parade": 0, "reichweite": 0, "schaden_min": 10, "schaden_max": 14}
    }

    schachtspinner = {
        "typ": "Schachtspinner", "hp": 90, "max_hp": 90, "wahrnehmung": 3, "waldkenntnis": 0, "verstecken": 4,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Biss", "wendigkeit": 3, "parade": 0, "reichweite": 0, "schaden_min": 10, "schaden_max": 14}
    }

    blindmolch = {
        "typ": "Blindmolch", "hp": 160, "max_hp": 160, "wahrnehmung": 4, "waldkenntnis": 0, "verstecken": 2,
        "angriffsart": "Nahkampf", "krit_chance": 5,
        "waffe": {"typ": "Biss", "wendigkeit": 2, "parade": 0, "reichweite": 1, "schaden_min": 12, "schaden_max": 17}
    }

    # =========================
    # AKTUELLE SITUATION
    # =========================

    situation = {
        "gebiet": "Wald",
        "umgebung": "Lichtung",
        "tageszeit": "Tag",
        "wetter": "Klar"
    }

    if isinstance(
        kampf_situation,
        dict
    ):
        for schluessel in (
            "gebiet",
            "umgebung",
            "tageszeit",
            "wetter"
        ):
            wert = kampf_situation.get(
                schluessel
            )

            if (
                isinstance(
                    wert,
                    str
                )
                and wert.strip()
            ):
                situation[
                    schluessel
                ] = wert.strip()

    # =========================
    # KAMPFEFFEKTE
    # =========================

    effekte = {
        "trefferchance_spieler": 0,
        "trefferchance_gegner": 0,
        "ausweichchance_spieler": 0,
        "ausweichchance_gegner": 0,
        "fluchtchance": 0,
        "krit_chance_spieler": 0,
        "krit_chance_gegner": 0,
        "paradechance_spieler": 0
    }

    start_effekte = {
        "trefferchance_gegner": 0,
        "ausweichchance_spieler": 0,
        "krit_chance_gegner": 0,
        "paradechance_spieler": 0
    }

    # =========================
    # UMGEBUNGSWERTE
    # =========================

    deckung = 0
    versteckmoeglichkeiten = 0
    bewegungsfreiheit = 0
    hinterhaltspotential = 0
    umgebungs_sicht = 0

    # =========================
    # REGION
    # =========================

    # Die Region bestimmt später hauptsächlich:
    # Gegner, Tiere, Ressourcen und Loot.
    # Kampfeffekte kommen von der konkreten Umgebung.

    # =========================
    # KAMPFUMGEBUNG
    # =========================

    if situation["umgebung"] == "Dichter Wald":
        deckung += 2
        umgebungs_sicht -= 2
        versteckmoeglichkeiten += 2
        bewegungsfreiheit -= 1
        hinterhaltspotential += 2

    elif situation["umgebung"] == "Lichtung":
        umgebungs_sicht += 1
        bewegungsfreiheit += 1

    elif situation["umgebung"] == "Wildspur":
        versteckmoeglichkeiten += 1
        hinterhaltspotential += 1

    elif situation["umgebung"] == "Enge Ruine":
        deckung += 1
        umgebungs_sicht -= 1
        bewegungsfreiheit -= 1

    elif situation["umgebung"] == "Offener Weg":
        bewegungsfreiheit += 1

    elif situation["umgebung"] == "Dunkle Tiefe":
        umgebungs_sicht -= 3
        bewegungsfreiheit -= 1

    elif situation["umgebung"] == "Tiefe mit Licht":
        umgebungs_sicht -= 1
        bewegungsfreiheit -= 1

    # =========================
    # TAGESZEIT
    # =========================

    if situation["tageszeit"] == "Nacht":
        umgebungs_sicht -= 2

    # =========================
    # WETTER
    # =========================

    if situation["wetter"] == "Regen":
        umgebungs_sicht -= 1
        bewegungsfreiheit -= 1

    # =========================
    # SPIELERWERTE
    # =========================

    staerke_schaden_faktor = 1.0 + (spieler["staerke"] - 2) * 0.03
    staerke_schaden_faktor = max(0.90, min(1.25, staerke_schaden_faktor))

    ausdauer_stufen = max(
        0,
        min(
            3,
            spieler["ausdauer"] - 1
        )
    )

    zaehigkeit_stufen = max(
        0,
        min(
            3,
            spieler["zaehigkeit"] - 1
        )
    )

    ausdauer_verteidigung_bonus = (
        ausdauer_stufen * 5
    )

    talent_verteidigung_bonus = kampfwerte.get(
        "talent_verteidigung_bonus",
        0
    )

    if (
        not isinstance(talent_verteidigung_bonus, int)
        or isinstance(talent_verteidigung_bonus, bool)
        or talent_verteidigung_bonus not in (0, 5)
    ):
        talent_verteidigung_bonus = 0

    fokus_treffer_bonus = kampfwerte.get(
        "fokus_treffer_bonus",
        0
    )

    if (
        not isinstance(fokus_treffer_bonus, int)
        or isinstance(fokus_treffer_bonus, bool)
        or fokus_treffer_bonus not in (0, 15)
    ):
        fokus_treffer_bonus = 0

    glutkrieger_gelernt = kampfwerte.get("glutkrieger_gelernt") is True
    glutkrieger_portion_bereit = glutkrieger_gelernt and kampfwerte.get("glutkrieger_portion") is True
    stahlkrieger_gelernt = kampfwerte.get("stahlkrieger_gelernt") is True
    waffenpflege_bonus = 4 if stahlkrieger_gelernt and kampfwerte.get("stahlkrieger_waffenpflege") is True else 2
    waffenpflege_anwendungen = 3 if kampfwerte.get("schmied_waffenpflege") is True else 0

    def talentwert(schluessel, erlaubt):
        wert = kampfwerte.get(schluessel, 0)
        if isinstance(wert, bool) or wert not in erlaubt:
            return 0
        return wert

    talent_parade_bonus = talentwert("talent_parade_bonus", (0, 5))
    talent_flucht_bonus = talentwert("talent_flucht_bonus", (0, 15))
    talent_heiltrank_bonus = talentwert("talent_heiltrank_bonus", (0, 5))
    talent_gegenschlag = kampfwerte.get("talent_gegenschlag") is True
    talent_unbeugsam = kampfwerte.get("talent_unbeugsam") is True
    talent_standhaft = kampfwerte.get("talent_standhaft") is True
    talent_nachtauge = kampfwerte.get("talent_nachtauge") is True
    # Plattenweste (Blutungsschutz in Prozent) und Flatterhautbinde (milderer Dunkelheitsabzug).
    blutungsschutz = talentwert("blutungsschutz", (0, 50))
    dunkel_milder = talentwert("dunkel_milder", (0, 5))
    talent_griffbereit = kampfwerte.get("talent_griffbereit") is True
    talent_zweiter_atem = kampfwerte.get("talent_zweiter_atem") is True
    talent_wachsam = kampfwerte.get("talent_wachsam") is True
    talent_heilkundig = kampfwerte.get("talent_heilkundig") is True
    # Umgehen nur, wenn das Reisesystem es für diese Begegnung erlaubt.
    reise_umgehen = talent_wachsam and kampfwerte.get("reise_umgehen") is True
    umgangen = False
    zweiter_atem_genutzt = False
    griffbereit_genutzt = False
    waffenpflege_ganzer_kampf = (
        waffenpflege_anwendungen > 0
        and kampfwerte.get("talent_pflege_ganzer_kampf") is True
    )
    gegenschlag_runde = 0
    unbeugsam_genutzt = False
    bestienjaeger_gelernt = kampfwerte.get("bestienjaeger_gelernt") is True
    krieger_deckung_gelernt = kampfwerte.get("krieger_deckung_gelernt") is True
    spaeher_luecke_gelernt = kampfwerte.get("spaeher_luecke_gelernt") is True
    gelehrter_muster_gelernt = kampfwerte.get("gelehrter_muster_gelernt") is True
    magier_geist = kampfwerte.get("magier_geist", 0)
    magier_uebersinnliches = kampfwerte.get("magier_uebersinnliches", 0)
    magier_resonanz_gelernt = (
        kampfwerte.get("magier_resonanz_gelernt") is True
        and type(magier_geist) is int and magier_geist >= 2
        and type(magier_uebersinnliches) is int and magier_uebersinnliches >= 1
    )


    ausdauer_flucht_bonus = (
        ausdauer_stufen * 5
    )

    zaehigkeit_schadensreduktion = (
        zaehigkeit_stufen * 0.05
    )

    ruestung_schutz = kampfwerte.get(
        "ruestung_schutz",
        0
    )

    if (
        isinstance(
            ruestung_schutz,
            bool
        )
        or not isinstance(
            ruestung_schutz,
            (int, float)
        )
    ):
        ruestung_schutz = 0

    ruestung_schutz = max(
        0,
        int(
            ruestung_schutz
        )
    )

    spieler_sicht = umgebungs_sicht
    spieler_bewegung = bewegungsfreiheit
    if talent_nachtauge:
        spieler_sicht += 2

    if spieler["wahrnehmung"] >= 2:
        spieler_sicht += 1

    if spieler["wahrnehmung"] >= 3:
        spieler_sicht += 1

    if spieler["wahrnehmung"] >= 4:
        spieler_sicht += 1

    if spieler["geschick"] >= 2:
        spieler_bewegung += 1

    if spieler["geschick"] >= 3:
        spieler_bewegung += 1

    if spieler["geschick"] >= 4:
        spieler_bewegung += 1

    # =========================
    # GEGNERWERTE
    # =========================
    if gegner_typ == "Waldwächter":
        gegner = {
            "typ": "Waldwächter",
            "hp": 180,
            "max_hp": 180,
            "wahrnehmung": 2,
            "waldkenntnis": 2,
            "verstecken": 0,
            "angriffsart": "Nahkampf",
            "krit_chance": 0,
            "waffe": {
                "typ": "Fäuste",
                "wendigkeit": 1,
                "parade": 0,
                "reichweite": 1,
                "schaden_min": 10,
                "schaden_max": 18
            }
        }

    elif gegner_typ == "Bandit":
        gegner = bandit.copy()

    elif gegner_typ == "Wolf":
        gegner = wolf.copy()

    elif gegner_typ == "Keiler":
        gegner = keiler.copy()

    elif gegner_typ == "Glutsalamander":
        gegner = glutsalamander.copy()

    elif gegner_typ == "Kohlenschmuggler":
        gegner = kohlenschmuggler.copy()

    elif gegner_typ == "Schieferpanzer":
        gegner = schieferpanzer.copy()

    elif gegner_typ == "Kreischer":
        gegner = kreischer.copy()

    elif gegner_typ == "Gezeitenkrebs":
        gegner = gezeitenkrebs.copy()

    elif gegner_typ == "Graupelz":
        gegner = graupelz.copy()

    elif gegner_typ == "Aschenkönig":
        gegner = aschenkoenig.copy()

    elif gegner_typ == "Rudelloser Wolf":
        gegner = rudelloser_wolf.copy()

    elif gegner_typ == "Echohirsch":
        gegner = echohirsch.copy()

    elif gegner_typ == "Blasser Hirsch":
        gegner = blasser_hirsch.copy()

    elif gegner_typ == "Steinvater":
        gegner = steinvater.copy()

    elif gegner_typ == "Einscherer":
        gegner = einscherer.copy()

    elif gegner_typ == "Wrackplünderer":
        gegner = wrackpluenderer.copy()

    elif gegner_typ == "Schachtflatterer":
        gegner = schachtflatterer.copy()

    elif gegner_typ == "Schachtkriecher":
        gegner = schachtkriecher.copy()

    elif gegner_typ == "Blindmolch":
        gegner = blindmolch.copy()

    elif gegner_typ == "Schachtspinner":
        gegner = schachtspinner.copy()

    elif gegner_typ is None:
        gegner = random.choice(
            [
                bandit,
                wolf,
                keiler
            ]
        ).copy()

    else:
        raise ValueError(
            f"Unbekannter Gegnertyp: {gegner_typ}"
        )

    flucht_erlaubt = gegner["typ"] != "Waldwächter"

    gegner_sicht = umgebungs_sicht
    gegner_verstecken = gegner["verstecken"]

    if gegner["wahrnehmung"] >= 3:
        gegner_sicht += 1

    if gegner["wahrnehmung"] >= 5:
        gegner_sicht += 1

    gegner_verstecken += versteckmoeglichkeiten

    if situation["gebiet"] == "Wald":
        gegner_sicht += gegner["waldkenntnis"]
        gegner_verstecken += gegner["waldkenntnis"]

    # =========================
    # DECKUNG
    # =========================

    spieler_deckung_chance = 0
    gegner_deckung_chance = 0

    if deckung > 0:

        spieler_deckung_chance = 10 + deckung * 15
        gegner_deckung_chance = 10 + deckung * 15

        spieler_deckung_chance += 10 + (spieler["geschick"] - 2) * 2

        if situation["gebiet"] == "Wald":
            gegner_deckung_chance += gegner["waldkenntnis"] * 10

    spieler_deckung_chance = max(0, min(100, spieler_deckung_chance))

    gegner_deckung_chance = max(0, min(100, gegner_deckung_chance))

    spieler_deckung_wurf = random.randint(1, 100)
    gegner_deckung_wurf = random.randint(1, 100)

    spieler_hat_deckung = (spieler_deckung_wurf <= spieler_deckung_chance)

    gegner_hat_deckung = (gegner_deckung_wurf <= gegner_deckung_chance)

    if spieler_hat_deckung:
        effekte["ausweichchance_spieler"] += 10

    if gegner_hat_deckung:
        effekte["ausweichchance_gegner"] += 10

    # =========================
    # ENTDECKUNG
    # =========================

    entdeckungs_chance = 50

    entdeckungs_chance += spieler_sicht * 10
    entdeckungs_chance += (spieler["wahrnehmung"] - 2) * 2
    entdeckungs_chance -= gegner_verstecken * 5

    entdeckungs_chance = max(0, min(100, entdeckungs_chance))

    entdeckungs_wurf = random.randint(1, 100)

    gegner_entdeckt = (
        gegner["typ"] == "Waldwächter"
        or entdeckungs_wurf <= entdeckungs_chance
    )

    if not gegner_entdeckt:
        start_effekte["trefferchance_gegner"] += 15
        start_effekte["ausweichchance_spieler"] -= 10

    # =========================
    # BEWEGUNG
    # =========================

    effekte["fluchtchance"] += spieler_bewegung * 10

    effekte["ausweichchance_spieler"] += (spieler_bewegung * 5)

    # =========================
    # HINTERHALT
    # =========================

    if not gegner_entdeckt:

        hinterhalt_chance = 10

        hinterhalt_chance += (hinterhaltspotential * 15)

        hinterhalt_chance += (gegner["verstecken"] * 5)

        if situation["gebiet"] == "Wald":
            hinterhalt_chance += (gegner["waldkenntnis"] * 5)

        hinterhalt_chance -= 10 + (spieler["wahrnehmung"] - 2) * 2

        hinterhalt_chance = max(0, min(100, hinterhalt_chance))

        if talent_wachsam:
            hinterhalt_chance //= 2

        hinterhalt_wurf = random.randint(1, 100)

        hinterhalt = (hinterhalt_wurf <= hinterhalt_chance)

    else:
        hinterhalt_chance = 0
        hinterhalt_wurf = 0
        hinterhalt = False

    if hinterhalt:

        start_effekte["trefferchance_gegner"] += (10 + hinterhaltspotential * 5)

        start_effekte["krit_chance_gegner"] += (gegner["verstecken"] * 3)

        start_effekte["paradechance_spieler"] -= 20

        if spieler_sicht < 0:
            start_effekte["ausweichchance_spieler"] += (spieler_sicht * 2)

    # Wachsam: Überraschung und Hinterhalt wiegen in Runde 1 nur halb so schwer.
    if talent_wachsam:
        for schluessel in start_effekte:
            start_effekte[schluessel] = int(start_effekte[schluessel] / 2)

    # Dunkelheit in den TIEFEN; Nachtauge mildert den Abzug.
    if situation["umgebung"] == "Dunkle Tiefe":
        effekte["trefferchance_spieler"] -= (10 if talent_nachtauge else 15) - dunkel_milder
        effekte["ausweichchance_spieler"] -= (7 if talent_nachtauge else 10) - dunkel_milder

    # Schachtflatterer: schwer zu treffen, im Laternenlicht geblendet.
    if gegner["typ"] == "Schachtflatterer":
        if situation["umgebung"] == "Tiefe mit Licht":
            effekte["ausweichchance_gegner"] += 5
            effekte["trefferchance_gegner"] -= 10
        else:
            effekte["ausweichchance_gegner"] += 15

    basis_effekte = effekte.copy()

    while True:
        effekte = basis_effekte.copy()

        # =========================
        # WAFFE / WENDIGKEIT
        # =========================

        if spieler_bewegung < 0:

            if spieler["waffe"]["wendigkeit"] >= 2:
                effekte["trefferchance_spieler"] += 5

        # =========================
        # REICHWEITE
        # =========================

        spieler_reichweite = (spieler["waffe"]["reichweite"])

        gegner_reichweite = (gegner["waffe"]["reichweite"])

        spieler_effektive_reichweite = (spieler_reichweite)

        gegner_effektive_reichweite = (gegner_reichweite)

        if bewegungsfreiheit < 0:

            spieler_reichweiten_malus = max(0, spieler["waffe"]["reichweite"] - spieler["waffe"]["wendigkeit"])

            gegner_reichweiten_malus = max(0, gegner["waffe"]["reichweite"] - gegner["waffe"]["wendigkeit"])

            spieler_effektive_reichweite -= (spieler_reichweiten_malus)

            gegner_effektive_reichweite -= (gegner_reichweiten_malus)

        spieler_effektive_reichweite = max(0, spieler_effektive_reichweite)

        gegner_effektive_reichweite = max(0, gegner_effektive_reichweite)

        reichweiten_vorteil = (spieler_effektive_reichweite - gegner_effektive_reichweite)

        if reichweiten_vorteil > 0:

            effekte["trefferchance_spieler"] += (reichweiten_vorteil * 5)

        elif reichweiten_vorteil < 0:

            effekte["trefferchance_gegner"] += (abs(reichweiten_vorteil) * 5)

        # =========================
        # PARADE
        # =========================

        if gegner["angriffsart"] == "Nahkampf":

            parade_chance = 10

            parade_chance += (spieler["waffe"]["parade"] * 10)

            parade_chance += 10 + (spieler["geschick"] - 2) * 2

            if spieler_sicht < 0:
                parade_chance += (spieler_sicht * 5)

            if spieler_bewegung < 0:
                parade_chance += (spieler_bewegung * 5)

            parade_chance = max(0, min(100, parade_chance))

            effekte["paradechance_spieler"] = (parade_chance)

        # =========================
        # WAFFE + KAMPFUMGEBUNG
        # =========================

        schneller_stich_treffer_umgebung = 0
        schneller_stich_schaden_umgebung = 1.0

        schwerer_stich_treffer_umgebung = 0
        schwerer_stich_schaden_umgebung = 1.0
        print()
        print("=== Kampfvorbereitung ===")
        print(f"{situation['gebiet']} | {situation['umgebung']}")
        if situation["gebiet"] == "Tiefen":
            print("Unter der Erde")
        else:
            print(f"{situation['tageszeit']} | Wetter: {situation['wetter']}")
        print()
        print("=== Umgebung ===")

        if situation["umgebung"] == "Dunkle Tiefe":
            print("− Dunkelheit: Du triffst und weichst schlechter aus.")
            if talent_nachtauge:
                print("+ Nachtauge: Die Dunkelheit stört dich weniger.")
        if gegner["typ"] == "Schachtflatterer" and situation["umgebung"] == "Tiefe mit Licht":
            print("+ Das Laternenlicht blendet den Schachtflatterer.")

        if situation["wetter"] == "Regen":
            print("− Regen verschlechtert die Sicht und macht den Boden rutschig.")

        if umgebungs_sicht < 0:
            print("− Schlechte Sicht: Gegner sind schwerer zu entdecken.")
        elif umgebungs_sicht > 0:
            print("+ Gute Sicht: Gegner sind leichter zu entdecken.")
        else:
            print("Neutrale Sichtverhältnisse.")
        if spieler_sicht < 0:
            print(f"− Schlechte Sicht: {abs(spieler_sicht * 5)} Prozentpunkte weniger Paradechance.")
        if bewegungsfreiheit < 0:
            print("− Eingeschränkte Bewegung: Ausweichen und Flucht sind erschwert.")
        elif bewegungsfreiheit > 0:
            print("+ Gute Bewegungsbedingungen: Ausweichen und Flucht sind erleichtert.")

        if spieler_bewegung < 0:
            print(f"− Eingeschränkte Bewegung: {abs(spieler_bewegung * 5)} Prozentpunkte weniger Paradechance.")
        if deckung > 0:
            if spieler_hat_deckung:
                print("+ Du hast Deckung: +10 Prozentpunkte Ausweichen.")
            else:
                print("Deckung ist vorhanden, aber du stehst ungeschützt.")
        print()
        print(f"=== Deine Waffe: {spieler['waffe']['typ']} ===")

        if spieler_bewegung < 0 and spieler["waffe"]["wendigkeit"] >= 2:
            print("+ Wendige Waffe: +5 Prozentpunkte Trefferchance bei eingeschränkter Bewegung.")

        print(f"Reichweite im Gelände: {spieler_effektive_reichweite} von {spieler_reichweite}")
        print(f"Paradechance vor Aktions- und Hinterhalt-Effekten: {effekte['paradechance_spieler']} %")
        if ruestung_schutz > 0:
            print(
                f"Rüstungsschutz: "
                f"{ruestung_schutz} Schaden"
            )

        if (spieler["waffe"]["typ"] == "Speer" and situation["umgebung"] == "Dichter Wald"):

            schwerer_stich_treffer_umgebung -= 10
            schwerer_stich_schaden_umgebung *= 0.90

            print()
            print("Der dichte Wald erschwert weite Speerbewegungen.")
            print(f"− Schwerer Stich: {abs(schwerer_stich_treffer_umgebung)} Prozentpunkte weniger Trefferchance.")
            print(f"− Schwerer Stich: {round((1 - schwerer_stich_schaden_umgebung) * 100)} % weniger Schaden.")

        elif (spieler["waffe"]["typ"] == "Speer" and situation["umgebung"] == "Lichtung"):

            schneller_stich_treffer_umgebung += 5

            schwerer_stich_treffer_umgebung += 5
            schwerer_stich_schaden_umgebung *= 1.10

            print()
            print("Auf der Lichtung kannst du die Reichweite deines Speers besser ausnutzen.")
            print(f"+ Schneller Stich: {schneller_stich_treffer_umgebung} Prozentpunkte Trefferchance.")
            print(f"+ Schwerer Stich: {schwerer_stich_treffer_umgebung} Prozentpunkte Trefferchance.")
            print(f"+ Schwerer Stich: {round((schwerer_stich_schaden_umgebung - 1) * 100)} % Schaden.")

        print()
        if gegner_entdeckt:
            print(f"Du bemerkst den {gegner['typ']} rechtzeitig.")
            if reise_umgehen and waffe is not None:
                print()
                print("1. Kämpfen")
                print("2. Unbemerkt umgehen")
                umgangen = kampf_eingabe(("1", "2")) == "2"
                break
        elif not hinterhalt:
            print("Du bemerkst die Gefahr erst im letzten Moment.")
        if hinterhalt:
            print("Hinterhalt! Keine Zeit zum Waffenwechsel.")
            input("Drücke Enter, um den Kampf zu beginnen ...")
            break

        if waffe is not None:
            input("Drücke Enter, um den Kampf zu beginnen ...")
            break

        print()
        print("1. Kampf beginnen")
        print("2. Speer ausrüsten")
        print("3. Schwert ausrüsten")
        print("4. Hammer ausrüsten")

        vorbereitung_auswahl = kampf_eingabe(
            ("1", "2", "3", "4")
        )

        if vorbereitung_auswahl == "1":
            break
        elif vorbereitung_auswahl == "2":
            spieler["waffe"] = speer
            bildschirm_leeren()
        elif vorbereitung_auswahl == "3":
            spieler["waffe"] = schwert
            bildschirm_leeren()
        elif vorbereitung_auswahl == "4":
            spieler["waffe"] = hammer
            bildschirm_leeren()
        else:
            print("Bitte 1, 2, 3 oder 4 eingeben.")

    # Wachsam: Der Gegner wird umgangen, kein Kampf, keine Beute.
    if umgangen:
        print()
        print(f"Du hältst Abstand und gehst unbemerkt am {gegner['typ']} vorbei.")
        return {
            "lebenspunkte": spieler["hp"],
            "heiltraenke": spieler["heiltraenke"],
            "bandagen": spieler["bandagen"],
            "wurfnetze": spieler["wurfnetze"],
            "wundsalben": spieler["wundsalben"],
            "gegengifte": spieler["gegengifte"],
            "gewonnen": False,
            "geflohen": False,
            "gegner_geflohen": False,
            "gegner_verschont": False,
            "angekuendigt": [],
            "besiegt": False,
            "gegner_typ": gegner["typ"],
            "status_effekte": status_effekte,
            "umgangen": True
        }

    # =========================
    # KAMPF
    # =========================

    oeffnung_naechste_runde = False
    starkes_taumeln_naechste_runde = False

    wolf_sprungbereit = False
    wolf_sprung_verstaerkt = False

    keiler_ansturm_bereit = False
    salamander_eingegraben_naechste_runde = False
    schmuggler_aschewurf_bereit = False
    schmuggler_aschewuerfe = 0
    schmuggler_benommen_bis = 0
    schmuggler_flucht_angekuendigt = False
    schmuggler_flucht_bereit = False
    gegner_geflohen = False
    angekuendigt = set()
    panzer_risse = 0
    panzer_gebrochen = False
    kreischer_sturz_naechste_runde = False
    krebs_packen_bereit = False
    krebs_halt_runden = 0
    netz_bereit = False
    netz_wuerfe = 0
    netz_naechste_runde = False

    # Wurfnetz: einmal pro Kampf. Große Gegner reißen sich los.
    wurfnetz_benutzt = False
    gegner_im_wurfnetz = False
    netz_spieler_bonus = 0
    netz_bonus_runde = 0
    wurfnetz_gross = gegner["typ"] in (
        "Waldwächter", "Graupelz", "Aschenkönig", "Steinvater", "Einscherer",
        "Blasser Hirsch", "Blindmolch"
    )
    gnade_angekuendigt = False
    gnade_bereit = False
    gegner_verschont = False
    graupelz_sprung_naechste_runde = False
    graupelz_geheult = False
    rudellos_sprung_naechste_runde = False
    echo_erkannt = False
    echo_erkannt_naechste_runde = False
    echo_gezeigt = False
    rudel_runden = 0
    keiler_ansturm_verstaerkt = False
    keiler_erholt_sich_naechste_runde = False
    keiler_ausweichen_versucht = False
    keiler_ausweichen_erfolgreich = False
    keiler_speer_abfangen_versucht = False
    keiler_speer_abfangen_erfolgreich = False

    geflohen = False
    bandit_raserei = False
    bandit_schwerer_hieb_bereit_ab = 1
    molch_schnappen_bereit_ab = 2
    letzter_combo_angriff = None
    gegner_zurueckgedraengt_naechste_runde = False


    runde = 1

    fokus_bereit_ab = 1
    fokus_diese_runde = False

    bestienjaeger_studiert = False
    bestienjaeger_jagdhieb_bereit_ab = 1
    bestienjaeger_jagdhieb_diese_runde = False
    bestienjaeger_jagdhieb_getroffen = False
    bestienjaeger_abwehr_erfolgreich = False
    jagdinstinkt_bonus = 10 if bestienjaeger_gelernt and gegner["typ"] in (
        "Wolf", "Keiler", "Glutsalamander", "Schieferpanzer", "Kreischer", "Gezeitenkrebs", "Graupelz",
        "Aschenkönig", "Steinvater", "Einscherer", "Rudelloser Wolf", "Echohirsch", "Blasser Hirsch",
        "Schachtflatterer", "Schachtkriecher", "Blindmolch", "Schachtspinner"
    ) else 0

    glutkrieger_portion_verbraucht = False
    glutkrieger_portion_runde = 0
    glutkrieger_bonus_bis = 0
    glutkrieger_nachwaerme_bis = 0
    glutkrieger_kraftschub_diese_runde = False
    glutkrieger_kraftschub_getroffen = False

    stahlkrieger_amboss_bereit_ab = 1
    stahlkrieger_amboss_bis = 0
    stahlkrieger_amboss_diese_runde = False
    stahlkrieger_amboss_erfolgreich = False
    stahlkrieger_schmiedehieb_bereit_ab = 1
    stahlkrieger_schmiedehieb_diese_runde = False
    stahlkrieger_schmiedehieb_getroffen = False
    stahlkrieger_oeffnung_runde = 0

    spaeher_luecke_bereit_ab = 1
    spaeher_luecke_diese_runde = False

    magier_resonanz_ladungen = 3 if magier_resonanz_gelernt else 0

    gelehrter_muster_bereit_ab = 1
    gelehrter_muster_bis = 0
    gelehrter_muster_diese_runde = False

    def angriffs_eingabe(gueltige_tasten):
        if (fokus_diese_runde or spaeher_luecke_diese_runde
                or gelehrter_muster_diese_runde or bestienjaeger_jagdhieb_diese_runde
                or stahlkrieger_schmiedehieb_diese_runde or glutkrieger_kraftschub_diese_runde):
            return "1"
        return kampf_eingabe(gueltige_tasten)

    def erzwungene_faehigkeit():
        if fokus_diese_runde:
            return "Fokussierter Angriff"
        if spaeher_luecke_diese_runde:
            return "Lücke nutzen"
        if gelehrter_muster_diese_runde:
            return "Muster erkennen"
        if bestienjaeger_jagdhieb_diese_runde:
            return "Gezielter Jagdhieb"
        if stahlkrieger_schmiedehieb_diese_runde:
            return "Schmiedehieb"
        if glutkrieger_kraftschub_diese_runde:
            return "Kraftschub"
        return None

    krieger_deckung_bereit_ab = 1
    krieger_konter_runde = 0

    standhalten_bereit_ab = 1

    abstand_halten_bereit_ab = 1
    messer_oeffnung_naechste_runde = False
    stab_kontrolle_naechste_runde = False

    while (spieler["hp"] > 0 and gegner["hp"] > 0 and not geflohen):

        print()
        if runde > 1:
            text_pause("rundenwechsel")

        print(f"────────── Runde {runde} ──────────")
        print(
            f"Du: {spieler['hp']}/{spieler['max_hp']} HP | "
            f"{gegner['typ']}: {gegner['hp']}/{gegner['max_hp']} HP"
        )

        schaden_bonus_diese_runde = (
            kampf_status_rundenstart(
                spieler,
                status_effekte,
                status_definitionen
            )
        )

        if spieler["hp"] <= 0:
            print(
                "Du wurdest besiegt."
            )
            break

        if (glutkrieger_portion_verbraucht
                and glutkrieger_portion_runde < runde <= glutkrieger_nachwaerme_bis):
            vorher = spieler["hp"]
            spieler["hp"] = min(spieler["max_hp"], spieler["hp"] + 3)
            print(f"Nachwärme: +{spieler['hp'] - vorher} Leben.")
        glutkrieger_bonus_aktiv = glutkrieger_portion_verbraucht and glutkrieger_portion_runde < runde <= glutkrieger_bonus_bis
        glutkrieger_kraftschub_diese_runde = False

        aktion = None
        krieger_deckung_diese_runde = False
        stahlkrieger_amboss_diese_runde = False
        stahlkrieger_schmiedehieb_diese_runde = False
        bestienjaeger_jagdhieb_diese_runde = False
        spaeher_luecke_diese_runde = False
        gelehrter_muster_diese_runde = False
        gelehrter_muster_aktiv = runde <= gelehrter_muster_bis
        if gelehrter_muster_aktiv:
            rest = gelehrter_muster_bis - runde + 1
            print(f"Du erkennst das Angriffsmuster: Gegner -15 Treffer / -10 Krit ({rest} Runden).")
        krieger_deckung_bonus = 0
        krieger_konter_aktiv = krieger_konter_runde == runde
        if krieger_konter_aktiv:
            print("Deine Deckung eröffnet jetzt einen Gegenangriff: +30 % Waffenschaden.")
        gegenschlag_aktiv = (
            talent_gegenschlag
            and gegenschlag_runde == runde
            and not krieger_konter_aktiv
        )
        if gegenschlag_aktiv:
            print("Gegenschlag bereit: Dein Angriff in dieser Runde trifft härter.")
        unbeugsam_meldung = False
        zweiter_atem_meldung = False
        fokus_diese_runde = False
        parade_mod_diese_runde = 0
        ausweich_mod_diese_runde = 0
        bandit_konter_bonus = 0
        beil_druck_diese_runde = False
        krit_mod_diese_runde = 0
        messer_oeffnung_aktiv = False
        stab_kontrolle_aktiv = False

        bonus_durch_oeffnung = 0
        schadensbonus_durch_taumeln = 1.0
        starkes_taumeln_aktiv = False
        gegner_spezialangriff = False

        wolf_sprung_diese_runde = False
        wolf_sprung_abgefangen = False
        wolf_konter_versucht = False
        wolf_bereitet_sprung_vor = False
        wolf_schwert_konter = False
        wolf_schwert_konter_erfolgreich = False
        wolf_sprung_verstaerkt_diese_runde = False 

        gegner_zurueckgedraengt_aktiv = False
        combo_durchbruch = False
        combo_nachsetzen = False

        keiler_ansturm_diese_runde = False
        keiler_bereitet_ansturm_vor = False
        salamander_eingegraben = salamander_eingegraben_naechste_runde
        salamander_eingegraben_naechste_runde = False
        salamander_gluehen = False
        schmuggler_aschewurf_diese_runde = False
        schmuggler_flucht_diese_runde = False
        panzer_eingerollt = False
        kreischer_in_luft = False
        kreischer_sturz_diese_runde = kreischer_sturz_naechste_runde
        kreischer_sturz_naechste_runde = False
        krebs_packen_diese_runde = False
        netz_wurf_diese_runde = False
        im_netz = netz_naechste_runde
        gegner_im_wurfnetz = False
        if runde > netz_bonus_runde:
            netz_spieler_bonus = 0
        netz_naechste_runde = False
        gnade_diese_runde = gnade_bereit
        gnade_bereit = False
        graupelz_sprung_diese_runde = graupelz_sprung_naechste_runde
        graupelz_sprung_naechste_runde = False
        rudellos_sprung_diese_runde = rudellos_sprung_naechste_runde
        rudellos_sprung_naechste_runde = False
        if echo_erkannt_naechste_runde:
            echo_erkannt = True
            echo_erkannt_naechste_runde = False
        elif echo_erkannt and random.randint(1, 100) <= (35 if gegner["typ"] == "Blasser Hirsch" else 25):
            echo_erkannt = False
            print()
            print("Die Gestalten verschieben sich im Nebel. Du verlierst den echten aus den Augen.")
        keiler_erholt_sich_diese_runde = keiler_erholt_sich_naechste_runde
        keiler_erholt_sich_naechste_runde = False

        if keiler_erholt_sich_diese_runde:
            print("Der Keiler muss nach seinem Ansturm wieder Halt finden.")
            print("Er greift diese Runde nicht an. Nutze die Gelegenheit!")
        keiler_ansturm_verstaerkt_diese_runde = False
        keiler_ausweichen_versucht = False
        keiler_ausweichen_erfolgreich = False
        keiler_speer_abfangen_versucht = False
        keiler_speer_abfangen_erfolgreich = False


        if (
            messer_oeffnung_naechste_runde
            and spieler["waffe"]["typ"] == "Messer"
        ):
            messer_oeffnung_aktiv = True
            messer_oeffnung_naechste_runde = False

            print()
            print("=== PRÄZISIONSFENSTER ===")

            print(
                "Dein letzter Schnitt hat die Deckung "
                "des Gegners geöffnet."
            )

            print(
                "Ein gezielter Stich ist jetzt "
                "wesentlich gefährlicher."
            )

        if gegner_zurueckgedraengt_naechste_runde:
            gegner_zurueckgedraengt_aktiv = True
            gegner_zurueckgedraengt_naechste_runde = False
            bonus_durch_oeffnung += 10

            print(f"Der {gegner['typ']} wurde zurückgedrängt und muss sich neu positionieren.")

            if stab_kontrolle_naechste_runde:
                stab_kontrolle_naechste_runde = False

                if spieler["waffe"]["typ"] == "Stab":
                    stab_kontrolle_aktiv = True
                    bonus_durch_oeffnung += 10

                    print()
                    print(
                        "Du hältst den Gegner genau auf der "
                        "Reichweite deines Wanderstabs."
                    )

                    print(
                        "Dein Schneller Stoß kann diese Öffnung "
                        "besonders gut ausnutzen."
                    )

            if gegner["typ"] == "Wolf" and wolf_sprungbereit:
                wolf_sprungbereit = False
                print("Der Wolf verliert seinen Ansatz zum Sprung!")


        if starkes_taumeln_naechste_runde:
            bonus_durch_oeffnung = 20
            schadensbonus_durch_taumeln = 1.50
            starkes_taumeln_aktiv = True

            starkes_taumeln_naechste_runde = False

            print(f"Der {gegner['typ']} taumelt!")

            if spieler["waffe"]["typ"] == "Speer":
                print("Ein schneller Stich verursacht mehr Schaden!")

            elif spieler["waffe"]["typ"] == "Schwert":
                print("Seine offene Deckung bietet die Chance für einen präzisen Konter!")

        elif oeffnung_naechste_runde:
            bonus_durch_oeffnung = 15
            oeffnung_naechste_runde = False

            print("Der Gegner ist aus dem Gleichgewicht.")
            print("Diese Runde hast du eine günstige Angriffsposition.")

            gegner_spezialangriff = False


        # Blindmolch: lauscht und schnappt dann zu (schwerer Angriff).
        if (
            gegner["typ"] == "Blindmolch"
            and not starkes_taumeln_aktiv
            and not gegner_zurueckgedraengt_aktiv
            and runde >= molch_schnappen_bereit_ab
        ):
            gegner_spezialangriff = random.randint(1, 100) <= 30
            if gegner_spezialangriff:
                molch_schnappen_bereit_ab = runde + 3

        if gegner["typ"] == "Bandit" and runde < bandit_schwerer_hieb_bereit_ab:
            print("Der Bandit richtet seine Deckung neu aus.")
            print("Diese Runde kann er nur normal angreifen.")

        if (
            gegner["typ"] == "Bandit"
            and not starkes_taumeln_aktiv
            and not gegner_zurueckgedraengt_aktiv
            and runde >= bandit_schwerer_hieb_bereit_ab
        ):
            gegner_spezialangriff = random.randint(1, 100) <= 50
            if gegner_spezialangriff:
                bandit_schwerer_hieb_bereit_ab = runde + 2

        elif gegner["typ"] == "Wolf" and not starkes_taumeln_aktiv and not gegner_zurueckgedraengt_aktiv:
            if wolf_sprungbereit:
                wolf_sprung_diese_runde = True
                wolf_sprungbereit = False

                wolf_sprung_verstaerkt_diese_runde = wolf_sprung_verstaerkt
                wolf_sprung_verstaerkt = False

            elif random.randint(1, 100) <= 30:
                wolf_sprungbereit = True
                wolf_bereitet_sprung_vor = True
                print()
                print("Der Wolf beginnt dich zu umkreisen und duckt sich tief.")
                angekuendigt.add("wolf_sprung")

        elif (
            gegner["typ"] == "Keiler"
            and not starkes_taumeln_aktiv
            and not gegner_zurueckgedraengt_aktiv
            and not keiler_erholt_sich_diese_runde
        ):
            if keiler_ansturm_bereit:
                keiler_ansturm_diese_runde = True
                keiler_ansturm_bereit = False

                keiler_ansturm_verstaerkt_diese_runde = keiler_ansturm_verstaerkt
                keiler_ansturm_verstaerkt = False

            elif random.randint(1, 100) <= 30:
                keiler_ansturm_bereit = True
                keiler_bereitet_ansturm_vor = True
                print()
                print("Der Keiler scharrt mit den Hufen über den Boden.")
                angekuendigt.add("keiler_ansturm")
                print("Er senkt den Kopf und bereitet einen Ansturm vor.")

        if gegner["typ"] in ("Glutsalamander", "Aschenkönig"):
            if salamander_eingegraben:
                print()
                print(f"Der {gegner['typ']} ist unter der Asche verschwunden.")
                if spieler["wahrnehmung"] >= 3:
                    print("Links von dir hebt sich die Asche kaum merklich.")
                print("Ein Angriff würde nur Asche treffen.")
            elif gegner["typ"] == "Aschenkönig" and gegner["hp"] <= gegner["max_hp"] * 0.5:
                salamander_gluehen = True
                print()
                print("Die Haut des Aschenkönigs glüht jetzt ununterbrochen.")
                angekuendigt.add("salamander_gluehen")
                print("Wer ihm zu nahe kommt, verbrennt sich.")
            elif (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and random.randint(1, 100) <= 25):
                salamander_gluehen = True
                print()
                print(f"Die Haut des {gegner['typ']}s glüht rot auf.")
                angekuendigt.add("salamander_gluehen")
                print("Wer ihm jetzt zu nahe kommt, verbrennt sich.")

        if gegner["typ"] == "Kohlenschmuggler":
            if schmuggler_flucht_bereit:
                schmuggler_flucht_diese_runde = True
                print()
                print("Der Kohlenschmuggler sieht sich hastig nach einem Fluchtweg um.")
                print("Mit Verteidigen kannst du versuchen, ihm den Weg abzuschneiden.")
            elif schmuggler_aschewurf_bereit:
                schmuggler_aschewurf_bereit = False
                schmuggler_aschewurf_diese_runde = True
                print()
                print("Der Kohlenschmuggler schleudert dir eine Handvoll Asche entgegen!")
            elif (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and schmuggler_aschewuerfe < 2
                    and random.randint(1, 100) <= 25):
                schmuggler_aschewurf_bereit = True
                schmuggler_aschewuerfe += 1
                print()
                print("Der Kohlenschmuggler greift in den Aschebeutel an seinem Gürtel.")
                angekuendigt.add("schmuggler_asche")
            if runde <= schmuggler_benommen_bis:
                print("Asche brennt dir noch in den Augen. Du triffst schlechter.")

        if gegner["typ"] in ("Schieferpanzer", "Steinvater", "Schachtkriecher"):
            if (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and random.randint(1, 100) <= (35 if gegner["typ"] == "Steinvater" else 25)):
                panzer_eingerollt = True
                print()
                print(f"Der {gegner['typ']} rollt sich zusammen. Nur zwischen den Platten bleiben schmale Lücken.")
                print("Wuchtige Schläge prallen jetzt ab, schnelle Stiche finden die Lücken.")
                angekuendigt.add("panzer_einrollen")

        if gegner["typ"] == "Kreischer":
            if kreischer_sturz_diese_runde:
                print()
                print("Der Kreischer legt die Flügel an und stürzt auf dich herab!")
            elif (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and random.randint(1, 100) <= 25):
                kreischer_in_luft = True
                kreischer_sturz_naechste_runde = True
                print()
                print("Der Kreischer schwingt sich in die Luft und kreist über dir.")
                print("Nur eine lange Waffe reicht jetzt bis zu ihm hinauf.")
                angekuendigt.add("kreischer_aufstieg")
            elif random.randint(1, 100) <= 20:
                schmuggler_benommen_bis = runde + 1
                print()
                print("Ein schriller Schrei fährt dir durch Mark und Bein. Du bist benommen.")
                angekuendigt.add("kreischer_schrei")
            if runde <= schmuggler_benommen_bis and not kreischer_in_luft:
                print("Der Schrei hallt noch in deinen Ohren nach. Du triffst schlechter.")

        if gegner["typ"] in ("Gezeitenkrebs", "Einscherer"):
            if krebs_halt_runden > 0:
                print()
                print("Die Schere hält deinen Arm fest umklammert.")
                print("Mit Verteidigen kannst du versuchen, dich loszureißen.")
                if spieler["waffe"].get("typ") == "Messer":
                    print("Mit dem Messer kannst du durch die Schere stechen.")
            elif krebs_packen_bereit:
                krebs_packen_bereit = False
                krebs_packen_diese_runde = True
                print()
                print(f"Der {gegner['typ']} schnappt mit der offenen Schere nach dir!")
            elif (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and random.randint(1, 100) <= (35 if gegner["typ"] == "Einscherer" else 25)):
                krebs_packen_bereit = True
                print()
                print(f"Der {gegner['typ']} öffnet seine große Schere weit.")
                angekuendigt.add("krebs_packen")

        if gegner["typ"] == "Rudelloser Wolf":
            if rudellos_sprung_diese_runde:
                if spieler["sensibilitaet"] >= 2:
                    print()
                    print("Jetzt! Der Wolf stößt sich ab.")
            elif (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and random.randint(1, 100) <= 35):
                rudellos_sprung_naechste_runde = True
                if spieler["sensibilitaet"] >= 2:
                    print()
                    print("Der Wolf steht ruhig da. Trotzdem spürst du, dass er gleich springen wird.")
                    angekuendigt.add("rudellos_sprung")

        if gegner["typ"] in ("Echohirsch", "Blasser Hirsch"):
            anzahl_text = "Drei" if gegner["typ"] == "Blasser Hirsch" else "Zwei"
            print()
            if echo_erkannt:
                print("Du weißt jetzt, welche der Gestalten die echte ist.")
            else:
                print(f"{anzahl_text} gleiche Gestalten stehen im Nebel. Nur eine davon ist echt.")
                print("Mit Verteidigen kannst du abwarten und beobachten.")
            if not echo_gezeigt:
                echo_gezeigt = True
                angekuendigt.add("hirsch_echo")

        if gegner["typ"] == "Graupelz":
            if graupelz_sprung_diese_runde:
                print()
                print("Graupelz schnellt aus der Hocke auf dich zu!")
            elif (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and random.randint(1, 100) <= 30):
                graupelz_sprung_naechste_runde = True
                print()
                print("Graupelz duckt sich tief, die Lefzen weit hochgezogen.")
                angekuendigt.add("graupelz_sprung")
            if rudel_runden > 0:
                print("Zwei Wölfe umkreisen dich und warten auf eine Lücke.")
                print("Mit Verteidigen hältst du sie auf Abstand.")

        if gegner["typ"] == "Wrackplünderer":
            if gnade_diese_runde:
                print()
                print("[Wrackplünderer] Lass mich laufen! Ich geb dir, was ich habe!")
                print("Mit Verteidigen lässt du ihn gehen.")
            elif im_netz:
                print()
                if spieler["waffe"].get("typ") == "Messer":
                    im_netz = False
                    print("Du schneidest dich mit dem Messer aus dem Netz frei.")
                else:
                    print("Du hängst im Netz fest. Diese Runde kommst du nicht zum Zug.")
            elif netz_bereit:
                netz_bereit = False
                netz_wurf_diese_runde = True
                print()
                print("Der Wrackplünderer schleudert sein Fangnetz nach dir!")
            elif (not starkes_taumeln_aktiv
                    and not gegner_zurueckgedraengt_aktiv
                    and netz_wuerfe < 2
                    and random.randint(1, 100) <= 25):
                netz_bereit = True
                netz_wuerfe += 1
                print()
                print("Der Wrackplünderer wirbelt ein Fangnetz über dem Kopf.")
                angekuendigt.add("netz_wurf")

        waldwaechter_spezialangriff = False

        if (
            gegner["typ"] == "Waldwächter"
            and not starkes_taumeln_aktiv
            and not gegner_zurueckgedraengt_aktiv
        ):
            waldwaechter_spezialangriff = random.randint(1, 100) <= 20

        if waldwaechter_spezialangriff:
            print()
            print("Der Waldwächter bereitet einen mächtigen Angriff vor!")
            print("Der Waldwächter hebt seine gewaltigen Arme und sammelt seine Kraft...")

        if gegner_spezialangriff and gegner["typ"] == "Blindmolch":
            print()
            print("Der Blindmolch hält still und lauscht. Dann reißt er das Maul auf!")
            angekuendigt.add("molch_lauschen")

        elif gegner_spezialangriff:
            print()
            print("Der Bandit holt zu einem heftigen Angriff aus!")
            angekuendigt.add("bandit_hieb")

        elif wolf_sprung_diese_runde:
            print()
            print("Der Wolf stößt sich vom Boden ab und springt auf dich zu!")

        elif keiler_ansturm_diese_runde:
            print()
            print("Der Keiler stürmt mit voller Wucht auf dich zu!")



        # =========================
        # AKTIONSMENÜ
        # =========================

        spaeher_oeffnung_aktiv = (
            bonus_durch_oeffnung > 0
            or starkes_taumeln_aktiv
            or gegner_zurueckgedraengt_aktiv
            or messer_oeffnung_aktiv
            or keiler_erholt_sich_diese_runde
        )
        aktion_gewaehlt = False

        while not aktion_gewaehlt:

            print()
            print("1. Angreifen")
            if gegner_spezialangriff and gegner["typ"] == "Blindmolch":
                print("2. Den Biss abwehren")
            elif gegner_spezialangriff:
                print("2. Schweren Hieb blockieren")
            elif wolf_sprung_diese_runde:
                print("2. Sprung abwehren [Schaden möglich]")
            elif keiler_ansturm_diese_runde:
                if spieler["waffe"]["typ"] == "Speer":
                    print("2. Ansturm mit dem Speer abfangen [riskant]")
                else:
                    print("2. Dem Ansturm ausweichen [riskant]")
            elif waldwaechter_spezialangriff:
                print("2. Schweren Angriff abwehren [Schaden möglich]")
            else:
                print("2. Verteidigen")
            print("3. Gegenstand")


            gueltige_aktionen = (
                ("1", "2", "3", "4")
                if flucht_erlaubt
                else ("1", "2", "3")
            )

            if fokus_treffer_bonus:
                rest = max(0, fokus_bereit_ab - runde)
                hinweis = (
                    "bereit"
                    if rest == 0
                    else f"noch {rest} Runden"
                )
                print(f"F. Fokussierter Angriff [{hinweis}]")
                gueltige_aktionen += ("f",)

            if krieger_deckung_gelernt:
                rest = max(0, krieger_deckung_bereit_ab - runde)
                hinweis = "bereit" if rest == 0 else f"noch {rest} Runden"
                print(f"K. Deckung halten [{hinweis}]")
                print("   +10 Abwehr; bei gelungener Abwehr +30 % Waffenschaden nächste Runde.")
                gueltige_aktionen += ("k",)

            if spaeher_luecke_gelernt:
                rest = max(0, spaeher_luecke_bereit_ab - runde)
                if rest:
                    hinweis = f"noch {rest} Runden"
                else:
                    hinweis = "bereit" if spaeher_oeffnung_aktiv else "keine Öffnung"
                print(f"L. Lücke nutzen [{hinweis}]")
                print("   Angriff 1 mit +35 % Waffenschaden; benötigt eine Gegneröffnung.")
                gueltige_aktionen += ("l",)

            if gelehrter_muster_gelernt:
                rest = max(0, gelehrter_muster_bereit_ab - runde)
                hinweis = "bereit" if rest == 0 else f"noch {rest} Runden"
                print(f"M. Muster erkennen [{hinweis}]")
                print("   Angriff 1; nächste drei Runden Gegner -15 Treffer / -10 Krit.")
                gueltige_aktionen += ("m",)

            if magier_resonanz_gelernt:
                print(f"R. Resonanzstoß [{magier_resonanz_ladungen}/3 Ladungen]")
                print("   Magischer Angriff; eine Runde und eine Ladung, auch bei Verfehlen.")
                gueltige_aktionen += ("r",)

            if bestienjaeger_gelernt:
                print("V. Beute studieren [bereits studiert]" if bestienjaeger_studiert else "V. Beute studieren [eine Vorbereitungsrunde]")
                rest = max(0, bestienjaeger_jagdhieb_bereit_ab - runde)
                hinweis = "erst studieren" if not bestienjaeger_studiert else f"noch {rest} Runden" if rest else "bereit"
                print(f"J. Gezielter Jagdhieb [{hinweis}]")
                gueltige_aktionen += ("v", "j")
            if stahlkrieger_gelernt:
                rest = max(0, stahlkrieger_amboss_bereit_ab - runde)
                hinweis = f"noch {rest} Runden" if rest else "bereit"
                print(f"A. Ambossstand [{hinweis}]")
                rest = max(0, stahlkrieger_schmiedehieb_bereit_ab - runde)
                hinweis = f"noch {rest} Runden" if rest else "bereit" if stahlkrieger_oeffnung_runde == runde else "erst erfolgreich verteidigen"
                print(f"S. Schmiedehieb [{hinweis}]")
                gueltige_aktionen += ("a", "s")
            if glutkrieger_gelernt:
                hinweis = "verbraucht" if glutkrieger_portion_verbraucht else "bereit" if glutkrieger_portion_bereit else "keine Portion"
                print(f"G. Kampfportion [{hinweis}]")
                hinweis = "bereit" if glutkrieger_bonus_aktiv else "keine Stärkung"
                print(f"B. Kraftschub [{hinweis}]")
                gueltige_aktionen += ("g", "b")
            if flucht_erlaubt:
                anzeige_fluchtchance = max(
                    10,
                    min(90, 40 + effekte["fluchtchance"] + ausdauer_flucht_bonus + talent_flucht_bonus)
                )
                print(f"4. Fliehen ({anzeige_fluchtchance} %)")

            kampf_auswahl = kampf_eingabe(
                gueltige_aktionen
            )

            if kampf_auswahl == "g":
                if not glutkrieger_portion_bereit or glutkrieger_portion_verbraucht:
                    print("Eine Kampfportion ist jetzt nicht verfügbar.")
                    continue
                glutkrieger_portion_verbraucht = True
                glutkrieger_portion_runde = runde
                glutkrieger_bonus_bis = runde + 3
                glutkrieger_nachwaerme_bis = runde + 3
                vorher = spieler["hp"]
                spieler["hp"] = min(spieler["max_hp"], spieler["hp"] + 20)
                print(f"Du isst deine Kampfportion: +{spieler['hp'] - vorher} Leben. Stärkung und Nachwärme für die drei Folgerunden.")
                aktion = "gegenstand"
                aktion_gewaehlt = True
                continue
            if kampf_auswahl == "b":
                if not glutkrieger_gelernt or not glutkrieger_bonus_aktiv:
                    print("Kraftschub benötigt die aktive Stärkung deiner Kampfportion.")
                    continue
                glutkrieger_kraftschub_diese_runde = True
                glutkrieger_bonus_bis = 0
                kampf_auswahl = "1"

            if kampf_auswahl == "a":
                if not stahlkrieger_gelernt or runde < stahlkrieger_amboss_bereit_ab:
                    print("Ambossstand ist noch nicht verfügbar.")
                    continue
                stahlkrieger_amboss_diese_runde = True
                stahlkrieger_amboss_bis = runde + 1
                stahlkrieger_amboss_bereit_ab = runde + 4
                kampf_auswahl = "2"
                print("Du gehst in den Ambossstand: bis zu 3 zusätzliche Schadensminderung für zwei Runden.")
            if kampf_auswahl == "s":
                if not stahlkrieger_gelernt or stahlkrieger_oeffnung_runde != runde:
                    print("Für Schmiedehieb musst du in der vorherigen Runde erfolgreich verteidigt haben.")
                    continue
                if runde < stahlkrieger_schmiedehieb_bereit_ab:
                    print("Schmiedehieb ist noch nicht bereit.")
                    continue
                stahlkrieger_schmiedehieb_diese_runde = True
                stahlkrieger_schmiedehieb_bereit_ab = runde + 4
                kampf_auswahl = "1"

            if kampf_auswahl == "v":
                if not bestienjaeger_gelernt or bestienjaeger_studiert:
                    print("Beute studieren ist jetzt nicht verfügbar.")
                    continue
                bestienjaeger_studiert = True
                aktion = "studieren"
                aktion_gewaehlt = True
                print("Du studierst die Beute. Dein Waffenschaden gegen diesen Gegner steigt um 20 %.")
                continue
            if kampf_auswahl == "j":
                if not bestienjaeger_gelernt or not bestienjaeger_studiert:
                    print("Für Jagdhieb musst du zuerst die Beute studieren.")
                    continue
                if runde < bestienjaeger_jagdhieb_bereit_ab:
                    print("Jagdhieb ist noch nicht bereit.")
                    continue
                bestienjaeger_jagdhieb_diese_runde = True
                bestienjaeger_jagdhieb_bereit_ab = runde + 3
                kampf_auswahl = "1"

            if kampf_auswahl == "r":
                if not magier_resonanz_gelernt:
                    print("Du hast diese Magierfähigkeit nicht gelernt.")
                    continue
                if magier_resonanz_ladungen <= 0:
                    print("Du hast in diesem Kampf keine Zauberladungen mehr.")
                    continue
                magier_resonanz_ladungen -= 1
                aktion = "zauber"
                aktion_gewaehlt = True
                continue

            if kampf_auswahl == "m":
                if not gelehrter_muster_gelernt:
                    print("Du hast diese Gelehrtenfähigkeit nicht gelernt.")
                    continue
                if runde < gelehrter_muster_bereit_ab:
                    print("Muster erkennen ist noch nicht bereit.")
                    continue
                gelehrter_muster_diese_runde = True
                gelehrter_muster_bis = runde + 3
                gelehrter_muster_bereit_ab = runde + 5
                print("Du greifst an und analysierst den Gegner für die nächsten drei Runden.")
                kampf_auswahl = "1"

            if kampf_auswahl == "l":
                if not spaeher_luecke_gelernt:
                    print("Du hast diese Späherfähigkeit nicht gelernt.")
                    continue
                if runde < spaeher_luecke_bereit_ab:
                    print("Lücke nutzen ist noch nicht bereit.")
                    continue
                if not spaeher_oeffnung_aktiv:
                    print("Der Gegner bietet gerade keine Öffnung.")
                    continue
                spaeher_luecke_diese_runde = True
                spaeher_luecke_bereit_ab = runde + 3
                kampf_auswahl = "1"

            if kampf_auswahl == "k":
                if not krieger_deckung_gelernt:
                    print("Du hast diese Kriegerfähigkeit nicht gelernt.")
                    continue
                if runde < krieger_deckung_bereit_ab:
                    print("Deckung halten ist noch nicht bereit.")
                    continue
                krieger_deckung_diese_runde = True
                krieger_deckung_bonus = 10
                krieger_deckung_bereit_ab = runde + 3
                kampf_auswahl = "2"

            if kampf_auswahl == "f":
                if not fokus_treffer_bonus:
                    print("Du hast diese Fähigkeit noch nicht gelernt.")
                    continue

                if runde < fokus_bereit_ab:
                    print("Fokussierter Angriff ist noch nicht bereit.")
                    continue

                fokus_diese_runde = True
                kampf_auswahl = "1"

            if kampf_auswahl == "1":

                # =========================
                # SPEER-ANGRIFFE
                # =========================

                if spieler["waffe"]["typ"] == "Speer":

                    while True:
                        faehigkeit = erzwungene_faehigkeit()
                        if faehigkeit:
                            print(f"{faehigkeit}: Schneller Stich")
                            print()
                        else:
                            print()
                            print("=== Speer ===")
                            print()
                            print("1. Schneller Stich [genauer, weniger Wucht]")
                            print("2. Schwerer Stich [Kraftangriff, offene Deckung]")
                            print("3. Zurück")

                        angriffs_auswahl = angriffs_eingabe(
                        ("1", "2", "3")
                        )

                        if angriffs_auswahl == "1":

                            angriffs_name = "Schneller Stich"

                            angriffs_treffer_mod = (10 + schneller_stich_treffer_umgebung)

                            angriffs_schaden_faktor = (0.85 * schneller_stich_schaden_umgebung)
                            parade_mod_diese_runde = 0
                            aktion = "angriff"

                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "2":

                            angriffs_name = "Schwerer Stich"

                            angriffs_treffer_mod = (-15 + schwerer_stich_treffer_umgebung)

                            angriffs_schaden_faktor = (1.35 * schwerer_stich_schaden_umgebung)
                            parade_mod_diese_runde = -10
                            aktion = "angriff"

                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "3":
                            break

                        else:
                            print("Ungültige Eingabe.")

                elif spieler["waffe"]["typ"] == "Schwert":

                    while True:
                        faehigkeit = erzwungene_faehigkeit()
                        if faehigkeit:
                            print(f"{faehigkeit}: Schneller Hieb")
                            print()
                        else:
                            print()
                            print("=== Schwert ===")
                            print()
                            print("1. Schneller Hieb [genauer, weniger Wucht]")
                            print("2. Kräftiger Hieb [mehr Wucht, offene Deckung]")
                            print("3. Zurück")

                        angriffs_auswahl = angriffs_eingabe(
                            ("1", "2", "3")
                        )

                        if angriffs_auswahl == "1":
                            angriffs_name = "Schneller Hieb"
                            angriffs_treffer_mod = 5
                            angriffs_schaden_faktor = 0.95
                            parade_mod_diese_runde = 0
                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "2":
                            angriffs_name = "Kräftiger Hieb"
                            angriffs_treffer_mod = -10
                            angriffs_schaden_faktor = 1.25
                            parade_mod_diese_runde = -5
                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "3":
                            break

                        else:
                            print("Ungültige Eingabe.")

                elif spieler["waffe"]["typ"] == "Hammer":
                    while True:
                        faehigkeit = erzwungene_faehigkeit()
                        if faehigkeit:
                            print(f"{faehigkeit}: Kurzer Schlag")
                            print()
                        else:
                            print()
                            print("=== Hammer ===")
                            print()
                            print("1. Kurzer Schlag [genauer, weniger Wucht]")
                            print("2. Wuchtiger Hieb [mehr Wucht, offene Deckung]")

                            rest = max(0, standhalten_bereit_ab - runde)

                            if rest == 0:
                                print("3. Standhalten [bereit]")
                                print("   Riskanter Gegenschlag: Bei Erfolg halber Trefferschaden.")
                                print("   Du musst den Treffer überleben, um zurückzuschlagen.")
                            else:
                                print(f"3. Standhalten [noch {rest} Runden]")

                            print("4. Zurück")
                        angriffs_auswahl = angriffs_eingabe(
                            ("1", "2", "3", "4")
                        )

                        if angriffs_auswahl == "1":
                            angriffs_name = "Kurzer Schlag"
                            angriffs_treffer_mod = 10
                            angriffs_schaden_faktor = 0.80
                            parade_mod_diese_runde = 0
                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "2":
                            angriffs_name = "Wuchtiger Hieb"
                            angriffs_treffer_mod = -15
                            angriffs_schaden_faktor = 1.30
                            parade_mod_diese_runde = -10
                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "3":
                            if rest > 0:
                                print("Standhalten ist noch nicht bereit.")
                                continue

                            aktion = "standhalten"
                            standhalten_bereit_ab = runde + 3
                            aktion_gewaehlt = True
                            print("Du festigst deinen Stand und wartest auf den Angriff.")
                            break

                        elif angriffs_auswahl == "4":
                            break

                        else:
                            print("Ungültige Eingabe.")

                elif spieler["waffe"]["typ"] == "Beil":

                    while True:
                        faehigkeit = erzwungene_faehigkeit()
                        if faehigkeit:
                            print(f"{faehigkeit}: Kurzer Hieb")
                            print()
                        else:
                            print()
                            print("=== Handbeil ===")
                            print()
                            print("1. Kurzer Hieb [genauer, weniger Wucht]")
                            print("2. Spaltender Hieb [mehr Wucht, offene Deckung]")
                            print("3. Zurück")

                        angriffs_auswahl = angriffs_eingabe(
                            ("1", "2", "3")
                        )

                        if angriffs_auswahl == "1":
                            angriffs_name = "Kurzer Hieb"
                            angriffs_treffer_mod = 5
                            angriffs_schaden_faktor = 1.00
                            parade_mod_diese_runde = 0

                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "2":
                            angriffs_name = "Spaltender Hieb"
                            angriffs_treffer_mod = -15
                            angriffs_schaden_faktor = 1.40
                            parade_mod_diese_runde = -10

                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "3":
                            break

                        else:
                            print("Ungültige Eingabe.")

                elif spieler["waffe"]["typ"] == "Stab":

                    while True:
                        faehigkeit = erzwungene_faehigkeit()
                        if faehigkeit:
                            print(f"{faehigkeit}: Schneller Stoß")
                            print()
                        else:
                            print()
                            print("=== Wanderstab ===")
                            print()

                            if stab_kontrolle_aktiv:
                                print(
                                    "1. Schneller Stoß "
                                    "[Distanzvorteil: genauer und kräftiger]"
                                )
                            else:
                                print("1. Schneller Stoß [genauer, bessere Abwehr]")

                            print("2. Weiter Schwung [ungenauer, weniger Abwehr]")

                            rest = max(
                                0,
                                abstand_halten_bereit_ab - runde
                            )

                            if rest == 0:
                                print("3. Abstand halten [bereit]")
                                print("   Verbessert die Abwehr und den nächsten schnellen Stoß.")
                                print("   Stoppt laufende Spezialangriffe nicht automatisch.")
                            else:
                                einheit = (
                                    "Runde"
                                    if rest == 1
                                    else "Runden"
                                )

                                print(
                                    f"3. Abstand halten "
                                    f"[noch {rest} {einheit}]"
                                )

                            print("4. Zurück")

                        angriffs_auswahl = angriffs_eingabe(
                            ("1", "2", "3", "4")
                        )

                        if angriffs_auswahl == "1":
                            angriffs_name = "Schneller Stoß"
                            angriffs_treffer_mod = 10
                            angriffs_schaden_faktor = 0.95
                            parade_mod_diese_runde = 5

                            if stab_kontrolle_aktiv:
                                angriffs_treffer_mod += 10
                                angriffs_schaden_faktor = 1.25

                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "2":
                            angriffs_name = "Weiter Schwung"
                            angriffs_treffer_mod = -5
                            angriffs_schaden_faktor = 1.05
                            parade_mod_diese_runde = 0

                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "3":

                            if rest > 0:
                                print(
                                    "Abstand halten ist "
                                    "noch nicht bereit."
                                )
                                continue

                            aktion = "abstand_halten"

                            parade_mod_diese_runde = 30
                            ausweich_mod_diese_runde = 20

                            gegner_zurueckgedraengt_naechste_runde = True
                            stab_kontrolle_naechste_runde = True

                            abstand_halten_bereit_ab = runde + 2

                            aktion_gewaehlt = True

                            print(
                                "Du hältst den Stab quer vor dich "
                                "und zwingst den Gegner auf Abstand."
                            )

                            break

                        elif angriffs_auswahl == "4":
                            break

                        else:
                            print("Ungültige Eingabe.")

                elif spieler["waffe"]["typ"] == "Messer":

                    while True:
                        faehigkeit = erzwungene_faehigkeit()
                        if faehigkeit:
                            print(f"{faehigkeit}: Schneller Schnitt")
                            print()
                        else:
                            print()
                            print("=== Jagdmesser ===")
                            print()
                            print("1. Schneller Schnitt [genauer, weniger Wucht]")
                            print("2. Gezielter Stich [mehr Krit-Chance, offene Deckung]")
                            print("3. Zurück")

                        angriffs_auswahl = angriffs_eingabe(
                            ("1", "2", "3")
                        )

                        if angriffs_auswahl == "1":
                            angriffs_name = "Schneller Schnitt"
                            angriffs_treffer_mod = 15
                            angriffs_schaden_faktor = 0.85
                            parade_mod_diese_runde = 0
                            krit_mod_diese_runde = 5

                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "2":
                            angriffs_name = "Gezielter Stich"
                            angriffs_treffer_mod = -5
                            angriffs_schaden_faktor = 1.10
                            parade_mod_diese_runde = -5
                            krit_mod_diese_runde = 20

                            if messer_oeffnung_aktiv:
                                angriffs_treffer_mod += 15
                                krit_mod_diese_runde += 20

                            aktion = "angriff"
                            aktion_gewaehlt = True
                            break

                        elif angriffs_auswahl == "3":
                            break

                        else:
                            print("Ungültige Eingabe.")

                else:



                    angriffs_name = "Angriff"

                    angriffs_treffer_mod = 0
                    angriffs_schaden_faktor = 1.0
                    parade_mod_diese_runde = 0
                    aktion = "angriff"

                    aktion_gewaehlt = True




            elif kampf_auswahl == "2":
                aktion = "verteidigen"

                parade_mod_diese_runde = (
                    25
                    + ausdauer_verteidigung_bonus
                    + talent_verteidigung_bonus
                    + krieger_deckung_bonus
                    + jagdinstinkt_bonus
                )

                ausweich_mod_diese_runde = (
                    10
                    + ausdauer_verteidigung_bonus
                    + talent_verteidigung_bonus
                    + krieger_deckung_bonus
                    + jagdinstinkt_bonus
                )

                if gegner_spezialangriff:
                    starkes_taumeln_naechste_runde = True

                elif wolf_sprung_diese_runde:
                    print(f"Du gehst mit deinem {spieler['waffe']['typ']} in eine feste Abwehrhaltung.")

                elif wolf_bereitet_sprung_vor:
                    print("Du hältst deine Stellung und beobachtest den Wolf.")

                elif keiler_ansturm_diese_runde:

                    if spieler["waffe"]["typ"] == "Speer":
                        parade_mod_diese_runde = 0
                        ausweich_mod_diese_runde = 0
                        keiler_speer_abfangen_versucht = True

                        keiler_speer_chance = 25
                        keiler_speer_chance += ausdauer_verteidigung_bonus
                        keiler_speer_chance += talent_verteidigung_bonus
                        keiler_speer_chance += krieger_deckung_bonus
                        keiler_speer_chance += jagdinstinkt_bonus
                        keiler_speer_chance += spieler["staerke"] * 5

                        keiler_speer_chance += (spieler["wahrnehmung"] - 2) * 2

                        if situation["umgebung"] == "Lichtung":
                            keiler_speer_chance += 5

                        elif situation["umgebung"] == "Dichter Wald":
                            keiler_speer_chance -= 10

                        keiler_speer_chance = max(10, min(85, keiler_speer_chance))

                        if random.randint(1, 100) <= keiler_speer_chance:
                            keiler_speer_abfangen_erfolgreich = True
                            print("Du stemmst den Speer gegen den Boden und erwartest den Ansturm.")
                        else:
                            print("Du bekommst den Speer nicht rechtzeitig in eine stabile Position!")

                    else:
                        parade_mod_diese_runde = 0
                        ausweich_mod_diese_runde = 0
                        keiler_ausweichen_versucht = True

                        keiler_ausweich_chance = 35
                        keiler_ausweich_chance += ausdauer_verteidigung_bonus
                        keiler_ausweich_chance += talent_verteidigung_bonus
                        keiler_ausweich_chance += krieger_deckung_bonus
                        keiler_ausweich_chance += jagdinstinkt_bonus
                        keiler_ausweich_chance += spieler_bewegung * 10

                        keiler_ausweich_chance += (spieler["wahrnehmung"] - 2) * 2

                        keiler_ausweich_chance = max(10, min(85, keiler_ausweich_chance))

                        if random.randint(1, 100) <= keiler_ausweich_chance:
                            keiler_ausweichen_erfolgreich = True
                            oeffnung_naechste_runde = True
                            print("Du bereitest dich darauf vor, im richtigen Moment zur Seite zu springen.")
                        else:
                            print("Du versuchst dem Ansturm auszuweichen, kommst aber nicht rechtzeitig weg.")

                elif keiler_bereitet_ansturm_vor:
                    print("Du gehst auf Abstand und beobachtest den Keiler.")

                else:
                    oeffnung_naechste_runde = True
                    print(f"Du zwingst den {gegner['typ']} in eine ungünstige Position.")



                aktion_gewaehlt = True

            elif kampf_auswahl == "3":
                print()
                print("=== Gegenstände ===")
                if talent_griffbereit and not griffbereit_genutzt:
                    print("Griffbereit: Der erste Gegenstand in diesem Kampf kostet keine Runde.")
                else:
                    print("Die Anwendung kostet eine Runde; der Gegner kann angreifen.")
                print()
                print(f"1. Heiltrank ({spieler['heiltraenke']}) [30 HP, stoppt Blutung]")
                bandage_info = "+8 HP bei Blutung" if talent_heilkundig else "keine Heilung"
                print(f"2. Bandage ({spieler['bandagen']}) [stoppt Blutung, {bandage_info}]")
                gegenstand_tasten = ["1", "2"]
                zusatz_gegenstaende = {}
                if spieler["wundsalben"] > 0:
                    taste = str(len(gegenstand_tasten) + 1)
                    print(f"{taste}. Wundsalbe ({spieler['wundsalben']}) [{wundsalbe_heilung} HP, stoppt Blutung]")
                    gegenstand_tasten.append(taste)
                    zusatz_gegenstaende[taste] = "wundsalbe"
                if spieler["gegengifte"] > 0:
                    taste = str(len(gegenstand_tasten) + 1)
                    print(f"{taste}. Gegengift ({spieler['gegengifte']}) [entfernt Vergiftung]")
                    gegenstand_tasten.append(taste)
                    zusatz_gegenstaende[taste] = "gegengift"
                if spieler["wurfnetze"] > 0 and not wurfnetz_benutzt:
                    taste = str(len(gegenstand_tasten) + 1)
                    print(f"{taste}. Wurfnetz ({spieler['wurfnetze']}) [einmal pro Kampf]")
                    gegenstand_tasten.append(taste)
                    zusatz_gegenstaende[taste] = "wurfnetz"
                zurueck_taste = str(len(gegenstand_tasten) + 1)
                print(f"{zurueck_taste}. Zurück")
                gegenstand_tasten.append(zurueck_taste)

                gegenstand_auswahl = kampf_eingabe(
                    tuple(gegenstand_tasten)
                )
                gegenstand_art = zusatz_gegenstaende.get(gegenstand_auswahl)

                if gegenstand_auswahl == "1":

                    blutung_aktiv = (
                        "bluten" in status_effekte
                    )

                    if spieler["heiltraenke"] <= 0:
                        print(
                            "Du hast keine Heiltränke mehr."
                        )

                    elif (
                        spieler["hp"]
                        >= spieler["max_hp"]
                        and not blutung_aktiv
                    ):
                        print(
                            "Deine Lebenspunkte sind bereits voll."
                        )

                    else:
                        heilung = 30 + talent_heiltrank_bonus

                        spieler["hp"] += heilung
                        spieler["hp"] = min(
                            spieler["hp"],
                            spieler["max_hp"]
                        )

                        spieler["heiltraenke"] -= 1

                        if blutung_aktiv:
                            status_effekte.pop(
                                "bluten",
                                None
                            )

                        aktion = "gegenstand"
                        aktion_gewaehlt = True

                        farbig_ausgeben(
                            f"Du trinkst einen Heiltrank und hast jetzt "
                            f"{spieler['hp']} HP.",
                            "gruen"
                        )

                        if blutung_aktiv:
                            farbig_ausgeben(
                                "Die Blutung kommt zum Stillstand.",
                                "gruen"
                            )

                elif gegenstand_auswahl == "2":
                    if spieler["bandagen"] <= 0:
                        print("Du hast keine Bandagen mehr.")
                    elif "bluten" not in status_effekte:
                        print("Du blutest nicht. Die Bandage bleibt unbenutzt.")
                    else:
                        spieler["bandagen"] -= 1
                        status_effekte.pop("bluten", None)
                        aktion = "gegenstand"
                        aktion_gewaehlt = True
                        print("Du legst eine Bandage an. Die Blutung stoppt.")
                        if talent_heilkundig:
                            spieler["hp"] = min(spieler["max_hp"], spieler["hp"] + 8)
                            print(f"Du versorgst die Wunde sorgfältig und hast jetzt {spieler['hp']} HP.")

                elif gegenstand_art == "wundsalbe":
                    if "bluten" not in status_effekte and spieler["hp"] >= spieler["max_hp"]:
                        print("Du bist unverletzt. Die Wundsalbe bleibt unbenutzt.")
                    else:
                        spieler["wundsalben"] -= 1
                        spieler["hp"] = min(spieler["max_hp"], spieler["hp"] + wundsalbe_heilung)
                        blutung_gestoppt = status_effekte.pop("bluten", None) is not None
                        aktion = "gegenstand"
                        aktion_gewaehlt = True
                        farbig_ausgeben(
                            f"Du streichst Wundsalbe auf und hast jetzt {spieler['hp']} HP.",
                            "gruen"
                        )
                        if blutung_gestoppt:
                            farbig_ausgeben("Die Blutung kommt zum Stillstand.", "gruen")
                elif gegenstand_art == "gegengift":
                    if "gift" not in status_effekte:
                        print("Du bist nicht vergiftet. Das Gegengift bleibt unbenutzt.")
                    else:
                        spieler["gegengifte"] -= 1
                        status_effekte.pop("gift", None)
                        aktion = "gegenstand"
                        aktion_gewaehlt = True
                        farbig_ausgeben("Du trinkst das Gegengift. Das Brennen lässt nach.", "gruen")
                elif gegenstand_art == "wurfnetz":
                    spieler["wurfnetze"] -= 1
                    wurfnetz_benutzt = True
                    gegner_im_wurfnetz = True
                    aktion = "gegenstand"
                    aktion_gewaehlt = True
                    if wurfnetz_gross:
                        netz_spieler_bonus = 10
                        netz_bonus_runde = runde + 1
                        print(f"Das Netz legt sich über den {gegner['typ']}. Er reißt daran, und die Maschen geben nach.")
                        print("Für einen Augenblick ist er behindert.")
                    else:
                        oeffnung_naechste_runde = True
                        print(f"Das Netz legt sich über den {gegner['typ']}. Er verfängt sich darin.")
                elif gegenstand_auswahl == zurueck_taste:
                    pass

                else:
                    print("Ungültige Eingabe.")

                if (
                    aktion == "gegenstand"
                    and talent_griffbereit
                    and not griffbereit_genutzt
                ):
                    griffbereit_genutzt = True
                    aktion = None
                    aktion_gewaehlt = False
                    print("Griffbereit: Du hast es schnell zur Hand und kannst noch handeln.")

            elif kampf_auswahl == "4":
                if not flucht_erlaubt:
                    print("Aus diesem Bosskampf kannst du nicht fliehen.")
                    continue

                aktion = "fliehen"

                flucht_chance = 40
                flucht_chance += effekte[
                    "fluchtchance"
                ]
                flucht_chance += (
                    ausdauer_flucht_bonus
                )
                flucht_chance += talent_flucht_bonus

                flucht_chance = max(10, min(90, flucht_chance))

                flucht_wurf = random.randint(1, 100)

                if flucht_wurf <= flucht_chance:
                    geflohen = True
                    print(f"Du entkommst dem {gegner['typ']}!")

                else:
                    print("Deine Flucht misslingt!")

                aktion_gewaehlt = True

            else:
                print("Ungültige Eingabe.")

        if fokus_diese_runde and aktion == "angriff":
            fokus_bereit_ab = runde + 3
            print("Du führst deinen Angriff besonders kontrolliert aus.")

        if geflohen:
            break
        if aktion != "angriff":
            letzter_combo_angriff = None




        # =========================
        # SPIELER-ANGRIFF
        # =========================

        if salamander_eingegraben and aktion in ("angriff", "zauber"):
            print("Dein Angriff trifft nur Asche.")
            aktion = "ins_leere"

        if im_netz and aktion in ("angriff", "zauber", "verteidigen", "standhalten"):
            print("Du zerrst am Netz und kommst nicht frei.")
            aktion = "ins_leere"

        if (kreischer_in_luft and aktion == "angriff"
                and spieler["waffe"].get("reichweite", 1) <= 1):
            print("Deine Waffe reicht nicht bis zu ihm hinauf.")
            aktion = "ins_leere"

        if gegner["typ"] in ("Echohirsch", "Blasser Hirsch") and aktion == "angriff" and not echo_erkannt:
            echo_chance = 66 if gegner["typ"] == "Blasser Hirsch" else 50
            if spieler["wahrnehmung"] >= 3 or spieler["sensibilitaet"] >= 2:
                echo_chance = 40 if gegner["typ"] == "Blasser Hirsch" else 25
            if random.randint(1, 100) <= echo_chance:
                print("Deine Waffe fährt durch die Gestalt hindurch. Sie zerfließt im Nebel.")
                aktion = "ins_leere"

        if aktion == "zauber":  
            magier_resonanz_wurf = random.randint(1, 100)
            if magier_resonanz_wurf <= 90:
                magier_resonanz_basis = random.randint(14, 20)
                magier_resonanz_schaden = (
                    magier_resonanz_basis
                    + 2 * magier_geist
                    + 2 * magier_uebersinnliches
                )
                gegner["hp"] = max(0, gegner["hp"] - magier_resonanz_schaden)
                print(f"Dein Resonanzstoß trifft den {gegner['typ']} für {magier_resonanz_schaden} Schaden.")
            else:
                print("Dein Resonanzstoß verfehlt den Gegner.")
            if gegner["hp"] <= 0:
                print(f"Der {gegner['typ']} wurde besiegt.")
                break
            if (gegner["typ"] == "Bandit"
                    and gegner["hp"] <= gegner["max_hp"] * 0.25
                    and not bandit_raserei):
                bandit_raserei = True
                print(f"Der {gegner['typ']} gerät in Panik!")
                print("Er kämpft jetzt wilder, lässt dabei aber seine Deckung fallen.")

        if aktion == "angriff":

            if wolf_sprung_diese_runde and spieler["waffe"]["typ"] == "Speer" and angriffs_name == "Schneller Stich":
                wolf_konter_versucht = True
                wolf_abfangen_chance = 30

                wolf_abfangen_chance += max(0, spieler["geschick"] - 2) * 3

                wolf_abfangen_chance += (spieler["wahrnehmung"] - 2) * 2

                if situation["umgebung"] == "Lichtung":
                    wolf_abfangen_chance += 5
                elif situation["umgebung"] == "Dichter Wald":
                    wolf_abfangen_chance -= 10

                wolf_abfangen_chance = max(10, min(80, wolf_abfangen_chance))
                wolf_abfangen_wurf = random.randint(1, 100)

                if wolf_abfangen_wurf <= wolf_abfangen_chance:
                    treffer_art = "voll"
                    wolf_sprung_abgefangen = True
                else:
                    treffer_art = "verfehlt"


            if wolf_sprung_diese_runde and spieler["waffe"]["typ"] == "Schwert" and angriffs_name == "Schneller Hieb":
                wolf_schwert_konter = True
                schwert_konter_chance = 25

                schwert_konter_chance += max(0, spieler["geschick"] - 2) * 3

                schwert_konter_chance += (spieler["wahrnehmung"] - 2) * 2

                if situation["umgebung"] == "Lichtung":
                    schwert_konter_chance += 5
                elif situation["umgebung"] == "Dichter Wald":
                    schwert_konter_chance -= 5

                schwert_konter_chance = max(10, min(80, schwert_konter_chance))

                if random.randint(1, 100) <= schwert_konter_chance:
                    wolf_schwert_konter_erfolgreich = True

        
            if not wolf_konter_versucht:
                grund_trefferchance = 80

                spieler_trefferchance = grund_trefferchance
                spieler_trefferchance += effekte["trefferchance_spieler"]
                spieler_trefferchance -= effekte["ausweichchance_gegner"]
                spieler_trefferchance += angriffs_treffer_mod
                spieler_trefferchance += bonus_durch_oeffnung
                spieler_trefferchance += netz_spieler_bonus
                netz_spieler_bonus = 0
                if fokus_diese_runde:
                    spieler_trefferchance += fokus_treffer_bonus

                if wolf_sprung_diese_runde and angriffs_name == "Schwerer Stich":
                    spieler_trefferchance -= 30

                if runde <= schmuggler_benommen_bis:
                    spieler_trefferchance -= 10

                spieler_trefferchance = max(0, min(100, spieler_trefferchance))
                streifgrenze = min(100, spieler_trefferchance + 15)
                angriff_wurf = random.randint(1, 100)

                if angriff_wurf <= spieler_trefferchance:
                    treffer_art = "voll"
                elif angriff_wurf <= streifgrenze:
                    treffer_art = "streif"
                else:
                    treffer_art = "verfehlt"

            if wolf_schwert_konter and treffer_art != "voll":
                wolf_schwert_konter_erfolgreich = False


            if (
                gegner["typ"] == "Bandit"
                and angriffs_name == "Schwerer Stich"
                and treffer_art == "verfehlt"
            ):
                bandit_konter_bonus = 20

            if (
                letzter_combo_angriff == "Kräftiger Hieb"
                and angriffs_name == "Schneller Hieb"
                and treffer_art == "voll"
            ):
                combo_nachsetzen = True

            if (
                letzter_combo_angriff == "Schneller Hieb"
                and angriffs_name == "Kräftiger Hieb"
                and treffer_art == "voll"
            ):
                combo_durchbruch = True

            # =========================
            # SPIELER-SCHADEN / KRIT
            # =========================

            schaden = 0
            krit = False
            krit_wurf = 0

            krit_chance = 5
            krit_chance += spieler["glück"] * 2
            krit_chance += effekte["krit_chance_spieler"]
            krit_chance += krit_mod_diese_runde

            if combo_nachsetzen:
                krit_chance += 30


            if starkes_taumeln_aktiv and angriffs_name == "Schneller Hieb":
                krit_chance += 20

            krit_chance = max(0, min(100, krit_chance))

            if treffer_art == "voll":

                schaden = random.randint(spieler["waffe"]["schaden_min"], spieler["waffe"]["schaden_max"])

                schaden = int(schaden * angriffs_schaden_faktor)
                if starkes_taumeln_aktiv and angriffs_name == "Schneller Stich":
                    schaden = int(schaden * schadensbonus_durch_taumeln)

                krit_wurf = random.randint(1, 100)
                krit = krit_wurf <= krit_chance

                if krit:
                    schaden = int(schaden * 1.5)

            elif treffer_art == "streif":

                schaden = random.randint(spieler["waffe"]["schaden_min"], spieler["waffe"]["schaden_max"])

                schaden = int(schaden * angriffs_schaden_faktor)
                if starkes_taumeln_aktiv and angriffs_name == "Schneller Stich":
                    schaden = int(schaden * schadensbonus_durch_taumeln)

                schaden = int(schaden * 0.4)


            if (
                treffer_art in ("voll", "streif")
                and angriffs_name in (
                    "Schwerer Stich",
                    "Kräftiger Hieb",
                    "Wuchtiger Hieb",
                    "Spaltender Hieb"
                )
            ):
                schaden = int(
                    schaden * staerke_schaden_faktor
                )

            if treffer_art == "voll":
                letzter_combo_angriff = angriffs_name
            else:
                letzter_combo_angriff = None

            if (
                spieler["waffe"]["typ"] == "Messer"
                and angriffs_name == "Schneller Schnitt"
                and treffer_art == "voll"
            ):
                messer_oeffnung_naechste_runde = True

            if (
                spieler["waffe"]["typ"] == "Beil"
                and angriffs_name == "Spaltender Hieb"
                and treffer_art == "voll"
            ):
                beil_druck_diese_runde = True

            if spaeher_luecke_diese_runde and schaden > 0:
                schaden = int(schaden * 1.35)
                print("Du nutzt die Lücke für einen gezielten Angriff!")

            if bestienjaeger_gelernt and bestienjaeger_studiert and schaden > 0:
                faktor = 1.80 if bestienjaeger_jagdhieb_diese_runde else 1.20
                schaden = int(schaden * faktor)
                if bestienjaeger_jagdhieb_diese_runde:
                    bestienjaeger_jagdhieb_getroffen = True
                    print("Dein gezielter Jagdhieb trifft die studierte Beute!")

            if stahlkrieger_schmiedehieb_diese_runde and schaden > 0:
                schaden = int(schaden * 1.50)
                stahlkrieger_schmiedehieb_getroffen = True
                print("Dein Schmiedehieb trifft mit der Wucht des Gegenangriffs!")

            if glutkrieger_kraftschub_diese_runde and schaden > 0:
                schaden = int(schaden * 1.60)
                glutkrieger_kraftschub_getroffen = True
                print("Dein Kraftschub trifft mit gesammelter Stärke!")

            if krieger_konter_aktiv and schaden > 0:
                schaden = int(schaden * 1.30)
                print("Du nutzt die vorbereitete Gegenangriffsöffnung!")

            if gegenschlag_aktiv and schaden > 0:
                schaden = int(schaden * 1.25)
                print("Gegenschlag: Du nutzt deine gelungene Abwehr.")

            if bandit_raserei:
                schaden = int(schaden * 1.25)

            if schaden > 0:
                schaden += (
                    schaden_bonus_diese_runde
                )

            if schaden > 0 and glutkrieger_bonus_aktiv:
                schaden += 3
                print("Kampfportion stärkt deinen Waffentreffer: +3 Schaden.")

            if schaden > 0 and waffenpflege_anwendungen > 0:
                schaden += waffenpflege_bonus
                if waffenpflege_ganzer_kampf:
                    print(f"Waffenpflege wirkt: +{waffenpflege_bonus} Schaden.")
                else:
                    waffenpflege_anwendungen -= 1
                    print(f"Waffenpflege wirkt: +{waffenpflege_bonus} Schaden. Verbleibende Anwendungen: {waffenpflege_anwendungen}.")

            if (gegner["typ"] in ("Gezeitenkrebs", "Einscherer") and krebs_halt_runden > 0
                    and schaden > 0 and spieler["waffe"].get("typ") != "Messer"):
                schaden = max(1, int(schaden * 0.5))
                print("Mit festgehaltenem Arm triffst du nur halb so hart.")

            if gegner["typ"] in ("Schieferpanzer", "Steinvater", "Schachtkriecher") and schaden > 0:
                platten = "Panzerplatten" if gegner["typ"] == "Schachtkriecher" else "Steinplatten"
                schwerer_schlag = (
                    angriffs_schaden_faktor > 1.1
                    or spieler["waffe"].get("typ") == "Hammer"
                )
                if panzer_eingerollt:
                    if schwerer_schlag:
                        schaden = max(1, int(schaden * 0.4))
                        print("Dein Schlag prallt an den eingerollten Platten ab.")
                    else:
                        print("Du triffst genau in eine Lücke zwischen den Platten.")
                elif not panzer_gebrochen:
                    if schwerer_schlag:
                        panzer_risse += 1
                        if panzer_risse >= (3 if gegner["typ"] == "Steinvater" else 2):
                            panzer_gebrochen = True
                            print("Mit einem lauten Knacken bricht der Panzer auf!")
                            angekuendigt.add("panzer_bruch")
                        else:
                            print(f"Ein Riss zieht sich durch die {platten}.")
                    elif spieler["waffe"].get("typ") == "Messer":
                        schaden = max(1, int(schaden * 0.7))
                        print("Deine Klinge findet eine Fuge zwischen den Platten.")
                    else:
                        schaden = max(1, int(schaden * 0.4))
                        print(f"Dein schneller Angriff schrammt nur über die {platten}.")
                else:
                    schaden = int(schaden * 1.2)

            gegner["hp"] -= schaden

            if gegner["hp"] < 0:
                gegner["hp"] = 0


            # Kurzer sichtbarer Kampftext

            if wolf_konter_versucht and wolf_sprung_abgefangen:
                farbig_ausgeben(f"Du fängst den Wolf im Sprung mit deinem Speer ab und verursachst {schaden} Schaden!", "blau")

            elif wolf_konter_versucht:
                print("Du setzt den Speer zu spät an – der Wolf durchbricht deine Abwehr!")

            elif wolf_schwert_konter and wolf_schwert_konter_erfolgreich:
                farbig_ausgeben(f"Du erwischst den Wolf im Sprung mit deinem Schwert und verursachst {schaden} Schaden!", "blau")
                print("Der Treffer bringt ihn aus der Bahn!")

            elif wolf_schwert_konter and treffer_art == "verfehlt":
                print("Dein schneller Hieb geht am Wolf vorbei!")

            elif gegner["typ"] == "Bandit" and treffer_art == "verfehlt" and angriffs_name == "Schwerer Stich":
                print("Dein schwerer Stich geht vorbei – der Bandit nutzt deine Blöße!")

            elif treffer_art == "verfehlt":
                print(f"Du verfehlst den {gegner['typ']}.")

            elif (starkes_taumeln_aktiv and angriffs_name == "Schneller Stich" and krit):
                farbig_ausgeben(f"Du nutzt das Taumeln perfekt! Dein schneller Stich trifft kritisch für {schaden} Schaden!", "gelb")

            elif (starkes_taumeln_aktiv and angriffs_name == "Schneller Stich"):
                farbig_ausgeben(f"Du nutzt das Taumeln! Dein schneller Stich verursacht {schaden} Schaden.", "blau")

            elif starkes_taumeln_aktiv and angriffs_name == "Schneller Hieb" and krit:
                farbig_ausgeben(f"Du nutzt die offene Deckung perfekt! Dein schneller Hieb trifft kritisch für {schaden} Schaden!", "gelb")

            elif starkes_taumeln_aktiv and angriffs_name == "Schneller Hieb" and treffer_art == "voll":
                farbig_ausgeben(f"Du nutzt die offene Deckung und triffst den {gegner['typ']} für {schaden} Schaden.", "blau")

            elif treffer_art == "streif":
                farbig_ausgeben(f"Du streifst den {gegner['typ']} und verursachst {schaden} Schaden.", "blau")

            elif combo_nachsetzen and krit:
                print("Combo: Nachsetzen!")
                farbig_ausgeben(f"Du nutzt die Bewegung des Gegners und triffst kritisch für {schaden} Schaden!", "gelb")

            elif combo_nachsetzen:
                print("Combo: Nachsetzen!")
                farbig_ausgeben(f"Du setzt sofort nach und verursachst {schaden} Schaden!", "blau")

            elif krit:
                farbig_ausgeben(f"Kritischer Treffer! Du verursachst {schaden} Schaden.", "gelb")

            else:
                farbig_ausgeben(f"Du triffst den {gegner['typ']} für {schaden} Schaden.", "blau")

            if (
                beil_druck_diese_runde
                and gegner["hp"] > 0
            ):
                print(
                    "Die Wucht deines Hiebs bringt den Gegner "
                    "aus dem Rhythmus."
                )

                print(
                    "Sein nächster Angriff ist ungenauer."
                )

            if gegner["typ"] == "Bandit" and gegner["hp"] <= gegner["max_hp"] * 0.25 and gegner["hp"] > 0 and not bandit_raserei:
                bandit_raserei = True
                print(f"Der {gegner['typ']} gerät in Panik!")
                print("Er kämpft jetzt wilder, lässt dabei aber seine Deckung fallen.")

            if (gegner["typ"] in ("Glutsalamander", "Aschenkönig") and salamander_gluehen
                    and spieler["waffe"].get("reichweite", 1) <= 1):
                if glutkrieger_bonus_aktiv:
                    print("Die Hitze der Schuppen erreicht dich kaum. Die Glut in dir hält dagegen.")
                else:
                    verbrennung = (random.randint(6, 9) if angriffs_schaden_faktor > 1.1
                                   else random.randint(4, 6))
                    spieler["hp"] = max(1, spieler["hp"] - verbrennung)
                    farbig_ausgeben(f"Du verbrennst dich an den glühenden Schuppen und erleidest {verbrennung} Schaden.", "rot")

            if (gegner["typ"] in ("Glutsalamander", "Aschenkönig") and treffer_art == "voll"
                    and gegner["hp"] > 0
                    and random.randint(1, 100) <= (50 if gegner["typ"] == "Aschenkönig" else 35)):
                salamander_eingegraben_naechste_runde = True
                print(f"Der {gegner['typ']} wühlt sich blitzschnell in die Asche.")
                angekuendigt.add("salamander_eingraben")

            if (gegner["typ"] == "Graupelz" and 0 < gegner["hp"] <= gegner["max_hp"] * 0.6
                    and not graupelz_geheult):
                graupelz_geheult = True
                rudel_runden = 3
                print("Graupelz wirft den Kopf zurück und heult.")
                print("Aus dem Unterholz antworten zwei Wölfe und kommen heran.")
                angekuendigt.add("graupelz_heulen")

            if (gegner["typ"] == "Wrackplünderer" and 0 < gegner["hp"] <= gegner["max_hp"] * 0.25
                    and not gnade_angekuendigt):
                gnade_angekuendigt = True
                gnade_bereit = True
                print("Der Wrackplünderer weicht zurück und hebt die Hände.")
                angekuendigt.add("pluenderer_gnade")

            if (gegner["typ"] == "Kohlenschmuggler" and 0 < gegner["hp"] <= gegner["max_hp"] * 0.25
                    and not schmuggler_flucht_angekuendigt):
                schmuggler_flucht_angekuendigt = True
                schmuggler_flucht_bereit = True
                print("Der Kohlenschmuggler weicht zurück. Er sucht einen Ausweg.")
                angekuendigt.add("schmuggler_flucht")

            # Gegner tot -> kein Gegenangriff

            if gegner["hp"] <= 0:
                print(f"Der {gegner['typ']} wurde besiegt.")
                break

            if wolf_sprung_abgefangen:
                runde += 1
                continue

        if combo_durchbruch and gegner["hp"] > 0:
            gegner_zurueckgedraengt_naechste_runde = True

            print()
            print("Combo: Durchbruch!")
            print(f"Dein kräftiger Hieb drängt den {gegner['typ']} zurück!")


        if wolf_bereitet_sprung_vor:
            text_pause("kampf")
            print()

            if aktion == "angriff" and spieler["waffe"]["typ"] == "Schwert":

                unterbrechung_chance = 0

                if angriffs_name == "Schneller Hieb":
                    unterbrechung_chance = 50

                elif angriffs_name == "Kräftiger Hieb":
                    unterbrechung_chance = 30

                if combo_durchbruch:
                    unterbrechung_chance = 100

                if treffer_art == "voll" and random.randint(1, 100) <= unterbrechung_chance:
                    wolf_sprungbereit = False
                    print("Dein Angriff bringt den Wolf aus seinem Ansatz!")
                    print("Der Wolf muss seinen Sprung abbrechen!")

                else:
                    wolf_sprung_verstaerkt = True
                    print("Du schaffst es nicht, den Wolf zu unterbrechen!")
                    print("Der Wolf wird noch aggressiver!")

            if wolf_sprungbereit:
                print("Der Wolf hält Abstand und bereitet seinen Sprung weiter vor.")

            runde += 1
            continue

        if keiler_bereitet_ansturm_vor:
            text_pause("kampf")
            print()

            if aktion == "angriff" and spieler["waffe"]["typ"] == "Schwert":

                unterbrechung_chance = 0

                if angriffs_name == "Schneller Hieb":
                    unterbrechung_chance = 20

                elif angriffs_name == "Kräftiger Hieb":
                    unterbrechung_chance = 55

                if combo_durchbruch:
                    unterbrechung_chance = 100

                if treffer_art == "voll" and random.randint(1, 100) <= unterbrechung_chance:
                    keiler_ansturm_bereit = False
                    print("Dein Angriff bringt den Keiler aus dem Gleichgewicht!")
                    print("Der Keiler muss seinen Ansturm abbrechen!")

                else:
                    keiler_ansturm_verstaerkt = True
                    print("Du schaffst es nicht, den Keiler aufzuhalten!")
                    print("Der Keiler setzt seinen Ansturm unbeirrt fort!")

            if keiler_ansturm_bereit:
                print("Der Keiler hält Abstand und bereitet seinen Ansturm weiter vor.")


            runde += 1
            continue

        if keiler_speer_abfangen_erfolgreich:

            keiler_speer_schaden = random.randint(
                spieler["waffe"]["schaden_min"],
                spieler["waffe"]["schaden_max"]
            )

            keiler_speer_schaden = int(keiler_speer_schaden * 1.60)

            if keiler_speer_schaden > 0:
                keiler_speer_schaden += (
                    schaden_bonus_diese_runde
                )

            gegner["hp"] -= keiler_speer_schaden
            gegner["hp"] = max(0, gegner["hp"])

            starkes_taumeln_naechste_runde = True

            farbig_ausgeben(f"Der Keiler läuft direkt in deinen Speer! Du verursachst {keiler_speer_schaden} Schaden.", "blau")

            if gegner["hp"] <= 0:
                if bestienjaeger_gelernt:
                    bestienjaeger_abwehr_erfolgreich = True
                if stahlkrieger_gelernt and stahlkrieger_amboss_diese_runde:
                    stahlkrieger_amboss_erfolgreich = True
                print("Der Keiler bricht zusammen.")
                break

        if keiler_erholt_sich_diese_runde:
            print("Der Keiler sammelt sich und setzt zum nächsten Schritt an.")
            runde += 1
            continue

        if gegner_im_wurfnetz and not wurfnetz_gross:
            gegner_im_wurfnetz = False
            print(f"Der {gegner['typ']} zerrt am Netz und kommt nicht zum Angriff.")
            runde += 1
            continue

        if keiler_ansturm_diese_runde:
            keiler_erholt_sich_naechste_runde = True

        if salamander_eingegraben_naechste_runde:
            runde += 1
            continue

        if kreischer_in_luft:
            runde += 1
            continue

        if (gegner["typ"] in ("Echohirsch", "Blasser Hirsch") and aktion == "verteidigen"
                and gegner["hp"] > 0 and not echo_erkannt):
            echo_erkannt_naechste_runde = True
            print()
            print("Du wartest ab und beobachtest. Nur eine der Gestalten lässt das Gras unter sich knicken.")
            angekuendigt.add("echo_erkannt")

        if rudel_runden > 0 and gegner["hp"] > 0:
            if aktion == "verteidigen":
                print("Du hältst die beiden Wölfe mit der Waffe auf Abstand.")
            else:
                rudel_biss = random.randint(4, 7)
                spieler["hp"] = max(0, spieler["hp"] - rudel_biss)
                farbig_ausgeben(f"Ein Wolf aus dem Rudel beißt zu: {rudel_biss} Schaden.", "rot")
                if spieler["hp"] <= 0 and talent_unbeugsam and not unbeugsam_genutzt:
                    spieler["hp"] = 1
                    unbeugsam_genutzt = True
                    print("Unbeugsam: Du bleibst mit 1 Leben stehen.")
            rudel_runden -= 1
            if rudel_runden == 0:
                print("Die beiden Wölfe ziehen sich ins Unterholz zurück.")

        if gegner["typ"] == "Wrackplünderer" and gnade_diese_runde and gegner["hp"] > 0:
            if aktion == "verteidigen":
                gegner_verschont = True
                gegner["hp"] = 0
                print()
                print("Du lässt ihn gehen. Er wirft dir seinen Geldbeutel vor die Füße und rennt den Strand hinunter.")
                angekuendigt.add("pluenderer_verschont")
                break
            print("Der Wrackplünderer greift wieder nach seinem Haken.")

        if gegner["typ"] in ("Gezeitenkrebs", "Einscherer") and krebs_halt_runden > 0 and aktion == "verteidigen":
            losreissen_chance = max(20, min(90, 50 + 10 * (spieler["staerke"] - 1)
                                            - (10 if gegner["typ"] == "Einscherer" else 0)))
            if random.randint(1, 100) <= losreissen_chance:
                krebs_halt_runden = 0
                oeffnung_naechste_runde = True
                print()
                print("Du reißt deinen Arm aus der Schere los!")
                angekuendigt.add("krebs_losreissen")
                runde += 1
                continue
            print()
            print("Du stemmst dich gegen die Schere, aber sie hält dich fest.")

        if (gegner["typ"] == "Kohlenschmuggler" and schmuggler_flucht_diese_runde
                and schmuggler_flucht_bereit and gegner["hp"] > 0):
            if aktion == "verteidigen":
                abschneiden_chance = max(30, min(90, 60 + 8 * (spieler["geschick"] - 1)
                                                 + 5 * spieler["waffe"].get("wendigkeit", 1)))
                if random.randint(1, 100) <= abschneiden_chance:
                    schmuggler_flucht_bereit = False
                    gegner["hp"] = 0
                    print()
                    print("Du stellst dich ihm in den Weg. Er kommt nicht an dir vorbei.")
                    print("Der Kohlenschmuggler lässt den Knüppel fallen und gibt auf.")
                    break
                else:
                    gegner_geflohen = True
            elif random.randint(1, 100) <= 50:
                gegner_geflohen = True
            if gegner_geflohen:
                print()
                print("Der Kohlenschmuggler rennt zwischen den Baumstümpfen davon.")
                print("Im Laufen verliert er einen Teil seines Geldes.")
                break

        # =========================
        # GEGNER-ANGRIFF
        # =========================
        text_pause("kampf")
        print()
        gegner_grund_trefferchance = 80

        gegner_trefferchance = gegner_grund_trefferchance
        gegner_trefferchance -= ausweich_mod_diese_runde
        if gegner_im_wurfnetz:
            gegner_im_wurfnetz = False
            gegner_trefferchance -= 30
            print("Die Netzreste behindern ihn noch.")

        gegner_trefferchance += effekte["trefferchance_gegner"]
        gegner_trefferchance -= effekte["ausweichchance_spieler"]
        gegner_trefferchance += bandit_konter_bonus

        if beil_druck_diese_runde:
            gegner_trefferchance -= 15

        spezial_schaden_faktor = 1.0


        if gegner_spezialangriff:
            gegner_trefferchance -= 10
            spezial_schaden_faktor = 2.5

        elif wolf_sprung_diese_runde:
            gegner_trefferchance += 10
            spezial_schaden_faktor = 2.2

            if aktion == "angriff" and angriffs_name == "Schwerer Stich":
                gegner_trefferchance += 20
                print("Dein schwerer Stich ist zu langsam – der Wolf nutzt die Öffnung!") 

        elif keiler_ansturm_diese_runde:
            gegner_trefferchance += 10
            spezial_schaden_faktor = 2.0

        elif kreischer_sturz_diese_runde:
            gegner_trefferchance += 10
            spezial_schaden_faktor = 2.0

        elif graupelz_sprung_diese_runde:
            gegner_trefferchance += 10
            spezial_schaden_faktor = 2.0

        elif rudellos_sprung_diese_runde:
            gegner_trefferchance += 10
            spezial_schaden_faktor = 1.8
            if aktion != "verteidigen":
                print("Der Wolf springt dich ohne jede Vorwarnung an!")

        elif gegner["typ"] in ("Gezeitenkrebs", "Einscherer") and krebs_halt_runden > 0 and not krebs_packen_diese_runde:
            spezial_schaden_faktor = 0.7

        elif salamander_eingegraben and aktion != "verteidigen":
            gegner_trefferchance += 10
            spezial_schaden_faktor = 1.5
            print(f"Der {gegner['typ']} bricht unter dir aus der Asche hervor!")






        if wolf_sprung_verstaerkt_diese_runde:
            spezial_schaden_faktor *= 1.25

        if keiler_ansturm_verstaerkt_diese_runde:
            spezial_schaden_faktor *= 1.25



        if runde == 1:
            gegner_trefferchance += start_effekte["trefferchance_gegner"]
            gegner_trefferchance -= start_effekte["ausweichchance_spieler"]
        if gelehrter_muster_aktiv:
            gegner_trefferchance -= 15
        gegner_trefferchance = max(5, min(95, gegner_trefferchance))

        gegner_streifgrenze = min(100, gegner_trefferchance + 15)

        gegner_angriff_wurf = random.randint(1, 100)

        if gegner_angriff_wurf <= gegner_trefferchance:
            gegner_treffer_art = "voll"

        elif gegner_angriff_wurf <= gegner_streifgrenze:
            gegner_treffer_art = "streif"

        else:
            gegner_treffer_art = "verfehlt"

        if keiler_ansturm_diese_runde and (
            keiler_ausweichen_erfolgreich or keiler_speer_abfangen_erfolgreich
        ):
            gegner_treffer_art = "verfehlt"

        if schmuggler_aschewurf_diese_runde:
            if aktion == "verteidigen":
                oeffnung_naechste_runde = True
                print("Du drehst den Kopf rechtzeitig weg. Die Asche verfehlt deine Augen.")
            else:
                schmuggler_benommen_bis = runde + 2
                farbig_ausgeben("Asche trifft dich in die Augen. Du bist benommen.", "rot")

        if rudellos_sprung_diese_runde and aktion == "verteidigen":
            gegner_treffer_art = "verfehlt"
            oeffnung_naechste_runde = True
            print("Du hast den Sprung kommen sehen und weichst ihm aus.")

        if (graupelz_sprung_diese_runde and aktion == "verteidigen"
                and spieler["waffe"].get("reichweite", 1) >= 3):
            gegner_treffer_art = "verfehlt"
            oeffnung_naechste_runde = True
            print("Du stemmst die Waffe gegen den Boden und fängst den Sprung ab.")

        if krebs_packen_diese_runde:
            if aktion == "verteidigen":
                gegner_treffer_art = "verfehlt"
                oeffnung_naechste_runde = True
                print("Du weichst der Schere im letzten Moment aus.")
            else:
                gegner_treffer_art = "voll"
                krebs_halt_runden = 3 if gegner["typ"] == "Einscherer" else 2
                print("Die Schere schließt sich um deinen Arm!")
        elif krebs_halt_runden > 0:
            gegner_treffer_art = "voll"
            krebs_halt_runden -= 1
            if krebs_halt_runden == 0:
                print("Der Krebs kneift ein letztes Mal zu und lässt dann los.")

        if netz_wurf_diese_runde:
            if aktion == "verteidigen":
                oeffnung_naechste_runde = True
                print("Du duckst dich unter dem Netz weg.")
            else:
                netz_naechste_runde = True
                print("Das Netz legt sich über dich!")

        if (kreischer_sturz_diese_runde and aktion == "verteidigen"
                and spieler["waffe"].get("reichweite", 1) >= 3):
            gegner_treffer_art = "verfehlt"
            oeffnung_naechste_runde = True
            print("Du hältst die Waffe hoch und fängst den Sturzflug ab.")

        if salamander_eingegraben and aktion == "verteidigen":
            gegner_treffer_art = "verfehlt"
            oeffnung_naechste_runde = True
            print(f"Du wartest ab. Als der {gegner['typ']} aus der Asche bricht, bist du bereit.")  

        gegner_treffer_art_original = gegner_treffer_art

        # =========================
        # SPIELER-PARADE
        # =========================

        parade_wurf = 0
        parade_erfolgreich = False

        aktuelle_paradechance = effekte["paradechance_spieler"]
        aktuelle_paradechance += parade_mod_diese_runde
        aktuelle_paradechance += talent_parade_bonus



        if wolf_sprung_diese_runde or keiler_ansturm_diese_runde or waldwaechter_spezialangriff:
            aktuelle_paradechance = 0

        elif gegner_spezialangriff and aktion != "verteidigen":
            aktuelle_paradechance = 0

        if runde == 1:
            aktuelle_paradechance += start_effekte["paradechance_spieler"]

        aktuelle_paradechance = max(0, min(100, aktuelle_paradechance))

        if gegner_treffer_art != "verfehlt":

            parade_wurf = random.randint(1, 100)

            parade_erfolgreich = (parade_wurf <= aktuelle_paradechance)

            if parade_erfolgreich:

                if gegner_treffer_art == "voll":
                    gegner_treffer_art = "streif"

                elif gegner_treffer_art == "streif":
                    gegner_treffer_art = "blockiert"

        if gegner_spezialangriff and aktion == "verteidigen":
            gegner_treffer_art = "blockiert"

        gegner_krit = False
        gegner_krit_chance = gegner["krit_chance"] + effekte["krit_chance_gegner"]

        if runde == 1:
            gegner_krit_chance += start_effekte["krit_chance_gegner"]

        if gelehrter_muster_aktiv:
            gegner_krit_chance -= 10
        gegner_krit_chance = max(0, min(100, gegner_krit_chance))

        # =========================
        # GEGNER-SCHADEN
        # =========================

        gegner_schaden = 0

        if gegner_treffer_art in ("voll", "streif"):
            if waldwaechter_spezialangriff:
                gegner_schaden = random.randint(35, 50)
            else:
                gegner_schaden = random.randint(
                    gegner["waffe"]["schaden_min"],
                    gegner["waffe"]["schaden_max"]
                )

            gegner_schaden = int(gegner_schaden * spezial_schaden_faktor)

            if gegner_treffer_art == "streif":
                gegner_schaden = int(gegner_schaden * 0.4)

            elif not (
                gegner_spezialangriff
                or wolf_sprung_diese_runde
                or keiler_ansturm_diese_runde
                or waldwaechter_spezialangriff
            ):
                gegner_krit_wurf = random.randint(1, 100)
                gegner_krit = gegner_krit_wurf <= gegner_krit_chance

                if gegner_krit:
                    gegner_schaden = int(gegner_schaden * 1.5)

        if gegner["typ"] == "Waldwächter" and aktion == "verteidigen":
            gegner_schaden //= 2

        if bandit_raserei and not gegner_spezialangriff:
            gegner_schaden = int(gegner_schaden * 1.20)

        if wolf_sprung_diese_runde and aktion == "verteidigen":
            gegner_schaden = int(gegner_schaden * 0.60)

        elif wolf_sprung_diese_runde and wolf_schwert_konter_erfolgreich:
            gegner_schaden = int(gegner_schaden * 0.50)

        if keiler_ansturm_diese_runde and aktion == "verteidigen":
            gegner_schaden = int(gegner_schaden * 0.60)

        standhalten_gegenschaden = 0

        if aktion == "standhalten":
            if gegner_schaden > 0:
                schwerer_angriff = (
                    gegner_spezialangriff
                    or wolf_sprung_diese_runde
                    or keiler_ansturm_diese_runde
                    or waldwaechter_spezialangriff
                )

                standhalten_chance = 70 if schwerer_angriff else 40

                if random.randint(1, 100) <= standhalten_chance:
                    gegner_schaden = int(gegner_schaden * 0.50)

                    standhalten_gegenschaden = random.randint(
                        spieler["waffe"]["schaden_min"],
                        spieler["waffe"]["schaden_max"]
                    )
                    standhalten_gegenschaden = int(
                        standhalten_gegenschaden
                        * staerke_schaden_faktor
                        * 1.80
                    )

                    if standhalten_gegenschaden > 0:
                        standhalten_gegenschaden += (
                            schaden_bonus_diese_runde
                        )

                    print("Du hältst stand und fängst einen Teil der Wucht ab!")
                else:
                    print("Du findest keinen sicheren Ansatz für deinen Gegenschlag.")
            else:
                print("Kein Treffer dringt durch – dein Gegenschlag bleibt aus.")

        if (
            talent_standhaft
            and gegner_schaden > 0
            and gegner["max_hp"] >= 120
        ):
            gegner_schaden = max(1, int(gegner_schaden * 0.95))
        if (
            gegner_schaden > 0
            and zaehigkeit_schadensreduktion > 0
        ):
            gegner_schaden = max(
                1,
                int(
                    gegner_schaden
                    * (
                        1.0
                        - zaehigkeit_schadensreduktion
                    )
                )
            )

        if (
            gegner_schaden > 0
            and ruestung_schutz > 0
        ):
            gegner_schaden = max(
                1,
                gegner_schaden
                - ruestung_schutz
            )

        if stahlkrieger_gelernt and runde <= stahlkrieger_amboss_bis and gegner_schaden > 0:
            vorher = gegner_schaden
            gegner_schaden = max(1, gegner_schaden - 3)
            print(f"Ambossstand fängt {vorher - gegner_schaden} zusätzlichen Schaden ab.")

        hp_vor_treffer = spieler["hp"]
        spieler["hp"] -= gegner_schaden

        # Zweiter Atem nur bei einem nicht tödlichen Treffer von 30+ auf 1–29.
        zweiter_atem_jetzt = (
            talent_zweiter_atem
            and not zweiter_atem_genutzt
            and hp_vor_treffer >= 30
            and 1 <= spieler["hp"] <= 29
        )

        # Blutung nur nach tatsächlichem Schaden (verfehlt und blockiert zählen nicht).
        if (
            spieler["hp"] > 0
            and (blutungsschutz <= 0 or random.randint(1, 100) > blutungsschutz)
        ):
            kampf_status_nach_gegnertreffer(
                gegner,
                gegner_treffer_art,
                gegner_schaden,
                gegner_krit,
                status_effekte,
                status_definitionen,
                gegner_spezialangriff=gegner_spezialangriff,
                wolf_sprung=wolf_sprung_diese_runde,
                keiler_ansturm=keiler_ansturm_diese_runde
            )

        # Schachtspinner: Giftbiss nach einem Treffer mit Schaden (Gift stapelt nicht).
        if (
            gegner["typ"] == "Schachtspinner"
            and spieler["hp"] > 0
            and gegner_schaden > 0
            and gegner_treffer_art in ("voll", "streif")
            and "gift" not in status_effekte
            and random.randint(1, 100) <= 30
        ):
            print("Der Biss brennt. Etwas breitet sich unter deiner Haut aus.")
            kampf_status_hinzufuegen(
                status_effekte,
                status_definitionen,
                "gift",
                quelle="kampf:Schachtspinner"
            )
            angekuendigt.add("spinner_gift")

        if spieler["hp"] <= 0 and talent_unbeugsam and not unbeugsam_genutzt:
            spieler["hp"] = 1
            unbeugsam_genutzt = True
            unbeugsam_meldung = True

        if zweiter_atem_jetzt and spieler["hp"] > 0:
            spieler["hp"] = min(spieler["max_hp"], spieler["hp"] + 12)
            zweiter_atem_genutzt = True
            zweiter_atem_meldung = True

        if (stahlkrieger_gelernt and aktion == "verteidigen"
                and spieler["hp"] > 0
                and (parade_erfolgreich or gegner_treffer_art in ("blockiert", "verfehlt"))):
            stahlkrieger_oeffnung_runde = runde + 1
            if stahlkrieger_amboss_diese_runde:
                stahlkrieger_amboss_erfolgreich = True
            print("Erfolgreiche Verteidigung: Schmiedehieb ist für die nächste Runde vorbereitet.")

        if (bestienjaeger_gelernt and aktion == "verteidigen"
                and spieler["hp"] > 0
                and (parade_erfolgreich or gegner_treffer_art in ("blockiert", "verfehlt"))):
            bestienjaeger_abwehr_erfolgreich = True

        if (
            krieger_deckung_diese_runde
            and spieler["hp"] > 0
            and (parade_erfolgreich or gegner_treffer_art in ("blockiert", "verfehlt"))
        ):
            krieger_konter_runde = runde + 1
            print("Deckung gehalten: Dein Gegenangriff ist für die nächste Runde vorbereitet.")

        if (
            talent_gegenschlag
            and spieler["hp"] > 0
            and (
                parade_erfolgreich
                or (aktion == "verteidigen" and gegner_treffer_art in ("blockiert", "verfehlt"))
            )
        ):
            gegenschlag_runde = runde + 1

        if spieler["hp"] < 0:
            spieler["hp"] = 0

        # Kurzer sichtbarer Kampftext

        if gegner_spezialangriff and aktion == "verteidigen":
            print("Du fängst den Spezialangriff ab!")
            print(f"Der {gegner['typ']} verliert das Gleichgewicht und taumelt.")

        elif keiler_ansturm_diese_runde and keiler_speer_abfangen_erfolgreich:
            print("Der Keiler wird an deiner Speerspitze gestoppt und taumelt zurück!")

        elif keiler_ansturm_diese_runde and keiler_ausweichen_erfolgreich:
            print("Du springst im letzten Moment zur Seite! Der Keiler schießt an dir vorbei.")

        elif keiler_ansturm_diese_runde and gegner_treffer_art == "verfehlt":
            print("Der Keiler rauscht knapp an dir vorbei!")

        elif keiler_ansturm_diese_runde and keiler_speer_abfangen_versucht:
            farbig_ausgeben(f"Der Keiler durchbricht deine Speerstellung! Du erleidest {gegner_schaden} Schaden.", "rot")

        elif keiler_ansturm_diese_runde and aktion == "verteidigen":
            farbig_ausgeben(f"Du kommst nicht vollständig aus der Bahn und erleidest {gegner_schaden} Schaden.", "rot")

        elif keiler_ansturm_diese_runde and gegner_treffer_art == "streif":
            farbig_ausgeben(f"Der Keiler erwischt dich im Vorbeistürmen! Du erleidest {gegner_schaden} Schaden.", "rot")

        elif keiler_ansturm_diese_runde:
            farbig_ausgeben(f"Der Keiler rammt dich mit voller Wucht! Du erleidest {gegner_schaden} Schaden.", "rot")

        elif wolf_sprung_diese_runde and gegner_treffer_art == "verfehlt":
            print("Der Wolf springt an dir vorbei!")

        elif wolf_sprung_diese_runde and wolf_schwert_konter_erfolgreich:
            farbig_ausgeben(f"Der Wolf wird abgelenkt und erwischt dich nur noch seitlich! Du erleidest {gegner_schaden} Schaden.", "rot")

        elif wolf_sprung_diese_runde and aktion == "verteidigen":
            farbig_ausgeben(f"Du fängst einen Teil des Sprungs mit deinem {spieler['waffe']['typ']} ab und erleidest {gegner_schaden} Schaden.", "rot")

        elif wolf_sprung_diese_runde and gegner_treffer_art == "streif":
            farbig_ausgeben(f"Der Wolf erwischt dich im Vorbeispringen! Du erleidest {gegner_schaden} Schaden.", "rot")

        elif wolf_sprung_diese_runde:
            farbig_ausgeben(f"Der Wolf trifft dich mit voller Wucht! Du erleidest {gegner_schaden} Schaden.", "rot")

        elif gegner_treffer_art == "verfehlt":
            print(f"Der {gegner['typ']} verfehlt dich.")

        elif gegner_spezialangriff and gegner_treffer_art == "streif":
            farbig_ausgeben(f"Der Spezialangriff streift dich! Du erleidest {gegner_schaden} Schaden.", "rot")

        elif gegner_spezialangriff:
            farbig_ausgeben(f"Wuchtiger Treffer! Der Spezialangriff verursacht {gegner_schaden} Schaden!", "rot")

        elif gegner_treffer_art == "blockiert":
            print("Du blockierst den Angriff vollständig.")

        elif bandit_konter_bonus > 0 and gegner_krit:
            farbig_ausgeben(f"Kritischer Konter! Der {gegner['typ']} nutzt deine Blöße und verursacht {gegner_schaden} Schaden!", "rot")

        elif bandit_konter_bonus > 0 and gegner_treffer_art == "voll":
            farbig_ausgeben(f"Der {gegner['typ']} nutzt deine Blöße und trifft dich für {gegner_schaden} Schaden!", "rot")

        elif gegner_krit:
            farbig_ausgeben(f"Kritischer Treffer! Der {gegner['typ']} verursacht {gegner_schaden} Schaden!", "rot")

        elif parade_erfolgreich:
            farbig_ausgeben(f"Du parierst einen Teil des Angriffs und erleidest {gegner_schaden} Schaden.", "rot")

        elif gegner_treffer_art == "streif":
            farbig_ausgeben(f"Der {gegner['typ']} streift dich. Du erleidest {gegner_schaden} Schaden.", "rot")

        else:
            farbig_ausgeben(f"Der {gegner['typ']} trifft dich für {gegner_schaden} Schaden.", "rot")


        if unbeugsam_meldung:
            print("Unbeugsam: Du bleibst mit 1 Leben stehen.")

        if zweiter_atem_meldung:
            print(f"Zweiter Atem: Du fängst dich und hast wieder {spieler['hp']} HP.")

        if spieler["hp"] <= 0:
            print("Du wurdest besiegt.")
            break

        if standhalten_gegenschaden > 0:
            text_pause("kampf")

            gegner["hp"] = max(
                0,
                gegner["hp"] - standhalten_gegenschaden
            )

            farbig_ausgeben(
                f"Du antwortest mit einem mächtigen Hammerschlag! "
                f"Du verursachst {standhalten_gegenschaden} Schaden.",
                "blau"
            )

            if (
                gegner["typ"] == "Bandit"
                and 0 < gegner["hp"] <= gegner["max_hp"] * 0.25
                and not bandit_raserei
            ):
                bandit_raserei = True
                print(f"Der {gegner['typ']} gerät in Panik!")
                print("Er kämpft jetzt wilder, lässt dabei aber seine Deckung fallen.")

            if gegner["hp"] <= 0:
                print(f"Der {gegner['typ']} wurde besiegt.")
                break

        runde += 1

    kampf_status_bereinigen(
        status_effekte,
        status_definitionen
    )

    ergebnis = {
        "lebenspunkte": spieler["hp"],
        "heiltraenke": spieler["heiltraenke"],
        "bandagen": spieler["bandagen"],
        "wurfnetze": spieler["wurfnetze"],
        "wundsalben": spieler["wundsalben"],
        "gegengifte": spieler["gegengifte"],
        "gewonnen": gegner["hp"] <= 0,
        "geflohen": geflohen,
        "gegner_geflohen": gegner_geflohen,
        "gegner_verschont": gegner_verschont,
        "angekuendigt": sorted(angekuendigt),
        "besiegt": spieler["hp"] <= 0,
        "gegner_typ": gegner["typ"],
        "status_effekte": status_effekte
    }
    if bestienjaeger_gelernt:
        ergebnis.update(
            bestienjaeger_studiert=bestienjaeger_studiert,
            bestienjaeger_abwehr=bestienjaeger_abwehr_erfolgreich,
            bestienjaeger_jagdhieb=bestienjaeger_jagdhieb_getroffen
        )
    if stahlkrieger_gelernt:
        ergebnis.update(
            stahlkrieger_amboss=stahlkrieger_amboss_erfolgreich,
            stahlkrieger_schmiedehieb=stahlkrieger_schmiedehieb_getroffen
        )
    if glutkrieger_gelernt:
        ergebnis.update(
            glutkrieger_portion_verbraucht=glutkrieger_portion_verbraucht,
            glutkrieger_kraftschub=glutkrieger_kraftschub_getroffen
        )
    return ergebnis
if __name__ == "__main__":
    ergebnis = kampf_starten(lebenspunkte=70, heiltraenke=3)
    print("Kampfergebnis:", ergebnis)

# # =========================
# # TESTAUSGABE
# # =========================

# print("=== Situation ===")
# print("Gebiet:", situation["gebiet"])
# print("Tageszeit:", situation["tageszeit"])
# print("Gegner:", gegner["typ"])

# print()
# print("=== Umgebung ===")
# print("Deckung:", deckung)
# print("Versteckmöglichkeiten:", versteckmoeglichkeiten)
# print("Bewegungsfreiheit:", bewegungsfreiheit)
# print("Hinterhaltspotential:", hinterhaltspotential)
# print("Umgebungssicht:", umgebungs_sicht)

# print()
# print("=== Sicht ===")
# print("Spielersicht:", spieler_sicht)
# print("Gegnersicht:", gegner_sicht)

# print()
# print("=== Bewegung ===")
# print("Spieler-Bewegung:", spieler_bewegung)

# print()
# print("=== Deckung ===")
# print(
#     "Spieler-Deckungschance:",
#     spieler_deckung_chance
# )
# print(
#     "Spieler-Deckungswurf:",
#     spieler_deckung_wurf
# )
# print(
#     "Spieler hat Deckung:",
#     spieler_hat_deckung
# )

# print(
#     "Gegner-Deckungschance:",
#     gegner_deckung_chance
# )
# print(
#     "Gegner-Deckungswurf:",
#     gegner_deckung_wurf
# )
# print(
#     "Gegner hat Deckung:",
#     gegner_hat_deckung
# )

# print()
# print("=== Entdeckung ===")

# if gegner_entdeckt:
#     print("Du entdeckst den Gegner rechtzeitig.")
# else:
#     print("Du bemerkst den Gegner nicht.")

# print(
#     "Entdeckungschance:",
#     entdeckungs_chance
# )
# print(
#     "Entdeckungswurf:",
#     entdeckungs_wurf
# )
# print(
#     "Gegner-Verstecken:",
#     gegner_verstecken
# )

# print()
# print("=== Hinterhalt ===")
# print(
#     "Hinterhaltchance:",
#     hinterhalt_chance
# )
# print(
#     "Hinterhaltwurf:",
#     hinterhalt_wurf
# )
# print(
#     "Hinterhalt:",
#     hinterhalt
# )

# print()
# print("=== Waffen ===")
# print(
#     "Spieler-Waffe:",
#     spieler["waffe"]["typ"]
# )
# print(
#     "Gegner-Waffe:",
#     gegner["waffe"]["typ"]
# )

# print()
# print("=== Reichweite ===")
# print(
#     "Spieler-Reichweite:",
#     spieler_reichweite
# )
# print(
#     "Effektive Spieler-Reichweite:",
#     spieler_effektive_reichweite
# )
# print(
#     "Gegner-Reichweite:",
#     gegner_reichweite
# )
# print(
#     "Effektive Gegner-Reichweite:",
#     gegner_effektive_reichweite
# )
# print(
#     "Reichweitenvorteil:",
#     reichweiten_vorteil
# )

# print()
# print("=== Parade ===")
# print(
#     "Paradechance:",
#     effekte["paradechance_spieler"]
# )

# print()
# print("=== Finale Kampfeffekte ===")
# print(effekte)

# print()
# print("=== Spieler-Angriff ===")
# print("Trefferchance:", spieler_trefferchance)
# print("Angriffswurf:", angriff_wurf)
# print("Trefferart:", treffer_art)

# print()
# print("=== Schaden ===")
# print("Krit-Chance:", krit_chance)
# print("Krit-Wurf:", krit_wurf)
# print("Krit:", krit)
# print("Schaden:", schaden)

# print()
# print("=== Gegner ===")
# print("Gegner-HP:", gegner["hp"])

# print()
# print("=== Gegner-Angriff ===")
# print("Trefferchance:", gegner_trefferchance)
# print("Angriffswurf:", gegner_angriff_wurf)
# print("Trefferart:", gegner_treffer_art)

# print()
# print("=== Parade ===")
# print("Paradechance:", effekte["paradechance_spieler"])
# print("Paradewurf:", parade_wurf)
# print("Parade erfolgreich:", parade_erfolgreich)

# print()
# print("=== Gegner-Schaden ===")
# print("Schaden:", gegner_schaden)
# print("Spieler-HP:", spieler["hp"])

# print("Ursprünglicher Treffer:", gegner_treffer_art_original)
# print("Nach Parade:", gegner_treffer_art)'
