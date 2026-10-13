# task452 design note

Architecture 1, drawn 2026-10-13 (wave 2, oviya1301). The seed (ET09, hospital cost-report peers) is health economics, which task451 holds among the last three draws, so no seed world is kept: the pairing comes from the client's ETL task types.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task452.json`, architecture v1, registered 2026-10-13. `guard.py check` returns WARN only. Each WARN is answered here.
  - `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, 8 of the last 12): the honest label for a load estimator the data select. The mechanism (unsampled days priced through the concentration-discharge relationship) is on no other card.
  - `overuse.org_family` (government_agency) and `overuse.objective` (ETL, the lane's objective): a lake commission is a public body, and the lane is ETL.
  - `overuse.shape` (01, 4 of the last 12): the program funds three projects, so the call is a ranked slate under a cap of three.
  - `test.same_driver_older` against task134 v2 is differentiated on the card. task134 sizes a forward inflow from a conversion hazard by time since entry; this build rebuilds a closed water year's total day by day from a concentration-discharge relationship.
  - The retransformation of a log-scale fit (task135 v1's spent driver) is part of the golden method, and no rung turns on it: the uncorrected curve funds the same three.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / Data Extraction & Conformation (ETL). A lake basin's waterborne phosphorus load inventory is put together from three sources: the commission's laboratory results, the gage network's 15-minute discharge and the station register. Each tributary's water-year 2026 load is set against the allocations of the lake's phosphorus agreement. Estimating a load from intermittent concentration samples and a continuous flow record is the field's own work (the regression or rating-curve method of load estimation).
- **Objective:** ETL. The conformed dataset is each tributary's water-year 2026 total phosphorus load on the agreement's basis, with two per-tributary measures beside it.
  - Retrospective by design: the restoration program funds the tributaries that delivered the most phosphorus above their allocations in the closed water year.
  - Not retaggable as Forecasting: no future value is predicted. The open part is the concentration on the days nobody sampled, inside a closed year.
- **Shape:** 01, a ranked slate under a cap of three. Criteria arithmetic (planned; the ask sheet fixes it at design):
  - the slate, 3 named tributaries, plus each tributary's load against its allocation, 10;
  - two per-tributary asks on measures the call does not use: upstream permitted wastewater phosphorus and practice acres under contract, 20;
  - the two files, 2.
  - About 35 in all.
- **Strategy:** other (no listed strategy names it). The samples are a flow-selected handful of the year's days, and concentration depends on flow. The decisive move is how the unsampled days are priced.
- **Mechanism:**
  - Gap: time (decisive: the samples describe the days they were taken on, mostly base flow, while the load is a whole water year), with population supporting (which days the samples represent).
  - Generators: G14 decisive (the sampled concentration does not apply to the unsampled storm days), G16 (the estimator the data select), G17 (the margin, asserted).
  - Gate G: method_or_model_selection. Layer 2: estimation_fit, `own:rating-curve-load-estimation-retransformed`.
- **World:** the Brannoch Lake Commission, a public commission in northern New England that administers the lake's phosphorus agreement among the state, the ten watershed towns and the wastewater permittees.
  - The agreement gives each of the ten monitored tributaries an annual phosphorus allocation at its compliance station.
  - The commission's field program samples each station on a fixed monthly schedule. The Ashgrove College Watershed Laboratory adds a few storm samples a year at most stations.
  - Discharge is recorded every 15 minutes by the commission's gage network, operated under contract by Merrifield Hydrometrics; the approved record for water year 2026 replaced the provisional one in December 2026.
  - Each year the commission's 2027 Tributary Restoration Fund takes on three watershed projects, in the tributaries that delivered the most phosphorus above their allocations in the water year just closed.
- **As-of:** water year 2026 (1 October 2025 to 30 September 2026); the laboratory and gage exports of 8 January 2027; the technical committee's meeting of 21 January 2027 that selects the 2027 projects.
- **Furniture:**
  - Forum committee_or_panel (the commission's technical committee); forcing event budget_or_appropriation (the 2027 Tributary Restoration Fund); organisation government_agency (a public lake commission).
  - Role programme_officer (the commission's water quality program manager; the prompt names no one); context artifact monitoring_export (the laboratory results export); calibration none.
- **People:** drawn with `guard.py names --geo us --seed 452` and `--seed 4521`, on the card: Matthew Douglas (the commission's executive director), Kathy Dominguez (water quality program manager), Troy Ramirez (director of the Ashgrove College Watershed Laboratory), Loretta Soto (hydrologist, Merrifield Hydrometrics).
- **Data-native sentence:** in these streams phosphorus rides on storm runoff, so concentration climbs with discharge. The Commission's fixed rounds (the first and third Tuesdays of each month) land mostly away from storms, and the college's few storm samples land on whichever storms its crews reached. Interpolating or averaging the samples across the year therefore prices the storm days, which carry most of the year's phosphorus, at the wrong concentration, too low where no storm was caught and too high where a caught storm is stretched across the days around it. On a stream whose concentration did not depend on flow, the trap would not exist.
- **Sources, one line each:**
  - `two-layer-task-design.md`, estimation_fit (ratio of totals against mean of ratios; censoring and truncation): the estimator has to fit how the samples were drawn, and here they were drawn mostly at base flow.
  - `strategies.md`, the field's estimator meets the data's process ("checks that see a unit just before resetting it", a yield moving with the base rate): the field program samples on a calendar, while the phosphorus arrives with the storms.
  - `layer1-messiness.md`, Physical & Environmental Sciences (instrument records with qualifiers, provisional against approved data, laboratory units and reporting limits): Layer 1, none of it on the decisive step.
  - task135 v1 (the back-transformed median is not the mean, retired because its default was the golden): its insight is a lower rung here, and the decisive step is upstream of it.
- **Prototype** (scratch, ten simulated tributaries, several seeds): against a rating curve corrected for retransformation, interpolation and averaging missed by tens of per cent in tributary-specific directions, while the rating-curve variants agreed closely. The build's measured ladder is in `## Ladder`, asserted in `checks.py`.

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read the phosphorus agreement and the restoration program: a tributary's water-year load is the total phosphorus carried past its compliance station from 1 October 2025 to 30 September 2026, and the fund takes the three tributaries with the most kilograms above their allocations.
2. Conform the laboratory results: total phosphorus, total fraction, routine samples (quality-control replicates and blanks out), accepted results, one unit, non-detects at half the reporting limit, each station through the register.
3. Build each station's daily mean discharge from the approved 15-minute record, on local days, carried by drainage-area ratio where the sampling station is off its gage.
4. Load: each day's concentration interpolated linearly between the water year's samples, times the day's discharge, summed over the water year.
5. Subtract each allocation, rank the excesses and take the top three.

