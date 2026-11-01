# task160 design note (architecture 2)

Corvane Remote Pharmacy's override review desk and the MSP26 medication alert package's hospital-wide go-live at
Quillfield Regional Medical Center on 4 January 2027: the net change in override reviews over the first thirteen weeks.
Architecture 1 (the cooperative's January 2027 agency nurse block) was re-rooted on 2026-11-01 at the Batch 3 queue
reset; its record is below and its world is closed.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task160.json`, architecture v2, registered 2026-11-01, architecture 1 moved to
   `lineage` with fate "re-rooted 2026-11-01 at the Batch 3 queue reset". `guard.py check` on the registered card: WARN
   only. `repeat.deliverables` (docx+xlsx against task259 v2) is answered here: a forecast workbook and a short covering
   memo are what a desk planning team sends with a change order, and the shell differs from every approved build's on
   question form and opener. NOTEs: differentiated against task169 v2 (a closed processing route that had pre-empted
   another, so the record understates; here an added upstream prompt removes inputs and the new prompt's own record
   overstates) and task304 v1 (absorption and depletion of a pool; nothing is absorbed here).
2. Window at the draw (last three live cards): task259, task452, task123, and after the final registration (22:47Z)
   task186, task452, task123. Redrawn axes: role `capacity_planner` (task123 v3) and then `operations_director` (task264
   v3 came back into the window when task452 re-registered after this card) to `product_manager`: the stakeholder is
   Corvane's override review service manager, who runs the desk as a client service line, staffs its shifts and prices
   each client's change orders; generators G11 first to G3 first (G11, eligibility
   precondition, was never this mechanism, and (population, G11, quantity_figure) repeats task141 v4; (population, G3)
   repeats task138 and task273 inside the batch, so time leads); forcing `cutover_or_migration` to `launch_or_rollout`
   (a content go-live on a fixed date is a rollout).
3. Pairing: Healthcare Delivery & Health Economics (client domain) / `utilization-access-demand-forecasting` /
   Forecasting & Predictive Modeling. The deciding analysis is a service demand forecast: the pharmacist override
   reviews a hospital's wards will send once new decision support content goes live, built the way pharmacy
   informatics builds it, from background (silent) mode alert counts and the answers the content draws where it runs.
4. Niche: a remote clinical pharmacy services firm forecasting the change in override reviews from a regional hospital's
   adult wards over the first thirteen weeks of a medication safety alert package going live everywhere, when the
   package's duplicate PRN opioid alert, answered by removing the new order about half the time on the pilot units,
   takes away severe interaction alerts that today fire against those orders.
5. Call and shape: `quantity_figure`, count, question form how-many: the net change in override reviews in the thirteen
   weeks from Monday 4 January 2027 against the same weeks without the go-live, to the nearest 100 (golden +300).
   Shape `single-figure`. Criteria: the call (1), its two components, QT reviews added and current reviews lost (2),
   desk hours for each ward going live (15), reviews signed off by month and shift (9), the memo's net figure and chart
   (2), the two files (2): 31.
6. Mechanism keys: gap time (the background log measures the package with nobody answering it; the decision is the
   live quarter), then population (today's review file is not the review stream the live package leaves). Generators
   G3 (record against operation: the background log is the package's record, the live operation removes orders), G9
   (downstream survival against upstream acquisition: a review survives only if the order it fires on and the order it
   fires against survive the new upstream alert), G13 (the base period's sixteen weeks against the plan's thirteen in
   2027). Gate G `forecasting`; strategy `causal_design` (the counterfactual alert stream with the package answering).
7. Layer 2: `estimand_identification`, pattern
   `own:a-live-duplicate-therapy-alert-removes-orders-that-later-interaction-alerts-fire-against`.
8. Furniture: role `product_manager` (above); forum `operations_desk` (Corvane's desk planning files the forecast; no
   committee approves it); forcing
   `launch_or_rollout` (CR-2291 fixes the go-live); organisation `professional_services`; calibration `pilot_log` (the
   pilot units' answers); context artifact `operations_log` (the alert history).
9. People, drawn with `guard.py names --geo usa --locale en_US --seed 160`: Chris Hernandez (Corvane, Director of
   Pharmacy Operations), Shawn Whitaker (Quillfield, Pharmacy Informatics Manager), Andrew Harvey (Quillfield, Chief
   Pharmacy Officer). Judith Harrison and Sheila Frazier, drawn first, raised `people.first` WARNs and were replaced.
10. Data-native sentence: the background log is written by rules that evaluate with nobody answering them, so every
   duplicate PRN opioid order it flags stays active in Quillfield's record and every severe interaction alert that
   later fires against it sits in the alert history as an ordinary overridden alert; on the pilot units, where the same
   rule is live, 49 per cent of such orders are removed at signing and never become an order anything fires against.
11. Sources: background (silent) mode testing is how hospitals size a CDS rule's alert volume before go-live; override
   rates for severe interaction alerts run high (here 88 per cent), while a new interruptive duplicate-therapy alert
   with a one-click removal is accepted about half the time; interaction alerts fire against the patient's active
   orders at signing (the rule register and the vendor bulletin say so in their rule definitions). Lane neighbours:
   task142 (a purchasing alliance's overflow block, a percentile construction), task169 and task304 (differentiated on
   the card), task255 (adherence persistence, another pharmacology world).
12. Abstraction sentence: none holds against the nearest builds. task169 v2 sends events a closed route used to
   pre-empt through the route that remains (the record understates); task161 v1 draws a built-up stock down at each
   holder's own rate; this build adds an upstream gate whose answers remove the inputs existing downstream events need,
   so the new gate's own record overstates the added load. The three share a forward count and nothing else a reviewer
   would call one move.
13. Pack (twelve files, four formats): the medication alert history, 1 January 2025 to 25 October 2026 (CSV, 48,434
   rows, the spine); the MSP26 background log, 6 July to 25 October 2026 (CSV, UTC); the unit census by day (CSV); the
   FY2027 inpatient volume plan (XLSX, by planning week); the medication alert rule register with its Units crosswalk
   (XLSX); Halverson's MSP26 release 2026.2 client bulletin (PDF); Schedule B revision 3 (PDF); CR-2291 (DOCX);
   Corvane's queue export for 30 June to 1 October 2026 (CSV, UTC, the asks only); Corvane's point-of-care location map
   (CSV, the asks only); distractors declared in `metadata.json`: the smart pump guardrail events (CSV) and Quillfield's
   own pharmacist interventions (XLSX).

## Survivor anatomy

- Actor: the deciding property, whether an alert overridden today will still reach the desk once the package is live,
  has no column in any file: it is a relation between a background-log row on one order and an alert-history row on
  that order or naming it as the interacting order, read through the pilot units' answers.
- Link: the background log's duplicate-opioid rows against the alert history's overridden alerts, through the order and
  the interacting order, is a comparison silent-mode burden counting never asks for; the order id is shared, and no
  sentence, field or document invites the join.
- Reflex: the field's named method for go-live burden, the background log's count times the live override share, sits
  at rung 0 and files about 500 more reviews.
- Back-test: the textbook route validates: the background log's QT alerts run 48 to 77 a week with no break across its
  sixteen weeks, its order ids all sit in the history, and the pilot units' QT override share is 58 per cent in 2025
  and 57 per cent in the last twelve months, so the silent-mode count looks complete and its override share well
  measured.
- Second use: every file the decisive step reads has its own job: the background log carries the QT additions (the
  default's own input), the alert history carries today's reviews (the base the change order prices against) and the
  pilot answers, the census and the plan carry the projection; delete the decisive step and no file drops out.
- Shock: the reviews lost are spread across every going-live unit in proportion to its opioid and sedative traffic; no
  unit, week or file shows an anomaly, and the pilot units' removals at the duplicate alert read as ordinary alert
  acceptance.
- Pins: Schedule B 4.3 files the WHAT in the agreement's own words (the reviews the units will send with the change
  live, prescribers answering its alerts as they have where it already runs, against the same weeks without it), 4.1
  the volume basis and 2.1 the unit; no filed sentence names removal, the interacting order, the link or the reach of a
  removed order, and deleting any one of them unforces a WHAT, never the step.

## Default path

1. Read CR-2291 and Schedule B 4.3: the forecast covers the thirteen weeks from 4 January 2027 on the units going live
   (the register's Background rows), against the same weeks without the go-live.
2. Conform the extracts: map the department names used before 9 November 2025 through the register's Units sheet,
   drop the boundary days each quarterly pull repeated, and move the background log from UTC to Eastern time.
3. Count the background log's MSP26_QT_COMBO alerts on the going-live units, 6 July to 25 October 2026: 1,005 on
   orders not removed at signing.
4. Apply the pilot units' QT override share (58 per cent): 578 reviews added in the base period; the duplicate PRN
   opioid alert is moderate and never reviewed, so it adds none.
5. Scale by the volume plan's admissions for the thirteen weeks over the census admissions in the base period
   (8,287 over 9,765): 491.
6. Carry today's reviews forward unchanged: the net change is the QT reviews added.

Ends on: 500 (built 490.9; the same route without the plan, by weeks, 470.0).
Golden: 300 (built 295.7: QT reviews added 490.9, current reviews lost 195.2).

## Stump sentence

The silent-mode route files about 500 more reviews (the background log's QT combination alerts on the going-live units
at the pilot units' 58 per cent override share, scaled to the plan's admissions), and the step that lands it there is
reading the background log as the package's whole effect: once live, the duplicate PRN opioid alert removes 49 per cent
of second PRN opioid orders at signing, and every overridden alert on such an order, or fired against it later in the
stay, never reaches the desk, about 200 reviews, so the net change is about 300.

## Three rules

- Task type: utilization-access-demand-forecasting (Healthcare Delivery & Health Economics): forecasting the demand a
  clinical service, pharmacist override review, will face after the hospital changes its decision support content; it
  serves Forecasting in the taxonomy.
- Domain test: the deciding quantity is the net change in pharmacist override reviews when medication alert content
  goes live, which pharmacy informatics forecasts from background mode alert counts and the override share where the
  content already runs; a noun swap leaves the active-order evaluation, the duplicate-therapy answer and the
  severity-gated review with nothing to stand on.
- Swap: "how many more tickets will the help desk get when the new software prompt goes live": a ticket queue has no
  prompt that withdraws an input other prompts evaluate against and no answer that takes a later ticket away, so the
  call stops making sense.
- Layer 1: the history's department names changed format at the November 2025 EHR upgrade (crosswalk in the register),
  its quarterly pulls repeat their boundary days, the CDS engine stamps the background log in UTC against the history's
  local time, the queue export is in UTC over a padded range with zero-padded alert references, the queue's point of
  care is a bed location, and the plan is by planning week against a census by day; each is how the source system
  writes, and none decides the call.
- Layer 2: estimand identification: the forecast quantity is the review stream with the package answered live, a
  counterfactual the background log does not record, and the choice that flips the call is identifying that stream
  rather than adding the logged new alerts to today's stream.
- Decisive step: recognising that a live interruptive duplicate-therapy alert removes orders at signing, so the
  overridden alerts on those orders and the severe interaction alerts that would fire against them later in the stay
  leave the review stream; the analysis ties each background duplicate-opioid row to today's overridden alerts on that
  order or naming it as the interacting order and prices each at the pilot units' removal share.
- Not semantics: every field read correctly (severity, user_action, the background display mode, the crosswalk, UTC)
  still files 500: no field, code or definition marks which of today's reviews the package will take away, because the
  removal and its reach are a relation across two files and a counterfactual no record holds.
- Not rule application: no filed rule removes reviews or links the logs, and Schedule B 4.3 files only the comparison;
  the enumerated family (silent-mode count 500, duplicate acknowledgements counted as reviews 1,500, own-order removal
  only 400, every duplicate removed 100, whole-encounter removal -100, the golden 300) spans six bins, the standing
  family (pilot windows and groupings, base periods, projection bases, removal combination, QT rows on removed orders,
  boundary days, the second-order term) runs 283 to 303 inside one bin, and what rules the rest out is quiet: 4.1's
  volume plan, 2.1's unit and the pilot record itself.
- Analyst test: a strong analyst reads every field and filed sentence, runs the background log as a silent-mode burden
  study (QT alerts times the pilot override share, scaled to the plan) and files about 500 more reviews, carrying
  today's reviews forward unchanged.
- Estimand: Schedule B 4.3 (Corvane_QRMC_Service_Schedule_B_rev3.pdf): the reviews the going-live units will send over
  the first thirteen weeks with the change live, prescribers answering its alerts as they have on any unit where it
  already runs, against the reviews the same units would send over the same weeks without it; the weeks from CR-2291,
  the unit from 2.1 (one overridden alert, one review), the volume basis from 4.1 (the inpatient volume plan).
- No decoy: nothing is planted to be caught: no memo, briefing, vendor estimate or stakeholder figure states a forecast;
  the background log and the pilot record are true, complete records of what they record, and the vendor bulletin
  describes background mode without claiming it measures review burden.
- Fine numbers: with every file complete and correct (the background log holds every alert the package would fire
  with nobody answering, the history every alert that fired and how it was answered, the census and plan every
  admission), the silent-mode route still files 500, because the log measures the package unanswered, a different
  quantity from the review stream 4.3 names; nothing is missing to be noticed, and the golden is an expectation over
  linked reviews at the pilot removal share, never a sum of reported rows.
- No certified replay: no certified or published figure is reproduced to recover the method; the golden comes from the
  pilot answers and the two logs, and nothing in the pack validates either route against a known forecast.
- Lesson: a background mode count measures a rule's own alerts with nobody answering them; once live, answers that
  remove orders reach every alert that would have fired on or against those orders, so a go-live burden forecast
  replays the answers instead of adding the log; no build on file teaches an upstream prompt pre-empting existing
  prompts through the inputs it withdraws.

## Readability screen

Tests: 1 a filed clause names it; 2 a column holds it or is one join from it; 3 it is the field's reflex for the
deciding quantity; 4 a helper document describes it; 5 one obvious join performs it; 6 the pack's largest anomaly
points at it; 7 a file is read by it alone.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 silent-mode count (500) | 4.3 | qt rows | yes | bulletin | no | no | no | readable |
| R0b duplicate acknowledgements as reviews (1,500) | no | severity | no | register | no | no | no | readable |
| R1 removals on the duplicate order itself only (400) | no | no | no | no | order id | no | no | readable |
| R2 removals on the order and against it, at the pilot share (300) (decisive) | no | no | no | no | no | no | no | silent |
| R3 every duplicate order removed (100) | no | no | no | no | order id | no | no | readable |
| R4 every review on an encounter with a duplicate (-100) | no | no | no | no | encounter | no | no | readable |

The decisive rung needs the counterfactual (a removed order is not active, so nothing fires against it), the two-file
relation through the interacting order, and the pilot answers; no clause, column, helper line or anomaly carries any of
the three.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a review | one overridden high-severity alert | one per order or message | same call (no order carries two QT alerts) | Schedule B 2.1, "One overridden alert is one review." |
| SF2 | the 13 weeks | 4 January to 4 April 2027, plan weeks 4 January to 29 March | calendar quarter | same call | CR-2291 names the dates; the plan's weeks align |
| SF3 | adult wards | all eighteen units; the pilot three change nothing | the fifteen going live only | same call | the register: the pilot units run the package live already |
| SF4 | without the go-live | the package stays in background mode | the package off | same call | background mode displays nothing (bulletin section 4) |
| SF5 | as they have where it already runs | the pilot units' whole record, pooled | last twelve months, 2025, the background weeks, alerts alone on their order | same call (291 to 303) | asserted in checks.py |
| SF6 | volume basis | planned over census admissions | patient days, unit by unit, weeks without the plan | same call (283 to 296) | Schedule B 4.1 names the plan; every basis lands in the bin |
| SF7 | base period | the background log's sixteen weeks | 13 weeks to 25 October, from 13 July, July to September | same call (299 to 303) | asserted |
| SF8 | combining two removal chances | product of survival chances | additive | same call | asserted |
| SF9 | QT rows on orders removed by another alert | dropped | kept | same call | asserted |
| SF10 | repeated boundary days | dropped | kept | same call | asserted |
| SF11 | pre-upgrade department names | mapped through the Units sheet | rows dropped | same call | asserted |
| SF12 | background log clock | UTC moved to Eastern | read as local | same call | asserted |
| SF13 | orders a pre-empted alert would itself have removed | not modelled | modelled (the replay's second-order term, +16) | same call | asserted against the generator's replay |
| SF14 | to the nearest 100 | 295.7 to 300 | truncation, 200 | ruled out | the prompt says nearest |

## Ladder

| Rung | Construction | Built | Files |
|---|---|---|---|
| R0 | background QT alerts times the pilot override share, plan-scaled (the default) | 490.9 | 500 |
| R0b | R0 plus the duplicate alerts kept with an acknowledgement, read as reviews | 1,485.8 | 1,500 |
| R1 | R0 less overridden alerts on the duplicate order itself, at the pilot removal share | 446.7 | 400 |
| R2 | R0 less overridden alerts on the order or fired against it (the golden) | 295.7 | 300 |
| R3 | R2 with every duplicate order removed | 97.5 | 100 |
| R4 | R0 less every review on an encounter carrying a duplicate alert, at the pilot share | -59.8 | -100 |

One rung reaches the golden's bin (checks.py, Gate F). The standing family runs 283.1 to 303.3; the components'
families run 470.0 to 499.7 (QT added, bin 450 to 550) and 186.8 to 200.3 (lost, bin 150 to 250). The generator's
replay of the forecast weeks with the package live files 352.9 against the golden's 295.7: the pilot's measured
removal share (49 per cent against the world's 46) and the second-order term (16) are noise and a refinement the bin
absorbs.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | every encounter on the going-live units over the thirteen weeks, those not yet admitted included through the plan | filed, 4.3 and 4.1 |
| 2 Unit of account | one overridden alert | filed, 2.1 |
| 3 Attribution window | alerts fired 4 January to 4 April 2027; base rows by alert time | filed, CR-2291; C1 over base periods |
| 4 As-of dating | extracts through 25 October 2026 | filed in the file names and CR-2291 |
| 5 Version basis | release 2026.2, rule logic unchanged from 2025.4 | C1, the bulletin |
| 6 Denominator | planned over census admissions | filed, 4.1; C1 over patient days and units |
| 7 Weighting | pilot answers pooled over the three units | C1 over groupings |
| 8 Window length | the pilot units' whole record | C1 over four windows |
| 9 Boundary inclusivity | 6 July 00:00 to 25 October 23:59 Eastern | C1, UTC read as local same call |
| 10 Rounding path | once, at the end, nearest 100 | filed in the prompt |
| 11 Tie-break | none arises | C1 |
| 12 Maturity and censoring | encounters straddling the base period's edges | C1 over base periods |
| 13 Order of operations | net then scale, or scale then net | C1, linear |
| 14 Row order | sums | C1 |
| 15 Duplicate resolution | repeated boundary days dropped | C1, kept same call |
| 16 Identity normalisation | pre-upgrade names through the Units sheet | the register's crosswalk; C1 |
| 17 Netting against gross | net, components beside it | filed, 4.3 "prices the difference" |
| 18 Dimensional units | reviews and admissions | C1 |
| 19 Code and status semantics | High severity reviewed when overridden | filed, 2.1, 2.2 and the register; never the stump |
| 20 Integerisation | expected counts summed, rounded once | C1 |
| 21 Clause scope | 4.3 applies to the units the change reaches | filed, CR-2291 and the register |
| 22 Forward window contents | the plan's thirteen weeks carry the volume | a shipped driver file, the plan |

## Literal reader

Executed word for word, 4.3 asks for the reviews with the change live, prescribers answering its alerts as they have on
the pilot units, less the reviews without it, over the thirteen weeks. The reader who takes the background log as "the
change live" answers only one of the package's two alerts, so the default is non-compliant on a literal reading: the
clause names the prescribers' answers, and on the pilot units half the answers to the duplicate alert remove an order.
Executing the clause in full needs those answers and what they do to the orders today's reviews fire on and against;
every licensed reading of the remaining conventions lands 283 to 303. Pass on paper and on the cut pack.

## Oracles

None. No control ties only under the golden: the background log reconciles to the history's orders under every route,
the pilot record gives both answer shares to every reader, and the plan and the census agree with any basis. Nothing in
the pack states a forecast, and no file ranks the units on the decision question.

## Ask sheet

Two asks on the July to September 2026 quarter of the desk's own work, both on files the call never reads.

**Ask A, desk hours on reviews from each ward going live, July to September 2026 (15 figures, nearest whole hour).**
Home: the change order's staffing basis per ward. Filed: Schedule B 3.2, desk time from claim to sign-off or return,
reported by the Quillfield department in which the alert fired.
- Primary device (D7, the true key elsewhere): the queue's point of care is the bed, and five pairs of ward teams
  exchanged wings for the renovation (4N and 4S from 20 July, 9E and 9W from 3 August, 10N and 10S from 17 August, 6E
  and 6W from 31 August, 11N and 11S from 14 September); Corvane's location map reads the wing, so only taking each
  session's department from the alert its reference names in the history gives the ten wards' hours.
- Hazards: the queue in UTC against Eastern quarter boundaries (no session straddles 1 July or 1 October, so a reader
  who splits sessions at the edge files the same hours, asserted); zero-padded alert references; the platform's handle
  minutes, which on a re-claimed task run from the first claim (a stress row: summing them misses all fifteen).

**Ask B, reviews signed off in each shift of each month, July to September 2026 (9 figures, whole reviews).** Home: the
shift mix the added reviews are staffed into. Filed: Schedule B 2.1 (one overridden alert, one review) and 3.1 (shift
hours, month and shift of sign-off).
- Primary device (D6, a grain below the row): a queue task is one message, an order's alerts overridden at one signing,
  and carries the first alert's reference only; 9 per cent of tasks carry two or more alerts, found only by counting
  each task's order and signing in the history.
- Hazards: UTC against Eastern shift hours (every cell moves); returned sessions, which are not sign-offs.

Pin test: the asking sentences and Schedule B pin the unit (one overridden alert), the shifts, the month of sign-off,
desk time and the department; no pin names a decant, a wing, a message or a bundle. The call's row population (the
history on the going-live units, the background log, the pilot rows, the census and the plan) carries zero device rows:
the devices live in the queue export and the location map.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| A, the ten decant wards | ward read off the point of care through Corvane's location map | miss |
| A, every ward, handle minutes (stress row) | the platform's handle minutes summed | miss |
| B, all nine month-shift cells | one review per signed-off task | miss |

Pair ceiling: 40.0 ((38 + 7 + 55 x 5/24) and (5 + 7 + 55 x 5/24), averaged)
Mirror leakage: 20.8 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack)

## Surface screen

`guard.py surface task160` on the final cut: exit 0; personas in the pack are the card's three. Three pairs promoted
for adjudication, each answered:
- task160 against task161 (adjacent numbers): gap time and the quantity_figure family are shared; the decisive pattern
  differs (G3 against G7), and so do the world (a port 3PL's overflow blocks after a front-loaded duty step), the actor
  and the driver (a stock drawn down at each holder's steady share of use, against an upstream alert removing orders
  that existing alerts fire against). No axis ban applies; the shared pair is what two forward counts share.
- task158 against task160 (two apart): the `pilot_log` calibration form is shared; task158's pilot prices calls on
  cold traffic for a GPU pool pick, this build's pilot units supply the answers to the package's two alerts. Nothing
  else is shared.
- task160 against task169: gap, pattern and decision family collide on the card; differentiated there and in the
  abstraction sentence (`## Draw` item 12): task169 re-routes events a closed route pre-empted and the record
  understates, this build adds a gate that removes downstream events and the gate's own record overstates.

## Leak sweep

`leak.py task160 --asof 2026-10-28`: REVIEW, no LEAK. Answered: sweep 3, Schedule B and CR-2291 share the call's plain
words (override reviews, adult wards, thirteen weeks) and carry no figure; sweep 4, the bulletin's background, duplicate,
interacting and orders are the rule definitions and the background log's fields, the schedule's alerts, overridden and
volume are its WHAT, and none names a removal reaching another alert; sweep 6, the location map and the register list
units and rank nothing; sweep 9, the volume plan's weeks after the as-of date are the plan itself, a forward document.

## Build record

- Generator: `params.py`, `world.py` (encounters, orders, alerts and answers, with hash-keyed answers so a live replay
  changes only what the package changes), `pack.py`, `docs.py`, `io_util.py`, `analysis.py`, `golden.py`, `writeup.py`,
  `checks.py`, `verify.py`, `ceiling.py`, `build.py`. Seed 169 (scanned over 160 to 170 for the narrowest standing
  family); queue salt 606 (scanned for every ward's hours at least 0.15 h from its rounding edge; the ward-day clock moved
  the queue's draws, so the earlier salt 352 was rescanned).
- Gates on the final cut are recorded in `pipeline.json`.

## Architecture 1 record (spent 2026-11-01)

A member-owned multi-state hospital cooperative block-booking the agency RN shifts its winter surge pool funds for the
four weeks from 4 January 2027 (healthcare-delivery-health-economics / patient-flow-beds-workforce-optimization,
Forecasting). The default averaged the closed Januaries' block draws (2,450 shifts); the golden timed the new northern
members' respiratory wave from Central by a stable four-week lag, so January held the North's whole wave and none of
the south's (600 shifts). Shipped 2026-10-18 after judge APPROVE (DETERMINISTIC), with no portal result, and re-rooted
on 2026-11-01 at the Batch 3 queue reset at the author's instruction; one architecture per world, so the surge-pool
world is closed. Its leak report is kept as `leak_check_report_arch1.md`.

## Tried and rejected
- Ask B as first built (only the teams that report after a stand-down): 8 of 16 members nil and every figure 0 or one
  team's size, so an all-nil response took half the column and cracking B1 alone kept all 16 (pair 47.3); the nurses a
  staffing office books on the open surge request for its other units (HA7) now give every member 6 to 20, and A2
  reaches Ask B at 15 of 16 (pair with B1 cracked 36.5).
- The first cut's hospital names: 14 sat within reach of a real hospital or institution (Calhoun Memorial, Little
  Traverse, Clinton Valley, Fairlane, Lakeshore Macomb, Saginaw General and others, `## Draw` item 10); renamed, every
  figure unchanged (figures.json byte-identical).
- The first cut's southern staffing: the pool's season draw spread flat over the season (617) and the south's draw per
  staffed bed carried to the North (612) both fell in the golden's cell by coincidence, without timing any wave; every
  southern member's Level 2 staffing was raised by two shifts a day (the North's untouched, the golden unchanged), and
  this winter's southern amplitude was set at 1.012 and 1.006 so the season's remainder (668) stays a bin off while the
  scaled construction (591.7) stays in the cell; one quantity, the south's December deficit, finances both, and the
  window that clears both runs from 48 to 91 shifts (66 built).
