# task168 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task168.json`, registered 2026-10-18T06:47:15Z, guard WARN (no BLOCK) against the registered card.
- **Pairing:** Supply Chain & Logistics (house domain `supply-chain-logistics`, task type transportation network), client domain Urban & Regional Science, task type `forecasting` (transport demand forecasting). Objective Forecasting & Predictive Modeling.
- **Seed:** FC39. Kept: the world (an airline whose summer schedule upgauges nine routes that run full every summer), the decision (the figure the outstation handling tender and the summer budget are built on) and the quantity (the additional passengers those routes will carry over last summer). Not kept: the seed's planning standard (demand as carried plus denied bookings), which would be a filed basis whose literal execution gives the wrong figure.
- **Strategy:** `population_selection`. The decisive step completes each sold-out departure's demand from the booking build of departures that never sold out, and the population that build is read from is selected on the outcome: departures that never sell out are the slow-booking, slow-season ones. Layer 2 family `estimation_fit` (censoring and truncation). Decisive generator G16 (which build the data entitles), then G6 (the sold-out departures' month mix against the reference's) and G12 (a sold-out departure's later demand is absent, not zero).
- **Furniture:** forum executive_team; forcing event season_or_peak (the summer 2026 season the handling tender and the budget have to be in place for); organisation other (a passenger airline); role capacity_planner (head of network planning); context artifact filed_standard (the summer 2026 planning basis that files the estimand); calibration prior_period_close_out (the routes upgauged for summer 2025, before and after).
- **Personas** (`guard.py names --geo Italy --seed 168`): Ugo Pacomio, Concetta Gaito, Piero Turchetta, Vincenza Passalacqua. Damiano Caruso (a real cyclist's name) and the drawn names carrying famous surnames were passed over.
- **Shape** (`other`, a forecast figure with a per-direction table): the call (1), two critical components (2), eighteen route-direction counts (18), the slide's bars and labels bound to those counts (2), the two files (2): 25 criteria.
- **Data-native sentence:** departures sell out only where demand is high, and on these routes demand is high in exactly the months whose passengers book earliest, so the departures that never sell out, the only ones whose final bookings the record observes, are the spring and autumn departures whose passengers book a few weeks out.
- **Network:** the nine Linate routes (A319, 144 seats), sixteen routes the airline upgauged for summer 2025 (to the A320neo, 186, or the A321, 220), and twenty-two thinner routes on the A319 twice a day that seldom sell out; every route's summer 2025 departures are in the booking build, summer 2024's in the YM3 archive.
- **Retrospective or forward:** forward. The call is the summer 2026 season (29 March to 24 October 2026), not yet sold when the pack closes on 12 December 2025.

## Default path

1. Read summer2026_capacity_plan_v3.xlsx: the nine routes gain 620,224 seats in summer 2026.
2. Read schedule_change_log.xlsx: sixteen routes changed gauge for summer 2025 (SC-25 gauge rows).
3. For those sixteen, summer 2025 passengers carried (dcs_flight_close_s25.csv) less summer 2024 (ym3_leg_history_s24.sqlite, lap infants taken out), over the seats each added: 0.80 extra passengers per extra seat.
4. Carry that response onto the nine routes: 0.80 x 620,224 = 495,838 additional passengers.

Ends on: 500,000 additional passengers (495,838 to the nearest 25,000)

Golden: 175,000 additional passengers (174,865 to the nearest 25,000)

## Stump sentence

A strong solver who sees that the nine routes run full takes the 2025 gauge changes' 0.80 extra passengers per extra seat times this summer's 620,224 added seats and files 500,000 against the golden of 175,000; the step that lands it there is carrying a response measured on gauge changes of 22 to 29 per cent, into routes whose demand still filled most of the new seats, onto a 61 per cent gauge change that summer 2025's demand fills only in part, when each sold-out departure's demand has to be completed from the booking build of the departures of its own month that never sold out.

## Three rules

Task type: Urban & Regional Science, forecasting (transport demand forecasting of passengers carried on a route network after a capacity change), a task type that serves Forecasting & Predictive Modeling.

Domain test: the quantity that decides the call is each sold-out departure's unconstrained demand, which a revenue management analyst recovers by projection detruncation (the seats over the share of final bookings that comparable uncensored departures hold at the moment it sold out) and replays against the new gauge; with hospital wards enlarged after a winter of full beds the call stops reading, because admissions have no advance booking build, no sell-out moment and no seasonal booking curve to complete a full ward from.

Swap: "how many more patients will our nine wards admit next winter now that they gain 600 beds" keeps the sentence and loses the analysis, since no ward fills from bookings made months ahead, so there is no build of uncensored units to complete a full one from and nothing seasonal about how early its demand arrives.

Layer 1: the revenue management system replaced between summers (summer 2024 in the YM3 archive's long layout, 19 snapshots, DD/MM/YYYY dates, three-digit flight numbers, text leg ids; summer 2025 in the new wide extract, 58 snapshots, sell-out stamped in UTC), the DCS close-out with lap infants in their own column, the close-out PDF whose summer 2024 figures include lap infants, the capacity plan's 1 June switch for Brindisi and Lamezia Terme, the booking engines' refusal log (UTC stamps, website and app sessions asking again, the agency feed's name-level records); each written by the system named, none placed to be caught, none moving the call (checks R2a to R2e).

Layer 2: estimation_fit, censoring and truncation: the completion of censored departures depends on which uncensored departures supply the booking build and on the completion's form, and the population that never sells out is selected on the outcome, so the choice that flips the call is matching the reference build on the departure's month rather than pooling it, taking the routes' own open departures, or replacing the build with a distribution fitted to final bookings.

Decisive step: completing each sold-out departure multiplicatively from the booking build of the departures of the same departure month that never sold out on the network's other routes, rather than from a build pooled over the summer or over coarser groups of months, from the nine routes' own open departures (spring and autumn departures whose passengers book a few weeks out), or from a normal EM fitted to final bookings that sit almost all at the seats.

Not semantics: every field reads plainly (sold_out_utc, bkd_dNNN, pax_flown, cap), and a solver who reads them all correctly, completes the sold-out departures from a build pooled over the summer and applies the new seats and the no-shows still files 225,000 (229,128); nothing in the call turns on a code, a unit or a definition.

Not rule application: no filed rule says how demand is estimated; the planning basis files the estimand (the routes, the seasons, passengers carried, capacity plan v3, no overbooking, no growth) and executing every one of its sentences still leaves the completion's reference and form open, while the default path that executes them files 500,000.

Analyst test: a strong analyst who reads every file and rule correctly and carries the 2025 gauge changes' 0.80 extra passengers per extra seat onto the 620,224 added seats files 500,000; one who completes the sold-out departures from a build pooled over the summer files 225,000, or 275,000 from the nine routes' own open departures, and one who fits a normal EM to final bookings files 100,000 to 150,000; only completing each departure from the build of the departures of its own month that never sold out files 175,000 (checks R3a, R3b, L10).

Estimand: planning_basis_NP-PB-26S_issue2.pdf files it, the nine Linate routes both ways (section 2), summer 2025 as flown against summer 2026 as scheduled with the same departures (section 3), passengers carried as flown at DCS close-out without lap infants or no-shows (section 4), capacity plan version 3 with no overbooking (section 5), no market growth with the same passengers wanting the same departures (section 6), and the figure as the additional passengers carried in summer 2026 over summer 2025 (section 7).

No decoy: nothing is planted to be caught, no copied block, hidden rule, memo, draft, briefing or stakeholder figure carries a wrong answer; the close-out PDF and the change log answer their own questions correctly, and no document ranks, endorses or computes a demand basis.

No certified replay: the method is not hidden behind a certified or published figure to be reproduced; no shipped figure ties only under the golden, and the back-test on the 2025 gauge changes confirms completion in general (within half a per cent) without separating the month build from the pooled one; the separations come from holdouts the solver builds on the shipped open departures.

Lesson: a censored unit's demand is completed from units that were not censored, but the uncensored units are selected on the outcome, so the reference has to be matched on what drives the timing of demand, here the departure month, and validated under censoring as deep as the units being completed; the card's differentiation against task70, the nearest same-puzzle card, is recorded, and no card on file completes censored units from an outcome-selected reference build.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| rung 0, extra passengers per extra seat (500,000) | none | the change log lists the 2025 gauge changes | builds the analog | the close-out confirms each route's totals | none | one ratio | readable |
| rung 1, carried plus turned away (50,000) | none | the refusals log | adds the denials | none | none | one sum | readable |
| rung 2, pooled build (225,000), own open build (275,000) or EM on final bookings (100,000 to 150,000) | section 6 asks for the passengers who wanted to fly | sold_out_utc and the bkd_dNNN snapshots | completes the censored departures | the 2025 back-test ties within 1.5 per cent | none | none | readable |
| rung 3, the build of the departure's own month (decisive) | no sentence names a month, a build, a reference or a form | no month, curve-group or demand column | the reflex holds the route (own open departures), pools for sample size or fits EM | no shipped control separates them; only the solver's own holdouts do | none | not a single subtraction or ratio | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | passengers carried | pax_flown, lap infants and no-shows out | seats sold, or flown with lap infants | seats sold 225,000 (213,311); infants 175,000 | section 4: "Lap infants are recorded separately and are not passengers carried; no-shows are not passengers carried"; infants same call |
| SF2 | summer 2025, summer 2026 | IATA seasons 30/03-25/10/2025 and 29/03-24/10/2026 | calendar months | same call | same call (the RM build and the DCS close-out hold exactly the IATA season) |
| SF3 | the nine routes | both directions, 18 legs | outbound only | about half | section 2: "A route counts both directions" |
| SF4 | summer 2026's departures | summer 2025's departures 364 days on | another schedule or the same calendar date | same call | section 3: "summer 2026 repeats summer 2025's departures, the same flights on the same weekdays at the same times" |
| SF5 | seats | physical seats, no overbooking | seats plus an overbooking allowance | above the bin | section 5: "Seats are sold up to the physical seats; we do not overbook domestic flights" |
| SF6 | demand | the passengers who wanted to fly | passengers carried in summer 2025 | none added | section 6: "the passengers who wanted to fly the nine routes in summer 2025, on the departures they wanted" |
| SF7 | summer 2026 capacity | capacity plan version 3 | version 2 (A321neo from the season start) | same call (182,038) | section 5 names version 3; same call |
| SF8 | rounding | once on the network total to the nearest 25,000 | per route then summed | same call | the prompt's last sentence; same call |
| SF9 | the comparison | summer 2025 as flown | summer 2025 as booked | 225,000 | section 3 "as flown" with section 4 |

## Ladder

| Rung | Construction | Figure | Rounded | Dies to |
|---|---|---|---|---|
| 0 | the 2025 gauge changes' 0.80 extra passengers per extra seat x 620,224 | 495,838 | 500,000 | the per-seat response runs 0.48 to 0.95 by route with how far demand exceeded the new seats (leave-one-route-out error 27 per cent), and completed demand exceeds 232 on 118 of 7,560 departures |
| 1 | each sold-out departure's bookings plus its logged refusals, capped at the new seats | 50,204 | 50,000 | the engines log only some refused parties; at the moments the nine routes' July and August departures sold out (a median 23 days out), departures of those months that never sold out still had about a fifth of their final bookings to come |
| 2 | completion from the open departures' build pooled over the summer | 229,128 | 225,000 | the open departures' builds differ by month; censored at 85 per cent, the pooled build puts July and August 12.4 and 13.5 per cent high, the month build within 0.9 per cent |
| 2b | completion from the nine routes' own open departures, pooled | 269,619 | 275,000 | the same: those are April, May and October departures; nearer windows of them drift up with their width in the selection holdout |
| 2c | normal EM on final bookings, by route direction and month | 135,645 | 125,000 | censored to the nine routes' monthly depth, EM falls 22 per cent short of the demand above the cap over the summer and 56 per cent in August, the month build 3 to 8 per cent over |
| 3 (decisive) | completion from the open departures of the departure's own month | 174,865 | 175,000 | |

Side errors on the golden construction: no-shows left in 213,311 (225,000); added seats at the summer 2025 load factor 594,876 (600,000).

**Method table** (every standard unconstraining method, its figure and its holdout):

| Method | Figure | Rounded | Holdout result |
|---|---|---|---|
| projection, month build of the other routes' open departures (golden) | 174,865 | 175,000 | censored at 85 per cent, every month within 0.9; at the nine routes' depth, 2.7 to 8.2 per cent over on the demand above the cap |
| projection, pooled over the summer | 229,128 | 225,000 | July +12.4, August +13.5 per cent |
| projection, nine routes' own open departures pooled | 269,619 | 275,000 | rejected: the same-flight windows drift from +5.1 (7 days) to +20.9 per cent (35 days) against the month build's +5.4 |
| projection, peak against shoulder or three or four periods | 182,096 to 197,540 | 175,000 or 200,000 | worst month 3.7 to 12.8 per cent against 0.9 |
| additive pickup, month build | 113,366 | 125,000 | size holdout: +4.6 per cent on small departures, -2.8 on large (multiplicative within 0.8) |
| additive pickup, pooled (other routes, every open departure, last open snapshot) | 138,114 to 143,558 | 150,000 | the same size holdout |
| additive pickup, nine routes' own pooled | 189,389 to 191,779 | 200,000 | the size holdout and the selection holdout |
| normal EM, route direction | 147,586 | 150,000 | the depth holdout below |
| normal EM, route direction and month | 135,645 | 125,000 | at the nine routes' depth: June -11.5, July -23.2, August -55.6, September -14.1, summer -21.9 per cent on the demand above the cap |
| normal EM, flight and month | 101,264 | 100,000 | the same |
| Kaplan-Meier on final bookings | undefined above 144 | | every peak observation at the cap is censored |

The nearest wrong method to the bin is the nine routes' own pooled additive pickup at 189,389, 1,889 above the edge, rejected twice by the data.

Construction family, every member 175,000 (checks L6, L7): month build at the sell-out stamp 174,865, at the last open snapshot 172,395, at the first closed snapshot 167,917, at the sell-out date 171,522; other routes only 174,660; the 2025 gauge changes only 176,218; every open departure including the nine's 174,989; Linate routes only 175,856; half months 172,696 (170,096 last open); ISO weeks 172,270 (169,658); by direction 174,867; by weekday 174,954; plus or minus 7 days 172,516 (169,922); plus or minus 15 days 174,024 (171,503); every open departure within 30 days 179,707; ratio of totals 174,781; median share 173,120; the nine routes' own open departures by month, the nearest month where none 179,480; route direction and month, own open, the network month where none 178,014; the same flight within 7, 14 and 21 days, falling back to the direction and the network month 175,653, 179,037 and 184,813; no-shows before the cap 176,880; each departure's own no-show share 174,920. The in-bin spread is 167,917 to 184,813; bootstrap sigma 1,732; the golden sits 12,365 from the nearest edge, the nearest member 2,687. The same-flight window drifts out of the bin at 28 days (192,447) and 35 days (200,644), where the selection holdout misses by 15.0 and 20.9 per cent against the month build's 5.4.

Coarser groupings of months: June to September against the rest 182,784 (worst month 3.7 per cent), July and August against the rest 197,540 (10.7), March to May, June to August, September and October 186,330 (6.2), March to June, July and August, September and October 195,088 (12.8), March to May, June to September, October 182,253 (4.4), four periods 182,096 (4.4); every one is rejected by the 85 per cent holdout against the month build's 0.9, and the two outside the bin miss by over a tenth.

Rounding: the in-bin family spans 167,917 to 184,813, about two-thirds of a 25,000 bin, so the figure is stated to the nearest 25,000, the precision every defensible construction shares; at the nearest 10,000 it would straddle three cells.

**Strength:** a top solver unconstrains at all about 0.7; given that, projection 0.6, additive 0.25, EM 0.15; a projection user lands with a month-or-finer network build (about 0.25), a same-flight window of three weeks or less (0.05) or an in-bin coarse grouping (0.05), about 0.35; additive and EM no longer land anywhere; the no-show and 1 June steps hold about 0.85. P(one) is about 0.7 x 0.6 x 0.35 x 0.85 = 0.125; P(both) about 0.016 independent and 0.03 to 0.05 with same-model correlation.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the nine routes' 7,560 summer 2025 departures both ways, sold out or not | filed, basis sections 2 and 3; C1 |
| 2 | Unit of account | passengers carried (pax_flown) | filed, section 4 |
| 3 | Attribution window | local departure date inside the IATA summer | filed, section 3; C1, no departure on the boundary |
| 4 | As-of dating | RM extract 01/12/2025, DCS as finalised | the extracts' own dates; static |
| 5 | Version basis | capacity plan v3 | filed, section 5; same call under v2 |
| 6 | Denominator | none, a count | n/a |
| 7 | Weighting | departures equally in the build (mean of shares) | C1: ratio of totals 174,781, median share 173,120 |
| 8 | Window length | the departure month; half month, ISO week, 7, 15 and 30 days either side | C3 corridor, every one 175,000; coarser groupings fail the holdout |
| 9 | Boundary inclusivity | ask: logged at or after the sell-out | C1: no request within 35 seconds of a sell-out |
| 10 | Rounding path | once, on the network total | the prompt |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | sold-out departures censored at the seats, completed | the decisive step; sold_out_utc in the dictionary |
| 13 | Order of operations | cap the bookings at the seats, then the no-show share | C1: no-shows before the cap 176,880, same call |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per departure in the RM build and the DCS close-out | asserted, R2e |
| 16 | Identity normalisation | flight_no and dep_date join the RM build to the DCS one to one | asserted in verify.py |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | passengers and seats | one unit |
| 19 | Code and status semantics | a blank sold_out_utc is a departure that never sold out | dictionary |
| 20 | Integerisation | none before the rounding | n/a |
| 21 | Clause scope | section 4's definition for both summers | filed |
| 22 | Forward window contents | summer 2026 is summer 2025's departures at plan v3's seats | filed, sections 3 and 5 |

## Literal reader

Executed word for word, section 6 makes summer 2026's demand summer 2025's demand departure by departure, sections 3 and 5 replay it at capacity plan v3's seats without overbooking, and section 4 counts flown passengers. The literal reader still has to estimate summer 2025's demand for the 6,418 departures that sold out, which no sentence does for it; every month-matched construction files 175,000 (C3 over the family above), and the alternatives a literal reader could still defend, additive pickup, coarser groupings of months, own-route windows of four weeks or more and a normal EM on final bookings, fall to holdouts on the shipped rows, not to a reading. No reading difference moves the call.

## Oracles

- summer2026_capacity_plan_v3.xlsx, 620,224 seats added: ties on every path.
- summer_closeout_IS24_IS25.pdf, route totals for both summers: ties on every path (rung 0 reads it, the golden does not need it).
- dcs_flight_close_s25.csv, summer 2025 carried 1,044,148: ties on every path.
- the 2025 gauge-change back-test (YM3 summer 2024 to DCS summer 2025): month build -0.4, pooled -1.5, own open +0.2 per cent; it ties under every completion, so it confirms none.
- booking_engine_refusals_s25.csv: no total in the pack ties to it; no control arbitrates the ask.
- the holdouts on open departures (85 per cent, and censored to the nine routes' monthly depth) are the solver's own analysis, not shipped figures.

## Ask sheet

The ask: passengers the booking engines turned away from summer 2025 departures because the flight was full, for each of the 18 route directions, whole passengers, in the workbook and charted with labels on one slide. The call reads no refusal record (R2d), so no device row sits in the main call's population (A9). Use: the commercial pack beside the figure (how many passengers the full flights sent away last summer). Golden total 50,632.

Devices, each on every route direction (checks A3 to A5) and each landing every figure outside its cell (A2):

- P1, a clock against a cutoff in another file (D8): fare-family refusals logged before the departure sold out (the lowest family closes at 70 per cent of the seats; those parties then bought a higher one), at least 255 records per direction; found only by setting logged_utc against the RM build's sold_out_utc. The departure-level read keeps them (54,053); dropping the lowest family altogether over-corrects (20,472).
- P2, battery-visible hazard (D1): website and app sessions asking again for the same departure, 40 to 400 seconds later at the same pax, at least 176 sessions per direction; counting every record gives 59,985.
- P3, silent with its over-cleaning half (D6, D1): the agency feed writes one record per passenger name under the booking reference, each at pax 1, a second apart; the key collapse that repairs P2 turns each agency booking into one passenger (45,371); found only by reading the feed's pax against its repeats.

Ladder stops over the 18 (totals): every record 73,201; refusals for departures that sold out at all 54,053; every record of a full flight 59,985; the cracker's key collapse 45,371; higher fare families only 20,472; golden 50,632.

Fairness: one handling reproduces the generator's party-level truth exactly (A1); no request sits within 35 seconds of a sell-out and the agency feed's name records are at most a second apart while website and app repeats are 40 seconds or more (A6, A7), so the handling has no knob.

Pair ceiling: 28.5 (cracker on the call 45.0 with no ask figure kept, mirror off the call 12.0; both on the call 45.0)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py on the cut pack (target.zip)

| Ask figure | Golden | Cracker (sell-out test, key collapse) | Cracker verdict |
|---|---|---|---|
| LIN-CTA | 4,760 | 4,294 | miss |
| CTA-LIN | 4,374 | 3,917 | miss |
| LIN-PMO | 4,173 | 3,766 | miss |
| PMO-LIN | 4,063 | 3,653 | miss |
| LIN-NAP | 2,349 | 2,106 | miss |
| NAP-LIN | 2,264 | 2,026 | miss |
| LIN-BRI | 2,731 | 2,479 | miss |
| BRI-LIN | 2,676 | 2,417 | miss |
| LIN-BDS | 2,959 | 2,639 | miss |
| BDS-LIN | 2,749 | 2,478 | miss |
| LIN-SUF | 2,644 | 2,351 | miss |
| SUF-LIN | 2,554 | 2,285 | miss |
| LIN-REG | 1,609 | 1,423 | miss |
| REG-LIN | 1,711 | 1,517 | miss |
| LIN-CAG | 2,902 | 2,588 | miss |
| CAG-LIN | 2,737 | 2,436 | miss |
| LIN-TPS | 1,661 | 1,469 | miss |
| TPS-LIN | 1,716 | 1,527 | miss |
| slide bars and labels | the 18 counts | the cracker's 18 | miss |

## House-fix register

- H1: scrubbed in the generator, not retrofitted: workbook application and modified stamp, PDF dates and library comment lines at equal byte length, the chart's embedded workbook; `scrub_producer_metadata.py` audits target/ and golden/ clean inside 2024-01-01 to 2025-12-12.
- H2: the design note's figures are printed by the build (checks L6, L7, L12, L13, H1 to H5); none comes from a scratch search.
- H7: two consecutive builds byte-identical; target.zip cut from the final rebuild; the goldens regenerate byte-identically.
- Registers: every registration once in the fleet register and every DCS tail in it with its type's seats (G8, G9); the summer 2024 flight-number blocks no longer overlap between bases.
- H9: the export manifest lists every other shipped file and not itself (G7); the dictionary covers the four extracts it names and gives the refusal log's own first and last logged dates (G10).
- H16: dates past 12/12/2025 only in the files that carry plans (planning basis, capacity plan, change log, fleet register), asserted as a file allow-list (S4), each extract's latest record before its extract date (S4').
- H11, H12, H13, H23, H24: one write-up and one prompt in the tree; rounding once at the close; the call is the opening question; no presupposing ask; the manifest speaks in the organisation's voice.

## Tried and rejected

- A saturation regime for the gauge response (demand above the new seats on the peak departures): the graded figure forked with the departure-level noise assumption; the response is now completed departure by departure.
- A weekday dependence in the booking build: the month-only build fell 4.8k from the month-and-weekday one, a near rival at the earlier rounding; the build no longer moves with the weekday.
- Homogeneous 2025 gauge changes: the pooled per-seat response back-tested at 3 per cent and stopped being a wrong rung; the sixteen changes now differ in depth (leave-one-out error 26 per cent).
- A summer 2024 refusals log beside summer 2025's: 425,000 rows, 37 MB and a 93-second build, for a calibrated-denials bypass nobody needs; the log covers summer 2025 departures only.
- A wet-leased (ACMI) operation on one route as an ask device: it sat in the main call's population.
- An ask on the 2025 gauge changes' own before and after: it is rung 0's construction, an ask keyed to the ladder.
- A booking lead that steps at month boundaries: a generator tell, and it made the calendar month the one exact partition (7-day windows filed 177.5k, 15-day 183.4k against 171.9k).
- A booking lead driven by the school-holiday dates with fortnight ramps: the month build filed 185.9k against 173.5k for 7-day windows, a bandwidth fork; replaced by a smooth seasonal lead.
- The call to the nearest 10,000: the construction family spans 167.7k to 179.5k, so it straddled 175,000; the figure is stated to the nearest 25,000.
- Contact-centre agent sessions reused across calls as an over-cleaning device: whether two records in one session were one caller or two was not determinable from the record.
- The agency feed repeating the party size on every name record: the key collapse a cracker runs for the website repeats repaired it for free; the feed now writes each name at pax 1.
- A first-closed-snapshot completion as the rejected variant: it lands inside the bin (167.7k) and is kept in the family rather than argued away.
- Leaving EM to argument: a normal EM passed the holdout a solver tries first (+1.4 per cent at half the departures censored, +0.5 at 80 per cent) and filed 125,000 to 150,000; the holdout censored to the nine routes' own monthly depth now separates it (EM 22 per cent short of the demand above the cap, the month build 5 per cent over) and is asserted.
- "Its own season" as the decisive step's wording: it licensed peak and shoulder groupings that file 182k to 198k; the wording is the departure month, and the 85 per cent holdout rejects every coarser grouping (worst month 3.7 to 12.8 per cent against 0.9).
- An open reference pool weighted to the 2025 gauge changes' 186 and 220-seat departures: pooled additive pickup landed the bin by two cancelling errors (167.7k to 172.9k); the other routes now fly the A319 twice a day and four shallow gauge changes once a day, which puts it at 138k to 144k.
- The same-flight window as a family member at any width: it drifts from 175.7k (7 days) to 200.6k (35 days); widths of four weeks or more leave the bin and fail the selection holdout.
- Summer 2024 flight-number blocks of 100 per base from 400: Linate's fourteen routes ran into Turin's block in the archive; Linate now starts at 200.
- Integer leg ids in the YM3 archive: the file's bytes spelled a token the document sweep reads as author vocabulary at every id stride tried; the archive is keyed by YM3's text leg id (date and flight).
