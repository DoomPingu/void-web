from weltdaten import WEGE


def weg_status(
    spieler_daten,
    weg_id
):
    return spieler_daten.get(
        "wege_status",
        {}
    ).get(
        weg_id,
        "unbekannt"
    )


def weg_bemerken(
    spieler_daten,
    weg_id
):
    wege_status = spieler_daten.setdefault(
        "wege_status",
        {}
    )

    if wege_status.get(
        weg_id,
        "unbekannt"
    ) == "unbekannt":
        wege_status[
            weg_id
        ] = "bemerkt"


def weg_entdecken(
    spieler_daten,
    weg_id
):
    if weg_id not in WEGE:
        return False, False

    wege_status = spieler_daten.setdefault(
        "wege_status",
        {}
    )

    war_bereits_entdeckt = (
        wege_status.get(
            weg_id
        )
        == "entdeckt"
    )

    wege_status[
        weg_id
    ] = "entdeckt"

    neu_entdeckt = (
        not war_bereits_entdeckt
    )

    if neu_entdeckt:
        neue_wege = spieler_daten.setdefault(
            "neue_wege",
            []
        )

        if weg_id not in neue_wege:
            neue_wege.append(
                weg_id
            )

    return True, neu_entdeckt


def weg_ist_neu(
    spieler_daten,
    weg_id
):
    return weg_id in spieler_daten.get(
        "neue_wege",
        []
    )


def weg_als_gesehen_markieren(
    spieler_daten,
    weg_id
):
    neue_wege = spieler_daten.setdefault(
        "neue_wege",
        []
    )

    if weg_id in neue_wege:
        neue_wege.remove(
            weg_id
        )


def routenkenntnis_bekannt(
    spieler_daten,
    weg_id
):
    return weg_id in spieler_daten.get(
        "routenkenntnis",
        []
    )


def routenkenntnis_lernen(
    spieler_daten,
    weg_id
):
    if weg_id not in WEGE:
        return False

    bekannte_routen = spieler_daten.setdefault(
        "routenkenntnis",
        []
    )

    if weg_id in bekannte_routen:
        return False

    bekannte_routen.append(
        weg_id
    )

    return True