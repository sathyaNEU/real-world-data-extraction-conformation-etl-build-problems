# task486 design note

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

Architecture 3, drawn 2026-10-25, re-rooted fresh after architecture 2 (a linkage unit's pairwise findings resolved into
people) was spent at stage 4 when scored reader A landed the call. The author's rule holds: no retirement, a fresh rebuild.
The draw keeps the lane's objective and moves to survey research and official statistics' census-register task type, the
honest home architecture 2 could not take while task479 held the pairing.

## Draw

| Field | Value |
|---|---|
| Domain and task type | survey-research-official-statistics / census-register-administrative-data-quality (ETL) |
| Objective | Data Extraction & Conformation (ETL): the tax authority's PAYE employer returns, the valuation list's 2017 and 2023 editions, six district councils' ratepayer accounts, the companies register and the town centre postcode lookup conformed into one table of workplace retail employment by designated town centre for March 2022 and March 2026 |
| Niche | an island nation's statistics office placing the PAYE register's employers, each held at its PAYE address, at the premises they occupy in the valuation list, to name the designated town centres whose workplace retail employment fell by 8 per cent or more between March 2022 and March 2026, the eligibility test of the government's 2027 Town Centre Renewal Fund |
| World | Torvasay, a fictional self-governing island nation in the British Isles: six districts (Rookgate, the capital, Dorrstead, Glenskarn, Ingmouth, Neshdale, Skelrigg), 31 designated town centres, the Revenue Office (PAYE), the Valuation Office (the rating list), the district councils (rates billing), Torvasay Statistics, the Department for the Economy (the fund) and the Council of Ministers. An island with one PAYE register and one valuation list holds every employer and every premises, which a sub-national region does not (`## Tried and rejected`) |
| People | Frances Davies (head of economic statistics at Torvasay Statistics, the requester), Stewart Sheppard (the Revenue Office's data-sharing lead), Irene Walters (the Department's fund programme manager); drawn with `guard.py names --geo "United Kingdom" --seed 486` |
| Stakeholder | the head of economic statistics, whose team compiles the island's employment statistics from the PAYE returns and prepares the fund's eligibility schedule (statistical_office_head) |
| Forum, forcing event | the Council of Ministers approves the fund's list of eligible centres at its meeting of 10 December 2026 (minister_or_cabinet, vote_or_meeting) |
| The call | which of the 31 designated town centres meet the fund's test, workplace retail employment (employees of retail employers, SIC 2007 division 47, at the premises they work in) down by 8 per cent or more from March 2022 to March 2026 |
| Decision type, unit | designation_set; a set of centres |
| Shape | 10, a scorecard against a threshold: each centre's workplace retail employment in both Marches, its change and its eligibility, every centre graded |
| Deliverables | `town_centre_fund_2027_eligibility.xlsx` (the schedule, and the asks' tables) and `town_centre_retail_employment_2022_2026.png` (each centre's change against the 8 per cent line) |
| Card | `.claude/skills/fingerprint/cards/task486.json`, architecture v3, registered 2026-10-25, architectures 1 and 2 in its lineage with their fates |
| Guard | the window task269, task303, task166 banned the first furniture (task269's council_or_assembly, budget_or_appropriation, local_government): the island's statistics office compiles and the Council of Ministers approves at a scheduled meeting, which is who would on an island with one register. test.same_puzzle_older and test.same_driver_older (population, G14, designation_set and etl_conformance) differentiated on the card against task233, task273, task280, task458 and task473, none of which places a recorded total at sites. WARN only at the draw: three_rules.strategy_risk (grain_or_unit) and repeat.question_form (which; the call is a set). At stage 3 the heart check BLOCKed ban.strategy and ban.artifact against task137 v2 (grain_or_unit, register), registered in another session three minutes before this card and merged after it; the card now files composition_mix and published_series, the honester labels (`## Tried and rejected`), and heart reads WARN (repeat.question_form only) |
| Nearest drivers | task470 0.09, task267 v0 0.08, task486 v1 0.07, task192 v3 0.07; `slots` on the mechanism's words (employment density, single-site, rateable value, apportion premises staff) and the setting's (head office, PAYE, local unit, valuation list, town centre, distribution centre) found no build that places an employer's staff at its premises; task305 reads the rating list's retail floor area into a spatial-interaction model |

**The decisive step.** The Revenue Office's PAYE returns hold each employer's employees paid in March at its PAYE
address, which for a chain is its head office or its payroll bureau. The valuation list holds each premises' rating
description, floor area and rateable value, and the districts' ratepayer accounts name each premises' occupier, so a
chain's premises are known while its staff are known only in total. Placing each multi-site employer's staff at its
premises by floor area, or by rateable value, is the standard apportionment and the easy route. But a shop holds about
six staff per 100 square metres, a superstore about four, a retail warehouse under one and a half and a distribution
centre about one, and between the two Marches several chains opened retail park units and distribution centres while
closing small town centre shops: a share by floor area moves a chain's staff out of its shops into the sparse premises it
opened, and gives a shop it closed a share far below the staff it had. The densities are measured by the register's
single-site employers, each matched to its one premises, as staff over floor area within each rating class. Each chain's
staff are placed at floor area times its class's density, scaled to the chain's total; nothing in the pack states a
density or names the step.

**Data-native sentence.** A distribution centre a chain opened in 2025 has about eighty times the floor area of one of
its shops and about thirteen times its staff.

**Retrospective count, forward call.** The fund's 2027 round is the forward decision; the quantity it turns on is the
change between two closed Marches, because the Department's prospectus files that change as the eligibility test.

## Default path

1. Conform the Revenue Office's two month-12 extracts (the 2022 layout with one scheme reference, the 2026 layout with
   the reference split into tax office and employer parts and a trading name added) into one table of PAYE schemes with
   their SIC 2007 class and employees paid; keep division 47 and add up each company's schemes.
