# task201 design note

Energy Systems & Utilities, `grid-reliability-outage-analysis`, Anomaly Detection & Diagnostics
(task180 to task227, oviya13ya). Architecture v2, drawn 2026-10-18 after both genomics candidates were
screened to death at the draw (the append-only section at the foot of this note).

## Draw

**Card:** `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/wave5/task201/task201_card.json`
(this session does not register; the orchestrator files it). `guard.py check` verdict: WARN, one WARN,
answered below. Maximum driver similarity on file 0.07 (task37, task452).

**Pairing.** Energy Systems & Utilities / `grid-reliability-outage-analysis`, which serves Root-Cause
and Anomaly Detection in the client taxonomy. Objective Anomaly Detection & Diagnostics: the object is
a flagged exposure figure and the call separates a real concentration of exposure from an artefact of
how the records were timed. Shape **12**, drill-down to one leaf: the criteria come from each box's
piece at each of three levels. Decision type `pick_one_of_n` (the leaf), answer unit `named_option`.
Gate G `method_or_model_selection`. Strategy `maturity_censoring`: each interruption on a feeder
without line telemetry has a duration record that is a lower bound, censored at the moment somebody
reported it, and the censored opening is recovered from the parallel channel.

**World.** Poland, a fictional distribution system operator in the north-east, four branches
(Zanowiec, Pustrzyca, Grabownik, Nierzyca), PLN, `utility_or_infrastructure`, forced by
`season_or_peak` (the storm season's one remediation slot). Personas drawn with
`guard.py names --geo Poland --seed 201`: Arkadiusz Dudko, Karina Kurda, Cezary Wawszczyk, Lidia
Lalak. Geography unspent on the corpus (United States 50, United Kingdom 15, Canada 12, Australia 10,
Netherlands 4, Poland absent); task197, the lane's last energy build, used a Dutch world and is not
touched here.

**Reserved axes taken, and the three I could not take.** `shape` 12, `stump_strategy`
`maturity_censoring`, `gate_g` `method_or_model_selection`, `gap` `time`, `forum` `operations_desk`,
`forcing_event` `season_or_peak` and `org_family` `utility_or_infrastructure` are as reserved, and
`guard.py check` passes all of them. The reserved `role_family` `operations_director` was taken at the
draw and lost to a later registration; see the redraw paragraph below. `forum`
BLOCKed against task246 at the first probe and came free when the axis bans were narrowed to live
cards, so the reserved value is restored and re-probed clear. Two departures:

- `calibration_form` is `parallel_run_overlap`, not the reserved `retry_or_revision_log`. The organ
  the construction reads is the overlap between two detection channels running side by side on the
  instrumented feeders. A revision log was drafted and killed on the revelation screen: an operator
  who back-dates an interruption's start after the crew reports publishes the quantity the decisive
  step estimates, so a filter on the revised rows would return the answer rather than an
  approximation.
- The decisive generator is `G12`, absence of record against record of absence, not `G3`, record
  against operation. `G3` is the sharper label and it BLOCKed twice, before and after the gate change:
  task172 is live and carries gap `time`, `G3` and `method_or_model_selection`. `G12` is honest rather
  than merely passing: what is missing is not a record of a different thing, it is the absence of any
  record over the interval between the loss of supply and the first notification, and the naive route
  reads that absence as the absence of an interruption. `test.same_driver_older` then fires against
  task192 v2 and task445 v1, both differentiated on the card.

**Two axes redrawn at the end of stage 3.** `guard.py check` was clear at the draw and BLOCKed later,
because task190 (6) and task202 registered in between. `role_family` moves from `operations_director`
to `field_unit_lead`: the honester label, since one crew-week is settled at the branch's own operations
review and not by a company operations director. `context_artifact` moves from `filed_standard` to
`published_series`, which corrects a mislabel as well as clearing the ban, since PR-07 is the pack's
governing document (`dataset-generation` 8) and the context artifact is the concession's filed
reliability returns (`dataset-generation` 5), which answer another question correctly and rank nobody.
Neither change touches a shipped byte.

**WARNs answered.** `overuse.objective` and `overuse.gate_g`: this is an Anomaly Detection lane and
`method_or_model_selection` is the honest Gate G here, so both are the shape of the batch rather than of
this build. `repeat.question_form`: "which" is forced, because the call picks one section class of
twelve and a count, a gate or an amount would misdescribe it. `repeat.gate_g`: `method_or_model_selection` repeats task172, one of the last two
builds. Kept because it is the honest label (two defensible ways to time an interruption stand, and
the estimand pins which) and because the alternatives are untrue here:
`decomposition_attribution` would claim the movement is correctly reported, which is exactly what it
is not, and `confirm_surface_read` would claim the reported figure is right.

**Data-native sentence.** A fused rural spur serves two to nineteen scattered holdings and carries no
telemetry, so nothing in this operator's records marks the moment its supply failed; the dispatch
system's start time for it is the moment one of those few customers rang in, and the only measurement
of how long that takes is the feeders where the telemetry programme happened to land, whose sections
are 57 per cent town trunks and village stations that somebody notices in eight to seventeen minutes.

**Sources read, one line each.**

- `guard.py mechanisms --objective anomaly-detection` (32 builds). Nearest neighbours and the insight
  each spends: **task184** spends the event-hour as the unit of analysis where events are recorded with
  a window instead of a time, so its decisive move is the denominator rather than any estimate of the
  window's contents; **task190 arch v1** spends the stock of undetected cases a scarce reviewer meets,
  arrival rate times time unseen, a level at a selected unit; **task194** spends counts that crystallise
  after the period they belong to, with the lag measured by two vintages of one series; **task196**
  spends how many events of a partly captured kind happened, from the overlap of two capture channels;
  **task199** spends a rise in event frequency read against how much the watchers filed; **task182 v4**
  spends a length-bias correction on durations entering a record through snapshots; **task180 v1**
  spends events entering the record only above an instrument's noise floor. What they leave: nothing on
  the corpus estimates **the unrecorded opening of a duration**, and nothing measures a nuisance on a
  parallel channel whose own coverage is the reason the pooled value of that nuisance is wrong.
  task196's device (two channels seeing one event stream) is reused here re-skinned, which `stumping`
  Part 6 licenses; its driver (a capture rate for a count) is not.
- `guard.py slots --driver "<the card's driver>"`: the five slots it returns (task198, task182,
  task229, task194 and this one) match on ordinary vocabulary only (branch, event, interval, channel),
  and none of their notes carries an unrecorded opening of a duration. Checked by reading task182's
  architecture 4 line (an unobserved component of an observed total, source apportionment) and
  task198's (a lesser-of payment rule) rather than by the keyword count.
- `stumping` 1.2a, the dichotomy: the filed quantity is **unobserved**, so two estimators of one
  quantity can stand. Run below under `Estimand:`.
- `stumping` 1.2, the estimand pincer and the variance screen: the decisive step settles none of the
  five parts, and it moves the point estimate rather than an interval. Both run below under
  `## Ladder`.
- `stumping` 1.2, the designation determinacy screen: the golden's own estimator family returns one
  path over six forms, measured, and the crude route is measured against the leaf rather than against
  the branch. Both numbers are in `## Ladder`.
- `stumping` 1.6a, what survived: an unobserved quantity identified by a construction combining two
  files at different grains, whose inputs are varied enough that no sorted column reproduces it. This
  build's construction reads the device register (one grain) against the telemetry archive and the
  notification log (two others).
- `dataset-generation` 7, the revelation screen: the subset the mechanic bound exactly is the
  telemetered set, and that subset is the **default path** rather than the answer, which is the safe
  configuration.
- `determinism-check` 1, the five parts: filed to the letter in procedure PR-07, with the estimator of
  the censored opening left open and forced by the data.
- `guide-to-prompt/references/shapes/12-drill-down-to-one-leaf.md`: the shape's own hard seam is mix
  against rate, which is `composition_mix` and spent; this build takes the shape's criteria structure
  and its greedy level-ordered drill, and puts its own difficulty under it.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, with every field
read correctly, every filed rule applied and every key normalised.

1. Read both dispatch exports, `awarie_oms_2026-10-01_2026-11-07.csv` (legacy layout) and
   `awarie_oms_2026-11-01_2026-11-15.csv` (current layout); rename the renamed columns and notice the
   seven-day overlap, de-duplicating on the interruption id: 7,423 export rows reduce to 6,448
   interruptions.
2. Apply procedure PR-07 section 3's population: unplanned only (planned switching out), restoration
   recorded on or before the extract, the window 1 October to 15 November 2026, the operator's own
   network: 6,005 interruptions.
3. Normalise the device identifier to the padded form and join `rejestr_urzadzen_sn_nn.xlsx` for the
   customers behind the device that operated and for its branch, rejon and section class; the raw
   string join drops 2,823 export rows.
4. Compute each interruption's interrupted customer-hours as the customers behind the device times the
   hours from the recorded start to restoration.
5. Sum to branch, take the largest share; inside it sum to rejon, take the largest share; inside that
   take the section class with the largest share, as PR-07 section 4 directs.

**Ends on:** the remediation slot filed against the `SN-magistrala` trunk sections of rejon Zanowiec
Miasto in the Zanowiec branch, Zanowiec carrying 206.9 thousand interrupted customer-hours against
Grabownik's 114.1.

**Golden:** the remediation slot filed against the `SN-odgalezienie` fused spurs of rejon Borowa
Puszcza in the Grabownik branch, which carry 7,152 customer-interruptions in that rejon, Grabownik
carrying 270.8 thousand interrupted customer-hours.

## Stump sentence

A solver who cleans both exports, normalises the device keys, applies PR-07's population exactly and
drills the recorded customer-hours level by level commits the slot to the Zanowiec trunk sections in
rejon Zanowiec Miasto on Zanowiec's 206.9 thousand interrupted customer-hours, because the dispatch
record times every interruption on a feeder without line
telemetry from the first customer notification rather than from the loss of supply, and that unrecorded
opening runs 242.5 minutes on the fused rural spurs that carry Grabownik's exposure against 8.6 on the
trunks that carry Zanowiec's.

## Three rules

- **Task type:** `grid-reliability-outage-analysis`, which serves Root-Cause and Anomaly Detection in
  the client taxonomy, worked the way reliability engineering works it, as interrupted customer-hours
  per network section over a storm window.
- **Domain test:** the deciding quantity is interrupted customer-hours, the numerator of the operator's
  regulated SAIDI-family index, and the field's own analysis times an interruption from the loss of
  supply, recovering the interval before notification from the feeders whose line-mounted telemetry
  timestamps the device operation, then conditioning it on the class of section because that is what
  governs how quickly anybody is in a position to report.
- **Swap:** rewritten with another field's nouns the call reads "which school district's share of total
  pupil-absence hours is largest, with the hours before the absence was reported added back", and it
  stops making sense at two points: nothing then decides which absences carry an instrument timestamp,
  where here the protection hierarchy decides it (a fuse clears a spur fault without the substation
  breaker ever operating, so the substation never sees it), and nothing makes the reporting interval
  fall by a factor of 28 from a trunk to a spur, where here it falls because a trunk de-energises a town
  centre and a spur serves a handful of scattered holdings.
- **Layer 1:** two dispatch export layouts with a seven-day overlap and renamed columns (the October
  upgrade of the dispatch reporting module); device identifiers unpadded on records whose device was
  commissioned before the 2024 upgrade (the identifier convention changed with it); the telemetry
  archive in UTC against the dispatch system and notification log in Europe/Warsaw (the SCADA historian
  stores UTC); customers in units in the device register and in thousands on the register's summary
  sheet (the summary is built for the annual report); a preliminary and a revised concession return
  overlapping on October (the regulator's own correction cycle); tables inside the prior-year return PDF
  (it is the filed document); the regulator's reporting calendar year against the storm season window
  (two different clocks the operator lives with); five interruptions unrestored at the extract (a
  destroyed line awaiting rebuild). None of them is placed to be caught and none carries the stump; the
  R2 block asserts each is neutral on the call.
- **Layer 2:** `field_method`, pattern `own:pre-notification-interval-from-parallel-telemetry`. The
  methodological choice that flips the call is whether the duration of an interruption is taken as the
  record states it or estimated from the loss of supply, with the unrecorded opening recovered on the
  parallel channel and conditioned on the section class the overlap shows it depends on.
- **Decisive step:** recover the pre-notification interval from the interruptions the line telemetry
  also timed, and apply it by section class rather than as one pooled interval, because 57 per cent of
  the telemetered interruptions sit on trunks and village stations where the interval is 8.6 and 17.0
  minutes while the spurs that need it stand at 242.5.
- **Not semantics:** the data dictionary states in plain words that the recorded start is taken from the
  line device's operation signal where the feeder reports one and otherwise from the first customer
  notification, so a solver can read every field correctly and still have no number for the loss of
  supply on 4,940 of the 6,005 interruptions. Reading the field correctly is necessary and not
  sufficient: what remains is to notice that the interval is measurable only where both channels saw
  the same event, and that the pooled value of that measurement is wrong for the sections that need it.
  The easy route after a perfect read is step 4 of the default path, which files Zanowiec.
- **Not rule application:** no shipped sentence, procedure, column or dictionary entry says to add the
  pre-notification interval back, names the interval, names the telemetered subset as a measurement of
  it, or says that it depends on the section class. PR-07 files the population, the window, the unit and
  the drill rule and stops; executing every one of its clauses exactly produces the default path's
  answer, which the R3a assertion executes on the clean truth.
- **Analyst test:** with both exports de-duplicated, the keys padded, the UTC archive converted, PR-07's
  population applied exactly and the drill rule executed to the letter, computing interrupted
  customer-hours from the recorded start to restoration files the Zanowiec branch at level one on 206.9
  thousand interrupted customer-hours, rejon Zanowiec Miasto at level two and its `SN-magistrala` trunk
  sections as the leaf, which is the wrong leaf.
- **Estimand:** PR-07 section 3 files it to the letter: the population (every unplanned interruption of
  supply on the operator's own network whose restoration is recorded on or before the extract, with its
  start in the window 1 October to 15 November 2026, both dates inclusive), the outcome (the customers a
  section left without supply multiplied by the hours they were without it), the window, the unit
  (interrupted customer-hours) and the comparison (the share of the parent level's own total, drilled
  branch then rejon then section class). The quantity so filed is **unobserved**, because the hours
  without supply are not recorded for any interruption the telemetry did not time, so two estimators of
  one filed quantity stand and the decisive step settles none of the five parts.
- **No decoy:** nothing is planted. No block is copied or backfilled, no memo argues for a branch, no
  stakeholder quotes a figure, no document ranks the branches on the decision question, and no filed
  rule or basis gives the wrong answer. The dispatch record is what the dispatch system writes; the
  telemetry programme is a capital programme with its own schedule; the planned-work rows are the autumn
  maintenance programme. The difficulty survives deleting every wrong number in the pack.
- **No certified replay:** no method is hidden and recovered by reproducing certified or published
  figures. The prior-year returns are at concession level by voltage class and carry no branch
  breakdown, so nothing in them can be fitted back to a branch ranking; the construction is forced by
  the data's own structure, not by matching a published figure.
- **Lesson:** that a duration is only as long as the record's clock, and that where the clock starts at
  notification the missing opening has to be estimated on the subset that saw both clocks and
  transported by what governs it, not by its pooled average over a subset selected for being easy to
  notice. No build on file teaches it: the corpus has the unrecorded opening of a duration nowhere, and
  its censoring builds are all about counts still arriving or about which rows enter a record at all.

## Readability screen

Six tests a rung (`stumping` 2.1). 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene,
6 linear.

| Rung | 1 filed | 2 schema | 3 reflex | 4 bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the pack as it stands, planned work in, overlap week doubled, unpadded keys dropped | PR-07 s.3 files the population | the kind-of-outage column; the exports state their own spans | the battery's duplicate and unmatched-join checks find it | none | yes, this is what the battery is for | yes | readable |
| 1 cleaned recorded customer-hours, the default path | PR-07 files the unit and the drill | the register join gives customers per device | the first group-by | none | no | one product per row | readable |
| 2 one pooled pre-notification interval added to every untimed interruption | nothing files it | nothing marks it; the subset comes from a join of three files | no | none | no | one mean over one subset | silent |
| 3 the interval by section class, the telemetered subset's own composition read against the untimed one **(decisive)** | nothing files it, names it or says it varies | no column holds it; the section class is the register's ordinary type and is benign everywhere else | no reflex reaches the leaf: the sweep below lands eleven of twelve wrong on the leaf | no control, corpus or published figure ties on it | no sweep touches it | no, it is a conditional mean over a subset defined by a three-file join | silent |

**The reflex sweep, run as code on the clean truth before any separation was measured.** Twelve routes
a strong analyst applies, each named with the branch it files at level one and the leaf it reaches,
which is what the call grades. The golden leaf is Grabownik / Borowa Puszcza / SN-odgalezienie.

| Route | Branch | Leaf | Reaches the golden leaf |
|---|---|---|---|
| recorded customer-hours, pooled over all rows (the default path) | Zanowiec | ZAN / Zanowiec Miasto / SN-magistrala | no |
| customers interrupted, not customer-hours | Zanowiec | no | no |
| recorded hours on the device-timed subset only | Zanowiec | no | no |
| recorded hours with the untimed rows dropped | Zanowiec | no | no |
| median span times customers, by branch | Zanowiec | no | no |
| stratify by section class and recombine on recorded spans | Zanowiec | no | no |
| the interval by customers-behind decile | Zanowiec | no | no |
| one pooled pre-notification interval (rung 2) | Pustrzyca | no | no |
| interruption count per branch, no duration at all | Grabownik | GRB / **Mokrzyce** / SN-odgalezienie | **no**, it lands the wrong rejon |
| recorded customer-hours per customer served | Grabownik | GRB / Borowa Puszcza / SN-odgalezienie | **yes, on a basis PR-07 excludes** |
| the interval conditioned on the branch rather than the class | Grabownik | the golden leaf | yes, a form of the decisive step |
| the interval by section class (decisive) | Grabownik | the golden leaf | the golden route |

Two rows need their numbers rather than a verdict. **The count drill** is the crude route the
designation screen warns about, and it was reaching the golden leaf exactly until the collinearity was
broken: with Grabownik's restoration times uniform across its rejony the count and the hours agreed at
every level, so a response running `size()` three times landed the call and all 25 graded counts. The
pack now gives Borowa Puszcza a restoration multiplier of 2.10 against Mokrzyce's 0.25, which the
dispatch note's own account of impassable forest roads supports, so Mokrzyce carries 1,846
interruptions against Borowa Puszcza's 1,136 while Borowa Puszcza carries 107.5 thousand customer-hours
against Mokrzyce's 70.2. The count drill therefore files Mokrzyce and loses the leaf, the three graded
level-three boxes and the eight graded level-two boxes. **The per-served drill** divides recorded hours
by the customers the register puts behind each level's trunks, 5.117 against Mokrzyce's 0.720 inside
Grabownik, and reaches the golden leaf. It is not executing PR-07: section 4 files the comparison as the
share of the parent level's own interrupted customer-hours, and a share of a parent total admits no
per-customer denominator, so the route answers a different question. It is recorded here with its
number rather than hidden, and it is the one route on the sweep that reaches the golden leaf without the
decisive step.

## Semantic fork table

| id | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "interrupted customer-hours" | customers behind the operated device times hours without supply | customer-minutes; customers alone; hours alone | same leaf on the first, different on the others | PR-07 s.3 names the unit as customer-hours; the other two are not that unit; every row's customer count is positive, asserted |
| SF2 | population: "unplanned" | unplanned only | all interruptions including planned switching | same leaf and same default path, measured | PR-07 s.3 excludes planned work by name; asserted both ways |
| SF3 | population: restoration recorded | restoration on or before the extract 2026-11-16 06:00 | the five unrestored rows carried at the extract time | same leaf, measured; no graded count moves | PR-07 s.3 requires a recorded restoration; asserted |
| SF4 | window "1 October to 15 November 2026" | the interruption's recorded start inside the window | restoration inside the window; any overlap with the window | same leaf and same figures | C1: every interruption starts and is restored inside the window, asserted on counts |
| SF5 | the overlapping export week | one row per interruption id | both copies counted | both copies file Nierzyca | the two exports state their own spans in their header rows and in `provenance.md`; the id is unique inside each export, asserted |
| SF6 | the device identifier join | normalised to the zero-padded form | raw string join, dropping unpadded rows | the raw join loses 2,823 rows and files a different branch | the dictionary states the padded convention and the 2024 change; C4, asserted |
| SF7 | telemetry: which interruptions a device timed | the register's telemetry flag, plus every trunk section | the programme workbook's commissioning dates | same leaf and same figures | C1: the programme's commissioned feeders are exactly the register's flagged ones, asserted set against set |
| SF8 | the telemetry archive's clock | the UTC column converted to Europe/Warsaw | read as local | read as local inflates every class interval by 60 minutes | the column is named for UTC, the dictionary states it and the header row states it; 1,065 of 1,065 timed starts reproduce at +01:00, asserted |
| SF9 | "share of its level" | the box's customer-hours over its own parent's total | over the network total at every level | same leaf | PR-07 s.4 names the parent level; each level's shares sum to 100, asserted |
| SF10 | rounding path on the drill | the shares computed from unrounded hours | hours rounded first | the same printed shares and the same leaf | C1 asserted both ways |
| SF11 | the leaf's name | the section class as the register spells it | the Polish long form in the dictionary | same leaf | both strings ship and name one class; the mapping is one to one, asserted |
| SF12 | tie-break at a level | the largest share | a tie needing a second rule | no tie arises | C1: the narrowest top-two gap at any level is 6.74 pp, asserted |

## Ladder

Three separating rungs, three different branches, every rung a defensible analysis that reproduces from
the raw files and dies to exactly one shipped fact. Figures in thousands of interrupted customer-hours,
from `generator/figures.json`.

| Rung | What it does | Branch | Margin | Golden's rank | Dies to |
|---|---|---|---|---|---|
| 0 | the pack as it stands: planned switching in, the overlap week counted twice, unpadded keys dropped | Nierzyca | 1.24x | 4th of four | PR-07 s.3's population, the exports' stated spans, the dictionary's padding note |
| 1 | cleaned recorded customer-hours, the default path | Zanowiec | 1.33x | 4th of four | nothing in the pack: it is the easy route and it is wrong |
| 2 | one pooled pre-notification interval on every untimed interruption | Pustrzyca | 1.42x | 3rd of four | the telemetered subset's own composition: 57 per cent of it is trunk and station sections |
| 3 | the interval by section class **(decisive)** | Grabownik | 1.31x | 1st | it is the answer |

**Position and dominance.** The golden is 4th of four on the pack as it stands and 4th of four on the
cleaned default path, 3rd on the pooled rung, and never 1st or 2nd on an intermediate rung. Dominance:
the golden's edge on the decisive axis (its correction, 156.7 thousand customer-hours) against the
decoy's carried advantage on the recorded axis (Zanowiec's lead over Grabownik on the default path,
92.8 thousand) is 1.69x, over the 1.2x floor. Both are asserted.

**The estimator family, measured on the cut pack.** Every form of the class-conditional interval a
competent analyst would use, and the pooled and branch-conditioned forms beside them.

| Form | Leaf | Distinct designations |
|---|---|---|
| class mean (golden) | GRB / Borowa Puszcza / SN-odgalezienie | |
| class median | the same | |
| class mean weighted by customers | the same | |
| class trimmed mean, 5 per cent each tail | the same | |
| branch by class mean | the same | |
| branch-pooled interval | the same | |

**Six forms, one distinct designation.** That is the designation determinacy number: the golden's own
estimator family returns one path, not 1.64 or 2.32 or 3.0 of them, and `checks.py` asserts the path
under each of the first five by name. The forms do move the drill's **shares**, by up to 0.3176
percentage points on a single box, which is why **no share is graded**: every figure the prompt asks for
on the call side is a whole count the records fix (25 of them, asserted integral), and the shares appear
in the deliverables as the drill's working, which the write-up does not state. That is the
discretisation `stumping` 1.2a prescribes, reached after measuring that no seed in 500 places a share
figure far enough from its bin edge to survive the family's own spread.

**Why a variance lever is not what is happening here.** The decisive step moves the point estimate: it
adds 156.7 thousand interrupted customer-hours to Grabownik and 2.3 thousand to Zanowiec, and reverses
the level-one ranking. No interval is widened, no hold becomes available, and no conservative reflex
reaches the call. The one free parameter a censored-duration estimator usually carries, an interval
midpoint rule or a grouping, is absent: the conditioner is the register's own four-valued section class
and the estimator is the mean of directly observed intervals inside it, so there is no band, bandwidth,
tolerance or cut-off to choose.

**The estimand pincer, run in writing.** The decisive step settles none of the five parts. Population:
PR-07 s.3 files it, including that interruptions without a recorded restoration are out. Outcome: s.3
files the customers times the hours without supply. Window: s.3 files both bounds inclusive. Unit: s.3
files customer-hours. Comparison: s.4 files the share of the parent level and the drill's order. What is
left open is how the hours without supply are obtained for the 4,940 interruptions no device timed,
which is a method, and the data forces it: the interval is observable only on the overlap, the overlap's
own composition rules out its pooled value, and the register's four-valued section class is the only
conditioner the records offer with no parameter to choose.

**Grid.** Four rungs by four branches; every cell is a named wrong answer the pack can produce. The
saturated case does not arise: rung 2's pooled interval and rung 3's class interval come from the same
subset and differ only in conditioning, which no partial application of rung 1 reproduces.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | unplanned interruptions, own network, restoration recorded on or before the extract, start inside the window | PR-07 s.3 files it literally, including that the five unrestored interruptions are out; SF2, SF3 |
| 2 | Unit of account | the interruption, with customers taken from the device that operated | PR-07 s.3 names customer-hours per section; the register is the only customer count in the pack; SF1 |
| 3 | Attribution window | the interruption's recorded start | C1: the generator drops anything whose recorded start falls outside the window, asserted on counts; SF4 |
| 4 | As-of dating | the extract, 2026-11-16 06:00, stated in `provenance.md` and every export header | filed as-of; the register and the programme are static across the window |
| 5 | Version basis | the current dispatch record; the revised concession return supersedes the preliminary one | the returns carry an issue sheet with dates; the main call reads neither |
| 6 | Denominator | the parent level's own total customer-hours | PR-07 s.4's words; SF9 |
| 7 | Weighting | customers behind the operated device, unweighted across interruptions | PR-07 s.3; the register holds one count per device |
| 8 | Window length | the interval is measured over the whole window's telemetered interruptions | the interval is drawn independently of date; the class is the only conditioner the records offer |
| 9 | Boundary inclusivity | both window bounds inclusive | C1: nothing is left on either edge, since the generator filters the recorded start into the window; SF4 |
| 10 | Rounding path | shares from unrounded hours, each figure rounded once | PR-07 s.4; SF10, asserted both ways |
| 11 | Tie-break | the largest share at each level | C1: narrowest top-two gap 6.74 pp, asserted; SF12 |
| 12 | Maturity and censoring | the duration record is censored at notification on untimed interruptions; the population excludes interruptions not yet restored | PR-07 s.3 for the population; the opening interval is the decisive step and is left to the analyst, forced by the data |
| 13 | Order of operations | de-duplicate, apply the population, join customers, compute hours | C1: every order gives one row set, since de-duplication is on a unique id and the population is a row predicate |
| 14 | Row order | file order | C1: every graded figure is a sum or a count |
| 15 | Duplicate resolution | one row per interruption id | the exports state their spans; the id is unique inside each export, asserted; SF5 |
| 16 | Identity normalisation | the device identifier padded to the register's convention | the dictionary states the convention and the 2024 change; C4, the raw join drops 2,823 rows; SF6 |
| 17 | Netting against gross | no netting; every interruption adds | nothing in the pack nets and the procedure does not mention it |
| 18 | Dimensional units | customers in units in the register, thousands on its summary sheet; hours in the deliverable, minutes in the archive | each column's unit is in its header and the dictionary; the summary sheet is not on the call's path, and its thousands equal the register's units, asserted |
| 19 | Code and status semantics | the kind of outage, the section class, the telemetry flag, the signal quality | flat definitions in the dictionary; never the stump; SF7, SF11 |
| 20 | Integerisation | every graded figure on the call side is a whole count | stated in the asking sentence; asserted integral, so no bin can be straddled |
| 21 | Clause scope | PR-07 s.3 and s.4 govern the window's drill, not the regulator's reporting year | PR-07 s.1 states its scope; the returns are the reporting year and carry no branch split |
| 22 | Forward window contents | none: the slot is committed for the rest of the season and the drill reads the window to date | the committed call needs no forward driver file; the forward-facing line below |

**Forward facing.** The committed call is forward facing: the one remediation crew-week is committed for
the remainder of the 2026/27 storm season, which PR-07 s.1 runs to 31 March and which had six weeks
behind it at the extract. The diagnostic quantity is the season to date, which is the only evidence the
operator has, and the window it informs is not closed. This is recorded because the quantity itself
looks backward.

## Literal reader

Executing the prompt, PR-07 and the dictionary word for word, with every silence enumerated: the
population, window, unit, comparison and rounding are each fixed by one filed sentence, and the only
thing the shipped text does not fix is how the hours without supply are obtained for the 4,940
interruptions no device timed. Every reading of every term returns the same row set (SF1 to SF12, each
asserted in `generator/checks.py`), so the single remaining freedom is the method, and the data forces
it: the interval is observable only on the overlap, the overlap's own composition rules out its pooled
value, and the section class is the only conditioner the records offer with no parameter to choose. The
easy answer is reached by an easy method on the same literal estimand, never by another reading. The one
route that reaches the golden leaf without the decisive step divides by customers served, which PR-07
s.4 excludes by filing the comparison as a share of the parent level's own total.

## Oracles

Every control, published figure and reconciliation column in the pack, with what it confirms on the
wrong path.

- `sprawozdanie_niezawodnosc_2024_2025.pdf`: the concession's own reported SAIDI and SAIFI for 2024 and
  2025 by voltage class and by planned against unplanned. It carries **no branch, rejon or section
  breakdown at all**, asserted by searching the extracted text for every branch code, so it cannot rank
  the candidates on any basis, and it ties under every handling of the window because it covers neither
  2026 nor the storm.
- `sprawozdanie_URE_2026_wstepne_i_korekta.xlsx`: concession-level monthly figures, preliminary and
  revised. Same: no branch column, asserted. It reconciles to the dispatch record only at concession
  level and only on planned interruption minutes, which the main call excludes, so it ties on every
  basis of the main call and is an ask organ.
- The device register's summary sheet: customers served per branch in thousands. It confirms the branch
  customer counts on every path and nominates nobody; its thousands are the register's own units,
  asserted.
- The telemetry programme workbook: feeders and commissioning dates. Its commissioned set is exactly the
  register's flagged set (SF7, asserted), so it confirms the same split on every path.
- No calibration corpus of settled decisions ships, and no document reproduces a graded figure.

## Ask sheet

Three asks, each a component of the call's case, each computed over rows the main call's declared
population does not contain, each with its own silent primary device.

**A1, the planned side of the season.** Whether any planned job in the window overran its published
window and if so how many and the hours over in total, with the customer-hours those jobs account for
per branch. Population: planned switching, which PR-07 s.3 excludes from the call, so zero device rows
sit in the call's population. H18 home: the remediation crew-week competes directly with the planned
programme, so the slot cannot be committed without it. Figures: 1 count, 1 total of hours, 4
customer-hours = 6.
Primary device: **D6 an event's quantity on every line it covers, grain unstated.** The grafik holds one
row per scheduled job and the dispatch export one row per interruption, so a visit that switched out two
or three sections of one feeder is one job and several rows. Forcing figure: 260 scheduled jobs carry
440 dispatch rows, and a job is never scheduled twice on one feeder on one day, so the published window
identifies its job; counting rows counts sections.
File path: `harmonogram_wylaczen_planowanych.xlsx` and the dispatch exports' planned rows; 11 columns.
Stops: rows counted against the issued November sheet (wrong), rows against the revision (wrong), jobs
against the issued sheet (wrong), jobs against the revision (golden).

**A2, the notifications nothing matches.** How many notifications match no interruption record, by
branch and channel, with the customers behind the devices they name. Population: notification rows with
no interruption id, which are outside the call's population by construction. H18 home: the call leans on
the notification channel, so the operations desk needs to know how much of it is noise before accepting
a figure built on it. Figures: 12 branch by channel, 1 total, 4 customers-behind = 17.
Primary device: **D1 a replay under fresh ids, key kept.** The contact centre wrote a second row under a
fresh notification id when an agent re-saved a ticket, same customer, same minute, same wording, so the
notification id stays unique and the exact-duplicate sweep sees nothing. Forcing figure: 2,166 rows
repeat a row on the same customer, the same minute and the same wording, and one customer cannot report
a loss of supply twice inside one minute.
Secondary, documented, so it moves the mirror and not the cracker: the IVR left the device and the
branch unwritten between 9 October and 2 November, and those rows resolve through `odbiorcy_ppe.csv`;
559 unmatched rows carry no device at all and resolve only that way.
File path: `zgloszenia_klientow_2026.csv`, `odbiorcy_ppe.csv`, `rejestr_urzadzen_sn_nn.xlsx`; 12 columns.
Stops: raw rows counted (wrong), re-saves removed but the blank-device rows dropped (wrong), blanks
resolved but the re-saves left in (wrong), both handled (golden).

**A3, the correction the concession filed.** October 2026's correction to reported unplanned
interruption minutes for each voltage level, in minutes and as a percentage. Population: the
concession-level return, outside the call's population and outside its grain. H18 home: the slot has to
be defended against what the operator has already reported to the regulator. Figures: 2 minutes, 2
percentages = 4.
Primary device: **D9 a control true only in its own scope.** The preliminary submission divided by the
customer count at 30 September and the revised one by the count at 31 October, which the concession grew
between, so the two sheets are not comparable row for row. Forcing figure: every one of the untouched
months differs between the sheets by one constant ratio, 1.04516, which a correction to October's events
cannot produce; re-basing on that ratio before reading October's difference gives +0.6 and +0.3 minutes
against the raw difference's +0.4 and +0.1.
File path: `sprawozdanie_URE_2026_wstepne_i_korekta.xlsx`; 5 columns.
Stops: raw sheet difference (wrong), the preliminary sheet taken as final (wrong), re-based and read on
planned minutes (wrong), re-based and read on unplanned minutes (golden).

**Main population zero-counts.** A1's rows: 0 in the call's population, asserted on the id sets. A2's
rows: every row it counts carries no interruption id, and the call reads the notification log only for
the earliest time per interruption id, which the IVR gap leaves intact; asserted. A3's rows: no branch
row exists in either sheet, asserted on the column names.

**Hazards, shared across asks.** H1, the two export layouts' renamed columns and the overlap week. H2,
the unpadded device identifier. Both are battery-visible and both are worked by the cracker; they buy
mirror leakage, not cracker misses.

**Referee.** One byte-clean referee: the revised return's October planned-minutes figure, which ties to
the dispatch record's planned rows at concession level under every handling of A1's device, so it
arbitrates nothing about the device and hands over no level.

**Measured by:** `generator/ceiling.py` (run on the cut pack; one row per response, the cracker's ask
row and the mirror's scored from different device readings).

| Ask | Cracker's path | Figures it keeps | Verdict |
|---|---|---|---|
| A1 planned switching overruns | reads the dictionary, runs the battery, executes PR-07 and the schedule's own issue note, counts dispatch rows | 0 of 6 | miss |
| A2 notifications nothing matches | same, plus the unmatched-join sweep and the dictionary's IVR note, no composite-key dedup | 0 of 17 | miss |
| A3 the October correction | same, plus every published-figure reconciliation, diffs the sheets row for row | 0 of 4 | miss |

**Pair ceiling:** 28.5
**Mirror leakage:** 0.0

## Tried and rejected

### Candidate 1, separating confounding inflation from polygenic signal, killed at the draw (2026-10-18)

(Architecture v1a, on `genomics-gwas-high-dimensional-association`; never registered.) The filed
quantity was each contributing cohort's confounding inflation, unobserved, recovered as the intercept
of a regression of chi-square on a linkage covariate. Killed on the sixth screen at four measured
settings with no window between them: profiled over the intercept with the slope free, the set within
two log-likelihood units was 0.0204 wide at its sharpest against a printed precision of 0.01, twice
the printed unit, and 0.0962 (ten times) at the only range where the low-covariate bin named the wrong
candidate. Three of nine enumerated routes reached the golden and all three were the same move, reading
the region where the signal is absent. **Rule earned:** an identification of the form "estimate the
nuisance where the signal vanishes" fails the sixth screen by construction, because the region where
the signal vanishes publishes the nuisance and the leverage that sharpens the identification is what
purifies that region.

### Candidate 2, fine-mapping which variant in a locus is causal, killed at the draw (2026-10-18)

(Architecture v1b; never registered.) Under the standard single-causal-variant model the causal variant
has the largest expected statistic, so the lead can differ from it in only three ways and each was
measured: with equal power the answer is the lead, so lead-by-p-value and largest-absolute-effect both
reach it and the standard pipeline is the golden; with the causal variant poorly imputed the licensed
method family split three to one on the graded name and the minimum of the imputation column published
the answer; with two causal variants the family split again and the well-posed answer is a set rather
than a name. **Rule earned:** where the well-posed answer to "which one" is a set, a build that grades
a name grades an arbitrary element of it, and no amount of margin fixes that.

### The genomics ground abandoned at the re-root (2026-10-18)

Both candidates above were on biomedical genomics ground and both died at the draw, the second on the
graded object itself. The ground is left behind rather than screened further: the number moves to
`energy-systems-utilities` / `grid-reliability-outage-analysis`, where the graded object is a single
named leaf of a drill whose every box carries one well-posed share.

### A revision log as the calibration organ, rejected before any file was cut (2026-10-18)

The reserved `calibration_form` was `retry_or_revision_log`, and the natural instance here is the
dispatch system's own edit history, where an operator back-dates an interruption's start once the crew
reports what it found. Rejected on the revelation screen: a revision that records the true loss of
supply publishes the quantity the decisive step estimates, so a filter on the revised rows returns the
answer rather than an approximation. Replaced by `parallel_run_overlap`, where the second channel exists
for its own operational reason and never covers the sections that need it.

### Interval censoring of the restoration end, rejected on measurement (2026-10-18)

The first shape tried on this ground censored the **restoration** time between two meter polls, so each
duration lay in an interval of width twice the polling period. Killed by one computation: with the two
offsets independent and uniform on the polling interval, the midpoint of the bracket is unbiased for the
mean, so the reflex "subtract one polling interval" reaches the golden exactly, and for a share rather
than a mean the per-event midpoint classifier was measured 0.5 percentage points from the truth at a
240-minute cadence against a 13-point error for the recorded bracket, so the only route that lands
wrong is one no analyst takes. Replaced by censoring at the **start**, which is one-sided, has no
midpoint to take because the record holds no upper bound for it, and whose size is measurable only on a
subset selected against the sections that need it.

### Right censoring at the extract as the decisive step, rejected on the WHAT screen (2026-10-18)

Treating the interruptions still open at the extract as right-censored rather than dropped was drafted
as the decisive step and killed on `stumping`'s WHAT screen without a measurement, because it settles
whether members not yet observed are in the population, which is one of the estimand's five parts: file
it and the computation follows from the clause (rule application), leave it unfiled and the main call
forks. This is task190's death in another world. The three unrestored interruptions still ship, filed
out of the population by PR-07 s.3, and `checks.py` asserts they move no graded share by more than
0.03 pp.

### Hour of day as the conditioner, rejected at design (2026-10-18)

The pre-notification interval is physically longer at night, which would have been a second conditioner
and a second rung. Rejected because the recorded start of an untelemetered interruption **is** the
notification, so an event that began at 02:00 and was reported at 06:40 carries an 06:40 start: the
conditioner would have to be recovered from the very quantity the step is estimating. Dropped in favour
of the section class, which the register fixes independently of any timestamp.

### Grading any share of the drill, rejected on measurement (2026-10-18)

The first design graded each box's share of its parent level to the nearest whole per cent, twelve
figures, which is what shape 12 grades. Killed by measurement rather than argument: the golden's own
estimator family (class mean, class median, class customer-weighted mean, class trimmed mean, branch by
class mean) spreads a single box's share by up to 0.3176 percentage points, driven by the sampling error
of the low-voltage class interval in the golden rejon, and a search over 500 seeds found **no** seed
where even one share figure sat far enough from its bin edge to survive that spread while the ladder
also held (the bar was an edge above three times the spread; the best seeds reached 0.049 pp of edge
against 0.374 pp of spread). Replaced by records-fixed counts: the 25 graded figures on the call side
are whole interruption and customer-interruption counts, the shares stay in the deliverables as the
drill's working and the write-up states none of them.

### The count drill reaching the golden leaf, found and broken (2026-10-18)

Measured on the cut pack: drilling on the plain **number of interruptions** at each level, with no
duration analysis of any kind, reached the golden leaf exactly, because the correction's whole effect is
to weight up the many small rural interruptions and those are where the counts are. With every graded
figure a count, a response running `size()` three times would have landed the call and all 25 counts.
Broken by giving the golden branch's rejony genuinely different restoration times, which the dispatch
note's account of impassable forest roads supports: Borowa Puszcza now carries a restoration multiplier
of 2.10 against Mokrzyce's 0.25, so Mokrzyce leads on count (1,846 against 1,136) while Borowa Puszcza
leads on customer-hours (107.5 thousand against 70.2), and the count drill files Mokrzyce. Re-measured
after the break: eleven of twelve enumerated routes miss the golden leaf.

### Interval censoring of the restoration end, rejected on measurement (2026-10-18)

The first shape tried on this ground censored the **restoration** time between two meter polls, so each
duration lay in an interval of width twice the polling period. Killed by one computation: with the two
offsets independent and uniform on the polling interval the midpoint of the bracket is unbiased for the
mean, so the reflex "subtract one polling interval" reaches the golden exactly, and for a share rather
than a mean the per-event midpoint classifier was measured 0.5 percentage points from the truth at a
240-minute cadence against a 13-point error for the recorded bracket, so the only route that lands wrong
is one no analyst takes. Replaced by censoring at the **start**, which is one-sided, has no midpoint to
take because the record holds no upper bound for it, and whose size is measurable only on a subset
selected against the sections that need it.

### Right censoring at the extract as the decisive step, rejected on the WHAT screen (2026-10-18)

Treating the interruptions still open at the extract as right-censored rather than dropped was drafted as
the decisive step and killed on `stumping`'s WHAT screen without a measurement, because it settles
whether members not yet observed are in the population, which is one of the estimand's five parts: file
it and the computation follows from the clause, leave it unfiled and the main call forks. This is
task190's death in another world. The five unrestored interruptions still ship, filed out of the
population by PR-07 s.3, and `checks.py` asserts that carrying them at the extract time leaves the call
where it is.

### Hour of day as the conditioner, rejected at design (2026-10-18)

The pre-notification interval is physically longer at night, which would have been a second conditioner
and a second rung. Rejected because the recorded start of an untimed interruption **is** the
notification, so an interruption that began at 02:00 and was reported at 06:40 carries an 06:40 start:
the conditioner would have to be recovered from the very quantity the step is estimating. Dropped in
favour of the section class, which the register fixes independently of any timestamp.

### A per-branch count of overrunning planned jobs, folded (2026-10-18)

A1 first asked for the overrunning jobs per branch. Measured on the cut pack, the row-grain and
job-grain counts coincided on the two small branches (Zanowiec 7 against 7, Grabownik 1 against 1), so
the cracker kept 2 of 27 ask figures and the A1 row was not an honest miss. Folded into one total, which
the row grain gets wrong globally, and the measured cracker keep went to 0 of 27.

### Architecture 6 abandoned at the re-root to architecture 7 (2026-10-18)

Built end to end with every free gate green and spent at stage 4. The determinism judge returned
NOT_DETERMINISTIC and SEND_BACK with **Gate G FAIL, `banned_stumping_type`**: `mechanism:
planted_defect_flip (mixed measurement clock)`, `stumping_family: surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`. What is left behind is the decisive rung:
the pre-notification interval recovered from the telemetered subset and transported by section
class, whose whole difficulty was catching that SD-OMS's own `poczatek_lokalny` and
`czas_trwania_min` understate 4,940 of the 6,005 interruptions. A surface-read rejection is banned
at any depth and on one uniform clock the task collapsed into executing PR-07 section 4's drill, so
the architecture is spent rather than repairable. What is kept: the world, the pack's file set, the
personas and every Layer 1 device. The clock correction stays in the pack as input hygiene and may
no longer decide the call, so any architecture 7 owes `checks.py` an assertion that the committed
answer is identical under the recorded clock, the pooled-mean, the pooled-median and the
class-stratified corrections.

**The determinacy lesson carried forward, because this build's own screen missed it.** The
designation determinacy screen above reports one distinct path across six members of the golden's
estimator family; the judge, counting the forms that skip the conditioning the decisive step adds,
found three leaves (pooled mean names Pustrzyca, pooled median names Zanowiec, class-stratified
names Grabownik). All six screened forms were class-conditioned, so the screen measured the family
on the assumption it was testing. A family is counted wide enough to include the forms that skip
the conditioning, or the count is worthless.

### Candidate 3, coincident-peak headroom on the transfer feeder, killed on measurement (2026-10-18)

(Architecture 7, screen 1, `wave5/task201b/screen1.py`, run on a designed clean truth before any
file was cut.) The crew-week's clearance needs the line dead, so in the storm season the load
transfers through the normally-open tie, and the receiving feeder's firm winter rating is the joint
limit several candidates draw on. Decisive step: whether a transfer fits is decided by the
**coincident** load of the two feeders at a common half hour of the clearance window, not by the sum
of their own maximum demands, which is the field's own diversity question. Killed by one
computation: across the twelve candidates the window diversity factor spans only **0.8996 to
1.0000, a range of 0.1004**, and the clearance window (07:00 to 16:00) already excludes the domestic
evening peak, so **11 of 12 candidates are admitted at a flat factor of 1.00** and the constraint
removes nobody. The golden ranked **1 of 12 on rung 1**: the exposure ranking alone reaches it. Every
flat coincidence factor from 0.80 to 0.97 named the same candidate, so the textbook diversity factor
reproduces the decisive step. **Structural reason, not a tuning failure:** an MV feeder's load is
dominated by domestic customers on every candidate, so no two feeders in this world carry profiles
different enough to open a diversity spread a flat factor cannot absorb.

### Candidate 4, the clearance outage's own planned interruption netted, killed on measurement (2026-10-18)

(Architecture 7, screen 2, `wave5/task201b/screen2.py`.) PR-07 would file the basis as the net
change in interrupted customer-hours, planned and unplanned alike, so the work's own planned
interruption sits on the other side of the ledger; the customers stranded while a stretch is worked
are those behind the nearest switching device upstream of it, so the honest cost is the line's own
isolating structure and the easy cost is its whole load for the whole job. The strand share was
genuinely wide, **0.2526 to 1.0000, a factor of 3.96**, and the mechanism still died twice:
**14 of 25 enumerated reflexes reached the decisive answer** and the decisive margin was **1.1165x**,
under the 1.15 floor. **Structural reason:** a forty-hour whole-line clearance outage on the leading
candidate costs 3,180 customers times 40 hours, **193.5 thousand customer-hours against 61.4
thousand of avoided unplanned exposure**, so the two sides of the ledger are not commensurate,
`E - C` is driven almost entirely by `-C`, and every cheapest-to-work reflex (exposure per km,
exposure per crew-hour, exposure per customer, benefit-cost on the whole-line cost, and every flat
fraction of it at 0.40 and above) lands the answer. Scaling the exposure to the remainder of the
season opens a window at a projection factor near 2.9, but the factor is then the single dial that
buys the separation and spends it.

### Candidate 5, concurrent upstream unavailability netted, killed on the reflex sweep (2026-10-18)

(Architecture 7, screens 3 to 6, `wave5/task201b/screen3.py` to `screen6.py`.) The joint limit is
the customer's own supply time: a customer loses supply whenever any device on its supply path is
open, while the dispatch record holds one row per device that operated, so a spur outage running
inside an outage of the trunk or station above it kept nobody on supply, and ranking the corridor
packages on the recorded interrupted customer-hours sizes each against the whole of the customer's
lost time. Generator G10, cross-dimensional duplication. Measured in two forms.

With the trunk packages in the shortlist the netting **only ever shrinks downstream candidates**,
and the upstream candidate's customer count is the sum of the downstream ones, so it cannot reorder
the top: the golden ranked **1 of 8** on the recorded ladder and **7 of 10 reflexes** reached it.
Restricted to the SN-odgalezienie corridor packages it does flip, and the flat-correction reflex is
broken by construction because a flat keep share cannot reorder: at the tuned cut the default path
files **GRB / Borowa Puszcza** on 16.291 thousand recorded customer-hours, the decisive route files
**ZAN / Zanowiec Miasto** on 13.173 thousand restorable against Borowa Puszcza's 10.978, a margin of
**1.2000x**, with the keep share spanning **0.633 to 1.000**.

It dies on the reflex sweep. Material concurrent unavailability needs a common cause, the only
common cause this world offers is the storm episode, and the measured collinearity is
**corr(netted share, storm share) = +0.8292** and **corr(netted share, storm customer-hours) =
+0.8554**, with the storm carrying **72.6 per cent** of the recorded total. So **excluding the storm
episodes reaches the golden as its top pick with no coincidence analysis at all**, and that is not
merely an opponent reflex: excluding major event days is the reliability standards' own convention
and the basis the concession's filed returns are reported on, so it fires the readability screen's
reflex test and its control-bench test at once. There is no setting that decouples them, because
decoupling needs long upstream outages in calm weather and independent failures do not overlap at
any material rate. **Rule earned:** a decisive step that nets concurrent unavailability cannot hold
where the concurrency is produced by a named episode the pack records, because the episode flag is a
one-line filter that reproduces the netting.

### The binding-constraint direction on this cell, screened out (2026-10-18)

Three structurally distinct instantiations of `binding_constraint` under gap `objective` (the only
gap `stumping` 1.4 licenses for it) were screened on measured truth and each died for its own
reason: the constraint did not bind differentially (candidate 3, spread 0.1004), the two sides of the
ledger were not commensurate (candidate 4, 193.5 against 61.4 thousand customer-hours), and the
decisive quantity was collinear with a recorded episode (candidate 5, +0.8292). A fourth, the
crew-week's clearance capacity in route-km against each candidate's corridor length, was rejected
without measurement on two grounds already measured elsewhere: the benefit of clearing part of a
corridor is proportional to the kilometres cleared, because a feeder's vegetation fault rate is set
by its whole corridor, so there is no physical warrant for the binary completion that
`strategies.md` F3 requires ("reachability binary, never graded"), and the graded form is the
exposure-per-kilometre density, which is the opponent's first normalisation. What F3's one portal
success rests on, a shared pool whose candidates' claims overlap so that sizing each against the
whole pool double-books it, is task106's spent driver, and the only instance of it this world offers
is candidate 5.

### Candidate 6, the decaying yield of a flagged set, killed on measurement (2026-10-18)

(Architecture 8, screen 1, `wave6/w6_201/screen1.py` and `seedsweep1.py`, run on a designed clean
truth before any file was cut, on the re-rooted cell `general-statistics-data-science` /
`multiple-testing-selective-inference`.) A sector inspectorate works its screen's flags in order of
the absolute shortfall, its verification capacity is a fixed 45 cells a quarter, and a filed
standard sets the minimum substantiated findings the campaign must reach, so the call is the
quarter close at which the bar is met. Decisive quantity: how many of the 4,450 flags are genuine
rather than the screen's own chance yield, so the campaign's yield decays once the list descends
past the real signals, a real shortfall scaling with a cell's expected caseload and a chance
shortfall with its square root. Every easy route carries a rate instead of a count: the pilot's own
observed rate (0.6500 over 60 verified files) files quarter 2, the pooled corpus rate quarter 2 and
the size-stratified pilot quarter 2, against a truth of quarter 5. It died twice over. **The graded
figure is the crossing of a cumulative random walk:** over 20 seeds with every parameter fixed the
truth took five distinct values, quarters 3, 4, 5, 6 and 7 (files 133 to 277 after the pilot),
while all 20 seeds filed quarter 2 on the easy route, so the ladder's margin is the seed's and not
the design's. **And the decisive route's estimator family does not close:** on one cut its six
defensible forms filed quarter 8 (a parametric null simulation), quarter 1 (Storey at 0.4, 0.5 and
0.6, and the Benjamini-Hochberg implied count) and quarter 2 (the null read off the unflagged
bulk), not one of them the realised quarter 5. corr(absolute shortfall, cell size) over the flags
is +0.9341 besides, so the worked order is the size order. **Rule earned:** an expected count of
genuine findings cannot be graded through the date a cumulative count crosses a bar, because the
crossing is a property of where individual signals happen to fall in the worked order rather than
of the quantity being estimated.

### Candidate 7, the genuine findings a fixed budget reaches, killed on measurement (2026-10-18)

(Architecture 8, screen 2, `wave6/w6_201/screen2.py`.) The repair for candidate 6 was to grade an
argmax rather than a crossing, which is what `stumping` 3 prescribes when a lever randomises the
graded figure: five filing rounds inside the statutory re-opening window, the inspectorate's
capacity covering 45 cells of one round, the call the round whose top 45 by shortfall holds the
most genuine under-reporting. The design claim was an inversion worth having, that at a fixed
budget a wider family is an advantage (more chances of holding a real signal in the top k) while at
a fixed trigger it is a penalty, so the multiplicity correction, this cell's reflex and task191's
whole cure, would point the wrong way. Measured, it points the right way. **4 of 10 enumerated
reflexes reached the golden, the correction among them:** the most Bonferroni survivors, the most
Benjamini-Hochberg survivors, the largest departure inside the top k and the highest pilot rate all
named 2026Q2, which is the golden. The true margin on the graded quantity was **1.0417x** (25
genuine findings against 24), far under the 1.15 floor; the golden held in only 19 of 24 seeds, the
other 5 naming 2026Q1; and the decisive route's own forms split three ways (a null simulation named
the golden at a margin of 1.0495, the local-FDR and BH-implied forms returned zero genuine findings
for every round, an excess-over-chance form named 2026Q4). **Structural reason, not a tuning
failure:** expected true discoveries at a fixed depth are dominated by per-test power, power here
is the cell's expected caseload, and both the multiplicity correction and the top-k departure rank
on exactly that, so the inversion is second order against the one thing every reflex already sorts
on.

### Candidate 8, a period's flags in excess of its own chance yield, killed on measurement (2026-10-18)

(Architecture 8, screen 3, `wave6/w6_201/screen3.py`.) The only remaining way to put a family-level
quantity to a decision is the fixed-trigger regime: each round's flags against the chance yield its
own family would produce, with the screen testing every cell against its own trailing reference and
the reference length drawn independently of size (2 to 24 months, out of entries, gaps and
suspensions), which is also the shape candidate 2 of this draw would have taken. **6 of 7 routes
reached the golden**, the plainest of all included: the most flags, the highest flag rate, the most
tests (one group-by on the submission file), the excess itself, and both routes restricted to the
common-exposure subset of cells carrying a full reference history. The golden's own margin was
**1.0172x** (59 genuine flags against 58). corr(excess, breadth) +0.9189, corr(genuine flags,
breadth) +0.8960, and corr(genuine flags, breadth times prevalence) **+0.9986**: a family's genuine
count is breadth times prevalence times detection, so it is collinear with the row count of the
file it is drawn from. The common-exposure filter reaching it is `stumping` 1.2's own screen fired
in its own words, and the escapes that screen allows are spent here (no unit attaining the exposure
is completion, which is task194's driver).

### The family-level multiplicity direction on this cell, screened out (2026-10-18)

Three structurally distinct ways of putting a false-discovery quantity to a decision were screened
on measured truth, each died for its own reason, and the three reasons are one wall. Such a
quantity can be put to a decision in exactly three ways: as **a count crossing a bar**, where the
graded figure is a random walk's crossing (candidate 6, five distinct quarters over 20 seeds); as
**a pick at a fixed budget**, where it is monotone in per-test power and the correction itself
ranks on power (candidate 7, 4 of 10 reflexes, margin 1.0417x); or as **a pick at a fixed
trigger**, where it is collinear with the family's breadth at +0.9986 and the breadth is one
group-by (candidate 8, 6 of 7 reflexes, margin 1.0172x). **Rule earned:** on this cell a
false-discovery quantity decides nothing a sorted column has not already decided, which is why the
one driver that held here took the shape it did, task191 asking *whether* one selected extremum
beats the extremum of a quiet set of the same size and length, a correction identical for every
candidate and therefore unable to order candidates at all. The task type's other objects were each
closed before this draw: the extremum against a null extremum is task191's; the null that holds a
filed error rate, and the unit of independent evidence that fixes it, is task186's; the shrinkage a
selected level needs is measured dead in task202 (the construction's spread 13.152 against the
10.499 bias it removed, with empirical Bayes beating it more than three to one and James-Stein
filing the golden verdict in 40 of 40 seeds) and in task471 (the shrinkage method forced by nothing
filed); a selection-conditional interval that only widens dies on `stumping` 1.2's variance-only
screen, with task195 holding the paired-difference uncertainty besides; and the family of
hypotheses is itself one of the estimand's five parts, so filing it is rule application and leaving
it open forks the main call. **What this leaves the next draw on this cell:** not a selective
quantity over a family, but a quantity whose construction the data forces with the designation
following from it, and the honest report is that this author's driver search on
`multiple-testing-selective-inference` under anomaly-detection is spent, not that the cell is
closed. The differentiation line this draw would have owed task191, written and now unspent: its
correction is common to every candidate and answers whether, while each of the three candidates
above needed a correction that differs by candidate, and all three ways of making it differ are
collinear with a column the pack ships.

### Candidate 9, a rank verified, killed on the determinacy criterion (2026-10-18)

(Architecture 9, screen 4, `wave6/w6_201b/screen4.py`, run twice byte-identical on a designed clean
truth before any file was cut. The object is the last one `stumping` Part 3 names for selected-unit
ground that task191 does not already hold: a simultaneous statement about which units' ranks the
evidence determines.) The determinacy geometry was priced in parallel on other ground and does **not**
close the object (120 adjacent pairs over 20 redraws: 73 more than ten family-spreads apart, 1 under
one spread, and 46 in the live middle, median normalised gap 12.30), so this screen was spent on the
one question left open: can a rank call be shaped so that no certainty bar is needed at all? **No,
and the answer is an enumeration rather than one instance's measurement.** A rank statement has
content only through a determinacy criterion, and a criterion is one of exactly four things, because
"verified" means "determined under a stated admissible set" and an admissible set is either filed,
recorded, or the estimator family itself. Each was built and measured on 14 units ranked into a
worst-three set, over 20 redraws:

- **A probability bar** is a filed level and therefore a filed method (`stumping` 2.1, test 1), and it
  is degenerate here besides: the Bonferroni pairwise certified set is **empty at all four of 0.80,
  0.90, 0.95 and 0.99** on the measured cut, and the set moves with the filed level in only 3 of 20
  seeds. So the graded object is the empty set most of the time and a filed number the rest.
- **Records-fixed bounds** (disclosure banding) make it exact interval arithmetic on shipped bounds:
  one comparison of a lower bound against the fourth largest upper bound, **0 estimates**, which is
  rule application.
- **A filed materiality tolerance** is that same arithmetic plus a shipped number, and it agreed with
  the plain sort of the point estimates in 8 of 20 seeds besides.
- **Unanimity across the licensed estimator family** is the only criterion whose content is
  analytical, and it dies twice. The certified set **is the plain sort in 18 of 20 seeds**, so nine
  times in ten it adds nothing a sorted column has not already added; and where it does have content
  it has it exactly where the call is not determinate, with
  **corr(distinct certified sets across the family, positions left undetermined) = +1.0000** and a
  mean of **1.10 distinct sets of 5** against the 1.00 `stumping` 1.2 permits.

**Rule earned:** removing the bar from a rank statement does not remove its determinacy criterion, it
relocates the criterion into the records, where it becomes arithmetic; and the one relocation that
keeps analytical content puts the criterion's content and the designation screen's refusal on the
same number, at a correlation of exactly one. So **neither of the two non-level objects `stumping`
Part 3 names for selected-unit ground is drawable beyond task191's**, and that list is exhausted
rather than half spent.

### Candidate 10, an authority's refusal propensity under selection into a voluntary register, killed on measurement (2026-10-18)

(Architecture 9, screen 5, first half, `wave6/w6_201b/screen5.py`, run twice byte-identical. Cell
re-rooted for this candidate to `political-science-public-policy` /
`conflict-protest-event-data-analysis`, objective anomaly-detection, drawn by the inverted procedure
`stumping` Part 3 prescribes where three screens close a cell: the file first, then the quantity that
file forces, and only then the field's method for it. Labelled candidate 9 inside the script.)
**Forcing file: the interior ministry's assembly notification register.** What it pins that no other
file in this world pins: which assemblies were *put to* the authority, so it is the only record of
the authority's own decisions, as against the observatory's log, which records what happened.
**Quantity it forces:** the authority's latent refusal propensity per district, unobserved because
the observed refusal rate is conditioned on a notification decision that responds to the propensity
itself. Organisers who expect refusal do not notify, so the notified pool is skimmed toward
permittable assemblies and the observed rate understates the propensity most exactly where it is
highest, which means the harshest district posts the mildest rate. It avoids this cell's two spent
drivers by construction, because the selection is organisers' behaviour and not whether an event
entered a record.

The easy route files a wrong answer in **14 of 20 seeds**, which is the half that works. It dies on
the other half, three times over. **The decisive route reaches the truth in only 6 of 20 seeds**,
worse than two plain routes, because the selection correction has to be solved per district off two
counts and injects more noise than the bias it removes (`stumping` Part 3, price the estimator's own
standard error). **The selection's own magnitude is a shipped column:**
**corr(notification rate, latent propensity) = -0.9915** on the measured cut and **-0.9681** over 20
seeds, range -0.9898 to -0.8942, so ranking districts by the lowest take-up against the published
roster of registered organisers reaches the truth **13 of 20**, more than twice the decisive route,
and the deterred share does the same at 13 of 20. **And the unexposed subset publishes it too:** the
first-time notifiers' refusal rate, one filter and one divide, reaches it 7 of 20 against the easy
route's 6, which is `stumping` 1.2's common-exposure subset screen fired in its own words. **Rule
earned:** a decisive step that corrects for selection into a voluntary register cannot hold where the
register's take-up rate is computable, because the take-up rate **is** the selection's magnitude and
is one divide against a published roster; withholding the roster removes the denominator the
correction itself needs, so it is the same single dial from both ends. This is `stumping` 1.2b's "the
region where the signal vanishes publishes the nuisance" with the region replaced by the mechanism's
own intensity.

### Candidate 11, a district's count against its own opportunity structure, killed on measurement (2026-10-18)

(Architecture 9, screen 5, second half, same cell and same inverted procedure. Labelled candidate 10
inside the script.) **Forcing file: the occasion calendar**, the dated verdict days, anniversaries
and council votes, with a second file pinning which districts each occasion reaches. What it pins
that nothing else pins: when and where assembly was scheduled to be possible. **Quantity it forces:**
a district's expected assembly count under its own opportunity structure, as an exact weighted sum
over the occasions that reach it, forced by arithmetic and not by a fit, which is the shape
`stumping` 1.6a records as the one that has passed a judge at Gate F strong. The anomaly is the
propensity and not the count, and the naive route compares districts whose occasion exposure inside
the window differed.

Dead on four measurements. **The plain route beats the designed one:** count per occasion touched,
one join and one divide with the weights thrown away, reaches the truth **13 of 20** against the
decisive weighted-exposure route's **12 of 20**. **The weights are decoration:**
**corr(weighted exposure, occasions touched) = +0.9305** on the cut and **+0.9407** over 20 seeds,
range +0.8218 to +0.9894. **There is no ladder:** the easy route, the raw count, reaches the truth
**11 of 20**, so rung 0 lands over half the time. **And the decisive route is not determinate
either**, at 12 of 20. **Rule earned:** an exposure built as a weighted sum over a shipped occasion
set is collinear with the unweighted count of that set at about +0.94, so the construction's weights
never reach the decision, and where the occasion set is a shipped calendar the exposure is one join.
That is candidate 8's breadth collinearity (+0.9986) reached from a different file in a different
domain, which makes it a property of weighted-sum exposures rather than of either cell.

### The rank-certainty direction, and the inverted draw on a second cell, screened out (2026-10-18)

Three candidates, three measured deaths, no card registered, no file cut, no git write. Two findings
carry forward and they are separate.

**On the object.** `stumping` Part 3 named two non-level objects for selected-unit ground, an extremum
judged against a null extremum and a rank verified. The first is task191's. The second is now
measured dead across an enumeration of all four determinacy criteria it can have, so that list is
exhausted and the ground-level rule it qualified ("a graded object which is a level at a selected
unit cannot hold") no longer has a drawable exception. A draw needing selected-unit ground changes
the ground, not the object.

**On the procedure.** The inverted draw was run exactly as `stumping` Part 3 prescribes, file first on
a fresh cell, and it still died twice, which is information about the inversion rather than about the
cell. Both candidates were unobserved quantities forced by arithmetic from a file at another grain,
both clearing `stumping` 1.6a's three clauses, and both died for one reason: **the forcing file
publishes a one-column proxy for the construction it forces.** A voluntary register publishes its own
take-up; a shipped occasion set publishes its own cardinality. So the inverted procedure needs a
fourth clause beyond 1.6a's three, and it is one computation: the forcing file must pin the
construction **without** shipping a scalar summary of it, tested as one correlation between the
construction's output and the plainest column of its own forcing file, run before any separation is
measured. Both deaths here would have been caught by that correlation at -0.97 and +0.94, and
candidate 8's at +0.9986, so the clause is three for three against measurements already on file.

**The axes, settled for whatever follows.** Two probe cards on the new cell, both `PASS` at exit 0
with no BLOCK and no WARN and a nearest driver of 0.07: `gap objective` with generator `G15` and
`gate_g binding_constraint`, and `gap population` with generator `G11` and `gate_g etl_conformance`.
The allocation's axis correction is therefore confirmed from the other side, and the window on
`political-science-public-policy` / `conflict-protest-event-data-analysis` is wide open; what this
objective is short of is a mechanism, not an axis. Personas for the cell drawn and never typed, with
`guard.py names --geo Spain --seed 201`: Bonifacio Morell, Sosimo Acevedo, Nacho Soriano, Estela
Lillo, Virgilio Toledo, Rosaura Sánchez. One tool finding alongside them: `--geo` on its own does
nothing, the locale does the work, and `business.LOCALE_FOR_GEO` recognises 27 patterns only, so
Chile, Kenya, Georgia and South Africa all fall back to `en_US` and return the identical six names at
a given seed. A draw wanting a non-European geography on this cell passes `--locale` or accepts
`en_US`.

### Architecture 10, the inverted draw on survey-research ground (2026-10-20)

Wave 7 re-rooted this number onto `survey-research-official-statistics` / `anomaly-detection`, objective
anomaly-detection, a cell this number has never held and the lane's most worked cell after grid
reliability. Three drivers were spent on it and the draw was taken away from all three: task125's
recruitment filter riding a rotating panel, task186's empirical null for cycles shared within a place,
and task190's architecture 6, the ratio of a complete administrative numerator to a stratified-sample
denominator, which failed Gate F by measurement when its reader took 43 of 43 figures. Nothing was
registered, no file was cut and no git write was made.

**The draw was inverted as the contract prescribes: the file first, then the quantity it forces, then the
field's method.** The organisation's files were enumerated before any estimator was named: the frame
extract and its build log, the selection and design file, the interviewer assignment and route sheets,
the contact-attempt log, the doorstep observation file, the response microdata, the instrument routing
and version log, the keystroke and timing paradata, the diary-keeping log, the edit-rule firing log, the
query and follow-up log, the imputation log, the weighting and calibration file, the replicate weights
and quality report, the incentive ledger, the reissue log, the record-linkage candidate-pair file, the
published series with its vintages, and the collection calendar. Each was read for what it pins that no
other file pins, and the proxy screen (contract screen 2) was run on the construction before any
separation was measured.

**The screen pass earns one law, and it is about this cell rather than about any candidate.** On survey
ground the forcing files are the office's own production logs, and a statistics office's quality
framework requires it to publish each log's own rate as an indicator: the response rate, the link rate,
the edit rate, the imputation rate, the item-nonresponse rate. So the one-column precis contract screen 2
looks for is not an accident of a particular file here, it is **mandated output**. Screen 2 therefore
fires structurally on this cell and not incidentally, which is why the escape the contract names (force
the quantity from the file's timing, its completeness conditions or the incentives that put rows in it)
does not help: on this ground the completeness condition **is** the published rate.

**Four candidates died, which is past the contract's stop rule of three, so the pass stopped.**

### Candidate 12, a composite's tail count under a split-module design, killed on uniqueness (2026-10-20)

(Architecture 10, screen 1, paper, with the measurement not spent because the uniqueness kill is prior.)
Forcing file: the module assignment and rotation design. What it pins that nothing else pins: which
components each household was asked, so it is the only record of which pairs of components were ever
observed together. Quantity forced: the count of households above a statutory burden threshold on a
composite none of whose households is ever observed whole, so the composite is latent for every unit and
the contract's screen 3 has no attaining subset to fire on. It cleared screens 1 (the correcting input is
fifteen pairwise covariances, one per pair, identified on every pair by the balanced design), 3, 6 (the
denominator is the frame count, records-fixed), 7 (the estimand files population, outcome, window, unit
and comparison; two methods of estimating that one quantity stand) and 8 (the graded object is a
population count, not a level at a selected unit). **It dies on the driver.** task237's driver is the
share of a composite's variance due to the attribute it is meant to capture, where a subset of the
components shares a second source of variance, estimated off a split design's pairwise covariances. With
the nouns stripped, that is this candidate: both are the covariance structure of a composite's components
mis-estimated because the design never observes them together. `guard.py check` scores the text at 0.08,
under the 0.12 WARN floor, which is the case the skill records as the text screen's blind spot and the
abstraction test's job. **Rule earned:** a split or rotating module design is one forcing structure, not
two, and the composite objects it forces (a reliability coefficient, a composite's spread, a composite's
tail count) are one driver told three ways.

### Candidate 13, a per-respondent cap on incident detail, killed on screen 2 by arithmetic (2026-10-20)

(Architecture 10, screen 2, no measurement needed.) Forcing file: the incident-level detail forms. What
it pins that nothing else pins: the characteristics of incidents, which the respondent-level file records
only as a count. Quantity forced: the population share of incidents carrying a characteristic, where the
office collects detail for at most a fixed number of incidents per respondent, so the incidents above
that cap have no form at all and the share is latent for them. **It dies before a world exists.** The
construction that corrects the share is one weight per form equal to the respondent's own incident count
over the number of forms, and that count is a shipped column of the respondent file. So the designed
construction **is** the one-divide route on the forcing file's plainest column, which is not a correlation
to measure but an identity, and it is the field's own incident weight besides. **Rule earned:** where a
collection cap is applied per unit and the uncapped count is still recorded, the cap's correction is the
recorded count divided, so a cap can only carry a stump where the uncapped count is itself unrecorded.

### Candidate 14, a tail share freed of within-unit variation, killed as a spent driver (2026-10-20)

(Architecture 10, screen 3, paper.) Forcing file: the repeat-measurement subsample, which pins the
within-unit day-to-day variance that nothing else pins. Quantity forced: the share of the population
whose usual level sits beyond a requirement, latent because every unit is measured on a short run of days
and the within-unit variance inflates both tails, which is the field's own usual-intake problem and the
reason a single-day count overstates inadequacy. The artifact was to be the number of collection days
falling for burden reasons, which fattens the tails with no change in the truth. **It dies on task202's
driver, drawn two days earlier**: the distribution of unit averages carries the spread between units and
none of the spread within them, so every upper cut is wrong. Mine is the same variance decomposition
read from the other end, single observations too wide where task202's averages are too narrow, and with
the nouns stripped the two sentences are one insight. **Rule earned:** the within-against-between variance
decomposition of a distribution's cuts is one driver whichever end of it a design stands on, so a
candidate that moves a tail by removing or adding a within-unit variance component is spent while
task202 stands.

### Candidate 15, the match-error correction of a register-carried status, killed on measurement (2026-10-20)

(Architecture 10, screen 4, `w7_201/screen10.py`, run twice byte-identical on a designed clean truth
before any file was cut, 20 world draws.) Forcing file: the **record-linkage candidate-pair comparison
file**, one row per pair the matching run considered with its field-by-field agreement pattern and match
weight. What it pins that no other file in a survey office pins: the matching process's own **evidence**
rather than its verdict, so it is the only record from which a pair's match status can be inferred at all.
Quantity forced: the population count of persons holding a qualifying status that only an administrative
register carries while only the survey carries the population and the weights, so every published figure
runs through a probabilistic link and no record states any pair's true match status. The anomaly is
whether a quarter's movement in the published count is the population or the link. The designed decisive
step recovers each key-quality stratum's own false-match and missed-match rates from the score mixture,
undoes the dilution of each stratum's measured share toward the register's own average, and weights the
corrected share to the frame count rather than to the linked count.

It cleared the screens the contract names as biting on this cell. **Screen 1:** the correcting input is
not one scalar but twelve numbers, a false-match rate and a link rate per key-quality stratum, and the
record identifies them in **6 of 6** strata, so neither horn fires. **Screen 3:** the attaining subset,
the pairs agreeing on every comparison field, is a filter and a divide and it is wrong by **28.760 per
cent on average, worst 34.422**, reaching the truth in **0 of 20** draws, because exact agreement is
concentrated in the well-keyed strata whose status prevalence is lowest. **Screen 6:** the graded
figure's denominator is the frame count, records-fixed, so neither the exact-arithmetic horn nor the
estimated-per-unit horn applies. **Screen 7:** the decisive step settles none of the estimand's five
parts, which are filed as the number of persons in the population holding the status at the reference
date, and two methods of estimating that one quantity stand. **Screen 8:** the graded object is a
population count under a banded verdict, not a level at a selected unit.

**It dies on screens 2 and 5, and they are the same number from both sides.** The easy route, weighting
up the linked records, errs **3.289 per cent on average** and reaches the truth in 0 of 20, so there is a
move available. But the first reflex, holding the linked pool to every recorded attribute by computing
the status share **within** each key-quality stratum and reweighting to the frame, errs only **0.316 per
cent on average, worst 0.413**, and lands within 1 per cent in **20 of 20** draws, with
**corr(decisive answer, full-adjustment answer) = +1.0000**. The one-line route on the forcing file's own
plainest column, scaling each stratum's linked count up by the inverse of its own link rate, returns the
identical figure, **+1.0000**. The reason is arithmetic rather than tuning: the weighted missed-match
rate is **0.2112** against a false-match rate of **0.0282**, a ratio of **7.50x**, and a statistics office
thresholds its matching conservatively, so the correction is dominated by the missed-link side, which is
exactly the link rate the office publishes as a quality indicator. Driving the false-match rate up to
where it would carry the decision is the one dial, and it buys the lever by making the office's own
matching implausible. The golden's family is fine, six false-match-rate estimator forms spreading
**0.560 per cent** of truth against a lever of 3.028, **lever over spread 5.408**, so determinacy was
never the problem. **Rule earned:** a correction built on an office's own process log cannot hold where
the log's headline rate is the correction's dominant term, and a quality framework that requires the rate
to be published makes that the normal case rather than the exception.

**The axes failed independently, and the window had moved twice under the pass.** `guard.py check` on the
candidate's honest card returned three BLOCKs: `ban.pattern` on decisive G12 and `ban.artifact` on
`monitoring_export`, both against **task250**, which registered after the wave's window update was
written, and `test.same_driver_older` on gap `population` plus pattern G12 plus Gate G
`method_or_model_selection`, a signature spent in five earlier builds (task196, task255, task268,
task456, task462). No relabelling was attempted, since an axis ban is not clearable by differentiation
and the mechanism was already dead. **task471, registered the same day, is record linkage as its own
task type**, which is a fourth and independent reason not to draw linkage on any cell this sitting.

### The survey-office process-log direction, screened out (2026-10-20)

Four candidates, four deaths, no card registered, no file cut, no git write. Three findings carry forward.

**On the ground.** The five shapes the corpus records as having survived on coarse-grained ground are each
already spent on this objective: a unit of analysis (task184, task192), an audit subsample's transported
error rate (task192), the uncertainty of a paired difference (task195), a construction over orderings
(task193), and a density from grouped tests with the pooling fixed by the design (task188). The sixth
door, a decisive step that is a unit-of-analysis choice, is closed from the other side, because
`grain_or_unit` is an axis ban this sitting (task269 and task202 carry it) and an axis ban does not clear
by differentiation. With `uncertainty_hold` withdrawn on this objective, `maturity_censoring` blocked by
task471, and `population_selection`, `time_semantics` and `decomposition_attribution` blocked by the live
window, the strategies left on this cell are `causal_design`, `binding_constraint`,
`forecast_method_backtest`, `composition_mix` and `other`, and the first of those meets contract screens
4 and 5 head on.

**On the procedure.** The inverted draw was run exactly as prescribed, the file enumerated first and the
proxy screen before any separation, and it still died, which is information about the inversion on this
cell. Architecture 9 earned the inversion a fourth clause from two deaths at -0.9681 and +0.9407.
Architecture 10 adds the reason the clause bites so hard here: the forcing files on survey ground are
production logs, and the office publishes each log's own rate because its quality framework requires it,
so the scalar precis is not something a world can be drawn without. **A draw on this cell has to force
its quantity from a file that is not a production log**, or accept that the proxy is shipped.

**On the axes, settled for whatever follows.** Two probe cards on this cell both PASS at exit 0 with no
BLOCK and no WARN and a nearest driver of 0.08: `gap objective` with generator `G16`, gate_g
`confirm_surface_read`, shape 18 and strategy `causal_design`, and `gap rule` with generator `G8`, gate_g
`binding_constraint`, shape 13 and strategy `other`. So the window on
`survey-research-official-statistics` / `anomaly-detection` is open and what the objective is short of is
a mechanism, not an axis, which is the same verdict architecture 9 returned on protest-event ground.
Personas drawn and never typed, `guard.py names --geo Finland --seed 201`, locale fi_FI: Einari Kivinen,
Aatos Karppinen, Lea Pakarinen, Tuomas Räisänen, Tauno Seppänen, Esteri Heinonen, Birgitta Lehto, Anneli
Järvelä, Julia Hyttinen, Miika Juntunen. One tool note alongside them: the extended locale map resolves
Finland to fi_FI, so the earlier en_US fallback finding does not apply to this geography.

**The thirteen `## Three rules` lines for candidate 15, with the failures said plainly.**

- **Task type:** `survey-research-official-statistics` / `anomaly-detection`, which the taxonomy lists
  under AD and which is the only task type in this domain that serves the objective. PASSES.
- **Domain test:** the deciding quantity is the population count of a status carried only by an
  administrative register and reached only through a probabilistic link, which official statistics
  estimates by decomposing the matching run's candidate-pair score distribution into its match and
  non-match components. **DOES NOT PASS.** The measured construction collapses to one reweighting within
  recorded strata, and a reweighting within strata reads the same with any field's nouns in it, so the
  domain is a backdrop once the measurement is in.
- **Swap:** "whether the quarter's movement in the count of persons holding the status is the population
  or the link" becomes, with hospitals for persons and admissions for status, a sentence that still reads
  correctly. **DOES NOT PASS**, for the same reason.
- **Layer 1:** frame vintage against the reference date, identifying fields with real variant structure,
  status spells read at a point-in-time reference date, one export in thousands. Nothing placed to be
  caught. PASSES.
- **Layer 2:** `estimation_fit`, the correction of an estimated share for match error recovered without a
  validation subsample. The family is right and the instance is dead.
- **Decisive step:** recover each key-quality stratum's own false-match and missed-match rates from the
  pair-score mixture and rebuild the count on the frame rather than on the linked set. **DOES NOT PASS:**
  measured, the step moves the answer 3.029 per cent while the first reflex moves it 2.713 of that, at
  correlation +1.0000.
- **Not semantics:** reading the register's status field, the agreement flags and the match weight
  correctly still leaves the linked share diluted toward the register average. PASSES on its own terms.
- **Not rule application:** no filed rule performs the mixture decomposition. PASSES on its own terms.
- **Analyst test:** a strong analyst computes the linked status share within every recorded key-quality
  stratum and reweights to the frame, and files a figure **0.316 per cent** from the truth. **DOES NOT
  PASS:** the easy route's answer is the golden to three figures, so there is no wrong answer to name.
- **Estimand:** the number of persons in the population holding the qualifying status at the reference
  date, filed in the release specification with population, outcome, window, unit and comparison.
  PASSES, and survives contract screen 7.
- **No decoy:** nothing is planted; no memo, draft or stakeholder figure argues for a step, and the
  published count is correct as published. PASSES.
- **No certified replay:** the match-error rates are recovered from the matching run's own score
  structure, not by reproducing certified or published figures. PASSES.
- **Lesson:** what a model would learn is that a link's missed matches and false matches bias an
  estimated share in opposite directions. **DOES NOT PASS as a lesson worth a build**, because the
  measurement shows the lesson is reachable by stratifying on the recorded key-quality attribute, which
  is the opponent's first reflex, and because task471 now holds record linkage as its own task type.


**Architecture 11, wave 8 allocation (`education-learning-sciences` x `anomaly-detection`, `causal_design`):
rejected at the pairing, before any mechanism search.** The allocated client domain carries no task type
that serves anomaly detection. Its seven task types serve descriptive-distribution, experiment-causal, etl,
forecasting and root-cause only, so `guard.py check` returns `BLOCK three_rules.task_type ... serves
forecasting, not anomaly-detection: the domain would be a backdrop`, with the fix line naming the two
escapes and closing both: "draw a task type of education-learning-sciences that serves anomaly-detection
(none in this domain), or another domain". `precut.py`'s `Task type:` line refuses it on the same rule, so
the `## Three rules` block cannot be written to pass. No screen, harness or world could have changed this,
and the education ground is closed for this objective by the taxonomy rather than by a measurement.

### Candidate 16, a per-case correcting factor varying only between candidates, killed on measurement (2026-10-23)

(Architecture 11, screen 0, `scratchpad/w11_201/floor_screen.py`, run twice byte-identical on a coupled
clean truth before any file was cut, 20 world draws of 12 candidates.) The briefed shape: a correcting
quantity one per case, forced by a second file at a finer grain, no case escaping it. Here the factor's
level differs by candidate and not by case within it. The raw total dies as designed (1 of 20 on the
designated three, corr +0.4992), and **one group-by on the second file reaches the designed set 14 of 20
at corr +0.9708 with a maximum absolute difference of 0.0247**. **Rule earned:** the part of a per-case
factor that defeats the raw total is its between-candidate level, and that level is one group-by, so the
same variation that buys the ladder hands the answer to a one-line route.

### Candidate 17, the factor a deterministic power of the case's own size, killed on measurement (2026-10-23)

(Architecture 11, screen 0, same harness.) The factor rises with the case's size uniformly across
candidates and carries no component of its own, so the within-candidate covariance of base and factor is
first order and the between-candidate level is flat. It dies three ways at once: the per-case divide is
then a **power transform of the observable**, so five licensed exponents reach the designed set 5 of 20 and
the designated top 9 to 15 of 20 (the free-exponent death task198's architecture 11 earned); the
mean-factor group-by reaches it 11 of 20 at corr +0.9434; and rho is 0.7255 against the floor's 0.80, so
the raw total is still bound at +0.8571. **Rule earned:** a factor with no independent component of its own
is a function of the quantity it corrects, so the construction is a transform whose exponent nothing files.

### Candidate 18, the coupling's strength differing by candidate, killed on measurement (2026-10-23)

(Architecture 11, screen 0, same harness, plus the 729-cell joint sweep.) The one cell the pincer leaves:
the factor keeps its own independent component, its level is flat across candidates, and the strength of
its coupling to the case's size differs by candidate, so only the per-case divide is right. Measured, the
mean-factor group-by still reaches the designed set 5 of 20 at corr +0.7778, and the designed route itself
recovers the world's elevated three only 3 of 20. **The sweep settles it jointly rather than marginally:
729 cells over the case-size spread, the coupling's mean and spread, the factor's own noise, its
between-candidate level, the lift and the baseline spread. 245 cells kill the raw total, 536 clear rho,
486 clear the margin, 324 have the designed route recovering the truth, and 0 cells kill every
one-group-by route. The weakest group-by cell on file sits at 3 of 20 and has the factor's own noise at
exactly zero, which is candidate 17.** **Rule earned:** the blessed shape's two requirements are one dial.
A per-case factor reorders the candidates only through its between-candidate level, which a group-by
removes, or through the within-candidate covariance, which makes it a transform of the observable.

### The identity clause, measured dead from the group-by side (2026-10-23)

The clause briefed as "forced arithmetically, linearly and by identity" was withdrawn mid-pass and the
withdrawal is confirmed independently here. A shipped per-case factor makes the designed construction the
cheapest one-group-by route (the orchestrator's own measurement: corr +1.000000, maximum absolute
difference exactly zero), which is rule application; and screen 0 adds that it fails the group-by pincer
too, at 0 of 729 cells. Both horns, one clause.

### Candidate 19, the factor unobserved and recovered with no free parameter, killed on measurement (2026-10-23)

(Architecture 11, screen 0b, `scratchpad/w11_201/recovery_screen.py` and `dense.py`, each run twice with
identical output.) The corrected shape: the per-case factor is unobserved, the second file carries the
case's own trajectory at a finer grain, the design fixes the form as linear so least squares returns one
answer, and the second file's sampling times are clustered per case so the per-case mean of its rows is
biased by the clustering times the slope. One dial, both ends, nothing between them. **Symmetric sampling:
the per-case mean of the second file's rows reaches the designed set 20 of 20 at corr +0.999799, so the fit
is decoration. Clustered sampling: the per-case mean route drops to 15 or 16 of 20 on the designed set and
reaches the world's own quantity 20 of 20 against the designed fit's 15 or 16, so the ladder inverts and
the cheap route is the better estimator. Thin and steep: every cheap route dies at 1 to 3 of 20 and the fit
dies with them, recovering the truth 0 of 20, because three to six rows a case cannot carry it.** The dial
counted jointly over 81 cells: 9 kill every cheap route, 27 have the fit recovering the truth, **0 do
both**. A density sweep to 150 rows a case (24 cells, task197's own region) returns **0 of 24**, and the
decisive cell is explicit: at a candidate-varying clustering of 0.40 and a slope spread of 1.20 the
per-case mean route dies at 3 of 20 and corr +0.2292, and **the candidate-level group-by survives in the
same cell at 14 of 20 and corr +0.9038**, rising to 18 of 20 and +0.9275 when the baseline is tightened to
widen the margin. **Rule earned:** making the correcting quantity unobserved restores the analysis and
restores nothing else, because the recovery's precision and the cheap route's error are set by the same
two numbers, the rows a case and the trajectory's slope.

### The driver is spent in task452's lineage, at the text screen's blind spot (2026-10-23)

`guard.py nearest` on the probe card scores the candidate driver at **0.08**, under the 0.12 WARN floor,
with **task452 v1 (lineage) nearest**: "a period total of the product of two series, one recorded at every
interval and one sampled on a few intervals that mostly catch the quiet state; the sampled factor rises
with the recorded one, so carrying the sampled values across the unsampled intervals, by averaging or
interpolating, misprices the busy intervals that carry most of the total". With the nouns stripped that is
candidates 17 to 19 exactly, and the live region screen 0b leaves (a dense second file, a steep per-case
slope, asymmetric sampling) is the region task452 v1 and task197 already occupy. This is the third time
this slot has met the 0.08 signature, after candidate 12 (task237) and candidate 14 (task202).

### The mandated-indicator filter, answered in writing for every AD ground (2026-10-23)

The filter architecture 10 earned was applied before any candidate was scored, by writing down who is
obliged to publish what about the process whose record forces the quantity. It drops
`survey-research-official-statistics/anomaly-detection` (the office publishes the response, link, edit and
imputation rates), `epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection`
(surveillance completeness and timeliness indicators), `pharmacology-pharmacoepidemiology-safety/safety-signal-detection`
(the reporting rate against exposure, in every periodic safety report),
`healthcare-delivery-health-economics/provider-quality-risk-adjustment` (the risk-adjusted indicator is
the mandated publication, which task194's architecture 6 measured),
`physical-environmental-sciences/environmental-monitoring-exceedance` (monitor data availability, and spill
duration returns), `criminology-justice/crime-incidence-hotspot-analysis` where the forcing file is the
force's own occurrence record (recording-accuracy audit), and
`human-factors-ergonomics/safety-incident-error-analysis` (the recordable incident frequency rate). It
passes a ground only where the forcing file belongs to a party with no publication duty over it, which on
this objective means a provider's, a scheme's, a laboratory's or a counterparty's record read by someone
else. **The filter is sound and it is not the binding constraint: candidates 16 to 19 were drawn on ground
that passes it and died on the group-by pincer instead.**

### The cell audit, which closes the ground question for this objective (2026-10-23)

Read before any candidate: every one of the 14 AD-serving task types carries a live sibling at stage 1 or 2
except `healthcare-delivery-health-economics/payment-claims-health-plan-analytics` and
`provider-quality-risk-adjustment`. The first has been screened to death twice by task182, whose
architectures 6 and 7 are recorded in its own note and which no `guard.py` subcommand surfaces: six
affordances across two file pairs, the enumeration closed at four exhaustive forms (a conversion, a
completeness estimate, a valuation, a population restriction), with `guard.py check` returning PASS at a
nearest driver of 0.06 on each. The second is the risk-adjustment publication trap above. **So the ground
question on this objective is settled and the driver question is the only open one, which is what
`guard.py coverage` says in its own words.**

### Architecture 12, step 1: the preserved lead is dead, and the harness understated its death (2026-10-23)

(Harness `scratchpad/w11_201/floor_screen.py` re-run twice, both at md5 `08d4d741f149b9774befea96ce1ed8dd`,
byte-identical with the preserved `run1.json`, so architecture 11's measurements stand. New harness
`scratchpad/w12_201/lead.py`, run twice byte-identical at md5 `c96070e928fe513111631dfba982206d`.)

The lead (`sd_log_s` 1.3, `sd_log_A` 0.12, `sd_log_F` 0.05, `beta_sd` 0.6, `beta_mean` 0.0, lift 3.5;
designed route 19 of 20, raw 2 of 20, margin 1.7213, rho 1.3031) was to be re-read to decide whether its
two failing conditions, the group-by route at a worst 3 of 20 and the power route at a worst 7 of 20, are
a property of the cell or of the harness's route definitions. **Both answers are now measured, and they
point opposite ways: the group-by failure is a grid-range artefact that is repairable, and the power
failure is a cell property that the harness understated by a factor of three.**

**The scoring is not the artefact.** Every route's `set_hit` is scored against the top three of the
designed statistic, which is a quantile of the designed statistic itself, so it was the first suspect.
Measured at the lead with both scorings side by side, they differ by at most one draw in twenty on every
one of eleven routes (raw 2 against 2, mean-factor 3 against 3, median-factor 1 against 1,
harmonic-factor 1 against 1, power-0.50 7 against 8, designed 20 against 19). The reason is arithmetic:
the designed route recovers the world's own elevated set 19 of 20, so its top three IS the truth in 19 of
20 draws and the two comparators coincide. **Rule earned:** scoring a reflex against the designed
statistic's own answer set is only an artefact where the designed route is a poor recoverer of truth;
where it recovers 19 of 20 the two scorings are the same measurement, and the defect caught elsewhere
today (a reflex scored against a quantile of its own statistic) does not apply.

**The power route is a cell property, and the harness swept the wrong range.** `floor_screen.py` scores
`sum(o_i ** q)` for q in 0.50 to 0.90 only, and at those exponents the route peaks at 7 of 20. Extending
the grid downward, with nothing else changed: **q 0.30 reaches the truth 18 of 20, q 0.20 reaches it 20 of
20 at corr +0.9167, and q 0.10 and q 0.05 reach it 20 of 20 at lift over noise 5.375 and 5.561, against
the designed route's own 4.601.** So the cheapest competing route is not merely alive, it is **a better
estimator of the decision's signal than the designed construction**, and the ladder is inverted. The
harness understated the strongest cheap route by 13 of 20 draws.

**The mechanism, which closes the whole `floor_screen` shape rather than this cell.** As q falls,
`mean(o_i ** q)` converges to ranking on `mean(log o_i)`, the per-case geometric mean of the observable.
In this generating process `log o_i = log A_u + log F_u + (1 + beta_u) log s_i`, and the latent size's log
has mean zero over cases, so the correcting factor's whole contribution to the geometric mean is
`beta_u` times the sample mean of `log s`, which is noise of order `sd_log_s` over the root of the case
count and not a distortion of the candidate's level. The lift sits on `A_u`, a candidate-level
multiplier, so it survives the transform undiminished in relative terms. Against that, the designed route
is the arithmetic mean of a heavy-tailed per-case quantity, whose relative sampling error is
`sqrt((exp(sd_log_s ** 2) - 1) / k)` against the geometric mean's `sd_log_s / sqrt(k)`, and the first
exceeds the second at every positive dispersion. **Rule earned:** where the decision's lift sits on a
candidate-level multiplier and the designed quantity is a sum over cases of that multiplier times a
heavy-tailed per-case term, the per-case geometric mean of the raw observable is a one-group-by route that
estimates the lift with LESS noise than the designed construction estimates its own quantity. The
correcting factor is irrelevant to it. This is the same death as candidate 17 (a power transform of the
observable whose exponent nothing files) reached from the estimator-precision side, and it does not need
the factor to be a deterministic power of case size.

**The factor's own independent component is not what buys the group-by kill.** Every cell in
architecture 11's `best_group_by` list carries `sd_log_eta` exactly 0.0, which read as candidate 17 again.
Measured at the lead with `sd_log_eta` swept 0.00, 0.10, 0.20, 0.40, 0.60, 0.80: the worst group-by route
moves only 3, 3, 3, 4, 4, 4 of 20 and the best power route holds at 19 of 20 on the set and **20 of 20 on
the truth at every one of the six**, with its lift over noise 5.561, 5.595, 5.598, 5.521, 5.363, 5.152
against the designed route's flat 4.601. So the eta association in the sweep's own best cells is
incidental, and the geometric-mean route is indifferent to the factor's independent component.

**The group-by failure is a grid-range artefact, and repairing it changes nothing.** `beta_sd` was capped
at 0.60 in the 729-cell sweep, which is why `pass_group_by` came back 0 of 729 with a floor of exactly 3:
the condition is reachable, just not on that grid. Extending it at the lead, `beta_sd` 0.90 gives worst
group-by **2** of 20 with raw 1, margin 1.7213, rho 1.9046 and the designed route still 19 of 20, and
`beta_sd` 1.20 gives worst group-by 2 with raw 0. So the designed, margin, raw, rho AND group-by
conditions hold together off the grid, which is the first time five of the six have held in this lane.
**The power route does not follow**: 19, 19, 18, 14 and 12 of 20 at `beta_sd` 0.60, 0.90, 1.20, 1.60 and
2.00, never reaching the condition, and still 12 of 20 at a coupling spread of 2.00 that no record would
carry. The two failures are therefore not one dial, and the one that is repairable is not the one that
kills.

**Why no setting exists, stated as the shape's own arithmetic.** The group-by route is killed by making
the correcting factor's coupling to case size differ strongly by candidate, because a candidate-mean
factor cannot undo a per-case power. The geometric-mean route is immune to exactly that move, because a
power of the case's size enters the log-mean through the sample mean of `log s` alone, which the coupling's
spread does not inflate. So the dial that buys the group-by kill spends nothing against the route that
actually reaches the answer, and the route that actually reaches the answer is not reachable by any dial
in the model, because it beats the designed construction on estimator precision rather than on bias.
**The lead is refused, and `floor_screen.py`'s shipped-per-case-factor shape is refused with it.**


### Architecture 12, step 2: the named harness artefact is real, and it sits in `recovery_screen.py`, not in the lead's own screen (2026-10-23)

(`scratchpad/w12_201/recov2.py`, a faithful re-implementation of `recovery_screen.draw_world` in the
same RNG draw order; it reproduces all four of that harness's cells exactly, asserted in the output's
`fidelity` block, and runs twice byte-identical at md5 `a9842b50ac3a41d9f88aa61963996af2`.
`recovery_screen.py` and `dense.py` were both re-run twice and both reproduce their preserved output at
md5 `b302c85624a49e14f6a022cad88d44b4` and `13b3038ebf4f22559d29e33eb2539742`.)

**The artefact.** `recovery_screen.py`'s dial condition `pass_cheap` is built on `set_hit`, which scores
each cheap route against the top three of the DESIGNED statistic, and the designed statistic in that
harness is the fitted recovery `D_fit`, not the world. In the extreme cells the fit is broken: the
design-fixed least squares is extrapolated to the span mid-point from sampling times clipped into
`[0, 1]`, so with a candidate-level clustering of 0.40 and a slope spread of 1.20 the fitted value
falls to the `1e-9` clamp and `o / fhat` explodes. The tell is in the harness's own output and was
read past: **cell D4 reports a margin of 478,516.257 and the designed route recovering truth 2 of 20**,
and the lead's parameters on the same dials report a margin of 271,329.74 and the designed route 0 of 20,
against a normal 1.5 to 1.8. Where the designed statistic is broken its top three is not the truth, so
the condition scored the cheap routes against a broken comparator. **Measured in one cell at the widest
possible gap: the per-case geometric mean of the raw observable scores 0 of 20 on the set and 20 of 20
on the truth.** `dense.py` computed a truth-scored pass as well (`pass_all_on_truth` 0 of 24), so its
verdict stands; `recovery_screen.py`'s own 81-cell dial does not, and its nine cells reported as
killing every cheap route are not evidence. **Rule earned:** where a screen's comparator is the
designed route's own OUTPUT rather than the world's truth, a cell that breaks the designed route
reports every reflex as dead. Score on the world, and read a margin in the hundreds of thousands as a
broken estimator rather than a wide one.

**And the artefact does not rescue the lead, because the lead's own screen does not carry it.**
`floor_screen.py`'s comparator is `B / M`, the world's own designed quantity, and at the lead the
designed route recovers the truth 19 of 20, so its top three IS the truth in 19 draws of 20 and set and
truth scoring differ by at most one draw on every one of eleven routes.

### Architecture 12, step 3: the lead at the licensed shape, where the designed route never works (2026-10-23)

Carrying the lead's parameters onto the shape the client licenses (the correcting quantity unobserved,
recovered by a construction the design fixes with no free parameter), over 36 cells of the recovery
dials: **`pass_designed` is 0 of 36.** The designed fit never reaches 18 of 20 on the world's truth,
because `sd_log_s` 1.3 makes the candidate's arithmetic sum too noisy to rank on, while the per-case
geometric mean of the raw observable reaches the truth **17 to 20 of 20 in every one of the 36**, at a
lift over noise flat at 5.05 to 5.11 against the designed route's 0.17 to 5.13. At the harness's own
base dials the reading is explicit: designed fit 17 of 20 at lift over noise 4.017, geometric mean 19 of
20 at 5.146, and the geometric mean taken after dividing by the candidate's mean factor 20 of 20 at
5.514. The ladder is inverted on the licensed shape as well as on the shipped-factor one.

### Architecture 12, step 4: the three-jaw pincer, counted jointly over 41 cells, 0 passing (2026-10-23)

(`scratchpad/w12_201/pincer.py` md5 `160dc8cc5522c367bead663b37320d05` and `corner.py` md5
`ab7d2c16820d4a95d624ec99b65c84be`, each run twice byte-identical, every route scored on the world's
truth.)

The shape has three jaws, and the third is new. **Jaw 1** (candidate 16): the factor's candidate-level
LEVEL is one group-by, so level variation hands the answer to a mean-factor route. **Jaw 2** (candidates
17 and 18): the factor's per-case COUPLING to case size makes the designed route a power transform of
the observable. **Jaw 3** (new): the per-case geometric mean of the raw observable estimates the
candidate-level multiplier better than the designed arithmetic sum estimates its own quantity, and a
power of case size leaves the geometric mean almost untouched, because the latent size's log has mean
zero over the candidate's cases. Jaw 1 is escaped by moving the factor's variation out of its level and
into its coupling; jaw 3 is escaped by the reverse. **So the two are one dial with no middle, and the
joint count says so:** over 25 cells of the factor's level against the coupling's spread,
`pass_group_by` holds in 10, `pass_power` in **0**, `pass_geomean` in **1**, and
`pass_group_by and pass_geomean` in **0**. The single cell where the geometric mean dies has the
factor's level dispersion at 1.00 and the coupling's spread at exactly zero, which is where the
mean-factor group-by reaches the truth 19 of 20. **The corner probed on its own**, the factor's level
dispersion 1.00 to 2.40 against the coupling's spread 0.90 to 2.40 and the cheap set widened to include
the geometric mean taken after the group-by: 16 cells, `pass_raw` 16, `pass_group_by` 16, `pass_power`
12, `pass_designed` 16, `pass_margin` 16, and **`pass_geomean` 0 of 16**, the geometric mean holding at
3 to 7 of 20 everywhere. `pass_all` is **0 of 41 cells** across both sweeps and the binding condition is
jaw 3 in every one.

**The precision arithmetic behind jaw 3, which is why no dial reaches it.** At `k` cases a candidate's
arithmetic mean of a log-normal base has relative sampling error `sqrt((exp(sd^2) - 1) / k)` against the
geometric mean's `sd / sqrt(k)`, and the ratio is 1.0314 at `sd` 0.35, 1.0971 at 0.60, 1.2412 at 0.90,
**1.6171 at 1.30** and 3.6605 at 2.00. So the dispersion law 4 demands (sd of the log factor at or above
about 1.4, which needs a comparably dispersed base to keep rho under control) is the same dispersion
that makes the geometric mean the better estimator. **Law 4's window and jaw 3's kill are one dial read
from opposite sides**, which closes the multiplicative-correction shape from a fourth direction after
the floor, the aggregation and the precision pincer.

**Laws 1, 2 and 4 on the lead, as the brief required.** Per case the lead carries sd(log factor)
**0.7816** against law 4's ceiling of about 1.4, so it is **under the ceiling**, and a per-case rho of
**0.5987**, under law 1's 0.80 floor. Its reported rho of 1.3031 is a candidate-grain quantity: the
coupling's spread converts a modest per-case factor dispersion into a large candidate-level distortion,
which is a real mechanism and is exactly the mechanism jaw 3 is immune to. On law 2 the lead runs the
other way from the law's stated form, rho at candidate grain **rising** with the case count (0.6661 at 3
cases, 0.9422 at 10, 1.2017 at 30, 1.3031 at 40, 1.7471 at 100), because the distortion is the
candidate's own coupling exponent and does not average away. That is law 2's own systematic mix term,
and law 2's warning is what happens: the mix term is reachable, here by a power transform or a log-mean
rather than by a stratification. **The case count pincers it from both ends:** the designed route needs
30 or more cases (3, 11, 17, 19, 20 of 20 at 3, 10, 30, 40, 100 cases) and the geometric-mean route
becomes precise on the same count (3, 6, 19, 20, 19), so there is no count at which the designed route
reaches 18 and the cheap route stays under 3. **0 of 6 case counts pass.**

### Architecture 12, step 5: the one escape jaw 3 leaves, measured dead from both ends (2026-10-23)

Jaw 3 recovers the candidate's level only up to a monotone transform, so `stumping`'s own exit is a
LEVEL-dependent graded object, and the sharpest is the count of a candidate's cases crossing an
ABSOLUTE limit. Screened with the limit's own value, never a quantile of any route's statistic.

**On the shipped-factor shape it works and is worthless.** Every cheap count is wrong in 20 of 20 worlds
(the raw count off by 44.1 crossings of 181.4, the mean-factor group-by by 50.1, the median-factor
group-by by 40.7, the pooled reading by 60.6) and the designed count is **exact in 20 of 20**. The
exactness is the tell: with the factor shipped per case the count is one divide and one comparison on
two shipped columns, which is the withdrawn identity clause and rule application.

**On the licensed shape the same exactness is unreachable.** (`scratchpad/w12_201/escape.py` md5
`a15aebe7f95f747c89ea4e74b6dad76d`, run twice byte-identical.) With the factor unobserved and recovered
by the design-fixed fit, over 54 cells of the recovery dials: **`pass_designed` is 0 of 54**, the best
cell reaching the exact count in 10 of 20 and only with a 60-row-per-case archive at a measurement noise
of 0.05. A count across a limit is discontinuous, so any per-case estimation error misplaces the cases
sitting near the limit, and the recovery always has one. **Both ends measured: 20 of 20 exact with the
factor shipped, at most 10 of 20 with it recovered. The graded count's exactness and the construction's
non-triviality are one dial.**

**And banding the count does not separate the designed route from the cheapest one.** The per-case mean
of the second file's own rows, one group-by at case grain with no construction, carries a relative count
error of 0.0236 against the designed fit's 0.0235 at the lead's parameters, 0.0400 against 0.0386 at the
harness's base, and 0.1735 against 0.1358 at a thin second file: the fit is between 1.0 and 2.5 times
better, never more, so any band wide enough to admit the fit admits the cheap route. The band would
separate the fit only from the raw, pooled, candidate-group-by and candidate-geometric-mean readings, at
0.23 to 0.74. **That is candidate 19's death (the fit is decoration beside the per-case mean) restated in
the level-dependent object's clothes, so the escape closes on the route that closed candidate 19.**

**Verdict on the preserved lead: refused, as a cell property.** Its two failing conditions are not one
thing. The group-by failure at a worst 3 of 20 was a grid-range artefact (`beta_sd` capped at 0.60 in the
729-cell sweep, which is why `pass_group_by` came back 0 of 729 with a floor of exactly 3) and is
repairable at `beta_sd` 0.90, where five of the six conditions hold together for the first time in this
lane. The power failure at a worst 7 of 20 was understated threefold by a q grid that stopped at 0.50,
and corrected it is 20 of 20 on the truth at q 0.05 to 0.20 and a better estimator than the designed
construction. **Nothing in the model reaches jaw 3, on either shape, on the ranking object or on the
count object, over 131 cells measured this pass.** Architecture 12 therefore refuses rather than draws,
and the direction for architecture 13 is not another cell of this shape: it is a decisive step that is
not a per-case correction of a per-case observable at all.


### Architecture 12, the handover: jaw 3 is new to the corpus, and the window is open on the wrong axis again (2026-10-23)

**`guard.py slots geometric log-mean logarithm --min-terms 1` places jaw 3 as a new law.** Three slots
have met the per-case geometric mean before and all three met it from the determinacy side, as a
convention that gives the same call: task272's rung R2 is "the same, geometric month means" naming the
golden 16, task194 measured a geometric mean of 0.480 against its arithmetic form with "both forms named
the same unit", and task243's SF18 reads the persons reaching each age as a geometric or an arithmetic
mean at "same call, inside every interval". That agreement is jaw 3 seen from the other end and taken as
harmless, which is what it is for a convention and is not what it is for a reach: none of the three
recorded that the geometric form is the better ESTIMATOR, so none of them priced it as a route. task183's
own dial is the nearest relative, 0 of 300 settings with "a cheap count form lands the call in all 32"
of the unanimous cells. **So jaw 3 is drawn from this pass rather than rediscovered, and it belongs in
`stumping` beside laws 1 to 4 as the fourth closure of the multiplicative-correction shape.**

**The window, read at the moment of this refusal rather than copied.** `guard.py recent` puts the three
live cards at task275 (`survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment`,
descriptive-distribution, shape 10, pattern G3, `population_selection`, `compliance_or_audit`), task483
(`survey-research-official-statistics/census-register-administrative-data-quality`, etl, shape 16,
pattern G19, `grain_or_unit`, `programme_officer`) and task482
(`supply-chain-logistics/transportation-network`, etl, shape 07, pattern G12,
`method_or_model_selection`, `procurement_lead`). So **pattern G12 is inside the ban window**, which
matters for this slot specifically because its own spent architecture 6 carried G12; the shape ban
reaches the last two, so shapes 16 and 07 are closed; and no anomaly-detection subdomain sits in the
window, so `ban.pairing` and `ban.subdomain` cannot fire on any AD cell, exactly as architecture 11
found. Occupancy is not the constraint here and has not been for three passes. **The driver is, and the
four laws plus jaw 3 now say which drivers are unavailable rather than merely untried: any decisive step
that corrects a per-case observable by a per-case factor is closed, whether the factor is shipped (rule
application) or recovered (the fit is decoration beside the per-case mean), on the ranking object (jaw 3)
and on the level-dependent count object (exactness and non-triviality are one dial).** Architecture 13
starts outside that family or not at all.


### Architecture 13, step 0: the axis window measured on a probe card, not read off the brief (2026-10-24)

The axis the author set for this pass is the one structure `stumping` records as having opened a two-ended
dial: a construction whose UNKNOWNS ARE STRICTLY FEWER THAN ITS CASES, so the data overidentifies it and
the estimator family closes by arithmetic rather than by a filed sentence. The assigned ground is a few
ASSESSOR parameters identified across many subjects by an incomplete overlap design, disjoint from two
siblings hunting the same axis on instrument-and-laboratory comparison and on handler-or-route effects.

**Probe card** at `scratchpad/w13_201/probe_card.json` (never registered), cell
`survey-research-official-statistics/anomaly-detection`, shape 01, decision `designation_set`,
strategy `decomposition_attribution`, role `field_unit_lead`, artifact `operations_log`, org
`research_or_statistics_office`, forum `operations_desk`, forcing event `season_or_peak`, people drawn
from `guard.py names --geo "United Kingdom" --seed 201`.

**Verdict: NO AXIS BAN FIRES ANYWHERE ON THIS DRAW.** Not `ban.subdomain`, `ban.pairing`, `ban.strategy`,
`ban.shape`, `ban.role`, `ban.artifact`, `ban.calibration`, `ban.spine`, `ban.forum`,
`ban.forcing_event`, `ban.org_family`, `ban.pattern`, `people.*` or `tell.names`. Measured rather than
assumed: task125's card on this same subdomain registered 2026-10-23T17:50:29Z and does **not** reach the
window, and the mid-wave WINDOW_UPDATE table (2026-10-20) is stale in both directions again. So for the
fourth consecutive pass on this number occupancy is not the constraint.

**The two BLOCKs that did fire are structural triples, and one of them names a concurrent sibling.** With
`gap: population` first the card BLOCKs on `test.same_puzzle_older` (task181 v4, task229 v1, task98 v3)
and `test.same_driver_older` (task103 v1 and v3, task72 v1 and v2, task81 v3, task86 v1, task90), and the
guard's own fix line says five differentiation lines is dearer than redrawing. Probed over sixteen honest
combinations of gap, pattern and Gate G: `gap: objective` first with `pattern: none` (`generators[0]` G14,
which is what the structural tests then key on) and `gate_g: decomposition_attribution` returns **WARN
only**, the warnings being `repeat.deliverables` (png+xlsx against task306) and `repeat.question_form`
(which, against task484 and task305). `pattern: E` is **not** available: with `designation_set` it BLOCKs
`test.same_puzzle` INSIDE THE BATCH against task482, which is the one collision `guard.py check` can see
and a reminder that the sibling cards are otherwise invisible to it. Free G-codes on the passing signature
are G14, G6 and G18; G1, G3, G5 and G17 all BLOCK.

**Why `objective` is the honester label and not merely the passing one.** The population is not in doubt
here: it is every site the programme visited in the window, and no row's membership is argued. What is in
doubt is what the recorded number is a measure OF, because the decision is scored on a site's own
condition while the record scores a site-and-assessor pair, and the obvious correction targets the wrong
objective by removing the caseload's real quality along with the assessor's severity. `population` stays
as the second gap, which is where the row-grain reading belongs.

**Driver text screen, for the record.** Nearest drivers 0.07 (task73 lineage), 0.05 (task189, task235 v2
and v1, task471 v2 lineage), all far under the 0.12 WARN floor, so the lexical screen says nothing and the
abstraction test has to be run by hand. The two neighbours it misses are named in the next entry.

### Architecture 13, step 1: the shared-assessor-parameter ground, REFUSED on measurement (2026-10-24)

(Harness at `scratchpad/w13_201/`: `world.py` one generating process, `exact.py` the reduced normal
equations so nothing depends on an iteration count, `screen2.py` the route table, `screen3.py` the joint
dial. Every route scored against the world's OWN truth, never against a quantile of the designed
statistic or of a fitted recovery.)

**The world, built to the axis.** Six districts, twelve assessors (two with each district as their home),
480 sites, eight visits a site, 3,840 visits. A visit goes to a home assessor of the site's district
unless it is cross-cover, when it goes to an assessor of another district. The assessor's own additive
effect is a district scoring-culture component plus an individual one; the site's level is its district's
quality plus its own. The filed comparison is each assessor's effect against the workload-weighted mean of
all assessors, the filed tolerance 5.0 points, and the graded object the set of assessors outside it. The
coupled quantities (district quality, scoring culture, severity, site level, roster, score) are all drawn
from the one process, and the roster's confound is structural rather than planted: an assessor's own mean
is their effect plus the quality of the caseload the roster gave them, whether or not culture and quality
are correlated at all (measured at a correlation of exactly zero).

**Does the process identify a few shared parameters across many cases? YES, and precisely.** Unknowns 491
(480 sites plus 12 assessors less the one location constraint) against 3,840 cases, 7.82 cases per
unknown. The analytic standard error of each shared parameter, from the reduced normal equations with the
residual sd estimated off the fit (5.99 against the world's 6.00), is **0.51 points against a filed
tolerance of 5.0**, about a tenth of the decision's own margin. That is the axis's premise confirmed, and
it is a fourteenfold improvement on the nearest measurement in the corpus: task198's architecture 2 put a
per-interviewer differential's standard error at 6.96 points against a golden rise of 3.0, because it
recovered each interviewer's differential from that interviewer's own 33 out-of-region observations, while
the joint solve here borrows every path through the connected roster. So the shape is not what killed
task198's architecture 2, and the count test is passed.

**R test, run first as the brief requires. R = 235.99 mean, 31.18 minimum, with 5.85 sign changes** over 20
mid-bin draws (and 136.79 mean, 37.34 minimum, 3.30 sign changes on the unfiltered base). The closed
per-case-correction family's identity is R = 1.000 with 0 sign changes, so **this construction is
structurally outside that family**, and for a reason that is algebra rather than tuning: the naive
distortion is a CONTRAST (an assessor looks harsh because their caseload is good, lenient because it is
bad) and the workload-weighted centring makes it sum to zero by construction, so it must change sign.

**The route table, the cheapest LICENSED member printed in the same table as the family's unanimity**
(20 draws, mid-bin clearance 3.0 standard errors either side of the tolerance, mean designated set 0.90 of
12; 542 draws tried for 20 kept):

| route | exact set | mean abs error (pts) | class |
|---|---|---|---|
| a0 each assessor's own mean score | 3 / 20 | 3.0344 | cheap |
| a1 mean deviation from the site's own mean (one group-by) | 10 / 20 | 1.3145 | cheap |
| a4 mean deviation from the district mean (one stratification) | 12 / 20 | 1.2776 | cheap |
| a5 cross-cover visits alone (the attaining subset) | 18 / 20 | 0.9304 | cheap |
| **L one-line OLS, score on assessor dummies and site dummies** | **20 / 20** | **0.4251** | **cheapest licensed** |
| a2 the designed joint solve | 20 / 20 | 0.4251 | standing |
| a3 the same with the site facet shrunk | 19 / 20 | 0.8239 | standing |
| a7 the same with medians | 20 / 20 | 0.5336 | standing |
| standing family unanimous on the set | 19 / 20 | | |

**The kill, and it is the law rather than a cell property. The cheapest licensed member and the designed
route are the SAME COLUMN**: over 59 worlds the maximum absolute difference between L and a2 is
**3.973e-12 points**, the backfitting tolerance and nothing else, because the one-line regression a
competent analyst types IS the reduced normal equations. (The shared parameter's analytic standard error
over the same 59 worlds is 0.5152 points, range 0.4911 to 0.5389.) So family unanimity (19 of 20) and the easy route landing (20 of 20) are one number read twice,
which is `stumping`'s own clause on a linear-solve construction, reproduced here on new nouns. And the
attaining-subset screen fires beside it: a filter and a divide over the cross-cover visits alone, with no
model at all, names the truth **18 of 20** at a mean absolute error of 0.93.

**The joint dial, counted jointly over 20 cells** (district culture 0.0 to 8.0 against cross-cover 0.02 to
0.25, mid-bin at 2.0 points and the designated set held to 1 to 4): **the one-line OLS reaches the truth in
78 of the 79 kept draws, and a2 is identical to it in all 20 cells.** There is no cell in which every cheap
reflex misses and the one-liner misses too.

**And the sweep's own PASS column says 8 of 20, which is a HARNESS ARTEFACT, recorded because reading it as
a pass is exactly the defect this skill already carries.** The pass condition tested `one_line_hits <= 2`
as an absolute threshold while the mid-bin and set-size filters left only **1 to 3 draws kept per cell**
(57 of every 60 draws rejected), so a cell where the one-liner hit 2 of its 2 kept draws scored as a cell
where it missed. Read against `kept` rather than against a constant, the one-liner hit every kept draw in
19 of the 20 cells. Two rules earned: a pass condition on a count is written against the cell's own kept
count, never against a constant; and a mid-bin filter that rejects 95 per cent of draws is itself a finding
(with twelve assessors and a tolerance at 5.0 points an honest world rarely clears the boundary
everywhere, so the designation object here is boundary-fragile and would have to be tuned rather than
drawn).

**The general clause, which the orchestrator closed from three further directions while this was running
and which the numbers above corroborate independently.** For a few shared parameters to be identified from
many cases, each case's observation must be a known function of the parameters of the handlers it touched,
and the organisation must SHIP which handlers it touched or nothing is identified at all. The pack is then
a design matrix plus an outcome, the link is forced by the design, and the construction is one call on the
shipped matrix. **The shipped design matrix is at once what closes the estimator family and what makes the
construction one line, so Gate C and Gate F are financed by the same object and the dial is one-ended by
construction.** The sibling's three further kills are the design's RANK rather than its case count (rank
deficient at every realistic window), the large case count being replication rather than information (and
replication buys a weighting choice that moved the designated set in 10 of 20 worlds), and R = 1.000 with
0 sign changes on its own ground. Ten shared-parameter constructions are closed with named kills and
**paired-comparison or Luce severities, which is this ground, is one of them**; the additive joint solve
measured here is another, and is a shipped build's driver besides.

**The lineage adjacency, which would have refused this ground on paper even had the arithmetic held.**
task198's architecture 2 sits on the SAME cell (`survey-research-official-statistics/anomaly-detection`),
the same objective, the same decisive gap `objective` with `population` second, the same
`gate_g: decomposition_attribution`, and its Layer 2 pattern is `own:measurer-portability-across-units`:
"a minority of interviewers work more than one region because rural workloads cross territorial authority
boundaries, so the record contains the same interviewer's own differential measured away from the region
that looks worst, which is the only thing that separates her from it". That is the incomplete overlap
roster in the same nouns. `guard.py check` passes my card at a nearest driver of 0.07 and does not see it,
because the structural triples key on the decisive pattern (G3 there, G14 here) and the driver screen is
lexical; the abstraction test sees it at once, since the latent structure, the default path and the
correcting move all map. Inverting the facets so the ASSESSORS are the decision's candidates and the sites
the nuisance does change the default path, the graded quantity and the decision, and it repairs that
architecture's standard-error death outright (0.51 against 6.96 points), but it does not touch the Gate F
kill above, so it is not drawn.

**Reproducibility.** `screen2.py` and `identity.py` were each run twice to byte-identical output
(`s2_run1.txt` and `s2_run2.txt` at md5 `8a897e220d1e73db78f487a2480d2402`, `id_run1.txt` and
`id_run2.txt` identical), and `screen3.py` ran to exit 0 once with its artefact recorded above.

**What was NOT measured, and is left recorded rather than screened:** the time-varying nuisance escape (the
sites drift inside the window, so site fixed effects is misspecified and the one-liner lands wrong). It is
not pursued because the repair is one slope per site, which is one unknown per case, the shape closed by
algebra in architecture 10's enumeration, and because the licensed drift forms (linear, by period, smooth)
reopen the estimator family on the graded designation.

### Architecture 13, step 2: the no-shipped-design-matrix direction, answered on this ground and not built (2026-10-24)

Asked whether a decisive step exists here whose licensed family has no shipped design matrix to solve, so
that the deciding quantity attaches to no unit the record labels: **on judgement-scored ground I cannot see
one, and the reason looks structural rather than local.** Every candidate enumerable on this ground falls
into one of five closed boxes. (1) An assessor's severity, a subject's level or a district's scoring
culture is a parameter of a labelled unit, the roster ships the incidence, and the construction is one call
on it, which is the refusal measured above. (2) A decision-consistency or agreement functional (the share
of subjects whose side of the filed tolerance would change on a replication of the measurement) genuinely
attaches to no labelled unit and satisfies the letter of the clause, and it is closed twice over by screens
already on file: it is a variance functional, so the lever that reorders the candidates is the variance
that randomises the quantity they are ranked on, and the determinacy screen has already measured a
discriminability statistic at 1.64 distinct designated sets over four licensed forms. (3) A coverage
quantity over the sites the roster never reached attaches to units with no rows, and its construction
transports a rate from the visited sites, which is `population_selection` needing the data to force the
selection, with the visited subset a filter and a divide. (4) A property of the design itself, which
contrasts the roster leaves unidentified or the date accumulating cross-cover makes a judgement possible,
is exact arithmetic on the shipped roster (rule application) or a running-sum crossing (the increment
trichotomy). (5) A rank or ordering object is dead across all four of its determinacy criteria, which are
exhaustive. **The structural reason is the mandated-indicator law reached from the design side:** a
quality system over human judgement exists in order to attribute variation to the people and units it
labels, so every quantity such an organisation keeps a record about is indexed by a labelled handler, and
the record that would be needed to identify an unlabelled quantity is the one it has no reason to keep.
Recorded, not drawn.

## Surface screen, answered

`guard.py surface task201` screens 246 builds and promotes five pairs for adjudication. Four are corpus
top-one-per-cent proximity on a single shared axis (task81 and task234 on the calibration form and the
artifact, task130 on the gap and the pattern together, task236 on the gap alone) and carry no finding: the
nearest driver to this build anywhere on file is 0.07 and none of those four appears in its driver
neighbourhood at all.

The fifth is the one worth answering. **task199 against task201, surface 0.100, two builds apart, sharing
the decisive pattern G12, the decision type and a published-series context artifact.** `guard.py check`
raises no ban on it, because the pattern ban reaches the last three live cards and task199 sits outside
them, but the screen is right that the draw should have seen it. The differentiation, also written onto the
card: task199's deciding quantity is an event count read against the observation effort that produced it,
so its correction is to the denominator of a rate and the records carrying it are a monitor's filing
volumes; this build's deciding quantity is a duration, and its correction is to when an interruption began,
recovered from the feeders whose line telemetry timestamps the device operation and conditioned on the
section class. One corrects for how much was watched, the other for when the clock started. Neither pack
can produce the other's correction, and the shared G12 label covers both because each turns on an absence
of record rather than on a record of absence.

**World-level repair pass, 2026-10-18. Raising the regulatory return's monthly figures: rejected, measured.**
The leak reader read the return's 3.93 and 4.35 as too small for monthly minutes per customer against a
171-minute annual SAIDI, and the obvious repair is to scale the workbook up. Measured on the pack's own
truth, the korekta sheet is not free: October SN 4.35 and nN 2.55 are exactly 0.63 and 0.37 of 6.898,
which is the window's unplanned customer-minutes over the 954,829 customers the register's trunk devices
carry, and that denominator is printed in the prior-year report. Scaling the workbook by the 2.5x the
reader's comparison implies would therefore plant a contradiction against the dispatch record that a
solver can compute, which is the defect class this pass exists to remove. The inconsistency was closed on
the side that ties to nothing instead: the filed 2024 and 2025 annual indices, which at 246 unplanned
minutes and 4.31 interruptions put the window's daily rate at only 1.31x and 1.05x the annual mean, when a
46-day storm-season window holding the year's windstorm should run two to three times it. Rebased to 124.2
minutes and 1.77 interruptions, both ratios land at 2.59x and 2.55x, asserted as a band in `checks.py`
(`doc.prior_year_saidi`, `doc.prior_year_saifi`). No graded figure moved.

**World-level repair pass, 2026-10-18. Stating the schedule's grain in the dictionary: rejected.**
The provenance count repair wanted a sentence saying one schedule row is one job covering several section
outages. That sentence adjudicates ask A1's own device, which is exactly the grafik-against-export grain
mismatch (`ceiling.py` A1), so the dictionary documents the `odcinkow` column factually and the provenance
states the job count alone, with the 440 section outages asserted in `checks.py` (`doc.planned_grain`)
rather than printed in a shipped document.


## Architecture 11, wave 8: the allocated pairing is undrawable, and the wave's premise is inverted

Stage 1 under `scratchpad/wave8/CONTRACT.md`. Allocation: domain `education-learning-sciences`, objective
`anomaly-detection`, strategy `causal_design` reserved. No card registered, nothing cut, no git write.
Harness in `scratchpad/w8_201/` (`map_ad.py`, `spend.py`), each run twice with byte-identical output.

**Death 1, structural, at the pairing.** `education-learning-sciences` has seven task types
(`student-growth-value-added-modeling` DD/EC, `randomized-quasi-experimental-program-evaluation` EC,
`item-response-theory-test-equating` ETL/DD, `learning-analytics-early-warning-models` F,
`multilevel-classroom-school-research` RC, `psychometrics` DD, `text-analysis` DD) and **none serves
anomaly detection**. `guard.py check` on the allocated card:

```
BLOCK three_rules.task_type    task type learning-analytics-early-warning-models serves forecasting,
                               not anomaly-detection: the domain would be a backdrop
        fix: draw a task type of education-learning-sciences that serves anomaly-detection
             (none in this domain), or another domain
```

The guard's own fix line enumerates the only two escapes and closes the first. The second, another domain,
is the orchestrator's axis, not this draw's. The single `## Three rules` line that fails is `Task type:`,
and it fails absolutely: no wording of it can name a task type that both belongs to this domain and serves
this objective. The other twelve lines were never reached, because a build whose domain is a backdrop by
construction fails rule 1 whatever they say.

**The route through the house domain is closed too.** `policy-education` is the only house domain touching
education, mapping to `political-science-public-policy` and `education-learning-sciences`. Its one
AD-serving task type is `political-science-public-policy/conflict-protest-event-data-analysis`, which is
protest event data and not education, so drawing it under an education wrapper is the rule 1 backdrop
failure in a second form; and `policy-education` x AD already carries two cards (4 architectures). Education
subject matter is reachable on this objective only as a *setting* under
`general-statistics-data-science`, where the taxonomy makes the setting another field's by design and the
deciding quantity must be the task type's own statistical object.

**The wave's premise is inverted, measured.** The contract reads the `.` cells of `coverage`'s domain x
objective grid as new ground. For this objective they are the opposite: a `.` in the ANOM column means the
domain has no AD-serving task type, so the cell is empty *because* it is undrawable.

- AD-serving ground, corpus-wide: **12 client domains, 14 task types**, against 45 for forecasting.
- Virgin AD task types: **0 of 14.** Every one is drawn (least spent one card, most spent four).
- Client domains with zero AD cards **and** an AD task type, that is, genuinely new AD ground: **0 of 21.**
- 34 AD cards hold **74 architectures** across 25 cells, so the mean cell has 3 dead or live architectures
  behind it.

Of the six wave-8 allocations, four name client domains with no AD task type and are undrawable as written:
task182 `urban-regional-science`, task194 `actuarial-science-insurance`, task201
`education-learning-sciences`, task202 `quantitative-finance`. The two that are legal, task190
`accounting-audit-forensic` and task198 `business-operations-analytics`, are legal only as *house* domains
inheriting AD task types from `banking-credit-financial-risk`, `general-statistics-data-science`,
`human-factors-ergonomics` and `healthcare-delivery-health-economics`, all of which already carry AD cards,
so neither is new ground either. `fingerprint` Part 4 names this failure and gives
`actuarial-science-insurance` as its worked example; the taxonomy line that settles it is the objective tags
beside each subdomain in `guide-to-prompt/references/domains/README.md`.

**What actually binds a redraw here, measured at the moment of the draw.** The three live cards in the ban
window are task475, task474 and task471, all `etl`. So **no AD subdomain sits inside the 3-build window at
all**: `ban.pairing` and `ban.subdomain` cannot fire for any AD cell right now, and the window strategies
are `composition_mix`, `decomposition_attribution` and `other`, leaving `causal_design` free of
`ban.strategy` and at 0 uses in the last 12 for `overuse.strategy`. Occupancy was never the constraint.
Wave 7 did not fail because its numbers sat on cells carrying AD cards; cells carrying AD cards are not
banned. It failed on **drivers**, which is the only thing that binds on this objective, and the remedy it
recommended, moving to virgin cells, was never available because there are none.

**The reserved strategy is in better shape than the contract states.** `causal_design` has 14 corpus uses
and 2 on this objective, task197 and task199, and **both are SHIPPED at stage 5**, neither failed; task197
is the shape `stumping` 1.6a names as the corpus's one positively-stated Gate-F-strong survivor. Neither
carries a portal result yet, so the honest claim is that `causal_design` is unconfirmed on AD, not that it
has never held. It is also already spent once on the allocated domain, at task450
(`education-learning-sciences/item-response-theory-test-equating`, objective `etl`).

**No candidate was screened.** Screens 1, 2, 3, 10, 11 and 12 take a candidate construction forced by a
named file, and with the pairing refused there is no legal task type to force a quantity for: screening a
construction whose domain cannot hold the objective would have measured nothing. The ground this slot
burned on its own earlier passes is wider than its card shows and is recorded above: architecture 10
candidates 1 and 1b spent GWAS ground (`biomedical-clinical-research/genomics-gwas-high-dimensional-association`,
one card) and candidate 15 spent the survey-office key-quality route, so the single-card appearance of those
two cells understates them for this number specifically.

- **Architecture 11, three candidates, all dead; the pass's own report was lost to a container restart and the
  harness is preserved.** Measurements read off `scratchpad/w11_201/run1.json`, byte-identical with `run2.json`
  (md5 08d4d741f149b9774befea96ce1ed8dd). The three candidates shared one fatal property: **the designed route
  itself recovers the truth only 3 of 20**, so there was nothing for a dial to protect.
  - `C16_between_only`, rho **1.7099** and no binding floor, margin **1.1085** (already under the 1.15 rung
    floor), designed truth **3 of 20**, and the mean-factor route reaching the designed designation **17 of
    20** at `corr` 0.9708.
  - `C17_coupled_no_eta`, rho **0.7255** against a floor of **0.6883**, so essentially on its own floor;
    designed truth 3 of 20, raw route already at `corr` 0.8571.
  - `C18_coupling_heterogeneous`, rho **1.2744**, designed truth 3 of 20, best cheap route `corr` 0.8231.
  - **The live lead this pass leaves, and it is the strongest separation on file in this lane.** Its parameter
    sweep found a cell at `sd_log_s` 1.3, `sd_log_A` 0.12, `sd_log_F` 0.05, `beta_sd` 0.6 and lift 3.5 where
    the **designed route recovers the truth 19 of 20 while the raw reflex takes 2 of 20**, at a margin of
    **1.7213** and rho **1.3031**, clearing the designed, margin, raw and rho conditions together. It fails on
    the group-by and power-route conditions (worst cases 3 and 7 of 20), and the pass's reading of why is lost
    with its report. That cell is where architecture 12 starts: re-run `recovery_screen.py` and `dense.py` at
    those parameters and establish whether the two failing conditions are a property of the cell or of the
    harness's route definitions.

