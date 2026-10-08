# DA01 — The three top-tier floors a state revenue conference adopts, when its published tables count households and the return file counts returns

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · public finance and income-tax revenue forecasting |
| Mirrors | Customer-concentration tiers built on billing accounts when the decision is about the enterprise behind them (top-customer tiers at cloud platforms, advertiser tiers across ad accounts at Meta and Google, seller concentration across storefronts on marketplaces) |
| Decision shape | A structure the body adopts: the floors of the three top tiers (10%, 5% and 1% of household units) that the conference's income-tax forecast carries |
| Committed call | The TY2025 tier schedule: three AGI floors, each to the nearest $1,000, headed by the top-1% floor |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S1, the unit the decision funds is not the unit the pack records, gated by Pattern B (only the true unit reproduces the published tables), with E18 (the coarse all-filer table) below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #2 counts file rows instead of the real unit · #3 stops at a close but inexact match · #1 reports a failed back-test, ships anyway · #14 coarsens the segment it was asked about |
| Calibration form | Published control set with a reproduction clause: the conference's three prior Household Income Tables (69 published cells), which the methodology makes the condition of adopting any schedule |
| Driving force | The tables count household units, which no file stores. A household is a federal filing unit plus the own returns of the people its dependents schedule claims, and a dependent's return carries no field naming its claimant. 380,000 resident returns are such returns. Attached, they stop being units, which lifts every floor through the count, and their custodial and trust income lifts the claimants who hold the only cells the textbook tax unit misses. |

## 1. Situation

A state's Revenue Estimating Conference forecasts personal income tax with the top of the distribution split into three tiers, the top
10%, 5% and 1% of household units, because realised capital gains move each tier differently. Each autumn staff re-base the tiers on the
latest processed year and bring the schedule of floors to the conference, which adopts it for the forecast. On the shared drive are the
TY2025 processed-return file (3,412,000 rows), the dependents schedule, the Department of Revenue's Returns Processed by AGI Class table
and the conference's published Household Income Tables for TY2022 to TY2024. The state's rate schedule gives two-earner couples a lower
combined bill when they file separate state returns, so many of them do.

## 2. Gate G: why this is legal

* **Litmus.** Every number in the pack is correct: the return file, the dependents schedule, the Department's all-filer table and the
  published household tables. Nobody's reading of their own figures is overturned, and the Department's table is right about returns.
  The difficulty is building the unit the conference's tables count, which no file stores.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief economist's view and the fiscal office's licensed basis. The return file still ties to the
  Department's table to the row and the dollar, and percentiles off it still look like the textbook answer.
* **Instrument repair.** Perfect every field of the return file and it changes nothing, because every field is already right. Returns
  are what the tax system files; a household is formed by claiming relationships between returns, which no return observes, so no
  better return instrument carries it.
* **Lens swap.** The naive read and the answer are different populations: 2,876,000 resident returns against 2,328,000 household units,
  a fifth of which hold two to four returns.

## 3. The driving force

A strong solver filters to full-year residents, takes each return as a unit and checks itself against the Department's table, which it
reproduces exactly. Knowing the top-income literature, it then recombines separately filed state returns into federal filing units through
the federal primary TIN each one carries. That is the textbook tax unit, and it reproduces 58 of the 69 published cells. The 11 misses are
the $500,000 to $1M class's units and AGI in each year (each under 0.4%) and five small-county counts, all on the same side. The published tables count households, and a household
also holds the own returns of the people its dependents schedule claims: summer-job wages, custodial-account and trust income. Nothing on
a dependent's own return names the claimant. Only the claimant's schedule lists the dependent's TIN, so the link is a two-hop join no
column invites. Attached, those 380,000 returns stop being units. That lifts every floor through the count, and their income lifts the
households just under $500,000 that hold the missing cells.

## 4. The ladder

| Rung | Construction | Lands on (top-1% floor) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every row of the processed-return file is a unit; percentiles of AGI | $504,000 (−32.1%) | The file ties to the Department's all-filer table to the row and the dollar | The codebook's residency list: codes 2 and 3 are part-year and non-resident filers, outside the methodology's full-year residents |
| 1 | Full-year residents (code 1), each return one unit | $565,000 (−23.9%) | The methodology's population, filtered on the authoritative code list | The published tables: the return grain reproduces only the 3 total-AGI cells of 69 |
| 2 | Federal filing units: separate state returns recombined through the federal primary TIN | $667,000 (−10.1%) | The literature's tax unit, reproducing 58 of 69 cells; its six state-level misses are each under 0.4% | The dependents schedule: 380,000 resident returns are filed by people another return claims, and only attaching them reproduces the 11 missed cells |
| 3 | **Decisive:** household units, each federal filing unit plus the own returns of the dependents its schedule claims | **$742,000** | — | — |

