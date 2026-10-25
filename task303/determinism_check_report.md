# determinism-check report, task303, 2026-10-25 (run r3, replaces r2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, the plan values each project at nine in ten of the vegetation, wind and wildlife customer-minutes on the backbone devices (feeder breaker, line recloser) outside accepted major event days, over seven. After the simultaneous substation-supply trips are removed, F-205 leads at 237,615 against 137,771 for F-112. The 20 supply-loss events are separable with no near-miss (all feeders at the substation open in the same minute, same cause). The thread reproduced every golden figure. The r2 fixes (restoration_utc filed, legacy DUR_MIN format filed, prompt reworded to accepted major event days) hold, and no golden moved.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Conversion, F-205/F-112/F-301/F-208/F-303/F-114 | 237,600/137,800/67,300/39,000/32,100/29,600 | 237,615/137,771/67,316/38,986/32,086/29,634 | yes |
| F-205 value at USD 2.10 | 499,000 | 498,992 | yes |
| Credit-every-breaker reading (F-112, F-114) | 455,400 / 285,400 | 455,450 / 285,449 | yes |
| Storm-day customer-minutes (F-112, F-114, F-205, F-208, F-301, F-303) | 11,615k/5,773k/7,332k/6,210k/9,952k/4,391k | 11,614,771/5,773,110/7,332,062/6,210,057/9,951,819/4,391,082 | yes |
| Storm-day minutes per customer | 411.9/339.7/393.5/413.5/406.1/420.3 | identical | yes |
| Tap customer-minutes a year | 23,840/14,450/25,950/9,000/16,410/13,540 | 23,841/14,452/25,951/9,001/16,413/13,540 | yes |
| Tap minutes per customer | 125.1/116.3/119.2/116.5/110.6/118.5 | identical | yes |
| Critical component 1 (12 / 3 / 0 simultaneous trips) | 12 / 3 / 0 | same | yes |

## Competing answers that survived
- Credit every breaker ticket: files F-112 (455,400). The single competing answer, closed by the plan's "faults on the converted backbone" and "would have removed" wording (a trip opening all three breakers is not a fault on one backbone) and by the data signature. The removal rule itself is not stated in a file; the thread judged it forced by the counterfactual estimand and advised against pinning it. Recorded as residual risk, not a failure.
- Legacy decimal DUR_MIN start: under the literal ticket-date reading the tap figures move (F-112 34,886; F-301 63,523 a year); the call does not move. The now-filed format closes it, and the ticket-order consistency discriminates. Asks only.
- Crew clock (EST vs local): the files support EST (En route precedes Assigned by about 48 minutes; 536 tickets with OMS restoration exactly 60 minutes earlier). Local reading gives F-112 11,068,651. Closed by the shipped notes. Asks only.
- Crew Restored vs OMS restoration: OMS reading gives F-112 14,020,061; closed by "lost" and the filed storm-desk entries. Asks only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, txt, docx) | yes |
| Large file | 25,000 rows or more | storm_crew_status_2023_2025.csv, 29,451 rows | yes |
| Distractors in metadata.json | 2 or more, none named by file name | vegetation_work_orders_2017_2026.csv, line_recloser_settings_2026.xlsx; names are neutral | yes |
| Distractors unused yet weighable | arithmetic reproduces, shipped fact rules out | thread listed them as unused by the solution; I did not separately recompute an answer from them | not independently verified |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx) | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-feeder, three-fold figures, rounding stated in prompt | yes |
| Prompt shape, 25 or more criteria | yes | shape 01 in metadata; 6 candidates plus 24 workbook cells plus value and call, above 25 by count | yes |
| Reads as real, not LLM generated | yes | thread found plan and order realistic; no leakage | yes |

Minor hygiene flag from the thread: major_event_days `accepted_in` cites Docket E-2024-031 for 2023 days, while the PDF is the March 2024 stipulation order, which does not itself accept days. Not exclusion-level.

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's Layer 2 (field_method: attribute each interruption to its origin; a supply loss is no backbone fault) and decisive step (separating same-minute breaker tickets across the substation's feeders before crediting nine in ten) match. No shipped artifact ranks candidates, and the declared distractors are not the surface read carrying the task. The thread's borderline remark (attribution versus a planted double-count) is noted; the events are realistic supply losses also appearing at non-candidate substations. No mismatch.

Gate H: domain: pass | layers: pass | decisive_step: analytical. Matches the design note's Three rules.

## Stump power (Gate F)
The easy route (filter cause and device, rank) files F-112 at 455,400 and F-114 at 285,400, a wrong call. Only a common-mode check across the substation's feeders moves it to F-205. The attribution is the field's own standard method and no judgment is left once the idea is had; the main thread should weigh the scored readers' result against that. The asks add independent traps (crew clock, crew versus desk restoration, legacy decimal tickets, event-day placement).

## Findings, ranked
1. Residual: the supply-loss removal is not filed in any shipped file; it rests on the plan's counterfactual wording plus a clean data signature. Thread recommends against pinning.
2. Minor: `accepted_in` docket reference does not match the shipped PDF.
3. Distractor arithmetic not independently verified.

## Next action for the author
Proceed to ship. Optionally correct the `accepted_in` docket text in major_event_days_2019_2025.csv (or the PDF) only if it can be done without moving any figure, and then re-zip.
