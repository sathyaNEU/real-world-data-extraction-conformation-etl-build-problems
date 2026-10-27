# task464 design note: the 2027 outpatient capacity register (architecture 3)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: architecture 1
(the Wendlemere building emissions slate) was sent back by the determinism judge, architecture 2 (placing the
retiring reading test's scores on the new scale) was solved on the portal because its decisive step was
psychometrics' own named method for the deciding quantity, and architecture 3 is drawn afresh in the ETL
objective with the field's method moved into the default path.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task464.json` (architecture 3, architectures 1 and 2 in `lineage`),
  registered 2026-10-27, guard WARN only, 299 cards validated. The one WARN is `repeat.question_form`: how-many
  also opens task141's prompt, two builds back. Answered: the decision is a count of weekly treatment slots, so
  how-many is the form the decision gives (the guard's own fix line), and task141 counted re-arrests at a horizon.
- **Pairing:** healthcare-delivery-health-economics / payment-claims-health-plan-analytics, objective Data
  Extraction & Conformation (ETL), prompt shape 07 (grid of cells: each area cell).
- **Shape 07 against the two the taxonomy calls native for ETL.** Shapes 03 and 15 both announce the decisive
  step: a bridge between totals makes its own line items name the step from attested stations to deliverable
  positions, and fields-to-one-schema makes each field's transform a filed instruction. A grid of twelve area
  cells grades the same conformation without naming how any field is built.
- **Niche:** a nonprofit Medicaid managed care plan's network unit conforming one capacity dataset for its 2027
  outpatient dialysis and infusion contracts, out of the provider directory, the state licence file, the staffing
  rosters and four years of timed treatment encounters.
- **Strategy:** `binding_constraint`, gap `population`, Gate G `binding_constraint`, generators `G8`, decisive
  rule filed `false`, official decoy `false`, validated decoy `false`, `stump_class: analytical`.
- **Data-native sentence.** A treatment encounter is recorded with the clock time the chair was occupied, because
  infusion and dialysis are billed in timed units, so this pack carries four years of a site's own service
  intervals; the greatest number of them that have ever run together at a site is a measurement of how many of
  its positions can be worked at one time, and nothing else in the pack measures that, because a directory
  attestation and a licence both count the positions that exist rather than the positions that can run.
- **Sources, one line each.** `guard.py mechanisms --objective etl` was read before drawing. task487 (emissions
  inventory ETL) spends the insight that a reported total is assembled from sources at different vintages, which
  this build does not use. task485 (census register ETL) spends coverage of a register against an independent
  enumeration, which is a completeness question rather than a capacity one. task137, the nearest build in this
  client domain, spends demand censored by refusals at a capacity-bound service, which is the mirror of this
  build and is about demand, not about how much a site can deliver. task69 spends overlap between the
  contributions of a capped set's members, between units; this build's overlap is inside one unit, between its
  own positions. Nearest driver on file is 0.08 (task479, lineage).
- **Fiction.** An unnamed state of the United States, USD, a nonprofit Medicaid managed care plan contracting
  outpatient dialysis and infusion capacity, forum `operations_desk`, forcing event a purchase order or contract,
  org family `nonprofit_or_charity`. People drawn with `guard.py names`: Katherine Dalton, Nicholas Clay.
- **Deliverables:** `outpatient_capacity_2027.csv` (one row per contracted site) and `area_capacity_2027.xlsx`
  (the twelve service areas against the adequacy standard, with the chart).
- **The call faces forward:** the 2027 network year is not yet contracted at the as-of date.

## Default path

A competent analyst builds this without hesitating, from the prompt's words and the files' grain.

1. Read `provider_directory_*.csv` and keep the outpatient dialysis and infusion sites with a 2027 contract
   intent, resolving each site's identifier through the directory's own attestation cycles (a site appears once
   per cycle, the latest row current).
2. Join the state licence file on the service address to confirm each site is licensed and to carry its licensed
   station count, reconciling the corporate-entity rows against the service-address rows.
3. Read the staffing rosters and count each site's rostered treatment sessions a week by position.
4. Conform the two encounter layouts across the clearinghouse change and aggregate four years of encounters to
   each site's treatments a week, to measure realised volume.
5. Take each site's capacity as its attested stations times its rostered sessions a week, times the treatments a
   position runs in a session.
6. Reconcile the product against realised volume and against the adequacy contract's utilisation standard: the
   ratio sits in a plausible band at most sites, and the sites where it does not are the ones the plan already
   knows are growing.
7. Roll the sites up to the twelve service areas and compare each area against the standard.

Ends on: a 2027 network capacity about a sixth above the golden, with three of the twelve areas filed above the
adequacy standard that are below it (target magnitudes, measured at stage 2 against the cut data).

Golden: the same conformation with each site's deliverable positions set to the greatest number of its own
treatments that have ever run at one time, which at about a third of the sites is several short of the stations
it attests and the licence lists.

## Stump sentence

The default path multiplies each site's attested stations by its rostered sessions, ties the product to realised
volume and the adequacy standard, and files a 2027 network capacity about a sixth high with three of the twelve
areas wrongly above the standard, because the stations a site attests are the positions it has, not the positions
it can work at one time, and at about a third of the sites no hour in four years of its own timed encounters has
ever had more than a fixed number of treatments running together.

## Three rules

Task type: provider-network-capacity-and-adequacy-analytics: conforming one capacity dataset for a contract year
out of a provider directory, a licence file, staffing rosters and a timed encounter extract, a task type serving
Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each contracted site's deliverable treatment capacity for the 2027 network
year, which health plan analytics builds as the positions a site can work times its staffed sessions and tests
against the utilisation standard the adequacy contract sets; put a warehouse's nouns in and there is no staffed
session, no treatment interval and no position a patient occupies for a fixed span, so the quantity disappears.

Swap: "how many pallet positions the 2027 network holds, from the yard directory, the operating permit, the shift
rosters and four years of timed putaway records" keeps the sentence and loses the move: a pallet position is
occupied by a pallet and nothing stops every position being full at once, so there is no ceiling below the count
of positions and the conformation is a join.

Layer 1: a directory refreshed on each site's own attestation cycle; licence rows at both the corporate entity
and the service address; two encounter layouts across a clearinghouse change (one carries start and stop, the
other start and a duration in minutes); treatment start and stop times in local clock with no offset on one feed;
rosters by position rather than by named staff; sites that moved address and kept their identifier; a group
practice billing three sites under one tax identifier; cancelled and no-show encounters carried with no stop time.
Each is written by the system that produces it, none is placed to be caught, and each is asserted neutral on the
call.

Layer 2: allocation under a constraint (`own:the ceiling the overlaps fix`): the call flips on reading each site's
deliverable positions off the overlaps of its own service intervals rather than off the station count the
directory and the licence carry.

Decisive step: setting each site's deliverable positions to the greatest number of its own treatments ever running
concurrently, recovered by sweeping four years of its service intervals, rather than to the stations it attests or
is licensed for; in the field's words, measuring the site's effective chair capacity instead of taking its
attested chair count.

Not semantics: every field, code, unit and definition read correctly leaves the easy route on the wrong answer.
The attested station count is read correctly as the stations the site attests and is true of the site; the licence
count is read correctly as the stations the state licensed; no field, label, dictionary entry or definition in the
pack names deliverable positions, effective capacity or a ceiling, so there is no field whose correct reading
supplies the figure. The figure has to be constructed from the encounters' overlaps.

Not rule application: the adequacy contract files the population, the window, the unit and the standard, and no
rule or procedure in the pack says how a site's deliverable positions are determined; executing every filed rule
with the attested station count files the wrong total, so the step no rule performs is the reconstruction of the
positions.

Analyst test: a strong analyst who resolves the directory's attestation cycles, reconciles the licence file's two
grains, conforms both encounter layouts and counts the rostered sessions correctly takes attested stations times
rostered sessions, reconciles it against realised volume and the utilisation standard, and files a network
capacity about a sixth high with three of the twelve areas wrongly above the standard. Executed in `checks.py` on
the generator's clean truth at stage 3.

Estimand: the adequacy contract's capacity section, filed in the contract document at authority: for each site
the plan intends to contract for the 2027 network year, the treatment slots a week the site can deliver, counted
as its deliverable treatment positions times the treatment sessions its roster staffs in a week times the
treatments a position runs in a session; and for each of the twelve service areas the sum over its sites against
the standard. It fixes the population, the window, the unit and the comparison, and says nothing about how a
site's deliverable positions are found.

No decoy: nothing is planted to be caught. The directory's attestation is a true attestation of the stations the
site has, the licence file is a true licence, no memo, briefing, draft or stakeholder figure argues for a method
or for a capacity number, and no file counts or ranks the areas against the standard.

No certified replay: no certified or published figure reproduces a method. The capacity report that ships as the
context artifact is the prior year's, states its own basis and is ruled out by the contract's window, and no table
of site capacities or area totals ships.

Lesson: capacity assembled from the positions a unit reports is an upper bound, not a measurement, and where the
unit's own service record is timed, the positions it can work at one time is measurable and smaller; no build on
file teaches a ceiling recovered from a unit's own overlaps (task69 overlaps the contributions of different
members of a capped set, task137 censors demand at a capacity bound).

## Readability screen

Owed at stage 2 for architecture 3. The decisive row is the concurrency ceiling and must come out `silent`; the
test to watch is test 3 (reflex), because a capacity planner handed timed service intervals may sweep them for
occupancy without being sent. The two encounter layouts (one with start and stop, one with start and a duration)
keep the sweep from being a single column's maximum.

## Semantic fork table

Owed at stage 2 for architecture 3. The rows already known to be needed: the reading of a site's ceiling (record
maximum against each year's, each month's and a high quantile over treating hours, converged by C1 on a hard
plateau and asserted, never pinned by a sentence saying how to compute it); the interval convention (half-open
against closed, converged by giving every site a strictly positive turnover between a position's successive
treatments, so no two of a site's intervals share an endpoint); cancelled and no-show encounters (carried with no
stop time, so no interval is constructible under any reading, with the ceiling asserted unchanged if a reader
treats them as instantaneous); the local clock with no offset on one feed (a site-level offset cancels inside a
site, asserted, including across the autumn fall-back hour); a treatment session and a week; the attestation
cycle that is current at the as-of date; and the rounding of the area totals.

