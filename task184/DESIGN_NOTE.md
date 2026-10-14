# task184 design note (architecture 1)

New build in oviya13ya's Anomaly Detection lane (wave 2), from seed AD07. The seed's world, decision and quantity are
kept: a national screening agency posts its one mobile screening team to one of eight airports its throughput detector
flagged this spring, judged by the passengers the team moves through screening within the 20-minute standard. The
seed's pitfall (the team opens lanes only where a lane position stands idle) is a per-airport cap that re-places the
pick, the dead form of strategies.md F3 (58 v3 and v4), and its pick-one shape 01 is banned for this slot; the pitfall
is re-found from the data.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task184.json` (v1), registered 2026-10-12, hardened 2026-10-14. `guard.py
  check`: WARN overuse.org_family only (government_agency in 24 builds): a national screening agency is the
  organisation that owns this decision in every country that has one, and the axis is not banned. A first card (shape
  07, forum executive_team, question form which) was blocked against task180 and task136; the shape is 13 and the
  question form where.
- **Pairing:** Supply Chain & Logistics (house domain; client domain Urban & Regional Science), aviation passenger
  screening operations, objective Anomaly Detection & Diagnostics. Supply chain by anomaly detection is built once
  before (task54, a different world). The anomaly is each flagged airport's spring queue breach; the diagnosis is
  which breach the mobile team can actually relieve, which turns on what each checkpoint opens rather than what its
  roster pattern plans.
- **World:** a fictional North Atlantic island republic (Kestland), its national screening agency (Kestland Aviation
  Security) and eight airports with one central checkpoint each. The mobile team (24 officers on two shifts) staffs
  three lanes from 05:00 to 21:00 at whichever airport it is posted to. People (guard.py names, en_IE, seed 184):
  Ruairi Barnett, Alana Marnan, Fergus Rynne, Leon O'Boyle; roles fixed at design.
- **Stakeholder, forum, forcing event:** the head of screening operations (role `operations_director`) posts the unit
  for 15 June to 31 August 2027 and Screening Operations acts on it directly under the deployment policy (forum
  `operations_desk`, redrawn at build from `line_manager_or_team`, which task137 took the same day); the forcing event
  is the posting's start (`launch_or_rollout`).
- **Shape 13 (scenarios and the flip point):** each airport's posting is a scenario, graded on the passengers the unit
  moves within the standard over the summer (8); the call, the runner-up and the flip (the uniform shortfall in the
  chosen airport's forecast passengers at which another posting moves more); the chart's eight bars and the chosen
  airport marked; and three 2026 measures for every airport (24). About 40 criteria.
- **Strategy and gate:** `causal_design` (the counterfactual arm of a capacity comparison), gate G
  `decomposition_attribution` (the team's added capacity net of what the host does and of what the host never did),
  gap objective then time, generators G1 then G3, pattern none, layer 2 `estimand_identification`
  (own:counterfactual-arm-read-from-the-pattern-not-the-record), calibration `pilot_log` (last summer's postings).
- **Data-native sentence:** a checkpoint's roster pattern is its establishment, and the overtime block that covers the
  bank's extra lanes is shorter than the pattern, so seven of the eight open fewer lanes at their banks than the
  pattern plans, every day of the summer and whether or not the unit is there; the lane sensors count only the lanes
  that ran, and the same feed also shows the lanes a duty manager stands down while the unit screens, so one
  subtraction against the pattern holds both and the pattern cannot tell them apart.
- **WARN answered (precut, task type serves the objective):** Urban & Regional Science lists no task type against
  Anomaly Detection, so no Task type line can pass the check; the build's task type is
  `municipal-service-demand-resource-allocation` and the objective stays Anomaly Detection because the object of the
  analysis is the queue breach the throughput detector flagged at eight checkpoints this spring and the call is a
  diagnosis of it: which of the eight breaches the unit can actually relieve, and which is an artifact of reading a
  roster pattern as the lanes open. It is not retaggable as Forecasting (the answer is not a predicted value; the
  design-day arrivals are given) and the prompt would have to be rewritten to read as Opportunity Sizing, whose
  headline is a pool sized down to what can be realised rather than a pick among flagged sites.
- **Same-puzzle test:** no build in the last twelve shares gap objective, pattern G1 and decision pick_one_of_n;
  nearest drivers 0.06 (task128 v2, task89 v9, task67 v1), none with a comparison whose counterfactual arm is read
  from a plan the records contradict. task51 (additionality over a baseline a standing rule moves) and task88 (an
  added booking displacing full-rate demand) are the nearest structures and neither has the plan-against-record arm.
- **Sources (one line each):** strategies.md F9 (interference between units sharing a pool; here the pool is the
  host's own officers, released while the team is there) and the counterfactual family in `references/client/`
  (a treatment effect measured against a plan rather than against what the untreated unit actually does);
  measured-drivers.md Part 2 (a dimension that lives on another entity, and a conjunction: the two subtractions have
  to be told apart, and each on its own files a different airport).

## Default path

1. Read the planning standard (KAS-STD-07, 2026): the expected wait in each 15 minutes from the queue at the start and
   half the arrivals over the open lanes' rate; a change is judged by the passengers it moves within the standard
   on the design days, times the days in each period.
2. Take each airport's 2027 design days (late June, July, August) from the planning sheet and its summer 2027 roster
   pattern of lanes by interval.
3. Add the unit's three lanes from 05:00 to 21:00 to the roster pattern at each airport in turn.
4. Run the standard with and without the unit on each design day, multiply by the days in each period and add up.
5. Post the unit where it moves the most passengers.

Ends on: Cullinvale, 697,500 passengers moved within the standard, 1.29 times Ardcarrig (542,600); Eskerford fourth (398,400).
Golden: Eskerford, 342,200, 1.26 times Halloran Bay (272,600), the one checkpoint of the eight whose roster pattern is what it opens.

## Stump sentence

A competent solver runs the planning standard on each airport's 2027 design days and summer roster pattern with the
unit's three lanes added and posts the unit to Cullinvale, where it moves 697,500 passengers within the standard; the
step that lands it there is taking the roster pattern as the lanes that will be open, on both sides of the comparison,
when the checkpoints' own lane counts show seven of the eight opening fewer lanes at their banks than the pattern
plans on every day of the summer, Eskerford two fewer, so Eskerford's posting is worth 342,200 and not 398,400 and
comes first.

## Three rules

- **Task type:** `municipal-service-demand-resource-allocation`, the client taxonomy's task type for placing a public
  service's own capacity against the demand each site carries, worked here as the diagnosis of which flagged breach
  the posting can relieve (the WARN this raises is answered in `## Draw`).
