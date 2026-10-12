# determinism-check report, task181, 2026-10-11 (pass 3)

Method note: this orchestrator session had no `Agent` tool, so no separate judge thread was spawned. The same isolation rules were applied in the session itself. It read only `prompt.md`, `submission.md`, `metadata.json`, `target/` (fresh read, scratch work outside the folder) and the `golden/` deliverables. It did not open the design note, generator, verifier, `solver_rounds/` or any earlier report. Because of that, the design-note half of the Gate G reconciliation was not done (the invocation forbade opening it).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one residual risk, below)
**Stumping type:** mechanism: reporting delay that differs by notifying laboratory, so the count "as it will stand" has to be nowcast per route; stumping_family: estimand / unit of analysis (analytical); surface_read_dependency: the surface read (cases notified so far, Wagga Wagga 9) is now ruled out by PR-07 4.2's own text and is not shipped as a ranked artifact; sole_data_defect: none (delay structure is a realistic lab-speed difference, not a planted defect)

## Why
PR-07 4.2 now defines the count as the number of cases "as it will stand once all the notifications for those 14 days have been received". That closes the observed-so-far reading by stated text. Under the route-specific nowcast, Griffith leads by a wide margin (excess about 26 to 68 depending on history window, against about 8 for Wagga Wagga). The only way to get a different area is to pool one delay distribution across the whole unit, which the shipped line list itself shows is a mis-specified model.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cases, specimens 21 Sep to 4 Oct, Wagga Wagga / Griffith / Snowy Valleys | 9 / 7 / 7 | 9 / 7 / 7 (episodes per 3.3, area per 3.4, non-residents dropped) | Yes |
| Other areas (Cootamundra-Gundagai 2; Edward River, Leeton, Narrandera 1 each) | as stated | same | Yes |
| Expected count (4.3, 2021 to 2025 same 14 dates) | 1.4 for all three | 1.4, 1.4, 1.4 | Yes |
| Griffith's 7 by lab | 6 Inland Pathology | 6 Inland, 1 hospital lab | Yes |
| Wagga Wagga and Snowy Valleys by lab | all hospital lab | 9 of 9 and 7 of 7 | Yes |
| Notified within 14 days of collection, Aug 2025 to Jul 2026 (Sydney dates) | Inland 76%, hospital lab 100% | 76.8% (rounds to 77%, reported as 76%; 63 of 82 is 76.8) and 100% | Yes within rounding (see Findings 2) |
| Quarterly confirmed / probable, all 10 areas | golden CSV | identical on all 10 rows | Yes |
| Infant cases per area (golden 2,1,1,1,0,0,1,1,1,1; total 9) | as stated | 9 infants, same area split (birth date from birth records, not line list) | Yes |
| Infants admitted / born to vaccinated mother | golden columns | Matched on 8 of 9 infants (Wagga Wagga, Edward River, Cootamundra-Gundagai, Snowy Valleys, Leeton, Junee, Narrandera, and the second Wagga Wagga infant); the Griffith infant's linkage (two babies fit on DOB, sex, postcode) was not resolved by this session's crude link | Mostly; Griffith row not independently confirmed |
| Clusters in Griffith (5.1) | Banna Avenue 5, Kooyoo Street 2 | 5 and 2 after name matching (Wollundry, 4 students, is a Wagga Wagga school) | Yes |

## Competing answers that survived
Test (a), the literal reading "cases on the extract so far". Under the new 4.2 it gives Wagga Wagga (excess 7.6 vs Griffith 5.6 and Snowy Valleys 5.6). It is no longer defensible: 4.2 now says the count is the number "once all the notifications ... have been received", the same quantity 4.3 counts for earlier years, and that a case belongs to its fortnight "whenever its notification is received". The 4.1 phrase "from the line-list extract" says what the area is decided from, not what is counted. The portal's fork is closed.

