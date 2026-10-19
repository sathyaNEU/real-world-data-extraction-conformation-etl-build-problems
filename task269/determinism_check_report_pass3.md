# determinism-check report, task269, 2026-10-19 (pass 3)

Judged against the bundle the thread saw (fix-pass pack, target.zip md5 7d5919da). The working-tree target.zip is now md5 bb6653ee (moved on in a repair pass) and was not re-judged. Thread output: /tmp/determinism-check-task269-r31792390143/verdict.md (one thread; the main session spawned it because my runtime has no Agent tool).

## Verdict
NOT_DETERMINISTIC (Ask B only), plus SOLUTION_WRONG on two solution-text claims.
**Disposition:** SEND_BACK (the thread's call; the fix changes what solvers see, so a rerun is needed). Main call, stump and Asks 1 to 3 may stay frozen.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Ask 4 (examiners eligible at the 7 Dec 2026 allocation, by site and session) turns on an identity decision no shipped file settles. Three training rows under hospital or Fennabeg numbers (H26652 Cal Gately, H30491 Evelyn Casserley, F85944 Carrie Coyne) each match exactly one register entry, a GP Trainer based in general practice. The golden gives them to a different person and drops them. Counting them as the register examiner, the rule the golden applies to every Callowfield, CUH and Fennabeg namesake, raises all 12 cells by one (Centre 29/29/30/31, Suite 34/34/35/35, Unit 23/25/22/20). Each shows the dual-post pattern (E-number initial training, later H or F refresher) and each offers the site of that session. Gates C and E fail on Ask B; taxonomy competing_defensible_answer. The allocation-date finding of pass 2 is closed (7 Dec 2026 is filed and the 3 Dec 2023 cut falls in a gap).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Marks prep (day-2 codes to day-1 badges, station 7 item 14 out, N/A out of denominator; 84 x 12 x 2) | balanced | 0 mismatches | yes |
| Variance components (EMS): cand, cand x domain, domain, station in domain, cand x station, examiner in station, residual | 0.92, 0.76, 0.22, 0.49, 1.36, 1.06, 1.08 | 0.925, 0.757, 0.230, 0.492, 1.355, 1.059, 1.076 | yes |
| Reliability 12 to 18 stations | 0.79, 0.81, 0.82, 0.83, 0.84, 0.84, 0.85 | 0.793, 0.806, 0.818, 0.828, 0.836, 0.845, 0.852 | yes |
| Main call | 13 | 13 (stable under equal weights 0.8058, item 14 kept 0.8069, N/A as 0 0.8052) | yes |
| Ask 3 (can be set / need SP) | 13/13, 16/13, 14/14, 14/6 | same | yes |
| Ask 4 | Centre 28/28/29/30, Suite 33/33/34/34, Unit 22/24/21/19 | same only with the three GP-base namesake rows dropped | partly (conditional) |
| "16 stations" for the undivided-bank design, candidate x domain booked as error | 16 | 0.797 at 18, no number within 18 | no |

## Competing answers that survived
1. Ask 4, GP-base namesakes (decisive): count the three rows as dual-post staff, every cell +1, versus the golden's exclusion. Nothing in the files separates the two readings; the register has no second person of those names. No shipped rule closes it.
2. Ask 4, source of training status (second order): register training and refresher dates give Centre 24/25/25/28, Suite 30/30/30/31, Unit 19/21/19/16. The log explains every disagreement (six register refreshers are Did not attend, 25 entries stale), but no file says the log governs.
3. Ask 3 (minor): four CV-26 version-1 records share a title with retired cases set in 2025 (Alcohol use: history, Shoulder examination, Discussing weight with a teenager, Checking a blood transfusion). If they inherit the sitting, counts fall by one per domain (12/12, 15/12, 13/13, 13/5). The files support the golden (version 1 is a newly written case), but the version-minus-one matching for CV-25 is inferred, not filed.
4. Main call: a random-bank reading of policy 4.3 ("stations being drawn from the case bank") is a residual argument; the thread judges 4.2 governs. 12 (single-examiner alpha 0.80/0.81, or the 2026 both-examiner 0.84) is ruled out by the delivery plan.

## Spec gates
Rubric size and "reads as LLM generated" for goldens are not decidable from the bundle; the thread found nothing machine-authored in the pack. Deliverable and distractor rows are from metadata.json and the submission.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | pdf, xlsx, csv, docx, txt (5) | yes |
| Large file | 25,000 rows or more | marks export 35,040 rows | yes |
| Distractors | 2 or more, named, unlabelled by file name | 3 named (SP invoices, feedback summary, global grades); none carries a graded quantity (global grades are ruled out by policy 3.2) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | stated in the prompt; Ask 4 is the one not determinate | no (Ask B) |
| Prompt shape and 25 or more criteria | identifiable | 23 ask figures plus call and components; not verified against a generated rubric | not verified |
| Reads as real work product | yes | no machine-authored signs found by the thread | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: Gate G method_or_model_selection, strategy decomposition_attribution, Layer 2 family field_method, decisive step the fixed-domain decision study. No mismatch. The thread names no declared distractor as the surface read; none is load-bearing. Gate H: domain pass (generalizability-theory decision study), layers pass (day-2 recoding, withdrawn item, N/A items, migration records, name and staff-number variants; Layer 2 is choosing which components are error), decisive_step analytical. Matches the design note's `## Three rules`.

## Stump power (Gate F)
Good. Single-examiner alpha files 12, the pooled/random-bank study files 16 or "not reachable"; the design note records two cold readers at stage 4 round 2 both filing 16. The margin around 0.80 is thin (about 0.006 either side) but clean.

## Findings, ranked
1. Ask B: three GP-base namesake training rows cannot be assigned from the files; all 12 cells move by one. Sole blocker.
2. Ask B: register training dates versus the attendance log, no filed precedence.
3. Solution text: the "16 stations" rationale (undivided bank "books each candidate's strength in a domain as error") does not reproduce; the thread gets 0.797 at 18 for that reading and 16 only with candidate x domain left out of both true score and error. The design note says the 16 is the pooled study's own number and that the write-up now states it with components; the rationale wording still needs to match the computation.
4. Solution text: step 8 reads backwards on why the three rows' attendance counts.
5. Ask A optional: pin CV-26 version-1 records as new cases and the version-minus-one inheritance rule in the filed text.

## Next action for the author
Make the identity of the three rows resolvable by a join in the files (a hospital or Fennabeg staff-number column for dual-post staff in the register, or a base field in the training log) and say which source governs training status; correct the 16-station rationale and step 8; then rebuild and send back. Main call and Asks 1 to 3 stay frozen. No second thread is licensed for this pass.
