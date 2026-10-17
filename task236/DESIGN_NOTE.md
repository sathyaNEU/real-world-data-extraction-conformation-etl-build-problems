# task236 design note

Architecture 1, wave 2, seed DQ09 (whether a step in the case series is flagged as a series break caused by testing
volume): the seed's decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Epidemiology
& Public Health, disease surveillance, Data Quality Monitoring & Alerting. A state health department's communicable
diseases branch publishes a weekly influenza report with each health region's notified laboratory-confirmed influenza.
When a region's testing changes, its notified series can step for reasons that have nothing to do with influenza: the
report's data quality protocol puts a testing-change break flag on a region's series from the week of the change when
the change moved the share of the region's influenza infections that get notified by more than a quarter. Every Tuesday
the surveillance epidemiologist signs off the flags; the week 36 report of 2027 (the week of Monday 6 to Sunday 12
September) is the first to carry the flags for the eight testing changes the testing change register logged this winter.

## Draw

Card `cards/task236.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, three lines: `overuse.org_family`
(a government agency: the state's communicable diseases branch is the body that publishes notifications);
`repeat.decision` and `repeat.question_form` against task235 (a designation set asked as which: the decision's own form,
a set of regions to flag). `test.same_puzzle_older` (task453, task463) is cleared by the card's differentiation lines:
neither reads a capture share against an independent index that the change cannot reach.

- **Pairing.** Epidemiology & Public Health / disease-surveillance-outbreak-anomaly-detection, serving Data Quality
  Monitoring & Alerting (the domain index lists this task type under AD and DQ). The seed's own domain; Epidemiology x
  Data Quality is not banned against the last three builds (task465, task264, task235). The seed's world (a laboratory
  joining a network) and its method (positivity) are not used: here positivity is the trap, and task234 spent
  positivity as an estimator.
- **Niche.** Influenza notifications rest on who gets tested. This winter point-of-care testing reached the general
  practices of some regions, others moved emergency departments to multiplex respiratory panels, one closed its
  drive-through clinics, and another merged two laboratories; RSV peaked early and hard in the north. The state's
  sentinel general practice network counts influenza-like-illness consultations against its practices' list sizes and
  swabs a fixed protocol sample of those patients, tested at the public health laboratory, whatever any region's
  testing does.
- **The call.** For each of the eight testing changes the register logged between weeks 27 and 32 (eight regions, one
  change each), flag the region's notified series from the change week or not.
- **Shape.** 07, a grid of cells: eight regions, each with its flag and the per-region figures the asks owe. Decision
  designation_set, answer set_of_items, question form which.
- **Strategy.** causal_design with G16 decisive (the infection proxy the shipped data supports: the sentinel
  consultations attributed to influenza by the protocol swabs), G6 supporting (a testing change moves the population
  tested, so the region's own positivity moves with it: the default path's trap) and G14 (the influenza-like-illness
  rate pools influenza with RSV and the other viruses behind the same syndrome); Gate G decomposition_attribution
  (the step split into the testing change's share and the infections'); calibration none; context artifact
  filed_standard (the data quality protocol); layer 2 family field_method, pattern
  own:ascertainment-against-a-sentinel-syndromic-virological-index.
- **Forum, event, organisation.** operations_desk (the surveillance epidemiologist signs off the report's flags; no
  committee), period_close (the week 36 report), government_agency (a state health department).
- **People** (`guard.py names --geo "Australia" --seed 236`): Heidi Sparks, surveillance epidemiologist, who signs off
  the flags; Brendan Davis, sentinel network coordinator; Jane Suarez, laboratory liaison, who keeps the testing change
  register.
- **Deliverables.** `influenza_testing_break_flags_week36_2027.xlsx` (one row per region with a logged change: the flag
  and the asks' figures) and `notifications_against_sentinel_activity_week36_2027.png` (each region's notifications
  against the sentinel network's influenza activity either side of its change).
- **Data-native sentence.** A testing change alters who is tested as well as how many, so each region's positivity moves
  with the change itself (multiplex panels test every emergency department respiratory patient, point-of-care tests
  reach patients a laboratory never saw at the same pre-test probability); the sentinel practices swab a fixed protocol
  sample of their influenza-like-illness patients that no regional testing change reaches, so their consultations times
  their swab positivity follow the region's influenza infections, and notifications against that index give the change
  in the share notified, while raw notifications ride the season's rise and notifications per consultation ride RSV,
  which fills the same consultations.

Sources, one line each (what it teaches; how this build differs):
- Client pattern disease-surveillance-outbreak-anomaly-detection/3 (testing volume changes the count; positivity or a
  test-adjusted rate): here the testing change moves who is tested, so positivity is itself moved, and the change in
  ascertainment is read against a sentinel index no testing change reaches.
- Influenza surveillance practice: sentinel general practice networks report influenza-like-illness consultations per
  registered patient and swab a protocol sample; consultations times the share of swabs positive for influenza is the
  field's own index of influenza activity, separated from RSV and other viruses by the swabs.
- Seed DQ09: the decision and the quantity only; its decoy-era design is not read.
- Spent on this objective (`guard.py mechanisms`): task228 (a ratio metric's variance at the randomised unit), task229
  (a daily mean through a convex rating), task230 (net coding bias of a late channel), task231 (the closed share of
  silent units from rounds the register caught up with), task232 (transmission from delayed, mixed outcomes), task233
  (a missing-not-at-random departure on the odds scale), task234 (a source's output read from a share a loss cannot
  move), task235 (a missing event censored until its device's next contact). None reads a capture share against an
  independent fixed-protocol sample that the capture change cannot reach.

## Default path

1. Read the data quality protocol: a region's notified influenza series carries a testing-change break flag from the
   week of a change in the testing change register when the change moved the share of the region's influenza
   infections that are notified by more than a quarter, the four weeks from the change week against the four weeks
   before it.
2. Take the laboratory and point-of-care results, collapse repeat specimens into episodes, assign each to its region by
   residential postcode, and count each region's notifications and tests by report week.
3. Adjust for testing: the share notified moves with testing, so compare each region's positivity (notifications per
   test) over the four weeks from its change week with the four weeks before, and flag a change of more than a quarter
   either way.

Ends on: four regions flagged, four of the eight wrong (the two unchanged regions whose positivity rose with the
season flagged, the drive-through closure and the northern point-of-care region missed, because closing a clinic and
adding point-of-care tests change how many people are tested without changing their positivity).

Golden: flag the three point-of-care regions (the share notified up by about two thirds or more) and the drive-through
closure (down by about two fifths), and none of the other four.

## Stump sentence

A competent solver adjusts for testing by comparing each region's positivity in the four weeks after its testing change
with the four weeks before and files 4 of the 8 regions wrong (Ends on: two unchanged regions flagged as their season
rose, the clinic closure and the northern point-of-care region missed); the step that lands it there is reading the
share of infections notified off the tests the region's own laboratories ran, which the testing change itself moved,
instead of off the sentinel practices' influenza-attributed consultations, which no testing change reaches.

## Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves Data
  Quality Monitoring & Alerting; the object is the comparability of a published notification series across a testing
  change, and the call is the report's break flag.
- **Domain test:** the quantity that decides is each region's change in influenza ascertainment (the share of its
  infections that are notified) across its testing change, read against the sentinel network's influenza-like-illness
  consultations attributed to influenza by its protocol swabs, the syndromic and virological index surveillance builds
  for exactly this.
- **Swap:** "which stores' sales series carry a till-change break flag, judged on the share of shoppers' purchases the
  tills record" has no syndrome that several viruses fill, no protocol swab that attributes it, and no testing change
  that moves who is tested; the analysis that decides here has nothing to act on.
- **Layer 1:** repeat specimens from one person within an episode, and a point-of-care result later confirmed by a
  laboratory (the laboratories and the point-of-care services each report); the residential postcode against the
  testing laboratory's region (the notification system records both); the report week by specimen collection date
  against UTC receipt times (the notification gateway stamps UTC); sentinel practices that miss a week's return and list
  sizes that change (the network's returns); result text varying by laboratory and multiplex panels reporting each
  virus on its own row (each laboratory system's export). Nothing is placed to be caught.
- **Layer 2:** field_method, ascertainment against an independent index: the change in the share notified is read
  against the sentinel network's influenza-attributed consultations; positivity, raw notifications and notifications
  per consultation each mismeasure it.
- **Decisive step:** estimating each region's influenza infections either side of its change from the sentinel
  practices' influenza-like-illness consultation rate times the share of their protocol swabs positive for influenza,
  and reading the change in notifications against that index rather than against the region's own tests.
- **Not semantics:** the default path reads every field, code and status right (episodes collapsed, postcodes mapped,
  weeks read by collection date, multiplex rows counted once per specimen) and still files 4 regions wrong; what it gets
  wrong is which quantity measures the region's infections, which no field states.
- **Not rule application:** the protocol files the flag's quantity (the change in the share of infections notified),
  the windows and the quarter; no rule says how a region's infections are to be estimated, and executing every stated
  rule still leaves that choice.
- **Analyst test:** a strong analyst who cleans the data and reads every rule, then judges each region's testing change
  on the change in its positivity, files 4 of the 8 regions wrong (Ends on: two unchanged regions flagged, the clinic
  closure and the northern point-of-care region missed); raw notifications flag every region as the season rises, and
  notifications per influenza-like-illness consultation flag every region too, RSV having filled the northern
  consultations.
- **Estimand:** the data quality protocol (in the pack) fixes the population (each region's influenza infections), the
  outcome (notified as a laboratory-confirmed or point-of-care-confirmed case), the window (the four report weeks from
  the change week against the four before), the unit (the region's notified series) and the comparison (a change in the
  share notified of more than a quarter either way).
- **No decoy:** nothing is planted: no memo, earlier report, draft or stakeholder figure states a region's ascertainment
  or a flag; the testing changes are the register's operational entries; the sentinel protocol describes the network as
  such protocols do.
- **No certified replay:** no certified or published ascertainment exists for a method to reproduce.
- **Lesson:** a change in how cases are found moves the found share and the tested population together, so the found
  share has to be read against a measure of infection that the change cannot reach; no build on file reads a capture
  share against an independent fixed-protocol sample.

## Tried and rejected

- The seed's laboratory joining a network, read on positivity: positivity as the estimator is spent (task234), and a
  laboratory joining moves the network's coverage rather than ascertainment within a region.
- Wastewater against notifications as the infection index: normalising by a faecal marker repeats task234's
  invariant-share insight, and the shedding lead adds a fork; the sentinel swab positivity alone is not proportional to
  infections when RSV fills the consultations, so it is a rung, not the index.
