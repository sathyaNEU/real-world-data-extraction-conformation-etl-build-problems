# determinism-check report, task119, 2026-10-10

**Run note.** This workflow environment exposed no `Agent` tool, so the judge was run inside the orchestrator under strict sequencing rather than as a spawned thread.
- **What the judge saw:** `prompt.md`, the blocks extracted from `submission.md`, `guidelines/determinism_judge_system_prompt.md` (v3) and a fresh copy of `target/` at `/tmp/determinism-check-task119-20261010T021721Z/target/`.
- **What it never opened:** the generator, any answer key, `solver_rounds/` and `pipeline.json`.
- **Sequencing:** its verdict was written to `/tmp/determinism-check-task119-20261010T021721Z/verdict.md` before `metadata.json`, `DESIGN_NOTE.md`, `golden/` or `leak_check_report.md` were opened, and it was not edited afterwards.
- **No pre-run contamination:** the orchestrator's information before the verdict was the same as a spawned thread's would have been.
- **Re-run if you want independence:** re-invoke in an environment with `Agent` if you want a thread that is independent of the orchestrator.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The terms of reference fix the objective:
- WRHB/26/097 s.3 counts deaths confirmed avoidable "because of problems in the reviewed trust's own care".
- s.4 says "A trust's decisions about the use of its own beds and staff are part of its own care".
- s.5 places the review on the latest four complete quarters, which is July 2025 to June 2026.

Rebuilding each own unit's census minute by minute gives these results:
- **Stennock:** all 27 remit deaths followed waits during which its unit held one or two staffed beds, assigned that morning to its own planned surgical patients who were still in theatre recovery.
- **Prideswick:** 15 deaths followed waits beside its own unassigned staffed bed.
- **Ristenholm:** the beds it freed during its waits went to other trusts' transfers, allocated by the network bed bureau (field guide `bed_confirmed_at`; ACCN/23/41 s.3).
- **Brackenford:** its unit was full at every minute of every long wait.
- **Lathingbury, Tannerby, Ellerdyke, Pellowham:** no level 3 unit in the placement year.

Stennock is forced, 12 deaths clear of Prideswick, on a margin with no estimation freedom. All gates A to E pass. There is no taxonomy failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Main call | Stennock | Stennock (27 v Prideswick 15) | yes |
| docx 1: trust | Stennock | Stennock | yes |
| docx 2: deaths a year of review could confirm | 27 | 27 | yes |
| docx 3: runner-up | Prideswick, 15 | Prideswick, 15 | yes |
| docx 4: gap | 12 | 12 | yes |
| CC1: Lathingbury remit deaths, no L3 beds | 56, none | 56; LAT-HDU care_level 2 in `acc_unit_register.csv` | yes |
| CC2: Stennock deaths all after held-bed waits | 27 of 27 | 27 of 27 (15 with one held bed, 12 with two; assigned 08:00 to 12:59 the same day; held 14 to 201 min). All 92 Stennock long waits had a held bed, and none fell at a weekend | yes |
| CC3: Prideswick deaths beside own empty staffed bed | 15 | 15 (free bed for 254 to 361 min of each wait; 2 bureau, 4 full) | yes |
| CC4: Stennock lead | 12 | 12 | yes |
| Step 2: placement-year remit deaths | 213 | 213 (193 admitted, 20 died before admission) | yes |
| Step 4/5: Ristenholm own-care deaths | 2 | 2 (35 waits had beds go to other-trust bureau transfers, 7 were full throughout) | yes |
| Step 4/5: Brackenford own-care deaths | 0 | 0 (0 free minutes in 35 waits; 118 of 118 long waits began 18:00 to 23:59) | yes |
| png 1: bars STN, PRW, RIS, LAT, BRK, ELL, TAN, PEL | 27, 21, 44, 56, 35, 13, 10, 7 | 27, 21, 44, 56, 35, 13, 10, 7 | yes |
| png 2: confirmable shading | 27, 15, 2, five at 0 | 27, 15, 2, five at 0 | yes |
| png 3: order | STN, PRW, RIS, then the five at 0 | same (the order among the five at 0 is unpinned) | yes |
| png 4: gap marked | 12 | 12 | yes |
| png 5: title names Stennock | yes | golden title "Stennock: 27 deaths a year of review could confirm, 12 more than Prideswick" | yes |
| xlsx Brackenford | 351 / 104 / 5 | 351 / 104 / 5 | yes |
| xlsx Ellerdyke | 140 / 40 / 6 | 140 / 40 / 6 | yes |
| xlsx Lathingbury | 559 / 165 / 0 | 559 / 165 / 0 | yes |
| xlsx Pellowham | 75 / 22 / 3 | 75 / 22 / 3 | yes |
| xlsx Prideswick | 221 / 63 / 46 | 221 / 63 / 46 | yes |
| xlsx Ristenholm | 438 / 126 / 8 | 438 / 126 / 8 | yes |
| xlsx Stennock | 275 / 80 / 80 | 275 / 80 / 80 | yes |
| xlsx Tannerby | 104 / 29 / 0 | 104 / 29 / 0 | yes |
| xlsx totals | 2,163 / 629 / 148 | 2,163 / 629 / 148 | yes |