- **Domain test:** the decisive analysis is checkpoint capacity planning: a fluid queue on 15-minute arrivals against
  the lanes actually open, scored against the 20-minute wait standard, with both arms of the comparison, the lanes
  open without the posting and with it, built from the checkpoint's own lane counts rather than from its roster
  pattern.
- **Swap:** "which clinic should the relief nursing team be posted to, and how many patients would it see within the
  30-minute standard" has no lane, no bank of departures, no queue carried from one 15 minutes to the next and no
  roster pattern that the establishment staffs and the overtime block does not, so the counterfactual arm has nothing
  to be read off and the task stops making sense.
- **Layer 1:** a lane sensor feed at 15-minute grain carrying the unit's positions and two staff and aircrew lanes per
  checkpoint under ordinary lane ids; a queue-camera feed with gaps; lane faults on the unit's off days; a superseded
  2023 edition of the standard beside the 2026 one; hotel invoices whose every line repeats the stay's
  officer-nights, with a credit note; a claims export assembled from monthly batches, the August batch appended
  twice; travel claimed on the Sunday before a posting week. Each is what these systems produce, and none decides
  the call (the asks' devices sit outside the call's rows, asserted).
- **Layer 2:** the shortcut is to compare a plan with a plan plus the posted resource; the expert builds both arms of
  the counterfactual from what the host actually does, and has to split the shortfall a posted day shows against the
  pattern into the part the posting caused and the part that was there anyway.
- **Decisive step:** taking the lanes open without the posting from the checkpoint's own days rather than from its
  roster pattern, so the posting's effect is measured against what the summer will look like without it.
- **Not semantics:** every field, code, unit and definition read correctly still leaves the easy route wrong, because
  nothing in the pack is misread: the roster pattern really is the lanes planned, the lane feed really is the lanes
  that ran, and the standard really does ask for the passengers outside the standard without the change. What the
  easy route gets wrong is which record stands for "without the change".
- **Not rule application:** no filed rule says what a checkpoint will open. KAS-STD-07 6.1 fixes the quantity (the
  passengers outside the standard without the change less those outside it with it) and 3.1 fixes what an open lane
  is; neither says to read the counterfactual arm off two summers of lane counts, nor how to split a posted day's
  shortfall into the posting's part and the checkpoint's own.
- **Analyst test:** a strong analyst who reads the planning standard, the 2027 design days, the roster patterns, the
  lane feed and the postings file correctly adds the unit's three lanes to each airport's roster pattern, runs the
  standard and posts the unit to Cullinvale, 697,500 passengers moved within the standard, 1.29 times Ardcarrig
  (542,600); Eskerford fourth (398,400). Wrong, because the roster pattern is not what any of the eight opens.
