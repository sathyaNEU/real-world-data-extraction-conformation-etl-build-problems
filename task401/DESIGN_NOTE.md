# task401 design note

Architecture 4, drawn 2026-11-03. The number was handed out against seed RC07 (a supplier's January imbalance bill).
The seed's world could not carry an honest unbanned draw; architecture 1 (a frailty virtual ward against care home
closures, Epidemiology and Public Health) and architecture 2 (a canola hybrid against July heat, Economics and
Econometrics) died at stage 2, and architecture 3 (a GB energy supplier's new-customer satisfaction fall booked to its
billing platform that its quote journey caused, Marketing and Consumer Research) was spent at stage 4, round 2, on an
ask's unfiled re-attribution while its main call held (`## Tried and rejected`, the card's `lineage`). One architecture
per world: architecture 4 moves to Physical and Environmental Sciences, a water and sewerage company's river catchment,
a new dataset and a new shell (`CLAUDE.md`, a dead design is re-rooted at once).

The world: Wendmoor Water, an invented water and sewerage company in the English East Midlands. Its Coldmere Water
Recycling Centre (an activated sludge works serving about 41,000 people and five trade dischargers) discharges to the
River Allery, a lowland, high-alkalinity river whose water body must reach good ammonia status. A continuous water
quality monitor below the works, part of the company's section 82 programme, has logged fifteen-minute ammonium since
October 2024. From November 2025 it logged a run of days with total ammonia above the good-status standard, against a
handful the winter before. In the same weeks the works' ammonia-based aeration control went into service (27 October
2025), a new turbo blower took the aeration duty, housing growth had taken the works close to its design load, the
winter was cold, and Thornlea Dairy, a trade discharger to the works' sewer, started a strained yoghurt line whose acid
whey is held on site for tanker collection (3 November 2025). The company's asset plan carries a GBP 14.2 million
nitrification upgrade at Coldmere, and the environment programme submission due to the Environment Agency in January
2027 has to say whether that upgrade is the answer.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v4, registered after `guard.py check` at WARN
  (overuse.objective: the slot's objective is fixed by its number; repeat.gate_g and overuse.gate_g: the mechanism that
  carries the stump is a split of failures between sources, honestly `decomposition_attribution`, and the strategy
  window is answered by the decisive move's family below). Structural tests against task36 R1, task83 v1 and task127 v2
  answered by differentiation lines on the card: none of them reads a contributor's discharges through a shared
  process's recovery.
- **Pairing:** Physical and Environmental Sciences (client domain), task type `pollution-source-attribution`, which
  serves Root-Cause Analysis in the taxonomy; objective Root-Cause Analysis; shape 12 (drill-down to one leaf: the
  winter's exceedance days, river to works to the works' failure days to the one discharger and its evenings).
- **Strategy:** `population_selection`, pattern C (the serviceable share behind a join): the deciding quantity is the
  share of the exceedance days each option can reach, the dairy's whey handling against the works' upgrade, behind a
  join of the dairy's fifteen-minute chamber record, the works' daily effluent record and the monitor's days
  (strategies.md F7, approved on 25 and 28). Generators G8 reachability versus magnitude (by load the dairy barely
  registers; by reach it carries every exceedance day), G3 record versus operation, G7 operating window. Gap population
  (the works' failures are not the works' own), objective second (the load apportionment is correct and is not what the
  decision is scored on). The window bans `binding_constraint`, `causal_design` and `decomposition_attribution`
  (task399, task400, task402); the decisive move is the construction of the reachable population, so the label is the
  move's own family, not a relabel.
- **Data-native sentence:** Thornlea's acid whey, run to its trade effluent drain on the evenings after a missed tanker
  collection, shows in its own fifteen-minute chamber record only as an evening hour at production flows and pH 6.1 to
  6.4, inside its consent's 6 to 11 and beside its benign night-time acid rinses; the weekly composite (Wednesday to
  Thursday) never holds one; at the works the whey's oxygen demand starves the nitrifiers for a day, so the river's
  exceedance days sit one or two days after evenings that no charging, compliance or process record marks.
- **Abstraction sentence:** a small contributor's short discharges switch off a shared process for days, so the share of
  downstream failures that acting on the contributor would reach is read through the process's recovery in two records,
  not apportioned by load. It is not writable against the nearest approved builds: task202 matched an input's physical
  state to a receiver's layers (no process switched off), task303 paired sibling events in one minute to find a shared
  upstream fault (no recovery window, no reach against magnitude), and task182's lineage read a running source's share
  at receptors.
