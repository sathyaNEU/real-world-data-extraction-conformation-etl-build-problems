# determinism-check report, task262, 2026-10-15

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, Bash only, readable scope /tmp/determinism-check-task262-r1/. Verdict file: /tmp/determinism-check-task262-r1/verdict.md. (Runtime of the first invocation had no Agent tool, so the main session spawned the thread from judge_brief.md.)

## Why
The brief fixes the population (every child, parents' census income above zero, earnings in at least one year at 30 to 34) and defines long-run income as the level yearly income moves around. Only the census year covers every child, so the elasticity must be de-attenuated with the swing measured in the tax history. Under that, Selvane Valley 0.49 leads Torvale Metro 0.40. The naive census-year slope names Torvale Metro (0.33); the five-year-mean slope on filers names Halverston (0.347); an IV on filers names Kestry North. The filer-only variants are closed by the "every child" population, and coverage differs by region (27% to 91%), so they are selected samples. The main call is analytical, not semantics or rule application.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Children total (cohort extract, brief filters) | 58,202 | 58,441 - 232 - 7 = 58,202 | yes |
| Children by region (8) | 6,106 / 15,320 / 5,261 / 4,220 / 6,868 / 7,726 / 7,152 / 5,549 | identical | yes |
| Selvane Valley elasticity | 0.49 | 0.490 | yes |
| Torvale Metro | 0.40 | 0.402 | yes |
| Wendmoor | 0.39 | 0.393 (0.401 per-child swing weighting) | yes, one fork |
| Kestry North | 0.39 | 0.388 | yes |
| Halverston | 0.39 | 0.388 | yes |
| Danholt Lakes | 0.37 | 0.371 | yes |
| Ostler Plains | 0.34 | 0.337 | yes |
| Caskell Coast | 0.29 | 0.292 | yes |
| Gap Selvane over Torvale | 0.09 | 0.088 | yes |
| Bridges starts (1,353 total) | TVL 318, DAN 193, OST 171, SEL 163, HAL 151, CAS 128, KES 117, WEN 112 | identical (54 transfer links, 233 CaseTrack to Northstar matches, 51 day/month swapped) | yes |
| Spending, nearest $1,000 | TVL 1,442; DAN 973; OST 853; SEL 818; HAL 830; CAS 689; KES 682; WEN 621 | identical; shares sum to ledger total $6,908,544 | yes |

## Competing answers that survived
No fork changes the main call. Residual forks on graded second-order figures:
1. Wendmoor 2-dp value: per-family swing weighting 0.393 (0.39), per-child weighting 0.401 (0.40). Torvale stays ahead at 0.402. Chart order inside the 0.39 trio (Wendmoor 0.393, Kestry North 0.388, Halverston 0.388) is not robust to weighting; the design note's SF11 edge assertion covers estimators of the swing, not this weighting.
2. Selvane per-child swing weighting 0.4950, on the 0.49/0.50 rounding edge (golden 0.490 under per-family, ddof 4).
3. Spending: the accrual treatment is a reading of the ledger descriptions; as posted shifts regional figures by $5,000 to $15,000. The descriptions make the double count visible, so judged forced (ask-side, Layer 1).
4. A literal reader taking "long-run income" as the five-year mean gets Halverston; closed by the brief's every-child population and the "level yearly income moves around" definition (judge's residual risk, SF4).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (CSV, PDF, XLSX, DOCX) | yes |
| Large file | 25,000 rows or more | child_earnings_2014_2022.csv, 525,969 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | regional_economic_indicators_2021.xlsx, youth_aspirations_survey_2023.pdf; names carry no label | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | medians and rates by region; plans after school; neither yields an elasticity or a ranking on persistence. The judge also read the close-out PDF as a distractor, but metadata classes it an ask file (program total, no regional split) | yes |
| Deliverables | 1 to 3, all in golden | 3 (pdf, xlsx, png), all in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each | elasticity (2 dp) with children; starts and spend (nearest $1,000) across 8 regions with transfer, migration and accrual devices | yes |
| Prompt shape and 25 or more criteria | identifiable, 25+ | shape 07 grid; graded figures: 8 elasticities, 8 child counts, 8 starts, 8 spends, call, gap, chart, about 35 or more. Rubric itself not seen (generated at the portal) | yes (by count) |
| Not LLM-looking, goldens real | yes | judge found no authoring disclosures; aspirations survey and indicators a mild "too neat" read, not decisive. Golden realism was a stage-3 gate | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: Gate G method_or_model_selection, Layer 2 family estimation_fit, stump_class analytical, nothing planted. Match. The declared distractors are not the surface read carrying the task. The judge's three wrong routes (census-year naive Torvale, filer five-year mean Halverston, IV Kestry North) agree with the design ladder R0 to R2 (Halverston, Torvale Metro, Kestry North). The note's R2 reliability-ratio route was not run separately by the judge; its IV Kestry North result lands on the same region.

Gate H line: domain pass, layers pass, decisive_step analytical. Matches the note's `## Three rules`: the decisive step is de-attenuating the elasticity with the swing carried from the filers to every family. Swap test holds.

Note vs judge: the note's convergence claim (within-family deviations, half squared year-to-year changes, census as sixth year give the same 2-dp figures) is confirmed for the first-difference swing (Selvane 0.493 vs 0.402). A biased ddof 0 swing gives Selvane 0.402 vs Torvale 0.386, still Selvane, with a 0.016 gap. The 0.09 gap needs the unbiased four-degrees-of-freedom swing, which the golden states.

## Stump power (Gate F)
Moderate to good. A strong model that reads the history file may see the attenuation problem, since the brief's sentence points at it; the tempting wrong answers are the naive slope, the filers' five-year-mean slope and the filers' reliability ratio. Ask-side traps (transfer chains, CaseTrack to Northstar match with swapped day and month, accrual removal) carry the rest and are free of the rules by design. No lever needed for determinism.

## Findings, ranked
1. Low: unfiled swing weighting leaves Wendmoor's 2-dp value (0.39 vs 0.40) and the chart order of ranks 3 to 5 open; Selvane sits on a rounding edge under per-child weighting. Does not touch the call or the gap.
2. Low: the gap of 0.09 holds only under the unbiased swing estimator (ddof 0 gives 0.016). The call is unchanged.
3. Info: accrual treatment on spending is a reading, forced by the ledger descriptions.
4. Info: the judge saw no prior shipped task, so no cross-batch hit is reported (clone-check is author-triggered).

## Next action for the author
Ship. Optional only: if you want to close finding 1, file in the brief that the swing is estimated per region over its families with a history (the WHAT), not the weighting formula; otherwise leave as is.

## After the verdict

The one optional finding (the swing weighted by each family's children moved Wendmoor across 0.395 and put Selvane
Valley on 0.495) was closed in the data, not in a filed sentence: the tax-year draws of Kestry North, Selvane Valley
and Wendmoor and four regions' upper slopes were re-chosen so the swing measured within families, from year-to-year
changes, with the census year as a sixth year, with each family weighted by its children in the sample, or over the
families with a child in the sample gives the same two-decimal elasticity in every region and the same runner-up
(asserted in checks.py, C1). The call, the gap and every rung's winner are unchanged (Selvane Valley 0.49, Torvale
Metro 0.40, a gap of 0.09; Halverston on the filers' averages, Torvale Metro on the census year, Kestry North on the
filers' reliability ratio); Wendmoor now stands at 0.38 and Kestry North at 0.39. No re-judge: the disposition was
APPROVE and no FIX_NOW was raised.
