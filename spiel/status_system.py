from spieldaten import STATUS_EFFEKTE


def status_effekte_aktiv(
    spieler_daten
):
    return spieler_daten.setdefault(
        "status_effekte",
        {}
    )


def status_aktiv(
    spieler_daten,
    status_id
):
    return status_id in status_effekte_aktiv(
        spieler_daten
    )


def status_hinzufuegen(
    spieler_daten,
    status_id,
    dauer=None,
    einheit=None,
    stapel=1,
    quelle=None
):
    definition = STATUS_EFFEKTE.get(
        status_id
    )

    if not definition:
        return False

    if dauer is None:
        dauer = definition.get(
            "standard_dauer"
        )

    if einheit is None:
        einheit = definition.get(
            "standard_einheit"
        )

    if (
        dauer is not None
        and (
            isinstance(dauer, bool)
            or not isinstance(
                dauer,
                (int, float)
            )
            or dauer <= 0
        )
    ):
        return False

    if (
        isinstance(stapel, bool)
        or not isinstance(stapel, int)
        or stapel <= 0
    ):
        return False

    aktive = status_effekte_aktiv(
        spieler_daten
    )

    vorhanden = aktive.get(
        status_id
    )

    if vorhanden:
        if definition.get(
            "stapelbar",
            False
        ):
            max_stapel = definition.get(
                "max_stapel",
                1
            )

            vorhanden["stapel"] = min(
                max_stapel,
                vorhanden.get(
                    "stapel",
                    1
                ) + stapel
            )

        if dauer is not None:
            if (
                vorhanden.get(
                    "einheit"
                ) == einheit
                and isinstance(
                    vorhanden.get(
                        "dauer"
                    ),
                    (int, float)
                )
            ):
                vorhanden["dauer"] = max(
                    vorhanden["dauer"],
                    dauer
                )

            else:
                vorhanden[
                    "dauer"
                ] = dauer

                vorhanden[
                    "einheit"
                ] = einheit

        if quelle is not None:
            vorhanden[
                "quelle"
            ] = quelle

    else:
        aktive[status_id] = {
            "dauer": dauer,
            "einheit": einheit,
            "stapel": min(
                stapel,
                definition.get(
                    "max_stapel",
                    stapel
                )
                if definition.get(
                    "stapelbar",
                    False
                )
                else 1
            ),
            "quelle": quelle
        }

    return True


def status_entfernen(
    spieler_daten,
    status_id
):
    aktive = status_effekte_aktiv(
        spieler_daten
    )

    if status_id not in aktive:
        return False

    aktive.pop(
        status_id,
        None
    )

    return True


def status_modifikator(
    spieler_daten,
    wert_id
):
    gesamt = 0

    for status_id, aktiv_daten in (
        status_effekte_aktiv(
            spieler_daten
        ).items()
    ):
        definition = STATUS_EFFEKTE.get(
            status_id,
            {}
        )

        modifikator = definition.get(
            "modifikatoren",
            {}
        ).get(
            wert_id,
            0
        )

        if not isinstance(
            modifikator,
            (int, float)
        ):
            continue

        stapel = max(
            1,
            aktiv_daten.get(
                "stapel",
                1
            )
        )

        gesamt += (
            modifikator * stapel
        )

    return gesamt


def status_dauer_verringern(
    spieler_daten,
    einheit,
    menge=1
):
    if (
        isinstance(menge, bool)
        or not isinstance(
            menge,
            (int, float)
        )
        or menge <= 0
    ):
        return []

    aktive = status_effekte_aktiv(
        spieler_daten
    )

    beendet = []

    for status_id, aktiv_daten in list(
        aktive.items()
    ):
        if aktiv_daten.get(
            "einheit"
        ) != einheit:
            continue

        dauer = aktiv_daten.get(
            "dauer"
        )

        if not isinstance(
            dauer,
            (int, float)
        ):
            continue

        aktiv_daten[
            "dauer"
        ] = dauer - menge

        if aktiv_daten[
            "dauer"
        ] <= 0:
            beendet.append(
                status_id
            )

    for status_id in beendet:
        aktive.pop(
            status_id,
            None
        )

    return beendet


def status_kampf_vorbereiten(
    spieler_daten
):
    for status_id, aktiv_daten in (
        status_effekte_aktiv(
            spieler_daten
        ).items()
    ):
        definition = STATUS_EFFEKTE.get(
            status_id,
            {}
        )

        kampf_einheit = definition.get(
            "kampf_einheit"
        )

        nach_kampf_einheit = definition.get(
            "nach_kampf_einheit"
        )

        if (
            kampf_einheit
            and nach_kampf_einheit
            and aktiv_daten.get(
                "einheit"
            ) == nach_kampf_einheit
        ):
            aktiv_daten[
                "einheit"
            ] = kampf_einheit


def status_nach_kampf_verarbeiten(
    spieler_daten
):
    for status_id, aktiv_daten in (
        status_effekte_aktiv(
            spieler_daten
        ).items()
    ):
        definition = STATUS_EFFEKTE.get(
            status_id,
            {}
        )

        nach_kampf_einheit = definition.get(
            "nach_kampf_einheit"
        )

        if (
            nach_kampf_einheit
            and aktiv_daten.get(
                "einheit"
            ) == "runden"
        ):
            aktiv_daten[
                "einheit"
            ] = nach_kampf_einheit