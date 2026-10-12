# determinism-check report, task185, 2026-10-12 (pass 1)

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
