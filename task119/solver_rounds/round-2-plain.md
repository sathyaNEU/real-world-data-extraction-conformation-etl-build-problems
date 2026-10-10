# solver round: round 2, plain

**Proxy score 82.3 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 40.3 of 58). Main call LANDED. 4 of 11 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the 2027-28 external review at Stennock University Hospitals NHS Foundation Trust, where a year of review could confirm 27 deaths.

solver: Place the 2027-28 external review in Stennock (STN). Over the placement period, July 2025 to June 2026, the reviewers could confirm 27 deaths there. Prideswick (PRW) comes next with 15, a gap of 12. Lathingbury (LAT) has the most remit deaths (56), which is the measure the chair would use, but it has no level 3 unit of its own, so none of those deaths can be confirmed against its own care.

tokens matched 3 of 5 (28, 27, Place, Stennock University Hospitals NHS Foundation, Trust)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| external_review_placement_2027-28.docx | 1 | 1 | 2 | 50% |
| external_review_placement_2027-28.docx | 2 | 1 | 1 | 100% |
| external_review_placement_2027-28.docx | 3 | 1 | 3 | 33% |
| external_review_placement_2027-28.docx | 4 | 1 | 1 | 100% |
| review_placement_workings.xlsx | 1 | 22 | 32 | 69% |
| review_placement_workings.xlsx | 2 | 4 | 4 | 100% |
| review_placement_by_trust.png | 1 | 3 | 11 | 27% |
| review_placement_by_trust.png | 2 | 3 | 4 | 75% |
| review_placement_by_trust.png | 3 | 2 | 4 | 50% |
| review_placement_by_trust.png | 4 | 3 | 5 | 60% |
| review_placement_by_trust.png | 5 | 2 | 2 | 100% |

## Solver's path

1. Calibration: tested the National Rapid Review Programme database (nrr_review_records.sqlite) against the confirmed counts in nrr_escalation_reviews_closed_2021-2025.xlsx. Level 3 by decided level, wait from decision to admit to bed assignment (or to death before admission) over 4h, and death within 30 days of the decision to admit reproduces 'Deaths confirmed avoidable' exactly in all 34 reviews. Requested level, waits from receipt and waits to arrival all fail. Every confirmed death in that database had a free bed in its own unit.
2. Referral record (critical_care_referrals csv, 30,785 rows): dropped 295 platform rows from the pilot period (19 Feb-1 Apr 2024) that duplicate a CCRS referral (same patient, decision time within 60 min). The bed stay carries the CCRS number. Converted CCRS received, decision and outcome times from UTC to local time; the transfer audit's decision times confirm the 0/60-min offset.
3. For level 3 on CCRS rows, used the DECISION entry in ccrs_referral_levels; 160 requested-3/decided-2 rows are out, and 60 LEVEL CHANGE entries are post-admission step-downs. Bed time for CCRS admissions comes from the unit stay row carrying the referral id. For platform admissions, outcome_at matches stay admitted_at and the transfer audit's bed_confirmed_at.
4. Measured waits in absolute (UTC) time. 20 waits spanning the spring clock change (31 Mar 2024 and 30 Mar 2025) look over 4h on the wall clock but are under 4h in real time, so they are out.
5. Deaths: took date_of_death from the APC episode extract on the verified key. Mapped temporary U-keys through pas_patient_key_links, which recovers 25 deaths. For 4 unlinked died-before-admission rows, used the outcome date. 30-day window = death date minus decision date of 0-30 days; no case sits on the boundary.
6. Remit = level 3, wait over 4h, died within 30 days, counted by referring trust; transfers stay with the referring trust. Counted distinct patients: 14 patients had two qualifying referrals each, all in Jul 2024-Jun 2025, so the remit deaths there fall from 226 to 212. CCU and SDU were treated as wards, since their stays show source location 06 (ward).
7. Confirmable = remit death where the trust's own level 3 unit (RIS, BRK, STN and PRW throughout; ELL-ACC to 31 Mar 2024; PEL-W3 4 Dec 2023-31 Mar 2024) either had a free bed during the wait or gave a bed to a planned local admission (type 04) during the wait. Rule base: the terms of reference's own-care test and methodology note, plus the calibration. Beds taken by inter-hospital transfers in (type 02) were excluded, because the network bed bureau allocates them and every such patient's decision to admit came before the waiting patient's. Trusts with no level 3 unit (LAT, TAN, PEL, and ELL from Apr 2024) get 0.
8. Placement period = latest four complete quarters, decisions to admit Jul 2025-Jun 2026. Remit deaths: LAT 56, RIS 44, BRK 35, STN 27, PRW 21, ELL 13, TAN 10, PEL 7 (213). Confirmable: STN 27 (all with planned surgical admissions taking beds), PRW 15 (free beds, mostly at weekends, under the consultant-on-site rule), RIS 2, all others 0 (44). STN leads PRW by 12.
9. Whole record Jul 2023-Jun 2026 for the workbook: 2,163 patients, 629 remit deaths, 148 confirmable.

confidence: Medium-high. The remit rule matches the calibration exactly, and STN leads in every year. The main judgement is excluding beds that transfers in took at RIS: counting them would put RIS at about 37 and make it the pick. I excluded them because the network bureau allocated those beds and the transferred patients had been referred earlier.

notes: The children and maternity exclusions could not be applied: no field in the folder identifies them, and no ward code marks a critical care unit. The confirmable rule (a free bed or a planned admission during the wait) is inferred from the terms of reference and the calibration. Counting Prideswick's full-unit weekend waits would raise PRW to 18 and narrow the gap to 9; STN stays first either way.

### external_review_placement_2027-28.docx (solver's answers)
- trust the review should sit in: Stennock (STN)
- deaths a year of review there could confirm: 27 deaths (Jul 2025-Jun 2026)
- trust that comes closest: Prideswick (PRW), 15 confirmable deaths
- gap between the two in deaths: 12 deaths

### review_placement_workings.xlsx (solver's answers)
- per trust, whole record Jul 2023-Jun 2026: patients in remit (level 3 decided, wait from decision to admit to bed over 4h) / remit deaths (died within 30 days) / confirmable deaths: BRK 351 / 104 / 5; ELL 140 / 40 / 6; LAT 559 / 165 / 0; PEL 75 / 22 / 3; PRW 221 / 63 / 46; RIS 438 / 126 / 8; STN 275 / 80 / 80; TAN 104 / 29 / 0
- column totals: Patients 2,163; remit deaths 629; confirmable deaths 148

### review_placement_by_trust.png (solver's answers)
- bars per trust, Jul 2025-Jun 2026: remit deaths (confirmable part shaded): STN 27 (27); PRW 21 (15); RIS 44 (2); BRK 35 (0); LAT 56 (0); ELL 13 (0); TAN 10 (0); PEL 7 (0); total 213 (44)
- order and gap marked: Ordered by confirmable deaths: STN 27, PRW 15, RIS 2, then the rest at 0. Gap to runner-up: 12 deaths (STN 27 vs PRW 15)
- title naming the trust: Stennock: 27 deaths a year the review could confirm, 12 more than Prideswick
