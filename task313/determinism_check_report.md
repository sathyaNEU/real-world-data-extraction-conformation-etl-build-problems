# determinism-check report, task313, 2026-11-04

## Verdict
DETERMINISTIC (no SOLUTION_WRONG; one graded cell of ask 3 sits on an exact rounding tie)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: other (estimand, the at-risk window the service can still reach), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet/medium judge, fresh unzip at /tmp/determinism-check-task313-1793795716/target/, verdict at /tmp/determinism-check-task313-1793795716/verdict.md. target.zip sha256 e0d62b0d...a600493.

## Why
Every committed figure recomputed from the shipped files. The main call (posts 9/7/6/3/5 for Kellingworth, Ravensby, Sedgefold, St Aldric's, Wennby; about 325 avoided) turns on the readmissions each unit has after the community office receives the discharge notification, with the trial's 0.43 held after the first call. The easy route (57 per cent on all 646 eligible readmissions) gives 8/8/5/4/5 and 375. The thread found the reachable reading forced by the spec's referral route (s4) and the notification file, and not an open fork. Two issues remain: ask 3 Weight loss usual-care is exactly 12/192 = 6.25 per cent, golden prints 6.2 (half-up gives 6.3), and the short-attempt rule behind ask 4 has no filed threshold (the data separate it).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible babies (5 units) | 2,803 / 2,419 / 1,908 / 1,514 / 1,639 | same | yes |
| Eligible readmissions | (180, 168, 111, 86, 101 in note) | 180/168/111/86/101 = 646 | yes |
| Reachable readmissions | 132/166/109/62/91 | 132/166/109/62/91 = 560 | yes |
| Trial RR | 0.43, 57 per cent | 56/2092 vs 134/2134 = 0.426 | yes (needs mother-filed mapping) |
| Total avoided | 325 | 319 (321.6 at 0.426), nearest 25 = 325 | yes |
| Posts | 9/7/6/3/5 | same by largest remainders | yes |
| Easy route | 8/8/5/4/5, 375 | 368 -> 375, 8/8/5/4/5 | yes |
| Ask 3 rates and RRs | 8.5/0.35, 6.1/0.64, 6.6/0.40, 6.2/0.29, 7.9/0.49, 5.7/0.65 | same, but WTL rate = 6.25 exactly | yes except WTL rounding tie |
| Ask 4 visits and calls | 1.80/2.93 ... 1.33/2.59 | 1.797/2.930, 1.238/2.810, 1.197/2.602, 1.530/3.018, 1.475/2.536, 1.333/2.593 | yes |

## Competing answers that survived
- Ask 3 Weight loss usual-care rate: 6.2 (golden) against 6.3 (round half up) on the exact 12/192 tie. The prompt says "one decimal" and files no tie convention. Open fork, one cell.
- Ask 4 short-attempt threshold: not filed as a number. The thread found the data separate it cleanly (pre-2025 HV 2 to 12 minutes against 26 or more, TEL 1 minute against 4 or more) and the code list dates NA/TNA, so it did not call it open. Keeping short attempts gives 1.83/3.05, so the fork is real if a solver does not drop them.
- Main call: none survived.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | notifications csv 60,840 rows (card) | yes |
| Distractors | 2 or more in metadata.json, none named by file | lmns_maternity_dashboard_2025-26.xlsx, community_midwifery_establishment_2026-10.csv; names do not label them | yes |
| Distractors unused and weighty | yes | note: used by no rung, relevant to staffing; they answer no graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg) | yes |
| Asks multi-dimensional with unit and rounding | yes | ask 3 and 4 are 6 reasons by 2 measures; every ask states unit and rounding in the prompt | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 05, allocation to a fixed total; 5 unit posts, total, 24 trial figures, chart (about 31 gradable); the rubric is generated, so not counted directly | yes (by count) |
| Reads as real, not LLM generated | yes | thread saw none; prompt is 900 characters, one paragraph; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: mechanism other (reachable-window estimand), analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Design note and card: strategy causal_design / estimand_identification; stump_class analytical; the decisive step is each baby's readmission set against its own receipt instant. The two match.
The declared distractors (LMNS dashboard, establishment file) are not named by the thread as a surface read, and the note says no rung reads them. The surface read the thread names is the trial's 57 per cent on all eligible readmissions, which is a ladder rung and not a shipped wrong ranking.
Gate G line: PASS. No shipped artifact ranks the units wrongly; the easy answer comes from the candidate's own application of the report's ratio. The thread's wording that the report headline is "genuinely correct" and the reachable window "lives in a separate system" agrees with the note's "nothing is planted".

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Note: decisive step is the per-baby comparison of the admission instant in the ICB extract with the receipt instant in the office's UTC log, before the trial ratio is applied; the analyst test says a strong analyst files 8/8/5/4/5 and 375.
Gate H line: domain pass / layers pass / decisive_step analytical. Matches the card and note, with one caution in Findings (finding 2).

