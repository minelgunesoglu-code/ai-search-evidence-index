# Verification by hand — round 5 (30 August 2026, 20:04 UTC)

Every claim counted as "linked" on a page that would be named was **read one at a
time.** The aim: a human confirms each machine verdict before the page is published
under its own name.

## 1. The three pages scoring "0%" — is the zero real

Giving a page an unfair zero is worse than a false positive. All three were checked
by counting every outbound link in the body.

| Page | Outbound links | What they were | Verdict |
|---|---|---|---|
| `llmrefs.com` | **0** | no outbound links in the body at all | 0% **correct** |
| `ayzeo.com` | 8 | all fonts / CDN / social share | 0% **correct** |
| `obapr.com` | 10 | 5 share buttons, a font, LinkedIn + **3 vendor links** | see below |

### `obapr.com` — where the rule decides the score

The page carries three price claims and links all three vendors:

- "Otterly.AI … Pricing: ~$99–299/month" → `otterly.ai` **(home page)**
- "Profound … Pricing: Custom enterprise" → `tryprofound.com` **(home page)**
- "AIClicks.io … Pricing: ~$79–199/month" → `aiclicks.io` **(home page)**

Rule (E) does not count a home-page link as a source: it does not take the reader to
where the price is written. Our own page links `otterly.ai/pricing`, which does.

The distinction is defensible, but **it decides obapr's score outright.** The rule
will be stated in the report alongside this example.

## 2. How much each rule costs each page — a full count

How many links the three exclusion rules (CTA/booking, home page, related-article
card) remove from each page:

| Page | Outbound | CTA | Home page | Card | Removed |
|---|---|---|---|---|---|
| **OURS-cited** | 11 | 0 | 0 | 0 | **0** |
| **OURS-geo** | 3 | 0 | 0 | 0 | **0** |
| **OURS-tools** | 21 | 0 | 0 | 0 | **0** |
| **OURS-track** | 11 | 0 | 0 | 0 | **0** |
| data-mania.com | 42 | 2 | 24 | 0 | 26 |
| aiclicks.io | 22 | 0 | 17 | 0 | 17 |
| dageno.ai | 19 | 0 | 5 | 0 | 5 |
| evertune.ai | 5 | 0 | 3 | 0 | 3 |
| obapr.com | 4 | 0 | 3 | 0 | 3 |
| usegrowthos.com | 5 | 3 | 0 | 0 | 3 |
| istudiosmedia.com | 3 | 0 | 2 | 0 | 2 |
| xseek.io | 3 | 1 | 1 | 0 | 2 |
| llmpulse.ai | 7 | 1 | 0 | 0 | 1 |
| industry-lens.com | 25 | 0 | 1 | 0 | 1 |
| visiblie.com | 1 | 1 | 0 | 0 | 1 |
| aitoolssme.com, ayzeo, frase, nav43, semrush, useomnia | — | 0 | 0 | 0 | **0** |

**Not one of the 46 outbound links on our own four pages is removed.**

The rules are not biased by construction — a sign-up button really is not a source.
But **their effect runs one way.** This table is published in the report so a reader
can see for themselves how much the rule decides the outcome.

Also: these rules were found **while reading competitors' pages**, not while reading
our own.

## 3. Tier A read page by page

| Page | Machine | On reading by hand |
|---|---|---|
| `visiblie.com` | 3 linked | **all three were "Start Free Trial" buttons** → corrected to 0 |
| `nav43.com` | 5 linked | **two were "Read Post" cards** → corrected to 3 |
| `data-mania.com` | 9 | one was a savvycal booking link → corrected to 8 |
| `useomnia.com` | 7 | one was a `/demo` button → 6. The rest are real: G2, Microsoft Clarity, Forrester |
| `usegrowthos.com` | 3 | two are real outside sources (TechCrunch, Gartner), one its own blog |
| `industry-lens.com` | 24 | mostly real outbound links (peec.ai/pricing, ahrefs.com/blog, tryprofound.com…). The site is a news aggregator and therefore structurally advantaged — to be stated in the report |
| `llmpulse.ai` | 8 | its own glossary and pricing page plus its own study. Legitimate self-citation |
| `xseek.io` | 1 | the arXiv GEO paper — a real academic citation |
| `OURS-tools` | 31 | none of the 21 outbound links is a home page; all go to specific pages |
| `OURS-cited` | 18 | of the 9 read, 9 are outbound: searchengineland, ahrefs, arxiv |
| `OURS-geo` | 22 | mostly self-citation to our own study — five were broken on 30.08 and were fixed |
| `OURS-track` | 7 | 5 vendor pricing pages, 3 BrightEdge |

