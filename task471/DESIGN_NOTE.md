# task471 design note: Kessick Valley's 2027 route pitch

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task471.json` (architecture v1), registered 2026-10-18 after a pull, so
  every card filed before it was in the check. One structural block cleared at the draw by naming the decisive
  generator honestly: with G12 first (a missing card is not a trip that did not happen) the signature (gap population,
  G12, Gate G method_or_model_selection) repeated task196 v2 in the batch and task255, task456 and task462 before it;
  the decisive generator is G7, the operating window (a reply can physically exist only between the car leaving and the
  boxes going in), with G12 and G16 behind it. Guard check then WARN only: government_agency is the organisation in 34
  builds (answered: the bureau is a state agency that owns both airports, the fact the pitch turns on); Gate G
  method_or_model_selection in 5 of the last 12 (answered: the decisive move is an estimator the fieldwork design
  forces, not a filed method, and no other Gate G fits); question form "which" repeats task245 (answered: the decision
  is a pick of three markets, and a pick asks which). Nearest driver task157 at 0.08. Personas from `guard.py names
  --geo us --seed 471`; Lisa Mccall replaced (her first name in task118).
- **Seed:** ET28 (an airport's air-service development team pitches three routes a year to airlines, choosing city
  pairs where local travellers pay most against a distance benchmark, from the 10% airline ticket sample; round trips
  looked twice as expensive and a market split across three New York airports never surfaced). Kept: the world (an air
  service development office pitching new nonstop routes from a regional airport to airlines, the 10% ticket sample and
  its market and ticket files), the decision (which three city-pair markets go in the year's pitch) and the quantity
  (how many of the region's travellers fly each market, and what they pay). Dropped as the decisive step: the seed's two
  moves, a round-trip fare read as a one-way fare and airports not rolled up to city markets, both data semantics or
  a market definition; they survive as Layer 1 on the main path (city markets) and as ask devices (fares).
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / ETL. The bureau's
  evidence is a conformed market file built from sources never designed to join: Brennick International's parking
  revenue system (daily entries by lot, the register of every parked trip), a card survey of Brennick's parkers in four
  four-week waves (home ZIP, final destination, nights away, party size), the survey's handout log, the service-area
  ZIP list, the regional airport's 2027 schedule and the ticket sample's market and ticket files. The deciding quantity
  is a register-based total completed by a supplement survey: each quarter's parked trips come from the register and
  the survey supplies who and where; survey research estimates it with each returned card weighted by the inverse of
  its chance of having been collected, which the fieldwork design sets.
- **Shape:** 01, a ranked list under a cap: each of the 14 candidate markets' 2026 service-area trips parked at Brennick
  and the passengers those trips carried (28 figures), the three pitched, the first market left out and the gap (4),
  the chart with the three marked (3) and the two files (2): about 37 criteria.
- **Strategy:** maturity_censoring (a card comes back only when its car leaves, so at the collection close the cards
  from each wave's last weeks are developed only for short stays), decisive generator G7 (the operating window of the
  reply process), with G12 and G16. Gate G method_or_model_selection: the right estimator is forced by the fieldwork
  design (handout days, the last box collection, the lots' 30-day limit), the easy ones are expansions of the replies.
- **World:** United States, an unnamed state. The state Department of Transportation's Bureau of Aviation owns and
  operates Brennick International (the state's hub, about 80 miles from the valley) and Kessick Valley Regional (a
  regional airport with nonstop service to three airline hubs). Brennick's public lots run full on peak weeks, and the
  bureau's two-airport strategy is to move the valley's own travellers back to Kessick Valley: each year the air
  service development office pitches three new nonstop markets from Kessick Valley to airlines, chosen as the markets
  where the most service-area trips drove to Brennick and parked to fly. In 2026 a survey contractor ran
  Brennick's parking card survey in four waves (February, May, August, November): a card handed to every car at the
  entry plazas for 28 days, completed cards collected from drop boxes at the exit plazas until two days after the
  last handout.
- **Forcing fact:** the pitch is taken to the airlines' network planners at the spring route development conference
  (March 2027); the office's market file and pitch brief are fixed on 29 January 2027. The call faces forward (the 2027
  pitch for service from 2028); its quantity is the closed 2026 year, which the bureau's pitch standard names as the
  basis (retrospective, with its reason: airlines judge a pitch on the latest full year).
- **Forum and forcing event:** customer_or_counterparty (the airlines receive the pitch), vote_or_meeting (the
  conference's airline meetings). Organisation government_agency; role programme_officer. Personas: Tina Hurley (Air
  Service Development Manager, who owns the pitch), Carlos Phillips (the survey contractor's project manager) and Donald
  Lara (Brennick's parking operations manager).
- **Data-native sentence:** a card handed out at the entry plaza can only come back when its car leaves, and the drop
  boxes came in two days after each wave's last handout, so from a wave's last weeks only the short trips' cards came
  back; the markets the valley's travellers stay at for two to four weeks (the Gulf Coast and the desert in winter) are
  the ones thinned out of the replies, and the business markets are not.
- **The WHAT screen.** Population: every trip parked in Brennick's public lots that entered in 2026 by a party whose home
  ZIP is in the Kessick Valley service area, whether or not its card came back (filed in the pitch standard and the
  survey's design, each wave standing for its quarter). Outcome: trips (one car's stay, counted once whatever its
  party), by final destination city market; passengers ride beside them as the ask. Window: entries in calendar 2026.
  Unit: trips. Comparison: the shortlisted markets without nonstop service from Kessick Valley in its 2027 schedule
  (seasonal included), ranked; three pitched. The decisive step settles none of them: it is how the returned cards are
  weighted to stand for the trips.
- **Deliverables:** `kvr_2027_pitch_markets.csv` (the conformed market file, one row per candidate market, its trips and
  passengers and the three marked) and `kvr_2027_route_pitch_brief.docx` (the bureau's internal brief: the three, the
  first market left out and the gap, the chart of every candidate's trips).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`: the task type's patterns (dual-system estimates within
    post-strata; net against gross classification error) are spent here or do not reach a destination; this build's
    pattern is its own (`own:replies-censored-by-collection-close`), from the estimation_fit family (censoring and
    truncation, weighting).
  - `stumping/references/strategies.md` maturity_censoring: open periods are not fully developed and arrival speed
    differs by unit, so the arrived count understates exactly the units that report slowly; here the unit is a
    destination and its arrival speed is the length of the stay.
  - `dataset-generation/references/layer1-messiness.md`: paper cards keyed and coded with the answers as written in a
    separate verbatims file, a handout log apart from the cards, quarterly register extracts whose layout changes, ZIP
    lists built from counties, airports rolled up to city markets; each asserted neutral on the call and on every
    trips figure (checks.py SF2, SF10, SF13, R2).
  - The lane's spent drivers (`guard.py mechanisms --objective etl`, 49 builds), one line each for the 2026-10 builds:
    445 a holder class keeps a fixed fraction, not a fixed amount; 447 an owner change redirects only flow whose payer
    terms allow it; 123 interval totals split onto calendar periods by a daily sample's rates; 448 a register completed
    from a second list whose capture depends on the filing route; 449 a linked value right only one time in k; 450 an
    instrument change estimated through shared items; 451 a period completed from arrival history with a delay that
    collapsed mid-period; 454 cost seen only where a price survey covered, least for one presentation; 459 a ratio that
    depends on the operating level; 453 a rotating panel's change read from the newest rotation group; 452 an area from
    strata of a revised classification; 456 one state seen through three imperfect records; 457 a report covering only
    events by its own date; 458 a lasting trait seen only while units are observed; 455 new identifiers continuing old
    units; 460 the marginal units a zero-rate source displaces; 461 a low quantile carried from a correlated long
    record; 462 intermittent sources seen by snapshot surveys whose detection rises with size; 463 a price index whose
    quantities jump in sale weeks; 465 two traits no large source records together; 464 a new scale's cut reached by
    regression that shrinks; 466 historical years known only as above or below a level; 467 a temporary change beside a
    permanent one acting on components; 468 a matcher failing for late-running records; 469 a duration seen only when it
    overruns its allowance; 470 a sensor that never records some units. The builds before 445 spend withheld rules,
    corpus fits and grain readings. None weights replies by when they could physically come back; the nearest are 451
    and 457 (amounts not yet arrived at a cut), where the delay is a property of the reporting route, not of the
    quantity being estimated, and 469, where a duration is censored by an allowance, not a reply by a collection close.

