# task401 design note

Architecture 5, drawn 2026-11-04. The number was handed out against seed RC07 (a supplier's January imbalance bill).
The seed's world could not carry an honest unbanned draw; architecture 1 (a frailty virtual ward against care home
closures, Epidemiology and Public Health) and architecture 2 (a canola hybrid against July heat, Economics and
Econometrics) died at stage 2, architecture 3 (a GB energy supplier's satisfaction fall, Marketing and Consumer
Research) was spent at stage 4, round 2, on an ask's unfiled re-attribution, and architecture 4 (a river's winter
ammonia failures below a water recycling centre, Physical and Environmental Sciences) was spent at stage 4, round 1,
when the judge's blind derivation reached the call and every ask figure (`## Tried and rejected`, the card's
`lineage`). One architecture per world: architecture 5 moves to Psychology and Behavioural Science, an English leisure
trust's membership base, a new dataset and a new shell.

The world: Wrenford Leisure Trust, an invented charity that runs Wrenford Borough Council's nine leisure centres under
an operating contract, with about 25,000 members paying monthly by Direct Debit. Members who joined before the January
2023 tariff migration sit on legacy tariffs (about a quarter of the base, and about three in ten of them had stopped
coming by January 2026 while still paying); everyone since is on the 2023 tariffs, and a 2023-tariff member's Rewards
account (points for visits, spent on guest passes, cafe credit and class bookings) opens after their third monthly
payment. To close a budget gap the trust made five changes in January and February 2026: a daytime class timetable
consolidated at the centres older members use most (12 January), the Rewards scheme closed (1 February), every legacy
member written to with the current terms at an unchanged price (letters posted from 2 February), shorter evening and
weekend hours at two centres (from 9 February), and a member care team calling members with no visit in three weeks
(from 16 February). Cancellations jumped in February. The council's contract review in April asks the trust which change
its 2026-27 plan reverses, and the head of membership has the trust's extract of 16 March 2026 to answer from. The
membership year runs from the first Monday in February, so the review's year is 2 February 2026 to 31 January 2027.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v5, registered after `guard.py check` at WARN.
  `overuse.objective`: the slot's objective is fixed by its number. `repeat.gate_g` and `overuse.gate_g`
  (`decomposition_attribution` repeats task402 and task403): the call assigns the year's cancellations among five
  changes made inside six weeks, and the stump is that the count to date assigns them the wrong way round, so the
  mechanism is honestly an attribution; `forecasting` would name the projection, which is the decisive step, not the
  call. `test.same_driver_older` against task122's lineage is answered by the card's differentiation line (nothing here
  is re-attributed), and so is task274, the nearest family member on file (below).
- **Pairing:** Psychology and Behavioural Science (client domain), task type `mediation-moderation-process-modeling`,
  which serves Root-Cause Analysis in the taxonomy; objective Root-Cause Analysis; shape 18 (the five filed changes are
  the hypotheses, each with its own in-place date and reach).
