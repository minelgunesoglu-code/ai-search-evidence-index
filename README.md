# The AI Search Evidence Index

**Source determinability of numeric claims on AI-visibility web pages**

| | |
|---|---|
| **Article** | https://ismybrandinai.com/do-ai-visibility-guides-link-their-sources |
| **Repository** | https://github.com/minelgunesoglu-code/ai-search-evidence-index |
| **Retrieved** | 30 August 2026, 20:38:51–20:40:15 UTC, one 84-second window |
| **Pages** | 38 sampled · 32 retrieved · 13 in the published table |
| **Headline** | Across the 13 pages, a median of **33%** of blocks containing a numeric claim carry a link to the source. The spread runs from **0% to 62%**. |
| **Reliability** | Cohen's κ = 0.85, 95% CI [0.75–0.95], on 120 blocks coded blind against the instrument |
| **Licence** | CC BY 4.0 (`LICENSE`); see `LICENCE-NOTES.md` for what it does and does not cover |


Data, code and coding materials for a measurement of whether a reader can reach
the source of a numeric claim on pages that rank for AI-search-visibility queries.

**What is measured:** determinability: can a reader reach the source of a figure.
**What is NOT measured:** whether any figure is correct. No accuracy claim is made
about any page in this dataset.

---

## 1. Sampling frame

Six seed queries were run on google.com (`hl=en&gl=us`) on 30 August 2026. Every
organic result on the first page was taken. Publishing platforms (Reddit, Quora,
LinkedIn, YouTube, Medium, Substack, Facebook, Instagram, Stack Exchange) and
sponsored results were excluded.

| Seed query |
|---|
| generative engine optimization guide 2026 |
| best AI search visibility tools comparison 2026 |
| how to get cited by chatgpt |
| how to track brand mentions in chatgpt |
| what is answer engine optimization |
| how to rank in google ai overviews |

Result: **38 URLs, 30 distinct domains.** A domain enters as many times as Google
ranked it; no manual selection of additional pages was made.

The full frame with every URL is in `data/sampling-frame.json`.

**The authors' own site is excluded from the measured pages and from every published
percentage.** It is not excluded from the calibration material: four of the authors' own pages
appear in `coding/coded-items.json`, the thirty-block set used in an earlier round to test the
instrument against a coder. They are marked `BIZ-*` and are named here so nobody has to find them.
The
authors had the instrument in hand while writing their own pages; the measured
pages did not. Any figure for the authors' pages would not be comparable.

## 2. Retrieval

All 38 URLs were fetched inside a single window: **30 August 2026,
20:38:51 – 20:40:15 UTC**. 32 were retrieved; **6 failed** (HTTP 403 bot
protection or connection failure) and are listed with their status in
`data/retrieval-log.csv`. The failures are not random: they are larger,
established sites, and this is stated as a limitation.

Of the 32 retrieved pages, **25 carry a measurement row**. The instrument skips a page that
carries fewer than three claim blocks, on the grounds that a percentage over one or two blocks is
noise; seven pages fell there. Of the 25, **13 carry ten or more claim blocks** and are given a
percentage; the other twelve are counted in the totals but not rated.

**Raw HTML snapshots are not redistributed here**, to avoid republishing third-party content in
full. Instead the dataset carries, for every retrieved page, its **URL, retrieval timestamp, byte
size and the SHA-256 hash of the exact snapshot we measured**
(`data/snapshot-hashes.csv`).

That is enough to reproduce and to falsify. Re-fetch a URL, hash what you get, and compare: an
identical hash means you are looking at the document we measured; a different one means the page
has changed since 30 August 2026, which is itself worth knowing. In an earlier round one page
lost 181 footnote links between two retrievals a day apart.

Quoted excerpts appear only in the coding sheets, only where they are needed to show why a block
was coded as it was. They are capped at 200 characters in the three coding sheets and at 700 in the
reliability sample. Counting each published excerpt once, they total about 43,000 characters, which for
most pages is between 1% and 5% of the page. Snapshots are retained by the authors and can be made
available for verification on request.

