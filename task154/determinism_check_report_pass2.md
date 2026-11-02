# determinism-check report, task154, 2026-11-02 (pass 2, architecture 3 re-judge after the FIX_NOW)

## Verdict
DETERMINISTIC. Every graded figure reproduced from the shipped bundle.
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The June 2014 test gives T 206 m2/d, S 0.00036. The geology extract files the Coldharbour Fault by two grid references. The 2015-2026 observation record, run under the returns' abstraction with the Windle Cross movement removed, separates the models: closed aquifer 0.03 m rms, unbounded 0.31 m. The letter files the test (drawdown on 31 March 2039 from the April 2015 rest level, BH2 at 1,200 m3/d to 31 March 2027, then the applied quantity). Datum is a difference from rest, so it does not enter. At 1,800 the drawdowns are 9.96 / 10.94 / 9.96 m (10 / 11 / 10). Lower Hay Farm limits at 1,328 to 1,331 m3/d, which is 1,300 to the nearest 100 (the midpoint 1,350 is more than 2 percent of T away). The previous FIX_NOW is closed: licence condition 6 now files "a period of 24 hours beginning at midnight, local time", and the controller runs plus the haulier's night shift fix the ticket day.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| T, S (joint Theis, OB1-3; OB3 kPa and BST fixed, Q about 2,164 m3/d) | 206, 0.00036 | 205.7, 3.60e-4, rms 0.0024 m | yes |
| Closed / unbounded rms vs OB record | 0.03 / 0.31 | 0.027-0.030 / 0.298-0.311 | yes |
| Drawdown at 1,800 LHF / KN / HB | 10 / 11 / 10 m | 9.96 / 10.94 / 9.96 | yes |
| Qmax LHF / KN / HB | LHF limits, 1,300 | 1,328 / about 1,635 / about 1,789 | yes |
| LHF at 1,300 and 1,400 | passes / fails | 7.37 / 7.89 vs 7.53 | yes |
| Volume Apr-Sep 2026 | 23,300 / 23,700 / 26,600 / 27,600 / 20,200 / 26,500 | 23,330 / 23,731 / 26,606 / 27,616 / 20,205 / 26,475 | yes |
| Days over 1,200 | 6, 8, 5, 5, 5, 5 | 6, 8, 5, 5, 5, 5 | yes |
| Line 3 litres per litre, Apr 2025 to Mar 2026 | 2.38 2.32 2.38 2.33 2.40 2.33 2.39 2.34 2.35 2.37 2.36 2.33 | 2.3828 2.3220 2.3820 2.3287 2.4020 2.3280 2.3913 2.3380 2.3520 2.3723 2.3576 2.3277 | yes, none on a rounding edge |

