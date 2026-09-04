#!/usr/bin/env python3
"""INDEPENDENT VERIFICATION — written again from scratch, sharing NO code with the
instrument.

The question: does a second implementation reach the same result? If it does not,
one of the two has a defect. It was written differently on purpose: different HTML
splitting, a different number pattern, the link rules applied in a different order.
Landing on the same figure by accident is not plausible.
"""
import re, io, glob, os, json, html as H
# --- path layout (identical in every script in this package) --------------
_D   = os.path.dirname(os.path.abspath(__file__))     # code/
ROOT = os.path.dirname(_D)                            # the package root
# Snapshots are not published in the package; derived working files are
# written there as well, so they cannot be mistaken for published data.
SNAPS = os.environ.get("SNAPSHOTS", os.path.join(ROOT, "snapshots"))


def extract_blocks(raw):
    """Strip the tags and produce text — a different order from the instrument's."""
    x = re.sub(r'(?is)<(script|style|noscript|nav|header|footer|form)[^>]*>.*?</\1>', ' ', raw)
    out = []
    for m in re.finditer(r'(?is)<(p|li|tr|blockquote)(\s[^>]*)?>(.*?)</\1>', x):
        inner = m.group(3)
        text = H.unescape(re.sub(r'<[^>]+>', ' ', inner))
        text = ' '.join(text.split())
        out.append((text, inner))
    return out

# a number pattern written differently — it has to catch the same thing
NUMBER = re.compile(r'(?:[$€£]\s?\d[\d.,]*[kKmMbB]?)|(?:\d[\d.,]*\s?%)|(?:\d+(?:\.\d+)?\s?[xX]\b)|(?:\b\d{2,}(?:[.,]\d{3})*\b)')
MONTHS = 'january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec'
def strip_dates(t):
    t = re.sub(r'\b(?:' + MONTHS + r')\.?\s+\d{1,2},?\s+\d{4}\b', ' ', t, flags=re.I)
    t = re.sub(r'\b\d{1,2}\s+(?:' + MONTHS + r')\.?,?\s+\d{4}\b', ' ', t, flags=re.I)
    return re.sub(r'\b(?:19|20)\d{2}\b', ' ', t)

SKIP_TEXT = [
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
REJECT_PATH = re.compile(r'/(?:signup|sign-up|register|demo|book|booking|contact|start|trial|get-started|checkout|cart|app)(?:/|$|\?)', re.I)
REJECT_HOST = re.compile(r'(?:calendly|savvycal|cal)\.com', re.I)
BARE_HOST = re.compile(r'^https?://[^/]+/?$')
PRICING_PATH = re.compile(r'/(?:pricing|plans)(?:/|$|\?)', re.I)
PRICING_TEXT = re.compile(r'[$€£]\s?\d|trial|/mo\b|per month', re.I)
OWN_PRODUCT = re.compile(r'/(?:products?|product-tour|features?|solutions?|glossary|integrations?|platform|use-cases?)(?:/|$|\?)', re.I)
CARD_ANCHOR = re.compile(r'^(?:read (?:post|more|article)|learn more|view (?:post|all))$', re.I)

def words(s): return {w for w in re.findall(r'[a-z0-9]{4,}', s.lower())}

def is_sourced(inner, text, domain):
    for m in re.finditer(r'(?is)<a\b[^>]*?href\s*=\s*"([^"]*)"[^>]*>(.*?)</a>', inner):
        href, anchor_raw = m.group(1), m.group(2)
        anchor = ' '.join(H.unescape(re.sub(r'<[^>]+>', '', anchor_raw)).split())
        if not (href.startswith('http') or (href.startswith('/') and len(href) > 3)):
            continue
        if REJECT_PATH.search(href) or REJECT_HOST.search(href):  continue
        if CARD_ANCHOR.match(anchor.strip()):                     continue
        if OWN_PRODUCT.search(href) and (href.startswith('/') or domain in href): continue
        if PRICING_PATH.search(href) and PRICING_TEXT.search(text): return True
        if BARE_HOST.match(href):                                 continue
        numbers = re.findall(r'\d[\d.,]*', text)
        if any(s and s in anchor for s in numbers):               return True
        if len(words(anchor) & words(text)) >= 2:                 return True
    return False

result = {}
for path in sorted(glob.glob(os.path.join(SNAPS, 'v2-*.html'))):
    name = os.path.basename(path)[3:-5]
    domain = name.split('-')[0]
    raw = io.open(path, encoding='utf-8', errors='ignore').read()
    total = sourced = 0
    for text, inner in extract_blocks(raw):
        if len(text) < 60:                                   continue
        if any(p.search(text) for p in SKIP_TEXT):           continue
        if not NUMBER.search(strip_dates(text)):             continue
        total += 1
        if is_sourced(inner, text, domain):                  sourced += 1
    if total: result[name] = (total, sourced)
json.dump(result, io.open(os.path.join(SNAPS, 'independent-result.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"independent counter: {len(result)} pages processed -> independent-result.json")
