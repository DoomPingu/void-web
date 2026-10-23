def koch_gelernt(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return False
    berufe = spieler_daten.get("berufe", {})
    if not isinstance(berufe, dict):
        return False
    daten = berufe.get("koch", {})
    if not isinstance(daten, dict):
        return False
    aufgaben = daten.get("aufgaben", [])
    return (
        isinstance(aufgaben, list)
        and all(isinstance(wert, str) for wert in aufgaben)
        and "mara_grundausbildung" in aufgaben
    )


KOCH_PRAXIS_REZEPTE = (
    "geroestetes_brot", "apfelkompott", "kraeuterbrot",
    "gebratenes_wildfleisch", "gemuesesuppe"
)


def koch_praxis_fortschritt(spieler_daten):
    if not koch_gelernt(spieler_daten):
        return None
    praxis = spieler_daten["berufe"]["koch"].get("praxis", [])
    if not isinstance(praxis, list) or not all(isinstance(wert, str) for wert in praxis):
        return None
    return len(set(praxis).intersection(KOCH_PRAXIS_REZEPTE))


def koch_praxis_abschliessen(spieler_daten, rezept_id):
    if (not isinstance(rezept_id, str) or rezept_id not in KOCH_PRAXIS_REZEPTE
            or koch_praxis_fortschritt(spieler_daten) is None):
        return False
    berufe = spieler_daten["berufe"]
    daten = berufe["koch"]
    praxis = daten.get("praxis", [])
    if rezept_id in praxis:
        return False
    neuer_stand = dict(daten)
    neuer_stand["praxis"] = praxis + [rezept_id]
    neue_berufe = dict(berufe)
    neue_berufe["koch"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def koch_vorratskueche_gelernt(spieler_daten):
    fortschritt = koch_praxis_fortschritt(spieler_daten)
    return (
        fortschritt is not None and fortschritt >= 2
        and "mara_vorratskueche" in spieler_daten["berufe"]["koch"]["aufgaben"]
    )


def koch_portionenstand(spieler_daten):
    if not koch_vorratskueche_gelernt(spieler_daten):
        return None
    stand = spieler_daten["berufe"]["koch"].get("portionenstand", 0)
    return stand if type(stand) is int and 0 <= stand <= 3 else None


def koch_vorratskueche_lernen(spieler_daten, *, bestaetigt=False):
    fortschritt = koch_praxis_fortschritt(spieler_daten)
    if (bestaetigt is not True or fortschritt is None or fortschritt < 2
            or koch_vorratskueche_gelernt(spieler_daten)):
        return False
    berufe = spieler_daten["berufe"]
    daten = berufe["koch"]
    if "portionenstand" in daten:
        return False
    neuer_stand = dict(daten)
    neuer_stand["aufgaben"] = daten["aufgaben"] + ["mara_vorratskueche"]
    neuer_stand["portionenstand"] = 0
    neue_berufe = dict(berufe)
    neue_berufe["koch"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def koch_zusatzportion(spieler_daten, rezept_id):
    if not isinstance(rezept_id, str) or rezept_id not in KOCH_PRAXIS_REZEPTE:
        return 0
    return 1 if koch_portionenstand(spieler_daten) == 3 else 0


def koch_zubereitung_abschliessen(spieler_daten, rezept_id):
    if not isinstance(rezept_id, str) or rezept_id not in KOCH_PRAXIS_REZEPTE:
        return False
    stand = koch_portionenstand(spieler_daten)
    if stand is None:
        return False
    berufe = spieler_daten["berufe"]
    neuer_stand = dict(berufe["koch"])
    neuer_stand["portionenstand"] = (stand + 1) % 4
    neue_berufe = dict(berufe)
    neue_berufe["koch"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def koch_grundausbildung_abschliessen(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return False
    berufe = spieler_daten.get("berufe", {})
    if not isinstance(berufe, dict):
        return False
    daten = berufe.get("koch", {})
    if not isinstance(daten, dict):
        return False
    aufgaben = daten.get("aufgaben", [])
    if (not isinstance(aufgaben, list)
            or not all(isinstance(wert, str) for wert in aufgaben)
            or koch_gelernt(spieler_daten) or "stufe" in daten):
        return False
    neuer_stand = dict(daten)
    neuer_stand["stufe"] = "grundausbildung"
    neuer_stand["aufgaben"] = aufgaben + ["mara_grundausbildung"]
    neue_berufe = dict(berufe)
    neue_berufe["koch"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def berufsuebersicht(spieler_daten):
    eintraege = []
    berufe = spieler_daten.get("berufe", {}) if isinstance(spieler_daten, dict) else None
    for beruf_id, name, lehrer in (
        ("schmied", "Schmied", "Bjorn – Schmiede in Eichenruh"),
        ("jaeger", "Jäger", "Rika – Köhlerei am Waldrand"),
        ("koch", "Koch", "Mara – Gasthaus in Eichenruh")
    ):
        daten = berufe.get(beruf_id, {}) if isinstance(berufe, dict) else None
        gueltig = isinstance(daten, dict)
        if gueltig:
            aufgaben = daten.get("aufgaben", [])
            praxis = daten.get("praxis", [])
            gueltig = (
                isinstance(aufgaben, list) and isinstance(praxis, list)
                and all(isinstance(wert, str) for wert in aufgaben + praxis)
            )
        leser = {
            "schmied": schmied_gelernt,
            "jaeger": jaeger_gelernt,
            "koch": koch_gelernt
        }
        gelernt = leser[beruf_id](spieler_daten) if gueltig else False
        if not gueltig:
            status = "Stand nicht lesbar"
            hinweise = ["Die vorhandenen Berufsdaten werden nicht verändert."]
        elif not gelernt and daten:
            status = "Unbekannter Berufsstand"
            hinweise = ["Die vorhandenen Berufsdaten werden nicht verändert."]
        elif not gelernt:
            status = "Noch nicht gelernt"
            hinweise = ["Grundausbildung beim Lehrer nach dem Prolog möglich."]
        elif daten.get("stufe") != "grundausbildung":
            status = "Unbekannter Berufsstand"
            hinweise = ["Die vorhandenen Berufsdaten werden nicht verändert."]
        elif beruf_id == "schmied":
            status = "Grundausbildung abgeschlossen"
            eigenbau = "hauermesser" in praxis
            hinweise = ["Eigenes Hauermesser: " + ("hergestellt" if eigenbau else "offen")]
            if eigenbau:
                if schmied_waffenpflege_gelernt(spieler_daten):
                    hinweise.append("Waffenpflege gelernt: 2 Gold für +2 Schaden bei drei Waffentreffern im nächsten Kampf.")
                    bereit = schmied_waffenpflege_bereit(spieler_daten)
                    hinweise.append("Vorbereitet: " + bereit if bereit else "Nächste Vorbereitung: an Bjorns Werkbank.")
                else:
                    hinweise.append("Nächster Schritt: Waffenpflege bei Bjorn lernen.")
            else:
                hinweise.append("Nächster Schritt: Hauermesser selbst an Bjorns Werkbank herstellen.")
            hinweise.append("Eigenbau: 2 Keilerhauer und 4 Gold; mit Materialkunde 2 Gold.")
        elif beruf_id == "koch":
            status = "Grundausbildung abgeschlossen"
            hinweise = [
                "Grundlagen: sauber vorbereiten und Hitze kontrollieren.",
                "Rezepte lernst du weiterhin aus Büchern und durch Aufgaben.",
                "Kochen ist zu Hause und am Lagerfeuer möglich."
            ]
            fortschritt = koch_praxis_fortschritt(spieler_daten)
            hinweise.append(f"Eigene Gerichte: {fortschritt} (erstes Praxisziel: 2 verschiedene)")
            if fortschritt >= 2:
                hinweise.append("Erstes Kochpraxisziel abgeschlossen.")
                if koch_vorratskueche_gelernt(spieler_daten):
                    hinweise.append("Aktiv: Vorratsküche – jede vierte Zubereitung ergibt eine Zusatzportion.")
                    stand = koch_portionenstand(spieler_daten)
                    hinweise.append(
                        f"Noch {4 - stand} erfolgreiche Zubereitungen bis zur Zusatzportion."
                        if stand is not None else "Der vorhandene Portionenstand ist nicht lesbar; der Bonus bleibt aus."
                    )
                else:
                    hinweise.append("Nächster Schritt: Vorratsküche bei Mara lernen.")
            else:
                hinweise.append("Nächster Schritt: zwei unterschiedliche bekannte Rezepte selbst zubereiten.")
        else:
            status = "Grundausbildung abgeschlossen"
            hinweise = [
                "Wolf auf der Wildspur: "+ ("erledigt" if "wolf" in praxis else "offen"),
                "Keiler auf der Wildspur: " + ("erledigt" if "keiler" in praxis else "offen")
            ]
            if jaeger_beuteversorgung_gelernt(spieler_daten):
                hinweise.append("Aktiv: Saubere Beuteversorgung auf der Wildspur.")
                hinweise.append("Wolfsfell: 60 % statt 45 % | Keilerhauer: 75 % statt 60 %")
            elif "wolf" in praxis and "keiler" in praxis:
                hinweise.append("Nächster Schritt: Saubere Beuteversorgung bei Rika lernen.")
            else:
                hinweise.append("Nächster Schritt: Fehlende Jagden abschließen und zu Rika zurückkehren.")
        eintraege.append({"name": name, "status": status, "lehrer": lehrer, "hinweise": hinweise})
    return eintraege


def jaeger_gelernt(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return False
    berufe = spieler_daten.get("berufe", {})
    if not isinstance(berufe, dict):
        return False
    jaeger = berufe.get("jaeger", {})
    if not isinstance(jaeger, dict):
        return False
    aufgaben = jaeger.get("aufgaben", [])
    return (
        isinstance(aufgaben, list)
        and all(isinstance(wert, str) for wert in aufgaben)
        and "rika_grundausbildung" in aufgaben
    )


def jaeger_praxisstand(spieler_daten):
    if not jaeger_gelernt(spieler_daten):
        return None
    praxis = spieler_daten["berufe"]["jaeger"].get("praxis", [])
    if not isinstance(praxis, list) or not all(isinstance(wert, str) for wert in praxis):
        return None
    return list(praxis)


def jaeger_jagdpraxis_abschliessen(spieler_daten, gegner_typ):
    praxis_id = {"Wolf": "wolf", "Keiler": "keiler"}.get(gegner_typ) if isinstance(gegner_typ, str) else None
    praxis = jaeger_praxisstand(spieler_daten)
    if praxis_id is None or praxis is None or praxis_id in praxis:
        return False
    berufe = spieler_daten["berufe"]
    neuer_stand = dict(berufe["jaeger"])
    neuer_stand["praxis"] = praxis + [praxis_id]
    neue_berufe = dict(berufe)
    neue_berufe["jaeger"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def jaeger_beuteversorgung_gelernt(spieler_daten):
    praxis = jaeger_praxisstand(spieler_daten)
    return (
        praxis is not None and "wolf" in praxis and "keiler" in praxis
        and "rika_beuteversorgung" in spieler_daten["berufe"]["jaeger"]["aufgaben"]
    )

def jaeger_beuteversorgung_lernen(spieler_daten, *, bestaetigt=False):
    praxis = jaeger_praxisstand(spieler_daten)
    if (bestaetigt is not True or praxis is None
            or "wolf" not in praxis or "keiler" not in praxis
            or jaeger_beuteversorgung_gelernt(spieler_daten)):
        return False
    berufe = spieler_daten["berufe"]
    daten = berufe["jaeger"]
    neuer_stand = dict(daten)
    neuer_stand["aufgaben"] = daten["aufgaben"] + ["rika_beuteversorgung"]
    neue_berufe = dict(berufe)
    neue_berufe["jaeger"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def jaeger_materialbonus(spieler_daten, gegner_typ, item_id):
    if not jaeger_beuteversorgung_gelernt(spieler_daten):
        return 0
    if ((gegner_typ == "Wolf" and item_id == "wolfsfell")
            or (gegner_typ == "Keiler" and item_id == "keilerhauer")):
        return 15
    return 0


def jaeger_grundausbildung_abschliessen(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return False
    berufe = spieler_daten.get("berufe", {})
    if not isinstance(berufe, dict):
        return False
    jaeger = berufe.get("jaeger", {})
    if not isinstance(jaeger, dict):
        return False
    aufgaben = jaeger.get("aufgaben", [])
    if (not isinstance(aufgaben, list)
            or not all(isinstance(wert, str) for wert in aufgaben)
            or jaeger_gelernt(spieler_daten)
            or "stufe" in jaeger):
        return False
    neuer_stand = dict(jaeger)
    neuer_stand["stufe"] = "grundausbildung"
    neuer_stand["aufgaben"] = aufgaben + ["rika_grundausbildung"]
    neue_berufe = dict(berufe)
    neue_berufe["jaeger"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def schmied_gelernt(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return False
    berufe = spieler_daten.get("berufe", {})
    if not isinstance(berufe, dict):
        return False
    schmied = berufe.get("schmied", {})
    return (
        isinstance(schmied, dict)
        and isinstance(schmied.get("aufgaben", []), list)
        and "bjorn_grundausbildung" in schmied.get("aufgaben", [])
    )


def schmied_eigenbau_moeglich(spieler_daten):
    if not schmied_gelernt(spieler_daten):
        return False
    daten = spieler_daten["berufe"]["schmied"]
    praxis = daten.get("praxis", [])
    return (
        isinstance(praxis, list)
        and all(isinstance(wert, str) for wert in praxis)
    )


def schmied_praxis_abschliessen(spieler_daten, praxis_id):
    if praxis_id != "hauermesser" or not schmied_eigenbau_moeglich(spieler_daten):
        return False
    berufe = spieler_daten["berufe"]
    daten = berufe["schmied"]
    praxis = daten.get("praxis", [])
    if praxis_id in praxis:
        return False
    neuer_stand = dict(daten)
    neuer_stand["praxis"] = praxis + [praxis_id]
    neue_berufe = dict(berufe)
    neue_berufe["schmied"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def _waffenpflege_signatur(waffe):
    if not isinstance(waffe, dict):
        return None
    for feld in ("name", "typ"):
        if not isinstance(waffe.get(feld), str) or not waffe[feld].strip():
            return None
    zahlen = ("min_schaden", "max_schaden", "wendigkeit", "parade", "reichweite")
    if any(type(waffe.get(feld)) is not int or waffe[feld] < 0 for feld in zahlen):
        return None
    if waffe["min_schaden"] > waffe["max_schaden"]:
        return None
    return {feld: waffe[feld] for feld in ("name", "typ") + zahlen}


def _schmied_waffenpflegestand(spieler_daten):
    if (not schmied_eigenbau_moeglich(spieler_daten)
            or spieler_daten.get("prolog_status") != "prolog_abgeschlossen"):
        return None
    daten = spieler_daten["berufe"]["schmied"]
    aufgaben = daten.get("aufgaben", [])
    if (not all(isinstance(wert, str) for wert in aufgaben)
            or "hauermesser" not in daten.get("praxis", [])
            or ("waffenpflege_waffe" in daten
                and _waffenpflege_signatur(daten["waffenpflege_waffe"]) is None)):
        return None
    return daten


def schmied_waffenpflege_gelernt(spieler_daten):
    daten = _schmied_waffenpflegestand(spieler_daten)
    return daten is not None and "bjorn_waffenpflege" in daten.get("aufgaben", [])


def schmied_waffenpflege_lernen(spieler_daten, *, bestaetigt=False):
    daten = _schmied_waffenpflegestand(spieler_daten)
    if bestaetigt is not True or daten is None or schmied_waffenpflege_gelernt(spieler_daten):
        return False
    neuer_stand = dict(daten)
    neuer_stand["aufgaben"] = daten.get("aufgaben", []) + ["bjorn_waffenpflege"]
    neue_berufe = dict(spieler_daten["berufe"])
    neue_berufe["schmied"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def schmied_waffenpflege_bereit(spieler_daten):
    if not schmied_waffenpflege_gelernt(spieler_daten):
        return None
    waffe = spieler_daten["berufe"]["schmied"].get("waffenpflege_waffe")
    return waffe["name"] if waffe is not None else None


def schmied_waffenpflege_vorbereiten(spieler_daten, *, bestaetigt=False):
    if (bestaetigt is not True or not schmied_waffenpflege_gelernt(spieler_daten)
            or schmied_waffenpflege_bereit(spieler_daten) is not None):
        return False
    waffe = _waffenpflege_signatur(spieler_daten.get("waffe"))
    gold = spieler_daten.get("gold")
    if waffe is None or type(gold) is not int or gold < 2:
        return False
    neuer_stand = dict(spieler_daten["berufe"]["schmied"])
    neuer_stand["waffenpflege_waffe"] = waffe
    neue_berufe = dict(spieler_daten["berufe"])
    neue_berufe["schmied"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    spieler_daten["gold"] = gold - 2
    return True


def schmied_waffenpflege_kampfbonus(spieler_daten, waffe):
    if schmied_waffenpflege_bereit(spieler_daten) is None:
        return False
    vorbereitet = spieler_daten["berufe"]["schmied"]["waffenpflege_waffe"]
    return _waffenpflege_signatur(waffe) == _waffenpflege_signatur(vorbereitet)


def schmied_waffenpflege_beenden(spieler_daten):
    if schmied_waffenpflege_bereit(spieler_daten) is None:
        return False
    neuer_stand = dict(spieler_daten["berufe"]["schmied"])
    del neuer_stand["waffenpflege_waffe"]
    neue_berufe = dict(spieler_daten["berufe"])
    neue_berufe["schmied"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True


def schmied_grundausbildung_abschliessen(spieler_daten):
    if not isinstance(spieler_daten, dict):
        return False
    berufe = spieler_daten.get("berufe", {})
    if not isinstance(berufe, dict):
        return False
    schmied = berufe.get("schmied", {})
    if not isinstance(schmied, dict):
        return False
    aufgaben = schmied.get("aufgaben", [])
    if (not isinstance(aufgaben, list)
            or not all(isinstance(wert, str) for wert in aufgaben)
            or schmied_gelernt(spieler_daten)
            or "stufe" in schmied):
        return False
    neuer_stand = dict(schmied)
    neuer_stand["stufe"] = "grundausbildung"
    neuer_stand["aufgaben"] = aufgaben + ["bjorn_grundausbildung"]
    neue_berufe = dict(berufe)
    neue_berufe["schmied"] = neuer_stand
    spieler_daten["berufe"] = neue_berufe
    return True