## Competing answers that survived
Main call: none. Second readings and their figures:
- Plain unbounded Theis with the test's T, S: 5.2 / 7.0 / 5.9 m at 1,800, so 1,800 passes (Qmax about 2,600, Kilnbrook). Contradicted by the fault in the geology extract and the record fit.
- Unbounded refit to the monthly record (T 112, S 1.1e-3): LHF 7.42, KN 10.62, Kilnbrook limits, about 1,700. Contradicted by the test (rms 0.0024 at T 206) and fits worse (0.055 vs 0.028).
- 24 years against 24 years less a day: no change.
Returns ask (all closed by a shipped fact):
- UTC day: (23,400, 7), (23,700, 8), (26,600, 5), (27,600, 6), (20,200, 4), (26,400, 6). Excluded by licence condition 6, local time.
- Ticket date as printed, no shift: days 5/7/4/6/4/4. Excluded by the controller runs; every ticket's window then holds exactly one run (255 tickets to 255 zero-FM-1 runs after 5 duplicate rows are dropped).
- FM-1 only: days 1/3/1/1/0/3. Excluded: the bulk runs are real pump runs with zero FM-1 flow.
- Run minutes at 24.8 l/s: days 9/11/8/7/6/7. Excluded: the tickets measure the bulk water (ticket litres equal run minutes times 19.5 l/s, r = 0.995).
- Strict ">" vs ">=": agree (nearest day total 1,290 against a day of at least 1,312.9). No run crosses local midnight, so run-start, run-end and pro-rata assignment agree.
Line 3 ask: one residual, low to moderate fork on BSG-1101's size. The brief says "the bottle's size". The export says 700 (stale), the fill weights show 750 nominal (758.8 g mean through March 2026, other SKUs run 1.2 to 1.9 percent over nominal). 700 gives 2.49 2.44 2.49 2.45 2.55 2.43 2.49 2.47 2.48 2.50 2.48 2.47. Measured fill 758.8 gives 2.35 2.29 2.35 2.30 2.37 2.30 2.36 2.31 2.32 2.34 2.33 2.30. The golden is the nominal reading, which the fill weights force against the export. Local-month and UTC-month water agree at 2 dp; no run crosses a month. Optional pin: "per litre of nominal bottle size".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 4 (csv, docx, pdf, xlsx) | yes |
| Large file | 25,000+ rows | telemetry 52,608 rows | yes |
| Distractors | 2+ in metadata, none labelled by file name | bh2_water_quality, brackenholt_rain_gauge; neither answers a graded quantity and neither is named in a file name | yes |
| Distractors unused, relevant | yes | water quality and rain gauge unused by the solution, plausible for a borehole licence; the stale SKU export (700) is a Layer 1 trap, not a declared distractor | yes |
| Deliverables | 1-3, all in golden | 2 (variation note PDF, returns CSV); both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 3 drawdowns, a chart, 12 monthly ratios, 6 months by 2 figures; the prompt's last sentence states every unit and rounding | yes |
| Prompt shape, 25+ criteria | yes | shape 13; main call plus about 40 graded figures | yes |
| Prompt | one paragraph, under 1,000 chars | 999 chars, no persona or bullets | yes |
| Reads as real, not LLM generated | yes | judge found real-looking mess and no authoring disclosures; goldens' realism is for golden-realism, not tested here | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_strategy forecast_method_backtest, stump_class analytical, decisive_rule_filed false, official_decoy false. Match. The declared distractors (water quality, rain gauge) are not the surface read; the surface read is the unbounded Theis fit to the test, which the data refute. No shipped artifact ranks the protected boreholes wrongly. Gate H line: domain pass, layers pass, decisive_step analytical. This matches the design note's `## Three rules` (domain test, Layer 1 / Layer 2, analyst test: 2,600 / 1,700 to 1,800 on the easy routes, 1,300 only with the fault).

## Stump power (Gate F)
Moderate to good. The easy route is an unbounded Theis fit from the test (rms 0.0024), filing "1,800 passes". Only a solver who back-tests boundary models against the observation record, or reads the fault as a closing boundary, files "no, 1,300". The refits land on the wrong limiter (Kilnbrook) and a wrong quantity. The thread did not class the step analytical merely because Theis is the field's method; the choice of boundary, validated out of sample, is the judgment. The main thread should still weigh that Theis with an image well is a textbook route a strong solver can reach (`stumping` 1.3), and that nothing in a file states the fault stops water. The asks carry independent Layer 1 traps (night-shift ticket day, bulk bay outside FM-1, UTC against local day, BSG-1101 size).

## Findings, ranked
1. Low: BSG-1101 bottle size on the line 3 ask ("the bottle's size") leaves a measured-fill reading (758.8 g) at 2.29 to 2.37. Forced to nominal 750 by the fill weights against the stale export. Optional prompt pin, no figure moves.
2. Low: the ticket +1 day (before noon, the night shift) is stated in no file; it is recoverable only from the controller events and the one-to-one match. It is data semantics on an ask, which the rules permit, and it is forced.
3. Hygiene: the geology prose places the Windle Cross road crossing at SJ 87040 39350, but the drawn road crosses the fault near northing 40.6 km. The fault trace is consistent between text and map, so the stump is unaffected.

## Next action for the author
None required for determinism. Proceed to ship once the leak check and the other gates are green. Optionally pin "per litre of nominal bottle size" in prompt.txt, which would need a re-run of the free gates (the prompt is at 999 of 1,000 characters, so it would need an equal trim).
