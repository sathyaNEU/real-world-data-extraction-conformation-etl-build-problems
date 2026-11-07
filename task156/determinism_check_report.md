# determinism-check report, task156, round 2, 2026-11-07

## Verdict
DETERMINISTIC. No SOLUTION_WRONG.
**Disposition:** FIX_NOW, on the solution's wording only (SOLUTION_STEPS step 8). No prompt or input change, no model rerun.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
- The main call is forced. The re-judge rebuilt the member-level logit and got the same 11 councils at or above half; the nearest council below the line is Rosedene at 0.455 and the nearest above is Copeland Downs at 0.574, about 6 points either side with nothing between.
- Every round-1 finding is closed: dues and hours reproduce for all 24 round councils (and the other six for dues), the Sunday period-end basis and the one-row-per-organiser-invitation-day unit now resolve from the shipped files and the prompt, scope is the 24, and no value sits near a rounding edge.
- The one defect: SOLUTION_STEPS step 8 says "a moved booking keeps its earlier row", while the golden computation keeps the later row (the booking as held, which is also what the prompt's "a moved booking counting once as held" supports). Keeping the earliest row would change 16 of 24 council hours by 1 to 2. Reword the step only.
- Per section 6 of determinism-check this is a wording fix on the solution block, not a gate failure at G or H.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Apply set | 11 councils | same 11 (.574 to .717; other 13 at or below .455) | yes |
| Delegate log odds / effect | 1.05 / about 24 points | 1.053 / +24.2 points | yes |
| Back-test | within about 1 point | mean absolute error 0.58 (no-delegate model 0.68) | yes |
| Naive route | 15 councils | 15, eight councils classified differently | yes |
| Rolls | declared rolls | all 18 (2023-24) and 14 (2021) declared rolls exact | yes |
| Dues, 24 round councils (and 6 others) | listed | all match to the dollar; 26 periods each | yes |
| Hours, 24 councils | listed | all match under the golden rule; nearest rounding edge .458 | yes |
| Step 8 wording | "earlier row" | golden keeps the latest `last_updated_utc` | NO, wording only |

## Competing answers that survived
- None that move a graded figure. Residual minor forks, both closed by shipped material: Thursday dues dates (FP-04 "period ends on a Sunday... paid later that week", the 14-day cadence, and received dates; move-back is the only direction consistent with all three) and the moved-booking row (the prompt's "as held").
- Only two respecifications flip the call: dropping the council effects (back-test error rises to 5 points, a visibly worse model) and dropping the delegate mark (the intended trap). Skipping the online-to-ballot calibration leaves no council above half; the declarations separate it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 8 csv, 5 pdf, 3 xlsx | yes |
| Large file | 25,000 rows or more | online_vote_invitations 54,892; register extract 27,075 | yes |
| Distractors | 2 or more, in metadata.json, not in a file name | council_workforce_returns_2026.csv, member_survey_2024_results.xlsx | yes |
| Deliverables | 1 to 3, in golden | 2 (xlsx, docx) | yes |
| Asks unit and rounding | stated | whole dollars and whole hours stated; existence of the half line asked as a flag | yes |
| Prompt | one paragraph, under 1,000 characters, no data count | 900 characters, no count | yes |
| Rubric | 25 or more criteria | per the design note's shape arithmetic, 24 sides plus asks well over 25 | yes |
| Reads as real work product | no LLM tell | alphabetical council names read synthetic but tolerable; creator names and PDF producer below | yes, with hygiene notes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H: domain pass, layers pass, decisive_step analytical. Design note and card: stump_class analytical, decisive step conditioning each member's turnout on the delegate in post at the ballot, easy route 15, golden 11; Layer 1 items (July 2024 recode, term-dated register, duplicate and Thursday remittances, bureau splits, moved bookings) agree. No mismatch. The surface read is the vote-history route, not either declared distractor. The thread named (as an alternative easy route) the last declared turnout, which yields a different set; the design note's ladder rung 0 sits on 15, a minor difference in how the thread stated it, not a mismatch.

## Stump power (Gate F)
Moderate to high. A member-level model without the delegate mark back-tests within 0.7 points and files 15; the last declared turnout or a missing ballot-level shift also fails. The decisive step needs the date-aware delegate marks joined from the register, so it is analytical judgment the data must settle, not a textbook route landed with no judgment. Weigh against the design note's ladder; the portal measures it.

## Findings, ranked
1. FIX_NOW, SOLUTION_STEPS step 8: change "(a moved booking keeps its earlier row)" to state the later row is kept (the booking as held). Wording only in `submission.md` (and the generator source that writes it); graded figures are unchanged.
2. Hygiene, optional: scrub the xlsx core properties (creator and lastModifiedBy name Samantha Taylor and Eric Goodwin, the design's drawn personas; the thread flags them, and a pack-level author name is harmless in-world but easy to remove).
3. Hygiene, optional: the 2021 declarations PDF carries a 2021 CreationDate with a LibreOffice 24.2 producer string (anachronism); set the producer or date consistently.
4. Not run: the cross-batch fingerprint (outside the thread's allow-list; `guard.py` covers it).

## Next action for the author
Reword step 8 in the generator's submission text to "keeps its later row", rebuild (two byte-identical builds), re-run `verify`, `figures_check.py` and `voice-check.py`; optionally scrub the xlsx creator fields and the 2021 PDF producer in the same rebuild. Because no graded figure or shipped clause moves, the approval is not voided and no third judge pass is needed, though a pack-changing hygiene scrub means rerunning `leak.py` and rebuilding the zip.

## Round 1 summary
Round 1 (2026-11-07) judged the earlier pack: the main call was forced and reproduced, Gate G analytical_non_defect, Gate H pass, with every failure confined to the supplementary asks (the Thursday dues dates, the diary collapse rule, 30 versus 24 council scope, and ask 1 turnout rounding). The thread wrote SEND_BACK, read against the gate table as an ask-layer FIX_NOW. The author then filed the Sunday basis, the unit and the 24-council scope in the pack and prompt, which is what round 2 judged.
