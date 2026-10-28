# determinism-check report, task270, 2026-10-28

Run record: one pass, run 1793194046 (verdict at /tmp/determinism-check-task270-1793194046/verdict.md). An earlier run folder, 1793190528, was stopped by a user interrupt at 12:36:32 UTC before the thread wrote anything; it is not a second pass.

## Verdict
NOT_DETERMINISTIC on ask 3 (and exposed on ask 1 and ask 2 by silent conventions); the main call's golden reproduces exactly. No SOLUTION_WRONG.
**Disposition:** SEND_BACK
**Stumping type:** mechanism: etl_conformance (cover replay executing a stated standard), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
1. Main call: OFRS-RS-03 files the estimand and the procedure end to end. Executed literally, with free engines placed where the log's location rows put them, it gives Wrenfold 73 and Pelmarsh 73 named. The standard says only that a drive runs "between the network nodes nearest its start and its end" and never says where a free engine away from base starts. Placing every free engine at its station (status still honoured) gives Wrenfold 77.6 and Pelmarsh 77.4 not named, and Altmoor 72.7 and Skirwold 73.2 named. That is a different named set, and only the data rules it out, not a clause.
2. Ask 3: the same-actuation rule (a call before the close of an earlier record at the same premises is one actuation) is in no shipped file. Counting records gives different figures for every district.
3. Ask 2 needs three conventions no file states: bookings are UK local time against a UTC log, a later-entered booking replaces the same firefighter's overlapping booking, and the register role is the year-end role. Each is forced only by reconciling against the log (0 contradictions with all three).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cover Calderstow / Tollesham / Wrenfold / Hollinbury / Pelmarsh / Altmoor / Skirwold | 84/78/73/80/73/77/77 | 83.98/77.74/73.23/79.87/73.24/76.92/76.76 | yes (live-location reading) |
| Named set | Wrenfold, Pelmarsh | same under live location; Altmoor, Skirwold under station placement | yes, but forks |
| Ask 2, 8 stations x 2 figures | 211h18/182h30, 764h55/632h5, 512h30/459h45, 588h47/280h30, 207h55/131h15, 809h8/353h44, 219h1/166h30, 401h7/362h0 | identical, second-resolution replay identical | yes, with the three unfiled conventions |
| Ask 3 counts and rates | 2632/62.1, 874/66.9, 762/63.2, 769/59.2, 714/59.0, 371/63.4, 375/62.9 | identical with the dedup rule; 2758/65.1, 903/69.1, 792/65.7, 809/62.3, 743/61.4, 392/67.0, 385/64.6 without | yes only with the unfiled rule |
| Denominators (C addresses) | per 100 premises | 4237, 1306, 1206, 1299, 1210, 585, 596 (match cabinet report Appendix A) | yes |
| Plot | ask 1 values | nothing further to recompute | n/a |

No figure failed to reproduce. The misses are forks, not arithmetic.

## Competing answers that survived
- Ask 1 and the call: live location (Wrenfold, Pelmarsh) against station placement (Altmoor, Skirwold) against static always-free (none named). Shipped rule meant to close it: standard section 4 "nodes nearest its start". It does not state where the start is.
- Ask 3: one record is one actuation against the dedup rule. No shipped sentence closes it.
- Ask 2: naive same-clock, union of bookings, or register role as always-commander give different hours (for example Thornstead 329h20m, 301h20m, and 113h0m for the no-commander figure). Off-the-run reasons: all reasons counted, which the prompt supports.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | log 320,050 rows, bookings 99,770, addresses 160,268 | yes |
| Distractors | 2 or more in metadata.json, none named by file | population_estimates_mid2025.xlsx, station_establishment_2026.xlsx; names carry no label | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | thread found both present and weighable; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both present | yes |
| Asks | multi-dimensional, unit and rounding stated | 7 + 16 + 14 figures plus the chart; unit and rounding in the prompt | yes |
| Prompt shape, rubric 25 or more | identifiable, 25 or more criteria | scorecard against a threshold, about 37 gradable figures | yes (count inferred, not generated) |
| Not LLM-reading, goldens real | nothing LLM-like | thread saw no authoring disclosure; golden realism not re-read here | yes (thread-level) |

## Gate G reconciliation
Thread: stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card holds no mechanism or stumping_family field (None). Design note: nothing planted, no decoy, no artifact ranks the districts. Gate G is analytical, with no planted defect. The declared distractors were not named as the surface read carrying the task.

## Gate H reconciliation
Thread line: domain pass, layers pass, decisive_step rule_application. Card and note: stump_class analytical, decisive step "placing each free engine where the log's location rows show it", with a note argument that no clause rules the station replay out. This is a mismatch, and the finding most likely to predict a send-back. The note itself concedes that "no clause rules the station replays out; only the data does". The thread reads the standard as an executable procedure whose one silent position convention is a semantics gap. The note's own SF7 and SF11 rows close the start of a drive with "same call" on section 4, which the standard's text does not support for where an engine stands. Layer-2 content (time-averaged dynamic cover) is real, but the decisive step is not defensible as analytical from the shipped text.

## Stump power (Gate F)
The easy routes (static always-free: none named; station-based: Altmoor and Skirwold) both miss the golden, so a solver skipping the live-position replay plausibly fails. The thread's point is that the failure comes from a silent convention, not a method choice. The main thread should weigh that against the note's ladder. A real reviewer who treats the standard as a literal procedure will see the live-location reading as the only text-consistent one, but the station placement is a defensible competing reading, so the stump is not safe from a determinism block.

## Findings, ranked
1. Gate H decisive step reads rule_application and the engine-start convention is silent, so the named set flips between two defensible readings. Fix: file the WHAT (the position a free engine's reach is measured from, as population/definition) without filing the method, or reroot the decisive step.
2. Ask 3 same-actuation rule is in no shipped file, so counts differ by 3 to 5 per cent per district. Fix: state the unit counted in the prompt or the cabinet report.
3. Ask 2 three conventions unfiled: booking clock (the bookings file carries no time-zone label while the log column is named time_utc), replacement of overlapping bookings, and role by effective date. Fix: label the booking clock and the role-on-the-day basis in a shipped document.
4. Design note's fork table closes SF7 and SF11 with "same call" on standard section 4, which does not state it. Correct the closure or file the convention.

## Next action for the author
Run /fix-determinism task270: file in the standard and the cabinet report where a free engine's reach is measured from, the unit for a repeat call at the same premises, the booking clock and role-on-the-day, and rework the decisive step so it rests on an analytical choice rather than on execution of the stated standard.
