# determinism-check report, task185, 2026-10-12 (pass 2 headline; pass 1 below)

## Headline (pass 2)
DETERMINISTIC, **Disposition: APPROVE**. Stumping type: mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. Gate H: domain pass, layers pass, decisive_step analytical.

# Pass 1 (superseded)

## Verdict
DETERMINISTIC, with SOLUTION_WRONG on a minor wording point (submission step 2 mixed pooled and Merrin Flat figures).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced by the pricing manual (rev 3) and the 2027/28 term sheet once the glass seasons are brought to the probe's basis at each glass reading. Readings of 34.5 C and 39.0 C and up cross the 35.0 and 40.0 triggers, giving +54 heat days and +29 severe days. The result is 16.658 heat days, 4.134 severe days and a burn of 397.41, times 1.32 = $524.58, which rounds to $525. Every reading-by-reading table the thread tried gave the same integer counts and the same premium: pooled seven-site, Merrin Flat only, 1 C or 2 C bins, quadratic or cubic, and a quantile map on Merrin Flat. The premium sits 0.08 above the 524.5 rounding line, which is thin but clean. The findings were an open fork on ask 3 (which source governs a block's sub-district) and the step 2 wording.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Glass days gained, heat / severe | 54 / 29 | 54 (at 34.5) / 17 + 12 | yes (register xlsx, parallel file) |
| Difference at 34.5 / 39.0 (pooled) | +0.72 / +1.35 | 0.719 (n=108) / 1.354 | yes |
| Heat / severe slope per decade | 0.30 / 0.19 | 0.296 / 0.191 | yes |
| 2027/28 line values | 16.7 / 4.1 | 16.658 / 4.134 | yes |
| Premium per hectare | $525 | $524.58 | yes |
| Schedule | 115 blocks, 722.7 ha | 115, 722.7 | yes |
| Sub-district blocks, ha, premium | 28/184.8/$97,020; 17/100.5/$52,763; 33/178.7/$93,818; 37/258.7/$135,818 | same, by block register | yes, under reading A only |
| Claims paid by season | 25, 28, 36, 38, 45, 52, 54, 55 | same | yes (GL by claim reference, season from claims register) |
| Payouts by season | $80,344 / 79,148 / 50,260 / 63,534 / 195,809 / 285,417 / 433,200 / 35,631 | same | yes |
| "+0.13 C on average" in step 2 | Merrin Flat mean | pooled mean is +0.17; Merrin Flat at the two readings is +0.62 / +1.40 | wording mixed bases |

## Competing answers that survived
- **Ask 3, sub-district source (open at pass 1):** the block register gives 28/184.8, 17/100.5, 33/178.7, 37/258.7. The policy schedule's own column gives 32/209.3, 15/87.5, 32/185.1, 36/240.8. Sixteen of 115 blocks differ and no shipped text said which governs. The coordinator closed this in the extract notes after the pass.
- **Whole-range linear fit of the difference on the reading:** $542 pooled (16.7 / 4.4), $557 Merrin Flat only. The data separate it, since the difference is flat and then bends, but the text files no method. This is a designed rung, left open on purpose.
- **Excluded as non-literal:**
  - A probability-of-exceedance conversion ($518 or $527).
  - A pooled quantile map across seven sites ($487).
  - Rounding the projected counts first ($522); manual 3.4 says counts are not rounded.
