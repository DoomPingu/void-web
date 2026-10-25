MAX_HEILTRÄNKE = 3
MAX_WUNDSALBEN = 3
MAX_GEGENGIFTE = 3



ITEMS = {
    "bandage": {
        "name": "Bandage",
        "typ": "Verbrauchsgegenstand",
        "beschreibung": (
            "Stoppt Blutungen vollständig, heilt aber keine Lebenspunkte. "
            "Im Kampf kostet die Anwendung eine Runde."
        )
    },
    "bjorns_lieferung": {
        "name": "Bjorns Lieferung",
        "typ": "Questgegenstand",
        "beschreibung": (
            "Ein schwerer Sack mit frisch geschmiedeten "
            "Keilen und Achsnägeln."
        )
    },

    "messmappe_wegstation": {
        "name": "Messmappe der Wegstation",
        "typ": "Questgegenstand",
        "beschreibung": (
            "Eine schmale Ledermappe mit Finchs Peilwerten von der alten "
            "Wegstation am Königsring."
        )
    },
    "siegelordnung": {
        "name": "Alte Siegelordnung",
        "typ": "Questgegenstand",
        "beschreibung": (
            "Eine flache Mappe aus dem Archiv von Oros. "
            "Die letzte Eintragung verzeichnet die Sperrung "
            "des alten TIEFEN-Zugangs: drei Siegel, "
            "drei Unterschriften."
        )
    },

    "laterne": {
        "name": "Laterne",
        "typ": "Questgegenstand",
        "beschreibung": (
            "Eine geschlossene Laterne aus dem Versorgungshof von Oros. "
            "Ohne Lampenöl bleibt sie dunkel."
        )
    },

    "lampenoel": {
        "name": "Lampenöl",
        "typ": "Verbrauchsgegenstand",
        "beschreibung": (
            "Eine Portion Öl für die Laterne. Sie reicht, um einen "
            "Abschnitt der TIEFEN zu beleuchten."
        )
    },

    "seil": {
        "name": "Seil",
        "typ": "Verbrauchsgegenstand",
        "beschreibung": (
            "Ein kräftiges Seil. Einmal befestigt, bleibt es an "
            "seiner Stelle hängen."
        )
    },

    "flatterhaut": {
        "name": "Flatterhaut",
        "typ": "Material",
        "beschreibung": (
            "Dünne, zähe Flughaut eines Schachtflatterers."
        )
    },

    "kriecherplatte": {
        "name": "Kriecherplatte",
        "typ": "Material",
        "beschreibung": (
            "Eine gewölbte Panzerplatte eines Schachtkriechers, "
            "leicht und hart."
        )
    },

    "molchhaut": {
        "name": "Molchhaut",
        "typ": "Material",
        "beschreibung": (
            "Bleiche, feste Haut eines Blindmolchs. Sie bleibt kühl, "
            "auch in der Hand."
        )
    },

    "gegengift": {
        "name": "Gegengift",
        "typ": "Verbrauchsgegenstand",
        "beschreibung": (
            "Ein bitterer Trank aus der Krankenstube von Oros. Entfernt "
            "Vergiftungen. Am besten trinkst du ihn, sobald du wieder Luft "
            "hast. Du kannst höchstens drei tragen."
        )
    },

    "wurfnetz": {
        "name": "Wurfnetz",
        "typ": "Kampfgegenstand",
        "beschreibung": (
            "Ein beschwertes Netz aus Netzgarn. Im Kampf einmal werfbar: "
            "Gewöhnliche Gegner verfangen sich und verlieren einen Angriff. "
            "Große reißen sich los, sind aber kurz behindert."
        )
    },

    "wundsalbe": {
        "name": "Wundsalbe",
        "typ": "Verbrauchsgegenstand",
        "heilung": 8,
        "beschreibung": (
            "Eine kühlende Salbe aus der Krankenstube von Oros. Heilt 8 "
            "Lebenspunkte und stoppt Blutungen. Du kannst höchstens drei "
            "tragen."
        )
    },

    "guerteltasche": {
        "name": "Gürteltasche",
        "typ": "Ausrüstungsverbesserung",
        "beschreibung": (
            "Eine feste Ledertasche am Gürtel. Du kannst einen Heiltrank mehr "
            "tragen (höchstens 4)."
        )
    },

    "alte_messmarke": {
        "name": "Alte Messmarke",
        "typ": "Besonderer Fund",
        "beschreibung": (
            "Ein kleines Stück aus einem Material, das du nicht kennst. "
            "In seine Oberfläche sind sorgfältig Kerben eingelassen. "
            "Gefunden in einer Wartungsnische unter dem Messgang."
        )
    },

    "mareks_routenmappe": {
        "name": "Mareks Routenmappe",
        "typ": "Reiseunterlage",
        "beschreibung": (
            "Eine robuste Ledermappe mit Mareks Notizen zum Königsring. "
            "Entfernungen, Raststellen, Steigungen und alte Wegzeichen "
            "sind sorgfältig vermerkt."
        )
    },

    "lina_wiegenlied_abschrift": {
        "name": "Abschrift von Linas Wiegenlied",
        "typ": "Aufzeichnung",
        "beschreibung": (
            "Eine saubere Abschrift des Liedblatts aus Eddas alter Truhe. "
            "Das Original bleibt bei Edda."
        ),
        "inhalt": [
            "Wenn die Laterne brennt,",
            "zieht die Möwe heim.",
            "Wenn die Welle schweigt,",
            "steigt die Sonne über den Stein."
        ]
    },

    "holz": {
        "name": "Holz",
        "typ": "Ressource",
        "beschreibung": (
            "Trockenes Holz, das sich zum Entzünden "
            "eines Lagerfeuers eignet."
        )
    },

    "apfel": {
        "name": "Apfel",
        "typ": "Nahrung",
        "beschreibung": (
            "Ein frischer Apfel. Einfach, aber nahrhaft."
        ),
        "heilung": 8
    },

    "brot": {
        "name": "Brot",
        "typ": "Nahrung",
        "beschreibung": (
            "Ein Stück kräftiges Bauernbrot aus Eichenruh."
        ),
        "heilung": 12
    },

    "karotte": {
        "name": "Karotte",
        "typ": "Nahrung",
        "beschreibung": (
            "Eine einfache frische Karotte vom Marktplatz."
        ),
        "heilung": 5
    },

    "kuechenkraeuter": {
        "name": "Küchenkräuter",
        "typ": "Zutat",
        "beschreibung": (
            "Ein kleines Bündel aromatischer Kräuter. "
            "Allein wenig sättigend, aber beim Kochen nützlich."
        )
    },


    "geroestetes_brot": {
        "name": "Geröstetes Brot",
        "typ": "Mahlzeit",
        "beschreibung": (
            "Eine warme Scheibe Brot, über dem Feuer "
            "knusprig geröstet."
        ),
        "heilung": 18
    },

    "apfelkompott": {
        "name": "Apfelkompott",
        "typ": "Mahlzeit",
        "beschreibung": (
            "Weich gekochte Äpfel. Einfach, warm "
            "und überraschend sättigend."
        ),
        "heilung": 22
    },

    "kraeuterbrot": {
        "name": "Kräuterbrot",
        "typ": "Mahlzeit",
        "beschreibung": (
            "Geröstetes Brot mit frischen Küchenkräutern. "
            "Einfach, aber deutlich besser als trockenes Brot."
        ),
        "heilung": 28,
        "status_effekte": [
            {
                "id": "geschaerfte_sinne",
                "dauer": 4,
                "einheit": "schritte"
            }
        ]
    },

    "gemuesesuppe": {
        "name": "Einfache Gemüsesuppe",
        "typ": "Mahlzeit",
        "beschreibung": (
            "Eine warme Suppe aus Karotten und Kräutern. "
            "Nichts Besonderes, aber kräftigend."
        ),
        "heilung": 30,
        "status_effekte": [
            {
                "id": "kraeftigend",
                "dauer": 3,
                "einheit": "runden"
            }
        ]
    },

    "versiegeltes_register": {
        "name": "Versiegeltes Register",
        "typ": "Besonderer Fund",
        "beschreibung": (
            "Ein ungewöhnlich gut erhaltenes Register aus einer "
            "verborgenen Kammer der alten Wegstation. "
            "Das Siegel auf dem Einband zeigt ein Zeichen, "
            "das du noch nicht einordnen kannst."
        )
    },


    "fahrtenbuch_haendler": {
        "name": "Fahrtenbuch des Händlers",
        "typ": "Besonderer Fund",
        "beschreibung": (
            "Ein abgegriffenes Fahrtenbuch aus dem verlassenen "
            "Handelskarren. Die letzten Einträge werden zunehmend "
            "unruhig und brechen schließlich mitten im Gedanken ab."
        )
    },

    "alte_wegmarke": {
        "name": "Alte Wegmarke",
        "typ": "Besonderer Fund",
        "beschreibung": (
            "Eine kleine, flache Metallscheibe mit einem "
            "fast abgeschliffenen Symbol. Du weißt nicht, "
            "wozu sie einmal gehörte."
        )
    },

    "altes_kartenstueck": {
        "name": "Altes Kartenstück",
        "typ": "Besonderer Fund",
        "beschreibung": (
            "Ein vergilbtes Stück einer alten Karte. "
            "Einige Linien und Markierungen sind noch zu erkennen, "
            "doch dir fehlt der Rest, um sie einzuordnen."
        )
    },

    "wildfleisch": {
        "name": "Rohes Wildfleisch",
        "typ": "Zutat",
        "beschreibung": (
            "Frisch gewonnenes Wildfleisch. Roh wenig einladend, "
            "aber als Grundlage für eine warme Mahlzeit geeignet."
        )
    },

    "gebratenes_wildfleisch": {
        "name": "Gebratenes Wildfleisch",
        "typ": "Mahlzeit",
        "beschreibung": (
            "Über der Glut gebratenes Wildfleisch. "
            "Einfach gewürzt wäre es besser, "
            "aber warm und sättigend ist es trotzdem."
        ),
        "heilung": 20
    },


    "wolfsfell": {
        "name": "Wolfsfell",
        "typ": "Material",
        "beschreibung": (
            "Ein raues Wolfsfell. Nicht makellos, "
            "aber für einen Gerber noch brauchbar. "
            "Bjorn kann aus drei Wolfsfellen gegen Gold "
            "eine Verstärkte Wolfslederweste herstellen."
        )
    },

    "keilerhauer": {
        "name": "Keilerhauer",
        "typ": "Material",
        "beschreibung": (
            "Ein harter, gebogener Hauer eines Keilers. "
            "Bjorn kann aus zwei Keilerhauern gegen Gold "
            "ein Hauermesser herstellen. Hilda kauft Keilerhauer an."
        )
    },


    "raeucherfleisch": {
        "name": "Räucherfleisch",
        "typ": "Mahlzeit",
        "beschreibung": (
            "Langsam über Holzkohle geräuchertes Wildfleisch. "
            "Kräftig, salzig und lange haltbar."
        ),
        "heilung": 25
    },

    "hirschgeweih": {
        "name": "Hirschgeweih",
        "typ": "Material",
        "beschreibung": (
            "Eine helle Geweihstange eines Echohirschs vom Pfad des Vergessens. "
            "Bjorn kann daraus einen Geweihtalisman fertigen."
        )
    },

    "blasses_geweih": {
        "name": "Blasses Geweih",
        "typ": "Material",
        "beschreibung": (
            "Ein fast weißes, ungewöhnlich leichtes Geweih des Blassen Hirschs. "
            "Bjorn kann daraus einen Geweihspeer schmieden."
        )
    },

    "glutkern": {
        "name": "Glutkern",
        "typ": "Material",
        "beschreibung": (
            "Ein faustgroßer, immer noch warmer Stein aus dem Inneren des Aschenkönigs. "
            "Bjorn kann daraus ein Glutbeil schmieden."
        )
    },

    "uraltschiefer": {
        "name": "Uraltschiefer",
        "typ": "Material",
        "beschreibung": (
            "Eine dunkle, schwere Steinplatte vom Rücken des Steinvaters. "
            "Bjorn kann daraus eine Steinhautweste fertigen."
        )
    },

    "riesenschere": {
        "name": "Riesenschere",
        "typ": "Material",
        "beschreibung": (
            "Die gewaltige verbliebene Schere des Einscherers. "
            "Bjorn kann daraus einen Scherenhammer schmieden."
        )
    },

    "graupelzfell": {
        "name": "Graupelzfell",
        "typ": "Material",
        "beschreibung": (
            "Das dichte, graue Fell des alten Leitwolfs von der Wildspur. "
            "Bjorn kann daraus eine Waldläuferweste fertigen."
        )
    },

    "krebsschere": {
        "name": "Krebsschere",
        "typ": "Material",
        "beschreibung": (
            "Eine schwere, gezackte Schere eines Gezeitenkrebses. "
            "Bjorn kann daraus einen Scherenarmschutz fertigen."
        )
    },

    "netzgarn": {
        "name": "Netzgarn",
        "typ": "Material",
        "beschreibung": (
            "Festes, salzverkrustetes Garn aus einem Fangnetz. "
            "Hilda kauft Netzgarn an."
        )
    },

    "schieferplatte": {
        "name": "Schieferplatte",
        "typ": "Material",
        "beschreibung": (
            "Eine flache, harte Steinplatte vom Rücken eines Schieferpanzers. "
            "Bjorn kann daraus eine Schieferweste herstellen."
        )
    },

    "kreischerfeder": {
        "name": "Kreischerfeder",
        "typ": "Material",
        "beschreibung": (
            "Eine lange, graue Schwungfeder eines Kreischers. "
            "Bjorn kann daraus ein Federamulett fertigen."
        )
    },

    "glutschuppe": {
        "name": "Glutschuppe",
        "typ": "Material",
        "beschreibung": (
            "Eine harte, rötlich schimmernde Schuppe eines Glutsalamanders. "
            "Sie hält die Wärme lange. Bjorn kann daraus mit Wolfsfell "
            "eine Schuppenweste herstellen."
        )
    },

    "holzkohle": {
        "name": "Holzkohle",
        "typ": "Material",
        "beschreibung": (
            "Leichte, schwarze Holzkohle aus den Meilern der Köhlerei. "
            "Mara räuchert damit Fleisch, die Köhler nehmen gestohlene "
            "Kohle gern zurück."
        )
    },

    "unbekanntes_fragment": {
        "name": "Unbekanntes Fragment",
        "typ": "Unbekannt",
        "beschreibung": (
            "Ein dunkles Stück Stein mit ungewöhnlich "
            "regelmäßigen Einkerbungen. "
            "Du kannst dir nicht erklären, wozu es einmal gehörte."
        )
    }
}