Test (b), a nowcast on one delay distribution pooled across the unit. This gives a different winner. Excess is Wagga Wagga 10.8, Griffith 8.0, Snowy Valleys 7.8. Across 24 variants it is Wagga Wagga every time. The variants were history windows of 24, 12, 9 and 7 months, available days a or a+1, and Sydney or UTC dates. Griffith leads under every route-stratified and every area-stratified variant (25.7 to 68.3), also in all 24 variants. This is a surviving fork only if the pooled model is defensible. I judge it is not: the shipped line list refutes it. Inland Pathology's median delay is 12 days and the hospital laboratory's is 2 (mean 12.5 vs 2.7), and `notifying_lab` is on every row. Pooled says 58% notified by day 3 and 70% by day 7. Griffith's own history says 5% and 7%. A pooled fit does not reproduce the area it is supposed to correct. This is the analytical step (choosing the right unit for the delay model), not a semantics or rule-application fork, so it is a valid stump. The residual risk: no shipped sentence forbids pooling, only the data does. A reviewer who runs the pooled version first may log it as a fork.

Other stratifications (per route, per area) agree on the winner. Magnitudes of Griffith's estimate vary (26 to 68), but the committed call and the slide do not ask for that figure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 11 | Yes |
| Formats | 3+ | 6 (csv, md, parquet, pdf, txt, xlsx) | Yes |
| Large file | 25,000+ rows | parquet 35,724; respiratory csv 29,036 | Yes |
| Distractors | 2+ declared, none labelled | influenza csv, week-35 weekly report; no label in names | Yes |
| Distractor looks relevant, unused | yes | same world; the weekly report ranks areas on a window ending 30 Aug, ruled out by its own stated dates | Yes |
| Deliverables | 1 to 3 | 2 (pptx, csv) | Yes |
| Deliverables present | all named | both in `golden/` | Yes |
| Multi-dimensional asks | yes | one area plus school clusters with counts; a 10 by 5 table | Yes |
| Unit and rounding | stated | counts only; the prompt names the measures, no rounding needed | Yes |
| Prompt | prose, under 1,000 characters | 850 characters, first person | Yes |
| Shape and 25-criteria floor | 25+ | shape 17; 50 table cells plus call plus clusters | Yes |
| Realism | no LLM tells | prompt, protocol and notes read plausibly; the pptx was not rendered or inspected in this pass | Not fully checked |

## Gate G reconciliation
Judge classification: mechanism is lab-specific reporting delay; family is estimand / unit of analysis; surface read is the observed count, now closed by 4.2's text. Comparison with the design note's claim was not made, because the invocation forbade opening the design note. The author or the main session should compare the card's `stump_class`, `analyst_test` and `domain_test` against this line.

Gate H: domain, rule 1 (really uses its domain): yes, reporting-delay nowcasting against a historical baseline is core outbreak surveillance. Rule 2 (two layers): yes. Layer 1 is the 90-day episode merge, split postcodes, UTC vs Sydney dates, DST, month-first dates and merged MRNs. Layer 2 is the nowcast by notifying route. Rule 3 (banned stump kinds): decisive step is analytical, with a residual that 4.2 now states the quantity, so the remaining choice is the delay model, which is analysis. decisive_step: nowcast each area's fortnight by its own laboratory routes' delay curves.

## Stump power (Gate F)
Too-easy signals: none found. The observed ranking (Wagga Wagga) is the wrong answer and is what a solver who skips the nowcast files. The pooled nowcast also lands on Wagga Wagga, so both lazy paths fail. Only a stratified nowcast reaches Griffith.

## Findings, ranked
1. Residual fork risk: a pooled-across-unit nowcast gives Wagga Wagga (10.8 vs 8.0). Nothing shipped says delay differs by laboratory except the data itself. If a send-back arrives on this, the cheapest fix is one neutral sentence in `pertussis_line_list_notes.md` saying the unit's two laboratories send notifications on different routes. That would leak the decisive step, so it is optional and not recommended on a pass.
2. Rounding: Inland Pathology's 14-day share computes to 76.8%, and the write-up states 76%. The claim truncates rather than rounds. Change `submission.md` Critical Components 4 and the Final Recommendation to 77%, or state "about three quarters".
3. Griffith's infant admission and vaccination cells were not independently confirmed here (see ledger).
4. The pptx was not inspected for realism in this pass.

## Next action for the author
Change the 76% figure in `submission.md` (Final Recommendation, Critical Component 4) to 77%, and then ship; no re-judge is needed for that edit.
