# FC24 — Where the supplier's 24 discounted fuel loads go after the wholesale drop, when a card account keeps its rebate only while every card clears the floor

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · fleet fuel procurement |
| Mirrors | Allocating a discounted supply when a volume rebate holds only while every member of an account clears its own minimum (fuel-card programmes at parcel and rental fleets, cloud committed-use discounts that need every project above a floor, marketplace seller tiers that lapse when any listing falls short) |
| Decision shape | An allocation under a cap: 24 discounted tanker loads across six depots for the eight weeks after the drop, at most eight per depot |
| Committed call | Loads per depot (D1–D6), adding to 24, and the eight-week saving they book, in $ thousands |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · a minimum over sub-units: a card account keeps its rebate in a month only if every card in it buys at least 400 gallons on the network, so a load that drains one depot's vans can cost a whole account its rebate; with a mixed van segment split through the vehicle register below it |
| Gate G mechanism | binding_constraint, with forecasting support |
| Measured traps engaged | #3 stops at a close but inexact match · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Change-log natural experiments: the fleet's three earlier bulk programmes, each logged with card purchases by vehicle before and after and the card provider's monthly rebate statements |
| Driving force | Card accounts earn 8¢ a gallon on every card gallon in a month when every card buys at least 400 gallons on the network. The statements show cards and totals, and the account averages sit far above 400, but the urban vans at D2 buy 450 and the diesel vans at D5 buy 800. One load at D2 takes its vans to 306 and costs the West account $19,758, three times the load's saving; a fourth load at D5 costs the East account $22,792. Per-card volumes come only from grouping the transaction file by card, and the floor is recovered from the statements, where the 2021 programme cost West its rebate while every account total cleared the tier. |

## 1. Situation

A delivery fleet buys fuel on network cards and, at six depots, from bulk tanks. Wholesale prices have just fallen 60¢, and the bulk
supplier has offered 24 tanker loads of 8,000 gallons at the new rack price over the next eight weeks. A depot can take at most eight, and
no more than its own vehicles would otherwise buy on cards there. The procurement standard places loads one at a time at the depot where
the next load lowers the fleet's fuel cost the most. The procurement memo files the retail-price model: a regression of card prices on
wholesale. The six depots sit in three card accounts: West (D1, D2), Central (D3, D4) and East (D5, D6).

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: card transactions, the vehicle register, the rebate statements, the price history, the bulk
  contract and the change log. No one's claim about their own numbers is overturned. The difficulty is a rebate that a single card can
  lose for a whole account.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. Asymmetric pass-through with D5's diesel vans split out still sends nine
  loads to the van depots, and the account totals still clear the tier.
* **Instrument repair.** Suspect: the card transaction file, whose product field reads "fuel" for every purchase, where half of D5's vans
  burn gasoline. Record the product: rung 0 then returns 0 · 3 · 0 · 8 · 6 · 7 and rung 1 becomes rung 2's 8 · 3 · 0 · 0 · 6 · 7, neither
  the answer. The statements are not suspect: each records the rebate the account earned that month, which is the decision's own
  attribute, and the transactions hold every card purchase, so per-card volumes are a grouping, not a recovery. The every-card floor is
  still a construction, needed for the answer.
* **Lens swap.** The naive read and the answer differ in population: an account read through its totals and average, against the
  account's weakest card in each month.

## 3. The driving force

A strong solver replaces the memo's instant pass-through with the asymmetry the price history shows (card prices fall at a third the
speed they rose), finds that only D5's diesel vans can use bulk diesel, and places loads where card prices will stay highest. That sends
three loads to D2's vans and six to D5's. Each also costs a rebate. The card provider pays 8¢ a gallon on all of an account's card gallons
in any month when every card in it bought at least 400 gallons on the network. The statements carry only an account's cards, total and
tier, and on those West, at 1,900 gallons a card, looks safe. Its 30 vans at D2 buy 450 gallons a month each. A single load drains 144
from each, every van falls below the floor, and West loses $19,758 over the eight weeks against a load's $6,480 saving. D5's 35 diesel
vans buy 800, so three loads leave them at 429 and a fourth costs East $22,792. The rule is in no document. It is recovered from the
statements of the fleet's earlier programmes, where in 2021 West lost its rebate in both bulk months while its total and average stayed
three times the tier, and only an every-card floor reproduces all 72 account-months.

## 4. The ladder