KAMPF_BEUTE = {
    "Schachtspinner": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "netzgarn", "chance": 50}
        ]
    },

    "Schachtflatterer": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "flatterhaut", "chance": 100}
        ]
    },

    "Schachtkriecher": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "kriecherplatte", "chance": 100}
        ]
    },

    "Blindmolch": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "molchhaut", "chance": 100}
        ]
    },

    "Bandit": {
        "gold_min": 6,
        "gold_max": 14,
        "items": []
    },

    "Wolf": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {
                "item_id": "wildfleisch",
                "min": 1,
                "max": 2,
                "chance": 100
            },
            {
                "item_id": "wolfsfell",
                "min": 1,
                "max": 1,
                "chance": 45
            }
        ]
    },

    "Glutsalamander": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {
                "item_id": "glutschuppe",
                "min": 1,
                "max": 2,
                "chance": 55
            }
        ]
    },

    "Rudelloser Wolf": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "wildfleisch", "min": 1, "max": 2, "chance": 100},
            {"item_id": "wolfsfell", "min": 1, "max": 1, "chance": 55}
        ]
    },

    "Echohirsch": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "wildfleisch", "min": 1, "max": 2, "chance": 100},
            {"item_id": "hirschgeweih", "min": 1, "max": 1, "chance": 60}
        ]
    },

    "Blasser Hirsch": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "blasses_geweih", "min": 1, "max": 1, "chance": 100},
            {"item_id": "hirschgeweih", "min": 2, "max": 2, "chance": 100}
        ]
    },

    "Aschenkönig": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "glutkern", "min": 1, "max": 1, "chance": 100},
            {"item_id": "glutschuppe", "min": 2, "max": 2, "chance": 100}
        ]
    },

    "Steinvater": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "uraltschiefer", "min": 1, "max": 1, "chance": 100},
            {"item_id": "schieferplatte", "min": 2, "max": 2, "chance": 100}
        ]
    },

    "Einscherer": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {"item_id": "riesenschere", "min": 1, "max": 1, "chance": 100},
            {"item_id": "krebsschere", "min": 1, "max": 1, "chance": 100}
        ]
    },

    "Graupelz": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {
                "item_id": "graupelzfell",
                "min": 1,
                "max": 1,
                "chance": 100
            },
            {
                "item_id": "wildfleisch",
                "min": 2,
                "max": 3,
                "chance": 100
            }
        ]
    },

    "Gezeitenkrebs": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {
                "item_id": "krebsschere",
                "min": 1,
                "max": 1,
                "chance": 55
            }
        ]
    },

    "Wrackplünderer": {
        "gold_min": 10,
        "gold_max": 18,
        "items": [
            {
                "item_id": "netzgarn",
                "min": 1,
                "max": 2,
                "chance": 70
            }
        ]
    },

    "Schieferpanzer": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {
                "item_id": "schieferplatte",
                "min": 1,
                "max": 2,
                "chance": 60
            }
        ]
    },

    "Kreischer": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {
                "item_id": "kreischerfeder",
                "min": 1,
                "max": 3,
                "chance": 70
            }
        ]
    },

    "Kohlenschmuggler": {
        "gold_min": 8,
        "gold_max": 16,
        "items": [
            {
                "item_id": "holzkohle",
                "min": 1,
                "max": 3,
                "chance": 100
            }
        ]
    },

    "Keiler": {
        "gold_min": 0,
        "gold_max": 0,
        "items": [
            {
                "item_id": "wildfleisch",
                "min": 2,
                "max": 3,
                "chance": 100
            },
            {
                "item_id": "keilerhauer",
                "min": 1,
                "max": 1,
                "chance": 60
            }
        ]
    }
}



