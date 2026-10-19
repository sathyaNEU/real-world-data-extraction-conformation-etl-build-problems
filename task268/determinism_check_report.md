# determinism-check report, task268, 2026-10-19 (round 2 of architecture 3)

Round 1 (same date): DETERMINISTIC, APPROVE, advisory findings only (estimator not filed, moderate; ask 2 and 3 dedupe conventions unfiled, low to moderate). Round 2 follows the rebuild for the reader's Gate F findings (Brenmoor now 68, Ask B's 2025 counts with a further record-level issue). This file replaces round 1's report.

## Verdict
NOT_DETERMINISTIC (governing label: margin_or_boundary_fragility)
**Disposition:** SEND_BACK (the repair widens a decisive margin or files a method-forcing criterion, both of which change what solvers see; a model rerun is required)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (general-purpose, sonnet, medium) saw only a fresh unzip and the inlined blocks. Every graded figure reproduces under the golden's estimator (hospital-specific, time-varying-class inverse-probability-of-censoring weights): GUL 64.9, FEN 67.0, BRE 67.9, LIN 73.25, WRE 72.2, gap 2.1. But charter 3.2 asks for the share alive at two years including patients the registry no longer follows, which for Gullhaven's 526 movers is unobserved, so the figure is a modelled estimate and no shipped file selects the model. Equally licensed class-adjusted estimators on the same cleaned data give Gullhaven 64.9 to 67.3 against Fennick's steady 67.0 to 67.05, and the gap comes out at 2.1, 0.8, 0.2 or -0.3 points. Gullhaven's lead (about one standard error of the difference, roughly 1.6 points) is inside method noise, and the thread's own claim that class-progression projection "gives the same five figures" (submission step 6) did not reproduce (it gives Gullhaven 66).

Formal reconciliation: the margin rule fails only when the thinness meets real uncertainty, with multiple valid methods whose range straddles the deciding line. Here the lowest-hospital pick holds under every hospital-specific class-adjusted method (IPCW, multi-state, landmark) and flips only under pooled-transition variants and baseline-class weighting, which are weaker choices. That alone I would weigh as a thin-but-mostly-clean call. The gap is the second half of the main ask ("by how many points"), and it is 2, 1 or 0 by method among hospital-specific estimators, with nothing shipped (no standard, selection criterion or filed back-test) to choose among them. The `Current spec` requires the method open only where the design, a standard or a filed criterion forces it, with the data separating candidates; the data here do not separate them. NOT_DETERMINISTIC stands, and since the repair changes solver-visible artifacts, SEND_BACK, not FIX_NOW.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cohort 2022 to 2023 | GUL 2,430; FEN 1,622; BRE 1,492; LIN 1,536; WRE 1,703 | identical | yes |
| GUL movers beyond linkage within 2 years | 526 | 526 (WRE 948 lost, mostly CNR) | yes |
| KM, moves and CNR as censoring | GUL 70, FEN 67 | GUL 69.6, FEN 67.2, BRE 68.0, LIN 73.3, WRE 72.3 | yes |
| GUL move chance at class III / IV | 2.2% / 24.3% | 2.19% / 24.5% | yes |
| Two-year survival, golden method | 65 / 67 / 68 / 73 / 72 (GUL, FEN, BRE, LIN, WRE) | 64.9 / 67.0 / 67.9 / 73.25 / 72.2 | yes, under that one method |
| Gap | 2 points | 2.1 (IPCW), 0.8 (multi-state), 0.2 (landmark), -0.3 (pooled landmark) | only under IPCW |
| Step 6 claim: projection gives the same five figures | same | GUL 66.2 to 66.6, WRE 71.6 to 71.7 | no |
| Ask 2, NT-proBNP | FEN 10,639; 6,991, LIN 8,364; 5,460, BRE 8,704; 5,718, GUL 11,770; 7,723, WRE 9,368; 6,040 | identical | yes, all ten |
| Ask 3, 2025 diagnoses; inpatient | FEN 795; 465, LIN 736; 417, BRE 734; 404, GUL 1,222; 723, WRE 833; 494 | identical | yes (with the stated reading, below) |

