import random


def dialog_thema_bekannt(
    spieler_daten,
    npc,
    thema
):
    return spieler_daten.get(
        "dialog_themen",
        {}
    ).get(
        npc,
        {}
    ).get(
        thema,
        False
    )


def dialog_option(
    spieler_daten,
    npc,
    thema,
    text
):
    if dialog_thema_bekannt(
        spieler_daten,
        npc,
        thema
    ):
        return f"{text} [Wiederholen]"

    return text


def dialog_thema_markieren(
    spieler_daten,
    npc,
    thema
):
    dialog_themen = spieler_daten.setdefault(
        "dialog_themen",
        {}
    )

    npc_themen = dialog_themen.setdefault(
        npc,
        {}
    )

    npc_themen[
        thema
    ] = True


def npc_status(
    spieler_daten,
    npc
):
    alle_npcs = spieler_daten.setdefault(
        "npc_status",
        {}
    )

    daten = alle_npcs.setdefault(
        npc,
        {
            "besuche": 0,
            "reaktionen": [],
            "themen": []
        }
    )

    return daten


def npc_besuch_starten(
    spieler_daten,
    npc
):
    daten = npc_status(
        spieler_daten,
        npc
    )

    daten[
        "besuche"
    ] += 1

    return daten[
        "besuche"
    ]


def npc_thema_bekannt(
    spieler_daten,
    npc,
    thema
):
    return thema in npc_status(
        spieler_daten,
        npc
    )["themen"]


def npc_thema_markieren(
    spieler_daten,
    npc,
    thema
):
    daten = npc_status(
        spieler_daten,
        npc
    )

    if thema not in daten["themen"]:
        daten["themen"].append(
            thema
        )


def npc_reaktion_gezeigt(
    spieler_daten,
    npc,
    reaktion
):
    return reaktion in npc_status(
        spieler_daten,
        npc
    )["reaktionen"]


def npc_reaktion_markieren(
    spieler_daten,
    npc,
    reaktion
):
    daten = npc_status(
        spieler_daten,
        npc
    )

    if reaktion not in daten["reaktionen"]:
        daten["reaktionen"].append(
            reaktion
        )


def npc_variante_waehlen(
    spieler_daten,
    npc,
    schluessel,
    varianten
):
    daten = npc_status(
        spieler_daten,
        npc
    )

    letzte_variante = daten.get(
        schluessel
    )

    moegliche_varianten = [
        variante
        for variante in varianten
        if variante != letzte_variante
    ]

    if not moegliche_varianten:
        moegliche_varianten = varianten

    variante = random.choice(
        moegliche_varianten
    )

    daten[
        schluessel
    ] = variante

    return variante


def npc_begruessung_waehlen(
    spieler_daten,
    npc,
    begruessungen
):
    daten = npc_status(
        spieler_daten,
        npc
    )

    letzte_begruessung = daten.get(
        "letzte_begruessung"
    )

    moegliche_begruessungen = [
        begruessung
        for begruessung in begruessungen
        if begruessung != letzte_begruessung
    ]

    if not moegliche_begruessungen:
        moegliche_begruessungen = begruessungen

    begruessung = random.choice(
        moegliche_begruessungen
    )

    daten[
        "letzte_begruessung"
    ] = begruessung

    return begruessung