- **Same-puzzle and library tests:** gap, pattern and decision type repeat only older lineage (task36 R1, task83 v1),
  differentiated; the golden is not a named correction (no textbook names "set a discharger's chamber log against a
  works' recovery"), and the field's methods for the deciding quantity, river source apportionment by mass balance and
  the works' process model, sit at rungs 0 and 1.
- **Layers:** Layer 1 is the company's own record-keeping: the dairy's chamber logger in clock time with logger gaps;
  the monitor in UTC with maintenance-visit flags and ratified then provisional releases; the works' historian with its
  effluent and oxygen tags renamed at the October 2025 works; the laboratory reporting composites one to three weeks
  after the round; automatic meter reads kept by meter point across two meter exchanges; an energy register that states
  its meters as they stand now. Layer 2 is the reachable share read through the works' recovery.
- **People** (`guard.py names --geo "United Kingdom, England" --seed 401`; Joanne O'Brien and Elliot Davies skipped,
  architecture 3's card holds them): Gerard Norris (environment programme manager, who owns the submission), Katy Hughes
  (trade effluent officer), Sylvia Phillips (Coldmere's process scientist); in the pack's own records Leonard James (the
  shutdown works record) and the samplers B. Hurst and J. Evans, from the same draw. The prompt names no one.
- **Furniture redrawn at registration:** task402's redraw took `capacity_planner` into the window, so the role family
  moved to `programme_officer`: the environment programme manager owns the submission the upgrade goes into, the honest
  owner of the call. Forum `regulator_or_inspector` (the Environment Agency's review of the submission), forcing event
  `statutory_or_regulatory_filing`, organisation family `utility_or_infrastructure`, context artifact `register` (the
  trade effluent consent register) and shape 12 all clear the window read off `guard.py check` on the registered card.
- **Sources:** synthetic throughout, built to the structure of the public records it imitates (the anchors below);
  every file's source, date and licence is recorded in `metadata.json` at stage 3.

### Physical anchors

- **The standard.** Good status for total ammonia (as N) in a lowland, high-alkalinity river is 0.6 mg/l as a 90th
  percentile (the Water Environment (Water Framework Directive) (England and Wales) Directions 2015, Schedule 3). The
  standard's percentile is not the graded metric: the company's own terms count an exceedance day as a UK day whose
  mean of valid fifteen-minute readings exceeds 0.6 mg/l, the way a continuous section 82 monitor (Environment Act 2021,
  inserting section 141DA into the Water Industry Act 1991) is read day by day.
- **The discharge.** Acid whey from strained yoghurt runs at about pH 4.2 to 4.6 and, like other whey, carries about
  50 to 80 g/l of COD (Rocha-Mendoza and others, J. Dairy Sci. 104, 2021, on acid whey; Carvalho, Prazeres and Rivas,
  Sci. Total Environ. 445-446, 2013, on whey wastewater). Each discharge in the generator is 17 to 31 m3 of whey at 55
  to 76 g/l (mean load 1,543 kg COD) run through the chamber with the evening's rinse water, 27 to 57 m3 in about an
  hour at pH 6.1 to 6.4 (part-neutralised by the alkaline wash water it meets in the drain).
- **After the sewer.** The discharge reaches the works in roughly an hour into about 390 m3 an hour of night inflow, a
  dilution of about one in eight to one in fifteen; at a domestic sewage alkalinity of 250 to 350 mg/l as CaCO3 the
  inlet pH barely moves, so the shock is not a pH shock and the historian carries no inlet pH. Its COD is a third to a
  half of the works' daily load (about 4,900 kg at 120 g a person a day) arriving in two hours, two to three times the
  oxygen demand the blowers meet at night: the blowers run flat out and the dissolved oxygen sits at 0.3 to 0.9 mg/l
  for five to eleven hours, below the nitrifiers' oxygen half-saturation range (Metcalf and Eddy, Wastewater
  Engineering, fifth edition, chapter 7), while the heterotrophs take the oxygen.
- **Recovery.** Nitrifiers starved of oxygen are not killed and recover within one to two days once the demand passes;
  in a winter at 7 to 10 degrees the works' effluent ammonia runs at 8 to 17 mg/l on the first day and about a third of
  that on the second (the generator's day two is 0.34 of day one), against 0.6 to 2 mg/l normally (the pack's slug-free
  daily maximum is 5.5, its mean 1.5); the river's dilution of six to ten turns the first day into an exceedance day and
  the second, nearly always, not.
- **The charges scheme.** The company's 2025-26 trade effluent charges scheme carries the Mogden formula, C = R + V +
  Bv + (Ot/Os) x B + (St/Ss) x S, in the form English undertakers' schemes use, with invented rates at published levels
  (Os 470 and Ss 330 mg/l); the ask executes the company's own scheme, filed in the pack.

### Go/no-go screens (on the generator's clean truth and the cut pack; `checks.py`, 20 redraws)

1. **Levels and the lever against the rivals' estimates.** At the anchors above the window holds 20 to 40 exceedance
   days across 20 redraws (35 on the shipped seed) against 4 the winter before; no slug-free day in either winter
   reaches 0.6 in any redraw (maximum 0.336), so the rivals (the control, the cold, rain, the storm tank, growth) reach
   no exceedance day.
2. **The golden's own method holds the call.** Every reach form (the first one to two, one to three, one to four, one to
   five and nought to three days; evening discharges with a flow floor or any low-pH night; episodes read from the
   works' effluent) files 35 of 35 on the pack and equals the window count in 20 of 20 redraws, so the graded reach is
   the same under every form and no window is filed.
3. **No easy completion.** The decisive variable (the days after an evening discharge) is not one the default path
   brings in: the dairy enters it only as a load and a compliance record, both normal. The process model books 34.6 of
   the 35 days to the aeration control and its flexible form 30.4; the oxygen sags that follow a discharge share their
   shape with the control's own night-load sags, and under half of any sag query's days are exceedance days.
4. **Literal execution.** The filed WHAT executed literally for every candidate lands wrong: mass balance at the monitor
   names the works; the works' process review on temperature, load and the dated control names the control; a dated
   before-and-after cannot part 27 October from 3 November and names the control; the dairy costed by its charging
   strength is about 2 per cent of the works' load. The golden needs the evening discharges, which the WHAT does not
   tell a solver to compute.

## Default path

1. Take the downstream monitor's valid fifteen-minute readings, form UK days and count the days above 0.6 mg/l: 35 from
   November 2025 to March 2026 against 4 a year earlier.
2. Apportion the downstream ammonia by mass balance with the gauged upstream flow and the works' flow (the field's river
   source apportionment): the works' effluent carries about 95 per cent of the load on the exceedance days, so the
   works is the source.
3. Model the works' final-effluent ammonia from its historian on wastewater temperature, the incoming load and the
   aeration control's go-live (the field's process review): the control's term carries 34.6 of the 35 days (30.4 in a
   flexible form with cold bands and interactions); since go-live the oxygen sags below 1 mg/l on many mornings with the
   blowers flat out, read as the control trimming the air and the aeration running out of capacity in the cold.
4. Check the trade dischargers by load and compliance: Thornlea's weekly composites (settled COD about 2,300 mg/l) and
   its pH log (6.1 to 10.3, inside the consent's 6 to 11) pass; an evening's discharge costed at the composite strength
   is about 100 kg of COD, 2 per cent of the works' daily load, so the dairy is dismissed; storm spills and upstream
   farming explain little.
- **Ends on:** the aeration control and the works' nitrification capacity in the cold; the GBP 14.2 million upgrade goes
  into the submission.
- **Golden:** Thornlea Dairy's evening whey discharges: all 35 of the winter's exceedance days fall on the first or second
  day after one in the dairy's own fifteen-minute record and none on load and cold alone, so the upgrade would reach none
  of them and stopping the discharges at the dairy would reach all 35.

## Stump sentence

A competent analyst apportions the Allery's ammonia to the works by mass balance, models the works' final-effluent
ammonia on temperature, load and the aeration control, costs Thornlea Dairy at its charging strength and books the
winter's exceedance days to the aeration control and nitrification capacity in the cold, ending on the GBP 14.2 million
upgrade, because they never set the dairy's fifteen-minute chamber record against the works' daily effluent and the
monitor's days, which puts all 35 exceedance days on the first or second day after an evening whey discharge.

## Three rules

- **Task type:** physical-environmental-sciences / pollution-source-attribution, which serves Root-Cause Analysis.
- **Domain test:** the deciding quantity is the share of the downstream exceedance days that fall inside the works'
  recovery after a trade discharger's oxygen-demand shock, worked as river source attribution through the works' process
  response, where the field's own estimates (mass balance at the monitor, the works' process model) apportion by load.
- **Swap:** "every Allery exceedance day follows a Thornlea whey evening within the works' recovery, so the upgrade would
  not stop them", rewritten as "every late delivery follows a supplier's short shipment", loses the dilution, the
  nitrifiers' oxygen starvation and recovery, and the consented strength that make the share computable, and stops
  reading.
- **Layer 1:** the dairy's chamber logger in clock time with gaps; the monitor in UTC with maintenance flags and
  ratified and provisional releases; the historian's tags renamed at the October works; composites reported weeks after
  the round; meter reads by meter point across exchanges; an energy register as it stands now. Each is produced by the
  system named; nothing is placed to be caught.