- **Strategy:** `maturity_censoring`, gap time first (the twelve months from 2 February 2026 are six weeks observed at
  the extract, and one change's cancellations sit almost wholly in the unobserved part), objective second (the count to
  date answers a different question from the year's count). Pattern none; generators G13 horizon mismatch (decisive),
  G3 record versus operation (the register lists as active a member who has stopped coming), G12 absence of record
  versus record of absence (no cancellation yet is not no cancellation caused). Layer 2 family `estimation_fit`. The
  window's three live cards hold `causal_design`, `time_semantics` and `composition_mix`.
- **Data-native sentence:** a member who stops coming keeps paying by Direct Debit for about three months before
  cancelling, so the members the Rewards closure lost in February sit in the visits record as members with no recent
  visit while the register still lists them as active, and reach the cancellations only from April; the legacy terms
  letters prompted members who had stopped coming long before to cancel within days, so their cancellations sit inside
  the extract's six weeks, and some of them would have cancelled later in the year anyway.
- **Abstraction sentence:** two changes made in the same week reach their outcome on opposite clocks, one at once and
  partly brought forward from later in the year, the other only after its units have sat idle for months, so the count
  to date ranks them the wrong way round and the idle stock, set against the same date a year earlier and converted at
  the earlier year's rate, puts them right. It is not writable against the nearest builds: task274 (shipped 11-02)
  completes units inside a recorded programme stage through that stage's hazard to size one randomised offer, with no
  rival and no unmarked pending state; task133 converts a dormant residue whose young units only look dormant (a stock
  forecast, no attribution); task402's architectures pair a unit's consecutive events or lose cases when an actor's
  assignment lapses; this slot's architecture 3 standardised a mix behind a satisfaction fall.
- **Same-puzzle and library tests:** gap, pattern and decision type repeat no build in the last twelve; gap, pattern
  and Gate G repeat only task122's lineage, differentiated. The golden is no named correction: the field's methods for
  the deciding quantity, a before-and-after or difference-in-differences on each change's cancellations and a mediation
  model read on the outcomes observed so far, sit at rungs 0 and 1 and both name the letters; no textbook names "count
  the members who stopped coming and still pay, against the same date a year earlier, and convert them at last year's
  rate".
- **Layers:** Layer 1 is the trust's own record-keeping: access-control entries in local time across the March 2025
  clock change with gate re-entries minutes apart and a turnstile outage week at one centre; a membership register whose
  tariff codes were renamed at the January 2023 migration; cancellation requests from three channels (online form,
  front desk, telephone) with request, notice and effective dates and duplicate requests; letters posted in batches over
  a week with returned mail; a care-call log keyed by membership number as text with its leading zeros dropped; a 2025
  and a 2026 extract of the register with different column names. Layer 2 is the cancellations still to come from
  members who have stopped coming, timed by the lag from last visit to cancellation.
- **People** (`guard.py names --geo "United Kingdom, England" --seed 401 --n 60`, taking the first three names in draw
  order whose first name and surname sit on no other card, lineage included, and fire no guard people rule, and that no
  earlier architecture of this slot used; Marilyn Patel, drawn first, was replaced on the coordinator's people.last
  finding against task155): Sophie Newman (the trust's head of membership, who owns the answer to the council), Shaun
  Steele (membership systems manager, who keeps the register and the extracts), Clifford Pope (the council's leisure
  contract manager). The prompt names no one.
- **Furniture drawn against the live window** (read off `guard.py check`): forum `customer_or_counterparty` (the
  council is the trust's contracting client; `committee_or_panel`, `trustees_or_governors` and `executive_team` are held
  by task400, task402 and task403), forcing event `period_close` (the 2025-26 year end sets the 2026-27 plan;
  `vote_or_meeting` and `season_or_peak` are held), organisation family `nonprofit_or_charity`, role family
  `operations_director` (`product_manager` is held by task403), context artifact `filed_standard` (the contract's
  performance schedule).
- **Sources:** synthetic throughout, built to the structure of the records it imitates; every file's source, date and
  licence goes into `metadata.json` at stage 3. Invented names checked: no place or organisation named Wrenford was
  found (the nearest is Wrenbury, a Cheshire village).

### Documented levels

- **The lag from last visit to cancellation.** DellaVigna and Malmendier (2006, "Paying Not to Go to the Gym",
  American Economic Review 96(3)) put the average at 2.31 months over every canceller. The world splits cancellers into
  members who quit while still coming (within days of a visit) and members who drift away, whose lag runs about three
  months on the 2023 tariffs (gamma, shape 6, mean 13 weeks), longer for older members (mean 22 weeks) and for legacy
  members (gamma, shape 2, mean 45 weeks). The spread of the drift lag is a modelling choice the source does not publish,
  and the design was moved until it held at this width (Tried and rejected, 2026-11-04).
- **Inattention and the reminder.** Einav, Klopack and Mahoney (2025, "Selling Subscriptions", American Economic Review
  115(5)) find subscription cancellations rise from 2 to at least 8 per cent in the month a card replacement forces the
  subscriber's attention. The terms letters are that shock for legacy members who have stopped coming: about two thirds of
  those idle four weeks or more cancel within three weeks, about five times legacy's ordinary monthly cancellations; most
  of them would have cancelled within the membership year anyway, on the legacy curve.
- **Attrition and reactivation.** About 3.8 to 4.0 per cent of members cancel a month on the 2025 run, a modelling level
  (no single published UK figure is cited); a member who has stopped coming returns at a weekly rate that fades with the
  time away (a 12-week scale), faster for older members.
- **The closure's effect.** Loyalty programme termination lowering patronage is documented (Melnyk and Bijmolt 2015,
  European Journal of Marketing 49(3/4)); the size is a modelling choice: about one Rewards holder in sixteen stops
  coming, most within a fortnight, and the holders' visits fall 7 to 9 per cent against the same weeks of 2025.
- **The other changes.** The timetable cuts older daytime class users' visits to 0.85 of the rate and stops 15 per cent
  of them coming for a while (their 28-day active share falls 8 to 12 per cent, more than the holders'); the hours cut
  sends a fifth of the two centres' visits to other centres (their visits per member fall 24 to 29 per cent) and lifts
  quitting there by 8 per cent; the care calls bring idle members back faster.

### The four go/no-go screens

Measured on the clean truth over 20 redraws (seeds 1 to 20) of the accepted world, `scratchpad/t401/a5/screens7.py` on
`proto7.py` (extract 16 March 2026; the reminder harvest in place). Truth over the membership year: the Rewards closure
672 to 797 cancellations, the letters 279 to 371, the timetable 133 to 224, the hours cut 20 to 120, the care calls -380
to -317; the closure first in 20 of 20.

1. **The lever against the rivals' estimates:** the golden (for every change, its excess cancellations so far plus its
   excess of members with no visit in the 28 days to the extract over the same date of 2025, times the share of last
   year's such members in its reach who cancelled by the end of the 2025-26 membership year) names the closure in 20 of 20
   and leads its own runner-up (the letters, netted) by 1.70x at the lowest; the letters' raw count so far (1,021 to
   1,177) is the default path's figure and exceeds the closure's golden by construction, which is the stump. The hours
   cut's year-on-year count from 9 February scaled to a year double-counts the letters' tail among the two centres'
   legacy members; against the members it did not reach it is near zero.
2. **The golden's own method holds the call:** at the filed year end it names the closure under both conversion sources
   (the reach's own last-year members or every member) and both baselines (year on year or against the members not
   reached) in 20 of 20, and so it does at 9, 10 and 12 months and at idle thresholds of 21 to 42 days; it flips at a
   six-month horizon (13 of 20) and at 56 days (20 of 20), both outside the filed membership year and the filed 28-day
   definition.
3. **No easy completion, and the first look lands wrong:** the cancellations first look (each change's reach, after
   against before, 2 to 6 weeks, lags 0 to 8) names the letters in 20 of 20, and so does the same reader net of 2025;
   the count reader (each change's excess cancellations plus the 28-day active members its reach lost, year on year)
   names the letters in 20 of 20, by 1.08x to 1.43x; the 28-day active share names the timetable in 19 of 20, visits per
   member the timetable in 20 of 20, the centre reader the two centres of the hours cut in 20 of 20, stated reasons the
   letters in 20 of 20; every flexible cracker rung lands off the closure in 20 of 20. The residual: the 28-day active
   count read alone, with no cancellations beside it, shows the closure's dent first (`## Readability screen`).
4. **Literal execution:** the filed WHAT (the cancellations among the members a change applies to over the membership
   year, against the same weeks of the year before) executed on the cancellations to the extract, by year-on-year count
   and against the members not reached, names the letters in 20 of 20; the golden needs the cancellations still to come
   and the cancellations the letters only brought forward, which no filed sentence asks for.

Shipping seed 18 (prototype): the closure 716 against the letters 312 in truth; the golden 687 against 317 (2.17x); the
count reader on the letters, 1,062 against 761 (1.40x); the active share on the timetable (-9.2 against -7.7 per cent).

## Default path

1. Read the savings programme paper for the five changes, their dates and the members each applies to; build each
   change's members from the register (Rewards account by 31 January, legacy tariff on 2 February), the class bookings
   (weekday classes before 5pm, 13 October 2025 to 11 January 2026) and the home centre; count each membership once at
   its first request (Schedule 4, 4.1).
2. The field's method for an intervention's effect on an outcome: each change's cancellations among its members from its
   date to the extract against the same weeks of 2025 at that year's rate, and against the members it did not reach
   (difference-in-differences). The letters: 1,062 (1,101 against the rest); the closure: -101 (-1,546); the timetable
   64; the hours cut 210 (6 against the rest). February's spike sits among legacy members; their stated reasons agree
   (Price or terms up 367 on the same weeks).
3. Because the year is not over, scale the ongoing changes to the year and keep the letters as a one-off, or read a
   mediation model (change, then visits, then cancellations) on the outcomes observed so far: the closure's visits fell
   about 9 per cent, but its indirect effect on cancellations so far is nil, so it scales to nothing.

Ends on: the legacy terms letters.

Golden: the Rewards closure.

## Stump sentence

A competent analyst counts each change's cancellations since its date against the same weeks of 2025 among the members
it applies to, finds the legacy terms letters behind February's spike (1,062 more legacy cancellations) and nothing yet
from the Rewards closure, and names the legacy terms letters, because they never count the Rewards holders who have
stopped coming and still pay (1,027 more than a year ago, of whom last year's position cancelled 76.8 per cent within the
year) or net the letters' cancellations against the long-idle legacy members who would have left within the year anyway.

## Three rules

- Task type: mediation-moderation-process-modeling (Psychology and Behavioural Science), which serves Root-Cause Analysis:
  the change works on cancellations through members' attendance, and the process's timing is the deciding structure.
- Domain test: the deciding quantity is each change's membership-year cancellations through the indirect path the field
  models, change to lapsed attendance to cancellation, timed by inattention: members who stop coming keep paying for
  months (DellaVigna and Malmendier 2006) and an attention shock makes the inattentive cancel at once (Einav, Klopack and
  Mahoney 2025); the field's estimate of it is the path's yield, here read off last year's members in the same position.
- Swap: "which change will cost the hospital the most patients over the year" reads, but nobody keeps paying a hospital
  they have stopped attending, so there is no stock of lapsed payers to carry forward and no reminder to pull their exits
  forward; the deciding quantity disappears with the subscription.
- Layer 1: the membership system's register with tariff codes renamed at the 2023 migration and statuses as at the
  extract; cancellation requests from three channels with members asking twice; the access system's weekly export with a
  turnstile outage week at Brookvale (November 2024); letters posted in five batches with returned post; a care-call log
  keyed by membership number with its leading zeros dropped; class bookings with no-shows and cancellations; for the asks,
  two Direct Debit bureaux with different dating, units and references, household mandates, two reception till systems
  with different line grains, and a pool closures log. Nothing is placed to be caught.
- Layer 2: family estimation_fit: the year's cancellations each change causes, estimated from the stock of members who
  have stopped coming and last year's yield of that stock, for both the change whose exits are still to come and the
  change whose exits were brought forward.
- Decisive step: carrying each change's members who are not visiting, against the same date a year earlier, through last
  year's cancellation rate for members in that position to the end of the membership year, which adds the closure's
  lapsed payers and takes the letters' pull-forward back out.
- Not semantics: every term is filed and read the same way by every route (a cancellation, the members a change applies
  to, the membership year, the same weeks of the previous year, the 28-day active member); a reader who reads every
  field, code and date correctly and counts cancellations still names the letters, because the closure's cancellations
  have not happened yet.
- Not rule application: no filed rule or procedure projects anything: Schedule 4 files the estimand and its comparison,
  never a method, and executing it on the records to the extract names the letters. The enumerated family (counts so far,
  year-on-year or against the rest, as counted or scaled to the year, a mediation read on outcomes so far, and the
  projection at 21 to 56 days, 6 to 12 months, either conversion source, either baseline, at the extract or at 1
  February) spreads the closure's figure from -13,437 to 2,361; the standing family (the projection at 21 to 42 days to
  9 months or more, both sources, both baselines, at the extract) spreads it 505 to 2,361 and names the closure in 64 of
  64; what rules out the counts is the data's own structure (1,027 more lapsed payers and last year's 76.8 per cent), not
  a sentence.
