# task229 design note

Seed DQ02 (whether the release-health alert fires on this week's build, when the metric is the
average user's rate), objective Data Quality Monitoring & Alerting.

**Where the build stands (2026-10-11).** Architecture 1 (a smart-meter data provider's read-health
alert, decided by the unit a build mean's standard error is built over) is spent: it shipped, failed the
portal's determinism QC with both reviewers on the standard error's unforced construction, was called a
backdrop by the in-house Gate H pass (H1), and its estimand rework was cracked on the leak reader's first
pass. The author re-rooted the number as architecture 2 (the stock-control field's count-reset logic). It
was built at stage 3, passed the leak read and the clone pre-flight, and its round 1 solver landed the call
and cracked every ask (proxy 97.9) on the design's own rung 3, found from a visible symptom. Hardening loop
1, on paper, found no rung above that accrual model that completes with its checks passing and still lands
wrong within the loop's bounds (`## Hardening loop 1 (architecture 2, paper)`), so **architecture 2 is spent**
and the number re-roots to architecture 3, its last. Architecture 2's sections (`## Draw` to
`## Build record`) and its generator, pack, goldens and write-up stay in this folder as its record until the
re-root's draw replaces them. Architecture 1's generator, pack, goldens, write-up and reports are removed from this
folder (all in git history at f981255); its record is `## Architecture 1 record (spent 2026-10-11)`.

## Draw

**Status (2026-10-11).** Architecture 2, drawn and designed on paper by the designer against main at
3966e83 (PR #39, literal determinism; PR #43, the methodology-first stumping skill, `precut.py` and
`prompt.txt`); no data is cut. The card is checked (guard WARN, no BLOCK; heart WARN, nearest heart text
0.07) and **not registered**: task228 registers its next architecture first, and task228's branch still
carries its architecture 2 card, so the main session registers this card after task228's. The card is at
`/home/user/orch/buildwork-task229/rework/card/task229_arch2_count_reset.json`; until it is registered,
`cards/task229.json` is still architecture 1's, which is what `precut.py`'s "card registered" check
currently reads. The paper prototype that sized the ladder is `/home/user/orch/buildwork-task229/rework/proto2/`
(`sim2.py`, `tune4.py`). A fresh builder builds from the sections from here to `## Coordination and registration`.

**Kept from the author's decision.** The pairing (General Statistics & Data Science /
missing-data-censoring-measurement-error x Data Quality Monitoring & Alerting), the task number,
architecture 2, loops 0, and the world: Corderoy Logistics, a third-party logistics operator, runs eight
distribution centres for Thornacre, a grocer with about 320 stores across England, Scotland and Wales, and
the call is which centres' pick-face stock records Thornacre's automated replenishment may order off
unattended through the peak freeze. **Changed:** the decisive step (the paused draft's weighting of counted
locations by their chance of being counted is the generic reweighting, and is now rung 2).

| Field | Value |
|---|---|
| domain / subdomain | general-statistics-data-science / missing-data-censoring-measurement-error (client domain) |
| objective | data-quality-monitoring |
| shape / decision | 10, scorecard against thresholds, one file / designation_set, set_of_items |
| gap / pattern / generators | time, population / none / G13 (decisive), G16, G17 |
| gate_g / strategy / calibration | method_or_model_selection / population_selection / none |
| stump_class / layer 2 | analytical / field_method, `own:count-corrects-the-record-it-measures` |
| decisive_rule_filed / official_decoy / validated_decoy | true / false / false |
| context artifact / role / forum / event / org | operations_log / compliance_or_audit / line_manager_or_team / season_or_peak / logistics_or_3pl |
| spine | pick-face count history (one count task on one face), eight centres, 1 June 2026 to the stand-down, synthetic |
| world | United Kingdom (England, Scotland, Wales), GBP; Corderoy Logistics, Thornacre; personas Rhys Flynn, Stacey Sykes, Arthur Mason, Leonard Finch (pack documents only; the prompt names nobody), drawn with `guard.py names --geo "United Kingdom" --seed 229` and checked by hand against every card's people (Debra Khan dropped for task135, Martin Wood for task182's surname Martin) |
| deliverable / question form | `freeze_gate_2026.html` / whether |

**Driver.** The decisive quantity is the share of units in a correct state at one moment, seen only
through checks that record a unit's state just before setting it right; scheduled checks see each unit
at the end of its interval and symptom-led checks see units because they were wrong, so the checked-unit
rate, however reweighted to the population's cells, measures states that have since been reset, and the
share at the moment is built unit by unit from what each has accrued since its own last check of any
kind, with the accrual read from the scheduled checks alone.

**Guard.** `guard.py check` on main at 3966e83: WARN, no BLOCK. `driver.near` 0.12 against task107 v1
(the share of past failures a new check could have stopped, split by each source's delivery kind, a
conditioned yield): the overlap is vocabulary ("share", "check"); that build split check coverage by a
source property, this one estimates a population's state at a moment from checks that reset what they
observe. `repeat.gate_g` against task228 v2 (method_or_model_selection): task228 separates each station's
own error by collocating three error-carrying references; this build chooses the estimator of a record
population's state at one moment, with no reference instrument. `guard.py heart` (run on a local copy,
restored): WARN, nearest heart text 0.07 (task107 v1). The last three in draw order (task181, task182,
task228) forced two redraws from the paused draft (context artifact filed_standard to operations_log,
forum operations_desk to line_manager_or_team) and keep the decisive G-code off G12 and G16, which G13
honours honestly.

**Data-native sentence.** The count history is the only window on the records, and every row in it is a
record observed at the moment the programme chose to count it and then set right: routine counts fall due
at the end of a velocity-class cycle and exception counts fire because a symptom showed the record wrong,
so this dataset's own observation process, not a defect, separates the counted rate from the state of the
records at the stand-down.

**Sources read, one line each (what it teaches, how this build differs).**
- Exemplar index (49 accepted tasks): depth comes from a construction the layout does not show and asks
  that are the construction's outputs by segment; here no control set is recovered and no rule withheld,
  the estimand is filed and the construction is a state model.
- Replenishment Cover Standards (0.13): the unit and population a filed definition implies but no file
  stores (depot arrival, not order line); here the population is the record population at one moment, and
  the pitfall is the observation process, not a grain recovered from 24 published means.
- Outbound Warehouse Volume Planning (0.44): the committed number is not the central estimate a trailing
  average gives; here the moment is filed literally and the trap is reading a count rate as a standing
  state, with no archival record to back-test.
- Pipeline Custody Transfer Measurement (0.35): measurement corrections tied to recalibration dates, and a
  construction step the model never back-tests; here there is no decoy or decoding, and the measurement (a
  count) changes the thing it measures.
- Layer 2 library, missing-data-censoring-measurement-error (Rubin's rules, attenuation with validation
  data, delta-adjusting MNAR): the analysis targets the population estimand the design implies; here the
  missingness is made by an observation that resets the outcome, a pattern the library does not carry.
- Layer 2 library, census-register quality and nonresponse adjustment (dual-system estimates within
  post-strata, cell-level weighting): register quality from field checks inside the right cells; that cell
  adjustment is this build's rung 2, which completes and still lands wrong.
- `_measured.md`, traps 7 and 13 (uses the ready-made measure; validates on one population, applies to
  another): the habits this build leans on; no ready-made accuracy figure ships, the solver builds the
  count rate itself and carries it to a moment it does not describe.
- `proven-in-production.md` Parts 1 and 4: L7 and L8 (the count rate predicts every week's counts and every
  count ties), the dead "control used as a search bench" (so no full count, audit sample or census ships),
  the dead "reflex correction" (rung 2 is one, so it cannot be decisive) and task46's usage-exposure law
  (kept out of the decisive step by placing the estimand where per-day and per-handling accrual converge).

## Default path

The pipeline a competent analyst builds without thinking, from the prompt's words and the files' grain:

1. Read Thornacre's standard for the gate: in-scope pick faces, the correct-record test, the measurement
   time and the 97.0 per cent line.
2. Take each centre's in-scope faces from the location master and their count tasks from the pick-face
   count history, 1 June 2026 to the stand-down.
3. Count the tasks whose result matched the record and divide by all the centre's tasks: the centre's share
   of correct records.
4. Compare each centre's share with 97.0 per cent and list the centres at or above it.

Ends on: no centre qualifies, so all eight stay on supervised replenishment
Golden: Hinckley, Daventry, Bellshill, Warrington, Magor and Avonmouth qualify; Thurrock and Doncaster stay on supervised replenishment

## Stump sentence

A competent solver takes each centre's share of correct records from its count history as the share of
count tasks that matched the record and finds that no centre qualifies, all eight held on supervised
replenishment, and its textbook correction (exception counts set aside as symptom-led, the routine counts
weighted to the in-scope A, B and C mix) still passes only Magor and Hinckley; the step that lands it there
is reading a count's result as the record's standing state, when every count also posts the confirmed
quantity as the record, so routine counts see each record at the end of its cycle and exception counts see
records because they were wrong, while at 06:00 on 7 December each face is only part way through its cycle
since its last count of any kind, and built face by face from the accrual since that count, read off the
routine counts alone, Hinckley, Daventry, Bellshill, Warrington, Magor and Avonmouth clear 97.0 per cent.

## Three rules

- **Litmus:** no reported number or stakeholder conclusion is overturned. The pack reports no accuracy
  figure at all, every count row is a correct record of a real count, and what defeats the solver is the
  estimator it builds for itself.
- **Domain test:** the deciding quantity is the share of stock records that are right at one moment, which
  no count observes, and the inventory field's own count-programme logic decides it: a cycle or exception
  count both measures a record and sets it right, and a record goes wrong again only through the handling
  it takes before its next count, so the share at the stand-down is built face by face from each face's
  handling or days since its last count of any kind, with the accrual read off the routine counts alone;
  the generalist's correction (weight the counts to the population's class and flag cells) never reaches
  it, and with survey or clinic nouns in place nothing resets what it measures, so the task no longer reads
  the same.
- **Analyst test:** a strong analyst who cleans the count history and reads Thornacre's standard and
  Corderoy's programme correctly sets the exception counts aside, weights the routine counts to each
  centre's class mix and passes Magor and Hinckley only, holding back Daventry, Bellshill, Warrington and
  Avonmouth, which qualify; the easy route is the weighted count rate, wrong because it measures records as
  they fall due, not the records each centre carries into the freeze.
- **Layer 1:** Corderoy's WMS and Thornacre's merchandising and finance systems produce it: UTC stamps
  against UK trading days across the 25 October clock change, an effective-dated location master
  (re-slots, merges, holds, re-labelled reserve bins), a line master with effective-dated pack sizes and
  single-pick lines held in eaches, a period-10 cost change file over a base cost list, a stock-by-location
  export whose quantity is the face total repeated on every batch row, a replenishment forecast run that
  carries each store's depot as assigned before the peak re-zoning, and a store trading calendar updated
  after that run. The main path carries only texture asserted unable to move the call.
- **Layer 2:** the tempting shortcut is the count-based accuracy, weighted to the population's cells; an
  expert in stock control refuses it because a count resets the record it reads, so a count rate describes
  records at the moment they fell due, and the share at the stand-down has to be built from each face's
  accrual since its last count.
- **Rule 3 (the decisive step is analytical):** scope, the correct-record test, reason codes and the posting
  rule are filed and read the same by everyone; what separates the answers is the estimator.

## Deletion tests and Gate G

