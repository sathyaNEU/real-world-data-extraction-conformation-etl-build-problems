# task159: Kelvanna Lake's 2027 budget gold at the raised ore cut-off (architecture 2)

Private, never ships. Architecture 1 (the Vellmouth Transit Commission's spring 2027 platform conductor pick,
urban-regional-science / forecasting, shipped 2026-10-17, no portal result) was re-rooted on 2026-11-01 at the Batch 3
queue reset; its world is closed and its record is kept below under `## Architecture 1 record`. This architecture is
a new world, dataset and prompt shell in a new client domain. Stump power is argued on paper; no solver, scored reader
or probe ran.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task159.json`, architecture v2, registered 2026-11-02T02:21:49Z,
  re-checked on the registered card as the last act of the draw: WARN only (`repeat.question_form` how-much against
  task281, answered below; `test.same_puzzle_older` against task488 differentiated: task488 links new items to an
  established scale through standings computed from provisional levels; nothing here is linked to a scale).
- **Pairing:** General Statistics & Data Science / regression-classification-model-diagnostics, which serves
  Forecasting & Predictive Modeling. The deciding quantity is the calibration of a predictor where a decision threshold
  is applied: the gold grade control will find above 0.90 g/t in blocks known only through a resource model's
  estimates. Objective kept from the number's lane (Forecasting); the committed call is a figure for a window not yet
  open (calendar 2027).
- **World:** Aubreth Gold Corporation's Kessock Lake open pit and carbon-in-leach mill, northeastern Ontario (UTM 17N,
  CAD); invented company, mine and people (`guard.py names --geo Canada --locale en_CA --seed 159`: Cindy Smith, Jeffrey
  Russell, Charles Bailey, Emily Schmitt, Kerri Steele, Brent Peck, Heidi Nichols). No in-flight world is near it
  (task186 airport screening, task271 lake stocking, task133 log trucks, task142 load forecasting, task304 road
  junctions, task149 rail station, task138 QT study were read).
- **Decision:** the 2027 budget gold (contained ounces in the ore mined), the figure the general manager takes to the
  board on 8 December 2026, after the board raised the ore cut-off from 0.50 to 0.90 g/t.
- **Shape:** `other`, single main figure with one component plus three ask trails. Criteria: the call (1), the ore
  tonnes (1), the plan's model basis and the record's factors as components (2), the stockpile at four dates in tonnes
  and gold (8), ball mill hours by quarter (7), fine gold poured by quarter (7), the chart's parts (3) and the files
  (2): 31.
- **Strategy:** `classification_error` (ore and waste are classified at the face on a measurement that spreads more
  widely than the plan's estimate). Gap `objective` (the reports' factor is correct at 0.50 g/t and is not what the
  decision is scored on), generators G14, G2, G3, Gate G `forecasting` (the correctly read past does not pin the
  forward factor). `repeat.gate_g` against task149 answered: task149's forward quantity is trips per worker from a stay
  panel; here it is the factor a selection threshold carries.
- **Data-native sentence:** grade control selects ore at the face on blast-hole assays whose block grades vary more
  than a kriged model's smoothed estimates although the model is right on average at every estimate, so this mine's
  own reconciliation factor is a property of the cut-off it was measured at, and the four years of blast holes laid
  into the model's blocks are the only record of how grade control spreads about the model.
- **Abstraction sentence (written to test against every approved build):** "a selection made on a finer measurement
  than the forecast's estimate keeps more above a raised threshold than the estimate's own distribution shows, so a
  kept-to-estimated factor measured at the old threshold understates the new one." No approved build carries it:
  task141 and task169 move units into a state the record already holds (no state changes here; the routes reading the
  record's units in the forward state, the model-ore blocks' own grade-control grades, file the wrong 130,000);
  task162 replays a cap; task135 and task143 understate a variance of a sum; task304 (in flight) shrinks selected sites
  toward a model, the opposite correction (here the model is conditionally unbiased and the gain comes from the finer
  selection).
- **Candidates weighed (fates in `## Tried and rejected`):** twin-plant wrong-train slips under a single operator
  (human-reliability-assessment), HRA response times pre-empted by an automatic trip, mixed-population wind extremes
  (climate-weather-extremes), a noisy-model version of this world (regression to the mean at the raised cut-off), and
  this smoothed-model version, chosen.
- **Sources:** a constructed pack (seeded generator, `generator/build.py`, seed 15902); real conventions only:
  NAD83(CSRS) UTM zone 17N with a rotated local mine grid, the troy ounce, fire-assay laboratory reporting in parts per
  billion with gravimetric re-assay of over-range results, refinery melt lots and settlement statements, DCS historian
  exports in UTC.

## Survivor anatomy

- **Actor:** the deciding property is each scheduled block's expected grade-control gold above 0.90 g/t given its
  model estimate, and the record's factor at 0.90 g/t; no file holds a grade-control grade per block, a factor at
  0.90 g/t or any 2027 grade-control figure (asserted in `checks.py`, R1).
- **Link:** blast holes are logged in UTM by the rigs' GNSS and the model lives in the rotated Kessock mine grid; the
  pairing runs through the survey control's transformation and the bench, a link no key offers, and the comparison it
  enables (grade control re-cut at the new cut-off against the model re-cut at it) is one the reconciliation's own
  method never asks for.
- **Reflex:** the field's method for converting a plan to a mined-ore forecast, the reconciliation factor (F1) from
  the monthly reports applied to the plan's model ounces, sits at rung 1 and files 130,000; the model-diagnostic reflex
  (check the model is right on average and keep the plan) sits at rung 1b and files 130,000.
- **Back-test:** the textbook route validates: the reports' F1 at 0.50 g/t holds near 1.02 every year of the record and
  predicts each year's grade-control ore gold from the model at 0.50 g/t within a few per cent; the regression of
  grade control on the model is slope 1.008 (log slope 1.002), so the calibration check passes.
- **Second use:** the blast-hole export is the grade-control record every reconciliation is built on; the model and
  the plan are the planning record; the survey control is the site standard every survey file needs. Delete the
  decisive step and the pack still carries each of them.
- **Shock:** nothing moves in the record: the cut-off change is a filed board decision and the factor at 0.50 g/t is
  steady; the gain at 0.90 g/t is a property of the record no statistic of any one file shows as an anomaly.
- **Pins:** the WHAT is filed in the mine planning superintendent's budget basis memo (cut-off, ore selected block by
  block on grade control, budget gold contained in calendar 2027 on grade-control grades and model tonnages, the
  schedule's blocks ore and waste alike); no filed sentence names the threshold dependence, the re-cut or the
  per-block reading.

## Default path