- Analyst test: a strong analyst who reads every file correctly compares each change's cancellations since its date
  with the same weeks of 2025 among its members, finds the letters behind the spike and nothing yet from the closure, and
  names the legacy terms letters.
- Estimand: Schedule 4, 4.3 (operating_contract_schedule_4.pdf): for each change, the cancellations made in the current
  membership year (2 February 2026 to 31 January 2027, the prompt and the terms) by the members the change applies to
  (the savings programme paper) that would not have been made without it, set against the members in the same position
  in the previous membership year over the same weeks; members not yet lapsed and cancellations not yet made are in it.
- No decoy: nothing is planted: no memo, briefing, dashboard or stakeholder figure argues for the letters; the spike is
  the letters' real effect and the stated reasons are members' own; the savings paper lists savings, never cancellations.
- No certified replay: no certified or published figure is reproduced to recover a method; last year's conversion is
  read from last year's own records.
- Lesson: an outcome counted to date is not the year's outcome when one cause works through a stock of lapsed payers and
  another only brings exits forward: the right comparison is the stock against the same date last year, carried through
  last year's yield; no build on file nets a pull-forward against a censored stock in one ranking.

## Survivor anatomy

- Actor: the deciding property, a member who has stopped coming and is still paying, has no column: the register says
  Active and the usage export simply has no rows for them in the last four weeks; it is a relation between two files
  and a date.
- Link: the comparison of this year's not-visiting stock with the same date a year earlier, and last year's stock with
  its own later cancellations, is a cross-period link no key offers and the field's method (a before-and-after on the
  outcome, a mediation read on outcomes so far) never asks for.
- Reflex: the field's methods sit at rungs 0 to 2 and all file the letters: the difference-in-differences on
  cancellations (1,062 against -101), its scaling to the year, and a mediation read on the outcomes so far.
- Back-test: the textbook route validates: the letters' spike reconciles with their mailing log and with members' own
  stated reasons (Price or terms up 367 on the same weeks), and the closure's members cancel no more than last year.
- Second use: every file the decisive step reads is in the pack for its own reason: the weekly usage export is the
  access system's report and the source of the contract's monthly return, the register and requests are the membership
  system's, and the bookings and letters log are the reach records of two other changes.
- Shock: what the step recovers is ordinary movement: Rewards holders not visiting rise by about 8 per cent of the holders,
  less than the timetable group's fall and far below February's cancellation spike, the pack's largest anomaly.
- Pins: the WHAT is filed in the contract's Schedule 4 and the trust's own terms and savings paper; no filed sentence
  names the not-visiting stock, the lag, a conversion or a projection, Schedule 4 defines the active member only as a
  monthly-return measure, and the prompt says nothing of activity.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 each change's cancellations since its date against the same weeks of 2025, and against the rest | Schedule 4 files the estimand and its comparison | requests, register and reach files | yes, the field's before-and-after | the stated reasons agree | no | yes | no | readable |
| R1 the ongoing changes scaled to the year, the letters a one-off | none | the same | yes | none | no | yes | no | readable |
| R2 a mediation model read on the outcomes so far | none | weekly usage and requests | yes, the subdomain's own model | none | no | no | no | readable |
| R3 the not-visiting stock against the same date a year earlier, carried through last year's yield for both changes (decisive) | no: nothing names a stock, a lag or a yield; 28 days is a monthly-return measure | no: the register says Active, the usage export has no flag | no: the reflexes are R0 to R2 | none ranks the changes | no | no: two moves applied to two changes | no: the usage export is the access system's own report | silent |

