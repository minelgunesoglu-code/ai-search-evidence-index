# Inter-coder reliability — 31 August 2026

## Method

Two independent coders, coding blind:

- **Coder 1 (Claude):** coded 30 items and **sealed the codes in advance**
  (`kor-kod-CLAUDE-1-30.json`, sha256 recorded, 30 August)
- **Coder 2 (the site's owner):** independently coded the 12 of those items
  **whose codes had never been seen** (31 August)

The 18 items whose codes had been revealed during discussion were **deliberately
excluded** — they can no longer count as blind. The remaining 12 were used.

Coder 2 was given only the block text and the measured value; the machine's
verdict, coder 1's code and the link status were withheld. *(That the blocks
carried no links had been verified mechanically beforehand, so that dimension was
not part of the judgement.)*

## Result

| | |
|---|---|
| n | **12** |
| Agreement (Po) | **11/12 = 92%** |
| Chance agreement (Pe) | 0.583 |
| **Cohen's κ** | **0.800** |

*Substantial* on the Landis & Koch scale — just below the 0.81 threshold for
*almost perfect*.

## The single disagreement, and the codebook gap it exposed

**Item 10** (`industry-lens.com`):

> "GEO went from a fringe idea to a **22,000**-search-a-month category in 2026."

| Coder | Code |
|---|---|
| Claude | **Y** (no source) |
| Site owner | **A** (a source is named) |

Further into the block comes *"IndustryLens tracks ten of them"* — that is, the
page **names itself**.

**The codebook does not cover this case:** *does a publisher naming itself count
as naming a source?*

This should have been settled **before** coding. The decision will be stated
plainly in the article and this disagreement given as the example.

## A correction about the sealing method

While verifying the seal, the hash **did not match**. On inspection: the codes had
not changed. When the seal was taken the dictionary keys were **integers**; read
back from the file they were **strings**, and `sort_keys` ordered them differently.
Same data, different order, different hash.

Recomputed with integer keys, the seal **matched exactly** (`0fa1d0bb…6070`).

**The lesson:** a seal that cannot be verified is not a seal. From now on keys are
normalised to one form before hashing. This incident is recorded in the report — a
verification step that turns out to be flawed itself is something to write down,
not something to hide.

## As it will appear in the report

> Coding reliability was measured with two independent coders. The first coder's
> codes were encrypted and sealed before the second coded anything. Across the 12
> overlapping items, agreement was 92%, **Cohen's κ = 0.80**. The single
> disagreement arose from a case the codebook did not cover: whether a publisher
> naming itself counts as naming a source.

---

## Resolving the disagreement — 31 August, after discussion

**Coder 2 (the site's owner) reported that the `A` code written for item 10 came
from misreading the question, and that the real judgement was `Y`.**

**κ is nevertheless UNCHANGED and reported as 0.80.** The reason: the difference
between "I misread it" and "I changed my mind once I saw the other coder's answer"
**cannot be verified from outside** — and often the coder cannot tell either.
Reliability is therefore computed from the coders' **first recorded** codes.

With the corrected code κ comes out at 1.00. Reporting that would be wrong for two
reasons: it would mean changing recorded data after discussion, and perfect
agreement across 12 items would itself invite suspicion. **0.80 is both true and
defensible.**

**As reported:** pre-discussion agreement **92%, κ = 0.80**; the single
disagreement was resolved by discussion and added to the codebook as a rule.

### RULE K (31.08.2026 — added after coding, and this is stated openly)

> A publisher **naming itself** does not count as naming a source — unless it
> points to a specific, identified piece of work.

| Example | Rule K |
|---|---|
| "IndustryLens tracks ten of them" | **does not count** — it does not take the reader to a document |
| "Similarweb's *2026 Generative AI Brand Visibility Index*" | **counts** — a specific study with a name |
| "We analyzed 700,000+ conversations from ChatGPT.com (Oct–Dec 2025)" | **counts** — what was measured and when is stated |

The test has not changed: **can the reader go and look?**

### The effect of Rule K

The rule concerns only **tier B** (named, not linked); tier A is link-based and is
unaffected. B is not published as a percentage anyway, so there is no effect on the
table — the effect is on the **B examples** we chose:

- The "(HubSpot, January 2026)" example given for `hubspot.com` **falls under
  Rule K** — its own name, not a specific piece of work
- The "We analyzed 700,000+ conversations… (Oct–Dec 2025)" example given for
  `tryprofound.com` **stands** — identified and dated
