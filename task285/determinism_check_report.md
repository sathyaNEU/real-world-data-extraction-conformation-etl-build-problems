# determinism-check report, task285, 2026-11-04

## Verdict
NOT_DETERMINISTIC (taxonomy underspecified_objective), confined to supplementary asks 3 and 4. The main call, ask 1 and ask 2 are forced and reproduce. The thread did not return SOLUTION_WRONG.
**Disposition:** SEND_BACK (the thread's own disposition; the repair is ask-layer only, see Next action, and spends no architecture).
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Order check: the thread reports it wrote derivation.md before opening graded_blocks.md. Its derivation matched the submission on the main call, the grants, ask 2 and nine of eleven ask-4 rows, and differed only on ask 4 (Hollinside, Upper Quarnell) and the unit and shape of ask 3. Thread files: /tmp/determinism-check-task285-154953/verdict.md and derivation.md.

## Why
The main call reproduces. Hour by hour through QRN25 D100CC, the network (14 closed 2025 links, all with a point 1.04 to 1.29 m deep, every other link at most 0.12 m) cuts off Hollinside (hours 12 to 19), Ravelsby Bridge (15 to 22), Lunnerby (16 to 24), Burnishaw (39 to 46), Wrennick and Cottergill (45 to 55). That is 2,093 households, and the grants reproduce exactly (4,788.82 / 4,416.15 / 5,786.43 / 6,399.90 / 4,611.08 / 3,997.61, summing to 30,000; closest to a rounding line is Lunnerby at 0.07). The depth test is inert to threshold 0.20 to 0.30, strict against inclusive, CL1/CR1 only and QRN23 against QRN25 (only the any-point v mean rule moves it, and the guidance's "where floodwater stands deeper" is per carriageway point).
Two asks fork on committed answers (Gates C/E):
- Ask 4 admits two licensed answers on who the payee is.
- Ask 3 has no stated unit, and its golden depends on four unstated conventions.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cut-off set, hour by hour | 6 parishes | same 6, hours as above | yes |
| Peak-for-whole-event alternative | 9 parishes, 3,828 hh | same 9 | yes (the trap, not the golden) |
| Households | 2,093 | 312+247+486+593+281+174 | yes |
| Grants | 4789, 4416, 5786, 6400, 4611, 3998 | as above, sum 30,000 | yes |
| Ask 2 dwellings | 1,254, per parish as listed | identical per parish | yes (SURV08 +0.42 m inferred from the 2022 survey overlap, n=477) |
| Ask 3 hours | 17,15,16,5,6,8,13,3,7 | 16.8, 15.0, 15.75, 5.0, 6.0, 8.1, 12.8, 3.15, 7.1 | only under the golden's grouping and conventions |
| Ask 4 unpaid | 420, 770, 5600, 295, 1580, 238, 620, 400, 59, 460, 132 | same, except Hollinside 1260 and Upper Quarnell 550 if village-hall money is not the parish's | 9 of 11 unambiguous |

## Competing answers that survived
Main call: one weaker alternative, the peak-for-whole-event reading (9 parishes). It is discussed under finding 1 below, not a fork on the thread's verdict.

Ask 4, the payee rule (ledger Transactions):
- Cells moved: Hollinside 420 v 1,260 (GBP 840 to "Hollinside and District Village Hall"); Upper Quarnell 132 v 550 (GBP 418 to "Upper Quarnell Village Hall Committee"); Burnishaw 238 v 950 (GBP 712 to "P. Lees, Clerk to Burnishaw PC"). The thread flagged the first two as open and Burnishaw as an alternative both of us counted; the design note's ask sheet treats all three as the payee device, so three cells move.
- Shipped rule meant to close it: none. Guidance s3 says only that the unpaid part "is paid with the 2027 grant". The ledger carries no remark that the payment was at the parish's request.
- The thread's closure: name the payee rule in the asking sentence or the ledger ("paid to the parish council" or "posted against the award").
- Would that state the device in plain words? Yes if put in the prompt: it hands over the second primary device (D7). Better closure: a data-side fact in the ledger, for example a remittance note column on those three rows ("paid at the parish council's written request"), so the prompt stays silent, the golden stays as it is, and a shipped fact rules out the parish-only reading.

Ask 3, hours closed:
- Section unit: "each road section" is undefined. The golden is keyed to nine labels HW21-07-01..09 although closure_ref is reused across roads (-04, -06, -08 each carry two roads), and the 2025 network has 14 closed sections. All nine rows depend on it.
- B5131 route closure (HW21-07-10, "Hollinside to Lunnerby, diversion signed at both ends"): the golden applies it to the three beck-crossing sections. Read literally it closes nine B5131 sections, and the five intermediate sections would show 15 h. Moves the three B5131 rows (17, 15, 16) and adds rows.
- Summed spells against first-closing to last-reopening: Nettlecote 7 v 9, Highfold 6 v 7, Yarrowcote 13 v 14 (three cells).
- Clock: highways times are "closed_local", police "closed_utc". Local is taken as BST, which no file states. Moves the police-involving rows by an hour, and the nearest-hour rounding for several.
- Police row with no opening time (C2047): resolves to the highways reopening (3 h) under either method; inert.
- The thread's closure: name the unit, say whether a route closure counts for the sections it spans, and whether "stayed closed" is hours in force or first closing to last reopening.
- Would that state the device in plain words? Naming the unit and "hours in force" are WHAT and are safe. Stating "a route closure counts for each section between its ends" would state device D6 in words; close it instead by shipping the fact (the route row's location column naming the sections it covers, or a section list in the closure log). The BST fork closes with one word ("local time, British Summer Time") in the log's header or a column name.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, geojson) | yes |
| Large file | 25,000 rows or more | address register 27,815 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 (rest_centres_2026.xlsx, flood_warning_areas_2025.geojson, storage_area_stages_QRN25_JUL21_hindcast.csv); no name labels one | yes |
| Distractors unused, relevant, ruled out | unused by solution; one that answers a graded quantity is ruled out by a shipped fact | thread used the hindcast only to confirm sections. Not independently recomputed: the hindcast stages could in principle be run against the survey levels to give July 2021 closure hours, so ask 3 should state that the duty and police logs are the source (cheap to close with the unit sentence) | yes, with that note |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each states unit and rounding | multi-dimensional; rounding stated in the closing sentence; ask 3's unit ("each road section") is undefined | NO (ask 3) |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 05; design note counts 18 + 9 + 11 ask figures plus chart parts and grants | yes |
| Reads as real | no LLM-generated look, goldens realistic | no authoring language seen; hand-keyed ledger, reused refs, mixed timezones. Prompt 766 characters, one paragraph, question first, no data-derivable count | yes |

Failed gates: asks (unit stated) for ask 3, and Gates C/E (answers contradict or are underdetermined by the files) for asks 3 and 4. All are confined to supplementary asks. The main call is forced, and Gates G and H pass.

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical, strategy time_semantics, official_decoy false, validated_decoy false. Design note: no decoy, nothing names a parish as cut off, no memo or list. Match on all four fields.
Gate G line: PASS. The thread names the model report's printed peak-stage table, not a declared distractor, as the surface read. The declared distractors (rest centres, warning areas, hindcast) carry no part of the call, so none is too load-bearing. The peak table is a correct, calibrated figure; no shipped artifact ranks the parishes wrongly.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Card: stump_class analytical, with analyst_test (peak envelope files nine, golden six) and domain_test (reachability under link failures). Design note `## Three rules`: same decisive step (the envelope is no state the network is ever in), same easy route (9 parishes, 3,828 households), same 3 labelled lines. Match.
Gate H line: domain pass, layers pass (Layer 1: crosswalk and split links, datum, UTC against local, reused refs, merged parish, hand-keyed ledger; Layer 2: concurrency of closures), decisive_step analytical.

## Stump power (Gate F)
Strong on the main call. The printed peak table and the "design flood" wording pull a strong analyst to the envelope (nine parishes, grants about 3,100 to 3,700), which is wrong on the hourly series. The design note's ladder has the cracker landing the call, the mirror off it, and a pair ceiling of 45.9, so the ask layer needs only the repair below, not a harder design. The thread suggests live testing could confirm 9 against 6 is analytical; no solver round is run, per the project's STOP rule, and stump power is argued on paper and measured by the portal. The easy-route miss is not a textbook method that the field's standard analysis lands: the field's analysis (reachability at each hour while links fail and recover) is the golden, and the peak map is the planner's shortcut.

## Findings, ranked
1. **Peak-stage reading (Gate C question on the main call).** The thread rates it weaker but notes no sentence rules it out. My reconciliation: it is the build's analytical stump, not an open fork. Guidance s2 defines cut off as a state: "a village is cut off when it has no road route to the hospital that an emergency ambulance could use". The envelope (every link that ever floods, closed at once) describes no hour at which any route is unusable together; the shipped hourly series is the only object that can say whether a route exists. The literal execution is the hour-by-hour read, and the thread and I reached the same six by it. It is not the banned flip-the-wrong-number shape: no shipped number is a candidate answer. The model report prints peaks of storage areas, not isolation sets, and the decisive step builds a graph per hour from the hourly stages, the survey and the crosswalk; it is a data-forced analysis, not a choice between two shipped figures. Residual risk, recorded for the main thread: a real reviewer could argue "the design flood" means the peak map, which is why a one-line SF1 (state not envelope) answer stays in the note and nothing should be added to the prompt or guidance. Adding "at any hour" would file the HOW and turn the decisive step into rule application.
2. **Ask 4 payee rule**: three cells (Hollinside, Burnishaw, Upper Quarnell), no shipped fact rules the parish-only reading out. Closure: ledger-side remittance note.
3. **Ask 3 unit and conventions**: all nine rows exposed to the unit; three rows to route extent; three to summed against span; several to the clock. Closure: name the unit, hours in force, local time stated, route closure covered by shipped data.
4. Minor: SURV08 being on the Navigation Datum is derivable only by cross-file inference (overlap with the 2022 survey plus the model report's datum remark). This is the declared ask-2 device D3 and reproduced for the thread (1,254 against 1,348 without it). No action.
5. Gate H Q6 caution (the fund guidance is a very complete procedure): see the next paragraph.

Q6 answer. Guidance s2 states the 0.25 m depth, the node, the sources and the definition of cut off. It states no rule that reads the network at each hour, names the envelope, or says routes are tested for concurrency. Executing every stated rule on the event's peak stages files nine parishes; on its hours, six. By the thread's Gate H a stated rule does not decide the main call: the decisive step (reading connectivity per hour) is analysis the solver must choose, and the stated rules constrain inputs. That the clause is a state predicate is what makes the literal answer determinate; it does not make execution mechanical.

## Next action for the author
Ask-layer repair in the generator, no re-root and no change to the main call, the grants, ask 1 or ask 2: (1) ledger: add a note to the three third-party payments (village hall x2, clerk) saying they were paid at the parish council's request, so ask 4 closes by data; (2) ask 3: name the unit in the prompt's asking clause (each place in the duty log) and "hours in force", state local time as British Summer Time in the log, and ship the route closure's covered sections in the log, then re-assert in checks.py; (3) rebuild twice byte-identical, rerun figures_check.py, precut.py and the leak read, then re-judge once if the author wants a pass 2.
