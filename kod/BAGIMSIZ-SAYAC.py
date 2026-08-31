#!/usr/bin/env python3
"""BAGIMSIZ DOGRULAMA — olcum kodundan HIC parca kullanmadan yeniden yazildi.

Amac: ayni sonucu ikinci bir uygulama da veriyor mu? Vermiyorsa birinde hata var.
Kasitli olarak farkli yazildi: farkli HTML ayirma, farkli sayi deseni, farkli
link kurallari sirasi. Ayni sayiyi vermesi tesadufi olmaz.
"""
import re, io, glob, os, json, html as H

def blok_cikar(ham):
    """Etiketleri kaldirip metin uret — olcum kodundan farkli sira."""
    x = re.sub(r'(?is)<(script|style|noscript|nav|header|footer|form)[^>]*>.*?</\1>', ' ', ham)
    out = []
    for m in re.finditer(r'(?is)<(p|li|tr|blockquote)(\s[^>]*)?>(.*?)</\1>', x):
        ic = m.group(3)
        metin = H.unescape(re.sub(r'<[^>]+>', ' ', ic))
        metin = ' '.join(metin.split())
        out.append((metin, ic))
    return out

# farkli yazilmis sayi deseni — ayni seyi yakalamali
RAKAM = re.compile(r'(?:[$€£]\s?\d[\d.,]*[kKmMbB]?)|(?:\d[\d.,]*\s?%)|(?:\d+(?:\.\d+)?\s?[xX]\b)|(?:\b\d{2,}(?:[.,]\d{3})*\b)')
AYLAR = 'january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec'
def tarih_temizle(t):
    t = re.sub(r'\b(?:' + AYLAR + r')\.?\s+\d{1,2},?\s+\d{4}\b', ' ', t, flags=re.I)
    t = re.sub(r'\b\d{1,2}\s+(?:' + AYLAR + r')\.?,?\s+\d{4}\b', ' ', t, flags=re.I)
    return re.sub(r'\b(?:19|20)\d{2}\b', ' ', t)

ATLA_METIN = [
    re.compile(r'\blast (?:updated|reviewed)\b|\bpublished\b|\bposted\b|\bupdated on\b', re.I),
    re.compile(r'^\s*[✔✓•\-]?\s*[""]'),
    re.compile(r'based on our \d{4} survey', re.I),
    re.compile(r'\[(?:category|your brand|competitor|use case|task|job-to-be-done|the problem)', re.I),
    re.compile(r'\d+\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|expertise|in\b)', re.I),
    re.compile(r'brings\s+\d+\+?\s*years?', re.I),
    re.compile(r"I(?:'|’)ve\s+spent\s+the\s+last\s+\d+", re.I),
    re.compile(r'is\s+the\s+(?:Founder|Co-Founder|CEO|CTO|Head)\s+of\b', re.I),
    re.compile(r'Fortune\s+\d00\b', re.I),
    re.compile(r'\d+\s+out\s+of\s+\d+', re.I),
    re.compile(r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(?:19|20)\d\d\s*$', re.I),
]
RED_YOL = re.compile(r'/(?:signup|sign-up|register|demo|book|booking|contact|start|trial|get-started|checkout|cart|app)(?:/|$|\?)', re.I)
RED_HOST = re.compile(r'(?:calendly|savvycal|cal)\.com', re.I)
KOK = re.compile(r'^https?://[^/]+/?$')
FIYAT_YOL = re.compile(r'/(?:pricing|plans)(?:/|$|\?)', re.I)
FIYAT_METIN = re.compile(r'[$€£]\s?\d|trial|/mo\b|per month', re.I)
KENDI_URUN = re.compile(r'/(?:products?|product-tour|features?|solutions?|glossary|integrations?|platform|use-cases?)(?:/|$|\?)', re.I)
KART_CIPA = re.compile(r'^(?:read (?:post|more|article)|learn more|view (?:post|all))$', re.I)

def sozcuk(s): return {w for w in re.findall(r'[a-z0-9]{4,}', s.lower())}

def kaynakli_mi(ic, metin, alan):
    for m in re.finditer(r'(?is)<a\b[^>]*?href\s*=\s*"([^"]*)"[^>]*>(.*?)</a>', ic):
        adres, cipa_ham = m.group(1), m.group(2)
        cipa = ' '.join(H.unescape(re.sub(r'<[^>]+>', '', cipa_ham)).split())
        if not (adres.startswith('http') or (adres.startswith('/') and len(adres) > 3)):
            continue
        if RED_YOL.search(adres) or RED_HOST.search(adres):  continue
        if KART_CIPA.match(cipa.strip()):                    continue
        if KENDI_URUN.search(adres) and (adres.startswith('/') or alan in adres): continue
        if FIYAT_YOL.search(adres) and FIYAT_METIN.search(metin): return True
        if KOK.match(adres):                                 continue
        sayilar = re.findall(r'\d[\d.,]*', metin)
        if any(s and s in cipa for s in sayilar):            return True
        if len(sozcuk(cipa) & sozcuk(metin)) >= 2:           return True
    return False

sonuc = {}
for yol in sorted(glob.glob('v2-*.html')):
    ad = os.path.basename(yol)[3:-5]
    alan = ad.split('-')[0]
    ham = io.open(yol, encoding='utf-8', errors='ignore').read()
    toplam = kaynak = 0
    for metin, ic in blok_cikar(ham):
        if len(metin) < 60:                                  continue
        if any(p.search(metin) for p in ATLA_METIN):         continue
        if not RAKAM.search(tarih_temizle(metin)):           continue
        toplam += 1
        if kaynakli_mi(ic, metin, alan):                     kaynak += 1
    if toplam: sonuc[ad] = (toplam, kaynak)
json.dump(sonuc, io.open('bagimsiz-sonuc.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"bagimsiz sayac: {len(sonuc)} sayfa islendi -> bagimsiz-sonuc.json")
