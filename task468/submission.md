## Tags

**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics: a Medicaid plan's hospital pay-for-performance measure conformed from its claims, a delegated group's encounters and the state's death record linkage, the linked deaths corrected for the linkage's own errors).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Five of Halbrook's 14 network hospitals lose the 2027 Hospital Quality Bonus: Brannock Medical Center, Calloway Memorial Hospital, Mercy Valley Medical Center, Northgate Community Hospital and Westover Regional Hospital. The other nine keep it.**
Their fiscal 2026 mortality ratios run from 1.25 to 1.55 against the 1.15 line; the highest ratio among the hospitals that keep it is Fairhaven Community Hospital's 1.09. Not the four hospitals that the deaths on the bills and the Office of Vital Records' links give, even with every link a later claim contradicts dropped and every death a later bill records added (Calloway, Northgate, Varden and Westover), because for members enrolled without a Social Security number the linkage links living members with common names to other people's deaths and misses the deaths of members with two-part surnames, and those repairs reach only the members whose later claims happen to show it: corrected at the error rates the record's recorded deaths and living members measure, Varden keeps the bonus and Brannock and Mercy Valley lose it.

## 2. Critical Components

1. The linkage's error rates by identifier class, measured on the index admissions whose deaths the bills record and on the members seen alive after day 30: Social Security number on file, **829 of 836** recorded deaths linked and **12 of 21,855** living members linked; no number, single surname, **44 of 48** recorded deaths linked and **20 of 1,179** living members linked; no number, two-part surname, **78 of 162** recorded deaths linked and **8 of 1,554** living members linked.
2. The hospitals that lose the bonus, deaths over expected deaths: Brannock Medical Center **84.9** over **67.9**, ratio **1.25**; Calloway Memorial Hospital **190.6** over **143.8**, ratio **1.33**; Mercy Valley Medical Center **502.2** over **387.1**, ratio **1.30**; Northgate Community Hospital **189.3** over **122.2**, ratio **1.55**; Westover Regional Hospital **260.3** over **179.9**, ratio **1.45**.
3. Varden Surgical Hospital, which the uncorrected links put over the line: **26.4** deaths over **25.6** expected, ratio **1.03**.

## 3. Step-by-Step Solution

1. Conformed hchp_ip_claims_extract_2026-10-05.csv and CMG_HCHP_IP_ENC_20261006.txt into stays, each as last corrected with voided and deleted bills dropped, Carrisford member numbers mapped through hchp_member_enrollment_extract_2026-10-05.csv and both of Mercy Valley's NPIs through hchp_network_hospitals_2026.csv.
2. Kept the index admissions of specification 2.1 to 2.4 (34,500 in all): adults, no delivery DRGs, no patient status 07, each member's first, a transfer joined to the first hospital's stay.
3. Summed each hospital's HIMM 3.2 scores from HIMM_3.2_scores_FY2026_admissions.xlsx, keyed by member, admission date and NPI.
4. Counted the deaths the bills record (patient status 20 on the stay, its transfer stay or a later stay ending within the 30 days) and joined OVR_HCHP_FY2026_DEATH_LINKAGE_RETURN.csv on member and admission date.
5. Classed each member by hchp_member_enrollment_extract_2026-10-05.csv (Social Security number on file; otherwise single or two-part surname) and measured each class's share of recorded deaths linked and share of members with a service line in hchp_member_service_lines_2025-01_2026-09.csv, an admission or a live discharge after day 30 linked.
6. For each hospital and class, estimated the deaths among the admissions neither recorded dead nor seen alive after day 30 as (links less the false-link share times the admissions) over (the share linked less the false-link share), and added the recorded deaths.
7. Divided each hospital's deaths by its expected deaths and marked the hospitals over 1.15 (specification 5.2).
8. Took 2 per cent of each hospital's Halbrook payments for stays discharged in fiscal 2026 (Carrisford's out): each stay its original plus a CPS replacement's change or a platform replacement's full amount, a voided bill nothing, plus each additional payment in HCHP_Provider_Dispute_Log_IP_2026-10-01.xlsx made by September 30 on those stays, except one the disputed claim's replacement bill paid that day already carries: the replacement's change to the stay's payment (a CPS replacement's amount, or a platform replacement's amount less the original's) equals the additional payment.

## 4. Deliverable Answers

### halbrook_2027_hospital_quality_bonus.xlsx

1. Hospitals that lose the 2027 bonus: **5**: Brannock Medical Center, Calloway Memorial Hospital, Mercy Valley Medical Center, Northgate Community Hospital and Westover Regional Hospital.
2. Each hospital, 2027 bonus and bonus at stake (2 per cent of fiscal 2026 inpatient payments, nearest $100):
   - Saint Brendan Medical Center: keeps, $791,900
   - Westover Regional Hospital: loses, $816,700
   - Calloway Memorial Hospital: loses, $477,100
   - Varden Surgical Hospital: keeps, $833,800
   - Mercy Valley Medical Center: loses, $579,700
   - Northgate Community Hospital: loses, $559,500
   - Tamsin General Hospital: keeps, $389,500
   - Pinecrest Hospital: keeps, $412,200
   - Brannock Medical Center: loses, $391,800
   - Lakeshore Hospital: keeps, $366,900
   - Corbel Falls Hospital: keeps, $314,400
   - Quayside Hospital: keeps, $599,300
   - Marlow Ridge Medical Center: keeps, $293,100
   - Fairhaven Community Hospital: keeps, $247,400
3. Total bonus at stake across the network: $7,073,300.
4. Bar chart of the 14 hospitals' fiscal 2026 mortality ratios against the 1.15 line, the five that lose the bonus highlighted.
