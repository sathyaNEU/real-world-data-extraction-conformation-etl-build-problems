# determinism-check report, task172, 2026-10-31

## Verdict
DETERMINISTIC (no SOLUTION_WRONG; one residual method fork on the main call, recorded below)
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Gate H:** domain: pass, layers: pass, decisive_step: analytical

Bundle judged: target.zip sha256 0b377dd6180abad062d54da1bd817ba2a0e09385de82555b184ac16111e6425e, architecture 2, one pass, one thread (verdict at /tmp/determinism-check-task172-233837/verdict.md).

## Why
Every graded figure reproduces from the shipped files. The main call is forced by the charter s4.1 ("progression in each arm over that remaining follow-up as the interim data estimate it") plus the data, which reject a constant per-arm hazard (piecewise-vs-constant likelihood-ratio p = 0.004; placebo hazard rises, ravolimab falls). Every time-varying projection the thread tried (6 piecewise cut-point sets, per-arm Weibull) gives conditional power of 96 to 100 per cent: 100 to the nearest 10, band C, continue as planned. The constant-versus-time-varying choice is not closed by a sentence, only by the data; the thread judged it a risk, not a failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Interim cut (165th event) | 17 Nov 2026 | 2026-11-17 (164 events the day before) | yes |
| Randomisation date UTC to site tz | arms 224/226 | 23 of 450 change day; 224 placebo, 226 ravolimab | yes |
| Events by arm | not stated | 87 placebo, 78 ravolimab | yes |
| Stratified HR (Cox, Efron) | 0.91 (0.67 to 1.24) | 0.911 (0.668 to 1.244) | yes |
| At risk at cut / past week 12 | 267 / 200 | 267 / about 200 | yes |
| Rate ratio early / late | 1.3 / 0.4 | about 1.4 / 0.34 (cut-point dependent) | same order |
| CP, HR 0.91 carried forward | about 5 | 6 to 8 (band A) | same band |
| CP, constant hazard per arm | not stated | 12 to 14 (band A) | n/a (competing reading) |
| CP, piecewise / Weibull | 100 | 98 to 100 / 96 to 98 (band C) | yes |
| SAE counts, both arms (patients, all, 4 SOCs) | 113/170/53/57/18/23; 132/222/65/74/23/30 | identical | yes |
| ALT>5x, AST>5x, bili>3x | 2/1/10 placebo; 10/10/16 ravolimab | identical (robust to first-dose source and cut filter) | yes |
| Exposure | 223/1455; 226/1501 | identical (IRT administered; EDC is a strict subset) | yes |

## Competing answers that survived
Recorded residuals with the thread's own reading of each:
1. **Main call, constant against time-varying hazard.** A reader estimating one constant rate per arm gets band A (stop) at about 13 per cent; one carrying the Cox HR gets band A at about 5 to 7. Neither charter nor SAP states proportional or non-proportional hazards. The data separate the candidates (LR p = 0.004; Weibull shapes 1.55 and 1.12) and "as the interim data estimate it" favours the time-varying estimate, so the thread did not fail Gate C. It is the single place a differently reading expert diverges. Closure, if wanted, only by filing the WHAT (projection from each arm's progression as it runs over follow-up time), never the piecewise HOW.
2. **SAE reports received after the cut** (listing runs to 2026-12-01). Ignoring them gives ravolimab 220 SAEs, 64 infections, 73 hepatobiliary. The SAP defines inclusion by onset date and "latest report", so the golden's reading is the literal one. Ask-level.
3. **EDC-only exposure.** Gives 1378 and 1439 doses, 220 and 224 patients; 139 IRT-administered doses have no EDC page (entry lag, three sites). The SAP names no source for "doses given"; IRT "Administered" and the union is the defensible answer, though no sentence says so. Ask-level.
4. **Melbourne receipt dates.** Dating central samples by receipt adds 2 patients each to ALT, AST and bilirubin per arm; the SAP's "sample taken" and the kit log close it. Ask-level.

Only fork 1 touches the main call; none of 2 to 4 flips the recommendation.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | pdf, csv, xlsx, json (4) | yes |
| Large file | 25,000 rows or more | talon2_central_lab_transfer.csv, 39,530 rows (metadata.json); thread counted 39,531 with header | yes |
| Distractors | 2 or more named, none labelled in a file name | talon2_edc_adverse_events.csv, talon2_investigator_tumour_assessments.csv, each with a stated ruling-out fact; the file names do not label them | yes |
| Distractors unused yet weighable | yes | investigator reads (183 against 152 progressions) and EDC AE pages are unused by the solution and relevant; neither answers a graded quantity (thread: "unused-but-weighable") | yes |
| Deliverables | 1 to 3, all in golden | 2 (recommendation pdf, tables csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 22 count cells across two arms from several sources; the prompt states "nearest 10 per cent" and "whole number" | yes |
| Prompt shape and 25+ criteria | identifiable; 25 or more | single paragraph, 922 characters, shape identifiable; the rubric is generated, so the count could not be confirmed here (24 graded values plus recommendation, 26 or more gradable items) | likely, unverified |
| Reads as real, not LLM generated | yes | thread found no authoring language; mess is system-style; timeline consistent | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card (`stump_class: analytical`, `analyst_test`, `domain_test` present; note has `No decoy:`, `Not semantics:`, `Not rule application:` lines and a Three rules block): the stump is the non-proportional hazard under a forward projection, the easy route being the B-value / carried-forward HR at about 5 per cent; this matches the thread. The declared distractors (investigator reads, EDC AE pages) were not named by the thread as the surface read carrying the task; they rank nothing. No mismatch. Gate H: the thread's line (domain pass, layers pass, decisive_step analytical) matches the card's domain_test and analyst_test (DMC conditional power inside group-sequential machinery; layer 1 mess is UTC dates, re-screen numbering, receipt-dated labs, units; layer 2 is projection over remaining follow-up).

## Stump power (Gate F)
Good, per the thread. The standard route (conditional power at the stratified HR 0.91 or one constant rate per arm) is a few lines and files a futility stop at 5 to 13 per cent against the golden's 100. Only a solver who checks the rate ratio by visit finds the crossing (about 1.4 early, 0.34 late) and projects the 200 late-phase at-risk patients on it. Caveat for the main thread: conditional power under the charter's "as the interim data estimate it" is the field's standard method, and a strong solver who inspects hazards by visit lands it, so weigh this against the design note's ladder. The thread classed the decisive step analytical, and the golden needed a judgment the data had to settle (constant against time-varying), so this is not a description of an execution-only route. The SAE re-screen linkage and Melbourne-date traps are real but ask-level.

## Findings, ranked
1. Residual fork 1 (constant against time-varying hazard): the only place a literal reader can legitimately diverge on the main call; separated by the data (p = 0.004), not by a filed sentence. Not blocking.
2. Fork 3 (exposure source): no sentence in the SAP names the source for "doses given". Ask-level.
3. Forks 2 and 4: closed by the SAP's wording. No action.
4. Rubric criterion count not verifiable at this stage.

## Next action for the author
None required to ship. Optional: if you want fork 1 closed from the filed text, add to the charter or SAP a WHAT sentence that the remaining follow-up is projected from each arm's progression as it runs over follow-up time (not the piecewise HOW), then rebuild and re-judge once.
