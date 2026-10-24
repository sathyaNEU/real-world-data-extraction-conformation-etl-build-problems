# task484 design note: Selwick Basin Clean Air Agency's wood smoke contingency determinations (architecture 2)

Drawn 2026-10-24 on the author's standing rule (no retirement) after architecture 1 was spent at stage 4; a fresh world.
Eight candidates screened before it are in Tried and rejected.

## Draw

- **Pairing:** Physical & Environmental Sciences / `emissions-inventory`, drawn for Data Extraction & Conformation
  (ETL). The task type builds an inventory from activity data and emission factors and keeps its time series
  consistent when a method changes. ETL because the deliverable is the conformed periodic inventory in the EPA
  Emissions Inventory System nonpoint layout (area by SCC), built from sources that disagree in layout, units, keys
  and vintage, with each area's base year recalculated.
- **Objective check:** the call is a determination per area read off the conformed inventory; nothing future is
  predicted (not Forecasting), and the work is the conformation and the recalculation (not Descriptive).
- **Shape:** 03, a bridge between totals: each area's 2014 base year and 2025-26 inventory by appliance class (six
  areas by six classes, both periods), each area's reduction and determination, and the call, with the asks.
- **Decision and window:** which of the six maintenance areas, if any, trigger their contingency measure for the
  2026-27 heating season, under each plan's provision (a reduction from the 2014 base year, recalculated on the
  current methods, below the area's commitment). The quantity is retrospective with its reason: the provision reads
  the latest complete heating season's periodic inventory (2025-26), and the decision it drives (the coming season's
  curtailment rules) is forward.
