# task465 design note: Callowmere Electric's 2027 medical energy assistance caseworkers

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: the slot's seed
world (a drought cover) was spent across a rainfall draft and architecture 1 (area-yield covers with withheld drought
years, sent back by the determinism judge on Gate H), and architecture 2 is drawn afresh in the ETL objective.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task465.json`, architecture v2, re-registered 2026-10-17 after
  architecture 1's SEND_BACK; architecture 1 and the rainfall draft are in its lineage with their fates. `guard.py
  check`: WARN only, answered below.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL. The task
  type's own work here is statistical matching: two surveys of the same households, each measuring one of the two
  eligibility traits, fused through the variables they share, with an auxiliary sample that measured both. The
  conformed division-by-income-band table is the ETL deliverable the staffing is set on.
- **Why this mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457), capture and coverage
  of registers (448, 454, 455), links and continuity (449, 455), a link through shared items (450), a rotating panel's
  measurement change (453), a stratified sample on a revised map (452), latent classes (456), observation selected on
  the trait (458), an operating level (459), a dispatch margin (460), an overlap extension (461), detection-weighted
  snapshots (462), a drift-free price index (463), a change in each unit's own record (464 v1) and withheld cells
  recovered from totals (465 v1). None fuses two sources that never observed the decisive pair of variables together.
- **Shape:** 07, a grid of cells: nine service divisions, each with its eligible households and its caseworkers (18
  cells), the total caseworkers, the eligible households of each division and band in the conformed table (18 cells),
  the chart's named parts and the two files (42 before the asks); the asks add a figure per division each (18).
- **Strategy:** composition_mix (F5): the health survey's equipment rate is correct for each division and income band
  but does not fit the pool of energy-burdened households inside the band, whose rate is higher; the pool's rate is
  rebuilt from the screening pilot, which observed both traits. Gap population (the eligible households are the joint
  of two traits; the default path counts independent coincidences). Generators G14 (decisive) and G16 (which fusion
  the data entitles). Gate G method_or_model_selection. Layer 2 family estimation_fit.
- **World:** an unnamed state on Central Time. Callowmere Electric Company, its investor-owned electric utility, runs
  the Home Energy Medical Assistance programme (HEMA) for customers with household incomes under $50,000 whose annual
  home energy costs exceed 6 per cent of income and in whose homes someone relies on electrically powered medical
  equipment (oxygen concentrators, home dialysis, ventilators, powered wheelchairs, feeding pumps). Its caseworkers
  enrol eligible households in the medical baseline rate, arrange payment plans and place backup batteries. The
  utility files its 2027 HEMA plan with the State Utility Commission by 1 December 2026; the plan staffs one caseworker
  for every 400 eligible households in a service division, or part of that number. No survey asked both eligibility
  questions: the State Energy Office's Household Energy Affordability Survey 2025 (9,000 households, county-stratified)
  measured energy costs and income, the State Department of Health's State Health Survey 2025 (12,000 households)
  measured the equipment, both weighted to the State Demographer's 2025 household estimates by county and income band,
  and Callowmere's 2025 HEMA screening pilot asked both questions at random residential addresses in its two
  metropolitan divisions (North Metro and South Metro; 8,874 screens returned, 3,309 complete below the income limit).
  Kestrelmere County moved from the Central to the Southwest division on 1 July 2026; the division register is the
  current map, and accounts opened before the move keep the division they were set up under.
- **Data-native sentence:** the equipment that makes a household eligible also runs up its electricity bill (in the
  pilot, homes with the equipment pay $1,128 a year for electricity against $851 under $25,000, and $1,524 against
  $1,089 from $25,000 to $49,999), so inside every income band the two traits go together; the state measured them in
  two surveys of different households, and only the utility's screening pilot asked both questions of the same
  homes, in two of the nine divisions.
- **Forum and forcing event:** regulator_or_inspector (the State Utility Commission receives the plan),
  statutory_or_regulatory_filing (the 2027 plan, due 1 December 2026); organisation utility_or_infrastructure; role
  capacity_planner. Personas from `guard.py names --geo us --seed 465`: Stacy Williams (HEMA programme manager, who
  sets the staffing), Shawn Taylor (vice president, customer programmes). As-of date 16 November 2026.
- **Sources (one line each):** the client's data-integration pattern (propagate linkage error) teaches that a
  combined estimate inherits the integration's error; here the integration error is the matching assumption, not a
  link. task256 carries a reference survey to members through a conditional distribution; here two surveys measure
  different traits of one population. task233 transports a departure on the odds scale; here nothing is transported
  across levels, the odds ratio is the pilot's within-band association kept inside each cell.
- **WARN answers:** `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection after task235 and task264): the
  method chosen here is the fusion of two surveys, a data-integration estimate the other builds do not make;
  `repeat.question_form` (how-many after task264): the decision is a count of caseworkers per division.