| Rung | Construction | Lands on (D1 · D2 · D3 · D4 · D5 · D6 loads; true saving) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The memo's regression (card prices fall at once to rack plus margin), loads placed by saving net of delivery fee | 0 · 3 · 0 · 8 · 8 · 5; $67k | The filed price model, the standard's rule | The price history: after each of the last nine wholesale drops, card prices fell at a third the speed they rose, slowest in the West |
| 1 | Asymmetric pass-through by region (West 50¢, Central 26¢, East 34¢ above equilibrium over the eight weeks) | 8 · 3 · 0 · 0 · 8 · 5; $80k | The price model the history supports, every saving forward-looking | **E29 (a mixed segment split through a join):** the vehicle register shows 35 of D5's 70 vans run on gasoline, and the bulk contract supplies on-road diesel only |
| 2 | D5's displaceable fuel limited to its diesel vans | 8 · 3 · 0 · 0 · 6 · 7; $89k | Every load displaces fuel it can replace, and each account's total and average stay far above 400 gallons a card | The 2021 statements: West lost its rebate in both bulk months while its total and average stayed three times the tier |
| 3 | **Decisive:** each load's saving net of the rebate an account loses when any of its cards falls below 400 gallons a month, per-card volumes from the transactions | **8 · 0 · 0 · 5 · 3 · 8; $123,760 → $124k** | — | — |

* **Figure shape.** The van depots (D2 and D5) take 11, 11 and 9 loads on the lower rungs and 3 at the decisive rung, and no other cell
  gives them fewer. Every lower rung costs both the West and East rebates, so its true saving is $67k–$89k against $124k.
* **Partial correction priced (L3).** Applying the floor but to all 70 of D5's vans names 8 · 0 · 0 · 2 · 6 · 8 ($103k), because D5's
  diesel vans then look able to take six loads. Counting a lost rebate only on the depot's own cards names 8 · 3 · 0 · 2 · 3 · 8 ($110k),
  since D2's loss then looks smaller than its saving. Applying the floor on the memo's instant pass-through names 5 · 0 · 0 · 8 · 3 · 8
  ($119k).
* **Grid.** Price model (instant, asymmetric) × D5 vans (all, diesel only) × rebate law (none, account average or total, depot's own
  cards, every card in the account) gives 16 cells. Only the asymmetric model with diesel vans and the every-card floor gives the answer;
  every other cell moves at least three loads.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The card contract speaks of "accounts meeting the network volume tier"; no document says the tier is tested card
   by card or that bulk fuel can break it. The change log ships as the procurement record of past programmes.
2. **The reproduction numbers.** The every-card floor reproduces all 72 account-months of rebates in the three earlier programmes; the
   account-total and average-card laws reproduce 70 and miss both West months of 2021. The floor is a construction: transactions grouped
   by card, each card's monthly network gallons, the account's minimum. No statement column holds it.
3. **No arithmetic symptom.** Gallons tie to invoices, loads to the supplier's offer, and every account's total clears the tier under
   every rung.
4. **Not a row predicate.** The rebate depends on the smallest of an account's card volumes after each load's displacement is spread over
   its depot's vehicles, and its cost falls on every card in the account.
5. **The enumeration is arithmetic.** Which loads break which account is computed from per-card volumes and displacement. No column says
   "at the floor".
6. **No cutover date.** The wholesale drop is dated, and it is the decoy for the price model; the floor binds only through next weeks'
   displaced purchases.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The change log of three earlier bulk programmes (2019, 2021, 2023): loads by depot and month, card purchases by vehicle before
  and after, and the provider's monthly rebate statements, 72 account-months in all.
* **What it certifies.** Displacement: each load replaced its depot's card purchases one for one, spread evenly over the vehicles that
  fuel there. The rebate rule: an account earns 8¢ a gallon in a month only if every card bought at least 400 network gallons.
* **What the rivals fit.** The total and average laws fit 70 of 72 account-months, because in 2019 and 2023 no card came near the floor.
* **Twin pair.** In 2021 West and Central each took six loads and were identical on every statement column: about 95 cards, 130,000
  gallons a month and an average card of 1,370. Their net savings were $17,800 and $35,600 (2.0×), because one West van depot's cards fell
  below 400. The account totals give both $35,600; only the every-card floor reproduces both.
