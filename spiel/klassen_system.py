KLASSEN = {
    "kaempfer": {
        "name": "Krieger",
        "beschreibung": "Standfestigkeit, Wucht und Gegenangriffe.",
        "voraussetzungen": {"koerper": 2}
    },
    "spaeher": {
        "name": "Späher",
        "beschreibung": "Beobachtung, Beweglichkeit und Gegneröffnungen.",
        "voraussetzungen": {"geschick": 2, "wahrnehmung": 2}
    },
    "gelehrter": {
        "name": "Gelehrter",
        "beschreibung": "Wissen, Analyse und das Erkennen gegnerischer Muster.",
        "voraussetzungen": {"geist": 2}
    },
    "magier": {
        "name": "Magier",
        "beschreibung": "Kontrollierte Resonanz und begrenzte magische Angriffe.",
        "voraussetzungen": {"geist": 2, "uebersinnliches": 1}
    }
}


def magier_resonanzwerte(spieler_daten):
    geist = klassen_eigener_wert(spieler_daten, "geist")
    uebersinnliches = klassen_eigener_wert(spieler_daten, "uebersinnliches")
    gelernt = (
        grundklasse_holen(spieler_daten) == "magier"
        and geist is not None and geist >= 2
        and uebersinnliches is not None and uebersinnliches >= 1
    )
    return {
        "magier_resonanz_gelernt": gelernt,
        "magier_geist": geist if gelernt else 0,
        "magier_uebersinnliches": uebersinnliches if gelernt else 0
    }


def _klassenstand_gueltig(daten):
    return (
        isinstance(daten, dict)
        and (daten.get("grundklasse") is None
             or isinstance(daten.get("grundklasse"), str))
        and isinstance(daten.get("ausbildungen", []), list)
        and all(isinstance(wert, str)
                for wert in daten.get("ausbildungen", []))
    )


def grundklasse_holen(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return None
    daten = spieler_daten.get("klasse", {})
    if not _klassenstand_gueltig(daten):
        return None
    return daten.get("grundklasse")


def klassen_eigener_wert(spieler_daten, wert_id):
    if not isinstance(spieler_daten, dict):
        return None
    attribute = spieler_daten.get("attribute")
    verfassungen = spieler_daten.get("verfassungen", {})
    if not isinstance(attribute, dict) or not isinstance(verfassungen, dict):
        return None
    zuordnung = {"geschick": "koerper", "wahrnehmung": "geist"}
    attribut_id = zuordnung.get(wert_id, wert_id)
    wert = attribute.get(attribut_id)
    if type(wert) is not int or wert < 0:
        return None
    if wert_id in zuordnung:
        praegung = verfassungen.get(wert_id, 0)
        if type(praegung) is not int or praegung < 0:
            return None
        wert += praegung
    return wert


KLASSEN_LEHRER = {
    "kaempfer": "Bjorn",
    "spaeher": "Rika",
    "gelehrter": "Mira",
    "magier": "Selene"
}


def klassenwahl_hindernisse(spieler_daten, klasse_id, *, wechsel=False):
    if not isinstance(spieler_daten, dict):
        return ["Ungültige Spielerdaten."]
    if not isinstance(klasse_id, str) or klasse_id not in KLASSEN:
        return ["Unbekannte Klasse."]
    daten = spieler_daten.get("klasse", {})
    if not _klassenstand_gueltig(daten):
        return ["Ungültiger Klassenstand; keine neue Wahl möglich."]
    if daten.get("grundklasse") == klasse_id:
        return ["Das ist bereits deine Grundklasse."]
    if daten.get("grundklasse") is not None and not wechsel:
        return [
            "Deine Grundklasse kannst du bei "
            f"{KLASSEN_LEHRER[klasse_id]} wechseln."
        ]
    hindernisse = []
    for wert_id, minimum in KLASSEN[klasse_id]["voraussetzungen"].items():
        wert = klassen_eigener_wert(spieler_daten, wert_id)
        if wert is None or wert < minimum:
            name = {
                "koerper": "Körper",
                "geist": "Geist",
                "uebersinnliches": "Übersinnliches",
                "geschick": "Geschick",
                "wahrnehmung": "Wahrnehmung"
            }.get(wert_id, wert_id)
            hindernisse.append(f"Benötigt eigenen Wert {name}: {minimum}.")
    if klasse_id not in daten.get("ausbildungen", []):
        hindernisse.append("Schließe zuerst die zugehörige Lehreraufgabe ab.")
    return hindernisse


def klassenausbildung_abschliessen(spieler_daten, klasse_id):
    if (not isinstance(spieler_daten, dict)
            or not isinstance(klasse_id, str)
            or klasse_id not in KLASSEN):
        return False
    daten = spieler_daten.get("klasse", {})
    if not _klassenstand_gueltig(daten):
        return False
    ausbildungen = daten.get("ausbildungen", [])
    if klasse_id in ausbildungen:
        return False
    spieler_daten["klasse"] = {
        **daten,
        "grundklasse": daten.get("grundklasse"),
        "ausbildungen": [*ausbildungen, klasse_id]
    }
    return True


def grundklasse_waehlen(spieler_daten, klasse_id, *, bestaetigt=False,
                        wechsel=False):
    if bestaetigt is not True:
        return False
    if klassenwahl_hindernisse(spieler_daten, klasse_id, wechsel=wechsel):
        return False
    daten = spieler_daten.get("klasse", {})
    spieler_daten["klasse"] = {**daten, "grundklasse": klasse_id}
    return True