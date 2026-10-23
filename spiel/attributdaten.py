ATTRIBUT_DEFINITIONEN = {
    "koerper": {
        "name": "Körper",
        "startwert": 1
    },

    "geist": {
        "name": "Geist",
        "startwert": 1
    },

    "uebersinnliches": {
        "name": "Übersinnliches",
        "startwert": 0
    }
}


VERFASSUNG_DEFINITIONEN = {
    # Körper
    "staerke": {
        "name": "Stärke",
        "attribut": "koerper"
    },

    "ausdauer": {
        "name": "Ausdauer",
        "attribut": "koerper"
    },

    "geschick": {
        "name": "Geschick",
        "attribut": "koerper"
    },

    "zaehigkeit": {
        "name": "Zähigkeit",
        "attribut": "koerper"
    },

    # Geist
    "wissen": {
        "name": "Wissen",
        "attribut": "geist"
    },

    "wahrnehmung": {
        "name": "Wahrnehmung",
        "attribut": "geist"
    },

    "willenskraft": {
        "name": "Willenskraft",
        "attribut": "geist"
    },

    "empathie": {
        "name": "Empathie",
        "attribut": "geist"
    },

    # Übersinnliches
    "sensibilitaet": {
        "name": "Sensibilität",
        "attribut": "uebersinnliches"
    },

    "resonanz": {
        "name": "Resonanz",
        "attribut": "uebersinnliches"
    },

    "kontrolle": {
        "name": "Kontrolle",
        "attribut": "uebersinnliches"
    },

    "anker": {
        "name": "Anker",
        "attribut": "uebersinnliches"
    }
}

