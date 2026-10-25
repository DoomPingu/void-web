// VOID im Browser: das Python-Spiel läuft unverändert in Pyodide.
// Warten auf Eingaben und Pausen über JSPI (pyodide.ffi.run_sync), keine Sonder-Kopfzeilen nötig.
importScripts("https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js");

const SPEICHER = ["void_save_1.json", "void_save_2.json", "void_save_3.json", "void_settings.json"];
const dec = new TextDecoder();
const stand = {};
let pyodide;
let eingabeAuflosen = null;
let pauseAuflosen = null;
let ueberspringen = false;
let spaltenzahl = 80;

function spielstaende_melden() {
  for (const name of SPEICHER) {
    const pfad = "/void/" + name;
    if (!pyodide.FS.analyzePath(pfad).exists) {
      if (stand[name] !== undefined) {
        delete stand[name];
        postMessage({ typ: "loeschen", name });
      }
      continue;
    }
    const text = pyodide.FS.readFile(pfad, { encoding: "utf8" });
    if (stand[name] !== text) {
      stand[name] = text;
      postMessage({ typ: "speichern", name, text });
    }
  }
}

self.eingabe_abwarten = () => {
  spielstaende_melden();
  ueberspringen = false;
  postMessage({ typ: "eingabe" });
  return new Promise((ok) => { eingabeAuflosen = ok; });
};

self.pause_abwarten = (sekunden) => {
  if (ueberspringen || !(sekunden > 0)) return Promise.resolve();
  return new Promise((ok) => {
    const t = setTimeout(() => { pauseAuflosen = null; ok(); }, sekunden * 1000);
    pauseAuflosen = () => { clearTimeout(t); pauseAuflosen = null; ok(); };
  });
};
self.spalten = () => spaltenzahl;
self.hud_melden = (s) => postMessage({ typ: "hud", daten: JSON.parse(s) });
self.gegner_melden = (name) => postMessage({ typ: "gegner", name });
self.ziele_melden = (s) => postMessage({ typ: "ziele", daten: JSON.parse(s) });

