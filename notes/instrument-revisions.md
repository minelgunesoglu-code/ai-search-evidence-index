# Revision history of the instrument — Evidence Index coder

The instrument was **revised five times in a single day, 30 August 2026.** Every
revision came out of reading by hand a number the machine had produced. None of
them could have been found by the machine.

This history is published: showing how many times a measuring instrument was wrong,
and why, matters as much as the result.

---

## v0 → v1.0

| # | Defect found | How it was found | Effect |
|---|---|---|---|
| 1 | **Dates were counted as claims** — `28` and `2026` were being extracted from `Updated On: July 28, 2026` | data-mania's 79% looked suspicious, so the examples were read | 275 → 261 claims |
| 2 | **Several numbers in one block** made the same code count repeatedly | Repeated texts were noticed | Block-level reporting added |
| 3 | **Page titles** were counted as claims (`19 Best AI Tools`) | A hand check of 40 claims | 15% frame defect |
| 4 | **Table source notes** did not cover their rows | Our own GEO page came out at 5%; the reason was looked for | Table rule added |

## v1.0 → v1.1

| # | Defect found | How it was found | Effect |
|---|---|---|---|
| 5 | **"Source named, no link" was counted as zero** — llmrefs.com named its sources (Vercel, Brandlight) but showed as 0% | The 5 zero-scoring pages were read by hand | A third tier added |
| 6 | **Template and example sentences** were counted as claims — obapr's *"✔ PR agencies charge $5,000-$50,000"* is a TEMPLATE offered to the reader | The same reading | Template filter |
| 7 | **A percentage on a small sample** was meaningless — thehoth showed "33%" on 3 claims | The same reading | A 10-claim threshold |
| 8 | **Parenthetical academic citations were invisible** — `(Ahrefs, 2025)`, `(Gartner, 2024)`. nav43 showed 8%; in reality the source is identified for 44% of its claims | nav43 read by hand | Named tier 30 → 64 |

## v1.1 → v1.2 — THE VALIDATION SET

Here the method changed: **measured validity** instead of guesswork.

A stratified sample of 92 claims was drawn and **46 linked claims were coded by
hand** (the human judgement being: *"does the link in this block ACTUALLY source
this number"*).

**v1.1's measured error: 38%** (15 wrong out of 39 codable claims). On top of that,
7 of the 46 (15%) were not claims at all — dates in card lists, document
identifiers such as `arXiv:2311.09735`.

The rules tried, and how each agreed with the validation set:

| Rule | Agreement | False positives |
|---|---|---|
| v1.1 — "a link in the block is enough" | 62% | 15 |
| + do not count a link to the site's own pages | **54%** ↓ | — |
| + do not count a bare home page | 67% | — |
| + anchor-text rule | 77% | 1 |
| **+ pricing-page exception** | **82%** | **2** |
| + a loosened threshold | 82% | 6 ❌ rejected |

**Chosen: 82% agreement, 2 false positives.** A looser setting giving the same
agreement was rejected — in a study that publishes scores under company names,
saying *"it has a source"* and being wrong is far more damaging than missing one.

### Where my intuition was wrong

I added a rule saying *"a link to the site's own pages does not count as a
source"*; it looked sensible. The validation set dropped agreement **from 77% to
54%** and the rule was thrown out. Linking to your own study or your own pricing
page is a legitimate source.

---

## Remaining limits (NOT closed in v1.2)

1. **18% disagreement persists** — 2 false positives, 5 missed. These require human judgement.
2. **The rule rewards one writing style.** Putting the claim in the anchor text is good practice, but our own links were written in exactly that style on 30 August; competitors anchor on brand names. **This asymmetry will be stated in the report.**
3. The validation set was coded by a **single coder** (no blind double coding).
4. The sample is 46 linked claims — more coding would narrow the agreement estimate.

---

## v1.3 — 30 August, the named-tier correction

### How it was found

A subset of 10 items was coded by hand without seeing the instrument's output (the
codes were sealed first into `kor-kod-CLAUDE-1-10.json`, with a sha256). Agreement
with the instrument: **7/10**.

All three misses ran **in the same direction**: blocks that named their source were
being counted as unsourced.

