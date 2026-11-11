from beruf_system import (
    jaeger_beuteversorgung_gelernt,
    schmied_waffenpflege_gelernt,
    schmied_waffenpflege_kampfbonus
)
from klassen_system import grundklasse_holen, magier_resonanzwerte
from glutkrieger_system import (
    GLUTKRIEGER_GERICHTE,
    glutkrieger_ausbildung_moeglich,
    glutkrieger_portion_holen
)


# Alle Hybridwege; jeder hat höchstens eine offene Probe ("<weg>_probe").
HYBRIDWEGE = ("bestienjaeger", "stahlkrieger", "glutkrieger", "runenschmied", "faehrtensteller")


def _hybridstand(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return None
    daten = spieler_daten.get("hybrid", {})
    if not isinstance(daten, dict):
        return None
    gelernt = daten.get("freigeschaltet", [])
    if (not isinstance(gelernt, list)
            or not all(isinstance(wert, str) for wert in gelernt)
            or daten.get("aktiv") not in (None,) + HYBRIDWEGE
            or any(type(daten.get(weg + "_probe", False)) is not bool
                   for weg in HYBRIDWEGE)
            or sum(daten.get(weg + "_probe", False)
                   for weg in HYBRIDWEGE) > 1
            or ("glutkrieger_portion" in daten
                and (not isinstance(daten["glutkrieger_portion"], str)
                     or daten["glutkrieger_portion"] not in GLUTKRIEGER_GERICHTE))):
        return None
    return daten


def hybrid_probe_offen(spieler_daten, ausser=None):
    daten = _hybridstand(spieler_daten)
    return daten is not None and any(
        daten.get(weg + "_probe", False)
        for weg in HYBRIDWEGE if weg != ausser
    )


def hybrid_probe_bestanden(spieler_daten, weg):
    # Gespeicherte Leistung, unabhängig von aktueller Grundklasse und Fusion.
    daten = _hybridstand(spieler_daten)
    return daten is not None and weg in daten.get("freigeschaltet", [])


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
    if daten.get("aktiv") == "runenschmied" and runenschmied_freigeschaltet(spieler_daten):
        return "runenschmied"
    if daten.get("aktiv") == "faehrtensteller" and faehrtensteller_freigeschaltet(spieler_daten):
        return "faehrtensteller"
    return None


def hybrid_name_holen(spieler_daten):
    return {"bestienjaeger": "Bestienjäger", "stahlkrieger": "Stahlkrieger", "glutkrieger": "Glutkrieger",
            "runenschmied": "Runenschmied", "faehrtensteller": "Fährtensteller"}.get(
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


# WM-C2: Runenschmied (Magier + Schmied). Runen gehören zur Waffe (Feld "rune").
RUNEN = {"klang": "Klangrune", "ruhe": "Ruherune", "halt": "Haltrune"}
# Verfassung, die eine Rune zum Setzen braucht (Schlüssel aus magier_resonanzwerte).
RUNEN_VERFASSUNG = {"klang": "magier_resonanz_stufe", "ruhe": "magier_kontrolle", "halt": "magier_anker"}
RUNE_KOSTEN = {"schieferplatte": 2, "gold": 10}


def runenschmied_voraussetzungen(spieler_daten):
    return (
        isinstance(spieler_daten, dict)
        and grundklasse_holen(spieler_daten) == "magier"
        and schmied_waffenpflege_gelernt(spieler_daten)
        and magier_resonanzwerte(spieler_daten)["magier_resonanz_stufe"] >= 1
        and _hybridstand(spieler_daten) is not None
    )


def runenschmied_freigeschaltet(spieler_daten):
    daten = _hybridstand(spieler_daten)
    return (
        runenschmied_voraussetzungen(spieler_daten)
        and "runenschmied" in daten.get("freigeschaltet", [])
    )


def rune_setzbar(spieler_daten, rune):
    # Setzen braucht den freigeschalteten (nicht aktiven) Runenschmied und die passende Verfassung >= 1.
    return (
        rune in RUNEN
        and runenschmied_freigeschaltet(spieler_daten)
        and magier_resonanzwerte(spieler_daten)[RUNEN_VERFASSUNG[rune]] >= 1
    )


def runenschmied_probe_starten(spieler_daten, *, bestaetigt=False):
    # Die ausgerüstete Waffe muss schon die Klangrune tragen (Übungsrune oder vorhandene).
    waffe = spieler_daten.get("waffe") if isinstance(spieler_daten, dict) else None
    if (bestaetigt is not True or not runenschmied_voraussetzungen(spieler_daten)
            or runenschmied_freigeschaltet(spieler_daten)
            or hybrid_probe_offen(spieler_daten)
            or not isinstance(waffe, dict) or waffe.get("rune") != "klang"):
        return False
    neuer_stand = dict(_hybridstand(spieler_daten))
    neuer_stand["runenschmied_probe"] = True
    spieler_daten["hybrid"] = neuer_stand
    return True


def runenschmied_probe_abbrechen(spieler_daten):
    # Auch ohne erfüllte Voraussetzungen möglich, damit eine offene Probe nie festhängt.
    daten = _hybridstand(spieler_daten)
    if daten is None or not daten.get("runenschmied_probe", False):
        return False
    neuer_stand = dict(daten)
    neuer_stand["runenschmied_probe"] = False
    spieler_daten["hybrid"] = neuer_stand
    return True


def runenschmied_kampfwerte(spieler_daten):
    daten = _hybridstand(spieler_daten)
    pruefung = runenschmied_voraussetzungen(spieler_daten) and daten.get("runenschmied_probe", False)
    aktiv = hybrid_aktiv_holen(spieler_daten) == "runenschmied"
    return {
        # Für Rune wecken: aktiver Hybrid bei Grundklasse Magier, keine andere Probe offen.
        "runenschmied_gelernt": aktiv and not hybrid_probe_offen(spieler_daten, "runenschmied"),
        "runenschmied_pruefung": pruefung
    }


def runenschmied_probe_auswerten(spieler_daten, ergebnis):
    # Nicht bestanden: Die Probe bleibt offen; der nächste Kampf ist der nächste Versuch.
    if not runenschmied_voraussetzungen(spieler_daten):
        return False
    daten = _hybridstand(spieler_daten)
    if not daten.get("runenschmied_probe", False) or not isinstance(ergebnis, dict):
        return False
    bestanden = (
        ergebnis.get("gewonnen") is True
        and ergebnis.get("besiegt") is False
        and ergebnis.get("geflohen") is False
        and "klang" in (ergebnis.get("rune_gewirkt") or [])
    )
    if not bestanden:
        return False
    neuer_stand = dict(daten)
    neuer_stand["runenschmied_probe"] = False
    if "runenschmied" not in daten.get("freigeschaltet", []):
        neuer_stand["freigeschaltet"] = daten.get("freigeschaltet", []) + ["runenschmied"]
    spieler_daten["hybrid"] = neuer_stand
    return True


# WM-D2: Fährtensteller (Späher + Jäger). Lehrerin Rika, Schlüssel "rika_faehrten".
FAEHRTEN_PRUEFGEGNER = ("Wolf", "Keiler")


def faehrtensteller_voraussetzungen(spieler_daten):
    return (
        isinstance(spieler_daten, dict)
        and spieler_daten.get("prolog_status") == "prolog_abgeschlossen"
        and grundklasse_holen(spieler_daten) == "spaeher"
        and jaeger_beuteversorgung_gelernt(spieler_daten)
        and _hybridstand(spieler_daten) is not None
    )


def faehrtensteller_freigeschaltet(spieler_daten):
    daten = _hybridstand(spieler_daten)
    return (
        faehrtensteller_voraussetzungen(spieler_daten)
        and "faehrtensteller" in daten.get("freigeschaltet", [])
    )


def faehrtensteller_probe_offen(spieler_daten):
    daten = _hybridstand(spieler_daten)
    return daten is not None and daten.get("faehrtensteller_probe", False) is True


def faehrtensteller_aktiv(spieler_daten):
    # Falle, Hinterhalt und Fährtenlesen: aktiver Fährtensteller, keine andere Probe offen.
    return (hybrid_aktiv_holen(spieler_daten) == "faehrtensteller"
            and not hybrid_probe_offen(spieler_daten, "faehrtensteller"))


def faehrtensteller_probe_starten(spieler_daten, *, bestaetigt=False):
    if (bestaetigt is not True or not faehrtensteller_voraussetzungen(spieler_daten)
            or faehrtensteller_freigeschaltet(spieler_daten)
            or hybrid_probe_offen(spieler_daten)):
        return False
    neuer_stand = dict(_hybridstand(spieler_daten))
    neuer_stand["faehrtensteller_probe"] = True
    spieler_daten["hybrid"] = neuer_stand
    return True


def faehrtensteller_probe_abbrechen(spieler_daten):
    # Auch ohne erfüllte Voraussetzungen möglich, damit eine offene Probe nie festhängt.
    if not faehrtensteller_probe_offen(spieler_daten):
        return False
    neuer_stand = dict(_hybridstand(spieler_daten))
    neuer_stand["faehrtensteller_probe"] = False
    spieler_daten["hybrid"] = neuer_stand
    return True


def faehrtensteller_kampfwerte(spieler_daten, gegner_typ, situation):
    # Prüfungskampf: offene Probe, Wolf oder Keiler auf der Wildspur (auch vor der Freischaltung).
    pruefung = (
        faehrtensteller_voraussetzungen(spieler_daten)
        and faehrtensteller_probe_offen(spieler_daten)
        and gegner_typ in FAEHRTEN_PRUEFGEGNER
        and isinstance(situation, dict)
        and situation.get("gebiet") == "Wald"
        and situation.get("umgebung") == "Wildspur"
    )
    return {
        "faehrtensteller_gelernt": faehrtensteller_aktiv(spieler_daten),
        "faehrtensteller_pruefung": pruefung
    }


def faehrtensteller_probe_auswerten(spieler_daten, ergebnis):
    # Ein Kampf zählt für sich; Fortschritte aus mehreren Kämpfen werden nicht zusammengesetzt.
    # Nur "bestanden" schaltet frei; sonst bleibt die Probe offen. None: keine Auswertung.
    if (not faehrtensteller_voraussetzungen(spieler_daten)
            or not faehrtensteller_probe_offen(spieler_daten)
            or not isinstance(ergebnis, dict)):
        return None
    if ergebnis.get("faehrten_entdeckt") is not True:
        return "nicht_bemerkt"
    if not (ergebnis.get("gewonnen") is True
            and ergebnis.get("besiegt") is False
            and ergebnis.get("geflohen") is False
            and ergebnis.get("gegner_typ") in FAEHRTEN_PRUEFGEGNER):
        return "misslungen"
    if ergebnis.get("faehrten_vorbereitung") not in ("falle", "hinterhalt"):
        return "ohne_vorbereitung"
    if ergebnis.get("faehrten_luecke_genutzt") is not True:
        return "ohne_luecke"
    daten = _hybridstand(spieler_daten)
    neuer_stand = dict(daten)
    neuer_stand["faehrtensteller_probe"] = False
    if "faehrtensteller" not in daten.get("freigeschaltet", []):
        neuer_stand["freigeschaltet"] = daten.get("freigeschaltet", []) + ["faehrtensteller"]
    spieler_daten["hybrid"] = neuer_stand
    return "bestanden"


def hybrid_beim_lehrer_waehlen(spieler_daten, hybrid_id, lehrer, *, bestaetigt=False):
    wege = {"rika": ("bestienjaeger", bestienjaeger_freigeschaltet),
            "bjorn": ("stahlkrieger", stahlkrieger_freigeschaltet),
            "mara": ("glutkrieger", glutkrieger_freigeschaltet),
            "bjorn_runen": ("runenschmied", runenschmied_freigeschaltet),
            "rika_faehrten": ("faehrtensteller", faehrtensteller_freigeschaltet)}
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