# DS06 — Which applicant gets the climate fund's anchor award, when only one baseline reproduces every certified reduction in the book

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Nonprofit & Grant-making · climate investment programmes |
| Mirrors | Choosing which project gets a flagship grant or offtake when certified impact depends on the counterfactual life of the replaced asset (Microsoft and Google clean-fleet and carbon procurement, Amazon's climate fund, utility fleet-electrification incentives) |
| Decision shape | Which of N gets one scarce thing: the round's single anchor award |
| Committed call | The applicant that gets the award, and its lifetime reduction in tonnes CO2e per $1,000 of grant, to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B with a reproduction clause (measured #1 and #3), with two grains of the grid emission factor (annual against hourly) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #4 never tests its reading against the control · #14 coarsens the segment it was asked about |
| Calibration form | Existing-book actuals: the fund's 40 funded projects, each with its certified annual reductions and the records of the assets it replaced |
| Driving force | The fund may use a quantification only if it reproduces every certified reduction in its existing book, and the method is written nowhere. The obvious two-stage baseline, with each replaced asset's life read as install year plus standard life, reproduces 33 of 40. All 40 reproduce only when each replaced vehicle's retirement is built from three sources: its register record, its latest re-power certificate, and any model-year phase-out ordinance. That construction cuts the refuse fleet's credit by 60% and almost fully restores the drayage cooperative's. |

## 1. Situation

A state climate fund has one anchor award this round, and six applicants have asked for between $18M and $40M. Under the programme
guidelines the award goes to the applicant with the most lifetime GHG reduction per grant dollar, quantified as the fund certifies it.
The guidelines also say a quantification may be used only if it reproduces, to the tonne, every certified reduction in the fund's existing
book. The book holds 40 funded projects, each with certified reductions and the asset records of what it replaced. The applications give
each project's assets, energy use and charging profiles. The grid operator publishes annual and hourly emission factors. The board likes the
transit electrification because its tonnage is the largest.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the applicants' stated reductions (right
  under their stated method), the published factors, the certified book, the asset register, the re-power certificates and the phase-out
  ordinance. The difficulty is that the certifying method has to be recovered from the book, and its decisive component is built across
  three files.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the board's preference and the applicants' stated figures. Recomputing reductions with the methodology's
  hourly counting and a standard two-stage baseline still names the refuse fleet, and still reproduces 33 of 40.
* **Instrument repair.** Make every meter, register entry and certificate perfect. The method still has to be recovered, and the refuse
  trucks still retire under the ordinance in the project's first year.
* **Lens swap.** The naive read credits each project against its own replaced asset for the project's whole life. The answer credits each
  replaced vehicle only until the date the register, its certificates and the ordinance would have retired it: a different counterfactual
  population of vehicle-years.

## 3. The driving force

A strong solver recomputes every applicant's reduction, counts electricity at the hour it is drawn, as the methodology requires, and
switches to the standard two-stage baseline: old asset against new until the old one would have retired, standard new against new after
that. It reads the old asset's retirement as install year plus standard life. Each step is competent and the book reproduces 33 of 40,
which reads as rounding. The seven misses are not rounding. They are fleets whose vehicles were re-powered (a certificate extends the life)
or whose city adopted a diesel phase-out (an ordinance ends the life by model year). The refuse fleet's 2019 trucks would run to 2037 on
install year, but the city's ordinance retires them in 2027, so its credit falls by 60%. The drayage cooperative's 2008 trucks would be at
end of life now on install year, but they were re-powered in 2021 with certificates to 2037, so its credit rises by 63%. Only the
three-source construction reproduces all 40.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lifetime reduction against the replaced asset at annual average grid factors, per $1,000 of grant | A, transit buses (2.97) | The applicants' own method, recomputed cleanly | The methodology: electricity is counted at the hour it is drawn, and the buses charge overnight on marginal fossil units |
| 1 | Hourly marginal factors weighted by each project's load profile (the two-grains rung) | B, cold-chain warehouse (2.44) | The filed counting rule applied exactly | The reproduction clause: full-life baselines reproduce 9 of the book's 40 |
| 2 | Two-stage baseline, old asset's life = install year + standard life (#3: 33 of 40) | C, municipal refuse fleet (1.84) | A standard counterfactual, and 33 of 40 looks like rounding | The book's seven misses: every one is a re-powered or phased-out fleet |
| 3 | **Decisive:** per replaced vehicle, retirement from the register's install date, the latest re-power certificate and any model-year phase-out; two-stage reductions summed per project (40 of 40) | **E, port drayage cooperative (1.47)** (4th of 6 on rung 0) | — | — |

* **Position table.** The drayage cooperative is 4th on rung 0 (1.69), 3rd on rung 1 (1.52) and 5th on rung 2 (0.90). It leads only rung 3,
  1.23× over the buses (1.19). Rung margins: 1.46, 1.25, 1.54, 1.23.
* **Discriminator dominance.** The refuse fleet carries a 2.04× advantage into rung 3 (1.84 against 0.90). The decisive construction moves
  the drayage cooperative by ×1.63 and the refuse fleet by ×0.40, a relative swing of 4.07. Product: 0.49 × 4.07 = 1.99, which is where the
  pair ends (1.47 against 0.74). The swing is 1.66× the 2.45 it needs (1.2 × the carried 2.04).
* **Partial correction priced (L3).** Taking the register only where it extends a life names the refuse fleet (1.84, 1.26× over the
  drayage cooperative's 1.47). Taking it only where it shortens one names the buses (1.19, 1.24× over the ferry and 1.33× over the drayage
  cooperative's 0.90). Register dates with annual factors name the buses (2.71, 1.66× over the drayage cooperative's 1.63). Every half
  lands on a wrong applicant.
* **Grid.** Factor grain (annual, hourly) × baseline (full life, install-year two-stage, register two-stage) gives 6 cells, naming A, B, A,
  C, A and E. The nearest wrong cell is register dates at annual factors (the buses, 1.66× clear), and it costs one omission: the hourly
  counting rule.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The methodology names a two-stage baseline "until the replaced asset's retirement". No document says how
   retirement is dated, or that certificates and ordinances move it.
2. **The reproducing rule is a construction, not a menu.** Hourly factors with the register-built retirement reproduce 40 of 40 to the
   tonne. The best rival (install-year life) reproduces 33 of 40, and its misses run six low and one high, 11% low on the book's total. The
   winning rule has no parameter to scan. Each vehicle's date comes from a join across the register, the certificate log and the ordinance
   schedule by model year, and is then summed across a project's vehicles.
3. **No arithmetic symptom.** Vehicle counts, fuel volumes and grant sums reconcile under every rung. The 33-of-40 rival misses only on
   fleets nothing marks as special.
4. **Not a row predicate.** Retirement is a per-vehicle maximum and minimum over records in two other files, and the reduction is a
   two-segment sum over vehicles.
5. **The enumeration is arithmetic.** No column says "extended" or "phased out"; the dates fall out of the join.
6. **No cutover date.** The ordinance's effective date falls inside the forward project life, not in any closed outcome series, and nothing
   steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The existing book: 40 funded projects, each with its certified annual reductions by year, its replaced vehicles or equipment,
  and its load profile.
* **What it pins.** Hourly counting with the register-built two-stage baseline: 40 of 40 to the tonne. Install-year two-stage: 33. Annual
  factors with register dates: 22. Hourly full-life: 9. Annual full-life: 4.
* **Twin pair.** Two refuse-truck projects from the 2022 round are identical on every visible column: 24 trucks of model year 2016, 410,000
  litres a year, a $6.0M grant, the same county and the same overnight charging profile. Their certified lifetime reductions are 21,400 and
  10,700 t (2.0×). One fleet was re-powered in 2020 with certificates to 2034, and the other's city adopted the phase-out. Only the
  three-source construction separates them.
* **Every rule exercised.** The book holds re-powered fleets, phased-out fleets, non-electric projects (where the hourly rule is inert), and
  electric projects with day and night profiles.
* **Resemblance points at the decoy.** The drayage application (2008 trucks, port duty, mid-day charging) most resembles the book's three
  oldest-fleet projects, which certified the lowest reductions per dollar.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The guidelines: the award goes to the most lifetime reduction per grant dollar, as the fund certifies it, over a 12-year
  project life. The reproduction clause. The methodology: electricity is counted at the hour it is drawn. One sentence each.
* **Empirical pins.** The retirement construction, from the book.
* **Voices.** The programme director: "Buses carry the most people; electrify them first." A board member: "The biggest tonnage is the safest
  flagship." The fleet adviser: "Install year plus standard life is how every fleet plans replacement."
* **Licensed wrong basis.** The guidelines record that the state treasurer's review reads applications on applicant-stated lifetime
  reductions per dollar and will see that table.

## 8. Determinism by construction

* **Dates.** Projects start on 1 July. Certificates and the ordinance end on 30 June dates, so no year needs prorating.
* **Hourly factors.** The operator's hourly marginal factors for the last full year are weighted by the applications' hourly profiles.
  Fifteen-minute and hourly aggregation agree to 0.3%.
* **Life and rounding.** The 12-year life is filed, and the book reproduces to the tonne only under the winning construction. The 1.23 final
  margin exceeds any rounding of the figure.

## 9. Prompt sketch and deliverables

> We have one anchor award this round and six applicants for it. The board likes the bus electrification because its tonnage is the
> biggest. Tell me which applicant gets the award, with its lifetime reduction in tonnes per thousand dollars of grant to two decimals, in a
> sentence for the award letter. Send `award_case.xlsx`, a chart `reduction_per_dollar.png`, and a one-page `award_memo.pdf`.

* `award_case.xlsx` — the six applicants under each construction, the equity sheet (ask A), the jobs sheet (ask B) and the reproduction
  sheet (ask C).
* `reduction_per_dollar.png` — a slope chart of the six applicants across the four constructions, the chosen applicant highlighted, each
  construction's book hit count printed above its column, and the two fleets the retirement construction moves annotated.
* `award_memo.pdf` — the committed applicant and figure, and why the refuse fleet falls.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each applicant, the share of its service-area population living in designated disadvantaged
  tracts. *Device:* tracts split at the last census are mapped through the published relationship file. Old tract IDs drop 7–9% of the
  population in two applicants' areas.
* **Ask B (device-carried).** For each applicant, grant dollars per job-year created. *Device:* the payroll attachments list part-time posts
  as heads, with an FTE field. Counting heads understates cost per job-year for three applicants by a quarter or more.
* **Ask C (validity).** The book's hit count (of 40) under each of the five constructions, and the six applicants' figures under each rung's
  construction.
* **Decoupling.** Clearing the retirement construction changes no figure in asks A or B. Tracts and payroll never enter a reduction.

## 11. Rubric arithmetic

6 equity shares (ask A) + 6 job-year costs (ask B) + 5 hit counts + 6 × 4 figures (ask C) + the committed applicant, its figure, the
runner-up and the margin + 6 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Per $1,000 of grant (rungs 0–3): buses 2.97 / 1.45 / 1.19 / 1.19; cold chain 2.03 / 2.44 / 0.93 / 0.93; refuse 1.98 / 1.95 / 1.84 / 0.74;
  ferry 1.59 / 1.22 / 0.96 / 0.96; drayage 1.69 / 1.52 / 0.90 / 1.47; schools 1.00 / 0.95 / 0.86 / 0.86. Grants ($M): 40 / 24 / 30 / 22 /
  34 / 18. Annual tonnes for old asset, new asset at annual factors, new asset at hourly factors and standard new asset: buses 11,000 /
  1,110 / 6,160 / 8,940; cold chain 6,000 / 1,932 / 1,110 / 2,700; refuse 6,600 / 1,650 / 1,722 / 3,290; ferry 3,300 / 390 / 1,072 /
  2,177; drayage 6,600 / 1,812 / 2,285 / 4,676; schools 2,400 / 900 / 975 / 2,115.
* Remaining life of the old asset in years, install-based then register-based: buses 7 / 7, cold chain 1 / 1, refuse 11 / 1, ferry 7 / 7,
  drayage 1 / 11, schools 6 / 6.
* The book: 40 projects reproducing 40 / 33 / 22 / 9 / 4 under the five constructions. The twin projects are identical on every visible
  column.
* Tracts and payroll records never touch vehicles, certificates, factors or reductions.
