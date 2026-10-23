from weltdaten import RUECKKEHR_HINWEISE


def hinweis_status(
    spieler_daten,
    hinweis_id
):
    if not isinstance(
        spieler_daten,
        dict
    ):
        return None

    return spieler_daten.get(
        "rueckkehr_hinweise",
        {}
    ).get(
        hinweis_id
    )


def hinweis_offen(
    spieler_daten,
    hinweis_id
):
    return hinweis_status(
        spieler_daten,
        hinweis_id
    ) in (
        "neu",
        "offen"
    )


def hinweis_aktivieren(
    spieler_daten,
    hinweis_id
):
    if not isinstance(
        spieler_daten,
        dict
    ):
        return False

    if hinweis_id not in RUECKKEHR_HINWEISE:
        return False

    hinweise = spieler_daten.setdefault(
        "rueckkehr_hinweise",
        {}
    )

    if hinweise.get(
        hinweis_id
    ) in (
        "neu",
        "offen",
        "erledigt"
    ):
        return False

    hinweise[
        hinweis_id
    ] = "neu"

    return True


def hinweis_erledigen(
    spieler_daten,
    hinweis_id
):
    if not isinstance(
        spieler_daten,
        dict
    ):
        return False

    hinweise = spieler_daten.setdefault(
        "rueckkehr_hinweise",
        {}
    )

    if hinweis_id not in hinweise:
        return False

    hinweise[
        hinweis_id
    ] = "erledigt"

    return True


def offene_hinweise_vorhanden(
    spieler_daten
):
    if not isinstance(
        spieler_daten,
        dict
    ):
        return False

    return any(
        status in (
            "neu",
            "offen"
        )
        for status in spieler_daten.get(
            "rueckkehr_hinweise",
            {}
        ).values()
    )