2. Read the extract specification: a scheme's postcode is its PAYE address (a head office, a payroll bureau or an
   accountant), so find where each retail employer works: its premises in the districts' ratepayer accounts liable and
   occupied at 31 March (by company number where the district records it, by name otherwise, through the companies
   register's previous names), joined to the valuation list entry in force (the 2017 list in 2022, the 2023 list in 2026).
3. Place each employer's employees at its occupied premises: a single-site employer's at its one premises, a multi-site
   employer's in proportion to each premises' floor area, the standard apportionment (rateable value and an equal share
   per premises are the alternatives it weighs and sets aside).
4. Sum the employees placed at premises whose postcode is in each designated centre's schedule, in each March, and take
   the change; a fall of 8 per cent or more qualifies.

Ends on: 19 centres qualify, the golden fifteen without Ravbeck and with Rookgate City Centre, Glenskarn, Neshdale,
Skelrigg and Halmoss.

Golden: 15 centres qualify: Dorrstead, Ingmouth, Fenmoss, Kellgarth, Quengate, Ravthwaite, Molwold, Ravbeck, Molscar,
Vaskhope, Tormoss, Vaskrigg, Quenstead, Ravwold and Tavscar.

Measurements throughout this note are on the cut pack (seed 490), by `generator/checks.py`, `generator/verify.py` and
`generator/ceiling.py`; the stage-2 prototype (seed 488) planned the same world on paper.

## Stump sentence

The default path places each chain's March staff at its premises by floor area and names 19 centres for the 2027 fund,
adding Rookgate City Centre, Glenskarn, Neshdale, Skelrigg and Halmoss and dropping Ravbeck, because chains opened retail
park units and distribution centres between the two Marches, premises that hold a fraction of a shop's staff per square
metre, so a share by floor area moves their staff out of the town centre shops they kept; placed at each premises' floor
area times its description's staffing density as the single-site employers measure it (a shop about 6.3 staff per 100
square metres, a supermarket 4.4, a retail warehouse 1.4, a warehouse 1.0), those five centres fell 5.3 to 6.4 per cent,
Ravbeck fell 10.0, and fifteen qualify.

## Three rules

Task type: Survey Research & Official Statistics, census-register-administrative-data-quality, which serves ETL in the taxonomy.
Domain test: the quantity that decides is each designated centre's workplace retail employment in each March, which register-based business statistics build by placing an employer's payroll at the local units its employees work in; a payroll register records a multi-site employer at its PAYE address, and the field places those staff at the employer's premises by each premises' floor area times the staffing density of its kind, estimated on the employers whose payroll and premises are one to one.
Swap: put megawatt-hours for employees and substations for premises and there is no payroll register holding a multi-site employer at one address, no rating description setting what each kind of premises holds per square metre and no single-site employer to measure it on, so the task stops making sense.
Layer 1: the two PAYE extracts in their own layouts (the 2026 extract splits the scheme reference and adds a trading name), produced by the Revenue Office's extract service; employers whose PAYE address is a payroll bureau or an accountant, as PAYE allows; the 2017 and 2023 valuation lists in their own layouts, shops measured net internal and large stores gross internal, appeals altering values with backdated effect and deleted entries carried with their end dates, as the Valuation Office keeps them; each district's ratepayer accounts in its own billing system's layout, with and without company numbers, trading and previous names, reliefs recorded by code, the empty property relief lapsing after three months, and only accounts with a liability published; a group's property company holding premises its trading company staffs; postcodes recoded between the lists; payroll schemes merged or split between the Marches; nothing is placed to be caught.
Layer 2: estimation_fit, a recorded total placed at the sites that produce it: a payroll held at one address goes to the employer's premises in proportion to the staff each premises is expected to hold, its floor area times its description's staff per square metre measured on the single-site employers, against a share by floor area, rateable value or count, each of which assumes every premises of an employer staffs alike.
Decisive step: placing each multi-site retail employer's March employees at its premises in proportion to floor area times the staff per square metre of the premises' description, that density measured as the ratio of total staff to total floor area of the single-site employers in the same description in the same March.
Not semantics: with every field read correctly (the PAYE address as the scheme's address, each employer matched to its premises through the accounts and the companies register, the list entry in force at each 31 March, net and gross floor areas as listed, the centre schedule's postcodes) the easy route still shares each chain's staff by floor area and names nineteen centres; no field, code, unit or definition read differently moves it.
Not rule application: the prospectus files the estimand (the employees of retail employers paid in the March tax month, counted at the premises where they work, a premises in a centre when its postcode is in the centre's schedule, a fall of 8 per cent or more on unrounded figures) and says nothing on how a multi-site employer's employees are placed; on the cut pack the enumerated family (the PAYE postcode, an equal share per premises, floor area, rateable value on each year's list or on one, the description's mean staff per premises and eight density estimators) files seven different sets, the standing family (the seven estimators: ratio of totals, mean and median of ratios, single-site employers of every sector, one year's densities for both Marches, a regression of every retail employer's staff on its floor area by description and the same over every employer) files one set and prints every centre's employment to the same 50 and its change to the same whole per cent, and what rules out a share by size is the single-site employers' own staff per square metre (6.3 per 100 square metres in a shop against 1.4 in a retail warehouse and 1.0 in a warehouse), which no filed clause states and no table displays; the cheapest licensed member (one group-by of single-site staff over floor area by description) files the golden set, so the step is the recognition, not a choice inside the family.
Analyst test: A strong analyst who reads every file correctly sees that the PAYE address is not the workplace, matches each retail employer to its premises through the ratepayer accounts and the valuation list, shares each chain's staff over its premises by floor area and names 19 centres, adding Rookgate City Centre, Glenskarn, Neshdale, Skelrigg and Halmoss and dropping Ravbeck, where the chains' new retail park units and distribution centres hold between a quarter and a sixth of a shop's staff per square metre and those five centres fell 5.3 to 6.4 per cent.
Estimand: each designated town centre's workplace retail employment in March 2022 and March 2026 (the employees of employers classified to SIC 2007 division 47 paid in the tax month ending 5 April, counted at the premises where they work, a premises being in a centre when its address postcode is in the Department's schedule for that centre) and its fall from the first March to the second, 8 per cent or more qualifying on unrounded figures; filed in the fund's prospectus (pdf), section 3.
No decoy: nothing is planted; the PAYE extracts, the valuation lists, the ratepayer accounts, the companies register and the centre schedule are the Revenue Office's, the Valuation Office's, the districts' and the Department's own records as their systems produce them; no memo, draft, briefing or stakeholder figure carries a wrong answer, and no filed sentence prescribes a share by floor area.
No certified replay: no workplace employment by premises, centre or district ships, so no certified or published figure confirms one placement over another; the densities come from the records.
Lesson: a payroll recorded at one address is placed at the sites that earn it by what each site's kind holds per square metre, read off the employers whose payroll and premises are one to one; no build on file places a recorded total at its sites by a per-kind density from the one-site units.

