# task310: when each region gets its round of 2,400 home batteries, and the energy each round delivers

Wave 7, Opportunity Sizing & Decision Support. Architecture 1, drawn 2026-10-27. Seed OS12 (a solar installer splitting
2,400 retrofit batteries across four regions) gives the world (rooftop solar homes, 2,400 retrofit batteries, four
regions) and the quantity (what the batteries are worth in each region). Its decoy-era mechanism, a closed leasing
channel whose homes still buy through its successor, is a reading of an owner-type code and is not used. Its split in
proportion to expected sales echoes task306's allocation of battery work in lots, and a pick of one region for a
retrofit round would echo task309, so the decision becomes the order of four annual regional rounds. No probe, reader or
solver was run (the STOP rule); the stump is argued on paper below and measured on the generator's clean truth.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | energy-systems-utilities / generation-capacity-planning (serves Opportunity Sizing): each round adds 2,400 home batteries to the state's distributed storage, valued on the energy they deliver |
| Objective | Opportunity Sizing & Decision Support: the headline is each round's yield, sized from the pool (the solar each region's eligible homes' panels can produce beyond the home's use at the time) to the realisable (what 2,400 batteries of the programme's specification take from that surplus and give back to the homes in a year), and the yields set the order of the rounds |
| Decision / answer unit / question form | schedule_or_sequence / date_or_period (each region's round year) with a kWh figure / when |
| Shape | 06, a sequenced schedule: each region's round year, its yield per battery and its round's annual energy, the first round's lead over the second, and a chart |
| Gap / pattern / generators | population / none / G3 (record versus operation), G12 (a near-zero export read as no surplus) |
| Gate G / strategy | binding_constraint / other (throttled-output recovery: a record that carries a site's output only after a limit set by the site's own load each hour) |
| Layer 2 | estimation_fit (censoring and truncation), own:storage-yield-on-the-panels-output-not-the-throttled-record |
| Forum / forcing event / org family | minister_or_cabinet (the energy minister approves the round order with the programme's 2027 to 2030 appropriation) / budget_or_appropriation / government_agency |
| Stakeholder | the energy analyst in the Kallara Energy Office's home battery programme (research_desk); the prompt carries no persona |
| People (guard.py names --geo AU --seed 310) | Brianna Parrish, programme director (signs the programme guideline); Keith Ruiz, connections manager at Southmark Networks (the connection standard); Katelyn Acosta, panel data manager (the panel's data guide) |
| World | the Kallara Energy Office of a fictional Australian state; Southmark Networks, its distribution network; the Home Energy Monitoring Panel, 240 homes (60 a region) with 2025 inverter and revenue-meter readings; regions Wennora Coast, Bellmere Metro, Yarrandale Valley and Tarrock Highlands; AUD; readings to 31 December 2025, brief November 2026 |
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
6. **The battery's yield on the panels' output rebuilt for the zero-export homes (chosen).** Default: simulate the
   programme battery on each home's recorded solar and load; golden: on the output the panels could produce.

**The data-native sentence:** Southmark Networks has connected every new system on the Yarrandale Valley feeders since
July 2023 on a zero-export agreement, so the inverter on each of those homes holds its output to the home's own use
hour by hour, and the monitoring panel records that held-down output as the home's solar; nothing in the readings marks
the solar the panels were not allowed to produce, and a battery beside the home would take it.

**Sources, one line each:**
- Client library: Energy Systems & Utilities carries Layer 1 techniques and no Layer 2 cards, so the pitfall comes from
  the estimation_fit family (censoring and truncation); here the limit is not a detection floor but a ceiling that moves
  with each home's own load each hour.
- Seed OS12: the world and the quantity only (`status.py task310` prints the header and Situation).
- task136 (a rooftop PV hosting-capacity forecast, a bulk-buy's pull-forward): the same physical setting; this build
  takes the installed systems as given and recovers what their held-down inverters did not record.
- task308 (capacity offers valued on shortfall hours, a class out together from one cause): the same task type; the
  driver differs (no shortfall hours, no common cause, the record held down per site).
- task197 and task470: their drivers rebuild an unrecorded quantity (a response under a scheduled trajectory, events a
  sensor never sees); the card's differentiation lines say why neither is this one.

## Default path

1. Read the programme guideline: each region's round is worth 2,400 times the average energy a year the programme
   battery (10 kWh usable, 5 kW, 95 per cent each way) would deliver to the panel's homes in that region, and the rounds
   run in order of that worth from 2027.
2. Build each panel home's 2025 hours: inverter solar from both vendors' feeds (one hourly in kWh on the local clock,
   one as lifetime watt-hour counters), revenue-meter import and export from the half-hourly reads in market time
   shifted to the local clock and summed to hours, the controlled-load channel added to import, replaced meters stitched.
3. Take each hour's load as solar plus import less export.
4. Simulate the battery hour by hour: charge from solar above the load, discharge to the load, within its power,
   capacity and efficiency; sum the year's energy delivered to each home.
5. Average the homes in each region and multiply by 2,400.
6. Order the rounds by that figure.

**Ends on:** Wennora Coast 2027, Bellmere Metro 2028, Tarrock Highlands 2029 and Yarrandale Valley 2030, Yarrandale last
at about 1,000 kWh a battery (measured on the prototype at 957 to 1,024 over four seeds).

**Golden:** Yarrandale Valley 2027 at about 3,000 kWh a battery, then Wennora Coast 2028, Bellmere Metro 2029 and
Tarrock Highlands 2030 (prototype: Yarrandale 2,937 to 3,022 against Wennora 2,535 to 2,703; the lead is tuned to 1.15
or more at stage 2).

## Stump sentence

A competent analyst simulates the programme battery against each panel home's recorded hourly solar and load and runs
the rounds Wennora Coast first and Yarrandale Valley last, at about 1,000 kWh a battery, because the Yarrandale homes on
zero-export connections recorded only the solar their own use took; their inverters held back the rest, and with their
output rebuilt hour by hour from the unlimited Yarrandale homes' energy per kilowatt their batteries fill on most days,
so Yarrandale Valley goes first at about 3,000 kWh a battery.

## Three rules

- **Task type:** energy-systems-utilities / generation-capacity-planning, which serves Opportunity Sizing: the rounds add
  distributed storage and are sized on the energy it delivers.
- **Domain test:** the deciding quantity is the energy a home battery delivers to the home in a year, which distributed
  energy planning gets by simulating the battery against the home's interval solar and load; the solar it charges from
  is what the panels can produce, which at an export-limited connection is more than the inverter recorded.
- **Swap:** "run the first round of 2,400 batteries in Yarrandale Valley, where the inverters on zero-export connections
  hold the panels to the home's use and a battery would take the rest" becomes "run the first round of 2,400 heat pumps
  in the district where the boilers are held to the radiators' draw"; the boiler, the export limit at the connection
  point and the battery's state of charge have no counterpart, and the hour-by-hour storage simulation has nothing to run
  on.
- **Layer 1:** revenue-meter half hours in market time (UTC+10 all year, the network's metering system) beside inverter
  hours on the local clock with daylight saving (the vendors' portals); one vendor's feed as lifetime watt-hour counters
  that reset when an inverter is replaced, the other in kWh per hour; a controlled-load register on a second meter
  channel (off-peak hot water); meters replaced part-way through the year under a new serial; estimated and substituted
  reads carried with quality flags; panel home identifiers keyed to network meter identifiers through the panel's
  recruitment file; connection codes for the export limit with effective dates. All produced by the systems that hold
  the data; none decides the order.
- **Layer 2:** estimation_fit, censoring and truncation: the recorded solar is held at a ceiling that moves with each
  home's own load, and the choice that flips the order is simulating the battery on the output the panels could produce,
  rebuilt for the limited homes from comparable unlimited homes under the same sky, instead of on the record.
- **Decisive step:** recognising that a zero-export home's recorded solar is inverter-limited output, a floor on what its
  panels produce, and rebuilding its available solar hour by hour from the unlimited homes' energy per kilowatt in the
  same region before simulating the battery.
- **Not semantics:** every field read correctly (the connection code says zero export, the units, clocks and channels
  handled, the replaced meters stitched) still leaves the battery simulated on the recorded flows, which is the field's
  standard method; no field, code or definition says how much solar a limited home's panels could have produced, and the
  network standard's clause that an export limit applies to exports only does not say the record is held down.
- **Not rule application:** no filed rule or procedure rebuilds a limited home's output; the guideline files the
  estimand and the battery, the network standard files what a limit applies to, and executing every stated rule on the
  recorded flows files Wennora Coast first and Yarrandale Valley last. Measured on the prototype: the enumerated family
  (recorded flows; recorded flows with the limited homes dropped; rebuilt output by regional median or mean per kW,
  orientation-matched or not) spreads Yarrandale's yield from about 980 to about 3,000 kWh a battery; the standing
  family (constructions that charge the battery from the panels' output, which the network standard's export-only limit
  requires) spreads it by under 10 kWh on a figure printed to the nearest 100; the ruling-out is not loud: it needs the
  connection codes, the standard's clause and the limited homes' clear-day output per kilowatt at about a third of their
  unlimited neighbours' read together, and that reading is the step.
- **Analyst test:** a strong analyst who aligns the clocks, converts the counters, adds the controlled load and reads
  every connection code simulates the battery on each home's recorded solar and load and ends on Wennora Coast 2027,
  Bellmere Metro 2028, Tarrock Highlands 2029 and Yarrandale Valley 2030, Yarrandale last at about 1,000 kWh a battery.
- **Estimand:** the programme guideline (section 3) files each region's round as 2,400 times the average annual energy
  the programme battery, as specified in its appendix, would deliver to the homes of the monitoring panel in that region
  over a year like 2025, and section 4 runs the rounds in order of that figure from 2027, one region a year.
- **No decoy:** nothing is planted to be caught: the export limits are the network's connection rule for the Yarrandale
  feeders, written in its standard and its register, and no memo, draft, briefing or stakeholder figure ranks the
  regions or carries the natural order.
- **No certified replay:** the method is not recovered by reproducing certified or published figures; the pack holds no
  published battery yield for any region.
- **Lesson:** a battery valued on a throttled record inherits the throttle: where an inverter holds output to a site's
  use, the recorded solar is a floor on what the panels produce and a store's value has to be simulated on the rebuilt
  output; no build on file teaches recovering a physically held-down record before a storage simulation.

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
