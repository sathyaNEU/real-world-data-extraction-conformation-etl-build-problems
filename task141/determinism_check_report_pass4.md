# determinism-check report, task141, pass 4, 2026-10-27

Scope note: this report records the pass that sent architecture 4's nearest-100 plan figure back. It judges only the r4 scratch copy of target.zip sha256 9d45538d7ae0b10a (scratch /tmp/determinism-check-task141-r4/). The task folder has since moved on: the generator was repaired after this verdict (the call is now the pods alone, the golden re-centred at 1,424 in the seven-pod band, new zip 2cea32997e4cbfa8), and a fresh pass 5 judges that zip. Nothing below speaks to the new zip. Earlier reports are untouched.

## Verdict
NOT_DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: forecasting (regime change, comparison-group choice for the end-of-term rate), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is one nearest-100 admissions figure (1,400) plus a pod count (7), both from one modelled quantity. The golden (1,383) sits 33 above the 1,350 rounding line and 123 above the 1,260 six-pod line. The thread rebuilt the projection from the shipped files and the filed rules and got about 1,280 to 1,350 (rounds to 1,300), and about 1,230 (6 pods) when it did not re-expose an extended term to a second end-of-term window. Unfiled choices: extension length and share, window denominator (early-terminated windows in or out), filing-day treatment, and conditioning on windows already open. The prompt says only "as the records show them acting". The author's own variant list holds a 6-pod construction (1,108). Confidence moderate: the thread's projection was cruder than the author's, so this is "not shown to be forced". Gates B, D, E clean; Gates A and C hit for the main call and asks 1 and 2.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Open felony terms at 30 Sep 2026 | 7,598 | 7,598 (cms2) | yes |
| Terms ending 31 Mar 2027 | 3,003 | 3,003 (3,002 if in-force date from orders; 12 same-day tolling/extension pairs) | yes |
| Petition share, last 120 days, at class maximum | about 2 in 5 | 38.0% (9,729 windows) | yes |
| Petition share, with room | 6% | 6.3% (19,625 windows; 53% extended) | yes |
| Trailing-year admissions | 833 | 833 | yes |
| Pooled-rate version | 886 | about 950 | consistent, same 5 pods |
| Pending / through-term / new starts | 34 / 206 / 175 | not rebuilt / about 200 / 179 | consistent |
| Run-out petitions, no room | 863 | 768 to 829 | no, 5 to 11% low |
| Run-out petitions, with room | 105 | 29 plus 73 to 79 second windows | only with second windows |
| Projection total | 1,383 | 1,282 to 1,350 (about 1,230 without second windows) | NO |
| Probationers by office and time (16 cells) | table | identical (officer's office on 30 Sep 2026, completed years) | yes, under that reading |
| Bed-days Q4 2025, Q2 2026, Q3 2026 | 24,970/2,219; 23,100/2,062; 24,762/2,475 | identical | yes |
| Bed-days Q1 2026 | 24,266 / 2,281 | 24,310 / 2,261 | NO |

## Competing answers that survived
1. Admissions 1,300 against 1,400: window rate and denominator (0.38 against about 0.395 to 0.41), second windows for extended terms, extension length (12 months, 9 months, latest end under the Act) and share, all unfiled. Result crosses the 1,350 line.
2. Pods 6 against 7: the "lost extensions shared between petition and lapse" reading gives 1,108. Weaker reading, but the data cannot show whether a capped term behaves like an observed at-max term or a with-room term.
3. Ask 5 office: the cms2 `office` column (case office at intake) against the officer's current office gives a different table (Eastfield 426/121/0/0 against 381/301/231/269). The officer reading is better but unfiled; instructions 6.1 say "each office supervising them".
4. Ask 5 time on supervision: completed years against 365.25-day years moves 3 to 4 cells by 1 to 4 people.
5. Ask 4 Q1 2026 bed-days: golden not reproduced (felony +44 and misdemeanor -20 in the thread's count, also without ID merging).

## Spec gates
Checked by me against /tmp/determinism-check-task141-r4/target/.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | CSV, PDF, XLSX | yes |
| Large file | 25,000 rows or more | detention_probation_bookings 45,550 rows (also term orders 17,765, petitions larger) | yes |
| Distractors | 2 or more in metadata.json, none named in a file | apd_annual_report_2025.pdf, detention_daily_headcount_2025_2026.csv; file names do not label them | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | FY aggregates and 06:00 headcount against midnight bed-days and the instructions' definitions; thread confirmed unused | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, docx, png), all in the golden folder per submission | yes |
| Asks multi-dimensional with unit and rounding | yes | yes (quarters, office by tenure cross-tab, nearest 100, whole days) | yes |
| Prompt shape and 25+ criteria | identifiable, 25 or more | shape identifiable; rubric count is generated downstream and was not counted here | not verified |
| Reads as real, not LLM | yes | thread found no authoring language in PDFs or code tables; golden realism not re-read | yes (thread) |

## Gate G reconciliation
Read after the verdict, from DESIGN_NOTE.md and metadata.json. Thread: mechanism forecasting with a comparison-group choice, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no, Gate G pass. Design note: family `estimand_identification`; the flip is the comparison group for capped terms' end-of-term petitions (terms already at class maximum), stump sentence naming the pooled-rate route (5 pods). These agree; the thread named the pooled-rate and trailing-year routes as the easy routes, not the declared distractors (annual report, headcount), which it called unused. No finding on distractor load. The note and golden have since moved to 1,424 and a pods-only call, so this reconciliation covers the r4 zip only.

## Stump power (Gate F)
Both easy routes land off the call (pooled about 886 to 950, 5 pods; trailing 833, 4 pods). The data separate at-max windows (38%) from windows with room (6%, 53% extended), so the trap is real and analytical, with Gate H: domain pass, layers pass, decisive_step analytical. The decisive step is an estimand choice, not a method the field standardises with no judgment, so no downgrade. The weakness is margin, not stump.

## Findings, ranked
1. The nearest-100 admissions figure is not forced: a literal rebuild spans 1,300 to 1,400 and the golden is 33 above the line. Fix by widening the margin (re-centre well inside a 100 band) or filing the WHAT of the projection (extension a term with room receives, window denominator, windows already open).
2. Pod count 6 against 7 hangs on the same unfiled choices at the low end (about 1,230).
3. Ask 5 office unfiled (officer's office on 30 September 2026 against case office).
4. Ask 5 tenure unit (completed years) unfiled; 1 to 4 people in 3 to 4 cells.
5. Q1 2026 bed-days not reproduced by the thread (24,310 / 2,261 against 24,266 / 2,281).

## Next action for the author
Already taken by the main session: the generator was repaired (pods-only call, golden re-centred at 1,424, zip 2cea32997e4cbfa8) and pass 5 is judging it; use that verdict, and confirm in it that ask 5's office and tenure wording and the Q1 2026 bed-days are closed.
