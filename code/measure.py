#!/usr/bin/env python3
"""EVIDENCE INDEX CODER v1.7
=============================
The measurement instrument of The AI Search Evidence Index. Version 1.7, 31 August 2026.
THIS VERSION PRODUCED THE PUBLISHED TABLE. Revision history: notes/instrument-revisions.md.

v1.2 (30 August) WAS VALIDATED: 46 of a 92-claim sample were coded by hand
(the human judgement being "does the link in this block ACTUALLY source this number").

  VALIDITY MEASURED AT v1.2: 82% agreement with the human coding (32 of 39 codable claims)
  · false positives 2  (said there was a source, there was not)
  · missed          5  (there was a source, it did not see it)

v1.7's reliability was measured on a separate and wider sample (120 blocks,
kappa = 0.85): coding/blind-sample-120.json and notes/reliability.md.

False positives were kept low DELIBERATELY: in a study that publishes scores under
company names, saying "it has a source" and being wrong is far more damaging than
missing one. A looser setting that held 82% but raised false positives to 6 was
tried and REJECTED.

DIFFERENCE FROM v1.1:
 D. ANCHOR RULE: a link counts as a source if its anchor text either contains the
    number itself or shares at least 2 meaningful words with the claim sentence.
    v1.1 said "there is a link in the block"; hand checking made that 38% wrong
    (an Otterly link for a Rankscale price, an investor's home page for a $35M
    round, and so on).
 E. A BARE HOME PAGE DOES NOT COUNT: a pathless link such as "seranking.com" does
    not evidence that number.
 F. PRICING-PAGE EXCEPTION: if the claim is a price and the link goes to /pricing
    or /plans, it counts as a source (even when the anchor text does not match).

TRIED AND REJECTED: the rule "a link to the site's own pages does not count"
DROPPED agreement from 77% to 54%. Linking to your own study or your own pricing
page is a legitimate source. The intuition was wrong; the measurement corrected it.

DIFFERENCE FROM v1.0 (three defects found in verification by hand):
 A. A THIRD TIER: "source named, no link" is no longer counted as zero. v1.0 was
    binary; llmrefs.com named its sources (Vercel, Brandlight) but came out at 0%.
    Our own codebook already contained this class.
 B. TEMPLATE AND EXAMPLE BLOCKS REMOVED: quoted patterns offered to the reader as
    "write it like this" are not claims (found on obapr.com and ayzeo.com).
 C. THRESHOLD: pages with fewer than 10 claims get NO PERCENTAGE, only the raw
    count. "33%" on 3 claims is statistically empty.

WHY VERSIONS: when a rule changes, the number changes. On 30 August we changed it
twice and the competitor median moved 5% -> 11% -> 19%; the pages were the same,
the rule changed. Every published figure is labelled "measured with v1.0" so it
stays reproducible. If a rule changes, v1.1 opens; the old figures do not become
invalid, it is written down which instrument measured them.

v1.0 RULES (frozen):
 1. Block types: p, li, tr, blockquote, h1-h6
 2. NOT A CLAIM: heading blocks · date lines ("last updated" and the like) ·
    blocks shorter than 60 characters · year and date patterns
 3. A numeric claim: a price, a percentage, a multiplier, a number of 2+ digits,
    "N engines/sources/questions"
 4. REACHABLE: the block contains an http or a site-internal (/) link
 5. TABLE RULE: a linked paragraph shorter than 400 characters immediately
    adjacent to table rows (within 2 blocks) covers all rows of that table
 6. Price claims are reported separately

KNOWN LIMIT, NOT CLOSED in v1.0:
 Rule 4 says "there is a link in the block", not "that link sources THIS number".
 In a hand check of 40 claims on 30.08, 7 of 20 "reachable" verdicts were wrong.
 The rate v1.0 produces is therefore an UPPER BOUND, with a measured error of
 about 35%. The report has to present it that way. Closing it requires human coding.

--- original note ---
ROUND 3 MEASUREMENT: the cleaned instrument.

Verification by hand (30.08, 40 claims) found two defects, both closed here:

  Error 2 - things that were not claims were being counted: a page title
           ("19 Best AI Tools"), a date line ("Last updated 12 June"), a worked
           example, a short label.
           FIX: heading blocks, date lines and blocks shorter than 60 characters
           are not claims.

  Error 1 - "there is a link in the block" is not "that link sources this number".
           Wrong 7 times in 20 examples. THIS COULD NOT BE CLOSED (it needs human
           judgement). CONSEQUENCE: the "reachable" rate is an UPPER BOUND, with
           an error margin of about 35%. The report has to present it that way.

Table rule (decided 29.08): a linked source note adjacent to a table also covers
that table's rows. Applied IDENTICALLY to every site.
"""
import re, io, os, csv, json, glob, html, collections, statistics as st