## Ladder

Owed at stage 2 for architecture 3. The rungs drawn on paper, to be measured against the cut data: rung 0 attested
stations times rostered sessions; rung 1 the state licence's station count in place of the directory's attestation,
for an analyst who distrusts a self-attestation; rung 2 a volume ceiling, each site capped at the treatments of its
busiest week over its sessions, which is defensible and lands on its own wrong total because a session can be
short-staffed and a position can turn over more than once; rung 3 the concurrency ceiling. Each rung names its own
total and its own set of areas above the standard, and the arithmetic of `dataset-generation` section 6 is written
here before any row is cut.

## Closure table

Owed at stage 2 for architecture 3: the 22 axes with the reading and the closure move, one row per axis number.

## Literal reader

Owed at stage 2 for architecture 3.

## Oracles

Owed at stage 2 for architecture 3. The prior year's capacity report is the context artifact and is the one control
to screen hardest: it must tie under every rung's basis or be out of window, never only under the golden.

## Ask sheet

Owed at stage 2 for architecture 3, with the pair arithmetic, the cracker and mirror sheets and the separation
counts. The main call's declared row population is the 2027 contract-intent sites' own encounters; every ask device
sits outside it.

## Layer 1 inventory

Owed at stage 3 for architecture 3, one row per item in `## Three rules`'s `Layer 1:` line with the system that
produces it and its asserted neutrality on the call.