| # | Page | Phrase missed | Why |
|---|---|---|---|
| 1 | nav43.com | `(Joshua Blyskal/Profound, 100,000 prompts analyzed, 2025)` | the parenthetical pattern expected `(Name, YYYY)` and broke when text appeared between the name and the year |
| 3 | llmpulse.ai | `Indig's data showed` | there was no possessive-plus-reporting-verb pattern |
| 9 | ayzeo.com | `Princeton-led GEO study` | only `study by X` existed, not `X-led study` |

### Why this is serious

The error was one-way: **it made competitors look less sourced than they are.** In a
study that publishes pages under their names, that is a misrepresentation that
cannot be undone.

### Overfitting check

Because the patterns were written by looking at those 10 items, testing on them
would be marking my own exam. So the new patterns were applied to **the whole
corpus** (2,258 unlinked blocks) and every new catch was read by hand.

- First attempt: 20 new catches → **8 were false alarms**
  (`One study analyzed…` = unnamed; `AI audit` / `site audit` = a product feature name;
  `Once the report loads` = sentence-start noise)
- The pattern was tightened: a capital letter at the start of a sentence does not count; `audit` and `report` were removed as head nouns (in this niche they are product names)
- Second attempt: **11 new catches, all 11 genuine** (read by hand, 0 false alarms)

### Effect

- Competitor claims where a source is "named but not linked": **69 → 85** (+23%)
- `nav43.com` 8% → **A 8% / A+B 48%** · `llmpulse.ai` 15% → **46%** · `xseek.io` 4% → **42%**
- **The link tier (A) did not change at all.** This correction touches only the named tier; v1.2's hand-measured **82%** link-tier validity stands unchanged.

### The consequence the report must carry

No single number will be published. Every page is given in **two tiers**:
**A (a link exists)** and **A+B (the source is at least named)**. Publishing A alone
would show pages that name their sources as sourcing nothing.

### A limit v1.3 did not close either

One label is given per block. In `ayzeo.com`'s 935-character block, the 40% figure
belongs to the Princeton study and the byline quote to a Google document — two
different sources, one label. Multiple citations within a block are not separated.

---

## v1.4 — 30 August, validation raised to 30 items

The sample went from 10 to 30 (codes sealed in `kor-kod-CLAUDE-1-30.json`). v1.3
scored **73%** on this set. Two demonstrable errors were found:

1. The `according to` pattern was **lower-case only** — `According to BrightEdge` was slipping through. This error had been present since v1.2.
2. The verbs `predicts` and `forecasts` were absent — `Gartner predicts`, `Gartner forecasts` were slipping through.

**Agreement 73% → 83%.**

### Tried and rolled back

Patterns added purely to raise the number, seen to produce false alarms across the
corpus, and **withdrawn**:

| Tried | Why it was rolled back |
|---|---|
| `shows / notes / states / finds` | `It shows the top 20 competitors`, `Page Analytics shows`, `This shows Warby Parker` — all read as sources |
| A capitalised domain name | In tool-comparison articles it fired on every product name (`Frase, Profound, Otterly.ai…` lists) |
| `X's own \w+` | It fired inside table cells (`Tied to Google's own retrieval`) |

Each attempt was applied to 2,347 unlinked blocks and the new catches read by hand.

### The limit that could not be closed → the publication decision

4 of the 5 remaining disagreements belong to **a single class**: a vendor's own
name inside a price claim (`Profound covers one engine at $99 and three at $399`,
`Frase plans start at $39/month`). The fifth is a character inside an article
(`James's fastest method`) — a name the reader could not look up.

For that reason **tier B will NOT enter the report as a percentage.** For each page,
only:

- **A (a link exists)** → published as a percentage, with hand-measured **82%** validity
- **B (named, not linked)** → a present/absent marker plus **1-2 hand-verified examples** (for nav43, `(Ahrefs, December 2025)`)

The reason: publishing a number we cannot measure risks doing an injustice to a site
we have named. `nav43.com` shows as 8% on a single figure; in fact it names its
source for a substantial share of its claims, it simply does not link them.

---

## v1.5 — 30 August, an error found in the MAIN measurement (the most serious)

