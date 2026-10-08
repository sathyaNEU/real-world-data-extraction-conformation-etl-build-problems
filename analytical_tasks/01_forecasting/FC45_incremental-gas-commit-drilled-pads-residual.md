# FC45 — How much 2027 incremental gas to commit to the LNG buyer, when a third of next year's new wells were drilled this year and sit in neither the rig schedule nor the production reports

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · upstream gas supply and marketing (Appalachian shale) |
| Mirrors | Committing next year's incremental supply from a pipeline of assets in flight (shale operators selling incremental volumes to LNG feedgas buyers, data-centre capacity built but not yet energised, warehouses fitted out but not yet live), where the work already done sits between the build plan and the live inventory |
| Decision shape | One figure committed at a date: the 2027 volume written into the incremental firm-sale agreement |
| Committed call | Gas from wells first turned in line in 2027 that will be produced in calendar 2027, in Bcf to the nearest whole Bcf |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S2 (a residual population between two correct records, projected on a single-valued interval), with finer controls separating constructions (measured #12) at rung 1 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #18 joins only on the visible key · #12 stops at the first control that passes · #7 uses the ready-made measure |
| Calibration form | Change-log natural experiments: the completion log's 26 past pads, each with its frac and turn-in-line dates, read against the state spud register and the monthly production reports |
| Driving force | The incremental volume is gas from wells first turned in line in 2027. The natural build takes them from the 2027 rig schedule. But four eight-well pads spudded from August to December 2026 have not been fracked: they are in neither the rig schedule (which lists 2027 spuds) nor the production reports (they have never produced), and no column marks them. They exist only as the residual of the spud register against the completion log and the reports, and every past pad turned in line 16–18 weeks after its last well was spudded, so all 32 wells start producing between January and April. In every closed year pads were small and turned in line the year they were drilled, so the residual was empty. |

## 1. Situation

A gas producer in north-east Pennsylvania is signing a 2027 incremental firm-sale agreement with an LNG feedgas buyer: the volume committed
is gas from wells first turned in line on or after 1 January 2027, delivered in calendar 2027. A shortfall is bought back at spot plus a
penalty; a surplus sells at a discount. The pack holds the state spud register, the state's monthly production reports (published to
September 2026), the operator's completion log, the 2027 rig schedule, the reserves team's type curve, the pad register with spacing and
lateral lengths, and the agreement. Since 2026 the operator drills eight-well pads at 660-foot spacing, where it used to drill two to four
wells at 1,000 feet. The term sheet is due on 20 November.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: spud dates, production reports, the completion log, the rig schedule, the type curve and the pad
  register. No stakeholder's reading of their own numbers is overturned; the type curve really does describe the wells it was built on.
  The difficulty is a population of wells that next year will contain and that neither plan nor production records.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the reserves lead's view and every voice. The rig schedule is still the natural list of next year's new
  wells, and every closed year still confirms it.
* **Instrument repair.** Imagine production reported with no lag. The drilled pads would still show nothing, because they have not been
  fracked; the gas they add in 2027 is set by when they turn in line and how tight-spaced wells perform, which no better record of past
  production shows.
* **Lens swap.** The naive read and the answer count different populations: wells the 2027 rig will spud, against wells that will first
  produce in 2027, a majority of which were spudded in 2026.

## 3. The driving force

A strong solver takes the 2027 rig schedule, places each pad's turn-in-line after its drilling, prices the wells with the type curve,
corrects the curve for spacing when the finer pad controls show tight wells 25% below it, and corrects the rig's pace from the spud
register's 15 days a well against the schedule's 12. It lands at 30 Bcf, and the same build reproduces every closed year within 3%. Every
step is correct. But the wells that will first produce in 2027 are not all on the rig schedule. The 2026 programme moved to eight-well
pads, and a pad is fracked only when its last well is drilled; the four pads spudded from August to December have no frac in the completion
log and no line in the production reports. They are 32 wells that exist only as a residual: spudded, never producing, not plugged. Every
one of the 26 past pads turned in line 16–18 weeks after its last spud, so these turn in line on 7 January, 16 February, 29 March and
26 April. At the spacing-adjusted curve they produce 100 Bcf in 2027, and the commitment is 130 Bcf.

## 4. The ladder