## Pre-ship check

Owed at stage 5 for architecture 3.

## Leak check

Owed at stage 3 for architecture 3. The pack ships no file whose job is to describe the data: no dictionary, field
notes, readme or manifest (`dataset-generation` section 3), so every convention the call leans on sits in the
adequacy contract at authority.

## Tried and rejected

- Architecture 2, placing the 2025 retiring reading test's scores on the new scale by a concordance from the
  single-group bridge study (2026-10-27): solved on the portal. Both responses landed the call and one filed the
  runner-up and the gap exactly. The diagnosis is in `## Portal result and the diagnosis, 2026-10-27` below, and
  the world was then measured closed in `## The world is exhausted for this decision, measured 2026-10-27`: the
  repeater population moves counts 1 to 22 and leaves the slate intact, and the count-day rolls and the crosswalk
  are exactly clean, so no harder call survives in that world. The root cause is the client's rule 3 read the
  other way round: the decisive step was psychometrics' own named method for the deciding quantity, so a response
  that knows the field reaches it by reflex (the stage-4 leak reader had already named a symmetric equating at 241
  or below). Architecture 3 keeps the number and the ETL objective, takes a fresh world, and moves the field's own
  method into the default path, so the decisive step is a reconstruction of a capacity input that no field holds
  rather than a choice between two named methods.

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
- The retiring test on a continuous scale (every integer a possible score): the concordance conventions disagreed at
  the Level 1 boundary unless the bridge's share sat within a student of a cumulative step (an exact count match tied
  the at-or-below conventions, a gap of one to three students split the quantile cut's "below" and "at or below"); the
  retiring test is now a 30-item paper form whose raw-to-scale table leaves six to eleven points between scale scores
  near the cut, and all 30 conventions agree with 41 bridge students to spare.
