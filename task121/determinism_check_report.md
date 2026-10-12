# determinism-check report, task121, 2026-10-12 (pass 1, round 1)

## Verdict
NOT_DETERMINISTIC, on one supplementary answer only (odor_events_2026.xlsx ask 1, the monthly complaint counts). Taxonomy label: `underspecified_objective` (an unfiled counting convention), with Gate A (a false citation in solution step 1), Gate C (a surviving competing answer) and Gate E (the prompt does not pin the count unit). The main recommendation and every other graded figure reproduce and are forced. No SOLUTION_WRONG.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (Ridgeway Organics first, Kestrel Valley Rendering second) is forced: every reasonable hour-matched baseline puts Ridgeway first and Kestrel second, and the other answers need baselines the event-hour distribution rules out. The monthly "complaints logged ... noticed that month" rests on a rule no shipped file states: an app report received twice (same address, same noticed minute, sometimes a different contact_id) counts once. Solution step 1 cites cp14_odor_complaint_procedure_rev4.pdf for that rule, and the PDF contains no such sentence (its only relevant text is "Complaint. One person's report of an odor."). A careful expert can defend either of the other readings below, and all nine cells are exposed.

## Recomputation ledger
All values recomputed by the judge from the round-1 bundle.

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Events May to Sep (boundary filter, 4 outside, all Jan to Mar) | 441 | 441 (227 coordinate keys; golden says 229 households, address-string keys give 230, a unit-formatting difference) | Yes |
| Legacy carry-over rows (OC-26-00007..00045, no 00031) | 38 excluded | 38, all Nov/Dec 2025 | Yes |
| Monthly complaints Jan..Sep, golden convention | 22, 24, 23, 20, 73, 78, 106, 110, 86 (542) | Same only under the unfiled dedupe on address + noticed minute | Only under the unfiled convention |
| Monthly complaints, dedupe only identical contact_id | n/a | 24, 25, 25, 21, 74, 81, 108, 112, 89 | Competing reading |
| Monthly complaints, no dedupe (literal "complaints logged") | n/a | 24, 26, 25, 22, 75, 82, 109, 116, 89 | Competing reading |
| App noticed times in UTC before the April release | Jan and Apr cells | Pattern confirmed from data (+7 or +8 h, then about 0 from May); no shipped file states it (fields file says "Pacific time"); moves two cells by 1 | Yes (data-derivable) |
| Usable hours May..Sep | 743, 670, 740, 738, 717 (3,608) | same | Yes |
| Calm hours May..Sep | 38, 35, 44, 39, 46 (202) | same | Yes |
| Events in calm hours / no usable wind / with direction | 58 / 2 / 381 | same | Yes |
| Upwind counts (landfill, Ridgeway, WPCP, Kestrel, Sutter Bend) | 164, 68, 7, 95, 41 | same | Yes |
| Same-hour expected (landfill, Ridgeway, WPCP, Kestrel, Sutter Bend) | 259.5, 23.5, 15.5, 73.2, 38.1 | 259.5, 23.5, 15.6, 73.1, 38.1 | Yes, to rounding |
| Excess / ratio, Ridgeway | +44.5 / 2.9x | +44.5 / 2.9x | Yes |
| Excess / ratio, Kestrel | +21.8 / 1.3x | +21.9 / 1.3x | Yes, to rounding |
| All-hours ratio, Kestrel / Ridgeway | 2.76x / 0.43x | same | Yes |
| Sixteen-sector counts (PNG) | N 77, NNE 21, NE 140, ENE 1, E 4, ESE 41, SE 0, SSE 0, S 1, SSW 3, SW 51, WSW 16, W 0, WNW 0, NW 0, NNW 26 | same | Yes (4 events within 0.5 degree of a sector edge, minor) |

## Competing answers that survived
1. odor_events_2026.xlsx ask 1, complaints by month Jan..Sep. The golden vector (22, 24, 23, 20, 73, 78, 106, 110, 86) against "dedupe only identical contact_id" (24, 25, 25, 21, 74, 81, 108, 112, 89) and "no dedupe" (24, 26, 25, 22, 75, 82, 109, 116, 89). 26 app pairs share a household and the noticed minute; the second record has a truncated description and about 15 have a different contact_id. The shipped rule that was supposed to close it does not exist in the files: the PDF defines a complaint as "one person's report of an odor" and says nothing of a resend.
2. Minor, optional: "usable wind" hours with calm inside the usable count (743 ...) against a disjoint reading (705, 636, 696, 699, 671). The prompt wording can be read either way.
3. Minor: the app UTC times before the April release move Jan and Apr by 1 each if not converted; derivable from the data pattern.

Main call: none survives. Variants (baseline including the event day, plus or minus 1 hour window, event-free-days baseline, month-matched baseline) all give Ridgeway first (excess +41.3 to +61.4) and Kestrel second (+21.8 to +44.5).

