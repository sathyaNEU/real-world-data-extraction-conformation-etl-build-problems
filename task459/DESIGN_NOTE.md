# task459 design note

Architecture 1, drawn 2026-10-14 (wave 3, oviya1301), from seed ET16 (a planning team's list of the most efficient gas plants from the generation survey). Kept: the world (gas-fired plants in one footprint, a planning team building a list of them), the decision (which plants make the list) and the quantity (efficiency, read here as carbon dioxide per net megawatt-hour). Not kept: the seed's mechanisms (combined-cycle steam turbines carrying generation and no fuel, CHP fuel, generator fan-out), which are data semantics; they survive only as Layer 1. task456 and task457 wait: no ETL task type is free for their worlds while task453 and task454 hold the last three draws. The call was recut before any review from a scorecard to a capped slate (see `## Tried and rejected`); the analysis, the pack and the asks did not move.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task459.json`, architecture v1, registered 2026-10-14 and updated for the slate call. `guard.py check` and `heart` return WARN only. Each WARN is answered here.
  - `overuse.objective` (ETL, 5 of the last 12): the lane's objective.
  - `overuse.gate_g` (method_or_model_selection, 6 of the last 12): the honest label for a rate the records must be read at the right operating level for. The mechanism (a unit's emission rate as a function of its output, read at the level a commitment fixes) is on no other card.
  - `test.same_driver_older` against task445 (a NOTE): differentiated on the card, as are task230, task256, task114, task33 and task452 (a curve through sparse samples, the nearest insight in the lane). `guard.py surface` promotes the task445 pair on the same signature for the author's adjudicated read. The mechanisms differ: task445 completes a still-open quarter's unreported 13F holders, index sponsors keeping a fixed fraction of each company, with the basis chosen by a filed back-test; here nothing is unreported and nothing is back-tested, and each plant's rate is a non-linear function of its own output that the commitment fixes. A population-decisive card would be honest too, but that signature is spent in eight builds.
  - `surface` people sweep: it reads Ashby Gulch, a plant named for a place, as a persona; no person carries the name.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / Data Extraction & Conformation (ETL). Each offered plant's carbon dioxide per net megawatt-hour is put together from five sources: EPA's hourly emissions records (per combustion-turbine stack), the sellers' revenue meters (per plant), the generator inventory, the unit-to-generator crosswalk and the offers. Building a generating unit's emission rate from hourly heat input, CO2 mass and metered net generation is the power-sector emissions inventory's own work.
- **Objective:** ETL. The conformed dataset is every offered plant's emission rate on the standard's basis (EPA's CO2 against the plant's metered net generation), with two measures beside it; the call fills the district's need from the offers that comply.
  - Forward facing: the commitment runs 2027 to 2036. The rate that decides is the one the plant emits at while delivering its contract capacity, estimated from its 2024 and 2025 records.
  - Not retaggable as Forecasting: no series is projected. The open part is the plant's emission rate at an operating level its records hold in some hours only.
- **Shape:** 01, a ranked list under a cap: the 1,000 MW need filled from the complying offers in order of capacity price, each taken whole, any that would take the total above 1,000 MW passed over. Criteria arithmetic:
  - the call, the megawatts filled and the plants, 2;
  - each complying offer's place in the fill (taken, or passed over with the total it would make), 7;
  - each of the ten offered plants' rate with its verdict, 10;
  - the chart of the ten rates against the 925 line (bars, the line, the signed plants marked), 3;
  - Ask A, each plant's 2025 forced outage hours and forced outages, 20;
  - Ask B, each plant's 2025 operating hours with CO2 from substitute data, 10;
  - the two files, 2.
  - 54 in all.
- **Strategy:** population_selection. The hours that enter the rate are the decision: the commitment's hours (the plant at its Contract Capacity), not the hours of 2025's dispatch. The invariant is the plant's heat input as a function of its output, recorded hour by hour; the closed period's average is not invariant to how the plant was dispatched.
- **Mechanism:**
  - Gap: time (decisive). The records describe the plants as they were dispatched in 2024 and 2025: cycling, part-loaded, and peaking on their duct burners. The commitment holds each plant at its contract capacity in every hour. Population supports it (which hours represent the commitment).
  - Generators: G14 decisive (the rate conditioned on the output level the commitment fixes), G13 (the decision covers an operating regime the closed window did not run), G17 (the margins, asserted).
  - Gate G: method_or_model_selection. Layer 2: estimation_fit, `own:emission-rate-at-committed-operating-level`. Pattern E: the yield (CO2 per MWh) conditioned on output, an absolute split no column names, the confounders (weather, season) controlled by construction.
- **World:** Calder County Public Utility District No. 1, a public power utility in Washington.
  - Its 2026 Baseload Request for Offers needs 1,000 MW for 2027 to 2036 under ten-year unit-contingent agreements, each for a plant's entire output delivered at its Contract Capacity in every hour. Ten gas-fired combined cycles in Washington and Oregon were offered: 3,590 MW, each with a capacity price.
  - The state's emissions performance standard bars a long-term baseload commitment with a plant that emits more than 925 pounds of CO2 per net MWh.
  - The district's procurement procedure RP-7 allows only each plant's own 2024 and 2025 records for its rate (EPA's hourly CO2 as reported, the revenue meter). The request for offers fills the need from the offers that pass every screen in order of capacity price.
  - The board of commissioners approves the commitments.
- **As-of:** the records for 2024 and 2025 (EPA data downloaded 6 October 2026); offers received by 30 September 2026; the evaluation folder of 4 November 2026; the determination dated 6 November 2026 for the board's meeting of 17 November 2026.
- **Furniture:**
  - Forum board_of_directors (the district's board of commissioners); forcing event purchase_order_or_contract (the ten-year agreements); organisation utility_or_infrastructure (a public utility district).
  - Role capacity_planner (the district's manager of resource planning; the prompt names no one); context artifact none (the sellers' capability tests went with the scorecard; the offers log is an operating extract the call reads and the generator inventory a lookup); calibration none.
- **People:** drawn with `guard.py names --geo "United States" --seed 459`, on the card: Victor Carr (the district's general manager), Adrian Dunn (manager, resource planning), Julie Jackson (environmental compliance specialist). Christine Burke and Lisa Howell were drawn and set aside (first names on older builds).
- **Data-native sentence:** a gas combined cycle burns more fuel per megawatt-hour at part load and in the hours after a start, and its duct burners add output at a far higher heat rate than the turbines. Plants that cycled through 2024 and 2025 carry those hours in their annual averages. The baseload commitment holds each plant at its contract capacity in every hour: a level the cycling plants held only in their best hours, and one Tamarack Landing reaches only with its duct burners firing.
- **Sources, one line each:**
  - `two-layer-task-design.md`, estimation_fit (the data's real structure; ratio of totals): the rate is a ratio of totals over hours whose operating levels the commitment changes.
  - `strategies.md` "the field's estimator meets the data's process": the invariant is the unit's input-output relation, recorded hourly; the generic move carries the period average.
  - `layer1-messiness.md`, Physical & Environmental Sciences and Energy (instrument records with method codes, standard against prevailing time, gross against net, prime-mover grain): Layer 1, none of it on the decisive step.
  - task452 (a concentration-discharge curve through sparse samples): the nearest insight in the lane. Here every hour is recorded, and the error is the operating level, not the sampling.
- **Generator** (`task459/generator/`, world seed 4591207):
  - Each plant is simulated hour by hour through two years of its zone's weather. Its dispatch style sets the operation: base, daily cycling, seasonal or mid-merit.
  - Its heat input rises at part load (a part-load curve), carries start-up fuel scaled to how long the plant was off, and adds duct firing at 10,500 to 10,950 Btu/kWh over heavy-load hours on hot and cold days.
  - Forced, maintenance and planned outages are written as GADS events, and reserve shutdowns come from the dispatch.
  - Station service runs while online and is drawn while idle.
  - The build's measured ladder is in `## Ladder`, asserted in `checks.py` and recomputed by `verify.py`.

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read the request for offers and RP-7: a baseload commitment may be signed only with a plant whose CO2 per net MWh is at or below 925 pounds; each offer names a plant, a Contract Capacity and a capacity price; the 1,000 MW need is filled from the complying offers in price order, each taken whole, passing over any that would take the total above 1,000 MW.
2. Conform the hourly emissions records: each monitored stack to its plant by facility ID (the offers' EIA plant codes, two matched by name), CO2 short tons to pounds, every reported hour kept.
3. Net generation: the revenue meter per plant per hour (or the survey's net generation), 2025.
4. Rate: the plant's 2025 CO2 over its 2025 net generation.
5. The plants at or below 925 comply: Tamarack Landing, Juniper Draw, Moraine Point, Ochre Flat and Lindgren Hill.
6. Fill the need from them in price order: Tamarack Landing (630 MW) taken; Juniper Draw passed over; Moraine Point (275 MW) taken; Lindgren Hill and Ochre Flat passed over.

**Ends on:** Tamarack Landing and Moraine Point, 905 MW of the 1,000 MW need; Sorrel Butte, Kessling Creek, Ashby Gulch, Brenmoor Mill and Coldbrook turned down on the standard.

**Golden:** Juniper Draw, Kessling Creek and Ashby Gulch, 990 MW of the 1,000 MW need, each plant's rate read at its Contract Capacity from the hours it ran at that output: seven comply, Tamarack Landing, Brenmoor Mill and Coldbrook do not, and the fill passes over Sorrel Butte, Moraine Point, Lindgren Hill and Ochre Flat.

## Stump sentence

The default path fills the need with Tamarack Landing and Moraine Point, 905 MW, because it rates each plant on its 2025 annual CO2 per net MWh. That average carries the cycling plants' starts and part-load hours, and Tamarack Landing's mostly unfired base operation, into a commitment that holds every plant at its Contract Capacity in every hour. Read at that output, Sorrel Butte, Kessling Creek and Ashby Gulch sit well under 925 pounds, and Tamarack Landing, firing its duct burners in every hour to reach its Contract Capacity, sits above it; the same fill then takes Juniper Draw, Kessling Creek and Ashby Gulch, 990 MW.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory (serves ETL in the client taxonomy): a plant-level CO2 inventory built from hourly monitoring records, revenue meters and the generator inventory, conformed into each offered plant's emission rate.
Domain test: the quantity that decides is each plant's CO2 per net MWh at its committed output. Emissions accounting for generating units estimates it from hourly CO2 mass (calculated from heat input) against metered net generation, read at the operating level, because a gas unit's heat rate falls with load, carries start-up fuel and rises once duct burners fire.
Swap: "fill the bed need from the hospitals whose cost per discharge at the contracted volume is at or below the cap" has no heat input, no part-load heat rate, no start-up fuel, no duct burner and no station service drawn while idle. The hourly records the rate is read from have no counterpart, so the task stops reading.
Layer 1: each item below comes from the system that writes it.
- Hourly monitoring per turbine stack, in local standard time, with method-coded substitute hours (the operators' data acquisition systems, EPA's export).
- Two stacks at the four two-turbine plants, summed to the plant by facility ID (EPA's unit grain).
- A stack renumbered at a monitor replacement (the monitoring plan).
- Revenue meters per plant: each hour's start in local time with its UTC offset, negative while the plant draws station service (the meter data systems).
- Offers under trade names, two without an EIA plant code (the sellers).
- The generator survey's combined-cycle rows and co-located peakers (EIA).
- GADS records unit by unit in UTC (the sellers' reporting systems; ask path).
Layer 2: estimation_fit. A plant's emission rate is a function of its output level; the commitment fixes the level, so the rate must be read at it, not carried from the closed period's average.
Decisive step: estimate each plant's CO2 per net MWh at its offered Contract Capacity from the hours its records hold at that output, instead of its 2025 annual average.
Not semantics: with every field read right, the annual average is still the easy route and still files the wrong plants. The fields are gross against net, short tons, standard against prevailing time, the stacks per plant, the renumbered stack, the substitute hours and the offers without codes.
Not rule application: RP-7 files the estimand (CO2 per MWh of net generation delivered under the commitment), the records and the threshold; the request for offers files the delivery (Contract Capacity in every hour) and the fill. No filed rule says how a rate at a committed output is estimated. Executing every filed rule, the fill included, on the annual average takes Tamarack Landing and Moraine Point.
Analyst test: a strong analyst conforms the records, aligns them with the meters, rates each plant on its 2025 CO2 per net MWh and fills the need by the request for offers' rule. That route takes Tamarack Landing and Moraine Point, 905 MW (the default path's Ends on); read at the Contract Capacities the same rule takes Juniper Draw, Kessling Creek and Ashby Gulch, 990 MW.
Estimand: CO2 per MWh of net generation the plant delivers under the commitment, against 925 pounds, per offered plant, compared unrounded. The commitment is the plant's entire output, its Contract Capacity in every hour of the term outside planned and forced outages. Filed in RP-7 5.1 to 5.4 and the request for offers 1.1, 3.1 to 3.3 and 5.2.
No decoy: nothing is planted. No memo, draft, seller attestation, published rate or prior determination states or argues for any plant's rate; RP-7 5.3 allows only the plant's own records.
No certified replay: no certified, published or prior rate for any plant ships, and the method is not recovered by reproducing one.
Lesson: a generating unit's emission rate belongs to the operating level it was measured at. When a commitment fixes the level, the rate is read at that level, since part load, starts and supplementary firing all move it. No build on file teaches it.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 battery | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| The 2025 annual CO2 over 2025 net generation (the default) | no | fires: annual totals sit in the survey and sum from the hourly files | fires: the plant emission rate every inventory publishes | no | no | fires: one ratio of two totals | readable |
| The 2025 average without start-up and shutdown hours | no | fires: the partial operating time column | fires: the cleaning reflex | no | no | fires: one ratio | readable |
| The rate in the plant's highest-output hours | no | no | fires: the full-load reflex once load is noticed | no | no | no | readable |
| (decisive) Each plant's rate at its offered Contract Capacity, from the 2024 and 2025 hours its meter shows it delivering that capacity | no. RP-7 5.2 files what is measured (CO2 per MWh of net generation delivered under the commitment) and the request for offers what the commitment delivers; no sentence relates a plant's rate to its output, names an hour selection or a curve | no. No column marks hours at the Contract Capacity, starts as such, or duct firing; the generator survey's duct burner flag says a plant has them, not that its offer needs them | no. Every reflex above lands wrong (905, 905 and 775 MW) | no. No published rate, prior determination or seller heat rate ships | no. Keys, joins, clocks and duplicates come back clean on the wrong path | no. An hourly match of EPA's CO2 to the meter's net output, selected by output, plant by plant | silent |

The decisive quantity is named by no sentence and no column, every reflex lands wrong, no control sees it and the battery is clean. It is the records' own structure: below 75 per cent of their Contract Capacities the four daily cyclers emit 14 to 20 per cent more per megawatt-hour than at them (asserted), and Tamarack Landing's Contract Capacity lies above its unfired output in every season.

## Semantic fork table

One row per term of the main ask and per convention its computation rests on. The calls are measured on the build by `checks.py`; each ruling sentence is asserted present in its document.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | an offer's capacity | the Contract Capacity, net MW at the point of interconnection | nameplate or tested capability | refused | request for offers 3.3 ("the net capacity, in megawatts at the Resource's point of interconnection") |
| SF2 | under the standard | rate at or under 925 | strictly under 925 | same call (asserted: no rate within 30 lb of 925) | RP-7 5.4 ("A plant complies if its emission rate does not exceed the standard") |
| SF3 | emission rate | CO2 per MWh of net generation delivered under the commitment | per gross MWh; per MWh of 2025 operation | refused | RP-7 5.2 ("per megawatt-hour of net generation it delivers under the commitment") |
| SF4 | the standard's gases | carbon dioxide | CO2e with methane and nitrous oxide | refused | RP-7 5.1 ("the District applies the standard to carbon dioxide") |
| SF5 | the records | 2024 and 2025 | 2025 alone | same call (asserted) | RP-7 5.3 ("for calendar years 2024 and 2025") |
| SF6 | substitute data | included as reported | left out | same call (asserted, R2) | RP-7 5.3 ("substitute data included as reported") |
| SF7 | net generation | the revenue meter's | the generation survey's | refused for an hourly rate (the survey is monthly); same default slate (asserted) | RP-7 2.4 ("as measured by its revenue meter") |
| SF8 | the plant | every unit offered, both stacks of a two-turbine plant, duct burners within the stacks' records | one stack | refused | RP-7 2.3 ("the generating units offered under one offer, with the equipment serving them") |
| SF9 | rounding | unrounded comparison | rates rounded first | same call (asserted) | RP-7 5.4 ("Rates are compared unrounded") |
| SF10 | filling the need | each offer whole, any offer that would take the total above 1,000 MW passed over and the next considered | stop at the first offer over the need (Juniper Draw alone); fill past the need (Juniper Draw and Sorrel Butte) | refused (asserted) | request for offers 5.2 ("taking each offer whole and passing over any offer that would take its total above 1,000 MW") |
| SF11 | under the commitment | the Contract Capacity in every hour | the plant's own dispatch | refused | request for offers 3.2 ("deliver the Contract Capacity to the District in every hour of the Delivery") |
| SF12 | the hour | EPA's local standard hour, the meter's start with its offset | the meter's local clock read as standard | same call (asserted, R2: Tamarack Landing 955) | the dictionary ("Date and Hour in local standard time"; the meter's "-08:00 standard time, -07:00 daylight time") |
| SF13 | whose output | the plant's entire output | a slice, the rest sold elsewhere | refused | request for offers 3.1 ("Each offer is for the entire output of one plant") |
| SF14 | the price order | the 2027 capacity price, lowest first | the price levelized over the term with each offer's escalation | same call (asserted: every complying offer escalates at 2.0 per cent; no two prices tie) | request for offers 5.2 ("in order of capacity price, lowest first") |
| SF15 | the need | 1,000 MW of baseload capacity | the 3,590 MW offered | refused | request for offers 1.1 ("The District needs 1,000 MW of baseload capacity and energy") |
| SF16 | the standard's reach | every offer, each agreement a commitment for baseload electric generation | the cycling plants (capacity factors of 23 to 29 per cent) not baseload generation, so outside the standard | refused | request for offers 1.2 ("Each agreement under this request is a long-term financial commitment for baseload electric generation") |
| SF17 | the records for the rate | the plants' 2024 and 2025 records as what may be used for the rate 5.2 defines | the rate as every 2024 and 2025 hour pooled, read as 5.3's own computation | refused: 5.3 says which records may be used, 5.2 what the rate is | RP-7 5.3 ("Only the plant's own records may be used to determine its emission rate") |
| SF18 | a complete offer | the three items of the data package, which every offer has | an offer without its EIA plant code incomplete (it would drop Kessling Creek and Ashby Gulch, 775 MW) | refused | request for offers 4.1, the package's last item ("(c) the Resource's planned outages for 2027.") |

The stump is none of these readings: the default and the golden read every term the same way and differ only in the operating level the rate is read at.

## Ladder

Measured on the build (world seed 4591207) by `checks.py` and recomputed by `verify.py`. Rates in pounds of CO2 per net MWh; the commitment truth holds each plant at its Contract Capacity through the two years' weather in the generator (no mess).

| Plant | Offer | MW | Price ($/kW-mo) | Golden | Golden family | 2025 annual | 2024 and 2025 | No starts | Top output | Commitment truth |
|---|---|---|---|---|---|---|---|---|---|---|
| Tamarack Landing | BL26-01 | 630 | 11.40 | 971 | 957 to 985 | 902 | 904 | 902 | 974 | 950 |
| Juniper Draw | BL26-02 | 500 | 11.55 | 890 | 886 to 891 | 885 | 887 | 885 | 940 | 893 |
| Sorrel Butte | BL26-03 | 530 | 11.80 | 892 | 889 to 893 | 998 | 996 | 946 | 879 | 888 |
| Coldbrook | BL26-04 | 415 | 10.40 | 982 | 978 to 984 | 972 | 973 | 971 | 970 | 986 |
| Moraine Point | BL26-05 | 275 | 12.25 | 876 | 872 to 877 | 862 | 862 | 861 | 859 | 875 |
| Ochre Flat | BL26-06 | 315 | 16.20 | 791 | 788 to 792 | 779 | 779 | 778 | 777 | 792 |
| Lindgren Hill | BL26-07 | 265 | 13.10 | 876 | 875 to 878 | 893 | 892 | 882 | 858 | 876 |
| Ashby Gulch | BL26-08 | 245 | 12.40 | 885 | 882 to 887 | 986 | 985 | 941 | 900 | 882 |
| Kessling Creek | BL26-09 | 245 | 12.10 | 884 | 882 to 887 | 989 | 990 | 946 | 868 | 887 |
| Brenmoor Mill | BL26-10 | 170 | 9.80 | 1,064 | 1,064 to 1,067 | 1,162 | 1,157 | 1,118 | 1,054 | 1,067 |

| Route | Construction | Complying | Slate | MW | Killed by |
|---|---|---|---|---|---|
| R0 (default) | 2025 CO2 over 2025 net generation | Tamarack Landing, Juniper Draw, Moraine Point, Ochre Flat, Lindgren Hill | Tamarack Landing, Moraine Point | 905 | the average carries the 2025 dispatch: 144 to 157 starts and the part-load hours at the three cycling plants; Tamarack Landing's mostly unfired base load |
| R0b | the same over 2024 and 2025 | the same five | the same | 905 | the same |
| R1 | the 2025 average without start-up and shutdown hours | the same five | the same | 905 | the part-load hours stay: Sorrel Butte, Kessling Creek and Ashby Gulch 941 to 946 |
| R2 | the hours at 95 per cent or more of the plant's highest hourly output | Sorrel Butte, Kessling Creek, Ochre Flat, Lindgren Hill, Ashby Gulch, Moraine Point | Sorrel Butte, Kessling Creek | 775 | Juniper Draw's highest hours are duct-fired (940), but its offer is its unfired capability |
| G (golden) | the hours (2024 and 2025) the meter shows the plant delivering its Contract Capacity within 2 per cent, every stack operating the full hour | Sorrel Butte, Kessling Creek, Ochre Flat, Juniper Draw, Lindgren Hill, Ashby Gulch, Moraine Point | Juniper Draw, Kessling Creek, Ashby Gulch | 990 | |
| G family | windows of 1, 3 and 5 per cent; 2025 alone; a quadratic of hourly CO2 on output from 80 per cent of the Contract Capacity; a straight line from 90 per cent; the mean of the hourly rates in the window | the same seven on every variant, each plant's rate inside its graded range | the same | 990 | |
| Verdict variants | the hours at or above the Contract Capacity (output the commitment never calls for); the median of the hourly rates (an emission rate is a ratio of totals) | the same seven | the same | 990 | rates outside some graded ranges |

**The grid of the two corrections** (asserted). Reading the cyclers at their Contract Capacities and reading Tamarack Landing there are separate moves; each half alone files its own wrong slate.

| Cyclers at the Contract Capacity | Tamarack Landing at the Contract Capacity | Slate | MW |
|---|---|---|---|
| no | no | Tamarack Landing, Moraine Point (the default) | 905 |
| yes | no | Tamarack Landing, Kessling Creek | 875 |
| no | yes | Juniper Draw, Moraine Point | 775 |
| yes | yes | Juniper Draw, Kessling Creek, Ashby Gulch (the golden) | 990 |

**Position and separation.** Every route names its own slate, and none shares the golden's plants or megawatts (asserted). The decisive step reverses the default on four plants. Sorrel Butte, Kessling Creek and Ashby Gulch go in, 998, 989 and 986 down to 892, 884 and 885. Tamarack Landing goes out, 902 up to 971, and with it the cheapest complying offer on the default's list. R2 reverses Juniper Draw the other way, which hands the first place in the fill to Sorrel Butte.

**Margins.** Every golden-family rate is at least 32 pounds from 925 (Tamarack Landing's lowest variant 957). Every default rate is at least 22 pounds from it (Tamarack Landing, 902). Each plant's Contract Capacity holds 294 to 1,020 hours of its record. In the golden fill, every complying offer passed over would take the total to at least 1,020 MW.

**The forcing evidence on the build** (asserted). Below 75 per cent of their Contract Capacities, the four daily cyclers' rates are 14 to 20 per cent above their rates at them (Sorrel Butte 16.0, Kessling Creek 20.1, Ashby Gulch 17.2, Brenmoor Mill 14.2). Tamarack Landing's 630 MW Contract Capacity sits in the top tenth of its hourly output and above its unfired output at every temperature in the record, so every one of its 327 hours at that output is duct-fired.

**The clean-truth test** (R3 in `checks.py`). On the generator's truth (true heat input, no substitute data, no clock or key mess), the easy route signs the default's five and the decisive step alone signs the golden seven. The plants held at their Contract Capacities through the two years' weather also sign the golden seven. Each lower rung (no starts, top output) stays on its wrong list.

**The Layer 1 slips** (R2 in `checks.py`, each on the golden route): each keeps the same seven, and so the same slate.
- The meter's UTC offsets dropped (daylight time read as standard; Tamarack Landing 955).
- Partial operating hours kept in the window.
- Substitute-data hours left out.
- The two offers without codes matched by name and county.
- Moraine Point's renumbered stack: one facility and one series either way.
- The idle hours' negative readings dropped from the default leave its five.

**Why the rate at the Contract Capacity and not the year's average.** A plant's CO2 per megawatt-hour is a property of the output it runs at, not a constant. The 2025 average is the rate of 2025's dispatch: daily starts and part-load hours at the cycling plants, unfired base load at Tamarack Landing. The commitment replaces that dispatch with the Contract Capacity in every hour. The records hold hundreds of hours at each plant's Contract Capacity, and RP-7 rates the plant on what it delivers under the commitment.

## Closure table

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | the ten offers received, each a plant's entire output | filed (request for offers 3.1; the offers log); SF13 |
| 2 | Unit of account | pounds of CO2 per MWh of net generation; capacity in MW at the point of interconnection | filed (RP-7 5.1, 5.2, 2.4; request for offers 3.3); SF1, SF3 |
| 3 | Attribution window | the commitment's operation, estimated from the 2024 and 2025 records | filed (RP-7 5.2, 5.3; request for offers 3.2); SF5, SF11 |
| 4 | As-of dating | EPA data downloaded 6 October 2026, 2025 fourth quarter included; offers of 30 September 2026 | filed (the dictionary, the offers log) |
| 5 | Version basis | EPA's hourly CO2 as reported, substitute data included | filed (RP-7 5.3); SF6 |
| 6 | Divisor and denominator | net generation at the revenue meter in the same hours | filed (RP-7 2.4, 5.3); SF7 |
| 7 | Weighting | a ratio of totals over the selected hours | C1: the curve variants give the same verdicts (asserted) |
| 8 | Measurement window length | 2024 and 2025 | filed (RP-7 5.3); C3: 2025 alone gives the same seven |
| 9 | Boundary inclusivity | at or under 925 complies; a total at or under 1,000 MW is within the need | filed (RP-7 5.4; request for offers 5.2); C4: no rate within 30 lb, no slate at 1,000 MW |
| 10 | Rounding path | unrounded comparison; rates to the pound, hours to the hour at the end | filed (RP-7 5.4; the prompt) |
| 11 | Tie-break | none needed: no two offers share a capacity price | C4 (asserted) |
| 12 | Maturity and censoring | none: the records are final for 2024 and 2025 | filed (the dictionary: fourth-quarter submissions included) |
| 13 | Order of operations | stacks summed to the plant each hour, matched to the meter's hour, then selected and summed; the standard screened before the fill | C1; filed (request for offers 5.1, 5.2) |
| 14 | Row order | the fill in order of capacity price, lowest first | filed (request for offers 5.2); SF14 |
| 15 | Duplicate resolution | none on the call's path (one row per stack-hour, one per offer-hour) | C1 (asserted: no repeated key) |
| 16 | Identity normalisation | facility ID equals the EIA plant code; two offers matched by name and county; the renumbered stack within its facility | filed (the dictionary); R2 asserted |
| 17 | Netting against gross | net generation, negative while idle | filed (RP-7 2.4; the dictionary) |
| 18 | Dimensional units | short tons to pounds (2,000); MWh; $/kW-month | filed (EPA's header; the offers log) |
| 19 | Code and status semantics | operating time, measure indicators, GADS event types | filed (the dictionary) |
| 20 | Integerisation | each offer taken whole | filed (request for offers 3.1, 5.2); SF10 |
| 21 | Scope of a stated clause | the standard applies to every offered plant; the fill to the offers that pass every screen | filed (RP-7 5.1, 5.5; request for offers 5.2) |
| 22 | Forward window contents | the term's operation is the Contract Capacity in every hour; planned and forced outages carry no delivery and no emissions | filed (request for offers 3.2) |
| + | The rate under the commitment | the hours at the Contract Capacity, a ratio of totals | the method, never filed; C3 across the windows, years, curves and the mean of hourly rates, every plant's graded figure a range over them (asserted), the data separating them from every period-average route; the hours at or above and the median give the same verdicts |
| + | Ask A: forced outage hours and outages | the hours in 2025 the whole plant was off line on a forced event (U1, U2, U3, SF), which is when every combustion turbine (or the single-shaft unit) is out; each unit's current entry for an outage; the count of such outages | filed: the dictionary (forced types; "Days and years in the evaluation are Pacific time"; "An outage takes a unit, or a whole plant, off line; a derate leaves it running below its net maximum capacity"); the current entry: C1 where a later entry extends an earlier one, and where a first estimate ran long EPA's hours show the plant operating inside it (asserted), so only the later entry fits the records; no plant outage runs into 2025 (asserted) |
| + | Ask B: clock hours with CO2 resting on substitute data | 2025 clock hours (local standard time) in which an operating stack's heat input came from substitute data | the ask names clock hours; the monitoring plans file CO2 by Appendix G, calculated from heat input; the dictionary files the measure indicators |

## Literal reader

The prompt, RP-7 and the request for offers, executed word for word, fix the estimand. For each of the ten offers, it is the pounds of carbon dioxide the plant emits per megawatt-hour of net generation it delivers under the commitment, against 925 pounds, compared unrounded. The commitment is the plant's entire output, delivered at its Contract Capacity in every hour of 2027 to 2036 outside planned and forced outages. RP-7 5.3 fixes the evidence: EPA's hourly CO2 as reported and the revenue meter, 2024 and 2025. The request for offers fixes the need (1,000 MW) and the fill: the offers that pass every screen in order of capacity price, each whole, passing over any that would take the total above 1,000 MW. Every literal reading of those terms selects the same plants, units, hours and order (SF1 to SF18).

The records do not hold the commitment; they hold the plants as they were dispatched. The data show a plant's CO2 per megawatt-hour moving with its output: 14 to 20 per cent higher below 75 per cent of the Contract Capacity at the four daily cyclers, and higher where duct burners fire. The literal estimand is therefore the rate at the Contract Capacity, and the records hold that rate directly in the 294 to 1,020 hours each plant ran there. Every window, year and curve gives the same seven and the same 990 MW, with each plant's rate inside its graded range; the hours at or above the Contract Capacity give the same seven too. The asks read the same way: the dictionary files the year (Pacific), what a plant outage is (the whole plant off line) and the forced types, and the ask names clock hours and CO2 resting on substitute data. The 2025 average is the rate of 2025's dispatch, a different quantity on the same files. The default's slate comes from that estimator, not from a reading.

## Oracles

- **What ships no figure.** No file states a plant's emission rate, heat rate, a prior determination or a ranking of the plants on the standard; RP-7 5.3 allows only the plant's own records.
- **The offers log** (an operating extract the call reads). Each offer's plant, Contract Capacity, capacity price and escalation, in the order the offers were logged; it says nothing about emissions, so it ties under every rate basis.
- **The generation survey** (distractor). Monthly fuel and net generation by prime mover. Its annual ratios reproduce the default's list, but it is the 2025 dispatch's rate, the same wrong basis as the default. It ranks nothing and states no rate. It cannot give an hourly rate.
- **The 2027 planned outages** (distractor). The sellers' scheduled outages; they carry no delivery and no emissions and move nothing.
- **The GADS records** (Ask A) and the substitute-data indicators (Ask B). Read by no step of the call (asserted).

## Ask sheet

**The main call's declared population:** EPA's hourly CO2 mass and operating time per stack (2024 and 2025), the revenue meters, the offers log (Contract Capacity and capacity price), the generator inventory's plant names (for the two offers without codes), RP-7 and the request for offers. Zero ask device rows in it: the GADS records are read by no step of the call, and the measure-indicator columns of EPA's file are read by no step of the call. Withholding them leaves the call and every rate (asserted).

**Ask A: each offered plant's forced outage hours and forced outages in 2025** (20 figures, whole hours and counts).
- H18 home: a measure every candidate carries that the call does not turn on. A baseload commitment pays for capacity the plant must deliver every hour, so forced outages are the commitment's undelivered hours.
- Use: the board weighs each plant's reliability beside its rate.
- WHAT, filed: the dictionary's forced types (U1, U2, U3, SF), its Pacific year, and "An outage takes a unit, or a whole plant, off line; a derate leaves it running below its net maximum capacity". The plant's hours in an outage are the hours it was off line.
- Construction: each unit's current entry for each outage, merged in time; the plant off line when every combustion turbine (or the single-shaft unit) is out; the hours in 2025 Pacific time and the merged outages.
- Primary device, D6 with a domain effect (an event's quantity on every line it covers, and which unit's loss takes the plant off line). The sellers log unit by unit: a plant trip is a forced entry on every unit's line, while a single turbine's trip at a two-turbine plant, or a steam turbine's at a plant whose turbines can bypass their steam generators, leaves the plant running (a forced derate on the steam turbine's line beside the first). Summing the lines counts each trip two or three times; the union of the plant's lines counts every single-unit trip as plant time. Seven plants' figures move.
- Second device, D2 (the record is the latest entry, not the widest). An outage's entries share its start. Where an outage ran past its first estimate, the later entry extends it (the union and the latest entry agree). At Moraine Point, Ochre Flat and Kessling Creek the first entry estimated a return to service days after the unit was back, past the plant's next forced outage, and the entry made after the outage gives its actual end; the union of entries runs the two outages together, over-counting the hours and under-counting the outages. EPA's records show each plant operating inside the first estimate (218, 104 and 33 hours, asserted), so only the later entry fits.
- Hazards: reserve shutdowns, planned and maintenance outages and derates in the same file (seen; the dictionary types them); times in UTC against the dictionary's Pacific year (Moraine Point's outage from New Year's Eve 2025).
- Path: the GADS records (11 columns), the dictionary, EPA's hourly file (to see the plant running), the generator inventory (configuration), the offers log; five files.
- Stops: the golden; the line sum (every figure off); the union of the plant's forced lines (every figure off); the intersection without the current entries (Moraine Point, Ochre Flat and Kessling Creek off); the UTC calendar (Moraine Point off).
- Determinism: no plant's hours within 0.15 of a rounding edge (asserted); outages separated by at least two hours; the current entries give the generator's true forced hours at every plant (asserted).
- Realism: GADS data are reported by unit; a plant trip is a forced outage on each unit, and an outage log keeps an entry for each estimate of return to service.

**Ask B: the clock hours each plant operated in 2025 with its CO2 resting on substitute data** (10 figures, whole hours).
- H18 home: the audit trail of the input the call consumes. The rate rests on EPA's CO2 as reported, substitute data included (RP-7 5.3); the board sees how much of each record rests on substituted values.
- Use: the board's auditor reads how far each determination rests on substituted data.
- WHAT: clock hours (named in the ask) in 2025 in which a monitored unit operated with its CO2 resting on substitute data. EPA calculates a gas unit's CO2 from its heat input (40 CFR 75 Appendix G, filed in the monitoring plans), so substituted heat input is CO2 resting on substitute data.
- Primary device, D3 with a domain effect (two columns one word apart). The CO2 mass measure indicator reads Calculated in every operating hour of every plant, because the CO2 is calculated; the substitution sits in the heat input measure indicator. Reading the CO2 column's own indicator gives zero at every plant.
- Second device, D6 (grain). At the four two-turbine plants a data acquisition outage substituted both stacks at once; counting stack rows counts those clock hours twice.
- Hazards: NOx monitor substitutions in the NOx rate indicator (counting any substitute flag over-counts every plant); non-operating hours carry no indicators.
- Path: EPA's hourly file (5 columns), the monitoring plans, the dictionary; three files.
- Stops: the golden; the CO2 indicator (zero everywhere); stack rows (the four two-turbine plants over by 2 to 20); any substitute flag (every plant over, 22 to 129).
- Realism: Part 75 gas units calculate CO2 from heat input, and EPA's export flags each parameter's own method; a data acquisition outage hits every stack it serves.

**Construction layer:** every plant's rate at its Contract Capacity (10 figures, graded within its range) and the chart. The cracker keeps them. The mirror's annual averages fall outside every range, Juniper Draw's by 1 pound.

**Hazard table:**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| reserve shutdowns, maintenance and planned outages counted as forced | A | every plant with such records, tens to hundreds of hours |
| UTC calendar against the dictionary's Pacific year | A | Moraine Point 7 hours under; no other plant |
| any substitute flag (NOx included) | B | every plant, +22 to +129 |

**Referee:** EPA's hourly operating time, which shows the plant running inside the three first estimates; it arbitrates the entries and hands over no figure.

**Cracker sheet:** the cracker landed the call and ran the battery (keys unique, no exact duplicate rows, every offer joins a facility) and executed the dictionary's filed sentences: the forced types, the Pacific year and the plant's outage as time off line, which it reads off the forced lines by merging the plant's lines in time (the dedup reflex; it does not model which unit's loss stops the plant) and counting the merged spans. For substitute data it reads the CO2 mass measure indicator.

| Ask figure | Cracker's read | Cracker | Golden | Verdict |
|---|---|---|---|---|
| A Tamarack Landing hours | union of the plant's forced lines | 61 | 23 | miss |
| A Tamarack Landing outages | merged spans | 4 | 2 | miss |
| A Juniper Draw hours | union of the plant's forced lines | 60 | 15 | miss |
| A Juniper Draw outages | merged spans | 5 | 2 | miss |
| A Sorrel Butte hours | union of the plant's forced lines | 147 | 22 | miss |
| A Sorrel Butte outages | merged spans | 6 | 3 | miss |
| A Coldbrook hours | union of the plant's forced lines | 28 | 17 | miss |
| A Coldbrook outages | merged spans | 4 | 1 | miss |
| A Moraine Point hours | union of the plant's forced lines | 303 | 85 | miss |
| A Moraine Point outages | merged spans | 6 | 7 | miss |
| A Ochre Flat hours | union of the plant's forced lines | 297 | 193 | miss |
| A Ochre Flat outages | merged spans | 4 | 5 | miss |
| A Lindgren Hill hours | union of the plant's forced lines | 47 | 46 | miss |
| A Lindgren Hill outages | merged spans | 3 | 2 | miss |
| A Ashby Gulch hours | union of the plant's forced lines | 28 | 16 | miss |
| A Ashby Gulch outages | merged spans | 5 | 3 | miss |
| A Kessling Creek hours | union of the plant's forced lines | 234 | 84 | miss |
| A Kessling Creek outages | merged spans | 4 | 5 | miss |
| A Brenmoor Mill hours | union of the plant's forced lines | 189 | 56 | miss |
| A Brenmoor Mill outages | merged spans | 6 | 4 | miss |
| B Tamarack Landing | CO2 indicator | 0 | 73 | miss |
| B Juniper Draw | CO2 indicator | 0 | 93 | miss |
| B Sorrel Butte | CO2 indicator | 0 | 81 | miss |
| B Coldbrook | CO2 indicator | 0 | 124 | miss |
| B Moraine Point | CO2 indicator | 0 | 22 | miss |
| B Ochre Flat | CO2 indicator | 0 | 23 | miss |
| B Lindgren Hill | CO2 indicator | 0 | 53 | miss |
| B Ashby Gulch | CO2 indicator | 0 | 33 | miss |
| B Kessling Creek | CO2 indicator | 0 | 15 | miss |
| B Brenmoor Mill | CO2 indicator | 0 | 37 | miss |

Lindgren Hill's hours are the thinnest row: the union gives 46.9 against 45.7, a different whole hour.

**Mirror sheet.** The mirror stops at the default (Tamarack Landing and Moraine Point, 905 MW) and takes the cracker's ask paths. It misses all 30 ask rows. It misses nine of the ten rate rows; Juniper Draw's 885 sits a pound under its range, so call it kept. It keeps the chart's form: 2 of 43 ask-side criteria.

Mirror leakage: 5 per cent of ask weight.

Pair ceiling: 38 (the cracker 38 + 7 + 55 x 0.30 = 61.5, keeping the ten rate rows and the chart, 13 of 43; the mirror 5 + 7 + 55 x 0.05 = 14.6).

## Layer 1 inventory

Each item, the system that writes it, its file and its natural mishandling; the R2 block in `checks.py` asserts the golden with the item mishandled.

| Item | System | File | Mishandled | Effect (asserted) |
|---|---|---|---|---|
| each hour's start in local time with its UTC offset | the sellers' meter data systems | the meter data | the offset dropped, daylight time read as standard | same seven, same slate (Tamarack Landing 955) |
| partial operating hours | the data acquisition systems' operating time | EPA's hourly file | kept in the window | same seven, same slate |
| substitute-data hours | Part 75 missing-data procedures | EPA's hourly file | left out | same seven, same slate |
| negative net while idle | the revenue meters drawing station service | the meter data | dropped | the default keeps its five |
| two offers without an EIA plant code | the sellers' offer forms | the offers log | matched by name and county in the generator inventory | one plant each |
| a stack renumbered at a monitor replacement | the monitoring plan | EPA's hourly file, the monitoring plans | read as two units | one facility and one series either way |
| two stacks at the two-turbine plants | EPA's unit grain | EPA's hourly file | one stack taken for the plant | refused by RP-7 2.3 (SF8); loud, the rate falls to about half |
| the generator survey's combined-cycle rows and co-located peakers | EIA | the generator inventory, the generation survey | the survey's net generation for the rate | the survey is monthly; same default slate (SF7) |
| GADS entries in UTC from the sellers' outage logs | the sellers' outage logging | the GADS records | read on the UTC calendar | Ask A only: Moraine Point |

## Pre-ship check

- **Three rules.** Domain: the emissions inventory's own estimate of a gas unit's CO2 per net MWh at the operating level a commitment fixes, read from hourly heat-input-based CO2 against metered output (the swap in the Three rules section stops reading). Two layers: the Layer 1 inventory above, each asserted neutral to the call or confined to an ask; Layer 2 the rate at the Contract Capacity. Decisive step analytical: the strong analyst who reads every field right and executes every filed rule, the fill included, takes Tamarack Landing and Moraine Point (R3a on the clean truth, asserted); the judge's Gate H reads the same.
- **Gates.** 12 files in 4 formats (csv, pdf, txt, xlsx); EPA's hourly file at 245,616 rows; two distractors (the generation survey and the 2027 planned outages) the solution never reads; 180 checks; `verify.py` from the bundle alone; two builds byte-identical; `figures_check.py`, `precut.py` and `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK); guard heart WARN, surface promoting the task445 pair for the author's read (both answered in the Draw); the containers carry the fiction's people and dates.
- **The main call after stage 4.** The repairs (RP-7 5.3 worded as the records that may be used, the request for offers' baseload sentence and data package, the dictionary's Pacific year and plant outage, Ask B's wording, Ochre Flat's New Year outage moved inside the year with every other plant's series byte-identical, the long first estimates in three outage logs) moved no rate, no verdict and no slate figure; Ochre Flat's forced outage hours went from 189 to 193.

## Leak check

- `leak.py`: REVIEW, no LEAK. Each REVIEW line is harmless: the dictionary's "generator" is EIA's generator data; RP-7, the request for offers and the dictionary carry the call's vocabulary without naming the move; the data files name the plants beside numbers and rank nothing; the dates after 6 November 2026 are the 2027 planned outages and the delivery term.
- Reader, first pass (2026-10-14): no decisive-step sentence, no ranking file, no answer-like figure, nothing that exists only to help. Question 5 read RP-7 5.3 as fixing the rate over every 2024 and 2025 hour, the easy answer, and question 6 called the main answer rule application on that reading: 5.3 was reworded (SF17), the quantity staying in 5.2. Realism tells fixed in the generator: the monitoring plans' lone history comment with a doubled stop (comments cleaned, ordinary history added at four units), the GADS file opening on a re-entered outage (sorted by unit and entry number, the GADS order), the request for offers without the sections a real one carries (credit and security, confidentiality). Tells left as they are: round Contract Capacities (offers are made in round megawatts), revenue-meter energy to three decimals (kilowatt-hours).
- Reader, second pass on the repaired pack (2026-10-14): questions 1 to 4 none; question 6 an analytical choice (how to build each plant's rate from the two sources), the fill the only stated rule. Question 5 still read "for calendar years 2024 and 2025, and on no others" as every hour of both years: 5.3 now says only which records may be used ("Only the plant's own records may be used to determine its emission rate"), the heat-rate exclusion it carried, which read as aimed at particular routes, folded into that. Realism: reserve-shutdown entries all stamped ten minutes after their start now carry varied entry times. Left as they are: the uniform Appendix D and G methodology (gas combined cycles monitor alike), EPA's integer capacities beside EIA's decimals in the crosswalk (the two agencies' own precision).
- Reader, third pass on the shipped pack (2026-10-14): questions 1 to 4 none; question 5 no filed sentence fixes the computation or the hours (5.2 defines the quantity, 5.3 the records that may be used, 5.4 the comparison); question 6 an analytical choice about which hours and basis define the rate under a run-every-hour commitment. No third rewording: the pooled reading the reader still sketches is the easy method on the filed estimand, which the judge's rounds 1 and 2 found closed by 5.2 and the request for offers 3.1 to 3.3. Tells left as they are: one spring inspection per plant in the 2027 planned outages (the distractor; each seller's annual outage), uniform resource descriptions (configurations named alike), round escalation rates (offers quote the District's form).

## Determinism judge

- Stage 4 (2026-10-14): NOT_DETERMINISTIC (underspecified_objective), SEND_BACK, on the workbook asks only. The 990 MW call reproduced and was forced; every rate reproduced and every window left every plant on its side; Gate F strong (the 2025 averages give 905 MW, the peak hours 775 MW), Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no, Gate H domain pass, layers pass, decisive step analytical. Findings: the whole-pound rate turns on the window; Ask A's year (UTC or Pacific) and what a plant outage is; Ask B's unit or clock hours and which indicator; two minor risks (a blank EIA code read as an incomplete offer, the cyclers' low capacity factors read as outside the standard).
- Re-judge (round 2, 2026-10-14): DETERMINISTIC, FIX_NOW. Every graded figure reproduced from the bundle (the ten rates inside their ranges, 990 MW and the fill's running totals, the twenty Ask A figures with the latest entry standing and the three long estimates seen in EPA's and the meter's hours, the ten Ask B clock-hour counts); every window, 2025 alone, the hours at or above 98 per cent, a 90 to 110 per cent band and a linear fit leave every plant on its side (Tamarack Landing 953 to 984). Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain pass, layers pass, decisive step analytical. The one repair: the EIA extracts' workbook properties named a person; they now carry the department.
- Re-judge (round 3, 2026-10-14, the shipped pack): DETERMINISTIC, APPROVE. Every graded figure reproduced; every window, 2025 alone and the fitted curves leave all ten plants on their side; hygiene clean, the file properties included. Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain pass, layers pass, decisive step analytical. Its one note, that the latest-entry rule for Ask A is in no filed sentence, it rates low risk because the entry times and EPA's hours make it the only coherent reading; a dictionary sentence saying so would hand the device over, so none is added. Report: `determinism_check_report.md`.
- Round 1's disposition is the client's for a prompt change after model runs; none had run, Gates F to H passed and the judge scoped the repair to the asks with the call, the stump and the pack frozen, so the architecture stands and the repair was re-judged once. Its proposed pins were not taken where they file the method (the 2 per cent band is the decisive step) or hand over a device (the heat-input field): the rates are graded on ranges, and the asks' readings are closed by filed definitions and wording, the devices kept as mishandlings the records rule out.

## Tried and rejected

- 2026-10-14, draw: task456 (ET13, regional hospital surge trigger) first, as `status.py next` names it. Rejected for now: hospital capacity sits in Healthcare Delivery's patient-flow task type, which serves no ETL objective, and the ETL task types free of the last three draws (payment claims, emissions inventory, test equating) do not hold it.
- 2026-10-14, draw: the ambient-temperature correction of full-load heat rate as the decisive step. Rejected: a combined cycle's full-load heat rate moves 1 to 2 per cent across the seasons, too little against the margins determinism needs; it stays inside the golden method.
- 2026-10-14, build: the revenue meter in hour-ending local prevailing time (23 and 25-hour days). Rejected: reading hour ending as hour beginning moved Tamarack Landing's rate from 980 to 894 on the first dispatch, across the line; a clock slip that flips the call is Layer 1 carrying the stump. The meter now gives each hour's start with its UTC offset, and dropping the offset leaves every plant on its side (asserted).
- 2026-10-14, build: hourly output drawn independently each hour, and duct firing hour by hour. Rejected: no plant follows load that way, and it made the hourly match fragile at every ramp; output now follows load over five-hour averages, and duct firing covers a hot or cold day's heavy-load hours at one level.
- 2026-10-14, build: the call as shape 10, the megawatts that comply (2,375 MW from seven plants, a scorecard against 925), with the sellers' seasonal capability tests as a capacity report and an eligibility screen. Rejected at the heart check: task230 v3, drawn just before, took shape 10 and the capacity report on the same puzzle lineage. The call now fills the 1,000 MW need from the complying offers in order of capacity price (request for offers 5.2, stated once), the capability tests are cut, and the rates, the ladder and the asks are unchanged.
- 2026-10-14, stage 4: the asks as first worded, whose wrong paths were readings rather than mishandlings (a plant outage as any unit out, the UTC year, stack hours, the CO2 indicator). Rejected by the judge as unfiled; the readings are now closed by the dictionary and the ask's wording, and the cracker's remaining path (the union of a plant's lines) landed on Moraine Point's, Ochre Flat's and Kessling Creek's figures until those logs carried a first estimate of return that ran long.
- 2026-10-14, stage 4: filing the 2 per cent window, the plant-out rule and the heat-input field, as the judge proposed. Rejected: the window is the decisive step filed as rule application, and the other two hand the ask devices over; the rates are graded on their ranges instead.
