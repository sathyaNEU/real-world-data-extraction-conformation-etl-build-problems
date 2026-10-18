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
  evidence is a conformed market file built from sources never designed to join: Ardmoor International's parking
  revenue system (daily entries by lot, the register of every parked trip), a card survey of Ardmoor's parkers in four
  four-week waves (home ZIP, final destination, nights away, party size), the survey's handout log, the service-area
  ZIP list, the regional airport's 2027 schedule and the ticket sample's market and ticket files. The deciding quantity
  is a register-based total completed by a supplement survey: each quarter's parked trips come from the register and
  the survey supplies who and where; survey research estimates it with each returned card weighted by the inverse of
  its chance of having been collected, which the fieldwork design sets.
- **Shape:** 01, a ranked list under a cap: each candidate market's 2026 service-area passengers parked at Ardmoor, the
  three pitched, the runner-up and the gap.
- **Strategy:** maturity_censoring (a card comes back only when its car leaves, so at the collection close the cards
  from each wave's last weeks are developed only for short stays), decisive generator G7 (the operating window of the
  reply process), with G12 and G16. Gate G method_or_model_selection: the right estimator is forced by the fieldwork
  design (handout days, the last box collection, the lots' 30-day limit), the easy ones are expansions of the replies.
- **World:** United States, an unnamed state. The state Department of Transportation's Bureau of Aviation owns and
  operates Ardmoor International (the state's hub, about 80 miles from the valley) and Kessick Valley Regional (a
  regional airport with nonstop service to three airline hubs). Ardmoor's public lots run full on peak weeks, and the
  bureau's two-airport strategy is to move the valley's own travellers back to Kessick Valley: each year the air
  service development office pitches three new nonstop markets from Kessick Valley to airlines, chosen as the markets
  where the most service-area passengers drove to Ardmoor and parked to fly. In 2026 a survey contractor ran
  Ardmoor's parking card survey in four waves (February, May, August, November): a card handed to every car at the
  entry plazas for 28 days, completed cards collected from drop boxes at the exit plazas until two days after the
  last handout.
- **Forcing fact:** the pitch is taken to the airlines' network planners at the spring route development conference
  (March 2027); the office's market file and pitch brief are fixed on 29 January 2027. The call faces forward (the 2027
  pitch for service from 2028); its quantity is the closed 2026 year, which the bureau's pitch standard names as the
  basis (retrospective, with its reason: airlines judge a pitch on the latest full year).
- **Forum and forcing event:** customer_or_counterparty (the airlines receive the pitch), vote_or_meeting (the
  conference's airline meetings). Organisation government_agency; role programme_officer. Personas: Tina Hurley (Air
  Service Development Manager, who owns the pitch), Carlos Phillips (the survey contractor's project manager) and Donald
  Lara (Ardmoor's parking operations manager).
- **Data-native sentence:** a card handed out at the entry plaza can only come back when its car leaves, and the drop
  boxes came in two days after each wave's last handout, so from a wave's last weeks only the short trips' cards came
  back; the markets the valley's travellers stay at for two to four weeks (the Gulf Coast and the desert in winter) are
  the ones thinned out of the replies, and the business markets are not.
- **The WHAT screen.** Population: every trip parked in Ardmoor's public lots that entered in 2026 by a party whose home
  ZIP is in the Kessick Valley service area, whether or not its card came back (filed in the pitch standard and the
  survey's design, each wave standing for its quarter). Outcome: passengers, the travel party in full, by final
  destination city market. Window: entries in calendar 2026. Unit: passengers. Comparison: the markets without nonstop
  service from Kessick Valley in its 2027 schedule, ranked; three pitched. The decisive step settles none of them: it is
  how the returned cards are weighted to stand for the trips.
- **Deliverables:** `kvr_2027_pitch_markets.csv` (the conformed market file, one row per candidate market) and
  `kvr_2027_route_pitch_brief.docx` (the three markets, the runner-up, a chart). Names to be fixed at the prompt.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`: the task type's patterns (dual-system estimates within
    post-strata; net against gross classification error) are spent here or do not reach a destination; this build's
    pattern is its own (`own:replies-censored-by-collection-close`), from the estimation_fit family (censoring and
    truncation, weighting).
  - `stumping/references/strategies.md` maturity_censoring: open periods are not fully developed and arrival speed
    differs by unit, so the arrived count understates exactly the units that report slowly; here the unit is a
    destination and its arrival speed is the length of the stay.
  - `dataset-generation/references/layer1-messiness.md`: paper cards keyed as written, a handout log apart from the
    cards, quarterly register extracts whose layout changes, ZIP lists built from counties, airports rolled up to city
    markets, the ticket sample's quarterly files; each to be asserted neutral on the call.
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

To be written at design.

## Stump sentence

To be written at design.

## Three rules

To be written at design.

## Readability screen

To be written at design.

## Semantic fork table

To be written at design.

## Ladder

To be written at design.

## Closure table

To be written at design.

## Literal reader

To be written at design.

## Oracles

To be written at design.

## Ask sheet

To be written at design.

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
