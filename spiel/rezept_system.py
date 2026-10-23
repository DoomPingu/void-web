from spieldaten import REZEPTE
from inventar_system import item_anzahl as inventar_item_anzahl


def rezept_ist_gelernt(
    spieler_daten,
    rezept_id
):
    return rezept_id in spieler_daten.get(
        "rezepte_gelernt",
        []
    )


def rezept_lernen(
    spieler_daten,
    rezept_id
):
    if rezept_id not in REZEPTE:
        return False

    gelernte_rezepte = spieler_daten.setdefault(
        "rezepte_gelernt",
        []
    )

    if rezept_id in gelernte_rezepte:
        return False

    gelernte_rezepte.append(
        rezept_id
    )

    return True


def rezept_fehlende_zutaten(
    spieler_daten,
    rezept
):
    fehlende_zutaten = []

    for item_id, anzahl in rezept[
        "zutaten"
    ].items():

        vorhanden = inventar_item_anzahl(
            spieler_daten,
            item_id
        )

        if vorhanden < anzahl:
            fehlende_zutaten.append(
                (
                    item_id,
                    anzahl - vorhanden
                )
            )

    return fehlende_zutaten


def rezept_kann_gekocht_werden(
    spieler_daten,
    rezept
):
    return not rezept_fehlende_zutaten(
        spieler_daten,
        rezept
    )