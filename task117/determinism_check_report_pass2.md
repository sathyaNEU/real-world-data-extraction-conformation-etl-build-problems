# determinism-check report, task117, 2026-10-09

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

**Run note.** This runtime exposes no Agent tool, so this pass's single judge ran in the orchestrator's own context, with isolation enforced by hand. That matches the task118 pass and pass 1 of this task.

Before `verdict.md` was written to `/tmp/determinism-check-task117-20261009T180701-1199/`, only these were read:
- a fresh copy of `target/`, which is checked sha256-identical to the folder (there is no `target.zip`)
- `prompt.md`
- `submission.md`, read whole to extract the blocks; Tags is not a judge input
- `guidelines/determinism_judge_system_prompt.md` (v3)
- generic context only: the repo `CLAUDE.md`, the determinism-check skill, and the run-note line of task118's report

After the verdict was fixed, I read:
- `metadata.json`
- the Draw, Stump sentence, Decisive rung, Gate G and Stage 6 sections of `DESIGN_NOTE.md`
- `golden/`

`generator/`, `pipeline.json`, `solver_rounds/` and `leak_check_report.md` were never opened.

**Pass numbering.** Pass 1 is recorded in `DESIGN_NOTE.md` under "Stage 6: judge rehearsal, fix cycle 1". Its report never reached the task folder; its verdict sits at `/tmp/determinism-check-task117-20261009T164655Z/verdict.md`, which I did not read. No `determinism_check_report*.md` existed here, so this file, numbered pass 2 as the invocation asked, overwrites nothing.

## Why
Every committed answer recomputes exactly from the shipped files: the call, the 12 contract months, the setting month, the deck split, the planners' figure and gap, the 12 back-test rows and the 24 panel rows. Every rival that moves an answer is closed by a shipped rule or by evidence in the record:
- Agreement §4: the first-year Contract Demand is the maximum Billing Demand expected.
- Schedule 26 §3: the billing window.
- FES-07 §§2 to 4: the base year, the factor in force, one rounding, and records as they stood.
- The 2026 statements: they reconcile only on joined charges (875 of 875 permit-months).
- The January 2027 renewal checks.
- The 101 North Deck pool-car hand-offs, whose starts follow the car ahead's finish.

