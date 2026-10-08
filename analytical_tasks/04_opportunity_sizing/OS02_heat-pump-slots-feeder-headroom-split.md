# OS02 — How to split 1,800 heat-pump rebate slots across four districts, when the homes that want them sit on feeders that cannot take them

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · residential heat-pump retrofit markets |
| Mirrors | Allocating a capped launch quantity across sales regions when what can be fulfilled is limited at a node nested below the region (EV-charger and smart-appliance programmes gated by distribution transformers, fibre rollouts gated by cabinet ports, capacity launches at Google Cloud and AWS gated by per-rack power) |
| Decision shape | An allocation under a cap: 1,800 rebated install slots split across four districts before the programme year opens |
| Committed call | The slots each district receives, and the rebated heat pumps installed in the year, to the nearest ten |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · S5, a per-feeder ceiling that does not commute with district totals, over finer published controls that separate the joint distribution from the product of marginals (#12) |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #12 stops at the first control that passes · #10 notes a binding limit as a risk · #13 validates on one population, applies to another |
| Calibration form | Pilot log: every qualified household in last year's six pilot neighbourhoods, with its heating system, purchase outcome and connection date |
| Driving force | A rebate is paid only on a heat pump the network connects in the year, and each connection takes 5 kW of the serving feeder's hosting headroom. Summed to districts, headroom exceeds demand everywhere. Feeder by feeder, the old neighbourhoods where the best prospects live are full, so a district can place only the slots of its full feeders plus the buyers on feeders with room. The neighbourhood → feeder grouping is reached through the utility's feeder map, and nothing states that the binding happens at feeder grain. |

## 1. Situation

An installer delivers a utility's heat-pump retrofit programme and holds 1,800 rebated install slots for next year. It must split them
across four districts, North Shore, Valley, Lakes and Uplands, before the year opens. The strategy deck sized each district by
multiplying published percentages (oil or resistance heat, owner-occupied, detached, income above the line) and assumed 2% uptake. A
weighted household survey, stratified by planning neighbourhood, carries all four attributes and the heating system type. Last year's
pilot sold to qualified households in six neighbourhoods. The utility publishes a hosting-capacity map by feeder.

## 2. Gate G: why this is legal

* **Litmus.** Every reported figure is correct: the published tables, the survey, the pilot's sales and connections, and the hosting
  map. No stakeholder read is overturned. The difficulty is that installs can only land where a feeder has room, and that room has to
  be counted feeder by feeder.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the deck and every voice. The survey and the pilot still produce a confident split of all 1,800 slots, and
  district totals of the hosting map still show no binding.
* **Instrument repair.** Survey every household and measure every feeder exactly. Demand and headroom are already exact; the binding
  still lives at a grain the allocation never forms.
* **Lens swap.** The naive read is households who would buy. The answer is households who would buy on a feeder with a free slot in
  the coming year, a different population.

## 3. The driving force

A strong solver rejects the deck's product of percentages because the survey reproduces the two-way tables and the product does not.
It replaces the flat 2% with the pilot's conversion by heating system, which the pilot certifies, and it shares the 1,800 slots in
proportion to expected buyers. It may even check the hosting map, summed to each district, and find headroom to spare everywhere.
But headroom cannot move between feeders. Ducted and hydronic oil homes cluster in old neighbourhoods on feeders with a few slots
left, while the headroom sits on newer feeders with few qualified homes. Per feeder, rebated installs are the smaller of buyers and
slots. That sum is 1,300 installs, so 500 slots cannot be placed this year, and the split moves to Lakes.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Product of the published one-way shares × households × 2% uptake, slots shared in proportion | NS 430 · VA 640 · LA 480 · UP 250; 1,800 installs (+38.5%) | The deck's method, and it reproduces the published oil-and-resistance counts (Table H1) exactly | Tables H2 (fuel × tenure) and H3 (tenure × structure): the product misses every two-way cell by 18–45% |
| 1 | Survey joint counts of qualified households × 2% | NS 620 · VA 470 · LA 460 · UP 250; 1,800 (+38.5%) | Reproduces H1, H2 and H3 to the household | The pilot log: conversion runs 8.0% for ducted oil, 3.0% for resistance and 1.0% for hydronic oil, never a flat 2% |
| 2 | Survey joint counts by heating system × pilot conversion | NS 440 · VA 450 · LA 360 · UP 550; 1,800 (+38.5%) | Certified by the pilot, every neighbourhood within 4% | The hosting map, joined through the neighbourhood → feeder map: 60% of expected buyers sit on feeders with fewer slots than buyers |
| 3 | **Decisive:** per feeder, the smaller of expected buyers and hosting slots (headroom ÷ 5 kW), summed to districts | **NS 210 · VA 350 · LA 470 · UP 270; 1,300 installs, 500 slots unplaced** | — | — |

* **Figure shape.** The answer is the minimum cell of the grid. Every rung below it commits all 1,800 slots, so every partial reading
  lands on the same wrong figure (+38.5%).
* **Leaders.** The district receiving most slots changes at every rung: Valley (1.33×), North Shore (1.32×), Uplands (1.22×), Lakes
  (1.34×).
* **Discriminator dominance.** Uplands carries 1.54× more expected buyers than Lakes into rung 3 (800 against 520). Lakes can place
  0.90 of its buyers against Uplands' 0.34, an edge of 2.68×, 1.45 times the 1.85× floor. Product: 2.68 / 1.54 = 1.74, Lakes 470 against
  Uplands 270.
* **Partial correction priced (L3).** A solver who checks the hosting map at district level finds headroom above demand in every district
  (North Shore 850 slots for 640 buyers, Uplands 970 for 800) and stays exactly at rung 2.
* **Grid.** Shares (product, joint) × uptake (flat, pilot) × headroom (none, district, feeder) gives 12 cells. Eight cells commit 1,800
  (+38.5%). With feeder capping, product × flat still fills the cap (+38.5%), product × pilot lands at 1,670 (+28.5%), and joint × flat
  at 1,480 (+13.8%), the nearest wrong cell, which needs the flat uptake the pilot refutes in all six neighbourhoods.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The connection standard says each heat pump is assessed at 5 kW of winter design load against the published
   hosting capacity. No document says at what grain, or that slots follow connections.
2. **Corpus blind for a computable reason.** *In every pilot neighbourhood the serving feeder had at least three times the slots the
   pilot's buyers used, because the pilot was sited on the six feeders rebuilt with larger transformers under the 2022 storm-hardening
   programme.* All 168 pilot buyers connected within ten weeks.
3. **No arithmetic symptom.** Survey weights sum to district households, the survey reproduces H1–H3, pilot buyers tie to the sales
   ledger, and district headroom exceeds district demand in every district.
4. **Not a row predicate.** Neighbourhoods are grouped to feeders through the feeder map, buyers summed per feeder, a minimum taken
   against each feeder's slots, and the minima summed to districts.
5. **The enumeration is arithmetic.** No column marks a home as connectable, and the survey has no feeder field.
6. **No cutover date.** The hosting map is a single published snapshot, the reinforcement schedule touches no saturated feeder before
   year-end, and no series steps.
7. **Survives deletion.** Removing the deck, the voices and the published tables leaves the pilot certifying an uncapped split.

## 6. The calibration corpus

* **Form.** The pilot log: 3,000 qualified households in six neighbourhoods, each with heating system, purchase outcome and connection
  date.
* **What it certifies.** Conversion by heating system: 144 of 1,800 ducted oil homes (8.0%), 18 of 600 resistance homes (3.0%), 6 of
  600 hydronic oil homes (1.0%). Segment rates reproduce all six neighbourhoods within 4%. A flat 2% predicts 60 buyers against 168 and
  misses all six by at least 50%, so it fails on the total too.
* **What it is blind to.** Feeder binding (above).
* **Twin pair.** Planning areas Elm Park (North Shore) and Birchwood (Valley) are identical on households, heating-system mix, expected
  buyers (160) and total hosting slots (160). Elm Park's buyers sit 140 on a feeder with 25 slots and 20 on one with 135, so it places
  45. Birchwood's sit 100 on a feeder with 35 and 60 on one with 125, so it places 95, 2.1× more. Only the per-feeder minimum separates
  them.
* **Resemblance points at the decoy.** The pilot's ducted-heavy homes most resemble Uplands, the rung-2 leader.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rules: a rebate is paid when the heat pump is connected, and slots unpaid at year-end lapse. The
  allocation rule: each district receives slots equal to its expected rebated installs, in tens, and where those together exceed 1,800
  the slots are shared in proportion by largest remainder. The connection standard: each heat pump is assessed at 5 kW of winter design
  load against the published hosting capacity.
* **Empirical pins.** Conversion by heating system, from the pilot. Feeder slots, from the hosting map.
* **Voices.** The programme manager: "Valley has always had the most homes we can convert." The installers' association: "Our crews
  can install every rebate you fund."
* **Licensed wrong basis.** The programme filing records that the state energy office apportions its matching funds on Table H1's
  oil- and resistance-heated household counts and will present that split at the review.

## 8. Determinism by construction

* **The hole.** Every feeder's expected buyers are either at least twice its slots or at most half of them, under every demand model in
  the grid. The smaller of expected buyers and slots therefore equals the expected smaller of the two, whatever order applicants arrive
  in.
* **Feeder map.** Each neighbourhood is served by exactly one feeder and each feeder lies in one district, so no buyer splits.
* **Whole installs.** Survey weights and pilot rates are built so every feeder's expected buyers is a whole number and every district's
  answer is a multiple of ten.
* **Snapshot.** The hosting map is dated before the year opens, and the reinforcement schedule finishes no saturated feeder in the year.
* **Survey rivals.** A partial joint (fuel × tenure from H2, with structure and income independent) reproduces H1 and H2 and misses H3
  by 12–30%, so only the full joint survives the published tables.

## 9. Prompt sketch and deliverables

> Before the programme year opens I have to split our 1,800 heat-pump rebate slots across the four districts, and our programme manager
> has always put the most in Valley. Give me the slots each district gets and how many rebated heat pumps we will actually put in this
> year, to the nearest ten, as a line I can file. Send `slot_split.csv`, the chart `district_slots.svg`, and a two-page
> `slot_note.docx`.

* `slot_split.csv` — one row per district: slots, expected buyers and rebated installs under each of the four rung bases, plus the
  invoice-cost rows (ask A) and the processing-time rows (ask B).
* `district_slots.svg` — a script-rendered stacked bar per district: expected buyers split into placeable and blocked by full feeders,
  with the slot allocation as a marker, the 1,800 cap as a reference line, the 500 unplaced slots annotated, and Elm Park and Birchwood
  called out.
* `slot_note.docx` — the committed split, the installs figure, and why the 500 slots cannot be placed this year.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each district, last year's average installed cost per heat pump for ducted, ductless and
  hydronic-replacement jobs, from the contractor invoices. *Device:* multi-zone ductless jobs are invoiced one line per indoor head, and
  the contractor price guide defines a multi-head system as one install. Counting lines as installs understates ductless cost per
  install in two districts.
* **Ask B (device-carried).** For each district, last year's median days from rebate application to payment and the share paid after 30
  days. *Device:* an application resubmitted after a document request gets a new ID that carries the original as `parent_application_id`,
  as the ticket guide documents. Treating resubmissions as new applications halves the median in two districts.
* **Ask C (validity).** The slot split and rebated installs under each of the four rung bases, and the pilot back-test (neighbourhoods
  within 5%, of 6) for flat uptake and for conversion by heating system.
* **Decoupling.** Removing the feeder cap changes no figure in asks A or B. Invoices and rebate tickets cover last year's jobs and touch
  neither the survey nor the hosting map.

## 11. Rubric arithmetic

4 districts × 3 job types (ask A) + 4 × 2 (ask B) + 4 bases × 5 figures (ask C) + the committed split (4), the installs figure and the
unplaced slots + 2 back-test counts + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Expected buyers (saturated feeders, roomy feeders) under joint × pilot: North Shore 520 / 120, Valley 380 / 280, Lakes 70 / 450,
  Uplands 600 / 200. Saturated-feeder slots: 90, 70, 20, 70. Roomy-feeder slots: 760, 1,050, 1,300, 900.
* Under joint × flat: 600 / 200, 270 / 330, 60 / 540, 160 / 160. Under product × flat: 320 / 300, 420 / 500, 50 / 640, 150 / 200.
  Under product × pilot: 400 / 200, 590 / 420, 70 / 560, 640 / 240.
* Every feeder sits outside the 0.5–2× band of buyers to slots under every model; district headroom exceeds district demand under every
  model.
* Rung leaders are Valley, North Shore, Uplands, Lakes, each at least 1.22× clear. No largest-remainder tie at any rung.
* Pilot: 3,000 households (1,800 ducted oil, 600 resistance, 600 hydronic oil), 168 buyers, all connected, all on rebuilt feeders.
* Elm Park and Birchwood match on every survey and pilot-visible column and on total slots.
* Invoices and rebate tickets never touch survey, feeder or pilot records.
