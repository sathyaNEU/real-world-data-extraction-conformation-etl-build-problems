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
