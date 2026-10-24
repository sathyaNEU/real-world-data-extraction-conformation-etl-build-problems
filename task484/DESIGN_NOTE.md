# task484 design note: Halvard County's 2025-26 wood smoke zone determinations after a propane price spike (architecture 3)

Drawn 2026-10-24 on the author's standing rule (no retirement) after architecture 2 was spent at stage 4 on the
judge's SEND_BACK; a fresh world and mechanism. The candidates screened before it are in Tried and rejected.

## Draw

- **Pairing:** Physical & Environmental Sciences / `emissions-inventory`, drawn for Data Extraction & Conformation
  (ETL). The task type builds an inventory from activity data and emission factors. ETL because the deliverable is
  the conformed 2025-26 residential heating inventory by burn zone and appliance class (SCC), built from the
  device registry, the household survey, three propane distributors' delivery tickets in three layouts, the
  airport station's temperatures and the state tool's conversion factors, which disagree in layout, units and keys.
- **Objective check:** the call is a determination per burn zone read off the conformed inventory; nothing future
  is predicted (not Forecasting), and the work is the conformation and the season's activity estimate (not
  Descriptive or Causal: the comparison is a means of estimating one season's wood burned, not a policy effect).
- **Shape:** 07, a grid of cells: five burn zones by six appliance classes (wood burned and PM2.5), each zone's
  total against its allotment and its determination, and the call, with the asks.
- **Decision and window:** which of the maintenance area's five burn zones, if any, had 2025-26 PM2.5 from
  residential wood combustion above their zone allotment in the maintenance plan, and so take the 2026-27 stove
  changeout funds, which the county ordinance splits equally among the zones over their allotments. The quantity
  is retrospective with its reason: the ordinance reads the latest complete heating season's inventory (1 October
  2025 to 30 April 2026), and the decision it drives (the 2026-27 changeout season, opening in November) is
  forward.
- **World:** Halvard County Air Quality Program, a county program in Montana for the Halvard Valley PM2.5
  maintenance area: five burn zones (Valley Floor North and South, served by the gas utility; East Bench, West
  Bench and Upper Valley, mostly propane), a solid fuel device registry kept since 2008, a 2024-25 household
  heating survey (the latest; the program surveys every third winter), and the three propane distributors'
  delivery tickets, which the program receives for the residential propane combustion category. Winter 2025-26
  ran about four per cent colder than 2024-25 by heating degree days, and propane prices spiked from December to
  February. Personas from `guard.py names --geo us --seed 484`: Billy Davis, Kimberly Rogers, Martin Booth.
