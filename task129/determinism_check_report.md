# determinism-check report, task129, 2026-10-14

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (run 1791956919, one pass, fresh unzip of target.zip, sha256 ce015bb4...) recomputed the main call and every memo and workbook figure from the bundle. The call is forced: North's 2025 rise sits at every time since trim and climbs with the ash share within falling distance. Garrity's and Hollenbeck's North units fail at 0.98 and 1.01 of expected, East's past-cycle units and South's windier 2025 are small. One fork survives, on the workbook's major-event-day ask only: the files never say that a second ticket on a device already out folds into that device's open outage. The main call, the memo rates and the dates of the major event days do not move under either reading.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cooperative rate 2025 | 21.9 | 21.92 | yes |
| Cooperative rate, mean 2021-23 | 11.2 | 11.17 (11.75, 11.59, 10.18) | yes |
| North rate 2025 / 2021-23 | 30.2 / 11.1 | 30.21 / 11.1 | yes |
| Major event days 2025 | 18 Jun, 9 Dec | 18 Jun, 9 Dec (same folded or not) | yes |
| MED takeout North (outages / members / cust-min) | 160 / 5,956 / 1,821,820 | same when folded; 182 / 6,698 / 2,008,298 unfolded | yes, folded only |
| MED takeout East | 122 / 3,511 / 1,193,712 | same when folded; 135 outages unfolded | yes, folded only |
| MED takeout South | 112 / 3,598 / 1,150,972 | same when folded; 128 outages unfolded | yes, folded only |
| End-2025 miles N / E / S | 1,773.3 / 1,237.8 / 1,138.3 | 1,773.289 / 1,237.807 / 1,138.310 | yes |
| Hollenbeck billed miles Q1-Q4 | 66.5 / 80.9 / 84.4 / 56.6 | same (credit memos take the reversed invoice's service_month) | yes |
| Garrity billed miles Q1-Q4 | 94.7 / 136.3 / 114.9 / 178.5 | same (linear feet / 5,280) | yes |
| North rise on units under 2 years | 18.8 | about 19.5 (under 2 years), about 19 (2-4 years) | yes, same size as late cycle |
| Contractor test | 0.98 / 1.01 | 0.98 / 1.01 | yes |
| Ash gradient, North 2025 | rises with ash share | 12.3 / 17.3 / 23.8 / 43.2; flat 10.4-11.4 in 2021-23 | yes |

## Competing answers that survived
- xlsx ask 2 (district outages, members and customer-minutes taken out by the major event days): fold a second ticket on a device already out into its open outage (160 / 122 / 112 outages) or count every outage_id (182 / 135 / 128). Policy 2.1 ("one device opening") reads as folding, but no file uses the word "storm-mode" or states the folding, and the data dictionary is silent. The design note's fork table has no row for it (SF3 closes only restoration steps). The call is unaffected, so this is a supplementary-answer fork.
- Minor: the retirement-date boundary in the averaged miles moves no one-decimal rate (SF2).
- Re-bid, catch-up and nothing new are all closed by the data (age-standardised contractor test, North has almost no past-cycle units, weather is small).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, docx, parquet) | yes |
| Large file | 25,000 rows or more | parquet 168,644 rows; OMS export 30,934 rows | yes |
| Distractors named in metadata.json | 2 or more, none labelled by file name | statewide_cooperative_reliability_2020-2024.csv, ami_momentary_events_2025.csv; no file name labels one | yes |
| Distractors unused yet weighable | yes | judge also counted weather as a minor driver, not a distractor; the statewide and momentary files are relevant, unused by the solution and ruled out by shipped facts (sustained, cause and district definitions) | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | contractor x quarter, district x three measures, district miles; prompt gives one decimal for rates and miles | yes (counts and customer-minutes carry no stated rounding, they are integers) |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 07; call, two rates, 8 billing cells, 9 takeout cells, 3 mileage cells, and the components give more than 25 | yes |
| Reads as real | no LLM tells, goldens realistic | no authoring disclosure found by the judge; golden realism not re-read by me | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: Gate G and stump_strategy decomposition_attribution, Layer 2 family estimand_identification, stump_class analytical. The mechanism matches. The family names differ in label only (a correct rise attributed across time since trim, contractor and species, versus the right comparison group for it); the substance agrees. The thread did not name the declared distractors (statewide file, AMI momentary events) as the surface read carrying the task, so they are not too load-bearing. The wrong-answer routes the thread saw (re-bid from the handover, catch-up from East) are the card's analyst_test route, as intended.

Gate H line: domain pass, layers pass, decisive_step analytical. Matches the design note's Three rules (domain test: regrowth clock and ash within falling distance; no decoy, not semantics, not rule application). Layer 1 is the folding, units, credit memos and species codes; Layer 2 is the age-standardised attribution.

## Stump power (Gate F)
Moderate. The easy route reads Garrity's 2024 takeover of North as the cause and files a re-bid, or files catch-up from East's handover. The same-age contractor test (0.98 / 1.01), the shift at every time since trim and the ash gradient defeat both. Policy section 6 maps the driver to the programme, so the last step is easy once the driver is found.

## Findings, ranked
1. Fork on xlsx ask 2: the folding of a second ticket on a device already out is unfiled. The golden holds only under folding (160 / 122 / 112); the literal reading without it gives 182 / 135 / 128. The design note's closure for the folding rests on its zero-counts assertion for the main population, not on a filed sentence, and it has no fork-table row.
2. Minor: the stumping_family label differs between thread and note (no substantive conflict).
3. No finding on the main call, the distractors or the spec gates.

## Next action for the author
File the WHAT in policy 2.1 and the data dictionary's outage_id line: a ticket for a device already out belongs to that device's open outage and is not a separate outage (population only, not a procedure), add the fork-table row asserted in checks.py, rebuild once and re-judge once; the main call and every graded figure stay as they are.
