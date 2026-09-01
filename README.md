# The AI Search Evidence Index

**Source determinability of numeric claims on AI-visibility web pages**

| | |
|---|---|
| **Article** | https://ismybrandinai.com/do-ai-visibility-guides-link-their-sources |
| **Retrieved** | 30 August 2026, 20:38:51–20:40:17 UTC — one 86-second window |
| **Pages** | 38 sampled · 32 retrieved · 13 in the published table |
| **Headline** | Across the 13 pages, a median of **33%** of blocks containing a numeric claim carry a working link to the source. The spread runs from **0% to 62%**. |
| **Reliability** | Cohen's κ = 0.80 between two independent coders (n = 12): an AI model reading the pages by hand, and a person |
| **Licence** | CC BY 4.0 — see `LICENSE` for what it does and does not cover |


Data, code and coding materials for a measurement of whether a reader can reach
the source of a numeric claim on pages that rank for AI-search-visibility queries.

**What is measured:** determinability — can a reader reach the source of a figure.
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

**The authors' own site (ismybrandinai.com) is excluded from the dataset.** The
authors had the instrument in hand while writing their own pages; the measured
pages did not. Any figure for the authors' pages would not be comparable.

## 2. Retrieval

All 38 URLs were fetched inside a single window: **30 August 2026,
20:38:51 – 20:40:17 UTC**. 32 were retrieved; **6 failed** (HTTP 403 bot
protection or connection failure) and are listed with their status in
`data/retrieval-log.csv`. The failures are not random — they are larger,
established sites — and this is stated as a limitation.

**Raw HTML snapshots are not redistributed here**, to avoid republishing third-party content in
full. Instead the dataset carries, for every retrieved page, its **URL, retrieval timestamp, byte
size and the SHA-256 hash of the exact snapshot we measured**
(`data/snapshot-hashes.csv`).

That is enough to reproduce and to falsify. Re-fetch a URL, hash what you get, and compare: an
identical hash means you are looking at the document we measured; a different one means the page
has changed since 30 August 2026 — which is itself worth knowing. In an earlier round one page
lost 181 footnote links between two retrievals a day apart.

Quoted excerpts appear only in the coding sheets, only where they are needed to show why a block
was coded as it was, and are capped at roughly 200 characters. Across all measured pages the
excerpts total about 16,000 characters — for most pages between 1% and 3% of the page. Snapshots
are retained by the authors and can be made available for verification on request.

## 3. Unit of analysis

The unit is a **block**: a `<p>`, `<li>`, `<tr>` or `<blockquote>` element of at
least 60 characters that contains at least one numeric claim.

An earlier version of the instrument counted each distinct number as a separate
claim and applied the block's link verdict to all of them. That over-credited a
single link with sourcing several figures, and inflated pages that write
number-dense blocks. The block was adopted as the unit; the per-number figures
are retained in `data/measurement-per-number.json` as a robustness check.

## 4. Coding scheme

Each block receives one code:

| Code | Definition |
|---|---|
| **A** | A working link inside the block leads to the source of the figure |
| **B** | A source is named in the block but not linked |
| **C** | Neither |

**Only A is reported as a percentage.** Agreement between the instrument and a
human coder on the B tier reached Cohen's κ = 0.66 — below the level at which a
percentage should be published. B is reported as a flag with hand-verified
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

**Instrument vs. human coder** (n = 30): agreement 83%, **Cohen's κ = 0.66**.
The instrument's errors are one-directional: it never labelled an unnamed source
as named. It only missed named sources. It does not make any page look better
than it is.

**Between two independent coders** (n = 12), one an AI model reading the pages by
hand and one a person: agreement 92%,
**Cohen's κ = 0.80**. Coder 1's codes were sealed (SHA-256) before Coder 2 coded.
Items whose codes had been disclosed in prior discussion were excluded from this
comparison. The single disagreement was resolved by discussion and produced
Rule K; **κ is reported from the pre-discussion codes and is not recomputed.**

Materials: `coding/`.

## 6. Verification

- Every published figure was read by a human. All 89 sourced blocks in the
  published table were inspected individually; 11 machine verdicts were rejected
  on inspection and the rejections are listed in `notes/final-results.md`.
- The counter was **re-implemented independently** (`code/independent-counter.py`)
  without reusing any of the original code. 17 of 25 pages matched exactly; all
  8 differences were traced to two causes (a table-credit rule present in one
  implementation, and a decimal-detection gap), neither of which changes the
  published table by more than one block on one page.

## 7. Known limitations

1. **Claim detection has a measured error rate.** 50 blocks were hand-coded for
   whether they contain a numeric claim at all; **11 (22%, 95% CI 11–33%) did
   not** — advice, author biographies, examples of good writing. Roughly 86% of
   these sat in unsourced blocks, so **the reported percentages understate the
   true rate.** A corrected pool estimate is ≈39% against a raw 31.7%.
2. **Six pages could not be retrieved** and are not random.
3. **One day, one snapshot.** Pages change; one page in an earlier round lost
   181 footnote links between two retrievals.
4. **Non-probability sample.** Six queries are not a field. Findings are stated
   as "these pages, on this date".
5. **Exclusion rules remove nothing from the authors' own pages** — the authors
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
          sampling-frame.json         the six queries and every organic result
          measurement-by-block.json   block-unit measurement (primary)
          measurement-per-number.json per-number measurement (robustness check)
code/     fetch.py                    single-window retrieval
          measure.py                  the instrument
          independent-counter.py      independent re-implementation
          dump-blocks.py              dumps a page's sourced blocks for human reading
coding/   coded-items.json            the coded items
          coder1-sealed-codes.json    Coder 1, sealed with SHA-256
          intercoder-kappa.json       inter-coder result
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

- **An error in the measurement, the code or the coding** — open an issue on this
  repository, or write to minel@ismybrandinai.com.
- **You publish one of the measured pages and want an excerpt removed** — write to
  info@ismybrandinai.com and it will be removed.
