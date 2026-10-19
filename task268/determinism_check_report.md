# determinism-check report, task268, 2026-10-19

Round 1 of architecture 3 (Gullhaven / heart failure survival). This file replaces architecture 2's report (the haddock survey task), overwritten at the coordinator's instruction.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (optional in-house pins on the asks and on the filing of the estimand, none required)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (general-purpose, sonnet, medium) saw only a fresh unzip at /tmp/determinism-check-task268-r1/target/ and the inlined blocks. The charter (3.2) files the estimand: the share of every patient newly diagnosed in 2022 and 2023, including patients the registry no longer follows, alive two years after diagnosis. The judge reproduced the five two-year survivals (65, 67, 69, 72, 73) under the time-varying class-weighted estimator, and an independent class-transition projection gave GUL 65.4, FEN 67.1, BRE 69.3, LIN 73.3: Gullhaven lowest and a 2-point gap under both (unrounded 2.1 and 1.7). The easy routes land elsewhere (KM with moves as censoring, no record = alive, baseline-class stratified KM: Fennick; leavers dropped or counted dead: Wrenhaven). The data separates them: 503 of Gullhaven's 526 movers left from NYHA III or IV, while Wrenhaven's re-consent leavers show no class gradient, so ordinary censoring is right for them. Gate A passes.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cohort 2022 to 2023 | 8,783 | 8,783 (GUL 2,430, WRE 1,703, FEN 1,622, LIN 1,536, BRE 1,492) | yes |
| GUL survival | 65% | 64.9 (IPW), 65.4 (projection) | yes |
| FEN / BRE / WRE / LIN survival | 67 / 69 / 72 / 73 | 67.0 / 69.3 / 72.2 / 73.3 | yes |
| Gap | 2 points | 2.1 and 1.7 | yes |
| KM, moves censored | FEN 67, GUL 70 | FEN 67.2, GUL 69.6 | yes |
| GUL movers, class III or IV | 526; 503 | 526; 503 (82 + 421) | yes |
| WRE re-consent leavers | 942 | 942 | yes |
| GUL move chance at class III / IV | 2.2% / 24.3% | 1.7% / 17% over all visits | not replicated (in-window visits not rebuilt); not graded |
| NT-proBNP tests; at or above 400 | FEN 10,639; 6,991, LIN 8,364; 5,460, BRE 8,704; 5,710, GUL 11,770; 7,723, WRE 9,368; 6,040 | identical | yes |
| 2025 diagnoses; inpatient | FEN 795; 465, LIN 736; 417, BRE 734; 404, GUL 1,222; 723, WRE 833; 494 | identical | yes |

## Competing answers that survived
1. Method for patients whose status the registry no longer holds. The charter files that they count but not how. Readings: no record = alive (FEN 67, BRE 70, gap 3), KM censoring (FEN), baseline-class KM (FEN), leavers dead (WRE), time-varying class adjustment (GUL 65). Only the last uses the class at the reported move, which the visit file carries; the design says the method stays open because the data separates the candidates (fork rows SF4, SF5, SF8 close the semantic terms). A literal grader could dispute the method pick: moderate residual risk, not a surviving defensible alternative.
2. Ask 2 and 3 conventions: a corrected NT-proBNP result re-released under a new accession counts once (raw GUL 11,810 against 11,770), and a 2025 enrolment mapping through the crosswalk to an earlier patient is not a new diagnosis (143 dropped; raw GUL 1,256 against 1,222). Neither is spelled out in a shipped document. Low to moderate risk, asks only.
3. The 364 probabilistic linkage death matches are kept; dropping them leaves Gullhaven lowest.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (pdf 2, csv 6, xlsx 3, txt 2) | yes |
| Large file | 25,000 rows or more | hf_registry_visits 97,172 rows (also ntprobnp 49,471, crosswalk 41,514) | yes |
| Distractors | 2 or more in metadata.json, no file name labels one | echo_lab_activity_2025.xlsx, hf_clinic_sessions_2026.csv; names neutral | yes |
| Distractor weight | unused, relevant enough to weigh; one answering a graded quantity is ruled out | neither answers a graded quantity (echo activity, 2026 clinic sessions); the judge did not use either; not independently stress-tested by me | yes (light check) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | five-hospital, multi-measure; whole percent and nearest point stated; counts have no rounding needed | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | prompt 850 characters, one paragraph; 15 ask figures plus call, gap, components and chart; the 25 count is not computable from the bundle | yes (estimated) |
| Reads as real | no LLM tells | no authoring disclosure seen; coherent timeline; in-fiction pack_contents.txt | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, mechanism informative censoring in a time-to-event estimate, nothing planted ("No decoy" line), difficulty survives on clean data (Gullhaven lowest by 2.2 on the generator truth). The two declared distractors are not the surface read carrying the task; the surface read is KM with moves as censoring (Fennick 67), which is a method, not a shipped artifact. No shipped artifact ranks the candidates wrongly. Gate G: clean, match, no finding.

Gate H: domain: pass (survival and informative censoring are field concepts; the swap test fails to preserve the task), layers: pass (Layer 1: legacy and new record numbers, BRE/BRN code change, mixed NYHA and setting codings, corrected lab re-releases, tri-state lag; Layer 2: class-dependent loss to follow-up), decisive_step: analytical. Matches the design note's Three rules and the card's analyst_test and domain_test.

## Stump power (Gate F)
Good. A strong analyst who cleans the data and reads every rule gets Fennick at 67 with KM, or Fennick again with no record = alive, or Wrenhaven by dropping the leavers; only weighting or projecting by the class recorded at the move gives Gullhaven 65 and the 2-point gap.

## Findings, ranked
1. (Advisory, moderate) The estimator is not filed. The judge accepted the pick because the data separates the candidates and the class at the move is in the visit file, but a very literal grader could dispute it. Optional repair: in the charter, state that the share alive is of the whole cohort and that patients with unobserved status are not assumed alive. File the WHAT only; do not name the method (a named method turns the decisive step into rule application).
2. (Advisory, low to moderate, asks only) The two dedupe conventions in asks 2 and 3 are unfiled. Optional repair: one sentence in the manual or prompt that a corrected result released again counts as one test, and that a re-enrolment of an already-registered patient is not a new diagnosis. Either edit changes solver-visible text and needs a rerun if adopted.
3. (Housekeeping) The GUL class-III and class-IV move chances in step 4 (2.2%, 24.3%) were not replicated by the judge; they are not graded.
4. (Housekeeping) The design note's `## Tried and rejected` section, as read, lists the commuting architecture 1 and seed-world rejections, not architecture 2 (haddock) as the coordinator described; confirm the haddock architecture's retirement line is recorded.

## Next action for the author
Proceed to the pre-ship check and ship; optionally adopt finding 1 (and 2) in the charter and manual and rebuild twice if you want the closed-form insurance.