## 3. Unit of analysis

The unit is a **block**: a `<p>`, `<li>`, `<tr>` or `<blockquote>` element of at
least 60 characters that contains at least one numeric claim. Headings and date
lines are excluded; counting headings was one of the errors the first revision
fixed. Blocks whose numbers are all prices are counted separately and are not in
the published percentages.

An earlier version of the instrument counted each distinct number as a separate
claim and applied the block's link verdict to all of them. That over-credited a
single link with sourcing several figures, and inflated pages that write
number-dense blocks. The block was adopted as the unit; the per-number figures
are retained in `data/measurement-per-number.json` as a robustness check.

## 4. Coding scheme

Each block receives one code:

| Code | Definition |
|---|---|
| **A** | A link inside the block points to the source of the figure. The instrument judges the link from its address and anchor text; it never opens it |
| **B** | A source is named in the block but not linked |
| **C** | Neither |

**Only A is reported as a percentage.** Agreement between the instrument and a
blind read on the B tier is weaker than on the first tier, below the level at
which a percentage should be published. B is reported as a flag with hand-verified
examples instead.

### Link rules (in order of application)

| Rule | Effect |
|---|---|
| **G** | Calls to action and booking links (`/signup`, `/demo`, `/trial`, `calendly`, `savvycal`) do not source a claim |
| **H** | Blocks whose anchor is `Read post` / `Read more` / `Learn more` are navigation, not claims |
| **I** | A link to the publisher's **own** product, feature, solutions, glossary or platform page does not source a claim. A link to the publisher's own **published study or dataset** does |
| **F** | For a price claim, a link to the vendor's `/pricing` or `/plans` page counts |
| **E** | A bare homepage link does not count |
| **D** | Otherwise the link counts if its anchor text contains the figure, or shares at least two content words with the claim sentence |
| **K** | A publisher naming **itself** is not naming a source, unless it points to a specific identified work (a named study, a dated dataset, a linked report) |

Rule K was added after coding, when a disagreement between the two coders showed
the codebook did not cover the case. This is disclosed rather than backdated.

## 5. Reliability

**Blind check against the instrument** (n = 120). Of the 470 claim-carrying
blocks across the 32 retrieved pages, 120 were drawn at random with a fixed seed
and coded without seeing the instrument's verdict. Agreement **112 of 120,
93.3%**; **Cohen's κ = 0.85, 95% CI [0.75–0.95]**. Every block is published with
its text, its links and the code it was given: `coding/blind-sample-120.json`.
The sample is reproducible from `code/blind-sample.py`.

**Which way the instrument errs.** In seven of the eight disagreements the
instrument credited a source the blind read did not; in one it missed a source
the read found. It errs towards making a page look **better** sourced than it
is. An earlier version of this README, written on a sample of thirty, reported
the opposite direction. That was wrong.

**Two known biases, pulling opposite ways.** This one moves the figure down:
across the 120 blind-coded blocks the instrument called 36.7% of them sourced
where the blind read called 31.7%, about five points it should not have
credited. The non-claim correction in limit 1 below moves it up by about four.
The two are measured on different populations and are not netted into a single
number, but they are close in size and opposite in sign — which is why the
figure reported is the one measured, and why neither adjustment is offered on
its own as a better estimate.

**A smaller human check** (n = 12), from an earlier round and not a subset of the
120 above. Twelve blocks, all of them link-free, were coded blind by a second
person on the named-source question only; eleven of twelve matched. Twelve items
is too small to publish as a rate. The single mismatch produced Rule K.

**Who coded.** Except where a second person is named above, the coder was the
language model that built the instrument. See section 11.

Materials: `coding/`.

## 6. Verification

- Every published figure was read. All 90 sourced blocks in the published table
  were inspected individually; 10 machine verdicts were rejected
  on inspection and the rejections are listed in `notes/final-results.md`.