**Ends on:** fund Varrow Brook, Orrinwood Brook and Ambrey River, the three tributaries the interpolated loads put furthest above their allocations (as designed; the generator places the allocations so the built ladder lands it, asserted in `checks.py`).

**Golden:** fund Kestle River, Hessick River and Varrow Brook, the three whose loads, with each day's concentration estimated from its discharge by a rating curve fitted to the samples and retransformed for the mean, stand furthest above their allocations.

## Stump sentence

The default path funds Varrow Brook, Orrinwood Brook and Ambrey River because step 4 interpolates each tributary's sampled concentrations across the water year's daily discharge, pricing the storm days that carry most of the phosphorus at whatever the nearest samples read (mostly base flow, now and then a caught storm stretched across the days around it); estimating each day's concentration from its discharge through the concentration-discharge rating curve, retransformed for the mean, funds Kestle River, Hessick River and Varrow Brook.

## Three rules

**Task type:** emissions inventory (`emissions-inventory`), serving the ETL objective: a lake basin's waterborne phosphorus load inventory. It is conformed from the commission's laboratory results, the gage network's 15-minute discharge and the station register into each tributary's water-year load against its allocation.

**Domain test:** the deciding quantity is each tributary's annual phosphorus load. Water quality science estimates it from intermittent concentration samples and a continuous discharge record with a concentration-discharge rating curve (the regression method of load estimation), because concentration depends on discharge and fixed-date samples miss the storms that carry the load.

**Swap:** "where the lake commission puts its three restoration projects, by the phosphorus each tributary delivered above its allocation" becomes "where a hospital system puts three quality projects, by the infections each ward recorded above its target". There is no discharge, no concentration that rises with flow, no daily record to price unsampled days on and no rating curve, so the estimation that decides the call has nothing to act on.

**Layer 1:** what these systems produce, none of it on the decisive step.
- The laboratory results come in a water quality exchange layout: characteristic name variants, total and dissolved fractions, mg/L and µg/L after a laboratory change, quality-control replicates and blanks, rejected and preliminary results, and non-detects with their reporting limits.
- Discharge comes as 15-minute values in UTC with provisional, estimated and ice-affected qualifiers, a provisional pull overlapping the approved record, and local water-year days to build.
- Two sampling organisations use their own station identifiers for shared sites, joined through the commission's register.
- One sampling station sits downstream of its gage, its discharge carried by drainage-area ratio.
- Water years run October to September; the program documents are calendar-year.
- Wastewater discharge monitoring reports carry statistical-base codes, monthly and quarterly reporting periods, resubmitted reports, and pounds per day against milligrams per litre.
- The farm practice program's contract export repeats each contract on its enrolled fields' lines, and fields straddle watershed boundaries.

**Layer 2:** estimation_fit (the estimator fitted to how the samples were drawn). The samples are a flow-selected handful of the year's days, and concentration rises with discharge. The expert prices every unsampled day through the concentration-discharge relationship on the full discharge record, retransformed to the mean.

**Decisive step:** estimating the concentration on the days nobody sampled. The expert estimates it from each day's discharge through a rating curve fitted to the samples, which captures the storm days at storm concentrations. Interpolating or averaging the samples across the year carries base-flow samples over the storms, or stretches one caught storm across the days around it.

**Not semantics:** every field read right (the characteristic names, fractions, units, quality-control types, qualifiers, reporting limits, time zones and the drainage-area ratio) still leaves the unsampled days to be estimated. The default path reads every one of them correctly and interpolates, the method many load reports use, and it funds the wrong three.

