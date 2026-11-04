# determinism-check report, task461 (architecture 3, pass 2), 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (metering-topology reconciliation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One fresh judge thread (sonnet, medium) on a fresh unzip of target.zip (sha256 c50af2dd...9c68) recomputed every load-bearing value. Base Building Electricity is the import less the Tenancy supplies (Schedule 9 cl. 1.4). That gives 1,917.3 MWh, 396.98 t and 18.4986 kg/m2 against 17.6, a miss of 0.9. The one judgment is the hierarchy: EM-102, 105, 108 and 117 sit inside EM-101, 104, 115 and 112. The half-hourly data separate them on three tests: increments never exceed the parent's over 17,499 half-hours, the same zero pattern, and zero exactly when the parent is isolated on 13 June. No other pair passes. Gates A-E pass for the main call and all asks.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Import (settlement date, calendar months) | 3,640 MWh | 3,639.9 | yes |
| Tenancy supplies, 13 meters | 1,723 MWh | 1,722.7 | yes |
| Base building by month | 158,145,156,141,150,176,190,175,166,153,152,154 | 158.4,144.6,156.5,141.3,150.3,176.1,189.8,174.6,166.4,153.3,152.0,154.0 | yes |
| Base building, year | 1,917 MWh | 1,917.31 | yes |
| Scope 2 | 397.0 t | 396.979 | yes |
| KPI / miss | 18.5 / 0.9 | 18.4986 / 0.90 | yes |
| Nested meters | 293 MWh | 293.4 | yes |
| All 17 subtracted (wrong route) | 15.7 | 15.7 (1,624 MWh) | yes |
| Gas oil Q1-Q4 | 575/312/325/446 L; 1,529/830/864/1,186 kg | same | yes |
| Refrigerant CH-1..4 | 10.8/20.7/14.8/20.5 kg; 15,444/29,601/21,164/29,315 kg | same | yes |

## Competing answers that survived
No fork touches the call or the KPI. Residual edges on supplementary figures only (judge's APPROVE stands):
1. Scope 2 rounding path: 1,917 rounded then times 0.20705 gives 396.9 t against 397.0 unrounded; the 12 rounded months sum to 1,916 against 1,917. KPI 18.5 and miss 0.9 hold either way. The prompt gives per-figure rounding but not "round once at the end".
2. Gas oil: Q2 and Q3 hold only when each week's burn is placed on that week's logged runs (linear interpolation gives about 249 L for Q2). The controller log is shipped and cl. 4.2 says "burned in each quarter", which supports the run-based reading. Q1 opening stock 2,047 L assumes no run on 29-31 Dec because the log starts 2 Jan 2026.
Rejected readings closed by shipped facts: per-occupier or per-premises (21.4 or 19.7), landlord meters EM-201..204 only (not the Schedule definition), roof licence EM-114 (a Tenancy under cl. 1.3, subtracted).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 13 / csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | BMS CSV 369,580 rows | yes |
| Distractors in metadata.json, none named in a file name | 2+ | met_wexmoor_daily_2026.csv, pellow_house_epc_2024.pdf (names do not label them) | yes |
| Distractors unused yet weighable; wrong-basis one ruled out by a shipped fact | yes | EPC area 27,940 m2 against Schedule NLA 21,460 (would give about 14.2); the schedule fixes NLA. Met file is weak but weighable context | yes (met file thin) |
| Deliverables | 1-3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | quarterly gas oil (8 figures), per-chiller refrigerant (8), monthly electricity; units and rounding in the prompt sentence | yes |
| Prompt shape, 25+ criteria | yes | shape "other", 12 months + year + Scope 2 + KPI + result + margin + 16 Scope 1 figures + letter items, about 35 gradable | yes |
| Prompt form | one paragraph, under 1,000 chars | 992 chars, one line | yes |
| Reads as real work product | yes | judge: BMS file realistic; register and tenancy schedule slightly tidy, nothing exclusion-level | yes |

## Gate G reconciliation
Read only after the thread returned. Thread: mechanism other, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, with analyst_test (subtract every register-listed meter, file 15.7) matching the thread's easy route exactly. The design note's Stump sentence names the same 15.7 against 18.5. No mismatch. The declared distractors (EPC, weather) were not named as carrying the task, so they are not too load-bearing. The thread noted that a strict reader could class the double-count as planted_defect_flip. I judge that low risk: the design note's "No decoy" line records ordinary sub-metering wiring, no wrong headline ships, and no memo or stakeholder figure exists. Main thread to weigh.

Gate H: domain pass (GHG Scope 1 and 2 for a sustainability-linked loan), layers pass (Layer 1: DST periods, Wh and kWh registers, meter swap, clock-change hour, Calbrook labels; Layer 2: hierarchy from interval data), decisive_step analytical. This matches the card's domain_test and the design note's Three rules. The thread did not class the step analytical merely because the method is textbook: no field resolves the hierarchy and the data had to settle it.

## Stump power (Gate F)
Strong per the thread: the register shows EM-119 (independent) and EM-102 (nested) identically, so the default of subtracting all 17 files "met the target" with no warning. Catching the nesting needs a pairwise half-hourly screen. Note for the main thread: a strong solver who screens increments will land it, since the hierarchy is findable from the data; the design note's ladder and the "full includer" limit on the asks should be weighed against the 60 build target.

## Findings, ranked
1. (Optional, low) Scope 2 rounding path: 396.9 against 397.0, and 1,916 against 1,917. Closing it by a prompt pin (round once at the end) would need a rerun, and the judge does not require it.
2. (Low) Gas oil Q1 opening assumes no run on 29-31 Dec; the Q2/Q3 apportionment relies on the run-based reading, which cl. 4.2 supports.
3. (Info) The met file is the weaker distractor.

## Next action for the author
Ship as is (APPROVE). If a pin is wanted, add "rounded once at the end" to prompt.txt and re-run the free gates; otherwise carry both residual edges as known.