AKT1_LERNQUELLEN = {
    # -------------------------
    # KÖRPER
    # -------------------------

    "holzsuche": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "staerke": 1,
            "ausdauer": 1
        },
        "max_nutzungen": 2
    },

    "lagerkeller_regal": {
        "attribut": "koerper",
        "menge": 2,
        "praegungen": {
            "staerke": 2
        }
    },

    "lagerkeller_geschick": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "geschick": 2
        }
    },

    "alte_schmiede_aufbrechen": {
        "attribut": "koerper",
        "menge": 2,
        "praegungen": {
            "staerke": 2
        }
    },

    "bjorn_schmiedetechnik": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "staerke": 2
        }
    },

    "joris_zeitgefuehl": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "ausdauer": 1
        }
    },

    "reise_koehlerei": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "ausdauer": 1
        }
    },

    "reise_koenigsring": {
        "attribut": "koerper",
        "menge": 2,
        "praegungen": {
            "ausdauer": 2
        }
    },

    "reise_pfad_des_vergessens": {
        "attribut": "koerper",
        "menge": 3,
        "praegungen": {
            "ausdauer": 2,
            "zaehigkeit": 1
        }
    },

    "reise_faden_der_erinnerung": {
        "attribut": "koerper",
        "menge": 2,
        "praegungen": {
            "ausdauer": 2
        }
    },

    "kampf_erfahrung": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "zaehigkeit": 1
        },
        "max_nutzungen": 3
    },

    "wald_unterholz_zaehigkeit": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "zaehigkeit": 2
        }
    },

    "wald_steinstufen_geschick": {
        "attribut": "koerper",
        "menge": 1,
        "praegungen": {
            "geschick": 2
        }
    },

    "waldwaechter_koerper": {
        "attribut": "koerper",
        "menge": 2,
        "praegungen": {
            "zaehigkeit": 2
        }
    },

    # -------------------------
    # GEIST
    # -------------------------

    "lagerkeller_hebel": {
        "attribut": "geist",
        "menge": 2,
        "praegungen": {
            "wahrnehmung": 1,
            "wissen": 1
        }
    },

    "alte_schmiede": {
        "attribut": "geist",
        "menge": 3,
        "praegungen": {
            "wissen": 3
        }
    },

    "unbekanntes_fragment": {
        "attribut": "geist",
        "menge": 2,
        "praegungen": {
            "wahrnehmung": 2
        }
    },

    "wegstation_register": {
        "attribut": "geist",
        "menge": 2,
        "praegungen": {
            "wissen": 2
        }
    },

    "wegstation_archiv": {
        "attribut": "geist",
        "menge": 2,
        "praegungen": {
            "wissen": 1,
            "wahrnehmung": 1
        }
    },

    "wegstation_kartenvergleich": {
        "attribut": "geist",
        "menge": 3,
        "praegungen": {
            "wissen": 2,
            "wahrnehmung": 1
        }
    },

    "wegstation_geheimraum": {
        "attribut": "geist",
        "menge": 2,
        "praegungen": {
            "wahrnehmung": 2
        }
    },

    "oros_messbuch_recherche": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wissen": 2
        },
        "max_nutzungen": 1
    },

    "oros_neuvermessung_vergleich": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wissen": 2
        },
        "max_nutzungen": 1
    },

    "wege_wegstein_linie": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wahrnehmung": 1,
            "wissen": 1
        },
        "max_nutzungen": 1
    },

    "wege_versunkene_steine": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wahrnehmung": 2
        },
        "max_nutzungen": 1
    },

    "oros_mauer_sensibilitaet": {
        "attribut": "uebersinnliches",
        "menge": 1,
        "praegungen": {
            "sensibilitaet": 1
        },
        "max_nutzungen": 1
    },

    "stelle_bauliste_schema": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wissen": 2
        },
        "max_nutzungen": 1
    },

    "stelle_steg_sensibilitaet": {
        "attribut": "uebersinnliches",
        "menge": 1,
        "praegungen": {
            "sensibilitaet": 1
        },
        "max_nutzungen": 1
    },

    "koehlerpfad_tierpfad": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wahrnehmung": 2
        },
        "max_nutzungen": 1
    },


    "edda_raetsel": {
        "attribut": "geist",
        "menge": 3,
        "praegungen": {
            "wissen": 1,
            "wahrnehmung": 2
        }
    },

    "edda_truhe_spuren": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wahrnehmung": 2
        }
    },

    "marek_quest": {
        "attribut": "geist",
        "menge": 3,
        "praegungen": {
            "empathie": 4,
            "wissen": 1
        }
    },

    "mara_hilda_sorge": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "empathie": 2
        }
    },

    "reise_baummarkierungen": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wahrnehmung": 1
        },
        "max_nutzungen": 1
    },


    "tomas_alte_wege": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wissen": 2
        }
    },

    "hilda_haendler_sorge": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "empathie": 2
        }
    },

    "hilda_erinnerungsanker": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "empathie": 2
        }
    },

    "sera_marek_widerspruch": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wahrnehmung": 2
        }
    },

    "marek_erinnerungsmuster": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "wahrnehmung": 1,
            "wissen": 1
        }
    },

    "elian_marek_restspuren": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "empathie": 2
        }
    },

    "waldwaechter_willenskraft": {
        "attribut": "geist",
        "menge": 1,
        "praegungen": {
            "willenskraft": 2
        }
    },

    # -------------------------
    # ÜBERSINNLICHES
    # -------------------------

    "waldwaechter_erwachen": {
        "attribut": "uebersinnliches",
        "menge": 6,
        "praegungen": {
            "sensibilitaet": 4
        }
    },

    "riss_erwachen": {
        "attribut": "uebersinnliches",
        "menge": 6,
        "praegungen": {
            "sensibilitaet": 4
        },
        "max_nutzungen": 1
    },

    "wegstein_sensibilitaet": {
        "attribut": "uebersinnliches",
        "menge": 1,
        "praegungen": {
            "sensibilitaet": 1
        }
    },

    "register_sensibilitaet": {
        "attribut": "uebersinnliches",
        "menge": 1,
        "praegungen": {
            "sensibilitaet": 1
        }
    }
}


AKT1_REISE_LERNQUELLEN = {
    frozenset(
        ("Eichenruh", "Köhlerei")
    ): "reise_koehlerei",

    frozenset(
        ("Eichenruh", "Letzthafen")
    ): "reise_koenigsring",

    frozenset(
        (
            "Eichenruh",
            "verlassenes_dorf"
        )
    ): "reise_pfad_des_vergessens",

    frozenset(
        (
            "Eichenruh",
            "universitaet_oros"
        )
    ): "reise_faden_der_erinnerung"
}