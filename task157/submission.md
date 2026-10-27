## Tags

**Domain:** Political science and public policy (election polling and forecasting).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Order the examination of all 540,000 signature lines filed for initiative serial I-18-2028.**
The sample projects 390,000 valid signatures, 101.3 per cent of the 384,924 required and inside the 365,678 to 404,170 band. Not 415,000, which carries the duplicate strikes at the sample's own factor of twenty as if a duplicate were a property of one signature. Not 420,000, which also re-derives the registration grounds from the snapshot taken before circulation opened.

## 2. Critical Components

1. Sampled signatures struck on a ground other than duplication: **6,277**
2. Signature lines those grounds carry in the whole petition: **125,540**
3. Sampled signatures struck as duplicates: **61**
4. Duplicate signature lines in the whole petition: **24,400**
5. Projection as a percentage of the number required: **101.3 per cent**

## 3. Step-by-Step Solution

1. Reconciled the fifteen recorders' returns in county_verification_returns_2028.csv to the sample the office records in sos_filing_and_selection_record_i18-2028.pdf: 27,000 lines, one disposition each.
2. Put Navajo County's returns on the current code set using navajo_recorder_disposition_codes_2019.txt, splitting its code 02 by the registration the recorder matched in avid_snapshot_extract_20280710.csv, then applied every query notice in county_return_corrections_2028.csv, which supersedes the disposition first returned for the line it names: 6,277 strikes on grounds other than duplication and 61 duplicate strikes.
3. Carried the grounds that belong to the one signature in front of the recorder at the sample's own factor of twenty, the 540,000 lines filed over the 27,000 sampled: 125,540 lines.
4. Carried the duplicate strikes at the chance the sample drew both lines of a pair, one in 400, because only the sampled lines were ever keyed and a duplicate could be found only where both of a signer's lines were drawn: 24,400 lines.
5. Projected valid signatures: 540,000 less 125,540 less 24,400 is 390,060, which prints 390,000 to the nearest 5,000 and is 101.3 per cent of the 384,924 required.
6. Took each sampled signature's firm from circulator_registration_extract_i18-2028.csv as the firm that had its circulator registered on the day the signature was given, since 22 circulators registered again under another firm inside the window, and read Mohave County's day-first signature dates as written: 2,332 sampled signatures for Sonoran Petition Services LLC in May 2028.
7. Rebuilt each signer's registration state on the day they signed from the registration and cancellation dates the July snapshot carries, so a registration re-established after a cancellation stands and one cancelled after the signature does not, and counted it lost only where the snapshot's status is cancelled: 487 of the signatures the recorders determined carry a registration in force when signed and cancelled now, 314 of them in Maricopa, and 488 over the sampled lines of all six months.
8. The projection sits between 365,678 and 404,170, so the office orders the examination of all 540,000 signature lines filed rather than certifying or rejecting the petition.

## 4. Deliverable Answers

### signature_projection_2028.xlsx

1. Projected valid signatures 390,000 to the nearest 5,000, 101.3 per cent of the number required; statutory outcome: examine all signature lines filed.
2. Each of the fifteen counties, how many signatures its own recorder determined, whatever code it gave, are lapsed, that is the signer's registration in force on the day signed with any cancellation of it after that day and cancelled in the 10 July 2028 snapshot:
   - Apache: 4
   - Cochise: 10
   - Coconino: 9
   - Gila: 3
   - Graham: 3
   - Greenlee: 0
   - La Paz: 2
   - Maricopa: 314
   - Mohave: 12
   - Navajo: 12
   - Pima: 57
   - Pinal: 24
   - Santa Cruz: 1
   - Yavapai: 25
   - Yuma: 11
3. Each circulator firm and month, the signatures gathered by circulators that firm had registered on the day signed and how many of those were struck on a ground other than duplication, 24 cells:
   - Sonoran Petition Services LLC, 2028-01: 685 sampled signatures, 133 struck on other grounds
   - Sonoran Petition Services LLC, 2028-02: 1,515 sampled signatures, 331 struck on other grounds
   - Sonoran Petition Services LLC, 2028-03: 2,180 sampled signatures, 516 struck on other grounds
   - Sonoran Petition Services LLC, 2028-04: 2,320 sampled signatures, 485 struck on other grounds
   - Sonoran Petition Services LLC, 2028-05: 2,332 sampled signatures, 520 struck on other grounds
   - Sonoran Petition Services LLC, 2028-06: 971 sampled signatures, 228 struck on other grounds
   - Copper State Signature Group LLC, 2028-01: 327 sampled signatures, 66 struck on other grounds
   - Copper State Signature Group LLC, 2028-02: 906 sampled signatures, 202 struck on other grounds
   - Copper State Signature Group LLC, 2028-03: 1,589 sampled signatures, 345 struck on other grounds
   - Copper State Signature Group LLC, 2028-04: 1,882 sampled signatures, 473 struck on other grounds
   - Copper State Signature Group LLC, 2028-05: 2,033 sampled signatures, 472 struck on other grounds
   - Copper State Signature Group LLC, 2028-06: 1,251 sampled signatures, 316 struck on other grounds
   - Verde Petition Operations Inc, 2028-01: 45 sampled signatures, 11 struck on other grounds
   - Verde Petition Operations Inc, 2028-02: 455 sampled signatures, 93 struck on other grounds
   - Verde Petition Operations Inc, 2028-03: 839 sampled signatures, 183 struck on other grounds
   - Verde Petition Operations Inc, 2028-04: 1,151 sampled signatures, 258 struck on other grounds
   - Verde Petition Operations Inc, 2028-05: 1,276 sampled signatures, 280 struck on other grounds
   - Verde Petition Operations Inc, 2028-06: 1,268 sampled signatures, 307 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-01: 0 sampled signatures, 0 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-02: 88 sampled signatures, 22 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-03: 467 sampled signatures, 114 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-04: 788 sampled signatures, 165 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-05: 926 sampled signatures, 232 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-06: 1,547 sampled signatures, 366 struck on other grounds
4. Each month from January to June 2028, the signatures signed in it and how many of them are lapsed:
   - 2028-01: 1,057 sampled signatures, 15 cancelled now
   - 2028-02: 2,964 sampled signatures, 59 cancelled now
   - 2028-03: 5,075 sampled signatures, 102 cancelled now
   - 2028-04: 6,141 sampled signatures, 119 cancelled now
   - 2028-05: 6,567 sampled signatures, 108 cancelled now
   - 2028-06: 5,037 sampled signatures, 85 cancelled now

### petition_disposition_2028.png

1. Bridge from the signature lines filed to the projection, with the number required and both band lines drawn and labelled, the projection bar distinguished, and the title stating that the petition goes to a full count.
