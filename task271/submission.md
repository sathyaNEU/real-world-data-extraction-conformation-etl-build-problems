## Tags

> **Domain:** Actuarial Science & Insurance (claims frequency and severity).
> **Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Open the 2027 agency in Dorrance Hill Borough.** Its owner-occupied single-family homes would bring 21 non-weather water claims per 1,000 house-years at our 2023 to 2025 experience, 4 fewer than Sallowmead's 25. Not Sallowmead, 1,238 of whose 3,096 homes draw from the water authority's Valley zone. Not Brookmere (28), whose newer slab-built homes look safest on the policy record but 2,192 of whose 2,584 homes draw from the Valley zone, where our homes claim at 2.31 times the rate of the Upper zone.

## 2. Critical Components

1. Homes in the Valley zone: Dorrance Hill **217** of 2,769, Sallowmead **1,238** of 3,096, Brookmere **2,192** of 2,584
2. The Frequency Model Standard's 2025 test chooses foundation and water supply zone at a Poisson deviance of **3,169.4**, against **3,252.4** for the best model on the characteristics the policy terms record (foundation alone)
3. Non-weather water claims per 1,000 house-years: Dorrance Hill **21**, Sallowmead **25**, Brookmere **28**

## 3. Step-by-Step Solution

1. Earned house-years by home and accident year from policy_terms_2023_2025.csv (standard 2.4) and non-weather water claims from claims_register_2023_2025.csv (standard 2.1 to 2.3: WTR-P, WTR-A, 3110, 3120 and 3130, each claim once with the -R1 lines dropped, by date of loss): 1,258 claims over 54,233.4 house-years, 23 per 1,000.
2. Placed each home's parcel point from tamswold_parcels_2026.csv in tcwa_pressure_zones.geojson (the Upper zone's two polygons are one zone): 217, 1,238 and 2,192 of the townships' homes are in the Valley zone.
3. Ran the standard's section 4 search over every main-effects Poisson model on foundation, year built era, full bathrooms, construction, stories and zone, fitted on 2023 and 2024 and judged on 2025: foundation and zone win at 3,169.4, the best model without the zone (foundation alone) scores 3,252.4.
4. Refitted the model on 2023 to 2025 (Valley zone 2.31 times the Upper zone) and averaged each township's owner-occupied single-family homes (R-SFD with the homestead exclusion, card 1 of tamswold_dwellings_2026.csv mapped per the underwriting guide): Dorrance Hill 21, Sallowmead 25, Brookmere 28 per 1,000 house-years.
5. Protected homes per the underwriting guide section 2: each test in tcwa_hydrant_flow_tests.csv joined to its hydrant by the number in force on its date (FORMER_ID before April 1, 2024), the latest test's flow carried to 20 psi residual by NFPA 291 (flow times ((static - 20) / (static - residual)) to the 0.54), in-service authority hydrants within 1,000 feet: Dorrance Hill 2,182, Sallowmead 2,686, Brookmere 1,994.
6. Market value: the roll's 2026 assessed totals, replaced by the 2026 decisions in assessment_appeals_2026.csv, over the common level ratio in effect on January 1, 2026 (0.451): Dorrance Hill $804.6 million, Sallowmead $906.7 million, Brookmere $768.0 million.
7. Water claim payments: indemnity per claim from claim_payments_2023_2026.csv (the -R1 lines' payments folded into their claim) plus the latest paid to date in cas_bordereau_halverstead_2023_2026.xlsx for the claims Corrigan Adjusting Services handled, net of recoveries: 2023 $10,769, 2024 $11,056, 2025 $11,670; fire and lightning claims (FIR, 5110, 5120) on the book's unprotected homes: 5.3 per 1,000 house-years.
8. The agency opens in Dorrance Hill Borough, the township with the fewest non-weather water claims per house-year.

## 4. Deliverable Answers

### agency_township_2027.xlsx

1. Non-weather water claims per 1,000 house-years: Dorrance Hill 21; Sallowmead 25; Brookmere 28
2. Protected owner-occupied single-family homes: Dorrance Hill 2,182; Sallowmead 2,686; Brookmere 1,994
3. Total market value of those homes: Dorrance Hill $804.6 million; Sallowmead $906.7 million; Brookmere $768.0 million
4. Average non-weather water claim payment: 2023 $10,769; 2024 $11,056; 2025 $11,670
5. Fire and lightning claims per 1,000 house-years, 2023 to 2025, on the homes the guide classes as unprotected: 5.3

### water_claims_by_township_2027.png

1. Horizontal bars of the three townships' frequencies, Dorrance Hill (21) highlighted, Sallowmead 25 and Brookmere 28, against a dashed line at the book's own 23 per 1,000 house-years
