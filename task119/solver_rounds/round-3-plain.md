# solver round: round 3, plain

**Proxy score 72.6 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 30.6 of 58). Main call LANDED. 3 of 11 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the 2027-28 external review at Stennock University Hospitals NHS Foundation Trust, where a year of review could confirm 27 deaths.

solver: Put the 2027-28 external review in Stennock University Hospital (STN). In the placement year, July 2025 to June 2026, 27 deaths there could be confirmed as avoidable because of the trust's own care: all 27 of Stennock's deaths inside the remit happened while Stennock gave freed beds to its own planned post-operative (recovery) patients. Prideswick (PRW) comes next with 15, all waits where an open bed sat empty under its weekend rule, so the gap is 12 deaths. Lathingbury (LAT) has the most deaths inside the remit (56), which is Norman Scott's test, but none of them can be confirmed: Lathingbury has no level 3 unit and its patients waited for beds that the network bed bureau allocates.

tokens matched 4 of 5 (28, 27, Place, Stennock University Hospitals NHS Foundation, Trust)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| external_review_placement_2027-28.docx | 1 | 1 | 2 | 50% |
| external_review_placement_2027-28.docx | 2 | 1 | 1 | 100% |
| external_review_placement_2027-28.docx | 3 | 1 | 3 | 33% |
| external_review_placement_2027-28.docx | 4 | 1 | 1 | 100% |
| review_placement_workings.xlsx | 1 | 6 | 32 | 19% |
| review_placement_workings.xlsx | 2 | 0 | 4 | 0% |
| review_placement_by_trust.png | 1 | 2 | 11 | 18% |
| review_placement_by_trust.png | 2 | 2 | 4 | 50% |
| review_placement_by_trust.png | 3 | 2 | 4 | 50% |
| review_placement_by_trust.png | 4 | 3 | 5 | 60% |
| review_placement_by_trust.png | 5 | 2 | 2 | 100% |

## Solver's path

1. Calibrated the rule on nrr_review_records.sqlite against the reviews log nrr_escalation_reviews_closed_2021-2025.xlsx. Deaths in remit (level decided 3, decision to admit to bed assignment or death over 4h, death within 30 days of the decision date, inclusive) equal the confirmed deaths in all 34 reviews. Every one of those waits had an open, empty bed in the unit. The NRR screen (waits over 4h from receipt) does not predict confirmations: Ormerleby and Selarwell have identical screen figures but confirmed 24 and 11.
2. Cleaned critical_care_referrals_202307_202606.csv. Dropped 281 CCRS pilot-period duplicates (same patient as a platform record, 19 Feb to 29 Mar 2024). Converted CCRS times from UTC to Europe/London, checked against the transfer audit decision times (0 minute difference). Took the CCRS level from the DECISION entry in ccrs_referral_levels; the 92 LEVEL CHANGE entries are post-admission step-downs. Mapped temporary patient keys to verified keys with pas_patient_key_links.
3. Wait end: the platform outcome_at (bed assigned) for platform records. For inter-trust transfers, bed_confirmed_at from interhospital_transfer_audit (all 3,797 matched on verified key and decision time). For CCRS-era local admissions, the first unit-feed row joined on referral_id. Stood-down referrals never wait more than 4h. Referrals from theatre recovery (REC) are outside scope and have no level 3 waits over 4h. CCU is treated as a ward, since no remit patient was in a registered critical care unit at the decision to admit.
4. Deaths: date_of_death from the APC extract on the verified key, falling back to the discharge date where discharge_method = 4. This recovers deaths on 10 unlinked temporary keys, all before the placement year. Remit across the whole record: 2,206 referrals and 660 deaths, which are 2,183 and 646 distinct people.
5. Placement period: the latest four complete quarters, decisions to admit from 1 Jul 2025 to 30 Jun 2026. The 30-day deaths are complete by the 14 Aug 2026 extract because registrations arrive within 14 days. Deaths in remit: LAT 56, RIS 44, BRK 35, STN 27, PRW 21, ELL 13, TAN 10, PEL 7 (213).
6. Confirmable test against each trust's own level 3 unit (acc_unit_stays plus bed returns; the feed matches the 08:00 returns exactly). A death counts if, during the wait, an open bed sat empty, or a freed bed went to a patient the trust itself chose: its own planned surgical or recovery admissions, or later own-trust patients. Beds the network bureau allocated to transfers from other trusts do not count. For CCRS-era transfers, the bed is taken as occupied from bed_confirmed_at, which removes reserved-bed gaps that look free in the feed.
7. Placement-year result: STN 27 of 27 (in every wait, own recovery patients with later decisions were admitted first). PRW 15 of 21 (an empty bed for about 5 hours; 13 weekends and 2 bank-holiday Mondays). RIS 2 of 44 (35 of its waits overlapped bureau transfers in). BRK 0 of 35 (6 overlapped bureau transfers; no empty bed during any wait). LAT, ELL, TAN and PEL 0, as they have no own level 3 unit in the year. Whole-record confirmable: STN 84, PRW 46, RIS 8, ELL 8, BRK 5, PEL 5, LAT 0, TAN 0 (156).
8. Decision: STN 27 against runner-up PRW 15, a gap of 12. Rejected Norman Scott's test (LAT, 56 deaths in remit) and the NRR and capacity-report screen (waits from receipt) because neither measures deaths the reviewers can confirm.

