# OS03 — How many injury crashes the 50-intersection redesign avoids in its first year, when a standing signal review was going to reach many of them anyway

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · municipal road-safety programmes |
| Mirrors | Sizing the benefit of treating the worst-performing units when part of their excess resolves without you, because a standing process will reach them anyway (retention offers to top-decile churn-risk accounts that a lifecycle campaign already touches, reliability sprints on the worst services that an automatic remediation job already sweeps at Google or Meta, shrink programmes in stores already due a routine audit) |
| Decision shape | One figure committed at a date: the programme's first-year avoided injury crashes, stated in the safety-grant application |
| Committed call | Injury crashes the redesign programme avoids in 2026, its first full year, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S10 (the governing verb is causal, so the baseline is constructed from a standing review), with Pattern B for the review's trigger and a binding build capacity (#10) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #10 notes a binding limit as a risk · #4 never tests its reading against the control |
| Calibration form | Revision log: the signal unit's timing-plan revision log, 120 corridor retimings over 2017–2024 with the plan each one replaced |
| Driving force | The grant counts crashes the programme avoids against what would happen without it. Without it, the signal unit still retimes the fifteen highest-ranked coordinated corridors every January. Which redesign sites that review reaches is a corridor-level rank with a four-year cooldown, reached through each site's controller and coordination plan, stated nowhere and recoverable only from the revision log. At a reached site the redesign adds only the gap between its own effect and the retiming's. |

## 1. Situation

A city's transportation department will redesign the 50 intersections with the most injury crashes over 2022–2024: 32 signalised
and 18 unsignalised. The federal safety-grant application, due 14 November, must state the injury crashes the programme avoids in
2026, its first full year. The budget request sized the benefit as 30% of the sites' observed crashes, using the state's crash
modification factor for the redesign. The signal unit separately reviews and retimes coordinated corridors every year. The traffic
engineer believes the worst intersections will keep producing crashes at their current rate until they are rebuilt.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the crash records, the state's calibrated safety performance functions, the crew register,
  the construction schedule and the revision log. No stakeholder read is overturned. The difficulty is the baseline the causal verb
  needs, which includes what another standing process will do to the same intersections.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the budget request's figure and the engineer's belief. Empirical-Bayes expectations and the build schedule
  still produce a confident 46.4, and nothing in the pack connects the retiming review to the grant.
* **Instrument repair.** Geocode every crash perfectly and observe every site for a decade. The expectations sharpen and the review
  still retimes the same corridors next January.
* **Lens swap.** The naive read compares the redesign against an untouched intersection. The answer compares it against the
  intersection as the city's own standing process will leave it in 2026, a different counterfactual population.

## 3. The driving force

A strong solver knows sites selected on three bad years regress, so it computes empirical-Bayes expectations from the state's
calibrated functions. It reads the crew register, sees that three signal crews rebuild six intersections each a year, and prorates
the benefit to the months each site is in service. That figure, 46.4, is careful and complete in every visible step. But the grant
counts what the programme avoids. Every January the signal unit retimes the fifteen coordinated corridors with the most injury crashes
over the trailing 36 months, skipping any retimed in the last four years. Eleven of the eighteen signalised sites rebuilt in 2026 sit
on corridors that review reaches, and retiming alone removes 15% of their crashes. There the redesign avoids only the further 15%.
The review's rule is written nowhere. It is the only rule that reproduces all 120 past retimings.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | 30% of the 50 sites' observed annual injury crashes (1,500 over three years) | 150.0 (+289.5%) | The state's factor on the city's own counts, as the budget request did | The state's calibrated functions: sites picked on extreme counts expect 310 crashes a year, 38% below their observed 500 |
| 1 | 30% of the empirical-Bayes expected crashes at all 50 sites | 93.0 (+141.5%) | Regression to the mean removed with the state's own functions | The crew register: three signal crews rebuild six intersections each a year, so 14 signalised sites are not in service in 2026 |
| 2 | 30% of expected crashes, prorated by each site's months in service in 2026 | 46.4 (+20.4%) | Every visible constraint applied, every number reconciled | The revision log: 11 of the 18 rebuilt signalised sites sit on corridors the standing review retimes in January 2026 |
| 3 | **Decisive:** as rung 2, but at reached sites the programme avoids only the redesign's effect beyond the retiming's (0.30 − 0.15) | **38.5 injury crashes** | — | — |