## Default path

1. Read `brennick_parking_survey_2026_cards.csv`, drop the 110 rows that repeat a card number (keying batch 3-55, which
   the export carries twice, its second copy straight after the first), take each home ZIP's first five digits and keep
   the cards whose ZIP is on `kvr_service_area_zip_codes.csv`.
2. Give each card the city market of its destination code (an airport or a metro code) through
   `bureau_city_markets.csv`; the candidates are Appendix A's shortlist in the pitch standard less Orlando, which
   Sunstream Air serves seasonally at Sanford in `kvr_nonstop_schedule_2027.pdf` (Kessick Valley's year-round flights
   go to Chicago, Charlotte and Detroit, none of them on the shortlist).
3. For each wave, take each candidate market's share of the wave's returned cards (every card in the denominator).
4. Expand each wave's shares to its quarter's transient entries in Economy C, Economy D and Long-Term from the revenue
   control system's four quarterly extracts (garage and permit lanes out), as the methods report has each wave stand
   for its quarter, and add the four quarters.
5. Rank the candidates and pitch the top three.

Ends on: Washington, New York and Dallas (Washington 6,513 trips, New York 5,121, Dallas 4,829; Phoenix fourth at 4,087
and Tampa fifth at 4,042).
Golden: Phoenix, Tampa and Washington (Phoenix 6,392 trips, Tampa 6,330, Washington 5,921; New York fourth at 4,702,
1,219 below Washington, and Dallas fifth at 4,399).