The residual, recorded at the coordinator's ruling: a reader who tabulates the 28-day active count alone in each change's
members, year on year, with no cancellations beside it, sees the closure's dent first (seed 18: -863 against -226 for
the timetable group, -203 for the two centres, +42 for legacy members). With cancellations beside it, the count reader
names the letters (1,062 against 762, 1.39x), and the share, visits, centre and stated-reasons readers all land off the
closure (`checks.py` asserts each on the shipped seed). Nothing in the pack steers a reader to the count alone: the prompt
names no activity, Schedule 4 headlines no active count as a change's cost, and no document tabulates activity by change.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives and the call under each | Ruled out by |
|---|---|---|---|---|
| SF1 | a cancellation | a membership's first request, once | every request (1,495 repeats): the closure | Schedule 4, 4.1; same call, asserted |
| SF2 | the closure's members | Rewards holders on 31 January 2026 | every 2023-tariff member: the closure (697) | the savings paper; same call, asserted |
| SF3 | the letters' members | legacy tariff on 2 February 2026 | the mailing log, returned post included | the savings paper; the same 6,809, asserted |
| SF4 | the timetable's members | any weekday booking before 5pm, 13 October to 11 January | attended bookings only | the savings paper says booked; same call, asserted |
| SF5 | the hours cut's members | home centre Northgate or Westcroft | members visiting those centres | the savings paper; same call, asserted |
| SF6 | the year | 2 February 2026 to 31 January 2027 | six months: the letters in 1 of 4 settings | the prompt and the terms (the membership year), asserted |
| SF7 | the same weeks of the previous year | 364 days back, 3 February 2025 start | 365 days | the terms (first Monday in February); asserted |
| SF8 | members in the same position then | last year's reach at the same date | this year's members a year earlier: the closure (593) | Schedule 4, 4.3; same call, asserted |
| SF9 | a member already leaving | out of a reach after their first request | in the denominator | a member cancels once (4.1); same call |
| SF10 | not visiting | no visit in the 28 days before | 21, 35 or 42 days: the closure; 56 days: not the closure | Schedule 4 (the 28-day measure); asserted |
| SF11 | last year's yield | the reach's own members | every member: the closure | same call, asserted |
| SF12 | the baseline | year on year | against the members not reached: the closure | same call, asserted |
| SF13 | the as-of date | the extract, 16 March 2026 | none | the prompt; every record ends there, asserted |

## Ladder

- R0 (the field's before-and-after on cancellations): the letters 1,062, the hours cut 210, the timetable 64, the
  closure -101: the closure 4th of 4.
- R1 (ongoing changes scaled to the year, the letters a one-off): the hours cut 1,825 (its count double-counts the letters'
  tail at the two centres), the letters 1,062, the timetable 552, the closure -880; against the rest, the letters 1,101.
- R2 (mediation on outcomes so far): the closure's visits fall 8.8 per cent but no cancellations follow yet: the letters.
- R3 (decisive, the golden): the closure 690, the letters 320, the timetable 190, the hours cut -90: the closure by 2.16x.
- Worth: the decisive step moves the closure from -101 to 690 and the letters from 1,062 to 320; every correction below
  it walks the same way (the letters first) and only R3 reverses. The standing family names the closure in 64 of 64
  settings, 505 to 2,361; over 20 redraws the golden names the closure 20 of 20, 1.70x over its runner-up at the lowest.
- Pricing: the residue the WHAT leaves is a method (the yield of a stock), not a knob; the lever (1,027 more lapsed payers
  at 76.8 per cent) puts the closure 2.16x over the netted letters at the shipped seed and 1.70x at the lowest over 20
  redraws; the letters' pull-forward (1,091 fewer not visiting at 68.3 per cent) is the second, independent quantity.

## Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | each change's members as the savings paper defines them, on the books at its date | filed (savings paper), SF2 to SF5 |
| 2 Unit of account | a membership and its first request | Schedule 4, 4.1 |
| 3 Attribution window | the current membership year | the prompt and the terms, SF6 |
| 4 As-of dating | the extract, 16 March 2026 | the prompt; every record ends there |
| 5 Version basis | one register extract, statuses as at the extract | single version |
| 6 Denominator | each change's members not already leaving at the date | SF9, same call |
| 7 Weighting | none; counts of members | n/a |
| 8 Window length | the same weeks of the previous year | the terms, SF7 |
| 9 Boundary inclusivity | a request on a change's date counts from that date | same call, the dates carry no ties |
| 10 Rounding path | costs to the nearest 10 as working; the call is the graded unit | the call is not rounded |
| 11 Tie-break | none; the lead is 2.16x | n/a |
| 12 Maturity and censoring | cancellations not yet made are in the estimand | Schedule 4, 4.3 and the prompt (the year) |
| 13 Order of operations | count, then stock, then yield | one order, the parts add |
| 14 Row order | none | n/a |
| 15 Duplicate resolution | a membership's repeat request | SF1 |
| 16 Identity normalisation | membership numbers keep six digits; the call log drops zeros | the call log is read zero-padded; it moves no reach the golden uses |
| 17 Netting against gross | the letters' pull-forward nets within the year | the estimand (would not have been made without it) |
| 18 Dimensional units | members | n/a |
| 19 Code and status semantics | legacy tariffs begin L- | the terms, section 5 |
| 20 Integerisation | none graded | n/a |
| 21 Clause scope | Schedule 4.3 applies to each change alike | one clause |
| 22 Forward window contents | members not yet lapsed and cancellations not yet made | the estimand includes them; last year's yield stands for them |

## Literal reader

Schedule 4, 4.3 executed word for word for each change on the records to the extract (the cancellations made by its
members that would not otherwise have been made, against the members in the same position over the same weeks of the
previous year) names the legacy terms letters by year-on-year count (1,062 against -101) and against the members not
reached (1,101 against -1,546); the year is not over, so a literal reader must still say what the rest of the year holds,
and the only record of that is last year's members in the same position: carried through their yield, the closure leads
(690 against 320). The asks' asking sentences file their counting units (each person admitted once; each fee in the
month it pays for); every reading of them converges on the golden or is ruled out by a shipped record (the price list,
the closures log, the bureau letter).

## Oracles

No shipped artifact ranks the changes, states a stock, a lag or a yield, or names the closure. The savings paper lists
savings; the stated reasons and the letters log confirm the letters' spike on the wrong path and say nothing of the
year; Schedule 4's monthly-return measures are definitions. On the asks, the price list's pay-as-you-go sheet and
charges sheet, the EPOS notice and the closures log are records every reader needs, and no control ties only under the
golden.

leak.py on the cut pack: REVIEW, no LEAK. Ruled harmless, one line each: `operating_contract_schedule_4.pdf` carries the review's words (cancellation, member, active) because it defines the monthly return and the review's estimand, and names no stock, lag, yield or projection; `savings_programme_2025-26.docx` carries the changes' own words (letters, points, account) because it lists the changes and who they apply to, with savings and no cancellations. The metadata line that used the author's word for the call was reworded at the first run.

## Ask sheet

- **Ask 1, pay-as-you-go admissions at Northgate and Westcroft together and at the other centres together, each month
  October 2025 to February 2026** (10 figures, nearest 10). H18: the hours cut's other public at the two centres and
  the trust's casual use beside it, a measure the review weighs that the call does not turn on. Files: the old till's
  sales report, the EPOS lines, the EPOS notice, the price list, the pool closures log.
  - Primary P1 (D6, a ticket's party on one line, the old-till block: October at the two centres, October and November
    elsewhere): a family ticket is one line whose price is its party (price list). Lines read as people undercount.
  - Primary P2 (D4 and D9, the EPOS block: November to February at the two centres, December to February elsewhere): a
    pool closure's swimmers were refunded to their cards in negative lines; they had been admitted, the closures log
    shows the closure, and netting every refund (the natural handling) undercounts. Hazards: a Swim and Gym ticket is two
    half-price EPOS lines (one person), voids in both systems, site codes.
