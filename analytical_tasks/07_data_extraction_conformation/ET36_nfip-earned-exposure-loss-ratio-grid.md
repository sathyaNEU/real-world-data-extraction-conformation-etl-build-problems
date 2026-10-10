# ET36 — Flood insurance loss ratios from public policy and claim records: written vs earned, rows vs insured units

| Field | Value |
|---|---|
| Domain | Property & casualty insurance / catastrophe risk / public insurance programs |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 07 · Grid of cells (state × flood-zone group loss ratio) |
| Core technique | Pro-rata earned premium and exposure across calendar years from policy terms; accident-year assignment of claims by date of loss; unit-count fields vs row counts; consistent cohort definitions |
| Trap family (honest data) | Written premium by effective-date year used as denominator; claims by year of payment or file year; counting rows instead of insured units; including ICC payments inconsistently |
| Primary sources | OpenFEMA FIMA NFIP Redacted Policies (v2) and Redacted Claims (v2), NFIP data dictionaries |

## 1. The real-world project

A state insurance regulator's catastrophe unit compares National Flood Insurance Program experience across states and flood
zones to target outreach for private-market flood products. The analyst grouped policies by the year of
`policyEffectiveDate`, summed premiums, and divided claims paid in each year. A state hit by a late-December storm looked
catastrophic one year and benign the next; condominium master policies dominated "policy counts".

## 2. The business decision (one deterministic recommendation)

**For calendar (accident) year 2022, which state × zone-group cell in the region has the highest loss ratio (and becomes the
pilot market), and what is it?**

Rules (experience-study method):

* Earned premium for 2022 = Σ policy `totalInsurancePremiumOfThePolicy` × (days of the policy term falling in 2022 ÷ total
  days in the term). Policies with terms spanning 2021–2022 or 2022–2023 contribute partially.
* Earned exposure (insured unit-years) = Σ `policyCount` × days in 2022 ÷ 365 (the field records insured units per policy
  record, e.g. units under a condominium master policy).
* Incurred losses for 2022 = Σ over claims with `dateOfLoss` in 2022 of building + contents paid amounts (ICC paid excluded).
* Zone groups from `ratedFloodZone`: A-zones (A, AE, AH, AO, AR, A99, A1–A30), V-zones (V, VE, V1–V30), X/B/C (moderate/
  minimal), D.
* Loss ratio = incurred ÷ earned premium; cells with earned premium < $1m are not eligible.
* Pilot = maximum eligible cell.

## 3. Why this gets overlooked in real projects

* Policy records carry a single premium for a term; "premium by effective year" is written premium, not earned, and moves
  with renewal calendars.
* Claims have several date fields (date of loss, year of loss, original payment dates); payment timing shifts losses into
  later years.
* Rows are policies, not insured units; `policyCount` matters for exposure but is easy to miss.
* Increased Cost of Compliance payments are a separate coverage and distort building-loss comparisons.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `FimaNfipPolicies_region_2021_2023.parquet` (regional extract) | Parquet | 10–20M | OpenFEMA FIMA NFIP Redacted Policies v2 | U.S. Gov public domain | Policy terms, premium, units |
| 2 | `FimaNfipClaims.csv` | CSV | ~2.6M | OpenFEMA FIMA NFIP Redacted Claims v2 | Public domain | Claims with date of loss |
| 3 | `FimaNfipPolicies_dictionary.pdf` | PDF | — | OpenFEMA | Public domain | Field meanings (policyCount, premium) |
| 4 | `FimaNfipClaims_dictionary.pdf` | PDF | — | OpenFEMA | Public domain | Claim fields |
| 5 | `nfip_flood_zone_definitions.pdf` | PDF | — | FEMA | Public domain | Zone groups |
| 6 | `nfip_monthly_policy_statistics_2022.xlsx` | XLSX | ~600 | FEMA NFIP statistics | Public domain | Policies-in-force check |
| 7 | `nfip_claims_statistics_by_state.xlsx` | XLSX | ~60 | FEMA | Public domain | Loss totals check |
| 8 | `states_in_scope.json` | JSON | ~6 | Task author | — | Region |
| 9 | `experience_study_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `extraction_query.sql` | SQL | — | Task author | — | Documented extraction of the policy subset |

## 5. Deterministic solution path

1. Filter policies whose term overlaps 2022 in the region; compute day overlap; earned premium and unit-years.
2. Filter claims with date of loss in 2022; sum building + contents payments (exclude ICC).
3. Map zones to groups; aggregate by state × group; compute loss ratios; apply eligibility; pick the max.
4. Contrast: written-premium and payment-year methods; row counts vs `policyCount`.

## 6. The traps

**Trap A — written premium by effective year.** Denominators wrong where renewals cluster; cells reorder.

**Trap B — claims by file/payment year.** December-2022 events shift to 2023; the pilot cell changes.

**Trap C — rows as exposure.** Condo master policies understate exposure; frequency metrics wrong.

**Trap D — ICC included / zone mapping errors.** Distorts V-zone cells.

## 7. Why the data is honest

OpenFEMA's NFIP datasets are official redacted records with documented fields. Earned vs written is standard insurance
accounting; nothing is planted.

## 8. Draft task prompt (prose)

> We'll pilot private flood outreach in the state and flood-zone group with the worst 2022 NFIP experience, measured on an
> earned, accident-year basis as our experience-study method describes. Using the OpenFEMA policy and claim files in the
> folder, build the grid of loss ratios and tell me the pilot cell and its loss ratio. Deliver `loss_ratio_grid.xlsx` with
> state × zone-group earned premium, earned unit-years, incurred losses and loss ratio (ineligible cells marked), and
> `loss_ratio_heatmap.png` with the pilot cell outlined. On the first sheet, state the pilot cell, its loss ratio, the
> runner-up, and which cell a written-premium, payment-year analysis would have chosen.

## 9. Deliverables

* `loss_ratio_grid.xlsx`, `loss_ratio_heatmap.png`.

## 10. Where 25+ rubric criteria come from

* ~6 states × 4 zone groups = 24 cells (loss ratios + eligibility); pilot, runner-up; alternative-method pick.

## 11. Golden-output checklist

* Pro-rata earning; date-of-loss assignment; policyCount; ICC excluded; eligibility; decision stated.

## 12. Build notes (scope tuning)

* Choose a region with a major late-year 2022 flood event (or another accident year with a year-end event) so Trap B flips.
* The policy file is very large; document the extraction (states, date overlap) and record the OpenFEMA refresh date.