## Default path

1. Read the energy survey's household file: annual home energy costs (electricity times 12 where it was reported as a
   typical monthly bill, plus utility gas and other fuels) over household income, high burden above 6 per cent; income
   band from income; service division from the county code through the division register; the final-weighted share
   with high burden in each division and eligible band.
2. Read the health survey's household file: service division from the county code, income band from its eight income
   categories, the equipment item with don't-know and refused answers left out; the household-weighted share with the
   equipment in each division and eligible band.
3. Households in each division and band from the demographer's county figures (the surveys' final weights total the
   same).
4. Eligible households in each division and band: households times the burden share times the equipment share (the
   two surveys aligned on division and band, the traits taken as independent inside the cell); summed by division.
5. Caseworkers: each division's eligible households over 400, rounded up.
- **Ends on:** staffs 26 caseworkers.
- **Golden:** staffs 38 caseworkers, the eligible households in each division and band fused from the two surveys'
  shares with the screening pilot's odds ratio between high burden and the equipment inside each income band (3.49
  under $25,000, 3.47 from $25,000 to $49,999), each cell keeping both surveys' shares.

## Stump sentence

The default path aligns the two surveys and multiplies each division-and-band cell's burden share by its equipment
share, treating the two traits as independent inside the cell, so it counts 8,200 eligible households where the fused
table holds 13,300 and staffs 26 caseworkers where the programme needs 38; carrying the screening pilot's within-band
association into each cell, with both surveys' shares kept, counts them, while the pilot's own shares (42), one survey's
share times the pilot's conditional rate (51 and 33) and the product scaled by the pilot's dependence ratio (41) each
break a survey's share in some cell and staff other wrong numbers.

## Three rules

- **Task type:** data integration (data-integration-record-linkage-entity-resolution): statistical matching of two
  surveys of the same households with an auxiliary sample that observed both variables; the ETL objective's conformed
  division-by-band table is the dataset the staffing is set on.
- **Domain test:** the deciding quantity is each division's count of households carrying both traits, a joint
  distribution no large survey observed; the field's method is statistical matching with auxiliary information, the
  auxiliary sample's within-cell association carried into tables calibrated to both surveys' estimates.
- **Swap:** General Statistics, so the swap is of the method: replace the fused joint with the product of the two
  surveys' rates (conditional independence) and most divisions' staffing changes; replace it with the pilot's own
  shares and it changes again. A noun swap (clinics for divisions, smoking for burden) keeps the same fusion, because
  the domain here is the method.