- **Ask 2, membership fees for each month November 2025 to February 2026 on the legacy and the 2023 tariffs, each fee in
  the month it pays for** (8 figures, nearest GBP 100). H18: the income behind the membership base the changes act on.
  Files: both bureaux' reports, the mandates, the returns, the bureau letter, the register's household column, the price
  list.
  - Primary P1 (D2 and D8, the November and December block): a November collection bureau A refused twice is taken with
    the member's December collection by bureau B, which has no return of its own to pair it with; read by its own
    reference the fee lands in December.
  - Primary P2 (D6, the January and February block): a household's memberships are one bureau B collection, split by
    each membership's fee; and a returned collection is carried into the next with the administration charge. Hazards:
    bureau A's processing dates and pence, re-presentations, a day-28 collection taken on 2 March paying for February.
- The main population's zero-counts: the call reads the register, requests, usage, bookings, letters and call log; no
  ask device sits in them (the asks read only their own files), asserted by construction.
- Cracker sheet, on the cut pack (pack digest in `ceiling.py`'s output):

| Ask | Cracker | Full includer | No repair | Mirror | Cracker verdict |
|---|---|---|---|---|---|
| 1 admissions | 0 of 10 | 3 of 10 | 0 of 10 | 0 of 10 | miss |
| 2 fees | 0 of 8 | 4 of 8 | 0 of 8 | 0 of 8 | miss |

- Pair ceiling: 49.9 (two full includers, one on the call at 66.4 and one off it at 33.4; the cracker on the call and the mirror off it make 28.5).
- Mirror leakage: 0.0 per cent of ask weight.
- Measured by: generator/ceiling.py on the cut pack.

## Tried and rejected

- 2026-11-03, the seed's world (RC07, a supplier's January imbalance bill against plant trips and low wind), every
  candidate screened before the card. The trips' effect on the supplier's own imbalance volume at the system price is
  settlement accounting: each unit's metered shortfall against its notified output in the window before the desk can
  re-trade, priced per settlement period, reconciles exactly to the bill, so nothing is left to decide (rule
  application). The price the supplier would have faced without its own units' trips re-runs the system's price
  formation on the changed path, task398's spent insight in other nouns. Netting the desk's replacement trades out of a
  trip's cost is the same insight again (the cause owns the response it triggered). Which settlement periods a trip owns
  (gate closure, the share of an interval) is a market rule or a time-semantics read, banned as decisive. The cost
  spike's drivers identified from interval data need a driver the settlement data does not meter, and in this market
  every driver is metered. Dual imbalance pricing makes the portfolio's net position matter, but executing the price
  rule on the with-and-without positions is rule application. The honest strategy, `decomposition_attribution`, and the
  seed's forum (the board) are both held by task398 in the window. Moved, per `CLAUDE.md`.
