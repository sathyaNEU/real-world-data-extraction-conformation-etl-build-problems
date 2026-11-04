# determinism-check report, task398, 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution (counterfactual source attribution through the lake's thermal structure; closest to other), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread verdict: /tmp/determinism-check-task398-796801/verdict.md (one pass, one thread, bundle unzipped fresh at /tmp/determinism-check-task398-796801/target/, target.zip sha256 8fd1530d...937c). Disposition is APPROVE with the open items below carried as findings, none of which changes the main call.

## Why
The thread recomputed the 47 days above 3.0 ug/L (GC/MS confirmation where run, else ELISA, per SOP-WQ-07 2.3), the intake depth (10.45 to 10.95 m) and each tributary's entry depth against the buoy profile. Fennick Creek sits within 0.19 m of the intake depth on every one of the 47 days (0.44 m with no look-back). Every other sub-watershed is at least 4.85 m away. A grid of tolerance 1 to 4 m by look-back 1 to 60 days gives Fennick 47 and the others 0 in all 20 cells. The ELISA-only reading (52 days) is closed by the filed SOP rule. All 16 monthly atrazine cells and all 4 carbon months reproduced to the whole unit.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Days above 3.0 ug/L, 15 Apr to 31 Oct | 47 | 47 (raw_water_log + LIMS, SOP 2.3) | yes |
| Stratified at dam | 27 Apr to 6 Oct | consistent with buoy profile | yes |
| Intake depth | 10.4 to 11.0 m | 10.45 to 10.95 m (829.24 NAVD88 less 0.24 ft) | yes |
| Days caused: Fennick / Dunmore / Ladd / Oxley / Tessel | 47 / 0 / 0 / 0 / 0 | 47 / 0 / 0 / 0 / 0 | yes |
| Tessel kg Apr to Jul | 7, 155, 179, 32 | same | yes |
| Fennick kg Apr to Jul | 3, 35, 41, 9 | same | yes |
| Oxley kg Apr to Jul | 6, 107, 106, 17 | same | yes |
| Dunmore kg Apr to Jul | 4, 64, 71, 14 | same | yes |
| Ladd Branch | not sampled | no samples in files | yes |
| PAC lb May to Aug | 3,243 / 25,024 / 23,776 / 3,693 | same | yes |
| Chart: 47 days marked | 47 | follows from the count | yes |

## Competing answers that survived
None on the main call. Forks the thread raised or I found on the asks (each closes to the golden under the literal text, none was shown to change the call):
- Carbon: CST day boundary instead of local gives 3,246 / 25,019 / 23,776 / 3,695; the thread took local because the operating report is plant-local. Ignoring stops gives 3,460 / 25,565 / 24,311 / 3,858.
- Autosampler clock read as UTC would move Tessel May by about 10 kg and Oxley May by about 7 kg; the thread closed it with the program-enable times coinciding with hydrograph rise onsets.
- Carbon outage end (see item 3 below): not tested by the thread.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 26 (the thread counted 27; my count of `find -type f` is 26) | yes |
| Formats | 3 or more | 5 (14 csv, 7 xlsx, 3 pdf, 1 dat, 1 txt) | yes |
| Large file | 25,000 rows or more | five station exports at about 29,180 rows; the SCADA alarm history 59,148 | yes |
| Distractors named in metadata.json | 2 or more, none labelled by file name | `distractor_files`: tributary_nitrate_2026.csv, merrin_beach_ecoli_2026.csv; neither name labels a distractor | yes |
| Distractors relevant, unused, ruled out by a shipped fact | each | nitrate is tributary-by-tributary and weighable; the beach E. coli file is a weak candidate (a swimming beach, not a source ranking). Neither answers a graded quantity | yes, E. coli thin |
| Deliverables | 1 to 3, all in golden | 3: docx, xlsx, png; all in the submission's Deliverable Answers | yes |
| Asks multi-dimensional, unit and rounding stated | each | counts per sub-watershed; 16 station-month cells; 4 carbon months; kilograms and pounds to the whole unit stated in the prompt | yes |
| Prompt shape and 25 criteria | identifiable, 25 or more | shape 12 (root-cause named); the design note's ask sheet lists 22 ask and chart criteria plus recommendation and components, so 25 or more is plausible; I did not see the generated rubric | not verified |
| Reads as real, not LLM generated | | the thread found no authoring disclosures, hidden sheets or benchmark language; plausible tool metadata | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: `gate_g` and `stump_strategy` decomposition_attribution, `stump_class` analytical, `layer2_family` field_method. They match.
- The thread's easy route (load share or acreage ranking, naming Tessel) is the card's `analyst_test` route (30-day load share, Tessel 39 of 47). The surface read is not either declared distractor.
- Finding: the thread named the Haldane extension survey as a distractor (it ranks Tessel by acreage). metadata.json does not declare it; only nitrate and beach E. coli are declared. The survey ranks the sub-watersheds on a basis (atrazine applied) that points to the wrong answer, and Gate G's exception covers only a declared wrong-basis distractor. The design note accepts it ("the extension survey ranks the Tessel River first by application") and lists it under Oracles. It does not rank the days, which is the decision quantity, so I record it as low-risk, but it is not declared and should be, or the survey's non-ranking of days should be argued in the note.

**Gate G line:** passes; match to the card; the only wrinkle is the undeclared Haldane survey that ranks Tessel by application.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Card: `stump_class: analytical`, `analyst_test` and `domain_test` filled; design note `## Three rules` has Domain test, Swap, Layer 1, Layer 2, Decisive step, Not semantics, Not rule application, No decoy. They match, including the swap test and the claim that no filed rule places an inflow in the lake.

