import json
import os


def einstellungen_laden_aus_datei(
    dateipfad,
    standard_einstellungen,
    text_faktoren
):
    if not os.path.exists(dateipfad):
        return False

    try:
        with open(
            dateipfad,
            "r",
            encoding="utf-8"
        ) as datei:
            daten = json.load(datei)

        if not isinstance(daten, dict):
            return False

    except (
        OSError,
        json.JSONDecodeError
    ):
        return False

    textgeschwindigkeit = daten.get(
        "textgeschwindigkeit"
    )

    if textgeschwindigkeit in text_faktoren:
        standard_einstellungen[
            "textgeschwindigkeit"
        ] = textgeschwindigkeit

    menue_eingabe = daten.get(
        "menue_eingabe"
    )

    if menue_eingabe in (
        "enter",
        "direkt"
    ):
        standard_einstellungen[
            "menue_eingabe"
        ] = menue_eingabe

    bildschirm_leeren = daten.get(
        "bildschirm_leeren"
    )

    if isinstance(
        bildschirm_leeren,
        bool
    ):
        standard_einstellungen[
            "bildschirm_leeren"
        ] = bildschirm_leeren

    spieler_name_farbe = daten.get(
        "spieler_name_farbe"
    )

    if spieler_name_farbe in (
        "standard",
        "blau",
        "cyan",
        "gruen",
        "gelb",
        "lila",
        "rot",
        "schwarz"
    ):
        standard_einstellungen[
            "spieler_name_farbe"
        ] = spieler_name_farbe

    dialog_stimmung = daten.get(
        "dialog_stimmung"
    )

    if isinstance(
        dialog_stimmung,
        bool
    ):
        standard_einstellungen[
            "dialog_stimmung"
        ] = dialog_stimmung

    return True


def einstellungen_speichern_in_datei(
    dateipfad,
    einstellungen,
    standard_einstellungen
):
    daten = {
        "textgeschwindigkeit": einstellungen.get(
            "textgeschwindigkeit",
            standard_einstellungen[
                "textgeschwindigkeit"
            ]
        ),

        "menue_eingabe": einstellungen.get(
            "menue_eingabe",
            standard_einstellungen[
                "menue_eingabe"
            ]
        ),

        "bildschirm_leeren": einstellungen.get(
            "bildschirm_leeren",
            standard_einstellungen[
                "bildschirm_leeren"
            ]
        ),

        "spieler_name_farbe": einstellungen.get(
            "spieler_name_farbe",
            standard_einstellungen[
                "spieler_name_farbe"
            ]
        ),

        "dialog_stimmung": einstellungen.get(
            "dialog_stimmung",
            standard_einstellungen[
                "dialog_stimmung"
            ]
        )
    }

    temp_datei = dateipfad + ".tmp"

    try:
        with open(
            temp_datei,
            "w",
            encoding="utf-8"
        ) as datei:
            json.dump(
                daten,
                datei,
                ensure_ascii=False,
                indent=4
            )

        os.replace(
            temp_datei,
            dateipfad
        )

    except (
        OSError,
        TypeError,
        ValueError
    ):
        if os.path.exists(temp_datei):
            try:
                os.remove(temp_datei)
            except OSError:
                pass

        return False

    return True