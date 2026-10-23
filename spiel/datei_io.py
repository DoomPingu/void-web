import json
import os
import time

def json_lesen(
    dateipfad
):
    try:
        with open(
            dateipfad,
            "r",
            encoding="utf-8"
        ) as datei:
            daten = json.load(datei)

    except (
        OSError,
        json.JSONDecodeError
    ) as fehler:
        return False, fehler

    return True, daten

def datei_backup_erstellen(
    dateipfad,
    version
):
    zeitstempel = time.strftime(
        "%Y%m%d-%H%M%S"
    )

    basis, _endung = os.path.splitext(
        dateipfad
    )

    backup_datei = (
        f"{basis}_backup_v"
        f"{version}_"
        f"{zeitstempel}.json"
    )

    nummer = 2

    while os.path.exists(
        backup_datei
    ):
        backup_datei = (
            f"{basis}_backup_v"
            f"{version}_"
            f"{zeitstempel}_"
            f"{nummer}.json"
        )

        nummer += 1

    try:
        with open(
            dateipfad,
            "rb"
        ) as quelle:
            inhalt = quelle.read()

        with open(
            backup_datei,
            "xb"
        ) as ziel:
            ziel.write(
                inhalt
            )

    except OSError as fehler:
        return None, fehler

    return backup_datei, None

def json_sicher_schreiben(
    dateipfad,
    daten
):
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
    ) as fehler:

        if os.path.exists(
            temp_datei
        ):
            try:
                os.remove(
                    temp_datei
                )
            except OSError:
                pass

        return False, fehler

    return True, None