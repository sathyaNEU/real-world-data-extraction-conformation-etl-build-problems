# task308: which network gets the 300 e-bikes, and the net fare revenue a year they add

Architecture 1, drawn 2026-10-25 (wave 7, Opportunity Sizing & Decision Support, perssathya; the author allowed a third
build in flight). Seed OS10's world, decision and quantity are kept (a city bike-share operator, e-bikes for one of five
districts, the net fare revenue a year they add); the seed's mechanism rows are decoy-era design and were not used, and
the pitfall was re-found from the data. The seed's 600 e-bikes became 300 at the build: 600 is more than any of the
five networks' classic fleets and read as a planning error.

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task308.json`, architecture v1 |
| Pairing | Product Analytics / churn-propensity-uplift-modeling / Opportunity Sizing & Decision Support |
| Niche | which of a bike-share operator's five classic networks gets 300 e-bikes and the net fare revenue a year they add, when the busiest network's stations rarely run dry and the campus network's residence-hall hubs run dry at every teaching-weekday class change |
| Call | the network that gets the e-bikes, and every network's net fare revenue a year, to the nearest USD 25,000 |
| Decision | `pick_one_of_n`, answer unit `named_option` (with its USD figure) |
| Mechanism | gap population then objective; pattern none; generators G7 (decisive: the seconds each station held no bike, pinned only by the flows in and out and the 03:00 audit), G12 (a station with no undock while empty is a non-answer, not zero demand) |
| Gate G | `method_or_model_selection`: which requests count as the e-bikes' added rides |
| Strategy | `informative_censoring`; layer 2 family `estimation_fit`, own pattern: served rides censored by empty stations |
| Calibration | `parallel_run_overlap` (the 2025 pilot: 24 Harbour stations with e-bikes beside 12 matched classic-only stations for the whole year) |
| Furniture | forum `board_of_directors`, forcing event `season_or_peak` (the order by 15 January 2027 for the 1 April season opening), organisation `software_or_platform` (the bike-share operator), role `product_manager`, context artifact `monitoring_export` (the 03:00 audit) |
| People | Joseph Graham (e-bike product lead, the paper's author), Gina Wells (director of operations, the pilot note's author); drawn with `guard.py names --geo usa --seed 308` |

**Data-native sentence.** A bike-share ride exists only when a rider meets a station holding a bike, so the trip record
is demand censored by each station's stock; University's two residence-hall hubs are drained by the morning class
change and stay short until the 14:00 van, so its noon and afternoon requests leave no row, while Central's four daily
van runs keep its stations stocked and its record close to its demand.

**Guard.** `guard.py check` on the card: WARN, no BLOCK. `repeat.gate_g` (method_or_model_selection, as task485 and
task269): the honest key, since the decisive step chooses which requests the e-bikes add. `repeat.decision`
(pick_one_of_n, as task303) and `repeat.question_form` (which): the seed's decision is a pick of one network.
`test.same_driver_older` against task271 v2 and task471 v1 (both lineage), and the signature lines against task199,
task268 v2, task196 v2, task255 v1 and task305, each differentiated on the card. The forcing event `launch_or_rollout`
and the calibration form `pilot_log` were barred against the live window; `season_or_peak` is the honester label (the
deadline is the riding season), and `parallel_run_overlap` names what the pilot is (e-bike stations run beside matched
stations over the same year). Nearest driver 0.06. Stage 3: `guard.py heart` WARN with no BLOCK (the draw's three
repeats, and `repeat.deliverables`, docx and xlsx as task301 v2: a board paper with the workbook behind it is the
forum's genre); `guard.py surface` promoted one pair, task160 at 0.102 (a hospital cooperative's agency-nurse block,
forecasting), which shares only a Layer 1 habit, a mid-year system switch in the records, and no driver, domain or
objective; the persona screen's Dock St and Marina Dr are station streets and Harlan Velo the vendor, not people.

**Abstraction test.** Stripped of nouns: a launch's added revenue is sized from the existing product's requests, the
record holds only the requests the existing supply met, and the candidate whose supply runs out at every peak hides the
most requests. Against task302 (lost sales while a product is unavailable, net of what goes to a substitute): there the
record overstates the loss; here it understates the demand, and no substitute exists, since the two hall hubs run dry
together. Against task305 (occupants counted at homes outside the area): there a population sits outside the record's
base; here every rider is in the base and only the requests made at an empty station are missing.

**Call-only probes (2026-10-25, the draw pack at scratchpad `t308/probe`).** Both isolated probes (sonnet and opus at
medium, prompt and pack only) named Central: sonnet at USD 270,000, opus at USD 100,000. Both rebuilt the pilot's
e-bike stock and found the choice share when an e-bike is docked; neither rebuilt the networks' classic stock. Both
flagged that Central could not hold the e-bikes and that pilot e-bikes were ridden to the matched stations: fixed at the
build (charging points come with the e-bikes; an e-bike can only be returned to a pilot station; Harbour, the pilot
network, is not a candidate).

**Sources, one line each.**
- `layer2-rigor-patterns.md`, churn-propensity-uplift-modeling #1 and #4 (target persuadables; rank by effect, not by
  treated response): the board's net fare revenue is an uplift, and the network with the most riders is where the
  e-bikes mostly convert riders who ride anyway; this build's step is the censoring that hides the persuadables.
- The shared-mobility literature's censored-demand estimate (requests per minute a station held a bike, carried to the
  minutes it was empty): the field's own estimator, run here on station-level stock rebuilt from the operator's records.
- task302 (stockout diversion) and task305 (an omitted population), differentiated above.

## Default path

1. Read the board paper, the pilot note, the fare schedule and the four trip exports; put the trips on one footing.
2. The pilot: at the 24 pilot stations 41.7 per cent of rides went on an e-bike, the pilot stations drew 4.4 per cent
   more rides than the comparison stations, and an e-bike ride paid USD 0.11 more than a classic ride.
3. Carry that to each network's 2025 rides: 4.4 per cent more rides at the classic fare, and 41.7 per cent of them at
   the e-bike premium; Central has the most rides.
Ends on: Central, about USD 50,000 a year.
Golden: University, USD 125,000 a year.

## Stump sentence

A competent analyst carries the pilot's e-bike share and new-rider uplift to each network's 2025 rides and names Central
at about USD 50,000 a year, because the trip record holds only the requests that found a bike: University's
residence-hall hubs run dry at every teaching-weekday class change and stay short until the afternoon van, so about
29,600 of its 2025 requests leave no row, and the requests rebuilt for its empty seconds (from each station's stock,
rebuilt from the 03:00 audit, every undock and dock and every van move, and its requests per stocked second) put
University first at USD 125,000 a year.

## Three rules

Task type: churn-propensity-uplift-modeling (product-analytics), which serves Opportunity Sizing: the call sizes the incremental fare revenue a product launch adds against the existing product, from a pilot's uplift carried to each candidate's demand.
Domain test: the deciding quantity is a launch's uplift against the existing product (the e-bike rides that are new, against the ones that only convert a classic ride), measured as product analysts in shared mobility measure it, from trip logs whose usage is censored by availability: a docked-bike service records a request only when the station holds a bike, so demand is rebuilt from each station's stock and its requests per stocked second.
Swap: "University gets the e-bikes because its hall hubs turn away the class-change requests the trip log never shows" with hospital beds and admissions in place of stations and rides reads as a capacity question with no launch, no product being converted against another and no stock moving between stations through the day; with a retailer it loses the station-by-station flows that empty one hub while filling another, which is what hides the requests here.
Layer 1: second-stamped trip exports from two trip systems across the 1 July platform switch (station names against station codes, legacy against new account ids, fares in dollars against cents, local time with the repeated November hour), the dispatch log in UTC, the 03:00 audit as a fleet-audit workbook, GBFS station and region feeds, false starts (an undock put straight back) in the trip exports, the City's open-data counts with small cells suppressed; nothing placed to be caught.
Layer 2: estimation_fit, censoring: the requests a network would make of the e-bikes are its rides plus the requests its empty stations turned away, and the turned-away requests are estimated from each station's rebuilt stock and its requests per stocked second in each month, day type and hour.
Decisive step: treat each network's rides as demand censored by station stock, rebuild every station's classic stock second by second from the 03:00 audit, the undocks and docks and the van moves, and add the requests its empty seconds turned away before carrying the pilot's uplift.
Not semantics: every field can be read correctly (what a ride is, what a van move is, what the audit counts) and the analyst still takes the network's rides as its demand, because no field, flag or document says a request was turned away; only the rebuilt stock shows the empty seconds.
Not rule application: no filed rule says how to count requests; the board paper files the estimand (the fares riders would pay with the e-bikes less the fares they paid in 2025, at 2025 demand) and the deployment, and nothing names censoring, stock or empty stations. Enumerated family: rides served, the pilot uplift per station or per e-bike, whole empty hours imputed, ten-minute steps imputed from the steps that start stocked, one rate per network and cell, a year-round rate per station, and the requests per stocked second by station, month and day type or by day of week or by teaching and break months; the enumerated spread on University's figure runs USD 32,270 to 132,059 and names Central or University. Standing family (the constructions the data leaves defensible, those that count turned-away requests at each station's own rate in cells the data shows homogeneous): seven constructions and the simulated e-bike world, USD 123,817 to 132,059 on University, all at USD 125,000 and every other network in one bin each (margins USD 5,143 to 10,791, asserted). The ruling-out is quiet: no column or clause eliminates the rides-served route; only the rebuilt stock does, and the lower censoring rungs are ruled out by the record itself (month-to-month rates, station-to-station rates and the stock dropping to zero inside ten-minute steps).
Analyst test: the easy route, the pilot's e-bike share and new-rider uplift carried to each network's 2025 rides, names Central at about USD 50,000 a year (the default path's Ends on), against University at USD 125,000.
Estimand: the board paper extract, section 2: each network is judged on the net fare revenue the e-bikes would add there in a year, the fares riders would pay in that network in a year with the e-bikes less the fares they paid in that network in 2025, at 2025 demand; section 3 files the deployment (every station holds e-bikes through the day).
No decoy: nothing is planted; no document argues for a network, carries a figure for one or ranks them; the City's open data counts rides by area, the same quantity the trip exports give, and is a declared distractor with the vendor's quotation.
No certified replay: no certified or published figure is shipped for a method to be recovered from; the golden is built from the trips, moves and audit.
Lesson: usage records of a capacity-limited service are demand censored by the capacity, so sizing a launch on recorded usage sends it where supply already meets demand; a model learns to rebuild the supply from the flows and count the requests the empty moments hid, which no build on file teaches for station-based stock.

## Readability screen

| Rung | What it needs | Verdict |
|---|---|---|
| the pilot's uplift on each network's 2025 rides (default path) | the trip exports, the pilot note's station table, the fare schedule | readable |
| the pilot's uplift on each network's 2025 fares | the same | readable |
| whole hours a station stood empty, imputed at its own hourly rate | the rebuilt stock read at hour grain | readable |
| ten-minute steps starting empty, imputed at the mean undocks of steps starting stocked | the rebuilt stock read at ten-minute grain | readable |
| requests per stocked second by station, month, day type and hour, carried to the empty seconds (decisive) | every undock and dock in four exports from two trip systems, every van move in UTC, the 03:00 audit; no column, flag or sentence anywhere says a station was empty or a request turned away | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | net fare revenue | the fares with the e-bikes less the 2025 fares, at the network | the e-bikes' gross fares | another figure | the board paper, section 2: less the fares they paid in that network in 2025 |
| SF2 | at 2025 demand | 2025's requests: the rides plus the requests empty stations turned away | 2025's rides | Central at 50,000 (the stump) | the record: the rebuilt stock shows stations empty while riders came; demand is not rides |
| SF3 | a year | calendar 2025's requests | another window | none shipped | the exports cover 1 January to 31 December 2025 (asserted) |
| SF4 | the fares | each ride billed as the fare schedule bills it: USD 1.00 and each started minute at 0.12 or 0.17 | another basis | same call | the fare schedule; every fare in the exports bills as filed (asserted) |
| SF5 | the e-bike share | the share of rides from pilot stations taken on an e-bike | the share among rides with an e-bike docked | same call | an e-bike is docked at a pilot station for all but a sliver of the year (asserted) |
| SF6 | the new-rider uplift | the rides a pilot station drew over the rides a comparison station drew, less 1 | the mean of per-station or daily ratios | same call and figures | asserted (the 18-cell grid) |
| SF7 | the classic fare | the network's mean classic fare | the pilot's or the system's | same call and figures | asserted (the 18-cell grid) |
| SF8 | the uplift's base | demand (rides plus turned-away requests) | the rides served | same call and figures (University 123,817) | asserted (the 18-cell grid) |
| SF9 | rounding | the network figure rounded once | the parts rounded first | same | asserted |
| SF10 | false starts | not a ride and not a request (the dictionary) | counted as rides | same call and figures | the data dictionary's Read me; asserted (R2b) |
| SF11 | a rider who prefers a classic bike when none is docked | takes an e-bike at the pilot's share of rides | the simulated e-bike world | same figure (University 130,349) | asserted (the simulation rounds to USD 125,000) |
| SF12 | the pilot's stations | the 24 pilot and 12 comparison stations in the pilot note's table | other Harbour stations | none | the pilot note (asserted) |
| SF13 | every request served with the e-bikes | every station holds e-bikes through the day | e-bikes running out | none shipped | the board paper, section 3 |
| SF14 | ask A, people | one person per rider: accounts on one card riding through the same months stay two, an account opened after another's last ride on the same card joins it | one per account; one per card | 9,810 and 9,413 on Central | the prompt asks for people; the register's card and opening dates (asserted) |
| SF15 | ask A, living in | the account's home_area, case and spaces set aside | where they ride | other figures | the dictionary: where the rider lives, as given at sign-up (asserted) |
| SF16 | ask A, rode with us in 2025 | at least one ride; false starts are not rides | any undock | 9,824 on Central | the dictionary's Read me (asserted) |
| SF17 | ask B, each month | the local month of plug-out | the UTC month | 233 for January | the dictionary: a session counts in the local day its plug-out falls (asserted) |
| SF18 | ask B, zero-energy sessions with a repeated register | kept or dropped | the other | same twelve figures | asserted (they carry no energy) |
| SF19 | ask C, each quarter | the local quarter of opening | the UTC quarter | same eight figures | the dictionary: reporting quarters run on Central Time (asserted: no job opens in another quarter by UTC) |
| SF20 | ask C, workshop jobs | every job card but a repair's road-test retest, scrapped bikes included | returned-to-service jobs only | other figures | a scrapped bike's job is a job (asserted) |
| SF21 | ask C, rides | the rides of that class in that quarter, false starts out | every undock | 52.6 for e-bikes Q1 (with every job) | the dictionary's Read me (asserted) |

## Ladder

| Rung | Construction | Central | University | Call |
|---|---|---|---|---|
| R0 | the pilot's uplift on each network's 2025 rides (default path) | 52,366 | 32,270 | Central at 50,000, clear by 20,096 |
| R1 | whole hours a station stood empty imputed at its own hourly rate | 53,464 | 32,688 | Central at 50,000 |
| R2a | ten-minute steps starting empty imputed at the mean undocks of steps starting stocked | 74,490 | 101,099 | University at 100,000 |
| R2b | one rate per network and cell | 69,994 | 88,082 | University at 100,000 |
| R2c | requests per stocked second without the month | 72,392 | 91,086 | University at 100,000 |
| R3 | requests per stocked second by station, month, day type and hour (golden) | 76,296 | 127,804 | University at 125,000, clear by 51,508 |

R0 is the stump; R1 is the solver who looks for empty stations at hour grain and finds almost none; R2a to R2c count the
turned-away requests with a construction the record refutes (ten-minute steps that start stocked and empty part way,
hall hubs and class hubs pooled, term months pooled with the summer). Every rung is asserted in checks.py.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every request at the network's stations in 2025, whether or not a bike was there, plus the requests the e-bikes draw | filed WHAT (the board paper: at 2025 demand); the construction is the stump |
| 2 | Unit of account | the network; USD of fares a year | filed (the prompt, the board paper) |
| 3 | Attribution window | calendar 2025 | filed (the exports' year; the board paper) |
| 4 | As-of dating | the 2025 exports; the GBFS feeds as at 1 November 2026 | filed (the dictionary) |
| 5 | Version basis | the 2025 fare schedule | filed |
| 6 | Denominator | stocked seconds per station and cell | C1 (seven constructions and the simulation, one bin each, asserted) |
| 7 | Weighting | each station's own rate | C1 (pooled by network is a refuted rung, asserted) |
| 8 | Window length | month, teaching or break months, or day of week within month | C1 (asserted) |
| 9 | Boundary inclusivity | an undock before a dock in the same second; the 03:00 count after that second's events | asserted (no station below zero) |
| 10 | Rounding path | the network figure rounded once | asserted (SF9) |
| 11 | Tie-break | none | asserted (51,508 clear) |
| 12 | Maturity and censoring | the censoring is the stump; no immature period | the construction |
| 13 | Order of operations | stock, rates, turned-away requests, then the revenue | the construction |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | none in the call's files; ask A's re-registrations, ask B's re-sent sessions and ask C's retests sit in the asks' files only | asserted (separation) |
| 16 | Identity normalisation | station names and codes through the GBFS feed; legacy account numbers through the register; bike numbers across three formats (the dictionary) | asserted (every join resolves) |
| 17 | Netting against gross | the 2025 fares netted | filed (SF1) |
| 18 | Dimensional units | seconds, rides, requests, USD, cents, Wh and kWh, jobs per 10,000 rides | units in the data, the dictionary and the prompt |
| 19 | Code and status semantics | classic and electric, CLASSIC and EBIKE; the audit's columns | the dictionary; never the stump |
| 20 | Integerisation | asks rounded once (whole people, whole kWh, one decimal) | filed (the prompt) |
| 21 | Clause scope | the deployment premise applies to the chosen network's stations | filed (the board paper, section 3) |
| 22 | Forward window contents | a year at 2025 demand with every request served | filed (the board paper, sections 2 and 3) |

## Literal reader

Executing the prompt and every filed sentence word for word (the board paper's sections 1 to 4, the pilot note, the fare
schedule, the dictionary) leaves one open move on the call: how many requests each network made in 2025. The board paper
files the measure at 2025 demand and every station holding e-bikes through the day, the pilot note files which stations
ran the pilot, the fare schedule files the fares, and every construction that counts the requests each station's empty
seconds turned away, at that station's own rate in a homogeneous cell, files University at USD 125,000 and every other
network in one bin (seven constructions and the simulated e-bike world, asserted); the rides-served answer comes from an
easy method on the same literal estimand, never from another reading of it. Each differing reading of a term (SF1, SF2,
SF10, SF13 to SF21) violates a quotable shipped sentence or the record.

## Oracles

None on the call: no file ties only under the golden and no past deployment is shipped. The City's open data counts
rides by area and month, the same quantity the trip exports give (small cells suppressed), and ties under every handling;
the pilot's comparison stations give the uplift on rides, which the rides-served route and the golden both use. On the
asks, nothing ties only under the golden: the account register's card fingerprints tie a re-registration and a
household alike, the charging export's energy column equals its register difference on every row, re-sent rows
included, and the workshop's job cards carry no retest flag; no total, control or published figure is shipped for any
ask.

## Ask sheet

**Ask A: the people who rode with us in 2025 living in each of the five network areas (5 figures, whole people).** H18:
the board paper's launch plan offers the e-bikes first to the riders who live in the chosen network's area; the call
reads none of the account register (asserted). Use: the launch offer's mailing. Primary device, silent (D7, the true key
elsewhere, with its over-cleaning half): a rider who loses access to an account signs up again with the same card, and
the old account stays open in the register; only its last ride before the new account's opening says the two are one
person. Interior: households pay for two riders' accounts with one card, and both ride through the same months, so one
person a card merges real people. Hazards: the 1 July platform switch (January to June rides carry legacy account
numbers), home areas typed in mixed case on the old sign-up form, false starts. Files: the four trip exports, the
account register (5 files, 10 columns). Stops (Central, University, Riverside, Old Town, Hillcrest): one person an
account 9,810, 5,078, 7,999, 5,272, 3,383; one person a card 9,413, 4,793, 7,709, 5,064, 3,232; legacy numbers left
unmapped 13,617, 7,712, 10,383, 7,187, 4,785; false starts as rides 9,824, 5,080, 8,007, 5,280, 3,389; golden 9,486,
4,853, 7,759, 5,102, 3,258. Realism: an operator CRM that opens a new account rather than recovering an old one.

**Ask B: the energy the Harbour pilot's charging points delivered in each month of 2025 (12 figures, whole kWh).** H18:
the deployment's electricity line, priced from the pilot's energy a month; the call reads none of the charging export
(asserted). Use: the power budget for the chosen network's charging points. Primary device, silent (D1, a replay under
fresh ids beside genuine sessions): after a restart a station controller re-sends the sessions still in its buffer under
new session ids, stamped from a clock it saved hours before the restart; only the point's energy register, repeating an
interval already delivered, says the session is a re-send. Interior: three controllers were replaced during the year
(the first in January) and their registers start again near zero, so a register-must-rise filter drops every later
session at those stations.
Hazards: UTC stamps against the local month of plug-out, zero-energy sessions with equal register readings. Files: the
charging export, the dictionary (2 files, 9 columns). Stops (January to December): every session 233, 237, 339, 393,
434, 460, 497, 487, 427, 405, 309, 244; a register-must-rise filter 207, 209, 301, 340, 382, 387, 422, 415, 359, 324,
248, 194; every session by UTC month 233, 238, 339, 392, 433, 461, 497, 488, 426, 407, 308, 244; golden 212, 220, 316,
357, 401, 426, 461, 451, 398, 374, 283, 224. Realism: a charging backend whose controllers re-upload their buffer after
a power cut with the clock they saved at the last sync.

**Ask C: the workshop jobs per 10,000 rides on e-bikes and on classic bikes in each quarter of 2025 (8 figures, one
decimal).** H18: the deployment's maintenance line, priced from the e-bikes' jobs per ride against the classic fleet's;
the call reads none of the workshop export (asserted). Use: the maintenance budget and the spares order. Primary device,
silent (D1, a resubmission that opens a second case): a repaired bike that fails its road test is booked as a new job
card on the same fault, the first card closed as returned to service; only the trip exports, showing no ride between the
first card's close and the second's opening, say the second is the same repair. Interior: intermittent faults come back
within a ride or two of a real return to service, so genuine repeats on the same fault fall inside the retests' 40
hours and no time window separates the two (74 genuine repeats inside it, asserted). Hazards: three bike-number formats
across the trip systems and the workshop, false starts in the ride counts, UTC stamps against local quarters. Files: the
workshop export, the four trip exports, the dictionary (6 files, 12 columns). Stops (e-bikes Q1 to Q4, classic Q1 to
Q4): every job 53.2, 32.8, 50.7, 29.6, 14.0, 16.3, 16.9, 11.2 (the same by UTC quarters); one job a bike and fault
within 30 days 36.9, 23.3, 31.2, 22.5, 9.2, 10.6, 10.9, 7.7; repeats within 24 hours dropped 49.1, 31.9, 47.6, 26.0,
12.4, 14.8, 15.7, 10.3; within 48 hours 47.8, 29.4, 41.4, 26.0, 11.5, 12.8, 13.7, 9.6; false starts as rides 52.6,
32.5, 50.0, 29.2, 13.9, 16.1, 16.7, 11.0; golden 49.1, 31.9, 46.8, 26.0, 12.0, 14.3, 15.2, 10.2. Realism: a job system that cannot reopen a closed card.

Main population zero-counts: the call reads the trip exports' times, stations, bike types and fares, the dispatch log,
the audit, the station feeds, the pilot note, the fare schedule and the board paper, and none of the account register,
the charging export or the workshop export; the asks read those and the trip exports' account and bike columns (asserted,
separation: the call's figures are unchanged with the asks' files and both distractors deleted).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A people by home area | 0 of 5 on one person an account, one a card, unmapped legacy numbers or false starts as rides | miss |
| B charging energy by month | 0 of 12 on every session, by UTC month or on a register-must-rise filter | miss |
| C workshop jobs per 10,000 rides | 0 of 8 on every job, a 30-day window, false starts as rides or UTC quarters; 3 of 8 at best (the e-bike cells) on a 24-hour window after meeting the device | miss |

Pair ceiling: 35.8 ((51.6 + 19.9) / 2), the cracker on the call keeping the best path on each ask (3 of the 25 ask
figures, a window repair counted against it) and the mirror on the rides-served call (Old Town's USD 25,000 the one call
figure it keeps) taking the same ask paths, since the asks read no file the call reads.
Mirror leakage: 12.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

## Tried and rejected

- 2026-10-25, before the pack: the seed's own step (cannibalisation measured on flat streets carried to a hilly
  district) is a visible-state stratification on elevation, which the probes on this lane land by reflex; a
  station-level pilot comparison missing members who switched stations is a contaminated comparison, found by both
  probes on task304; battery swaps capping a hilly district's rides are handed over by battery columns. Set aside on paper.
- 2026-10-25, stage 2: twenty small University stations; per-station cells by day of week within month overshot the
  turned-away requests by 13 per cent (a station's stocked seconds and empty seconds move together when a few bikes
  drain), so the family forked; five large hubs (two residence halls, three class hubs) cut it to 3 per cent.
- 2026-10-25, stage 2: the graded figure to the nearest USD 10,000; the standing family on University spans about USD
  8,000 (induced riders on the rides served, day-of-week cells, the simulated e-bike world), so no seed holds it in one
  10,000 bin; 25,000 holds every network with USD 5,000 to spare.
- 2026-10-25, stage 2: per-station 2024 trips as a distractor; it licenses a difference-in-differences reading of the
  pilot that moves the uplift by a point and University's figure by USD 6,000. Dropped for the vendor's quotation.
- 2026-10-25, stage 2: the operations director's line that the e-bikes should go where the riders are, in the board
  paper; a stakeholder view pointing at the wrong answer reads as a planted decoy. Cut.
- 2026-10-25, stage 2: billing ZIP codes with a lookup for ask A; any real ZIP ties the invented city to a real one. The
  register carries the rider's home area from sign-up instead.
- 2026-10-26, stage 2: road-test retests reopened within 90 minutes only; a one-day window repair then lands the golden.
  Retests now reopen up to 39 hours later and intermittent faults come back within a ride or two, so no window separates
  them from genuine repeats.
- 2026-10-26, stage 3: the e-bike crew's moves on a 15-second grid, every charging session taking the lowest free point and
  192 sessions plugged in at local midnight on 1 January read as generated; the crew's pace, the point a rider picks and
  the New Year's Eve plug-ins now come from their own stream, and no call figure moved.
- 2026-10-26, stage 3: the 03:00 audit showed each station at its par on 92 per cent of mornings, a constant stream; the
  night crew now leaves a station a bike or two off par when the van runs short, and the call's figures moved by under
  USD 200 (University USD 127,946 to 127,804).
- 2026-10-26, stage 3: the first controller replacement in April; with the points re-drawn, a register-must-rise filter
  landed two of the three months before it. Moved to January, the filter misses every month.
- 2026-10-26, stage 4: architecture 1 spent. Both isolated scored readers (sonnet and opus at medium, prompt and pack
  only) rebuilt each station's classic stock from the 03:00 audit, the trips and the van moves, imputed the requests the
  empty seconds turned away and named University (USD 100,000 on station x day x hour-by-weekend cells; USD 125,000, the
  golden, on station x hour x day type x term cells): demand censored at empty stations is the field's textbook estimate,
  and a pack holding the audit and the dispatch log makes it executable. Both landed ask B (the re-sent sessions by their
  repeated registers) and neither ask A (one person a card) nor ask C (every job card). The judge thread returned
  NOT_DETERMINISTIC, SEND_BACK on Gate C (the estimation grain and the e-bikes' new riders unfiled in the measure; the
  person and job definitions in asks A and C), Gate G analytical_non_defect and Gate H pass. Realism tells the readers
  named: the inventory closing to zero on every station-day, one par per network at the 03:00 audit, Harbour's flat
  per-station rides, trip durations and the e-bike share flat across networks, hours and distances, the pilot note issued
  in January in the past tense, the pilot stations' capacities against the 5 per cent match. Re-root at stage 1.
- 2026-10-26, re-root screen (scratch t308v2): the pilot's comparison stations ran dry too, so the ride-based uplift
  double counts the relief; call-only probe B (opus) found the comparison stations' empty hours and measured the uplift
  on demand (University at USD 125,000). Any stump that runs through censoring or stock in this world is spent.
- 2026-10-26, re-root concept readers (opus, medium, scenario text only): household interference in an
  account-randomised retention trial, appraisal-smoothed private-fund returns, first-round against repeat screening
  yield. Each reader took the named textbook move at once (household-level contrasts, Geltner desmoothing, first kits
  split from repeats). Dropped before a pack.
- 2026-10-26, re-root, the journey unit (scratch t308v3): members re-dock at 45 minutes and day-pass holders at 30 to
  restart their included minutes, and the pilot's riders choose an e-bike once per journey, so take-up read per ride
  undervalues Central's day-pass tours. Both concept readers and both call-only probes on the first pack missed it
  (Riverside at USD 125,000 against the golden Central at USD 200,000). On the second pack (tourists riding two or
  three journeys a pass-day), probe D (opus) read the pile-up of classic rides just under the included minutes and
  the cliff after them as riders re-docking, chained same-station restarts within five minutes and filed the golden
  exactly (Central USD 225,000), and probe C (sonnet) reached Central through the day-pass e-bike rides' uncapped
  lengths. The allowance's cliff in the ride-length distribution announces the re-dock. Dead.
- 2026-10-26, re-root screen (plan-only Opus readers, text only, no figures): county procurement savings that budget-bound
  departments re-spend, a growth grant's induced jobs where the workforce commutes in, a Medicaid plan's savings past its
  members' churn, bus journeys from housing sites that build out slower than the developers' survey says, and contingent
  business interruption carried by suppliers' locations. Each reader named the step itself as the decisive one, unprompted.
  An economic mechanism that the filed estimand's own wording invites ("the fall in expenditure", "regional jobs", "the
  plan's spending") is a reflex, whatever the world.
- 2026-10-26, re-root probe pack (job-search app, a cancellation-flow save offer tested in two markets, carried to five):
  subscribers who cancel because an employer on the platform has just hired them cannot be saved by a price, and one
  market's employer side hires half its cancellers. The plan-only reader missed it; on the pack the Sonnet probe filed
  Mexico (USD 510,000) and the Opus probe linked the employer placement invoices to the cancellers and filed Colombia
  (USD 420,000, the golden). A hire record in its own file is read as churn by the first reader who opens it. Dead.
- 2026-10-26, plan-only screen of six general mechanisms (Opus readers, text only): a list-price rise judged on promotion-week elasticities (stockpiling), an adherence programme sized on the adherent against non-adherent admission gap (healthy adherer), a heat programme sized on same-day excess deaths (harvesting), threshold clinics sized on the last reading (regression to the mean), fare-free days sized on the trial days' lift (trips moved between days), and a ward sized on average occupancy (queueing at the peaks). Every reader named its mechanism unprompted, five of them as a numbered step. A general statistical mechanism is a reflex whatever world it is dressed in; only a world-specific structure is worth a pack.
- 2026-10-26, plan-only screen of four world-specific candidates (Opus readers, text only): a road reconstruction sized on patching avoided (the reader weighted traffic by standard axles unprompted), a station car park sized on new rail journeys (the reader named railheading and the full car park's hidden demand), and a cancellation-screen save offer carried to five markets (the reader named app-store billing as the first thing that could move the winner). All three dead on paper. The fourth, a bus priority corridor whose late running carries into the vehicles' next journeys, passed: the reader worked the corridor's own journeys only.
- 2026-10-26, probe pack (bus priority on one of four corridors, sized by the passenger lateness removed in 2027; Mill Lane's buses go straight on to the busy cross-town 22 and 30 on a short layover, so the lateness the scheme removes there stops passing into those journeys; the corridor-journeys replay files Harbour Road at 62,000 against the golden Mill Lane at 96,000): the plan-only reader missed it, but on the pack the Opus probe rebuilt the 2025 operation from the AVL, found that holding at timing points and a two-minute stand on each running board reproduced every recorded arrival to the second, replayed every board-day with the scheme and filed Mill Lane at 96,000 in eight tool calls; the Sonnet probe read the same two-minute stand off the running boards and filed Mill Lane at 96,000 too. A record that a replay of its own rules reproduces exactly invites the replay, and a replay of the whole operation carries every knock-on with it. Dead.