The workbook figures reproduce only with the full conformance applied:
- CCRS times converted from UTC.
- The DECISION level used.
- CCRS-era transfer beds taken from the audit's `bed_confirmed_at`.
- Contiguous bed rows merged into one stay.
- Pilot twins counted once.
- Elapsed time measured across the clock changes.
- Temporary keys resolved for the audit join as well as for deaths.
- Each patient counted once.

Each of these is pinned by a shipped spec. Dropping any one of them moves the totals: naive clock 2,183/646/156, no UTC fix 2,183/645/172, no transfer fix 2,191/650/183, no bed-row merge 148 becomes 156, no key linkage 148 becomes 149.

## Competing answers that survived
None survived on any committed answer. The main call holds on every alternative window: FY 2025-26 (29 v 11), July 2024 to June 2025 (28 v 17) and the three-year record (80 v 46). The forks below are closed by shipped facts, but thinly. They are listed so the author can see the two answers each would produce.

- **`CCU` referral code (supplementary only).** ToR s.2 excludes "patients referred from another critical care unit", and the field guide never defines `CCU`.
  - Read as a critical care unit, the workbook becomes BRK 309/89/4 and RIS 403/115/7, with totals 2,086/603/146. The bars become BRK 31 and RIS 41.
  - What closes it: the unit feed codes every CCU-referred admission `source_location` 06 (ward), and no unit in the register is a CCU. This is the weakest closure in the build.
- **Died before admission (supplementary only).** If these patients are excluded, the bars become LAT 46, RIS 41, BRK 33, ELL 11, TAN 8 and PEL 6, and the workbook becomes 2,113/579. What closes it: the ToR wording ("waited more than four hours from the decision to admit to the assignment of a bed") and the plain sense of "died waiting".
- **CCRS LEVEL CHANGE 3 to 2 (supplementary only).** Using the last level instead of the DECISION level gives 2,159/627/148. What closes it: all 92 changes are recorded 11 to 73 hours after the patient was placed in a bed.
- **Bureau-allocated beds counted as the receiving trust's decision (main call).** Under this reading Ristenholm would have 37 own-care deaths and lead. What closes it: the field guide says `bed_confirmed_at` is "the time the network bed bureau allocated the bed", and ACCN/23/41 s.3 says transfers are agreed through the bureau.
- **Not forks:**
  - Which pilot twin is kept.
  - The October ambiguous hour.
  - Excluding REC (no REC referral ever waits more than 4 h).
  - The 30-day boundary (no remit death falls 24 to 35 days after the decision).
  - The NRR database: confirmed deaths equal remit deaths in all 34 reviews, and all 412 of those deaths sat beside an empty own bed, so it agrees with the own-care rule.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 20 | yes |
