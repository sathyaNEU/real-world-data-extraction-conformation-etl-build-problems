# task137 design note

Architecture 5, drawn and registered 2026-11-02 (Forecasting lane, wave 2 slot). Architecture 1 (Kaimai Building
Society's maturity campaign, banking) was landed on the portal; architecture 2 (Calderbrook Care's adverse-drug-event
admissions) lost every decisive step to probes; architecture 3 (Calderwick Police's custody hub) was spent at stage 4;
architecture 4 (Hollinsfield and Brantmoor's phlebotomy hub) kept a sound call but was spent on its ask layer, and its
10-26 version stays on the portal as delivered. All four identities are in the card's lineage and their dead ends in the
last section; nothing of any of them is kept. This draw is Tarnfield Wholesale's 2027 motor claims fund: the collision
claims its 7.5-tonne delivery fleet will make in 2027 once a new schedule sends every store route out between 03:45 and
05:15 all year.

## Draw

1. **Card.** `.claude/skills/fingerprint/cards/task137.json`, architecture v5, registered 2026-11-02T20:53:26Z with
   architectures 1 to 4 in its lineage (architecture 4 marked `architecture_spent`, its shell in `lineage_shells`).
   `guard.py check` on the draft and on the registered card: PASS, with two NOTEs answered on the card
   (`test.same_puzzle_older` against task204, a room's unsteady ventilation balance; `driver.near` 0.16 against
   task121 v3, clock-hour matching of complaints to a facility). Axes redrawn at the draw because task458 v3 and task197
   v2 were filed minutes earlier and moved the window: forum `committee_or_panel` to `board_of_directors` (the board
   approves the self-insured claims fund), role `finance_controller` to `procurement_lead` (the manager buys the motor
   cover and runs the fund), org `other` to `logistics_or_3pl` (a delivered wholesaler whose business is distribution on
   its own fleet), strategy `forecast_method_backtest` to `composition_mix` (honest: the rate is stable within light
   condition and hour band, and the schedule moves the light mix), gap `time` to `objective` then `time` with G7 first
   (`test.same_puzzle` and `test.same_driver` blocked on time with G14 or G7 against task154's and task183's lineages).
2. **Pairing.** Actuarial Science & Insurance, task type `claims-frequency-severity` (serves Forecasting and
   Descriptive), objective Forecasting & Predictive Modeling: the call is a count of claims in a year not yet begun.
   The first draw of this slot in the client domain; no architecture of the lineage used it.
3. **Shape.** 02, a forecast across periods: the 2027 claims and each 2027 quarter's, with the asks' figures beside
   them (the criteria arithmetic is in `## Ladder` and `## Ask sheet`).
4. **Strategy and mechanism.** `composition_mix`, generators G7 (when the driving physically happens against sunrise and
   sunset decides its rate), G6 (the forward exposure's light mix moves under a clock-hour mix the record already ran),
   G14 (the collision rate conditioned on the light each kilometre is driven in). Gate G `forecasting`.
5. **Data-native sentence.** The fleet ran its small-hours departures only on the May-to-August summer schedule, so
   every early-morning kilometre in the record was driven after sunrise and the record's driving in darkness happened on
   winter evenings' returns and at the summer schedule's first and last weeks; the 2027 schedule runs the small-hours
   departures all year.
6. **Abstraction sentence.** "A rate per unit of exposure is stationary only once each unit is placed in a physical
   condition the clock tracks only by season, and a schedule that moves the exposure into hours the record ran only
   while the condition was absent leaves every clock-hour rate low." No approved build carries it: task501's meter drift
   and task139's accumulated use both swap one exposure clock for another (litres for months, use for months of cover);
   here the exposure measure is unchanged (kilometres) and what decides is the light each kilometre is driven in, a
   property of the date, the clock time and the depot's position that no clock-hour rate or month term recovers.
   task163 (shipped, pending) moves picks beside near-weight neighbours through a check-weigh's blind band, a filter and
   a layout; nothing here is filtered and nothing is rearranged in space.
7. **Mechanisms read** (`guard.py mechanisms --objective forecasting`, 92 builds): the exposure-clock family (task46
   cumulative service exposure, task139 accumulated use, task501 litres not months) spends the swap of one usage measure
   for another; task176 v2 an external age clock; task132 renewal restarts; task163 a filter's blind band moved by a
   layout; task121 v3 (dead) clock-hour matching to attribute events; none prices exposure by solar light.
8. **Slots read, both screens, before the first harness.** Setting nouns (darkness, sunrise, daylight, twilight, clock
   change): task182's architecture 8 screen rejected an hour-of-week profile in darkness-relative time as exact
   arithmetic on a shipped sunset table that settles the estimand's own clock; here no sunset table ships, the estimand
   (claims in 2027) has no clock to settle, and the light condition is the exposure model's HOW; task138, task248,
   task119, task125 and task472 carry daylight saving only as Layer 1. Mechanism and world nouns (fleet, telematics,
   collision, motor insurer): task174's telematics onboarding score and task268's development by notifying route
   (spent as one join away) are other mechanisms; task165 and task153 use telematics as a spine for other quantities.
9. **Neighbouring slots' `resume` lines read** (every forecasting slot in flight): task130, task143, task145, task146,
   task148, task161, task170, task173, task176 and task178; task178's note that a reserving-development-triangles cell
   was searched and found nothing that holds is why this draw sits in claims-frequency-severity, not reserving; the
   recurring finding in task143, task148, task161 and task170 (ask layers spent once the cracker was made honest) is why
   the ask records were named before registration and are screened as code before any data is cut.
10. **The ask records, named at the draw.** (A) The receipts other insurers paid towards the fleet's own-damage repairs
    (the wholesaler self-insures own damage): the domain mechanic is subrogated recovery of the outlay at the other
    side's share of liability, contributory negligence splitting a collision 50:50 or 75:25, remitted under the paying
    insurer's own reference on many lines. (B) The bodyshop network's invoice feed: the domain mechanic is a feed
    resend under fresh invoice numbers beside genuine same-day second invoices on one repair (a supplementary after
    strip-down), each repair's authorised total fixing which lines are real. Both are screened against the
    careful-solver cracker as code before the pack is cut (`## Ask sheet`).
11. **Sources.** Synthetic world on real geography and real rules: sunrise and sunset by the NOAA solar position
    equations at each depot's latitude and longitude; British Summer Time from the last Sunday of March to the last
    Sunday of October; England's bank holidays 2023 to 2027; UK motor claims practice (own damage, third-party property
    and injury, subrogated recovery at a liability split). People drawn with `guard.py names --geo GB --seed 137`.

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
- The coming list's special as the 2024 three-year special (5.65 per cent onto a 3.00 per cent card): the latest
  campaign's share by term and the share by locked rate within term landed 2 to 3 per cent under the golden, because the
  2026 campaigns' three-year deposits, opened at the 2023 peak, met the same drop. Moved to a 2023 four-year special,
  whose past four-year peers all locked in the 2021 and 2022 lows; every term-based rival now lands 19 to 28 per cent
  short.
- Hours to the nearest 100: with the list's drops on thin past support (0.25, 0.55, 1.50 points) the estimator corridor
  (bands of 0.2 to 0.5 at offsets, logistic, isotonic) spread 110 to 230 hours. The 2027 card was set so the list's
  drops sit on dense past drops (0.45, 1.35, 2.00, 2.30, 2.50), and the block moved to multiples of 250 (SOW 2.2,
  procedure 6.1).
- Hours to the nearest 500: the locked-rate and trend rivals landed all three months, and rounding each month to 500
  stopped the months adding to the block.
- Extract notes that said the certificates in the holdings view were moved to the core and what MIGRATED means: they
  narrated Ask B's overlap; the notes now describe the files' fields only.
- Forum `line_manager_or_team` (the head of deposits signing the block order alone): task136 moved its forum to the same
  key after this card was registered, and `ban.forum` blocked; the Deposits Committee now approves the block.
- Write-up figures rounded coarser than they read: the list's retention-offer share to the nearest 5 per cent (60,
  against 62.1) and its non-reaching dials to the nearest 500 (67,500, against 67,354.8); the judge read both as wrong.
  Now whole per cent and nearest 100 (62, 67,400), with freeze.py allowing the two keys
  (`components.retention_share_pct`, `steps.non_reaching_dials`); the Final Recommendation and Critical Components move
  only by that 60 to 62.
- The judge's wording for the Ask A clause (a deposit counts if any of its maturity proceeds were in a society term
  deposit, its principal the amount in term deposit then): "maturity proceeds" is the transfer extract's narrative and
  points at Ask A's device, and "the amount on term deposit then" reads as the new deposit's whole balance, new money
  included (the whole-principal stop). Filed as: counting a deposit if any of its principal was, and only the part that
  was.
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK), because its decisive step, the share of
  conversations going to the retention offer conditioned on each deposit's drop from its locked rate to the card, was
  the strong model's reflex and the field's textbook model: a logistic of the retention outcome on term with a separate
  locked-rate slope per term booked about 5,496 hours, inside the golden's 5,500 bin, without reading any card; the
  share by locked rate sat one bin under; Ask B's migration batches file announced the overlap and an account-level
  dedup against it cracked the ask; Ask A's clause (a deposit counted if any of its principal was kept, and only that
  part) signalled the partial-move device; and the swap test passed only narrowly (insurance renewals priced off a rate
  card read almost the same). Round 2 keeps the world, the call and the asks' populations and moves the decisive step
  to the class of the money, a reason only deposit repricing behaviour has.
