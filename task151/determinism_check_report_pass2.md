# determinism-check report, task151, 2026-10-28

Pass context: `/fix-rubric` reship. The main call and every file it reads are frozen and byte-identical to
the shipped commit `e93c6561`. `prompt.txt`'s ask sentence was rewritten and the supplementary ask
re-sited onto the payroll ledger (the playing-time bonuses other than plate-appearance bonuses the club
paid for each of 2023, 2024 and 2025, player by player and in total). Bundle judged: `target.zip`
sha256 `f4bcf386b7171226e5a20fc239a8895bc269ea63bd89e3da61d2d459b2769294`, current `prompt.txt` and
`submission.md`.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread, working only from a fresh unzip of `target.zip` and the five extracted
blocks, recomputed every load-bearing figure and found all of them forced. The main call's foundations
(1,440 non-catcher lineup-seasons, the five hitters' 2027 slots, the term-sheet thresholds, the look-back
basis selection) were not touched by this revision and reproduced on spot-check. The revised
supplementary ask, the "other playing-time bonuses paid" table for 2023/2024/2025, is the part that
actually changed this pass, and it fully reproduces: all eleven named players, the legacy-employee-number
reuse (01661 = Benítez in 2023, Pietersz in 2025), the three embedded All-Star/award-bonus bundlings in
the legacy "OTHER BONUS" line, and the one void-and-reissue case all trace to specific cells in
`ral_player_contract_register_2023_2026.xlsx`, `ral_payroll_player_earnings_2023_2026.csv`,
`ral_payroll_earning_codes.csv` and `ral_hris_legacy_employee_map.csv`, and the three season totals
($580,000 / $1,080,000 / $1,230,000) recompute exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Non-catcher lineup-seasons, 2021-2026 | 1,440 | 240/season x 6 seasons = 1,440 (`hvbd_winter_depth_charts_2021_2026.xlsx`) | Yes |
| Five hitters' 2027 lineup slots | 5th-9th (Lusk, Rivas, Brock, Medina, Meeks) | Matches `ral_depth_chart_2027.xlsx` | Yes |
| Term-sheet thresholds/amounts, all five | per submission | Matches `term_sheets_2027_free_agent_hitters.pdf` | Yes |
| Per-player accrual (main call) | $500k/$1.0M/$600k/$1.2M/$900k | Spot-checked against frozen figures, not fully re-derived (main call not touched this pass) | Yes (spot-check) |
| Total accrual | $4,250,000 | Spot-checked | Yes (spot-check) |
| 2023 other-playing-time-bonus total | $580,000 | Recomputed player by player from payroll ledger | Yes |
| 2024 other-playing-time-bonus total | $1,080,000 | Recomputed player by player from payroll ledger | Yes |
| 2025 other-playing-time-bonus total | $1,230,000 | Recomputed player by player, including the void/reissue (Reed) and legacy-code reuse (Pietersz) | Yes |

