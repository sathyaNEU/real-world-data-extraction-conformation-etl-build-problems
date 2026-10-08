# RC28 — Which cause of lost visitor spending gets the recovery tranche, when the closed cruise line's customers never left

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · tourism and destination marketing |
| Mirrors | Revenue triage after a product sunset on consumer platforms (a streaming plan tier retired, an Amazon or Etsy listing replaced by a successor listing, an app feature folded into a new one), where the sunset is blamed and the successor's flat line hides a real decline among customers who were never part of it |
| Decision shape | Which of N root causes gets the fix: one recovery tranche, five candidate causes of this year's lost visitor spending |
| Committed call | The one cause the authority's $9M recovery tranche addresses, named in a sentence, with each candidate's lost spending |
| Gap · Pattern | Gap 2 (population) · S7 (every screen is right and the answer is what nothing flags): the cruise market's loss is a continuation, and the successor's line masks the quiet decline |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #23 reads a closure notice as a market exit · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Settled-transaction ledger: Seaward Lines' settled bookings with customer IDs, filed under its co-op agreement, for four closed years and this year |
| Driving force | Seaward Lines ended its inter-island cruise in March, and the cruise market's spending vanished from the authority's tables. Its customers did not leave. From April, 8,900 of them bought Seaward's new island-hop air package, and the authority counts them as US West air visitors. Their $63M fills the US West air line, which reads −$6M while US West residents' own spending fell $69M. Only a customer-level link through the operator's settled ledger separates the two. |

## 1. Situation

The islands' visitor authority has a $9M recovery tranche for one cause of this year's lost visitor spending, and its fund rules size each
candidate on the spending its fix would restore. Five causes are on the table. The cruise line Seaward ended its inter-island sailings in
March. The 1,240-unit Halekai resort was under renovation from March to October. The weak yen cut Japanese visitors' spending per day. US East
visitors' stays shortened. US West visitors' spending softened. The authority's market tables, its lodging register and Seaward's settled
ledger are all in the pack, and the board chair is sure the cruise exit hurt most.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the market tables, the lodging register, the renovation permit, the exchange-rate series and
  the operator's ledger. The cruise market really did lose its spending, and the US West air line really is nearly flat. No reading of anyone's
  own figures is overturned. The question is who those figures describe.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's view and every voice. The market table still shows the cruise line −$75M and US West air −$6M, and
  every natural attribution still books the cruise loss to the cruise exit.
* **Instrument repair.** No file is suspect. The market tables classify every visitor correctly by origin and mode, the lodging register,
  unit inventory and permit are complete, and the ledger carries every customer ID. Repair the visitor tables anyway, down to a perfect
  survey of every visitor. Rung 0 still names the Halekai (110), rung 1 the yen (90) and rung 2 the cruise exit (75), because a perfect
  count still puts the continuers in US West air. Continuity is a customer's history across one operator's products, which no row claims to
  record, so the link is still needed.
* **Lens swap.** The naive reading sizes a product category, the cruise market. The answer sizes customers who left the destination, with
  the continuers moved to the market they now sit in. These are different populations.

## 3. The driving force

A strong solver sizes each candidate the way the fund rules require. It splits the Halekai into the units that actually closed and splits
Japan's decline by factor so that only the daily-spend part is the yen's. It is left with the cruise exit as the clear leader, because
the cruise market's $75M is gone and the closure notice is dated. But Seaward's settled ledger carries a customer ID on every booking. From
April a new product line appears in it, the island-hop air-and-hotel package. Joined on customer ID, 8,900 of its 9,400 buyers had sailed
with Seaward in the previous 15 months. They flew in, so the authority counts them as US West air visitors. That masks the real loss: US West
residents who were never Seaward customers spent $69M less. The successor line makes the decline invisible in every market table.

## 4. The ladder

