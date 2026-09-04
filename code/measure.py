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
ROOT = os.path.dirname(D)                                # the package root
# Snapshots (v2-*.html) are NOT published in the package, for copyright reasons.
# Take your own with code/fetch.py, or point at a folder with SNAPSHOTS.
SNAPS = os.environ.get("SNAPSHOTS", os.path.join(ROOT, "snapshots"))

NUMBER = re.compile(
    r'(?<![\w.])(?:'
    r'\$\s?\d[\d,]*(?:\.\d+)?(?:\s?[kKmMbB]\b)?'
    r'|\d+(?:\.\d+)?\s?%'
    r'|\d+(?:\.\d+)?\s?x\b'
    r'|\b\d{2,}(?:,\d{3})*\b'
    r'|\b\d+\s+(?:engines?|sources?|prompts?|questions?|tools?|models?|domains?|'
    r'platforms?|queries|sites?|brands?|weeks?|months?|days?|runs?|citations?)\b'
    r')', re.I)
MONTH = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*'
DATE_LINE = re.compile(r'(last (updated|reviewed)|published|posted|updated on)\b', re.I)
# (B) template/example block: a pattern sentence handed to the reader.
# (J) v1.7 (31.08) — blocks that are NOT claims. In a 30-item hand coding, 7 were not
# real claims (23%), and 6 of those 7 carried NO LINK: the denominator swells while the
# numerator does not, so every percentage came out LOW (the pool moved from 37% to 46%
# once corrected). Only cases that are MECHANICALLY certain are dropped; ones needing
# judgement, such as an advice sentence, are KEPT, and the remaining error rate is
# stated in the report.
BIO = re.compile(
    r"\b\d+\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|expertise|in\b)"
    r"|\bbrings\s+\d+\+?\s*years?"
    r"|\bI(?:'|\u2019)ve\s+spent\s+the\s+last\s+\d+"
    r"|\bis\s+the\s+(?:Founder|Co-Founder|CEO|CTO|Head)\s+of\b"
    r"|\bFortune\s+\d00\b", re.I)
N_OUT_OF_N = re.compile(r"\b\d+\s+out\s+of\s+\d+\b", re.I)
TRAILING_DATE = re.compile(r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(?:19|20)\d\d\s*$", re.I)
TEMPLATE = re.compile(r'^\s*[✔✓•\-]?\s*["“]|based on our \d{4} survey|\[(category|your brand|competitor|'
                    r'use case|task|job-to-be-done|the problem)', re.I)
# (A) a source is NAMED but not linked.
# v1.4 (30.08) — against a 30-item hand coding, v1.3 scored 73%. Two PROVEN misses:
#   1) 'according to' was lower-case in the pattern, so 'According to BrightEdge' ESCAPED
#   2) the verbs 'predicts/forecasts' were absent, so 'Gartner predicts' ESCAPED
# TRIED AND REVERTED (they raised false alarms across the corpus, measured on 2,347 blocks):
#   - shows/notes/states/finds -> 'It shows the top 20 competitors', 'Page Analytics
#     shows', 'This shows Warby Parker' were all read as sources
#   - a capitalised domain name -> in tool-comparison articles it fired on every product name
#   - "X's own \w+"            -> it fired inside table cells
# Remaining agreement: 25/30 = 83%. Four of the ones left open are the same class: a
# price claim carrying the vendor's own name (Profound $399, Frase $39). That is why
# tier B IS NOT PUBLISHED AS A PERCENTAGE; it is given as a signal plus hand-verified
# examples only.
SOURCE_NAMED = re.compile(
    r'\b[a-z0-9][a-z0-9-]{2,}\.(?:com|ai|org|io|net|co|dev)\b'
    r'|[Aa]ccording to\b|\bper\s+[A-Z]|[Cc]ited by\b'
    r'|\b[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)?\s+(?:found|reports?|reported|says?|said|'
    r'suggests?|estimates?|puts?|measured|published|analy[sz]ed|predicts?|forecasts?)\b'
    r"|\([A-Z][A-Za-z&.\-/' ]{2,60}?,[^)]{0,60}?(?:19|20)\d\d\)"
    r"|\b[A-Z][A-Za-z]+(?:'s|\u2019s)\s+(?:data|study|research|analysis|survey|report|audit|benchmark|figures?|numbers?)\b"
    r"|(?<=[a-z,;:] )[A-Z][A-Za-z]+(?:-(?:led|backed|funded|run))?\s+(?:[A-Z][A-Za-z]*\s)?(?:study|survey|benchmark|dataset)\b"
    r'|\b(?:study|research|survey|analysis|report|data|edition)\s+(?:of|by|from)\s+[A-Z]')
PRICE = re.compile(r'\$\s?\d')

def blocks(h):
    h = re.sub(r'(?is)<(script|style|nav|header|footer|form|noscript)\b.*?</\1>', ' ', h)
    out = []
    for m in re.finditer(r'(?is)<(p|li|tr|h[1-6]|blockquote)\b[^>]*>(.*?)</\1>', h):
        kind, raw = m.group(1).lower(), m.group(2)
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw))).strip()
        if len(txt) >= 12:
            out.append((kind, txt, raw))
    return out

