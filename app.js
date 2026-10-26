const statusZeile = document.getElementById("status");
const hudEl = document.getElementById("hud");
// Ladebildschirm: zeigt dieselben Statusmeldungen wie die Kopfzeile.
new MutationObserver(() => { if (statusZeile.textContent) document.getElementById("ladetext").textContent = statusZeile.textContent; })
  .observe(statusZeile, { childList: true, characterData: true, subtree: true });
const knoepfeEl = document.getElementById("knoepfe");
let leseStart = 0;
let bildschirmZeilen = () => [];
let antwort = () => {};
let anpassen = () => {};

function spielstaende() {
  const st = {};
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k.startsWith("void:")) st[k.slice(5)] = localStorage.getItem(k);
    }
  } catch (e) {}
  return st;
}

function balken(id, text, wert, max) {
  const el = hudEl.querySelector("#" + id);
  el.firstChild.style.width = (max ? Math.max(0, Math.min(100, (wert / max) * 100)) : 100) + "%";
  el.lastChild.textContent = text;
}

// Bilder liegen in bilder/ (ort_<name>.webp, gegner_<name>.webp). Fehlt eins, bleibt es beim dunklen Hintergrund.
const ORT_NAMEN = { spieler_zimmer: "spielerzimmer", alte_schmiede: "schmiede", bjorns_schmiede: "schmiede",
  tiefen_messgang: "tiefen", die_tiefen: "tiefen", oros_zentrale_halle: "oros_halle", oros_haupttor: "oros_tor",
  universitaet_von_oros: "oros_tor", brandschneise: "koehlerei", koehlerei_am_waldrand: "koehlerei",
  huette_am_waldrand: "huette", marktplatz_von_eichenruh: "marktplatz", die_alte_versorgungskehre: "versorgungskehre",
  letzthafen: "wrackstrand" };
const bildName = (s) => String(s).toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
  .replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
const fehlend = new Set();
// Welche Bilder es gibt, steht in offline.json (entsteht bei jeder Veröffentlichung). Damit entfällt das Raten der Endung
// (und die vielen 404-Anfragen); ohne die Liste wird wie früher probiert.
let BILD_ENDUNG = null;
fetch("offline.json").then((r) => r.json()).then((liste) => {
  const m = {};
  liste.filter((p) => p.startsWith("bilder/")).forEach((p) => { const f = p.slice(7), i = f.lastIndexOf("."); m[f.slice(0, i)] = f.slice(i + 1); });
  if (Object.keys(m).length) BILD_ENDUNG = m;
}).catch(() => {});
function bildLaden(name, fertig, endungen = ["webp", "jpg", "svg"]) {
  if (fehlend.has(name)) return fertig(null);
  if (BILD_ENDUNG && endungen.length > 1) {
    const e = BILD_ENDUNG[name];
    if (!e) { fehlend.add(name); return fertig(null); }
    endungen = [e];
  }
  const img = new Image();
  img.onload = () => fertig(img.src);
  img.onerror = () => {
    if (endungen.length > 1) return bildLaden(name, fertig, endungen.slice(1));
    fehlend.add(name); fertig(null);
  };
  img.src = "bilder/" + name + "." + endungen[0];
}
let aktuellerOrt = "";
// Hauptmenü und Optionen spielen die Intro-Musik; danach läuft wieder der Klang des aktuellen Ortes.
let klangOrt = "", imMenue = false;
function klangOrtSetzen(name) { klangOrt = name; if (!imMenue) Klang.ort(name); }
const MENUE_TITEL = /^\s*(VOID|OPTIONEN|NEUES SPIEL|SPIEL LADEN|SPIELSTAND L.SCHEN|TEXTGESCHWINDIGKEIT|BILDSCHIRM LEEREN|MEN.-EINGABE|SPIELERNAME-FARBE)\b/;
function menueKlang(zeilen) {
  const jetzt = zeilen.some((z) => MENUE_TITEL.test(z));
  if (jetzt === imMenue) return;
  imMenue = jetzt;
  Klang.ort(jetzt ? "intro" : (klangOrt || "intro"));
}
// Fehlt das Bild eines Ortes, zeigt ein Farbverlauf nach Gebiet statt Schwarz die Stimmung an.
const GEBIETE = [
  [/koehler|brand|boss|asche/, ["#2b1a14", "#100908"]],
  [/wald|bach|furt|unterholz|quell|lichtung|seitenpfad|wildspur|felshang|felsspalte|steinstufen|lagerplatz|wegmarke|wegstein|versunkene|schlamm|pfad|eingang/, ["#16261a", "#0a120c"]],
  [/oros|archiv|halle|vorhof|wachraum|schreibstube|keller|kammer|station|lehr/, ["#1d2430", "#0b0e14"]],
  [/tiefen|hoehle|schacht|messgang|stollen/, ["#1c1826", "#08070d"]],
  [/strand|hafen|wrack|kueste|see/, ["#14242c", "#080f13"]],
  [/schmiede|gasthaus|zimmer|huette|haus|taverne|laden/, ["#2a2018", "#0e0a07"]],
];
function gebietVerlauf(n) {
  const g = GEBIETE.find(([re]) => re.test(n));
  const f = g ? g[1] : ["#161c26", "#0b0d10"];
  return "linear-gradient(" + f[0] + ", " + f[1] + ")";
}
function hintergrundSetzen(ort) {
  const n = bildName(ort);
  if (n === aktuellerOrt) return;
  aktuellerOrt = n;
  // Erst der ganze Name, dann nur die Endstücke ("wald_bachlauf" -> "bachlauf"), dann ohne Endstücke ("wald").
  const teile = n.split("_");
  const namen = [n];
  for (let i = 1; i < teile.length; i++) namen.push(teile.slice(i).join("_"));
  for (let i = teile.length - 1; i >= 1; i--) namen.push(teile.slice(0, i).join("_"));
  const kandidaten = [...new Set(namen.map((x) => ORT_NAMEN[x] || x))];
  const versuchen = (i) => {
    if (n !== aktuellerOrt) return;
    if (i >= kandidaten.length) { klangOrtSetzen(n); return anzeigen(null); }
    bildLaden("ort_" + kandidaten[i], (src) => (src ? (klangOrtSetzen(kandidaten[i]), anzeigen(src)) : versuchen(i + 1)));
  };
  const anzeigen = (src) => {
    const el = document.getElementById("hintergrund");
    el.style.backgroundImage = src ? 'url("' + src + '")' : gebietVerlauf(n);
    el.classList.toggle("leer", !src);
  };
  versuchen(0);
}
let aktuellerGegner = "";
function gegnerSetzen(name) {
  aktuellerGegner = name;
  Klang.kampf(!!name);
  const box = document.getElementById("gegner");
  const img = box.querySelector("img");
  box.querySelector(".balken.gegner > i").style.width = "100%";
  box.querySelector(".balken.gegner > span").textContent = name;
  box.querySelector(".balken.du").style.visibility = "hidden";
  box.querySelector(".kampfchips").replaceChildren();
  kampfBlutet = false;
  if (!name) { box.style.display = "none"; anpassen(); return; }
  box.style.display = "flex";
  img.style.display = "none";
  anpassen();
  bildLaden("gegner_" + bildName(name), (src) => {
    if (name !== aktuellerGegner) return;
    if (src) { img.src = src; img.style.display = "block"; }
    anpassen();
  });
}

// Kampfzeile "Du: 80/100 HP | Wolf: 25/40 HP": Gegner-Balken oben, eigener HP-Balken während des Kampfs.
function kampfLeisteSetzen(zeilen) {
  if (!aktuellerGegner) return;
  let m = null;
  for (const z of zeilen) m = z.match(/Du:\s*(\d+)\/(\d+)\s*HP\s*\|\s*(.+?):\s*(\d+)\/(\d+)\s*HP/) || m;
  if (!m) return;
  const box = document.getElementById("gegner");
  const prozent = (a, b) => (+b ? Math.max(0, Math.min(100, (+a / +b) * 100)) : 0) + "%";
  box.querySelector(".balken.gegner > i").style.width = prozent(m[4], m[5]);
  box.querySelector(".balken.gegner > span").textContent = m[3] + " " + m[4] + " / " + m[5];
  const du = box.querySelector(".balken.du");
  du.style.visibility = "visible";
  du.querySelector("i").style.width = prozent(m[1], m[2]);
  du.querySelector("span").textContent = "Du " + m[1] + " / " + m[2];
  if (hudEl.firstChild) balken("hp", "HP " + m[1] + " / " + m[2], +m[1], +m[2]);
  // Runde und Blutung als kleine Chips.
  let runde = 0;
  for (const z of zeilen) {
    const r = z.match(/Runde\s+(\d+)/); if (r && /[─\-]{3,}/.test(z)) runde = +r[1];
    if (/Bluten ist abgeklungen|Blutung (?:ist )?(?:gestoppt|abgeklungen)/.test(z)) kampfBlutet = false;
    else if (/^\s*Bluten:|beginnst zu bluten|Du blutest/.test(z)) kampfBlutet = true;
  }
  const chips = box.querySelector(".kampfchips");
  chips.replaceChildren();
  if (runde) { const c = document.createElement("span"); c.textContent = "Runde " + runde; chips.append(c); }
  if (kampfBlutet) { const c = document.createElement("span"); c.className = "blut"; c.textContent = "🩸 Blutung"; chips.append(c); }
}
let kampfBlutet = false;

// Sprecher: letzte Zeile "[Name] ..." auf dem Bildschirm; Porträt aus bilder/npc_<name>.webp.
// Porträts aus dem Pack von Corax Digital Art (Credit-Pflicht laut Lizenz).
const NPC_AUS_PACK = new Set(["marek", "ahrens", "elian", "edda", "sera", "joris", "raban", "levin", "koehler", "rika", "schreiber", "nela", "ida", "arvid", "selene", "gerrit", "mira", "kiran", "fischer", "tarek", "runa", "enno"]);
let aktuellerNpc = "";
function npcPlatzhalter(name) {
  const farbe = sprecherFarbe(name);
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56"><circle cx="28" cy="28" r="28" fill="#1a2230"/><circle cx="28" cy="28" r="25" fill="none" stroke="' + farbe + '" stroke-width="2"/>' +
    '<text x="28" y="37" font-size="26" font-family="sans-serif" font-weight="700" text-anchor="middle" fill="' + farbe + '">' + esc(name.trim().charAt(0).toUpperCase()) + "</text></svg>";
  return "data:image/svg+xml," + encodeURIComponent(svg);
}
function npcSetzen(zeilen) {
  let name = "";
  for (const z of zeilen) {
    const m = z.match(/^\s*\[([A-Za-zÄÖÜäöü][^\]]{2,22})\]\s/);
    if (m && m[1] !== "Beliebige Taste") name = m[1];
  }
  if (name === aktuellerNpc) return;
  aktuellerNpc = name;
  const box = document.getElementById("npc");
  if (!name) { box.style.display = "none"; anpassen(); return; }
  bildLaden("npc_" + bildName(name), (src) => {
    if (name !== aktuellerNpc) return;
    // Ohne Porträt gibt es einen Platzhalter mit Anfangsbuchstabe in der Sprecherfarbe.
    const echt = !!src;
    if (!src) src = npcPlatzhalter(name);
    box.querySelector("img").src = src; box.querySelector("span").textContent = name;
    box.querySelector("#credit").style.display = echt && NPC_AUS_PACK.has(bildName(name)) ? "block" : "none";
    box.style.display = "flex";
    anpassen();
  });
}

// Tageszeit und Wetter als Symbol im Kopf. Das Spiel führt beides bisher nur als "Tag"/"Klar" (nie geändert); damit der Kopf
// nicht dauernd eine Sonne zeigt, erscheint das Symbol erst, wenn sich ein Wert vom Standard unterscheidet.
const TAGESZEIT_ICON = { tag: "☀️", nacht: "🌙", morgen: "🌅", morgens: "🌅", abend: "🌇", abends: "🌇", daemmerung: "🌆", "dämmerung": "🌆" };
const WETTER_ICON = { regen: "🌧️", nebel: "🌫️", sturm: "⛈️", gewitter: "⛈️", schnee: "❄️", wind: "💨", bewoelkt: "☁️", "bewölkt": "☁️" };
function himmelSymbol(tageszeit, wetter) {
  const t = String(tageszeit || "Tag").toLowerCase(), w = String(wetter || "Klar").toLowerCase();
  if (t === "tag" && w === "klar") return "";
  return (TAGESZEIT_ICON[t] || "") + (WETTER_ICON[w] || "");
}
// Der Hintergrund wird draußen je nach Tageszeit und Wetter getönt. Drinnen (Zimmer, Gasthaus, Schmiede, Keller, Tiefen, Oros-Hallen) bleibt er gleich.
const DRINNEN = /zimmer|gasthaus|schmiede|huette|keller|tiefen|halle|archiv|lehr|kammer|haus|station|raum/;
const TON_ZEIT = { nacht: "brightness(.5) saturate(.75) hue-rotate(8deg)", abend: "brightness(.82) sepia(.3) saturate(1.1)", morgen: "brightness(.92) sepia(.12)" };
const TON_WETTER = { regen: "brightness(.82) saturate(.8) hue-rotate(-6deg)", nebel: "brightness(.92) contrast(.82) saturate(.55)", sturm: "brightness(.7) saturate(.7)" };
function himmelTonen(d) {
  const drin = DRINNEN.test(bildName(d.ort || ""));
  const st = document.body.style;
  st.setProperty("--ton-zeit", (!drin && TON_ZEIT[String(d.tageszeit || "").toLowerCase()]) || "brightness(1)");
  st.setProperty("--ton-wetter", (!drin && TON_WETTER[String(d.wetter || "").toLowerCase()]) || "brightness(1)");
}
let statistik = null;
function hudZeigen(d) {
  statistik = d;
  himmelTonen(d);
  document.body.classList.add("imspiel");
  hudOrt = String(d.ort || "");
  spielerName = String(d.name || "");
  hintergrundSetzen(d.ort);
  if (!hudEl.firstChild) {
    hudEl.innerHTML = '<div class="zeile"><span class="ort"></span><span class="gold"></span></div>' +
      '<div class="balken" id="hp"><i></i><span></span></div><div class="balken" id="xp"><i></i><span></span></div>';
  }
  const ORT_ANZEIGE = { spieler_zimmer: "Dein Haus", alte_schmiede: "Alte Schmiede", verlassenes_dorf: "Verlassenes Dorf",
    lagerkeller: "Alter Lagerkeller", tiefen_messgang: "TIEFEN – Messgang", oros_zentrale_halle: "Oros – Zentrale Halle" };
  const ort = ORT_ANZEIGE[d.ort] || String(d.ort).replace(/_/g, " ").replace(/(^|\s)\S/g, (c) => c.toUpperCase());
  const himmel = himmelSymbol(d.tageszeit, d.wetter);
  hudEl.querySelector(".ort").textContent = (himmel ? himmel + " " : "") + d.name + " · " + ort;
  hudEl.querySelector(".gold").textContent = d.gold + " Gold" + (d.diamanten ? " · " + d.diamanten + " Diamanten" : "") + (d.spielzeit ? " · ⏱ " + d.spielzeit : "");
  balken("hp", "HP " + d.hp + " / " + d.hp_max, d.hp, d.hp_max);
  balken("xp", "Level " + d.level + " · EP " + (d.exp_ziel ? d.exp + " / " + d.exp_ziel : "Max"), d.exp, d.exp_ziel);
  hudEl.style.display = "block";
  anpassen();
}

