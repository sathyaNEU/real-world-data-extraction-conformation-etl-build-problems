# task143: Kalvenhorst Systeme, the warranty reserve for cell lot ZC2638's Model K packs (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC14. The seed (a laptop maker's warranty reserve for a
new cell lot's three-cell packs, booked at lot release from 100-cycle qualification tests and an early-life model) was
read at its header and Situation only. Its world, decision and quantity are kept: a notebook maker qualifies each
supplier cell lot on 100 cycles, the lab's model of record turns each test cell's first 100 cycles into a predicted
cycle life, the test sample is whole formation trays, and finance books the reserve for the lot's three-cell packs on
release day, counted in packs expected to fall below 80 per cent of rated capacity within the 600-cycle warranty. The
seed's mechanism and the rest of its note are not read. The pitfall is re-found from how the records come to exist:
the model's error for a cell is mostly an effect of the formation tray it came off, which the first 100 cycles do not
show and only the earlier lots' whole trays cycled to the end do, and the pack line builds every pack from tray-mates.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task143.json`, architecture v1, registered 2026-10-15 after `git pull` (task142, task455, task260 and task141 on file); `guard.py check` WARN (strategy risk, repeat.gate_g, repeat.question_form, each answered below), no BLOCK; `guard.py validate` clean |
| Domain / task type | `general-statistics-data-science` (client domain; general statistics has never carried a forecasting build), task type `bayesian-modeling-posterior-inference` (forecasting): the call is a posterior predictive for members of new groups, the chance that the weakest of three cells from a new formation tray reaches 80 per cent before 600 cycles, which turns on the between-tray variance of the release model's error |
| Objective | Forecasting & Predictive Modeling: the number of the lot's 7,200 Model K packs that will fall below 80 per cent of rated capacity within their first 600 cycles, packs built in October 2026 whose cells were never tested, forecast from the release test and the earlier lots' life tests |
| Shape | `single-figure` (one committed count) with two ask tables and a chart supplying the criteria: the call and its components (about 5), the four repair partners' replacements and average cost (8), the twelve months' replacements (12), the chart's named parts (3) and the two files, about 30 criteria |
| Decision | `quantity_figure`, answer unit `count` (packs, to the nearest 50) |
| Mechanism | gap population (decisive: the reserve's unit is a pack of three tray-mates, whose shared share of the model error is one draw, not three) then time (the earlier lots' pack rate belongs to stronger lots than the one under release); pattern none, generators G17 decisive (statistical rigor: the error's between-tray share carried into the members' joint predictive), G2 (the pack as the unit), G6 (the lot under release predicts shorter lives than the history); Gate G `forecasting`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `estimation_fit` (clustered errors in a joint prediction); `general-statistics-data-science/bayesian-modeling-posterior-inference/2` (predict with the posterior predictive, observation noise and between-group variance, for new units in new groups): this build's version asks for the predictive of a new group's members jointly, because the reserve pays on the weakest of them |
| Furniture | forum `other` (product finance books the reserve under its release reserve policy, no meeting), forcing event `other` (the lot's release for shipment on Friday 16 October 2026, when the reserve is booked), organisation family `manufacturer` (Kalvenhorst Systeme GmbH, a business-notebook maker with its own battery plant and reliability lab), role family `finance_controller` (the notebook division's product finance controller), context artifact `monitoring_export` (the lab's life monitoring results, each finished cell's cycles to 80 per cent: a monitoring export of a past quantity that answers its own question correctly; QM-07, which files the release model of record, its two features and its validation error and no reserve, is a governing document), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `qp3_first100_cycles_fleet_a.csv` (174,006 rows) and `qp3_first100_cycles_fleet_b.csv` (130,698 rows), the reliability lab's cycler exports of the first 100 QP-3 cycles of every release-test cell (two fleets in two layouts), one row per cell per cycle, for the twenty lots whose life tests have finished, the four still running and the lot under release; constructed |
| Deliverables | `z2638_warranty_reserve.xlsx` (the reserve and its working, the partners' table and the months' table), `z2638_reserve_note.docx` (a one-page note to Product Finance opening with the reserve, with the chart of the monthly replacements by region) |
| People | drawn with `guard.py names --geo "Germany" --seed 143` and `--seed 1431`, every name the guard clears: Christiana Harloff (product finance controller, notebook division, the requester and owner of the reserve policy), Frieder Henschel (head of the battery reliability lab, author of QM-07), Dietmar Schaaf (manufacturing engineering, battery plant, the pack genealogy), Annelie Geisel (service operations analyst, the service case system); none appears in the prompt |

**Guard.** `guard.py check` on the registered card: WARN, no BLOCK. Answered: `three_rules.strategy_risk`
(grain_or_unit): the analyst test below reads every field and rule correctly and still files the wrong reserve,
because no field or rule says a pack's cells share their error; `repeat.gate_g` (forecasting beside task142): Gate G
names where the stump sits, a projection for packs whose cells were never tested, and task142's forecasting gate carries
a percentile of a period total; `repeat.question_form` (how-many beside task142): the call is a count of packs, and a
count asks how many. A first card carried pattern D (two grains, spent in fourteen builds: `test.same_puzzle_older` and
`test.same_driver_older` BLOCK) and then a decisive G2 (BLOCK `ban.pattern` against task142, whose G2 is the independent
unit of a period total); the decisive step is that a formation tray's share of the model error is one draw which the
three cells of a pack share, carried into the members' joint predictive. The draw keyed it G10 with a differentiation
line for task98 v7 (two removal lists that list some members twice); at stage 3 `guard.py surface` promoted task98 on
gap, pattern and decision family, and the card was re-keyed G17 (statistical rigor), the key a reviewer gives a
group-shared error in a joint prediction: `guard.py check` WARN as above, no BLOCK, `surface` 0 promoted. After the
stage 3 rebase, task455 re-registered after this build, which put task141 (a filed model) among the last three and
`heart` BLOCKed on `ban.artifact`; the card's context artifact is now the life monitoring export (above), the file the
dataset-generation roles call the context artifact, and `heart` is WARN again.

**Same-puzzle and same-driver tests.** Gap population, decisive G17, decision `quantity_figure`, Gate G `forecasting`:
`guard.py check` finds no build, recent or older, carrying the three together (no NOTE). task98 v7 (the draw's G10
neighbour) keeps its differentiation line on the card (a member duplicated across two dated lists, nothing of a
shared error or a weakest member); task131 v1 (lineage) is a randomised sub-unit whose lift carries outcomes moved from
its siblings: an interference effect on an experiment, not a joint prediction.

