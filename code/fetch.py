#!/usr/bin/env python3
"""v2 ÇEKİM — altı sorgunun organik sonuçları, TEK zaman damgasıyla.

Çerçeve: data/sampling-frame.json (30.08.2026, google.com, hl=en&gl=us).
Yayın platformları ve sponsorlu sonuçlar SERP çıkarımında zaten elenmişti.

Çekilemeyen (403, ölü, boş) LİSTEDEN DÜŞER ve düştüğü raporlanır — sessizce atlanmaz.
Dosyalar v2-<alan>[-N].html olarak yazılır; tur 3/4/5 dosyalarına DOKUNULMAZ.
"""
import subprocess, os, csv, json, datetime, time, collections
import urllib.parse as up

D = os.path.dirname(os.path.abspath(__file__))          # code/
KOK = os.path.dirname(D)                                # paketin kökü
ANLIK = os.environ.get("SNAPSHOTS", os.path.join(KOK, "snapshots"))
os.makedirs(ANLIK, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
serp = json.load(open(os.path.join(KOK, "data/sampling-frame.json"), encoding="utf-8"))

hedef = []
say = collections.Counter()
for q, urls in serp["queries"].items():
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
    f = os.path.join(ANLIK, f"v2-{ad}.html")
    open(f, "w", encoding="utf-8").write(govde)
    meta.append({"ad": ad, "url": u, "sorgu": q, "zaman": t.isoformat(), "karakter": len(govde)})
    print(f"  ok     {ad:26} http 200 · {len(govde):>8} bayt")
    time.sleep(0.6)
son = datetime.datetime.now(datetime.timezone.utc)
# Çıktı gerçek bir CSV. Çekilemeyen sayfalar SATIR OLARAK kalır (sessizce
# düşmez); sorgu ve zaman sütunları boş, status = failed_http_<kod>.
with open(os.path.join(KOK, "data/retrieval-log.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["page_id", "url", "seed_query", "retrieved_utc", "characters", "status"])
    for m in meta:
        w.writerow([m["ad"], m["url"], m["sorgu"], m["zaman"], m["karakter"], "retrieved"])
    for a, u, k, b in dusen:
        w.writerow([a, u, "", "", b, f"failed_http_{k}"])
print(f"\nalinan {len(meta)} · dusen {len(dusen)} · sure {(son-bas).seconds} sn")
print(f"pencere: {bas.strftime('%H:%M:%S')} - {son.strftime('%H:%M:%S')} UTC")
if dusen:
    print("\nDUSEN SAYFALAR (rapora girecek):")
    for a, u, k, b in dusen: print(f"  {a} · http {k} · {u}")
