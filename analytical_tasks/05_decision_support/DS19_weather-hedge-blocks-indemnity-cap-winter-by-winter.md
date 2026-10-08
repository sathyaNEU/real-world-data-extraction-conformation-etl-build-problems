# DS19 — How a gas utility spreads its six weather-hedge blocks, when no winter's payout may exceed that region's extra supply cost

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · energy risk management |
| Mirrors | Spreading hedge or insurance cover across exposures when recoveries are capped by the loss actually incurred (Amazon and Apple supply-disruption cover, cloud providers' regional power-price hedges, airline fuel hedges by hub) |
| Decision shape | Allocation under a cap: six blocks of four cold-weather contracts across five supply regions, at most two blocks per region |
| Committed call | The blocks per region, and the expected recovery a winter, in $ millions to one decimal |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · S5, a cap that does not commute (recovery is the lesser of payout and incremental supply cost, winter by winter and region by region), with two grains of heating degree days (regional against index station) at rung 1 and the policy's detrending at rung 2 |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #7 uses the ready-made measure · #4 never tests its reading against the control · #13 validates on one population, applies to another · #15 follows the requester's hunch over the rule |
| Calibration form | Pilot log: last winter's four-contract pilot, with each contract's daily index-station degree-day accruals, its settlement and its region's incremental supply cost |
| Driving force | A contract pays on its index station's heating degree days, but under the master agreement's indemnity clause no region may recover more in a winter than its incremental supply cost that winter. A second block is therefore worth only what it recovers in winters where the first has not already covered the cost. Expected payout per contract, even on the right station and detrended, takes the expectation outside that cap. Winter by winter, Northgate's storage keeps its extra cost below one block's payout in most cold winters, so its second block hands back 95% of what it pays; Bayside buys spot LNG and recovers both blocks almost in full. |

## 1. Situation

A gas utility hedges its winter supply cost with cold-weather contracts bought in blocks of four under one master agreement. The board has
approved six blocks for the coming winter, with at most two in any of its five supply regions: Northgate, Bayside, Uplands, Seaboard and
Glenside. The hedging policy values the programme on expected recovery over the last 30 winters, and the supply model has priced each
region's incremental supply cost for every one of those winters on next year's system. The utility holds its regional weather series, the
index-station records named in the term sheet, and last winter's pilot log. The head of trading wants the cover where the payouts are
biggest.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the regional series, the station records,
  the term sheet, the supply model's costs and the pilot's settlements. The difficulty is that the indemnity clause turns each block's value
  into a winter-by-winter minimum, and no table states that minimum.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of trading's view. Expected payout per contract, on any series, still fills the three biggest regions
  with two blocks each, and every payout ties to the term sheet.
* **Instrument repair.** No file the ladder uses is suspect: the regional series and the station records are complete and exact for
  what each measures, the 1990s winters are correct records of colder winters that the policy detrends by method, and the supply model's
  costs and the pilot log are complete. A perfect station at every load centre and a perfect cost model move no rung (2-2-2-0-0, 2-0-2-2-0,
  2-0-2-0-2), and the winter-by-winter clause is still needed for 1-2-1-1-1.
* **Lens swap.** The naive read values the contracts' average payout. The answer values what each block keeps in each winter, a different
  population of region-winters once the cap is applied.

## 3. The driving force

A strong solver prices each region's contracts from the 30-winter burn, settles them on the term sheet's index stations rather than the
utility's regional series, detrends as the hedging policy requires, and gives two blocks to each of the three regions with the largest
expected payout. Each step is competent, and the plan claims $13.8M a winter. The pilot log confirms every settlement. But the master
agreement's indemnity clause returns, in any winter, whatever a region's payouts exceed its incremental supply cost that winter. Northgate
pays most because its continental winters are cold, yet its storage keeps its extra cost at $0.9M in a moderate winter and $6.1M in a
continental one, below what one block pays. Its second block recovers $0.17M a winter, not the $3.20M its average payout suggests. Bayside
has no storage and buys spot LNG, so its cost exceeds two blocks' payout in nearly every winter, and its second block keeps $1.49M.
Valuing every block winter by winter and region by region, then choosing the six with the largest marginal recovery, moves the cover to
one block each in four regions and two in Bayside.

## 4. The ladder

| Rung | Construction | Lands on (N-B-U-S-G) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Expected payout per contract on the utility's regional degree days, raw 30-winter burn; two blocks to each of the top three | 2-2-2-0-0; claims $17.45M, recovers $7.33M | The utility's own weather and the term sheet's payout formula | The term sheet: contracts settle on each region's index station, and the pilot settled on it |
| 1 | The same on index-station degree days (two grains) | 2-0-2-2-0; claims $15.51M, recovers $6.61M | The settlement grain the pilot confirms to the cent | The hedging policy: burn analysis uses degree days detrended to the coming winter, and two 1990s winters carry Uplands' and Seaboard's raw payouts |
| 2 | Station degree days, detrended (hygiene) | 2-0-2-0-2; claims $13.77M, recovers $6.24M | Right grain, right method, and the pilot reproduces | The master agreement's indemnity clause: a region's payout above its incremental supply cost in a winter goes back |
| 3 | **Decisive:** each block's recovery as the lesser of payout and incremental cost, winter by winter and region by region; the six blocks with the largest marginal recovery | **1-2-1-1-1; $9.52M** | — | — |

* **Figure shape.** The claimed recovery walks down at every rung (17.45, 15.51, 13.77, 9.52), and the answer is the smallest claim. On the
  recovery each allocation actually earns, the first three rungs walk down (7.33, 6.61, 6.24) and the decisive rung reverses them (+53%).
* **Position.** Bayside, which takes two blocks in the answer, has the lowest station payout of the five on rungs 1 and 2 and gets none
  there. No intermediate rung's allocation equals the answer.
* **Discriminator dominance.** Northgate's second block carries a 2.02× lead over Bayside's into rung 3 ($3.20M against $1.59M a winter in
  expected payout). Winter by winter the clause leaves Northgate's second block $0.17M and Bayside's $1.49M, an 8.8× reversal. Swing: 2.02
  × 8.8 = 17.7, against a required 1.2 × 2.02 = 2.4.
* **Partial correction priced (L3).** Applying the clause to expected payout against expected cost lands on 1-1-1-2-1 and recovers $8.66M
  (−9.1%). Applying it winter by winter without detrending lands on 1-1-2-1-1 ($8.88M, −6.7%). Applying it on the regional series lands on
  1-2-2-1-0 ($8.87M, −6.9%). No half lands on the answer.
* **Grid.** Grain (regional, station) × burn (raw, detrended) × clause (ignored, on expectations, winter by winter) gives 12 cells and nine
  distinct allocations. Only the station, detrended, winter-by-winter cell names the answer. The nearest wrong cell is the raw winter-by-winter
  cell (1-1-2-1-1, −6.7%), and it costs one omission: the detrending.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The clause sits in the master agreement's indemnity schedule as a settlement rule. No document says it changes what
   a second block is worth, and the policy's valuation section speaks only of expected payout.
2. **No sweepable corpus nominates it.** *In the pilot winter no contract's payout exceeded its region's incremental cost, because the
   winter was mild and only four contracts were placed.* The pilot log certifies settlement on the index station and is silent on the
   clause, so a solver who back-tests against it is confirmed at rung 2.
3. **No arithmetic symptom.** Payouts reconcile to the term sheet, costs to the supply model, and the pilot's settlements to the cent,
   under every rung.
4. **Not a row predicate.** It needs each winter's payout per block from daily station accruals, the region's cost that winter, the lesser
   of the two for one and two blocks, and a choice of six blocks by marginal recovery across regions.
5. **The enumeration is arithmetic.** No column gives a block's marginal recovery; each falls out of 30 winter-by-winter minima.
6. **No cutover date.** The clause has applied since the agreement was signed, and nothing in any series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot log: last winter's four contracts, two on Bayside and two on Glenside, with daily index-station degree-day accruals,
  each contract's settlement, and each region's incremental supply cost for the winter.
* **What it certifies.** Settlement is tick × station degree days above strike, capped per contract, accrued daily on the term sheet's
  station. Regional degree days reproduce none of the four settlements.
* **What it is blind to.** The indemnity clause (property 2).
* **Twin pair.** The Bayside and Glenside contracts are identical on every visible column: the same strike, tick and cap, and the same
  regional degree days for the winter (2,960). They settled at $0.30M and $0.60M (2.0×). Only the index stations separate them: Bayside's
  sits at a lakeside airport milder than its load centre, and Glenside's in a valley floor colder than its towns.
* **Every rule exercised.** Both settlements stayed under the per-contract cap, and both regions' costs exceeded the payouts, so the
  settlement rule is pinned and the clause is untouched.
* **Resemblance points at the decoy.** By regional weather Bayside looks like Uplands, and by expected payout like the cheapest cover on
  the slate, which every payout-based ranking leaves out.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The hedging policy: the programme is valued on expected recovery over the last 30 winters, on index-station degree days
  detrended to the coming winter. The board resolution: six blocks, at most two per region. The supply model's incremental cost per region
  and winter. One sentence each.
* **Empirical pins.** The settlement rule, from the pilot log.
* **Voices.** The head of trading: "Put the cover where the payouts are biggest." The Uplands regional director: "Nobody here forgets the
  1990s winters." The chief financial officer: "A hedge is always cheaper than spot LNG."
* **Licensed wrong basis.** The policy records that the board's risk committee reviews the programme on expected payout per contract from
  the utility's regional weather and will see that basis.

## 8. Determinism by construction

* **Burn window.** The 30 winters 1995–2024, filed in the policy, with no partial season.
* **Detrending.** The policy's single method (a linear trend in each station's seasonal degree days, carried to 2025), so detrended payouts
  have one value.
