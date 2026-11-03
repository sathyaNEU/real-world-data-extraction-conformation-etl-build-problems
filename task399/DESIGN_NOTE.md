# task399 design note

Architecture 1, drawn 2026-11-03 (wave 7, Root-Cause lane, sathay3012), numbered from seed RC05 (a regional
electricity distributor choosing one reliability programme from five, judged on the customer minutes each
programme's cause accounted for, where the costliest cause leaves no fault record). The seed's world was screened
first against the shipped builds next to it and collides (`## Tried and rejected`), so the build moved to another
client domain, world and dataset under the same objective and number. What is kept from the seed: the decision (one
programme funded from a catalogue of five), the quantity in kind (the dollars of a shortfall each programme's cause
accounted for over the last twelve months, in millions to one decimal) and the seed's own kernel, a cost that leaves
no record of its own.

Thornell Industries, a US manufacturer, sponsors a closed defined-benefit pension plan (the Thornell Industries
Retirement Plan, about USD 8.4 billion). Its Global Equity Program (about USD 3.1 billion) is run by five external
managers against a policy benchmark half hedged to the dollar, and in the twelve months to 30 September 2026 it fell
short of that benchmark. The plan pays benefits on the first of every month and its contributions no longer cover
them, so the plan's treasury raises each coming quarter's three payments in one go: on the quarter's first business
day the core manager sells every holding pro rata at the close, and the proceeds wait in the core account until the
custodian moves each month's payroll out. The pension investment committee funds one initiative for 2027 from five.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task399.json`, architecture v1, drawn and registered 2026-11-03.
  `guard.py check` on the draft returned WARN (a first name met in an older build; `test.same_driver_older` against
  task101, task121 v2 and task464 v10 answered by differentiation lines on the card, and one against task303 written
  before the screen asked for it).
- **Pairing:** Quantitative Finance (client domain) / `factor-return-attribution` / Root-Cause Analysis. The task type
  serves Root-Cause only, and the domain has never been built on this objective (`guard.py coverage`, 2026-11-03).
- **Objective and call:** which initiative the committee funds, decided by attributing the program's shortfall against
  its policy benchmark to its sources. The call faces forward (the initiative runs in 2027) and is judged on the closed
  twelve months the committee's budget paper names; nothing is forecast, so the tag stays Root-Cause Analysis.
- **Shape:** 18, hypotheses against evidence: the five initiatives against the lines of evidence (each manager's
  shortfall against its benchmark, its factor exposures, the currency basis, the drift, the plan's own cash), each cell a
  computed figure, plus the call, the runner-up, the gap and the core manager's own shortfall. The arithmetic is written
  into `## Ask sheet` at stage 2.
- **Strategy and Gate G:** `decomposition_attribution`, Gate G `decomposition_attribution` (every figure in the pack is
  correct; the call turns on booking one account's cash to the right decision maker). Gap population (the core
  account's record is not the core manager's decisions); pattern none; generator G3 (record against operation: the
  custodian records the waiting benefit money as the core manager's holding).
- **Furniture:** forum `committee_or_panel` (the pension investment committee), forcing event `budget_or_appropriation`
  (the 2027 initiative budget), org family `manufacturer` (the plan's sponsor), role family `portfolio_manager` (the
  plan's chief investment officer), context artifact `filed_standard` (the committee's 2027 budget paper and the
  investment policy statement), calibration none. None of these is held by the last three live cards (task483, task274,
  task277) at the draw.
- **People** (`guard.py names --geo "United States" --seed 399`): Jacqueline Keller (the plan's chief investment
  officer), James Torres (the plan's treasury and benefits finance manager), Kelsey Smith (the committee's secretary).
  None appears in the prompt. The first-name WARN on James (one older build) is answered here: the full name is new.
- **Data-native sentence:** Thornell's treasury raises each quarter's benefit payments by having the core manager sell
  every holding pro rata at the close on the quarter's first business day and leaves the proceeds in the core account
  until the custodian moves each month's payroll out on its payment date, so a quarter's benefit money spends a rising
  year as cash inside one manager's account, where every attribution reads it as that manager's low market exposure.
- **The abstraction sentence**, written against every approved build's driver (`guard.py mechanisms`, the ledger's
  approved rows) and the nearest on file: "money a parent raised for its own payments waits in one unit's account and
  is read as the unit's own exposure; followed along its path from the sale to the payments, it belongs to the parent
  and makes the candidate that would keep it invested the largest". task303 strips from a feeder's tickets the supply
  losses every sibling opened in the same minute (an upstream event identified by simultaneity across siblings); task101
  finds an organisation's own top-ups in a baseline; task258 rebuilds page loads part by part; task135 reads stale noon
  prices through cross-day covariances; task120 nets a storage gain from production; none follows one unit's own cash
  from a parent's pro-rata sale to the parent's payments, so the sentence does not apply to any of them.
- **Same-puzzle and same-driver tests:** gap population, decisive generator G3 and Gate G decomposition_attribution
  repeat task101, task121 v2 and task464 v10 (older); each is another mechanism and the card differentiates.
- **Library test:** the golden is not a named correction. The field's method for the deciding quantity, plan-level
  attribution with a returns-based factor decomposition of each manager, sits at rung 1 and files the core manager's
  replacement; the step is recognising that the core account's cash is the plan's benefit money, which no field marks.
- **Sources** (every file synthetic, generated by `generator/` from seed 399, invented world, no real organisation,
  licence CC BY 4.0, recorded in `metadata.json`): written at stage 3.

## Default path

The route a competent analyst builds without thinking, from the prompt's words and the files' grain, with the field's
method for the deciding quantity in it (figures provisional until the stage 2 harness measures them on the clean truth):

1. Reconcile each manager account's daily market values and flows from the custodian, across the custodian's reporting
   platform change, and compute each account's daily time-weighted return and its benchmark's.
2. Attribute the program's daily dollar shortfall against the policy benchmark at the plan level, the field's way: each
   manager's selection (its return against its benchmark on the assets in its account), the drift of the managers'
   weights from policy, the currency basis (the program unhedged against the policy's half hedge) and the plan's own
   cash account.
3. Decompose each manager's active return on the factor returns (market, size, value, momentum) to read what drove it:
   the core manager's shortfall is mostly a low market exposure in a rising market.
4. Credit each initiative with its line: the core manager's selection, the currency basis, the plan cash account's
   drag, the drift, the emerging markets manager's selection; fund the largest.

Ends on: replacing the core manager, about USD 13 million of the shortfall (provisional).

Golden: the cash overlay, about USD 10.6 million (the benefit payments' cash waiting in the core account and in the
plan's cash account), against the currency hedge at about USD 8 million, the runner-up; the core manager's own
decisions about USD 3 million (provisional).

## Stump sentence

A competent solver attributes the program's shortfall against its policy benchmark by manager, factor, currency and
cash, finds the core manager's shortfall the largest line (about USD 13 million, most of it a low market exposure) and
funds replacing the core manager (Ends on: replacing the core manager); the step that lands it there is booking the
cash in the core account to the core manager, when it is the plan's benefit-payment money, raised by pro-rata sales on
each quarter's first business day and waiting there for the monthly payment dates, which makes the cash overlay the
largest initiative and the core manager's own shortfall one of the smallest.

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