- 2026-11-03, other moves screened and set aside before this draw: gas turbine inlet icing in freezing fog read against
  temperature (the winter measures on the table name the mechanism, so a reader checks each one's conditions and lands
  it; two cheap routes); a groundwater nitrate rise read against travel time through the unsaturated zone (task202's
  reach-the-receptor insight in other nouns, and the field's first move); a bathing water's sources separated by marker
  decay in transit (task202's reach and task248's transit loss); selective in-migration behind a widening mortality gap
  (task68's entrants and task134 v2's newcomers, and the prior-diagnosis read lands the decision without it); depletion
  of the frail by a winter's deaths before an intervention's evaluation (dead on lever at realistic excess mortality, as
  task173's screens found for mortality displacement, and its frailty proxy forks the expectation); the Will Rogers
  stage migration (the field's stage-specific comparison collapses into which stage field to read, data semantics);
  attenuation by a mediator's or a predictor's unreliability (task262's insight); regression dilution of a risk factor
  in a disparity decomposition (task262 again); a funnel's downstream rate falling when an upstream filter loosened (the
  end-to-end funnel is the field's reflex); a two-stage complaint escalation's selection (the per-complaint view lands it);
  a mode or non-response shift in a satisfaction tracker (task121 v4's linkage and halo).
- 2026-11-03, prototypes before the card (`scratchpad/t401/proto1.py` to `proto3.py`, expected values with Poisson draws):
  winter-only counts in a city of 600,000 left the default and the golden overlapping across draws (default 5th to 95th
  percentile 23 to 179, golden -38 to 119), so the build runs at integrated-care-system scale over October-to-September
  years with the closures in the year between the baseline and the pilot; there the default's expectation is 912 (spread
  208) against a golden of 392 (spread 215, truth 389), and the trend-adjusted golden forms agree within a median of 6.4
  admissions once the framework files the comparison; without the comparison filed, the no-trend form differs from them
  by a median of 77 (a fork the framework's comparison sentence closes, a WHAT naming no method).
- 2026-11-03, architecture 1 dies at stage 2 on the coordinator's realism check, before any data was cut. Set to published
  English levels (a care home resident aged 80 and over about 0.70 to 0.75 emergency admissions a year, community
  residents by band 0.24 to 0.58, a same-age ratio near two, not the prototype's five), the composition lever is about
  113 admissions for the 440 Core20 residents the closures moved (sd 26), against draw-to-draw spreads of 202 in the
  default and 214 in the golden on a one-year baseline and about 160 on three years (`scratchpad/t401/proto4.py`, 400
  draws). A bar at the midpoint separates default above from golden below in 22 per cent of draws (27 on three years);
  900 residents moved gives 41 to 51 per cent and 1,400 gives 58 to 72, and 1,400 is two fifths of Core20's care home
  places in one system closing in a year, which no honest care group failure produces. A larger 80 and over population
  scales the spread with the lever, and a bar nearer the truth only moves the coin flip. The stump was the noise. Re-rooted.
- 2026-11-03, the redraw's other candidates, set aside before the card: regression to the mean of units chosen on a
  noisy outcome (task130 v3 landed it; task149 and task174 rejected it on that lineage); a satisfaction fall read against
  the conditions each respondent met, or a tracker's mode or response shift (task121 v4); a storable good's purchases
  pulled forward before an announced price rise and paid back after (the pre-rise spike is the pack's largest movement
  and announces the step); a distributor's orders falling as channel stock is drawn down (sell-through is the field's
  reflex and lands it); a local policy confounded by a common shock loading on each unit's exposure (the council
  furniture is banned in the window and the exposure needs data no operator holds); transformer insulation ageing under
  new loads (electricity is spent, task129, task196, task201, task303, and F6's 46 already holds a rate stationary in a
  constructed exposure); in the crop world itself, a hybrid placed on clubroot or hail-struck fields (a lab result or an
  adjuster's claim names the field, readable), and a hybrid whose own later flowering met the heat (`crop2.py`: a three-day
  shift moves the season-long panel only 3 to 5 per cent, and the forward step then needs a climatology fork).
- 2026-11-03, prototypes for architecture 2 (`scratchpad/t401/crop1.py`, `crop3.py`, ten weather draws each, the
  hybrid's own effect nil and equal phenology): with most of the hybrid's seed late by 8 to 14 days, the season-long
  panel files minus 9.1 per cent (sd 9.8 across weather draws), farm-by-year effects minus 9.3, a linear seeding-date term
  minus 7.0, raw 2026 means minus 11.6, the flowering-window exposure minus 0.1 (sd 0.9), its variants (thresholds 28 and
  31 C, windows 14 and 22 days, 490 and 550 heat units to flower) minus 3.5 to plus 0.5, and fields seeded on the same
  days on the same farm minus 0.6 (the same insight by matching). The spread across draws is the weather's: the pack's
  July heat wave and seed delay are set by design, never picked from draws.
- 2026-11-03, architecture 2 dies at stage 2 on its own ladder (`generator/ladder.py`, seed 4012026, measured at commit
  7d3a3cd), before any data was cut. First, the golden's own method forks the main call: the flowering-window variants
  land +2.1 (28 C), -2.5 (31 C), -12.0 (a 14-day window), +3.4 (a 22-day window), -8.2 (490 heat units to flower) and
  +4.9 (550 units) against the 5 per cent bar, so two agronomically defensible variants drop the hybrid and four keep
  it; filing the window or the heat metric would name the decisive step, and the generator cannot close the spread under
  realistic catch-up (a 17-day seeding gap became a 6-day flowering gap). Second, the stump rests on a functional-form
  choice: the default path's own rung 4 already rebuilds seeding dates from the seeder's logs, and every flexible form of
  that variable then lands the golden (seeding-week bins +3.6, a cubic +4.4, same-day matching +9.3); only a linear term
  stays wrong (-10.1 in the season panel, -8.3 with farm-by-year effects), so Gate F would rest on the solver choosing a
  straight line. Spent; one architecture per world, so the crop and weather world is closed to this slot. Re-rooted at
  architecture 3 in another client domain, world and dataset.
- 2026-11-03, architecture 3's draw, candidates set aside before the card. In the never-built satisfaction cell, the
  client card's moves (Shapley shares, a Net Promoter change's multinomial error, penalty against reward, loyalty read
  on later behaviour) are reflexes, and reading a fall on the conditions each response was made under is task121 v4's.
  A broadband provider's speed promise against delivered speed died on the regulator's own reflex (the share of plan
  speed delivered is the standard metric). The energy quote mechanism in the supplier's base-wide relationship tracker
  carried 0.54 points (1.35 with 2025's joiners using a fifth more) against a fall whose draw-to-draw spread is 0.66
  (`scratchpad/t401/a3/proto_e2.py`), architecture 1's death in other nouns, so the build runs on the six-month
  new-customer tracker. In the concentrated form a first harness with the platform's own effect at 1.3 points left the
  golden's 10 and 20 per cent flags (0.98, 1.78) under the residual (`proto_e3.py`); at the platform's realistic small
  effect the standing forms clear it (`proto_e4.py`). Other cells screened: education multilevel (the client's three
  cards are reflexes; teacher reassignment and special-needs assessment waits fail screen 1 or repeat the actor family),
  health equity (an inhaler switch run practice by practice is task400's staggered rollout; discharge after a missed
  appointment repeats task402's broken-off cases), pollution source attribution (every wind, tide and capture-zone route
  is task202's reach), water network reliability (the isolation extent per burst is one group-by; transients read
  through topology sit beside task303), the human factors cells (the pairing is barred against task400), and
  interpretability (ruled a backdrop at task129 v1).
- 2026-11-03, stage 2 on architecture 3, three cuts. (a) The first world set the first Direct Debit from the quote, so
  the review rise was a near-copy of the gap and a solver asking why payments rose walked to the quote; the payment is
  now set from the meter point's industry quantity at registration, and the Direct Debit change books 0.35 points and
  names the platform (`## Ladder`, R2b). (b) A Direct Debit policy document stating that rule was drafted and dropped:
  its sentence on industry quantities would send a reader to set quotes against quantities, and the golden never needs
  it. (c) The contact centre ask and its two call logs were cut for budget; the contact rival stays on the tracker's own
  contact question. The asks' first devices as drafted (stale legacy status, re-runs keyed on the legacy reference,
  withdrawals) were each executable from the cutover plan's and the asking sentences' own pins, so they were re-sited
  onto an erroneous-transfer return, a reload chain with a pilot twin, and a gas registration raised under its own
  reference.
- 2026-11-03, stage 2 on architecture 3, the full includer (precut FAIL: one primary per ask). The coordinator's candidates
  were screened against the full includer: (a) Ask B, an account whose gas was removed between its first load and its
  reload: the full includer that walks the chain takes the last load's row, fuels with its week, and keeps the block, and
  the sentence that closes the fork (the fuels that load carried) makes it a work order; (b) Ask C, broker switches
  registered on the broker's lead reference: noticing the unmatched reference and joining on the prospect is one act, and
  every quote under a broker's lead is a broker quote, so nothing goes wrong after the notice; re-sited onto a broker sale
  re-quoted by the phone team after the registration; (c) Ask A, two-rate registers alone: a work order once the plan
  files day and night together; the device is the register set changing at an exchange, and gas has no register. Also set
  aside: split-fuel legacy accounts merged on load (one platform number on two rows, and the filed unit, the account the
  platform holds, makes it a work order); a requested supply start on legacy sales (the industry registration date in the
  quantities fixes it in one act); fuel add-ons across the migration renumbering (the solver who landed the call already
  built the crosswalk).
- 2026-11-03, stage 2, the full includer at 36 of 58 (62 per cent of the ask weight, 79.1 on the call): one second device
  per ask on its own block left a full includer and an on-call cracker pairing near 62. Widened: Ask A gained a change of
  occupier on the same meter points (the primary's own repair keeps the leaving account), Ask B's returned accounts take
  both fuels, Ask C's re-quotes reach every channel; the full includer keeps none of the 58.
- 2026-11-03, stage 4 round 1 (judge NOT_DETERMINISTIC and SOLUTION_WRONG, SEND_BACK light on the workbook asks alone, main
  call forced, Gates G and H passing; reader clean on the main call): Ask B's second device, the 410 accounts loaded and
  returned to the legacy platform, died to its own WHAT. Filing what counts as moved (the new platform billing the account
  at the end of 2 November 2025) closed the judge's fork 1 and made the returns a work order: with the sentence filed and
  nothing else changed, the full includer keeps 16 of 18 Ask B figures (`scratchpad/t401/fix/remeasure_b.py`). The returns
  stay as a hazard; the second device is re-sited onto 389 accounts the legacy platform took back during 2026 on a change
  to prepayment, where the repair the sentence invites is right before the close and wrong after it (the full includer
  keeps 0 of 18).
- 2026-11-03, stage 4 round 1, the Gate A anomaly: the change-of-occupier branch drew the leaving account's supply start
  without reference to its closure, so two Closed accounts began after they closed and took their meter points from the
  live occupiers (Eastern and London one account short under the golden's own rule). The leaving account's start now
  precedes its closure, asserted over every account. Fork 3 was closed by "no withdrawn registration counted" rather than
  by dating the boundary in the asking sentence (shorter, and true whatever the date), with every withdrawal now dated
  before the start it requested, as switching allows.
- 2026-11-03, stage 4 round 2, architecture 3 spent. The round-2 judge returned NOT_DETERMINISTIC, SEND_BACK (narrow), on
  the switches table: "credited to the sale it was registered on", read word for word, takes each registration's
  quote_ref, and 596 Phone registrations name a quote dated 2 to 10 days after the registration; the golden moves each to
  the prospect's latest quote on or before it, a rule no file states, and for 94 of those prospects latest against
  earliest moves about 20 cells. The literal ask executor in checks.py had carried the re-attribution as though it were
  the field's own value, so it never saw the fork. Every round-1 finding closed, and the main call held in both rounds
  (forced and reproduced; Gate F good; Gate G analytical_non_defect; Gate H analytical), but the judge noted that
  Critical Component 2's "more than half" depends on the cut (a binary covered split puts 14 per cent of the fall on the
  quote mix, five bands 60, eight bands 85, the kinked model 75). A second round without APPROVE spends the architecture
  under the round-1 ruling; the slot re-roots at architecture 4 in another domain, world, dataset and shell. Lessons: a
  literal executor takes every field at its face value, so a golden that overrides a field's own link (a reference, a
  date, a status) carries a filed WHAT or the data are regenerated so the face value is the golden; and every quantity
  the write-up states for the main call holds at every natural granularity of the comparison, or is stated so it does.
- 2026-11-03, architecture 4's draw, candidates set aside before the card (four go/no-go screens, `scratchpad/t401/a4/`).
  The strategy window (binding_constraint, causal_design and decomposition_attribution held by task399, task400 and
  task402) bars the natural attribution labels, so each candidate's decisive move was labelled before it was priced.
  (a) An online retailer's checkout conversion fall booked to a checkout release, caused by a collection partner
  withdrawing urban points while adding as many in suburbs (`proto1.py`, `proto2.py`, 20 redraws): it fails screens 2
  and 3, since the access effect acts only on latent collection-preferring shoppers through a continuous distance, so its
  share runs 0.84 to 2.50 points across defensible exposure forms and the release's residual -0.62 to 2.67, and it fails
  the swap test (collection points read the same as clinics); it also sits beside task129's surroundings exposure and
  task399 v3's supply behind a journey, and task177 had called a nearest-locker reading a replay. (b) Opportunity to
  learn in a primary trust's mid-year maths tests, a new scheme's sequence placing tested topics after the test date:
  an intrinsic fork, because the scheme's sequencing is itself a counterfactual cause of the measured spring fall, so
  the default's "the scheme" and the golden's "the sequence against the test date" name one candidate. (c) A school
  trust's illness absence driven by classroom ventilation cut to save energy: at published levels (about 0.5 to 0.9
  points of absence per 1,000 ppm) the lever is a fifth to a half of the rise. (d) Deploy-spanning journeys breaking
  in-flight checkouts: task129 v1 spent the first-use-after-a-version-change shape. (e) Split shipments across
  fulfilment centres: task175's seed and task277's reflex. (f) Tampered HGVs read from roadside remote sensing: task202
  screened it. (g) Storm overflows against the load apportionment model: the overflow record is the zeitgeist's first
  check, and the move is attribution. (h) A charity upgrade appeal's anchored figure, a norm boomerang and a goal
  difficulty gap: the levels are not documented, or the gap is architecture 3's family. (i) Composition designs in
  every cell: this slot has spent two (architecture 1's closures, architecture 3's mix standardisation).
- 2026-11-03, architecture 4, stage 2: the caustic clean-in-place excursion drawn at the card (pH above 11 for twenty
  to forty minutes) breaches the consent's "pH of any sample ... not more than 11" in the dairy's own record, so a
  careful reader catches a breach by reading a condition (rule 3, a field reading deciding). Redrawn to acid whey run
  to the drain on evenings after a missed collection: an oxygen-demand shock at pH 6.1 to 6.4, inside the consent.
- 2026-11-03, stage 2: whey evenings on Thursday to Sunday only put every exceedance day on Friday to Tuesday, a weekly
  hole one tabulation finds. Spread to every evening but Wednesday's (the composite's night); no weekday now holds
  above three tenths of the days.
- 2026-11-03, stage 2: the morning-after oxygen sag alone in the historian (0.05 to 0.35 mg/l with the blowers flat
  out) marked the shock days at the works in one query. Given twins of the same shape (the control's night-load sags
  after go-live, storm flushes before), so under half of the days in any of four sag queries are exceedance days.
- 2026-11-03, stage 2: the dairy's pH drawn as a clipped normal piled readings at the clip (6.60) and its gamma
  replacement reached 11.9, a visible breach. Replaced by a smooth distribution held under 10.3.
- 2026-11-03, stage 2, asks: homes connected per quarter (flats behind one lateral) is a device whose discovery is its
  remedy (the addressing register lists the homes), and no second device of another family stood on it without a filed
  sentence naming it, so the full includer kept 12 of 12. Dropped with the inspection record and the addressing
  register. The first trade effluent set handed the cracker both devices (a meter register listing each exchange with
  its final and initial reads beside the multiplier it opens the file for; the scheme's "dated by its collection"), and
  suspended solids moved under one bin for three dischargers. The multiplier moved to the consent's metering columns,
  the exchange reads into the reads file, the dating left to the WHAT ("collected in the charging year"), solids
  ungraded. The first energy set named TB1 on MCC 7 in the meters sheet, handing the new blower to the cracker; the
  board is now listed without its load and the shutdown works record names it.
- 2026-11-03, stage 2, the coordinator's ruling on the first rebuilt ask layer: the blowers' transformer change shared
  its file and its question with the new blower's board (a reader opening the shutdown record for MCC 7 reads both rows),
  was marked on the reads sheet (a site read and an "as at" note), was fixed by one swapped multiplier, and sat in D2
  with the trade effluent exchange; the full includer kept 18 of 18. The report date against the collection date was
  caught too (the scheme's emptying sentence pointed at the round sheets, the laboratory column is honestly named and the
  label is the join): 15 of 15. The blowers' electricity was dropped: every fact its golden needed had to be stated, and
  once stated its fix was a swap. The ask now carries one primary per family, P1 the exchanges (D2) and P2 the
  two-bottle composites weighted by the samplers' logged volumes (D6); charges came out because they sit in both blocks.
- 2026-11-03, stage 2: two-bottle composites at one week in ten moved three strengths under one bin (the laundry's and
  the bottler's suspended solids under a plain mean, three under the second bottle dropped). Raised to about a third of
  weeks with the night bottle at 45 to 65 per cent of the day's strength; every wrong reading now moves every strength by
  3 bins or more.
- 2026-11-04, architecture 4 spent at stage 4, round 1: the judge's blind derivation reached the call and every ask
  figure. Every free gate had passed, precut was clean, the leak reader found no decisive-step sentence, and the judge
  returned DETERMINISTIC with a wording FIX_NOW and Gate F "moderate to good"; but its derivation, written before it
  opened the graded blocks, landed the call and all 15 ask figures in 26 tool calls. The works' hourly final-effluent
  ammonia jumped to 10 to 17 mg/l from midnight on every failure day (against 0.7 to 1.0), the spikes aligned one to one
  with the discharger's evening pH dips in its own fifteen-minute monitor file (a file the pack carried for that
  discharger alone; 38 of 38 such evenings were followed by a failure day), and the prompt's chart sentence ("tracing the
  winter's exceedance days from the river down through the works to whatever sets them off") announced the trace. The ask
  fell the same way: the scheme's filed WHAT ("the strength of a composite sample is the strength of the effluent it
  holds") beside the sampler log's volume column made volume-weighting the bottles the obvious move. The deeper cause: a
  graded count that holds under every operationalisation needed a clean, short, visible alignment, which is exactly what
  one look finds, so the stump sat in finding the signal and determinism and difficulty pulled against each other.
  Lessons carried to architecture 5: the first-look reader (the outcome at its finest grain beside every candidate's own
  record, aligned by date and lag, plus a before-and-after on each dated change) is coded and must land the wrong call;
  every candidate's evidence sits in records all candidates share at one grain; the prompt names the WHAT, never the
  route; a filed WHAT never names the property its ask's remedy needs while the column that supplies it ships.
- 2026-11-04, architecture 5's draw, cells and candidates set aside before the card (screens in `scratchpad/t401/a5/`).
  Cells: workload-fatigue-shift-analysis is barred by `ban.pairing` against task400 (human factors on root-cause);
  funnel-journey-analysis registered to task403 at 01:15Z the same day (shape 09, `executive_team`, `product_manager`, a
  price change booked for a subscription conversion fall), so it, those axes and any price-change rival are kept clear
  of; interpretability (directly or through the nonprofit and audit house domains) reads as a backdrop on every world
  tried. Mechanisms screened on paper, each with its reason: an age-matched comparison against units' life-cycle curves
  (the pre-trend check and unit trends are reflexes); a remedy targeted at members already lapsing (confounding by
  indication is a reflex once the targeting is read); a change's harm reaching the comparison units through shared
  demand (task500 v2's spillover through a link); a timetable change breaking members' habitual slots (architecture 2's
  dated shock meeting each unit's own phase); a detector's precision falling with prevalence (the swap test fails);
  separating two same-day changes by a dose rebuilt from records (task129 v1 and task129's surroundings); an
  instructor's departure breaking classes (task402 v1's lapsed actor); a consumable's stock running out unit by unit
  (task50's rotation); members leaving at a contract's end (a column); a reward's withdrawal read on the dose alone (the
  dose test lands it whenever its cancellations fall inside the window).
- 2026-11-04, architecture 5's prototypes (`proto1.py` to `proto4.py`, `screens.py`, 20 redraws each): a permanent visit
  loss after the Rewards closure kept producing lapses after the cut, which no snapshot can count (the golden reached a
  third of the truth); with the closure in January its lapsed members were harvested by the February letter, so its
  in-window effect was 550 of 870 and the two causes tangled; with disjoint reaches and a 1 March cut the golden's figure
  moved with the inactivity rule (an eight-week rule cannot see five-week-old lapses), closed by the contract's 28-day
  active-member definition; a Direct Debit notification to every member put part of the letter's spike inside the
  closure's own reach, so the mixed extrapolation landed on the closure in 15 of 20; the legacy terms letter (legacy
  members only, price unchanged) restored every screen. The price rise first used for the letter was dropped for task403's
  price-change rival in the same wave.
- 2026-11-04, architecture 5's screens re-run before the card (`screens2.py`, 20 redraws per setting): the prototype's
  drift lag (mean ten weeks, the published 2.31-month average, at gamma shape 14, a spread of a quarter of the mean)
  held the mixed-extrapolation cracker (the closure's count so far scaled to the year, the letters kept as a one-off) in
  19 of 20 only by its tightness: at shape 10 that cracker named the closure in 10 of 20 and at shape 6 in 19 of 20,
  and the published average is taken over every canceller, members who quit while still coming included, so the drift
  path's own lag runs longer and wider than the prototype had it. At the 23 March extract a three-month drift lag at
  shape 6 still let the cracker in 3 of 20 (7 of 20 at 13.7 weeks and shape 5). Moved the extract to 16 March with the
  three-month drift lag at shape 6, which holds every screen (`## Draw`); at the 16 March extract the 23 March
  setting's tight ten-week lag left the golden's own variants on the call in only 18 of 20.
- 2026-11-04, architecture 5's personas: the drafted card's three people were not in the seed-401 draw; redrawn from
  `guard.py names --seed 401 --n 30` in draw order, skipping the names that fire a people rule (Harry, Patricia, Hayley,
  Raymond and five more first names on older builds) and every name this slot's architectures 3 and 4 used.
- 2026-11-04, architecture 5, stage 2, the engagement first look coded in full at the coordinator's request
  (`screens6.py` on `proto6.py`, 20 redraws): with Rewards holding made observable (an account after the third
  payment), the timetable change cutting older daytime class users' visits to 0.85 and stopping 12 per cent of them for a
  while, and the hours cut moving a fifth of the two centres' visits elsewhere, the 28-day active share, visits per member,
  centre, stated-reasons and cancellation first looks all landed off the closure in 20 of 20, but the year-on-year count
  of 28-day active members in each change's reach named the closure in 20 of 20 (-1,000 to -1,100 against -250 to -355),
  beside a letters spike of about 230. The coordinator ruled that a firing readability screen (active members are the
  contract's own measure; once it shows -1,050 against about 300 letter cancellations, "people who stopped coming will
  cancel" is one sentence away). Per-change figures and the gap were also found ungradable: with 28 days and the year
  pinned, conversion source and baseline moved the closure's figure by up to 393 and the gap by up to 467, so the main call
  grades the decision unit only.
- 2026-11-04, architecture 5, stage 2, the reminder harvest (`screens7.py` on `proto7.py`, 20 redraws), the bounded fix
  the coordinator allowed in this world: reactivation fades with time idle, legacy members visit at 0.65 of the rate, so
  about three in ten of them are idle at the closure, and the terms letters act as an attention shock on them (Einav,
  Klopack and Mahoney 2025: cancellations rise from 2 to at least 8 per cent a month when a card replacement forces
  attention), cancelling about two thirds within three weeks. Two settings were tried on four seeds first: the stronger
  shock with the smaller stock let the active-share reader onto the closure on one seed of four, so the larger stock with
  a 30 per cent weekly shock was taken. Over 20 redraws the letters' visible harm (excess cancellations to the extract,
  1,021 to 1,177) beats the closure's lost regulars (761 to 974) in 20 of 20 while their true membership-year cost is 279
  to 371 against the closure's 672 to 797; every first look and literal execution lands off the closure in 19 or 20 of
  20; the call holds under both conversion sources and both baselines at the year end, 9, 10 and 12 months and at 21 to
  42 days, and flips only at a six-month horizon (13 of 20) and at 56 days (20 of 20), both outside the filed membership
  year and the filed 28-day definition. Kept; shipping seed 18.
