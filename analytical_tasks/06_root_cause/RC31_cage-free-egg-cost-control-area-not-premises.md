# RC31 — Which cause of the cage-free egg cost spike the sourcing fix addresses, when a supplier's uninfected farms stopped shipping too

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · grocery sourcing and supplier risk |
| Mirrors | Supplier-region concentration risk at large retailers and hardware makers (Amazon and Walmart fresh sourcing, Apple's component base), where a disruption zone stops every supplier site inside it, not only the one that failed |
| Decision shape | Which of N root causes gets the fix: one sourcing fix before next spring's contracts, five candidate causes of last year's cage-free cost spike |
| Committed call | The one cause the sourcing fix addresses, named in a sentence, with each cause's share of last year's extra cage-free egg cost |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S1 (the unit of disruption is the control area, not the infected premises), with each fix's reach behind a spatial join |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #14 coarsens the segment it was asked about · #17 guesses an attribution the data can settle |
| Calibration form | Change-log natural experiments: the chain's supply-disruption log of seven past supplier shortfalls, each with its cause and deliveries before and after |
| Driving force | The movement rule stops eggs leaving every premises within 10 km of an infected farm until the area is released, so the unit of disruption is the control area, not the infected premises. Fairmeadow, the chain's cage-free supplier, lost one complex to depopulation. Three of its uninfected complexes sat inside neighbours' control areas for 11 to 12 weeks, and they shorted the chain in the same weeks. Only a spatial and date join of detections, complex locations and release notices shows that most of the spot bill came from Fairmeadow's position in a dense cluster, not from its own losses. |

## 1. Situation

Pennick Markets sells eggs in four states, two of which allow only cage-free eggs. Last year its cage-free egg cost ran $24.0M over the
year before. The pricing team blames feed and wants feed-indexed cost-plus clauses. The supply chain team blames avian-flu losses at
Fairmeadow, which supplies most of Pennick's cage-free volume from complexes in Calder County. Before next spring's contracts, sourcing
can fund one fix: feed clauses, biosecurity co-investment at Fairmeadow, moving conventional contracts off the wholesale quote, higher
contracted cage-free cover, or a cage-free contract outside Calder County.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: deliveries, spot invoices, the contract schedule, the regulator's detections, release
  notices and its weekly count of restricted premises. The supply chain team is right that avian flu drove the spike. What is open is which
  mechanism, and so which fix.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both teams' views. Delivery shortfalls still line up in time with Fairmeadow's own detection, and the natural
  attribution still books them to its depopulation.
* **Instrument repair.** No file is suspect. Deliveries, detections, release notices and complex locations are complete and current, and no
  delivery row records why a supplier shorted. Repair them anyway at every depth. Rung 0 still names quote-indexed contracts (19.0), rung 1
  under-contracting (15.0) and rung 2 Fairmeadow's own losses (12.5). The control area is a unit built from detections, distances and
  release dates, which no row claims to record, so the decisive construction is still needed.
* **Lens swap.** The naive grain is the infected premises, the rows of the detection file. The answer's unit is every premises inside a
  control area, most of them never infected: a different population.

## 3. The driving force

A strong solver narrows to cage-free, as the question asks. It finds that cage-free contracts are cost-plus, so the wholesale quote barely
touches them, and that the spike is mostly spot buying in weeks Fairmeadow shorted. Then it attributes the shortfalls. Fairmeadow's complex
F-03 was depopulated in the same weeks the shortfalls ran, the detection file names it, and the time alignment is clean. That reading books
$12.5M to Fairmeadow's own losses and funds biosecurity. But the movement rule halts every premises within 10 km of any infected farm
until release. Two neighbouring farms' detections put Fairmeadow's uninfected complexes F-05, F-07 and F-11 inside control areas for 11 to
12 weeks, overlapping F-03's outage. Nothing in the delivery file separates the four complexes' shortfalls by cause. The split comes from
the premises register's coordinates, the detection dates and the release notices. Most of the bill is cluster exposure, which biosecurity
at Fairmeadow cannot touch.

## 4. The ladder

| Rung | Construction | Names (extra cost, $M) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Chain-wide egg category: cost change split into quote-indexed, feed pass-through and spot premium | Quote-indexed contracts (19.0; feed 9.0, spot 8.0) | The category P&L and the national quote, the most prominent figures | The labelling standard's class list and contract schedule: cage-free SKUs are on cost-plus contracts, and the question is about cage-free |
| 1 | Cage-free segment only, with spot premium booked to under-contracting | Under-contracting (15.0 against feed 7.0) | The segment asked about, and the spot bill is the obvious lever | Delivery records: 83% of cage-free spot volume was bought in weeks Fairmeadow shorted while F-03 was depopulated |
| 2 | Shortfalls attributed by premises: weeks aligned with Fairmeadow's own detection booked to its depopulation | Fairmeadow's own losses (12.5 against feed 7.0) | Clean time alignment with a named detection, and every shortfall explained | The regulator's control-area rule and release notices: F-05, F-07 and F-11 were inside neighbours' control areas for 11 to 12 weeks |
| 3 | **Decisive:** each complex's shortfall attributed by its own status (depopulated, restricted inside a control area, or neither) | **Cluster exposure (10.0 against feed 7.0)**, 5th on rung 0 | — | — |

* **Position table.** Cluster exposure is 5th on rungs 0, 1 and 2, and leads only rung 3. Margins are 2.11, 2.14, 1.79 and 1.43.
* **Discriminator dominance.** Fairmeadow's own losses carry a $12.5M lead over cluster exposure into rung 3. The control-area unit moves
  $10.0M from one to the other, a $20.0M swing, 1.60× the carried lead. The floor is 1.2×, so the edge has 1.33× headroom.
* **Partial correction priced (L3).** One solver builds control areas but ends them at the rule's 30-day minimum instead of the release
  notices. That books $3.7M to the cluster and $8.8M to Fairmeadow's own losses, which it names again, 1.26× ahead of feed. Another draws control areas only
  around Fairmeadow's own infected complex, which books $2.0M to the cluster and $10.5M to its own losses, naming them at 1.50× feed. Neither half names cluster exposure.
* **Grid.** Segment (category or cage-free) × cause grain (none, premises, control areas ended by the minimum, control areas ended by
  notices) gives 8 cells. Only cage-free with notice-dated control areas names cluster exposure.
* **Control totals.** The cage-free extra cost is $24.0M on every rung from 1 to 3, because every attribution partitions the same spot
  invoices.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The movement rule is a regulator's biosecurity text. No sourcing document says a supplier's uninfected sites can
   stop, or connects release notices to deliveries.
2. **Corpus blind for a computable reason.** *In every disruption in the log, the shorting supplier's own premises was the infected
   premises, because the earlier outbreaks struck isolated farms with no other premises within 10 km.* The premises grain and the
   control-area unit coincide in all seven cases.
3. **No arithmetic symptom.** Deliveries tie to invoices, shortfalls tie to spot purchases, and the $24.0M total is invariant under every
   attribution.
4. **Not a row predicate.** Restriction status needs each complex's distance to every detected premises, intersected with each control
   area's dates from detection to release, then mapped onto weekly shortfalls.
5. **The enumeration is arithmetic.** No field says a complex was restricted. The status comes out of the spatial and date join.
6. **No cutover date.** Detections are dated, and they are the decoy. The answer is a geometry of clustering, not a step at one date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The chain's supply-disruption log: seven past supplier shortfalls, each with the supplier's stated cause and weekly deliveries
  for twelve weeks before and after.
* **What it certifies.** The spot-premium arithmetic and the premises attribution. Shortfall × (spot − contract price) reproduces every
  logged cost within 0.5%. Booking each shortfall to the shorting supplier's own event reproduces all seven stated causes.
* **What it is blind to.** Restriction of uninfected premises (property 2).
* **Twin pair.** Complexes F-07 and F-11 are identical on supplier, flock size (1.2M hens), housing, county and detection history (none).
  Their shortfalls were 9.4M and 4.6M dozen (2.04×). F-07 sat inside two overlapping control areas for twelve weeks and F-11 inside one for
  six. Only the control-area construction reproduces both.
* **Resemblance points at the decoy.** This year's shortfall weeks most resemble the logged 2019 event: same county, the supplier's own
  detection, closed as a depopulation shortfall.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The movement rule: "No eggs leave a premises inside a control area until the area is released." The sourcing policy: "A
  fix is ranked on the extra cost of the cause it addresses." The labelling standard lists the cage-free classes.
* **Empirical pins.** The 10 km construction is pinned by the regulator's published weekly count of restricted premises, which only that
  radius and the release dates reproduce.
* **Voices.** Pricing lead: "Feed went up first and our costs followed; the correlation is right there." Supply chain director: "Fairmeadow
  lost a whole complex to the flu. That is the story." Category manager: "We were short on contract cover all year and paid for it on spot."
* **Licensed wrong basis.** The sourcing policy records that the board's audit committee reviews egg cost on the chain-wide category P&L
  and will see the fix proposal on that basis.

## 8. Determinism by construction

* **Radius.** Every Pennick supplier complex sits under 8 km or over 13 km from every detected premises, so any radius from 8 to 13 km
  selects the same complexes.
* **Release.** Every restricted complex resumed shipping within three days of its area's release notice, so shipping resumption and notice
  dates give the same weeks.
* **Overlap of causes.** F-03, the only depopulated complex, was never also restricted, and no restricted complex was depopulated.
* **Spot premium.** Invoice spot price minus the contract price for the same week and size, with no averaging choice.
* **Maturity.** Every control area was released, and every invoice settled, before year-end.

## 9. Prompt sketch and deliverables

> I can fund one egg sourcing fix before spring contracts go out, and it should hit whatever drove last year's spike in our cage-free egg
> cost. The supply chain team is certain it was the flu losses at Fairmeadow. Tell me which cause the fix should address, as a sentence for
> the sourcing committee, with what each cause cost us in millions of dollars to one decimal. Send `cagefree_cost_case.xlsx`, a chart
> `shortfall_by_complex.png`, and a one-page `sourcing_fix_memo.pdf`.

* `cagefree_cost_case.xlsx` — the five causes sized, the availability sheet (ask A), the shelf-price sheet (ask B) and the log back-test
  (ask C).
* `shortfall_by_complex.png` — weekly cage-free shortfall by Fairmeadow complex, stacked by cause (own depopulation, control-area
  restriction, other). Control-area windows are shaded, each complex's distance to its nearest detection is labelled, and the title names
  the funded cause.
* `sourcing_fix_memo.pdf` — the named cause and why each other fix buys less.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each state, segment and quarter, the share of store-days on which at least one egg SKU was out
  of stock. *Device:* SKUs in planogram changeover carry a transition status and zero on-hand by design, as the availability dictionary
  says. Counting them as out of stock adds about 3 points in two states. Store availability never enters the cost attribution.
* **Ask B (device-carried).** Average cage-free shelf price per dozen by state and quarter. *Device:* promotions sit in a separate file with
  effective date ranges that override the regular price. Using regular prices alone overstates shelf price in the two mandate states by
  6% to 9%.
* **Ask C (validity).** For each of the seven logged disruptions, its recorded cost beside shortfall × spot premium from its deliveries.
* **Decoupling.** Clearing the control-area construction changes no figure in asks A or B. Ask C's cases contain no restricted uninfected
  premises.

## 11. Rubric arithmetic

4 states × 2 segments × 4 quarters (ask A) + 4 states × 4 quarters (ask B) + 7 cases (ask C) + the named cause, the five sizes and the winning
margin + 5 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* Cage-free extra cost is $24.0M. By rung: under-contracting 15.0 / 2.5 / 2.5, Fairmeadow's own losses 0 / 12.5 / 2.5, cluster exposure
  0 / 0 / 10.0, feed 7.0, quote 2.0. Chain-wide on rung 0: quote 19.0, feed 9.0, spot 8.0.
* F-03 was depopulated. F-05, F-07 and F-11 were restricted for 11 to 12 weeks and never infected. Every complex sits under 8 km or over
  13 km from each detection.
* F-07 and F-11 are identical on every register column, with shortfalls of 9.4M and 4.6M dozen.
* The seven logged cases all have the shorting supplier's own premises infected, with no premises within 10 km.
* Changeover statuses and promotion overrides never touch deliveries, invoices or the regulator's files.
