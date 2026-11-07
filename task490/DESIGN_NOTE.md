# task490 design note

Architecture 1, drawn 2026-11-07. Which summit the Coldmere Canals Trust's 2027/28 back-pumping scheme serves:
the summit whose two summit locks drew the most water from its summit pound by filling their chambers over the
2026 boating season (1 April to 31 October), rebuilt from the lock counters' camera records, the lock-keepers'
log and the lock register into one ledger of chamber cycles. The number is fixed in Data Extraction &
Conformation (ETL) by `START_HERE.md`; its seed (ET47, Land Registry price-paid delta files) supplied the
objective only, for the reasons in `## Tried and rejected`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task490.json`, architecture v1, registered 2026-11-07 (re-registered the same evening after the shape and forcing-event redraw below) |
| Client domain / task type | General Statistics & Data Science (`general-statistics-data-science`), `data-integration-record-linkage-entity-resolution` (serves ETL): three record systems at six summit locks (two camera firmware layouts, a typed-up keepers' log, a lock register in two units) integrated into one return at the grain that draws water |
| Objective | Data Extraction & Conformation: the season's boat movements at every summit lock conformed into the trust's lockage return (summit lock by day: boats up, boats down, water drawn), and each summit's lockage read off it |
| Decision | which summit the 2027/28 back-pumping scheme serves, the one whose summit locks drew the most water from the summit pound over the 2026 season (`pick_one_of_n`). A retrospective quantity for a forward call: the pump is sited and sized on the last complete season's lockage because the 2027 season's boats are not yet on the water; nothing is forecast, so the tag stays ETL |
| Shape | 15: fields conformed to one schema. The criteria come from the conformed return (each summit lock's water, each summit's lockage, the counter records left out by reason) and the water budget the paper sets beside it; the arithmetic is in `## Ask sheet` |
| Gap / pattern / generators | `objective` (the counters report boat movements correctly, and the decision is scored on water); pattern `none`; `G2` decisive (one unit of the decided thing is a chamber filling, the record's unit is a boat movement, and no key bridges them), `G1` (a boat charged at a lockful, rung 0), `G19` (the return's conformance, depth only) |
| Gate G | `etl_conformance`: the conformed lockage return is judged against the programme paper's lockage definition |
| Strategy | `grain_or_unit`; Layer 2 family `field_method`; pattern `own:lock-chamber-state-replayed-through-chamber-cycles` |
| Forum, forcing event, org family | `trustees_or_governors` (the trustees' capital meeting on 10 December 2026 approves the site), `vote_or_meeting` (that meeting; the money for one scheme was set in the 2026/27 plan), `nonprofit_or_charity` (a waterways charity that owns and runs a regional canal network) |
| Role | the trust's water resources planner, preparing the siting paper (`capacity_planner`) |
| Context artifact | `operations_log`: the Tilsey volunteer lock-keepers' log |
| Calibration | none: the chamber's physics closes the reconstruction, and no sensor records a filling |
| Personas | Katy Wilkinson (water resources planner, the golden's author), Elaine Freeman (head of water management, author of the programme paper), Keith Rahman (Tilsey lock-keeper team leader), Kim Hussain (volunteer lock-keeper coordinator, the log's keeper), Louis Carey (asset engineer, the 2025 survey and the reservoir register), Gillian Walsh (counter programme officer, the site export), from `guard.py names --geo England --seed 490`; Nicole Holmes from the same draw was dropped on `people.first`; the keepers' initials in the log (KR, KH, PM, BD, DA, RJ) are the same draw's Keith Rahman, Kim Hussain, Patricia Murray, Billy Davis, Declan Adams and Rita Johnston |
| Fiction as-of date | 2026-11-06 (the planner's working date; the counter export is taken on 3 November 2026 and the keepers' log typed up on 4 November) |
| Guard | `guard.py check` on the first draft BLOCKed `test.same_puzzle_older` against task192 v4 and task311 (objective, G2, `pick_one_of_n`); both are differentiated on the card. After registering, task315 (registered two minutes earlier) put shape 07 and `budget_or_appropriation` in the window, so the shape was redrawn to 15 and the forcing event to the trustees' meeting, and the card re-registered. The register-time check is WARN only, answered below |

**The world.** The Coldmere Canals Trust (an invented waterways charity in the English West Midlands) owns and
runs a regional network of narrow and broad canals. Three of its lines cross a watershed at a summit pound fed by
reservoirs: Kelsby summit (narrow locks, the hire base at Kelsby Wharf on the summit pound and the Kelsby Ring
holiday route), Harnock summit (broad locks on the old barge route) and Tilsey summit (narrow locks at the head of
the Tilsey flight, with volunteer lock-keepers at weekends and through the school holidays). A summit pound loses
water each time one of the two locks that rise to it is filled. The programme paper files the WHAT (3.1 to 3.4):
the scheme serves the summit whose summit locks drew the most water from the summit pound by filling their chambers
over the 2026 season, clock time at the lock, a lockful being the 2025 chamber survey's chamber volume, the record
of lock use being the counter export and, on the keepers' days at Tilsey, their log. The pack: the counter
network's movement export (46,423 rows, two firmware layouts), its site configuration, the keepers' log, the lock
register (2025 survey and the 1951 schedule), the navigation notices, the programme paper, the reservoir returns,
the Coldmere outlet telemetry, the reservoir register extract, the abstraction agreements, their meter readings,
the works orders, and two distractors.

**Why the world moved.** ET47 asks which local market drove a regional mean-price fall, read from monthly
price-paid delta files appended to a yearly base. Every decisive step it offers is a field reading (the delta
files' add, change and delete records, the Category B transfer flag), a field method a strong solver takes as
written (a mix-adjusted or repeat-sales index), or a family banned or spent (mix against price is composition,
splitting the fall by market is decomposition, banned against task211). The number keeps its objective and moves
to a physical record system, where the ETL pincer does not close: what the counters record is a boat, what drains
the summit is a chamber filling, and the arithmetic between them is the lock's own.

**The data-native sentence.** A broad chamber takes two narrowboats side by side, so on the Harnock line two boats
recorded under a minute apart going the same way are one filling, and a summit's water follows the order and pairing
of its boats through each chamber rather than their number.

**Priced on a clean-truth prototype before registering (five seeds), then on the generator's clean truth.** A
lockful a boat files Harnock (2,448.0 Ml against Tilsey's 1,895.0), the chamber replayed boat by boat files Harnock
(1,843.0 against Kelsby's 1,468.8), cycles charged a lockful each without the chamber's state file Tilsey (1,876.6),
and the replay through chamber cycles files Kelsby (1,460.8 against Tilsey's 1,186.5 and Harnock's 1,140.8).
Kelsby's holiday ring sends most crews up Kelsby Top Lock and down Wharf Lock, so its chambers are left set against
the next boat and it draws about 0.82 of a lockful a boat; Tilsey's busy flight is worked in turn (about 0.63);
Harnock's broad chambers carry two boats a cycle for 57 per cent of its boats (about 0.47 of a lockful a boat, each
lockful 1.3 to 1.8 times a narrow one).

**Window and WARN answers.** `three_rules.strategy_risk`: the analyst test runs on the clean truth (`checks.py`
R3a), where every field is read and no rule is filed; the easy routes fail on the chamber's grain and state, not on a
reading. `overuse.objective`: the objective is fixed by the number. `repeat.decision` and `repeat.question_form`:
the scheme serves one summit, so the call is one of a set and the question asks where; the asks carry the
quantities. `people.first`: Nicole replaced from the same draw.

## Three rules

- **Task type:** `data-integration-record-linkage-entity-resolution` in General Statistics & Data Science, serving
  Data Extraction & Conformation: three record systems integrated into the trust's lockage return at the grain that
  draws water.
- **Domain test:** the deciding quantity is lockage, the water a summit pound gives up to fill the chambers of the
  locks that rise to it, which canal water managers reckon from the lock's own physics: a boat going up always needs
  the chamber filled from the summit, and a boat going down needs it filled only when the last boat left it empty.
- **Swap:** "Kelsby gets the pump because its chambers, worked by a one-way holiday ring and never shared, are filled
  for most boats": put a ward's patients or a feeder's faults in place of boats and chambers and the sentence loses
  the chamber whose state makes one boat's water depend on the boat before it and on the boat beside it.
- **Layer 1:** the camera firmware change in June (4.2.1 writes the outstation's UK clock as dd/mm/yyyy and UP or
  DOWN; 5.0.3 writes UTC with a Z and A>B or B>A on the camera axis, both in the site export); repeat reads when a
  boat holds under the camera (the same plate seconds apart); canoes and paddleboards logged as unpowered craft
  though they portage round the lock; unreadable plates left blank and visiting boats under visitor pass numbers;
  the Tilsey Top camera out from 3 to 23 August, covered by the keepers' log in local time with boat names and plate
  numbers, overlapping the camera on the days it failed and returned; chamber dimensions in feet and inches on the
  1951 schedule against metres and lockfuls on the 2025 survey. Each is neutral for the call (`checks.py` R2 and SF9
  to SF11).
- **Layer 2:** `field_method`, the lock's own reckoning done right: the water a summit gives up is a count of chamber
  fillings, each set by the cycle before it, at the grain of the chamber cycle rather than the boat.
- **Decisive step:** seeing that two boats recorded within a minute or two going the same way at one lock went
  through in one cycle, so the chamber is filled once for the pair, and carrying the chamber's state (full or empty)
  through each lock's cycles in order, so a cycle going down draws water only when the cycle before it went down.
- **Not semantics:** the easy routes read every field right: direction, class, plate and time mean what the export
  and the site sheet say, and the boat-by-boat replay uses them exactly; what makes it wrong is taking a record for a
  filling, which no field, code, unit or definition says either way, and on the clean truth, with every record read
  correctly, it still files Harnock.
- **Not rule application:** no filed rule says how fillings are counted, how boats share a chamber or what state a
  chamber is in; the programme paper files only what is counted (the summit locks, the season, water drawn by filling
  their chambers, the survey's lockful), so executing every stated sentence leaves the reckoning open, and the
  records' own timing (pairs within 1.1 minutes of each other, separate cycles at least 14 minutes apart) settles it.
- **Analyst test:** a strong analyst who cleans the counter records, stitches the keepers' log into the camera
  outage, reads the lock register correctly and replays each summit lock's chamber one boat at a time names Harnock
  at 1,843.0 Ml, because two boats that share a broad chamber are two records and one filling.
- **Estimand:** programme paper 3.1 to 3.4 (`backpumping_programme_2027-28.pdf`): the summit whose two summit locks
  (named in 3.2) drew the most water from the summit pound by filling their chambers over 1 April to 31 October 2026,
  clock time at the lock, in megalitres, a lockful being the 2025 chamber survey's chamber volume.
- **No decoy:** nothing is planted to be caught: no document argues for Harnock, names a lockful a boat, a pairing
  or a chamber state; the hire base's convoys and the broad locks' shared cycles are how the lines are worked, and
  the records hold them as they happened.
- **No certified replay:** no published or certified figure reproduces under the golden or under the easy route; no
  lockage figure, filling count or per-boat factor ships, and the reservoir releases exceed every route's lockage at
  every summit, so the water budget cannot score a reading.
- **Lesson:** a counter counts what passes its camera, and the water a lock uses is set by the chamber, so the
  conformed return has to be built at the grain of the chamber's cycles and carry the chamber's state between them.

## Survivor anatomy

- **Actor:** the chamber, full or empty, and its cycle, one boat or two: no column holds either; the export carries
  detections with time, direction, class and plate.
- **Link:** consecutive records at one lock, read across rows of the movement export: two plates under a minute
  apart going the same way are one cycle, and each cycle's water turns on the direction of the one before; no key,
  cycle number or sentence invites the comparison.
- **Reflex:** the field's reflexes sit at rungs 0 and 1: a lockful a boat (Harnock, 2,448.0 Ml) and the
  boat-by-boat reckoning of a lock worked in turn (Harnock, 1,843.0 Ml).
- **Back-test:** none ships: no paddle counter or chamber level logger records a filling, and the summit water
  balance cannot score a reading because each summit's reservoir supply exceeds every route's lockage there and its
  losses are unknown.
- **Second use:** the movement export, the site sheet, the keepers' log, the lock register and the notices are read
  by every route that counts water, the easy ones included; no file ships for the decisive step alone.
- **Shock:** Kelsby tops no simple statistic of the pack: it has the fewest boats (12,872 against Harnock's 13,506
  and Tilsey's 18,697), smaller lockfuls than Harnock, the smallest reservoir supply, and it is third at a lockful a
  boat and second boat by boat.
- **Pins:** the WHAT is filed once, in the programme paper's 3.1 to 3.4 in the trust's own form; no filed sentence
  names a pair, a shared chamber, a cycle, a chamber's state or a per-boat factor, and deleting any pin leaves the
  reckoning open rather than forced.

## Default path

1. Read the counter export, converting the June firmware's UTC to clock time and A>B to up through the site sheet.
2. Drop unpowered craft and repeat reads of one plate; take the Tilsey keepers' log entries for the camera outage.
3. Join each summit lock to its 2025 survey lockful.
4. Replay each lock's chamber one boat at a time: a boat going up fills it, a boat going down fills it when the boat
   before left it empty.
5. Sum each summit's water and name the largest.

- **Ends on:** Harnock, 1,843.0 Ml (Kelsby 1,468.8, Tilsey 1,204.9); a lockful a boat gives Harnock 2,448.0.
- **Golden:** Kelsby, 1,460.8 Ml (Tilsey 1,186.5, Harnock 1,140.8, a lead of 274.3).

## Stump sentence

A competent analyst replays each summit lock's chamber one boat at a time, or charges a lockful a boat, and names
Harnock at 1,843.0 Ml, whose broad chambers hold the most water; the step that lands it there is treating two boats
that share a broad chamber as two fillings, which hides that Kelsby, whose holiday ring sends most crews up one summit
lock and down the other so each chamber is left set against the next boat, draws the most at 1,460.8 Ml.

## Readability screen

Tests: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second use. The reflex row is
enumerated from the field's own reckonings of lockage (a lockful a boat, half a lockful for locks worked in turn,
the boat-by-boat chamber reckoning, the counter's count), never from the rungs beneath.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 a lockful a boat (Harnock 2,448.0) | no | the boat count | a reflex | none | no | product | yes | readable |
| 1 the chamber replayed boat by boat (Harnock 1,843.0) | no | direction column | the textbook reckoning | none | no | one pass | yes | readable |
| side cycles at a lockful each, no state (Tilsey 1,876.6) | no | none | no | none | no | grouping | yes | readable |
| 2 (decisive) the chamber replayed through its cycles (Kelsby 1,460.8) | no sentence names a pair, a cycle or a state | no column holds a cycle or a filling | not a reflex: the field's reflexes are rungs 0 and 1 | no paddle counter, logger or control scores a filling | the battery drops repeat reads of one plate and never merges two plates into one cycle | a state carried through grouped records | every file it reads is read by rung 1 | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | summit locks | the two locks rising to each summit pound, as 3.2 names them | other flight locks | none ship in the export | programme 3.2; asserted |
| SF2 | a lockful | the 2025 survey's chamber volume | the 1951 schedule's feet and inches | same call (1,458.1 against 1,182.1 and 1,137.6) | programme 3.3; same call, asserted |
| SF3 | the season | 1 April to 31 October 2026, clock time at the lock | UTC days | same call; the export holds the season only | programme 3.1; asserted |
| SF4 | water drawn | fillings times the lockful, in megalitres | boats times the lockful | the easy route, not a reading | programme 3.1 ("by filling their chambers") |
| SF5 | whose boats | every boat, hire, private or visiting | visitors left out | same call | programme 3.1; same call, asserted |
| SF6 | one chamber cycle | same-direction records at one lock under a few minutes apart | any threshold from 1.6 to 11 minutes | the same fillings at every threshold | C1: no same-direction records fall 1.6 to 11 minutes apart (asserted) |
| SF7 | Steward's Lock after its stoppage | left empty on reopening at 17:00 on 29 May | carried over from 11 May | same call | notice CCT-N-2026-0189; same call, asserted |
| SF8 | a chamber overnight | holds its water | drains | same call | survey: every summit lock falls under 25 mm in 12 hours (asserted) |
| SF9 | unpowered craft | portage, not a lock use | counted as boats | same call | the class column; same call, asserted |
| SF10 | repeat reads | the same plate seconds apart is one boat | two boats | the same fillings either way | C1, asserted |
| SF11 | the Tilsey outage | the keepers' log entries the camera did not record | the outage left empty | same call | programme 3.4; same call, asserted |
| SF12 | a tie | none | | Kelsby by 274.3 Ml | same call |
| SF13 | the most water | the total for the season | water per boat | same call | programme 3.1 ("the most water"); same call |
| SF14 | rounding | megalitres to one decimal | unrounded | same call | prompt; same call |

## Ladder

| Rung | Route | Names | Its figure (Ml) | Kelsby | Margin |
|---|---|---|---|---|---|
| 0 | a lockful a boat | Harnock | 2,448.0 | 1,780.5, third | 1.29 over Tilsey's 1,895.0 |
| 1 | the chamber replayed boat by boat | Harnock | 1,843.0 | 1,468.8, second | 1.25 over Kelsby |
| side | cycles at a lockful each, no state | Tilsey | 1,876.6 | 1,772.5, second | 1.06 over Kelsby |
| 2 | the chamber replayed through its cycles | Kelsby | 1,460.8 | | 1.23 over Tilsey's 1,186.5 |

Dominance (`checks.py`): the decisive step takes 694.1 Ml more off Harnock than off Kelsby against Harnock's carried
lead of 374.1 on rung 1, 1.86 times it. The side route is a partial repair (grouping without the state) and is not a
rung a solver reaches from the default path; it is asserted wrong.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the six summit locks named in programme 3.2 | filed; the export holds no other lock (SF1) |
| 2 Unit of account | the chamber filling, at the survey's lockful | filed WHAT (3.1, 3.3); the reckoning forced by the records' timing (SF6) |
| 3 Attribution window | a filling counts in the season when its cycle runs in it | C1: the export holds 1 April to 31 October only (SF3) |
| 4 As-of dating | the season as recorded; the export of 3 November | the export is final |
| 5 Version basis | the 2025 survey's lockful | filed, 3.3 (SF2 same call) |
| 6 Denominator | none: a total | SF13 |
| 7 Weighting | none: every filling a lockful | filed, 3.3 |
| 8 Window length | 214 days | filed, 3.1 |
| 9 Boundary inclusivity | 1 April 00:00 to 31 October 24:00 | filed; no boat moves near midnight |
| 10 Rounding path | lockfuls summed in cubic metres, rounded once to 0.1 Ml | the prompt; every figure at least 0.0079 Ml inside its bin (asserted) |
| 11 Tie-break | not needed | SF12 |
| 12 Maturity and censoring | the season is closed | n/a, asserted inert |
| 13 Order of operations | clean, stitch, group, replay | C1: every order of the cleaning steps gives the same fillings |
| 14 Row order | the replay runs in time order at each lock | C1: no two records at one lock share a second with opposite directions |
| 15 Duplicate resolution | the same plate seconds apart is one boat | SF10, same fillings |
| 16 Identity normalisation | camera site code to asset through the site export; keepers' lock names to assets | the site export; the log's Top and Engine |
| 17 Netting against gross | none | n/a |
| 18 Dimensional units | cubic metres, megalitres | units in the column names |
| 19 Code and status semantics | direction and class codes per firmware | the site export states both layouts |
| 20 Integerisation | whole fillings | C1 |
| 21 Clause scope | 3.4's log covers the keepers' days at Tilsey | filed |
| 22 Forward window contents | none: the season is closed | n/a |

## Literal reader

Executed word for word, programme 3.1 asks for the water each summit pound gave up to fill its summit locks'
chambers; the pack's only record of the chambers' use is the counter's detections, so the literal reader has to
decide when a chamber was filled, and the lock's physics (a boat rises only in a full chamber filled from above, a
boat descends only from a full chamber) makes that a function of the order of the cycles. A reader who executes it
literally on the records finds same-direction detections at one lock either within 1.1 minutes of each other or at least 14
minutes apart and never between, while the survey gives each chamber a filling time of 6.5 to 9 minutes, so a pair
seconds apart cannot have been two fillings. The literal reading is therefore the golden's, the easy answer comes
from an easy method on the same literal estimand (a filling per boat, or a lockful a boat), and every convention the
computation needs is closed in the fork table, by a quotable sentence or as the same call.

## Oracles

None ships. No paddle counter, chamber level logger or lockage figure scores a reading of the movements, and no
document states a per-boat factor. The reservoir releases a solver might set against lockage exceed every route's
lockage at every summit (Kelsby received 2,246.9 Ml against 1,780.5 at a lockful a boat; Harnock 4,462.5 against
2,448.0; Tilsey 3,487.2 against 1,895.0) and the summits' losses are unknown, so the water budget confirms no route.

## Ask sheet

Planning weights 38 / 7 / 55. The call side carries the call, the runner-up and the lead, each summit's lockage,
each summit lock's water and the two counts of counter records left out (14 criteria). The asks sit on files the
call never reads.

- **Ask S, the season's reservoir water: each reservoir's release and the water each summit received (7 figures,
  Ml to one decimal).** H18 home: the supply side of the summit water budget the programme paper's 4.1 sets beside
  the lockage, a measure every summit carries that the call does not turn on. Path: the keepers' returns (date,
  rate at 09:00, released, timed remarks), the Coldmere telemetry (period end in UTC, head, the outstation's flow),
  the reservoir register (the weir formula, the crest plates and their dates, Fox Bridge's two notches and crests),
  the programme paper 4.2. Primary 1 (D2, a label stored before a silent switch): Coldmere's crest plate went from
  0.75 m to 0.60 m at 10:30 UTC on 16 June and the outstation kept computing its flow on the old plate until early
  August, so the flow column over-reads; only the head re-rated on the plate in service is right. Primary 2 (D8, a
  recorded date for the event date): Lower Kelsby's keeper books each release in full on the day the valve is shut,
  so the season's first and last releases straddle the season's ends on their booking lines. Third device (a reflex
  repair wrong): Fox Bridge divides Coldmere's water by the pool's head over two notches whose crests differ by
  0.060 m, so a split by notch width is wrong in every interval. Hazards: Upper Kelsby releases into Lower Kelsby;
  the keepers' water day ends at 09:00 and the valve was opened on 31 March afternoon; the telemetry is in UTC.
  Pin test: 4.2 files where water is reckoned (the outlets, the season's clock hours) and that Fox Bridge divides it;
  no sentence names the plate's rating, the booking day or the head. Stops: the flow column (Coldmere 7,373.8), the
  Released column summed (Lower Kelsby 2,215.7), the width split (Harnock 4,337.5, Tilsey 4,126.8), the golden
  (Upper Kelsby 527.2, Lower Kelsby 2,246.9, Coldmere 6,859.1, Tilsey 1,090.6; received Kelsby 2,246.9, Harnock
  4,462.5, Tilsey 3,487.2). Realism: an outstation's rating table updated weeks after a plate change, and a keeper
  who books a release when the valve is shut, are how such records come to be.
- **Ask A, abstraction: each agreement's metered take between its March and October month-end readings and each
  summit's total (12 figures, whole cubic metres).** H18 home: the demand beside lockage on each summit (4.1, 4.3).
  Path: the agreements register (licence, point, current serial, dials), the meter readings (serial, point, date,
  reading), the works orders (completion notes). Primary (D4, absence evidenced in a file no habitual join reaches):
  four meters were exchanged in the season, the register shows only the new serial, the readings carry both serials
  at one point, and the removal and installation readings sit only in the works orders' completion notes, so chaining
  the two meters' month-end readings loses the take between the last old reading and the first new one. Hazards: the
  trout farm's five-dial meter rolls over four times; readings fall on the last working day. Stops: the chain without
  the works orders (KA/022 14,183, HA/019 19,609, HA/026 11,203, TA/011 22,099; totals Kelsby 50,771, Harnock
  498,639, Tilsey 52,682), the golden (KA/014 30,500, KA/022 17,790, KA/031 6,088, HA/007 467,827, HA/019 27,299,
  HA/026 12,904, TA/003 19,398, TA/011 24,099, TA/018 11,185; Kelsby 54,378, Harnock 508,030, Tilsey 54,682).
- **Main population zero-counts:** no ask file is read by the call (the returns, telemetry, register extract,
  agreements, readings and works orders), and deleting all six leaves the call and every call-side figure
  (asserted by construction: the lockage code opens none of them).
- **The full includer:** a response that re-rates Coldmere on the plate in service, divides it at Fox Bridge by the
  pool's head and spreads Lower Kelsby's bookings over their hours keeps ask S, and one that reads the works orders'
  exchange readings keeps ask A; each remedy is a reconstruction across two files, never a filed rule.
- **Referee:** none; every ask figure is recomputed on `generator/verify.py`'s own path.

| Ask figure | Cracker (remarks read, flow column summed, Released column summed, width split, meters chained by point) | Golden | Cracker |
|---|---|---|---|
| S: release Lower Kelsby | 2,215.7 | 2,246.9 | miss |
| S: release Coldmere | 7,373.8 | 6,859.1 | miss |
| S: received Kelsby | 2,215.7 | 2,246.9 | miss |
| S: received Harnock | 4,337.5 | 4,462.5 | miss |
| S: received Tilsey | 4,126.8 | 3,487.2 | miss |
| A: take KA/022 | 14,183 | 17,790 | miss |
| A: take HA/019 | 19,609 | 27,299 | miss |
| A: take HA/026 | 11,203 | 12,904 | miss |
| A: take TA/011 | 22,099 | 24,099 | miss |
| A: totals by summit | 50,771; 498,639; 52,682 | 54,378; 508,030; 54,682 | miss |

The cracker keeps Upper Kelsby and Tilsey on ask S (2 of 7) and the five unexchanged agreements on ask A (5 of 12).

- **Pair ceiling:** 49.0 (the cracker 65.3 on the call with 7 of 19 ask figures; the mirror 32.7 at rung 1 with the
  two record counts of the call side and the same ask handling).
- **Mirror leakage:** 36.8 per cent of the ask weight.
- **Measured by:** `generator/ceiling.py`, run on the cut pack.

## Gate answers

- **Stage 3 gates on the hand-off cut.** `checks.py` 58 assertions, 0 failed (R1 to R3c, the ladder and
  dominance, SF1 to SF14, the H29 bounds, mess neutrality, the asks' devices measured as numbers, the input gates,
  the realism sweep, both PDFs read back with positive controls); `verify.py` 25 checks, 0 failed, reading only
  `target.zip` on its own parsers (movement export, site JSON, keepers' log, notices, lock register, reservoir
  returns, telemetry, both PDFs through pypdf, agreements, readings, works orders); two consecutive builds
  byte-identical (target.zip, the three goldens, figures.json, metadata.json); `figures_check.py` 55 of 55;
  `precut.py` 61 checks, 0 FAIL; `voice-check.py` PASS; `ceiling.py` pair 49.0, mirror 36.8 per cent; the
  producer-metadata audit clean on target/ and golden/.
- **Input gates.** 14 files in four formats (csv, json, pdf, xlsx); the movement export holds 46,423 rows;
  distractors declared in `metadata.json`: the boat licence register extract and the weekly reservoir storage.
- **`leak.py --asof 2026-11-06`: REVIEW, no LEAK.** The first run was LEAK on sweep 12: the programme paper
  repeated nine labels the data files use as headers (Date, Lock, Reservoir, asset, station, Summit pound and three
  first-row values). Fixed in the generator by relabelling at the source (the timetable's When, the register
  extract's Name, the survey sheet's Chamber survey 2025, the telemetry's site, the storage file's reservoir_name,
  the returns' Site, the log's Day and At, the survey's Lock name, the agreements' Pound); sweep 12 is now clean.
  The REVIEW lines, each harmless:
  - Sweep 3, lock and reservoir names beside decision words in the programme paper and the reservoir register: the
    paper's 3.2 lists every summit's two locks evenly as the population, and the register lists its reservoirs; no
    graded figure appears in any shipped file.
  - Sweep 3, the call's seventeen words in the programme paper: they are the paper's own (scheme, summit, summit
    locks, drew, water, filling, chambers); it names no summit as the site and carries no lockage figure.
  - Sweep 4 (ruled here, never handed to a reader): the stump-paragraph terms in the two PDFs are nouns of the world
    (chamber, filling, lockful, keepers, register, the summits' names); none of the decisive move's own words appears
    in any document or notice, asserted in `checks.py` R3c.
  - Sweep 6: none of the eight files ranks the summits on lockage: the agreements list licensed quantities, the site
    export firmware dates, the survey chamber dimensions, the notices closures, the register capacities, the returns
    and the storage file releases and storage.
  - Sweep 9: the boat licence register's expiry dates are licences running forward, and the 2026/27 winter works
    notices were issued on 21 and 22 October for works from November; both are records the trust holds on the
    export date.
- **`guard.py heart`: WARN** (three_rules.strategy_risk, repeat.decision, repeat.question_form, answered under
  `## Draw`; the older same-puzzle note differentiated against task192 v4 and task311); nearest driver text 0.08
  (task117). **`guard.py surface`:** two pairs promoted for adjudication and no hard tell (no shared invented name,
  byte-identical file or same-seed table): task211 on surface similarity 0.100 (the corpus top 1 percent, with no
  shared file name, sentence construction or name in its evidence) and task192 on the card's gap, decisive generator
  and decision type (objective, G2, `pick_one_of_n`), which the card already differentiates (192 groups a feeder's
  fault events by a shared measured signature to find one failing point; here two boats are one chamber cycle by the
  lock's physics and the decision turns on the chamber's state carried through the cycles). Gap `population` was
  priced as the alternative label and collides with three older builds (task187, task228 v5, task486 v1), so the card
  keeps `objective`. Both pairs are left for the author's adjudicated clone check. The personas in the cut pack are
  Elaine Freeman and Louis Carey, both drawn.
- **Open for the reader and the judge.** Whether the records' timing makes the shared cycle the literal reading for
  a reader who has never worked a broad lock (no same-direction pair at one lock falls between 1.1 and 14 minutes
  apart, against filling times of 6.5 to 9 minutes); whether the keepers' log stitch at the outage's edges is forced
  (plates are readable on every camera and log record within two hours of either edge); whether Fox Bridge's
  division (one pool level over two notches whose crests differ by 0.060 m) reads as forced by the register's
  formula; whether Lower Kelsby's booking on the shut day is found from its own rate column and remarks.

## Tried and rejected

- Seed ET47's world (which local market drove the regional mean-price fall, read from price-paid delta files): every decisive step is a field reading (the delta records' add, change and delete status, the Category B flag), a field method taken as written (mix-adjusted or repeat-sales index; repeat sales screened dead in task479 screen 13), or a family banned or spent (composition_mix, decomposition_attribution against task211); world moved, objective kept.
- Bounding suppressed cells of published tables from overlapping cross-tabulations: spent by task475, task465 and task201 at the draw.
- Administrative-world candidates in the remaining ETL cells (identity resolution, grain, time semantics in a register or claims world): the ETL pincer closes them, a correction input on file makes the step rule application and one absent fails Gate B; screened at the draw against task464 architecture 5's cell map and task476's screens.
- Bridge weigh-in-motion with coincident lorries on the span (each event's strain is the sum of every vehicle on it, and the routine reads it as one): the honest stump strategy is decomposition_attribution (one measured response split across coincident components), banned against task211, and labelling it other to pass the ban is a relabel; the probe card also hit test.same_driver against task461 and the older same puzzle against task194. Dropped at the draw.
- Shape 07 (a summit by month lockage grid) and a budget-round forcing event, as first registered: task315 registered two minutes earlier with both, so the shape moved to 15 (the conformed return) and the forcing event to the trustees' meeting.
- A chamber level logger at one Harnock lock as a back-test: it would hand the pairing to any solver that set its fillings beside the boats, so no sensor records a filling.
- Lower Kelsby's releases with each session's total repeated on every day line: the hygiene battery's repeated-total check finds it, so the keeper books each release once, on the day the valve is shut.
