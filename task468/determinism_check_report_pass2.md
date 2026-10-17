# determinism-check report, task468, 2026-10-17 (pass 2)

Scratch: /tmp/determinism-check-task468-195537-p2/ (fresh unzip of target.zip; verdict at /tmp/determinism-check-task468-195537-p2/verdict.md). One judge thread, one pass, no retry.

## Verdict
DETERMINISTIC (as the thread wrote it; main call and asks 1 to 3 forced, ask 4 carries one residual fork, no SOLUTION_WRONG).
**Disposition:** FIX_NOW (as the thread wrote it): one pin in ask 4 so the schedule is the timetable feed's scheduled departure at the designated stop, not the AVL export's own schedule field. The main-call surface is untouched.
**Stumping type:** mechanism: statistical_rigor (etl_conformance beneath), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The guidance (3.2 to 3.4, 5.1) fixes the 125 counting days, the thirteen hours, departures counted whether or not tied to a route, and the top five by weekday boardings. The review memo's sampling design (250 bus-days a month, one event per bus-day) forces design weights; with them Route 17 qualifies and the five are 2, 4, 6, 17 and 22 with Route 11 first left out. Only the unweighted mix or the matched-proportional share-out give another five. Pass 1's failure (the asks) is closed except for one fork in ask 4, below.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counting days | 125 | 125 (calendar, guidance 3.4) | yes |
| Departures, hours 6 to 18 | 106,687 | 106,687 | yes |
| Departures with no trip | 17,112 | 17,112 | yes |
| Repeated Quinnell rows dropped | not claimed | 386; bus-days listed per month match the memo tally exactly | yes (confirms dedup and service-day rule) |
| Route 17 share of Transit Mall no-trip, weighted | 57% | 57.4% | yes |
| Same, unweighted | 35% | 34.6% | yes |
| Route 17 lowest hourly average | 4.8 | 4.81 (hour 6) | yes |
| Other lowest hours | verdicts of ask 1 | 2: 4.73, 4: 4.91, 6: 4.67, 11: 5.65, 22: 4.83, 40: 4.84; 9: 3.70, 14: 3.11, 31: 3.48, 51: 2.94 | yes |
| Boardings rank | 2, 4, 6, 17, 22; 11 next | 6,850 / 6,120 / 4,980 / 4,450 / 3,710 / 3,240 | yes |
| Ask 4 on-time shares (feed schedule, bounds inclusive) | 62 70 54 71 73 72 37 72 72 75 73 | 61.8 69.8 53.8 71.0 73.2 71.7 37.1 71.7 72.3 74.7 73.0 | yes, all 11 |

Robustness: a stratified bootstrap of the review keeps all seven qualifiers at 4.0 or more in every draw (Route 17 low end 4.56). Out-of-service redistributed across routes, no month factor, weights from counting-hour counts and review events restricted to counting hours all leave the five unchanged.

## Competing answers that survived
- Main call and asks 1 to 3: none. Unweighted review mix (Route 17 35%, minimum 3.56) gives 2, 4, 6, 22, 11; matched-proportional share gives 2, 4, 9, 22, 11; matched departures only contradicts guidance 3.4. Each is ruled out by the memo's own sampling design or a stated rule.
- Ask 4 (survives): scoring Q1 departures against Arbor's minute-truncated `sched_dep` instead of the feed's scheduled departure gives 2: 60, 4: 69, 6: 51, 9: 74, 11: 74, 14: 75, 17: 35, 22: 73, 31: 77, 40: 76, 51: 76. Guidance 4.2 and the prompt say only "the trip's scheduled departure"; the cutover notes call Arbor's field "Arbor's schedule time" while Quinnell's is defined as the feed's. The feed reading is the careful one (Quinnell's DeviationSec equals the feed deviation exactly), but the text does not close it. The bounds are inclusive by "no more than" (exclusive bounds would move Route 6 from 54 to 53).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 in the unzip (metadata.json records 13; nominations_folder_list.csv appears uncounted there) | yes |
| Formats | 3 or more | csv, pdf, xlsx, zip (GTFS txt) | yes |
| Large file | 25,000 rows or more | Quinnell 83,843 rows; Arbor 81,314 | yes |
| Distractors | 2 or more named, none labelled by file name | metadata.json names title_vi_service_monitoring_2025.pdf and farebox_revenue_by_route_2026h1.xlsx; file names are neutral | yes |
| Distractor relevance | unused, weighable, ruled out by a fact | not used by the solution; the thread found no shipped artifact answering a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 1 (xlsx), present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | verdicts for 11 routes, the five, first left out, 11 on-time shares "to the nearest whole per cent" | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 01 (ranked list under a cap). The 25-criteria count is generated at ship and was not independently counted here | shape yes; count not verified |
| Reads as real | no LLM tells, goldens realistic | thread found no authoring disclosures; system-export mess present | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_strategy identity_resolution, stump_class analytical. Same family (FINE-numbers estimation method, review weighted by its own design). The label differs (statistical_rigor against method_or_model_selection) but both sit in the passing family. The thread names the raw review mix (Route 17 at 35%, lowest hour 3.56) as the easy route; that is the review's honest log, not the declared distractors, so no distractor is load-bearing. The analyst_test (raw mix files 2, 4, 6, 22, 11; proportional files 2, 4, 9, 22, 11) matches the thread's competing answers exactly. Match.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Layer 1 is two AVL vendors with different keys, UTC against local, repeated file heads, renumbered stop ids and frequency-based trips. Layer 2 is design-weighting a one-event-per-bus-day audit. This agrees with the card's domain_test and the design note's `## Three rules` (No decoy, Not semantics, Not rule application).

## Stump power (Gate F)
Good, per the thread. The raw-mix share-out is the natural wrong route and needs the memo's sampling design turned into weights. Ask 4 adds a second layer (frequency expansion for Route 11, feed by date, UTC to local, the feed's seconds against Arbor's rounded schedule) over eleven separate figures. Design-note ceilings (cracker 45.0, mirror 27.9, pair 36.5) are the author's paper numbers, not measured here.

## Findings, ranked
1. Ask 4, Q1 schedule source: Arbor's `sched_dep` against the feed's scheduled departure moves all 11 shares, by 1 to 5 points. The design note's fork row SF15 closes it as "same call" using the guidance text and the Quinnell change note, but the shipped guidance does not say the feed governs, and the real reviewer reads only the shipped text. The fork is real and the design deliberately uses it as the ask-level device. This is the only open finding.
2. metadata.json says 13 files while the bundle holds 14 (hygiene bookkeeping only).
3. Inclusive-bounds sensitivity (Route 6 at 54 or 53) is closed by "no more than" and is not a finding.

## Next action for the author
Pin the source in ask 4 by one phrase in prompt.txt (669 characters now, under the 1,000 limit), for example "against the trip's scheduled departure from the designated stop in the timetable feed in effect that day". That files the WHAT (the source), not the HOW. Then rebuild, update the goldens and re-run checks. The main-call surface stays byte-identical. Reconcile the file count in metadata.json.
