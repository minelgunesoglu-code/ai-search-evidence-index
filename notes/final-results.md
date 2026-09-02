# The AI Search Evidence Index — the result of record

**Retrieval:** 30 August 2026, 20:38:51–20:40:15 UTC · **Instrument:** v1.7 (block unit)
**Verification:** every published block was read by hand (90 blocks, without exception); 10 machine verdicts were rejected

## The table

Unit = **block**. A block is a paragraph, list item, table row or quote carrying at
least one numeric claim. "Sourced" = the block contains a working link that leads
to the source of that claim.

| Page | Blocks | Sourced | **A%** | *(per number)* |
|---|---|---|---|---|
| industry-lens.com | 21 | 13 | **62%** | *63%* |
| tryprofound.com — *top-experts* | 11 | 6 | **55%** | *74%* |
| tryprofound.com — *what-is-aeo* | 10 | 5 | **50%** | *59%* |
| promptzero.tech | 15 | 6 | **40%** | *44%* |
| writer.com | 35 | 14 | **40%** | *58%* |
| frase.io | 48 | 19 | **40%** | *41%* |
| ahrefs.com | 15 | 5 | **33%** | *57%* |
| aisearch.similarweb.com | 24 | 8 | **33%** | *37%* |
| semrush.com | 18 | 2 | **11%** | *11%* |
| seocrawl.ai | 17 | 1 | **6%** | *9%* |
| tryprofound.com — *best-tools* | 17 | 1 | **6%** | *10%* |
| llmrefs.com | 11 | 0 | **0%** | *0%* |
| zapier.com | 10 | 0 | **0%** | *5%* |

**13 pages · median 33% · range 0%–62% · pooled 80/252 = 31.7%**

Twelve (12) pages carrying fewer than 10 blocks were left without a percentage.

## Corrections made by hand (machine → human)

Each was read and rejected:

| Page | Rejected | Reason |
|---|---|---|
| `ahrefs.com` | `help.ahrefs.com/…` · `linkedin.com/in/joshuahardwick28` | help document · personal profile |
| `frase.io` | `/blog/ai-visibility` · `/tools/geo-score?utm_…` | its own guide · its own tool |
| `aisearch.similarweb.com` | `/ai-brand-visibility/prompt-analysis/` | its own tool |
| `promptzero.tech` | `promptzero.tech/#features` | its own product section |
| `semrush.com` | `semrush.com/ai-seo/overview/` | its own product page |
| `zapier.com` | `zapier.com/apps` | its own app directory |
| `industry-lens.com` | `ahrefs.com/pricing` (for the "466M prompts" claim) | the pricing page does not carry that figure |
| `tryprofound.com-4` | its own related article (for the Gartner claim) | does not source the claim |

## Three warnings to publish alongside the result

**1. `industry-lens.com` is structurally advantaged.** It leads the table, but most
of its sources are **its own `/reports/` pages**. The site is a news aggregator;
every item it publishes already points at a source. That is a difference in kind,
not a mark of superiority.

**2. The measured error in claim detection: 22.4%.** In the blind 120-block sample,
19 of the 85 blocks the instrument would actually score were not claims at all
(advice, biography, examples of writing) — 95% CI 13%–31%. Only 3 of those 19 had
been counted as sourced, so they sit mostly on the unsourced side, which means
**the published rates run below the true figure.** Applied to the 252 blocks, the
corrected pooled estimate is ≈ **36%**. (An earlier 50-block pass gave a consistent
22%, but its per-item verdicts were not retained and cannot be reproduced from the
published sheets.)

**3. Six pages could not be retrieved: four to HTTP 403 bot protection, two to connection errors** — and they are not
random: searchengineland (2), business.adobe.com, technologyadvice, brafton,
otterly. A rough browser-side reading gave 8%, 14%, 11%, 71%, 100%. They are not
part of the main table.

## The finding that did not move

The unit changed (number → block), 10 links were rejected by hand, and the sample
grew from two queries to six. **The headline finding survived all three changes:**

> There is no norm for sourcing in this field. Pages run from **0% to 62%**, and
> **the gap between one publisher's own pages** is as wide as the gap between
> publishers: `tryprofound.com` scores 55% on one page and 6% on another.

Sourcing is not a house policy; it varies page by page and writer by writer.