STATUS_EFFEKTE = {
    "geschaerfte_sinne": {
        "name": "Geschärfte Sinne",
        "art": "buff",
        "beschreibung": (
            "Deine Wahrnehmung ist vorübergehend erhöht."
        ),
        "design": "positiv",
        "standard_dauer": 4,
        "standard_einheit": "schritte",
        "stapelbar": False,
        "modifikatoren": {
            "wahrnehmung": 2
        }
    },

    "kurze_rast": {
        "name": "Kurze Rast",
        "art": "buff",
        "beschreibung": (
            "Ein paar ruhige Minuten und etwas Warmes "
            "haben dir gutgetan."
        ),
        "design": "positiv",
        "standard_dauer": 2,
        "standard_einheit": "kaempfe",
        "stapelbar": False,
        "modifikatoren": {
            "kampf_wahrnehmung": 1
        }
    },


    "kraeftigend": {
        "name": "Kräftigend",
        "art": "buff",
        "beschreibung": (
            "Du fühlst dich für kurze Zeit kräftiger."
        ),
        "design": "positiv",
        "standard_dauer": 3,
        "standard_einheit": "runden",
        "stapelbar": False,
        "modifikatoren": {
            "schaden_bonus": 2
        }
    },

    "benommen": {
        "name": "Benommen",
        "art": "debuff",
        "beschreibung": (
            "Deine Sinne reagieren langsamer als gewöhnlich."
        ),
        "design": "warnung",
        "standard_dauer": 2,
        "standard_einheit": "runden",
        "stapelbar": False,
        "modifikatoren": {
            "wahrnehmung": -2
        }
    },

    "bluten": {
        "name": "Bluten",
        "art": "zustand",
        "beschreibung": (
            "Eine offene Verletzung verursacht fortlaufend Schaden."
        ),
        "design": "gefahr",
        "standard_dauer": 3,
        "standard_einheit": "runden",
        "stapelbar": True,
        "max_stapel": 3,
        "schaden_pro_tick": 2,
        "kampf_einheit": "runden",
        "nach_kampf_einheit": "schritte",
        "schaden_ausserhalb_kampf": True
    },

    "gift": {
        "name": "Vergiftet",
        "art": "zustand",
        "beschreibung": (
            "Gift wirkt in deinem Körper weiter."
        ),
        "design": "gefahr",
        "standard_dauer": 6,
        "standard_einheit": "runden",
        "stapelbar": False,
        "schaden_pro_tick": 3,
        "kampf_einheit": "runden",
        "nach_kampf_einheit": "schritte",
        "schaden_ausserhalb_kampf": True
    }
}

