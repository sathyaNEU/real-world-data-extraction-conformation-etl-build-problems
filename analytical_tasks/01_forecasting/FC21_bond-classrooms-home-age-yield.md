# FC21 — Where the bond's 24 new classrooms go across seven elementary schools, when the most crowded school has already peaked

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · school facilities planning |
| Mirrors | Placing capacity where demand will mature rather than where it last peaked (Amazon delivery-station capacity by neighbourhood build-out, broadband and cloud capacity for new subdivisions or tenant cohorts, utilities' load forecasts by subdivision age, retail store staffing as a catchment's households age) |
| Decision shape | An allocation under a cap: 24 bond-funded classrooms across seven elementary schools, at most eight per site |
| Committed call | Classrooms for each of the seven schools, adding to 24, as the bond's placement schedule |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern A (past exceedance against forward yield), with the moderator in how each school year treats a home (the pupils a home yields at its age), and an implicit join through plat and lot numbers below it |
| Gate G mechanism | forecasting, with binding_constraint support |
| Measured traps engaged | #18 joins only on the visible key · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Settled-transaction ledger: the county's school impact-fee ledger, every fee settled at a home's certificate of occupancy since 2008, including each prepaid plat's credit draws by lot |
| Driving force | The overcrowding report is right that Brookside has run at 130% of capacity, and its growth was real. But a home's elementary pupils climb for seven years after occupancy and then fall, and Brookside's 1,100 homes are five to eight years old. Its enrolment peaks now and falls through the bond's window. The next growth sits in homes too young to show it: Dunmore's 1,000 homes occupied in the last three years, and Fairfield's 1,300 lots. Home ages come from the impact-fee ledger, where a prepaid plat's homes post as credit draws on the plat's retired master parcel and reach their own parcels only through the subdivision register. |

## 1. Situation

A suburban district passed a bond that funds 24 classrooms, built in the coming year and in use for the five school years after. The
facilities standard places them school by school in descending order of average projected enrolment over those five years above rated
capacity (24 pupils a classroom). Each school is topped up to its need, rounded up, with at most eight per site, until the 24 are placed.
The district has no filed projection method. The developer-agreement template uses 0.45 elementary pupils per new single-family home.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the October enrolment counts, the facilities inventory, the impact-fee ledger, the subdivision
  register, the student file and the overcrowding report. No one's claim about their own numbers is overturned. The difficulty is which
  homes will send pupils through the bond's window, and how many each sends at its age.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the facilities committee's report. Cohort survival with the pipeline at 0.45 a home still
  gives Brookside eight classrooms and Glenview none.
* **Instrument repair.** Count every pupil and home perfectly. Brookside's pupils are really there, and Dunmore's are not yet. No better
  record of past Octobers shows that the first set will leave and the second will arrive.
* **Lens swap.** The naive read and the answer differ in moment: each school's enrolment as it has run, against the pupils each home will
  yield at the ages it will reach in years two to six.

## 3. The driving force

A strong solver joins the pipeline of platted lots to zones, finds the lots a parcel join drops, and projects enrolled pupils by cohort
survival, which every closed year rewards: in the record, every school's three-year trend carried on. That is the past speaking. A
home's elementary yield is set by its age. Joining the ledger's occupancy dates to the student file shows 0.15 pupils in a home's first
year, 0.60 by its seventh, and 0.30 after its thirteenth. Brookside's growth came from 1,100 homes now five to eight years old, at the top
of that curve, so its enrolment runs from 870 in year two to 646 in year six. Dunmore's 1,000 homes are two years old or less, so its
enrolment climbs from 654 to 857 as their children reach school age. Fairfield's 1,300 lots start at 0.15 and are not all occupied until
year five, so the flat 0.45 a home over-counts them early. Every home's age comes from the impact-fee ledger. The homes in prepaid plats
post as credit draws on master parcels that the parcel layer retired, so only the subdivision register's plat-and-lot index places them.

## 4. The ladder

