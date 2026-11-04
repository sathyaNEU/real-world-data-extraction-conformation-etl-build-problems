# determinism-check report, task210, pass 2, 2026-11-04

Pack judged: target.zip sha256 bab3e3210c945c61fffd26f0d722a54c328a74f6e763181a757851ae6549c9b7 (new pack: ladder hardened, data and 25 graded cells changed since pass 1). The pass-1 report was not shown to the thread and is untouched.

## Verdict
DETERMINISTIC (the thread also marks SOLUTION_WRONG on one wording point only: solution step 5).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Process note
This pass's brief inlined the graded blocks (final recommendation, deliverable answers, critical components, solution steps) in the brief itself. The determinism-check skill says they belong in their own file, which the thread opens only once its own derivation is on disk. The brief therefore relied on the thread choosing not to read the answers before deriving, and the thread did not report whether it kept the order. By the skill's own words this pass's Gate C evidence ("the answer was forced") is the weaker kind: a judge that cannot be surprised cannot tell you the answer was forced. The skill also says a pass that broke the order does not spend the architecture's one re-judge; the breach is the orchestrator's. The thread's recomputation (below) is independent evidence for Gate A and the readings, but its Gate C verdict should be weighed accordingly. The next pass will keep the order (blocks in their own file, opened only after the derivation is written).

## Why
Read literally, the shipped telemetry forces one answer. Pass-forward flow is the pump's delivered rate (fill plus draw between the control levels, from de-duplicated pump cycles): Gallowfen 48 l/s against its 72 l/s permit; every other station clears its permit by 6 l/s or more (closest Sallowholme 57 against 50). Gallowfen is the only breach, so the main call and answers 1 to 3 are forced. Rated duty and drawdown-only are ruled out by the prompt's words and the rising-main meters. The one defect is wording: solution step 5 says the monitor was "installed in the week before it retired", which is 8 days for the 12/11 retirements (Northwade Bank and Reedhaven installed 04/11, retired 12/11). The mapping is still unique by alarm coincidence (21 of 21 for AQ7-19-1137 to Reedhaven), so no fork results and no graded figure moves, and Gallowfen's monitor was never retired.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gallowfen pass-forward (median cycle rate) | 48 l/s | 47.95 (mean 47.88, P90 48.46, night median 48.17) | yes (pump_event + Pumping stations sheet) |
| Gallowfen permit, condition 2.3.1 | 72 l/s | 72 | yes (consents csv) |
| Gallowfen rated duty | 85.3 l/s | 307.1 m3/h / 3.6 = 85.3 | yes |
| 48 as share of 72 | 67 per cent | 66.7 | yes |
| Other 13 stations' pass-forward | 41, 36, 19, 45, 57, 118, 29, 84, 32, 52, 22, 67, 43 | identical | yes, all 14 |
| Closest non-breach | Sallowholme 57 v 50 | same | yes |
| Spill counts, 14 overflows | 15, 12, 30, 57, 15, 13, 11, 14, 13, 17, 9, 20, 9, 11 | identical | yes |
| Hours (1 dp) | 28.9, 20.4, 97.9, 198.2, 24.1, 15.9, 15.1, 29.0, 19.7, 23.3, 17.4, 31.5, 12.3, 20.9 | 28.88, 20.41, 97.94, 198.21, 24.11, 15.88, 15.14, 28.98, 19.72, 23.27, 17.41, 31.54, 12.26, 20.86 | yes |
| Monitored per cent (1 dp) | 100.0, 99.5, 99.9, 98.0, 97.4, 99.8, 98.5, 99.4, 98.8, 99.9, 100.0, 99.4, 99.7, 99.8 | 100.00, 99.48, 99.87, 97.97, 97.42, 99.80, 98.53, 99.43, 98.79, 99.89, 100.00, 99.41, 99.67, 99.85 | yes |
| Step 5 "week before it retired" | one week | 8 days for Northwade Bank and Reedhaven (04/11 to 12/11) | no (wording) |
| Monthly chart cells | as drawn | spot-recomputed: all seven near-tie cells reproduce (table below) | yes for the cells the thread listed; not all 168 cells itemised |

## Competing answers that survived
None on the main call. Readings tested, with the thread's recorded answer:

1. Rated duty of the running pump: 41.6, 85.3, 36.8, 19.7, 47.2, 58.9, 118.5, 28.4, 86.3, 33.5, 52.7, 22.6, 67.1, 44.9 l/s, all above permit. Flags none, would file "none breached". Ruled out by the prompt ("the flow the station was passing forward while it spilled": a datasheet duty is not a measured flow) and by Gallowfen's telemetry (48 against 85.3). The thread notes a residual risk: the three meters read 97 to 100 per cent of rated duty, and no shipped file states that rated duty is not the operating flow. A weak competitor, not a surviving fork.
2. Drawdown only (net of inflow), flagged stations on each variant:
   - median of all runs: Gallowfen 39.5, Hagworth Wold 12.2, Marram End 15.0 (three);
   - night runs (22:00 to 06:00 local): Gallowfen 41.5, Hagworth Wold 13.2, Marram End 15.9 (three);
   - 90th percentile: Gallowfen 42.2 and Hagworth Wold 15.0 only; Marram End 16.3 passes (two);
   - mean: the same three as the median.
   No variant names a single overflow, so none yields one self-report. A solver who keeps the route and names its outlier would file Hagworth Wold (ratio 0.39 of permit), which is wrong; the design anticipates this as rung 0b. Ruled out by the rising-main meters (117.8 / 83.8 / 66.8 l/s against fill-plus-draw 117.9 / 83.8 / 66.8 and drawdown alone 103.3 / 76.0 / 61.7). Gallowfen, Hagworth Wold and Marram End have no meter, so the refutation there is by analogy and by the meaning of "passing forward". Reconciliation note for the author: the design note's ladder says Marram End is "above it at night" on this route; the thread's 22:00 to 06:00 window gives 15.9, below 16. The night window is not filed, so the number depends on the window chosen; the conclusion (no single overflow) holds either way.
3. Delivered rate with inflow added back: the golden. Flags Gallowfen only (48 v 72); would self-report Gallowfen's overflow (12 spills, 20.4 h). Validated by the meters.
4. Stations flagged and self-report: rated duty none; drawdown three or two as above; fill-plus-draw Gallowfen only.
5. 24-hour block: "any part" gives the golden; "starts only" gives Hagworth Wold 29 (not 30) and Marram End 54 (not 57), the other twelve unchanged. Ruled out by WW-ENV-PR-014 s3 ("A block contains discharge when any part of a discharge falls within it"). Gallowfen is 12 either way.
6. Monitored percentage, average against daily maximum: the average moves 11 lines (Scarrow 99.9, Cressfleet 97.3, Sallowholme 99.7, Northwade 98.4, Brackenings 99.3, Thornmarsh 98.6, Kettlewade 99.8, Saltwade 99.9, Reedhaven 99.3, Sedgefleet 99.5, Swathe 99.7); Gallowfen, Hagworth Wold and Marram End are unchanged. Ruled out by procedure s5 (hours "monitored and the monitoring data reached the company" is met if any monitor reported). Does not touch the main call.
7. Log clock: the log leads the UTC alarm clock by 1 h in summer (lag to raised_utc 20 to 125 s when read as UK local time, about 3,700 s otherwise), so the data force local time. Read as UTC, no count, hours figure or chart cell moves, and the mapping winners are unchanged. Procedure s2 files the reporting year as UK local time.
8. Rounding ties: see below.

### Reading 8, chart cells within a minute of a rounding line
No return-line figure is within 0.03 of a tie (closest 98.785 against 98.75). Seven monthly chart cells lie within a minute of a one-decimal rounding line:

| Cell | Unrounded hours | Rounds to | Distance to the line | Graded | Determinate on the second-resolution log |
|---|---|---|---|---|---|
| Hagworth Wold Jan | 8.9494 | 8.9 | about 2 s | yes, a labelled chart cell of ask 1 of the SVG | yes, for a faithful recompute |
| Cressfleet Oct | 0.6494 | 0.6 | about 2 s | yes | yes |
| Cressfleet Nov | 3.2508 | 3.3 | about 3 s | yes | yes |
| Brackenings Oct | 0.2508 | 0.3 | about 3 s | yes | yes |
| Reedhaven Dec | 4.6519 | 4.7 | about 7 s | yes | yes |
| Gallowfen Sep | 2.3483 | 2.3 | about 6 s | yes | yes |
| Sallowholme Sep | 2.0478 | 2.0 | about 8 s | yes | yes |