MARA_SORTIMENT = {
    "bandage": {
        "preis": 5
    },
    "apfel": {
        "preis": 4
    },

    "brot": {
        "preis": 6
    }
}

HILDA_MATERIAL_ANKAUF = {
    "wolfsfell": {
        "preis": 8
    },

    "keilerhauer": {
        "preis": 6
    },

    "netzgarn": {
        "preis": 6
    }
}



HILDA_SORTIMENT = {
    "karotte": {
        "preis": 3
    },

    "kuechenkraeuter": {
        "preis": 4
    }
}

REZEPTE = {
    "geroestetes_brot": {
        "name": "Geröstetes Brot",
        "zutaten": {
            "brot": 1
        },
        "ergebnis": "geroestetes_brot",
        "anzahl": 1
    },

    "apfelkompott": {
        "name": "Apfelkompott",
        "zutaten": {
            "apfel": 2
        },
        "ergebnis": "apfelkompott",
        "anzahl": 1
    },

    "kraeuterbrot": {
        "name": "Kräuterbrot",
        "zutaten": {
            "brot": 1,
            "kuechenkraeuter": 1
        },
        "ergebnis": "kraeuterbrot",
        "anzahl": 1
    },

    "gebratenes_wildfleisch": {
        "name": "Gebratenes Wildfleisch",
        "zutaten": {
            "wildfleisch": 1
        },
        "ergebnis": "gebratenes_wildfleisch",
        "anzahl": 1
    },


    "raeucherfleisch": {
        "name": "Räucherfleisch",
        "zutaten": {
            "wildfleisch": 2,
            "holzkohle": 1
        },
        "ergebnis": "raeucherfleisch",
        "anzahl": 2
    },

    "gemuesesuppe": {
        "name": "Einfache Gemüsesuppe",
        "zutaten": {
            "karotte": 2,
            "kuechenkraeuter": 1
        },
        "ergebnis": "gemuesesuppe",
        "anzahl": 1
    }
}

MENSCHEN_GEBIETE = (
    ("eichenruh", "Eichenruh und Umgebung"),
    ("oros", "Oros"),
    ("letzthafen", "Letzthafen")
)


