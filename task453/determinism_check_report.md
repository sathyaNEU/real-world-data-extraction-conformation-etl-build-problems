# determinism-check report, task453 (architecture 2), 2026-10-14

Pack judged: the target.zip as of the first unzip (scratch /tmp/determinism-check-task453-r1/target/). The generator was being repaired during this pass: the CAI cells file in that unzip is 2,121,904 bytes, and `metadata.json` and the current `target/` record 2,121,188 bytes. This report applies to the judged pack, and the re-judge after the repair is a separate pass.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (the CSV precision and base in ask 6, a prompt sentence or a stated grading tolerance; the main call, the stump and the data stay frozen)
**Stumping type:** mechanism: method_or_model_selection (interview-mix confound; etl_conformance for the CSV), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The restated trigger of 6.5 reproduces from the shipped cells under the design the data select. The cells show a first-interview bias of +1.30 points on the previous questionnaire. The interview-by-interview effects average 0.4921 (0.49 to 0.52 across every estimator variant tried). A common-effect model with interview number held fixed fits worse (weighted RSS 2.10M against 1.76M) and gives 0.31 to 0.34, a trigger of 6.3. The Act (s.7, s.8, s.9(2), s.10) and the methodology note supply every rule. Four regions are designated at 6.5, and North Coast misses by 0.04. Every literal fork tested closes (SF2 to SF14).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Table 2 and Table 3 vs the CAI and ICS cells, 60 months | equal | max diff 0.0 after the concordance and the six-group average; Table 1 matches | yes |
| First-interview bias, CAI | 1.3 | +1.305 (interviews 1 to 6: +1.305, +0.146, -0.106, -0.290, -0.471, -0.584) | yes |
| Change in the published rate | +0.4921, +0.5 | 0.4921 (region level, LF-weighted); 0.4900 national; 0.512 unweighted; 0.49 to 0.52 across variants | yes |
| Common-effect change | 0.3 to 0.4 | 0.31 to 0.34 (trigger 6.3) | yes |
| July to November 2025 group gap | 1.2 | 1.18 national, 1.19 regional (trigger about 7.2) | yes |
| 2026 averages, Table 2 | ER 6.61, WC 6.63, RD 7.45, HL 8.33, NC 6.46 | 6.608, 6.633, 7.450, 8.333, 6.458 (cells unrounded: 6.594, 6.638, 7.449, 8.330, 6.444) | yes |
| Q4 2026 responding dwellings | 91,459 total; Capital 16,343, Harbour 12,336, North Coast 9,866, Inland Plains 10,982, Eastern Ranges 8,170, Southern Valleys 9,328, Western Coast 7,511, River Delta 10,367, Highlands 6,556 | identical (113,280 dwellings in all; distinct dwelling_ref alone gives 74,997; response contacts 182,138) | yes |
| CSV rates, 324 rows | to two decimals | the pre-July 2025 and 2026 rows reproduce under published plus 0.5 and as published. The 45 July to November 2025 rows depend on the estimator and can differ by 0.005 to 0.017 | partly (finding 1) |

## Competing answers that survived
- Main call: none. The group gap (7.2, River Delta and Highlands) and the common effect (6.3, adds North Coast) are both rejected by the data and by s.9(2) and the note.
- Ask 6, July to November 2025 rows: per-interview effects from equally rigorous estimators (national or regional, weighted or unweighted) differ in the second or third decimal. No filed rule fixes the estimator.
- Ask 6, other rows: the base is published one-decimal plus 0.5, or unrounded cells plus 0.4921. They differ by up to about 0.05.
- Ask 4: the all-three-months reading of "responded in Q4" is not licensed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | CAI cells 72,090; contacts parquet 254,880 | yes |
| Distractors | 2 or more named in metadata.json, none labelled in a file name | 3: population_benchmarks, seasonal_factors_2027_projected, response_rates; none labelled by name | yes |
| Distractor quality | unused by the solution, relevant enough to weigh, a shipped fact rules it out | per the thread unused by the solution; the design note says they carry no change; the thread did not read metadata.json, and none of the three answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (a PDF and a CSV), both in the golden | yes |
| Asks | multi-dimensional, unit and rounding stated | six asks. The prompt gives one decimal for the trigger and the change and two for the CSV. The dwelling counts are whole numbers | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | shape recorded as other; 6 asks, 9 regional counts and 324 CSV rows give well over 25 criteria. The rubric is not shipped, so this is not verified | yes (not verified) |
| Not LLM generated | nothing reads as LLM generated | thread: operational artifacts, no authoring language; goldens not read by the thread | provisional, left to realism sweep |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card has `gate_g: method_or_model_selection`, `stump_class: analytical`, and the design note's decisive step is the same interview-by-interview comparison. They match. The card's mechanism, stumping_family, surface_read_dependency and sole_data_defect fields are None, so only the gate_g line could be compared. The thread did not name a declared distractor as the surface read, so the distractors are not too load-bearing. The thread's two competing routes (the group gap and the common effect) are the design's analyst_test routes (7.2, then 6.3 or 6.4).

## Stump power (Gate F)
Moderate to good. Both easy routes are plausible for a strong analyst who has cleaned the data correctly. The risk is that a capable model finds the interview-number bias in the CAI cells and fits the interview-by-interview design. Ask 6 then separates solvers at the second decimal (finding 1). The change of 0.49 sits 0.04 above the 0.45 rounding edge and no variant crosses it, so the margin is thin but clean.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. This matches the design note's `## Three rules` (estimand_identification, the right comparison group). The swap test fails for hospital nouns, because there is no rotation group, first-interview bias or dependent interviewing. Layer 1 is the 2019 to 2025 renumbering, the CAI and ICS layouts, the six-month overlap and the reused sample reference. Layer 2 is estimating the redesign effect interview by interview.

## Findings, ranked
1. (Medium, ask 6 only.) The 45 July to November 2025 CSV rows need per-interview effects, and equally rigorous estimators differ by 0.005 to 0.017 at the second decimal. The prompt says only "two decimals". If the rubric grades them exactly, a correct solver can miss.
2. (Low to medium, ask 6.) The base of the pre-July 2025 and 2026 rows is published one-decimal plus 0.5 in the golden. Recomputing from unrounded cells, or adding 0.4921, differs by up to about 0.05.
3. (Low, ask 4.) The dictionary calls dwelling_ref a "sample reference" and does not say it is reused when a rotation group is replaced. The derivation is available from interview_no and note s.1, and "each dwelling once" points at it. This is data semantics inside an ask, which is allowed.
4. (Note.) The pack judged is not the pack now on disk: the CAI cells byte count differs from metadata.json. After the repair, a FIX_NOW is re-judged once, and this report records the earlier pack.
5. (Note.) The thread did not read metadata.json, so provenance and license were not audited by it. The metadata records CC0 for every file.

## Next action for the author
Close finding 1 and finding 2 without filing the method. Add one sentence to ask 6 that files the WHAT, for example "from the published one-decimal series, to two decimals, with the July to November 2025 rows graded within 0.02", or set that tolerance in the rubric. Optionally add a clause to ask 4 saying a dwelling is a sampled household in its entry month, not a sample reference (this closes finding 3). Then rebuild and re-judge once.
