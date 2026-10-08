# OS32 — Savings from preventable admissions: you will not reach zero, and charges are not costs

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Gap-to-best-performer sizing (closing the gap to top-quartile stores, regions or teams) where "eliminate all" targets and list prices inflate the opportunity |
| Domain | Healthcare / population health |
| Task shape | 01 · Ranked list under a cap (5 counties for a care-coordination programme by achievable cost savings) |
| Core method | AHRQ Prevention Quality Indicator (PQI) admissions identified from diagnosis codes; county rates per 1,000 adults; achievable benchmark = the 25th-percentile county rate (top quartile) by age band; avoidable admissions = max(0, rate − benchmark) × population; costs = charges × hospital cost-to-charge ratio |
| Analytical stump | Sizing savings as eliminating all PQI admissions assumes a zero rate that no population achieves; using charges instead of costs overstates savings by ~3×. Ranking counties by total PQI charges picks large counties, not those with the largest achievable gap |
| Primary sources | New York SPARCS hospital inpatient discharges (de-identified), New York State health data; HCRIS/CMS cost-to-charge ratios |

## 1. The real-world situation

A Medicaid managed-care plan will fund care-coordination programmes in **5** New York counties. The proposal sized savings as all
ambulatory-care-sensitive admissions' charges and ranked counties by that total. Finance asked for an achievable-benchmark estimate in costs.

## 2. The decision (one deterministic recommendation)

**The 5 counties selected, ranked by achievable annual cost savings, and the 6th.**

Rules (programme memo):

* Data: SPARCS inpatient de-identified discharges for the year in memo; adults 18+; PQI overall composite (PQI 90) identified using the AHRQ
  specification codes provided (ICD-10-CM lists), excluding transfers per spec.
* County: patient county of residence (as reported); population by county and age band from Census estimates.
* Rates by county × age band (18–39, 40–64, 65+).
* Benchmark per age band = 25th percentile of county rates (unweighted across counties with ≥ 20 PQI admissions).
* Avoidable admissions = Σ_bands max(0, rate − benchmark) × population.
* Average cost per PQI admission in the county = Σ charges × hospital CCR ÷ admissions (CCR by facility per memo's file).
* Achievable savings = avoidable × average cost × 0.5 (programme effectiveness per memo).
* Rank; top 5; report #6.

## 3. Why capable analysts get it wrong

* Total charges for preventable admissions make striking headlines.
* Zero is not an achievable rate; benchmarks reflect what peers achieve.
* Charges are list prices; costs are much lower.
* Age structure differs by county; benchmarks must be age-specific.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Hospital_Inpatient_Discharges__SPARCS_De-Identified___<year>.csv` | CSV | ~2.1M | New York State Department of Health (health.data.ny.gov) | NY open data terms (public) | Discharges with diagnoses, county, charges |
| 2 | `sparcs_deidentified_data_dictionary.pdf` | PDF | — | NYSDOH | Public | Fields |
| 3 | `ahrq_pqi_90_technical_specs.pdf` | PDF | — | AHRQ | Public domain | Code lists |
| 4 | `pqi_icd10_code_lists.json` | JSON | ~2k codes | Task author (from AHRQ specs) | Public domain | Diagnosis codes |
| 5 | `facility_cost_to_charge.csv` | CSV | ~200 | Derived from CMS cost report data (cite) | Public domain | CCR by facility |
| 6 | `county_population_age.csv` | CSV | ~62 × 3 | Census estimates | Public domain | Population |
| 7 | `programme_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `proposal_total_charges.xlsx` | XLSX | 62 | Task author | — | Naive ranking |

## 5. Deterministic solution path

1. Filter adults; flag PQI admissions with code lists and exclusions.
2. Rates by county × age band; benchmarks; avoidable admissions.
3. Costs via CCR; achievable savings; rank; top 5 + #6.
4. Contrast with the charges-based ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — all PQI charges.** Overstated and mis-ranked.

**B — benchmark of zero.** Unachievable.

**C — all-ages benchmark.** Age confounding.

**D — charges as costs.** ~3× overstatement.

## 7. Why the stump is analytical, not semantic

Codes, benchmarks and conversions are specified. The trap is unachievable targets and price-versus-cost confusion.

## 8. Draft task prompt (prose)

> Which five counties should get care-coordination programmes? Size achievable savings against top-quartile benchmarks in costs, as the programme
> memo specifies. Provide `county_savings.csv` (county: PQI admissions, rates by age, avoidable, cost per admission, savings, rank),
> `rate_vs_benchmark.png`, and a one-page `county_selection.pdf`.

## 9. Deliverables

* `county_savings.csv`, `rate_vs_benchmark.png`, `county_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 counties + #6; benchmarks (3); values for 8 counties; contrast.

## 11. Golden-output checklist

* PQI flagging; exclusions; age bands; benchmark; CCR; effectiveness; ranking.

## 12. Build notes (scope tuning)

* Confirm the charges-based top 5 includes at least two counties outside the achievable-savings top 5.
