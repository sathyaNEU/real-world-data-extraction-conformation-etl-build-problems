# task399 design note

Architecture 3, drawn 2026-11-03 (wave 7, Root-Cause lane, sathay3012), numbered from seed RC05 (a regional
electricity distributor choosing one reliability programme from five, where the costliest cause leaves no record of
its own). The seed's world collided at the draw screen; architecture 1 (Quantitative Finance) was spent at the draw in
task398's cell and architecture 2 (a bus operator's drivers' rest) at the draw as a template of shipped task121 v6
(`## Tried and rejected`, the card's lineage). Kept from the seed: the decision (one programme funded from a catalogue
of five), the quantity in kind (what each programme's cause cost over the last twelve months) and the kernel, a cost
that leaves no record of its own: a search that found no road-test slot leaves no trace of the shortage.

Norland Driver Services, a fictional Canadian province's licensing agency, books road tests through a self-service
portal that offers the slots open at each test centre within the next six weeks. New drivers licensed fell in the twelve
months to 30 September 2026. The executive team funds one 2027 initiative from five: the portal's booking redesign
(released March 2026), more examiner shifts, a hazard-perception practice module, a fee rebate, no-show reminders.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task399.json`, architecture v3, registered 2026-11-03 with architectures
  1 and 2 in its lineage. `guard.py check` on the draft: BLOCK test.same_puzzle_older against task121 v4 (gap,
  pattern and decision type) and people.first Melissa; cleared by the differentiation line against task121 (and lines
  against task307 and task254, the nearest drivers) and by drawing Christopher Wolfe instead. Re-checked on the
  registered card as the last act of stage 1: WARN only (first name Christopher in one older build, government_agency
  overused); the full names are new.
- **Pairing:** Product Analytics (client domain) / `funnel-journey-analysis` / Root-Cause Analysis; the subdomain has
  never been drawn.
- **Objective and call:** where in the permit-to-licence journey the fall came from and which initiative removes it,
  judged on the closed twelve months; the initiative runs in 2027, nothing is forecast.
- **Shape:** 09, a funnel of stages for a fall: each stage's volume, rate and the candidates it lost against the prior
  year, plus the call, the runner-up and the gap. Arithmetic in `## Ask sheet` at stage 2.
- **Strategy and Gate G:** `binding_constraint` for both: the examiners' slot stock is the limit, and the limit itself
  moves the naive pick off the booking redesign. Gap objective (the stage that shows the loss is not the stage that
  causes it); generator G3 (the portal records a search with no booking; the scheduling system shows no slot was open).
- **Furniture:** forum `executive_team`, forcing event `budget_or_appropriation`, org family `government_agency`, role
  family `product_manager`, context artifact `operations_log` (the scheduling system's slot log), question form
  `where`. None is held by task398, task277 or task274; shape 09 and `where` differ from task121's 18 and `what`.
- **People** (`guard.py names --geo Canada --seed 399`): Eric Davis (product manager, road-test booking), Brian
  Williams (director, testing operations), Christopher Wolfe (examiner workforce planning). None is in the prompt.
- **Data-native sentence:** the portal offers only the slots open within six weeks at the centre searched and logs a
  search that ends without a booking exactly as it logs one where the user simply left, while the scheduling system
  logs every slot released from an examiner's shift, every booking and every cancellation returned to the pool, so the
  shortage exists only as a stock rebuilt day by day from the scheduling system.
- **Semantic screen** (`guard.py mechanisms --objective root-cause`, one line per build on the insight it spends):
  task13 re-attributes outcomes from an exceptions-only log where absence means success; task11 a threshold rebate
  that makes the shallowest discount pay, seen only on a rebuilt ledger; task36 a filed rule excluding the largest
  candidate because an agreement already remedies it; task50 the share of each candidate's exposure inside a funded
  window, projected by a filed issue order; task72 booking a movement to the owner whose agreement covered each piece;
  task84 identical concurrently live units competing on a key nothing is keyed on; task111 which cause still operates
  in the forward window (overflow work landing late in the day); task500 a matched-reference method pinned by two
  certified statements; task129 a rise booked to a maintenance provider that scales with each unit's surroundings;
  task121 the conditions each response or event was made under (v4 journey conditions, v6 the rest before a shift);
  task202 the share of each input reaching the layer the response draws on; task398 an exposure rule driven by the
  whole's own path. **Is the new decisive step any of them in other nouns?** No: it rebuilds a stock (open slots per
  centre and day) from releases, bookings and cancellations and shows a funnel stage's loss sat where that stock was
  empty; nothing on file reads a stage's loss against a capacity stock behind the journey. The nearest are task121 v4
  (it conditions ratings on ambient journey conditions, no stock and no stage) and task111 (capacity overflow, but its
  step is which cause survives into a forward window).
- **Slots, run twice:** mechanism nouns (slot, capacity, inventory, booking): task179 (parole and jail bookings),
  task147 (a hotel block's bookings replayed against a cap, a forecast's order of operations) and task456 (a converter's
  VOC bypass), none this insight; setting nouns (driving test, examiner, learner, licence, portal): task130 (a licence
  register) and task277 (a portal), neither this world.
- **Library test:** the golden is not a named correction; the field's funnel reading (stage rates, release cohorts,
  segment cuts) sits at rung 1 and files the booking redesign.

## Default path

1. Build the permit-to-licence funnel for each twelve months (permits reaching eligibility, portal searches, bookings,
   tests sat, passes, licences issued), across the portal's search log and the testing records.
2. Compare each stage's conversion year on year: the search-to-booking stage carries the largest fall.
3. Segment that stage by release, device and centre: the fall starts with the March 2026 booking redesign and sits on
   the redesigned flow.