- **Layer 1:** the two surveys on different geographies (county names and service divisions in one, county codes and
  public health districts in the other: the agencies' own sampling frames); income in dollars in one and in eight
  categories in the other (each survey's questionnaire); energy costs as annual totals or monthly averages (how
  respondents answered); a base and a final weight in one survey and a person and a household weight in the other
  (their weighting files); don't-know and refused codes (the questionnaire); pilot screens duplicated where an address
  answered by mail and by phone (the utility's screening system); household estimates published with division
  subtotals and a state total among the county rows (the demographer's release). Nothing is placed to be caught.
- **Layer 2:** estimation that fits the data: statistical matching beyond conditional independence. The choice that
  flips the call is how the joint of the two traits is built from sources that never measured them together.
- **Decisive step:** fuse the two surveys' division-and-band rates with the screening pilot's within-band odds ratio,
  an association-preserving fusion that keeps both surveys' rates, instead of multiplying the rates.
- **Not semantics:** every field read correctly (burden from annualised costs, the eight categories nested into the
  four bands, the household weight, don't-know and refused left out, county codes to divisions) still leaves the
  product of the two surveys' rates; what moves the call is the analysis that the two traits go together inside the
  cells, which no field, code or definition states.
- **Not rule application:** no filed rule says how the two surveys combine into the eligible count; the plan's data
  annex requires the conformed table to agree with the household estimates and both surveys' weighted estimates, which
  the product of the shares satisfies as well as the fused table, so executing every filed rule still files the
  default (26).
- **Analyst test:** a strong analyst who aligns both surveys' geographies and income bands, annualises costs, uses the
  right weights, drops don't-know and refused answers and reads the plan's caseload standard joins the two surveys'
  shares on division and income band and multiplies them, and staffs 26 caseworkers (the default path's `Ends on:`).
- **Estimand:** the HEMA plan's eligibility, data annex and staffing standard (`callowmere_hema_plan_2027_draft.pdf`):
  eligible households are households in the territory with incomes under $50,000 whose annual home energy costs exceed
  6 per cent of income and in which someone relies on electrically powered medical equipment at home, counted for
  each service division and income band for 2025, the latest survey year; the conformed table agrees with the
  demographer's household estimates and with each survey's weighted estimates; one caseworker for every 400 eligible
  households in a division, or part of that number.
- **No decoy:** nothing is planted: the pilot is the utility's own test of its screener, its association is the
  equipment's electricity use, no memo argues for independence, and no file states an eligible count.
- **No certified replay:** no certified figure is reproduced to recover a method; the surveys' published estimates are
  inputs the fused table keeps, never a key to the method.
- **Lesson:** two sources that each measured one trait cannot be joined on the attributes they share and multiplied
  when a third source shows the traits go together inside those attributes; the joint has to carry that within-cell
  association into tables that keep both sources' estimates. No build on file teaches statistical matching's
  conditional-independence assumption.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 each division-and-band cell's burden share times its equipment share, the traits independent inside the cell (26; the default path) | the plan's annex asks for a table by division and band agreeing with the households and both surveys' estimates, which the product satisfies | two surveys keyed by county and income, no household in both | yes: join on the shared variables and multiply | no | no | one product per cell | readable |
| R0b the same with each division's two bands pooled (25) | the plan staffs by division | division-level shares | yes | no | no | one product per division | readable |
| R1 the pilot's own share with both traits in each band, applied to every division (42) | none | the pilot holds both answers on each screen | yes: decompose the pilot | no | no | one share per band | readable |
| R2 one survey's share times the pilot's conditional rate: the energy survey's burden share times the pilot's equipment rate among high-burden screens (51), the health survey's equipment share times the pilot's burden rate among equipment screens (33) | none | the pilot's answers by band | yes: impute the trait a survey lacks from the file that has it | no | no | one product per cell | readable |
| R2b the product scaled by the pilot's share with both traits over the product of its two shares (41) | none | the pilot's shares by band | yes: a dependence ratio | no | no | one ratio per band | readable |
| R3 the pilot's within-band association carried into every cell with both surveys' shares kept: the pilot's band table raked to each cell's two shares, or its odds ratio fused with them (decisive) | no: the plan files the eligibility, the table's agreement with the households and both surveys, and the caseload standard; no sentence names an association, an odds ratio, raking, independence or the pilot as a source for the count | no column holds a joint share, an association or a referral flag; the pilot report counts screens by status and mode | no: the reflexes land on 26, 25, 42, 51, 33 or 41; raking the pilot to its own divisions' shares reaches two of nine divisions | no | no | no: a quadratic per cell, or a raking run to convergence | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | eligible household | income under $50,000, annual home energy costs above 6 per cent of income, someone in the home relies on electrically powered medical equipment | income at or under $50,000; costs at 6 per cent or more | same call: no surveyed or screened household at an income of exactly $50,000 or within 0.12 points of 6 per cent (asserted) | the plan's eligibility section |
| SF2 | annual home energy costs | electricity (a typical monthly bill times 12 where so reported) plus utility gas plus other fuels | electricity alone; the monthly bill taken as the year's | electricity alone: fewer eligible, a different call; the monthly bill: same call (asserted, R2) | the plan's eligibility ("electricity, natural gas and other home heating fuels"); the technical notes' cost items |
| SF3 | 2025 eligible households | the households of 2025: the 2025 surveys over the demographer's 1 July 2025 estimates | households projected to 2027 | not executable: no projection ships | the plan's annex ("the latest survey year") |
| SF4 | service division | the division register's current map (Kestrelmere in Southwest) | Kestrelmere under Central, its division before 1 July 2026 | a different Central and Southwest | the plan's staffing section (the nine divisions of the company's division register); the register holds one division per county |
| SF5 | household | the surveys' household and the demographer's household | persons or adults | same call: no person weight ships; the household weights reproduce the demographer's households | the codebook (HH_WT) and the technical notes (WT_FINAL) |
| SF6 | someone relies on the equipment | the health survey's MEDEQUIP yes, among yes and no; don't know and refused left out | don't know and refused counted as no | same call (asserted, R2) | the codebook's estimation note |
| SF7 | income band | the demographer's bands; the health survey's categories 1 to 3 under $25,000 and 4 to 5 from $25,000 to $49,999; the energy survey's dollars cut at $25,000 and $50,000 | none open | same call: the categories nest exactly (asserted) | the codebook's category labels |
| SF8 | weights | the energy survey's WT_FINAL; the health survey's HH_WT | the energy survey's WT_BASE | same call (asserted, R2) | the technical notes and the codebook |
| SF9 | households in a division and band | the demographer's county figures summed over the register's counties | the surveys' weighted totals | same call: the final weights reproduce the county figures (asserted) | the technical notes' and the codebook's calibration notes |
| SF10 | caseload standard | one caseworker for every 400 eligible households in a division, or part of that number (rounded up, division by division) | rounded to the nearest; the territory total over 400 | a different call | the plan's staffing sentence ("in a service division, or part of that number") |
| SF11 | rounding path | caseworkers from the unrounded counts; households to the nearest hundred | caseworkers from the rounded counts | same call: every division 90 or more households from a step (asserted) | the prompt's rounding sentence |
| SF12 | an address screened twice | its latest complete screen | both screens; the first | same call (asserted, R2) | the pilot report's screen rule |
| SF13 | partial screens and don't-know answers in the pilot | left out of the pilot's tables (no equipment answer) | counted as no | same call (asserted, R2) | the pilot report |
| SF14 | the conformed table agrees with each survey | each cell's burden share is the energy survey's final-weighted share and its equipment share the health survey's household-weighted share, its households the demographer's | none open | the pilot's own shares, the conditional imputations and the dependence ratio break it (cells with more eligible households than households with the equipment, or burden shares the energy survey does not hold; asserted) | the plan's annex |
| SF15 | estimation domain of the eligible households | each division and band as a whole: each survey's division-and-band share and the division-and-band households | county by band, summed to the divisions | same staffing; Central 1,432 eligible households (1,400) and Southwest's under-$25,000 cell 1,618 (1,600), each county-and-band share resting on 13 to 22 interviews (asserted) | the plan's annex ("each estimated for the division and band as a whole") |

## Ladder

| Rung | Construction | Caseworkers (Northern, Lakeshore, River Valley, High Plains, Central, Southern Hills, Southwest, North Metro, South Metro) | Total |
|---|---|---|---|
| R0 | the two surveys' shares multiplied in each division and band (the default path) | 2, 2, 3, 3, 3, 2, 4, 4, 3 | 26 |
| R0b | the same with each division's bands pooled | 2, 2, 3, 2, 3, 2, 4, 4, 3 | 25 |
| R1 | the pilot's own share with both traits by band, in every division | 4, 3, 5, 4, 4, 3, 7, 6, 6 | 42 |
| R2a | the energy survey's burden share times the pilot's equipment rate among high-burden screens | 7, 5, 6, 5, 4, 3, 8, 7, 6 | 51 |
| R2b | the health survey's equipment share times the pilot's burden rate among equipment screens | 2, 2, 3, 3, 4, 2, 6, 6, 5 | 33 |
| R2c | the product scaled by the pilot's dependence ratio | 3, 3, 5, 4, 5, 3, 7, 6, 5 | 41 |
| R3 | the pilot's band table raked to each cell's two shares (golden; a Mantel-Haenszel odds ratio, each pilot division's own odds ratio, the bands' pooled odds ratio and the pilot's equipment rate ratio alike) | 2, 3, 4, 4, 4, 3, 7, 6, 5 | 38 |

- **Margins:** the golden's division totals sit 99 to 198 households from a caseworker step; every fusion in the R3
  family (eight, each pilot division on its own odds ratio among them) lands within 24 households of the golden in
  every cell and on the same hundred in all 18 cells and nine division totals. R0's division totals sit 58 or more from
  a step.
- **Position and dominance:** R0 counts 8,200 eligible households against 13,300 and undercounts every division by 24
  to 46 per cent, because inside each band the pilot's odds of the equipment are about three and a half times as high
  in high-burden homes (3.49 under $25,000, 3.47 from $25,000 to $49,999; 3.32 to 3.62 in each pilot division and
  band).
- **Grid:** two choices, the association (none or the pilot's) and the shares kept (both surveys', the energy survey's
  only, the health survey's only, none): none and both is R0 (26); the pilot's and both is the golden (38); the
  pilot's and the energy survey's is R2a (51); the pilot's and the health survey's is R2b (33); the pilot's and none
  is R1 (42); the association on the ratio scale is R2c (41); every cell a named wrong answer but one.
- **Worth:** R0 against the golden moves all 18 cells and eight of nine divisions' staffing (Northern alone stays at
  two).
- **Each lower rung breaks the annex in the data:** R1 gives Northern more eligible households than households with
  the equipment in both bands (and Lakeshore under $25,000); R2a does so in six cells; R2c in three; R2b's table holds
  burden shares of 0.43 to 0.45 under $25,000 in every division, five or more points under the energy survey's 0.52
  to 0.81 in the seven divisions outside the pilot.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | territory households with incomes under $50,000 (two bands) in the nine divisions, 2025 | the plan's eligibility and annex (SF1, SF3) |
| 2 | Unit of account | the household | SF5 |
| 3 | Attribution window | the 2025 survey year; the demographer's 1 July 2025 estimates | the plan's annex; the estimates' reference date |
| 4 | As-of dating | the surveys and estimates as released; the division register as it stands for the filing | SF4 |
| 5 | Version basis | one release of each survey; the pilot's latest complete screen per address | SF12 |
| 6 | Denominator | burden: the division and band's energy survey households; equipment: its yes and no answers | SF6, SF8 |
| 7 | Weighting | WT_FINAL and HH_WT; the pilot unweighted (random addresses in its two divisions) | SF8; C1: each pilot division on its own odds ratio, or on its own Mantel-Haenszel ratio, leaves every cell on its hundred (asserted) |
| 8 | Window length | one survey year | the plan's annex |
| 9 | Boundary inclusivity | under $50,000; above 6 per cent | C1, nothing on either edge (SF1) |
| 10 | Rounding path | caseworkers from the unrounded counts; households to the nearest hundred | SF11 |
| 11 | Tie-break | none needed | n/a |
| 12 | Maturity and censoring | the 2025 surveys and the pilot are closed | n/a |
| 13 | Order of operations | conform, take the shares, fuse each division-and-band cell, sum, staff | C1: the raked tables and the closed-form fusion give the same cells (asserted); the cell is the division and band as a whole (SF15) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | the pilot's latest complete screen | SF12 |
| 16 | Identity normalisation | county codes as three-digit text in one survey and integers in the other | the register's codes; every survey county joins (asserted) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | dollars a year; a monthly bill times 12 | SF2 |
| 19 | Code and status semantics | MEDEQUIP 1, 2, 7 and 9; the pilot's screen statuses | SF6, SF13 |
| 20 | Integerisation | caseworkers rounded up in each division | SF10 |
| 21 | Clause scope | the standard applies to every division alike | the plan's staffing section |
| 22 | Forward window contents | 2027 staffing on the 2025 eligible households | the plan's annex ("the latest survey year") |

## Literal reader

Executed word for word, the plan defines eligible households (income under $50,000, annual home energy costs above 6
per cent of income, someone relying on electrically powered medical equipment at home), asks for a conformed table by
division and income band that agrees with the demographer's households and with each survey's weighted estimates, and
staffs one caseworker for every 400 eligible households in a division, or part of that number. The text leaves open how
the joint of the two traits is built when no large survey measured both. Independence satisfies every filed sentence
and files 26, and the pilot's tables reject it inside both bands and in both pilot divisions (the equipment in 10.7 and
11.7 per cent of high-burden screens against 3.3 and 3.7 per cent of the rest). The pilot's own shares, one survey's
share times the pilot's conditional rate and the dependence ratio break the annex in the data (a division with more
eligible households than households with the equipment, or burden shares the energy survey does not hold). Every fusion
that keeps both surveys' shares and carries the pilot's within-band association (its band tables raked, a
Mantel-Haenszel odds ratio, each pilot division's own odds ratio, the bands' pooled odds ratio, the equipment rate
ratio) files 38, with all 18
cells and nine division totals on the same hundred.

## Oracles

None ties only under the golden. The demographer's region and state totals tie under every reading (they sum its county
rows); the surveys publish no division estimates; the pilot report's counts of screens by status and mode count the
screens as returned, whatever the handling. The energy assistance applications and the heat vulnerability index are
distractors that confirm nothing.

## Ask sheet

- **Ask A, each division's households on the medical baseline rate at the end of October 2026 (9 figures, whole
  households).** H18 home: the programme's current caseload beside each division's eligible households, a measure every
  division carries that the staffing does not turn on. Path: the enrolment extract (spell, account, prior account,
  premise, service county, stored division, start and end dates), the division register and the data dictionary (three
  files, nine columns). Primary device: D7, the true key elsewhere: a move inside the territory opens a new account with
  the rate transferred (the new spell names the old account), and the customer usually starts service at the new home
  before stopping it at the old one, so on 31 October some households have both accounts on the rate; counting spells
  or accounts counts them twice; every division has three or more (asserted). Hazard H1: the stored division of
  accounts opened in Kestrelmere before 1 July 2026 reads Central. Hazard H3: the extract ran on 3 November, so the
  spells open in it are not the households on the rate on 31 October. Stops (asserted): open accounts by the register
  (the cracker) +3 to +11 in every division; open accounts by the stored division, Central +625 and Southwest -611;
  spells open at the extract +1 to +12 in every division; households by the stored division, Central +620 and
  Southwest -620; the golden 821 to 3,500 a division. Realism: a billing system keys on accounts, and a customer moving
  house holds two for a few weeks.
- **Ask B, each division's households given a backup battery from January to October 2026 (9 figures, whole
  households).** H18 home: the 2026 workload the caseworkers carried, beside the staffing. Path: the battery work orders
  (order, account, premise, service county, booked date, status, completion time in UTC, unit serial, removed serial),
  the enrolment extract's prior accounts, the register and the dictionary (four files, ten columns). Primary device:
  D1, one household under two keys: a failed unit replaced at the same account (a second completed order, a new serial,
  the old one removed) and a unit re-installed after a move inside the territory (a second completed order under the
  new account, the same serial); counting orders counts both twice, counting accounts the relocations, counting
  serials the exchanges; only the enrolment extract's account chain joins every pair. Hazard H2: completion times in
  UTC: every division has an order finished after 7 p.m. on Saturday 31 October 2026 (1 November in UTC), and three
  finished after 6 p.m. on 31 December 2025 (January in UTC), each of those three with a second late finish on 31
  October. Hazard H4: a booked date in place of the completion (a few
  visits finished one to three days late across the window's ends). Texture: cancelled and no-access orders. Stops
  (asserted): distinct accounts on Central Time (the cracker) +5 to +25 in every division; distinct serials +3 to +34;
  completed orders on UTC dates +11 to +56; households on UTC dates move all nine divisions by one or two; the golden
  161 to 641 a division. Realism: a field crew's handheld stamps UTC, and units are swapped and moved with their households.
- **The construction layer:** each division's eligible households and caseworkers, the eighteen cells of the conformed
  table and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the main call reads no enrolment, battery or distractor row (the call
  and every rung computed with those files deleted are identical); the asks read no survey, pilot or estimates row
  (both asks computed with those files deleted are identical); the register is shared and carries no device row.
- **Hazard table (asserted):** H1 moves Central and Southwest in Ask A; H3 every division in Ask A; H2 all nine
  divisions in Ask B; H4 three divisions in Ask B.
- **Referee:** none; no total in an ask file ties only under one handling.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, households on the medical baseline rate at the end of October 2026 by division | counts distinct accounts with a spell open on 31 October, each by its service county through the register; a transferred household's two accounts both counted | miss |
| B, households given a backup battery from January to October 2026 by division | counts distinct accounts with a completed order in Central Time, through the register; a relocated household's two accounts both counted | miss |

- Mirror leakage: about 10 per cent of ask weight (a response on R0 keeps the two files; it misses every Ask A and Ask B
  figure on the same devices as the cracker).
- Pair ceiling: 34.0 (planning weights 38 / 7 / 55 with the call, each division's eligible households and caseworkers,
  the eighteen cells and the chart in the main block and r = 5; the ask weight over 20 criteria: A 9, B 9, the two
  files 2; the cracker keeps the files, 2 of 20, 38 + 7 + 5.5 = 50.5; the mirror keeps r, instruction-following and the
  files, 5 + 7 + 5.5 = 17.5; average 34.0), rerun from the generated rubric at ship.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| Electricity as a typical monthly bill for some respondents | the energy survey's questionnaire | energy survey file | the monthly bill taken as the year's | call unchanged |
| A base and a final weight | the energy survey's weighting | energy survey file | the base weight | call unchanged |
| County codes as three-digit text and as integers, with public health districts | the two agencies' frames | both survey files | an unpadded join | call unchanged (loud: counties drop) |
| Eight income categories against four bands | the health survey's questionnaire | health survey file | none likely; the categories nest | call unchanged |
| Don't-know and refused codes | the health survey's questionnaire | health survey file | counted as no | call unchanged |
| An address screened by mail and by telephone | the screening system | pilot file | both screens kept | call unchanged |
| Partial screens and don't-know answers | the screening system | pilot file | counted as no | call unchanged |
| Region subtotals and a state total among the county rows | the demographer's release | estimates workbook | summed with the counties | call unchanged (loud) |
| Counties outside the territory | the state surveys and the demographer | surveys, estimates | kept | call unchanged (no division) |

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each division's count of households
  carrying two traits that no large survey measured together, built the way data-integration statisticians build it
  (each survey's weighted division-and-band share, the auxiliary sample's within-band association carried into tables
  that keep both shares); multiplying the shares staffs 26, the pilot's own shares 42, the conditional imputations 51 and
  33, the dependence ratio 41. Two layers: the Layer 1 inventory above, each item asserted neutral on the call (R2 and
  SF2, SF6, SF8, SF12, SF13), each ask device confined to its ask with zero main-call rows (the separation checks); Layer
  2 the fusion beyond independence. The decisive step is none of the three banned kinds, each executed in `checks.py`:
  not a plant (R3c: no document names independence, an odds ratio, raking, association or fusion; the pilot report
  counts screens only; no repeated survey record); not data semantics (R2 and SF1 to SF14: every field read right still
  leaves the default path on 26); not rule application (R3a: every filed rule executed with the shares multiplied on the
  clean truth files 26, and the independence table keeps every filed sentence; R3b: only the pilot's within-band
  association with both shares kept files 38).
- **Gates.** 15 files in 3 formats (csv, pdf, xlsx); medical_baseline_enrolment_2026.csv at 38,848 rows; two distractors
  (the heat vulnerability index and the energy assistance applications) the solution never reads; 88 generator checks; `verify.py`
  (10 checks) from the bundle alone; two builds byte-identical; `figures_check.py`, `precut.py` (49) and `voice-check.py` exit 0;
  `leak.py` REVIEW (no LEAK); guard heart WARN (answered in the draw); the containers clean (H1 audit). The surface
  screen promotes nine card-level pairs for the author's read, none on the pack's surface: task464 and task450 (the
  population gap), task136 (the capacity-report artifact), task233, task256 and task262 (the same-driver signature, each
  differentiated on the card), task134 and task146 (the same-puzzle signature, differentiated). The persona screen's
  "Metro Mail" is a table cell of the pilot report (a division and a contact mode), not a person; the metropolitan
  divisions were renamed North Metro and South Metro so no division reads as a name, the dictionary's and register's
  column sets were renamed after the screen matched them to task453's and task501's, and "Upper Valley" became River
  Valley after the guard matched it to task233's invented names.

## Leak check

`leak.py --asof 2026-11-16`: REVIEW, no LEAK. The band labels ($25,000, $49,999, $50,000) and the caseload (400) are
stated inputs (`metadata.json`); each REVIEW line answered:
- The pilot report carries 10,800 and 21,600 (the addresses mailed), which contain 800 and 600. Harmless.
- The plan, the technical notes and the pilot report carry survey, household, equipment, utility, health, estimates,
  county, sample and screens: a programme plan's, a survey note's and an operations report's own vocabulary; none names
  independence, an association, an odds ratio, raking or fusion (asserted in R3c). Harmless.
- The pilot report names the two pilot divisions beside its screen counts, the enrolment extract names divisions in its
  stored column, and the register names every division: none ranks the divisions on caseworkers or eligible households.
  Harmless.
- A mid-stage LEAK, fixed: after the pilot was redrawn its report counted 1,100 screens ended at the income question in
  one row, the same number as two graded hundreds; the centring now keeps every graded figure off the report's counts
  (asserted in R3c: no graded figure of four digits or more appears in a document).

Reader, three rounds (answers and rulings in `leak_check_report.md`). Round 1: nothing quoted for question 1 and no
ranking file; the reader's literal computation was the default path (26) and it called the call rule application
because the annex read as a recipe; the annex was reworded as the Commission's consistency check, the dictionary's
folder row removed and six realism tells fixed in the generator. Round 2, on the rebuilt pack: the same reading (26,
"the plan prescribes the cell product"), while the reader also wrote that the text files neither the pooling level nor
the independence of the two shares; ruled the stump at work, not a filed rule (the annex fixes what the table must
agree with, which the product and the fused table both satisfy, and the judge's Gate H reads the decisive step as
analytical in both rounds); its realism tells were coincidences or the fiction's design (three work orders 13 apart
among 3,917 with gaps of 1 to 214, the first day of mail returns, the federal county coding, the pilot's sample
design). Round 3, after the estimation-domain pin (SF15), the only document changed after the re-judge: nothing
quoted for question 1, no ranking file, the literal text fixing everything but the joint, and question 6 analytical
(how to build the joint from two separately estimated shares); its one realism fix, the work orders' first record
numbers 13 apart, redrawn with nothing graded moving.

Judge: round 1 DETERMINISTIC, FIX_NOW (each pilot division on its own odds ratio moved North Metro's $25,000 to
$49,999 cell and total to the next hundred); fixed in the data, the pilot redrawn and every fusion that keeps both
shares held on the golden's hundreds by the centring (C1). Re-judge DETERMINISTIC, APPROVE, Gate H analytical; its
residual note, a county-by-band fusion moving two graded hundreds with the staffing unchanged, is closed by the annex's
estimation domain (SF15), a document-only change: every other shipped file but the work orders (record numbers
redrawn) is byte-identical to the judged pack, and every graded figure, golden and the submission are unchanged.

## Tried and rejected

- A rainfall index on cooperative-observer gauges with dormant seasons rebuilt from the airport, the decisive move
  averaging the kinked payout over the rebuilding's error: the expectation-of-a-nonlinear-payout lesson is already
  task151's (a stepped payout over the season total's distribution), task187's and task229's; superseded before any
  data was cut.
- A district index averaged over a network that grew from three gauges to seven: the variance of a three-gauge mean
  exceeds a seven-gauge mean's by only 5 to 15 per cent at the region's inter-gauge correlations, and in a prototype the
  burn's sampling noise swamped it in half the draws; no stable call.
- Station breaks (a gauge moved, an instrument changed): the change found in a unit's own record is task464's spent
  architecture.
- Carrying a short gauge record through a long airport record by the overlap's ratio: task461's driver.
- Withholding framed as a disclosure rule (fewer than three farms, to protect individual operations): a confidentiality
  rule needs complementary suppression, which would stop the single-county subtraction and make the design read as a
  leak engineered for the solver; re-framed as the service's publication standard for reliability (fewer than five
  reports or a coefficient of variation above 30 per cent), which needs none (stage 2, 2026-10-17).