**Abstraction test.** Stripped of nouns, the driver is: the chance that the weakest of a few members taken together
from one new group falls below a threshold, when the predictor's error is mostly a group effect the members share and
shows only in the outcomes of whole groups followed to the end, so compounding each member's marginal chance as if the
members were independent overstates the count. The three nearest drivers on file (`guard.py check`): task98 v3 lineage
(units that are chains of members within a distance, not labelled groups, 0.06), task229 v1 lineage (the standard error
of a mean over entities that fail together through a shared parent, 0.06) and task256 v1 (the share whose correlated
measurements all fall inside a box, carried through a conditional distribution, 0.06). task229 v1 shares a latent
structure (members of a group fail together) but asks for an uncertainty, which clustering widens; here the quantity is
a point forecast of a series system, which the shared effect lowers, and the default and the correction both differ.
task256 is a joint probability over several correlated measurements of one person, its decisive step the transfer of
a reference distribution to a selected population; nothing there is a shared group effect or a weakest member. The
build drawn just before this one, task142 (in design), builds a period total's percentile from the admissions and stays
that generate it: its object is the spread of a sum of multi-day units, its default a count model on visits, its fix a
compound process. Here nothing is summed: the object is a joint probability over a pack's three members, its default a
correct marginal compounded as independent, its fix the between-tray variance of a model's error carried into the
members' joint predictive, and the structure is visible only in outcomes of whole trays cycled to the end, never in the
inputs. The lessons differ (the spread of a compound total against the weakest member of a group with a shared random
effect), and the guard's driver score between the two is under 0.05.

**Data-native sentence.** Zelvora forms its pouch cells six to a formation tray, and a tray's six cells share their
formation run, temperature and electrolyte fill, which set when the capacity knee arrives late in life but leave the
first 100 cycles' fade and resistance growth looking like any other tray's; Kalvenhorst's pack line takes three cells
at a time from one tray, so every Model K pack is three tray-mates, and the release model's error, which is mostly that
tray effect, is shared by a pack's cells, a structure that only the earlier lots' whole trays cycled to 80 per cent
show.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (54 builds): renewal of a replaced item
(132), conditional survival (133), hazards by time since entry (134), competing exits (134 v1), a period total built from
its generating units (142), selective labels (141): none builds a series system's failure chance from a model error
shared within groups. `layer2-rigor-patterns.md`, general statistics: bayesian-modeling-posterior-inference/2 (the
posterior predictive with between-group variance for new groups) is the decisive line, resampling/1 (resample the
independent unit) the nearest reflex it defeats when applied to cells; regression diagnostics are a lower rung (the
model's error carried at all). `two-layer-task-design.md`: "the data's real structure" and "clustered errors" are the
client's family for this step. `measured-drivers.md`: held tasks sit upstream of every graded figure; the error's
structure sits upstream of the reserve and is invisible in the inputs. The seed's header and Situation (FC14) for the
world, decision and quantity only.

**World.** Kalvenhorst Systeme GmbH (Bielefeld) builds business and rugged notebooks and assembles their battery packs
in its own battery plant on the Bielefeld site from pouch cells bought from Zelvora Cell s.r.o. (Ostrava, Czechia).
Zelvora forms its cells six to a formation tray and ships each tray's cells in one transport tray with a cell data
package (per cell: serial, formation tray, formation capacity, open-circuit voltage, AC impedance, self-discharge K
value). Kalvenhorst's incoming inspection measures every cell, rejects cells outside its limits and grades each tray A
(Model K) or B (Model J). Model K is the three-cell series pack (3S1P, rated 4,820 mAh, 11.6 V, 56 Wh) of the K14 and
K15 notebooks; its full charge capacity is that of its weakest cell. Kalvenhorst warrants a Model K pack for its first
600 cycles: a pack whose full charge capacity falls below 80 per cent of rated within its first 600 cycles is replaced.
The battery reliability lab releases each Zelvora lot on a release test: 20 A trays (120 cells) run the qualification
protocol QP-3 (1C charge, 1C discharge, 25 degrees C) for 100 cycles, and the release model of record RL-3 (memo QM-07)
predicts each cell's cycles to 80 per cent of rated capacity on QP-3 from two features of its first 100 cycles; the
cells then stay on QP-3 until they reach 80 per cent (the life monitoring program), so every lot since ZC2437 whose cells
have all finished has whole trays followed to the end. Product finance's release reserve policy (FIN-RS-04) books, on
the day a lot is released, a warranty reserve for the lot's Model K packs equal to the expected number that will fall
below 80 per cent of rated capacity within 600 cycles, cell lives taken on QP-3 as RL-3 predicts them. Lot ZC2638 was
formed from 14 to 19 September 2026; its 7,200 Model K packs were built from 28 September to 9 October and are held in
the bonded store; its release test finished on 6 October; the lot is released on Friday 16 October 2026.

As-of dates: the lab's exports, the supplier package and the pack genealogy were pulled on 12 October 2026 (the pack's
export stamp); the service case system and the DACH depot's SAP export on 5 October; the returns depot log, the carrier
statement, the partners' invoices, treasury's rates and the cost sheet on 9 October. The note is dated 15 October; the
release is Friday 16 October 2026. The service side of the world: the DACH depot in Bielefeld (SAP until 1 March 2026,
the service case system from 2 March, orders created from 1 September 2025 carried over with their SAP number) and four
repair partners, Dauvergne Réparation (Lille, FRB, EUR), Tolley Marsh Repair (Sheffield, UKI, GBP), Ljungqvist Service
(Jönköping, NOR, SEK) and Ferrucci Assistenza (Bologna, SOU, EUR), invoicing monthly in their own layouts and
languages; the warranty desk closes a partner's case when it approves the invoice that bills it.

## Default path

1. Read FIN-RS-04 (the reserve is the expected number of the lot's Model K packs that fall below 80 per cent of rated
   capacity within 600 cycles, cell lives on QP-3 as the release model predicts them) and QM-07 (RL-3's two features,
   its coefficients and its validation error of 0.182 on held-out lots).
2. Stack the two cycler fleets' exports of the release test, compute each of the 120 cells' two features exactly as
   QM-07 defines them, and predict each cell's log life with RL-3: every cell clears 600 cycles.
3. Carry the model's validation error into the prediction: each cell's chance of falling below 80 per cent within 600
   cycles is the normal tail of its predicted log life at 0.182, averaged over the 120 cells: 2.4 per cent.
4. A pack falls below 80 per cent when its weakest cell does (the pack specification), so a pack's chance is
   1 - (1 - 0.024)^3, 7.1 per cent; times 7,200 packs, 514.

Ends on: 500 packs (514 unrounded).
Golden: 400 packs (398.9 unrounded): RL-3's error on the finished lots splits into a part a formation tray's cells share
(standard deviation 0.160) and each cell's own (0.086), 78 per cent of its variance at the tray, seen only in the
finished lots' whole trays cycled to 80 per cent; 7,063 of the 7,200 packs are three tray-mates (the genealogy and the
supplier's tray map), so a pack's chance is the expectation, over a new tray's shared error, of the chance that any of
its cells falls short: 5.5 per cent.

## Stump sentence