// Liest die Auswahl aus dem Text vor dem Prompt: "1. Text" und "[S] Text".
// Passt nichts, bleibt nur das Textfeld.
// Name vor Gedankenstrich oder Klammer als Hauptzeile, der Zusatz dahinter als kleine zweite Zeile.
// Lange Beschreibungen stehen im Text darüber und kommen nicht auf den Knopf.
function knopfTeile(e) {
  let text = e.text.replace(/\s+/g, " "), detail = "", neu = false;
  if (/\s*\[!\]\s*$/.test(text)) { neu = true; text = text.replace(/\s*\[!\]\s*$/, ""); }
  const dm = text.match(/^(.*?) [-–] (.+)$/);
  if (dm) { text = dm[1]; detail = dm[2]; }
  const bm = text.match(/^(.*?)\s*\[([^\]]*)\]\s*$/);
  if (bm && bm[1]) { text = bm[1]; if (bm[2].trim() === "!") neu = true; else detail = detail || bm[2]; }
  return { text, detail, neu };
}
// Vibration bei Treffern, Level-up usw.: einmal pro Seite, nach dem Text. Funktioniert nur auf Geräten, die es können (Android).
let vibrNr = -1;
function vibrieren(text) {
  let muster = 0;
  const effekte = [];
  if (/LEVELAUFSTIEG/.test(text)) { muster = [40, 40, 40, 40, 140]; effekte.push("levelup"); }
  else if (/KAMPF GEWONNEN/.test(text)) { muster = [30, 30, 70]; effekte.push("sieg"); }
  else {
    if (/Kritischer Treffer/.test(text)) { muster = [70, 50, 70]; effekte.push("kritisch"); }
    else if (/Du triffst .{0,40}für \d+ Schaden/.test(text)) effekte.push("treffer");
    if (/Du erleidest \d+ Schaden|trifft dich|streift dich/.test(text)) { muster = muster || 45; effekte.push("schaden"); }
    if (!effekte.length && /SPIEL GESPEICHERT|Spielstand gespeichert/.test(text)) { muster = 25; effekte.push("speichern"); }
    // Ohne Kampf: Truhe, Tür, Münzen (nach dem Wortlaut der Seite; ein Effekt pro Seite).
    if (!effekte.length && !aktuellerGegner) {
      // Wortlaute aus dem Spiel: "Du hast eine kleine Truhe gefunden.", "12 Gold gefunden", "Du erhältst 12 Gold.", "Du bezahlst: 40 Gold", "Du öffnest die Tür zu …".
      if (/Truhe gefunden|geöffneten Truhe|Truhe (öffnet|springt)/.test(text)) effekte.push("truhe");
      else if (/\d+ Gold gefunden|Gefunden: \d+ Gold|Du (erhältst|bezahlst):? \d+ Gold|und \d+ Gold!/.test(text)) effekte.push("muenzen");
      else if (/Du (öffnest|drückst) die Tür|Tür öffnet sich|öffnet die Tür/.test(text)) effekte.push("tuer");
    }
  }
  if (muster && UI.vibration !== false && navigator.vibrate) { try { navigator.vibrate(muster); } catch (e) {} }
  // Effekte nacheinander, damit Treffer und Schaden nicht übereinanderliegen.
  if (typeof Klang !== "undefined" && Klang.effekt) effekte.forEach((n, i) => setTimeout(() => Klang.effekt(n), i * 300));
}
let kette = [];
const SCHNELLSPEICHERN = [
  { screen: /^\s*MEN.\s*$/, pick: /Spiel speichern/ },
  { screen: /SPIEL GESPEICHERT/, pick: "weiter" },
  { screen: /^\s*MEN.\s*$/, pick: /Weiterspielen/ }
];
const IKONEN = {
  s: { icon: "📊", name: "Status", test: /Status/ },
  i: { icon: "🎒", name: "Inventar", test: /Inventar/ },
  j: { icon: "📜", name: "Journal", test: /Quest|Journal/ },
  t: { icon: "✨", name: "Talente", test: /Talent/ },
  q: { icon: "☰", name: "Menü", test: /Speichern|Menü/ }
};
let letzteRede = false;
function knoepfeBauen() {
  document.body.classList.remove("laden");
  knoepfeEl.replaceChildren();
  const zeilen = bildschirmZeilen();
  npcSetzen(zeilen);
  kampfLeisteSetzen(zeilen);
  menueKlang(zeilen);
  if (vibrNr !== bildschirmNr) {
    vibrNr = bildschirmNr; vibrieren(zeilen.join("\n"));
    // Für Bildschirmleser: der neue Text wird einmal pro Seite angesagt.
    document.getElementById("ansage").textContent = zeilen.filter((z) => z.trim()).join(" ").slice(0, 900);
  }
  if (document.body.classList.contains("imspiel") && !aktuellerGegner && !zeilen.some((z) => /^\s*1\.\s+Neues Spiel/.test(z))) {
    if (!UI.intro) introZeigen();
    else if (UI.stand !== APP_STAND) { if (NEUES[APP_STAND]) neuesZeigen(); else { UI.stand = APP_STAND; uiSichern(); } }
  }
  const istStart = zeilen.some((z) => /^\s*1\.\s+Neues Spiel/.test(z)) && zeilen.some((z) => /^\s*\d\.\s+Beenden/.test(z));
  startSetzen(istStart);
  if (startAktion && !istStart) {
    // "Weiterspielen": im Ladebildschirm den gewählten Platz antippen.
    const platz = startAktion;
    startAktion = 0;
    if (zeilen.some((z) => /SPIEL LADEN/.test(z))) setTimeout(() => antwort(String(platz)), 0);
  }
  const nichtLeer = zeilen.filter((z) => z.trim());
  const letzte = nichtLeer.length ? nichtLeer[nichtLeer.length - 1] : "";
  let eintraege = [];
  const gesehen = new Set();
  let letzterEintrag = null;
  for (const z of zeilen) {
    const klammer = /^\s*\[/.test(z);
    // Im Kampf gibt es auch Einträge wie "F. Fokussierter Angriff".
    const m = z.match(/^\s*(\d{1,2})[.)]\s+(.+)$/) || z.match(/^\s*\[([A-Za-z])\]\s+(.+)$/)
      || (aktuellerGegner && z.match(/^\s*([A-Za-z])[.)]\s+(.+)$/));
    if (m && !gesehen.has(m[1].toLowerCase())) {
      gesehen.add(m[1].toLowerCase());
      letzterEintrag = { wert: m[1].toLowerCase(), text: m[2], sonder: klammer };
      eintraege.push(letzterEintrag);
    } else if (m) {
      letzterEintrag = null;
    } else if (letzterEintrag && z.trim() && z.trim() !== letzte.trim() && !/^\s{2,}/.test(z)) {
      // Umbruch: Zeile direkt unter einem Eintrag gehört dazu.
      letzterEintrag.text += " " + z.trim();
    } else {
      letzterEintrag = null;
    }
  }
  if (/Enter|Beliebige Taste/i.test(letzte)) {
    eintraege = [{ wert: "", text: letzte.replace(/^\[Beliebige Taste\]\s*/, "") || "Weiter", weiter: true }];
  } else if (!/[:>]\s*$/.test(letzte)) {
    // Kein Auswahl-Prompt: bei einer Frage Textfeld, sonst wartet das Spiel nur auf Enter.
    eintraege = /\?\s*$/.test(letzte) ? [] : [{ wert: "", text: "Weiter", weiter: true }];
  }
  if (istStart) eintraege = eintraege.filter((e) => !/^Beenden/.test(e.text));
  eintraege = eintraege.filter((e) => !/^Textgeschwindigkeit/.test(e.text));
  if (kette.length) {
    // Schnellspeichern: Menü → "Spiel speichern" → Weiter → "Weiterspielen".
    const schritt = kette[0];
    const e = zeilen.some((z) => schritt.screen.test(z)) && (schritt.pick === "weiter" ? eintraege.find((x) => x.weiter) : eintraege.find((x) => schritt.pick.test(x.text)));
    if (e) {
      kette.shift();
      if (schritt.screen.test("SPIEL GESPEICHERT")) { UI.gespeichert = Date.now(); uiSichern(); }
      if (!kette.length) hinweis("Spielstand gespeichert");
      setTimeout(() => antwort(e.wert), 0);
      return;
    }
    kette = [];
  }
  document.body.classList.toggle("qfrei", eintraege.some((e) => e.sonder && e.wert === "q"));
  feldSetzen(eintraege.length === 0 || (eintraege.length === 1 && !eintraege[0].weiter));
  if (raetselPruefen(zeilen, eintraege)) return;
  if (dialPruefen(eintraege)) return;
  // Die festen Kurztasten (Status, Inventar, Journal, Talente, Menü) bilden eine Icon-Leiste unter den Knöpfen.
  const ikonen = eintraege.filter((e) => e.sonder && IKONEN[e.wert] && IKONEN[e.wert].test.test(e.text));
  const normale = eintraege.filter((e) => !ikonen.includes(e));
  // Am Startbild nach hinten und dezent: "Spielstand löschen" soll man nicht aus Versehen treffen.
  const loeschen = istStart ? normale.findIndex((e) => /Spielstand l.schen/.test(e.text)) : -1;
  if (loeschen >= 0) normale.push(normale.splice(loeschen, 1)[0]);
  // Zusatzzeilen (Preis, Hinweis) nur, wenn sie bei allen Einträgen kurz genug sind. Sonst gäbe es sie nur bei einigen
  // (z. B. bei Geschick, Wahrnehmung, Empathie, aber nicht bei den anderen Veranlagungen).
  const zusatzOk = normale.every((e) => knopfTeile(e).detail.length <= 44);
  // Die Auswahlliste im Text entfällt, wenn die Knöpfe alles zeigen (Name kurz genug, Zusatz vollständig).
  listeAus = (normale.length + ikonen.length > 0) && normale.every((e) => {
    const p = knopfTeile(e);
    return !p.detail || (zusatzOk && p.detail.length <= 44);
  });
  leseNeu();
  // Gespräch: Enthält die Seite Sprecher-Zeilen "[Name] Text" (Name mit mind. 2 Zeichen, kein [S]/[Q]), erscheinen die
  // Auswahlmöglichkeiten als Sprechblasen-Antworten. Ausgenommen: Weiter, Zurück-/Abbrechen-Einträge und Kämpfe.
  // Die Antwortseite selbst enthält oft nur die Auswahl; dann gilt die Seite davor (letzteRede).
  const hatRede = zeilen.some((z) => /^\s*\[[^\]\d]{2,24}\]\s+\S/.test(z));
  const nurAuswahl = nichtLeer.every((z) => /^\s*(\d{1,2}[.)]|\[[A-Za-z]\])\s/.test(z) || /^Auswahl\b|^\s*>/.test(z) || /^\s{2,}\S/.test(z));
  const gespraech = !aktuellerGegner && !istStart && (hatRede || (letzteRede && nurAuswahl));
  letzteRede = gespraech && (hatRede || nurAuswahl);
  for (const e of normale) {
    const b = document.createElement("button");
    b.type = "button";
    const { text, detail: d0, neu } = knopfTeile(e);
    const detail = zusatzOk ? d0 : "";
    // Am Handy ohne Nummern (die braucht man nur zum Tippen im Terminal-Modus).
    const antwortBlase = gespraech && !e.weiter && !e.sonder && !/^(Nein,\s*)?(Zurück|zurück|Abbrechen|Schließen|Gespräch beenden|Verabschieden|Gehen)\b/.test(text);
    const kopf = e.weiter ? "↵ " : antwortBlase ? "💬 " : (UI.lesen ? "" : (e.sonder ? "[" + e.wert.toUpperCase() + "] " : e.wert.toUpperCase() + ". "));
    b.innerHTML = '<span class="t">' + esc(kopf + text) + (neu ? ' <b class="neu">!</b>' : "") + "</span>" + (detail ? "<small>" + esc(detail) + "</small>" : "");
    if (e.sonder || (istStart && /Spielstand l.schen/.test(e.text))) b.className = "sonder";
    // Lange Einträge (Antworten, Beschreibungen) über die ganze Breite, damit nichts abgeschnitten wird.
    if ((kopf + text).length > 28 || antwortBlase) b.classList.add("eine");
    if (antwortBlase) b.classList.add("antwort");
    b.dataset.voll = e.text.replace(/\s*\[!\]\s*$/, "");
    b.onclick = () => antwort(e.wert);
    knoepfeEl.append(b);
  }
  if (normale.length === 1) knoepfeEl.firstChild.classList.add("eine");
  if (ikonen.length) {
    const leiste = document.createElement("div");
    leiste.className = "ikonen";
    for (const e of ikonen) {
      const b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", IKONEN[e.wert].name);
      b.innerHTML = "<span>" + IKONEN[e.wert].icon + "</span><small>" + IKONEN[e.wert].name + "</small>";
      b.onclick = () => antwort(e.wert);
      leiste.append(b);
    }
    knoepfeEl.append(leiste);
  }
  knoepfeEl.classList.toggle("kampf", !!aktuellerGegner);
  knoepfeEl.style.display = eintraege.length ? "grid" : "none";
  anpassen();
}

// ---- Vorschau Paket A/B -------------------------------------------------------------
// Darstellung und Sicherung. Eigene Einstellungen liegen unter "void-ui" (nicht unter "void:", sie gehören nicht in die Sicherung).
const UI_KEY = "void-ui";
// Eingabefeld: auf dem Handy nur zeigen, wenn das Spiel Text will; am PC immer.
const UI = Object.assign({ schrift: 16, lesen: true, serif: false, farben: true, sicherung: 0,
  feld: matchMedia("(pointer: coarse)").matches ? "auto" : "immer" }, (() => {
  try { return JSON.parse(localStorage.getItem(UI_KEY)) || {}; } catch (e) { return {}; }
})());
const uiSichern = () => { try { localStorage.setItem(UI_KEY, JSON.stringify(UI)); } catch (e) {} };
let termRef = null;
let sicherungLaeuft = false;   // beim Einspielen keine Spielstände mehr aus dem laufenden Spiel übernehmen
const spaltenWert = () => (UI.lesen ? 200 : (termRef ? termRef.cols : 80));

const SPRECHER_FARBE = { Mara: "#f2b66d", Bjorn: "#e8895c", Hilda: "#e57fb0", Tomas: "#b6c27a", Joris: "#7fd0c4",
  Finch: "#8fb4e8", Valerie: "#c79cf0", Ignaz: "#d9c27a", Haller: "#e07a7a", Ahrens: "#9ac7b0", Raban: "#d0a070",
  Levin: "#a3b8e8", Sera: "#f09a8a", Marek: "#9fcf8f", Ida: "#f0a0c0", Edda: "#c0b0e0" };
