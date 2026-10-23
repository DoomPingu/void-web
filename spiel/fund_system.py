from weltdaten import BESONDERE_FUNDE


def besonderer_fund_status(
    spieler_daten,
    fund_id
):
    return spieler_daten.get(
        "besondere_funde",
        {}
    ).get(
        fund_id
    )


def besonderer_fund_bekannt(
    spieler_daten,
    fund_id
):
    return besonderer_fund_status(
        spieler_daten,
        fund_id
    ) is not None


def besonderen_fund_dokumentieren(
    spieler_daten,
    fund_id,
    status="gefunden"
):
    if fund_id not in BESONDERE_FUNDE:
        return False

    funde = spieler_daten.setdefault(
        "besondere_funde",
        {}
    )

    alter_status = funde.get(
        fund_id
    )

    funde[
        fund_id
    ] = status

    return alter_status != status