**Gate H line:** domain pass; layers pass; decisive_step analytical, as the card declares.

The thread does not class the decisive step analytical because it is "the field's standard method" with no judgment to settle. Placing each tributary at the depth where the lake matches its temperature is a computation across files with no filed rule, and the data separate the candidates.

## Stump power (Gate F)
Good by the thread. The quick route (load or acreage) names Tessel; the buoy-depth bookkeeping, the datum conversion and the tributary temperature clocks are all needed to reach Fennick; the margin is wide once reached. The design note's ladder puts Fennick last at rungs 0 and 1.

**Ask exposure (per the coordinator's second point).** The thread reproduced every ask figure, including the storm-bottle matching to the autosampler run logs (bottle count equals OK positions at each station, so the NO LIQUID positions hold no bottle) and the feeder outages from the SCADA alarm history. The builder's ceiling read is that a careful solver's route keeps 0 of 20 ask figures and the full reconstruction keeps 19 of 20, a pair near 81 if both top responses do both and land the call. The shipped text invites both reconstructions in two places:
- The prompt asks for atrazine "interpolating its samples linearly in time against the 15-minute flows". The autosampler log's own header is `Sample time`, beside `Carousel removed`, while the bottle log carries `Time logged`. A solver who takes "its samples ... in time" literally reaches for the column named `Sample time`.
- The prompt asks for "the powdered carbon the plant fed", not the carbon the setpoints called for. The feeder's `RUN STATUS OFF` and `RUN STATUS ON` events sit in the alarm history beside the `MOTOR OVERLOAD TRIP` and `HOPPER LEVEL LOW-LOW NO FEED` alarms. "Fed" invites checking whether the feeder ran, though the prompt does not say where.
So the shipped text does not hide either reconstruction, and a thorough solver reaches both. The 19-of-20 route is open to a strong solver on the asks, and what holds the pair down is whether the top two land the main call. The main-call ladder (Tessel at 39 days on the load-share route) must do the work; I leave that weighing to the main thread against the design note's ladder.

## Findings, ranked
1. **Carbon outage end is an untested fork on the asks.** The design note's ask sheet says a trip until its return-to-normal (`RTN`) moves three of the four months against the golden's trip-until-next-`RUN STATUS ON`. The SCADA history shows `RTN` at 12:29 on 30 May after a `RUN STATUS OFF` at 12:10; the golden ends the outage at the next `RUN STATUS ON`. The filed text (SOP 3.2, the prompt) never says how an outage ends. The golden reading is the physically sensible one and the events state it, but verdict.md recorded only "stops" and "no-feed intervals" and ran no alternative.
2. **DC-04 logger time zone is not stated in the file.** The DC-04 header shows `Date,Time,ms,LEVEL,TEMPERATURE` with no zone, and the golden says UTC. The thread did not examine it. The effect is limited to Dunmore Creek's monthly cells and its placement temperature, and the rating's `Effective from ... CDT` stamp is the closest evidence. The thread's recomputed Dunmore cells match.
3. **Haldane survey undeclared** (Gate G section above).
4. **File count**: the thread reported 27, I count 26; formats and thresholds unaffected.
5. **Rubric criteria count** unverified from the files.

## Next action for the author
Treat the main call as clear. Before reshipping, settle the carbon outage end: either add a sentence or record in the shipped files that closes it (the `RUN STATUS` events are the feeder's state) or argue in the design note why the filed text fixes `RUN STATUS ON` over `RTN`; and declare or argue away the Haldane survey in metadata.json.

## Builder-flagged points against verdict.md (coordinator's item 3)
| Point | Addressed in verdict.md | What the thread found |
|---|---|---|
| Literal reading of the sample time reaching the storm bottles' fill times | Partly | Storm times taken from the autosampler; bottle count equals OK positions per station; autosampler clock local (enable times coincide with rise onsets); UTC reading would move Tessel May about 10 kg and Oxley May about 7 kg. The logged-time (`Time logged`) alternative was not run. |
| DC-04 logger offset step on 3 July | Yes | Golden reproduced (4, 64, 71, 14); ignoring the step gives July 17; rating 1 only gives June 75 and July 15. |
| DC-04 logger time zone, not stated in the file | No | Untouched (finding 2). |
| Plan 5.1 counterfactual's literal reading | Indirectly | The thread tested placement and layer exposure over tolerance and look-back, invariant at 20 of 20 cells. It did not execute the literal removal of a sub-watershed's atrazine against the 0.21 ug/L residue (SF10) or the mass-balance reading. |
| Carbon outage end at next RUN STATUS ON | No | Only says feeder stops and no-feed intervals were applied (finding 1). |
| Lagged correlation of raw water on each tributary's samples, Fennick by 0.004 | No | Untouched. The design note puts Fennick at r 0.705 against Tessel 0.701 and calls it no separation. Because it tops Fennick it points to the golden's answer, so it is no fork on the call, but the thread did not test it. |

## Coordinator's item 1: would pinning plan 5.1's attribution method file the HOW?
Yes. The thread's optional fix says the written plan could pin the attribution criterion. Plan 5.1 already files the WHAT: a day counts for a sub-watershed when the raw water would have stayed at or below the trigger that day without that sub-watershed's atrazine. The remaining open item is how to know what the intake drew without that atrazine. Pinning it (the 2 m layer, the 30-day look-back, matching by temperature to the buoy profile) would file the method that carries the decisive step, so the call would become rule application, which CLAUDE.md bans as the decisive step ("File the WHAT ..., never the HOW"). The thread itself found the result invariant over tolerance 1 to 4 m and look-back 1 to 60 days, so no pin is needed. Its closing line, "file ... the layer-exposure criterion", is the same trap, and I advise against taking it.