* **Figure shape.** The answer is the maximum cell of the grid, so every partial application files floors too low and pushes top-tier
  liability into the middle tier. The full answer schedule is $214,000 / $318,000 / $742,000; rung 2 files $197,000 / $293,000 / $667,000.
* **Partial correction priced (L3).** A solver who finds the dependents' returns and attaches them, but keeps separately filed spouses as
  two units, lands at $628,000 (−15.4%), further out than rung 2. A solver who finds them and drops them, the literature's convention for
  dependent filers, lands at $718,000. The gate refuses that construction outright: it misses all three published total-AGI cells by
  −2.1%, totals that every complete partition ties.
* **Grid.** Residency (all filers or code 1) × filing unit (return or federal) × dependents (separate or attached) gives 8 cells. The
  nearest non-answer cells are rung 2 at −10.1% and households built on all filers at −10.6%. Reaching the answer takes the residency
  filter and both links.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The methodology says tiers are drawn on "full-year resident household units" and that a schedule needs a
   construction reproducing the published tables. It never says what a household holds. The schedule's codebook describes it as the list
   of dependents claimed for the exemption credit.
2. **Reproduction, and why it is a construction.** Households reproduce 69 of 69 published cells. Federal filing units reproduce 58 and
   the return grain 3. Every rival miss runs the same way (too few units in the $500,000 to $1M class), so no rival nets out on that class.
   The reproducing unit is a connected set of returns reached through two link types, one of them a two-hop join from schedule to own
   return. No column or parameter can be scanned to reach it.
3. **No arithmetic symptom.** Every construction is a complete partition of the same resident returns, so total AGI ties the Department's
   table and the published total cells under every rung. Row counts reconcile, and no TIN repeats.
