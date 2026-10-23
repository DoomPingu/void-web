LEVEL_KOSTEN = (100, 180, 300, 470, 700, 1000)

# Erste EXP-Testwerte; Belohnungen je Ziel einmalig.
EXP_QUELLEN = {
    "oros_listen_abschluss": {
        "name": "Ein Name auf der Liste",
        "exp": 120,
        "limit": 1,
        "bedingung": ("quest_oros_listen", "abgeschlossen")
    },
    "prolog_abschluss": {
        "name": "Prolog abgeschlossen",
        "exp": 60,
        "limit": 1,
        "bedingung": ("prolog_status", "prolog_abgeschlossen")
    },
    "hilda_lieferung": {
        "name": "Die verschwundene Lieferung",
        "exp": 60,
        "limit": 1,
        "bedingung": ("quest_hilda", "abgeschlossen")
    },
    "marek_abschluss": {
        "name": "Ein Name fehlt",
        "exp": 120,
        "limit": 1,
        "bedingung": ("quest_ein_name_fehlt", "abgeschlossen")
    },
    "wiegenlied_abschluss": {
        "name": "Das stumme Wiegenlied",
        "exp": 100,
        "limit": 1,
        "bedingung": ("quest_wiegenlied", "abgeschlossen")
    },
    "fund_alte_wegmarke": {
        "name": "Alte Wegmarke entdeckt",
        "exp": 25,
        "limit": 1,
        "bedingung": (
            ("wald_erforschung", "funde", "alte_wegmarke_gefunden"),
            True
        )
    },
    "fund_altes_kartenstueck": {
        "name": "Altes Kartenstück entdeckt",
        "exp": 25,
        "limit": 1,
        "bedingung": (
            ("wald_erforschung", "funde", "altes_kartenstueck_erhalten"),
            True
        )
    },
    "faden_abschluss": {
        "name": "Faden der Erinnerung",
        "exp": 40,
        "limit": 1,
        "bedingung": ("quest_oros", "abgeschlossen")
    },
    "oros_tiefen_abschluss": {
        "name": "Was Oros vergessen hat",
        "exp": 150,
        "limit": 1,
        "bedingung": ("quest_oros_tiefen", "abgeschlossen")
    },
    "schmied_abschluss": {
        "name": "Der Schmied des Weges",
        "exp": 100,
        "limit": 1,
        "bedingung": ("quest_schmied", "abgeschlossen")
    },
    "waldwaechter_sieg": {
        "name": "Der Waldwächter",
        "exp": 100,
        "limit": 1,
        "bedingung": ("waldwaechter_besiegt", True)
    },
    "revierherr_graupelz": {
        "name": "Revierherr: Graupelz",
        "exp": 30,
        "limit": 1,
        "bedingung": (("jagdbuch", "Graupelz", "beute"), True)
    },
    "revierherr_aschenkoenig": {
        "name": "Revierherr: Aschenkönig",
        "exp": 30,
        "limit": 1,
        "bedingung": (("jagdbuch", "Aschenkönig", "beute"), True)
    },
    "revierherr_steinvater": {
        "name": "Revierherr: Steinvater",
        "exp": 30,
        "limit": 1,
        "bedingung": (("jagdbuch", "Steinvater", "beute"), True)
    },
    "revierherr_einscherer": {
        "name": "Revierherr: Einscherer",
        "exp": 30,
        "limit": 1,
        "bedingung": (("jagdbuch", "Einscherer", "beute"), True)
    },
    "revierherr_blasser_hirsch": {
        "name": "Revierherr: Blasser Hirsch",
        "exp": 30,
        "limit": 1,
        "bedingung": (("jagdbuch", "Blasser Hirsch", "beute"), True)
    },
    "wege_versunkene_steine": {
        "name": "Die versunkenen Steine",
        "exp": 60,
        "limit": 1,
        "bedingung": ("wege_versunkene_steine_untersucht", True)
    },
    "wege_pfad_randsteine": {
        "name": "Die Randsteine am Pfad",
        "exp": 60,
        "limit": 1,
        "bedingung": ("wege_pfad_randsteine_untersucht", True)
    },
    "wege_abschluss": {
        "name": "Was die Wege verbindet",
        "exp": 100,
        "limit": 1,
        "bedingung": ("quest_wege_verbinden", "abgeschlossen")
    },
    "stelle_fundamentstein": {
        "name": "Der Stein im Signalturm",
        "exp": 60,
        "limit": 1,
        "bedingung": ("stelle_fundamentstein_gesehen", True)
    },
    "stelle_abschluss": {
        "name": "Was an seine Stelle trat",
        "exp": 100,
        "limit": 1,
        "bedingung": ("quest_was_an_seine_stelle_trat", "abgeschlossen")
    },
    "koehlerpfad_entdeckt": {
        "name": "Alter Köhlerpfad entdeckt",
        "exp": 25,
        "limit": 1,
        "bedingung": ("koehlerpfad_betreten", True)
    },
    "schutz_abschluss": {
        "name": "Die Antwort der Schutzverwaltung",
        "exp": 100,
        "limit": 1,
        "bedingung": ("quest_schutzverwaltung", "abgeschlossen")
    },
    "tiefen_messgang": {
        "name": "Der Messgang",
        "exp": 60,
        "limit": 1,
        "bedingung": (("tiefen", "messgang_entdeckt"), True)
    },
    "tiefen_kammer": {
        "name": "Die Kammer der Reihe",
        "exp": 60,
        "limit": 1,
        "bedingung": (("tiefen", "kammer_entdeckt"), True)
    },
    "tiefen_iv_c_abschluss": {
        "name": "Unter der Mauer",
        "exp": 150,
        "limit": 1,
        "bedingung": ("quest_unter_der_mauer", "abgeschlossen")
    },
    "wegstation_messung1": {
        "name": "Die erste Messung",
        "exp": 40,
        "limit": 1,
        "bedingung": (("wegstation_messung", "messung1"), True)
    },
    "wegstation_messung2": {
        "name": "Die zweite Messung",
        "exp": 40,
        "limit": 1,
        "bedingung": (("wegstation_messung", "messung2"), True)
    },
    "wegstation_auswertung": {
        "name": "Valeries Auswertung",
        "exp": 30,
        "limit": 1,
        "bedingung": (("wegstation_messung", "auswertung"), True)
    },
    "wegstation_abschluss": {
        "name": "Die Wegstation",
        "exp": 80,
        "limit": 1,
        "bedingung": ("quest_wegstation", "abgeschlossen")
    },
    "abtrennung_rahmen": {
        "name": "Der Sicherungsrahmen",
        "exp": 60,
        "limit": 1,
        "bedingung": (("abtrennung", "rahmen"), True)
    },
    "abtrennung_ruecknahme": {
        "name": "Die Rücknahme",
        "exp": 40,
        "limit": 1,
        "bedingung": (("abtrennung", "ruecknahme"), True)
    },
    "abtrennung_halten": {
        "name": "Die Verbindung im Messgang",
        "exp": 60,
        "limit": 1,
        "bedingung": (("abtrennung", "halten"), True)
    },
    "akt1_ende": {
        "name": "Ende von Akt 1",
        "exp": 150,
        "limit": 1,
        "bedingung": ("quest_letzte_abtrennung", "abgeschlossen")
    },
    "tore_vermessung": {
        "name": "Die Neuvermessung",
        "exp": 60,
        "limit": 1,
        "bedingung": (("kapitel6", "weg_eichenruh_vermessen"), True)
    },
    "tore_aufnahme": {
        "name": "Die offenen Tore",
        "exp": 100,
        "limit": 1,
        "bedingung": ("quest_offene_tore", "abgeschlossen")
    },
    "caelen_spur": {
        "name": "Die Hütte am Waldrand",
        "exp": 60,
        "limit": 1,
        "bedingung": ("quest_caelen", "abgeschlossen")
    },
    "kehre_weg": {
        "name": "Der Weg zur Kehre",
        "exp": 80,
        "limit": 1,
        "bedingung": (("kapitel6", "kehre_weg"), True)
    },
    "kehre_felsweg": {
        "name": "Der Felsweg",
        "exp": 70,
        "limit": 1,
        "bedingung": (("kapitel6", "kehre_felsweg"), True)
    },
    "kehre_erreicht": {
        "name": "Die Eingeschlossenen",
        "exp": 100,
        "limit": 1,
        "bedingung": (("kapitel6", "kehre_erreicht"), True)
    },
    "kehre_abschluss": {
        "name": "Die Zurückgelassenen",
        "exp": 150,
        "limit": 1,
        "bedingung": ("quest_zurueckgelassene", "abgeschlossen")
    }
}


