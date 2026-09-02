# Extended design (v2) — 30 August 2026

Round 5 stands, but it is **narrow**: 19 pages, 19 domains, one page per site. All
we could speak about was "this page". v2 widens that.

**Rule: this document was written before measurement began. It is not changed
during measurement.** If it changes, the change is dated and everything affected
is re-measured.

## 1. Sampling frame

The candidate pool is the first ten organic results for **six seed queries**. Two
queries carry over from round 5; four were added from our own pages' target
queries:

1. `generative engine optimization guide 2026` *(carried over)*
2. `best AI search visibility tools comparison 2026` *(carried over)*
3. `how to get cited by ChatGPT`
4. `how to track brand mentions in ChatGPT`
5. `what is answer engine optimization`
6. `how to rank in AI Overviews`

The queries are our own pages' targets, which keeps the condition "competing in
the same query as us" intact.

## 2. Inclusion (carried over from round 5 unchanged)

1. An independent site — not a publishing platform (Medium, LinkedIn, Substack excluded)
2. The page must carry a numeric claim
3. It must be competing in the same query as one of our pages

**Excluded:** ismybrandinai.com. The reason: while the instrument was in our hands
we corrected our own pages, and the measured pages could not do that — a figure
for us would not be comparable with theirs. Our own numbers are not hidden: the
measurement of our four pages (52%, 42%, 52%, 17%) is published in the article's
"Why our own pages are not in the table" section.

## 3. Depth: THREE pages per site

From each qualifying domain, three pages of the same kind (a guide or comparison
carrying numbers). They are not averaged — **all three are reported separately.**
Within-site variation is a finding in its own right: if a site sources one page and
not another, we want to see it.

Sites where three pages cannot be found enter with what is found, and the number of
pages they entered with is recorded.

## 4. Splitting by type (ADDED in v2)

Round 5 mixed two different kinds of page into one metric:

| Kind | Nature of the claims | What reachability means |
|---|---|---|
| **Tool comparison** | price / feature ("$99/month, 10 engines") | is the vendor's pricing page linked |
| **Guide / research** | statistics ("68% of searches end without a click") | is the study linked |

The two are **reported separately.** The instrument already counts price claims
apart (`fiyat` / `fiyat_ulasilir` columns); v2 carries that split through to the
report.

## 5. Measurement

- Instrument **v1.5**, frozen. Not changed during measurement.
- One timestamp, everything fetched back to back; whatever cannot be fetched drops out and is reported.
- **Tier A (linked) is published as a percentage** — hand-measured at 82% validity.
- **Tier B is NOT published as a percentage** — signal plus a verified example.
- **Bibliography column**: how many entries the end-of-page list holds, and how many are linked.
- A page with fewer than 10 claims gets no percentage.

## 6. Verification

- **Every** published tier-A link is read by hand. Without exception.
- One tier-B example per page is verified by hand.
- 20 claims drawn at random from the newly added pages are coded blind; agreement with the instrument is reported (in round 5 it was 83% across 30 items).

## 7. Limits accepted in advance

1. One day, one retrieval. Pages change — `data-mania.com` lost 181 footnote links in round 3, and the evidence is kept.
2. Whether three pages represent a site — they may not. We say "these three pages".
3. Six queries are not a field. We say "the pages these queries returned".
4. Frame flaws are symmetrical, but symmetry breaks when page structures differ: table-heavy pages inflate the denominator. Block counts are reported separately as well.
5. The instrument stalled at 83% on tier B; that is why the tier carries no percentage.

## 8. Where round 5 stands

Round 5 is **not cancelled**. When v2 is complete the two are compared: does the
narrow sample's result hold in the wide one? If it does not, that is a finding too.

---

## CHANGE 1 — 30.08.2026, after the SERPs were collected, before measurement began

**The §3 rule of "three pages per site" is removed.** In its place: **the frame is
the SERP itself.** A domain enters with as many pages as Google ranks it for.

**Reason:** "three pages per site" required *me* to choose the second and third page
— which three? That is a judgement step, and it breaks reproducibility. The SERP
frame is mechanical: anyone running the same queries reaches the same list.

It also weights naturally: `tryprofound.com` appears in four queries and enters with
four pages. That is not a flaw; it is a measure of that site's visibility in this
field. Sites appearing with one page enter with one.

**Result:** 38 URLs across 30 unique domains. Entering with more than one page:
tryprofound.com (4), semrush.com (4), developers.google.com (2),
searchengineland.com (2).

**Where round 5 sits:** not cancelled. Round 5 is reported as a two-query **pilot**,
and whether the six-query frame confirms it is written up separately. Six of round
5's 19 pages appear in the new frame as well (digitalapplied, evertune, frase,
industry-lens, llmrefs, semrush) — for those six, the two rounds can be compared.
