# determinism-check report, task151, 2026-10-28

Author-side rehearsal, run as the stage-4 judge pass of a `/fix-rubric` reship. The main call, the
FIN-14 4.4 look-back basis, and every file the main call reads are frozen for this reship; only the
supplementary table's evidence (payroll export, contract register, HRIS map) was rebuilt and seven of
its figures moved. One isolated judge thread (general-purpose, sonnet, medium) was spawned on a fresh
unzip of `target.zip` (sha256 `44480c2bed8db3f95e02204a89343b9b0542701f48cca520f1deae4e11b97cc4`) at
`/tmp/determinism-check-task151-1793175989/target`, with only `graded_blocks.md` (the five labelled
blocks lifted from `submission.md`) and the inlined judge system prompt
(`guidelines/determinism_judge_system_prompt.md`, verbatim). The thread never opened `submission.md`,
`DESIGN_NOTE.md`, `metadata.json`, `generator/`, or any earlier report; it did its own derivation
(unzipping the xlsx/docx XML, extracting PDF text, reimplementing the look-back scoring and the full
payroll reconciliation) before writing `verdict.md`.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main recommendation is forced by FIN-14 4.4 / CF-14.4's look-back: of four defensible bases for
pricing the plate-appearance-bonus probabilities, the thread independently reimplemented the look-back
scoring over the 748 eligible 2023-2026 hitter-seasons and reproduced the winning basis's score of
0.17301 (claimed 0.1730) against three materially worse rejected bases (0.218-0.287, not a near-tie).
Re-deriving the five players' accruals from that basis and the term sheet reproduces the committed
figures exactly (Lusk $500,000; Rivas $1,000,000; Brock $600,000; Medina $1,200,000; Meeks $900,000;
unrounded total $4,221,715 rounds to $4,250,000, while the rounded player figures separately sum to
$4,200,000 exactly as SOLUTION_STEPS documents, not a defect). The rebuilt supplementary table (ask 2,
the non-PA playing-time bonuses for 2023/2024/2025) is the part that actually changed in this reship,
and the thread traced all ten player-season reconciliations it checked (Benítez, Casilla, Lara x3, Ruiz
x2, White x2, Pietersz, Livingston x2, Robertson x2, Blair) through the legacy-to-HRIS employee map, the
Reed void/reissue, the bundled-vs-separately-dated award distinction, and the cumulative deferred-salary
gap recognized in the line after a contract's last season, and every one matched the committed table
exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Batting-line universe 2021-2026 | 276,378 | 184,271 + 92,107 = 276,378 | Yes |
| Non-catcher regular seasons (1,440 total) | 391 >=155 starts / 178 <100 | 391 / 178 | Yes |
| PA/start by slot, 2027 lineup | 4.25/4.14/4.04/3.94/3.83 | 4.247/4.139/4.038/3.936/3.828 | Yes |
| Eligible 2023-2026 hitter-seasons | 748 | 748 | Yes |
| Winning look-back score | 0.1730 | 0.17301 | Yes |
| Rejected bases' scores | "each scores higher" | vendor+band 0.227, nines-whole 0.218, own seasons 0.287 | Yes, all materially worse |
| Five players' accruals | $500k/$1.0M/$600k/$1.2M/$900k | identical | Yes |
| Total accrual (nearest $250,000) | $4,250,000 | $4,221,715 rounds to $4,250,000 | Yes |
| Ask 2, 2023/2024/2025 season totals | $525,000 / $1,005,000 / $1,085,000 | all ten traced player-season lines, incl. the 01661 reuse (Benítez 2023 / Pietersz 2025), the Reed void/reissue, and the deferred-salary catch-up | Yes |

## Competing answers that survived
None. The one real candidate the prompt and files put on the table besides the winning basis, the
vendor's own player-specific 2027 PA projections, is named in FINAL_RECOMMENDATION and scores clearly
worse in the backtest (0.227 vs 0.1730), so it does not survive as a defensible fork. No fork opened on
the supplementary payroll table either: the thread's ten independent reconciliations landed on the
committed figures with no second reading of the legacy earning codes, the void/reissue, or the
deferred-salary catch-up producing a different number.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / formats | >=10 files, >=3 formats | 21 files, 5 formats (csv, json, pdf, txt, xlsx) | Pass |
| Large file | one file >=25,000 rows | `lsf_batting_2021_2024.txt`, 184,271 rows (`lsf_batting_2025_2026.csv` 92,107 rows) | Pass |
| Distractors | metadata.json names >=2, none labelled in a file name | 5 named in `metadata.json.distractor_files`; names are ordinary feed/report names (`hvbd_hitter_projections_2022_2027.csv`, `league_schedule_2027.csv`, `lsf_transactions_2024_2026.json`, `league_office_il_report_2024_2026.csv`, `league_rules_art22_injured_lists_excerpt.pdf`); none reads as "distractor" | Pass |
| Distractor relevance/exclusion | relevant, unused, one that answers a graded quantity reproduces and a shipped fact rules it out | `hvbd_hitter_projections_2022_2027.csv` (the vendor's own 2027 PA projections) reproduces a materially different, arithmetically valid accrual (~$6.25M per the card's `analyst_test`) and is ruled out by the shipped look-back score, not by any planted rule; the IL report / Article 22 excerpt / transactions wire are ruled out by FIN-14 4.3's stated exclusion of health/playing-time assumptions from the probability (DESIGN_NOTE 10-28 note) | Pass |
| Deliverables | 1-3, all present in golden, no format family forced | 2 (`pa_bonus_accrual_2027.xlsx`, `pa_bonus_accrual_memo_2027.docx`), both present under `golden/` | Pass |
| Asks multi-dimensional, unit/rounding stated | yes | main ask is 5 players x 15 bonus lines; ask 2 is 18 player-rows x 3 season totals; rounding to nearest $250,000 / $100,000 / whole dollars stated in `prompt.txt` | Pass |
| Rubric >=25 criteria | yes | DESIGN_NOTE's 10-28 stage-4 note: total + 5 player accruals (6) + 18 player rows and 3 season totals (21) + the memo (1) = 28, before instruction-following lines | Pass |
| LLM-generation / golden realism | none | judge thread hygiene PASS; no benchmark/tool-signature leakage found; legacy/platform/HRIS migration mess reads as genuine operational artifact | Pass |