def _natuerliche_zahl(wert):
    return (
        isinstance(wert, int)
        and not isinstance(wert, bool)
        and wert >= 0
    )


def level_system_sicherstellen(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return False

    daten = spieler_daten.get("entwicklung")

    if not isinstance(daten, dict):
        daten = {}
        spieler_daten["entwicklung"] = daten

    if not _natuerliche_zahl(daten.get("gesamt_exp")):
        daten["gesamt_exp"] = 0

    quellen = daten.get("exp_quellen")

    if not isinstance(quellen, dict):
        quellen = {}
        daten["exp_quellen"] = quellen

    for quelle_id, anzahl in list(quellen.items()):
        if (
            not isinstance(quelle_id, str)
            or not _natuerliche_zahl(anzahl)
        ):
            quellen.pop(quelle_id, None)

    return True


def level_fuer_exp(gesamt_exp):
    if not _natuerliche_zahl(gesamt_exp):
        gesamt_exp = 0

    schwelle = 0

    for level, kosten in enumerate(LEVEL_KOSTEN, start=1):
        schwelle += kosten

        if gesamt_exp < schwelle:
            return level

    return len(LEVEL_KOSTEN) + 1


def level_fortschritt(spieler_daten):
    if not level_system_sicherstellen(spieler_daten):
        raise TypeError(
            "Spielerdaten müssen ein Dictionary sein."
        )

    gesamt_exp = spieler_daten["entwicklung"]["gesamt_exp"]
    level = level_fuer_exp(gesamt_exp)

    kosten = (
        LEVEL_KOSTEN[level - 1]
        if level <= len(LEVEL_KOSTEN)
        else None
    )

    seit_aufstieg = (
        gesamt_exp
        - sum(LEVEL_KOSTEN[:level - 1])
    )

    return {
        "level": level,
        "gesamt_exp": gesamt_exp,
        "exp_im_level": seit_aufstieg,
        "exp_bis_aufstieg": (
            None
            if kosten is None
            else kosten - seit_aufstieg
        ),
        "aufstiegskosten": kosten,
        "talentpunkte_verdient": level
    }


def exp_hinzufuegen(spieler_daten, quelle_id):
    if not isinstance(quelle_id, str):
        raise ValueError(
            "EXP-Quelle muss eine registrierte Kennung sein."
        )

    quelle = EXP_QUELLEN.get(quelle_id)

    if not isinstance(quelle, dict):
        raise ValueError(
            f"Unbekannte EXP-Quelle: {quelle_id}"
        )

    menge = quelle.get("exp")
    limit = quelle.get("limit", 1)

    if not _natuerliche_zahl(menge) or menge == 0:
        raise ValueError(
            "EXP-Belohnung muss eine positive ganze Zahl sein."
        )

    if not _natuerliche_zahl(limit) or limit == 0:
        raise ValueError(
            "EXP-Quellenlimit muss eine positive ganze Zahl sein."
        )

    vorher = level_fortschritt(spieler_daten)
    daten = spieler_daten["entwicklung"]
    anzahl = daten["exp_quellen"].get(quelle_id, 0)
    vergeben = 0

    if anzahl < limit:
        daten["gesamt_exp"] += menge
        daten["exp_quellen"][quelle_id] = anzahl + 1
        vergeben = menge

    nachher = level_fortschritt(spieler_daten)

    return {
        "vergebene_exp": vergeben,
        "level_vorher": vorher["level"],
        "level_nachher": nachher["level"],
        "neue_talentpunkte": (
            nachher["level"] - vorher["level"]
        )
    }




def exp_ziele_abgleichen(spieler_daten):
    if not level_system_sicherstellen(spieler_daten):
        raise TypeError(
            "Spielerdaten müssen ein Dictionary sein."
        )

    belohnungen = []

    for quelle_id, quelle in EXP_QUELLEN.items():
        bedingung = quelle.get("bedingung")

        if (
            not isinstance(bedingung, tuple)
            or len(bedingung) != 2
        ):
            continue

        feld, zielwert = bedingung
        pfad = (feld,) if isinstance(feld, str) else feld

        if not isinstance(pfad, tuple) or not pfad:
            continue

        wert = spieler_daten

        for schluessel in pfad:
            if (
                not isinstance(wert, dict)
                or not isinstance(schluessel, str)
            ):
                wert = None
                break

            wert = wert.get(schluessel)

        if isinstance(zielwert, bool):
            if wert is not zielwert:
                continue
        elif wert != zielwert:
            continue

        ergebnis = exp_hinzufuegen(
            spieler_daten,
            quelle_id
        )

        if ergebnis["vergebene_exp"]:
            belohnungen.append({
                "quelle_id": quelle_id,
                "name": quelle["name"],
                **ergebnis
            })

    return belohnungen