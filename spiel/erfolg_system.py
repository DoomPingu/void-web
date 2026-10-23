from spieldaten import ERFOLGE


def erfolg_ist_freigeschaltet(
    spieler_daten,
    erfolg_id
):
    return erfolg_id in spieler_daten.get(
        "erfolge_freigeschaltet",
        []
    )


def erfolg_freischalten(
    spieler_daten,
    erfolg_id
):
    if erfolg_id not in ERFOLGE:
        return False

    erfolge = spieler_daten.setdefault(
        "erfolge_freigeschaltet",
        []
    )

    if erfolg_id in erfolge:
        return False

    erfolge.append(
        erfolg_id
    )

    return True