* **Figure shape.** Every correction walks the figure down and the answer is the minimum cell. The decisive move removes 16.9% of the
  rung-2 figure.
* **Partial correction priced (L3).** A solver who sees the review but recovers it with corridor totals over 24 months (96 of 120
  retimings) reaches 4 rebuilt sites and lands at 43.9 (+13.9%). One who ranks intersections rather than corridors (71 of 120) reaches
  all 18 and lands at 34.0 (−11.8%), so the two failure directions bracket the answer.
* **Grid.** Expectation (observed, empirical Bayes) × build capacity (ignored, applied) × standing review (ignored, applied) gives 8
  cells: 150.0, 122.9, 93.0, 76.2, 74.8, 62.1, 46.4 and the answer. The nearest wrong cell is rung 2 at +20.4%, and it costs ignoring
  the review.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The signal unit's procedures say corridors are reviewed on crash performance. No document gives the trigger, and
   none links the review to the grant's baseline.
2. **Reproduction, not a menu.** The rule (sum injury crashes over each coordinated corridor's member intersections for the 36 months
   to 30 September, rank all corridors citywide, take the top fifteen, skipping any retimed in the last four years and taking the next)
   reproduces 120 of 120 retimings. The best rival reproduces 96. Membership comes from effective-dated coordination plans reached
   through each intersection's controller, and the cooldown is visible only in the skipped ranks, so no single column or threshold
   sweep reaches it.
3. **No arithmetic symptom.** Crashes reconcile to the state file, expectations reproduce the state's published site table, and the
   schedule's in-service months sum to the crew register's capacity.
4. **Not a row predicate.** Reach needs a group (corridor), a citywide rank, an exclusion by each corridor's retiming history, and a
   join from site to controller to plan.
5. **The enumeration is arithmetic.** No column flags a site as due for retiming; reach is computed for 214 corridors.
6. **No cutover date.** The review is an annual standing process. The decisive quantity is which sites it reaches, computed from a rule,
   and no redesign site's crash series steps on any date.
7. **Survives deletion.** Removing the budget request and the voices leaves the careful rung-2 pipeline intact and wrong.

## 6. The calibration corpus

* **Form.** The revision log: 120 corridor retimings (fifteen a year, 2017–2024), each with its effective date, the plan replaced and
  the corridor's member controllers, alongside the crash file and the coordination plans.
* **What it pins.** The review's trigger (above), 120 of 120. Rivals: corridor totals over 24 months 96 of 120; per-signal corridor
  rates 88; intersection-level ranks 71. Each rival's misses include corridors the cooldown skipped, so none reconciles in aggregate.
* **What it does not need to show.** The retiming effect is a filed factor, and the redesign's effect is filed; the log pins only reach.
* **Twin pair.** Sites 1147 and 2208 are identical on legs, control, entering volume, 27 injury crashes in 2022–2024, an expectation of
  6.4 a year and an April in-service date. Site 1147's corridor ranks 9th and is due; site 2208's ranks 6th but was retimed in 2023.
  The programme avoids 1.44 crashes at 2208 and 0.72 at 1147, 2.0× apart, separated only by the review's rule.
* **Resemblance points at the decoy.** By volume and crash count the reached sites most resemble sites on corridors the review skipped
  in 2023, so a resemblance reading predicts no retiming.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant rules: a programme's benefit is the injury crashes it avoids against what would occur without it, in the
  first full calendar year. The state's factor list: the redesign carries a factor of 0.70 and includes a new timing plan; a corridor
  retiming carries 0.85. The construction schedule: signal rebuilds proceed in descending order of expected crashes.