- A market-gap stump for round 2 (each deposit's locked rate against a published market rate for its term and opening
  month, the deposits far above the market leaving): the market table made the premium a visible column and the step
  one join (readability tests 2 and 6); the class is rebuilt from each list's own cohorts instead, with no table naming
  it.
- Other round-2 candidates for the decisive step, dropped at the draw: the term structure of the card alone (still the
  drop, read term by term, the reflex the audit measured); the best card across terms as the rate a deposit is compared
  with (a second reading of the rate it reinvests at, a fork and never a stump); money above the Depositor Compensation
  Scheme's per-depositor cover leaving at maturity (a filed limit executed on a visible principal column, rule
  application read off the schema).
- Round 2's first prototype kept round 1's January to March 2027 card (four years 3.15 per cent, so the special's drop
  was 2.50 points): past special money dominated the 2.50 band, so the share by drop alone booked near the golden, and
  the locked-rate-by-term logit carried the special's deposits at about 0.8. The 2027 card was turned up (four years
  4.00, a drop of 1.65), a band in which past conversations are 89 per cent member money.
- The card's gap reordered to population first: `guard.py check` blocked on `test.same_driver` (population, E,
  forecasting against task124's lineage) and `test.same_puzzle_older`; the gap stays time then population, the honest
  order for a premium that lapses at first maturity.
