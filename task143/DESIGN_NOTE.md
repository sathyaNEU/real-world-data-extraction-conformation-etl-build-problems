# task143: Kalvenhorst Systeme, the warranty reserve for cell lot Z2638's Model K packs (architecture 1)

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
| Shape | `single-figure` (one committed count) with three ask tables and a chart supplying the criteria: the call and its components (about 4), the replacement counts and shares of twelve earlier lots (24), the cost of a replacement in five service regions (5), the chart's named parts (4) and the two files, about 39 criteria, arithmetic under `## Ask sheet` at stage 2 |
| Decision | `quantity_figure`, answer unit `count` (packs, to the nearest 50) |
| Mechanism | gap population (decisive: the reserve's unit is a pack of three tray-mates, whose shared share of the model error is one draw, not three) then time (the earlier lots' pack rate belongs to stronger lots than the one under release); pattern none, generators G10 (one tray draw of the error counted as three independent cell draws), G2 (the pack as the unit), G17 (the model's error carried into the predictive at all), G6 (the lot under release predicts shorter lives than the history); Gate G `forecasting`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `estimation_fit` (clustered errors in a joint prediction); `general-statistics-data-science/bayesian-modeling-posterior-inference/2` (predict with the posterior predictive, observation noise and between-group variance, for new units in new groups): this build's version asks for the predictive of a new group's members jointly, because the reserve pays on the weakest of them |
| Furniture | forum `other` (product finance books the reserve under its release reserve policy, no meeting), forcing event `other` (the lot's release for shipment on Friday 16 October 2026, when the reserve is booked), organisation family `manufacturer` (Kalvenhorst Systeme GmbH, a business-notebook maker with its own battery plant and reliability lab), role family `finance_controller` (the notebook division's product finance controller), context artifact `filed_model` (the qualification memo QM-07 files the release model of record, its two features and its validation error, no reserve), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `qualification_cycles_first100_*.csv`, the reliability lab's cycler exports of the first 100 cycles of every qualification cell (two cycler fleets in two layouts), one row per cell per cycle for the twenty lots whose life tests have finished and the lot under release; constructed |
| Deliverables | `z2638_warranty_reserve.xlsx` (the reserve and the two ask tables), `z2638_reserve_note.docx` (a one-page note to finance opening with the reserve, with the chart of the earlier lots' replacement shares) |
| People | drawn with `guard.py names --geo "Germany" --seed 143` and `--seed 1431`, every name the guard clears: Christiana Harloff (product finance controller, notebook division, the requester and owner of the reserve policy), Frieder Henschel (head of the battery reliability lab, author of QM-07), Dietmar Schaaf (manufacturing engineering, battery plant, the pack genealogy), Annelie Geisel (service operations analyst, the service case system); none appears in the prompt |

**Guard.** `guard.py check` on the registered card: WARN, no BLOCK. Answered: `three_rules.strategy_risk`
(grain_or_unit): the analyst test below reads every field and rule correctly and still files the wrong reserve,
because no field or rule says a pack's cells share their error; `repeat.gate_g` (forecasting beside task142): Gate G
names where the stump sits, a projection for packs whose cells were never tested, and task142's forecasting gate carries
a percentile of a period total; `repeat.question_form` (how-many beside task142): the call is a count of packs, and a
count asks how many. A first card carried pattern D (two grains, spent in fourteen builds: `test.same_puzzle_older` and
`test.same_driver_older` BLOCK) and then a decisive G2 (BLOCK `ban.pattern` against task142, whose G2 is the independent
unit of a period total); the decisive step is that a formation tray's share of the model error is one draw which the
three cells of a pack share, the house's G10 (task131 v1 carries it for sibling sub-units sharing a parent), and the
card carries G10 with one differentiation line for task98 v7 (two removal lists that list some members twice).

**Same-puzzle and same-driver tests.** Gap population, decisive G10, decision `quantity_figure`, Gate G `forecasting`:
no build in the last twelve carries gap and G10 with either; task98 v7 (older) carries all three and is differentiated
on the card (a member duplicated across two dated lists, nothing of a shared error or a weakest member). task131 v1
(lineage, G10 with method selection) is a randomised sub-unit whose lift carries outcomes moved from its siblings: an
interference effect on an experiment, not a joint prediction.

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
cells then stay on QP-3 until they reach 80 per cent (the life monitoring program), so every lot since Z2441 whose cells
have all finished has whole trays followed to the end. Product finance's release reserve policy (FIN-RS-04) books, on
the day a lot is released, a warranty reserve for the lot's Model K packs equal to the expected number that will fall
below 80 per cent of rated capacity within 600 cycles, cell lives taken on QP-3 as RL-3 predicts them. Lot Z2638 was
formed from 14 to 19 September 2026; its 7,200 Model K packs were built from 28 September to 9 October and are held in
the bonded store; its release test finished on 6 October; the lot is released on Friday 16 October 2026.

As-of dates (set at stage 2 with the generator): the lab exports, the supplier package and the pack genealogy pulled
on 12 October 2026; the service case export and the partners' invoices to 30 September 2026, pulled 5 October.

## Default path

1. Read FIN-RS-04 (the reserve is the expected number of the lot's Model K packs that fall below 80 per cent of rated
   capacity within 600 cycles, lives on QP-3 as the release model predicts them) and QM-07 (RL-3's two features, its
   coefficients and its validation error on held-out lots).
2. Stack the two cycler fleets' exports of the release test, compute each of the 120 cells' two features exactly as
   QM-07 defines them, and predict each cell's log life with RL-3.
3. Carry the model's validation error into the prediction: each cell's chance of reaching 80 per cent before 600 cycles
   is the normal tail of its predicted log life at QM-07's error, averaged over the 120 cells (about 2.6 per cent).
4. A pack falls below 80 per cent when its weakest cell does (the pack specification), so a pack's chance is one minus
   the chance that none of its three cells fails, 1 - (1 - 0.026)^3, about 7.6 per cent; times 7,200 packs.

Ends on: about 550 packs (stage 2 design target from the prototype; the generator's figures replace it).
Golden: about 400 packs: the release model's error splits into a formation-tray part (about 0.19 on the log scale)
and a within-tray part (about 0.05), seen in the earlier lots' whole trays cycled to 80 per cent; every Model K pack is
three tray-mates (the genealogy and the supplier's tray map), so a pack's chance is the expectation, over a new tray's
shared error, of the chance that any of its three cells fails, about 5.6 per cent (stage 2 design target from the
prototype; the generator's figures replace it).

## Stump sentence

A competent solver computes RL-3's features for lot Z2638's 120 release-test cells, predicts each cell's life with the
model's validation error, averages each cell's chance of reaching 80 per cent before 600 cycles (about 2.6 per cent)
and compounds it over a pack's three cells as if they were independent, filing about 550 packs (Ends on); the step that
lands it there is treating a pack's three cells as independent draws when they are tray-mates and the release model's
error is mostly a formation-tray effect they share: carried through the tray effect that the earlier lots' whole trays
show, a pack's chance is about 5.6 per cent and the reserve about 400 packs.

## Three rules

- **Task type:** `general-statistics-data-science`, `bayesian-modeling-posterior-inference` (serves Forecasting): the
  reserve is the posterior predictive, for members of new formation trays, of the chance that the weakest of a pack's
  three cells reaches 80 per cent of rated capacity before 600 cycles, under a hierarchical model of the release model's
  error with a between-tray variance.
- **Domain test:** the deciding quantity is the predictive chance that the weakest of three new cells from one new
  tray falls below the warranty line, which the task type gets by integrating the between-tray variance of the model
  error over the members a pack shares, estimated from the earlier lots' whole trays followed to the end; the generic
  summary of the model's accuracy (one pooled error, applied to each cell independently) files about 550 packs against
  about 400, so the call turns on the predictive for new groups, the task type's own object.
- **Swap:** in general statistics the setting is another field's, so the swap that matters is of the method: "the lot's
  reserve is about 400 packs because a pack's three cells share their tray's error" read with the posterior predictive
  replaced by the pooled cell-level error compounded independently ("each cell fails with 2.6 per cent, a pack with 7.6")
  files about 550; read with another field's nouns ("a hospital's three-drug regimens") the sentence loses the series
  pack that fails with its weakest cell, the formation tray whose effect appears only at the knee of life, and the
  release test whose 100 cycles cannot see it, so what makes the joint chance differ from the compounded one stops
  making sense.
- **Layer 1:** the release test's cycles come from two cycler fleets exporting different layouts (column names, date and
  number formats, the protocol's first cycle numbered 0 on one fleet and 1 on the other), cells split across them by
  channel availability; cycler exports pulled in overlapping windows, so some cycles arrive twice; cell serials in the
  supplier's form against the cyclers' and the pack plant's scanned forms; the supplier's cell data package changing its
  tray key format between lots; life tests stopped by a channel fault before a cell reached 80 per cent; packs completed
  from part trays when a tray lost a cell at incoming inspection; and, on the ask paths, the service case system, the
  repair depot's returns log, the partners' monthly invoices in their own currencies and layouts and the treasury rate
  table. Each is what these systems write; none decides the call (each mishandled leaves the call where it is, asserted
  at stage 3).
- **Layer 2:** `estimation_fit`: the shortcut treats the release model's validation error as each cell's own, so a
  pack's chance is the cell chance compounded over three independent cells; the expert reads the error's structure in
  the earlier lots' whole trays (most of it shared by tray-mates) and builds the pack's chance from the joint predictive
  of three cells of one new tray.
- **Decisive step:** decomposing the release model's error on the earlier lots' life tests into a between-tray and a
  within-tray component, and computing each pack's chance as the expectation over its tray's shared error of the chance
  that any of its three cells falls below 80 per cent before 600 cycles (the posterior predictive for members of a new
  group), with the pack's composition read from the genealogy and the supplier's tray map, instead of compounding one
  pooled cell chance over three independent cells.
- **Not semantics:** every field, code, unit and definition can be read correctly (the protocol's cycles, the features,
  the model, the warranty line, the weakest-cell rule, the genealogy, the tray map) and the default path reads them all
  correctly and still files about 550 packs; nothing in the pack names a correlation, a shared error or a tray effect,
  and the answer moves only on how the joint chance of a pack's three lives is estimated.
- **Not rule application:** FIN-RS-04 files the estimand (the lot's Model K packs as built, the 80 per cent line, the
  600-cycle window, lives on QP-3 as the release model predicts them) and QM-07 files the model and its error; no rule,
  procedure or document says how a pack's chance is built from its cells' predictions, and executing every filed rule
  with the default construction files about 550, so the step that moves it to about 400 is performed by no filed rule.
- **Analyst test:** a strong analyst who stacks both cycler exports, computes RL-3's features exactly as QM-07 defines
  them, predicts every release-test cell's life with the model's validation error and counts a pack as failing when its
  weakest cell does files about 550 packs (Ends on) by compounding the cell chance over three independent cells;
  checking the release test's own predictions for a tray effect finds none and files the same, the earlier lots' own pack
  rate files about 150, the whole pack treated as one cell about 200, and only the pack's joint chance under the
  between-tray share of the model error files about 400 (R3a and R3b asserted at stage 3).
- **Estimand:** FIN-RS-04's reserve clause (`fin_rs04_battery_warranty_reserve_policy.pdf`, set at stage 2): the
  expected number of the lot's Model K packs, every pack built from the lot whether shipped or not, whose full charge
  capacity will fall below 80 per cent of rated capacity within its first 600 cycles, cell lives taken on QP-3 as the
  release model of record predicts them; the population, outcome, window, unit and model of record are filed, the
  pack's joint chance is not.
- **No decoy:** nothing is planted to be caught: no copied block, no hidden rule, and no memo, draft, briefing or
  stakeholder figure states a reserve, a pack failure rate or a method; QM-07's validation error is the model's true
  error on held-out lots, stated as an accuracy figure and never as a reserve basis; the distractors (set at stage 2)
  rank nothing.
- **No certified replay:** no published reserve, certified pack failure rate or past booking ships to be reproduced;
  the tray structure of the error is estimated from the life tests on file, and no closed figure is matched to recover a
  method.
- **Lesson:** a system that fails with its weakest member, built from members that share a group's unobserved effect,
  fails less often than the members' marginal chance compounded independently, and when that effect lives in a
  predictor's error it shows only in outcomes of whole groups followed to the end, never in the inputs; no build on
  file teaches a series system's chance under a shared random effect (task229 v1 teaches the widened uncertainty of a
  mean over co-failing entities, task142 the spread of a total of multi-day units).

## Readability screen

Stage 2.

## Semantic fork table

Stage 2.

## Ladder

Stage 2.

## Closure table

Stage 2.

## Literal reader

Stage 2.

## Oracles

Stage 2.

## Ask sheet

Stage 2.

## Tried and rejected

- The seed's own title mechanism was not read beyond its header; the world, decision and quantity are kept.
- Pattern D on the card (two grains, cell and pack): the signature is spent in fourteen builds (guard BLOCK
  `test.same_puzzle_older`, `test.same_driver_older`); the decisive step is not a second grain but a shared draw, G10.
- A decisive G2 (the pack as the independent unit): BLOCK `ban.pattern` against task142, whose G2 is a period total's
  independent unit; the step here is a tray's error shared across a pack's cells, G10.
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
