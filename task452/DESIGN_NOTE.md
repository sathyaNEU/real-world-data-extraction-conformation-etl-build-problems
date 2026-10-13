# task452 design note

Architecture 1, drawn 2026-10-13 (wave 2, oviya1301). The seed (ET09, hospital cost-report peers) is health economics, which task451 holds among the last three draws, so no seed world is kept: the pairing comes from the client's ETL task types.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task452.json`, architecture v1, registered 2026-10-13. `guard.py check` returns WARN only. Each WARN is answered here.
  - `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, 8 of the last 12): the honest label for a load estimator the data select. The mechanism (unsampled days priced through the concentration-discharge relationship) is on no other card.
  - `overuse.org_family` (government_agency) and `overuse.objective` (ETL, the lane's objective): a lake commission is a public body, and the lane is ETL.
  - `overuse.shape` (01, 4 of the last 12): the program funds three projects, so the call is a ranked slate under a cap of three.
  - `test.same_driver_older` against task134 v2 is differentiated on the card. task134 sizes a forward inflow from a conversion hazard by time since entry; this build rebuilds a closed water year's total day by day from a concentration-discharge relationship.
  - The retransformation of a log-scale fit (task135 v1's spent driver) sits here on a lower rung only, never the decisive step.
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
- **Data-native sentence:** in these streams phosphorus rides on storm runoff, so concentration climbs with discharge. The field program's fixed monthly dates land mostly on base flow, and the few storm samples land on whichever storms the laboratory reached. Interpolating or averaging the samples across the year therefore prices the storm days, which carry most of the year's phosphorus, at the wrong concentration, too low where no storm was caught and too high where a caught storm is stretched across the days around it. On a stream whose concentration did not depend on flow, the trap would not exist.
- **Sources, one line each:**
  - `two-layer-task-design.md`, estimation_fit (ratio of totals against mean of ratios; censoring and truncation): the estimator has to fit how the samples were drawn, and here they were drawn mostly at base flow.
  - `strategies.md`, the field's estimator meets the data's process ("checks that see a unit just before resetting it", a yield moving with the base rate): the field program samples on a calendar, while the phosphorus arrives with the storms.
  - `layer1-messiness.md`, Physical & Environmental Sciences (instrument records with qualifiers, provisional against approved data, laboratory units and reporting limits): Layer 1, none of it on the decisive step.
  - task135 v1 (the back-transformed median is not the mean, retired because its default was the golden): its insight is a lower rung here, and the decisive step is upstream of it.
- **Prototype** (scratch `t452/proto1.py`, ten simulated tributaries): against a rating curve corrected for retransformation, interpolation and averaging missed by -38 to +24 per cent in tributary-specific directions. The uncorrected rating curve missed by -4 to -15 per cent, and the corrected variants (with or without seasonal terms, smearing or the normal-theory correction) agreed within about 4 per cent.

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
- Wastewater discharge monitoring reports carry statistical-base codes, resubmitted months, and pounds per day against milligrams per litre.
- Agricultural practice contracts have fields that straddle watershed boundaries.

**Layer 2:** estimation_fit (the estimator fitted to how the samples were drawn). The samples are a flow-selected handful of the year's days, and concentration rises with discharge. The expert prices every unsampled day through the concentration-discharge relationship on the full discharge record, retransformed to the mean.

**Decisive step:** estimating the concentration on the days nobody sampled. The expert estimates it from each day's discharge through a rating curve fitted to the samples, which captures the storm days at storm concentrations. Interpolating or averaging the samples across the year carries base-flow samples over the storms, or stretches one caught storm across the days around it.

**Not semantics:** every field read right (the characteristic names, fractions, units, quality-control types, qualifiers, reporting limits, time zones and the drainage-area ratio) still leaves the unsampled days to be estimated. The default path reads every one of them correctly and interpolates, the method many load reports use, and it funds the wrong three.

**Not rule application:** the agreement files the WHAT (the total phosphorus carried past each compliance station over the water year, and the ranking by kilograms above allocation). No rule names an estimator, an interpolation, a regression or a correction, so executing every filed rule still leaves the default path on the wrong three.

**Analyst test:** a strong analyst who conforms the laboratory results, builds daily discharge from the approved gage records and computes each tributary's load by interpolating the sampled concentrations across the year's days funds Varrow Brook, Orrinwood Brook and Ambrey River (the default path's `Ends on:`). Estimating each day's concentration from its discharge with a rating curve retransformed for the mean funds the right three.

**Estimand:** the commission's phosphorus agreement and its restoration program rules. A tributary's water-year load is the total phosphorus carried past its compliance station from 1 October 2025 to 30 September 2026. The fund takes the three tributaries with the most kilograms of load above their allocations.

**No decoy:** nothing is planted to be caught. No memo, consultant's table, earlier report or preliminary figure states a load, a concentration-discharge relationship or a ranking, and the monitoring program's schedule is the ordinary one its plan describes.

**No certified replay:** no shipped figure is reproduced to recover a method; no load for any water year ships.

**Lesson:** a load is concentration times flow summed over every day, and when concentration depends on flow and the samples miss the storms, the unsampled days are priced through that dependence on the full flow record, not carried over from the nearest samples; no build on file teaches it (the nearest driver on file is task184 at 0.09).

## Tried and rejected

- 2026-10-13, draw: the seed's world (ET09, hospital margin peers from cost reports). Rejected: health economics is task451's pairing among the last three draws; the domain moved to Physical & Environmental Sciences.
- 2026-10-13, draw: population_selection as the strategy, with the gap population and G14 first. Rejected: the guard blocks population_selection against task258 and the triple (population, G14, method selection) against task256; the gap is time (the samples describe their own days, the load the whole year) and the strategy other.
- 2026-10-13, draw: the time gap with G16 first. Rejected: the triple (time, G16, method selection) repeats task501's lineage inside the batch; G14 leads (the sampled concentration does not apply to the storm days).
- 2026-10-13, draw: a designation set (every tributary over its allocation) with an xlsx and png pair. Rejected: both repeat task451; the program's three projects make a ranked slate, delivered as a memo and a CSV.
