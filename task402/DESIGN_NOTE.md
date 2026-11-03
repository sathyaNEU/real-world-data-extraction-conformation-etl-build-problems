# task402 design note

Architecture 3, drawn 2026-11-03 (wave 7, Root-Cause lane), numbered from seed RC08 (a wind turbine's five faults and
its one spring crew visit). Architecture 1 (an NHS Talking Therapies service) died at stage 4 on the determinism judge's
SEND_BACK and architecture 2 (a bowel screening hub's equity fund) died at stage 2 on honest levels, before any
generator (`## Tried and rejected`, their lines, and the card's `lineage`). Architecture 3 moves domain, world, dataset
and shell. Kept from the seed: the decision kind (one of five changes gets the single fix) and the quantity's kind (what
the change cost over the review year, in the period's natural unit). The kernel is new.

An electric membership cooperative in central Minnesota (an invented county north of the Twin Cities; about 136,000
members on some 190 feeders) adopts its 2027 reliability work plan at the board's November 2026 meeting. The plan funds
one fix: the one change, among the five the reliability review lists for the twelve months to 30 September 2026, that
cost the members the most sustained interruptions (IEEE 1366 customer interruptions, major event days excluded). The
review's five changes, each with its filed in-place date and scope: heat pumps connected under the cooperative's rebate
without a load study (1 November 2025, services connected under the rebate); the control centre's restoration switching
template revised to shorten restoration times, every section now picked up in one switching step (1 December 2025, all
restorations); the
pre-winter infrared inspection of underground terminations skipped (from 1 October 2025, underground sections); the
animal guard programme ended (1 January 2026, its 2026 site list); a new pole-top transformer supplier (1 February
2026, transformers fitted after).

What nothing in the pack says: after an hour or more without supply in hard frost every electric heating load on a
section calls at once, so a section re-energised in one step draws two to four times its diversified load and its
protection trips again within minutes. Under the old template the control centre picked such sections up in pieces
and re-trips were rare; from 1 December they are common, each one a second sustained interruption of the same members,
logged as an overload trip on the section that had just been restored. The heat pump policy takes the rise.

## Draw

- Card: `.claude/skills/fingerprint/cards/task402.json`, architecture v3, drawn and registered 2026-11-03 (the
  registered stamp and the last `check` are in `pipeline.json`); architecture 1's and 2's identities sit in the card's
  `lineage` with their fates and their shells in `lineage_shells`. `guard.py validate` clean.
- Pairing: Energy Systems and Utilities, task type grid-reliability-outage-analysis, objective Root-Cause Analysis. The
  work plan is decided on which change raised the members' interruptions, the task type's own question, worked on the
  outage record by cause, device and restoration. Probed with `guard.py check` on probe cards in both directions before
  the draw: this cell is legal for Root-Cause (no task-type BLOCK), and the cell's builds (task129, task183, task187,
  task197, task201) were read, with the `resume` of each grid slot (task201 paused at architecture 14 on shared-parameter
  constructions; nothing on restoration practice or re-trips).
- Shape 01, ranked list: the five changes, each with its fiscal 2026 cost in sustained customer interruptions and in
  interruption events; the call, runner-up, gap and flip; a ranked bar chart with its parts; three files. The sum is
  written in `## Ladder` at stage 2.
- Strategy decomposition_attribution: the year's rise in overload interruptions splits between true overloads from new
  heat pump load and cold-load re-trips after one-step restoration, and only pairing each trip with the same section's
  restoration minutes before decides the split. Decisive generator G9 (downstream survival against upstream
  acquisition: the restoration the revision's own measure times is the acquisition, whether the restored supply held is the
  outcome scored); G14 (conditioned yield) behind it, the staged-era re-trip rate applying only to restorations after an
  hour or more in frost.
- Decision, quantity and tense: pick one of five; the quantity is interruptions in a closed review year (12 months to
  30 September 2026), the decision forward (the 2027 work plan's one fix). Retrospective quantity by design: the board
  policy costs each change on the year just closed, and the forward reading only widens the winner's lead (the revised
  template stays in force and every winter repeats it).
- Data-native sentence: the outage record logs each interruption on the device that opened, with the cause the crew or
  the control centre gives it, so a re-trip is a fresh overload trip on a section a few minutes after that section's
  previous interruption ended; nothing marks it as the restoration's consequence, and the pairing exists only as a
  relation between consecutive rows of one section.
- Abstraction sentence, tried against the nearest builds and not writable: against task121 (a coincident change takes the
  blame while a state rebuilt from consecutive records shows where the harm sits) a reviewer could say "a hidden state
  built from consecutive records decides", and it does not hold: no state is rebuilt here, the decisive object is one
  event that the previous event caused, and the change it implicates is the one whose stated effect is on durations;
  against task303 (losses every sibling unit logs in the same minute come from a shared upstream source) the pairing is
  within one unit across minutes, not across siblings at one minute; against task129 (a rise booked to a contractor is
  the surroundings beyond the cleared zone) no surroundings decide and nothing outside the record's own sequence does;
  against task173 (work on a unit raises failures in the following weeks) nothing is worked on: the restoration step
  itself sets off the second interruption within minutes, by the physics of lost load diversity.
- One line per nearest spent insight, screened semantically: task121, rest rebuilt from consecutive shifts (no rest, no
  state; one event caused by the one before); task129, outages per exposure and surroundings (no surroundings); task202,
  a source's input reaching the layer the response draws on (no transport); task398, a path-dependent counterfactual
  (no rule replay; the counterfactual is the staged-era re-trip rate); task399 a3, unmet demand behind an empty
  capacity stock (no capacity); task399, an advocate's absence at each call (no actor); task400, a staggered rollout's
  natural comparison (nothing staggered: the template changed at once); task401 a1, composition by closures (none); task401 a2,
  a dated shock meeting each unit's sensitive phase (no phase: the condition is the outage's own length and the day's
  frost); task401 a3, expectation against delivery (none); task402 a1, cases broken off when a fixed-term actor's
  assignment lapses (no actor); task402 a2, a level loss from a change in force through both compared years (the template
  changed inside the year and its harm is a rise, not a level); task187, a unit's shortfall against a reference curve (no
  curve); task13, outcomes re-attributed by evidence against their label (the label "overload" is right: the device did
  trip on overload; what decides is which change made it trip).
- `slots` before the first harness: mechanism nouns (cold load, restoration, re-trip, overload) return task129's realism
  line only (re-trips after restoration on storm days as Layer 1); setting nouns (cooperative, heat pump, electric heat,
  SAIFI, interruption, staged) return no slot at three terms; the driver run returns generic-word hits (task129, task118,
  task174, task190, task201, task202), none the insight.