- Two sandy counties in two districts with a golden buying both their covers (the drawn calibration): a reading of
  every withheld mark as a total crop failure buys the same pair, and with the other three counties' calls the same on
  every route the grid left a wrong call four of five covers right; re-laid at stage 2 with four sandy counties in four
  districts, three bought on recovery, one (Tresham) dear even with its years back so the total-failure reading files
  another set, and Corvin, with every year published, dear on every route.
- Re-rooting the decisive step on the same world was weighed at stage 2 and dropped: carrying past shortfalls forward
  in proportion to the trend level (a regression diagnostic, not this task type's analysis, and additive against
  proportional reads as a convention to a literal judge); allocating district counts by an ancillary density, a stop-loss
  layer's leveraged trend and pooled medians against averaged ones (each a weaker default path in another world).
- Architecture 1, the withheld drought years recovered from the district totals as the decisive step (selection on the
  outcome): judge SEND_BACK at stage 4 (2026-10-17), Gate H `decisive_step: rule_application`. The recovery is an
  identity the methods note files (2.1), and with the cells restored the call is the policy's filed formula, so the
  stump sat in Layer 1 (suppressed cells) and the term sheet's filed additive rating basis left no estimation choice.
  The world, the pack and the recovery stay usable as Layer 1 cleaning for architecture 2.