function sprecherFarbe(n) {
  if (SPRECHER_FARBE[n]) return SPRECHER_FARBE[n];
  let h = 0;
  for (const c of n) h = (h * 31 + c.charCodeAt(0)) % 360;
  return "hsl(" + h + " 55% 70%)";
}
const ANSI = ["#000", "#e06c75", "#98c379", "#e5c07b", "#61afef", "#c678dd", "#56b6c2", "#d7dbe0",
  "#7d8590", "#ff7b86", "#b5e08d", "#f0d08a", "#7ec0ff", "#d996f0", "#7fd0dc", "#fff"];
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// Leseansicht: spiegelt den Terminal-Puffer als Fließtext. Das Terminal bleibt im Hintergrund die Quelle
// (Auswahl-Knöpfe, HUD, Sprecher werden weiter daraus gelesen). Tabellen und ausgerichtete Zeilen bleiben Festbreite.
let leseTimer = 0;
function leseNeu() {
  if (!UI.lesen || !termRef || leseTimer) return;
  leseTimer = setTimeout(() => { leseTimer = 0; leseRendern(); }, 60);
}
function zeilenFarbe(z) {
  // Farbe des ersten sichtbaren Zeichens (z. B. cyanfarbene Überschriften).
  const n = z.length;
  for (let x = 0; x < n; x++) {
    const c = z.getCell(x);
    if (!c || !c.getChars().trim()) continue;
    if (c.isFgPalette()) { const i = c.getFgColor(); return i < 16 && i !== 7 && i !== 15 ? ANSI[i] : ""; }
    return "";
  }
  return "";
}
// Zeilen, die in der Leseansicht entfallen: Tastenhinweise und die Option "Textgeschwindigkeit" (Texte kommen hier immer sofort).
const KV_ICON = { Gold: "🪙", Lebenspunkte: "❤️", HP: "❤️", "Heiltränke": "🧪", Fackeln: "🔥", Diamanten: "💎", Level: "⭐",
  "Besiegte Gegner": "☠️", Spielzeit: "⏱", Waffe: "⚔️", "Aktuelle Waffe": "⚔️", "Gesamt-EXP": "✨", "Freie Talentpunkte": "🌟", Name: "👤", Grundklasse: "🛡️" };
const TASTENHINWEIS =/^\s*(Mit \[?[SIJTQ]\]? (öffnest du|sicherst du)\b|Textgeschwindigkeit\s*(:|$))/;
function leseRendern() {
  const buf = termRef.buffer.active;
  const lese = document.getElementById("lese");
  const ende = buf.baseY + buf.cursorY;
  const start = leseStart;
  // Jeder Bildschirm ist eine neue Seite: nur der Text seit der letzten Antwort wird gezeigt. Ältere Seiten stehen unter "Vorheriger Text".
  const von = Math.max(start > ende ? buf.baseY : start, ende - 700);
  const zeilen = [];
  for (let y = von; y <= ende; y++) {
    const z = buf.getLine(y);
    if (!z) continue;
    const t = z.translateToString(true);
    // Tastenhinweise ("Mit T öffnest du Talente ...") sind auf dem Handy überflüssig: dort gibt es Knöpfe.
    if (!z.isWrapped && TASTENHINWEIS.test(t)) continue;
    if (z.isWrapped && zeilen.length) zeilen[zeilen.length - 1].text += t;
    else zeilen.push({ text: t, z, y });
  }
  // Steht der Tastenhinweis mitten in einer Zeile (z. B. nach "Tipp: ..."), wird nur dieser Satz entfernt (nach dem Zusammenfügen umbrochener Zeilen).
  for (let i = zeilen.length - 1; i >= 0; i--) {
    const neu = zeilen[i].text.replace(/\s*Mit \[?[SIJTQ]\]?[^.]*? (?:öffnest|sicherst) du[^.]*\./g, "");
    if (neu === zeilen[i].text) continue;
    if (neu.trim()) zeilen[i].text = neu; else zeilen.splice(i, 1);
  }
  const KV = /^[A-ZÄÖÜ][\wäöüßÄÖÜ \-]{1,28}:\s+\S.{0,56}$/;
  const kvZeile = (s) => KV.test(s) && !/[.!]$/.test(s) && !/\w\?$/.test(s);
  const art = zeilen.map(({ text: t }) => {
    if (!t.trim()) return "leer";
    if (/^\s*[=\-─]{6,}\s*$/.test(t)) return "hr";
    if (/[█╗╔╝╚║]/.test(t)) return "logo";
    if (/^\s*>\s*\S{0,3}\s*$/.test(t)) return "wahl";
    if (/^\s*Schritt\s+\d+\s*\/\s*\d+\s*$/.test(t)) return "schritt";
    if (/^(Körper|Geist|Übersinnliches)\s*\d*:\s*\S/.test(t)) return "attr";
    if (/^\s{8,}Peilskizze\s+gemessen\s*$/.test(t)) return "peilkopf";
    if (/^\s*✓\s+\S/.test(t)) return "erfolg";
    if (/^\s*\?\s+\?\?\?\s*$/.test(t)) return "gesperrt";
    if (/^\s*Ziel:\s+\S/.test(t)) return "questziel";
    if (/^\s*\[(ABGESCHLOSSEN|Abgeschlossen|Offen)\]\s*$/.test(t)) return "badge";
    if (/^\s*[─\-]{3,}\s*Runde\s+\d+\s*[─\-]{3,}\s*$/.test(t)) return "runde";
    const m = t.match(/^\s*\[([A-ZÄÖÜ][\wäöüß' ?-]{1,22})\]\s+\S/);
    if (m && !/^(Beliebige Taste)$/.test(m[1])) return "rede";
    if (/^\s*(\d{1,2}[.)]|\[[A-Za-z]\]|[A-Z][.)])\s/.test(t) || /^(Auswahl|Eingabe)\b/.test(t) || /^\s*\[Beliebige Taste\]/.test(t)) return "wahl";
    if (/^\s*===\s*.+\s*===\s*$/.test(t)) return "abschnitt";
    if (/^\s*[-•]\s+\S/.test(t) && !/\S {2,}\S|\|/.test(t)) return "liste";
    if (/^\s*Du:\s*\d+\/\d+\s*HP\s*\|/.test(t)) return "kampfzeile";
    if (/^[+−]\s+\S/.test(t)) return t[0] === "+" ? "modpos" : "modneg";
    if (/\b\d+ Schaden\b/.test(t) && /^(Du|Der|Die|Das|Dein|Deine|Ein|Eine)\b/.test(t) && !/:/.test(t)) return /^Du\b/.test(t) ? "treffdu" : "treffgegner";
    if (/^\s{2,}\S/.test(t)) {
      const s = t.trim();
      if (/\S {2,}\S|\|/.test(s)) return "mono";
      return kvZeile(s) ? "kvein" : "beschr";
    }
    if (/^[^|]{1,30} \| [^|]{1,40}$/.test(t) && !/\bHP\b/.test(t) && !/\S {2,}\S/.test(t)) return "pipe";
    if (/\S {2,}\S|\|/.test(t)) return "mono";
    if (kvZeile(t)) return "kv";
    if (/^[A-ZÄÖÜ][A-ZÄÖÜ \-]{2,28}$/.test(t.trim())) return "abschnitt";
    return "erzaehl";
  });
  // Kurze Zeile ohne Satzzeichen direkt über Auswahl, Werten oder Beschreibungen = Zwischenüberschrift.
  art.forEach((a, i) => {
    const t = zeilen[i].text.trim();
    if (a === "erzaehl" && t.split(/\s+/).length <= 3 && !/[.!?:,;]$/.test(t) && ["wahl", "kv", "kvein", "beschr"].includes(art[i + 1])) art[i] = "abschnitt";
  });
  // Peiltabelle (Finchs Messungen): Zeilen unter der Kopfzeile "Peilskizze / gemessen" gehören zur Tabelle.
  for (let i = 0; i < art.length; i++) {
    if (art[i] !== "peilkopf") continue;
    for (let j = i + 1; j < art.length && /^\S.{0,27}?\s{2,}\S+\s+\S+\s*$/.test(zeilen[j].text); j++) art[j] = "peilzeile";
  }
  // Quest-Namen: eine Textzeile direkt über "Ziel: …" oder einem Status-Schild.
  art.forEach((a, i) => {
    if (a !== "erzaehl") return;
    let j = i + 1;
    while (art[j] === "leer") j++;
    if ((art[j] === "questziel" || art[j] === "badge") && zeilen[i].text.trim().length < 70) art[i] = "questname";
  });
  // Nummerierte Einträge mit Zwischentext (Überschriften, Beschreibungen, z. B. im Inventar) bleiben stehen:
  // Dort stehen Name und Info im Text, die Knöpfe zeigen nur die Namen.
  const mitInfo = new Set();
  {
    let gruppe = [], letzte = -1;
    const abschliessen = () => {
      if (gruppe.length) {
        let info = false;
        for (let k = gruppe[0]; k <= gruppe[gruppe.length - 1]; k++) if (art[k] !== "wahl" && art[k] !== "leer") { info = true; break; }
        if (info) gruppe.forEach((k) => mitInfo.add(k));
      }
      gruppe = []; letzte = -1;
    };
    zeilen.forEach((zl, i) => {
      const m = art[i] === "wahl" && zl.text.match(/^\s*(\d{1,2})[.)]\s/);
      if (!m) return;
      if (+m[1] <= letzte) abschliessen();
      gruppe.push(i); letzte = +m[1];
    });
    abschliessen();
  }
  let html = "", vorherLeer = true, markiert = false, letzterSprecher = "";
  zeilen.forEach(({ text: t, z, y }, i) => {
    let a = art[i];
    // Auswahllisten ("1. ...", "[S] ...", "Auswahl:", "> 1") entfallen, wenn es dafür Knöpfe gibt.
    if (a === "wahl" && (y < start || listeAus) && !mitInfo.has(i)
      && (/^\s*(\d{1,2}[.)]|\[[A-Za-z]\]|[A-Z][.)])\s/.test(t) || /^Auswahl\b/.test(t) || /^\s*\[Beliebige Taste\]/.test(t) || /^\s*>\s*\S{0,3}\s*$/.test(t))) return;
    if (a === "kampfzeile" && aktuellerGegner) return;   // steht schon als Balken oben
    if (a === "leer") { if (!vorherLeer) html += '<div class="abstand"></div>'; vorherLeer = true; return; }
    vorherLeer = false;
    if (a !== "rede") letzterSprecher = "";
    // Marke an der ersten sichtbaren Zeile des neuen Bildschirms: dort beginnt das Fenster (leere und ausgeblendete Zeilen zählen nicht).
    if (!markiert && y >= start) { html += '<i id="lesemarke"></i>'; markiert = true; }
    t = t.replace(/\s+$/, "");
    if (a === "logo") {
      // Block-Schrift (Logo) bleibt zusammen und in Festbreite, sonst verschiebt sie sich.
      if (art[i - 1] === "logo") return;
      const teile = [];
      for (let j = i; art[j] === "logo"; j++) teile.push(zeilen[j].text.replace(/\s+$/, ""));
      const links = Math.min(...teile.map((s) => s.match(/^ */)[0].length));
      html += '<pre class="logo">' + esc(teile.map((s) => s.slice(links)).join("\n")) + "</pre>";
      return;
    }
    if (a === "hr") {
      html = html.replace(/<div class="abstand"><\/div>(<i id="lesemarke"><\/i>)?$/, "$1") + "<hr>";
      vorherLeer = true;
      return;
    }
    if ((a === "erzaehl" || a === "abschnitt") && art[i - 1] === "hr" && art[i + 1] === "hr") {
      const f = zeilenFarbe(z);
      html += '<p class="titel"' + (f ? ' style="color:' + f + '"' : "") + ">" + esc(t.trim()) + "</p>";
      return;
    }
    if (a === "rede") {
      // Sprechblase mit Anfangsbuchstaben-Kreis; folgen mehrere Zeilen desselben Sprechers, steht sein Name nur einmal.
      const m = t.match(/^\s*\[([^\]]+)\]\s+(.*)$/);
      const wer = m[1], gleich = letzterSprecher === wer, ich = spielerName && wer === spielerName;
      letzterSprecher = wer;
      html += '<div class="sprech' + (ich ? " ich" : "") + '" style="--c:' + sprecherFarbe(wer) + '"><span class="av' + (gleich ? " leer" : "") + '">' + esc(wer.charAt(0).toUpperCase()) +
        '</span><div class="blase">' + (gleich ? "" : "<b>" + esc(wer) + "</b>") + esc(m[2]) + "</div></div>";
      return;
    }
    if (a === "schritt") {
      const m = t.match(/(\d+)\s*\/\s*(\d+)/);
      const p = +m[2] ? Math.max(0, Math.min(100, (+m[1] / +m[2]) * 100)) : 0;
      html += '<p class="schritt"><span class="bar"><i style="width:' + p + '%"></i></span><b>Schritt ' + m[1] + " / " + m[2] + "</b></p>";
      return;
    }
    if (a === "wahl") { html += '<p class="wahl">' + esc(t.trim()) + "</p>"; return; }
    if (a === "peilzeile") return;   // steckt schon in der Tabelle
    if (a === "peilkopf") {
      let zeilenHtml = "";
      for (let j = i + 1; art[j] === "peilzeile"; j++) {
        const m = zeilen[j].text.trim().match(/^(.+?)\s{2,}(\S+)\s+(\S+)$/);
        const alt = parseFloat(m[2]), neu = parseFloat(m[3]);
        const abw = Number.isFinite(alt) && Number.isFinite(neu) ? neu - alt : null;
        zeilenHtml += '<tr class="' + (abw ? "abw" : "") + '"><td>' + esc(m[1]) + "</td><td>" + esc(m[2]) + "</td><td>" + esc(m[3]) + "</td><td>" + (abw === null ? "" : abw === 0 ? "✓" : (abw > 0 ? "+" : "") + abw) + "</td></tr>";
      }
      html += '<table class="peil"><thead><tr><th></th><th>Skizze</th><th>Gemessen</th><th>Abw.</th></tr></thead><tbody>' + zeilenHtml + "</tbody></table>";
      return;
    }
    if (a === "erfolg") {
      const m = t.trim().replace(/^✓\s+/, "").match(/^(.+?)\s+[–-]\s+(.+)$/);
      html += '<div class="erfolg ok"><b>' + esc(m ? m[1] : t.trim().replace(/^✓\s+/, "")) + "</b>" + (m ? "<span>" + esc(m[2]) + "</span>" : "") + "</div>";
      return;
    }
    if (a === "gesperrt") {
      // Mehrere verborgene Einträge hintereinander werden zu einer Zeile zusammengefasst.
      let p = i - 1; while (p >= 0 && art[p] === "leer") p--;
      if (p >= 0 && art[p] === "gesperrt") return;
      let n = 0;
      for (let q = i; q < art.length && (art[q] === "gesperrt" || art[q] === "leer"); q++) if (art[q] === "gesperrt") n++;
      html += '<div class="erfolg zu"><b>🔒 ' + (n > 1 ? n + " weitere noch verborgen" : "noch verborgen") + "</b></div>";
      return;
    }
    if (a === "questname") { html += '<p class="questname">' + esc(t.trim()) + "</p>"; return; }
    if (a === "questziel") { html += '<p class="questziel"><b>🎯</b> ' + esc(t.trim().replace(/^Ziel:\s*/, "")) + "</p>"; return; }
    if (a === "badge") {
      const fertig = /ABGESCHLOSSEN|Abgeschlossen/.test(t);
      html += '<p class="badge' + (fertig ? " ok" : "") + '">' + (fertig ? "✓ Abgeschlossen" : "○ Offen") + "</p>";
      return;
    }
    if (a === "attr") {
      const m = t.trim().match(/^([^:]+):\s*(.+)$/);
      const chips = (m[2].includes("?") && !/\d/.test(m[2])) ? '<span class="chip aus">noch verborgen</span>'
        : m[2].split(",").map((x) => { const q = x.trim().match(/^(.+?)\s+(\d+)$/); return q ? '<span class="chip">' + esc(q[1]) + " <b>" + q[2] + "</b></span>" : '<span class="chip">' + esc(x.trim()) + "</span>"; }).join("");
      html += '<div class="attr"><b>' + esc(m[1]) + "</b><div>" + chips + "</div></div>";
      return;
    }
    if (a === "kv" || a === "kvein") {
      const s = t.trim();
      const k = s.indexOf(":");
      const kl = s.slice(0, k).trim(), kw = s.slice(k + 1).trim();
      const bm = kw.match(/^(\d+)\s*\/\s*(\d+)/);
      const balkenArt = bm && +bm[2] > 0 ? (/^(Lebenspunkte|HP)$/.test(kl) ? "hp" : (/EXP/.test(kl) ? "xp" : "")) : "";
      if (balkenArt) {
        const p = Math.max(0, Math.min(100, (+bm[1] / +bm[2]) * 100));
        html += '<p class="kv fort ' + balkenArt + '"><span class="l">' + (KV_ICON[kl] || (/EXP/.test(kl) ? "✨" : "") ? (KV_ICON[kl] || "✨") + " " : "") + esc(kl) + '</span><span class="w"><span class="bar"><i style="width:' + p + '%"></i></span><b>' + bm[1] + " / " + bm[2] + "</b></span></p>";
        return;
      }
      const fort = /^Fortschritt$/.test(s.slice(0, k).trim()) && s.slice(k + 1).trim().match(/^(\d+)\s*\/\s*(\d+)$/);
      if (fort && +fort[2] > 0) {
        const p = Math.max(0, Math.min(100, (+fort[1] / +fort[2]) * 100));
        html += '<p class="kv fort"><span class="l">Fortschritt</span><span class="w"><span class="bar"><i style="width:' + p + '%"></i></span><b>' + fort[1] + " / " + fort[2] + "</b></span></p>";
        return;
      }
      const stat = /^erledigt$|^abgeschlossen$/i.test(kw) ? "ok" : /^offen$/i.test(kw) ? "offen" : "";
      html += '<p class="kv' + (a === "kvein" ? " ein" : "") + '"><span class="l">' + (KV_ICON[kl] ? KV_ICON[kl] + " " : "") + esc(kl) + '</span><span class="w' + (stat ? " " + stat : "") + '">' + (stat === "ok" ? "✓ " : stat === "offen" ? "○ " : "") + esc(kw) + "</span></p>";
      return;
    }
    if (a === "abschnitt") {
      const f = zeilenFarbe(z);
      html += '<p class="abschnitt"' + (f ? ' style="color:' + f + '"' : "") + ">" + esc(t.trim().replace(/^===\s*|\s*===$/g, "")) + "</p>";
      return;
    }
    if (a === "liste") { html += '<p class="liste"><b>–</b>' + esc(t.trim().replace(/^[-•]\s+/, "")) + "</p>"; return; }
    if (a === "beschr") { html += '<p class="beschr">' + esc(t.trim()) + "</p>"; return; }
    if (a === "kampfzeile") { html += '<p class="kampfzeile">' + esc(t.trim()) + "</p>"; return; }
    if (a === "runde") { html += '<p class="runde">' + esc(t.replace(/[─\-]/g, "").trim()) + "</p>"; return; }
    if (a === "modpos" || a === "modneg") {
      const s = t.trim();
      html += '<p class="mod ' + (a === "modpos" ? "pos" : "neg") + '"><b>' + esc(s[0]) + "</b>" + esc(s.slice(1).trim()) + "</p>";
      return;
    }
    if (a === "treffdu" || a === "treffgegner") { html += '<p class="treff ' + (a === "treffdu" ? "du" : "gegner") + '">' + esc(t.trim()) + "</p>"; return; }
    if (a === "pipe") { html += '<p class="pipe">' + esc(t.trim().replace(/\s\|\s/g, " · ")) + "</p>"; return; }
    if (a === "mono") { html += '<p class="mono">' + esc(t) + "</p>"; return; }
    const f = zeilenFarbe(z);
    html += '<p class="erzaehl"' + (f ? ' style="color:' + f + '"' : "") + ">" + esc(t.trim()) + "</p>";
  });
  if (!markiert) html += '<i id="lesemarke"></i>';
  if (statistik && zeilen.some((x) => /^\s*QUESTLOG\/ERFOLGE\s*$/.test(x.text))) {
    const z = [["⏱ Spielzeit", statistik.spielzeit || "–"], ["⚔️ Besiegte Gegner", statistik.besiegt ?? 0],
      ["🏆 Erfolge", (statistik.erfolge ?? 0) + (statistik.erfolge_max ? " / " + statistik.erfolge_max : "")], ["📖 Jagdbuch", (statistik.jagd ?? 0) + " Gegner"]];
    html += '<div class="statistik"><b>📈 Statistik</b>' + z.map(([k, v]) => "<span>" + esc(k) + "</span><em>" + esc(String(v)) + "</em>").join("") + "</div>";
  }
  // Drei oder mehr Wert-Zeilen hintereinander (Status, Inventar, Verfassungen) kommen auf eine Karte.
  html = html.replace(/(?:<p class="kv[^"]*">.*?<\/p>){2,}/g, (m) => '<div class="karte">' + m + "</div>");
  const neuerSchirm = bildschirmNr !== gezeigtNr;
  // Die fertige vorige Seite wandert in den Verlauf (nur wenn sie wirklich Text enthielt).
  if (neuerSchirm && seiteHtml && /<p class="(erzaehl|rede|kv|beschr|liste|treff|mod|abschnitt|titel)/.test(seiteHtml)
    && seitenVerlauf[seitenVerlauf.length - 1] !== seiteHtml) {
    seitenVerlauf.push(seiteHtml);
    if (seitenVerlauf.length > 15) seitenVerlauf.shift();
    verlaufSichern();
  }
  seiteHtml = html.replace('<i id="lesemarke"></i>', "");
  html += '<div id="lesespacer"></div>';
  leseProgramm = true;
  lese.innerHTML = html;
  gezeigtNr = bildschirmNr;
  if (neuerSchirm) leseFolgen = true;
  leseAnker(lese);
  requestAnimationFrame(() => { leseProgramm = false; });
  if (neuerSchirm) nachAnkern();
}
// Neuer Text beginnt oben im Fenster (nicht unten). Scrollst du selbst, bleibt die Ansicht, wo du sie lässt,
// bis der nächste Bildschirm kommt.
let leseFolgen = true, leseProgramm = false, bildschirmNr = 0, gezeigtNr = -1, listeAus = false;
let seiteHtml = "";            // aktuelle Seite als HTML (ohne Marke)
const seitenVerlauf = (() => { try { const v = JSON.parse(localStorage.getItem("void-verlauf")); return Array.isArray(v) ? v.filter((x) => typeof x === "string").slice(-15) : []; } catch (e) { return []; } })();   // frühere Seiten, die letzte zuletzt
const verlaufSichern = () => { try { localStorage.setItem("void-verlauf", JSON.stringify(seitenVerlauf)); } catch (e) {} };
function leseAnker(l) {
  const marke = l.querySelector("#lesemarke"), abstand = l.querySelector("#lesespacer");
  if (!marke || !abstand || !leseFolgen) return;
  abstand.style.height = "0px";   // erst ohne Platzhalter messen, sonst rechnet sich der alte Wert immer wieder selbst fest
  const y = marke.getBoundingClientRect().top - l.getBoundingClientRect().top + l.scrollTop;
  // Ist der neue Text kürzer als das Fenster, Platz darunter lassen, damit er trotzdem ganz oben beginnen kann.
  // (scrollHeight ist mindestens so hoch wie das Fenster, deshalb das Ende des Inhalts über den Platzhalter messen.)
  const ende = abstand.getBoundingClientRect().top - l.getBoundingClientRect().top + l.scrollTop + 12;
  const ziel = y <= 12 ? 0 : y - 4;   // steht der Anfang schon ganz oben, gibt es nichts zu scrollen
  abstand.style.height = Math.max(0, ziel + l.clientHeight - ende) + "px";
  l.scrollTop = ziel;
}
// Auf echten Handys ändert sich das Layout kurz nach dem Zeichnen noch (Tastatur, Adressleiste, Bilder, Schrift).
// Darum wird der Textanfang kurz danach noch einmal nach oben gesetzt, solange du nicht selbst gescrollt hast.
let ankerTimer = 0;
function nachAnkern() {
  clearTimeout(ankerTimer);
  [60, 250, 700].forEach((ms, i) => { ankerTimer = setTimeout(() => {
    const l = document.getElementById("lese");
    if (!leseFolgen || !l.querySelector("#lesemarke")) return;
    leseProgramm = true; leseAnker(l);
    requestAnimationFrame(() => { leseProgramm = false; });
  }, ms); });
}
addEventListener("resize", nachAnkern);
if (window.visualViewport) visualViewport.addEventListener("resize", nachAnkern);
document.getElementById("lese").addEventListener("scroll", () => {
  if (!leseProgramm) leseFolgen = false;
}, { passive: true });
new ResizeObserver(() => {
  const l = document.getElementById("lese");
  if (leseFolgen) { leseProgramm = true; leseAnker(l); requestAnimationFrame(() => { leseProgramm = false; }); }
}).observe(document.getElementById("lese"));
function uiAnwenden() {
  document.body.classList.toggle("lesen", UI.lesen);
  document.body.classList.toggle("farben", UI.farben);
  document.body.classList.toggle("gross", !!UI.gross);
  document.body.classList.toggle("kontrast", !!UI.kontrast);
  document.getElementById("lese").classList.toggle("serif", UI.serif);
  document.getElementById("probe").classList.toggle("serif", UI.serif);
  document.documentElement.style.setProperty("--fs", (UI.schrift + 1) + "px");
  if (termRef) termRef.options.fontSize = UI.schrift;
  anpassen();
  leseNeu();
  if (UI.lesen) leseRendern();
}