- January's share of the 2023 four-year special's sales at 0.242: January's hours sat near a rounding edge and the drop
  and term logistic landed January's bin (1,250); the sales by month are now 0.184, 0.408 and 0.408, January's golden
  1,206.9 and that rival's January 1,000.
- Ask B at six figures (each month's maturing principal on and off the list): with Ask B the most obvious device, the
  cracker's pair ceiling rose to 41; cut to four figures (the three months and the quarter's part not on the list),
  39.0.
- Ask A's device as a posting date (D8, maturity proceeds posted on the next business day): the hygiene battery's
  unmatched-join count found it at once; moved to the payments system's settlement account with the matured deposit
  named only in the narrative (D7).
- The write-up's past share for member money (15 per cent, 14.57 unrounded) and all past conversations' share in the
  special's band (35 per cent, 34.55): both within 0.07 of a rounding edge; dropped from figures.json, the write-up, the
  note and the workbook, the band given by class instead (88 and 28 per cent, 0.24 and 0.18 from an edge).
- The note's chart title "Seven in ten hours are conversations, most of them retention offers": under the round-2
  shares January's conversations go to the offer 45 per cent of the time and the retention offer's minutes are under
  half the talk in January and March; retitled to the measured two-thirds (0.665 to 0.693, asserted).
- Band shares as a Critical Component (88 against 28 per cent at drops of 1.50 to 1.75): a corridor member (special
  money pooled, a logistic within each class) never computes them; the component keeps the class's 87 per cent and the
  bands stay in the steps.
- Portal round 1 (2026-10-25): response 1 landed the call exactly, 5,250 agent-hours (1,250, 2,000 and 2,000 by maturity month), so reading each reached holder's retention-offer share by the class of the money (the 2023 four-year special's block at 5.65 per cent against its cohort's 5.15) is a reflex for the portal's model, as the drop was for the audit's; with both the drop and the class spent, the world's deposit behaviour layer has no decisive step left, and the one structural step it still holds (a reached holder's conversation settling the holder's later deposits on the list, so hours follow holders, not deposits) reads the same with a clinic's reminder calls, a backdrop by the swap test.
- Re-root to architecture 2 (2026-10-25): architecture 1 spent on portal round 1 (above); the slot moves to a new
  cell, healthcare-delivery-health-economics / utilization-access-demand-forecasting, with nothing of the seed's world kept.
- Architecture 2 draw, coastal high-water flood days in 2027 from the window's astronomical tide plus skew surge
  (climate-weather-extremes): dead on the slots screen, it is task178's architecture 1, spent at Gate F when a scored
  reader conditioned on the 2027 tide table; the prototype (`tide.py`) had shown 2027's tide-only exceedances 15 to 25
  per cent under 2026's at a semidiurnal port.
