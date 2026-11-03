# task402 design note

Architecture 2, drawn 2026-11-03 (wave 7, Root-Cause lane), numbered from seed RC08 (a wind turbine's five faults and
its one spring crew visit). Architecture 1 (an NHS Talking Therapies service) died at stage 4 on the determinism
judge's SEND_BACK (`## Tried and rejected`, its line and the card's lineage). Architecture 2 moves domain, world,
dataset and shell. Kept from the seed: the decision kind (one of five changes gets the single fix) and the quantity's
kind (what that change cost over the period, in the period's natural unit). The kernel is new.

A regional bowel cancer screening hub (hosted by an NHS foundation trust, invented region) posts a faecal
immunochemical test kit to everyone aged 50 to 74 every two years; a completed screen is a kit that comes back with a
usable result. The trust board commits its 2026-27 bowel screening equity fund in July 2026 to the fix for the one
change on the programme's review that cost the most deprived fifth of the region the most completed screens in
2025-26. The review lists five changes: A, the community screening champions in the most deprived localities ended
(31 March 2025); B, the age extension, 50 and 51 year olds invited for the first time (from 1 April 2025); C, the kit
helpline closed and queries moved to a web form (1 April 2025); D, the integrated care board's shared registration
service took over general practices' registration administration (1 April 2024); E, the reminder letter moved from
four to eight weeks after the kit (from 6 October 2025).

What nothing in the pack says: since April 2024 the shared service has applied address changes weeks to months after
a patient asks for them, the hub posts each kit to the registered address on the despatch date, and a kit posted while
a change is pending goes to the address the person has left and almost never comes back. The loss runs at the same
rate in 2024-25 and 2025-26.

## Draw

- Card: `.claude/skills/fingerprint/cards/task402.json`, architecture v2, registered 2026-11-03T18:12:57Z; `guard.py
  check` on the registered card exits 0 (WARN only), `validate` clean. Architecture 1's identity sits in the card's
  `lineage` with its fate and its shell in `lineage_shells`.
- Pairing: Epidemiology and Public Health, task type health-equity-disparity-decomposition, objective Root-Cause
  Analysis. The equity fund is decided on the most deprived fifth's shortfall split by cause, the task type's own
  question. Probed with `guard.py check` on probe cards in both directions before the draw: this cell, the never-built
  education multilevel cell and grid reliability are all legal for Root-Cause; no task-type BLOCK on any.
- Shape 07, grid of cells: the five changes by the five deprivation fifths, each cell the completed screens that change
  cost that fifth in 2025-26; the call is one column's largest row. Sum: 25 cells, call, runner-up, gap, flip (4), the
  grid's chart with its parts (6), two files: 37 before the asks.
- Strategy population_selection: the shortfall sits on a cohort built from two histories (each kit's despatch date and
  the shared service's own request and completion dates for each address change), never a status word or column.
  Decisive generator G8 (reachability against magnitude), G13 (horizon mismatch) behind it.
- Decision, quantity and tense: pick one of five; the quantity is screens lost in a closed year (2025-26), the decision
  forward (the 2026-27 fund). Retrospective quantity by design: the fund's terms cost the year just closed, and the
  forward reading only widens the winner's lead (the pending cohort does not shrink while the service runs as it does).
- Data-native sentence: the hub posts to whatever address the register holds on the day it despatches, and the
  register's address is the one the shared service has applied, so the people the programme loses are the ones whose
  change was asked for and not yet applied, a cohort that exists only as the overlap of a despatch date with an
  open request in another organisation's queue.
- Abstraction sentence, tried against the nearest builds and not writable: against task121 (a coincident change takes
  the blame while a state rebuilt from consecutive records shows where the harm sits) a reviewer could say "a hidden
  state shows which change the harm follows", and it does not hold here: nothing coincides, no state comes from
  consecutive records, and the decisive point is that the winner's loss is a level present through both compared
  years, so the comparison the terms invite gives it nothing. Against task51's lineage (two baselines rank drivers
  differently, the step a choice of base) the step here is not a choice of base: the terms file the year's cost as a
  level and one baseline; the step is identifying an in-force change's level through the cohort. Against task399 (an
  actor's absence at each event read off a second roster) nothing is absent at an event: the kit was posted, to the
  wrong door, and the person's own record says so only through a request's two dates.
- One line per nearest spent insight, screened semantically: task121, rest rebuilt from consecutive shifts (no clock
  here); task129, outages scaling with each unit's surroundings (no place property decides here); task202, a source's
  input reaching the layer the response draws on (no transport); task398, a path-dependent counterfactual (none);
  task399, an advocate's absence at each call (no presence at an event); task399 a3, unmet demand behind an empty
  capacity stock (no capacity); task400, a staggered rollout's comparison (nothing staggered; the winner has no
  contrast at all); task401 a1, composition by closures (B's composition is rung 0, not the step); task401 a2, a
  dated shock meeting each unit's sensitive phase (no phase); task401 a3, expectation against delivery (none);
  task402 a1, cases broken off when a fixed-term actor's assignment lapses (no actor); task187, a unit's shortfall
  against a reference curve (no curve).
- `slots` before any harness: mechanism nouns (registration, backlog, pending, address, despatch, kit) and setting
  nouns (bowel, screening, FIT, kit, hub, deprivation, fifth, completion) return no slot at three terms or more; the
  driver run returns only generic-word hits (task194, task135, task464, task474, task130, task170), none the insight.
  The architecture 1 words were run too and return this slot first.
- Guard WARNs answered: `overuse.objective` and `overuse.gate_g` (the lane is Root-Cause and decomposition_attribution is the honest Gate G
  key for a fall assigned to a change; the strategy differs from all three window builds); `repeat.gate_g` against
  task400 and task401 (same answer). `test.same_puzzle_older` against task258 and `test.same_driver_older` against
  task303 are differentiated on the card.
- Shell drawn with the world: question form "where" (whether-class in voice-check, 14 per cent of the corpus, not
  either of the last two prompts), the second sentence opened by the deliverable's use rather than "Put", the rounding
  sentence opened by the figures it governs, deliverable set docx and csv (no build in the window; architecture 1's was
  pptx and xlsx). Architecture 1's shell (how-many, our, pptx+xlsx) is in `lineage_shells`.
- People (`guard.py names --geo england`, seed 402 and then 4020; architecture 1's four skipped, and Lesley Thompson
  and Ronald Bailey redrawn on the coordinator's read, `people.last` against task155 and `people.first` against
  task110): Frances Greenwood, Terence Cooper, no people WARN on `check`.
- The four go/no-go screens, run as a prototype on the clean truth before the card was registered (scratch proto4,
  eight draws, about 58,000 most-deprived-fifth kits a year):
  1. Realistic levels: completion within thirteen weeks about 55 per cent in the most deprived fifth to 74 in the
     least [OHID Fingertips, bowel screening uptake by deprivation decile, 2023-24]; previous participants about 88,
     previous non-participants about 22, first-time invitees about 58 [programme round reports]; moves of 50 to 74
     year olds about 3 a year for owners, 6 social renters, 20 private renters, two thirds within the county [English
     Housing Survey 2022-23]; a request applied on average six months later; mail to an address left reaches the
     person about one time in five [redirection volumes against moves]; the reminder at four weeks worth 5 to 7 points,
     so eight weeks loses about 0.8 inside thirteen weeks; outreach trials 1 to 2 points, its end 0.5. Measured: D costs
     the most deprived fifth 370 to 395 screens in 2025-26 against 230 for E, the next real change; minimum ratio 1.60
     across the draws, spread plus or minus 13, mid-bin at the nearest 100 (every draw in the 350 to 450 bin, at least
     20 from an edge).
  2. The golden's own method holds the call: D's cost by a matched comparison (non-pending kits by previous
     participation, first invitation, sex and age band) 373 to 412, by the completion gap against all non-pending
     kits 374 to 412; the next real change at most 232; minimum ratio 1.61. No fork in the method closes only by naming
     the step.
  3. No easy completion: the pending cohort is predicted from every visible attribute at AUC 0.5 to 0.6; the joint
     model with year, the locality term, the October term and every visible covariate has no term for D because D
     never varies inside the files; once the cohort is in hand the cost is a difference in completion, no functional
     form. The cracker's flexible versions (age-standardised, by locality, by half-year, joint, by previous
     participation) all name E, C or A.
  4. Literal execution: the fund's terms file population, window, outcome, unit and the comparison (what those kits
     would have completed without the change). Executed for every change with every natural operationalisation (the
     year against 2024-25, the localities and half-years as differences in differences, a joint model with every
     visible covariate, exposure by kit date or by request date), D's cost is zero every time: it was in force through
     both years at one rate and the files hold nothing from before it. The literal winners: C or the April residual
     422 to 748 when the whole fall is put on the April changes, A 90 below to 410, E 17 below to 335 by its half-year
     difference, the joint model's year term 161 below to 408; never D. The golden needs a step the terms never ask
     for: setting each kit's despatch date against the shared service's open request for that person.