* **Clause.** Applied per region and per winter, as the agreement's schedule states; costs come from the supply model's filed replay.
* **Blocks.** Marginal recoveries are concave by region, so greedy and exhaustive choice agree, and the answer beats the next allocation by
  6.7%.
* **Rounding.** The expected recovery is $9.519M, filed to one decimal ($9.5M).

## 9. Prompt sketch and deliverables

> The board has approved six blocks of cold-weather cover for this winter, no more than two in any region. Our head of trading wants them
> where the payouts are biggest. Tell me how many blocks each region gets and what the programme should recover in an average winter, in
> millions to one decimal, in a line for the risk committee. Send `hedge_blocks.xlsx`, a chart `block_value.png`, and a one-page
> `hedge_note.pdf`.

* `hedge_blocks.xlsx` — the five regions' payouts and costs by winter, the 12 grid cells, the sendout sheet (ask A), the customer sheet
  (ask B) and the validity sheet (ask C).
* `block_value.png` — a bar for each region's first and second block, expected payout against recovery after the clause, with the six
  chosen blocks highlighted, plus a panel of Northgate's and Bayside's payout and cost by winter for two blocks.
* `hedge_note.pdf` — the committed allocation and figure, and why Northgate gets one block.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each region, last winter's peak gas-day sendout. *Device:* the gas day runs 09:00 to 09:00,
  and the meter log is stored in calendar days, as the operations data guide documents. Summing calendar days moves the peak to the wrong
  day in three regions.
