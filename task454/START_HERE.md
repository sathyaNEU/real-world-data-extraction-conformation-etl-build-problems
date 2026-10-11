# task454: start here

| | |
|---|---|
| Task | task454 |
| Objective (Axis 1) | Data Extraction & Conformation (ETL) |
| Block | task445 to task493 |
| Lane owner | unassigned (current owner and status: the root `START_HERE.md` on main) |
| Seed | ET11, `analytical_tasks/07_data_extraction_conformation/ET11_ndc-normalization-nadac-medicaid-spread.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task454`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task454-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Medicaid pharmacy spread: 10-digit NDCs, effective-dated prices and the dispensing fee hiding in the total
- **objective:** Data Extraction & Conformation (ETL / Pipeline Build)
- **domain:** Medicaid pharmacy benefit / payer analytics / drug pricing
- **decision_shape:** 03 · Bridge between two totals (amount reimbursed → NADAC ingredient benchmark)
- **committed_call:** Which drug class (FDA Established Pharmacologic Class) has the largest FY2023 fee-for-service ingredient spread in the state, and how large is it?
- **technique:** Segment-aware NDC 10→11 normalization; effective-dated price lookup (SCD type 2); billing-unit alignment; separating fee components from reimbursement totals
- **trap:** Naive left-padding of NDCs; current price applied to history; dispensing fees left inside "spread"
- **sources:** CMS State Drug Utilization Data (SDUD); CMS NADAC weekly files; FDA NDC Directory

## Seed note

## ET11, Medicaid pharmacy spread: 10-digit NDCs, effective-dated prices and the dispensing fee hiding in the total

| Field | Value |
|---|---|
| Domain | Medicaid pharmacy benefit / payer analytics / drug pricing |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 03 · Bridge between two totals (amount reimbursed → NADAC ingredient benchmark) |
| Core technique | Segment-aware NDC 10→11 normalization; effective-dated price lookup (SCD type 2); billing-unit alignment; separating fee components from reimbursement totals |
| Trap family (honest data) | Naive left-padding of NDCs; current price applied to history; dispensing fees left inside "spread" |
| Primary sources | CMS State Drug Utilization Data (SDUD); CMS NADAC weekly files; FDA NDC Directory |

### 1. The real-world project

A state Medicaid pharmacy team wants to extend its maximum-allowable-cost (MAC) list to one more **drug class**, picking
the class where fee-for-service reimbursement most exceeds acquisition cost. Analysts compare SDUD "Total Amount
Reimbursed" with NADAC × units. Their first cut showed huge spreads in classes dominated by cheap generics with many
prescriptions, and NADAC matches for only 70% of NDCs.

### 2. The business decision (one deterministic recommendation)

**Which drug class (FDA Established Pharmacologic Class) has the largest FY2023 fee-for-service ingredient spread in the
state, and how large is it?**

Rules (pharmacy analytics standard):

* Utilization: SDUD rows with `Utilization Type = FFSU`, the state, federal FY2023 quarters (2022Q4–2023Q3), `Suppression
  Used = false`.
* NDC conformance: FDA `NDCPACKAGECODE` (10 digits, 4-4-2 / 5-3-2 / 5-4-1) → 11-digit 5-4-2 by inserting a leading zero
  **in the short segment** (4-4-2 → 0xxxx-xxxx-xx; 5-3-2 → xxxxx-0xxx-xx; 5-4-1 → xxxxx-xxxx-0x), then remove hyphens.
* Class: first EPC term in the FDA product's `PHARM_CLASSES` (`[EPC]` suffix).
* Ingredient benchmark = units reimbursed × NADAC per unit, where NADAC per unit for a quarter is the mean of the rates
  **in effect** on the last day of each of the quarter's three months (rate in effect = latest `Effective Date` ≤ that
  day, taken from the weekly file published closest after that day).
* Dispensing fee = number of prescriptions × the state's FFS professional dispensing fee for the period (from the state
  plan excerpt in the folder).
* Ingredient spread = Total Amount Reimbursed − dispensing fees − ingredient benchmark, over NADAC-priced NDCs only;
  unpriced NDCs are a separate bridge item.

### 3. Why this gets overlooked in real projects

* NDCs look numeric. Stripping hyphens and left-padding to 11 digits works for 4-4-2 codes and silently produces *valid
  but wrong* codes for 5-3-2 and 5-4-1 codes; some collide with real, different packages.
