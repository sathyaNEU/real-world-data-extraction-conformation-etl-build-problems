# determinism-check report, task303 (run r2), 2026-10-25

## Verdict
DETERMINISTIC (main recommendation forced; every graded figure reproduced). Two ask-level forks are open on the literal text.
**Disposition:** FIX_NOW (optional pins on the two asks; no model rerun for the main call). Not SEND_BACK.
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect (thread wrote analytical_attribution), surface_read_dependency: no, sole_data_defect: no

Pack note: the thread judged the pre-rebuild unzip (all 11 files, hash 784cd964). target.zip was then rebuilt (8f1811e2); the three data files oms_interruptions_2019_2022.csv, oms_interruptions_2023_2025.csv and storm_crew_status_2023_2025.csv differ, the other eight are byte-identical. I re-ran the load-bearing recomputation myself on the new pack (see ledger): every figure is identical to the judged pack. The judged text (prompt, submission, notes) is unchanged.

## Why
Outside the accepted major event days, F-205 removes 237,615 customer-minutes a year (0.9 x backbone breaker and recloser tickets from vegetation, wind and wildlife, over 7). Crediting every breaker ticket to its own backbone gives F-112 455,449. Dropping the tickets that all three feeders at a substation opened in the same minute (Pell Creek 12, Byers Mill 3, Sorrel Hill 0) gives F-112 137,771, about 100k below F-205: a wide, clean margin. The plan says the conversion does nothing for faults elsewhere, and a backbone fault cannot interrupt sibling feeders.

## Recomputation ledger
| Figure | Claimed | Judge recomputed (old pack) | Me, rebuilt pack | Reproduced |
|---|---|---|---|---|
| F-205 / F-112 / F-301 / F-208 / F-303 / F-114 | 237,600 / 137,800 / 67,300 / 39,000 / 32,100 / 29,600 | 237,615 / 137,771 / 67,316 / 38,986 / 32,086 / 29,634 | identical | yes |
| F-112 crediting every ticket | 455,400 | 455,449 | 455,450 | yes |
| Same-minute 3-feeder events | 12 / 3 / 0 | 12 / 3 / 0 | 7+5 / 1+2 / 0 (legacy + current substation labels) | yes |
| USD value | 499,000 | 498,991 | n/a | yes |
| Storm record cm (crew Restored, contract crews EST) | 11,615,000; 5,773,000; 7,332,000; 6,210,000; 9,952,000; 4,391,000 | 11,614,771 ... 4,391,082 | identical | yes |
| Storm min per customer | 411.9 / 339.7 / 393.5 / 413.5 / 406.1 / 420.3 | same | identical | yes |
| Taps cm/yr | 23,840; 14,450; 25,950; 9,000; 16,410; 13,540 | 23,841 ... 13,540 | identical | yes |
| Taps min per customer | 125.1 / 116.3 / 119.2 / 116.5 / 110.6 / 118.5 | same | identical | yes |

## Competing answers that survived
Main call: none. Counting each shared event once, reclosers only, and any n>1 same-minute test were stress-tested (identical figures or not defensible).
Ask-level forks (both repairable by a pin, neither moves the call):
1. Workbook ask 1, restoration source: OMS restoration_utc gives 14,031,730 / 7,375,539 / 8,480,709 / 7,110,809 / 11,959,696 / 5,027,984 (F-112, F-114, F-205, F-208, F-301, F-303); the crew Restored time (contract crews on EST) gives the golden. The prompt does not say which. The crew note ("the crew reported the customers on the job back in supply") and the data (raw contract times put En route before Assigned) favour the golden but never state it.
2. Workbook ask 2, legacy handheld tickets (decimal DUR_MIN, h.mm, OUT_DT the closing day): never stated in oms_export_notes.txt. Reading OUT_DT as the start day gives 32,893 / 30,308 / 42,045 / 21,589 / 27,928 / 34,102. The golden is recoverable (ticket numbers run in start order) but not filed. By design this is an ask-level semantic, which the spec allows.
3. "accepted in 2023 to 2025" read by docket year: strained; the plan's last three years supports the golden.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | csv, xlsx, pdf, docx, txt (5) | yes |
| Large file | 25,000 rows or more | storm_crew_status 29,451 rows | yes |
| Distractors in metadata | 2 or more, no file name labels one | vegetation_work_orders_2017_2026.csv, line_recloser_settings_2026.xlsx; names neutral | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | thread confirmed unused and present; I did not test an arithmetic reproduction of a graded quantity from either | partly verified |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (pdf, xlsx); both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12-figure asks each, rounding in the prompt | yes |
| Prompt shape / rubric | identifiable, 25 or more criteria | shape 01; about 33 graded figures (call, value, 6 candidates, 12 + 12) | yes |
| Reads real, not LLM generated | clean | thread found nothing; the golden/ files were not inspected by me | not independently checked |

## Gate G reconciliation
Thread: decomposition_attribution, surface_read_dependency no, sole_data_defect no. Design note and card: strategy decomposition_attribution (gap population, generators G8 and G3). Match. The surface read the thread names as carrying the task is crediting every breaker ticket to its own backbone, not either declared distractor (vegetation work orders, recloser settings), so the distractors are not too load-bearing. Residual risk: every ticket is true as recorded, but the attribution rests on a fact stated in no field or sentence (the design's readability screen marks it "silent"); the thread treats it as FINE-numbers attribution, and the design's Three rules lines are consistent. The main thread should weigh this with the blind readers' result.

## Stump power (Gate F)
Good. The easy route (sum breaker and recloser tickets, take F-112 at 455,400) is what the design's own call-only probes filed. The decisive cross-feeder same-minute check is never prompted. The over-correction (drop all breaker tickets) files F-301, a second wrong answer. The asks add device-time and handheld-format traps. Gate H reconciliation: thread `domain: pass`, `layers: pass`, `decisive_step: analytical`; design note Three rules and card agree (common-cause attribution by origin; swap test fails). No case of classing the decisive step analytical merely because the method is standard: the thread reached the golden only after testing sibling-feeder coincidence, a judgment the data had to settle.

## Findings, ranked
1. Ask-level fork: restoration source for the storm record (workbook ask 1). FIX_NOW, optional one-line pin of the WHAT.
2. Ask-level fork: legacy handheld ticket format and closing-day OUT_DT (workbook ask 2). Optional pin; it would lower that ask's difficulty slightly.
3. Judge ran on the pre-rebuild unzip; I verified the main call, storm record and taps figures on the rebuilt pack and they match. The thread did not itself test a distractor-arithmetic reproduction.
4. Hygiene PASS, no exclusion-level finding; provenance and license are recorded in metadata.json (CC0, original work).

## Next action for the author
Decide whether to pin the two ask-level semantics in oms_export_notes.txt and the prompt (file the WHAT only, not the method); if not, ship as is, accepting the two ask forks. The main call needs no change.
