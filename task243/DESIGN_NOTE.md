# task243 design note

Architecture 1, wave 4, seed DQ16 (which local areas' register counts breach the undercoverage alert): the seed's
world (local areas' register counts), decision (which areas go into the register-improvement programme) and quantity
(how far a register falls short of what it should hold) only. The seed's register is a population register checked by
a coverage survey and its pitfall a dual-system estimate; capture-recapture traps are spent in the corpus (task448's
second list measured within route strata, task196's second source fed by the first), so the register becomes the civil
register of deaths, whose undercoverage the field measures with a death distribution method rather than a second
count. The Province of Kalinawan (fictional, in Mindanao, the Philippines) reviews the death registration of the local
civil registry offices (LCROs) of its two component cities and ten municipalities between the 2015 census (POPCEN,
reference date 1 August 2015) and the 2020 census (CPH, reference date 1 May 2020); the offices that register fewer
than 80 per cent of their residents' adult deaths go into the province's 2024 civil registration improvement programme.

## Draw

Card `cards/task243.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, each answered here:
repeat.question_form (which, against task194): the decision is a designation of LGUs, and "which" is the form a
designation takes. repeat.gate_g and repeat.decision (decomposition_attribution and designation_set, against task470,
another lane's ETL build): task470 rebuilds each airfield's piston operations from a receiver network that never
records some aircraft (the never-recorded based aircraft times the activity per such aircraft at fully counted fields)
and designates the fields that qualify for grants; task243 books each age group's shrinkage between two censuses to
deaths and to movement and designates offices against a completeness alert; the mechanism family and the answer type
are shared, the quantity, the method and the data are not. test.same_puzzle_older (task450
v2) and test.same_driver_older (task129 v2) are differentiated on the card; the nearest driver is task181 v2 at 0.07.
task470 was registered 21 minutes before this card and reached main only after this card's check, so its stakeholder
role and organisation family (policy_adviser, local_government) blocked at stage 3; both are redrawn: the review is
done by a university population studies centre the committee engages (research_desk, university_or_school).

- **Pairing.** Survey Research & Official Statistics / census-register-administrative-data-quality, serving Data
  Quality Monitoring & Alerting. Not banned against the last three builds (task196, task190, task194). The object is
  the health of the civil registration data (the share of its residents' deaths each office registers), the call a
  monitoring decision: which offices carry the completeness alert into the programme.
- **Niche.** Death registration completeness between two censuses, read the way demographers read it where
  registration is incomplete: the population above each age changes between the censuses by the people who reach that
  age, the deaths above it and the people who move in or out above it, so the deaths the registers should hold are
  recovered from the censuses' age counts (Hill's general growth balance), and the completeness is the registered
  deaths against them.
- **The call.** Which of the 12 LGUs' offices register fewer than 80 per cent of the deaths of their usual residents
  aged 15 and over that occurred between the two census reference dates (registered by 31 March 2023, the extract), and
  so go into the 2024 programme.
- **Shape.** 07, a grid of cells: one row per LGU with its completeness and the alert, beside the LGU's columns for the
  asks (12 rows, the call picked per row), the designated set, the chart (each LGU's completeness against the 80 per
  cent line, the designated LGUs marked) and the two files: 12 completeness figures, 12 alerts, 24 ask figures, the set,
  the chart's parts and the files, well over 25 criteria before the rubric folds them. Decision designation_set, answer
  set_of_items, question form which.
- **Strategy.** decomposition_attribution (the change in each age group above an age between the censuses is booked
  to deaths and to movement; the closed balance books all of it to deaths), G4 decisive (who holds a mover once the
  mover leaves: the origin's population loses the mover without a death, the destination gains one whose later death it
  registers), G16 (the closed balance against the balance carrying movement, forced by the census's own count of
  movers), G6 (the population above each age shifts by movement under the balance); gap population (the population
  above each age is open); Gate G decomposition_attribution; calibration none (no corpus or gold standard: the
  censuses' own residence question carries the term); context artifact published_series (the two censuses' age
  tables, the province's working inputs); layer 2 family field_method, pattern
  own:migration-term-in-the-growth-balance.
- **Forum, event, organisation.** committee_or_panel (the Provincial Civil Registration Committee, which selects the
  programme's offices), launch_or_rollout (the programme's rollout to its first offices in January 2024),
  university_or_school (Kalinawan State University's Population Studies Center, which the committee engages for the
  review under the province's agreement with the university). All clear the last three (task190, task194, task470).
- **People** (`guard.py names --locale fil_PH --seed 243`, chosen from the draw for names common in the Philippines):
  Nicole Gomez, a research associate at the university's Population Studies Center, who runs the review for the
  committee; Randy
  Cortez, the civil registrar of Kalinawan City, who chairs the committee's technical working group; Casey Carrillo,
  the provincial statistical office's officer who handled the census tabulation request; Steven Jimenez, the provincial
  administrator, who chairs the committee.
- **Deliverables.** `lcro_death_registration_completeness_2015_2020.xlsx` (each LGU's row: completeness, its range
  over the fitting choices, the alert, and the asks' columns) and `crvs_committee_note_2023.docx` (the committee note,
  with one chart: each LGU's completeness against the 80 per cent line, the designated LGUs marked).
- **As-of.** Monday 6 November 2023: the census office released the 2020 census's age and sex tables in 2022 and the
  special tabulation of residence five years earlier for the province in October 2023, the civil registry extract was
  taken on 31 March 2023, and the committee meets on 21 November to name the offices for the January rollout. The call
  is retrospective by nature (completeness is measured between two censuses, and 2015 to 2020 is the latest pair); what
  it settles is which offices go into the 2024 programme.
- **Data-native sentence.** Kalinawan's oldest residents leave the farming and remote municipalities for their
  children's households, most of them out of the province, at rates that rise with their frailty, so each place's
  population above every age shrinks between the censuses by departures as well as by deaths, in proportion to its
  deaths; the growth balance taken as closed keeps its straight line while its slope reads the departures as deaths
  nobody registered, and only the 2020 census's question on where each person lived on 1 May 2015 (whose special
  tabulation also counts the former residents enumerated elsewhere in the country) carries the movement into the
  balance.

Sources, one line each (what it teaches; how this build differs):
- Hill (1987), the general growth balance: completeness of death registration relative to two censuses from the
  birthday rate less the growth rate above each age against the registered death rate above it; here the population is
  open, and the field's repair is the build's decisive step, never named in the pack.
- Hill and Queiroz (2010), adjusting the general growth balance for migration (applied to Brazil's states): the net
  migration rate above each age enters the balance; here the movers are the oldest residents, whose movement follows
  their mortality, so leaving it out moves the slope without bending the line.
- Bennett and Horiuchi (1981), synthetic extinct generations, and the hybrid of Hill, You and Choi (2009): the other
  death distribution methods, which share the closure assumption; a rung, never the answer, and carrying the movement
  they file the same five (asserted).
- Moultrie and colleagues, Tools for Demographic Estimation (IUSSP, 2013), the death distribution chapters: the
  textbook route a careful analyst follows (fit over the ages that sit on a line, trimming the young adults' labour
  moves), which is the default path here.

## Default path

1. Read the two censuses' household population tables by LGU and five-year age group (2015 POPCEN and 2020 CPH, both
   on the 2020 boundaries).
2. From the civil registry extract keep the deaths of each LGU's usual residents that occurred from 1 August 2015 to
   30 April 2020, as registered by 31 March 2023: placed by usual residence, residence spellings mapped, a row sent twice
   and a death registered at two offices counted once, non-residents and fetal deaths out, unstated ages spread pro
   rata.
3. Fit Hill's general growth balance for each LGU (the birthday rate less the growth rate above each age against the
   registered death rate above it, over ages 15+ to 65+, or trimmed to 35+ to 75+ once the young adults' labour moves
   show as a bump at 15 to 25, orthogonal fit), the population taken as closed; completeness is one over the slope.
4. Flag each LGU under 80 per cent.

Ends on: eight LGUs flagged (the City of Santa Cruz, San Isidro, Esperanza, Magsaysay, Mabini, Libertad, San Luis,
Del Carmen): the three farming municipalities whose oldest residents leave read 72, 76 and 74 per cent over 15+ to 65+
(74, 78 and 75 trimmed), every fit a straight line.

Golden: five LGUs flagged (the City of Santa Cruz, San Isidro, Libertad, San Luis, Del Carmen), from the same balance
carrying each LGU's net movement above each age: the persons in the LGU in 2020 who lived elsewhere on 1 May 2015, less
the persons anywhere in the country in 2020 who lived in the LGU then, from the census office's special tabulation;
Esperanza, Magsaysay and Mabini register 89 per cent each.

## Stump sentence

A competent demographer fits the general growth balance to each LGU's 2015 and 2020 census age counts and its
registered adult deaths with the population taken as closed, as the method is set out (over 15+ to 65+, or trimmed to
35+ to 75+ for the young adults' labour moves), finds every fit a clean straight line and ends on eight LGUs flagged,
the three farming municipalities among them at 72 to 78 per cent; the step that lands it there is leaving the oldest
residents' movement out of the balance, which reads each departure as a death nobody registered, so only the balance
carrying the 2020 census's count of who moved above each age, the former residents enumerated elsewhere in the country
included, gives the five.

## Three rules

- **Task type:** survey-research-official-statistics / census-register-administrative-data-quality, which serves Data
  Quality Monitoring & Alerting (the civil register of deaths is the monitored administrative data, the completeness
  alert the monitoring decision).
- **Domain test:** the quantity that decides is each LGU's completeness of adult death registration, estimated the way
  demographers estimate it where registration is incomplete: a death distribution method, Hill's general growth balance
  of the population above each age between two censuses against the deaths registered above that age, with the net
  migration rate above each age in the balance (Hill and Queiroz) because the LGUs are open populations.
- **Swap:** "which LGUs' civil registry offices register fewer than 80 per cent of their residents' adult deaths"
  rewritten as "which hospitals' discharge registers record fewer than 80 per cent of their discharges", or with
  megawatt-hours for deaths: there is no population ageing between two censuses, no birthday rate above an age and no
  balance to fit, so the completeness has nowhere to come from and the task stops making sense.
- **Layer 1:** the civil registry extract (keyed by registering office, the City of Santa Cruz's records before its
  2019 charter under the municipality's name) carries residence written in several spellings, late registrations
  entered months or years after the death (the 2020 lockdown's backlog among them), deaths registered where they
  occurred (the provincial hospital's office and offices outside the province holding the province's residents, and
  other provinces' residents in the city's hospitals), deaths registered a second time at the residence office, a
  batch two offices' systems sent twice, fetal deaths, and unstated ages or infants' ages in months, days or hours; the
  census tables are in the census office's printed layout (an All Ages row per LGU, the 2015 table naming Santa Cruz as
  the municipality it then was). Each is produced by the system that records it; none is placed to be caught, and the
  call is the same under every handling of each (SF rows in checks.py) or loudly wrong (Kalinawan City over 200 per
  cent when deaths are placed by the registering office).
- **Layer 2:** field_method: the death distribution method carried for an open population, the net movement above each
  age from the census's residence question put into the growth balance, against the balance taken as closed.
- **Decisive step:** carrying each LGU's net movement above each age into the growth balance, so that the population
  the balance reads between the censuses changes by entries, deaths and movement, rather than fitting the balance with
  the population taken as closed (over any age range, or with any other death distribution method that shares the
  closure).
- **Not semantics:** reading every field right (usual residence, date of death, date of registration, age units, the
  census tables, the residence five years earlier) still leaves the closed balance on eight LGUs flagged: the census's
  residence question is plain, and reading it right does not say that it belongs in the balance or how it enters.
- **Not rule application:** the province's review terms file what completeness is (the registered share of the deaths
  of the LGU's usual residents aged 15 and over in the interval) and the 80 per cent alert; no filed rule or procedure
  says how the deaths that should have been registered are estimated, so executing every stated rule with the textbook
  closed balance files the wrong eight.
- **Analyst test:** a strong analyst who reads every file right and applies the alert as filed fits the general growth
  balance with the population taken as closed (as the textbook sets it out, over the usual ages or a trimmed range),
  sees straight lines and ends on eight LGUs flagged, Esperanza, Magsaysay and Mabini wrongly; on the simulator's
  clean truth (everyone counted, every registered death once) the same route files the same eight, the three farming
  municipalities at 0.71 to 0.75, and the decisive step alone gives the five, the three at 0.87 to 0.88 (R3a and R3b in
  checks.py).
- **Estimand:** the province's review terms (`crvs_review_terms_of_reference_2023.pdf`, indicator D1) define
  completeness: the registered deaths of the LGU's usual residents aged 15 and over that occurred from 1 August 2015 to
  30 April 2020 and were registered in the Civil Registry System by 31 March 2023, as a share of all deaths of those
  residents in that interval, a death belonging to the LGU of the deceased's usual residence at death, wherever in the
  country it was registered; the alert is D1 below 80 per cent; the prompt asks for completeness in whole per cent.
- **No decoy:** nothing is planted: no memo, earlier assessment or stakeholder figure argues a method or an office; the
  census tables and the special tabulation are the census office's products, the extract is the registry's own, the
  FHSIS reports are the health offices' own (a different, incomplete count, set against nothing) and no file ranks the
  offices on completeness.
- **No certified replay:** no certified or published completeness for 2015 to 2020 exists for a method to reproduce;
  the method is found from the data's structure (the censuses, the deaths and the census's own residence question).
- **Lesson:** a death distribution method reads each age group's shrinkage between two censuses as deaths, so where the
  oldest residents move at rates that follow their frailty the shrinkage includes the movers while the diagnostic line
  stays straight, and the balance has to carry the census's own count of who moved; no build on file uses a demographic
  balance or a death distribution method (task231 and task230 carry late exits and a late channel, task242 a detector
  fading with time).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) the closed balance over 15+ to 65+: eight | the ToR defines D1, no method | the census tables and the extract | yes, the growth balance as the manual sets it out | none | no | a fitted line | readable |
| 1 the closed balance trimmed to 35+ to 75+ for the labour bump: eight | none | the census tables | yes, fit the straight part | none | no | a fitted line | readable |
| 2 synthetic extinct generations, or Brass's one-census balance: eight, or all twelve | none | the census tables | yes, a second method as a cross-check | none | no | a cumulation | readable |
| 3 the tabulation's movement within the province only: eight | none | the tabulation's own rows | partly, the province's offices as the universe | none | no | sums by age | readable |
| 4 (decisive) every LGU's net movement above each age, the former residents enumerated elsewhere in the country included, carried into the balance: five | no sentence names movement, migration or the balance's closure; the cover note describes the tabulation, sent for the PDPFP update | no migration rate, net mover or completeness column; the tabulation joins by name and age group only | no: the textbook balance is closed and its line stays straight | no control, published completeness or earlier estimate | no | not linear: a net movement by age, placed half a group younger, carried to the interval, cumulated above each age, per person-year, inside the fit | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | residents' deaths | by usual residence at death | by the registering office, or the place of death | another set, Kalinawan City over 200 per cent | the ToR's D1: "A death belongs to the city or municipality of the deceased's usual residence at death", and its scope "wherever in the country the event was registered" (asserted) |
| SF2 | deaths at ages 15 and over (unstated age) | unstated ages spread pro rata | dropped | same call | same call (asserted) |
| SF3 | age at death | as stated on the certificate | from the date of birth where stated | same call | same call (asserted) |
| SF4 | between the census reference dates | 1 August 2015 to 30 April 2020 | to 1 May 2020 inclusive | same call | the ToR's dates; same call (asserted) |
| SF5 | deaths that occurred in the interval | by date of death | by date of registration | same call | the ToR ("that occurred from"); same call (asserted) |
| SF6 | registrations up to 31 March 2023 | every extract row | none differs | converge | every row was registered by 31 March 2023 (asserted) |
| SF7 | register (a death registered at two offices) | once, at its first registration | twice | same call | same call (asserted) |
| SF8 | rows sent twice | once | twice | same call | same call (asserted) |
| SF9 | deaths (fetal deaths) | certificates of death only | fetal deaths read as deaths of unstated age | same call | the dictionary's CERT_TYPE; same call (asserted) |
| SF10 | residents (other provinces') | the province's residents | every row | converge | no other province's residence maps to an office (asserted) |
| SF11 | cities and municipalities | the 12 LGUs, every spelling mapped, Santa Cruz before its charter included | none differs | converge | every resident's residence maps (asserted) |
| SF12 | the interval's length | days over 365.25 (4.7502) | 4.75, or days over 365.2425 | same call | same call (asserted) |
| SF13 | completeness relative to what | the censuses' mean coverage | relative to either census | same call, inside the accepted interval | the readings (asserted) |
| SF14 | fewer than 80 per cent | strictly below | at most 80 | same call | no reading within 4 points of 80 (asserted) |
| SF15 | completeness in whole per cent | the golden reading rounded, inside the interval | any reading in the interval | accepted | the interval (asserted) |
| SF16 | population | household population, both censuses | none ships | converge | both tables are household population; the tabulation leaves out institutional households (asserted) |
| SF17 | completeness of each office (one figure) | both sexes together | each sex separately, combined over their registered deaths | same call, inside every interval | same call (asserted) |
| SF18 | persons reaching each age per year | the geometric mean of the two age groups either side | the arithmetic mean | same call, inside every interval | the readings (asserted) |
| SF19 | a death registered at two offices (blank date of birth) | a blank matches a blank | a blank never matches | converge | every second registration carries its date of birth (hospital certificates do), asserted for the interval and for 2022 |

## Ladder

Four wrong rungs and the golden, each a defensible way to estimate completeness, each dying to one fact of the record
(figures on the cut pack, printed by `generator/pair.py --ladder`, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | the closed balance, 15+ to 65+, orthogonal | eight: Esperanza 72, Magsaysay 76, Mabini 74 per cent with the five | the tabulation: Esperanza lost a net 653 people aged 50 and over in the five years, Magsaysay 544, Mabini 581 |
| 1 | the closed balance trimmed to 35+ to 75+, or over any of the 25 ranges by either fit and either mean | eight (Esperanza 0.692 to 0.749, Magsaysay 0.723 to 0.781, Mabini 0.689 to 0.748) | the same: trimming removes the labour bump, not the oldest residents' departures, which follow their mortality |
| 2 | synthetic extinct generations (closed), or Brass's one-census balance | eight, or all twelve | the same closure; Brass also assumes a stable population the censuses' growth rates refute |
| 3 | the tabulation's movement within the province only | eight (Esperanza 74, Magsaysay 77, Mabini 75) | the tabulation's ELSEWHERE IN THE PHILIPPINES rows: most of the three's departing elders went out of the province |
| 4 (golden) | every LGU's net movement above each age in the balance | five | |

- **Margins.** The five sit at 52 to 64 per cent (readings 49 to 68), the other seven at 89 or 90 (readings 82 to 99);
  over the 1,200 readings an office (both placements of the movers' ages, scaled or not, 25 fitting ranges from a
  lowest age of 10+ to 30+ and a highest of 55+ to 75+, two fits, the geometric or arithmetic mean for the persons
  reaching each age, three coverage bases) no flagged reading passes 0.675 and no other falls under 0.818. Synthetic extinct generations and the
  hybrid, both carrying the movement over six and three ranges, file the same five, the five under 0.775 and the rest
  over 0.845.
- **Position.** The five are reached by no other rung: every closed reading, the trimmed balance, synthetic extinct
  generations and the in-province movement file eight, Brass all twelve.
- **Dominance.** The decisive move takes the three farming municipalities from 0.689 to 0.781 to 0.823 to 0.989, and
  moves the others by 6.2 points or less on the 15+ to 65+ fit: the three remote municipalities, which lose elders too,
  rise 5.6 to 6.2 points and stay far under the line; Kalinawan City and the towns, which take in a few, come down 2.2
  to 5.6; the two peri-urban municipalities move 1.3 points or less.
- **Grid.** Closed, any range or fit (eight); closed SEG (eight); Brass (twelve); in-province movement (eight); the full
  movement under any reading (five); the full movement with SEG or the hybrid (five). On the simulator's clean truth the
  closed balance files the eight (the three at 0.71 to 0.75) and the survivors' movement gives the five (the three at
  0.87 to 0.88) (R3a, R3b).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | usual residents of each LGU aged 15 and over, by residence at death (ToR D1; SF1, SF10, SF11) |
| 2 | Unit of account | one LGU's completeness, one alert per LGU (ToR) |
| 3 | Attribution window | deaths that occurred 1 August 2015 to 30 April 2020 (ToR; SF4, SF5) |
| 4 | As-of dating | registrations by 31 March 2023, the extract's date; the review folder of 6 November 2023 (SF6) |
| 5 | Version basis | the 2015 POPCEN and 2020 CPH household tables as published; the tabulation as sent on 12 October 2023 |
| 6 | Denominator | all deaths of the residents in the interval, estimated from the censuses (ToR D1's "as a share of all deaths") |
| 7 | Weighting | the balance's orthogonal fit over the ages (slope the ratio of the standard deviations); either fit, and either mean for the persons reaching each age, inside the interval (C1, SF18) |
| 8 | Window length | 4.75 years between the reference dates (SF12) |
| 9 | Boundary inclusivity | below 80 per cent; no reading within 4 points of the line (SF14) |
| 10 | Rounding path | completeness from unrounded figures, whole per cent at the close, accepted inside the interval (SF15) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | registrations up to 31 March 2023 count, as the ToR files; nothing later exists |
| 13 | Order of operations | dedupe, place, window, group by age, movement, balance, fit, alert |
| 14 | Row order | no step depends on file order; a double registration's first registration by registration date and office |
| 15 | Duplicate resolution | rows sent twice and second registrations once (SF7, SF8); either way the same call |
| 16 | Identity normalisation | residence spellings mapped to the 12 LGUs, Santa Cruz's earlier name included (SF11) |
| 17 | Netting against gross | net movement: in-movers less out-movers by age group |
| 18 | Dimensional units | completeness in per cent; rates per person-year; persons |
| 19 | Code and status semantics | CERT_TYPE DEATH and FETAL DEATH (SF9); AGE_UNIT YEARS, MONTHS, DAYS, HOURS; the tabulation's SAME CITY/MUNICIPALITY, NOT STATED, OTHER PROVINCE, FOREIGN COUNTRY, ELSEWHERE IN THE PHILIPPINES |
| 20 | Integerisation | none; persons and deaths are counts already |
| 21 | Clause scope | D1 applies to each of the 12 LGUs' offices (ToR scope) |
| 22 | Forward window contents | nothing is forecast; the programme's first round from January 2024 is the call's use |

## Literal reader

Executing the prompt and the ToR's D1 and alert word for word: for each LGU the registered deaths of its usual
residents aged 15 and over, dated 1 August 2015 to 30 April 2020 and registered by 31 March 2023, as a share of all
their deaths in that interval, against 80 per cent. All their deaths are not counted anywhere, so the literal estimand
needs an estimate of them; the files hold the two censuses' age counts, the registered deaths by age and the 2020
census's residence five years earlier, and the field's estimate from those is a death distribution method, whose
balance holds for the LGU's population only with the movement in it. Every reading of that estimate (1,200 an office) and
the other death distribution methods carrying the movement file the five; the easy answer, eight, comes from an easy
method on the same literal estimand (the balance taken as closed), never from another reading: every row of the fork
table files the five except SF1's placement by registering office, which the ToR's own words rule out and which puts
Kalinawan City over 200 per cent.

## Oracles

None for the call: no published completeness, earlier assessment or alert list ships; the census tables and the
tabulation are inputs, tie to nothing and confirm no basis; the FHSIS mortality reports (a distractor) count the
deaths the health offices reported, a different and incomplete count that most offices' registrations exceed, so it
scores no method. For the asks, no published B1 or C1 ships; the ToR defines both and says nothing about second
registrations, twins or who signs a certificate in the health office's name.

## Ask sheet

**Ask A, each LGU's share of 2022 live births registered within 30 days** (B1, 12 figures). H18: the second-round
indicator the committee asked to see beside D1 (the request; the ToR: "reported beside D1 for the committee's second
round"); the call reads no birth. Use: the committee's request. Primary device D1 (a replay under fresh ids beside
genuine same-day pairs: a child born in the city's hospitals is registered at the hospital's office and again, weeks
later, at the parents' own office under a new registry number, so no exact-duplicate sweep sees it, while twins are
two children of one mother on one day); hazards: rows sent twice (exact repeats), births to mothers from other
provinces in the city's hospitals, late registrations of earlier years' births in 2022's drives. Path: the births
extract, the ToR, the dictionary, the README (4 files, 14 columns: REGISTRY_NO, LCRO_CODE, LCRO_NAME, DATE_REGISTERED,
CHILD_FIRST_NAME, CHILD_MIDDLE_NAME, CHILD_LAST_NAME, SEX, DATE_OF_BIRTH, TYPE_OF_BIRTH, MOTHER_FIRST_NAME,
MOTHER_MAIDEN_LAST_NAME, MOTHER_RES_CITY_MUN, MOTHER_RES_PROVINCE). Stops: every certificate a birth -1.8 to -0.4;
twins removed with the doubles (mother and day) -0.1 to +0.1, two of 12 kept; births registered in 2022 -6.4 to -4.8;
by the registering office -6.5 to -0.7. Realism: Philippine hospitals file the certificate at the city's office while
parents, unaware, register the child again at home, and the PSA's own matching counts each child once.

**Ask B, each LGU's share of its residents' 2022 deaths whose cause a licensed physician certified** (C1, 12 figures).
H18: the second-round indicator beside D1; the call reads no certifier column and no 2022 death. Use: the committee's
request. Primary device D7 (the true key elsewhere: a certificate for an unattended death is made in the health
office's name, its title MHO or CHO, but signed by whoever the office sent, a nurse, a midwife, or the nurse in charge
while the physician's post was vacant in four offices in 2022; only the PHO roster's posts and terms show who that
was); hazards: deaths registered a second time at the residence office (D1), a batch one office's system sent twice
(May 2022, Quezon), the visible titles NURSE, MIDWIFE and the mayors, fetal deaths, other provinces' residents. Path:
the death extract, the roster, the ToR, the dictionary (4 files, 12 columns: CERT_TYPE, RES_CITY_MUN, RES_PROVINCE,
DATE_OF_DEATH, DATE_REGISTERED, LCRO_CODE, REGISTRY_NO, CERTIFIED_BY, CERTIFIER_TITLE, the roster's NAME, POSITION,
FROM and TO). Stops: the title as written (MHO and CHO as physicians) +10.9 to +52.7; the same, each death once +10.7
to +52.6; the roster joined, every certificate +0.2 to +1.8. Realism: rural health units in the Philippines run with
one physician or none, nurses and midwives sign in the office's name, and a vacant post is filled by a nurse in charge
for months.

Main population zero-counts: the call's rows are the deaths dated 1 August 2015 to 30 April 2020, the census tables and
the tabulation; no 2022 death, birth or roster row is among them, every vacancy is after the interval, and the call
computed with the certifier, attendant and place-of-death columns blanked and no birth or roster row is the same
(asserted); every Layer 1 handling keeps the five or is loudly wrong (SF1 to SF16, L1 rows).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| births registered twice under a new number (D1) | A | -1.8 |
| twins removed by a mother-and-day dedupe (D1 over-clean) | A | +0.1 / -0.1 |
| late registrations of earlier births (D8) | A | -6.4 |
| births to other provinces' mothers (D5) | A | -0.4 (Kalinawan City) |
| office-title certificates signed by nurses and midwives (D7) | B | +52.7 |
| deaths registered a second time (D1) | B | +1.8 |
| the batch sent twice (D1) | B | +0.2 (Quezon) |
| fetal deaths (D5) | B | +3.2 |

Referee: the PHO roster for who held a physician's post; the child's names, date of birth and mother for one birth.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, Kalinawan City to Mabini | exact repeats dropped, mothers by residence, births dated in 2022, every certificate a birth | miss |
| Ask A, Libertad to San Miguel | the same | miss |
| Ask B, Kalinawan City to Mabini | exact repeats and second registrations dropped, the certifier read by the title written: MD, attending physician, MHO and CHO physicians, nurses, midwives and mayors not | miss |
| Ask B, Libertad to San Miguel | the same | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 0 of the 24 ask figures, and 0 when it also joins
the roster but counts every certificate; the over-cleaner (twins dropped with the doubles) keeps 2 of 24, Lc 0.083;
the mirror (stopped at the closed balance) keeps 0 of 24, Ls 0, and 15.4 of the 38 recommendation points (9 of 12
alerts, 4 of 12 completeness figures inside the interval).

Pair ceiling: 36.0 ((38 + 7 + 55 x 0.083) and (15.4 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each office's completeness of adult death registration, estimated with a death
   distribution method (the general growth balance of two censuses' age counts against the registered deaths above
   each age, carrying the net movement above each age); with hospital discharges or megawatt-hours in place of deaths
   there is no population ageing between two counts and no balance, and the task stops making sense.
2. Two layers: Layer 1 (residence spellings, Santa Cruz under its earlier name, registrations at the place of death,
   second registrations, a batch sent twice, fetal deaths, unstated and infant ages, late registrations, the census
   tables' printed layout) is neutral on the call: every handling keeps the five or is loudly wrong (SF1 to SF17, L1
   rows). Layer 2 is the movement carried into the balance, asserted alone to move the default path to the golden on the
   simulator's clean truth (R3a eight, R3b five).
3. No banned stump decides: nothing is planted (no completeness figure, earlier assessment or alert list ships, and
   no document names movement, migration or the balance's closure, R3c); not semantics (every field read right, the
   closed balance still files eight); not rule application (the ToR files D1's estimand and the 80 per cent alert and no
   method).
4. Gate G: no shipped artifact ranks the offices; the FHSIS reports set against the registrations flag two offices,
   neither the golden's pair, and most offices' registrations exceed them.
5. Determinism: the five hold under all 1,200 readings an office (flagged at most 0.675, the rest at least 0.818) and
   under synthetic extinct generations and the hybrid carrying the movement (flagged at most 0.774, the rest at least
   0.845), and by sex combined (SF17); completeness graded inside each office's interval; the asks' figures sit at least
   0.002 from a rounding edge; 17 fork rows asserted; the verifier recomputes by its own route and reads back every
   format the pack ships; two builds byte-identical.
6. Fingerprint: heart WARN (repeat.gate_g and repeat.decision against task470, repeat.question_form against task194,
   answered under Draw) after the role and organisation were redrawn; surface WARN only (Santa Cruz read as a person).
7. Judge (one isolated thread, Sonnet, medium, the bundle and the graded blocks only), pass 1: DETERMINISTIC with a
   minor SOLUTION_WRONG, FIX_NOW; the five forced under every variant it ran (person-years, fits, shift, not-stated
   spread, duplicate matching, window end, ranges); B1 reproduced exactly; Gate G method_or_model_selection,
   analytical_non_defect; Gate H domain, layers and decisive step pass. Its three findings were fixed in one pass: its
   whole-per-cent figures ran 1 to 2 points under the golden because the write-up's balance step had lost its
   definition of the persons reaching each age (it took the arithmetic mean; the step now states the geometric mean
   and the fit, and the arithmetic mean joins the readings, SF18); "no reading crosses 80" failed for a 5+ to 30+ fit
   (the accepted readings now start at 10+, over the full 25-range grid, asserted); C1 moved by up to 0.4 if a blank
   date of birth never matches (every second registration now carries its date of birth, SF19). Pass 2 on the fixed
   build: DETERMINISTIC, APPROVE; every completeness figure, B1 and C1 reproduced exactly; no reading of the grid moved
   an office across 80 (closest Mabini and Rizal at about 0.82); stump power strong and analytical; Gate G
   method_or_model_selection, analytical_non_defect; Gate H domain, layers and decisive step pass. Its optional note (a
   line saying the denominator is estimated from the censuses) is not taken: the ToR's "any other census output the
   review needs" already licenses the tabulation, and a sentence pointing at the censuses would point at the method.

## Leak check

`leak.py --asof 2023-11-06`: REVIEW, no LEAK. Each REVIEW line:
- Sweep 4, `DATA_DICTIONARY.md`, `README.md`, `cph2020_special_tabulation_cover_note.pdf`,
  `crvs_review_terms_of_reference_2023.pdf`: the shared terms are the field's nouns (population, office, residence,
  tabulation, provincial, registry); none names movement in the balance, a death distribution method or the closure,
  and R3c in checks.py asserts it for every document. Harmless.
- Sweep 6, the birth and death extracts: they name the offices on every row beside registry numbers, ages and dates;
  they are the registers themselves and rank nothing. Harmless.
- `guard.py surface`: "Santa Cruz" is read as a person (the city's name); WARN people.last on the surname Cruz against
  task97 is the same false reading. Harmless.

Reader (one isolated agent, Sonnet, medium, the prompt and the pack only): Q1 none (no sentence names the step; the
residence table was the file that pointed at it), Q2 none, Q3 none, Q4 none, Q5 the ToR's D1 fixes population, window
and comparison and leaves the denominator's method open, which is the design, Q6 an analytical choice; every REVIEW line
harmless. Fixed: the request now names the special tabulation by its purpose (the PDPFP update) and the file is
`cph2020_special_tabulation_pdpfp_kalinawan.csv`, so neither the file list nor the request points at movement; the
cover note still describes the table, as a census office's transmittal would. Its realism notes (offices outside the
province leading the extract's sort, the attendant codes in use) describe the registry's own layout and were kept.

## Tried and rejected

- The seed's dual-system estimate of a population register's undercoverage from a coverage survey (2026-10-18, before
  any file): capture-recapture traps are spent in the corpus (task448's second list within route strata, task196's
  second source fed by the first), and any heterogeneity or dependence trap would replicate one of them.
- Movers in a 60 to 75 age band (prototype, 2026-10-18): the closed balance bends visibly (residuals 3 to 6 per
  thousand against 0.2 with no movement) and its completeness swings from 0.71 to 1.29 with the fitted range, so a
  careful analyst sees the failure; dropped for movement that follows frailty, which keeps the line straight (residuals
  0.2 to 0.4 per thousand) while moving completeness 9 to 21 points.
- Completeness graded to one decimal with movers following mortality through the oldest ages (prototype, 2026-10-18):
  the census counts only movers who survived to 2020 and the oldest die soon after moving, so a receiving LGU's
  migration-adjusted completeness spread 0.78 to 0.91 across the movers' age conventions; the movers' rates follow
  mortality only to the late seventies, and completeness is graded inside each LGU's interval over the readings the
  method admits rather than at a fixed precision.
- The elders moving into the two peri-urban municipalities, so the closed balance also passed them wrongly
  (2026-10-18, stage 3): the census counts only the movers who survived to 2020, so every migration-adjusted method
  still read a receiving LGU high, and synthetic extinct generations and the hybrid put San Isidro at 0.80 to 0.87
  against the balance's 0.76, a valid method straddling the line; the elders now leave mostly for elsewhere in the
  country and a few for Kalinawan City, the offices below the line take in almost none, and every method carrying the
  movement files the same five with 2 points or more either side.
- The accepted range over lowest fitted ages from 5+ (stage 4, judge pass 1): the 0 to 4 group shrank between the
  censuses, so a fit starting at 5+ (5+ to 30+) put every office under 80; the readings now start at 10+, over every
  lowest age from 10+ to 30+ and highest from 55+ to 75+.
- The special tabulation named by its content in the file name and the request (stage 4, reader): the pack's file list
  and the request's inventory pointed at movement before any analysis; both now name it by the PDPFP update it was made
  for.