## Stump sentence

The default path expands each wave's returned cards to its quarter's entries and pitches Washington, New York and
Dallas (6,513, 5,121 and 4,829 trips), because a card comes back only when its car leaves and each wave's drop boxes
were taken in two days after its last handout, so the cards handed in a wave's later days came back only from short
stays, and the two- to four-week winter stays that make up much of Phoenix and Tampa are thinned out of the replies.

## Three rules

- Task type: census-register-administrative-data-quality (Survey Research & Official Statistics, serving ETL): an
  administrative register, the parking revenue control system's count of every car entering the long-stay lots, is
  completed by a supplement survey that carries what the register lacks (home, destination, party), and the pitch file
  conforms the two with the city-market table and the service area's ZIP list.
- Domain test: the deciding quantity is each candidate market's 2026 service-area trips, a register total split by a
  supplement survey; survey research estimates it design-based, each returned card weighted by the inverse of its
  probability of being collected, which the fieldwork design (28 handout days, the last box collection on the night of
  day 30, the lots' 28-day limit) fixes from the card's handout day and its stay.
- Swap: the setting is another field's, so the swap is of the method: with the design-based estimate replaced by the
  share of the replies, the generic summary any field would take, the call moves from Phoenix, Tampa and Washington to
  Washington, New York and Dallas; with a clinic's or a retailer's nouns there is no register of entries, no card that
  can exist only once a stay ends and no collection close, and nothing is left to estimate.
- Layer 1: the contractor's paper cards keyed and coded (the destination coded to an airport or a metro code, the
  answers to Q2 and Q4 as written in a separate verbatims file with the hand-written spellings and slips a keyer
  copies, 229 home ZIPs keyed with a plus-four or a space, one keying batch carried twice by the export); the
  attendants' handout log (card ranges and counts by plaza and day, a PDF, the share of cars reached moving plaza by
  plaza and day by day); the revenue control system's quarterly extracts (the July upgrade renamed the lot codes,
  changed the date format and added a permit column; the garage in every file); the bureau's ZIP list built from
  county lists (47058 under both Tilden and Corvel); the city-market table's multi-airport and metro codes; Kessick
  Valley's 2027 schedule with a seasonal service and local times across two time zones. Each is what the system that
  wrote it produces; none is placed to be caught, and each mishandled leaves the call and every trips figure in its
  hundred (checks.py SF2, SF10, SF13, R2).
- Layer 2: estimation_fit (censoring and truncation, weighting): the replies are right-truncated by the collection
  close, and the truncation is undone by inverse-probability weights the fieldwork design supplies.
- Decisive step: weight each returned card by the inverse of the share of its wave's handed cards whose handout day
  left room for a stay of its nights to end by the last box collection, instead of letting each card stand for an equal
  share of the wave.
