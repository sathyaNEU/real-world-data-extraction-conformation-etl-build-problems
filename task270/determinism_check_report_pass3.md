# determinism-check report, task270, 2026-10-19 (pass 3, run r4)

## Verdict
DETERMINISTIC (main call and asks 1, 2, 4 and the ask 3 frequencies reproduce; the eight ask 3 average costs rest on a convention the shipped text does not state).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (truncation/selection correction of a counterfactual estimand), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Isolation caveat: the brief held the graded blocks in the same file the thread read first. The thread says it then derived everything from the bundle with its own code before comparing with the golden. Read the agreement as a weaker independence signal than a blind derivation.

## Why
Band C = North West, West Midlands, Yorkshire and the Humber, with South East first below, is forced. Note section 2.1 defines the frequency as a counterfactual with every policy on step protection. Steps 1 to 5 cannot buy the add-on and show the same missing small claims, so they must be corrected as well. Every estimator the thread ran gives the same band C set: scaling by the step 0 and Step Protection share above a threshold (1,500 to 4,000), a step 0 only reference, a Step Protection only reference, and region-specific shares. The easy routes, reported frequency and the Step Protection uplift on steps 6 to 9, both put South East in.

One open fork remains, on ask 3's eight average costs only. Note 3.2 says a replacement and the camera recalibration it needs are one claim, and is silent on a recalibration booked alone for a screen another repairer fitted. Read literally with no attach, the costs are NEC 267, NW 301, YH 282, EM 293, WM 317, EoE 316, SE 363, SWW 286, against the golden's 273, 307, 285, 296, 324, 322, 369, 292. The frequencies move by 0.1 or less. The golden's rule also says "nearest same-policy repairer claim" only in the thread's reconstruction, so the filed sentence must say how a recalibration is matched when a policy has more than one repairer claim.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Vehicle-years 2024-25 | 182,255 | 182,255.0 (policy terms legacy+platform, mid-term adjustments, region map) | yes |
| Accident claims above nil | 19,592 | 19,592, each joined to one policy-year segment | yes |
| Reported frequency SE / NW | 12.5 / 11.8 | 12.50 / 11.76 (YH 12.82, WM 12.73) | yes |
| Share of step 0 + Step Protection claims above 2,500 | 37.8% | 37.85% (3,012 protected claims) | yes |
| Step Protection uplift, steps 6 to 9 | 1.27 | 1.268 | yes |
| Ask 1 / 2 band C and first below | NW, WM, YH; SE | same (NW 14.18, WM 14.16, YH 13.63, SE 12.29) | yes |
| Ask 3 frequencies, 8 regions | 10.7, 13.0, 11.3, 10.7, 12.7, 9.5, 11.7, 10.2 | match with recalibration attach | yes |
| Ask 3 average costs, 8 regions | 273, 307, 285, 296, 324, 322, 369, 292 | match only with the attach; 267, 301, 282, 293, 317, 316, 363, 286 without | conditional |
| Ask 4 theft rates and costs | 7.5/5,474 ... 5.6/6,444 | all eight match (4,605 claims into 3,700 thefts) | yes |
| Chart ask (png) | ranking and band marking | follows the main call | yes |

## Competing answers that survived
- Ask 3 average cost, windscreen: attach a recalibration-only job's amount with VAT to the other repairer's claim (golden) or leave it out because 3.2 is silent (each region 6 pounds lower). The shipped rule meant to close it is the solution-steps sentence in submission.md, which is not in the bundle. It is not closed by any shipped file.
- Main call: none.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | pdf, csv, xlsx, txt | yes |
| Large file | 25,000 rows or more | 230,324 and 114,837 row policy extracts | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | industry_private_motor_statistics_2025.xlsx, customer_complaints_log_2025.csv; neither name labels one | yes |
| Distractor relevance | unused by solution, weighable, ruled out by a shipped fact | thread found both unused and plausible but not decisive; no figure answering a graded quantity was tested | yes, weakly checked |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | the prompt gives per 100 and per 1,000 to one decimal and costs in whole pounds; 8 regions by 2 measures | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 01 ranked list under a cap per the design note; the rubric is not generated at this stage, count not verified | not verifiable here |
| Reads as real work product | no LLM look | thread found no synthetic language; note PDF metadata shows September 2026 creation against the 5 October guide date, scrub | yes, with a metadata scrub |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Gate G `method_or_model_selection`, strategy `population_selection`, analytical stump, decisive generator G12 then G14 and G16. These match. The thread names no declared distractor as the surface read carrying the task; the two declared distractors play no part in either easy route. The easy routes it names are the reported frequency and the Step Protection uplift, which the note's analyst test also names (both file South East, West Midlands, Yorkshire and the Humber).

## Gate H line
domain: pass, layers: pass (Layer 1: legacy/platform systems, units, time zones, region map change, crosswalk; Layer 2: correcting for no-claims-step suppression of small claims), decisive_step: analytical. The thread's reading agrees with the note's `## Three rules` (Domain test, Analyst test, No decoy, Not semantics, Not rule application). The note does not file the correction method, so the decisive step is not rule application. The estimand is filed and the method left to the data, which the CLAUDE.md spec allows. The thread did not class it analytical merely because it is a standard method: its easy-route alternatives measurably give a different band C.

## Stump power (Gate F)
Good. A strong analyst who cleans everything lands on South East in band C from the reported frequency (12.5 against 11.8) or from the Step Protection uplift (SE 14.87, NW 12.27). Both leave steps 1 to 5 uncorrected. The asks add independent device work: the recalibration attach, duplicate platform registration of partner jobs, the salvage join and separator-normalised crime references. The portal's measure, not this thread, decides stumping.

## Findings, ranked
1. Ask 3 average cost fork (Gate C/E), fixed by one filed sentence on a recalibration alone, including its match to a repairer claim. This touches no figure and no solver-visible data.
2. Minor: rating_basis_2027_note.pdf metadata dates (September 2026) precede nothing it cites but sit oddly against the 5 October guide date; scrub.
3. Reading-order note: the thread saw the graded blocks before deriving. Consider a separate blocks file for the next pass.

## Next action for the author
In the data guide or rating_basis_2027_note.pdf section 3.2, add one sentence: a camera recalibration booked alone for a screen another repairer fitted on the same policy just before is part of that repairer's claim, its amount with VAT added to that claim, and is not a claim of its own. Also state which claim receives it when the policy has several. Rebuild the pack with identical figures, scrub the PDF metadata dates, and the report goes to the main session. This is the one re-judge already used, so the main session decides whether a further read is needed.
