# task400 design note

Architecture 1, drawn 2026-11-03 (wave 7, Root-Cause lane), numbered from seed RC06 (an area control centre's summer
of tripled en-route delay). The seed's world could not carry an honest unbanned draw (`## Tried and rejected`, first
line), so the build moved to another client domain, world and dataset under the same objective and number (CLAUDE.md,
a stuck build is unblocked). Kept from the seed: the decision kind (a body adopts one account of a tripled operational
outcome and corrective action follows from it) and the kernel (part of the rise is self-inflicted by a change made with
good intentions, while every recorded code is correct). The mechanism was redesigned at stage 2, before any data was
cut, on the coordinator's review (`## Tried and rejected`, third line; `## Draw`, the three points).

Ternhallow Iron Ore runs the Mount Bracken open-pit iron ore mine in the Pilbara region of Western Australia. Its haul
trucks carry collision avoidance units that warn the operator when a tagged vehicle comes close, first with a warning
alert and then, closer in, a critical alert; light vehicles carry tags. Vehicle interaction incidents rose from 24 in
July to October 2025 to 89 in July to October 2026, the rise starting in June 2026. Three things changed that month:
stage 3 of the north pit opened on 1 June and put more trucks on the North waste route through the North ramp
junction, the North pit ramp's limit was cut on 9 June, and the vendor installed firmware 5.0.2 on every haul truck
unit between 2 and 23 June. The update made the critical alert sound like the warning alert, which nothing in the pack
says: operators still press acknowledge and no longer brake. After a collision at the North ramp junction on 7 July
the Mines Safety Inspectorate issued an improvement notice (2 September) requiring the cause and a control; the site
safety steering committee funds one of five 2027 programmes on 19 November 2026 under terms HSE-TOR-026.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task400.json`, architecture 1, registered 2026-11-03 and brought to the
  redesigned mechanism at stage 2 (driver, stump, analyst test, niche, layer1, people). `guard.py check` on the merged
  tree with the sibling cards in place: WARN only (repeat.gate_g and repeat.question_form against task398; a pick asks
  which, and decomposition_attribution is the honest Gate G). NOTE test.same_driver_older against task107 v2 and
  task121 v4 (lineage), differentiated on the card.
- **Pairing:** Human Factors & Ergonomics (client domain) / `safety-incident-error-analysis` / Root-Cause Analysis. The
  task type serves Root-Cause and Anomaly Detection; no live Root-Cause card sits on it (task190 is its Anomaly build;
  task191 architecture 3, a bus operator's collision warnings, died at stage 4 before shipping).
- **Objective and call:** which one of five programmes the committee funds for 2027, decided by naming the driver that
  accounts for most of 2026's rise (terms 3.2). The programme runs in 2027, so the call faces forward; it is judged on
  the closed record of January 2025 to October 2026 because the notice asks for the cause of the rise. Root-Cause, not
  Forecasting: nothing is projected.
- **Candidates (terms section 4):** A operator vigilance refresher; B separated light vehicle access at the North ramp
  junction; C collision avoidance alerting review on the haul truck units; D night shift fatigue monitoring; E ROM
  crusher pad traffic management.
- **Shape:** 18, hypotheses against evidence: each programme's driver read against the evidence it predicts, the call,
  and two asks on the exposure records the committee's plan needs (`## Ask sheet`).
- **Strategy and Gate G:** `causal_design` (the staggered rollout is a comparison inside three weeks: the same crews on
  the same days drove upgraded and not-yet-upgraded trucks); Gate G `decomposition_attribution` (a correctly reported
  rise assigned to the right driver). Gap objective then time; pattern none; generators G3 (an alert against what the
  operator did next), G12 (the acknowledgement press is logged, the absence of braking is logged nowhere), G6 (stage 3
  shifting the route mix toward the junction).
