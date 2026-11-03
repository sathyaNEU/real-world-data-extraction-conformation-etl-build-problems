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
without a load study (1 November 2025, sections with such connections); the control centre's staged cold-weather
restoration rule withdrawn, every section now picked up in one switching step (1 December 2025, all restorations); the
pre-winter infrared inspection of underground terminations skipped (from 1 October 2025, underground sections); the
animal guard programme ended (1 January 2026, its 2026 site list); a new pole-top transformer supplier (1 February
2026, transformers fitted after).

What nothing in the pack says: after an hour or more without supply in hard frost every electric heating load on a
section calls at once, so a section re-energised in one step draws two to four times its diversified load and its
protection trips again within minutes. Under the staged rule the control centre picked such sections up in pieces and
re-trips were rare; from 1 December they are common, each one a second sustained interruption of the same members,
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
  acquisition: the restoration the rule's purpose measures is the acquisition, whether the restored supply held is the
  outcome scored); G14 (conditioned yield) behind it, the staged-era re-trip rate applying only to restorations after an
  hour or more in frost.
- Decision, quantity and tense: pick one of five; the quantity is interruptions in a closed review year (12 months to
  30 September 2026), the decision forward (the 2027 work plan's one fix). Retrospective quantity by design: the board
  policy costs each change on the year just closed, and the forward reading only widens the winner's lead (the rule
  stays withdrawn and every winter repeats it).
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
  natural comparison (nothing staggered: the rule went at once); task401 a1, composition by closures (none); task401 a2,
  a dated shock meeting each unit's sensitive phase (no phase: the condition is the outage's own length and the day's
  frost); task401 a3, expectation against delivery (none); task402 a1, cases broken off when a fixed-term actor's
  assignment lapses (no actor); task402 a2, a level loss from a change in force through both compared years (the rule
  went inside the year and its harm is a rise, not a level); task187, a unit's shortfall against a reference curve (no
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

### The four go/no-go screens (prototype on the clean truth, 20 redraws each, before the card was registered)

Scratch: `t402/a3/proto_clpu3.py` (event timestamps to the minute, re-trips found by pairing) and its outputs
`screen_central.txt` and `screen_low.txt`. A redraw re-draws every interruption, connection and re-trip; the realised
weather of the two years is the world's own and stays fixed. Levels, each with its source or its stated absence:

- Interruptions: about 155,000 sustained customer interruptions a year on 136,000 members, SAIFI about 1.1 outside major
  event days, inside the range US distribution utilities report to the EIA (Form EIA-861 reliability data, 2021-2024,
  SAIFI without major event days about 1.0 to 1.4) and the range public power and cooperative benchmarks show.
- Cold load pickup: after an hour or more without supply in sub-freezing weather a section's load at re-energisation runs
  two to four times its diversified level and decays over tens of minutes (the IEEE Power System Relaying Committee's
  working group reports on cold load pickup and the papers behind them, from McDonald, Bruning and Mahieu, IEEE
  Transactions on Power Apparatus and Systems, 1979, onward); phase overcurrent pickup is set near twice peak load, so a
  one-step pickup of a heavily electric-heated section exceeds it; sectionalised (staged) restoration is the practice
  those sources describe for it. The re-trip probability itself has no published figure: it is set to rise with the
  outage's length past an hour, the day's frost below minus 3 C and the section's electric heating share, to at most 0.5
  per qualifying restoration without staging and 0.02 with it, and the call is measured at 0.3 as well (below).
- Electric heat: electric heating shares of 2 to 90 per cent by feeder (median about a third), the spread of a Minnesota
  cooperative with off-peak and dual-fuel electric heat programmes; heat pumps under the rebate go to members already
  heating electrically (the rebate's purpose is to displace resistance heat).
- Rivals: true overload trips from new heat pump load on the coldest days, termination failures on underground sections
  in frost, animal contacts on overhead sections, transformer infant failures; none has a published rate for this
  cooperative and each is set small, under a third of the winner.

1. **Realistic levels and the lever against the rivals' estimates.** The golden's cost of the restoration rule (pairing
   each trip with the same section's restoration minutes before, net of the staged-era re-trip rate) is about 8,700
   customer interruptions (sd 1,450) against the best rival estimate's 1,200 to 2,600 (heat pump overloads 1,229 sd
   562; animal guards 1,778 sd 310; terminations 1,248 sd 464; transformers 831 sd 562). Every golden variant beats the
   best rival estimate by 1.5 times or more in **20 of 20** redraws, worst ratio **3.07**. At the low edge of the
   unpublished re-trip lever (0.3 at the worst exposure) the winner falls to about 4,800 and every variant still clears
   1.5 times in 17 of 20 (worst 0.86); the shipped level is the central 0.5. Mid-bin is asserted on the generator.
2. **The golden's own method holds the call.** Eighteen variants of the golden (a pairing window of 5, 10, 20 or 30
   minutes after the restoration; a qualifying outage of any length, 15, 30 or 60 minutes or more; with and without a
   frost condition; with and without netting the staged-era rate) give 8,500 to 9,100 on average and each is the winner
   in every redraw; no specification choice moves the call, because a cold-load re-trip follows its restoration within
   four minutes and a qualifying restoration is an hour or more in frost by the physics, so the windows agree.
