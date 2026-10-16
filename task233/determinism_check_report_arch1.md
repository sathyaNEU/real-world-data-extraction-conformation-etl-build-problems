# determinism-check report, task233, 2026-10-16 (run r1, stage 4)

## Verdict
NOT_DETERMINISTIC (Gates C/E, taxonomy: underspecified_objective). Every golden number reproduces; the form of the follow-up departure is not forced, and a second fork sits on the suppressed cells.
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
QS-4 section 3 says each nonrespondent's allocation is moved "as the most recent nonresponse follow-up found ... destinations departing from their allocations". It does not file the scale of the departure (points, ratio, odds ratio; pooled or by band). The golden's pooled odds ratio (2.59 NEET, 0.45 HE) gives 4 suppressed, 5 standard and 15 caution. The judge found band-stratified gap and band-stratified ratio models that fit the follow-up within 1 to 4 log-likelihood units and that flip flags on the main call. Pooled gap and pooled ratio are refuted by the data, but the stratified ones are not. The prompt's "the rate the release will publish" is also open for the four suppressed NEET statistics, because QS-4 section 4 says a suppressed statistic shows the suppression mark.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Comparable follow-up cases (outcomes + crosswalk + 2025 final) | 2,438 | 2,438 (2,913 drawn, 2,815 resolved) | yes |
| Odds ratio NEET / HE | 2.59 / 0.45 | 2.590 / 0.450 (offset logit) | yes |
| Nonrespondents on 2026 frame | 8,297 of 47,734 | same | yes |
| Pooled NEET points gap | 17.3 | 17.3 (41.2 vs 23.9) | yes |
| 24 district published rates | per Deliverable Answers | all 24 match | yes |
| Band table (points from state_exam_points_2026.csv) | 11,331 / 14,483 / 12,699 / 9,221 and rates | match to one decimal | yes |
| Shifts, 0.50 to 4.56 points, flags 4 / 5 / 15 | as claimed | match | yes |
| "Bands refute a ratio" | refuted | true for the pooled ratio only; band ratio and band gap survive | no |

## Competing answers that survived
1. Departure form. Band-stratified gap: ED10 and ED11 NEET suppressed, ED06 to ED08 NEET caution, no standard HE flags. Band-stratified ratio: ED04 NEET suppressed, ED09 NEET standard, ED06, ED08, ED09, ED10 HE suppressed. Golden: pooled odds ratio. Nothing shipped closes it. The follow-up also covers only 5 of 12 districts, so carrying one ratio to the other 7 rests on the same unfiled choice.
2. Suppressed cells. The golden lists the computed rate (27.9, 23.2, 16.8, 31.4) beside "suppressed". A literal reader writes the suppression mark.
3. Online build 7.3.2 code order. The golden infers the 2025 7-code order; activity_codes.csv lists only the 8-code list. Published-rate cells move (ED01 HE 27.7 vs 27.0, ED12 HE 13.8 vs 12.5), flags do not. The data favour the golden, so this is minor.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, md) | yes |
| Large file | 25,000 rows or more | frame 47,734; 2025 final 46,493 | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | 3 named in metadata (lfs_youth_neet_by_region_2025.csv, destinations_release_2025_tables.xlsx, careers_service_contacts_2026.csv); no file name labels one | yes |
| Distractors weigh but do not answer a graded quantity | | judge found them unused; I did not re-test them for weight | not verified |
| Deliverables | 1 to 3, all in golden | 1, present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 flag+rate cells and a 4-band table, per cent to one decimal | yes |
| Prompt shape, rubric | shape identifiable, 25 or more criteria | shape 07 (grid of cells); no rubric in the folder | shape yes, count not verified |
| Reads as real work product | | judge saw nothing LLM-generated; I did not audit the golden for realism | not verified |
| Prompt | one paragraph, under 1,000 characters | 537 characters | yes |

## Gate G reconciliation
Thread: method_or_model_selection / analytical_non_defect / surface_read_dependency no / sole_data_defect no. The design note and the card (stump_class analytical) agree: the stump is carrying the departure as a points gap rather than on the odds scale. No distractor is the surface read carrying the task. There is no mismatch on the family. The mismatch is in forcing: the design note's literal-reader claim ("every model that fits those cases gives the golden grid") holds for pooled models, not for the band-stratified candidates, and the fork table has no row for the departure form or for the suppressed-cell display.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis is a nonresponse sensitivity (delta adjustment) calibrated on a follow-up. The easy route is the pooled 17.3-point NEET gap (minus 10.7 HE), which gives nine wrong flags. This matches the card's analyst_test and domain_test.

## Stump power (Gate F)
Moderate. The pooled points gap is a natural wrong route, but the stump is partly contested because a band-stratified fit is also defensible.

## Findings, ranked
1. Departure form not forced; band-stratified gap and ratio survive (main call, Gates C/E).
2. Suppressed statistic: the prompt does not say rate or mark (supplementary ask 1).
3. Build 7.3.2 code order is inferred (supplementary ask 1, published-rate cells only).
4. Design note claim that the bands refute a ratio overstates; it holds only for the pooled ratio.
5. Spec items not verified: distractor weight, rubric count, golden realism.

## Next action for the author
Run /fix-determinism-style closure: file the WHAT so that only the odds-scale departure fits the follow-up. For example, give follow-up structure in which band-level gap and ratio are clearly rejected, with a data-clear reason to carry one departure to the 7 unfollowed districts. Do not file the HOW as a recipe. Also state in the prompt whether a suppressed statistic shows the computed rate or the suppression mark. Add fork-table rows for both, then rebuild and re-judge once.