D = os.path.dirname(os.path.abspath(__file__))          # code/
KOK = os.path.dirname(D)                                # the package root
# Snapshots (v2-*.html) are NOT published in the package, for copyright reasons.
# Take your own with code/fetch.py, or point at a folder with SNAPSHOTS.
ANLIK = os.environ.get("SNAPSHOTS", os.path.join(KOK, "snapshots"))

SAYI = re.compile(
    r'(?<![\w.])(?:'
    r'\$\s?\d[\d,]*(?:\.\d+)?(?:\s?[kKmMbB]\b)?'
    r'|\d+(?:\.\d+)?\s?%'
    r'|\d+(?:\.\d+)?\s?x\b'
    r'|\b\d{2,}(?:,\d{3})*\b'
    r'|\b\d+\s+(?:engines?|sources?|prompts?|questions?|tools?|models?|domains?|'
    r'platforms?|queries|sites?|brands?|weeks?|months?|days?|runs?|citations?)\b'
    r')', re.I)
AY = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*'
TARIH = re.compile(r'(last (updated|reviewed)|published|posted|updated on)\b', re.I)
# (B) sablon/ornek blogu: okura verilen kalip cumle
# (J) v1.7 (31.08) — IDDIA OLMAYAN bloklar. 30 maddelik elle kodlamada 7'si
# gercek iddia degildi (%23) ve 7'nin 6'si LINKSIZ — payda sisiyor, pay sismiyor:
# butun yuzdeler oldugundan DUSUK cikiyordu (havuz %37 -> %46 duzeltilince).
# Yalniz MEKANIK olarak kesin olanlar elenir; "tavsiye cumlesi" gibi hukum
# gerektirenler ELENMEZ, kalan hata orani raporda yazilir.
BIYOGRAFI = re.compile(
    r"\b\d+\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|expertise|in\b)"
    r"|\bbrings\s+\d+\+?\s*years?"
    r"|\bI(?:'|\u2019)ve\s+spent\s+the\s+last\s+\d+"
    r"|\bis\s+the\s+(?:Founder|Co-Founder|CEO|CTO|Head)\s+of\b"
    r"|\bFortune\s+\d00\b", re.I)