This revision corrects an error not in the named tier but in **the headline number
that would be published**.

### How it was found

Every claim counted as "linked" on the 8 pages that would be named was read one
at a time. Some of what the instrument counted as sources were not sources:

| Page | Instrument | Reality |
|---|---|---|
| `visiblie.com` | 3 linked claims | **all three were "Start Free Trial" buttons** — the `14-day trial` and `500+ companies` figures had been mapped to the `app.visiblie.com/signup` link |
| `nav43.com` | 5 | **two were "Read Post" cards** — the related-article boxes beneath the article |
| `data-mania.com` | 9 | one was a **savvycal booking link** |
| `useomnia.com` | 7 | one was a `/demo` button |

Root cause: v1.2's **(F) pricing rule** treated the `/signup` path as a pricing page
too, so a trial-period figure matched a sign-up button.

### Two rules added

- **(G)** Call-to-action and booking links such as `/signup`, `/demo`, `/trial`, `/book`, `/contact`, `calendly`, `savvycal` **do not count as sources.** Rule (F) was narrowed to `/pricing` and `/plans` only.
- **(H)** Blocks anchored on `Read Post` / `Read more` / `Learn more` are **navigation**, not claims.

### Effect

| Page | v1.4 | v1.5 |
|---|---|---|
| `visiblie.com` | 1% | **0%** |
| `nav43.com` | 8% | **5%** |
| `useomnia.com` | 41% | **35%** |
| `data-mania.com` | 5% | 5% |
| **our own 4 pages** | — | **unchanged (0 links removed)** |

### This asymmetry will be written into the report

The rule is applied identically to everyone; not one link is removed from our pages,
because we do not use call-to-action buttons as sources. But the rule **was found
while reading competitors' pages**. The report will say so plainly, and will give
examples of the removed links (`app.visiblie.com/signup` → "Start Free Trial →") so
a reader can check for themselves.

### The lesson

The first four revisions chased the named tier; the real error was **in the headline
number**, and it only became visible when the pages were read one at a time.
Validating a regex with a regex does not find the error.

---

## v1.6 — 31 August, an error found in the wider frame

It came out while reading the v2 frame (38 pages) by hand.

### The finding

| Page | Instrument | On reading by hand |
|---|---|---|
| `hubspot.com` | 36% (4 linked claims) | **all four went to its own product page** (`hubspot.com/products/aeo`) |
| `digitalapplied.com` | 1 linked | to its own **glossary** page — a related-content link, not a source |

Against that, links counted as legitimate — to a publisher's **own published study**:
`aisearch.similarweb.com` → `similarweb.com/corp/reports/…` (its own research report),
`tryprofound.com` → `/customers/…` (its own case study). These take the reader to the
document the number came from; a product page does not.

### Rule (I)

A link to the publisher's **OWN** product, feature, solution, glossary or platform
page does not count as a source.

### The first attempt WAS WRONG — and was corrected

The rule was first applied to every link and removed `blog.google/products/search/…`
addresses. Those are Google's **blog posts**, not product pages — they were being
removed because `/products/` appeared in the path. The rule was narrowed to
**internal links only** (same domain or a relative path).

### Effect

| Page | v1.5 | v1.6 |
|---|---|---|
| `hubspot.com` | 36% | **0%** |
| `frase.io` | 42% | 41% |
| `purposelaunch.com` | 10% | 10% *(an outbound link, restored)* |
| **competitor median** | **36%** | **23%** |

## v1.8 — 1 September 2026, packaging repair (NO MEASUREMENT LOGIC CHANGED)

On 31 August the file and folder names were translated from Turkish to English, but
the code was not updated. The result: **the published code could not read the
published data.** In a study measuring whether sources can be reached, the study
itself could not be run.

**No measurement rule was touched in this revision.** The evidence: after the repair
`measure.py` was re-run and all 25 of the 25 rows of `data/measurement-by-block.json` came out
identical, field for field, across all five fields.

### What was repaired

