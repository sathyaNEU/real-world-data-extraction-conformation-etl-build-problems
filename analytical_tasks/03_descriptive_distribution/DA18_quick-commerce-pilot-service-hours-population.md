# DA18 — Which metro gets the weekday quick-commerce pilot, when every density on file counts people where they sleep

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · quick-commerce network siting |
| Mirrors | Siting capacity by where customers are when they use the service rather than where they live (dark stores and lockers at Amazon and grocery delivery platforms, ride-hail driver positioning at Uber and Lyft, mobile-network small cells sized on daytime rather than residential population) |
| Decision shape | Which of N gets one scarce thing: the single dense-urban pilot, for one of six candidate metros |
| Committed call | The metro, and its delivery-weighted density (people present in service hours per km² of land, weighted by people present) |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern D (two grains, both flawless: people counted where they sleep and where they are in service hours), with E15 (harbour water inside the boundary file's tract areas, a quiet contamination with its own control) below it, pinned by Pattern B on the expansion log |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure · #13 validates on one population, applies to another · #1 reports a failed back-test, ships anyway |
| Calibration form | Change-log natural experiments: eleven expansions of the service's zones in the company's three home metros (2023–2026), each logged with its date, the tracts it added and weekly deliveries by tract for eight weeks before and after |
| Driving force | The pilot runs on weekdays from nine to six, and its deliveries go where people are, not where they sleep. The census counts people at home. Wrenmouth's waterfront district has 20,000 residents and 77,000 people present on a weekday. Every density the planning team knows is computed on residents. The expansion log shows each new tract's deliveries tracking its service-hours population (residents less those who commute out, plus workers who commute in) in all 64 tracts. On that basis Wrenmouth comes first; on the deck's it is fifth. |

## 1. Situation

A quick-commerce company delivers groceries and household goods by e-bike within twenty minutes, on weekdays from 9:00 to 18:00, from
dark stores in three home metros. It has budget for one dense-urban pilot in a new metro and six candidates: Corvale, Brantley, Port
Ellery, Wrenmouth, Gatesford and Ormsby, each with a core of tracts fixed on the planning map. The board's rule sends the pilot where
couriers will make the most deliveries per hour. The pack holds the census tract tables, the tract boundary file, the census gazetteer,
the regional commuting table (primary jobs by tract of residence and tract of work), the expansion log, the routing standard and the
board paper. The board decides on 4 February 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: residents, boundaries, land and water areas, commuting flows and the delivery counts in the
  expansion log. The real-estate team's residential density ranking is right about residents, and nobody's reading of their own
  numbers is overturned. The difficulty is which people the deliveries follow.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the strategy lead's view, the growth lead's view and the real-estate ranking. The census is still the only
  table that counts people by tract, and population-weighted density on it is still the textbook answer.
* **Instrument repair.** Perfect the census and it still counts each person at home, because that is what a census counts. The
  service-hours population is built from the commuting table, which no density measure on file uses.
* **Lens swap.** The two reads cover different populations at different moments: 1,606,000 residents at night against 1,292,000 people
  present on a weekday, of whom 352,000 have come in from another tract.

## 3. The driving force

A strong solver reads the routing standard: a courier's deliveries per hour rise with the deliveries per km² of land in each delivery's
own tract. It drops the deck's metro-wide density for population-weighted density, the textbook "density as experienced", and on the
boundary file it names Brantley. It then notices the standard says land. The gazetteer's land areas strip out the harbour water that
the boundary file leaves inside Port Ellery's and Wrenmouth's core tracts, and Port Ellery's packed harbour towers lead by twice. That is
a careful, standard measure. But the pilot runs on weekdays from nine to six. Port Ellery's harbour residents commute out by 8:30, while
Wrenmouth's waterfront district fills with 62,000 office workers and its neighbourhoods mostly work locally. The expansion log shows
deliveries in all 64 added tracts tracking residents less out-commuters plus in-commuters. Residents reproduce only 23 of them. Weighted
that way, Wrenmouth's deliveries are the densest by a third.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Residents per km² across each core, on boundary-file areas | A, Corvale (4,500, 2.13× Brantley) | The strategy deck's standard comparison | The routing standard measures density in each delivery's own tract, not across a footprint |
| 1 | Population-weighted density of residents, on boundary-file areas | B, Brantley (6,990, 1.28× Port Ellery) | The textbook density as people experience it | The routing standard counts land only, and the gazetteer's land areas exclude the harbour water inside Port Ellery's and Wrenmouth's core tracts (E15) |
| 2 | Population-weighted density of residents, on land areas | C, Port Ellery (14,230, 2.04× Brantley) | The standard's grain and area, on the census | The expansion log: residents reproduce 23 of the 64 added tracts' deliveries, and under-predict every tract with a net inflow of workers |
| 3 | **Decisive:** population-weighted density of the service-hours population (residents less out-commuters plus in-commuters, from the commuting table), on land areas | **D, Wrenmouth (11,780, 1.36× Gatesford)** (5th of 6 on rung 0) | — | — |

* **Position table.** Wrenmouth ranks 5th on rung 0 and 4th on rungs 1 and 2, and leads only rung 3. Rung leaders beat their runners-up
  by at least 1.28×.
* **Discriminator dominance.** Port Ellery carries 3.32× (14,230 against 4,280) into rung 3. On the decisive axis, service-hours density
  over residential density, Wrenmouth rises 2.75-fold and Port Ellery keeps 0.20, an edge of 13.5×. That is 3.4 times the required
  1.2 × 3.32 = 3.99. The final margin over Port Ellery is 11,780 against 2,900 (4.1×).
* **Partial correction priced (L3).** Every half-applied construction names a wrong metro. The service-hours population on boundary-file
  areas names Gatesford (8,670 against Wrenmouth's 6,600, 1.31×). Adding in-commuters without removing out-commuters names Port Ellery
  (14,590 against 11,020, 1.32×). Counting in-commuting workers alone names Gatesford's office district (20,090 against 15,470, 1.30×).
  Removing out-commuters without adding in-commuters names Brantley (4,990 against 3,670, 1.36×). The service-hours population as a
  metro-wide density names Corvale.
* **Grid.** Density form (metro-wide or population-weighted) × area (boundary file or land) × population (residents or service hours)
  gives 8 cells. The four metro-wide cells name Corvale, and the population-weighted cells name Brantley, Gatesford, Port Ellery and,
  only with land areas and the service-hours population, Wrenmouth.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The routing standard defines density at the delivery's tract, per km² of land. The service description gives the
   hours. No document says whose presence the deliveries follow, and none mentions the commuting table.
2. **Reproduction, and why it is a construction.** The service-hours population reproduces all 64 added tracts' deliveries within 3%.
   Residents reproduce 23, residents plus in-commuters 31 and in-commuters alone 9, and residents under-predict the log's total by 22%,
   every miss on a tract with net inflow running the same way. The reproducing quantity is a tract's residents less its residents' flows
   out plus everyone else's flows in, two opposite group-bys of the commuting table combined. No column carries it.
3. **No arithmetic symptom.** Census totals reconcile, the commuting table's flows sum to each tract's employed residents and jobs, and
   every rung's arithmetic is clean.
4. **Not a row predicate.** A tract's service-hours population depends on flows to and from every other tract. No row in any file holds
   it.
5. **The enumeration is arithmetic.** 352,000 in-commuters and 666,000 out-commuters across the six cores are placed by the table, not by a
   field.
6. **No cutover date.** The expansions are spread over four years, and the commuting pattern is the same in every one.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the census is still the population table.

## 6. The calibration corpus

* **Form.** The expansion log: eleven expansions of the zones in the company's three home metros, 2023–2026, each with its date, the 64
  tracts it added and weekly deliveries by tract for eight weeks before and after.
* **What it pins.** That deliveries follow the service-hours population: 290 deliveries a week per 1,000 people present, within 3% in
  every added tract, and no change in the zones' existing tracts. It also refuses the rivals in aggregate (above).
* **Twin pair.** Added tracts H-17 and K-04 are identical on every census and gazetteer column: 4,200 residents, the same households, ages,
  land area (0.70 km²) and water. K-04 sits beside an office park and draws 3,900 in-commuters, H-17 draws 900, and both send out 2,100.
  Their deliveries were 1,740 and 870 a week (2.0×). Only the service-hours population separates them.
* **Resemblance points at the decoy.** On every census column, Port Ellery's harbour towers most resemble the dense residential zones
  where the service first launched in its home metros, its busiest zones today.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board paper: "The pilot goes to the candidate metro where couriers will make the most deliveries per hour." The
  routing standard: "A courier's deliveries per hour rise with the density of deliveries around each delivery: the deliveries per km² of
  land in the delivery's own tract." The service description: weekdays, 9:00 to 18:00. The planning map fixes each candidate's core
  tracts.
* **Empirical pins.** The service-hours population, from the expansion log.
* **Voices.** The strategy lead: "Wherever people live packed together, couriers will be busy." The growth lead: "Port Ellery's harbour
  towers are where our customers have always been."
* **Licensed wrong basis.** The board paper records that the real-estate team ranks metros by residential population-weighted density
  and will present that ranking at the board.

## 8. Determinism by construction

* **The construction.** Residents of a tract less its residents who work in another tract, plus workers living in another tract. People
  who live and work in one tract, and people not in work, stay. The commuting table holds primary jobs only, so no worker counts twice.
* **Areas.** Land area from the gazetteer. The boundary file's polygon areas include water, and the routing standard says land.
* **Core tracts.** Fixed by the planning map, so no boundary choice moves a metro.
* **Telework and students.** The table as published reproduces the log, and any telework or school adjustment reproduces fewer tracts.
* **Margins.** Every rung's leader and every partial's leader is at least 1.28× ahead of its runner-up, so no rounding or area
  convention can reorder them.

## 9. Prompt sketch and deliverables

> Where should our one dense-urban pilot go? We have six candidate metros, the board decides on 4 February, and our strategy lead is sure
> that wherever people live packed together our couriers will be busy. Tell me which metro gets the pilot and its delivery-weighted
> density, people per km² to the nearest hundred, in a sentence for the board paper, and send `pilot_siting.xlsx` with the sheets below
> and a chart `density_by_basis.png`.

* `pilot_siting.xlsx` — the six metros under each rung's construction with the expansion log's reproduction counts (ask C), the
  availability sheet (ask A) and the refunds sheet (ask B).
* `density_by_basis.png` — each metro's density on residents and on the service-hours population as paired bars, the expansion log's
  64 tracts as a scatter of deliveries against both populations, K-04 and H-17 marked, and the chosen metro highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** The share of the catalogue in stock at 10:00 on each weekday of September 2026, for each of the
  nine dark stores in the home metros. *Device:* an item a supplier suspends is flagged delisted for the suspension window and returns
  under the same item number, and the availability guide takes delisted items out of the catalogue. Counting them as out of stock
  understates availability by 2 to 6 points on 31 of the 36 store-weeks.
* **Ask B (device-carried).** Refunds by reason (missing item, damaged, late, wrong item) and month, July to December 2026. *Device:* a
  partial refund later topped up to a full refund is two rows under one refund case, as the refunds guide documents. Summing rows
  double-counts 11% of refunded value and moves 17 of the 24 cells.
* **Ask C (validity).** Each metro's density under each of the four rung constructions, the expansion log's reproduction count for each
  population (service hours, residents, residents plus in-commuters, in-commuters), and K-04's and H-17's deliveries against each.
* **Decoupling.** Stock, refunds and the census, commuting table and expansion log share no row. Clearing the service-hours construction
  changes no figure in asks A or B.

## 11. Rubric arithmetic

9 stores × 4 weeks (ask A) + 4 reasons × 6 months (ask B) + 6 metros × 4 constructions, 4 reproduction counts and 2 twin figures
(ask C) + the committed metro, its density and its margin + 4 named chart parts + 2 files ≈ 99 criteria.

## 12. World-building constraints

* Densities (people per km²) by rung, Corvale / Brantley / Port Ellery / Wrenmouth / Gatesford / Ormsby: rung 0: 4,500 / 2,110 / 2,080 /
  1,530 / 1,360 / 1,610; rung 1: 4,500 / 6,990 / 5,450 / 3,030 / 2,560 / 2,230; rung 2: 4,500 / 6,990 / 14,230 / 4,280 / 2,560 / 2,230;
  rung 3: 4,150 / 6,480 / 2,900 / 11,780 / 8,670 / 2,150.
* Partials as in section 4: Gatesford 8,670 (boundary areas), Port Ellery 14,590 (residents plus in-commuters), Gatesford 20,090
  (in-commuters alone), Brantley 4,990 (residents less out-commuters).
* Wrenmouth's waterfront district: 2.5 km² of land and 2.5 of water, 20,000 residents, 5,000 out-commuters, 62,000 in-commuters. Port
  Ellery's harbour core: 3 km² of land and 7 of water, 110,000 residents, 88,000 out-commuters, 4,000 in-commuters.
* Core residents: 180,000 / 262,000 / 350,000 / 310,000 / 254,000 / 250,000; service-hours population: 166,000 / 204,000 / 170,000 /
  307,000 / 221,000 / 224,000.
* Expansion log: 64 added tracts, 290 deliveries a week per 1,000 people present (±3%). K-04 and H-17 are identical on every census
  column.
* Stock and refund records touch no census, commuting or expansion row.