4. **Not a row predicate.** Membership is a property of another return (the claimant's schedule), reached through a join and resolved into
   components. A dependent's own return carries no flag a filter could use.
5. **The enumeration is arithmetic.** No column says "household". The 380,000 memberships are computed, not flagged.
6. **No cutover date.** Separate filing and dependents' returns run unchanged through every year in the pack, and no series steps.
7. **Survives deletion.** No wrong number exists to delete; with every voice removed, the return file still invites the row as the unit.

## 6. The calibration corpus

* **Form.** The three published Household Income Tables. For the nine AGI classes from $100,000 up, each gives household units and AGI,
  plus total AGI: 19 cells a year, 57 in all. The TY2024 table adds a county appendix of household units above $500,000 for the 12
  largest counties. That makes 69 cells.
* **What it pins.** The household construction, uniquely, at 69 of 69 against 58 for the best rival.
* **What it cannot show.** The count of household units. No published cell covers units under $100,000, so the largest effect on the
  floors (380,000 fewer units) is visible only through the construction the cells pin.
* **Twin pair.** Kessler and Abington counties are identical on resident returns by class, separately filing couples, dependents' own
  returns (1,240 each, $17.6M of AGI each) and federal filing units above $500,000 (58 each). Their published household units above
  $500,000 are 117 against 58 (2.02×). Kessler's dependents with custodial income are claimed by households just under $500,000, and
  only attaching them through the schedule reproduces both counts.
* **Resemblance points at the decoy.** TY2025's resident profile most resembles TY2023's table, the year in which federal filing units come
  closest (38 units short in one class).

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The methodology: "Tiers are drawn on full-year resident household units at the 10, 5 and 1 per cent marks, and each
  floor is stated to the nearest $1,000." The methodology: "A tier schedule is adopted only on a construction that reproduces every
  published cell of the three most recent Household Income Tables." The return codebook lists residency codes 1 to 3. The Department's
  table is headed "Returns processed, all filers", a different question correctly answered.
* **Empirical pins.** What a household holds comes from reproducing the published tables. No sentence fixes it.
* **Voices.** The chief economist: "Every return is a taxpayer; build the tiers off this year's returns and you can't go far wrong." The
  Department's statistics chief: "Our table ties to the processed file to the dollar. That's the file I'd trust."
* **Licensed wrong basis.** The methodology records that the legislative fiscal office draws its tiers on federal filing units and will
  present its own schedule at the conference.

## 8. Determinism by construction

* **Residency of a household.** No federal filing unit mixes residency codes, and every dependent claimed on a code-1 return files with
  code 1, so a household's residency is never in question.
* **Claims.** Each dependent TIN appears on exactly one schedule (the Department rejects duplicate claims), and no TIN changes during the
  year.
* **Quantile convention.** Near each floor, adjacent units sit under $50 apart and no floor lies within $500 of a $1,000 boundary, so
  nearest-rank, interpolated and weighted-midpoint quantiles file the same rounded figures.
* **Zero and negative AGI.** These units count in the base under every construction and sit far below every floor.
* **No prior schedule ships.** The published tables carry class cells and totals only, so no earlier floor anchors a guess.

## 9. Prompt sketch and deliverables

> The conference sits on 14 November and I have to bring it the TY2025 tier schedule, the three floors our income-tax forecast uses for
> its top tiers. Our chief economist believes the schedule should come straight off this year's returns. Give me the three floors in
> dollars, each to the nearest thousand, in one sentence the conference can adopt, and send `tier_schedule.xlsx` with the build and the
> sheets below, plus `tier_floors.png`.

* `tier_schedule.xlsx` — the household build, the four constructions' schedules and hit counts (ask C), the withholding sheet (ask A) and
  the estimated-payment sheet (ask B).
* `tier_floors.png` — the cumulative count of units above each AGI from $150,000 up on a log axis under the four constructions, the three
  adopted floors as labelled vertical lines, the Kessler and Abington counts annotated, and each construction's published-cell hit count
  in the legend.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 24 months from October 2023 to September 2025, withholding receipts attributed to
  the month in which the wages were paid. *Device:* the deposit ledger dates every deposit on receipt. Monthly-schedule employers deposit a
  month's withholding by the 15th of the next month, and semi-weekly employers within three business days, as the employer deposit guide
  documents and each deposit's schedule code shows. Grouping by receipt month shifts the monthly depositors' 38% of receipts by a month
  and misstates every month by 2% to 9%.
* **Ask B (device-carried).** For TY2022 to TY2024, the cash estimated payments received for each tax year at each of the four
  instalments. *Device:* the January instalment arrives in the following calendar year. An overpayment carried forward from the prior
  return posts as a credit entry under the new tax year (payment type CF), and it is not cash. Grouping by calendar year, or counting
  credits as April payments, misstates 7 of the 12 cells.
* **Ask C (validity).** The three floors under each of the four rung constructions, with each construction's hit count out of 69 published
  cells.
* **Decoupling.** The withholding and estimated-payment ledgers share no row with the return file. Clearing the household construction
  changes no figure in asks A or B.

## 11. Rubric arithmetic

24 months (ask A) + 12 instalment cells (ask B) + 4 constructions × (3 floors and a hit count) (ask C) + the committed schedule's three floors,
the household-unit count and the twin-county counts + 4 named chart parts + 2 files ≈ 64 criteria.

## 12. World-building constraints

* 3,412,000 rows: 2,876,000 code 1, 97,000 code 2, 439,000 code 3. Code 2 and 3 filers are mostly commuters with federal AGI between
  $60,000 and $400,000, below every floor, so removing them raises each floor by about 12%.
* 168,000 resident couples file separately (336,000 returns), 71% of them in the top two deciles of federal filing units. Each separate
  return carries the federal primary TIN, giving 2,708,000 federal filing units.
* 380,000 resident returns are filed by people claimed on another resident return. They hold 2.1% of resident AGI, and each TIN sits on
  exactly one schedule. That gives 2,328,000 households with floors $214,000 / $318,000 / $742,000.
* Top-1% floors by rung are $504,000 / $565,000 / $667,000 / $742,000, and every other grid cell sits at least 10% below the answer. The
  dropped-dependents construction ($718,000) misses each year's total-AGI cell by −2.1%.
* Hit counts out of 69: households 69, federal filing units 58, return grain 3. Federal filing units fall short in the $500,000 to $1M
  class by 92, 38 and 121 units in TY2022 to TY2024 (TY2024's 121 include Kessler's 59). The Kessler and Abington twin facts hold exactly.
* No prior floors ship, and the withholding and estimated-payment ledgers touch no return.