// Startbildschirm: großer Titel und "Weiterspielen" mit dem zuletzt gespeicherten Platz.
let startAktion = 0;
function weiterSlot() {
  const st = spielstaende();
  const da = SLOT_NAMEN.filter((n) => st[n]);
  if (!da.length) return "";
  if (UI.zuletzt && st[UI.zuletzt]) return UI.zuletzt;
  const zeit = (n) => { try { return +JSON.parse(st[n]).spieler.spielzeit || 0; } catch (e) { return 0; } };
  return da.reduce((a, b) => (zeit(b) > zeit(a) ? b : a));
}
function startSetzen(an) {
  document.body.classList.toggle("start", an);
  if (!an) return;
  document.body.classList.remove("imspiel");
  hintergrundSetzen("eichenruh");
  const knopf = document.getElementById("weiterspielen");
  const n = weiterSlot();
  knopf.hidden = !n;
  if (!n) return;
  const d = slotInfo(spielstaende()[n]);
  knopf.innerHTML = "▶ Weiterspielen<small>" + esc(d.titel) + (d.info ? " · " + esc(d.info) : "") + "</small>";
}
document.getElementById("weiterspielen").addEventListener("click", () => {
  const n = weiterSlot();
  if (!n) return;
  UI.zuletzt = n; uiSichern();
  startAktion = SLOT_NAMEN.indexOf(n) + 1;
  antwort("2");
});

// Aktuelle Ziele: die Seite bekommt sie vom Spiel (worker.js liest quests()). Oben steht das zuletzt geänderte, Tippen zeigt alle.
let ziele = [], zielAktuell = "";
function zieleSetzen(liste) {
  const alt = new Map(ziele.map((z) => [z.titel, z.ziel]));
  const geaendert = liste.filter((z) => alt.get(z.titel) !== z.ziel);
  if (ziele.length && geaendert.length) zielAktuell = geaendert[geaendert.length - 1].titel;
  ziele = liste;
  if (!ziele.some((z) => z.titel === zielAktuell)) zielAktuell = ziele.length ? ziele[ziele.length - 1].titel : "";
  const z = ziele.find((x) => x.titel === zielAktuell);
  const knopf = document.getElementById("ziel");
  document.body.classList.toggle("hatziel", !!z);
  if (z) knopf.textContent = "🎯 " + z.ziel + (ziele.length > 1 ? "  (+" + (ziele.length - 1) + ")" : "");
}
const zielBlatt = document.getElementById("zielblatt");
function zielBlattSchliessen() { zielBlatt.classList.remove("offen"); zielBlatt.setAttribute("aria-hidden", "true"); }
document.getElementById("ziel").addEventListener("click", () => {
  document.getElementById("zielliste").innerHTML = ziele.map((z) => '<div class="z"><b>' + esc(z.titel) + "</b><span>" + esc(z.ziel) + "</span></div>").join("");
  zielBlatt.classList.add("offen"); zielBlatt.setAttribute("aria-hidden", "false");
});
document.getElementById("zielZu").addEventListener("click", zielBlattSchliessen);

