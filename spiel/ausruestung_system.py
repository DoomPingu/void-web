from ausruestungsdaten import (
    AUSRUESTUNGS_GEGENSTAENDE
)


AUSRUESTUNGS_SLOTS = (
    "waffe",
    "ruestung",
    "zubehoer",
    "werkzeug"
)

def ausruestungs_modifikator(spieler_daten, wert_id):
    if not isinstance(spieler_daten, dict):
        return 0

    ausruestung = spieler_daten.get("ausruestung", {})
    if not isinstance(ausruestung, dict):
        return 0

    bonus = 0
    for slot in ("ruestung", "zubehoer", "werkzeug"):
        gegenstand = ausruestung.get(slot)
        if not isinstance(gegenstand, dict):
            continue

        gegenstand_id = gegenstand.get("id")
        if not isinstance(gegenstand_id, str):
            continue

        daten = AUSRUESTUNGS_GEGENSTAENDE.get(gegenstand_id)
        if not isinstance(daten, dict) or daten.get("slot") != slot:
            continue

        boni = daten.get("pruefwert_boni", {})
        if not isinstance(boni, dict):
            continue

        wert = boni.get(wert_id, 0)
        if isinstance(wert, int) and not isinstance(wert, bool):
            bonus += wert

    return bonus



def ausruestung_sicherstellen(
    spieler_daten
):
    if not isinstance(
        spieler_daten,
        dict
    ):
        return False

    ausruestung = spieler_daten.get(
        "ausruestung"
    )

    if not isinstance(
        ausruestung,
        dict
    ):
        ausruestung = {}

        spieler_daten[
            "ausruestung"
        ] = ausruestung

    for slot in AUSRUESTUNGS_SLOTS:
        ausruestung.setdefault(
            slot,
            None
        )

    ausruestungs_inventar = spieler_daten.get(
        "ausruestungs_inventar"
    )

    if not isinstance(
        ausruestungs_inventar,
        list
    ):
        spieler_daten[
            "ausruestungs_inventar"
        ] = []

    # -------------------------
    # ALTES WAFFENSYSTEM
    # -------------------------
    #
    # Solange Combat und ältere Funktionen noch
    # spieler["waffe"] verwenden, bleibt dieser
    # Wert mit dem neuen Waffen-Slot synchron.
    # -------------------------

    if "waffe" in spieler_daten:
        ausruestung[
            "waffe"
        ] = spieler_daten.get(
            "waffe"
        )

    else:
        spieler_daten[
            "waffe"
        ] = ausruestung.get(
            "waffe"
        )

    return True


def ausruestung_holen(
    spieler_daten,
    slot
):
    if slot not in AUSRUESTUNGS_SLOTS:
        return None

    if not ausruestung_sicherstellen(
        spieler_daten
    ):
        return None

    return spieler_daten[
        "ausruestung"
    ].get(
        slot
    )


def ausgeruestet(
    spieler_daten,
    slot
):
    return ausruestung_holen(
        spieler_daten,
        slot
    ) is not None


def ausruestung_setzen(
    spieler_daten,
    slot,
    gegenstand
):
    if slot not in AUSRUESTUNGS_SLOTS:
        return False

    if not ausruestung_sicherstellen(
        spieler_daten
    ):
        return False

    spieler_daten[
        "ausruestung"
    ][
        slot
    ] = gegenstand

    # Vorläufige Kompatibilität
    # mit dem bisherigen Kampfsystem.
    if slot == "waffe":
        spieler_daten[
            "waffe"
        ] = gegenstand

    return True


def ausruestung_ablegen(
    spieler_daten,
    slot
):
    if slot not in AUSRUESTUNGS_SLOTS:
        return None

    alter_gegenstand = ausruestung_holen(
        spieler_daten,
        slot
    )

    if alter_gegenstand is None:
        return None

    ausruestung_setzen(
        spieler_daten,
        slot,
        None
    )

    return alter_gegenstand


def waffe_aus_inventar_ausruesten(
    spieler_daten,
    index
):
    if not ausruestung_sicherstellen(
        spieler_daten
    ):
        return False, None, None

    inventar = spieler_daten.setdefault(
        "waffen_inventar",
        []
    )

    if (
        isinstance(index, bool)
        or not isinstance(index, int)
        or index < 0
        or index >= len(inventar)
    ):
        return False, None, None

    neue_waffe = inventar.pop(
        index
    )

    alte_waffe = ausruestung_holen(
        spieler_daten,
        "waffe"
    )

    ausruestung_setzen(
        spieler_daten,
        "waffe",
        neue_waffe
    )

    if alte_waffe is not None:
        inventar.append(
            alte_waffe
        )

    return (
        True,
        neue_waffe,
        alte_waffe
    )

