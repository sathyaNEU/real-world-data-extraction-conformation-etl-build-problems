# determinism-check report, task488, 2026-10-28

## Verdict
DETERMINISTIC, append SOLUTION_WRONG (the main recommendation and all six per-grade commission figures reproduce exactly; three supplementary-deliverable figures carry a reproducible item-selection bug in the solution's own build, not in the prompt or input files).

**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread independently re-implemented the marginal-maximum-likelihood (fixed-anchor) Rasch calibration from the Corvane spec and scale note, using the 3,894,963 complete/incomplete 2025-26 responses, and reproduced the committed below-cut counts (123/111/119/117/101/130), the workshop-items-below-cut counts (60/49/62/61/46/60), and the final commission (199: 27/39/31/33/49/20) to the item. It also reproduced both named wrong-method decoys exactly (93 from the writing panel's ratings as stored; 138 from calibrating against students' already-reported scale scores, which is circular because those scores were themselves computed from the panel's ratings). A sensitivity run collapsing the per-window population structure to one population per grade gave the identical answer, closing that fork.

The only defect found is confined to the supplementary deliverables (Gate A, `solution_incorrect`): the submission's own build script selected pool membership from the authoring catalog's `status == "active"` rows instead of the bank export's own `status == "operational"` rows (the rule the Corvane specification actually states, §1). This silently drops 98 bank-operational, fully-calibrated items whose only catalog row happens to be `status == "superseded"`, which undercounts `bank_import_2027-28.csv` (2,538 rows claimed vs. 2,636 true), the domain table in `pool_summary_2027-28.xlsx` ask 2 (sums to 2,538), and the enemy-set table in ask 3 (at least 7 named sets — EG-104/108/109/113/137/146/150 — gain a qualifying second member once the 98 are restored). This affects supplementary answers only; it does not touch the main recommendation, the memo, or any input file.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Operational responses used | 3,894,963 | 3,894,963 | yes |
| Below-cut per grade post-calibration | 123/111/119/117/101/130 | same | yes |
| Workshop items below cut | 60/49/62/61/46/60 | same | yes |
| Commission (main recommendation) | 199 (27/39/31/33/49/20) | same | yes |
| Decoy "93" (panel ratings as stored) | named, rejected | 93 | yes (confirms the rejected path) |
| Decoy "138" (Rasch vs. reported scores) | named, rejected | 138 | yes (confirms the rejected path) |
| Single-population-per-grade sensitivity | n/a | 123/111/119/117/101/130, total 199 | robust, no fork |
| `bank_import_2027-28.csv` row count | 2,538 | 2,636 bank-operational items; 98 omitted | **no** |
| `pool_summary_2027-28.xlsx` ask 2 domain table | sums to 2,538 | should sum to 2,636 | **no** |
| `pool_summary_2027-28.xlsx` ask 3 enemy sets | 14/10/9/11/9/11 sets | at least 7 sets (EG-104/108/109/113/137/146/150) undercounted | **no** |

## Competing answers that survived
None for the main recommendation. The judge enumerated the operationalization fork on the population-structure choice (per-window vs. single population) and confirmed both give the identical 199/27/39/31/33/49/20; no other defensible main-call answer survives. (The three supplementary-deliverable figures above are a reproduction bug, not a competing defensible answer — the spec's own rule is unambiguous, the solution's build just used the wrong table's status field.)

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / formats / large file | 10+ files, 3+ formats, 1 file 25k+ rows | 12 files, 4 formats (csv, xlsx, pdf, parquet), `tessaline_item_responses_2025-26.parquet` 3,925,625 rows (also `tessaline_sessions_2025-26.csv` 98,478 rows) | yes |
| Distractors named, none in a file name | 2+ named in metadata.json, none labeled in a filename | 3 named (`qrac_workshop_payments_2024_2025.csv`, `tessaline_platform_incidents_2025-26.csv`, `qrac_writing_panel_ratings_2024_2025.csv`); no filename says "distractor" | yes |
| Distractor relevance / one reproduces & is ruled out | each unused yet weighable; one reproduces a graded quantity arithmetically and a shipped fact rules it out | `qrac_writing_panel_ratings_2024_2025.csv` reproduces the named decoy 93 arithmetically and is ruled out by the bank export's own `difficulty_basis` column; the other two are relevant-but-unused (cost side; platform incidents) | yes |
| 1-3 deliverables, all present, no format family forced | prompt asks for 3: csv, xlsx, docx | all 3 present in `golden/` (`bank_import_2027-28.csv`, `pool_summary_2027-28.xlsx`, `low_band_commission_memo.docx`) | yes |
| Asks multi-dimensional, unit/rounding stated | not stacked lookups; unit+rounding in the asking sentence | Ask A (30 figures: 6 grades x 5 domains), Ask B (12 figures: 6 grades x sets/items) = 42 ask figures, each multi-dimensional; prompt's last sentence pins "whole items" and "one decimal of a scale point" | yes |
| Prompt shape identifiable, rubric reaches 25+ criteria | shape maps to a generated 25+-criterion rubric | no rubric.json shipped yet at this stage; design note's Ask sheet documents 42 gradable ask figures plus the main call and 2 critical-components lines, comfortably above the 25-criterion floor once generated | yes (pending formal generation, not a design gap) |
| Nothing LLM-generated; goldens read real | — | judge found catalog versioning/supersession, the 2010->2026 crosswalk, invalidated/incomplete events, and the provisional-vs-launch `difficulty_basis` split read as genuine multi-system exports, not LLM-authored | yes |

## Gate G reconciliation
Judge: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Card (`task488.json`): `stump_class: analytical`, `gate_g: etl_conformance`, `strategy: None` (design note names it "other (contaminated conditioning)"). Design note's own self-label (`etl_conformance`) and the judge's independent label (`method_or_model_selection`) differ in wording but land in the same non-banned bucket of Gate G's FINE-numbers list, so there is no disposition-relevant mismatch: both agree the task is not surface-read-rejection. The judge explicitly checked whether either decoy (93 from the panel ratings, 138 from the reported scores) is a "misleading reported read" the task flips away from, and correctly concluded neither reported value is wrong for its own stated purpose (a provisional rating; an honestly computed operational score) — the trap is choosing the right joint-calibration method and validating it out-of-sample against the launch items, exactly the method_or_model_selection shape Gate F wants. The judge did not name the declared distractor (`qrac_writing_panel_ratings_2024_2025.csv`) as the surface read carrying the task; it correctly identified it as the weaker, explicitly-dismissed decoy (93), while the design note's actual stump sentence and ladder center on the 138 decoy (Rasch against reported scores), which is not a declared distractor at all but the field's own natural reflex. No surface-read-dependency finding, no mismatch.

## Gate H reconciliation
Judge: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Card: `stump_class: analytical`. Design note's `## Three rules`: domain test and analyst test both name the same mechanism the judge independently reproduced (joint/marginal calibration with launch items fixed, vs. the easy reflex of calibrating against reported scale scores, which files 138). The judge's H3 reasoning matches the design note's "Not semantics" and "Not rule application" lines nearly verbatim (no filed rule or field ever states the calibration method; the reported-score and panel-ratings routes are each a plausible, honestly-reasoned route a strong analyst could take and still be wrong). Full agreement between the judge and the card/design note; no rebuild is indicated.

One genuine, useful cross-check: the judge's Gate-A finding (98 items dropped by reading catalog `active` status instead of bank `operational` status) lands exactly on the design note's own Ask B device ("a group set before a revision sits on the superseded version's catalog row, so reading the active rows alone drops the member") and matches the design's own predicted "miss" row in the Ask sheet's cracker-route table ("B, enemy sets and their items by grade | the catalog's active rows | under wherever a member sits on a superseded version | miss"). The authored golden fell into the exact trap the design built for a careless solver on two of the three supplementary deliverables. This is evidence the device works as designed, but it means the shipped golden itself needs the fix, not the task's construction.

## Findings, ranked
1. **(Gate A, solution_incorrect, FIX_NOW)** `bank_import_2027-28.csv` and the domain/enemy-set blocks of `pool_summary_2027-28.xlsx` were built from the authoring catalog's `status == "active"` field instead of the bank export's own `status == "operational"` field (Corvane spec §1). This drops 98 bank-operational, fully-calibrated items whose only catalog row is `superseded`, undercounting `bank_import_2027-28.csv` (2,538 vs. true 2,636), `pool_summary` ask 2's domain counts (sum 2,538 vs. true 2,636), and ask 3's enemy-set counts (at least EG-104, EG-108, EG-109, EG-113, EG-137, EG-146, EG-150 gain a qualifying second member). The main recommendation, the critical components, and the memo's commission numbers are unaffected.
2. No other defects found. Main call, both named decoys, hygiene, Gate G, and Gate H all check out clean.

## Next action for the author
Regenerate `bank_import_2027-28.csv` and the affected blocks of `pool_summary_2027-28.xlsx` (ask 2's domain table and ask 3's enemy-set table) from the bank export's `status == "operational"` rows (2,636 items), carrying each of the 98 `superseded`-only catalog rows' `skill_tag`/`standard_code` through the crosswalk for `reporting_domain` and its `enemy_group` for enemy-set membership — the same crosswalk-fallback logic SOLUTION_STEPS 6 already describes, just applied to the bank's own operational set rather than the catalog's active set. No change to prompt.txt, any input file, the main recommendation, or the memo is required, so no model rerun is needed; re-verify the two regenerated figures with `figures_check.py` before reshipping.
