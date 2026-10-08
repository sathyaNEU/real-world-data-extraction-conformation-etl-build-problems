# DS21 — How many bags of the new hybrid the cooperative commits for next season, when most of its biggest members' acres are already promised to a rival

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · agricultural input distribution |
| Mirrors | Committing launch inventory when part of the addressable base is locked into a rival's volume contract (Apple and Amazon device launches into carrier-contract bases, cloud migrations against committed-spend agreements, enterprise seats under a rival's multi-year licence) |
| Decision shape | One figure at a date: the firm launch order the seed company needs by 1 December |
| Committed call | Bags of the new hybrid to commit for next season, to the nearest hundred |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · Pattern C (serviceable share behind a join: only the acres a member has not committed under a rival's volume rebate can take the launch), under a reproduction clause, with an implicit join through family entities (#18) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #18 joins only on the visible key · #7 uses the ready-made measure · #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match |
| Calibration form | Published control set with a reproduction clause: the seed company's sell-through statements for the cooperative's last six hybrid launches, and the purchasing policy's rule that a volume model must reproduce each to within 1% |
| Driving force | The cooperative sells several brands, and members who sign a rival brand's volume rebate commit bags for next season across every acre they farm, including acres farmed through family entities. A launch can only reach the acres left open: each member's planned corn acres, with its entities' acres attached through the beneficial-owner table, less its committed bags converted to acres, floored at zero. Only that construction reproduces the six past launches. The biggest members, who plant most of the footprint, have committed 91% of their acres, and members rotating out of corn are committed beyond their acres, so neither an acreage figure nor an aggregate netting gets the order right. |

## 1. Situation

A farm supply cooperative must place a firm order by 1 December for a new corn hybrid, with returns capped at 10%. It sells several seed
brands to its 1,250 members. It holds the field registry, the membership rules with the beneficial-owner table for members who farm
through family entities, the crop plans members filed for next season, the agreement register of volume-rebate commitments, the hybrid's
agronomy sheet (34,000 seeds an acre, 80,000-seed bags), and the seed company's launch model, which puts year-one uptake at 12% of a
grower's corn acres. The purchasing policy requires any volume model to reproduce the last six launches' first-season sales, published in
the seed company's sell-through statements. The agronomy manager wants the order sized to the members' corn footprint.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the registry's acres, the crop plans,
  the commitments, the launch model's 12% (true of open acres) and every sell-through statement. The difficulty is that the launch reaches
  a population no file lists: acres not already promised.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the agronomy manager's view. The launch model times members' corn acres still gives a confident order, and
  every acre ties to the registry or the crop plans.
* **Instrument repair.** The suspect field is the registry's operator key, which carries entity-farmed fields under the entity, not the
  member. Linked to members directly, rung 0 lands on rung 1's 35,900, and rungs 1 and 2 stay at 35,900 and 37,600. The crop plans and the
  agreement register are complete, and no file records open acres, so the netting is still needed for 16,800.
* **Lens swap.** The naive read orders for the corn footprint. The answer orders for the open acres, a different population that differs
  member by member.

## 3. The driving force

A strong solver joins the field registry to the member list, multiplies corn acres by the launch model's 12% and by 0.425 bags an acre,
and orders 30,700 bags. It then finds, from the membership rules, that many members farm through family entities whose fields carry the
entity's identifier, not the member's, and it attaches those fields through the beneficial-owner table. It switches from last season's
acres to next season's crop plans, and the order rises to 37,600. Each step is competent. But the purchasing policy's reproduction test
fails at every rung: the acreage model over-predicts all six past launches, by 1.6× to 4.8×. A member who signs a rival brand's volume
rebate commits bags for every acre it farms, entities included, and only acres left over can take a new hybrid. Open acres are each
member's planned corn acres less its committed bags at 0.425 an acre, floored at zero, because a member rotating out of corn cannot lend
its excess commitment to anyone else. The 60 largest members plant 201,000 acres and have 17,500 open. That construction reproduces all
six launches and puts next season's order at 16,800 bags.

## 4. The ladder

| Rung | Construction | Figure (bags) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Registry corn acres joined to members on the operator key, last season, × 12% × 0.425 | 30,700 | The cooperative's own acres and the seed company's own model | The membership rules: members farm through family entities, linked by the beneficial-owner table, and 102,000 acres sit under entity identifiers |
| 1 | Entity fields attached through the beneficial-owner table (#18) | 35,900 | Every member acre now counted | The crop plans: members filed next season's corn acres by 15 November, and rotation moves 34,500 acres |
| 2 | Next season's planned corn acres, members and entities | 37,600 | The forward acreage, filed by the members themselves | The reproduction clause: the acreage model over-predicts every one of the six past launches |
| 3 | **Decisive:** open acres per member (planned acres with entities attached, less committed bags ÷ 0.425, floored at zero) × 12% × 0.425 | **16,800** | — | — |

* **Walk and reversal.** The corrections walk the order up, 30,700 → 35,900 → 37,600 (offsets +5,200 and +1,700), as the population
  widens to the true footprint. The decisive rung reverses them by −20,800, below every rung.
* **Partial correction priced (L3).** Open acres on the operator key alone, with entity acres missed, gives 14,300 (−15%). Treating entities
  as separate operators with no commitment gives 20,400 (+21%). Netting all commitments against all acres in aggregate gives 13,700
  (−18%), because the rotating members' excess commitments are subtracted from other members' acres. Rescaling the launch share to fit the
  past launches' total gives 27,100 (+61%) and reproduces 2 of 6. No half lands within 15% of the answer.
* **Grid.** Acres (last season, planned) × join (operator key, beneficial-owner chain) × commitments (ignored, aggregate, per member) gives
  12 cells, from 6,800 to 37,600 bags. Only planned acres, the chain and per-member netting give 16,800. The nearest wrong cell is per-member
  netting on the operator key (14,300, −15%), and it costs one omission: the beneficial-owner table.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The launch model speaks of "a grower's corn acres", the rebate agreements of bags, and no document converts a
   commitment into acres closed to a launch.
2. **The reproducing rule is a construction, not a menu.** Open acres reproduce all six launches to within 1%. The best rival, the launch
   share refitted to the six launches' total, reproduces 2 of 6, missing high in the years the rival's rebate programme was large and low in
   the others. The winning rule has no parameter to scan: it needs each member's commitments, its entities' planned acres through a two-hop
   join, and a per-member floor, then a sum.
3. **No arithmetic symptom.** Acres tie to the registry and the crop plans, commitments to the agreement register, and the launch model's
   arithmetic is right at every rung.
4. **Not a row predicate.** No field is in or out. Each member's open acres are a floored difference between two quantities from two files,
   reached through the beneficial-owner chain.
5. **The enumeration is arithmetic.** No column holds open acres; the 330,100 fall out of the netting.
6. **No cutover date.** Rebate commitments are signed member by member through the autumn, and no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The seed company's sell-through statements for the cooperative's last six hybrid launches (first-season bags sold), with each
  launch year's crop plans and agreement register, and the purchasing policy's 1% reproduction clause.
* **What it pins.** Open acres × 12% × 0.425 reproduces every launch (15,900, 13,600, 17,200, 11,400, 6,800 and 14,700 bags). The acreage
  model reproduces none. The refitted share reproduces 2.
* **Twin pair.** Launches L2 and L5 are identical on every visible column: 640,000 planned member corn acres, the same seeding rate and the
  same list price. They sold 13,600 and 6,800 bags (2.0×). Only open acres separate them: L5's season fell under a rival's three-year
  rebate programme that committed most large members' acres.
* **Every rule exercised.** Two launch years held rotating members committed beyond their acres, which tests the per-member floor, and
  every year held entity-farmed acres covered by members' agreements, which tests the chain.
* **Resemblance points at the decoy.** Next season's planned footprint (737,500 acres) resembles L3's, the cooperative's best launch, which
  came in the year the rival's programme lapsed.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The purchasing policy: the launch order is the expected first-season sales, and any volume model must reproduce the last
  six launches within 1%. The agronomy sheet: 34,000 seeds an acre, 80,000-seed bags. The rebate agreements' scope clause: a commitment
  covers every acre the member farms directly or through entities it controls. One sentence each.
* **Empirical pins.** The open-acres construction, from the six launches.
* **Voices.** The agronomy manager: "Order for the footprint; members always want the new genetics." The seed company's representative:
  "Year-one uptake looks the same everywhere we launch." The board chair: "Running short at planting costs us more than carrying bags."
* **Licensed wrong basis.** The policy records that the board reviews launch orders as a share of members' corn acres and will see that
  basis.

## 8. Determinism by construction

* **Acres.** Every member filed a crop plan by 15 November, as the membership rules require, so planned acres have one value.
* **Commitments.** The agreement register lists bags by member for next season, and each agreement's scope covers controlled entities.
* **Conversion.** 34,000 seeds an acre over 80,000-seed bags is exactly 0.425 bags an acre.
* **Floor.** Each member's open acres are floored at zero, and the 50 rotating members are the only ones committed beyond their acres.
* **Rounding.** 330,147 open acres give 16,837 bags, filed to the nearest hundred (16,800), and no cell lies within 15%.

## 9. Prompt sketch and deliverables

> The seed company needs our firm order for the new hybrid by 1 December, and returns are capped at 10%. Our agronomy manager wants it sized
> to the members' corn footprint. Tell me how many bags we commit, to the nearest hundred, in a line for the purchasing committee. Send
> `launch_order.xlsx`, a chart `open_acres.png`, and a one-page `order_note.pdf`.

* `launch_order.xlsx` — the order under each rung, the member build, the delivery sheet (ask A), the fertiliser sheet (ask B) and the
  reproduction sheet (ask C).
* `open_acres.png` — for each member class (large, mid-size, small, rotating), planned corn acres split into committed and open as stacked
  bars, plus a panel of the six past launches' sales against each construction's prediction.
* `order_note.pdf` — the committed order and why it is less than half the footprint figure.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Median days from a member's seed order to delivery last spring. *Device:* a split delivery carries
  the original order number with a sequence suffix, as the delivery system documents. Treating each suffix as an order halves the median.
* **Ask B (device-carried).** Fertiliser tonnes delivered per quarter last year. *Device:* blended products are logged one row per
  component under a blend identifier. Summing component rows with the blend's total row double-counts every blend.
* **Ask C (validity).** Each construction's predictions for the six launches and its hits against the 1% clause, and the 12 grid cells.
* **Decoupling.** Clearing the netting and the chain changes no figure in asks A or B. Deliveries and fertiliser rows never enter an acre
  or a commitment.

## 11. Rubric arithmetic

4 rung figures + 12 grid cells + 6 launches × 4 constructions (ask C) + 4 member-class builds + the committed order and the open acres +
4 quarterly fertiliser figures (ask B) + the delivery median (ask A) + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Member classes (members; planned own + entity corn acres each; committed bags each): large 60, 1,900 + 1,450, 1,300; mid-size 400,
  640 + 80, 190; small 740, 275 + 0, 0; rotating 50, 900 + 0, 900. Last season: large 1,700 + 1,300, mid-size 560 + 60, small 250,
  rotating 1,800.
* Open acres 330,147 (large 291 each, mid-size 273, small 275, rotating 0). Order 16,837 bags. Rung figures 30,651, 35,853, 37,612.
* The six launches are reproduced within 1% by open acres only; L2 and L5 are identical on every visible column with sales 2.0× apart.
* Delivery suffixes and blend rows never touch acres, crop plans or commitments.
