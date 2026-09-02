#!/usr/bin/env python3
"""Kor kodlama sayfasi: her iddia blogunu metni ve linkleriyle doker.
Aracin hukmu AYRI dosyaya yazilir; kodlayan onu gormez."""
import io, re, os, json, html, glob, random, importlib.util, sys
# --- path layout (identical in every script in this package) --------------
_D   = os.path.dirname(os.path.abspath(__file__))     # code/
KOK  = os.path.dirname(_D)                            # the package root
# Snapshots are not published in the package; derived working files are
# written there as well, so they cannot be mistaken for published data.
ANLIK = os.environ.get("SNAPSHOTS", os.path.join(KOK, "snapshots"))


spec = importlib.util.spec_from_file_location("ins", os.path.join(_D, "measure.py"))
ins = importlib.util.module_from_spec(spec); spec.loader.exec_module(ins)

havuz = []
for f in sorted(glob.glob(os.path.join(ANLIK, "v2-*.html"))):
    alan = os.path.basename(f)[3:-5]
    h = open(f, encoding="utf-8", errors="ignore").read()
    for i, (tur, txt, ham) in enumerate(ins.bloklar(h)):
        if len(txt) < 60 or not ins.SAYI.search(txt):
            continue
        linkler = [{"href": m.group(1),
                    "anchor": re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()}
                   for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', ham, re.S | re.I)]
        havuz.append({
            "id": f"{alan}#{i}", "page": alan, "element": tur,
            "text": txt[:700], "links": linkler,
            "_machine": bool(ins.linkli(ham, txt, alan)),
        })

random.seed(20260901)
ornek = random.sample(havuz, min(120, len(havuz)))
json.dump([{k: v for k, v in b.items() if k != "_machine"} for b in ornek],
          io.open(os.path.join(ANLIK, "blind-sample-120-BOS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({b["id"]: b["_machine"] for b in ornek},
          io.open(os.path.join(ANLIK, "instrument-verdicts.json"), "w", encoding="utf-8"), indent=1)
print(f"havuz {len(havuz)} blok · orneklem {len(ornek)}")
print(f"  kor sayfa    -> BOS kodlama sayfasi (aracin hukmu YOK)")
print(f"  makine hukmu -> instrument-verdicts.json (kodlama bitince acilacak)")

# UYARI: bu betik BOS kodlama sayfasi uretir. Yayinlanan
# coding/blind-sample-120.json TAMAMLANMIS sayfadir: insan kodlari (code) ve
# aracin hukmu (instrument_said_sourced) kodlama bittikten SONRA eklendi.
# Betigin ciktisi bilerek ANLIK klasorune yazilir; yayinlanan dosyanin uzerine
# yazilmaz, cunku bu 120 insan kodunu silerdi.
