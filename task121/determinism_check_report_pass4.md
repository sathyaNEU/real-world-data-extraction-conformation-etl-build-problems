# determinism-check report, task121, 2026-11-01 (pass 4, reship after the leak-gate repair)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG on a graded figure)
**Disposition:** FIX_NOW (solution blocks only: wording, no pack change, no model rerun)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scratch: /tmp/determinism-check-task121-r4/ (verdict.md from one isolated thread). Pack md5 0d39c59f3c649ddbc68494806a3e72b0, 12 files, no data_dictionary.csv, no file index, qa_program_measures_2025.pdf present.

## Why
From March the rise sits wholly on shifts begun after an 8-hour turnaround (31.1% against 10.7% on rested shifts; rested shifts 10.2% before March). Release 13.3, the graduates and the mix each fail the filed counterfactual test (QA 1.1). Every graded figure recomputed from the bundle and reproduced to the filed rounding, including all 36 monthly ask figures. The removal of the dictionary and index opens no fork that the data and the surviving QA text do not close, subject to the rulings below (one residual, TG05).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Under-triage Sep-Feb / Mar-Aug | 10.5 / 14.8 | 1110/10620 = 10.45; 1471/9966 = 14.76 | yes |
| Quick-return shifts Sep-Feb / Mar-Aug | 1.5 / 15.8 | 66/4543; 803/5080 | yes |
| Rate on quick-return / rested shifts from March | 31.1 / 10.7 | 618/1989; 853/7977 | yes |
| Rested shifts before March | 10.2 | 1063/10449 | yes |
| Veterans before / from March | 10.4 / 14.5 | 10.37 / 14.49 | yes |
| Earlier protocol mix, Mar-Aug | 14.7 | 14.73 (protocol grain) | yes (but see Findings 1: "call mix") |
| Ask A, 12 p90 values | 121 ... 130 | identical | yes |
| Ask B, 12 medians | 112 ... 112 | identical | yes |
| Ask C, 12 shares | 92.5 ... 92.7 | identical (Sep 92.496) | yes |
| Chart series (monthly rate) | 9.6 ... 13.0 | 9.6, 10.0, 10.2, 11.3, 10.7, 10.7, 16.0, 15.1, 15.2, 14.1, 14.8, 13.0 | yes |

## Competing answers that survived
Rulings on the five conventions the thread lists as undefined after the dictionary was removed. C1 = one reading the shipped files support. Device = the ask's designed silent device in the design note's Ask sheet (the reship brief bars filing these in a document).

1. **unit_assigned as the final unit's time. C1; designed hazard, not the primary.** Alternative p90 series 142 ... 156 (33 to 52 s over). QA 3.1 files "the first ambulance being assigned"; cad_unit_history holds earlier assignment rows for diverted or cancelled units (3,794), and cad_medical_calls.unit_assigned equals the assigned time of only the row for the CAD's own (final) unit. "First" read literally is the minimum over the unit history. The Ask sheet lists this as a hazard ("the CAD's unit_assigned holds the ambulance now on the incident"), not as the primary. Not a genuine second figure; no closure needed.
2. **A repeated che_call_id as one call. C1 and the Ask A primary device (D6).** Alternative 128, 127, 127 ... 137 (5 to 8 s over). 1,548 pairs of incidents (69,080 rows, 67,532 calls; the thread's "60 pairs" was a slip) share a che_call_id, answer second and call-taker; each che_call_id appears once in the call detail; QA 3.1/3.2 count calls, and QA 6.1 says answering is as the equipment records it. Barred from filing; the Ask sheet states it rests on QA 3.2 and the key alone.
3. **Position-pass records. C1 and the Ask C primary device (D1).** Alternative adds 0.4 to 0.7 points (9 of 12 monthly figures change at one decimal). The data signature is clean: 12,258 records arrive in the same second an earlier same-trunk, same-number record was released, with no gaps of 1 to 5 s (the next gap is 6 s), and each is answered within seconds. QA 4.2 counts "calls" and the equipment logs an offer, not a call. Barred from filing. Weakest of the asks but a device by design.
4. **QA7's minutes and seconds keyed without the colon. C1 and the Ask B primary device (D3).** Alternative months 2 to 19 s over. Evidence: no QA7 value ends in 60 to 99 (other reviewers' do one time in six); the calibration pairs (QA 5.2 names calibration) differ by 0.9 s on average when QA7 is read as mmss against 73 s as stored. Barred from filing.
5. **TG05 as a 911 group. Not a device; leans C1 but a genuine second figure with a small footprint.** centre_reference.xlsx describes TG05 as "911 calls transferred from the Sheriff's Office", TG07 as the "10-digit emergency line". The design note's Ask C hazard is TG07 only and TG05 appears nowhere in the note, so it is not a designed device. I recomputed with TG05 left out: Nov 92.1 (golden 92.2), Dec 90.1 (90.2), Mar 92.3 (92.2), Jul 91.9 (92.0); 4 of 12 months move by 0.1, 8 do not. Support for the golden: the only 911 / 10-digit distinction in the pack is that sheet, TG05's description opens "911 calls", it carries wireline, wireless and residential classes as the 911 groups do, and QA 4 counts calls "arriving at the centre". Support for the alternative: the word "transferred" (a call already answered elsewhere). Nothing in the pack says transferred calls are not 911 calls. A literal reader includes it, so I rule it C1 by the sheet's own label, with residual risk that a reviewer treats it as an open fork.
   - **Smallest WHAT closure, only if the author wants zero residual:** one population clause in QA 4.2 (not a method): "911 calls are the calls arriving on the trunk groups the centre reference describes as 911 lines, including those transferred from the Sheriff's Office." Prefer no change; the reference sheet already carries this.