- Coordinator's stage-2 rows (2026-11-03, after the merge at bfe5590), measured on the clean truth (scratch proto5,
  five draws) or decided, each to be re-measured on the generator and asserted in `checks.py`:
  1. What the pack holds before April 2024: no file reaches before D's start (the invitation extract and the queue
     export begin 1 April 2024; the registration history carries pre-2024 addresses but no request dates), so there is
     no before-and-after for D. The counterfactual "without D" comes from one filed fact in the shared service's own
     transfer document, in its voice and naming no method: before 1 April 2024 practice staff keyed an address change
     on the day it was received or the next working day. D's cost in the most deprived fifth under the defensible
     pre-D lags: 387 (none), 382 (2 days), 371 (7 days), 356 (14 days); the filed fact admits 0 to 3 days, 368 to 399,
     every draw mid-bin at the nearest 100 (at least 18 from the 350 edge). A 14-day lag would sit 6 from the edge, so
     the filed fact's words carry the day.
  2. Returned kits: a regional hub logs a kit returned undelivered when the envelope comes back; most misaddressed
     kits never do. Decided: the invitation extract carries a "returned undelivered" kit status for about one
     misaddressed kit in eight plus a baseline of about 0.2 per cent of all kits (deaths, demolished and invalid
     addresses), the same in both years. Costing D from returned kits alone gives about 105 screens in the fifth, a
     lower rung below E; the count does not move between the years, so the year-on-year route never reads it.
     Readability row for the field: test 2 schema fires on a twelfth of D's kits only; the decisive rung stays silent.
     To measure on the generator.
  3. The domain test and swap lines now stand on the epidemiology (the deprivation gradient in moving house, the
     programme's completion measure, the decomposition by fifth); the graded quantity is completed screens lost in the
     most deprived fifth on the programme's measure.
  4. The April 2025 coincidence: B's new age band (first invitations at 50 and 51) is visible in the extract, so the
     golden prices B by its own kits (it adds about 1,670 screens in the fifth) and C on settled kits outside B's band
     and A's localities across 1 April 2025, standardised for age. C's true effect is nil; the prototype's quick
     estimate (371 to 628) left B's first invitations in the comparison and is void; C's golden is re-measured on the
     generator with B's band removed, and D must lead A, B, C and E by 1.15 times or more under every golden variant.
  5. The literal solver who will not accept zero for D and costs it from the pack's own mobility evidence without the
     decisive join: completion of people whose address took effect in the 12 months before despatch against everyone
     else, times those movers. It lands D at 36 (6 to 75), below E and A, because a pending person's move has not
     taken effect on the register at despatch: the register's movers are exactly the people whose kits reached them.
     With a genuine 8-point mobility barrier the same row reads 214 (185 to 235), level with E, so the generator holds
     the barrier at 2 points or less and asserts this row below E. The join that does land D is a kit's despatch set
     against a request received in another organisation's queue and not yet applied: that is the decisive step, not a
     field read.
- Sources: every input file is synthetic, generated by `generator/` (seed and licence in `metadata.json`); the
  deprivation lookup assigns invented small areas to national fifths in the published indices' format; the published
  rates above set the generator's levels and are cited, not shipped.

## Default path

The pipeline a strong analyst builds from the fund's terms and the files' grain, with the field's method in it.

1. Read the fund's terms: kits despatched 1 April 2025 to 31 March 2026, the most deprived fifth by the registered
   address on the despatch date, a completed screen as a usable result inside thirteen weeks, each change costed as
   the screens those kits would have completed without it, less those they completed.
2. Join each kit to the registration history at its despatch date, place the address in a deprivation fifth through
   the area lookup, and keep the most deprived fifth; count a spoilt kit's re-test once.
3. Standardise completion for age by five-year band (the field's method for comparing a group's rate across years),
   2025-26 against 2024-25.
4. Cost each change against 2024-25 by its natural exposure: B adds first-time invitees and their screens, so it costs
   nothing; A by its localities against the rest of the fifth; E by kits from 6 October against April to September,
   net of the same split a year earlier; C and whatever remains by the residual from April.
5. D ran through both years and the files hold nothing before it, so its year-on-year contrast is zero; set aside.
6. Rank the costs and file the largest.

Ends on: E, the reminder moved to eight weeks, about 250 screens.
Golden: D, the shared registration service, about 400 screens.

## Stump sentence

A solver who standardises completion for age and costs each change on the review against 2024-25 files E, the
reminder moved to eight weeks, at about 250 of the most deprived fifth's screens, setting D aside because it ran
through both years; the step that lands them there is never setting each kit's despatch date against the shared
registration service's open address requests, which shows kits posted while a change was pending going to the address
the person had left, about 400 screens a year in the most deprived fifth, so the fund goes to D.

## Three rules

- Task type: health-equity-disparity-decomposition (Epidemiology and Public Health), which serves Root-Cause in the
  taxonomy; the equity fund is decided on the most deprived fifth's shortfall split by cause.
- Domain test: the deciding quantity is each change's cost in completed screens to the most deprived fifth on the
  programme's own completion measure, the equity decomposition of that fifth's shortfall by cause; it turns on the
  deprivation gradient in residential mobility (the most deprived fifth moves house about twice as often as the
  least, so more of its kits fall inside a pending window), read on the round structure and the thirteen-week
  completion clock, the way the field decomposes a screening gap by fifth.
- Swap: swapped to parcels ("which change cost the poorest fifth of customers the most delivered parcels") the
  misdelivery survives, but the decision does not: the cost is graded on the programme's completion measure in the
  most deprived fifth, its size is set by the deprivation gradient in moving house and by the round and the
  thirteen-week clock, and the fund is an equity decomposition by fifth; none of those has a parcel analogue.
- Layer 1: a registration history whose rows carry the date each address took effect, beside the shared service's work
  queue export (requests with received and completed dates, several request types); the programme's monthly uptake
  report on the address held at despatch; spoilt and technical-failure results re-tested under a new kit number; first
  invitations added mid-round by the age extension; despatch stamped in local time against laboratory receipt in UTC;
  localities defined on practice lists against residence for deprivation. Each is produced by the system that holds it,
  and none moves the call when mishandled.
- Layer 2: estimand identification; the methodological choice is how to cost a change that never varies inside the
  files: the year-on-year comparison the field reaches for gives it nothing, and its cost is identified only inside the
  year, through the kits it touched against the kits it did not.
- Decisive step: set each 2025-26 kit's despatch date against the shared registration service's queue for that person;
  a kit posted after an address change was asked for and before it was applied went to the address the person had
  left, and those kits, against comparable kits that reached their door, carry the most deprived fifth's largest loss.
- Not semantics: every field (registered address, request received and completed dates, despatch date, result codes,
  the fifth lookup) can be read correctly and the year-on-year costing still files E, because D's loss is identical in
  both years and no field marks a kit as sent to a former address.
- Not rule application: no filed rule or procedure says which kits reached a door or how to cost a change in force in
  both years; the terms name the population, window, outcome, unit and comparison and nothing else. Enumerated family
  (every construction a competent analyst reaches for, measured in proto4): D's cost from 0 (year-on-year, differences
  in differences, the joint model, exposure by kit or request date) to 373 to 412 (the pending-cohort constructions).
  Standing family (what the data and terms leave defensible once the cohort is seen): 373 to 412 across matched and
  gap comparisons, all one bin at the nearest 100. What rules the zero out is loud once looked at: kits posted while a
  change was pending complete at about a fifth of the rate of comparable kits, across thousands of kits.