- **Estimand:** the passengers outside the 20-minute standard on the lanes open at the checkpoint without the unit,
  less those outside it on the lanes open with the unit, on each design day of 15 to 30 June, July and August 2027,
  times the days in the period; filed in KAS-STD-07 6.1 with 3.1 defining an open lane as one staffed and screening.
- **No decoy:** nothing is planted to be caught. No block is copied, no rule withheld, no memo, draft or briefing
  argues a wrong answer, and no shipped figure ranks the eight airports on the posting question. Every lane count is
  the checkpoint's own record and nothing in it is wrong.
- **No certified replay:** no published or certified posting figure exists in the pack, so the method cannot be
  recovered by reproducing one. Last summer's postings are a log of weeks and officer-nights, not of effects.
- **Lesson:** a posted resource's worth is the difference between two states of the world, and the untreated state has
  to be estimated from what the host actually does, not from the plan it files; where a record shows the plan was
  never met, the plan is the wrong counterfactual on both arms. No build on file teaches it: task51 moves a baseline
  by a standing rule, task88 displaces demand, and neither reads the untreated arm off a record that contradicts a plan.

## Readability screen

Each rung is the move a solver makes to leave the rung below; the decisive rung has to be silent on all six tests.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| lateral, last summer's realised effect per posted week (lands on Cullinvale, rung 0's answer) | no | yes, the postings file names the weeks | yes, a forecaster's first evidence | no | no | no | readable |
| 1, the posted day's whole gap averaged over the unit's hours | no | no | no, but natural once the gap is seen | no | no | yes, one mean subtracted | readable |
| 2, that gap by interval, the roster pattern still the baseline | no: no document names a stand-down or an unopened lane | yes in part: the gap is one subtraction of the lane feed from the pattern on posted days, which a solver reaches for once the unit's lanes are in view | yes, the correction a careful solver makes | no | no | yes | readable |
| 3, both arms on the lanes the checkpoint opens (decisive) | no: no document says a checkpoint opens fewer lanes than its pattern, names the overtime block, or distinguishes the two parts of the gap (asserted by word sweep over every document) | no: no column marks a lane unopened; it shows only as the lane feed's own days falling below the pattern, a cut across three files (lane feed, 2026 roster pattern, postings file) that a solver has no reason to make once the posted days are explained | no: the pattern plus three, last summer's realised effect, the averaged gap, the gap by interval and the gap taken off both arms all land elsewhere | no: no shipped figure scores a posting; the detector's flags rank the checkpoints on spring breach intervals, a different order | no: keys unique, every join matched, no duplicate, no missing day | no: the two parts of the gap enter the queue run in different intervals and on different arms | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | passengers moved within the standard | those outside the standard without the posting less those outside it with it, on the design days, times the days | passengers screened on the unit's lanes | not a reading: the standard defines the measure | KAS-STD-07 6.1 (asserted present) |
| SF2 | the lanes open with the unit posted | the roster pattern less the whole shortfall its posted days show, by interval, plus the unit's three | the roster pattern plus three | the default's ending, not a reading | the standard computes on lanes open and 3.1 calls an open lane one staffed and screening; every posted day at every host shows the same gap, Ardcarrig's two weeks running included, and the 2026 and 2027 patterns plan the same lanes (asserted) |
| SF3 | the design day | the planning sheet's design day for each period | none shipped | same call | the planning sheet is the only design-day source in the pack |
| SF4 | the periods | 15 to 30 June, July, August 2027 | whole June | same call | the prompt's dates; the planning sheet's periods |
| SF5 | the unit's hours | three lanes, 05:00 to 21:00, every day | weekdays only | same call | the deployment policy |
| SF6 | the 20-minute standard | over 20 minutes is outside; 20 or less within | 20 or more outside | same call | KAS-STD-07 2.2; no wait within 0.3 minute of 20 on the golden's runs nor 0.1 on the ladder's (asserted) |
| SF7 | the shortfall's size | whole lanes, the same every day | a fractional mean | same call | KAS-STD-07 3.1 (lanes counted whole); the differences are whole on every day with no fault on it (asserted) |
| SF8 | the flip | the smallest whole per cent uniform shortfall in the chosen airport's design-day arrivals at which another posting moves more | the last whole per cent still ahead (one less); scaled arrivals rounded or floored | same call, 13 | the prompt asks the smallest whole per cent shortfall at which another posting would move more (asserted present); rounding the scaled arrivals or not gives 13 (asserted) |
| SF9 | rounding | each summer figure from unrounded counts, to the nearest hundred | the sum of rounded periods | same call | the two agree at every airport (asserted); no figure within 2 of a rounding edge |
| SF10 | the lanes open without the unit | the lanes the checkpoint opens on its own days, the pattern less the bank lanes it does not open | the roster pattern itself | the rung-2 answer, Halloran Bay, not a reading of "lanes open" | KAS-STD-07 3.1 and 6.1 read literally ask for the lanes open, and the lane feed shows every checkpoint's own days falling below its pattern on at least forty days with no fault (asserted); taking the shortfall as lanes off the pattern or as the lanes left open reads the same |

