# determinism-check report, task265, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) recomputed from a fresh unzip: all six ten-year figures, the 54 construct-by-hospital counts and the 28 missing hips reproduce. Policy VA-07 4.2 and 4.3 file the bar (5.0 or less), the unit, Kaplan-Meier and the censoring. The data dictionary files the entry date of pre-2018 hips (Enrolled on visit). Delayed entry with the clock from the operation keeps exactly Askvane/Quarvel, Holbrin/Pellvoro and Askvane/Pellvoro. Nearest values to the bar are 4.1 and 5.68, so no margin is thin. Horizon (3,650 to 3,653 days) and month-only death day (1st, 15th, month-end) change nothing at one decimal and no verdict.

Note on bundle version: the thread judged the bundle unzipped before the generator's last edits (one dictionary sentence closing the move-out-of-Wisconsin reading, the log's HO/KO prefix fix, varied log linkage dates). The coordinator reports no graded figure moved, with checks, independent verifier and byte-identical rebuild green. I did not re-judge (one thread only); the current target.zip is 8,702,193 bytes against 8,702,041 judged.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Edvalt/Kelvarne 10y CPR | 7.0 | 7.02 | yes |
| Edvalt/Pellvoro | 5.7 | 5.68 | yes |
| Kalvoran/Morvenne | 7.6 | 7.62 | yes |
| Askvane/Quarvel | 3.7 | 3.70 | yes |
| Holbrin/Pellvoro | 4.1 | recomputed, matches | yes |
| Askvane/Pellvoro | 3.5 | recomputed, matches | yes |
| 2026 primary THA | 1,009 (54 cell counts) | 998 cases + 11 bilateral = 1,009; split matches ask 2 | yes |
| Missing from registry | 28 (1/2/7/4/8/6; 12/5/11) | identical | yes |
Wrong-route values: no entry correction gives 3.08 and 3.16 (five kept); entry at 2018-01-01 gives 6.17 and 4.55 (four kept).

## Competing answers that survived
None. Closed alternatives: no move censoring (Askvane/Quarvel 3.64 gives 3.6) is not licensed by Policy 4.3 and the dictionary; no merge expansion gives 40 missing and ignoring side gives 26, both solver errors against the stated unit and files. Residual softness, not a fork: the rule that implants on the other side of a one-sided case are not that day's operation is stated nowhere, and is forced only by the case list plus the registry's non-presence of those lines (48 lines, none with a registry operation).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | CSV, XLSX, PDF | yes |
| Large file | 25,000 rows or more | periop log 32,416 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | price schedule PDF and clinic visits CSV; names are neutral | yes |
| Distractor weighing | unused by solution, relevant, ruled out by a shipped fact | thread also lists Orsinne and Fennimark constructs (off the agreement), hemiarthroplasty and revision cases; no distractor answers a graded quantity | yes (thread-level; not independently arithmetic-tested by me) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx) | yes |
| Asks | multi-dimensional, unit and rounding stated | four asks, whole numbers and one decimal stated in prompt | yes |
| Rubric 25 or more | prompt shape identifiable | shape 14 per design note (6 constructs x cuts, 54 cells, 28 reconciling counts); count not generated here | yes, by shape |
| Reads as real | no LLM tells | thread: operational extracts, mixed date formats, no authoring language; one HO/KO nit since fixed | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor (delayed entry / left truncation), family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, gate_g method_or_model_selection, strategy population_selection; design stump is the legacy enrolment left truncation. Match. The declared distractors (Schedule B price schedule, clinic visits) are not named by the thread as the surface read carrying the task. No shipped artifact ranks candidates wrongly; no finding.
**Gate G classification:** pass, analytical, no banned scaffold.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Layer 1: legacy workbook against prospective export, Thorvik renumbering, month-only deaths, merged MRNs, wrong-side log lines. Layer 2: the risk set for hips entered after their operation. Matches the design note's Three rules (No decoy, Not semantics, Not rule application).

## Stump power (Gate F)
Good. Standard KM from the operation gives five kept (3.1 and 3.2); the 2018-01-01 shortcut gives four kept (4.6); both natural, separated from the answer by wide margins. The asks add independent error chances (side, net of explants, merges).

## Findings, ranked
1. Watch item, Gate H: the judge counted the dictionary's Enrolled-on entry rule as filed. A reviewer could read that as data semantics or rule application. The design note's defence (the policy files the estimator but no filed rule says when a hip enters the risk set; the default path reads every field correctly yet is wrong) is sound, but this is the likeliest send-back angle. No change needed.
2. Unstated rule on other-side implant lines in the periop log (inferable from data, not a fork).
3. Hygiene (resolved by coordinator after the thread's read): HO/KO prefix mismatch in the log, the move-out-of-Wisconsin dictionary sentence, linkage dates. Bundle changed after judging; figures unchanged per coordinator.
No SOLUTION_WRONG.

## Next action for the author
Proceed to ship; optionally run a cheap check that the shipped target.zip's figures still match the golden (verifier already green).
