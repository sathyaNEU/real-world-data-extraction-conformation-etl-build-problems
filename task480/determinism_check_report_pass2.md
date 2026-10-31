# determinism-check report, task480 (pass 2), 2026-10-31

## Verdict
NOT_DETERMINISTIC (underspecified_objective / competing_defensible_answer). The golden figures reproduce under the golden's own method; the SOLUTION is not wrong.
**Disposition:** SEND_BACK (the thread's disposition, not softened).
**Stumping type:** mechanism: method_selection (mileage curve), stumping_family: method_or_model_selection, surface_read_dependency: no, sole_data_defect: no

## Why
Guidelines 3.3 say only that 2027 miles are "judged on its own odometer reading" with age counted from 1 January of the model year. Nothing shipped mentions a cumulative curve, a fit, a quadratic, or a rise from 1 Jan 2027 to 1 Jan 2028. Solution step 3 cites "guidelines 3.3" for it, and 3.3 does not say it. The call flips with the estimator: odometer divided by age gives 9 counties, a linear cumulative fit gives 6 (Dunmarsh 10.29), and the golden quadratic gives 5. The odometer-over-age route is the plain literal reading of 3.3, and the golden rejects it. Ask 3 has a second fork on "retired" (below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible vehicles (vehicle_registrations_2026-07-01.csv) | 65,305 | 65,305 | yes |
| Vehicles with a usable first INITIAL reading (eip_inspections_2024_2025.csv, VIN plus 74 plate/model-year joins) | 61,865 | 61,865 | yes |
| 12 county 2027 NOx, quadratic ratio x rise | 15/14/13/12/11/9/8/8/8/6/5/5 | 15.32/14.30/13.32/12.33/11.27/9.21/8.22/8.20/8.18/6.13/5.15/5.10 | yes, all 12 |
| Quadratic with whole-year ages / through origin | n/a | 5 counties both | same call |
| Linear fit | n/a | 6 counties (Dunmarsh 10.29, Copperleaf 9.20) | competing answer |
| Odometer / age | n/a | 9 counties (Dunmarsh 12.81, Copperleaf 11.45, Larkhaven 11.40, Quarrybrook 11.37) | competing answer |
| Pilot retired vehicles (vrp_pilot_vouchers_2025.xlsx, ACTIVE-VIN exclusion) | 222/201/154/102 (679) | 679 (741 vouchers less 62 ACTIVE) | yes |
| Pilot dollars (tow-zone charges 185/280/330/395, Calderwick and Thistlebury lines) | 59,050/53,985/42,590/26,625 | match once the 679 rule is accepted | yes |

## Competing answers that survived
1. **Main call and ask 1 (estimator fork).** Odometer over age gives 9 counties, a linear fit gives 6, the golden quadratic gives 5. Nothing shipped selects among them.
2. **Ask 3 ("retired").** All 741 vouchers are PAID with a surrender date and an invoice. The golden drops the 62 with a later ACTIVE registration. The only shipped hook is the code-values line "CANCELLED: Title cancelled: destroyed, exported or retired", and no shipped sentence ties "retired" to that status or excludes ACTIVE owners. The literal count is 741 (238/214/171/118) with higher dollars; the golden is 679. I could not close this from guidelines 4.1 and 6 or the close-out.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | registrations 253,717; inspections 197,738 | yes |
| Distractors | 2 or more, in metadata.json, none named in a file name | DOT VMT and gasoline sales named in metadata.json (a register and population are also present), none labelled in a file name | yes |
| Distractor weight | unused by the solution, relevant, ruled out by a shipped fact | VMT and gasoline are ruled out by the 3.3 wording | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states tons, dollars and counts | yes |
| Rubric 25 or more criteria | 25 or more | not countable from the shipped pack; 12 counties plus 4 pilot rows plus chart and memo make it plausible | unverified |
| Reads as human work product | yes | thread saw no LLM tells | yes |

## Gate G reconciliation
Thread: method_or_model_selection, surface_read_dependency no, sole_data_defect no. The design note declares a method_or_model_selection, analytical_non_defect stump, so the family matches. The thread did not name the declared distractors (VMT, gasoline) as the surface read, so they are not too load-bearing. The mismatch is not in the family. It is that the method is not filed: the design note says the curve is selected by the data (chi-square 5,820 linear against 30 quadratic), but nothing shipped states a selection criterion or the curve form. The thread's own F-test (quadratic against linear F = 16.0; cubic F = 2.3) shows the data does separate them, but only by a test the solver has to choose. Under the contract's literal-execution rule, a method open without a filed criterion is an open fork, not a pass.

Main-thread facts, weighed:
- The first pass (2026-10-21) found DETERMINISTIC/APPROVE with watch items on these same two points.
- This reship changed neither the estimator evidence nor the pilot files.
- The real reviewer sees only the shipped text. I do not soften the verdict because an earlier pass was lenient.
- The reship did remove the extract notes, which had explained codes. Whether guidelines 3.3 changed I did not check, so I do not claim this thread's finding is new.

## Gate H
domain: pass (mileage accumulation and emission inventory estimation). layers: pass (Layer 1 is typed VINs, KM readings, 0/999999 odometers, unmatched plates and Oakhaven repeated totals; Layer 2 is modelling 2027 travel from cross-sectional odometers). decisive_step: analytical in intent, since the easy route fails; but the curve choice is unfiled, so it behaves as a withheld rule. The design note and card also say analytical. This matches, and the defect is determinism, not Gate H.

## Stump power (Gate F)
The trap is genuine and data-native: average miles per year overstates a vehicle's marginal 2027 miles because cumulative mileage is concave (about 10k a year against 14k average). A strong model on odometer over age fails. A solver who fits a linear curve also misses, and cannot tell a legitimate alternative from an error. A strong solver on a fitted-curve route is a landable call, so stump power rests on the method being found, not on a filed rule. Once the WHAT is filed it is a textbook route, so weigh the 1.3 stumping against the design-note ladder.

## Findings, ranked
1. Estimator unfiled (main call and ask 1): 9, 6 or 5 counties depending on method. File the WHAT (that 2027 miles are the vehicle's reading scaled by the area's cumulative-mileage-by-age curve fitted to the cycle's readings) and a selection criterion between linear and quadratic, or ship a fact that separates them. Do not file the HOW as a recipe.
2. Ask 3 "retired" rests on an inference (741 against 679). File a sentence on what counts as retired, or on a surrendered vehicle later registered again.
3. Minor: add the age convention (fractional days/365.25 against whole years) to the fork table. Both give the same call.
4. Rubric criteria count unverified from the pack.

## Next action for the author
Close the estimator fork and the "retired" fork in the shipped text (guidelines or close-out), keeping the method choice a filed criterion and not a recipe. Rebuild, then re-judge once under /fix-determinism.