MENSCHEN = {
    "bjorn": {
        "name": "Bjorn",
        "gebiet": "eichenruh",
        "ort": "Schmiede, Eichenruh",
        "text": "Schmied von Eichenruh. Handelt mit Waffen, stellt Ausrüstung her und bildet Krieger aus."
    },
    "mara": {
        "name": "Mara",
        "gebiet": "eichenruh",
        "ort": "Gasthaus, Eichenruh",
        "text": "Führt das Gasthaus von Eichenruh und kocht dort. Wer kochen lernen will, lernt es bei ihr."
    },
    "hilda": {
        "name": "Hilda",
        "gebiet": "eichenruh",
        "ort": "Marktplatz, Eichenruh",
        "text": "Händlerin mit eigenem Marktstand. Kauft auch Materialien an."
    },
    "tomas": {
        "name": "Tomas",
        "gebiet": "eichenruh",
        "ort": "Marktplatz, Eichenruh",
        "text": "Sitzt auf seiner Bank am Rand des Marktplatzes und kennt sich mit den alten Wegen aus."
    },
    "joris": {
        "name": "Joris",
        "gebiet": "eichenruh",
        "ort": "Eichenruh",
        "text": "Bjorns Lehrling."
    },
    "rika": {
        "name": "Rika",
        "gebiet": "eichenruh",
        "ort": "Köhlerei",
        "text": "Hält die Wege für die Köhler im Blick und jagt für sie. Bildet Späher und Jäger aus."
    },
    "finch": {
        "name": "Alistair Finch",
        "gebiet": "oros",
        "ort": "Lehrhallen, Oros",
        "text": "Professor an der Universität von Oros."
    },
    "selene": {
        "name": "Selene",
        "gebiet": "oros",
        "ort": "Lehrhallen, Oros",
        "text": "Magistra an der Universität von Oros. Bildet Magier aus."
    },
    "mira": {
        "name": "Mira",
        "gebiet": "oros",
        "ort": "Lehrhallen, Oros",
        "text": "Dozentin an der Universität von Oros. Bildet Gelehrte aus."
    },
    "valerie": {
        "name": "Valerie Vance",
        "gebiet": "oros",
        "ort": "Forschungsräume, Oros",
        "text": "Forscht zu Archäologie, Materialanalyse und allem, was irgendwann ausgegraben wurde."
    },
    "ignaz": {
        "name": "Ignaz",
        "gebiet": "oros",
        "ort": "Archiv, Oros",
        "text": "Arbeitet im Archiv von Oros. Bewahrt auch auf, wovon niemand mehr weiß, warum es wichtig war."
    },
    "levin": {
        "name": "Levin",
        "gebiet": "oros",
        "ort": "Archiv, Oros",
        "text": "Hilft Ignaz mit den Verzeichnissen im Archiv."
    },
    "ida": {
        "name": "Ida",
        "gebiet": "oros",
        "ort": "Krankenstube, Oros",
        "text": "Levins Schwester. Hilft in der Krankenstube."
    },
    "raban": {
        "name": "Raban",
        "gebiet": "oros",
        "ort": "Versorgungshof, Oros",
        "text": "Prüft im Versorgungshof Frachtblätter und Lieferungen und führt ein eigenes Lager."
    },
    "sera": {
        "name": "Sera",
        "gebiet": "letzthafen",
        "ort": "Zum letzten Licht, Letzthafen",
        "text": "Wirtin im Gasthaus „Zum letzten Licht“. Schreibt auf, was in einem Hafen sonst Streit gibt."
    },
    "marek": {
        "name": "Marek",
        "gebiet": "letzthafen",
        "ort": "Hafen, Letzthafen",
        "text": "Kennt die Knoten am Hafen besser als die Namen der Menschen dort."
    },
    "elian": {
        "name": "Elian",
        "gebiet": "letzthafen",
        "ort": "Bootswerkstatt, Letzthafen",
        "text": "Baut Boote in der Werkstatt mit den grünen Türen. Mareks Bruder."
    },
    "edda": {
        "name": "Edda",
        "gebiet": "letzthafen",
        "ort": "Haus mit der blauen Tür, Letzthafen",
        "text": "Ältere Frau, deren wortloses Summen der Wind bis weit hinaus trägt."
    },
    "nela": {
        "name": "Nela",
        "gebiet": "letzthafen",
        "ort": "Oberer Steg, Letzthafen",
        "text": "Bei ihr hat Marek fünf Winter unter dem Dach gewohnt."
    }
}


SAMMLUNGEN = {
    "orte_eichenruh": {
        "name": "Eichenruh und Umgebung",
        "eintraege": [
            ("ort_eichenruh", "Eichenruh"),
            ("ort_gasthaus", "Gasthaus"),
            ("ort_schmiede", "Bjorns Schmiede"),
            ("ort_marktplatz", "Marktplatz"),
            ("ort_wald", "Wald"),
            ("ort_wildspur", "Wildspur"),
            ("ort_wegstein", "Alter Wegstein"),
            ("ort_versunkene_steine", "Versunkene Steine"),
            ("ort_wegstation", "Alte Wegstation"),
            ("ort_lichtung", "Stille Lichtung"),
            ("ort_koehlerei", "Köhlerei"),
            ("ort_alter_koehlerpfad", "Alter Köhlerpfad"),
            ("ort_brandschneise", "Brandschneise"),
            ("ort_verlassenes_dorf", "Verlassenes Dorf"),
            ("ort_alte_schmiede", "Alte Schmiede")
        ]
    },

    "orte_oros": {
        "name": "Oros",
        "eintraege": [
            ("ort_oros", "Universität von Oros"),
            ("ort_oros_halle", "Zentrale Halle"),
            ("ort_oros_lehrhallen", "Lehrhallen"),
            ("ort_oros_forschung", "Forschungsräume"),
            ("ort_oros_archiv", "Archiv"),
            ("ort_felsterrassen", "Felsterrassen")
        ]
    },

    "orte_letzthafen": {
        "name": "Letzthafen",
        "eintraege": [
            ("ort_letzthafen", "Letzthafen"),
            ("ort_letztes_licht", "Zum letzten Licht"),
            ("ort_elian_werkstatt", "Bootswerkstatt"),
            ("ort_gezeitensteg", "Gezeitensteg"),
            ("ort_haus_der_listen", "Haus der Listen"),
            ("ort_namenstein", "Namenstein"),
            ("ort_edda_haus", "Eddas Haus"),
            ("ort_altes_leuchtfeuer", "Altes Leuchtfeuer"),
            ("ort_klippenweg", "Klippenweg"),
            ("ort_wrackstrand", "Wrackstrand")
        ]
    },

    "wege": {
        "name": "Wege",
        "eintraege": [
            ("weg_koenigsring", "Königsring"),
            ("weg_alter_seitenpfad", "Alter Seitenpfad"),
            ("weg_pfad_des_vergessens", "Pfad des Vergessens"),
            ("weg_faden_der_erinnerung", "Faden der Erinnerung")
        ]
    },

    "materialien": {
        "name": "Materialien",
        "eintraege": [
            ("holz", "Holz"),
            ("wolfsfell", "Wolfsfell"),
            ("keilerhauer", "Keilerhauer"),
            ("glutschuppe", "Glutschuppe"),
            ("holzkohle", "Holzkohle"),
            ("schieferplatte", "Schieferplatte"),
            ("kreischerfeder", "Kreischerfeder"),
            ("krebsschere", "Krebsschere"),
            ("netzgarn", "Netzgarn"),
            ("graupelzfell", "Graupelzfell"),
            ("glutkern", "Glutkern"),
            ("uraltschiefer", "Uraltschiefer"),
            ("riesenschere", "Riesenschere"),
            ("hirschgeweih", "Hirschgeweih"),
            ("blasses_geweih", "Blasses Geweih"),
            ("flatterhaut", "Flatterhaut"),
            ("kriecherplatte", "Kriecherplatte"),
            ("molchhaut", "Molchhaut")
        ]
    },

    "handwerk": {
        "name": "Handwerk",
        "eintraege": [
            ("Verstärktes Jagdbeil", "Verstärktes Jagdbeil"),
            ("Verstärkter Wanderstab", "Verstärkter Wanderstab"),
            ("Einfacher Speer", "Einfacher Speer"),
            ("Hauermesser", "Hauermesser"),
            ("verstaerkte_wolfslederweste", "Verstärkte Wolfslederweste"),
            ("leichte_jaegerweste", "Leichte Jägerweste"),
            ("schuppenweste", "Schuppenweste"),
            ("schieferweste", "Schieferweste"),
            ("spurenleser_amulett", "Spurenleser-Amulett"),
            ("ring_der_standfestigkeit", "Ring der Standfestigkeit"),
            ("federamulett", "Federamulett"),
            ("scherenarmschutz", "Scherenarmschutz"),
            ("waldlaeuferweste", "Waldläuferweste"),
            ("Glutbeil", "Glutbeil"),
            ("steinhautweste", "Steinhautweste"),
            ("Scherenhammer", "Scherenhammer"),
            ("geweihtalisman", "Geweihtalisman"),
            ("Geweihspeer", "Geweihspeer"),
            ("plattenweste", "Plattenweste"),
            ("flatterhautbinde", "Flatterhautbinde")
        ]
    }
}

