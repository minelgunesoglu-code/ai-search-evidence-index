#!/usr/bin/env python3
"""Dumps every tier-A claim on one page in a form a person can read by hand."""
import re, io, os, sys, html

# --- path layout (identical in every script in this package) --------------
_D   = os.path.dirname(os.path.abspath(__file__))     # code/
ROOT = os.path.dirname(_D)                            # the package root
# Snapshots are not published in the package; derived working files are
# written there as well, so they cannot be mistaken for published data.
SNAPS = os.environ.get("SNAPSHOTS", os.path.join(ROOT, "snapshots"))

NUMBER = re.compile(r'(?<![\w.])(?:\$\s?\d[\d,]*(?:\.\d+)?(?:\s?[kKmMbB]\b)?|\d+(?:\.\d+)?\s?%|\d+(?:\.\d+)?\s?x\b|\b\d{2,}(?:,\d{3})*\b|\b\d+\s+(?:engines?|sources?|prompts?|questions?|tools?|models?|domains?|platforms?|queries|sites?|brands?|weeks?|months?|days?|runs?|citations?)\b)', re.I)
MONTH = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*'
DATE_LINE = re.compile(r'(last (updated|reviewed)|published|posted|updated on)\b', re.I)
TEMPLATE = re.compile(r'^\s*[✔✓•\-]?\s*["“]|based on our \d{4} survey|\[(category|your brand|competitor|use case|task|job-to-be-done|the problem)', re.I)
BIO = re.compile(r"\b\d+\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|expertise|in\b)|\bbrings\s+\d+\+?\s*years?|\bI(?:'|’)ve\s+spent\s+the\s+last\s+\d+|\bis\s+the\s+(?:Founder|Co-Founder|CEO|CTO|Head)\s+of\b|\bFortune\s+\d00\b", re.I)
N_OUT_OF_N = re.compile(r"\b\d+\s+out\s+of\s+\d+\b", re.I)
TRAILING_DATE = re.compile(r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(?:19|20)\d\d\s*$", re.I)
BARE_HOST = re.compile(r'https?://[^/]+/?$')
PRICING_PATH = re.compile(r'/(pricing|plans)(?:/|$|\?)', re.I)
PRICE_CLAIM = re.compile(r'[\$€£]\s?\d|\btrial\b|/mo\b|per month', re.I)
CTA = re.compile(r'/(signup|sign-up|register|demo|book|booking|contact|start|trial|get-started|checkout|cart|app)(?:/|$|\?)|calendly\.com|savvycal\.com|cal\.com', re.I)
OWN_PRODUCT = re.compile(r'/(products?|product-tour|features?|solutions?|glossary|integrations?|platform|use-cases?)(?:/|$|\?)', re.I)
CARD_ANCHOR = re.compile(r'^\s*(read (post|more|article)|learn more|view (post|all))\s*$', re.I)
def words(s): return set(re.findall(r'[a-z0-9]{4,}', s.lower()))
def sourced(raw, sentence, domain):
    sent_words = words(sentence)
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S | re.I):
        u = m.group(1)
        if not (u.startswith("http") or (u.startswith("/") and len(u) > 3)): continue
        anchor = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
        if CTA.search(u) or CARD_ANCHOR.match(anchor): continue
        if OWN_PRODUCT.search(u) and (u.startswith('/') or domain in u): continue
        if PRICING_PATH.search(u) and PRICE_CLAIM.search(sentence): return u, anchor, "F-price"
        if BARE_HOST.match(u): continue
        numbers = re.findall(r'\d[\d,.]*', sentence)
        if any(s and s in anchor for s in numbers): return u, anchor, "D-number"
        if len(words(anchor) & sent_words) >= 2: return u, anchor, "D-words"
    return None, None, None
if len(sys.argv) < 2:
    raise SystemExit("usage  : python3 code/dump-blocks.py <page_id>\n"
                     "  example: python3 code/dump-blocks.py ahrefs.com\n"
                     "  page_id values: data/results.csv")
name = sys.argv[1]; domain = name.split('-')[0]
h = io.open(os.path.join(SNAPS, f'v2-{name}.html'), encoding='utf-8', errors='ignore').read()
h = re.sub(r'(?is)<(script|style|nav|header|footer|form|noscript)\b.*?</\1>', ' ', h)
n = 0
print(f"=== {name} ===")
for m in re.finditer(r'(?is)<(p|li|tr|blockquote)\b[^>]*>(.*?)</\1>', h):
    raw = m.group(2)
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw))).strip()
    if len(t) < 60 or DATE_LINE.search(t) or TEMPLATE.search(t): continue
    if BIO.search(t) or N_OUT_OF_N.search(t) or TRAILING_DATE.search(t.strip()): continue
    t2 = re.sub(MONTH + r'\.?\s+\d{1,2},?\s+(?:19|20)\d\d', ' ', t, flags=re.I)
    t2 = re.sub(r'\b(?:19|20)\d\d\b', ' ', t2)
    v = sorted(set(NUMBER.findall(t2)))
    if not v: continue
    u, anchor, rule = sourced(raw, t, domain)
    if not u: continue
    n += 1
    print(f"{n:3}. [{rule}] {v[0]}")
    print(f"     '{(anchor or '')[:46]}' -> {u[:78]}")
    print(f"     {t[:126]}")
print(f"total A: {n}")