- The rival clause at 2,850: the five Januaries' mean (2,872.8 per night, 2,873 shift by shift) sits two shifts from
  the 2,875 edge, so the write-up states it as nearly 2,900, which both constructions share.
- The dictionary's `file, field, definition` sheet, identical to task460's; the persona sweep's place pairs off
  Schedule A (`## Surface screen`).
- The chart graded on five parts (21 weekly bars, the agency split, the block weeks marked, the axis, a title) with only
  the busiest week's total carrying a device: the mirror kept the free parts and both top responses on the call stood
  at 52.2; the chart is now graded on two labelled figures, the busiest week's funded total and the agency shifts
  starting that week billed to the pool, both moved by A2 and by the payroll date, and no chart part is free (both on
  the call 45.0).
- The uniform-lag world: the North followed the Southeast by 37 to 40 days in every closed winter, so the rule-3
  audit's aligned analog (the whole census moved onto this winter's Southeast centre or first surge night) and an
  eyeballed Southeast-to-North lag both filed 602 without reading any region's relation (P(both) about 0.12); West and
  Central now trails the Southeast by 4 to 32 days across the closed winters and the North follows West and Central by
  30 to 33, with the North's wastewater tied to West and Central's, so every Southeast-anchored route misses by a full
  bin or more (aligned 1,094 to 1,282, eyeballed 0 to 90, wastewater 14) and every West and Central route files 602.