## Ladder

Built values. Passengers moved within the standard over the posting, by airport.

| Rung | Construction | Names | Note |
|---|---|---|---|
| 0, default | 2027 design days, roster pattern plus three | Cullinvale 697,500 | 1.29 times Ardcarrig; Eskerford fourth, 398,400 |
| lateral | last summer's realised effect per posted week | Cullinvale 35,200 a week | 1.49 times Faranloe; Eskerford fourth, Halloran Bay last |
| 1 | the posted day's whole gap averaged over the unit's hours | Halloran Bay 212,600 | 1.77 times Eskerford (120,000) |
| 2 | that gap by interval, the roster pattern the baseline | Halloran Bay 272,600 | 1.31 times Eskerford (208,700); the same airport as rung 1 at a different figure |
| 3, golden | both arms on the lanes each checkpoint opens | Eskerford 342,200 | 1.26 times Halloran Bay (272,600), which is 1.13 times Ardcarrig (240,800) |

- **Variants (asserted):** the gap taken off both arms (double-counting the part that was there anyway) names
  Halloran Bay, 272,600, Eskerford 1.36 behind; the baseline corrected with the stand-down ignored names Cullinvale,
  814,900, Eskerford fourth; the gap averaged by shift names Halloran Bay, by whole day Halloran Bay, Cullinvale's
  stand-down applied at every host names Ardcarrig, and every one of them leaves Eskerford at least 1.10 behind.
  Averaging both arms by the hour instead of by 15 minutes gives Eskerford by 1.27, so the grain does not decide.
  The superseded 2023 basis moves the figures but not the call.
- **Position:** Eskerford fourth on rung 0, fourth on the lateral, second on rung 1 (by 1.77) and second on rung 2 (by
  1.31), first only on the golden; never first on an intermediate rung.
- **Dominance:** the baseline swings Eskerford's figure 1.64 times against Halloran Bay's, against Halloran Bay's
  carried lead of 1.31 on rung 2 (asserted at 1.2 times, needing 1.57).
- **Grid:** baseline (roster pattern, the checkpoint's own days) by posted-day gap (none, averaged, by interval, taken
  off twice): Cullinvale, Halloran Bay, Halloran Bay on the pattern; Cullinvale, Halloran Bay, Eskerford, Halloran Bay
  on the checkpoint's own days. Only the checkpoint's own days with the gap counted once name Eskerford.
- **Worth:** rung 0 matches the golden on none of the eight summer figures, rung 1 on none, rung 2 on one (Halloran
  Bay's, the one checkpoint that opens its pattern), so a response off the call keeps almost no airport figure.
- **Flip:** 13 per cent, the smallest whole per cent shortfall at which Halloran Bay's posting moves more.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the passengers arriving at each central checkpoint on its 2027 design days | filed in the planning sheet |
| 2 | Unit of account | a passenger arriving in a 15-minute interval | filed in the standard |
| 3 | Attribution window | 15 June to 31 August 2027 | the prompt's dates; the policy's posting dates |
| 4 | As-of dating | the 2026 records to 31 August 2026; the 2027 sheets as issued in April 2027 | filed in the extract notes |
| 5 | Version basis | the 2026 standard | it replaces the 2023 edition from 1 March 2026, on its face |
| 6 | Denominator | none (a count) | not applicable |
| 7 | Weighting | days in each period | 16, 31 and 31 days (asserted) |
| 8 | Window length | every day of last summer for the unopened lanes, every posted day for the stand-down | the same on every such day (asserted) |
| 9 | Boundary inclusivity | over 20 minutes is outside | SF6 |
| 10 | Rounding path | nearest hundred from unrounded counts | SF9 |
| 11 | Tie-break | none | margins asserted |
| 12 | Maturity and censoring | the 2026 records complete | every day's queue clears within the closing interval (asserted in the simulation) |
| 13 | Order of operations | lanes, then the queue run, then the difference | the standard |
| 14 | Row order | none | the queue runs in interval order, filed |
| 15 | Duplicate resolution | the lane feed has one row per lane and interval | asserted |
| 16 | Identity normalisation | operations codes across the operations files; purchase orders to postings for hotels | the extract notes' code list; the postings file |
| 17 | Netting | the stand-down nets against the unit's lanes; the unopened lanes net against neither, they sit on both arms | SF2, SF10 |
| 18 | Dimensional units | passengers, minutes, lanes, euros | the standard and the extract notes |
| 19 | Code semantics | lane ids, claim categories | extract notes; never the stump |
| 20 | Integerisation | lanes whole | SF7 |
| 21 | Clause scope | the posting from 15 June to 31 August 2027 at one airport | the policy |
| 22 | Forward window contents | 2027 design days, roster patterns, the unit's hours, what each checkpoint opens and the hosts' response | filed sheets; the two from every day and every posted day of 2026 |

## Literal reader

Executing the prompt, the deployment policy and the planning standard word for word: the unit goes where it will move
the most passengers within the 20-minute standard over the posting; an open lane is one staffed and screening
passengers (3.1); the standard counts a passenger arriving in an interval as outside it when the queue at the
interval's start and half its arrivals, over the open lanes' rate, take more than 20 minutes; a change's passengers
moved are those outside the standard on the lanes open without it less those outside it on the lanes open with it,
times the days. So each airport's figure is its 2027 design days run on the lanes it will have open without the unit
and with it. The only record of either is the checkpoint's own lane counts: its own days give the first, and its
posted days give the second. Every reading in SF1 to SF10 returns Eskerford; the default comes from the same estimand
by taking a roster pattern for an open lane on both arms, and rung 2 from taking it on one.

## Oracles

- The detector's spring flags: the eight airports flagged, the weeks and breach counts; a different question, its
  order is not the posting order and its worst checkpoint is not the pick (asserted).
- The 2026 lane feed on the unit's off days: it is the baseline arm itself, not an oracle on it; it scores no posting
  and names no airport.
- The operators' monthly returns: they reconcile with the passenger lanes in July and August (ask 1's referee); the
  call never reads them.