- The counter was **re-implemented independently** (`code/independent-counter.py`)
  without reusing any of the original code. The re-implementation has no price
  rule, so the comparison is made on totals with price blocks left in: on that
  basis 17 of 25 pages matched exactly; all
  8 differences were traced to two causes (a table-credit rule present in one
  implementation, and a decimal-detection gap), neither of which changes the
  published table by more than one block on one page.

## 7. Known limitations

1. **Claim detection has a measured error rate.** In the 120-block reliability
   sample, **32 (27%, 95% CI 19–35%) carry no numeric claim at all**: advice,
   author biographies, plan names, scale definitions. That figure can be
   recomputed from `coding/blind-sample-120.json`, where every item carries an
   `is_a_numeric_claim` field. On the 85 of those 120 blocks the instrument
   would actually score, the rate is 22.4% (95% CI 13–31%), and only 3 of those
   19 non-claims were credited with a source — so they sit mostly on the
   unsourced side and **the reported percentages understate the true rate.**
   Applying that rate to the 252 blocks in the table gives a corrected pool
   estimate of **≈36%** against a raw 31.7%. An earlier 50-block pass gave a
   consistent 22%, but its per-item verdicts were not retained, so it cannot be
   recomputed from the published sheets and is reported only as corroboration.
2. **Six pages could not be retrieved** and are not random.
3. **One day, one snapshot.** Pages change; one page in an earlier round lost
   181 footnote links between two retrievals.
4. **Non-probability sample.** Six queries are not a field. Findings are stated
   as "these pages, on this date".
5. **Exclusion rules remove nothing from the authors' own pages**: the authors
   do not use calls to action or homepage links as sources. The rules were also
   discovered while reading measured pages, not the authors' own. The per-page
   count of what each rule removed is published in `notes/hand-verification.md`.
6. **One page is structurally advantaged.** `industry-lens.com` is a news
   aggregator whose format links a source by default.
7. **Single instrument, single language, one sector** (English-language B2B
   software / marketing).

## 8. Files

```
data/     results.csv                 final table, one row per published page
          snapshot-hashes.csv         SHA-256 of every snapshot, for document-identity checks
          retrieval-log.csv           all 38 URLs incl. the 6 failures, with timestamps
          compute-log.json            tokens and model calls, by day
          sampling-frame.json         the six queries and every organic result
          measurement-by-block.json   block-unit measurement (primary)
          measurement-per-number.json per-number measurement (robustness check)
code/     fetch.py                    single-window retrieval
          measure.py                  the instrument
          independent-counter.py      independent re-implementation
          blind-sample.py             draws the 120-block sample, fixed seed
          dump-blocks.py              dumps a page's sourced blocks for reading
          bibliography-scan.py        checks for end-of-page source lists
coding/   blind-sample-120.json       the 120-block blind sample, every code published
          coded-items.json            the thirty items from the earlier round
          coder1-sealed-codes.json    those thirty, sealed with SHA-256
          claim-validation-*.json     claim-detection validation samples
notes/    (in Turkish) design, revision history, decisions, hand-verification log
```

The documents in `notes/` are in Turkish; this README carries the method in
English. The revision history (`notes/instrument-revisions.md`) records seven
revisions of the instrument, each with the error found and how it was found.

## 9. Reuse

CC BY 4.0. Quoted excerpts from measured pages appear only where needed to show
a coding decision.

## 10. Corrections

If you find an error, tell us. We will correct it and record what changed.

- **An error in the measurement, the code or the coding**: open an issue on this
  repository, or write to minel@ismybrandinai.com.
- **You publish one of the measured pages and want an excerpt removed**: write to
  info@ismybrandinai.com and it will be removed.

## 11. Who did the work

This study was run by a person and a language model. Minel Gunesoglu set the
question, made every decision about scope and publication, and reviewed the
results. The model wrote the instrument, retrieved the pages, coded the blocks
and drafted the write-up. Where a figure depends on someone reading a page
rather than a script parsing it, the reader was the model unless a second person
is named.

The author takes full responsibility for the content, including the parts
produced with AI assistance.
