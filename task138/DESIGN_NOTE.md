# task138: Dunraith substation transfer requirement for the 2027 to 2031 construction work plan (architecture 3)

Private, never ships. Re-rooted on 2026-11-01 after architecture 2 (the Orrinsford levee crown review) was spent at the
re-judge on Gate H3; its record is in `## Architecture 2 record` and its reports are kept with the `_arch2` suffix.
Architecture 1 (the Kestrel Bend season order) is in `## Architecture 1 record`. Seed FC09 numbered the slot; nothing of
its world, decision or quantity is used beyond the objective. Both earlier worlds are closed.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task138.json`, architecture 3, registered 2026-11-01T19:49:38Z; `guard.py check` PASS at registration (redrawn off G14, G7, G6, filed_standard and committee_or_panel). Re-run on the final cut it BLOCKs on the window: builds that stood between task273 (registered 01:51Z) and this card at registration re-registered after it, so task273 (energy-systems-utilities / forecasting, capacity_planner, operations_log) and task125 and task281 (executive_team) now sit in its last three. Open for the main session (the build record below). |
| Domain / task type | energy-systems-utilities / load-forecasting (client domain energy-systems-utilities; the task type serves Forecasting): a distribution substation's summer planning peak for the construction work plan |
| Objective | Forecasting & Predictive Modeling: the planning peaks of summers 2027 to 2031, windows not yet open, with an operating change (CVR on every feeder from 1 June 2027) the history never ran |
| Shape | 02 (a quantity per period): the transfer requirement for each of five summers (5) and the planning peak for each (5), the relief at the planning peak and the weather-normal peak as components; ask A (members' energy by feeder, 8) and ask B (the feeders' peak 15-minute demand on the ten hottest days of 2026, 10); the chart sheet; about 31 criteria |
| Decision | `quantity_figure`, answer unit `count` (MW in whole 0.5 MW switching blocks) |
| Mechanism | gap population then time (the trial's hours are not the planning peak's hours, and the change starts in a window the history never saw); pattern none; generators G8 (reachability against magnitude: the change reaches the voltage-sensitive load, which is the small part at the peak) and G14 |
| Forum and forcing | executive_team; budget_or_appropriation (the 2027 construction work plan and budget) |
| Org and world | cooperative_or_member_body: Breckwater Electric Cooperative, a member-owned distribution cooperative in a fictional Plains state, its wholesale supplier Westmarch G&T; people from `guard.py names`: Julie Gibbs, Peter Roman, Desiree Thompson, Bailey Becker, Sherry Nixon |
| Calibration and context | pilot_log (the 2025 week-on, week-off CVR pilot on three feeders); operations_log (the regulator controllers' event log) |
| Layer 2 | estimand_identification, own: the voltage reduction's effect at the design conditions |
| Shell | question form how-much; second-sentence opener "Work"; rounding opener "Transfers are"; one deliverable, `dunraith_planning.xlsx` with a chart sheet (voice-check quota PASS); architecture 2's shell was whether, alongside, pdf+xlsx |

Data-native sentence: Dunraith's evening peak on a 101 F day is mostly air-conditioner compressors, which draw nearly
the same power at a lower voltage, so a voltage cut that takes 2.4 per cent off the feeders' load over a pilot summer's
hours takes about 1.1 per cent off at the planning peak, and the pilot's own afternoons at 99 F or more show it.

Abstraction: an operating change trialled on a few units, switched in alternate weeks against unswitched peers, is
carried to a forward peak whose conditions the trial's average does not represent; the change acts only on part of
the load, and that part shrinks toward the peak.

Literal-reader test at the draw (the H3 lesson): the filed sentences, read word for word with the default's inputs.
Criteria 3.1 makes the planning peak the highest hourly load on a design-temperature day with every feeder run as the
summer's operating plan sets it; 3.3 adjusts the weather-normal peak by the change's effect on the substation load at
the planning peak. The default's inputs are the line of 3.2 and the pilot's effect over every hour (or at each day's
peak hour, mostly mild days): neither is the effect at the planning peak, so the default is non-compliant on a literal
reading, and the analysis is how to estimate, from the pilot, the quantity 3.3 already names. Run with no CVR at all, the
default fails 3.1 and 3.3 outright. The default is an easier method on correct data, inside a filed WHAT that names what
it leaves out; no shipped artifact is contradicted by the truth.

Dropped before this draw: in `## Tried and rejected`.

## Survivor anatomy

- Actor: the members' air conditioners, a constant-power load with no column of its own; the feeders' MW mix it with
  the voltage-sensitive load and only the hour and the day's heat say how much of each is there.
- Link: the pilot feeders against the comparison feeders, hour by hour, joined to the day's maximum at the airport (a
  standard-time export one hour off the historian's daylight clock); no key invites the join to the weather.
- Reflex: the field's method, the trial's CVR effect as an on-week against off-week comparison against the unswitched
  feeders over the pilot (the average reduction a CVR evaluation reports), sits at rung 1.
- Back-test: the pilot's relief by the day's maximum falls from 2.3 per cent on afternoons under 85 F to 1.1 per cent at
  99 F or more, so the estimate at the planning peak's conditions is read where the data reach them, not extrapolated.
- Second use: the relief at the planning peak is the figure the 2028 to 2031 peaks carry too; every summer's transfer
  moves with it, so one decisive step moves five graded figures and five planning peaks.
- Shock: CVR from 1 June 2027 on every feeder, a change none of the five summers ran except the pilot's three feeders
  in alternate weeks of 2025.
- Pins: the WHAT is filed (3.1, 3.3: the effect at the planning peak; 3.2's line, window, threshold, base summer and
  growth; 4.1's blocks); the HOW of the pilot estimate is open and forced by the data (every hot-afternoon reading
  agrees, SF12 and SF13).

## Default path

1. Read the planning criteria: fit 3.2's line to five summers of daily peaks against the airport's daily maximum,
   102.9 MW at 101 F for 2024, grown at the base case 0.95 per cent a year: 105.9 MW in 2027.
