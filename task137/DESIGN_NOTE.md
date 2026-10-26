# task137 design note

Architecture 2, drawn 2026-10-25 (wave 2 slot, Forecasting lane, sathya8571), a re-root after portal round 1, decisive step
re-registered 2026-10-26. Architecture 1 (Kaimai Building Society's maturity calls booked in agent-hours, seed FC08) was
landed on its golden by a portal response; its identity is in the card's lineage and its dead ends below. Nothing of the
seed's world is kept, and no banking: this draw is a care home group's 2027 baseline of emergency admissions for adverse
drug events. The draw's first two decisive steps (the interacting pairs a resident holds; the restarts of the medicines the
autumn 2026 programme stopped) died before any pack was cut, the second to two isolated Opus probes (`## Tried and
rejected`); both stay as rungs every careful solver climbs.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task137.json`, architecture v2, re-registered 2026-10-26 (`guard.py check` WARN,
   `ban.source` only: every pack on file is constructed; `test.same_puzzle_older` and `test.same_driver_older` NOTE,
   differentiated against task133, task196, task180 and task305).
2. Pairing: Healthcare Delivery & Health Economics (client domain) / `utilization-access-demand-forecasting` /
   Forecasting & Predictive Modeling. The deciding quantity is a care provider's 2027 emergency admissions for adverse
   drug events over every bed it provides, a utilisation forecast whose denominator is two populations.
3. Niche: Calderbrook Care, a care home group in the north of England (34 homes, about 2,400 long-term beds, six homes
   joined from Ferncliffe Lodge Homes in April 2025). Its 2027 gain-share agreement with Wethermoor Integrated Care Board
   pays against a baseline Calderbrook proposes: the emergency admissions for an adverse drug event of every person
   accommodated in its beds during 2027. Since April 2025 the board has also bought discharge-to-assess step-down beds in
   six of the homes (40 beds), booked through the board's placement system; the 2027 contract buys 180, across fifteen
   homes, from 1 January 2027.
4. Call and shape: the 2027 count (`quantity_figure`, question form how-many), rounding fixed at stage 2 from the family
   spread; shape `02` (the call with its path by quarter and an ask layer counted in `## Ask sheet`).
5. Mechanism keys: gap population (the residents register, and the returns drawn on it, are not everyone the baseline
   counts); pattern none, generators G12 (the register's silence about the guests read as nobody there), G3 (the register
   records residents, the beds accommodate guests too), G6 (the forward year's beds hold four and a half times as many
   guests); Gate G `forecasting`; strategy `population_selection`.
