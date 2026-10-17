# task465 design note: Quillfield Re's 2027 county drought covers for the Ardley Plains growers

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task465.json`, registered 2026-10-17, guard WARN only (answered below).
  The first keying (gap objective, G16, Gate G method_or_model_selection) blocked on `test.same_puzzle_older` against
  task182 and `test.same_driver_older` against task228's lineage; both differentiated on the card, and Gate G re-keyed
  to forecasting (the quantity is a 2027 expectation). A first persona drew a first-name WARN and was re-drawn from the
  same list.
- **Seed:** ET22 (`analytical_tasks/07_data_extraction_conformation`), world, decision and quantity only: a reinsurer
  prices a parametric June to August drought cover for a farmers' cooperative from a station's daily record (GHCN-Daily
  layout, a 40 mm daily cap, payout between a trigger and an exit, burn analysis over the seasons since 1991). The
  seed's own mechanism (tenths of millimetres, quality flags, weekend totals) is Layer 1 here and decides nothing.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL. The physical
  sciences have no task type serving ETL other than emissions inventory, whose pairing task464 holds in the last three;
  data integration is the task type that does this work: one contract-conforming seasonal record per county built from
  the climate data centre's daily file, the airports' hourly observations and the station histories, with the seasons a
  county's gauge never observed carried from its airport station. General statistics sets its tasks in another field's
  world, so the swap test is of the method (`## Three rules`).
- **Why this task type and mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457), capture
  and coverage of registers (448, 454, 455), linkage error through a k-way link (449), continuity of identifiers (455),
  a link through shared items (450), a rotating panel's measurement change (453), a stratified sample on a revised map
  (452), latent classes from three imperfect records (456), observation selected on the trait (458), an operating level
  (459), a dispatch margin (460), a short record carried through an auxiliary series' overlap (461), detection-weighted
  snapshots (462), a drift-free price index (463) and a change found in each unit's own record (464, spent). None prices
  a payout that bends at a threshold over values the integration predicted rather than observed, where the prediction's
  own error, not its value, decides what the payout is expected to be.
- **Shape:** 07, a grid of cells: five county covers, each with its expected 2027 payout, its technical premium and the
  write-or-decline against the cooperative's offer; the conformed seasonal record and the asks add the rest (sum at
  stage 2).
- **Strategy:** other (the expectation of a kinked payout over a reconstruction's error: Jensen's inequality at the
  trigger and at the exit), on the objective gap (each county is priced on its expected payout, and a rebuilt season's
  payout at its predicted total is not its expected payout) with the population gap behind it (the seasons the gauge
  never observed are members of the climate sample the expectation runs over). Generators G16 (which estimator of a
  season's payout the evidence entitles) and G12 (a dormant season is a non-answer, not a dry or an average one). Gate G
  forecasting.
- **World:** an invented High Plains region of the United States. Quillfield Re, a reinsurer with an agricultural
  parametric desk, is asked by the Ardley Plains Growers' Cooperative to write June to August drought covers for 2027
  in its five member counties (Ardley, Corvin, Elster, Pallard, Tresham), each cover paying on the county's
  cooperative-observer rain gauge: the season's rainfall with each day capped at 40 mm, nothing above the county's
  trigger, the full limit at or below its exit, in proportion between. The gauges are read at 7 am by volunteer
  observers who leave the gauge unread on weekends and holidays and report a multi-day total the next morning; when an
  observer quits, the gauge sits dormant until the data centre recruits another. Two airport stations (Corvin Regional
  and Pallard Municipal) report every day, midnight to midnight, and hourly. Data: the climate data centre's daily file
  for the seven stations 1991 to 2026 (GHCN-Daily long layout), the airports' hourly observations, the station
  histories, the cooperative's request (counties, insured acres, dollars an acre, triggers, exits, the premium it
  offers), the term sheet and Quillfield Re's underwriting guidelines.