- Analyst test: a strong analyst who reads every field and the terms correctly standardises for age, costs each change
  against 2024-25 and files E, the reminder moved to eight weeks, at about 250 screens, setting D aside as in force
  through both years; executed on the generator's clean truth in `checks.py`.
- Estimand: the equity fund's terms (the trust's governing document, `equity_fund_terms_2026-27.docx`): population,
  kits despatched 1 April 2025 to 31 March 2026 whose registered address on the despatch date lies in the most
  deprived fifth; outcome, a completed screen (a usable result inside thirteen weeks of despatch, a re-test counted
  once); window 2025-26; unit, completed screens; comparison, for each change on the review, the screens those kits
  would have completed without it, less those they completed; the fund goes to the change with the most.
- No decoy: nothing is planted. Every change on the review is real and has its true effect (B adds screens, C has
  none, A and E cost a little); no memo, draft, briefing or stakeholder figure argues for any change; the monthly
  uptake report ranks nothing.
- No certified replay: no figure in the pack is certified against a method; the uptake report states rates on the
  programme's own convention and blesses no costing.
- Lesson: an ongoing cost is a level, not a movement; a comparison of a year against the last cannot cost a change in
  force in both, and the cohort it hurts is found by setting each action's date against another organisation's open
  record. No build on file teaches it: the corpus's root-cause builds cost changes by their movement, timing or
  exposure, and none has a winner whose loss is constant through the compared periods.

