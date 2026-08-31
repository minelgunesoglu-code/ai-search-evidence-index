#!/usr/bin/env python3
"""v2 ÇEKİM — altı sorgunun organik sonuçları, TEK zaman damgasıyla.

Çerçeve: serp-v2.json (30.08.2026, google.com, hl=en&gl=us).
Yayın platformları ve sponsorlu sonuçlar SERP çıkarımında zaten elenmişti.

Çekilemeyen (403, ölü, boş) LİSTEDEN DÜŞER ve düştüğü raporlanır — sessizce atlanmaz.
Dosyalar v2-<alan>[-N].html olarak yazılır; tur 3/4/5 dosyalarına DOKUNULMAZ.
"""
import subprocess, os, json, datetime, time, collections
import urllib.parse as up

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
serp = json.load(open(os.path.join(D, "serp-v2.json"), encoding="utf-8"))

hedef = []
say = collections.Counter()
for q, urls in serp["sorgular"].items():
    for u in urls:
        alan = up.urlparse(u).netloc.replace("www.", "")
        say[alan] += 1
        ad = alan if say[alan] == 1 else f"{alan}-{say[alan]}"
        hedef.append((ad, u, q))

bas = datetime.datetime.now(datetime.timezone.utc)
meta, dusen = [], []
print(f"{len(hedef)} sayfa · baslangic {bas.strftime('%H:%M:%S')} UTC\n")
for ad, u, q in hedef:
    t = datetime.datetime.now(datetime.timezone.utc)
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "25", u,
                        "-w", "\n@@HTTP@@%{http_code}"], capture_output=True, text=True)
    out = r.stdout or ""
    i = out.rfind("@@HTTP@@")
    kod = out[i+8:].strip() if i > 0 else "0"
    govde = out[:i] if i > 0 else out
    if kod != "200" or len(govde) < 2000:
        dusen.append((ad, u, kod, len(govde)))
        print(f"  DUSTU  {ad:26} http {kod} · {len(govde)} bayt")
        continue
    f = os.path.join(D, f"v2-{ad}.html")
    open(f, "w", encoding="utf-8").write(govde)
    meta.append({"ad": ad, "url": u, "sorgu": q, "zaman": t.isoformat(), "bayt": len(govde)})
    print(f"  ok     {ad:26} http 200 · {len(govde):>8} bayt")
    time.sleep(0.6)
son = datetime.datetime.now(datetime.timezone.utc)
json.dump({"cekim_penceresi": [bas.isoformat(), son.isoformat()],
           "alinan": len(meta), "dusen": [{"ad": a, "url": u, "http": k, "bayt": b} for a, u, k, b in dusen],
           "sayfalar": meta},
          open(os.path.join(D, "v2-cekim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nalinan {len(meta)} · dusen {len(dusen)} · sure {(son-bas).seconds} sn")
print(f"pencere: {bas.strftime('%H:%M:%S')} - {son.strftime('%H:%M:%S')} UTC")
if dusen:
    print("\nDUSEN SAYFALAR (rapora girecek):")
    for a, u, k, b in dusen: print(f"  {a} · http {k} · {u}")