- A bracket of the slate, the overcounting routes (inverse regression, the range match) also wrong: it needed grade 9
  cohorts two to three times the grade 10 ones in two districts; those routes land the golden six with every count
  wrong, and the ladder rests on the prediction and cohort routes.
- Equal cohorts statewide: matching the two cohorts' statewide percentiles or z-scores landed the golden; the 2025 grade
  8 cohort now reads 0.20 standard deviations below the 2026 one, which the bridge sample's retiring-test mean shows,
  and every cohort match places 231.
- Bridge draw 0: 53 per cent of its students with a retiring score of 241 sat at Level 1, so a per-score majority rule
  placed 241 at Level 1 and filed the golden; the bridge's schools are drawn again (draw 11: 43.5 per cent, all 30
  conventions still agreeing at every cut).
- A school realignment between two districts as an ask hazard, the vendor's file keeping the old district: the date of
  the move could not be read from the folder without a filed sentence, a fork; dropped.
- Asks on the students the count leaves out (no grade 8 result) or on the movers: the complement or a split of the main
  population, so a device on them moves the call's rows; dropped.

## Portal result and the diagnosis, 2026-10-27

**Both responses landed the call.** Each funded the golden six (Kessick, Varlow City, Brenmoor County, Calderidge
Unified, Garnet Hills, Elmorrow), and the second also filed the runner-up and the gap exactly: "Harlenbrook is first
left out with 353 eligible students, 15 fewer than Elmorrow's 368", which are the golden's own figures. So the second
response executed the concordance, not a route that lands the slate by accident. Architecture 2 is spent, and the
reason is in this note rather than in the portal.

**Cause 1, and it is the root: the decisive step is the field's standard practice, so it is a reflex.** The
`Domain test:` line says it outright: "psychometrics places one test's scores on another's scale by a concordance that
matches the two score distributions (equipercentile or linear linking ...), while a regression of one score on the
other is a prediction that pulls every converted score toward the sample's mean." The golden is that concordance. The
`## Readability screen` then rated the same move `silent` on test 3 with "no: the prediction reflexes and the cohort
match land on 231". Both cannot be true. If the field's own method for the deciding quantity is the golden, a
competent analyst applies it; what the screen measured was that the *wrong* routes are also reflexes, which is not
what test 3 asks. Test 3 asks whether the decisive move is an opponent default, and for anyone who has linked two
tests it is the first thing they reach for.

**Cause 2: the stage-4 reader had already solved it, and its answer was read for its taxonomy rather than its
content.** Round 2's question 6 says the easy routes "swap Elmorrow and Harlenbrook; a symmetric equating (less than
or equal to 241) does not". That is the decisive step, the correct cut and the correct consequence, in the reader's
own words, before the build shipped. It was recorded as a pass because question 6's answer was "an analytical
choice", which it is: the step's KIND was never the problem. Gate F was, and the evidence for failing it was sitting
in the same paragraph.