- **Forcing fact:** the covers attach on 1 June 2027 and the cooperative needs Quillfield Re's answer by 15 November
  2026 to set its members' 2027 enrolment; the call faces forward (each cover's expected payout for the 2027 season) on
  a record that closes with the 2025 season (the 2026 season's data is still provisional in the file).
- **Forum and forcing event:** customer_or_counterparty (the answer goes to the cooperative), season_or_peak (the 2027
  growing season). Organisation financial_institution; role portfolio_manager. Personas from `guard.py names --geo us
  --seed 465`: Brent Little (Quillfield Re's pricing analyst, who prepares the quotes), Martha Dalton (Quillfield Re's
  head of agricultural reinsurance, who answers the cooperative).
- **Data-native sentence:** a cooperative-observer gauge goes silent for whole seasons when its volunteer observer quits
  and before the data centre recruits the next one, so the gauge a cover settles on has seasons its record never saw,
  some of them the region's dry seasons, and the only witness to them is the airport station twenty-odd kilometres
  away, which saw a correlated but different season.
- **Sources (one line each):** `guide-to-prompt/references/exemplars.md` (the client's measured tasks: a forecast on a
  correctly read past is a FINE-numbers shape; this build's past is read correctly and the difficulty is the estimator);
  `stumping/references/client/two-layer-task-design.md` (estimation that fits the data: the expectation of a nonlinear
  function is not the function of the expectation); the GSDS data-integration rigor pattern (propagate the
  integration's error to the estimate: here into a payout, not a regression); task461 (a short record carried through
  an overlap; here the carried values are the default path and the move is beyond them).
- **WARN answers:** `repeat.gate_g` (forecasting after task464): task464's architecture is spent and re-rooted, and the
  forecast here is an expectation over the climate, not a trend; `repeat.deliverables` (csv and xlsx after task464):
  the conformed record is a CSV and the quotes a workbook because that is what a pricing desk produces;
  `repeat.question_form` (which after task194): the decision is a pick of covers.

## Default path

1. Read the climate data centre's daily file: precipitation for the five county gauges, June to August, 1991 to 2025,
   tenths of a millimetre to millimetres, multi-day totals spread over the unread days as the term sheet says, each day
   capped at 40 mm, the season summed.
2. Find each gauge's dormant seasons (no observations from June to August) and rebuild each from its airport station:
   regress the gauge's seasonal index on the airport's (capped the same way) over the seasons both observed, and put
   the fitted value in each dormant season.
3. Replay each county's cover over the 35 seasons on the observed and rebuilt indices; average the payouts; price at
   the guidelines' loading; write a cover where the cooperative's offer covers its technical premium.
- **Ends on:** writes Corvin's cover (its two dormant dry seasons rebuild just above the trigger and pay nothing) and
  declines Tresham's (its dormant drought season rebuilds below the exit and pays the full limit). Calibrated at stage 2.
- **Golden:** writes Ardley's, Pallard's and Tresham's covers and declines Corvin's and Elster's: each dormant season's
  payout is its expected payout given the airport's season, the payout averaged over the rebuilding's error (the
  spread of the gauge about the airport's line in the seasons both observed).

## Stump sentence

The default path rebuilds each dormant season at its predicted index and replays the cover on it, so Corvin's two dry
seasons rebuild just above the trigger and pay nothing and Tresham's drought season rebuilds below the exit and pays the
full limit, writing Corvin's cover and declining Tresham's; a rebuilt season's expected payout is its payout averaged
over the rebuilding's error, which pays Corvin's dry seasons a material share of the limit and Tresham's drought season
less than all of it.

## Three rules

- **Task type:** data integration (data-integration-record-linkage-entity-resolution): one contract-conforming seasonal
  record per county built from the data centre's daily file, the airports' hourly observations and the station
  histories, with the seasons a county gauge never observed carried from its airport station; the ETL objective's
  conformed record is the dataset the quotes are read from.
- **Domain test:** the deciding quantity is each cover's expected payout over the 35 seasons' weather, which for the
  dormant seasons is the expected payout given the airport station's season: the data-integration estimate carries the
  airport's record to the gauge together with the relationship's error, and the payout, which bends at the trigger and
  at the exit, has to be averaged over that error.
- **Swap:** General Statistics, so the swap is of the method: replace the carried distribution with its point
  prediction (or the gauge's observed seasons alone, or the airport's seasons as they are) and the set of covers written
  changes; a noun swap ("a clinic's expected overtime cost on days its sign-in sheet was lost, rebuilt from the
  hospital's census") keeps the sentence only where the cost bends at a threshold, and with a payout linear in the
  index the point prediction would do.
- **Layer 1:** precipitation in tenths of a millimetre, trace kept as a flag on a zero value and failed quality checks
  flagged in place (the data centre's daily format); multi-day totals after unread weekends and holidays with the
  unread days blank (volunteer observers); 7 am observer days against the airports' midnight days and the airports'
  hourly records in UTC (the airports' automated systems); a gauge renumbered without moving (the data centre's station
  history); limits written as insured acres and dollars an acre (the cooperative's request). Each is what the system
  that writes the file produces; none carries the call (asserted at stage 3).
- **Layer 2:** estimation that fits the data: the expected value of a payout that is flat above the trigger, linear to
  the exit and flat again below it, over seasons known only through a correlated series, is the payout averaged over the
  prediction's error, not the payout of the prediction.
- **Decisive step:** for each dormant season, take the gauge's index given the airport's season as a distribution (the
  fitted line and the spread of the shared seasons about it) and average the cover's payout over it.
- **Not semantics:** every field, flag, unit, multi-day total and clock read correctly still leaves the easy route
  replaying the cover on rebuilt indices; what moves the call is the analysis that a rebuilt index is a conditional mean
  and the payout bends at its trigger and exit.
- **Not rule application:** the guidelines file the estimand (each cover's expected payout for the 2027 season over the
  weather of the 35 seasons 1991 to 2025 at the cover's gauge), the loading and the write rule; no file says how a
  dormant season enters an expectation, and executing every filed rule on rebuilt indices files the wrong set.
- **Analyst test:** a strong analyst who reads every file correctly and applies every filed rule rebuilds the dormant
  seasons from the airport station by regression and replays the cover on the rebuilt indices, writing Corvin's cover
  and declining Tresham's (the default path's `Ends on:`); by the ratio of the stations' means, or by the gauge's
  observed seasons alone, it files another wrong set.
- **Estimand:** Quillfield Re's underwriting guidelines (`quillfield_re_parametric_underwriting_guidelines.pdf`) file
  it: each cover's expected payout for the season it covers, over the weather of the 35 seasons 1991 to 2025 at the
  gauge the cover settles on.
- **No decoy:** nothing is planted: no memo, draft or stakeholder figure argues a payout, the dormant seasons are the
  observer vacancies the station histories record, and no file ranks the covers.
- **No certified replay:** no published or certified payout history is shipped to be reproduced; the method is not
  recovered from figures.
- **Lesson:** a value the integration predicted is a conditional mean, and a decision that bends at a threshold has to
  be taken over the prediction's error; no build on file teaches that the integrated point estimate itself is the trap
  once the payoff is nonlinear (task461 teaches carrying a short record through an overlap, which is this build's
  default path).

## Tried and rejected

- A district index averaged over a network that grew from three gauges to seven: the variance of a three-gauge mean
  exceeds a seven-gauge mean's by only 5 to 15 per cent at the region's inter-gauge correlations, and in a prototype the
  burn's sampling noise swamped it in half the draws; no stable call.
- Station breaks (a gauge moved, an instrument changed): the change found in a unit's own record is task464's spent
  architecture.
- Carrying a short gauge record through a long airport record by the overlap's ratio as the decisive move: task461's
  driver; it stays a lower rung here.
