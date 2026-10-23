# task176 design note: Allerton's 2027 family child care home closures

**Status: architecture 2, drawn 2026-10-23 in sociology-demography / event-history-life-course-analysis
(Forecasting), the sixth allocation of the rebuild.** The card is
`.claude/skills/fingerprint/cards/task176.json`. Every earlier world, cell and mechanism on this number is
spent; their record is `## Earlier draws (screen record)`, `## Tried and rejected`, `## Retired` and
`## Rebuild (2026-10-23)`. Prototypes for this draw: session scratchpad `b176e/proto` (`fcc1.py` to `fcc5.py`).

## Draw

- **Cell.** Client domain Sociology & Demography, task type `event-history-life-course-analysis` (serves
  Forecasting & Predictive Modeling). Objective Forecasting: the call is how many of the family child care
  homes licensed in Allerton on 31 December 2026 will close during 2027, a window not yet open, pinned by the
  licensing record of 2016 to 2026. The call faces forward.
- **World.** The State of Allerton (fictional; its counties, agencies, programmes, providers and records are
  invented; the field's method is real). The Department of Early Learning (DEL) licenses child care and runs the
  child care subsidy. Its Office of Child Care sets the size of the 2027 round of the Home Child Care Start-Up
  Grant from the homes expected to close during 2027. The 2023 round, paid from federal relief money, licensed
  about 1,250 new homes in one year, four times the usual intake.
- **Card.** `domain` sociology-demography, `subdomain` event-history-life-course-analysis, `objective`
  forecasting, `shape` single-figure, `decision_type` quantity_figure, `answer_unit` count, `gap` [time,
  population], `pattern` [none], `generators` [G14, G6, G13], `gate_g` method_or_model_selection,
  `calibration_form` none, `stump_strategy` time_semantics, `context_artifact` capacity_report, `role_family`
  capacity_planner, `forum` minister_or_cabinet, `forcing_event` statutory_or_regulatory_filing, `org_family`
  government_agency; `stump_class` analytical; `layer2_family` field_method; `layer2_pattern`
  own:linked-lives-clock-youngest-own-child-school-entry. People from `guard.py names --geo "United States"
  --seed 176`: Misty Hawkins, Leroy Parker (Paula Fields and Cory Villegas dropped on people.first WARNs).
- **Guard.** `guard.py check` WARN only after two axes were redrawn at the probe: `forum` executive_team blocked
  against task175, and the call goes to the Secretary of Early Learning, who sets the round (minister_or_cabinet);
  `forcing_event` budget_or_appropriation blocked against task170 and launch_or_rollout against task178 (which
  registered while this card waited for the lock), and what forces the figure is the department's statutory supply
  report to the General Assembly, due 1 February 2027, which carries the forecast the round is sized on
  (statutory_or_regulatory_filing). `gate_g` forecasting tripped test.same_driver against task169's lineage on
  (time, G14, forecasting); the honest mechanism is the choice of the hazard's clock, which the record separates by
  deviance, so method_or_model_selection, and the older same-puzzle and same-driver matches (task134 v2 round 1,
  task149, task446, task452) carry differentiation lines on the card. WARNs answered: strategy_risk (the analyst
  test below names the analytical route that still fails with every field and rule read), overuse of the
  organisation family and objective (a state agency is who forecasts licensed supply; Forecasting is this lane),
  repeat.decision (a count is what the round is sized on).
- **Strategy.** time_semantics in its legal form (stumping strategies F1): a clock process already in the data,
  estimated by the field's method from every home that went through it. A family child care home's closure
  follows its provider's family life course: most homes run by a parent of young children close in the summer
  before her youngest own child living in the home starts kindergarten. The record reads that clock through the
  annual capacity worksheet, which lists every child who counts toward a home's capacity with a birth date and a
  relationship, and the 2023 round's providers joined when their youngest were babies, so they reach that summer
  together in 2027, in their fourth year, where a tenure clock puts the record's lowest closure rate.
- **Shape and criteria.** The call is one count to the nearest 50 (1). Two ask tables on rows the call never reads:
  the money the subsidy paid the homes by region and quarter of the 2026 payment run (20), and subsidised child-days
  of care in family child care homes across Allerton in each half of 2026, a child counted once on a day (2). The
  workbook and its tables (2 to 3). About 29 criteria, every one a cell of the prompt's shape.
- **Data-native sentence.** In Allerton's licensing record a home's closure is written against the licence, but
  the clock that times it is in another file and another person's life: the capacity worksheet's own-child birth
  dates put most parent-run homes' closures in the summer before the youngest starts kindergarten, at whatever
  tenure that falls, and the 2023 grant round licensed its providers when their youngest were babies rather than
  toddlers, so their kindergarten summer falls together in 2027 at a tenure where the record's other homes close
  least.
- **Sources read, and how this differs.**
  - `layer2-rigor-patterns.md` sociology-demography event-history-life-course-analysis 1 (competing events as
    cumulative incidence), 2 (cause-specific against subdistribution hazards), 3 (repeated spells), 4 (late entry
    as left truncation): 4 is a lower rung here (homes licensed before 2016 enter the risk set at their 2016
    tenure, which the careful default does), 1 to 3 do not bite (a closure is the one ending, a home has one
    spell); the golden is none of them applied as stated.
  - task266 (this cell): competing endings read as cumulative incidence. Here nothing competes and nothing is
    censored wrongly; the hazard's clock is the judgment.
  - task265, task133: delayed entry and left truncation. Here delayed entry is handled on the default path.
  - task134 v2, task468: a hazard by time since entry after a surge. Here time since entry is the wrong clock.
  - task177 v2 (held): an effect measured across a cycle carried to a population at one end of it. Here no effect
    is carried; the forward cohort sits at one point of a clock the record already shows in full.
  - task162 (held): a calendar-locked restart burst. Here the school year fixes the month, but what is decisive is
    whose clock it is (a linked person's age), not the calendar.
- **Screens run as code** (prototypes `fcc1.py` to `fcc5.py`, six seeds each, the generator's checks repeat them
  on the cut pack):
  - Lever: the tenure life table files 0.613 to 0.647 of the golden (the golden 1.58 times it); every reflex on
    the obvious covariates stays at or below 0.71 (provider age, the grant cohort, a has-a-parent flag at
    licensing, a child-under-six flag, the number of own children, the youngest's age as a straight line, the
    latest year's rate, the three-year mean rate); the youngest's age in bands without the school year reaches
    0.87 to 0.91; the kindergarten year of any own child, not the youngest, 0.84 to 0.88 and is rejected by a
    deviance of 532 to 641 against the youngest.
  - Golden family (log, logit and additive monthly hazards, the summer or the whole kindergarten year, an
    annual share, fitting windows from 2014, 2016 and 2019, with and without a summer term): 0.946 to 1.025 of
    the log-hazard golden over six seeds; the seed-to-seed sigma of the golden about 2 per cent.
  - Simulated forward truth: 0.958 to 1.019 of the golden.
  - Partial-coverage, common-exposure and null-region screens: the unaffected home-months estimate only the
    non-kindergarten hazard, so no filter of them reaches the call; the homes already in a kindergarten summer are
    the golden's own construction and need the clock to be found. Dispersion and truncation direction do not
    apply (a level, nothing suppressed); variance-only passes (the step moves the point).

## Default path

The pipeline a strong analyst builds from the prompt, the rules and the files' grain, every filed rule applied.

1. Conform the licence extract: keep every home (small and large, rules 6.40.010), read the closure effective date
   as the end of the licence, and admit the homes licensed before 2016 into the risk set at their January 2016
   tenure (delayed entry, the cell's card 4).
2. Build home-months from January 2016 to December 2026 and estimate the monthly closure rate by year of tenure (a
   life table), with the provider's age (63 or more, 68 or more), the June to August lift, the county and the 2023
   grant round's flag from startup_grant_awards_2023.xlsx as the obvious covariates.
3. Apply the rates month by month through 2027 to the 3,081 homes licensed on 31 December 2026 and sum each home's
   chance of closing.

Ends on: 300 (323.1 unrounded; 252.3 with the grant round's own tenure rates, which file 250)

Golden: 450 (461.0)

## Stump sentence

A competent solver fits closure rates by years licensed on the 2016 to 2026 home-months, with provider age and the
summer months, and files 300 closures for 2027 (250 on the 2023 grant round's own rates so far); the step that lands
it there is reading closure on the home's tenure, when a parent-run home closes in the June to August before the
provider's youngest own child starts kindergarten, which 427 homes reach together in 2027, 336 of them from the 2023
round whose providers were licensed with babies, so the count is 450.

## Three rules

- Task type: event-history-life-course-analysis (Sociology & Demography), which serves Forecasting & Predictive
  Modeling: a forward count of a life-course transition (a provider leaving home-based child care) built from the
  transition's hazard over the record's home-months.
- Domain test: the deciding quantity is each home's monthly closure hazard read on its provider's family life course,
  the June to August before her youngest own child living in the home starts kindergarten, estimated as a
  discrete-time event-history model over 314,262 home-months with that time-varying clock taken from the capacity
  worksheets' birth dates; the field reads a transition on the clock of the linked life it depends on.
- Swap: "how many of the hair salons licensed on 31 December 2026 will close during 2027" keeps the tenure life table
  and loses the youngest child, the school year and the 2023 round's family stage, so the deciding clock vanishes and
  the task stops being the same; with clinics, shops or machines the same.
- Layer 1: the licensing system's 1 July 2019 replacement (former licence numbers on the worksheets with a crosswalk,
  two relationship code sets, birth dates as month/day/year before it and ISO after); the capacity worksheet repeating
  each child at every renewal and listing a newborn only from the next worksheet; grandchildren, foster children and
  other relatives on the same worksheet; homes licensed before 2016 present only from 2016 (delayed entry); blank
  birth years for some legacy providers; county names and codes in three forms across files; on the asks, notice and
  split-care lines, every child line repeating its remittance's amount, remittance numbers restarting in each county
  office's run, voided remittances paid again in the next run, December 2025 service in the January 2026 run, and
  centres and exempt carers in the same file. Each is the system's own;
  none is placed to be caught, and each mishandled leaves the call in its cell (checks.py R2).
- Layer 2: field_method, the event-history clock: which time scale the closure hazard runs on (a linked person's
  school entry rather than the unit's tenure) and the forecast built from each home's own position on it.
- Decisive step: reading the closure hazard on the provider's youngest own child's kindergarten summer, a
  time-varying covariate rebuilt from the worksheet children's birth dates and the school-year cutoff, instead of on
  the home's years licensed and the covariates the licence file carries.
- Not semantics: the default path reads every field and code correctly (worksheets mapped, both code sets read,
  delayed entry handled, small and large homes kept) and still files 300; no field, code, unit or definition says
  that closures follow a child's school entry, and the worksheet exists to count children toward capacity.
- Not rule application: no filed rule or procedure says how closures arise or which clock a hazard runs on (the
  school-age rule in the subsidy policy sets rates for subsidised children), so executing every stated rule files
  300. The family the estimand leaves open, enumerated (tenure tables; Poisson and logit hazards with provider age,
  summer, county and the grant flag; a child-under-six flag; the youngest's age as a line and in bands; any own
  child's summer; the youngest's summer in six windows and forms and three fitting windows) spreads 252.3 to 463.2,
  printed 250 to 450; the standing family (the 18 constructions the record's likelihood keeps, every one reading the
  youngest's summer) spreads 432.1 to 463.2, every one printed 450; the ruling out is the record's own likelihood
  (2 dlogL 1,528 for no clock, 795 for the age bands, 364 for any own child), never a filed clause.
- Analyst test: a strong analyst who joins the former and current licence numbers, keeps small and large homes,
  admits pre-2016 homes at their 2016 tenure and fits closure rates by years licensed with provider age, the summer
  months, county and the grant flag files 300 closures for 2027 (Ends on: 300), because a tenure clock spreads the
  2023 round's closures thin when they arrive together in the summer their youngest own children start kindergarten.
- Estimand: the prompt files it: population, the family child care homes licensed on 31 December 2026 (status ACTIVE
  in fcc_licence_extract_20261231.csv, small and large under rules 6.40.010, no home licensed later); outcome, the
  licence ending (closure effective date, rules 6.40.070); window, 1 January to 31 December 2027; unit, homes, a
  count to the nearest 50; no comparison.
- No decoy: nothing is planted to be caught; no memo, draft, forecast, briefing or stakeholder figure exists; the
  supply report states past homes, places, openings and closures correctly and forecasts nothing; no document argues
  a method or a figure.
- No certified replay: no certified or published figure is reproduced to recover the method; the supply report's
  counts to 30 September 2026 are past quantities every route reproduces from the extract, so they select nothing.
- Lesson: a closure hazard in a home-based occupation runs on the provider's family life course (linked lives), so a
  hazard read on the unit's own tenure averages over cohorts that joined at different family stages and misplaces a
  cohort that joined together at one; no build on file reads a hazard on a linked person's age.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 0: closure rates by years licensed | no | the extract's dates | yes, the field's life table | no | no | no | readable |
| Rung 1: provider age, summer, county, grant flag | no | licence and grant columns | yes, a hazard model on the visible covariates | no | no | no | readable |
| Rung 2: own children as covariates (under six, the youngest's age) | no | the worksheet's birth dates | partly, feature building | no | no | no | readable |
| Rung 3 (decisive): the youngest own child's kindergarten summer | no: no sentence ties closures to a child's school entry; the school-age rule is a subsidy rate rule | no: no column; rebuilt from birth dates, the cutoff and the youngest at each month | no: the field's reflex is tenure and covariates | no: no corpus scores clocks | no: no sweep builds a clock | no: a per-home time-varying flag, not a ratio of shipped figures | silent |

The reflex row is enumerated from the field's own vocabulary for the deciding quantity (closure of a provider: a
life table by tenure, a Cox or Poisson hazard on the licence's attributes, cohort rates by entry year, the latest
year's rate, a trend), not from the rungs beneath it; every one of them lands at 250 to 350.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | licensed on 31 December 2026 | status ACTIVE in the extract, closure date blank | open at any time in December | same call (ACTIVE equals blank closure date, asserted) | the extract's status as at 31 December 2026 (dictionary) |
| SF2 | close during 2027 | the licence's closure effective date in 1 January to 31 December 2027 | a closure recorded in 2027 | same call (the forecast is of licences ending in 2027) | rules 6.40.070: the licence ends on the closure effective date |
| SF3 | family child care homes | small and large homes | small homes only (would file 400) | 400 | rules 6.40.010: "Family child care homes are licensed in two types" |
| SF4 | kindergarten year of a child | the school year in the calendar year the child turns five on or before 1 September | turns five in the calendar year | same call (433.7, asserted) | CCAP payment policy, section 5 |
| SF5 | to the nearest 50 | 461.0 to 450 | 461.0 to 450 by any rounding rule | same call (14.0 homes from the half-cell boundary) | the golden is clear of 475 and 425 (asserted) |
| SF6 | a home | one licence (one provider, one residence) | one provider | same call (one licence per provider, asserted) | rules 6.40.010: a licence is issued to one provider for one residence |
| SF7 | own child living in the home | relationship C or OWN CHILD with lives_in_home Y | own child wherever the child lives | same call (every own child row is Y, asserted) | dictionary, worksheet relationship and lives_in_home |
| SF8 | provider age | from provider_birth_year; blank years carry no age term | blank read as a year | same call (59 blank years, all pre-2009 homes, no age terms changes 450) | dictionary: blank where the legacy system did not hold it |

## Ladder

The graded figure is one count to the nearest 50; the golden cell is 425 to 475. Every figure below is computed on the
cut pack by `generator/checks.py` (RIV, FAM) and recomputed by `generator/verify.py` on its own code.

| Rung | Construction | Figure | Printed | Dies to |
|---|---|---|---|---|
| 0 | closure rates by years licensed (the default path) | 323.1 | 300 | the kindergarten summers the record shows at every tenure, 401 closures in 905 such summers |
| 1a | rung 0 with provider age | 321.6 | 300 | the same |
| 1b | Poisson hazard on tenure, age and summer | 319.5 | 300 | the same |
| 1c | rates by tenure split by the 2023 grant round | 252.3 | 250 | the round's homes measured while their youngest were babies |
| 1d | the latest year's rate | 293.2 | 300 | the same, and no clock |
| 2a | a child-under-six flag | 341.6 | 350 | the flag is on for years before the summer that closes the home |
| 2b | the youngest's age as a straight line | 328.8 | 350 | the hazard is a spike in one summer, not a slope |
| 2c | the youngest's age in yearly bands | 419.9 | 400 | the record's likelihood: 2 dlogL 795 against the summer clock |
| 2d | any own child's kindergarten summer | 424.2 | 400 | the record's likelihood: 2 dlogL 364 (an older child's school entry closes nothing) |
| 3 (decisive) | the youngest own child's kindergarten summer | 461.0 | 450 | (golden) |

- Position and margins: every rung that reads no child's school year sits at 1.2 times or more below the cell's lower
  edge (the nearest, 341.6, at 1.24); the two rungs that read children without the youngest's school year sit one
  cell below, ruled out by the likelihood rather than by a margin, and a solver on either has taken the direction of
  the decisive step.
- Standing family, 18 constructions (log and logit hazards; additive excess; the annual share; no summer, no age,
  2020 and grandchild terms; tenure capped at five years; the whole kindergarten year and May to September windows,
  each in log and additive form; fitting from 2016, 2019 and 2021; own children wherever they live; the step with the
  age bands or any own child added): 432.1 to 463.2, every one printed 450, both edges clear by 7.1 and 11.8 homes.
- Noise: one sigma of the summer's closure share (44.3 per cent on 905 summers) moves the call by 7.1 homes, inside
  the golden's 14.0 homes to its upper edge and 36.0 to its lower; 401 closures carry the step.
- Lever: the decisive step moves the figure from 323.1 to 461.0, 30 per cent of the graded figure, against a standing
  family spread of 6.7 per cent of it.
- Worth: delete every wrong number (none ships) and the difficulty stands: no file computes a forecast, and the
  tenure route is wrong on the clean truth (checks.py R3a).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | homes licensed on 31 December 2026, small and large | prompt; extract status; rules 6.40.010 (SF1, SF3) |
| 2 | Unit of account | the home, one licence | rules 6.40.010 (SF6) |
| 3 | Attribution window | a closure falls in the month of its effective date | C1: the forecast is a calendar-year sum |
| 4 | As-of dating | status at the end of 31 December 2026 | dictionary (extract pulled 8 January 2027) |
| 5 | Version basis | the extract as pulled; worksheets as filed | C1: one vintage ships |
| 6 | Denominator | home-months at risk from 2016 | C1 across fitting windows (2016, 2019, 2021, asserted) |
| 7 | Weighting | each home-month once | C1: pooled and annual forms agree in the cell |
| 8 | Window length | the fitting window | C1 (three windows, asserted) |
| 9 | Boundary inclusivity | the closure month counted as at risk | C1: in the cell either way (asserted with the first month) |
| 10 | Rounding path | expected count once, to the nearest 50 | prompt; 14.0 homes from the edge |
| 11 | Tie-break | none needed | not arising |
| 12 | Maturity and censoring | homes open at the end of 2026 censored | C1: the hazard model treats them as at risk to December 2026 |
| 13 | Order of operations | map numbers, dedupe children, then flag | C1: the order does not change the youngest at a month |
| 14 | Row order | file order | C1: no figure depends on it |
| 15 | Duplicate resolution | a child repeated across worksheets is one child | C1: initials and birth date (asserted with the latest worksheet only, R2 L2) |
| 16 | Identity normalisation | former and current licence numbers | crosswalk; R2 L1 asserted |
| 17 | Netting against gross | none | not arising |
| 18 | Dimensional units | homes; months | in the data |
| 19 | Code and status semantics | relationship codes; lives_in_home | dictionary (SF7) |
| 20 | Integerisation | the count rounds once | prompt |
| 21 | Clause scope | the school-age rule applies to the kindergarten year | policy section 5 (SF4) |
| 22 | Forward window contents | the 2027 months of each home with its worksheet children | the worksheets carry every child's birth date (the driver for 2027 ships) |

## Literal reader

Executed word for word, the prompt's population (homes licensed on 31 December 2026), outcome (licence ending),
window (2027) and unit (homes) are filed and every reading of them gives the same 3,081 homes and the same window
(SF1 to SF8 asserted in `checks.py`); the method is left open and the record forces it, its likelihood rejecting every
clock but the youngest own child's kindergarten summer, and every standing construction prints 450. No shipped
sentence, read literally, fixes the tenure route or any other method.

## Oracles

- `child_care_supply_report_2026q3.pdf`: homes, places, openings and closures by region to 30 September 2026, and the
  2023 round's homes still licensed; past quantities that every route reproduces from the extract; ties under every
  basis; forecasts nothing.
- `startup_grant_awards_2023.xlsx`: awards, payments and recoveries; the grant flag rung 1c reads; no closure
  forecast.
- No control, corpus or published figure ties only under the golden or only on the wrong read.

## Ask sheet

**Main call's declared row population:** fcc_licence_extract_20261231.csv, licence_number_crosswalk_2019.csv and
capacity_worksheet_children_2016_2026.csv. Device and hazard rows in it: 0 (asserted, `checks.py` SEP: the call reads
those three files and no ask file; the ask file carries no row the call reads).

**Re-sited on 2026-10-23 before the pack went to readers.** The first ask layer carried a food program ask (a revised
claim against a second sponsor's part-month claim) and a visits ask (two module records at one arrival). The round's
stage 4 measurements had readers break both shapes (a re-filed schedule against a supplement; fills grouped by time,
trader and side), so both were cut and their files stay in the pack as distractors; their line is in `## Tried and
rejected`.

**Re-sited again after round 1 (zip 13d6ad18, 2026-10-23).** Both readers took one remittance per run date and
provider (20 of 20 money cells each) and the judge named a fork in "child-days" (each paid line against each child once
a day). The prompt now files the child-day by literal WHAT ("counting a child once on a day") and the child-days ask is
shrunk to the two statewide halves, priced as carrying no device; the money device moved onto the payee, so that the
readers' grouping is the wrong one. The line is in `## Tried and rejected`.

**Ask A. The child-days of care the subsidy paid family child care homes for in each half of 2026 across Allerton,
counting a child once on a day** (2 figures, whole numbers). H18 home: the subsidised care that rests on the homes the
call says will close.
- No device: the prompt's clause settles the one-child-two-lines reading (a child paid at the home left through its
  notice days while the new home's lines start, and a child in split care paid at two homes on the same days). Summing
  care_days instead gives 135,010 and 154,218 against 125,938 and 137,949; with the clause read a careful reader lands
  both figures, and the ask's surface is shrunk to two figures for that reason.
- Hazards: centre and exempt lines in the same file, voided remittances paid again in the next run, December 2025
  service in the January 2026 run.

**Ask B. For each region, the money the subsidy paid family child care homes in each quarter of 2026 by the date of
the payment run** (20 figures, nearest dollar). H18 home: the subsidy income the homes' closures take out of the
regions, the money the grant round is weighed against.
- B1 (silent primary, what one payment is): each payee receives one remittance in a run and every child line of it
  carries the remittance's amount; a home in a family child care network is paid through the network's remittance, so
  one remittance carries the children of two to five homes (496 of 12,387 home remittances, 207 homes), and the file
  names on each line the home that gave the care, not the payee. Each county office numbers its remittances in its
  own sequence every run (policy section 3; the dictionary), so one payment is a remittance number, a run date and a
  county office. The readers' grouping, one amount per run date and provider, counts a network's remittance once per
  member home: every cell high by 31,084 to 169,269. Every other key a careful de-duplicator reaches for misses every
  cell: number alone, number and run date, number and provider, number and amount, number and county office, provider
  and amount, run and county office with amount, number with run and amount, number with run and provider (by 58,951 to
  1,131,873 either way); summing every line is high by 146,698 to 849,004.
- Hazards: voided remittances (keeping them adds 1,583 to 18,063 a cell), the January 2027 run (December service)
  outside 2026, centres and exempt carers in the same file.
- Stops (asserted): lines summed and each of the eleven alternative keys (all 20); voids kept (all 20); voids kept on
  the readers' key (all 20).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| H1 notice and split-care lines | a child paid at two homes on the same days | A | closed by the prompt's clause (summed: +9,072 and +16,269) |
| H2 voided remittances paid again | a remittance returned unpaid, reissued in the next run | A, B | B +1,583 to +18,063 a cell |
| H3 the remittance amount on every line | a remittance export at child-line grain | B | every cell, +146,698 to +849,004 when summed |
| H4 network remittances | a home that joined a network is paid through the network's remittance | B | every cell, +31,084 to +169,269 on one per run and provider |
| H5 remittance numbers per county office and run | each office numbers its run in its own sequence | B | every cell under a key without the county office |
| H6 the January 2027 run | December service paid in the first January run | B | outside the 2026 quarters (the run date files it) |

**Referee.** For B, the remittance's one amount and status on every line of a number, run and county office
(asserted), the same number, run and office carrying lines of several homes in every region and quarter (asserted),
and the same number carrying other providers in other offices and runs. Countable from the shipped rows; the identity
is filed in policy section 3 and the dictionary, and the network is never named.

**Ceiling sheet** (`generator/ceiling.py` on the cut pack; every route scored figure by figure against the golden)

| Route | Child-days | Money | Kept of 22 | Landed | Off the call |
|---|---|---|---|---|---|
| reader A verbatim (each child and day once; one amount per run date and provider) | 2 | 0 | 2 | 50.0 | 17.0 |
| reader B verbatim (care_days summed; one amount per run date and provider) | 0 | 0 | 0 | 45.0 | 12.0 |
| reader B with the clause read | 2 | 0 | 2 | 50.0 | 17.0 |
| each of the twelve alternative money keys, child-days once a day | 2 | 0 | 2 | 50.0 | 17.0 |
| mirror (300, care_days summed, every line's amount) | 0 | 0 | 0 | 45.0 | 12.0 |

**Cracker sheet** (the device-bearing ask only; the cracker lands the call, keeps the home lines, drops voided
remittances, keeps the 2026 runs, and takes the repeated remittance amount once on its best key)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask B, money by region and quarter | 20 | one amount per run date and provider (both readers), or any of the eleven other keys | B1 | miss |

Ask A carries no device and is not a cracker row: the cracker lands both of its figures, and the ceiling sheet above
prices them as landed on every route.

Worst route: 2 of 22, 50.0 landed; pair with the best reader off the call 33.5. Both readers as filed (both off the
call at 300): 17.0 and 12.0. Money cracked (number, run date and county office): 22 of 22, 100.0 landed, pair 58.5; the
build stands on B1 holding.

Measured by: `generator/ceiling.py` (run on the cut pack; Part 0's weights, the call and its components 38, the
instructions 7, the asks 55 over the 22 ask figures; a response off the call keeps 5).

Mirror leakage: 0.0 per cent of ask weight (the mirror, off the call at 300, sums care_days and the amount on every
line and keeps none of the 22 figures).

Pair ceiling: 33.5 measured on the cut pack (the worst route landed 50.0, the best reader off the call 17.0); the
worst single crack 58.5 (B1).

**Call edge (round-1 judge, answered risk).** The full-record specifications sit at 442 to 461, inside the 450 bin;
the judge reached 423 (fit on the years before 2023, the kindergarten flag only) and 474 to 487 (windows from 2024
on, with a kindergarten-by-tenure interaction). No filed WHAT removes them without filing the method: the population
(homes licensed on 31 December 2026), the window (closures during 2027) and the unit (a home's licence) are filed, and
choosing the fit window or an interaction is the method, which stays open with the record's likelihood separating the
candidates. Recorded as an answered risk; the call does not move.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | R2 (checks.py) |
|---|---|---|---|---|
| L1 former licence numbers on worksheets before 1 July 2019 | licensing system replacement | worksheets and crosswalk | pre-2019 worksheets unmatched | call unchanged (437.5) |
| L2 a child repeated at every renewal; a newborn only from the next worksheet | capacity worksheet process | worksheets | the latest worksheet only | call unchanged (466.0) |
| L3 two relationship code sets and two date formats | licensing system replacement | worksheets | one set read | the same rows as L1 (call unchanged) |
| L4 homes licensed before 2016 present from 2016 | the extract's scope | licence extract | tenure started at 2016 | call unchanged (444.6) |
| L5 grandchildren, foster children, other relatives on the worksheet | rules 6.40.030 | worksheets | any child read as a provider's own | ruled out by SF7 and the likelihood (any own child) |
| L6 blank birth years for legacy providers | the legacy system | licence extract | blank read as a year | call unchanged (no age terms, 462.7) |
| L7 county names, codes and spellings across files | each system's own | lookup and ask files | a region unmapped | every county maps (asserted) |
| L8 notice and split-care lines, voided remittances, December 2025 service | CCAP payment system | ccap_payment_lines_2026.csv | lines summed | outside the call's files; Ask A hazards (the prompt's clause closes the reading) |
| L9 the remittance amount on every child line; network remittances carrying several homes; numbers in each county office's sequence per run | CCAP payment system | ccap_payment_lines_2026.csv | amounts summed, or deduped per run and provider or on a partial key | outside the call's files; Ask B device |
| L10 revised food program claims and sponsor changes; twin visit records | CACFP claims and licensing systems | distractor files | none (no figure reads them) | distractors |

## Leak sweep

`leak.py task176 --asof 2027-01-14`: REVIEW, no LEAK. Each REVIEW line, answered:
- The policy, the supply report, the dictionary and the rules carry six or seven of the call's words because they are
  the department's own vocabulary (family child care homes, licensed, Allerton, December); none states a count, a
  rate or a forecast.
- Stump-paragraph terms in the same four documents (children, capacity, provider, worksheet, closure, school) are the
  field's nouns: the rules say what the capacity worksheet lists and why (capacity counting), the policy says when a
  subsidised child is school-age (rates and hours), and neither ties a child's school entry to a home's closure.
- The quality ratings carry their expiry dates, which by nature fall after the as-of date; a distractor file.
- Single-use test: the capacity worksheet's in-world use is capacity counting, it holds grandchildren, foster children
  and other relatives as well as own children, and the decisive step reads one derived flag from it; the school-age
  sentence's use is the subsidy's hours and rates.

## Earlier draws (screen record)

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** Wave 8, new, Forecasting, seed FC47: a
broadband satellite operator with 360 satellites ready for 2027 and six rideshare launches (February, April,
June, August, October, December) of at most 60 each; satellites released at 210 km raise themselves to their
shell, and until they pass 350 km a geomagnetic storm's drag can bring them down; the mission assurance memo
lets a launch carry only as many satellites as keep its expected storm loss at two or fewer, the rest waiting
for 2028. The world, the decision and the quantity were kept; the seed's own mechanism (onsets against storm
days) was set aside as a unit reading to be filed as a WHAT. Two decisive steps were screened on code, the
brief's two ideas, and neither held on measurement. No architecture is live. This note holds the screen
record only; it carries none of the `precut.py` sections, because no design exists. The prototypes stay in
the session scratchpad (b176/proto).

**The structural sentence, and the first thing to read.** Every factor of a 2027 launch's expected storm
loss is either barely forecastable beyond climatology or barely moved by the solar cycle. The storm onset
rate for one phase of one cycle varies from cycle to cycle by a coefficient of variation of 0.40 at the 2027
phase, far more than the phase itself moves it, so the field's standard conditioning forms (phase with the
cycle's amplitude as sunspot number, as F10.7, or as the cycle's own storm level) spread wider than any cheap
route misses by, and none beats the all-years climatology out of sample by a visible margin. The time below
350 km, the factor the operator's own records measure precisely, is set by thrust and not by drag for any
satellite with the thrust margin to survive solar maximum, so the solar cycle moves it by 25 per cent from
F10.7 70 to 240 and by about 5 per cent between 2026 and 2027; it becomes steep only where the drag-to-thrust
ratio nears one at 210 km, which is where a batch is lost anyway. The loss per onset rests on the few dozen
batch-storm encounters an operator's history holds. A draw on this quantity needs a difference between 2027
and the record that is large, measured in full in the record, and estimated from many events; none was found
in this world.

**The taxonomy finding.** A storm-frequency step sits honestly in physical-environmental-sciences
`climate-weather-extremes` (F, never drawn), the frequency of an extreme in a coming window. The exposure step
is at that task type's edge (the thermosphere's solar-cycle climate, not an extreme). `hydrology-flood-frequency`
is a different field, and actuarial `claims-frequency-severity` (DD, F) fits only an insurer's world, which the
seed is not. The seed's Supply Chain line has no forecasting home for a hazard rate.

**The data finding.** GFZ's own file since 1932 (kp.gfz-potsdam.de, datapub.gfz-potsdam.de) and every NOAA,
NASA and SILSO host returned 403 at this session's proxy; PyPI and raw GitHub were reachable. The screen ran on
CelesTrak's `SW-All.txt` (updated 21 July 2025, bundled in the `spaceweather` 0.4.2 wheel on PyPI, CelesTrak's
note: no licensing requirement, cite the URL), which compiles GFZ's definitive Kp and Ap (CC BY 4.0, Matzka et
al. 2021, doi 10.5880/Kp.0001) and NRCan's F10.7 from 1 October 1957 to 20 July 2025 (24,765 days, 2,231 storm
onsets at Kp 5o or more with a 24-hour gap), plus the July 2025 monthly predicted F10.7 to 2041. So the record
holds cycles 19 to 24 in full and cycle 25 to 0.7 years after its October 2024 maximum, not the eight cycles
the seed names; the two missing cycles would narrow a mean's sampling error and close none of the family
spread below, which comes from how the cycle's strength is measured. SILSO's sunspot number (CC BY-NC 4.0) was
used only as a screen covariate. A pack set at a late-2026 as-of would need Kp from August 2025 onward by
another route, since a constructed Kp may not carry GFZ's or NOAA's name.

**Redraw in a new world, 2026-10-19 (actuarial-science-insurance / reserving-development-triangles,
Forecasting), screened at stage 1 and failed; no card registered, nothing cut.** The coordinator allocated the
cell; the client's reserving cards (`actuarial-science-insurance/loss-reserving-claims-development/1` to `/3`:
Berquist-Sherman on disposal rates, a fitted tail, a Mack or bootstrap range) and Bornhuetter-Ferguson against the
chain ladder are the careful reader's routes, so a stump had to be a judgment those take for granted that the data
settle. The structural sentence for the cell: every maturity shift (exposure attaching later in its period, reports
arriving sooner, settlement speeding up) moves the chain ladder by 15 to 170 per cent but moves
Bornhuetter-Ferguson materially only where the unpaid share is mid-range, and the disposal-rate card restates it
away whenever closed counts track the shift; the rest of the cell's triangle judgments are spent on file (case
adequacy, settlement speed, completion of immature periods, a cap that binds more often), banned this round (every
mix shift, `composition_mix`), need a filed future rate (calendar-year inflation, which is rule application or a
fork), or are a variance (ranges, tails). Prototypes are in the session scratchpad (r176/proto).

**Second redraw, 2026-10-19 (sociology-demography / population-estimation-demographic-projection, Forecasting),
screened at stage 1 and failed; no card registered, nothing cut.** The coordinator allocated the cell and lifted the
round's extra bans. The cell's cards (`sociology-demography/population-estimation-demographic-projection/1` to `/5`:
cohort-component ageing, gross migration flows, stated-coverage intervals, the control total, shrinking small-area
rates) are the careful demographer's routes. The structural sentence for the cell: the judgments those cards take
for granted that the records settle are each spent on file, closed by the guard's window, or a textbook route of
their own:
- who is at risk of a flow (duration since arrival, parity, a pool outside the area by age) is a hazard on a pool
  whose composition shifted (task134 v2, task468);
- a fixed stock's turnover is task132's renewal;
- a housing capacity is the housing-unit method;
- special populations are `population_selection` (task270's window) and census practice;
- a back-test of projection methods is `forecast_method_backtest` (task177's window);
- on population levels the structural levers run under 10 per cent, because flows are small against stocks.

Prototypes are in the session scratchpad (r176/demog).

## Tried and rejected

- **The solar cycle's phase, with or without the cycle's amplitude, as the decisive step** (the brief's first
  idea; prototypes `load.py`, `phase1.py` to `phase3.py`, `backtest1.py`, `season1.py`, and `screen_c1.py`,
  whose output `screen_c1.out` is byte-identical over two runs). Killed at stage 1 on measurement, on the real
  record: the right family spreads wider than the rivals miss by, and the data does not reject the rival out
  of sample.
  - The 2027 windows sit 2.3 to 3.2 years after the October 2024 maximum; the screen reads the half-year bins
    from 2.0 to 3.5 years after each earlier maximum. At Kp 5o or more with a 24-hour gap, in onsets a year:
    - all years 32.9, cycle 25's last 2.7 years 28.8, cycle 24's same phase 24.7;
    - the same phase of cycles 19 to 24 alone (phase-only) 42.4, by cycle 56.7, 30.7, 62.0, 54.0, 26.7 and 24.7;
    - a Poisson model on phase bins with log amplitude 34.3 (sunspot amplitude) and 40.6 (F10.7 amplitude),
      and cycle 25's own level times the earlier cycles' declining-to-maximum ratio 34.8 (mean ratio) and
      32.6 (median).
  - The amplitude-conditioned family runs 32.6 to 40.6 (25 per cent wide) and contains the all-years rate;
    phase-only sits 4 per cent above its top and the last 2.7 years 12 per cent below its floor. The Poisson
    model's dispersion is 2.51 per degree of freedom: the cycles differ by far more than counting noise.
  - The pattern holds at every threshold and gap tried. The family is 28.2 to 32.4 at a 48-hour gap
    (all years 27.3, phase-only 33.4) and 23.0 to 28.0 at 72 hours (all years 23.7, last 2.7 years 24.8). At
    Kp 6- it is 20.4 to 27.2 (all years 19.6, phase-only 28.7), at Kp 7- 5.2 to 11.2 (all years 7.3, phase-only
    11.3), at Kp 5- 43.8 to 50.3 (all years 41.6, phase-only 52.1), and at Kp 4o 55.8 to 61.4, where every route lands (all years 56.8, last 2.7 years 58.4).
    The lever and the spread grow together with the threshold: one dial.
  - The leave-forward back-test forecasts each of cycles 20 to 24 from the record before its window, in RMS log
    error over the five cycles: the sunspot-amplitude model 0.297, the F10.7-amplitude model 0.337, the last 2.7
    years carried 0.346, all years 0.363, level times shape 0.365 (four cycles), phase-only 0.512 and the previous
    cycle's same phase 0.528. Phase-only is worse than climatology, and the best form beats persistence by 0.05
    in log error with five cycles behind it, so no rival is rejected by a visible margin; a year-ahead forecast
    at this phase misses by about a third whatever the method.
  - The eda6c8c screens, as code: dispersion does not apply (a level), though the cross-cycle coefficient of
    variation at the phase is 0.40; variance-only passes (phase-only moves the point estimate to 1.29 times
    climatology); the common-exposure subset fires, since the same-phase years of past cycles, filtered and
    divided, are the phase-only route itself (42.4) and land above the family, while the family holds the
    all-years rate; truncation direction does not apply.
  - Determinism fails before strength. With six whole-satellite launch counts, or loading in 12-satellite
    trays, a bin holding a 25 per cent family spread plus one sigma (about 16 per cent, a six-cycle mean at CV
    0.40) leaves no room for the all-years route, which sits inside the family, or for the last two years,
    which sit 12 per cent from its floor.
  - Seasonality is not a separate stump. The record's equinoctial modulation of onsets (monthly factors 0.70
    in December to 1.24 in October at Kp 5o) is what a careful analyst gets by default when counting onsets in
    each window's calendar days across every year.
- **Exposure below 350 km set by the thermosphere's solar-cycle state as the decisive step** (the brief's
  second idea; prototypes `expo1.py`, `expo_run.py`, and `screen_c2.py`, whose output `screen_c2.out` is
  byte-identical over two runs). The revision log's overrun ("raising has run longer than planned") would be
  the solar maximum's thicker thermosphere, which the declining phase removes. Killed at stage 1 on lever:
  every cheap route lands inside the right family's own spread.
  - The truth, as built:
    - each batch climbs from 210 km under electric thrust (1.6e-4 m/s2, a 1.5 to 3 day checkout at 0.8 duty)
      against drag on an exponential thermosphere tuned to MSIS-like magnitudes, with density at 200 km of
      2.0e-10 kg/m3 times (F10.7/70)^0.72, a scale height of 33 + 0.055 (F10.7 - 70) km, an Ap term and a
      30 per cent semiannual oscillation;
    - real daily F10.7 and Ap drive it to 20 July 2025, then the July 2025 predicted F10.7 plus AR(1) and
      27-day noise;
    - 47 to 48 launches run from March 2020 to October 2026, each with a plan computed at a reference
      atmosphere (F10.7 150, Ap 12);
    - the 2027 windows run on the predicted F10.7 of 102 to 122; seeds 1, 2 and 3 were fixed before outcomes.
  - The lever is the climb's flux elasticity. With the thrust margin to survive solar maximum (ballistic
    coefficient 0.008 m2/kg) the climb takes 6.80 days at a constant F10.7 of 70, 7.25 at 130, 8.00 at 200 and
    8.55 at 240. Near stall (0.0095) it takes 6.95, 7.50, 8.60 and 9.70, steepening only past 240 (12.05 at
    280), where storms stall batches (1 to 2 of the history's launches never climbed).
  - The golden comes out at 7.05 to 7.64 days below 350 km. The right family (a physical replay on the
    planning flux, linear, log-log and quadratic regressions on the 81-day F10.7, and the launches flown
    within 15 of each window's planning flux) spreads 0.93 to 1.06 of its median.
  - The cheap routes, over three seeds, six windows and both regimes, as a share of the golden: the plan 1.01
    to 1.08, the all-history mean 1.01 to 1.06, the last four launches 0.97 to 1.05, the latest launch 0.97 to
    1.11, the plan scaled by the mean or recent overrun 0.97 to 1.06, launches in the same months 0.98 to
    1.14, and the straight-line trend 1.08 to 1.19. Only the trend clears the family's top, and at its nearest by
    0.04, under half the family's own width.
  - The eda6c8c screens, as code: the common-exposure subset fires, since the launches flown at the 2027 flux,
    filtered and divided, sit at 0.93 to 1.02 of the golden; variance-only passes; dispersion and truncation
    direction do not apply.
  - The overrun's other two causes give no stump either:
    - a procedural lengthening (a longer checkout) persists, so carrying the latest launches is the right
      forecast;
    - a heavier bus is a register column, so reading it hands the step over.
- **Paper screens, not coded.**
  - Storm-attributable loss net of background deployment failures (the excess over a baseline hazard): an
    operator flying about 2,500 satellites in 2020 to 2026 holds 50 to 70 batch-storm encounters. With a
    per-encounter loss fraction spread at a coefficient of variation near 1.5, the mean loss per encounter
    carries about 20 per cent at one sigma, against the under 10 per cent a 12-satellite tray bin can absorb.
  - Loss per onset by the batch's altitude at onset, or by the storm's intensity: the pooled rate carried onto
    a different mix is `composition_mix` (held for task165 and task173 in the queue), and it rests on the same
    encounter count.
  - The stragglers' long tail of time below 350 km (satellites with raising anomalies carry most of the storm
    exposure): the per-satellite mean from the orbit table is the careful route by default, a coin flip
    between a batch figure and a per-satellite one.
  - A loss per onset that rises with storm duration, since declining-phase recurrent storms last longer:
    unscreened; it needs a duration response fitted on the same few dozen encounters.
- **Redraw P1, 2026-10-19: an underwriting-year (risks-attaching) triangle whose recent periods' contracts attach
  late in the period, read on each period's own exposure clock** (prototype `p1_ev.py`, expected values). With 52
  per cent of a period's contracts moved from mostly 1 January to a 1 October inception, the period chain ladder
  files 0.55 to 0.93 of the true ultimate at ages 12 to 48 months (gamma payment patterns with means of 20, 30 and 45
  months), but Bornhuetter-Ferguson on the true prior files 0.79 to 0.99 of the true unpaid (0.88 to 0.94 at 36 to
  48 months on the 30-month pattern) and about 0.95 on the 2024 to 2026 total, so the textbook route for immature
  periods lands inside any bin the 30 per cent bar allows. A whole-period shift of inception is fixed exactly by the
  age-shift reflex (the old pattern read at the age less the shift). The re-based clock is also task468's live
  driver (development by months in the current episode, not since first activity) by the abstraction test, and
  `guard.py slots` on the driver hit task468's draw lines. Died at stage 1 on the BF reflex and the driver repeat.
- **Redraw P2, 2026-10-19: reports arrive sooner for recent accident years while settlement from report is
  unchanged, projected from reports and the payment delay from report** (prototypes `p2_ev.py`, `p2_sim.py`). On
  expected values, cutting the mean report lag from 12 to 4 months puts the chain ladder at 1.10 to 2.67 times the
  true ultimate and Bornhuetter-Ferguson at 1.05 to 2.20 times the true unpaid at ages 12 to 60. On a claim-level
  simulation (15 accident years, about 4,000 claims a year, larger claims settling later; seeds 1 and 2), the
  unpaid for accident years 2023 to 2026 over the truth is: paid chain ladder 2.01 to 2.17, Bornhuetter-Ferguson with
  the exact expected ultimate 1.19 to 1.20, Berquist-Sherman on all-years count ultimates 1.42 to 1.46, and
  Berquist-Sherman on latest-three count factors 1.05 to 1.08. The disposal-rate card is the careful reader's route
  once the reported-count factors visibly drop, and it lands within a bin. Died on the library test (stumping 1.3).
- **Redraw paper screens, 2026-10-19, each dead before code:**
  - a per-claim benefit cap that binds more as treatment intensity drifts up: task172's driver by the abstraction
    test (a per-unit cap that cut only the record's tail now binds most forward units), close to task168;
  - settlement speed through Berquist-Sherman or operational time: task127 architecture 3's mechanism (judge
    SEND_BACK, frequency-severity $350M against the restatement's $400M); case-reserve adequacy: task228's kill;
  - a calendar-year step (a fee schedule or benefit revision): a dated cause an event study finds, and rule
    application once filed; chronic calendar-year inflation: the forward rate is an assumption (a fork) or a filed
    index (rule application), with a lever of 5 to 15 per cent;
  - a tail from claimant-level annuities: a mortality-longevity task, a filed table is rule application, and the
    claimants' own deaths give about 6 per cent at one sigma; a fitted tail where the factor curve bends: the
    decay rate of late increments is too poorly determined (a 1 against 2 per cent decay halves the tail);
  - a reserve range or 75th percentile with diagonal dependence: the variance-only screen, and a spread estimated
    from 10 to 40 diagonals carries 20 per cent or more relative error;
  - chain-ladder leverage on immature years, additive against proportional development: the BF reflex lands;
  - every mix shift (channel, litigation share, claim type, deductible mix, closure order): `composition_mix`;
  - reopened claims by time since closure after closures accelerate: a lever of a few per cent (reopenings are a
    small share of the reserve), and returns by time since leaving read as task157's driver;
  - the split of development into new reports and growth on reported claims under a filed notification cut-off:
    once the window is filed as the WHAT, the report-year triangle and a reported-count projection are the careful
    reader's routes;
  - settlement timed by a litigation calendar's trial dates: task172's per-unit scheduled date ending the wait, and
    a timing-only lever on a reserve; claims-unit closure capacity: the swap test fails (any queue);
  - excess-layer, large-deductible and per-policy aggregate development: too few claims for a sigma near 1 per
    cent and an open per-claim family; retro-rating and corridor treaties: the contract formula is rule
    application; a large-loss transfer between claims systems: a filed threshold plus a join;
  - a closed exposed pool depleting as members claim (latent and mass claims): the hazard's shape on the remaining
    pool is a fork (constant against heterogeneous), the forcing rosters sit in epidemiology, and the natural
    instances are sensitive.
- **Second redraw D1, 2026-10-19: returners drawn from the area's diaspora (people born there living elsewhere), a
  wave that left at 20 to 30 in 1995 to 2010 now ageing into the return ages** (prototype `d1_diaspora.py`, expected
  values, return hazard 0.5 per cent a year at 25 to 49 and 2.0 at 55 to 69). On the 2027 to 2031 return flow the
  card-2 route (origin-destination rates by age on the origin population, struck over 2016 to 2025) files 0.62 of the
  truth, a linear trend 0.81 and the latest year carried about 0.75; at 55 to 74 the card-2 route files 0.08 of the
  flow. But on the 55 to 74 population level the returns move the figure about 4 per cent, and the abstraction is
  task134 v2 round 1's driver (an inflow that a pool held outside the decision's record sends at a hazard on that
  pool, whose composition shifted). The birthplace column on the in-migration records also makes the split a row
  predicate. Died on the driver repeat and the level lever.
- **Second redraw paper screens, 2026-10-19, each dead before code:**
  - duration-dependent out-migration after an influx (mover-stayer): task134's slot measured it at about 1 per cent
    (its `sim1.py`), and it is task468's and task134 v2's driver (a hazard by time since entry after a surge);
  - gross against net migration (card 2): task150 shipped it on school attendance areas, and task134's slot found
    the gross variants split unless every origin is static;
  - second births echoing a surge of first births (parity and interval): the same time-since-entry family;
  - housing-constrained growth: the housing-unit method (dwellings, occupancy, persons per household) or a
    headship-rate household projection is the field's textbook for a capped small area, and task79 carries the
    capacity insight;
  - turnover in a fixed stock as its occupants age in place (vacancy chains): task132's renewal driver;
  - special populations (students, prisons, barracks, care homes) that do not age in place: `population_selection`
    sits in the window (task270), and projecting group quarters apart is census practice;
  - the control-total gap allocated by the component that makes it up (card 4's judgment): the regional model's
    closed-system note reads it out, and each area's own external migration, the careful route, lands;
  - a births-based base for young children against a census undercount: a lever of about 5 per cent;
  - stated-coverage intervals with cross-area correlation (card 3's judgment): the variance-only screen, and a
    correlation estimated from 30 years carries about 15 per cent;
  - shrinkage choices (card 5): the shrinkage family (stumping 1.2);
  - fertility postponement and recuperation: a future-rate assumption, a fork;
  - cohort mortality improvement at 85 and over: the mortality-longevity card;
  - a group returning in a wave: task157;
  - two-sex births (partner availability): the marriage function's form is open (harmonic, geometric, minimum)
    and the real effect is weak;
  - simple trend methods beating cohort-component out of sample: `forecast_method_backtest` sits in the window
    (task177);
  - a caseload ageing out at a fixed age: task172's cap;
  - education-specific rates: a mix on a visible column;
  - an error-of-closure correction of the base: one past event per area and a back-test organ.

- **Third redraw E1, 2026-10-23 (cell general-statistics-data-science / bayesian-modeling-posterior-inference):
  the extra gifts a direct-mail fundraising programme's 2027 budget can count on from the package changes it adopts
  off its 2026 split tests, each adopted because its test cell beat control at a one-sided z of 1.96 or more**
  (prototypes `d2.py` to `d7.py`, `w1.py` to `w5.py` in the session scratchpad `b176n/proto`). The golden was the
  posterior mean of each adopted change's lift under the distribution of true lifts the programme's whole test
  record identifies (most changes near nil, a minority real), times the change's 2027 projected standard-pack gifts;
  the default path the tests' own lifts carried; the reflex a normal-prior empirical Bayes shrinkage. Measured on
  binomial test cells (1,980 to 4,850 tests, 20 to 50 adopted changes, 6 to 10 seeds a setting), as shares of the
  golden: the tests' own lifts 1.57 to 2.23, normal-prior shrinkage 0.62 to 0.85, a scaled-t prior 0.78 to 0.84, the
  lifts discounted by a Storey null share 1.07 to 1.66, the lifts weighted by one less the local false discovery rate
  1.13 to 1.57; the shape-aware family (grid NPMLE, a spike plus one normal, two and three normals) within 1 to 2 per
  cent where the truth is one spike and one slab, and the normal prior rejected by a likelihood ratio of about 500.
  Dead on two counts, both measured:
  - a Benjamini-Hochberg filter at 10 per cent on the season's tests, the survivors then counted at face value, lands
    at 0.96 to 1.07 of the golden on average in four configurations (0.53 to 1.28 seed by seed), and the survivors of
    z above 2.5 at face value at 1.03 to 1.16: a sparse prior's posterior mean is a soft threshold and an FDR filter
    is a hard one placed close to it, so the multiple-testing reflex reaches the call;
  - outside re-implementations of the golden itself spread 4 to 10 per cent: the prior fitted on absolute rather than
    relative differences 0.86 to 1.11 at 1,980 tests (0.97 to 1.02 at 4,850), fitted by test type 0.92 to 1.12, fitted
    on the 2023 to 2026 seasons only 0.88 to 1.09, the delta-method standard error on the linear lift 0.91 to 0.94
    against the null standard error, and a single slab 1.02 to 1.17 where the truth carries two.
  The house rule on levels at selected units and the winner's-curse verdicts in task200's and task471's notes say the
  same from the other side.
- **Third redraw C1, 2026-10-23: a permit's monthly compliance value moving from one grab sample to the mean of four,
  forecast as the 2027 count of monthly exceedances, the decisive split being the within-month variation the
  averaging removes against the month-level variation it keeps** (prototype `m1.py`). The confirmation re-samples
  taken after an exceedance give that split by a pair difference with almost no selection bias (measurement variance
  0.0917 against a true 0.09, the pair-route forecast 0.0331 against the golden 0.0333), so one group-by lands it, and
  the abstraction (a function of several new draws must carry what they share) is task143's driver in this cell,
  with the repeat-agreement split task246's.
- **Third redraw paper screens, 2026-10-23, each dead before or at a first harness:**
  - unseen classes still to appear (Good-Toulmin from the frequency of frequencies): the accumulation curve is the
    rarefaction of the same counts, so a best-fitting curve extrapolated to t of 1 or less reaches the Good-Toulmin
    figure (exactly, b ln 2, under a log-series truth), and past t of 1 the empirical Bayes family itself forks;
  - class shares re-estimated for a new intake under label shift: Rogan-Gladen on the validation sensitivity and
    specificity is a one-line textbook route to the golden, and the abstraction is task192's transported audit error;
  - drifting group effects or hidden states with a forward selection on recent results: the panel replays the same
    selection in past periods, a filter and a divide;
  - a slot's effect inherited by its next holder (positions, storefronts, sites): partial pooling by slot is card 1
    itself, the successor-on-predecessor regression interpolates the transfer, and past the record's range the
    frailty's tail forks it;
  - a volume-dependent shrinkage target for new small units: the record's units at that volume are the attaining
    subset, and below the record's range the curve's form forks;
  - marginal against conditional prediction for new groups in a log-link model: the pooled crude rate reaches the
    marginal mean, so the reflex is right and only the sophisticated route is wrong;
  - a forward sampling or instrument change read through a gauge or reference study: task246's driver;
  - a Bayesian sequential or stop-rule forecast: executing the filed protocol is rule application, and replaying it
    on the record's tests lands it.

- **Fourth redraw, 2026-10-23 (cell urban-regional-science / municipal-service-demand-resource-allocation,
  Forecasting, allocated by the main session with the criterion that the forward condition acts through a quantity
  the change does not name and no unit in the record has reached), paper screens, each dead at the draw.** The cards
  on the cell, task148 (a queue drained by callers who give up) and task165 (a gain conditioned on each unit's prior
  coverage), and the cell's client cards (complaints as reporting, small-area rate rankings, percentile standards)
  were read as spent or as the default path. The common grave: a forward change that is a deterministic transform
  of recorded cases is replayed on the record (apply it to last year's cases, a filter and a sum), and one that needs
  a behavioural or physical response beyond the record's range extrapolates a fitted curve whose form forks.
  - ambulance unit-hours after a hospital closes (each transport's distance to the nearest open hospital): the extra
    time is linear in distance, so the aggregate (affected transports times mean extra distance) equals the per-call
    sum, and replaying the closure on last year's geocoded calls lands it; the duration-times-count quantity is
    task142's driver and task179's slot screened the same ground; the receiving hospital's offload delay rising with
    its load extrapolates a congestion curve past the record's range;
  - garbage route-hours when collection moves from weekly to every other week (disposal trips set by tonnage over
    payload, not by visits): summing each pair of last year's route-days and re-counting the trips replays it;
  - water demand of a new low-yard housing type (indoor per person, outdoor per irrigable square metre): existing
    yardless metered units give the indoor per-capita rate, one group-by times the plan's persons per unit;
  - pickup requests under a new per-household cap, e-book licences that now expire after a set number of loans, the
    5 cm plowing trigger replacing 10 cm: each is the filed mechanic applied to last year's records, rule
    application plus a replay;
  - assessment appeals after a revaluation with jumps larger than any past cycle, 311 reports rising with faster
    response, paratransit trips under distance-based fares: response curves extrapolated past the record, the form a
    fork;
  - a proactive rental-inspection cycle pre-empting complaint inspections (complaints by time since the last
    inspection): the record's post-inspection units are complaint-selected, so the transfer needs a unit frailty
    whose form forks, and units inspected within three years are an attaining subset;
  - a permit review step moved past a statutory refund deadline: task172's driver; a triage line closing so its
    diverted calls return to ambulances: task169's driver.
  Also a standing block: `guard.py check` on a probe card returns `ban.pairing` against task175
  (urban-regional-science with Forecasting, registered 2026-10-23 and still a live card in the last three).

- **Fifth allocation, 2026-10-23, the cell left to this build's choice among the Forecasting task types outside the
  exclusions (the three domains in the last three registrations, the two cells above, task174's five, task173's and
  task177 to 179's), with the shape to look for named: the forcing input in a second file at a finer grain, entering
  by identity, leaving no part of the record unaffected.** No cell was drawn, because each candidate instance died at
  the draw:
  - quantitative-finance / strategy-backtesting-evaluation (each fill's half-spread from the quote file, the forward
    capital acting through each trade's participation): the spread and impact decomposition is the field's standard
    transaction-cost analysis, and under a power-law impact the forward cost is the present cost times one factor;
  - general-statistics-data-science / scaling-laws (training compute per run from the step log): 6 N D on the tokens
    trained is already the textbook x-axis, and the intermediate-checkpoint and floor corrections are the cell's cards;
  - human-factors-ergonomics / human-reliability-assessment (errors per opportunity from a step log, a forward work
    plan changing the conditions): either the condition exists in the record (attaining subset) or its fatigue or
    workload curve is extrapolated (form fork), and a second detection channel is a shipped mechanism;
  - education-learning-sciences / learning-analytics-early-warning-models (credits earned by identity from the course
    file under a new course size): within-student correlation of passes is task143's driver;
  - energy-systems-utilities / asset-condition-maintenance (starts or cycles from a dispatch log, transformer aging by
    the loading standard): per-start damage is one group-by, damage exponents fork, a filed aging equation is rule
    application, and `utility_or_infrastructure` is banned against task175;
  - healthcare-delivery-health-economics / patient-flow-beds-workforce-optimization (weekend discharge waits from the
    discharge-ready date): replaying seven-day discharge on the recorded ready dates is rule application;
  - actuarial-science-insurance / mortality-longevity and claims-frequency-severity (amount-weighted deaths, earned
    exposure from mid-term changes): each is the cell's own card or a small lever.
  The recurring death across the session: where a finer file forces a per-case quantity by identity, either the
  forward change can be replayed on the corrected record, or the identity makes the correction one group-by.

- **Sixth allocation, 2026-10-23 (cell sociology-demography / event-history-life-course-analysis, Forecasting),
  paper screens before the draw, each dead before a harness.** The cell's cards (competing endings as cumulative
  incidence, cause-specific against subdistribution hazards, repeated spells, left truncation) are the careful
  reader's routes, and task266 (competing endings) and task265 (late entry) are spent on file.
  - A state pension age moving from 66 to 67 for one birth cohort, retirements read on years to the pension age:
    the careful reflex shifts the spike with the pension age, and the golden differs from that full shift only by
    the age gradient at a fixed distance to the pension age, a few per cent; the record's earlier pension-age
    steps are a natural experiment a reader runs by default.
  - Divorce applications in the first year after a no-fault act removes the two and five year separation facts:
    the backlog of waiting couples is the reflex the act invites, and sizing it needs reconciliations during the
    wait that no record holds (a behavioural fork) or a right-truncation completion the field teaches as standard.
  - Benefit closures detected only at eligibility reviews when reviews move from annual to quarterly: the swap test
    fails (failures found at inspections reads the same), so the domain is a backdrop.
  - Care home self-funders crossing a raised capital limit: a deterministic shift of each depletion time,
    replayed, and social care finance rather than the life course.
  - Temporary layoffs ending in recall to the same employer removed by a short-time work scheme: labour economics,
    and a filter on the recall spells once the rule is read.
  - Care entry or moves by time since widowhood after a mortality shock, and childminders or foster carers whose
    exits follow a surge of entries: the hazard-by-time-since-entry-after-a-surge family (task134 v2, task468).
  - Naturalisation after a residence requirement falls from 8 to 5 years: either the language and income
    conditions are filed (rule application on a conjunction) or the transport from shorter-eligibility groups is
    confounded by who those groups are (a fork).
  - Joint retirement of spouses after one spouse's pension age moves: the lever on any population's total is a few
    per cent, capped by the share of couples the change reaches.
  - Same-sex couples marrying after a bar lifts (unselected long-duration couples): an analogue from one past
    legalisation, and a behavioural uptake.

- **Ask layer re-sited, 2026-10-23, before any reader (coordinator's stage 4 measurements).** Cut: a food program
  ask whose device was a sponsor's revised claim (same sponsor, home and month, later received) against a second
  sponsor's part-month claim (a home changing sponsor), and a visits ask whose device was a monitoring visit and a
  complaint investigation entered as two records at one arrival. The round's readers broke both shapes elsewhere (a
  re-filed schedule replacing the first against a supplement that adds members; fills grouped by time, trader and
  side), so neither is silent. Replaced by the subsidy money ask, whose device is a property of the payment run itself
  (the remittance amount on every child line and remittance numbers restarting in each county office's run); the two
  files stay as distractors.
- Round 1 ask layer (zip 13d6ad18, 2026-10-23): both readers took one remittance per run date and provider, which the
  per-county renumbering never touched because a remittance was one provider's (money 20 of 20 for each); reader B
  summed care_days and the judge named the fork in "child-days". Died as built: the renumbering device sat on a
  property the readers' natural unit made irrelevant. Child-days closed by the prompt and shrunk to two statewide
  figures; money moved onto network remittances, where the run-and-provider unit is the wrong one.

## Retired

**RETIRED 2026-10-19 under the author's rule that a number which dies in its second new cell this round is
retired.** Three worlds were screened at stage 1 and none held:
- the seed's satellite storm-loss world, two architectures on code;
- actuarial reserving triangles, P1 and P2 on code and 17 on paper;
- sociology population projection, D1 on code and 18 on paper.

No card was ever registered, so no guard axis is held. The screens above are the number's record for `guard.py
slots`.

## Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired, for a from-scratch rebuild in general-statistics-data-science
/ bayesian-modeling-posterior-inference (worktree `b_176n`). No candidate held at stage 1: E1 and C1 measured dead on code
and eight more directions dead on paper, all in `## Tried and rejected`. No card registered; PAUSED for another cell.
The main session then allocated urban-regional-science / municipal-service-demand-resource-allocation; nothing held there
either (paper screens in `## Tried and rejected`, and `ban.pairing` against task175 standing), so the number stays PAUSED for
another cell.
A fifth allocation, left to this build's choice of cell, found no Forecasting task type where the named shape lives
naturally (`## Tried and rejected`); the number stays PAUSED.
A sixth allocation, sociology-demography / event-history-life-course-analysis (Forecasting), drew architecture 2 on
2026-10-23: Allerton's 2027 family child care home closures, each home's hazard read on its provider's youngest
own child's kindergarten year (`## Draw`); the number is live again.
