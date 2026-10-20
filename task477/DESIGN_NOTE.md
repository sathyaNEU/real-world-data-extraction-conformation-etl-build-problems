# task477 design note: the Tallis Valley workforce board's 2027 sector-partnership slate

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task477.json` (architecture v1), registered 2026-10-20 with WARNs only
  (ETL in 6 of 12 is the lane; shape 01 in 4 of 12; Gate G method_or_model_selection after task471 and task476, the
  decisive step being how each industry's pay-date exposure is estimated among defensible methods; "which" after
  task471 and task476, the slate being a pick of four). The first draft's decisive generator G13 repeated task476's
  driver signature and was redrawn to G3 (the record counts pay when it is paid, the decision runs on the work it
  pays for), the honest label; csv+xlsx repeated task472's set and became csv+docx. Nearest driver task102 at 0.07.
- **Seed:** ET34 (a county's private-sector average weekly wage jump read from QCEW). Kept: the world (a county
  labor market's covered-wage record), the decision (which industries' pay per job really grew) and the quantity
  (pay per job by industry). Dropped: the seed's hierarchy, ownership and suppression mechanism, which is Layer 1
  mess here.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production / Data
  Extraction & Conformation (ETL). The board conforms the state's quarterly covered-wage files (wages counted in the
  quarter they are paid, several releases, two layouts) into an earned-basis wage series by industry, the pay for the
  work done in each calendar year, and ranks industries on it.
- **Shape:** 01, a ranked list under a cap: each industry's 2021 and 2025 earned pay per job and growth, the four
  funded, the runner-up and its gap, the files.
- **Strategy:** composition_mix. Each industry's payroll is a mix of pay schedules (weekly, every other Friday on
  one of two alternating weeks, twice a month, monthly), recorded nowhere; 2021 holds 53 Fridays and, for one
  alternating-Friday phase, 27 pay dates, so each industry's 2021 wages are inflated by its own unseen mix. Decisive
  generator G3, with G6 (the schedule mix) and G17 (the exposure estimated from quarterly pay-date counts).
- **World:** United States, a fictional multi-county labor market region in an unnamed state. The Tallis Valley
  Workforce Development Board files its 2027 to 2029 sector-partnership slate (four industries) with the state's
  sector-partnership fund; the slate is the four industries with the fastest growth in pay per job from 2021, the
  program's base year, to 2025. Personas from `guard.py names --geo "United States" --seed 477`: Beverly Ray (labor
  market analyst), Dalton Harding (executive director).
- **Data-native sentence:** the county file counts wages in the quarter they are paid, a pay date falling on New
  Year's Day is paid on 31 December, and 2025 is the year in which that moved a 53rd Thursday and a 27th alternate
  Thursday into the books, so every industry's 2025 wages carry its own unrecorded share of Thursday payroll as an
  extra pay date while 2021 carries none.
- **Forcing fact:** the board votes on 5 November 2026 and files with the Council by 15 January 2027; the slate funds
  2027 to 2029 (forward). Its quantity is the closed 2021 and 2025 years the guidelines name (retrospective by the
  Fund's rule).
- **Forum and forcing event:** funder_or_donor (the state's Sector Partnership Fund), vote_or_meeting (the board's
  slate vote). Organisation family nonprofit_or_charity (a workforce development board).

## Default path

1. Read the guidelines: eligible industries are private NAICS sectors with 2025 annual average jobs of 1,000 or more;
   rank them on growth in pay per job, the pay earned for the work performed in each calendar year over annual
   average jobs, 2021 to 2025; the slate is the top four.
2. Conform the county file: Tallis County (52037), own_code 5, agglvl_code 74, the three releases stacked with the
   2025 annual release over the first-published 2025 quarters, the 2013 to 2019 layout's renamed column mapped.
3. Take each industry's annual wages and annual average jobs (the twelve monthly levels) for 2021 and 2025; pay per
   job is wages over jobs (the county file's own annual average pay); rank the growth.

Ends on: Information, Finance and insurance, Transportation and warehousing, Health care and social assistance on the slate

Golden: Information, Finance and insurance, Professional, scientific, and technical services, Construction on the slate

## Stump sentence

The default path ranks industries on wages per job as the county file records them, and so files Information, Finance
and insurance, Transportation and warehousing, Health care and social assistance on the slate, with a Friday-only
payday check finding nothing to correct; the record counts wages in the quarter paid, and 2025 carried an extra
Thursday pay date (New Year's Day 2026 paid on 31 December 2025) for the share of each industry's payroll run on
Thursdays, which no file records and hospitals and trucking and warehousing hold most of, so only each industry's
pay-date exposure estimated from its own quarterly record puts the slate on the work done.

## Three rules

Task type: Survey Research & Official Statistics, seasonal-adjustment-official-time-series-production, which the taxonomy tags for ETL: conforming three releases of the quarterly covered-wage file into a series of pay for the work done in each year, with the calendar (pay-date) effect estimated and removed as official series production does.

Domain test: the quantity that decides the call is each industry's growth in pay per job for the work done in 2021 and 2025, worked as official time-series production works a calendar effect: a regression of the quarterly series on the count of pay dates each quarter holds, by schedule, with year and quarter effects, and the estimated effect removed from the years it distorts.

Swap: "which four hospitals' megawatt-hours per bed grew fastest" keeps the words but loses the step: nothing in metered energy is booked on a pay date, and the fixed-interval pay schedules, the quarter-of-payment rule of unemployment-insurance wage reporting and the holiday rule that moves a pay date across the year end are what create the effect and what identify it.

Layer 1: three releases with the first-published 2025 quarters revised by the annual release (the state's QCEW publication cycle); two layouts (qtrly_estabs_count renamed in 2020); ownership and aggregation-level codes in one long file; suppressed subsector cells flagged N (the disclosure screen); retail subsectors recoded to NAICS 2022 from 2022; monthly employment on the 12th against quarterly wages; each asserted neutral on the call in checks.py (R2).

Layer 2: estimation_fit. The methodological choice is how wages paid become pay for the work done: as recorded, with one assumed pay-schedule mix, with a mix fitted to the county total, with Friday pay dates only, or with each industry's exposure to every Friday and Thursday phase estimated from its own quarterly record.

Decisive step: estimating each industry's share of payroll on each alternate-week Friday and Thursday phase from how its quarterly wages per job move with the pay dates each quarter holds (holiday pay dates paid the business day before), and dividing the 2021 and 2025 wages by the paid-to-earned ratio those shares imply.

Not semantics: reading every field correctly, including that total_qtrly_wages are paid during the quarter regardless of when the services were performed, still leaves the easy routes on the wrong slate: the record names no industry's pay schedule, a Friday-only check finds 2021 and 2025 both normal, and one assumed mix moves every industry alike; the step is an estimate, not a reading.

Not rule application: the guidelines file the population (eligible private sectors), the outcome (pay for the work performed in each year over annual average jobs), the years and the slate; no filed rule says which schedules a payroll runs on or how to remove an extra pay date, and executing every stated rule on wages as recorded files the wrong slate.

Analyst test: a strong analyst who conforms the releases and reads every field and rule correctly, and ranks wages per job as recorded or corrects with one assumed mix or with Friday pay dates, files Information, Finance and insurance, Transportation and warehousing, Health care and social assistance on the slate (the default path's Ends on); only each industry's estimated exposure files Information, Finance and insurance, Professional, scientific, and technical services and Construction.

Estimand: guidelines 2.1 to 2.3 (sector_partnership_fund_guidelines_2027.pdf) file the population (private NAICS sectors with 2025 annual average jobs of 1,000 or more), the outcome (pay earned for the work performed in the calendar year over annual average jobs), the years (2021 and 2025), the unit (growth, 2025 over 2021 less one) and the comparison (the four highest).

No decoy: nothing is planted to be caught; no memo, draft, earlier slate or stakeholder figure ships, and the county file is the state's ordinary publication, true as published; the two distractors are a projection and a survey of occupational wages, neither ranking industries on the Fund's measure.

No certified replay: no certified or published figure is reproduced to recover the method; the pay-date exposure is read from the quarterly record's own response to the calendar, not fitted to a reported total.

Lesson: a series booked when money moves rather than when value is created carries the calendar into every comparison, and the size of the distortion is a property of each unit's payment schedule, measurable from how the unit's own history responds to the calendar; no build on file estimates a calendar effect from a record's own response to pay-date counts.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, wages per job as recorded (51, 52, 48-49, 62) | guidelines 2.2 names pay for the work performed: fires | total_qtrly_wages and the monthly levels: fires | the county file's annual average pay: fires | none | none | one division: fires | readable |
| R1, one assumed pay-schedule mix for every industry (51, 52, 48-49, 62) | none | none | a 53rd-Friday or 27-pay-period correction: fires | none | none | one ratio: fires | readable |
| R2, Friday pay dates only, fitted (51, 52, 48-49, 62) | none | none | the common payday is Friday: fires | none | none | a regression | readable |
| R3, exposures without the holiday shift (51, 52, 23, 48-49) | none | none | pay dates counted on the calendar: fires | none | none | a regression | readable |
| G (decisive), each industry's exposure to every Friday and Thursday phase, holiday dates paid the day before (51, 52, 54, 23) | no clause names a schedule, a weekday, a phase or a holiday rule | no column holds a schedule or a pay date: the exposure is the quarterly record's response to the calendar | no reflex correction reaches Thursday phases | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | annual average jobs | the mean of the twelve monthly levels | third-month levels | same call (asserted) | guidelines 2.2 "the mean of the twelve monthly job counts" |
| SF2 | 2025 figures | the 2025 annual release | the first-published quarters | same call (asserted) | the layout notes: the annual release replaces the first-published figures |
| SF3 | 1,000 or more | 2025 annual average jobs at or above 1,000 | above 1,000 | same call (nearest industry 221 jobs from the line, asserted) | guidelines 2.1 |
| SF4 | pay per job | pay earned for the work performed in the calendar year over annual average jobs | wages paid in the year over jobs | not the Fund's measure: files 51, 52, 48-49, 62 | guidelines 2.2 "for the work they performed in that calendar year" with the layout's "paid during the calendar quarter, regardless of when the services were performed" |
| SF5 | a pay date on a holiday | paid the business day before | the day after; not moved | the record rules them out: the day-before rule fits 62 and 48-49 8.5 and 16.9 times better (asserted) | the data (C2) |
| SF6 | the slate's ranking | unrounded growth | whole-percent growth | same call (the fifth 18 per cent, the fourth 19, asserted) | guidelines 2.3 |
| SF7 | weekly payrolls | half on each alternate-week phase of the weekday | a separate weekly regressor | same call (collinear; the family names one slate, asserted) | the calendar: weekly dates are the union of the two phases |
| SF8 | the years | 2021 and 2025 | 2020 and 2025 | not the Fund's measure | guidelines 2.2 "from 2021, the Fund's base year, to 2025" |
| SF9 | industry | NAICS sector, 31-33, 44-45 and 48-49 each one | three-digit subsectors | not the Fund's unit | guidelines 2.1 |
| SF10 | private | own_code 5 | total covered (own_code 0) | not the Fund's population | guidelines 2.1 "private-ownership NAICS sector" |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (growth in pay per job, 2021 to 2025, per cent).

- **R0, wages per job as recorded (51, 52, 48-49, 62; next 54).** Transportation and warehousing 20.3 and Health care
  19.7 pass Professional services 19.2 and Construction 18.8. Dies to guidelines 2.2 with the layout's definition:
  wages are counted when paid.
- **R1, one assumed mix (51, 52, 48-49, 62).** A uniform correction moves every industry alike and leaves the order.
  Dies to the record: the industries' 2025 fourth quarters jump by different amounts.
- **R2, Friday pay dates only, or a mix fitted to the county total (51, 52, 48-49, 62).** Fridays fell normally in
  both years; the county total spreads the Thursday payrolls over every industry. Dies to the record's fit.
- **R3, exposures fitted without the holiday rule (51, 52, 23, 48-49).** Counting 1 January 2026 in 2026 leaves 2025
  normal and misfits every 27-date year. Dies to the fit (SF5).
- **G, the decisive move (51 21.9, 52 21.1, 54 19.2, 23 18.9; next 31-33 18.2).** Each industry's exposure fitted
  on its own 52 quarters; Health care falls to 17.7 and Transportation and warehousing to 17.9. The truth (pay for
  the work done, generator only) names the same four and the same fifth.
- **Margins (cut pack):** the golden's fourth over fifth by 0.70 points; the paid route's fourth over fifth by 0.52;
  the golden family (year or trend effects, logs or levels, wages or wages per job, 2016 on, without 2020) names one
  slate and prints every growth at the same whole percent, the nearest edge 0.14 against a largest spread of 0.26.
- **Position, separation and dominance:** a top-four pick; R0, R1 and R2 name one wrong slate, R3 another, G the
  golden; only the estimated Thursday exposure takes Health care and Transportation and warehousing off together.
- **Worth:** the slate (4), the next in line and every eligible industry's growth (15); R0 keeps two of the slate and
  five of the growths, so the asks carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | private NAICS sectors with 2025 annual average jobs of 1,000 or more in Tallis County (guidelines 2.1) |
| 2 | Unit of account | the industry; growth in pay per job, per cent |
| 3 | Attribution window | the calendar years 2021 and 2025, pay for the work performed in each (SF4, SF8) |
| 4 | As-of dating | the 2025 annual release of June 2026 |
| 5 | Version basis | the latest release of each quarter (SF2) |
| 6 | Denominator | annual average jobs, the mean of the twelve monthly levels (SF1) |
| 7 | Weighting | none across industries; each industry's own wages and jobs |
| 8 | Window length | two calendar years |
| 9 | Boundary inclusivity | 1,000 jobs or more (SF3) |
| 10 | Rounding path | the ranking on unrounded growth; growth printed whole (SF6) |
| 11 | Tie-break | none needed: the fourth over the fifth by 0.70 points |
| 12 | Maturity and censoring | 2025 complete in the annual release |
| 13 | Order of operations | exposures, the paid-to-earned ratio, pay per job, growth, the ranking |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | the latest release of each quarter |
| 16 | Identity normalisation | the 2020 column rename; NAICS 2022 retail codes below the sector |
| 17 | Netting | none |
| 18 | Dimensional units | dollars, jobs, per cent |
| 19 | Code and status semantics | own_code 5, agglvl_code 74, disclosure N; never the stump |
| 20 | Integerisation | none before the ranking |
| 21 | Clause scope | guidelines 2: the 2027-2029 round |
| 22 | Forward window contents | the 2027 to 2029 slate on the closed 2021 and 2025 years the guidelines name (Draw) |

## Literal reader

Executed word for word, the guidelines fix the population (private sectors with 2025 annual average jobs of 1,000 or
more), the outcome (the pay employees earned for the work they performed in each calendar year over annual average
jobs), the years and the slate. The layout notes say the county file's wages are paid during the quarter regardless
of when the services were performed, so the filed outcome is not in the file and has to be estimated. The candidates
are the record as is, a uniform correction, a correction on the common Friday pay dates, and each industry's exposure
to every schedule estimated from its own quarterly record. The data separate them: the quarterly record responds to
the pay dates a quarter holds, Thursday phases included, and the day-before holiday rule fits each Thursday-paying
industry's record many times better than the alternatives (SF5); every estimator of the exposure in the family (year
or trend effects, logs or levels, per job or not, shorter windows) names the same slate and prints the same whole
percent for every industry (checks.py). Every write-up step names the file and rule it executes.

## Oracles

None. No control, published figure or reconciliation ties only under the golden: the county file's own average weekly
wage is on the paid basis and ranks nothing the Fund uses, and no earlier slate, memo or ranking ships.

## Ask sheet

- **Ask A, each eligible industry's 2025 exiters employed in the second quarter after exit: 15 figures.** H18 home:
  guidelines 3.2, the application reports it for every eligible industry; a measure every industry carries that the
  slate does not turn on. Path: the exits, the wage-record match return, the employer accounts, the PEO client
  registrations, the manual: five files, eleven columns. Primary device: D7, the true key elsewhere. A business that
  leases its staff through a professional employer organization is reported under the PEO's account, which the
  employer file codes to NAICS 561330, so the exiter lands in Administrative and support; only the return's
  rptg_unit against the registrations' client_seq finds the client business and its industry. Hazards (filed, the
  battery executes them): co-enrolled exits, repeat exits (the last counts), two employers in the quarter (the most
  pay), zero-wage rows.
- **Ask B, each eligible industry's 2025 ITA payments: 15 figures.** H18 home: guidelines 3.3. Path: the check
  register, the voucher ledger, the training provider list, the guidelines: four files, nine columns. Primary device:
  D6, a ledger at another grain than its name: the fiscal agent pays each provider one check per run covering every
  installment due since the last run, and the ledger carries the voucher's whole amount on each installment line, so
  summing the lines, taking each voucher once or splitting a check in proportion to the voucher amounts all miss;
  only voucher_amount over of_installments per line (the last taking the cents left) ties each check exactly.
  Hazards: voided and reissued checks, 2024 checks absent from the register.
- **The construction layer:** the slate, the next in line, every industry's growth; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no exit, wage-record, employer, PEO, ledger, check or
  provider row.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, exiters employed by industry | each exiter once at the last exit, the second quarter after it, the business paying most, its NAICS from the employer file; PEO-reported rows land in sector 56 and leave their client industries short, so every industry's count falls outside its bin | miss |
| B, ITA payments by industry | the 2025 checks net of voids, each split over its ledger lines in proportion to their voucher amounts; installment counts differ within a check, so every industry's total falls outside its bin | miss |

- Mirror leakage: 0.0 per cent of ask weight (the asks read no rung's construction).
- Pair ceiling: 32.6 on the cut pack (weights 38 / 7 / 55; the cracker keeps the main block and instructions, 45.0,
  and none of the 30 ask figures; the mirror, R0, keeps 7 of 20 main figures, 20.3).
- Measured by: generator/ceiling.py

## Tried and rejected

- First draft of the mechanism, 2021's 53rd Friday and 27th alternate Friday inflating the base year: dead at the
  prototype, because a Friday pay date on New Year's Day is paid on 31 December, so the extra date fell in 2020 for
  every Friday payroll and 2021 was a normal year; the holiday rule moved the live year to 2025's Thursdays.
- Graded pay-per-job levels in a conformed series CSV: dropped before the pack was cut, the estimator family spread
  the levels by up to $245, so the deliverable became one row per industry with growth at a whole percent.
- Ask B as checks paid one per installment: dropped before the pack was cut, guidelines 3.3 points straight at the
  register and the check amount answers it; the fiscal agent's batch runs moved the device onto the ledger's grain.
