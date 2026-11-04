# determinism-check report (pass 2), task488, 2026-11-04

Scope: final cut, target.zip sha256 dde9588d06276d40733dbca49a6148846424ec29678cc6024dea486d3e568532. Fresh scratch /tmp/determinism-check-task488-v2p2-1793788450/; the thread saw no earlier report. Judge thread verdict: /tmp/determinism-check-task488-v2p2-1793788450/verdict.md. This pass supersedes the pass-1 APPROVE for this cut only.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance (hydraulic and mixed-tank mass-balance trace), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
A segment-level FIFO plug-flow model over the register's 44 segments, fed by 200 Corbel and 113 Northgarth tickets (void dropped), idle-pit flushes and Monday drains, reproduces every committed answer. The model's draw total matches SCADA pump-station flow within 52 L/min in every minute from 13:00Z 13 Oct to 12:30Z 14 Oct, so there is no unticketed draw and no timing slack. All 31 density samples agree with the model's batch call. No surviving competing answer except the rack-line carry-over, which the evidence forces.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pier B (HB-06, HB-07) | 6,600 L | 6,587 L | Yes |
| Cargo apron (HE-01 to HE-03) | 11,000 L | 10,996 L | Yes |
| Remote stands (HF-01, HF-02) | 3,600 L | 3,625 L | Yes |
| Other sections | none | 0 | Yes |
| Hydrant uplifts with batch | 73 (A33 B20 C13 E4 F3) | 73, same split, every ticket id | Yes |
| Refueller uplifts with batch | 13 | 13, each within 5 L | Yes |
| RF-23 / RF-24 / T-31 / T-35 | 3,070 / 310 / 14,680 / 2,340 | 3,067 / 306 / 14,680 / 2,343 | Yes |
| Airline totals (Brightwing, Northcove, Orvelle, Sablewood, Tallowmere, Vireo) | 4,130 / 10,740 / 240 / 7,550 / 3,020 / 330 | 4,133 / 10,742 / 239 / 7,549 / 3,018 / 330 | Yes |
| 22 partial hydrant rows | per item 5 | all within 21 L of golden | Yes |

Grading bands (item 5): inside the stated band under gross-vs-15C litres, flush instantaneous/5/20 min, line-up minute -2/+2/+10, changeover +-1.5 min, pipe volume +-0.3%. They break only on readings the files contradict (changeover +-2 min or more, pinned to 22:40Z by SCADA and the shift log; pipe volume +-1%; line-up +-30 min against SCADA). Bands are determinate and licensed. Section totals sit 25 to 46 L from a 50 L rounding boundary under defensible variation.

## Competing answers that survived
- Rack-line carry-over (RK-01, 4,222 L pushes the previous source ahead of each load). Ignoring it gives 10 refueller uplifts, not 13 (T-35 and Vireo drop out), RF-23 4,270 L, RF-24 426 L. No document states the rule; the line fill is shipped with no other use and the load times straddle the 06:00 and 12:20 rack changes, so the judge classed it as forced by evidence, the softest point. It moves part of the main recommendation (drain list: T-35) and the asks.
- N-7 on T-31 vs T-35: closed by the vehicle log; no ticket near the 18:52 to 18:58Z boundary.
- RF-23 to RF-24 transfer (3,843 L): in the equipment log; used.
- Rounding: RF-24 306, CB418424 124, CB418399 274, CB418369 276 sit within 1 to 2 L of a 10 L boundary; graded within 10 L in item 4. Confirm the PDF totals are graded with the same tolerance.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / big file | 10+, 3+, 25,000 rows | 17 files; csv, xlsx, pdf; SCADA csv 44,070 rows | Yes |
| Distractors | 2+ in metadata.json, none labelled by file name | pit_valve_inspections_2026-q3.xlsx, stock_reconciliation_2026-09.pdf; names carry no label | Yes |
| Distractors unused, relevant | yes | Thread found both unused by the solution and plausible to weigh; neither answers a graded quantity | Yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (csv, pdf); both in golden/ | Yes |
| Asks multi-dimensional, unit and rounding stated | yes | 100 L / 10 L stated in prompt; row-per-uplift, section and refueller grids | Yes |
| Prompt shape, 25+ criteria | identifiable, 25+ | shape 07; design note plans about 30 criteria (not independently counted here, rubric is portal-generated) | Yes (planned) |
| Not LLM-generated; goldens real work products | yes | Thread: operator-style exports, no authoring banners. Golden realism not re-read by me | Yes |

## Gate G reconciliation
Thread: mechanism etl_conformance, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, decisive step segment-by-segment tracking against the product-change line-fill reckoning, nothing planted, every reported reading true. Match. The wrong routes the thread named (one line fill by 18:19; branch turnover) are the design's rivals, not the declared distractors (stock reconciliation, pit valve inspections), so no distractor is load-bearing. Gate G not raised.

## Gate H
Thread: domain pass, layers pass, decisive_step analytical. Card analyst_test and domain_test, and the note's Three rules (swap test, Layer 1 mess, Layer 2 estimand identification by exposure, not semantics, not rule application) agree. Method note for the main thread: the FIFO trace is the field's own plug-flow method, not a withheld rule; QM-09 files what is drained, not where the batch went, and the thread reached the golden by modelling with the data settling the dead-end structure and closed stands, so it is a landable route for a strong solver. Weigh against the note's ladder (stumping 1.3).

## Stump power (Gate F)
Strong per the thread: the product-change reckoning files the hydrant clear and notifies 64 (author's number, not re-derived); the right answer needs the segment trace, closed stands, dead-end branches and mixed-tank/trailer coupling. The trap is structural to the data.

## Findings, ranked
1. Rack-line carry-over is unfiled and decides T-35, the Vireo row and RF-23/RF-24 litres. Evidence forces it; the design note declares it as a hazard and the fork table row 13 asserts the order. Residual risk only. Optional repair: file the WHAT (the rack line holds the prior source's fuel at each load) without the method.
2. Prompt names 8 CSV fields; golden has 9 (adds into-plane agent). Harmless; name it or drop it.
3. Near-boundary refueller roundings, absorbed by the 10 L grading; confirm the same in the PDF totals.

## Next action for the author
None required; proceed to ship the final cut. Optionally resolve finding 2 (one phrase in prompt.txt, or drop the column) only if the cut is reopened anyway, since any edit voids this APPROVE's scope.