**Not rule application:** the agreement files the WHAT (the total phosphorus carried past each compliance station over the water year, and the ranking by kilograms above allocation). No rule names an estimator, an interpolation, a regression or a correction, so executing every filed rule still leaves the default path on the wrong three.

**Analyst test:** a strong analyst who conforms the laboratory results, builds daily discharge from the approved gage records and computes each tributary's load by interpolating the sampled concentrations across the year's days funds Varrow Brook, Orrinwood Brook and Ambrey River (the default path's `Ends on:`). Estimating each day's concentration from its discharge with a rating curve retransformed for the mean funds the right three.

**Estimand:** the commission's phosphorus agreement and its restoration program rules. A tributary's water-year load is the total phosphorus carried past its compliance station from 1 October 2025 to 30 September 2026. The fund takes the three tributaries with the most kilograms of load above their allocations.

**No decoy:** nothing is planted to be caught. No memo, consultant's table, earlier report or preliminary figure states a load, a concentration-discharge relationship or a ranking, and the monitoring program's schedule is the ordinary one its plan describes.

**No certified replay:** no shipped figure is reproduced to recover a method; no load for any water year ships.

**Lesson:** a load is concentration times flow summed over every day, and when concentration depends on flow and the samples miss the storms, the unsampled days are priced through that dependence on the full flow record, not carried over from the nearest samples; no build on file teaches it (the nearest driver on file is task184 at 0.09).

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 battery | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| Interpolation of the water year's samples across its days (the default) | no | fires: dated samples beside a complete daily discharge record make the day-by-day fill the obvious table operation | fires: the period-weighted method many load reports use | no | no | no | readable |
| The samples' mean concentration times the year's volume | no | no | fires: the simplest load | no | no | fires: one product | readable |
| The flow-weighted mean of the samples times the volume | no | no | fires: the obvious correction for flow | no | no | no | readable |
| Each month's samples times the month's volume | no | no | fires: a monthly habit | no | no | no | readable |
| (decisive) Each day's concentration from its discharge, through a rating curve fitted to the record's samples and retransformed for the mean | no. The agreement defines the load and names the record's sources (the Commission's samples, the college's storm samples, the gage record); no sentence relates concentration to discharge or names an estimator | no. No column marks storm days or the discharge at sampling; the college's samples carry the same activity type as the Commission's | no. Every reflex above lands wrong | no. No load, earlier report, published curve or ranking ships | no. The battery (units, fractions, quality-control rows, statuses, provisional discharge, time zones) comes back clean on the wrong path | no. A regression on three years' samples, applied to 365 days at each of ten stations | silent |

The decisive quantity is named by no sentence and no column, every reflex lands wrong, no control sees it, and the battery is clean. It is the record's own structure: concentration climbs with discharge at every station (log slopes 0.31 to 0.86), and few samples fall on the high-flow days that carry most of the load.

## Semantic fork table

One row per term of the main ask and per convention its computation rests on. The calls are measured on the build by `checks.py`; each ruling sentence is asserted present in its document.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | water year 2026 | 1 October 2025 to 30 September 2026 | calendar 2026 | refused | agreement 1.1 ("named for the calendar year in which it ends") |
| SF2 | each tributary | its compliance station in Schedule 1 | any station on the stream | refused | agreement 1.2 ("at which the tributary's load is measured") |
| SF3 | phosphorus | total phosphorus, the unfiltered fraction | dissolved phosphorus or orthophosphate | refused | agreement 1.3 ("phosphorus in all forms in an unfiltered sample of stream water, expressed as P") |
| SF4 | water-year load | the mass carried past the station over the year, in kilograms | a mean concentration or a flow-weighted concentration | refused | agreement 1.4 ("carried past a tributary's compliance station during a water year, in kilograms") |
| SF5 | the record | both organisations' samples and the gage record | the Commission's samples only | same call on every golden route (asserted) | agreement 1.4 ("the Commission's samples, the storm samples the Ashgrove College Watershed Laboratory takes...") |
| SF6 | the comparison | unrounded loads | loads rounded to 10 kg first | same call (asserted): no golden excess within 60 kg of zero | agreement 2.2 ("Comparisons under this agreement are made on unrounded loads") |
| SF7 | which three | the most kilograms above allocation | the largest share above allocation | same call (asserted: Varrow, Hessick, Kestle by share) | agreement 3.1 ("exceeds its allocation by the most kilograms") |
| SF8 | three projects | the three largest excesses | fewer, when fewer exceed | same call: five tributaries exceed on every golden route (asserted) | agreement 3.1 ("Where fewer than three tributaries exceed their allocations") |
| SF9 | quality-control samples | routine samples only | replicates and blanks kept | same call (asserted, R2) | the program notes ("Both are reported with their activity type") |
| SF10 | rejected results | accepted results only | rejected kept | same call (asserted, R2) | the program notes ("Result status is Accepted once a result passes review, or Rejected with the reason in the comment") |
| SF11 | July to September discharge | the approved record | the provisional pull | same call (asserted, R2) | the transmittal ("The approved values above replace them") |
| SF12 | a day | the local calendar day | the UTC day | same call (asserted, R2) | the transmittal ("Daily values are means over local calendar days") |
| SF13 | Dunmarsh Brook's discharge | the gage's, carried by the ratio of drainage areas | the gage's as recorded | same call (asserted, R2) | the program notes ("whose gage is 4.2 km upstream; the register gives both drainage areas") |

The stump is none of these readings: the default and the golden read every term the same way and differ only in how the unsampled days' concentrations are estimated.

## Ladder

Measured on the build (world seed 4522) by `checks.py` and recomputed by `verify.py`. Allocations are Schedule 1's; the excess is the water-year load less the allocation, in kilograms; the fund takes the three largest.

| Route | Construction | Funds | Excess on the build (kg) | Killed by |
|---|---|---|---|---|
| R0 (default) | each day's concentration interpolated between the water year's samples, times the day's discharge | Ambrey, Orrinwood, Varrow | Ambrey +310, Orrinwood +280, Varrow +270, Hessick -1,060, Kestle -4,160 | few samples sit on the high flows while concentration rises with discharge: Kestle's top tenth of days carry 63 per cent of its load and 4 per cent of its samples |
| R2 | the samples' mean concentration times the year's volume | Varrow, Orrinwood (two exceed) | Varrow +110, Orrinwood +90 | the same, more so |
| R3 | the samples' flow-weighted mean times the volume | Ambrey, Orrinwood, Varrow | Ambrey +2,660, Orrinwood +1,960, Varrow +700 | weights the caught storms by their own discharge and spreads them over every day |
| R4 | each month's samples times the month's volume | Varrow, Orrinwood, Ambrey | Varrow +210, Orrinwood +150, Ambrey +70 | carries a month's base-flow samples over its storms |
| G1 (golden) | rating curve: log concentration on log discharge with a seasonal cycle, every accepted routine sample of water years 2024 to 2026, smearing | Kestle, Hessick, Varrow | Kestle +2,540, Hessick +1,250, Varrow +1,120; Ambrey +350, Orrinwood +210 | |
| G2 | the same with the normal-theory correction | the same three | Varrow +1,130 against Ambrey +370 | |
| G3 | no seasonal cycle | the same three | Varrow +1,120 against Ambrey +340 | |
| G4 | a quadratic term in discharge | the same three | Varrow +1,210 against Ambrey +350 | |
| G5 | no retransformation correction | the same three | Varrow +950 against Ambrey +160 | |
| G6 | calibrated on water years 2025 and 2026 only | the same three | Hessick +680 against Ambrey +430 | |
| G7 | calibrated on water year 2026 only | the same three | Varrow +920 against Orrinwood +450 | |

**Margins.** The G2 to G7 rows give each route's third against its fourth. On every golden route the third stands at least 244 kg above the fourth (G1 772, G2 764, G3 775, G4 859, G5 785, G6 244, G7 471); on the default the third stands 412 kg above the fourth. No golden excess is within 63 kg of zero (Pellow Brook, the nearest, sits 63 to 96 kg under its allocation).

**The forcing evidence on the build** (figures.json, asserted). Concentration rises with discharge at every station (log slopes 0.31 to 0.86 on the rating curve). Each station's top tenth of water year 2026 days by discharge carry 34 to 63 per cent of its load and hold 4 to 15 per cent of its samples (Kestle 63 and 4, Hessick 60 and 4).

**The grid and the Layer 1 slips** (R2 in `checks.py`, each on the golden route): quality-control rows and rejected results kept, UTC days, Dunmarsh Brook without the drainage-area ratio, and the provisional July to September discharge all fund the same three. Dropping the college's storm samples (the Commission's samples only) funds the same three on every golden route; agreement 1.4 names both organisations' samples as the record. Interpolating the Commission's samples alone funds Varrow Brook only.

