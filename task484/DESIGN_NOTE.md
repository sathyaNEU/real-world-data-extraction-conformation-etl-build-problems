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
  programme from 2015 to 2024 that funded primary-heat households first, a 2024 household survey (the current
  method's activity source) and the plans' 2014 base-year workbook (the old method, regional default cords per
  appliance). Personas from `guard.py names --geo US-WA --seed 484`: Kylie Maxwell, Mitchell Conway, Alyssa Jacobs.
- **Planned pack:** the registry (csv), the 2024 household survey (csv), the changeout applications 2015 to 2024 (csv,
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
- **Data-native sentence:** the changeout funded primary-heat households first, so the uncertified stoves still in
  use are mostly secondary heat, while the plan's 2014 count holds every stove the programme later took; the survey
  can only see the survivors, and the applications are the one record of what each removed stove was.
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

Golden: Quarrow and Wethermoor trigger their contingency measures; Brannock, Ivelton, Saddeny and Ellick do not.

## Stump sentence

The default path multiplies each area's 2014 appliance counts by the 2024 survey's cords per appliance class (or by its class-and-status cells at the survey's own mix), so the base year holds the primary-heat stoves since changed out at the survivors' mostly secondary burning, the reductions to the 2025-26 inventory shrink by 8 to 28 points, and all six areas trigger the contingency measure where only two do.

## Readability screen

Measured on the paper world (`generator/paper_screen.py`, seed 48431; areas Brannock (A1), Ivelton (A2), Quarrow (A3), Saddeny (A4), Wethermoor (A5) and Ellick (A6),
commitments 25, 22, 20, 15, 15 and 25 per cent on paper; the generator sets Saddeny's at 13). The names are working names until the surface screen.

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the old method's base year | the 2014 counts at the plan's regional default cords, the current factors | the 2014 workbook is the plan's approved base year | readable |
| L1 class means carried back (default) | the 2014 counts at the 2024 survey's cords per appliance of each class | the provision's "recalculated on the current methods"; the survey's per-class means | readable |
| L1a status cells at the survey's mix | the same, split by heat status at the survey's own mix of primary and secondary heat | the survey's heat-status field | readable |
| L2 survivors only | the registry's survivors of 2014 at the class means, the changed-out units dropped | the registry's removal records | readable |
| L3 changed-out units at the class mean | survivors and changed-out units both counted, each at its class mean | the applications' unit counts | readable |
| L4 changed-out units at the primary-heat cell | survivors at their own mix, every changed-out unit at the primary-heat cords | the programme's primary-heat-first rule | readable |
| G golden (decisive) | survivors at their own mix (the survey's units installed by 2014) and each changed-out unit at the cords for its recorded status | the estimand's "each appliance in the plan's 2014 count" and the applications' status field; nothing announces the selection | silent |

Each half of the decisive step alone (L1a, the status split at the survey's mix; L3, the changed-out units counted at
the class mean) files the default's answer, so no partial fix moves toward the golden.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the 2014 count | the plan's approved counts by area and class (the 2014 workbook) | the registry's devices active in the 2014 season | same call (to assert at stage 3) | the provision's "each appliance in the plan's 2014 base year" |
| SF2 | the base-year burning of an appliance still in use | its burning in the survey season, not weather-adjusted | scaled by heating degree days, 2014 against the survey season | same call (to assert) | methods appendix: wood combustion activity is not weather-adjusted |
| SF3 | an appliance removed outside the programme | at its class's survivors' mix of heat status | dropped from the base | same call (to assert) | the provision counts every appliance in the 2014 base year |
| SF4 | reported use in face cords and pickup loads | a face cord is a third of a cord, a pickup load half a cord | face cords read as cords | same call (to assert) | the survey codebook |
| SF5 | an appliance's area | the 2020 boundaries | the 2014 boundaries | another set (to measure) | the provision names the areas as revised in 2020 |
| SF6 | the commitment | each plan's own percentage | one percentage for every area | another set | the provision's table of commitments |
| SF7 | falls short | a reduction below the commitment | at or below it | same call: no area sits within 5 points of its commitment (paper; asserted at stage 3) | the provision's wording |
| SF8 | the survey's grain | each area's own respondents | respondents pooled across areas | to measure (the valleys burn differently) | methods appendix: activity is estimated for each area from its own respondents |
| SF9 | the survey weights | each respondent's weight | unweighted means | same call within an area (weights are equal inside an area's stratum) | the survey documentation |
| SF10 | heat status | wood is the household's main heat source, in both the survey question and the application form | any wood heating | not computed (no file records it) | the survey questionnaire and the application form |
| SF11 | the current factors | the current table's pounds per ton by SCC, the survey's cords at the table's tons per cord | the 2014 tool's factors | another set | methods appendix |
| SF12 | the inventory period | the 2025-26 heating season | a calendar year | same call | the provision |
| SF13 | an appliance registered but not used in the season | in the class mean at zero cords | out of the count | same call (consistent in both periods) | methods appendix |
| SF14 | a changed-out unit recorded as secondary heat | at the secondary-heat cords | at the primary-heat cords | same call (L4 files the golden's set) | the application's status field |
| SF15 | a unit the programme installed, in the base year | not in it (installed after 2014) | in it at its class | the default's answer for the certified classes | the survey's install year and the programme's install dates |

## Ladder

Measured in the generator (`checks.py` on the world's clean truth, `verify.py` recomputing the golden from the cut
pack; areas Brannock, Ivelton, Quarrow, Saddeny, Wethermoor and Ellick, commitments 25, 22, 20, 13, 15 and 25 per cent).

| Rung | Areas triggering | Flips from the golden | Call kept |
|---|---|---|---|
| L0 the old method's base year | Ivelton, Quarrow, Saddeny, Wethermoor | 2 | no |
| L1 class means carried back (default) | all six | 4 | no |
| L1a status cells at the survey's mix | all six (identical to L1 inside every stratum, max gap 8.9e-16) | 4 | no |
| L2 survivors only | all six | 4 | no |
| L4 changed-out units at the primary-heat cell | Quarrow, Wethermoor | none | yes |
| G golden | Quarrow, Wethermoor | none | yes |
| T the world's true burning | Quarrow, Wethermoor | none | yes |

The golden's reductions are 42.5, 35.1, 10.6, 18.8, 4.3 and 48.0 per cent, 5.8 to 23.0 points from the commitments;
the world's truth sits 7.7 points or more from them; the default's (15.6, 17.0, 4.9, 10.4, 2.2, 14.3) sit under every
commitment. The correction tracks each area's changed-out share, not its size.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each area's appliances in the plan's 2014 base year, and those in use in the 2025-26 season | filed (the provision); SF1, SF3, SF15 |
| 2 | Unit of account | an area's PM2.5 tons from residential wood combustion | filed (the provision) |
| 3 | Attribution window | the 2025-26 heating season; the 2014 base year | filed (the provision); SF12 |
| 4 | As-of dating | the registry as of its extract date; the 2024 survey as the current method's activity | filed (methods appendix) |
| 5 | Version basis | the current factor table's edition; the 2020 boundaries | filed; SF5, SF11 |
| 6 | Denominator | the recalculated 2014 base year's tons | filed (the provision) |
| 7 | Weighting | the survey's respondent weights inside each area | filed (survey documentation); SF9 |
| 8 | Window length | one heating season | filed (the provision) |
| 9 | Boundary inclusivity | a reduction below the commitment triggers | filed; SF7, margins asserted |
| 10 | Rounding path | the determination on unrounded reductions; tons and percentages rounded only for the deliverables | the prompt's rounding sentence; asserted that no area sits within rounding of its commitment |
| 11 | Tie-break | none needed | asserted: no area at its commitment |
| 12 | Maturity and censoring | none: the season is closed | not applicable |
| 13 | Order of operations | cords converted, per-appliance means, counts, factors | same call in any order (linear); asserted |
| 14 | Row order | the inventory sorted by area and SCC | filed in the layout |
| 15 | Duplicate resolution | a device re-registered on a parcel split counted once, through the registry's predecessor field | Layer 1; asserted at stage 3 |
| 16 | Identity normalisation | applications matched to devices by parcel or by street address | Layer 1; asserted |
| 17 | Netting against gross | none: counts are of appliances in place | not applicable |
| 18 | Dimensional units | cords (face cords and pickup loads converted), tons per cord, pounds per ton, short tons | filed (codebook and factor table); SF4, SF11 |
| 19 | Code and status semantics | heat status, SCC and registry status codes | filed (codebooks); SF10 |
| 20 | Integerisation | counts are whole appliances; estimates are not integerised | not applicable |
| 21 | Clause scope | the recalculation clause covers residential wood combustion only | filed (the provision) |
| 22 | Forward window contents | the determination governs the 2026-27 season; no forward quantity is estimated | not applicable |

## Literal reader

Executing the prompt and every filed sentence word for word: the provision measures each area's reduction against
the 2014 base year recalculated on the current methods, the base year being the cords each appliance in the plan's
2014 count burned times the current factors, and the current method measures the cords burned per appliance, by class
and with the household's heat status, for the appliances in use. A literal reader asks what the 2014 appliances
burned: those still in use burn what the survey measures for their class and heat status, and each one changed out
since is known by its application's class and heat status, so each takes the survey's cords for its class and status.
That is the golden. A reader who applies the survey's class mean to the 2014 count executes the current method on the
current stock, which is not the stock the provision names.

## Oracles

No file ties only under the golden or only on a wrong read. The pack holds no recalculated base year and no area's
reduction or determination; the 2014 workbook states the old method's base year, which every route can read and none
needs to reproduce; the programme's annual reports state units changed out and vouchers paid by fiscal year, never
burning. The asks' referees are fixed with the ask sheet.

## Ask sheet

Planned on paper; the cracker and mirror sheets, the pair ceiling and the mirror leakage are measured at stage 3 by
`generator/ceiling.py` on the first cut pack, and every row is stamped with that pack's digest.

The call's declared population is each area's appliances in the plan's 2014 count and in use in 2025-26 (the
registry's devices active in the 2025-26 season, the survey's respondents, the completed changeouts' applications).
No ask computes over it: the 2025-26 tons and the recalculated 2014 tons by area and SCC are graded with the call's
critical components (the construction layer), not as asks.

| Ask | Quantity (unit, rounding in the prompt's closing sentence) | Population, outside the call's | Primary device (silent) | How it enters the call (H18) |
|---|---|---|---|---|
| A | each area's devices in place in the 2014 season by class from the registry, and the items between that count and the plan's approved 2014 count (counts) | registry rows closed before the 2025-26 season or never in it: devices superseded at a parcel split, registered after the plan's extract with an earlier install year, moved into an area by the 2020 boundary revision | D1 a re-registration at a parcel split copies the original install year onto the new device id while the old id is closed as superseded; only the predecessor field joins them | the audit trail of the 2014 counts the call consumes |
| B | each county's remainder outside the maintenance areas, 2025-26 wood burned and PM2.5 by class on the state tool's method (tons) | the counties' households outside the six areas (ACS block groups and the assessor's improvement records), which the registry does not cover | D5 block groups split by the 2020 boundary, their inside share known only from the assessor's parcels; D2 the ACS vintage the state tool names, not the latest | the inventory submission the determination is drawn from, its rows outside the areas |

Shared hazards (to place at stage 3, each moving both asks): face cords and pickup loads in reported use; parcels
keyed two ways; the programme's fiscal years against heating seasons. Each ask's prompt wording is fixed against the
golden at stage 3, with "any" so that none is a grammatical answer, and no trap word (reconcile is not used).


Measured by: `generator/ceiling.py` on the first cut pack (target.zip 8b1df16c3144cafa).

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps |
|---|---|---|---|---|
| A registry counts in place in the 2014 season | 36 | 36 | 36 | 2 |
| B remainder PM2.5 by county and SCC | 18 | 18 | 18 | 1 |
| share of ask weight (score) | 54 | 100.0 per cent (100.0) | 100.0 per cent (67.0) | 5.6 per cent |

Pair ceiling: 83.5, against the 40 the bar is built to: the layer fails as drafted.
Mirror leakage: 100.0 per cent of ask weight.
Every device in the draft is seen rather than silent: ask A's re-registrations carry a predecessor id, ask B's
release is named in the tool note and the assessor file labels each block group's part inside an area, so the
hygiene battery and the filed rules keep every figure. The asks are re-sited with silent devices before stage 4.
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