## Still to do

- One hand-verified tier-B example per page
- The eight small-sample pages (fewer than 10 claims) stay without a percentage; if they are to be named, their links must be read too

## 4. End-of-page bibliographies — the instrument's largest remaining flaw

The measure is **per block**: for a number to count as sourced, the link has to sit
inside that block. A page that gathers its citations academically **at the end** looks,
on this measure, as though it sourced nothing.

Every page was scanned. Three carry an end-of-page citation list:

| Page | Measured A% | Entries | Linked |
|---|---|---|---|
| **`ayzeo.com`** | **0%** | **9** | **0** |
| `xseek.io` | 4% | 2 | 1 |
| `obapr.com` | 0% | 1 | 1 |

### `ayzeo.com` — the worst injustice, caught before publication

At the foot of the page is a bibliography of nine entries, none of them linked:

1. BrightEdge Research (2025). *ChatGPT Brand Mentions vs. Citations.*
2. Frase.io (2025). *Are FAQs and FAQ Schemas Important to AI Search, GEO and AEO?*
3. Averi (2025). *Schema Markup for AI Citations.*
4. SingleGrain (2025). *How E-E-A-T SEO Builds Trust in AI Search Results.*
5. **Reuters (2024).** *Reddit in AI content licensing deal with Google.*
6. **Reuters (2023).** *Associated Press, OpenAI partner…*
7. **Associated Press News (2023).** *OpenAI to start using news content from News Corp.*
8. Generative AI Pub (2024). *Stack Overflow Partners With OpenAI.*
9. Previsible (2025). *LLMs Are Transforming Search But…*

The body also carries cited references such as `Princeton-led GEO study` and
`Aggarwal, P. … (2024). GEO: Generative Engine Optimization. KDD '24`.

Publishing this page as simply **"0%"** would have been a misrepresentation. A reader
can reach the sources from those entries — more easily than from many hyperlinks.

### `xseek.io` — a "Sources & References" section

There is a five-entry sources section; four are linked (the arXiv GEO paper,
seranking.com, its own studies). But because the entries sit **at the foot of the
page rather than beside the numbers**, a per-block measure cannot attach them to the
claims in the body. The measured A value stays at 4%.

### The decision

**The A percentage does not change** — what it measures is inline reachability, and
that is a valid measure. But a **bibliography column is added** to the table, and for
each page we publish "end-of-page citations: N entries, M of them linked".

The addition is mechanical, requires no judgement, and on its own stops a reader who
looks only at A from drawing the wrong conclusion about `ayzeo.com` and `xseek.io`.

## 5. End-of-page citation scan — the v2 round (2 September 2026)

The citation scan done in round 5 had not been repeated in this round. The article
names that gap as the instrument's largest remaining flaw, and the 0% scores were about
to be published without the scan being run. It was run.

**Method.** `code/bibliography-scan.py`: the final third of each page is searched for
a source heading (`Sources`, `References`, `Bibliography`, `Citations`,
`Works cited`, `Further reading`), and where one is found the outbound links beneath
it are counted. An automated scan is not evidence on its own; every hit is read by hand.

**Result: a heading was found on 1 of the 32 pages.**

| Page | Measured A% | Heading | Outbound links |
|---|---|---|---|
| `ahrefs.com` | 33% | *Further reading* | 4 |

And it is **not a bibliography.** The four links are two Search Engine Journal posts,
the schema.org validator and one more — none of them the source of any number in the
body; they are suggested further reading. Ahrefs' 33% does not change.

**Read by hand.** The closing blocks of the four lowest-scoring pages that carry a
published percentage were read one at a time, because that is where the risk was:

| Page | A% | How the page ends |
|---|---|---|
| `llmrefs.com` | **0%** | a bulleted list of "takeaways" |
| `zapier.com` | **0%** | related-article cards plus a product call to action |
| `seocrawl.ai` | 6% | a product feature table |
| `tryprofound.com-2` | 6% | related-article cards |

None of them carries a source list.

**What goes in the report:** in this round, no page gathers its sources at the end.
The two published 0% scores are not the result of a per-block measure overlooking a
bibliography. Round 5 was different (`ayzeo.com` had 9 bibliography entries, none of
them linked) — which is why the check must be repeated every round, and has been made
a rule.