// Karte: die fünf Hauptorte. Ein Tipp auf einen von hier erreichbaren Ort drückt den passenden Knopf im Spiel.
let hudOrt = "", spielerName = "";
const KARTE_ORTE = [
  { id: "eichenruh", name: "Eichenruh", sym: "🏘️", x: 160, y: 185, hier: /eichenruh|spieler_zimmer|gasthaus|marktplatz|^schmiede|bjorns/i, besucht: /eichenruh/i, knopf: /Eichenruh/ },
  { id: "koehlerei", name: "Köhlerei", sym: "🔥", x: 62, y: 80, hier: /k[oö]e?hlerei|brandschneise/i, besucht: /k[oö]e?hlerei/i, knopf: /K[öo]e?hlerei/ },
  { id: "oros", name: "Oros", sym: "🏛️", x: 258, y: 80, hier: /oros|tiefen|universit/i, besucht: /oros|tiefen|universit/i, knopf: /Oros|Universit|Faden/ },
  { id: "dorf", name: "Verlassenes Dorf", sym: "🏚️", x: 62, y: 290, hier: /verlassenes_dorf|verlassenes dorf|alte_schmiede|alte schmiede|lagerkeller|huette/i, besucht: /dorf|alte_schmiede|lagerkeller/i, knopf: /Dorf|Pfad des Vergessens/ },
  { id: "hafen", name: "Letzthafen", sym: "⚓", x: 258, y: 290, hier: /letzthafen|wrackstrand|edda|namenstein|leuchtfeuer|klippe/i, besucht: /letzthafen|hafen|wrack|edda/i, knopf: /Letzthafen|K[öo]nigsring/ }
];
// Kleine Orte: erscheinen erst, wenn du dort warst oder sie von hier aus erreichbar sind.
KARTE_ORTE.push(
  { id: "gasthaus", klein: true, name: "Gasthaus", sym: "🍺", x: 118, y: 142, hier: /^gasthaus|maras/i, besucht: /gasthaus/i, knopf: /Gasthaus/ },
  { id: "schmiede", klein: true, name: "Schmiede", sym: "⚒️", x: 202, y: 142, hier: /^schmiede|bjorns/i, besucht: /^schmiede/i, knopf: /Bjorns Schmiede|^Schmiede/ },
  { id: "markt", klein: true, name: "Markt", sym: "🧺", x: 118, y: 232, hier: /marktplatz/i, besucht: /marktplatz/i, knopf: /Marktplatz/ },
  { id: "haus", klein: true, name: "Haus", sym: "🏠", x: 202, y: 232, hier: /spieler_zimmer|dein haus/i, besucht: /spieler_zimmer/i, knopf: /Nach Hause/ },
  { id: "alteschmiede", klein: true, name: "Alte Schmiede", sym: "⚒️", x: 24, y: 252, hier: /alte_schmiede|alte schmiede/i, besucht: /alte_schmiede/i, knopf: /Alte Schmiede/ },
  { id: "lagerkeller", klein: true, name: "Lagerkeller", sym: "📦", x: 100, y: 252, hier: /lagerkeller/i, besucht: /lagerkeller/i, knopf: /Lagerkeller/ },
  { id: "wrackstrand", klein: true, name: "Wrackstrand", sym: "🌊", x: 220, y: 252, hier: /wrackstrand/i, besucht: /wrack/i, knopf: /Wrackstrand/ },
  { id: "edda", klein: true, name: "Eddas Haus", sym: "🏚️", x: 298, y: 252, hier: /edda/i, besucht: /edda/i, knopf: /Edda/ },
  { id: "archiv", klein: true, name: "Archiv", sym: "📚", x: 220, y: 118, hier: /archiv/i, besucht: /archiv/i, knopf: /Archiv/ },
  { id: "tiefen", klein: true, name: "Tiefen", sym: "⛏️", x: 298, y: 118, hier: /tiefen/i, besucht: /tiefen/i, knopf: /Tiefen|TIEFEN/ }
);
const KARTE_WEGE = [["eichenruh", "koehlerei", "Waldweg"], ["eichenruh", "oros", "Faden der Erinnerung"], ["eichenruh", "dorf", "Pfad des Vergessens"], ["eichenruh", "hafen", "Königsring"]];
const kartenBlatt = document.getElementById("kartenblatt");
function kartenSchliessen() { kartenBlatt.classList.remove("offen"); kartenBlatt.setAttribute("aria-hidden", "true"); }
function kartenWerte() {
  let besucht = [];
  try { const n = weiterSlot(); if (n) besucht = [].concat(JSON.parse(spielstaende()[n]).spieler.besuchte_orte || []).map(String); } catch (e) {}
  const knoepfe = knoepfeEl.style.display === "none" ? [] : [...knoepfeEl.querySelectorAll("button")].filter((b) => !b.closest(".ikonen"));
  const hierKlein = KARTE_ORTE.find((o) => o.klein && o.hier.test(hudOrt));
  return KARTE_ORTE.map((o) => {
    const hier = hierKlein ? o === hierKlein : (!o.klein && o.hier.test(hudOrt));
    const knopf = hier ? null : knoepfe.find((b) => o.knopf.test(b.textContent));
    const bekannt = besucht.some((s) => o.besucht.test(s));
    return { o, hier, knopf, klasse: hier ? "hier" : knopf ? "nah" : bekannt ? "bekannt" : "unbekannt", sichtbar: hier || !!knopf || bekannt };
  });
}
function kartenZeichnen() {
  const w = kartenWerte();
  const von = (id) => KARTE_ORTE.find((o) => o.id === id);
  const linien = KARTE_WEGE.map(([a, b, n]) => {
    const A = von(a), B = von(b);
    return '<line class="weg" x1="' + A.x + '" y1="' + A.y + '" x2="' + B.x + '" y2="' + B.y + '"/><text class="wegname" x="' + ((A.x + B.x) / 2 + (B.x > A.x ? 14 : -14)) + '" y="' + ((A.y + B.y) / 2) + '">' + esc(n) + "</text>";
  }).join("");
  const orte = w.filter(({ o, sichtbar }) => !o.klein || sichtbar).map(({ o, klasse, sichtbar }) =>
    '<g class="ort ' + klasse + (o.klein ? " klein" : "") + '" data-id="' + o.id + '"><circle cx="' + o.x + '" cy="' + o.y + '" r="' + (o.klein ? 14 : 24) + '"/><text class="sym" x="' + o.x + '" y="' + (o.y + (o.klein ? 4 : 6)) + '">' + (sichtbar ? o.sym : "?") +
    '</text><text x="' + o.x + '" y="' + (o.y + (o.klein ? 27 : 42)) + '">' + (sichtbar ? esc(o.name) : "Unbekannt") + "</text></g>").join("");
  document.getElementById("karteninhalt").innerHTML = '<svg viewBox="0 0 320 350" role="img" aria-label="Karte">' + linien + orte + "</svg>";
  document.getElementById("kartenhinweis").textContent = hudOrt && !w.some((x) => x.hier) ? "Du bist unterwegs. Tippe auf einen Ort, wenn ein Weg dorthin offen ist." : "Tippe auf einen gelb umrandeten Ort, um dorthin zu reisen.";
  document.querySelectorAll("#karteninhalt .ort").forEach((g) => g.addEventListener("click", () => {
    const eintrag = kartenWerte().find((x) => x.o.id === g.dataset.id);
    if (eintrag.hier) { document.getElementById("kartenhinweis").textContent = "Du bist schon hier."; return; }
    if (eintrag.knopf) { kartenSchliessen(); eintrag.knopf.click(); return; }
    const hierWo = kartenWerte().some((x) => x.hier && x.o.id === "eichenruh");
    document.getElementById("kartenhinweis").textContent = hierWo ? "Dieser Weg ist gerade nicht offen." : "Von hier aus geht es nur über Eichenruh oder gar nicht, solange du mitten in etwas steckst.";
  }));
}
document.getElementById("kartenKnopf").addEventListener("click", () => { kartenZeichnen(); kartenBlatt.classList.add("offen"); kartenBlatt.setAttribute("aria-hidden", "false"); });
document.getElementById("kartenZu").addEventListener("click", kartenSchliessen);
kartenBlatt.addEventListener("click", (e) => { if (e.target === kartenBlatt) kartenSchliessen(); });

// Vorheriger Text: die letzten Seiten, jüngste zuerst.
const verlaufBlatt = document.getElementById("verlaufblatt");
function verlaufSchliessen() { verlaufBlatt.classList.remove("offen"); verlaufBlatt.setAttribute("aria-hidden", "true"); }
document.getElementById("verlauf").addEventListener("click", () => {
  const liste = document.getElementById("verlaufliste");
  const n = seitenVerlauf.length;
  liste.innerHTML = n ? seitenVerlauf.map((h, i) => "<section><small>" + (i === n - 1 ? "Letzte Seite" : "Vor " + (n - i) + " Seiten") + "</small>" + h + "</section>").reverse().join("")
    : '<p class="erzaehl">Noch keine früheren Seiten.</p>';
  verlaufBlatt.classList.add("offen"); verlaufBlatt.setAttribute("aria-hidden", "false");
  verlaufBlatt.querySelector(".blatt").scrollTop = 0;
});
document.getElementById("verlaufZu").addEventListener("click", verlaufSchliessen);
verlaufBlatt.addEventListener("click", (e) => { if (e.target === verlaufBlatt) verlaufSchliessen(); });
zielBlatt.addEventListener("click", (e) => { if (e.target === zielBlatt) zielBlattSchliessen(); });

// Einführung: beim ersten Spielstart einmal, danach über das ⚙-Blatt.
const introBlatt = document.getElementById("einfuehrung");
function introZeigen() { introBlatt.classList.add("offen"); introBlatt.setAttribute("aria-hidden", "false"); }
function introSchliessen() { introBlatt.classList.remove("offen"); introBlatt.setAttribute("aria-hidden", "true"); UI.intro = true; UI.stand = APP_STAND; uiSichern(); }
document.getElementById("einfuehrungZu").addEventListener("click", introSchliessen);

// "Was ist neu": einmal nach jedem Update, falls für den Stand ein Text hinterlegt ist.
const NEUES = {
  "2026-10-25-26": [
    "<b>Stimmung im Text:</b> Unter dem Ortsnamen steht draußen eine Zeile zu Abend, Nacht, Regen oder Nebel.",
    "<b>Nachts und im Nebel</b> begegnest du auf Reisen etwas häufiger Gegnern.",
    "<b>Behoben:</b> Nach einem langen Druck auf einen Knopf konnte der nächste Tipp verschluckt werden."
  ],
  "2026-10-25-25": [
    "<b>Tag und Nacht gelten jetzt wirklich:</b> Ein Spieltag dauert 40 Minuten Spielzeit. Nachts, bei Regen und bei Nebel siehst du draußen schlechter, das spürst du im Kampf. Das Talent Nachtauge gleicht die Nacht aus.",
    "<b>Stimmung:</b> Draußen wird der Hintergrund abends und nachts dunkler, bei Regen und Nebel gedämpft. In Häusern und Höhlen bleibt er gleich.",
    "<b>Seit der letzten Version:</b> kleinere Töne (Offline-Paket etwa 10 MB), Antworten als Sprechblasen 💬, Vorlesen 🗣, Statistik im Journal."
  ],
  "2026-10-25-24": [
    "<b>Tageszeit und Wetter:</b> Oben im Kopf zeigt ein Symbol Abend, Nacht, Nebel oder Regen. Es dient nur der Stimmung und ändert nichts im Kampf.",
    "<b>Kleinere Töne:</b> Die Musik ist jetzt etwa zehnmal kleiner. Das Offline-Paket umfasst nur noch rund 10 MB.",
    "<b>Seit der letzten Version:</b> Antworten als Sprechblasen 💬, Vorlesen 🗣, Statistik im Journal, Fehlertext kopieren, Sicherung als Text."
  ],
  "2026-10-25-22": [
    "<b>Gespräch:</b> Antworten erscheinen als Sprechblasen 💬. Langes Drücken auf einen Knopf zeigt den ganzen Text.",
    "<b>Vorlesen:</b> Der Knopf 🗣 oben liest die Seite mit der deutschen Stimme deines Handys vor.",
    "<b>Hilfe bei Fehlern:</b> Stürzt das Spiel ab, kannst du den Fehlertext kopieren. Spielstand auch als Text sichern.",
    "<b>Weiteres:</b> Bildschirm anlassen (⚙), Punkt am 💾 bei langer Zeit ohne Speichern, Statistik im Journal, neue Klänge für Truhe, Tür und Münzen."
  ],
  "2026-10-25-16": [
    "<b>Karte:</b> Kleine Orte wie Gasthaus, Schmiede, Markt und Haus erscheinen als Punkte, sobald du dort warst.",
    "<b>Peiltabelle:</b> Finchs Messwerte stehen als Tabelle, Abweichungen sind rot markiert.",
    "<b>Zweite Kopie:</b> Deine Spielstände liegen zusätzlich in einem zweiten Speicher des Geräts. Fehlen sie im Browser, wird die Wiederherstellung angeboten.",
    "<b>Seit der letzten Version:</b> Sprechblasen im Gespräch, Musik und Effekte getrennt einstellbar."
  ]
};
const neuesBlatt = document.getElementById("neues");
function neuesZeigen() {
  document.getElementById("neuesliste").innerHTML = (NEUES[APP_STAND] || []).map((t) => "<li>" + t + "</li>").join("");
  neuesBlatt.classList.add("offen"); neuesBlatt.setAttribute("aria-hidden", "false");
}
function neuesSchliessen() { neuesBlatt.classList.remove("offen"); neuesBlatt.setAttribute("aria-hidden", "true"); UI.stand = APP_STAND; uiSichern(); }
document.getElementById("neuesZu").addEventListener("click", neuesSchliessen);

