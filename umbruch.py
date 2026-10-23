"""Wortumbruch für die Web-Fassung: bricht Zeilen an Wortgrenzen um, auch beim Schreibmaschinen-Effekt.

Läuft ein Wort über den Rand, wird es mit ANSI-Steuerzeichen zurückgenommen und in der nächsten Zeile
neu geschrieben. Farbcodes zählen nicht zur Breite.
"""
import io


class Umbruch(io.TextIOBase):
    def __init__(self, ziel, breite):
        self.ziel = ziel
        self.breite = breite      # Funktion, liefert die aktuelle Spaltenzahl
        self.spalte = 0
        self.wort = ""            # Rohtext des laufenden Worts (inkl. Farbcodes)
        self.wort_laenge = 0      # sichtbare Zeichen im laufenden Wort
        self.esc = ""             # angefangene Steuersequenz

    def writable(self):
        return True

    def isatty(self):
        return True

    def write(self, text):
        raus = []
        grenze = max(20, self.breite() - 1)
        for z in text:
            if self.esc:
                self.esc += z
                if len(self.esc) > 1 and (z.isalpha() or z == "~"):
                    raus.append(self.esc)
                    if self.wort:
                        self.wort += self.esc
                    if z in "HJ":
                        self.spalte = 0
                        self.wort, self.wort_laenge = "", 0
                    self.esc = ""
                continue
            if z == "\x1b":
                self.esc = z
                continue
            if z in "\n\r":
                raus.append(z)
                self.spalte = 0
                self.wort, self.wort_laenge = "", 0
                continue
            if z == " ":
                self.wort, self.wort_laenge = "", 0
                if self.spalte >= grenze:
                    raus.append("\n")
                    self.spalte = 0
                else:
                    raus.append(z)
                    self.spalte += 1
                continue
            if self.spalte >= grenze:
                if 0 < self.wort_laenge < grenze:
                    # Wort zurücknehmen und in die nächste Zeile setzen.
                    raus.append(f"\x1b[{self.wort_laenge}D\x1b[K\n{self.wort}")
                    self.spalte = self.wort_laenge
                else:
                    raus.append("\n")
                    self.spalte = 0
            raus.append(z)
            self.wort += z
            self.wort_laenge += 1
            self.spalte += 1
        if raus:
            self.ziel.write("".join(raus))
        return len(text)

    def flush(self):
        self.ziel.flush()