- Inland Seas' payroll date left undocumented (B1 silent, backing A2 at all 16): the judge read it as an ask-side fork,
  a convention no shipped sentence filed; the dictionary now files it in the pool office's voice for both workbooks, B1
  is a convention the cracker executes, and the ask layer rests on A2 alone (pair with A2 cracked 56.0, against 35.7
  when B1 was silent).
- The block book's even halves, the register's uniform plan-revision dates, the query labels in Inland Seas' timesheet
  detail ("Billed to pool after stand-down") and typed block totals that, in the regional-lag world, sat above every
  January's draw: each read as made by hand; the splits follow the season's Schedule A slots with an agency confirming
  short in some seasons, each member's plan carries its own revision history on working days (the North's dated when
  each joined), the detail tab carries the agency's order numbers and request references, and each later block is the
  last January's draw carried, the pool manager's practice.
- The write-up's basis at 602.4 and the rival clause "not none, the pool's own draw in the same weeks after each closed
  winter's peak": the judge's own North waves averaged 604.4 and read the clause as garbled; blocks 1 to 3 state the
  basis as about 600, the precision every defensible construction shares, with one plain clause per rival and the
  Southeast-timed rival named without a figure, its constructions running from none to 1,282.
- Ask A resting on A2 alone: with A2 cracked the asks fell whole (the pair 56.0 against the bar of 40); Crestfield's
  late-cancellation lines (D3: four hours billed on one line against a booked shift no nurse worked, clause 4.2 filed
  as a rate term) now reach all 16 members in both columns, and each device cracked alone keeps the pair at 30.1 and
  31.7.