## Stump power (Gate F)
Thread: good. The strong analyst who cleans every key and applies 57 per cent to all eligible readmissions files Ravensby 8, Kellingworth 8 and 375; the reachable limit lives in a separate log. The thread did not class the step analytical merely because the method is standard. It did say a solver who notices the notification file and the s4 referral route lands the call. For the main thread's weighing: the route is "join two logs and cut at the receipt", which is a landable call once the notification file is opened. The note's own survivor anatomy rates it hidden because no column holds a delay.

## Findings, ranked
1. **Ask 3 WTL usual-care rate sits on 12/192 = 6.25 exactly.** Golden 6.2, half-up 6.3. Fix in the generator (nudge a trial row so the cell leaves the tie, or file the rounding convention), regenerate the golden, rerun the affected ask.
2. **Defect 3, the optional filed sentence ("avoidable readmissions are those after the service can first reach the family").** Read against determinism-check section 1 and CLAUDE.md "file the WHAT, never the HOW": the sentence is nominally a window, but the window is the decisive step. The note's own Three rules line says "no filed rule ties the service's start to the receipt" and rests "Not rule application" on that. Filing it would hand over the content of the stump, so executing the spec word for word would file 325, and the main call becomes rule application, which the client bans as a decisive step. It also moves the stump from HOW (which readmissions the service reaches) into the WHAT, contradicting the skill's "stump lives in HOW, never in WHAT" only if the window truly is HOW here; the safer reading is that it collapses the analyst test. The thread did not treat the reading as an open fork: it called it forced by the shipped spec s4 and the notification file, "not stated word for word", a mild Gate C soft spot, and offered the sentence as optional only. Recommendation: do not add it. The main-thread decision is whether a mild Gate C is accepted as closed by s4 and the note's fork table (a literal reader still has to decide which readmissions the service is expected to avoid, per the note's own Literal reader section, so the judge's own finding is that the data force it).
3. **Short-attempt rule for ask 4 has no filed threshold.** Thread suggests a WHAT sentence (an attempt shorter than the service's minimum is not a contact). That is ask-side, where rule application is allowed; the data separate it. Cheap to add, low risk.
4. **Builder-flagged points the verdict addresses or leaves untouched:**
   - Separate effect per risk reason (total 285.7 to 320.6, SF15): NOT addressed. The verdict says only that one pooled effect carries in the main call, and never tests per-reason effects or the report's interaction statements. Untouched; pass 2 should compute it and check that the trial report's no-interaction wording rules it out in words.
   - Calling-hours convention: ADDRESSED. Data-supported (first calls follow same day for receipts 08:00 to 18:59, about 94 per cent, never from 19:00), and the same posts come out with receipt time used directly, so it is not load-bearing.
   - Effect starting at first home visit (7, 10, 6, 2, 5; about 200): NOT addressed. Not tested by the thread. Untouched; pass 2 should check the trial's day-one ratio rules it out.
   - Mother-filed postnatal-ward readmissions mapped to baby: PARTLY addressed. The thread found the mapping reproduces 0.43 (without it, the report's 46/108), calls it Layer 1 mess the pack supports through the MOTHER NHS number, but does not say whether it is forced by the prompt text. Pass 2 should say whether an unmapped solver files a different ask 3/4 answer under the prompt's "babies it analysed" (the note says it moves Ask A and Ask B only).
   - Ask B's code-change device: ADDRESSED. Found data-separated and the NA code lists but has no NA rows; the filed-sentence suggestion is finding 3. The thread also found 290 duplicate contact_id rows deduped by id.
5. Minor temporal note from the thread: spec issued 21 September 2026 sets a basis year ending 30 September 2026 and extracts run to 31 October 2026; harmless.

## Next action for the author
Fix the ask 3 Weight loss tie in the generator (move the cell off 12/192 or file the half-up convention), rebuild twice for byte identity, and add the one ask-side sentence on short attempts if desired. Do not file the reachable-window sentence; re-judge once only if the main call or the prompt text changes.