## Survivor anatomy

- Actor: the deciding property, a kit posted while the person's address change sat open in the shared service's
  queue, has no column in any file: it is the overlap of the invitation extract's despatch date with the queue
  export's received and completed dates for an address-change request; the registration history stores only the date
  each address took effect, and the uptake report only the address held at despatch.
- Link: read through a comparison no key invites and no sentence asks for: each kit's despatch date against another
  organisation's work queue for the same person. The queue export is the shared service's own turnaround record, the
  review's evidence for D's line; nothing in the terms, the review or the files sets its dates against despatch.
- Reflex: the field's method for the deciding quantity (completion standardised for age by deprivation fifth, each
  change costed against the year before, the fifth's fall split by change) sits at rung 1 and files E.
- Back-test: the textbook route validates: the monthly uptake report reconciles to the invitation extract month by
  month on its own convention, and the year-on-year costing accounts for the fifth's fall with A, C and E and leaves
  nothing for D, which never moves inside the files.
- Second use: every file the decisive step reads has its own use: the invitation extract carries the whole pathway
  and every rung; the registration history places each kit in a deprivation fifth; the queue export is the review's
  turnaround evidence for D and the source of the fifth-by-registered-address convention's audit.
- Shock: the loss reads as ordinary non-response in the fifth whose completion is always lowest; no shipped statistic
  sorts the pending cohort to an extreme, and the kits went out and did not come back, as one in four never do.
- Pins: the WHAT sits once in the equity fund's terms (population, window, outcome, unit, comparison, decision rule);
  no filed sentence names addresses held, the queue, open requests, despatch against requests or the year-on-year
  comparison. Deleting each filed sentence in turn (asserted in `checks.py`): no deletion moves the call toward D, and
  deleting the comparison clause leaves "cost" undefined, so it stays.

## Readability screen