- D3's first build billed every worked night at twelve hours, so a night across the November clock change, thirteen
  hours long, billed fewer hours than it spanned, as a cancellation does; worked lines now bill the hours as worked (11
  or 13 across a change), and only a cancellation bills fewer hours than it spans (asserted).
- The one-state world (the Two Peninsulas Hospital Association, Michigan): the North a month behind West and Central
  and West and Central four days to a month behind Metro Detroit are lags no single state's season shows, where a wave
  crosses the state in days, and the rule-3 recheck read them as implausible; the pool moved to a three-region
  cooperative (Georgia and South Carolina, Tennessee, Kentucky and West Virginia, northern Michigan), Central 3.5 to
  14.5 days behind the Southeast and the North 26 to 34 behind Central, that lag moving about four days either way.
- Lockstep onsets and copied shapes: 8 of 9 Southeast members first surged on the same night this winter, tighter than
  in any closed winter, and every member's wave had nearly the same width and height (amplitudes within about four per
  cent); each member now carries its own stable offset, its own winter jitter, its own size and its own rise and fall (a
  wave rising faster than it falls), and this winter's southern onsets spread over a week like the closed winters' (at
  most five members of a region share a first night in any winter, asserted).
- The first multi-state tuning: Central's spells this winter ran past 31 December at their longest closed length and
  the North's typical wave touched both block edges; Central's spells were narrowed, its gap this winter set at two and
  a half weeks, the North's spells narrowed and its surge staffing raised so each wave stays whole at about 600.
