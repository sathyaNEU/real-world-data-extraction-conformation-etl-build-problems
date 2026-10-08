# OS09 — What net savings next year's mini-split rebate programme will claim, when its newly registered installers fit most of their systems without anyone filing for the rebate

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · programme evaluation and market transformation |
| Mirrors | Counting the effect of a partner-enablement programme beyond the transactions that carry its tag (Google and Meta partner programmes whose trained agencies run campaigns outside the incentive, Amazon seller-training programmes, Apple developer programmes), where the untagged effect is a residual between partner sell-through and tagged claims |
| Decision shape | One figure committed at a date: next year's net savings, filed in the programme plan |
| Committed call | The programme's net first-year savings next year, in GWh to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S2 (a population found as the residual between two correct records), with the unit the savings rule counts (#2) below it |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #2 counts file rows instead of the real unit · #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: the evaluator's results for the four closed programme years, with verified systems, free-ridership and spillover |
| Driving force | Net savings include spillover, and next year's spillover sits in no record: systems that newly registered independent installers fit without a rebate claim. It is the exact residual, installer by installer, between the distributors' outdoor-unit sales to each registered account and that installer's rebated systems, less its own purchases before it registered. Rebated systems are built from claim lines through the job file. Every closed year shows a residual of zero, because until this year every registered installer was a direct-install contractor obliged to claim every system it fitted. |

## 1. Situation

A utility's ductless heat-pump (mini-split) programme pays a rebate per system, claimed by the customer within 90 days of installation.
Its annual plan must state next year's net first-year savings. The plan sets next year's rebated volume at this year's plus 10%. The
state's technical reference manual deems 3.2 MWh a year per system, and the regulator's order defines net savings as gross savings less
free-ridership plus spillover. This year the programme opened installer registration, previously limited to its direct-install
contractors, to independent installers who complete its training: 40 registered so far, and the training schedule has 150 registered by
1 January. Under a data agreement the three regional distributors report monthly outdoor-unit sales by installer account.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the claim lines, the job file, the evaluator's results, the distributor reports and the
  training schedule. No stakeholder read is overturned. The difficulty is a population of programme-induced systems that no file
  records, recoverable only as a difference between two that do.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice. Rebated systems, the evaluated free-ridership and the plan's volume still produce a clean
  13.4 GWh that the closed years confirm.
* **Instrument repair.** Install a perfect census of every system fitted, with its installer. Nothing in it says which systems the
  programme caused: the answer still subtracts each installer's own pre-registration run-rate, a counterfactual no instrument records,
  and still projects the rate onto 110 installers who have not yet registered.
* **Lens swap.** The naive read is rebated systems. The answer adds a different population, unclaimed systems fitted by newly
  registered installers, found in a different pair of files.

## 3. The driving force

A strong solver counts systems, not claim lines, because the manual deems savings per system. It applies the evaluated free-ridership,
which has held at 30% in all four closed years, and it checks participant spillover, which the evaluator measured at half a percent.
The closed years reproduce, and the figure is 13.4 GWh. But the order counts spillover, and the closed years could not see the kind that
now matters. Direct-install contractors had to claim every system, so their distributor purchases always equalled their rebated systems.
Independent installers do not. The distributor reports show each registered independent buying 3.4 outdoor units a month against 0.84
before registering, while its customers claim 0.90. The other 1.66 systems a month are fitted because of the programme and never
claimed. Across the 150 independents registered for next year that is 2,988 systems.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | This year's claim rows plus 10%, × 3.2 MWh | 49.9 GWh (+117%) | The tracking database's own count, on the deemed value | The manual deems savings per system, and the evaluator's verified system counts are 2.6 claim lines each, 4 of 4 closed years |
| 1 | Rebated systems (lines grouped through the job file) × 3.2 MWh | 19.2 GWh (−16.5%) | The right unit, verified by the evaluator | The order nets free-ridership, evaluated at 30% in every closed year |
| 2 | Rebated systems × 3.2 MWh × 0.70, plus participant spillover | 13.4 GWh (−41.6%) | Reproduces all four closed years' evaluated net savings | The distributor reports: registered independents buy 3.4 units a month against 0.84 before registering, and claim 0.90 |
| 3 | **Decisive:** rung 2 plus installer spillover, each registered installer's purchases less its pre-registration run-rate less its rebated systems, × 150 installers × 12 months × 3.2 MWh | **23.0 GWh** | — | — |

* **Figure shape.** The first two corrections walk the figure down and the decisive move reverses it, so the answer is bracketed: rung 1
  at −16.5% and rung 2 at −41.6% below, rung 0 above.
* **Partial correction priced (L3).** A solver who finds the residual but skips each installer's pre-registration purchases lands at
  27.8 GWh (+21.0%). One who applies it only to the 40 installers registered today lands at 16.0 GWh (−30.5%). One who computes it on claim
  lines finds 0.22 units a month and lands at 36.2 GWh (+57%).
* **Grid.** Unit (lines, systems) × free-ridership (off, on) × installer spillover (off, on) gives 8 cells: 49.9, 51.2, 34.9, 36.2, 19.2,
  28.8, 13.4 and the answer. The nearest wrong cell is rung 1 at −16.5%, and it costs dropping both free-ridership and spillover.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The order says net savings include spillover. It does not say where spillover is found, and the evaluator's
   method measured it by participant survey.
2. **Corpus blind for a computable reason.** *In every closed programme year the installer residual was zero, because every registered
   installer was a direct-install contractor whose contract requires a claim for every system it fits.* Distributor purchases equal
   rebated systems in all 48 closed contractor-years, and the four evaluated years reproduce at rung 2.
