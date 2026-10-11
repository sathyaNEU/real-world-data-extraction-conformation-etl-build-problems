# determinism-check report (pass 2), task182, 2026-10-11

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (a per-bore climate-response counterfactual, run forward, then a decomposition of the observed fall into climate and mine), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

**Process note.** This run had no Agent tool, so no separate judge thread was spawned. I did the judge's recomputation myself in a scratch copy of `target/` (`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/t`). I read only `prompt.md`, `submission.md`, `target/`, the metadata and the judge system prompt. I read the golden xlsx and docx only after the recomputation was finished, to compare. I did not open the design note, generator, verifier, solver_rounds/ or any earlier report, so the Gate G reconciliation against the design note was not done (the caller barred it). All recomputation used pandas, numpy and scipy from the shipped files only.

## Why
Every September level and change reproduced exactly from the files. Every attributed decline reproduced inside the stated band when the gamma response is fitted properly; the largest gap is 0.07 m, against a 0.3 m band. The offer list is forced: five bores (KV-LB04, 05, 07, 10, 12) clear their triggers by 3.3 to 4.3 m at the coal-measure bores and 2.4 m at KV-LB12, and no other bore comes near its trigger. Reading KV-LB16 as an unaffected coal-measures control is ruled out by its own record.

## Recomputation ledger
Level and change come from the register, dips and loggers (bore-day means in Queensland time, barometric compensation, measuring point in force, ft converted, duplicates and pumped dips dropped). Decline is fitted level for September 2026 less the September assessment level, from a gamma response to rainfall less a share of Morton evaporation, fitted on readings before 4 July 2022 with shape, mean response time and evaporation share optimised continuously.

| Bore | Level claimed | Level recomputed | Change claimed | Change recomputed | Decline claimed (band) | Decline recomputed | Reproduced |
|---|---|---|---|---|---|---|---|
| KV-LB01 | 209.51 | 209.510 | -4.63 | -4.630 | 0.6 (0.3) | 0.64 | yes |
| KV-LB02 | 205.24 | 205.242 | -5.23 | -5.228 | 0.8 (0.3) | 0.77 | yes |
| KV-LB03 | 204.86 | 204.860 | -4.64 | -4.640 | 0.6 (0.3) | 0.63 | yes |
| KV-LB04 | 207.77 | 207.768 | -2.44 | -2.442 | 8.7 (0.3) | 8.71 | yes |
| KV-LB05 | 214.47 | 214.471 | -2.49 | -2.489 | 9.3 (0.3) | 9.33 | yes |
| KV-LB06 | 209.61 | 209.610 | -4.84 | -4.840 | 0.5 (0.4) | 0.50 | yes |
| KV-LB07 | 195.44 | 195.442 | -2.46 | -2.458 | 8.4 (0.3) | 8.39 | yes |
| KV-LB08 | 201.27 | 201.267 | -4.81 | -4.813 | 0.5 (0.3) | 0.54 | yes |
| KV-LB09 | 199.16 | 199.163 | -4.69 | -4.687 | 0.4 (0.3) | 0.42 | yes |
| KV-LB10 | 203.49 | 203.490 | -2.21 | -2.210 | 8.3 (0.3) | 8.32 | yes |
| KV-LB11 | 238.12 | 238.120 | -2.59 | -2.590 | 1.1 (0.3) | 1.10 | yes |
| KV-LB12 | 209.50 | 209.498 | -8.78 | -8.782 | 4.4 (0.3) | 4.45 | yes |
| KV-LB13 | 202.33 | 202.330 | -0.98 | -0.980 | 0.1 (0.3) | 0.14 | yes |
| KV-LB14 | 201.88 | 201.877 | -0.87 | -0.873 | 0.1 (0.3) | 0.10 | yes |
| KV-LB15 | 241.33 | 241.328 | -3.02 | -3.022 | 1.6 (0.3) | 1.60 | yes |
| KV-LB16 | 209.84 | 209.843 | +1.74 | +1.743 | 2.4 (0.3) | 2.38 to 2.42 | yes |
| KV-LB17 | 243.13 | 243.133 | -2.68 | -2.677 | 0.9 (0.3) | 0.93 | yes |
| KV-LB18 | 245.75 | 245.748 | -8.70 | -8.702 | 1.5 (0.3) | 1.46 | yes |