The thread found all seven exact on the log (start and end written to the second) and flipping only if a solver rounds durations or merges the handover overlaps differently: deterministic for a faithful recompute, fragile for an approximate one. Distance column is my conversion of the thread's 4-decimal hours (rounded values, so +/- 1 s); I did not independently recompute the cells. Reconciliation note: checks.py asserts only that no month cell is within 0.0005 h (1.8 s) of a half; the design note's "seven seconds or more" applies to the hours figures. The two Hagworth Wold and Cressfleet Oct cells sit near that floor. The main call, the self-report figures (48, 72, Gallowfen 12 spills, 20.4 h, 99.5 per cent) are far from any tie.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv x8, sqlite, xlsx x2, pdf) | yes |
| Large file | 25,000 rows or large database | rainfall 175,200 rows, flow meters 105,120, sqlite pump_event 324,394 rows (34 MB) | yes |
| Distractors | 2 or more named, none labelled by file name | 4 named in metadata.json (rainfall, groundwater, improvement plan, work orders); file names do not label them | yes |
| Distractor behaviour | unused by the solution, weighable, ruled out by a shipped fact | rainfall feeds the dry-day screen (Hagworth Wold), ruled out because the station passes 36 l/s against 31 through those spills; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden, no format family required | 3 (docx, csv, svg), all three present in golden/ | yes |
| Asks | multi-dimensional; unit and rounding stated | prompt states whole l/s, hours and percentages to one decimal; 14 lines by 6 fields plus a 14 by 12 grid | yes |
| Prompt shape and rubric | shape identifiable; 25 or more criteria | shape 10 on the card; per-overflow lines and chart cells give well over 25 gradable figures | yes |
| Prompt | one paragraph, under 1,000 characters, no data count | 940 characters, no count the data hold | yes |
| Reads as real | no LLM tells; goldens read as work products | thread found no authoring language; goldens not separately reviewed here | yes (thread) |

## Gate G reconciliation
The thread's mechanism (method_or_model_selection), stumping family (analytical_non_defect), surface_read_dependency (no) and sole_data_defect (no) match the card: stump_strategy binding_constraint, stump_class analytical, layer2_family field_method, official_decoy false, decisive_rule_filed false, and the design note's statement that nothing is planted. The thread named the rated duty and the drawdown-only route as the easy reads, both of which the design note places at rungs 0 and 0b. Neither is a declared distractor: metadata.json names rainfall, groundwater, the improvement plan and the work orders, and the thread did not make any of them carry the task (the groundwater and rainfall files are what close the Hagworth Wold dry-day route). No shipped artifact ranks the candidates wrongly. Match, no finding.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. This matches the design note's `## Three rules` (domain_test: delivered rate from wet well fill and draw; Layer 1: UTC against local time, re-sent events, m3/h against l/s, mAOD against depth, duplicate-key monitors; Layer 2: inflow-corrected delivered flow; No decoy, Not semantics, Not rule application all answered) and the card's analyst_test and domain_test. The thread did not class the step analytical on the grounds that the golden is the field's standard method; it reached the golden by applying a measurement the data support, and the design note itself puts the field's desk test (rated duty) at the wrong rung. No mismatch.

## Stump power (Gate F)
Moderate to good, per the thread. The easy routes are nameplate duty (none breached, with an m3/h conversion) and drawdown-only (flags Gallowfen, Hagworth Wold and Marram End on three of four variants, so the wrong set; the natural single call is Hagworth Wold). Getting 48 needs the inflow correction (V/ton plus V/toff), validated against the rising-main meters. A careful solver who finds the meter files can reconstruct it, and the 24-member estimator family agrees to the whole l/s, so the golden is reachable; the main thread weighs this against the design note's ladder. Note the thread worked with the answers in its brief, so its Gate F and C judgments are the weaker kind.

## Findings, ranked
1. Solution step 5 (and the design note's SF18) says the monitor was installed "in the week before it retired"; it is 8 days for the 04/11 installs retired 12/11 (Northwade Bank, Reedhaven). SF19 of the design note already says nine days. Wording only; mapping unique by alarm coincidence; no graded figure moves.
2. Seven chart cells lie within a minute of a rounding line (table above); two within about 2 s, the design's own assertion floor is 1.8 s. Deterministic on the log but fragile; consider noting or shifting a draw.
3. Night-run drawdown for Marram End is 15.9 on the thread's window against the design note's "above it at night": the window is unfiled; conclusion unaffected.
4. Rated-duty reading carries a small residual risk (meters read 97 to 100 per cent of rated duty; no file says rated duty is not operating flow).
5. Process: blocks inlined in the brief; Gate C evidence weaker; the one re-judge is not spent.

## Next action for the author
Reword step 5 of `submission.md` (and the design note's SF18 to match SF19's nine days) so the retired-serial mapping does not rest on "the week before it retired"; change no input file, the prompt or the goldens, then re-run `figures_check.py` and the pre-ship gates and ship.
