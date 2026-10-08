# OS31 — Carbon-cost exposure for a shipping fleet: only part of each voyage's emissions is in scope

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Exposure sizing under scoped regulations (carbon pricing, digital services taxes, data-residency rules) where only a defined share of activity is liable and liability phases in |
| Domain | Maritime / carbon markets |
| Task shape | 02 · Forecast across many periods (annual EU ETS allowance cost 2024–2026 for a fleet; the hedge volume purchased for 2025) |
| Core method | From ship-level monitoring reports, split CO₂ into intra-EU voyages (100% in scope), voyages to/from EU ports (50%), and emissions at berth in EU ports (100%); apply the phase-in (40% of 2024 emissions surrendered, 70% of 2025, 100% of 2026); multiply by allowance price scenarios; fleet totals |
| Analytical stump | Multiplying total reported CO₂ by the allowance price overstates exposure: extra-EU legs count half, and surrender obligations phase in. Using only intra-EU emissions understates it. Exposure depends on each ship's trade pattern, which the monitoring data split explicitly |
| Primary sources | EU MRV (THETIS-MRV) ship-level CO₂ emissions reports published by EMSA |

## 1. The real-world situation

A shipping company must hedge its EU ETS allowance needs for 2025. Treasury multiplied the fleet's total reported CO₂ by the forward price
and proposed buying that volume. The sustainability team noted that only part of the fleet's emissions is in scope and that the obligation phases
in.

## 2. The decision (one deterministic recommendation)

**The number of allowances (thousand EUAs, rounded) to hedge for 2025 emissions, and the annual cost exposure 2024–2026 at the central price.**

Rules (treasury memo):

* Data: THETIS-MRV public reports for the company's ships (IMO numbers in memo) for the latest reporting year; fields for CO₂ from voyages
  between EU ports, voyages departing from EU ports, voyages to EU ports, and at berth.
* In-scope CO₂ = between-EU + at-berth + 0.5 × (departing + arriving) (memo's mapping of report fields).
* Fleet activity assumption: 2024–2026 emissions equal the latest year's (memo), except ships listed for sale in 2025 are excluded from 2025
  onward.
* Surrender share: 2024 → 40%, 2025 → 70%, 2026 → 100%.
* Allowances for year Y = in-scope CO₂ × share(Y).
* Cost = allowances × price scenario (low/central/high from memo).
* Hedge for 2025 = allowances(2025).

## 3. Why capable analysts get it wrong

* Total CO₂ is the headline figure in each report.
* Scope rules distinguish voyage types; reports already split them.
* Phase-in shares reduce early-year obligations.
* Fleet changes alter exposure.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `<year>-v<version>-<date>-EU MRV Publication of information.xlsx` | XLSX | ~12k ships | EMSA THETIS-MRV public reports | EU reuse policy (public; cite) | Ship-level emissions by voyage category |
| 2 | `mrv_report_field_guide.pdf` | PDF | — | EMSA | Public | Field definitions |
| 3 | `company_fleet.csv` | CSV | ~40 | Task author | — | IMO numbers, sale plans |
| 4 | `eu_ets_maritime_rules_citation.pdf` | PDF | — | Directive (EU) 2023/959 (cite) | EU reuse | Scope and phase-in |
| 5 | `price_scenarios.json` | JSON | 3 | Task author | — | EUA prices |
| 6 | `treasury_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `treasury_total_co2_hedge.xlsx` | XLSX | — | Task author | — | Naive hedge |

## 5. Deterministic solution path

1. Filter the company's ships; extract category emissions.
2. In-scope CO₂ per ship; fleet changes by year.
3. Allowances by year with phase-in; costs by scenario; hedge.
4. Contrast with treasury's figure.

## 6. Wrong paths (method errors, not misreadings)

**A — total CO₂ × price.** Overstated.

**B — intra-EU only.** Understated.

**C — no phase-in.** Overstated early years.

**D — ignoring fleet changes.** Misstated 2025–2026.

## 7. Why the stump is analytical, not semantic

The mapping and rules are specified. The trap is scoping and phasing liability correctly in exposure sizing.

## 8. Draft task prompt (prose)

> How many EU allowances should we hedge for 2025, and what is our cost exposure through 2026? Compute in-scope emissions per ship from the
> MRV reports as the treasury memo specifies. Provide `ets_exposure.csv` (ship × year: in-scope CO₂, allowances; fleet totals by scenario),
> `exposure_by_year.png`, and a one-page `hedge_recommendation.pdf`.

## 9. Deliverables

* `ets_exposure.csv`, `exposure_by_year.png`, `hedge_recommendation.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 years × 3 scenarios = 9 costs; hedge; in-scope CO₂ for 10 ships; contrast.

## 11. Golden-output checklist

* Ship filter; field mapping; 50% rule; phase-in; fleet changes; scenarios.

## 12. Build notes (scope tuning)

* Choose a fleet mixing intra-EU feeders and deep-sea ships so scope rules matter.