| Rung | Construction | Names (lost spending, $M) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each market's whole change booked to its named cause, Halekai valued at the whole property | Halekai renovation (110; yen 90, cruise 75, US East 35, US West 6) | The authority's own reading of its tables | The renovation permit covers the hotel tower only, and the unit inventory shows 720 vacation-ownership units in the Ewa tower stayed open |
| 1 | Halekai split to the 520 tower units that closed (the mixed segment split through the unit inventory) | Weak yen (90 against cruise 75) | Every lodging figure now matches the units that shut | The fund rules size the yen fix on the spending it restores, and LMDI puts only 38 of Japan's 90 in the daily-spend factor |
| 2 | LMDI by factor within each market, each fix sized on its own factor | Cruise exit (75 against Halekai 46) | An exact, order-free bridge with every fix sized as the rules say, and the dated closure is a satisfying cause | Seaward's ledger: 8,900 of the island-hop package's 9,400 buyers are Seaward cruise customers, counted this year as US West air visitors |
| 3 | **Decisive:** continuers linked by customer ID and moved from the cruise loss to the US West line they now sit in | **Softening US West demand (69 against Halekai 46)**, 5th on rung 0 | — | — |

* **Position table.** US West ranks 5th on rungs 0, 1 and 2, and leads only rung 3. Rung margins are 1.22, 1.20, 1.63 and 1.50.
* **Discriminator dominance.** The cruise exit carries a $69M lead over US West into rung 3 ($75M against $6M). Continuity moves $63M from
  one column to the other, a $126M swing, which is 1.83× the carried lead and above the 1.2× floor.
* **Partial correction priced (L3).** One solver nets Seaward's two product lines at operator level, so the cruise loss falls to $9M, but
  leaves the continuers in US West air. It names the Halekai at $46M, 1.21× the yen. Another links continuity only through this year's
  January–March sailors. That catches 2,700 continuers ($19M) and names the cruise exit again at $56M, 1.22× the Halekai. Neither half
  lands on US West.
* **Grid.** Halekai (whole or split) × Japan (market or factor) × cruise continuity (none, operator-netted, Q1-linked, customer-linked) = 16
  cells. Only the fully corrected cell names US West. Every other cell names the Halekai, the yen or the cruise exit.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The closure notice announces the end of sailings. Seaward's package launch is a line in its co-op filing, and no
   document says the package's buyers are the cruise's customers or how the authority counts them.
2. **Corpus blind for a computable reason.** *In every closed year every Seaward customer booked the cruise, because the island-hop package
   did not exist before April, so the ledger's product lines and the authority's markets map one to one.* The ledger reconciles to the cruise
   market's spending in all four closed years and in this year's first quarter.
3. **No arithmetic symptom.** The cruise market ties to the cruise product line. US West air's −$6M is ordinary year-to-year movement, and
   island totals, lodging and tax receipts reconcile under every reading.
4. **Not a row predicate.** Continuity is a customer-level join across product lines and years, an ordering of each customer's bookings, then
   a move of their spending between market columns.
5. **The enumeration is arithmetic.** Nothing flags a continuer. The 8,900 come out of a join and a lookback.
6. **No cutover date.** The closure is dated, and it is the decoy. The US West softening is gradual across the year.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Seaward's settled-booking ledger: every booking with customer ID, product, travel dates and settled amount, for four closed years
  and this year.
* **What it certifies.** The cruise market's estimate: settled cruise bookings plus the survey's onshore spend reproduce the authority's cruise
  spending within 0.3% in each closed year and in this year's first quarter, under the market reading of rungs 0 to 2.
* **What it is blind to.** Continuity across a product change (property 2).
* **Twin pair.** Two closed-year withdrawals in the authority's market register, the Bluewater inter-island ferry and the Kailani evening
  cruise programme, are identical on passengers, market mix, season and closure month. Their markets lost $14M and $29M (2.07×). Bluewater's
  operator moved its customers onto an air shuttle and Kailani's did not. Only a customer-level continuity rule reproduces both.
* **Resemblance points at the decoy.** Seaward's sailing most resembles Kailani's: an evening product sold to US West couples, whose closure
  cost its full programme.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rules: "Each candidate is sized on the visitor spending its fix would restore, in current dollars." The lodging
  register is the authority's record of units, and the renovation permit is the county's record of scope.