- None ties only under the golden.

## Ask sheet

The main call's declared row population: the planning sheet, the 2027 roster pattern, the 2026 lane feed's rows of
passenger and unit lanes from 05:00 to 21:00 on posted days, the 2026 roster pattern, the postings file's weeks and
airports, and the two documents. Staff and aircrew lanes (active only before 05:00 and after 21:00), the operators'
returns, the hotel invoices, the claims export, the queue-camera feed, the fault log and the feedback file are
outside it (asserted: the main path never opens them; no staff lane row from 05:00 to 21:00). Each ask is a measure
every candidate airport carries in the posting case (last summer's load and the posting's cost beside the call, H18),
on which the call does not turn; none is keyed to the call, and the three share no primary family and no file path.

**Ask 1. Passengers screened at each checkpoint, 15 June to 31 August 2026 (8 figures, nearest hundred).**
- Use: last summer's load beside the posting.
- Primary device (D5, out-of-scope rows known only by structure): two lanes at each checkpoint search staff and
  aircrew at the shift changes, in the same feed under ordinary lane ids, active only before 05:00 and after 21:00;
  summed with the passenger lanes every airport is high (by 13,800 to 27,600).
- Split evidence: the lanes' hours; the policy's line that the checkpoints search staff and aircrew before 05:00 and
  after 21:00; the operators' returns reconcile with the passenger lanes within 0.8 per cent in July and August and
  fall 1.2 per cent or more short of every lane (asserted). No sentence names the lanes.
- Hazard: the unit's lanes screen passengers and belong in the sum (dropping them puts every airport low, by 26,000
  to 112,900).
- Span (4 files, 8 columns): lane feed, lane register, operators' returns, policy.
- Stops (asserted outside the bin at every airport): every lane; passenger lanes without the unit's; golden.

**Ask 2. Hotel cost per officer-night at each airport, summer 2026 (8 figures, euros to the cent).**
- Use: the posting's cost.
- Primary device (D6, an event's quantity on every line it covers): every invoice line (room, breakfast where
  separate, local tax) carries the stay's officer-nights, so nights summed over lines divide by two or three times
  too many (31.24 to 45.15 against 84.70 to 116.72).
- Hazards: Halloran Bay's credit note for two officers' unused nights keeps a tenth of the room rate (dropping it
  gives 112.50 against 112.98); invoices reach airports only through the purchase order in the postings file;
  Cullinvale's second week at another hotel; Ardcarrig's two weeks on one invoice.
- Span (3 files, 8 columns): hotel invoices, postings file, extract notes.
- Stops (asserted): nights over every line; credit note dropped; golden.

**Ask 3. The unit's expense claims per posting week at each airport, summer 2026 (8 figures, euros to the cent).**
- Use: the posting's cost.
- Primary device (D1, a replay under fresh ids, key kept): the export appends finance's monthly batches and the
  August batch twice, so every line approved in August appears twice under new row ids with the same claim
  reference and line; summed, the airports posted from mid-July to mid-August are high.
