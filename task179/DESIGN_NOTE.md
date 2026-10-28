# task179 design note

**Architecture 5, drawn 2026-10-28: criminology-justice / recidivism-risk-assessment (Forecasting).** Architecture 3
(the Corriemoor first-year entrants' repeat classmates) was returned on 2026-10-25 for Duplicate against task175, and
architecture 4's candidates (probes 5 to 10, candidates B and C1) died before any card registered; both are in
`## Tried and rejected`. Under `CLAUDE.md`'s STOP block no probe, solver or scored reader is run on this draw: the stump
is argued on paper against the nine survivor properties (`## Draw`) and measured by the portal alone. Everything worked
on this number before is kept below as history (`## Tried and rejected`, `## Earlier architectures`).

## Draw

| Item | Value |
|---|---|
| Card | `cards/task179.json` architecture v5, registered 2026-10-28; v2 and v3 in its lineage |
| Pairing | criminology-justice / recidivism-risk-assessment, Forecasting & Predictive Modeling; client domain Criminology & Justice |
| Call | how many of the people on Region 4's supervision caseload at the end of 31 December 2026 will be booked into either county jail at least once in 2027 on a new charge on Directive 26-07's Schedule B (a violent felony or a firearm offence) while still under Region 4 supervision, to the nearest 50; the figure sizes the GPS enrolments the Region reserves in its 2027 order, since the directive places every such supervisee on GPS from 1 January 2027 |
| Shape | other: the call and its critical components, then the asks (the 2026 Schedule B booking notices by jail and quarter, the 2026 GPS days the vendor may bill by month, the year-end caseload by county and risk level), in two deliverables, an order workbook and a forecast memo |
| Strategy | other: an acute dynamic risk factor recorded only by another agency (violent victimization in the city police's incident records), linked to the caseload by name and date of birth, whose prevalence nearly tripled in the second half of 2026; Layer 2 family field_method |
| Gap, pattern, Gate G | time then population; G12 (the supervision record's silence on victimization is an absence of record, not a record of absence) and G14 (the raised booking hazard is conditioned on a victim record in the window before the year end); forecasting |
| Forum, forcing event, org, role | executive_team (the Region's executive team signs the order); purchase_order_or_contract (the 2027 GPS order reserves enrolments in advance); government_agency; research_desk (the Region 4 research and planning lead) |
| People | Zachary Wallace and Ashlee Evans, from `guard.py names --geo us --seed 179` |
| Spine | `cms_supervision_episodes_2018-2026.csv`, one row per supervision episode open at any time from 2018 to 2026 (person x episode) |
| Seed | none: drawn without a seed; the world (a state supervision region of two counties and one city) is new to the lane |

**Why this cell.** The directive excludes the domains probes 6 to 10 used (Actuarial, Sociology and Demography,
Economics and Econometrics, Energy) and Education, healthcare delivery and product analytics. Criminology & Justice
serves Forecasting through one task type, recidivism-risk-assessment, which `guard.py check` passes for this card;
task141 (violator pods under a term cap) and task169 (parole returns re-routed through the courts) sit in the same cell
with other drivers, and this draw keeps away from their furniture: no jail capacity decision, no statute changing who is
revoked, no commission, a vendor order instead of a jail plan.

**The guard's answers.** `guard.py check` on the card: WARN, no BLOCK.
- overuse.org_family (government_agency, in 41 builds): a state corrections department's supervision region is a
  government agency; local_government would misstate it, and no other family is honest.
- repeat.gate_g (forecasting, task118 v3 and task304 v2): the objective is Forecasting and the deciding quantity is a
  forecast; task118 v3 (a deprescribing team's fall admissions) and task304 v2 (a hepatitis C charity's van) share only
  the tag.
- repeat.deliverables (docx and xlsx, task118 v3): a planning lead sends a contracts office the order workbook and a
  short memo; task118 v3 is a health build in another domain and retired.
- test.same_puzzle_older and test.same_driver_older (time, G12, quantity_figure, forecasting): differentiated on the
  card against task157 v1, task192 v2, task482 v10, task231 and task250 v2 (a defect seen only when both members of a
  sampled pair fall in the sample; an instrument's labels after its validation window; episodes recorded only at their
  end; exits reaching the record a year late; alerts a less sensitive limit would raise). None reads an exposure a
  second agency records about the same people under another role.
- Abstraction test against the nearest drivers (0.07 to 0.08): task179 v3 (this slot: repeat classmates in a cohort's
  own classes) and task177 v3 (one event leaving the paying body) are each a member's own record; task137's candidates
  (a new site's demand, pairs of exposures, a register of long-term members) read the provider's own files. The
  closest in shape is task166 (founders linked to leavers across customers' workspaces by mobile number): the same
  device, a link across two bodies' records, but its quantity is a pipeline of new arrivals produced by another
  population's exits, while here no new member arrives and nobody leaves: each existing member's own hazard is raised
  by an event a second agency records about that member in another role.
- `guard.py slots` on the mechanism's words (victim, victimization, overlap) and the setting's (supervisee, probation,
  parole, booking, jail, police) found no slot note with this mechanism; task141's jail extract with UTC times is a
  Layer 1 neighbour, so this pack's UTC jail is the second county's whole extract, not a mid-series switch.

**Data-native sentence.** The city police record a victim by the name and birth date given at the scene and never by
the state identification number, because victims are not fingerprinted, so a supervisee who is shot or assaulted
appears in the police extract as a stranger, while the jails' booking notices carry the state number of every
supervisee they book.

**A line per source.**
- The client's `recidivism-risk-assessment` rigor cards (calibration is not discrimination, fixed follow-up, later
  cohorts for validation, selective labels, local base rates) are the default path's own virtues here: the easy route
  validates on later year ends, follows each person for a fixed year and is well calibrated overall; the decisive step
  is none of them, it is an exposure the instrument never scores.
- The criminological literature on the victim-offender overlap (violent victimization raising later violent offending
  and weapon carrying) is the domain's knowledge the step uses; supervision risk instruments score criminal history,
  attitudes, associates, employment and substance use, and no instrument on file, nor any build, scores a police
  victim record.
- task166 and task137 v4, the two builds that held on the portal with a linked second record, are the anatomy the
  nine properties below were read from; this draw takes the anatomy, never their drivers (a founder pipeline,
  deterrence after run-outs), both banned for this number.
- The death record of probes 5 to 10 and candidates B and C1 (`## Tried and rejected`) set what the anatomy must
  avoid: a column for the actor (probe6), the domain's own reflex (probe7), a filed event or precedent (probe8), the
  textbook model's strongest feature pointing at the driver (probe9), a keyed join and a shock that is the largest file's
  largest spike (probe10).

**The nine survivor properties, argued** (prototype `scratchpad/t179_a11/proto2.py hr=8 surge=6 sm=7 vwb=-0.8 seed=1`,
a monthly simulation of the caseload, its bookings and the city's violent victimizations from 2014 to 2027, fitted
exactly as the default path and the golden would be on the built pack; the generator re-measures every figure at stage 3).

1. **An actor with no column.** No supervision, assessment or jail file carries victimization: the case-management
   export has offence, priors, terms and addresses, the instrument scores seven needs domains, and the jails record
   only bookings. The actor is whoever assaulted the supervisee, recorded by a third agency.
2. **A signature only through an untypical link inside the main data.** The raised hazard shows only once the police
   victim rows are matched to the caseload; the link is a victim to a supervisee, the opposite role from every link a
   supervision analyst runs (arrestee to supervisee, by state number).
3. **A textbook route that back-tests well.** The own-attribute model (age, sex, priors, offence, supervision type,
   months remaining, risk score, recent bookings) back-tests on the 2022 to 2025 year ends at 429 against 430, 440
   against 421, 415 against 443 and 390 against 434 on the prototype; the generator holds every back-test within five
   per cent (a stage 3 assertion), and the model's 2026 caseload mean risk equals 2025's (0.0549 against 0.0559).
4. **No framing or helper file that exposes the step.** The pack ships no data dictionary, no memo on violence, no
   research brief on victimization; the directive defines Schedule B by statute and the vendor's order form counts
   enrolments; nothing names the police file as a source of risk.
5. **A mechanism a practitioner would not name unprompted.** The overlap is a research finding, not a forecasting
   input: no supervision instrument (LSI-R, ORAS, COMPAS, the state's own) scores victimization, and a planning lead
   forecasting bookings reaches for the instrument, history and terms. The police file sits in the pack for an ask
   (below), so its presence is explained without the step.
6. **No strong textbook feature pointing at the driver.** The prototype's own-attribute model ranks months remaining
   (0.50 in coefficient times standard deviation), age (0.33), risk score (0.32), sex (0.26) and a violent lead offence
   (0.25) first; none moves in 2026 (mean risk 0.0549 against 0.0559), and the textbook score predicts who carries a
   2026 victim record no better than general risk does (AUC 0.675). Asking what changes any of them leads back to the
   caseload, never to the police.
7. **The shock's file has its own evident purpose.** The city police's violent-incident extract (one row per victim per
   incident) is in the pack because Directive 26-07 requires a GPS exclusion zone around each victim of a supervisee's
   Schedule B charge who lives in the city, and the vendor bills each zone: an ask counts the 2026 zones by joining the
   bookings to the incidents on the arresting agency's case number, a keyed join on the offender side.
8. **The link is an identity resolution across records of different entities that no key joins.** Victims carry no
   state number; the police write `LAST, FIRST M` with dates as `MM/DD/YYYY` and the case-management export separate
   name fields with ISO dates; the match is a cleaned surname, given name and birth date, and the generator asserts it
   unique (no two people share a cleaned name and birth date, every true match agrees after cleaning).
9. **The shock reads as ordinary, explained movement and is not the pack's largest anomaly.** The city's recorded
   violent victimizations fall 4.2 per cent in 2026 (12,479 to 11,949), continuing the decline from the 2021 peak
   (-7.1, -10.8, -8.5, -5.7 per cent a year), with every district down (-0.9 to -9.3 per cent) and September to December
   2026 inside the monthly year-on-year range of 2019 to 2025 (-17.4 to +22.7 per cent). Supervisees are 2.6 per cent of
   the city's victims in 2025 and 6.6 per cent in 2026, visible only after the link. The pack's larger anomalies are
   ordinary and explained: the 2020 to 2021 rise in violence (+10.3 and +14.6 per cent), the spring 2020 booking
   collapse, the June 2022 case-system migration and the July 2024 recodification of every statute.

**The prototype's call.** The own-attribute model files 426.4 (450 at the nearest 50); the same model with a 2026
victim record (the twelve months before each year end, as fitted on 2018 to 2025) files 496.2, and every linked form
sits from 488.5 to 499.5 (the AIC-best, the twelve months, the twelve to twenty-four months and ever, 494.4), 500 at the
nearest 50. The 2027 truth the prototype simulates is 497. The cheap routes off the record land 383.0 (recalibrated on
the latest back-test), 395.8 (2026's rate on the 2026 caseload) and 426.3 (a district violence covariate).

## Three rules

- Task type: criminology-justice / recidivism-risk-assessment, which serves Forecasting: the 2027 count of a supervision caseload's people booked on a new violent-felony or firearm charge, forecast person by person from their risk.
- Domain test: the quantity that decides the call is the year-end caseload's 2027 count of people booked on a Schedule B charge, which recidivism risk assessment forecasts as each supervisee's booking hazard over a fixed year from static and dynamic risk factors; the dynamic factor that moved is acute, recent violent victimization (the victim-offender overlap), measured by linking the city police's victim records to the caseload by name and date of birth and carried into 2027 for the two years the record shows the raised hazard lasting.
- Swap: "how many of a hospital's discharged patients will be readmitted in 2027": a readmission is not raised by a police victim record, no overlap between victims and offenders exists, and no second agency records the patients under another role by name alone, so the linked exposure that decides this call stops meaning anything.
- Layer 1: every mess item comes from the agencies' own systems: two county jails' booking notices in different layouts (one row per booking charge in local time; one row per booking with charges concatenated, in UTC), warrant-only, violation-only, court-transport and hospital re-bookings beside new arrests, the July 2024 recodification with its crosswalk published as a PDF table, the June 2022 case-management migration with legacy offender numbers on the older assessments and merged duplicates in the crosswalk, concurrent episodes for one person and county transfers closing and reopening an episode, the 2023 revision of the risk instrument with new cut-offs, the police's victim names and birth dates in their own layout with supplements re-listing victims and business victims with no birth date, the vendor's device swaps; nothing placed to be caught.
- Layer 2: field_method, a forecast whose information set omits an acute dynamic risk factor: a supervisee's Schedule B booking hazard is raised for about two years after a police victim record, the caseload's victimization nearly tripled in the second half of 2026, and a risk model on the caseload's own records cannot see either; adding the linked exposure flips the call.
- Decisive step: recognising that a supervisee recorded as the victim of a violent incident is booked on violent and firearm charges at several times the risk model's rate, linking the city police's victim rows to the caseload by cleaned name and date of birth, estimating the raised hazard on the 2018 to 2025 year ends and scoring the 31 December 2026 caseload with its own 2026 victim records.
- Not semantics: every field reads plainly (a booking type, a statute, a victim's name and birth date, an episode's dates) and reading all of them correctly still leaves the risk model on 450, because no supervision or jail field carries victimization and the police file never names a supervisee: the deciding exposure exists only once two agencies' records of one person in two roles are matched.
- Not rule application: no filed rule, directive or form says victims are at raised risk or that the police file belongs in the forecast, and executing Schedule B, the booking types and every counting rule files 450; enumerated family on the prototype: own-attribute logistic models, recalibrated on the latest back-test, the 2026 rate on the 2026 caseload, a district violence covariate and the linked forms (twelve months, twelve and twenty-four, six and six to twelve, a count, ever, all three), 383.0 to 499.5 across three printed calls (400, 450, 500); standing family: the linked forms, since the record's own control shows the 2018 to 2025 victims booked at several times the own-attribute model's rate (an odds ratio of about 5.6 on the twelve-month flag), 488.5 to 499.5, one printed call (500); the ruling-out is not loud: no file, field or one-group-by names victimization, the city's count falls in 2026 and the own-attribute model back-tests within its noise, so only the link shows it.
- Analyst test: with both jails' notices conformed, the recodification mapped to Schedule B, the migration crosswalked and each person counted once, the easy route fits a Schedule B booking model on each year end's own risk score, age, sex, priors, offence, supervision type, months remaining and recent bookings over 2018 to 2025, back-tests it on the later year ends, scores the 31 December 2026 caseload and files 450, because it never links the city police's victim records to the caseload, so the second half of 2026's rise in victimization never enters it.
- Estimand: the prompt files it: the people with an open Region 4 supervision episode at the end of 31 December 2026, counted once, who are booked into the Darrow County Jail or the Keswick County Jail at least once from 1 January to 31 December 2027 (local time) on a new charge that Directive 26-07's Schedule B lists, while their Region 4 supervision is still open, to the nearest 50; Schedule B and the booking types sit in the directive, the population in the case-management export.
- No decoy: nothing is planted: the victimization rise is ordinary police records of ordinary incidents, no memo, brief or file argues a figure or ranks anything on 2027, the statewide recidivism brief and the programme referrals are distractors named in `metadata.json`, and the police file is in the pack for the exclusion-zone ask it serves.
- No certified replay: no certified or published figure is reproduced to recover a method: the raised hazard and its duration are estimated from the linked records, and no file states a 2027 figure or a past year's forecast.
- Lesson: a risk forecaster learns to ask which acute risk factors moved since the instrument was scored and which agency records them: a caseload's violent victimization is recorded only by the police, under names, and a surge in it raises next year's violent and firearm bookings where no static factor moves; no build on file forecasts an outcome from an exposure another body records about the same people in another role, linked by name and birth date.

## Tried and rejected
- **Architecture v2 (the serial interval read from transmission links right truncated at the extract), spent at stage 4 Gate F on target.zip 9e1843f8:** scored reader B landed 5,000 cases, R 1.6 and 13 days on its own first route, "Serial interval: onset differences on transmission links where both ends are cases; sources with early onset (right-truncation), mean about 13 days, gamma (shape 2.86, scale 4.6). R from r via gamma moment generating function: 1.59", then the renewal projection with the halving from 2 November; it kept 0 of 16 ask figures. The correction is a reflex at medium effort in this field (the textbook nowcasting caution), so it was the default path, not the stump; the judge and reader A were stopped.
- **Architecture v2's first world (a named real disease in a named real province):** declined on the real-places records concern, since its pack would be fabricated public-health records of a real outbreak; the mechanism was re-sited unchanged into the fictional Republic of Orvanthe.

- **Candidate 1: the district's requirement read from the areas' joint evenings, against the closed summers'
  area-by-area staffing, the areas treated as independent, a square-root pooling law and a pooling discount** (the
  brief's first and second ideas; `c1_pool.py`, `c1_summary.py`, `c1_station.py`, `c1_total.py`, seeds 1, 2 and 3
  fixed before outcomes).
  Killed at stage 1 on measurement and on the estimand screen.
  - The world: five planning areas whose block calls are Poisson around a lognormal intensity carrying a city-wide
    evening factor (weather, events), a district factor and an area factor, Friday 0.95, Saturday 1.15 and Sunday
    0.88, 3 per cent a year; 2026 means 14, 12, 18, 10 and 15 calls a block; summers 2021 to 2026 (236 evenings),
    the truth simulated on 200,000 evenings of 2027.
  - The golden family on one pack (the district's evening totals rescaled to 2027 by their own log-linear trend and
    quantiled: type 7, type 1, Harrell-Davis, last three summers, area trends summed, additive rescaling, a negative
    binomial by weekday mixed): at the base world (city factor 0.15, district 0.05, area 0.10) North 10.92 to 11.22
    continuous units, Central 11.43 to 13.37, South 6.40 to 7.03 for the type 7 member, the family spanning two
    whole numbers in 6 of 9 district-seeds, a bootstrap sigma of 0.47 to 0.58 (North), 0.53 to 0.69 (Central) and
    0.38 to 0.44 (South).
  - The sweep, North and Central over three seeds (sigma, family spread on one pack, the area-by-area default's
    units above the golden, and how often independence and the square-root law land the golden's whole number):

    | World | Sigma | Family spread | Area-by-area | Independence lands | Square-root law lands |
    |---|---|---|---|---|---|
    | city factor 0.05 | 0.43 | 0.44 | +1.50 | 6 of 6 | 6 of 6 |
    | city factor 0.15 (base) | 0.58 | 0.62 | +1.17 | 3 of 6 | 4 of 6 |
    | city factor 0.25 | 0.71 | 0.88 | +1.33 | 5 of 6 | 5 of 6 |
    | city factor 0.35, area 0.15 | 0.91 | 1.02 | +1.00 | 0 of 6 | 0 of 6 |
    | nine summers (2017 to 2026 less 2020) | 0.40 | 0.61 | +1.50 | 5 of 6 | 5 of 6 |
    | twice the size | 1.51 | 1.19 | +1.67 | 0 of 6 | 0 of 6 |
    | small Poisson districts (means 4 to 6 an area) | 0.24 | 0.22 | +1.00 | 6 of 6 | 6 of 6 |

  - The lever at the truth: area-by-area staffing needs one unit more than the district in North and Central (13
    against 12, 8 per cent of the units a district needs), one or two at twice the size, none in South, against the
    brief's 30 per cent. Staffing station by station in the closed summers (three station areas a planning area)
    raises it to 29 to 33 per cent (16 against 12, 9 against 7) and changes nothing else below.
  - One dial: the independence and square-root routes miss only where the city factor is strong enough to make the
    golden's own sigma 0.91 units or more and the family spread a unit; where sigma falls toward 0.24 they land in
    every district-seed. No world puts both rivals a bin away while the golden holds a quarter-bin and one sigma.
  - The eda6c8c screens, as code (`screen179.py`): dispersion fires (the co-movement is estimated, and on one pack
    the family spreads 0.49 to 0.78 units); variance-only passes (area-by-area +0 to +2, independence -1 to +0, the
    point moves); the common-exposure subset fires in 6 of 6 district-seeds, since the district's own evening totals
    filtered, summed and quantiled are the golden, a filter and a sum with no model; truncation direction: blanking
    station cells of one or two calls (13 to 21 per cent of evenings carry one) leaves every district's units
    unchanged at an imputation of 0, 1, 1.5 or 2, so the suppression hides the bottom and is Layer 1 at most.
  - Why it is dead whatever the tuning: pooling is the estimand's unit (the district's block, which the standard
    has to file), so filing it makes the computation follow and the strong analyst's first build, the district's
    own totals, is the golden (rule 3, rule application); the co-movement reading is task143's driver; and the
    sigma floor above holds at every size.
- **Candidate 2: next summer's level against the record's, a trend, an accelerating district, a break and a
  one-off, each route priced in whole units and the route chosen on the 2025 and 2026 summers held out** (the
  brief's third and fourth ideas; `c2_level.py`, `c2_sigma.py`, seeds 1, 2 and 3 fixed before outcomes, then 101
  to 120 for the routes' own sigma). Killed at stage 1 on measurement. Built on small Poisson districts (2026 means
  North 16, Central 20 and South 11 calls a block, city factor 0.06) so that the percentile's noise is the smallest
  the world allows; summers 2018, 2019 and 2021 to 2026, spring weekends through April 2027.
  - The routes: the last summer flat; the last summer times the record's trend; every summer detrended; the last
    three summers on their own trend; the last summer times spring 2027 over spring 2026; a quadratic trend; the
    plain mean of the summers.
  - A, 3 per cent a year everywhere: Central's truth 9 units (8.10 continuous); the routes' means over 20 seeds
    7.36 to 8.42, their own sigma 0.19 to 0.45; on seeds 1 to 3, 5, 3 and 5 of the 7 routes land the truth's whole
    number; the back-test lands the truth in 13 of 20 and picks six different routes across them (every summer
    detrended 9 times, the last summer flat 4, the last three 4).
  - B, North's growth accelerating from 4 to 9 per cent a year from 2022: truth 8 (7.20); routes 5.40 to 8.31 on
    seeds 1 to 3, 2, 1 and 3 of them landing; the back-test right in 1 of 3.
  - C, Central 18 per cent lower from January 2025 (a diversion programme): truth 7 (6.90); routes' means 5.95 to
    7.17, sigma 0.15 to 0.48; on seeds 1 to 3, 4, 3 and 7 of 7 routes land; the back-test lands the truth in 17 of
    20, picking the plain mean of the summers in 8 of them (and on seeds 1 to 3 every time), which lands by
    cancellation (the break against the trend, mean 6.94).
  - D, South 20 per cent higher in summer 2026 only: truth 5 (4.80); only the plain mean lands (4.49, sigma 0.10),
    the flat hold once; the back-test lands the truth in 2 of 20 and never picks the plain mean.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply (a level, no suppressing
    threshold on the path); variance-only passes (on seeds 1 to 3 each scenario's routes spread 0.58 to 2.91
    continuous units); the common-exposure subset fires, since the summers already at the coming level, filtered
    and quantiled (the last summer, the last three on their own trend), land the truth in 8 of 12 scenario-seeds
    (all three of A and C, one of B and of D).
  - Why it is dead: the levers a trend, an 18 per cent break, a 20 per cent one-off and an accelerating district
    can buy are a unit or less on districts this small, against routes whose own sigma is 0.10 to 0.48 units (0.26
    to 0.48 for every route that carries a trend), so the flat hold, the plain mean and the last summer land, two
    wrong steps cancel (scenario C), and two held-out summers of 39 or 40 evenings cannot select the route (it lands the
    truth in 2 to 17 of 20 depending on the scenario). On larger districts the levers grow with the noise, as
    candidate 1's sweep shows.
- **Paper screens, not coded.**
  - Heat normalised over a long weather record: the lever is the record's weather sample against climatology,
    whose sign the draw sets, and the recent summers are the better guide to a warming climate, so the reading is
    contested.
  - A new venue's or team's weekend evenings on a filed event calendar: `composition_mix` (held by task165 and
    task268), the coming window's cells unfilled, and the venue's own event evenings filtered and divided hand it
    over.
  - A new development's occupancy: its occupied dwellings' rate times the forward occupancy is two filters and a
    divide.
  - An alternative-response or sobering-centre pilot going city-wide: a filed forward condition, the pilot
    district's own post-period evenings at the coming exposure, and a lever of a few per cent of block calls.
  - A frequent-caller programme and its regression to the mean: a lever of a few per cent.
  - Calls passed to county mutual aid or held when an area's units were all committed (capacity-censored demand):
    task168's driver, and a mutual-aid log that records every overflow call makes it a join.
  - The county's own units cut, so more of its calls overflow to the contractor (a loss model): task156's driver
    (work reaches a second tier only when the first falls short).
  - Hospital offload delays or cross-area travel lengthening each call under district dispatch: the 1.2 unit-hours
    a call is part of the filed estimand, and leaving it open makes the quantity a duration times a count,
    task142's driver.
  - Peak concurrency inside the block: task142's and task148's drivers, and the filed unit-hour standard does not
    ask for it.
  - Summing the block's hourly 90th fractiles (the demand-pattern reflex) or the stations' requirements: the
    estimand's unit again, which a strong analyst reads off the standard.
  - The predictive spread widened by next summer's own level shock: variance-only, the golden always above the
    plug-in, so a padding reflex lands it.
  - A summer-specific growth against all-year growth: a lever of a few per cent a year.
  - One 9-in-10 condition across the three districts jointly: the estimand again, and once filed the joint
    record's evenings answer it by a count.

- **Redraw cell, 2026-10-19: Economics & Econometrics, `time-series-macro-econometrics`, Forecasting.** The cell's
  three library cards (cointegration critical values, the Johansen rank's deterministic terms, shock identification)
  were read first; `guard.py recent`, `coverage`, `mechanisms --objective forecasting` and `slots` (pass-through,
  asymmetric, invoicing, indexation, cointegration, error correction, recovery, seasonal, mortgage, lock-in, rent,
  catch-up, settlement, Phillips, kink, capacity utilisation) ran before any candidate. No build on file sits in this
  task type. The live window at a932f79 is task249, task177 and task270 (strategies `causal_design`,
  `forecast_method_backtest`, `population_selection`; patterns G14, G16, G12; task269 is spent and skipped). Prototypes
  in the session scratchpad, b179r/screen: `s1_cp.py`, `lm1.py`, `d1.py`, `w1.py`, `w2.py`, and `screen179r.py`, whose
  output `screen179r.out` is byte-identical with `screen179r_run2.out` (as `lm1.out` is with `lm1_run2.out`). Seeds
  were fixed before outcomes. No card was drafted, because nothing passed the measurement.
  - **Measured: a business survey's up, same and down shares against the quarter's mean output move** (the balance
    bridge against a quantification that scales the shares by the firms' spread, Carlson-Parkin; `s1_cp.py`, 20
    world draws a scenario, 1,500 firms a quarter, 127 quarters, t(5) firm growth). At ordinary spread the balance
    bridge lands (truth -1.0: balance -0.86, golden -0.98); only a deep fall at an unprecedented spread separates it
    (truth -3.0 at spread 12: balance -1.80, the up-and-down two-share regression -2.55, golden -2.89 with a sd of
    0.35, 12 per cent of the figure). The nearest reflex sits about one golden sigma away, the golden's own sigma is
    an order above the bar, and the separating world needs a recession no record has seen.
  - **Measured: long memory, a fractionally integrated series against the AR chosen by AIC and the KPSS-chosen unit
    root** (`lm1.py`, 40 draws, d 0.4, 480 months, the mean of months 25 to 36). The AR by AIC, the AR(1) and the
    estimated-d forecast agree (mean absolute errors 0.605, 0.593 and 0.599 sd units, the random walk 0.936), and all
    three miss the truth through the sample mean's own long-memory error (correlation -0.89 to -0.93 with it). No
    lever between the textbook route and the golden: the residue is the mean, not the method.
  - **Measured: national excess unemployment twelve months on when the shock sits in the slowest regions** (bottom-up
    regional persistence against the national AR; `d1.py`, 30 seeds, eight regions at monthly persistence 0.90 to
    0.985). The national AR understates the remaining excess by 0.108 (24 per cent of 0.459); the bottom-up AR(1)
    overshoots by 0.087 with a sd of 0.085, so the golden's own error is the size of the lever, because forty years
    of monthly data pin a near-unit-root persistence too loosely. By abstraction it is also composition weights that
    moved (task95, task446).
  - **Measured: new collective agreements' annualised increase once a long pre-surge wave expires** (the catch-up of
    real pay lost since each agreement's own last settlement; `w1.py`, `w2.py`, seeds 1 to 5, about 13,600
    agreements over 2000 to 2027). On the 2027 approvals the trailing-inflation regression lands within 0.15 to 0.50
    points (2.50 against truths of 2.64 to 3.00, 5 to 17 per cent); the symmetric catch-up regression misses as
    badly (2.20 to 2.57) and only an asymmetric catch-up lands (2.61 to 2.95), so the decisive step became the
    asymmetry, a 0.4-point split inside the golden family against the lever. Catch-up since the last settlement is
    also the first thing a labour economist checks after a surge, a cousin of task165's gain conditioned on each
    unit's own baseline, and the settlement regression is panel estimation rather than this task type.
  - Paper: invoicing-currency (dominant-currency) pass-through into import prices is task145's driver (units differ
    in which currency they hold fixed), and task153 rejected its pass-through cousins.
  - Paper: asymmetric error correction in a retail price (rockets and feathers) is the adjustment-speed cousin
    task153 rejected.
  - Paper: phase-asymmetric unemployment (steep rises, recoveries at a steady log pace) against a linear AR: a gap
    closing at a fixed pace rather than in proportion is task161's driver (own-use burn against a half-life), its
    honest strategy `forecast_method_backtest` (a regime) is in the window (task177), and the pace of past
    recoveries, the natural analogue, is the golden.
  - Paper: a rent index under a cap on sitting-tenant increases with vacancy decontrol (a backlog drawn down at the
    cap, a nonlinear error correction): fixed-rate drawdown is task161's driver and the saturation task79's, and once
    the cap is filed the sitting tenancies' path executes it.
  - Paper: a convex price response to capacity utilisation read from an industry panel is task79's kink (task149
    rejected the same).
  - Paper: mortgage-rate lock-in holding down housing transactions and transfer-tax receipts is task166's driver
    (units whose own rate the terms beat).
  - Paper: a moving lunar holiday (Ramadan and Eid) in a monthly flow or in banknote demand is task162's
    calendar-locked alignment, and a strong reader models it.
  - Paper: a reset-month step in a price index sized by trailing inflation (state-dependent seasonality from annual
    indexation), and year-end appropriation spending sized by the unspent balance: both task146's driver (a step at a
    calendar turn is not a fixed seasonal share).
  - Paper: downward nominal wage rigidity bending aggregate wage growth: at plausible desired growth for 2027 (1 to 3
    per cent, a worker sd of 3) the floor moves aggregate growth 0.09 points from a linear extrapolation, and
    aggregation over a per-unit floor is task16's driver.
  - Paper: cointegration and error correction against a VAR in differences or ARIMA, including the partner that
    reveals a shock's permanence and a trend in the cointegrating relation: the cell's own cards 1 and 2 applied as
    stated, which the library test says a blind reader lands; where the golden is no reversion, ARIMA lands it; and
    `coint` applies MacKinnon's critical values by default.
  - Paper: signal extraction from a sampled series: IMA(1,1) is the optimal filter for a random walk plus noise and
    lands, and autocorrelated sampling error needs the filed design variance (rule application).
  - Paper: a minimum wage's effect through its bite is task165's untreated part; the shadow rate at the lower bound
    is markets and lending ground, with a rule fitted on off-floor quarters both the default and the golden; an
    uncertainty hold on a trend-growth revision (HAC against iid) fails the variance-only screen; inventory payback,
    the accelerator and the carry-over are accounting a strong reader states; tariff diversion to untariffed origins
    is a product-panel elasticity outside this task type and close to task88's displacement.
  - The cell finding: the field's textbook routes (ARIMA, VAR, VECM, bridge, X-13) are routes a blind reader takes,
    and every structural judgment beyond them that this search found is either a driver on file by abstraction
    (fixed-pace drawdown, a kink, a calendar turn's step, a conditioned gain, a moved mix, a lock-in, pass-through)
    or, where it is new, carries a golden whose own sigma (12 per cent, 18 per cent of the figure) or family split
    is the size of its lever, because macro aggregates rest on too few independent events. Micro registers give the
    precision and move the work out of this task type.

- **Rebuild screen, 2026-10-23: product-analytics / `feature-adoption-diffusion-modeling`, Forecasting** (the number
  reopened under the author's rule; worktree `b_179n`). The cell's three library cards (novelty against durable use,
  the eligible denominator in a staged rollout, censored non-adopters) and the field's textbook routes (a Bass curve
  fitted to the adoption series, analogue launches, a logistic on account features) were taken as the default path;
  task144's spotlight cascade through follower feeds and task162's calendar-locked restart burst were read as spent.
  `guard.py recent` at a544497 put task173, task178 and task482 in the window. Three candidates measured on code
  (scratchpad b179n/screen: `a1.py`, `a2.py`, `b1.py`, `c1.py`; `screen179n.out` byte-identical with
  `screen179n_run2.out`; seeds fixed before outcomes) and sixteen on the structural screens; no card was drafted.
  - **Measured: contagion local to each customer account against the Bass curve's global mixing** (each non-adopter's
    weekly hazard p plus q times the adopted share of the user's own account; 3,000 accounts, lognormal sizes median 6,
    the feature live 39 weeks). Over a 13-week window the recent pace lands (+1.4 and +4.5 per cent on two seeds)
    because account ignitions are a steady flow. Over 52 weeks the nearest textbook route is the Bass curve with the
    whole base as its potential (-14.6 to -15.5 per cent), the recent pace +20.5 to +26.4 and the pooled hazard -31 to
    -33, while the golden family splits: the account-share hazard by likelihood lands the truth, the count form is
    rejected by about 5,000 log-likelihood units, but a two-stage account construction (ignition by size band, the
    completion curve by weeks since ignition, held flat past the 39 observed weeks) files -51 to -53 per cent. Lever
    about 15 per cent against a family that forks on the extrapolation: dead.
  - **Measured: adoption on the session clock (a constant chance per session, heterogeneous session rates)** (30,000
    users, lognormal rates sd 1.2, 52-week window). The per-session golden lands within 1 per cent (plug-in and
    gamma-Poisson empirical Bayes agree), but the eligible-denominator card's own route (the hazard per active
    non-adopter week times each non-adopter's active-week share) files +10.5 to +13.1 per cent and the pooled hazard
    with a log-linear decay -7.5 to -15.6 (-0.1 at a tighter spread): the card is the golden to a tenth and a half,
    and the golden is one divide and one group-by. Dead.
  - **Measured: substitution inside the account (one adopter serves the team, teammates' hazard falling to a tenth
    after the first adoption)** (4,000 accounts, median 8, 52-week window). The recent pace and the pooled hazard miss
    by +31 to +60 per cent, but the pooled hazard's decay extrapolation lands in some seeds (-3.9, -5.4) and swings to
    +90 in others, and the decisive fact is on the surface (two in three accounts adopted with about 1.2 adopters each),
    so the golden is one group-by of ignitions per account-week by size band. Dead.
  - Paper: a staged rollout's last wave or a long-term holdout released in the window is the eligible-denominator card
    applied to a filed date, the first wave's early weeks the attaining subset.
  - Paper: a growing in-app prompt read by the Bass curve as imitation (marketing effort against contagion): bucketed
    prompts are the eligibility card, session-level prompts one divide per impression, and the recent pace lands once
    the prompt is at its full share.
  - Paper: a past device or plan purchase surge ageing into replacement in the window, and self-hosted instances
    synchronised by a security upgrade wave: task46's cohort crossing a step and task162's burst by abstraction.
  - Paper: adoption at each account's renewal, quarterly business review or payroll run: task177 v2's days to the next
    bill by abstraction.
  - Paper: a need pool (the users who can use the feature) pinned by a finer file: the class with zero adoption is the
    attaining subset, one group-by.
  - Paper: cross-market lead-lag spillover between staggered country launches: a handful of markets carry the
    spillover coefficient, and the latest launch is the attaining analogue.
  - Paper: a second generation substituting for the first (Norton-Bass): the first generation's base is a group-by.
  - Paper: influence from current rather than cumulative users after disadoption: the definition of current is a free
    window, and the recent pace lands once current users plateau.
  - Paper: hard-deleted churned accounts inflating the analogue curves: a retention policy read (semantics) or a
    reconciliation (Layer 1).
  - Paper: churn as a competing exit against Kaplan-Meier: the textbook competing-risks correction.
  - Paper: later adopters' lighter durable use for a usage-volume forecast: the cohort chain ladder carries each
    cohort's level, and future cohorts' level is an extrapolation that forks.
  - Paper: late-arriving telemetry from offline devices: the right-truncation reflex this number already spent.
  - Paper: two-sided adoption through a counterparty graph, and contagion through feature-made artifacts: task144's
    per-view rate through a graph by abstraction.
  - Paper: a waitlist throttling admissions: task168's capacity-censored demand.
  - Paper: beta testers' adoption transported to general availability: selection on observables is the logistic
    route, on unobservables unidentified.
  - Paper: interference in a user-randomised test of a collaborative feature, the full rollout at a team-treated share
    of one: the network-interference card, small fully treated teams the attaining subset, and task177 v2's exposure
    end by abstraction.
  - The cell finding: an adoption forecast from a user or account event log is landed by one of three reflexes
    whenever the process is stationary over the window (the recent pace on a short window, the eligible-denominator
    hazard or a depletion-aware curve on a long one), so a lever of 30 to 50 per cent needs the window to change the
    process; every predictable change this search found is a filed date (rollout, holdout, sunset, price), a cohort or
    calendar alignment already on file (task46, task162, task177 v2), a cap or a pipeline in flight (task172, task77),
    or a network cascade (task144). Where the structure is new (local contagion, substitution in the team), the
    golden is either a group-by visible on the surface or an extrapolation past the observed weeks on which the
    golden family forks.

- **Second rebuild cell, 2026-10-23, chosen by this build: pharmacology-pharmacoepidemiology-safety /
  `population-pharmacokinetics-exposure-response`, Forecasting** (no card on file in the task type; the domain is
  outside the guard window of task178, task482 and task274). Why its window changes the process: a monoclonal
  antibody's move from 300 mg every three weeks to 600 mg every six puts each patient's trough twice as far from the
  dose, into the low concentrations where target-mediated elimination bends the decline and which the three-weekly
  record reaches only during treatment holds; no patient in the record has run the six-weekly schedule, so it cannot
  be replayed. The cell's four library cards (covariates inside the mixed model, allometric centring, exposure-response
  confounded by clearance, below-quantification samples as censored) and the field's textbook route (a population
  model fitted to the monitoring levels, each patient's own levels read by maximum a posteriori, the new schedule
  simulated) were taken as the default path. One candidate measured on code (scratchpad b179n/screen2: `pk1.py`,
  `pk1fit.py`; `pk_screen.out` byte-identical with `pk_screen_run2.out`) and eleven on paper; nothing holds.
  - **Measured: target-mediated (Michaelis-Menten) elimination against the linear one-compartment model** (600
    patients, clearance CV 35 per cent, troughs before half the infusions, a tenth of infusions with a peak, 5 to 15 per
    cent of patients with a hold of 5 to 12 weeks sampled one to three times; graded figure the share of patients whose
    six-weekly steady-state trough falls under 8 mg/L). With Km 2 mg/L the truth is 21.7 and 21.5 per cent on two
    seeds; carrying the linear clearance alone would file 11.5 and 12.3, but the textbook per-patient linear fit files
    21.2 and 21.0 (19.0 and 19.3 with the hold samples dropped), because each patient's own levels absorb the bend at
    that patient's concentrations. With Km 6 mg/L and holds in 5 per cent of patients the truth is 33.5 and the linear
    fit 28.8 (a lever of 14 per cent of the figure), and where the bend is strong enough for a 30 per cent lever the
    hold samples show it on a log plot. Dead: the field's own precision-dosing route reads each unit at its own level,
    and the only records of the forward region are the holds, an attaining subset.
  - Paper: two-compartment kinetics against one compartment for the longer interval: the standard structural choice for
    an antibody, tested by any population modeller, and three-weekly troughs already sit in the terminal phase.
  - Paper: each patient's half-life from the loading-phase accumulation (first trough over steady trough): an identity
    per patient, and the per-patient fit takes it anyway.
  - Paper: time-varying clearance falling with time on treatment: each patient's latest levels carry it.
  - Paper: anti-drug antibodies induced by lower troughs feeding faster clearance: the response is identified only by
    the patients already at low troughs (an attaining subset), with reverse causation as an open fork.
  - Paper: exposure-response confounded by clearance carried to the higher-exposure regimen: the cell's own card 3.
  - Paper, dose-response-pk-pd-modeling: the same per-patient absorption, and the cell's cards (relative ED50, AUC to
    infinity, hysteresis) are the textbook.
  - Paper, election-polling-forecasting (the other untouched Forecasting cell): a move from plurality to instant
    runoff (the upper house's ballot-level preferences are the obvious and only flow data), an election moved
    on-cycle (the national electorate in the voter file is the attaining subset), compulsory voting (the
    registered-voter sample is the cell's card 3), a party's withdrawal (districts it never contested are the
    attaining subset), a lowered voting age or a new party (unidentified).
  - Paper, banking deposit-liquidity-behaviour and credit-scoring-pd-modeling: a lower deposit-guarantee limit (the
    balances already above the old limit), branch closures (earlier closures), a payroll client leaving (customers
    who lost a salary credit), reject inference for a widened approval policy (rejects' bureau performance elsewhere),
    a payment holiday ending (pre-holiday performance), forbearance withdrawn (task169's removed route by
    abstraction).
  - The cell finding: in exposure modelling the field's own forecast already conditions on each patient's levels, so a
    forward schedule that stays near the record's concentrations is landed by the per-patient fit, and one that moves
    far from them is informed only by the minority of records already there (holds, delays), which a filter reads.

- **Third rebuild cell, 2026-10-23: education-learning-sciences / `learning-analytics-early-warning-models`,
  Forecasting** (assigned by the main session; worktree `b_179n`). The cell's four library cards and the earlier
  death in this task type (task176's credits by identity under a new course size, task143's driver) were read first;
  the textbook routes (a validated early-warning model on entrant attributes, the last intake's rate, analogue
  intakes) were taken as the default path. Architecture v3 (the co-enrolment exposure after the class allocation
  ended) was drawn from this cell; the directions below died on paper before it.
  - Paper: exam bunching under a compressed exam period: the compression is the forcing fact and names the covariate,
    and the record's same-day sittings are a filter on a timetable column.
  - Paper: a curriculum reform making final-year school mathematics optional: the reform names the covariate and the
    transcript file is single-purpose.
  - Paper: a hall of residence closing so more entrants commute: housing status is a column, a filter and a divide.
  - Paper: a shift in the instructor mix of gateway papers: the instructor is a field on the class, and shrunken
    instructor effects are the multilevel card.
  - Paper: a move of first-year sections online: a modality column.
  - Paper: dual-enrolment credit expanding in the forward intake: incoming credit is an admissions field the textbook
    model carries.
  - Paper: a grant that ends after the first year, read by a regression discontinuity at the renewal grade: the
    discontinuity gives a local effect and carrying it to every recipient forks.
  - Paper: an early-alert tutoring programme ending, so the record's outcomes are post-treatment: card 3's
    discontinuity at the old cut-off, local, a filed forward condition, and the transport to every flagged student
    forks.
  - Paper: completion anchored on deadlines under an extended deadline: task162's calendar-locked burst by
    abstraction, and modules with longer windows are the attaining subset.
  - Paper: mid-semester grades reported for every student after a new system (deficiency notices before): the
    feature's meaning changed, which is data semantics.
  - Paper: dropout timed on the legal leaving age, with a school-entry cut-off change moving the forward cohort's birth
    months: `time_semantics` (banned against task176 in the window) and task46's cohort crossing a step.
  - Paper: younger siblings of a cohort that left during a local crisis: the recent rate brackets the golden and the
    sibling link is a single-purpose join on the guardian.
  - Paper: school consolidation lengthening travel: the plan names the covariate, the record's distance bands are a
    filter, and the service-sequence selection is task175's template.
  - Paper: click counts across courses of different design (portability): within-course standardisation is the
    field's standard caution, and a forward course with no history is unidentified.
  - Measured and repaired, not dead: the co-enrolment mechanism's first generator world forked 7 per cent on
    functional form (`wfam.py`: bands 2,936, a linear term 2,819, log 2,725), because the forward intake's repeat
    classmates sat at 1 to 4 where the record had little support; the world now makes the fourth paper a
    university-wide elective and the protection near flat below five repeat classmates (`## Screens`).
  - Round 1 deaths of two ask devices (stage 4 on fab8b152): the co-taught pairs listing two teachers fell to both readers,
    who merged classes with identical meeting sets (room, day, start, weeks) and added; the transfer left as a second
    enrolled attempt fell to reader B's register join, and pinning its faculty (the judge's fork) would hand it to every
    reader. Replaced by the combination's figure repeated on ARC classes against own figures on SIRIUS pairs, read
    against the room (`## Ask sheet`).
  - Portal (2026-10-24) on the repeated combination figure read against the room: both responses kept all 20 cells,
    because the device's whole inconsistency sat in one file and a strong reader's capacity check finds it. Replaced
    by two devices under every cell, lecture-only pairs (three groups) and places held by students on leave or who
    left, seen only through the class list joined to the census history (`## Rubric repair`).
  - Judge pass 3 (2026-10-24) on the group unit left to section 4's "in one room at one time": counting every
    room-and-time meeting, or every class code, was as defensible as the distinct sets of classes. Closed by the
    prompt clause (SF11) rather than section 4, which the call reads.
  - Portal round 2 judge 2 (2026-10-24) on the class-enrolment change left unfiled: a count-free model read as
    defensible and the 2026 collapse as a possible migration artefact. Closed by the cutover notes' section 6 (who
    entered the class enrolments). Rejected for the closure: a candidate-predictor list in the conventions (the
    decisive step becomes rule application) and a stated held-out benchmark (no intake in the record enrolled
    itself, and a stated figure would be a certified record).
  - Judge r5 (2026-10-24) on the group unit left to the prompt's clause alone: two classes sharing one meeting
    were not filed as three groups, nor weeks as part of one time. Closed in GROUP_PIN in the write-up's words.
  - Portal round 3 (2026-10-25) on the count read as measured differently across the cutover: closed by section 6's
    comparability sentence (SF14). Rejected for the closure: naming the record's entrants who chose their own
    classes (confirmed after the July run, part-time) as a control, because it opens a process-indicator route that
    never builds the count (an indicator for choosing one's classes set for every 2026 entrant: 2,752.0 to 3,047.2 by
    run date, printing 2,750 or 3,000); the judge's comparability rule (it files the HOW and, read literally,
    excludes the count, 2,250); rewording section 6 to say the Registry allocated entrants (allocation is the
    decisive step's own word, D2).
  - Same round, in the write-up: an out-of-sample figure (the count-free model fitted on the entrants meeting 10 or
    more, 2,448.2 for the rest). Dropped: part-time entrants never meet 10 or more twice, so the part-time term is
    unidentified in that fit and the figure rests on a rank-deficient design.
- Portal round 4 (2026-10-25, zip c8032390): section 6 and its comparability sentence as the determinism closure.
  Both responses landed 3,250: the closure told a strong solver the classes changed hands and still mean the same,
  which is the step's premise. Withdrawn whole; the call side is the first ship's again.
- Same round, considered: keeping section 6's first paragraph alone (round 3's pack). Rejected: it held the call but
  failed the determinism block on its own reading (a measurement change, so the count dropped as not transportable).
- Same round, considered: a new rung under the classmate count to re-stump the landed version. Rejected: it redesigns
  the step that held six of six, against one withdrawn section.
- Portal round 5 (2026-10-25, 01124ef4): the write-up without the files' comparability evidence. Judge 1 read the 2026 collapse as a class-code artefact; the evidence (classes per entrant, class sizes, one paper a class) moved into step 4 as exact counts; nothing filed, the pack unchanged.
- **Architecture v3 (the Corriemoor entrants' repeat classmates), returned 2026-10-25 on version 391 for Duplicate:**
  the portal read it as a templated near duplicate of task175 (an unnamed neighbour count with the forecast
  population at its floor) after the call had held on four of six portal rounds; re-rooted on 2026-10-26 to
  architecture 4 under the coordinator's go, with a new driver, prompt and deliverable shell required.
- 2026-10-26, probe5 (alert-time leakage: week-6 ratings stored as revised at results for 2019 to 2025 and as at the week-8 extract for 2026, rebuilt from a migrated audit trail): landed two of two. Opus p179aa filed 6,000 (6,015.3) in about five minutes: it rebuilt every year's ratings from the audit trail as at Friday of week 8 with ARC's UTC turned to local time, saw 2026 at 18.7 per cent At risk and 32.6 Some concern against about 12 and 20, tied it to the bulletin's late timetable and one-day orientation, back-tested on 2025 (6,215 against 6,208) and threw out the stored-ratings model as "inflated by hindsight" (AUC 0.83). Opus p179ab filed 6,000 (6,027.3) by the same rebuild at 25 days after each record's first rating, on one clock. Lesson: a file whose only job is to reconstruct history (an audit trail next to a snapshot) gives the step away. The probe asks why the file is there and does the point-in-time rebuild by reflex. Point-in-time rebuilding is spent in every form that ships the history. Layer 1 tells the probe named, never to ship again: (a) the mid-semester raises to Some concern for students who kept attending gave the revised ratings an inverted retention (Some concern 0.91 against Satisfactory 0.88); (b) the hall occupancy distractor ran weekly to mid-December, past the 9 October extract.
- 2026-10-26, candidate B for architecture 5 (a professional body's students certify practical experience only under a registered training principal; a 2026 surge of principal exits at sole and small practices stalls the certification of those principals' students, visible only by linking each student's last certifying principal to the membership register). Measured on clean truth, not built: the surge put 7.7 to 11.7 per cent of active students under an exited principal (1.2 to 3.2 per cent in earlier years), but the twelve-month completion count moved only 34 to 73 on about 2,100 across three seeds, inside the textbook model's back-test error of 10 to 30. Only students due inside the window are delayed, and small practices replace a principal within months. Too small to carry a call at the nearest 100 without an unrealistic surge (scratchpad t179_a5/sim_b.py).
- 2026-10-26, the Education and Learning Sciences screen (closes the cell for this number): only the early-warning task type serves Forecasting in ELS, so every ELS setting is a fixed cohort's outcome, and the survivor anatomy needs a hidden flow into or out of the target. Corriemoor's actors are all recorded (programme, hall, hardship grant, offer date), banned (classmates, tutors, advisers, siblings), framed by a policy document (allowance, visa, fee and exclusion rules) or unseen in the university's own files (transfers to Halden or the polytech, employers). Variants worked and dropped: pre-census managed withdrawals skipped in 2026 (a data-quality join finds it), students moved off their admitted programme (the faculty rule points at it), full-time to part-time switchers (the 2026 part-time share is visibly up), students with no rating (a plain count finds them), moderated first-semester grades (a group effect and an unstated rule), hall retention when beds are spare (the spent capacity driver). Apprenticeships, K-12 and online courses fail the same way. The coordinator's go of 2026-10-26 moved task179 to another Forecasting cell.
- 2026-10-26, candidate C1 for architecture 5 (a motor book's accidental damage claims when the compulsory excess rises from 250 to 400: policyholders claim only when the bill net of the excess beats what the claim costs them in lost no-claims discount, so the rise moves every policyholder's own claiming point and the size-of-loss elimination misses half the cut). Measured on clean truth (scratchpad t179_a6/sim_xs.py, three seeds): observed 41,000, truth 36,800, the elimination route 39,100, the raw cross-section on voluntary excess 32,400, a large-claim-normalised cross-section 35,900 to 36,800. Dropped before the card: it is task270 v2's driver (claims absorbed under a no-claims scale, large claims as the unabsorbed count, protected policies as the self-selected reference), which a stage 4 reader landed, and task174's pricing-cell screen files the deductible change in that family.
- probe6 (Actuarial reserving, Sandhill Prairie Mutual CAT26-07 hail IBNR claims, contractor canvass halted by snow in 38 ZIP codes, golden 6,000, default 1,000): died at the first Opus call-only probe (p179ba, 2026-10-26), which landed 6,000 (5,938.8) by splitting the claims on the report channel (contractor, public adjuster and attorney as solicited), reading the solicited-to-self-reported ratio of 1.61 off every closed event and ZIP, and taking CAT23-09's March 2024 wave as the winter halt's evidence; the second probe was stopped. The actor had a column of its own (the report channel), so survivor property 1 failed, and the ratio was tidy enough to read straight off.
- probe7 (probe6's Sandhill world with the actor columnless: crews' claims reported by homeowners through the ordinary channels, the canvass visible only as each ZIP's own early burst and later wave, ratios by roof basis, golden 7,000, default 1,000): died at Opus probe 2 (p179cb, 2026-10-27), which landed 7,000 (6,970.6) by splitting every ZIP's claims into a first-notice burst and one later wave ("likely contractor canvassing", named unprompted), taking the wave's ratio by roof basis (RC 2.07, ACV 0.25), finding the 47 unreached ZIPs and reading CAT23-09's March and April wave as the spring resumption; probe 1 was stopped. The hail canvass is the domain's own knowledge, so removing its column left the reflex intact: readability test 3 fires on the decisive rung. The Sandhill world is spent for this number.
- probe8 (Sociology and Demography event history: Kinloch Logistics' Harrow Point DC 2027 leavers, express-bus riders leaving faster for a year after the route turns local, Route 9 Limited in 2023 as the calibration and Route 14 Express ending 31 December 2026, golden 350, default 250): died at Opus probe 1 (p179da, 2026-10-27), which landed 350 (353.5) by reading the route's end in the pass vendor's SKU catalogue, linking the riders through the payroll deduction's external reference, and taking Route 9 Limited's 2023 conversion as the precedent (2.82 times the tenure-expected rate, a difference-in-differences of 2.91); probe 2 was stopped. A filed event (the catalogue's end date) and a readable precedent in the same data are the banned "visible step at a filed event" and "precedent" drivers in another dress: the forcing structure must not also be the discovery path.
- 2026-10-27, probe9 draws set aside before any data was cut: (a) latent lightning damage to distribution transformers, read through a spatial join of strike records to the asset register, dropped on survivor property 5 (storm damage is on every asset engineer's checklist, and a strike file in the pack has only that job) and on task173's induced-failure driver in the same cell; (b) a bank's 2027 card defaults after one landlord group repriced its homes at 2026 renewals, read through the holders' rent debits on the checking side, BLOCKed at guard.py check on org family (financial_institution) and context artifact (monitoring_export) against task304, and its excess was under a tenth of the book's defaults.
- probe9 (Economics and Econometrics forecasting: Weldon & Pryor's 1 February 2027 delinquent roll, escrowed accounts missing their first owner-paid bill after a 2026 payoff surge from 2011's fifteen-year refinances, golden 1,200, default 1,000): died at Opus probe 1 (p179ea, 2026-10-27), which landed 1,200 (1,171.1): the prior payment channel (a servicer batch) was the strongest feature in its own collection model, so it asked what ends a servicer's payments, linked the clerk's lien releases to accounts by property ID and legal description, read a release with no new mortgage or sale nearby as a payoff (about 23 per cent delinquent against 1.3), and saw the 2026 surge across every lender; probe 2 was stopped. A mechanism that the textbook model's own strongest feature points at is found by asking what changes that feature; the clerk's index sitting in the pack invited the link.
- probe10 (Energy Systems and Utilities load forecasting: Corvell Hydro's 2027 residential rooftop solar applications, houses whose shading tree is felled applying at 6.7 in 100 against 1.6, a 2026 dead-ash felling surge in the field orders, golden 1,500, default 1,200): died at Opus probe 2 (p179fb, 2026-10-27), which landed 1,500 (1,458.6) by linking the field orders to premises through the new and legacy service point ids, reading a four to five times application rate 6 to 24 months after a felling ("consistent with removing shade"), and carrying the 2026 ash removals through it; probe 1 was stopped. The surge was the largest file's biggest 2026 spike and the join a standard premise key, so a reader that mines every order type against later applications finds it; the causal story (shade off, solar on) is intuitive once the spike is seen.
- 2026-10-28, architecture 5's draw, candidates set aside before the card (paper only, under the STOP block): (a) the
  release of a co-defendant raising a supervisee's arrest hazard, read through shared court case numbers, dropped as
  close to task170's peer note and to task179 v3's and task175's neighbour counts; (b) a private-equity roll-up
  redirecting business deposits, close to task447's change-of-owner redirect; (c) newspaper circulation and home sales,
  gift subscriptions, bundle roll-offs and cord-cutting, each a reflex or an invited join; (d) a bank's payroll switch,
  a probe8-like group shock with the direct-deposit feature pointing at the driver (property 6); (e) contagion through
  common owners, close to task446's ownership links. The victim-offender overlap was kept: no card, slot note or
  ledger row carries it, and it meets all nine properties on paper (`## Draw`).
- 2026-10-28, architecture 5's calibration (prototype `proto.py`, `proto2.py`): any new charge as the outcome moved the
  call by 4 per cent (2,110 against 2,200 at the nearest 100, one bin on its edge), so the outcome narrowed to the
  directive's Schedule B (violent felonies and firearm offences), where the raised hazard concentrates; a twelve-month
  raised hazard with the surge late in the year split the linked forms (the twelve-month flag under-reads victims
  recorded in the last months by about two fifths), so the hazard lasts about two years and starts about two months
  after the record, which keeps every linked form in one bin and keeps the surge out of the 2026 back-test (its
  recalibration ratio 0.90 to 1.04 on the seeds tried). A jail hold-bed decision was dropped as task141's furniture (a
  jail plan sized on supervision bookings); the GPS order replaces it.

## Earlier architectures (history)

Architecture v2's record, the first cell's record, the retirement and the 2026-10-23 rebuild, kept as
written; architecture v3's sections were replaced by this draw and live in the repository history.

### Architecture v2 record (spent, kept as history)

The v2 design as it stood when it was spent at stage 4 Gate F; every heading below is history.

#### v2 Draw

1. Card: `.claude/skills/fingerprint/cards/task179.json`, architecture v2, first registered 2026-10-21 and
   re-registered at the re-site. `guard.py check` WARN only: `repeat.gate_g` against task178 (answered in item 5);
   `test.same_puzzle_older` and `test.same_driver_older` against task133, task196 and task180 (G12) and earlier
   task126, task138 and task82 (G3), differentiated on the card (left truncation of loan exposure, capture-recapture
   of uncounted events, events masked by instrument noise; none reads a delay distribution from linked pairs).
   Nearest drivers 0.07 (task251 v4) and 0.06 (task192 v1).
2. Pairing: Epidemiology & Public Health (client domain) / `infectious-disease-transmission-modeling` /
   Forecasting & Predictive Modeling. The one build on file in this task type is task501 (a next-generation matrix
   built from contact diaries of the season's regime); nothing here touches a contact matrix or an eigenvalue.
3. Niche: Larrowmede Medical Relief, a medical humanitarian organisation running two treatment centres in the
   fictional Dunmarrow Province of the fictional Republic of Orvanthe, projecting the cases its centres must plan
   for in epidemiological weeks 49 to 52 (30 November to 27 December 2026) of an outbreak of Tamberlow virus disease
   (a fictional haemorrhagic fever first described in this outbreak) under the provincial response plan's central
   scenario, from the province's line list and the response's transmission links.
4. Call and shape: the number of new cases (confirmed and probable, by date of symptom onset) in weeks 49 to 52
   under the central scenario, to the nearest thousand (`quantity_figure`, `count`, question form how-many), with the
   reproduction number and the mean serial interval as components. Shape `single-figure`.
5. Mechanism keys: gap population (the transmission links are not the population of transmission intervals, they
   are the subset whose case has already fallen ill) then time; generators G12 (absence of a record against a record
   of absence: the long intervals are missing because their later event has not happened, not because they do not
   exist), G3 (the record's interval against the process's), G13 (each pair observed only inside its source's
   horizon to the extract). G13 led the first draft and G3 the second; task178 and task484 took them into the window
   in turn, and G12 reads the step as honestly. Gate G `forecasting` (a forecast the correctly read past does not
   pin); the WARN `repeat.gate_g` against task178 is answered by the honest key, since no validation or standard pins
   a method here. Strategy `maturity_censoring` (right truncation of a delay at the extract).
6. Layer 2: `estimation_fit` (censoring and truncation), pattern
   `epidemiology-public-health/infectious-disease-transmission-modeling/1` (Rt needs onset timing and the
   generation interval). The default path is that card's method; the stump is the judgment it takes for granted,
   that the serial interval read from the outbreak's own pairs is the interval the renewal equation needs.
7. Furniture: forum `operations_desk` (the organisation's emergency desk orders beds and staff on the planning
   lead's figure); forcing event `incident_or_complaint` (the outbreak, with the response plan's phase 3 starting 2
   November); organisation family `hospital_or_health_provider` (a non-governmental operator whose role here is
   running treatment centres); role family `capacity_planner`; context artifact `capacity_report` (the centres'
   weekly bed and roster file); calibration `none`.
8. Spine: the provincial line list as extracted on Sunday 18 October 2026 (one row per notified suspected,
   probable or confirmed case); the 25,000-row file is the contact registry (one row per listing of a person).
9. Deliverables: `tvd_projection_w49-w52.xlsx` (the projection, its components and the ask tables) and
   `tvd_projection_curve.svg` (observed and projected weekly cases with phase 3's start marked).
10. World, fictional throughout: the Republic of Orvanthe and its Dunmarrow Province (provincial capital
    Kettlebank), seven districts with cases (Tamberlow, Quillmarsh, Threlmarren, Wendlecombe, Brindlecourt, Kettlebank
    North, Kettlebank South), the Dunmarrow Provincial Health Directorate, the Kettlebank public health laboratory
    and the Tamberlow field laboratory, Larrowmede Medical Relief and its two centres, and Tamberlow virus disease
    with its own provincial case definition. No real administrative geography, agency, product or report voice is
    used; `metadata.json` states that the setting is fictional and the data synthetic. The epidemiology is kept
    real: a growing outbreak (doubling about every 18 days), onset to notification to laboratory to outcome links,
    contact tracing. Personas from `guard.py names --geo "Republic of Orvanthe" --seed 179`: Jacqueline Arnold
    (response epidemiologist, owner of the planning note), Tanner Molina (emergency coordinator), Kristin Sampson
    (treatment-centre medical lead).
11. As-of: the line list and the transmission links extracted Sunday 18 October 2026 at 23:59 (Orvanthe Standard
    Time, UTC+1); notification closes within four days of onset, so onsets to Sunday 11 October are complete; the
    laboratories' exports were pulled at 08:00 on Monday 19 October.
12. Sources read for the domain (stumping 1.3): the cell's two library cards (renewal-equation Rt with onset timing
    and the generation interval; the next-generation matrix's eigenvalue); task501 (a contact matrix pooled over two
    regimes); task232 (a transmission rate per exposure from closed episodes whose outcomes surface after a delay
    window; here the delay itself is the estimated quantity); task181's lineage (counts read before their records
    finish arriving; here the counts are complete and the intervals between linked records are what the cut-off
    bends); task133 (left truncation; here truncation is on the right and by the later event).
13. Data-native sentence: a source-to-case link is entered in the tracing system only when the infected contact
    falls ill and is notified, and the outbreak doubles about every 18 days, so at the extract most sources are
    recent and appear only with the cases they infected within the few weeks they have had, which bends the links'
    intervals short in exactly the cohort the renewal equation's growth window reads.

#### v2 Screens (stumping 1.2, as code)

Prototypes in the session scratchpad, b179e/screen (`a1.py` to `a4.py`, `e1.py`; seeds fixed before outcomes,
the outbreaks that died out before 2,500 cases skipped). The world screened is a discrete-day onset process,
offspring negative binomial (R 1.7, k 0.4), serial interval a discretised gamma (mean 12.6, sd 7.4 days), 62 per
cent of cases linked to a source, extract at day 165; eight outbreaks of 6,979 to 18,354 cases with 4,364 to
11,356 pairs. Figures are the projected cases in a four-week window starting five weeks after a 40 per cent cut,
each route against the golden (truncated maximum likelihood, gamma) on the same pack.

- The default family lands about a quarter low and tightly: every pair fitted (empirical or gamma) -27.2 per cent
  (sd 0.8), the same with the renewal-ratio R -27.0 (2.5), dropping pairs whose case fell ill in the last 21 or 42
  days (the hygiene reflex, on the case's clock) -27.9 and -26.9.
- The golden family converges where the data close it: truncated gamma 0.0, truncated Weibull +0.5 (0.1), the
  reverse-time nonparametric estimator 0.0, sources whose onset is 50 or 70 days before the cut-off (the
  complete-cohort subset, on the source's clock) +0.9 (3.0) and +0.3 (4.9). The lognormal reads +4.0 and the data
  reject it (negative log-likelihood 64 to 183 units worse than the gamma on every pack).
- The open residue is the current reproduction number's window and estimator: from the growth rate over 42 days
  it is the golden, over 28 days -0.1 with sd 7.4, the renewal ratio over the same 42 days +0.6 with sd 3.0. That
  is a knob, not the stump, so the window is filed (the six weeks to 11 October, weeks 36 to 41) and the spread of
  the two estimators on that window is measured on the cut pack before the rounding is set.
- Dispersion: the decisive quantity is a delay distribution's location; the parametric forms the data do not
  reject agree within 0.5 per cent and the nonparametric estimator within 0.1.
- Variance-only: the step moves the point (a quarter of the figure), it does not widen an interval.
- Common-exposure subset: the subset already complete, sources old enough that every case they caused has fallen
  ill, lands within its own sampling noise; choosing it means filtering on the source's onset, which is the
  decisive step itself. On the case's clock (the reflex) it lands the default.
- Truncation direction: the cut-off hides the top of the interval distribution (the long intervals), which is the
  case the screen keeps alive.
- Literature reflex: none applies in the re-sited world, since the virus is described only in this outbreak and the
  planning note says no parameter comes from elsewhere; in the screened world an outside interval (15.3 days, sd 9.3)
  landed +30 per cent, outside the golden's bin either way.
- `guard.py slots --driver`: vocabulary hits only (task194, task190, task253, task117, task501); no slot records
  a truncated delay distribution or a serial interval dying.

#### v2 Default path

1. Daily onsets of confirmed and probable cases from the line list (people found not to be cases and suspected cases
   left out, a case notified twice under two numbers kept once by its sample), complete to 11 October.
2. The serial interval from every source-to-case pair in the transmission links: onset of case less onset of source,
   2,449 pairs, a gamma fitted or the pairs' own distribution (mean 11 days).
3. The reproduction number implied by the exponential growth rate of daily onsets over weeks 36 to 41 (0.038 a day)
   through that interval (1.5).
4. The renewal equation forward from 12 October, the reproduction number halved for every source with onset from
   2 November, cases summed over weeks 49 to 52 (3,564).

Ends on: 4,000 cases
Golden: 5,000 cases

#### v2 Stump sentence

A competent analyst fits the serial interval to every source-to-case pair in the transmission links (11 days), takes
the reproduction number implied by the growth of onsets over weeks 36 to 41 (1.5), halves it from 2 November and
projects about 4,000 cases for weeks 49 to 52 instead of about 5,000, because the tracing system holds a link only
once its case has fallen ill, so September's and October's sources appear only with the cases they infected quickly;
read against the time each source had to 11 October, the links give the 13-day interval the chains run on, a
reproduction number of 1.6 and a December that holds a quarter higher.

#### v2 Three rules

Task type: infectious-disease-transmission-modeling (Epidemiology & Public Health): the outbreak's line list and transmission links turned into a serial interval, a reproduction number and a renewal-equation projection of cases under the response plan's central scenario, a projection serving Forecasting & Predictive Modeling.

Domain test: the deciding quantity is the serial interval distribution the renewal equation runs on, estimated from the outbreak's own transmission pairs the way a transmission modeller estimates a delay during a growing epidemic: each pair read against the longest interval its source could show at the cut-off (right truncation), then the reproduction number from the growth rate through that interval (Wallinga and Lipsitch) and the renewal equation forward under the scenario's halving.

Swap: "how many referrals a sales network brings in December, from referrer-to-referee links" keeps a link between two dated events and loses the step's ground: no renewal equation turning a growth rate into a reproduction number through the generation interval, no scenario that halves transmission by the source's onset, no epidemic whose growth makes the recent sources the numerous ones.

Layer 1: a case notified a second time from a neighbouring district under a new number with the same laboratory sample, people found not to be cases and suspected cases awaiting a result in the line list, rows fed from the field laboratory's forms carrying ISO dates beside day-first ones, links graded by certainty and links whose case was later discarded; each is how a surveillance line list and a tracing system write, nothing is placed to be caught, and checks.py asserts the call holds under each (SF1, SF6, L1, L2).

Layer 2: estimation_fit, the data's real structure: the serial interval is read from pairs that exist only once the later case has fallen ill, so the sample is right truncated at the extract, and during growth the truncation falls on the recent sources that are most of the pairs.

Decisive step: estimating the serial interval with each pair conditioned on its interval being no longer than 11 October less its source's onset (or any estimator that reads the pairs against their sources' horizon), which moves the mean from 11 to 13 days, the reproduction number from 1.5 to 1.6 and weeks 49 to 52 from 3,564 to 5,049 cases.

Not semantics: every field, code and definition read correctly (the classifications, the duplicate case numbers, the two date formats, the links' source and target, the dictionary's note that a link is entered when the target case is notified) still leaves the easy route fitting the pairs as they stand, because no field says the pairs are a truncated sample of the outbreak's intervals; the step is the inference that a growing outbreak cut off at an extract holds only the quick intervals of its recent sources, which the data show (the mean interval of the pairs falls from 13.5 days for sources ill in August to 11.0 for September's and 5.2 for October's) and no sentence says.

Not rule application: the planning note files the population, outcome, window, unit, scenario and the reproduction number's basis, and no rule says how the serial interval is read from the links; executing every filed rule with the pairs fitted as they stand files 4,000 cases.

Analyst test: a strong analyst who cleans the line list and reads every rule, fitting the serial interval to every pair in the links, files 4,000 cases (the default path's Ends on); one who drops the pairs whose case fell ill in the last fortnight (the hygiene reflex, on the case's clock) files 4,000 too; only reading each pair against its source's time to 11 October files 5,000; checks.py runs the three on the generator's clean truth (R3a, R3b, R3c).

Estimand: the planning note (planning_note_phase3_2026-10-19.pdf, sections 1 to 3): the population (new cases of Tamberlow virus disease, confirmed and probable under the provincial case definition, in the seven districts with cases), the outcome and unit (cases by date of symptom onset), the window (ISO weeks 49 to 52, 30 November to 27 December 2026), the scenario (every case with onset on or after 2 November causes half as many new cases as cases did over weeks 36 to 41, whose reproduction number is the one implied by the exponential growth rate of their daily onsets), the records (the line list and the transmission links as extracted on 18 October, onsets complete to 11 October, no outside parameter).

No decoy: nothing is planted: the line list, links, contact registry, laboratory exports, capacity report and situation report are the producing systems' records, the planning note states the scenario without a method, and no serial interval, reproduction number, projection or published parameter ships anywhere in the pack.

No certified replay: no certified or published serial interval, reproduction number or projection ships; the planning note says the virus is described only in this outbreak, so the method is not recovered by reproducing any figure.

Lesson: a delay read from linked records that exist only once the later event has happened is truncated at the extract, and while the process grows that truncation sits on the recent sources, which are most of the record; no build on file estimates a delay distribution from linked pairs read against each pair's own horizon.

#### v2 Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| Layer 1: the duplicate case numbers, non-cases and suspects, two date formats | the dictionary and the line list | readable |
| R0 growth of onsets over weeks 36 to 41 | the planning note, section 2 | readable |
| R1 (default path) the serial interval from every pair as it stands | the transmission links and the dictionary | readable |
| R1b the pairs whose case fell ill in the last fortnight dropped | the hygiene reflex on the links' dates | readable |
| R2 (decisive) each pair read against its source's time to 11 October | nothing: no sentence names truncation, the interval's bias, a cohort of complete sources or an estimator; the dictionary says when a link is entered and nothing about what that does to the intervals | silent |

#### v2 Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a case | Confirmed and Probable, a person notified twice under two numbers counted once by sample | both numbers kept; Not a case kept | same call (5,206; 4,898) | planning note section 3; checks.py SF1 |
| SF2 | completeness | onsets to 11 October complete, pairs whose case fell ill by 11 October | pairs and onsets to the 18 October extract | same call (4,739) | planning note section 3; SF2 |
| SF3 | the growth rate | log-linear least squares on daily onsets, 31 August to 11 October | Poisson regression on daily onsets; weekly counts | same call (5,005; 5,004) | SF3 |
| SF4 | the reproduction number's basis | the one implied by the exponential growth rate through the serial interval | the renewal ratio over the same six weeks (5,508) | not the filed estimand | planning note section 2, "implied by the exponential growth rate of their daily onsets" |
| SF5 | the halving | every source with onset on or after 2 November transmits at half | cases whose own onset falls on or after 2 November halved (2,525) | not the filed scenario | planning note section 2, "every case with symptom onset on or after 2 November causes half as many new cases" |
| SF6 | the links' certainty | every link | Low certainty dropped | same call (4,992) | SF6 |
| SF7 | the interval's family | discretised gamma | Weibull; the reverse-time nonparametric estimator; lognormal | same call (5,062; 5,047; 5,406, the lognormal 36 log-likelihood units worse) | SF7 |
| SF8 | the window | ISO weeks 49 to 52 by onset, 30 November to 27 December | none | filed | planning note section 1 |
| SF9 | rounding | the unrounded projection to the nearest thousand | none | prompt | prompt.txt |
| SF10 | the projection's start | the renewal equation from 12 October on onsets to 11 October | the onsets of 12 to 18 October read as complete (4,241) | not the filed record | planning note section 3, "onsets to Sunday 11 October are complete in the extract"; SF10 |

#### v2 Ladder

Built values from the cut pack (generator/checks.py R1 to R3c, SF1 to SF10), cases in weeks 49 to 52.

| Rung | Route | Serial interval (days) | R | Cases | Call |
|---|---|---|---|---|---|
| R1 (default path) | every pair as it stands, gamma or empirical | 11.13 | 1.484 | 3,564 | 4,000 |
| R1b | pairs whose case fell ill in the last 14 days dropped | 11.09 | 1.483 | 3,549 | 4,000 |
| Golden | truncated gamma, each pair conditioned on its source's time to 11 October | 13.16 | 1.586 | 5,049 | 5,000 |
| Golden family | truncated Weibull; reverse-time nonparametric; sources 50 or 60 days old only | 13.04; 13.14; 13.15; 12.83 | 1.585; 1.586; 1.589; 1.573 | 5,062; 5,047; 5,092; 4,857 | 5,000 |

- Dominance: every member of the golden family sits in [4,500, 5,500), the nearest 7.4 per cent from an edge (the
  complete-cohort subset at 60 days, 4,857), the golden 8.9 per cent; a bootstrap of the pairs (60 draws) puts the
  golden's sd at 3.0 per cent and every draw in the bin (B1); the default family sits in [3,500, 4,500).
- The data separates the readings: the mean interval of the pairs by the month their source fell ill falls from 13.5
  days (August, 519 pairs) to 11.0 (September, 1,486) and 5.2 (October, 215), which an interval that does not change
  cannot do unless the record is cut off; read against each source's horizon, the truncated fit's interval holds
  (sources 50 days old or more, whose cases have all fallen ill, give 13.15 days).

#### v2 Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | new cases, confirmed and probable, in the seven districts with cases | filed (planning note 1, 3) |
| 2 | Unit of account | a case by date of symptom onset | filed (planning note 1) |
| 3 | Attribution window | ISO weeks 49 to 52, 30 November to 27 December 2026 | filed (SF8) |
| 4 | As-of dating | the extract of 18 October 23:59, onsets complete to 11 October | planning note 3; manifest (SF2) |
| 5 | Version basis | one line list and one links export, no earlier release | the manifest |
| 6 | Denominator | none (a count) | commutes |
| 7 | Weighting | each pair once, each day's onsets as counted | SF3, SF7 |
| 8 | Window length | the growth window weeks 36 to 41 | filed (planning note 2) |
| 9 | Boundary inclusivity | onset on or after 2 November halved; 30 November and 27 December inside | filed (SF5, SF8) |
| 10 | Rounding path | the unrounded projection to the nearest thousand | prompt (SF9) |
| 11 | Tie-break | none | the golden family 3.0 per cent or more inside its bin |
| 12 | Maturity and censoring | the pairs right truncated at 11 October; onsets complete to 11 October | the decisive step; SF2 |
| 13 | Order of operations | clean, pair, fit, grow, project from complete onsets, sum | SF10 |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | a case notified twice counted once by its sample | SF1 |
| 16 | Identity normalisation | case numbers across the line list and the links, duplicates mapped to the first | SF1 |
| 17 | Netting against gross | not a case and suspected rows out | filed (planning note 3, SF1) |
| 18 | Dimensional units | days, cases | the dictionary |
| 19 | Code and status semantics | classifications, certainty grades | the dictionary (SF6); never the stump |
| 20 | Integerisation | none before the rounding | commutes |
| 21 | Clause scope | the halving applies to every source in every district from 2 November | filed (SF5) |
| 22 | Forward window contents | cases not yet ill, the scenario's halving the only change | filed (planning note 2) |

#### v2 Literal reader

The planning note executed word for word asks for the cases with onset in weeks 49 to 52 under a scenario whose base
is the reproduction number the growth of weeks 36 to 41 implies through the outbreak's serial interval; the literal
question is the interval the chains run on, which the links show only in part, since a link exists once its case has
fallen ill. A literal reader who fits the links as they stand has assumed the extract holds every interval its
sources will produce, which the falling mean interval by source month contradicts; every other reading converges or
violates a quoted sentence (fork table). Re-run on the finished pack.

#### v2 Oracles

- No shipped file carries a serial interval, a reproduction number, a projection or a published parameter for the
  virus; the planning note says none comes from elsewhere.
- The Kettlebank public health laboratory's results, the centres' admissions and the safe burials log are
  distractors (metadata.json); none ranks a projection.
- The situation report counts cases by week of notification as notified at 13 October; it projects nothing.
- No control ties only under the golden on the asks.

#### v2 Ask sheet

- **Ask A, contacts first listed in weeks 37 to 39 in Tamberlow, Quillmarsh, Kettlebank North and Brindlecourt:
  different people and the percentage who completed follow-up (eight figures, whole numbers and one decimal).**
  Home: the planning note's section 4 (the follow-up the scenario leans on). Path: the contact registry. Primary
  device: the same records under two key schemes: in the four districts the directorate's paper listings are
  entered at the district office beside the organisation's tablet listings of the same contacts, and the paper form
  carries an estimated age one to three years off the tablet's, so the exact person key counts those people twice;
  only source case, household, initials and sex, listed within a day, tie them. Hazards: a person exposed to two
  cases is listed once for each; completion is the person's last listing, not each listing's.
- **Ask B, the Tamberlow field laboratory's diagnostic samples by ISO week of collection, weeks 38 to 41: average
  hours from collection to final result and the percentage resulted within 24 hours (eight figures, one decimal).**
  Home: the planning note's section 4 (the laboratory turnaround). Path: the field laboratory's workbook. Primary
  device: a clock basis: the analyser writes its result time on UTC while collection and reception are keyed on
  local time (UTC+1); the evidence is in the data, results less than the 92-minute cartridge run after reception and
  positives a day before the line list's lab_result_date. Hazards: the final result is the re-run after
  Indeterminate; discharge-control samples are out.
- **The construction layer:** the call, its two components and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the line list and the links only; the registry and the
  laboratory workbook are read by the asks only (X1).
- **Hazard table (asserted):** A1 to A3, B1 to B3 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, people and completion by district | the exact person key, the last listing's status; keeps 0 of 8 | miss |
| B, turnaround by week | the final result on the clock the file shows; keeps 0 of 8 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 16).
- Pair ceiling: 28.5 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the call and keeps no ask figure, 12.0). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

### First-cell record

**First cell (2026-10-18).** New, Forecasting, seed FC50. The world was
moved honestly off `local_government`: a private ambulance company holds a city's 911 ambulance contract (the city
stays as the contract's counterparty) and decides its own summer surge pool, ten medic units for the weekend
20:00 to 24:00 block from June to August, any it does not need offered to the county's mutual-aid roster for the
summer; the contract's deployment standard staffs so that on nine weekend evenings in ten the units can answer every
call in the block at 1.2 unit-hours a call, and from June dispatch sends any unit in a district to any call in it,
North (planning areas 1 and 2), Central (3 and 4) and South (5). The world, the decision and the quantity were kept.
The seed's own mechanisms (a filed staffing formula executed literally, the public dataset's suppression of one-
and two-call cells, a sentence telling the solver to pool the areas) were never candidates. Two decisive steps were
screened on code, each one of the brief's ideas in its strongest form, over three seeds each plus sweeps, and
neither held. No architecture is live. This note holds the screen record only; it carries none of the `precut.py`
sections, because no design exists. The prototypes stay in the session scratchpad (b179/screen:
`c1_pool.py`, `c1_summary.py`, `c1_station.py`, `c1_total.py`, `c2_level.py`, `c2_sigma.py` and `screen179.py`,
whose output `screen179.out` is byte-identical with `screen179_run2.out` over two runs).

**The structural sentence, and the first thing to read.** The quantity cannot carry a graded whole-unit call under
the bar, whatever the decisive step. A district's units at the 9-in-10 standard are the ceiling of 0.3 times the
90th percentile of its block calls over one summer's 39 or 40 Friday, Saturday and Sunday evenings, and the record that
estimates that percentile is at most nine or ten summers of those evenings: the golden's own bootstrap sigma is
0.40 to 0.91 units in every realistic world measured (1.51 at twice the size), against the 0.25 units a whole-unit
bin leaves once its quarter-bin margin is taken, and on one pack the defensible estimators of that percentile
spread 0.44 to 1.19 units; only small Poisson-dominated districts reach 0.24 and 0.22, where every lever on file
(pooling, co-movement, a trend, a break, a one-off) moves the call by at most one unit and the cheap routes land.
The total of the three districts is worse: its sigma is 1.09 to 1.19 units at the base world (`c1_total.py`).
And the one forward change this world really carries, district dispatch, is the estimand's unit: once the standard
names the district's block as what its units must answer, the district's own evening totals in the record,
filtered, summed and quantiled with a trend, are the golden family, which is the first thing a strong analyst
builds. A draw on this quantity needs a graded figure resting on many more events than one evening's percentile (a
season's unit-hours, say, which changes the seed's quantity), or another world.

**The registration finding.** Nothing was registered and no axis of the window was spent. The window moved during
the screen: at fa74407 it was task201, task247 and task165; at 2689b12 it is task165 (`council_or_assembly`,
`purchase_order_or_contract`, `local_government`, `operations_director`, `register`, `single-figure`,
`composition_mix`), task268 (`board_of_directors`, `launch_or_rollout`, `retailer_or_ecommerce`,
`operations_director`, `operations_log`, `14`, `composition_mix`) and task248 (`line_manager_or_team`,
`cutover_or_migration`, `government_agency`, `capacity_planner`, `monitoring_export`, `03`, `other`). The keys this
world offers honestly outside it, had a design held: organisation `hospital_or_health_provider` (a licensed
ambulance service), forum `customer_or_counterparty` (the city's EMS contract office receives the summer deployment
plan), forcing event `other` (the county's mutual-aid roster closing in May), context artifact `filed_standard`
(the contract's deployment standard), calibration `prior_period_close_out` (the summers' close-outs), shape `05`
(ten units across three districts, the rest released). The honest role is `capacity_planner` (the contractor's
deployment planner), which task248 now holds, and the honest strategies are `grain_or_unit` for candidate 1's
pooling reading and `forecast_method_backtest` for candidate 2, both free.

**The taxonomy finding.** The honest home is Healthcare Delivery & Health Economics,
`utilization-access-demand-forecasting` (ambulance demand forecasting; the client library's pattern 4 there, plan
capacity to an overdispersed quantile against a mean plus a Poisson margin, is this quantity exactly), or
`patient-flow-beds-workforce-optimization` (staffing to the standard). The urban-regional municipal-service cell is
held by task165's subdomain in the window.

**The repeat screen.** `guard.py recent`, `coverage`, `mechanisms --objective forecasting` and `slots` ran before
any card, `slots` on the pooled-percentile driver, the level driver and the terms pooling, percentile, surge,
ambulance, medic and dispatch: no slot or card spent a pooled-percentile or a surge-pool level mechanism. The binding
matches are by the abstraction test: candidate 1's co-movement reading is task143's driver (a joint tail of a few
members whose error is mostly a component they share, the members treated as independent misstating it, the shared
component carried into the joint quantity), and its percentile-of-a-total reading sits beside task142 (an upper
percentile of a period's total built from the units that generate it). The brief's near drivers were read in full
on their cards: task148 (Erlang A with reneging in a 911 queue), task159 (platform backlog behind full trains),
task160 (regional waves timed by their lag) and task162 (version uptake set by the monthly restart burst); neither
candidate touches them.

### Retired

Retired on 2026-10-21 under the author's rule for this round (a number that dies in its second new cell is
retired). Three worlds were worked. The first cell, the seed's own world (a private ambulance contractor's summer
surge pool), died at stage 1 on code: the golden's own sigma was wider than a whole-unit bin under every pooling and
level lever. The redraw cell in Economics & Econometrics (time-series macro-econometrics) died on code and paper
before any card: every structural judgment beyond the textbook routes was a driver on file or carried a golden whose
own error matched its lever. The second new cell, Epidemiology & Public Health
(infectious-disease-transmission-modeling), carried architecture v2: the serial interval read from transmission
links that exist only once the later case has fallen ill, right truncated at the extract while the outbreak grows.
Its first world, a named real disease in a named real province, was declined on the real-place records concern; it
was re-sited into a fictional setting (the Republic of Orvanthe, Dunmarrow Province, Tamberlow virus disease),
built to stage 3 green (44 checks, the independent verifier, two byte-identical builds, precut.py exit 0, pair
ceiling 28.5) and spent at Gate F when scored reader B landed the call and both components.

The lesson: a correction the field teaches as standard is the default path, not the stump. Right truncation of a
delay read from linked records is the textbook caution of outbreak analytics (nowcasting, serial and generation
interval estimation), so a strong reader applies it on the first pass; the screen that measured the uncorrected
fit as the competent route measured a route this field's analysts do not take. A delay-truncation stump needs a
setting where the truncation is not the field's own named hazard, or a judgment beyond the correction.

The card stays filed with `architecture_spent` set. The two ask devices held (the reader kept 0 of 16) and are kept
here as reusable records:

- **Device record, the paper register's handover join.** During a handover between two field teams, the outgoing
  team's paper listings were keyed at the district office beside the incoming team's tablet listings of the same
  people, the paper form carrying an estimated age one to three years off and the listing closed as lost when the
  visits stopped. The exact person key counts those people twice and drags completion down; only source case,
  household, initials and sex, listed within a day, with the age inside the paper form's estimate, tie them. The
  filed definition (the follow-up that ends last, completed by either team) keeps the completion share determinate.
  Measured: the exact key, the key without age, the listing id and per-listing completion each missed every
  district's count and percentage.
- **Device record, the UTC result clock inferred from an internal inconsistency.** A laboratory analyser writes its
  result time on UTC while collection and reception are keyed on local time (UTC+1); nothing labels the clock. The
  evidence sits in the data: about 2.6 per cent of results land less than the dictionary's 92-minute cartridge run
  after reception, and positives fall on the day before the line list's result date, both vanishing once an hour is
  added. Measured: the clock read as local missed every week's mean and within-24-hour share; the re-run after an
  indeterminate result is the hazard beside it.

### Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired, for a from-scratch rebuild in product-analytics /
feature-adoption-diffusion-modeling (Forecasting), worktree `b_179n`. No candidate held at stage 1: three measured dead on
code (local contagion, the session clock, substitution inside the account) and sixteen directions dead on paper, all in
`## Tried and rejected` with the cell finding. No card registered, so architecture v2 stays the card's current identity
and nothing moved into `lineage`; nothing cut. PAUSED at stage 1 for the coordinator to assign another cell.

The coordinator then left the next cell to this build's choice: pharmacology-pharmacoepidemiology-safety /
population-pharmacokinetics-exposure-response (Forecasting). One candidate measured dead on code (target-mediated
elimination under a six-weekly schedule) and eleven directions on paper, with the election-polling and banking cells
screened on paper beside it (`## Tried and rejected`). No card registered; PAUSED at stage 1 again.

The main session then assigned a third cell: education-learning-sciences / learning-analytics-early-warning-models
(Forecasting), worktree `b_179n`. Architecture v3 was drawn there (an intake's next-census non-enrolment read at each
entrant's repeat classmates after the Registry's class allocation ended) and built through stage 3; its card is
drafted with the old identity in `lineage` (v2, spent) and waits on the guard window (`## Draw` item 1). The v2 artifacts (generator, golden, write-up, pack) were
removed for the rebuild.
