# Validating claim detection — 31 August 2026

Until now what was tested was the instrument's **verdict** ("does this number have
a link"). This document tests its **counting**: *is what the machine counts as a
claim actually a claim?*

That is the **denominator** of the percentages. If the denominator inflates, every
rate falls.

## Method

Two independent samples, both random (seed recorded), **50 items** in total, coded
by hand. One question: *is this a factual numeric claim whose source a reader could
ask for?*

- **Counted as a claim:** a research statistic, a price, product scope (number of engines or languages), a case-study result, the methodology of the page's own measurements
- **Not counted as a claim:** advice ("refresh every 90 days"), an author biography, an example of good writing, an idiom ("Fortune 500"), a date, a worked formula

## Result

| | |
|---|---|
| Items coded | **50** |
| Not a claim | **11** |
| **False-positive rate** | **22%** (95% CI: 11% – 33%) |
| Of those, unlinked | **6/7** *(measured in the first sample)* |

## The direction is what matters

Almost all the false positives are **unlinked**. So the denominator inflates while
the numerator does not → **every percentage runs below the truth.** It is an error
that makes everyone, ourselves included, look worse.

| | Raw | Corrected point estimate | Range |
|---|---|---|---|
| Pooled rate (474 claims, 178 linked) | **37.6%** | **46.3%** | 41% – 53% |
| Page median | **24%** | **~29%** | — |

## A mechanical fix was TRIED and was NOT enough

In v1.7 the unambiguous categories were filtered out (biography patterns, the
`N out of M` formula example, the `31 Jul 2026` date format, `Fortune 500`).
13 of 474 claims dropped, and the median moved from 23% to 24%.

**But in the second sample the false-positive rate stayed at 20%** (from 23%). The
filters caught those particular phrasings, not the category:

| What slipped through | Why a regex cannot catch it |
|---|---|
| "Review top-performing content every 90 days" | advice — grammatically indistinguishable from a claim |
| "worked as senior SEO specialist for Chess.com — one of the top 100 most visited websites" | a biography, phrased differently |
| `GEO-optimized: "Video content is increasingly surfaced by AI engines…"` | an example of good writing, inside quotes, but the template filter misses it |
| "Choose Google AI Overviews if: You already rank well organically" | advice |

**Decision: no more patterns will be added.** Every addition produced a new false
alarm (see `instrument-revisions.md`, v1.4 and v1.6). Instead, **the calibration is
published**: the raw figure, the hand-measured 22% false-positive rate, the
confidence interval, and the corrected estimate.

## As it will appear in the report

> Our instrument counts the numeric claims on each page automatically. Checking 50
> claims by hand, we measured that **22% of them (95% CI: 11%–33%)** were not
> claims at all — sentences of advice, author biographies, examples of writing.
> Almost all of these miscounts sit in unlinked blocks, which means the rates we
> publish are **below the true figure**. We give the raw and the corrected numbers
> together; the raw one is what we measured, the corrected one is our estimate.

## Why this is acceptable

1. The error is **symmetrical** — the same instrument was applied to everyone, so the ranking does not change
2. Its direction is **known and one-way** — it makes nobody look better than they are
3. Its size is **measured**, not guessed
4. The finding itself (**a 0%–74% spread, even within one site**) is unaffected by this correction — the spread rests on the differences between the rates, not on their absolute level