- **Layer 2:** estimand identification: the share each option reaches is the population of exceedance days inside the
  works' recovery after a discharge, built by joining three records, not the load each source sends.
- **Decisive step:** set Thornlea's fifteen-minute chamber record against the works' daily effluent and the monitor's
  days, mark the first and second day after each evening discharge, and read the exceedance days on and off them: every
  one is on them, none falls on load and cold alone, so the upgrade and the control reach none.
- **Not semantics:** every field reads plainly (pH units, m3 per fifteen minutes, mg/l as N, the monitor's flags, the
  consent's limits), and reading each correctly still leaves the mass balance on the works and the process model on the
  aeration control and the cold; no field, code or definition marks a discharge as a trigger of anything at the works.
- **Not rule application:** no filed rule or procedure links a discharger's chamber record to the works' failures (the
  consent's limits are met; charging rests on weekly composites that never hold a discharge evening), so executing every
  stated rule files the control. The enumerated family spreads from 0 of 35 days reached through the dairy (mass
  balance, the process model, the load costing) to 35 of 35 (the reach); the standing family, once the chamber record is
  in, is every reach form (one to five days, nought to three, evening or any night, with or without a flow floor,
  episodes in the works' effluent), all at 35 of 35 on the pack and equal in 20 of 20 redraws, so the graded figure
  carries no spread; the ruling-out is done by the records alone (no slug-free day reaches 0.6, maximum 0.336 over 20
  redraws) and nothing in the text announces it.
- **Analyst test:** a strong analyst with every field read and every rule applied apportions by mass balance to the
  works, models the works' effluent on temperature, load and the aeration control, dismisses the dairy at its charging
  strength, and ends on the aeration control and nitrification capacity, backing the GBP 14.2 million upgrade.
- **Estimand:** filed in the company's investigation terms (`coldmere_ammonia_investigation_terms.docx`): the population
  (every day from 1 November 2025 to 31 March 2026 at the downstream monitor), the outcome (a UK day whose mean of valid
  fifteen-minute readings exceeds 0.6 mg/l, flagged readings invalid, 72 readings at least), the unit (the monitor day),
  the comparison (the same months a year earlier) and the question each option answers (which exceedance days it would
  have prevented); no sentence names a discharge, a lag, a recovery window or a join.
- **No decoy:** nothing is planted: the aeration control's go-live, the new blower, the housing growth, the cold and the
  storm spills are real changes with their own records; no memo, draft, briefing or stakeholder figure argues for the
  upgrade or blames the control or the dairy.
- **No certified replay:** no certified or published figure is reproduced to recover a method; the golden's construction
  reproduces nothing in the pack.
- **Lesson:** a source's share of a failure is its reach through the process that fails, not its share of the load: a
  small discharger whose evening whey starves a works' nitrifiers owns the days the works needs to recover, and only its
  own high-frequency record set against the works' and the river's days shows it; no build on file teaches a process
  switched off by a minor contributor's discharges.

## Survivor anatomy

- **Actor:** the deciding property, which river days follow which of the dairy's evenings through the works' recovery,
  has no column in any file: the chamber record carries flow, pH and temperature with no event, alarm or status column,
  the monitor carries readings, the historian hours; the relation is a lag across three files that nothing stores.
- **Link:** the signal is read through a cross-file comparison the field's methods never ask for: a discharger's chamber
  record (clock time, fifteen minutes) against the monitor's days (UTC) through the works' daily effluent; no key joins
  a dairy evening to a river day and no clause names both sides.
- **Reflex:** the field's methods for the deciding quantity, mass balance at the monitor and the works' process model on
  temperature, load and the control, sit at rungs 0 and 1 and file the works and the control (34.6 of 35 days to the
  control).
- **Back-test:** the textbook route validates: the control's go-live precedes the jump from 4 days to 35, the oxygen
  sags below 1 mg/l on 96 days of the winter with the blowers flat out (33 of them exceedance days), and the dairy's
  composites and pH log pass every consent test.
- **Second use:** every file the decisive step reads sits in the pack for its own reason: the chamber record is the
  consent's condition 5 self-monitoring record, read by the default path for pH compliance; the historian is the works'
  process record, read by the process model; the monitor is the population. Delete the decisive step and all three stay.
- **Shock:** the discharges read as ordinary production: an evening hour at production flows and pH 6.1 to 6.4 inside the
  consent, beside night-time acid rinses at 6.35 to 6.65; the exceedance days spread over every weekday (none above three
  tenths, asserted); the morning-after oxygen sags share their shape with the control's night-load sags (asserted under
  four sag queries).
- **Pins:** the WHAT is filed in the company's investigation terms (the day, the standard, validity, the window, the
  comparison and the question each option answers); no filed sentence names a discharge, a lag, a recovery window, a
  join or the dairy's record, and deleting any filed sentence leaves the call forced by the records.

## Readability screen

The screen takes two readers: the strong generalist, and the reader who knows that a dairy's whey reaching a works
starves its nitrifiers of oxygen. Nothing in the pack says whey reached the sewer: the composites never cover an
evening discharge, the pH log stays inside the consent, the works' historian has no inlet pH or inhibition tag, and its
oxygen sags on the mornings after a discharge look like the control's own. The whey-aware reader must open the chamber
record, pick the evening discharges out of production and the night-time acid rinses on pH and flow, and carry each
through the works' recovery to the monitor's days: three moves from the text, not one query.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 mass balance at the monitor, the works as the source | the terms name the monitor and the standard | monitor, gauge and works flow columns | yes, the field's source apportionment | none | no | yes | no | readable |
| R1 the works' process model on temperature, load and the dated control | the terms date the control | historian columns | yes, the field's process review | none | no | yes | no | readable |
| R2 the flexible process model with cold bands and interactions | none | historian columns | yes | none | no | yes | no | readable |
| R3 the trade dischargers by load and consent compliance | the scheme and the consent conditions | composites and the chamber pH | yes | the consent's limits | no | yes | no | readable |
| R4 for the generalist: each evening discharge set against the monitor's days through the works' effluent (decisive) | no sentence names a discharge, a lag or a join | no column marks a discharge; pH stays in consent; acid rinses are its twins | no: the field's methods apportion by load | no control scores it | no: the battery converts clocks and dedupes, it does not pair a night with a river day | no: a selection, a lag and a count across three files | no: the chamber record is the consent's self-monitoring return, read by R3 | silent |
| R4 for the whey-aware reader (decisive) | no: nothing says whey reached the sewer, the composites never hold a discharge evening | no: an evening hour at production flows and pH 6.1 to 6.4, beside the acid rinses | not from the text: the reflex fires only after the chamber record is opened, the evenings picked out and carried through the works' recovery | none | no | no | no | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives and the call under each | Ruled out by |
|---|---|---|---|---|
| SF1 | a reading flagged at a maintenance visit | invalid (the terms) | counted: the same 35 and 4 days | same call, asserted on both winters |
| SF2 | "above 0.6 mg/l" for a day | the day's mean strictly above | at or above; a share of readings above | same call: no day mean within 0.07 of the standard, asserted |
| SF3 | a day with missing readings | counted with 72 or more valid readings | any readings | same call: every day carries 72 or more, asserted |
| SF4 | the days a discharge reaches | the first or second day after it | one to three, four or five days; nought to three; any low-pH night; episodes in the works' effluent | same call: 35 of 35 under every form, every form equal in 20 of 20 redraws, asserted |
| SF5 | the monitor day | midnight to midnight UK time (the terms) | UTC days as the file stamps them | same call: the same days in both winters, asserted |
| SF6 | this winter | 1 November 2025 to 31 March 2026 (the terms) | December to February; October to March | same call: every exceedance day reached under both, asserted |
| SF7 | the comparison | the same months a year earlier (the terms) | the whole previous October to March | same call: 35 against 4, asserted |
| SF8 | the candidates | the terms' four options | the cold, storm spills, upstream farming, growth | same call: no exceedance day in either winter lacks a discharge on the two evenings before it, asserted |
| SF9 | a composite that fills a second bottle (the ask) | the two bottles together, one composite | each bottle counted as its own composite: every one of the ten strengths moves by 10 bins or more | the scheme, section 4: "the two bottles together are the composite sample" |
| SF10 | the strength of a two-bottle composite (the ask) | the strength of the effluent it holds, the bottles weighted by the volumes the samplers log | a plain mean of the two bottles: every strength moves by 4 bins or more | the scheme, section 4: "The strength of a composite sample is the strength of the effluent it holds" |
| SF11 | the second bottle (the ask) | part of the composite | dropped, the first bottle taken as the composite: every strength moves by 3 bins or more | the scheme, section 4: "the two bottles together are the composite sample" |

## Ladder

- **R0, the count:** 35 exceedance days from November 2025 to March 2026 (10, 6, 6, 3, 10 by month) against 4 a year
  earlier (1, 1, 1, 1, 0); every reader reaches it, and it is graded.
- **R1, mass balance:** the works' effluent carries about 95 per cent of the downstream load on the exceedance days:
  the works.
- **R2, the process model:** the control's go-live carries 34.6 of the 35 days, 30.4 in the flexible form: the aeration
  control, with the capacity story behind it (blowers flat out on the sag mornings).
- **R3, the dairy by load:** an evening's discharge at the composite strength is about 100 kg of COD against about 4,900
  a day at the works: dismissed, back to the control and the upgrade.
- **R4, the reach (decisive):** all 35 exceedance days fall on the first or second day after an evening discharge in the
  chamber record; on the other days the works runs at 1.5 mg/l and the river never reaches 0.6; the upgrade and the
  control reach none, the dairy all 35. The prior winter's 4 days follow the old line's occasional losses the same way.
- **The graded main-call figures:** the monthly exceedance days of both winters, the 35 the dairy's whey reaches and the
  0 the upgrade reaches; each is the same under every SF row and every reach form.

## Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | every day 1 November 2025 to 31 March 2026 at the downstream monitor | filed in the terms; C1, none excluded |
| 2 Unit of account | the monitor day; for the asks each discharger and each calendar month | the terms and the asking sentence |
| 3 Attribution window | the days after a discharge a reach counts | C1: every form files 35 of 35 (SF4) |
| 4 As-of dating | ratified readings to 31 December 2025, provisional after; the pack exported 19 October 2026 | the terms; one status per reading, C1 |
| 5 Version basis | the meter reads span two meters at two sites | the reads file carries each exchange's final and initial reads as facts |
| 6 Denominator | no rate is graded; the reach is a count of days | C1 |
| 7 Weighting | strengths are arithmetic means over composites; a composite's strength is that of the effluent it holds | filed in the charges scheme (SF9 to SF11) |
| 8 Window length | the winter and its comparison | filed in the terms; SF6 and SF7 same call |
| 9 Boundary inclusivity | "above 0.6" | C1: no day mean within 0.07 (SF2) |
| 10 Rounding path | counts are whole; asks round once at the end | the asking sentence; every graded figure mid-bin, asserted |
| 11 Tie-break | none arises | C1 |
| 12 Maturity and censoring | a discharge on the last evenings of March reaches past the window | C1: every window exceedance day has both preceding evenings in the record |
| 13 Order of operations | daily mean then threshold; volume times multiplier times allowance | filed; the volume terms commute |
| 14 Row order | none matters | C1 |
| 15 Duplicate resolution | the exchange's two reads on one day are two meters, not a duplicate | Ask A's device, ruled by the read type |
| 16 Identity normalisation | the historian's renamed tags; the bottler's two customer codes on one sampling point | the columns join by time; the consent names the sampling point |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | mg/l as N; mg/l for the strengths; register units times the consent's multiplier for m3 | units in the data and the consents |
| 19 Code and status semantics | the monitor's M flag; read types; data status | the terms (SF1); never the stump |
| 20 Integerisation | days are whole | C1 |
| 21 Clause scope | the day definition covers both winters; the charges scheme covers 2025-26 | filed scope |
| 22 Forward window contents | the call faces the submission and the winters ahead; no forward figure is graded | the recorded winter carries the evidence; the dairy's line runs on |

## Literal reader

The terms executed word for word for each candidate (`coldmere_ammonia_investigation_terms.docx`, sections 2 and 3):
the exceedance days are fixed (35 and 4; SF1 to SF7 converge), and "which exceedance days each option would have
prevented" is executed as each reader's route executes it:

- **Mass balance at the monitor:** the works carries the load on every exceedance day; the upgrade is the works' option.
  Lands on the upgrade.
- **The works' process review:** temperature, load and the dated control; the control's term carries 34.6 of 35 days.
  Lands on the control.
- **A dated before-and-after with every option's own date:** the control (27 October), the new line (3 November) and
  the growth by month all precede the first exceedance day; daily data a week apart cannot part them. Lands on the
  control.
- **The reader who sees the evening excursions and costs the dairy by load:** the chamber record's evening hours at pH
  6.1 to 6.4 are seen, each costed at the composite's settled COD of about 2,300 mg/l: about 42 m3 an evening, about 100
  kg of COD, 2 per cent of the works' daily load, inside every consent limit. Lands on the control and the upgrade.
- **The reach (the golden):** the evening discharges in the chamber record, carried one or two days through the works'
  recovery, reach all 35 exceedance days and nothing else reaches one (SF8). Lands on the dairy.
- **The ask's literal executor**, every field at face value: the charges scheme's sentences on the consent's meter
  point, multiplier and allowance, every read the reads file holds for that point (the exchange reads included), and
  each composite collected in the charging year taken as the bottles one round collected at the consented point (the
  round sheet's bottle number matched to the samplers' download log's), at the strength of the effluent they hold: it
  reproduces all fifteen figures (asserted in `checks.py`, rebuilt from the filed fields alone). No golden figure
  overrides a field.

## Oracles

No shipped artifact ranks the options, states a share, a lag or a reach, or names the dairy as a suspect. The composites
and the consent's pH condition pass for the dairy (asserted), the chamber record has no alarm or status column, and the
historian's oxygen sags are no one-query signal (under half of the days in any of four sag queries are exceedance days,
asserted). The prior winter's 4 days follow the old line's losses the same way, which a reader can use as a check only
after making the join. On the ask, no control ties only under the golden: the reads file's quarterly reads agree with the
differenced route as well as the walked one, the round sheets and the laboratory agree bottle for bottle under every
reading, and the samplers' download log records volumes, not strengths or a total.

## Ask sheet

- **Ask A, each trade discharger's chargeable volume (m3) and its settled COD and suspended solids strengths (mg/l) for
  2025-26** (15 figures, whole units). H18: the trade effluent the works receives, by volume and strength, is what the
  charging system holds against its load; the call does not turn on it. Files: the charges scheme (PDF), the consents
  register (XLSX), the automatic meter reads, the sampling round sheets, the samplers' download log and the laboratory's
  results (CSV). The blowers' electricity was dropped (`## Tried and rejected`); the energy files stay as distractors.
- **Primary P1 (D2, a state walked through its log; its block the brewery's and the meat plant's volumes):** both had
  their meters exchanged inside the year (14 August and 3 December 2025) and the fitted meters' registers were not set
  back, so each meter point's 1 April reads span two meters; the reads file carries the removed meter's final read and
  the fitted meter's initial read beside the quarterly reads, and differencing the 1 April reads adds 2,516 and 3,804 m3
  before the allowance.
- **Primary P2 (D6, an allocation whose weight is recorded; its block all ten strengths, disjoint from P1's):** each
  site's sampler is flow-proportional, and on a high-flow day it fills its 2.5-litre bottle and runs on into a second,
  which fills over the night on weaker effluent (16 to 27 second bottles a site over the record). The sampler collects
  each bottle under its own label and the laboratory analyses each one; the round sheet carries each bottle's number, and
  the bottle volumes sit only in the samplers' download log (point, run start and end, bottle, aliquots, volume). The
  scheme files the unit and the strength as WHAT ("the two bottles together are the composite sample"; "The strength of
  a composite sample is the strength of the effluent it holds") and states no handling. Each composite's strength is the
  volume-weighted mix of its bottles. The three wrong readings each move every one of the ten strengths: each bottle as
  its own composite by 10 to 247 bins, a plain mean of the two bottles by 4 to 143, the second bottle dropped by 3 to 93
  (asserted, SF9 to SF11). The join is unique at face value: one run per point per round, no logged run overlapping
  another at the same point, every bottle on the round sheets in the log and the reverse (asserted).
- **Hazards, priced as caught:** results dated by report against the round's collection (D8); the bottler's earlier
  customer code on the same sampling point; the laundry's ten-unit register (the consent's multiplier); settled against
  total COD; the allowance.
- **Pin test:** the asking sentence names the volume, the two strengths, the charging year and the units; the devices sit
  in which meter recorded which part of the year and how much of each bottle a composite holds.
- **Main population zero-counts:** no ask file is read by the main call; the dairy's meter, composites and sampler runs
  are rows outside the call's population (the monitor days, the historian's effluent, the chamber record); no composite
  covers a discharge evening (the strained line stands on Wednesdays, asserted).

| Ask | Cracker | Full includer, plain mean | Full includer, volume-weighted | No repair | Mirror | Cracker verdict |
|---|---|---|---|---|---|---|
| A trade effluent | 3 of 15 | 5 of 15 | 15 of 15 | 2 of 15 | 3 of 15 | miss |

- Measured on the cut pack: the cracker (the 1 April reads, the consent's multiplier and allowance, results at the
  consented point by the laboratory's date, each bottle a composite) keeps the three unexchanged volumes; the full
  includer (every file read, every stated fact acted on: the exchange reads walked, composites dated by collection, the
  bottles of a round taken as one composite) keeps 5 of 15 when it combines a composite's bottles by a plain mean and 15
  of 15 when it weights them by the logged volumes; the no-repair reader keeps 2; the mirror handles the ask as the
  cracker does.
- Pairs (38 + 7 + 55 x share on the call, 5 + 7 + 55 x share off it): the cracker on and the mirror off, 39.5; with the
  plain-mean full includer, both on the call 59.7, one on and one off 43.2; with the volume-weighting full includer, both
  on the call 78.0, one on and one off 61.5.
- Pair ceiling: 39.5 (cracker on the call 56.0, mirror off it 23.0).
- Mirror leakage: 20.0 per cent of ask weight.
- Measured by: generator/ceiling.py on the cut pack.

## Tried and rejected

- 2026-11-03, the seed's world (RC07, a supplier's January imbalance bill against plant trips and low wind), every
  candidate screened before the card. The trips' effect on the supplier's own imbalance volume at the system price is
  settlement accounting: each unit's metered shortfall against its notified output in the window before the desk can
  re-trade, priced per settlement period, reconciles exactly to the bill, so nothing is left to decide (rule
  application). The price the supplier would have faced without its own units' trips re-runs the system's price
  formation on the changed path, task398's spent insight in other nouns. Netting the desk's replacement trades out of a
  trip's cost is the same insight again (the cause owns the response it triggered). Which settlement periods a trip owns
  (gate closure, the share of an interval) is a market rule or a time-semantics read, banned as decisive. The cost
  spike's drivers identified from interval data need a driver the settlement data does not meter, and in this market
  every driver is metered. Dual imbalance pricing makes the portfolio's net position matter, but executing the price
  rule on the with-and-without positions is rule application. The honest strategy, `decomposition_attribution`, and the
  seed's forum (the board) are both held by task398 in the window. Moved, per `CLAUDE.md`.
- 2026-11-03, other moves screened and set aside before this draw: gas turbine inlet icing in freezing fog read against
  temperature (the winter measures on the table name the mechanism, so a reader checks each one's conditions and lands
  it; two cheap routes); a groundwater nitrate rise read against travel time through the unsaturated zone (task202's
  reach-the-receptor insight in other nouns, and the field's first move); a bathing water's sources separated by marker
  decay in transit (task202's reach and task248's transit loss); selective in-migration behind a widening mortality gap
  (task68's entrants and task134 v2's newcomers, and the prior-diagnosis read lands the decision without it); depletion
  of the frail by a winter's deaths before an intervention's evaluation (dead on lever at realistic excess mortality, as
  task173's screens found for mortality displacement, and its frailty proxy forks the expectation); the Will Rogers
  stage migration (the field's stage-specific comparison collapses into which stage field to read, data semantics);
  attenuation by a mediator's or a predictor's unreliability (task262's insight); regression dilution of a risk factor
  in a disparity decomposition (task262 again); a funnel's downstream rate falling when an upstream filter loosened (the
  end-to-end funnel is the field's reflex); a two-stage complaint escalation's selection (the per-complaint view lands it);
  a mode or non-response shift in a satisfaction tracker (task121 v4's linkage and halo).
- 2026-11-03, prototypes before the card (`scratchpad/t401/proto1.py` to `proto3.py`, expected values with Poisson draws):
  winter-only counts in a city of 600,000 left the default and the golden overlapping across draws (default 5th to 95th
  percentile 23 to 179, golden -38 to 119), so the build runs at integrated-care-system scale over October-to-September
  years with the closures in the year between the baseline and the pilot; there the default's expectation is 912 (spread
  208) against a golden of 392 (spread 215, truth 389), and the trend-adjusted golden forms agree within a median of 6.4
  admissions once the framework files the comparison; without the comparison filed, the no-trend form differs from them
  by a median of 77 (a fork the framework's comparison sentence closes, a WHAT naming no method).
- 2026-11-03, architecture 1 dies at stage 2 on the coordinator's realism check, before any data was cut. Set to published
  English levels (a care home resident aged 80 and over about 0.70 to 0.75 emergency admissions a year, community
  residents by band 0.24 to 0.58, a same-age ratio near two, not the prototype's five), the composition lever is about
  113 admissions for the 440 Core20 residents the closures moved (sd 26), against draw-to-draw spreads of 202 in the
  default and 214 in the golden on a one-year baseline and about 160 on three years (`scratchpad/t401/proto4.py`, 400
  draws). A bar at the midpoint separates default above from golden below in 22 per cent of draws (27 on three years);
  900 residents moved gives 41 to 51 per cent and 1,400 gives 58 to 72, and 1,400 is two fifths of Core20's care home
  places in one system closing in a year, which no honest care group failure produces. A larger 80 and over population
  scales the spread with the lever, and a bar nearer the truth only moves the coin flip. The stump was the noise. Re-rooted.
- 2026-11-03, the redraw's other candidates, set aside before the card: regression to the mean of units chosen on a
  noisy outcome (task130 v3 landed it; task149 and task174 rejected it on that lineage); a satisfaction fall read against
  the conditions each respondent met, or a tracker's mode or response shift (task121 v4); a storable good's purchases
  pulled forward before an announced price rise and paid back after (the pre-rise spike is the pack's largest movement
  and announces the step); a distributor's orders falling as channel stock is drawn down (sell-through is the field's
  reflex and lands it); a local policy confounded by a common shock loading on each unit's exposure (the council
  furniture is banned in the window and the exposure needs data no operator holds); transformer insulation ageing under
  new loads (electricity is spent, task129, task196, task201, task303, and F6's 46 already holds a rate stationary in a
  constructed exposure); in the crop world itself, a hybrid placed on clubroot or hail-struck fields (a lab result or an
  adjuster's claim names the field, readable), and a hybrid whose own later flowering met the heat (`crop2.py`: a three-day
  shift moves the season-long panel only 3 to 5 per cent, and the forward step then needs a climatology fork).
- 2026-11-03, prototypes for architecture 2 (`scratchpad/t401/crop1.py`, `crop3.py`, ten weather draws each, the
  hybrid's own effect nil and equal phenology): with most of the hybrid's seed late by 8 to 14 days, the season-long
  panel files minus 9.1 per cent (sd 9.8 across weather draws), farm-by-year effects minus 9.3, a linear seeding-date term
  minus 7.0, raw 2026 means minus 11.6, the flowering-window exposure minus 0.1 (sd 0.9), its variants (thresholds 28 and
  31 C, windows 14 and 22 days, 490 and 550 heat units to flower) minus 3.5 to plus 0.5, and fields seeded on the same
  days on the same farm minus 0.6 (the same insight by matching). The spread across draws is the weather's: the pack's
  July heat wave and seed delay are set by design, never picked from draws.
- 2026-11-03, architecture 2 dies at stage 2 on its own ladder (`generator/ladder.py`, seed 4012026, measured at commit
  7d3a3cd), before any data was cut. First, the golden's own method forks the main call: the flowering-window variants
  land +2.1 (28 C), -2.5 (31 C), -12.0 (a 14-day window), +3.4 (a 22-day window), -8.2 (490 heat units to flower) and
  +4.9 (550 units) against the 5 per cent bar, so two agronomically defensible variants drop the hybrid and four keep
  it; filing the window or the heat metric would name the decisive step, and the generator cannot close the spread under
  realistic catch-up (a 17-day seeding gap became a 6-day flowering gap). Second, the stump rests on a functional-form
  choice: the default path's own rung 4 already rebuilds seeding dates from the seeder's logs, and every flexible form of
  that variable then lands the golden (seeding-week bins +3.6, a cubic +4.4, same-day matching +9.3); only a linear term
  stays wrong (-10.1 in the season panel, -8.3 with farm-by-year effects), so Gate F would rest on the solver choosing a
  straight line. Spent; one architecture per world, so the crop and weather world is closed to this slot. Re-rooted at
  architecture 3 in another client domain, world and dataset.
- 2026-11-03, architecture 3's draw, candidates set aside before the card. In the never-built satisfaction cell, the
  client card's moves (Shapley shares, a Net Promoter change's multinomial error, penalty against reward, loyalty read
  on later behaviour) are reflexes, and reading a fall on the conditions each response was made under is task121 v4's.
  A broadband provider's speed promise against delivered speed died on the regulator's own reflex (the share of plan
  speed delivered is the standard metric). The energy quote mechanism in the supplier's base-wide relationship tracker
  carried 0.54 points (1.35 with 2025's joiners using a fifth more) against a fall whose draw-to-draw spread is 0.66
  (`scratchpad/t401/a3/proto_e2.py`), architecture 1's death in other nouns, so the build runs on the six-month
  new-customer tracker. In the concentrated form a first harness with the platform's own effect at 1.3 points left the
  golden's 10 and 20 per cent flags (0.98, 1.78) under the residual (`proto_e3.py`); at the platform's realistic small
  effect the standing forms clear it (`proto_e4.py`). Other cells screened: education multilevel (the client's three
  cards are reflexes; teacher reassignment and special-needs assessment waits fail screen 1 or repeat the actor family),
  health equity (an inhaler switch run practice by practice is task400's staggered rollout; discharge after a missed
  appointment repeats task402's broken-off cases), pollution source attribution (every wind, tide and capture-zone route
  is task202's reach), water network reliability (the isolation extent per burst is one group-by; transients read
  through topology sit beside task303), the human factors cells (the pairing is barred against task400), and
  interpretability (ruled a backdrop at task129 v1).
- 2026-11-03, stage 2 on architecture 3, three cuts. (a) The first world set the first Direct Debit from the quote, so
  the review rise was a near-copy of the gap and a solver asking why payments rose walked to the quote; the payment is
  now set from the meter point's industry quantity at registration, and the Direct Debit change books 0.35 points and
  names the platform (`## Ladder`, R2b). (b) A Direct Debit policy document stating that rule was drafted and dropped:
  its sentence on industry quantities would send a reader to set quotes against quantities, and the golden never needs
  it. (c) The contact centre ask and its two call logs were cut for budget; the contact rival stays on the tracker's own
  contact question. The asks' first devices as drafted (stale legacy status, re-runs keyed on the legacy reference,
  withdrawals) were each executable from the cutover plan's and the asking sentences' own pins, so they were re-sited
  onto an erroneous-transfer return, a reload chain with a pilot twin, and a gas registration raised under its own
  reference.
- 2026-11-03, stage 2 on architecture 3, the full includer (precut FAIL: one primary per ask). The coordinator's candidates
  were screened against the full includer: (a) Ask B, an account whose gas was removed between its first load and its
  reload: the full includer that walks the chain takes the last load's row, fuels with its week, and keeps the block, and
  the sentence that closes the fork (the fuels that load carried) makes it a work order; (b) Ask C, broker switches
  registered on the broker's lead reference: noticing the unmatched reference and joining on the prospect is one act, and
  every quote under a broker's lead is a broker quote, so nothing goes wrong after the notice; re-sited onto a broker sale
  re-quoted by the phone team after the registration; (c) Ask A, two-rate registers alone: a work order once the plan
  files day and night together; the device is the register set changing at an exchange, and gas has no register. Also set
  aside: split-fuel legacy accounts merged on load (one platform number on two rows, and the filed unit, the account the
  platform holds, makes it a work order); a requested supply start on legacy sales (the industry registration date in the
  quantities fixes it in one act); fuel add-ons across the migration renumbering (the solver who landed the call already
  built the crosswalk).
- 2026-11-03, stage 2, the full includer at 36 of 58 (62 per cent of the ask weight, 79.1 on the call): one second device
  per ask on its own block left a full includer and an on-call cracker pairing near 62. Widened: Ask A gained a change of
  occupier on the same meter points (the primary's own repair keeps the leaving account), Ask B's returned accounts take
  both fuels, Ask C's re-quotes reach every channel; the full includer keeps none of the 58.
- 2026-11-03, stage 4 round 1 (judge NOT_DETERMINISTIC and SOLUTION_WRONG, SEND_BACK light on the workbook asks alone, main
  call forced, Gates G and H passing; reader clean on the main call): Ask B's second device, the 410 accounts loaded and
  returned to the legacy platform, died to its own WHAT. Filing what counts as moved (the new platform billing the account
  at the end of 2 November 2025) closed the judge's fork 1 and made the returns a work order: with the sentence filed and
  nothing else changed, the full includer keeps 16 of 18 Ask B figures (`scratchpad/t401/fix/remeasure_b.py`). The returns
  stay as a hazard; the second device is re-sited onto 389 accounts the legacy platform took back during 2026 on a change
  to prepayment, where the repair the sentence invites is right before the close and wrong after it (the full includer
  keeps 0 of 18).
- 2026-11-03, stage 4 round 1, the Gate A anomaly: the change-of-occupier branch drew the leaving account's supply start
  without reference to its closure, so two Closed accounts began after they closed and took their meter points from the
  live occupiers (Eastern and London one account short under the golden's own rule). The leaving account's start now
  precedes its closure, asserted over every account. Fork 3 was closed by "no withdrawn registration counted" rather than
  by dating the boundary in the asking sentence (shorter, and true whatever the date), with every withdrawal now dated
  before the start it requested, as switching allows.
- 2026-11-03, stage 4 round 2, architecture 3 spent. The round-2 judge returned NOT_DETERMINISTIC, SEND_BACK (narrow), on
  the switches table: "credited to the sale it was registered on", read word for word, takes each registration's
  quote_ref, and 596 Phone registrations name a quote dated 2 to 10 days after the registration; the golden moves each to
  the prospect's latest quote on or before it, a rule no file states, and for 94 of those prospects latest against
  earliest moves about 20 cells. The literal ask executor in checks.py had carried the re-attribution as though it were
  the field's own value, so it never saw the fork. Every round-1 finding closed, and the main call held in both rounds
  (forced and reproduced; Gate F good; Gate G analytical_non_defect; Gate H analytical), but the judge noted that
  Critical Component 2's "more than half" depends on the cut (a binary covered split puts 14 per cent of the fall on the
  quote mix, five bands 60, eight bands 85, the kinked model 75). A second round without APPROVE spends the architecture
  under the round-1 ruling; the slot re-roots at architecture 4 in another domain, world, dataset and shell. Lessons: a
  literal executor takes every field at its face value, so a golden that overrides a field's own link (a reference, a
  date, a status) carries a filed WHAT or the data are regenerated so the face value is the golden; and every quantity
  the write-up states for the main call holds at every natural granularity of the comparison, or is stated so it does.
- 2026-11-03, architecture 4's draw, candidates set aside before the card (four go/no-go screens, `scratchpad/t401/a4/`).
  The strategy window (binding_constraint, causal_design and decomposition_attribution held by task399, task400 and
  task402) bars the natural attribution labels, so each candidate's decisive move was labelled before it was priced.
  (a) An online retailer's checkout conversion fall booked to a checkout release, caused by a collection partner
  withdrawing urban points while adding as many in suburbs (`proto1.py`, `proto2.py`, 20 redraws): it fails screens 2
  and 3, since the access effect acts only on latent collection-preferring shoppers through a continuous distance, so its
  share runs 0.84 to 2.50 points across defensible exposure forms and the release's residual -0.62 to 2.67, and it fails
  the swap test (collection points read the same as clinics); it also sits beside task129's surroundings exposure and
  task399 v3's supply behind a journey, and task177 had called a nearest-locker reading a replay. (b) Opportunity to
  learn in a primary trust's mid-year maths tests, a new scheme's sequence placing tested topics after the test date:
  an intrinsic fork, because the scheme's sequencing is itself a counterfactual cause of the measured spring fall, so
  the default's "the scheme" and the golden's "the sequence against the test date" name one candidate. (c) A school
  trust's illness absence driven by classroom ventilation cut to save energy: at published levels (about 0.5 to 0.9
  points of absence per 1,000 ppm) the lever is a fifth to a half of the rise. (d) Deploy-spanning journeys breaking
  in-flight checkouts: task129 v1 spent the first-use-after-a-version-change shape. (e) Split shipments across
  fulfilment centres: task175's seed and task277's reflex. (f) Tampered HGVs read from roadside remote sensing: task202
  screened it. (g) Storm overflows against the load apportionment model: the overflow record is the zeitgeist's first
  check, and the move is attribution. (h) A charity upgrade appeal's anchored figure, a norm boomerang and a goal
  difficulty gap: the levels are not documented, or the gap is architecture 3's family. (i) Composition designs in
  every cell: this slot has spent two (architecture 1's closures, architecture 3's mix standardisation).
- 2026-11-03, architecture 4, stage 2: the caustic clean-in-place excursion drawn at the card (pH above 11 for twenty
  to forty minutes) breaches the consent's "pH of any sample ... not more than 11" in the dairy's own record, so a
  careful reader catches a breach by reading a condition (rule 3, a field reading deciding). Redrawn to acid whey run
  to the drain on evenings after a missed collection: an oxygen-demand shock at pH 6.1 to 6.4, inside the consent.
- 2026-11-03, stage 2: whey evenings on Thursday to Sunday only put every exceedance day on Friday to Tuesday, a weekly
  hole one tabulation finds. Spread to every evening but Wednesday's (the composite's night); no weekday now holds
  above three tenths of the days.
- 2026-11-03, stage 2: the morning-after oxygen sag alone in the historian (0.05 to 0.35 mg/l with the blowers flat
  out) marked the shock days at the works in one query. Given twins of the same shape (the control's night-load sags
  after go-live, storm flushes before), so under half of the days in any of four sag queries are exceedance days.
- 2026-11-03, stage 2: the dairy's pH drawn as a clipped normal piled readings at the clip (6.60) and its gamma
  replacement reached 11.9, a visible breach. Replaced by a smooth distribution held under 10.3.
- 2026-11-03, stage 2, asks: homes connected per quarter (flats behind one lateral) is a device whose discovery is its
  remedy (the addressing register lists the homes), and no second device of another family stood on it without a filed
  sentence naming it, so the full includer kept 12 of 12. Dropped with the inspection record and the addressing
  register. The first trade effluent set handed the cracker both devices (a meter register listing each exchange with
  its final and initial reads beside the multiplier it opens the file for; the scheme's "dated by its collection"), and
  suspended solids moved under one bin for three dischargers. The multiplier moved to the consent's metering columns,
  the exchange reads into the reads file, the dating left to the WHAT ("collected in the charging year"), solids
  ungraded. The first energy set named TB1 on MCC 7 in the meters sheet, handing the new blower to the cracker; the
  board is now listed without its load and the shutdown works record names it.
- 2026-11-03, stage 2, the coordinator's ruling on the first rebuilt ask layer: the blowers' transformer change shared
  its file and its question with the new blower's board (a reader opening the shutdown record for MCC 7 reads both rows),
  was marked on the reads sheet (a site read and an "as at" note), was fixed by one swapped multiplier, and sat in D2
  with the trade effluent exchange; the full includer kept 18 of 18. The report date against the collection date was
  caught too (the scheme's emptying sentence pointed at the round sheets, the laboratory column is honestly named and the
  label is the join): 15 of 15. The blowers' electricity was dropped: every fact its golden needed had to be stated, and
  once stated its fix was a swap. The ask now carries one primary per family, P1 the exchanges (D2) and P2 the
  two-bottle composites weighted by the samplers' logged volumes (D6); charges came out because they sit in both blocks.
- 2026-11-03, stage 2: two-bottle composites at one week in ten moved three strengths under one bin (the laundry's and
  the bottler's suspended solids under a plain mean, three under the second bottle dropped). Raised to about a third of
  weeks with the night bottle at 45 to 65 per cent of the day's strength; every wrong reading now moves every strength by
  3 bins or more.
- 2026-11-04, architecture 4 spent at stage 4, round 1: the judge's blind derivation reached the call and every ask
  figure. Every free gate had passed, precut was clean, the leak reader found no decisive-step sentence, and the judge
  returned DETERMINISTIC with a wording FIX_NOW and Gate F "moderate to good"; but its derivation, written before it
  opened the graded blocks, landed the call and all 15 ask figures in 26 tool calls. The works' hourly final-effluent
  ammonia jumped to 10 to 17 mg/l from midnight on every failure day (against 0.7 to 1.0), the spikes aligned one to one
  with the discharger's evening pH dips in its own fifteen-minute monitor file (a file the pack carried for that
  discharger alone; 38 of 38 such evenings were followed by a failure day), and the prompt's chart sentence ("tracing the
  winter's exceedance days from the river down through the works to whatever sets them off") announced the trace. The ask
  fell the same way: the scheme's filed WHAT ("the strength of a composite sample is the strength of the effluent it
  holds") beside the sampler log's volume column made volume-weighting the bottles the obvious move. The deeper cause: a
  graded count that holds under every operationalisation needed a clean, short, visible alignment, which is exactly what
  one look finds, so the stump sat in finding the signal and determinism and difficulty pulled against each other.
  Lessons carried to architecture 5: the first-look reader (the outcome at its finest grain beside every candidate's own
  record, aligned by date and lag, plus a before-and-after on each dated change) is coded and must land the wrong call;
  every candidate's evidence sits in records all candidates share at one grain; the prompt names the WHAT, never the
  route; a filed WHAT never names the property its ask's remedy needs while the column that supplies it ships.
- 2026-11-04, architecture 5's draw, cells and candidates set aside before the card (screens in `scratchpad/t401/a5/`).
  Cells: workload-fatigue-shift-analysis is barred by `ban.pairing` against task400 (human factors on root-cause);
  funnel-journey-analysis registered to task403 at 01:15Z the same day (shape 09, `executive_team`, `product_manager`, a
  price change booked for a subscription conversion fall), so it, those axes and any price-change rival are kept clear
  of; interpretability (directly or through the nonprofit and audit house domains) reads as a backdrop on every world
  tried. Mechanisms screened on paper, each with its reason: an age-matched comparison against units' life-cycle curves
  (the pre-trend check and unit trends are reflexes); a remedy targeted at members already lapsing (confounding by
  indication is a reflex once the targeting is read); a change's harm reaching the comparison units through shared
  demand (task500 v2's spillover through a link); a timetable change breaking members' habitual slots (architecture 2's
  dated shock meeting each unit's own phase); a detector's precision falling with prevalence (the swap test fails);
  separating two same-day changes by a dose rebuilt from records (task129 v1 and task129's surroundings); an
  instructor's departure breaking classes (task402 v1's lapsed actor); a consumable's stock running out unit by unit
  (task50's rotation); members leaving at a contract's end (a column); a reward's withdrawal read on the dose alone (the
  dose test lands it whenever its cancellations fall inside the window).
- 2026-11-04, architecture 5's prototypes (`proto1.py` to `proto4.py`, `screens.py`, 20 redraws each): a permanent visit
  loss after the Rewards closure kept producing lapses after the cut, which no snapshot can count (the golden reached a
  third of the truth); with the closure in January its lapsed members were harvested by the February letter, so its
  in-window effect was 550 of 870 and the two causes tangled; with disjoint reaches and a 1 March cut the golden's figure
  moved with the inactivity rule (an eight-week rule cannot see five-week-old lapses), closed by the contract's 28-day
  active-member definition; a Direct Debit notification to every member put part of the letter's spike inside the
  closure's own reach, so the mixed extrapolation landed on the closure in 15 of 20; the legacy terms letter (legacy
  members only, price unchanged) restored every screen. The price rise first used for the letter was dropped for task403's
  price-change rival in the same wave.