Other non-graded forks: pooled against mean-of-months for the two six-month rates (QA 2.2 ratio of counts, closes it); "call mix" at determinant grain gives 10.3 (see Findings 1).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | che 148,589 rows (cad, history, epcr also large) | yes |
| Distractors | 2 or more named in metadata.json, none labelled in a file name | protocol_case_reviews and ems_unit_hours named; file names carry no label | yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | both flat across March (thread and design note agree); neither reproduces a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 asks of 12 months; prompt gives per cent to one decimal, whole seconds | yes |
| Prompt | one paragraph, question first, under 1,000 chars, no count the data hold | 699 chars | yes |
| Rubric 25 or more criteria | reached by prompt shape | 2 rates + cause + 36 monthly figures + chart | yes |
| Reads as LLM generated / golden realism | no | thread found no authoring language in PDFs or xlsx; golden realism not re-judged here | yes (no finding) |

## Gate G reconciliation
Thread: mechanism decomposition_attribution; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical (rest since the previous shift, built from consecutive roster rows, joined through call_takers, then stratified).

Card (task121.json) and the design note: stump_class analytical; layer 2 family estimand_identification, "a rise attributed by an exposure that varies inside the period"; domain test and analyst test name the same decisive step (rest before the shift, quick returns under 11 hours) and the same easy route (release 13.3 coincident on 3 March). The two descriptions agree: the thread's "decomposition_attribution" and the note's "estimand_identification" are different labels for the same attribution-by-varying-exposure step, and neither is a planted defect, decoy, semantic reading or rule execution. The declared distractors (case reviews, unit hours) are not named by the thread as the surface read; the surface read is release 13.3, a real coincident change that the design intends as the trap and not a declared distractor. No mismatch. The thread did not class the step analytical merely because it is a textbook method; it reached the call by stratification the data had to support, so the Gate F note on landability stands as the design note's ladder argues it (a strong solver who builds the shift-level variable lands it; one who does not names 13.3).

## Stump power (Gate F)
Release 13.3 is perfectly collinear with time at call level, so any pre/post or version comparison names it; graduates and mix splits do not rescue it. Only per-call-taker rest built from the roster separates the cause. Likely partial credit on the asks because the three ride unstated data conventions (devices 2 to 4, hazard 1). Judge concurs with the design note's expectation; no portal evidence at this pass.

## Findings, ranked
1. **FIX_NOW (wording).** The Final Recommendation and Step 3 say "the call mix" for the 14.7 figure. Standardised at determinant grain the "call mix" gives 10.3, a different number and a different reading; at protocol grain it is 14.7. Change both to "the protocol mix" (the filed grain).
2. **FIX_NOW (wording).** "the rotation worked from 2 March 2026" (recommendation, step 7, the xlsx cause line) rests on a date no shipped file states; the first quick-return shift starts 4 March. Soften to "the rotation worked from early March 2026" or drop the date. The 11-hour line is not threshold-sensitive (rests are only 8 h or 16 h and longer).
3. Optional: Steps 4 to 6 may say the split-incident rule, the passed-position rule and QA7's encoding are read from the data; this does not file the HOW in any shipped document.
4. Residual: TG05 (ruling 5). No pack change recommended.
5. Hygiene PASS: no README or authoring language; dates coherent (decision 10 Dec 2026, data to Aug 2026).

## Next action for the author
Edit submission.md only: "call mix" to "protocol mix" in the Final Recommendation and Step 3, and soften "2 March" in the recommendation, step 7 and Deliverable Answers item 1. No pack, prompt, model or target.zip change; no re-judge needed beyond this pass since the figures are untouched.
