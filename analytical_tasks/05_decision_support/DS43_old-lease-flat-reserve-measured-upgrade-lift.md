# DS43 — The reserve a housing trust sets on its old-lease flats, when their block is upgraded halfway through the hold

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · housing asset management |
| Mirrors | Valuing the hold alternative for an ageing asset when a scheduled refurbishment changes what it will be worth (fleet disposal timing at airlines and car-rental firms, data-centre hardware resale against a planned refresh, store-lease exits ahead of a mall refurbishment) |
| Decision shape | One figure committed at a date: the reserve for Block 216's standard four-room flats at this year's sale, set by the board by 31 March |
| Committed call | The reserve per flat, in Singapore dollars to the nearest thousand |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · S4, the hold path is generated under a regime the comparables never show (the block's upgrading programme completes in year two), measured as #25 from the programme log, with the population a flag suggests (E33) at rung 1 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #25 assumes an effect the log could measure · #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another |
| Calibration form | Prior-period close-out: last year's disposal close-out, 14 flats in five other blocks, with each reserve, its hold valuation and the price realised |
| Driving force | The reserve is the value of renting for five years and then selling. Lease decay drags that value down, and every correction to the decay curve lowers it further. But Block 216's upgrading programme completes in year two, and the authority's programme log, read as eleven natural experiments against same-lease blocks without programmes, shows a stable 10.5% lift. The agent assumes 22%; the comparables assume nothing. |

## 1. Situation

A housing trust owns 64 four-room flats on leases with about 52 years left, lets them under the authority's interim rental scheme at
rents fixed to 2031, and sells a batch each year to fund new building. At this year's sale it offers twelve flats in Block 216. Its
disposal policy sells a flat only if the best bid meets the reserve, and sets the reserve at the present value of keeping the flat: five
more years of the scheme's rent, then a sale, at the trust's 4% discount rate and net of its costs. The board sets the reserve by 31 March. The trust's agent projects prices from the town's average growth since 2017.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the resale transactions, the published remaining-lease field, the scheme's rent schedule, the
  programme log and last year's close-out. No stakeholder read is overturned. The town's prices did grow, old leases do decay, and upgrading does lift
  prices. The difficulty is what the flat will be when the trust sells it in five years.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the agent's projection and every voice. A hedonic lease-decay model on the transactions still values the hold
  path without the upgrade.
* **Instrument repair.** Suspect file: the published remaining-lease field, computed at the extract date rather than the sale date. Repaired
  to lease at sale, rung 1 lands with rung 2 on S$428,000, and rung 0 stays at S$612,000. Block 216 has not been upgraded, so a perfect
  valuation of today carries none of the 2031 lift; the measured lift is still needed.
* **Lens swap.** The naive read and the answer differ in moment and population: today's block, valued like every comparable, against the
  block in 2031, upgraded, which today's comparables do not include.

## 3. The driving force

A strong solver distrusts the agent's flat growth rate, fits a hedonic model with month and town effects and a lease-decay spline,
corrects the remaining-lease field (which the dictionary computes at the extract date, not the sale date), and values the hold path: rents
to 2031, then a sale at 47 years of lease. Each correction lowers the reserve, because old leases decay faster than any average shows. Every
step is right. But Block 216 is in the authority's upgrading programme, due to complete in 2027. The programme log lists eleven past
programmes in the town, and aligning each block's resale prices before and after its programme with same-town blocks of the same lease
decade that had none gives a lift of 9.8% to 11.2%, 10.5% pooled. The agent's rule of thumb is 22%; a raw before-and-after reading,
which carries the market's growth, is 25%; the hedonic comparables carry nothing. The scheme's rents are fixed whatever the block's
condition, so the measured lift reaches the reserve through the 2031 sale alone, and it turns the reserve back up.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Today's value grown at the town's average rate since 2017, plus rents, discounted | S$612,000 (+29.9%) | The agent's projection, on the town's own record | The transactions: four-room prices fall steeply with remaining lease, which average growth hides because newer flats enter the sample |
| 1 | Hedonic model with month and town effects and a lease spline, on the published remaining-lease field; hold path to 2031 | S$538,000 (+14.2%) | A proper asset-specific decay curve on official data | The data dictionary: the remaining-lease field is computed at the extract date, so older sales carry up to seven years too little lease |
| 2 | Hygiene of the population: lease at sale rebuilt from commencement year and sale month; same model; hold path to 2031 | S$428,000 (−9.1%) | The curve now steep where it should be, and last year's close-out reproduced | The programme log: Block 216 completes its upgrading programme in 2027, and eleven past programmes show what completion does to resale prices |
| 3 | **Decisive:** the lift measured from the eleven programmes against same-lease blocks without one (10.5%), applied to the 2031 sale, four years after completion | **S$471,000** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the reserve down and the decisive move reverses them. Offsets: +29.9%, +14.2%, −9.1%.
* **Partial correction priced (L3).** Applying the agent's assumed 22% lifts the reserve to S$518,000 (+10.0%). Measuring the lift as
  each upgraded block's raw before-and-after change, which carries the market's growth, gives 25% and S$530,000 (+12.5%). Applying the
  measured lift on the published-lease curve gives S$585,000 (+24%). Every half-measured lift overshoots, and leaving it out is rung 2.
* **Grid.** Lease field (published, at sale) × upgrade (none, assumed 22%, raw before-and-after, measured) = 8 cells. Only lease at sale
  with the measured lift gives S$471,000; every other cell sits at least 9.1% away, the nearest being rung 2's S$428,000.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The programme log is a public schedule of blocks and dates. No document says what an upgrade does to prices, or
   that the trust's block is in the log.
2. **Corpus blind for a computable reason.** *No flat in last year's close-out sat in a block with an upgrading programme scheduled or
   completed within five years, so the close-out's hold valuations carry no lift and reproduce identically with or without one.* It
   certifies the decay curve, the rents and the discounting.
3. **No arithmetic symptom.** The hedonic model fits, the close-out reproduces, and the hold path is positive and plausible under every
   rung.
4. **Not a row predicate.** The lift is a difference in price changes between programme blocks and matched blocks without one, across
   eleven programmes, and it then enters a hold path at a future date.
5. **The enumeration is arithmetic.** No transaction carries an upgrade flag; the block's status comes from the log by block and date.
6. **No cutover date in the decision.** The past programmes are measurement instances spread over a decade; the trust's block has not been
   upgraded, and nothing in the series it is valued on steps.
7. **Survives deletion.** No wrong number exists to delete. Without the agent, the comparables still say nothing about upgrading.

## 6. The calibration corpus

* **Form.** Last year's disposal close-out: 14 flats in five blocks, each with its reserve, the hold valuation behind it, the rents and
  costs used, and the price realised at the sale.
* **What it certifies.** The hold valuation method at rung 2: lease at sale, the hedonic curve, the rent schedule and the 4% discount rate
  reproduce all 14 hold valuations within S$1,000. The published-lease curve misses 11 of 14, every miss high.
* **What it is blind to.** Upgrading (above).
* **Twin pair.** Blocks 105 and 131 are identical on every column the transactions and the block register show: same town, lease commenced
  in 1977, the same flat-type mix and storey profile, and the same median price in 2016. Over the next three years their four-room prices
  rose 14% and 7% (2.0×). Block 105's programme completed in 2017; only the programme log separates them.
* **Resemblance points at the decoy.** By lease, size and storey, Block 216 most resembles the two close-out blocks whose realised prices
  matched their hold valuations to within 1%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The disposal policy: a flat sells only if the bid meets the reserve; the reserve is the present value of five more
  years' rent and a sale at the end, at 4%, net of the trust's costs. The interim rental scheme: rents fixed by flat type to 2031. The
  authority's programme log. The data dictionary.
* **Empirical pins.** The lease-decay curve, from the transactions; the upgrade lift, from the eleven programmes.
* **Voices.** The agent: "Prices here have grown four per cent a year since 2017, and your flats will too." The finance director: "Old
  leases only go one way; sell while you can." The estate manager: "Upgrading is paint and lifts; buyers pay for the lease."
* **Licensed wrong basis.** The policy records that the trust's auditors check each reserve against the agent's market report.

## 8. Determinism by construction

* **Hedonic.** The specification is filed: month and town effects, storey band, floor area and a lease spline with knots at 50, 60, 70, 80
  and 90 years, on four-room flats.
* **Lift.** Each programme's lift compares price changes from two years before announcement to two years after completion; windows one
  year shorter or longer move the pooled figure by at most 0.3 points.
* **Hold path.** The sale in 2031 is at 47 years of lease, four years after completion, so every programme's two-year post-completion
  window lies inside the hold; the scheme's rents do not move with condition.
* **Rounding.** The reserve is S$471,400 before rounding, inside its thousand.

## 9. Prompt sketch and deliverables

> The board sets the reserve for Block 216's four-room flats by 31 March, and below it we keep renting them for another five years. Our
> agent expects the town's price growth to carry on. Give me the reserve per flat, in dollars to the nearest thousand, as the line for the
> board paper. Send `reserve_build.xlsx`, a chart `hold_path_value.png`, and a one-page `board_reserve_note.pdf`.

* `reserve_build.xlsx` — the reserve under each rung construction, the eleven programmes' lifts (ask C), the rent sheet (ask A) and the
  tenancy sheet (ask B).
* `hold_path_value.png` — the flat's projected value from today to 2031 under the agent's growth, the decay curve and the decay curve with
  the measured lift, as three lines, with the 2027 completion marked and the reserve labelled.
* `board_reserve_note.pdf` — the committed reserve and why the comparables understate the hold.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 26 towns, last year's median monthly rent for a four-room flat. *Device:* the
  rental approvals register records a renewal as a new approval with a renewal flag, as its guide documents. Counting renewals as new
  lettings weights long-standing tenancies twice and pulls the median toward older rents in towns with stable tenants.
* **Ask B (device-carried).** For each of the twelve flats in Block 216, the tenancy end date and arrears at 31 December. *Device:* the
  tenancy register keeps superseded tenancies when a lease is extended, and the ledger allocates part-payments to the oldest charge first.
  Taking the first tenancy row and the latest charge misstates five flats.
* **Ask C (validity).** The reserve under each of the four rung constructions, and the measured lift for each of the eleven programmes.
* **Decoupling.** Clearing the upgrade lift changes no figure in asks A or B. Rental approvals, tenancies and arrears touch no transaction,
  lease or programme record.

## 11. Rubric arithmetic

26 towns (ask A) + 12 flats × 2 (ask B) + 4 reserves + 11 programme lifts (ask C) + the committed reserve, the 2031 sale value, the lift
used and the completion year + 5 named chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* Reserves S$612,000 / 538,000 / 428,000 / 471,000; partial cells S$518,000, 530,000 and 585,000. Of rung 2's S$428,000, the 2031 sale
  carries S$409,500 in present value and the fixed rents the rest.
* Eleven programmes, lifts 9.8–11.2%, pooled 10.5%; raw before-and-after 25%; the agent's rule 22%. Blocks 105 and 131 match on every
  transaction and register column.
* The close-out's 14 flats sit in blocks with no programme within five years; the published-lease curve misses 11 of 14 high.
* Rental approvals, tenancies and arrears are independent of every main-call record.