* **Empirical pins.** The review's trigger, from the revision log. Expected crashes, from the state's calibrated functions.
* **Voices.** The traffic engineer: "These intersections will keep crashing at this rate until we rebuild them." The signal unit
  supervisor: "Retiming is maintenance. It isn't a safety programme."
* **Licensed wrong basis.** The grant rules record that the state reviewer benchmarks applications at 30% of observed crashes at the
  treated sites and will apply that basis at the panel.

## 8. Determinism by construction

* **Timing.** Every retiming in the log takes effect on the first Monday of January, so a reached site is retimed for the whole of 2026.
  In-service months are whole months from the first of the month, as the schedule records.
* **Ranking window.** The unit ranks in October on the 36 months to 30 September. No crash in the extract falls within ten days of that
  date at any corridor near the top-fifteen line, so a window end moved by a week selects the same corridors.
* **Corridor membership.** The plan in force on 30 September defines membership. No plan for a reached corridor changed in 2025.
* **Unsignalised sites.** None of the 18 belongs to any coordinated corridor, so the review never touches them.
* **Expectations.** The state publishes its functions and overdispersion, so empirical-Bayes weights have one value per site.
* **Rounding.** The committed figure is 38.51, mid-bin at one decimal.

## 9. Prompt sketch and deliverables

> The safety-grant application goes in on 14 November and has to say how many injury crashes our 50-intersection programme will avoid
> in its first full year, to one decimal. Our traffic engineer is sure the worst intersections will keep crashing at their current rate
> until we rebuild them. Give me the figure as a sentence for the application, with `crash_benefit.xlsx`, a chart `benefit_steps.png`,
> and a one-page `application_note.pdf`.

* `crash_benefit.xlsx` — one row per site (observed, expected, months in service, corridor and rank, avoided), the camera sheet (ask A),
  the repair sheet (ask B) and the bases and back-test (ask C).
* `benefit_steps.png` — a script-rendered waterfall from the budget request's 150.0 to the committed figure, one labelled step per
  correction, the reached sites' contribution shaded, the twin sites marked, and the committed figure as a labelled end bar.
* `application_note.pdf` — the committed figure and how it treats the standing review.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve school-zone speed cameras, citations per 1,000 passing vehicles in the last
  school year and the share contested. *Device:* a citation reissued after a plate-read correction gets a new number with `supersedes`
  pointing at the voided one, as the enforcement data guide documents. Counting both overstates citations at four cameras.
* **Ask B (device-carried).** For each of the six signal maintenance zones, last year's median hours from a malfunction report to repair
  and the share over 48 hours. *Device:* a repair that fails inspection reopens the work order and logs a second completion, and the
  maintenance guide times a repair to its final completion. Using the first completion understates hours in three zones.
* **Ask C (validity).** The 2026 figure under each of the four rung bases, and retimings reproduced (of 120) by the corridor rule and its
  three rivals.
* **Decoupling.** Clearing the review's reach changes no figure in asks A or B. Camera citations and maintenance work orders touch
  neither the crash file nor the revision log.

## 11. Rubric arithmetic

12 cameras × 2 (ask A) + 6 zones × 2 (ask B) + 4 bases and 4 back-test counts (ask C) + the committed figure, the reached sites, the
sites in service and the twin gap + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Observed injury crashes at the 50 sites: 1,500 over 2022–2024. Expected a year: 310 (unsignalised 120, the 18 earliest signal
  rebuilds 150, the other 14 signalised 40). In-service fractions in 2026: unsignalised 0.60, rebuilt signalised 0.55.
* The 11 reached rebuilt sites carry 95 expected crashes a year; all reached signalised sites carry 112.
* Rung figures 150.0 / 93.0 / 46.4 / 38.5; grid cells as listed; rivals at +13.9% and −11.8%.
* 214 coordinated corridors; 120 retimings; the rule reproduces 120 and the best rival 96.
* Sites 1147 and 2208 match on every site-level column and in-service month.
* Camera citations and maintenance work orders never touch crash, plan or schedule records.