4. Fund the booking redesign's rework.

Ends on: the booking redesign (provisional figures at stage 2).

Golden: more examiner shifts, the search-to-booking loss read against the slot stock open when each search ran
(provisional).

## Stump sentence

A competent solver builds the permit-to-licence funnel, finds the search-to-booking stage carries the largest fall and
that it lines up with the March 2026 booking redesign, and funds the redesign (Ends on: the booking redesign); the step
that lands it there is reading the stage's loss as the portal's, when the scheduling system's releases, bookings and
cancellations show no slot open within six weeks at the centre searched for most of the failed searches, which puts the
fall on examiner capacity.

## Three rules

Drafted at the draw; completed and measured at stage 2.

## Tried and rejected

- Seed RC05's own world (a regional distributor's five reliability programmes: animal guarding, recloser firmware,
  trunk vegetation, storm hardening, live-line crews; customer minutes by cause), screened at the draw on 2026-11-03
  before any harness: a screen card in that world ran `guard.py check` (axis BLOCKs only), `heart` (WARN 0.14 against
  task303's stump, the feeder breaker and recloser tickets by vegetation, wind and wildlife) and `slots` on its setting
  nouns (task303 five terms, task132, task183, task201 on outage, feeder, recloser). It collides on world with task129
  (grid-reliability outage root cause, the same subdomain and objective, vegetation and storms among its drivers) and
  task303 (customer-minutes, storm hardening): moved to another client domain, world and dataset (CLAUDE.md, a stuck
  build is unblocked). Its kernel (planned work for want of crews leaves no fault record) is a second register the
  estimand would have to name, which task445 v2 measured as rule application.
- Health equity decomposition of a life expectancy gap by cause (Epidemiology, `health-equity-disparity-decomposition`):
  the field's method (Arriaga by age and cause) is the golden on any honest data and every structural twist found
  (registration delay, denominators, residence at death) is maturity, Layer 1 or the population the estimand files.
- E-prescribing selection slips against look-alike name mistakes read from the search the prescriber typed (Human
  Factors, `safety-incident-error-analysis`): fresh mechanism, but crediting the programmes needs the error modes
  defined, and the sentence that defines a selection slip names what the decisive step recognises (the fork is the
  stump), while leaving it undefined forks on the reporter's contributing-factor tick.
- Sun glare behind signal heads reassigning red-light crashes to signal visibility (Human Factors): the glare set has
  no threshold the physics fixes, the count moves 10 to 40 per cent across defensible windows, and the excess that
  removes the threshold is task121 v3's comparison against the same unit's hours on other days.
- Teacher vacancies covered by long-term substitutes, invisible to the teacher of record (Education,
  `multilevel-classroom-school-research`): the vacancy is read off the substitute system's assignment type, a field
  reading, and the abstraction is the holder at the time.
- Vaccine doses from fridges that froze, read from logger records (Epidemiology): the freezes are the logger file's
  largest anomaly (Shock), and the vaccine incident guidance that invalidates frozen doses is a filed rule.
- A process plant's safety system bypassed during proof tests, turning leaks into large releases (Human Factors): the
  candidate that shortens bypasses tests its own mechanism straight off the bypass log, and every release's initiator
  and the bypass are both but-for causes, a fork on the split.
- The same pension world with the core manager as the naive winner and the currency hedge as the golden (no overlay on
  the list): the decisive step then only deflates the core manager and the golden's figure is the one every route
  computes, so a solver who doubts the core manager for any reason lands the call; the overlay was put on the list so
  the golden's own figure needs the step.
- Architecture 1 itself (Quantitative Finance, `factor-return-attribution`: a manufacturer's pension plan whose
  benefit money, raised by a quarterly pro-rata sale in the core manager's account, waits there as the manager's cash,
  so the core manager looks like the largest line and the cash overlay the smallest), spent at the draw on 2026-11-03
  with a calibrated clean truth (golden overlay USD 12.05 million against the hedge at 7.95; rung 0 the core manager at
  12.12): task398's draw in the same cell had been registered earlier on a branch this guard could not see, and with it
  visible `guard.py check` returned BLOCK on ban.pairing, ban.subdomain, ban.artifact and ban.strategy, and a reviewer
  reads the two as one decision. Its measured lessons carried here: the cost of short-held cash is dominated by the
  market's path on the held days (40 market paths spread the same balance's cost from minus 5 to plus 23 million), and a
  third ask on management fees was dead on supplemental rule 3 (the fee basis is the main call's account values).
- A 911 or ambulance call-taking centre whose breaks were eaten by callbacks (Human Factors): the setting matches
  task148's 911 call-takers and callback desk and task121 v6's call-takers' rest, so a reviewer holds the same room
  twice; moved to bus duties, where the rest is a terminus stand and the operation's own record is the trip log.
- A parcel sortation hub with the same missed-break mechanism: org family logistics_or_3pl is held by task277 (BLOCK
  ban.org_family), and pick and sort accuracy is task277's own quantity.
- Architecture 2 itself (Human Factors, `workload-fatigue-shift-analysis`: Morrowbank Regional Buses, whose drivers'
  terminus stands the duty schedule promised were driven through by late trips, rebuilt from the vehicle location
  records), spent at the draw on 2026-11-03 before any data was cut: the same cell and the same decisive insight as
  shipped task121 v6 (the rest each worker really had, rebuilt from the operator's own records, while the obvious
  candidate is wrong), with nine axes equal to task121 (domain, subdomain, objective, shape 18, Gate G, strategy,
  decision type, question form what, org family); the lexical guard scored it 0.06 and passed it, a template only the
  semantic read catches. No rest, fatigue or time on task may decide this slot again.