**Placement** (build.py `place_allocations`, from the shipped data). Kestle and Hessick sit 12 per cent under their lowest golden-route load. Varrow sits 6 per cent of its load under its interpolated load. Orrinwood and Ambrey sit 5 per cent under the lower of their lowest golden and interpolated loads. The other five sit 8 per cent over the higher of their highest golden and interpolated loads. Allocations are rounded to 10 kg.

**Why the rating curve and not the nearest samples.** A load sums every day's discharge times that day's concentration. The discharge record is complete; the concentration record holds about 26 days a year at each station, few of them on the high flows that carry the load. Where concentration climbs with discharge, the days nobody sampled are priced from that relationship, which the record's own samples define across the range of flows. Carrying the nearest samples across them prices the storms at base flow, or stretches a caught storm across its neighbours.

## Closure table

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | the ten tributaries at their compliance stations; both organisations' samples | filed (1.2, 1.4); SF2, SF5 |
| 2 | Unit of account | kilograms of total phosphorus a water year | filed (1.3, 1.4); SF3, SF4 |
| 3 | Attribution window | the water year, 1 October 2025 to 30 September 2026 | filed (1.1); SF1 |
| 4 | As-of dating | the approved discharge of 14 December 2026; the results export of 8 January 2027 | filed (the transmittal); SF11 |
| 5 | Version basis | approved over provisional discharge; accepted over rejected results | filed (the transmittal, the program notes); C1 (R2) |
| 6 | Divisor and denominator | none: a total | not applicable |
| 7 | Weighting | each day's product of discharge and concentration, summed | filed (1.4: the mass carried past the station) |
| 8 | Measurement window length | the water year for the load; the calibration record water years 2024 to 2026 | C3: one, two or three years of calibration fund the same three (G6, G7 asserted) |
| 9 | Boundary inclusivity | "exceeds" its allocation | C4: no golden excess within 60 kg of zero |
| 10 | Rounding path | unrounded comparison; kilograms and acres to the nearest 10 at the end | filed (2.2; the prompt) |
| 11 | Tie-break | none | C4: the third and fourth are 244 kg apart or more on every golden route |
| 12 | Maturity and censoring | routine total phosphorus has no non-detects; blanks are quality control | C1 |
| 13 | Order of operations | daily mean discharge from the 15-minute record, then the day's concentration, the product and the sum | C1 |
| 14 | Row order | order-free | C1 |
| 15 | Duplicate resolution | replicates are quality control, left out | C1 (R2); SF9 |
| 16 | Identity normalisation | station identifiers by organisation, joined through the register | filed (the register); SF5 |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | milligrams per litre (micrograms converted); cubic feet per second to kilograms a day by 2.4466 | filed (the program notes, the transmittal) |
| 19 | Code and status semantics | activity types, result status, discharge qualifiers | filed (the program notes, the transmittal); SF9, SF10 |
| 20 | Integerisation | none | not applicable |
| 21 | Scope of a stated clause | 3.1 applies to the water year just closed (2026) | filed |
| 22 | Forward window contents | the 2027 projects are chosen on the closed water year 2026; the open part is the concentration on unsampled days, which the estimand includes | filed (1.4) |
| + | Load estimator | each day's concentration from a rating curve on the record's samples, retransformed for the mean | the method, never filed; C3 across seven rating-curve variants, the data separating them from every carried-sample estimator (asserted) |
| + | Ask A: upstream wastewater phosphorus | the facilities whose outfalls are upstream of the station on its stream network while in service, each report at its latest submission, its averages times the days of its monitoring period | filed (4.1(a)); the register's Streams and Facilities sheets place each outfall; each report states its period, and the periods cover the water year once (asserted) |
| + | Ask B: cover crop acres | contracts in force for crop year 2026 at their latest amendment, each enrolled field's own acres shared by the overlay | filed (4.1(b): acres "lying in its watershed"); the export's header (whole fields, the latest amendment in force); contract and field acres agree on every version (asserted) |

