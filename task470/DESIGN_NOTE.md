# task470 design note

Architecture 2 (re-rooted 2026-10-31). Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task470.json`, architecture v2, registered 2026-10-31T17:41:05Z after a pull,
  so every card filed before it was in the check (the re-roots of task118, task181 and task306 included). `guard.py check`
  on the registered card: PASS. One older-build match on gap, pattern and Gate G (task477) is answered by a
  differentiation line on the card. Axes drawn clear of the window at registration: organisation family
  research_or_statistics_office (local_government is banned against task181, government_agency against task306,
  utility_or_infrastructure against task118), forum minister_or_cabinet, forcing event statutory_or_regulatory_filing,
  role statistical_office_head, strategy classification_error, calibration none, context artifact register, shape 01.
  Architecture 1's identity and fate are the card's lineage, its shell (how-many, "Put", csv and docx) in
  `lineage_shells`.
- **Pairing.** Survey Research & Official Statistics / `census-register-administrative-data-quality` / Data Extraction &
  Conformation. The task type serves ETL in the taxonomy. The work is the field's own: a register-based dwelling statistic
  built by conforming the cadastre, the population register, the electricity hub's meter point register and its hourly
  reads into one dwelling-level occupancy file under the scheme's data contract, and the call is the grant designation
  that file decides.
- **Niche.** A ministry's 2027 vacant dwelling activation grant, piloted in one fictional Norwegian county of ten
  municipalities, goes to every municipality where at least 5.0 per cent of the dwellings the regulation counts stood
  vacant in the reference fortnight of 9 to 22 November 2026. The regulation defines vacant by whether anyone lived in the
  dwelling, whatever the population register shows, and has the national statistics office certify each municipality's
  share by 15 January 2027 from the hub's hourly meter data, which the regulation makes the office's source.
- **The call.** Which municipalities qualify (a designation set), with each municipality's vacant dwellings and share.
  Retrospective measurement, forward decision: the fortnight is closed, the grant is the 2027 programme's, and the
  regulation designates on that fortnight.
- **Shape.** 01, the candidates against a threshold: each municipality's vacant dwellings and share (two figures for each
  municipality), the designated set, the margin to the line, a chart of the shares against the threshold with named parts
  and the two files; with the asks, well over 25 criteria. Decision designation_set, answer set_of_items, question form
  whether (the call is where the grant should go).
- **Strategy.** classification_error. Gap objective first (the register's residents and the meter's level are correct
  records and are not what the regulation scores, which is whether anyone lived there), then population. Generators G3
  (record against operation: the meter's level records the heating, not the household) and G12 (absence of a registered
  resident against absence of residents). Gate G method_or_model_selection. Layer 2 family estimation_fit, pattern
  own:occupancy-from-the-household-daily-cycle-against-a-heating-load.
- **The ETL pincer, answered.** Of the five ETL moves this is the per-case input a second file pins: each dwelling's
  occupancy, pinned by its own hourly reads. The forcing file pins a condition (a household's daily cycle on some day of
  the fortnight). Reading the file correctly gives a level per hour and per day, and neither says whether anyone lived
  there; occupancy is the presence of the morning and evening rise over the dwelling's own night-time load, a model of a
  household's routine against a heating load that no field records, so a correct read is not sufficient. Nothing in the
  step is identity resolution, grain or time semantics.
- **Forum, event, organisation, role.** The ministry adopts the list (minister_or_cabinet); the regulation's delivery
  deadline forces it (statutory_or_regulatory_filing); the national statistics office certifies it
  (research_or_statistics_office), its dwelling statistics section head the stakeholder (statistical_office_head).
- **People** (`guard.py names --geo Norway --seed 470`, locale no_NO): Martine Strøm, head of the office's dwelling
  statistics section; Eirik Haug, the ministry's adviser on the scheme. Neither appears in the prompt.
- **Data-native sentence.** An empty dwelling in a Norwegian November is heated (a lowered thermostat or frost protection
  keeps the electric heating on), so its hourly load runs with the outdoor temperature at levels many lived-in flats never
  reach, while the population register still lists residents who have moved to care or abroad and omits students and
  workers who never re-registered; only a household's own morning and evening rise over its night-time load shows that
  someone lived there.
- **Abstraction sentence** (written against the nearest approved builds, not writable as the same): task182's "each
  bore's own lagged driver response" reads a unit's departure from its own response to a shared driver; here the step is
  the presence or absence of the users' daily rhythm in a unit's own record whose level a use-independent load carries,
  with no response to a driver estimated. Against task236 (a notified share read through a sentinel network's positivity)
  and task258 (each slow load rebuilt part by part), no second channel is used and nothing is rebuilt from components.
- **Sources.** The client's two-layer standard; register-based housing statistics (dwelling occupancy from the
  population register's registered residents, the official statistics convention this task's regulation sets aside);
  utility-data vacancy statistics (a dwelling counted vacant below a consumption floor over a period, the field's
  method at rung 1); smart-meter occupancy detection from load profiles (the household's daily activity cycle);
  Norway's centralised meter-data hub, its hourly reads and quality codes, and its meter point register.

## Default path

The path a competent analyst takes after conforming every file correctly and reading the regulation (figures are the
draw's prototype and are replaced by the generator's at stage 2).

1. Read the regulation: the dwellings the cadastre holds in use on 1 November 2026 (no holiday homes, nothing under
   construction), vacant when nobody lived in it from 9 to 22 November 2026 whatever the population register shows,
   the grant at a share of 5.0 per cent or more.
2. Conform the cadastre's dwellings to the hub's meter points by address and unit number, the hourly reads to local
   time, each hour once (the measured value over an earlier estimate), a replaced meter's two IDs joined.
3. Take each dwelling's average daily consumption over the fortnight and count as vacant the dwellings under a
   consumption floor, the utility-data vacancy rule (any floor from 1 to 12 kWh a day).
4. Share by municipality; designate those at 5.0 per cent or more.

Ends on: one municipality designated (the one whose empty dwellings are mostly unheated).

Golden: four municipalities designated.

## Stump sentence

A competent solver conforms the cadastre, the population register and the hub's hourly reads, counts as vacant the
dwellings whose average daily consumption over the fortnight sits under a floor, and designates one municipality; an
empty dwelling in a Norwegian November is heated, so its load runs with the outdoor temperature at levels many lived-in
flats never reach, and only a household's morning and evening rise over the dwelling's own night-time load shows that
someone lived there, which designates four.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own move, reading 2019 tail numbers through today's register, is identity
  resolution decided by reading the register right (data semantics); kept as Layer 1.
- 2026-10-18, at the draw: a 2027 projection of commercial aircraft NOx after the 50-seat jets retire, decided by a
  departure queue's relief at the hub's runway: the same lesson as task459 (a rate read at the decision's operating
  level, not the period average) in the same pairing, and a second hub ground-time task after task469.
- 2026-10-18, at the draw: the transition effect read against not-yet-transitioned airports (staggered adoption):
  already taught by task136 and task230.
- 2026-10-18, at the draw: operations at untowered fields from a rate per based aircraft learned at towered fields
  (selection on the outcome) as the decisive step alone: one live degree of freedom (every rung a different rate on
  the same based-aircraft list); kept as a lower rung beside the network route.
- 2026-10-18, at design: based broadcasting airplanes laid up for the year counted among the never-recorded: the small
  count fields' ratios split (L08 2 airplanes to 5) and the family of rate estimators spread 3 per cent; dropped.
- 2026-10-18, at design: an N-number changed late in 2026 at a count field read as never recorded by its current
  address and moved L08's ratio; changes kept to fields without a count and before September (SF12 asserted).
- 2026-10-18, at design: piston helicopters in the fleet: Table 1 is airplanes only and would need a rotorcraft factor;
  the valley's helicopters are turbine.
- 2026-10-18, at design: field targets on whole kilograms gave leads of exactly 22.00 and 3.00; offsets added so no lead
  sits within 0.02 kg of a whole kilogram and no tower's operations on a hundred.
- 2026-10-18, at stage 4: W33 under R4b (the never-recorded share of based airplanes as the unrecorded share, reader
  round 1's route) sat 0.1 per cent under the line, so that rung named no set; W33's recorded lead raised 0.38 kg, R4b
  now 5.2 per cent over, the golden W33 at 14.1 kg.
- 2026-10-18, at stage 4: today's register as the ask's primary device (the moved addresses' piston months priced as
  the turbines): reader round 2 resolved MASTER and DEREG by issue and cancel dates and hit all twelve figures, so the
  honest cracker scored 100 and the pair 66.6; the device became the Registry's dates leading the swap.
- 2026-10-18, at stage 4: the Registry's dates trailing the swap (the turbine flying under the number before its
  certificate): the turbines visit fields without a tower in that window, so the register's dates would price
  untowered operations as piston and move the call, and four towers' turbines fly too little to clear the bins.
- 2026-10-31, architecture 1 spent at the batch 1 repair: `guard.py heart` BLOCKed it against task242, registered ninety
  minutes earlier in another session, on strategy composition_mix, calibration gold_standard_subsample, forum
  council_or_assembly, forcing event budget_or_appropriation and organisation family local_government, and on pattern E
  against task197. It is the same core puzzle as task242 (a detector's capture calibrated on a gold-standard subsample,
  corrected by the composition of what it misses), so the slot re-roots into another world, dataset and shell. The
  repair's lessons (no file describing the data, no count the data hold in the prompt, the shell under its quotas,
  metadata prose that says what the task decides) carry into architecture 2.
- 2026-10-31, re-root screens on the item-response-theory-test-equating cell, each dead on file: item position effects
  in pre-equating (task482 v6, landed at stage 4); rapid guessing in a low-stakes sitting (task479 v4); drifted or
  released anchors and non-equivalent groups (task450, task471); rater severity on a shared subset (task471 v2).
- 2026-10-31, re-root screen: a computer-based mode effect read against students' prior paper scores with the prior's
  measurement error corrected. Rejected before code: the correction is a model of the measurement (the sampled case of
  `guide-to-prompt`'s ETL pincer, whose estimate spreads across reasonable settings), and with schools opting in, the
  school's mean prior score (measured almost without error) removes most of the bias, so the contextual model a strong
  analyst writes first lands the golden.
- 2026-10-31, re-root screens on the payment-claims and register cells: ACA grace-period cures (task482 v11, rule-heavy);
  high-cost regression to the mean, bundles against a comparison group, contract-order reconciliation and risk-adjusted
  ratios of totals (task487's screen); register over-coverage by signs of life (task478, task482); the seasonal
  adjustment cell's patterns (task453, task463, task467, task477, task481 spent).
- 2026-10-31, the world's first form, an Irish county council's vacancy programme: Ireland was drawn hours earlier by
  task268, and local_government is banned against task181, so the world moved to a Norwegian county pilot run by the
  national statistics office, where an empty dwelling is heated in November and the field's consumption floor fails for
  a reason of the country's own housing.
