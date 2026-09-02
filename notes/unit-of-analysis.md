# Choosing the unit of analysis — 31 August 2026

**The unit of measurement was changed to the BLOCK.** The per-number count is
reported alongside it as a robustness check.

## The problem

Since v1.2 the instrument had treated **every separate number** inside a block as
one claim, and applied the block's link verdict to all of them. A block holding
five numbers and carrying a **single** link was therefore counted as **five
sourced claims**.

One link does not source five numbers. Usually it sources one of them.

## Who this favoured

Pages that write number-dense blocks — that is, a writing habit, not a sourcing
habit.

| Page | Per number | Per block | Change |
|---|---|---|---|
| `tryprofound.com` | 74% | **55%** | −19 |
| `writer.com` | 58% | **40%** | −18 |
| `ahrefs.com` | 57% | **47%** | −10 |
| `industry-lens.com` | 63% | 67% | +4 |
| `semrush.com` | 11% | 17% | +6 |

**All three pages at the top of the table were inflated.** In a table published
with names attached, that is not acceptable.

## The decision

**Primary measure: per block.** One block is one claim; it counts as reachable if
the block carries a working link to a source.

**Why:**
1. One link does not earn credit for every number in the block
2. It is independent of writing style (number density)
3. It is closer to what a reader experiences: a sourced paragraph, or an unsourced one

**The per-number measure is not dropped** — it appears as a second column in every
table, so a reader can see what both measures say.

## The field-level finding holds under either unit

| | Per number | Per block |
|---|---|---|
| v2 competitor median | 41% | **40%** |
| Round 5 competitor median | 5% | **6%** |
| Spread | 0% – 74% | **0% – 67%** |

The headline finding — **there is no norm, and the same site varies inside
itself** — does not depend on the choice of unit. Only the individual page
percentages move, which is why both are published.

## Our own pages (round 5, excluded from the table, shown here for symmetry)

| Page | Per number | Per block |
|---|---|---|
| `OURS-cited` | 90% | 91% |
| `OURS-geo` | 85% | **75%** |
| `OURS-tools` | 74% | 74% |
| `OURS-track` | 24% | **33%** |

The same correction was applied to us; `OURS-geo` lost 10 points.
