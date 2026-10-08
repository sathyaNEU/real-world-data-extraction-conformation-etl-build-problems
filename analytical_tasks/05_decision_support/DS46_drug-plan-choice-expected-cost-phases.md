# DS46 — Choosing a drug plan: price the whole year through the benefit phases, not the average month

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Choosing among pricing plans with tiers, caps and deductibles (cloud commitments, telecom plans, insurance) where cost is a piecewise function of uncertain usage |
| Domain | Health insurance / benefits advising |
| Task shape | 07 · Grid of cells (beneficiary profiles × 4 candidate Part D plans → expected annual out-of-pocket plus premium; the plan recommended for each profile) |
| Core method | For each plan: premium, deductible, tier cost-sharing (copay or coinsurance) by drug, out-of-pocket threshold (catastrophic phase/cap) from CMS plan files; simulate the year month by month through deductible → initial coverage → catastrophic for each profile's drug list and fill pattern; expected cost over a distribution of fills (memo's adherence scenarios); choose the minimum expected total |
| Analytical stump | Comparing plans on monthly copays at average use, or on premiums, ignores that costs accumulate through phases: a plan with a low copay but high deductible can cost more for a heavy user; the annual cap truncates costs nonlinearly. Expected cost over usage uncertainty differs from cost at average usage |
| Primary sources | CMS Prescription Drug Plan Formulary, Pharmacy Network and Pricing Information Files (quarterly public use files) |

## 1. The real-world situation

A benefits advisory service recommends Part D plans to clients. Its tool compares plans by premium plus 12 × the copays of the client's drugs at the
initial-coverage tier. Clients on specialty drugs reported much higher costs than the tool predicted in some plans and lower in others.

## 2. The decision (one deterministic recommendation)

**The recommended plan for each of 6 standard client profiles (lowest expected annual premium + out-of-pocket), and the profiles for which the tool's
recommendation differs.**

Rules (advisory memo):

* Data: CMS formulary/pricing files for the plan year and region in memo; 4 candidate plans (contract-plan IDs); drug prices (unit cost) and tier
  cost-sharing at preferred retail pharmacies.
* Profiles: 6 drug lists in `client_profiles.json` (NDCs, monthly quantities).
* Benefit phases per plan file: deductible (applies to tiers per plan), initial coverage cost-sharing, out-of-pocket cap per the plan year's rules.
* Fill uncertainty: each month's fill of each drug occurs with probability 0.9 (adherence), independently; expected OOP estimated by Monte Carlo
  over 20,000 simulated years (seed 2025).
* Expected annual cost = premium × 12 + E[OOP].
* Tool contrast: premium × 12 + 12 × initial-coverage copays.

## 3. Why capable analysts get it wrong

* Monthly copays are what members see.
* Deductibles and caps make annual cost nonlinear in usage.
* Expected cost under variable adherence differs from cost at average use.
* Plan rules vary (which tiers the deductible applies to).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `plan_information.txt` | Pipe-delimited | ~6k plans | CMS Part D PUF (formulary, pharmacy network, pricing) | U.S. Gov public domain | Premiums, deductibles |
| 2 | `basic_drugs_formulary.txt` | Pipe-delimited | ~1.5M | CMS | Public domain | Tiers by NDC/RXCUI |
| 3 | `beneficiary_cost.txt` | Pipe-delimited | ~200k | CMS | Public domain | Cost-sharing by tier/phase |
| 4 | `pricing.txt` | Pipe-delimited | ~10M | CMS | Public domain | Unit costs |
| 5 | `partd_puf_documentation.pdf` | PDF | — | CMS | Public domain | Layouts |
| 6 | `client_profiles.json` | JSON | 6 | Task author | — | Drug lists |
| 7 | `advisory_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `tool_recommendations.xlsx` | XLSX | 6 | Task author | — | Current tool output |

## 5. Deterministic solution path

1. Extract plan parameters, tiers, cost-sharing and prices for candidates.
2. Simulate annual OOP per profile × plan with phases and cap.
3. Expected totals; recommendations; contrast with tool.

## 6. Wrong paths (method errors, not misreadings)

**A — premium + 12 × copay.** Ignores phases.

**B — cost at average fills (0.9 × 12) deterministically.** Misses nonlinearity near thresholds.

**C — ignoring tier-specific deductible rules.** Wrong OOP.

**D — wrong pharmacy network pricing.** Different cost-sharing.

## 7. Why the stump is analytical, not semantic

Files and rules are specified. The trap is linear thinking about piecewise annual costs under uncertainty.

## 8. Draft task prompt (prose)

> Which Part D plan should we recommend for each client profile? Simulate annual costs through the benefit phases as the advisory memo specifies and
> compare with our tool. Provide `plan_grid.csv` (profile × plan: premium, expected OOP, total), `cumulative_oop.png`, and a one-page
> `plan_recommendations.pdf`.

## 9. Deliverables

* `plan_grid.csv`, `cumulative_oop.png`, `plan_recommendations.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 profiles × 4 plans = 24 expected totals; 6 recommendations; tool differences.

## 11. Golden-output checklist

* Plan parameters; tier mapping; phase logic; cap; simulation; recommendation.

## 12. Build notes (scope tuning)

* Include at least one specialty-drug profile and one low-use profile so the tool fails in both directions.