6. Layer 2: `field_method`, pattern `own:utilisation-denominator-covers-the-step-down-beds-off-the-register`.
7. Furniture: forum `executive_team` (the executive team signs the agreement); forcing event `purchase_order_or_contract`
   (the 2027 gain-share agreement and step-down contract); organisation family `hospital_or_health_provider`; role family
   `operations_director` (the director of clinical services prepares the baseline); context artifact `capacity_report`
   (the homes' 2027 bed plan, kept for staffing and registration); calibration `realised_outcome_roster` (the board's
   placement returns since April 2025: each step-down placement's dates and how it ended).
8. Spine: Fellside Pharmacy Services' monthly dispensing for the long-term residents, January 2023 to December 2026.
   The forcing files are the board's placement returns and the bed plan; other files at stage 3.
9. Deliverables: `ade_admissions_forecast_2027.xlsx` and `review_impact_note.docx` (checked against the last three builds
   at stage 2).
10. People, drawn with `guard.py names --geo "United Kingdom" --seed 137`: Katherine Storey, Hugh Metcalfe, Charlene Dale,
    Richard Davies, Emma Roberts.

**Data-native sentence.** A discharge-to-assess guest arrives from a hospital ward for a few weeks of assessment before a
decision on long-term care, in the first weeks after a stay when a changed regimen is most likely to bring them back, and
the board books the bed on its own placement system: the guest is never on Calderbrook's residents register, so the
trusts' returns, drawn on the register's NHS numbers, never carry their admissions, and the record the residents' forecast
is built and checked on is complete without them.

## Three rules

Task type: utilization-access-demand-forecasting (healthcare delivery), which serves Forecasting in the taxonomy: a care provider's emergency admissions in a coming year over every bed it provides.
Domain test: the deciding quantity is the 2027 emergency admissions for adverse drug events over every bed-day Calderbrook provides, a utilisation forecast whose denominator is two populations with different exposure: long-term residents, whose risk follows the medicines they hold, and discharge-to-assess guests in their first weeks out of hospital, whose readmission risk the step-down placements' own outcomes measure; a hotel's guests have no discharge-to-assess pathway, no first weeks after a hospital stay and no medicines the risk follows.
Swap: "the baseline counts the step-down guests the register never holds" with a hotel group's guests and its loyalty members reads as nothing: there is no placement booked by a commissioner, no assessment after a hospital stay, and no adverse drug event whose rate a readmission return measures.
Layer 1: two pharmacy suppliers' feeds coded differently, the acquired homes' eMAR with its own resident numbers, the trusts' returns in two layouts with the adverse-effect codes in secondary positions, a coding backlog during one trust's system change, residents' NHS numbers in mixed formats, the board's placement return in its own layout; each is what these systems produce, none carries the call.
Layer 2: field_method: the utilisation forecast's denominator is every occupied bed in 2027, so the residents' model (medicines, the autumn 2026 programme and its restarts) is completed by the step-down guests, sized from the bed plan and priced per occupied bed-month from the board's own placement returns.
Decisive step: carrying the step-down guests as the second population of the baseline, their 2027 bed-months from the bed plan's 180 beds at the placements' measured occupancy, their adverse-drug-event readmissions per bed-month from the placement returns since April 2025, rather than taking the residents register as everyone the baseline counts.
Not semantics: every field reads as what it is; the register is complete for residents, the returns for the register's patients and the placement return for the board's placements; no field says the guests are missing from the residents' forecast, and an analyst who reads every field correctly still forecasts the residents alone.
Not rule application: the agreement files the WHAT (every person accommodated in Calderbrook's beds during 2027, from arrival to departure, emergency admissions with a Y40 to Y59 code, calendar 2027, the rounding) and nothing about how the count is built; executing it needs the guests modelled, which no rule describes.
Analyst test: a strong analyst who links every file to the residents, fits the residents' admissions on their medicines, frailty and care type, carries the autumn reviews and the medicines' restarts, and back-tests on the 2024 and 2025 year-start cohorts files the residents' 2027 admissions, about a fifth under the golden (measured on the prototype at stage 2).
Estimand: emergency admissions for an adverse drug event (a Y40 to Y59 code in any diagnosis position) beginning in calendar 2027 of every person accommodated in one of Calderbrook's beds at any time in 2027, each counted while they are accommodated there; filed in the agreement's Schedule 2.
No decoy: nothing is planted; no memo, draft or figure argues for a count; the placement return is the board's own monitoring of the contract.
No certified replay: no certified figure is reproduced; the residents' history reconciles and the guests' are measured from their own returns.
Lesson: a provider's utilisation baseline is only as complete as its population; a commissioner's short-stay beds inside the provider's homes hold people its own register never sees, and their own placement returns are what price them; no build on file prices a care population that lives off the provider's register.

## Default path

1. Link Fellside's dispensing, the Ferncliffe eMAR and the reviews to the residents register; code each trust return's
   admissions to an adverse drug event (Y40 to Y59 in any position) and link them to residents by NHS number.
2. Fit the residents' monthly admission rate on their medicines and the interacting pairs, frailty, care type and time
   since admission; carry the autumn 2026 programme's stops and the medicines' restarts month by month, the annual
   reviews in 2027, exits and new residents (the probes' microsimulation).
3. Back-test on the 2024 and 2025 year-start cohorts (both reconcile) and file the residents' 2027 total.

Ends on: the long-term residents' 2027 admissions (figure measured on the prototype)
Golden: the residents' admissions plus the step-down guests' (figure measured on the prototype)

## Stump sentence

A competent analyst models Calderbrook's long-term residents from the register, the dispensing and the trusts' returns,
which reconcile month by month, and files the residents' 2027 admissions; the step that lands it there is taking the
register as everyone the baseline counts, when the step-down guests in the board's discharge-to-assess beds live in the
same homes, sit in no register and no return drawn on it, fill 180 beds from January 2027 against 40 before, and are
readmitted for an adverse drug event at about five per cent a month.

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