- **Gate G line:** mechanism `method_or_model_selection` (the estimator of the record population's state at
  the stand-down, chosen over count-based rates; the design forces it and Thornacre 4.5 states the
  standard's general requirement on any estimate, `determinism-check` §1 forms 1 and 2, with no filed back-test),
  `stumping_family: analytical_non_defect`, `surface_read_dependency: no` (no reported figure ships; the
  count rates are the solver's own constructions), `sole_data_defect: no`.
- **Delete every wrong number:** there is none to delete; the task stays exactly as hard.
- **Clean-data test:** no file is incomplete, stale, superseded, delta-shaped or filtered on the main path
  (the count history is the full log, one row per count task); repairing every ask-path device leaves the
  answer and the naive answer unchanged and different (asserted). The instrument argument: the pack's
  instrument is an operational correction programme whose every output is right, no reported figure is
  repaired, and the decision's quantity is the state of a population at a moment, which is the
  missing-data analysis the subdomain names; in the judge's own words the task stumps on perfectly clean
  data.
- **Lens swap:** the naive read and the answer are different moments (each count's own moment before its
  posting, against 06:00 on 7 December), and the answer is a construction, not a relabel.
- **Identity:** the share at the stand-down closes over each face's state at 06:00, which no file ships; it
  does not close over shipped quantities.
- **Corpus direction:** the pack ships no control total, published figure or closed corpus on the main
  path; every count reconciles under every estimator.
- **First moves:** the one-period group-by (match rate by centre) gives none; the decomposition by reason
  and class gives Magor, or Magor and Hinckley; the natural operationalisation of 4.3 (each face's latest
  count result) gives Magor; the hygiene battery is clean. None lands.

## The decisive step and the domain-coupling verdict

**The field's own method.** In a perpetual inventory a count is two things at once: it measures the record
and then posts the confirmed count as the record. A record then goes wrong again only through the handling
it takes (picks, let-downs, put-aways) before its next count. A count programme is designed on that logic
(count frequency set by class because errors come with handling), and it fixes what the gate's quantity
is: the share of in-scope faces whose record a full count at 06:00 on 7 December would find correct is the
share that has stayed right since each face's own last count. Routine counts see each record at the end of
its cycle and exception counts see records because they were wrong, and both then set them right, so every
count-based rate is the accuracy of records at the moment they fell due or failed.

**Domain-coupling verdict.** The draft's step is the generic reweighting and is demoted to rung 2. The
decisive step is the field's count-reset logic: the state at the stand-down built face by face from the
accrual since each face's last count of any kind, with the accrual read off the routine counts alone
(exception counts are symptom-led, so they are resets and never accrual observations).

**The textbook move, completed.** "The counts are not a random sample: exception counts fire on symptoms
and A faces are counted three times as often as C faces, so set the exception counts aside and weight the
routine match rates to each centre's in-scope A, B and C mix." A strong solver completes it exactly and it
reconciles everywhere. It lands wrong because it reweights observations of the wrong moment: the weights fix
the class mix and cannot fix the age, and on the freeze morning a face counted three nights ago carries
three nights of handling, not a full cycle's. Every rigorous variant (per handling pooled or by class, per day
by class, exponential or linear) gives the same six centres (`## Ladder`, the per-rung table). A per-day accrual
pooled over the three classes does not: it gives Magor and Hinckley, rung 2's set (Hinckley 97.20), and the
routine counts rule it out on their own structure, because an A face goes wrong 18 to 49 times as fast a day as a
C face at every centre with non-overlapping intervals, and the pooled day rate mis-predicts every class's own
routine match rate (SF13). Per handling, pooling is legitimate because the handling carries the class difference;
per day it is not.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex correction | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 0, the default path (all count tasks' match rate) | no | the count history's result column; this is the default itself | no | no | no | no | readable |
| Rung 1, exception counts set aside | no | the reason code makes it a row filter | fires: re-screen the residual, set the symptom-led rows aside | no | no | no | readable |
| Rung 2, routine counts weighted to the in-scope class mix | no | the class column on the location master | fires: reweight to the population's cells | no | no | no | readable |
| Rung 3 (decisive), each face's state at 06:00 from the accrual since its last count of any kind, read off the routine counts | no: Thornacre 4.3 and 4.5 name the estimand (what a full count at the measurement time would find) and its unbiasedness, and Corderoy's programme files when counts fall due and that a confirmed count is posted, as a real procedure must; no sentence names a face's time or handling since its last count, an age, a decay or a reset | no: no last-counted, age or days-since column ships; a face's last count is a group-by max, and the move is the accrual fit applied to every face, not a row predicate | no: not a reweight, stratification, shrinkage, analog, control or decomposition | no: no full count, audit sample, census, KPI or published accuracy ships, and nothing scores candidate estimators | no: counts tie, keys are unique per count task, every face joins, on the wrong path as on the right one | no: no reported figure exists to halve or subtract; the state is built face by face from a fitted accrual | silent |

## Semantic fork table

| Id | Term or convention in the main ask or the main computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "our eight distribution centres" | the eight Corderoy centres on the centre register holding Thornacre pick faces | any other set of sites (a reserve-only site, a closed one) | same call | the centre register lists eight Thornacre centres and no other site holds an in-scope face |
| SF2 | "meet Thornacre's peak stock-record standard" | record accuracy at the measurement time is 97.0 per cent or more (standard 5.1 with 4.3 and 4.4) | the share of the window's count tasks that matched is 97.0 per cent or more | no centre | standard 4.3: the number of in-scope locations whose record a full count at the measurement time would find correct, over the in-scope locations at that time, not a share of count tasks over a window |
| SF3 | "share of correct records" (correct) | system quantity equal to what a count under the 3PL's programme records, in the line's stock unit (4.2) | a record within a case either way counts as correct | more centres pass | standard 4.2 ("equals"; the scale tolerance applies to weighed lines only) |
| SF4 | "as the standard measures it" (the moment) | 06:00 on 7 December 2026 (4.4) | the end of the freeze, or an average over it | another estimand | standard 4.4 names the stand-down as the measurement time for the peak gate |
| SF5 | "as the standard measures it" (an estimate) | an estimate a full count at 06:00 on 7 December would be expected to bear out (4.5) | any estimate built from the count records | Magor and Hinckley (rung 2) | standard 4.5: the estimate is the one a full count at the measurement time would be expected to bear out, which the count records in the window are not (they are counts at other times) |
| SF6 | "the faces the gate covers" (in scope) | pick faces slotted to a Thornacre line at 06:00 on 7 December, not on hold or recall (4.1) | every pick face, held ones included | same call | standard 4.1, and asserted: counting the held faces in moves no verdict and no whole per cent |
| SF7 | "qualifies" | 97.0 per cent or more (5.1) | strictly above 97.0 | same call | no centre within 0.6 of the line under any estimator (asserted) |
| SF8 | the rounding path | the gate on the unrounded share; the page in whole per cents | the gate on the whole-per-cent share | same call | margins asserted: no centre's share rounds across 97 |
| SF9 | which counts are exception counts | the reason codes the programme's code table marks as raised by a symptom | the overflowed-replenishment code read as routine | same call | the programme's reason-code table, and asserted |
| SF10 | the count history's close | every count up to the last count window before 06:00 on 7 December | the last night's counts left out | same call | the extract notes (the export closes at the stand-down), and asserted |
| SF11 | a face's centre and class | the centre and slotting class on the location master, unchanged through the window | the site field on the count task, the class at each count | same call | the two agree on every in-scope face (asserted); the location master carries one class per in-scope face through the window |
| SF12 | "through the freeze" | 06:00 on 7 December 2026 to 06:00 on 4 January 2027 (5.1) | the calendar days 7 December to 3 January | same call | standard 5.1; the forecast's trading days are the same days |
| SF13 | "as the standard measures it" (the accrual's form) | each face's per-day accrual taken by its slotting class (or per handling, pooled or by class) | one per-day accrual pooled over the A, B and C faces | Magor and Hinckley (Hinckley 97.20) | the data's own structure, not a sentence (form 1): fitted on each centre's routine counts the per-day hazards are A 0.0022 to 0.0092, B 0.0004 to 0.0018, C 0.0001 to 0.0004, an A face going wrong 18 to 49 times as fast a day as a C face, with 95 per cent intervals that do not overlap at any centre; the pooled day rate over-predicts the A faces' routine match rate by 3.7 to 14.5 points and under-predicts the B faces' by 0.7 to 4.2 and the C faces' by 3.2 to 17.3 at every centre, while each class's own rate reproduces its match rate within 0.1; CP-THN-04's cycle table files the classes the programme counts by (asserted) |
| SF14 | "share of correct records" (which count is the count) | the confirmed count (the recount where there is one, otherwise the first count), the WMS `result` | the blind first count against the system quantity | Bellshill, Daventry, Hinckley and Magor (Avonmouth 96.84 and Warrington 96.82 fall below the line) | CP-THN-04 s.5: "The confirmed count (the recount where there is one, otherwise the first count) is posted as the location's record", read with SCS-07 4.2 (correct when the system quantity equals what a count under the 3PL's programme would record); the sentence asserted present in the shipped docx |

**The stump is none of these readings.** SF2 and SF5 close the two readings that would reach the textbook
answers by misreading; the rung-2 solver reads 4.3 to 4.5 correctly and believes its weighted count rate is
the estimate a full count would bear out, because it takes record accuracy as a stable property of a centre.
That belief is the method error, and the data, not the text, refutes it.

## Ladder

Four rungs, each a complete pipeline a competent analyst files, each naming a different set, each killed
by one shipped fact or one construction.

| Rung | The analysis filed | Gap, code | Centres that qualify | Killed by |
|---|---|---|---|---|
| 0, the default path | each centre's match rate over every count task in the window | population, G13 | none | the programme's trigger list: exception counts are raised by a symptom |
| 1, the obvious correction | exception counts set aside; the routine match rate | population | Magor | the cycle table with the class shares: A faces are counted three times as often as C faces |
| 2, the sophisticated correction | routine counts weighted to the in-scope A, B and C mix (the textbook reweighting) | population | Magor, Hinckley | the posting clause with the due-date clause: each routine count sees a record at the end of its cycle and then sets it right, so the share at 06:00 is the accrual since each face's last count |
| 3, decisive | resets at every count; accrual from the routine counts only, each routine count's exposure measured from the face's last count of any kind; each in-scope face's state at 06:00 built from its days or handling since its last count | time, G13 and G16 | Hinckley, Daventry, Bellshill, Warrington, Magor, Avonmouth | the answer |

**The satisfying sentence at each stop.** Rung 0: "None of the eight clears 97 on its own counts; the
standard is out of reach this peak." Rung 1: "The exception counts are there because something went wrong;
on the routine counts only Magor clears the line." Rung 2: "Weighted to each centre's mix of fast and slow
faces, as the standard counts every face once, Magor and Hinckley clear it."

**Grid and partial cells** (each asserted by name): every count weighted by its flag-and-class cell gives
Magor; each face's latest count result taken as its state gives Magor; the reset seen with the accrual
estimated from every count, exception counts included, gives Magor; resets at routine counts only (exception
counts ignored altogether) converges on the answer within 0.2 points, because it carries the decisive move;
a face counted in the window taken as correct with no accrual gives all eight (the over-correction stop).
Sign discipline: every count-based cell sits below the answer on every centre and the over-correction above
it, so the answer is bracketed and no single half-step reaches it by cancellation.

**Per-rung worth on the graded quantity** (prototype `tune4.py`, one seed; percentages of in-scope faces;
the builder re-tunes on the real generator):

| Centre | truth (private) | rung 3, per handling | rung 3, per day by class | rung 3, linear | rung 2 (whole export, 27 weeks) | rung 2 (4 weeks) | rung 2 (8 weeks) | rung 1 | rung 0 |
|---|---|---|---|---|---|---|---|---|---|
| Hinckley | 99.09 | 98.93 | 98.88 | 98.89 | 97.84 | 97.92 | 97.71 | 97.03 (target 96.5 or under) | 91.46 |
| Daventry | 98.08 | 98.09 | 98.04 | 98.06 | 96.00 | 96.14 | 96.04 | 94.94 | 83.32 |
| Bellshill | 98.08 | 97.94 | 97.91 | 97.93 | 95.85 | 95.86 | 95.75 | 94.43 | 88.18 |
| Thurrock | 95.73 | 96.25 | 96.12 | 96.21 | 92.19 | 92.92 | 92.18 | 89.49 | 84.44 |
| Magor | 99.29 | 99.26 | 99.39 | 99.40 | 98.68 | 98.59 | 98.78 | 98.00 | 95.23 |
| Warrington | 98.18 | 98.02 | 97.95 | 97.97 | 95.96 | 95.53 | 96.04 | 94.88 | 84.72 |
| Avonmouth | 98.21 | 97.97 | 98.04 | 98.06 | 96.16 | 95.76 | 95.86 | 94.75 | 81.62 |
| Doncaster | 95.63 | 95.69 | 95.74 | 95.85 | 91.94 | 92.02 | 92.33 | 88.86 | 83.17 |

**Margins and position (asserted).** Every rung-3 estimator at least 0.6 points from 97.0 on every centre,
and the private truth on the golden's side; every rung-3 estimate at least 0.2 from an x.5 edge (whole per
cents); rung 2's set differs from the answer in at least four verdicts under every window from 4 to 26
weeks, and is Magor and Hinckley on the 8 to 26 week windows; rung 1 at least 0.5 from the line on every
centre (Hinckley's 97.03 in the prototype is the first tuning item: the builder gives Hinckley's fast faces a
larger share of its routine counts until rung 1 is at 96.5 or under while rung 2 stays at 97.5 or over); rung
0 at least 1.0 under the line everywhere. The answer's distinctive centres (Daventry, Bellshill, Warrington,
Avonmouth) qualify on no intermediate rung. The rung-collision guard recomputes every rung's set by name
after each parameter change.

## Closure table

| # | Axis | Reading and closing move |
|---|---|---|
| 1 | Population | in-scope = pick faces slotted to a Thornacre line on the location master at 06:00 on 7 December, not on hold or recall (standard 4.1); the main population carries no effective-dated churn (re-slots, merges and re-labels sit on out-of-scope and reserve rows, and a hold shows as the face's status at the moment); C1, asserted: counting the held faces in moves no verdict and no whole per cent |
| 2 | Unit of account | the pick face, one line per face (asserted) |
| 3 | Attribution window | which counts are routine and which exception: the programme's reason-code table, one meaning per code; accrual observations are routine counts with a known previous count of any kind |
| 4 | As-of dating | the measurement time is 06:00 on 7 December (4.4); the export closes then; counts sit in the 02:00 to 05:30 window at the end of a trading day, so a face counted on the last night has no handling after it |
| 5 | Version basis | in-scope faces keep one class and one line through the export window (re-classing ran before 1 June); asserted |
| 6 | Divisor | in-scope faces at the measurement time (4.3) |
| 7 | Weighting | each face counts once (4.3) |
| 8 | Measurement window | the accrual read from routine counts over any window from 8 to 26 weeks gives the same set and whole per cents (C3, asserted) |
| 9 | Boundary | 97.0 per cent or more (5.1); every centre at least 0.6 from it |
| 10 | Rounding path | the gate on the unrounded share; whole per cents on the page; every estimator at least 0.2 from an x.5 edge (asserted) |
| 11 | Tie-break | none, a set call |
| 12 | Maturity and censoring | every in-scope face has a count in the 189-day export (the longest cycle is 91 days, asserted); no face is opened in the window |
| 13 | Order of operations | the accrual applied face by face or by class converges (asserted) |
| 14 | Row order | none |
| 15 | Duplicate resolution | the count history is one row per count task, the supervisor recount carried as a column; no re-delivered rows on the main path |
| 16 | Identity normalisation | location codes stable on in-scope faces; re-labels only on reserve rows (ask paths) |
| 17 | Netting against gross | a record is right or wrong (4.2); netting arises only on the ask paths |
| 18 | Dimensional units | the count history's result column is the WMS's own test in the line's stock unit; main-path quantities consistent; the units hazard sits on the snapshot and the forecast |
| 19 | Code and status semantics | reason codes and location statuses filed once, in the programme and the extract notes |
| 20 | Integerisation | none on the main call; the asks round once, after the per-centre sum |
| 21 | Scope of a stated clause | the measurement time governs the peak gate only (4.4); 4.5 governs any estimate of 4.3 |
| 22 | Forward window contents | the freeze bounds the forecast ask only; the call governs the freeze, which has not run |
| + | The estimator (HOW, forced by the design, form 1, and by the standard's general requirement 4.5, form 2; no filed back-test) | per handling pooled or by class, per day by class, exponential or linear: same set and whole per cents (C1, asserted); per day pooled over the classes gives Magor and Hinckley and is ruled out by the routine counts' own structure, the class day hazards separated at every centre and the pooled day rate mis-predicting each class's routine match rate (C4 against the data, SF13, asserted); every count-based rate falls short of the full-count share by 1.0 to 3.6 points at every centre on the data's own accrual (C4, each cell mapped to 4.5); the UTC against local-day attribution of counts moves no main figure (C1, asserted) |

## Literal reader

Executed word for word, Thornacre's standard asks for the number of in-scope faces whose record a full
count at 06:00 on 7 December would find correct, over the in-scope faces at that time (4.1 to 4.4), and it
lets the 3PL estimate that share from its count records only with an estimate such a full count would be
expected to bear out (4.5). Corderoy's programme files that a routine count is generated on the night a face
falls due under its class's cycle and that every confirmed count is posted as the location's record. Read
literally, a face counted in the last window is correct at 06:00 by the text, and every other face's state
depends on what has happened since its last count. Where the text is silent (the estimator), the options
are the count-based rates (all counts, routine, class-weighted, cell-weighted, latest result per face) and
the state estimates. Every count-based rate is the share correct at each count before its posting, a
different moment; on the data's own accrual (match rates rise as the interval since a face's previous count
shortens) each is expected to fall short of a full count at 06:00 by 1.0 to 3.6 points at every centre, so
each violates 4.5, a sentence one can quote, and is an easy method on the same literal estimand, never
another reading of it. Every state estimate converges on the same six centres and the same whole per cents
(asserted), except a per-day accrual pooled over the classes, which the routine counts' own class separation
rules out (SF13); reading "correct" on the blind first count instead of the confirmed count gives four centres and
violates CP-THN-04 s.5 with 4.2 (SF14). No filed sentence defines or reports a count-based accuracy, and no filed rule read literally
gives another answer.

**What forces HOW** (`determinism-check` §1). Form 1, the design: the estimand at 06:00 through a full count,
the filed posting and due-date facts and the data's own age-dependent match rates rule out every count-based
rate, and no sentence names the step. Form 2, the standard's general method: 4.5 states, as an assurance
standard would, that any estimate is the one a full count at the measurement time would be expected to bear
out, which names no method. Form 3 (a filed back-test against a closed full count) is not used, so the pack
ships no recognisable back-test organ and no full count that a solver could score estimators against.

## Oracles

- None on the main path. No full count, audit sample, census, accuracy KPI, count summary or published
  accuracy ships, so nothing scores the candidate estimators and nothing confirms the answer.
- The location master's in-scope face count per centre ties to the centre register under every estimator
  (one population); it confirms the population, never a share.
- The count history's system, counted and posted quantities tie to the adjustment arithmetic under every
  basis.
- Ask A: the batch register is the pack's one referee; it arbitrates the repeated face quantity on batch rows
  and carries no value and no centre total. No stock valuation total ships.
- Ask B: the forecast's network daily totals are the same under every servicing assignment, so they tie on
  every path; no centre-level forecast summary ships.

## Ask sheet

Both asks are per centre, decoupled from the main computation (no count-history column, no accrual), and
each is a component of each centre's case under H18: what the verdict puts at stake. The chart is built on
ask B's own quantity, never on the decision quantity.

| Ask | Figure, unit, rounding | H18 home and use | Primary device (silent) | Hazards | Path |
|---|---|---|---|---|---|
| A, the stock on the gate's faces | Thornacre stock value on each centre's in-scope faces at the stand-down, nearest £1,000 | component (the exposure beside each verdict); the account director states it in the peak declaration | D6: the WMS stock-by-location export repeats the face's total quantity on every batch row of a date-coded face, with the export's grain stated as "one row per stock record"; batch quantities live in the batch register | H1 (D2): the period-10 cost changes, effective 6 December, arrive as a change file over a base cost list extracted on 28 November; H2 (D3, shared): single-pick lines held in eaches against a per-case cost, with case sizes changed on effective dates in the line master | snapshot, batch register, location master, line master, base cost list, period-10 change file, standard (4.1), centre register, extract notes: 9 files, about 14 columns |
| B, the replenishment the verdict governs | cases Thornacre's stores are forecast to draw from each centre over the freeze, nearest hundred; and one bar per centre of them, largest first, each labelled, under a title naming the centre with the most | component (the volume each verdict sets running unattended); Corderoy's peak planners and the account director size the freeze by it | D2 stored label before a silent switch: Thornacre's replenishment forecast run of 23 November carries each store's serving depot as assigned when the run was made; the peak re-zoning agreed on 1 December moves about forty-five stores between centres in every regime from 7 December, and part of it ends on 27 December (the far edge), recorded only on the effective-dated store servicing map | H2 (D3, shared): single-pick categories forecast in units, converted by the category table's units per case; H3 (D4): Boxing Day trading decided on 1 December closes about forty stores on 26 December on the store trading calendar, while the forecast run still loads their demand | daily forecast, store servicing map, store trading calendar, store list, category table, centre register (Thornacre depot codes to Corderoy centres), standard (5.1 freeze dates), extract notes: 8 files, about 13 columns |

**Stops** (each asserted, distinct, outside the bin). A: (1) the lazy read, the snapshot's quantity summed
over its rows at the base cost with eaches read as cases, far high; (2) the fan-out handled, base cost,
eaches as cases, high; (3) the fan-out and units handled, period-10 changes missed, off on every centre; (4)
over-cleaned, one row kept per line per centre, which drops the genuine second faces of fast lines, low; (5)
the golden. B: (1) the lazy read, the forecast grouped by its own depot column with units read as cases;
(2) the servicing map at the freeze's start applied to the whole freeze (the 27 December return missed);
(3) the map applied day by day and units converted, Boxing Day closures missed; (4) over-cleaned, every
re-zoned store dropped as "in transition", low; (5) the golden. The lazy delta on every figure is outside
the bin by at least two bins.

**Hazard table.** H1 moves ask A on every centre (period-10 lines are stocked everywhere). H2 moves ask A and
ask B on every centre (single-pick lines and categories everywhere). H3 moves ask B on every centre that
serves a Boxing Day closure (all eight). Composed deltas for every subset of mishandlings land outside the
bins (asserted).

**Separation.** The main call's declared row population is the in-scope faces' rows on the location master
and their rows in the count history. Every device and hazard sits on the snapshot, the batch register, the
cost files, the line master, the forecast, the servicing map and the trading calendar: zero device rows and
zero hazard rows inside the main population (counts asserted and written here by the builder).

**Referee.** The batch register (ask A), byte-clean, never trapped, carrying no value and no centre total.

| Ask item | The cracker's path (call landed, hygiene battery run, every filed rule executed) | Why it lands outside the bin | Verdict |
|---|---|---|---|
| A, the eight centres' stock values | the key check flags several rows per face and line, the rows differ by batch, so it sums the quantity over the batch rows and values it at the cost list it finds | the quantity on a multi-batch face is the face total repeated on each batch row, so every centre with date-coded lines is overstated, and no filed rule adjudicates the export's grain; the period-10 change file is on no path a filed rule points at | miss |
| B, the eight centres' forecast cases | groups the forecast by the depot the run carries, which every store has, so nothing is unmatched | the depot on the run is the pre-re-zoning assignment; the effective-dated servicing map is joined by no key the battery tests, and the 27 December return and the Boxing Day closures move every centre | miss |
| B, the chart's order | orders the bars on its own centre totals | the re-zoning changes the order of the ambient centres | miss |
| B, the chart's labels | labels each bar with its own total | every total is off by the devices above | miss |
| B, the chart's title | names the centre with the largest total on its path | on the run's depots the largest centre is Thurrock; on the servicing map it is Hinckley | miss |

**Mirror sheet.** The best response that misses the call runs the same ask path, because no ask needs the
call or its construction; the two sheets differ only in the recommendation criteria.

**Pair arithmetic.** Planning weights 38 / 7 / 55, r about 5. With the cracker missing every ask row, each
top response keeps only the chart's structural criterion (one bar per centre, about 0.05 of the ask weight):
C = 38 + 7 + 2.75 = 47.75, S = 5 + 7 + 2.75 = 14.75.

Pair ceiling: 32 (average of 47.75 and 14.75, rounded up; recomputed from the real rubric when it generates)

**Reuse.** D6 reuses task20's repeated event quantity and D2's stored label reuses task98 v4's, both
re-skinned; neither repeats this author's last builds.

## Shape and criteria

Shape 10, one file: each centre's gate check (share against the line, one criterion per cell), two further
measures per centre and the chart's parts. The call (1), each centre's share and verdict (8), stock value per
centre (8), forecast cases per centre (8), the chart's bars, order, labels and title (4), the file (1): about
30 criteria. The decisive checks are the four rung-2 flips (Daventry, Bellshill, Warrington, Avonmouth);
Magor, Hinckley, Thurrock and Doncaster read the same on rung 2 and the answer, which is why the asks carry
the weight.

## Prompt

`task229/prompt.txt`, one paragraph, 733 characters, question first ("whether" form), one file, rounding at
the close; `voice-check.py task229` passes every rule:

> Do our eight distribution centres each meet Thornacre's peak stock-record standard, so that its
> replenishment can order off our pick-face records unattended through the freeze? Put the answer in
> freeze_gate_2026.html: each centre's share of correct records as the standard measures it, beside the
> standard's line and marked qualifies or not; for each centre, the Thornacre stock value on the faces the
> gate covers and the cases its stores are forecast to draw over the freeze; and one bar per centre of those
> forecast cases, largest first, each bar labelled with its value, under a title naming the centre with the
> most. Give the shares in whole per cents, the stock values to the nearest £1,000 and the cases to the
> nearest hundred.

It names no person, file, standard acronym, method, moment or trap word; the moment, the scope, the line and
the estimate criterion live in Thornacre's standard. The 10/10 check: the answer turns on the estimator, not
on a procedure or a field.

## Stopping rule

Filed at ceiling, and re-rooted rather than repaired, if two consecutive in-house rounds land the call by
the count-reset construction, or the portal lands it twice. One more repair is licensed when a round misses
the call but keeps 35 per cent or more of the ask weight (the ask layer only), or when the judge finds a fork
on the estimator that a pin naming an observable (never the move) closes. Three hardening loops, then
re-root; this is the number's second architecture of three.

## Builder's work order

Read this note from `## Draw` to here, `## Tried and rejected` first, and `pipeline.json`; invoke
`dataset-generation`, `determinism-check`, `supplemental-stumping` (Parts 2 to 5), `submission-writeup`
(blocks from `figures.json`, `figures_check.py`), `golden-realism` and `reduce-house-fixes` as the pipeline
orders them. Never ship the private truth, the prototype, a full count or any count-based accuracy figure.

**The world, fixed here.** Ambient: Hinckley (England), Bellshill (Scotland), Thurrock (England), Avonmouth
(England). Chilled: Daventry, Warrington (England). Frozen: Magor (Wales), Doncaster (England). About 24,000
in-scope pick faces (2,400 to 3,600 a centre); Thornacre about 320 stores. Trading day 06:00 to 06:00 UK
local; counts in the 02:00 to 05:30 window; exports in UTC. Freeze 06:00 Monday 7 December 2026 to 06:00
Monday 4 January 2027; Corderoy's counting (routine and exception) stands down at 06:00 on 7 December. The
prompt's moment is the morning of 7 December. Personas, in documents only: Stacey Sykes (Thornacre head of
replenishment, owner of the standard), Arthur Mason (Corderoy inventory control manager, owner of the
programme), Leonard Finch (Corderoy BI analyst, the extract notes), Rhys Flynn (Corderoy account director,
the declaration's signatory, named only where a real document would carry him).

**The filed wording that carries determinism** (Thornacre's standard, PDF): 4.1 a location is in scope at a
time when it is a pick face holding a slot for a Thornacre line on the 3PL's location master and is not on
quality hold or recall; 4.2 a location's record is correct when its system quantity equals the quantity a
count under the 3PL's count programme would record, in the line's stock unit (kilograms within the scale
tolerance for weighed lines); 4.3 record accuracy at a time is the number of in-scope locations whose record
a full count at that time would find correct, divided by the number of in-scope locations at that time, as
a percentage; 4.4 for the peak gate the measurement time is the moment the 3PL stands its counting down for
the freeze, 06:00 on 7 December 2026; 4.5 where the 3PL does not count every in-scope location at the
measurement time it estimates record accuracy from its count records, and the estimate is the one a full
count at the measurement time would be expected to bear out; 5.1 a centre's replenishment runs unattended
through the freeze (06:00 on 7 December 2026 to 06:00 on 4 January 2027) when its record accuracy at the
measurement time is 97.0 per cent or more, and is supervised otherwise. Corderoy's programme (DOCX): classes
from the slotting class; a routine count generated on the night a face falls due under its class's cycle (A
28, B 56, C 91 days), rolling to the next night when not done; exception counts the same night on a short
pick, a negative balance, an empty-face report or an overflowed replenishment; blind first counts, a
supervisor recount on any difference, the confirmed count posted as the location's record; the count window;
the reason-code table; the peak stand-down. No document defines or reports a count-based accuracy, and none
speaks of a record's age, decay, accrual or reset.

**Generator, file by file (`task229/generator/`).**
1. `world.py`: centres, classes, cycles, class mixes, velocity scales, error rates per handling (silent and
   loud), false triggers, slip rate, dates, personas, seeds; start from `tune4.py`.
2. `simulate.py`: per face, from a burn-in of at least 240 days to 06:00 on 7 December: daily handling,
   silent errors that persist to a count, loud errors that surface the same trading day and draw an
   exception count that night, false triggers, the routine cycle with roll-over slips, a blind count, a
   supervisor recount on a difference, the confirmed count posted. Keeps the private truth.
3. `estimate.py`: every rung, every grid cell and every rung-3 estimator, reading only what ships; the golden
   is the per-face accrual by class in days (the write-up states it), the others asserted to agree.
4. `asks.py`: the snapshot and batch register, line master, cost list and period-10 change file, daily
   forecast, servicing map, trading calendar, store list, category table; every device with its
   over-cleaning half; every ask stop; the chart's order and title under every stop.
5. `docs.py`: the standard (PDF), the programme (DOCX), the extract notes (TXT), `metadata.json` (synthetic,
   CC0, sources and dates, the two distractors named).
6. `golden.py`: `freeze_gate_2026.html`, a table of the eight centres (share in whole per cents, qualifies or
   not, stock value nearest £1,000, forecast cases nearest hundred) and an inline SVG bar chart of the
   forecast cases, largest first, each bar labelled, titled with the centre with the most; then
   `golden-realism`. `figures.json` carries every owed figure.
7. `checks.py`: every SF id (SF1 to SF12) asserted by name; the ladder sets and margins; rung-3 convergence;
   the private truth on the golden's side; the C4 shortfall of every count-based rate under 4.5; rung 2 under
   every window from 4 to 26 weeks; UTC against local-day invariance; zero device and hazard rows inside the
   main population; each device's per-figure delta outside its bin, every subset composed; the cracker and
   mirror sheets; the input gates; two builds byte-identical.
8. `verify.py`: recomputes every graded figure, rung and stop from `target/` alone.
9. `make.py`: writes `target/` and `target.zip`; then `precut.py task229` (its SF check passes once
   `checks.py` exists), `figures_check.py`, `leak.py`, `guard.py surface`.

**The pack (`target/`, names in the organisations' own idiom).**

| File | Format | Role | Path |
|---|---|---|---|
| Thornacre peak stock-record standard | PDF | filed standard | main (4.1 to 5.1) and ask A (scope) |
| Corderoy perpetual count programme | DOCX | procedure | main |
| pick-face count history, Thornacre, 1 June 2026 to the stand-down | CSV, about 110,000 rows | spine | main |
| location master, effective-dated, pick faces and reserve | CSV | register | main (in-scope faces, class, velocity) and ask A |
| stock by location at 06:00 on 7 December, and the batch register | CSV, CSV | snapshot, referee | ask A |
| Thornacre line master | XLSX | reference | asks A and B |
| base cost list and the period-10 change file | CSV, CSV | reference | ask A |
| daily store forecast over the freeze (run of 23 November) | CSV, about 30,000 rows or more | reference | ask B |
| store servicing map, effective-dated; store trading calendar; store list; category table | CSV | registers | ask B |
| centre register | CSV | reference | main and asks |
| peak labour plan (agency hours by centre and week) | XLSX | distractor | none |
| goods-in booking summary over the freeze | CSV | distractor | none |
| extract notes | TXT | provenance | all |
| `metadata.json` | JSON | provenance, distractors named | all |

**Input gates.** 19 files; PDF, DOCX, CSV, XLSX, TXT, JSON; the count history at about 110,000 rows; two
distractors that bear on the freeze but not on the gate, named in `metadata.json` and never in a file name;
one deliverable; unit and rounding in every ask; everything synthetic with source, date and licence
recorded; nothing that ranks the centres on record accuracy.

**First tuning items.** Hinckley's rung 1 to 96.5 or under with rung 2 at 97.5 or over; every rung-3
estimate at least 0.2 from an x.5 edge; the private truth at least 0.6 from 97.0; every grid cell's set named;
the chart's title flipping under ask B's primary device. If a margin cannot be met without changing a rung,
commit and hand back to a designer.

## Coordination and registration

This card registers after task228's next architecture (the coordination of 2026-10-11: cards dated today
sort task228, task229, task230). At registration the main session copies the scratch card into
`.claude/skills/fingerprint/cards/task229.json` with `guard.py register`, re-runs the check against task228's
new card, and answers any new WARN here; a BLOCK goes back to the author. The builder does not start before
the card is registered.

## Build record (architecture 2, stage 3)

**Built 2026-10-11 by the builder from the work order; no rung, pin or decisive step changed.** Generator
`task229/generator/` (`world`, `simulate`, `estimate`, `asks`, `docs`, `golden`, `checks`, `verify`, `make`, plus
`build` (the pack writer with the bin anchors) and `postprocess` (container normaliser)). `make.py`: `checks.py`
791 assertions green, `verify.py` 65 checks green (csv module and its own likelihood search, no pandas, no
generator state), two builds byte-identical, house fixes H7, H8, H9 and H11 asserted on the cut, `figures_check.py`
exit 0 (52 figures), `precut.py` exit 0, `voice-check.py` pass, `guard.py surface` 0 promoted pairs (nearest
task127 0.10), `guard.py heart` WARN (task107 v1 0.12, task228 v2 gate_g, both answered at the draw), no BLOCK.

**As built** (percentages of in-scope faces; truth private, never shipped):

| Centre | truth | per day by class (golden) | per handling pooled | per handling by class | linear | rung 2 | rung 2, 4 wk | rung 2, 8 wk | rung 1 | rung 0 | cell-weighted | latest result | accrual from every count | resets at routine only | per day pooled over classes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Hinckley | 98.77 | 98.82 | 98.79 | 98.81 | 98.83 | 97.69 | 97.46 | 97.79 | 96.36 | 86.99 | 92.82 | 94.28 | 95.37 | 98.85 | 97.20 |
| Daventry | 98.25 | 98.16 | 98.18 | 98.15 | 98.18 | 96.30 | 96.05 | 95.86 | 95.27 | 84.00 | 88.80 | 91.69 | 93.14 | 98.25 | 96.65 |
| Bellshill | 98.20 | 98.06 | 98.10 | 98.07 | 98.08 | 95.98 | 96.19 | 96.39 | 94.74 | 88.25 | 92.06 | 93.26 | 95.35 | 98.12 | 96.30 |
| Thurrock | 95.84 | 95.91 | 95.95 | 95.90 | 96.01 | 92.21 | 91.74 | 91.90 | 89.19 | 83.70 | 89.25 | 89.93 | 93.63 | 96.09 | 91.78 |
| Magor | 99.08 | 99.11 | 99.16 | 99.11 | 99.11 | 98.33 | 98.37 | 98.39 | 97.65 | 95.79 | 97.30 | 97.58 | 98.38 | 99.16 | 98.23 |
| Warrington | 97.84 | 97.90 | 97.91 | 97.89 | 97.92 | 95.99 | 95.29 | 95.87 | 94.83 | 84.98 | 89.54 | 91.40 | 93.39 | 97.95 | 96.23 |
| Avonmouth | 97.94 | 97.96 | 97.96 | 97.94 | 97.98 | 96.01 | 95.92 | 96.07 | 94.70 | 81.21 | 87.87 | 90.34 | 91.96 | 98.01 | 95.97 |
| Doncaster | 96.07 | 96.02 | 95.93 | 96.00 | 96.11 | 92.18 | 92.02 | 92.22 | 89.05 | 83.01 | 88.94 | 89.93 | 93.34 | 96.01 | 91.93 |

Sets: rung 0 none; rung 1 Magor; rung 2 Magor and Hinckley (every window from 8 to 26 weeks; from 4 weeks the
four distinctive centres never qualify); rung 3, all four estimators, the six; golden set the six. First tuning
item met: Hinckley rung 1 96.36, rung 2 97.69 (its A faces run at 1.7 times the class's picks a day). Every rung-3
estimate at least 0.71 from 97.0 and 0.21 from an x.5 edge, one whole per cent per centre; truth at least 0.84
from the line on the golden's side.

**Departures from the work order, none touching a rung.** (1) In-scope faces 26,188 (2,605 to 3,935 a centre),
not about 24,000: the count history needed them to reach 107,072 rows. (2) `target/` holds 18 files;
`metadata.json` sits in the task folder (dataset-generation 8.3: distractors are never named under `target/`), so
19 with it; the store list is the JSON file. (3) C4 as built: every count-based rate (rungs 0 to 2, every rung-2
window, cell-weighted, latest result) falls short of the estimate by 0.68 (Magor, a rung-2 window) to 16.75 (Avonmouth,
rung 0) points; on the six centres other than Magor and Hinckley at least 1.6; asserted at 0.5 or more everywhere.
(4) One extra grid cell, asserted by name: a per-day accrual pooled over the three classes (ignoring that an A face
goes wrong about twenty times as fast a day as a C face) gives Magor and Hinckley, rung 2's set; it is a
misspecified rung-3 variant, not one of the four rigorous estimators, and the designer should weigh whether the
judge could read it as a defensible estimator (Hinckley 97.20, 0.20 over the line). (5) Ask B's re-zoning is 49
store-chain moves (PZ26-04), one more ambient move (Hinckley to Thurrock, three East Midlands stores) than the sheet
so that no two ask B stops coincide on Thurrock; Daventry to Warrington returns five of six on 27 December so that
the start-map basis and missed Boxing Day closures cannot cancel. (6) Each graded ask figure sits inside its bin
by one quiet quantity per centre (one plain face's quantity for ask A, one steady store's forecast for ask B,
listed by `build.py`), never on the exact bin centre.

**Pre-round repair (stage 4, after leak read 1; no rung, pin, decisive step or shipped file changed).** Item (4)
above is closed as SF13: the per-day accrual pooled over the classes is not a rigorous variant, and the routine
counts rule it out by their own class separation (non-overlapping per-day hazard intervals and the pooled rate's
class mis-prediction, asserted per centre). The reader's first-against-confirmed count is closed as SF14: the two
readings differ (the first count gives Bellshill, Daventry, Hinckley and Magor), and CP-THN-04 s.5 with SCS-07 4.2
is the ruling text, asserted present in the shipped docx. `checks.py` 860 assertions green; target files and
target.zip byte-unchanged.

**Separation (asserted).** Main population: 26,188 in-scope rows of `wms_location_master_THN_eff.csv` and their
105,279 rows of the count history; device and hazard rows inside it: 0 (no batch, cost, depot, store or age column
on either file; the main estimate recomputes from those two files alone). Device rows elsewhere: 5,592 snapshot rows
on 2,497 multi-batch locations (D6), 11,663 eaches rows (H2), 1,512 superseded case-size rows (H2), 2,460 period-10
rows (H1), 73 PZ26-04 servicing rows on 49 store-chains (D2), 49,308 forecast rows in units (H2), 492 forecast rows
on the 41 Boxing Day closures (H3). Every subset of ask A mishandlings (fan-out, units, case-size version, period
10) and every combination of ask B basis (run, start map), units and closures lands outside the bin on every
centre; the over-cleaned stops land low; each ask's five stops are distinct. Cracker sheet asserted: ask A, ask B,
the chart's order and its title all missed (the run's depots put Thurrock first). Pair ceiling 32.

**leak.py on the final cut: REVIEW (10 lines), no LEAK.** Each answered:
- SCS-07 carries 97.0: the filed line of 5.1, which the prompt asks the page to show beside each share; it is the
  threshold, not an answer figure.
- CP-THN-04, SCS-07 and the extract notes share 9, 7 and 5 stump-paragraph terms (record, counts, routine,
  history, accuracy): the vocabulary of any count programme and accuracy standard. Read for the move: no sentence
  names a face's time since its last count, an age, a decay, an accrual or a reset, and none defines or reports a
  count-based accuracy; the posting and due-date clauses are the filed facts the design needs (`## Literal reader`).
- Dates after 7 December in the forecast run (the freeze it forecasts), the servicing map (PZ26-04 validity), the
  trading calendar (Christmas and New Year), the snapshot and batch register (best-before dates) and the goods-in
  summary (bookings over the freeze): each is a forward date a real extract carries on the day of the pull; the
  allow-list is exactly these six files (H16).

## Hardening loop 1 (architecture 2, paper)

**Inputs (2026-10-11).** Round 1 (`solver_rounds/round-1-architecture-2.md`, the round's row and brief in
`pipeline.json`): the call landed, every ask item cracked, proxy 97.9. Designer pass on paper; no data cut.

### Default path, rewritten from round 1

1. Read SCS-07 v3 (scope 4.1, the correct-record test 4.2, the estimand 4.3, the measurement time 4.4, the
   estimate a full count then would be expected to bear out 4.5, the 97.0 per cent line 5.1) and CP-THN-04
   (classes A 28, B 56, C 91 days; routine CYC counts; exception codes SHP, NEG, EMP, OVR; the confirmed count
   posted as the record).
2. Take the in-scope faces from the location master version in force on 7 December (pick face, Thornacre,
   line present, active): 26,188.
3. Mark each count correct when the confirmed count equals the system quantity, set the exception counts
   aside as symptom-led and keep the 93,136 routine counts.
4. See the routine match rate fall with days since the face's previous count (class A about 98 per cent at 0
   to 7 days, about 88 at 28) and fit a per-day error rate for each centre and class on the routine counts by
   that age.
5. Apply each centre and class rate to every in-scope face's days since its last count of any reason at
   06:00 on 7 December, average per centre (a linear model agrees within 0.1) and compare with 97.0.

Ends on: Hinckley, Daventry, Bellshill, Warrington, Magor and Avonmouth qualify; Thurrock and Doncaster stay
on supervised replenishment. The golden is the same six, so the ladder as drawn carries no stump (`stumping`
1.5): the competent default construction is the decisive rung.

### What kept four solvers off the call, and how this build differs

- **task182** (round 1, missed at the coal-measures counterfactual): its control regression on the far-field
  coal-measure bore fitted the pre-take record closely, but that bore was itself being drawn down as the cone
  spread, and only each bore's own years-long response to rain, calibrated before the take, sees the
  drawdown. Here nothing outside round 1's model is left out: its age-conditional routine rate already
  describes the faces at the stand-down.
- **task446 architecture 2** (round 2, missed at the basis choice): it ran the filed leave-one-cohort-out test
  over the two bases it thought of and accepted a 40.6 per cent miss, never trying fixed capture and
  false-alarm rates. Here no filed test can ship (a past full count scores estimators, a control bench), and
  round 1's estimator is the field's own construction, not a narrow candidate set.
- **task133 loop 1** (round 1, missed at R3): the conditioning divisor needs the closures in the development
  sample, a second file nothing points at, and every control ties without it. Here both events that end a
  record's run (routine and exception counts) sit in the one file the solver reads, and it used both
  correctly.
- **task445** (round 1, missed at R0): it conformed every filed line and stopped at the reports in hand, a
  miss the portal then failed as `answer_contradicts_files` because the literal reading supported it. Here
  the estimand is filed literally and was executed exactly; no reading is left to lean on, and leaning on one
  would repeat task445's failure.

### The search for a rung above round 1's model

**What a rung needs.** Round 1's accrual model completes, its checks pass, and the answer is still wrong; the
step is the stock-control field's own; no symptom reaches the solver's exploration; nothing is planted; it is
not task46's exposure clock (handling in place of days) and not a third reset driver (task132's renewal and
this build's count reset).

**Why the field is empty here.** Round 1 reads, for each centre and class, the share of routine counts that
matched at each age since the face's last count of any kind, and applies it to each face's age at 06:00. The
routine due dates fall on the class grid whatever the face's state, and the error process is stationary, so
the routine counts at each age describe faces with the same history as the faces standing at that age at the
stand-down (no count of any kind for that many days). The one selection left, that faces reset by an
exception are the error-prone ones, shows in the routine counts at short ages long before it moves the
estimate (measured below). A rung above the model therefore needs one of two openings, and each fails a
bound: an error rate that changes into the peak (driven by handling it is task46's clock; driven by a dated
cause it is a step the event study aligns and the routine counts show by month, `stumping` Part 9), or
routine counting whose timing depends on the face's state (a symptom in the routine counts, or a reason code
to classify, which is data semantics).

| Candidate | What it would turn on | Verdict |
|---|---|---|
| a persistent cause the count does not remove (a look-alike neighbour, a wrong case size): a share of faces with higher silent and loud rates | faces last reset by an exception are the error-prone ones, so the stand-down's mix at each age differs from the routine counts' | dead, measured (`/home/user/orch/buildwork-task229/d2h1/frail.py`, 20 per cent of faces at four times both rates, six seeds): round 1's estimate moves 0.0 to +0.4 points (realisation spread 0.1 to 0.4) while the class A routine counts run 3 to 10 points under the fitted curve at 8 to 21 days, a symptom with no flip; fitting by the previous count's type moves nothing |
| follow-up counts after a found difference | routine timing tied to the last result | dead: a reason code the solver classifies (data semantics), and on the routine path the same visible symptom |
| an error rate climbing into the peak with volume | per-handling exposure | dead: task46's driver, rejected at the draw |
| an error rate climbing with the agency share or a dated change | a calendar step | dead: a dated cause the routine counts show by month and the event study aligns |
| imperfect resets (a posting over a later movement, an exception count of part of a face, an adjustment held for approval) | the reset's quality | dead: a third reset driver |
| peak lines slotted in November | a population shift | dead: a reflex stratification on a line attribute, or no routine counts to force their rate |
| a past full count as a back-test of estimators | a filed selection criterion | dead: a control bench that nominates the survivor (screen test 4) |
| a confidence bound in 4.5 in place of the expected share | statistical rigor | dead: moves WHAT and is generic statistics, not the field's step |
| open exception tasks or pending recounts at the stand-down | faces known wrong at 06:00 | dead: a status column decides it (data semantics) |
| catch-weight lines drifting inside the scale tolerance | a non-exponential accrual | dead: the routine counts show the flat start and the linear cross-check breaks (a symptom), and the drift accrues per pick (handling) |

**The ask layer.** Every round 1 device fell to the hygiene battery: one quantity per location over the
repeated batch rows, the period-10 change file over the base list, singles to cases, the closed trading days
and the servicing map in force on each date. No ask redesign is drawn, because an ask layer cannot hold a
build whose call lands (both top responses bank about 45 before an ask, `supplemental-stumping` Part 0).

**Decision: spent.** No rung above round 1's accrual model passes the screen within the loop's bounds, and
the only fixes that would stop this solver are a plant or a symptom it would follow. A second round on this
ladder would spend a round on a pack that cannot hold, so architecture 2 is spent after one landing and the
number re-roots to architecture 3, its last, drawn fresh at stage 1.

## Architecture 1 record (spent 2026-10-11)

Kept as the record of the spent architecture; nothing below binds architecture 2's build.

### Rework after the portal result (2026-10-11)

- **What the portal said.** The stump held: both portal models diverged from the ground truth and the
  rubric scored under 50. Determinism QC failed with both reviewers: R1 C and D fail, G fail,
  `competing_defensible_answer`; R2 C, D and E fail, `underspecified_objective`; both put the fix in the
  input files. The fork was the standard error's construction: the old 7 ("standard deviations are
  sample standard deviations ... and standard errors are built from them") with the old 4.3 read
  literally as sample SD over root n across installations, which fires EM3.12.0 and EM3.12.2, and the
  reason to build the error over the nodes lived only in the write-up's steps. The in-house Gate H pass
  then called the domain a backdrop (H1): a general-statistics clustered error in an energy setting,
  under a domain whose task types list nothing that serves Data Quality Monitoring.
- **The author's fix, done.** (A) MDS-STD-114 now defines the estimand and not the estimator (4.3 a scope
  exclusion, 4.4 the standard error as the spread over repeats of the week with co-moving installations
  as one unit, 5.2 the limit, 7 the rounding path and the divisor over independent units); no sentence
  names a unit, the node field, a network element or an estimator (`## Why the standard defines the
  estimand and not the estimator`). (B) The domain is re-filed under General Statistics & Data Science,
  missing-data-censoring-measurement-error, on the card, in the write-up's Tags, in `metadata.json` and
  here. (C) Data, stump and committed answer are unchanged: the rebuilt pack differs from the
  portal-tested one only in the standard's PDF, every graded figure is the same, and 271 assertions,
  the verifier and two byte-identical builds are green. The determinism targets are asserted in
  `checks.py` (`## Stump or fork`, (i) to (iv)).