**Cause 3: the slate is landable without the decisive step.** The `## Ladder` records it: R2 (inverse regression) and
R2b (the two scales' ranges matched) both file "the golden six, every count high". Three of the seven rungs land the
call, so a response that links the scales wrongly in the other direction still banks the recommendation. Only the
counts separate them, and the counts are ask weight, not the call.

**What this does not need.** The determinism is sound (two judge passes on file), the pack and its Layer 1 inventory
measured sound, the asks are decoupled and the conformed-file deliverable is good. The world, the fourteen applicants,
the two vendors and the count-day machinery can all be kept. What has to move is the decisive step.

**What a re-root needs here.** A decisive step that is not the field's named method for the deciding quantity, that no
competent reflex reaches, and that the records force to one execution. The test to apply at the draw, from this
failure: if the `Domain test:` line and the `Decisive step:` line name the same method, the screen's test 3 fails and
the draw is not ready.


- Architecture 2's decisive step, the concordance against the regression prediction (2026-10-27, on the portal
  result): spent. Both responses landed the call and one filed the golden's runner-up and gap exactly. The step is the
  field's own standard practice, which the note's `Domain test:` line states and the readability screen then rated
  silent on test 3; a reflex reaching the golden spends the stump whatever the step's kind. The stage-4 reader had
  already named the symmetric equating and the 241 cut in its own words, which was Gate F evidence recorded as a pass
  because its question-6 answer was "analytical choice". Compounding it, R2 and R2b land the slate too, so three of
  seven rungs reach the call and only the counts separate them.
- Defending the concordance better, or adding a rung above it: refused before it was tried, on task184's measured
  precedent in this repo. There, deleting the three clauses that licensed the textbook weight left the same answer
  reachable, because the reader had reached it unprompted; the note's conclusion was that the golden has to move off
  the textbook move rather than be better defended. The same holds here: the equating is reachable from the bridge
  file alone.

## The world is exhausted for this decision, measured 2026-10-27

Before drawing architecture 3 I looked for a decisive step in this world that is not the test placement, because the
placement is the reflex that spent architecture 2. The pack was re-measured from `target.zip` directly, and the
reconstruction reproduces the golden exactly (sixth 368, seventh 353, gap 15), so the measurements below are against
the shipped truth and not against a re-derivation.

**What the pack still holds that architecture 2 never used.** The grade in 2026-27 does not determine which
instrument carries a student's grade 8 result, because students repeat grades:

| Population | Students |
|---|---|
| Grade 9 with a new-test grade 8 result (the expected path) | 22,513 |
| Grade 9 with a retiring-test grade 8 result only, so grade 9 repeaters | 610 |
| Grade 9 with both, so grade 8 repeaters whose latest result is the newer one | 326 |
| Grade 10 with a retiring-test result (the expected path) | 22,351 |
| Grade 9 or 10 with no grade 8 reading result at all | 1,063 |

That is 936 grade 9 students whom a pipeline keyed on grade either drops or places on the wrong instrument, and the
spent default path's own step 4 ("Grade 9 on the new test") does exactly that.

**And it does not move the call.** Measured per district against the golden: the by-grade pipeline moves every count
down, by 1 to 22 students, and leaves the slate and the boundary where they were (sixth 1220 at 363 against 368,
seventh 1240 at 349 against 353, the gap 14 against 15). The ordering is untouched.

**So the only lever in this world that moves the funding boundary is the placement of the retiring test's scores on
the new scale**, which is the field's named method and the reflex that failed. Everything else is measured flat: the
count-day roll has no ambiguity at all (88,329 covering spells, zero students with two, zero on two districts'
rolls), the examinee crosswalk is exactly one to one in both directions (71,949 ids each way, no fan-out), the
students with no result cannot be counted at Level 1 under any reading, and the ladder already measured the retiring
test's own performance levels as a rung rather than a lever.

**Conclusion: architecture 3 cannot be drawn in this world.** Any call this pack can ask routes its analytical content
back through test linking, because linking two scales is what this world is about. The re-root keeps the number and
the ETL objective and takes a fresh world, which is a full stage-1 draw and a new pack rather than a repair.


- A decisive step built on the repeater and off-instrument populations, in this world (2026-10-27, measured before
  the draw): refused on magnitude. The structure is real, 610 grade 9 students carrying only a retiring-test grade 8
  result and 326 carrying both, and the spent default path mishandles all 936. But it moves each district's count by
  only 1 to 22 students and leaves the slate, the sixth and seventh places and the gap intact, so it cannot carry a
  call. It also sits on the hygiene battery's own unmatched-join check, which the opponent runs.
- Keeping this world for architecture 3 at all (2026-10-27): refused on the same measurement. The placement of the
  retiring scores on the new scale is the only lever that moves the funding boundary, and it is the field's named
  method, so every call this pack can ask routes back through the reflex that spent architecture 2. The count-day
  roll, the crosswalk and the unresulted students are each measured flat. The re-root takes a fresh world in the same
  objective and number.