REZEPT_SAMMLUNGEN = {
    "koehlerei": {
        "name": "Rezepte der Köhlerei",
        "rezepte": [
            "raeucherfleisch"
        ]
    },

    "eichenruh": {
        "name": "Rezepte von Eichenruh",
        "rezepte": [
            "geroestetes_brot",
            "apfelkompott",
            "kraeuterbrot",
            "gemuesesuppe"
        ]
    }
}

RESSOURCEN_VORKOMMEN = {
    # Nebenstollen: Tierbestände und Fundstellen, nur echte Reiseschritte regenerieren.
    "stollen_flatterer": {"item_id": "flatterhaut", "maximum": 2, "fund_min": 1, "fund_max": 1, "regeneration_schritte": 10},
    "stollen_kriecher": {"item_id": "kriecherplatte", "maximum": 2, "fund_min": 1, "fund_max": 1, "regeneration_schritte": 10},
    "stollen_molch": {"item_id": "molchhaut", "maximum": 2, "fund_min": 1, "fund_max": 1, "regeneration_schritte": 10},
    "stollen_spinner": {"item_id": "netzgarn", "maximum": 1, "fund_min": 1, "fund_max": 1, "regeneration_schritte": 15},
    "fund_platte": {"item_id": "kriecherplatte", "maximum": 1, "fund_min": 1, "fund_max": 1, "regeneration_schritte": 20},
    "fund_haut": {"item_id": "flatterhaut", "maximum": 1, "fund_min": 1, "fund_max": 1, "regeneration_schritte": 20},
    "fund_molch": {"item_id": "molchhaut", "maximum": 1, "fund_min": 1, "fund_max": 1, "regeneration_schritte": 20},
    "wald_holz": {
        "item_id": "holz",
        "maximum": 5,
        "fund_min": 1,
        "fund_max": 2,
        "regeneration_schritte": 2
    }
}


