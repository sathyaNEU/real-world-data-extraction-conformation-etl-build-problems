# task243 submission

## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: a province's review of the completeness of death registration in the civil registry offices of its cities and municipalities, measured between two censuses).
**Analytical objective:** Data Quality Monitoring & Alerting (which offices' death registration falls below the 80 per cent completeness alert and goes into the first round of the 2024 Civil Registration Improvement Programme, with each office's timely birth registration and medical certification of deaths beside it).

## 1. Final Recommendation

**Five offices go into the first round of CRIP 2024: the City of Santa Cruz, San Isidro, Libertad, San Luis and Del Carmen register fewer than 80 per cent of their residents' deaths at ages 15 and over between the 2015 and 2020 census reference dates (about 63, 63, 56, 64 and 52 per cent); the other seven register 89 per cent or more and stay out.**

Completeness is the general growth balance of the two censuses' household population above each age against the deaths registered above it, carrying each office's net movement above each age from the 2020 census's residence five years earlier. Not the balance taken as closed, which reads the older residents who left Esperanza, Magsaysay and Mabini, most of them for elsewhere in the country, as deaths nobody registered and would send those three as well: with their movement in the balance they each register 89 per cent.

## 2. Critical Components

1. The five offices register **52 to 64** per cent of their residents' adult deaths (City of Santa Cruz 63; San Isidro 63; Libertad 56; San Luis 64; Del Carmen 52).
2. Esperanza, Magsaysay and Mabini register **89** per cent once the residents who left are in the balance.
3. Kalinawan City, Quezon, Rizal and San Miguel register **89 to 90** per cent.

## 3. Step-by-Step Solution

1. Deaths (D1 in crvs_review_terms_of_reference_2023.pdf): certificates of death in crs_death_records_extract_20230331.csv, rows repeated exactly dropped, the province's residents placed by the residence as written (every spelling mapped, Santa Cruz's records before its 2019 charter included), a death registered at a second office counted once at its first registration (same names, sex, date of death and date of birth), dated 1 August 2015 to 30 April 2020, by five-year age group at death, unstated ages spread over the office's stated ages in proportion.
2. Population: the household population by five-year age group in popcen2015_household_population_age_sex_kalinawan.xlsx and cph2020_household_population_age_sex_kalinawan.xlsx; the interval is 4.75 years (days between the reference dates over 365.25).
3. Movement: in cph2020_special_tabulation_pdpfp_kalinawan.csv each office's persons in 2020 who lived elsewhere on 1 May 2015 (NOT STATED spread in proportion to the stated rows of the same age group), less the persons anywhere in the country in 2020 who lived there then (ELSEWHERE IN THE PHILIPPINES included), by age group; each group's net movers split equally between that group and the next younger one (the age they moved at), times the interval over five years.
4. Balance: for ages x from 15+ to 65+ by five, the persons reaching x per year (the geometric mean of the two age groups either side of x in each census, the two censuses' values combined geometrically, over five) per person-year above x (the interval times the geometric mean of the two censuses' populations above x), less the growth rate above x, plus the net movers above x per person-year, against the registered deaths above x per person-year; orthogonal fit (the slope is the ratio of the two rates' standard deviations); completeness is one over the slope.
5. Accepted range: the same balance fitted from any lowest age of 10+ to 30+ to any highest of 55+ to 75+, with the movers kept at their census age, the movement not carried to the interval, a least-squares fit, the arithmetic mean of the two age groups for the persons reaching x, or completeness relative to either census, gives each office's range in the workbook answer; none of these readings crosses 80 per cent.
6. B1: births in crs_birth_records_extract_20230331.csv dated in 2022 to mothers resident in each city or municipality, rows repeated exactly dropped, each child counted once at its first registration (same child's names, sex, date of birth and mother; twins are two births), registered within 30 days.
7. C1: the residents' deaths dated in 2022, counted as in step 1; certified by a licensed physician when the certifier is an MD or attending physician or, for a certificate in the health office's name (MHO, CHO), when pho_health_office_clinical_staff_2019_2023.xlsx shows its signer in a physician's post on the date of death.
8. Alert (D1 below 80 per cent): the City of Santa Cruz, San Isidro, Libertad, San Luis and Del Carmen go into the first round.

## 4. Deliverable Answers

### lcro_death_registration_completeness_2015_2020.xlsx

1. Completeness (whole per cent, accepted range in brackets) and the first round:
   - Kalinawan City: 89 (84 to 94); stays out
   - City of Santa Cruz: 63 (59 to 66); goes in
   - San Isidro: 63 (60 to 67); goes in
   - Esperanza: 89 (84 to 99); stays out
   - Magsaysay: 89 (83 to 96); stays out
   - Mabini: 89 (82 to 96); stays out
   - Libertad: 56 (51 to 60); goes in
   - San Luis: 64 (59 to 68); goes in
   - Del Carmen: 52 (49 to 57); goes in
   - Quezon: 90 (86 to 95); stays out
   - Rizal: 89 (81 to 92); stays out
   - San Miguel: 90 (84 to 93); stays out
2. Share of 2022 live births registered within 30 days (per cent): Kalinawan City 88.0; City of Santa Cruz 76.5; San Isidro 73.6; Esperanza 85.2; Magsaysay 82.8; Mabini 81.6; Libertad 61.0; San Luis 66.0; Del Carmen 70.4; Quezon 86.0; Rizal 81.5; San Miguel 83.3.
3. Share of residents' 2022 deaths certified by a licensed physician (per cent): Kalinawan City 77.2; City of Santa Cruz 84.6; San Isidro 84.4; Esperanza 81.8; Magsaysay 77.3; Mabini 59.2; Libertad 39.8; San Luis 37.8; Del Carmen 64.6; Quezon 78.1; Rizal 74.9; San Miguel 75.9.

### crvs_committee_note_2023.docx

4. One chart: every city and municipality's completeness against the 80 per cent line, the five going into the first round (the City of Santa Cruz, San Isidro, Libertad, San Luis and Del Carmen) marked.