// Absturz-Hilfe: Das Spiel druckt selbst nie "[Fehler]" oder "Traceback"; kommt das im Text vor, ist Python abgestürzt.
const absturzBlatt = document.getElementById("absturz");
let absturzRest = "", absturzGezeigt = false, absturzTimer = 0;
function absturzZeigen(text) {
  if (absturzGezeigt) return;
  absturzGezeigt = true;
  const bericht = ["VOID Absturzbericht", "App-Stand: " + APP_STAND, "Ort: " + (hudOrt || "?"), "Browser: " + navigator.userAgent, "", String(text).trim()].join("\n");
  document.getElementById("absturzText").textContent = bericht;
  absturzBlatt.classList.add("offen"); absturzBlatt.setAttribute("aria-hidden", "false");
}
function absturzSchliessen() { absturzBlatt.classList.remove("offen"); absturzBlatt.setAttribute("aria-hidden", "true"); }
function absturzLauschen(t) {
  if (absturzGezeigt) return;
  absturzRest = (absturzRest + t).slice(-3000);
  if (!/Traceback \(most recent call last\)|\[Fehler\]/.test(absturzRest)) return;
  clearTimeout(absturzTimer);
  absturzTimer = setTimeout(() => absturzZeigen(absturzRest.replace(/\x1b\[[0-9;?]*[A-Za-z]/g, "").replace(/^[\s\S]*?(?=\[Fehler\]|Traceback)/, "")), 600);
}
function textKopieren(text, fertig) {
  const altweg = () => {
    try {
      const t = document.createElement("textarea");
      t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
      document.body.append(t); t.select();
      const ok = document.execCommand("copy");
      t.remove(); fertig(ok);
    } catch (e) { fertig(false); }
  };
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(() => fertig(true), altweg);
  else altweg();
}
document.getElementById("absturzKopieren").addEventListener("click", (e) => {
  const k = e.currentTarget;
  textKopieren(document.getElementById("absturzText").textContent, (ok) => { k.textContent = ok ? "✓ Kopiert" : "Kopieren nicht möglich, Text markieren"; setTimeout(() => { k.textContent = "📋 Fehlertext kopieren"; }, 2500); });
});
document.getElementById("absturzNeu").addEventListener("click", () => location.reload());
document.getElementById("absturzZu").addEventListener("click", absturzSchliessen);
addEventListener("error", (e) => !/ResizeObserver|^Script error/.test(e.message || "") && absturzZeigen("Fehler in der App: " + (e.message || "") + " (" + (e.filename || "") + ":" + (e.lineno || "") + ")"));

// Vorlesen: Die aktuelle Seite wird mit der deutschen Stimme des Geräts vorgelesen (speechSynthesis). Neue Seite oder erneutes Tippen stoppt.
const vorlesenKnopf = document.getElementById("vorlesen");
function vorlesenStopp() {
  if (window.speechSynthesis && (speechSynthesis.speaking || speechSynthesis.pending)) speechSynthesis.cancel();
  vorlesenKnopf.classList.remove("an");
}
function vorlesenText() {
  const lese = document.getElementById("lese");
  const kopie = lese.cloneNode(true);
  kopie.querySelectorAll("#lesemarke, .logo").forEach((e) => e.remove());
  return (kopie.innerText || kopie.textContent || "").replace(/[─═━\-_=*]{3,}/g, " ").replace(/[ \t]+/g, " ").trim();
}
function vorlesenTeile(text) {
  // Kurze Stücke an Satzenden: lange Äußerungen bricht Chrome auf Android sonst gern ab.
  const teile = [];
  for (const absatz of text.split(/\n+/)) {
    let rest = absatz.trim();
    while (rest.length > 180) {
      let i = Math.max(rest.lastIndexOf(". ", 180), rest.lastIndexOf("! ", 180), rest.lastIndexOf("? ", 180), rest.lastIndexOf(", ", 180));
      if (i < 40) i = rest.lastIndexOf(" ", 180);
      if (i < 1) i = 180;
      teile.push(rest.slice(0, i + 1).trim()); rest = rest.slice(i + 1).trim();
    }
    if (rest) teile.push(rest);
  }
  return teile;
}
if (window.speechSynthesis && window.SpeechSynthesisUtterance) {
  vorlesenKnopf.hidden = false;
  vorlesenKnopf.addEventListener("click", () => {
    if (speechSynthesis.speaking || speechSynthesis.pending) { vorlesenStopp(); return; }
    const teile = vorlesenTeile(vorlesenText());
    if (!teile.length) { hinweis("Hier gibt es nichts zum Vorlesen"); return; }
    const stimmen = speechSynthesis.getVoices();
    const stimme = stimmen.find((v) => /^de[-_]DE/i.test(v.lang)) || stimmen.find((v) => /^de/i.test(v.lang));
    if (stimmen.length && !stimme) hinweis("Keine deutsche Stimme gefunden (Android-Einstellungen, Sprachausgabe)");
    vorlesenKnopf.classList.add("an");
    teile.forEach((t, i) => {
      const u = new SpeechSynthesisUtterance(t);
      u.lang = stimme ? stimme.lang : "de-DE";
      if (stimme) u.voice = stimme;
      if (i === teile.length - 1) { u.onend = u.onerror = () => vorlesenKnopf.classList.remove("an"); }
      speechSynthesis.speak(u);
    });
  });
}

// Speichern-Hinweis: Ein Punkt am 💾, wenn seit über 20 Minuten Spielzeit in dieser Sitzung nicht gespeichert wurde.
const SITZUNG_START = Date.now();
function speicherPunktSetzen() {
  const alt = Date.now() - Math.max(SITZUNG_START, UI.gespeichert || 0);
  document.getElementById("speicherPunkt").classList.toggle("an", document.body.classList.contains("imspiel") && alt > 20 * 60e3);
}
setInterval(speicherPunktSetzen, 30000);

// Langer Druck (0,5 s) auf einen Knopf zeigt den ganzen Eintrag samt Beschreibung, ohne ihn auszulösen.
{
  const tipp = document.getElementById("langtipp");
  let timer = 0, gezeigt = false, sx = 0, sy = 0;
  const weg = () => { clearTimeout(timer); tipp.classList.remove("an"); };
  knoepfeEl.addEventListener("pointerdown", (e) => {
    const b = e.target.closest("button");
    if (!b || !b.dataset.voll) return;
    gezeigt = false; sx = e.clientX; sy = e.clientY;
    clearTimeout(timer);
    timer = setTimeout(() => {
      gezeigt = true;
      tipp.innerHTML = esc(b.dataset.voll) + "<small>Loslassen zum Schließen. Der Knopf wurde nicht ausgelöst.</small>";
      tipp.classList.add("an");
      if (UI.vibration !== false && navigator.vibrate) { try { navigator.vibrate(15); } catch (err) {} }
    }, 500);
  });
  knoepfeEl.addEventListener("pointermove", (e) => { if (!gezeigt && Math.abs(e.clientX - sx) + Math.abs(e.clientY - sy) > 12) clearTimeout(timer); });
  // Der Klick folgt dem Loslassen sofort; bleibt er aus (Finger weggezogen), darf er den nächsten Tipp nicht verschlucken.
  ["pointerup", "pointercancel", "pointerleave"].forEach((n) => knoepfeEl.addEventListener(n, () => {
    clearTimeout(timer);
    if (gezeigt) { setTimeout(weg, 1200); setTimeout(() => { gezeigt = false; }, 300); }
  }));
  // Der Klick nach einem langen Druck wird verschluckt.
  knoepfeEl.addEventListener("click", (e) => { if (gezeigt) { e.stopImmediatePropagation(); e.preventDefault(); gezeigt = false; } }, true);
  knoepfeEl.addEventListener("contextmenu", (e) => e.preventDefault());
}

// Eingabefeld nur zeigen, wenn das Spiel Text erwartet (Name, Menge) oder keine Auswahl erkennbar ist.
// Das Tastatur-Symbol im Kopf holt es bei Bedarf herbei.
let feldOffen = false;
function feldSetzen(noetig) {
  feldOffen = false;
  document.body.classList.toggle("ohnefeld", UI.feld === "auto" && !noetig);
  if (UI.feld === "immer" || noetig) document.getElementById("eingabe").focus({ preventScroll: true });
}
document.getElementById("speicher").addEventListener("click", () => {
  kette = SCHNELLSPEICHERN.map((s) => s);
  antwort("q");
});
document.getElementById("tasten").addEventListener("click", () => {
  feldOffen = true;
  document.body.classList.remove("ohnefeld");
  document.getElementById("eingabe").focus();
});

// Zurück-Taste von Android: schließt das ⚙-Blatt oder löst im Spiel "Zurück"/"Abbrechen" aus.
// Zweimal schnell Zurück verlässt die App.
let beendenBis = 0;
function hinweis(t) {
  const el = document.getElementById("hinweiszeile");
  el.textContent = t; el.classList.add("an");
  clearTimeout(hinweis.t); hinweis.t = setTimeout(() => el.classList.remove("an"), 2000);
}
try { history.replaceState({ void: 0 }, ""); history.pushState({ void: 1 }, ""); } catch (e) {}
// Eine Ebene zurück: erst offene Fenster schließen, dann im Spiel "Zurück"/"Abbrechen" drücken. Gibt an, ob etwas passiert ist.
function zurueckGehen() {
  if (absturzBlatt.classList.contains("offen")) { absturzSchliessen(); return true; }
  if (neuesBlatt.classList.contains("offen")) { neuesSchliessen(); return true; }
  if (introBlatt.classList.contains("offen")) { introSchliessen(); return true; }
  if (kartenBlatt.classList.contains("offen")) { kartenSchliessen(); return true; }
  if (verlaufBlatt.classList.contains("offen")) { verlaufSchliessen(); return true; }
  if (zielBlatt.classList.contains("offen")) { zielBlattSchliessen(); return true; }
  if (einstEl.classList.contains("offen")) { einstSchliessen(); return true; }
  const rKnopf = ratEl().classList.contains("an") && ratEl().querySelector(".abbrechen");
  if (rKnopf) { rKnopf.click(); return true; }
  const zurueck = knoepfeEl.style.display !== "none" && [...knoepfeEl.querySelectorAll("button")].find((b) => {
    const t = b.querySelector(".t");
    return t && /^(\d+\.\s*)?(Nein,\s*)?(Zurück|zurück|Abbrechen|Schließen)\s*$/.test(t.textContent);
  });
  if (zurueck) { zurueck.click(); return true; }
  return false;
}
addEventListener("popstate", () => {
  const wieder = () => { try { history.pushState({ void: 1 }, ""); } catch (e) {} };
  if (zurueckGehen()) { wieder(); return; }
  if (Date.now() < beendenBis) { history.back(); return; }
  beendenBis = Date.now() + 2000;
  hinweis("Noch einmal Zurück, um die App zu verlassen");
  wieder();
});
// Wisch vom linken Rand nach rechts = Zurück (wie die Zurück-Geste).
{
  let sx = 0, sy = 0, aktiv = false;
  document.addEventListener("touchstart", (e) => { const t = e.touches[0]; aktiv = e.touches.length === 1 && t.clientX < 22; sx = t.clientX; sy = t.clientY; }, { passive: true });
  document.addEventListener("touchend", (e) => {
    if (!aktiv) return; aktiv = false;
    const t = e.changedTouches[0], dx = t.clientX - sx, dy = Math.abs(t.clientY - sy);
    if (dx > 70 && dx > dy * 2 && !zurueckGehen()) hinweis("Hier gibt es kein Zurück");
  }, { passive: true });
}

// Symbolrätsel (Eddas Truhe, Werkbank der Alten Schmiede): Das Spiel fragt Position für Position ab
// ("Position 2 von 4" + Nummernliste + "Abbrechen"). Hier legt man die ganze Folge per Tippen und die App
// schickt die Nummern nacheinander an das Spiel. Das Spiel selbst bleibt unverändert.
const RAETSEL_ICON = { "Möwe": "🐦", Sonne: "☀️", Laterne: "🏮", Welle: "🌊", Amboss: "⚒️", Wasser: "💧", Flamme: "🔥" };
let rat = null;
const ratEl = () => document.getElementById("raetsel");
function raetselAus() { rat = null; ratEl().classList.remove("an"); ratEl().replaceChildren(); }
function raetselPruefen(zeilen, eintraege) {
  const m = zeilen.map((z) => z.match(/^\s*Position\s+(\d+)\s+von\s+(\d+)\s*$/)).find(Boolean);
  const abbr = eintraege.find((e) => !e.sonder && /^Abbrechen/.test(e.text));
  const symbole = eintraege.filter((e) => e !== abbr && !e.sonder && !e.weiter);
  if (!m || !abbr || !symbole.length) { raetselAus(); return false; }
  const k = +m[1], n = +m[2];
  if (rat && rat.senden && rat.n === n && rat.folge[k - 1]) {
    // Folge wird abgeschickt: nächsten Schritt wählen (die Liste ist um die bereits gewählten Symbole kürzer).
    const e = symbole.find((x) => x.text === rat.folge[k - 1]);
    if (e) { setTimeout(() => antwort(e.wert), 0); return true; }
  }
  if (k !== 1 || symbole.length < 2) { raetselAus(); return false; }
  rat = { n, folge: [], senden: false, eintraege: symbole, abbr: abbr.wert };
  knoepfeEl.style.display = "none";
  listeAus = true; leseNeu();
  ratEl().classList.add("an");
  raetselZeichnen();
  anpassen();
  return true;
}
function raetselZeichnen() {
  const el = ratEl();
  const namen = rat.eintraege.map((e) => e.text);
  const symbolHtml = (s) => '<span>' + (RAETSEL_ICON[s] || "") + "</span>" + esc(s);
  el.innerHTML = '<p class="hilfe">Tippe die Symbole in der richtigen Reihenfolge. Auf einen Platz tippen nimmt es zurück.</p>' +
    '<div class="plaetze">' + Array.from({ length: rat.n }, (_, i) => rat.folge[i]
      ? '<button type="button" class="platz voll" data-i="' + i + '" aria-label="Platz ' + (i + 1) + ': ' + esc(rat.folge[i]) + '">' + (RAETSEL_ICON[rat.folge[i]] || esc(rat.folge[i])) + "</button>"
      : '<button type="button" class="platz" disabled aria-label="Platz ' + (i + 1) + ' leer">' + (i + 1) + "</button>").join("") + "</div>" +
    '<div class="symbole">' + namen.map((s) => '<button type="button" class="symbol" data-s="' + esc(s) + '"' + (rat.folge.includes(s) || rat.folge.length >= rat.n ? " disabled" : "") + ">" + symbolHtml(s) + "</button>").join("") + "</div>" +
    '<div class="aktionen"><button type="button" class="abbrechen">Abbrechen</button><button type="button" class="pruefen"' + (rat.folge.length < rat.n ? " disabled" : "") + ">Prüfen</button></div>";
  el.querySelectorAll(".platz.voll").forEach((b) => b.addEventListener("click", () => { rat.folge.splice(+b.dataset.i, 1); raetselZeichnen(); }));
  el.querySelectorAll(".symbol").forEach((b) => b.addEventListener("click", () => { rat.folge.push(b.dataset.s); raetselZeichnen(); }));
  el.querySelector(".abbrechen").addEventListener("click", () => { const w = rat.abbr; raetselAus(); antwort(w); });
  el.querySelector(".pruefen").addEventListener("click", () => {
    const e = rat.eintraege.find((x) => x.text === rat.folge[0]);
    if (!e || rat.folge.length < rat.n) return;
    rat.senden = true;
    el.classList.remove("an");
    antwort(e.wert);
  });
}

// Finchs Peilscheibe (Messgang in den TIEFEN): Die Kerbe wird an einem Drehkreis auf eine Markierung gestellt.
// Die Auswahl entspricht den drei Antworten des Spiels, das Spiel selbst bleibt unverändert.
const DIAL_ZIELE = [
  { re: /Kerbe auf die Kerben im Boden ausrichten/, winkel: 90, name: "Auf die Kerben im Boden" },
  { re: /Kerbe in Richtung IV-C drehen/, winkel: 210, name: "Richtung IV-C" },
  { re: /Führung quer zum Gang stellen/, winkel: 330, name: "Quer zum Gang" }
];
let dial = null;
const dialEl = () => document.getElementById("dial");
function dialAus() { dial = null; dialEl().classList.remove("an"); dialEl().replaceChildren(); }
function dialPruefen(eintraege) {
  const ziele = DIAL_ZIELE.map((z) => ({ ...z, e: eintraege.find((x) => z.re.test(x.text)) }));
  if (ziele.some((z) => !z.e)) { dialAus(); return false; }
  dial = { ziele, winkel: 0 };
  knoepfeEl.style.display = "none";
  listeAus = true; leseNeu();
  dialEl().classList.add("an");
  dialZeichnen();
  anpassen();
  return true;
}
function dialZeichnen() {
  const el = dialEl();
  const P = (w, r) => [120 + r * Math.sin(w * Math.PI / 180), 120 - r * Math.cos(w * Math.PI / 180)];
  const striche = Array.from({ length: 36 }, (_, i) => { const a = P(i * 10, 70), b = P(i * 10, 80); return '<line class="strich" x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '"/>'; }).join("");
  const marken = dial.ziele.map((z, i) => { const p = P(z.winkel, 80), t = P(z.winkel, 106); return '<circle class="marke" data-i="' + i + '" cx="' + p[0] + '" cy="' + p[1] + '" r="7"/><text class="markname" x="' + t[0] + '" y="' + (t[1] + 3) + '">' + esc(z.name) + "</text>"; }).join("");
  el.innerHTML = '<svg viewBox="-20 -6 280 252" role="img" aria-label="Peilscheibe"><circle class="scheibe" cx="120" cy="120" r="82"/>' + striche + marken +
    '<line class="zeiger" x1="120" y1="120" x2="120" y2="52"/><circle class="griff" cx="120" cy="52" r="11"/></svg>' +
    '<div class="dialtext">Drehe die Kerbe auf eine Markierung.</div><button type="button" class="einstellen" disabled>Einstellen</button>';
  const svg = el.querySelector("svg"), zeiger = el.querySelector(".zeiger"), griff = el.querySelector(".griff"), text = el.querySelector(".dialtext"), knopf = el.querySelector(".einstellen");
  const naechstes = () => {
    let best = null, abstand = 999;
    dial.ziele.forEach((z) => { const d = Math.abs(((dial.winkel - z.winkel + 540) % 360) - 180); if (d < abstand) { abstand = d; best = z; } });
    return abstand <= 22 ? best : null;
  };
  const setzen = (w) => {
    dial.winkel = w;
    const p = P(w, 68);
    zeiger.setAttribute("x2", p[0]); zeiger.setAttribute("y2", p[1]);
    griff.setAttribute("cx", p[0]); griff.setAttribute("cy", p[1]);
    const z = naechstes();
    el.querySelectorAll(".marke").forEach((m, i) => m.classList.toggle("aktiv", !!z && dial.ziele[i] === z));
    text.textContent = z ? "Die Kerbe zeigt: " + z.name : "Drehe die Kerbe auf eine Markierung.";
    knopf.disabled = !z;
  };
  const winkelAus = (e) => {
    const r = svg.getBoundingClientRect();
    // Die Mitte der Scheibe liegt bei (120, 120) im viewBox "-20 -6 280 252".
    const mx = r.left + ((120 + 20) / 280) * r.width, my = r.top + ((120 + 6) / 252) * r.height;
    let w = Math.atan2(e.clientX - mx, -(e.clientY - my)) * 180 / Math.PI;
    return w < 0 ? w + 360 : w;
  };
  let zieht = false;
  svg.addEventListener("pointerdown", (e) => { zieht = true; try { svg.setPointerCapture(e.pointerId); } catch (x) {} setzen(winkelAus(e)); e.preventDefault(); });
  svg.addEventListener("pointermove", (e) => { if (zieht) setzen(winkelAus(e)); });
  const los = () => { if (!zieht) return; zieht = false; const z = naechstes(); if (z) setzen(z.winkel); };
  svg.addEventListener("pointerup", los); svg.addEventListener("pointercancel", los);
  knopf.addEventListener("click", () => { const z = naechstes(); if (!z) return; dialAus(); antwort(z.e.wert); });
  setzen(0);
}

// Zweite Kopie der Spielstände in IndexedDB (neben dem Browser-Speicher). Fehlt im Browser-Speicher alles, wird die Wiederherstellung angeboten.
const idbSicher = {
  oeffnen() {
    return new Promise((ok, nein) => {
      const r = indexedDB.open("void-kopie", 1);
      r.onupgradeneeded = () => r.result.createObjectStore("saves");
      r.onsuccess = () => ok(r.result);
      r.onerror = () => nein(r.error);
    });
  },
  async setzen(name, text) { try { const db = await this.oeffnen(); db.transaction("saves", "readwrite").objectStore("saves").put(text, name); } catch (e) {} },
  async loeschen(name) { try { const db = await this.oeffnen(); db.transaction("saves", "readwrite").objectStore("saves").delete(name); } catch (e) {} },
  async alle() {
    try {
      const db = await this.oeffnen();
      return await new Promise((ok) => {
        const out = {}, rq = db.transaction("saves").objectStore("saves").openCursor();
        rq.onsuccess = () => { const c = rq.result; if (c) { out[c.key] = c.value; c.continue(); } else ok(out); };
        rq.onerror = () => ok({});
      });
    } catch (e) { return {}; }
  }
};
async function kopieWiederherstellen() {
  const hat = Object.keys(spielstaende()).some((n) => /^void_save_[1-3]\.json$/.test(n));
  if (hat) return;
  const k = await idbSicher.alle();
  const namen = Object.keys(k).filter((n) => /^void_(save_[1-3]|settings)\.json$/.test(n) && typeof k[n] === "string");
  const anzahl = namen.filter((n) => n.startsWith("void_save_")).length;
  if (!anzahl) return;
  if (confirm("Im Browser-Speicher fehlen deine Spielstände, aber auf diesem Gerät gibt es eine Kopie (" + anzahl + " Spielstand/Spielstände). Wiederherstellen?")) {
    namen.forEach((n) => { try { localStorage.setItem("void:" + n, k[n]); } catch (e) {} });
  }
}

// Einstellungen und Sicherung
const einstEl = document.getElementById("einst");
const meldungEl = document.getElementById("meldung");
const SLOT_NAMEN = ["void_save_1.json", "void_save_2.json", "void_save_3.json"];
function zeitText(sek) {
  sek = Math.max(0, Math.floor(+sek || 0));
  const h = Math.floor(sek / 3600), m = Math.floor((sek % 3600) / 60);
  return h ? h + " h " + m + " min" : m + " min";
}
function slotInfo(text) {
  try {
    const s = JSON.parse(text).spieler || {};
    const ort = String(s.ort || "").replace(/_/g, " ").replace(/(^|\s)\S/g, (c) => c.toUpperCase());
    return { titel: (s.name || "Unbenannt") + " · " + (ort || "?"), info: (s.gold ?? 0) + " Gold" + (s.spielzeit ? " · ⏱ " + zeitText(s.spielzeit) : "") };
  } catch (e) { return { titel: "Nicht lesbar", info: "" }; }
}
// "Bildschirm anlassen": Der Bildschirm bleibt an, solange die App sichtbar ist (Wake Lock). Beim Wechsel der App wird er neu angefordert.
let wachSperre = null;
async function wachSetzen() {
  if (!navigator.wakeLock) return;
  try {
    if (UI.wach && !wachSperre && !document.hidden) {
      wachSperre = await navigator.wakeLock.request("screen");
      wachSperre.addEventListener("release", () => { wachSperre = null; });
    } else if (!UI.wach && wachSperre) {
      const s = wachSperre; wachSperre = null; await s.release();
    }
  } catch (e) { wachSperre = null; }
}
document.addEventListener("visibilitychange", () => { if (!document.hidden) wachSetzen(); });
document.addEventListener("pointerdown", () => { if (UI.wach && !wachSperre) wachSetzen(); });
function einstellungenFuellen() {
  const st = spielstaende();
  document.getElementById("slots").innerHTML = SLOT_NAMEN.map((n, i) => {
    if (!st[n]) return '<div class="slot"><span>Platz ' + (i + 1) + '</span><small>leer</small></div>';
    const d = slotInfo(st[n]);
    return '<div class="slot"><span>Platz ' + (i + 1) + ": " + esc(d.titel) + "</span><small>" + esc(d.info) + "</small></div>";
  }).join("");
  const markieren = (id, wert) => document.querySelectorAll("#" + id + " button").forEach((b) => b.classList.toggle("gewaehlt", b.dataset.v === wert));
  markieren("gAnsicht", UI.lesen ? "lese" : "terminal");
  markieren("gSchrift", UI.serif ? "serif" : "aus");
  markieren("gFarben", UI.farben ? "an" : "aus");
  markieren("gFeld", UI.feld);
  markieren("gGross", UI.gross ? "gross" : "normal");
  markieren("gKontrast", UI.kontrast ? "hoch" : "normal");
  markieren("gVibr", UI.vibration === false ? "aus" : "an");
  markieren("gWach", UI.wach ? "an" : "aus");
  document.getElementById("wachZeile").style.display = navigator.wakeLock ? "" : "none";
  const eff = Math.round((Klang.effektLautstaerke ? Klang.effektLautstaerke() : 0.8) * 100);
  document.getElementById("effektRegler").value = eff;
  document.getElementById("effektWert").textContent = eff;
  const laut = Math.round((Klang.lautstaerke ? Klang.lautstaerke() : 0.5) * 100);
  document.getElementById("lautRegler").value = laut;
  document.getElementById("lautWert").textContent = laut;
  const ver = document.getElementById("version");
  ver.textContent = "App-Stand " + APP_STAND;
  fetch("spiel/void_version.json").then((r) => r.json()).then((v) => { ver.textContent = "Spiel: " + (v.name || v.version) + " · App-Stand " + APP_STAND; }).catch(() => {});
  offlineStandZeigen();
  idbSicher.alle().then((k) => {
    const plaetze = Object.keys(k).filter((n) => /^void_save_[1-3]\.json$/.test(n)).map((n) => n.match(/_(\d)\./)[1]).sort();
    document.getElementById("kopieInfo").textContent = plaetze.length ? "Zweite Kopie auf diesem Gerät: Platz " + plaetze.join(", ") + ". Sie hilft, wenn der Browser-Speicher beschädigt ist, nicht beim Löschen der Browserdaten." : "Noch keine zweite Kopie auf diesem Gerät (entsteht beim nächsten Speichern).";
  });
  document.getElementById("schriftRegler").value = UI.schrift;
  document.getElementById("schriftWert").textContent = UI.schrift;
  const schutz = document.getElementById("schutz");
  if (navigator.storage && navigator.storage.persisted) {
    navigator.storage.persisted().then((p) => {
      schutz.textContent = p ? "Speicher: dauerhaft geschützt, der Browser löscht ihn nicht von selbst."
        : "Speicher: nicht dauerhaft geschützt. Mit einer installierten App bleibt er in der Regel erhalten.";
    });
  }
  const alt = !UI.sicherung ? Infinity : (Date.now() - UI.sicherung) / 864e5;
  const zuletzt = UI.sicherung ? "Letzte Sicherung: " + new Date(UI.sicherung).toLocaleDateString("de-CH") + "." : "Noch nie gesichert.";
  meldungEl.textContent = zuletzt;
  einstEl.dataset.alt = alt;
}
function punktSetzen() {
  const hatStand = Object.keys(spielstaende()).some((n) => n.startsWith("void_save_"));
  const alt = !UI.sicherung ? Infinity : (Date.now() - UI.sicherung) / 864e5;
  document.getElementById("punkt").classList.toggle("an", hatStand && alt > 14);
}
// Version, Offline-Speicher und Update-Hinweis.
const APP_STAND = "2026-10-25-27";
const OFFLINE_DATEIEN = ["bilder/gegner_aschenkoenig.jpg","bilder/gegner_bandit.jpg","bilder/gegner_blasser_hirsch.jpg","bilder/gegner_blindmolch.jpg","bilder/gegner_echohirsch.jpg","bilder/gegner_einscherer.jpg","bilder/gegner_gezeitenkrebs.jpg","bilder/gegner_glutsalamander.jpg","bilder/gegner_graupelz.jpg","bilder/gegner_keiler.jpg","bilder/gegner_kohlenschmuggler.jpg","bilder/gegner_kreischer.jpg","bilder/gegner_rudelloser_wolf.jpg","bilder/gegner_schachtflatterer.jpg","bilder/gegner_schachtkriecher.jpg","bilder/gegner_schachtspinner.jpg","bilder/gegner_schieferpanzer.jpg","bilder/gegner_steinvater.jpg","bilder/gegner_waldwaechter.jpg","bilder/gegner_wolf.jpg","bilder/gegner_wrackpluenderer.jpg","bilder/npc_ahrens.jpg","bilder/npc_arvid.jpg","bilder/npc_bjorn.jpg","bilder/npc_edda.jpg","bilder/npc_elian.jpg","bilder/npc_enno.jpg","bilder/npc_finch.jpg","bilder/npc_fischer.jpg","bilder/npc_gerrit.jpg","bilder/npc_haller.jpg","bilder/npc_hilda.jpg","bilder/npc_ida.jpg","bilder/npc_ignaz.jpg","bilder/npc_joris.jpg","bilder/npc_kiran.jpg","bilder/npc_koehler.jpg","bilder/npc_levin.jpg","bilder/npc_mara.jpg","bilder/npc_marek.jpg","bilder/npc_mira.jpg","bilder/npc_nela.jpg","bilder/npc_raban.jpg","bilder/npc_rika.jpg","bilder/npc_runa.jpg","bilder/npc_schreiber.jpg","bilder/npc_selene.jpg","bilder/npc_sera.jpg","bilder/npc_tarek.jpg","bilder/npc_tomas.jpg","bilder/npc_valerie.jpg","bilder/ort_bachlauf.jpg","bilder/ort_eichenruh.jpg","bilder/ort_felsterrassen.jpg","bilder/ort_gasthaus.jpg","bilder/ort_huette.jpg","bilder/ort_koehlerei.jpg","bilder/ort_lagerfeuer.jpg","bilder/ort_lagerkeller.jpg","bilder/ort_marktplatz.jpg","bilder/ort_oros_archiv.jpg","bilder/ort_oros_halle.jpg","bilder/ort_oros_lehrhallen.jpg","bilder/ort_oros_tor.jpg","bilder/ort_pfad_des_vergessens.jpg","bilder/ort_schmiede.jpg","bilder/ort_spielerzimmer.jpg","bilder/ort_tiefen.jpg","bilder/ort_verlassenes_dorf.jpg","bilder/ort_versorgungskehre.jpg","bilder/ort_wald.jpg","bilder/ort_waldlichtung.jpg","bilder/ort_wrackstrand.jpg","klang/drinnen.ogg","klang/feuer.ogg","klang/hoehle.ogg","klang/intro.ogg","klang/kampf.ogg","klang/kueste.ogg","klang/markt.m4a","klang/taverne.ogg","klang/wald.ogg","klang/wind.ogg","klang/zimmer.ogg"];
async function offlineListe() {
  let spiel = [], medien = OFFLINE_DATEIEN;
  try { spiel = (await (await fetch("dateien.json")).json()).map((n) => "spiel/" + n); } catch (e) {}
  // offline.json entsteht bei jeder Veröffentlichung automatisch aus den Ordnern bilder/ und klang/.
  try { const m = await (await fetch("offline.json", { cache: "no-cache" })).json(); if (Array.isArray(m) && m.length) medien = m; } catch (e) {}
  return [...new Set([...medien, ...spiel, "spiel/void_version.json"])];
}
let offlineLaeuft = false;
async function offlineStandZeigen() {
  const t = document.getElementById("offlineText");
  if (!window.caches || offlineLaeuft) return;
  const liste = await offlineListe();
  let da = 0;
  for (const u of liste) { try { if (await caches.match(u, { ignoreSearch: true })) da++; } catch (e) {} }
  if (!offlineLaeuft) t.textContent = da + " von " + liste.length + " Dateien offline gespeichert.";
}
async function offlineLaden() {
  if (offlineLaeuft) return;
  offlineLaeuft = true;
  const t = document.getElementById("offlineText");
  const liste = await offlineListe();
  const warteschlange = [...liste];
  let fertig = 0, fehler = 0;
  const arbeiter = async () => {
    while (warteschlange.length) {
      const u = warteschlange.shift();
      try { const r = await fetch(u); if (r.ok) await r.arrayBuffer(); else fehler++; } catch (e) { fehler++; }
      fertig++;
      t.textContent = "Lade … " + fertig + " / " + liste.length;
    }
  };
  await Promise.all([arbeiter(), arbeiter(), arbeiter(), arbeiter()]);
  offlineLaeuft = false;
  t.textContent = fehler ? "Fertig, aber " + fehler + " Dateien fehlen. Später mit Netz noch einmal versuchen."
    : "Fertig: " + liste.length + " Dateien gespeichert. Die App läuft jetzt auch ohne Netz.";
}
async function updatePruefen() {
  try {
    const text = await (await fetch("app.js", { cache: "no-store" })).text();
    const m = text.match(/const APP_STAND = "([^"]+)"/);
    if (m && m[1] !== APP_STAND) document.getElementById("neuVersion").classList.add("an");
  } catch (e) {}
}
document.getElementById("neuLaden").addEventListener("click", () => location.reload());
setTimeout(updatePruefen, 5000);
document.addEventListener("visibilitychange", () => { if (!document.hidden) updatePruefen(); });

function einstOeffnen() {
  einstellungenFuellen();
  einstEl.classList.add("offen");
  einstEl.setAttribute("aria-hidden", "false");
  if (navigator.storage && navigator.storage.persist) navigator.storage.persist().then(() => einstellungenFuellen()).catch(() => {});
}
function einstSchliessen() {
  einstEl.classList.remove("offen");
  einstEl.setAttribute("aria-hidden", "true");
}
function sicherungText() {
  const st = spielstaende();
  if (!Object.keys(st).some((n) => n.startsWith("void_save_"))) { meldungEl.textContent = "Es gibt noch keinen gespeicherten Spielstand."; return null; }
  return JSON.stringify({ void_sicherung: 1, erstellt: new Date().toISOString(), dateien: st });
}
function sicherungBauen() {
  const text = sicherungText();
  if (!text) return null;
  const d = new Date();
  const name = "void-sicherung-" + d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0") + ".json";
  return new File([text], name, { type: "application/json" });
}
function sicherungKopieren() {
  const text = sicherungText();
  if (!text) return;
  textKopieren(text, (ok) => {
    if (ok) { UI.sicherung = Date.now(); uiSichern(); punktSetzen(); }
    meldungEl.textContent = ok ? "Sicherung als Text kopiert (" + Math.ceil(text.length / 1024) + " KB). Füge sie in eine Notiz oder Mail ein, am besten an dich selbst."
      : "Kopieren ist hier nicht möglich. Nimm „Sicherung als Datei speichern“.";
  });
}
function sichernDatei() {
  const datei = sicherungBauen();
  if (!datei) return;
  const a = document.createElement("a");
  a.href = URL.createObjectURL(datei);
  a.download = datei.name;
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 3000);
  UI.sicherung = Date.now(); uiSichern(); punktSetzen();
  meldungEl.textContent = "Sicherung gespeichert (Ordner Downloads): " + datei.name;
}
// Teilen-Dialog des Handys (Drive, WhatsApp, Mail ...); der Knopf erscheint nur, wo der Browser Dateien teilen kann.
function sicherungTeilen() {
  const datei = sicherungBauen();
  if (!datei) return;
  navigator.share({ files: [datei], title: "VOID Sicherung" }).then(() => {
    UI.sicherung = Date.now(); uiSichern(); punktSetzen();
    meldungEl.textContent = "Sicherung geteilt: " + datei.name;
  }).catch((e) => { if (e && e.name !== "AbortError") meldungEl.textContent = "Teilen nicht möglich. Nimm „Sicherung als Datei speichern“."; });
}
function einspielen(datei) {
  const leser = new FileReader();
  leser.onload = () => einspielenText(leser.result);
  leser.readAsText(datei);
}
// Gemeinsame Prüfung für Datei und eingefügten Text; bei jedem Fehler bleibt alles unverändert.
function einspielenText(inhaltText) {
  {
    try {
      const o = JSON.parse(String(inhaltText).trim());
      if (!o || o.void_sicherung !== 1 || typeof o.dateien !== "object") throw new Error("keine VOID-Sicherung");
      const namen = Object.keys(o.dateien);
      if (!namen.length || !namen.every((n) => /^void_(save_[1-3]|settings)\.json$/.test(n) && typeof o.dateien[n] === "string")) throw new Error("unbekannter Inhalt");
      namen.forEach((n) => JSON.parse(o.dateien[n]));
      const anzahl = namen.filter((n) => n.startsWith("void_save_")).length;
      if (!confirm(anzahl + " Spielstand/Spielstände einspielen? Vorhandene Spielstände auf denselben Plätzen werden ersetzt.")) return;
      sicherungLaeuft = true;
      namen.forEach((n) => { localStorage.setItem("void:" + n, o.dateien[n]); idbSicher.setzen(n, o.dateien[n]); });
      location.reload();
    } catch (e) {
      meldungEl.textContent = "Das lässt sich nicht einspielen: Es ist keine gültige VOID-Sicherung (oder der Text ist unvollständig). Es wurde nichts verändert.";
    }
  }
}
function einstellungenVerdrahten() {
  document.getElementById("einstKnopf").addEventListener("click", (e) => { e.stopPropagation(); einstOeffnen(); });
  document.getElementById("einstZu").addEventListener("click", einstSchliessen);
  einstEl.addEventListener("click", (e) => { e.stopPropagation(); if (e.target === einstEl) einstSchliessen(); });
  const gruppe = (id, tun) => document.getElementById(id).addEventListener("click", (e) => {
    const b = e.target.closest("button"); if (!b) return; tun(b.dataset.v); uiSichern(); uiAnwenden(); einstellungenFuellen();
  });
  gruppe("gAnsicht", (v) => { UI.lesen = v === "lese"; });
  gruppe("gSchrift", (v) => { UI.serif = v === "serif"; });
  gruppe("gFarben", (v) => { UI.farben = v === "an"; });
  document.getElementById("lautRegler").addEventListener("input", (e) => {
    document.getElementById("lautWert").textContent = e.target.value;
    if (Klang.lautstaerke) Klang.lautstaerke(e.target.value / 100);
  });
  document.getElementById("offline").addEventListener("click", offlineLaden);
  const effektRegler = document.getElementById("effektRegler");
  effektRegler.addEventListener("input", (e) => {
    document.getElementById("effektWert").textContent = e.target.value;
    if (Klang.effektLautstaerke) Klang.effektLautstaerke(e.target.value / 100);
  });
  effektRegler.addEventListener("change", () => { if (Klang.effekt) Klang.effekt("treffer"); });
  gruppe("gGross", (v) => { UI.gross = v === "gross"; });
  gruppe("gKontrast", (v) => { UI.kontrast = v === "hoch"; });
  document.getElementById("introNochmal").addEventListener("click", () => { einstSchliessen(); introZeigen(); });
  gruppe("gWach", (v) => { UI.wach = v === "an"; wachSetzen(); });
  wachSetzen();
  gruppe("gVibr", (v) => { UI.vibration = v === "an"; if (UI.vibration && navigator.vibrate) navigator.vibrate(30); });
  gruppe("gFeld", (v) => { UI.feld = v; feldOffen = false; document.body.classList.remove("ohnefeld"); });
  document.getElementById("schriftRegler").addEventListener("input", (e) => {
    UI.schrift = +e.target.value; document.getElementById("schriftWert").textContent = UI.schrift; uiSichern(); uiAnwenden();
  });
  document.getElementById("sichern").addEventListener("click", sichernDatei);
  const teilenKnopf = document.getElementById("teilen");
  try {
    const probe = new File(["{}"], "p.json", { type: "application/json" });
    if (navigator.share && navigator.canShare && navigator.canShare({ files: [probe] })) { teilenKnopf.hidden = false; teilenKnopf.addEventListener("click", sicherungTeilen); }
  } catch (e) {}
  document.getElementById("textKopieren").addEventListener("click", sicherungKopieren);
  document.getElementById("textEinfuegen").addEventListener("click", () => {
    const box = document.getElementById("textBox");
    box.hidden = !box.hidden;
    if (!box.hidden) document.getElementById("textFeld").focus();
  });
  document.getElementById("textEinspielen").addEventListener("click", () => {
    const t = document.getElementById("textFeld").value.trim();
    if (!t) { meldungEl.textContent = "Das Feld ist leer. Füge zuerst den kopierten Text ein."; return; }
    einspielenText(t);
  });
  document.getElementById("laden").addEventListener("click", () => document.getElementById("ladeDatei").click());
  document.getElementById("ladeDatei").addEventListener("change", (e) => { if (e.target.files[0]) einspielen(e.target.files[0]); e.target.value = ""; });
  punktSetzen();
}

async function starten() {
  if (typeof WebAssembly.Suspending !== "function") {
    statusZeile.textContent = "Dieser Browser ist zu alt für VOID. Bitte Chrome aktualisieren (Version 137 oder neuer).";
    document.body.classList.add("ladefehler");
    return;
  }
  const term = new Terminal({ convertEol: true, fontSize: UI.schrift, scrollback: 5000, disableStdin: true,
    cursorBlink: false, allowTransparency: true, theme: { background: "rgba(0,0,0,0)" } });
  const fit = new FitAddon.FitAddon();
  term.loadAddon(fit);
  term.open(document.getElementById("terminal"));
  fit.fit();

  const worker = window.__worker || new Worker("worker.js");
  let wartet = false;
  // Text seit der letzten Antwort, so wie er wirklich auf dem Bildschirm steht (ohne Schreibmaschinen-Zwischenstände).
  bildschirmZeilen = () => {
    const buf = term.buffer.active;
    const ende = buf.baseY + buf.cursorY;
    const out = [];
    for (let y = leseStart > ende ? buf.baseY : leseStart; y <= ende; y++) {
      const zeile = buf.getLine(y);
      if (!zeile) continue;
      const t = zeile.translateToString(true);
      if (zeile.isWrapped && out.length) out[out.length - 1] += t;
      else out.push(t);
    }
    return out;
  };

  anpassen = function () {
    fit.fit();
    worker.postMessage({ typ: "spalten", spalten: spaltenWert() });
  };
  termRef = term;
  term.onWriteParsed(leseNeu);
  einstellungenVerdrahten();
  uiAnwenden();
  setTimeout(anpassen, 300);
  addEventListener("resize", anpassen);

  worker.onerror = (e) => absturzZeigen("Fehler im Hintergrundprozess: " + (e.message || e));
  worker.onmessage = (e) => {
    const m = e.data;
    if (m.typ === "text") {
      absturzLauschen(m.text);
      // Bildschirm geleert: gelesen wird erst ab dem neuen Bildschirmanfang.
      const klar = m.text.lastIndexOf("\x1b[H");
      if (m.text.includes("\x1b[2J") && klar >= 0) {
        term.write(m.text.slice(0, klar + 3), () => { leseStart = term.buffer.active.baseY; bildschirmNr++; });
        term.write(m.text.slice(klar + 3));
      } else {
        term.write(m.text);
      }
    }
    else if (m.typ === "hud") hudZeigen(m.daten);
    else if (m.typ === "gegner") gegnerSetzen(m.name);
    else if (m.typ === "ziele") zieleSetzen(m.daten);
    else if (m.typ === "status") statusZeile.textContent = m.text;
    else if (m.typ === "eingabe") { wartet = true; term.write("", knoepfeBauen); }
    else if (m.typ === "speichern") {
      if (!sicherungLaeuft) { try { localStorage.setItem("void:" + m.name, m.text); } catch (err) {} idbSicher.setzen(m.name, m.text); }
      if (/^void_save_[1-3]\.json$/.test(m.name)) { UI.zuletzt = m.name; UI.gespeichert = Date.now(); uiSichern(); speicherPunktSetzen(); }
    }
    else if (m.typ === "loeschen") { if (!sicherungLaeuft) { try { localStorage.removeItem("void:" + m.name); } catch (err) {} idbSicher.loeschen(m.name); } }
    else if (m.typ === "ende") statusZeile.textContent = "Spiel beendet. Seite neu laden, um wieder zu starten.";
  };
  const dateien = await (await fetch("dateien.json", { cache: "no-cache" })).json();
  await kopieWiederherstellen();
  worker.postMessage({ typ: "start", dateien, spielstaende: spielstaende(), spalten: spaltenWert() });

  const feld = document.getElementById("eingabe");
  antwort = (zeile) => {
    if (!wartet) {
      // Text läuft noch: Tippen zeigt den Rest sofort.
      worker.postMessage({ typ: "ueberspringen" });
      return;
    }
    wartet = false;
    vorlesenStopp();
    knoepfeEl.style.display = "none";
    listeAus = true;
    term.write(zeile + "\n", () => {
      const buf = term.buffer.active;
      leseStart = buf.baseY + buf.cursorY;
      bildschirmNr++;
    });
    worker.postMessage({ typ: "zeile", text: zeile });
    anpassen();
  };
  // Tippen auf den Text zeigt laufenden Text sofort ganz an.
  document.addEventListener("click", () => {
    if (!wartet) worker.postMessage({ typ: "ueberspringen" });
  });
  new ResizeObserver(() => anpassen()).observe(document.getElementById("terminal"));

  // Eigenes Touch-Scrollen: xterm scrollt per Finger nur zeilenweise ruckelnd. Hier fließend, mit Schwung.
  const termEl = document.getElementById("terminal");
  let ty = 0, rest = 0, tempo = 0, tZeit = 0, anim = 0;
  const zeilenHoehe = () => (termEl.querySelector(".xterm-screen").clientHeight / term.rows) || 17;
  const schieben = (dy) => {
    rest += dy;
    const h = zeilenHoehe();
    const n = Math.trunc(rest / h);
    if (n) { term.scrollLines(n); rest -= n * h; }
  };
  termEl.addEventListener("touchstart", (e) => {
    cancelAnimationFrame(anim);
    ty = e.touches[0].clientY; rest = 0; tempo = 0; tZeit = e.timeStamp;
    e.stopPropagation();
  }, { capture: true, passive: true });
  termEl.addEventListener("touchmove", (e) => {
    const y = e.touches[0].clientY;
    const dy = ty - y;
    const dt = Math.max(1, e.timeStamp - tZeit);
    tempo = dy / dt;
    ty = y; tZeit = e.timeStamp;
    schieben(dy);
    e.preventDefault();
    e.stopPropagation();
  }, { capture: true, passive: false });
  termEl.addEventListener("touchend", (e) => {
    e.stopPropagation();
    const schwung = () => {
      tempo *= 0.95;
      schieben(tempo * 16);
      if (Math.abs(tempo) > 0.03) anim = requestAnimationFrame(schwung);
    };
    anim = requestAnimationFrame(schwung);
  }, { capture: true, passive: true });
  document.getElementById("leiste").addEventListener("submit", (e) => {
    e.preventDefault();
    const zeile = feld.value;
    if (wartet) feld.value = "";
    antwort(zeile);
  });
}
// Ton: Der Browser erlaubt Audio erst nach dem ersten Tippen.
const tonKnopf = document.getElementById("ton");
const tonAnzeige = () => { tonKnopf.textContent = Klang.istAn() ? "🔊" : "🔇"; };
tonAnzeige();
document.addEventListener("pointerdown", () => Klang.entsperren(), { once: true });
tonKnopf.addEventListener("click", () => { Klang.entsperren(); Klang.umschalten(); tonAnzeige(); });

// App-Installation: Service Worker für Offline-Start, Button zum Installieren.
// Der Knopf ist immer da, außer in der installierten App. Chrome bietet die Installation nicht immer sofort an;
// bis dahin erklärt der Knopf den Weg über das Browser-Menü.
let installAngebot = null;
const installKnopf = document.getElementById("install");
const alsApp = matchMedia("(display-mode: standalone)").matches || navigator.standalone;
installKnopf.hidden = !!alsApp;
addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); installAngebot = e; });
addEventListener("appinstalled", () => { installKnopf.hidden = true; });
installKnopf.addEventListener("click", async () => {
  if (!installAngebot) {
    alert("Installieren: Tippe in Chrome oben rechts auf das Menü (drei Punkte) und wähle \"App installieren\" oder \"Zum Startbildschirm hinzufügen\".");
    return;
  }
  installAngebot.prompt();
  await installAngebot.userChoice.catch(() => {});
  installAngebot = null;
});
if ("serviceWorker" in navigator) {
  addEventListener("load", () => { navigator.serviceWorker.register("sw.js").catch(() => {}); });
}
starten();