3. **No easy completion.** The decisive variable (the minutes between a trip and the same section's last restoration)
   is not one the default path brings in: the default reads interruptions by cause and month and costs each change on
   its scope. Once it is in hand the cost is a count of paired trips less the staged-era rate, no functional form. The
   cracker's flexible versions of the default rungs land elsewhere: the heat pump policy costed on its own sections'
   overload trips (a difference in differences against sections without heat pumps) names it in 19 of 20 (animal guards
   once); costed on the overload category's whole rise, 20 of 20; costed on peak-hour overloads only, which deflates it,
   the call goes to animal guards (6), terminations (2), transformers (1) or back to heat pumps (9), and to the
   restoration rule in 1 of 20 only through a weather-noisy residual, never through its own mechanism.
4. **Literal execution.** The board policy files the WHAT (population: the cooperative's members; outcome: sustained
   customer interruptions under IEEE 1366, major event days excluded; window: the 12 months to 30 September 2026;
   comparison: the year with the change against the year without it, everything else as it was) and the review table
   files each change's in-place date and scope. Executed literally with every natural operationalisation (each scope
   against the rest across the in-place date; each cause category against the year before; the system's residual after
   the scoped changes), the call lands on the heat pump policy in 19 or 20 of 20 and on animal guards otherwise, never
   on the restoration rule, whose filed effect is on restoration minutes and whose literal cost on interruptions is
   nil. The golden needs a step the WHAT never asks for: pairing each trip with the same section's restoration minutes
   earlier. Every candidate has its own in-place date and scope, so none ties the golden on the same interruptions.

## Default path

1. Read the outage management extract for fiscal 2025 and fiscal 2026 (local time; momentary operations under five
   minutes excluded), drop major event days by the IEEE 1366 2.5 beta method on five years of daily SAIDI, and count
   sustained customer interruptions by cause and month.
2. Overload trips rose most, in the winter, and on sections where members connected heat pumps under the rebate since
   1 November 2025; animal contacts, termination failures and transformer failures rose less.
3. Cost each change on its scope across its in-place date: the heat pump policy on its sections' overload trips against
   sections without heat pump connections; terminations on underground sections; animal guards on the programme's 2026
   list; the transformer supplier on units fitted after 1 February; the restoration rule on restoration minutes, where
   it cut SAIDI, and on interruptions at nothing, since restoring a section in one step changes how long members wait,
   not whether they lose supply.
4. File the heat pump connection policy for the 2027 fix.

Ends on: the heat pump connection policy, about 8,800 sustained customer interruptions in fiscal 2026 on the default's
scope comparison.
Golden: the staged cold-weather restoration rule's withdrawal, about 8,700 sustained customer interruptions from
cold-load re-trips, more than three times the next change; the heat pump policy's own overload trips are about 1,200.

## Stump sentence

A solver who books fiscal 2026's sustained interruptions by cause files the heat pump connection policy, at about 8,800
customer interruptions, because overload trips rose most and on the sections where heat pumps were added, and costs the
withdrawn restoration rule at nothing because it only shortens outages; the step that lands them there is never pairing
each overload trip with the same section's restoration minutes earlier, which shows most of the winter's rise as
cold-load re-trips after the rule went and puts the fix on the restoration rule.

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
- Layer 2: estimand_identification; the choice that flips the call is the comparison that costs the restoration rule:
  its interruptions are the re-trips its one-step restorations set off, counted by pairing each trip with the same
  section's restoration minutes before and netting the staged-era rate, not its filed effect on restoration minutes.
- Decisive step: attributing the winter's overload interruptions between new heat pump load and cold load pickup by
  pairing each trip with the section's own preceding restoration, which shows the restoration practice, not the load,
  set most of them off.
- Not semantics: every field reads right as it stands: the re-trips are correctly coded overload (the protection did
  trip on overload), the restoration rule's withdrawal is correctly described as a change to how sections are picked
  up, and the heat pump register is correct; a solver who reads all of it correctly still books the overload rise to
  the heat pumps, because the relation that moves it is between rows, not in any field.
- Not rule application: no filed rule pairs a trip with the restoration before it or says that a restoration can cause
  an interruption; the board policy files only the WHAT, and executing it with every natural operationalisation (each
  change's scope across its date, each cause category year on year, the system residual) costs the restoration rule at
  nil and files the heat pump policy (19 or 20 of 20 redraws, animal guards otherwise). The licensed family that takes
  the step (pairing windows of 5 to 30 minutes, qualifying outages of any length to an hour or more, with or without a
  frost condition or the staged-era netting) spreads 8,500 to 9,100 customer interruptions and never changes the call;
  the family that skips it spreads 1,200 to 10,000 on the heat pump policy and never reaches the rule.
- Analyst test: a strong analyst who reads every field and the policy correctly books fiscal 2026's sustained
  interruptions by cause, sees overload trips rise most on the sections given heat pumps, files the heat pump connection
  policy (Ends on: the heat pump connection policy, about 8,800 customer interruptions on its scope comparison) and
  costs the restoration rule at nothing because it only shortens outages.
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
