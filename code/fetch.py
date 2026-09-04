#!/usr/bin/env python3
"""v2 RETRIEVAL: the organic results of six queries, under ONE timestamp.

Frame: data/sampling-frame.json (30.08.2026, google.com, hl=en&gl=us).
Publishing platforms and sponsored results were already removed when the SERPs were extracted.

Anything that cannot be fetched (403, dead, empty) DROPS OUT and the drop is reported; it is never skipped silently.
Files are written as v2-<domain>[-N].html; the round 3/4/5 files are NOT touched.
"""
import subprocess, os, csv, json, datetime, time, collections
import urllib.parse as up

D = os.path.dirname(os.path.abspath(__file__))          # code/
ROOT = os.path.dirname(D)                               # the package root
SNAPS = os.environ.get("SNAPSHOTS", os.path.join(ROOT, "snapshots"))
os.makedirs(SNAPS, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
serp = json.load(open(os.path.join(ROOT, "data/sampling-frame.json"), encoding="utf-8"))

targets = []
seen = collections.Counter()
for q, urls in serp["queries"].items():
    for u in urls:
        domain = up.urlparse(u).netloc.replace("www.", "")
        seen[domain] += 1
        name = domain if seen[domain] == 1 else f"{domain}-{seen[domain]}"
        targets.append((name, u, q))

start = datetime.datetime.now(datetime.timezone.utc)
meta, dropped = [], []
print(f"{len(targets)} pages · start {start.strftime('%H:%M:%S')} UTC\n")
for name, u, q in targets:
    t = datetime.datetime.now(datetime.timezone.utc)
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "25", u,
                        "-w", "\n@@HTTP@@%{http_code}"], capture_output=True, text=True)
    out = r.stdout or ""
    i = out.rfind("@@HTTP@@")
    code = out[i+8:].strip() if i > 0 else "0"
    body = out[:i] if i > 0 else out
    if code != "200" or len(body) < 2000:
        dropped.append((name, u, code, len(body)))
        print(f"  DROPPED {name:26} http {code} · {len(body)} bytes")
        continue
    f = os.path.join(SNAPS, f"v2-{name}.html")
    open(f, "w", encoding="utf-8").write(body)
    meta.append({"name": name, "url": u, "query": q, "time": t.isoformat(), "characters": len(body)})
    print(f"  ok      {name:26} http 200 · {len(body):>8} bytes")
    time.sleep(0.6)
end = datetime.datetime.now(datetime.timezone.utc)
# The output is a real CSV. Pages that could not be fetched stay AS ROWS (they
# do not vanish); query and time columns empty, status = failed_http_<code>.
with open(os.path.join(ROOT, "data/retrieval-log.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["page_id", "url", "seed_query", "retrieved_utc", "characters", "status"])
    for m in meta:
        w.writerow([m["name"], m["url"], m["query"], m["time"], m["characters"], "retrieved"])
    for a, u, k, b in dropped:
        w.writerow([a, u, "", "", b, f"failed_http_{k}"])
print(f"\nretrieved {len(meta)} · dropped {len(dropped)} · elapsed {(end-start).seconds} s")
print(f"window: {start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')} UTC")
if dropped:
    print("\nDROPPED PAGES (these go into the report):")
    for a, u, k, b in dropped: print(f"  {a} · http {k} · {u}")