STOP = set("the a an of in on for to and or is are was were with by from that this it its as at".split())
BARE_HOST = re.compile(r'https?://[^/]+/?$')
PRICING_PATH = re.compile(r'/(pricing|plans)(?:/|$|\?)', re.I)
# v1.5 (30.08) — CTA and booking links ARE NOT SOURCES. In hand checking, all three
# of visiblie.com's 'linked claims' were the 'Start Free Trial' button (the '14-day
# trial' figure matched a /signup link); one of data-mania's was a savvycal booking link.
CTA = re.compile(r'/(signup|sign-up|register|demo|book|booking|contact|start|trial|get-started|checkout|cart|app)(?:/|$|\?)|calendly\.com|savvycal\.com|cal\.com', re.I)
# RELATED-POST CARD — blocks whose anchor reads 'Read Post' or 'Read more' are
# navigation, not claims. All three of nav43.com's 'sourced claims' were the
# related-post box under the article.
# (I) v1.6 (31.08) — a PRODUCT or GLOSSARY page IS NOT a source.
# In hand checking, all four of hubspot.com's "sourced" claims went to its own
# product page (hubspot.com/products/aeo), and digitalapplied's single claim to its
# own glossary. Linking to your own RESEARCH report (similarweb.com/corp/reports/...)
# or your own CASE study (tryprofound /customers/...) is legitimate by contrast: it
# leads to a published source.
OWN_PRODUCT = re.compile(r'/(products?|product-tour|features?|solutions?|glossary|integrations?|platform|use-cases?)(?:/|$|\?)', re.I)
CARD_ANCHOR = re.compile(r'^\s*(read (post|more|article)|learn more|view (post|all))\s*$', re.I)
PRICE_CLAIM = re.compile(r'[\$€£]\s?\d|\btrial\b|/mo\b|per month', re.I)

def words(s):
    return {w for w in re.findall(r"[a-z]{3,}", (s or "").lower()) if w not in STOP}

def sourced(raw, sentence="", domain=None):
    """(D)(E)(F) — does this link source THIS figure? See the v1.2 note."""
    sent_words = words(sentence)
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S | re.I):
        u = m.group(1)
        if not (u.startswith("http") or (u.startswith("/") and len(u) > 3)):
            continue
        anchor = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
        if CTA.search(u): continue                      # (G) v1.5 CTA/booking is not a source
        if OWN_PRODUCT.search(u) and (u.startswith('/') or (domain and domain in u)):
            continue                                    # (I) v1.6 the site's OWN product/glossary page
        if CARD_ANCHOR.match(anchor): continue                    # (H) v1.5 related-post card
        if PRICING_PATH.search(u) and PRICE_CLAIM.search(sentence):      # (F)
            return True
        if BARE_HOST.match(u):                                            # (E)
            continue
        numbers = re.findall(r'\d[\d,.]*', sentence)
        if any(s and s in anchor for s in numbers):                        # (D) anchor carries the figure
            return True
        if len(words(anchor) & sent_words) >= 2:                             # (D) anchor shares words with the sentence
            return True
    return False

def measure(h, domain=None):
    bls = blocks(h)
    # table rule: give credit if a short linked paragraph sits next to the tr block
    credit = [False] * len(bls)
    for i, (kind, txt, raw) in enumerate(bls):
        if kind != "tr":
            continue
        a = i
        while a > 0 and bls[a-1][0] == "tr": a -= 1
        b = i
        while b < len(bls)-1 and bls[b+1][0] == "tr": b += 1
        for j in (a-1, a-2, b+1, b+2):
            if 0 <= j < len(bls) and bls[j][0] in ("p", "li") and sourced(bls[j][2], bls[j][1]) and len(bls[j][1]) < 400:
                credit[i] = True
                break
    n = sourced_n = 0
    fn = fa = 0
    named = 0                                   # (A) a source is named, with no link
    for i, (kind, txt, raw) in enumerate(bls):
        if kind.startswith("h") or DATE_LINE.search(txt) or len(txt) < 60:
            continue                                   # not a claim
        if TEMPLATE.search(txt):
            continue                                   # (B) a pattern handed to the reader
        if BIO.search(txt) or N_OUT_OF_N.search(txt) or TRAILING_DATE.search(txt.strip()):
            continue                                   # (J) v1.7 not a claim
        t2 = re.sub(MONTH + r'\.?\s+\d{1,2},?\s+(?:19|20)\d\d', ' ', txt, flags=re.I)
        t2 = re.sub(r'\d{1,2}\s+' + MONTH + r'\.?\s+(?:19|20)\d\d', ' ', t2, flags=re.I)
        t2 = re.sub(r'\b(?:19|20)\d\d\b', ' ', t2)
        ok = sourced(raw, txt, domain=domain) or credit[i]
        has_name = bool(SOURCE_NAMED.search(txt))
        found = set(NUMBER.findall(t2))
        if not found: continue
        if all(PRICE.search(v) for v in found):
            fn += 1; fa += ok
        else:
            n += 1; sourced_n += ok
            if not ok and has_name: named += 1          # (A)
    return n, sourced_n, fn, fa, named