The call of 110 kW is 97.4 kW × 1.12 = 109.088. That sits 1.59 kW inside the nearest-5 bin, and nearest and round-up both file 110. Every charge in the setting quarter-hour runs through the full 15 minutes, so no choice of time grain moves it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Sessions of record | ACCEPTED version, one row per auth_code, dated register join | 111,570 records. 82 redelivered auth codes collapsed. Deck IDs reused at Ferry Terminal and Market Square from 2025-08-18 and 2025-10-06 excluded by date | yes |
| Settlement-split join | reproduces every permit-month's charge count | 2026 deck records 10,142 become 7,046 charges (3,096 pairs at 10:02 to 10:04). Charges and kWh match 875/875 statement rows. Raw records match 5% | yes |
| CC2, county permits re-carred | 18, 7.2 to 11.0 kW | 18, each 2020 Bolt EV to 2023 Bolt EV (`permit_vehicle_checks.csv`, `vehicle_reference_list.csv`) | yes |
| CC3, pool-car hand-offs | 101 on North Deck | 101 (all county to county, all North). 39 incoming permits. Car ahead off 6.0 to 19.9 min after finishing. Next car on 1.0 to 5.4 min later. Other charges' median dwell after finishing 6.67 h | yes |
| CC4, replay peak | 97.4 kW at 12:00 Wed 21 Jan 2026 | 97.400 (12 × 7.2 + 11.0). Next quarter-hour 94.76. Nearest charge ends 11:30 and 12:24 | yes |
| CC5, January 2028 forecast | 109.1 kW, highest month | 109.088, highest. December 2027 runner-up at 96.88 | yes |
| Contracted demand | 110 kW | 109.088 to nearest 5 = 110 (round-up also 110) | yes |
| April 2027 | 74 | 74.144 | yes |
| May 2027 | 77 | 76.832 | yes |
| June 2027 | 87 | 87.136 | yes |
| July 2027 | 80 | 80.192 | yes |
| August 2027 | 67 | 66.752 | yes |
| September 2027 | 95 | 95.200 | yes |
| October 2027 | 86 | 86.016 | yes |
| November 2027 | 79 | 79.072 | yes |
| December 2027 | 97 | 96.880 | yes |
| January 2028 | 109 | 109.088 | yes |
| February 2028 | 76 | 75.936 | yes |
| March 2028 | 82 | 81.760 | yes |
| Month that sets it | January 2028 | January 2028 (base Wed 21 Jan 2026, 12:00) | yes |
| Deck split, North | 56 kW | 50.4 × 1.12 = 56.448 | yes |
| Deck split, South | 53 kW | 47.0 × 1.12 = 52.640 | yes |
| Planners' figure | 225 kW | 32 × 11.5 × 0.60 = 220.8, next 5 kW above = 225 (Section 7.3, Table 7-2) | yes |
| Gap to ours | 115 kW | 225 − 110 = 115 | yes |
| PNG basis day | Wed 21 Jan 2026 | same. Actual draw at 12:00 on the 6.6 kW units 145.2 kW (72.6 a deck) | yes |
| PNG marked quarter-hour | 12:00 at 109 kW, line at 110 | 109.088 at 12:00. Contract line 110 | yes |
| Back-test January 2025 | 112 kW, −0.9% | 111.923 gives 112. Actual 113.144 gives 113. −0.885% | yes |
| Back-test February 2025 | 122 kW, +1.7% | 121.824 gives 122. 119.844 gives 120. +1.667% | yes |
| Back-test March 2025 | 105 kW, −1.9% | 105.144 gives 105. 107.092 gives 107. −1.869% | yes |
| Back-test April 2025 | 102 kW, +1.0% | 102.103 gives 102. 101.092 gives 101. +0.990% | yes |
| Back-test May 2025 | 102 kW, −1.0% | 101.874 gives 102. 102.904 gives 103. −0.971% | yes |
| Back-test June 2025 | 83 kW, +2.5% | 83.208 gives 83. 80.828 gives 81. +2.469% | yes |
| Back-test July 2025 | 83 kW, −1.2% | 83.100 gives 83. 84.140 gives 84. −1.190% | yes |
| Back-test August 2025 | 82 kW, +1.2% | 82.197 gives 82. 80.800 gives 81. +1.235% | yes |
| Back-test September 2025 | 107 kW, −1.8% | 106.829 gives 107. 109.224 gives 109. −1.835% | yes |
| Back-test October 2025 | 114 kW, +1.8% | 114.225 gives 114. 111.876 gives 112. +1.786% | yes |
| Back-test November 2025 | 121 kW, +1.7% | 120.804 gives 121. 118.916 gives 119. +1.681% | yes |
| Back-test December 2025 | 114 kW, −0.9% | 113.880 gives 114. 114.888 gives 115. −0.870% | yes |
| Back-test spread | −1.9% to +2.5%, six over and six under | same | yes |
| CP-N read 1 (Jan 30) | 1,069 | 1,068.833 | yes |
| CP-N read 2 (Feb 27) | 908 | 907.835 | yes |
| CP-N read 3 (Mar 31) | 910 | 910.160 | yes |
| CP-N read 4 (Apr 30) | 725 | 725.153 | yes |
| CP-N read 5 (May 29) | 594 | 593.828 | yes |
| CP-N read 6 (Jun 30) | 592 | 592.120 | yes |
| CP-N read 7 (Jul 31) | 599 | 599.144 | yes |
| CP-N read 8 (Aug 31) | 691 | 691.158 | yes |
| CP-N read 9 (Sep 30) | 791 | 791.208 | yes |
| CP-N read 10 (Oct 30) | 914 | 913.777 | yes |
| CP-N read 11 (Nov 30) | 1,063 | 1,062.861 | yes |
| CP-N read 12 (Dec 31) | 1,133 | 1,132.898 | yes |
| CP-S read 1 (Jan 30) | 934 | 933.924 | yes |
| CP-S read 2 (Feb 27) | 799 | 798.803 | yes |
| CP-S read 3 (Mar 31) | 794 | 794.181 | yes |
| CP-S read 4 (Apr 30) | 633 | 633.144 | yes |
| CP-S read 5 (May 29) | 520 | 519.869 | yes |
| CP-S read 6 (Jun 30) | 517 | 517.163 | yes |
| CP-S read 7 (Jul 31) | 523 | 523.166 | yes |
| CP-S read 8 (Aug 31) | 606 | 606.158 | yes |
| CP-S read 9 (Sep 30) | 693 | 693.178 | yes |
| CP-S read 10 (Oct 30) | 799 | 799.201 | yes |
| CP-S read 11 (Nov 30) | 932 | 932.163 | yes |
| CP-S read 12 (Dec 31) | 990 | 989.822 | yes |

