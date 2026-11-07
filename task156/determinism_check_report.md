# determinism-check report, task156, 2026-11-07

## Verdict
NOT_DETERMINISTIC (the judge's label; confined to asks 1 to 3 of the workbook). The main call is forced and reproduces. No SOLUTION_WRONG.
**Disposition:** FIX_NOW (the thread wrote SEND_BACK; I read it against the gate table, section 6, and do not agree it is a send-back; see Why).
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
- Main call: the 11-council list reproduces from the bundle, no council within 5 points of half (closest Rosedene about 45, Valmont about 57). Critical components 1 to 3 reproduce (delegate logit 1.053, 24.2 points; calibration shift 0.905, mean absolute error 0.7 points; naive route 15 councils).
- Gates H and G pass in the thread's reading and match the design note (below). The table sends back on G and H only. Every failure is a Gate C or E failure confined to supplementary asks 1 to 3, which are legally free of the call's rules. Per determinism-check section 6 ("A disposition is read against the gate table"), that is an ask-layer wording repair, not a re-root. I agree with the coordinator: FIX_NOW. Because the fix alters what solvers see and moves the graded set of values for asks 2 and 3 (if scope is cut), the one re-judge applies.
- Gate A, on the asks: all 30 dues values and all 30 hours values reproduce exactly under the golden's recipe, so the golden is right; the defect is that the recipe is not filed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Apply set (11 councils) | Ardeen, Copeland Downs, Corrigan Valley, Fairholme, Halston, Lindale, Northvale, Pellham, Stanwick, Valmont, Westhaven | same 11 (.570 to .715; other 13 below .46) | yes |
| Delegate log odds / lift | 1.05 / 24 points | 1.053 (SE 0.022) / 24.2 | yes |
| Back-test | within about 1 point | mean absolute error 0.7 | yes |
| Naive route set | 15 | 15, same eight movers | yes |
| Turnout whole percent (ask 1) | e.g. Ardeen 66, Halston 60, Valmont 58 | 65.3, 59.2, 57.2 (about 0.7 below on most rows) | sides yes; whole-percent values no |
| Dues, 30 councils (ask 2) | listed | all 30 match under the golden recipe | yes, but only with the unfiled Thursday shift |
| Hours, 30 councils (ask 3) | listed | all 30 match under the golden recipe | yes, but only with the unfiled collapse rule |
| Rolls | 32 declared rolls | `ceased` blank means employed reproduces all 32 | yes |

## Competing answers that survived
1. Dues, Thursday-dated platform runs: golden moves 12 councils' runs back four days to the Sunday; literal reading puts `period_end` 2026-07-02 outside 2025-26 and excludes 134,473 dollars (Ardeen, Ashby, Burnleigh, Darnley Plains, Denholm, Glenvale Hills, Halston, Northvale, Oakmere, Stanwick, Valmont, Westhaven; 4.8k to 24.8k each). No shipped file states the shift. (Gate C, also touches B.)
2. Hours, diary collapse rule: golden keeps the last update per organiser, invitation and day. Summing raw rows adds about 16 hours per council (up to 31); one row per invitation and day subtracts about 27 (12 to 43). No dictionary files it.
3. Scope of asks 2 and 3: written beside "every council in the round", which reads as 24; golden gives 30 (six "Outside the round"). A 24-row answer is graded as missing six.
4. Turnout rounding (ask 1): whole-percent values are not unique (about 0.7 points of calibration spread); prompt pins no rounding for turnout. Reach-half flags unaffected.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | online_vote_invitations 54,892 rows | yes |
| Distractors | 2 or more, named in metadata.json, not in a file name | council_workforce_returns_2026.csv, member_survey_2024_results.xlsx; neither named as a distractor in any file name; both carry no turnout or delegate figure | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both present | yes |
| Asks unit and rounding | each states unit and rounding | dues and hours state whole dollars and whole hours; turnout ask 1 states no rounding | NO (finding 4) |
| Asks multi-dimensional | not stacked lookups | per-council across years, files and sources | yes |
| Prompt | under 1,000 characters, one paragraph, no data count | 827 characters; no count. Adding "30 councils" would put a count the data hold in the prompt | yes (constrains the fix) |
| Rubric | 25 or more criteria | design note's shape arithmetic is well over 25 (set 1, sides 24, movers 8, components 2, asks 60, deliverables 2) | yes |
| Reads as real work product | golden realism | not re-judged here (leak reader and golden-realism cover it); judge found no toolchain leakage | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H: domain pass, layers pass, decisive_step analytical. Design note and card: stump_class analytical; mechanism population (pattern A, G14, G13, G4); decisive step is conditioning each member's turnout on the delegate in post at the ballot; easy route 15 councils, golden 11. These match. The thread names the vote-history route (ladder rungs 0 to 1'') as the surface read, not the declared distractors (survey, workforce returns), so the distractors are not too load-bearing. The thread recomputed the same 15-council easy route and the same eight movers. No mismatch.
Stump power note for the main thread: the thread rates it "moderate to good" and says strong models that fit the delegate term land the call. The design note's own ladder puts every cheap rung on 15, and the delegate term is a standard covariate in a field that estimates contact lift; weigh this against the ladder, since only the portal measures it. This is not a defect of determinism.

## Stump power (Gate F)
Moderate to good. A solver who stops at history or the last declared turnout files 15 and gets 8 calls wrong (6 false positives, 2 misses). Five round councils (Brackley Ranges, Fairholme, Kelvale, Quarrington, Westhaven) have no declaration, forcing a model. The decisive step is analytical, not a field-standard method with no judgment: the delegate effect has to be found in the register and joined. Asks 2 and 3 carry unfiled conventions, which will hold both top responses down on ask weight, but through ambiguity rather than analysis; fixing them makes the asks fairly hard rather than arbitrarily so (the careful-solver device is the cadence and the revisions, which stay discoverable).

## Findings, ranked
1. FIX_NOW, ask 2 (dues), Thursday dates: file the WHAT in the ask sentence or in a shipped platform note. Fix: "pay periods ending in 2025-26, each platform run dated to the Sunday on which its pay period ends", or add a payroll platform note (a line in an existing file, such as the bureau statements PDF or the guide) stating the Thursday date is the run date and the pay period ends the preceding Sunday. Re-assert in `checks.py`.
2. FIX_NOW, ask 3 (hours), diary collapse: file "one entry per organiser, invitation and day at its last update, travel and administration excluded" (population and unit, not the procedure), or ship an export note saying superseded revisions share the key. Re-assert the alternatives' differences in `checks.py`.
3. FIX_NOW, asks 2 and 3 scope (30 versus 24): decide one. Either cut the golden and submission to the 24 round councils, or word the ask to cover every council with dues or hours in the data, with no count in the prompt (the prompt bars counts the data hold). Cutting to 24 is the smaller change and matches the prompt's "every council in the round".
4. FIX_NOW, ask 1 turnout rounding: state "in whole per cent" in the asking sentence and move the golden to a value a reasonable refit reproduces, or grade the side only; the 0.7-point calibration spread flips the whole-percent figure on many rows. Pin the rounding or accept a tolerance in the rubric.
5. Minor, no action needed for determinism: Lindale delegate LIN-104 (member 128164) ceased 2026-08-19; 7 members ceased on the extract date; no call moves.
Do not touch the main call, the ladder, the apply list or the stump. Prompt length stays under 1,000 characters with no count; any fix that lengthens `prompt.txt` goes through `voice-check.py`.

## Next action for the author
In the generator, file the Sunday-period-end basis and the one-entry-per-organiser-invitation-day unit (in a shipped note or the ask sentence), settle asks 2 and 3 to the 24 round councils (or word an unnumbered every-council scope), pin ask 1's rounding; rebuild byte-identically, re-run `checks.py`, `figures_check.py`, `precut.py`, `voice-check.py` and `leak.py`, then re-judge once.
