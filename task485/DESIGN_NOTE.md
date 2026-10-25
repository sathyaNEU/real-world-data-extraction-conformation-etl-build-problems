# task485 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-25. The seed (ET42, an
employer index of entry-level wage reliance from H-1B labour condition applications) was screened at the draw and its
world set aside (`## Tried and rejected`); the slot is re-worlded, as this lane's task482 and task484 were, into a
boundary commission's electoral review, keeping the seed's shape of a designation read from a conformed
administrative register whose records are not yet the thing the decision counts.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task485.json` (architecture v1), registered 2026-10-25 after a fetch of
  main. The window the axis bans read (task184, task302 and task301, the live cards filed last) closes the strategies
  informative_censoring, causal_design and population_selection, the forums council_or_assembly, line_manager_or_team
  and executive_team, the forcing events period_close, cutover_or_migration and budget_or_appropriation, the
  organisations local_government, retailer_or_ecommerce and foundation_or_funder, the roles programme_officer,
  operations_director and research_desk, the context artifacts planning_thread, other and register, and the shape
  other. The draw's honest labels clear all of them: the decision is the Commission's, not the council's (a national
  boundary commission, government_agency; its members agree draft recommendations at a meeting, committee_or_panel and
  vote_or_meeting), the requester is its review manager for the district (policy_adviser), and the stakeholder's own
  file is its technical guidance on electorate forecasts (filed_standard).
- **WARNs answered.** `test.same_puzzle_older` (time, E, designation_set against task235 and task445) and
  `test.same_driver_older` (time, E, etl_conformance against task481) are differentiated on the card: none of them has
  a unit whose count builds up toward a settled level over rounds after it is created, or a forecast that has to age
  units that do not yet exist to the horizon. `overuse.org_family` (government_agency in 40 builds): the Commission is
  the body that decides a warding pattern, and the council's electoral services only supply the data.
  `repeat.question_form` (which, against task302 and task301): the Commission names the wards whose pattern it must
  change, so the question asks which.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: six published registers at property level in two election management system layouts, the address
  register, the council's completions monitoring and housing trajectory, and the polling district and ward schedules,
  conformed into each ward's electors on the register to be published after the 2032 canvass.
- **The decision and the quantity:** an unnamed UK-like country with individual electoral registration and an annual
  canvass, whose Local Government Boundary Commission reviews a district of 23 wards and 43 councillors, last warded
  in 2014. The Commission bases a warding pattern on the electorate five years after its final recommendations (due
  in 2027): the electors on the register published on 1 December 2032. A ward whose electors per councillor on that
  register would lie more than 10 per cent from the district's average fails the Commission's electoral equality
  test, and its pattern must change. At its December 2026 meeting the Commission agrees which of the 23 wards fail at
  today's boundaries and councillor numbers, and the draft recommendations redraw those.
- **Shape:** `10`, a scorecard against thresholds: each ward's 2032 electors, its electors per councillor and its
  variance from the average against the 10 per cent line, beside the call; the asks are designed at stage 2.
- **The default path holds the field's method (stumping 1.1b).** Conform the 1 December 2026 register to wards, add
  every dwelling the council's trajectory places before the 2032 canvass at the settled stock's electors per dwelling
  (by dwelling type, from the 2026 register over the dwellings in use), keep each existing dwelling at its 2026 count,
  and test each ward's variance. That is the method the Commission's guidance describes in general terms (the current
  register plus the electors expected at new dwellings) and the one an electoral administrator builds first.
- **The decisive step:** that method's precondition is that a dwelling's electors are on the register at the settled
  ratio from the canvass after it is built. They are not: a household joins the register over the canvasses after it
  moves in (the completeness-by-length-of-residence the electoral field measures), so the estates completed since
  2022 hold well under their settled electors on the 2026 register and will reach them by 2032, while the dwellings
  the trajectory places in 2030 to 2032 will still be young at the 2032 canvass. The register's own six canvasses show
  each completion cohort's electors per dwelling rising canvass by canvass toward the settled stock's; ageing every
  dwelling, built or to be built, to its number of canvasses at December 2032 moves wards across the 10 per cent line
  in both directions. A uniform completeness factor (the national share of adults on the register) moves no ward,
  since every variance is a ratio to the district's own average.
- **People:** drawn with `guard.py names --geo uk --seed 485` (Maurice Evans, Megan Stewart, Jean Grant, Donald
  Hayes, Conor Porter, Gordon Hope): Megan Stewart, the Commission's review manager for the district and requester;
  Donald Hayes, the district's electoral services manager who supplied the data. Owners in file properties and
  sign-offs only.

## Three rules

Task type: Survey Research & Official Statistics, census-register-administrative-data-quality, which serves ETL in the taxonomy (registers conformed across two system layouts, an address register and a planning trajectory into an electorate the register only partly holds yet).
Domain test: the quantity that decides is each ward's electors on the register to be published after the 2032 canvass, against the district's average electors per councillor; electoral statistics measure a register's completeness by the elector's length of residence, and the field's forecast adds new dwellings at an electors-per-dwelling ratio, so the decisive analysis is the register's coverage of a dwelling's electors by the number of canvasses since the dwelling was completed, read from the register's own canvasses and applied dwelling by dwelling at the 2032 canvass.
Swap: "which of the district's 23 school catchments will be more than 10 per cent from the average pupils per form of entry in 2032" (catchments for wards, pupils for electors) has no build-up to age: a pupil is on roll from the day of admission and no canvass adds pupils a year at a time, so the step has nothing to act on and the task reads differently.
Layer 1: the register in two election management system layouts (2021 and 2022 keyed by the old system's property reference, 2023 to 2026 by UPRN after the migration), polling district codes renamed by the 2024 polling district review, franchise markers (overseas electors on the register for parliamentary elections only, local-only electors), attainers listed with their dates of birth, the address register's alternative and historical records beside each approved record, the trajectory in monitoring years (April to March) against canvass years (register published 1 December), and the trajectory's base date falling after part of 2026/27 was built and canvassed; each written by the system that holds it, none placed to be caught, each asserted neutral on the call (R2).
Layer 2: field_method, a register's build-up: a dwelling's electors reach the register over several canvasses after it is completed, so the 2026 register is censored low exactly at the estates still building up and the settled ratio is wrong for dwellings that will be young in 2032; the choice that flips the call is ageing every dwelling to its canvass count at December 2032 on the build-up the register's own canvasses show.
Decisive step: recognising that the settled stock's electors per dwelling holds only for dwellings several canvasses old, reading from the six registers how each completion cohort's electors per dwelling rises canvass by canvass toward the settled level of its dwelling type, and applying that build-up to every dwelling completed since 2020 and every dwelling the trajectory places before the 2032 canvass, at its number of canvasses on 1 December 2032.
Not semantics: with every field read correctly (UPRNs across the two layouts, the 2024 polling district codes, franchise markers and attainers, the address register's approved records and their states, monitoring years against canvass years), the easy route still flags the wrong wards, because no field records that a dwelling's electors are still joining: an estate completed in 2025 shows an ordinary property with fewer electors than its neighbours, and nothing says how many it will hold in 2032.
Not rule application: the Commission's guidance files the WHAT (the electors on the register published on 1 December 2032, at today's boundaries and councillor numbers, against the district average, with the trajectory's dwellings as the council phases them) and no clause says how a dwelling's electors are projected, so executing every filed rule is the default path. Measured on paper (23 wards, expected values): the enumerated family (the settled ratio for the district or by type, a uniform completeness factor, the ratio today's new estates show, the recent estates caught up alone, the future dwellings aged alone, every dwelling aged) files four distinct sets, the uniform factor files the default's set exactly, and only ageing every dwelling files the golden; the standing family (the build-up read cross-sectionally from the 2026 register or from the six-canvass panel, pooled or by dwelling type) and its spread on the call are re-measured on the generator's clean truth at stage 2, where precut's numbers replace these; the ruling-out is the panel's cohort-by-canvass table, which no file prints.
Analyst test: A strong analyst conforms the 1 December 2026 register to wards, adds every dwelling the trajectory places before the 2032 canvass at the settled stock's electors per dwelling by type, keeps each existing dwelling at its 2026 count, and flags the wards whose late sites it counts as full while missing the wards whose estates completed since 2022 are still joining the register (the set is fixed at stage 2).
Estimand: each ward's electors on the register published on 1 December 2032 (local government electors, every dwelling in use by then, the trajectory's dwellings as the council's 30 September 2026 trajectory phases them), divided by its councillors and compared with the district's 2032 electors over 43 councillors, a ward failing where it lies more than 10 per cent from that average; filed in the Commission's technical guidance on electorate forecasts.
No decoy: nothing is planted; the registers, address records, completions and trajectory are the council's own records as its systems write them, no forecast, memo, draft or stakeholder figure carrying a wrong answer ships, and the estates still building up are ordinary new housing whose residents register as residents do.
No certified replay: no certified or published figure is reproduced to recover the method; the published electoral statistics carry district totals only, and the build-up is read from the registers themselves.
Lesson: a register's count at a new dwelling builds up over the canvasses after it is completed, so a five-year electorate forecast has to age every dwelling, built or still to be built, to its canvass count at the horizon, because both the settled ratio and the ratio new estates show today are wrong for most of them; no build on file teaches it (task451 and task445 complete closed periods from arrival lags, task480's age curve is a falling rate of use, none ages units that do not yet exist to the horizon).

## Tried and rejected
- 2026-10-25, at the draw: the seed's own world, each employer's FY2025 H-1B workers at Level I read from labour
  condition applications through USCIS's employer data hub, positions converting to approved petitions at very
  different rates by petition type (cap lottery against continuations) so the position share overstates Level I where
  it sits in new employment: the per-type apportionment is one join and one group-by once seen, the hub's initial and
  continuing columns invite it, and the employer-level conversion that leaves the share unchanged is the only partial
  fix; the cheapest licensed member is the golden, a single insight a reader has or does not. Not drawn.
- 2026-10-25, at the draw: the FY2027 weighted wage-level selection, each employer's Level I intake read through
  selection probabilities by level: executing the stated selection procedure is rule application, and its separation
  from the linear reading is small (Level I at 0.174 against 0.154 on a plausible pool). Not drawn.
- 2026-10-25, at the draw: regression to the mean and retransformation bias (spent in five slot notes each), landfill
  first-order decay (set aside three times in this lane against task480), overdose deaths with unspecified drugs
  (task455 v1's certificates corrected by drug class), age heaping (task230's rejected draw), areal interpolation
  (task253), a business register's head-office employment (a reflex join once the local unit register ships), a
  housing trajectory's lead-in times for unstarted sites (the trajectory reproduces the started sites by construction
  and fails forward on the rest, a validated decoy), spiralled forms in a random-groups equating (a balance check is a
  reflex and presmoothing forks the cut), a business register's industry codes maturing with the enterprise's age (a
  completion reskin). Spent or not drawn.
