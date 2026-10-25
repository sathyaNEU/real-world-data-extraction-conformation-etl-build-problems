# task121 determinism check (architecture 4, stage 4, 2026-10-25)

One isolated judge thread on the cut pack (target.zip 2fbf1358), briefed by the determinism-judge agent; its verdict follows verbatim. Outcome: DETERMINISTIC, SEND_BACK on Gate H (the decisive step reads as rule application once the data are linked); with both scored readers on the call, architecture 4 is spent.


- **Verdict:** DETERMINISTIC
- **Disposition:** SEND_BACK, on Gate H only (decisive step is rule application and linkage). The determinism of every committed answer is clean. The repair rebuilds the decisive step, so a rerun is needed.

## Why
Every committed answer reproduces from the shipped files. The letter (WRP/CM/2026/118 (a)) and Schedule 7 Part 3.1 fix the estimand: the four conditions of each passenger's own trip and the counterfactual "had journeys met that driver as in spring 2025, the other three as they were". All reasonable estimators land on the same whole-point answer, so there is no live fork on the main call or the asks. The weakness is Gate H: nothing analytical separates a careful solver from the golden once the data is linked and the definitions are read.

## Evidence (recomputed from the bundle)
| Item | Golden | Mine | Reproduced |
|---|---|---|---|
| Weighted share satisfied (codes 4-5), 2025 / 2026 | 86.4 / 81.2 | 86.35 / 81.16 (fall 5.19) | yes |
| Crowded journeys 2025 / 2026 (train-level load-weigh sum above formed seats, any departure on the passenger's trip) | 7.2 / 16.8 | 7.22 / 16.84 | yes |
| Late 2025 / 2026 | 8.0 / 12.5 | 8.04 / 12.45 | yes |
| Unstaffed 2025 / 2026 | 9.3 / 39.0 | 9.28 / 39.02 | yes |
| Crowding effect | -32.5 pts | -32.45 (weighted linear, wave term) | yes |
| Points: crowd / staffing / punctuality / fares | 3 / 1 / 1 / 0 | 3.12 / 1.27 / 0.65 / 0.01, residual 0.13 | yes |
| On time (MAIN, VALE, COAST, BRANCH, LINK) | 81.0 / 84.6 / 85.0 / 87.4 / 79.0 | 81.03 / 84.61 / 85.01 / 87.40 / 78.98 | yes |
| Staffed (same order) | 89.5 / 43.9 / 47.6 / 43.5 / 88.8 | 89.51 / 43.94 / 47.59 / 43.46 / 88.84 | yes |
| Standing at MVC 07:00-09:59 (MAIN, VALE, COAST, LINK) | 1,720 / 829 / 1,210 / 3,021 | 1,720 / 829 / 1,210 / 3,021 | yes |

Linking steps that reproduce uniquely:
- Station codes: each lowercased written name maps to exactly one code across the coded rows, so the uncoded rows resolve with no ambiguity.
- Batches: all 1,588 fieldwork batches match a train in the movements by date and headcode.
- Roster amendments: all 26 amendments match exactly one Sick or Vacant turn (original_staff_ref, same or next day), with 0 ambiguous. The 19 Sick/Vacant turns left unmatched are correctly unstaffed.
- Standing: the load-weigh rows must be matched by unit and the departure minute, because a headcode runs twice a day. The 9 trains without a previous-station departure and the 14 missing-unit rows are trains that did not run, which gives 0 either way. Counting seats for missing units gives identical totals.

Estimator robustness for the points, all giving 3 / 1 / 1 / 0:

| Estimator | Crowding | Staffing | Punctuality | Fares |
|---|---|---|---|---|
| Weighted linear, with or without wave term | 3.1 | 1.3 | 0.65 | 0.01 |
| Logit standardised (g-computation) | 3.16 | 1.27 | 0.65 | 0.05 |
| Unadjusted stratified | 3.07 | 0.64 | 0.69 | ~0 |
| Separate per-wave fits | ~3 | ~1.3 | ~0.7-0.9 | ~0 |

The punctuality and unadjusted-staffing values (0.64 to 0.69) sit near the 0.5 rounding line but stay above it under every variant tried. Rounding to the nearest whole point is licensed by the prompt.

Competing answers tried:
- Unit-level "any unit over its seats" crowding: 8.5 / 18.4 shares, 2.9 points. The answer is the same, and Schedule 7 3.1(a) says "the train".
- Ratings-controlled model: crowding falls to about 0.9 pts and staffing 2 by derived importance. Neither is licensed, because the letter defines the points through journey conditions, not attribute ratings.
- Topline Q5 ratings (staffing availability -14): this is a different estimand from the one filed, not a defensible alternative.

## Files/Hygiene
PASS. 19 files in 4 formats: csv x14, pdf x4, xlsx x1, txt x1. The files read as operational extracts: written-in station spellings, reissued headcodes, a closed archive replaced by a new rostering platform, a Dec24/Dec25 timetable change, and a vehicle-row system change. Distractors present: customer_contacts, delay_attribution, the topline PDF. No authoring or provenance leakage and no temporal incoherence found (field notes 23 Oct 2026, letter 2 Oct 2026, baseline ends 19 Sep 2026). Nothing exclusion-level.

## Stump power
Moderate to low. Every honest estimator reproduces the golden, and unadjusted stratification gets 3 / 1 / 1 too. The only wrong route is the topline or Q5 ratings route (staffing availability -14, derived importance 2 for staffing), which the letter's counterfactual wording already rules out. The real difficulty is the heavy linkage and execution of the defined measures (about 17,800 responses to batches, trains, units, load-weigh, crew, roster, amendments). A strong model that links the data correctly passes, and one that does not is stumped on execution, not insight. Most natural lever: make the effect estimation itself decide the call, so that adjusting for the other three drivers or for service-group and time-band mix, or handling a selection effect in who responds, flips crowding against staffing. The wave-level confound should be real in the data and not defeated by an unadjusted split.

## Stumping type
mechanism: etl_conformance / rule application (decision is the execution of filed Schedule 7 definitions on linked data); stumping_family: analytical_non_defect (borderline); surface_read_dependency: no (borderline); sole_data_defect: no. The topline and Q5 ratings are correct numbers, and the task asks for a different estimand, so this is not a banned flip. The risk is that it is weakly analytical (see Gate H).

## Three rules
domain: pass (the swap test fails to reproduce the same task: a key-driver bridge of a satisfaction tracker through journey-level conditions is customer-research work), layers: pass (Layer 1 is written-in station spellings, headcodes reissued across timetables, Dec24/Dec25 timetables, bank holidays on SUN schedules, vehicle versus unit load-weigh rows, rostering platform change with logged-evening amendments; Layer 2 is the effect estimation and the bridge), decisive_step: rule_application.
The decisive work is linking and executing definitions that are already filed (Schedule 7 3.1, letter (a)). The easy route a strong analyst would take, a one-driver-at-a-time unadjusted standardisation on the correctly linked conditions, gives the same 3 / 1 / 1 / 0, so no analytical choice separates the solver from the golden. The wrong answers come only from skipping the linkage and using the topline ratings.

## Fix
prompt / input_files. Do not alter the baseline measures (they are clean and forced). Rebuild the main call so that estimator choice decides it: for example, respondent selection or sample mix that makes the unadjusted and the adjusted effects point to different drivers, or a driver whose effect is only visible with the right comparison group. Then re-run the Gate H test.