- The draw-weighted centre left open: aligning the whole census on the season's draw-weighted centre filed 598.8 on the
  fcb08fab cut without reading any region's relation; in the multi-state world it files 242 (118 and 391 with the anchor
  three days either side), asserted a full bin off.
- The first season's even block split, back in the multi-state block book: each member's Crestfield skeleton slot now
  enters the season's Schedule A slots, so no season splits evenly.
- The first multi-state lags: across the five closed winters the North's lag behind Central fell, by chance, with the
  Southeast's timing and rose with Central's gap, so a regression of the North's centre on both southern regions'
  centres beat Central's lag out of sample (1.8 days against 3.5 left out one winter at a time) and, carried to this
  winter's early Southeast, put the North in February and filed none; the North's lags were re-drawn (26.0 to 34.25
  days, the same spread) so the record carries no such fit: that regression now misses by 15.6 days out of sample and
  files 600, and its first-night twin misses by 6.6 against Central's 3.1 and files 54 (asserted, OOS and REFLEX).
- Every activation in the declaration log numbered as a pool surge request (SR-), the North's before it joined
  included, with no line on why the northern members stayed out of the pool until 2026: the recheck read both as loose
  ends of the joining; the North's pre-pool activations carry their own capacity-reporting numbers (CAP-) and the
  dictionary says when and why they joined (asserted, REAL), every figure unchanged.
