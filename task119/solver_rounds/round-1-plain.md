# solver round: round 1, plain

**Proxy score 83.8 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 41.8 of 58). Main call LANDED. 4 of 11 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the 2027-28 external review at Stennock University Hospitals NHS Foundation Trust, where a year of review could confirm 27 deaths.

solver: Place the 2027-28 external review at Stennock (STN). Over the latest four complete quarters (July 2025 to June 2026), 27 of its 27 in-remit deaths are confirmable as own-care: each patient waited while Stennock gave freed level 3 beds to planned surgical admissions. The runner-up is Prideswick with 15 (gap 12). Lathingbury has the most in-remit deaths (56), but none are confirmable because it has no level 3 unit.

tokens matched 3 of 5 (28, 27, Place, Stennock University Hospitals NHS Foundation, Trust)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| external_review_placement_2027-28.docx | 1 | 1 | 2 | 50% |
| external_review_placement_2027-28.docx | 2 | 1 | 1 | 100% |
| external_review_placement_2027-28.docx | 3 | 1 | 3 | 33% |
| external_review_placement_2027-28.docx | 4 | 1 | 1 | 100% |
| review_placement_workings.xlsx | 1 | 20 | 32 | 62% |
| review_placement_workings.xlsx | 2 | 4 | 4 | 100% |
| review_placement_by_trust.png | 1 | 4 | 11 | 36% |
| review_placement_by_trust.png | 2 | 3 | 4 | 75% |
| review_placement_by_trust.png | 3 | 3 | 4 | 75% |
| review_placement_by_trust.png | 4 | 3 | 5 | 60% |
| review_placement_by_trust.png | 5 | 2 | 2 | 100% |

## Solver's path

1. Read the terms of reference (review_terms_of_reference_2027-28.docx). Remit: decided level 3; waited more than 4h from decision to admit to bed assignment; died within 30 days of the decision; counted under the referring trust. Judged on deaths confirmed avoidable through the trust's own care, with bed and staff decisions counting as own care. Placement uses the latest four complete quarters (2025Q3 to 2026Q2).
2. Checked the method against the NRR closed reviews: nrr_review_records.sqlite against nrr_escalation_reviews_closed_2021-2025.xlsx. Remit deaths built from level_decided=3, not stood down, wait from decision to bed >4h and death within 30 days of the decision match 'Deaths confirmed avoidable' exactly in all 34 reviews. Variants using the requested level, the wait from receipt, the arrival time or deaths at any time miss on 19 to 33 reviews. Every NRR unit had free beds when patients waited.
3. Built the referral record from critical_care_referrals_202307_202606.csv. Migrated CCRS (CC) times converted from UTC to Europe/London. CC levels taken from the DECISION entries in ccrs_referral_levels (243 requested-3/decided-2 referrals drop out; level changes all came after admission). CC bed time taken from the first acc_unit_stays row carrying the referral_id; platform outcome_at equals the stay admitted_at in all 11,481 cases. Dropped 307 duplicate platform records from the 19 Feb to 1 Apr 2024 pilot-ward double entry. Result: 29,952 referrals.
4. Deaths: date_of_death from the APC episodes, with temporary keys mapped through pas_patient_key_links; in-hospital death discharges used as a fallback. Days from decision to death split cleanly (in-remit deaths at 23 days or fewer, others at 36 or more), so the 30-day edge does not move any count.
5. Remit over the whole record: 2172 patients and 629 deaths. Latest four quarters: 213 deaths (LAT 56, RIS 44, BRK 35, STN 27, PRW 21, ELL 13, TAN 10, PEL 7).
6. Own-care test. Each trust's own level 3 unit is dated from acc_unit_register (ELL-ACC level 3 until 31 Mar 2024; PEL-W3 from 4 Dec 2023 to 31 Mar 2024). Occupancy rebuilt from the stays; it matches acc_bed_return beds_occupied_0800 exactly. A remit death is confirmable when the trust's own unit had a free bed during the wait, or admitted another patient (here always a planned surgical admission) during it. Trusts with no level 3 unit (LAT, TAN, and ELL/PEL outside their windows) wait on other trusts' beds and get 0.
7. Confirmable deaths, latest four quarters: STN 27 (every one waited while elective surgical admissions took the freed beds); PRW 15 (weekend and bank-holiday waits with a free bed, consistent with the on-site consultant rule); RIS 2; all others 0, BRK included (its own patients waited only while its unit was full). STN 27 leads PRW 15 by 12. Whole record: 148 confirmable (STN 80, PRW 46, RIS 8, ELL 6, BRK 5, PEL 3).

confidence: Medium-high. The remit definition matches the NRR record in all 34 reviews. The own-care test (a free bed, or a competing planned admission, during the wait) is inferred from the methodology note, because no NRR unit was ever full; the patterns in the data are clean, though (STN elective admissions, PRW weekend free beds).

notes: CCU and SDU referrals are counted as ward referrals: their stays are coded source 06 (ward) and no paediatric or obstetric specialties appear, so the children/maternity/critical-care-unit exclusions remove nothing. Two choices barely change the totals: the in-hospital death fallback and keeping the CCRS rather than the platform copy of the pilot duplicates.

### external_review_placement_2027-28.docx (solver's answers)
- Trust the review should sit in: Stennock (STN), Stennock University Hospital
- Deaths a year of review there could confirm: 27 deaths (confirmable deaths, July 2025 to June 2026, whole number)
- Trust that comes closest: Prideswick (PRW), 15 confirmable deaths
- Gap between the two: 12 deaths (27 - 15)

### review_placement_workings.xlsx (solver's answers)
- Per trust, whole record Jul 2023-Jun 2026: patients in remit / remit deaths / confirmable deaths: BRK 352 / 104 / 5; ELL 141 / 40 / 6; LAT 561 / 165 / 0; PEL 76 / 22 / 3; PRW 222 / 63 / 46; RIS 439 / 126 / 8; STN 276 / 80 / 80; TAN 105 / 29 / 0
- Column totals: Patients in remit 2172; remit deaths 629; confirmable deaths 148

### review_placement_by_trust.png (solver's answers)
- Remit deaths per trust, latest four quarters (Jul 2025-Jun 2026), with confirmable part: STN 27 (27 confirmable); PRW 21 (15); RIS 44 (2); LAT 56 (0); BRK 35 (0); ELL 13 (0); TAN 10 (0); PEL 7 (0); totals 213 remit deaths, 44 confirmable
- Bar order by confirmable part: STN 27, PRW 15, RIS 2, then the zero trusts (LAT, BRK, ELL, TAN, PEL)
- Gap to runner-up marked: 12 deaths, STN over PRW
- Title naming the trust: Stennock: 27 confirmable deaths in the year to June 2026, 12 more than Prideswick
