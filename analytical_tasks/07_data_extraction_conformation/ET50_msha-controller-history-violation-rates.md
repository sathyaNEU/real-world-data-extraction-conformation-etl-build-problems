# ET50 — Mine-safety performance by parent company: violations belong to the controller at the time, not the owner today

| Field | Value |
|---|---|
| Domain | Mining / industrial safety / ESG screening and insurance underwriting |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (ten controllers selected for engagement) |
| Core technique | Effective-dated (SCD type 2) ownership attribution for both numerator events and denominator exposure; day-weighted allocation of quarterly exposure across ownership changes; exposure scope rules (operator vs contractor, sub-units) |
| Trap family (honest data) | Current controller used for history; hours including contractor/office sub-units; violator type ignored; controller names instead of IDs |
| Primary sources | MSHA Open Government Data (Mines, Controller/Operator History, Violations, Quarterly Employment/Production), MSHA data dictionaries |

## 1. The real-world project

An ESG research team (and the insurer that licenses its scores) ranks mine **controllers** — the parent companies MSHA
records as controlling mine operators — by significant-and-substantial (S&S) violation rate per 200,000 hours worked
over 2021–2023, and engages the ten worst. The analyst joined violations and hours to each mine's *current* controller.
A company that bought several troubled mines in 2023 inherited their 2021–2022 record; the sellers looked spotless.

## 2. The business decision (one deterministic recommendation)

**Which ten controllers are selected for engagement (highest 2021–2023 S&S rate among controllers with ≥ 1,000,000
hours), and which controller is eleventh?**

Rules (scoring method):

* Attribution: each violation and each hour is attributed to the controller **in effect at that date**, from the
  Controller/Operator History (start/end dates; open end = still in effect).
* Numerator: violations with S&S = Y, issued to the **operator** (violator type operator, not contractor), dated
  2021-01-01 … 2023-12-31, excluding vacated citations (field per the dictionary).
* Denominator: operator hours worked from the quarterly employment/production file, all sub-units except office workers
  (sub-unit 99). When a controller change occurs within a quarter, allocate the quarter's hours by calendar days under each
  controller.
* Rate = S&S violations × 200,000 ÷ hours. Controller identity = `CONTROLLER_ID`.
* Rank descending; ties by more hours.

## 3. Why this gets overlooked in real projects

* The Mines table carries convenient `CURRENT_CONTROLLER_*` columns; history lives in a separate file with overlapping
  operator and controller date ranges.
* Exposure is quarterly while events are daily; ownership changes mid-quarter need allocation, which most joins skip.
* Contractors receive violations at mine sites; their hours are in a different file. Mixing them distorts both sides.
* Controller names vary in spelling across records; IDs are stable.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `Mines.txt` | Pipe-delimited | ~90k | MSHA Open Government Data | U.S. Gov public domain | Mine attributes, current controller |
| 2 | `ControllerOperatorHistory.txt` | Pipe-delimited | ~150k+ | MSHA | Public domain | Effective-dated controllers/operators |
| 3 | `Violations.txt` | Pipe-delimited | ~3M | MSHA | Public domain | Violations (S&S, violator type, dates) |
| 4 | `Inspections.txt` | Pipe-delimited | ~1M+ | MSHA | Public domain | Context |
| 5 | `MinesProdQuarterly.txt` | Pipe-delimited | ~1.5M | MSHA | Public domain | Operator hours by sub-unit |
| 6 | `ContractorProdQuarterly.txt` | Pipe-delimited | ~0.3M | MSHA | Public domain | Contractor hours (must not be mixed) |
| 7 | `*_Definition_File.txt` (dictionaries for each dataset) | Text | — | MSHA | Public domain | Field definitions |
| 8 | `msha_ss_designation_guidance.pdf` | PDF | — | MSHA | Public domain | S&S meaning |
| 9 | `scoring_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `sector_scope.json` | JSON | ~5 | Task author | — | Commodity/sector scope (e.g. coal + metal/non-metal) |

## 5. Deterministic solution path

1. Build controller intervals per mine; for each violation, find the controller in effect on its date.
2. For each mine-quarter, split hours across controllers by days (excluding sub-unit 99, operator hours only).
3. Filter violations (S&S, operator, period, not vacated); aggregate counts and hours by controller.
4. Apply the hours floor; compute rates; rank; ten + eleventh.
5. Contrast: current-controller attribution; contractor-inclusive counts/hours.

## 6. The traps

**Trap A — current controller.** Acquirers inherit sellers' histories; the ten change.

**Trap B — quarter not split.** Hours assigned wholly to one controller around transactions.

**Trap C — contractors/office hours mixed.** Rates diluted or inflated unevenly.

**Trap D — names, not IDs.** Splits large controllers below the floor.

## 7. Why the data is honest

MSHA's datasets are the agency's official records; controller history is explicitly maintained with dates. The method
defines attribution; nothing is planted.

## 8. Draft task prompt (prose)

> We engage the ten controllers with the worst 2021–2023 S&S violation rates per 200,000 hours, among controllers with at
> least a million hours, attributing every violation and every hour to the controller in charge at the time, as our scoring
> method describes. Using the MSHA files in the folder, tell me the ten and the eleventh. Provide `controller_rates.csv`
> (controller ID, name, mines controlled during the period, hours, S&S violations, rate, rank) and `controller_rates.png`, a
> ranked bar chart of the top twenty with the cut after ten and controllers involved in an ownership change marked. Add a
> one-page `engagement_memo.pdf` with the list, the margin at the cut, and which controllers would enter or leave the list if
> current controllers had been used.

## 9. Deliverables

* `controller_rates.csv`, `controller_rates.png`, `engagement_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 controllers + 11th + margin; rates for top 20; hours/violations for 3 controllers with transactions; current-controller
  variant entrants/leavers.

## 11. Golden-output checklist

* Date-effective attribution; day-split quarters; operator-only scope; IDs; decision stated.

## 12. Build notes (scope tuning)

* Choose a sector scope where at least two controller changes in 2021–2023 involved mines with high S&S counts; confirm
  Trap A changes the ten.
* Confirm violator-type and vacated-status field names in the MSHA definition files.
