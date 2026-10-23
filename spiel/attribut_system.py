from attributdaten import (
    ATTRIBUT_DEFINITIONEN,
    VERFASSUNG_DEFINITIONEN,
    AKT1_LERNQUELLEN,
    AKT1_REISE_LERNQUELLEN
)

from status_system import (
    status_modifikator
)

from ausruestung_system import (
    ausruestungs_modifikator
)



def attribut_system_sicherstellen(
    spieler_daten
):
    if not isinstance(
        spieler_daten,
        dict
    ):
        return False

    attribute = spieler_daten.get(
        "attribute"
    )

    if not isinstance(
        attribute,
        dict
    ):
        attribute = {}

        spieler_daten[
            "attribute"
        ] = attribute

    for attribut_id, definition in (
        ATTRIBUT_DEFINITIONEN.items()
    ):
        wert = attribute.get(
            attribut_id
        )

        if (
            isinstance(wert, bool)
            or not isinstance(
                wert,
                int
            )
        ):
            attribute[
                attribut_id
            ] = definition[
                "startwert"
            ]

    fortschritt = spieler_daten.get(
        "attribut_fortschritt"
    )

    if not isinstance(
        fortschritt,
        dict
    ):
        fortschritt = {}

        spieler_daten[
            "attribut_fortschritt"
        ] = fortschritt

    for attribut_id in (
        ATTRIBUT_DEFINITIONEN
    ):
        wert = fortschritt.get(
            attribut_id
        )

        if (
            isinstance(wert, bool)
            or not isinstance(
                wert,
                (int, float)
            )
        ):
            fortschritt[
                attribut_id
            ] = 0

    verfassungen = spieler_daten.get(
        "verfassungen"
    )

    if not isinstance(
        verfassungen,
        dict
    ):
        verfassungen = {}

        spieler_daten[
            "verfassungen"
        ] = verfassungen

    praegung = spieler_daten.get(
        "verfassungs_praegung"
    )

    if not isinstance(
        praegung,
        dict
    ):
        praegung = {}

        spieler_daten[
            "verfassungs_praegung"
        ] = praegung

    for verfassung_id in (
        VERFASSUNG_DEFINITIONEN
    ):
        wert = verfassungen.get(
            verfassung_id
        )

        if (
            isinstance(wert, bool)
            or not isinstance(
                wert,
                int
            )
        ):
            verfassungen[
                verfassung_id
            ] = 0

        wert = praegung.get(
            verfassung_id
        )

        if (
            isinstance(wert, bool)
            or not isinstance(
                wert,
                (int, float)
            )
        ):
            praegung[
                verfassung_id
            ] = 0

    lernquellen = spieler_daten.get(
        "lernquellen"
    )

    if not isinstance(lernquellen, dict):
        lernquellen = {}
        spieler_daten["lernquellen"] = lernquellen

    for quelle_id, nutzungen in list(lernquellen.items()):
        if not isinstance(quelle_id, str) or not quelle_id:
            lernquellen.pop(quelle_id, None)
            continue

        if (
            isinstance(nutzungen, bool)
            or not isinstance(nutzungen, int)
            or nutzungen < 0
        ):
            lernquellen[quelle_id] = 0

    return True


def verfassung_wert_aus_praegung(
    punkte
):
    if (
        isinstance(punkte, bool)
        or not isinstance(
            punkte,
            (int, float)
        )
    ):
        return 0

    if punkte >= 18:
        return 3

    if punkte >= 10:
        return 2

    if punkte >= 4:
        return 1

    return 0


def verfassung_neuberechnen(
    spieler_daten,
    verfassung_id
):
    attribut_system_sicherstellen(
        spieler_daten
    )

    if (
        verfassung_id
        not in VERFASSUNG_DEFINITIONEN
    ):
        return False, None, None

    praegung = spieler_daten[
        "verfassungs_praegung"
    ].get(
        verfassung_id,
        0
    )

    alter_wert = spieler_daten[
        "verfassungen"
    ].get(
        verfassung_id,
        0
    )

    neuer_wert = (
        verfassung_wert_aus_praegung(
            praegung
        )
    )

    if neuer_wert == alter_wert:
        return False, alter_wert, neuer_wert

    spieler_daten[
        "verfassungen"
    ][
        verfassung_id
    ] = neuer_wert

    return True, alter_wert, neuer_wert