- (a) All 18 levels and all 18 changes reproduce to two decimals. The closest rounding margin is 0.0014 m (KV-LB08 -4.813, KV-LB12 -8.782 are comfortably clear; KV-LB05 -2.4886 rounds to -2.49 with 0.004 to spare), so the 0.01 m band on the change column is generous and sufficient.
- All 18 declines fall inside their bands. Spreads from the stated centre: 0.00 to 0.07 m, except KV-LB05 and the first-pass coal fits noted below.
- Other claims checked: the three state reference bores, fitted the same way, give fit-minus-observed of -0.04, -0.12 and +0.01 m (within 0.3 m as claimed; none is coal measures: alluvium, alluvium, basalt). Fit RMSE on the coal-measure bores is 0.026 to 0.040 m, on the others 0.045 to 0.094 m. Counts of five impaired bores and four owners reproduce.
- Not recomputed: the claim that the take in `pit_dewatering_2022-2026.csv`, fitted as a second stress, gives the same five bores. The mine monitoring bore KV-MB01 shows a 6.3 m departure, consistent with the pit acting on the alluvium.

**Fit fragility to know about (a solver error, not a defect in the pack).** A default optimisation capped at shape 12 returns 8.95 for KV-LB04 (still inside the band) but is trapped at a local optimum for KV-LB05 (2.98, RMSE 0.405). Widening the shape bound to 30 and starting from a grid converges to 9.33 (RMSE 0.026). The 15-fold RMSE gap identifies the bad fit.

