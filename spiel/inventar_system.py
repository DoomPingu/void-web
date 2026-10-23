from spieldaten import ITEMS


def _gueltige_menge(anzahl):
    return (
        isinstance(anzahl, int)
        and not isinstance(anzahl, bool)
        and anzahl > 0
    )


def item_anzahl(spieler_daten, item_id):
    return spieler_daten.get(
        "inventar_items",
        {}
    ).get(item_id, 0)


def item_besitzt(spieler_daten, item_id, anzahl=1):
    if not _gueltige_menge(anzahl):
        return False

    return item_anzahl(spieler_daten, item_id) >= anzahl


def item_hinzufuegen(spieler_daten, item_id, anzahl=1):
    if not _gueltige_menge(anzahl):
        return False

    if item_id not in ITEMS:
        return False

    inventar_items = spieler_daten.setdefault(
        "inventar_items",
        {}
    )

    inventar_items[item_id] = (
        inventar_items.get(item_id, 0) + anzahl
    )

    return True


def item_entfernen(spieler_daten, item_id, anzahl=1):
    if not _gueltige_menge(anzahl):
        return False

    inventar_items = spieler_daten.get(
        "inventar_items",
        {}
    )

    vorhandene_anzahl = inventar_items.get(item_id, 0)

    if vorhandene_anzahl < anzahl:
        return False

    neue_anzahl = vorhandene_anzahl - anzahl

    if neue_anzahl == 0:
        inventar_items.pop(item_id, None)
    else:
        inventar_items[item_id] = neue_anzahl

    return True