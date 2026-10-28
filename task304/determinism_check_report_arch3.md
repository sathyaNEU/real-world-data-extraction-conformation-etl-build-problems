# determinism-check report, task304, 2026-10-28

Architecture 3 (re-rooted after architecture 2's portal FAILED_TO_STUMP). target.zip sha256 prefix
`6ccd2099db2bb961891739ae5d575698286fae3f2191c13e88b83806008ecffc`.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread (fresh unzip of `target/`, no access to submission.md, DESIGN_NOTE.md, metadata.json, generator/ or golden/) independently reproduced every figure in CRITICAL_COMPONENTS, every SOLUTION_STEPS figure, every SUPPLEMENTARY_ANSWERS cell in both deliverables, and the FINAL_RECOMMENDATION margin (Fenwold Recovery 70 vs needle exchange pharmacies 50). The decisive step is two independent forward-looking corrections to a 2026 screening yield carried naively to 2027: (1) PH-12's pharmacist test-and-treat rollout drags citywide pharmacy yield toward the three-pharmacy depleted rate (0.025 vs 0.168), and (2) 737 of 905 hostel residents were already tested in 2026, so the hostel pool in 2027 is mostly the untested residue plus arrivals, not the full census. Both corrections are forced by joins across shipped files (register, van tests, ICB commissioning PDF, resident lists), never by a planted defect, a hidden rule, or a semantic reading. Gates A-E all passed in the judge's independent reconstruction; no competing defensible answer survived.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pharmacy depletion rate (3 pharmacies) | 0.025 | 3/120 = 0.025 | Yes |
| Pharmacy rate, other 21 | 0.168 | matches | Yes |
| Hostel residents tested in 2026 | 737 of 905 | matches (two-sheet xlsx join) | Yes |
| Start-within-84-days shares (AP/HH/DS/NSP) | 0.50/0.81/0.62/0.72 | 0.500/0.811/0.618/0.702 | Yes |
| 2027 pool sizes (AP/HH/DS/NSP) | 102+485 / 905+264 / 1,872 / 1,861 | exact | Yes |
| Hostel negative-resident incidence | 2 in 1,559 person-years | 2 in 1,559.2 | Yes |
| Found, nearest 10 (AP/HH/DS/NSP) | 40/50/110/70 | 40.4/49.9/111.3/68.8-70.1 | Yes |
| Started, nearest 10 (AP/HH/DS/NSP) | 20/40/70/50 | 20.2/40.4/68.7-68.8/48-50 | Yes |
| Clinic cures, 5 clinics x 2 half-years (10 counts) | 66/35, 44/36, 38/29, 21/23, 18/23 | all 10 exact (course chains via migrated_from, last dose + 27 days, RNA Not detected >=84 days) | Yes |

## Competing answers that survived
None at the committed figures. Two candidate wrong answers exist by design and are explicitly closed by shipped facts:
- Naive 2026-yield-forward (no correction): needle exchange pharmacies win at ~130 starts. Closed by PH-12 (every pharmacy reaches test-and-treat from 1 April 2027) plus the register showing the three early-adopter pharmacies' depleted 0.025 yield.
- Rollout correction alone (no hostel correction): city hostels win at ~110 (or ~80 on the resident lists alone). Closed by the person-level join of the resident lists to the van's 2026 test log (737 of 905 already tested).
Both forks are named and closed in the design note's Ladder and Semantic fork table (SF1-SF20); the judge, working blind, reconstructed the same two forks independently and confirmed both are closed by shipped facts, not by an unpinned convention.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 16 | Yes |
| Format mix | >=3 | csv, pdf, xlsx (3) | Yes |
| Large file | 1 file >=25,000 rows or large DB | virology_hcv_results, 42,381 rows | Yes |
| Distractors named, unlabeled | >=2 named in metadata.json, none in a file name | van_fibroscan_sessions_2026.xlsx, van_running_costs_2026.xlsx; neither name says "distractor" | Yes |
| Distractors relevant, unused | each weighable, unused by solution | fibroscan (liver staging) and running costs (budget) are both plausible things an analyst would reach for in this exact decision and neither is used in solution_steps | Yes (soft sub-item -- no distractor arithmetically reproduces a graded figure that a shipped fact then rules out; this is optional framing, not a floor, and is not a finding) |
| Deliverables | 1-3, present in golden, no format family required | 2 (`van_2027_trustee_paper.docx`, `clinic_cures_2024-25.xlsx`), both present in `golden/` | Yes |
| Asks multi-dimensional | not stacked lookups, unit+rounding stated | 4 settings x 2 metrics + chart; 5 clinics x 2 half-years; "round people to the nearest ten and give cures as whole counts" stated in the prompt's last sentence | Yes |
| Prompt shape / rubric | shape identifiable, rubric >=25 criteria | shape "09" (metadata.json); 18 numbered figures (8+10) plus the setting, the chart and the recommendation/critical-components weighting plausibly clears 25, but no rubric artifact is present in this repo to count directly | Not independently verifiable from this folder; flag for the author to confirm at rubric generation |
| Realism / LLM-generated | nothing reads as LLM generated, goldens read as real work product | judge found tablet-sync duplicates, a clinic-code migration, inconsistent referral-source spellings, mixed date formats, a two-sheet offset workbook; no boilerplate, no round numbers, no authoring disclosures | Yes |

## Gate G reconciliation
Judge: `mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Judge's Gate H: `domain: pass`, `layers: pass`, `decisive_step: analytical` -- the decisive step is recognizing the hostel yield came from a first (prevalent) round of a standing population, so only the untested residue and arrivals carry 2027 yield, together with the pharmacy rollout.

Design note / card (`.claude/skills/fingerprint/cards/task304.json`): `stump_class: analytical`, `gate_g: forecasting`, matching `analyst_test` and `domain_test`. The card's `analyst_test` names the identical two-rung ladder the judge reconstructed blind (naive -> pharmacies ~130; rollout-only -> hostels ~110/80; both -> Fenwold Recovery ~70), and `domain_test` names the same field-specific quantity (a screening programme's yield, falling after a first round and after a competing service absorbs the pool) that the judge's swap-test reasoning independently reached.

This is a clean match: the judge did not name either of the two declared distractor files (fibroscan sessions, running costs) as carrying the stump, and did not class the decisive step as planted, data-semantics, or rule-application. No mismatch finding. One bookkeeping note, not load-bearing: the card's own `answer` field (`"the needle exchange pharmacies' new registrants, about 50 ... Fenwold Recovery's new entrants next at about 30"`) is stale from an earlier architecture and disagrees with the current golden (Fenwold Recovery 70 vs pharmacies 50); and `DESIGN_NOTE.md` line 48 still names an old deliverable filename (`van_2027_funnel.xlsx`) superseded by `clinic_cures_2024-25.xlsx` everywhere else (prompt.txt, submission.md, metadata.json, golden/). Neither is shipped to a solver and neither affects the verdict.

## Stump power (Gate F)
Two independent, non-obvious corrections are each individually load-bearing (removing either one flips the winner), and both survive on honest, correctly-reported numbers -- a genuine forecasting shape, not surface-read-rejection. The judge rates this as real stump power: a model that extrapolates either rate naively lands on a specific, provable wrong setting (pharmacies or hostels), not a coin flip. This matches the design note's Ladder, which shows every single-correction rung landing off the golden and only the conjunction reordering the head (margins 1.21-1.90 printed units off-call, 1.39 on-call).

## Findings, ranked
1. (Informational, non-blocking) `DESIGN_NOTE.md` line 48 still names `van_2027_funnel.xlsx` as a deliverable; the shipped deliverable is `clinic_cures_2024-25.xlsx` everywhere a solver or grader would see it (prompt.txt, submission.md, metadata.json, golden/). Fix location: solution (design note housekeeping only; not solver-facing, no rerun implicated).
2. (Informational, non-blocking) The fingerprint card's `answer` field is stale from an earlier architecture (names pharmacies ~50, Recovery ~30) and disagrees with the current golden (Recovery 70, pharmacies 50). Fix location: solution (card bookkeeping; `status.py`/`register` metadata only, no rerun implicated).
3. (Informational) The rubric criteria count (>=25) could not be verified directly from this folder because no rubric artifact is present in the repo; the prompt shape (18 numbered figures plus setting, chart, cures grid) plausibly clears it but this should be confirmed at rubric generation / portal time.

No gate failure, no Gate G or Gate H mismatch, no determinism defect found.

## Next action for the author
None required to ship architecture 3; at convenience, update `DESIGN_NOTE.md` line 48's deliverable name and refresh the fingerprint card's stale `answer` field to match the current golden (Fenwold Recovery 70 vs pharmacies 50), as pure bookkeeping with no rerun implication.