* **Resemblance points at the decoy.** This year's West account matches 2019's Central on every statement column, an account that took
  bulk fuel and kept its rebate.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The procurement standard: loads go one at a time where the next load lowers the fleet's fuel cost most, at most eight
  per depot and no more than the depot's vehicles would buy on cards. The bulk contract: on-road diesel, 8,000-gallon loads, delivery fees
  by depot. The card contract: 8¢ a gallon for accounts meeting the network volume tier. The memo: card prices by regression on
  wholesale.
* **Empirical pins.** Pass-through by region, from the price history. Engine types, from the vehicle register. The floor and the
  displacement, from the change log.
* **Voices.** The fleet manager: "The vans are where we pay the most at the pump; that's where bulk pays off." The finance analyst:
  "Our accounts are three times over the tier. The rebate isn't at risk."
* **Licensed wrong basis.** The standard records that finance budgets bulk savings as loads times the price gap at each depot, rebates
  aside, and will present the budget on that basis.

## 8. Determinism by construction

* **Floor margins.** At every threshold the affected cards sit at least 29 gallons from 400 on either side (D2's vans at 450 before a
  load and 306 after; D5's diesel vans at 429 after three loads and 306 after four), so rounding of volumes cannot move a load.
* **Displacement.** Loads spread over a depot's vehicles that fuel there, evenly, as every earlier programme did.
* **Order.** Per-load savings differ by at least $320 at every placement in the answer, so the greedy order is fixed.
* **Rebate months.** The eight weeks span 1.85 rebate months, and every rung's rebate loss counts both months whole, as the statements
  do.
* **Maturity.** The price history and the earlier programmes' statements are final.

## 9. Prompt sketch and deliverables

> The bulk supplier has given us 24 loads at the new rack price for the next eight weeks, and I have to tell them by Friday which depots
> get how many, and what it saves us. Our fleet manager says the vans are where bulk pays off. Send me `bulk_load_plan.xlsx`, a chart
> `card_floor_check.png`, and a one-page `load_plan_note.pdf`.

* `bulk_load_plan.xlsx` — loads and savings by depot under each construction, the price-path sheet (ask A) and the idling sheet (ask B).
* `card_floor_check.png` — each account's cards as a strip of monthly volumes before and after the plan, the 400-gallon floor as a line,
  the West and East van cards highlighted, the loads per depot as bars, and the rebate kept or lost labelled per account.
* `load_plan_note.pdf` — the committed loads, the saving, and the budget basis finance will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each region, the eight weekly card prices the asymmetric model expects and last drop's
  realised path. *Device:* the price history posts a station's correction to a misreported price as a new row with the original report's
  ID and a correction flag, and the survey replaces the original. Averaging both rows misstates three weeks of last drop's path.
* **Ask B (device-carried).** For each depot, last month's idling hours per vehicle and the fuel they burned. *Device:* the telematics
  feed splits an idling episode that crosses midnight into two rows sharing an episode ID, and the idling standard caps an episode at
  four hours. Capping each row separately overstates idling at four depots.
* **Ask C (validity).** The allocation and true saving under each of the four rung constructions, with each construction's fit to the 72
  account-months of earlier rebates.
* **Decoupling.** Replacing the every-card floor with account totals changes no figure in asks A or B.

## 11. Rubric arithmetic

3 regions × 8 weeks (ask A) + 6 depots × 2 (ask B) + 6 depots × 4 constructions (ask C) + the six committed loads and the saving + 5
named chart parts + 3 files ≈ 75 criteria.

## 12. World-building constraints

* Accounts and cards (gallons a month): West D1 40 trucks × 3,000, D2 30 vans × 450; Central D3 50 × 1,400, D4 45 × 1,300; East D5 70
  vans × 800 (35 diesel), D6 35 × 2,800. Rebate losses over the eight weeks: West $19,758, Central $19,018, East $22,792.
* Per-load savings (asymmetric): D1 $6,000, D2 $6,480, D3 $4,000, D4 $4,400, D5 $5,120, D6 $4,800; instant pass-through: $1,920–2,480.
  Caps: D2 3, D5 8 (6 diesel only), the rest 8.
* A load a depot's vehicles cannot use is turned back at the gate and not charged, so true savings count at most six loads at D5.
  Allocations and true savings by rung as in the ladder; partial cells $103k, $110k and $119k.
* In 2021 West and Central are identical on every statement column. 70 of 72 account-months fit the total law.
* Price corrections and split idling episodes never touch card volumes, the register or the statements.
