# determinism-check report, task268, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (two optional in-house pins on the asks, none touches the main call)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (general-purpose, sonnet, medium) saw only the fresh unzip and the inlined blocks. The plan (stock_recovery_plan_2026.pdf 4.1 and 4.2) files the estimand: the ground whose haddock stock, the weight of haddock on its Annex A stock area, fell furthest below its 2019 to 2021 average. The survey manual section 2 (twelve stations per depth band whatever its area) and Annex A give the band areas, so area-weighted band means are the stock. Halmorie Deep 62.8 (63) against Brettach Bank 52.0 (52), gap 10.83 (11 either rounding path). The easy routes miss: plain tow mean gives Brettach 51.6 vs Halmorie 43.6; commercial catch per hour gives Brettach 46.6 vs Halmorie -10.0. All committed figures reproduced. No surviving rival on the main call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Falls SKB / HMD / MRG / BRB / VKH / CLP (survey_tows + ground_grid_annex_a) | 34 / 63 / 32 / 52 / 23 / 5 | 34.0 / 62.8 / 32.0 / 52.0 / 22.8 / 5.0 | yes |
| Gap HMD over BRB | 11 points | 10.83 | yes |
| Tow placement (shot lat/lon to cell) | n/a | 1,727 of 1,727 placed, ground and band agree | yes |
| Ground areas vs plan table | n/a | 3,833 / 6,644 / 3,773 / 4,991 / 3,534 / 4,229 | yes |
| Eastquay t / £ (sales_notes, member_vessels, conversion_factors) | 1,257; 2,512,050 | same | yes |
| Kelmoor | 1,833; 3,582,185 | same | yes |
| Tolsetter | 1,213; 2,387,574 | same | yes |
| Haldness | 1,550; 3,059,583 | same | yes |
| Quota left N / E / T / S / I (quota_ledger) | 1,503 / 1,079 / 670 / 713 / 250 | same | yes |

## Competing answers that survived
- Main call: none. Brettach wins only under the plain average or the commercial catch rate, neither of which is the weight on the stock area.
- Fork 1 (ask 1, whole-percent falls): an estimator that fills unsampled cells by band mean from sampled cell means gives HMD 64, BRB 52, SKB 37, MRG 34, VKH 21, CLP 12. Call and an 12-point gap survive but four falls differ. The prompt and plan name no estimator; the stratified-by-band mean is the design-consistent reading. This is the one graded-figure fork.
- Fork 2 (ask 2, value at first sale): the shipped files do not define a re-issued note. Keeping the later note (golden) gives the filed figures; keeping the original moves values by under £400 per port (Eastquay £2,512,143, Haldness £3,059,356, Kelmoor £3,582,292, Tolsetter £2,387,482); not de-duplicating adds about £34k. Tonnes unaffected. "In place of the note it corrects" appears only in the solution steps.
- Landing port is the note's port field (78 notes land away from the registered port); the posted-date quota reading (1,253 / 277 / 1,672 / 757 / 831) is ruled out by quota rules 2.5 and 3.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 (pack_contents.txt included) | yes |
| Formats | 3 or more | pdf, csv, xlsx, txt | yes |
| Large file | 25,000 rows or more | sales_notes 32,295; elogbook 32,246 | yes |
| Distractors in metadata.json, none labelled by file name | 2 or more | sea_temperature_rectangles_2019_2026.csv, gear_trial_note_2025.pdf; names carry no label | yes |
| Distractor unused yet weighable; one answering a graded quantity reproduces and is ruled out by a shipped fact | yes | the two declared files are unused and weighable; neither answers a graded quantity. The e-logbook and tow sheets are the wrong-basis read (not declared, see findings) | yes, with note |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | falls by 6 grounds, port tonnes plus value by 4 ports, quota by 5 pools; units and rounding in the prompt | yes |
| Prompt shape and 25 or more criteria | identifiable | shape 01 (ranked list under a cap); 6 + 8 + 5 graded figures plus call components support 25; the rubric itself is not in the folder, not verified here | yes (rubric count not seen) |
| Reads human, goldens real work products | yes | judge found organisation-style records, no authoring disclosures; golden realism not re-judged here | yes |

## Gate G reconciliation
Design note: Gate G `method_or_model_selection`, strategy `population_selection`, decisive G12 (abandoned cells absent from logbooks). Thread: mechanism statistical_rigor (design-based stratified estimation), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. These match. The thread names the plain survey mean and the logbook catch rate as the surface reads; neither is the declared distractor (sea temperature, gear trial), so the declared distractors are not load-bearing. Gate G: no shipped artifact ranks the candidates; the logbook route is only available by computation from raw records, which is the Layer-1 data the note says is off the decisive path. The thread flagged that a reader could call rejection of CPUE a rejection of a misleading read, and concluded it is a population choice, not the stump.
Gate H: domain pass, layers pass, decisive_step analytical. Design note `## Three rules` and card agree: Layer 2 is area-weighted stratified estimation from a probability sample against preferentially sampled logbooks; Layer 1 is the PLN change, re-issued notes, UTC, keyed paper sheets, effective against posted dates. Easy route lands Brettach (52 vs 44 survey mean; 47 catch rate). No mismatch.

## Stump power (Gate F)
Judge reading: strong on paper; both natural routes (plain survey mean, members' catch per hour) put Brettach first, and a clean-data analyst still files Brettach unless the strata are area-weighted. The coordinator reports the separate stage-4 leak reader landed the call (score_reader exit 1, Gate F failed). That is a leak-reader result outside this thread; I have not seen its evidence, and it does not change this determinism verdict. If the reader reached Halmorie Deep, the likely route is the manual's own twelve-per-band design cue, which the judge also noted ("the manual's equal-per-band design signals it"); this bears on Gate F, not on determinism.

## Findings, ranked
1. Fork 1: whole-percent falls for four grounds are estimator-sensitive (SKB 34 vs 37, MRG 32 vs 34, CLP 5 vs 12, VKH 23 vs 21). The plan files the WHAT (weight on the stock area) and the survey design points to band stratification, but no text names the band-weighted survey mean. Main call and gap unaffected. Optional pin: name the stock's population (survey tows, each depth band weighted by its stock area) in the plan, filing the WHAT not the method.
2. Fork 2: re-issued-note replacement is defined only in the solution steps. Pound-level effect only. Optional pin: one line in sales note or prompt. Sits on ask 2, where rule application is allowed.
3. Distractor declaration: metadata.json names two distractors that are unused and non-answering; the files that actually carry the wrong-basis read (e-logbook, tow sheets) are not declared. This passes the input gate but the author may wish to confirm that is intended.
4. Rubric criterion count was not available to check.

## Next action for the author
Optionally add the one-line filings for findings 1 and 2 in the plan text or the sales-note documentation (population and replacement, not method), rebuild, and ship; otherwise ship as is. The leak reader's Gate F failure is handled in the main session.