async function starten(m) {
  postMessage({ typ: "status", text: "Lade Python … (beim ersten Mal etwas länger)" });
  pyodide = await loadPyodide();
  pyodide.FS.mkdirTree("/void");
  pyodide.FS.mkdirTree("/web");
  postMessage({ typ: "status", text: "Lade VOID …" });
  for (const name of m.dateien) {
    const antwort = await fetch("spiel/" + name, { cache: "no-cache" });
    pyodide.FS.writeFile("/void/" + name, new Uint8Array(await antwort.arrayBuffer()));
  }
  const umbruch = await fetch("umbruch.py", { cache: "no-cache" });
  pyodide.FS.writeFile("/web/umbruch.py", new Uint8Array(await umbruch.arrayBuffer()));
  for (const [name, text] of Object.entries(m.spielstaende || {})) {
    pyodide.FS.writeFile("/void/" + name, text, { encoding: "utf8" });
    stand[name] = text;
  }
  const raus = { write: (buf) => { postMessage({ typ: "text", text: dec.decode(buf, { stream: true }) }); return buf.length; }, isatty: true };
  pyodide.setStdout(raus);
  pyodide.setStderr(raus);
  postMessage({ typ: "status", text: "" });
  try {
    await pyodide.runPythonAsync(`
import builtins, os, sys, time, runpy, js
from pyodide.ffi import run_sync
sys.path.insert(0, "/web")
from umbruch import Umbruch
sys.stdout = Umbruch(sys.stdout, lambda: int(js.spalten()))

def _system(befehl):
    if befehl in ("clear", "cls"):
        sys.stdout.write("\\x1b[2J\\x1b[3J\\x1b[H")
        sys.stdout.flush()
    return 0

_kampf_gepatcht = []

def _kampf_patchen(m):
    # Meldet der Seite den Gegner, solange ein Kampf läuft (für das Gegnerbild).
    if _kampf_gepatcht or not hasattr(m, "kampfsystem_kampf_starten"):
        return
    _kampf_gepatcht.append(1)
    original = m.kampfsystem_kampf_starten
    def umhuellt(*a, **k):
        js.gegner_melden(str(k.get("gegner_typ") or ""))
        try:
            return original(*a, **k)
        finally:
            js.gegner_melden("")
    m.kampfsystem_kampf_starten = umhuellt

class _FertigGelesen(Exception):
    pass

_ziele_zuletzt = [None]

def _ziele(m):
    # Aktuelle Ziele aus quests() lesen, ohne etwas anzuzeigen: die Ausgabefunktionen werden kurz durch Sammler ersetzt.
    # quests() ist reine Anzeige (keine Eingaben, keine Änderungen am Spielstand).
    import json
    if not hasattr(m, "quests"):
        return
    ereignisse = []
    def fang_print(*a, **k):
        ereignisse.append(("p", " ".join(str(x) for x in a)))
    def fang_design(text, design="normal", art="menue"):
        ereignisse.append(("d", str(text), design))
    def nichts(*a, **k):
        return None
    def ende(*a, **k):
        raise _FertigGelesen()
    ersatz = {"print": fang_print, "design_text": fang_design, "text_ausgeben": fang_print, "menue_trenner": nichts,
              "ort_titel": nichts, "eingabe_menu": ende, "warte_auf_taste": ende}
    alt = {n: m.__dict__[n] for n in ersatz if n in m.__dict__}
    m.__dict__.update(ersatz)
    try:
        m.quests()
    except _FertigGelesen:
        pass
    finally:
        for n in ersatz:
            if n in alt:
                m.__dict__[n] = alt[n]
            else:
                m.__dict__.pop(n, None)
    quests = []
    aktuell = None
    for e in ereignisse:
        if e[0] == "d" and e[2] == "wichtig":
            aktuell = {"titel": e[1], "ziel": "", "fertig": False}
            quests.append(aktuell)
        elif e[0] == "d" and e[2] == "quest_abgeschlossen" and aktuell:
            aktuell["fertig"] = True
        elif e[0] == "p" and aktuell and not aktuell["ziel"] and e[1].strip().startswith("Ziel:"):
            aktuell["ziel"] = e[1].strip()[5:].strip()
    aktiv = [{"titel": q["titel"], "ziel": q["ziel"]} for q in quests if q["ziel"] and not q["fertig"]]
    s = json.dumps(aktiv, ensure_ascii=False)
    if s != _ziele_zuletzt[0]:
        _ziele_zuletzt[0] = s
        js.ziele_melden(s)

def _hud():
    try:
        import json
        m = sys.modules["__main__"]
        _kampf_patchen(m)
        s = m.spieler
        if not isinstance(s, dict):
            return
        f = m.level_fortschritt(s)
        js.hud_melden(json.dumps({
            "name": s.get("name", ""), "ort": s.get("ort", ""),
            "hp": s.get("lebenspunkte", 0), "hp_max": m.spieler_max_lebenspunkte(),
            "gold": s.get("gold", 0), "diamanten": s.get("diamanten", 0),
            "spielzeit": m.spielzeit_text() if hasattr(m, "spielzeit_text") else "",
            "level": f["level"], "exp": f["exp_im_level"], "exp_ziel": f["aufstiegskosten"],
        }))
    except Exception:
        pass
    try:
        _ziele(sys.modules["__main__"])
    except Exception:
        pass

def _input(prompt=""):
    _hud()
    sys.stdout.write(str(prompt))
    sys.stdout.flush()
    zeile = run_sync(js.eingabe_abwarten())
    sys.stdout.spalte = 0
    sys.stdout.wort, sys.stdout.wort_laenge = "", 0
    return str(zeile)

def _sleep(sekunden):
    sys.stdout.flush()
    run_sync(js.pause_abwarten(float(sekunden)))

os.system = _system
builtins.input = _input
time.sleep = _sleep
os.chdir("/void")
sys.path.insert(0, "/void")
sys.argv = ["main.py"]
try:
    runpy.run_path("/void/main.py", run_name="__main__")
except SystemExit:
    pass
`);
  } catch (err) {
    postMessage({ typ: "text", text: "\r\n[Fehler] " + err + "\r\n" });
  }
  spielstaende_melden();
  postMessage({ typ: "ende" });
}

onmessage = (e) => {
  const m = e.data;
  if (m.typ === "start") {
    spaltenzahl = m.spalten || 80;
    starten(m);
  } else if (m.typ === "spalten") {
    spaltenzahl = m.spalten;
  } else if (m.typ === "zeile") {
    if (eingabeAuflosen) {
      const ok = eingabeAuflosen;
      eingabeAuflosen = null;
      ok(m.text);
    }
  } else if (m.typ === "ueberspringen") {
    ueberspringen = true;
    if (pauseAuflosen) pauseAuflosen();
  }
};