Rungs: R0 B by the crude completion rate; R1 E by the age-standardised year-on-year costing; R2 C by the April
residual left after A and E; R3 (decisive) D by the pending cohort. Tests: 1 filed sentence, 2 schema, 3 reflex, 4
control bench, 5 hygiene, 6 linear, 7 dedicated organ.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 B, crude rate | no | yes (age column) | yes | no | no | yes | no | readable |
| R1 E, year-on-year | no | yes (despatch date) | yes (the field's method) | no | no | yes | no | readable |
| R2 C, April residual | no | no | yes | no | no | yes | no | readable |
| R3 D, pending cohort (decisive) | no | no (three dates, two files, no column) | no (the field costs a change by its movement) | no (no control ties to it) | no (despatch inside a request's open interval is no consistency check) | no (a matched comparison inside the year) | no (the queue is the review's own evidence for D's line) | silent |

## Semantic fork table

Main-call terms and conventions. Each closure is a filed WHAT in the fund's terms or `same call`, asserted in
`generator/checks.py` under these ids, with the cross product of SF2, SF4 and SF6 asserted together.

| Id | Term or convention | Golden reading | Alternatives | Ruled out by |
|---|---|---|---|---|
| SF1 | completed screen | a usable result (normal or abnormal) within thirteen weeks of the kit's despatch | any kit returned; within six months; results dated in the year | the terms' outcome sentence; same call under each (asserted) |
| SF2 | the most deprived fifth | the national fifth of the area holding the registered address on the despatch date | address at result; latest address; the address asked for | the terms' population sentence; same call under each (asserted) |
| SF3 | 2025-26 | kits despatched 1 April 2025 to 31 March 2026, local date | invitation letter date; result date | the terms' window sentence; same call (asserted) |
| SF4 | a change's cost | the screens those kits would have completed without the change, less those completed | the fall against 2024-25 | the terms' comparison sentence; the golden under either reading of the counterfactual's baseline is D (asserted) |
| SF5 | B, the age extension | first invitations added screens, so B's cost is below zero | B's effect on the rate | the terms count screens; same call (asserted) |
| SF6 | spoilt kits and re-tests | one person-round; a re-test's usable result completes the round | each kit counted | the terms' outcome sentence; same call (asserted) |
| SF7 | people who died or left the region after despatch | in the population (the kit was posted) | removed | the terms' population sentence; same call (asserted) |
| SF8 | D's in-place date | 1 April 2024, every request handled by the shared service from then | requests received before 1 April 2024 and completed after | the review's D line; same call (asserted) |

## Ladder

Positions and margins are re-measured on the cut pack by `checks.py` and written here from its output; the
prototype (proto4, eight draws) gave the shape below.

| Rung | Construction | Winner | Its figure | D's figure there | Dies to |
|---|---|---|---|---|---|
| R0 | crude completion rate in the fifth, 2025-26 against 2024-25 | B | the fall concentrated in first invitations | 0 | the terms count screens, and B's first invitations add them |
| R1 | completion standardised for age, each change costed against 2024-25 by its natural exposure | E | about 250 | 0 | inside the year, kits whose address was settled show no change at October beyond E's own effect of about 230 |
| R2 | the April residual after A's localities and E's half-years | C | 50 below to 450 by draw | 0 | kits whose address was settled show no change across April 2025 |
| R3 | each kit's despatch date against the shared service's open requests; the pending kits against comparable settled kits | D | about 400 | about 400 | (the golden) |

Pricing sequence (stumping Part 3), on the clean truth: residue the WHAT leaves, how a change in force through both
years is costed; the ceiling, every pending kit's lost screen at about 0.4 of a screen each against about 1,000
pending kits a year in the fifth; the one-group-by route, none (D never varies inside the files); the standard error
of D's cost about 13 against a margin of about 150 over E; the lever and the ranked quantity are not one variance;
the unit's own history is flat across both years by construction; the bound subset hands nothing over (no row is
censored or capped); the reflex sweep as code, the pending cohort at AUC 0.5 to 0.6 on every visible attribute.
Dominance asserted in `checks.py`: D's figure over every rival's widest estimate by 1.15 times or more, every rung's
winner over its runner-up by the same floor.

## Closure table

| # | Axis | Reading here | Closure |
|---|---|---|---|
| 1 | Population | kits despatched in 2025-26 to people whose registered address on the despatch date is in the most deprived fifth | SF2, SF7 filed |
| 2 | Unit of account | the person-round; a completed screen is one round | SF1, SF6 filed |
| 3 | Attribution window | the despatch date | SF3 filed |
| 4 | As-of dating | the extracts taken in July 2026, every kit despatched to 31 March 2026 with thirteen weeks run | filed in the terms |
| 5 | Version basis | the extracts over the monthly uptake report | the report is a convention, not a rival; same call |
| 6 | Denominator | none for the call (screens); rates only in R0 and R1 | SF4, SF5 |
| 7 | Weighting | age standardisation to the 2024-25 kits' five-year bands, for the rungs only | same call under any standard |
| 8 | Window length | one financial year | SF3 |
| 9 | Boundary inclusivity | 1 April to 31 March inclusive, local dates | asserted inert |
| 10 | Rounding path | whole screens, the call to the nearest 100, rounded once | in the prompt's rounding sentence |
| 11 | Tie-break | not needed: D over every rival's widest estimate by the asserted floor | asserted |
| 12 | Maturity and censoring | thirteen weeks run for every kit by the extract date | filed as-of |
| 13 | Order of operations | place each kit in a fifth, then cost each change | same call in either order |
| 14 | Row order | none | asserted over permutations |
| 15 | Duplicate resolution | a re-test is the same round (SF6); re-sent despatch rows share a kit number | asserted |
| 16 | Identity normalisation | NHS number across the invitation, registration and queue files | asserted single key |
| 17 | Netting against gross | B's added screens net against nothing | SF5 |
| 18 | Dimensional units | screens are counts | n/a |
| 19 | Code and status semantics | result codes (normal, abnormal, spoilt, technical failure); request types and statuses | SF1, SF6, SF8 |
| 20 | Integerisation | whole screens | rounding once |
| 21 | Clause scope | the cost clause applies to every change alike | SF4 |
| 22 | Forward window contents | none: the fund is decided on the closed year | n/a |

## Literal reader

A literal reader executes the fund's terms word for word: the population, window, outcome, unit and comparison are
each filed once, and the comparison ("the screens those kits would have completed without the change") is executed
for D, the one change that never varies inside the files, only within the year, through the kits D touched against
comparable kits it did not; every other change's literal costing and the golden's agree within the bin, and D's
literal cost is the golden once the kits it touched are identified (`determinism-check` §2).

## Oracles

- The programme's monthly uptake report: confirms the size of the fifth's fall on the wrong path and on the right one
  alike (it states rates on the address held at despatch and ranks no change); ties under every basis.
- The review's D line with the shared service's turnaround figure: confirms that requests take time on every path,
  names no kit; ties under every basis.
- No control ties only under the golden.

## Ask sheet

Design (to be cut and measured; the asks sit on the screening pathway's own records downstream of a completed screen
and in the helpline's case log, files the main call never reads).

- Ask 1, abnormal results seen within fourteen days, each month of 2025-26 (12 figures, whole people). H18 home: the
  pathway's own timeliness measure every change's case carries. Use: the fund's paper reports the pathway behind the
  screens. Files: specialist screening practitioner clinic bookings (ask-only), the laboratory results' abnormal rows
  (read for dates only). Primary (D7, a reconstruction): appointments rebooked through the hospital switchboard carry
  the hospital number only; the person is recovered through the booking they replaced. Second device (D3, disjoint
  block): from the clinic's site merger on 3 November 2025 the second site's rows use its own status vocabulary.
  Pin test: the sentence carries the clock (the result letter's date) and the counting unit (a person's first
  attended appointment); both devices sit in which rows are the same person and which status is an attendance.
- Ask 2, each endoscopist's adenoma detection rate on screening colonoscopies in 2025-26 (one figure per endoscopist,
  per cent to one decimal). H18 home: the quality measure every colonoscopy the screens lead to carries. Files:
  endoscopy procedure reports, pathology specimens, the endoscopist roster (all ask-only). Primary (D6, a
  reconstruction): pathology is one row per specimen pot, linked to its procedure only through the accession prefix
  of the specimen number; a procedure counts once. Second device (D7, disjoint block): trainee lists are recorded
  under the supervising endoscopist's code with the trainee in the assisting field, and the sentence names the
  endoscopist who performed it. Pin test: the sentence names the screening colonoscopy, the year by procedure date and
  the performing endoscopist; the devices sit in which rows are one procedure and whose list it was.
- Ask 3, web-form kit queries received and answered within two working days, each month from April 2025 to March 2026
  (24 figures). H18 home: C's own measure. File: the web-form case log (ask-only) and the service calendar. Primary
  (D1, a reconstruction): a person who writes again while a query is open is given a new case number; the queries are
  one event by person and kit within the open interval, with no merge field. Second device (D8, disjoint block): the
  case log stamps receipt in UTC and the service's working day is local, so receipts in the last hour before midnight
  in British Summer Time fall on the next day. Pin test: the sentence carries the clock (working days in the service's
  calendar) and the counting unit (a query, not a case).
- Main population zero-counts: no device or hazard row in the invitation extract, registration history, queue export
  or the lab's results for completion (asserted by count from the shipped rows).
- Cracker sheet, full includer, no-repair profile and mirror: to be scored by `generator/ceiling.py` on the cut pack.
- Pair ceiling: to be measured (target 51, bar 60).
- Mirror leakage: to be measured (target under 40 per cent).
- Measured by: generator/ceiling.py (to be written with the generator).

## Tried and rejected

- The seed's world (2026-11-03, at the draw): a wind turbine's five faults read against the turbine's own healthy-year
  power curve is task187's insight (a unit's shortfall against the right reference curve at matched conditions) in the
  same room (turbines, nacelle anemometers, icing, yaw, pitch); its client domain (Supply Chain & Logistics) reaches
  Root-Cause only through interpretability, ruled a backdrop for an operations world at task129 v1; energy's
  Root-Cause cell is task129's and the room is task187's. Moved before any harness.
