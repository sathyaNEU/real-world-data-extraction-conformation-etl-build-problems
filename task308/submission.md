## Tags

**Domain:** Actuarial science and insurance (catastrophe exposure and accumulation).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Pennine should take the 2027 catastrophe layer: it is worth GBP 0.1 million a year there, GBP 0.1 million more than on any other book.** Not Severn Vale (GBP 0.0 million), which leads when recorded repair costs are carried forward by the index alone and where what the layer would recover about pays for its premium and expected reinstatement premium; nor Coastal North (GBP -0.5 million) or Fenland (GBP -0.8 million), where the premium and the expected reinstatement premium exceed what the layer would recover.

## 2. Critical Components

1. Pennine's four pre-2021 freezes (December 2010, January 2013, December 2017 and February 2018) each exhaust the layer at the 2027 scale: **4** full recoveries of GBP 15 million.
2. Pennine's expected recoveries are **GBP 3.75 million** a year.
3. Pennine's expected reinstatement premium is **GBP 0.73 million** a year, against a quoted premium of **GBP 2.93 million**.

## 3. Step-by-Step Solution

1. Built each region's windstorm, flood and freeze loss occurrences in home_claims_2010_2025.parquet by date of loss under catastrophe_event_definitions.pdf: one period of 72 hours (windstorm) or 168 hours (flood, freeze) from each catastrophe's first loss, holding every claim of the peril dated in it.
2. Carried each claim to the 2027 book and 2027 costs under catastrophe_layer_valuation_basis.pdf: its district's 2027 policies (the plan in business_plan_2027.xlsx, spread by the mid-2025 mix in exposure_by_district_2010_2025.csv) over the year's, times 146.4 over the index for its month of loss in rebuild_cost_index_2010_2026.xlsx.
3. Counted each region's repair panel firms each year (the distinct repair_contractor on its claims) and each occurrence's claims per firm, then and at the 2027 scale on the 2025 panel: Pennine's four pre-2021 freezes go from 22.6 to 25.1 claims a firm to 44.1 to 49.6.
4. Fitted the log of each occurrence's index-adjusted cost per claim on its claims per firm across the 64 occurrences of 150 claims or more, claim-weighted, with a level for each peril and a hinge at 16.5 claims a firm (2.8 per cent a claim a firm above it), and re-priced each occurrence by the fit at its 2027 claims per firm over the fit at its own.
5. Applied the layer under cat_xl_quotations_2027.pdf to each occurrence, capped each year at GBP 30 million, averaged 2010 to 2025 and took off the quoted premium and the expected reinstatement premium: Pennine GBP 0.1 million; Severn Vale GBP 0.0 million; Coastal North GBP -0.5 million; Fenland GBP -0.8 million.
6. Ask A: the five perils' claims in home_claims_2010_2025.parquet; each claim the Major Loss Unit holds in major_loss_unit_monthly_2023_2026.xlsx (its cases grouped by policy, peril and the date of loss on their latest rows, and joined to the platform claim with that policy and peril dated on any date of loss the cases have carried) at the sum of its cases' latest incurred, in the year of that latest date of loss, unless one of its cases dropped out of the reports before October 2026 without a Closed row, when the platform's claim stands as it is; the unit's claims with no platform claim added in the year of their latest date of loss unless one of their cases dropped out the same way; over the mid-year policies in force in exposure_by_district_2010_2025.csv: the twelve figures in block 4.
7. Ask B: direct_policies_in_force_2025-12-31.csv plus every Lowther and Pike term in lowther_pike_risk_bordereaux_2025-10_to_2026-02.csv whose dates cover 31 December 2025, less each term with a cancellation effective by that day unless the term is listed for a later month that began after the cancellation took effect (a reinstatement; a rewrite ends one term and starts another under the same policy number), each at its first listed sum insured moved by endorsements effective by that day: the four figures in block 4.
8. Recommended Pennine, where the layer is worth most.

## 4. Deliverable Answers

### cat_layer_placement_2027.pdf

1. Region to take the layer: Pennine.
2. The layer's value on Pennine: GBP 0.1 million.
3. The layer's value on each of the other three: Severn Vale GBP 0.0 million; Coastal North GBP -0.5 million; Fenland GBP -0.8 million.

### cat_layer_workbook_2027.xlsx

1. Incurred at 31 October 2026 per policy in force, escape of water, accidental damage, theft, fire and subsidence claims taken together:
   - 2023: Fenland GBP 117.89; Pennine GBP 135.36; Severn Vale GBP 113.58; Coastal North GBP 122.17
   - 2024: Fenland GBP 117.26; Pennine GBP 134.52; Severn Vale GBP 120.57; Coastal North GBP 116.35
   - 2025: Fenland GBP 121.28; Pennine GBP 130.95; Severn Vale GBP 125.88; Coastal North GBP 135.16
2. Buildings sums insured on 31 December 2025:
   - Fenland: GBP 59,442.2 million
   - Pennine: GBP 73,441.1 million
   - Severn Vale: GBP 131,316.2 million
   - Coastal North: GBP 71,630.8 million
