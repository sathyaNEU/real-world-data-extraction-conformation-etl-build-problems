# determinism-check report, task468, 2026-10-17

## Verdict
NOT_DETERMINISTIC (on the supplementary asks only; the main recommendation is forced and reproduces). Governing label: underspecified_objective, with a Gate B/E element (the eleven candidates are never named).
**Disposition:** SEND_BACK (light), as the thread wrote it.
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call (Routes 2, 4, 6, 17, 22; Route 11 first left out) rests on the sampling design stated in service_quality_trip_matching_review_2026.pdf (one no-trip event per bus-day, 250 bus-days a month). Weighting each reviewed event by its bus-day's no-trip count and listed/drawn gives Route 17 a lowest hour of 4.81. The unweighted mix gives 3.56 and drops Route 17. A month-stratified bootstrap gives Route 17 a mean of 4.80, SD 0.13. The weighting is forced and the margin is clean.
The asks are not all literal-forced:
- The 386 repeated Quinnell rows are not mentioned in the export notes. The golden drops them.
- The prompt says "eleven candidate routes", but the files hold 14 routes and none names the eleven (Routes 3, 12 and 60 are excluded in the golden).
- Ask 4 forks: Arbor's rounded adherence_min moves 14, 40, 51 and 22 by a point; strict against inclusive bounds moves 2, 9, 40 and 11; Quinnell's DeviationSec disagrees with departure minus scheduled time and the guidance wording "as the AVL system records it" invites it.
- Ask 5: Route 11's wait is 5.2 with the frequency end_time exclusive, 5.0 inclusive or read as headway/2.
- Quinnell ask: raw rows or calendar months give other counts.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counting days | 125 | 125 | yes |
| Departures in counting hours / no trip | 106,687 / 17,112 | same | yes |
| Route 17 share of Transit Mall no-trip departures | 57% (unweighted 35%) | 57% / 35% | yes |
| Lowest hourly averages | 2: 4.7, 4: 4.9, 6: 4.7, 9: 3.7, 11: 5.7, 14: 3.1, 17: 4.8, 22: 4.8, 31: 3.5, 40: 4.8, 51: 2.9 | 4.73, 4.91, 4.67, 3.70, 5.65, 3.11, 4.81, 4.83, 3.48, 4.84, 2.94 | yes |
| Ranking by weekday boardings | 2, 4, 6, 17, 22, then 11 | 6850, 6120, 4980, 4450, 3710, 3240, 2410 | yes |
| Ask 4 on-time shares | 59, 68, 47, 78, 76, 79, 32, 73, 80, 78, 78 | same from timestamps | yes (fork-sensitive, see below) |
| Ask 5 waits | 6.1, 5.8, 6.2, 6.1, 5.2, 6.8, 7.1, 5.8, 7.9, 6.8, 7.7 | same except Route 11 (5.0 under inclusive end) | all but Route 11 |
| Quinnell record counts | golden table | match with 386 repeats dropped, 3 a.m. service-day cut | only under the unstated dedup |

## Competing answers that survived
- Quinnell repeats: dropped (golden) against kept (raw counts 8388, 8362, 8503 for 1040; 4194 for 1093 April). Closing rule: none shipped.
- Candidate set: the golden's eleven against any eleven of 14 routes. Closing rule: none shipped (only a grey route_color hint).
- Ask 4 source: timestamps (golden) against adherence_min or DeviationSec, and inclusive against strict bounds. Closing rule: none shipped.
- Route 11 wait: end-exclusive 5.2 against end-inclusive or headway/2 at 5.0. Closing rule: none shipped.
- Main call: no surviving fork. Renormalising over in-service buses, weekday-only, month-stratified and 3-hour-stratified mixes keep the call. Hour-stratified mixes (cells of about 30 events) drop Routes 2 and 17; noted as an unreasonable choice.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, pdf, xlsx, zip (GTFS txt) | yes |
| Large file | 25,000 rows or more | Quinnell 83,843 rows; Arbor 81,314 | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | title_vi_service_monitoring_2025.pdf, farebox_revenue_by_route_2026h1.xlsx; no file name labels them | yes |
| Distractors unused yet weighable | yes | no departure counts in either; the thread judged them relevant to weigh | yes, as read from the thread and metadata (I did not open the PDFs or xlsx) |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | per-route and per-stop-month grids; the prompt gives per cent and minutes to one decimal | yes |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | shape 01 (ranked list under a cap); design note plans 26 criteria, generated rubric not seen | yes on the design note's plan, rubric to be re-run at ship |
| Not LLM-reading; goldens real | yes | thread found nothing exclusion-level; two minor filler notes | yes, not independently checked |
| Candidate set determinate | implied by Gate B/E | eleven candidates never named | NO |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H line: domain pass, layers pass, decisive_step analytical.
Against the design note and metadata.json (read after the thread returned): the stump sentence names the raw (unweighted) review mix as the default path, with Route 17 at 35 per cent and a lowest hour of 3.6, against the 57 per cent its bus-days carry. The note's Three rules block names the same decisive step and Layer 1 inventory. The declared distractors (farebox, Title VI) are not named by the thread as carrying the task. No mismatch. The note's expected unweighted call (Routes 2, 4, 6, 22, 11) matches the thread's.
Note: the note's fork table does not appear to close the unnamed candidate set, the Quinnell repeats, the adherence source or the frequency end boundary for the asks. The main call is clean.

## Stump power (Gate F)
Good. The raw review log looks like a census, the memo states the one-event-per-bus-day design without announcing a weight, and the weighted margin is wide (about six SD).

## Findings, ranked
1. Eleven candidate routes never named in any shipped file (14 routes in the files). Gate B/E.
2. Quinnell repeated head-of-file rows are undocumented; the Quinnell ask counts and the main counts depend on dropping them.
3. Ask 4: DeviationSec and adherence_min against timestamps, plus boundary inclusivity, move whole per cents.
4. Route 11 wait depends on an unstated end_time convention (5.2 against 5.0).
5. Minor: the memo says "the month before" while the log's review_month equals the service month; the "Every bus carries CCTV" filler line.

## Next action for the author
Run /fix-determinism task468 with the thread's four fixes, filing WHAT not HOW: name the eleven candidates (or the selecting rule), state that rows repeated at the head of a daily file are one event, pin ask 4 to timestamps against scheduled departure with inclusive bounds, and pin the frequency end_time as exclusive. Keep the main call, memo, review log and AVL data byte-identical; the rebuild changes solver-visible text, so the one allowed re-judge applies.
