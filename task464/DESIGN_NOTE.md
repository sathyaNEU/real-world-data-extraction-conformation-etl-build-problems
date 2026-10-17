# task464 design note: the 2027 Adolescent Literacy Partnership grants (architecture 2)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: architecture 1 (the
Wendlemere building emissions slate) was sent back by the determinism judge and a first redraw was dropped before
registration; architecture 2 is drawn afresh in the ETL objective.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task464.json` (architecture v2, architecture 1 in `lineage`), registered
  2026-10-17 09:40 UTC, guard WARN only. Answered: the first name Jeffrey appears in one older build (task141); the
  state department of education is the honest organisation (government_agency, overused); Gate G
  method_or_model_selection repeats across the batch, the honest mechanism; the question form is which, because the
  call picks districts. Differentiated: task450 (common-item linking of two forms given to different groups, the
  instrument's change separated from the groups' difference; here one group took both tests and the trap is a
  regression's prediction used as a concordance) and task184 (an offence spread over its occurrence window).
- **Seed:** none kept. ET21's world (a building emissions slate) is spent with architecture 1; the slot is re-drawn in
  a new world.
- **Pairing:** Education & Learning Sciences / item-response-theory-test-equating / ETL, own pattern "concordance by
  distribution matching, not regression". Placing a retired test's scores on a new test's scale is the task type's own
  work, and the conformed file (each student's latest grade 8 reading level on the new scale) is the dataset the grants
  are set on. The task type is the least drawn of the six that serve ETL (task450 alone), and none of its three listed
  patterns (DIF matched on ability, anchor drift, anchor-based equating for nonequivalent groups) is this mechanism.
- **Shape:** 01, a ranked list under a cap: the six districts awarded, each one's grade 9 and 10 students at Level 1,
  the first district left out and its gap to the sixth, and a chart; the conformed file and the asks add the rest.
- **Strategy:** other (scale linking). The decisive step is the field's concordance between the retiring and the new
  test, on the population gap (a regression's predicted scores are not the scores the 2025 cohort would have had, and
  the grants count a distribution's tail) with G1 (a score on one scale read on another's) and G16 (method selection).
  Gate G method_or_model_selection.
- **World:** an unnamed state of the United States. Its Department of Education replaced the Grade-Level Reading
  Assessment (grades 3 to 8, last given in spring 2025, its own scale and four performance levels) with the Statewide
  Literacy Measure (first given in spring 2026, a new scale and four new levels). In spring 2026 the Department's
  assessment office ran a bridge study: the grade 8 students of a random sample of schools took both tests, in
  counterbalanced order. The 2027 Adolescent Literacy Partnership grants go to the six districts with the most grade 9
  and grade 10 students, on the October 2026 enrolment count, whose latest grade 8 state reading result is at the
  Statewide Literacy Measure's Level 1, a Grade-Level Reading Assessment result counted at the level it places at on the
  new scale. This year's grade 9 took the new test in grade 8; grade 10 took the retiring one.
- **Forcing fact:** the State Board of Education awards the grants at its December 2026 meeting for calendar 2027; the
  call faces forward (the 2027 grants on the students now in grades 9 and 10).
- **Forum and forcing event:** trustees_or_governors (the State Board of Education), budget_or_appropriation (the 2027
  grant appropriation). Organisation government_agency; role programme_officer. Personas from `guard.py names --geo
  "United States" --seed 464`: Jeffrey Warren (the programme's director, who issues the grant rules) and William
  Holloway (the assessment office's psychometrician who ran the bridge study).
- **Data-native sentence:** the state changed its reading test after spring 2025, so this year's grade 10 carries only
  the retiring test's grade 8 scores while grade 9 carries the new test's, and the only link is a bridge study in which
  each student's two scores both carry measurement error, so the regression of one score on the other is flatter than
  the line that matches the two scales, and placing each 2025 score at its regression prediction pulls the low scores
  toward the bridge sample's mean and out of Level 1.
- **The WHAT screen.** The estimand's five parts are filed by the grant rules: the population (grade 9 and 10 students
  enrolled in each district on the October 2026 count day), the outcome (the latest grade 8 state reading result at
  the new test's Level 1, a 2025 result counted at the level it places at on the new scale), the window (the latest
  grade 8 administration, spring 2025 or spring 2026), the unit (students) and the comparison (every district, the six
  with the most). The decisive step settles none of them: it is how a 2025 score is placed on the new scale, a
  regression's prediction or a concordance that matches the two tests' score distributions, two ways of estimating one
  filed quantity, and the bridge data rule out the easy one (placed by the regression, the bridge sample's own retiring
  scores put fewer students at Level 1 than its new scores do).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, item-response-theory-test-equating: DIF, anchor drift and
    nonequivalent-groups equating are the listed patterns; this build takes the linking design itself (a single-group
    bridge) and the decision between prediction and scale alignment, which none of them covers.
  - `stumping/references/client/two-layer-task-design.md`, estimation that fits the data: both variables carry error,
    so the least-squares line of one on the other is attenuated; here the attenuation decides who counts at Level 1.
  - The field's own practice: tests are placed on a common scale by equating or concordance (equipercentile or linear,
    symmetric and invariant across groups), and a regression of one test on the other is a prediction, not a linking;
    the build files neither, it files the quantity.
  - `dataset-generation/references/layer1-messiness.md`: two vendors' layouts and identifiers, not-tested and
    invalidation codes, retests, transfers between districts, a merged district; none on the decisive step.

## Tried and rejected

- Weather normalization alone, with oil fills and estimated reads as the interval structure: in a prototype of 150
  buildings, a degree-day regression on calendar-month bills with oil deliveries summed by month landed within 2 per
  cent of the fill-to-fill fit for most oil buildings (6 at most) and on the golden's slate, so a strong analyst's
  regression lands the call; the estimated reads and fills are Layer 1 (cleaning them makes the call easy) and stay
  there. The decisive structure is each building's change in how it runs.
- A first keying of the card on the time gap with pattern A and Gate G forecasting: the signature is spent in seven
  older builds; keyed on the population gap with G4 first, which also reads truer (the bills before a change are not
  the decided building).
- The 2025 benchmarking year scaled by degree days as the default path: the cycle rules name the bills, statements and
  tickets as the records, so a competent analyst fits them; the filings route stays below rung 0 and the default path
  is the whole-record fit.
- Ask B on the gap between the filings and the bills for 2025: its golden sat near zero for most types; Ask B now
  carries the filings' own emissions and site energy by type on the export's lot rows.
- A six-day sensor outage in April 2024 in the weather record: leaving missing days out of the degree days moved 808
  Thornwick Avenue and 686 Fenwright Avenue across their $5,000 bins; the outage now sits in April 2019, outside the
  billing years.
- Partial oil deliveries at random on every building: taking them as fills hid one building's boiler change from the
  search and put it in the slate; partials now fall in the 2022 to 2023 season, on no building near the cut, and every
  building away from the cut is held under $55,000 on a whole-record fit.
- The law's billing sentence ("bills it to the property's tax lot and posts any deduction ... against the same
  notice"): an ask organ in a document the call reads, and wrong against the ledger (a reassessment opens a new
  notice); cut.
- Round floor areas on the twenty buildings placed around the cut (each a multiple of 1,000, against none of the other
  138): a giveaway; each now carries an ordinary area and the calibration re-aims.
- Keeping estimated reads and partial deliveries off the buildings around the cut, to hold those items neutral: a second
  giveaway. Every building now carries the same processes: the utility's estimates land within a few per cent, as a
  weather-adjusted routine does (estimates missing by 20 to 40 per cent, read as actual, hid two slate properties'
  changes from the search), none after the advanced meters of October 2025 or the steam company's January 2025 system,
  and partial deliveries stop a few hundred gallons short, in the 2022 to 2023 season only.
- A window started one span after the found break as a variant the golden must hold under: no reader would choose it
  (the first span after a change is wholly post-change), and 62 Merrow Street moves 2 per cent under it; the variant
  asserted is the generator's own change dates.
- Architecture 1, the degree-day fit on each fuel's spans after its last change found in the property's own bills
  (2026-10-17): judged NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, underspecified_objective). The post-
  change window's first span and whether electricity is refit with the heating fuel are open (461 Tallman Street's
  electricity rises 1.35 times when its gas falls; refit, it is the first left out at $70,990 against 633 Lattermore
  Place's $68,577), a step search run as written flags dozens of series and moves four $5,000 amounts, and a $7,000
  12th-to-13th margin sits inside a $40,000 to $57,000 window freedom. Filing the window or a dated change log would make
  the step rule application; an undated change cannot be pinned without it. The architecture is spent and re-rooted.
- A first redraw (architecture 2 on paper, 2026-10-17): each district's claim under a state challenge judged by the
  upper end of its inventory's 95 per cent interval, the decisive move carrying each shared emission factor's error on
  the district's fuel total instead of building by building. The correlated-error lesson is already task228's,
  task229 v1's, task260's and task261's (an error shared by the units does not average away); dropped before
  registration.