| Format count | 3 or more | 8 (csv 8, parquet 3, pdf 3, xlsx 2, sqlite, docx, eml, txt) | yes |
| Largest row count or database | 25,000+ rows or a large DB | `apc_episodes` 88,202 rows; `ambulance_handovers` 70,072; `nrr_review_records.sqlite` 12.7 MB (48,755 referral rows) | yes |
| Distractors declared | 2 or more in `metadata.json`, none labelled in `target/` | 2 (`level2_unit_bed_return_0800_2025-26.csv`, `ambulance_handovers_hourly_2025-26.csv`); file names neutral; the field guide lists both neutrally | yes |
| Distractors unused yet relevant | unused, same world | both are off the solution path. The level-2 return is a real near miss (own HDU beds at LAT, TAN, PEL, ELL), ruled out by the register's commissioned `care_level`. The ambulance handovers file is same-world but only weakly tied to the decision | yes (ambulance weak) |
| Distractor that answers a graded quantity is ruled out | reproduces, shipped fact rules it out | the level-2 return would yield "own empty beds" at trusts with no L3 unit, which `care_level` 2 rules out. The licensed wrong basis (the NRR screen on waits from receipt, computable from the capacity report's Referral waits sheet, which ranks Lathingbury first) is ruled out by ToR s.2/s.3 but is **not declared** in `metadata.json` | partial |
| Deliverable count | 1 to 3 | 3 (docx, xlsx, png) | yes |
| Format family | none required | n/a | yes |
| Multi-dimensional asks | not stacked lookups | workbook grid of 8 trusts x 3 measures plus totals over 36 months; chart of 8 bars with shading, order, gap and title; memo's 3 figures keyed to the call | yes |
| Goldens present | every named golden | 3 of 3. Every figure matches the recomputation, including the placement-year sheet (731/213/44) and the memo's 25/28/27 against 14/17/15 by four-quarter year | yes |
| Units and rounding | stated for every ask | units are inside every ask (deaths, patients). Rounding is stated once for all asks ("whole numbers throughout") rather than in each sentence | yes |
| Prompt shape and 25-criteria floor | shape identifiable, 25+ | per-trust grid plus a ranked chart under one call, about 49 gradable items (1 call, 3 memo figures, 27 workbook cells, 8 bars, the shaded parts, order, gap, title, 4 components). `metadata.json` records `prompt_shape: "other"` | yes (record the shape) |
| Realism | nothing reads LLM-generated; goldens read as work products | goldens read as a real board paper, workbook and chart. Notes below | yes, with notes |

Realism notes:
- **Goldens (trust names):** they give the trusts legal names that appear in no shipped file: "Stennock University Hospitals NHS Foundation Trust", "Prideswick Hospitals NHS Foundation Trust", "Ristenholm Teaching Hospitals NHS Foundation Trust", "Brackenford Hospitals NHS Foundation Trust", "Lathingbury Hospitals NHS Trust" and "Tannerby Hospital NHS Trust". Only Ellerdyke's and Pellowham's names are grounded, in ACCN/23/41.
- **Goldens (workbook totals):** the totals are typed values, not formulas.
- **Pack (bed returns):** `beds_open` is constant for 1,126 days, with RIS and STN at exactly 100% every morning.
- **Pack (timing of long waits):** long waits are tightly time-boxed: Stennock only on weekdays between 10:00 and 13:59, Brackenford only between 18:00 and 23:59.
- **Pack (30-day hole):** remit deaths have an engineered gap between 24 and 35 days after the decision.
- **Pack (board paper date):** the board-paper PDF is dated 14 Nov 2023 but records its own approval on 21 Nov 2023.
- **Pack (capacity report):** its closing read-me line reads as an authoring guard.

None of these is exclusion-level.

## Gate G reconciliation
| Field | Judge | Design note (stage 2 `### Gate G`, restated in hardening loop 3) | Match |
|---|---|---|---|
| mechanism | decomposition_attribution | decomposition_attribution ("each trust's long-wait deaths split into network capacity and its own care") | yes |
| stumping_family | analytical_non_defect | analytical_non_defect | yes |
| surface_read_dependency | no | no | yes |
| sole_data_defect | no | no | yes |

- **Distractors.** The judge did not name either declared distractor as the surface read carrying the task, so there is no finding that a distractor is too load-bearing.
- **Stump sentence.** The judge reached the design note's named wrong answers independently: Prideswick at 15 by reading bed assignment as occupancy, and Ristenholm at 37 by re-timing every held bed including the bureau's.
- **Borderline caution.** The judge flagged one caution for live testing: the decisive Stennock rung turns on reading "assigned" beds as held-empty beds, which a strict reviewer could call a single lens swap on the "full every morning" read.
  - The loop-3 clean-data argument answers it: an in-bed lens alone names Ristenholm at 37, so the bureau attribution is still the solver's work.
  - The stage-2 lens-swap test was written for the earlier decisive step (an interval join to another patient's planned admission) and was not re-run when loop 3 moved the decision onto assignment versus arrival.
- **Implication.** The build reads as the same shape from outside as from inside, so Gate G is not where this build is at risk.

## Stump power (Gate F)
The judge rates stump power as strong:
- **Careful solver lands on Prideswick.** A solver who reads the terms of reference, builds a minute census and sets the bureau's transfers aside still files Prideswick at 15 against Stennock's apparent 0.
- **The theatre join decides.** Stennock's held beds appear only when unit stays are joined to `rds_theatre_cases_2023-2026.parquet` and `admitted_at` is read as bed assignment rather than arrival. The prompt never mentions that join.
- **Shallower solvers miss in other directions:** Lathingbury (raw deaths, the chair's view), Ristenholm (most long waits, or counting bureau beds as its own) or Brackenford (empty beds at 08:00).
- **Too-easy signals are minor:**
  - Maria Reynolds' email gives Prideswick's weekend rule away, but Prideswick is the decoy.
  - The CCRS export specification documents each workbook correction, which softens only the supplementary workbook.
  - The email's one-opinion-per-trust layout is a roll-call shape.
- **Lever:** none is needed on stump power.

## Findings, ranked
1. **CCU is undefined, which thinly closes 6 workbook cells, 3 totals and 2 bars.** Add `CCU` to the `referred_from` definition in the field guide (`wenmarsh_acc_extract_field_guide.pdf`, section 2), for example "CCU coronary care unit (a ward)". Make the change through `generator/`, rebuild, and confirm that every figure stays at 2,163/629/148. This is a data-dictionary pin and needs no model rerun.
2. **Trust names in the committed answers are ungrounded (Gate B, wording).** Replace "Stennock University Hospitals NHS Foundation Trust" and "Prideswick Hospitals NHS Foundation Trust" in `submission.md` blocks 1 and 4 with names the files use (Stennock, STN, Stennock University Hospital; Prideswick, PRW). Do the same for every trust name in `golden/external_review_placement_2027-28.docx` and `golden/review_placement_workings.xlsx`. Do not add the legal names to `target/`.
3. **Licensed wrong basis not declared.** Add `wenmarsh_acc_capacity_report_2024-04_to_2026-06.xlsx`, `nrr_escalation_reviews_closed_2021-2025.xlsx` and `nrr_review_records.sqlite` to `distractor_files` in `metadata.json`. The design note calls the NRR screen the licensed wrong basis that ranks Lathingbury first, and all three files are off the solution path.
4. **Prompt shape not recorded.** Set `prompt_shape` in `metadata.json` to the picker's name for a per-trust grid plus a ranked chart, instead of "other".
5. **Stage-2 lens-swap test is stale.** Re-run it against the loop-3 decisive step in `DESIGN_NOTE.md`, so the record answers the "single lens swap" reading of the Stennock rung directly.
6. **Workbook realism.** Make the totals rows in `golden/review_placement_workings.xlsx` live SUM formulas. Optionally state the died-before-admission and DECISION-level rules in a solver-facing pin; the golden's Notes sheet states both, but solvers never see it.

## Next action for the author
In one generator-and-write-up pass:
- add the `CCU` definition to the field guide in `generator/` and rebuild the pack;
- restate every trust name in `submission.md` and the three goldens as the shipped files write them;
- re-run `reduce-house-fixes` and `leak.py` on the rebuilt pack before shipping.
