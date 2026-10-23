from beruf_system import koch_vorratskueche_gelernt
from klassen_system import grundklasse_holen


GLUTKRIEGER_GERICHTE = {
    "geroestetes_brot": "Geröstetes Brot",
    "apfelkompott": "Apfelkompott",
    "kraeuterbrot": "Kräuterbrot",
    "gebratenes_wildfleisch": "Gebratenes Wildfleisch",
    "gemuesesuppe": "Einfache Gemüsesuppe"
}


def glutkrieger_ausbildung_moeglich(spieler_daten):
    return (
        isinstance(spieler_daten, dict)
        and spieler_daten.get("prolog_status") == "prolog_abgeschlossen"
        and grundklasse_holen(spieler_daten) == "kaempfer"
        and koch_vorratskueche_gelernt(spieler_daten)
    )


def glutkrieger_portion_holen(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return None
    daten = spieler_daten.get("hybrid", {})
    if not isinstance(daten, dict):
        return None
    portion = daten.get("glutkrieger_portion")
    return portion if isinstance(portion, str) and portion in GLUTKRIEGER_GERICHTE else None


def glutkrieger_portion_vorbereiten(spieler_daten, gericht, *, bestaetigt=False):
    if (bestaetigt is not True or not glutkrieger_ausbildung_moeglich(spieler_daten)
            or not isinstance(gericht, str) or gericht not in GLUTKRIEGER_GERICHTE):
        return False
    daten = spieler_daten.get("hybrid", {})
    inventar = spieler_daten.get("inventar_items", {})
    if (not isinstance(daten, dict) or not isinstance(inventar, dict)
            or "glutkrieger_portion" in daten
            or type(inventar.get(gericht)) is not int or inventar[gericht] < 1):
        return False
    neuer_stand = dict(daten)
    neuer_stand["glutkrieger_portion"] = gericht
    neues_inventar = dict(inventar)
    neues_inventar[gericht] -= 1
    if neues_inventar[gericht] == 0:
        del neues_inventar[gericht]
    spieler_daten["hybrid"] = neuer_stand
    spieler_daten["inventar_items"] = neues_inventar
    return True


def glutkrieger_portion_verbrauchen(spieler_daten, ergebnis):
    if (not isinstance(ergebnis, dict)
            or ergebnis.get("glutkrieger_portion_verbraucht") is not True
            or glutkrieger_portion_holen(spieler_daten) is None):
        return False
    neuer_stand = dict(spieler_daten["hybrid"])
    del neuer_stand["glutkrieger_portion"]
    spieler_daten["hybrid"] = neuer_stand
    return True