- Guard WARNs answered: `overuse.objective` and `overuse.gate_g` (the lane is Root-Cause, and decomposition_attribution
  is the honest Gate G key for a rise split between two changes); `repeat.gate_g` against task400 and task401 (same
  answer; the strategy differs from all three window builds); `repeat.question_form` against task400 (a pick asks which;
  the shell's second sentence and deliverable set are redrawn, below). `test.same_driver_older` against task252 is
  differentiated on the card. Axis redraws, measured: G3 (record against operation) as the decisive generator BLOCKed on
  `ban.pattern` against task400; G7 and population-first gaps BLOCKed on `test.same_puzzle` and `test.same_driver` against
  task202, task308 and task487; utility_or_infrastructure would BLOCK on `ban.org_family` against task401 and is not
  the honest key anyway: a member-owned cooperative is cooperative_or_member_body, as task129 and task308 carry it.
- Shell drawn with the world: question form "which" (28 per cent of the corpus, under the 30 per cent quota), the second
  sentence opened by the year's terms rather than "Put" or "The", the rounding sentence opened by the figures it governs,
  deliverable set docx, png and xlsx (no build in the window and neither lineage shell: how-many, our, pptx+xlsx; where,
  csv+docx).
- People (`guard.py names --geo usa`, seeds 402 and 4020; Todd Holloway and Katherine Vazquez WARNed on `people.first`
  against task454 and task191 and were redrawn): Kayla Dean, Lawrence Reed, no people WARN on `check`.

- Axes redrawn at stage 3 (heart, 2026-11-03): once task401's architecture 3 was spent and left the window, task398 came into it and `ban.forum`, `ban.role`, `ban.artifact` and `ban.strategy` BLOCKed. Redrawn, each the honester label: the work plan is adopted by the cooperative's elected Board of Trustees (trustees_or_governors; the pack's documents name it so); the manager of system reliability sits in system planning (capacity_planner; research_desk was the looser fit); the stakeholder's context artifact is the fiscal year's reliability review, a close-out of the year (close_out_summary); the decisive variable is the minutes between a trip and the same section's last restoration, a relation in time between records (time_semantics), with decomposition_attribution kept as the Gate G mechanism. `three_rules.strategy_risk` WARN answered: no field carries those minutes and no filed rule computes them; reading every field right still files the heat pump policy. Heart is WARN only.

### The four go/no-go screens (prototype on the clean truth, 20 redraws each, before the card was registered)

Scratch: `t402/a3/proto_clpu3.py` for the draw (event timestamps to the minute, re-trips found by pairing; outputs
`screen_central.txt`, `screen_low.txt`) and `proto_clpu4.py` for the stage-2 re-measure after the coordinator's review
(heat pumps on a quarter of the electrically heated sections only, the policy's own harm on service transformers;
outputs `screen_p4b.txt`, `screen_p4c.txt`). A redraw re-draws every interruption, connection and re-trip; the realised
weather of the two years is the world's own and stays fixed. The figures below are the stage-2 calibration
(`screen_p4c.txt`); the draw's were within a tenth of them. Levels, each with its source or its stated absence:

- Interruptions: about 155,000 sustained customer interruptions a year on 136,000 members, SAIFI about 1.1 outside major
  event days, inside the range US distribution utilities report to the EIA (Form EIA-861 reliability data, 2021-2024,
  SAIFI without major event days about 1.0 to 1.4) and the range public power and cooperative benchmarks show.
- Cold load pickup: after an hour or more without supply in sub-freezing weather a section's load at re-energisation runs
  two to four times its diversified level and decays over tens of minutes (the IEEE Power System Relaying Committee's
  working group reports on cold load pickup and the papers behind them, from McDonald, Bruning and Mahieu, IEEE
  Transactions on Power Apparatus and Systems, 1979, onward); phase overcurrent pickup is set near twice peak load, so a
  one-step pickup of a heavily electric-heated section exceeds it; sectionalised restoration is the practice those
  sources describe for it. The re-trip probability itself has no published figure: it rises with the outage's length
  past an hour, the day's frost below minus 3 C and the section's electric heating share, to at most 0.5 per qualifying
  restoration without staging and 0.02 with it; the call is measured at 0.3 as well.
- Electric heat: electric heating shares of 2 to 90 per cent by feeder (median about a third), the spread of a Minnesota
  cooperative with off-peak and dual-fuel electric heat programmes. Rebate heat pumps go only to members already heating
  with electric resistance and replace it (the rebate's own eligibility and sizing terms, shipped), so a connection does
  not raise a section's electric heating load; a quarter of the electrically heated sections took one in the year.
- Rivals: the policy's own harm is service transformers serving rebate members blowing their fuses on the coldest days
  (about nine members each; the load study it waived checks exactly the service transformer and secondary, shipped);
  termination failures on underground sections in frost; animal contacts on overhead sections; transformer infant
  failures. None has a published rate for this cooperative and each is set under a quarter of the winner.

1. **Realistic levels and the lever against the rivals' estimates.** The golden's cost of the switching change (pairing
   each trip with the same section's restoration minutes before, net of the staged-era re-trip rate) is about 7,850
   customer interruptions (sd 1,240) against the rivals' 650 to 1,750 (animal guards 1,753 sd 261; heat pump policy
   1,348 sd 172; terminations 1,063 sd 341; transformers 647 sd 472). Every golden variant beats the best rival
   estimate by 1.5 times or more in **20 of 20** redraws, worst ratio **2.22**. At the low edge of the unpublished
   re-trip lever (0.3) every variant still clears 1.5 times in 17 of 20 (draw calibration, worst 0.86); the shipped
   level is the central 0.5. Mid-bin is asserted on the generator.
2. **The golden's own method holds the call.** Eighteen variants of the golden (a pairing window of 5, 10, 20 or 30
   minutes after the restoration; a qualifying outage of any length, 15, 30 or 60 minutes or more; with and without a
   frost condition; with and without netting the staged-era rate) average 7,650 to 8,260 and each is the winner in
   every redraw: a cold-load re-trip follows its restoration within four minutes and a qualifying restoration is an
   hour or more in frost by the physics, so the windows agree.
3. **No easy completion.** The decisive variable (the minutes between a trip and the same section's last restoration)
   is not one the default path brings in. Once it is in hand the cost is a count of paired trips less the staged-era
   rate, no functional form. The cracker's flexible versions of the default rungs land elsewhere: the overload
   category's rise booked to the heat pump policy names it 20 of 20; the policy on its own sections against the rest
   names animal guards 11, the policy 6, terminations 3; the same comparison inside bands of electric heating share
   names animal guards 11, the policy 5, terminations 4; the policy on peak-hour overloads names animal guards 13,
   terminations 6 and the switching change once, through a weather-noisy system residual only.
4. **Literal execution.** The board policy files the WHAT (population: the cooperative's members; outcome: unplanned
   sustained customer interruptions counted as the outage management system records them, IEEE 1366 major event days
   excluded; window: the 12 months to 30 September 2026; comparison: the year with the change against the same year
   without it, everything else as it was) and the review table files each change's in-place date and scope. Executed
   literally with every natural operationalisation (each scope against the rest across the in-place date; each cause
   category against the year before; the system's residual after the scoped changes), the call lands on the heat pump
   policy or animal guards and never on the switching change, whose filed effect is on restoration times and whose
   literal cost on interruptions is nil. The golden needs a step the WHAT never asks for. Every candidate has its own
   in-place date and scope, so none ties the golden on the same interruptions.

Re-measured on the generator at stage 2 (shipped draw, `generator/checks.py`, the files under `target/` read back): the
switching revision costs **8,700** customer interruptions and all 21 licensed variants of the golden (pairing window 5 to
30 minutes, qualifying outage of any length to an hour, with and without the frost condition, the staged era from fiscal
2025 or from fiscal 2022, transformer-level records in or out, netted or not) print the same figure, because the staged
era of the shipped draw carries no re-trip at all (stepped pickup at 0.3 per cent of the one-step lever); the rivals,
each a replay of recorded facts, are the heat pump policy 1,520, animal guards 702, riser terminations 671 and the
transformer supplier 118. The golden is 5.7 times the runner-up. The joint re-trip fork on the generator: 23 per cent of
the re-trips sit on sections with a waiver connection; booked to the policy the revision still leads (6,691 against
3,529), and over 20 redraws of the generator's world it leads in **20 of 20**, with the re-trip rate per qualifying
restoration equal on electrically heated sections with and without a connection (mean difference -1.9 points, sd 8.4).

The joint re-trip fork (the coordinator's review, measured on `screen_p4c.txt`): a quarter of the golden's re-trips
(mean 25 per cent, sd 8) sit on sections that took a rebate heat pump; booked to the heat pump policy they leave the
switching change first in **19 of 20** redraws (6,145 against 3,407), so the fork is inert at the call. At the draw's
coupling (heat pumps on 55 per cent of the electrically heated sections, `screen_p4b.txt`) the share was 53 per cent and
the change kept first in only 1 of 20 if they were booked to the policy, so the overlap was moved (`## Tried and
rejected`). The re-trip rate per qualifying restoration is equal on electrically heated sections with and without a
connection (27.4 against 29.3 per cent, difference sd 7.8 over the redraws).

## Default path

1. Read the outage management extract for fiscal 2025 and fiscal 2026 (local time; planned work out; records of five
   minutes or more), drop major event days by the IEEE 1366 2.5 beta method on the five years of daily SAIDI before the
   review year, and count sustained customer interruptions by cause and month.
2. The overload category rose most, in the winter, after heat pumps were connected without a load study from
   1 November 2025; animal contacts, riser terminations and transformer failures moved less.
3. Cost each change on its own mechanism and scope: the heat pump policy at the overload category's rise (the one change
   that adds load), checked against its own sections (overloads rose more on sections with a waiver connection); riser
   terminations on the 2025 replacement list's risers; animal guards on the 2026 list's sites; the transformer supplier on
   units fitted from 1 February; the switching revision on restoration minutes, where it shortened restorations, and on
   interruptions at nothing, since a revision that shortens restoration changes how long members wait, not whether
   they lose supply.
4. File the heat pump connection policy for the 2027 fix.

Ends on: the heat pump connection policy, about 10,900 sustained customer interruptions (the overload category's rise).
Golden: the restoration switching revision, about 8,700 sustained customer interruptions from cold-load re-trips, 5.7
times the next change; the heat pump policy's own service transformer trips are about 1,500.

## Stump sentence

A solver who books fiscal 2026's sustained interruptions by cause files the heat pump connection policy, at about 10,900
customer interruptions, because the overload category rose most once heat pumps were connected without a load study,
and costs the switching revision at nothing because it only shortens restorations; the step that lands them there is
never pairing each overload trip with the same section's restoration minutes earlier, which shows most of the winter's
rise as cold-load re-trips after one-step re-energisation began and puts the fix on the switching revision.

## Three rules

- Task type: grid-reliability-outage-analysis (Energy Systems and Utilities), which serves Root-Cause Analysis in the
  taxonomy; the call names which change raised the members' sustained interruptions.
- Domain test: the deciding quantity is the sustained customer interruptions (IEEE 1366, major event days excluded) that
  cold load pickup re-trips added once sections were re-energised in one step: the field counts interruptions by
  device, cause and restoration, and the physics of lost load diversity after an hour or more in frost (two to four
  times the diversified load against a pickup near twice peak) is what makes a restoration set off the next
  interruption.
- Swap: "which of five changes cost the most re-admissions, when a discharge practice sent patients home in one step"
  keeps a sentence but loses the decisive object: there is no relay pickup, no load diversity and no minutes-long
  re-trip on the same device for the pairing to find; the call stands only on the distribution system's own physics
  and record.
- Layer 1: an outage management extract logged in local time across the daylight saving changes, with multi-step
  restorations in a separate step table (the control centre's own system); momentary operations under five minutes in
  the same device log (the SCADA feed); five years of daily SAIDI whose first two years come from the retired outage
  system in another layout (the 2023 migration); a section and device register re-keyed in a GIS migration with a
  crosswalk (engineering); heat pump rebate connections keyed by service address and meter (member services); weather
  from an airport station in UTC hours (the national weather service); nothing placed to be caught.
- Layer 2: estimand_identification; the choice that flips the call is the comparison that costs the switching revision:
  its interruptions are the re-trips its one-step restorations set off, counted by pairing each trip with the same
  section's restoration minutes before and netting the staged-era rate, not its filed effect on restoration minutes.
- Decisive step: attributing the winter's overload interruptions between new heat pump load and cold load pickup by
  pairing each trip with the section's own preceding restoration, which shows the restoration practice, not the load,
  set most of them off.
- Not semantics: every field reads right as it stands: the re-trips are correctly coded overload (the protection did
  trip on overload), the switching revision is correctly described as made to shorten restoration times (it did
  shorten them), and the heat pump register is correct; a solver who reads all of it correctly still books the overload rise to
  the heat pumps, because the relation that moves it is between rows, not in any field.
- Not rule application: no filed rule pairs a trip with the restoration before it or says that a restoration can cause
  an interruption; the board policy files only the WHAT, and executing it with every natural operationalisation (the
  overload category's rise, each change's scope across its date, the scope inside electric heating bands, the system
  residual) costs the switching revision at nil and files the heat pump policy (10,928, 1,676 and 1,014 on the shipped
  draw; the prototype's 20 redraws named the policy or animal guards, never the revision). The enumerated family of
  costings for the revision spreads from nil (every route that skips the pairing) to 8,700; the standing family, the
  21 pairing variants the WHAT and the data leave defensible (windows of 5 to 30 minutes, qualifying outages of any
  length to an hour, with or without the frost condition, either staged era, netted or not), spreads 0 on the shipped
  draw (every one prints 8,700, the staged era holding no re-trip) and never changes the call; what rules the skipping
  routes out is quiet: only the restoration step table and the minutes between rows of one section show it.
- Analyst test: a strong analyst who reads every field and the policy correctly books fiscal 2026's sustained
  interruptions by cause, sees the overload category rise most after heat pumps were connected without a load study,
  files the heat pump connection policy (Ends on: the heat pump connection policy, about 10,900 sustained customer
  interruptions, the overload category's rise) and costs the switching revision at nothing because it only shortens
  restorations.
- Estimand: the cooperative's reliability work plan policy (a board policy in the pack, section on costing changes)
  files population (the members), outcome (sustained customer interruptions under IEEE 1366, major event days
  excluded), window (12 months to 30 September 2026), unit (customer interruptions) and comparison (the year with the
  change against the same year without it, everything else as it was); the review table files each change's in-place
  date and scope.
- No decoy: nothing is planted to be caught: no copied block, hidden rule, memo, draft, briefing or stakeholder figure
  carries the wrong answer; the review lists five real changes with their dates and scopes and ranks none of them.
- No certified replay: the method is not hidden and recovered by reproducing certified or published figures; no
  published figure in the pack is reproduced only by the golden.
- Lesson: an interruption can be caused by the restoration of the one before it, so a change to restoration practice
  can add interruptions while its own measure (restoration minutes) improves; no build on file teaches that a change
  whose stated effect is on durations is costed on counts by pairing each failure with the same unit's return minutes
  before (the corpus's restoration and re-trip lines are Layer 1 realism in task129).

## Survivor anatomy

- Actor: the deciding property is a relation between two rows of one section in the outage record (a trip that begins
  within minutes of the same section's restoration after an hour or more off in frost); no file carries a re-trip
  flag, a parent-interruption key or a cold-load cause code, and the cause the record gives (overload) is right.
- Link: the pairing is a within-section, across-time comparison the field's method never asks for (IEEE 1366 counts
  interruptions by cause and device and never relates one interruption to the restoration before it); no key joins
  a trip to its predecessor and no sentence in the pack invites it.
- Reflex: the field's method at rung 0, the year's IEEE 1366 customer interruptions by cause with each change costed on
  its mechanism and scope, files the heat pump connection policy (Ends on) and costs the switching revision at nil.
- Back-test: the textbook route validates: the overload category rises after the policy's date and in the winter's
  frost, the heat pump register's connections by month track the overload trips' months, and every cause category's
  change reconciles to the year's total change.
- Second use: every file the decisive step reads sits in the pack for its own reason: the outage extract is the
  year's interruption record every costing reads; its restoration step table carries the restoration minutes the
  switching revision is costed on by default; the hourly weather serves the cold-day costing of the heat pump policy
  and the terminations; the section register carries members for every figure and the momentary ask.
- Shock: the movement the step recovers reads as ordinary explained movement: overload interruptions rising in a cold
  winter after heat pumps were connected without a load study is the story the review already tells; no unit leads
  every statistic and the switching revision touches every section.
- Pins: the board policy files the WHAT (members; unplanned sustained customer interruptions counted as the outage
  management system records them, IEEE 1366 major event days excluded; the review year; the year with the change
  against the same year without it); the review table files each change's date and scope and describes the switching
  revision only as the control centre's record does (the template revised to shorten restoration times); member
  services' rebate terms and the connection policy file what a connection replaces and what a load study checks. No
  filed sentence names re-trips, cold load, staging or a pairing, and deleting any one of them leaves the call forced.

## Readability screen

The screen takes two readers: the strong generalist, and the reader who knows cold load pickup and asks what the
switching revision did. The review's line says only that the template was revised to shorten restoration times; what
it did is visible in the restoration step table (qualifying restorations closed in two to four steps before 1 December,
in one after), and the old practice's purpose is stated nowhere, because the control centre's record does not state
it. The cold-load-aware reader must open the step table, see the steps disappear on long outages in frost, connect
that to the overload trips and pair them: three moves from the text, not one query.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the cause category's rise, each change on its own mechanism | the review table names each scope and mechanism | cause code column | yes, the field's method | none | no | yes | no | readable |
| R1 the heat pump policy on its own sections against the rest | none | heat pump register | yes | none | no | no | no | readable |
| R2 the same comparison inside bands of electric heating share | none | section register's electric heat members | partly | none | no | no | no | readable |
| R3 for the generalist: pairing each trip with the same section's restoration minutes before, net of the staged-era rate (decisive) | no sentence names it | no column or key marks it | no: IEEE 1366 never relates interruptions | no control scores it | no: the battery dedupes and converts, it does not pair | no: a sort, a lag within section and a count | no: the extract, its step table and the weather are read by other costings | silent |
| R3 for the cold-load-aware reader (decisive) | no: the revision's line states no content and no purpose | no: the step table shows steps, not why | not from the text: the reflex fires only after the step table is opened and read against the overload trips | none | no | no | no | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a sustained customer interruption | each interruption record in the outage extract, its customers interrupted, five minutes or longer | a trip within minutes of restoration merged into the interruption before it | the switching revision's cost falls and the heat pump policy files | the policy's words: interruptions are counted as the outage management system records them, one record one interruption |
| SF2 | major event days excluded | IEEE 1366 2.5 beta on the five fiscal years before the review year (threshold 15.5 SAIDI minutes) | no exclusion; the review year's own days in the threshold | same call (no exclusion: 8,700 against 1,520) | asserted: no paired re-trip on a day within 25 per cent of the threshold |
| SF3 | unplanned | outage records other than planned work | planned switching included | same call | planned work sits in its own register; asserted inert |
| SF4 | the review year | 1 October 2025 to 30 September 2026, local time | calendar 2026; UTC days | same call | the policy's dates; asserted: no paired trip within a day of either boundary |
| SF5 | would not have occurred, everything else as it was | the staged-era re-trip rate per qualifying restoration netted from the revision's re-trips | no netting; another staged era; the rate without the frost condition | same figure (C1: the staged era of the shipped draw holds no re-trip, so all 21 variants print 8,700) | asserted over every reading |
| SF6 | each change's in-place date | the review table's date | the first day of the month after | same call (animal guards and risers from the month after: 702 and 671 or less) | the review table; asserted |
| SF7 | the heat pump policy's scope | services connected under the waiver, after each connection, through the rebate register's service transformer | every rebate connection on the register | same figure (1,520 against 1,520) | asserted over both scopes |
| SF8 | customers interrupted | the record's own count | members on the section or transformer from the register | same figure: the two agree on every record of the year | asserted |
| SF9 | cost to the nearest 100 | each change's figure rounded once | rounded per month then summed | same call | the prompt's rounding sentence; every figure asserted mid-bin |
| SF10 | the heat pump policy's cost, argument (i): the connections added the electric heating load whose diversity the pickup lost | re-trips are the revision's: the rebate goes only to homes already heated by electric resistance, so the load lost its diversity whether or not a heat pump came | re-trips on sections with a waiver connection booked to the policy | same call: 23 per cent of the re-trips sit there; booked to the policy the revision leads 6,691 to 3,529, and in 20 of 20 redraws | member services' rebate terms (eligibility); asserted: re-trip rate per qualifying restoration equal with and without a connection over 20 redraws (mean difference -1.9 points, sd 8.4), the share a minority, the booked margin |
| SF11 | the heat pump policy's cost, argument (ii): a load study would have reinforced the section so a one-step pickup would not trip | a load study checks the service transformer and secondary serving the member, never the section's protection | re-trips on connected sections booked to the waived load studies | same call (as SF10) | the rebate terms' connection clause, which a literal reading executes as the transformer replay; asserted as SF10 |
| SF12 | each rival's cost | a replay of its recorded facts: the 2026 list's sites, the 2025 list's risers, the units fitted from 1 February, the waiver's transformers | the cause category's rise year on year | same call: no rival's category rise reaches the revision's cost | asserted (`checks.py`, the ladder rungs and the residual) |
| SF13 | the heat pump policy's cost, by a comparison | the interruptions a load study would have prevented: the trips of the transformers it checks | the policy's sections against the rest, all overload trips (1,700 bin) or inside electric-heat bands (1,000 bin) | same call; every estimator of the transformer trips a study checks holds 1,500 (replay 1,520, every rebate connection 1,520, scope on transformer trips 1,533, the banded scope on transformer trips in the same bin) and the gap holds 7,200 under each | the rebate terms' load study clause read with the extract's device_type at face value: a section device's trip is not one a study checks; asserted, with the other rivals netted by their own records (guarded sites 694, replaced risers none, the old supplier's infant failures 82), each in its bin |

## Ladder

- Rungs, each named by the change it files, on the generator's shipped draw (`checks.py` prints each; the prototype's 20
  redraws in `## Draw`, screen 3, gave the same order of rungs):
  - R0, the overload category's rise booked to the heat pump policy, each other change on its own list or units: the
    heat pump policy at 10,928 against animal guards 702; the switching revision nil.
  - R1, the heat pump policy on its own sections against sections without a waiver connection, overloads year on year:
    the policy at 1,676, still first among the costed changes; the switching revision nil.
  - R2, the same comparison inside bands of electric heating share: the policy at 1,014, first; the revision nil.
  - R3 (decisive), pairing each trip with the same section's restoration minutes earlier, net of the staged-era rate:
    the switching revision 8,700 against the heat pump policy's own transformer trips 1,520, animal guards 702, riser
    terminations 671 and the transformer supplier 118.
- Margins: R0's winner over its runner-up about 15 times; the golden over the runner-up 5.7 times; R1 and R2 lead by
  1.4 to 2.4 times on a single scope comparison that the redraws show is noisy (the prototype's R1 named animal guards in
  11 of 20).
- Position: the switching revision is last on R0 to R2 (no scope or category of its own to rise) and first on R3; only
  R3 reverses it.
- Dominance and grid: each rung's winner clears its runner-up by the 1.15 floor on the shipped draw (asserted); no cell
  ties.
- Who stays on the default: a strong generalist stops at R0 (the category story reconciles, and connections by month
  track the overload months) or at R1 or R2 (each a satisfying scope comparison naming the same policy). A reader who
  costs the heat pump policy by its own mechanism (transformer trips the waived study would have caught) is left with a
  section-level overload rise of about 9,000 that no costed change explains; that reader either books it to the colder
  winter (and files the heat pump policy at 1,520 or, on R1, the scope comparison) or recognises one-step pickup in frost
  and pairs the trips. Only that last move reaches R3, so at least one of the top two stays off the call unless both
  are cold-load aware and both read the restoration record against the overload trips.
- Pricing sequence: (1) the residue the WHAT leaves is how the year without the switching revision is estimated, a
  method; (2) the move needs about 8,700 of the year's customer interruptions and the affected population (every
  restoration after an hour or more in frost) produces it; (3) the one-group-by route (interruptions by cause) is the
  default and lands the heat pump policy; (4) the golden has no sampling spread across its licensed variants on the
  shipped draw (21 of 21 identical) against a lead of 7,180; (5) the lever is a count, not a variance; (6) no variance
  correction; (7) the paired subset prints the revision's re-trips exactly, which is the step itself and no shipped
  column; (8) reflex sweep as code: R0 to R2 and the system residual land elsewhere (`checks.py`).
- Shape 01 sum: five changes with their costs 5; call, runner-up and gap 3; the ranked chart with its parts (five bars,
  their labels, the order) 6; three files 3: 17 before the asks; the asks add 40 (16 district-quarter figures, 12 months
  of hours, 12 of pay): 57.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the cooperative's members on every section | filed in the policy; C1 |
| 2 Unit of account | a customer interruption, one member one interruption record | filed; SF1, SF8 |
| 3 Attribution window | the review year, local dates | filed; C1, nothing paired near a boundary |
| 4 As-of dating | each record's own start | filed by the extract; C1 |
| 5 Version basis | the extract as closed for the review | one extract shipped; C1 |
| 6 Denominator | none for the call (a count) | C1 |
| 7 Weighting | customers interrupted per record | filed; C1 |
| 8 Window length | the pairing window | C1: 5 to 30 minutes print one figure, asserted |
| 9 Boundary inclusivity | trips at exactly the window edge | C1: none within a minute of any edge, asserted |
| 10 Rounding path | each change's figure once, to the nearest 100 | prompt; asserted mid-bin |
| 11 Tie-break | none needed | C4: the winner leads by 5.7 times |
| 12 Maturity and censoring | the year is closed at extract | C1 |
| 13 Order of operations | major event days out before the pairing | C1: no paired trip on a near-threshold day |
| 14 Row order | sorting by section and start | C1, asserted over shuffles |
| 15 Duplicate resolution | an interruption once | C1: the extract carries no duplicate interruption |
| 16 Identity normalisation | sections across the GIS re-keying | the register's crosswalk; C4 |
| 17 Netting against gross | the staged-era rate | C1: the staged era holds no re-trip; SF5 |
| 18 Dimensional units | customers interrupted, minutes | C1 |
| 19 Code and status semantics | cause codes are read as given and decide nothing on the golden path | C1 |
| 20 Integerisation | whole interruptions | C1 |
| 21 Clause scope | the policy's costing clause covers every change alike | filed |
| 22 Forward window contents | none: the quantity is the closed year | C1 |

## Literal reader

Executed word for word: the policy counts each outage record's customers interrupted in the review year outside the
major event days and asks, per change, for the interruptions that would not have occurred without it; the review
table gives each change's date and scope. Read literally with every natural operationalisation (scope across date,
cause category year on year, system residual) the heat pump policy or animal guards file and the switching revision
costs nil, because nothing filed says a restoration can cause an interruption; the golden is reached only by
estimating the year without the revision from the records, which the WHAT requires and no sentence performs. The two
readings that would book the revision's re-trips to the heat pump policy (SF10, SF11) are closed by member services'
rebate terms and the connection policy, and are inert at the call besides (19 of 20). Every SF row is closed or
convergent and asserted.

## Oracles

- The heat pump register's monthly connections against the overload trips' months: confirms the default (both rise
  from November) and ties on the golden too (the policy's own transformer trips also rise); never an oracle.
- The year's total change in customer interruptions: reconciles under every route (each route only splits it).
- Weather: frost explains both the policy's transformer trips and the re-trips, so it confirms the default and the
  golden alike.
- No published or certified figure in the pack is reproduced by one route only.

## Ask sheet

- Ask A, momentary interruption events per member (IEEE 1366 MAIFIe) for each district in each quarter of the review
  year, to two decimals (16 figures). H18: the review's district scorecards carry it beside the sustained indices; the
  call does not turn on it. Files: the SCADA historian's reclosing operations (UTC, one row per trip or close), the
  register's reclosing devices and sections, the outage extract (lockouts, and the feeder each record was on).
  Primary P1 (D6 grain, held family): in the North and Lakes districts the substation breakers' relays trip with a line
  recloser for the same fault, so the members beyond the recloser see two devices operate in the same second and have
  one momentary event; nothing joins the two devices' rows but the register's feeder and the time. Every merge a member
  sees is that same-second pair: no two devices reach one member between one second and five minutes apart (asserted),
  so one event per member within five minutes and one event per fault print the same 16 figures. Counting each
  device's sequences against its members double counts them. Primary P2 (D2 version, another family, its figure block
  the Prairie and River districts before July): sections were moved between feeders on 1 June 2026; the register states
  its feeders as at 30 September 2026 inside the workbook, and the outage extract records each move as an XFER record on
  the section's earlier feeder, so each section's feeder before June is a recorded fact read at face value. Hazards: sequences ending in lockout (sustained, in the outage
  extract), the UTC clock against the local quarter boundaries, several trips and closes in one sequence (the
  five-minute rule). Pin test: the sentence names the measure, the district and the quarter; the devices sit in which
  rows are one event for a member and which feeder a section was on.
- Ask B, crew callout hours and callout pay for restoration work in each month of the review year, hours to the nearest
  hour and pay to the nearest dollar (24 figures). H18: the switching revision's own case is crew time. Files: the
  timekeeping export (overtime and callout entries), the agreement's Article 14 and Schedule A, the outage extract.
  Primary P1 (D6 grain): a crew moved from one outage to the next has a row per job, the rows a few minutes apart for the
  drive; the agreement's callout runs from the start of work to release with travel included and carries one two-hour
  minimum, so the rows of a chain are one callout. Primary P2 (D8, a recorded date for the event date, another family,
  its block every month's hours and pay): the foreman enters the crew's time each Monday for the week before (Article
  14.4), so the export carries each job's start and end time of day and the entry's timestamp, and no work date; the
  date a job was worked is its work order's outage in the outage extract. Dating rows by their entry moves every
  callout of a month's last days into the next month. Every field is read at face value: order_type OUTAGE is the
  restoration work, entered_at is the entry. Hazards: double time on the agreement's holidays, an entry corrected by a
  later entry for the same employee, order and start, a duplicate the foreman rejected, after-hours service calls and
  capital callouts that restored nobody. Pin test: the sentence names hours, pay, restoration work and the month; the
  devices sit in which rows are one callout and which day each row was worked.
- Main population zero-counts: no SCADA operation and no timekeeping row is in the main call's population (unplanned
  sustained records in the outage extract), and no outage record is changed by either ask's device (asserted).
- Cracker sheet (the careful solver lands the call, runs the battery, groups each device's operations by the
  five-minute rule, drops lockouts by each device's final state, applies the latest correction, drops rejected entries
  and pays holidays at double time):

| Ask | Cracker | Full includer | No repair | Mirror |
|---|---|---|---|---|
| A momentary events | miss | miss | miss | miss |
| B crew callouts | miss | miss | miss | miss |

- Measured on the cut pack: the cracker keeps 2 of 16 on A and 0 of 24 on B; the full includer (each member once across
  devices, each employee's chained jobs one callout) keeps 10 of 16 on A (P2's block missed) and 0 of 24 on B (rows dated
  by their Monday entry), under two fifths of the ask figures; the no-repair reader keeps 1 of 40.
- Pair ceiling: 31.2 (cracker on the call 47.8, mirror off it 14.8).
- Mirror leakage: 5.0 per cent of ask weight.
- Measured by: generator/ceiling.py on the cut pack.

## Tried and rejected

- The seed's world (2026-11-03, at the draw): a wind turbine's five faults read against the turbine's own healthy-year
  power curve is task187's insight (a unit's shortfall against the right reference curve at matched conditions) in the
  same room (turbines, nacelle anemometers, icing, yaw, pitch); its client domain (Supply Chain & Logistics) reaches
  Root-Cause only through interpretability, ruled a backdrop for an operations world at task129 v1; energy's
  Root-Cause cell is task129's and the room is task187's. Moved before any harness.
- Screened on paper at the draw (2026-11-03), each set aside before any code, with the reason:
  - an epidemiology composition draw (a borough's excess admissions carried by care home residents): task401's cell
    and insight, registered the same day;
  - drug co-prescription (the "triple whammy") behind excess acute kidney injury: the coarse exposure (any of the
    three drugs) contains the fine one, so the attributable count is the same either way, and naming the target
    population makes the step a filed rule;
  - a point-of-care assay's missed RSV corrected from quality-control re-tests: two-phase verification weighted by the
    testing rate is spent (task267, task120, task124, task228, task274's screen) and a verification report names the
    sensitivity;
  - stated cancellation reasons corrected from a save desk's probed reasons: the "true" reason is another opinion, so
    either the plan names it (a rule) or the reading forks, and it re-attributes losses away from a filed label
    (task13);
  - fluoridated water supply zones behind child dental extractions: an outcome scaling with a property of each case's
    surroundings is task129's form;
  - preventer supply lapsing over the school holidays behind September asthma admissions: a per-event state rebuilt
    from consecutive records is task121's device and close to its insight;
  - stock against flow (length-biased) census sampling: task182's driver;
  - an inspection window's onset: task487;
  - competing exits in a cumulative incidence: task133's lesson;
  - immortal time in a churn driver model: the decisive step is the exposure clock, which a pin would name;
  - net of recovered or deferred demand: either a count of listed recoveries (a rule) or a window the WHAT names;
  - a production line's restart tail booked as speed loss: no client domain with a Root-Cause task type holds it;
  - a fraud model's false declines from a holdout: precision moving with the base rate is task446's insight;
  - a mystery-shop routine blind to evenings: the swap test reads the same in any branch network.
- The first harness world (2026-11-03, stage 2): agency cover allocated by a wait threshold of 16 weeks, so short and
  long waiters both reached it; the cross-tab of wait band by first practitioner separated the wait from the cover at
  once (101 long waiters with employed therapists recovering at 51.6 per cent, 142 short waiters with agency cover), a
  cheap route to A. Redrawn so the cover takes the backlog (waits of 18 weeks and over) and one long-standing locum
  carries ordinary short-wait courses.
- Waits rising through the year with the cover ending in early November (2026-11-03, stage 2): about 400 long waiters
  started after the cover ended and went to employed therapists, the same cheap separation. Redrawn so the backlog
  forms between January and June 2025 and the initiative's funding ends on 19 December 2025 with final blocks booked
  to that date.
- A waiting-list leaving hazard of 0.85 per cent a week (2026-11-03, stage 2): with the longer backlog, C's own cost
  (the extra leavers) exceeded A's at three seeds of six. Lowered to 0.30 per cent.
- Telephone-first step 2 at 2.2 points of recovery with a small video and face-to-face group (2026-11-03, stage 2):
  B's reads swung from -25 to 102 by method, within reach of A. Cut to 0.4 points with a larger comparison group.
- G4 and then G6 as the decisive generator (2026-11-03, stage 2): refused by `check` (test.same_driver against task232
  v2, whose interviewer change between waves identifies a roster effect, task121 v6, task129 v2 and task243;
  test.same_puzzle_older against task144, task228, task265 and task68). G9 stays decisive.
- A flat list-leaving hazard of 0.6 per cent a week (2026-11-03, stage 2, risk 1): the backlog's leavers split across
  2024-25 and 2025-26, so C's extra leavers fell to 12 and C with leavers came within 1.07 times of coarse A. Replaced by
  0.3 per cent a week to 18 weeks and 2 per cent after (C's leavers 56.1).
- Monday-start agency bookings (2026-11-03, stage 2): lapses bunched on single Sundays (130 to 215 broken courses a date)
  and the long-wait employed cell rose to 21. Starts drawn over working days.
- A first wave started over six weeks with a first renewal of 0.2 (2026-11-03, stage 2, risk 3): 524 of 762 breaks fell in
  August and early endings jumped to 313 in September as agency therapists in post fell from 38 to 16, the readability
  screen firing on the monthly chart. Spread over ten weeks with a first renewal of 0.4.
- No referral surge (2026-11-03, stage 2): step 3 starts fell to 0.4 of normal from December 2024 to April 2025 while 40
  employed therapists stayed in post, an idle-staff tell. A winter rise in referrals forms the backlog instead.
- Loose clearance without longest-first order (2026-11-03, stage 2): broken courses halved, A fell to 110 to 160 and rivals
  came within 1.2 times at some seeds. Longest-first kept.
- The long-standing locum taking 5 per cent of ordinary step 3 patients: about 40 sessions a week. Cut to 2.5 per cent.
- Seeds 7 and 14 (2026-11-03, stage 2): seed 14's longest waiters recovered best inside the backlog cohort (30 to 33 weeks
  38.6 per cent against 20.7 at 18 to 21 weeks), a dose-response a careful solver would read against the wait; seed 7 sat
  on an earlier world. Seed 402 shipped: no gradient inside the cohort, every filed-comparison estimator mid-bin.
- Ask devices dropped at stage 2: carried-across digital patients (discovery and remedy one act); the digital beginners,
  the over-18-week counts and the agency cover's November and December (no device reaches them); three agency therapists
  booked after the backlog cleared, with no patients (an idle booking reads as generated), left out of the pack.
- Ask devices one-sided against the full includer (2026-11-03, stage 2, the coordinator's precut read): an off-call
  response that handles every device banks the ask weight. The timesheet corrections were made two-sided at the route
  change of 1 August 2025 (filed in the register), and the digital ask was moved to span the January 2026 content release.
  Its first form, which only added sections, let the cracker's whole-export inference keep January and February (2 of 6),
  so the release also retires a section of module 3, and both structures now count against any single inference. The
  waiting list ask stays one-sided (its WHAT cannot change mid-year without a filed rule the cracker would execute).
- Architecture 1, the Talking Therapies world (2026-11-03, stage 4): the determinism judge returned NOT_DETERMINISTIC,
  SEND_BACK. Gate H rule_application: the plan filed each change's cost as expected minus actual recoveries read from the
  year's other referrals at the same step, largest wins, so a solver executing it literally with any-contact exposure
  costs every change directly and lands A at 249 (naive comparator 267, golden 257, all 250 to the nearest 50; only the
  last-clinician exposure, 222, rounds to 200); the funnel walk filing C was not the route a rule-following solver takes.
  Gate F low to moderate. Gate C forks: A's exposure (any contact 250, last clinician 200); C had no filed in-place date
  or wait threshold and tied A at 248 to 257 on the same patients. Ask 4 (agency hours and cost by month) needed
  conventions no file stated (a dropped 2023 booking, the later of two portal timesheets before 1 August and summing
  after, catch-up lumps spread over unclaimed weeks, working-day allocation; week-commencing allocation moves June by
  about 1,200 hours). The reader's realism tells: a parquet footer naming pyarrow with a pandas schema block; near-even
  splits (step 50.2 against 49.8, three referral sources at 12.7, 12.7 and 12.5, authorisers in near-even thirds);
  near-uniform hourly slots; every timesheet Authorised, submitted on the 1st; every group course six sessions; UUIDs
  that are not valid version 4; whole-minute event times. The world is spent; re-rooted at architecture 2 in another
  world, dataset and shell (the dead shell: how-many, our, pptx+xlsx).
- Architecture 2 draw, screened and set aside before registering (2026-11-03): childhood immunisation call and recall
  with invitations to superseded addresses (the age-cohort windows made the WHAT fork and families' moves gave the
  lever, but a records-system change would have been the call); bowel screening with a new call-and-recall system's
  stale addresses accumulating from go-live (proto, eight draws: D 537 to 592 against 146; set aside because the
  cause is a two-system cutover, which the house rule bars from the call, and its ramp from the data's first month is a
  trend a cracker dates to the go-live); the same with an annual address reload (a sawtooth that resets each April,
  leaving an unexplained jump up at April 2025 on the changes' date); a one-off cohort of changes made during a
  pre-migration freeze (no time signature, but again a system cutover as the call); masking the winner's
  differences in differences by a concurrent benefit in the same localities (a balance that reads as planted); a
  universal winner tied with a universal decoy on the same date (every literal costing ties them, a tie the judge
  could call a fork). The shared registration service is an organisational change, not a two-system cutover, its
  loss is steady from its first months, and the year-on-year comparison gives it nothing.
- Pending cohort at a four-month mean wait and 240,000 people (proto3): D 129 to 148 screens against E 145, screen 1
  failed. Region doubled (less noise, same ratios), mean wait six months, E at 0.8 and A at 0.5 points (the low end of
  their published ranges): D 370 to 395 against 230 (proto4).
- Architecture 2 at honest levels (2026-11-03, stage 2, before any generator): the queue re-anchored to what the
  published accounts of a shared primary care support service support (NAO HC 632, 17 May 2018, and PAC HC 698, 2018:
  half a million patient registration letters in backlog and practitioners waiting months, with no wait distribution
  published), a first-in-first-out backlog of address changes at a mean of 15 weeks with 15 per cent applied quickly,
  85 per cent of within-region movers asking 0 to 8 weeks after moving, a kit to the address left completing at 0.30
  of normal (about half of movers redirect mail and fewer on low incomes, Citizens Advice, Left behind), a 1.5-point
  mobility barrier (no published barrier for colorectal screening): D costs the fifth 157 screens (sd 8, 20 redraws)
  against E's true 145 at 0.5 points (1.08 times) and 116 at 0.4 (1.36); every rival is costed by a difference of
  completion rates whose sampling sd is 120 to 280 screens (E within the year 120, E against 2024-25 169, A's
  localities 148, C on settled kits 202, the April residual 280), as large as D's lead, so D's lowest golden variant
  clears every rival estimator by 1.15 in 1 of 20 redraws, 3 of 20 with every lever at its honest edge (a 20-week mean
  wait, 0.20, everyone asking, E and A at 0.3 points, D 279) and 4 of 20 at the old six-month exponential; the
  shape-07 grid's fifteen rival cells carry the same noise, and the earlier screens had compared D with the rivals'
  true costs, never with their estimators. The movers-in-12-months row (46, sd 18) and the returned-kit row (26) stayed
  below E. Architecture 2 is spent before any data was cut (scratch t402/a2 proto6.py and p6_sd.py).
- Architecture 3 draw, screened and set aside before registering (2026-11-03, scratch t402/a3): a distribution network
  operator's licence area (utility_or_infrastructure BLOCKs on `ban.org_family` against task401, and a city-owned utility
  carries the same key in the corpus, task118); latent excavation damage on a cooperative's direct-buried cable after a
  contract locator or a fiber partner's bores (proto1 to proto3: the golden 2,300 to 2,550 customer interruptions
  against the default's paused aged-cable programme, every rival under 1,000, but it is task173's insight in other
  nouns, work on or over a unit raising its failures in the weeks after, and its per-crossing damage lever has no
  published level); lateral fuse upsizing and recloser miscoordination (already screened and set aside in task129's and
  task398's notes: an event study finds it and the device codes name it); a component batch reaching depots as old
  stock runs out (dilution preserves totals, so a vintage difference finds it, and the onset is task400's staggered one);
  product-funnel mechanisms (a per-address rate limit on shared mobile addresses, saved drafts lost at releases, a card
  issuer's authentication flow, a redesign's novelty decay: each readable by a segmentation or a lookup join, and the
  drafts in flight at a release are architecture 2's pending window again); pull-forward after a promotion (task463's
  buyers stocking up); education and pollution mechanisms (a phonics sequence against the check's items, ozone
  titration read through total oxidant, a source's impact set by the river's flow when it discharges: noisy, reflexive
  or task202's insight).
- Cold load pickup, first calibration (2026-11-03, proto_clpu and proto_clpu2): heat pump overload trips at 0.9 per unit
  of new heat pump share and animal contacts up 55 per cent made both rivals as large as the winner (107,000 and 18,000
  against 77,000 customer interruptions), and with both years equally stormy the system residual after the scoped
  changes picked the restoration rule in 3 of 10 redraws. Recalibrated: heat pump overloads 0.012, animal rise 12 per
  cent, terminations 80 per cent, the comparison year stormier (9 per cent of days against 3), heat pumps going to
  members already heating electrically; the residual then names the rule in 0 of 20 on the default's comparisons.
- Cold load pickup with re-trips 1 to 8 minutes after restoration and qualifying outages from 30 minutes (proto_clpu3
  run 1): the narrow pairing window (5 minutes) and the 60-minute qualifying variant fell to 0.92 times the best rival
  (15 of 20 redraws at 1.5). Re-trips now follow within 4 minutes and qualify from an hour in frost, as the physics has
  it; every variant clears 1.5 times in 20 of 20.
- Heat pumps on 55 per cent of the electrically heated sections (proto_clpu4 at the draw's coupling, 2026-11-03, the
  coordinator's joint re-trip review): 53 per cent of the golden's re-trips sat on connected sections, and booked to the
  heat pump policy the switching change kept first in only 1 of 20 redraws. Moved to a quarter of those sections: 25 per
  cent on the prototype (19 of 20), 23 per cent on the generator (20 of 20).
- The review describing the change as "the staged cold-weather restoration rule withdrawn" (the draw's wording, set
  aside at stage 2 on the coordinator's readability review): it names the old practice's protective purpose, which hands
  a cold-load-aware reader the suspicion in one line. The review now records what the control centre's own revision log
  says, the switching template revised to shorten restoration times, and the step table shows what it did.
- The rivals costed in the golden by their cause categories' rises or scope comparisons (the prototype's estimators,
  2026-11-03): each left its figure an open method (the termination and animal rises swung with the winter by several
  hundred), a Gate C fork on every graded rival. Each rival is now a replay of recorded facts: the list's sites or risers,
  the units fitted, the waiver's transformers.
- Stepped pickup at 0.8 per cent of the one-step re-trip lever (generator, 2026-11-03): the staged era carried a few
  re-trips and the netting variants (staged era span, frost condition, netted or not) spread 120 to 650 across draws,
  wider than a nearest-100 bin. At 0.3 per cent the staged era of most draws holds none; the shipped draw is one of the
  six in 150 whose 21 variants print one figure with every graded figure mid-bin, which agrees with the design (stepped
  pickup prevents the re-trips) rather than arguing against it.
- An ask device on the month a callout's hours fall in (callouts across a month end split at midnight): a reading of
  "hours in each month", so a fork, not a device; the generator keeps every restoration callout inside one month. The
  historian's per-shot logging after a firmware upgrade was also set aside: the five-minute rule the careful solver
  applies already repairs it.
- Ask B's second device as capital-order rows inside an outage callout counted as restoration work (stage 2, 2026-11-03,
  the coordinator's review of the precut hand-back, measured on the cut pack): the golden kept 348 of 415 approved
  CAPITAL rows because each sat within 15 minutes of an OUTAGE row, overriding the export's own order_type with nothing
  filed to say restoration work is defined by when supply returns; taken at face value all 24 figures moved (hours 14
  to 95 a month, pay 319 to 1,600), a competing defensible answer for a literal judge. The replacements are now booked
  to the outage's order, and the second device is the work date the export does not carry (D8, Monday entry).