3. **No arithmetic symptom.** Claim lines reconcile to systems through the job file, systems to the evaluator's counts, and distributor
   reports to the distributors' own totals.
4. **Not a row predicate.** The residual needs distributor accounts matched to registered installers through the registration file,
   monthly purchases before and after each installer's own registration month, and rebated systems per installer built from claim lines.
5. **The enumeration is arithmetic.** No column marks a system as spillover; nothing records an unclaimed system at all.
6. **No cutover date.** Independents registered one by one through the year, each on its own month, so no aggregate series steps.
7. **Survives deletion.** Removing every voice leaves the closed years certifying rung 2.

## 6. The calibration corpus

* **Form.** The evaluator's results for 2021–2024: claimed and verified systems, free-ridership, participant spillover and net savings,
  with the claims and the distributor reports for those years.
* **What it certifies.** Systems as the unit (4 of 4; claim rows 0 of 4), free-ridership of 0.30 (4 of 4 within 1 point) and net savings
  at rung 2, 4 of 4.
* **What it is blind to.** Installer spillover (above).
* **Twin pair.** Independents Harlow Climate and Quayside Heating registered in the same month, in the same region, from the same
  training cohort, and each buys 3.4 units and has 0.90 claimed a month. Harlow bought 0.6 a month before registering and Quayside 1.5, so
  their spillover is 1.9 and 1.0 systems a month, 1.9× apart. Only each installer's own pre-registration purchases separate them.
* **Resemblance points at the decoy.** By claims a month, the independents look like the smallest direct-install contractors, whose
  residual has always been zero.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The order: net savings are gross savings less free-ridership plus spillover. The manual: 3.2 MWh a year per system,
  a system being one outdoor unit and the indoor heads it serves. The plan: next year's rebated volume is this year's plus 10%. The
  training schedule: 150 independents registered by 1 January.
* **Empirical pins.** Free-ridership, from the closed years. The residual per installer, from the distributor reports and the claims.
* **Voices.** The programme manager: "Our savings are our rebates. If nobody claims, as far as the plan is concerned nothing happened."
  The evaluation lead: "Free-ridership is the only adjustment that has ever moved our numbers."
* **Licensed wrong basis.** The order records that the consumer advocate reviews plans on net savings from rebated systems alone and will
  present that figure at the hearing.

## 8. Determinism by construction

* **Run-rates.** Every independent's monthly purchases are flat before registration and flat from its registration month, so any
  baseline window and any start month give the same residual.
* **Coverage.** The data agreement covers every outdoor unit sold in the territory, and registered installers buy only from the three
  distributors, so no purchase escapes the reports.
* **Maturity.** This year's run-rate uses installations from January to September, whose 90-day claim windows have all closed by the
  extract on 31 December.
* **Systems.** Indoor heads reference the installer's job number and the job file gives each job's outdoor serial, so every line joins to
  exactly one system.
* **Rounding.** The committed figure is 23.00 GWh, mid-bin at one decimal.

## 9. Prompt sketch and deliverables

> The programme plan has to state next year's net savings for the mini-split rebate, in GWh to one decimal, and it goes in on the 20th.
> Our programme manager's view is that if nobody claims a rebate, nothing happened. Give me the figure as a sentence for the plan, with
> `net_savings_build.xlsx`, a chart `installer_residuals.png`, and a short `plan_savings_note.docx`.

* `net_savings_build.xlsx` — the four bases, the closed-year reproduction, the installer residual table, the training sheet (ask A) and
  the load-research sheet (ask B).
* `installer_residuals.png` — a script-rendered dot chart: one row per registered independent, its monthly purchases before and after
  registering and its rebated systems, the residual shaded between them, the direct-install contractors shown as a reference band at
  zero, and Harlow and Quayside labelled.
* `plan_savings_note.docx` — the committed figure and the bridge from rebated net savings to it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of this year's six training cohorts, the share of trainees certified and the mean
  attempts per certified trainee. *Device:* a trainee who re-sits the exam appears again under the same trainee number with an attempt
  count, and the certification guide counts a trainee's best attempt. Counting attempts as trainees understates the pass rate in four
  cohorts.
* **Ask B (device-carried).** For each of the four system sizes, the average winter peak demand per system and the peak-hour load factor
  from the 60 metered homes. *Device:* the meters' November repeated hour is flagged `dst_repeat`, and the meter guide says to average the
  pair. Summing it inflates peak demand for two sizes.
* **Ask C (validity).** Next year's figure under each of the four rung bases, and each closed year's evaluated net savings as reproduced
  on claim lines and on systems.
* **Decoupling.** Setting installer spillover to zero changes no figure in asks A or B. Exam records and load-research meters touch
  neither claims nor distributor reports.

## 11. Rubric arithmetic

6 cohorts × 2 (ask A) + 4 sizes × 2 (ask B) + 4 bases and 4 years × 2 (ask C) + the committed figure, the spillover systems, rebated
systems and the residual rate + 5 named chart parts + 3 files ≈ 44 criteria.

## 12. World-building constraints

* Next year: 6,000 rebated systems (2.6 claim lines each), 3.2 MWh a system, free-ridership 0.30, 150 independents for 12 months.
* Every registered independent: 3.4 units a month after registering, 0.84 before (average), 0.90 claimed; residual 1.66.
* Rung figures 49.9 / 19.2 / 13.4 / 23.0 GWh; partial readings 27.8, 16.0 and 36.2.
* Closed years: distributor purchases equal rebated systems for every registered contractor; free-ridership 0.30 ± 0.01.
* Harlow and Quayside match on every column outside their pre-registration purchases.
* Exam records and load-research meters never touch claims, jobs or distributor reports.
