from spieldaten import RESSOURCEN_VORKOMMEN


def vorkommen_status(
    spieler_daten,
    vorkommen_id
):
    if vorkommen_id not in RESSOURCEN_VORKOMMEN:
        return None

    alle_vorkommen = spieler_daten.setdefault(
        "ressourcen_vorkommen",
        {}
    )

    status = alle_vorkommen.setdefault(
        vorkommen_id,
        {}
    )

    daten = RESSOURCEN_VORKOMMEN[
        vorkommen_id
    ]

    status.setdefault(
        "vorrat",
        daten["maximum"]
    )

    status.setdefault(
        "regeneration",
        0
    )

    return status


def vorkommen_regenerieren(
    spieler_daten,
    vorkommen_id,
    schritte=1
):
    status = vorkommen_status(
        spieler_daten,
        vorkommen_id
    )

    if status is None:
        return 0

    daten = RESSOURCEN_VORKOMMEN[
        vorkommen_id
    ]

    maximum = daten[
        "maximum"
    ]

    if status["vorrat"] >= maximum:
        status["vorrat"] = maximum
        status["regeneration"] = 0
        return 0

    status["regeneration"] += schritte

    regeneriert = 0

    while (
        status["regeneration"]
        >= daten["regeneration_schritte"]
        and status["vorrat"] < maximum
    ):
        status["regeneration"] -= (
            daten["regeneration_schritte"]
        )

        status["vorrat"] += 1
        regeneriert += 1

    if status["vorrat"] >= maximum:
        status["vorrat"] = maximum
        status["regeneration"] = 0

    return regeneriert