def attribut_schwelle(
    spieler_daten,
    attribut_id
):
    attribut_system_sicherstellen(
        spieler_daten
    )

    if attribut_id not in ATTRIBUT_DEFINITIONEN:
        return None

    aktueller_wert = spieler_daten[
        "attribute"
    ][
        attribut_id
    ]

    if (
        attribut_id == "uebersinnliches"
        and aktueller_wert == 0
    ):
        return 6

    return (
        8
        + aktueller_wert * 4
    )


def spieler_pruefwert(
    spieler_daten,
    wert_id
):
    attribut_system_sicherstellen(
        spieler_daten
    )

    basis_wert = None

    attribute = spieler_daten.get(
        "attribute",
        {}
    )

    verfassungen = spieler_daten.get(
        "verfassungen",
        {}
    )

    if wert_id in ATTRIBUT_DEFINITIONEN:
        wert = attribute.get(
            wert_id
        )

        if (
            not isinstance(wert, bool)
            and isinstance(
                wert,
                (int, float)
            )
        ):
            basis_wert = wert

    elif wert_id in VERFASSUNG_DEFINITIONEN:
        attribut_id = (
            VERFASSUNG_DEFINITIONEN[
                wert_id
            ][
                "attribut"
            ]
        )

        attribut_wert = attribute.get(
            attribut_id,
            0
        )

        verfassung_wert = (
            verfassungen.get(
                wert_id,
                0
            )
        )

        if (
            isinstance(
                attribut_wert,
                (int, float)
            )
            and not isinstance(
                attribut_wert,
                bool
            )
            and isinstance(
                verfassung_wert,
                (int, float)
            )
            and not isinstance(
                verfassung_wert,
                bool
            )
        ):
            basis_wert = (
                attribut_wert
                + verfassung_wert
            )

    if basis_wert is None:
        wert = spieler_daten.get(
            wert_id
        )

        if (
            not isinstance(wert, bool)
            and isinstance(
                wert,
                (int, float)
            )
        ):
            basis_wert = wert

    status_bonus = status_modifikator(
        spieler_daten,
        wert_id
    )
    ausruestungs_bonus = ausruestungs_modifikator(
        spieler_daten,
        wert_id
    )
    gesamt_bonus = status_bonus + ausruestungs_bonus

    if basis_wert is None:
        if gesamt_bonus != 0:
            return gesamt_bonus
        return None

    return basis_wert + gesamt_bonus




def spieler_pruefung(
    spieler_daten,
    wert_id,
    mindestwert
):
    wert = spieler_pruefwert(
        spieler_daten,
        wert_id
    )

    if (
        isinstance(wert, bool)
        or not isinstance(
            wert,
            (int, float)
        )
    ):
        return False

    if (
        isinstance(mindestwert, bool)
        or not isinstance(
            mindestwert,
            (int, float)
        )
    ):
        return False

    return wert >= mindestwert

