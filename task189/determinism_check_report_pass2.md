# determinism-check report, task189, 2026-11-01 (pass 2, rubric reship)

## Verdict
NOT_DETERMINISTIC, plus SOLUTION_WRONG (solution step 5 and critical component 3 wording).
**Disposition:** SEND_BACK
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (4 non-compliant: Cloonfad, Glasheen, Kilcrohane, Owenbeg) reproduces under every data-supported censored estimator (censored lognormal fit, Kaplan-Meier on the flipped sample, fitted lognormal mean). The new supplementary ask 2 (and the chart, ask 3, which carries the same 26 numbers) does not hold. The ortho-phosphate counts reach the golden only through rules no shipped file states:
- A bottle standing identically under two client points is counted "at the point of its newer booking". One such pair per water body; counting at the older booking or both moves all 13 rows by plus 1 sample and plus 1 below-limit (Aghavannagh 23/11, Owenbeg 47/24). The programme's 12-rounds-per-point sheet, if anything, favours the older booking.
- Result status V is excluded as withdrawn, but no file defines A, P or V (regulation 7.5 speaks of "withdrawn" only in words), and both quarterly reports print V rows as "approved". Counting V changes Ballynure 46/22, Carrowbeg 28/11, Drominagh 35/23, Glasheen 35/11, Tirneevin Stream 29/11.
- Carrowbeg: the golden drops 12 Tirneevin ARWA-CB-41 bottles as operational ARW-2241's, but the programme names Tirneevin as ARW-1041's laboratory, the crosswalk maps ARWA-CB-41 to ARW-1041, and ARW-2241 is absent from the crosswalk. Keeping them gives 38/22. The "catchment plus last two digits" numbering rule is in no file.
- Same-point double bookings (one to three days apart, identical results) are inferable but unstated; not merging shifts 11 rows.
- Chart bar order is unpinned (ties at 34 and 23), minor.
Taxonomy: competing_defensible_answer on ask 2 (governing); secondary underspecified_objective on the MCPA estimator (clause 7.2 names none; a literal own-limit fill, which is how solution step 5 reads, gives 11).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MCPA FIELD samples, 13 water bodies | 427 | 427 (lims export, determinand MCPA, FIELD, status A v1) | yes |
| Below reporting limit | 276 | 276 (qualifier "<") | yes |
| Non-compliant, censored fit / KM / lognormal mean | 4 | 4 (same four) | yes |
| Half limit / own limit / drop / zero | 7 / 11 / 8 / 3 | 7 / 11 / (not restated) / 3 | yes (drop not rerun) |
| Smallest margin | at least 11 per cent | Owenbeg about 12 per cent (KM) | yes |
| Same-month sensitive-method fill | 4 | not rerun (needs unstated fallback for missing months) | no |
| Solution step 5 "held at its own limit" | 4 | 11 | no |
| Ask 2 ortho-phosphate 13 pairs | as listed | reproduced only under the author's four rules; each alternative moves at least one row, the cross-booking rule all 13 | conditional, fork open |
| Ask 3 bars | same numbers | same forks, order unpinned | conditional, fork open |

## Competing answers that survived
1. Cross-point identical bottle: newer booking (golden) vs older or both. Closing rule shipped: none.
2. Status V: withdrawn (golden) vs approved (quarterly reports). Closing rule: none defines the code.
3. ARWA-CB-41 Tirneevin bottles: operational ARW-2241 (golden, 22 for Carrowbeg minus) vs ARW-1041 (Carrowbeg 38/22). Closing rule: none in crosswalk or programme.
4. Same-point double booking: merge (golden) vs count both. Unstated.
5. MCPA estimator: data-supported fill (4) vs own-limit literal reading of step 5 (11). Closed only by the phrase "the results it holds support" in 7.2 and by the data.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, json) | yes |
| Large file | 25,000 rows | lims export 25,316 | yes |
| Distractors in metadata.json, none named in a file | 2 or more | 5 (flow, sales returns, two quarterly reports, abstraction register); file names carry no label | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | the quarterly reports list one quarter of ortho-phosphate and would reproduce a partial count; the export's full year rules them out | yes (see Findings 3) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | whole numbers stated; ask 2 is 26 cells | yes |
| Prompt shape and rubric 25 or more criteria | yes | 26 ask cells plus main call plausibly exceed 25; rubric not inspected | not verified |
| Reads as real, not LLM generated | yes | judge found no authoring disclosure | yes |
| Determinism of every graded figure | yes | ask 2 and 3 open | NO |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: censored-data estimator versus substituted constant, default path half limit giving 7, declared distractors none on the decision question, `declared_wrong_basis_distractor` null. Match. No distractor carries the call. The mismatch is not in the stump but in the asks: the design note's ask W lists the three ortho-phosphate reconstructions (re-booked bottle, double booking, Tirneevin code collision) as the intended silent devices; the judge reads each as an unfiled rule rather than a recoverable fact.

## Gate H reconciliation
Judge: domain pass, layers pass, decisive_step analytical. Design note: same (censoring-aware annual mean, easy route half-limit gives 7). Match. Rule 3 binds only the main call; the asks are free of it, but they still must be determinate.

## Stump power (Gate F)
Real: half-limit substitution is the common convention and files 7. Some solvers will reach a fitted fill because 7.2 distrusts a fitted distribution's mean, and the censored fit, Kaplan-Meier and sensitive-method fill are textbook routes a strong solver takes (stumping 1.3). The estimator is not literally filed; the data separates the candidates (Tirneevin quantifies at 0.005, so the bounded Kilgarron results sit far below 0.05).

## Findings, ranked
1. Ask 2 and ask 3 not determinate (competing_defensible_answer): four unfiled conventions, rows move under each.
2. Solution step 5 and critical component 3 say "held at its own limit"; literally that is 11. Reword to a fill below its own limit.
3. The same-month sensitive-method estimate depends on an unstated fallback where no Tirneevin result exists for the month; remove it from critical component 3 or specify.
4. Quarterly reports print V rows as "approved", contradicting the golden's exclusion unless a shipped legend defines V.
5. Chart bar order unpinned.

## Next action for the author
Rework the ortho-phosphate asks in the generator: either ship a LIMS export legend (A, P, V) and a crosswalk or programme note that resolves the cross-booked bottles and the ARW-2122 / ARW-2241 codes, or drop those devices from the pack and ask so that each of the 26 cells has one literal answer; then reword step 5 and critical component 3, pin the bar order, rebuild and re-judge.
