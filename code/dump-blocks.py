#!/usr/bin/env python3
"""Bir sayfanin butun A kademesi iddialarini elle okunacak bicimde doker."""
import re, io, os, sys, html

# --- yol düzeni (paketteki bütün betiklerde aynı) ------------------------
_D   = os.path.dirname(os.path.abspath(__file__))     # code/
KOK  = os.path.dirname(_D)                            # paketin kökü
# Anlık görüntüler pakette yayınlanmıyor; türetilmiş çalışma dosyaları da
# oraya yazılır ki yayınlanan veriyle karışmasın.
ANLIK = os.environ.get("SNAPSHOTS", os.path.join(KOK, "snapshots"))

SAYI = re.compile(r'(?<![\w.])(?:\$\s?\d[\d,]*(?:\.\d+)?(?:\s?[kKmMbB]\b)?|\d+(?:\.\d+)?\s?%|\d+(?:\.\d+)?\s?x\b|\b\d{2,}(?:,\d{3})*\b|\b\d+\s+(?:engines?|sources?|prompts?|questions?|tools?|models?|domains?|platforms?|queries|sites?|brands?|weeks?|months?|days?|runs?|citations?)\b)', re.I)
AY = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*'
TARIH = re.compile(r'(last (updated|reviewed)|published|posted|updated on)\b', re.I)
SABLON = re.compile(r'^\s*[✔✓•\-]?\s*["“]|based on our \d{4} survey|\[(category|your brand|competitor|use case|task|job-to-be-done|the problem)', re.I)
BIYO = re.compile(r"\b\d+\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|expertise|in\b)|\bbrings\s+\d+\+?\s*years?|\bI(?:'|’)ve\s+spent\s+the\s+last\s+\d+|\bis\s+the\s+(?:Founder|Co-Founder|CEO|CTO|Head)\s+of\b|\bFortune\s+\d00\b", re.I)
ORNEK = re.compile(r"\b\d+\s+out\s+of\s+\d+\b", re.I)
TARIH2 = re.compile(r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(?:19|20)\d\d\s*$", re.I)
ANA = re.compile(r'https?://[^/]+/?$')
FIYATSAYFA = re.compile(r'/(pricing|plans)(?:/|$|\?)', re.I)
FIYATIDDIA = re.compile(r'[\$€£]\s?\d|\btrial\b|/mo\b|per month', re.I)
CTA = re.compile(r'/(signup|sign-up|register|demo|book|booking|contact|start|trial|get-started|checkout|cart|app)(?:/|$|\?)|calendly\.com|savvycal\.com|cal\.com', re.I)
URUN = re.compile(r'/(products?|product-tour|features?|solutions?|glossary|integrations?|platform|use-cases?)(?:/|$|\?)', re.I)
KART = re.compile(r'^\s*(read (post|more|article)|learn more|view (post|all))\s*$', re.I)
def kel(s): return set(re.findall(r'[a-z0-9]{4,}', s.lower()))
def linkli(ham, c, alan):
    cum = kel(c)
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', ham, re.S | re.I):
        u = m.group(1)
        if not (u.startswith("http") or (u.startswith("/") and len(u) > 3)): continue
        cip = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
        if CTA.search(u) or KART.match(cip): continue
        if URUN.search(u) and (u.startswith('/') or alan in u): continue
        if FIYATSAYFA.search(u) and FIYATIDDIA.search(c): return u, cip, "F-fiyat"
        if ANA.match(u): continue
        say = re.findall(r'\d[\d,.]*', c)
        if any(s and s in cip for s in say): return u, cip, "D-sayı"
        if len(kel(cip) & cum) >= 2: return u, cip, "D-kelime"
    return None, None, None
if len(sys.argv) < 2:
    raise SystemExit("kullanım: python3 code/dump-blocks.py <page_id>\n"
                     "  örnek : python3 code/dump-blocks.py ahrefs.com\n"
                     "  page_id değerleri: data/results.csv")
ad = sys.argv[1]; alan = ad.split('-')[0]
h = io.open(os.path.join(ANLIK, f'v2-{ad}.html'), encoding='utf-8', errors='ignore').read()
h = re.sub(r'(?is)<(script|style|nav|header|footer|form|noscript)\b.*?</\1>', ' ', h)
n = 0
print(f"=== {ad} ===")
for m in re.finditer(r'(?is)<(p|li|tr|blockquote)\b[^>]*>(.*?)</\1>', h):
    ham = m.group(2)
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', ham))).strip()
    if len(t) < 60 or TARIH.search(t) or SABLON.search(t): continue
    if BIYO.search(t) or ORNEK.search(t) or TARIH2.search(t.strip()): continue
    t2 = re.sub(AY + r'\.?\s+\d{1,2},?\s+(?:19|20)\d\d', ' ', t, flags=re.I)
    t2 = re.sub(r'\b(?:19|20)\d\d\b', ' ', t2)
    v = sorted(set(SAYI.findall(t2)))
    if not v: continue
    u, cip, kural = linkli(ham, t, alan)
    if not u: continue
    n += 1
    print(f"{n:3}. [{kural}] {v[0]}")
    print(f"     '{(cip or '')[:46]}' -> {u[:78]}")
    print(f"     {t[:126]}")
print(f"toplam A: {n}")