2. See that the 2027 operating plan runs CVR on every feeder and that 3.3 calls for its effect.
3. Estimate the effect from the 2025 pilot the way a CVR evaluation does: pilot feeders against comparison feeders,
   CVR weeks against normal weeks, every hour: 2.4 per cent (or each day's peak hour, mostly mild days: 1.5 per cent).
4. Take it off and round the excess over 104.0 MW up to 0.5 MW blocks.

Ends on: transfers of 0, 0.5, 1.5, 2.5 and 3.5 MW for 2027 to 2031 (no transfer in 2027; from each day's peak hour,
0.5 to 4.5 MW)
Golden: transfers of 1.0, 2.0, 3.0, 4.0 and 5.0 MW (planning peaks 105, 106, 107, 108 and 109 MW, the relief at the
planning peak 1.1 per cent)

## Stump sentence

The capable planner takes the pilot's CVR effect over every hour, 2.4 per cent, off the weather-normal peak and files
transfers of 0, 0.5, 1.5, 2.5 and 3.5 MW (or 0.5 to 4.5 MW from each day's peak hour, mostly mild days), but on the
hottest afternoons air-conditioner compressors carry most of Dunraith's load and hardly respond to voltage, so the cut
takes 1.1 per cent off at the planning peak and the transfers are 1.0, 2.0, 3.0, 4.0 and 5.0 MW.

## Three rules

- Task type: load forecasting (energy-systems-utilities), the summer planning peak of a distribution substation five
  years out, worked the way a utility planner works it, weather-normalised and carried at the load forecast's growth.
- Domain test: the deciding quantity is a planning peak, the load a substation carries at the design temperature, and
  how far a voltage cut lowers it depends on what the load is made of: compressors that draw constant power against
  load that falls with voltage; swap in another field's nouns and the voltage-dependence that sets the answer is gone.
- Swap: "hospital beds" for "MW" and "flu season" for "summer" keeps the arithmetic but loses why a cut acts on part
  of the load only, which is what moves the effect between the trial's average and the peak.
- Layer 1: a historian layout change (kW, hour-ending, one column a feeder, then MW, hour-beginning, long), airport
  observations in Celsius on local standard time, specials between routine reports, a late and a missed pilot switch,
  overnight Bad hours, tables inside PDFs; each asserted neutral (checks R2 lines).
- Layer 2: estimand identification: the effect at the planning peak's own conditions, read from the trial's hottest
  afternoons against unswitched peers, not the trial's average effect.
- Decisive step: read the voltage cut's relief on the pilot's afternoons of days at 99 F or more, pilot feeders against
  the unswitched feeders, because the relief shrinks with the heat: 1.1 per cent, not the 2.4 per cent of every hour.
- Not semantics: no field, code or unit flips the answer; every reading of every column gives the same rows, and the
  answer moves only with which pilot hours stand for the planning peak.
- Not rule application: no filed rule says which hours; 3.3 names the quantity, and a planner executing every rule
  still takes the trial's average effect, the effect a CVR study reports, and lands on 0 MW in 2027.
- Analyst test: a strong analyst who cleans the data and reads every rule still files 0, 0.5, 1.5, 2.5 and 3.5 MW by
  taking the pilot's effect over every hour (asserted on the clean truth, R3a); the easy route is wrong.
- Estimand: the highest hourly Dunraith load on a 101 F day in each summer 2027 to 2031 with CVR on every feeder
  (3.1), carried from the 2024 line at 0.95 per cent a year less the cut's effect at that hour (3.3).
- No decoy: no document states an effect size, a CVR factor or a savings figure; the test plan states settings and a
  schedule only; nothing ranks the transfers.
- No certified replay: no shipped table or memo computes a planning peak, a relief or a transfer; the forecast workbook
  carries growth rates only.
- Lesson: the arch 2 H3 death (a filed procedure read word for word landing on the default) is answered by 3.3 naming
  the effect at the planning peak, which the default visibly substitutes, and by data that are correct throughout.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Neutral (asserted) |
|---|---|---|---|---|
| Historian layout change | the retired SCADA historian | DUNRAITH_FDR_KW_2022-2023.csv | hour-ending labels read as hour-beginning; kW | SF5, R2 |
| Standard-time airport clock | the climate data service | mossford_ap_obs_2022-2026.csv | days cut at standard-time midnight | SF3, R2 |
| Celsius readings | the ASOS export | mossford_ap_obs_2022-2026.csv | rounded to whole F | SF4, R2 |
| Specials | ASOS | mossford_ap_obs_2022-2026.csv | counted with routine reports | SF17, R2 |
| Late and missed pilot switch | regulator controllers | VR_event_log_DUN_2025.csv | the plan's schedule used | SF10, SF11, R2 |
| Overnight Bad hours | the new historian | dunraith_feeder_mw_2024-2026.csv | filled or zeroed | SF16, R2 |
| Tables inside PDFs | the cooperative's documents | five PDFs | none (positive control) | verify.py |

## Readability screen

| Rung | Column or one join | Field reflex | Named in a document | Helper narration | Largest anomaly | File read only by it | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 0, no CVR | the 3.2 line | yes | 3.2 | none | no | no | readable |
| Rung 1, the pilot's effect over every hour | one join of the log to the historian | yes, the CVR evaluation's average | no | none | no | no | readable |
| Rung 2, each day's peak hour | the same join, one hour a day | partly | no | none | no | no | silent |
| Rung 3, the decisive: the effect on the pilot's hottest afternoons (decisive) | three files joined: log, historian, airport by day | no | no | none | no | no | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | summer | June to September | May to September | same call | criteria 2 files it |
| SF2 | the five summers | 2022 to 2026 | 2021 to 2025 | not available | criteria 3.2, five most recent complete |
| SF3 | day of the maximum | local daylight day | the export's standard-time day | same call | asserted |
| SF4 | temperature units | Celsius to F unrounded | whole F | same call | asserted |
| SF5 | old historian labels | hour-ending | hour-beginning | same call | asserted |
| SF6 | pilot days in the line | as run | dropped, or relief added back | same call | 3.2 "as they ran"; asserted |
| SF7 | base summer | 2024, the middle summer | 2026 | not taken | 3.2 files it |
| SF8 | growth | compounded yearly | simple | not taken | 3.2 files it |
| SF9 | growth case | base | high or low | not taken | 3.2 files it |
| SF10 | pilot weeks | the regulator log | the test plan's schedule | same call | asserted |
| SF11 | hours with a switch inside | left out | counted by the start | same call | asserted |
| SF12 | the planning peak's conditions | days at 99 F, 16:00 to 21:00 | 98 or 100 F, other windows, weekdays, each hot day's peak hour | same call | asserted (relief 1.04 to 1.14 per cent) |
| SF13 | relief estimator | ratio of means | a line in the day's maximum read at 101 F, mean of daily ratios | same call | asserted |
| SF14 | transfer basis | unrounded peak | peak to the nearest MW | same transfers | asserted |
| SF15 | CVR in 2027 to 2031 | every summer from 1 June 2027 | 2027 only (1, 3, 4, 5, 6 MW) | not taken | operating plan 3.1: standing practice, every year from 1 June 2027 |
| SF16 | Bad hours | left out | filled | same call | criteria 5; asserted |
| SF17 | specials | counted | routine only | same call | asserted |
| SF18 | ask A, the switching day | 30 June on the old feeder, 1 July on the new | 30 June on the new | not taken | SO-2026-114 opens the switches at 00:00 on 1 July, the day boundary; the paralleled minutes pro-rated give the same figures (asserted) |
| SF19 | ask B, the ten hottest days | local days | standard-time days | same ten | asserted, 1.44 F gap at the tenth |
| SF20 | ask B, interval ending at midnight | previous day | next day | same figures | asserted |
| SF21 | ask B, estimated intervals | kept | dropped | same figures | asserted, overnight only |
| SF22 | ask A, a meter's set day | new multiplier | old | data decide | the kWh falls twentyfold on the set day |
| SF23 | ask B, the summer clock | UTC less 5 hours | UTC less 4, 6 or 7 | same figures | asserted (every hot-day peak ends 18:30 to 19:45) |
| SF24 | ask B, 41-2208 from its repeated stamp | 15 minutes later | as stamped, or the repeat dropped | not taken | only the realigned recorders tie to the historian's hourly feeder total (scatter 0.10 per cent against 1.5), asserted |

## Ladder

| Rung | Handling | Relief | 2027 planning peak | Transfers 2027 to 2031 (MW) |
|---|---|---|---|---|
| R0 | 3.2's line grown, no CVR | 0 | 105.9 | 2.0, 3.0, 4.0, 5.0, 6.0 |
| R1 | the pilot's effect over every hour | 2.4 per cent | 103.4 | 0, 0.5, 1.5, 2.5, 3.5 |
| R2 | each day's peak hour | 1.5 per cent | 104.3 | 0.5, 1.5, 2.5, 3.5, 4.5 |
| Golden | afternoons of days at 99 F or more | 1.1 per cent | 104.7 (105 to the MW) | 1.0, 2.0, 3.0, 4.0, 5.0 |
| Off-path | on against off weeks without the comparison feeders | 3.1 (all hours), 1.8 (hot) | | wrong |

Margins: every golden peak sits 0.24 MW or more from a half-MW edge and every excess 0.22 MW or more from a block edge;
the hot-afternoon family spans 1.04 to 1.14 per cent and every member files the golden (SF12, SF13).

## Closure table

| # | Axis | Closure |
|---|---|---|
| 1 | Population | Dunraith's eight feeders, as run; asks: transformers in the meter data system, recorders 41-2207 and 41-2208 |
| 2 | Unit of account | MW hourly average; MWh; MW over 15 minutes |
| 3 | Attribution window | summers June to September (criteria 2); ask A 1 June to 30 September 2026 |
| 4 | As-of dating | review of 27 October 2026; five complete summers 2022 to 2026 |
| 5 | Version basis | criteria revision 4; the 2027 operating plan; the 2025 forecast's base case |
| 6 | Denominator | relief: CVR-hour ratio over normal-hour ratio |
| 7 | Weighting | none: least squares over days, means over hours |
| 8 | Window length | five summers; afternoons 16:00 to 21:00 |
| 9 | Boundary inclusivity | 85 F or more (filed); 99 F or more; excess rounded up |
| 10 | Rounding path | unrounded to the end; peaks to the MW, transfers in 0.5 MW blocks (SF14) |
| 11 | Tie-break | none arises (tenth hot day 1.44 F above the eleventh) |
| 12 | Maturity and censoring | summer 2026 complete before the review |
| 13 | Order of operations | relief and growth multiply, order-free |
| 14 | Row order | none matters; ask B's repeated stamp read in file order |
| 15 | Duplicate resolution | ask B: 41-2208 repeats a stamp on 9 June and runs 15 minutes early from there; moved 15 minutes later it ties to the historian (SF24) |
| 16 | Identity normalisation | historian point names to feeders; recorders to Exhibit A's metering points |
| 17 | Netting against gross | none |
| 18 | Dimensional units | kW to MW; Celsius to F; kWh to MW over 15 minutes |
| 19 | Code and status semantics | Quality Bad left out (criteria 5); VEE estimated intervals kept (SF21) |
| 20 | Integerisation | whole 0.5 MW blocks (criteria 4.1) |
| 21 | Clause scope | 3.3 applies to every summer whose plan runs CVR, 2027 to 2031 |
| 22 | Forward window contents | CVR on every feeder from 1 June 2027 at all hours; no other change (operating plan 2) |

## Literal reader

Read word for word on the pack: 3.2 gives 102.9 MW at 101 F (561 days at 85 F or more), 105.9 MW in 2027 at 0.95 per
cent compounded from 2024; the operating plan runs CVR on every feeder from 1 June 2027; 3.3 asks for the change's
effect on the substation load at the planning peak, which 3.1 puts on a day at the design temperature. The pilot is the
only evidence of that effect, and its afternoons on days at 99 F or more (the planning peak's conditions within the
pilot) give 1.1 per cent; every reading of those conditions agrees (SF12, SF13). 4.1 then gives 1.0, 2.0, 3.0, 4.0 and
5.0 MW. A reader who executed the filed procedure with no CVR would breach 3.1 and 3.3; one who took the pilot's all-hours
effect would breach 3.3's "at the planning peak". `verify.py` runs this path on its own readers.

## Oracles

- The world's own relief at the design afternoon, 1.04 per cent, beside the golden's 1.08 (checks R3a).
- The world's energy by feeder and its daily peaks, against asks A and B (checks, exact at the rounding).
- `verify.py`: CSV, XLSX and PDF read on its own code path; every graded figure recomputed and matched.

## Ask sheet

Two asks, both off the main call's rows: the call reads the historian, the airport, the regulator log, the criteria,
the operating plan, the pilot plan and the forecast; the asks read the meter data system, the register, the switching
order, the MV-90 export and Exhibit A, which the call never reads (asserted: the call computes with them deleted).

- Ask A, members' energy by feeder, June to September 2026 (8 figures, MWh to 10; the budget's revenue papers).
  Primary device (D7, the true key elsewhere): the meter data system and the register carry each transformer's feeder
  as the GIS holds it now; SO-2026-114 moved the sections beyond S-1302, S-4471 and S-6120 on 30 June and lists
  switches, not transformers, so the June energy of 25 transformers belongs to their old feeders only once the register's
  device tree is traced below each opened switch (two levels: a fuse under the switch, a recloser and its fuses). Second
  primary (D2, a label stored after a silent switch): three LP-3 services went onto CT metering on 2 and 3 June, the
  register holds today's multiplier and set date, and their kWh falls twentyfold on the set day; the register's
  multiplier on every day overstates DUN-5 and DUN-7. Hazard: multipliers held in the register (every feeder).
- Ask B, the feeders' peak 15-minute demand on the ten hottest days of 2026 (10 figures, MW to one decimal; the
  supplier's demand bills). Primary device (D2/D8): from 9 June recorder 41-2208 stamps each interval at its start
  under the export's interval-ending header; its stamp repeats once there, and summing the two recorders by stamp pairs
  each T1 interval with the next T2 one. The alignment is determinate: only the realigned pair ties to the historian's
  hourly feeder total. Each recorder reads its own bus (T1 DUN-1 to DUN-4, T2 DUN-5 to DUN-8) and T2 carried both
  while T1 was out on 15 and 16 September. Hazards: UTC interval ends (the hot-day peaks
  end at 18:30 to 19:45 CDT, across UTC midnight); recorder 41-2391, the 69 kV line terminal, which Exhibit A's
  delivery point demand includes and the feeders do not.

| Ask | Golden | Cracker handling | Cracker figures | Cracker |
|---|---|---|---|---|
| A, feeders the reconfiguration touched (DUN-1, 2, 3, 4, 6, 8) | 16,600, 16,210, 17,670, 11,150, 8,990, 15,850 | multipliers on every day, feeders as recorded | 16,050, 16,830, 18,210, 10,570, 8,360, 16,430 | miss |
| A, DUN-5 and DUN-7 | 16,980, 14,810 | multipliers on every day | 17,120, 14,880 | miss |
| B, ten days | 112.9, 101.2, 101.6, 98.2, 97.9, 96.2, 95.5, 94.4, 90.9, 92.8 | CDT, T1 + T2, repeated stamp dropped | 112.6, 100.9, 101.7, 98.7, 97.4, 96.4, 95.3, 94.6, 90.5, 93.0 | miss |

Mirror: off the call at rung 1, the same ask handling (nothing in the asks comes from the call): 0 of 18. Stress rows
(not the gate): the tracer (also traces the moved sections) keeps 6 of 18; the full includer keeps 18 of 18.

Pair ceiling: 28.5 (cracker 45.0, mirror 12.0)
Mirror leakage: 0.0 per cent of the ask weight
Measured by: generator/ceiling.py on the cut pack

## Prompt

`prompt.txt`, 949 characters, voice-check PASS: question first (how much load to transfer in each summer 2027 to 2031
with CVR on every feeder), the criteria as the WHAT, the two asks, one workbook with a chart sheet, rounding last. No
count the data hold; no persona.

## Leak review

`leak.py --asof 2026-10-27`: REVIEW, no LEAK. Answer figures: 2.0 (bandwidth 2.0 V in two PDFs) and 0.5 (the
switching block, a filed input) are inputs. The call's words in the
criteria and the pilot plan are the world's nouns. Column names PROTECTIVE_DEVICE, Equipment and DRY_BULB_C are the
source systems' own. Stump vocabulary: none of the decisive step's words (afternoon, compressor, constant power,
relief) appears in a shipped file.

## Stage 4 round 1

The judge: DETERMINISTIC (SOLUTION_WRONG in wording only), FIX_NOW, order kept. The main call reproduced independently
(102.93 MW at 101 F over 561 days; transfers 1 to 5 MW for any CVR effect between about 0.88 and 1.31 per cent), asks A
and B reproduced, Gate F strong, Gate G PASS (statistical rigor, analytical, no surface read, no sole defect), Gate H
PASS (decisive step analytical). The leak reader found no leak. Fixed in the generator in one pass:

1. Write-up wording: step 2 names DATE_LST (local standard time) and DRY_BULB_C; step 3 the hours beginning 16:00 to
   20:00 (65 and 50 hours); step 7 says what the export shows (41-2208's repeated stamp and the 15-minute move) and why
   (the tie to the historian); step 6 the June meters as the register and the data show them.
2. Ask A, feeder membership: SO-2026-114 now closes the ties at 23:56 to 23:58 on 30 June and opens S-4471, S-6120 and
   S-1302 by SCADA at 00:00 on 1 July, and its closeout states the sections are carried on the new feeders from 00:00
   on 1 July, the meter-reading day's start; no daily reading is split (SF18).
3. Ask B, the T2 recorder: each recorder now reads its own bus with its own scatter (T2 to T1 from 0.906 to 0.933, no
   fixed multiple), T2 carried both buses while T1 was out on 15 and 16 September, and the realignment is decided by the
   tie to the historian's hourly feeder total (scatter 0.10 per cent realigned, 1.5 as stamped; SF24).
4. CVR beyond 2027: the operating plan files it as standing practice, every year from 1 June 2027 (SF15).
5. Time zone: every offset from UTC less 4 to UTC less 7 gives the same ten figures (SF23).
6. Realism: the spring regulator confirmations at irregular crew-visit times; tie capacities and conductor limits at
   working values.

Resume: the re-judge, then the author's decision on the guard window BLOCK.

## Build record

Built 2026-11-01 and rebuilt after stage 4 round 1; every gate on the final cut is in `pipeline.json` and the report.
Generator: `generator/build.py` builds twice from the fixed seeds, byte-identical, and installs `target/`, `golden/`,
`metadata.json`, `generator/figures.json` and `target.zip`; `generator/writeup.py` emits `submission.md` from
`figures.json`. `checks.py` (77 assertions: R1 to R3c on the clean truth, the ladder and margins, SF1 to SF24, Layer 1
neutrality, the asks' devices, truth and alignment, separation, distractors, input gates, realism sweep, the golden
workbook), `verify.py` on its own CSV, XLSX and PDF readers (every graded figure and the recorders' tie),
`figures_check.py`, `precut.py`, `voice-check.py`, `leak.py` REVIEW, `ceiling.py` (pair 28.5). Pack: 15 files in three
formats (seven CSV, five PDF, three XLSX), the largest `dunraith_feeder_mw_2024-2026.csv` at 70,272 rows; distractors
`OMS_outage_events_2026.csv` and `DUN_feeder_ties_2026.xlsx`. Open: `guard.py check` and `heart` BLOCK on the window
(ban.pairing, ban.role and ban.artifact against task273 v6, ban.forum against task125 v4 and task281 v3), which passed
at registration; the heart's driver similarity is 0.07 at most; the decision is the author's.

## Architecture 1 record (shipped 2026-10-15, re-rooted 2026-11-01)

- Draw: the Kestrel Bend Irrigation District's 2027 season order from the Tolan Valley Project (California),
  physical-environmental-sciences / hydrology-flood-frequency, shape 13, question form how-much; the order at the
  headgate requirement covered in 24 of 30 replayed weather seasons through a daily root-zone balance of each field.
- Round 3 golden: 212,000 acre-feet, each replay started from the root-zone state the 2026 record leaves at the
  efficiency the soil moisture network's season shows; default path 215,000 (the record run at Table 4's design
  efficiency). Rounds 1 and 2 are in the lines below (round 1 weak on the 10/10 audit, round 2 read as rule
  application).
- Build: shipped 2026-10-15 (19 files in `target.zip`, 2,541,365 bytes, sha256 50c887dc), determinism and leak reports
  kept with the `_arch1` suffix.
- Fate: no portal result; re-rooted 2026-11-01 at the Batch 3 queue reset (one architecture per world: the
  irrigation-district world is closed); its card identity is in the v2 card's `lineage`.

## Architecture 2 record (built 2026-11-01, spent the same day)

- Draw: the Orrinsford Levee and Drainage District's crown review, physical-environmental-sciences /
  hydrology-flood-frequency, shape 04, question form whether; the 1 per cent annual chance flood for the river as it
  now runs, rebuilt from Coyle Bridge through the post-raise relation, carried through Table 4 to a whole-foot raise.
- Golden: raise the crown 2 ft (design discharge 110,000 cfs); default path no raise (95,000 cfs, LS-02's fit to the
  published Orrinsford record).
- Build: round-1 repair green, `target.zip` 81bc1b75; reports kept with the `_arch2` suffix.
- Fate: spent 2026-11-01. The re-judge (derive-first) returned NOT_DETERMINISTIC, SEND_BACK on Gate H3: LS-02 s.3 and
  s.8 read word for word send the fit to the published Orrinsford peaks (95,000 cfs, no raise), and s.2's "as they
  stand" was not read as requiring a reconstructed record. One architecture per world: the levee and flood-frequency
  world is closed.

## Tried and rejected

- The seed's loss-per-refill mixture (fill per refill plus seepage per wetted day, recovered from the 270 closed lateral
  balances): the same driver as task67 (a fixed-plus-variable cost carried per unit onto a denser period), and its
  dry-out gap was a rule recovered from a closed corpus; dropped at the draw.
- Seed 1380202 for the world: the setting year was the same on every rung, so the setting year and its requirement
  carried nothing; moved to 1380206.
- Six-inch flashboards with the board height in the structures sheet: the bare-crest spill exceeded a lateral's whole
  measured loss, so the device announced itself; cut to 2-inch boards whose height is only in the riders' remarks.
- Planning tables with even last digits (root depths in whole feet, allowable depletion fractions of 0.50): replay days
  landed exactly on an allowable depletion in most weather years, so the irrigation test was settled by floating-point
  noise and several monthly figures moved between the two tie-breaks; Tables 2 and 3 re-cut so every allowable
  depletion is an odd number of hundred-thousandths of an inch (asserted), and the walnut June coefficient set at 1.11
  to keep the months clear of their rounding edges.
- One WOP 2.4 sentence stating that a replay starts from each field's depletion at the end of 31 January, carried from
  its last delivered 2026 set (the judge's optional hardening, 12 October): refused. It names the decisive rung and
  pins the method, turning R3 into rule application; the start stays forced by WOP 3.1 and 3.4 on the record (SF9).
- Every replacement meter at a near-zero register (the reader's random-looking registers): a solver who counts a new
  meter's first read from zero would recover 307 of the 500 acre-feet the 31 swaps hide, and bench-test registers
  summing to 0.8 acre-feet on Lateral 3's two would put its delivery back in the golden's bin; kept the shop's real
  mix instead, 14 new meters at 0.00 and 17 rebuilt with their carried registers, every Ask A figure off on that
  path (S2b).
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK, 2026-10-14), because its stump (each replay started
  from the depletion each field carried on 31 January, from its last set taken as a refill, against a full start) was the
  same gap as the judge's one open fork (no filed sentence fixed the 1 February state, so the DETERMINISTIC verdict was
  conditional on it), the decisive step was visible (the 64,887-row orders file the one large non-distractor file the
  default path never read, Table 1's November to January coefficients, the weather run to 31 January 2027; the judge and
  the reader both found it unprompted), and Ask A's meter chaining was crackable through the shop log's registers with no
  second device on the figures it moved.
- Filing the start state (WOP 2.4) on round 1's world: the literal estimand made round 1's golden the default path with
  nothing left to decide (every field's last set had refilled it in that world); the growers were rebuilt so the drip,
  micro-sprinkler and sprinkler fields are held at a working deficit, which only the record's water shows.
- An unscoped sentence that an irrigation returns the root zone to field capacity (round 1's WOP 3.4): its literal
  execution on the 2026 sets is the default path (a filed sentence whose literal reading gives the easy answer, a
  main-call fork); scoped to the replays ("In a replay").
- Filing a field-capacity start on 1 February 2026, or the record run itself: names the method (rule application); left
  to the data (SF12, the run converges from any start before the wet winter).
- Grading the monthly schedule (WOP 5.1): R3's monthly shares matched the golden's from May to September, five of nine
  months free to the default path; dropped from the prompt.
- Grading the setting replay's requirement to the nearest 10 or 100 acre-feet: defensible constructions of the record
  run (SF13 to SF16, SF22, SF27) move it by up to 267 acre-feet, across those bins; dropped, and the order moved to whole
  thousands so every construction lands in one bin.
- Asking for the setting weather year: the default path and every near correction also land on 2012, a free criterion
  for the mirror; dropped.
- The Lateral 5 tail reach (05-045 to 05-058) re-served through a connector: replaced by the west spur (05-021 to
  05-034), every spur meter read on the change day and no water across it, so the as-of assignment converges.
- A heading logger cutover (a clock change in mid-season) as Ask 2's device: it moved only the days at the season's
  edges and announced itself in the daily series; replaced by the logger outages whose estimates sit in the operations
  log.
- Closing SF14 (the record's water within a day) by an evening convention: abandoned; the three orders of a day converge
  on the order and the year (asserted).
- `UNIT_SALT` 0 (the first draw of which replacements came new): a new meter's first read counted from zero landed
  Lateral 2's deliveries in the golden's bin (1.5 acre-feet off); redrawn (14), every lateral 18 acre-feet or more off.
- Cancelled sets placed after a field's last set and allowed to run past 31 October: two 2026 orders ended on 1
  November, a set the ordering system would not take after the canal's close; such a set is no longer placed.
- The asks' motive as round 1 worded it ("Our loss allowances will be set against what the laterals did in 2026"): it
  named a later decision with another owner (the Board's next allowances), the H18 defect; retied to the call as the
  audit trail of the allowance the order carries for each lateral.
- The record run started at field capacity on 1 February 2026 and the golden's note saying the winter had every root zone
  full then: four dry days after the 27 January rain left every field up to 0.17 inches short on 1 February, so the note
  was not true of the record (H6); the run now starts from the end of 27 January 2026, when every root zone was full
  from any November state (asserted), and files the same state on 31 January 2027.
- A WOP sentence crediting each field's 2026 delivered sets to its root zone, to answer the judge's round 2 residual:
  refused. It files the HOW, the decisive step's own estimator, and turns the record run into rule application; the
  residual is closed by the estimand and the data instead (SF34, asserted on the clean truth).
- Round 2 shipped design: decisive step read as rule application per the rule 3 audit (2026-10-15, VERDICT FAIL), because
  its start state was the procedure's daily balance (WOP 3.1 to 3.3) executed on the 2026 delivery record at Table 4's
  efficiency, which the table's note then defined as "the share of the water delivered to a field that its root zone
  receives", as WOP 2.4 pointed to; executed word for word on clean data it gave the golden (215,000) with no parameter
  fitted, no state uncertain and no candidate estimators separated by data. Kept the world, the order rule, the replay
  model and the estimand; the start is now an estimate (Table 4 scoped to WOP 3.5, the record's efficiency fitted on the
  soil moisture network), and 215,000 is the default path.
- The audit's proposed late-January probe snapshot on a random sample of fields of each method (prototype, 65 probed
  fields): the probed fields' mean share of total available water by method, an additive offset of the Table 4 run and
  a regression on the probes each landed in or next to the golden's bin (217,000 against 217,000 at an efficiency below
  Table 4; 212,000 and 213,000 against 212,000 above it), so the probe file's natural use was the answer and the file
  a signpost; replaced by a season-long station network whose 31 January readings cannot see the efficiency.
- A probe sample skewed by crop (no tubes in the shaken nut orchards) or by the last set (cooperators' later sets),
  prototype: the transfers' misses swung a bin either way with the efficiency and the draw, never a structural miss;
  replaced by stations in the early blocks, which the dry autumn takes to the bottom of their root zones under any
  efficiency, so the January snapshot is blind for a computable reason.
- The record's efficiency below Table 4 (systems short of design): the start saturates near total available water, the
  order flattens (216,100 to 216,400 across 0.88 to 0.94 times Table 4), the stations' January share lands the golden's
  bin, and the growers' orchards would have run far past allowable depletion all summer; replaced by an efficiency above
  Table 4 (a deficit set loses little below the root zone), 1.0425 times it give or take 0.004 field to field.
- Re-simulating the growers on the record's efficiency (each set sized to the true share): it moves every set, the
  meter book, the headings, the weirs and every ask figure; dropped: the growers keep sizing their sets on Table 4 (the
  2026 record unchanged byte for byte) and only the root zone as it is runs on the share that reaches it.
- Stations drawn without the January property (`STATION_SALT` 0 to 8 at 1.04 times Table 4): five to nine of the eleven
  stations blind, the rest still short of the bottom of their root zones on 31 January, so their January offsets showed
  the Table 4 run's excess and an offset correction moved to 214,000; redrawn (9): every station's 31 January state the
  same under Table 4 and under every efficiency up to its own (asserted), the order 212,000 with its 24th mid-bin.
- The grant's name ("water use efficiency") in the station export's title line: the stump's own word in a main-call
  file; the grant is named the state's on-farm water conservation grant.
- Fitting each station by golden section alone: on a small pasture root zone the misfit's floor is flat and bumpy (local
  minima 0.0005 apart), so the verifier's own search settled elsewhere and one replay crossed a 10 acre-foot line; the fit
  is now the best of a ten-thousandth grid, refined, and the verifier scans the same grid on its own code.
- The ranch names (a place or bird word plus Ranch, Farms, Vineyards: "Juniper Vineyards" on 11 request rows, 203 names
  over 688 rows) and the operations log's nine outage pairs in one frame ("Lateral N heading flume: ... No logger total;
  Water Master estimating ..."): generator tells under the wave 3 bar; replaced by grower accounts drawn the way an
  east-side district's accounts read (family farms, partnerships, trusts, a few road-named LLCs, account names unique) and
  outage entries in their writers' own words, every estimate and ask figure unchanged (asserted).
- A March station gap noted as the probe pulled for the grower's ripping, on an alfalfa block: ripping is an orchard and
  vineyard job; the note now says gophers chewed through the logger cable.
- The round 3 judge's optional prompt clause filing the start "from the root zone the District's 2026 deliveries and
  soil moisture readings put each field in on 31 January" (a WHAT, not the fit): declined at ship; it names the decisive
  step's evidence in the prompt, a single-purpose sentence the wave 3 bar bans, and the judge found the method forced by
  the data without it (SF48).
- Architecture 1 (Kestrel Bend Irrigation District, round 3, 212,000 acre-feet): shipped 2026-10-15 with no portal
  result and re-rooted 2026-11-01 at the Batch 3 queue reset; one architecture per world, so the irrigation-district
  world is closed and the slot redrawn as architecture 2 (`## Architecture 1 record`).
- Draw candidate, TV audience flow after a lead-in change (2026-11-01): spent at the slots screen (task115 and task174
  rejected the same inherited-against-loyal audience law); dropped before a card.
- Draw candidate, hospital weekend discharges and the Monday pile-up: spent (task127 loop 1 and task170); dropped.
- Draw candidate, a gauge's stage-discharge rating drifting with channel aggradation so the published discharges carry
  a level shift: removing an artefact from a published series is catching a defect (rule 3's planted-defect ban, the
  literal standard is the golden), and the field's correction is a reflex once seen; dropped at the draw.
- Draw candidate, rating hysteresis on the rising and falling limbs of a flood: spent at the abstraction test
  (task279's concentration-discharge hysteresis screen) and decided by a field reading of the loop; dropped.
- Draw candidate, a reservoir upstream regulating the flood record: the agency codes regulated peaks and Bulletin 17C
  names the remedy (the post-regulation period), so the step is read off a code and the reflex lands it; dropped.
- Draw candidate, landfill airspace with waste settlement: the field's settlement curve fitted to the survey record
  would itself be the golden (no precondition the data violate), the method-at-the-top shape 1.1b forbids; dropped.
- First card draft (2026-11-01): `ban.pattern` G5 (task125), `ban.artifact` register and `ban.forum`
  board_of_directors (task133); redrawn to G16 then G6, `published_series`, `trustees_or_governors`. A G13 decisive
  generator with gap time hit `test.same_driver` inside the batch, not clearable by differentiation; dropped.
- First personas from a hand list (James, Danielle, Richard, Jennifer, Matthew, Nicole): `people.first` WARNs; replaced
  by the seed-138 draw (Dennis Zhang, Kristin Lucas, Eric Thornton, Jesus Hernandez).
- Orrinsford's drainage area at 5,900 sq mi in the prototype: the drainage-area ratio at exponent 0.5 landed the golden's
  raise (a cheap route on the call, Gate F); set to 6,480 sq mi (ratio 1.314), the area routes now file 3 ft or more.
- Other world seeds in the draw-stage search (a scratch screen, not shipped): many put the at-site route or the
  post-raise-only route on the golden's raise, or made the trend tests significant; seed 1445 puts every rung on its
  own raise with trend tests at p 0.48 and 0.77 and the golden family inside one design-discharge bin (asserted in
  `checks.py` on the shipped pack).
- A crown built knot by knot from Table 4 margins (each cross-section's own shortfall, -1.50 to +0.41 ft): the 50 ft
  survey points between cross-sections near the railroad bridge, inside its 4 ft freeboard zone, came within 0.1 ft of
  2 ft of shortfall (a fork on where the crown is checked), and a 650 ft misaligned survey join produced negative
  settlement; the crown is now a smooth as-built grade, the bridges short only through their afflux and extra
  freeboard.
- Annual chances under the first hydraulics (WS_C 7.30, exponent 0.55, railroad afflux 1.45): the golden family's
  spread left the five settings at best about 0.009 percentage points inside their one-decimal bins (a scratch
  measurement on that pack); the hydraulic model
  re-cut (6.80, 0.58, 1.40) and the railroad crown placed about 1.48 ft short, every setting now 0.012 points or more
  inside under all twelve constructions (asserted).
- The 2016 stationing as a 2019 extension (old station plus 650 ft): a station-number join then gave settlement 0.16
  ft too small, negative in four reaches, so the device announced itself; the 2019 work is now a realignment that
  took the first 650 ft out of service, the join's error is positive everywhere (silent).
- The Main Street sill at 617.60 and then 617.90 ft: under the re-cut hydraulics the 2025 flood no longer reached it and
  water year 2022 sat within 0.33 ft; set to 617.45 ft (2025 reaches it by 0.35 ft, 2022 stays 0.68 ft below).
- Estimate codes on early Coyle Bridge and Orrinsford peaks: dropping the estimated years moved the design discharge to
  115,000 (a Layer 1 item moving a critical component, R2); the codes now sit on the Ashby, Gale Creek and Fenwick rows.
- A Notes sheet in the DNR inventory (what RM and "Crown raised" mean): a sheet describing the data
  (`dataset-generation` section 3); removed, each column's header carries its meaning.
- OP-04 (2014) listing the closures at 62+40 and 118+70: the present stationing dates from 2019, an anachronism and a
  second key to the ask A device; the closures are named only.
- LS-02 (April 2018) naming "the 2019 hydraulic update": a document citing a later one; it now names the district's
  current hydraulic study.
- Table 4's discharge grid at 60,000 to 150,000 cfs in 10,000 steps: its 110,000 column header is the golden design
  discharge to the nearest 5,000, a `leak.py` sweep 3 LEAK by coincidence; the grid now runs 65,000 to 155,000, and the
  crown was re-placed (1.485 ft short in the world, 1.48 ft on the survey) so every annual chance stays mid-bin.
- The town named Halbrook: one letter from real towns named Holbrook (`reduce-house-fixes` H21) and already used by
  five builds on file; renamed Orrinsford (district OLDD, logger ORF2, benchmarks OL-), no figure moved.
- The ORF2 logger export with battery voltage and enclosure temperature: the battery's charging hour profiles the clock
  in one file (a hygiene-battery item, so the cracker kept the three 2020 floods); the export now carries stage alone
  and the clock shows only against the published peak times or the Coyle Bridge travel time.
- OP-04's warning as "21.0 ft on the gauge (elevation 661.00 ft NGVD 29)" with the prompt asking for the warning
  stage: a literal reader could take the gauge figure as the trigger after the datum change (a fork on ask B); OP-04
  now files the warning level as the elevation with the gauge figure in brackets, and the prompt asks for the warning
  level.
- The Orrinsford gauge datum at 608.00 ft NAVD 88: low-flow stages read about -1 ft on the ORF2 logger, below any real
  gauge datum's floor; set to 600.00 ft (599.73 ft NGVD 29), the sill at 17.45 ft on the gauge, every crossing and
  lead time unchanged (both datums whole feet, so the hundredths round alike).
- LS-02 s.3 with no window and s.8 saying the annual peaks are "those published by the State Water Survey" (judge
  round 1, Gate C): the 18 water years since the last raise met s.2 and s.8 as written (1 ft), and s.8 read literally
  forbade any rebuilt year; s.3 now files the window (one peak for every water year since 1962) and s.8 the source
  only. The judge's wording ("the discharges the present river would carry in the years of the Coyle Bridge record")
  was refused: it names the move.
- The relation at about 2 per cent scatter (intervening share sd 0.018, noise 0.011) around 1.078: the judge's
  extension forms ran 111.2k to 113.6k, the top past the 112,500 edge; the intervening tributaries' share made steadier
  (they crest a day before the main stem reaches town: sd 0.009, noise 0.0055) and smaller (0.065), centring the
  design discharge at 110,403 with six forms at 110,260 to 110,477.
- Published peak times off the hourly records by 0 to 3 h (each crest pulled earlier by a falling baseflow), which
  pointed at a 4 h clock: the published times are now the hour the agency's own record tops out, each annual crest a
  single top hour in every shipped series (crest sharpness set per flood).
- The ORF2 logger swap as a 7 h gap: nothing inside the export fixed the old clock; the two loggers now run together
  for three days and line up only at 6 h.
- Lead times with fractions up to 0.86 h: truncation filed other whole hours (judge round 1); every lead now sits 0.1
  to 0.4 h past its whole hour.
- Reach descriptors ("north tie-in to Pump Station 1" and the rest) in the golden and the write-up with no shipped
  source: dropped; the reaches are their ids and station ranges from the 2024 survey.
- A 2024 survey every 50 ft against a 2016 survey every 100 ft with a 650 ft realignment: the 2016 shots paired with
  one 2024 shot in two, so the surveys' reach means differed from the paired figure (R1 0.06, R2 0.11, R8 0.10);
  both surveys every 100 ft and the realignment 700 ft, pairing one to one.
- Table 4 with one uniform fall and a crown falling smoothly at round steps (the leak reader read both as computed):
  reach slopes, cross-section effects and the bridges' afflux in Table 4; low spots, the 2019 tie-in step and the
  Cedar Street floodwall's level top in the crown, none within 400 ft of a bridge.
- The 2025 inspection summary with an overall-rating paragraph and a follow-up line: restyled as the DNR checklist's
  item, station, rating and remark table.
- The Coyle Bridge datum change in October 2021: with the ORF2 overlap now visible to the battery, a cracker fixing
  the clock would have kept the three 2020 floods; the change moved to 22 October 2019, before every flood in the ask.
- The Main Street sill at 617.45 ft under the repaired hydraulics: the 2025 flood crested below it; set to 616.95 ft
  (2025 over it by 0.42 ft, water year 2022 0.74 ft under).

- Architecture 2, the Orrinsford levee crown (the present river rebuilt from Coyle Bridge): spent 2026-11-01 at the
  re-judge on Gate H3, LS-02 s.3 and s.8 read literally landing on the published-record fit (95,000 cfs, no raise);
  the filed procedure itself produced the default, so the next draw files a WHAT the default visibly substitutes.
- Candidates dropped before architecture 3: demand response added back to a peak (task173's 4CP ground); a coincident
  new load (task164); a reservoir inflow mass balance (task118, task120 storage change); urgent care diversion (task171
  and task174 ground, a weak rule 1); new subdivision yields (task174, task150); historical floods or an ungauged
  transfer (the flood world is closed).
- Card redraws at the architecture 3 draw: decisive generator G14 (task133), G7 (task255) and G6 (task281); G2, G13 and
  G3 on driver similarity; context artifact filed_standard and forum committee_or_panel (task281); personas redrawn off
  first-name WARNs.
- Air conditioning saturating at 97 F (exponent 1.8): the weather line read 6 MW above every 101 F day, which no
  planner would file; saturation at 102 F, exponent 1.5, puts the line at the hot days' mean.
- The airport export in UTC: a UTC-day reading moved the line 0.29 MW and crossed the 2027 block edge, so the clock
  carried the call; the climate service's local standard time, an hour off the historian, is neutral.
- The switching order listing the moved transformers: it narrated ask A's device; it now lists switches and sections,
  and the transformers come from the register's device tree.
- The T2 recorder swap on 28 July: four hot days fell before it and the cracker kept them; moved to 9 June, before
  every hot day.
- The 2026 summer on the shared weather stream: the tenth and eleventh hottest days 0.1 C apart; 2026 drawn on its own
  stream, 1.44 F apart.
- The outage log running to 31 October, after the review: cut at 20 October.
- SO-2026-114 switching at 23:22 to 23:52 on 30 June: the day's meter reading straddled the move and putting 30 June on
  the new feeders shifted six figures by 20 MWh (the judge's Gate C residual); the switches now open at 00:00 on 1 July.
- T2 as a fixed 12/13 of T1: real transformers never read so; the judge recovered the recorder's shift from that
  ratio alone; each recorder now reads its own bus with its own scatter and the historian's total decides the shift.
- CVR filed for 2027 only: 2028 to 2031 read without it give 1, 3, 4, 5 and 6 MW; the operating plan now files it as
  standing practice from 1 June 2027.