## Competing answers that survived
None. The judge thread checked the three All-Star/award-bonus bundlings (Ruiz 2023, Livingston 2024,
Pietersz 2025) and White's separate Cy-Young line against a naive face-value read of the Oct-15 legacy
line, and found every one of those naive readings overstates a specific player-season by exactly the
bundled award amount, with the contract register's own award-bonus column closing the fork. The
employee-number reuse (01661) is closed by payee name on the payroll line itself, not by the current
HRIS crosswalk. No fork on the main call (frozen, not in scope this pass) and none on the revised ask
survived the thread's stress test.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / formats / large file | >=10 files, >=3 formats, 1 file >=25,000 rows | 21 files, 5 formats (csv/json/pdf/txt/xlsx); `lsf_batting_2021_2024.txt` 184,271 data rows, `lsf_batting_2025_2026.csv` 92,107 rows | Pass |
| Distractors declared, unlabelled | metadata.json names >=2, no filename labels one | 5 declared (`hvbd_hitter_projections_2022_2027.csv`, `league_schedule_2027.csv`, `lsf_transactions_2024_2026.json`, `league_office_il_report_2024_2026.csv`, `league_rules_art22_injured_lists_excerpt.pdf`); none named "distractor" | Pass |
| One distractor reproduces arithmetically, ruled out by a shipped fact | required | `hvbd_hitter_projections_2022_2027.csv` (the vendor's projection-with-band basis) is named and ruled out in the FINAL_RECOMMENDATION text itself, reproduces to a different total (design note: $6,250,000) and is ruled out by CF-14.4's look-back score, a shipped fact | Pass |
| Distractors otherwise unused but relevant | required | the three roster/IL distractors (`league_office_il_report_2024_2026.csv`, `league_rules_art22_injured_lists_excerpt.pdf`, `lsf_transactions_2024_2026.json`) are no longer touched by either ask after this reship's re-site (the prior Ask A used injured-list dates; the current ask 2 is payroll-sourced). They remain plausibly relevant to a solver puzzling over why some depth-chart seasons show fewer than 100 starts, but the author should confirm they still earn their place now that the ask layer has moved away from IL mechanics | Pass, flagged for author attention |
| 1-3 deliverables, all present, no format family forced | required | 2 deliverables (`pa_bonus_accrual_2027.xlsx`, `pa_bonus_accrual_memo_2027.docx`), both named in the prompt and present in the submission's Deliverable Answers | Pass |
| Asks multi-dimensional, unit/rounding in the ask | required | ask 2 is player x season x total; the prompt states rounding for the total, each player, and the bonuses paid in whole dollars | Pass |
| Prompt shape identifiable, rubric >=25 criteria | required | prompt shape named in metadata.json ("a total accrual ... fifteen bonus lines, a table ... and a one-page memo"); the rubric itself is not a file shipped under `target/` or readable without the generator, so the 25-criteria count was not independently verified in this pass | Not verified |
| No LLM-generated tells, goldens read as real work product | required | per the judge thread's hygiene check: PASS, real-looking legacy/HRIS migration artifacts, void-and-reissue line, multi-generation earning-code table; no disclosure or tool-banner language | Pass |

## Gate G reconciliation
The judge thread's classification (`mechanism: method_or_model_selection`, `stumping_family:
analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`) matches both the fingerprint
card's `stump_class: analytical` and the prior-cycle judge record already in `pipeline.json` ("gate_g:
PASS: method_or_model_selection, analytical_non_defect, surface_read_dependency no"). The declared
distractor (`hvbd_hitter_projections_2022_2027.csv`) is used exactly as the input-gates exception
permits: named and ruled out by a shipped fact (the look-back score) inside the FINAL_RECOMMENDATION
itself, never treated by the thread as "the surface read" the task defeats a solver by rejecting. No
mismatch found.

## Gate H reconciliation
The thread's line (`domain: pass`, `layers: pass`, `decisive_step: analytical`) matches the design note's
"## Three rules" section verbatim in substance: H1 (the task type is resampling/simulation choosing the
right predictive-distribution basis for a stepped payout, not a backdrop; the design note's own swap test
with "quota bonuses of ... account executives" shows the quantity has nothing to attach to outside this
domain), H2 (Layer 1 is the box-score platform change, legacy/HRIS payroll migration, void-and-reissue and
distractor files; Layer 2 is the FIN-14 4.4 out-of-sample look-back), and H3 (a capable analyst who read
everything correctly could still price the bonuses off the vendor's own 2027 projections, the players' own
seasons, or the whole starting nines, each of which scores higher in the look-back and files a different,
wrong total). This also matches the prior-cycle judge record in `pipeline.json` ("gate_h: domain pass,
layers pass, decisive_step analytical"). No mismatch; the main call's architecture is unchanged by this
reship, so continuity with the prior record is expected, not incidental.

## Stump power (Gate F)
The main call's stump (method/model selection among four candidate predictive-distribution bases, decided
by an out-of-sample look-back) is unaffected by this reship. The revised ask adds an independent trap: a
careless solver either trusts the current legacy-to-HRIS crosswalk and misattributes employee number 01661
across the 2023/2025 boundary, takes the Oct-15 legacy "OTHER BONUS" line at face value and overstates
three players by their bundled All-Star amount, or folds White's separate Cy-Young line into his
playing-time total. Each produces a specific, provable wrong number on a gradable cell; this is the kind
of device Rule 3 permits on a supplementary ask (Rule 3 binds only the main call's decisive step, and the
main call's decisive step stays the field's own out-of-sample method selection, not this ask's data
semantics).

## Findings, ranked
1. (Informational, not a determinism or Gate G/H failure) Three of the five declared distractors
   (`league_office_il_report_2024_2026.csv`, `league_rules_art22_injured_lists_excerpt.pdf`,
   `lsf_transactions_2024_2026.json`) were plausibly sited against the prior ask's injured-list mechanics;
   after this reship's re-site onto payroll data, confirm they still meet "relevant enough to weigh" on
   their own terms (roster/IL context for the depth-chart start counts) rather than riding on the
   now-retired ask.
2. The rubric's criterion count (>=25) was not independently verified in this pass; no rubric file ships
   under `target/`, and the generator was out of scope for this review per the pass's instruction.

## Next action for the author
None required for shipping; APPROVE. Optionally, confirm the three IL/transaction distractors still earn
their place now that the supplementary ask no longer uses injured-list dates, and confirm the rubric
criterion count separately (outside this pass's scope).
