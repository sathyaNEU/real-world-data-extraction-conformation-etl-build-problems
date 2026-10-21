# determinism-check report, task480, 2026-10-21

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (with one caveat: the judged bundle is the pre-re-site bundle, see Findings 1)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (sonnet, medium) judged the fresh unzip of target.zip and the inlined blocks; full output at /tmp/determinism-check-task480-025558/verdict.md. Every committed answer reproduced from the shipped files. The five-county call (Wexmoor, Halvering, Linnmere, Elkhollow, Marlbank) holds under every curve of degree 2 or higher, either fit population and integer or fractional age (Marlbank 10.94 to 11.28 tons, Dunmarsh 8.94 to 9.21 against the 10.0 line). The competing easy routes are biased and file different sets: odometer over age gives nine counties; the area curve without the own reading gives Dunmarsh, Halvering, Linnmere, Wexmoor.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible vehicles (registrations, ACTIVE, MY 2005-14, G/F, GVWR 1/2a) | 65,305 | 65,305 | yes |
| Vehicles with a usable first completed INITIAL reading | 61,865 | 61,865 | yes |
| Marlbank 2027 NOx | 11 t | 10.94 | yes |
| Dunmarsh 2027 NOx | 9 t | 8.94 | yes |
| All 12 county tons (15,14,13,12,11,9,8,8,8,6,5,5) | as listed | 14.91,13.91,12.95,11.97,10.94,8.94,7.97,7.97,7.93,5.94,4.99,4.96 | yes |
| Counties at 10 t or more | 5 | 5 | yes |
| Pilot retired / dismantler cost: Elkhollow, Dunmarsh, Larkhaven, Kinnard | 222/$59,050; 201/$53,985; 154/$42,590; 102/$26,625 | same | yes |
| Station counts, 12 counties (Wexmoor 30,798 ... Kinnard 4,693) | as filed | all 12 exact | yes (on the pre-re-site bundle) |

## Competing answers that survived
No fork changes the main call. Two watch items from the thread, both on the asks or inside a closed margin:
- Curve family: guidelines 3.3 name no curve. Linear cumulative fit gives Dunmarsh 10.29 or 11.18 (six counties); a non-parametric by-age mean gives Dunmarsh 9.76 (still below the line) but moves tons by up to 1.3. The data's visible concavity rejects the linear fit; the main call survives every degree 2 or higher fit.
- Pilot "retired" test (ask 3): no filed sentence says ACTIVE after surrender means not retired. The literal all-741-voucher reading gives 238/214/171/118 vehicles and $63,405/$57,640/$47,280/$30,720. The dictionary defines CANCELLED as destroyed, exported or retired, and the golden's 679 all show it. Weakly closed, ask only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 3 (CSV, XLSX, PDF) | yes |
| Large file | 25,000 or more rows | 197,738 inspections; 253,717 registrations | yes |
| Distractors named in metadata.json, none labelled in a file name | 2 or more | 3 (dot_county_vmt_2025.csv, gasoline_sales_by_county_2025.csv, county_population_estimates_2025.csv), each with a "why" | yes |
| Distractors unused, relevant, ruled out by a shipped fact | yes | VMT, gallons and population are other bases; ruled out by 3.3 (own-reading basis); none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | county NOx, chart, pilot counts and dollars, 12-county station counts; prompt states tons, dollars, whole numbers | yes |
| Rubric 25 or more criteria, prompt shape | 25 | not checkable here (rubric generated downstream); 12-county table plus 4-county pilot plus 12 station counts plus components supply well over 25 gradable items | not verified |
| Reads as real work product, not LLM generated | yes | thread: agency-style artifacts (station-number reuse, Oakhaven export defect, KM readings, ABORT rows); golden xlsx and docx not opened by the thread | partly |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Layer 2 is estimation_fit (own reading as level on the fleet's cumulative curve times the curve's rise over 2027), the analyst test files nine counties (and four on the curve alone), No decoy / Not semantics / Not rule application lines present. These match. The declared distractors (DOT VMT, fuel sales, population) are not named by the thread as the surface read carrying the task; the competing wrong routes are both built from the registrations and inspections, not from a distractor. Gate G: pass, no shipped artifact ranks counties on the decision question.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the note's Three rules (mobile-source inventory mileage accumulation by age; Layer 1 is KM readings, typed VINs, 0/999999 odometers, reused station numbers, Oakhaven totals).

## Stump power (Gate F)
Moderate to high. Two plausible easy routes both land on wrong sets (nine counties; four counties). The correct route needs the cumulative age curve plus a per-vehicle level ratio. The thread classed the step analytical, and reached the golden by applying a judgment the data had to settle (the concavity), not by executing a stated method. Residual risk is a solver split on the unfiled curve family, mitigated because degrees 2 and up agree. The cumulative-curve differencing is a recognised inventory method, so the main thread should weigh it with the scored readers' result.

## Findings, ranked
1. Re-site not judged. After the thread was spawned, stage 4 changed an ask device: the station register no longer carries licensed_since, and the reissue shows as a cross-file conflict and a pause in the number's tests. The coordinator states the main call, NOx figures, write-up figures and station counts are unchanged. At the time of this check, task480/target.zip still held the old register (same md5 as the judged copy, with licensed_since in the header), so neither the thread nor I verified the re-sited bundle or that the 12 station counts still reproduce from it. Ask 4's closure (step 7 of the solution text refers to licensed_since) now needs checking against the new register and the revised write-up.
2. Pilot "retired" test is not filed literally (weakly closed by the CANCELLED definition).
3. Curve family unfiled; main call robust across degree 2 or higher.
4. Optional hardening from the thread: file the WHAT of 3.3 (2027 miles are expected travel in calendar 2027, not the lifetime average); do not file the method.
5. Rubric count and golden realism not verified by this pass.

## Next action for the author
Rebuild target.zip with the re-sited register, then confirm the 12 station counts reproduce from it with the cross-file-conflict reading (Python read of the new register plus the 2024 annual report), and update submission.md step 7 so it no longer cites licensed_since. A re-judge is not needed for the NOx call; one will be needed only if the author wants the re-sited ask 4 independently judged.