- Architecture 1 (the cooperative's January 2027 agency nurse block, 600 shifts): re-rooted 2026-11-01 at the Batch 3
  queue reset, shipped 2026-10-18 with no portal result; one architecture per world, so the surge-pool world is closed.
- Architecture 2's first pre-emptor, the renal dosing alert removing a drug a later interaction alert needed (prototype
  p1): the lever moved about 2 per cent of the reviews, under a tenth of a bin; the duplicate PRN opioid rule took its
  place, its removals reaching the opioid and sedative interaction alerts that make up much of the review stream.
- A pilot before-and-after comparison as a route (pilot units' reviews per admission before and after their go-live,
  carried to the other units): it filed 731 to 1,130 in the prototype, off the case mix of oncology and palliative care,
  and it would have been a confounded rival estimator; the pilot units now run the package live from before the
  extract begins, so no before period exists.
- Severe interaction alerts accepted at 36 per cent: orders removed by a pre-empted alert survive once live and their
  other alerts become reviews, and the replayed truth on the base weeks ran 30 per cent above the first-order estimate
  (227 against 174); acceptance set at 12 per cent (an 88 per cent override share, as such alerts run) leaves a
  second-order term of 16 reviews projected, asserted inside the bin (SF13).
- Seeds 160 to 168 and 170: standing families 35 to 116 reviews wide (seed 160's low-side combination three from the
  250 edge, seed 166's crossing the 350 edge); seed 169 at 28, then the going-live units' second QT drug and second PRN opioid
  propensities rescaled to centre the net, the QT reviews and the reviews lost in their bins.
- Guard axes redrawn at the draw: role capacity_planner (task123 v3), generator G11 first ((population, G11) repeats
  task141 v4), (population, G3) (task138 and task273 inside the batch), forcing cutover_or_migration (the honest label
  is launch_or_rollout); personas Judith Harrison and Sheila Frazier (people.first WARNs).
- A first-cut ask on the share of reviews signed off within 60 minutes of the override, its device an interface
  outage's late deliveries: the pin "of the override" points at the history's override time and spends the device, and
  the outage touched two of nine cells; replaced by Ask B's count by shift.
- Schedule B 2.1 first said a review counts "whether it reaches the desk alone or in one message with other alerts",
  and a 3.3 named the alert history as the record of where each alert fired: the first filed Ask B's device, the second
  pointed every reader at Ask A's link; both cut, the WHAT kept ("One overridden alert is one review"; desk time by the
  department in which the alert fired).
