# task175 design note

**Architecture 1 (rebuild of 2026-10-23).** The number was reopened under the author's rule that no number stays
retired, and is rebuilt from scratch in the cell urban-regional-science / land-use-spatial-development-modeling
for Forecasting. Everything screened on this number before 2026-10-23 (the seed FC46's world, the
human-reliability cell and the strategy-backtesting cell) is spent and kept below as history
(`## Earlier screens (2026-10-18 and 2026-10-19)`, `## Tried and rejected`, `## Retired`).

## Draw

- **Card.** `cards/task175.json`, filed 2026-10-23 through `register_serial.sh`; `guard.py check` WARN on
  `repeat.gate_g` only (answered below), with the older same-puzzle and same-driver signatures differentiated
  against task124, task132, task144, task163, task465 and task165.
- **Pairing.** Client domain urban-regional-science, task type land-use-spatial-development-modeling (serves
  Forecasting); objective Forecasting & Predictive Modeling; decision a quantity figure (a count of permits);
  shape 07, a grid: the call as the three areas' total, with the asks' grid of fiscal 2026 connections (the core and
  four phases by quarter) and the four quarters' capacity fee receipts.
- **World.** Port Ardell, a fictional Gulf Coast Florida city of about 95,000 residents, platted lot by lot by the
  Ardell Gulf Land Company between 1958 and 1971 (about 110,000 quarter-acre lots in numbered plat units) and
  built one home at a time. The city-owned utility runs the Ardell Utility Extension Program: water, sewer and
  irrigation lines are carried into one area at a time, paid for by special assessments on the lots, and an
  area's lots can connect once its lines are accepted. The program sewered the areas with the most septic tanks
  first. Its 2027 phase connects three areas from January 2027: North 6, North 7 and Northwest 3.
- **Decision and call.** The utility's bond resolution requires a revenue sufficiency report each January, and
  its capacity fee line, the 2027 meter purchases and the connection crew hours rest on the number of
  single-family building permits the city will issue in 2027 on lots in the three areas (forward facing: the
  window is not yet open). The call: that count for the three areas together (the per-area figures left the call in the round 1 fix).
- **The quantity.** Each vacant lot's chance of a single-family permit in 2027 once its lines are accepted,
  summed over the three areas' vacant lots at the 2026 market.