## Literal reader

The prompt and the agreement, executed word for word, fix the estimand. It is the mass of total phosphorus carried past each Schedule 1 compliance station from 1 October 2025 to 30 September 2026, in kilograms, estimated from the record: the Commission's samples, the college's storm samples and the gage record. The fund takes the three tributaries with the most kilograms above their allocations, compared unrounded. Every literal reading of those terms selects the same samples and days (SF1 to SF13). The record holds concentration on about 26 days a year at each station and discharge on every day; how the other days' concentration is estimated is filed nowhere. The data force it: concentration climbs with discharge at every station, and few samples fall on the high-flow days (4 to 15 per cent of the samples on the top tenth of days, which carry 34 to 63 per cent of the load). Carrying the nearest samples across the year prices the storms at base flow, and the rating curve the record's samples define, applied to every day, does not. Every rating-curve variant funds the same three. The default's three come from the estimator, not from a reading.

## Oracles

- **What ships no figure.** No file states a load, a rating curve, a concentration-discharge slope, an earlier year's report or a ranking of the tributaries.
- **The lake monitoring** (distractor). In-lake summer phosphorus, chlorophyll and clarity; it attributes nothing to a tributary.
- **The precipitation record** (distractor). Storm timing at three weather stations. It confirms when storms fell, and it neither prices a day nor ranks a tributary.
- **The provisional discharge** (superseded). It differs from the approved record at two gages from 1 August and funds the same three (asserted).
- **The program notes.** They describe the sampling (the Commission's rounds, the college's storm samples when crews can reach the stations). They say nothing about how loads are estimated.
- **The asks' files** (the reports, the contracts, the field overlay, the Streams and Facilities sheets). Read by no step of the call (asserted).

## Ask sheet

**The main call's declared population:** the water quality results (total phosphorus, routine, accepted), the approved discharge (15-minute values for water year 2026, daily values before), the register's Stations sheet, and the agreement's definitions, allocations and Fund rule with Schedule 1. Zero ask device rows in it: the discharge monitoring reports, the contracts, the field overlay and the register's Streams and Facilities sheets are read by no step of the call, and withholding them leaves the call (asserted). Section 4.1 is the asks' clause, and the call does not read it.