- Ask A's decant first moved three ward pairs on one date: nine of the fifteen ward figures were free to the cracker;
  five pairs now move on five dates from 20 July, leaving five free (pair 40.0).
- The vendor file first named "Release_Notes": leak.py sweep 1 reads a release-notes name as a describing file; renamed
  as the client bulletin it is.
- Unit 3E first named "3 East Neuroscience": the write-up's figure check reads "eur" as a currency next to the ward's
  hours; renamed 3 East Stroke and Spine, every figure unchanged.
- Role `operations_director`: clear at the first registration, then BLOCKed by `guard.py heart` against task264 v3 once
  task452 re-registered after this card and the window moved; redrawn to `product_manager` and re-registered. The
  prompt's second sentence first opened on "The change order rests on that net figure" (shell how-many | the |
  docx+xlsx, a `shell.repeat` WARN against task301 v2); it now opens on the use, "For the change order".
- Order signings first spread evenly over the 24 hours, so the night shift signed off as many reviews as the day shift:
  every time in an encounter now passes through one monotone ward-day clock (a morning-round peak, a quiet night),
  which moves no event's date and no ordering between events, so the call's figures are unchanged and the asks' shift
  mix reads as a hospital's; the queue salt was rescanned for the ward hours' rounding margins.
- The vendor bulletin's rule table first broke the rule ids and the severity words mid-word at the page width
  (`pdftotext -layout`); its columns were widened.
