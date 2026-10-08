# FC36 — How much more road salt the city commits above its rolled-over contract, when the bus network redesign moved 424 lane-kilometres of collectors to bare-pavement treatment after the last winter closed

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · municipal public works (winter road maintenance) |
| Mirrors | Committing seasonal supply after part of the served network moved to a heavier service level between seasons (the seasonal rock-salt programmes Cargill, Compass Minerals and Morton Salt run with state transport departments and cities, where the buyer commits its tonnage each summer and is held to most of it, placed after routes have been re-tiered; telecom carriers' winter-peak capacity commitments after a summer of site upgrades) |
| Decision shape | One figure committed at a date: the additional salt committed by 1 October above the contract that rolls over at last winter's tonnage |
| Committed call | The additional rock salt for November to March, in tonnes to the nearest hundred |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · maturity (the redesigned streets' first Priority 1 winter crystallises after the extract, and only the route register holds it), with a latent attribution marker (measured #17) at rung 2 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #17 guesses an attribution the data can settle · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Revision log: the route-audit revision log, each reclassification cohort's salt per lane-kilometre as rated at request, revised at the pre-season audit and confirmed against the following winter's spreader records |
| Driving force | A street's salt is set by its treatment class, and a street moved to Priority 1 takes bare-pavement salt only from its first winter there. The bus network redesign of 30 August put frequent service on 424 lane-kilometres of Priority 2 collectors, which the snow and ice policy makes Priority 1, after the last winter closed, so not one of them has a Priority 1 event in the spreader records; every closed winter is fully developed and every model fitted to them ties. Their first-winter salt is in the route register, rated at the September audit at 25.8 tonnes a lane-kilometre against 12.5 at Priority 2, and the revision log shows audit ratings confirmed by the following winter's spreader records since 2023. The spreader records carry no class; earlier reclassifications show only as bare-pavement confirmations from their first Priority 1 winter. |

## 1. Situation

A northern city's public works department buys its rock salt under a supply contract that rolls over each 1 October at last winter's
delivered tonnage, 39,100 t for November to March, which matched the salt spread. Anything above that must be committed as a separate
seasonal tonnage by 1 October; salt beyond it is bought at the supplier's spot price. The snow and ice policy treats arterials and every
street with frequent bus service as Priority 1, cleared to bare pavement after every event, and collectors as Priority 2, salted at
intersections, hills and curves. On 30 August the regional transit agency launched its redesigned bus network, which moved frequent
service onto 424 lane-kilometres of collectors. The pack holds five winters of GPS spreader records by route section, the severity index
the city files each winter, the route register with each section's current class and the September audit's ratings for the sections it
re-rated, the route-audit revision log, the council-petition list, depot time sheets and shift assignments, contractor invoices, the
materials-planning tool's model ranking, and the operations team's usage model with its back-tests.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the spreader records, the severity index, the route register and the revision log. The operations
  team's model really has back-tested within 1% for five winters. No reported number is overturned; the difficulty is salt that belongs to
  the coming winter and that no closed winter contains.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the operations team's confidence and every voice. A severity-and-trend model on the spreader records still
  ties every closed winter, and still sees nothing of the redesign.
* **Instrument repair.** Clean-data test. One field is missing: the spreader records carry no class, and the route register keeps only
  each section's current class, so class history comes from the bare-pavement confirmations; the records themselves are complete, every
  pass and tonne logged. Repaired at every depth, up to a pass log that carries each section's class at the time and a register with dated
  class history, rung 0 still returns 1,800 t, rung 1 400 t and rung 2 −700 t (it finds the same reclassified sections), none of them
  5,000, and the redesign's first winter is still needed, because its 424 lane-kilometres have had no winter at Priority 1 and no record
  of a closed winter can hold one.
* **Lens swap.** The naive read and the answer are different moments for the same streets: the 424 lane-kilometres as they were last
  winter, collectors salted at intersections and hills, against the same streets this winter, bus routes cleared to bare pavement.

## 3. The driving force

A strong solver normalises last winter to the severity normal, selects the model whose five-month totals back-test best, and forecasts the
coming winter. Seeing that the total's growth has come from reclassified sections rather than from the network in general, it dates each
reclassification by its bare-pavement confirmations, projects reclassified and never-reclassified sections separately, and finds the
never-reclassified falling 1% a year. Every step is correct, and every closed winter reproduces. The reclassifications it separates are
the ones whose winters are already in the records. A section's Priority 1 salt first appears in its first winter at Priority 1, so the
sections moved on 30 August are invisible in every record they have produced: those records show collectors salted at intersections, hills
and curves. The route register holds every section the redesign moved with its audited Priority 1 rating, and the revision log shows that
since audits began in 2023 those ratings have matched the next winter's normalised spreader tonnes to within 1%. Replacing those sections'
Priority 2 projection (5,247 t) with their audited first winter (10,939 t) adds 5,692 t that no model fitted to the records can produce,
and the commitment is 5,000 t.

## 4. The ladder

| Rung | Construction | Lands on (additional salt) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The materials tool's one-month winner: seasonal naive with drift (+4.6%) on last winter's actual | 1,800 t (−64%) | The tool's own model choice, and it tracks the series month to month | The tool ranks models on one-month error; the commitment is a five-month total, and on five-month totals the severity-and-trend regression wins every back-test |
| 1 | Severity-and-trend regression selected on five-month totals, at normal severity | 400 t (−92%) | Horizon-matched selection and severity normalisation: back-tests within 1% on all five closed winters | Priority 1 sections carry a bare-pavement confirmation after every event; dating each reclassification by them, the total's trend (+1.8% a year) is reclassifications, and sections never reclassified fall 1.0% a year |
| 2 | Reclassified and never-reclassified sections separated by their bare-pavement confirmations, each section projected on its own history at its class | −700 t (no additional salt) | Attributes the growth to its source; the organic decline is real and every reclassified section's salt is carried | The route register: 424 lane-kilometres moved to Priority 1 for the coming winter, every section rated at the September audit and none with a Priority 1 winter in the spreader records |
| 3 | **Decisive:** the redesign's sections at their audited Priority 1 ratings (424 lane-km × 25.8 t) in place of their Priority 2 projection | **5,000 t** | — | — |

* **Figure shape.** The corrections walk the commitment down (1,800, 400, −700) and the decisive rung reverses past rung 0, so a solver
  who stops anywhere short under-commits and buys the gap at the spot price.
* **Partial correction priced (L3).** A solver who finds the register but uses request ratings (31.0 t a lane-kilometre at the standard
  application rate, the kind of rating the revision log shows running 18–22% high before audits began) commits 7,200 t (+44%). One who
  adds the audited sections to the rung 1 regression, whose trend already carries a typical year's reclassifications, commits 6,000 t
  (+20%).
* **Grid.** Base (one-month winner, season regression, sections separated) × redesign sections (none, request ratings, audit ratings) ×
  their Priority 2 salt (removed, left in) = 15 cells, landing between −700 and 14,900 t. Every wrong cell sits at least 1,000 t (20%)
  from 5,000; the nearest is the audited sections added to the regression (6,000), which takes keeping a trend the marker has already
  attributed.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The snow and ice policy defines the classes, and the transit agency's notice lists the new frequent routes. No
   document links the route register to salt purchasing or says a reclassified street's salt changes with its first winter at its new
   class.
2. **Corpus blind to the cohort.** *In every closed winter the lane-kilometres reclassified since the winter before numbered at most 90,
   because reclassification came one bus corridor at a time until the redesign moved 424 at once; each such cohort sat inside the trend
   the regression back-tests on.* Every closed winter is fully developed, and none holds a cohort of 424.
3. **No arithmetic symptom.** Spreader tonnes reconcile to dome draws and deliveries, severity normalisation reproduces each closed
   winter, and the register's lane-kilometres match the street inventory.
4. **Not a row predicate.** The forward tonnage is a sum over a register the spreader pipeline never joins, section by section, replacing
   each re-rated section's Priority 2 projection with its audit rating, on top of projections that need every section's class history
   recovered first.
5. **The enumeration is arithmetic.** No spreader column marks a 2026 reclassification; the redesign's sections carry no bare-pavement
   confirmation because they have had no winter at Priority 1.
6. **No cutover date in any outcome series.** The redesign launched on 30 August, but nothing it caused has reached a spreader record: the
   sections' first Priority 1 winter is the coming one.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The route-audit revision log for the 2021–2025 reclassification cohorts: each cohort's lane-kilometres and salt per
  lane-kilometre as rated at request, as revised at the pre-season audit (from 2023), and as confirmed by the following winter's
  normalised spreader tonnes.
* **What it certifies.** That audit ratings matched the following winter within 1% for the 2023, 2024 and 2025 cohorts, so the register's
  audited 2026 ratings are the ones to use; and that request ratings, at the standard application rate, ran 18–22% high for the 2021 and
  2022 cohorts, because they assume full passes where a section shares intersections and turnarounds with existing Priority 1 routes.
* **The settled attribution case (E19).** The 2025 cohort's normalised first-winter increase (1,140 t) reproduces only when reclassified
  sections are identified by their bare-pavement confirmations; the council-petition list, which holds only the reclassifications
  residents petitioned for, finds 61% of them.
* **Twin pair.** Sections 4417 and 4492 are identical on every spreader-record column through September 2026: 3.9 km of two-lane collector
  each, Priority 2 in all five winters, the same depot and passes per event, 97.5 t normalised last winter, and no bare-pavement
  confirmation. Their forecast winter salt differs 2.1× (96.5 t and 201 t), because the redesigned network runs frequent buses on 4417
  from 30 August and not on 4492. Only the route register separates them.
* **Resemblance points at the decoy.** By severity and network length, the coming winter most resembles the 2023–24 winter, which the
  regression reproduced to 0.4%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The supply contract: it rolls over each 1 October at last winter's delivered tonnage (39,100 t), any increase is
  committed as a separate seasonal tonnage by 1 October, and salt beyond the commitment is bought at the supplier's spot price. The
  commitment is set at the forecast November-to-March salt at normal severity, less the rolled-over tonnage. Normal severity is the
  thirty-year normal of the index the city files with the state. The snow and ice policy: Priority 1 for arterials and every street with
  frequent bus service, Priority 2 for collectors.
* **Empirical pins.** The redesign's sections at their audited ratings, validated by the revision log. Each earlier reclassification's
  first Priority 1 winter, from the bare-pavement confirmations. The organic trend, from never-reclassified sections.
* **Voices.** The winter operations manager: "Our usage model has called every winter we've run it on." The transit agency's liaison: "The
  new network runs on streets your crews already treat." The finance director: "Commit what the model says and not a tonne more."
* **Licensed wrong basis.** The state purchasing cooperative's rules record that a member's commitment above its rolled-over tonnage is
  reviewed against the member's filed usage regression, and the city's will be checked on that basis.

## 8. Determinism by construction

* **Reclassification timing.** Every 2026 move took effect on 30 August, after last winter's final event on 28 March, so no part of any
  section's Priority 1 salt is in the records under any reading of the season.
* **Season.** Each audit rating is a November-to-March figure at normal severity, so no allocation across months is needed.
* **Organic trend.** Never-reclassified sections' normalised salt fell 0.9–1.1% in each of the last five winters, so window choice does
  not move it.
* **Severity.** The thirty-year normal is filed; a twenty-year normal moves the commitment by under 100 t.
* **Maturity.** The register is complete for the redesign: the September audit rated every section it moved and closed on 25 September,
  before the extract.
* **Rounding.** The commitment lands at 5,004 t, 46 t inside the nearest rounding boundary.

## 9. Prompt sketch and deliverables

> Our salt contract rolls over at last winter's 39,100 tonnes on 1 October, and anything more has to be committed by then. The operations
> team is confident its usage model has the winter called. Tell me how much more salt to commit, in tonnes to the nearest hundred, in a
> line I can take to the purchasing committee, and send `salt_commitment.xlsx` with the build and the sheets below, a chart
> `winter_salt_build.png`, and a one-page `commitment_memo.pdf`.

* `salt_commitment.xlsx` — the winter salt build by component, the plough-hours sheet (ask A) and the contractor-hours sheet (ask B).
* `winter_salt_build.png` — stacked bars for the last five winters and the coming one: never-reclassified sections, earlier-reclassified
  sections and the redesign's sections, with the 39,100 t rolled-over line, the regression's forecast as a marker, and the commitment
  annotated as the gap.
* `commitment_memo.pdf` — the committed tonnage and why the back-tested model cannot see it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six depots and each month of last winter, the plough-down hours its trucks
  worked. *Device:* a truck lent mid-shift to another depot's route keeps its home depot on the time sheet, with the borrowing depot in
  the shift-assignment table, as the fleet guide documents; reading the time sheet alone credits borrowed hours to the lending depot at
  four depots. Plough hours enter no part of the salt build, which runs on spreader tonnes.
* **Ask B (device-carried).** For each of the three residential ploughing contracts and each month of last winter, the contractor hours
  paid. *Device:* a contractor invoices per storm event, and an event that spans a month end is split across the months in the payment
  schedule by hours worked, as the contract documents; dating each invoice line by its invoice date puts whole events in the wrong month
  under every contract. Contract ploughing is on residential streets that take no salt.
* **Ask C (validity).** The commitment under each of the four rung constructions, and each construction's back-test error on the five
  closed winters.
* **Decoupling.** Clearing the redesign's sections changes no figure in asks A or B.

## 11. Rubric arithmetic

6 depots × 5 months (ask A) + 3 contracts × 5 months (ask B) + 4 constructions × 2 (ask C) + the committed tonnage, the redesign's
first-winter salt and the organic trend + 5 named chart parts + 3 files ≈ 64 criteria.

## 12. World-building constraints

* Last winter: 39,100 t spread and delivered (0.8% more severe than normal), 38,800 t normalised: never-reclassified sections 28,400 (the
  redesign's sections 5,300 of it, at 12.5 t a lane-kilometre), earlier-reclassified sections 10,400. The coming winter at normal
  severity: 22,869 + 10,296 + 10,939 = 44,104 t, a commitment of 5,004.
* Cohorts: 70–90 lane-kilometres a year in 2021–2025, the 2025 cohort 86; 424 in 2026, moved on 30 August; 25.8 t a lane-kilometre
  audited, 31.0 at request.
* Commitment by rung: 1,800 / 400 / −700 / 5,000; request ratings 7,200; the audited sections on the regression 6,000. Every wrong cell at
  least 1,000 t away.
* The tool's drift (+4.6%) comes from the mild 2021–22 winter (12% below normal) at the start of the history; the regression's trend is
  +1.8% a year, and every section's normalised salt at a constant class falls 1.0% a year.
* Revision log: audit ratings within 1% of the following winter for 2023–2025; request ratings 18–22% high for 2021–2022.
* The twin sections are identical on every spreader-record column through September 2026.
* Time sheets, shift assignments and contractor invoices touch no spreader tonne or section used in the build.
