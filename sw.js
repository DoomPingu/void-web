// Service Worker für VOID: macht die App installierbar und lässt sie auch ohne Netz starten.
// Eigene Dateien: erst Netz (immer aktuell), sonst Zwischenspeicher. Pyodide vom CDN: Zwischenspeicher zuerst.
const VERSION = "void-app-1";
const SCHALE = ["./", "index.html", "klang.js", "worker.js", "umbruch.py", "dateien.json", "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "klang/LIESMICH.txt"];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(VERSION).then((c) => Promise.all(SCHALE.map((u) => c.add(u).catch(() => {})))).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((namen) => Promise.all(namen.filter((n) => n !== VERSION).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

async function ablegen(anfrage, antwort) {
  if (antwort && (antwort.ok || antwort.type === "opaque")) {
    const c = await caches.open(VERSION);
    c.put(anfrage, antwort.clone()).catch(() => {});
  }
  return antwort;
}

self.addEventListener("fetch", (e) => {
  const a = e.request;
  if (a.method !== "GET") return;
  const url = new URL(a.url);
  if (url.origin === location.origin) {
    e.respondWith(
      fetch(a, { cache: "no-cache" }).then((r) => ablegen(a, r)).catch(() => caches.match(a, { ignoreSearch: true }).then((r) => r || Response.error()))
    );
  } else if (url.hostname === "cdn.jsdelivr.net") {
    e.respondWith(
      caches.match(a).then((r) => r || fetch(a).then((n) => ablegen(a, n)))
    );
  }
});