- **Easy route:** a mean offset or the raw glass record gives $567 with 17.2 / 4.5. This is the intended wrong answer.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 5 (csv, pdf, xlsx, json, md) | yes |
| Large file | 25,000 rows or more | daily series, 34,404 rows | yes |
| Distractors | 2 or more, in metadata, no file name labels one | `ncs_district_stations_monthly_mean_max.csv` and `heat_cover_term_sheet_2026_27.pdf`; neither is labelled by name | yes |
| Distractor weighs but is unused | yes | the 2026/27 terms differ (deductible 15, rates 38.60 and 55.70, cap 1,350); the quote is priced on the 2027/28 terms; district means unused | yes |
| Deliverables | 1 to 3, all in the golden | 2 (a quote PDF and a payouts CSV), both in `golden/` | yes |
| Asks | multi-dimensional, unit and rounding stated | schedule by 4 sub-districts, 8 seasons by 2 figures, the chart; units and rounding stated | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 14; the design note counts 41 criteria; I did not generate the rubric | yes (by the note's count) |
| Reads as real, not LLM generated | yes | the thread found a clean hygiene pass (digitised register, quality flags, duplicated rows, day-first GL dates, a desk note) | yes |

Mild flag from the thread: the prompt says "since it went automatic in November 1995", which pre-names the instrument change. The first-order trap is still the level-dependence of the difference, so this is not an exclusion.

## Gate G reconciliation
The thread returned `method_or_model_selection`, `analytical_non_defect`, surface read `no` and sole data defect `no`. The card and design note declare Gate G `method_or_model_selection` and the stump as a conversion sized at each reading, with the mean-difference path ending on $567. This matches. The declared distractors (the 2026/27 term sheet and the district means) are not the surface read carrying the task. The stump sentence matches the thread's easy route and its "$542 for one offset" figure. The thread's regression-on-reading route ($542) is the design note's own "linear fit over all days" default. Gate G is classified as analytical, with no planted defect.

Gate H: domain pass, layers pass, decisive_step analytical. The thread's Layer 2 is homogenising a 30-year glass record to the present probe before fitting the trend and pricing the burn. The card's `domain_test` and `analyst_test` agree: the strong analyst who reads everything correctly and applies the mean difference lands on $567. There is no mismatch.

## Stump power (Gate F)
Moderate to good. The mean offset or raw route files $567 and a one-offset route files $542, while only the reading-specific difference gives $525. The station history and the parallel file are handed over, so the hurdle is whether a solver examines the difference by reading and not on average.

## Findings, ranked
1. Ask 3 fork (underspecified_objective): the sub-district source was unfiled, and the schedule and the register disagree on 16 blocks. The solution said "per the register" with no shipped file stating it.
2. Step 2 of the solution blocks mixed pooled and Merrin Flat figures (+0.72 and +1.35 pooled against +0.13 Merrin Flat).
3. Residual: the whole-range linear fit of the difference ($542 pooled, $557 Merrin Flat) is not excluded by text. It is a designed rung and low weight.
4. Minor: the four rounded sub-district premiums sum to $379,419 against a rounded total of $379,418. A solver who prints a total would disagree with the golden.
5. Not yet checked: the thread could not run a cross-batch duplicate check.

## Next action for the author
Pin the register as the sub-district source in the extract notes. Correct submission step 2 to the seven sites pooled, with no Merrin Flat mean. Drop the summed premium from the quote's total row. Then re-judge once (pass 2).


---

# Pass 2 (current bundle and submission after the generator fixes)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
A fresh thread reproduced every committed answer from the shipped files: premium $525 (397.41 x 1.32 = 524.58), 16.66 / 4.13 days (lines 0.2959 and 0.1911 a year), the 115 blocks and 722.7 ha, the four sub-district rows, and the eight seasons of payouts. The pooled difference of +0.719 C at 34.5 C and +1.354 C at 39.0 C sets the two crossings. Each of these gives $525:
- Merrin Flat only.
- The other six sites only.
- The per-reading median.
- A quadratic fit of the difference.
- An OLS fit on readings of 30 C and over.
- A bootstrap of the pairs: the crossings were unchanged in 300 of 300 draws.

The ask 3 fork is closed: the extract notes name the register as the co-operative's sub-districts. Step 2 is consistent (seven sites pooled). The summed premium is gone from the quote, so the $379,419 against $379,418 rounding difference does not bite.

## Competing answers that survived
- **Conversion estimator, not forced by text but separated by the data:**
  - A single OLS of probe on glass gives $542. It misfits the hot end, predicting +0.67 at 39.0 C against +1.35 observed.
  - Expected exceedance gives $518, and yields fractional days, which the manual's "each day's maximum" does not describe.
- **Easy route:** no adjustment or any constant offset gives $567; a constant offset from readings of 34 C and over gives $506.
- **Margin:** 524.58 is 0.08 above the 524.50 line. Every reasonable per-reading estimator gives identical day counts, so the thread rated it thin but clean.

## Spec gates (reconciled)
All pass, unchanged from pass 1: 14 files, 5 formats, 34,404 rows in the largest file, two distractors named in `metadata.json` and not labelled by file name, 2 deliverables both in the golden, shape 14 (41 criteria by the design note). The thread's hygiene read: clean, temporally coherent, nothing exclusion-level.

## Gate G reconciliation
The thread returned `method_or_model_selection`, `analytical_non_defect`, surface read no, sole data defect no. This matches the card and design note. Gate G is classified as analytical. The declared distractors, the 2026/27 term sheet and the district means, are not what carries the task. The thread gave a borderline note: the prompt itself names the changeover, so a reader could call the raw-count rejection a surface-read flip. It judged the decisive work to be estimating the conversion, not spotting a defect.

Gate H: domain pass, layers pass, decisive_step analytical. The easy route (a count of raw or constant-offset days) files $567; the reading-dependent conversion files $525. The thread's swap test says the task does not read the same with other nouns. There is no mismatch with the card's `analyst_test` and `domain_test`.

## Stump power (Gate F)
Moderate to good. A strong run can fail on a mean offset or a global regression ($542). The prompt flags the changeover and the manual pins the target instrument, so some strong runs will land it. The thread says no lever is needed before live testing.

## Findings, ranked
1. None blocking.
2. Optional, solution text only: state that the mean difference is read at each half-degree reading, with 34.5 C and 39.0 C the crossing readings, so the estimator is on record. No change to files or prompt.
3. The rounding margin of $0.08 is the most fragile point, but it is not contested.

## Next action for the author
Proceed to ship (stage 5). Optionally add the estimator sentence to the write-up.
