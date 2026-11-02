# determinism-check report, task154, 2026-11-02

## Verdict
DETERMINISTIC on the main call; two open readings on the returns ask.
**Disposition:** FIX_NOW (prompt only: pin the returns ask's day clock and ticket day; data, main call and stump stay frozen; no model rerun for the main call)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The pre-application letter files the test (drawdown on 31 March 2039 from the April 2015 rest level, BH2 at 1,200 m3/d from 1 April 2015, then the applied quantity, against the table's available drawdown). The geology extract's Coldharbour Fault and the 2015-2026 observation record (closed model rms 0.036 m against 0.308 m unbounded, recovering the 2014 test's own T and S) force the closed aquifer: Lower Hay Farm limits at 1,330, which is 1,300 to the nearest 100, and 1,800 fails. The returns ask is not closed. The licence says only "a day ... beginning at midnight" (condition 6), the telemetry is UTC while the controller log and tickets are local, and seven tickets straddle midnight.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| T, S (Theis, OB1-3, 25.0 l/s, OB3 kPa and BST fixed) | 206, 0.00036 | 205.3, 0.000359 | yes |
| LHF / KN / HB drawdown at 1,800 | 10 / 11 / 10 m | 9.96 / 10.94 / 9.96 | yes |
| Qmax by borehole | LHF limits, 1,300 | LHF 1,330, KN 1,635, HB 1,789 | yes |
| LHF at 1,300 | passes | 7.37 m < 7.53 | yes |
| Unbounded 2014 T,S | 1,800 passes, KN limits | 2,618 KN | yes |
| Unbounded refit to OB record | KN limits, above 1,300 | T 112, S 0.00108; KN 1,687 | yes |
| Closed / unbounded fit rms | 0.03 / 0.31 | 0.036 / 0.308 | yes |
| Monthly volume Apr-Sep 2026 | 23,300 / 23,700 / 26,600 / 27,600 / 20,200 / 26,500 | 23,330 / 23,731 / 26,606 / 27,616 / 20,205 / 26,475 | yes (local day, ticket on pump-run day) |
| Days over 1,200 | 6, 8, 5, 5, 5, 5 | 6, 8, 5, 5, 5, 5 | yes |
| Line 3 litres per litre | 2.38 2.32 2.38 2.33 2.40 2.33 2.39 2.34 2.35 2.37 2.36 2.33 | 2.383 2.322 2.382 2.329 2.402 2.328 2.391 2.338 2.352 2.372 2.358 2.328 | yes |

## Competing answers that survived
1. Returns, day clock (survives). On UTC days the counts are 7, 8, 5, 6, 4, 6 and volumes 23,400 / 23,700 / 26,600 / 27,600 / 20,200 / 26,400, against the golden's local-day figures. Neither the prompt nor the licence names the clock. The design note's fork row SF17 asserts "same figures under all three" readings, which the judge's recomputation contradicts. The author should re-run that assertion in checks.py.
2. Returns, ticket day (survives). Seven tickets have time in 23:5x and a pump start 00:0x. Counting litres on the ticket's own time-in day gives April 23,357, which rounds to 23,400 (golden 23,300), and shifts the April/May split. Day counts are unchanged.
Closed forks, each with the second reading's figure:
- Unbounded aquifer, 2014 T,S: 2,600 (KN). Unbounded refit: 1,700 (KN). Both are contradicted by the fault and the record.
- Actual returns instead of the filed 1,200 scenario: LHF 1,384, which rounds to 1,400. The letter states the scenario literally, so this is not licensed.
- Rounding margin: LHF 1,330.5 sits 20 below the 1,350 boundary. T from 204 to 207 gives 1,318-1,337, so it holds at 1,300.
- Bottle size: the export's 700 ml gives 2.43-2.55. The fill weights force 750 ml.
- Rejects counted as packed: 2.41-2.52. "Good bottles" closes it.
- Naive ticket date or kept duplicates: day counts 5, 7, 4, 6, 4, 4. Layer 1 mess, forced by the one-to-one match of 255 tickets to 255 pump runs.
- Chart window "over the term" is unpinned. Minor, because the graded content is the plotted series.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10 / 3 / 25,000 rows | 17 / 4 (csv, pdf, xlsx, docx) / 52,608 rows | yes |
| Distractors | 2 or more named in metadata.json, none in a file name | water quality csv and rain gauge csv named; no file name labels one | yes |
| Distractors unused yet weighable | unused by the solution | the thread found the SKU master a weak decoy and the other two unused; I did not independently check that they fail to reproduce a graded quantity | yes (not independently checked) |
| Deliverables | 1 to 3, all in golden | 2 (the PDF note and the CSV), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt files nearest 100 m3/d, nearest metre, 2 decimals, nearest 100 m3 | yes |
| Prompt | one paragraph, under 1,000 characters, no persona | 999 characters, one paragraph | yes |
| Rubric 25 or more criteria | 25 or more | not generated; the design note argues the count from the per-month and per-borehole asks (12 + 12 + 3 + chart + call) | argued, not verified |
| Reads as real, not LLM generated | yes | the thread found no such signs; duplicate tickets, meter rollover, casing change and mixed date formats read as system exports | yes |
| Hygiene note | | line5_project_brief.docx explains the litres-per-litre metric slightly; acceptable | yes |

## Gate G reconciliation
The thread and the design note agree. The thread gave method_or_model_selection and no surface-read dependency, and the note's Layer 2 is forecast_uncertainty with a model chosen on the record. The thread did not name either declared distractor as the surface read. The surface read it names is the correct 2014 test fit, which is not a distractor. Gate G passes.

## Gate H reconciliation
The thread gave domain pass, layers pass and decisive_step analytical, and the card and note's `## Three rules` say the same. The easy route is Theis on the 2014 test filing 2,600 with KN limiting and 1,800 passing, or an OB refit filing 1,700. The fault appears in the geology extract and the record independently confirms it, so it is not a planted decoy. No mismatch was found. The concern is that the geology extract describes the fault, so a strong reader of every file could find it.

## Stump power (Gate F)
The 72-hour test fits an unbounded curve to rms 0.002 m, so a solver who stops at the clean fit files 2,600. The fault and the 2015-2026 record are the separators. The thread's rating is that the main call carries the stump and the asks (UTC against local day, night-shift tickets, bulk water outside FM-1, 750 against 700 ml) hold the top responses down. Neither it nor I classed the decisive step as the field's standard method applied with no judgment, so the main thread should weigh it against the note's ladder. No hardening is advised.

## Findings, ranked
1. Returns ask: the day clock is unpinned (UTC and local days give different counts and volumes), and the design note's SF17 "same figures" assertion does not hold on the judge's recomputation.
2. Returns ask: the ticket day for midnight-straddling tickets is unpinned (April 23,400 against 23,300).
3. The chart's "over the term" window is unpinned (minor).
4. The rubric count is not verified.

## Next action for the author
Edit `prompt.txt` to file the WHAT for the returns ask, for example "days run local midnight to midnight and each bulk load counts on the day its pump run began", staying under 1,000 characters (the prompt is at 999, so tighten other words). Then re-assert SF17 and SF15 in checks.py, rebuild twice byte-identically, and re-judge once. Optionally pin the chart window to 31 March 2016 to 2039.