- **Not changed, on purpose.** The prompt (a changed prompt changes the solver surface for nothing the
  fork needs), the world and every data file, the asks and the goldens' figures.

### DRAW

| Axis | Value |
|---|---|
| Domain / subdomain | General Statistics & Data Science / missing-data-censoring-measurement-error (the task type serves Data Quality Monitoring): the deciding quantity is the standard error of a missing-reads rate under dependent missingness, in a smart-meter metering data provider's world. First shipped as Energy Systems & Utilities / other, re-filed after the portal result (`## Tried and rejected`) |
| Objective | Data Quality Monitoring & Alerting |
| Niche | a smart-meter data provider's read-health gate on the communications-module firmware builds live in its fleet, deciding which builds the read-health alert fires on before the next rollout wave |
| Shape | 10 scorecard against thresholds: eight builds, each with read health, its standard error, lower limit, distance from the limit and fire or hold, plus the Wave 8 moves and the Settlement substitution load under the call |
| Decision type / unit | designation_set (which builds the alert fires on) / set_of_items |
| Gap / pattern / generators | population (decisive: the unit the noise lives in is the comms node the installations share, not the installation; the file grain is the register-day delivery), time (the delivery cut-off as of which a read counts); pattern D (two grains, both flawless: installation and node); G2 grain mismatch, G7 operating window, G12, G17 statistical rigor |
| Gate G mechanism | signal_vs_noise_or_hold (which builds sit below the reference by more than their own noise; five of eight hold, two of them on the noise their shared nodes carry) |
| Stump strategy | grain_or_unit; decisive rule filed (the standard defines the measure, the reference, the three-standard-error limit and, in 4.4, what the standard error measures: the spread of the build's read health over repeats of the week, installations whose read losses move together counting as one unit); the step that turns the rule into the answer (which installations move together, and so the units the error counts) is in no sentence, and no sentence names a unit, a field or an estimator; no official decoy; no validated decoy; no calibration organ |
| Layer 2 | estimation_fit, `survey-research-official-statistics/complex-survey-estimation-variance/1` (variance must reflect the primary units; a simple-random-sample formula on the respondent count understates it severalfold for clustered items), made this build's own: the primary unit is the mesh collector or access point, because a node that misses a night's collection takes that day from most of the installations behind it at once, and firmware waves are pushed node by node, so a build's installations are concentrated behind few nodes |
| Layer 1 | interval reads with quality codes at mixed 5, 15 and 30 minute resolution; register-days re-delivered when a later retrieval completes them, and days the MDM held nothing for until its estimation run; receipts in UTC, market time in AEST, field times in AEDT, against a filed cut-off; firmware build codes spelled three ways; effective-dated meter-to-installation assignments with mid-week exchanges; head-end events replayed after a failover and failed activations rolled back; each meter's comms parent in the head-end record with the date it joined |
| Calibration form | none, because the strategy is a stated rule whose construction is the work; no closed corpus is needed or shipped |
| Context artifact | filed_standard (the read-health standard MDS-STD-114 the gate runs on; redrawn from monitoring_export once task228, drawn earlier the same day, took that type) |
| Stakeholder | metering data services lead, who owns the read-health alert the rollout desk gates each wave on |
| Forum / forcing event / org family | operations_desk (the rollout desk holds the wave for any build the alert fires on) / cutover_or_migration (Wave 8 of the firmware migration goes out on Tuesday night) / utility_or_infrastructure |
| World | Halvane Metering, an accredited metering provider and metering data provider in the National Electricity Market, New South Wales, AUD; personas drawn with `guard.py names --locale en_AU --seed 229` |
| Deliverables | `wave8_read_health_alerts.json` (the alert payload the routing system ingests: commits), `read_health_by_build_wk41.png` (reads at a glance) |
| Guard | re-filed card (rework): check WARN on three_rules.strategy_risk, repeat.opening against task134 and repeat.geography against task133 (answered below), NOTE same_puzzle_older against task98 v3 (differentiated on the card), registered; heart WARN, nearest heart text 0.04 (task60's ledger row), nearest driver 0.06 (task87 v3); surface 0 promoted pairs, nearest 0.10, no persona in the pack. First ship: heart WARN on repeat.gate_g against task228 (answered below; task228 has since re-rooted to architecture 2 in physical-environmental-sciences and its live card is copied in); adjudicated pre-flight on the loop-1 driver CLEAN (`clone_check_report.md`), and the driver has not changed |

**Rework WARNs, answered.** `three_rules.strategy_risk`: the decisive step is not reading a field or
applying a rule; 4.4 states what the error measures and leaves which installations move together to the
data, and the analyst test (`## Three rules`) names the easy route that still fails once every field and
rule is read correctly. `repeat.opening` against task134 and `repeat.geography` against task133: the
prompt and the world are the ones the portal tested, and the rework changes neither, because a changed
prompt would change the solver surface for no determinism gain.

**WARN repeat.gate_g (task228), answered.** Both builds label their Gate G mechanism
signal_vs_noise_or_hold because both are alerting calls; task228 picks which metric an alert should
watch from a replay of past check nights (one of N), task229 constructs one stated measure and the
error that measure carries on a network whose nodes fail together, and designates the builds that
breach. The decisive constructions share nothing.

**Coordination with task228.** Drawn the same day in the same objective. task228 holds the
product-analytics experiment-platform guardrail world; this build differs in domain (energy
utilities), organisation (a metering data provider), forum (the rollout desk), forcing event (a
firmware migration wave), geography (New South Wales), personas (en_AU draw), data structure
(register-day deliveries of interval counts by quality flag, an activation history and a two-mesh
topology), stump strategy (grain_or_unit on the unit of the error) and context-artifact type.
task228's card is copied into this build's cards folder so the guard sees both. The prompt avoids the
six idioms the corpus over-uses (a named colleague's belief about the naive pick, a closing role line,
"what I need is", a chart title asked for last, the pick marked on the chart, the runner-up beside the
pick).

**Data-native sentence.** An AMI mesh collects every meter's day through a collector or access point,
and when a node's backhaul or power fails overnight the day of most of the meters behind it misses the
MDM's cut-off together; firmware waves are pushed node by node, so a build's installations sit behind
few nodes, and on this fleet a build's weekly read health is a draw of its nodes' nights, not of
independent installations. The standard says which property matters (losses that move together count
once) and the data say where it holds; a capable analyst whose pipeline is a list of installations looks
for that property in each installation's own rows, where it cannot show.

**Why every element is real.** NEM metering data providers deliver interval data with quality flags
(actual, substituted, estimated) by register and day, re-deliver a day when a later retrieval
recovers the reads, and work in market time (AEST) while field crews and the head-end log local or
UTC time; RF mesh head-ends record each meter's parent node, collect the day overnight and backfill a
node's meters when it comes back; firmware is downloaded through the node, so waves go node by node,
with a go/no-go per build.

### Stump sentence

A competent solver applies MDS-STD-114 correctly (installations whose meter ran a build all week, reads
held at the 06:00 AEST cut-off against every expected interval of every stream, the mean of the
installations' read health) and reads 4.4: a build's standard error is the spread its read health would
show across repeats of the week, installations whose read losses move together counting as one unit.
It then looks for losses that move together where its pipeline already is, in each installation's own
register-days and the register's fields (network, data streams, interval length), finds none, and keeps
every installation as its own unit: the sample standard deviation over the square root of the
installation count. The alert fires on EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2 and PX5.2.7, Wave 8's
1,274 moves onto EM3.12.2 stop, and Settlement Operations is warned of 5,379 installations. The step
that carries the stump is diagnosing which installations move together. The EM3.12.2 installations the
standard assesses were piloted on seven collectors, and on Thursday 8 October one of them (EMC-8631)
missed the night's collection and its backlog reached the MDM after 10:16 the next morning, so 20 of
its 23 EM3.12.2 installations held nothing for that day at the cut-off, together; two collectors in the
newer suburbs did the same to 121 EM3.12.0 installations on the Monday and the Sunday, and EMC-8631 to
32 more. Only the head-end's comms parent records what ties those installations together. Counted one unit per collector or access point, EM3.12.2's standard
error is 1.83 (not 0.40) and EM3.12.0's is 0.57 (not 0.09), both hold, and the alert fires on EM3.12.1,
EM3.10.9 and PX5.2.7 only, whose shortfalls are spread across their nodes and fire on either error.

### Gate G

- **Litmus.** No reported number or stakeholder conclusion is overturned. The pack carries no
  read-health report, no scorecard and no ranking of the builds; the MDM receipts, the head-end
  history and the register are correct records of what happened, the node failures included (they
  are real reads that were not held, and the standard counts them on purpose). The prompt carries no
  stakeholder belief. The difficulty is constructing the measure and the error the standard defines:
  the unit, the population, the version, the expected reads the deliveries do not carry, and the units
  the error counts, which 4.4 defines by a property and the data locate. Answer: no.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Primary mechanism:** signal_vs_noise_or_hold (which builds sit below the reference by more than
  their own noise), with `statistical_rigor` support (the error built over the units that fail
  independently). The unit itself is Pattern D, two grains both flawless: the installation and the
  node.
- **Deletion test.** Nothing in the pack is wrong; there is nothing to delete. Still hard because the
  installation-level error and the node-level error are both arithmetically perfect and disagree on
  two builds.
- **Clean-data test (asserted).** Repair the Layer 1 mess on the main path (replayed head-end events
  removed, the first-delivery and latest-delivery versions set aside for the cut-off version, every
  register-day given its expected intervals): the answer does not move and the installation-level
  answer does not move, and they differ. The node failures are not a defect to repair: they are reads
  that did not reach the MDM by the cut-off, the standard's own measure; an instrument that dropped
  them would be measuring something the standard does not score.
- **Lens-swap test.** The naive reading and the answer are not one population at one moment: the
  natural pipeline takes 7,930 installations on their end-of-week build with the latest deliveries,
  pooled; the answer takes the 6,729 that ran one build all week, the deliveries held at each day's
  cut-off against every expected interval, the mean, and an error built over 3 to 53 nodes per build.
  The last rung is not a re-reading of a stated figure: no figure is stated, and the units of the error
  are found from the data's own dependence (below), which 4.4 asks for and does not supply.
- **Forward framing.** The measure is of the week just closed, which is what the standard scores;
  the decision is forward (Wave 8 moves nothing onto a build the alert fires on). A Data Quality
  Monitoring call is a gate on the next action, and its evidence is the last complete window by
  design.

### Three rules (the client's 10/10 update)

- **Domain (H1).** General Statistics & Data Science, missing data, censoring and measurement error. The
  deciding quantity is the standard error of a missing-data rate (the share of expected interval reads
  not held at the cut-off) when the missingness is dependent: reads go missing together for every meter
  behind a collection node that misses a night, so the error has to count each set of co-missing
  installations once. That is the domain's own analysis (how missingness that is not independent
  inflates the uncertainty of the rate it leaves), and the smart-meter world is where the data come
  from, as it must be for a general-statistics task. The swap test reads the statistical nouns, not the
  setting's: put a stated score or a lookup in place of the dependent-missingness error and nothing of
  the domain's work is left.
- **Layers (H2).** Layer 1 and Layer 2 as in `## Layers`: system mess with no planted defect (overlapping
  deliveries, three clocks, re-stored head-end events, rollbacks, serials and NMIs in two shapes, a
  re-batched schedule), and the error of a mean under dependent missingness as the step that decides.
- **Decisive step (H3): analytical.** The analyst test: a strong analyst who cleans the receipts, applies
  the cut-off, actual-read, assessed-installation and mean rules correctly and reads 4.4 still takes the
  easy route, looking for co-moving losses only in each installation's own rows and keeping every
  installation as its own unit (sample SD over root n), which fires EM3.10.9, EM3.12.0, EM3.12.1,
  EM3.12.2 and PX5.2.7 and stops Wave 8's 1,274 moves onto EM3.12.2. 4.4 states what the error measures;
  it does not say which installations move together, which field records the tie or how to count it,
  so the decisive step is diagnosing the data's dependence structure and choosing the unit of analysis,
  which the client counts as analysis. Lower rungs (the cut-off, the expected reads, the assessed
  population, the mean) are stated rules and are not what decides.

### Stump or fork

The first ship's rounds (2 and 3) had every solver miss the call at R4, and they said why they never
used the node field: "the planned-interruption and comms_parent data were not used because the
standard sets no exclusions for them". The portal reviewers then showed that the miss was not yet
forced: the standard's old 7 ("standard deviations are sample standard deviations ... and standard
errors are built from them") and old 4.3 ("only the build's own assessed installations enter its read
health and its standard error") read literally as sample SD over root n across installations, so R4
was a defensible reading of filed text. The rework makes it a reading that breaks a filed definition,
and asserts each step in `checks.py` (targets (i) to (iv) of the author's brief):

- **(i) No filed sentence is literally satisfied by the installation-level route.** The standard's
  every sentence on a standard error or a standard deviation is one of six (4.3 scope, the two of 4.4,
  5.2, the two of 7), asserted verbatim from the PDF's bytes; "built from", "sample standard
  deviation", "square root" and "less than the count" are gone, and the standard names no unit, field,
  network element or estimator (asserted word by word, and again in `verify.py` through pdftotext).
- **(ii) The installation-level route's output violates 4.4.** It counts as independent units the
  installations that lost a night together: 20 EM3.12.2 installations behind EMC-8631 on 8 October, and
  153 EM3.12.0 installations (70 behind EMC-8306 on 5 October, 51 behind EMC-2773 on 11 October, 32
  behind EMC-8631). At the rate an installation loses a whole day on every other node-night (0.14 per
  cent), each of the four failed node-nights has a binomial tail of 10^-159 to 10^-209. Its error is
  under half of every error that counts those installations as one unit, the narrowest such reading
  included (merge only the installations seen losing a night together): 0.40 against at least 1.61 for
  EM3.12.2, 0.09 against at least 0.48 for EM3.12.0.
- **(iii) Every dependence-aware construction lands the call**, every build at least 0.05 from its limit
  under every one of them (tightest 0.081, PX5.3.0 under the day grouping): the node error with and
  without the small-sample factor, the CR2 and CR3 leverage adjustments, the delete-one-node jackknife,
  the bootstrap over nodes, the narrowest merge, the installation-day panel grouped by node (the golden's
  figures to the last digit), by node-day, by day and two ways, and the random-intercept fit with its
  own mean and error. Twelve constructions, one fire set.
- **(iv) The routes the earlier passes found.**
  - *The outage carve-out* (`## The outage carve-out route`) files a wrong set on all three variants
    under either error, EM3.12.0 firing by 0.148 to 0.158, and 3.3 and 3.5 rule it out.
  - *The random-intercept hybrid* (the judge's pass-1 residual): the simple mean with the variance a
    random-intercept model gives it (the same as Kish's design effect on the size-weighted unit size)
    holds EM3.10.9 alone, 0.65 against the 0.48 it needs. Its model is refuted by EM3.10.9's own units:
    84 per cent of the spread between them comes from the four small units that lost a night (19
    installations), the model charges that spread to every unit by its size squared, and its eleven
    units of 21 to 36 installations sit at 97.67 to 99.58 against the 2.9-point spread the model gives
    them (chi-square 1.14 on 11, lower tail 1e-4). The full fit, which applies the same model to the
    mean, fires EM3.10.9 with the golden set.
  - *The unweighted error of unit means* (SD of the units' own means over root k) also holds EM3.10.9,
    and it is the error of a different figure, the mean of the units' means (97.54), not of 4.2's mean
    of installations (98.06): EM3.10.9's units run from 1 to 36 installations.
- **(v) Realism.** `## Why the standard defines the estimand and not the estimator`.

**What the repeated-week estimand leaves open, recorded so the next pass does not rediscover it.**
Re-running the world's own processes for the week 120 times on the same fleet (new node-night failures
and installation texture each time; `/home/user/orch/buildwork-task229/rework/explore/truesd.py`) puts the
standard deviation of each build's read health at about 0.53 (EM3.10.9), 0.46 (EM3.12.0), 0.74
(EM3.12.1), 1.01 (EM3.12.2), 0.63 (PX5.2.7) and 0.60 (PX5.3.0): every collector carries the same
nightly failure chance, so a build whose nodes did not fail this week still carries that risk, and no
one-week estimate sees it. Nothing the shipped files and 4.3 allow can reach those figures: EM3.12.1's
eleven collectors and PX5.2.7's fourteen access points lost no night, and 4.3 bars borrowing another
build's failures, so every estimator from the build's own week fires them. EM3.10.9 is the one build
where a within-build model (the hybrid above) reaches past the design-based estimate, because its
failures fell on its smallest units; that is the residual fork risk this build carries into the judge,
and the hand-back says so.

### Why the standard defines the estimand and not the estimator

- **What the portal reviewers asked for.** Both reviewers' fix was a clause naming the construction:
  cluster-robust over the comms parents, or installation-level. Either would close the fork they found,
  and either would break the build. An installation-level clause makes the wrong answer the filed one
  (an official decoy, which the guard bans). A clause naming the nodes or the estimator turns the
  decisive step into executing a stated rule, which is rule application under the client's third rule
  (H3), and it hands the solver the one field the step turns on.
- **What 4.4 files instead is the estimand**: what the standard error measures (the standard deviation
  of the build's read health across repeats of the week with the same installations, which is the
  textbook definition of a standard error, made explicit) and the one property of that variation the
  installation-level reading denies (installations whose read losses move together count as one unit,
  not independent ones). That closes the reviewers' fork at its root, because R4 now contradicts a filed
  definition (asserted, (ii) above) rather than an unstated convention, and it still leaves the analysis
  open: which installations move together, which field records the tie, and how an error is built that
  counts each tied group once for 4.2's mean of installations. Those are found from the data's
  structure (the node-night losses, the head-end's comms parent), which is analysis, and choosing the
  unit of analysis is the client's own example of an analytical step.
- **The divisor convention stays filed, re-pointed.** "Never repair by deletion" (`dataset-generation`
  §12): the old 7 carried the small-sample convention the graded figures need, so the new 7 keeps it
  as the divisor one less than the number of independent units (4.4) a standard deviation is estimated
  from, and adds that figures are rounded only for the report, which pins the rounding path the pass-1
  judge noted (four limits and distances move by 0.01 from a two-decimal error).
- **Why "unit" and not "source of variation".** The brief's wording was "one source of variation". In a
  standard, "source of variation" is analysis-of-variance vocabulary and points a statistician at a
  variance-components model, whose variance of the simple mean is the one within-build route that moves
  a build (EM3.10.9, above). "One unit ... not independent ones" says the same thing in the vocabulary of
  the units the variation is counted over.
- **The realism test (v).** A metering data provider's read-health standard carries a statistical gate,
  and the team that wrote three standard errors into it would define the term it gates on; "readings
  that fail together are one piece of evidence, not many" is the sentence such a team adds after a
  single collector outage trips a false alarm. 4.3 now reads as a scope exclusion (no other build's
  reads), not as an instruction about units. Nothing in the standard explains why or names the network.
- **Cards.** `decisive_rule_filed: true` (the rule that decides is 4.4 with 5.2 and 5.3);
  `official_decoy: false` (no sentence states or implies installation-level independence, and 4.4 rules
  it out wherever losses move together); the card's notes record the rework.

### The outage carve-out route (leak reader, round 2)

The reader found that setting the four node failures aside and keeping the installation-level error
landed the committed fire list, with EM3.12.0 within 0.006 of its limit. Two closures, both now in
place:

- **The pack rules the route out.** 3.3 counts every interval of every data stream metered in the
  week, and no clause excuses any cause; 3.5 says only reads held at the cut-off count. Both round-2
  solvers declined to exclude anything on exactly that reading, and the reader itself notes that no
  document states the carve-out. It is a reading that violates a filed clause, not a fork.
- **The route no longer lands by luck.** EM3.12.0's own firmware gap and outage rates were raised
  (0.074 and 0.029 to 0.085 and 0.035 a day and a week), so its shortfall without the node failures
  sits clearly under its installation-level limit: every carve-out variant (failed node-days dropped,
  the node backlog counted as held, installations behind failed nodes dropped) fires EM3.12.0 by 0.15
  and files a wrong set (asserted). The golden still holds EM3.12.0 by 0.41.
- **Re-checked after the rework.** With 4.4 filed, a solver could carve the failures out and then build
  the node error on what is left; with no failure left EM3.12.0's node error is small, and every variant
  still fires EM3.12.0 (by 0.151 to 0.158) and files a wrong set (asserted under both errors).

### Solver rounds

| Round | Cut | Plain | Skeptic | Decision |
|---|---|---|---|---|
| 1 | architecture 1 as first built | landed, 91.3 | landed, 87.4 | harden: the decisive step was a filed formula |
| 2 | loop 1 | missed at R4, 54.5 | missed at R4, 54.5 | harden the asks: read for the facts each kept about 37, no margin under 40 |
| 3 | loop 2 | missed at R4, 47.0 | missed at R4, 43.4 | pass (recorded under the PR #17 single-solver rule: the main call missed; proxy recorded) |
| 4 | rework (4.4 filed, domain re-filed) | one solver, pending | | |

Rounds 1 to 3 ran under the two-solver rule (plain and skeptic, mean proxy at most 40). PR #17 replaced
it while the judge was reading the loop-2 cut: a round is one isolated solver in a sandbox, it passes
when the solver does not commit to the main call, the proxy is recorded and does not gate, and
whether a different answer is a stump or a fork is the determinism judge's question at stage 7.
Round 3 is recorded as a pass under that rule: neither solver, and not the leak reader solving on its
own, committed to the golden fire set. No hardening loop 3 ran for the proxy. The record below is the
round as graded under the old rule, kept for the judge and the portal.

1. **Both solvers miss the main call.** Both filed fire on EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1 and
   PX5.2.7 with "SE = sample SD (n-1)/sqrt(n)" and no use of `comms_parent`, and both stopped Wave 8
   onto EM3.12.2. The round-3 leak reader, solving on its own, filed the same five fires and tried a
   cut-off sweep, AEDT, a pooled error, the build at the week start, dropping missing or estimated days
   and excluding the four failed collectors (EM3.12.0 still fires there, at minus 0.15), and never an
   error over the nodes.
2. **The proxy (recorded, no longer gating): the pair stays under 40 on the facts.** Read for what each solver filed, each kept 17 of 51 ask
   criteria (the read-health figures, six of the eight per-build alerts, PX5.3.1's Wave 8 figure and
   the chart's points and reference line) and lost every standard error, limit and distance, both
   lists, the order, EM3.12.2's Wave 8 figure, the substitution load and the chart's title, order and
   ticks: about 31 each. By grade.py's own cracked-item count (one of four items each) the pair
   arithmetic gives about 27. grade.py's decimal (47.0 and 43.4) is inflated by its matcher, which is
   the reason the skill reads the facts rather than the decimal: it accepts a number within 0.5 per
   cent of the golden (about 0.49 points on percentages near 99, so 98.89 passes for 98.40), matches
   numbers anywhere in an answer rather than on their build, credits the eligible 1,274 the solvers
   quoted beside their committed 0, and scores a capitalised word in the load item. With the
   tolerance at the prompt's rounding the decimals are 44.5 and 40.8 (`solver_rounds/round-3-*.md`).
3. **Every miss is a stump on the main thread's read** (`## Stump or fork`; the judge rules on it): the
   files refute the independence R4 assumes, and every dependence-respecting grouping lands the golden
   call. The judge agreed (`## Determinism check (stage 7)`).

### Determinism check (stage 7)

Pass 1, an isolated judge on the loop-2 cut (`determinism_check_report.md`): **DETERMINISTIC, APPROVE**,
Gate G passes (`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`). It rebuilt the chain from the ten files and
reproduced every figure in the four graded blocks to two decimals. It found the four collector-nights
(77 to 100 per cent of the installations behind one collector losing the day, at most 3 installations
elsewhere), and all nine collector-aware estimators it tried, design-based and model-based, landed the
golden call. It judged the independent-installation error an analytical error, not a licensed
reading. Its notes, and what was done:

- **Grading tolerance.** A limit or distance worked from the two-decimal standard error moves by 0.01
  for EM3.12.1, EM3.10.9, PX5.3.0 and EM3.12.0. Step 6 of the write-up now says the limits and
  distances come from the unrounded error and names the four that move by 0.01 with no call changing.
- **Wording.** The recommendation called EM3.12.0 a deciding margin; the thinnest margins are PX5.2.7
  (0.23 below) and PX5.3.0 (0.13 above), and the recommendation now names those.
- **Container nits, fixed in the generator.** The standard's PDF named Microsoft Word as its creator
  over a ReportLab structure; it now names the records system that renders it (HVM Records, already
  its producer). The three workbooks carried openpyxl's layout (inline strings, calc id 124519, a
  two-field app.xml, explicit defaults) and one shared modified stamp. They are now laid out the way
  Excel saves a workbook (shared strings, calc id 191029, full extended properties, Excel's entry order
  and 1980 entry stamps), each with its own created and last-saved stamps in UTC, matching the extract
  log's local times. The golden's Wave 8 note said the schedule was cut on 1 October; batch B was
  rebuilt on 9 October, and the note now says so.
- **Nothing graded or read moved.** The rebuilt pack was compared with the judged cut:
  - the seven text files are byte-identical;
  - the PDF's extracted text is identical page for page and parses with no error logged;
  - every workbook cell value, type, number format, bold header and frozen pane is identical. The 239
    empty Wave 8 NMI cells that openpyxl stored as empty strings are now unstored, as Excel stores
    them, and still read as empty;
  - LibreOffice opens all three workbooks;
  - the goldens' figures, the 120 assertions and the verifier are unchanged, and two builds are
    byte-identical.

  No fresh round and no second pass are owed, since no graded figure, rung or document text a solver
  reads moved.
- **The judge's cross-batch duplicate check did not run** (its allow-list barred the batch folders).
  The duplicate check stands on stage 5 (heart and adjudicated pre-flight) and on the surface screen
  against task228 (`## Build record`).

**Rework.** Pass 1's verdict is on the first ship's cut. The portal's QC then failed the build on the
fork pass 1 had not counted (the old 7 read as sample SD over root n), and the rework changes the one
document that carried it, so pass 2 runs on the rework cut after its solver round passes, and its report
is `determinism_check_report_pass2.md`.

**Reconciliation (main thread, after the verdict).**

- **Gate G.** The judge's three flags match this note's `## Gate G` exactly. Its mechanism label
  (method or model selection) is the judge's vocabulary for the move this note files as
  signal_vs_noise_or_hold with statistical_rigor support: choosing the unit of the error on honest
  data. Its stump-power paragraph calls it a signal-versus-noise call. There is no mismatch, and the
  judge names no distractor as the surface read.
- **Spec gates.** All pass:
  - 10 files in 5 formats, the largest at 95,140 rows;
  - two declared distractors, unused by the golden and named for nothing;
  - two deliverables;
  - every ask with its unit and rounding;
  - shape 10, at about 51 criteria.

### The decisive move, and why it survives the opponent

1. **Written in no sentence.** The standard defines the installation's read health, the build's read
   health as their mean, the reference, the limit as three standard errors, and (4.4) what a standard
   error measures: the spread over repeats of the week, installations whose read losses move together
   counting as one unit; 7 files the divisor over independent units and the rounding path. Nothing says
   which installations move together, that a node failure is what ties them, which field records the
   tie, or that waves go node by node. The field reference describes `comms_parent` as the node that
   collects the meter's reads, which is what the head-end field is. The rework concedes the question
   (4.4 tells the solver that co-moving losses matter) and not the answer (where they are).
2. **No sweepable corpus.** There is no prior read-health report, no published error, no closed
   corpus; nothing nominates a method.
3. **No arithmetic symptom.** The installation-level error is complete, plausible and internally
   consistent; read health is identical under both errors (only the error moves); every
   reconciliation ties. The node failures are counted the same way on either path.
4. **Not a per-row predicate.** It needs a group (each build's installations by node), the deviations
   summed within the group, and a spread across groups.
5. **Enumeration is arithmetic.** The node is a stored attribute; the move is not a filter on it but
   the finding that read losses move together at that grain, which the data force and no clause states.
   Round 2 shows the attribute alone does not hand it over: both solvers saw it and considered it only
   as an exclusion. With 4.4 filed the solver is told to look; the round after the rework measures
   whether it looks in the head-end history or only in its own installation rows.
6. **No cutover date, and the dated events sit on the wrong side.** The node failures are four
   nights on four nodes; an event study on EM3.12.2's daily read health finds Thursday's dip, which is
   real and counted, and which is exactly what makes the installation-level error fire.
7. **Survives the deletion** (above).

**First-moves test.** The opponent's first moves (execute the standard; give a mean its textbook
error) land on R4: five fires and Wave 8 stopped onto EM3.12.2. Round 1's plain solver wrote exactly
that error, and both round-2 solvers filed it.

### Layers

- **Layer 1 (the realistic mess and the system that produces it).** MDM interval receipts at
  register-day by delivery grain with A, S, F and E quality counts at 5, 15 and 30 minute resolution;
  a later delivery replaces the register-day; a day the head-end collected nothing for has no version
  until the MDM's 06:30 estimation run and arrives when the node's backlog clears; UTC receipt stamps
  against a market-time (AEST) cut-off, while the register and the schedule are in local time (AEDT
  since 4 October); the head-end history as nested JSON with staging, failed activations, rollbacks,
  decommissioning, events re-stored after a failover, and each meter's comms parent with the date it
  joined; HES image ids that the catalogue maps to release names and the schedule spells a third way;
  NMIs with and without the checksum character; serials that lost their leading zeros in the register.
- **Layer 2 (the analytical shortcut).** Treating the assessed installations as independent draws
  when the standard asks for the standard error of their mean and says that installations whose read
  losses move together are one unit: the shortcut looks for co-moving losses inside each installation's
  own record, finds none, and keeps the installation as the unit. An expert in missing data or cluster
  inference recognises it: missingness that arrives by collection path is shared by everything on the
  path, the primary units are the nodes, the effective sample of a build piloted on seven collectors is
  seven, and an error on the installation count understates the noise severalfold.
  Beneath it, the round-1 ladder stays as the lower rungs: the cut-off version, the register's expected
  reads (absence of a record is not a record of absence), the full-week population, and the mean of
  installations rather than pooled reads.

### Ladder (asserted by name in `generator/checks.py`)

Answer: fire on {EM3.12.1, EM3.10.9, PX5.2.7}, hold on the other five.

| Rung | Reading | Fires on | Killed by |
|---|---|---|---|
| R0 natural pipeline | latest delivery per register-day, every installation on its end-of-week build, pooled reads, binomial error on reads | EM3.10.9, EM3.12.0, EM3.12.2, PX5.3.0, PX5.3.1 | 3.5 (read held at cut-off) with 3.3 (every expected interval) |
| R1 | + reads held at the 06:00 cut-off against every interval of every stream (a register-day held nowhere counts zero) | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.0, PX5.3.1 | 3.6 and 3.7 (assessed installation) |
| R2 | + only installations that ran the build all week | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.0 | 4.2 (the mean of installations) |
| R3 | + the mean of installation read health | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.1 | 4.4 (the standard error of the build's read health, which is a mean of installations; reads are not independent draws) |
| R4 | + the error with each installation its own unit (sample SD over root n) | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7 | 4.4 with the node-night split: installations behind one node lose a night together, so they are one unit |
| R5 | + the error built over the nodes the installations report through | **EM3.12.1, EM3.10.9, PX5.2.7** | answer |

- **How the round-1 brief is answered.** Round 1's landing step was R4 executed as a filed formula.
  R4 is now the step a competent solver supplies by habit, it completes, and it returns five fires and
  a stopped wave; R5 is built so that exactly that step is the wrong one, from the data's structure
  and not from a clause. Round 2 measured it: both solvers filed R4.
- **Partial applications.** Dividing by the register-days the MDM held at the cut-off (instead of the
  register's expected reads) makes the node failures vanish altogether (EM3.12.2 99.83) and holds
  PX5.2.7; the cut-off applied to rows alone in the natural pipeline holds PX5.2.7 and fires six
  others; every outage carve-out fires EM3.12.0 (asserted).
- **Satisfying to stop at.** R0 is the dashboard number every MDP reports; R1 is what a careful analyst
  who read the cut-off and expected-reads clauses files; R2 is the clause-by-clause population; R3 is a
  correct mean with the error a proportion invites; R4 is the correct mean with the error every
  textbook gives a mean, which both round-2 solvers filed.
- **Position.** Calls right per rung (of eight): R0 2, R1 4, R2 5, R3 5, R4 6, R5 8. No intermediate
  rung lands the call.
- **Discriminator dominance.** EM3.12.2: 97.87 against 98.30 on the installation-level error (fires
  by 0.43), against 94.01 on the node-level error (holds by 3.86). EM3.12.0: 98.21 against 99.22 (fires
  by 1.01) or 97.80 (holds by 0.41). The three builds that fire do so on either error by at least
  0.23, because their shortfalls are spread across their nodes (EM3.12.1's 695 installations over
  eleven collectors in the older suburbs, none of which failed).
- **Convergence (asserted).** The call is the same under the twelve dependence-aware constructions of
  `## Stump or fork` (iii): the k/(k minus 1) small-sample factor and without it, CR2 and CR3, the
  delete-one-node jackknife, the bootstrap over nodes, the narrowest merge, the node, node-day, day and
  two-way groupings of the installation-day panel and the full random-intercept fit, every build at least
  0.05 from its limit under each; the installation-level error fires EM3.12.0 and EM3.12.2 under either
  divisor. No build's node-level error undercuts its installation-level error by more than 15 per cent
  (tuned), so the node grain only ever widens the noise where nodes failed.
- **Grid (asserted cell by cell).** 3 versions (cut-off, latest, first) x 3 populations (whole week,
  start-of-week build, end-of-week build) x 4 units (installation mean, pooled reads, register-day
  rows, data streams) x 6 errors (nodes with and without the small-sample factor, installations,
  binomial on reads, binomial on installations, none) x 2 denominators = 432 cells. Every cell that
  lands the call builds its error over the nodes; the ones other than the standard's reading take the
  first delivery of each register-day, which moves at least four builds' graded figures.
- **Sign discipline, margins.** Every build sits at least 0.05 percentage points from its limit, the
  distances to the limits are at least 0.04 apart (the payload's order is not a near tie), every
  two-decimal read health, standard error, limit and distance sits at least 0.0015 from its rounding
  edge, and each distance reads the same from the rounded figures as from the unrounded ones.

### Closure table (determinism-check, the 22 axes)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | installations whose meter ran the build all week | filed (3.7, 3.6); readings by start or end build are grid cells |
| 2 | Unit of account | the installation | filed (4.1, 4.2); rows, streams and reads are grid cells |
| 3 | Attribution window | market days 5 to 11 October | filed (3.2); the receipts carry only those read dates |
| 4 | As-of dating | the meter's build at the week start, no activation inside the week | filed (3.6, 3.7) |
| 5 | Version basis | latest delivery received before the cut-off | filed (3.5); first and latest are grid cells |
| 6 | Denominator | every interval of every data stream the register lists, every day | filed (3.3); the rows held at the cut-off are a grid cell; no clause excuses any interval, so an outage carve-out violates 3.3 (and files a wrong set, asserted) |
| 7 | Weighting | equal per installation | filed (4.2) |
| 8 | Window length | one week | filed (3.2) |
| 9 | Boundary inclusivity | received before 06:00; fire when strictly below | C1: no delivery lands within 8 minutes of a cut-off; no build within 0.05 of its limit |
| 10 | Rounding path | compute unrounded, report two decimals | filed (7: rounded only for the report); every figure clear of its edge; distances agree from rounded and unrounded figures |
| 11 | Tie-break | none needed | C1: no ties in the order (distances 0.04 apart) |
| 12 | Maturity | the week is closed and every cut-off has passed | C1: the extract is after Sunday's cut-off |
| 13 | Order of operations | share per installation, then mean, then the error | filed (4.1, 4.2, 5.2) |
| 14 | Row order | any | C1 |
| 15 | Duplicate resolution | head-end events by event id; deliveries by the cut-off rule | C1 for the population (replays change no assessed installation, asserted); filed for deliveries |
| 16 | Identity | NMI to 10 characters, serials to 8 digits | C1: the joins have one answer once normalised |
| 17 | Netting | not applicable | none |
| 18 | Dimensional units | interval counts only | C1: kWh totals are never used |
| 19 | Code semantics | A is a read; S, F and E are not; a rolled-back activation is not a move | filed (3.5, 3.6) and the field reference |
| 20 | Integerisation | counts are counts | C1 |
| 21 | Scope of a clause | the standard governs the alert; the Wave 8 ask and the substitution load are defined in the prompt and 6.1 | prompt wording and 6.1 |
| 22 | Forward window contents | Wave 8 moves under this week's call, on the schedule as cut | prompt wording ("once this call is applied") and 6.1 |
| + | Unit the error is built over | the node (collector or access point) each installation reports through | filed estimand (4.4: installations whose read losses move together are one unit) located by the data's structure: the independence test and the node-night split (asserted); the node is the grain that keeps an installation's whole week in one unit and every tied installation with its node, where node-day splits an installation and the narrowest merge splits a node by this week's luck; all twelve dependence-aware constructions give the same call (asserted); every assessed installation has one node and no assessed meter changed node during the week (asserted) |
| + | Small-sample convention | k/(k minus 1) over the nodes' summed deviations | filed (7: the divisor one less than the number of independent units); the call is the same without it, under CR2, CR3, the jackknife and the bootstrap (asserted) |
| + | Domain or full design | the build's own installations | filed (4.3: no reads from another build's installations enter a build's read health or its standard error) |
| + | Estimator family | design-based over the nodes (the units' summed deviations) | 4.4 defines the estimand; the design-based family and the full random-intercept fit agree on the call (asserted); the hybrid (simple mean with a random-intercept variance) holds EM3.10.9 on a model EM3.10.9's own units refute, and the unweighted error of unit means measures a different figure (asserted, `## Stump or fork` (iv)) |
| + | As-of for "run a build" | the build each in-service meter runs at the extract | C1: identical at the week's end and at the extract (asserted) |

### Ask sheet (supplemental-stumping)

Main row population: the receipts of the 6,729 assessed installations on read dates 5 to 11 October,
their meters' head-end histories up to the week start and comms parents, and their register rows.
Zero mover, exchange or schedule rows inside it (asserted).

| Ask | What it is in the decision | Device | Stops (asserted) | Named use |
|---|---|---|---|---|
| A. The scorecard: each build's read health, standard error, lower limit and distance from the limit, in order | the evidence the router files beside each fire or hold | the construction itself: the error's unit moves 24 of its 32 figures and the order | the installation-level error is wrong on every standard error, limit and distance (asserted) | the vendor desk and the rollout desk read the margins |
| B. Wave 8 moves onto EM3.12.2 and PX5.3.1 once the call is applied | the exposure each go/no-go releases, as the desk will run it on the night | D2 a schedule cut on 1 October before 37 + 9 meters went in Wave 7 and 22 were exchanged out; D7 serials that lost their leading zeros on batch A; D1 rows re-batched onto B and left on A (16 + 5), with blank NMIs on a third of batch A punishing a dedup on NMI; and the call itself (none onto a build that fires) | rows, distinct rows and one per NMI cell all miss (asserted, logged); the installation-level call 0 / 109; answer **1,274 / 109** | the desk sizes field support for the night |
| C. The substitution load: installations running a build the alert fires on | the warning 6.1 sends Settlement Operations | the call, and the build each installation runs now (movers, exchanges and bench meters on the targets for any call that fires them) | the installation-level call 5,379; answer **1,846** | Settlement Operations plans its substitutions |

**Loop 2 changes, and why.** The Wave 7 ask (moves and move-night losses) was cracked in full by all
four solvers across rounds 1 and 2: its devices (UTC and AEDT nights against market days, replays,
rollback retries) are ones these solvers handle by reflex, so it paid a response that missed the call
as much as one that landed it, and it is gone. The distance from the limit (an output of the decisive
construction for every build) and the substitution load (6.1's own routing figure, which follows the
call) replace it. Ask B carries the call on purpose: the figure the desk runs on Tuesday is the
schedule under this week's call.

**Pair arithmetic.** A response that lands the call keeps the scorecard, the chart, the substitution
load and whatever the schedule's devices leave of Wave 8. A response that misses the call on the error
keeps the eight read-health figures, six of the eight per-build alerts, PX5.3.1's Wave 8 figure and
the chart's points and reference line: about a third of the ask criteria (roughly 17 of 51), and it
loses every standard error, limit and distance, the order, both lists, EM3.12.2's Wave 8 figure, the
substitution load and the chart's title, order and ticks. The build still leans on the main call
staying missed by both top responses; the worth-it gate tests that.

### Shape and criteria

Shape 10: eight builds x (read health, standard error, lower limit, distance, fire or hold) = 40, plus
the fire and hold lists, the order, Wave 8 (2), the substitution load and the chart parts (5): about 51.

### Realism debts

- Four node-nights failing in one week across 72 nodes is a bad week for a mesh, not an impossible
  one: a backhaul SIM or a pole-top power supply takes a collector out overnight, and the backlog
  arrives after the morning cut-off.
- 2,242 installations on one build and 37 on the pilot is the shape of a real fleet mid-migration; a
  pilot spread over seven collectors at about twenty meters each is how a careful desk pilots a mesh
  firmware.
- EM3.12.1's eleven collectors are the older suburbs where the hotfix list sits; none failed this
  week, and its spread-out shortfall fires on either error.
- EM3.12.0 runs a little worse than EM3.11.4 on its own (gap and outage rates of 0.085 and 0.035),
  which is why its shortfall would fire on an installation-level error even without the node failures;
  the node failures are what make the week's evidence too noisy to fire on.
- 4.4 is a statistician's sentence in an operations standard. A metering data provider that gates
  firmware waves on three standard errors employs someone who knows what a standard error is, and the
  sentence is the kind written after a collector outage trips a false alarm; it states a definition and
  explains nothing.

### The client's pre-ship check (stage 8)

One line each, from `stumping/references/client/two-layer-task-design.md`; re-answered for the rework.

1. **The domain's own analysis, and the swap test.** The standard error of a missing-data rate under
   dependent missingness, the core of the missing-data task type; swap the statistical nouns (a score,
   a lookup) and nothing is left (`## Three rules`).
2. **Real work to put the inputs in order, none of it planted.** Ten files in five formats: register-day
   deliveries replaced by later deliveries, a cut-off in market time against UTC stamps and AEDT field
   times, an activation history with replays, failed activations and rollbacks, serials that lost their
   zeros in a CIS migration, NMIs with and without the checksum, a schedule re-batched by a depot. Each
   is what these systems export; nothing exists to be caught.
3. **The step that flips the call is a methodological choice.** Which installations' read losses move
   together, and so the units the standard error of a mean counts: independent installations, or the
   comms nodes the installations share. Nothing is planted; the node failures are real reads the
   standard counts, and 4.4 states the estimand without the unit.
4. **The analyst test holds.** Route and wrong answer in `## Three rules`: installations kept as their
   own units after 4.4 is read, five fires, Wave 8 onto EM3.12.2 stopped, a load of 5,379.
5. **One defensible method.** MDS-STD-114 files the population, the measure, the window, the cut-off, the
   reference, the rule and the standard error's estimand; the files show where losses move together;
   every dependence-aware construction lands the same call and the installation-level route breaks 4.4
   (asserted); 4.3 and 7 pin the domain, the divisor and the rounding path for the figures. The residual
   (a random-intercept variance of the simple mean, on EM3.10.9) is in `## Stump or fork`.
6. **No decoy memo, staff draft or briefing.** The pack carries no memo, no ranking, no prior read-health
   report and no stakeholder belief, and no sentence states or implies installation-level independence.
7. **The method is not hidden and recovered from certified figures.** There are no certified or
   published figures to reproduce and no corpus to back-test; the method follows from 4.4 and the
   dependence the files show.
8. **The lesson is new.** An alert's error built over the units whose data go missing together
   (dependent missingness on a monitoring gate). The adjudicated pre-flight found no Track A or Track B
   finding at any tier; the nearest mechanism neighbour (task131) is clean, and the driver is unchanged
   by the rework.

### Stopping rule

At ceiling if the portal's top two land the call; licensed one repair if the top two miss the call
but the asks leak above a fifth each. In-house: if a round has a solver build the error over the nodes
from the data alone, the architecture has no unstated step left that the data force, and the next move
is the third hardening loop or a re-root, decided on that solver's path sentence.

### Build record

- Generator: `generator/make.py` builds the pack (`build.py`), the goldens from the shipped bundle
  alone (`deliver.py` over `golden.py`), `metadata.json`, runs `checks.py` (271 assertions: the six
  rungs by name, the 432-cell grid, the standard's six sentences on the error read from the PDF and the
  words it may not use, the node-night split and the independence test, the installation-level route's
  violation of 4.4, the twelve dependence-aware constructions with their margins, the carve-out routes
  under both errors, the random-intercept hybrid and its model check, the unweighted unit-means route,
  the deciding contrasts in both directions, both asks' stops, chronology, separation, the gates, single
  statement of the reference and the cut-off, the write-up against the golden) and the independent
  `verify.py` (standard library, openpyxl and pdftotext, no shared code: the node-level error, the
  distances, the substitution load and the standard's 4.4 and 7 recomputed or read), builds a second
  time into scratch and requires byte-identical target and golden files, then cuts `target.zip` (flat,
  ten members).
- Network: two RF meshes (56 EM3 collectors in pilot, Wave 7, Wave 8, older-suburb and newer-suburb
  groups; 16 PX5 access points), installations placed by the wave history, node failures drawn per
  node per night (`world.EVENT_P`), a failure taking the day from each meter behind the node with the
  event's share as its chance and the backlog arriving between 07:05 and 12:55 AEST. Texture salts
  per build and the network salt were chosen by `tune.py` against the design's margins, edges and the
  carve-out routes.
- Surface screen (`guard.py surface task229`, loop-1 cut and again on the rework cut): 0 promoted
  pairs, nearest surface 0.10; no persona of another build in the cut pack. Against task228's pack (stage 8, final cut): the run
  was a scratch worktree holding both branches, with task228 at 6b19d41 built from its generator, and
  the worktree was removed afterwards.
  - **Result:** 0 promoted pairs, and no persona in the cut pack.
  - **Track A (task228 against task229): 0.08.** They share no file name, schema, seeded table, prompt
    or write-up wording, entity or deliverable species; both are flat, with one shared format.
  - **Track B:** they share only the population gap label (pattern, decision family and mechanism
    0), so the pair is not promoted.
- Input gates: 10 files; csv, json, md, pdf, xlsx; the MDM receipts carry 95,140 rows; distractors
  `extract_log_20261012.csv` (the pull's provenance: sources, times, coverage, record counts) and
  `dnsp_planned_interruptions_oct2026.xlsx` (the distributors' planned supply interruption
  notifications; the meters keep their interval data through daytime works, so the reads are
  unaffected while the day totals dip), both named in `metadata.json` and asserted unused by the
  golden. `hes_firmware_census_20261012.csv` (the head-end's inventory by image and status) is a
  supporting cross-check, not a distractor: solvers use it to confirm each meter's build, and once the
  fire set is known its in-service counts sum to the substitution load.

### House fixes and realism (reduce-house-fixes, golden-realism)

- H1: the standard's PDF is written invariant and stamped 24/06/2026 with the owner's records system
  as creator and producer; `scrub_producer_metadata.py` audits the target clean; workbooks carry their
  owners and their own created and last-saved stamps (UTC, matching the extract log), laid out the
  way Excel saves them (`postprocess.normalize_zip`). Goldens are script output (matplotlib, json) and
  are left as such.
- H2, H3: every figure in `submission.md` is printed by `golden.py` and re-derived by `verify.py`;
  the steps cite clauses rather than restating figures. The rework's step 5 carries one count (no
  other node lost the day for more than three of its installations on any night), recomputed on the
  assessed population.
- H8 (rework): the standard was renumbered (4.4 added, 5.2 and 7 reworded), so every clause citation in
  `submission.md`, the golden payload and the generator was swept against the PDF's clauses (3.1 to
  3.7, 4.1 to 4.4, 5.1 to 5.3, 6.1, 6.2, 7): all resolve, and the payload's note on the error now cites
  4.4.
- H4: `target.zip` members equal the ten declared files, no enclosing folder; the chart was opened
  and read after rendering (EM3.12.2's limit drawn off scale at the left edge with its value).
- H12: one convention sentence (per cent to two decimals, counts whole) carries every figure.
- H13: the call is the last sentence of the context; each later paragraph ties back to it.
- H16: no meter runs an image before its release date, no event postdates the extract, and no meter
  joins a node before it was installed (asserted); the standard (effective 01/07/2026) predates every
  document that cites it.
- H18: Wave 8's moves are the exposure each go/no-go releases, as the desk will run them under the
  call; the substitution load is 6.1's own warning to Settlement Operations; the distances are the
  margins the vendor desk reads.
- H20: the prompt names the comms firmware rollout, installations, the market and Settlement
  Operations, which place the request with a metering data provider; after the re-file the domain's
  statistical character rides on what the prompt asks for (read health, the standard error of that read
  health and its lower limit) and on the standard's 3.5, 4.1 and 4.4 (reads held against expected
  reads, and losses that move together), and the prompt is unchanged on purpose (`## Rework after the
  portal result`).
- H21: the invented organisation is Halvane Metering; distributor names (Ausgrid, Endeavour Energy) are
  the real NSW networks matching each NMI's prefix, used as texture; the register withholds address
  fields as an analytics extract does.
- golden-realism (re-run on the rework cut, after the figures were frozen and asserted; only one
  payload note changed, to cite 4.4, and the chart is byte-identical): payload carries an alert id, the
  week, the routing list, a note on the error's unit, notes sourced from the standard's own clauses,
  two-decimal percentages with signed distances;
  the chart uses the validated categorical blue for holds and the reserved critical red for fires,
  with a FIRE label beside every red mark, ink-coloured text, a title stating the call and the
  reference line labelled.

### Leak check (stage 4, mechanical half)

**Rework cut.** `leak.py --asof 2026-10-12`: REVIEW, three lines, no LEAK.

- The standard "carries 6 of 6 distinctive words of the committed call" (read-health, alert, fire, hold
  and the like, which it defines; it names no build): harmless, as on the first ship.
- The standard carries 8 of the stump paragraph's terms (together, installation, cut-off, losses,
  provider, repeat and the like): 4.4's own words. The estimand is filed on purpose (`## Why the standard
  defines the estimand and not the estimator`); it says that losses moving together count once and not
  where they move together, and names no node, field, network element or estimator. It concedes the
  question and not the answer; the solver's-eye reader and the solver round test whether that holds.
- The field reference carries 4 (installation, quality, interval, head-end): its own field semantics,
  unchanged from the first ship; harmless.
- Block 1 of the write-up first cited "MDS-STD-114 4.4", which the sweep took for two golden figures
  (114 and 4.4) found in the standard; block 1 now says "as the standard counts installations whose read
  losses move together" and the steps keep the clause citations.

**First ship.**

`leak.py --asof 2026-10-12` on the loop-2 cut, and again on the stage 8 rebuild: REVIEW, the same
three lines, no LEAK. The stage 8 rebuild changed containers only. No text under `target/` changed and
the prompt did not change, so round 3's reader pass stands (the equivalence is in `## Determinism check
(stage 7)`). (Loop 1's first run was
LEAK twice, fixed in the generator: block 4 named the reference value on the chart line, and the
standard's revision history gave the old reference as 99.30, which had become a lower limit to the
digit; the history now reads 99.20.) Each REVIEW line:

- The standard "carries 6 of 6 distinctive words of the committed call": the words are read-health,
  alert, fire, hold and the like, which the standard defines; it names no build; harmless.
- The standard carries six stump terms (cut-off, provider, measure, interval, delivery, installation)
  and the field reference five (quality, interval, delivery, carries, installation): the documents'
  own subject matter; neither mentions errors, independence, outages, carve-outs or which grouping
  matters; harmless.

Round 2's solver's-eye reader (on the loop-1 cut) quoted nothing for any question and called every
REVIEW line harmless; its solvability point is answered in `## The outage carve-out route`. Round 3's
reader (on the loop-2 cut, after the prompt changed) again quoted nothing for any question and called
every REVIEW line harmless. Two points from it:

- It names `dnsp_planned_interruptions_oct2026.xlsx` as a distractor that does not help ("none of the
  NMIs it lists in the assessment week lost reads on the notified day"), as designed.
- For question 4 it notes that once the fire set is known, the census's in-service counts sum to the
  substitution load (695 + 423 + 728 = 1,846): a second route to the same figure, which is
  convergence, not a fork, but it means the census answers a graded quantity, so it cannot stay a
  declared distractor. `metadata.json` now declares the extract log and the planned-interruption
  notifications as the two distractors and the census as a supporting cross-check (the change touches
  no shipped byte, no graded figure and no document a solver reads).

### Verdict after the rework's leak read (2026-10-11)

**What the reader did.** Its question 1 quoted 4.4 ("Installations whose read losses move together are one
unit in that standard deviation, not independent ones") and 7 ("independent units (4.4)") as telling it the
decisive step. It took the unit from the field reference's `comms_parent` row ("the node that collects the
meter's reads"), clustered on its first pass with the G/(G-1) ratio form, and reproduced the committed fire
and hold lists in the committed order (gaps -0.38, -0.34, -0.23, +0.13, +0.41, +0.52, +2.63, +3.86). It
rated 4.4 "a leak, of the principle", and raised a second fork: SD of collector means over root G holds
EM3.10.9 (+0.19 to +0.21) where the ratio form fires it (-0.34). The solver round was not run.

**Verdict: architecture 1 is spent.** Its decisive move is binary and sits on a stored, documented field.
Any filed sentence that makes the error count co-losing installations once (4.4 now) leaves only a
one-line group-by on `comms_parent`, which a strong analyst lands (the reader did, first pass): H3 and the
worth-it gate fail. Take the sentence out and the installation-level error is again the textbook reading
of "standard error", which both portal reviewers called defensible ("no shipped file mandates
clustering"). There is no third position where the step is forced by the files and still analytical,
because the analysis left after the hint is trivial. The architecture has also used its three loops (rounds
2 and 3, and this rework).

**The one in-architecture candidate, and why it is not recommended.** File only the estimand (4.4: "A build's
standard error is the standard deviation its read health would show across repeats of the assessment week
with the same installations."), no "move together" or "independent units" wording, and 7 with "the divisor
one less than the number of values it is estimated from". It removes the literal s/sqrt(n) the reviewers
objected to and keeps H3. But (a) its forcing rests on the data alone (the four node-nights, binomial tails
of 10^-159 and below), which is the evidence the reviewers already ruled insufficient; (b) it cannot close
EM3.10.9 (below); and (c) the literal estimand's true value is against the golden: re-running the world's
own week 120 times puts every build's repeated-week SD above its one-week estimate, and on those SDs every
build holds (EM3.10.9 +0.16, EM3.12.0 +0.09, EM3.12.1 +1.64, PX5.2.7 +1.12). Under 4.3 only EM3.10.9's gap is
reachable from the files, through within-build models. A coin flip at the portal, past the loop cap.

**The SE-form fork on EM3.10.9 is open in practice.** On 4.2 with 4.4 the error is the SD of the mean of
installations, and SD of collector means over root G is the SD of a different statistic, the mean of the
collector means (97.54 against 98.06), so a statistician closes it. But 7's sentence ("a standard deviation
estimated from the assessment week's reads uses the divisor one less than the number of independent units
it is estimated from") is literally satisfied by that form, so a reviewer reading the text can call both
forms compliant, and it moves the main call. It is a data property: EM3.10.9's four failed units are its
smallest (3 to 7 installations, 84 per cent of its between-unit spread), so every route that spreads that
failure risk to its large units holds it (unit-means form +0.19, random-intercept hybrid +0.52, the world's
repeated-week SD +0.16), and only the design-based ratio forms fire it (-0.33 to -0.35). No wording closes
it; a data change does.

**Recommended re-root (architecture 2), in the same pairing.** General Statistics & Data Science,
missing-data-censoring-measurement-error x Data Quality Monitoring. A third-party logistics operator's
inventory-record-accuracy gate before a client's holiday peak: which distribution centres' stock records the
client's automated replenishment may run on unattended.
- **The decisive step.** Accuracy is the share of all stock locations whose system quantity matches the
  physical count, and it is observed only on counted locations. The count programme counts
  exception-triggered locations far more often than routine ones, so the outcome is missing by design,
  missing at random given the trigger. The rate among counted locations (the count report's ready-made
  figure) describes the counts, not the population; weighting each counted location by the inverse of its
  stratum's counted share does. This is the library's partial-verification pattern
  (`diagnostic-biomarker-accuracy/1`, Begg-Greenes), made the build's own.
- **Why it can be forced without being handed over.** The estimand is plain business language, and the
  programme's trigger rules are a real filed procedure, not a decoy. The raw rate is provably another
  population's rate. Reading the procedure does not compute the weights: the counted shares come from the
  count log and the location master. The two easy routes (pooled raw rate, and routine counts only) should
  err in opposite directions.
- **Evidence the model misses it.** Measured traps 7 (uses the ready-made raw checked rate) and 13
  (validates on one population, applies to another).
- **Guard.** A scratch draft card (not registered,
  `/home/user/orch/buildwork-task229/rework/card/task229_v2_draft.json`) checks WARN with no BLOCK against main
  (f3f79d9) with task228's architecture 2 and task230's live cards in place: people.first (redraw at the
  draw) and repeat.gate_g against task134. Nearest driver 0.06 (task107). Its axes avoid the last three
  builds: shape 10, population_selection, filed_standard, operations_desk, season_or_peak,
  logistics_or_3pl, Ontario.
- **Risks to check at the draw.** The weighting family sits near task230's reweighted comparison pool, so
  run the adjudicated pre-flight for monoculture. Argue H1 as missing outcomes by design, since the
  pattern's library home is biomedical. Do not ship a summary file that sums to a graded figure (this
  pack's census did).

**Reader findings that bind any rebuild in this world.**
- The field reference defuses most of the Layer 1 mess line by line (10-character NMI, 8-digit serials,
  local Installed and Removed, staged images, ts_utc against ingested_utc, bench meters).
- The census's in-service rows for the fired images sum to the substitution load (1,846), a lookup once
  the call is made.
- The containers show generation: the PDF keeps ReportLab's page preamble and ProcSet under an overwritten
  producer, and the workbooks carry styles Excel does not write.

## Tried and rejected

- Keeping the seed's product-analytics crash-rate world: a per-user crash rate is a product health
  metric, not the health of data or of a pipeline, so the build would retag as Anomaly Detection
  without changing a word; and task228 holds product-analytics in this objective on the same day,
  so the pairing would block on `ban.pairing` at the heart check.
- First cut of PX5.2.7's late data as partial-day misses (16:00 to 24:00) that the overnight delivery
  already carried as substituted reads: a solver who applied the cut-off clause to the rows it held
  reached PX5.2.7's fire with no further thought. Replaced before any round with whole-day misses that
  leave the MDM no version of the register-day until its 06:30 estimate.
- First rounding-edge assertion measured distance to the bin centre instead of to the x.xx5 edge;
  caught on review, fixed in `tune.py` and `checks.py`, salts re-chosen.
- Architecture 1, round 1 (2026-10-11): both solvers landed the call and every scorecard figure
  (plain 91.3, skeptic 87.4). Plain path: "a build's read health is the mean of its installations'
  read health; its lower limit is 99.50 minus 3 x (sample standard deviation / square root of n)",
  read straight off section 4.2 and 5.2, with the cut-off, the register denominators and the full-week
  population executed as written. Every decisive step was a filed formula, which is the dead shape
  "a committed figure that is the output of a filed formula". Brief: keep the world and the call shape,
  and move the decisive step into the error the measure needs when outages are shared by the meters
  behind one comms node, which no formula in the pack spells out.
- Hardening loop 1, first draft (pooled share with a node-level error, never shipped): making the
  stated measure the pooled share of reads, as the brief first proposed, put the 5-minute
  three-register installations in charge of the installation-level ratio error, which then held
  EM3.12.2 on its own, and split the natural route between a binomial read count and a ratio error,
  so the decisive rung stopped being the one step every solver takes. The filed mean stays, and the
  natural error stays the one round 1 wrote.
- Hardening loop 1, node failures on the access points carrying PX5.2.7 and PX5.3.0, and on the
  older-suburb collectors carrying EM3.12.1: with fourteen and eleven nodes, one failure there widens
  a genuinely degraded build's error until it holds, which buries the signal the alert exists for.
  The tuned week keeps those nodes clean, so the builds that fire do so on a spread-out shortfall and
  the node grain only bites where nodes failed.
- Architecture 1, loop 1, round 2 (2026-10-11): both solvers missed the call at R4 (the stump held).
  Plain path: "Assessed = IN_SERVICE meter, NMI with no meter change, no activation inside the week ->
  6729 installations; mean, sample SD, SE, LL per build; fire if mean < LL -> 5 fire, 3 hold"; both
  filed fire on EM3.12.0, EM3.10.9, PX5.2.7, EM3.12.1 and EM3.12.2 and set Wave 8 onto EM3.12.2 to 0,
  and both set the node field aside "because the standard sets no exclusions for them". The asks
  leaked: `grade.py` scored each 54.5 (the fire-and-hold item's only gradable tokens are its two verbs,
  so any list scores it, and a Wave 8 answer that quoted the eligible 1,274 beside its 0 scored that
  item too); read honestly, each kept the read-health figures, PX5.3.1's Wave 8 figure and the whole
  Wave 7 ask, about 37 points, under 40 but with no margin. Decision: harden the ask layer (loop 2):
  drop Wave 7, add the distance from the limit and 6.1's substitution load, and merge the lists into
  the scorecard item.
- Loop 1's leak reader (round 2) found the outage carve-out route: setting the four node failures aside
  with the installation-level error landed the committed list with EM3.12.0 within 0.006 of its limit.
  Closed in loop 2 by raising EM3.12.0's own gap and outage rates so every carve-out fires EM3.12.0 by
  0.15 (`## The outage carve-out route`).
- The first ship (architecture 1, loop 2, judge pass 1 APPROVE), failed at the portal's determinism QC
  on 2026-10-11 with both reviewers (R1 `competing_defensible_answer`, R2 `underspecified_objective`,
  both fixing in the input files): MDS-STD-114 named the three-standard-error limit but not what the
  standard error measures, and its 7 ("standard deviations are sample standard deviations ... and
  standard errors are built from them") with 4.3 ("only the build's own assessed installations enter its
  read health and its standard error") read literally as sample SD over root n across installations,
  which fires EM3.12.0 and EM3.12.2; the reason to build the error over the nodes lived only in the
  write-up's step 6, which no solver sees. The stump itself held (both portal models diverged, rubric
  under 50). Lesson: a decisive estimator the shipped files do not force is a competing defensible
  answer however much better it is; define the estimand in the filed text so the naive method breaks a
  filed definition, and name no estimator (naming it is rule application). Its domain, Energy Systems &
  Utilities with no task type serving Data Quality Monitoring, was called a backdrop by the in-house Gate
  H pass (a general-statistics clustered error in an energy setting) and is re-filed.
- Rework 1 on architecture 1 (2026-10-11): MDS-STD-114 4.4 filed the standard error's estimand with
  "installations whose read losses move together are one unit ... not independent ones", and 7 the divisor
  over "independent units (4.4)". The solver's-eye reader quoted both for question 1, took the unit from the
  field reference's comms_parent row, clustered on its first pass and reproduced the committed lists in the
  committed order. A filed estimand that names co-moving losses hands the decisive step to a strong analyst
  (H3, worth-it gate). 7's wording also makes SD of collector means over root G look compliant, which holds
  EM3.10.9. Architecture 1 spent; re-root recommended (`## Verdict after the rework's leak read`).
- Architecture 1 re-rooted (the author's decision, 2026-10-11). Its decisive move, the unit a build
  mean's standard error is built over, was binary on a documented field: left unfiled, the portal's
  two determinism reviewers called the installation-level error a competing defensible answer; filed as
  an estimand, the leak reader clustered on its first pass. Its first domain (Energy Systems &
  Utilities) read as a backdrop under Gate H (H1). Do not redraw a gate decided by how a standard
  error is built over units that share a parent, in any world.
- Architecture 2's paused draft, decisive step weighting counted locations by the inverse of their
  stratum's counted share (dropped at the draw, 2026-10-11): under stumping Part 2's domain-coupling rule
  it is the generic reweighting the in-house solvers landed on task228 (rounds 3 and 4) and task230
  (rounds 1 and 2), and its estimand (accuracy over the window, each location once) made that reweighting
  the answer. Kept as the textbook rung of the redrawn ladder, where it lands on Magor alone.
- Exposure in handling rather than calendar days as the decisive step (rejected at the draw): it is
  task46's insight (a rate law stationary only in cumulative usage, so calendar-age routes underbuy) and
  needs a forward window whose volumes change; the estimand sits at the stand-down, where per-transaction
  and per-day accrual agree within 0.17 points (prototype 2), so the exposure choice is never the stump.
- Exception counts ignored as resets (accrual fitted on routine-to-routine intervals, resets at routine
  counts only) as a rung (rejected in prototype 2): its two errors cancel (older ages lower the share,
  longer intervals with fewer misses raise it) and it lands on the golden set within 0.2 points.
- Audit projection of count differences to the book (monetary-unit sampling, taintings, the upper
  misstatement limit) as the decisive step (rejected at the draw): under PPS the point projection is the
  Horvitz-Thompson reweighting the solvers land, the bound methods (Stringer, cell, normal) disagree with no
  filed criterion to choose among them, and a book-value misstatement is not what an unattended
  replenishment gate turns on.
- Non-blind count confirmation corrected with a blind audit subsample (sensitivity and specificity) as the
  decisive step (rejected at the draw): checking one instrument against a better reference is the
  cross-check reflex (task228's landing on collocation), and setting the non-blind counts aside is a
  natural partial route whose result the design could not force.
- A pre-peak count blitz that finds and fixes the accumulated errors (rejected at the draw): a dated spike
  of counts with a low match rate makes the reset visible to the event-study opponent, and it is Pattern
  A's resolving-candidates shape.
- An estimand three days after the data closes (rejected at the draw): it would settle the in-house
  instrument-repair question, but carrying the records forward over days with no counting invites decay
  reasoning that leads straight to the reset; the estimand sits at the stand-down, where the export closes,
  and the judge's own clean-data test passes.
- A count summary, an accuracy KPI report or a contract KPI definition in the pack (rejected at the draw):
  a shipped count-based accuracy per centre ranks the centres on the decision question and gets it wrong
  (Gate G, official decoy); the count rates stay the solver's own construction.
- Architecture 2's first paper design (written against main at 045b245, committed at 8adfec6): a six-rung
  ladder, a two-paragraph `prompt.md` that named the account director, the gate's own shares drawn as the
  chart, and the estimator left open with no filed criterion. Superseded at 3966e83: the ladder is now four
  rungs; the prompt is a one-paragraph `prompt.txt` with no persona; a chart ordered and titled on the
  decision quantity is banked by the response that lands the call (supplemental-stumping 1.4), so the chart
  moved onto ask B's forecast cases; and under PR #39 and its follow-up the estimator is forced by the design with Thornacre 4.5 (an
  estimate a full count at the measurement time would be expected to bear out), which the data settles.
- Architecture 2, round 1 (2026-10-11): the solver landed the call and cracked every ask (proxy 97.9). Its
  path: "SCS-07 does not say how to model accuracy between counts; I read 4.5 as the expected accuracy at each
  face's actual age on 7 Dec, fitted from routine counts": routine-count accuracy falls with days since the
  face's previous count (class A about 98 per cent at 0 to 7 days, about 88 at 28), an exponential error rate
  per centre and class fitted on the CYC counts and applied to every in-scope face's age from its last count
  of any reason, a linear model within 0.1. That is the design's rung 3, found from a visible symptom. Every
  ask device fell to the hygiene battery (one quantity per location over the repeated batch rows, the P10
  changes over the 28 November list, eaches to cases, the closed trading days, the servicing map in force on
  each date).
- Hardening loop 1 on architecture 2 (paper, 2026-10-11): no rung above round 1's accrual model. With the
  routine due dates on the class grid and a stationary error process, the age-conditional routine rate
  describes the faces standing at the stand-down, so a rung needs an error rate that changes into the peak
  (by handling it is task46's clock; by a dated cause the event study aligns it and the routine counts show
  it by month) or counting whose timing depends on the face's state (a symptom in the routine counts, or a
  reason code to classify). A persistent-cause layer, prototyped (20 per cent of faces at four times the
  silent and loud rates, six seeds), moved round 1's estimate by 0.0 to +0.4 points while its class A
  routine counts ran 3 to 10 points under the fitted curve at 8 to 21 days: a symptom with no flip.
  Architecture 2 spent; re-rooted to architecture 3, the number's last
  (`## Hardening loop 1 (architecture 2, paper)`). Do not redraw a gate decided by the state of units at a
  moment rebuilt from checks that reset them, in any world.

## Architecture 3 draft (phase A, stopped by the author on 2026-10-12, partial, card unregistered)

The author stopped all work on 2026-10-12 at about 00:15 UTC while a designer was drawing architecture 3 on paper. What it had written is kept below verbatim, headings demoted one level, as the starting point for the next designer. It is not a design: it has the draw, the default path, the stump sentence, the three rules and the deletion tests, and it is missing the readability screen, the semantic fork table, the ladder, the closure table, the literal-reader line, the oracles, the ask sheet, prompt.txt and the builder's work order. Its card is drafted but never checked against the window at registration or registered; the draft card follows the text.

## task229 design note

Seed DQ02 (whether the release-health alert fires on this week's build, when the metric is the
average user's rate), objective Data Quality Monitoring & Alerting.

**Where the build stands (2026-10-12).** Architecture 1 (a smart-meter data provider's read-health
alert, decided by the unit a build mean's standard error is built over) is spent: it failed the portal's
determinism QC and its estimand rework was cracked on the leak reader's first pass. Architecture 2 (a
third-party logistics operator's stock-record accuracy gate, decided by each record's state at one moment
rebuilt from the accrual since its last count) is spent: round 1 landed the call and every ask, and
hardening loop 1 found no rung above the solver's accrual model. **Architecture 3, the number's last, is
drawn here on paper** (designer pass, phase A, 2026-10-12): a new world and a new client domain, a city's
permanent cycle-counter network in urban and regional science, with the objective kept. The sections from
`## Draw` to `## Builder's work order` are architecture 3's and bind the build. Architecture 2's design and
build record is `## Architecture 2 record (spent 2026-10-11)` and architecture 1's is
`## Architecture 1 record (spent 2026-10-11)`; neither binds anything. Architecture 2's generator, pack,
goldens, write-up, metadata and leak report are removed from this folder (all in git history at b569668).

### Draw

| Axis | Draw |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task229.json` v3, drawn and registered 2026-10-12 (commit 834f2fc); architectures 1 and 2 in `lineage` with their fates |
| Domain / task type | urban-regional-science / other: the data health of a city's permanent cycle-counter network (active-travel monitoring), a client domain never built for this objective |
| Objective | Data Quality Monitoring & Alerting: the object is the health of the counter data (the share of passing cyclists each counter records) and the call is a monitoring decision (from which month each site's counts must be upgraded or flagged under the fund's condition) |
| Shape | 13, scenarios and the flip point: the season's months are the scenarios, each site's earliest failing month is graded, and the asks carry the 2026 baselines |
| Gate G mechanism | binding_constraint: the crossing signal's red phase is the constraint the default path never checks, and it removes sites from the compliant set without replacing any |
| Gap / pattern / generators | objective then time / none / G7 (decisive: operating window, a cyclist leaving a signalled crossing passes the counter only in the trail's interval), G13 (the season's months, the dates the crossings switch on) |
| Decision type / answer unit / question form | date_or_period / date_or_period / when (all three never drawn on any card before this one) |
| Stump strategy | binding_constraint; decisive rule filed: yes (the counting standard files the capture estimand and the 90 per cent condition, and the maker's report files the capture at a steady flow; nothing files the flow a gated stream crosses the loop at); official decoy: no; validated decoy: no |
| Calibration form | gold_standard_subsample: the contractor's 2025 and 2026 video audits certify the loop's capture curve, every one at a site where cyclists reached the loop unsignalled |
| Context artifact | monitoring_export (the counter portal's per-site exports) |
| Role, forum, forcing event, organisation | the lead of the city's cycle-counting programme (field_unit_lead); the provincial active transportation fund that part-funds the network and sets its monitoring condition (funder_or_donor); the four crossing signals switching on in May and June 2027 (launch_or_rollout); a city's transportation department (local_government) |
| World | Canada, Alberta: the fictional City of Pembury; the Old Spur Trail (a rail trail), the Old Spur Trail Crossings Upgrade, Tallis Counting Systems (the counter maker), the Pembury Region Travel Model; CAD |
| People | Phyllis Thompson (counting programme lead, writes the inventory and the maintenance log), Brandon Holden (signals engineer, signs the crossing design summary), Teresa Chen (transport modeller, issues the forecast); drawn with `guard.py names --geo "Canada, Alberta"` (seeds 229 and 2290) and checked by hand against every card's people: Troy, Margaret, Veronica and the surname Brown were dropped as last-twelve repeats |
| Layer 2 | field_method, `own:signal-gated-arrivals-set-a-counter-loop-capture` |
| Deliverables | `counter_season_2027.xlsx`, `trail_baseline_2026.png` |

**Data-native sentence.** On a rail trail whose four arterial road crossings switch from give-way to
signal control on 3 May and 7 June 2027, every cyclist who reaches the loop 40 metres beyond a crossing has
started across inside the trail's 18 to 22 second walk-and-bike interval of a 90 to 110 second cycle, so on
those four channels the flow over the loop while cyclists pass it is four and a half to six times the hour's
average, and a loop whose capture falls as the flow over it rises records far fewer of them than the hour's
average says.

**Guard.** `guard.py check` PASS and `guard.py heart task229` PASS against the window the 2026-10-12 date
gives (task230 v2 from its branch `perssathya/task230-event-volume-drop`, task445, task446), run on a
scratch copy of the cards folder holding task230's branch card; re-run after merging main (task135 v2,
dated 2026-10-11, sorts outside the window). One WARN on the first check, `repeat.deliverables` (svg plus
xlsx against task446), answered by moving the chart to PNG. Nearest drivers 0.10 (task94 v2 lineage, an
eight-week rolling minimum on a period plan) and 0.05 (task115, task95, task181 v2): different moves.
Furniture clear of the window: no committee_or_panel, professional_services, operations_director,
capacity_report, customer_or_counterparty, financial_institution, budget_or_appropriation or
purchase_order_or_contract. task135 v2 also carries G7 decisive (dated 2026-10-11, inside the last twelve):
its structural keys (time, G7, dial_setting; time, G7, method_or_model_selection) differ from this card's
(objective, G7, date_or_period; objective, G7, binding_constraint), and its move is a growth share under a
dial, not a gated flow.

**One line per source read.**
- task133 (held on the portal for one model): its divisor sat in a second file the natural pipeline never opened. What transfers is the shape of the miss, a deciding quantity outside the frame the solver's own checks test; here the frame is the counters' own records and audits and the deciding quantity sits in the crossing design summary. The move differs (a base for a conditional rate there, the flow a nonlinear capture is read at here).
- task182 (held in-house): the solver's regression fitted and reconciled while the deciding process (the aquifer's long memory) acted outside its window. Transfers: the default construction is complete and validated on the closed record; here the validation (the audits) is blind to the signals by construction.
- task446 (held in-house): the solver's candidate bases lacked the one that carries to the new condition. Transfers: the default uses a correct quantity on the wrong basis; here the basis is the flow over the loop, not a base rate.
- task445: its portal miss came from a literal reading of a filed clause, a fork. Avoided: the gated flow is forced by the summary's sentence that cyclists start crossing only in the walk-and-bike interval and by the maker's steady-flow definition, and the default is an easy method on the same literal estimand (`## Literal reader`).
- Client exemplars, supply-chain-logistics.md (Rail Grade Crossing Safety Programs, 0.17; Port Grain Export Loading, 0.49) and product-analytics.md (SaaS Usage Allowance Pricing, 0.20): the depth is a per-site construction graded site by site; their withheld-method architecture is capped and not used.
- layer2-rigor-patterns: healthcare-delivery "Size beds by blocking probability, not occupancy" (a response that is nonlinear in load read at the average load) and urban "Transit access depends on departure minute" (a quantity that varies within the period it is averaged over). This build's own version: a counter's capture read at the flow a signal compresses each cycle into.
- `_measured.md`: #13 validates on one population, applies to another (the audits' sites were all unsignalled), #7 uses the ready-made measure (the audited capture), #11 beats the headline trap and misses the quiet one (the quarter-hour peaking).
- `proven-in-production.md`: L1 (the audits certify the curve and are blind to the gate, because no audited loop had a signal before it), L7 (the naive basis is excellent on the closed record), L8; Part 4 checked: the decisive cause is not dated in the history (no record before 3 May 2027 carries a signal at the trail), no filed formula decides (the curve is filed; the flow it is read at is not), no forward population is named by a clause.
- The brief's spent list, checked: not the unit of a standard error, not a check that resets what it measures, not renewal, not the exposure clock, not source independence, not errors-in-variables, not regression to the mean or shrinkage, not late-arrival maturity, not comparison-pool composition, not prevalence and human detection, not competing exits, not transport (task124's analogs held down by an intervention), not repeated looks, not reweighting to a mix, not a frailty layer; and none of this block's later seeds (DQ04 to DQ25) sits in urban and regional science or turns on a gated flow.

### Default path

What this solver does (it explores, fits, checks residuals and reconciles), on the files as planned:

1. Reads the counting standard (a site meets the condition for a month when, in each direction, its loop records at least 90 per cent of the cyclists who pass over it in the month's weekday peak hours, 07:30 to 08:30 and 16:30 to 17:30 local time; the season is April to October), the fund's monitoring condition, the inventory (16 sites, their channels and positions), the Tallis test report (at a steady flow of N cyclists a minute over the loop, the loop records 99.6 minus 0.55 N per cent, tested 0 to 60 a minute in each direction), the 2027 forecast workbook (each site's weekday morning and evening peak-hour cyclists by direction and month, arrivals steady through the hour) and the crossing design summary.
2. Explores the 2026 exports and the contractor's video audits: every audited channel's recorded share sits within a point of the curve at its audited flow, so the curve describes the loops; the residuals show no pattern by site type, counter model or month (the back-test passes).
3. For every site, direction and month, turns the forecast peak-hour flow into cyclists a minute (flow over 60), reads the capture off the curve, and weights the morning and evening hours by their cyclists to get the month's capture.
4. Checks: every flow inside the curve's tested range, the forecast's link totals reconciled to its site rows, no site above the loop's rated flow, and a sensitivity on the curve's slope that moves no verdict.
5. The careful variant replaces each hour's flow with its busiest quarter hour, using each channel's 2026 peak-quarter factor, and gets Cutler Bridge from June and Lowgate Bridge from August.
6. Files the schedule: Cutler Bridge falls below the line from July and every other site holds through October.

Ends on: Cutler Bridge from July; the other fifteen sites hold the 90 per cent standard through October

Golden: Old Spur Trail at Hallett Avenue and at Ravine Road from May, at Gorse Street and at Mallory Drive from June, and Cutler Bridge from July; the other eleven sites hold through October

(Planned on the paper prototype `proto3/ladder2.py`; the builder re-tunes the world, keeps the schedule's shape and re-asserts both lines from the cut pack.)

### Stump sentence

A competent solver reads each channel's 2027 capture off the counter maker's steady-flow curve at the forecast weekday peak-hour flow, finds that the curve reproduces every video audit, and files that only Cutler Bridge falls below the 90 per cent standard, from July, while the other fifteen sites hold through October; the step that lands it there is taking the hour's average flow as the flow over the loop, when the four Old Spur Trail crossings that switch to signal control on 3 May and 7 June release each cycle's cyclists inside an 18 to 22 second walk-and-bike interval, so the channel 40 metres beyond each crossing carries four and a half to six times the hour's flow while cyclists pass it and records under 90 per cent from the month its signal starts: Hallett and Ravine from May, Gorse and Mallory from June.

### Three rules

- **Domain test:** The deciding quantity is the flow at which cyclists actually cross a counter's loop, and traffic signal control sets it: a crossing signal releases each cycle's cyclists inside its walk-and-bike interval, so beyond the crossing the flow while they pass is the cycle's cyclists over that interval, several times the hour's average; with another field's nouns there is no signal cycle gating arrivals and no loop whose capture falls with the flow over it, so the task does not survive the swap.
- **Analyst test:** A strong analyst who cleans every export and reads the counting standard, the maker's curve and the crossing design summary correctly applies the curve at each channel's forecast peak-hour flow and files that only Cutler Bridge drops below 90 per cent (from July), because nothing the hour's average shows changes at the trail; the four trail sites beyond the newly signalled crossings fall below the standard from May and June.
- **Layer 1:** per-site counter portal exports at 15-minute grain, one CSV per site, whose channel numbering runs past the bicycle loops into infrared beams at combined sites; interval stamps in local standard time all year on the trail counters' firmware family against local clock time with daylight saving on the older family; the trail loops re-terminated during the June 2026 resurfacing, the inventory keeping the installation directions; two loops in one direction on the two widest trail sections, exported under one direction label; trail chainage in the crossing summary against map coordinates in the inventory, joined through a trail centreline file; a forecast workbook keyed by model link with a link-to-site lookup; the crossing summary issued as a PDF whose timing sits in tables; video audits from a contractor timed in local clock time. None of it touches the main call's decisive step (`## Ask sheet`, separation).
- **Layer 2:** field_method. The shortcut a capable analyst takes is reading a flow-dependent capture at the period's average flow; the expert sees that a crossing signal concentrates every cyclist leaving the crossing into the trail's interval, so the loop beyond it works at the cycle's cyclists over the interval. Nothing filed says so: the summary states how the crossing operates, the maker states the curve, the standard states the estimand.
- **Stump class:** analytical. Litmus: no reported figure is overturned; the curve, the audits, the forecast and the timing plans are all correct. Not planted (the signals are the city's own upgrade in the forward window), not data semantics (no field read two ways decides; `## Semantic fork table`), not rule application (no filed rule relates a signal to a counter's capture).
- **Objective's discriminating test:** retagged as Forecasting it fails, because the 2027 flows are given and the analysis is the counters' capture of them; retagged as Anomaly Detection it fails, because nothing in any record is anomalous. The call is forward facing: the 2027 season has not opened.

### Deletion tests and Gate G

- **Delete every wrong number:** none is planted; still hard.
- **Clean-data test:** repair every Layer 1 file (the trail exports' stamps and channel order, the beam channels, the forecast's link lookup, the chainage join) and the call and the default answer do not move, because the main path reads none of them (asserted by the builder).
- **Lens swap:** no. The default and the answer read the same curve at two different constructions of the flow over the loop.
- **Identity:** capture is recorded over passing; passing is the forecast and 2027 recordings do not exist, so the identity closes over nothing shipped.
- **Corpus direction:** in every video audit the cyclists reached the loop unsignalled, because the trail crossings were give-way until May 2027 and every audited path and cycle-track site sits 300 metres or more from a signal; so the audits reproduce the curve on the naive read and say nothing about a gated channel (L1).
- **First moves:** the forecast group-by, the curve at the forecast flows, the audit back-test, the busiest-quarter refinement and the hygiene battery each end on a rung below the answer.
- **Gate G:** mechanism binding_constraint; `surface_read_dependency: no`, `stumping_family: analytical_non_defect`, `sole_data_defect: no`.

### Draft card (unregistered)

```json
{
 "task": "task229",
 "architecture": "v3",
 "drawn": "2026-10-12",
 "slot_note": "seed DQ02 (release-health alert on the average user's rate). Architecture 1 (a smart-meter data provider's read-health alert, decided by the unit of the build mean's standard error) is spent on the portal's determinism QC and the cracked estimand rework; architecture 2 (a third-party logistics operator's stock-record accuracy gate, decided by the state of each record at one moment rebuilt from the accrual since its last count) is spent at hardening loop 1. Architecture 3, the number's last, keeps the objective and re-roots in a new world and a new client domain: a city's permanent cycle-counter network in urban and regional science, decided by the flow at which cyclists actually pass a loop once a crossing signal gates them.",
 "domain": "urban-regional-science",
 "subdomain": "other",
 "client_domain": "urban-regional-science",
 "niche": "a city's permanent cycle-counter network: from which month of the 2027 counting season each counter site will record fewer than nine in ten of the cyclists passing it in the weekday peak hours, once four rail-trail crossings become signal controlled and cycling grows through the season",
 "objective": "data-quality-monitoring",
 "shape": "13",
 "decision_type": "date_or_period",
 "answer_unit": "date_or_period",
 "answer": "Upgrade or flag the Old Spur Trail counters at Hallett Avenue and Ravine Road from May 2027, at Gorse Street from June and at Mallory Drive from July, and the Cutler Bridge counter from August; the other eleven sites hold the 90 per cent capture standard through October (planned; the builder confirms it from the cut pack).",
 "answer_source": "design note, planned schedule (prototype proto3/ladder.py); replaced by the golden at ship",
 "gap": [
  "objective",
  "time"
 ],
 "pattern": [
  "none"
 ],
 "generators": [
  "G7",
  "G13"
 ],
 "gate_g": "binding_constraint",
 "calibration_form": "gold_standard_subsample",
 "stump_strategy": "binding_constraint",
 "decisive_rule_filed": true,
 "official_decoy": false,
 "validated_decoy": false,
 "stump_class": "analytical",
 "analyst_test": "A strong analyst who cleans every counter export and reads the counting standard, the counter maker's capture curve and the crossing design summary correctly applies the curve at each channel's forecast 2027 weekday peak-hour flow and files that only the busiest bridge drops below 90 per cent (in August), because nothing the hour's average shows changes at the trail; the four trail sites just beyond the newly signalled crossings fall below the standard from May, May, June and July.",
 "domain_test": "The deciding quantity is the flow at which cyclists actually cross a counter's loop, and traffic signal control sets it: a crossing signal releases each cycle's cyclists in its green, so beyond the crossing the flow while they pass is the cycle's cyclists over the green, several times the hour's average; with another field's nouns there is no signal cycle gating arrivals and no loop whose capture falls with the passing flow, so the task does not survive the swap.",
 "layer2_family": "field_method",
 "layer2_pattern": "own:signal-gated-arrivals-set-a-counter-loop-capture",
 "layer1": [
  "per-site counter portal exports at 15-minute grain, one file per site, with channel numbering that runs past the bicycle channels into pedestrian infrared channels at combined sites",
  "interval stamps in local standard time all year on one firmware family against local clock time with daylight saving on the other",
  "two loops in one direction on the widest trail sections, exported under one direction label",
  "trail chainage in the crossing design summary against map coordinates in the counter inventory",
  "a forecast workbook keyed by travel-model link, with a link-to-channel lookup",
  "a crossing design summary issued as a PDF with its timing tables",
  "video audit counts at 15-minute grain from a separate contractor, timed in local clock time"
 ],
 "context_artifact": "monitoring_export",
 "stakeholder_role": "the lead of a city's cycle-counting programme, who has to tell the provincial active transportation fund which counter sites will meet its 90 per cent capture condition through the 2027 season, and from which month each of the others must be upgraded or its counts flagged",
 "role_family": "field_unit_lead",
 "scoring_unit": "other",
 "spine": {
  "file": "per-site counter portal exports for 2026, one CSV per site, 15-minute counts by channel",
  "rows": 0,
  "entity": "one 15-minute count on one counter channel (an inductive loop for one direction of cycling, or an infrared beam for pedestrians at combined sites) at one counter site",
  "grain": "counter channel x 15-minute interval",
  "source": "synthetic"
 },
 "forum": "funder_or_donor",
 "forcing_event": "launch_or_rollout",
 "org_family": "local_government",
 "world": {
  "geography": "Canada, Alberta (a fictional mid-size city)",
  "currency": "CAD",
  "org_type": "a city's transportation department running a permanent cycle-counter network, funded in part by a provincial active transportation fund",
  "invented_names": [
   "City of Pembury",
   "Old Spur Trail",
   "Tallis Counting Systems",
   "Pembury Region Travel Model",
   "Old Spur Trail Crossings Upgrade"
  ],
  "people": [
   "Phyllis Thompson",
   "Brandon Holden",
   "Teresa Chen"
  ]
 },
 "deliverables": [
  "counter_season_2027.xlsx",
  "trail_baseline_2026.png"
 ],
 "opening_move": "question-first",
 "question_form": "when",
 "driver": "The decisive quantity is the rate at which units pass a counting point while they actually pass, which a gate upstream confines to a short open phase of each cycle; a counter whose capture falls as that rate rises records far less of a gated stream than the period's average rate implies, so a capture curve validated where arrivals were ungated and applied at the average rate passes points that the new gate pushes below the standard.",
 "driver_concrete": "Four Old Spur Trail crossings of arterial roads become signal controlled in May and June 2027, so every cyclist reaching a counter loop 40 metres beyond a crossing in that direction passes during the trail's 18 to 20 second green of a 90 to 110 second cycle; the Tallis loop records 0.55 points fewer for every extra cyclist a minute of steady flow, so at the green-phase flow (four and a half to six times the hour's average) those channels fall below 90 per cent from the month their signal starts, while every video audit that certifies the loop's curve was taken where cyclists arrived unsignalled.",
 "stump": "A competent solver applies the counter maker's capture curve to each channel's forecast 2027 weekday peak-hour flow (and, if careful, to the busiest quarter hour) and files that the network holds the 90 per cent standard all season except Cutler Bridge in August; the step that lands it there is taking the hour's average flow as the flow cyclists cross the loop at, when at the four Old Spur Trail crossings signalled from May and June every cyclist leaving a crossing passes the loop 40 metres on inside the trail's green, so those four sites fall below 90 per cent from May, May, June and July.",
 "mechanism_source": "design_note",
 "differentiation": {},
 "lineage": [
  {
   "architecture": "v1",
   "drawn": "2026-10-11",
   "fate": "spent 2026-10-11: shipped, then failed the portal's determinism QC with both reviewers (the standard error's construction was not forced: the old 7 and 4.3 read literally as sample SD over root n); the in-house Gate H pass called its first domain (energy-systems-utilities) a backdrop (H1); the estimand-route rework under general-statistics-data-science was cracked on the leak reader's first pass (the filed estimand named co-moving losses and the field reference named the node)",
   "domain": "energy-systems-utilities",
   "subdomain": "other",
   "objective": "data-quality-monitoring",
   "gap": [
    "population",
    "time"
   ],
   "pattern": [
    "D"
   ],
   "generators": [
    "G2",
    "G12",
    "G7",
    "G17"
   ],
   "gate_g": "signal_vs_noise_or_hold",
   "stump_strategy": "grain_or_unit",
   "decision_type": "designation_set",
   "driver": "The decisive quantity is the standard error of a mean over entities that fail together through a shared parent node, so it has to be built over the nodes; an error that takes each entity as an independent unit understates it severalfold for a group concentrated behind few nodes, and the alert fires on what is node noise."
  },
  {
   "architecture": "v2",
   "drawn": "2026-10-11",
   "fate": "spent 2026-10-11 at hardening loop 1 (paper): solver round 1 landed the call and cracked every ask (proxy 97.9) by fitting an error rate per centre and class on the routine counts against days since the face's last count, the design's own rung 3, found from a visible symptom (routine-count accuracy falling with days since the previous count); no rung above that accrual model completes with its checks passing and still lands wrong, so the architecture was re-rooted",
   "domain": "general-statistics-data-science",
   "subdomain": "missing-data-censoring-measurement-error",
   "objective": "data-quality-monitoring",
   "shape": "10",
   "gap": [
    "time",
    "population"
   ],
   "pattern": [
    "none"
   ],
   "generators": [
    "G13",
    "G16",
    "G17"
   ],
   "gate_g": "method_or_model_selection",
   "stump_strategy": "population_selection",
   "decision_type": "designation_set",
   "calibration_form": "none",
   "context_artifact": "operations_log",
   "role_family": "compliance_or_audit",
   "forum": "line_manager_or_team",
   "forcing_event": "season_or_peak",
   "org_family": "logistics_or_3pl",
   "layer2_family": "field_method",
   "layer2_pattern": "own:count-corrects-the-record-it-measures",
   "spine": {
    "file": "pick-face count history, Thornacre lines, eight centres, export start to the stand-down",
    "rows": 0,
    "entity": "one count task on one pick face (a cycle count or an exception count), with the system quantity, the first count, the supervisor recount where one was taken, the quantity posted, the result and the task's reason code",
    "grain": "pick face x count task",
    "source": "synthetic"
   },
   "world": {
    "geography": "United Kingdom, England, Scotland and Wales",
    "currency": "GBP",
    "org_type": "third-party logistics operator running ambient, chilled and frozen distribution centres for a grocery retail client",
    "invented_names": [
     "Corderoy Logistics",
     "Thornacre"
    ],
    "people": [
     "Rhys Flynn",
     "Stacey Sykes",
     "Arthur Mason",
     "Leonard Finch"
    ]
   },
   "niche": "a third-party logistics operator's peak stock-record gate for a grocery client: which of the eight distribution centres it runs for the client carry pick-face stock records accurate enough, at the moment counting stands down for the peak freeze, for the client's automated replenishment to order off them unattended, judged from a perpetual count programme whose cycle and exception counts each correct the record they read",
   "driver": "The decisive quantity is the share of units in a correct state at one moment, seen only through checks that record a unit's state just before setting it right; scheduled checks see each unit at the end of its interval and symptom-led checks see units because they were wrong, so the checked-unit rate, however reweighted to the population's cells, measures states that have since been reset, and the share at the moment is built unit by unit from what each has accrued since its own last check of any kind, with the accrual read from the scheduled checks alone.",
   "driver_concrete": "Corderoy's cycle and exception counts each record a pick face's system quantity against the physical count and then post the confirmed count as the record, so every count leaves the record right; the routine counts on the A, B and C cycles of four, eight and thirteen weeks see each record at the end of its cycle and the exception counts see records because a short pick or a negative balance showed them wrong, while at the stand-down each face is only part way through its cycle since its last count of any kind; so a centre's count accuracy, even with the exception counts set aside and the routine counts weighted to its A, B and C mix, understates the records it carries into the freeze, most where fast faces run long cycles, and Thornacre's 97.0 per cent gate passes six centres where the weighted count rate passes two.",
   "stump": "A competent solver takes each centre's share of correct records from its count history as the share of count tasks that matched the record and finds that no centre qualifies, all eight held on supervised replenishment, and its textbook correction (exception counts set aside as symptom-led, the routine counts weighted to the in-scope A, B and C mix) still passes only Magor and Hinckley; the step that lands it there is reading a count's result as the record's standing state, when every count also posts the confirmed quantity as the record, so routine counts see each record at the end of its cycle and exception counts see records because they were wrong, while at 06:00 on 7 December each face is only part way through its cycle since its last count of any kind, and built face by face from the accrual since that count, read off the routine counts alone, Hinckley, Daventry, Bellshill, Warrington, Magor and Avonmouth clear 97.0 per cent."
  }
 ],
 "notes": "Architecture 3 drawn 2026-10-12 (re-root of the number's last architecture, designer pass on branch perssathya/task229-rework). Decisive G-code G7 (operating window: a cyclist leaving a signalled crossing can pass the counter only in the trail's green), with G13 (the 2027 season, the months the crossings switch on); pattern none. Gate G binding_constraint and strategy binding_constraint: the crossing signal's red phase is the constraint the default path never checks, and it removes sites from the compliant set without replacing any. decisive_rule_filed true: the counting standard files the capture estimand and the 90 per cent condition, and the counter maker's test report files the capture at a steady flow; nothing files the flow at which a gated stream crosses the loop. official_decoy false: no shipped document reports a forecast capture for any site. calibration_form gold_standard_subsample: the contractor's video audits certify the loop's capture curve, all at sites where cyclists arrived unsignalled in 2025 and 2026. Window at registration (dated 2026-10-12): task230 v2 (branch perssathya/task230-event-volume-drop), task445, task446."
}
```