## Gate G reconciliation
Thread (fresh, blind to design): `mechanism: method_or_model_selection`, `stumping_family:
analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Gate H line: `domain:
pass`, `layers: pass`, `decisive_step: analytical`.

DESIGN_NOTE's own stage-4 (10-28) log of the prior pass2 judge records the identical classification:
"Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no; Gate H domain
pass, layers pass, decisive step analytical." This pass3 thread, run independently after the
supplementary-table rebuild, reaches the same classification on a frozen main call, which is the
expected and desired outcome (the reship should not have moved the main call's stump shape). The card's
`stump_class: analytical` agrees, and its `domain_test` (the deciding quantity is a predictive
distribution of 2027 plate appearances that only resampling winter-planned regular whole seasons at the
new slot's rate recovers) matches the thread's H1/H3 reasoning that the vendor's player-specific
projections are the tempting but wrong basis because they carry each player's PA history at his old,
higher-slot role.

One inconsistency worth flagging, not disqualifying: the card's `analyst_test` opens by saying a strong
analyst "files $4,500,000" as the easy-route wrong answer, but $4,500,000 does not appear among the six
alternate-basis figures the same sentence goes on to enumerate ($6,250,000, $7,750,000, $5,250,000,
$3,750,000, $3,500,000, $4,000,000). This reads like a stale figure left over from before the 10-28
rubric-hardening rework of `records.py`/`calc.py` (the deferred-salary and `settle_whole`/`double`/`cap`
changes), which only touched the supplementary payroll table, not the main call's bases, so it should
not have moved this number. It is a documentation-hygiene item on the card, not a Gate H finding: the
thread's own easy-route answer (pricing off the vendor projections, ~$6,250,000) is internally consistent
with the rest of the card's enumerated list and with DESIGN_NOTE.

## Stump power (Gate F)
The thread's assessment: the task hands the solver the decision rule (run the look-back, use the
lowest-scoring basis) outright, so rule-discovery is not the trap by design. What stumps is that the
"obviously best" data source, the vendor's player-specific 2027 PA projections, is the detail-rich,
natural-looking choice, but it carries each free agent's recent PA history at his old team's higher
lineup slot, systematically overstating his 2027 probability; only running the stated backtest surfaces
that it scores worse than the slot-based regulars' basis. This is a genuine method-selection trap on
honest, correctly-reported data (method_or_model_selection, Gate F's library of FINE-numbers shapes,
`stumping` 1.3): a strong analyst who read every file and rule correctly could still take the vendor-
projection shortcut and file a materially higher, wrong accrual, with no judgment the data had to settle
beyond applying the field's own backtest discipline. The main thread should weigh this against
DESIGN_NOTE's ladder (the `ceiling.py` ladder reports "the full handling of the first device 13" off the
call, 46.0/61.0 on the two weightings) for how much of that stump power the top-two bar actually banks;
this report records the landable-call framing per the agent contract, it does not re-run the ladder.

## Findings, ranked
1. (Informational, not a finding against this build) The card's `analyst_test` carries a stray
   $4,500,000 figure that does not match its own enumerated alternate-basis list; worth a quick author
   check against the current generator next time the card is touched, but it does not affect the main
   call, the frozen files, or this pass's verdict.
2. No determinism, correctness, Gate F, Gate G, or Gate H defect found in this pass. The rebuilt
   supplementary table (ask 2) reproduces exactly across all ten player-season lines the thread checked.

## Next action for the author
None required to ship this reship: APPROVE and move to the portal. If touching the card again, correct
the stray $4,500,000 figure in `analyst_test` to match the enumerated alternate-basis list (or confirm
it refers to a distinct basis not yet named, and name it).
