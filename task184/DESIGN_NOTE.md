# task184 design note (architecture 1)

New build in oviya13ya's Anomaly Detection lane (wave 2), from seed AD07. The seed's world, decision and quantity are
kept: a national screening agency posts its one mobile screening team to one of eight airports its throughput detector
flagged this spring, judged by the passengers the team moves through screening within the 20-minute standard. The
seed's pitfall (the team opens lanes only where a lane position stands idle) is a per-airport cap that re-places the
pick, the dead form of strategies.md F3 (58 v3 and v4), and its pick-one shape 01 is banned for this slot; the pitfall
is re-found from the data.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task184.json` (v1), registered 2026-10-12. `guard.py check`: WARN
  overuse.org_family only (government_agency in 24 builds): a national screening agency is the organisation that owns
  this decision in every country that has one, and the axis is not banned. A first card (shape 07, forum
  executive_team, question form which) was blocked against task180 and task136; the shape is 13 and the question form
  where.
- **Pairing:** Supply Chain & Logistics (house domain; client domain Urban & Regional Science), aviation passenger
  screening operations, objective Anomaly Detection & Diagnostics. Supply chain by anomaly detection is built once
  before (task54, a different world). The anomaly is each flagged airport's spring queue breach; the diagnosis is which
  breach the mobile team can actually relieve, separating the team's real added capacity from the artifact of its own
  lanes' throughput.
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
- **Strategy and gate:** `causal_design` (interference: the host's response to the posting), gate G
  `decomposition_attribution` (the team's added capacity net of the host's release), gap objective then time,
  generators G1 then G3, pattern none, layer 2 `estimand_identification`
  (own:host-release-crowd-out-of-a-posted-team), calibration `pilot_log` (last summer's postings).
- **Data-native sentence:** a duty manager handed three extra lanes for a week sends officers to the recurrent training
  the summer otherwise leaves no room for, and the lane sensors count each lane's own passengers, so the mobile team's
  lanes show their full throughput while the host's own lanes go dark, all day at some airports and only in the quiet
  hours at others.
- **Same-puzzle test:** no build in the last twelve shares gap objective, pattern G1 and decision pick_one_of_n; nearest
  drivers 0.06 (task128 v2, task89 v9, task67 v1), none with a host withdrawing its own resource when a shared one
  arrives. task51 (additionality over a baseline a standing rule moves) and task88 (an added booking displacing
  full-rate demand) are the nearest structures and neither has the host's response.
- **Sources (one line each):** strategies.md F9 (interference between units sharing a pool; here the pool is the host's
  own officers, released while the team is there); measured-drivers.md Part 2 (a dimension that lives on another
  entity: the host's lanes, not the team's, carry the effect; and a conjunction, the release and its timing, where the
  day-averaged fix lands on a third airport).

## Default path

1. Read the planning standard (KAS-STD-07, 2026): the expected wait in each 15 minutes from the queue at the start and
   half the arrivals over the open lanes' rate; a change is judged by the passengers it moves within the standard
   on the design days, times the days in each period.
2. Take each airport's 2027 design days (late June, July, August) from the planning sheet and its summer 2027 roster
   pattern of lanes by interval.
3. Add the unit's three lanes from 05:00 to 21:00 to the roster pattern at each airport in turn.
4. Run the standard with and without the unit on each design day, multiply by the days in each period and add up.
5. Post the unit where it moves the most passengers.

Ends on: Cullinvale, 730,800 passengers moved within the standard, 1.28 times Ardcarrig (569,700); Halloran Bay fifth (382,700).
Golden: Halloran Bay, 382,700, 1.61 times Cullinvale (237,700), every other host having stood down two of its own lanes for the whole of the unit's day while the unit was there last summer.

## Stump sentence

A competent solver runs the planning standard on each airport's 2027 design days and summer roster pattern with the
unit's three lanes added and posts the unit to Cullinvale, where it moves 730,800 passengers within the standard; the
step that lands it there is taking the roster pattern plus three as the lanes that will be open, when every posted day
last summer shows the host's duty managers standing down two of their own lanes for the whole of the unit's day at
seven of the eight airports, and Halloran Bay standing down none through its banks, so the unit adds one lane at the
banks everywhere but Halloran Bay, where it adds three and moves the most passengers, 382,700.

## Three rules

- **Domain test:** the decisive analysis is checkpoint capacity planning: a fluid queue on 15-minute arrivals against
  the lanes actually open, scored against the 20-minute wait standard, with the lanes a posting adds read net of the
  host's own response from the lane sensors and roster patterns of past postings; with another field's nouns there is
  no lane, wait standard, queue ahead or host roster, and the task stops making sense.
- **Analyst test:** a strong analyst who reads the planning standard, the 2027 design days, the roster patterns and the
  postings file correctly adds the unit's three lanes to each airport's roster pattern, runs the standard and posts
  the unit to Cullinvale; wrong, because the hosts' own lanes open while the unit screened fell short of their
  pattern last summer, two lanes all day at seven airports and none through Halloran Bay's banks.
- **Layer 1:** a lane sensor feed at 15-minute grain carrying the unit's positions and two staff and aircrew lanes per
  checkpoint under ordinary lane ids; a queue-camera feed with gaps; lane faults on the unit's off days; a superseded
  2023 edition of the standard beside the 2026 one; hotel invoices whose every line repeats the stay's
  officer-nights, with a credit note; a claims export assembled from monthly batches, the August batch appended
  twice; travel claimed on the Sunday before a posting week. Each is what these systems produce, and none decides
  the call (the asks' devices sit outside the call's rows, asserted).
- **Layer 2:** the shortcut is to treat the posted resource's own lanes as the gain; the expert reads what the host
  does while the resource is there from past postings, interval by interval against the host's roster pattern, and
  scores the posting on the lanes that will actually be open.

## Readability screen

Each rung is the move a solver makes to leave the rung below; the decisive rung has to be silent on all six tests.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| lateral, last summer's realised effect per posted week (lands on Cullinvale, rung 0's answer) | no | yes, the postings file names the weeks | yes, a forecaster's first evidence | no | no | no | readable |
| 1, the stand-down averaged over the unit's day | no | no | no, but natural once the stand-down is seen | no | no | yes, one mean subtracted | readable |
| 2, the stand-down by interval (decisive) | no: no document names a stand-down, a release, training or the host's lanes with the unit there; the policy states the unit's lanes and hours only (asserted by word sweep) | no: no column marks a lane stood down; it shows only as a host's own lanes open below its roster pattern on its posted days, a cut across three files (lane sensor feed, 2026 roster pattern, postings file) | no: adding three lanes, carrying last summer's effect, trending demand and averaging the stand-down all land elsewhere | no: no shipped figure scores a posting; last summer's effects are not filed | no: keys unique, every join matched | no: the stand-down enters the queue run interval by interval | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | passengers moved within the standard | those outside the standard without the posting less those outside it with it, on the design days, times the days | passengers screened on the unit's lanes | not a reading: the standard defines the measure | KAS-STD-07 6.1 (asserted present) |
| SF2 | the lanes open with the unit posted | the host's roster pattern less what it stood down on every posted day last summer, by interval, plus the unit's three | the roster pattern plus three | the default's ending, not a reading | the standard computes on lanes open; every posted day at every host shows the same stand-down, Ardcarrig's two weeks running included, and the 2026 and 2027 roster patterns plan the same lanes, so taking the stand-down as lanes off the pattern or as the lanes left open reads the same (asserted) |
| SF3 | the design day | the planning sheet's design day for each period | none shipped | same call | the planning sheet is the only design-day source in the pack |
| SF4 | the periods | 15 to 30 June, July, August 2027 | whole June | same call | the prompt's dates; the planning sheet's periods |
| SF5 | the unit's hours | three lanes, 05:00 to 21:00, every day | weekdays only | same call | the deployment policy |
| SF6 | the 20-minute standard | over 20 minutes is outside; 20 or less within | 20 or more outside | same call | KAS-STD-07 2.2; no wait within 0.3 minute of 20 on the golden's runs nor 0.1 on the ladder's (asserted) |
| SF7 | the stand-down's size | whole lanes, the same every posted day | a fractional mean | same call | KAS-STD-07 3.1 (lanes counted whole); the differences are whole on every posted day with no faults on them (asserted) |
| SF8 | the flip | the smallest whole per cent uniform shortfall in the chosen airport's design-day arrivals at which another posting moves more | the last whole per cent still ahead (one less); scaled arrivals rounded or floored | same call, 14 | the prompt asks the smallest whole per cent shortfall at which another posting would move more (asserted present); rounding the scaled arrivals or not gives 14 (asserted); Halloran Bay 2.5 per cent ahead at 13 and 5.7 per cent behind at 14 |
| SF9 | rounding | each summer figure from unrounded counts, to the nearest hundred | the sum of rounded periods | same call | the two agree at every airport (asserted); no figure within 2 of a rounding edge |

## Ladder

Built values. Passengers moved within the standard over the posting, by airport.

| Rung | Construction | Names | Note |
|---|---|---|---|
| 0, default | 2027 design days, roster pattern plus three | Cullinvale 730,800 | 1.28 times Ardcarrig; Halloran Bay fifth, 382,700 |
| lateral | last summer's realised effect per posted week | Cullinvale 33,300 a week | 1.48 times Eskerford; Halloran Bay last |
| 1 | 2027 design days, the stand-down averaged over the unit's day | Eskerford 159,000 | 1.30 times Halloran Bay (122,000), whose stand-down averages to a little over two lanes |
| 2, golden | 2027 design days, the stand-down by interval | Halloran Bay 382,700 | 1.61 times Cullinvale (237,700), which is 1.22 times Eskerford |

- **Variants (asserted):** the stand-down averaged by shift or over 04:00 to 22:00 names Eskerford; Cullinvale's two
  lanes applied at every host names Cullinvale; the stand-down averaged within each hour gives the golden exactly;
  the after-bank windows never move a figure (the all-day part alone gives the golden). The superseded 2023 basis
  moves the figures but not the call.
- **Position:** Halloran Bay fifth on rung 0, second on rung 1 (by 1.30), first only on the golden.
- **Dominance:** the stand-down swings Cullinvale's figure 3.07 times against Halloran Bay's, against Cullinvale's
  carried gross lead of 1.91 (asserted at 1.2 times).
- **Grid:** basis (2027 design days, last summer's effect) by stand-down (none, averaged, by interval): Cullinvale,
  Eskerford, Halloran Bay on the design days; Cullinvale on last summer's effect. Only the design days with the
  stand-down by interval name Halloran Bay.
- **Worth:** the stand-down moves the figure at every airport but Halloran Bay; rung 0 matches the golden on one of
  the eight summer figures (Halloran Bay's), rung 1 on none, so a response off the call keeps almost no airport
  figure.
- **Flip:** 14 per cent, the smallest whole per cent shortfall at which Cullinvale's posting moves more; at 13 Halloran
  Bay leads by 2.5 per cent, at 14 trails by 5.7 per cent.

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
| 8 | Window length | every posted day last summer for the stand-down | the same on every posted day (asserted) |
| 9 | Boundary inclusivity | over 20 minutes is outside | SF6 |
| 10 | Rounding path | nearest hundred from unrounded counts | SF9 |
| 11 | Tie-break | none | margins asserted |
| 12 | Maturity and censoring | the 2026 records complete | every day's queue clears by close (asserted in the simulation) |
| 13 | Order of operations | lanes, then the queue run, then the difference | the standard |
| 14 | Row order | none | the queue runs in interval order, filed |
| 15 | Duplicate resolution | the lane feed has one row per lane and interval | asserted |
| 16 | Identity normalisation | operations codes across the operations files; purchase orders to postings for hotels | the extract notes' code list; the postings file |
| 17 | Netting | the stand-down nets against the unit's lanes | SF2 |
| 18 | Dimensional units | passengers, minutes, lanes, euros | the standard and the extract notes |
| 19 | Code semantics | lane ids, claim categories | extract notes; never the stump |
| 20 | Integerisation | lanes whole | SF7 |
| 21 | Clause scope | the posting from 15 June to 31 August 2027 at one airport | the policy |
| 22 | Forward window contents | 2027 design days, roster patterns, the unit's hours and the hosts' response | filed sheets; the response from every posted day of 2026 |

## Literal reader

Executing the prompt, the deployment policy and the planning standard word for word: the unit goes where it will move
the most passengers within the 20-minute standard over the posting; the standard counts a passenger arriving in an
interval as outside it when the queue at the interval's start and half its arrivals, over the open lanes' rate, take
more than 20 minutes; a change's passengers moved are those outside the standard on the lanes open without it less
those outside it on the lanes open with it, times the days. So each airport's figure is its 2027 design days run on
the lanes that will be open with the unit there. Last summer's postings are the only record of what a host opens
while the unit screens, and every posted day at every host shows the same lanes stood down. Every reading in SF1 to
SF9 returns Halloran Bay; the default comes from the same estimand by taking the roster pattern as the host's lanes.

## Oracles

- The detector's spring flags: the eight airports flagged, the weeks and breach counts; a different question, and
  its order matches no rung.
- The 2026 lane feed on the unit's off days: the hosts open their roster pattern less logged faults; it confirms the
  pattern on every basis and scores no posting.
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

**The cracker sheet.** The cracker landed Halloran Bay, ran the hygiene battery (keys unique, no exact duplicates,
every join matched) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, passengers 2026 (8) | every lane's counts summed by airport | staff and aircrew lanes counted as passengers | miss |
| Ask 2, hotel per officer-night (8) | invoice amounts over nights summed by line | nights repeat on every line | miss |
| Ask 3, claims per week (8) | export rows summed by airport over its posting weeks, each by its date | the August batch twice; travel dated the Sunday before | miss |
| Chart (rec block, not an ask) | carried by the main call | scored with the recommendation | outside |

The mirror sheet (stopped at Cullinvale) differs from the cracker sheet only on the recommendation criteria, the
chart and seven of the eight airport figures (it holds Halloran Bay's).

Mirror leakage: 6 per cent of the ask weight (Halloran Bay's summer figure and method credit, no measure).

**Pair arithmetic.** Planning weights 38 recommendation, 7 instruction following, 55 asks over 32 figures (8 airport
figures, the construction layer the cracker holds, and 24 measures). With r = 5: C = 38 + 7 + 55 x 8/32 = 58.8 for
the cracker; S = 5 + 7 + 55 x 0.06 = 15.3 for the mirror.

Pair ceiling: 37.0

## Build record

- Generator: world, models, profiles (2027 design days with a late-morning wave, an afternoon lull, a thinning last
  hour, cresting banks and rough 15-minute noise, the draw per airport and period chosen to keep every
  golden wait 0.3 minute off 20, every figure off a whole thousand and a half-hundred tie, every summer figure equal to
  its rounded periods), sim (the
  2026 summer: daily demand, faults on the unit's off days, the hosts' stand-down on posted days, the queue, lane
  counts and the camera feed), records, docs, analysis, asks, deliver, checks, verify (pandas, the shipped files
  only), metadata, build.
- Built values: rung 0 Cullinvale 730,800 (1.28); rung 1 Eskerford 159,000 (1.30 over Halloran Bay); golden Halloran
  Bay 382,700 (1.61 over Cullinvale 237,700); last summer's realised effect Cullinvale (1.48); flip 14 per cent.
- Ask goldens: passengers 2026 from 616,007 (Halloran Bay) to 1,299,095 (Cullinvale); hotel 84.70 to 116.72 per
  officer-night; claims 7,135.92 to 8,824.96 per posting week; every stop outside its bin at every airport.

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

## Pre-ship check

- Call: post the unit to Halloran Bay, 382,700 passengers moved within the standard against Cullinvale's 237,700;
  14 per cent is the smallest whole per cent shortfall in Halloran Bay's forecast at which another posting moves more.
- Default path: the roster pattern plus three, Cullinvale at 730,800, Halloran Bay fifth; the day-averaged stand-down
  names Eskerford; last summer's realised effect names Cullinvale.
- Gates: 11,632 checks, independent verifier from target/ alone, two byte-identical builds, figures_check 50 figures,
  precut 38 of 38, scrub clean (target and golden), leak.py REVIEW (no LEAK), guard surface 0 promoted, heart WARN
  (government_agency overuse only).
- Deliverables: mobile_team_posting_summer_2027.pdf (two pages, chart and two tables),
  mobile_team_effect_2027.xlsx (posting effect, summer 2026, notes); target.zip from the final rebuild, 17 files.
- Judge: pass 1 FIX_NOW on the flip's convention only (fixed by the prompt's pin); pass 2 below.
- Card current: forum redrawn to operations_desk, driver, stump, answer, spine rows 279,417, layer 1 as built.

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