The card files the strategy as composition_mix: reading the register's grain correctly is the first rung (R0 to R2 all
read it), and the call turns on the chains' shift in premises mix between the two Marches, which the per-kind density
standardises and which no field states.

## Readability screen

Measured on the cut pack (seed 490).

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| R0 the PAYE postcode | each retail scheme's employees at its scheme postcode | the extract's postcode field | readable |
| R1 an equal share per premises | each chain's staff spread evenly over its occupied premises | the accounts list premises by ratepayer | readable |
| R2 floor area (default) | each chain's staff shared by its premises' floor areas | the valuation list's floor area column; the field's standard apportionment | readable |
| R3 rateable value | each chain's staff shared by rateable value, each year's list or one list for both | the list's rateable value column | readable |
| G golden (decisive) | each premises weighted by floor area times its description's staff per square metre, the single-site employers' staff over their floor area in that description and March | nothing states a density or that one employer's premises staff differently; the single-site employers are only employers with one premises, and no file compares staff with floor area | silent |

The description's mean staff per premises (the class step without floor area) names 13 centres on the cut pack, Fenmoss
and Quengate out: it takes the class recognition and drops floor area, so it is a variant that misses, not a member of
the standing family.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | workplace retail employment | employees of SIC 2007 division 47 employers paid in month 12, at the premises where they work | employees working in shop premises whoever employs them | not licensed, another quantity (asserted: one liable account a premises a day, so no premises is both a retail and another employer's) | prospectus 3.1 |
| SF2 | a retail employer | the class in that March's extract (division 47) | the class in the other extract; motor trades (45) or wholesale (46) added | same call under the other extract's class (asserted); 45 and 46 not licensed | prospectus 3.1 names division 47 and the extract of each March |
| SF3 | March | the tax month 12 return (6 March to 5 April), employees paid in the month | employees on the payroll at 31 March | same quantity: the extract carries one count | the extract specification |
| SF4 | a premises in a centre | its valuation list postcode in the centre's schedule | the PAYE postcode; the ratepayer's billing address | the PAYE postcode is rung R0 (another set); billing addresses are not in the schedule | prospectus 3.2 and the schedule |
| SF5 | the premises an employer occupies at 31 March | the account liable on that day and not shown empty | the account current at the extract date; empty accounts kept | same call (asserted: no retail account opens or closes within 14 days of either 31 March) | the accounts' dates and relief codes; C1 |
| SF6 | the list entry for a premises | the entry in force on that 31 March (2017 list for 2022, 2023 list for 2026) | the compiled entry; the latest alteration; a deleted entry | same call (asserted: floor area and description never differ between one premises' entries) | the lists' effective dates |
| SF7 | a fall of 8 per cent or more | unrounded March 2026 employment over March 2022, less one, at or below -0.08 | rounded figures | same call (asserted: every centre 1.65 points or more from the line) | prospectus 3.3 |
| SF8 | an employer | the company with all its schemes where incorporated, the scheme otherwise | each scheme on its own | same call and same figures (asserted: a company's schemes share its premises in the same proportions) | the specification's scheme note; C1 |
| SF9 | premises billed to a group's property company | the premises of the group's trading company, whose staff work there | the property company as an occupier with no staff | same call (asserted) | the companies register's parent company field and the premises' trading names in the accounts |
| SF10 | the single-site employers | retail employers occupying one premises in that March | employers of every sector; one March's set for both | same call and same rounded figures (asserted, the standing family) | the design |
| SF11 | an employer with no premises in the accounts | its employees work at no premises in any centre | its employees at its PAYE postcode | same call (asserted: none has a PAYE postcode in a centre's schedule) | prospectus 3.1, at the premises where they work |
| SF12 | the centre schedule | the Department's schedule with live and terminated postcodes | live postcodes only | same call (asserted: the schedule with live postcodes only files the golden set) | the schedule's own header |
| SF13 | rounding | employment to the nearest 50, changes to whole per cent from unrounded figures, premises whole | other roundings | not licensed | the prompt's closing sentence |
| SF14 | a shop premises (asks A and B) | a valuation list entry described Shop and premises | every retail description | not licensed | the prompt names shop premises; the list's descriptions |
| SF15 | empty (asks A and B) | an owner's account on the day: on empty property relief, or in the name of a company the register classes to letting (68209) or development (41100) | every premises without an occupier's account; an owner told by its name | a premises with no account: filed; the owner told by name: another count (the asks' device, ledgered) | the accounts' contents note and the companies register (ask sheet) |
| SF16 | empty for twelve months or more (ask B) | in the list throughout the twelve months to that 31 March and in no one's occupation on any of those days, the spell running through consecutive owners' accounts | the current account's start date; a premises entered within the twelve months | the current account: another count (a hazard, ledgered); in the list throughout: filed | the prospectus annex and the accounts' dates (ask sheet) |

## Ladder

Measured on the cut pack (seed 490): every golden centre 1.65 points or more from the line under every standing member.

| Rung | Centres that qualify | Flips from the golden | Call kept |
|---|---|---|---|
| R0 the PAYE postcode | 9: Skelrigg in; Dorrstead, Fenmoss, Kellgarth, Ravbeck, Vaskhope, Tormoss and Quenstead out | 8 | no |
| R1 an equal share per premises | 12: Ingmouth, Fenmoss and Quengate out | 3 | no |
| R2 floor area (default) | 19: Rookgate City Centre, Glenskarn, Neshdale, Skelrigg and Halmoss in, Ravbeck out | 6 | no |
| R3 rateable value, each year's list | 20: the same five in | 5 | no |
| R3b rateable value, the 2023 list for both | 18: Rookgate City Centre, Neshdale and Halmoss in | 3 | no |
| G golden and its standing family (seven estimators) | 15 | none | yes |
| T the world's true placement | 15 | none | yes |

Stage 3 targets, asserted in `generator/checks.py` on the clean truth and in `golden.py` on the cut pack: every golden
centre at least max(1.3 points, 8 employees over its 2022 level) from the line under every standing member and the
truth; every rung naming a different set from the golden and from each other; R2 off by three or more centres; every
standing member printing the same employment to the nearest 50 and the same whole-per-cent change for every centre.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | retail employers' employees paid in month 12 of each March | filed (prospectus 3.1); SF1, SF2 |
| 2 | Unit of account | a centre's employees placed at its premises, both Marches | filed (prospectus 3.1, 3.2) |
| 3 | Attribution window | the tax month ending 5 April 2022 and 5 April 2026; occupation on 31 March | filed (prospectus 3.1); SF3, SF5, C1 |
| 4 | As-of dating | the extracts of May 2022 and May 2026; accounts as liable on 31 March; list entries in force that day | filed (the specification, the accounts' headers); SF5, SF6 |
| 5 | Version basis | the 2017 list for 2022, the 2023 list for 2026 | filed (prospectus 3.2); SF6 |
| 6 | Denominator | March 2022 employment for the change | filed (prospectus 3.3) |
| 7 | Weighting | none filed: the placement is the method | the design (the standing family, asserted) |
| 8 | Window length | one month each March | filed |
| 9 | Boundary inclusivity | a fall of 8 per cent or more qualifies | filed (prospectus 3.3); SF7, margins asserted |
| 10 | Rounding path | the test on unrounded figures; employment to 50 and changes to whole per cent in the schedule | the prompt; bins asserted for the standing family |
| 11 | Tie-break | none needed | asserted: no centre within 1.3 points of the line |
| 12 | Maturity and censoring | none: both Marches closed | not applicable |
| 13 | Order of operations | schemes to employers, employers to premises, placement, centre sums, change | linear in any order |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | a company's schemes added up; a premises' superseded list entries dropped | SF6, SF8 converge, asserted |
| 16 | Identity normalisation | ratepayers to employers by company number, else by name through the companies register's previous names and trading names | Layer 1; every retail employer's premises matched exactly once (asserted) |
| 17 | Netting against gross | none: headcounts | not applicable |
| 18 | Dimensional units | employees, square metres (net internal for shops, gross for large stores as listed), pounds of rateable value | filed (the lists' basis column) |
| 19 | Code and status semantics | SIC 2007 classes, the lists' description codes, the accounts' relief codes | filed (the lookups, the councils' code notes); SF2, SF14, SF15 |
| 20 | Integerisation | placed employees are fractional and summed unrounded | the prompt's rounding at the end |
| 21 | Clause scope | prospectus 3 covers the employment test; the asks are the schedule's vacancy annex | filed |
| 22 | Forward window contents | the eligibility governs the 2027 round; nothing forward is estimated | not applicable |

## Literal reader

Executing the prompt and every filed sentence word for word: the prospectus measures each centre's workplace retail
employment as the employees of division 47 employers paid in the March tax month, counted at the premises where they
work, and the extract specification says a scheme's postcode is its PAYE address. No file states where any multi-site
employer's employees work: the PAYE extracts give each employer's employees in total, the ratepayer accounts and the
valuation list give its premises, their descriptions and floor areas, and no file records staff by premises. A literal
reader therefore has to estimate each premises' employees from what the pack measures, and the only records that measure
staff against premises are the single-site employers', whose staff per square metre differ six-fold by description;
sharing a payroll by floor area assumes every premises staffs alike, which those records contradict, and the golden is
the placement they imply. Every alternative reading of a term (SF1 to SF16) is either filed away or converges.

## Oracles

No file ties only under the golden or only on a wrong read. No shipped file states workplace employment by premises,
centre or district, or ranks the centres; the footfall counts (the Department's town centre indicator) and the Labour
Force Survey's residents in employment by industry and district carry no workplace employment by centre. The asks' referees: the valuation list carries every shop premises with its entries
in force, and the companies register carries each ratepayer's activity class, the evidence an owner's empty account
rests on (never an answer).

## Ask sheet

The call's declared population is the retail employers in the two extracts, the premises they occupy at each 31 March
in the accounts and the lists, and the 31 centres' schedules. No ask computes over it: both asks count shop premises in
the centres that no one occupies.

| Ask | Quantity (unit, rounding in the prompt's closing sentence) | Population, outside the call's | Primary device (silent) | How it enters the call (H18) |
|---|---|---|---|---|
| A | for each district, the shop premises in its designated centres empty at 31 March 2022 and at 31 March 2026 (whole premises) | shop premises with no occupier on the day | D9 name agreement lying both ways: an owner's account carries no relief once the three months' empty property relief has run, and the companies the register classes to letting their own real estate (68209) trade under nominee, holding, numbered and family names as often as under property names, while the estate and letting agencies trading from shops (68310) carry property names; the register's class tells owner from occupier, the name does not | the schedule's vacancy annex, which the Department reads beside each centre's eligibility for the bid assessment |
| B | for each district, the shop premises in its designated centres empty for twelve months or more at 31 March 2022 and at 31 March 2026 (whole premises) | the same unoccupied shop premises, by the length of their empty spell | D5 a category crossed by label: developers (41100) hold premises bought for schemes, empty and sold on between developers and letting companies, so a register read that takes letting companies alone as owners drops or cuts every such spell; the spell runs through consecutive owners' accounts of either class | the annex's long-term vacancy line |

Shared hazards: reliefs recorded by code in every district, the empty property relief lapsing after three months (asks A
and B); the twelve months dated from the account current on the day rather than from the first of the consecutive
owners' accounts (ask B); deleted list entries carried with their end dates (asks A and B, and the call's path, neutral
there: asserted); premises entered in the list after April 2017 (ask B: the annex files "in the list throughout"). Fair
handling, asserted on the clean truth: an owner's account (empty property relief, or a liable party the register
classes 68209 or 41100) read as empty and a premises with no account read as occupied, as the accounts' contents note
files, reproduces all 12 of ask A, and chaining consecutive owners' accounts reproduces all 12 of ask B. Separation,
asserted by count: no owner's account names a retail employer, no premises without an account is a retail employer's,
and no ask row is read by the call.

Measured by: `generator/ceiling.py` on the cut pack.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A empty shop premises by district, both Marches | 12 | 0 | 0 | 0 | misses |
| B shop premises empty twelve months or more by district, both Marches | 12 | 0 | 0 | 0 | misses |

The cracker lands the call, runs the hygiene battery and reads the accounts carefully: it takes a premises with no
account as occupied, as the contents note says, an account on empty property relief as an owner's, and a liable party
the companies register classes to letting its own real estate as an owner, and it chains consecutive owners' accounts
day by day; it misses the developers, so over the 24 figures it keeps 0.0 per cent of ask weight (scores 45.0 with the
call), the mirror 0.0 per cent (12.0). The naive handling tells owners by name (property, estates, real estate,
investments) and keeps 0; taking every real estate class as an owner, the agencies included, keeps 1; taking any party
seen on empty property relief as an owner everywhere keeps 0; dating from the account current on the day keeps all 12
of ask A and none of ask B.

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.

## Tried and rejected

- 2026-10-21, the seed's world (ET43, U.S. pharmaceutical exports to Germany against Germany's imports from the U.S.):
  every lever is a filed concept (CIF against FOB valuation, country of origin against destination, recording date,
  classification) or an estimated rate small against the gap (freight margins by weight) or a composition rate of the kind
  task481 just spent (the asymmetry ratio by product mix, the re-dispatched share through Dutch hubs); dropped before any
  data was cut.
- 2026-10-21, survey research's census-register task type for this world: the honest home, but its ETL pairing was taken by
  task479's re-root (BLOCK ban.pairing, and ban.artifact on published_series); the build is filed in data integration.
- 2026-10-21, a single-area figure or a per-area allocation as the call: the allocation's decision type repeats task471's
  puzzle triple (population, none, allocation_to_total) and the per-dollar rounding cannot hold two unbiased estimators in
  one bin; the call is the census table itself, counts to the nearest ten.
- 2026-10-21, noise added to each cell at the block level with no structural zeros (the demonstration-data behaviour):
  four to five per cent of the county's residents landed in blocks with no housing, a symptom the hygiene battery flags
  and a share no production release would show; the release leaves such blocks empty, which also silences the device.
- 2026-10-21, block groups alike in age within a tract: the tract route then matched the golden on most counts and left
  two estimators in one bin for some and not others; block groups now differ in age within a tract, as they do, and the
  tract route is a rung (6 of 12 off).
- 2026-10-21, ask B's prior-number deaths left to chance: a death hazard spread over a decade put no unreported death under
  an earlier number in the four rural providers; the July 2026 review not held, and at least one such death per provider,
  give the device mass everywhere.
- 2026-10-21, each block's total held to its own precise count (as the production release holds block totals) with the
  age cells forced to it: on paper the drift between blocks turns into flattening inside each block toward the 46
  cells' even share, which moves a rural block's 60-and-over count only by the gap between its true share (about 31 per
  cent) and the cells' 35, a few residents per area against the 40 to 190 the per-cell processing moves; kept the
  per-cell processing, under which small blocks publish more residents than their housing would hold.
- 2026-10-21, architecture 1 (each provider area's census-day counts built from the release's block groups, cut groups split by census-day housing units, against the block sum), spent at stage 4: the judge returned NOT_DETERMINISTIC and SEND_BACK, competing_defensible_answer, because nothing shipped showed the published block counts biased, so the block sum read as a defensible estimate (Gates G and H passed); documenting the bias would leave the step to whoever reads the notes. Both scored readers filed the block sum (0 of 12) and kept all 12 service figures: the roster's meals_per_day capped the re-sent rows and the registry's links chained the earlier numbers, so both devices sat on the careful path.
- 2026-10-21, architecture 2 draw, screened before the entity-resolution step (each dead on file or on measurement):
  left truncation in an asset or licence register (task133's delayed entry, rejected again in task262, task257, task265);
  the oldest-old counted by extinct generations (task228); non-detects under several reporting limits (task189); triple
  collocation (task228); age heaping (task230's rejected draw); a lowered reporting threshold bridged by an overlap ratio
  (task481's conversion rates); a benchmark-to-indicator ratio carried past the last benchmark (task457's report against
  final); landfill first-order decay (task480's age-declining increments); load estimation from sparse samples (Jensen,
  task229); a staggered rollout of a measurement change (task453, and task480 v2's meter exchange in flight); pooled
  medians from brackets (the never-average reflex, task480's screen); degree-day temperature adjustment (fresh, but a
  per-unit degree-day regression is the textbook route and lands it); hedonic quality adjustment (the estimand's own words,
  constant quality, name the method, and the specification family forks); equipercentile against linear equating on random
  groups (task450's ground, a moderate stump); Fellegi-Sunter frequency weights (the linker's own error is task468's).
- 2026-10-21, architecture 2 draw, the card's first labels: population, G2 or G12 and method_or_model_selection repeat four
  older builds' signature (test.same_driver_older, test.same_puzzle_older against task142); relabelled G17 with G2 beside
  it and gate etl_conformance, the call being the region's conformed count with the resolution inside it. Then task251 v5
  entered the window and blocked local_government and operations_log: the integrator is the region's nonprofit HMIS lead
  and the context artifact the published point-in-time count.
- 2026-10-21, architecture 2 draw, the prototype (20,000 people over two fiscal years, half of the names drawn from a
  concentrated list): chaining every link left the region 387 short, 115 of the chained groups holding two records of one
  source and 112 holding two people with no such conflict. A merge with no conflict cannot be refuted by anything shipped,
  so the generator keeps every wrong link inside a conflict (no undetectable merge) and gives every partial record its own
  person among the records it links, or the resolved count would differ from the people served by a quantity no method
  can see.
- 2026-10-23, the linkage weights as first drawn (a birth month or day disagreement at -3.0 and -3.5): two different
  people of one name and year who agree on the month or the day alone scored 10.5 to 11.5 and linked, and 35 of 207
  merged groups then split one way under an exact constrained optimum and another strongest first; the disagreements
  weigh -6.0, as they do between true matches, and the generator's tidy step makes every licensed resolution return the
  same people (strongest first under any order of equal links, on FY2026 records only, and every optimum of three
  objectives).
- 2026-10-23, materiality at 24,000 to 30,000 households: the default path moved Halvering's amount by about 18,000
  dollars; 44,000 households, with the City's outreach team also meeting downtown single adults outside the street count,
  give 130 Halvering people and 28,815 dollars.
- 2026-10-23, the bridge as the graded shape (03): its opening items, each source's records with FY2026 service, need no
  linkage, so every response banks them; the graded structure is the allocation's buckets (05).
- 2026-10-23, ask B over households: 147 households moved in twice in FY2026, so an average per household forks; the ask
  is per move-in. Its figures needed placing mid-bin, so the move-in waits are drawn from their own stream after the
  world is fixed, with a knob by Continuum and household type.
- 2026-10-23, ask A's 16 cells beside ask B's 5: one repair (a person's night counted once) gave a solver 16 of 21 ask
  figures; ask B is split by household type, 10 figures.
- 2026-10-23, Melbray's enrollment keys written as E- and six digits: 875 ids collided and exits joined to the wrong
  stays; the vendor's key carries seven digits.
- 2026-10-23, the world's first names (Calvera, Mardell, Ostry, Pellam, Valley Street Medicine, Safe Harbor, Riverside,
  New Hope, Mercy Commons): house fix H21 against a register of U.S. counties, states and cities found Calvera two letters
  from California's Calaveras County and Pellam one from Pelham, with Sartell, Story County, Valley Stream, Safety Harbor
  and New Hope near the rest; renamed Halvering, Melbray, Ondrava, Pyrenna, Wayfarer Street Health, Hearthstone, Elm
  Street and Brightwater, Stepping Stone and Kestrel Commons, with Continuum codes HAL, MEL, OND and PYR chosen to keep
  the old codes' alphabetical order so no draw moved (every figure unchanged, asserted by the rebuild).
- 2026-10-23, architecture 2 (the unit's pairwise findings resolved into people so no person holds two records of one
  source), spent at stage 4: scored reader A, on a fresh copy of the prompt and the pack, merged the LINK findings,
  counted each merged group's records by source, found the 225 groups holding two records of one source ("which cannot
  be one person"), clustered strongest first refusing a shared source or a NONLINK and landed the call exactly (all five
  amounts and people; score_reader FAIL, 22 of 32 ask figures, every night cell, no wait). It named the guide's
  one-record-per-person sentences as what decided it: the grains the determinism needs are the cue, and a conflict a
  per-group count shows is a visible relation. Reader B and the judge thread were stopped at the spend. Re-rooted fresh
  by the author's rule (no retirement).
- 2026-10-25, architecture 3 draw, screened before the class-density step (each dead on file or on measurement): member
  months and the ratio of totals (spent); length bias (task182 v4 and others); net against gross misclassification
  (task481, task244); trend uncertainty (task482 v10); moving holidays (task162, task467); deductible leveraging and a
  plan-year clock (task479 v3, task478's screen); adverse selection (task174, task479); over-coverage and signs of life,
  extinct cohorts, death completeness (spent); a lagoon's volatile solids (a kinetic fork); truth discovery across sources
  (Layer 1); suppressed cells (task465, task475); rater severity (task471 v2); clock drift (spent); tankering (the bottom-up
  burn table is the reflex, task153 a sibling driver); surprise-billing arbitration (an open-dispute maturity replica of
  task482 v14, or composition, or a final-offer model that fails the swap); fuel factors by stoichiometry (the hourly fuel
  records cover the units that matter); testlet and subscore reliability (not the objective); deadband logs (fails the
  swap); fertiliser forestalling (cue and determinism); a bridge detour (task474 v6's world); rice water regimes (forks);
  aircraft auxiliary power by stand (the ground power logs cover it); surname-change blocking misses (Layer 1 keys);
  second homes (task305); point-source subtraction (semantics); central payroll profiling read from accounts notes (a
  cue, and zero-employee retailers show in a per-unit check).
- 2026-10-25, a head office's staff placed at premises with a local-unit file shipped: a reflex join once the file ships
  (task485's own screen); here no local-unit staff ship, and a premises' staff exist only through the density.
- 2026-10-25, a sub-national region (a combined authority) as the world: national chains are registered outside it, so
  their staff sit outside the region's PAYE extract while their shops sit inside its town centres; the island holds one
  register and one valuation list.
- 2026-10-25, the prototype with chains whose class mix holds still (proto2): floor area and rateable value named the
  golden set exactly (25 of 25), because a share by size is biased in level but not in change when a chain's sparse share
  does not move. Chains that open retail park units and distribution centres and close small shops between the Marches
  separate them (proto3: floor area adds five centres, rateable value three, the premises count drops four, the PAYE
  postcodes miss three; five density variants agree, the rateable-value density flips one centre at minus 7.47 per cent,
  a margin to build at stage 2).
- 2026-10-25, the card's first furniture (the combined authority's board, its budget round, local government) against the
  window: task269's council_or_assembly, budget_or_appropriation and local_government; redrawn with the world.
- 2026-10-25, the Department's 2025 town centre health check as the second distractor: it gave each centre's vacant
  shop units, a soft oracle for ask A; replaced with the Labour Force Survey's residents in employment by industry and
  district, which carries no premises and no centre.
- 2026-10-25, recoding every postcode unit the postal administration terminated: units holding a retail employer's
  premises moved the call when a solver dropped the terminated codes (R2 failed); the recode touches only units with no
  retail employer, as a small batch of recodes would.
- 2026-10-25, the island's total change in component 2 to the whole per cent: it sat at minus 6.500 per cent, on a
  rounding boundary; component 2 states the two totals to the nearest thousand and no per cent.
- 2026-10-25, the planner's flips placed at the line: centres bunched just past 8 per cent under a share by floor area;
  each flip target is drawn within its feasible range.
- 2026-10-25, empty spells starting uniformly over the decade: about nine in ten empty shops had stood empty a year or
  more; closures are weighted to the later years.
- 2026-10-26, the relief's ceiling applied to the unrounded rateable value: the lists print values below 10,000 to the
  nearest 25, so three premises listed at exactly 8,000 had no account; the ceiling now applies to the value the list
  prints, entry by entry (every graded figure unchanged, asserted by the rebuild).
- 2026-10-26, the card's strategy and context artifact as drawn (grain_or_unit, register): task137 v2 filed both three
  minutes earlier in another session and merged after this draw, so heart BLOCKed both axes at stage 3. Redrawn, not
  argued: the step the call turns on is the chains' premises mix moving between the Marches (with the mix held still a
  share by floor area names the golden set exactly, the proto2 line above), corrected by standardising each premises'
  staff to its kind's density, which is composition_mix; and the context artifact is the office's own Labour Force Survey
  series, a published_series answering the residence-based question correctly, while the registers are evidence.
- 2026-10-26, the world's first names against real places (H21, GeoNames places of 500 or more in the British Isles and
  the main English-speaking countries, and small British Isles places the file lacks): Lundwold sat one letter from
  Lundwood (Barnsley), Glenholt is a Plymouth suburb, Ravscar two letters from Ravenscar, Kellscar held Kells, Molmoss
  two from Moyross, Molwick one from Holwick, Halsett one from Hallett, Glengarth two from Glengarry; the chains
  Brackwell, Kilnworth, Hartwick, Ashcombe, Hearthwell and Ferngrove one or two from Bracknell, Kilworth, Harwick,
  Ashcombe, Hartwell and Ferny Grove; the property roots Thornbury, Larchmont, Mullion, Yarrow, Kingsmere and Highcross
  are real places or a shopping centre. Renamed Torvasay, Glenskarn, Ravbeck, Kellholm, Molscar, Molrigg, Halvask,
  Glenscar, Brackmoor, Kilnhaven, Hartsmere, Hobbyhorse, Hearthside, Fernhollow, Thornwater, Larchcroft, Architrave,
  Cowslip, Kingsmarsh and Highgable, each clear of the same screen and of every other build's invented words.
- 2026-10-26, stage 4 round 1 on zip 2494d1db: both scored readers missed the call (reader A 11 centres, a density
  fitted on the chains' own headcounts; reader B 13, weights fitted on the chains' totals, Fenmoss and Quengate out),
  but the ask layer split: reader A kept 0 of 24 (unaccounted shops counted empty), reader B 24 of 24 (owners told by
  the 30 landlord name stems the generator drew, checked against the two status columns, unaccounted shops left
  occupied, the twelve months checked day by day). The judge: DETERMINISTIC, FIX_NOW on block 1's "10 per cent or
  more" (true only rounded) and on the unaccounted reading being unfiled, a fork rather than a device; the silently
  partial extract (D5) and the anchor on the current record (D8) are set aside as primaries, the first a fork once a
  literal judge reads it, the second falling to the day-by-day check the annex's own definition invites. Re-sited in
  one pass with the call frozen (figures.json call, components, schedule and ladder identical): the accounts' contents
  note files what an account is and what no account means; the two status columns dropped; owners drawn from 78
  roots under property, nominee, holding, numbered and family names, developers among them; agencies under property
  names; the annex's twelve months need the premises in the list throughout; accounts clipped to the start of their
  premises' list entry.
- 2026-10-26, architecture 3 (each multi-site retail employer's PAYE staff placed at its premises by floor area times
  its description's staff per square metre, measured on the single-site retail employers), spent at stage 4 round 2 on
  zip 032f619f: scored reader D (sonnet, medium, fresh copy) estimated the densities from the single-site employers
  by description, split each multi-site employer's staff by floor area times them and landed the call, all 62
  employment figures, all 31 changes and all 24 ask figures (score_reader exit 1); reader C took a share by floor
  area (17 centres, missed) but also kept all 24 ask figures; the pass 3 judge thread returned DETERMINISTIC and
  APPROVE (Gates G and H pass; an optional tidy of six 2017-list rows dated after its extract). Across the two rounds
  three of four readers remarked the single-site employers' staff per square metre as a tight, visible ratio (0.062
  to 0.063 a square metre, correlation about 0.9 with area), one of them applied it by description, and a per-kind
  density read off the one-site units is a single group-by once noticed. The re-sited asks fell the same way: with the
  status columns gone, both round 2 readers took the companies register's class (68209 and 41100) as the owner's
  mark, the obvious next signal, so an owner told by its register class is the careful route, not a device. Spent by
  the lane's rule (a call any reader lands is spent); reader C stopped at the spend.
- 2026-10-26, architecture 4 draw, screened against every card, slot note and the four ETL cells the window leaves open
  (data integration, payment claims, emissions inventory, IRT test equating; the census-register pairing banned by
  task485), each dead on file or on the rules: a common stack's units unmixed by their hourly mix (task263); startup
  excess carried from monitored to unmonitored units by starts or by downtime before each start (a rate set by an
  operating condition, task478 v7, and a state rebuilt from the unit's own record, task485 v4's driver); landfill first
  order decay, load estimation from sparse samples, Fellegi-Sunter frequency weights, non-detects, age heaping and
  degree days (this note's architecture 2 screen); length-biased durations from snapshots (task182, task120, task130,
  task135, task201); rapid guessing read from response times (task479, task249); capacity-censored demand (task120's
  screen, and no ETL task type works it); repeaters in a random-groups equating (population_selection, banned against
  task137, and NEAT is task450's); opt-outs imputed from prior scores (a missing-data step no ETL task type works);
  benefit accumulators against an out-of-pocket maximum (executing the stated benefit design member by member is rule
  application); pharmacy rebates allocated by product (a grain read off the rebate file); hourly grid factors against
  the annual factor (the reporting standard's own choice, semantics); the sampling variance of a fuel's composite
  analyses behind a listing bound (the variance family forks a borderline listing). The lane's last three ships turn on
  one shape (a rate conditioned on a covariate whose mix shifted: heat content, class density, migration history), so a
  fourth is a strategy monoculture whatever its label. The UCI order log (task487's seed spine) is refused by the
  network proxy, so that pack would be constructed too. Resume at the draw with a step outside those families.