- **Planned pack:** the registry (csv), the 2024-25 survey (csv, with its weights), the delivery tickets 2023-07 to
  2026-06 from three distributors (a ticket csv, a fixed-width text export, a workbook of monthly gallons by
  account) with each distributor's service address list, the airport station's daily temperatures, the state
  RWC tool's documentation (appliance efficiencies and the energy in a cord, pdf), the state energy office's
  heating fuel equivalents sheet, the 2023 emission factor table, the burn zone parcel crosswalk, the SCC
  crosswalk, the maintenance plan's zone allotments and the ordinance (pdf); distractors named in metadata.json at
  stage 3 (the national forest's firewood permits, the curtailment day log).
- **Deliverables:** `rwc_inventory_2025_26.xlsx` (the inventory by zone and SCC, with the residential propane
  category) and `zone_determinations_2026_27.csv` (one row per zone in the program's determination layout).
- **Card:** `.claude/skills/fingerprint/cards/task484.json` (architecture v3, lineage v1 and v2 spent), checked
  before registration: WARN only. Differentiation lines are filed against task123 (the same decisive gap, G4 and
  decision type) and task152, task232 and task269 (the same decisive gap, G4 and Gate G).
- **WARN answers:** repeat.question_form (which): the decision is a designation set, so the question asks which
  zones, with "if any" so that none is a grammatical answer.
- **Data-native sentence:** the propane price spike moved part of the heat in propane-heated homes with a stove
  onto the stove, which no meter records; it shows only in the propane tickets, as deliveries falling further at
  the customers with a registered stove than at those without, where the two groups fell alike in proportion from
  2023-24 to 2024-25.
- **Strategy label:** causal_design: the season's wood burned is recovered through a difference-in-differences on
  the displaced fuel, with the comparison group (propane customers without a registered stove) and the pre-period
  check the decisive choices. Gate G decomposition_attribution: the tickets' fall is split between thrift every
  propane customer shared and a switch only the stove owners could make.
- **Paper screen** (scratch `t484v3/sub_sim2.py`, three seeds): carrying the survey's cords at the winter's degree
  days puts the benches at 39 to 47 tons and the valley floor zones at 60 to 66; adding the switch read from the
  tickets by ratio puts the benches at 57 to 72 (wood burned up 38 to 56 per cent, the world's truth within three
  tons) and the valley floor at 66 to 73 (up 6 to 12 per cent). The ratio comparison by zone and pooled agree
  within about a ton; a comparison in gallons sits within two tons of the ratio but fails the 2023-24 to 2024-25
  check at about eight standard errors (stove customers' deliveries 6 to 21 gallons higher than a level comparison
  predicts, the ratio comparison within half a per cent). The allotments are set at stage 2 so the default names
  one valley floor zone and the golden adds both benches, every golden margin at least four tons.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which serves ETL in the taxonomy.
Domain test: the quantity that decides is each burn zone's 2025-26 PM2.5 from residential wood combustion, the cords its appliances burned that winter times the 2023 emission factors, estimated for a season the household survey did not cover; a winter's fuel switching is measured where the displaced fuel is metered, a difference-in-differences on propane deliveries between customers with and without a registered stove checked on the earlier pair of winters, carried through the heat balance at the furnace's and each stove's efficiency.
Swap: "which of our five burn zones were over their wood smoke allotment" with clinics for stoves and patient visits for cords has no fuel a household switches between, no heat balance and no propane customer without a stove to compare against, so it stops making sense.
Layer 1: three propane distributors export tickets in three layouts, one as individual tickets, one as fixed-width text and one as monthly gallons per account (each distributor's billing system); service addresses are written as the distributors write them, not as the registry's parcel addresses (their customer systems); the survey reports use in cords, face cords and pickup loads (the survey vendor's instrument); the registry codes device types and keeps a status history (the county's permitting system); burn zones are defined by parcel (the ordinance's map); the station reports daily temperatures, not degree days (the airport's observing system); nothing is placed to be caught.
Layer 2: estimand identification, a difference-in-differences with a pre-period check: a season's wood burned is not measured, the survey's rates describe the winter before, and a price shock on the competing fuel moved heat onto the stoves of the homes that heat with it; the choice that flips the call is reading that switch from the propane tickets against the customers without a stove, in proportion, against carrying the survey's rates into the new winter at its degree days.
Decisive step: estimating each zone's 2025-26 wood burned as the survey's cords at the winter's degree days plus the heat the propane customers with a registered stove moved off propane, measured by how much further their deliveries fell than at the zone's propane customers without one (in proportion, as in 2023-24 to 2024-25) and carried into cords at the propane furnace's and each stove class's efficiency.
Not semantics: with every field read correctly (tickets in gallons, accounts joined to service addresses, cords converted, devices mapped to SCCs, zones from parcels, degree days from temperatures) the easy route still carries the survey's cords into 2025-26 and reads the tickets' fall as thrift in the propane category, and no field, code, unit or definition read differently moves it.
Not rule application: the ordinance and the plan file the estimand (the PM2.5 the zone's appliances in use emitted from the wood they burned in the 2025-26 season, at the 2023 factors, against the zone's allotment) and say nothing on how that winter's wood burned is estimated; on the paper world the enumerated family (the survey's cords as reported, at the winter's degree days, plus the switch read in gallons, plus the switch read in proportion pooled or by zone) spans 45 to 68 tons on the East Bench and files three different sets, the standing family (the proportional comparisons, pooled or by zone) agrees within about a ton and files one set, and what rules out the gallon comparison is the 2023-24 to 2024-25 check, which no filed clause states; the cheapest licensed member (one pooled ratio of the no-stove customers' deliveries applied to each stove customer's 2024-25 deliveries) is measured against the golden set at stage 2.
Analyst test: A strong analyst who reads every file correctly builds the 2025-26 inventory from the 2024-25 household survey's cords per appliance class, scaled by the two winters' heating degree days, times the registry's in-use appliances, uses the propane distributors' tickets only for the residential propane category, and names the valley floor zone as the only one over its allotment, where the benches' wood burning rose by about half and both are over.
Estimand: each burn zone's PM2.5 from residential wood combustion in the 2025-26 heating season (1 October 2025 to 30 April 2026), the wood burned by the appliances in use that season at the 2023 emission factors, against the zone's allotment in the maintenance plan; filed in the ordinance's changeout section and the plan's zone allotment table (pdf).
No decoy: nothing is planted; the registry, survey, tickets, temperatures and conversion factors are the program's and its suppliers' own records as their systems produce them, no memo, draft, briefing or stakeholder figure carries a wrong answer, and no filed sentence prescribes carrying the survey into a later winter.
No certified replay: no certified or published figure is reproduced to recover the method; the construction follows from the estimand and from the data.
Lesson: an unmetered fuel's use in a season the survey missed can be read off the metered fuel the households left, but only against the households that could not switch and only in proportion, as the earlier winters show; no build on file teaches recovering one fuel's use from another fuel's deliveries by appliance ownership.

## Tried and rejected

- 2026-10-20, at the draw: ET41's own world, broadband grant allocation from the FCC map: served, underserved,
  reliable technology, enforceable commitments and the location fabric are filed BEAD definitions and the base is a
  recorded count, so every lever was a filed definition, a fabric clean-up (Layer 1) or maturity of pending
  challenges; re-worlded.
- 2026-10-20, at stage 4 (architecture 1 spent): isolated reader 2 (sonnet, medium, fresh unzip) landed the call
  (Fairhaven and Linden) and all 24 ask figures. It read rule 2.2's "occupied housing units on 1 April 2026" as units
  occupied, not units existing, saw in the utility file that premises first billed after January 2021 start near
  empty while the older ones sit flat at 0.947, built the lease-up curve and applied it to every city; and it keyed
  the permits on city and parcel, which exposed every expired-and-reissued permit. Lessons: a fill record whose new
  premises begin at zero beside a flat stock is a ready-made curve one step from use, so it is the reflex, not a
  skipped step; the word "occupied" in the estimand points at it; a parcel key exposes re-issues to any hygiene
  pass. Reader 1 and the judge were stopped.
- 2026-10-24, architecture 2 draw: the payroll survey's birth-death model against the lagged QCEW census (reserved
  in task482's note). The months after the benchmark need a forecast of the net birth-death residual, and no filed
  criterion closes that carry-forward family; survey-research/etl is also under ban.pairing while task483 sits in
  the window. Not drawn.
- 2026-10-24, architecture 2 draw: a health plan's paid claims completed by received-date development after a
  processing speed-up. Spent in task451 (received-date development against the paid-date chain ladder).
- 2026-10-24, architecture 2 draw: a scanner-data price index's chain drift under sales, a multilateral index
  against linked Tornqvist. Spent in task463.
- 2026-10-24, architecture 2 draw: the variance of a year-on-year change over an overlapping member panel (a cost
  growth target read through a confidence interval). Spent in task195 (the paired difference), where a reader landed
  it.
- 2026-10-24, architecture 2 draw: rapid guessing read from response times. Spent in task479 (Gate G
  planted_defect_flip).
- 2026-10-24, architecture 2 draw: an aerial survey's intermittent plumes annualised as detections over overflights.
  That is task478 architectures 1 to 4's insight (detections over the coverage that could have seen them), and
  readers landed it there.
- 2026-10-24, architecture 2 draw: orphan wells' methane from a measurement campaign after worst-first plugging. The
  surviving wells' domain is one hygiene filter from the golden: a reader who counts unplugged wells drops the
  plugged ones from the sample too, so the reflex lands it.
- 2026-10-24, architecture 2 draw: an inventory base year recalculated after a method change, where the per-class
  recalculation (the reflex) is wrong because worst-first replacement left a cleaner surviving stock. Unspent at the
  slot screens, but its natural world is gas distribution mains, which is task476's (a niche repeat); a vehicle
  fleet's model-year rates tangle age with model year and reopen the family. Carried to the next draw as a lead, not
  drawn.
- 2026-10-24, architecture 2 ask draft (first cut pack 8b1df16c3144cafa): ask A on re-registrations linked by a
  predecessor id and ask B on a filed ACS vintage rule with labelled split block groups; ceiling.py measured the
  cracker and the mirror keeping 54 of 54 figures (pair ceiling 83.5), because every device was a field or a filed
  rule. Re-site both with silent devices (supplemental-stumping Part 3).
- 2026-10-24, ask A re-sited (second cut pack c7ccb8e1679941e1): the predecessor id removed and the split's old
  record closed as an ordinary closed record beside genuine same-day pairs; the cracker now keeps 3 of 36. Ask B unchanged.
- 2026-10-24, ask B re-sited (third cut pack 79bf825cac69ff18): the assessors' housing units keyed to 2010 block
  groups, the relationship file shipped, and every area-and-class cell given a genuine same-day pair; ceiling.py measures
  the cracker keeping 0 of 54 and a pair ceiling of 28.5.
- 2026-10-24, architecture 2 spent at stage 4 (zip 79bf825cac69ff18): both scored readers missed the call (each
  filed all six areas) and kept none of the 54 ask figures, but the judge returned NOT_DETERMINISTIC, SEND_BACK,
  competing_defensible_answer: the provision's 4.2 with the appendix's "by appliance class" executes literally as
  the survey's class mean times the plan's 2014 count, so the survivorship correction the golden makes is licensed
  by no shipped sentence, and filing that the base year means the stock that burned then, changed-out units
  included, would name the move. The judge also failed the golden's 2014 cells to one decimal (its fireplace rate
  0.372 against a class mean of 0.383, unexplained). Lesson: where the reflex is the literal execution of the filed
  estimand, the stump is a fork, not a step; the decisive population must follow from the WHAT as filed, with the
  easy route a different reading of the data rather than of the text.
- 2026-10-24, architecture 3 draw: road fuel sold at border stations to drivers from a neighbouring state (fuel
  tourism) read by a difference-in-differences around the neighbour's tax change. The swap test fails (cigarette
  sales read the same), and the territorial estimand's reading, not an analysis, decides. Not drawn.
- 2026-10-24, architecture 3 draw: a staggered rollout read with not-yet-treated comparisons against two-way fixed
  effects. Spent in task177's note.
- 2026-10-24, architecture 3 draw: a gas utility's unaccounted-for gas split into billing lag, the temperature
  under-registration of uncompensated residential meters and meter drift, leaving leaks as the residual. task476's
  gas distribution niche; the billing lag is task123's calendarization, and the temperature term executes Charles's
  law as a formula once seen. Not drawn.
- 2026-10-24, architecture 3 draw: landfill methane by first-order decay (task480's age-declining increments and
  four slot notes), capture-recapture across overlapping lists (task123, task180, task196, task253, task269,
  task448), gross flows corrected for reinterview misclassification (task244), equivalent soil mass for a soil
  carbon stock change (task279's conserved-component insight), glider kits' engine age (task474's ask device) and a
  replaceable component's own age (task132). Spent.
- 2026-10-24, architecture 3 draw: container ships' at-berth load by the reefers on board, calibrated on shore
  power meters. Rejected in task482's architecture 8 screens (a reader calibrating on the meters sees the per-call
  spread with reefers its first explanation).
- 2026-10-24, architecture 3 draw: hydropower turbine degassing of hypolimnetic methane. The pathway is either
  named by the filed estimand (then executed as a rule) or left to a reading of "reservoir emissions" (a fork, as
  architecture 2's judge ruled). Not drawn.
- 2026-10-24, architecture 3 draw: low-voltage anode effects emitting CF4 outside the potline's anode effect log.
  The cheapest licensed member is one regression with an intercept on the logged anode-effect minutes, task263's
  unmixing lesson. Not drawn.
- 2026-10-24, architecture 3 draw: flared gas booked as the balancing item of a production report and recovered
  by weighted least squares on the meters' stated uncertainties. Pro-rata and uncertainty-based allocation are both
  industry methods and the flare meter alone is a third defensible reading; filing one names the move. Not drawn.
- 2026-10-24, architecture 3 draw: N2O outside a growing-season chamber window (the spring thaw pulse) carried by
  fall-applied nitrogen. The gap is read off the estimand's dates (semantics), and the off-season transport forks
  between a ratio to the season and a ratio to fall nitrogen. Not drawn.
- 2026-10-24, architecture 3 draw: the leveraged trend of stop-loss excess claims (a reader with claimant-level
  claims trends each claimant by reflex), commercial cooking PM by device from health inspection equipment lists (a
  device-based inventory joins the season's device counts by reflex), bunching below a regulatory threshold (the
  counterfactual density's polynomial and window fork), and residential wood use moved by heat pumps or read from the
  assessor's heating type (architecture 2's heat-status variable, a composition one table hands over). Not drawn.
- 2026-10-24, architecture 3 draw: a Lunar New Year factory shutdown reaching a US port's container imports a
  Pacific crossing later, for its official seasonally adjusted series. The calendar regressor is a reflex in
  official statistics (task135, task467), and survey-research/etl sits under ban.pairing while task483 is in the
  window. Kept as a lead for task482's next architecture once the pairing frees.