- Architecture 2 draw, candidates killed on the lane's dead lists before code: bike-share pairs and pupil yield by
  estate age (task170's ninth cell), event prediction and illness-death states (task171, task174), the disposition
  effect in listings and notification habituation (task177's rate-by-state screens), vacancy chains (too close to
  task166's live junior-on-senior driver), OR-list overruns and clinic slot cascades (task170's replay law).
- Architecture 2 draw, a liability book's back-loaded accident year (`res1.py`, two seeds): the accident-year chain
  ladder missed by -36 to -42 per cent but Bornhuetter-Ferguson and frequency-severity on earned exposure landed within
  5 to 14 per cent: the textbook fallback for an immature year is the golden, so dead.
- Architecture 2 draw, warranty claims on a months-in-service clock a new retail channel delays (`war1.py`, two seeds):
  the shipment-clock default missed by only -2 to -5 per cent; dead on lever.

- Interacting pairs as the decisive step (the registered card's, 2026-10-25, restarted thread): a strong enumerator's own
  pick, so on the enumerable chain. On the generator's world a logistic with the canonical pairs wins out of sample
  (log-likelihood -1,629.7 against -1,741.2 per medicine and -1,641.8 for every two-way pair, 2023 to mid-2025 fitted,
  the next nine months scored), and replayed on the regimens the reviews left it files 191 admissions against the
  golden's 343; the pairs stay as a rung any solver climbs, and the decisive step moves to the stopped medicines'
  restarts.
- The dead thread's restart world with the programme counting as each resident's annual review: the 2027 annual reviews
  then all fall in October to December 2027, and leaving them out filed 9 per cent high, a fork between two readings of
  the procedure; the programme is now additional to the annual review, which continues in its usual month, so an
  implicit stop hazard over every month and explicit 2027 reviews agree within 1 per cent (345.4 against 343.0).
- Start hazards scaled by frailty: the pooled restart clock then sat 3 to 6 per cent under the truth, so a frailty-
  stratified estimator would have crossed a bin; the start and restart hazards are frailty-free and the record's clock
  recovers the truth within 1 per cent.
- Pair partners stopped only where the pair is held, with small main effects for NSAIDs and benzodiazepines: the per-
  medicine model with a pooled start hazard landed within 1 per cent of the golden (two errors of opposite sign); the
  criteria now stop NSAIDs and benzodiazepines in every regular user, their own effects carry most of their harm, and
  that route sits at 329 (4 per cent under).

- The restart clock as the decisive step (the stopped medicines restarted on the record's clock from each earlier
  stop), probed 2026-10-26 on a six-file pack (golden 343.0, nearest 25 = 350; frozen 191 to 220, pooled Markov 295):
  two isolated Opus call-only probes landed it, p137a at 350 (355.4) and p137b at 350 (361.9), each with a monthly
  Poisson rate on the month's medicines and their combinations, frailty and care type, validated on October to December
  2026, every medicine switched month by month with recent stoppers restarting faster and about three in ten stopped at
  an annual review, a leaving hazard and a microsimulation, back-tested on the 2024 and 2025 year-start cohorts within 2
  to 5 per cent. Any transition the record shows as a rate gets measured; dead. Their realism catches carried forward:
  the programme stopped 93 per cent of the NSAIDs and benzodiazepines it reviewed against 31 per cent at annual reviews
  under criteria the schedule called the same; no annual reviews after 26 October 2026; 24 admissions overlapping the
  person's previous stay; discharge dates after the pull.
- The blanket-programme restart curve (the programme's stops restarting like Ferncliffe's 2025 blanket programme rather
  than like selective annual-review stops), prototyped 2026-10-26 before a probe: the pooled clock landed 9 to 17 per cent
  under it and the per-medicine model with the pooled clock within one bin (two errors of opposite sign); set aside
  unprobed for the coordinator's evidence from five probe deaths: every dead step put the decisive attribute on the frame's
  own units, where a thorough modeller joins it and measures it, and the survivors (task305, task306) carry a body the
  frame does not hold; re-registered on the step-down guests.

- The step-down guests as the decisive step (re-registered 2026-10-26, d1f3551d), probed on a six-file pack (probe3):
  Opus probe p137c took the step, filing 500 (502.4) as 407.4 for the long-term residents plus 95.0 for the step-down
  guests (37 drug-event readmissions over 23,576 occupied bed-days, 180 beds at 92.1 per cent occupancy), because Annex A
  split each home's beds into long-term and step-down. No honest rebuild hides them: the golden is determinate only if a
  file states the 2027 step-down beds (an annex, a bed plan, a purchase order or a registration variation), and the
  probe cross-matched every file by NHS number (it found the 81 guests who became long-term residents, none on the
  register); if the trusts' returns carry the guests, they are an unmatched block, and if they do not, the guests' rate
  has no determinate source (an analogue choice is a fork). Dead in this world.
- The households other councils placed in Hartmoor's hotels and hostels as the decisive step (architecture 3's first
  candidate, a borough council's 2027 Part 7 assessments; probe pack probe5, golden 1,400 against the frame's 1,200, never
  registered): Opus probe p137f landed it exactly, 1,400 (1,383) and both asks. The block bookings showed as 655 s208
  notices in Q4 2026 against about 20 a quarter, and normalised addresses linked 151 of the 324 earlier placed households
  to later cases (47 per cent, about 27 per cent within a year), a direct analogue in the same files, carried to the 2027
  window by a Kaplan-Meier curve. Every landing so far had an anomaly that invites a look plus an analogue a join can
  measure; the next candidate keeps the outside body steady and quiet, applies a validated model to a situation the
  record's units never had, ties the body to the quantity by an indirect domain link, and forces its size and rate from
  ordinary data with other uses.
- The serving personnel beside a new urgent treatment centre as the decisive step (architecture 3's second candidate,
  Harrowdown ICB's Wexley UTC, 2027 attendances; probe pack probe6, golden 12,500 against the model's 11,000, never
  registered): Opus probe p137h landed it, 12,500 (12,456.7) and the ask. It ran the model as filed (10,846), then
  calibrated the open centres' other attendances as 0.98 per cent of ICB attendances plus 0.99 times the model's demand
  for the census defence population, a fit that matched all three centres and explained Tolland's higher share by the
  RAF station; it knew the personnel are registered with Defence Medical Services, and it excluded the prison and the
  halls students correctly. Defence was the communal establishment table's largest category, and the open centres
  carried enough of it to calibrate the rate. The next candidate's outside body is small wherever the solver can
  measure it, absent from the open units, concentrated on the new one, and sized from data the model does not use.

- Re-root to architecture 3 (2026-10-26): architecture 2, the care world, is spent on probes (the pairs, the restarts and
  the step-down guests above), so the number moves to urban-regional-science / municipal-service-demand-resource-allocation
  with nothing of Calderbrook kept; architecture 3's first two candidates (above) died at the probe gate before
  registration, and the third, the Tanner Street custody hub (Harrowdown Police's on the probe pack, Calderwick Police's since stage 3), was missed by both probes (`## Draw`).

- Stage 3, ask B as each suite's initial health assessments in each quarter (16 figures): the closures reached only the
  quarters they fell in (six of sixteen cells), so a reader who joined the handover lines and kept the labelled suites
  kept ten; moved to day and night by suite (eight figures), every one of which a closure reaches (B6, B7).
- Stage 3, ask B framed as the custody healthcare tender: a second decision with its own owner (H18); its home is now
  the medical rooms of the same fit-out contract.
- Stage 3, Wendle Cross's refit as the only closure: it reaches two suites; Eastmoor's 19-day flood closure in August
  2025, with its team at Northgate, reaches the other two.
- Stage 3, an overflow booking into Wendle Cross during its refit: the nearest-suite overflow ignored the closure, so
  the arrest records' longest Wendle Cross gap fell inside the refit (22 December to 12 January); a closed suite takes
  no overflow.
- Stage 3, the refit's move at its planned 08:00: assessments of detainees booked before the move but seen after it
  read either way; the move is the minute after the last booking, and Eastmoor's planned closure was set at 14:20 so
  that no assessment of a detainee booked before either closure falls after it (B4, C1).
- Stage 3, co-defendants charged at the first-named defendant's time: the file's charge time served every defendant on
  it, so attaching them at the file's times was right; they are now charged in turn after the first-named defendant.
- Stage 3, every file keyed to its own detention: the co-defendant join was the only reconstruction and the reverse
  unmatched join finds it; 104 of the 2025-26 files now carry the case's earlier arrest, as a remand file does when the
  person was released and arrested again.
- Stage 3, a file matched to its detention by suite and charge time alone: two unrelated Southfields defendants were
  charged at 05:18 on 10 October 2025; the linked arrest is taken first and the charge-time match only where the linked
  arrest is an earlier release.
- Stage 3, the detention clock on UK wall-clock times: a hold across the October clock change came out an hour long;
  the clock is elapsed time in UTC and the remand times are its UK reading.
- Stage 3, remand stream 0 and 1: a cell-hours sum 0.02 hours from its rounding edge and a hold within two minutes of 24
  hours; stream 8 clears both (A4, A5).
- Stage 3, the probe pack's personas (Charlene Dale, Hugh Metcalfe): `guard.py names --geo GB --seed 137` does not give
  them; replaced with Liam Clayton and Emma Roberts from that draw.
- Stage 3, the BTP part as a graded figure to the nearest 10: the four sizings print 260, 270, 280 and 290; the part is
  stated with its method in the write-up and only the call is graded on its print.
- Stage 3, the city and force named Harrowdown (the probe pack's name): it contains Harrow, a real London borough
  with its own school, and is the name of a real Oxfordshire hill (H21); renamed Calderwick, with the estate's postcodes
  moved off the real HD and CV areas to unassigned ones (CK, CL). No figure moved.
- Stage 3, the prompt's question without the catchment: the estimand read only "the detentions the hub will book";
  it now names the six city centre wards the hub takes over, which is model 2.1's population and the domain's
  catchment (H20).
- Architecture 3 spent at stage 4 (2026-10-26, on d1d38e72): the determinism judge returned DETERMINISTIC on every
  committed figure with disposition SEND_BACK. Gate G read the call as a single conceptual flip (stumping family
  surface_read_rejection, surface_read_dependency yes, sole_data_defect yes) and Gate H its decisive step as
  data_semantics: the flip rests on the brief's coverage line ("one row per arrest by a Calderwick Police officer") and
  allocation note 2, and any BTP figure from 121 to 371 rounds to 4,000, so once the note is read nothing analytical can
  go wrong. Both scored readers landed 4,000: reader A (Sonnet) quoted note 2 as the decisive-step sentence (5 of 21 ask
  figures, 23.8 per cent, all five the chart's years; score_reader exit 1), and reader B (Opus, 3,754 plus about 265 BTP)
  wrote that what flips the answer between 3,750 and 4,000 is close to reading a stated rule and a field's definition.
  Neither took an ask figure: both re-keyed the files carrying a case's earlier arrest and missed the co-defendants, and
  both counted the closed suites' teams at their own suites. The probes missed only while the coverage fact was unfiled;
  filing it, which determinism needs, makes it semantics and lands it, so the same fact cannot be both Gate B's pin and
  silent. The judge's other findings, kept for the record and not fixed: pin 19:00 (nine first assessments start
  exactly then), pin the assessment unit and the "where it happened" wording, say defendants are counted from the arrest
  records, and the model PDF's header still reads HARROWDOWN POLICE (an upper-case leftover of the rename); reader B
  also flagged the HDL licence prefix and four arrests at the spring clock change booked before their arrest time (a
  local time in the skipped hour converted as GMT). By build-pipeline an architecture is spent on a SEND_BACK, and the
  retirement rule applies to this third spent architecture unless the author sets another cap; that decision is the
  author's, and no architecture 4 is drawn.

- Re-root to architecture 4 (2026-10-26): architecture 3 spent at stage 4 (above) and the author's ruling the same day
  that task137 is neither retired nor paused; the number moves to healthcare-delivery-health-economics /
  utilization-access-demand-forecasting with nothing of Calderwick kept.
- Architecture 4 backup candidate (probe8, 2026-10-26, never registered): Kestermoor District Council's 2027-28 Annual Tonnage Nomination to the Thrumley ERF, kerbside residual after a staggered weekly food waste rollout (two caddy-only pilot waves, then three waves that also swapped in a 180-litre residual bin, the 48-round wave 4 six periods in, wave 5 live from 2027-28 period 1), golden 53,000 against 55,000 to 58,000 for the static and pooled TWFE routes; died on Opus probe p137lb, which landed 53,000 (53,174.5) by comparing each wave period by period with wave 5, the one not yet treated, splitting the two packages and running wave 4 along wave 3's path: the package column in the rollout schedule hands over the clean comparison by package, so a staggered rollout with a documented package split is a reflex for the probe model, not a stump.
- Architecture 4 draw, explorer B's families: demand censored by capacity and vintages, never the staggered rollout. The
  recapture form (a patient turned away comes back on a later day and is counted twice, so only the refusals that never
  return are demand the record missed) was dropped before code: a regression of later days' visits on the turned-away
  counts is the opponent's own return check, which both probes then ran unprompted on probeB1. The deterrence form
  (a week of run-outs keeps the next week's patients away) went to the probe pack.
- Architecture 4 probe pack probeB1 (seed 16, a deterrence of 0.30 on every arrival, golden 54,000 against the default
  51,000 at the nearest 1,000): both Opus probes missed (`## Draw`), but its own rolling five-day share attenuated to
  52,000 (52,046) and its clean-day fits printed 49,000 and 52,000, forks a full pack could not ship.
- Stage 2 prototypes v2 and v3 (the deterrence on every arrival, the run-outs from staffing shortfalls): whenever the
  run-outs were scattered the rolling-window members attenuated a cell under the previous-week share, and a vacancy
  overlapping a surge gave the vacancy a t of 3 or more. The run-outs now come mostly from the hospital clinics' recall
  programmes, which run for weeks; the vacancy sits in summer; the bank backfills the long-term sickness lines; so every
  window files one call and staffing has no effect of its own (t 0.29 for the vacancy, -0.20 for staff on the floor).
- The deterrence on every GP-referred patient: it is now held by the seven practices with their own phlebotomy clinics
  (arrivals times exp(-0.45 x the previous week's run-out share)), the five without one untouched, so the step is a
  referral pattern the request forms' practice codes show rather than a property of every patient.
- The plan to the nearest 1,000: the deterrence specifications spread 44,035 to 45,114 across two cells. At the nearest
  2,500 they sit in one (43,750 to 46,250), with the default (42,561) and both careful-frame methods one cell under.
- A practice barcode blank on 3.1 per cent of GP forms: a solver counting GP-referred visits by practice code would
  have moved the call; 0.6 per cent now (426 forms), the same call either way (SF1).
- The annual report's sentence on the hospital clinics' recall programmes (which months each specialty recalled its
  patients): it named the run-outs' driver and made the GP dips readable beside it; removed, the programmes show only
  in the hospital-form visits by clinic code, which ask A counts.
- Personas outside the seed-137 draw (Liam Clayton, carried from architecture 3) and from it with first names older
  builds use (Rachel Reynolds, Patricia Bryant; Richard, Rebecca and Duncan also warn): replaced with Charlene Dale,
  Bethan Matthews and Joseph Wood from `guard.py names --geo GB --seed 137`.
- Strategy `causal_design` on the card: `ban.strategy` against task121's architecture 6 inside the three-build window,
  and `informative_censoring`, the nearest key, is task487's; filed as `other`.
- Brantmoor Community Hospital's booked clinic left unstated: with the turned away offered a booked slot there, "the hub
  takes every patient with a GP request, walk-in and booked" left open whether Brantmoor's own booked patients move to
  the hub, which no file counts; the annual report now says the booked clinic at Brantmoor carries on as now (SF10).
- A family-spread assertion at 0.4 of the printed unit: the 27 specifications spread 0.43 (44,035 for the programme-week
  dummy to 45,114 for the quiet-period fit over ten clinic days), every one at least 285 inside the cell; the assertion
  is one printed cell and a spread under 0.45, with the figure stated rather than the family trimmed.
- Stage 4 on zip 6611e937 (2026-10-26): the judge returned DETERMINISTIC with APPROVE (Gate G statistical_rigor,
  analytical_non_defect; Gate H analytical), and both scored readers missed the call at 42,500 (Sonnet on seen plus
  turned away, Opus on run-out days completed from the arrival profile); the asks leaked, the Opus reader keeping 36 of
  36 and the Sonnet reader 8 of 36.
- Ask A's device as a same-string reallocation of the clinic codes on 1 April 2026 with `code_in_use_from` in the
  register: the Opus reader read the column, mapped each old code by its request weekdays to the register's clinic days
  and took all 28 cells. Replaced by the new PAS's codes from 16 March 2026 and the 2026-27 templates from 1 April, which
  make that same weekday route name every old code wrongly; the link runs through the March fortnight instead.
- Ask B's device as one long-term sickness row carrying the absence's hours (270.00 and 337.50 on one day): an
  impossible day both readers spread over clinic days, taking all eight cells. Replaced by the e-roster unassigning a
  holder's line after five clinic days of sickness, so the absence reads as vacancy unless the holder is followed.
- The annual report's sentence dating the two long-term absences: it narrated ask B's device and went; the report keeps
  the one vacant post, and its definition now says vacant posts rather than vacant lines, so the literal execution is the
  golden.
- Clinic days left on the old weekdays after 1 April 2026: the old codes' weekdays then match their own specialties in
  the register and the careful route is exact; the 2026-27 templates give each specialty another's old weekdays, every
  set moving, so no old code keeps its match.
- Post-April requests moved to the nearest earlier template session: General medicine's requests stayed on Fridays while
  the register lists Tuesday, Wednesday and Friday; they are now drawn over the template's sessions in the week before,
  from their own random stream, so no other record moves.
- Item (a) of the judge's report: the underlying base printed as 41,714 reproduces only under the generator's exact
  specification (the judge refitted 41,663, the same plan); block 1, critical component 3, steps 3 and 4 and the golden
  workbook now state the model's figures to the nearest 100 (about 41,700, about 2,000 kept in-house, about 44,700 grown,
  a coefficient of about -0.21), counted figures exact. freeze.py rubric mode reports those three numbers as moved, which
  is item (a); nothing else on the main side moved.
- Item (b): "walk-in and booked" in section 6 left open whether booked GP patients at other sites join the hub; the
  report now says the hub's booked slots are for the same patients, who can book rather than queue.
- Stage 4 round 2 on zip d3c6d25d (2026-10-26): the judge returned DETERMINISTIC with a FIX_NOW on the intermediates'
  wording (applied as bands, the ship-ready zip 5c27c2ab), the Sonnet reader filed 42,500 with 0 of 36 asks, and the Opus
  reader landed 45,000 with 8 of 36: it fitted open days' GP-referred visits on weekday, financial year and month terms
  and ten daily lags of the days the kiosk filled (the lags summing to about -33 visits a run-out, peaking a week later,
  placebo leads flat) and predicted every 2025-26 day with no run-outs. The previous-week version died there: with the
  practices' in-housing held to the one calendar week after a run-out week, a fortnight of daily lags held all of it,
  so the careful reader's model was the golden's.
- Hardening screen on the clean world (seeds 26 to 37, the practices' in-housing persisting L weeks with a uniform
  weight, strength K): L 4 at K 0.45 to 0.9 left the ten-lag route at 45,000 on one to three seeds of 12, and twenty lags
  landed on 10 to 12; L 6 put the ten-lag route at 42,500 on 11 or 12 of 12, but twenty lags landed on 1 to 8 and thirty
  on 10 to 12; L 8 at K 0.75 to 0.8 put the ten-lag route at 42,500 on 12 of 12 with 1,120 or more to spare, twenty lags
  on none, thirty on 2 to 4, and the window chosen by AIC at 45,000 on 12 of 12. A geometric decay chosen by AIC read
  high (45,552 to 46,635 at K 0.8, one seed at 47,500), so the shipped seed was chosen with it at least 250 under the
  cell's top.
- Shipped-world seed screen (`generator/seeds.py`, the staffing seed 31 kept so the e-roster and ask B are unchanged;
  demand seeds 1 to 60 under L 8 at K 0.75 and 0.8 and L 7 at K 0.8 and 0.85): 31 of 240 worlds held every clean-world
  margin and 24 of them kept thirty lags off the call too. On the cut pack demand seed 48 at K 0.75 counted the
  parallel-run fortnight twice into 47,500 (46,408) and left an exposure form 136 inside the cell's top; seeds 1, 11,
  18, 21, 46, 55 and 56 each failed one or more assertions (an exposure form or twelve weekly lags within 250 of an
  edge, the fortnight counted twice leaving the cell, the trend cheaper than 100 in AIC, five weeks within 50 of the
  best, the eight-week window not picked, thirty lags reaching 45,000, a repeated count); demand seed 14 at K 0.8 passed
  every one.
- Records seed 31 under demand seed 14: Rheumatology's 2025-26 hospital-clinic visits read 363 in three quarters and
  Renal medicine's 411 twice, and seed 32 repeated a Gastroenterology quarter; a row with a value repeated across its
  quarters reads as a fill-down error, so seed 33, the first with four distinct quarters in every row, ships, and the
  rule is an assertion.
- The intermediates' band over the previous week's share and the previous ten clinic days' share (the round 2 fix): both
  windows are rungs now, so the band runs over the window the fit picks and the window next to it in fit (eight and
  nine weeks, 2.7 apart in AIC).
- The shipped pack carried `data_dictionary.csv` (column descriptions for seven files), which the new leak gate reads as a
  file describing the data: dropped 2026-11-01. Closure axis 19 now rests on the annual report's activity note and the
  systems' own labels, asserted with the data's convergence; the ask-side lines (Vacant line, request_date, clinic_days,
  clinic_code) left unstated, since the report's section 4 and the prompt's pins close the asks without them.
- Step 3's "every window of five weeks or fewer at least 67 worse" (the whole record's own margin) shipped on 8f5c6aa2;
  judge pass 5 reproduced 65.3 on the whole record and 62.6 on a common sample, so the step now states a bound computed over
  four samples (60, SF11), and steps 5 and 6 each gained one clause on the evidence that separates ask A's late-March
  link from the register's clinic_days and ask B's holder stretches from vacancies (SF12, SF13), no document changed.
- The ceiling recorded on the reship cut was a narrowed cracker's (2026-11-01, honest-cracker audit): the careful solver, every field read by its plain meaning, every filed rule executed and the hygiene battery run, keeps 8 of 36 against the recorded 0 of 36, SPENT on Ask B (Ask A holds, weakly), pair 40.7; the reason in one line: the annual report's section 4 names the one vacant post, so reading every unassigned line as vacant contradicts a filed fact; the other 67 follow a holder's Sickness lines. The ask layer is owed a /fix-rubric pass before delivery; the leak repair stands.
- The /fix-rubric re-site of Ask B (2026-11-01, after the honest-cracker audit) found no device that passes both tests, so nothing shipped: section 4 fixes each quarter's filled post-days (427, 411, 448, 441), the kiosk's 40 and 32 ticket rule and the queue bays fix which holders were off the floor each day (40, 45, 56, 31 holder-days), so only the label on those days is free and only the run it sits in can force it, which is the battery's sequence check; an as-of bank label on a holder's absence lines (43 label flips, 46 days at six substantive lines), a shadow key carrying her absences (never on the floor, 46 days at eight lines), a sickness keyed as worked (the ticket rule broken on every such day) and a relabelled absence type (no file records the type, so unforced) all died, new hospital-side records hand over Ask A's code link and GP-side ones carry the in-house signal; Ask A cannot be strengthened cheaply, its rows sitting in the queue export the call reads.
- The sickness ask cut and Ask A measured on its own (2026-11-02, the coordinator's decision after the re-site found no Ask B device): the cut moved no pack byte (target.zip md5 8f5c6aa2, every file the call reads asserted byte-identical) and no main-call figure (freeze rubric PASS), but the careful-solver cracker lands Ask A, because a careful solver tests the register's clinic_days on the 805 register-coded 2025-26 visits before naming the 16,417 old-code visits by them, the test fails on 328 of them with every off-schedule form issued 16 to 31 March and none from 1 April, and the late-March link follows (generator/ceiling.py: 28 of 28, pair 83.5, mirror leakage 100.0 per cent); nothing shipped, and the ask layer is owed a device on records the call does not read.
- The full replacement on new ask-only records (2026-11-02, /fix-rubric step 4b) found no device that passes both tests, so nothing shipped. The attempt was the anticoagulation service's dosing-system export of 2025-26 INR results, asked as the venous INR checks the walk-in clinic drew each month and the patients they were for each quarter (16 figures, the INR part of block A's residual that the ICB letter's 12 per cent a year moves to community pharmacies), prototyped on the generator's world and dead on the careful solver both ways: the anticoagulation clinic's own venous confirmations surface as same-patient same-day pairs in the near-duplicate item (101 pairs; 6 to 20 minutes after the clinic's fingerprick against 31 minutes or more after a pharmacy's), and Brantmoor's booked venous INRs surface in the received clock's hour profile (12 to 21 results in one minute on Monday and Thursday mornings, the courier's batch) and in the per-day check against block A's Haematology-form visits (28 days over), with the delay alone no clean forcing (walk-in up to 26 minutes, Brantmoor from 19); a reader told either finds it in a few lines. On paper: every hospital-clinic visit count is pinned by the frozen queue export (day, code and issue date, the new codes naming their specialties and the late-March weekday sets linking the old), hospital-clinic patients carry only identity devices (the batch's monoculture), requests, orders and re-bleeds die to key uniqueness and near-duplicates or are the refiled family, staff records are fixed by the bays and the 40 and 32 ticket rule, consumables, incidents, pay arrears and survey records die to the battery or fail H18, other service lines (inpatient rounds, the INR line's base) fail H18, GP-side records carry the in-house signal and Brantmoor's activity reopens SF5 and SF10. The ask layer needs a route outside /fix-rubric scope.
- The re-cut of the hospital forms' request_org and request_date, the fields the call never reads (2026-11-02, the main thread's route, one ask-only record allowed), found no device that passes both tests, so nothing shipped and no pack byte moved (target.zip md5 8f5c6aa2): each quarter's hospital-clinic visits are pinned by the check-ins the standing family reads, so the specialty split is the ask's only free dimension, and with no patient key or test on a hospital form the only hard contradiction of the register's mapping is a schedule one, which the careful solver's code-against-schedule validation and re-key item perform. Measured on the generator's world (session scratchpad task137_askrw2, nothing written to the pack): every variant that keeps a late-March link is landed (the shipped and a six-day window 28 of 28, off-schedule 0.43 and 0.55 before April against nil after; benign off-template forms at 0.05, 0.15 and 0.30 still 28, 28 and 24 of 28 at 0.45 to 0.50 against 0.04 to 0.21); a three-day window leaves the link unique for two codes of seven (8 of 28 landed, the rest unforced); the no-overlap re-cut (new codes and templates both from 1 April) is missed in all 28 cells but leaves the register's weekday mapping a clean one-to-one reading that no row contradicts (no form on a bank holiday or after its visit, and level continuity across April as good under the mapping for three codes, x0.81 to 1.07, as under the truth, x0.87 to 1.24 outside Rheumatology's recall); a fasting-share fingerprint on the free pathway field links six codes of seven and keeps both readings coherent (every fasting share moving at April, or every weekday set); Haematology's forms losing their barcode from 1 October 2025 drain its coded Q4 to nil beside 495 blanks, seen by a per-specialty series check and read literally as unattributed visits; an ask-only PAS session list under the new codes forces the link (exact weekday sets, seven of seven) and is the re-key item's own crosswalk (28 of 28); on paper, a shared block printer's code is re-derived by weekday or, on a shared weekday, unforced, and a request number with stale-form scans resolved by a bay collections file leaves the scanned form and the drawn request as two readings of a visit's specialty, the two sources' disagreement sending the careful solver to the bay-and-time join.
- Re-root to architecture 5 (2026-11-02): architecture 4 (the phlebotomy hub) kept a sound call (judge pass 6
  APPROVE) but its ask layer was spent: the honest-cracker audit landed both asks, and every /fix-rubric route on that
  world (the e-roster re-site, the INR replacement, the hospital forms' request fields) found no device both tests pass.
  The slot moves to Actuarial Science & Insurance (claims frequency for a self-insured delivery fleet), a client domain
  no architecture of the lineage used, with a new world, dataset, generator and shell (how-many | use | docx+xlsx
  against architecture 4's how-many | plan | png+xlsx); the ask records were named before registration this time.
- Draw candidates screened and dropped before this one (2026-11-02, paper and code): unemployment insurance benefit
  weeks after a potential-duration cut (the exit hazard riding the weeks left to exhaustion is task176 v2's external
  clock, and the behavioural response is the labour field's own reflex); job-search displacement at full rollout
  (`causal_design` in the three-build window, and the swap test fails: a hospital's discharge team competing for care
  home beds reads the same); selective lapse after a repricing (adverse selection is the insurance reflex); a TV
  campaign's audience decaying through longer breaks (a layout moving units into worse positions, task163's abstraction);
  a fleet forecast with the darkness rate taken from a ramp through civil twilight at 2.6 and day runs returning before
  dark (prototype `proto2.py` to `proto4.py`: the record's dark kilometres were 4 to 5 per cent, the dark rate's own
  noise spread the golden family by up to 15 per cent, and the overall per-kilometre rate landed within 5 per cent of
  the golden on most seeds because the darkness only moved from evening rush to quiet mornings).