1. **Paths.** Every script was relative to the `code/` folder; they now find the package root. Snapshots are pointed to with the `SNAPSHOTS` environment variable (default `snapshots/`), because copyright prevents publishing them.
2. **`retrieval-log.csv` is a real CSV.** `measure.py` was calling `json.load()` on it while `fetch.py` was writing JSON over it. Both were fixed; `fetch.py` now writes the same columns as the published file and leaves failed pages as rows (`status = failed_http_<code>`).
3. **The `sampling-frame.json` key.** `fetch.py` looked for `sorgular`; the file says `queries`.
4. **Output keys.** `measure.py` wrote Turkish keys; it now produces the English keys of the published file.
5. **The `seed_query` truncation.** The code carried a 28-character abbreviation. The published file holds the full queries, so the truncation never reached it — but it would have if the code had been run, because the version that produced the published file did not carry the abbreviation. It was removed entirely.
6. **An import side effect.** `measure.py` ran the measurement at module level and overwrote `data/measurement-by-block.json`; `blind-sample.py` imports it. BEFORE the repair this danger could not materialise, because the code was already crashing on the path error (item 1) — but it became live the moment the paths were fixed. The measurement is now behind an `if __name__ == "__main__"` guard.
7. **`blind-sample.py` was deleting data.** The published `blind-sample-120.json` is the COMPLETED sheet (120 human codes plus the instrument's verdict). The script produces an EMPTY sheet and was writing to the same path. This too could not happen before the repair because of the crash; during the repair it happened once and 120 human codes were deleted, then restored exactly from backup. The script now writes its output to the `SNAPSHOTS` folder.
8. **`blind-sample.py` filename derivation.** While the paths were being made absolute, the line `alan = f[3:-5]` was left without `os.path.basename`; block identifiers started to be produced as full file paths, and because `alan` was corrupted the own-domain rule ran incorrectly — on a single block (`hubspot.com#85`) the instrument's verdict changed, and kappa came out at 0.835 instead of 0.852. This error was PRODUCED during the repair, caught in the independent audit run the same day, and corrected. After the fix the script reproduces the published sample exactly: the same 120 identifiers, the same texts, the same verdicts, the matrix (37,1,7,75), kappa = 0.8522, 95% CI 0.753–0.951.
9. **`dump-blocks.py`** was not importing `os` and gave a traceback when called without arguments; it now prints a usage line.

### The retrieval window — a small difference that must be reported

The published `retrieval_window` value came from `fetch.py`'s own start and end
times and included the download time of the last page: 85.4 seconds. The window
derived from the row timestamps in `retrieval-log.csv` is 83.6 seconds. The CSV is
now the single source, because it is the only thing published. The whole package was
aligned to that value: the article, README, CITATION.cff, `notes/final-results.md`
and `data/measurement-per-number.json` now say 20:38:51–20:40:15 and "84 seconds".
`measurement-per-number.json` is the only hand-corrected data field in this package;
no script that produces it is published.

### What the repair made possible: the independent-counter claim verified for the first time

Once the code ran, `independent-counter.py` could be run against the v1.7 data for
the first time. The article's and README's claim that **"17 of 25 pages matched
exactly, 8 differ"** was **confirmed** — but only when compared on the right basis.

The independent counter draws no price distinction: it folds price blocks into the
total claim count. The comparison therefore has to be made against the instrument's
price-inclusive figures — and **both the total claims and the sourced count** have
to be compared together. Looking at totals alone gives 19/25; the published 17/25
and the eight pages named are produced only when the two numbers are compared
together:

| basis of comparison | matching exactly | differing |
|---|---|---|
| price included (as the counter counts) | **17 / 25** | **8** — the published claim |
| price separate (as the instrument counts) | 11 / 25 | 14 |

On the first attempt I computed the second row and concluded the claim could not be
reproduced; the error was mine, not the claim's. **The lesson:** the article says
"17 of 25" without saying which basis the comparison used. It should — otherwise a
reader trying to verify it picks the same wrong basis and believes the claim
refuted.

The 8 that differ on the price-inclusive basis: ahrefs.com,
aisearch.similarweb.com, digitalapplied.com, frase.io, llmrefs.com, orchly.ai,
seocrawl.ai, writer.com. The README attributes them to two causes (a table-credit
rule in one implementation and a gap in decimal capture); its numbers agree with the
table above.