Rounding margins:
- Every contract-month figure is at least 0.252 from a .5 edge.
- Back-test forecasts are at least 0.275 from an edge, and actuals at least 0.276.
- Panel rows are at least 0.277 from an edge.

How the back-test reproduces:
- The 2024 base uses records as they stood in January 2025, so the 12 restated sessions count at v1.
- Gateway B is added (299 sessions on N-01, N-02, N-05 and N-06), plus the 33 deck fleet-card charges the export lacks.
- Those charges are placed UTC to local. START equals the export's plug_in to the second on 100% of the charges both files carry.
- They are drawn at full rate from plug-in, as every metered session shows (flat 1.65 kWh quarter-hours, then zeros).
- The result is × 1.08 and rounded once.

How the panel rows reproduce:
- the Corrections sheet is applied;
- the later 31 Dec South read stands;
- the meter clock is PST (DST disabled);
- N-11 sits on HP-N from 1 June to 12 July;
- the courtesy sessions are included (none straddles a read).

## Competing answers that survived
None. Each fork tested and what closes it:

| Fork | Rival answer | Closed by |
|---|---|---|
| Keep every 2026 start (no hand-off re-timing) | 129.136, files 130 | The hand-off record: all 101 starts follow the car ahead's finish. Same wait, zero wait, gap-only and dwell-only re-timings all give 109.088 |
| Replay with the 2026 cars | 148.512, files 150 (Feb 2026 base) | January 2027 renewal rows in `permit_vehicle_checks.csv`; the forecast is for the contract year |
| Settlement records replayed as charges | 128.486 (re-timed) or 155.357 (held), files 130 or 155 | Statements reconcile 875/875 only on joined charges; field notes' 10 a.m. run |
| Every charge at 11.5 kW | 90.16, files 90 | Car ratings in `vehicle_reference_list.csv` |
| Factor 1.10 (planning year 2026) | 107.14, files 105 | FES-07 §3, factor in force on the date made (1.12 since 15 Sep 2026) |
| Nameplate × diversity | 225 | Agreement §4 (expected maximum Billing Demand) |
| 2026 billing peak or meter registers scaled by 11.5/6.6 | 309 to 412 | Schedule 26 §3 window; registers are all-hours on old units |
| File low and let the ratchet reset | below 110 | Agreement §4 |
| Back-test on current records (2024 restatements applied) | all 12 forecasts move (each restated session sits at its month's maximum) | FES-07 §4, records as they stood, no restatement. The base-month rule dates the forecast to January 2025 |
| Back-test factor 1.09 | all 12 move | FES-07 §3, factor in force in January 2025 |
| Back-test without gateway B | Jan to Apr move | Data-sources note; gateway B units are N-01, N-02, N-05 and N-06 |
| Fleet file absent or read as local time | forecasts and Jan to Mar actuals move | NETWORK_REF to auth_code match, UTC on 100% |
| Spread unmetered energy over plug-in time | errors up to +8.6% | Contradicts the metered profile of every exported session |
| Error against the unrounded actual | all 12 move by 0.1 to 0.3 | FES-07 §4 ("recorded billing demand in whole kilowatts"); the whole-kW-difference reading converges |
| Panel rows without Corrections | 16 rows move (each of the 8 corrections shifts two spans) | Corrections sheet header |
| Earlier 31 Dec South read | 2,989 | Reads sheet note: the later reading stands |
| Read times as local clock | 18 rows move (March to November spans) | `deck_submeter_nameplates.csv`, PST, DST disabled |
| No courtesy sessions | all 24 move | Export carries no weekend or holiday deck charging |
| N-11 left on CP-N, or refed from the WO open date (28 May) | Jun and Jul, or May and Jun, move | `deck_panel_circuit_schedule.csv` effective dates |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in the pack | 10 or more | 24 | yes |
| Distinct formats | 3 or more | 6: CSV 17, TXT 2, PDF 3, DOCX 1, XLSX 1, Parquet 1 | yes |
| Largest row count | a file of 25,000+ rows or a large database | `settled_sessions_2024-2026.csv` 111,709 rows; `session_intervals_2024-2026.parquet` 1,537,144 rows | yes |
| Distractors declared | 2 or more in `metadata.json`, none labelled by name or content | 2: `civic_center_campus_electric_statements_2024-2026.csv`, `charger_status_events_2026.csv`; names neutral, the data-sources note describes both neutrally | yes |
| Distractors unused yet relevant | same world, must be weighed | Statements: the decks' current NSPL campus account with billing and contract demand columns. Status events: firmware, communication and fault events on the deck units. Neither feeds any graded figure | yes |
| Distractor answering a graded quantity | reproduces, and a shipped fact rules it out | Neither offers a graded quantity. The campus billing demand (565.7 to 758.0 kW, non-calendar periods, contract 800 kW) is ruled out by Schedule 26 §3 (calendar billing month on the dedicated service) and Agreement §1 (the new service replaces the campus feed) | yes |
| Deliverables | 1 to 3 | 3: `contract_demand_note.pdf`, `deck_load_day.png`, `civic_service_demand.xlsx` | yes |
| Format family | none assigned, none required | PDF, PNG, XLSX | n/a |
| Multi-dimensional asks | not stacked lookups | 12-month forecast, 12 × 2 back-test, 2 × 12 panel grid, deck split at the binding quarter-hour | yes |
| Goldens present | every deliverable the prompt names | all three in `golden/`, each opened | yes |
| Units and rounding | stated for every ask | "in kW to the nearest 5 kW"; "kW and kWh as whole numbers unless I say otherwise"; error "as a percentage of the actual to one decimal" | yes |
| Prompt shape and 25-criteria floor | shape identifiable, 25+ criteria | Shape 02, forecast across many periods; about 71 gradable items (1 + 12 + 1 + 2 + 2 + 5 + 24 + 24) | yes |
| Realism | nothing reads as LLM generated; goldens read as work products | Pack carries real irregularities (restatements, redeliveries, reused IDs, three time bases, a double read, keyed corrections). Memo, chart and workbook read as finished work. No em dashes in prompt, write-up or memo. Two cosmetic golden items, findings 3 and 4 | yes |

## Gate G reconciliation
The judge's line and the design note's line agree on all four axes:
- Judge: forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no.
- `DESIGN_NOTE.md` (Gate G as restated at harden loop 3 and carried through stage 6): forecasting (method_or_model_selection supporting), analytical_non_defect, no, no.

The supporting label differs only in name. The judge called the support layer ETL conformance on honest data; the note calls it method selection (session replay over ratio scaling). The primary mechanism is the same.

The judge also reached the decisive rung on its own. It named the hand-off re-timing as the trap that does the work, which is the note's rung 7 (trap #13). Its rivals reproduce the note's ladder exactly: rung 2 at 90.16, rung 5 at 155.357 and rung 6 at 129.136. The memo's "149 kW in February" with 2026 cars is the judge's 148.512.

Neither declared distractor was named as the surface read carrying the task, so there is no distractor finding. The build reads the same shape from the outside as from the inside, so the strongest predictor of a send-back is absent.

## Stump power (Gate F)
Moderate to good on the main call. Three independent rungs each move 110:
- the hand-off re-timing (130);
- the settlement-split join (130 or 155);
- the renewal cars (150).

A solver lands 110 only with all three. The hand-off is the trap that does the work: no document states that a pool car's start depends on the car ahead, and only WO-26-0529 corroborates it. The renewal-car rung is the weakest, because taking each permit's latest check lands on the 2027 car by default.

Too-easy signals named:
- `parking_services_data_sources.txt` and `curbline_export_field_notes.txt` state the gateway B gap, the restatement rule, identifier reuse and the 10 a.m. run. That pre-disarms much of the ETL layer, which mostly guards the asks.
- Ricardo Moore's "everyone charged before lunch" points the solver at the noon boundary.

The ask layer is strong: 48 separately graded back-test and panel figures (12 back-test rows of two figures, 24 panel rows), each behind two to five traps.

## Findings, ranked
1. **`submission.md` step 6 under-describes the 2025 actuals** (solution block, in-house, no rerun). Say that 2025 is built from the sessions of record with the accepted 2025 restatements, plus the January to March 2025 fleet-card charges the export does not carry. The workbook notes (`2025 back-test`!A21 and A23) already say this; the write-up does not.
   - Without the fleet charges, January to March read 0.0, +2.5 and −0.9.
   - Without the accepted restatements, May to July read 0.0, +3.8 and 0.0.
   - Corrections to the scratch `verdict.md`. None of them changes the verdict, the disposition or any closure, because each rival still moves at least one graded figure:
     - its illustration of this fix gives February as −0.8; the recomputed value is +2.5;
     - it says the current-records rival moves 9 of 12 forecasts; it moves all 12;
     - it says the unrounded-actual rival moves rows by 0.1 to 0.2; the range is 0.1 to 0.3;
     - it says the no-Corrections rival moves 10 rows; it moves 16;
     - it says the local-clock rival moves 14 rows; it moves 18;
     - it counts 36 graded ask figures; there are 48.
2. **Deck-split ask wording, watch only** (prompt; editing it costs a rerun). "How many kW each deck carries in the quarter-hour that sets it" is read naturally as the forecast split, 56 and 53, which sum to the setting 109. The only live rival is the pre-growth replay split, 50 and 47. The old-unit draw at that quarter-hour was 72.6 a deck. The write-up line already names the January 2028 forecast quarter-hour. Leave the prompt alone unless graders split.
3. **Memo attribution** (`golden/contract_demand_note.pdf`, regenerate through `golden.py`, no rerun). "Section 4 of the agreement asks for the maximum billing demand we expect, and a month above 110 kW would reset the contract…" puts the reset in the agreement's section. The reset is Schedule 26 §4, so cite Schedule 26 for the second clause.
4. **Tied maxima in the workbook** (`golden/civic_service_demand.xlsx`, `Contract year` column C). April (12:00, 12:15 and 12:30), May (12:00 and 12:15) and September (12:00 and 12:15) tie at the month's maximum, but the column names only 12:00. This is not graded, but a reviewer may query it. Label it "from 12:00", or list the tie.
5. **Optional hardening, not recommended now** (input files, rerun cost). The documentation hands out several ETL repairs. The decisive rung is undocumented, so the main call does not depend on them.

## Next action for the author
Reword step 6 of `submission.md` (through `submission-writeup`) so that the 2025 actuals name the accepted 2025 restatements and the January to March 2025 fleet-card charges. Nothing solvers see changes, so the build stays APPROVE and moves on to the `/leak-check` reader pass.