- Hazard (D8, an anchor on the event's own date): each officer's travel out is claimed on the Sunday before the
  posting week, which falls in the previous host's week (or before the window for the first), so lines placed by
  their own dates move between airports; a claim belongs to the posting its subsistence days fall in.
- Over-cleaning stop: dropping rows that repeat officer, date, category and amount deletes genuine same-day taxi
  pairs.
- Span (3 files, 9 columns): claims export, postings file, policy.
- Stops (asserted outside the bin at every airport): every row by its date; lines once but by their date; rows once
  by officer, date and amount; golden.

**The cracker sheet.** The cracker landed Eskerford, ran the hygiene battery (keys unique, no exact duplicates,
every join matched) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, passengers 2026 (8) | every lane's counts summed by airport | staff and aircrew lanes counted as passengers | miss |
| Ask 2, hotel per officer-night (8) | invoice amounts over nights summed by line | nights repeat on every line | miss |
| Ask 3, claims per week (8) | export rows summed by airport over its posting weeks, each by its date | the August batch twice; travel dated the Sunday before | miss |
| Chart (rec block, not an ask) | carried by the main call | scored with the recommendation | outside |

The mirror sheet (stopped at Halloran Bay, rung 2) differs from the cracker sheet only on the recommendation
criteria, the chart and seven of the eight airport figures (it holds Halloran Bay's).

Mirror leakage: 6 per cent of the ask weight (Halloran Bay's own summer figure and method credit, no measure).

**Pair arithmetic.** Planning weights 38 recommendation, 7 instruction following, 55 asks over 32 figures (8 airport
figures, the construction layer the cracker holds, and 24 measures). With r = 5: C = 38 + 7 + 55 x 8/32 = 58.8 for
the cracker; S = 5 + 7 + 55 x 0.06 = 15.3 for the mirror.

Pair ceiling: 37.0

## Build record

- Generator: world (the eight checkpoints, their roster patterns, the lanes each one leaves closed at its banks, the
  lanes its duty managers stand down while the unit screens, last summer's postings), models (the standard's queue,
  the two arms of every basis), profiles (2027 design days with a late-morning wave, an afternoon lull, a thinning
  last hour, cresting banks and rough 15-minute noise, the draw per airport and period chosen to keep every golden
  wait 0.3 minute off 20, every figure off a whole thousand and a half-hundred tie, every summer figure equal to its
  rounded periods), sim (the 2026 summer: daily demand, faults on the unit's off days, the lanes each checkpoint
  opens, the stand-down on posted days, the queue, lane counts and the camera feed), records, docs, analysis, asks,
  deliver, checks, verify (pandas, the shipped files only), metadata, build.
- Built values: rung 0 Cullinvale 697,500 (1.29 over Ardcarrig 542,600, Eskerford fourth at 398,400); lateral
  Cullinvale 35,200 a week (1.49); rung 1 Halloran Bay 212,600 (1.77 over Eskerford); rung 2 Halloran Bay 272,600
  (1.31 over Eskerford's 208,700); golden Eskerford 342,200 (1.26 over Halloran Bay 272,600, itself 1.13 over
  Ardcarrig 240,800); flip 13 per cent. Rung 2 holds one of the eight summer figures (Halloran Bay's), rungs 0 and 1
  none.
- Ask goldens: passengers 2026 from 588,800 (Halloran Bay) to 1,218,600 (Cullinvale); hotel 84.70 to 116.72 per
  officer-night; claims 7,135.92 to 8,824.96 per posting week; every stop outside its bin at every airport.
- Realism envelope: the 2026 queue-time sensor reads a median of 4.5 minutes, a 99th percentile of 50 and a maximum
  of 80, with 18.5 per cent of intervals over the 20-minute standard; that is the summer the throughput detector
  flagged, and the design days are the planning sheet's forecast of the next one.

## Judge record

- Pass 1 (2026-10-12): NOT_DETERMINISTIC, FIX_NOW, on one answer only. "How far the chosen airport's forecast
  passengers could fall short before another posting would move more" read as the last whole per cent still ahead (12
  on that build) or the first behind (13, the golden). Everything else reproduced from target/ alone: the eight summer
  figures, the 24 measures, and the stand-down, the same on every posted day at every host, which the judge accepted
  as forced. Gate G: decomposition (counterfactual capacity baseline), analytical, no surface read, no sole data
  defect. Gate H: domain pass, layers pass, decisive step analytical. Repair: the prompt asks the smallest whole per
  cent shortfall at which another posting would move more; SF8 corrected and asserted.
- Repairs in the same pass: the leak reader's realism tells (design days with an off-peak shape and rough noise; the
  2027 roster pattern from the airports' new rostering tool, one column per checkpoint; the deployment policy's
  running of a posting) and its Q5 reading, ruled the easy method on the same estimand (determinism-check 2.3, the
  standard's 3.1 and every posted day refuting the roster pattern plus three), with the extract notes' "ran every
  day" reworded. The design days' redraw moved every figure; every gate re-ran.

- Pass 2 (2026-10-12): DETERMINISTIC, APPROVE. All eight summer figures, the 14 per cent flip (Halloran Bay 244,431
  at 13 against Cullinvale's 237,703, 224,159 at 14, under every rounding of the scaled arrivals) and the 24 measures
  reproduced from target/ alone; the figures hold under a flat two-lane or by-interval stand-down. Gate G: net against
  gross capacity estimated from the 2026 postings, analytical, no surface read, no sole defect. Gate H: domain,
  layers pass, decisive step analytical. Its optional pins (the staff-lane exclusion, claims assigned whole to their
  posting) are declined: each would state an ask's device, and the judge found both readings forced by the pack (the
  operators' returns, the policy's staff and aircrew search, the Sunday travel lines). Its note that Halloran Bay's
  bank-window stand-down rests on one posting week stands as filed: every posted day at every host shows its pattern.

- Pass 3 (2026-10-14, the hardening): NOT_DETERMINISTIC, SEND_BACK. Every figure reproduced from the bundle alone
  (the eight summer figures, the call, the runner-up, the 13 per cent flip under integer and fractional arrivals, and
  the 24 measures), and hygiene passed. The findings are on the architecture, not the build:
  - **Gate C, the main call.** Nothing in the pack says the 2026 bank-lane closures or the posted-day stand-down carry
    into summer 2027, and the only filed 2027 lane source is `roster_pattern_summer2027.xlsx`, which the extract notes
    call the lanes planned for the checkpoint's own officers. Four forward readings are each defensible: the pattern
    on both arms (Cullinvale 697,500), the checkpoint's own lanes on both arms with no stand-down (Cullinvale
    814,900), the pattern against the posted-day lanes (Halloran Bay), and the golden (Eskerford 342,200). The golden
    fits every 2026 record and clause 3.1, but the persistence into 2027 is inferred, not filed.
  - **Gate G.** `surface_read_rejection` with `surface_read_dependency`: the difficulty is that an official artifact,
    the roster pattern, is not what happens, and the answer comes from refusing it. The v3 judge bans that scaffold
    at any depth, which is the same objection against the first architecture's single layer as against this
    hardening's second.
  - **Gate H.** Domain pass (borderline), layers pass, decisive step read as planted: the closures and the stand-down
    are unstated regularities in the lane feed.
  - Secondary forks it names: counting the two staff and aircrew lanes as open lanes (Eskerford 336,300, Ardcarrig
    236,900) and the two CC-4109 claims dated outside every posting week.
  - **Disposition taken:** the architecture is spent (`build-pipeline`, Re-root and retirement: a judge SEND_BACK).
    Filing the persistence or the lane source in the pack would make the decisive step rule application, which is the
    repair `/fix-determinism` forbids, so the build is not shipped and the number waits on a re-root at stage 1.
- Isolated reader (2026-10-14): nothing quoted for question 1, no file ranks the airports on the question, nothing
  reads as the answer. Its question 5 reading executes clause 6.1 with the roster pattern on both arms and lands on
  the default, and its question 6 names rule application, which is the judge's Gate C and Gate H finding read from
  the other side. Realism findings taken: the 2026 queue-time means sat within 0.12 minute of each other at six of
  the eight airports (the sensor is still to be retuned), the feedback file carried ten distinct comments (now
  twenty-six, with the line about half the lanes being open cut as a signpost), and the lane faults ran up to three
  and a half hours (now two).


## Pre-ship check

- Call: post the unit to Eskerford, 342,200 passengers moved within the standard against Halloran Bay's 272,600;
  13 per cent is the smallest whole per cent shortfall in Eskerford's forecast at which another posting moves more.
- Default path: the roster pattern plus three on both arms, Cullinvale at 697,500, Eskerford fourth; the whole
  posted-day gap averaged names Halloran Bay; that gap by interval against the pattern names Halloran Bay at a
  different figure; last summer's realised effect names Cullinvale.
- Gates: 11,719 checks, independent verifier from target/ alone (both arms rebuilt from the lane feed, the two roster
  patterns and the planning sheet), two byte-identical builds, figures_check 51 figures, precut 49 of 49 with one
  WARN answered, scrub clean (target and golden), leak.py REVIEW (no LEAK).
- `guard.py heart` reads BLOCK on `ban.pattern` and `ban.role` against task140, a build drawn after task184 shipped;
  neither axis moved in this hardening and the driver's nearest neighbour on file is 0.07 (task114). `guard.py
  surface` promotes task184 against task185 at 0.100 (99th percentile of consecutive builds) on surface tokens alone;
  the two worlds share no domain, no spine and no deliverable, and the adjudicated read is the author's call.
- Deliverables: mobile_team_posting_summer_2027.pdf (two pages, chart and two tables),
  mobile_team_effect_2027.xlsx (posting effect, summer 2026, notes); target.zip from the final rebuild, 17 files.
- The 10/10 rules re-read against the built pack: the decisive step is still the counterfactual arm, an analytical
  choice; the mess is still Layer 1 only (no shipped figure is wrong, nothing is planted to be caught, and the
  unopened lanes are the checkpoints' own record, not a defect); the asks' devices sit outside the call's rows.

## Tried and rejected

- The seed's idle lane positions as the decisive limit (2026-10-12, at the draw): a per-airport cap that removes the
  natural pick and re-places it, strategies.md F3's dead form (58 v3 and v4).
- Lane capacity observed only while a queue stands, so passengers per lane-hour measures demand at quiet airports
  (2026-10-12, at the draw): task127's driver (a team's capacity visible only as the ceiling it held through a surge).
- Transfer passengers who never reach the landside checkpoint, so departing seats overstate the hub's summer demand
  (2026-10-12, at the draw): the share of a flight's passengers who pass the checkpoint is one ratio per route, and a
  bottom-up build calibrated to last summer's checkpoint counts at airport level already lands close to the call, so
  the decisive step is one enumerable correction.
- The release at only Cullinvale, Ardcarrig and Faranloe, four hosts releasing nothing (2026-10-12, at build): the
  default path kept 15 of the 24 airport-period figures and the averaged path 21, so a response off the call banked
  most of the airport figures; every host but Halloran Bay now stands down two lanes all day.
- Dromkeel as last summer's realised-effect leader (2026-10-12, at build): on the simulated 2026 feed Cullinvale's
  deep queues give it the largest realised effect (1.48 times Eskerford) under every demand Dromkeel's checkpoint
  clears by close; the lateral rung lands on rung 0's answer and the ladder runs three rungs.
- Asking for each airport's figure by period (2026-10-12, at build): 24 construction figures the cracker holds put the
  pair near 44; the prompt asks each airport's summer figure.
- Sinusoidal design days with flat banks (2026-10-12, stage 4): the leak reader read them as synthetic-smooth and the
  same shape at every airport; the design days now carry a late-morning wave, an afternoon lull, a thinning last hour,
  cresting banks and rough 15-minute noise.
- "How far the chosen airport's forecast passengers could fall short before another posting would move more"
  (2026-10-12, judge pass 1): read as the last whole per cent still ahead or the first behind; the prompt asks the
  smallest whole per cent shortfall at which another posting would move more.
- Taking the stand-down as the whole decisive step (2026-10-14, the hardening): the first architecture's single layer,
  shipped 10-12. The portal left it off the approved list, so the posted-day gap against the roster pattern is now
  rung 2 and the decisive step is the counterfactual arm: both sides of the comparison read from the lanes each
  checkpoint actually opens. Every figure moved; the call moved from Halloran Bay to Eskerford.
- The host stand-down measured against matched non-posted weeks, with the crowd-out as the difference (2026-10-14, at
  the hardening): the quiet-hour closures a matched-week design nets out never breach the standard, so the correction
  was worth nothing on the graded quantity (stumping Part 3, a rung measured on the graded figure). The same
  comparison against the checkpoint's own days moves the baseline arm, where it is worth 23 to 40 per cent of every
  airport's figure.
- A chronic shortfall across the whole rostered peak window (2026-10-14, at the hardening): two lanes short through
  Eskerford's plateau put its 2027 design-day waits over 95 minutes and left 58 of 78 simulated 2026 days with a
  queue at close, which no national agency would run a summer on. The shortfall now sits on the pattern's shoulders,
  which keeps the 2026 sensor's 99th percentile at 50 minutes.
- A shallow-breach world (the banks just above the pattern's capacity) to make the shortfall cheap in queue time
  (2026-10-14, at the hardening): with the plan barely breaching, the unit's three lanes fully relieve every
  checkpoint, so the stand-down stops biting and rung 2 collapses onto rung 0's answer; the ladder needs the banks
  deep enough for a two-lane stand-down to leave a residual.
- The whole hardening: the counterfactual arm read from the checkpoint's own days against its filed roster pattern
  (2026-10-14, judge pass 3): built, green on every free gate and 1.26 times clear on the call, and sent back on the
  architecture. The forward lanes are not filed, so both arms rest on an inference from last summer, and the
  difficulty is the refusal of an official artifact, which Gate G bans at any depth. The repair that would close the
  fork (filing the persistence, or naming the lane sensor record as the basis) is the one `/fix-determinism` forbids,
  because it turns the decisive step into rule application. The number re-roots at stage 1: the next draw needs a
  Layer 2 family that does not turn on a plan the records contradict.
