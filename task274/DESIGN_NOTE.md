# task274 design note

Architecture 1, drawn 2026-10-23 (wave 5, Descriptive lane, sathay3012) from seed DA24's quantity only, a count read off a distribution against a fixed limit; the seed's affordability world was screened and holds no unspent analytical step (Tried and rejected), so the world is redrawn. Kestrin Valley Electric Cooperative, a member-owned rural electric cooperative whose lines were energized from 1938, sizes the first full groundline inspection under the board's 2024 pole policy: every wood distribution pole fifty or older in a calendar year (a pole's age being the year less the year it was set) is excavated, sounded and bored in that year, and the 2027 contract is let on the number of those poles on the register of 30 September 2026. Poles set since the 1987 conversion to continuing property records carry the year of the work order that set them; poles set before carry a year only where an inspector of the 2016 to 2025 groundline cycle could read the brand, and about one pole in nine on the register carries none. The plant ledger holds the poles added, retired and in service each year from 1938, and since the conversion the pre-1987 poles' retirements as one count a year, no year of setting attached.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task274.json`, architecture v1. `guard.py check`: WARN only, no BLOCK. `people.first` (Kendra, task186; Alexis, task457; Christopher, task450; Paige, task474): drawn by `guard.py names --geo us --seed 274`, each a single older use; Natalie (a recent use) and Michael were swapped for Paige and Chelsea from the same draw. `repeat.gate_g` (method_or_model_selection, task482 v7): two ways of dating the poles with no year stand, spreading them like the read brands and rebuilding each year's survivors, and the ledger's own balances select the second, which is the vocabulary's definition. `repeat.deliverables` (xlsx and png, task170): a count with its components and a district table is a workbook and one chart. Nearest driver 0.09 (task243, the share of exits a register records, read by growth balance: a different quantity). `slots` on the mechanism's words (vintage, survivor, additions, retirements, ledger, brand) and the setting's (pole, cooperative, groundline): no screen rebuilds lost entry years from intake through a survival curve (task133 counts a takeover's exposure from the takeover, task129 set aside a cable-failure draw on survivors, task265 corrects a left-truncated register). The first pole card (general statistics, an investor-owned utility, shape 04) was blocked by the window as it stood then; the organisation (a cooperative) and the shape were redrawn, and the shape is now 07, the asks' district grid.
2. Pairing: General Statistics & Data Science / `missing-data-censoring-measurement-error` / Descriptive & Distribution Analysis. One pole in nine has no year of setting and the missing years are the old ones (brands fade); the age distribution is recovered by a stock-flow construction, each year's survivors its additions times a survivor curve fitted to the ledger's year-end balances, the poles with no year spread over what that leaves. The setting is a utility's plant; the statistical object is a distribution whose values are missing not at random, recovered through a survival model fitted to aggregate counts.
3. Niche: a rural electric cooperative's 2027 full groundline inspection, sized by how many wood poles will be fifty or older, when about one pole in nine carries no year of setting.
4. Objective: Descriptive & Distribution Analysis: how the cooperative's poles in service are distributed by year set, read at 1977. The call faces forward (the 2027 contract); it is today's poles' years read against 2027, not a value the history pins about the future.
5. Shape 07 (grid of cells): the count, three register components, and four figures for each of the four districts on the cycle's rejected poles; arithmetic in `## Ask sheet`.
6. Decision type quantity_figure; answer unit count; question form how-many. Forum: the board of directors, which approves the 2027 work plan on 17 November 2026; forcing event: the lender's operations and maintenance review in March 2027 (audit_or_inspection); organisation: cooperative_or_member_body; stakeholder: the manager of system maintenance (operations_director); context artifact: the inspection contractor's close-out of the 2016 to 2025 cycle (close_out_summary).
7. Deliverables: `pole_inspection_2027.xlsx` (the count, the register's figures, the reconstruction, the rejected poles by district) and `pole_inspection_2027.png` (the poles in service by year set, the poles with no year shown as estimated, the line at 1977).
8. People, drawn with `guard.py names --geo us --seed 274`: Kendra Dennis (manager of system maintenance, the memo's author), Alexis Camacho (general manager), Becky Mcmillan (mapping and records), Chelsea Ross (office manager in 1987), Regina Mcdaniel (manager in 1987), Christopher Riggs (the contractor's project manager), Tara Gilbert (the telephone company), Paige Gibbs (general manager in 2015). Invented names are screened in `checks.py` (H21).

## Default path

1. Read the policy and the memo: the count is the cooperative's distribution poles on the register of 30 September 2026 set in 1977 or earlier.
2. Read the register: 231,103 distribution poles; 177,975 carry the year of the work order that set them (1987 or later); 53,128 were set before 1987, and of those 27,543 carry a year read from the brand and 25,585 none.
3. Spread the poles with no year over 1938 to 1986 like the pre-1987 poles whose brand was read.
4. Count the poles set in 1977 or earlier.

Ends on: about 26,000 poles fifty or older (spread like the read brands). The careful variants land elsewhere: spreading the poles with no year in proportion to each year's additions files about 35,300; a two-parameter Weibull survivor curve fitted to the ledger's balances files about 34,400 and fitted to its yearly retirements about 33,800 (a lognormal, log-logistic or gamma curve 34,200 to 35,600); the poles spread by each year's survivors without the read brands taken off files about 29,300; the ledger's own oldest-first convention files about 26,900.

Golden: 33,000 poles fifty or older to the nearest thousand (32,771): each pre-1987 year's poles still standing rebuilt as its additions times a Makeham-Weibull survivor curve fitted by least squares to the ledger's year-end balances, 1938 to 2025, less that year's read brands, the poles with no year spread over the remainder.

## Stump sentence

A competent analyst who parses every brand and reads every account spreads the poles with no year of setting like the pre-1987 poles whose brand was read and files about 26,000 poles fifty or older (or, spreading them by each year's additions, about 35,300); brands fade with age, so the poles with no year are the oldest, and each year's survivors are its additions thinned by decades of retirements that climb after forty years, so only a survivor curve fitted to the ledger's balances, flexible enough to carry both the steady early losses and the late wear-out, applied to each year's additions, says how many poles of each age still stand (33,000). Data-native: the ledger's additions and year-end balances from 1938 fit the curve, and the read brands, thinning toward the oldest years against those additions, show the poles with no year are the old ones.

## Three rules

- Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), which serves Descriptive & Distribution Analysis: the call is a count read off the poles' distribution by year set, with the year missing not at random for one pole in nine.
- Domain test: the quantity that decides the call is the number of the cooperative's distribution poles in service set in 1977 or earlier; the field's estimator for a distribution whose values are missing not at random while the population's inflows and stock are recorded in aggregate is a stock-flow reconstruction, each year's survivors its additions times a survivor curve fitted by least squares to the recorded stock, the missing values spread over what that leaves; the recorded years' own distribution in its place moves the count by thousands.
- Swap: "how many of the bank's savings accounts opened in 1977 or earlier are still open" keeps the words and loses the step: accounts close at a rate that does not climb with age, so each year's openings in proportion already give the survivors' shape; the step exists because wood decays at the groundline and poles come out ever faster after forty years, which only the ledger's balances show.
- Layer 1: a register from the mapping system (years from work orders since 1987, brands typed as they read, in two or four digits, month and year, or with supplier and treatment codes, blanks for the rest); a ledger typed up from the books at the conversion beside a property system's records since; retirements booked when the work order closes, so the accounts and the register differ by the open orders; streetlight-only poles on the register; two districts merged in 2019 with old codes on records nobody has edited since. All of it is the cooperative's own record keeping; nothing is placed to be caught.
- Layer 2: estimation_fit (survivorship): the poles still standing from each year are a survivorship product, and the choice that flips the count is fitting a survivor curve to the ledger's balances and spreading the poles with no year by what each year's additions leave, rather than like the read brands, by additions, oldest first, or on a curve too rigid to follow the ledger.
- Decisive step: rebuild the surviving poles of each pre-conversion year as its additions times the survivor curve the ledger's year-end balances fit (the depreciation profession's simulated plant-record method), and spread the poles with no year over that remainder after the read brands.
- Not semantics: reading every field right (each brand parsed, the streetlight poles left out, the open orders reconciled) still leaves 25,585 poles with no year and no field that says how old they are; spreading them like the read brands is a correct reading that files about 26,000.
- Not rule application: no filed rule says how to date a pole with no year; the policy fixes the population, the date and the age (the year less the year set) and nothing else. The standing family (Makeham-Weibull, Gompertz-Makeham, Gompertz, generalised gamma and a constant hazard with a lognormal, log-logistic or gamma wear-out, each fitted to the balances and to the yearly retirements, a year's poles dated mid-year or at its start, the survivors read at the register's date, at 1 January 2027 or at the ledger's last year end, and piecewise hazards) runs 32,659 to 33,291 and prints 33,000, while the Weibull, lognormal, log-logistic and gamma curves, which fit the balances 990 to 2,926 times and the yearly retirements 9.7 to 31.7 times worse than the Makeham-Weibull, print 34,000 to 36,000; the ruling-out is quiet, since nothing says the brands fade or that the oldest poles lack years, and the read brands against the additions show it only to an analyst who sets them side by side.
- Analyst test: the easy route, the poles with no year spread like the pre-1987 poles whose brand was read, files about 26,000 poles fifty or older against the golden 33,000; spreading them by additions files about 35,300.
- Estimand: the number of the cooperative's distribution poles on the register of 30 September 2026 set in 1977 or earlier (fifty or older in 2027), filed in the board's Policy 302 (4.1, 4.2) and the 2027 work plan memo.
- No decoy: nothing is planted: the contractor's close-out reports the cycle's findings, not ages; the plant accounts are the cooperative's own records; no memo, draft or staff figure argues a count.
- No certified replay: no published or certified figure reproduces the reconstruction; the accounts publish no age profile and no average age, and the method is not recovered by matching a filed number.
- Lesson: when the oldest members of a population have lost their entry dates, the age distribution is rebuilt from the entries by year through a survival curve fitted to the recorded stock, with a form flexible enough to follow it; no build on file rebuilds lost entry years (task133 counts a takeover's exposure, task243 measures exit recording, task265 corrects a left-truncated register).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the read brands alone | none (the policy counts every pole) | BRAND parses to a year | count what the data say | none | none | a filter | readable |
| R1 (the default path) the poles with no year spread like the read brands | none | BRAND and the blanks | proportional imputation over the observed distribution | none | none | one ratio a year | readable |
| R3 spread by each year's additions | none | the ledger's additions | allocate by intake | none | none | one ratio a year | readable |
| R5 a two-parameter survivor curve fitted to the ledger | none | the ledger's balances | a Weibull or lognormal life | none | none | a fit | readable |
| (decisive) R7 each year's additions on a survivor curve the ledger's balances fit, flexible enough to follow them, the poles with no year spread over what that leaves after the read brands | none: the policy fixes the population and the age and says nothing of how to date a pole with no year; the conversion memo says the ledger never recorded which pole was set in which year | no column holds a pole's estimated year; the survivors need the ledger's 88 year-end balances fitted against 49 years of additions | none: the reflexes for a missing value (drop it, impute from the observed, spread by intake) each leave the brands' fading in the answer; a two-parameter life curve leaves the early losses and the wear-out unfitted | none: no shipped figure ties under either reading | none: the battery passes on the records as written | a fit over 88 balances, once the selection is seen | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a year's poles' age | set mid-year | set at the start of the year | the same count | same call |
| SF2 | the date the survivors are read | the register's date, 30 September 2026 | 1 January 2027 | the same count | same call |
| SF3 | the date the survivors are read | the register's date | the ledger's last year end, 31 December 2025 | the same count | same call |
| SF4 | distribution poles | POLE_USE DIST | streetlight-only poles counted too | the same count: none was set by 1977 | Policy 302, 2.2; same call |
| SF5 | the ledger series the curve is fitted to | the year-end balances | the yearly retirements | the same count | same call |
| SF6 | fifty or older in 2027 | set in 1977 or earlier | set in 1976 or earlier | another count | Policy 302, 4.2: the age is the year less the year set |
| SF7 | within twelve months | on or before the inspection's first anniversary | within 365 days | the same figures | same call (no completion within three days of the anniversary) |
| SF8 | out of service | the completion of the work order that replaced the pole or retired its line | the pole's own date | the same figures | Policy 302, 5.2 |
| SF9 | on 30 September 2026 | completions on or before that date | completions to the extract's date | the same figures: none falls on the date, and the ask says by that date | the asking sentence |

## Ladder

| Rung | Construction | Count | What kills it |
|---|---|---|---|
| R0 | the poles whose brand gives 1977 or earlier | 13,495 | the 25,585 poles with no year are poles too |
| R1 | the poles with no year spread like the read brands | about 26,000 | brands fade: on the world's own poles the brand was read on 69 per cent of those set from 1978 to 1986, 37 per cent of 1958 to 1967 and 7 per cent of 1938 to 1947; in the pack, read brands per hundred poles added fall from 46 to 10 to 0.2 over the same years, so the poles with no year are the old ones |
| R2 | the ledger's retirements taken from the oldest additions first | about 26,900 | the 1950s' poles still stand on the register long after an oldest-first ledger would have retired them |
| R6 | spread by each year's survivors on the curve, the read brands not taken off | about 29,300 | the read brands are already among the survivors |
| R5 | a Weibull, lognormal, log-logistic or gamma curve | 33,757 to 35,573 | its error on the ledger is 990 to 2,926 times the Makeham-Weibull's on the balances and 9.7 to 31.7 times on the yearly retirements: it cannot carry the steady early losses and the wear-out together (the Weibull is the Makeham-Weibull with no constant hazard) |
| R3 | spread by each year's additions | about 35,300 | decades of retirements have thinned the oldest years |
| R7 (golden) | the curve the balances fit, the poles with no year spread over what it leaves after the read brands | 33,000 (32,771) | |

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the cooperative's distribution poles on the register of 30 September 2026 (Policy 302, 2.1 and 2.2; the memo); streetlight-only poles out, none set by 1977 (SF4) |
| 2 | Unit of account | a pole; the register is one row a pole |
| 3 | Attribution window | the year a pole was set, 1977 or earlier (4.2) |
| 4 | As-of dating | the register's date; the survivors read then, at 1 January 2027 or at the ledger's last year end give the same count (SF2, SF3) |
| 5 | Version basis | one register, one ledger; no revision |
| 6 | Denominator | none: a count |
| 7 | Weighting | each year's survivors weight the spread; the family converges (checks F rows) |
| 8 | Window length | the ledger's whole history, 1938 to 2025 |
| 9 | Boundary inclusivity | 1977 in (4.2) |
| 10 | Rounding path | the count to the nearest thousand, once; the golden 271 from its cell's edge, the whole family 159 |
| 11 | Tie-break | none |
| 12 | Maturity and censoring | the ledger closes at 2025; the register's date is the count's date (SF3) |
| 13 | Order of operations | survivors, then the read brands taken off, then the spread (R6 is the wrong order) |
| 14 | Row order | none: sums |
| 15 | Duplicate resolution | register locations unique (asserted) |
| 16 | Identity normalisation | none for the call |
| 17 | Netting against gross | none |
| 18 | Dimensional units | the ledger is in units of poles (its Notes sheet); no dollars ship |
| 19 | Code and status semantics | POLE_USE DIST and SL in the dictionary (SF4); never the stump |
| 20 | Integerisation | the spread is fractional, the count is rounded to the thousand |
| 21 | Clause scope | 4.1 to 4.3 scope the count; 5.1 and 5.2 the asks |
| 22 | Forward window contents | poles set after the register's date cannot be fifty in 2027 (the memo) |

## Literal reader

Executed word for word, Policy 302 and the memo file the cooperative's distribution poles on the 30 September 2026 register set in 1977 or earlier. The register gives a year for 205,518 of its 231,103 distribution poles and none for 25,585, all set before 1987; the literal estimand still counts those, and no file says how old any of them is. The ledger's additions by year and its year-end balances from 1938 to 2025 fix how many poles of each year still stand only through a survivor curve fitted to the balances; every form that fits them (Makeham-Weibull, Gompertz-Makeham, Gompertz, generalised gamma, a constant hazard with a lognormal, log-logistic or gamma wear-out, each to the balances or the yearly retirements, a year's poles dated mid-year or at the start, read at the register's date, 1 January 2027 or the ledger's last year end, and piecewise hazards over ten- and five-year ages) prints 33,000 (32,659 to 33,291), and the Weibull, lognormal, log-logistic and gamma curves, whose error is 9.7 to 2,926 times the Makeham-Weibull's on the same target, print 34,000 to 36,000 (`checks.py` F rows). The world's own count prints 33,000.

## Oracles

No shipped figure states a pole's estimated year, an age profile, an average age or a count of old poles. The close-out's season table counts poles inspected, treated and rejected, and ties under every reading of the asks (the asks' devices change no reject). The ledger's balances are the curve's input, read the same way by every route; no control total ties only under the golden or only under the easy route.

## Ask sheet

The asks are decoupled from the call: they read the cycle's inspection results, the work orders and the district codes, which the call never opens, and the register only at locations whose pole was set since 2016 (the separation assertion); the call is unchanged with those files deleted. Each is a district's record of the cycle's rejected poles, the second thing the lender's review reads beside the count under Policy 302 section 5, and none turns on a pole's age.

**Ask A. For each of the four districts, how many of the poles the 2016 to 2025 cycle rejected were out of service within twelve months of their inspection, how many later but by 30 September 2026, and how many were still in service on that date (12 figures).** Primary (silent, D6 a paper row covering several ledger lines): the work order extract is one row a work order, raised against one location, and a replacement crew often clears several rejects on one feeder in one order (POLES_SET above one); the rejects after the first are found only through the register, whose WORK_ORDER names the order that set the pole now standing at each location. Joining the rejects to the extract on location, the habitual route, finds the first reject of each such order and leaves the rest looking unreplaced; the key is unique, nothing is an exact duplicate and an unmatched reject is what a backlog looks like, so the battery passes. Hazards: orders raised twice and cancelled; replacement orders still open; feeders renumbered at the 2019 merger.

**Ask B. For each of the four districts, how many of the poles the cycle rejected were still in the ground on 30 September 2026 (4 figures).** Primary (silent, a domain effect: a replaced pole that carried the telephone company's cable stays in the ground beside the new one until the cable is moved, and a removal order, raised at the location after the replacement, pulls it): the replacement order's completion takes the pole out of service and not out of the ground, so a response that equates the two files the still-in-service figures here. Shared hazard: the D6 grain of Ask A.

**Separation.** Zero device rows reach the call: the multi-pole orders and the removal orders sit in the work order extract, which the call never reads; the register rows the asks read past the location are poles set since 2016, outside the call's population (asserted).

**Cracker sheet.** The response that landed the call, ran the hygiene battery (key uniqueness on each file, exact duplicates, unmatched joins) and executed every filed rule its path points at (Policy 302, 5.1 and 5.2):

| Ask row | What the cracker does | Against the golden | Cracker |
|---|---|---|---|
| A, out of service within twelve months, four districts | each reject's order found by location | every district off | miss |
| A, out of service later, four districts | the same | every district off | miss |
| A, still in service, four districts | rejects with no order found | every district off | miss |
| B, still in the ground, four districts | the poles still in service | every district off | miss |

**Mirror sheet.** The response on the default path reads the asks as the cracker does (they consume nothing the call's construction produces), so its ask rows miss the same way.

Mirror leakage: 0 per cent of ask weight (every ask row misses for the mirror as for the cracker).

Pair ceiling: 28.5 (the one-cracker case: (38 + 7 + 0 + 5 + 7 + 0) / 2).

Measured by: generator/cracker.py on the cut pack.

## Build record

- Generator: `common`, `world` (positions, pole lifetimes, the cycle's inspections and brand reads, the ledger), `work` (findings, rejects, replacement, removal, retirement and new construction orders), `records` (the register, the inspection results, the work orders, the codes, the ledger, the outages), `docs` (policy, memo, 1987 memo, close-out, dictionary, joint use agreement, the workbooks, the contents), `pack` (the shipped files' readers), `analysis` (the golden, the family, the routes, the asks), `deliver` (the goldens and figures.json), `checks`, `verify` (independent, pandas and least_squares), `cracker`, `writeup`, `postprocess`, `build`. Seed 315.
- Pack: 14 files (CSV, PDF, XLSX, TXT); the register 233,174 rows, the inspection results 222,856, the work orders about 75,000. Distractors (`metadata.json`): the joint use agreement, the outage records and the 2027 unit rates.
- Gates: checks 0 failed, verify agrees on every figure, two builds byte-identical, figures_check 41 of 41, precut 51 checks, voice-check PASS; the workbook and chart opened and read.
- leak.py: REVIEW, every line harmless: the memo, the policy and the dictionary share the call sentence's words because the memo and the policy file the estimand (the register's date, the distribution poles, 1977); no document states 33,000 or any age profile; the vocabulary hits (ledger, cooperative, records, accounts) are the documents' own subjects; the outage file names the protective equipment that opened in EQUIPMENT_OPENED.

## Tried and rejected

- The seed's own mechanism (take-up conditioned on how each customer is reached) and its nearest honest variant, take-up read by distance below the cut in force from two pilot counties at different cuts: both are conditioned yield, G14, which the window held (task273), and the seed's architecture is the withheld-rule-with-decoy form the client bans.
- Enrollment ramping through Year 1 against the pilot's year-end take-up (credit-months against ever-enrolled): one ratio computed straight from the pilot's records, so a reader who reads "credits a month" lands it; and the call becomes a forecast.
- Survey income against verified income (a reporting gap measured on the panel's pilot-county applicants): the noise-variance-from-a-subsample insight task262 spent in this lane, and the verified subsample is selected on the outcome.
- Item imputation for missing income, a bracket-response imputation, raking to billing auxiliaries, small-area shrinkage: each screened on file as a template or rule application (task253's Tried and rejected), and the panel's income is asked in dollars here.
- Heaped incomes at round amounts, spread over their rounding interval: the spread's form forks the count at a whole-step cut.
- The affordability panel carried to the account base as stayers plus in-movers (prototyped, the first draft of this note): in a steady-state base the 2025 cross-section is the 2026 cross-section in distribution, so the panel weighted to today's accounts landed the golden's cut (recent movers 25.3 per cent of the frame, new accounts 25.2 per cent of today's base, panel and golden on one cut); only a turnover shift the world would have to be built to carry moves it, and carrying a survey to a later date is task259's report-ageing ground in the same subdomain.
- The affordability world as a whole: its deciding quantity is a survey-weighted income share whose remaining pitfalls are nonresponse within classes (task253 architecture 1), measurement noise from a subsample (task262), seasonal reference income (task272) or reflex calibration on visible auxiliaries; redrawn.
- The same reconstruction in a housing association's tenancies (start dates lost at a system migration, rebuilt from lettings by year through a curve fitted to the legacy endings), prototyped at 44,000 homes: tenancy endings rise only gently late in life, so spreading by lettings landed within 2 per cent of the truth at middle cutoffs while the golden's own fitted forms spread 3 to 6 per cent at the oldest; the poles' wear-out separates where tenancies do not.
- A coincident peak of a transformer's homes (diversity): task196's driver. Death registration completeness by growth balance: task243's driver. Reach and frequency by a beta-binomial and claim counts by a negative binomial: the latent rate from short windows, task253's ground.
- Five-year age bands beside the count (shape 14, the first pole design): the forms that agree on the count split the oldest band by 5,962 to 6,807, so the bands are not determinate; the main side is the single count.
- A ledger shipped only from the 1986 field count on (the pre-1987 group's balances 1986 to 2025): the forms spread 2.5 per cent (a ten-year piecewise hazard 33,856 against Makeham-Weibull's 33,032 on one world), since nothing before the conversion pins the curve's young ages; the ledger ships its whole history from 1938, as plant ledgers keep it.
- A register carrying a 1900 placeholder for the poles with no year, and the telephone company's poles beside the cooperative's: either mishandled moves the count by thousands, so neither is neutral Layer 1; the placeholder is a blank and the register holds the cooperative's own poles.
- Brands with a digit unread ("5?") on the register: "no year of setting" then reads two ways on a graded component (25,945 or 25,673 on the seed-274 world); every typed brand now gives a year.
- The 2017 to 2026 cycle: a close-out cannot predate the 2026 season's end in November; the cycle is 2016 to 2025, closed out in February 2026.
- The task number's own world (seed 274): the family ran 33,087 to 33,406 read at the register's date and to 33,583 read at the ledger's last year end, across the 33,500 edge; seed 315 keeps every member inside 33,000 with 159 poles to spare (52 worlds scanned, `checks.py` F rows).
- A Sowden Fork district and a Dunmarrow head office: both within two letters of real places (Bowdon, Borden; Marr inside the name), renamed Brackwater and Greythorn (H21).
- Architecture 1, the pre-1987 poles with no year rebuilt from the plant ledger (each year's additions times a survivor curve fitted to the ledger's 1938 to 2025 year-end balances, the poles with no year spread over what the brand-read poles leave): spent 10-23 at stage 4 on Gate F. The isolated scored reader fitted a Makeham-Weibull hazard to the balances by least squares on its own, rebuilt each vintage's survivors from its additions and committed 33,000, the golden, with 14 of 19 ask figures (every within, later and in-service figure but Halvorne's within, off by one; the double-wood device held all four still-in-the-ground figures). The simulated plant record is the depreciation field's textbook method for an unaged account, and a ledger of additions and balances by year invites it, so the reflex is the method and nothing in the data turns the reflex wrong.
