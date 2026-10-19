## Tags

**Domain:** Actuarial Science & Insurance, claims frequency and severity (which three of a mutual motor insurer's eight rating regions go in the top accident frequency band of its 2027 rating basis, once the 2027 wording makes step protection standard and an at-fault claim no longer costs a policy its no-claims steps).
**Analytical objective:** Descriptive & Distribution Analysis (each region's accident claim frequency over the 2024 and 2025 accident years on the 2027 wording, read from a claims record cut below the size each policyholder chose to pay for privately rather than lose steps).

## 1. Final Recommendation

**Band C of the 2027 rating basis holds North West, West Midlands and Yorkshire and the Humber; South East is the first region below.**
North West's policyholders stand mostly on the middle no-claims steps, where a claim costs the most premium over the climb back, so they paid more of their small damage themselves; scaled from its claims above £2,500, which nobody pays privately, by the 37.8 per cent of step 0 and Step Protection claims that large, North West moves above South East on the 2027 wording. Not South East on the reported frequency (12.5 against North West's 11.8 per 100 vehicle-years), which counts only the claims the 2024 scale let through. Not South East on the Step Protection holders' uplift (1.27 times other policyholders' frequency on steps 6 to 9), which the holders' claims above £2,500 share, so it carries their choice of the add-on, and which never reaches steps 1 to 5, where most claims are kept back.

## 2. Critical Components

1. Vehicle-years earned over the 2024 and 2025 accident years: **182,255**; accident claims paid or reserved above nil: **19,592**
2. Reported frequency per 100 vehicle-years: South East **12.5** against North West **11.8**

## 3. Step-by-Step Solution

1. Earned each policy year in policy_terms_legacy_export_2023_2025.csv and policy_terms_platform_export_2025_2026.csv (the legacy expiry date is the last day on cover, the platform's term_end the renewal date, a cancellation ends cover) over 2024 and 2025, split at each mid-term adjustment in mid_term_adjustments_2023_2026.csv and placed by rating_region_postcode_map.csv on the day (rating_basis_2027_note.pdf, section 2): 182,255 vehicle-years.
2. Took the accident claims in claims_legacy_export_2023_2025.csv (amounts in pence) and claims_platform_export_2025_2026.csv with incurred above nil and an accident date in 2024 or 2025 (section 2), each joined to the policy year covering its accident date, through policy_number_crosswalk_2025.csv where a claim carries the platform number: 19,592 claims, South East reporting 12.5 per 100 vehicle-years and North West 11.8.
3. Compared claim sizes by step: a claim costs a step 0 or Step Protection policy no steps, and their claims show the full size distribution; on steps 1 to 9 without protection small claims are missing in proportion to the premium a claim costs on the step (no_claims_step_scale_2024.pdf), and above £2,500 the two distributions agree.
4. Divided each region's accident claims above £2,500 by 37.8 per cent, the share of step 0 and Step Protection claims above £2,500, over its vehicle-years: North West, West Midlands and Yorkshire and the Humber lead, South East next; the same band at every threshold from £1,500 to £3,000.
5. Windscreen (the basis note, section 3): counted Clearvane Auto Glass's jobs billed to the Society in glass_partner_jobs_2025.csv that repair or replace a screen, a job's lines one claim, at net plus VAT, and the windscreen claims of repairers the policyholder chose; the platform's windscreen claims from 1 July 2025 that carry a partner job's policy number, booking day and net amount are that job registered again and are not counted twice, and a partner job that is a camera recalibration alone recalibrates the screen another repairer fitted on the same policy just before, so its amount with VAT is part of that repairer's claim and it is not a claim of its own; over comprehensive vehicle-years in 2025 by cover and region on the day.
6. Theft (the basis note, section 4): grouped the theft claims of both exports by police crime reference (the legacy system writes it with separators), so a recovered car's repair claim stays with its theft, dated each theft by its first claim's loss date, kept those with a cost, and took every claim's incurred less the net proceeds in salvage_sales_statements_2025_2026.xlsx (both years' statements), over 2025 vehicle-years on either cover.
7. Band C for 2027: North West, West Midlands and Yorkshire and the Humber; first region below, South East.

## 4. Deliverable Answers

### 2027_rating_basis_bands.xlsx

1. Band C: North West, West Midlands, Yorkshire and the Humber
2. First region below band C: South East
3. 2025 windscreen claims per 100 vehicle-years with glass cover, and their average cost including VAT:
   - North East and Cumbria: 10.7; £273
   - North West: 13.0; £307
   - Yorkshire and the Humber: 11.3; £285
   - East Midlands: 10.7; £296
   - West Midlands: 12.7; £324
   - East of England: 9.5; £322
   - South East: 11.7; £369
   - South West and Wales: 10.2; £292
4. 2025 thefts per 1,000 vehicle-years, and their average cost net of salvage:
   - North East and Cumbria: 7.5; £5,474
   - North West: 13.7; £4,959
   - Yorkshire and the Humber: 11.0; £4,847
   - East Midlands: 10.6; £4,917
   - West Midlands: 15.8; £5,310
   - East of England: 5.7; £4,651
   - South East: 8.8; £5,289
   - South West and Wales: 5.6; £6,444

### band_c_frequency_2027_basis.png

1. A bar chart of the eight regions' accident frequencies on the 2027 wording, band C (North West, West Midlands and Yorkshire and the Humber) marked above the line, each region's reported frequency shown beside its bar.
