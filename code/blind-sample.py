#!/usr/bin/env python3
"""Blind coding sheet: dumps every claim block with its text and its links.
The instrument's verdict is written to a SEPARATE file; the coder does not see it."""
import io, re, os, json, html, glob, random, importlib.util, sys
# --- path layout (identical in every script in this package) --------------
_D   = os.path.dirname(os.path.abspath(__file__))     # code/
ROOT = os.path.dirname(_D)                            # the package root
# Snapshots are not published in the package; derived working files are
# written there as well, so they cannot be mistaken for published data.
SNAPS = os.environ.get("SNAPSHOTS", os.path.join(ROOT, "snapshots"))


spec = importlib.util.spec_from_file_location("ins", os.path.join(_D, "measure.py"))
ins = importlib.util.module_from_spec(spec); spec.loader.exec_module(ins)

pool = []
for f in sorted(glob.glob(os.path.join(SNAPS, "v2-*.html"))):
    domain = os.path.basename(f)[3:-5]
    h = open(f, encoding="utf-8", errors="ignore").read()
    for i, (kind, txt, raw) in enumerate(ins.blocks(h)):
        if len(txt) < 60 or not ins.NUMBER.search(txt):
            continue
        links = [{"href": m.group(1),
                  "anchor": re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()}
                 for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S | re.I)]
        pool.append({
            "id": f"{domain}#{i}", "page": domain, "element": kind,
            "text": txt[:700], "links": links,
            "_machine": bool(ins.sourced(raw, txt, domain)),
        })

random.seed(20260901)
sample = random.sample(pool, min(120, len(pool)))
json.dump([{k: v for k, v in b.items() if k != "_machine"} for b in sample],
          io.open(os.path.join(SNAPS, "blind-sample-120-EMPTY.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({b["id"]: b["_machine"] for b in sample},
          io.open(os.path.join(SNAPS, "instrument-verdicts.json"), "w", encoding="utf-8"), indent=1)
print(f"pool {len(pool)} blocks · sample {len(sample)}")
print(f"  blind sheet       -> EMPTY coding sheet (the instrument's verdict is NOT in it)")
print(f"  machine verdicts  -> instrument-verdicts.json (to be opened once coding is finished)")

# WARNING: this script produces an EMPTY coding sheet. The published
# coding/blind-sample-120.json is the COMPLETED sheet: the human codes (code) and
# the instrument's verdict (instrument_said_sourced) were added AFTER the coding
# was finished. The script's output is written to the SNAPSHOTS folder on purpose;
# it does not overwrite the published file, because that would erase the 120
# human codes.
