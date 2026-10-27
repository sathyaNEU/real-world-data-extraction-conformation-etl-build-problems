# task310: when each region gets its round of 2,400 home batteries, and the energy each round delivers

Wave 7, Opportunity Sizing & Decision Support. Architecture 1, drawn 2026-10-27. Seed OS12 (a solar installer splitting
2,400 retrofit batteries across four regions) gives the world (rooftop solar homes, 2,400 retrofit batteries, four
regions) and the quantity (what the batteries are worth in each region). Its decoy-era mechanism, a closed leasing
channel whose homes still buy through its successor, is a reading of an owner-type code and is not used. Its split in
proportion to expected sales echoes task306's allocation of battery work in lots, and a pick of one region for a
retrofit round would echo task309, so the decision becomes the order of four annual regional rounds. No probe, reader or
solver was run (the STOP rule); the stump is argued on paper below and measured on the generator's clean truth and the
cut pack (generator/checks.py, 125 assertions).

## Draw

| Axis | Value |
|---|---|
| Domain / task type | energy-systems-utilities / generation-capacity-planning (serves Opportunity Sizing): each round adds 2,400 home batteries to the state's distributed storage, valued on the energy they deliver |
| Objective | Opportunity Sizing & Decision Support: the headline is each round's yearly energy, sized from the pool (the solar each region's homes' arrays produce beyond the home's use at the time) to the realisable (what 2,400 batteries of the programme's specification take from that surplus and give back to the homes in a year), and the sizes set the order of the rounds |
| Decision / answer unit / question form | schedule_or_sequence / date_or_period (each region's round year) with a kWh and an MWh figure / when |
| Shape | 06, a sequenced schedule: each region's round year, the energy a battery and a round delivers a year, a chart, and three asks across the regions and the pilot's quarters |
| Gap / pattern / generators | population / none / G3 (record versus operation), G12 (a held-down export read as no surplus) |
| Gate G / strategy | binding_constraint / other (throttled-output recovery: a record that carries a site's output only up to a limit set by the site's own use each hour) |
| Layer 2 | estimation_fit (censoring and truncation), own:storage-yield-on-the-panels-output-not-the-throttled-record |
| Forum / forcing event / org family | minister_or_cabinet (the energy minister approves the round order with the programme's 2027 to 2030 appropriation) / budget_or_appropriation / government_agency |
| Stakeholder | the analyst in the State Energy Office's home battery programme (research_desk); the prompt carries no persona |
| People (guard.py names --geo AU --seed 310) | Brianna Parrish, programme director (signs the guideline and the brief); Keith Ruiz, connections manager at Southmark Networks (the connection standard); Katelyn Acosta, panel data manager (the panel's data guide) |
| World | the State Energy Office of a fictional Australian state; Southmark Networks, its distribution network; the Home Energy Monitoring Panel, 160 homes (40 a region) with 2025 inverter and revenue-meter readings; regions Sandhaven Coast, Eastbrook Metro, Yarrandale Valley and Tarrock Highlands; Yarrandale's growth corridor in Riverbend Estate and Quarry Hill Estate on the constrained Riverbend zone substation; readings to 31 December 2025, brief November 2026 |
| Deliverables | battery_rounds_2027_2030.xlsx (the workbook), round_yield_by_region.png (the chart), minister_brief_battery_rounds.pdf (the one-page brief) |
| Guard | WARN only: overuse.org_family (government_agency), overuse.objective |

The WARNs, answered: the organisation that values home batteries on the energy they deliver to homes is a state energy
office (a network would value them on exports avoided and a retailer on bills, which are other quantities), so
government_agency is the honest family; the objective is the lane's. Axes redrawn at the check: Gate G from
method_or_model_selection to binding_constraint, after (population, G3) and (population, G12) under
method_or_model_selection were spent in six and seven earlier builds. The label is the honest one: the network's export
limit binds on the recorded output (the inverter holds solar to the home's use plus the limit), and that binding limit
is what puts the natural order wrong, while the battery's charging is not bound by it. Also the deliverables from docx to
pdf (repeat.deliverables against task309) and one persona (people.first).

### Candidates written before the choice (each with its default path)

1. **The seed's successor channel** (a closed leasing programme's 12,500 homes still buying through its servicer).
   Default: drop the closed-lease homes. Dropped: the call turns on reading an owner-type code, which is data semantics.
2. **Feed-in tariff expiry in event time** (retrofit demand by months since each home's premium rate ended). Default:
   2026 sales share or a post-expiry segment rate. Dropped: the tariff register's end dates send any solver to event
   time, and the construction is one group-by on months since expiry.
3. **A pilot's first contact harvesting the ready households** (a second contact converts less). Dropped: the swap test
   reads the same for subscribers offered an upgrade, so the domain is a backdrop, and the depletion is a stratification
   on contact count.
4. **A contact pulling purchases forward.** Dropped: task136's driver (a bulk-buy mostly enrols homes about to install).
5. **A battery valued on daily surplus capped by its capacity against annual totals.** Dropped: hour-by-hour simulation
   is the field's first move, so the golden would be the opponent's default construction.
6. **The battery's yield on the arrays' output rebuilt for the export-limited homes (chosen).** Default: simulate the
   programme battery on each home's recorded solar and use; golden: on the output the arrays produce.

**The data-native sentence:** Southmark Networks has connected every new system on the Riverbend zone substation's
feeders since July 2023 on a 0.5 kW constrained-zone agreement, so the inverter on each of those homes holds its output
to the home's own use plus half a kilowatt hour by hour, and the monitoring panel records that held-down output as the
home's solar; nothing in the readings marks the solar the arrays were not allowed to produce, and a battery beside the
home would take it.

**Sources, one line each:**
- Client library: Energy Systems & Utilities carries Layer 1 techniques and no Layer 2 cards, so the pitfall comes from
  the estimation_fit family (censoring and truncation); here the limit is not a detection floor but a ceiling that moves
  with each home's own use each hour.
- Seed OS12: the world and the quantity only (`status.py task310` prints the header and Situation).
- task136 (a rooftop PV hosting-capacity forecast, a bulk-buy's pull-forward): the same physical setting; this build
  takes the installed systems as given and recovers what their held-down inverters did not record.
- task308 (capacity offers valued on shortfall hours, a class out together from one cause): the same task type; the
  driver differs (no shortfall hours, no common cause, the record held down per site).
- task197 and task470: their drivers rebuild an unrecorded quantity (a response under a scheduled trajectory, events a
  sensor never sees); the card's differentiation lines say why neither is this one.

## Default path

1. Read the programme guideline: each region's round is worth 2,400 times the average energy a year the programme
   battery (10 kWh usable, 5 kW, 95 per cent each way) would deliver to the panel's homes in that region, simulated hour
   by hour over the 2025 readings from an empty battery, and the rounds run in order of that worth from 2027.
2. Build each panel home's 2025 hours: inverter solar from both portals (Velkora hourly on the local clock with its UTC
   offset; Ondrava lifetime watt-hour counters at the local hour end), revenue-meter import and export from the
   half-hourly reads in market time, summed to hours, the controlled-load channel left out, replaced meters joined on
   the NMI.
3. Take each hour's general-supply use as solar plus E1 import less B1 export.
4. Simulate the battery hour by hour: charge from solar above the use, discharge to the use, within its power, capacity
   and efficiency; sum the year's energy delivered to each home.
5. Average each region's 40 homes and multiply by 2,400.
6. Order the rounds by that figure.

**Ends on:** Sandhaven Coast 2027, Eastbrook Metro 2028, Tarrock Highlands 2029 and Yarrandale Valley 2030, Yarrandale last
at 1,210 kWh a battery (1,200 printed), its round 2,900 MWh a year.

**Golden:** Yarrandale Valley 2027 at 2,458 kWh a battery (2,450 printed, 5,900 MWh a round), then Sandhaven Coast 2028
(1,900 and 4,600), Eastbrook Metro 2029 (1,500 and 3,600) and Tarrock Highlands 2030 (1,300 and 3,100); the world's
truth, the battery run on what every array actually produced, is Yarrandale 2,453, Sandhaven 1,908, Eastbrook 1,497,
Tarrock 1,294.

## Stump sentence

A competent analyst simulates the programme battery against each panel home's recorded hourly solar and use and runs the
rounds Sandhaven Coast first and Yarrandale Valley last, Sandhaven Coast 2027, Eastbrook Metro 2028, Tarrock Highlands 2029
and Yarrandale Valley 2030 at about 1,200 kWh a battery, because the 28 Yarrandale estate homes on the 0.5 kW
constrained-zone agreement recorded only the solar their own use and the limit took: their inverters held back the
rest, and with their output rebuilt hour by hour from the unlimited Yarrandale homes' energy per kilowatt their
batteries fill on most days, so Yarrandale Valley goes first at about 2,450 kWh a battery.

## Three rules

- **Task type:** energy-systems-utilities / generation-capacity-planning, which serves Opportunity Sizing: the rounds add
  distributed storage and are sized on the energy it delivers.
- **Domain test:** the deciding quantity is the energy a home battery delivers to the home in a year, which distributed
  energy planning gets by simulating the battery against the home's interval solar and load; the solar it charges from
  is what the arrays produce, which at an export-limited connection is more than the inverter recorded.
- **Swap:** "run the first round of 2,400 batteries in Yarrandale Valley, where the inverters on constrained-zone
  connections hold the arrays to the home's use plus half a kilowatt and a battery would take the rest" becomes "run the
  first round of 2,400 heat pumps in the district where the boilers are held to the radiators' draw"; the export limit
  at the connection point, the inverter's export control and the battery's state of charge have no counterpart, and the
  hour-by-hour storage simulation has nothing to run on.
- **Layer 1:** revenue-meter half hours in market time, stamped at the end of the interval (UTC+10 all year, the
  network's metering system), beside inverter hours on the local clock with daylight saving (the vendors' portals); one
  vendor's feed as lifetime watt-hour counters at the local hour end with no offset, a repeated 03:00 on 6 April and none
  on 5 October, that restart from zero when an inverter is replaced, the other in watt-hours per hour with its offset; a
  controlled-load register on a second channel (off-peak hot water); meters replaced part-way through the year under a
  new serial; estimated and substituted reads carried with quality flags; panel ids keyed to network meter numbers
  through the panel register; connection codes with effective dates. All written by the systems that hold the data;
  every mishandling leaves the call and every printed figure where they were (R2, asserted).
- **Layer 2:** estimation_fit, censoring and truncation: the recorded solar is held at a ceiling that moves with each
  home's own use, and the choice that flips the order is simulating the battery on the output the arrays produce,
  rebuilt for the limited homes from comparable unlimited homes under the same sky, instead of on the record.
- **Decisive step:** recognising that an export-limited home's recorded solar is inverter-limited output, a floor on
  what its array produces, and rebuilding its available solar hour by hour from the unlimited homes' energy per
  kilowatt in the same region before running the battery.
- **Not semantics:** every field read correctly (the connection code says 0.5 kW, the units, clocks and channels
  handled, the replaced meters joined) still leaves the battery simulated on the recorded flows, which is the field's
  standard method; no field, code or definition says how much solar a limited home's array could have produced, and the
  network standard's clause that an export limit applies to exports only does not say the record is held down.
- **Not rule application:** no filed rule or procedure rebuilds a limited home's output; the guideline files the
  valuation and the battery, the network standard files what a limit applies to, and executing every stated rule on the
  recorded flows files Sandhaven Coast first and Yarrandale Valley last. Measured on the cut pack: the enumerated family
  (recorded flows; the limited homes dropped; annual totals; rebuilt output by regional median or mean per kWp, pooled or
  orientation-matched, calibrated or not, capped or not, floored or not, statewide or regional) spreads Yarrandale's
  figure from 1,210 to 2,459 kWh a battery; the standing family (the eight rebuilds that charge the battery from the
  arrays' output under the region's own sky) spreads it by 8 kWh and Eastbrook's by 12 on figures printed to the nearest
  50, every member at least 10 kWh inside its bin on both printed figures; the ruling-out is not loud: it needs the
  connection codes, the standard's export-only clause and the limited homes' midday output at the limit read together,
  and that reading is the step.
- **Analyst test:** a strong analyst who aligns the clocks, differences the counters, leaves out the controlled load and
  reads every connection code simulates the battery on each home's recorded solar and use and ends on Sandhaven Coast
  2027, Eastbrook Metro 2028, Tarrock Highlands 2029 and Yarrandale Valley 2030, Yarrandale last at about 1,200 kWh a
  battery.
- **Estimand:** the programme guideline (section 3) files each region's round as 2,400 times the average annual energy
  the programme battery, as specified in its appendix, would deliver to the homes of the monitoring panel in that region
  over 2025, hour by hour from an empty battery, and section 4 runs the rounds in order of that figure from 2027.
- **No decoy:** nothing is planted to be caught: the export limits are the network's connection rule for the Riverbend
  feeders, written in its standard and its register, and no memo, draft, briefing or stakeholder figure ranks the
  regions or carries the natural order.
- **No certified replay:** the method is not recovered by reproducing certified or published figures; the pack holds no
  published battery yield for any region, and the pilot's telemetry is of other homes in two other regions.
- **Lesson:** a battery valued on a throttled record inherits the throttle: where an inverter holds output to a site's
  use plus a limit, the recorded solar is a floor on what the array produces and a store's value has to be simulated on
  the rebuilt output; no build on file teaches recovering a physically held-down record before a storage simulation.

## Readability screen

| Rung | What it needs | Verdict |
|---|---|---|
| general-supply use as solar plus E1 less B1, E2 out | data guide section 4; guideline Appendix A | readable |
| clocks: meter in market time interval-ending, inverters local with daylight saving | data guide section 3 | readable |
| a replaced Ondrava inverter's counter from zero | data guide section 5; the system register's note | readable |
| the battery: 10 kWh, 5 kW, 95 per cent each way, empty on 1 January, hour by hour | guideline section 3 and Appendix A | readable |
| a round is 2,400 times the regional average; order descending | guideline sections 3 and 4 | readable |
| the export limit applies to exports only, and the limited homes' inverters hold output to use plus the limit (decisive) | no sentence; the connection register's codes, the standard's export-only clause and the limited homes' recorded output pinned at use plus 0.5 kW (or 1.5 kW) through every clear midday | silent |

## Ladder

| Rung | Construction | Sandhaven Coast | Eastbrook Metro | Yarrandale Valley | Tarrock Highlands | Call |
|---|---|---|---|---|---|---|
| R0 | mean array size (kWp) | 5.93 | 4.08 | 5.78 | 3.62 | Sandhaven Coast |
| R1 | annual totals: export times round-trip efficiency, capped by import and a cycle a day | 2,271 | 1,588 | 1,292 | 1,407 | Sandhaven Coast |
| R2 | the default path: the battery on the recorded flows | 1,908 | 1,468 | 1,210 | 1,294 | Sandhaven Coast |
| R3 | the limited homes dropped as unrepresentative | 1,908 | 1,369 | 1,356 | 1,294 | Sandhaven Coast |
| R4 | only the 0.5 kW homes rebuilt | 1,908 | 1,468 | 2,458 | 1,294 | Yarrandale Valley |
| R5 | the golden: every limited home rebuilt from its region's median per kWp | 1,908 | 1,502 | 2,458 | 1,294 | Yarrandale Valley |
| R5' | the standing family's range (eight constructions) | 1,908 | 1,490 to 1,502 | 2,451 to 2,459 | 1,294 | Yarrandale Valley |
| T | the world's truth (the battery on what each array produced) | 1,908 | 1,497 | 2,453 | 1,294 | Yarrandale Valley |

kWh a battery a year, from the cut pack. Rounds a year: the golden's Yarrandale 5,900 MWh, Sandhaven 4,600, Eastbrook
3,600, Tarrock 3,100. R2 is the stump; R3 is the closest repair that misses (it notices the limited homes and drops
them, which keeps Yarrandale third); R4 lands the call and misses Eastbrook's two figures (1,450 and 3,500 printed). The
golden clears each next round by 1.288, 1.270 and 1.161; the default path's top clears its runner-up by 1.299 and puts
Yarrandale last by 1.069; no cheap route (R0 to R3, mean inverter rating, mean export, mean recorded solar) names
Yarrandale first (asserted). The default path's schedule matches the golden in no year. Sloppy rebuilds the data refute
(a calibration on hours that include half hours exported at the limit, 2,391; another region's sky, 2,367) keep the call
and miss the figures. A size ranking (R0) lands nothing: the estates' arrays are sized under the 133 per cent rule on 5
to 6 kW inverters, and Sandhaven's retirees' arrays are larger.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the use a battery serves | general supply: solar plus E1 less B1 | E2 added to the use | same call; Sandhaven's figures move (2,048) | guideline Appendix A (not connected to a controlled-load circuit); data guide section 4 |
| SF2 | the time step | hour by hour | half hours | another construction | guideline section 3 ("hour by hour") |
| SF3 | the battery's state on 1 January | empty | full | same call, same figures (asserted) | guideline section 3; converge |
| SF4 | efficiency | 95 per cent stored on charge, 95 per cent delivered on discharge | 90 per cent round trip on one side | same call | guideline Appendix A |
| SF5 | power | 5 kW charging and discharging | power on discharge only | same call | guideline Appendix A |
| SF6 | the round's value | 2,400 times the regional average | the regional total | same order | guideline section 3 |
| SF7 | the panel's weights | equal, 40 homes a region | weighted to the eligible homes | another estimand | guideline section 3; data guide section 6 (not weighted) |
| SF8 | the year's clock | market time, UTC+10 | the local clock throughout | same call, same figures (asserted) | data guide section 3; converge |
| SF9 | what the battery may do with solar | charge from solar beyond use, discharge to use, never export | export from the battery | same call | guideline Appendix A (self-consumption, no export from the battery) |
| SF10 | the rebuild's reference | the region's unlimited homes' median output per kWp each hour | the mean; orientation-matched where three or more match | same call, same figures (asserted) | converge |
| SF11 | calibration to each home's own unexported hours | none | a factor fitted on hours importing in both half hours | same call, same figures (asserted) | converge |
| SF12 | which homes are rebuilt | every home whose inverter rating exceeds its export limit | only the 0.5 kW homes | same call; Eastbrook's figures move (asserted) | the connection register: the 1.5 kW homes' output is held the same way |
| SF13 | the inverter's AC rating on the rebuilt output | capped | uncapped | same call, same figures (asserted) | converge |
| SF14 | the floor at what the home recorded | kept | dropped | same call, same figures (asserted) | converge |
| SF15 | the order | descending by round value, 2027 first | ascending | another schedule | guideline section 4 |
| SF16 | rounding | kWh a battery to the nearest 50, MWh a round to the nearest 100, from unrounded values | rounding the battery figure first | same figures (every standing member at least 10 kWh inside both bins, asserted) | the prompt's closing sentence |
| SF17 | Ondrava's first reading of the year | closes a night hour (no energy) | counted from zero | same figures | data guide section 5; a replacement inverter's counter starts from zero |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each region's 40 panel homes as recruited, none added or lost | filed (guideline section 3, data guide section 1) |
| 2 | Unit of account | kWh a battery a year; MWh a round of 2,400 | filed (guideline sections 1 and 3) |
| 3 | Attribution window | calendar 2025 of the panel's readings | filed (guideline section 3) |
| 4 | As-of dating | the panel's 2025 release of 9 March 2026 | filed (data guide) |
| 5 | Version basis | one release of each file | C1 |
| 6 | Denominator | the region's 40 homes, equal weight | filed (SF7) |
| 7 | Weighting | equal | filed (data guide section 6) |
| 8 | Window length | the full year from 1 January | filed (guideline section 3) |
| 9 | Boundary inclusivity | the year's first and last hours in market time; the local-clock alternative prints the same figures | C1 (SF8, asserted) |
| 10 | Rounding path | unrounded values, rounded once at the end | the prompt |
| 11 | Tie-break | none: every next round cleared by 1.16 or more | asserted |
| 12 | Maturity and censoring | the export limit censors the record of the limited homes' output; that is the decisive step | the analysis (R5) |
| 13 | Order of operations | rebuild the solar, then use, then the battery hour by hour, then average and multiply | WHAT filed (guideline section 3); the rebuild is the analysis |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | the repeated 03:00 counter reading is the clock going back, both kept in order | C1 (R2, asserted) |
| 16 | Identity normalisation | panel ids to NMIs through the register; replaced meters and inverters joined on NMI and panel id | asserted (R2) |
| 17 | Netting against gross | use is solar plus import less export | filed (SF1) |
| 18 | Dimensional units | Wh in the portals, kWh in the meter reads | filed in the records |
| 19 | Code and status semantics | quality A, E and S are all settlement values; agreement codes carry their limits | filed (data guide section 4; standard section 2); never the stump |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | the export limit applies at the connection point to exports only and continues with the battery | filed (standard sections 3 and 4, guideline Appendix A) |
| 22 | Forward window contents | 2025 is the year the guideline values every round on, for every round year | filed (guideline section 3) |

## Literal reader

Executing the prompt and every filed sentence word for word (the guideline's sections 1 to 4 and Appendix A, the
standard's sections 2 to 4, the data guide's sections 1 to 6) leaves one open move on the call: what solar the battery
charges from. The estimand is filed literally (2,400 times the panel average of the energy the programme battery would
have delivered over 2025, hour by hour from empty), the battery is filed to its efficiency and power, and the record
settles the open move: the limited homes' output sits at their use plus their limit through every clear midday while
their arrays and the unlimited homes beside them show the sun was there, so every construction that charges the
battery from the arrays' output files Yarrandale Valley first at 2,450 kWh a battery; the default files Sandhaven Coast
first by running the same literal estimand on the throttled record, never another reading of it.

## Oracles

None on the call: no file states a battery yield, ranks the regions or prints a round's energy. The tariff schedule and
the household survey are distractors (named in metadata.json) and carry no figure the call reads. On the asks there is
no control total: the network register's 2025 battery commissionings do not tie to the certificates under any handling,
because commissioning lags installation and some installers never notify.

## Ask sheet

**Ask A: homes eligible for the 2027 round on 30 September 2026 in each region (4 figures, whole homes).** H18: the
pool each round draws its 2,400 homes from, a measure every region carries that the call does not turn on (the call
reads the panel's files, never the network's registers or the Booster claims; asserted). Use: the minister's question
whether each region can fill its round. Primary device, silent (D2/D8, an anchor on the current record, and D7, the
true key along a prior-id chain): the guideline's twelve-month solar rule is executed on the register's commissioned
date, but when Southmark reissues a premises' NMI after a switchboard upgrade, its solar and battery rows move to the new
NMI dated from the reissue, and the extinct NMI's rows close that day; only the standing data's previous_nmi links them.
Interior: a replaced system ran until its successor was commissioned, on the same NMI or the old one. Hazards: Booster
claims lodged before July 2022 carry no NMI and their batteries are often unregistered (address, suburb and postcode
normalised; two suburbs share postcodes 2592 and 2711), Paid claims on an extinct NMI, business premises, 2025 batteries
commissioned weeks after installation. Files: southmark_der_register_2026-09-30.csv,
southmark_nmi_standing_data_2026-09-30.csv, battery_booster_claims_2021-2023.xlsx, the guideline. Stops (Sandhaven /
Eastbrook / Yarrandale / Tarrock): solar dated from the NMI's own earliest row (the careful path) 6,552 / 8,494 / 4,356 /
4,515; from the active row 6,503 / 8,447 / 4,218 / 4,491; claims by the NMI they carry only, or by addresses as written,
6,731 / 8,745 / 4,396 / 4,649; no claims read 6,752 / 8,779 / 4,403 / 4,670; golden 6,591 / 8,535 / 4,381 / 4,539.

**Ask B: the energy the 600 pilot batteries delivered to their homes in each quarter of 2025 (4 figures, MWh to one
decimal).** H18: the programme's measured delivery from the 2024 pilot, in Sandhaven Coast and Eastbrook Metro, other
homes than the panel's (the call never reads the telemetry; asserted). Use: the brief's evidence that installed
batteries deliver. Primary device, silent (D6, an event's quantity on every line it covers): at the 24 homes with a Duo
(two units behind one battery meter) each unit's daily row carries the meter's energy and the meter's lifetime counter,
so summing units counts the home twice; the pilot register lists both units without a word on their wiring. Interior:
ten homes with two separately metered units, whose rows differ and both count. Hazards: cloud outages leave days
without rows while the counters carry the energy, rows re-sent after an outage, six warranty swaps whose new unit counts
from zero. Files: norvane_pilot_battery_telemetry_2025.parquet, pilot_round_2024_sites.xlsx. Stops (Q1 / Q2 / Q3 / Q4):
re-sent rows dropped and counters read at the quarter ends, every unit summed (the careful path) 343.4 / 305.2 / 288.3 /
328.6; every two-unit home counted once 320.3 / 283.9 / 267.4 / 305.6; daily rows summed 338.0 / 300.3 / 283.8 / 322.7;
every row 340.3 / 302.6 / 285.7 / 325.1; golden 324.6 / 287.8 / 271.3 / 309.9.

**Ask C: batteries installed in 2025 in each region by installers accredited for the whole of 2027 (4 figures, whole
batteries).** H18: the delivery capacity each round's region already has, a measure every region carries that the call
does not turn on. Use: guideline section 5 (only installers accredited for the whole of the round's year). Primary
device, silent (D1, a resubmission that opens no second case): an installation lodged a second time (a portal error or
a resubmission) carries a new certificate number, a later lodgement date, sometimes a corrected installation date and,
across 1 August 2025, the installer's new accreditation number; most were never audited, so both certificates stand, and
only the module serials, which a battery carries once, tie them. Interior: second lodgements the scheme did process
(the first withdrawn in the amendments), so collapsing before applying the withdrawals loses the installation; and
neighbouring jobs on one day by one installer in one suburb with the same model, which are separate installations.
Hazards: module rows (one certificate per battery), the A to S renumbering on 1 August 2025 (previous_no), withdrawals
and installer corrections, postcodes 2716 and 2905 spanning two regions (placed by suburb). Files:
battery_installation_certificates_2025.csv, battery_installation_certificate_amendments_2025.csv,
installer_accreditation_register_2026-10.csv, southmark_nmi_standing_data_2026-09-30.csv,
southmark_der_register_2026-09-30.csv. Stops (Sandhaven / Eastbrook / Yarrandale / Tarrock): certificates after the
amendments, numbers mapped, by suburb (the careful path) 420 / 463 / 298 / 163; shared modules collapsed to the first
lodgement before the amendments 408 / 454 / 289 / 159; near-duplicates merged on installer, date, suburb and model 414 /
455 / 291 / 156; amendments not applied 421 / 459 / 302 / 165; golden 410 / 456 / 292 / 161.

Main population zero-counts: the call reads the panel register, the system register, both inverter portals, the meter
reads and the panel's connection register; the asks read the network's DER register and standing data, the Booster
claims, the pilot telemetry and register, the accreditation register and the certificates (asserted in checks.py: the
panel's 160 homes carry no reissue, replaced system, battery or Booster claim, and their NMIs hold one active PV row
each and nothing else).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A homes eligible by region | 0 of 4 | miss |
| B pilot energy by quarter | 0 of 4 | miss |
| C 2025 installations by region | 0 of 4 | miss |

Pair ceiling: 32.3 ((45.0 + 19.7) / 2), the cracker keeping 12 of the 12 call figures and 0 of the 12 ask figures, the
mirror (the default path's call) keeping 4 of the 12 call figures (Sandhaven's and Tarrock's battery and round figures,
which no export limit touches) and the same 0 of 12 ask figures; the cracker's ask routes are this note's model of the
careful path, not a measurement of a reader.
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

## Pre-ship check

- 2026-10-27, stage 3 on the final pack: generator checks 137, verify 24 graded figures with 0 disagreements, two
  byte-identical builds (target.zip 6990902f5cfbcf85), figures_check 42 of 42, precut 53/0/0, voice-check PASS,
  leak.py REVIEW with no LEAK, guard heart WARN (overuse.org_family and overuse.objective, answered at the draw),
  guard surface four pairs at 0.10 adjudicated clean: task308 shares the pairing two builds back with another decision
  (one offer of four) and another driver (a common-cause outage), and task309, task165 and task453 share surface only.
- Mechanical leak lines ruled here (sweep 4, kept from the reader): the data guide lists the panel's files, clocks and
  channels and says each portal reports the inverter's AC output, nothing on export limits or what any output was
  held to; the guideline files the estimand and the battery, and its "export limit continue to apply" is the
  connection rule a battery application carries; the standard is the network's own export-limit rules (3.1 to 3.3),
  as a real export-limitation standard states them, and says nothing about what the panel recorded or how a battery
  is valued. All three harmless; the readability screen counts the standard as one of the three reads the step needs.
- House fixes on this pass: invented names screened for real places, schools and companies within two letters (two
  regions, the state, both inverter brands, two module makers and six installers renamed, no retired name left in
  the tree); every shipped PDF read whole by pypdf lenient and strict, pdfminer and pdftotext (H25, asserted).
- Golden realism: the brief and the chart titled with the finding, a source note under every workbook sheet, frozen
  header rows, precision by quantity (kWh to 50, MWh to 100, pilot MWh to one decimal, counts whole).

## Tried and rejected

- The seed's successor-channel architecture (a closed leasing programme's homes buying through its servicer): the call
  turns on reading an owner-type code, data semantics; not drawn.
- The seed's split of 2,400 batteries in proportion to expected sales, and a pick of one region for the round: the split
  echoes task306 (battery work allocated in lots) and the pick echoes task309 (a retrofit round given to one of four
  counties), so the decision moved to the order of four annual rounds.
- Feed-in tariff expiry in event time: readable from the tariff register's end dates and one group-by; not drawn.
- A pilot's first contact harvesting the ready households: a backdrop on the swap test and a stratification on contact
  count; not drawn.
- Contact pulling purchases forward: task136's driver; not drawn.
- Daily surplus capped by capacity against annual totals: hour-by-hour simulation is the field's first move; kept only as
  the default path's rung 1.
- Card check at method_or_model_selection: BLOCK test.same_driver on (population, G3) against task270's lineage and
  (population, G12) against task271 and task273's lineages, with six and seven older carriers; redrawn to
  binding_constraint, the honest label for a limit that binds on the record.
- Zero-export estates: the flat recorded output at the home's use was a glaring anomaly a reader sees in one plot;
  moved to a 0.5 kW constrained-zone limit, which the network standard files and the record shows only as an export
  pinned at half a kilowatt.
- Estates with mixed roof orientations and a pooled reference: a calibration fitted on each home's own unexported hours
  ran 50 to 80 kWh a battery under the golden for the north-east and north-west homes, wider than half a printed unit;
  the estates' builder put every array on the north roof, and the family closed to 8 kWh.
- Estate arrays of 8.4 to 11 kWp and Sandhaven's at 7.4 to 9.2 kWp: the first made a ranking by mean array size reproduce
  the golden order (a one-group-by landing the call), the second broke Australia's 133 per cent oversizing rule on 5 kW
  inverters; the estates now carry 6.6 to 8 kWp on 5 to 6 kW inverters, every array sized under the rule, and both size
  rankings put Sandhaven first.
- Round figures to 100 kWh a battery and 100 MWh a round together: the two grids' edges conflict near the golden;
  battery figures moved to the nearest 50 kWh and the world tuned so every standing member sits at least 10 kWh inside
  both bins.
- Ask devices as first drafted (Booster claims without an NMI, re-sent telemetry rows, module rows and the A to S
  renumbering): every one is found by the hygiene battery and repaired by reflex, so the careful path landed all twelve
  ask figures; re-sited onto silent primaries (the reissue re-dating behind the twelve-month rule, the Duo meter on both
  units' rows, second lodgements tied only by module serials) and the first drafts kept as hazards.
- The panel's homes absent from the network's registers and 2025's certificates without a battery on the register:
  realism gaps a reader would trip on; the panel's homes now sit in the DER register and standing data with nothing but
  their solar, and every live 2025 job commissions its battery with a lag and a 93 per cent notification rate, so the
  register and the certificates do not tie under any handling (no oracle for ask C).
- Neighbouring jobs and second lodgements drawn across all of 2025's jobs: Tarrock Highlands' few installations left a
  mishandling (collapsing near-duplicates, or collapsing shared modules before the withdrawals) exactly on the golden;
  both are now drawn region by region, and every mishandled route misses every region (asserted).