- Screened on paper at the draw (2026-11-03), each set aside before any code, with the reason:
  - an epidemiology composition draw (a borough's excess admissions carried by care home residents): task401's cell
    and insight, registered the same day;
  - drug co-prescription (the "triple whammy") behind excess acute kidney injury: the coarse exposure (any of the
    three drugs) contains the fine one, so the attributable count is the same either way, and naming the target
    population makes the step a filed rule;
  - a point-of-care assay's missed RSV corrected from quality-control re-tests: two-phase verification weighted by the
    testing rate is spent (task267, task120, task124, task228, task274's screen) and a verification report names the
    sensitivity;
  - stated cancellation reasons corrected from a save desk's probed reasons: the "true" reason is another opinion, so
    either the plan names it (a rule) or the reading forks, and it re-attributes losses away from a filed label
    (task13);
  - fluoridated water supply zones behind child dental extractions: an outcome scaling with a property of each case's
    surroundings is task129's form;
  - preventer supply lapsing over the school holidays behind September asthma admissions: a per-event state rebuilt
    from consecutive records is task121's device and close to its insight;
  - stock against flow (length-biased) census sampling: task182's driver;
  - an inspection window's onset: task487;
  - competing exits in a cumulative incidence: task133's lesson;
  - immortal time in a churn driver model: the decisive step is the exposure clock, which a pin would name;
  - net of recovered or deferred demand: either a count of listed recoveries (a rule) or a window the WHAT names;
  - a production line's restart tail booked as speed loss: no client domain with a Root-Cause task type holds it;
  - a fraud model's false declines from a holdout: precision moving with the base rate is task446's insight;
  - a mystery-shop routine blind to evenings: the swap test reads the same in any branch network.
- The first harness world (2026-11-03, stage 2): agency cover allocated by a wait threshold of 16 weeks, so short and
  long waiters both reached it; the cross-tab of wait band by first practitioner separated the wait from the cover at
  once (101 long waiters with employed therapists recovering at 51.6 per cent, 142 short waiters with agency cover), a
  cheap route to A. Redrawn so the cover takes the backlog (waits of 18 weeks and over) and one long-standing locum
  carries ordinary short-wait courses.
- Waits rising through the year with the cover ending in early November (2026-11-03, stage 2): about 400 long waiters
  started after the cover ended and went to employed therapists, the same cheap separation. Redrawn so the backlog
  forms between January and June 2025 and the initiative's funding ends on 19 December 2025 with final blocks booked
  to that date.
- A waiting-list leaving hazard of 0.85 per cent a week (2026-11-03, stage 2): with the longer backlog, C's own cost
  (the extra leavers) exceeded A's at three seeds of six. Lowered to 0.30 per cent.
- Telephone-first step 2 at 2.2 points of recovery with a small video and face-to-face group (2026-11-03, stage 2):
  B's reads swung from -25 to 102 by method, within reach of A. Cut to 0.4 points with a larger comparison group.
- G4 and then G6 as the decisive generator (2026-11-03, stage 2): refused by `check` (test.same_driver against task232
  v2, whose interviewer change between waves identifies a roster effect, task121 v6, task129 v2 and task243;
  test.same_puzzle_older against task144, task228, task265 and task68). G9 stays decisive.
- A flat list-leaving hazard of 0.6 per cent a week (2026-11-03, stage 2, risk 1): the backlog's leavers split across
  2024-25 and 2025-26, so C's extra leavers fell to 12 and C with leavers came within 1.07 times of coarse A. Replaced by
  0.3 per cent a week to 18 weeks and 2 per cent after (C's leavers 56.1).
- Monday-start agency bookings (2026-11-03, stage 2): lapses bunched on single Sundays (130 to 215 broken courses a date)
  and the long-wait employed cell rose to 21. Starts drawn over working days.
- A first wave started over six weeks with a first renewal of 0.2 (2026-11-03, stage 2, risk 3): 524 of 762 breaks fell in
  August and early endings jumped to 313 in September as agency therapists in post fell from 38 to 16, the readability
  screen firing on the monthly chart. Spread over ten weeks with a first renewal of 0.4.
- No referral surge (2026-11-03, stage 2): step 3 starts fell to 0.4 of normal from December 2024 to April 2025 while 40
  employed therapists stayed in post, an idle-staff tell. A winter rise in referrals forms the backlog instead.
- Loose clearance without longest-first order (2026-11-03, stage 2): broken courses halved, A fell to 110 to 160 and rivals
  came within 1.2 times at some seeds. Longest-first kept.
- The long-standing locum taking 5 per cent of ordinary step 3 patients: about 40 sessions a week. Cut to 2.5 per cent.
- Seeds 7 and 14 (2026-11-03, stage 2): seed 14's longest waiters recovered best inside the backlog cohort (30 to 33 weeks
  38.6 per cent against 20.7 at 18 to 21 weeks), a dose-response a careful solver would read against the wait; seed 7 sat
  on an earlier world. Seed 402 shipped: no gradient inside the cohort, every filed-comparison estimator mid-bin.
- Ask devices dropped at stage 2: carried-across digital patients (discovery and remedy one act); the digital beginners,
  the over-18-week counts and the agency cover's November and December (no device reaches them); three agency therapists
  booked after the backlog cleared, with no patients (an idle booking reads as generated), left out of the pack.
- Ask devices one-sided against the full includer (2026-11-03, stage 2, the coordinator's precut read): an off-call
  response that handles every device banks the ask weight. The timesheet corrections were made two-sided at the route
  change of 1 August 2025 (filed in the register), and the digital ask was moved to span the January 2026 content release.
  Its first form, which only added sections, let the cracker's whole-export inference keep January and February (2 of 6),
  so the release also retires a section of module 3, and both structures now count against any single inference. The
  waiting list ask stays one-sided (its WHAT cannot change mid-year without a filed rule the cracker would execute).
- Architecture 1, the Talking Therapies world (2026-11-03, stage 4): the determinism judge returned NOT_DETERMINISTIC,
  SEND_BACK. Gate H rule_application: the plan filed each change's cost as expected minus actual recoveries read from the
  year's other referrals at the same step, largest wins, so a solver executing it literally with any-contact exposure
  costs every change directly and lands A at 249 (naive comparator 267, golden 257, all 250 to the nearest 50; only the
  last-clinician exposure, 222, rounds to 200); the funnel walk filing C was not the route a rule-following solver takes.
  Gate F low to moderate. Gate C forks: A's exposure (any contact 250, last clinician 200); C had no filed in-place date
  or wait threshold and tied A at 248 to 257 on the same patients. Ask 4 (agency hours and cost by month) needed
  conventions no file stated (a dropped 2023 booking, the later of two portal timesheets before 1 August and summing
  after, catch-up lumps spread over unclaimed weeks, working-day allocation; week-commencing allocation moves June by
  about 1,200 hours). The reader's realism tells: a parquet footer naming pyarrow with a pandas schema block; near-even
  splits (step 50.2 against 49.8, three referral sources at 12.7, 12.7 and 12.5, authorisers in near-even thirds);
  near-uniform hourly slots; every timesheet Authorised, submitted on the 1st; every group course six sessions; UUIDs
  that are not valid version 4; whole-minute event times. The world is spent; re-rooted at architecture 2 in another
  world, dataset and shell (the dead shell: how-many, our, pptx+xlsx).
- Architecture 2 draw, screened and set aside before registering (2026-11-03): childhood immunisation call and recall
  with invitations to superseded addresses (the age-cohort windows made the WHAT fork and families' moves gave the
  lever, but a records-system change would have been the call); bowel screening with a new call-and-recall system's
  stale addresses accumulating from go-live (proto, eight draws: D 537 to 592 against 146; set aside because the
  cause is a two-system cutover, which the house rule bars from the call, and its ramp from the data's first month is a
  trend a cracker dates to the go-live); the same with an annual address reload (a sawtooth that resets each April,
  leaving an unexplained jump up at April 2025 on the changes' date); a one-off cohort of changes made during a
  pre-migration freeze (no time signature, but again a system cutover as the call); masking the winner's
  differences in differences by a concurrent benefit in the same localities (a balance that reads as planted); a
  universal winner tied with a universal decoy on the same date (every literal costing ties them, a tie the judge
  could call a fork). The shared registration service is an organisational change, not a two-system cutover, its
  loss is steady from its first months, and the year-on-year comparison gives it nothing.
- Pending cohort at a four-month mean wait and 240,000 people (proto3): D 129 to 148 screens against E 145, screen 1
  failed. Region doubled (less noise, same ratios), mean wait six months, E at 0.8 and A at 0.5 points (the low end of
  their published ranges): D 370 to 395 against 230 (proto4).
- Architecture 2 at honest levels (2026-11-03, stage 2, before any generator): the queue re-anchored to what the
  published accounts of a shared primary care support service support (NAO HC 632, 17 May 2018, and PAC HC 698, 2018:
  half a million patient registration letters in backlog and practitioners waiting months, with no wait distribution
  published), a first-in-first-out backlog of address changes at a mean of 15 weeks with 15 per cent applied quickly,
  85 per cent of within-region movers asking 0 to 8 weeks after moving, a kit to the address left completing at 0.30
  of normal (about half of movers redirect mail and fewer on low incomes, Citizens Advice, Left behind), a 1.5-point
  mobility barrier (no published barrier for colorectal screening): D costs the fifth 157 screens (sd 8, 20 redraws)
  against E's true 145 at 0.5 points (1.08 times) and 116 at 0.4 (1.36); every rival is costed by a difference of
  completion rates whose sampling sd is 120 to 280 screens (E within the year 120, E against 2024-25 169, A's
  localities 148, C on settled kits 202, the April residual 280), as large as D's lead, so D's lowest golden variant
  clears every rival estimator by 1.15 in 1 of 20 redraws, 3 of 20 with every lever at its honest edge (a 20-week mean
  wait, 0.20, everyone asking, E and A at 0.3 points, D 279) and 4 of 20 at the old six-month exponential; the
  shape-07 grid's fifteen rival cells carry the same noise, and the earlier screens had compared D with the rivals'
  true costs, never with their estimators. The movers-in-12-months row (46, sd 18) and the returned-kit row (26) stayed
  below E. Architecture 2 is spent before any data was cut (scratch t402/a2 proto6.py and p6_sd.py).