* NADAC is published weekly as a full current list; the easiest join is "latest file", which applies 2024 prices to 2023
  utilization. Generic prices drift downward, so history looks overpaid.
* "Total Amount Reimbursed" includes the pharmacy's dispensing fee. Classes with many low-cost prescriptions look like
  spread leaders when the gap is mostly fees.

### 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–2 | `sdud_2022.csv`, `sdud_2023.csv` | CSV | ~5M each (national) | data.medicaid.gov State Drug Utilization Data | U.S. Gov public domain | Utilization and reimbursement |
| 3–15 | `nadac_week_YYYY-MM-DD.csv` (≈13 weekly files nearest each month-end, Sep 2022–Oct 2023) | CSV | ~25–30k each | data.medicaid.gov NADAC | Public domain | Effective-dated unit prices |
| 16 | `fda_ndc_product.txt` | TSV | ~100k | FDA NDC Directory | Public domain | Product, PHARM_CLASSES |
| 17 | `fda_ndc_package.xlsx` | XLSX | ~250k | FDA NDC Directory (also excluded/unfinished files) | Public domain | Package codes |
| 18 | `nadac_methodology.pdf` | PDF |, | CMS NADAC survey methodology | Public domain | Pricing unit, effective date meaning |
| 19 | `state_plan_dispensing_fee_excerpt.pdf` | PDF |, | State Medicaid plan amendment (public) | Public | Fee amount and dates |
| 20 | `analytics_standard.pdf` | PDF |, | Task author |, | Rules in §2 |

### 5. Deterministic solution path

1. Normalize FDA package codes to 11 digits by segment pattern; build NDC11 → EPC map (include excluded/unfinished files
   for completeness; flag unmapped).
2. Filter SDUD; join to EPC.
3. Build quarter NADAC per unit for each NDC11 from month-end effective rates.
4. Compute fees, benchmark and spread by class; rank; choose top class.
5. Bridge for the chosen class: Total reimbursed → − dispensing fees → − NADAC benchmark (priced NDCs) → − reimbursement
   on unpriced NDCs → ingredient spread.
6. Re-run with naive padding, latest-NADAC and fee-inclusive variants for comparison.

### 6. The traps

**Trap A, naive padding.** 5-3-2 and 5-4-1 codes map to wrong or nonexistent NDC11s; whole products drop out of their
class or land in another class.

**Trap B, latest NADAC.** Generic-heavy classes gain apparent spread; the top class changes.

**Trap C, fees in spread.** High-volume, low-cost classes jump to the top.

**Trap D, averaging NADAC over all weekly rows.** Over-weights weeks and mis-handles mid-quarter price changes.

### 7. Why the data is honest

SDUD, NADAC and the NDC Directory are official public files. NDC formats, effective dates and dispensing fees are all
documented. The work is joining them correctly.

### 8. Draft task prompt (prose)

> We will add one more drug class to the state MAC list: the class with the largest fee-for-service ingredient spread in
> federal FY2023 under our analytics standard. Using the SDUD, NADAC and FDA NDC files in the folder, compute every
> class's spread and name the class. Deliver `class_spread.xlsx` ranking the top twenty classes with total reimbursed,
> prescriptions, dispensing fees, NADAC benchmark, unpriced reimbursement and ingredient spread; and `spread_bridge.png`,
> a waterfall for the chosen class from total amount reimbursed to ingredient spread. On the workbook's first sheet,
> state the class, its spread, the runner-up, and which class would have been chosen if dispensing fees had been left
> in.

### 9. Deliverables

* `class_spread.xlsx`, `spread_bridge.png`.

### 10. Where 25+ rubric criteria come from

* 20 class spreads/ranks (top 10 checked); chosen class and runner-up; bridge bars; fee-inclusive alternative; NDC11
  conversions for 3 spot-check codes of each format.

### 11. Golden-output checklist

* Segment-aware NDC conversion; month-end effective NADAC; fees removed; unpriced separated; decision stated.

### 12. Build notes (scope tuning)

* Pick a state whose FFS volume is large enough (FFS is small in heavily managed-care states) and confirm that Traps A–C
  each change the chosen class or its spread by >10%.
* Confirm the dispensing-fee amount and effective dates from the state's approved plan amendment.
