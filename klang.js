// Ambient-Klang für VOID: wird live im Browser erzeugt (Web Audio), es sind keine Audiodateien nötig.
// Pro Ort eine Stimmung, im Kampf kommt ein Herzschlag dazu. Start erst nach dem ersten Tippen.
const Klang = (() => {
  let ctx = null, master = null, rauschen = null;
  let an = true;
  let szene = null, szeneName = "intro", kampfWunsch = false, kampfNode = null;
  let laut = 0.5; // Lautstärke der Musik 0 bis 1 (Schieberegler in den Einstellungen)
  let effLaut = 0.8, fx = null; // Lautstärke der Effekte, getrennt von der Musik
  try { an = localStorage.getItem("void:ton") !== "aus"; } catch (e) {}
  try { const v = parseFloat(localStorage.getItem("void-laut")); if (v >= 0 && v <= 1) laut = v; } catch (e) {}
  try { const v = parseFloat(localStorage.getItem("void-effekt-laut")); if (v >= 0 && v <= 1) effLaut = v; } catch (e) {}

  const ART = {
    // Ort (normalisierter Name) -> Stimmung
    intro: "intro", spielerzimmer: "zimmer", gasthaus: "taverne", schmiede: "feuer", huette: "feuer", lagerkeller: "hoehle",
    oros_halle: "drinnen", oros_archiv: "drinnen", oros_lehrhallen: "drinnen", oros_tor: "wind",
    eichenruh: "wind", marktplatz: "markt", verlassenes_dorf: "wind", wald: "wald", waldlichtung: "wald",
    bachlauf: "wald", koehlerei: "feuer", pfad_des_vergessens: "wald", wrackstrand: "kueste",
    felsterrassen: "wind", versorgungskehre: "wind", tiefen: "hoehle", lagerfeuer: "feuer",
  };

  function sicher(f) { try { return f(); } catch (e) { console.warn("Klang:", e); return null; } }

  function starten() {
    if (ctx) return;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    ctx = new AC();
    master = ctx.createGain();
    master.gain.value = an ? laut : 0;
    master.connect(ctx.destination);
    fx = ctx.createGain(); fx.gain.value = effLaut; fx.connect(master);
    const len = ctx.sampleRate * 2;
    rauschen = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = rauschen.getChannelData(0);
    let b = 0;
    for (let i = 0; i < len; i++) { const w = Math.random() * 2 - 1; b = (b + 0.02 * w) / 1.02; d[i] = b * 3.5; } // braunes Rauschen
    if (szeneName) setzen(szeneName);
    if (kampfWunsch) kampfStart();
    himmelAnwenden();
  }

  // ---- Bausteine ----
  function rausch(filterTyp, freq, q, pegel) {
    const s = ctx.createBufferSource(); s.buffer = rauschen; s.loop = true;
    const f = ctx.createBiquadFilter(); f.type = filterTyp; f.frequency.value = freq; f.Q.value = q;
    const g = ctx.createGain(); g.gain.value = pegel;
    s.connect(f); f.connect(g); s.start();
    return { quelle: s, filter: f, gain: g, aus: g };
  }
  function lfo(rate, tiefe, ziel) {
    const o = ctx.createOscillator(); o.frequency.value = rate;
    const g = ctx.createGain(); g.gain.value = tiefe;
    o.connect(g); g.connect(ziel); o.start();
    return o;
  }
  function brummen(f1, pegel) {
    const g = ctx.createGain(); g.gain.value = pegel;
    const lp = ctx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 400;
    const a = ctx.createOscillator(); a.type = "triangle"; a.frequency.value = f1;
    const b = ctx.createOscillator(); b.type = "sine"; b.frequency.value = f1 * 1.5 + 0.7;
    a.connect(lp); b.connect(lp); lp.connect(g); a.start(); b.start();
    lfo(0.05, pegel * 0.5, g.gain);
    return { oszis: [a, b], aus: g };
  }
  function zufall(minS, maxS, tun) {
    let t;
    const lauf = () => { tun(); t = setTimeout(lauf, (minS + Math.random() * (maxS - minS)) * 1000); };
    t = setTimeout(lauf, 500);
    return () => clearTimeout(t);
  }
  function knistern(ziel) {
    return zufall(0.15, 1.2, () => {
      const r = rausch("highpass", 1500 + Math.random() * 2500, 0.7, 0);
      r.aus.connect(ziel);
      const t = ctx.currentTime;
      r.gain.gain.setValueAtTime(0, t);
      r.gain.gain.linearRampToValueAtTime(0.35 + Math.random() * 0.3, t + 0.005);
      r.gain.gain.exponentialRampToValueAtTime(0.001, t + 0.05 + Math.random() * 0.06);
      r.quelle.stop(t + 0.2);
    });
  }
  function tropfen(ziel) {
    return zufall(1.5, 5, () => {
      const o = ctx.createOscillator(); o.type = "sine";
      const g = ctx.createGain(); const t = ctx.currentTime;
      const f = 700 + Math.random() * 500;
      o.frequency.setValueAtTime(f, t); o.frequency.exponentialRampToValueAtTime(f * 0.6, t + 0.12);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.12, t + 0.01); g.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
      o.connect(g); g.connect(ziel); o.start(t); o.stop(t + 0.3);
    });
  }

  // ---- Stimmungen: jede liefert { aus: Gain, raeumen: Funktion } ----
  const STIMMUNG = {
    drinnen: (ziel) => {
      const b = brummen(55, 0.10); b.aus.connect(ziel);
      const r = rausch("lowpass", 180, 0.5, 0.05); r.aus.connect(ziel);
      return { raeumen: () => { b.oszis.forEach((o) => o.stop()); r.quelle.stop(); } };
    },
    feuer: (ziel) => {
      const b = brummen(50, 0.07); b.aus.connect(ziel);
      const r = rausch("lowpass", 220, 0.5, 0.07); r.aus.connect(ziel);
      const k = knistern(ziel);
      return { raeumen: () => { b.oszis.forEach((o) => o.stop()); r.quelle.stop(); k(); } };
    },
    wald: (ziel) => {
      const w = rausch("bandpass", 420, 0.6, 0.30); w.aus.connect(ziel);
      lfo(0.07, 220, w.filter.frequency); lfo(0.11, 0.12, w.gain.gain);
      const b = brummen(46, 0.06); b.aus.connect(ziel);
      return { raeumen: () => { w.quelle.stop(); b.oszis.forEach((o) => o.stop()); } };
    },
    wind: (ziel) => {
      const w = rausch("bandpass", 520, 0.5, 0.28); w.aus.connect(ziel);
      lfo(0.09, 260, w.filter.frequency); lfo(0.06, 0.14, w.gain.gain);
      const b = brummen(52, 0.04); b.aus.connect(ziel);
      return { raeumen: () => { w.quelle.stop(); b.oszis.forEach((o) => o.stop()); } };
    },
    kueste: (ziel) => {
      const w = rausch("lowpass", 600, 0.4, 0.28); w.aus.connect(ziel);
      lfo(0.12, 0.22, w.gain.gain);
      const wi = rausch("bandpass", 700, 0.5, 0.10); wi.aus.connect(ziel);
      lfo(0.08, 0.06, wi.gain.gain);
      return { raeumen: () => { w.quelle.stop(); wi.quelle.stop(); } };
    },
    hoehle: (ziel) => {
      const b = brummen(38, 0.12); b.aus.connect(ziel);
      const r = rausch("lowpass", 120, 0.5, 0.06); r.aus.connect(ziel);
      const t = tropfen(ziel);
      return { raeumen: () => { b.oszis.forEach((o) => o.stop()); r.quelle.stop(); t(); } };
    },
  };

  // Echte Aufnahmen: liegt klang/<stimmung>.ogg oder .mp3 vor, wird sie als Schleife gespielt, sonst der erzeugte Klang.
  const dateien = {};
  function datei(name) {
    if (!(name in dateien)) {
      dateien[name] = (async () => {
        for (const ende of ["ogg", "mp3", "m4a", "wav"]) {
          try {
            const r = await fetch("klang/" + name + "." + ende);
            if (r.ok) return await ctx.decodeAudioData(await r.arrayBuffer());
          } catch (e) { /* nächste Endung */ }
        }
        return null;
      })();
    }
    return dateien[name];
  }
  function schleife(buf, ziel) {
    const s = ctx.createBufferSource(); s.buffer = buf; s.loop = true; s.connect(ziel); s.start();
    return { raeumen: () => s.stop() };
  }

  let szenenZaehler = 0;
  STIMMUNG.taverne = STIMMUNG.feuer; // ohne Aufnahme klingt die Taverne wie Feuer
  STIMMUNG.markt = STIMMUNG.wind; // ohne Aufnahme klingt der Markt wie Wind
  STIMMUNG.intro = STIMMUNG.drinnen; // Hauptmenü, bis das Spiel einen Ort setzt
  STIMMUNG.zimmer = STIMMUNG.drinnen; // ohne Aufnahme klingt das Zimmer wie ein Innenraum
  function setzen(name) {
    szeneName = name;
    if (!ctx) return;
    const art = ART[name] || "drinnen";
    if (szene && szene.art === art) return;
    const nr = ++szenenZaehler;
    datei(art).then((buf) => {
      if (nr !== szenenZaehler) return;
      const alt = szene;
      if (alt) {
        const t = ctx.currentTime;
        alt.gain.gain.cancelScheduledValues(t);
        alt.gain.gain.setValueAtTime(alt.gain.gain.value, t);
        alt.gain.gain.linearRampToValueAtTime(0, t + 2.5);
        setTimeout(() => sicher(() => alt.teile.raeumen()), 2800);
      }
      const g = ctx.createGain(); g.gain.value = 0; g.connect(master);
      g.gain.linearRampToValueAtTime(1, ctx.currentTime + 2.5);
      const teile = buf ? sicher(() => schleife(buf, g)) : sicher(() => STIMMUNG[art](g));
      szene = { art, gain: g, teile: teile || { raeumen() {} } };
    });
  }

  function kampfStart() {
    if (!ctx || kampfNode) return;
    kampfNode = { stop() {} };
    datei("kampf").then((buf) => {
      if (!kampfNode) return; // Kampf ist schon vorbei
      kampfNode = buf ? kampfDatei(buf) : kampfHerzschlag();
    });
  }
  function kampfDatei(buf) {
    const g = ctx.createGain(); g.gain.value = 0; g.connect(master);
    g.gain.linearRampToValueAtTime(0.6, ctx.currentTime + 1); // Kampfmusik etwas leiser als die Ortsklänge
    const s = ctx.createBufferSource(); s.buffer = buf; s.loop = true; s.connect(g); s.start();
    return { stop: () => { g.gain.linearRampToValueAtTime(0, ctx.currentTime + 1); setTimeout(() => s.stop(), 1200); } };
  }
  function kampfHerzschlag() {
    const o = ctx.createOscillator(); o.type = "sine"; o.frequency.value = 52;
    const g = ctx.createGain(); g.gain.value = 0;
    o.connect(g); g.connect(master); o.start();
    const schlag = () => {
      const t = ctx.currentTime;
      g.gain.cancelScheduledValues(t);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.35, t + 0.03); g.gain.exponentialRampToValueAtTime(0.001, t + 0.28);
    };
    schlag();
    const iv = setInterval(() => { schlag(); setTimeout(schlag, 230); }, 1100);
    return { stop: () => { clearInterval(iv); o.stop(); } };
  }
  function kampfEnde() { if (kampfNode) { kampfNode.stop(); kampfNode = null; } }

  // Wetter- und Nachtschicht über der Ortsstimmung (live erzeugt): Regen, Nebel, Grillen. Drinnen klingt alles gedämpft.
  let himmelWunsch = null, himmelSchicht = null;
  function himmelBauen(art, drinnen) {
    const g = ctx.createGain(); g.gain.value = 0; g.connect(master);
    let ziel = g;
    if (drinnen) { const lp = ctx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 450; lp.connect(g); ziel = lp; }
    const stopper = [];
    if (art.includes("regen")) {
      const a = rausch("highpass", 1600, 0.4, 0.07); a.aus.connect(ziel); lfo(0.13, 0.015, a.gain.gain);
      const b = rausch("bandpass", 4200, 0.8, 0.05); b.aus.connect(ziel);
      stopper.push(() => { a.quelle.stop(); b.quelle.stop(); });
    }
    if (art.includes("nebel")) {
      const n = rausch("lowpass", 260, 0.3, 0.07); n.aus.connect(ziel); lfo(0.05, 0.03, n.gain.gain);
      stopper.push(() => n.quelle.stop());
    }
    if (art.includes("nacht") && !art.includes("regen") && !drinnen) {
      stopper.push(zufall(0.5, 1.8, () => {
        const f = 4200 + Math.random() * 400;
        for (let i = 0; i < 3; i++) {
          const t = ctx.currentTime + i * 0.09;
          const o = ctx.createOscillator(); o.type = "sine"; o.frequency.value = f;
          const e = ctx.createGain(); e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(0.02, t + 0.01); e.gain.linearRampToValueAtTime(0, t + 0.05);
          o.connect(e); e.connect(ziel); o.start(t); o.stop(t + 0.07);
        }
      }));
    }
    g.gain.linearRampToValueAtTime(1, ctx.currentTime + 2.5);
    return { gain: g, raeumen: () => stopper.forEach((s) => sicher(s)) };
  }
  function himmelAnwenden() {
    if (!ctx || !himmelWunsch) return;
    const [zeit, wetter, drinnen] = himmelWunsch;
    const art = [zeit === "nacht" ? "nacht" : "", wetter === "regen" || wetter === "nebel" ? wetter : ""].filter(Boolean).join(" ");
    const schluessel = art ? art + (drinnen ? " drinnen" : "") : "";
    if ((himmelSchicht ? himmelSchicht.schluessel : "") === schluessel) return;
    const alt = himmelSchicht;
    himmelSchicht = null;
    if (alt) {
      const t = ctx.currentTime;
      alt.gain.gain.cancelScheduledValues(t);
      alt.gain.gain.setValueAtTime(alt.gain.gain.value, t);
      alt.gain.gain.linearRampToValueAtTime(0, t + 2);
      setTimeout(() => sicher(() => alt.raeumen()), 2300);
    }
    if (schluessel) { himmelSchicht = sicher(() => himmelBauen(art, drinnen)); if (himmelSchicht) himmelSchicht.schluessel = schluessel; }
  }

  // Kurze Effekte (live erzeugt, keine Dateien): Treffer, Schaden, Level-up usw.
  function ton(freq, dauer, typ, pegel, start = 0, bis = 0) {
    const t = ctx.currentTime + start;
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = typ; o.frequency.setValueAtTime(freq, t);
    if (bis) o.frequency.exponentialRampToValueAtTime(bis, t + dauer);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(pegel, t + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, t + dauer);
    o.connect(g); g.connect(fx || master); o.start(t); o.stop(t + dauer + 0.05);
  }
  function stoss(dauer, pegel, freq, start = 0) {
    const t = ctx.currentTime + start;
    const s = ctx.createBufferSource(); s.buffer = rauschen;
    const f = ctx.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = freq;
    const g = ctx.createGain();
    g.gain.setValueAtTime(pegel, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dauer);
    s.connect(f); f.connect(g); g.connect(fx || master); s.start(t); s.stop(t + dauer + 0.05);
  }
  const EFFEKTE = {
    treffer() { stoss(0.12, 0.5, 900); ton(150, 0.12, "sine", 0.5, 0, 60); },
    kritisch() { stoss(0.2, 0.7, 2600); ton(230, 0.2, "square", 0.22, 0, 80); ton(95, 0.28, "sine", 0.6, 0, 40); },
    schaden() { ton(120, 0.22, "sawtooth", 0.28, 0, 55); stoss(0.1, 0.4, 500); },
    levelup() { [523, 659, 784, 1047].forEach((f, i) => ton(f, 0.38, "triangle", 0.28, i * 0.12)); },
    sieg() { [392, 523, 659].forEach((f, i) => ton(f, 0.42, "triangle", 0.26, i * 0.14)); },
    speichern() { ton(880, 0.08, "sine", 0.2); ton(1320, 0.12, "sine", 0.18, 0.07); },
    muenzen() { [1568, 2093, 1760, 2349].forEach((f, i) => ton(f, 0.16, "triangle", 0.16, i * 0.07)); stoss(0.05, 0.12, 6000, 0.02); },
    truhe() { ton(90, 0.45, "sawtooth", 0.14, 0, 180); stoss(0.3, 0.1, 1200, 0.02); [659, 988, 1319].forEach((f, i) => ton(f, 0.3, "sine", 0.16, 0.5 + i * 0.1)); },
    tuer() { stoss(0.09, 0.45, 400); ton(70, 0.16, "sine", 0.5, 0, 45); ton(210, 0.38, "sawtooth", 0.09, 0.1, 150); }
  };

  // Läuft die Seite im Hintergrund (App gewechselt, Bildschirm aus), wird der Ton angehalten.
  document.addEventListener("visibilitychange", () => {
    if (!ctx) return;
    if (document.hidden) ctx.suspend(); else if (an) ctx.resume();
  });
  addEventListener("pagehide", () => { if (ctx) ctx.suspend(); });

  return {
    entsperren() {
      sicher(starten);
      if (!ctx) return;
      if (an && ctx.state === "suspended") ctx.resume(); else if (!an && ctx.state === "running") ctx.suspend();
    },
    ort(name) { setzen(name); },
    himmel(zeit, wetter, drinnen) {
      himmelWunsch = [String(zeit || "").toLowerCase(), String(wetter || "").toLowerCase(), !!drinnen];
      himmelAnwenden();
    },
    himmelArt() { return himmelSchicht ? himmelSchicht.schluessel : ""; },
    effekt(name) {
      if (!ctx || !an || ctx.state !== "running" || !EFFEKTE[name]) return;
      sicher(() => EFFEKTE[name]());
    },
    kampf(ein) {
      kampfWunsch = !!ein;
      if (ein) kampfStart(); else kampfEnde();
    },
    umschalten() {
      an = !an;
      try { localStorage.setItem("void:ton", an ? "an" : "aus"); } catch (e) {}
      if (ctx) {
        master.gain.linearRampToValueAtTime(an ? laut : 0, ctx.currentTime + 0.3);
        if (an) ctx.resume(); else setTimeout(() => { if (!an) ctx.suspend(); }, 500); // stumm = kein Strom für den Ton
      }
      return an;
    },
    istAn: () => an,
    effektLautstaerke(v) {
      if (v === undefined) return effLaut;
      effLaut = Math.max(0, Math.min(1, +v || 0));
      try { localStorage.setItem("void-effekt-laut", String(effLaut)); } catch (e) {}
      if (fx) fx.gain.setTargetAtTime(effLaut, ctx.currentTime, 0.05);
      return effLaut;
    },
    lautstaerke(v) {
      if (v === undefined) return laut;
      laut = Math.max(0, Math.min(1, +v || 0));
      try { localStorage.setItem("void-laut", String(laut)); } catch (e) {}
      if (ctx && an) master.gain.setTargetAtTime(laut, ctx.currentTime, 0.05);
      return laut;
    },
  };
})();