## Spec gates
Run against the round-1 bundle at /tmp/determinism-check-task121-r1/target/target/.

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | Yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, txt, geojson) | Yes |
| Large file | 25,000 rows or more | hfs_met_5min_2026-01-01_2026-09-30.csv, 78,624 rows | Yes |
| Distractors declared | 2 or more in metadata.json, none labelled in a file name | 3 (operator_monthly_reports_2026.xlsx, hfs_pm25_hourly_2026.csv, kestrel_county_airport_hourly_2026.csv); no file name labels one | Yes |
| Distractors relevant, unused, ruled out | same world, none answers the question | Same world as the decision; none ranks the facilities or answers a graded quantity; the operator reports show process changes that do not decide the call; PM2.5 is particles not odor; the airport is outside the valley | Yes |
| Deliverable count | 1 to 3 | 3 (docx, xlsx, png) | Yes |
| Format family | none required | not applied | Yes |
| Asks multi-dimensional | not stacked lookups | 9 complaint months, 5 usable-hour months, 5 calm-hour months, 5 upwind counts, a 16-sector chart | Yes |
| Deliverables present | all named | all three in task121/golden/ | Yes |
| Units and rounding stated | each ask | "Counts are whole numbers" in prompt.txt; hours and counts stated in the asks | Yes |
| Prompt shape and 25-criteria floor | shape identifiable, 25 or more | shape 07; design note counts 34 criteria; prompt.txt is 922 characters, one paragraph, question first | Yes |
| Realism | nothing reads as LLM generated | Judge saw district-system exports (mixed address case and suffixes, truncated app resubmissions, a migration batch, a maintenance log), coherent with the Oct 2, 2026 export; no provenance leak | Yes |
| Determinism of every graded figure | one answer each | Fails on the monthly complaint counts (see above) | No |

## Gate G reconciliation
The judge's line is `mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no`, and it passes Gate G. The card claims `stump_class: analytical`, `gate_g: decomposition_attribution`, `stump_strategy: causal_design`, and an `analyst_test` in which a correct cleaner still files the landfill by counting upwind events or the rendering plant by dividing by all-hours frequency. The two readings match: the judge names the diurnal confound (the upwind indicator confounded by the daily wind regime, fixed by an hour-matched baseline) as the difficulty, and says it would stump on perfectly clean data. The judge did not name any declared distractor as carrying the task. Design note and judge agree on the lures (landfill 164, Kestrel 2.76x, unconverted PST hour collapsing Ridgeway to 34). No mismatch.

## Gate H reconciliation
The judge's line is `domain: pass, layers: pass, decisive_step: analytical`. The card's `domain_test` (odor source attribution from complaint geometry and the local wind record is the air agency's own analysis; the swap test fails for other fields) and `analyst_test` agree, and the design note's Layer 1 list (PST station against local time, held-vane and unplugged-monitor records, the legacy migration batch, app resends, UTC app times) matches the layers the judge named. The judge's one residual risk: the hour-matched baseline is named in no file, and the author should accept that as the intended method-selection stump, not a fork. Consistent with the card's `decisive_rule_filed: false`. No mismatch.

## Stump power (Gate F)
Moderate to good. The lures are the raw upwind count (landfill 164, the largest and the obvious answer), the all-hours chance comparison (Kestrel 2.76x) and, behind both, the unconverted PST/PDT hour (Ridgeway falls to 34). A strong model that notices the complaints fall only between 18:00 and 08:59 and conditions on clock hour lands on Ridgeway, so some strong runs will pass. The Layer 1 hazards (held vane, unplugged monitor, duplicates, legacy batch, UTC app times) mainly stump the supplementary cells. The judge names no too-easy signal and recommends no hardening of the main call; if more is wanted, tighten the asks.

## Findings, ranked
1. odor_events_2026.xlsx ask 1 (the monthly complaints): the duplicate-report convention (an app report received twice counts once, keyed on household and noticed minute) is in no shipped file. File it in cp14_odor_complaint_procedure_rev4.pdf section 3 or complaint_export_fields.txt, or reword ask 1 as "distinct reports, counting an app report received twice once". The golden counts then stand.
2. submission.md Step-by-Step Solution step 1 cites cp14_odor_complaint_procedure_rev4.pdf for the duplicate rule, and the PDF has no such sentence. Correct the citation to the file where the rule is actually filed.
3. Optional: pin that "usable wind" hours include the calm hours, or ask for "usable and not calm", so 743, 670, 740, 738, 717 is the only reading.
4. Optional: state in complaint_export_fields.txt that app noticed times before the April release are UTC (it moves only Jan and Apr by 1), or accept it as derivable from the data pattern.

## Next action for the author
File the duplicate-report convention in the pack (or reword ask 1) and correct the solution step 1 citation, changing nothing in the wind, the events or the main analysis, then rebuild and re-judge once. The design note and submission in the folder may already carry the author's repair; this report judges the round-1 bundle only.