- **World:** Selwick Basin Clean Air Agency, a regional clean air agency in Washington serving six PM2.5 maintenance
  areas: a registry of wood-burning devices kept since 2010 (the spine, about 27,000 devices), a stove changeout
  programme from 2015 to 2025 that funded primary-heat households first, a 2024 household survey (the current
  method's activity source) and the plans' 2014 base-year workbook (the old method, regional default cords per
  appliance). Personas from `guard.py names --geo US-WA --seed 484`: Kylie Maxwell, Mitchell Conway, Alyssa Jacobs.
- **Planned pack:** the registry (csv), the 2024 household survey (csv), the changeout applications 2015 to 2025 (csv,
  extracted from scanned forms), the 2014 base-year workbook (xlsx), the plans' contingency provision and inventory
  methods appendix (pdf), the current emission factor table, the area boundary crosswalk with the 2020 revision, an
  SCC crosswalk; distractors named in metadata.json at stage 3 (heating degree days, the curtailment log, PM2.5
  monitor daily values, firewood permit sales).
- **Deliverables:** `rwc_periodic_inventory_2025_26.xlsx` (the inventory and the recalculated base year, area by SCC)
  and `contingency_determinations_2026_27.csv` (one row per area in the agency's determination layout).
- **Card:** `.claude/skills/fingerprint/cards/task484.json` (architecture v2, lineage v1 spent), checked after
  registration: WARN only. Differentiation lines are filed against task245, task265, task139, task182, task270 and
  task452 (the same decisive gap, generator G9 and Gate G).
- **WARN answers:** repeat.gate_g and overuse.gate_g (method_or_model_selection): the mechanism carrying the stump is
  a choice among recalculation constructions for a base year, which is that key; etl_conformance would misstate it.
  repeat.question_form (which): the decision is a designation set, so the question asks which areas, with "if any"
  so that none is a grammatical answer.
- **Strategy label:** composition_mix: the survey measures the right population for 2025-26, and the error is
  carrying its class mixture of heat status back to a base year with a different mixture. population_selection would
  also read and is under ban.strategy against task275.
- **Paper screen** (scratch `t484/sim2.py`, seed 4843, a 15 per cent commitment in every area): the golden triggers A3
  and A5 (11.1 and 5.2) and clears A1 31.9, A2 27.1, A4 19.3 and A6 34.0, the same set as the world's truth (31.7,
  26.2, 13.3, 20.6, 3.0, 38.2); the survey's class means carried back trigger all six (5.5 to 11.3); the survey's
  class-and-status cells at the survey's own mix trigger all six (identical); the old regional default triggers A3,
  A4 and A5. Each half of the decisive step alone files the class-mean answer, so no partial fix moves toward the
  golden.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which serves ETL in the taxonomy.
Domain test: the quantity that decides is each area's 2014 base-year PM2.5 from residential wood combustion recalculated on the current method, the cords its base-year appliance stock burned times the current emission factors, the inventory field's time-series consistency recalculation with activity representative of the base-year source population.
Swap: "which of our six maintenance areas trigger their contingency measure" with patients for stoves and clinic visits for cords has no base-year appliance stock, no recalculation of an emissions base year on a new activity method and no changeout record of what each removed unit was, so it stops making sense.
Layer 1: the registry re-registers a device when its parcel splits (the assessor's parcel system); applications are keyed by parcel or by street address and carry heat status as a checkbox code or in words (the programme's scanned forms); the survey writes install years two ways and reported use in cords, face cords or pickup loads (the survey vendor's instrument); the 2014 workbook keeps its own layout and SCC vintage (the 2014 inventory tool); maintenance area boundaries were revised in 2020 (the state's rule); the programme reports by fiscal year while the inventory runs by heating season (the agency's budget cycle); nothing is placed to be caught.
Layer 2: estimand identification (G9 downstream survival against upstream acquisition, G6 composition shift): a class's base-year activity is a mixture of primary-heat and secondary-heat units whose mixture changed because the changeout took primary-heat units first, and the choice that flips the call is rebuilding the 2014 stock's mixture from the survivors and each changed-out unit's own recorded status, against carrying the survey's class mean or its own mixture back.
Decisive step: recalculating the base year with activity representative of the base-year source population, each 2014 appliance at the survey's cords for its class and heat status, the status of every unit changed out since read from its application.
Not semantics: with every field read correctly (cords converted, SCCs mapped, install years parsed, areas on the 2020 boundaries, heat status codes read) the easy route still applies the survey's class means, or its status cells at its own mix, to the 2014 counts and files all six areas, and no field, code, unit or definition read differently moves it.
Not rule application: the plans file the estimand (the cords each appliance in the 2014 count burned, on the current household survey method and the current factors, against the 2025-26 inventory) and say nothing on how a stock that no longer exists takes the survey's activity; on the paper world the enumerated family (class means carried back, the survey's class-and-status cells at its own mix, the old regional default, the rebuilt mixture) spans 5.5 to 31.9 points on area A1's reduction and files three different sets, the standing family is measured at stage 2, and what rules out the survey-mix constructions is the applications' own status mix (about 85 per cent primary heat against 6 to 42 per cent among the survivors), which no filed clause states.
Analyst test: A strong analyst recalculates each area's 2014 base year on the current method by applying the 2024 household survey's cords per appliance class, even split by heat status at the survey's own mix, to the plan's 2014 appliance counts with the current emission factors, which reads the survivors of a decade of primary-heat-first changeouts as the 2014 stock, and files all six areas as triggering the contingency measure where two do.
Estimand: each maintenance area's PM2.5 from residential wood combustion in the 2025-26 heating season and in the 2014 base year, the base year recalculated on the current methods (the cords each appliance in the plan's 2014 count burned, on the household survey's measure of cords burned, times the current emission factors), and the reduction from one to the other against the area's commitment, filed in the plans' contingency provision and the inventory methods appendix (pdf).
No decoy: nothing is planted; the registry, survey, applications, workbook and factors are the agency's own records as their systems produce them, no memo, draft, briefing or stakeholder figure carries a wrong answer, and the 2014 workbook is the old method's own base year, which the golden does not use.
No certified replay: no certified or published figure is reproduced to recover the method; the construction follows from the estimand and from the data.
Lesson: a recalculated base year is only as good as the population its activity describes, and when removal took one kind first the current sample describes the survivors, so the base year is rebuilt member by member from what the removal records say each member was; no build on file teaches recalculation over a stock thinned by a selective programme.

## Default path

1. Conform the registry, survey, applications and workbook: parcels and addresses resolved, cords converted, SCCs
   mapped, areas on the 2020 boundaries.
2. The 2025-26 inventory: each area's devices in use by class, times the survey's weighted cords per appliance of the
   class, times the current factors (right as it stands).
3. The 2014 base year on the current method: the plan's 2014 counts by class times the same survey cords per
   appliance (or the survey's class-and-status cells at the survey's mix), times the current factors.
4. Each area's reduction against its commitment.

Ends on: all six areas trigger the contingency measure.

## Stump sentence

The default path multiplies each area's 2014 appliance counts by the 2024 survey's cords per appliance class (or by its class-and-status cells at the survey's own mix), so the base year holds the primary-heat stoves since changed out at the survivors' mostly secondary burning, the reductions to the 2025-26 inventory shrink by 8 to 28 points, and all six areas trigger the contingency measure where only two do.

## Readability screen

Stage 2.

## Semantic fork table

Stage 2.

## Ladder

Stage 2.

## Closure table

Stage 2.

## Literal reader

Stage 2.

## Oracles

Stage 2.

## Ask sheet

Stage 2.

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
