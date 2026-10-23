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

async function starten(m) {
  postMessage({ typ: "status", text: "Lade Python … (beim ersten Mal etwas länger)" });
  pyodide = await loadPyodide();
  pyodide.FS.mkdirTree("/void");
  pyodide.FS.mkdirTree("/web");
  postMessage({ typ: "status", text: "Lade VOID …" });
  for (const name of m.dateien) {
    const antwort = await fetch("../spiel/" + name, { cache: "no-cache" });
    pyodide.FS.writeFile("/void/" + name, new Uint8Array(await antwort.arrayBuffer()));
  }
  const umbruch = await fetch("../umbruch.py", { cache: "no-cache" });
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

def _hud():
    try:
        import json
        m = sys.modules["__main__"]
        s = m.spieler
        if not isinstance(s, dict):
            return
        f = m.level_fortschritt(s)
        js.hud_melden(json.dumps({
            "name": s.get("name", ""), "ort": s.get("ort", ""),
            "hp": s.get("lebenspunkte", 0), "hp_max": m.spieler_max_lebenspunkte(),
            "gold": s.get("gold", 0), "diamanten": s.get("diamanten", 0),
            "level": f["level"], "exp": f["exp_im_level"], "exp_ziel": f["aufstiegskosten"],
        }))
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
