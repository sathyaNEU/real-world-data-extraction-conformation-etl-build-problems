## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (medication adherence and persistence: each primary care network's share of its older self-managing statin patients under 80 per cent of days covered in 2026).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The board should put Briskdale, Corvendale, Feldcote, Grevmoor, Krathwold and Nevgarth in the enhanced tier of the 2027-28 Statin Adherence Support Service.**
In each, 30 per cent or more of the service's population fell under 80 per cent of days covered in 2026 (lowest Briskdale at 32.1 per cent), and the closest network left out, Iversford, sits 3.0 points under the line. Not the four networks the practice lists' codes alone give (Corvendale, Feldcote, Krathwold and Nevgarth), which keep the patients whose statins a pharmacy dispensed on a compliance-aid cycle, uncoded, in the count at full cover and hold Briskdale and Grevmoor under the line.

## 2. Critical Components

1. Patients in the service's population across the twelve networks: **22,060**.
2. Patients out because their 2026 statin items ran on a compliance-aid cycle, recorded on a list or not: **2,136**.
3. Briskdale's share fallen behind is **32.1 per cent**.
4. Grevmoor's share fallen behind is **32.2 per cent**.
5. Iversford, the closest network left out, is at **27.0 per cent**.

## 3. Step-by-Step Solution

1. Carried every pre-July pseudonym in community_pharmacy_statin_dispensing_2025-12-01_to_2026-12-31.csv through pseudonym_crosswalk_2026-07-01.csv and kept the patients on quarvis_practices_lipid_cohort_2026-12-31.csv and synaris_practices_lipid_cohort_2026-12-31.xlsx born in 1961 or earlier with two or more 2026 statin items, each in the network its practice was in on 31 December 2026 (practice_network_membership_2026.csv): 24,893 patients.
2. Took out the care home residents both lists record (care_home_since; Residence Care home): 697 patients.
3. Took out every patient whose 2026 items all fall on one weekday at steps of 7 or 28 days, a pack due on a Sunday or bank holiday supplied the next opening day (compliance_aids_prescribing_and_supply_guidance_2025.pdf), which every patient quarvis_practices_lipid_cohort_2026-12-31.csv records with mds_since shows and no other patient's collections keep to: 2,136 patients, 682 of them recorded.
4. Computed each remaining patient's proportion of days covered as statin_adherence_support_service_specification_2027-28.pdf 2.2 defines it and took each network's share under 80 per cent (2.3, 3.1): six networks at 30 per cent or more.
5. For the pilot, added to services_portal_statin_pilot_export_pulled_2026-10-02.csv the payment lines in pilot_payment_statements_2025-11_to_2027-01.xlsx it lacks (consultations recorded after the pull), dropped a recovered first consultation only where the same patient, through the crosswalk, has another first consultation the federation did not recover (a hand-keyed second record), kept every other recovered record (a consultation held and claimed late), placed each consultation in the network its pharmacy was in that day (community_pharmacies_2026-12.csv relocated_on and previous_locality), and counted each patient's first consultation once by quarter, followed up if a follow-up came 1 to 41 days after it.
6. The board puts Briskdale, Corvendale, Feldcote, Grevmoor, Krathwold and Nevgarth in the enhanced tier.

## 4. Deliverable Answers

### statin_service_tiers_2027-28.docx

1. Networks in the enhanced tier: Briskdale, Corvendale, Feldcote, Grevmoor, Krathwold and Nevgarth.
2. Each network's patients in the service's population and share fallen behind in 2026, per cent to one decimal:
   - Corvendale: 2,500 patients, 35.1, enhanced
   - Feldcote: 1,686 patients, 33.6, enhanced
   - Nevgarth: 2,086 patients, 33.4, enhanced
   - Krathwold: 1,978 patients, 32.9, enhanced
   - Grevmoor: 2,094 patients, 32.2, enhanced
   - Briskdale: 1,905 patients, 32.1, enhanced
   - Iversford: 1,555 patients, 27.0, standard
   - Marlwold: 1,477 patients, 26.3, standard
   - Pellholt: 1,779 patients, 26.0, standard
   - Lathcombe: 1,669 patients, 24.9, standard
   - Tarvdale: 1,640 patients, 24.1, standard
   - Ellinholt: 1,691 patients, 23.9, standard
3. The closest network left out, Iversford, sits 3.0 percentage points under the line.
4. Bar chart of the twelve networks' shares against the 30 per cent line, the enhanced tier in blue.

### statin_adherence_2026_by_network.xlsx

5. Patients with a first consultation in the pilot, October 2025 to September 2026, by quarter:
   - Krathwold, October to December 2025: 124
   - Krathwold, January to March 2026: 88
   - Krathwold, April to June 2026: 97
   - Krathwold, July to September 2026: 72
   - Lathcombe, October to December 2025: 78
   - Lathcombe, January to March 2026: 76
   - Lathcombe, April to June 2026: 83
   - Lathcombe, July to September 2026: 74
6. Of them, followed up within six weeks:
   - Krathwold, October to December 2025: 57
   - Krathwold, January to March 2026: 49
   - Krathwold, April to June 2026: 50
   - Krathwold, July to September 2026: 33
   - Lathcombe, October to December 2025: 46
   - Lathcombe, January to March 2026: 34
   - Lathcombe, April to June 2026: 46
   - Lathcombe, July to September 2026: 34