# The measurement runs only when this file is executed DIRECTLY. blind-sample.py
# imports this module for the rule definitions; importing it must NOT overwrite
# the published data/measurement-by-block.json.
if __name__ == "__main__":
    with io.open(os.path.join(ROOT, "data/retrieval-log.csv"), encoding="utf-8") as fh:
        log = [r for r in csv.DictReader(fh)]
    retrieved = [r for r in log if r["status"] == "retrieved"]
    queries = {r["page_id"]: r["seed_query"] for r in retrieved}
    # Retrieval window = from the FIRST fetch's timestamp to the LAST one's. This is
    # reproducible because its only source is the published retrieval-log.csv.
    # NOTE: the window in the first published file came from fetch.py's own start and
    # end times and included the download time of the last page (85.4 s); the one
    # derived here is 83.6 s. The article's "inside 86 seconds" holds for both.
    # Detail: notes/instrument-revisions.md v1.8.
    stamps = sorted(r["retrieved_utc"] for r in retrieved)
    window = [stamps[0], stamps[-1]]

    rows = []
    snaps = sorted(glob.glob(os.path.join(SNAPS, "v2-*.html")))
    if not snaps:
        raise SystemExit(f"No snapshots found: {SNAPS}\n"
                         f"Fetch your own with code/fetch.py, or pass SNAPSHOTS=<folder>.")
    for f in snaps:
        name = os.path.basename(f)[3:-5]
        n, a, fn, fa, named = measure(io.open(f, encoding="utf-8", errors="ignore").read(), domain=name.split("-")[0])
        if n + fn < 3:
            print(f"  SKIPPED (fewer than 3 claims): {name}")
            continue
        rows.append({"page_id": name, "seed_query": queries.get(name, "?"),
                     "blocks_with_numeric_claim": n, "blocks_sourced": a,
                     "blocks_source_named_not_linked": named,
                     "price_claims": fn, "price_claims_sourced": fa})

    def pct(a, b): return 100*a/b if b else None

    MIN_CLAIMS = 10   # (C) below this count NO PERCENTAGE is given
    print(f"\n{'site':21} {'claims':>6} {'linked':>7} {'named':>6} {'reachable':>10}  note")
    for r in sorted(rows, key=lambda x: -(x["blocks_sourced"]/x["blocks_with_numeric_claim"] if x["blocks_with_numeric_claim"] else 0)):
        p = pct(r["blocks_sourced"], r["blocks_with_numeric_claim"])
        small = r["blocks_with_numeric_claim"] < MIN_CLAIMS
        shown = "small sample" if small else (f"{p:.0f}%" if p is not None else "-")
        mark = "  <<<" if r["page_id"].startswith("BIZ") else ""
        print(f"  {r['page_id']:19} {r['blocks_with_numeric_claim']:6} {r['blocks_sourced']:7} {r['blocks_source_named_not_linked']:6} "
              f"{shown:>9}{mark}")

    rated = [r for r in rows if r["blocks_with_numeric_claim"] >= MIN_CLAIMS]                 # eligible for a percentage
    rivals = [pct(r["blocks_sourced"], r["blocks_with_numeric_claim"]) for r in rated if not r["page_id"].startswith("BIZ")]
    ours = [pct(r["blocks_sourced"], r["blocks_with_numeric_claim"]) for r in rated if r["page_id"].startswith("BIZ")]
    small  = [r["page_id"] for r in rows if r["blocks_with_numeric_claim"] < MIN_CLAIMS]
    print(f"\n  (a percentage is given only for pages with {MIN_CLAIMS}+ claims)")
    print(f"  COMPETITORS {len(rivals)} pages · median {st.median(rivals):.0f}% · "
          f"zeros {sum(1 for v in rivals if v == 0)} · under 10% {sum(1 for v in rivals if v < 10)}")
    print(f"  OURS  {len(ours)} pages" + (f" · median {st.median(ours):.0f}%" if ours else " (not in this frame)"))
    print(f"  small-sample (under {MIN_CLAIMS}): {', '.join(small) if small else 'none'}")
    named_total = sum(r["blocks_source_named_not_linked"] for r in rows if not r["page_id"].startswith("BIZ"))
    print(f"\n  claims with a source NAMED but not linked (competitors): {named_total}")
    OUT = os.path.join(ROOT, "data/measurement-by-block.json")
    json.dump({"_about": ("Block-unit measurement (the primary unit). One row per page: "
                          "how many blocks carry a numeric claim, and how many of those "
                          "carry a link to the source. The instrument judges each link "
                          "from its address and anchor text; it never opens it."),
               "retrieval_window": window, "rows": rows},
              io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n-> data/measurement-by-block.json")