* **Empirical pins.** Continuers come from the ledger's customer IDs. The Halekai split comes from the unit inventory. Factor shares come from
  the market tables.
* **Voices.** Board chair: "Losing Seaward's ship hurt us more than anything else this year." Lodging association president: "When the
  Halekai went dark, the whole coast went quiet." Japan desk manager: "The yen is the story in our market; nothing else moved."
* **Licensed wrong basis.** The fund rules record that the legislature's tourism committee reads each market's change as its cause's cost,
  as the authority's annual report does, and will see the tranche request on that basis.

## 8. Determinism by construction

* **Lookback.** Every continuer last sailed within the 15 months before the closure, and no package buyer's last sailing falls 15 to 60 months
  back, so any lookback from 15 to 60 months links the same 8,900.
* **Customer IDs.** The ledger documents that IDs persist across products. No ID maps to two people, and no customer holds two IDs.
* **Factor method.** LMDI-I and a Shapley split put Japan's daily-spend factor at $38.0M and $38.4M, so the method cannot change a name.
* **Halekai.** Last year's occupancy is in the lodging register by tower, so the closed tower's lost visitor-days need no assumption.
* **Currency and prices.** The fund rules price in current dollars. The yen factor is measured in dollars and needs no deflator.

## 9. Prompt sketch and deliverables

> The $9M recovery tranche goes to one cause of this year's lost visitor spending, and the board votes on it next week. The chair is sure
> Seaward's exit hurt us most. Tell me which of the five causes the tranche should go to, in a sentence I can put to the vote, with what each
> cause cost us in millions of dollars to one decimal. Send `recovery_case.xlsx`, a chart `cause_sizes.png`, and a one-page
> `tranche_memo.pdf`.

* `recovery_case.xlsx` — each candidate's sizing, the lodging sheet (ask A), the tax sheet (ask B) and the ledger reconciliation (ask C).
* `cause_sizes.png` — a dumbbell per candidate from the market-table reading to the final sizing. The funded cause is marked, the $63M
  cruise-to-US West move is drawn as a labelled arrow, and the title names the funded cause.
* `tranche_memo.pdf` — the named cause and why the other four fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each island, this year's occupied unit-nights and average daily rate for hotels, vacation
  ownership and vacation rentals. *Device:* a vacation-rental listing can rent several units, and the listing register carries each
  listing's unit count, as its dictionary documents. Counting listings as units understates occupied units by about 12% on two islands. No
  vacation-rental row enters the main call.
* **Ask B (device-carried).** Transient accommodations tax collected by island and quarter. *Device:* amended returns post as new rows
  carrying the original filing period, as the tax ledger's notes state. Assigning by posting date misplaces about 9% of collections across
  quarters.
* **Ask C (validity).** For each of the four closed years and this year's first quarter, the authority's cruise-market spending beside
  settled cruise bookings plus survey onshore spend.
* **Decoupling.** Clearing the customer link changes no figure in asks A or B. Ask C uses only cruise-product rows from periods before the
  package existed.

## 11. Rubric arithmetic

4 islands × 3 lodging types × 2 measures (ask A) + 4 islands × 4 quarters (ask B) + 5 periods × 2 (ask C) + the named cause, the five
sizings and the winning margin + 5 named chart parts + 3 files ≈ 65 criteria.

## 12. World-building constraints

* Lost spending by rung ($M) is Halekai 110 / 46 / 46 / 46, yen 90 / 90 / 38 / 38, cruise 75 / 75 / 75 / 12, US East 35 throughout, and
  US West 6 / 6 / 6 / 69.
* Seaward's package has 9,400 buyers, 8,900 of them prior cruise customers, all of whom last sailed within 15 months. Continuers spent $63M
  in US West air.
* The Halekai has 520 hotel-tower units, closed March to October, and 720 vacation-ownership units in the Ewa tower, open throughout.
* Bluewater and Kailani are identical on every register column, with losses of $14M and $29M.
* The cruise market reconciles to the ledger within 0.3% in every closed year and in this year's Q1.
* Multi-unit listings and amended tax returns never touch market spending, the Halekai units or the ledger.