A competent solver computes RL-3's features for lot ZC2638's 120 release-test cells, predicts each cell's life with the
model's validation error, averages each cell's chance of falling below 80 per cent within 600 cycles (2.4 per cent) and
compounds it over a pack's three cells as if they were independent, filing 500 packs (514 unrounded, Ends on); the step
that lands it there is treating a pack's three cells as independent draws when they are tray-mates and the release
model's error is mostly a formation-tray effect they share: carried through the tray effect that the finished lots'
whole trays show, a pack's chance is 5.5 per cent and the reserve 400 packs (398.9).

## Three rules

- **Task type:** `general-statistics-data-science`, `bayesian-modeling-posterior-inference` (serves Forecasting): the
  reserve is the posterior predictive, for members of new formation trays, of the chance that the weakest of a pack's
  three cells falls below 80 per cent of rated capacity within 600 cycles, under a hierarchical model of the release
  model's error with a between-tray variance.
- **Domain test:** the deciding quantity is the predictive chance that the weakest of three new cells from one new
  tray falls below the warranty line, which the task type gets by integrating the between-tray variance of the model
  error over the members a pack shares, estimated from the finished lots' whole trays followed to the end; the generic
  summary of the model's accuracy (one pooled error, applied to each cell independently) files 500 packs (514) against
  400 (398.9), so the call turns on the predictive for new groups, the task type's own object.