| Rung | Construction | Lands on (Ashby · Brookside · Cedar Hill · Dunmore · Elm Park · Fairfield · Glenview) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Current enrolment held, plus 0.45 pupils per platted lot not yet occupied, lots placed in zones by a parcel join from the ledger | 0 · 8 · 4 · 0 · 4 · 0 · 8 | The district's own yield on the development pipeline, every pupil counted | **E20 (an implicit join):** the ledger guide: a prepaid plat's homes post as credit draws on the plat's master parcel, retired when the plat was recorded, so a parcel join silently drops Fairfield's 1,300 lots and Dunmore's 1,000 homes |
| 1 | The same with prepaid homes and lots placed through the subdivision register's plat-and-lot index | 0 · 8 · 0 · 0 · 0 · 8 · 8 | Every lot in the pipeline found, the yield applied | The enrolment history: Brookside rose from 729 to 901 and Dunmore from 270 to 497 in three years, so holding enrolment flat ignores growth under way |
| 2 | Cohort survival of enrolled pupils on each school's own three-year grade ratios, plus the pipeline at 0.45 a lot | 0 · 8 · 0 · 8 · 0 · 8 · 0 | The textbook enrolment method, and every closed year's trend carried on | The ledger's occupancy dates joined to the student file: pupils per home rise to 0.60 at year seven and fall to 0.30 after year thirteen; Brookside's homes are five to eight years old and Dunmore's two or less |
| 3 | **Decisive:** every home's pupils in years two to six from its own age on the yield curve (occupied homes and pipeline lots alike, ages from the ledger through the plat index) | **0 · 1 · 0 · 8 · 0 · 8 · 7** | — | — |

* **Figure shape.** Brookside, which the overcrowding report ranks first, takes eight classrooms on every lower rung and one at the
  decisive rung. No other cell gives it fewer than three, so the answer is its extreme cell. Glenview runs 8, 8, 0, 7.
* **Partial correction priced (L3).** The yield curve on the parcel join, with prepaid homes left at today's pupils and their lots
  unseen, gives 1 · 3 · 1 · 1 · 2 · 0 · 7 and holds nine classrooms, because Fairfield and Dunmore vanish. The curve on pipeline lots
  only, with today's enrolment held, gives 0 · 8 · 0 · 0 · 2 · 8 · 6: Brookside keeps 8 on a need of 8.6 against the answer's 3.0. Cohort
  survival for enrolled pupils with the curve on the pipeline gives rung 2's 0 · 8 · 0 · 8 · 0 · 8 · 0.
* **Grid.** Lot placement (parcel, plat index) × enrolled pupils (held, cohort survival, yield curve) × pipeline (0.45 a lot, yield
  curve) gives 12 cells. Only the plat index with the yield curve on both homes and lots gives the answer; every other cell gives
  Brookside three or more classrooms or Fairfield none.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The template's 0.45 is a single number. No document says a home's yield depends on its age, that Brookside has
   peaked, or that prepaid plats need the register; the ledger ships for the developer-fee ask.
2. **Corpus blind for a computable reason.** *In every closed year each school's three-year trend continued, because the only homes old
   enough to be past their peak yield were small 2008–2012 subdivisions spread across three zones, too small to turn any school.* Cohort
   survival back-tests within 3% on every closed school-year.
3. **No arithmetic symptom.** Enrolment ties to the October counts, homes to the ledger, lots to the register and capacity to the
   inventory, under every rung. Nothing fails a reconciliation.
4. **Not a row predicate.** No home is filtered. Each home's pupils in each year come from its age through a curve, and the homes in
   prepaid plats reach their parcels and ages only through a two-file join.
5. **The enumeration is arithmetic.** Which schools rise and which fall in years two to six is computed from home ages. No column says
   "peaked".
6. **No cutover date.** Occupancy dates spread over twelve years; no series steps, and Brookside's decline lies wholly in the forward
   window.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The impact-fee ledger: every fee settled at a certificate of occupancy since 2008 (one row per home, with parcel and date),
  plus each prepaid plat's prepayment and the credit draws that post as its homes are occupied, keyed by master parcel and lot.
* **What it certifies.** Joined to the student file by parcel, the yield of a home by age: 0.15, 0.22, 0.30, 0.38, 0.46, 0.53, 0.58,
  0.60 in years one to eight, falling through 0.53, 0.47, 0.41 and 0.36 to 0.30 from year thirteen. The decline is traced by the small
  2008–2012 subdivisions, now twelve to sixteen years old.
* **Twin pair.** Subdivisions P-14 (in Brookside's zone) and P-27 (in Ashby's) are identical on every column the planning template
  reads: 600 single-family homes, the same lot sizes, and 180 elementary pupils each at the 2019 count. In 2024 they had 360 and 180
  (2.0×), because P-14's homes were two years old in 2019 and P-27's thirty. A flat yield per home gives both one figure.
