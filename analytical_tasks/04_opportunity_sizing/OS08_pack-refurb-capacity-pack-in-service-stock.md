# OS08 — How to split 3,000 refurbishment slots across five EV platforms, when the cars that have already had a new pack are still counted as carrying an old one

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · EV battery remanufacturing |
| Mirrors | Sizing replacement and refurbishment demand from an installed base whose units have already been partly replaced (device battery service at Apple, drive and power-supply swaps in hyperscale fleets at Google and Meta, spare-parts pools for Amazon's delivery fleet), where the unit at risk is the part in service, not the asset it sits in |
| Decision shape | An allocation under a cap: next year's 3,000 refurbishment slots tooled across five platforms |
| Committed call | The slots tooled for each platform, and next year's out-of-warranty pack replacements across the five platforms |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern B with a reproduction clause (the pack in service is the unit at risk, built from the settled ledger), with an implicit import-certificate join (#18) below it |
| Gate G mechanism | method_or_model_selection, with forecasting |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #18 joins only on the visible key |
| Calibration form | Settled-transaction ledger: the national parts distributor's ledger of every replacement pack settled 2016–2025, whose published annual counts by platform are the control set |
| Driving force | The unit that fails is the pack in service, not the car. Every settled replacement in the distributor's ledger takes an original pack out of the at-risk stock and puts in a refurbished pack with its own two-year warranty and its own life curve. Built from the ledger through each vehicle's VIN, that pack stock is the only construction that reproduces all 20 published counts. Ageing cars instead reproduces 13, because the most-replaced platforms keep counting packs they no longer carry. |

## 1. Situation

A battery-refurbishment company will tool its plant for 3,000 out-of-warranty pack replacements next year across five platforms: the
Volta hatch, Kestrel SUV, Arden saloon, Mira city car and Tern van. Tooling is committed per platform in lots of 50, in proportion to
each platform's forecast, before the year starts. Its investors' term sheet admits a demand model only if it reproduces the parts
distributor's published out-of-warranty replacement count for every platform in every year from 2021 to 2024. The vehicle register
gives each car's platform and Dutch registration date. A separate import register holds the first-use abroad of imported used cars. The
OEM publishes its pack-life curve, and the company's own refurbished packs carry a two-year warranty and a filed life curve.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the register, the import certificates, the ledger, the published counts and both life curves.
  No stakeholder read is overturned. The difficulty is which population is at risk of failing next year, and it is a stock of packs
  that no file stores.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the investors' fleet-over-life model and every voice. A hazard model on correctly aged cars still reproduces
  13 of 20 counts, and the clause still sends the solver hunting.
* **Instrument repair.** Make the register and ledger perfect; they already are. The pack stock still has to be built, and a car
  registered in 2014 can carry a pack installed in 2023.
* **Lens swap.** The naive read is cars by age. The answer is packs in service by their own install dates, a different population.

## 3. The driving force

A strong solver drops the fleet-over-life shortcut and applies the OEM life curve to each platform's cars by age. Its back-test against
the published counts fails on the Mira, which it traces to imports: the register's date is when a used import reached the Netherlands,
and the import certificate, linked through the register's certificate number, puts first use 3.5 years earlier. Aged correctly, cars
reproduce 13 of 20 counts, and the misses all run high in the later years. That looks like noise near a solution. It is depletion: every
settled replacement removes an original pack and installs a refurbished one with its own clock. Arden and Mira have lost 2,900 and 3,400
original packs to replacement since 2019. Rebuilt as a stock of packs in service, Arden's forecast falls from 1,300 to 760, Mira's from
1,600 to 1,040, and Volta, with few packs replaced so far, leads.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Registered fleet ÷ a twelve-year life, by platform | Kestrel leads (1,200 slots); 6,300 replacements (+67.6%) | The investors' own model | The published counts: it reproduces none of the 20 |
| 1 | OEM life curve on cars aged from the register's Dutch date, out of warranty after 8 years | Arden leads (1,150); 3,250 (−13.6%) | A proper hazard on the installed base; reproduces 8 of 20 | The import register: 55% of Mira cars were first used abroad 3.5 years before their Dutch date |
| 2 | The same with imported cars aged from first use, through the certificate chain | Mira leads (1,000, 1.23× over Arden); 4,810 (+27.9%) | Reproduces 13 of 20, every miss in the later years | The ledger: 2,900 Arden and 3,400 Mira originals were replaced in 2019–2025 and are no longer at risk |
| 3 | **Decisive:** a stock of packs in service from the ledger (originals aged from first use, refurbished packs aged from install on their own curve and warranty) | **Volta 1,050 · Kestrel 150 · Arden 600 · Mira 800 · Tern 400; 3,760 replacements** | — | — |

* **Shape.** The graded objects are the slot vector and the demand figure. The leading platform changes at every rung (Kestrel, Arden,
  Mira, Volta, each at least 1.23× clear), and the answer is bracketed: −13.6% at rung 1 and +27.9% at rung 2.
* **Partial correction priced (L3).** A solver who removes replaced packs from the risk set but gives the refurbished packs no clock of
  their own reproduces 15 of 20, every miss low, and lands at 2,560 (−31.9%), further from the answer than rung 2, with 360 slots
  misplaced.
* **Grid.** Dates (Dutch, first use) × at-risk unit (car, pack stock) × refurbished clock (none, own curve) gives the cells: 3,250,
  4,810, the Dutch-date pack stock at 2,770 (−26.3%), the partial at 2,560, and the answer. The nearest wrong figure is rung 1 at −13.6%,
  and it costs two refuted readings at once.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The term sheet makes reproduction the gate. The OEM curve and the refurbished-pack standard describe packs. No
   document says the risk set is the pack in service or that the ledger defines it.
2. **Reproduction, not a menu.** The pack stock reproduces 20 of 20 published counts to the unit. The best rival, cars aged from first
   use, reproduces 13, and all seven misses run high, so it fails the 2021–2024 total by 11% too. The reproducing rule is a construction:
   each vehicle's current pack and its install date come from chaining that VIN's settled replacements in date order, and the refurbished
   packs need their own curve and warranty. No parameter sweep over a car-age model reaches it.
3. **No arithmetic symptom.** The register reconciles to platform fleet counts, every ledger line matches a registered VIN, and the
   published counts tie to the ledger's own annual totals.
4. **Not a row predicate.** The stock needs a group per VIN, an order of its replacements, and a different clock for each pack it has
   carried.
5. **The enumeration is arithmetic.** No column says which pack a car carries now; 9,100 cars carry refurbished packs.
6. **No cutover date.** Replacements accumulate year by year with no step in any series.
7. **Survives deletion.** Removing the investors' model and every voice leaves the clause and a 13-of-20 rival.

## 6. The calibration corpus

* **Form.** The distributor's settled ledger (every replacement pack 2016–2025: VIN, pack type installed, settlement date) and its
  published out-of-warranty counts by platform for 2021–2024 (20 controls).
* **What it pins.** The pack-in-service construction, 20 of 20; cars on Dutch dates 8; cars on first-use dates 13; packs without a
  refurbished clock 15 (all misses low).
* **Twin pair.** The Arden 2024 and Mira 2021 control cells are identical on cars at risk (8,000), ages (9–11 years from first use) and
  import share (22%). Their published counts are 410 and 830, 2.0× apart: by 2024 Arden had already replaced 2,900 originals, most now
  refurbished packs inside their warranty. Only the pack stock separates them.
* **Resemblance points at the decoy.** Next year's Arden and Mira fleets resemble Mira 2021, the highest count on file.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The term sheet: a demand model may be used to tool the plant only if it reproduces the distributor's published
  out-of-warranty count for every platform in every year 2021–2024. The OEM warranty runs 8 years from first use, and its pack-life curve
  is Weibull, shape 3.5, scale 14 years. The refurbished-pack standard: a two-year warranty and a Weibull life curve, shape 2.8, scale 7
  years from install. The tooling rule: 3,000 slots in lots of 50, in proportion to each platform's forecast, by largest remainder.
* **Empirical pins.** First-use dates, through the import certificates. The pack stock, from the ledger.
* **Voices.** The lead investor: "The biggest fleet is the biggest market." The operations lead: "Old platforms fail most; tool for the
  oldest."
* **Licensed wrong basis.** The term sheet records that the lead investor sizes demand as each platform's registered fleet over a
  twelve-year life and will present that model to the board.

## 8. Determinism by construction

* **Maturity.** The distributor settles every replacement within seven days, and the extract runs to 14 January, so every 2025
  replacement is in the ledger and the stock on 1 January is complete.
* **Exact controls.** The world is built so each published count equals the construction's expected count to the unit, and every rival
  misses at least one control by 8% or more.
* **Scrappage.** Scrapped and exported cars carry an end date in the register and leave both the car and pack stocks on that date.
* **Imports.** Every imported car has a certificate with a first-use date, so no age needs imputing.
* **Rounding.** No platform's quota lands within 0.05 lots of a remainder tie at any rung.

## 9. Prompt sketch and deliverables

> We have to commit next year's 3,000 refurbishment slots across the five platforms before tooling starts, and our lead investor's view is
> that the biggest fleet is the biggest market. Tell me the slots for each platform and how many out-of-warranty replacements the five
> platforms will need next year, as the figures I put to the board. Send `tooling_plan.xlsx`, a chart `pack_stock_by_age.png`, and a
> one-page `board_note.pdf`.

* `tooling_plan.xlsx` — the five platforms on four constructions with their back-tests against the 20 published counts, the core-return
  sheet (ask A) and the yield sheet (ask B).
* `pack_stock_by_age.png` — a script-rendered stacked histogram per platform: packs in service by age, original and refurbished stacked,
  the 8-year and 2-year warranty lines drawn, and each platform's forecast labelled above its panel.
* `board_note.pdf` — the committed slot vector, the demand figure, and the back-test that admits the model.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each platform, the share of replaced packs returned to the distributor as cores within 30
  days in 2025 and the median days to return. *Device:* cores sent in consolidated shipments carry the shipment number, not the claim,
  and the returns guide links them through the shipment manifest. Matching on claim number finds only direct returns and halves the
  share for three platforms.
* **Ask B (device-carried).** For each platform, the share of incoming cores passing cell grading in each quarter of 2025. *Device:* a core
  re-tested after balancing gets a second record under the same core number, and the grading procedure says the final test decides.
  Counting first tests understates yield on the Arden and Mira.
* **Ask C (validity).** Controls reproduced (of 20) and next year's demand under each of the four constructions and the partial reading.
* **Decoupling.** Rebuilding the risk set on cars instead of packs changes no figure in asks A or B. Core returns and grading records
  touch neither the register nor the forecast.

## 11. Rubric arithmetic

5 platforms × 2 (ask A) + 5 × 4 quarters (ask B) + 5 constructions × 2 (ask C) + the slot vector (5) and the demand figure + 5 named
chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Forecasts by platform (Volta, Kestrel, Arden, Mira, Tern): rung 0 1,500 / 2,500 / 1,000 / 800 / 500; rung 1 1,000 / 150 / 1,250 / 600
  / 250; rung 2 1,300 / 160 / 1,300 / 1,600 / 450; answer 1,300 / 180 / 760 / 1,040 / 480; partial 1,180 / 160 / 420 / 560 / 240.
* Refurbished-pack failures out of warranty next year: 1,200 of the 3,760.
* 55% of Mira cars are imports first used 3.5 years before their Dutch date; other platforms 4–22%.
* Reproduction: 0, 8, 13, 15 and 20 of 20 for rung 0, rung 1, rung 2, the partial and the answer.
* Arden 2024 and Mira 2021 match on every control-visible column.
* Core returns and grading records never touch the register, the import certificates or the ledger's replacement lines.