- Not semantics: every field read correctly (the home ZIP, the destination code, the nights, the box date, the card
  number's handout day, the register's transient entries, the standard's trips and candidates) still leaves the
  expansion of the replies on Washington, New York and Dallas.
- Not rule application: no filed rule weights the cards; the standard files what to count, the methods report files
  the fieldwork, the collection schedule and the coding, and executing every filed rule with each card as an equal
  share of its wave files Washington, New York and Dallas; the weighting is an inference about which trips could have
  replied.
- Analyst test: a strong analyst who keys every destination to its city market, keeps the service-area ZIPs, drops
  the served market and expands each wave's returned cards to its quarter's entries pitches Washington, New York and
  Dallas (6,513, 5,121 and 4,829 trips); reweighting the cards to each handout day's cards handed, by one over the
  nights, pooling the waves or post-stratifying to each lot's entries lands the same three; only the collection-window
  weighting pitches Phoenix, Tampa and Washington (checks.py R3a and R3b on the clean truth).
- Estimand: the bureau's Air Service Pitch Standard (`bureau_air_service_pitch_standard_2027.pdf`) section 2 counts the
  trips that entered Brennick's long-stay lots in 2026 by parties whose home ZIP is on the service-area list, by the
  city market of the final destination, every such trip and not only those a survey reached; section 3 the candidates
  (the shortlist's markets without Kessick Valley nonstop service in its 2027 schedule, seasonal included); section 4
  the three with the most trips; the methods report has each wave's 28 days of entries stand for its quarter.
- No decoy: nothing is planted to be caught: no memo, draft, topline or recommended weighting; the contractor's report
  describes the fieldwork, the collection and the coding and leaves expansion to the bureau, and no file ranks the
  candidates on the pitch's basis (the DB1B market file, a declared wrong-basis distractor, ranks New York, Denver and
  Boston on Kessick Valley's own passengers).
- No certified replay: the method is not recovered by reproducing certified or published figures; the register's
  entries are the expansion base and tie under every method, and Table 1's counts are the cards handed and keyed.
- Lesson: a reply that can exist only after the event ends is truncated by the collection close, so the replies
  under-represent long events in proportion to the share of handout days that left room for them, and the fieldwork log
  supplies the weights; no build on file teaches reply truncation by a fieldwork close (the nearest, task451 and
  task457, complete amounts not yet arrived by the reporting route, and task469 censors a duration at an allowance).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 each wave's returned cards expanded to its quarter (default) | the methods report has each wave stand for its quarter (the WHAT, filed) | no | the survey expansion reflex | no | no | yes | readable |
| R1 R0 with each card reweighted to the cards handed on its handout day | no | the handout log's counts by day | the nonresponse-adjustment reflex | no | no | no | readable |
| R2 R0 with each card weighted by one over its nights | no | no | the length-bias reflex of windshield surveys | no | no | no | readable |
| R3 (decisive) each card weighted by the inverse of the share of its wave's handed cards whose handout day left room for its stay | no: the report gives the collection as an operation and no sentence names its effect | no column marks a card or a stay as cut short | not a default move | no stay data in the register, no published stay distribution | the battery finds nothing: card numbers unique once the repeated batch is dropped, every join matches | no | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative and its call | Ruled out by |
|---|---|---|---|---|
| SF1 | trips | one car's stay, counted once whatever its party | passengers: Phoenix, Tampa and Myrtle Beach | standard 4.1 (the three with the most trips) and 2.2 |
| SF2 | the service area | home ZIP on the bureau's list, each ZIP once | the list joined row for row (47058 under Tilden and Corvel) counts its cards twice: same call, every trips figure in its hundred | asserted |
| SF3 | candidate market | a city market with no Kessick Valley nonstop to any of its airports in the 2027 schedule, seasonal included | Chicago (Midway unserved) and Orlando (seasonal only) as candidates: same three, Chicago fourth at 4,755 | standard 3.1 |
| SF4 | the year and the wave's quarter | each wave's cards expanded to its own quarter's entries | the waves pooled and expanded to the year: same call, figures off (Phoenix 6,815); each wave's own 28 days of entries scaled by the quarter's days: same call, every figure in its hundred | methods report 1.2; asserted |
| SF5 | the long-stay lots | Economy C, Economy D and Long-Term | the garage added to the base: same call, every figure larger | standard 2.1 |
| SF6 | entries | the register's transient entries | the permit lanes added (third and fourth quarters): same call, figures off | standard 2.4 |
| SF7 | final destination | the coded Q2 | a connection point: no such field | the card's wording (methods report, Appendix A) |
| SF8 | handout day | the handout log's range holding the card's number | the box date less the nights: identical on every card | asserted |
| SF9 | nights | Q3 as written | none: every card's handout day plus nights falls by day 30, no stay over 28 | asserted |
| SF10 | repeated rows | one row per card number | the repeated batch kept: same call, every trips figure in its hundred | Table 1 counts each card once; asserted |
| SF11 | the wave's denominator | every returned card of the wave | the service area's cards alone: same call, figures inflated more than tenfold | standard 2.4 (the entries are every car's) |
| SF12 | rounding | the year's figure rounded once | each quarter rounded first: no reading of 4.3; moves 8 figures, same call | standard 4.3 |
| SF13 | the ZIP as keyed | its first five digits | matched as keyed (229 cards lost): same call, every trips figure in its hundred | asserted |
| SF14 | city-market roll-up | airports and metro codes through the table | airport codes alone: Washington and New York split, Phoenix, Tampa and Dallas | standard 2.5 |
| SF15 | the gap | the third's trips less the first left out's, in trips | from the rounded figures: the same hundred | asserted |
| SF16 | the weight's day counts | the log's cards handed by day, pooled over the plazas | each plaza's own counts, post-stratified to each lot's entries, or both: same call, same first market left out, every trips and passengers figure in its hundred; every handout day counted once: same call, every trips figure in its hundred | asserted |
| SF17 | the last collection | the night of day 30 (Table 1), a card dropped that day collected | the night before or after: same call, figures off | methods report 3.1, 3.2 and Table 1 |

## Ladder

| Rung | What it does | Its three | Third against fourth |
|---|---|---|---|
| R0 (default) | each wave's returned cards expanded to its quarter's entries | Washington 6,513, New York 5,121, Dallas 4,829 | 1.182 |
| R1 | R0 with each card reweighted to the cards handed on its handout day | Washington 7,027, New York 5,513, Dallas 5,216 | 1.401 |
| R2 | R0 with each card weighted by one over its nights | Washington 11,149, Dallas 7,587, New York 7,376 | 1.470 |
| R3 (decisive) | each card weighted by the inverse of the share of its wave's handed cards whose handout day left room for its stay | Phoenix 6,392, Tampa 6,330, Washington 5,921 | 1.259 |

- Position: on R0 Phoenix is fourth and Tampa fifth; on R1 fourth and fifth; on R2 tenth and eleventh. Every correction
  short of R3 walks the same way or further (R1 lifts the late days' short stays, R2 the short stays everywhere), and
  only R3 reverses.
- First market left out: New York at 4,702 against Dallas at 4,399 (1.069), the same fourth under every reading in
  SF16 and SF4 and every Layer 1 mishandling.
- Dominance: the decisive step swings Tampa against New York by 1.71 (Tampa 1.35 times New York on R3, New York 1.27
  times Tampa on R0), above 1.2 times the default path's carried advantage (1.52).
- Two separations, one quantity: the truncation's lift pays for both R0's margin and R3's; Phoenix rises 56 per cent
  and Tampa 57 from R0 to R3 while the business markets fall 8 to 9, spent 1.182 on R0 and 1.259 on R3 (product 1.49);
  a 1.5 final margin is outside the budget without dropping R0 under 1.15.
- Other routes: the waves pooled (Washington, New York, Dallas, 1.171), post-stratified to each lot's entries (the
  same, 1.182), the garage in the base (the same, 1.174). Ranking on passengers lands no shortcut: on R0's weights the
  written parties rank Myrtle Beach, Washington and New York, the coded parties Washington, Myrtle Beach and New York.
- Partial fix: keeping only each wave's first 14 handout days (the truncation seen, the late days dropped) pitches
  Washington, Tampa and Phoenix, the golden's three, with 3 of the 14 trips figures in their hundreds; it is the
  decisive insight applied crudely, and it holds the call while it loses the figures.
- Grid: two seed searches (60 and 120 worlds); the second, after the plaza-by-plaza coverage and the fourth-against-
  fifth condition (1.07) were added, passed one world of 120 on every rung condition (golden three, R0 three with the
  golden's members fourth and fifth, R1 and R2 wrong with margins, no passengers shortcut, the year's actual trips
  topping the same three, New York clear of Dallas); the build runs seed 512 and settles 20 single replies
  (calibrate.py) so every figure sits inside its hundred under every reading the fork table names.
- Worth: R3 moves Phoenix's trips 56 per cent, Tampa's 57 and Fort Myers' 82 above R0 and every business market's 8 to
  9 below, so a response off it misses the call and every candidate's figure (the mirror keeps none of the 14).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every trip that entered the three long-stay lots in 2026 by a service-area party, not only those a survey reached (standard 2.2, 2.6); the candidates (standard 3.1) |
| 2 | Unit of account | the trip, one car's stay (SF1); passengers the ask's unit, the party counted in full (standard 2.7) |
| 3 | Attribution window | entry date in 2026; each wave stands for its quarter (methods report 1.2, SF4) |
| 4 | As-of dating | the extracts of 6 January 2027, the cards and verbatims of 15 December 2026, the 2027 schedule of 20 January 2027 |
| 5 | Version basis | one version of every file |
| 6 | Denominator | the wave's returned cards, every residence and destination (SF11) |
| 7 | Weighting | the decisive step (HOW): the collection-window weights; the R3 family agrees (SF16) |
| 8 | Window length | each wave's 28 handout days and its collection to the night of day 30 |
| 9 | Boundary inclusivity | a card dropped on day 30 counts; nothing later was collected (SF17) |
| 10 | Rounding path | figures summed unrounded, reported to the nearest hundred (SF12) |
| 11 | Tie-break | none needed: third and fourth 1.26 apart, fourth and fifth 1.07 |
| 12 | Maturity and censoring | the replies are right-truncated by the collection close; completing them is the decisive step |
| 13 | Order of operations | repeated rows, ZIPs, markets, served markets out, weights, wave shares, quarter expansion, sum, rank |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | the batch exported twice dropped by card number (SF10) |
| 16 | Identity normalisation | ZIPs to five digits (SF13), airports and metro codes to city markets (SF14), card numbers to handout days (SF8) |
| 17 | Netting | none: transient entries only (SF6) |
| 18 | Dimensional units | trips and passengers; nights are days between entry and exit |
| 19 | Code and status semantics | the register's lot codes before and after July (on the rate card); purpose codes unused; never the stump |
| 20 | Integerisation | nearest hundred |
| 21 | Clause scope | standard 2 to 4; the methods report's design, returns and coding sections |
| 22 | Forward window contents | the 2027 pitch on the closed 2026 year (a retrospective quantity with its reason, Draw) |

## Literal reader

Executing the standard (every 2026 trip in the long-stay lots by a service-area party, by destination city market,
not only the trips a survey reached; candidates the shortlist's unserved markets, seasonal service counting as
service; the three with the most trips) and the methods report (cards handed at entry on 28 days, collected at the exit
plazas each night until the night of day 30, each wave standing for its quarter) with the rate card's 28-day limit word
for word, a returned card stands for the trips of its nights whose cards could have come back, which is the share of
the wave's handed cards whose handout day left room for that stay; the share of the replies is an easier method on the
same estimand, not another reading, and every term (SF1 to SF17) closes to one reading or to the same call.

## Oracles

None. The register's quarterly entries are the expansion base and tie under every method; Table 1's cards handed and
keyed tie under every method; Kessick Valley's DB1B market file and T-100 segments are a different population
(travellers who flew from Kessick Valley) and rank nothing on the pitch's basis; no file gives a stay distribution, an
average stay or a topline of destinations.

## Ask sheet

- **Ask A, each candidate market's 2026 passengers on those trips (nearest hundred): fourteen figures.** H18 home: a
  measure every candidate carries that the call does not turn on, the airline-facing size of each market the pitch
  file lists. Use: airlines plan seats on passengers, and the pitch file gives them beside the trips. Path: the cards
  (card_no, wave, box_collected, home_zip, destination_code, nights, party), the verbatims (card_no, question,
  as_written), the handout log, the register, the ZIP list, the city-market table, the 2027 schedule, the standard
  (2.7: the party counted in full) and the methods report's coding section: nine files, fourteen columns.
  Primary device: D3 with split evidence, two columns one word apart in two files, cut both ways. The card asks how
  many people flew in the party, including the traveller; the contractor's coding put a number in the cards file's
  `party`, and the verbatims file keeps the answer as written. Where the traveller wrote a sum ("2+2", "1 + 1", "2
  adults 2 kids", "me + 1"), the coding took the first number, so `party` holds 2 for a party of four: 7,588 cards, in
  every candidate market (Fort Lauderdale fewest, 13 from the service area). Where the traveller wrote the number with
  a word on who it covers ("1 (me)", "2 (me and my wife)", "3 incl. me", "4 (2 adults 2 kids)"), the coding is right
  and a parser adding every number written counts the party twice: 7,509 cards, in every candidate market (Fort
  Lauderdale fewest, 8). The methods report says only that Q4 is coded as a number. One handling (the number written,
  a sum added, "me" one) reproduces every party exactly. Every key passes, every coded value is a plausible party,
  nothing flags the rows, and no filed rule sends the analyst to the verbatims: only joining them to the cards and
  reading each Q4 answer against `party` finds both halves.
  Hazards: the collection-window weighting (the construction), the repeated batch, the ZIP forms, parties of one.
  Stops (asserted in checks.py and generator/ceiling.py): the coded party with the collection weighting (the cracker)
  misses all 14, the closest 130 outside the golden's hundred; every number written added, "me" one, with the
  collection weighting (the over-cleaner) misses all 14, the closest 140 outside; the coded party with each wave's
  replies (the mirror) misses 13; the written party with each wave's replies misses 14; the golden reads the written
  party with the collection weighting.
  Realism: a contractor coding paper cards keeps the keyed text for audit; taking the first number of a sum is the
  commonest coding slip on a count field, and a count written with who it covers is the commonest write-in on a party
  question.
- **The construction layer:** the three markets, the first left out, the gap, each candidate's trips and the chart; the
  cracker has them.
- **Main population zero-counts (asserted):** the call reads no party column (trips with every party set to one are the
  golden's); the coded and written parties move no trip figure and no member of the three.
- **Hazard table (asserted):** the device moves all 14 passengers figures; the Layer 1 items move none of them out of
  the call and no trips figure out of its hundred.
- **Referee:** none; nothing in the pack ties passengers under one handling only.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each candidate's 2026 passengers | weights each card by the collection window, counts each trip's party from the cards file's `party` (Q4 coded as a number, as the methods report files it); the verbatims, which no rule or sweep sends it to, stay unread | miss |
| A, over-cleaned | weights each card by the collection window, finds the sums by reading the verbatims against `party` and adds every number written, "me" one: the parties written with who they cover ("2 (me and my wife)", "4 (2 adults 2 kids)") count twice | miss |
| A, reconciled | weights each card by the collection window and reads Q4 in the verbatims against `party`, as reader rounds 2 and 3 did, recoding each party from the answer as written ("2+2" 4, "4 (2 adults 2 kids)" 4, "me + 2" 3) | lands all 14 |

- Mirror leakage: 7.1 per cent of ask weight (the mirror, on R0 with the coded party, keeps one of the 14:
  generator/ceiling.py).
- Pair ceiling: 55.5, over the gate (weights 38 / 7 / 55: the call 8 and each candidate's trips 30 over 14 in the main
  block, each candidate's passengers 55 over 14 in the asks). The cracker that reads Q4 in the verbatims against the
  coded party, as reader rounds 2 and 3 did, keeps everything, 100.0; the mirror keeps instructions and one passengers
  figure, 10.9. On the coded party the cracker keeps 45.0 and the pair 28.0, but the verbatims sit documented beside
  the coded column (methods report 4.2), so the device is a mirror device the cracker reconciles: the ask layer has no
  silent primary, and the build is paused on it (`pipeline.json`, resume).
- Measured by: generator/ceiling.py (on the cut pack).

## Leak check

`leak.py --asof 2027-01-29`: REVIEW, no LEAK (the first sweep's one LEAK, the DB1B file named with the word sample,
fixed by renaming it `kvr_db1b_market_2026q1_q3.csv`). Each REVIEW line answered: the standard carries the call's
words because it is the pitch standard (Kessick Valley Regional, the pitch, nonstop service) and names the fourteen
candidates only in its shortlist, unranked; the methods report, the handout log and the standard share the survey's
own words (handout, collection, returned cards, entries) and none names a weighting, a response adjustment, a stay
cut short or which cards came back (R3c asserts the absence); the verbatims, the city-market table and the standard
name candidates beside codes and answers, never beside a ranking. Harmless.

Reader, round 1 (answers appended to `leak_check_report.md`): nothing quoted for question 1 beyond the methods report's
3.1 and 3.2 and standard 2.6, which name no correction; no file ranks the candidates; question 6 an analytical choice.
It landed the call and all fourteen trips figures (each card weighted by one over its chance of being observable,
rescaled to each lot's quarter of entries) and missed all fourteen passengers figures on the coded party, noting "me +
1" coded 1 as an inconsistency without acting on it. Its findings, fixed in the generator in one pass with the judge's:
New York only 2 per cent ahead of Dallas as the first market left out (a seed search with the fourth against the fifth
at 1.07 or more, and a calibration guard at 1.05 under every reading); handout coverage identical plaza to plaza (the
share of cars reached now moves plaza by plaza and day by day, with lot choice independent of the stay so the pooled
and post-stratified estimates agree); a return rate the same everywhere (now by lot as well as by wave); destination
write-ins too tidy (a keyed tail of capitals, lower case, a state added, a full stop, a letter dropped or doubled); the
repeated batch at the end of the file (now straight after its first copy); Chicago arrivals on Eastern time (now Central,
the schedule saying so). Harmless as the systems' own: the 2027 schedule published after the standard that cites it
(a standard cites the pitch year's schedule by its role), DTT and ORL as metropolitan codes (the industry's own), an
A320 on a seasonal leisure route.

Judge, pass 1 (`determinism_check_report.md`): DETERMINISTIC, FIX_NOW on the write-up's step 2 only (it named Chicago,
Charlotte and Detroit as cut from the shortlist; only Orlando is on it), fixed in writeup.py and in the brief. Every
figure reproduced; expanding by lot, per-plaza weights, weights by day count and the cutoff a day either way all keep
the three and the first market left out. Gate G statistical_rigor (the card files method_or_model_selection; both name
the censoring-aware expansion), analytical_non_defect; Gate H pass, decisive step analytical. Stump power moderate.

Reader, round 2 (on the fix-pass pack): nothing quoted for question 1 beyond the methods report's 3.1 and 3.2 and
standard 2.6; no file ranks the candidates; question 6 an analytical choice. It landed the call (its trips from a
product-limit estimate of each market's stay lengths with the chance of collection floored at 0.1, Phoenix 6,800,
figures it calls noisy by 300; the design gives each card's chance of collection exactly from the log's counts by day
and the last collection, which both judge passes reproduce) and recoded every party from Q4 as written, the sums
added, so the first-number coding cost it nothing. Realism fixed in the generator with the device: the coding slip on
every sum form alike, the garage's flat year (now seasonal), a post office named apart from its town. Harmless: the
log's 1,027 (its one count over a thousand, printed with the comma), serials contiguous within each plaza and day (cards
issued from numbered pads), file dates listed without a year.

Judge, pass 2 (`determinism_check_report_pass2.md`, on the fix-pass pack): DETERMINISTIC, APPROVE. Every figure
reproduced (Phoenix 6,392, Tampa 6,310, Washington 5,921, New York 4,702, the gap 1,219); expanding by lot or plaza,
the last collection a day either way and a uniform-handout weight keep the three and New York fourth; its one residual,
the coded party against Q4 as written, moves passengers only and is forced to the written answers by standard 2.7.
Gate G statistical_rigor and analytical_non_defect, Gate H pass, stump power moderate.

The passengers device was then cut both ways on the ask path with every figure in `generator/figures.json` unchanged:
the parties written with who they cover coded right, so a parser adding every number written counts them twice.

Reader, round 3 (target.zip c9e9c2fd35a4d875): nothing quoted for question 1 beyond 3.1, 3.2 and 2.6; no file ranks the
candidates; question 5's literal reading fixes the population and leaves the estimator to the design; question 6 an
analytical choice. It landed the call and all fourteen trips figures (each card weighted by the register's entries on
the days that left room for its stay against the wave's) and all fourteen passengers figures, recoding each party from
Q4 as written ("3 (2 adults 1 kid)" 3, "2 (me and my wife)" 2, "me + 2" 3). Its brief asked for example write-ins in
the closing summary, which points at the verbatims, so the round overstates the exposure; round 2's brief did not, and
it reconciled the coding all the same. Realism notes left at the pause: the Q4 write-ins drawn from 62 forms, the
destination typos mechanical, every card complete, the ZIPs contiguous; wave 3's longest stay of 19 nights is the
summer draw's thin tail, not a cap.

Stage 4 outcome: the call deterministic and analytical (judge twice, readers three times), its stump power moderate
(every reader landed it, round 3 citing the returns per card handed falling from 0.35 to 0.09 over each wave's last
eight handout days, a rate rung 1's weighting by handout day computes on the way); the ask layer has no silent
primary. PAUSED, not shipped.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own moves, a round-trip itinerary fare read as a one-way fare and the New York
  airports left as three markets: data semantics and a market definition (the estimand's unit), so neither may decide;
  kept as Layer 1 and as ask devices.
- 2026-10-18, at the draw: a windshield census (cards put on every car parked in the lots at sweep times), whose cards
  over-represent long stays in proportion to their length: population_selection, banned against task245 at the draw,
  and the label is not moved to pass the guard; replaced by the entry-plaza handout, a different mechanism (replies
  censored by the collection close, which thins the long stays instead of inflating them).
- 2026-10-18, at the draw: the fare premium over a log-log fare-distance benchmark, decided by retransformation bias:
  generic econometrics, and a clinic's charges against a severity curve read the same (swap test fails).
- 2026-10-18, at the draw: the three markets with the highest premium in thin ticket-sample cells, decided by
  shrinkage (the winner's curse): the shrinkage method is not forced by anything filed, a coin flip for determinism.
- 2026-10-18, at the draw: leakage read from an agency ticket dataset whose capture depends on the sales channel,
  measured where the ticket sample sees everything: the same lesson as task448 and task470 (capture by unit measured
  on the overlap).
- 2026-10-18, at the draw: a departure-lounge survey with a fixed quota of interviews per flight (unequal inclusion):
  a ratio within each destination sidesteps it, and by house precedent (task452) a design-weight stump is
  population_selection, banned at the draw.
- 2026-10-18, at the draw: capacity-censored (spilled) demand on full flights to the hubs: the demand turned away is
  model-dependent and every demand model is a fork.
- 2026-10-18, at the draw: the share of one-way tickets that are residents' trips (a one-way ticket's origin is not
  its traveller's home): turns on reading what the ticket origin field means, data semantics.
- 2026-10-18, at the draw: business travel by market from the fare-class proxy corrected for its false positives
  (Rogan-Gladen): the lesson task456 teaches (an imperfect record's false positives subtracted, not only its misses).
- 2026-10-18, at the build: the party verbatim beside the coded party in the cards file, with a filed rule sending the
  analyst to the verbatim for parties of nine or more: the rule pointed every careful solver at the verbatim column,
  where the sums sit in plain view; the verbatims moved to their own file and the cap dropped.
- 2026-10-18, at the build: home ZIPs keyed with a plus-four on 16 per cent of cards: matched as keyed they moved every
  trips figure out of its hundred, so a Layer 1 item carried figure difficulty; cut to a realistic 0.3 per cent and
  asserted neutral, with the two-county ZIP made a small rural office and the repeated batch chosen so its second copy
  moves no figure out of its hundred.
- 2026-10-18, at the build: passengers on the default path's weights ranked Washington, Phoenix and Tampa, the golden's
  three, so ranking on passengers was a shortcut to the call; the winter markets' parties cut to couples and singles
  (1.65 to 1.75) and Myrtle Beach's summer family trips raised to 3,000, so passengers on any weighting carry Myrtle
  Beach.
- 2026-10-18, at the build: the first realisation (seed 471) put New York within 1.12 of the third market once the party
  draw moved onto each card; New York and Dallas set lower in the world and a seed search run over 60 worlds; seed 504.
- 2026-10-18, at stage 4: seed 504's world, where New York led Dallas for the first market left out by 2 per cent and
  a reweighting or a dropped batch could swap them (reader round 1); the handout coverage reworked plaza by plaza and
  day by day with lot choice independent of the stay, and a 120-world search run with the fourth against the fifth at
  1.07 or more; one world passed, seed 512.
- 2026-10-18, at stage 4: the passengers device cut one way (a sum written on the card coded as its first number):
  reader round 2 read Q4 in the verbatims against `party` and recoded every party, the sums added.
- 2026-10-18, at stage 4: the same device cut both ways (the parties written with who they cover coded right, so adding
  every number written counts them twice): reader round 3 recoded every party right. Both cuts are mirror devices: the
  verbatims are documented beside the coded column (methods report 4.2), so reconciling them is the cracker's reflex,
  and no reading of Q4 the frozen documents leave open is both determinate and missed by a careful parser.
- 2026-10-19, re-root tried on paper: the same parking survey with the third pick held unless its lead over the first
  market left out clears twice its design-based standard error (cards clustered by handout day, weighted by the return
  window). Measured on the v1 pack it cannot bind: 73,909 returned cards put Phoenix, Tampa and Washington each 3.5
  standard errors clear of New York on the weighted card-level variance and 2.3 to 3.4 clustered by day; binding it
  would need a tenfold smaller sample and same-day group travel, a planted structure, and the clustering unit itself
  is arguable when the waves are consecutive days. Dropped before any data was cut.