## Competing answers that survived
1. Estimator of the deciding quantity (main call and Ask 1). Two answers on the gap and Gullhaven's whole-percent figure: 65 and 2 points (hospital-specific IPCW) against 66 and 1 point (continuous-time multi-state) or 67 and 0 points (landmark); the lowest hospital flips to Fennick under the pooled variants and baseline-class weighting. The shipped rule meant to close it: none (the design's ladder asserts separation among its own rungs, but the later methods are not on it and nothing filed selects among them).
2. Ask 3 diagnosis date. 208 rows carry a diagnosis date after the enrolment date, 95 dated 2025 but enrolled in 2024 with an HF24- id. Read as written, the counts are BRE 756, FEN 811, GUL 1,244, LIN 750, WRE 854. The golden takes the enrolment date for those rows. Manual 2.1 (diagnosis precedes entry) and the id prefix close it only by inference.
3. Wrenhaven's CNR leavers as ordinary censoring: KM 72.3, multi-state 71.7, landmark 71.6; all round to 72. No effect on the pick.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, txt) | yes |
| Large file | 25,000 rows or more | visits file 97,172 rows (also ntprobnp, crosswalk) | yes |
| Distractors | 2 or more, in metadata.json, not labelled by file name | echo_lab_activity_2025.xlsx, hf_clinic_sessions_2026.csv; neutral names | yes |
| Distractor weight | unused; relevant enough to weigh | not used by the thread's recomputation; not independently stress-tested by me | yes (light check) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx) | yes |
| Asks | multi-dimensional, unit and rounding stated | five-hospital multi-measure; whole percent and nearest point stated | yes |
| Prompt shape and rubric | 25 or more criteria | one paragraph, 850 characters; 25 not computable from the bundle | yes (estimated) |
| Reads as real | no LLM tells | none seen; dates coherent with the 14 April 2026 pack | yes |
Hygiene is clean: nothing exclusion-level. The determinism gates (A partly, C, margin) are the failures.

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note and card say the same (stump_class analytical; the surface read is KM with moves as censoring, a method rather than a shipped artifact; the two declared distractors do not carry the task). Match, no Gate G finding. Gate H: domain pass, layers pass, decisive_step analytical, matching the note's Three rules (Layer 1: legacy and new record numbers, code changes, tri-state and Florida death sources, corrected lab re-releases; Layer 2: class-dependent moves). The note's analyst test (a strong analyst runs KM and names Fennick 67 against Gullhaven 70) reproduces. The mismatch the send-back rests on is not Gate G or H but the note's closure: its fork table treats the estimator as closed by the ladder (R4), where the thread finds valid sibling estimators the ladder does not carry.

Realism items applied after the thread's unzip (two diagnosis dates after a death, 29 relocations after a consent withdrawal, specimens after death or move) leave every graded figure unchanged and do not bear on these findings; they were not part of the thread's pack, so the next pass must unzip the rebuilt target.zip fresh.

## Stump power (Gate F)
Good, and not the problem. KM on the cleaned data names Fennick (or Wrenhaven if movers are dropped or counted dead); only class-adjusted handling reaches Gullhaven. The weakness is too open, not too easy: even the intended insight does not yield a single number.

## Findings, ranked
1. (Blocking) The gap and Gullhaven's whole-percent figure are not forced: hospital-specific class-adjusted estimators give a 2.1, 0.8 or 0.2 point gap, and some pooled variants flip the lowest hospital. Gullhaven's lead is about one standard error. Gates C and the margin test fail on the main call.
2. (Blocking, same cause) Submission step 6 claims the class-progression projection gives the same five figures; it did not reproduce (Gullhaven 66, Wrenhaven 71.6 to 71.7). Drop or substantiate it.
3. (Should fix) Ask 3 turns on an inferred reading of 208 diagnosis-after-enrolment rows. Close it in the manual or repair the dates.
4. (Advisory) Carried from round 1: nothing files the estimand's treatment of unobserved status beyond "counts"; file the WHAT, never name the method.

## Next action for the author
Redesign the margin, not the wording: either widen Gullhaven's real deficit so it leads under every hospital-specific class-adjusted estimator and rounds to the same whole percent and gap (with Fennick unchanged), or file a selection criterion the estimators can be held to (for example a filed out-of-sample back-test that the data resolve; never the method by name, never consecutive builds). Correct step 6, close the Ask 3 date reading, rebuild twice, and run one fresh determinism pass on the new target.zip.
