# task119 · Placing the Wenmarsh external review of deaths after delayed escalation, 2027-28

## Tags

**Domain:** Policy & Education (public administration: a regional health board placing its one external mortality review among eight acute trusts).
**Analytical objective:** Anomaly Detection & Diagnostics (separating the long waits a trust's own care made from the waits network capacity made).

## 1. Final Recommendation

**Place the 2027-28 external review at Stennock University Hospitals NHS Foundation Trust, where a year of review could confirm 27 deaths.**

That is 12 deaths ahead of the runner-up, Prideswick Hospitals NHS Foundation Trust, at 15. Not Lathingbury, which has the most deaths inside the remit but runs no level 3 beds, so every wait was for another trust's bed. Not Ristenholm, where 2 deaths followed a wait beside its own empty staffed bed, or Brackenford, where none did; their other long waits passed with their own units full and admitting no planned patients. Not Prideswick, whose waits beside its own empty staffed beds account for fewer deaths. Not Ellerdyke, Tannerby or Pellowham, which held no level 3 beds in the placement year.

## 2. Critical Components

1. Lathingbury has the most deaths inside the remit in July 2025 to June 2026, **56**, and holds no level 3 beds
2. All **27** of Stennock's deaths inside the remit followed waits through which its full unit was admitting planned surgical patients from Stennock's own theatres
3. Prideswick's deaths after waits beside its own empty staffed beds are **15**
4. Stennock leads Prideswick by **12** deaths

## 3. Step-by-Step Solution

1. Took referrals in `critical_care_referrals_202307_202606.csv` with a level 3 decision to admit from July 2025 to June 2026 (the placement basis in `review_terms_of_reference_2027-28.docx`, section 5) that waited more than four hours from `dta_at` to the bed's assignment: 731 patients.
2. Linked `date_of_death` from `apc_episodes_referred_patients_2022-2026.parquet` within 30 days of the decision: 213 deaths, Lathingbury the most at 56.
3. Read each referring trust's own level 3 unit from `acc_unit_register.csv` on the decision date: Lathingbury, Tannerby, Ellerdyke and Pellowham held none, so none of their deaths is their own care.
4. Rebuilt each unit's census minute by minute from `acc_unit_stays_202306_202606.parquet` against `beds_open` in `acc_bed_return_0800_202306_202606.csv`: Prideswick 15 and Ristenholm 2 deaths followed waits beside the trust's own empty staffed bed, and every other wait passed with the own unit full.
5. Read the own unit's admissions during each full-unit wait: through every Stennock wait its unit admitted planned local surgical patients (`admission_type` 04) from its theatres, which the methodology note (section 4) makes Stennock's own care: 27 deaths.
6. Ranked the deaths in each trust's own care: Stennock 27, Prideswick 15, gap 12.
7. Repeated steps 1 to 5 from July 2023, conforming the migrated CCRS rows (times from UTC per `ccrs_migration_export_specification_rel2.3.pdf`, decision level from `ccrs_referral_levels_202307_202604.csv`, verified keys from `pas_patient_key_links_2023-2026.csv`, each patient once, contiguous bed rows as one stay, unit levels as registered on the date): 2,163 patients, 629 deaths, 148 confirmable.
8. Recommendation: place the review at Stennock University Hospitals NHS Foundation Trust.

## 4. Deliverable Answers

### external_review_placement_2027-28.docx

1. Stennock University Hospitals NHS Foundation Trust
2. 27 deaths a year of review there could confirm
3. Runner-up Prideswick Hospitals NHS Foundation Trust, at 15
4. Gap of 12 deaths

### review_placement_workings.xlsx

1. One row per trust, July 2023 to June 2026, whole patients:
   - Brackenford: 351 patients inside the remit, 104 deaths inside the remit, 5 deaths the reviewers could have confirmed
   - Ellerdyke: 140 patients, 40 deaths, 6 confirmable
   - Lathingbury: 559 patients, 165 deaths, 0 confirmable
   - Pellowham: 75 patients, 22 deaths, 3 confirmable
   - Prideswick: 221 patients, 63 deaths, 46 confirmable
   - Ristenholm: 438 patients, 126 deaths, 8 confirmable
   - Stennock: 275 patients, 80 deaths, 80 confirmable
   - Tannerby: 104 patients, 29 deaths, 0 confirmable
2. Totals: 2,163 patients inside the remit, 629 deaths inside the remit, 148 deaths the reviewers could have confirmed

### review_placement_by_trust.png

1. One bar per trust for deaths inside the remit, July 2025 to June 2026: Stennock 27, Prideswick 21, Ristenholm 44, Lathingbury 56, Brackenford 35, Ellerdyke 13, Tannerby 10, Pellowham 7
2. Confirmable part shaded within each bar: Stennock 27, Prideswick 15, Ristenholm 2, the other five trusts 0
3. Trusts ordered by the confirmable part: Stennock, Prideswick, Ristenholm, then the five trusts with none
4. Gap to the runner-up marked: 12 deaths between Stennock's 27 and Prideswick's 15
5. Title naming Stennock