def ausruestungsgegenstand_erstellen(
    gegenstand_id
):
    daten = AUSRUESTUNGS_GEGENSTAENDE.get(
        gegenstand_id
    )

    if not isinstance(
        daten,
        dict
    ):
        return None

    gegenstand = {
        "id": gegenstand_id
    }

    gegenstand.update(
        daten
    )

    return gegenstand


def ausruestungsgegenstand_besitzt(
    spieler_daten,
    gegenstand_id
):
    if not ausruestung_sicherstellen(
        spieler_daten
    ):
        return False

    for gegenstand in spieler_daten[
        "ausruestungs_inventar"
    ]:
        if (
            isinstance(
                gegenstand,
                dict
            )
            and gegenstand.get(
                "id"
            ) == gegenstand_id
        ):
            return True

    for slot in (
        "ruestung",
        "zubehoer",
        "werkzeug"
    ):
        gegenstand = spieler_daten[
            "ausruestung"
        ].get(
            slot
        )

        if (
            isinstance(
                gegenstand,
                dict
            )
            and gegenstand.get(
                "id"
            ) == gegenstand_id
        ):
            return True

    return False


def ausruestungsgegenstand_hinzufuegen(
    spieler_daten,
    gegenstand_id
):
    if not ausruestung_sicherstellen(
        spieler_daten
    ):
        return False

    gegenstand = (
        ausruestungsgegenstand_erstellen(
            gegenstand_id
        )
    )

    if gegenstand is None:
        return False

    if gegenstand.get(
        "slot"
    ) not in (
        "ruestung",
        "zubehoer",
        "werkzeug"
    ):
        return False

    spieler_daten[
        "ausruestungs_inventar"
    ].append(
        gegenstand
    )

    return True


def ausruestungsinventar_fuer_slot(
    spieler_daten,
    slot
):
    if slot not in (
        "ruestung",
        "zubehoer",
        "werkzeug"
    ):
        return []

    if not ausruestung_sicherstellen(
        spieler_daten
    ):
        return []

    ergebnis = []

    for index, gegenstand in enumerate(
        spieler_daten[
            "ausruestungs_inventar"
        ]
    ):
        if not isinstance(
            gegenstand,
            dict
        ):
            continue

        if gegenstand.get(
            "slot"
        ) != slot:
            continue

        ergebnis.append(
            (
                index,
                gegenstand
            )
        )

    return ergebnis


def ausruestungsgegenstand_ausruesten(
    spieler_daten,
    inventar_index
):
    if not ausruestung_sicherstellen(
        spieler_daten
    ):
        return False, None, None

    inventar = spieler_daten[
        "ausruestungs_inventar"
    ]

    if (
        isinstance(
            inventar_index,
            bool
        )
        or not isinstance(
            inventar_index,
            int
        )
        or inventar_index < 0
        or inventar_index >= len(
            inventar
        )
    ):
        return False, None, None

    neuer_gegenstand = inventar[
        inventar_index
    ]

    if not isinstance(
        neuer_gegenstand,
        dict
    ):
        return False, None, None

    slot = neuer_gegenstand.get(
        "slot"
    )

    if slot not in (
        "ruestung",
        "zubehoer",
        "werkzeug"
    ):
        return False, None, None

    neuer_gegenstand = inventar.pop(
        inventar_index
    )

    alter_gegenstand = ausruestung_holen(
        spieler_daten,
        slot
    )

    ausruestung_setzen(
        spieler_daten,
        slot,
        neuer_gegenstand
    )

    if alter_gegenstand is not None:
        inventar.append(
            alter_gegenstand
        )

    return (
        True,
        neuer_gegenstand,
        alter_gegenstand
    )


def ausruestung_in_inventar_ablegen(
    spieler_daten,
    slot
):
    if slot not in (
        "ruestung",
        "zubehoer",
        "werkzeug"
    ):
        return False, None

    gegenstand = ausruestung_ablegen(
        spieler_daten,
        slot
    )

    if gegenstand is None:
        return False, None

    spieler_daten[
        "ausruestungs_inventar"
    ].append(
        gegenstand
    )

    return True, gegenstand