| Rung | Construction | Lands on (2027 Bcf) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The 2027 rig schedule's pads, turned in line 17 weeks after their planned last spud, priced on the reserves team's type curve | 60 (−54%) | The operator's standard incremental build, and it reproduces 2025's incremental volume within 2% | The pad register: every 2027 and late-2026 pad is spaced at 660 feet, while the type curve's wells are at 1,000 feet or wider |
| 1 | Type curve rebuilt by spacing, fitted to the pads at each spacing | 45 (−65%) | Passes the salient control (2025's programme total) and the finer per-pad controls the pooled curve fails | The spud register: every 2025–26 pad drilled at 14.6–15.4 days a well against the schedule's 12, so each 2027 pad turns in line later |
| 2 | Drilling pace from the spud register applied to the 2027 pads | 30 (−77%) | Right curve, right timing, and it reproduces every closed year within 3% | The spud register against the completion log and the reports: 32 wells on four pads spudded August–December 2026 have no frac, no turn-in-line and no production |
| 3 | **Decisive:** the 32 drilled wells recovered as the residual of the spud register against the completion log and the reports, turned in line 17 weeks after each pad's last spud, priced on the spacing-adjusted curve | **130** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the volume down (−54%, −65%, −77%) and the decisive rung reverses past rung 0, so a solver who stops
  anywhere short under-commits and sells 2027's surplus at a discount.
* **Partial correction priced (L3).** A solver who finds the drilled pads but puts them online on 1 January lands at 150 (+15%). One who
  adds them but prices them on the pooled curve, because the rig schedule's pads were the ones it re-curved, lands at 163 (+25%). One who
  adds only the two pads whose last spud fell before the production reports' cut-off lands at 82 (−37%).
* **Grid.** Curve (pooled, by spacing) × pace (schedule, register) × drilled pads (out, in) = 8 cells: without the pads 60, 40, 45, 30;
  with them 193, 173, 145, 130. The nearest wrong cell is the scheduled pace with the pads in, 145 (+11.5%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The agreement defines incremental gas by first turn-in-line; the rig schedule lists 2027 spuds; no document lists
   wells awaiting a frac or says when a pad is fracked.
2. **Corpus blind to the residual.** *In every closed year every pad drilled in the year turned in line in the same year, because pads had
   two to four wells and drilling ran from January to August; so the year-end residual of drilled, never-producing wells was empty, and the
   rig schedule priced on the type curve reproduced every closed year's incremental volume within 3%.*
3. **No arithmetic symptom.** Spuds reconcile to permits, turn-in-lines to first production, and every rung's volume ties to its wells.
4. **Not a row predicate.** The drilled pads come from an anti-join of the spud register against both the completion log and the reports,
   grouped by pad, each pad's last spud taken and the interval applied before any well is priced.
5. **The enumeration is arithmetic.** The state register calls every unplugged well "active"; no column says "drilled, not completed".
6. **No cutover date.** No outcome series steps; pad size grew over the 2026 programme, and the residual is a consequence, not an event.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The completion log's 26 past pads (2021–2026), each with its frac start, frac end and turn-in-line, joined to the spud register
  for each well's spud date and to the monthly production reports for what followed.
* **What it certifies.** The rig-schedule build, the spacing-adjusted curve and the drilling pace, each reproducing the closed years.
* **What it pins.** The interval: every pad turned in line 16–18 weeks after its last well was spudded, whatever its size or season.
* **Twin pair.** Pads Ridgeline 4 and Kettle Run 2 are identical in the spud register and the pad register: first spud on 3 March 2025,
  four wells, 1,000-foot spacing, equal laterals. Their 2025 volumes were 7.9 and 3.8 Bcf (2.1× apart), because a stuck-pipe sidetrack moved
  Kettle Run 2's last spud from late March to late May, and its turn-in-line followed 17 weeks later. Only the last-spud interval separates
  them.
* **Resemblance points at the decoy.** By rig count, schedule and curve inputs, 2027 most resembles 2025, whose incremental volume the
  rig-schedule build reproduced within 2%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The agreement: incremental gas is gas from wells first turned in line on or after 1 January 2027, delivered in calendar
  2027. The reserves team's type curve and the pad register. The rig schedule's 2027 pads.
* **Empirical pins.** The 16–18 week interval and the drilling pace, from the completion log and the spud register. The spacing-adjusted
  curve, from the pads at each spacing.
* **Voices.** The reserves lead: "The type curve and the rig schedule tell us everything we'll bring on next year." The drilling manager:
  "We'll hit the rig schedule; we always have." The marketing vice-president: "Commit low; a shortfall costs us more than a surplus."
* **Licensed wrong basis.** The agreement records that the buyer's credit desk sizes its letter of credit on the operator's rig schedule
  priced on the type curve and will review the committed volume on that basis.

## 8. Determinism by construction

* **Interval.** Each drilled pad's turn-in-line falls in the same month under 16, 17 or 18 weeks, because no date lands within a week of
  a month's edge.
* **Residual.** The spud register, completion log and reports agree on every pad identifier, and the plugging register holds none of the
  32 wells, so the anti-join returns one set under any join order.
* **Curve.** The spacing-adjusted curve is pinned month by month to the pads at each spacing; fitting by month online or by calendar month
  agrees within 0.4%.
* **Pace.** Every 2025–26 pad drilled at 14.6–15.4 days a well, so mean and median give the same 2027 turn-in-line months.
* **Rounding.** The forecast is 130.4 Bcf, clear of the rounding edges.

## 9. Prompt sketch and deliverables

> We sign the 2027 incremental supply deal with the LNG buyer on the 20th, and the volume we commit has to be gas we will actually have.
> Our reserves lead says the type curve and the rig schedule tell us everything. Give me the 2027 volume to commit, in Bcf to the nearest
> whole Bcf, in one sentence for the term sheet, and send `incremental_2027.xlsx` with the build and the sheets below, a chart
> `til_timeline.png`, and a one-page `term_sheet_note.md`.

* `incremental_2027.xlsx` — wells by pad with spud, turn-in-line and 2027 volume, the line-loss sheet (ask A) and the owners sheet (ask B).
* `til_timeline.png` — one bar per pad from first spud to turn-in-line, the 17-week interval hatched, the four drilled pads highlighted,
  1 January 2027 marked, and 2027's monthly incremental volume stacked beneath by pad.
* `term_sheet_note.md` — the committed volume, the drilled pads behind it, and why the rig schedule alone understates 2027.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight largest producing pads and each month of the third quarter, the gathering
  line loss (pad meter minus its share of the central delivery meter). *Device:* a pad meter replaced mid-month reports two partial-month
  readings under two meter IDs, linked in the meter-change log, as the measurement manual documents; reading one ID understates three pads'
  volumes and overstates their losses. Producing pads enter no part of the incremental forecast.
* **Ask B (device-carried).** For each of the three counties and each quarter of 2026, the royalty owners paid. *Device:* an interest sold
  or inherited appears under a new owner ID, with the succession in the division-order change table, as the land department's guide
  documents; counting raw IDs overstates owners in every county. Royalty records enter no part of the forecast.
* **Ask C (validity).** The 2027 volume under each of the four rung constructions, and each closed year's incremental volume (2023–2026)
  reproduced by each construction.
* **Decoupling.** Clearing the drilled-pad residual changes no figure in asks A or B.

## 11. Rubric arithmetic

8 pads × 3 months (ask A) + 3 counties × 4 quarters (ask B) + 4 constructions × 2 (ask C) + the committed volume, the 32 drilled wells and
their 2027 volume + 5 named chart parts + 3 files ≈ 55 criteria.

## 12. World-building constraints

* 2027 volume by rung: 60 / 45 / 30 / 130 Bcf (130.4 unrounded). Grid with the drilled pads: 193, 173, 145, 130; partials 150, 163, 82.
* Drilled pads: four of eight wells at 660 feet, last spuds 10 September, 20 October, 30 November and 28 December 2026; turn-in-line
  7 January, 16 February, 29 March, 26 April 2027; 100 Bcf in 2027 on the spacing-adjusted curve, 133 on the pooled one.
* Tight-spaced wells run 25% below the pooled curve; the pooled curve reproduces 2025's programme within 2% and misses every tight pad high.
* Completion log: 26 pads, turn-in-line 16–18 weeks after the last spud; drilling pace 14.6–15.4 days a well against the schedule's 12.
* The twin pads are identical on every spud-register and pad-register column; 7.9 and 3.8 Bcf in 2025.
* Meter changes and owner successions touch no spud, turn-in-line or volume in the forecast.
