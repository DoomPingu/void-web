from beruf_system import (
    jaeger_beuteversorgung_gelernt,
    schmied_waffenpflege_gelernt,
    schmied_waffenpflege_kampfbonus
)
from klassen_system import grundklasse_holen
from glutkrieger_system import (
    GLUTKRIEGER_GERICHTE,
    glutkrieger_ausbildung_moeglich,
    glutkrieger_portion_holen
)


def _hybridstand(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return None
    daten = spieler_daten.get("hybrid", {})
    if not isinstance(daten, dict):
        return None
    gelernt = daten.get("freigeschaltet", [])
    if (not isinstance(gelernt, list)
            or not all(isinstance(wert, str) for wert in gelernt)
            or daten.get("aktiv") not in (None, "bestienjaeger", "stahlkrieger", "glutkrieger")
            or any(type(daten.get(weg + "_probe", False)) is not bool
                   for weg in ("bestienjaeger", "stahlkrieger", "glutkrieger"))
            or sum(daten.get(weg + "_probe", False)
                   for weg in ("bestienjaeger", "stahlkrieger", "glutkrieger")) > 1
            or ("glutkrieger_portion" in daten
                and (not isinstance(daten["glutkrieger_portion"], str)
                     or daten["glutkrieger_portion"] not in GLUTKRIEGER_GERICHTE))):
        return None
    return daten


def hybrid_probe_offen(spieler_daten, ausser=None):
    daten = _hybridstand(spieler_daten)
    return daten is not None and any(
        daten.get(weg + "_probe", False)
        for weg in ("bestienjaeger", "stahlkrieger", "glutkrieger") if weg != ausser
    )


def bestienjaeger_voraussetzungen(spieler_daten):
    return (
        isinstance(spieler_daten, dict)
        and spieler_daten.get("prolog_status") == "prolog_abgeschlossen"
        and grundklasse_holen(spieler_daten) == "kaempfer"
        and jaeger_beuteversorgung_gelernt(spieler_daten)
        and _hybridstand(spieler_daten) is not None
    )


def bestienjaeger_freigeschaltet(spieler_daten):
    daten = _hybridstand(spieler_daten)
    return (
        bestienjaeger_voraussetzungen(spieler_daten)
        and "bestienjaeger" in daten.get("freigeschaltet", [])
    )


def stahlkrieger_voraussetzungen(spieler_daten):
    return (
        isinstance(spieler_daten, dict)
        and grundklasse_holen(spieler_daten) == "kaempfer"
        and schmied_waffenpflege_gelernt(spieler_daten)
        and _hybridstand(spieler_daten) is not None
    )


def stahlkrieger_freigeschaltet(spieler_daten):
    daten = _hybridstand(spieler_daten)
    return (
        stahlkrieger_voraussetzungen(spieler_daten)
        and "stahlkrieger" in daten.get("freigeschaltet", [])
    )


def hybrid_aktiv_holen(spieler_daten):
    daten = _hybridstand(spieler_daten)
    if daten is None:
        return None
    if daten.get("aktiv") == "bestienjaeger" and bestienjaeger_freigeschaltet(spieler_daten):
        return "bestienjaeger"
    if daten.get("aktiv") == "stahlkrieger" and stahlkrieger_freigeschaltet(spieler_daten):
        return "stahlkrieger"
    if daten.get("aktiv") == "glutkrieger" and glutkrieger_freigeschaltet(spieler_daten):
        return "glutkrieger"
    return None


def hybrid_name_holen(spieler_daten):
    return {"bestienjaeger": "Bestienjäger", "stahlkrieger": "Stahlkrieger", "glutkrieger": "Glutkrieger"}.get(
        hybrid_aktiv_holen(spieler_daten)
    )


def bestienjaeger_probe_starten(spieler_daten, *, bestaetigt=False):
    if (bestaetigt is not True or not bestienjaeger_voraussetzungen(spieler_daten)
            or bestienjaeger_freigeschaltet(spieler_daten)):
        return False
    daten = _hybridstand(spieler_daten)
    if hybrid_probe_offen(spieler_daten):
        return False
    neuer_stand = dict(daten)
    neuer_stand["bestienjaeger_probe"] = True
    spieler_daten["hybrid"] = neuer_stand
    return True


def bestienjaeger_kampfwerte(spieler_daten, gegner_typ, situation):
    daten = _hybridstand(spieler_daten)
    pruefung = (
        bestienjaeger_voraussetzungen(spieler_daten)
        and daten.get("bestienjaeger_probe", False)
        and gegner_typ in ("Wolf", "Keiler")
        and isinstance(situation, dict)
        and situation.get("gebiet") == "Wald"
        and situation.get("umgebung") == "Wildspur"
    )
    aktiv = hybrid_aktiv_holen(spieler_daten) == "bestienjaeger"
    return {
        "bestienjaeger_gelernt": (aktiv and not hybrid_probe_offen(spieler_daten, "bestienjaeger")) or pruefung,
        "bestienjaeger_pruefung": pruefung
    }


def bestienjaeger_probe_auswerten(spieler_daten, ergebnis):
    if not bestienjaeger_voraussetzungen(spieler_daten):
        return False
    daten = _hybridstand(spieler_daten)
    if not daten.get("bestienjaeger_probe", False) or not isinstance(ergebnis, dict):
        return False
    bestanden = (
        ergebnis.get("gewonnen") is True
        and ergebnis.get("besiegt") is False
        and ergebnis.get("geflohen") is False
        and ergebnis.get("gegner_typ") in ("Wolf", "Keiler")
        and ergebnis.get("bestienjaeger_studiert") is True
        and ergebnis.get("bestienjaeger_abwehr") is True
        and ergebnis.get("bestienjaeger_jagdhieb") is True
    )
    neuer_stand = dict(daten)
    neuer_stand["bestienjaeger_probe"] = False
    if bestanden and "bestienjaeger" not in daten.get("freigeschaltet", []):
        neuer_stand["freigeschaltet"] = daten.get("freigeschaltet", []) + ["bestienjaeger"]
    spieler_daten["hybrid"] = neuer_stand
    return bestanden


def stahlkrieger_probe_starten(spieler_daten, *, bestaetigt=False):
    if (bestaetigt is not True or not stahlkrieger_voraussetzungen(spieler_daten)
            or stahlkrieger_freigeschaltet(spieler_daten)
            or not schmied_waffenpflege_kampfbonus(spieler_daten, spieler_daten.get("waffe"))):
        return False
    daten = _hybridstand(spieler_daten)
    if hybrid_probe_offen(spieler_daten):
        return False
    neuer_stand = dict(daten)
    neuer_stand["stahlkrieger_probe"] = True
    spieler_daten["hybrid"] = neuer_stand
    return True


def stahlkrieger_kampfwerte(spieler_daten, waffe):
    daten = _hybridstand(spieler_daten)
    pruefung = stahlkrieger_voraussetzungen(spieler_daten) and daten.get("stahlkrieger_probe", False)
    pflege = schmied_waffenpflege_kampfbonus(spieler_daten, waffe)
    aktiv = hybrid_aktiv_holen(spieler_daten) == "stahlkrieger"
    gelernt = (aktiv and not hybrid_probe_offen(spieler_daten, "stahlkrieger")) or (pruefung and pflege)
    return {
        "stahlkrieger_gelernt": gelernt,
        "stahlkrieger_pruefung": pruefung,
        "stahlkrieger_waffenpflege": gelernt and pflege
    }


def stahlkrieger_probe_auswerten(spieler_daten, ergebnis):
    if not stahlkrieger_voraussetzungen(spieler_daten):
        return False
    daten = _hybridstand(spieler_daten)
    if not daten.get("stahlkrieger_probe", False) or not isinstance(ergebnis, dict):
        return False
    bestanden = (
        ergebnis.get("gewonnen") is True
        and ergebnis.get("besiegt") is False
        and ergebnis.get("geflohen") is False
        and ergebnis.get("gegner_typ") in ("Wolf", "Keiler", "Bandit", "Waldwächter")
        and ergebnis.get("stahlkrieger_amboss") is True
        and ergebnis.get("stahlkrieger_schmiedehieb") is True
    )
    neuer_stand = dict(daten)
    neuer_stand["stahlkrieger_probe"] = False
    if bestanden and "stahlkrieger" not in daten.get("freigeschaltet", []):
        neuer_stand["freigeschaltet"] = daten.get("freigeschaltet", []) + ["stahlkrieger"]
    spieler_daten["hybrid"] = neuer_stand
    return bestanden


def glutkrieger_voraussetzungen(spieler_daten):
    return glutkrieger_ausbildung_moeglich(spieler_daten) and _hybridstand(spieler_daten) is not None


def glutkrieger_freigeschaltet(spieler_daten):
    return (glutkrieger_voraussetzungen(spieler_daten)
            and "glutkrieger" in spieler_daten.get("hybrid", {}).get("freigeschaltet", []))


def glutkrieger_probe_starten(spieler_daten, *, bestaetigt=False):
    if (bestaetigt is not True or not glutkrieger_voraussetzungen(spieler_daten)
            or glutkrieger_freigeschaltet(spieler_daten)
            or hybrid_probe_offen(spieler_daten)
            or glutkrieger_portion_holen(spieler_daten) is None):
        return False
    neuer_stand = dict(spieler_daten.get("hybrid", {}))
    neuer_stand["glutkrieger_probe"] = True
    spieler_daten["hybrid"] = neuer_stand
    return True


def glutkrieger_kampfwerte(spieler_daten):
    daten = _hybridstand(spieler_daten)
    pruefung = glutkrieger_voraussetzungen(spieler_daten) and daten.get("glutkrieger_probe", False)
    aktiv = hybrid_aktiv_holen(spieler_daten) == "glutkrieger"
    gelernt = (aktiv and not hybrid_probe_offen(spieler_daten, "glutkrieger")) or pruefung
    return {
        "glutkrieger_gelernt": gelernt,
        "glutkrieger_pruefung": pruefung,
        "glutkrieger_portion": gelernt and glutkrieger_portion_holen(spieler_daten) is not None
    }


def glutkrieger_probe_auswerten(spieler_daten, ergebnis):
    if not glutkrieger_voraussetzungen(spieler_daten):
        return False
    daten = _hybridstand(spieler_daten)
    if not daten.get("glutkrieger_probe", False) or not isinstance(ergebnis, dict):
        return False
    bestanden = (
        ergebnis.get("gewonnen") is True
        and ergebnis.get("besiegt") is False
        and ergebnis.get("geflohen") is False
        and ergebnis.get("gegner_typ") in ("Wolf", "Keiler", "Bandit", "Waldwächter")
        and ergebnis.get("glutkrieger_portion_verbraucht") is True
        and ergebnis.get("glutkrieger_kraftschub") is True
    )
    neuer_stand = dict(daten)
    neuer_stand["glutkrieger_probe"] = False
    if bestanden and "glutkrieger" not in daten.get("freigeschaltet", []):
        neuer_stand["freigeschaltet"] = daten.get("freigeschaltet", []) + ["glutkrieger"]
    spieler_daten["hybrid"] = neuer_stand
    return bestanden


def hybrid_beim_lehrer_waehlen(spieler_daten, hybrid_id, lehrer, *, bestaetigt=False):
    wege = {"rika": ("bestienjaeger", bestienjaeger_freigeschaltet),
            "bjorn": ("stahlkrieger", stahlkrieger_freigeschaltet),
            "mara": ("glutkrieger", glutkrieger_freigeschaltet)}
    if bestaetigt is not True or not isinstance(lehrer, str) or lehrer not in wege:
        return False
    weg, freigeschaltet = wege[lehrer]
    if hybrid_id not in (None, weg) or not freigeschaltet(spieler_daten):
        return False
    daten = _hybridstand(spieler_daten)
    if (hybrid_probe_offen(spieler_daten)
            or daten.get("aktiv") == hybrid_id
            or (hybrid_id is None and daten.get("aktiv") != weg)):
        return False
    neuer_stand = dict(daten)
    neuer_stand["aktiv"] = hybrid_id
    spieler_daten["hybrid"] = neuer_stand
    return True 