def attribut_fortschritt_hinzufuegen(
    spieler_daten,
    attribut_id,
    menge=1,
    praegungen=None
):
    attribut_system_sicherstellen(
        spieler_daten
    )

    if attribut_id not in ATTRIBUT_DEFINITIONEN:
        return None

    if (
        isinstance(menge, bool)
        or not isinstance(
            menge,
            (int, float)
        )
        or menge <= 0
    ):
        return None

    if praegungen is None:
        praegungen = {}

    if not isinstance(
        praegungen,
        dict
    ):
        return None

    verfassungs_entwicklungen = []
    attribut_entwicklungen = []
    gepraegte_verfassungen = []

    # -------------------------
    # VERFASSUNGSPRÄGUNG
    # -------------------------

    for (
        verfassung_id,
        praegung_menge
    ) in praegungen.items():

        definition = (
            VERFASSUNG_DEFINITIONEN.get(
                verfassung_id
            )
        )

        if not definition:
            continue

        if (
            definition[
                "attribut"
            ] != attribut_id
        ):
            continue

        if (
            isinstance(
                praegung_menge,
                bool
            )
            or not isinstance(
                praegung_menge,
                (int, float)
            )
            or praegung_menge <= 0
        ):
            continue

        spieler_daten[
            "verfassungs_praegung"
        ][
            verfassung_id
        ] += praegung_menge

        gepraegte_verfassungen.append(
            verfassung_id
        )

        (
            entwickelt,
            alter_wert,
            neuer_wert
        ) = verfassung_neuberechnen(
            spieler_daten,
            verfassung_id
        )

        if entwickelt:
            verfassungs_entwicklungen.append(
                (
                    verfassung_id,
                    alter_wert,
                    neuer_wert
                )
            )

    # -------------------------
    # HAUPTATTRIBUT
    # -------------------------

    spieler_daten[
        "attribut_fortschritt"
    ][
        attribut_id
    ] += menge

    while True:
        schwelle = attribut_schwelle(
            spieler_daten,
            attribut_id
        )

        if schwelle is None:
            break

        fortschritt = spieler_daten[
            "attribut_fortschritt"
        ][
            attribut_id
        ]

        if fortschritt < schwelle:
            break

        spieler_daten[
            "attribut_fortschritt"
        ][
            attribut_id
        ] -= schwelle

        alter_wert = spieler_daten[
            "attribute"
        ][
            attribut_id
        ]

        spieler_daten[
            "attribute"
        ][
            attribut_id
        ] += 1

        neuer_wert = spieler_daten[
            "attribute"
        ][
            attribut_id
        ]

        attribut_entwicklungen.append(
            (
                attribut_id,
                alter_wert,
                neuer_wert
            )
        )

    return {
        "entwickelt": bool(
            verfassungs_entwicklungen
            or attribut_entwicklungen
        ),
        "verfassungen": verfassungs_entwicklungen,
        "attribute": attribut_entwicklungen,
        "attribut": attribut_id,
        "gepraegt": gepraegte_verfassungen
    }


def lernerfahrung_hinzufuegen(
    spieler_daten,
    quelle_id,
    attribut_id,
    menge=1,
    praegungen=None,
    max_nutzungen=1
):
    attribut_system_sicherstellen(
        spieler_daten
    )

    if (
        not isinstance(
            quelle_id,
            str
        )
        or not quelle_id
    ):
        return None

    if attribut_id not in ATTRIBUT_DEFINITIONEN:
        return None

    if (
        isinstance(menge, bool)
        or not isinstance(
            menge,
            (int, float)
        )
        or menge <= 0
    ):
        return None

    if praegungen is None:
        praegungen = {}

    if not isinstance(
        praegungen,
        dict
    ):
        return None

    if (
        isinstance(
            max_nutzungen,
            bool
        )
        or not isinstance(
            max_nutzungen,
            int
        )
        or max_nutzungen <= 0
    ):
        return None

    bisher = spieler_daten[
        "lernquellen"
    ].get(
        quelle_id,
        0
    )

    if bisher >= max_nutzungen:
        return None

    spieler_daten[
        "lernquellen"
    ][
        quelle_id
    ] = bisher + 1

    return attribut_fortschritt_hinzufuegen(
        spieler_daten,
        attribut_id,
        menge=menge,
        praegungen=praegungen
    )


def akt1_lernerfahrung(
    spieler_daten,
    quelle_id
):
    daten = AKT1_LERNQUELLEN.get(
        quelle_id
    )

    if not daten:
        return None

    return lernerfahrung_hinzufuegen(
        spieler_daten,
        "akt1_" + quelle_id,
        daten["attribut"],
        menge=daten.get(
            "menge",
            1
        ),
        praegungen=daten.get(
            "praegungen",
            {}
        ),
        max_nutzungen=daten.get(
            "max_nutzungen",
            1
        )
    )


def akt1_reise_lernerfahrung(
    spieler_daten,
    start,
    ziel
):
    quelle_id = (
        AKT1_REISE_LERNQUELLEN.get(
            frozenset(
                (start, ziel)
            )
        )
    )

    if not quelle_id:
        return None

    return akt1_lernerfahrung(
        spieler_daten,
        quelle_id
    )