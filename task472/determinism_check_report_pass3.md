# determinism-check report, task472 (pass 3), 2026-11-01

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: binding_constraint, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (fresh unzip, 17 files) reproduced every committed figure from the bundle alone. All 784 actual sailings are reproduced to the minute by Harbor Master's Directions 3.4, 8.1, 9.2 and 9.3, the tide file, the register's LOA and draft, and the pilot record, so the sailing model is forced by the data. Millrace 887 leads Halyard 556 by 331 under the literal reading. Gates A to E pass. This re-check follows the removal of the data dictionary and manifest, rules 2.3, 3.8 and 3.9, the SRT_LABOUR_HRS rename and the prompt reword; none of these opened a fork.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Large-vessel FY2026 calls | 784 | 784 | yes |
| Berth hours saved (MRW/HLY/PNC/ORD/GNP/SLT) | 887/556/449/423/395/257 | 886.76/555.70/448.76/422.76/395.28/257.19 | yes |
| Margin | 331 | 331.06 | yes |
| Ask A breakdown hours (ORD/PNC/GNP/HLY/SLT/MRW) | 1,273/972/501/1,121/704/1,718 | 1273.3/971.7/500.8/1120.8/703.8/1717.8 | yes |
| Ask B labor hours (same order) | 2,981/3,191/1,753/3,061/2,268/3,595 | 2980.75/3190.75/1752.75/3060.75/2268.00/3594.75 | yes |

## Competing answers that survive
No fork on the call or on any graded figure. Variants tested:
- Naive 0.2 x cargo work: Saltworks 991, Pine Neck 804, Millrace 531. This is the easy route and a wrong answer, not a rival reading of the files.
- Fixed-lag notice mapping (the shipped text does not state how the notice moves): lag 1.0 h gives MRW 885, HLY 559, PNC 452, ORD 425, GNP 399, SLT 257; lag 0 gives MRW 930, HLY 649. Millrace wins in every variant, so the call holds. The whole-hour terminal figures and the 331 margin are tied to the equal-shift reading (notice brought forward by a fifth of cargo work, stated in rule 3.6 per the solution steps). That reading is the only one that reproduces the record, so residual risk is low.
- Per-call two-decimal rounding then summing: 886.79/555.71/448.76/422.76/395.30/257.18, the same whole hours.
- Ask B DEFECT-class SRT jobs carry no down/up time and are dated by RAISED. The result is unique (adds exactly 27.00 MRW, 42.25 SLT), but the date convention is not written down. Minor note, no competing figure.
- Moved cranes Q08, Q13, Q28: last-activity and next-activity attribution give identical results.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 17 / 5 (csv, json, txt, pdf, xlsx) | yes |
| Large file | 25,000+ rows | tos_crane_activity 80,059 rows; srt_tos_export 38,781 | yes |
| Distractors | 2+ in metadata, none labelled by file name | 3 named (ais_berth_segments, cmms_yard_equipment_work_orders, berth_windows_fy2027) | yes |
| Distractors unused, weighed, ruled out | unused by solution; shipped fact rules out | AIS measures time alongside (not read); yard equipment excluded by asset type; 2027 windows are next year's. Judge saw no graded quantity answered by them. | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | six-terminal asks; unit and rounding in prompt | yes |
| Prompt shape / rubric | identifiable, 25+ criteria | design note counts 28 from structure (not regenerated here) | yes (per note) |
| Reads as real / not LLM | yes | judge found no authoring language | yes |

## Gate G reconciliation
Thread: mechanism binding_constraint, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, stump sentence is the constrained sailing counterfactual (default Saltworks 991, golden Millrace). Match. The declared distractors (AIS, yard orders, 2027 windows) were not named by the thread as carrying the task, so none is too load-bearing. No shipped artifact ranks terminals on the decision question.
**Gate G: PASS.**

## Stump power (Gate F)
Good. The 0.2 x cargo work route, which a strong analyst reaches by reading rule 3.6 literally, files Saltworks (991 against Millrace 531). Landing Millrace needs the finding that the tide window and 0600 to 2000 limit bind the sailing, so a faster finish only moves the sailing to the next permitted slot. The thread notes the executing of 8.1 and 9.2 is partly rule application, but no text directs the solver to apply the Directions to the counterfactual, so choosing that model is the analysis. Not a textbook route a solver lands by default. Name and call-sign matching, DST tide times and cross-system dedup add cost on the asks.

## Findings, ranked
1. None blocking.
2. Low: the notice-mapping convention (equal shift by a fifth of cargo work) rests on rule 3.6 plus the record; the call is invariant to it, only whole-hour per-terminal figures and the margin depend on it.
3. Low: DATE convention for DEFECT-class SRT jobs (RAISED) is unstated in Ask B but forced numerically.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test. Design note's Three rules lines (No decoy, Not semantics, Not rule application) agree.

## Next action for the author
Proceed to ship; optionally state the DEFECT-class dating convention in the SRT sheet or rules if a one-line fix is wanted.