ERFOLGE = {
    
    "wo_das_wasser_schweigt": {
        "name": "Wo das Wasser schweigt",
        "kategorie": "entdeckt",
        "verborgen": True
    },

    "immer_wieder_nach_hause": {
        "name": "Immer wieder nach Hause",
        "kategorie": "entdeckt",
        "verborgen": True
    },

    "ein_lied_das_blieb": {
        "name": "Ein Lied, das blieb",
        "kategorie": "entdeckt",
        "verborgen": True
    },

    # Geschichte
    "der_verlorene_lehrling": {
        "name": "Der verlorene Lehrling",
        "kategorie": "geschichte",
        "verborgen": False,
        "beschreibung": "Joris ist wieder zu Hause."
    },
    "was_von_einem_namen_bleibt": {
        "name": "Was von einem Namen bleibt",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Marek hat seinen Weg zurück gefunden."
    },
    "die_verschwundene_lieferung": {
        "name": "Die verschwundene Lieferung",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Hildas Händler ist gefunden."
    },
    "das_stumme_wiegenlied": {
        "name": "Das stumme Wiegenlied",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Edda hat ihr Lied wieder."
    },
    "der_schmied_des_weges": {
        "name": "Der Schmied des Weges",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Der Hammer des Weges ist bei Bjorn."
    },
    "die_stille_lichtung": {
        "name": "Die stille Lichtung",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Du hast dich dem Wächter auf der Lichtung gestellt."
    },
    "der_faden_nach_oros": {
        "name": "Der Faden nach Oros",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Die Universität von Oros erreicht."
    },
    "ein_name_auf_der_liste": {
        "name": "Ein Name auf der Liste",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Du hast über Levins Namen entschieden."
    },
    "zeichen_ohne_namen": {
        "name": "Zeichen ohne Namen",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Hammer und Register tragen dasselbe alte Zeichen."
    },
    "messreihe_vier": {
        "name": "Messreihe IV",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Das alte Messbuch in den Lehrhallen gefunden."
    },

    # Eigener Weg
    "eine_eigene_richtung": {
        "name": "Eine eigene Richtung",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Eine Grundklasse gewählt."
    },
    "bestienjaeger": {
        "name": "Bestienjäger",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Rikas Prüfung bestanden."
    },
    "stahlkrieger": {
        "name": "Stahlkrieger",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Bjorns Prüfung bestanden."
    },
    "glutkrieger": {
        "name": "Glutkrieger",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Maras Prüfung bestanden."
    },
    "am_herd": {
        "name": "Am Herd",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Bei Mara den Beruf Koch gelernt."
    },
    "auf_der_faehrte": {
        "name": "Auf der Fährte",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Bei Rika den Beruf Jäger gelernt."
    },
    "am_amboss": {
        "name": "Am Amboss",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Bei Bjorn den Beruf Schmied gelernt."
    },
    "eigene_haende": {
        "name": "Eigene Hände",
        "kategorie": "weg",
        "verborgen": False,
        "beschreibung": "Ein Ausrüstungsstück aus selbst gejagtem Material besessen."
    },

    # Jagd
    "asche_und_glut": {
        "name": "Asche und Glut",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Eine Glutschuppe erbeutet."
    },
    "gestohlene_kohle": {
        "name": "Gestohlene Kohle",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Einem Kohlenschmuggler die Beute abgenommen."
    },
    "volles_jagdbuch": {
        "name": "Volles Jagdbuch",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Jeden Gegner im Jagdbuch eingetragen."
    },
    "kenne_deine_beute": {
        "name": "Kenne deine Beute",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Jedes Verhalten im Jagdbuch beobachtet."
    },
    "gebrochener_stein": {
        "name": "Gebrochener Stein",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Den Panzer eines Schieferpanzers gebrochen."
    },
    "aus_der_luft_geholt": {
        "name": "Aus der Luft geholt",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Einem Kreischer Federn abgenommen."
    },
    "aus_der_schere_befreit": {
        "name": "Aus der Schere befreit",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Dich aus der Schere eines Gezeitenkrebses losgerissen."
    },
    "gnade_am_strand": {
        "name": "Gnade am Strand",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Einen Wrackplünderer laufen lassen."
    },
    "der_alte_leitwolf": {
        "name": "Der alte Leitwolf",
        "kategorie": "jagd",
        "verborgen": True,
        "beschreibung": "Graupelz auf der Wildspur besiegt."
    },
    "asche_zu_asche": {
        "name": "Asche zu Asche",
        "kategorie": "jagd",
        "verborgen": True,
        "beschreibung": "Den Aschenkönig in der Brandschneise besiegt."
    },
    "aelter_als_stein": {
        "name": "Älter als Stein",
        "kategorie": "jagd",
        "verborgen": True,
        "beschreibung": "Den Steinvater auf den Felsterrassen besiegt."
    },
    "die_eine_schere": {
        "name": "Die eine Schere",
        "kategorie": "jagd",
        "verborgen": True,
        "beschreibung": "Den Einscherer am Wrackstrand besiegt."
    },
    "herr_der_reviere": {
        "name": "Herr der Reviere",
        "kategorie": "jagd",
        "verborgen": True,
        "beschreibung": "Alle Revierherren besiegt."
    },
    "ein_vergessener_zweck": {
        "name": "Ein vergessener Zweck",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Herausgefunden, dass IV-C nie aufgegeben wurde."
    },
    "das_echte_tier": {
        "name": "Das echte Tier",
        "kategorie": "jagd",
        "verborgen": False,
        "beschreibung": "Im Nebel den echten Echohirsch erkannt."
    },
    "der_blasse": {
        "name": "Der Blasse",
        "kategorie": "jagd",
        "verborgen": True,
        "beschreibung": "Den Blassen Hirsch am Pfad des Vergessens besiegt."
    },
    "bekannte_gesichter": {
        "name": "Bekannte Gesichter",
        "kategorie": "geschichte",
        "verborgen": True,
        "beschreibung": "Alle Menschen im Verzeichnis kennengelernt."
    }
}


