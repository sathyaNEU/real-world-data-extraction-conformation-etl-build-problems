# determinism-check report, task168, 2026-11-01 (pass 2, the single re-judge licensed by /fix-determinism)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (the isolated thread's call; two non-blocking findings below, one worth the author's attention)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread run: one general-purpose Agent, sonnet, medium, spawned by the main session from my judge_brief.md (this runtime had no Agent tool). Scratch /tmp/determinism-check-task168-r2/ (fresh unzip of target.zip, 12 files). Derive-before-reading order: kept. derivation.md written 17:03, answers.md (the graded blocks, a separate file) opened afterwards, verdict.md 17:04, and the verdict states it derived first; its derivation records figures that match the blocks only after the fact. I could not independently audit the thread's file access, only its timestamps and self-report. Report file is pass2 because determinism_check_report.md is an earlier pass and is not overwritten.

## Why
All 18 turned-away figures (total 50,632) and 175,000 reproduce from the files alone. The portal's claim (attribution of a refusal to route and direction) was tested: the literal reading attributes by flight_no and dep_date to the operated leg, filtered to requests at or after the departure's sold_out_utc, deduplicated by (session_ref, flight_no, dep_date) at its constant pax. The competing reading (journey_orig and journey_dest, 47,484) drops 9,040 network-wide connecting GDS itineraries and is ruled out by the prompt's "from summer 2025 departures", the log's header writing the departure as flight_no and dep_date, and the airports being named journey_*. The fork exists as a reading but is not defensible against the text. Main figure forced by the planning basis and the 85 per cent censoring at 144.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| S25 carried, nine routes | 1,044,148 | 1,044,148 (dcs pax_flown; matches close-out PDF rows) | yes |
| Sold-out departures | 6,418 of 7,560 | same (sold_out_utc non-null iff pax_booked = seats) | yes |
| 18 turned-away counts | e.g. LIN-CTA 4,760 ... TPS-LIN 1,716 | all 18 exact, total 50,632 | yes |
| Additional passengers | 175,000 | 165.6k to 168.4k carried increment by curve granularity, 173.6k with no show-rate; all round to 175,000 | yes (rounding) |

## Competing answers that survived
None on the main figure. On the turned-away ask the thread lists forks, each ruled out by shipped text:
- No sold-out-time filter (departures that ended full) 60,404; every NO_AVAIL row 61,782 (LIN-CTA 5,578 / 5,674). Ruled out by "because the flight was full" plus sold_out_utc. NO_AVAIL is never defined in words in any file.
- Journey airports as the route: 47,484 (the portal's fork).
- No dedup: 72,993.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / big file | 10+ / 3+ / 25,000 rows | 12 / 4 (csv, xlsx, pdf, sqlite) / 142,969-row refusals csv, 740,885-row sqlite | pass |
| Distractors | 2+ named, none labelled by file name | metadata names fare_report_IS25.xlsx and competitor_seats_IS25_IS26.csv; names are neutral | pass |
| Distractors unused, relevant, ruled out by a shipped fact | yes | thread lists them (plus ym3 IS24 archive, fleet register) and found none answering a graded quantity; not independently reproduced by me | pass (thread) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | pass |
| Asks multi-dimensional, unit and rounding stated | yes | 18 route-direction counts, whole numbers; 25,000 rounding stated | pass |
| Prompt shape, 25+ criteria | yes | 1 + 18 + 1 chart requirements plus components is plausibly 25+; the rubric is generated and not in the bundle, not verified | not verified |
| Prompt rules (CLAUDE.md) | one paragraph, under 1,000 chars, no count the data hold | 706 chars, one paragraph; but states "nine" routes and "about 620,000 seats", both derivable (620,224 in the capacity plan) | flag (low) |
| Reads as real work product | yes | 12 constructed files, business-realistic mess; goldens present, realism not judged here | pass (thread hygiene PASS) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: a forecasting task whose decisive step is completing each sold-out departure's censored demand from the booking build of its own month (projection detruncation), the easy route filing 500,000 (the 0.80 passengers per extra seat). Thread's easy routes: seats times load factor (600k+), 0.80 per extra seat (about 500k), booked plus recorded turnaways (about 50k), pooled curve (230k to 270k). Match. The declared distractors (fare report, competitor seats) were not named as the surface read carrying the task. Gate G passes.
**Gate H:** domain: pass, layers: pass, decisive_step: analytical. Matches the design note's `## Three rules` (domain pass, layers pass, analytical). Layer 1: flight renumbering, lap infants, UTC against local, connecting itineraries, the capacity plan versions; Layer 2: revenue-management unconstraining of censored departures.

## Stump power (Gate F)
Strong on paper: easy routes give 500k, 600k+, about 50k or 230k to 270k against 175,000. Caveat for the main thread to weigh against the ladder: the thread classes the c / F(t sold-out) estimator as one that validates itself (back-test on uncapped 150 to 220 flights censored at 144 gives ratio 1.003 to 1.005), so a strong analyst who builds the curve by departure date and validates it lands the call; this is a landable call, textbook for the field (stumping 1.3), and the wrong answers come from pooled or coarse curves and the 0.80 shortcut. The thread also finds a plausible miss on the turned-away ask (no filter, or journey match).

## Findings, ranked
1. **The SF11 closure the design note records is no longer in the bundle.** DESIGN_NOTE line 297 and the earlier determinism report's pass-1 rest the attribution closure on a sentence in data_dictionary_rev5.pdf ("orig, dest: ... journey requested"). The current target.zip has 12 files and no dictionary (design note lines 252 and 260 say it was retired as a leak); the refusals header now reads journey_orig and journey_dest beside flight_no and dep_date. The thread, not seeing any dictionary, still found the flight_no / dep_date reading forced, so the verdict stands, but the closure is now only the header names and the prompt's "from summer 2025 departures". The portal's two responses both filed 47,484 on the earlier wording, so this fork has already caught real readers; it is the highest residual risk. The design note's line 297 and the pipeline.json "move" text are stale against the bundle and should be corrected. Under my contract this is a diagnosis; no fix made.
2. **Thin-but-clean margin on the main figure.** Thread's unrounded increments (165.6k to 168.4k) sit 3k to 6k above the 162.5k rounding boundary, narrower than the design note's 167.9k to 184.8k family; a valid estimator biased about 2 per cent low would file 150,000. Thin, not contested.
3. **Prompt states derivable counts** ("nine" routes, "about 620,000 seats"), against the no-count-the-data-hold rule. Low; style/spec, not a determinism fork.
4. Rubric criteria count (25+) and golden realism not verifiable from the bundle by this pass.
5. Optional (thread): say in the write-up that the sold_out_utc filter is what "because the flight was full" means and that route and direction come from the flight leg (step 8 already does).

## Next action for the author
Reconcile DESIGN_NOTE.md line 297 and pipeline.json's returned[].move with the shipped bundle (no dictionary; closure is the journey_orig / journey_dest header names), then decide whether the thin closure on SF11 is acceptable for reshipping or needs a filed sentence that does not return the dictionary file.
