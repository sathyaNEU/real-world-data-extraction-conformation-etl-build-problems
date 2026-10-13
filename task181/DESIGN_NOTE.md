# task181 design note

Architecture 4. Seed AD04 (Anomaly Detection & Diagnostics, a pump's zone-D vibration split by operating point) is
idea material only: its insight is task180 v2's (a monitored signal carried in from ordinary operation), and its world
has no client task type that serves this objective. Three architectures are spent (`## Tried and rejected`); the
author's builds are never retired, so the objective and the number are kept and the draw is new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task181.json`, architecture v4, registered 2026-10-12 after `guard.py
  check` (WARN only: `three_rules.strategy_risk` and `repeat.gate_g`, both answered below; the older same-puzzle and
  same-driver matches, task229 v1, task98 v3 and task60 v8, differentiated on the card).
- **Pairing:** Human Factors & Ergonomics, task type safety-incident-error-analysis, objective Anomaly Detection &
  Diagnostics (a pairing never built). The anomaly is a sector whose losses of separation will run over the safety
  plan's tolerance in summer 2027; the diagnosis is what generates a sector's losses. Shape 01 (each sector's forecast
  against the tolerance line, in or out). Decision `designation_set` (the sectors over the tolerance, possibly none),
  question form `whether`.
- **World:** Aldmark (a fictional northern European state), its national air navigation service provider Aldmark Air
  Navigation and the Holmvik Area Control Centre, eight elementary en-route sectors from FL245 up (Tarvik, Mosby,
  Grendal, Linmark, Karrow, Lysvik, Hallin, Sandvik; codes TRV, MSB, GRD, LNM, KRW, LYS, HAL, SDV) over a hub (Holmvik)
  and two regional airports (Brekka, Skarnes). An east-west trunk airway crosses Grendal, Tarvik and Lysvik at FL330 to
  FL400; Brekka, under the west of Tarvik, gets a low-cost carrier's new base for the summer 2027 schedule, whose
  eastbound departures climb and arrivals descend through Tarvik.
- **As of:** extracts pulled 12 October 2026 (actuals 1 January 2025 to 30 September 2026); the summer 2027 traffic
  sample issued 9 October 2026; the unit safety review board approves the summer 2027 sector plan on 4 November 2026.
  `leak.py --asof 2026-10-12`.
- **Mechanism:** gap population (what one unit of exposure is: a pair of aircraft, one crossing the other's level),
  then time (the forward window holds traffic the closed window never had); pattern D (two flawless grains, the
  flight-hour grain of the extract and the crossing grain of the losses, no key bridging them); generators G2 (decisive)
  and G13. Gate G `forecasting`. Strategy `grain_or_unit`.
- **Furniture:** forum `committee_or_panel` (the unit safety review board), forcing event `season_or_peak` (summer 2027),
  organisation family `utility_or_infrastructure`, role family `capacity_planner`, context artifact `close_out_summary`
  (the summer 2026 safety performance close-out), opening `question-first`. Personas drawn with `guard.py names --geo
  Denmark --seed 181` (Dorte Koch, Erik Sørensen, Paw Frandsen, Kenny Lassen); the prompt carries none of them.
- **WARNs answered.** `three_rules.strategy_risk` (grain_or_unit): nothing here turns on reading a field; every field is
  read the same on both paths, and the analyst test below names the easy route that still fails once every field and
  rule is read correctly. `repeat.gate_g` (forecasting against task501 v3): forecasting is the honest label, because
  the call is a bet on summer 2027 losses that no closed figure states; task501's mechanism (a buffer read off horizon
  totals instead of a cumulative path) shares nothing with this one.
- **Data-native sentence:** separation in this centre is lost almost only where one aircraft climbs or descends
  through the level of another in the same sector (level traffic on the airways is spaced in trail by the flow
  measures), so a sector's losses follow the vertical crossings its traffic creates, and the summer 2027 schedules send
  the new Brekka base's departures and arrivals climbing and descending through Tarvik's busy trunk-airway cruise
  levels while adding few flight hours.
- **Sources read, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: the three rules and the two layers; the mess goes on the ask
    paths and the stump into the forecast's exposure.
  - `layer2-rigor-patterns.md` has no human-factors patterns; the five families in the client's standard place this
    under the field's own method (`field_method`): the field's exposure for a separation loss is the interaction, not
    the hour flown.
  - `stumping/references/strategies.md` Parts 1, 4 and 6: the dead shapes avoided are the default construction as
    golden, a quantity named by a sentence or a column, a reflex (pool, square the traffic, stratify by phase, trend),
    a dated cause stepping a series, and a linear mechanism in a rate-times-exposure world.
  - `stumping/references/client/measured-drivers.md`: the held group's lesson taken is the compound construction a
    solver does not build (here an exposure made by pairing rows of one extract in time and level); none of their
    withheld-method pins is used.
  - Architecture 3's rejected draws (squared load, overlapping panels, competing exits, funnel limits, fabricated
    interviews as inliers, warranty curves, the seed's zone-D split): none is reused.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain:

1. Read the safety plan's tolerance: a sector's forecast rate of ATM-related losses of separation for the summer season
   (1 June to 31 August, local time) may not exceed 40.0 per 100,000 flight hours.
2. Load the occurrence export, keep the losses of separation with an ATM contribution and count them by elementary
   sector and summer; sum each sector's flight hours in the flight data extract (entry to exit of every traversal) and
   compute each sector's summer 2026 rate, which ties to the summer 2026 close-out.
3. Sum each sector's flight hours in the summer 2027 planning traffic, scale each sector's summer 2026 losses by its
   growth in flight hours (the rate held at 2026's), and compare each forecast rate with 40.0.
4. No sector reaches 40.0 (Mosby highest at 32.0, Tarvik 13.4); file that summer 2027 stays inside the tolerance.

Ends on: no sector over the tolerance
Golden: Tarvik

## Stump sentence

A competent solver keeps each sector's summer 2026 losses of separation per 100,000 flight hours, scales each sector's
losses with its 2027 flight hours from the planning traffic and files no sector over the tolerance (Mosby highest at
32.0 against 40.0, Tarvik 13.4), and the step that lands it there is forecasting losses from flight hours when
separation is lost where one aircraft climbs or descends through another's level: the new Brekka departures and
arrivals add about 10 per cent to Tarvik's flight hours but multiply its pairs whose levels change order five-fold
(9,682 to 48,545), which takes Tarvik to 72.4 losses per 100,000 flight hours while every other sector stays at or
under 26.4.

## Three rules

- **Litmus:** no reported number is wrong and nothing overturns one. The flight data, the occurrence export, the
  close-out and the traffic sample are all correct; the difficulty is building a summer 2027 count no file states.
- Domain test: what decides the call is the field's own traffic-complexity measure, the count of aircraft pairs whose
  levels change order inside a sector. A loss of separation happens in a vertical interaction, an aircraft cleared
  through the level of another, so a sector's expected losses follow its vertical crossings rather than its flight
  hours, and air traffic safety analysis keeps that complexity count beside the hours for exactly this reason. Nothing
  here measures controller workload; the quantity is the traffic's own geometry. With another field's nouns there are
  no flight levels to cross and no climb through a cruising flow, so the task does not survive the swap.
- Analyst test: a strong analyst who keeps the ATM-related losses of separation, attributes each to its elementary
  sector, reads the season in local time and computes summer flight hours exactly still forecasts
  summer 2027 by scaling each sector's losses with its flight hours, with the square of its traffic or with its
  climbing and descending flight hours, and files that no sector exceeds 40.0, because only counting the vertical
  crossings in each sector shows the new Brekka departures taking Tarvik over the tolerance.
- Layer 1: realistic mess from the centre's own systems: the flight data extract at flight x elementary sector grain
  with levels in hundreds of feet and times in UTC against a season defined in local time; sectors named in full in the
  occurrence export and by code in the flight data; the summer 2027 planning traffic built by the forecast team in its
  own layout and flight key; and, on the ask paths, a delay export that keeps a re-filed flight's cancelled plan, a
  configuration table revised mid-season, and both crews' reports of one ACAS encounter filed as two occurrences.
- Layer 2: a sector's forward losses are not its flight hours times its past rate, nor a function of its traffic count
  or of the time its traffic spends climbing: separation is lost between two aircraft where one changes level through
  the other's, so the forecast has to carry the vertical crossings each sector's traffic creates, and the record proves
  it (losses per crossing hold steady across sectors and months while losses per flight hour vary several-fold).
- **Stump class:** analytical. Rule 3 is cleared: no planted defect or decoy decides it, no field reading flips it (every
  field is read the same on both paths) and no stated rule produces it (the tolerance is filed; nothing in the pack
  says how to forecast the losses).

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the summer 2026 rates as they stand (Mosby highest, no sector over) | the close-out states them | the close-out's table | no | the close-out ties | clean | one ratio | readable |
| R1 the default path: losses scaled with flight hours, the 2026 rate held (none over) | no | flight hours from entry and exit times | the rate-times-exposure habit | the close-out ties | clean | one ratio per sector | readable |
| R2 losses scaled with the square of each sector's hourly traffic, or with pairs of aircraft in the sector at once (none over) | no | traversal times | yes: density squared is the traffic-safety rule of thumb | no | clean | no | readable |
| R2b losses per climbing or descending flight hour, applied to each sector's 2027 vertical flight hours (none over) | no | the occurrence phases show climbing and descending aircraft | yes: stratify on a visible attribute | no | clean | one ratio per phase | readable |
| R2c each sector's 2025 to 2026 rise carried on (Grendal and Hallin over) | no | two closed summers | yes: trend | no | clean | one difference | readable |
| R3 (decisive) losses per vertical crossing, a pair in one sector at once where one aircraft passes through the other's level, applied to the crossings in the summer 2027 planning traffic (Tarvik over) | no sentence names a crossing, a pair or an interaction | no column carries it: it is built by pairing traversal rows of one sector in time and comparing their level profiles, and no marker isolates the Brekka traffic's crossings | not a reflex: the reflexes scale exposure the rows already state (hours, counts, squares, vertical hours) | no control sees a crossing; the close-out publishes rates per flight hour | clean on the wrong path: every key unique, every join matches, the close-out ties | no: a rate estimated on 21 months of pairs and applied to a stock of pairs the 2027 traffic builds | silent |

## Semantic fork table

| Id | Term or convention in the main ask or the main computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "losses of separation" | ATM-related losses (ATM contribution direct or indirect), as the safety plan's tolerance counts them | every loss of separation, pilot-induced ones included | Tarvik only | safety plan cl. 3.4 and 4.1, and same call (asserted: Tarvik 79.9, next 29.1) |
| SF2 | "summer 2027" | 1 June to 31 August 2027, local time | the same dates in UTC | Tarvik only | safety plan cl. 3.2, and same call (asserted) |
| SF3 | "flight hours" | time from sector entry to exit of every traversal in the planning traffic | the same clipped at the season's edges | Tarvik only | safety plan cl. 3.5, and same call (asserted) |
| SF4 | "sector" | the eight elementary sectors | the configured control positions, collapsed at night | Tarvik only | safety plan cl. 3.1 (occurrences and flight hours counted for the elementary sector), and same call |
| SF5 | the window the loss rate is estimated on | the whole record since 1 January 2025 (January 2025 to September 2026) | summers only, or 2026 only | Tarvik only | safety plan cl. 4.2 (the record since the eight-sector structure came into use on 1 January 2025), and same call (asserted: 73.8, 71.5, 71.9) |
| SF6 | the pair | two traversals of one sector overlapping in time whose straight-line level profiles change order | pairs that meet at a level, pairs within 1,000 ft or 2,000 ft with one aircraft changing level, any pair with an aircraft changing level | Tarvik only | the record (every loss is a pair whose levels changed order, 106 of 106), and same call (asserted: 69.6, 67.2, 63.4, 59.4; next at most 29.9) |
| SF7 | the loss rate's pooling | one rate per pair for the centre | each sector's own rate per pair | Tarvik only | same call (asserted: Tarvik 72.5, next 25.6) |
| SF8 | "run over the tolerance" | the forecast rate above 40.0 | at or above 40.0 | Tarvik only | same call (no sector within 6 per cent of 40.0, asserted) |
| SF9 | rounding before the comparison | unrounded rate against 40.0 | the rate rounded to one decimal first | Tarvik only | same call (asserted) |

## Ladder

Built values (generator checks 1 to 34, verifier from the bundle). Rates are ATM-related losses of separation per
100,000 flight hours in the summer season.

| Rung | Construction | Over 40.0 | Tarvik | Highest other |
|---|---|---|---|---|
| R0 | summer 2026 rates as they stand (the close-out) | none | 13.4 | Mosby 32.0 |
| R1, the default path | 2026 rate held, losses scaled with flight hours | none | 13.4 | Mosby 32.0 |
| R1b | the whole record's rate per flight hour, or the two summers' | none | 13.8, 17.0 | Karrow 24.2, Mosby 32.5 |
| R2 | losses scaled with the square of hourly traffic | none | 16.0 | Mosby 32.9 |
| R2b | losses per climbing or descending flight hour, own sector, pooled, or pooled on summer 2026 | none | 25.3, 32.0, 36.6 | Mosby 31.9, 32.1, 36.6 |
| R2c | the 2025 to 2026 change carried on | Grendal, Hallin | 8.7 | Grendal 55.4, Hallin 53.3 |
| R3, decisive | losses per pair whose levels change order, pooled over the record, times each sector's pairs in the planning traffic | Tarvik | 72.4 | Lysvik 26.4 |

- **Kills, one fact each:** R0, R1 and R1b by the record's mechanism (every loss is a pair whose levels changed order;
  losses per flight hour run from 13.8 to 24.2 across the sectors while losses per pair hold, max/min 1.12); R2 by
  the same record (the square of the traffic counts level pairs that carried no loss in 21 months); R2b by the record
  (losses per climbing hour differ with how busy the levels climbed through are); R2c by the close-out and the
  planning traffic (Hallin's rise is the western arrival stream moving onto its descent with AIRAC 2603, flat into
  2027; Grendal's is one more loss on three); R3 stands.
- **Why each rung is satisfying:** R1 is the safety plan's own unit carried forward the way rates always are; R2 and
  R2b are the density and phase-of-flight corrections an analyst reaches for when losses look traffic-driven; R2c is
  the trend reflex.
- **Position rule:** the default path names no sector; Tarvik is last of eight on the summer 2026 rate and first only
  on R3.
- **Where the evidence sits:** the record names both aircraft in every loss; joined to the flight data, every one of
  the 106 losses (96 ATM-related) is a pair in one sector at once whose levels changed order.
- **Discriminator dominance:** the new Brekka flows take Tarvik's pairs from 9,682 in summer 2026 to 48,545 in the
  planning traffic (x5.0) while its flight hours rise from 14,957 to 16,414 (x1.10), against Mosby's default-path lead
  (32.0 against Tarvik's 13.4).
- **Variants asserted on R3:** pairs that meet at a level (Tarvik 69.6), within 1,000 ft (67.2) or 2,000 ft (63.4)
  with one aircraft changing level, any pair with an aircraft changing level (59.4), each sector's own rate (72.5),
  summers-only (73.8), summer 2026 only (71.5) or 2026-only (71.9) estimation, every loss including pilot-induced ones
  (79.9): every variant puts Tarvik over 40.0 by at least 15 per cent and every other sector at or under 29.9.
- **Realised counts:** losses are scheduled by error diffusion on the expected count per sector and local month (moving
  threshold), so every sector's realised summer 2025 and 2026 rate sits at least 6 per cent under 40.0 and the pooled
  rate per pair reproduces on every window (asserted).
- **Per-rung worth on the graded quantity:** the graded quantity is the set of sectors over the tolerance and the
  chart's bars; each rung's set is asserted.

## Closure table

| # | Axis | Reading chosen | Closure move |
|---|---|---|---|
| 1 | Population | the eight elementary sectors; the summer 2027 planning traffic as issued 9 October 2026 | C1: one planning traffic file ships; asserted |
| 2 | Unit of account | one ATM-related loss of separation, one occurrence | C1: occurrence numbers unique, one row per occurrence, asserted |
| 3 | Attribution window | losses dated by occurrence time, local season | C1 (SF2) |
| 4 | As-of dating | data to 30 September 2026, planning traffic of 9 October 2026 | filed in the extract notes; C1 |
| 5 | Version basis | the planning traffic as issued | C1: no later vintage ships |
| 6 | Denominator | flight hours in the summer 2027 planning traffic, entry to exit | filed in the safety plan's own words; C1 (SF3) |
| 7 | Weighting | one rate per pair pooled over the centre | C3: sector rates give the same set (SF7) |
| 8 | Window length | the record since 1 January 2025 for the rate | pinned in safety plan cl. 4.2; C3: summers only or 2026 only, same set (SF5) |
| 9 | Boundary inclusivity | above 40.0 | C1: no sector within 6 per cent (SF8) |
| 10 | Rounding path | the call is a set; ask figures rounded once at the end | pinned in the prompt's closing sentence (SF9) |
| 11 | Tie-break | none needed | C4: Tarvik 72.4 against 40.0, the next 26.4 |
| 12 | Maturity and censoring | occurrences reported within the month; none open at the cut | C1: no occurrence dated after 30 September 2026, asserted |
| 13 | Order of operations | filter ATM-related, then rate, then forecast | C1: the filters commute |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | none on the main path | C1: one row per occurrence and per traversal, asserted |
| 16 | Identity normalisation | traversals keyed by flight plan id; occurrences name both callsigns | C1: every occurrence's two aircraft found in the traversals, asserted |
| 17 | Netting against gross | not applicable | C1 |
| 18 | Dimensional units | flight levels in hundreds of feet, hours from UTC times | C1 |
| 19 | Code and status semantics | ATM contribution codes from the occurrence scheme | pinned by the code list; C1 (SF1) |
| 20 | Integerisation | expected losses are not integers | C1 |
| 21 | Clause scope | the tolerance per elementary sector per summer | filed in the safety plan; C1 (SF4) |
| 22 | Forward window contents | summer 2027 as the planning traffic carries it | C1: one full-season planning traffic file ships |

## Literal reader

Filed estimand, from the prompt and the safety plan: each elementary sector's forecast rate of ATM-related losses of
separation in summer 2027 (1 June to 31 August, local time, cl. 3.2) per 100,000 flight hours of the summer 2027
planning traffic (cl. 3.5), from the occurrence record since 1 January 2025 (cl. 4.2), against the plan's 40.0
(cl. 4.1); the call is the set of sectors over it, or none. Criterion: none filed, because the design forces the
method (determinism-check §1, form 1): the record names both aircraft in every loss, every one a pair in one sector
at once where one aircraft passed through the other's level, and losses per such pair hold across sectors (2.31 to
2.59 per 10,000) while losses per flight hour run from 13.8 to 24.2, so a forecast that ignores the pairs contradicts
the record it is fitted on. Why the careful computation still lands wrong: the careful, obvious computation of the
filed quantity (each sector's 2026 rate carried onto its 2027 flight hours, or scaled with its traffic density or
its climbing and descending hours) files no sector; every literal reading of the prompt's terms puts Tarvik alone
over 40.0 once the forecast carries the pairs (the semantic fork table), and the easy answer comes only from the easy
method on the same estimand.

## Oracles

- The summer 2026 close-out (each sector's ATM-related losses for summers 2025 and 2026, summer 2026 flight hours and
  rate): reproduces the record exactly (asserted), ranks nothing on 2027, and confirms no ask figure.
- The network manager's regulation list carries no delay totals, so nothing ties the slot list as delivered.
- Nothing ties only under the golden, for the call or any ask.

## Ask sheet

The main call's declared row population: the flight data traversals of January 2025 to September 2026, the
occurrence rows of type SMI, and the summer 2027 planning traffic. Every device below lives in the network manager's
slot allocation list, the configuration log and its tables, and the occurrence rows of type ACAS RA, which the main
call never reads as rows; the generator asserts that no device row sits inside the declared population (the 662 plans
that never flew are absent from the flight data; the advisory reports share no occurrence number with the SMI rows).
Each ask is one of the other measures the summer sector plan carries for every sector, on which the call does not
turn (H18 home 1): capacity, staffing and a second safety indicator. No ask is keyed to the call or its construction,
and the three asks share no primary family and no file path.

**Ask 1. En-route ATFM delay per flight in summer 2026, every sector (8 figures, minutes to two decimals).**
- Use: the summer plan reads capacity beside safety, and the board weighs delay against any capacity cut.
- Construction: each flight that flew, at the slot delay of its most penalising regulation (the extract notes' field
  note), charged to that regulation's sector when the regulation is en-route, over the flights that entered the
  sector in the local summer.
- Primary device (D1, plans that never became flights): the slot list keeps the original plan of a flight re-filed
  after its slot was issued (its own plan id, the larger delay; the re-filed plan flew with a smaller delay or none)
  and a few plans of flights cancelled outright after their slot; 662 plans, every one absent from the flight data and
  nothing else marking them. Ids are unique and no row repeats another; a callsign-and-day dedup removes the
  re-filings it can see, keeps the larger cancelled delay, misses the plans whose re-filing escaped every regulation
  and the cancellations, and merges the cargo and charter rotations that fly out and back under one callsign. Only
  the plan ids in the flight data show which plan flew. Every sector's figure moves.
- Texture (executed by the battery): one row per plan per regulation that captured it; a plan's delay is its largest,
  and a flight whose largest is a Holmvik arrival regulation carries no en-route delay (moves three sectors in the
  third decimal only).
- Span (5 files, 11 columns): slot list, regulation list, sector register, flight data, extract notes; `ifplid`,
  `callsign`, `eobt`, `regulation_id`, `slot_delay_min`, `traffic_volume`, `location_type`, `code`, `sector`,
  `entry_time_utc`, `ifplid` (flight data).
- Ladder (asserted): every row summed (Tarvik 0.62, every sector high); largest delay per plan id with the plans that
  never flew (the cracker, Tarvik 0.59, every sector high); callsign-and-day dedup (Tarvik 0.57, at least six sectors
  off); golden (Tarvik 0.53, Mosby 0.41, Grendal 0.43, Linmark 0.16, Karrow 0.29, Lysvik 0.55, Hallin 0.27,
  Sandvik 0.10).

**Ask 2. Hours each sector was open as a sector on its own in summer 2026 (8 figures, hours to one decimal).**
- Use: the summer plan's staffing reads how long each sector needed its own team.
- Construction: the supervisors' configuration log (local time) against the configuration table in force at each
  moment, summing the time each elementary sector had a position to itself.
- Primary device (D2, an attribute at the wrong vintage): the current table file is revision 9, which regrouped three
  day configurations (C6A, C6B, C5) from 06:00 on 14 July 2026; revision 8, in force before, is only in the operations
  manual's Table 3.4-1 (edition of 26 March 2026), and the switch is a remark in the log. Every code in the log matches
  the current file, so the join is clean; every sector's hours move.
- Texture: the log is in local time and labelled so; reading it as UTC moves nothing (night configurations open no
  sector on its own).
- Span (4 files, 7 columns): configuration log, current table, operations manual extract, sector register;
  `log_time_local`, `configuration`, `remarks`, `position`, `sectors`, `table_revision`, `name`.
- Ladder (asserted): current table all season (the cracker, every figure off); the manual's table all season (every
  figure off); golden (Tarvik 1532.1, Mosby 1310.5, Grendal 735.3, Linmark 1202.3, Karrow 771.1, Lysvik 1410.2,
  Hallin 971.6, Sandvik 1301.9).

**Ask 3. Encounters that gave an aircraft an ACAS resolution advisory in summer 2026, every sector (8 whole numbers).**
- Use: the second safety indicator the board reads beside losses of separation.
- Construction: the occurrence rows of type ACAS RA in the local summer, two reports naming the same two aircraft in
  the same sector minutes apart being one encounter.
- Primary device (D1, one event under two reports): when both crews report, the export carries two occurrences (two
  numbers, each crew naming the other aircraft, separations as each crew judged them); single reports are the
  majority. Only pairing reports by the two callsigns and time counts encounters. Every sector's figure moves.
- Hazard H1 (D8): occurrence times are UTC and the season local; an advisory at 22:56 UTC on 31 May 2026 is 1 June
  local (Hallin) and one at 22:14 UTC on 31 August is 1 September local (Lysvik): the UTC season moves two sectors.
- Span (3 files, 8 columns): occurrence export, occurrence scheme codes, sector register; `occurrence_no`,
  `occurrence_type`, `occurrence_date`, `time_utc`, `sector`, `ac1_callsign`, `ac2_callsign`, `reported_by`.
- Ladder (asserted): report rows counted (the cracker, every figure high); UTC season (two sectors off); golden
  (Tarvik 8, Mosby 9, Grendal 10, Linmark 7, Karrow 4, Lysvik 7, Hallin 3, Sandvik 2).

**The cracker sheet.** The cracker landed Tarvik, ran the hygiene battery (keys unique, no exact duplicates, every
join matched, no fan-out beyond the regulation ids reused across months, the close-out tied) and executed every
filed rule (the most penalising regulation, the local season, the configuration codes):

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, delay per flight (8) | largest delay per plan id, charged to the regulation's sector, over the flights in the sector | the 662 plans that never flew are counted, every sector 6 to 20 per cent high | miss |
| Ask 2, hours open alone (8) | configuration log against the current table, local time | revision 8 applied to 1 June to 14 July for C6A, C6B and C5, every sector | miss |
| Ask 3, advisory encounters (8) | advisory rows counted by sector in the local season | both crews' reports of one encounter counted twice, every sector | miss |
| Chart (rec block, not an ask) | bars of the summer 2027 forecast rate with the 40.0 line | carried by the main call, scored with the recommendation | outside |

The mirror sheet (the same response stopped at no sector) differs from the cracker sheet only on the recommendation
criteria and the chart, so no ask is coupled to the call.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure; the mirror's ask rows are the
cracker's).

**Pair arithmetic.** Planning weights 38 recommendation, 7 instruction following, 55 asks over 24 figures. With r = 5
(the recommendation criteria a wrong call keeps: the ATM-related filter, the flight-hour denominator) and each top
response keeping about 8 per cent of the ask weight: C = 38 + 7 + 4.4 = 49.4 for the cracker, S = 5 + 7 + 4.4 = 16.4
for the mirror.

Pair ceiling: 32.9

## Pins

- In the prompt (the question, never a convention): the eight sectors, ATM-related losses of separation, summer
  2027, the safety plan's tolerance, and each ask's unit, period and rounding.
- Filed at authority in the safety plan (the unit's safety performance plan, the document the board approves the summer
  plan against): the tolerance (40.0 ATM-related losses of separation per 100,000 flight hours per elementary sector
  per summer season, cl. 4.1), the forecast's inputs (the occurrence record since 1 January 2025 and the planning
  traffic, cl. 4.2), the season (1 June to 31 August, local time), ATM-related meaning an ATM contribution direct or
  indirect, flight hours from sector entry to exit.
- The occurrence scheme: occurrence types, ATM contribution codes, severity. The network manager's field note (in the
  extract notes): a flight plan captured by several regulations takes the slot of its most penalising one, and its
  ATFM delay is that regulation's. The extract notes: the as-of dates and each system's clock. The operations manual:
  amendments to Table 3.4-1 take effect at the time stated and are recorded in the log.
- No pin names a crossing, a pair, an interaction, the level of the other aircraft or any forecasting method. The
  readability screen was re-run on every pin.

## Stopping rule

Written before the first portal test. If a top portal response names Tarvik by counting vertical crossings, the
call is at ceiling in this world: the next move is to change the decision, never to harden this mechanism. If the call
holds and the asks score over the bar, the ask-only revision runs with the main call byte-identical. A fork on the
call that convergence cannot close re-roots the decisive step rather than pinning it.

## Pre-ship check

1. Domain: the task is an area control centre's human-factors safety analysis, where its losses of separation will
   come from next summer; the exposure for a loss is the controller's vertical interaction between two aircraft in
   one sector, which the field counts beside flight hours, and another field's nouns break it (no levels to cross).
2. Real work, nothing planted: an FDPS archive at flight x sector grain in UTC, a safety database export with crew
   and controller reports, a planning traffic in the forecast team's own key, a network manager slot list that keeps
   plans as allocated, a supervisors' log in local time beside a configuration table revised mid-season, each from
   the centre's own systems.
3. The flip is a method choice: forecasting each sector's losses from the pairs its traffic builds, never a field read
   or a rule; every rule in the pack (ATM-related, the season, flight hours, the tolerance) is read the same on both
   paths.
4. The analyst test holds: the summer 2026 rate carried forward names no sector (Mosby 32.0 highest), density squared
   and climbing hours name none, the 2025 to 2026 trend names Grendal and Hallin; only the pair count names Tarvik.
5. One defensible method: the prompt and the plan fix the estimand; the record forces the exposure (every loss is a
   pair whose levels changed order, 106 of 106), and every pair definition, window and pooling puts Tarvik alone over;
   the write-up counts pairs strictly (one above the other where the overlap begins, below it where it ends), and the
   judge's second pass (APPROVE) found the touching reading moves Tarvik to about 64 to 70 with the call unchanged.
6. No decoy: the close-out is a correct, labelled history of summer 2026 rates; no memo, draft or voice argues for a
   sector or a method.
7. Nothing hidden and recovered: no certified figure pins the method; the rate per pair is estimated on the record.
8. A new lesson: a forward change that sends new climbing and descending traffic through a busy level band multiplies
   the encounters that produce events while barely adding exposure time, which a rate per hour and its visible
   refinements both hide (`guard.py heart` WARN only, nearest driver task183 at 0.06).

## Leak and duplicate checks

`leak.py --asof 2026-10-12`: REVIEW, no LEAK (the tolerance, the rate basis and the close-out figures the write-up
quotes are listed as `stated_inputs`). Each REVIEW line:
- The close-out and the safety plan carry the call's words: the indicator's own vocabulary (tolerance, ATM-related,
  losses of separation, flight hours, summer) in the documents that define and report it; neither forecasts 2027 or
  names a sector over. Harmless.
- The manual, the close-out and the extract notes carry stump-paragraph words (traffic, control, levels, Tarvik,
  Grendal, Hallin): sector names and ordinary operations vocabulary; none names a pair, a crossing or an
  interaction. Harmless.
- The planning traffic's 2027 dates: it is the summer 2027 season's traffic, issued 9 October 2026. Harmless.
`guard.py heart`: WARN (the strategy-risk and Gate G repeat WARNs answered in the Draw). `guard.py surface`: promotes
task181 against task183 (surface 0.100) on the lane and the pack idiom, after the goldens moved from a workbook and
a PNG (task183's pair) to a board deck and a measures CSV; the mechanisms share nothing (card differentiation), and
task60 is differentiated on the card.
The reader, twice (before and after the stage 4 repair): nothing for questions 1 to 4 (the close-out's Table 1 is the
labelled summer 2026 standing, not a 2027 ranking); the question 5 sentences (plan 3.1 to 3.5, 4.1 to 4.3, the notes'
grain and clock) execute to the golden's population, window and denominator and leave the model form open. Pass 1's
realism tells fixed in the generator (document genres, the table's export date, out-of-order flight keys, the roster
remarks); pass 2's minor tells harmless.

## Tried and rejected

- Architecture 1 (a credit union's counterfeit wave traced to two skimmed terminals behind a dominant common point):
  spent at in-house round 1, where a solver explained the co-visited sites away as subsets of the dominant source's
  victims and re-screened the residual; any further rung falls to the same subset check or opens a fork.
- Architecture 2 (a public health unit's pertussis line list, the fortnight completed by laboratory route): stumped
  in-house only while the estimand was open; the portal's determinism QC called it a fork, and once the eventual count
  was filed literally a per-laboratory completion landed it (96.8), and any filed criterion choosing the delay history
  names the step.
- Architecture 3 (a housing association's estates, near-repeat burglary runs against each estate's background):
  spent at design; a filed back-test on about ten break-ins per estate-quarter cannot select the background projection
  on honest data (the usual winter wins the back-test in most seeds), and nothing short of a planted smoothing closes it.
- An airspace-change safety case on losses of separation per flight hour against interactions, read retrospectively
  (which sector's 2026 losses most exceed its traffic): the industry keeps losses per 100,000 flight hours as its
  standard rate, so "beyond what its traffic explains" is a fork between that rate and the interaction rate; the
  forward count with the tolerance filed literally removes the fork.
- Forklift and pedestrian near misses scaled by the product of zone occupancies: the product of two counts is a
  mass-action reflex for a quantitative solver, so the decisive rung is readable.
- Rail signals passed at danger per approach at red: a stop-aspect exposure is the first thought once an aspect log
  ships (a solver reasons that only a red signal can be passed at danger).
- Hospital ward acquisitions of a resistant organism per colonised patient-day: colonisation pressure is infection
  prevention's own reflex, and under mass action it equals the colonised-day rate the reflex computes.
- A survey's regional estimate moved by a gradual shift to web interviewing, separated by its randomised-mode
  subsample: the randomised arm is a schema cue a solver uses at once.
- Excess deaths in a heatwave net of mortality displacement: once the window is filed literally the net excess is a
  reading, and the field is architecture 2's.
- Ambulance mileage, impossible days, upcoding against audit-log time, check kiting on uncollected funds: each turns on
  a filed rule or a field read correctly (rule application or data semantics).
- A workload ceiling crossed in saturated hours (errors by occupancy band applied to a 2027 staffing plan) and a queue's
  ageing into a 52-week breach: both are state-based forward projections, the family task183 and task132 already hold.
- The first cut shipped a workbook and a PNG chart as the goldens, the pair task183 shipped the same day; the surface screen put the two builds at 0.100, so the goldens became the review board deck and a measures CSV.
- The first cut graded every sector's forecast at one decimal: the seven sectors under the line fork between the
  pooled losses per pair and each sector's own ratio (Linmark 24.1 against 25.6, Lysvik 26.4 against 24.9), so the
  deck grades the set over the line and Tarvik's rate, and the other seven as under 30.
- The delay ask with the slot list's plans that never reached the flight data left unfiled: read literally, every
  sector's delay moved at two decimals; the extract notes now file the network manager's definition (counted for the
  flights that operated).
- A configuration log remark of a sector bandboxed briefly and reopened minutes later with no logged change: deducting
  it moved Tarvik's hours open alone to 1,531.7, so the remark left the log's vocabulary.