- Architecture 2 candidates on the area-yield world, weighed at the re-root and dropped: past shortfalls scaled with
  the trend level (heteroscedastic burn), the transport-scale lesson task233 and task258 already teach; a trend that
  plateaued, chosen out of sample (every plateau-aware fit gives a different expected loss, no unique figure); the
  expected loss conditioned on the La Nina outlook or on the 2026 drought (the conditional and unconditional estimands
  both defensible on the policy's wording); credibility weighting toward the district (only by filing the method);
  monthly series benchmarked to annual totals in a new world (the extrapolation turns on an assumed ratio path).
- The fused-survey card first checked without a registration stamp: the guard sorted it before every card drawn the
  same day and compared it with the wrong batch (G14 against task233, G16 against task463); stamped, the honest G14
  signature is clear of the batch and differentiated against the older builds that share it.
- A caseload of one caseworker for every 1,200 eligible households (the first calibration): with one to three
  caseworkers a division, the pilot's own shares and the health survey's conditional imputation matched the golden in
  eight of nine divisions; 400 makes every rung a different staffing.
- A pilot drawn across the whole territory: its own shares by band landed the golden total; the pilot now runs in the
  two metropolitan divisions, as a utility's first test of a screener would, so its shares describe two divisions only.
- Eligibility in all four income bands: above $50,000 the pilot's tables held a handful of homes with both traits, so
  band-specific and pooled odds ratios split; the plan's income limit keeps the two bands where the pilot is deep.
- A person weight beside the household weight in the health survey: weighting the equipment item by adults moved two
  divisions' staffing (R2), so the household file ships the household weight only.
- The territory total of eligible households as a graded figure: the R3 family's totals span 114 households, so the
  total cannot sit inside one hundred under every fusion; the prompt asks for the total caseworkers, and the workbook's
  eligible total is the sum of the divisions' figures.
- Filing the pilot's odds ratio as pooled over its two divisions (the round-1 judge's suggested fix for the North Metro
  cell): it files how the association is estimated, the method, and points at the pilot as the source; rejected for a
  data fix (stage 4, 2026-10-17).
- The pilot's first draw: its two divisions' odds ratios (North Metro 3.47 and 3.63 against South Metro 2.75 and 2.95)
  differed enough that each division's own odds ratio moved North Metro's $25,000 to $49,999 cell and total to the next
  hundred; the pilot was redrawn until its divisions agree within sampling error (3.32 to 3.62 against 3.49 and 3.47
  by band), and the call moved from 37 to 38 caseworkers.
