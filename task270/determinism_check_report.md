# determinism-check report, task270, 2026-10-19 (run task270-r2, architecture 2, round 1)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (optional, wording only; no rerun needed for the call)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Band C is forced by the note's definition (claims the region's policies would have made with step protection). Raw counts put Y&H, WM, SE in band C with NW 4th (SE 12.5, NW 11.8). Completing small-claim truncation by step (above 2,500 claims scaled by the 37.8% share among step 0 and Step Protection claims) gives NW, WM, Y&H, with SE 4th by 1.2 to 2 points. The same set holds at thresholds 1,000 to 3,500, in a fault-aware variant and on the reference-group-only frequency. Every committed answer reproduced. Source: /tmp/determinism-check-task270-r2/verdict.md (single sonnet thread, scratch-only).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Vehicle-years 2024-25 (policy terms, mid-term, region map) | 182,255 | 182,255, all 8 regions match | yes |
| Accident claims incurred > 0 | 19,592 | 19,592, all 8 regions match | yes |
| Reported frequency SE / NW | 12.5 / 11.8 | 12.50 / 11.76 | yes |
| Share above 2,500 in step 0 + SP | 37.8% | 0.3785 (1,140 of 3,012) | yes |
| Windscreen freq and avg cost (8 regions) | 10.6/£270 ... 10.1/£296 | all 8 match | yes |
| Theft per 1,000 and net avg cost (8 regions) | 7.5/£5,474 ... 5.6/£6,444 | all 8 match | yes |

## Competing answers that survived
- None on the main call or asks 1, 2, 4.
- Ask 3 averages only: no file says whether the 1,213 chosen-repairer windscreen claim amounts include VAT. Grossing them up by 20% (prompted by the partner-job copies carrying net) gives NE £278, NW £322, Y&H £283, EM £310, WM £326, EoE £317, SE £369, SW&W £305 against the golden £270 to £359. The literal wording (amount the Society pays) supports the golden. Closing rule would be one sentence in the data guide.
- Minor: note 4.1 says thefts per 100 vehicle-years while the prompt and golden say per 1,000. The prompt is explicit, so it is determinate. NW against WM order within band C flips with threshold; not asked.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 15 | yes |
| Formats | 3+ | csv, pdf, xlsx, txt | yes |
| Large file | 25,000+ rows | policy terms 230,325 and 114,838 lines | yes |
| Distractors | 2+ in metadata.json, none named in a file | industry_private_motor_statistics_2025.xlsx, customer_complaints_log_2025.csv; file names carry no label | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | judge also flagged glass fitting_postcode_district as an unused field; both named distractors unused by the solution. Whether each reproduces a graded quantity was not separately tested | yes, weak evidence |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | asks 3 and 4 are 8 regions by frequency and cost; units and rounding in the prompt | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | ranked list under a cap (design note shape 01); the 3 + 1 + 16 asked figures plus the chart and the components exceed 25 on count, but I did not see the generated rubric | likely yes, unverified |
| Reads as real, not LLM generated | | judge found no authoring or benchmark disclosure; layout realistic | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor (counterfactual completion of censored claim counts), family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: Gate G `method_or_model_selection`, strategy `population_selection`, decisive step recovery of absorbed small claims from the claim-size distribution of step 0 and Step Protection policies. These agree: no planted defect, the stump is an estimator the data entitle. Neither declared distractor is named by the thread as carrying the task, and no shipped artifact ranks the regions on the 2027 basis. Gate G passes.
Gate H line: domain pass, layers pass, decisive_step analytical. Matches the note's `## Three rules` (domain test, Layer 1 migration mess, Layer 2 estimation_fit, not semantics, not rule application, no decoy).

## Stump power (Gate F)
Strong. The easy route (reported count per vehicle-year, or lifting steps 6 to 9 by the Step Protection uplift) after perfect cleaning files SE in band C and NW out. The data guide and step scale do not describe the truncation, so the solver must find it by comparing size distributions by step. The decisive step is not the field's textbook route handed over by a filed method, and the thread did not class it analytical on the basis of a standard method it applied without judgment. The thread rated it strong; the scored readers' result should still weigh it, since the method (size-based recovery) is reachable by a strong solver who thinks of reporting thresholds. Layer 1 (exposure, crosswalk, dedup, salvage) is gradeable grind on the asks.

## Findings, ranked
1. Optional: ask 3 average cost on chosen-repairer windscreen claims has a VAT-gross-up reading (see forks); one data guide sentence closes it, or accept as is.
2. Cosmetic: note 4.1 theft unit per 100 against the prompt's per 1,000.
3. Within-band order NW/WM is unstable but ungraded.
4. Rubric criteria count not independently verified.

## Next action for the author
Add one sentence to claims_and_policy_data_guide.pdf (via the generator) stating that chosen-repairer windscreen claim amounts are the amounts the Society paid, VAT included, and align note 4.1's theft unit to per 1,000; or accept both as they are. The main call needs no change and no re-judge.