ORNEKORAN = re.compile(r"\b\d+\s+out\s+of\s+\d+\b", re.I)
TARIH2 = re.compile(r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(?:19|20)\d\d\s*$", re.I)
SABLON = re.compile(r'^\s*[✔✓•\-]?\s*["“]|based on our \d{4} survey|\[(category|your brand|competitor|'
                    r'use case|task|job-to-be-done|the problem)', re.I)
# (A) kaynak ADI var ama link yok
# v1.4 (30.08) — 30 maddelik elle kodlamada v1.3 %73 verdi. Iki KANITLI hata:
#   1) 'according to' desende kucuk harfliydi; 'According to BrightEdge' KACIYORDU
#   2) 'predicts/forecasts' fiilleri yoktu; 'Gartner predicts' KACIYORDU
# Denenip GERI ALINANLAR (korpusta yanlis alarm urettiler, 2.347 blokta olculdu):
#   - shows/notes/states/finds  -> 'It shows the top 20 competitors', 'Page Analytics
#     shows', 'This shows Warby Parker' hepsi kaynak sanildi
#   - buyuk harfli alan adi     -> arac karsilastirma yazilarinda her urun adina atesledi
#   - "X's own \w+"             -> tablo hucrelerinde atesledi
# Kalan uyum: 25/30 = %83. Kapatilamayanlarin 4'u ayni sinif: fiyat iddiasinda
# saticinin kendi adi (Profound $399, Frase $39). Bu yuzden B kademesi RAPORDA
# YUZDE OLARAK YAYINLANMAZ; yalnizca isaret + elle dogrulanmis ornek verilir.
ADI = re.compile(
    r'\b[a-z0-9][a-z0-9-]{2,}\.(?:com|ai|org|io|net|co|dev)\b'
    r'|[Aa]ccording to\b|\bper\s+[A-Z]|[Cc]ited by\b'
    r'|\b[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)?\s+(?:found|reports?|reported|says?|said|'
    r'suggests?|estimates?|puts?|measured|published|analy[sz]ed|predicts?|forecasts?)\b'
    r"|\([A-Z][A-Za-z&.\-/' ]{2,60}?,[^)]{0,60}?(?:19|20)\d\d\)"
    r"|\b[A-Z][A-Za-z]+(?:'s|\u2019s)\s+(?:data|study|research|analysis|survey|report|audit|benchmark|figures?|numbers?)\b"
    r"|(?<=[a-z,;:] )[A-Z][A-Za-z]+(?:-(?:led|backed|funded|run))?\s+(?:[A-Z][A-Za-z]*\s)?(?:study|survey|benchmark|dataset)\b"
    r'|\b(?:study|research|survey|analysis|report|data|edition)\s+(?:of|by|from)\s+[A-Z]')
FIYAT = re.compile(r'\$\s?\d')

def bloklar(h):
    h = re.sub(r'(?is)<(script|style|nav|header|footer|form|noscript)\b.*?</\1>', ' ', h)
    out = []
    for m in re.finditer(r'(?is)<(p|li|tr|h[1-6]|blockquote)\b[^>]*>(.*?)</\1>', h):
        tur, ham = m.group(1).lower(), m.group(2)
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', ham))).strip()
        if len(txt) >= 12:
            out.append((tur, txt, ham))
    return out

DUR = set("the a an of in on for to and or is are was were with by from that this it its as at".split())
ANA = re.compile(r'https?://[^/]+/?$')
FIYATSAYFA = re.compile(r'/(pricing|plans)(?:/|$|\?)', re.I)
# v1.5 (30.08) — CTA/randevu linkleri KAYNAK DEGILDIR. Elle kontrolde visiblie.com'un
# uc 'linkli iddiasi'nin ucu de 'Start Free Trial' dugmesiydi ('14-day trial' sayisi
# /signup linkine eslendi); data-mania'nin biri savvycal randevu linkiydi.
CTA = re.compile(r'/(signup|sign-up|register|demo|book|booking|contact|start|trial|get-started|checkout|cart|app)(?:/|$|\?)|calendly\.com|savvycal\.com|cal\.com', re.I)
# ILGILI-YAZI KARTI — 'Read Post' / 'Read more' cipali bloklar navigasyondur, iddia degil.
# nav43.com'un uc 'linkli iddiasi'nin ucu de yazi altindaki ilgili-yazi kutusuydu.
# (I) v1.6 (31.08) — URUN / SOZLUK sayfasi kaynak DEGILDIR.
# Elle kontrolde hubspot.com'un dort "kaynakli" iddiasinin dordu de kendi urun
# sayfasina (hubspot.com/products/aeo) gidiyordu; digitalapplied'in tek iddiasi
# kendi sozluk sayfasina. Buna karsilik similarweb'in kendi ARASTIRMA raporuna
# (similarweb.com/corp/reports/...) ve tryprofound'un kendi VAKA calismasina
# (/customers/...) link vermesi mesrudur — yayinlanmis kaynaga goturuyor.
URUN = re.compile(r'/(products?|product-tour|features?|solutions?|glossary|integrations?|platform|use-cases?)(?:/|$|\?)', re.I)
KART = re.compile(r'^\s*(read (post|more|article)|learn more|view (post|all))\s*$', re.I)
FIYATIDDIA = re.compile(r'[\$€£]\s?\d|\btrial\b|/mo\b|per month', re.I)

def kelime(s):
    return {w for w in re.findall(r"[a-z]{3,}", (s or "").lower()) if w not in DUR}

def linkli(ham, cumle="", ALAN=None):
    """(D)(E)(F) — link BU rakami kaynakliyor mu? Bkz. v1.2 notu."""
    cum = kelime(cumle)
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', ham, re.S | re.I):
        u = m.group(1)
        if not (u.startswith("http") or (u.startswith("/") and len(u) > 3)):
            continue
        cip = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
        if CTA.search(u): continue                      # (G) v1.5 CTA/randevu = kaynak degil
        if URUN.search(u) and (u.startswith('/') or (ALAN and ALAN in u)):
            continue                                    # (I) v1.6 KENDI urun/sozluk sayfasi
        if KART.match(cip): continue                    # (H) v1.5 ilgili-yazi karti
        if FIYATSAYFA.search(u) and FIYATIDDIA.search(cumle):      # (F)
            return True
        if ANA.match(u):                                            # (E)
            continue
        say = re.findall(r'\d[\d,.]*', cumle)
        if any(s and s in cip for s in say):                        # (D) cipa sayiyi iceriyor
            return True
        if len(kelime(cip) & cum) >= 2:                             # (D) cipa cumleyle ortak
            return True
    return False

def olc(h, ALAN=None):
    bl = bloklar(h)
    # table rule: give credit if a short linked paragraph sits next to the tr block
    kredi = [False] * len(bl)
    for i, (tur, txt, ham) in enumerate(bl):
        if tur != "tr":
            continue
        a = i
        while a > 0 and bl[a-1][0] == "tr": a -= 1
        b = i
        while b < len(bl)-1 and bl[b+1][0] == "tr": b += 1
        for j in (a-1, a-2, b+1, b+2):
            if 0 <= j < len(bl) and bl[j][0] in ("p", "li") and linkli(bl[j][2], bl[j][1]) and len(bl[j][1]) < 400:
                kredi[i] = True
                break
    n = a_ = 0
    fn = fa = 0
    adli = 0                                   # (A) kaynak adi var, link yok
    for i, (tur, txt, ham) in enumerate(bl):
        if tur.startswith("h") or TARIH.search(txt) or len(txt) < 60:
            continue                                   # not a claim
        if SABLON.search(txt):
            continue                                   # (B) okura verilen kalip
        if BIYOGRAFI.search(txt) or ORNEKORAN.search(txt) or TARIH2.search(txt.strip()):
            continue                                   # (J) v1.7 iddia degil
        t2 = re.sub(AY + r'\.?\s+\d{1,2},?\s+(?:19|20)\d\d', ' ', txt, flags=re.I)
        t2 = re.sub(r'\d{1,2}\s+' + AY + r'\.?\s+(?:19|20)\d\d', ' ', t2, flags=re.I)
        t2 = re.sub(r'\b(?:19|20)\d\d\b', ' ', t2)
        ok = linkli(ham, txt, ALAN=ALAN) or kredi[i]
        advar = bool(ADI.search(txt))
        vs = set(SAYI.findall(t2))
        if not vs: continue
        if all(FIYAT.search(v) for v in vs):
            fn += 1; fa += ok
        else:
            n += 1; a_ += ok
            if not ok and advar: adli += 1          # (A)
    return n, a_, fn, fa, adli

# The measurement runs only when this file is executed DIRECTLY. blind-sample.py
# imports this module for the rule definitions; importing it must NOT overwrite
# the published data/measurement-by-block.json.
if __name__ == "__main__":
    with io.open(os.path.join(KOK, "data/retrieval-log.csv"), encoding="utf-8") as fh:
        cek = [r for r in csv.DictReader(fh)]
    alinan = [r for r in cek if r["status"] == "retrieved"]
    kume = {r["page_id"]: r["seed_query"] for r in alinan}
    # Retrieval window = from the FIRST fetch's timestamp to the LAST one's. This is
    # reproducible because its only source is the published retrieval-log.csv.
    # NOTE: the window in the first published file came from fetch.py's own start and
    # end times and included the download time of the last page (85.4 s); the one
    # derived here is 83.6 s. The article's "inside 86 seconds" holds for both.
    # Detail: notes/instrument-revisions.md v1.8.
    zaman = sorted(r["retrieved_utc"] for r in alinan)
    pencere = [zaman[0], zaman[-1]]

    rows = []
    anlik = sorted(glob.glob(os.path.join(ANLIK, "v2-*.html")))
    if not anlik:
        raise SystemExit(f"No snapshots found: {ANLIK}\n"
                         f"Fetch your own with code/fetch.py, or pass SNAPSHOTS=<folder>.")
    for f in anlik:
        ad = os.path.basename(f)[3:-5]
        n, a, fn, fa, adli = olc(io.open(f, encoding="utf-8", errors="ignore").read(), ALAN=ad.split("-")[0])
        if n + fn < 3:
            print(f"  ATLANDI (3'ten az iddia): {ad}")
            continue
        rows.append({"page_id": ad, "seed_query": kume.get(ad, "?"),
                     "blocks_with_numeric_claim": n, "blocks_sourced": a,
                     "blocks_source_named_not_linked": adli,
                     "price_claims": fn, "price_claims_sourced": fa})

    def pct(a, b): return 100*a/b if b else None

    ESIK = 10   # (C) bu sayinin altinda YUZDE verilmez
    print(f"\n{'site':21} {'claims':>6} {'linked':>7} {'named':>6} {'reachable':>10}  note")
    for r in sorted(rows, key=lambda x: -(x["blocks_sourced"]/x["blocks_with_numeric_claim"] if x["blocks_with_numeric_claim"] else 0)):
        p = pct(r["blocks_sourced"], r["blocks_with_numeric_claim"])
        az = r["blocks_with_numeric_claim"] < ESIK
        gost = "small sample" if az else (f"{p:.0f}%" if p is not None else "-")
        mark = "  <<<" if r["page_id"].startswith("BIZ") else ""
        print(f"  {r['page_id']:19} {r['blocks_with_numeric_claim']:6} {r['blocks_sourced']:7} {r['blocks_source_named_not_linked']:6} "
              f"{gost:>9}{mark}")

    ge = [r for r in rows if r["blocks_with_numeric_claim"] >= ESIK]                 # yuzde verilebilir
    rak = [pct(r["blocks_sourced"], r["blocks_with_numeric_claim"]) for r in ge if not r["page_id"].startswith("BIZ")]
    biz = [pct(r["blocks_sourced"], r["blocks_with_numeric_claim"]) for r in ge if r["page_id"].startswith("BIZ")]
    az  = [r["page_id"] for r in rows if r["blocks_with_numeric_claim"] < ESIK]
    print(f"\n  (a percentage is given only for pages with {ESIK}+ claims)")
    print(f"  COMPETITORS {len(rak)} pages · median {st.median(rak):.0f}% · "
          f"zeros {sum(1 for v in rak if v == 0)} · under 10% {sum(1 for v in rak if v < 10)}")
    print(f"  OURS  {len(biz)} pages" + (f" · median {st.median(biz):.0f}%" if biz else " (not in this frame)"))
    print(f"  small-sample (under {ESIK}): {', '.join(az) if az else 'none'}")
    adt = sum(r["blocks_source_named_not_linked"] for r in rows if not r["page_id"].startswith("BIZ"))
    print(f"\n  linksiz ama KAYNAK ADI verilen iddia (rakiplerde): {adt}")
    CIKTI = os.path.join(KOK, "data/measurement-by-block.json")
    json.dump({"_about": ("Block-unit measurement (the primary unit). One row per page: "
                          "how many blocks carry a numeric claim, and how many of those "
                          "carry a link to the source. The instrument judges each link "
                          "from its address and anchor text; it never opens it."),
               "retrieval_window": pencere, "rows": rows},
              io.open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n-> data/measurement-by-block.json")