JAGDBUCH = {
    "Schachtspinner": {
        "beschreibung": "Lebt in der Geröllkammer der alten Nebenstollen. Sein Biss kann vergiften.",
        "verhalten": {
            "spinner_gift": "Giftbiss: Ein Treffer kann vergiften. Das Gift wirkt nach dem Kampf weiter."
        },
        "beute": "Netzgarn."
    },
    "Schachtflatterer": {
        "beschreibung": "Hängt in alten Schächten unter Oros. Schnell und schwer zu treffen; Laternenlicht blendet ihn.",
        "verhalten": {},
        "beute": "Flatterhaut."
    },
    "Schachtkriecher": {
        "beschreibung": "Eine Assel, groß wie ein Hund. Liegt zwischen Trümmern und sieht aus wie einer.",
        "verhalten": {
            "panzer_einrollen": "Rollt sich ein: Wuchtige Schläge prallen ab, schnelle Stiche treffen die Lücken.",
            "panzer_bruch": "Schwere Schläge oder ein Hammer brechen den Panzer. Danach ist er verwundbar."
        },
        "beute": "Kriecherplatte."
    },
    "Blindmolch": {
        "beschreibung": "Blind und bleich. Folgt Geräuschen, nicht dem Licht; Dunkelheit stört ihn nicht.",
        "verhalten": {
            "molch_lauschen": "Hält still und lauscht: Dann schnappt er zu. Abwehren lohnt sich."
        },
        "beute": "Molchhaut."
    },
    "Wolf": {
        "beschreibung": "Schnell und aufmerksam. Jagt auf der Wildspur und an Waldwegen.",
        "verhalten": {
            "wolf_sprung": "Umkreist dich und duckt sich: Danach springt er. Abwehren oder mit dem Speer abfangen."
        },
        "beute": "Wildfleisch, manchmal ein Wolfsfell."
    },
    "Keiler": {
        "beschreibung": "Schwer und zäh. Lebt auf der Wildspur.",
        "verhalten": {
            "keiler_ansturm": "Scharrt mit den Hufen: Danach stürmt er. Ausweichen, abfangen oder verteidigen; nach dem Ansturm braucht er eine Runde."
        },
        "beute": "Viel Wildfleisch, manchmal ein Keilerhauer."
    },
    "Bandit": {
        "beschreibung": "Ein Mensch mit Dolch, der von Reisenden lebt.",
        "verhalten": {
            "bandit_hieb": "Holt weit aus: Ein schwerer Hieb folgt. Blockieren lohnt sich."
        },
        "beute": "Etwas Gold."
    },
    "Glutsalamander": {
        "beschreibung": "Lebt in der warmen Asche der Brandschneise hinter der Köhlerei.",
        "verhalten": {
            "salamander_gluehen": "Glühende Haut: Nahkampf verbrennt dich. Speer oder Stab halten ihn auf Abstand.",
            "salamander_eingraben": "Verschwindet in der Asche: Abwarten und verteidigen, nicht blind zuschlagen."
        },
        "beute": "Manchmal Glutschuppen."
    },
    "Kohlenschmuggler": {
        "beschreibung": "Stiehlt den Köhlern Kohle und versteckt sich in der Brandschneise.",
        "verhalten": {
            "schmuggler_asche": "Greift in den Aschebeutel: Verteidigen, sonst trifft dich Asche in die Augen.",
            "schmuggler_flucht": "Sucht einen Ausweg: Verteidigen schneidet ihm den Weg ab, dann gibt er auf."
        },
        "beute": "Gold und gestohlene Holzkohle. Bei Flucht nur ein Teil des Goldes."
    },
    "Schieferpanzer": {
        "beschreibung": "Gedrungenes Tier mit Steinplatten auf dem Rücken. Lebt auf den Felsterrassen bei Oros.",
        "verhalten": {
            "panzer_einrollen": "Rollt sich ein: Wuchtige Schläge prallen ab, schnelle Stiche treffen die Lücken.",
            "panzer_bruch": "Schwere Schläge oder ein Hammer brechen den Panzer. Danach ist er verwundbar."
        },
        "beute": "Manchmal Schieferplatten."
    },
    "Kreischer": {
        "beschreibung": "Großer Raubvogel der Felsterrassen. Greift aus der Luft an.",
        "verhalten": {
            "kreischer_aufstieg": "Steigt auf: Nur Speer oder Stab reichen hinauf. Danach stürzt er herab; mit langer Waffe abfangen.",
            "kreischer_schrei": "Ein schriller Schrei macht dich kurz benommen."
        },
        "beute": "Meist Kreischerfedern."
    },
    "Gezeitenkrebs": {
        "beschreibung": "Krebs von der Größe eines Hundes. Lebt zwischen Wrackteilen am Strand unter den Klippen von Letzthafen.",
        "verhalten": {
            "krebs_packen": "Öffnet die Schere weit: Verteidigen weicht aus, sonst hält er dich fest.",
            "krebs_losreissen": "Festgehalten: Verteidigen reißt dich los, ein Messer sticht durch die Schere."
        },
        "beute": "Manchmal eine Krebsschere."
    },
    "Wrackplünderer": {
        "beschreibung": "Sucht am Wrackstrand nach Strandgut und überfällt, wer ihm in die Quere kommt.",
        "verhalten": {
            "netz_wurf": "Wirbelt ein Fangnetz: Verteidigen duckt dich weg, sonst verlierst du eine Runde. Ein Messer schneidet dich frei.",
            "pluenderer_gnade": "Bittet am Ende um Gnade: Verteidigen lässt ihn gehen, er lässt seinen Geldbeutel da."
        },
        "beute": "Gold und Netzgarn. Wer ihn gehen lässt, bekommt nur das Gold."
    },
    "Graupelz": {
        "beschreibung": "Alter, narbiger Leitwolf der Wildspur. Zeigt sich nur selten.",
        "verhalten": {
            "graupelz_sprung": "Duckt sich tief: Danach springt er mit voller Wucht. Ein Speer fängt den Sprung ab.",
            "graupelz_heulen": "Verletzt heult er sein Rudel herbei. Verteidigen hält die Wölfe auf Abstand."
        },
        "beute": "Sein Fell und Wildfleisch."
    },
    "Rudelloser Wolf": {
        "beschreibung": "Ein einzelner Wolf ohne Rudel. Streift am Pfad des Vergessens umher und verhält sich anders als andere Wölfe.",
        "verhalten": {
            "rudellos_sprung": "Springt ohne sichtbare Vorwarnung. Wer ihn spürt, kann rechtzeitig ausweichen."
        },
        "beute": "Wildfleisch, oft ein Wolfsfell."
    },
    "Echohirsch": {
        "beschreibung": "Ein heller Hirsch im Nebel am Pfad des Vergessens. Man sieht ihn doppelt.",
        "verhalten": {
            "hirsch_echo": "Nur eine der Gestalten ist echt. Angriffe auf die falsche gehen ins Leere.",
            "echo_erkannt": "Wer abwartet und beobachtet, erkennt den echten Hirsch."
        },
        "beute": "Wildfleisch, manchmal ein Hirschgeweih."
    },
    "Blasser Hirsch": {
        "beschreibung": "Ein fast weißer, riesiger Hirsch am Pfad des Vergessens. Zeigt sich nur selten, und nie allein.",
        "verhalten": {
            "hirsch_echo": "Steht dreifach im Nebel. Angriffe treffen oft nur ein Echo.",
            "echo_erkannt": "Abwarten zeigt den echten. Die Gestalten verschieben sich aber immer wieder."
        },
        "beute": "Ein Blasses Geweih und Hirschgeweihe."
    },
    "Aschenkönig": {
        "beschreibung": "Riesiger Glutsalamander, der tief in der Asche der Brandschneise lebt. Zeigt sich nur selten.",
        "verhalten": {
            "salamander_gluehen": "Glüht, und ab der Hälfte seiner Kraft ununterbrochen: Speer oder Stab halten ihn auf Abstand.",
            "salamander_eingraben": "Gräbt sich oft in die Asche: abwarten und verteidigen."
        },
        "beute": "Ein Glutkern und Glutschuppen."
    },
    "Steinvater": {
        "beschreibung": "Uralter Schieferpanzer der Felsterrassen, kaum von einem Felsen zu unterscheiden. Zeigt sich nur selten.",
        "verhalten": {
            "panzer_einrollen": "Rollt sich oft ein: Wuchtige Schläge prallen ab, schnelle Stiche treffen die Lücken.",
            "panzer_bruch": "Erst drei schwere Treffer brechen seinen Panzer."
        },
        "beute": "Uraltschiefer und Schieferplatten."
    },
    "Einscherer": {
        "beschreibung": "Gewaltiger Krebs mit nur einer Schere. Haust im alten Bootswrack am Wrackstrand. Zeigt sich nur selten.",
        "verhalten": {
            "krebs_packen": "Packt oft zu und hält bis zu drei Runden fest: in der Folgerunde verteidigen.",
            "krebs_losreissen": "Losreißen ist bei ihm schwerer. Ein Messer sticht durch die Schere."
        },
        "beute": "Seine Riesenschere und eine Krebsschere."
    }
}