1. Read the budget basis memo: ore at 0.90 g/t on grade control, budget gold contained in calendar 2027.
2. Sum the Schedule sheet of `kessock_mine_plan_2027_v3.xlsx` at AU_OK of 0.90 g/t or more: 2,719,560 t and
   127,655 oz on the resource model (the plan's Summary sheet shows the same on its basis line).
3. Open `monthly_reconciliation_jan2023_oct2026.pdf`, the record of how grade control and the mill compare with the
   model, and take the January 2023 to October 2026 gold factor F1 of 1.02 (steady by year: 1.01, 1.01, 1.03, 1.02).
4. Apply it to the plan's model gold, the field's method for a mined-ore forecast: 127,655 x 1.0191 = 130,093 oz.
5. (Rung 1b, the model-diagnostic check) pair the blast holes with the model and confirm the model is right on average
   (regression slope 1.008, ratio of means 1.004 over the blocks it calls ore), and keep the plan's 127,700.

Ends on: 130,000 oz (130,093 unrounded; the plan's 127,655 and the calibration route's 128,119 print the same).
Golden: 150,000 oz (149,863 unrounded under the per-block reading; ore 2.8 Mt).

## Stump sentence

A competent analyst applies the reconciliation reports' grade-control-to-model gold factor, 1.02, measured each month
on ore cut at 0.50 g/t, to the 2027 plan's 127,655 model ounces at 0.90 g/t and files 130,000 oz; the step that lands
there is treating the model's grade-tonnage curve as grade control's, when grade control's block grades spread more
widely than the model's and a 0.90 g/t cut on them keeps more gold, which only the blast holes laid into the model's
blocks and re-cut at 0.90 g/t on both sides show, putting the budget at 150,000 oz.

## Three rules

- **Task type:** regression-classification-model-diagnostics (General Statistics & Data Science), which serves
  Forecasting & Predictive Modeling: judging a predictor's calibration where its use applies a threshold.
- **Domain test:** the deciding quantity is the gold a selection on grade control keeps above 0.90 g/t in blocks known
  only through the resource model's estimates; the field's estimator for carrying a plan to mined ore is the
  observed-to-estimated ratio over the closed record (the mine's reconciliation factor, F1), and the field's
  diagnostic of the estimate is whether it is right on average.
- **Swap:** with another field's nouns ("a risk score" for "the block model", "claims paid" for "grade control"), the
  task survives only if the threshold is applied to a finer measurement than the predictor, the outcome is seen only
  for the units that measurement selected, and the record's factor was measured at another threshold; a plain
  forecast of a total, or a stated score, reads differently.
- **Layer 1:** blast-hole assays in parts per billion from the site laboratory against block grades in g/t (the
  laboratory's LIMS); collars in UTM from the rigs' GNSS against a model in the rotated mine grid (survey control
  sheet); the mid-2025 LIMS migration carrying legacy sample numbers, sample-type codes and date formats into one
  export; below-detection results as text and over-range results re-assayed by gravimetric finish in their own column
  (laboratory practice); field duplicates, certified reference materials and blanks in the sample stream (QA/QC
  insertion); the mill's production day running 06:00 to 06:00 (mill reporting); monthly reconciliation tables inside
  a PDF report; dispatch and DCS times in UTC against maintenance and production records in local time.
- **Layer 2:** `estimation_fit`: the estimate must fit the data's structure (a smoothed predictor against a finer
  selecting measurement); the methodological choice that flips the call is whether the record's factor is read at
  the cut-off it was measured at or re-measured where the decision applies the threshold.
- **Decisive step:** recognising that this record's grade-control-to-model gold factor depends on the cut-off because
  grade control's block grades are more dispersed than the smoothed estimates, and re-reading the paired record at
  0.90 g/t (as a re-cut ratio or block by block through the record's grade-control-to-model ratios).
- **Not semantics:** every field read correctly (ppb converted, the grid transformed, the reports' 0.50 g/t line read,
  the memo's ore definition read) still leaves the reports' factor, a correct measured property of the mine, applied
  to the plan's ounces at 130,000; nothing in any file has to be reinterpreted to move it, the gain comes from a
  recomputation the record supports and no column holds.
- **Not rule application:** no filed rule or procedure performs the re-cut or the per-block reading; executing every
  filed sentence leaves the analyst choosing how to carry model ounces to grade control. Enumerated family spread
  (plan raw 127,655; reports' F1 130,093; reports' F3 130,209; calibration route 128,119; per-block over the plan's
  ore blocks only 108,506; re-cut factor 152,883; binned conditional means 151,274 to 152,092; log-normal 149,875;
  empirical ratios 149,863): 108,506 to 152,883, five printed cells. Standing family (the routes the memo and the data
  leave defensible: the re-cut factor on all, the last 24 or the last 12 months of the record, the binned means at
  three widths, the log-normal and the empirical ratios): 149,653 to 153,609, one printed cell (150,000). The
  ruling-out is loud: the report's own heading says its factors are "for ore at the 0.50 g/t cut-off" and the memo
  says ore is selected on grade control at 0.90 g/t.
- **Analyst test:** a strong analyst who converts the assays from ppb, moves the collars onto the mine grid, drops the
  laboratory's control samples, reads the budget basis correctly and applies the reconciliation reports' gold factor
  (1.02, measured on ore cut at 0.50 g/t) to the plan's model ounces files 130,000 oz; one who first confirms the
  model is right on average and keeps the plan files the same cell.
- **Estimand:** filed in `budget_2027_basis_of_ore_and_gold.pdf`: "Budget gold is the gold contained in the ore mined
  in calendar 2027, in troy ounces, on grade-control grades and the resource model's block tonnages"; ore is "a block
  ... when its grade-control grade is 0.90 g/t or more", a block's grade-control grade "the average of the primary
  blast-hole assays from the holes collared in it"; the volume is "every Main Zone block the plan mines in 2027, ore
  and waste alike" (blocks not yet mined, known only through the model, are the population by construction).
- **No decoy:** nothing is planted: the reconciliation report answers its own question correctly (monthly factors at
  the operating cut-off), the plan reports its own basis, no memo, draft or stakeholder figure argues a budget number,
  and no block of data is copied or altered.
- **No certified replay:** the method is not recovered by reproducing certified figures; the reports' figures
  reproduce under the default and the golden alike, and the golden is an estimate the paired record supports.
- **Lesson:** a predictor that passes its calibration check can still misstate what a threshold applied to the
  outcome's own finer measurement will keep, so a factor measured where the threshold sat does not travel to a new
  threshold; no build on file teaches the selection-on-a-finer-measurement effect (support and information effect).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the plan's model ounces at 0.90 g/t | the plan's Summary prints it | AU_OK column | yes | no | no | yes | no | readable |
| R1 the reports' F1 at 0.50 g/t on the plan | the report prints 1.02 | no | yes (the field's method) | the report blesses it | no | yes | no | readable |
| R1b the model checked right on average, plan kept | no | no | yes (calibration check) | the slope of 1.008 blesses it | no | no | no | readable |
| R2 re-measure the record at 0.90 g/t, block by block or as a re-cut ratio (decisive) | no: the memo files the basis (grade control at 0.90 g/t), no sentence names a factor's dependence on the cut-off or the re-cut | no column holds a block's grade-control grade or a factor at 0.90 g/t | no: both reflexes file 130,000 | no: the reports and the calibration check both bless the reflex | no: the battery has no step that re-cuts a reconciliation | no: a recomputation over 21,616 paired blocks, not a reported figure | no: the blast-hole record ships for the reconciliation and grade control | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | budget gold | contained gold | recovered gold | another figure | memo: "the gold contained in the ore mined in calendar 2027" |
| SF2 | 2027 | calendar 2027 | a fiscal year | another volume | memo "calendar 2027"; the Schedule runs Jan-27 to Dec-27 |
| SF3 | ore | grade control at 0.90 g/t or more | the model at 0.90 g/t | 130,000 | memo: "A block is ore when its grade-control grade is 0.90 g/t or more" |
| SF4 | a block's grade-control grade | mean of primary blast-hole assays | field duplicates averaged in | same call | memo excludes duplicates; asserted same call |
| SF5 | below-detection results | half the limit | zero or the limit | same call | asserted same call |
| SF6 | over-range results | the gravimetric column | capped at 10 g/t | same call | asserted same call |
| SF7 | the budget's volume | every scheduled Main Zone block, ore and waste | the plan's ore blocks only | 110,000 | memo: "every Main Zone block the plan mines in 2027, ore and waste alike" |
| SF8 | tonnes | the model's block tonnages | the plan's TONNES column | same call (identical) | asserted identical |
| SF9 | the record's window | all four years | the last 24 or 12 months | same call | asserted same call |
| SF10 | the estimator inside the family | empirical ratios per block | log-normal, binned means, the re-cut factor | same call | asserted same call (149,653 to 153,609) |
| SF11 | ratio centring | centred so the model is right on average | uncentred | same call | asserted same call |
| SF12 | rounding | nearest 10,000 oz, once | a different path | same call | the figure sits 4,863 oz inside its cell |
| SF13 | ounce | troy ounce, 31.1034768 g | avoirdupois | another figure | prompt: "Gold is in troy ounces" |
| SF14 | grid transformation | the control sheet's parameters | a fit to the monuments | same call | asserted (monuments reproduced to 2 mm) |
| SF15 | the model's estimate | AU_OK | another estimate | same call | the export carries one estimate |
| SF16 | ore tonnes | tonnes of grade-control ore | the plan's model ore, or the reports' tonnage factor on it | 2.7 or 2.4 Mt | prompt "ore tonnes behind it" with SF3 |

## Ladder

| Rung | Construction | Unrounded | Prints | Note |
|---|---|---|---|---|
| R0 | the plan's model ounces at 0.90 g/t | 127,655 | 130,000 | the planning basis |
| R1 | R0 x the reports' F1 at 0.50 g/t (1.0191) | 130,093 | 130,000 | the default path; F3 (1.02) gives 130,209 |
| R1b | the model checked right on average, R0 kept | 128,119 | 130,000 | the calibration route |
| R1c | per-block reading over the plan's ore blocks only | 108,506 | 110,000 | half the step: grade control's ore gain from the schedule's waste left out |
| R2 | the record re-cut at 0.90 g/t (factor 1.1976) on R0 | 152,883 | 150,000 | decisive step, ratio form |
| G | each scheduled block through the record's ratios | 149,863 | 150,000 | golden; ore 2,778,429 t |

Bin test in units of the 10,000 oz cell: (a) the decisive step's worth, golden less default, 19,770 oz = 1.98 cells;
(b) the spread of the standing family, 149,653 to 153,609 = 0.40 cells; (c) the golden's sampling interval,
bootstrap SD 168 oz, about 0.03 cells at 95 per cent. (a) exceeds (b) + (c) by four times. Tonnes: the standing
family's ore tonnes run 2,778,429 to 2,817,999, inside the 2.75 to 2.85 Mt cell by 28,429 t at the nearest edge;
the reports' tonnage factor on the plan gives 2,368,373 (2.4 Mt) and the plan's own ore 2,719,560 (2.7 Mt). The re-cut
factor read off a single year spans 1.167 to 1.252 because each year's estimates sit differently about the cut-off;
the per-block reading is year-proof (149,701 to 150,239 by year).

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | every scheduled Main Zone block, ore and waste (memo, SF7); the record is every mined block with holes, C1 |
| 2 | Unit of account | the model block, the memo's selection unit (SF3, SF4) |
| 3 | Attribution window | calendar 2027 by the Schedule's months (SF2) |
| 4 | As-of dating | the record to 31 October 2026; the plan of 9 November 2026; nothing depends on a later state |
| 5 | Version basis | model 2026R, plan v3, LIMS export of 5 November 2026: one version each shipped |
| 6 | Denominator | none in the call; the factor's denominator is the model's gold at the same cut-off, C1 |
| 7 | Weighting | tonnage-weighted throughout (block tonnages), C1 |
| 8 | Window length | record window converges (SF9), C1 asserted |
| 9 | Boundary inclusivity | 0.90 g/t or more (memo); no block sits on 0.900 in a way that moves a cell, asserted via the margin |
| 10 | Rounding path | once, at the end, nearest 10,000 oz and 100,000 t (prompt) |
| 11 | Tie-break | none arises |
| 12 | Maturity and censoring | no censoring; every mined block is closed |
| 13 | Order of operations | average holes, then cut (memo), C1 |
| 14 | Row order | no step depends on file order, asserted by the verifier's independent path |
| 15 | Duplicate resolution | field duplicates and laboratory controls excluded (memo, SF4) |
| 16 | Identity normalisation | hole to block through the grid and the bench; the verifier fits the grid independently, C1 |
| 17 | Netting against gross | not applicable to the call |
| 18 | Dimensional units | ppb to g/t, troy ounces (SF13), C4 |
| 19 | Code and status semantics | sample-type codes across the LIMS migration (BH and BLASTHOLE), C1 |
| 20 | Integerisation | none |
| 21 | Clause scope | the cut-off applies from 1 January 2027 to every scheduled block (memo) |
| 22 | Forward window contents | the Schedule sheet is the shipped driver file for 2027 |

## Literal reader

Executed word for word: ore is a block whose grade-control grade (the average of its primary blast-hole assays) is
0.90 g/t or more; budget gold is the gold contained in the ore mined in calendar 2027 on grade-control grades and the
model's tonnages; the volume is the Schedule's blocks. No grade-control grade exists for a 2027 block, so the literal
reader must estimate grade control's gold above 0.90 g/t from the only record relating grade control to the model,
the paired blast holes; every estimator that does so lands 150,000. The reports' factor is, by the report's own line,
measured "for ore at the 0.50 g/t cut-off", a basis the memo's 0.90 g/t definition does not name, so the default is
an easier method on correct data inside the filed estimand, not another reading of it. The asks read literally too:
"at the end of 2023 ... at 31 October 2026" and "each calendar quarter ... all in local time" fix the dates and clock,
"the fine gold in the bars poured in each of those quarters" fixes the pour date and the fine (not gross) basis.

## Oracles

- The generator's clean truth (`world.py`, `world_ops.py`): the asks' goldens equal the hauls, recorded stops and lots
  the world made (asserted in `checks.py`).
- `generator/checks.py` (80 assertions: input gates, the three-rules block R1 to R3c, every SF row, mess neutrality,
  margins, devices, separation, distractors, realism, H1, H25).
- `generator/verify.py`, an independent path from `target.zip` (its own readers, a grid fitted to the monuments, the
  log-normal per-block reading and the re-cut factor, pypdf for the documents).
- `generator/ceiling.py`, the cracker and mirror sheets on the cut pack.

## Ask sheet

The asks are the board pack's trails beside the budget: what the stockpile the higher cut-off adds to already holds,
how long the mill that will treat the ore actually ran, and the gold it actually poured. Each is computed from files
the call never reads (asserted: the call is unchanged with every ask file deleted), on rows outside the call's
population (zero dispatch, DCS, maintenance, gold room or refinery rows in the call).

**Ask A, the low-grade stockpile** (8 figures: tonnes to the nearest 1,000 and gold to the nearest 100 oz at
31 December 2023, 2024, 2025 and 31 October 2026). H18: an audit trail of the inventory the plan adds 0.50 to 0.90 g/t
material to. Files: `dispatch_loads_to_lgsp_2023-2026.csv` (8 columns), `haul_fleet_register_2026-10.xlsx` (Fleet and
Disposals), `stockpile_inventory_2022-12-31.csv`. Primary device (D7, key reissued): two truck numbers (T-04, T-09)
were reissued in 2024 to CAT 785D trucks (136.1 t) after their CAT 777G units (90.7 t) were disposed; the Fleet sheet
holds only the current units and the old ones sit on the Disposals sheet, so a payload joined on the number alone
gives every 2023 and early-2024 haul by those numbers the larger payload; found only by a haul dated before its
truck's in-service date. Hazards: the dispatch system's duplicate records (4.3 per cent of hauls logged twice, one to
six minutes apart, a new load id, same truck and source; a truck's real cycle is 22 minutes or more) and UTC times at
the year-end boundaries. Stops: golden 3,629,000 t and 45,500 oz at 2023 (and 5,417,000 / 68,200; 7,196,000 / 90,700;
8,803,000 / 110,900); current-fleet payloads with duplicates removed 3,749,000 / 47,000 (the cracker); dated payloads
with duplicates kept 3,690,000 / 46,300; both mishandled 3,816,000 / 47,900. Pin test: the asking sentence names the
dates, the clock (local) and the measures; neither device's dimension (which truck a number meant on a date, which
records are one haul) is named. Realism: dispatch systems log hauls in UTC and auto-assign a load while a truck's GNSS
drops out; fleets reuse numbers.

**Ask B, ball mill running hours** (7 figures, nearest hour, each calendar quarter January 2025 to September 2026,
local time). H18: the capacity the budget ore meets. Files: `dcs_event_export_grinding_2025-2026.csv` (5 columns),
`cmms_work_orders_grinding_2025-2026.csv` (8 columns). Primary device (D4, absence evidenced in another file): the
historian's collector was down through one planned shutdown in every quarter (seven outages, each opening hours before
the shutdown and closing hours after), so the DCS shows the mill running straight through; only the maintenance
system's shutdown work orders show the stop. Second primary (D2, a label stored before a silent switch): the DCS
migration ran through the May 2026 shutdown and the ball mill's run state continues under a new tag
(GRD.BM01.RUN_STS) from the end of that outage. Hazards: UTC against local quarter boundaries; exact re-sends.
Stops: golden 2,045 / 2,094 / 2,080 / 2,131 / 2,043 / 2,087 / 2,070; DCS only 21 to 58 hours higher every quarter (the
cracker); the old tag only 15 and 41 hours higher in the last two quarters; a fixed UTC-5 clock 1 to 2 hours off.
Pin test: the asking sentence names the quarter and the clock; it names neither the outages nor the tag. Realism:
historians lose data through collector restarts, and IT patches them during shutdown windows; DCS upgrades rename
tags.

**Ask C, fine gold poured** (7 figures, nearest 100 oz, the bars poured in each quarter, local time). H18: the audit
trail of the mill's gold production, the basis of every recovery the budget leans on. Files:
`goldroom_bar_register_2025-2026.csv` (5 columns), `refinery_outturn_statements_2025-2026.csv` (9 columns). Primary
device (D6, an event's quantity on every line it covers): the refinery melts a bar under 300 oz with its neighbour on
the manifest and prints the lot's fine gold on each bar's line, while a bar over its 1,600 oz melt limit is cut into
two lots, each line its own; a bar's fine gold is its share of its lots by gross weight. Summing the lines
double-counts every combined lot (one at each month end); deduplicating by bar loses the second half of every cut bar.
Hazards: bar numbers restart each year and the refinery's reference drops the year; statement dates are settlement
dates. Stops: golden 24,600 / 26,300 / 29,600 / 28,900 / 30,300 / 27,900 / 29,400; lines summed 1,900 to 3,800 oz
higher every quarter (the cracker); quartered by statement date 19,700 / 24,300 / 29,400 / 27,400 / 29,500 / 30,300 /
29,200. Pin test: the sentence names the pour basis and fine gold; it names neither lot shape. Realism: refineries
combine small bars and cut heavy ones to their melt size and report per melt lot.

**Main population zero-counts:** the call reads the LIMS's primary blast-hole rows, the model and the plan; the asks'
devices sit in the dispatch, fleet, DCS, maintenance, gold room and refinery files, none of which the call opens
(asserted by deletion).

| Hazard | Asks moved | Delta |
|---|---|---|
| UTC times | A (year ends), B (quarter ends) | under 1 cell in A; 1 to 2 hours in B |
| exact re-sends | B | none once dropped |
| duplicate hauls | A | 62,000 to 280,000 t and 800 to 3,500 oz |
| settlement dates | C | up to 4,900 oz |

Referee: none; every device is found by an internal inconsistency (a haul before its truck's service date; a week with
no events from any tag while the work orders show a shutdown; a lot's fine gold larger than its bar's gross weight).

| Ask figure | Golden | Mirror | Cracker | Cracker verdict |
|---|---|---|---|---|
| A stockpile tonnes, 4 dates | 3,629,000 to 8,803,000 | 3,690,000 to 9,083,000 | 3,749,000 to 8,987,000 | miss |
| A stockpile gold, 4 dates | 45,500 to 110,900 | 46,300 to 114,400 | 47,000 to 113,200 | miss |
| B ball mill hours, 7 quarters | 2,043 to 2,131 | 1 to 2 hours off each | 21 to 58 hours over each | miss |
| C fine gold poured, 7 quarters | 24,600 to 30,300 | by statement date | 1,900 to 3,800 oz over each | miss |

Mirror leakage: 0.0 per cent of the ask figures (the mirror's half-handled stops miss every figure).
Pair ceiling: 28.5 (cracker 45.0 on the call with no ask figure, mirror 12.0 off the call).
Measured by: generator/ceiling.py on target/ (every row of all 22 figures printed; rerun after every build).

## Architecture 1 record

Private, never ships. A new build (wave 5), numbered from seed FC30. The seed was read at its header and Situation only
(`status.py task159`). Its world (a city transit agency posting weekday-morning platform conductors where crowding is
forecast), its decision (the weekly shift count filed in the spring roster pick notice) and its quantity (one conductor
per platform per weekday morning whose forecast peak 15-minute accumulation is more than 85 per cent of rated capacity)
are kept. The 85 per cent standard is an estimand and a threshold and is filed as the WHAT. The seed's own mechanism
(counts kept per station complex against posting per platform) is kept as the pack's lower rungs and its Layer 1: the
fare system counts entries per complex, and a platform's arrivals have to be built from the census and the counts. The
pitfall is re-found from how a crowded platform actually fills: a six-car train that reaches the first interchange of a
suburban branch already carrying the branch takes only part of the platform's crowd, and the rest wait for the next.

### Draw (architecture 1)

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task159.json`, architecture v1; `guard.py check` WARN (`overuse.org_family`, answered below), one NOTE (`test.same_driver_older`, differentiated against task147 on the card); nearest driver 0.07 (task451 v2) |
| Domain / task type | `urban-regional-science`, task type `forecasting` (serves Forecasting): the deciding quantity is each watch-list platform's peak quarter-hour accumulation forecast for each weekday of a window not yet begun, built from the fare history, the autumn station census and platform counts, and the spring service plan |
| Objective | Forecasting & Predictive Modeling: the spring 2027 pick runs Monday 1 March to Friday 25 June 2027; the as-of date is Monday 11 January 2027 (the fare export to Sunday 10 January); the pick notice closes Wednesday 20 January |
| Shape | `other`: the call (shifts a week) with its weekday counts and the posting schedule, then two decoupled asks on the watch-list complexes and a chart. Criteria: the call 1, the five weekday counts 5, the posting sets 3 (the platforms posted every weekday, those posted Tuesday to Thursday, Corran Junction's Line 5 not posted), Ask A 14 (each complex's escalator flow down and up), Ask B 7 (each complex's elevator-hours), the chart 3: 33 |
| Decision | `quantity_figure`, answer unit `count` (weekday-morning platform conductor shifts a week) |
| Mechanism | gap objective (decisive: a binding limit the proportional carry never checks, the room left on each arriving train) with time (the forward window's weekdays and its eight-car Line 5 trains are a regime the mid-week counts do not show); generators G8 (can the arriving train take them), G16 (the crowd model chosen on the counts it was not fitted to), G13 (the spring pick, its weekdays and its service plan); Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing); `own:platform-queue-behind-trains-arriving-full` |
| Calibration | `physical_verification`: the autumn platform counts, the Monday and Friday counts of the hybrid-day sample the out-of-sample test the crowd model is chosen on |
| Furniture | forum `operations_desk` (Rail Operations' station planning desk files the pick notice), forcing event `shift_or_daily_cycle` (the spring roster pick closes 20 January), organisation family `government_agency`, role family `capacity_planner`, context artifact `register` (the platform capacity register the call reads; re-keyed at stage 2 from `published_series` when the ridership dashboard became a distractor, `guard.py check` re-run clean but for the answered WARN), opening `question-first`, question form `how-many` |
| Spine | the fare back office's hourly entries per station complex and payment type (`vtc_fare_entries_hourly_2024-06-03_2027-01-10.parquet`, UTC, 761,594 rows, from the June 2024 parallel run), beside the legacy four-hour register reads to the July 2024 cutover (`afc_register_reads_2022-02-01_2024-06-30.csv`, local time, a distractor); constructed in the layout of a transit agency's open-data hourly ridership export |
| Deliverables | `spring_2027_platform_conductors.xlsx` (the posting schedule, the weekday counts and the ask tables) and `platform_escalators_am_peak.png` (Ask A's figures charted, never the decision quantity) |
| People | drawn with `guard.py names --geo "United States" --seed 159`: Beth Lewis (station planning manager, owner of the crowding standard), Ralph Chambers (service planning, author of the spring service plan), Mary Wheeler (ridership data, owner of the fare export and dashboard), Caleb Rowe (count programme supervisor); the requester is in no file and not in the prompt |
| World | Vellmouth (checked: no real city, county or transit agency of the name; the nearest hits are a novel's imaginary resort, Valmouth, and unrelated European hamlets), a United States city whose transit commission runs a six-line subway; the commission, its stations, people, systems and data are fictional |

**WARN answered.** `overuse.org_family`: a city transit commission is a government agency; no other key is honest, and
the guard's bans (forum, forcing event, organisation family against the last three builds) all pass.

**Same-puzzle and same-driver tests.** Gap objective, pattern none, `quantity_figure`: no build in the last twelve
carries the triple. Gap objective, no pattern, Gate G `binding_constraint`: task147 (multi-night stays blocked by two
sold-out nights), older than the window and differentiated on the card: there a request is lost when any unit of its run
is full, here nobody is lost, the riders a full train cannot take wait for the next one, so the backlog inflates the
heavy days' counted stock and is absent on the light days.

**Abstraction test.** Stripped of nouns: a stock counted at each stop on the heaviest days is mostly the backlog left by
services that arrive with less room than one interval's arrivals, a backlog that builds only while that shortfall
lasts; on lighter days, when the arrivals and the services' own incoming loads both fall, and once a service is
lengthened, no backlog forms and the stock is one interval's arrivals. Against `guard.py nearest`: task451 v2 (a period
total completed for the part not yet observed), task190 v1 (undetected cases a scarce reviewer would meet), task150 (a
cohort-component projection); none maps onto it. Against the capacity builds in this lane, the nearest by shape though
not by text: task156 (a volunteer tier whose capacity shows only where it fell short, the overflow volume each period
graded) and task153 (a per-visit cap summed segment by segment). Here the capacity is known to move with the weekday's
upstream riders and with the consist, it is built from the census of the branch upstream, and the graded quantity is a
backlog that accumulates train by train over the peak and vanishes on the light days.

**Kinship, answered (the builds the brief names, and every transit card).**
- task254 (a hospital shuttle's latest departure from probe segment times read when the vehicle reaches each segment):
  a trip time; nothing here times a trip, and the only vehicle quantity is how much room a train has.
- task134 (net new homes on upzoned lots around transit stations): land development near stations; no rider, train or
  platform is modelled.
- task123 (cycle-read gas bills calendarised by a measured daily shape): splitting a total over periods by a measured
  profile; here no total is split over periods, and the within-morning profile comes from the census as counted.
- task148 (a 911 late shift's Erlang A with censored caller patience): a queue drained by callers who give up; nobody
  here leaves, the backlog is the riders a full train could not take, set by how full each train arrives from upstream,
  and the rival rejected is proportional scaling of a counted crowd, not the patience-free queue.
- task150 (classrooms placed on cohort-component projections, transfers on the sending school's base): every rider
  source here follows one weekday pattern, and nothing is carried on a sender's base.
- task155 (a relief crew placed where call-ins carrying on from a rostered shift would fill the most): a take-up rate
  conditioned on adjacency; here nobody chooses, the train's room decides who boards.
- task468 (a city transit department's delivered frequency, AVL departures linked to routes): an ETL linkage of vehicle
  records; no vehicle record ships here, and the call is a forecast of platform crowds.
- task256 (a transit authority's operator workstation fitted to the operators' body dimensions): shares the employer
  type only.

**WHAT screen (stumping 1.2).** The decisive step forecasts the filed quantity; it settles none of the estimand's five
parts, each filed in the crowding standard: population (the watch-list platforms in its schedule, every one of them
counted last autumn, none of the spring weekdays yet observed), outcome (a platform's accumulation is the number of
people on it as each train arrives, before its doors open; the peak is the highest quarter-hour mean from 07:00 to
09:45), window (the spring 2027 pick's weekdays, Memorial Day out, each weekday forecast on its own), unit (one conductor
per platform per weekday morning; the call is shifts a week) and comparison (more than 85 per cent of the platform's
rated capacity in the register at the pick's start). No shipped sentence says how a crowd responds to fewer riders or to
longer trains.

**Data-native sentence.** Vellmouth's six-car trains on Lines 1, 4 and 5 reach the first interchange of their suburban
branches already carrying the branch, so on Tuesday to Thursday mornings a train takes only part of the crowd at
Sallow Park and Corran Junction and the rest wait for the next; the count sheets record the crowd as each train arrives,
the fare system counts entries per complex, the census counts the flows onto and off every platform, and no record says
who was left behind, so the backlog shows only as crowds several headways' worth of arrivals deep, and as its absence on
the Mondays and Fridays the count programme sampled.

**Sources read, one line each.**
- Seed FC30 header and Situation (`status.py task159`): the world, the 85 per cent standard per platform, the pick dates
  and the pack's file kinds; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: the forecasting drivers on file price units, cohorts, censoring,
  conditioned yields, constructed exposures and capacity residuals; none forecasts a backlog behind batch service whose
  room is set upstream.
- `two-layer-task-design.md`: "handling the data's real structure" (the counted crowd is a queue) and "validating a
  forecast properly (testing it only on data it was not built on)" (the hybrid-day counts) frame the decisive step.
- `layer2-rigor-patterns.md`, urban and regional science, forecasting pattern 1 (backtest from the forecast origin):
  learned, not copied; here the counts the crowd model is not fitted to are the test.
- `strategies.md` F3 (the limit the metric never checked): the limit is a train's remaining room, shared by every rider
  on the platform and moved by the riders upstream, never a per-candidate cap.
- `guide-to-prompt/references/examples.md` 1 (task133, the divisor no sentence names): the stump is a step a careful
  analyst takes by default, here carrying a counted crowd in proportion to the complex's entries.

### Default path (architecture 1)

Every figure below is built by `generator/calc.py` from the shipped pack and asserted in `generator/checks.py`.

1. Read the crowding standard: a conductor is posted on a watch-list platform on each weekday whose forecast morning
   peak (the highest quarter-hour mean of the people on the platform as each train arrives, 07:00 to 09:45) is more
   than 85 per cent of its rated capacity on 1 March 2027, forecast for an average Monday to Friday of the pick.
2. Take each platform's morning peak on its autumn 2026 mid-week count days (`platform_counts_autumn_2026.xlsx`) and
   average the two mornings.
3. From the fare export (UTC to local), take each complex's weekday index (06:00 to 09:59 entries by weekday over the
   autumn pick's weekdays, against the Tuesday-to-Thursday mean) and the spring-over-autumn ratio (spring 2026 over
   autumn 2025).
4. Carry each platform's mid-week peak to each spring weekday by its complex's index and the ratio; post the
   platform-weekdays over 85 per cent of capacity and count them.

Ends on: 35 shifts a week.

Golden: 26 shifts a week.

### Stump sentence (architecture 1)

A competent solver carries each watch-list platform's mid-week counted peak to each spring weekday in proportion to its
complex's morning entries and files 35 shifts a week, posting Monday and Friday conductors on Sallow Park's Line 1 and
Line 4 southbound platforms and keeping Corran Junction's Line 5 westbound platform posted every weekday; the step that
lands it there is treating a mid-week crowd behind full trains as proportional to arrivals, when on Mondays, Fridays and
eight-car Line 5 trains every train takes everyone and the pick needs 26.

### Three rules (architecture 1)

- **Task type:** `urban-regional-science` / `forecasting`, which serves Forecasting: the deciding object is each
  watch-list platform's forecast morning peak for each weekday of the spring 2027 pick, a window not begun at the as-of
  date, its crowd model chosen on counts it was not fitted to.
- **Domain test:** the quantity that decides the call is each platform's forecast peak quarter-hour accumulation by
  weekday, built the way transit capacity analysis builds platform loading: the arrivals over each headway against the
  room each arriving train still has, the room set by the riders the train already carries from its branch, with the
  riders a full train leaves behind waiting for the next; replacing it with a generic summary (the counted crowd scaled
  by entries) moves the call by nine shifts.
- **Swap:** "how many afternoon clinic shifts the spring rota funds when a waiting room is staffed above 85 per cent of
  its seats" reads as a staffing count, but nothing in a clinic sets how many waiting patients an appointment slot can
  take by how full it arrives from upstream, or lengthens a slot when the consist changes; the backlog behind full
  trains has no counterpart.
- **Layer 1:** each item is how the commission's own systems record the morning and none is placed to be caught, each
  asserted neutral in `checks.py` (R2, FAMILY, SF rows): the fare back office's hourly export in UTC across the 1
  November 2026 clock change, with federal holidays and the weekday-timetable holidays in it; complex ids in the export
  against complex names in the census and the count sheets; the census by platform access and passage, quarter-hours
  labelled by their start, island platforms counted whole with the two directions' riders together; the count
  contractor's sheets by complex, island counts noted by train direction, crowds of about 200 or more estimated in tens,
  timetable times against counted arrivals; the capacity register's effective-dated ratings (Ferrier Square's Line 4
  southbound re-rated while a stair is rebuilt); the June 2024 parallel run of the back office beside the legacy
  four-hour register reads, with Kennet Street a station of its own before March 2024, and the dashboard's rounded,
  preliminary month (both files distractors).
- **Layer 2:** `allocation_constraints`: the platform's crowd modelled as a backlog behind trains of limited room, the
  room built from the branch's own census flows on each weekday, against the proportional carry and the one-headway
  crowd; the proportional carry is rejected out of sample on the hybrid-day Monday and Friday counts and the one-headway
  crowd on the mid-week counts.
- **Decisive step:** treating the mid-week crowds at the first-interchange inbound platforms as backlogs of riders left
  behind by trains that arrive carrying their branch, so that the Monday, Friday and eight-car Line 5 crowds are a
  headway's arrivals rather than the mid-week crowd scaled by entries.
- **Not semantics:** no field, code or note says anyone was left behind: the count sheets record the people on the
  platform as each train arrives, the census the flows onto and off it, the fare export entries per complex; reading
  every column right still scales the counted crowd by the complex's entries and posts the Monday and Friday shifts.
- **Not rule application:** the standard files the measure, the threshold, the window and the posting unit; no filed
  rule says how a crowd responds to fewer riders or longer trains, so executing every stated rule leaves the crowd model
  open, and the natural proportional carry files the default path's figure.
- **Analyst test:** a strong analyst who converts the export to local time, maps the census and the counts onto
  platforms, reads the standard correctly and carries each platform's mid-week counted peak to each spring weekday by its
  complex's morning entries files 35 shifts a week; one who builds each crowd from one headway's arrivals files 20; only
  the backlog behind full trains, against the room each train brings from its branch on each weekday, files 26.
- **Estimand:** the platform crowding standard (`platform_crowding_standard_rev4.pdf`) fixes the population (the
  platforms in its schedule), the outcome (the people on the platform as each train arrives, the peak the highest
  quarter-hour mean among the quarter-hours starting 07:00 to 09:30), the window (an average Monday to Friday of the
  spring 2027 pick, every weekday the weekday timetable runs), the unit (one conductor per platform per weekday morning,
  a posting one shift a week) and the comparison (more than 85 per cent of the rated capacity in the register on 1 March
  2027).
- **No decoy:** nothing is planted to be caught: the counts, the census and the entries are what each system records,
  no memo or thread argues for any count, the hybrid-day sample is the count programme's own choice of each complex's
  top platform the year before, and no stakeholder figure is wrong so the task can overturn it.
- **No certified replay:** the method is not hidden and recovered by reproducing certified figures: nothing certifies a
  crowd forecast, and the hybrid-day counts are raw observations a forecast is tested against.
- **Lesson:** a crowd counted where trains arrive full is a backlog, not a multiple of the arrivals; forecast it from the
  arrivals over each headway against the room each train still has, carry the backlog, and test the model on days when
  the trains have room; no build on file teaches platform loading behind full trains.

### Readability screen (architecture 1)

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the mid-week counted peaks carried to each spring weekday by the complex's entries (35) | the standard asks for a forecast by weekday, which invites carrying the counts | the count sheets and the export's weekdays | yes, the default | the hybrid-day Monday and Friday counts at COR-5W sit 0.6 to 0.7 of capacity under it (under half of it), for an analyst who back-tests | no | yes, one index | readable |
| R0b the same with the hybrid-day counts read as they are where they exist (33) | no | the count sheets' Mondays and Fridays | yes, use the observation | nothing scores Sallow Park's Mondays, which were not counted | no | yes | readable |
| R1 each crowd one headway's arrivals from the census, every train taking everyone (20) | no | the census flows and the timetable | yes, the textbook platform load | the mid-week counts sit 0.8 to 1.9 times capacity above it at SAL-1S, SAL-4S and COR-5W | no | yes, flow times headway | readable |
| R2a a backlog model on the autumn timetable, Line 5 at six cars in the spring (29) | no | the timetable's cars column | a half-step | the spring service plan and the SPR27 timetable run Line 5 at eight cars | no | no | readable |
| R2b a backlog model whose trains keep their mid-week room on every weekday (28) | no | no | a half-step | the hybrid-day counts at COR-5W show no backlog on the Monday and Friday | no | no | readable |
| R3 (decisive) the backlog behind trains whose room is built from the branch's own riders on each weekday, run on the spring timetable (26) | no shipped sentence names a backlog, a train's room, riders left behind or how a crowd responds to fewer riders or longer trains | no column holds boardings, loads, room or riders left behind; the census counts flows, the sheets the people waiting | no: the reflexes scale the counts, use the observation, or take a headway's arrivals | the hybrid-day counts reject the carry at COR-5W on the autumn timetable; nothing scores a spring forecast, Sallow Park's Mondays or the eight-car Line 5 | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a train-by-train run of every branch | silent |

### Semantic fork table (architecture 1)

Every term in the main ask and every convention the main computation needs; every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "shifts a week" | one shift per posted platform-weekday | conductors (people) or hours | same count | the standard ("One posting is one weekday-morning shift a week, 06:45 to 10:00, for the length of the pick") |
| SF2 | "more than 85 per cent" | strictly greater | at least | same call (no platform-weekday within 0.07 of the line, asserted) | the standard; same call, asserted |
| SF3 | rated capacity | the register's rating in force on 1 March 2027 | the rating in force at the pull (Ferrier Square's Line 4 southbound at 300) | same call, asserted | the standard ("in the platform capacity register on the first day of the pick") |
| SF4 | the morning peak's window | quarter-hours starting 07:00 to 09:30 | a sliding window; quarter-hours to 09:45 inclusive of a 09:45 start | same call | the standard ("among the quarter-hours starting at 07:00, 07:15 and so on to 09:30, local time") |
| SF5 | an island platform's accumulation | everyone on the island | the arriving direction's riders only | Monday and Friday posts at the four islands fall away | the standard ("On an island platform it is everyone on the island, whichever train they are waiting for") |
| SF6 | "an average Monday ... of the pick" | the pick's average riding on that weekday | the month-by-month level, March to June | same call (March and June levels asserted) | the standard; same call, asserted |
| SF7 | clock | local time | UTC | same call | the standard ("local time"); the count sheets' method ("All times are local") |
| SF8 | the pick's weekdays | every weekday the weekday timetable runs (Memorial Day out, Juneteenth in) | calendar weekdays | same call (an average weekday) | the standard and the spring service plan |
| SF9 | "mean accumulation over the trains arriving in a quarter-hour" | the mean over that quarter's trains | the largest train's crowd | same call at the backlog platforms (asserted) | the standard |
| SF10 | accumulation | the people on the platform as a train arrives, before its doors open | the people left after the doors close | another quantity | the standard ("as a train arrives, before its doors open") |
| SF11 | the fare export's morning for the weekday index | 06:00 to 09:59 local | 07:00 to 09:59; 05:00 to 10:59 | same call, asserted | same call, asserted |
| SF12 | weekdays in the index | the autumn pick's weekdays, federal holidays out | holidays kept | same call, asserted | same call, asserted |

### Ladder (architecture 1)

Built figures from `generator/calc.py` on the shipped pack, every row asserted in `generator/checks.py` (LADDER, OOS,
FAMILY). The graded quantity is a count of platform-weekdays; each rung names a different count.

| Rung | Construction | Shifts a week | Dies to |
|---|---|---|---|
| R0 default | mid-week counted peaks carried by the weekday index and the spring ratio | 35 (7 each weekday) | the hybrid-day counts at COR-5W (Monday 0.55 and Friday 0.51 of capacity counted, 1.25 and 1.14 carried) |
| R0b | R0 with the hybrid-day counts read as they are where they exist | 33 | Sallow Park was not counted on a Monday or Friday; the eight-car Line 5 |
| R0c | R0 with COR-5W scaled by six cars over eight | 35 | the backlog does not scale with the train: at eight cars it clears |
| R0d | the mid-week counts as every spring weekday's | 35 | the weekday index |
| R1 | one headway's arrivals from the census, every train taking everyone | 20 | the mid-week counts at SAL-1S, SAL-4S, COR-5W (2.17, 2.63, 1.51 of capacity counted against at most 0.71 under R1) |
| R2a | the backlog model with Line 5 at six cars in the spring | 29 | the spring timetable and service plan |
| R2b | the backlog model, trains keeping their mid-week room every weekday | 28 | the branch's own Monday and Friday riders; COR-5W's hybrid days |
| R2c | the backlog model at the fleet register's planning load (110 a car) | 30 | the counts (its autumn back-cast puts the mid-week crowds at 2.5 to 3.9 times those counted) |
| R2d | each complex's forecast against the sum of its watch-list platforms' capacities | 43 | the standard posts platforms |
| R2e | each complex's mean morning hour split equally over its platforms | 13 | the census's platform flows |
| R2f | R0 or the golden averaged over the week | 35 or 30 | the standard forecasts each weekday |
| R2g | the one-headway model scaled by one network factor fitted to the mid-week counts | 35 | the hybrid days |
| R2h | the one-headway model scaled platform by platform to its mid-week counts | 35 | the hybrid days |
| R3 decisive | the backlog behind trains of the spring timetable, each taking at most cars times 150 less the riders it brings from upstream plus those getting off, the branch's riders on each weekday | 26 (4, 6, 6, 6, 4) | golden |

**Position and margins.** The golden is the lowest count of every backlog-free carry and above every one-headway
count; the nearest rivals miss by two (R2b, 28) and three (R2a, 29) shifts, the default path by nine. Each platform-day
sits at least 0.12 of capacity from the line in the golden (0.11 at 120 a car) and 0.076 across its family.

**Convergence (C1, asserted).** Thirteen constructions of the golden file 26 with the same posts: island riders split
30/70, 50/50 or 70/30 between directions; the spring ratio from 2025, 2026, their mean, flat, 0.985 or 1.03; the weekday
index on 07:00 to 09:59 or 05:00 to 10:59; the load per car at 120, 135 or 145. On the clean truth the golden holds from
6 per cent under to 6 per cent over the forecast level, and one sigma of the spring level (the two years' ratios apart
plus 2 per cent for the census normalisation) leaves it unchanged.

**Car-load sweep (CARLOAD, asserted).** Run on the shipped pack from 110 to 160 people a car in steps of five, the
golden files 26 with the same posts at every load from 120 to 155. It moves at 115 (SAL-4S's Monday and COR-5W's
Tuesday to Thursday over the line, 30), at the fleet register's planning load of 110 (30) and above the register's
maximum of 150, at 160 (24). The counts pick the load: the autumn back-cast meets the mid-week crowds at SAL-1S, SAL-4S
and COR-5W best at 145 a car (7 per cent mean error; 140 and 145 within 20 per cent), at 150 it reads 22 to 38 per cent
low, still inside the landing range, and under 120 it puts them at over twice the counts (115: 2.4 to 3.4 times; 110:
2.5 to 3.9 times). Every load the counts hold within 20 per cent files the golden, 20 a car or more above the range's
lower edge.

**Worth on the graded quantity.** Seeing the backlog at Sallow Park is worth four shifts (its Monday and Friday posts
fall away); carrying the backlog to the eight-car Line 5 is worth five more (COR-5W's posts fall away).

**Out of sample.** On the autumn timetable the backlog model puts COR-5W's hybrid Monday and Friday at 0.56 and 0.52 of
capacity against 0.55 and 0.51 counted, and errs 0.069 on average over the hybrid-day sample against the carry's 0.156.

**Strength.** P(one strong solver lands) about 0.20 (the stage 4 rule-3 audit's figure; the stage 2 estimate of 0.15
was optimistic): it has to read the Sallow Park and Corran Junction crowds of one and a half to over two and a half times
capacity as riders left behind rather than riders arriving, build the trains' room from the branch census on each
weekday, and carry the result both to Sallow Park's uncounted Mondays and Fridays and to the eight-car Line 5. P(both
land) about 0.06 to 0.08 with the correlation the audit allows. The seed was fixed by rule (the task number,
then the as-of month and day: 1590111) before any data was generated and is never searched.

### Closure table (architecture 1)

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the platforms in the standard's schedule | filed (the standard's schedule) |
| 2 | Unit of account | the platform-weekday; a posting one shift a week | filed (the standard); SF1 |
| 3 | Attribution window | an average weekday of the spring 2027 pick | filed (the standard and the spring plan); SF6, SF8 |
| 4 | As-of dating | the pull of 11 January 2027; the export to the 10 January service day | the data dictionary; no record after the pull (asserted) |
| 5 | Version basis | the capacity rating in force on 1 March 2027 | filed (the standard); SF3 |
| 6 | Denominator | rated capacity | filed (the standard and the register) |
| 7 | Weighting | none: counts of platform-weekdays | n/a |
| 8 | Window length | the autumn pick for the weekday index, a year for the spring ratio | C1 across index windows and ratio years (asserted) |
| 9 | Boundary inclusivity | more than 85 per cent | filed; nothing within 0.07 of the line (SF2, asserted) |
| 10 | Rounding path | none before the count | n/a |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | the spring pick unobserved at the as-of | the decisive forecast itself; nothing in the pack covers it |
| 13 | Order of operations | the weekday and spring factors applied to the flows before the trains run | C1 (the factors multiply the flows; asserted across variants) |
| 14 | Row order | sums and train order by departure | C1 |
| 15 | Duplicate resolution | none on the call's rows | the realism sweep (no repeated complex-day or census block) |
| 16 | Identity normalisation | complex ids to names through complex_reference.csv | the reference table; the census carries both |
| 17 | Netting against gross | riders getting off free room on arriving trains | the decisive model; no netting rule filed |
| 18 | Dimensional units | people, people a minute, cars at 150 people | the fleet register; R2c rules out the planning load |
| 19 | Code and status semantics | to platform, from platform, passage; E estimated | the census notes and the count method (Layer 1, neutral) |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | the standard applies from the autumn 2026 pick | filed (revision 4 in force from 8 September 2026) |
| 22 | Forward window contents | the spring pick's timetable and consists | the SPR27 timetable and the spring service plan ship |

### Literal reader (architecture 1)

Executing the prompt and the standard word for word gives the count of watch-list platform-weekdays whose forecast
morning peak (the highest quarter-hour mean of the people on the platform as trains arrive, quarter-hours starting 07:00
to 09:30 local) for an average weekday of the spring 2027 pick is more than 85 per cent of the rating in force on 1 March
2027; no shipped sentence says how to forecast a crowd, so a literal reader must model it, the easy method on the same
literal estimand (carrying the mid-week counts by entries) files 35, and the fork table leaves no reading under which a
rung is the golden.

### Oracles (architecture 1)

- The hybrid-day counts (COR-5W, GAR-2, HES-3, FER-5W, ALB-6, QUA-6 on a Monday and a Friday): autumn observations on the
  autumn timetable; on the wrong path they confirm nothing (the carry misses COR-5W's by more than capacity), and they tie
  as well with reading them as they are (R0b, 33) as with the backlog model, so they do not tie only under the golden.
  No spring observation ships.
- The fare export and the census: inputs every method reads alike; neither ranks a platform.
- The ridership dashboard (a distractor): average weekday entries by complex and month, consistent with the export on
  its own definition; it ranks nothing on the decision.
- No control ties only under the golden.

### Ask sheet (architecture 1)

**Main call's declared row population:** the station census, the platform counts, the fare export's `entries` column,
the weekday timetables, the fleet register, the platform capacity register, the complex reference, the crowding
standard and the two service plans. Device and hazard rows in it: 0 (asserted, SEPARATION: the golden reads none of the
ask files and the asks read none of the call's records; the asks' devices sit in the inventory's direction and speed
columns, the work orders' times and the monitoring's modes).

**Ask A. For each watch-list complex, the people a minute the escalators between its mezzanines and any of its
platforms can carry at their rated flows down to the platforms and up from them between 07:00 and 09:30 on the days of
the autumn 2026 pick that ran the weekday timetable, all times local** (14 figures, whole people a minute).
- H18 home: a measure every candidate complex carries that the call does not turn on, how fast the morning's riders
  reach and leave its platforms, read beside the posting schedule for the conductors' post orders.
- Basis (filed in the station planning manual, chapter 5, the owner's voice): "An escalator's rated flow depends on its
  step width: 40 people a minute for a 600 mm step, 60 for an 800 mm step and 80 for a 1,000 mm step at 0.5 metres a
  second, and in proportion to its speed at other speeds. An escalator carries its rated flow in the direction it is set
  to run." and "The escalator capacity between two levels is the sum of the rated flows of the escalators between them,
  taken for each direction. Capacities are rated with every escalator running and make no allowance for stoppages."
- Readings closed (round 1, each built as a route in `calc.py` and asserted to move figures and to be ruled out by
  filed text): the controllers' fault minutes deducted (five figures move: Sallow Park down 215, Hesper Avenue up 143,
  Ferrier Square up 247, Quarry Road 131 down and 95 up; the manual's "make no allowance for stoppages"); only the
  escalators to watch-list platforms (five move, Sallow Park's Line 4 northbound E6 and Corran Junction's Line 5
  eastbound E3 among them; the prompt's "any of its platforms"); the holiday-timetable days of 26 and 27 November in,
  when the escalators stay in their all-day directions (all fourteen move; the prompt's weekday-timetable days, the
  standard's own weekday); the log's UTC read as local (all fourteen move; "all times local" and the dictionary's
  "UTC"). Weighted over the window with no allowance for stoppages the figures are the golden's (asserted), so minutes
  and days aggregate to the same people a minute.
- Readings closed at ship (the re-judge's advisory and the targeted re-read, each asserted): the clock, now one line
  in the dictionary's Notes sheet (US Eastern, UTC-4 before 1 November 2026 and UTC-5 after; the log at a fixed UTC-4
  or UTC-5 all autumn moves all fourteen); time-weighted against dominant direction (every one of the 2,736 unit-days
  holds one direction for all of the window, so the two agree); a stopped unit's direction (the only stoppages inside
  the window are faults, on 25 unit-days, each reset to the direction set, and the manual makes no allowance for
  them); the inventory's direction against the log (17 of 38 units differ in the window; the dictionary dates the
  inventory's direction to the condition survey and the manual counts an escalator in the direction it is set to
  run); widths in inches (every inch width at 25.4 mm falls in the asset register's own step class, 600 or 1,000 mm,
  on all 38 units).
- Primary A1 (D2, an attribute at the wrong vintage): the engineering inventory records each escalator's running
  direction as surveyed at midday; in the morning peak station operations turn the pair at a boarding platform both
  down and at an alighting platform both up; the escalator controllers' log carries every direction change. Fair: the
  log gives every escalator one direction from 07:00 to 09:30 on every autumn weekday (asserted). Silent: the inventory's
  direction is complete and valid, and no shipped sentence mentions a morning reversal.
- Primary A2 (D2, a label stored before a silent switch): the inventory keeps each escalator's design speed (0.5 m/s);
  the Lines 1 to 4 escalators were slowed to 0.45 m/s in the 2019 step-chain programme, a setting only the maintenance
  system's asset register holds. Fair: the register gives every unit's controller speed. Silent: the inventory's speed
  is a valid design value, and nothing narrates the slowdown.
- Hazards: HA1 step widths in inches on Lines 1 to 4 and millimetres on Lines 5 and 6 (the dictionary says so); HA2
  street escalators in the same inventory (the ask counts the escalators between mezzanines and platforms); HA3 UTC in
  the log.
- Stops (built and asserted, every figure missed by each): the inventory's directions and speeds (S1: Garnett Street
  120 down, 120 up against the golden 72, 144); the log's directions with the design speed (S2: 80, 160); the
  inventory's directions with the controllers' speeds (S3: 108, 108); the golden.
- Span: the station elements inventory, the escalator controller log, the escalator asset register, the station
  planning manual, the data dictionary (5 files).
- Realism: transit systems reverse escalators by time of day to the main flow, and an engineering inventory keeps the
  surveyed direction and the design speed while the maintenance system keeps the controller settings.

**Ask B. For each watch-list complex, the total elevator-hours all its elevators were out of service between 07:00 and
09:45 on those mornings, all times local** (7 figures, one decimal).
- H18 home: a measure every candidate complex carries that the call does not turn on, how often its riders who need
  the elevators met one out in the morning peak, read beside the posting for the conductors' post orders.
- Basis (filed in the station planning manual, chapter 5): "An elevator is out of service whenever it is not in normal
  passenger service: from the moment it stops on a fault, or is taken out of service for maintenance, inspection or
  repair, to the moment it is back in normal passenger service. Time out of service for more than one reason at once
  counts once." The union of the two sources' intervals is that definition executed; the window and the pick's
  weekday-timetable days are the prompt's, the holiday-timetable days the autumn service plan's.
- Readings closed (round 1, built and asserted as for Ask A): the holiday-timetable days in (Garnett Street 31.8 against
  27.9, the other six unchanged; the prompt's weekday-timetable days); a mean per morning (every figure; "the total
  elevator-hours"); the street elevators left out (every figure; "all its elevators"); the logs' UTC read as local
  (every figure; "all times local"); overlapping work-order and monitoring intervals counted twice (every figure; the
  manual's "counts once"). At ship: the logs at a fixed UTC-4 or UTC-5 all autumn (every figure; the dictionary's clock
  line).
- Primary B1 (D8, an anchor on the record, not the event): the control centre opens a work order when the station
  reports the fault, so its out-of-service time runs after the car stopped; the remote monitoring logs the stop.
  Fair: the monitoring gives each fault's stop and its return to normal service. Silent: every work order is complete
  and valid, its out-of-service time earlier than its return.
- Primary B2 (D4, a reporter or channel absent): the remote monitoring receives the controller's passenger-service
  modes (normal, fault, independent, shutdown); planned maintenance runs the car on inspection operation, which the
  monitoring does not receive, so planned maintenance is only in the work orders (type PM, "the car on inspection
  operation for the work" in the dictionary). Fair: every PM work order carries its own start and end, and inspection
  operation is not normal passenger service. Silent: the monitoring log is complete for the modes it receives.
- Hazards: HB1 times in UTC across the 1 November clock change (the dictionary says UTC); HB2 outages running over
  more than one morning (the windows clip them); HB3 Columbus Day and Veterans Day run the weekday timetable (in), the
  Thanksgiving days the holiday timetable (out).
- Stops (built and asserted): the work orders alone (every figure missed by 0.7 to 2.0 hours: Garnett Street 27.2
  against the golden 27.9); the monitoring alone (missed by 1.2 to 7.0 hours: Garnett Street 21.0); the golden.
- Span: the elevator work orders, the elevator monitoring, the station planning manual, the autumn service plan, the
  data dictionary (5 files).
- Realism: maintenance systems stamp a work order when it is opened, and remote monitoring vendors report the
  passenger-service modes rather than the mechanic's inspection operation.

**The chart** (`platform_escalators_am_peak.png`): Ask A's figures, down and up for each complex, each bar labelled;
graded on its content (Ask A's figures) and its parts (both directions for every complex, labelled; the title).

**Hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| Units (inches and millimetres for escalator steps) | A | A: a step read in the wrong unit lands in another flow band |
| Clocks (UTC in the controller log, the work orders and the monitoring; local windows) | A, B | B: November and December windows an hour out under a fixed offset |
| Scope (street against platform escalators; weekday-timetable holidays) | A, B | A: street escalators add to a complex's figures; B: two mornings in or out |

**Referee.** The controllers' log and the asset register (Ask A), the monitoring and the PM work orders (Ask B); none
hands over a level.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, seven complexes' flows down and up (14) | the manual's rated flows on the inventory's escalators, steps converted to millimetres, platform escalators only | A1 the morning reversals and A2 the slowed controllers, each alone enough | miss |
| B, seven complexes' elevator-hours (7) | the work orders' out-of-service times clipped to 07:00 to 09:45 local on the pick's weekdays | B1 the report lag and B2 the maintenance the monitoring does not report, each alone enough | miss |

Measured by: generator/cracker.py (run on the cut pack: each response scored on a rubric modelled on the generated
one, the call and its components 35, the instructions 7, the asks 58 over every ask figure and the chart's parts).

**Mirror sheet.** The mirror stops at R0 (35 shifts) and meets the same devices; it keeps the chart's two parts and no
Ask A or B figure. Cracking any one device (A1, A2 or B1) leaves its ask missed, since each ask has a second device.

Mirror leakage: 8.3 per cent of ask weight (the chart's two parts).

Pair ceiling: 29.3 (the cracker 46.8, the mirror 11.8; with the most obvious device cracked 29.3; both top responses on
the call with no device cracked 46.8). Rerun from the generated rubric at stage 4.

### Surface screen (architecture 1)

`guard.py surface task159` promotes one pair, at the card level only: task147 against task159 (gap objective, pattern
G8, Gate G `binding_constraint`, the same-driver signature), differentiated on the card at the draw: there a
multi-night request is lost when any night of its run is sold out; here nobody is lost, the riders a full train cannot
take wait for the next one, so the backlog inflates the heavy days' counted crowds and is absent on the light days. No
hard tell (no shared file name, schema, invented name or same-seed table). `guard.py heart` was WARN through stage 4
(`overuse.org_family`, answered at the draw; nearest driver 0.07, task451 v2) and BLOCKs at ship on furniture against
task158 (forum and role family), raised after the draw by two re-roots' re-registration; the pre-ship check records it
for the author. The persona sweep reads "Line Early" off the service plans' headway table, where the column heading
"Early" follows the row heading "Line"; it is not a person.

### Leak sweep (architecture 1)

`leak.py task159 --asof 2027-01-11` returns REVIEW (no LEAK); every line answered:
- Sweep 3, the crowding standard names the watch-list platforms beside the call's vocabulary: the schedule is the
  population the call executes and the standard is the rule it runs on; it carries no count, forecast or posting.
- Sweep 4, stump-paragraph terms in the standard, the service plans and the station planning manual (counts, trains,
  forecast, capacity, Monday, Friday, timetable, headway; the manual's "capacity", "carries" and "counts once" are its
  escalator capacities and its out-of-service definition): each document's own subject (the measure and the count
  programme; the weekday service and its consists; vertical circulation); none names a backlog, a train's room, riders
  left behind or how to carry a crowd (asserted in `checks.py`, R3c).
- Sweep 6, files naming the watch-list complexes beside numbers (the legacy reads, the elevator work orders, the
  capacity register, the dashboard, the census, the inventory): records per complex of entries, outages, ratings,
  flows and elements; none ranks the platforms on the posting question.
- Sweep 9, dates after the as-of: the capacity register's restored rating for Ferrier Square's Line 4 southbound from
  2027-02-13 (the works end 2027-02-12) and the change register's spring entries from 2027-03-01, forward-looking
  records allowed by file (`reduce-house-fixes` H16).
- Sweep 10: no writer signature or out-of-band stamp; the fare export's Parquet footer carries Arrow's own writer
  string, as any export from that toolchain does.

### Build record (architecture 1)

Stage 3, 2026-10-17; rebuilt after the stage 4 round 1 findings and again at ship the same day. `build.py`: checks 129
run, 0 failed (the
three-rules block R1 to R3c on the generator's clean truth, the R2 mess-neutrality variants, every SF row SF1 to SF12,
the ladder's fifteen rungs and rivals, the out-of-sample test, thirteen family constructions and the one-sigma
corridor, the car-load sweep, both asks with their routes, edges and every closed reading, the separation line, the
input gates, the distractors' deletion test, the realism sweep and the dates allow-list); `verify.py` (pandas, no
generator import) 6 passed, 0 failed; two consecutive builds byte-identical (target, golden, figures.json,
submission); `figures_check.py` 0 absent (40 figures); `voice-check.py` PASS (950 characters); `precut.py` exit 0;
`leak.py` REVIEW, no LEAK; the H1 audit clean on the pack and the goldens; `guard.py validate` clean, `heart` WARN
(answered), `surface` one card-level pair (above); `generator/cracker.py` pair ceiling 29.3, mirror leakage 8.3 per
cent. 20 files in 4 formats (parquet, csv, xlsx, pdf), the largest the fare export at 761,594 rows; distractors
`afc_register_reads_2022-02-01_2024-06-30.csv` and `ridership_dashboard_avg_weekday_2025-2026.xlsx` in `metadata.json`.
Invented names checked: Vellmouth (no real city or transit agency), the count contractor Tollison Field Data (renamed
at round 1 from a name echoing task148's Halvorsen Township; no firm of the name in a web search, and no other build
uses it); station names are ordinary street and place names; the car and escalator builders are real manufacturers
named descriptively; personas from `guard.py names`. The platform capacity register states its rating basis on every
row (one person per square metre of usable platform area, from the 2019 survey; Sallow Park's August 2026 re-measure on
its own row from 1 September 2026, the rating unchanged). The seed was fixed by rule
(1590111) before any data was generated and never searched. The pack's files share the pull's modification time, the
house convention (`dataset-generation` section 9).

### Pre-ship check (architecture 1)

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each watch-list platform's forecast
  peak quarter-hour accumulation by spring weekday, built the way transit capacity analysis builds platform loading
  (arrivals over each headway against each arriving train's room, the riders a full train leaves waiting), on the clean
  truth and on the pack (R1 to R3c). Two layers: the Layer 1 inventory in `## Three rules`, each item asserted neutral
  on the call (R2: the export's UTC read as local, converted at four hours and at five hours all year, the census
  quarter-hours read as ending at their label, a spring ratio off the legacy reads; SF1 to SF12); the asks' devices
  confined to the ask files (SEPARATION); Layer 2 the backlog behind full trains, chosen on the hybrid-day counts it was
  not fitted to (OOS). The decisive step is none of the three banned kinds: not a plant (R3c: no document names a
  backlog, a train's room or riders left behind, and the counts, census and entries are what each system records);
  not data semantics (every term read right still carries the counts by entries to 35); not rule application (every
  filed rule executed with the proportional carry files 35, with one headway's arrivals 20; only the queue files 26).
- **Gates.** 20 files in 4 formats (csv, parquet, pdf, xlsx); the fare export at 761,594 rows; two distractors (the
  legacy register reads and the ridership dashboard), each deletion asserted; `checks.py` 129 run, 0 failed;
  `verify.py` (pandas, no generator import) 6 passed; two builds byte-identical (target, golden, figures.json,
  submission); `figures_check.py` 40 of 40; `precut.py` exit 0; `voice-check.py` PASS at 950 characters; `leak.py`
  REVIEW, no LEAK, every line answered; the H1 audit clean on the pack and the goldens; `guard.py validate` clean,
  `surface` one card-level pair (task147, differentiated at the draw), `heart` BLOCK at ship on furniture (below);
  `generator/cracker.py` pair ceiling 29.3, mirror leakage 8.3 per cent. `target.zip` cut from the final rebuild, 20
  entries equal to `target/` byte for byte, sha256 150f8fc2.
- **Heart at ship, for the author.** `guard.py heart` now BLOCKs `ban.role` (capacity_planner) and `ban.forum`
  (operations_desk) against task158, with `repeat.deliverables` (png and xlsx) a WARN. The ban was raised after the
  draw: at the DRAWN commit (8ec573e) the last three draws before this one were task190, task240 and task194 and the
  check passed; task190 (architecture 4) and task194 (architecture 3) have since re-rooted and re-registered after this
  card, which brings task158, drawn at 16:46 and the same lane's previous build, into the window. Both keys are this
  build's honest ones (the station planning desk acts on the count; the stakeholder plans staffing), so they are kept,
  not relabelled; no shipped file or prompt sentence names either. Whether the pair reads as a batch repeat is the
  author's call before upload.
- **Stage 4.** Round 1: judge DETERMINISTIC, FIX_NOW on the asks only; leak reader clean, the decisive step analytical;
  rule 3 audit PASS (P(one) about 0.20, P(both) about 0.06 to 0.08). Every finding fixed in one generator pass with the
  call frozen (`## Tried and rejected`, the ask sheet's closed readings, the car-load sweep). Re-judge DETERMINISTIC,
  APPROVE: its own train-capacity queue model filed 26 (4, 6, 6, 6, 4) with the same postings and reproduced every
  escalator and elevator figure; its one advisory (the clock) filed at ship. The targeted re-read was clean on the main
  call.
- **Gate G.** No shipped artifact ranks the platforms on the posting question, and `metadata.json` declares no
  wrong-basis distractor. Delete every wrong number in the pack and the call still turns on reading the mid-week crowds
  as a backlog behind full trains.

### Residual (architecture 1)

- The capacity register repeats one basis text on most rows, as a register rated in one survey reads; kept.
- Sallow Park's August 2026 re-measure kept its 2019 effective date when the re-judge read the pack; it now has its own
  row from 1 September 2026 with the rating unchanged, so no graded figure moved.
- The clock was derivable but unnamed (the first trains and escalator starts near 05:00 local); the dictionary now
  names the zone and the 2026 change at no cost to Layer 1, since the main call is the same at either fixed offset.
- At 150 a car the back-cast reads the mid-week crowds 22 to 38 per cent low (the census-scaled model runs lighter than
  the counts); the counts' best fit, about 145 a car, sits inside the landing range, and the golden holds at both.

## Tried and rejected

- Weekday patterns by rider source (transfers on the feeding line's week, street entries on the complex's): rejected at
  the draw before any card was filed, because its kernel (an inflow carried on its sender's driver, not the receiver's)
  is task150's.
- A train-load file pinning each train's room: rejected at the draw; it would hand over platform boardings on every
  uncrowded day and break the seed's complex-level premise; the room is built from the census of the branch upstream.
- Trains' room assumed constant across weekdays when only mid-week rooms are inferable: rejected at the draw; the
  Monday verdicts then turn on an assumption the data cannot settle (a Gate C fork), so the room is pinned from the
  branch census and the weekday entries.
- Near-threshold platforms off the backlog lines (an island at 0.77 to 0.97 of capacity, posted Tuesday to Thursday):
  dropped at stage 2, because the island counts' noise (the other direction's riders, a delayed train) and the census
  split of island riders by direction moved those platform-days across the line between defensible constructions; the
  ratings were set so every platform off the backlog lines is at least 0.10 from the line.
- A Sallow Park backlog only 4 per cent above its knee on Thursdays: deepened at stage 2 (the branch riders 3 per cent
  up and the mid-week weekdays within a point of each other), so the golden holds from 6 per cent under to 6 per cent
  over the forecast level.
- Revenue protection's evasion survey reconciled to the fare system as an ask: dropped, because every natural device
  sat at one or two complexes and none moved every figure; the census's array counts would have put an ask organ in a
  document the call reads.
- Escalator sizes by nominal width as the second escalator device: dropped, because the manual's "step width" and a
  step-width column in the asset register adjudicate it; the slowed controllers replace it.
- The ask anchored "at 08:00" on the controllers' settings: dropped, because a clock time sends the solver to the log;
  the ask now names the morning peak window.
- Planned maintenance logged in the elevator monitoring: dropped, because with every mode logged the monitoring alone
  answers the ask once found; inspection operation is now reported only in the work orders.
- The golden held only from about 140 a car (judge, round 1: SAL-4S's Monday crossed the line at about 135 a car, and
  more platform-days below 130): the Line 1 and Line 4 branches above Sallow Park now ride hybrid weeks (Mondays
  and Fridays about 0.66 and 0.62 of mid-week against the network's 0.82 and 0.76) and Line 5 westbound boards 3 per cent
  lighter, so the golden holds from 120 to 155 a car.
- Sallow Park's own Mondays and Fridays as light as its branch's (round 1, the first pass): rejected, because with
  Sallow Park's own boarders that light the trains' mid-week room takes them on every weekday and the constant-room
  rival (R2b) filed the golden; the branch upstream carries the hybrid week and Sallow Park rides like the network.
- Line 5 westbound 1.5 per cent lighter instead of 3 (round 1): rejected, because COR-5W's eight-car Wednesday then
  crosses the line at 120 a car.
- The asks' fault minutes and holiday-timetable days left to the rubric (accepting 215 or 216, 27.9 or 31.8): rejected
  at round 1; the manual and the prompt now close both, with every other reading the reader raised.
- 2026-11-01, Batch 3 queue reset: architecture 1 (the Vellmouth platform conductor pick) re-rooted whatever its
  status; the transit world is closed, task133 had just shipped in urban-regional-science / forecasting, and the old
  card's identity moved to the card's lineage with fate "re-rooted 2026-11-01 at the Batch 3 queue reset".
- Architecture 2 draw, twin-plant wrong-train slips under one panel operator (human-reliability-assessment, a urea
  complex's new central control room; the slip rate read in the hours one operator already ran both trains): rejected
  at the abstraction test against task141 (a forward change puts every unit into a state some units already occupy, so
  the rate those units show applies to all); the guard also blocked its gap and generator signatures.
- Architecture 2 draw, the same world with slips per switch between trains: rejected; the exposure unit is a model
  the data could not force without filing it (a Gate C fork or a filed HOW).
- Architecture 2 draw, operator response times pre-empted by an automatic trip, read with the trips as censored:
  rejected against task169 (a pre-empting route hides what the remaining route would have done).
- Architecture 2 draw, the prevalence effect at an inspection station and alarm floods at a merged console: spent
  (task175's screens retired the low-prevalence effect in this task type; task170's note found the console merger
  replayable).
- Architecture 2 draw, mixed-population wind extremes for a design gust (climate-weather-extremes): set aside; the
  extreme-value fits spread across the bin and separating storm types is the wind engineer's textbook route.
- Architecture 2 draw, this world with a noisy, conditionally biased model (regression to the mean at the raised
  cut-off): set aside; regression to the mean under selection is task304 v5's driver in this batch. The smoothed,
  conditionally unbiased model replaces it: the routes that read the model's own calibration (slope 1.008) or the
  model-ore blocks' grade-control grades file the default's 130,000, so the step cannot be read as a shrinkage.
- Architecture 2 build, the ore grade as the main call's component: dropped; the default's grade (the plan's 1.46 g/t
  times the reports' grade factor 1.17) prints the golden's 1.7, so it graded nothing; the ore tonnes replace it.
- Architecture 2 build, the plan's face position on bench 1185: 10,150 left the per-block ore tonnes 7,000 t from the
  2.75 Mt line and 10,190 left the re-cut factor on the last twelve months 400 oz from the 155,000 line; 10,180 keeps
  the whole standing family inside one cell for ounces (1,391 oz clearance at the tightest) and tonnes (28,429 t).
- Architecture 2 build, the ratio route on a single year of the record: noted, not licensed; the factor re-cut on one
  year spans 1.167 to 1.252 because each year's estimates sit differently about the cut-off (2024 alone files
  159,799), while the per-block reading is year-proof (149,701 to 150,239).
- Architecture 2 asks, a laboratory CRM performance trail (a legacy code re-pointed to a new certificate): dropped; the
  CRM issue log is a helper document the careful solver reads, so the device was a work order.
- Architecture 2 asks, refinery combined lots alone: strengthened with cut heavy bars; the battery's header-to-items
  pairing lands combined lots on their own, and the two shapes need opposite repairs.
- Architecture 2 asks, historian outages in four quarters: raised to one planned shutdown a quarter so every quarter
  carries the device.
- Architecture 2 build, maintenance isolation times equal to the DCS stop and start: rejected; two observers sharing
  every bound is a causal impossibility, so the crew's isolation runs from 3 to 13 minutes after the stop to 4 to 16
  minutes before the start.
- Architecture 2 build, hauls generated on local wall time: rejected; spring-forward wall times that do not exist put
  four real hauls within ten minutes of another in UTC, so hauls are generated on UTC.