- **Strategy and family.** `composition_mix` (pattern none, G6 then G14), Layer 2 family
  `estimand_identification`, `layer2_pattern` urban-regional-science/land-use-spatial-development-modeling/3
  translated: the card's pitfall is that a land-use change lands where growth already was, and its shortcut
  (the treated areas' before and after, or the area average) is this build's default path; here the city served
  its most built-up areas first, and the comparison the data force is lot by lot on the street each lot faces.
- **Data-native sentence.** Port Ardell's lots were sold to distant buyers in the 1960s and are built one at a
  time, and a builder puts a spec home where homes already stand on the street it faces; the utility sewered the
  areas with the most septic tanks first, so every earlier extension area was connected with most of its streets
  started, and the 2027 areas are the empty end of the city.
- **The screen, measured before the card** (`scratchpad/b175n/proto/a1.py` to `a4.py`, five seeds, a 76,000-lot
  world with 15 earlier extension areas served 2010 to 2024 and three forward areas, about 20,000 permits on
  360,000 served lot-years). Against the 2027 expected truth: the first-year analog 58 to 77 per cent high
  (market-scaled) or 36 to 62 per cent (raw); a regression of the analog on each area's built share at service
  37 to 75 per cent high once the earlier areas' started-street share is realistic; the lot hazard on the plat
  block's build-out 28 to 39 per cent high; on adjacent lots 32 to 38 per cent high; a log-share parametric form
  of the street exposure 10 to 15 per cent high; homes within 110 metres minus 9 to plus 10 per cent; the golden
  (served lot-years binned on the street segment's build-out with year effects, applied at 2026) within
  0.2 to 0.6 per cent of itself across 5 and 10 point bins and minus 1.5 to plus 6 per cent of the truth. The
  street exposure beats the plat block, the radius and the adjacent lots by 550 to 1,000 log-likelihood units.
- **On the generator** (`task175/generator/`, 98,512 lots, about 18,500 single-family permits 2008 to 2026): the
  golden 293.2 expected distinct lots (300 at the nearest 50) against a 2027 expectation of 274; the default 506,
  every rival a bin or more away (`## Ladder`).
- **Sources.** The library card (land-use 3, upzoning goes where growth already was): taught the shortcut and
  the comparison; this build differs in that the decisive comparison is a neighbourhood term no area-level
  comparison reaches. task134 (the cell's only earlier card): the yield of a raised allowance through
  feasibility; nothing here is a zoning allowance or a feasibility test. task165 (the nearest held shape): a gain
  that is the headroom the old service left; here there is no dose or headroom, the street's build-out
  multiplies a hazard. task484: lease-up of new buildings, not their building.
- **Guard, the relabel and the WARN.** The first check BLOCKed `ban.pattern` on G14 against task273 (live in
  the last three). G6 (composition shift) is the decisive label because the error the default path makes is
  carrying a rate measured on one composition of streets to a population of a different one, and the
  conditioned yield (G14) that fixes it is stable; both codes stay on the card. `repeat.gate_g`: the lane's
  objective is Forecasting and its Gate G is the forecast itself; the mechanism is the street-level hazard, new
  to the forecasting corpus. Personas Melissa Payne and Steven Burke from `guard.py names --geo us --seed 175`.
- **Axes against the live window** (task273, task169, task478): forum `executive_team`, forcing event
  `statutory_or_regulatory_filing`, organisation `utility_or_infrastructure`, role `finance_controller`,
  artifact `register` (the extension program schedule), shape 07. The forcing event was first drawn as
  `launch_or_rollout` (the three areas go live in January 2027) and BLOCKed under the registration lock
  against task273; the honest replacement is the January revenue sufficiency report the bond resolution
  requires, which is the filing that carries this forecast, and the go-live stays in the world as a fact.

## Default path

1. Read the prompt and the forecasting conventions: single-family permits by issue date in calendar 2027, on lots in
   the plat units the schedule lists for North 6, North 7 and Northwest 3, the expected number of distinct lots
   permitted, the market held at its 2026 level.
2. Map every lot to its area through the plat unit in `LEGAL_DESC` and the schedule's table; take each earlier
   extension area's acceptance date from the same table.
3. Stitch the two permit systems (the legacy file by site address, the new file by parcel, carried-over permits
   once) and count, for each of the fifteen earlier areas, the single-family permits issued in the twelve months
   after its lines were accepted over the lots still vacant at acceptance.
4. Apply the pooled first-year rate (4.2 per cent of vacant lots) to the 14,232 vacant lots of the three 2027 areas,
   each from its scheduled acceptance date.

Ends on: 500 permits in 2027 (506.3 unrounded)

Golden: 300 permits in 2027 (293.2 unrounded)

## Stump sentence

A competent solver applies the permits per vacant lot that the earlier extension areas drew in their first year of
service to the 2027 areas' vacant lots and files 500 permits (506; 566 with the first years rescaled to the 2026
market, 549 with the rate regressed on each area's built share at service), against 300, because it never reads
each vacant lot's chance at the number of homes standing on the street it faces: the city connected its most
built-up areas first, so every earlier first year was drawn from streets that already had homes, while 10,309 of the
14,232 vacant lots in North 6, North 7 and Northwest 3 stand on streets with no home at all.

## Three rules

Task type: land-use-spatial-development-modeling (urban-regional-science), which serves Forecasting: the forward count of lots a utility extension turns into building sites, worked lot by lot.
Domain test: the deciding quantity is each vacant platted lot's yearly chance of a single-family permit once water and sewer reach it, which land-use change models estimate lot by lot with a neighbourhood term (the homes already standing on the lot's street), carried here to areas whose streets are nearly empty.
Swap: "how many prescriptions will the three new clinics fill in 2027" keeps the arithmetic of a rate times a population, but there is no platted lot, no street segment of a hundred-block, no utility extension sequence chosen by septic density and no first home on a street, so the step that moves the answer has nothing to stand on.
Layer 1: a legacy permit system keyed by address and a 2019 system keyed by parcel, overlapping on carried-over permits (Building Division systems); legal descriptions and site addresses to parse to plat units and hundred-blocks (appraiser's roll); the roll as of 1 January 2026, so 2026 completions show only as certificates of occupancy (appraiser's cycle); the program schedule as a table in a PDF (Capital Program Division); fiscal against calendar years, premises without parcel numbers, an AMI head-end log and a cashiering export at permit-line grain (utility systems); nothing placed to be caught.
Layer 2: estimand_identification, card land-use 3 translated: service went where building already was, so the treated areas' first year is not the comparison; the comparison the data force is a served vacant lot on a street with as many homes standing as the forecast lot's own.
Decisive step: read each vacant lot's chance of a permit at the build-out of the street it faces, from served vacant lot-years 2008 to 2026 with the homes standing on the street on 1 January, and sum it over the 2027 areas' lots street by street, instead of carrying an area-level first-year rate.
Not semantics: every field (plat unit, hundred-block, year built, certificate of occupancy, acceptance date) can be read correctly and the analog route still files 520; nothing in any file says a lot's chance depends on its street, and no column holds a street's build-out.
Not rule application: no filed rule or procedure says how a lot's chance is estimated; the conventions fix only what is counted (permits, issue date, plat units, calendar 2027, expected distinct lots, the 2026 market). The enumerated honest family (homes-on-street count bins, 5-point and 10-point share bins, rate times exposure against the filed expected distinct lots, fit windows from 2013, 2019 and 2025, the 2023 to 2026 level, no canal term, a zero-homes indicator, a zero indicator plus a linear count) spreads 283.2 to 315.6 on the total, one printed total (300 at the nearest 50) with every member 8.2 or more inside the bin; the forms the data reject (the zero indicators, about 11 and 27 log-likelihood units worse; no canal, 249 worse) are kept in it on purpose, and the ruling-out of the rivals is loud: the street beats the plat block by 354 log-likelihood units and homes permitted rather than completed by 42.
Analyst test: a strong analyst who stitches both permit systems, maps every lot through its plat unit, reads the acceptance dates and holds the 2026 market takes the earlier areas' first-year permits per vacant lot and files 500 permits (Ends on), or 550 to 600 rescaled or regressed, against 300.
Estimand: the expected number of distinct lots receiving a single-family building permit (work class Residential New Single Family) issued in calendar 2027 in the plat units the schedule lists for North 6, North 7 and Northwest 3 taken together, a lot permitted at most once, the building market held at its calendar 2026 level; filed in revenue_sufficiency_forecast_conventions_fy2027.pdf section 2 with the schedule's table.
No decoy: nothing is planted to be caught: no forecast, target, earlier estimate, memo or stakeholder figure ships; the analog is the solver's own arithmetic on the permit record, and the schedule and conventions state only facts the organisation files.
No certified replay: no certified or published figure is reproduced to recover the method; the conventions file the WHAT and no figure in the pack is a published output of the forecasting method.
Lesson: a development rate measured where a utility (or any infrastructure) went first is conditioned on the build-out that sent it there; a model learns to read the forward lots at their own neighbourhood's build-out, which no build on file teaches (task134 conditions on feasibility, task165 on a service headroom, task484 on months since completion).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 first-year analog of the earlier areas | no | no | yes (the absorption analog) | no | no | yes | readable |
| 1 analog rescaled to the 2026 market, or regressed on each area's built share | no | yes (acceptance dates, YR_BUILT) | yes | no | no | yes | readable |
| 2 lot model on parcel attributes, canal and plat block | no | yes (WATERFRONT, BLK in LEGAL_DESC) | yes (add the visible attributes) | no | no | no | readable |
| 3 (decisive) homes standing on the lot's street (hundred-block, both sides) on 1 January | no | no (no street key; the hundred-block is built from SITE_ADDR) | no (the opponent's reflexes are pool, analog, control, reweight, shrink) | no | no | no | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | single-family building permits | work class Residential New Single Family, legacy RES NEW SFR | any residential permit (pools, re-roofs, additions) | thousands | conventions section 2, PERMIT_PIN |
| SF2 | issue | the issue date | application or certificate of occupancy date | other years' permits | PERMIT_PIN, "by issue date" |
| SF3 | in 2027 | calendar 2027 | fiscal 2027 (October 2026 to September 2027) | another window | PERMIT_PIN, "in the calendar year forecast" |
| SF4 | on lots in North 6, North 7 and Northwest 3 | lots in the plat units the schedule lists for each area | areas by street prefix or by the special assessment roll | other lots | PERMIT_PIN, "plat units the program schedule lists" |
| SF5 | the 2026 market | the 2026 year's level | 2023 to 2026 average (288.5) | same call (asserted, 300) | same call; MARKET_PIN |
| SF6 | carried-over permits | counted once | both copies kept | same call (asserted) | same call |
| SF7 | when a lot is served | from the acceptance date | from the following month | same call | same call; ACCEPT_PIN |
| SF8 | permits before an area is served | counted at the well and septic rate | left out | same call (asserted) | same call |
| SF9 | how a forecast counts | expected distinct lots, one less the exponential of the cumulative rate | rate times exposure (297.3) | same call (asserted, 300) | same call; ESTIMAND_PIN |
| SF10 | the graded figure | the three areas together | each area | not graded: at the nearest 5, 10 and 25 some area's family straddles a line (asserted B3) | the prompt asks for the total only |

## Ladder

| Rung | Route | 2027 total | Printed (nearest 50) | Distance from the golden's bin (275 to 325) | Dies to |
|---|---|---|---|---|---|
| 0 | first-year analog, raw | 506.3 | 500 | 181 | the street exposure: the earlier areas' first years were drawn on built streets |
| 1a | analog rescaled to the 2026 market | 566.4 | 550 | 241 | same |
| 1b | analog regressed on built share at service | 549.1 | 550 | 224 | an area's built share is not its streets' |
| 2a | served lot model without the street | 609.1 | 600 | 284 | same |
| 2b | lot model on the plat block's homes | 396.4 | 400 | 71 | the block mixes two streets' lots; 354 log-likelihood units worse |
| r1 | round 1 readers (area Poisson with an acceptance-year exposure; last three areas' intensity) | 430, 550 | 450, 550 | 105, 225 | the area mix is not the streets' |
| 3 | golden family (count bins and ten members, `## Three rules`) | 283.2 to 315.6 | 300 | inside, 8.2 or more from each edge | |

Position and margins: the golden is the lowest figure on the ladder and every correction short of the street walks
the figure down toward it from above; the nearest wrong rung (the plat block) sits 71 past the bin's edge, more than
a bin. Worth: the street step moves the total from 506 to 293 (42 per cent of the default, 73 per cent of the
golden) against an honest-family spread of 32 on a bin of 50. The per-area figures left the call in the round 1
fix (`## Stage 4 round 1`).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | lots in the three areas' plat units, vacant on 1 January 2027 | filed (PERMIT_PIN and the schedule) |
| 2 Unit of account | permits | the question names it |
| 3 Attribution window | issue date in calendar 2027 | PERMIT_PIN |
| 4 As-of dating | records to 31 December 2026; roll as of 1 January 2026 | dictionary (ROLL_YR) and manifest |
| 5 Version basis | schedule Revision 12 | the schedule and conventions name it |
| 6 Denominator | vacant lots, each counted once | C1: every route counts the same 14,232; ESTIMAND_PIN |
| 7 Weighting | lot by lot | the estimand sums lots; C1 |
| 8 Window length | 2008 to 2026 history | C3: the golden family agrees within 0.5 per cent across fitting windows from 2013 |
| 9 Boundary inclusivity | acceptance day inclusive | ACCEPT_PIN |
| 10 Rounding path | the total to the nearest 50 | the prompt; the honest family inside one bin (asserted B1) |
| 11 Tie-break | none | no ranking |
| 12 Maturity and censoring | lots permitted in 2026 are not at risk | C1: the vacant count excludes them in every route |
| 13 Order of operations | none non-commuting | C1 |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | carried-over permits once | SF6, same call asserted |
| 16 Identity normalisation | legacy addresses to the roll | dictionary semantics; mess neutral (R2) |
| 17 Netting against gross | none | n/a, nothing nets |
| 18 Dimensional units | counts | n/a |
| 19 Code and status semantics | work class and use codes | dictionary semantics, never the stump |
| 20 Integerisation | rounding of expected counts | the prompt's rounding |
| 21 Clause scope | the conventions govern the January 2027 report | the conventions say so |
| 22 Forward window contents | the 2027 acceptance dates | the schedule's scheduled dates |

## Literal reader

Executed word for word, the prompt and the conventions fix the count (single-family permits, issue date, calendar
2027, plat units, expected distinct lots, 2026 market, lots served from their acceptance dates, the three areas'
total at the nearest 50) and leave the estimate of each lot's chance to the data; every reading of SF1 to SF10
either violates a quoted sentence or files the same call, and the easy answer (500) comes from an easy method on the
same literal estimand, not from another reading.

## Oracles

none: no control, published figure or reconciliation column in the pack confirms either the analog or the golden;
the schedule's lot counts and the roll agree under every route, and the special assessment roll and the ACS tracts
(the distractors) carry no permit counts.

## Ask sheet

- **Ask A, new single-family connections in fiscal 2026, core and four phases by quarter (20 figures).** H18 home:
  the actual connections the January report sets beside the forecast. Files: `ami_headend_installs_fy25_fy26.csv`,
  `cis_account_history_20261231.csv`, `cis_premise_extract_20261231.csv`, `pa_parcel_extract_2026.csv` (to place a
  premise), schedule PDF. Primary (D1, a replay under fresh ids at a kept premise, re-sited in the round 1 fix): a
  meter pulled when a build stalls is set again when work resumes, and the head-end logs the second set as a fresh
  install at the same premise, before any account opens, so it passes the "no account before the install" rule and
  matches a new single-family permit; only a premise's first install is its connection, which the log itself shows
  (two installs at one premise, no account between). In every cell. Hazards (mirror devices, round 1's primaries):
  meter exchanges at billed homes, the premise's stored UEP_PHASE from before the 2021 regrouping, fiscal quarters,
  premises without a parcel number. Stops: every install (cracker), the account rule with plat-unit phases (reader A),
  the account rule at 1,000 days with set-up-date phases (reader B), stored phases, the answer.
- **Ask B, capacity fees received in each fiscal 2026 quarter (4 figures).** H18 home: the receipts line of the
  January report. File: `capacity_fee_receipts_fy2026.xlsx`. Primary (D1, keys recycled across payers, re-sited in
  the round 1 fix): receipt numbers run by drawer and day (YYDDD-NNN) and the export does not carry the drawer, so a
  payment at the second drawer shares its number with a same-day, same-amount payment from another builder at the
  first; one amount per receipt number drops it in every quarter, and the line shows nothing (one receipt cannot
  have two payers, which the file itself shows). Kept beside it, the round 1 grain device: a receipt covering several
  permits repeats its total on each line, so summing lines overstates. Fees now run per ERC (a 1 inch meter is 2.5
  ERCs, conventions section 4), so no fee-times-permits tie closes the quarter.
- **Chart (fy2026_new_connections.png):** its segment labels are Ask A's cells.
- Main population zero-counts: no device row in the roll or either permit file; the asks' files are not read by the
  call (asserted S1, S2).

| Ask | Figures | Cracker and round 1 readers' routes (installs, account rule, plat-unit or set-up phases, one amount per receipt number) | Verdict |
|---|---|---|---|
| A core, Q1 to Q4 | 4 | re-sets counted | miss |
| A Phase 1, Q1 to Q4 | 4 | re-sets counted | miss |
| A Phase 2, Q1 to Q4 | 4 | re-sets counted | miss |
| A Phase 3, Q1 to Q4 | 4 | re-sets counted | miss |
| A Phase 4, Q1 to Q4 | 4 | re-sets counted | miss |
| B Q1 to Q4 | 4 | shared receipt numbers merged (or lines summed) | miss |

Pair ceiling: 28.5 (worst of four routes keeps 0 of 24; cracker 45.0, mirror 12.0, on weights 38, 7 and 55)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

## Stage 4 round 1 (on target.zip 0c46c781) and the fix pass

- Readers: A filed 430, B filed 550, both off the call (each fitted areas, not streets); both kept all 24 ask figures
  (A: dropped the 237 exchanges by the account rule and tied the rest to new permits, re-derived phases from the plat
  unit, counted each receipt once; B: the same with a 1,000-day account rule and set-up-date phases).
- Judge: NOT_DETERMINISTIC, margin_or_boundary_fragility on the call: the honest family (rate against expected
  distinct lots, fit windows, averaged levels, zero-homes forms) spread 289 to 321 against bins of 5 and 10. Gate H
  passed, the stump analytical; the asks forced.
- Fix 1: the conventions file the estimand as the expected number of distinct lots, a lot permitted at most once
  (ESTIMAND_PIN), the golden switched to one less the exponential of each lot's cumulative rate, the call is the
  three areas' total at the nearest 50, and the per-area figures left the call: at the nearest 5, 10 and 25 some
  area's family straddles a line (North 6 84.3 to 94.2, North 7 108.6 to 121.7, Northwest 3 90.0 to 99.7; asserted
  B3). Northwest 3's scheduled acceptance moved 6 to 13 April to centre the family: 283.2 to 315.6 in 275 to 325.
- Fix 2: the asks' primaries re-sited (`## Ask sheet`), measured against the cracker and both readers' routes in
  `ceiling.py`: 0 of 24 kept on every route.
- Fix 3: the plat index records units in order, 1958 to 1971, books and pages running as a recorder's would.

## Stage 3 gates (2026-10-23, re-run after the round 1 fix)

- Generator: `python3 task175/generator/build.py`; `checks.py` 70 assertions green (input gates, R1, R2, R3a and
  R3b against the bin, the honest family B1 to B3, SF1 to SF10, refutations L1 to L3, the ask devices on four
  routes A1 to A4 and B4 to B7, separation S1 and S2, documents, realism, distractor deletion); `verify.py` (pandas,
  pypdf, IRLS, its own path) recomputes 293.2 and every ask figure, 0 failed; two consecutive builds byte-identical
  over 19 files; `target.zip` md5 cb34c3c769a0d303ed59de94b40790c7.
- `figures_check.py` PASS (39 figures); `precut.py` exit 0; `voice-check.py` PASS (734 characters); `guard.py heart`
  WARN (`repeat.gate_g`, answered at the draw); container scrub audit clean.
- `leak.py --asof 2027-01-08` REVIEW, each line harmless: the dictionary and the conventions share common words
  (family, january, vacant, schedule, forecasting) with the stump paragraph and name no move (D2 greps them for the
  street vocabulary with a positive control); the permit system's Expiration Date runs a year past issue, so
  permits issued in 2026 carry 2027 expiry dates.
- Single-use test: no file or sentence serves only the street step.
- Keys for the round 2 readers: the call `call_total_permits_2027` (the per-area keys are gone); the asks
  `ask_connections_fy2026_<core|phase1|phase2|phase3|phase4>_q<1..4>` and `ask_capacity_fees_fy2026_q<1..4>`;
  withhold `cc1_*`, `cc2_*`, `label_*` and `_unrounded`.

## Earlier screens (2026-10-18 and 2026-10-19)

History, kept as written; every world, cell and mechanism in it is spent.

### What was screened

- **Seed** FC46, header and Situation only (`status.py task175`). Kept: an online music retailer gives
  its 25,000 best customers a free two-day shipping membership for 52 weeks; the programme pays at most
  $150 of any member's shipping; the catalogue sits across three fulfilment centres, standard orders
  wait for the consolidation shuttle and ship in one parcel, two-day orders cannot wait and ship one
  parcel per centre the basket spans. The call: the shipping the programme pays for the 25,000 over the
  first 52 weeks, one budget figure. The seed's own mechanisms (a parcel count read off the SKU location
  table, the cost report's per-item shipping as an official decoy) were never candidates.
- **Pairing tried:** `product-analytics` / `retention-cohort-lifetime-value-modeling` (serves F),
  objective forecasting, decision a quantity figure. `churn-propensity-uplift-modeling` was the fallback
  for a response-heterogeneity step; the measurements below close both.
- **Corpus reads** before any design: `guard.py recent`, `coverage`, `mechanisms --objective
  forecasting` (81 builds) and `slots` on three term sets (membership, subscription, free shipping,
  capped, limited expected, Jensen; BG/NBD, Pareto, P(alive), dropout, lapsed, regression to the mean,
  heterogeneity, negative binomial; cart, session, batching, basket, consolidated). The hits that bear:
  task151 rejected the step payout alone at its draw ("one enumerable insight (Jensen) is the coin-flip
  signature"); task147 rejected a Jensen gap on capacity as too small to move its pick; task130 v3 died
  on the analog cohort (a group chosen on a noisy outcome, forecast by the next-period experience of a
  group chosen the same way, landed in four minutes); task153's driver is a per-segment cap at a
  tankful; task142 and task143 spend "the distribution, not the point" on a percentile and a joint
  chance. No screen on file touches cart sessions or order batching.

### The harness

`scratchpad/b175/proto/` in this session (session-scoped; rebuild from this section). `proto2.py` is
candidate 1, `proto3.py` candidate 2, `pilot52.py` the subset arithmetic, `proto1.py` and `sweep1.py`
the first parameter sweep. Shared world: 420,000 customers; weeks from Monday 2 January 2023 to Sunday
29 November 2026 with a December-heavy seasonal profile; registration dates spread with growth (55 to
60 per cent before the window); standard order rates gamma across customers (shape 0.8 or 0.9); the
25,000 chosen as the top trailing-52-week spenders to 29 November 2026; a 26-week randomised pilot from
28 April 2025 (15,000 treated of the then top 40,000 by trailing spend, the rest the holdout); per-order
two-day cost gamma with a member-level mean (zone and centre mix, lognormal SD 0.18) and CV 0.45, so a
year's cost given its order count is gamma and every capped expectation is computed exactly, summed over
the count's predictive distribution, never simulated. The golden in each candidate is what a correct
analyst computes from the pack: a negative binomial fitted by maximum likelihood on every customer's
counts and exposure, each member's posterior predictive for the membership year, the pilot's estimates,
and the cap applied to each member's predictive cost distribution.

### The structural finding: a member-level capped forecast is a continuum, and the cap cancels

The truncation-direction screen passes (the cap hides the top, and the latent quantity is the upper tail
of each member's coming year), and the variance-only screen passes (every spread moves the point figure
through the cap). What kills the family is three regularities, each measured:

1. **The right family is a continuum, not a point.** Every source of a member's predictive variance
   lowers the capped total by its own fraction: the estimation uncertainty of the member's own rate
   (posterior mean with chance on top, against the negative binomial predictive) **+1.26% to +1.54%**,
   the response's form at fixed moments (gamma against lognormal) **+0.41% to +0.51%**, the parcel-cost
   spread mis-set by a third **-0.41% to +0.30%**, and the pilot's own sampling (estimated against true
   response parameters) **-0.70% to +0.51%** at 15,000 treated (one sigma about 0.6 per cent; at 6,000
   treated +1.07% on one seed). The rate-uncertainty term is structural: its share of the predictive's
   chance variance is the membership multiplier over the years of history, about 0.47 to 0.52 at three
   years, so no realistic history removes it. The family therefore spans 1.5 to 2.5 per cent, which
   needs bins of 6 to 10 per cent for a quarter-bin margin.
2. **Under a per-member cap a misallocated factor is half absorbed, so errors cancel.** A member pushed
   above the cap loses its error and a member pulled below keeps it, so a common factor applied in place
   of each member's own errs downward, while capping a point forecast errs upward. The route that does
   both lands near the golden: orders times the pilot's average uplift, point-capped, **+1.77% to
   +2.60%** (candidate 2); the analog cohort times the average uplift **+2.15% to +3.06%**
   (candidate 1).
3. **The pilot is either too short or it hands the answer over.** A 26-week pilot leaves the annual cap
   to a model (the continuum above). A 52-week pilot answers by filter and divide: capping each of a
   random 6,000 like members' realised years and scaling to 25,000 lands **-0.86%** from the golden with
   a sampling SD of **0.58%**, within $50,000 of the golden in 194 of 200 draws. There is no pilot
   length between.

So at bins narrow enough for the far partial routes to miss (about 4 per cent, $100,000 on a $2.4M to
$2.7M figure), the right family alone breaks the quarter-bin and the cancelling routes of law 2 sit
inside one bin; at bins wide enough to hold the family (6 to 10 per cent), the plug-in, shrunk-response
and analog routes land in the golden's bin or the next. This is the same dial at both ends
that `stumping` 1.6a and `determinism-check` section 1 record for task194, met here on a capped sum.

### Redraw screen: human-reliability-assessment (2026-10-19)

- **Cell and fences.** human-factors-ergonomics / human-reliability-assessment (serves Forecasting), a
  pairing never built. The round's bans: pattern G14, `composition_mix`, `local_government`,
  `committee_or_panel` and `executive_team`, `programme_officer` and `capacity_planner`,
  `monitoring_export` and `filed_standard`. The guard's window after task249, task269 and task468 adds
  patterns G16, G2 and G13, strategies `causal_design`, `decomposition_attribution` and `composition_mix`,
  and shapes 04 and 05. The library refresh (b7a54be) leaves Human Factors with no cards, so the seeds
  were the five families in `two-layer-task-design.md` and the nearest domains' cards (healthcare
  delivery's patient-flow and provider-quality cards, general statistics' calibration, robustness and
  measurement-error cards, banking's reviewer-capacity and labels-above-the-line cards).
- **Deaths read first, all binding on this cell.** task171 (screeners' detection under short stints and a
  new-hire cohort; dispensing errors under longer shifts, task149's within-person driver); task230 v2
  (the low-prevalence effect at a shared verification pool, shipped in this task type and retired);
  task194 architecture 8 (signal detection's discriminability against criterion, accident-proneness, an
  own rate behind a load-dependent downstream catch); task202's six human-factors drivers (an unpublished
  opportunity count a forward change multiplies, which is task181 v4; within-period clustering; two
  checks' joint miss; a practice curve; a classification lag; a marginal contribution to a set); task181
  (losses of separation follow level crossings); task182 (composition and observability screens).
- **The structural finding.** In its own form, human reliability forecasting carries an error
  probability conditioned on performance-shaping factors onto the forward mix of those factors, which an
  honest card labels G14 or `composition_mix`, both out this round. The structures in this field that
  are not a mix (dependence between checks, prevalence and detection criteria, thinned counts, time on
  task, learning, shift length, unpublished opportunity counts, co-presence pairs, classification lags,
  bursts, proneness, load-dependent catch, latency waves, caps, calendar locks) are each spent on file.
  The residue was two candidates, a time-reliability race read at each demand's own window and a
  performance-shaping factor's slope flattened by a noisy record, and both died on measurement.
- **The harness.** `scratchpad/r175/proto/c11.py` (the race, five seeds, a `vol` multiplier) and
  `c10.py` (the flattened slope, three seeds, settings `b` and `lam`), session-scoped; each was run twice
  with byte-identical output, and the settings and figures are in the Tried and rejected lines so the
  harness rebuilds from this note. `guard.py slots` on both driver sentences returned lexical overlaps
  only (task182, task194, task117, task132, task201), no screen of either mechanism.

### Redraw screen: strategy-backtesting-evaluation (2026-10-19)

- **Cell and fences.** quantitative-finance / strategy-backtesting-evaluation (serves Forecasting), the
  graded call forward facing (a capacity, a capital or a net return at a planned capital, never a
  retrospective backtest statistic). The window re-read after the b7a54be refresh: task249 carries
  `architecture_spent`, so the live three are task268, task269 and task468 (patterns G6, G2 and G13;
  strategies `population_selection`, `decomposition_attribution` and `composition_mix`; roles
  `research_desk`, `programme_officer`, `operations_director`; forums `committee_or_panel`,
  `regulator_or_inspector`, `executive_team`; organisation families `hospital_or_health_provider`,
  `university_or_school`, `other`; shapes 04 and 05), on top of the round's bans; task170 draws in banking
  this round, so a bank's ALM desk was kept off every axis.
- **Seeds.** The library's Quantitative Finance cards (next-bar fills, point-in-time universes, reporting
  lags, deflated Sharpe, Fama-MacBeth, linked attribution, constrained and shrunk portfolios) are the
  default path and Layer 1 here; the judgment sought was one they take for granted, and for a capacity call
  that is what a strategy's own trading at the planned capital does to its costs and alpha. The domain's
  only cards on file are task135 (asynchronous valuation strikes) and task445 (13F completion), and `slots`
  found no screen of impact, capacity or crowding.
- **The structural finding.** A capacity forecast's decisive quantity is the market's response to the
  strategy's own flow, and the routes the data leave open are either the textbook square-root cost per
  trade (the default, which lands wherever the strategy's trades are isolated) or a model of how impact
  carries across days, whose classes agree on every one-way execution on file and part two to four times on
  a strategy's own runs and reversals; every judgment beyond that (informed drift in the slippage, the
  firm's netting, borrow demand) is a reflex control, a shared-pool clone or a minor cost line.
- **The harness.** `scratchpad/r175/proto/qf_runs.py`, `qf_family.py`, `qf1c.py` and `qf6.py`,
  session-scoped and deterministic per seed; settings and figures are in the Tried and rejected lines.

### Resume as written on 2026-10-19

No screen left a live design, so the next move is the coordinator's or the author's: move the number to
another Forecasting cell, or come back to human reliability or strategy evaluation when the round's G14
and `composition_mix` bans lapse. Do not re-screen, in any of the three worlds, anything in
`## Tried and rejected`:

1. **The seed's world (FC46).** The three laws close the per-member capped forecast for any decisive step
   that refines a member's predictive year, because the refinements form a continuum wider than a
   quarter-bin and the cap makes the common-factor and point-forecast errors cancel.
2. **Human reliability under this round's bans.** The cell's own form is a conditioned error probability,
   which is G14 by an honest label, and its non-mix structures are spent on file (the redraw screen's list).
   A time-reliability race dies on rare trips and the window-band filter and divide; a flattened factor
   slope dies on its lever and on the audited rows. A further draw here would start from a file the
   organisation keeps whose forcing input no stratification of the error log reproduces, and would price
   the four unscreened card seeds first, with their predicted deaths: labels that exist only above a
   review line (a verified subsample, spent, and a filter and a divide on it); reviewer-capacity yield (a
   binding constraint on a filed integer of hours); an error-risk score's calibration against its ranking
   (the card applied as stated, the library test); blocking probability against occupancy for a staffed
   desk (queueing, the swap test).
3. **Strategy evaluation under this round's bans.** A capacity call turns on how the market answers the
   strategy's own flow; the per-trade square-root cost is the default and the only data-forced refinement
   is how impact carries across days, whose model classes part 2.2 to 4.4 times on a strategy's runs and
   reversals while agreeing on every one-way execution a desk records. A further draw here needs an
   execution record that itself contains the strategy's runs and reversals, or a decisive step that is not
   a cost of the strategy's own trading.

Window facts on 2026-10-19 after the b7a54be refresh: task249 is spent and skipped, so patterns G6, G2 and
G13, strategies `population_selection`, `decomposition_attribution` and `composition_mix`, and shapes 04
and 05 sit in the ban window, and this round's serial registrations will move it again.

## Tried and rejected

- **Candidate 1, the cap priced on each member's predictive year, with the spread of individual
  responses the pilot measures** (2026-10-18, stage 1, measured on seeds 1, 2, 3). Driver as drafted: a
  per-member cap is worth the limited expected value of each member's coming year, whose spread comes
  from chance, from how far the member's own record pins its rate (the members were chosen for a good
  year), and from how differently members answer free shipping, which the pilot's treated arm shows as
  spread beyond its holdout's. Golden $2,449,197 to $2,478,491 (response mean 1.55, SD 0.70, gamma).
  Routes against the golden: posterior mean with chance and the response spread +1.52% to +1.54%
  (family, breaks the quarter-bin); lognormal response +0.41% to +0.51%; the three-year rate plugged in
  with the response spread +5.86% to +5.87%; individual responses shrunk toward the mean +5.01% to
  +5.35%; the analog cohort (last year's top 25,000 and their next year) times the average uplift
  +2.15% to +3.06%; the analog cohort with drawn responses -4.57% to -5.04%; posterior predictive with a
  common uplift +7.30% to +8.21%; the pilot's average cost seasonally scaled, uncapped, times 25,000
  +8.78% to +10.35% (and +0.85% in a configuration with shape 1.1 and response 1.40/0.65, so its position is
  a coincidence of parameters); point posterior capped +13.71% to +14.64%; the default path
  (trailing-year orders times the uplift times the two-day cost, capped) +28.47% to +29.58%; raw
  individual ratios as the response spread -12.39% to -13.13%; the pilot seasonally scaled and capped
  -15.52% to -16.47%; uncapped +30.95% to +32.41%. Sensitivity: +1% on the mean response moves the
  golden +0.67% to +0.69%, +5% on the response SD moves it -0.64% to -0.71%. The first sweep (true
  response parameters, response CV 0.30 to 0.60, cost $9 to $12 an order, shape 0.45 to 0.80) put the
  plug-in-rate route at +2.40% to +5.67% and the common-uplift route at +3.23% to +14.03%. Dead on the
  continuum (law 1) and the analog cancellation (law 2), and the response spread is a dispersion whose
  estimator family is open in form, which is the dispersion screen's warning met exactly.
- **Candidate 2, membership orders are the member's purchase sessions, which its paid-shipping orders
  batched** (2026-10-18, stage 1, measured on seeds 1, 2, 3). Driver as drafted: once shipping is free a
  member places an order at each visit whose items it buys (the cart log's sessions), so the coming
  year's orders are its sessions, not its past orders times the pilot's uplift, and heavy buyers, who
  batched most, take the cap fastest. Built to remove candidate 1's latent response form (each member's
  response is its own sessions per order, observable, correlation of log sessions with log batching
  0.55 to 0.57 among the 25,000). Golden $2,691,823 to $2,709,498 (the pilot's session-to-order
  conversion 0.879 to 0.881 and session uplift 0.076 to 0.083). Routes: posterior mean with chance
  +1.26% to +1.27% (family, breaks the quarter-bin); orders times the average uplift, point-capped
  +1.77% to +2.60%; the same with chance +2.36% to +3.20%; the pilot's average cost seasonally scaled,
  uncapped +3.37% to +3.73%; the three-year session rate plugged in +4.37% to +4.43%; items over the
  pilot's basket +4.97% to +5.45%; orders times the uplift with the predictive -4.53% to -5.28%; the
  analog cohort's orders times the uplift -4.69% to -5.76%; point posterior sessions capped +6.38% to
  +6.40%; every session taken as an order +6.92% to +7.08%; trailing-year sessions +10.07% to +10.19%;
  the default path +10.94% to +12.08%; the pilot capped and scaled -17.25% to -17.60%; uncapped +23.56%
  to +23.89%. The analog cohort's own sessions, the empirical member of the right family, sat -2.05% to
  -2.56% (the harness dropped the pilot's treated members from the analog, whose second year carries
  membership months; a careful analog strips those months instead). Dead on laws 1 and 2: the
  point-capped uplift route and the pilot average sit inside one bin, and the family spans more than a
  quarter-bin. The order-to-session unit is also `grain_or_unit` beside task153's segment-by-segment
  cap, which the brief named as a driver to stay clear of.
- **Also set aside at the draw, on paper, before either prototype:** the cap's Jensen gap alone (task151's
  measured coin-flip signature, and enumerable); regression to the mean of the chosen 25,000 alone
  (task130 v3's analog-cohort death, and the analog is free here); the pilot's mean response as the
  decider (the common-exposure subset screen, law 3); the split count off the SKU table (a stated
  construction, the seed's banned mechanism); a novelty burst in the pilot's response (the midpoint of
  the pilot's average uplift and its latest month is exactly the 52-week answer, since the burst falls
  once in both windows); the response conditioned on batching or on the delivery time two-day saves
  (`composition_mix`, which task165 and task173 carry in the ban window, and a stratification reflex on
  a column the history builds); a capped trial's stopping rule (Wald's identity makes events over
  exposure on the offer weeks consistent, so the on-offer weeks answer by filter and divide); free
  shipping weeks as the response (a promotion measures stockpiling, not the unbatching a membership
  causes); uptake of the invitation (a censored activation clock on the lightest members, a lever of a
  few per cent); members going quiet in the year (the analog cohort hands it over by recency band).
- **Redraw candidate 11, a time-reliability race read at each demand's own window** (2026-10-19, stage 1,
  human-reliability-assessment, `c11.py`, five seeds). World: a bulk liquids terminal whose operators stop
  each transfer between the high-level alarm and the automatic overfill trip; the time each alarm leaves
  is the tank's headspace between the two levels over the transfer's fill rate; the operator's response
  is a two-component lognormal (attentive, median 4.0 minutes; lapses, 12 per cent, median 16) independent
  of the rate; 2027 raises the pipeline receipt rate into the gasoline tanks from 700 to 1,000 to 1,600 to
  2,000 cubic metres an hour. Graded figure: expected automatic trips in 2027. Driver as drafted: the
  chance a demand fails is the response-time survival read at that demand's own window, so shorter
  windows raise trips by the curve's bend across demands rather than at their average window. At a
  typical terminal (about 10,800 transfers and 480 alarm demands a year, 23 to 41 trips in four years,
  2027 truth 11.2 to 12.8 trips) the golden family (Kaplan-Meier on response times censored at each
  trip's window, and the two-component mixture) agrees within 2.4 points but sits -11.0 to +14.5 per
  cent from the truth, sigma about 9 per cent. At the largest realistic terminal (three times the volume,
  88 to 108 trips in four years, truth 33.3 to 38.3) the golden sits -2.6 to +8.7 (sigma about 4) while
  the trip share by window band, a filter and a divide once each demand's window is built, lands -12.3
  to +5.7 (mean -1.8); trips per demand by stream with the changed stream rate-scaled -13.1 to -30.7;
  persistence -18.9 to -41.3; the field's textbook time-reliability curve (one lognormal fitted to the
  operators' stop times, read at the nominal window) -77.3 to -85.3, and with the trips taken as
  censored -67.0 to -76.2; single-component censored Weibull and log-logistic fits 25 to 50 per cent
  under. Only at ten times a terminal's volume (about 20,000 demands, 350 trips) does the golden reach
  +0.1 to +5.8, and there the window-band share lands -7.0 to +7.9. Dead three ways: sigma 4 to 9 per
  cent at any real volume, because trips are rare and the lapse tail that decides them is read from
  those few; the subset screen (the window-band share lands inside the golden's own seed range); and
  the library test (the golden is the censored survival curve applied demand by demand, the
  probabilistic-analysis card's "not at the mean" with the forcing fact, faster receipts, cueing the
  window). An honest card also reads it as a trip rate conditioned on each demand's window carried to the
  forward window mix, G14.
- **Redraw candidate 10, a performance-shaping factor's slope flattened by a noisy record** (2026-10-19,
  stage 1, `c10.py`, three seeds). World: medication administration errors per ward-shift Poisson in
  administrations, log rate rising by `b` per patient per nurse actually on the floor; the staffing
  system records the ratio with classical error (reliability `lam`); a badge-swipe audit on four wards for
  six months (2,160 ward-shifts) carries the true ratio; 2027 mandates at most 5 patients per nurse
  against a recorded mean of 6.3. Graded figure: expected 2027 administration errors (truth about 11,700).
  At a realistic effect and record (`b` 0.15, `lam` 0.6, 43,000 errors in three years) the naive slope
  misses by only +7.0 to +9.3 per cent (fitted 0.089 to 0.091 against 0.15), against the 30 per cent
  that held; the golden (regression calibration, moments) sits -1.6 to +1.3, SIMEX with a quadratic
  extrapolant +3.3 to +4.0, and the slope fitted on the audited ward-shifts alone -5.7 to +2.2. The lever
  is exp(-b(1-lam)D) for a forward shift D, so 30 per cent needs `b` 0.30 with `lam` 0.4 at once; there
  the naive slope misses by +27.5 to +31.1, but the golden's own seed range widens to -7.1 to +7.0
  (reliability estimated 0.36 to 0.40 from the audit), SIMEX splits the family at +15.0 to +21.9, and
  the audited rows alone land -0.6 to +2.4, nearer the truth than the designed correction. Dead on the
  lever at any plausible setting, on the subset screen (the card's own validation rows are a filter that
  beats the correction), on an open method family (the extrapolant), on the library test (general
  statistics' measurement-error card 2 applied as stated, its pin the audit file), on the swap test
  (staffing and errors swap for any load proxy and failure count) and on the label (an error rate
  conditioned on staffing carried to the mandated ratio is G14), beside task149's workload driver.
- **Also set aside in the human-reliability cell, on paper, before either prototype:** the low-prevalence
  effect at a final check after an upstream improvement (task230 v2, and G14 by its honest label;
  inside the observed range a filter and a divide, outside it a 15 per cent family spread on paper);
  confusable items or addresses grouped together (task181's co-presence); red-signal approaches as the
  exposure for a new timetable (task202 C1, task181 v4, and the forecast of red approaches is an
  operations simulation); errors at the first execution after a change (C1 again, and G14); adding or
  removing a redundant check (task202 C3, and a read-across); latent maintenance errors found at
  scheduled inspections (a dose-response conditioned yield, task77 v1's pipeline and task157's wave);
  time-reliability tails for a single action (the empirical share is a filter and a divide,
  extrapolated tails spread by form, and samples per action are sparse); a reminder or re-alarm moved
  inside a response duration (task172's driver in other nouns); fatigue states under a new roster
  (task171's shift death, G14, and the fatigue models' own spread).
- **Quant candidate QF1, impact carried across days by a slow strategy's own trades** (2026-10-19,
  strategy-backtesting-evaluation, `qf_runs.py` and `qf_family.py`). World: 800 names (ADV median $25m,
  daily volatility about 1.8 per cent), a smoothed signal rebalanced daily, gross exposure twice capital;
  the strategy's same-direction trades run 8.9 days on average. Driver as drafted: the market prices each
  day's trade against the impact the strategy's own earlier trades left, so a per-trade square-root cost
  understates what a slow strategy pays at the planned capital. Measured at $1bn on one square-root
  calibration (Y 0.7): per-trade fresh start 92 bps of capital a year (the default); impact concave in the
  decayed cumulative flow 249 to 309 for memories of 5 to 40 days (flat at 282 to 309 for 8 to 40, and
  20,000 executions pin the memory to 13 to 34 days); each run priced fresh 500, and the opposite run's
  netting is why it overshoots; concave per-day impacts superposed with exponential decay 543 to 1,228; a
  power-law kernel 543 to 793. Dead on the estimator family: the model classes agree on every one-way
  execution a desk's file holds and part 2.2 to 4.4 times on the strategy's runs and reversals, which no
  one-way order tests, so pinning the class files the HOW and leaving it open forks the figure.
- **Quant candidate QF1c, the same mechanism behind a no-trade band** (2026-10-19, `qf1c.py`). Built to
  separate runs by idle gaps so that multi-day executions on file would force the class. The band makes
  trades isolated instead (mean run 1.00 day, median idle gap 4 days, 9 per cent of name-days trading):
  per-trade pricing sits at 0.99, 0.94, 0.81 and 0.63 of the truth for post-trade half-lives of 0.6, 1.0,
  1.9 and 4.3 days, and the superposed class at 1.00 to 1.30, so the lever vanishes where the class is
  forced and the family reopens where the lever returns. With a live record in the pack, the paper
  portfolio's gap to the real one is Perold's implementation shortfall, the textbook route, and it lands;
  set against the desk's slippage report it is a control that refutes the naive read.
- **Quant candidate QF6, the fund's own short demand pushing borrow fees up a convex utilisation curve**
  (2026-10-19, `qf6.py`, three seeds). At $2bn the fees cost 57.5 to 72.0 bps of capital a year against
  33.2 to 40.7 at today's fees (0.50 to 0.61), a minor line beside the gross alpha; the median fee of names
  already at the forward utilisation band, a filter and a divide on the prime broker history, lands at
  0.976 to 1.003; and the curve fitted to the same history explodes for the few names pushed toward full
  utilisation (log-linear 1.05 to 167 times, log-quadratic 6 times and far beyond), where the question is
  a hard cap on unborrowable shorts. Dead on the lever, the subset screen and the cap.
- **Also set aside in the quant cell, on paper:** informed drift in the desk's slippage (the golden's
  regression is slippage on the square-root participation and the signal, so the opponent's add-a-control
  reflex lands it); netting the new strategy's flow against the firm's other books (task164's and task106's
  shared-resource increment in other nouns); a hard borrow cap (a single-purpose file and a min()); alpha
  diluted into weaker signals at scale (a conditioned yield, G14); participation-capped multi-day
  execution losing a front-loaded alpha (QF1's family returns, and a capped simulation is the reader's first
  move); point-in-time vintages of a fundamental feed (alpha research card 2 applied as stated); merger
  arbitrage completion conditioned on time pending (task133's driver); a volatility target's leverage cap
  (G14 and a volatility forecast on the obvious covariate); auction and roll calendars (task162's
  calendar lock); limit prices truncating the desk's slippage (the cap that truncates, task168 and task172);
  alpha carried through cross-sectional dispersion (task446 v2 and task194's invariant abstraction);
  post-publication decay read across older signals (a filter and a divide, and a known result); carry read
  off today's curve (observable ex ante).
- **Rebuild screen, urban-regional-science / land-use-spatial-development-modeling (2026-10-23), set aside on
  paper or by a first harness before the card:**
  - Subdivision absorption by community count, opening ramp and sell-out: once each subdivision is capped at
    its remaining platted lots and new plats are added at the pace past openings kept, the ramp and the
    builder count move a county's year by under 10 per cent, and the per-subdivision run rate is the
    homebuilder's textbook route, so the golden would be the default.
  - The builder's section as the unit of pace (pace proportional to builders, not lots): the swap test reads it
    as stores in a mall, and the lever on a realistic roster is under 10 per cent.
  - Shared submarket demand among concurrent subdivisions or lease-ups: demand-limited absorption makes the
    trend the golden; lease-up after completion is task484's driver.
  - Upzoning yield refinements (applicant against city-initiated rezonings, land assembly against holdouts,
    network walksheds around stations): each is task134's world (homes from an upzoning), and an assembled site
    is a unit the records do not define, so the forecast forks on it.
  - Cellular-automaton contagion over a five-year window: the dynamic feedback moves a total by 10 to 15 per
    cent while the neighbourhood weights and the simulation open the estimator family.
  - Latecomer parcels in developer-financed sewer extensions (the financing developer's own parcels selected,
    the third parties exogenous): greenfield development is lumpy, about 70 parcel events across eight basins,
    so the golden's sigma sits near 12 per cent.
  - Student yield by the age of housing: a population-estimation task type, not this cell, and year built makes
    it a stratification a reader reaches by reflex.
  - Construction duration lengthening under pipeline load: swaps to any queue (rule 1), and the forward load
    sits beyond the history.
  - Entitlement conversion by approval age, vesting waves before a downzoning, a lifted growth cap, a moratorium
    lifted: task167's hazard by time since entry, task161's drawn-down stock and task168 and task172's cap.
  - Developer-built roads and mains leaking into a land-change logit: the point-in-time correction is standard
    and the forward extensions are themselves endogenous.
  - Transit capitalization at announcement for value capture: one subtraction of the current premium from the
    mature one lands it.
  - Candidate alpha, first harness (`a1.py`, `a2.py`): with a neighbourhood effect also acting before service the
    2027 areas' own unserved rate times the earlier areas' service uplift lands the golden (minus 9 to plus
    2 per cent), and with the earlier areas' started-street share drawn loosely the area-level regression lands
    on one seed in three (minus 4 per cent). Kept by making the unserved building flat (owner-builders on well
    and septic, not spec builders) and the earlier areas' started share realistic (78 to 92 per cent), which
    `a4.py` measures.
  - Build iteration (generator, 2026-10-23): a street term continuous in the share of the street built (0.15 at
    an empty street rising with scale 0.06) left the golden family 0 to 4 per cent apart across 5-point, 10-point and
    homes-count bins, too wide for the printed total; replaced by a term on the homes standing (empty, one home, then
    rising), where the family sits within 0.8 per cent. A pre-service rate of 0.025 of the served one put enough
    2026 completions on the 2027 areas' streets that reading the roll alone moved the total a bin (R2a); set to
    0.012, a well and septic home being rarer than a sewered one.
  - Stage 4 round 1 (2026-10-23, zip 0c46c781): the call at 90, 115, 95 and 300 (areas to 5, total to 10) was
    fragile on Gate C: the honest family spread 289 to 321, so the per-area figures were dropped and the total moved
    to the nearest 50 with the estimand filed. The three ask primaries died to both readers: meter exchanges (the
    account history at another grain finds them, and a careful reader ties the rest to new permits), the stored
    UEP_PHASE (the schedule's plat units re-derive the phase), and the receipt total repeated per line (counting
    each receipt once); all three stay as mirror devices.

## Retired

task175 retired on 2026-10-19 under the author's rule for this round (a number that dies in its second new cell retires);
no card was ever written or registered. The seed FC46's world died on 2026-10-18 (a member-level capped forecast is a
continuum and the cap cancels), and the redraw round's two cells died on code: human-factors-ergonomics /
human-reliability-assessment (67d2099: the time-reliability race sits inside the window-band filter and divide on rare
trips, and the flattened factor slope is a 7 to 9 per cent lever the audited rows beat) and quantitative-finance /
strategy-backtesting-evaluation (248746c: impact carried across days splits into model classes no one-way execution
record can tell apart, and own borrow demand is a minor line whose attaining band lands). The lesson: a lever that
needs a record the organisation does not keep is a fork, and one the record does keep is a filter and a divide.

## Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired; rebuilt from scratch as architecture 1 in urban-regional-science / land-use-spatial-development-modeling (`## Draw`).