* **Resemblance points at the decoy.** Dunmore today resembles Brookside four years ago on every enrolment column, and Brookside's
  enrolment then kept growing, which reads as proof that trends carry on.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The facilities standard: classrooms go in descending order of average projected enrolment above rated capacity over
  the five school years after construction, each school topped up to its need rounded up, at most eight per site. The bond: 24 classrooms,
  built in the coming year. The facilities inventory: rated classrooms per school. The ledger guide: a prepaid plat's homes post as credit
  draws on the plat's master parcel with their lot numbers.
* **Empirical pins.** The yield curve, from the ledger and the student file. Home ages, from occupancy dates. Lot-to-parcel links, from
  the subdivision register.
* **Voices.** The facilities committee chair: "Brookside has been bursting for three years; it comes first." The planning director: "New
  homes bring 0.45 kids each. That number has never let us down."
* **Licensed wrong basis.** The standard records that the board's facilities committee reviews requests against the overcrowding report
  (each school's enrolment over capacity in the last three Octobers) and will see the bond schedule beside it.

## 8. Determinism by construction

* **Window.** Construction takes the coming year, so the window is years two to six, as the bond schedule states.
* **Need.** Average enrolment above capacity in classrooms of 24, unrounded, then rounded up for the top-up; under the answer the order
  gaps are at least 1.6 classrooms and Glenview's need is 6.4, so no rounding convention moves a classroom.
* **Ages.** A home's age at each October count is whole years since its certificate of occupancy; pipeline lots enter at age zero in their
  scheduled year from the register's recording dates.
* **Older homes.** Homes occupied before 2008 carry year-built dates in the parcel layer and sit at the curve's long-run 0.30.
* **Maturity.** Every October count in the record is final, and the ledger is complete through the extract.

## 9. Prompt sketch and deliverables

> The bond pays for 24 classrooms and I take the placement schedule to the board on Tuesday: how many each of our seven elementary schools
> gets. Our facilities committee chair is certain Brookside comes first. Send me `classroom_allocation.xlsx`, a chart
> `enrolment_paths.png`, and a two-page `board_paper.pdf` that commits to the seven numbers.

* `classroom_allocation.xlsx` — the projection by school and home cohort under each construction, the attendance sheet (ask A) and the
  class-size sheet (ask B).
* `enrolment_paths.png` — each school's enrolment for the last five Octobers and projected for years two to six as lines, rated capacity
  as a dashed line per school, Brookside and Dunmore highlighted, the yield-by-age curve as an inset, and the allocation as labelled bars.
* `board_paper.pdf` — the committed allocation, why Brookside gets one classroom, and the overcrowding report the committee will hold.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each school, last year's chronic-absence rate (pupils missing at least 10% of the days they
  were enrolled). *Device:* the state attendance manual measures absence over each pupil's own enrolled days. Dividing by the full 180-day
  year understates chronic absence at the two schools with the most mid-year arrivals.
* **Ask B (device-carried).** For each school, last year's classrooms in use and average class size in grades K–3 and 4–5. *Device:* a
  combined-grade class appears once per grade in the scheduling file under one section ID. Counting rows double-counts the split classes
  at three schools. Capacity comes from the facilities inventory, never from the scheduling file.
* **Ask C (validity).** The allocation under each of the four rung constructions, with each one's back-test on the 2019 counts projected
  to 2024.
* **Decoupling.** Replacing the yield curve with 0.45 a home changes no figure in asks A or B.

## 11. Rubric arithmetic

7 schools × 2 (ask A) + 7 schools × 3 (ask B) + 7 schools × 4 constructions (ask C) + the seven committed allocations and Brookside's need
+ 5 named chart parts + 3 files ≈ 79 criteria.

## 12. World-building constraints

* Capacity (rooms × 24) and current enrolment: Ashby 648/657, Brookside 696/901, Cedar Hill 600/616, Dunmore 480/497, Elm Park 576/618,
  Fairfield 384/292, Glenview 480/477.
* Homes: Brookside 1,100 aged five to eight; Dunmore 1,000 aged zero to two (prepaid plat); Fairfield 150 new homes and 1,300 prepaid lots
  occupied over years one to five; Glenview 490 conventional lots over years one to four; the rest mostly homes over thirteen years old.
* Needs under the answer (classrooms): Dunmore 12.3, Fairfield 10.8, Glenview 6.4, Brookside 3.0, Elm Park 1.3, Cedar Hill 1.0, Ashby 0.0.
  Brookside's projected enrolment runs 870, 818, 756, 694, 646; Dunmore's 654, 730, 796, 842, 857.
* Rung allocations as in the ladder. P-14 and P-27 are identical on every template column.
* Mid-year arrivals and split classes never touch homes, lots, the ledger or rated capacity.