* **Ask B (device-carried).** For each region and month end, the number of interruptible customers. *Device:* dual-fuel customers appear in
  both the firm and the interruptible registers under one premises number. Counting both registers double-counts 8–12% of them.
* **Ask C (validity).** Each region's expected payout per contract on the three bases, and each block's marginal recovery under the clause.
* **Decoupling.** Clearing the clause and the detrending changes no figure in asks A or B. Sendout and customer registers never enter a
  payout or a cost.

## 11. Rubric arithmetic

5 regions × 3 payout bases + 10 block marginal recoveries (ask C) + 5 peak sendouts (ask A) + 5 × 6 month-end counts (ask B) + the six
committed blocks and the expected recovery + 12 grid cells + 5 named chart parts + 3 files ≈ 87 criteria.

## 12. World-building constraints

* Winters: 10 mild, 8 moderate, 5 continental, 4 coastal storm, 1 general severe, 2 severe 1990s. Detrended station payout per contract
  ($M), by type and region (N, B, U, S, G): moderate 0.81, 0.52, 0.46, 0.11, 0.60; continental 2.41, 0.85, 1.03, 0.06, 1.23; coastal 0.63,
  0.13, 0.39, 2.22, 0.02; general 2.5 each; 1990s 0.23, 0.24, 0.34, 0.10, 0.27 (raw 0.69, 0.42, 2.5, 1.40, 0.38). Regional degree days
  scale station payouts by 1.0, 1.78, 1.26, 1.0 and 0.61.
* Incremental cost ($M): moderate 0.9, 4.3, 1.2, 1.2, 1.0; continental 6.1, 14.3, 10.7, 8.9, 7.1; coastal 1.1, 0.3, 0.4, 11.6, 0.9;
  general 13.2, 19.2, 14.9, 12.5, 10.2; 1990s 2.6, 2.2, 1.1, 2.7, 2.9 (raw Uplands 23.1).
* Marginal recovery per block (first, second): N 1.80, 0.17; B 1.56, 1.49; U 1.47, 0.85; S 1.70, 0.63; G 1.50, 0.45. The answer 1-2-1-1-1
  recovers $9.519M; the next allocation $8.88M.
* The twin pilot contracts are identical on every visible column. Sendout rows and customer registers never touch payouts or costs.
