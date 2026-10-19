# task269 design note

Architecture 3, re-rooted 2026-10-19 (wave 4, Descriptive lane, sathay3012) after architecture 2 was spent at stage 4 on Gate F (`## Tried and rejected`); it is the number's last architecture, and a reader landing the call retires task269. Pellbrook Metro, the state transport agency's bus network in the (fictional) Australian city of Pellbrook, runs a headway management programme: the operator, Pellbrook Bus Company, posts supervisors at timing points in the weekday peaks to keep buses evenly spaced. For 2027 the programme pays for four supervisor teams, and its guidelines give them to the four of the eight frequent routes (3, 7, 9, 14, 22, 31, 40 and 52) whose weekday-peak riders on the frequent corridor lose the most to excess waiting per boarding, measured over the August census fortnight. Four routes (7, 14, 31 and 52) run their frequent corridor from the City and then split: alternate buses go to two branches. A rider bound for a corridor stop can take either branch's bus; a rider bound for a branch can take only that branch's. On route 14 most outbound corridor riders are bound for a branch, and its two branches run as bunched pairs (the busier branch's buses come in late off a long inbound run and leave the City close behind the other branch's) while each branch keeps its own interval; on route 7 most outbound corridor riders are bound for corridor stops. The route-level measure, worked over all of a route's departures, books route 14's pairing as waiting its branch riders never do and puts it in the four; worked over the departures that serve the stop each rider taps off at, route 14 falls to fifth and route 3 takes the fourth place.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task269.json`, architecture v3, registered 2026-10-19 07:19 UTC, v1 and v2 in `lineage` with their fates. Pellbrook Metro (`government_agency`) settles the 2027 programme's routes in the contract variation it signs with Pellbrook Bus Company in December (`purchase_order_or_contract`), decided by the network performance team (`line_manager_or_team`); the requester is the network performance manager, who runs the programme and plans its supervisor posts (`capacity_planner`); the working file is the agency's monthly service performance report (`published_series`).
2. Pairing: Urban & Regional Science (client domain) / network-analysis / Descriptive & Distribution Analysis. The task type's own object decides the call: how the waiting a frequent bus network imposes on its riders is distributed across its routes, given which services each rider's trip can use on a network whose branched routes share a corridor (the common-lines structure of transit network analysis). The seed DA20 (a bus agency's headway-supervisor posts) was read for its header and Situation only; its world and quantity are taken and its own step (the frequent network's stop ranges, a WHAT) is not (`## Tried and rejected`).
3. Niche: a frequent bus network whose four branched routes send alternate buses to two branches beyond a shared corridor, so a corridor rider bound for a corridor stop can take either branch's bus and one bound for a branch only that branch's.
4. Call and shape: which four routes get the 2027 supervisor teams (`ranked_slate_under_cap`, question form which). Shape 01 (a ranked list under a cap): each route's excess wait per corridor boarding, in or out, and the first route below the four; the cap is the programme's four teams. Shape 10 (a scorecard against a filed threshold) was the first draw and is banned by task249 (`## Tried and rejected`).
5. Gate G `method_or_model_selection`, strategy `grain_or_unit`: the decisive step chooses the departures over which each rider's wait is worked (the rider's attractive set, by destination) rather than the route's or the boarded bus's. Decisive generator G2 (the grain of a rider's service: the departures serving the rider's destination, not the route), with G16 (the estimator the network's structure forces). Layer 2 family `field_method`, pattern `own:common-lines-wait-over-each-riders-attractive-set`.
6. Data-native sentence: on Pellbrook's branched routes alternate buses serve two branches beyond a shared corridor and the busier branch's buses leave the City close behind the other branch's, so the corridor's departures come in bunched pairs while each branch keeps an even interval, and the tag-on and tag-off journeys record where every corridor rider is going, which decides whether the pairs cost that rider anything.
7. Sources, one line each:
   - The client's rigor library, network-analysis: catchments by network paths and critical links by removal; neither works a wait over a rider's attractive set, and nothing here is a catchment or a link's criticality.
   - task135 (`## Tried and rejected`): the inspection paradox (waiting over irregular headways) was set aside there as a reflex; here the random-arrival wait is the standard's own formula, the default path applies it, and the stump is which departures it runs over.
   - task254 (the bus world of this lane, pace on a shuttle) and task159 (platform crowding): other quantities; task148 (queue patience, the nearest driver at 0.11) is a queue that leaves, not a wait over interleaved services.
   - task263, task120 v1, task239 and task264 v1 (the guard's older structural matches): differentiated on the card.
   - `guard.py slots` on excess wait, attractive lines, common lines and branched routes: no screen on file beyond task135's line and task198's unrelated excess.
8. People, drawn with `guard.py names --geo Australia --seed 269`: Mary Patton (Pellbrook Metro's network performance manager, the requester, author of the programme guidelines) and Jason Neal (Pellbrook Bus Company's operations manager, author of the pilot's timesheet notes). Invented names (Pellbrook, Pellbrook Metro, Pellbrook Bus Company, the corridor and suburb names) screened by hand against Australian cities, suburbs and transport operators.
9. WARNs answered: `three_rules.strategy_risk` (grain_or_unit: the analyst test's route reads every field and still files the wrong four, because no field says which departures a branch rider can take); `overuse.org_family` (a transport agency's network team is the honest organisation; every axis ban passes); `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection against task249: the estimator the network's structure forces is this build's mechanism); `repeat.question_form` against task249 (which: the call picks four of eight).
10. Screens, run as code on a passenger-level simulation before any card (buses run stop by stop with dwell from boarders; riders arrive at random and board the first bus they can use) over four world draws, scratch `t269v3/sweep3.py`:
    - WHAT screen: the population (boardings at frequent-corridor stops in the census weekday peaks), outcome (the extra time passengers spend waiting at the stop beyond the timetable's promise, arrivals at random), window (the census fortnight), unit (minutes per boarding) and comparison (the four highest) are all filed; the decisive step settles none of them, it decides over which departures the unobserved wait is estimated.
    - 1.2a: the filed quantity, passengers' waiting at the stop, is unobserved (no record holds when a rider reached the stop); the route-level measure and the golden are two estimators of it, and the route-level one assumes every rider can take every bus.
    - Reflex sweep (every one a wrong set in all four draws): the route-level measure boarding-weighted (7, 14, 31 and 40 or 3, 7, 14 and 31), unweighted by cell (the same), the peak direction only (the same), each rider on the boarded bus's branch (3, 9, 22, 40), inbound combined and outbound by the boarded branch (3, 9, 31, 40), the destination split outbound with inbound by the boarded branch (3, 9, 22, 40), the branch riders dropped (7, 14, 31 and 3 or 40), and half the gap before the boarded bus over the route's departures (3, 14, 31, 40); the golden (3, 7, 31, 40) in all four.
    - Designation determinacy, the golden's own family: per-day cells, cells pooled over the fortnight and the passenger-sampled form over each rider's usable departures each return 3, 7, 31 and 40 in all four draws; stage 3 adds the handlings of journeys without a tag-off and of near-duplicate departures and asserts one set.
    - Proxy and scalar screens: the correcting input is per rider (each journey's tag-off) and per route (each route's shares), never one number; no shipped column summarises a route's riders by usable set or its excess wait.
    - The estimator's own error: each cell's wait comes from every headway of ten census days, so the ranking's margins (about 0.25 minutes a boarding between the fourth and fifth) are many times the day-to-day noise (route figures moved under 0.06 between draws).
    - Variance-only: the step moves each branched route's level, down for route 14 and up relative to the boarded-branch reading for route 7; it is not an uncertainty correction.

## Default path

1. Read the service standard: excess wait is the extra time passengers spend waiting at the stop beyond what the timetable in force would have them wait, passengers arriving at random through the peak; it is measured at timing points (a boarding at the last timing point at or before its stop in its direction of travel) in each weekday peak of each census day, from the location vendor's revised departures; a route's figure is the average over its boardings at frequent-corridor stops, in minutes per boarding.
2. Read the programme guidelines: the four routes with the highest excess wait per corridor boarding in the census fortnight get the 2027 supervisor teams.
3. Build each corridor timing point's departures in each peak of each census day from the revised release (a bus that reopened its doors counted once) and the scheduled departures from the feed in force that day.
4. For each route, timing point, peak and day, the random-arrival wait from the route's actual headways (the sum of squared headways over twice their sum) less the same from the timetable's: the excess wait.
5. Give each corridor peak boarding its timing point's excess wait and average over each route's boardings.
6. Rank the eight routes and take the top four.

Ends on: routes 7, 14, 31 and 40
Golden: routes 3, 7, 31 and 40

## Stump sentence

The default path gives the teams to routes 7, 14, 31 and 40, because it works every corridor rider's wait from all of the route's departures at the timing point; on the four branched routes alternate buses go to different branches, so a rider bound for a branch can take only that branch's buses, which on route 14 (most of whose outbound corridor riders are branch-bound) keep an even interval while the branches run as bunched pairs, and only working each rider's wait over the departures serving the stop the rider taps off at drops route 14 to fifth and puts route 3 in.

## Three rules

Task type: network-analysis (Urban & Regional Science), which serves Descriptive & Distribution Analysis: how the waiting a frequent bus network imposes on its riders is distributed across its routes, given which services each rider's trip can use on a network whose branched routes share a corridor.
Domain test: the deciding quantity is the expected excess wait of corridor riders arriving at random, worked over the attractive set of departures serving each rider's destination (the common-lines problem of transit network analysis: riders bound for the shared corridor, and every inbound rider, face both branches' combined headways, riders bound for a branch only that branch's), from the vendor's departures and the tag-on and tag-off journeys; replacing it with the route-level excess wait over all departures gives the teams to routes 7, 14, 31 and 40 instead of 3, 7, 31 and 40.
Swap: "which four routes' corridor riders lose the most to excess waiting per boarding in the weekday peaks" with another field's nouns (wards for routes, admissions for boardings, bed-days for minutes) has no timing points, headways, riders arriving at random or branches sharing a corridor, so the question of which departures a rider can take, and the task, stop making sense.
Layer 1: the location vendor's timing-point departures come as first released and as revised after its unmatched pings were re-run (both cover the fortnight; the standard takes the revised), with a second record wherever a bus reopened its doors at a timing point; a few per cent of journeys have no tag-off and carry the default fare; the timetable changed on Monday 17 August (new running times on every frequent route), so two feeds are in force over the fortnight; a corridor stop relocated that day took a new stop code, recorded in the stop changes log; each is how an AVL vendor, a ticketing system and a timetable office keep records, and none moves the call (R2 asserted per item).
Layer 2: field_method, the common-lines wait over each rider's attractive set: a rider bound for a branch waits for that branch's buses and a rider bound for the corridor (and every inbound rider) for any bus, so the excess wait is worked per rider over the departures serving the stop the rider taps off at; the route-level measure overstates the branched routes whose branches run as bunched pairs while each keeps its interval, and the boarded-bus measure understates the riders who could take either.
Decisive step: working each corridor rider's excess wait over the departures that serve the stop the rider taps off at (both branches' departures for a corridor stop and for every inbound rider, one branch's for a branch stop), recognising that on a branched route a rider's service is the set of departures that can carry the rider, not the route and not the bus the rider happened to board.
Not semantics: every field read correctly (each departure's trip and branch, the revised release, the doubled records collapsed, each journey's tag-on and tag-off stops, the relocated stop through the changes log, the feed in force each day, the standard's formula and conventions) still leaves the route-level measure at routes 7, 14, 31 and 40, because no field, code or definition says which departures a branch rider can take: that follows from the network's structure, read from the two branches' stop patterns in the timetable feed against each journey's tag-off.
Not rule application: the standard defines excess wait (the extra time passengers spend waiting at the stop beyond what the timetable would have them wait, arrivals at random), where it is measured and how a route's figure averages it over corridor boardings, and the guidelines give the teams to the four highest; no rule or procedure says over which departures a rider's wait is worked, and executing every stated rule over the route's departures files 7, 14, 31 and 40.
Analyst test: a strong analyst who reads every file and rule correctly works each route's excess wait at its corridor timing points from all of the route's departures, weights it by corridor boardings and gives the teams to routes 7, 14, 31 and 40; on the branched routes a rider bound for a branch can take only that branch's buses, and working each rider's wait over the departures serving the stop the rider taps off at drops route 14 to fifth and puts route 3 in.
Estimand: the average excess wait per boarding at stops on each route's frequent corridor in the weekday peaks (07:00 to 09:00 and 15:30 to 18:00) of the census fortnight (Monday 10 to Friday 21 August 2026), excess wait being the extra time passengers spend waiting at the stop beyond what the timetable in force would have them wait with passengers arriving at random through the peak, measured at timing points from the vendor's revised departures, in minutes per boarding, the four highest routes getting the teams; filed in the service standard (section 3) and the programme guidelines (section 2).
No decoy: nothing is planted; branches running as bunched pairs while each keeps its own interval is how a branched route behaves when one branch's buses come in late off a long inbound run, no shipped file states an excess wait, a ranking or a method, and no memo, draft or stakeholder figure argues for a set of routes.
No certified replay: the pack carries no excess wait for any route or period; the monthly service report publishes on-time running and patronage only, so nothing is recovered by matching published figures.
Lesson: a passenger's wait on a network with shared corridors is worked over the departures that can carry that passenger where they are going (the common-lines attractive set), not over a route's or a bus's departures, so a branched route's bunched pairs cost its corridor riders and not its branch riders; no build on file works a wait over destination-dependent attractive sets.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the route-level excess wait: the standard's random-arrival wait over all the route's departures at each corridor timing point, boarding-weighted (7, 14, 31 and 40) | the standard's formula and timing points | the departures file's route column | the agency's usual excess wait by route | none | none | one formula per cell | readable |
| R1 each rider on the branch of the bus they boarded: the branch's own departures, boarding-weighted (3, 9, 22 and 40) | none | the branch on each departure and each journey's trip | grouping by the variant | none | none | a group-by on the branch | readable |
| R2 inbound riders on both branches' departures (every inbound bus runs to the City), outbound riders on the boarded bus's branch (3, 9, 31 and 40) | none | the direction and branch columns | a direction-aware split by branch | none | none | two group-bys | readable |
| R3 (decisive) each rider over the departures serving the stop the rider taps off at: corridor stops and every inbound rider on both branches, branch stops on that branch (3, 7, 31 and 40) | none: no sentence names a rider's usable departures | no column marks a rider as corridor- or branch-bound; it needs each tag-off placed in the two branches' stop patterns from the timetable feed | none: the reflexes take the route or the boarded bus | none | none | every journey classified against the stop patterns, then a cell per usable set | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | excess wait | the extra time passengers spend waiting at the stop beyond what the timetable in force would have them wait, passengers arriving at random | lateness against the timetable (on-time running) | another measure, routes by punctuality | standard 3.1, which defines it on passengers' waiting at the stop |
| SF2 | per boarding | every tag-on at a corridor stop in a census peak weighs once | per distinct rider, or per departure | same call (asserted for distinct cards) | standard 3.3 |
| SF3 | the frequent corridor | the corridor workbook's stop range for each route (City to the branch point on branched routes) | the whole route, branches included | another population (asserted wrong) | guidelines 2.1 and the corridor workbook |
| SF4 | the weekday peaks | 07:00 to before 09:00 and 15:30 to before 18:00 local time, a boarding by its tag-on time, headways beginning and ending inside the peak | the hour after each peak's end | same call (asserted for the boarding-by-departure reading) | standard 3.2 |
| SF5 | the census fortnight | the ten weekdays Monday 10 to Friday 21 August 2026 | the whole of Term 3 | nothing else is in the extract | guidelines 2.2 |
| SF6 | a boarding's timing point | the last timing point at or before its stop in its direction of travel | the nearest timing point | same call (asserted) | standard 3.2 |
| SF7 | the departures | the vendor's revised release | the first release | same call (asserted) | standard 3.2 |
| SF8 | a doubled departure record | one departure a trip a timing point, the later record (the time the bus left) | both records, or the earlier | same call (asserted) | standard 3.2 |
| SF9 | the timetable | the feed in force on each day (the 17 August feed from Monday 17) | one feed for the fortnight | same call (asserted) | standard 3.2 |
| SF10 | arrivals at random | evenly through the peak, so the wait over headways h is the sum of h squared over twice the sum of h | arrivals weighted by when boardings happened | same call (asserted) | standard 3.1 |
| SF11 | a journey without a tag-off | a boarding, in the population | left out | same call (asserted, every handling of its destination) | standard 3.3 |
| SF12 | a stop code | the relocated stop's new code through the stop changes log | the July codes only | same call (asserted) | the stop changes log |
| SF13 | the cell | each timing point, peak and census day | pooled over the fortnight | same call (asserted) | standard 3.2 |
| SF14 | four routes | the four highest figures, unrounded | ties at the printed figure | none: no tie within 0.1 of the cut (asserted) | guidelines 2.3 |

## Ladder

| Rung | Route | Four routes |
|---|---|---|
| R0 | the route-level excess wait, boarding-weighted (the default path) | 7, 14, 31, 40: wrong (route 14 in, route 3 out) |
| R0u | the same, each cell weighted equally | 7, 14, 31, 40: wrong |
| R0p | the same, the peak direction only | 7, 14, 31, 40: wrong |
| R1 | each rider on the boarded bus's branch | 3, 9, 22, 40: wrong |
| R2 | inbound on both branches, outbound on the boarded branch | 3, 9, 31, 40: wrong |
| R2b | the destination split outbound, inbound on the boarded branch | 3, 9, 22, 40: wrong |
| Rx | the branch riders dropped (corridor-to-corridor journeys only) | 7, 14, 31, 40: wrong |
| Rh | half the gap before the boarded bus, over the route's departures | 3, 14, 31, 40: wrong |
| R3 | each rider over the departures serving the stop the rider taps off at | 3, 7, 31, 40: golden |

Targets for stage 3's world (screen values, minutes per corridor boarding, golden): 31 about 1.3, 40 about 1.15, 7 about 1.05, 3 about 1.0; first below the four route 14 about 0.78, then 9 about 0.62, 22 about 0.5 and 52 about 0.35; the route-level measure puts 14 at about 1.3, above 40, with 3 out by about 0.15. Margins the generator asserts: the golden's fourth and fifth at least 0.15 apart, every reflex's set different from the golden's, every printed route figure at least 0.02 from its rounding edge under every member of the golden's family.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | boardings (tag-ons) at frequent-corridor stops in the census weekday peaks, both directions | standard 3.3; the corridor workbook |
| 2 | Unit of account | minutes of excess wait per boarding | standard 3.3 |
| 3 | Attribution window | the census fortnight, 10 to 21 August 2026 | guidelines 2.2 |
| 4 | As-of dating | the vendor's revised release of 2 September 2026 | standard 3.2 |
| 5 | Version basis | the revised release governs the first | standard 3.2 |
| 6 | Denominator | every corridor peak tag-on, journeys without a tag-off included | standard 3.3 |
| 7 | Weighting | each boarding equally; each cell's wait evenly over its peak | standard 3.1, 3.3 |
| 8 | Window length | two peaks a weekday on ten weekdays | standard 3.2 |
| 9 | Boundary inclusivity | a peak from its start to before its end; headways beginning and ending inside it; a boarding by its tag-on time | standard 3.2 |
| 10 | Rounding path | route figures unrounded for the ranking, printed to one decimal | the prompt |
| 11 | Tie-break | none needed: the fourth and fifth at least 0.15 apart | asserted |
| 12 | Maturity and censoring | none: the fortnight is complete in both releases | the releases' coverage |
| 13 | Order of operations | each cell's excess wait first, then averaged over boardings | standard 3.3 |
| 14 | Row order | none | asserted over a permutation |
| 15 | Duplicate resolution | a doubled departure record counted once (the later); tag-ons are one row each | standard 3.2; SF8 |
| 16 | Identity normalisation | the relocated stop's two codes through the stop changes log; departures to journeys by trip | the stop changes log; the departures' trip column |
| 17 | Netting against gross | none | nothing nets |
| 18 | Dimensional units | minutes; local time (AEST, UTC+10:00 throughout the fortnight) | the files' time columns |
| 19 | Code and status semantics | a default-fare journey is a boarding with no tag-off | the journeys file's notes |
| 20 | Integerisation | four routes | guidelines 2.3 |
| 21 | Clause scope | standard section 3 governs excess wait; guidelines section 2 the routes and the cap | the two documents |
| 22 | Forward window contents | the 2027 programme runs on the routes the guidelines select from the last census; the call is retrospective by design (the guidelines designate on the census just measured) | guidelines 2.2 |

## Literal reader

Executed word for word: guidelines 2 give the teams to the four routes with the highest excess wait per corridor boarding in the census fortnight's weekday peaks; standard 3.1 defines excess wait as the extra time passengers spend waiting at the stop beyond what the timetable in force would have them wait, arrivals at random, and 3.2 and 3.3 fix where (each boarding's timing point), when (each peak of each census day), from what (the revised departures and the feed in force) and how a route's figure averages it (over its corridor boardings). Read literally, a passenger waits at the stop until a bus that takes them where they are going leaves, and the timetable would have them wait for the same buses, so the literal execution over each rider's destination is the golden (3, 7, 31 and 40); the route-level route substitutes all of the route's buses for the ones a branch rider can board, which no sentence says.

## Oracles

- `generator/checks.py` (stage 3): the easy route and the decisive step on the generator's clean truth; every fork row; every rung and reflex of the sweep; the golden family's one set; Layer 1 per item (R2); the call computing identically from a pack without the ask files; the ask devices' placement; the cracker's misses; the input gates; the house checks.
- `generator/verify.py` (stage 3): every graded figure from the shipped files alone, agreeing with `figures.json` and the goldens.
- `generator/cracker.py` (stage 3): the cracker's and the mirror's ask figures on the cut pack and the pair ceiling.
- No referee file: nothing in the pack states an excess wait, a ranking or a usable set; the monthly service report's on-time running ties under every reading because the golden never uses it.

## Ask sheet

Two asks, each the trail the 2027 contract variation's price is set against: the 2026 pilot, in which one supervisor post on each frequent route ran in the weekday PM peak from February to June 2026, the routes joining in three waves. Neither ask reads a file the call reads.

**Ask A, the supervisor shifts the 2026 pilot worked on each route** (8 figures, whole numbers). Construction: each shift a pilot supervisor worked at the route's pilot post (the pilot plan's post list), counted once; cancelled shifts and the operator's own depot supervision out. Use: the variation prices 2027 post-shifts on the pilot's record. H18: a component every route carries, the trail from the pilot's record to the price.
- Primary device P1 (D1, the same records under two key schemes): the operator moved supervisors' timesheets from its payroll system (employee number, post code, the date as day-first text) to its rostering app (app user id, route and timing point, ISO date) on Monday 4 May 2026, and in the two cut-over weeks every shift was logged in both; the export stacks the two systems. Natural read: the rows at pilot posts, which counts every cut-over shift twice. Silent: no key repeats inside a system, no row is an exact duplicate, nothing marks the cut-over; matching needs the operator's staff list (employee number beside app user id) and the pilot plan's post list (post code beside route and timing point).
- Hazards: H1 (D3) the payroll dates day-first, so a match on dates parsed month-first misses most cut-over days; H2 (D4) the app keeps cancelled shifts with their status, payroll never records them; H3 (D5) the export carries the operator's depot supervision at posts outside the pilot plan.
- Span: the timesheet export, the staff list, the pilot plan: 3 files, 10 columns.
- Stops: natural (every pilot-post row, cancellations out: over by every route's cut-over shifts); half-handled (matched on person and a month-first date: over by the days that swap); over-cleaned (matched on route and date alone, which drops the two supervisors who covered one post on the same day); answer.

**Ask B, what the pilot cost on each route** (8 figures, whole dollars). Construction (the pilot plan): each route's post charges as the operator invoiced them, plus a share of the operator's monthly coordination fee in proportion to the route's shifts that month, the pilot's accounts closing with the June invoice. Use: the variation's price per post-shift. H18: a component every route carries.
- Primary device P2 (D6 and D2, an accrual reversed centrally): the June invoice had not arrived at the 30 June year end, so finance accrued each route's June post charge to the route's cost centre; the invoice was posted to the route cost centres in July and the year-end accruals were reversed in one line to the network performance cost centre. Natural read (each route's cost-centre lines, plus the central lines shared by shifts): June's charge twice on every route, and the reversal shared out as if it were a fee.
- Shared device: P1 (A's shifts) moves every B figure through the coordination fee's share.
- Hazard: H4 (D8) the ledger runs on the July to June financial year and June's coordination fee posted in July with no accrual, so a solver taking the 2025-26 year alone misses it on every route.
- Span: the ledger extract, the pilot plan, the timesheet export, the staff list: 4 files, 11 columns.
- Stops: natural (route lines and central lines by shifts: over); the 2025-26 year alone (under by June's fee share); A's shifts uncorrected (every share off); answer.

**The chart** (`excess_wait_by_route_census_2026.png`): the call's own exhibit, the eight routes' excess wait per corridor boarding in order with the four marked and the cut drawn; main side, not an ask.

**Hazard table** (stage 3 writes every count into this ledger):

| Device | Family | Asks moved | Main-path rows |
|---|---|---|---|
| P1 two timesheet systems | D1 | A, B (fee shares) | 0 (the pilot files are ask-path files) |
| P2 the June accrual reversed centrally | D6, D2 | B | 0 |
| H1 day-first payroll dates | D3 | A, B | 0 |
| H2 cancelled shifts in the app | D4 | A, B | 0 |
| H3 depot supervision in the export | D5 | A, B | 0 |
| H4 June's fee in the next financial year | D8 | B | 0 |

**The separation line.** The main call's declared row population: the revised departures at corridor timing points in the census peaks, the tag-on and tag-off journeys at corridor stops in those peaks, the two timetable feeds, the corridor workbook, the stop changes log, the service standard and the guidelines. Every device and hazard row sits in the pilot's timesheet export, the operator's staff list, the pilot plan or the ledger extract, none of which the main call opens (zero-count asserted per device).

**Referee:** none.

**Cracker sheet** (the response that lands 3, 7, 31 and 40, runs the hygiene battery and executes every filed rule):

| Ask row | Figures | What the cracker does | Cracker |
|---|---|---|---|
| A, pilot shifts by route | 8 | pilot posts only, cancellations out, no match across the two systems (no key joins them): over by each route's cut-over shifts | miss |
| B, pilot cost by route | 8 | route lines with June's accrual and invoice both, central lines shared by its own shifts | miss |

**Mirror sheet** (the same response at R0, routes 7, 14, 31 and 40): takes the asks the cracker's way and misses all 16; keeps the route figures of the four unbranched routes on the main side.

Mirror leakage: 0 per cent of the ask weight on paper (no ask figure is kept by a response that misses the devices).
Pair ceiling: 33.5 on paper (the cracker at 45, the call and its components with instruction-following and no ask figure; the mirror at about 22, five for a wrong call, the four unbranched route figures and the chart's form, with instruction-following).
Measured by: `generator/cracker.py`, v3's written at stage 3 and run on the cut pack after every change; the figures above are the paper sheet until then.

## Tried and rejected

- The seed DA19's world (a civil service's FY2026 attrition baseline for its IT retention-bonus pilot), set aside at the draw on 2026-10-19: its own stump, linking fixed-term specialists' break chains across new worker IDs, is identity resolution (data semantics as the decisive step); the average roll's seasonal surge is a reading of "average roll"; reproducing the FY2025 pilot release is a certified replay; a nowcast of the returns still open is task157's calendar-gated return wave (set aside at task268's re-root); the remaining levers (tenure hazards, the held-post mix, the stock against the flow) are survival, composition and population selection, each spent in this lane or banned in the window.
- Screens run at the draw on 2026-10-19 before this pairing, each set aside with its record: capture-recapture across overlapping lists (task123, task180, task196, task243, task248, task253 and others record it as spent or as an estimand naming its method); the dissimilarity index's small-unit bias and tempo-adjusted fertility (task262, task265 and task268: each estimand names its method); class shares from classify-and-count against mixture weights with fixed profiles (task456's latent class prevalence teaches the same lesson); range restriction of a selection test's predictive validity (its honest key is `population_selection`, banned against task268 and already six times in this lane); roll-call ideal points bridged across sessions (scaling forms with different metrics spread the graded ratio); a life expectancy gap decomposed by cause (the client tags gap decomposition as health-equity-disparity-decomposition, Root-Cause Analysis); anchoring vignettes and the Double Jeopardy benchmark (task257: the vignette items and the "for its size" estimand hand over the method); panel conditioning across rotation groups (task453, task238); pairwise comparisons scored by Bradley-Terry (the strong solver's reflex on pairwise data); heaping at a threshold (de-heaping forms disagree); a time-weighted average under value-triggered sampling (task189: the weighting is a reading).
- Architecture 1 (the 2026 dual-examined marks' variance components recombined for single examining in three circuits, 15 stations), spent at stage 4 on 2026-10-19: the cold reader (Sonnet, medium, 2.5 minutes) landed the call and every graded figure, 24 of 24 with the seven reliabilities and both asks (`score_reader.py`: call hit, ask figures 100 per cent). It fitted candidates by examiners-within-stations from the 2026 marks on its own and counted the examiner's stringency as error, quoting policy 4.3's universe ("the stations being drawn from the case bank each year and the examiners from the faculty's examiner register") and the plan's "Each station will have one examiner in each circuit" as the decisive sentences; its Q6 called the step analytical, and its only hesitation was the noise in a twelve-pair stringency estimate. The decision study for a new examining design is the field's textbook move, so no ladder on it holds a strong solver. Ask A fell to matching re-created records on title, specialty and review date (the specialty that told the newer same-title cases apart handed the over-cleaning half over), Ask B to the training record read directly and responses matched by name, the latest standing: both devices sat on the reader's own path.
- Ask A's shared-date device (architecture 2, cut 2026-10-19): each re-created record carried its old record's review date, two of three renamed. Stage 4 reader 2 linked each to the retired record of its domain, specialty and review date and landed all four domains: the shared date, with the specialty unique among a domain's retired records, made the link a lookup.
- Ask B's staff-number device alone (architecture 2, cut 2026-10-19): the hospital's and Fennabeg's attendances under their own staff numbers. Stage 4 reader 1 joined the training record on the staff number or else the name and landed all twelve figures (52.2 per cent, exit 1): once the names agree, a name join resolves the device and leaves no wrong path.
- Architecture 2 (the 2026 marks decomposed with the blueprint's domains as a fixed facet, each candidate's domain strength counted as true score: 13 stations against the pooled study's 16), spent at stage 4 on 2026-10-19: of six scored readers over three rounds, five filed 16 by the pooled decision study and the sixth stratified the study by domain on policy 4.2's "the same number from each of the four blueprint domains" and landed the call and every reliability. Judge passes 2 and 3 confined their findings to Ask B (the allocation date, then whose number a sign-in row carries) and reproduced 13 under every variant they tried. A blueprint that states a fixed content mix hands a careful generalizability analyst the stratified model; the step held five readers in six but not every reader.
- Seed DA20's own mechanism (the frequent network's stop ranges against whole routes, from the seed's header and Situation), set aside at architecture 3's draw on 2026-10-19: restricting the measure to the riders the standard counts settles the population, a WHAT, so filing it is rule application; only the world (the headway programme, eight frequent routes, four branching beyond a shared corridor) and the quantity (excess wait) were taken.
- A scorecard of the eight routes against a filed excess-wait threshold (architecture 3's first shape, 2026-10-19): shape 10 repeats task249 within the last two builds (`ban.shape`), and the programme funds a fixed number of teams anyway, so the call became a slate of four under the programme's cap (shape 01).
- Equal ridership on each branched route's two branches (screen, 2026-10-19): crediting each corridor boarding with half the gap before the bus it took, over all the route's departures, landed the golden set, because a branch rider is credited half the pairing lag too little on the early branch and too much on the late one and the two cancel when the branches carry equal riders; the late branch's share of branch riders is unequal by route (busy on route 14, quiet on route 7), and the screen asserts the half-gap crediting lands a wrong set.
- A late branch lagging by as much as the headway (screen, 2026-10-19): about half the late buses then left behind the next early one, the pairs' order flipped from trip to trip and the half-gap crediting's error averaged out (it landed the golden set in two of four draws); the lag is drawn as a fraction of the headway (0.64 to 0.80) so the late branch stays the follower.
- Inbound irregularity drawn as independent scatter at the merge comparable to the headway (screen, 2026-10-19): each branch's own inbound stream then waited about as irregularly as the combined stream, so the boarded-branch route agreed with the golden inbound; inbound irregularity is one branch arriving late at the merge, as outbound.