- **Furniture:** forum `committee_or_panel`, forcing event `incident_or_complaint` (the 7 July collision and the
  improvement notice), org family `other` (a mining company), role `compliance_or_audit` (the health and safety
  superintendent), context artifact `monitoring_export` (the vendor's monthly fleet report), calibration none. None is
  held by the last three live cards (task277, task398, task399 architecture 4).
- **People** (`guard.py names --geo "Australia" --seed 400`): Shari Jefferson (health and safety superintendent, owner
  of the terms and the register), Ana Cuevas (the vendor's site support engineer, the monthly report), Nancy Franco
  (inspector of mines, the notice), Kerri Smith (production manager, on the card, not in the pack). None is in the
  prompt.
- **The coordinator's three points, settled by measurement at stage 2:**
  1. *The reflex risk on C.* Every cheap route to C was measured on the cut pack and asserted in `checks.py`: alerts per
     100 operating hours run 37.4 to 42.0 in every month (no flood); critical alerts per load rise from 0.20 to 0.23
     with stage 3's longer cycles, which reads as B's traffic; acknowledgement runs 89.6 to 96.6 per cent and is 96.2
     against 96.4 per cent on the two firmwares; the critical alert fires at the same range (median 15.5 against 15.3
     m); the incident split by firmware inside the rollout weeks is 2 incidents on 543 truck shifts on 4.3 against 6 on
     589 on 5.0.2 (2.4 and 7.8 expected from the world's own rates, R3d), too few to carry the call alone; and the June
     step in the monthly count is shared by three dated changes (stage 3's traffic, the ramp limit, the firmware). The design dropped the earlier alarm flood (`## Tried and rejected`) because a flood is
     itself a route to C.
  2. *The endpoint.* The default path ends on B, the junction, never on C; A is the careful stop after B dies on rates
     (the pooled slowdown share falls from June, which reads as operators' attention). Both are measured in `## Ladder`.
- **Round 1 at stage 4 (judge DETERMINISTIC, FIX_NOW; reader clean), answered in one generator pass:** the two counted
  units are filed in the prompt as WHAT (`## Semantic fork table` SF7 and SF9); the incident draw is re-drawn to a
  representative one and the write-up's attribution cut to what the records show (`## Tried and rejected`); the
  reader's question 7 is closed row by row (SF16 to SF18, the gate codes added to the location list); the register's
  free text is varied and asserted (no description more than three times).
  3. *No shared narrative with task399 v4.* No newcomer and no arrival: every operator is the mine's own and the crews
     do not change; nothing is dated March 2026; the change is a vendor's software update, not a process change.
- **Data-native sentence:** the collision avoidance log records every alert and the operator's acknowledgement press in
  UTC under the unit's serial, and nothing records whether the operator slowed; the truck's speed in the dispatch
  system's event windows, on Western Australian time under the truck's fleet number, is the only record of what the
  operator did, the unit-to-truck link exists only in the device register's dated installs, and the firmware each unit
  ran sits in a third sheet, so the response by firmware exists only as a reconstruction across three systems.
- **The abstraction sentence:** "a software update changed how a warning sounds; the people warned kept acknowledging
  it and stopped acting on it, and incidents rose while every count the warning's vendor reports stayed flat." Written
  against every approved and delivered Root-Cause driver and the warning, alert and exposure drivers on file: task122 v4
  reads a decision aid's effect at like traffic (confounding by conditions of use); task129 places a rise outside a
  provider's zone; task303 removes a shared supply loss logged under each feeder; task398 re-runs a rule keyed to the
  whole's own path; task399 v4 reads an advocate's presence in the room; task191 architecture 3 (never shipped) read
  depots' failure to act on genuine warnings once planted fixed structures were caught. None is a warning that kept
  firing and being acknowledged after it stopped working, separated from the people by a staggered rollout.
- **Semantic screen** (`guard.py mechanisms --objective root-cause`): the decisive step rebuilds no stock, re-runs no
  system on a changed path, rebuilds no worker's state from his own consecutive records, places no exposure in
  surroundings or layers and reads nobody's presence in a room; it reads each warning against what the warned operator
  did in the next seconds and compares warnings from upgraded and not-yet-upgraded units inside the rollout weeks.
- **Library test:** the golden is not a named correction. The field's measures (incidents per exposure by location,
  route and shift; the hotspot; the vendor's alert and acknowledgement rates) sit at rungs 0 to 4.
- **Sources** (every file synthetic, generated by `generator/` from seed 400, invented world, no real organisation,
  mine, vendor or person; licence CC BY 4.0, recorded in `metadata.json`): the collision avoidance alert log (the spine,
  141,693 rows, UTC), the dispatch system's event windows (speed samples, local time), the dispatch shift summary, the
  pit gate reads, the incident register, the device register, the location codes, the light vehicle register, the
  speed limit schedule, the vendor's monthly report, the inspectorate's notice, the review's terms, and two
  distractors named in `metadata.json` (haul road dust and road maintenance).

## Default path

1. Read the terms (vi_review_terms_2026.docx) and the notice: name the driver that accounts for most of the rise
   (3.2) and fund the programme that answers it.
2. Count the register's VI-COL and VI-SPI entries by month (2.1): 24 in July to October 2025, 89 in July to October
   2026, the monthly count stepping up in June 2026.
3. Split by location: the North ramp junction goes from 6 to 24 and is 2026's top location; the notice's 7 July
   collision was there.
4. Read exposure from the dispatch summary: the North waste route, the one through the junction, goes from about 14 to
   about 35 per cent of truck shifts from June 2026, and critical alerts per 100 operating hours rise with it.
5. Read the vendor's report: alerts per 100 operating hours and acknowledgement steady through the firmware update of
   2 to 23 June, so the system works and operators answer it.
6. Fund B, separated light vehicle access at the North ramp junction.

Ends on: B, separated light vehicle access at the North ramp junction.

Golden: C, the collision avoidance alerting review: in the weeks 5.0.2 went on, the same crews slowed for about 85
per cent of critical alerts from units still on 4.3 and about 30 per cent from units already on 5.0.2.

## Stump sentence

A competent solver counts the register's vehicle interaction incidents (24 to 89), finds them gathered at the North
ramp junction, where the notice's 7 July collision happened and where stage 3 put more trucks from June, reads the
vendor's steady alert and acknowledgement rates as a working system, and funds B (Ends on: B); the step that lands it
there is never reading each critical alert against the truck's speed by the unit's firmware, which shows that in the
weeks 5.0.2 went on the same crews slowed for about 85 per cent of critical alerts on 4.3 units and about 30 per cent on
5.0.2 units, so the driver is the alerting and the programme is C.

## Three rules

- **Task type:** `safety-incident-error-analysis` (Human Factors & Ergonomics): incident causation read from the
  incident register and the systems' own logs; it serves Root-Cause in the taxonomy.
- **Domain test:** the quantity that decides is the share of critical collision warnings operators acted on, the
  measure of whether a warning still works as a warning, estimated alert by alert from the truck's speed after onset;
  the field's reflex measures are incident counts and rates per exposure by location, route and shift.
- **Swap:** "fund the alerting review because operators stopped braking for critical collision warnings from units on
  the new firmware" with a retailer's nouns ("shoppers stopped stopping for red shelf tags on the new labels") loses
  the seconds-scale response read from vehicle telemetry against a warning's onset, so the estimate has nothing to run on.
- **Layer 1:** the alert log runs on UTC under unit serials while the dispatch system and the register run on local
  time under fleet numbers (vendor cloud against site systems); six units were swapped between trucks, dated only in
  the device register; 1.9 per cent of critical alerts have no event window and 1.6 per cent of speed samples have no
  GPS fix; the FMS export restates each window's limit to today's; FMS 7.2 logs a run still over the limit as a second
  window from 1 August; a second North gate reader came online on 14 July and both readers misread plates; the
  register mixes VI codes with injuries, damage and environment entries. Nothing is placed to be caught.
- **Layer 2:** causal design: the staggered rollout is a natural comparison that holds the crews, the routes and the
  days fixed while only the alerting differs, against the before-and-after and hotspot reads that confound the
  firmware with stage 3's traffic.
- **Decisive step:** comparing warnings from units already upgraded with warnings from units not yet upgraded inside
  the 2 to 23 June stagger, the same crews on the same days, rather than reading the fall in braking across all units
  as a fall in the operators' attention.
- **Not semantics:** every code, clock, unit and definition read right (VI codes, UTC against local, serials against
  fleet numbers, the firmware dates) still leaves the easy route on B, and on A after rates: no field says an operator
  did or did not brake, and the hotspot, the vendor's steady counts and the monthly fall in braking all read correctly.
- **Not rule application:** no filed rule says to read alerts against speed, to split by firmware or to use the rollout
  weeks; the terms file only the incidents, the window and "the driver that accounts for most of that rise". The
  enumerated family files five calls (the hotspot B, the crusher pad E, the night share D, the pooled braking share A,
  the firmware split C); the standing family once the records are read is the firmware split alone, which prints 85
  and 30 per cent to the nearest 5 under every slowdown rule (4 to 10 km/h at 4, 6 or 8 seconds) and every reading of
  the rollout weeks (spread zero at the graded precision); what rules the others out is quiet, a comparison no
  document invites and no sentence names.
- **Analyst test:** a strong analyst who reads every field and rule correctly counts 24 to 89, finds the junction on
  top with the North waste route's traffic up from June and the vendor's counts steady, and files B (Ends on: B); one
  who also rates by route sees B fail, reads braking month by month and files A; only the firmware split inside the
  rollout weeks separates the alerting from the operators.
- **Estimand:** vi_review_terms_2026.docx 2.1 and 3.1 to 3.2: VI-COL and VI-SPI register entries counted in their
  month, Western Australian time, July to October 2026 against July to October 2025; the driver that accounts for most
  of the rise; the section 4 programme that answers it.
- **No decoy:** nothing is planted: the notice cites a real collision, the vendor's report is correct for what it
  measures, no memo, draft or stakeholder figure argues a programme, and no block of records is copied.
- **No certified replay:** no certified or published figure encodes the method; the vendor's report says nothing about
  braking and the golden's split reproduces no shipped figure.
- **Lesson:** a warning can keep firing and being acknowledged after it has stopped working as a warning, and a
  staggered rollout is a ready-made comparison that separates the system from its users; no build on file reads a
  warning against the warned person's behaviour across a staggered change.

## Survivor anatomy

- **Actor:** whether an operator acted on a critical alert has no column: alerts carry onset, range and
  acknowledgement, windows carry speed samples, and the property is a relation between an alert's onset and the speed
  samples of a window on the same truck seconds later.
- **Link:** alert serial to truck through the Devices sheet's dated installs, UTC to local, the CAS_CRITICAL window on
  that truck within seconds after onset, the firmware at onset from the Firmware sheet; no key is shared by any two of
  the three systems.
- **Reflex:** the field's measures (the hotspot by location, incidents per truck shift by route, the night share, the
  braking share pooled over units) sit at rungs 0 to 4 and file B, then A.
- **Back-test:** the vendor's report validates the easy route: alerts per 100 operating hours steady, acknowledgement
  steady, the same on both firmwares, and the critical alert's range at onset unchanged.
- **Second use:** the alert log feeds the vendor's report; the event windows carry the OVERSPEED windows ask B reads;
  the device register is the vendor's asset record; the dispatch summary carries the exposure every rate needs; delete
  the decisive step and every file stays.
- **Shock:** the fall the step recovers sits in no shipped statistic; the June step in incidents is shared by three
  dated changes, and the golden is the top of no sort (the junction tops locations, the North waste route tops
  traffic).
- **Pins:** the terms file the WHAT in the organisation's own genre (codes, months in local time, the two windows, the
  driver of most of the rise, the programmes); no sentence names the speed reading, the firmware split, the rollout
  weeks or a slowdown threshold, and deleting any filed sentence leaves the call forced by the records.

## Readability screen

| Rung | What a reader needs to find it | Verdict |
|---|---|---|
| B, the junction (rung 0) | the register's location codes, the notice, the dispatch route mix | readable |
| E, the crusher pad | the register's location codes | readable |
| D, night shift | the register's times against the shift pattern | readable |
| A, the pooled braking share | alerts against speed windows, pooled over units | silent |
| C, the firmware split (decisive) | alerts against speed windows by firmware at onset inside the rollout weeks | silent |

## Ladder

Measured on the cut pack (`checks.py`, `ceiling.py`), July to October unless stated.

| Rung | Read | Figures | Dies to |
|---|---|---|---|
| 0, B | the hotspot and its traffic | junction 6 to 24, top in 2026; North waste route 13 to 15 per cent of truck shifts to May, 33 to 36 from June | per 1,000 truck shifts every route rose: South pit ore 2.2 to 9.2, South waste 3.6 to 10.6, North ore 4.0 to 11.0, North waste 8.4 to 21.3 |
| 1, E | the crusher pad | 7 to 15 | its share fell from 29 to 17 per cent while every location rose |
| 2, D | the night share | 9 of 24 to 40 of 89 | days rose 15 to 49; on 5.0.2 units braking is 32.1 per cent by day and 31.8 by night |
| 3, A | braking share by month, pooled | 0.86 to 0.88 every month to May 2026, 0.54 in June, 0.30 to 0.33 July to October | inside the rollout weeks the same crews brake on 4.3 units |
| 4, C (decisive) | braking share by firmware at onset, 2 to 23 June | 85.9 per cent of 629 alerts on 4.3 against 29.4 of 640 on 5.0.2; 129 operators drove both | none |

Margins: the decisive split is 2.92 times; critical alerts nobody slowed for rose from about 880 to about 4,900 in
July to October (more than fivefold under every slowdown rule), against incidents rising from 24 to 89; every slowdown rule from 4 to 10 km/h read at 4, 6 or 8 seconds, and every
reading of the rollout weeks (local days, UTC days, first to last upgrade, all of June), gives 85 and 30 to the nearest
5. Separation: the call reads the register, the alert log, the CAS_CRITICAL windows, the device register and the
dispatch summary; the asks read the gate reads, the OVERSPEED windows and the speed limit schedule; no ask device sits
on a row the call reads.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | vehicle interaction incident | VI-COL or VI-SPI entry | add NM near misses | same call | terms 2.1 |
| SF2 | the month an incident falls in | Western Australian time | UTC | same call (24 and 89 either way) | terms 2.1 |
| SF3 | the comparison window | July to October 2026 against July to October 2025 | calendar years | same call | terms 3.1 |
| SF4 | "accounts for most of that rise" | the driver behind most incidents | the largest single location | same call (C under every split the records allow) | terms 3.2, asserted |
| SF5 | an alert acted on | the truck slowed by a clear margin within seconds | any rule from 4 to 10 km/h read at 4, 6 or 8 s | same call, 85 and 30 | C1, asserted |
| SF6 | firmware family | 4.3.11 and 4.3.14 together against 5.0.2 | each 4.3 release apart | same call (both above 0.8) | C1, asserted |
| SF7 | a light-vehicle trip into the pits | one vehicle entering a pit, whichever readers recorded it | every IN read | ask figures move | the prompt's "a trip is one vehicle entering a pit"; the readers' timing separates entries, asserted |
| SF8 | a trip by a vehicle whose tag the gate did not detect | empty cas_tag on the trip | either North reader empty | same figures (both readers agree) | C1, asserted |
| SF9 | a time over the limit | one continuous run: a window joins the run before it only where it opens on that window's closing sample with the truck over the limit | each FMS window; windows within a gap | ask figures move | the prompt's "one continuous run above it"; the shared sample decides, the same for any line from the limit to the limit plus 2 (C1), asserted |
| SF10 | peaked more than 5 km/h over | highest recorded speed above limit plus 5 | at the trigger sample | same figures (no peak within 0.3 km/h of the line) | C1, asserted |
| SF11 | the limit in force | the schedule's limit on the window's day | the window's own limit column | ask figures move | the prompt's "in force", haul_road_speed_limits.csv |
| SF12 | the month of a window | the window's trigger time, local | UTC | same figures | C1, asserted |
| SF13 | each pit ramp | NRP and SRP | the haul roads too | ask figures move | site_location_codes.csv names the ramps |
| SF14 | light vehicles at the gates | every vehicle the gates read (light vehicles only) | registered vehicles only | same figures | C1, asserted |
| SF15 | the rollout weeks | 2 to 23 June 2026 | UTC days, first to last upgrade, all of June | same call, 85 and 30 | C1, asserted |
| SF16 | the month of a gate read or an event window | Western Australian month | UTC month | ask figures move | the headers read_time_awst and trigger_time_awst, asserted |
| SF17 | a tag the gate did not detect | a blank cas_tag | a tag missing from the device register | same figures (every read tag is registered and in service) | C1, asserted |
| SF18 | samples with no GPS fix | dropped where missing; each window's first, last and highest samples are always present | windows with a missing sample dropped, or another offset for the braking read | same figures | C1, asserted |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | VI-COL and VI-SPI entries; haul trucks' critical alerts | terms 2.1 and 2.2; C1 |
| 2 Unit of account | a register entry; an alert; a trip; a time over | terms 2.1; the prompt's nouns |
| 3 Attribution window | month of occurrence, local | terms 2.1; SF2 C1 |
| 4 As-of dating | firmware and unit at the alert's onset | C1 (SF15), asserted |
| 5 Version basis | the register as exported 1 November 2026 | one export, no revisions |
| 6 Denominator | alerts with an event window | C1: 1.9 per cent lack one, split unchanged |
| 7 Weighting | alerts pooled within each firmware | C1 over operator-level reads, asserted |
| 8 Window length | July to October | terms 3.1 |
| 9 Boundary inclusivity | July 1 to October 31 inclusive | nothing near the edges moves the call |
| 10 Rounding path | whole counts; shares rounded once to the nearest 5 | filed in the write-up's block 2 |
| 11 Tie-break | none needed | no ties among programmes |
| 12 Maturity and censoring | October 2026 complete in the export | export of 1 November 2026 |
| 13 Order of operations | map unit to truck, then match the window | C1, asserted |
| 14 Row order | none | counts and shares are order-free |
| 15 Duplicate resolution | two North reads of one entry are one trip; a window opening on its predecessor's closing sample above the limit continues that run | the prompt's two units (SF7, SF9), asserted |
| 16 Identity normalisation | serial to truck by dated installs; plates as read | C1, asserted |
| 17 Netting against gross | none | no offsets |
| 18 Dimensional units | km/h throughout | C1 |
| 19 Code and status semantics | VI codes per terms 2.1 | terms 2.1 |
| 20 Integerisation | whole counts | by construction |
| 21 Clause scope | terms apply to the review | terms 1 |
| 22 Forward window contents | the call funds 2027 from the closed record | terms 3.2; the notice |

## Literal reader

Executed word for word: the prompt asks which programme to fund against the rise; terms 2.1 and 3.1 fix the
incidents (24 and 89), 3.2 fixes the target (the driver of most of the rise) and section 4 maps drivers to programmes.
The records do the rest: every reading of an acted-on alert and of the rollout weeks gives the same split (SF5, SF15),
every location and route reading leaves the rise site-wide, and no literal reading of any filed sentence names
another programme. The asks' literal readings (SF7 to SF14, SF16 to SF18) each resolve to one figure set; the ones that move figures
are fixed by the prompt's own words ("a trip is one vehicle entering a pit", "one continuous run above it", "in
force") or by the export's own headers (the zone in read_time_awst and trigger_time_awst).

## Oracles

- improvement_notice_IN-2026-0417.pdf: requires a cause and a control, names the 7 July collision; ranks no programme.
- cas_monthly_report_2026-10.pdf: alert volumes and acknowledgement by month, correct for what it measures, and the
  firmware line; ranks no programme and says nothing about braking.
- vi_review_terms_2026.docx: defines and lists; ranks no programme.
- Gate G: no shipped artifact ranks the candidates on the decision question; no declared wrong-basis distractor.
- leak.py's stump-vocabulary lines, ruled here (they never reach the reader): the vendor report's alert words are its
  own subject and it names no driver; the notice's register, junction and operator words cite its own collision; the
  terms' words are its definitions and its programme list. All harmless. Round 1's reader ruled the two call-word lines
  harmless and answered question 1 with none.

## Ask sheet

**Shape 18, the criteria.** The call side: the call, the two counts, the rollout weeks, the two braking shares, the
chart's bars and labels (8). The files: 2. The asks: 24 figures. 34 criteria; weights 38 on the call side and chart,
7 on instruction-following, 55 on the asks.

- **Ask A, light-vehicle trips into the pits and those with no tag detected, by month July to October 2026 (eight
  figures, whole counts).** H18 home: the light-vehicle exposure and tag compliance the committee's plan needs, a
  measure every programme carries that the call does not turn on. Path: the gate reads, the light vehicle register.
  Primary (D1, one passage under two readers whose plates differ): from 14 July the North gate has two readers that
  read each vehicle seconds apart and each misreads plates on its own, so a vehicle read twice under the same plate
  collapses on any dedupe while a pair read under two plates survives one; only the readers' timing pairs them.
  Hazard: the second reader's arrival mid-July. The filed unit ("a trip is one vehicle entering a pit") names no
  reader, so it leaves the pairing to the records.
- **Ask B, haul truck times over the limit in force on each pit ramp and those peaking more than 5 km/h over, by month
  July to October 2026 (sixteen figures, whole counts).** H18 home: the ramp speed record the plan's controls are set
  against. Path: the OVERSPEED windows, the speed limit schedule, the location codes. Primary (which windows are one
  run, read from the samples): on the long descents a truck braked under the limit and ran away again on the next
  sample or two, so two windows open 10, 12 or 14 seconds apart are separate runs, while from FMS 7.2 on 1 August a run
  still over the limit when its window closes is logged again in a window that opens on the closing sample; only that
  shared instant's speed, over the limit or under it, tells a continuation from a new run, so counting windows
  overcounts August to October and merging by gap undercounts every month. Hazard (D2, a label stored as of today):
  each window's limit column carries today's limit, wrong for the South ramp before 18 August.
- **Separation (asserted):** the asks read the gate reads, the OVERSPEED windows and the schedule; the call reads none
  of them. Delete every device and the call is as hard.
- **Rounding edges:** every graded ask figure is a whole count; the braking shares are graded to the nearest 5 and the
  tightest sits 0.77 points from an edge (SF15).

| Ask | Cracker (lands the call, runs the battery, executes every filed statement) | Verdict |
|---|---|---|
| A trips | one trip per plate per gate within 30 seconds: 0 of 8 (trips 7,647, 7,828, 7,683 and 7,876 off) | miss |
| B ramp times | the schedule's limit, windows that abut in time taken as one run: 2 of 16 (North ramp 50, 64, 55 and 39 runs off) | miss |

Measured by: generator/ceiling.py on the cut pack (target.zip 63cfa0bc; pandas only, no generator code): the cracker
keeps 2 of the 24 ask figures; the mirror on B keeps the same 2 and 4 of 8 on the call side (the two counts and the
chart).
Pair ceiling: 40.1 (the cracker 38 + 7 + 4.6 = 49.6; the mirror 19.0 + 7 + 4.6 = 30.6).
Mirror leakage: 8.3 per cent of ask weight.
Stress rows: a response that counts every window keeps the four July ramp figures (no continuation windows before 1
August); the full includer (North reads paired by the readers' timing whatever the plates, runs read from the shared
sample) keeps 24 of 24, the residual risk recorded here.

## Tried and rejected

- 2026-11-03, the seed's own world (RC06: an area control centre's summer of tripled en-route ATFM delay, the
  performance plan's characterisation of each mechanism's share), refused at the draw before any harness: (1) its
  honest decisive step, a queue replay in which a short hour's backlog outlives it, is task398's path-dependent re-run
  counterfactual and task399's capacity stock against demand in other nouns, and every honest route to the seed's
  quantity runs through that replay; (2) its honest strategy, decomposition_attribution, is held by task398 in the ban
  window, and so is its forcing event, a statutory filing; (3) under Supply Chain & Logistics and under Human Factors
  the same queue is the decisive step again. Moved world, dataset and domain.
- 2026-11-03, draw screens set aside before the card (each one line): an electricity network's evening-peak fuse
  operations from synchronised EV charging (task196's coincident peak, task201's diversity factor); a hospital's
  medication incidents on outlier patients (task122 v4's confounding); a dispensing robot's mis-filled canisters (a
  state rebuilt from its own events, task121 and task399); workers' compensation claims developed for report lag
  (task130, task149, task196); a bathing beach's markers tested only after rain (the WHAT screen); blood lead through
  first-draw samples (task202's layers); ambulance manual handling per heavy carry (task129's exposure family);
  aircraft noise complaints against events above 65 dB (a free dose-response form).
- 2026-11-03, stage 2, the first mechanism (warning zones widened in March 2026, an alarm flood of false alerts, a
  contractor's new operators on the North waste circuit from April, the default path ending on A, contractor
  retraining): dropped at the coordinator's review before data was cut. A flood is itself a cheap route to C (alerts
  per hour jump at the change), a newcomer plus a same-spring process change is task399 v4's narrative, March 2026 is
  task399's month, and strong solvers leave a retraining endpoint for an engineering control, so the next stop had to
  be B. Replaced by the unannounced firmware tone change with steady alert counts and the junction as the endpoint.
- 2026-11-03, stage 3, ask A's turn-backs (vehicles read IN and OUT at one gate within two minutes, dropped as no
  trip): dropped because whether a vehicle turned back at the boom made a trip into the pit is a reading, not a
  reconstruction, so the device was a semantic fork the judge would file and filing it would hand it to the cracker.
- 2026-11-03, stage 3, ask B by quarter of 2026 to September: the cracker kept every first and second quarter figure
  (the only device there was the restated limit, which the schedule repairs), putting the pair near 60; re-sited to the
  months July to October, where the continuation windows bite three months in four.
- 2026-11-03, stage 3, the braking shares stated over the whole record (86 and 32 per cent): the 4.3 share sat on its
  rounding edge (86.4 to 86.5 under rules read at 8 seconds) and the rollout share moved a point with how the weeks are
  bounded; the component now states the rollout weeks to the nearest 5, and the response traces were sharpened so every
  reasonable slowdown rule classifies the same alerts.
- 2026-11-03, stage 4 round 1, the judge's FIX_NOW (two ask units unfiled): filed in the prompt as WHAT, "a trip is one
  vehicle entering a pit, and a time over the limit is one continuous run above it". The judge's own wording ("however
  many gate readers read it", "however many windows the system logged") was not taken: it names the readers and the
  windows, the very dimensions the two devices live in.
- 2026-11-03, stage 4 round 1, ask B's continuation device under the filed unit: windows that abut in time are merged by
  anyone executing "one continuous run", so the continuation alone was a work order. Re-sited on this world's own
  Layer 1: runs on the long descents that dip under the limit and run away again on the next sample sit 10 to 14
  seconds apart like continuations, and only the shared sample's speed separates them.
- 2026-11-03, stage 4 round 1, the incident draw (stream "incident"): the 4.3 units carried 7 incidents in the rollout
  weeks against 2.4 expected from the world's own rates (about a 1-in-70 draw), so the register argued against the
  driver the records measure, and checks.py had asserted the split "under 2 times" instead of asking whether the draw
  was representative. Re-drawn on the incident stream only (incident-87: 2 against 2.4 and 6 against 7.8), with R3d
  screening representativeness; the crusher pad's rung killer moved from its count to its share, because a fourfold
  site-wide rise lifts every location's count; the write-up's attribution now claims only the braking split inside the
  stagger and the unheeded critical alerts, not that the register alone proves the firmware carries the rise.
- 2026-11-03, stage 4 round 2 (judge DETERMINISTIC, FIX_NOW on the solution side; reader clean; every round-1 finding
  closed): the chart line in the write-up graded a bar chart with labelled bars where the prompt asks only for a chart
  of the monthly count, so it now grades that chart with each month's count readable (the golden chart is unchanged).
  Two residual forks were closed in the generator with no figure moving: 33 same-vehicle north-gate entries 16 to 27
  seconds apart (a vehicle's next entry is now at least 20 minutes after its last, moved later in the same month, or
  earlier at a month's end), and a South ramp run on 18 August peaking between the new and the old limit (no ramp
  window now falls on its limit-change day; such runs moved to the next day of the same month). Only the gate reads
  and the event windows changed; every document, the prompt and all 38 figures in figures.json are byte-identical or
  equal to the round-2 pack's.

## Pre-ship check

- **The 10/10 rules, re-read against the built pack (target.zip 63cfa0bc).** Rule 1: the deciding quantity is the share
  of critical collision warnings operators acted on, estimated alert by alert from the trucks' speed windows; swap in
  another field's nouns and nothing is left to estimate it from. Rule 2: Layer 1 is the systems' own mess (UTC alerts
  against local windows, serials against fleet numbers through dated installs, a second gate reader with independent
  misreads, an FMS release logging continuations, fix-less samples, a restated limit column), none of which decides the
  call; Layer 2 is the within-stagger comparison. Rule 3: no plant (the notice, the vendor report and the terms are each
  correct for what they say and rank nothing), no semantics (every field read right still files B, then A), no rule
  application (no filed sentence names the speed reading, the firmware split or the rollout weeks). Analyst test: the
  easy route ends on B (the junction, its stage 3 traffic, the notice's 7 July collision). The judge's Gate H: domain
  pass, layers pass, decisive step analytical (rounds 1 and 2); the reader's question 6: an analytical choice (both
  rounds).
- **Gates on the final cut:** checks.py 75 assertions, 0 FAIL (tightest edges: the rollout-week shares 1.29 points of 5
  under every rule and 0.39 under every reading of the weeks; the step-2 rates named in their own assertion);
  verify.py 30 figures, 0 mismatch; two byte-identical builds; figures_check 0 absent; precut 0 FAIL, 0 WARN,
  voice-check exit 0; leak.py REVIEW, no LEAK; guard heart WARN (nearest task191 v3, 0.11, lineage), surface exit 0.
- **Deliverables:** vi_programme_paper_2027.docx (the call, the two counts, the chart) and vi_workings_2026.xlsx (the
  two ask tables); office properties scrubbed (H1), pack PDFs carry no library default entries.
- **Flag carried to the author:** surface promotes task398 against task400 (two apart; decisive gap and decision type
  collide, pattern differs), for the adjudicated /clone-check if wanted.