- **Swap:** in general statistics the setting is another field's, so the swap that matters is of the method: "the lot's
  reserve is 400 packs because a pack's three cells share their tray's error" read with the posterior predictive
  replaced by the pooled cell-level error compounded independently ("each cell fails with 2.4 per cent, a pack with
  7.1") files 500; read with another field's nouns ("a hospital's three-drug regimens") the sentence loses the series
  pack that fails with its weakest cell, the formation tray whose effect appears only at the knee of life, and the
  release test whose 100 cycles cannot see it, so what makes the joint chance differ from the compounded one stops
  making sense.
- **Layer 1:** on the call's path, the release test's cycles come from two cycler fleets exporting different layouts
  (column names, semicolons and decimal commas against commas and points, Bielefeld wall time against UTC, the
  protocol's first cycle numbered 0 on fleet A and 1 on fleet B), cells split across them tray by tray; fleet B's
  export assembled from weekly pulls overlapping by a day, so some cycles arrive twice; a test stopped by a channel
  fault continued on the other fleet as a new test; cell serials in three forms (the supplier's, fleet A's, fleet B's
  and the line scanner's); Zelvora's tray key changing its format from lot ZC2532; life tests stopped by a thermal
  alarm or a channel fault before 80 per cent; packs completed from part trays when incoming inspection rejected a
  cell. On the ask paths, the service case system, the DACH depot's SAP export and its carried-over orders, the returns
  depot's log, the carrier statement, the four partners' monthly invoices in their own languages, currencies and
  layouts, treasury's rate table and the cost sheet. Each is what these systems write; none decides the call (each
  mishandled leaves the call at 400, asserted: R2).
- **Layer 2:** `estimation_fit`: the shortcut treats the release model's validation error as each cell's own, so a
  pack's chance is the cell chance compounded over three independent cells; the expert reads the error's structure in
  the finished lots' whole trays (most of it shared by tray-mates) and builds the pack's chance from the joint
  predictive of three cells of one new tray.
- **Decisive step:** decomposing the release model's error on the finished lots' life tests into a between-tray and a
  within-tray component, and computing each pack's chance as the expectation over its tray's shared error of the chance
  that any of its three cells falls below 80 per cent within 600 cycles (the posterior predictive for members of a new
  group), with the pack's composition read from the genealogy and the supplier's tray map, instead of compounding one
  pooled cell chance over three independent cells.
- **Not semantics:** every field, code, unit and definition can be read correctly (the protocol's cycles, the features,
  the model, the warranty line, the weakest-cell rule, the genealogy, the tray map) and the default path reads them all
  correctly and still files 500 packs; nothing in the pack names a correlation, a shared error or a tray effect
  (asserted), and the answer moves only on how the joint chance of a pack's three lives is estimated.
- **Not rule application:** FIN-RS-04 files the estimand (the lot's Model K packs as built, the 80 per cent line, the
  600-cycle window, lives on QP-3 as RL-3 predicts them, the model's error on the finished lots' life tests) and QM-07
  files the model and its validation error; no rule, procedure or document says how a pack's chance is built from its
  cells' predictions, and executing every filed rule with the default construction files 500, so the step that moves
  it to 400 is performed by no filed rule.
- **Analyst test:** a strong analyst who stacks both cycler exports, computes RL-3's features exactly as QM-07 defines
  them, predicts every release-test cell's life with the model's validation error and counts a pack as failing when
  its weakest cell does files 500 packs (514, Ends on) by compounding the cell chance over three independent cells;
  checking the release test's own predictions for a tray effect finds almost none (1.5 per cent of their variance) and
  files 500 again (517), the finished lots' own tray-mate packs file 150 (162), the whole pack treated as one cell 200
  (176), and only the pack's joint chance under the between-tray share of the model error files 400 (398.9); on the
  generator's clean truth the easy route files 514 and the decisive step alone 394 (R3a and R3b asserted).
- **Estimand:** FIN-RS-04 (`fin_rs04_battery_warranty_reserve_policy.pdf`) clause 3.2: the expected number of the
  lot's Model K packs that will need a warranty replacement, the sum over the packs of each pack's probability that its
  full charge capacity falls below 80 per cent of rated capacity within its first 600 cycles; clause 2.2 the packs
  (every Model K pack built from the lot's cells by the release day); clause 3.3 the cycles (QP-3) and the lives (RL-3
  and the model's error on the life tests of every earlier lot whose life tests have finished); clause 3.4 the unit
  (packs, nearest 50). Population, outcome, window, unit, model of record and evidence window are filed; the pack's
  joint chance is not.
- **No decoy:** nothing is planted to be caught: no copied block (fleet B's repeats are whole rows of its overlapping
  pulls, asserted), no hidden rule, and no memo, draft, briefing or stakeholder figure states a reserve, a pack failure
  rate or a method; QM-07's validation error is the model's true error on held-out lots, stated as an accuracy figure
  and never as a reserve basis; the distractors (the Model J genealogy and Zelvora's certificate of analysis) rank
  nothing.
- **No certified replay:** no published reserve, certified pack failure rate or past booking ships to be reproduced;
  the tray structure of the error is estimated from the life tests on file, and no closed figure is matched to recover
  a method.
- **Lesson:** a system that fails with its weakest member, built from members that share a group's unobserved effect,
  fails less often than the members' marginal chance compounded independently, and when that effect lives in a
  predictor's error it shows only in outcomes of whole groups followed to the end, never in the inputs; no build on
  file teaches a series system's chance under a shared random effect (task229 v1 teaches the widened uncertainty of a
  mean over co-failing entities, task142 the spread of a total of multi-day units).

## Readability screen

| Rung (the move that climbs it) | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R-1 to R0: carry RL-3's validation error into each cell's chance | QM-07 section 5 states 0.182 | no | yes, a model's error is carried by reflex | no | no | no | readable |
| R0 to R1: look for a tray structure in the release test's own predictions | no | the register's tray column | yes, a clustering check | no | no | no | readable |
| R0 to R2: take the finished lots' own tray-mate packs as observed | no | no | yes, a back-test on history | no | no | no | readable |
| R3 (decisive): split RL-3's error on the finished lots' life tests by formation tray and carry the tray's share into each pack's joint chance | none: no sentence names a shared error, a tray effect, a correlation or a joint chance (asserted); FIN-RS-04 3.3 names the model's error on the finished life tests, which the default path already uses as 0.182 | the tray column sits in the register beside lot, fleet and channel, the lab's bookkeeping; nothing marks a tray as long- or short-lived | every reflex lands on 500: the validation error, the in-sample error, residuals bootstrapped per cell, the predictions' clustering | none: no record scores a pack | none: the battery passes on every route | no: a variance split and an integral over the shared error | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the lot's 7,200 Model K packs | every Model K pack built from the lot by the release day, the genealogy's 7,200 | Model J packs added; only packs shipped | Model J is another genealogy; none shipped yet | FIN-RS-04 2.2 and 1.2 (Model J under FIN-RS-05); the prompt's 7,200 Model K packs |
| SF2 | below 80 per cent of rated capacity | below 3,856 mAh | at or below | 402.5, same call | same call (asserted) |
| SF3 | within the 600-cycle warranty | within the first 600 cycles | through cycle 599 | 395.3, same call | same call (asserted) |
| SF4 | cycles | QP-3 cycles | the gauge's cycles counted another way | none | FIN-RS-04 3.3: "which are the cycles of the reliability lab's qualification protocol QP-3" |
| SF5 | a pack below 80 per cent | its weakest cell below | the cells' mean capacity below | 81.7, a miss | pack specification section 4: the pack's capacity "is that of its weakest cell" |
| SF6 | the reserve | the expected number | a high percentile of the count | above 398.9 | FIN-RS-04 3.2: "The reserve is the expected number" |
| SF7 | rounding | the expected number to the nearest 50, once | per composition class | 400 | FIN-RS-04 3.4 and the prompt |
| SF8 | the release model of record | RL-3 as QM-07 rev. 4 files it | refitted on the life tests | 400.2, same call | same call (asserted) |
| SF9 | the protocol's cycle 1 | fleet A's cycle 0, fleet B's cycle 1 | fleet A's 0 read as the protocol's first | 387.5, same call | QM-07 section 2 ("Cycle 1 is the protocol's first full cycle") and the lab's extracts note |
| SF10 | F1's logarithm | natural | common | 0, a miss | QM-07 section 3: "the natural logarithm" |
| SF11 | the life tests | the twenty finished lots' EOL cells | the open lots' running tests | not shipped | same call |
| SF12 | the packs' composition | genealogy and tray map: 7,063 three tray-mates, 136 two and one, one pack three trays | every pack three tray-mates | 397.6, same call | same call (asserted) |
| SF13 | the error's split | in-sample residuals by tray within lot | leave-one-lot-out residuals; 0.182 split at the tray share | 400.5, same call | same call (asserted) |
| SF14 | the lot's cells | the 120 release-test predictions | a normal fitted to them | 399.3, same call | same call (asserted) |
| SF15 | a lot-level error | none (restricted maximum likelihood puts it at zero) | a lot draw every pack shares | 396.0, same call | same call (asserted) |
| SF16 | the counted outcome | packs falling below the line | warranty claims made | none | FIN-RS-04 3.2: "each pack's probability that its full charge capacity falls below 80 per cent" |

## Ladder

| Rung | Construction | Packs (unrounded) | Files | Dies to |
|---|---|---|---|---|
| R-1 | each cell's point prediction against 600 cycles | 0 (0.0) | 0 | QM-07 section 5's validation error, carried by reflex |
| R0 (default) | the cell chance at 0.182 compounded over three independent cells | 500 (514.0) | 500 | the finished lots' whole trays: 78 per cent of the error is the tray's |
| R0b | the same at the in-sample residual error | 500 (508.6) | 500 | the same |
| R0c | each cell with the finished lots' residuals bootstrapped | 500 (500.8) | 500 | the same |
| R1 | the release test's predictions checked for a tray structure (1.5 per cent), cells then independent | 500 (516.6) | 500 | the structure lives in the error, visible only in finished trays' outcomes |
| R2 | the finished lots' tray-mate packs as they lived | 150 (162.1) | 150 | the lot under release predicts shorter lives than 18 of the 20 finished lots |
| R2b | the finished lots' cell share, three independent cells | 200 (180.5) | 200 | the same, and independence |
| R2c | the three weakest finished lots' tray-mate packs | 250 (242.1) | 250 | still longer-lived than ZC2638 |
| Rover | the pack as one cell | 200 (175.6) | 200 | a cell's own error, 22 per cent of the variance |
| Rx | the cell chance over two cells | 350 (346.9) | 350 | no basis |
| R3 (golden) | each pack's tray-shared joint chance | 400 (398.9) | 400 | none |

- **Constructions of the golden**, every one 400: within-lot analysis of variance 398.9, trays pooled across lots 397.4,
  restricted maximum likelihood with lots and trays 396.0 (the lot level at zero), a normal fitted to the predictions
  399.3, every pack three tray-mates 397.6, the finished lots' tray-mate residuals resampled three at a time 395.2, a
  million single-tray packs by Monte Carlo 396.6, RL-3 refitted 400.2, the validation error split at the tray share
  400.5. The golden sits 23.9 packs from the nearer edge (375).
- **The error's window** (FIN-RS-04 3.3, every finished lot): leaving out any one lot gives 387.4 to 414.9, the lots
  before and from Zelvora's tray key change 398.9 and 398.8, the odd and even lots 392.6 and 405.2, all 400.
- **Separation:** every rival a bin or more from the golden (asserted); the default two bins (100 packs) away; the
  nearest, Rx at 350, has no construction behind it. Single figure: no candidate positions or dominance. The decisive
  move is the largest on the graded figure (514 to 398.9); R1's check moves the default by 3 packs, R0b and R0c by under
  14, and none leaves the 500 bin.
- **Grid:** every construction without the error's tray structure files 500 (R0, R0b, R0c, R1: independent cells, or
  the predictions' structure) or 200 (Rover: one shared error); every construction with it files 400 (above); every
  history construction (R2, R2b, R2c) files 150 to 250.
- **Worth on the graded figure:** the decisive step moves the call from 500 to 400; no lower rung moves it at all.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every Model K pack built from the lot by the release day, the genealogy's 7,200 | FIN-RS-04 2.2, the prompt; C1 (Model J apart) |
| 2 Unit of account | the pack | FIN-RS-04 3.2 sums packs' probabilities; the prompt counts packs |
| 3 Attribution window | a pack's first 600 cycles | FIN-RS-04 3.2; C1 at 599.5 and 600.5 cycles (SF2, SF3) |
| 4 As-of dating | the lab pull of 12 October 2026: the release test finished, the twenty finished lots' life tests | the extracts note; nothing later ships |
| 5 Version basis | RL-3 rev. 4 of 30 September 2026 | QM-07; the refit converges (SF8) |
| 6 Denominator | the 7,200 packs for the expected share | FIN-RS-04 2.2; C1 |
| 7 Weighting | each EOL cell once in the error split, trays by the analysis of variance | C3: restricted maximum likelihood and pooled trays converge (396.0, 397.4) |
| 8 Window length | every finished lot's life tests | FIN-RS-04 3.3; C3 over leave-one-lot-out, halves at the tray key change and odd and even lots (387.4 to 414.9) |
| 9 Boundary inclusivity | below 80 per cent, within 600 cycles | C1 (SF2, SF3) |
| 10 Rounding path | the expected number once to the nearest 50 | FIN-RS-04 3.4; 23.9 packs from the nearer edge |
| 11 Tie-break | none: no ranking | n.a., asserted no candidate set |
| 12 Maturity and censoring | 27 life tests stopped first are censored | QM-07 leaves them out; read as lives the call stays at 400 (403.7, R2) |
| 13 Order of operations | predict, integrate over the shared error, sum over packs, round last | FIN-RS-04 3.2 and 3.4; C4 n.a. |
| 14 Row order | a continued test stitched in time order | C1: Bielefeld time read as UTC changes no order (asserted) |
| 15 Duplicate resolution | fleet B's repeated rows once | C1: cycles picked by number give the same features (399.0, asserted) |
| 16 Identity normalisation | three serial forms to the supplier's | the lab's extracts note; every join complete (asserted) |
| 17 Netting against gross | none | n.a. |
| 18 Dimensional units | mAh, milliohm, QP-3 cycles; F1 a natural logarithm | QM-07 sections 3 and 4 (SF10) |
| 19 Code and status semantics | EOL and STOPPED; the tray key's two formats | the lab's extracts note; never the stump |
| 20 Integerisation | cycles whole, the line at 600 inside a continuous model | C1 (SF3) |
| 21 Clause scope | FIN-RS-04 3.2 per pack, 2.2 every built pack | the policy's own clauses |
| 22 Forward window contents | the packs' first 600 cycles, ahead of release | the release test and the finished lots' life tests ship; FIN-RS-04 3.3 |

## Literal reader

Executed word for word, the prompt, FIN-RS-04 2.2 and 3.2 to 3.4, QM-07 and the pack specification give the expected
number of the 7,200 packs whose weakest cell falls below 3,856 mAh within 600 QP-3 cycles, cell lives as RL-3
predicts them with the model's error on the finished lots' life tests, to the nearest 50. The text is silent on how a
pack's three cell errors combine; the readings are independence (514, 500), the error's structure as the finished
lots' trays show it (398.9, 400) and one shared error (175.6, 200). The shipped life tests contradict the first and the
last (78 per cent of the error is shared within a tray and 22 per cent is each cell's own) while every pack is three
tray-mates or nearly, so the data's structure forces the method (`determinism-check` section 1, the design). Every term
and convention converges or is ruled out by a quoted sentence (SF1 to SF16, all asserted in `checks.py`); the easy
answer comes from an easy method on the same literal estimand, never from another reading.

## Oracles

- QM-07 Table 1 (each lot's mean error and error): the model's marginal accuracy; it ties on every route and scores no
  pack.
- QM-07 section 6 (the release criterion): ZC2638 passes it on every route; it says nothing of packs.
- The finished lots' observed tray-mate packs (R2, 150): lower than both the default and the golden, so it confirms
  neither; the lot under release is weaker than 18 of the 20.
- Zelvora's certificate of analysis: conforms on every route.
- The service records: the asks only; the call opens none (asserted).
- None ties only under the golden.

## Ask sheet

**Main call's declared row population:** the two cycler exports, the release register, the life monitoring results,
Zelvora's cell data package and the Model K genealogy, with QM-07, FIN-RS-04, the pack specification and the lab's
extracts note. Device and hazard rows in it: 0 (asserted: the call opens no service or costing file, and computed with
every ask file removed it is the golden; the asks computed with every main-call file removed are the asks). Both asks
read the service case system, the DACH depot's SAP export, the returns depot log, the carrier statement, the four
partners' invoices, treasury's rates, the cost sheet and the service extracts note, outside the call's population.
Neither is keyed to the call, its construction or its figures; they share no primary device.

**Ask A. For each of the four repair partners, the capacity replacements under the warranty carried out from October
2025 to September 2026 and what one cost on average, to the nearest euro** (8 figures): Dauvergne Réparation 99 at 99,
Tolley Marsh Repair 81 at 102, Ljungqvist Service 58 at 112, Ferrucci Assistenza 79 at 96 (unrounded 99.086,
101.892, 111.732, 95.933). With a battery that never travelled dropped from the average, or given its partner's mean
freight, the four read 99.086 and 99.086, 102.054 and 102.046, 112.225 and 112.260, 96.070 and 96.066: every reading on
the golden euro, each 0.23 or more from an edge (asserted).
- H18 home: the cost of one replacement where the lot's packs will be serviced, which values the reserve (FIN-RS-04
  3.4: Service Operations controlling values it); a measure the reserve carries that the count does not turn on. Use:
  the reserve's valuation in the release record, in the controller's words ("what one cost us").
- Construction: each partner case coded CAP, WTY and REPLACED, dated by the service period of the invoice line that
  bills it (the reissue in place of the invoice it replaces), in the twelve months; its invoice line in euros at
  treasury's month-end rate for that period, its battery's share of its consignment's carrier charge (the consignment
  from the returns log, the charge and pieces from the carrier statement; none for a battery that never reached
  Bielefeld), and the service pack at the standard cost valid when it was fitted. Golden equals the field's own events
  exactly (asserted).
- Primary device (D6, an event's quantity on every line it covers): the returns depot's log writes its consignment's
  carrier charge on every battery row (the delivery note's freight), while the carrier statement bills each consignment
  once with its pieces; no key repeats, no row is a duplicate, and the column reads as the battery's freight.
- Second device (D8, a settlement date for the event date): the case system closes a partner's case when the warranty
  desk approves the invoice that bills it, 8 to 45 days after the service period ends (median 17); the repair month
  appears only as the invoice's service period, a header field, and no line carries a date. Closing days move both window edges (September
  2025 repairs in, September 2026 repairs out), the rate's month and the pack's cost version.
- Hazards: HA1 (D2) Tolley Marsh Repair's March 2026 invoice and its reissue in one workbook, the first with last
  year's handling fee and one job billed twice; HA2 (D3) GBP and SEK lines at treasury's month-end rate for the service
  period; HA3 (D2) the service pack's standard cost lowered from 1 January 2026; HA4 (D5) goodwill replacements after
  600 cycles and no-fault-found diagnoses on the same invoices, a goodwill case's gauge count above 600 against every
  warranty case's at or below it (the service extracts note says the gauge counts the cycle in which it learns a
  capacity fault); HA5 (D4) a battery scrapped where it was removed (swollen, or failing the transport check) is not
  shipped, has no row and carries no freight, its repair standing as any other (filed in the service extracts note, 7
  of 317 partner lines).
- Stops (computed and asserted): S1 freight on every row: 99 at 153, 81 at 159, 58 at 156, 79 at 149; S2 closing
  days: 87 at 100, 69 at 103, 51 at 113, 69 at 97; S3 both (the cracker): 87 at 149, 69 at 156, 51 at 154, 69 at 147;
  S4 no freight: 95, 96, 102, 91; S5 goodwill kept: 279, 225, 158 and 223 replacements. HA1, HA2, HA3 and HA5 alone
  stay inside the euro (Tolley Marsh 102.01 with both invoices, 101.99 at the invoice date's rate; the current pack
  cost throughout 98.77, 101.60, 111.33, 95.77; the never-shipped readings above): texture.
- Span: the case system, the four invoice workbooks, the returns log, the carrier statement, treasury's rates, the cost
  sheet and the service extracts note (10 files); case_no, region, partner, fault_code, warranty, action, closed_utc;
  the invoice number, the invoice it replaces, the period, the currency, the line's case, labour and handling;
  Reference, Consignment, Freight EUR; consignment, pieces, charge_eur; month_end, currency, units_per_eur; Part, Valid
  from, Valid to, Standard cost EUR.
- Realism: a returns depot's goods-receipt log repeats the delivery note's freight on each line it receives, and a
  warranty desk closes a partner's claims when it approves the partner's monthly invoice.

**Ask B. The capacity replacements under the warranty carried out in each month from October 2025 to September 2026,
all five service regions** (12 figures): 8, 17, 23, 25, 26, 39, 41, 51, 57, 56, 74, 71 (488 in all; every month's count
differs from every other's).
- H18 home: the trail of the warranty reserves the call adds to (FIN-RS-04 3.5 charges each lot's warranty
  replacements against its reserve and trues it up each quarter): what the reserves carried, month by month. Use: the
  note's chart, in the controller's words ("carried out in each of those twelve months").
- Construction: the DACH depot's orders by SAP's Techn. Abschluss to 1 March 2026 and its cases by their closing day
  after (an order completed in SAP and carried into the case system counted once), the partners' cases by their
  invoice's service period.
- Primary device (D8): as Ask A's second device, here the whole figure: every month gains the previous months' partner
  repairs approved in it and loses its own, and September 2026's repairs are still open at the extract.
- Hazards: HB1 (D1) DACH orders created from 1 September 2025 carried into the case system with their SAP number in
  legacy_ref; HB2 (D5) goodwill replacements on the same cases; HB3 (D8) the extract's cut on 30 September.
- Stops (computed and asserted): the cracker's closing months 12, 7, 17, 31, 16, 46, 31, 39, 61, 52, 53, 83 (every
  month off by 4 or more); the carried-over orders twice 11, 21, 29, 37, 35 from October to February, then the golden;
  goodwill kept 21, 30, 34, 56, 57, 76, 82, 111, 113, 140, 168, 168.
- Span: the case system, the SAP export, the four invoice workbooks and the service extracts note (7 files).
- Realism: as Ask A.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 the March invoice and its reissue | Tolley Marsh's queried invoice | Ask A, Tolley Marsh | 0.12 euro, inside the euro |
| HA2 GBP and SEK at another month's rate | treasury's month-end table | Ask A, Tolley Marsh and Ljungqvist | 0.10 and 0.05 euro |
| HA3 the pack's standard cost from 1 January 2026 | the cost sheet's two rows | Ask A, every partner | 0.16 to 0.40 euro |
| HA4, HB2 goodwill and diagnoses beside warranty replacements | the partners' invoices, the case codes | Ask A counts, Ask B every month | +180, +144, +100, +144; +11 to +97 a month |
| HB1 carried-over depot orders | the depot's move from SAP | Ask B, October to February | +3 to +12 a month |
| HA5, HB3 batteries scrapped where removed, repairs open at the cut | the partners' transport check, the extract | Ask A freight, Ask B September | 0.00 to 0.53 euro, inside the euro; part of the closing-month shift |

**Referee.** The invoice's service period arbitrates the repair month and the carrier statement the freight; each is
a source the golden reads, neither a control that ties only under the golden. No filed sentence says when a partner
case closes or that the log's freight is the consignment's (asserted for the first).

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A replacements (4) | partner cases CAP, WTY, REPLACED closed in the twelve months | 87, 69, 51, 69 against 99, 81, 58, 79 | miss |
| A average cost (4) | the invoice line at the closing month's rate, the log's freight on the battery's row, the pack at the closing day's cost | 149, 156, 154, 147 against 99, 102, 112, 96 | miss |
| B the twelve months (12) | the depot's orders and cases by repair day (carried-over orders once), the partners' cases by closing month | 12, 7, 17, 31, 16, 46, 31, 39, 61, 52, 53, 83 against the golden | miss |
| the chart | the cracker's month counts drawn as the golden draws them | its bars carry Ask B's miss | outside |

Mirror leakage: 12 per cent of the ask weight. The mirror (R0, 500 packs) runs the same ask paths as the cracker, so it
misses every Ask A and Ask B figure the cracker misses and keeps only the chart's form (one bar a month, the regions,
the totals).
Pair ceiling: 36 (the cracker about 50 with the call, its components, the instructions and the chart's form; the
mirror about 22 with the instructions, the chart's form and part of the components).

## Gate record (stage 3)

- **Generator.** `task143/generator/build.py`: world (the lots, the finished lots' trays and lives, the lot under
  release cell by cell), field (packs, notebooks, battery events, the depot's move from SAP, returns, invoices and their
  approval), records, docs, calc (the golden and every rung and stop from the pack alone), deliver, metadata, checks
  (139 assertions: input gates, R1 to R3c on the pack and the clean truth, every rung's bin, nine constructions of the
  golden, the error's window, SF1 to SF16, mess neutrality, both asks with every stop and the cracker's path, the
  separation line, the distractors, the realism sweep, the golden files) and verify (pandas readers, RL-3 refitted, a
  mixed model by restricted maximum likelihood on the trays, Gauss-Hermite quadrature over the shared error, the asks
  by joins; 6 of 6 figures). Two consecutive builds byte-identical; `target.zip` cut from the final rebuild.
- **Pack.** 23 files in four formats (csv, pdf, txt, xlsx); fleet A's export 174,006 rows, fleet B's 130,698;
  distractors the Model J genealogy and Zelvora's certificate of analysis (`metadata.json`), each deleted with the
  call, the asks and every rung unchanged (asserted).
- **Golden.** 400 packs (398.9); a pack's chance 5.5 per cent; RL-3's error 0.160 at the tray and 0.086 the cell's own,
  78 per cent at the tray; 7,063 packs three tray-mates. Partners: Dauvergne Réparation 99 at 99 euros, Tolley Marsh
  Repair 81 at 102, Ljungqvist Service 58 at 112, Ferrucci Assistenza 79 at 96. Months: 8, 17, 23, 25, 26, 39, 41,
  51, 57, 56, 74, 71 (488).
- **Free gates.** `precut.py` 49 checks, 0 FAIL, 0 WARN; `voice-check.py` PASS (924 characters); `figures_check.py`
  58 figures, 0 absent; container audit clean on `target/` and `golden/`; `guard.py validate` clean, `surface` 0
  promoted (personas Christiana Harloff and Frieder Henschel, both on the card), `heart` WARN (strategy risk,
  repeat.gate_g, repeat.question_form, answered under Guard; nearest driver task261 at 0.09), rechecked after the
  rebase onto task144's draw with the context artifact re-keyed.
- **golden-realism and house fixes.** Finding titles on the workbook and the note; the note's identifying block, one
  true footnote from FIN-RS-04 2.2 and 3.3, precision by quantity; the chart titled with its finding, regions in a set
  palette, totals labelled, a source line. H4 23 archive members, no folder; H8 every citation resolves (FIN-RS-04 2.2
  and 3.2 to 3.4, the specification's section 4, QM-07 sections 2, 3 and 5, TM-2603-R1); H11 one prompt and one
  write-up; H14 the error's window asserted; H16 every extract's latest date on or before its pull; H21 the partners
  re-coined; H23 "if any" in the cost ask; H24 nothing under `target/` says the world is built.
- **`leak.py --asof 2026-10-12`: REVIEW, no LEAK.** Each line, harmless:
  - "the model" in the lab's extracts note, FIN-RS-04 and QM-07: the fiction's own nouns, the Model K pack and the
    release model RL-3.
  - "golden figure 2.4" in FIN-RS-04: the clause number 2.4 (Release), not the cell chance.
  - three or four of the call's five distinctive words in the lab's extracts note, FIN-RS-04 and QM-07: the lot, its
    packs and its release are those documents' subject; none states a reserve or a pack's chance (R3c asserted).
  - stump-paragraph terms (cycles, release, finished, system, effect, weakest, validation) in the four documents: the
    protocol's and the policy's vocabulary ("effective" on FIN-RS-04's revision line, the weakest-cell rule the default
    path also executes); no document names a shared error, a tray effect or a joint chance (R1 asserted).
  - the service extracts note and the cost sheet name the partners beside numbers: country codes, vendor codes and
    contract rates (labour, handling, diagnosis), one part of an invoice line; neither states an average cost or ranks
    the partners.
- **Stage 4.** The leak reader came back clean (no announcing sentence, no ranking file, no answer figure, the decisive
  step analytical, every REVIEW line harmless); its solver's-eye read is appended to `leak_check_report.md`. The
  determinism judge returned DETERMINISTIC, FIX_NOW of low severity (`determinism_check_report.md`): the reserve, the
  partner counts, the twelve months and the FX, cost-date and invoice bases all reproduced; two readings were open.
  Repair, in one generator pass with the call, the stump and every graded figure frozen: (1) Ljungqvist's average read
  112 with no freight for a battery that never travelled and 113 with the line dropped or the mean freight filled; the
  service extracts note now files that such a battery is not shipped, has no row and no freight and its repair
  stands, the share of batteries scrapped where they were removed went from 5.5 to 2 per cent (7 of 317 partner
  lines), and Tolley Marsh's and Ljungqvist's labour rates moved (GBP 33.75, SEK 505.50) so every reading of every
  partner rounds to the golden euro (asserted); (2) goodwill case KS26-015372 sat at a gauge count of 600: the gauge
  now counts the cycle in which it learns a capacity fault (filed), every warranty case sits at or below 600 and every
  goodwill or paid one above (asserted), and the case reads 601; (3) the extract notes renamed
  `extract_note_battery_lab_2026-10-12.txt` and `extract_note_service_operations_2026-10-09.txt`. After it:
  `build.py` 143 assertions, verify 6 of 6, two builds byte-identical, `target.zip` sha256 78dc1ed8...; `freeze.py
  check --mode determinism` passes with six cost parts allowed (`ask_a_parts`, the freight and invoice-line averages
  the repair moved; no graded figure moved).
- **Re-judge (stage 4, round 2): DETERMINISTIC, APPROVE** (`determinism_check_report.md`; the FIX_NOW report stays in
  git history). Every graded figure reproduced. Findings recorded: (1) a thin margin, clean: only a maximum-likelihood
  fit with lot as a fixed effect gives a tray standard deviation of 0.156 (about 367 packs, 350), a biased variance
  estimator; restricted maximum likelihood, the analysis of variance and the method of moments give 0.160 (400), and
  350 needs 0.1555 or less, 450 more than 0.1645; (2) a residual fork on the partner's job date, the invoice's service
  period against the case's closed_utc: this is the designed device (Ask A's second, Ask B's primary), settled by the
  invoice workbooks ("a line per job in the invoice's service period") and the cost sheet, which both key on the
  service period. The targeted re-read: clean on Q1, Q2 and Q4, Q6 analytical; its one finding, a realism tell in the
  two sentences the repair added to the service extracts note (they read as instructions to the analyst), was reworded
  in the system owner's field-note voice with the same content ("Battery scrapped where removed (swollen, or failed
  the transport check): not shipped, no returns-log row, no carrier charge; case and invoice line unaffected." and
  "cycle_count: gauge cycle count when the fault was logged, the fault's own cycle included."). No data or figure
  moved: `build.py` 143 assertions, verify 6 of 6, two builds byte-identical, freeze PASS, figures_check 58/0, precut
  49/0/0, voice-check PASS, leak.py REVIEW with no LEAK, guard surface 0 promoted and heart WARN, container clean;
  `target.zip` sha256 f51980cb99be1f9d8173729dc96bc8fceed56f864148a1bd706f601b722cc939.

## Pre-ship check

- **Rule 1, the domain, on the built pack.** The reserve is decided by the posterior predictive of a pack's weakest
  cell under the between-tray share of RL-3's error, estimated from the life monitoring results of the twenty finished
  lots (2,373 cells cycled to 80 per cent) joined to the release register's formation trays, and carried to the 7,200
  packs through the genealogy and Zelvora's tray map; no shipped column holds a tray effect, a correlation, a pack
  chance or a reserve (asserted). With another field's nouns the series pack, the formation tray and the 100-cycle
  release test lose the structure that makes the joint chance differ from the compounded one.
- **Rule 2, two layers.** Layer 1 on the call's path is the lab's own mess, each item neutral (asserted): two cycler
  layouts with cycle 0 against cycle 1 and Bielefeld time against UTC, fleet B's overlapping pulls, continued tests,
  three serial forms, the tray key's format change at ZC2532, life tests stopped late in life, part-tray packs. Layer 2
  is the error's tray structure carried into a weakest-cell pack, which no cleaning step touches: on the generator's
  clean truth the easy route files 514 and the decisive step alone 394 (R3a, R3b).
- **Rule 3, the decisive step.** No filed sentence names a shared error, a tray effect, a correlation or a joint
  chance (asserted on every shipped document); FIN-RS-04 files the estimand (packs, the 80 per cent line, 600 cycles,
  RL-3, the model's error on the finished lots) and the specification the weakest-cell rule, both executed by the
  default path as well. Nothing planted, copied or withheld carries the answer (R3c); the distractors (the Model J
  genealogy, Zelvora's certificate of analysis) rank nothing.
- **Determinism.** Every construction with the error's tray structure files 400 (395.2 to 400.5), every leave-one-lot
  estimate and both halves at the tray key change too; the asks' devices each have one handling that reproduces the
  field's own events exactly (asserted), the never-shipped battery and the 600-cycle line are filed, and the cracker's
  path misses all 20 ask figures.

## Tried and rejected

- The seed's own title mechanism was not read beyond its header; the world, decision and quantity are kept.
- Pattern D on the card (two grains, cell and pack): the signature is spent in fourteen builds (guard BLOCK
  `test.same_puzzle_older`, `test.same_driver_older`); the decisive step is not a second grain but a shared draw.
- A decisive G2 (the pack as the independent unit): BLOCK `ban.pattern` against task142, whose G2 is a period total's
  independent unit; the step here is a tray's error shared across a pack's cells.
- A decisive G10 (cross-dimensional duplication): it fits a list counted twice, not a shared error, and at stage 3
  `guard.py surface` promoted task98 on gap, pattern and decision family; re-keyed G17 (G16 is banned against task260).
- The early-life model's error carried in at all (plug-in against predictive) as the decisive step: every test cell's
  point prediction clears 600 cycles, so the plug-in reserve is nil, but a strong analyst adds the stated validation
  error by reflex, so it is a lower rung (R-1), never the stump.
- The lower tail of the error's distribution (a smallest-extreme-value tail against the normal) as the decisive step:
  a residual plot or a bootstrap of residuals reaches it in one move and every iid construction would then file the
  golden; dropped at the draw.
- A two-dimensional warranty (600 cycles or 36 months) with owners' usage rates as the decisive step: the obvious
  correction (the share of owners reaching 600 cycles in 36 months) lands within a bin of the golden; dropped at the
  draw.
- The new lot's own error offset (validation by held-out lot) as the decisive step: the between-lot variance rests on
  twenty lots, a small count, and moves the reserve both ways; the data is built with no lot effect and the
  convergence asserted.
- The earlier lots' field experience as an ask (each of twelve lots' capacity replacements and their share of the
  packs shipped): young and long-lived lots carry 3 to 14 replacements, so no device moved every lot's figure on the
  strongest solver's path (8 of 12 counts unmoved); replaced by the partners' cost and the monthly replacements, where
  money and months move on every row. The shipments file and the pack register went with it.
- The depot's orders carried into the case system as a primary device (D1, keyed by legacy_ref): a key the hygiene
  battery dedupes (migration duplicates are removed by both top responses on the record); kept as hazard HB1.
- Partner cases closed a few days after the repair (a continuous approval lag): three of the twelve months tied the
  golden under closing months. Closing at the invoice's approval moves every month; the invoice-date stream is the one
  of sixteen tried whose closing months miss every month by 4 or more.
- Per-lot stratified tray effects for the finished lots: the refit moved RL-3's slope and the golden to about 500, and
  the pooled and within-lot splits fell a bin apart; the random deal of one stratified sample kept.
- Zelvora's tray key change at lot ZC2602: its four later lots alone gave 317, a regime a careful reader might split
  the error on; the change moved to ZC2532, where the lots before and after give 398.9 and 398.8, and FIN-RS-04 3.3
  files the model's error on every finished lot.
- Life tests stopped first at any cycle (a channel fault at cycle 180): read as lives they moved the call to 650. A
  stopped test now ends late in life (a warm cell's alarm, a late fault); read as lives the call stays at 400 (403.7).
- Partner names Servitec, Hallam Repair, Nordfix and Reparo Sud: two match real companies and one sits inside a real
  university's name; renamed Dauvergne Réparation, Tolley Marsh Repair, Ljungqvist Service and Ferrucci Assistenza,
  with their own vendor codes (DVG, TMR, LJQ, FRC).
- Ask A's averages to the cent: a per-line rounding path moves a cent; rounded to the nearest euro, each average set
  within 0.05 of a whole euro by the partners' contract rates.
- File names `qp3_life_test_results.csv` and `release_test_register.csv`: `leak.py` reads `test_` as author
  vocabulary; renamed `qp3_life_monitoring_results.csv` and `qp3_release_register.csv` (the lab's own words).
- The context artifact keyed `filed_model` (QM-07): after the stage 3 rebase task455's re-registration put task141's
  filed model in this build's last three and `heart` BLOCKed on `ban.artifact`; re-keyed `monitoring_export`, the life
  monitoring results, with QM-07 read as a governing document.
- Batteries that never reached the returns depot at 5.5 per cent of removals, unexplained (judge FIX_NOW, low): 18 of
  317 partner lines had no row, and Ljungqvist's average read 112 with no freight but 113 with the line dropped or the
  mean freight filled. The service extracts note now files the battery scrapped where it was removed (no row, no
  freight, the repair stands), the share is 2 per cent, and two labour rates moved so every reading rounds to the
  golden euro; the cost parts in figures.json moved with them (`freeze.py --allow` ask_a_parts.DVG.freight_eur,
  ask_a_parts.TMR.freight_eur, ask_a_parts.TMR.invoice_eur, ask_a_parts.LJQ.freight_eur, ask_a_parts.LJQ.invoice_eur,
  ask_a_parts.FRC.freight_eur; no graded figure moved).
- A goodwill capacity case at a gauge count of exactly 600 (KS26-015372, judge): read against "within 600 cycles" it
  could join the warranty count. The gauge now counts the cycle in which it learns a capacity fault, which the service
  extracts note files; the case reads 601, and no warranty case sits above 600 or goodwill case at or below it.
- Extract notes named `README_battery_extracts.txt` and `README_service_extracts.txt`: the judge read the name as a
  build artifact; renamed for the system that wrote each.
