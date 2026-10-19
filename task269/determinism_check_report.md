# determinism-check report, task269, 2026-10-19

## Verdict
DETERMINISTIC (no SOLUTION_WRONG on any figure)
**Disposition:** FIX_NOW (solution wording only: "7 Dec 2026" in ask 4 and step 6 appears in no shipped file; prompt says "the December allocation"; any December date gives identical counts). No figure moves, no rerun of the judge needed for correctness.
**Stumping type:** mechanism: method_or_model_selection (G-study to single-examiner D-study), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Policy 4.3 and the 2027 delivery plan (one examiner a station, three circuits, same stations everywhere) applied to a candidates x examiners-within-stations decomposition of the 2026 marks give R(n) = 1.010 / (1.010 + (1.704 + 0.960 + 1.033)/n): 0.793 at 14, 0.804 at 15, so 15 is the fewest stations meeting 0.80 within eighteen rooms. Every ask reproduced from the bundle. Source: judge thread verdict.md (one pass, sonnet, medium, isolated scratch unzip, md5 of target.zip cb57d759af9a79fab3e748a5874238c6).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Candidate variance | 1.010 | 1.0105 | yes |
| Station variance | 1.364 | 1.3640 | yes |
| Candidate x station | 1.704 | 1.7043 | yes |
| Examiner within station | 0.960 | 0.9605 | yes |
| Residual | 1.033 | 1.0329 | yes |
| Reliability 12..18 | .766 .780 .793 .804 .814 .823 .831 | .7663 .7803 .7928 .8039 .8139 .8229 .8311 | yes |
| Stations needed | 15 | 15 | yes |
| Cases settable / SP-needing (History, PhysEx, Comm, Procedural) | 18/18, 24/18, 19/19, 18/7 | same | yes |
| Eligible examiners offering sessions, 3 sites x 4 | 24,27,28,25 / 28,22,34,28 / 34,30,26,30 | same | yes |

## Competing answers that survived
No fork changes the committed call; three could move graded ask figures.
1. Ask 4, register vs attendance log: the register's "Last refresher" holds the date of 11 sessions the log records as Did not attend or Cancelled. Reading the register as proof of attendance gives 27,30,31,27 / 32,25,38,30 / 37,32,29,33 (sites in golden order: Centre, Simulation Suite, Fennabeg). Policy 5.2 says "have completed" and the log has explicit outcomes, so the golden follows from the text, but no shipped sentence says the register is not self-updating. Residual medium-risk item (this is the declared ask device, D2 in the design note). Optional closure: a register footnote.
2. Ask 3, CV-26 records sharing a title with a retired record: title matching gives 17/17, 23/17, 18/18, 17/6. The migration report's rule (CV-25 re-created records only) closes it; the text never says outright that CV-26 same-title cases are separate. Low to medium.
3. Ask 4 allocation date: no file gives 7 Dec 2026; counts identical for any December date. Immaterial to figures, but a wording defect in the solution blocks.
Tested and closed: absolute vs relative coefficient (0.782 at 18, closed by policy 4.3 and the plan: same stations every circuit); station 7 item 14 kept (15 holds); N/A as zero (15 holds, 0.802); circuit-session shared examiner effect scaled 11/12 (15 holds, 3-decimal figures would move to 0.796/0.807; standard G-study formula is the natural reading, low risk). Thin margin 0.8039 vs 0.80 is a clean point estimate; bootstrap SE about 0.03 but the text does not license a confidence-bound reading.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | 5 (pdf, xlsx, csv, docx, txt) | yes |
| Large file | 25,000+ rows | osce2026_marks_export.csv 35,040 rows | yes |
| Distractors named, none labelled by file name | 2+ | 3 in metadata.json (sp_agency_invoices_2026.xlsx, osce2026_candidate_feedback_summary.pdf, osce2026_global_grades.csv); names do not label them | yes |
| Distractors unused, relevant, ruled out | yes | unused by every answer; global grades ruled out by policy 3.2 (checklist is the station mark); none yields a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 7 reliabilities (3 dp), 8 domain counts, 12 site-session counts, chart; prompt states 3 dp and counts | yes |
| Prompt shape, rubric 25+ criteria | 25+ | prompt 803 chars, one paragraph; graded figures about 28 plus call and chart (rubric is generated; count not separately verified) | yes (by figure count) |
| No LLM-generated feel, goldens real | yes | judge found exports and office documents read as system output; goldens not opened by me | yes (judge hygiene PASS) |
Hygiene note from judge: May 2026 minutes cite policy numbers 3.2 and 3.4 while policy v7 is dated September 2026 (numbering assumed carried across); no stump impact.

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump class analytical, field_method (generalizability study to decision study), no decoy, no certified replay. Match. The declared distractors (invoices, feedback summary, global grades) were not named by the thread as carrying the task. Gate G classification: clean (no shipped artifact ranks the candidates on the decision question wrongly; no pack figure states a reliability or station count). Minor numeric note: the thread puts the crossed-examiner easy route at 0.817 at 12 stations (0.803 at 11) and alpha at 0.845 on the two-examiner mean; the note cites 0.816 single-examiner and 0.820/0.810 alphas. Same family and same wrong call (12), no conflict.
Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the note's Three rules (No decoy, Not semantics, Not rule application). The judge classes asks 3 and 4 as rule application, allowed for asks.

## Stump power (Gate F)
Good. Alpha with Spearman-Brown on the two-examiner mean, or a crossed lead/second rater model, says the standard is met at 12 (or 11); only the nested single-examiner D-study with stringency as error gives 15. Per the coordinator, the stage-4 cold reader landed the call and every ask figure, so architecture 1 is recorded as spent on Gate F; this report stands as determinism evidence for it.

## Findings, ranked
1. Solution wording: "7 Dec 2026" (ask 4, step 6) appears in no shipped file (prompt: "the December allocation"). Replace with "the December allocation (any December date gives the same counts)". FIX_NOW, wording only.
2. Ask 4 register vs attendance log (optional): footnote in the examiner register that "Last refresher" records the latest session booked, not proof of attendance. Changes no figure.
3. Ask 3 CV-26 same-title cases: low to medium; text closes via the migration report rule.
4. Margin 0.804 vs 0.80 is thin but clean.

## Next action for the author
Edit the solution blocks in submission.md (ask 4 and step 6) to drop the unsupported "7 December 2026" date; optionally add the register footnote in the generator (then rebuild twice byte-identically and reship). No prompt, golden figure or judge re-run required.
