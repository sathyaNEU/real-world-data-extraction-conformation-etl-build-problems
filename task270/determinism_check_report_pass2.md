# determinism-check report, task270, 2026-10-28 (pass 2)

Run id p2172304, target.zip sha256 prefix 8e02e3d3, one thread (general-purpose, sonnet, medium) judging cold. Raw verdict: /tmp/determinism-check-task270-p2172304/verdict.md

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, guidelines 3.1 to 3.4 give life expectancy at 85 below seven years for Windermoor 6.6, Coldwater Plains 6.8, Dunesford 6.9 and Saltwick Shoals 6.9. Every other area is 7.1 or higher (Cobbleton 7.1 is the nearest). All twelve life expectancies, all twelve visit counts and all twelve resident counts reproduced from the shipped files. The only place the text is silent is how to obtain single-year population at 85 to 94 and 95 and over inside the published 85-and-over ERP. The data separates the candidate estimators: the cohort rebuild reconciles to the shipped 85+ ERP within 1.5 percent (ratio 0.985 to 1.007 in every area), and the census-split and NSW-shape routes do not respect the shipped ERP.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Deaths 85+, 2024 to 2026 (BDM csv + interstate xlsx, via ASGS SA2 to LGA) | 7,485 | 7,485 (per-area counts all match) | yes |
| Thistlebank SA2 remap (guidelines s4) | Wolfram Ranges | 525 BDM rows remapped | yes |
| Denominators (census cohorts, 41/365 split, deaths removed, scaled to ERP) | rebuilt | ratio to ERP 0.985 to 1.007 | yes |
| Life expectancy at 85, 12 areas | 6.6 / 6.8 / 6.9 / 6.9 qualifiers, others 7.1 to 7.5 | 6.588, 6.819, 6.876, 6.919, 7.122, 7.190, 7.227, 7.295, 7.309, 7.385, 7.423, 7.477 | yes, all 12 to 1 dp |
| Visits 2026, 85+ (overlap-merged, local arrival date) | 1,002 / 340 / 278 / 839 / 1,156 / 568 / 630 / 393 / 1,109 / 828 / 212 / 304 | same | yes, all 12 |
| Distinct residents (client_key via external_id) | 697 / 233 / 211 / 592 / 829 / 407 / 471 / 281 / 797 / 596 / 151 / 229 | same | yes, all 12 |

## Competing answers that survived
None on the main call. Competing readings tested:
- Census 2021 85+ shares applied to each ERP: Windermoor, Coldwater, Spraymouth qualify (Dunesford 7.04, Saltwick 7.22 do not). Wrong set, closed by the data (coast cohorts that turned 85 after census night; Spraymouth 85+ ERP falling).
- NSW single-year shape on LGA 85+: Windermoor only. Same closure.
- NSW shape adjusted by local census structure: Windermoor, Coldwater, Spraymouth.
- Cohorts aged by whole years with deaths removed: same four areas as golden (6.59, 6.83, 6.89, 6.92).
- Cohorts aged with death attrition ignored: Dunesford and Saltwick fall out. Closed by the ERP reconciliation.
- Ask-level forks, confined to asks 2 and 3 (asks are free of rules): "visit" has three counts (rows 1069, case_ref 923, merged 1002 for Bannockvale), separated by a bimodal within-case gap structure (overlap of at least 5 minutes, or return of at least 60 minutes, nothing between). Raw client_key gives 750 against 697 linked through external_id. No shipped file defines "visit" in so many words. Residual fragility noted: Dunesford (6.876) and Saltwick (6.919) sit 0.08 to 0.12 under the line, stable to 0.02 under the rebuild's own conventions.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | csv x5, xlsx x3, pdf x1 | yes |
| Large file | 25,000 rows or more | bdm_death_registrations 73,066 rows | yes |
| Distractors named in metadata.json (key `distractor_files`), no file name labels one | 2 or more | 3: erp_nsw_single_year, residential_aged_care_services, falls_injury_hospitalisations; names neutral | yes |
| Distractors unused and relevant | weigh but ruled out | NSW single-year shape reproduces a graded quantity (Windermoor only) and the shipped ERP rules it out; aged care and falls unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12-area cells for visits and residents plus life expectancy to 1 dp; prompt states years to one decimal and whole numbers | yes |
| Prompt shape and 25+ criteria | identifiable, 25 or more | scorecard against a threshold; 12 x 3 cells plus chart parts, design note ladder counts 40 ask criteria; rubric not independently generated here | yes (by design note count, not re-derived) |
| Reads as real, not LLM generated | yes | thread saw real ABS-style structure, no provenance leak; golden xlsx and png present | yes (the thread did not open the xlsx or png goldens) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical, stump_strategy composition_mix, official_decoy false, validated_decoy false. Match. The thread did not name the declared distractor (NSW single-year ERP) as the surface read carrying the task; the easy route it names is the census split of the published ERP, which is the card's analyst_test route. The distractor is not too load-bearing.

## Gate H reconciliation
Thread: domain pass, layers pass (Layer 1: Thistlebank reassignment, interstate registrations, revised and preliminary ERP, DST, system-change ids; Layer 2: single-year denominator estimation and life table), decisive_step analytical. Design note `## Three rules` (No decoy, Not semantics, Not rule application) and card analyst_test and domain_test say the same: the census split names Coldwater, Spraymouth and Windermoor against the golden four. Match, no mismatch.

## Stump power (Gate F)
Good. The easy route splits the 85-and-over ERP by the 2021 census (or NSW) ages and names three areas (or one), wrongly including Spraymouth and excluding Dunesford and Saltwick. The guidelines do not say the denominator must be rebuilt by cohort with death attrition; only the data do. Caveat for the main thread against the design note's ladder: the cohort rebuild is a recognisable demographic method and the thread itself calls some strong models likely to take the census split, so the ladder's expectation that at least one of the top two is off the call stands on that route being tempting, not on it being hidden. The design note records a pair ceiling of 43.6 for the cracker with the call.

## Findings, ranked
1. None blocking.
2. Minor, ask-level: "visit" is not defined in a shipped file and is resolved by the data's gap structure and the asking sentence. The thread judged it confined to the asks and recommends no change. Not required.
3. Minor: Dunesford and Saltwick qualify by 0.08 to 0.12 years; stable under the rebuild's conventions.

## Next action for the author
Ship: no repair needed. Proceed to stage 5 on target.zip 8e02e3d3 once the leak reader's pass is also clean.