**Ask A: each tributary's upstream permitted wastewater phosphorus in water year 2026** (10 figures, to the nearest 10 kg).
- H18 home: agreement 4.1(a), the annual report's line beside each tributary's load, the point-source part of what it carried; the call does not turn on it.
- Use: the committee weighs a nonpoint restoration project against what permitted facilities already discharge upstream.
- Primary device, D8 (a reporting period off the month): twelve of the seventeen facilities, the smaller dischargers, report by calendar quarter. A quarterly report's monthly averages cover the quarter's 90 to 92 days, so multiplying each report by the days in its end month (4.1(a)'s "times the days in the month", executed report by report) counts about a third of their discharge. Every tributary has a quarterly discharger upstream of its station (asserted), so every figure moves. The tells are the reports' start dates and four reports a year against twelve; no sentence names the quarterly reporters, and every report keeps the same columns and statistical base.
- Second device, D7 (a multi-hop network): ten facilities discharge to brooks that join a tributary above its station, so their receiving water names no tributary, and Little Varrow Brook, named for the valley it drains, joins the Ambrey River. The Dunmarsh Brook facility's outfall sits below its station, and the Ambrey Village facility moved its discharge to a new outfall (002), below its station, on 1 April 2026. The register's Streams and Facilities sheets place every outfall, river km measured up each stream from its mouth.
- Hazards: resubmitted reports (the latest replaces the original, 7 reporting periods), daily-maximum rows beside the monthly averages, mass reported in pounds a day at three facilities.
- Path: the reports (11 columns), the register's Facilities, Streams and Stations sheets, agreement 4.1(a). Four sources.
- Stops: the golden (the network, the latest submission, each report times its period's days); each report times its end month's days, 47 to 307 kg off on every tributary; the receiving-water name join, 32 to 462 kg off on every tributary; every submission summed, 3 rows landing.
- Determinism: each report states its monitoring period, and each facility's reports cover every month of the water year exactly once (asserted); 4.1(a) prices each month at the averages of the report covering it.
- Realism: small dischargers monitor nutrients quarterly under their permits, and monitoring report exports carry each report's period; facilities discharge to the small brooks that join the rivers miles upstream.

**Ask B: each watershed's 2026 cover crop acres under the farm practice program** (10 figures, to the nearest 10 acres).
- H18 home: agreement 4.1(b), the annual report's practice line beside each tributary; the call does not turn on it.
- Use: the committee sees the cover crop already in place where a project would go.
- Primary device, D6 (an event's quantity on every line it covers, grain unstated): a contract enrols one to three whole fields, and the contract export repeats the contract's acres on each of its field lines (63 of 115 contract versions enrol more than one field). A line-by-line sum counts a multi-field contract's acres once per field. The tell is cross-file: the overlay gives each field's own acres, which fall short of its line's contracted acres and add up to them across a contract's lines (asserted on every contract version).
- Second device, D6 (an allocation at the wrong weight): each line carries the field's watershed of record, and 52 of 176 enrolled fields straddle a divide; 4.1(b) counts the acres lying in each watershed, which the overlay's shares give.
- Hazards: amendments (18 contracts amended to add or withdraw a field; the latest amendment is the contract in force), contracts outside crop year 2026.
- Path: the contracts (11 columns), the overlay (4 columns), agreement 4.1(b). Three sources.
- Stops: the golden (each enrolled field's own acres shared by the overlay, at the latest amendments); each line's contracted acres shared by the overlay, 372 to 2,126 acres off on every watershed; each line's contracted acres under its watershed of record, 306 to 2,046; each field's own acres under its watershed of record, 19 to 62; every amendment's lines under the watershed of record, 489 to 2,543.
- Determinism: 4.1(b) counts the acres lying in the watershed on fields under contract, and the overlay is the only per-watershed acreage; the export's header says contracts enrol whole fields and the latest amendment is the contract in force; a contract's acres equal its fields' acres in the overlay on every version (asserted), so a line's contracted acres are the contract's.
- Realism: conservation contract exports join each contract to its land units and repeat the contract's fields on every line; programs file each field under one watershed and keep a GIS overlay for the fields that cross a divide.

**Hazard table.** Resubmitted reports and daily-maximum rows (Ask A only, repaired right by the cracker). Amendments and crop years (Ask B only, repaired right). Neither moves the call.

**Referee.** None: no control total ships for either ask.

**Cracker sheet.** The cracker lands the call, runs the hygiene battery and executes every filed rule. For Ask A it walks the register's network, takes each report's latest submission, converts the mass reports and multiplies each report by the days in its end month. For Ask B it follows 4.1(b) to the overlay and the latest amendments, and shares each line's contracted acres by the overlay.

| Row (cracker) | Cracker's figure | Golden | Verdict |
|---|---|---|---|
| A Fallowmere Brook | 30 | 80 | miss |
| A Kestle River | 850 | 1,040 | miss |
| A Orrinwood Brook | 110 | 340 | miss |
| A Tamsell River | 100 | 310 | miss |
| A Varrow Brook | 380 | 480 | miss |
| A Hessick River | 740 | 1,050 | miss |
| A Pellow Brook | 60 | 170 | miss |
| A Ambrey River | 240 | 320 | miss |
| A Dunmarsh Brook | 90 | 280 | miss |
| A Corriden River | 500 | 540 | miss |
| B Fallowmere Brook | 1,290 | 630 | miss |
| B Kestle River | 2,070 | 1,030 | miss |
| B Orrinwood Brook | 2,190 | 1,040 | miss |
| B Tamsell River | 1,060 | 690 | miss |
| B Varrow Brook | 1,590 | 900 | miss |
| B Hessick River | 3,630 | 1,500 | miss |
| B Pellow Brook | 1,630 | 660 | miss |
| B Ambrey River | 2,930 | 1,180 | miss |
| B Dunmarsh Brook | 1,600 | 840 | miss |
| B Corriden River | 1,500 | 750 | miss |

**Mirror sheet.** The mirror stops at the default (Ambrey, Orrinwood and Varrow) and takes the cracker's ask paths. It misses all 20 ask rows and every load row (each interpolated load falls outside its full-record range), keeping the memo's chart form (1 of about 32 ask criteria).

Mirror leakage: 3 per cent of ask weight.

Pair ceiling: 39 (the cracker 38 + 7 + 55 x 0.375 = 65.6, keeping the ten load rows, the chart and the project flags as one criterion; the mirror 3 + 7 + 55 x 0.03 = 11.7).

## Pre-ship check

- **Three rules.** Domain: water quality science's own load estimation, each unsampled day's concentration taken from its discharge through the rating curve the record's samples define (swap test in the Three rules section). Two layers: the Layer 1 inventory (two organisations' results under two station schemes, the laboratory change to micrograms per litre, quality-control rows and rejected results, 15-minute discharge in UTC against local days, the approved record replacing the provisional pull, Dunmarsh Brook's gage below a smaller drainage area; for the asks, reports in two units with resubmissions and daily maxima, contracts with amendments, fields straddling a divide), all of it what the Commission's, the college's, Merrifield's, the facilities' and the program's systems write; and the estimator that prices the unsampled high-flow days, which carries the call. Decisive step analytical: the analyst who conforms everything, applies every filed rule and interpolates the samples funds Ambrey, Orrinwood and Varrow (asserted on the shipped data); changing only the day's concentration to the rating curve funds the golden three (asserted), and every reflex estimator (the sample mean, the flow-weighted mean, the monthly product) stays wrong.
- **Gates.** 13 files in 5 formats (csv, xlsx, pdf, docx, txt), the approved 15-minute discharge at 350,400 rows, two distractors (the weather stations' precipitation and the lake monitoring) the solution never reads; 125 checks; `verify.py` 0 failed from the bundle alone (the golden curve, the four full-record curves' ranges, the default, the forcing evidence, both asks); two builds byte-identical; `figures_check.py` exit 0 (107 figures); `precut.py` exit 0; `leak.py --asof 2027-01-12` REVIEW with no LEAK (Schedule 1's allocations declared as stated inputs); `guard.py heart` WARN (organisation family, objective, shape and Gate G overuse, answered in the Draw; task134 differentiated).
- **Surface pairs.** `guard.py surface` promotes two pairs. task451, back to back at 0.100: the same gap label (time) and nothing else, since task451 completes a claims triangle on received dates across an adjudication change and task452 prices unsampled days through a concentration-discharge relationship; the prompts shared a skeleton ("now that ... are in", "a row per ... showing whether"), so task452's question and file sentences were reworded at stage 3 and share no phrase now. task134 (gap, pattern and Gate G on the cards): differentiated at the draw. The personas in the pack are the card's four.

## Leak check

- `leak.py --asof 2027-01-12` (after the final build, both reader passes appended to the report): REVIEW, no LEAK. The REVIEW lines: digits of Schedule 1's allocations (280 and 660 inside 14,280 and 5,660; the allocations are stated inputs); the agreement's and the transmittal's words beside the call's names (the Fund rule and the gage list); three documents sharing the design's ordinary vocabulary (samples, discharge, record, laboratory, and rating as the gage's stage-discharge rating), none naming the estimator; the register, the agreement, the transmittal and the contracts naming every tributary beside numbers (areas, river km, allocations, gages, acres), none ranking them.
- Reader, pass 1 (isolated, Sonnet, medium, fresh copies of the prompt and the pack): Q1 to Q4 none (1.4 lists the record's sources and names no estimator); Q5 every filed sentence executes to the golden's population (the water year, total phosphorus, the unrounded comparison, local days, the approved discharge, the drainage-area ratio); Q6 an analytical choice. Q8 found two readings in the asks, the river-km datum of an outfall against a station and whether an amendment replaces the contract, both closed in the generator (the register's Streams and Facilities sheets state the datum; the contract export's header says the latest amendment is the contract in force).
- Reader, pass 2 (after the ask layer was rebuilt; same isolation, fresh copies): Q1 to Q4 none; Q5 every filed sentence executes to the golden's population; Q6 an analytical choice; every sweep line harmless. Q8 found two readings in Ask A, 4.1(a)'s days in the month against the quarterly reports and an original report against its resubmission; both left as filed, since the re-judge executed each to the golden (a report stands for the days of its period; the latest received submission replaces the original) and found no fork. Its realism note, a contract's acres repeated on each field line, is the ask's device and an ordinary export join.

## Determinism judge

- Pass 1 (2026-10-13, isolated thread on the cut pack): DETERMINISTIC, FIX_NOW. Every claimed figure reproduced, and the call held on every rating curve it fitted (the normal-theory correction, a quadratic term, no seasonal terms, the Commission's samples alone, an added time trend, shorter fits); Gate G method_or_model_selection, analytical_non_defect; Gate H domain pass, layers pass, decisive step analytical. Its findings: the cover crop acres read either from the contract's watershed column or from the overlay, with no document choosing; the loads to the nearest 10 kg not determinate where curves sit within a kilogram of a rounding edge; a repeated and a missing UTC hour at the clock changes. Repairs, in one generator pass: 4.1(b) counts the acres lying in each watershed; the ask layer rebuilt (quarterly reports, contract acres repeated on field lines, the network and the straddling fields kept as second devices); the loads and excesses given as full-record ranges rounded outward; the 15-minute record continuous in UTC. The call, the ladder and every main-call figure are unchanged (figures.json compared before and after).
- Pass 2 (the one re-judge, on the repaired cut): DETERMINISTIC, APPROVE. Every figure reproduced, the 20 ask rows included (quarterly reports at their period's days, the latest submissions, the network and the relocated outfall; each enrolled field's own acres shared by the overlay at the latest amendments); the call held on every rating-curve variant, the Commission's samples alone and the provisional file used by mistake; Gate G method_or_model_selection, analytical_non_defect; Gate H domain pass, layers pass, decisive step analytical. Its two optional notes went into the answer key only: 10 kg of tolerance at each end of the load ranges, and the sample share stated on water year 2026's samples. Report: `determinism_check_report.md`.

## Tried and rejected

- 2026-10-13, draw: the seed's world (ET09, hospital margin peers from cost reports). Rejected: health economics is task451's pairing among the last three draws; the domain moved to Physical & Environmental Sciences.
- 2026-10-13, draw: population_selection as the strategy, with the gap population and G14 first. Rejected: the guard blocks population_selection against task258 and the triple (population, G14, method selection) against task256; the gap is time (the samples describe their own days, the load the whole year) and the strategy other.
- 2026-10-13, draw: the time gap with G16 first. Rejected: the triple (time, G16, method selection) repeats task501's lineage inside the batch; G14 leads (the sampled concentration does not apply to the storm days).
- 2026-10-13, draw: a designation set (every tributary over its allocation) with an xlsx and png pair. Rejected: both repeat task451; the program's three projects make a ranked slate, delivered as a memo and a CSV.
- 2026-10-13, design: Hessick River at a residual scatter of 0.62, so that a rating curve without the retransformation correction drops it from the slate (a rung for regression-savvy solvers). Rejected: at that scatter Hessick's load moved by up to 18 per cent across defensible rating curves, and calibrating on two years, or dropping the college's storm samples, swapped it for Ambrey River; the scatter is 0.30 like the other streams, and the uncorrected curve funds the golden three.
- 2026-10-13, design: monthly sampling rounds (the second Tuesday). Rejected: with about 14 samples a station in water year 2026, a rating curve calibrated on that year alone moved loads by up to 30 per cent; the Commission samples on the first and third Tuesdays, and every calibration window funds the same three.
- 2026-10-13, design: the agreement's load definition naming the record's start year (water year 2024). Rejected: a sentence telling the solver to estimate one year's load from three years of samples points at a fitted relationship; the definition names the record's sources instead, and the calibration window converges in the data.
- 2026-10-13, design: Orrinwood and Ambrey placed between their rating-curve and interpolated loads. Rejected: their interpolated loads sat under the rating curve's on several seeds, so the default funded only one or two; they sit just under both, and the default's three come from interpolation sinking Kestle and Hessick.
- 2026-10-13, stage 4: the asks' primary devices as first built, the receiving-water name join (Ask A) and the contract's watershed label against the program's overlay (Ask B). Rejected: a careful solver walks the register's stream network, and once 4.1(b) is read to the acres lying in each watershed it takes the overlay, so both asks would have fallen to the cracker; the judge also found the label against the overlay an open reading. The primary devices are now the quarterly reports (each report covering its period's days) and the contract acres repeated on each enrolled field's line, with the network and the straddling fields kept as second devices, and 4.1(b) counts the acres lying in each watershed.
- 2026-10-13, stage 4: the 15-minute record's timestamps converted with each local date's offset. Rejected: it repeated an hour at the spring clock change and dropped one in the autumn (the judge found both); the record runs in UTC from each local midnight, the days of the clock changes holding 92 and 100 values, and the local days are built from the exact switch instants.
- 2026-10-13, stage 4: each tributary's load graded to the nearest 10 kg as a point. Rejected: Pellow, Dunmarsh and Hessick sat within a kilogram of a rounding edge on defensible curves (the judge); the write-up gives each load and excess as its range over the full-record curves, rounded outward to 10 kg.
