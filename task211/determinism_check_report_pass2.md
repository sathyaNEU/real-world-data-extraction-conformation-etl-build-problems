# determinism-check report (pass 2), task211, 2026-11-07

## Verdict
DETERMINISTIC on the main call and on every graded figure as filed. Two ask forks have no filed closure and need a pin (below). Minor SOLUTION_WRONG wording applies.
**Disposition:** FIX_NOW. The repairs are solution wording and a pin that fixes only what is true, and no solver-facing analytic surface moves. This is the one re-judge. Further FIX_NOW findings on these two pins would be a dead-design signal under the build rules.
**Stumping type:** mechanism: other (signal classification by each increase's course and end, plus ETL reconstruction on the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread kept the order (derivation.md first, graded_blocks.md after). Its derivation matched the submission on every figure, and the brief held no graded block. It recomputed all 11 detection days (MV334 6 days, max 155; MV129 5 days, max 164), the 24 source checks (2 fails), the 24 timeliness figures and the 39 gross beta figures. Across about 215 increases the 11 are the only ones ending in a single step fall of 85 per cent or more. Natural decays never fall more than 40.6 per cent in a step. Rain at the nearest gauge, neighbours and time of day all misfile (adding about 16 natural events, or clearing 5 true ones). The course-and-end reading is the only survivor, and it separates cleanly (11 against about 200).
The weak point is that no shipped file states the criterion for origin (agreement 2.2 says only "of artificial origin"). It is closed by the data's bimodality, not by a sentence. See Gate H.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MV334 dates, max | 6 days, 155 | same | yes |
| MV129 dates, max | 5 days, 164 | same | yes |
| Natural max step fall | 41 per cent | 40.6 | yes |
| Artificial step falls | 85 per cent or more | 85.3 to 103 | yes |
| Rain within an hour on detection days | 5 | 5 (17 Jul, 20 Jul, 7 Aug, 24 Aug, 17 Sep) | yes |
| Source checks | 24 figures, 2 fails (MV243 89.5, MV184 112.6) | same | yes |
| Timeliness | 24 figures, 95.9 to 100.0 | same | yes |
| Gross beta | 39 figures | same; five fills give identical 2 dp | yes |

## Competing answers that survived
1. **F (fault) records counted as received (ask on timeliness).**
   - The golden sets F records aside because they carry no dose rate. Counting them as received moves 11 stations (MV176 95.9 becomes 96.9, MV142 97.8 becomes 99.3). No 95 line is crossed, but the graded 1 dp figures change.
   - **Closure:** the files do close it, but only through a reading of "value". Procedure section 2 says an outstation "still sends a record for the interval, with the status F and no dose rate", which separates a record from a value. Agreement 2.3 counts "the station's value" and says a test-mode value "is the station's value for its interval". The ingest log counts F records among its records. No shipped sentence states that an F record is not a received value.
   - **Verdict:** closed by wording, not stated. A strict literal executor can defend either reading. The distribution of delays does not help, because F records arrive on time.
2. **LoRa receipt clock read as UTC (ask on timeliness).**
   - LoRa receipts are written dd/mm/yyyy hh:mm:ss with no zone, while every 4G receipt is ISO with Z.
   - Read as UK local time, the delay is 1.6 to 5.8 minutes. Read as UTC, every LoRa record is 61.6 to 65.8 minutes late and about 14 stations move (MV305 96.0, MV142 95.2).
   - **Closure:** no shipped file states the zone. I grepped the three PDFs for local, BST, clock, gateway, LoRa and UTC. The only zone statement is "interval start in UTC" (procedure section 2, and the 2025 change-log row 6), which concerns interval starts, not receipts. The platform alarm configuration says nothing either.
   - Only the data closes it: the delay distribution, where UTC gives a uniform one-hour late band that no live link shows. The design note files the gateway's UK clock as Layer 1 mess, but no document in the pack carries it.
   - **Verdict:** this is an open fork on 14 graded figures. It is closed by data inference only and is not filed. It is the one real determinism exposure.
3. **Set-flow volume as the air drawn (gross beta).** Closed by the producing systems' own column names (`run_totaliser_at_set_flow_m3`, "Volume at set flow") and the procedure's "air drawn". It survives only as a weak competing answer. Zero fill is not reasonable, and all four reasonable fills agree.
4. **Rain, neighbour and night screens (main call).** Ruled out by the data (11 against about 200). No file contradicts them in words, so the exclusion is by data only.
5. **Rounding.** Timeliness figures are 1.1 to 1.5 intervals from a rounding line for several stations (MV129, MV142, MV166, MV184, MV311, MV176, MV243, MV157). They are exact counts, so a solver who does not dedupe the re-sent hours could flip them. The closest source-check figure is MV129 97.526 (0.024 from 97.55). The closest gross beta figure is AF2-26-030 0.4962 (0.0012 above the line, stable across fills). Dose rates are integers.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (csv, xlsx, json, pdf) | yes |
| Large file | 25,000 rows or more | 317,569-row CSV | yes |
| Distractors | 2 or more in metadata, none named in a file name | 2 named (annual report 2025, gamma spectrometry); neither file name says distractor | yes |
| Distractors relevant but unused | each weighable, ruled out by a shipped fact | the thread found both do not answer origin (Cs-137 and I-131 below MDA at samplers). The spectrometry one is only a weak weigh. | yes, with a caveat |
| Deliverables | 1 to 3, all in the golden | 3 (docx, xlsx, svg); all 3 present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 87 figures across 3 tables; prompt pins nSv/h whole, percent 1 dp, mBq/m3 2 dp | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | 883 characters, one paragraph, question first, no count the data hold; 87 ask figures plus the call and components clear 25 | yes |
| Not LLM-generated; goldens read as real work products | | thread found nothing; I read `submission.md` only, not the golden files | yes (not independently checked) |

## Gate G reconciliation
The thread found mechanism "other (course and end)", family analytical_non_defect, surface_read_dependency no and sole_data_defect no. The card and note have `stump_class: analytical`, with the decisive step as judging each excursion by its own last step against the rate at which a washout excess can fade. They file Layer 2 as `estimation_fit`. These agree. The thread names the rain screen and neighbour screens as the surface read that fails, and it does not name the declared distractors (annual report, gamma spectrometry) as carrying the task. The distractors are not too load-bearing. The rain gauges are a natural wrong route, not a declared distractor and not a shipped wrong ranking. No mismatch.

## Gate H reconciliation
The thread says domain pass, layers pass, decisive_step analytical. The note's Three rules agree: the domain test is radon-chain physics, with the swap failing on another field's nouns. Layer 1 is the platform's own mess (microsieverts, duplicates, codes, clocks, totalisers). The decisive step is the fall in one step against what lead-214 and bismuth-214 allow. The analyst test is the nearest-gauge screen landing 16 stations.
Residual risk on rules 2 and 3. The note itself says the deciding physics is "silent... no document states". A reviewer could read an unfiled criterion as a hidden rule. It is not planted (no memo or decoy). The data separates cleanly, and 72 of 72 fall-test settings file the golden, so the choice is not a semantic or rule-application step. I accept analytical, and I flag that the thread's own caveat on this point is fair.
The LoRa fork does not touch Gate H, since it sits on an ask. Asks are free of rule 3, but they still need determinism.

## Stump power (Gate F)
Moderate. The main call is stumped by the nearest-gauge, neighbour and night screens, but a strong analyst who plots the traces will see two plateau stations, so the call itself is landable by a good solver. The textbook route of decay-bound reasoning is the field's method, so I weigh this against the ladder at stumping 1.3. The asks carry the rest: the KIT-2 source swap and certificate by date, the LoRa clock, F handling and measured against set-flow volume. The design note's own naive-route retention on the asks is 16 to 36 per cent.

## Findings, ranked
1. **LoRa receipt clock, unfiled (14 graded timeliness figures).** Only data closes it.
2. **F record handling, closed only by a reading of "value" (11 graded figures).** Not stated in agreement 2.3.
3. **Unsupported words in the solution blocks.** "Radiography" (final recommendation) and "valley" (critical component 3) appear in no shipped file. "LoRa UK clock converted" asserts a zone no file gives.
4. **Origin criterion unfiled.** Closed by the data's bimodality only. Accepted, because a filing would turn the decisive step into rule application.
5. **Timeliness figures sit about one interval from rounding lines.** They rely on identical dedupe and counting, which the earliest-receipt rule closes.

## Next action for the author
Smallest filed closure that moves no graded figure (it files the WHAT, not the HOW):
- **Both sentences into one place.** Add to agreement Schedule 2.3, or to procedure section 2, one sentence on the receipt clock and one on F. Suggested wording for the clock: "Receipts logged by the LoRa gateway are stamped in UK clock time; all other receipts are in UTC." For F: "A record with the status F carries no value, so the platform has not received the station's value for that interval."
- **Why this is the smallest.** The zone sentence states what the stamp is and not how to convert it. The F sentence restates procedure section 2's "no dose rate". Neither changes any golden figure. Neither touches the main call, since both are on the timeliness ask only. No prompt or data file changes, so the bundle needs rebuilding only for the one PDF.
- **Not preferred.** A note in the ingest log header, or a renamed `received_at` column, would change what solvers see in the data file. Prefer the PDF.

Fix list:
1. File the two sentences above in the shipped agreement or procedure PDF, then rebuild, check two byte-identical builds and re-run the free gates. Add both to the design note's fork table with `same call` and assert them in `checks.py`.
2. Delete "radiography" from the final recommendation and "valley" from critical component 3 (both unsupported). Replace "LoRa UK clock converted" with the filed sentence's meaning.
3. Optionally cite the F sentence in solution step 6.
If the author declines item 1, the LoRa fork stays an open determinism finding on a graded ask and I would not approve.
