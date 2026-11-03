# task399 design note

Architecture 4, drawn 2026-11-03 (wave 7, Root-Cause lane, sathay3012), numbered from seed RC05 (a regional
electricity distributor choosing one reliability programme from five, where the costliest cause leaves no record of
its own). The seed's world collided at the draw; architecture 1 (Quantitative Finance) was spent at the draw in
task398's cell, architecture 2 (a bus operator's drivers' rest) at the draw as a template of shipped task121 v6, and
architecture 3 (a licensing agency's road-test booking journey) at stage 2 on the pricing harness (`## Tried and
rejected`, the card's lineage). Kept from the seed: the decision (one initiative funded from a shortlist), the
quantity in kind (what each initiative's cause did to the year's outcome) and the kernel, a cost that leaves no record
of its own: a defendant called while the duty lawyer is serving the list next door leaves no record that nobody spoke
for them.

The Halsey Coast region's District Courts hear defendants arrested and held in police custody at the next sitting's
custody list. In the twelve months to 30 September 2026 the gap in remands in custody at first appearance between
defendants without their own lawyer and defendants with one widened. The Ministry of Justice's regional manager for
criminal court operations puts one initiative into the region's Budget 2027 bid, from a shortlist of five: more
electronically monitored (EM) bail assessment capacity, a District Court judge on the Kestrel Bay custody list, a
second duty lawyer on the region's custody-list roster, supported bail accommodation, and court-date text reminders.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task399.json`, architecture v4, registered 2026-11-03 with architectures
  1 to 3 in its lineage. `guard.py check` on the draft: BLOCK test.same_driver_older against task253 v2 (gap, G5 and
  binding_constraint) and WARN driver.near against task141 v1 (0.14), both cleared by differentiation lines (task253 v2
  re-solves a congestible network's loading; task141 v1 prices a release rule from the gradient across rota'd
  decision-makers); first-name WARNs on Anthony, Nathan, Gavin, Nicole, Jessica and Alexander redrawn. Re-checked on
  the registered card as the last act of stage 1: WARN overuse.org_family only (a Ministry of Justice region is the
  honest label).
- **Pairing:** Criminology & Justice (client domain) / `sentencing-bail-disparity-analysis` / Root-Cause Analysis; the
  subdomain has never been drawn, lineage included.
- **Objective and call:** where in the region's first appearances the widening sits and which shortlisted initiative
  removes it. The call is retrospective on the closed twelve months, with its reason: a root cause is named for a year
  already closed, the initiative is funded from July 2027, and nothing is forecast.
- **Shape:** 12, a drill-down to one leaf (region, courthouse, list, judicial officer, and the leaf the drill lands
  on), each branch's piece of the widening graded at each level. Arithmetic in `## Ask sheet` at stage 2.
- **Strategy and Gate G:** `binding_constraint` for both. One rostered duty lawyer is the limit that two lists sitting
  at the same time share, and that limit moves the naive pick off the bench. Gap objective (the duty lawyer's daily
  presence and volume are correct and are not what decides); generator G5 (provision elsewhere: the provision was in
  the next courtroom when the matter was called).
- **Furniture:** forum `minister_or_cabinet` (the Budget 2027 bid goes to the Minister), forcing event
  `budget_or_appropriation`, org family `government_agency`, role family `operations_director`, context artifact
  `operations_log` (the duty lawyer service's own record), question form `where`. The ban window (task274, task277,
  task398) holds none of them.
- **Neighbour:** task274 (criminology, a US county's pre-plea diversion lottery on docket events) is three builds back.
  The domain repeats; the subdomain, objective, geography, spine (an appearance extract, not docket events), decision
  and mechanism do not (differentiation on the card).
- **People** (`guard.py names --geo "New Zealand" --seed 399`): Freya Herd (regional manager, criminal court
  operations), Casey Neal (manager of the region's duty lawyer service), Toby Conway (Corrections EM bail team
  leader). None is in the prompt.
- **Data-native sentence:** the court's appearance extract records a defendant's counsel of record (blank alike for a
  defendant the duty lawyer helped and for one nobody helped) and the minute each matter was called, the duty lawyer
  service records each defendant it assisted and when, and the sitting calendar records the audio-visual remand list
  sitting in the next courtroom, so a custody-list matter called while the one rostered duty lawyer was on the
  audio-visual list exists only as a time overlap across three records.
- **Abstraction sentence:** one advocate rostered to two lists that sit at the same time leaves the cases called
  while it serves the other list unassisted; its daily presence and output are flat, so the decision-maker who sits
  the overlapping hours carries the gap on a within-decision-maker comparison. Not writable against an approved build:
  task119 (a resource recorded full but held empty for planned work), task303 (a shared upstream loss every sibling
  logs in the same minute), task124 (the kind a group was laid in, read off its surviving members) and task121 v6 (the
  rest actually taken against the schedule) each spend another relation.
- **Semantic screen** (`guard.py mechanisms --objective root-cause`, one line per build on the insight it spends):
  task13 re-attributes outcomes from an exceptions-only log; task11 a threshold rebate seen on a rebuilt ledger; task36
  a filed rule excluding the largest candidate; task50 the share of exposure inside a funded window; task72 the owner
  whose agreement covered each piece; task84 identical concurrent units competing on an unkeyed target; task111 the
  cause still operating in the forward window; task500 a matched-reference method pinned by certified statements;
  task129 a rise scaling with each unit's surroundings; task121 the conditions each event was made under (v6 the rest
  before a shift); task202 the share of each input reaching the layer the response draws on; task398 an exposure rule
  driven by the whole's own path; task399 v3 a capacity stock rebuilt from releases and bookings. **Is the new
  decisive step any of them in other nouns?** No: it reads one advocate's presence at each case's call across two
  simultaneous lists behind a within-decision-maker disparity; no build on file reads a disparity against the absence
  of the person who speaks for the case.
- **Slots, run twice before any harness:** setting nouns (bail, remand, duty counsel, duty lawyer, magistrate,
  detention): task202 only, whose note set aside a binding hold read from the jail extract (the holds sit in a
  column) and a charging-cell sentencing disparity (readable); neither is this insight. Mechanism nouns
  (double-booked, simultaneous, overlap, same session, two places, adjourned): none.
- **Library test:** the golden is not a named correction; the field's own method for the deciding quantity
  (disparity within court and judicial officer, net of the legally relevant pre-decision factors, the rigor card's
  pattern 4) sits at rung 1 and files a judge on the custody list.

## Default path

1. Take every first appearance from police custody in the two twelve-month periods (October 2024 to September 2025,
   October 2025 to September 2026) from the court's appearance extract, flag a remand in custody, and split by counsel
   of record (own lawyer against none).
2. The gap in the remand-in-custody share between defendants with no lawyer of record and defendants with one widens
   between the periods.
3. Estimate the disparity the field's way: within court and judicial officer, with the legally relevant pre-decision
   factors (charge seriousness, criminal history, bail history, on bail at arrest) as controls, the counsel-by-period
   interaction carrying the widening.
4. Drill: courthouse, then list, then judicial officer. The widening sits in the Kestrel Bay custody list, under the
   community magistrate who took it over in March 2026.
5. Check the dated changes: EM bail assessments slowed from February 2026 (EM bail is sought at a later appearance,
   never decided at the first); the duty lawyer roster is unchanged (one duty lawyer at every Kestrel Bay sitting,
   clients a sitting flat); reminders and accommodation show nothing at first appearance.
6. Fund a District Court judge on the Kestrel Bay custody list.

Ends on: a District Court judge on the Kestrel Bay custody list (provisional figures at stage 2).

Golden: a second duty lawyer on the custody-list roster, the widening read against whether the duty lawyer was in the
custody courtroom when each matter was called (provisional).

## Stump sentence

A competent solver measures the first-appearance custody-remand gap within court and judicial officer with the
legally relevant factors as controls, finds the widening in the Kestrel Bay custody list under the community
magistrate who took it over in March 2026, and funds a judge on the custody list (Ends on: a District Court judge on
the Kestrel Bay custody list); the step that lands it there is reading a within-officer difference as the officer's,
when the duty lawyer service's record and the sitting calendar show the single rostered duty lawyer was serving the
new audio-visual remand list next door when most of the widening's matters were called, which puts the gap on the duty
lawyer roster.

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
- Architecture 3 itself (Product Analytics, `funnel-journey-analysis`: Norland Driver Services' road-test booking
  journey, the search-to-booking fall read against the slot stock rebuilt from releases, bookings and cancellations),
  spent at stage 2 on 2026-11-03 before any data was cut. The pricing sequence's step 3 run as a daily queue harness
  over two years (scratch `a3/harness.py`) under three variants built to hide the binding (the busy centres losing 14
  per cent of slots; the province's releases held flat by rural top-ups; a quarter of slots released four days ahead):
  in every variant two one-group-by routes name the golden at rung 1, releases by centre down about 8 per cent at the
  busy centres and bookings over releases by centre at the ceiling there, while the decisive rebuild put 95 per cent
  of failed searches on an empty stock. The throughput identity (tests sat at a fully booked centre equal its releases)
  makes a binding capacity one subtraction (readability tests 3 and 6; Gate F's two cheap routes), so no honest booking
  world hides it.
- Duty counsel absent on some sitting days, read off the duty counsel log by day (Criminology, the same bail world as
  architecture 4): the initiative "restore full duty counsel coverage" invites the count of sitting days with no
  duty counsel entry, one group-by on the log, and the step is architecture 3's family (a resource's availability at
  the event against its aggregate).
- Video bail hearings recovered from the remand centre's court-escort movements: the initiative names the mode, so
  the solver looks for it and the escort movement type is one join from the hearing; and the dated switch to video is
  itself the before-and-after a solver runs first.
- A legal aid contract concentrating bail work in fewer lawyers, read as their double-booking across courtrooms: the
  per-lawyer caseload by year is one group-by and names the concentration.
- The binding matter across a person's open cases (released on the new charge, held on an old one): task202's note
  measured the holds as a column of every custody extract, and the rule that books a custody day to one matter would
  have to be filed (rule application).
- Failures to appear per scheduled appearance against the lead time each date was set at: a pooled rate over a mix
  that shifted, `composition_mix`, banned in the window by task277, and lead time is one lag a solver enumerates.
- Remand bed-days split into admissions and length of stay (exit-cohort stays shrink while stays lengthen):
  `maturity_censoring`, banned in the window by task274, and Little's law makes the split one division.
- Island ferry cancellations behind a visitor economy's turnover (Economics, panel data): the cancellations are the
  pack's largest anomaly (Shock) and the relief-ferry initiative invites its own check.
- An energy price shock absorbed by a panel's time effects, read through each town's energy-intensive employment
  (Economics, panel data): exposure times the shock is the energy rebate's natural check, and the hedged-contract
  second correction is a column one join away.
- A scoring model's inputs as scored against as stored after a late feed was backfilled (General Statistics,
  interpretability): the cause is a pipeline defect, so the step is Layer 1 carrying the call.
- Vaccine hesitancy measured after the missed dose in a parents' survey (Psychology, mediation): temporal precedence of
  the mediator is the rigor card's own pattern 3, a reflex.