## Competing answers that survived
None survived as a fork. Three were tested:
1. **Change since baseline against the trigger.** It names the alluvial bores (seven at more than 2 m) and the ridge bore KV-LB18 (8.70 m), and misses the coal measures (2.2 to 2.5 m). It answers a different question from MG-02 4.1 ("decline caused by the mine"; "a decline with another cause is not the mine's"), so it is closed by the shipped rule.
2. **Change less the reference bores' fall.** This keeps KV-LB12 alone. The reference bores are alluvium and basalt, so none stands for the coal measures, and the coal-measure bores' pre-2022 responses (range about 16 m, six to seven year response time) cannot be offset by a bore with a half-year response.
3. **A single exponential response (shape fixed at 1).** It gives declines of 4.5, 5.6, 4.3 and 4.4 m at the four coal bores, straddling the 5 m trigger, but its RMSE is 1.0 to 1.1 m against 0.03 m for the gamma fit. It is rejected by the fit residuals the solver must examine. This is a method-selection error and not a defensible alternative.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in pack | 10 or more | 11 | yes |
| Distinct formats | 3 or more | 5 (csv, md, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | 994,869 rows (parquet), 99,959 (csv) | yes |
| Declared distractors | 2 or more in metadata, none labelled in file names | `landholder_contact_log_2026.xlsx`, `groundwater_quality_2012-2026.csv`; neither name labels them | yes |
| Distractors look relevant, unused, ruled out | same world, no graded quantity from them | contact log (complaint dates, no levels) and water quality (EC, ions by bore) are same-world; neither gives a level or a decline | yes |
| Deliverables | 1 to 3 | 2 (xlsx, docx) | yes |
| Golden deliverables present | all named | both in `golden/` | yes |
| Multi-dimensional asks | not stacked lookups | 18 bores by four figures plus offers list and count and four causal sentences | yes |
| Units and rounding | stated | 2 dp metres AHD, 2 dp change, 1 dp decline, yes/no; offers counted | yes |
| Prompt length | under 1,000 chars | 901 | yes |
| Prompt shape and criteria floor | 25 or more | shape 11; 72 cell values plus the offer list, count and four causal notes comfortably exceed 25 | yes |
| Realism | no LLM tells | golden docx and xlsx read as an internal memo and workbook (named author, offer references, method sheet); not exhaustively edited-pass audited | yes (light check) |

## Gate G reconciliation
Judge classification: mechanism forecasting/decomposition, analytical_non_defect, surface_read_dependency no, sole_data_defect no. The reported numbers in the pack (the register's baseline levels, the dips, the loggers) are fine and nothing shipped is a ranked wrong read; the stump is the choice of estimand (counterfactual from the bore's own climate response, not change since baseline), which survives deleting every messy-data device. Reconciliation against the design note and card was not done, as the caller barred opening the design note. The distractors do not carry the answer, so no distractor finding.

**Gate H:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: a hydrogeologist estimating mine-caused drawdown from a pre-impact rainfall-response model is the field's own analysis and the sentence would not survive swapping in "school" or "visits". Layer 1 is the feet/metres, key variants, measuring-point change, pumped dips, duplicates, logger swaps and barometric compensation; layer 2 is the counterfactual. The easy route (change since baseline, or less the reference bores) gives wrong answers even after clean data and correct rule reading: it picks the alluvial bores and KV-LB18 and misses the four coal-measure bores.

## Stump power (Gate F)
Strong. The coal-measure bores fell only 2.2 to 2.5 m, so the surface read excludes them; the exponential-response shortcut lands on 4.3 to 5.6 m and mostly misses the trigger; the reference-bore subtraction keeps KV-LB12 alone. Getting the five requires recognising the six-year response time and fitting it well. No too-easy signal: the loaded phrase in the prompt ("sucking air") points at the four complainants, who all fail the test.

## Checks the caller asked for
- (a) Levels, changes and declines reproduce within the stated bands: yes, all 18.
- (b) Offer list forced: yes. Five bores clear their trigger and no sixth is close (highest non-offer decline is 2.4 m at KV-LB16 against 5 m). Four owners, since Yarrowmere's two bores are one agreement (MG-02 6.1).
- (c) KV-LB16 as an unaffected coal-measures control remains ruled out. Its own pre-July-2022 record fits the same long-memory response as the other coal bores (shape about 15.5, mean response about 6.6 years, RMSE 0.036 m). Run forward, its observed level departs from its climate-only trajectory by an increasing amount, from 0.0 m in 2022 to 0.2, 0.8, 1.7 and 2.3 m in the following years, the same shape as KV-LB04 (0.4, 2.2, 4.9, 6.8, 8.2) and KV-LB07. It is therefore itself drawn down by 2.4 m. Its +1.74 m rise since baseline also cannot be subtracted from other bores' falls, since its pre-2022 range is about 4 m against about 16 m at KV-LB04 and 07. Using the +1.74 m as a control would give KV-LB04 a decline of 4.2 m and no coal-measure offers, which the bundle's record contradicts.
- (d) KV-LB12 at 4.45 m sits on the 4.4/4.5 rounding edge, but the band is 4.4 plus or minus 0.3 (4.1 to 4.7), which takes both roundings and the exponential variant's 4.3. It is safely graded. The trigger test is not sensitive: 4.45 against 2 m.

## Findings, ranked
1. Pass 1's three findings are closed: declines reproduce from a continuous refit, the change column has a 0.01 m band, and the golden's method sheet describes the refit (note: the golden `Method` sheet claims "other response forms ... give the same five bores"; my single-exponential variant does not, because it fits poorly. The statement is true of the response forms that fit, and the judge would not treat it as a defect, but the author may wish to say "other response forms that fit the pre-2022 record").
2. A solver fit that stops at a local optimum (KV-LB05: 2.98 m, RMSE 0.405) lands outside the band. That is a solver error identifiable from the residuals, not a gap in the pack.
3. Not checked in this pass: the golden memo's reference-bore distances (25 to 32 km), the 2019 to 2021 rise rates (0.6 to 0.8 m a year), and the second-stress pit-volume fit.

## Next action for the author
Ship the build: no further change is required. Optionally narrow the golden Method sheet's "other response forms" sentence to forms that fit the pre-2022 record.
