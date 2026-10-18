# task243 design note

Architecture 1, wave 4, seed DQ16 (which local areas' register counts breach the undercoverage alert): the seed's
world (local areas' register counts), decision (which areas go into the register-improvement programme) and quantity
(how far a register falls short of what it should hold) only. The seed's register is a population register checked by
a coverage survey and its pitfall a dual-system estimate; capture-recapture traps are spent in the corpus (task448's
second list measured within route strata, task196's second source fed by the first), so the register becomes the civil
register of deaths, whose undercoverage the field measures with a death distribution method rather than a second
count. The Province of Kalinawan (fictional, in Mindanao, the Philippines) reviews the death registration of the local
civil registry offices (LCROs) of its component city and eleven municipalities between the 2015 census (POPCEN,
reference date 1 August 2015) and the 2020 census (CPH, reference date 1 May 2020); the offices that register fewer
than 80 per cent of their residents' adult deaths go into the province's 2024 civil registration improvement programme.

## Draw

Card `cards/task243.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, each answered here:
repeat.question_form (which, against task190 and task194): the decision is a designation of LGUs, and "which" is the
form a designation takes. test.same_puzzle_older (task450 v2) and test.same_driver_older (task129 v2) are
differentiated on the card; the nearest driver is task181 v2 at 0.07.

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
- **Shape.** 07, a grid of cells: one row per LGU with its registered adult deaths in the interval, the completeness
  estimated and the alert, beside the LGU's columns for the asks (12 rows, the call picked per row), the designated
  set, the chart (each LGU's completeness against the 80 per cent line, the designated LGUs marked) and the two files:
  well over 25 criteria before the rubric folds them. Decision designation_set, answer set_of_items, question form
  which.
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
  local_government (the provincial government's planning and development office with the LGUs' civil registry
  offices). All clear the last three.
- **People** (`guard.py names --locale fil_PH --seed 243`, chosen from the draw for names common in the Philippines):
  Nicole Gomez, the provincial planning office's population officer, who runs the review for the committee; Randy
  Cortez, the civil registrar of Kalinawan City, who chairs the committee's technical working group; Casey Carrillo,
  the provincial statistical office's officer who handled the census tabulation request; Steven Jimenez, the provincial
  administrator, who chairs the committee.
- **Deliverables.** `lcro_death_registration_completeness_2015_2020.xlsx` (each LGU's row: registered adult deaths in
  the interval, completeness estimated, alert, and the asks' columns) and `crvs_committee_note_2023.docx` (the
  committee note, with one chart: each LGU's completeness against the 80 per cent line, the designated LGUs marked).
- **As-of.** Monday 6 November 2023: the census office released the 2020 census's age and sex tables in 2022 and the
  special tabulation of residence five years earlier for the province in October 2023, the civil registry extract was
  taken on 31 March 2023, and the committee meets on 21 November to name the offices for the January rollout. The call
  is retrospective by nature (completeness is measured between two censuses, and 2015 to 2020 is the latest pair); what
  it settles is which offices go into the 2024 programme.
- **Data-native sentence.** Kalinawan's oldest residents leave the farming municipalities for their children's
  households (in the peri-urban municipalities around the city, and for one municipality mostly in Metro Manila) at
  rates that rise with their frailty, so each place's population above every age changes between the censuses by
  movement as well as by death, in proportion to its deaths; the growth balance taken as closed keeps its straight line
  while its slope reads the departures as unregistered deaths and the arrivals as registered ones, and only the 2020
  census's question on where each person lived on 1 May 2015 carries the movement into the balance.

Sources, one line each (what it teaches; how this build differs):
- Hill (1987), the general growth balance: completeness of death registration relative to two censuses from the
  birthday rate less the growth rate above each age against the registered death rate above it; here the population is
  open, and the field's repair is the build's decisive step, never named in the pack.
- Hill and Queiroz (2010), adjusting the general growth balance for migration (applied to Brazil's states): the net
  migration rate above each age enters the balance; here the movers are the oldest residents, whose movement follows
  their mortality, so leaving it out moves the slope without bending the line.
- Bennett and Horiuchi (1981), synthetic extinct generations, and the hybrid of Hill, You and Choi (2009): the other
  death distribution methods, which share the closure assumption; a rung, never the answer.
- Moultrie and colleagues, Tools for Demographic Estimation (IUSSP, 2013), the death distribution chapters: the
  textbook route a careful analyst follows (fit over the ages that sit on a line), which is the default path here.

## Default path

1. Read the two censuses' household population tables by LGU, sex and five-year age group (2015 POPCEN and 2020 CPH,
   both on the 2020 boundaries).
2. From the civil registry extract keep the deaths of each LGU's usual residents aged 15 and over that occurred from
   1 August 2015 to 30 April 2020, as registered by 31 March 2023: placed by usual residence, a record transmitted twice
   counted once, non-residents and fetal deaths out, unstated ages spread pro rata.
3. Fit Hill's general growth balance for each LGU (the birthday rate less the growth rate above each age against the
   registered death rate above it, over ages 15+ to 65+ or a range trimmed for the young adults' labour moves,
   orthogonal fit), the population taken as closed; completeness is the fitted ratio, adjusted for the two censuses'
   relative coverage.
4. Flag each LGU under 80 per cent.

Ends on: six LGUs flagged (Esperanza, Magsaysay, Santa Fe, Libertad, San Luis, Del Carmen): the three farming
municipalities whose oldest residents leave read about 70 to 75 per cent, and the two peri-urban municipalities the
oldest move into (Santa Cruz, San Isidro) pass at about 84 to 87 (planned values, confirmed at stage 2).

Golden: five LGUs flagged (Santa Cruz, San Isidro, Libertad, San Luis, Del Carmen), from the same balance carrying each
LGU's net movement above each age: the persons in the LGU in 2020 who lived elsewhere on 1 May 2015, less the persons
anywhere in the country in 2020 who lived in the LGU then, from the census office's special tabulation.

## Stump sentence

A competent demographer fits the general growth balance to each LGU's 2015 and 2020 census age counts and its
registered adult deaths with the population taken as closed, as the method is set out, finds every fit a clean
straight line and ends on six LGUs flagged, the three farming municipalities whose oldest residents leave (about 70 to 75
per cent) and the three remote ones, while passing the two peri-urban municipalities the oldest move into (about 84 to
87); the step that lands it there is leaving the oldest residents' movement out of the balance, which reads each
departure as an unregistered death and each arrival as a registered one, so only the balance carrying the 2020
census's count of who moved above each age gives the five.

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
- **Layer 1:** the civil registry extract (keyed by registering office, the component city's records before its 2019
  conversion under the municipality's old name) carries late registrations entered months or years after the death
  (the 2020 lockdown's backlog among them), deaths registered where they occurred (the provincial hospital's office
  holding other LGUs' and other provinces' residents), records transmitted twice from the hospital office to the
  residence office, fetal deaths, and unstated ages or infants' ages in months, days or hours; the census tables are on
  the boundaries of their day. Each is produced by the system that records it; none is placed to be caught, and the call
  is the same under every handling of each (SF rows in checks.py).
- **Layer 2:** field_method: the death distribution method carried for an open population, the net movement above each
  age from the census's residence question put into the growth balance, against the balance taken as closed.
- **Decisive step:** carrying each LGU's net movement above each age into the growth balance, so that the population
  the balance reads between the censuses changes by entries, deaths and movement, rather than fitting the balance with
  the population taken as closed (over any age range, or with any other death distribution method that shares the
  closure).
- **Not semantics:** reading every field right (usual residence, date of death, date of registration, age units, the
  census tables, the residence five years earlier) still leaves the closed balance on six LGUs flagged: the census's
  residence question is plain, and reading it right does not say that it belongs in the balance or how it enters.
- **Not rule application:** the province's review terms file what completeness is (the registered share of the deaths
  of the LGU's usual residents aged 15 and over in the interval) and the 80 per cent alert; no filed rule or procedure
  says how the deaths that should have been registered are estimated, so executing every stated rule with the textbook
  closed balance files the wrong six.
- **Analyst test:** a strong analyst who reads every file right and applies the alert as filed fits the general growth
  balance with the population taken as closed (as the textbook sets it out, over the usual ages or a trimmed range),
  sees straight lines and flags six LGUs, three of them wrongly, while passing the two peri-urban municipalities; on the
  simulator's clean truth the same route files the same six and the decisive step alone gives the five (rows in
  checks.py).
- **Estimand:** the province's review terms (`crvs_review_terms_of_reference_2023.pdf`) define completeness: the
  registered deaths of the LGU's usual residents aged 15 and over that occurred from the 2015 census reference date to
  the day before the 2020 census reference date and were registered by 31 March 2023, as a share of all deaths of those
  residents in that interval, residents counted at their usual residence at death, those who moved in included; the
  alert is completeness below 80 per cent, reported to the nearest 5 per cent.
- **No decoy:** nothing is planted: no memo, earlier assessment or stakeholder figure argues a method or an office; the
  census tables and the special tabulation are the census office's products, the extract is the registry's own, and no
  file ranks the offices on completeness.
- **No certified replay:** no certified or published completeness for 2015 to 2020 exists for a method to reproduce;
  the method is found from the data's structure (the censuses, the deaths and the census's own residence question).
- **Lesson:** a death distribution method reads each age group's shrinkage between two censuses as deaths, so where the
  oldest residents move at rates that follow their frailty the shrinkage includes the movers while the diagnostic line
  stays straight, and the balance has to carry the census's own count of who moved; no build on file uses a demographic
  balance or a death distribution method (task231 and task230 carry late exits and a late channel, task242 a detector
  fading with time).

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
  mortality only to the late seventies, and completeness is reported to the nearest 5 per cent, the precision a death
  distribution method carries.