confidence: Medium-high on the main call: STN leads PRW 27 to 15 under every variant tested (free bed only, own-bed use, with or without CCU). Medium on the whole-record workings figures: they depend on choosing distinct people over referrals, on treating CCU as a ward, and on CCRS-era local waits being measured to bed placement, because that system recorded no bed-assignment time.

notes: CCRS-era local admissions carry only the time the patient was placed in the bed, not the time the bed was assigned, so those waits run slightly long; this does not touch the placement year. Workings figures count distinct people (2183 / 646 / 156); counting referrals gives 2206 / 660 / 156. Treating CCU as a critical care unit would remove 4 BRK and 3 RIS placement-year remit deaths but changes no confirmable figure.

### external_review_placement_2027-28.docx (solver's answers)
- trust the review should sit in: Stennock University Hospital (STN)
- deaths a year of review there could confirm: 27 deaths (placement year, decisions to admit 1 Jul 2025 to 30 Jun 2026)
- trust that comes closest: Prideswick County Hospital (PRW), 15 confirmable deaths
- gap between the two: 12 deaths (27 - 15)

### review_placement_workings.xlsx (solver's answers)
- patients inside the remit, whole record Jul 2023 to Jun 2026 (distinct people): BRK 353; ELL 143; LAT 561; PEL 78; PRW 223; RIS 440; STN 279; TAN 106; Total 2183 (counting referrals instead gives 2206)
- deaths inside the remit, whole record (distinct people): BRK 106; ELL 42; LAT 167; PEL 25; PRW 65; RIS 128; STN 84; TAN 29; Total 646 (counting referrals instead gives 660)
- deaths reviewers could have confirmed, whole record: BRK 5; ELL 8; LAT 0; PEL 5; PRW 46; RIS 8; STN 84; TAN 0; Total 156

### review_placement_by_trust.png (solver's answers)
- deaths inside the remit per trust, placement year Jul 2025 to Jun 2026: LAT 56; RIS 44; BRK 35; STN 27; PRW 21; ELL 13; TAN 10; PEL 7; Total 213
- confirmable part per trust (shaded) and bar order: STN 27; PRW 15; RIS 2; BRK 0; LAT 0; ELL 0; TAN 0; PEL 0 (Total 44); bars ordered STN, PRW, RIS, then the zero trusts
- gap to runner-up marked: 12 deaths, STN 27 against PRW 15
- title: Names Stennock University Hospital as the trust for the review
