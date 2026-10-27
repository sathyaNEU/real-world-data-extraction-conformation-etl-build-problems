## Tags

**Domain:** Political science and public policy (election polling and forecasting).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Order the examination of all 540,000 signature lines filed for initiative serial I-18-2028.**
The sample projects 390,000 valid signatures, 101.4 per cent of the 384,924 required and inside the 365,678 to 404,170 band. Not 415,000, which carries the duplicate strikes at the sample's own factor of twenty as if a duplicate were a property of one signature. Not 420,000, which also re-derives the registration grounds from the snapshot taken before circulation opened.

## 2. Critical Components

1. Sampled signatures struck on a ground other than duplication: **6,270**
2. Signature lines those grounds carry in the whole petition: **125,400**
3. Sampled signatures struck as duplicates: **61**
4. Duplicate signature lines in the whole petition: **24,400**
5. Projection as a percentage of the number required: **101.4 per cent**

## 3. Step-by-Step Solution

1. Reconciled the fifteen recorders' returns in county_verification_returns_2028.csv to the sample the office records in sos_filing_and_selection_record_i18-2028.pdf: 27,000 lines, one disposition each.
2. Put Navajo County's returns on the current code set using navajo_recorder_disposition_codes_2019.txt, splitting its code 02 by the registration the recorder matched in avid_snapshot_extract_20280710.csv, then applied every query notice in county_return_corrections_2028.csv, which supersedes the disposition first returned for the line it names: 6,270 strikes on grounds other than duplication and 61 duplicate strikes.
3. Carried the grounds that belong to the one signature in front of the recorder at the sample's own factor of twenty, the 540,000 lines filed over the 27,000 sampled: 125,400 lines.
4. Carried the duplicate strikes at the chance the sample drew both lines of a pair, one in 400, because only the sampled lines were ever keyed and a duplicate could be found only where both of a signer's lines were drawn: 24,400 lines.
5. Projected valid signatures: 540,000 less 125,400 less 24,400 is 390,200, which prints 390,000 to the nearest 5,000 and is 101.4 per cent of the 384,924 required.
6. Took each sampled signature's firm from circulator_registration_extract_i18-2028.csv as the firm that had its circulator registered on the day the signature was given, since 22 circulators registered again under another firm inside the window, and read Mohave County's day-first signature dates as written: 2,350 sampled signatures for Sonoran Petition Services LLC in May 2028.
7. Rebuilt each signer's registration state on the day they signed from the registration and cancellation dates the July snapshot carries, so a registration re-established after a cancellation stands and one cancelled after the signature does not, and counted it lost only where the snapshot's status is cancelled: 558 of the signatures the recorders determined were registered when signed and are no longer valid, 356 of them in Maricopa.
8. The projection sits between 365,678 and 404,170, so the office orders the examination of all 540,000 signature lines filed rather than certifying or rejecting the petition.

## 4. Deliverable Answers

### signature_projection_2028.xlsx

1. Projected valid signatures 390,000 to the nearest 5,000, 101.4 per cent of the number required; statutory outcome: examine all signature lines filed.
2. Each county, the sampled signatures its recorder returned a determination for and how many of those were registered when they signed and are no longer shown as valid, 15 counties:
   - Apache: 243 signatures determined, 5 no longer valid
   - Cochise: 503 signatures determined, 7 no longer valid
   - Coconino: 544 signatures determined, 6 no longer valid
   - Gila: 223 signatures determined, 2 no longer valid
   - Graham: 124 signatures determined, 5 no longer valid
   - Greenlee: 41 signatures determined, 3 no longer valid
   - La Paz: 81 signatures determined, 3 no longer valid
   - Maricopa: 16,714 signatures determined, 356 no longer valid
   - Mohave: 820 signatures determined, 10 no longer valid
   - Navajo: 357 signatures determined, 8 no longer valid
   - Pima: 3,966 signatures determined, 80 no longer valid
   - Pinal: 1,441 signatures determined, 22 no longer valid
   - Santa Cruz: 162 signatures determined, 3 no longer valid
   - Yavapai: 1,070 signatures determined, 30 no longer valid
   - Yuma: 529 signatures determined, 18 no longer valid
3. Each circulator firm and month, the sampled signatures gathered by circulators that firm had registered on the day they were given and how many of those were struck on a ground other than duplication, 24 cells:
   - Sonoran Petition Services LLC, 2028-01: 733 sampled signatures, 157 struck on other grounds
   - Sonoran Petition Services LLC, 2028-02: 1,519 sampled signatures, 332 struck on other grounds
   - Sonoran Petition Services LLC, 2028-03: 2,246 sampled signatures, 507 struck on other grounds
   - Sonoran Petition Services LLC, 2028-04: 2,310 sampled signatures, 514 struck on other grounds
   - Sonoran Petition Services LLC, 2028-05: 2,350 sampled signatures, 561 struck on other grounds
   - Sonoran Petition Services LLC, 2028-06: 1,042 sampled signatures, 233 struck on other grounds
   - Copper State Signature Group LLC, 2028-01: 264 sampled signatures, 61 struck on other grounds
   - Copper State Signature Group LLC, 2028-02: 830 sampled signatures, 189 struck on other grounds
   - Copper State Signature Group LLC, 2028-03: 1,544 sampled signatures, 366 struck on other grounds
   - Copper State Signature Group LLC, 2028-04: 1,789 sampled signatures, 392 struck on other grounds
   - Copper State Signature Group LLC, 2028-05: 1,715 sampled signatures, 424 struck on other grounds
   - Copper State Signature Group LLC, 2028-06: 991 sampled signatures, 225 struck on other grounds
   - Verde Petition Operations Inc, 2028-01: 45 sampled signatures, 8 struck on other grounds
   - Verde Petition Operations Inc, 2028-02: 474 sampled signatures, 90 struck on other grounds
   - Verde Petition Operations Inc, 2028-03: 938 sampled signatures, 219 struck on other grounds
   - Verde Petition Operations Inc, 2028-04: 1,281 sampled signatures, 288 struck on other grounds
   - Verde Petition Operations Inc, 2028-05: 1,555 sampled signatures, 342 struck on other grounds
   - Verde Petition Operations Inc, 2028-06: 1,504 sampled signatures, 333 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-01: 0 sampled signatures, 0 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-02: 79 sampled signatures, 17 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-03: 423 sampled signatures, 87 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-04: 705 sampled signatures, 169 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-05: 933 sampled signatures, 230 struck on other grounds
   - Mesquite Civic Outreach LLC, 2028-06: 1,571 sampled signatures, 367 struck on other grounds
4. Each month of the circulation period, the sampled signatures signed in it and the petition sheet serials they sit on, 6 months:
   - 2028-01: 1,042 sampled signatures on 776 sheet serials
   - 2028-02: 2,902 sampled signatures on 2,125 sheet serials
   - 2028-03: 5,151 sampled signatures on 3,841 sheet serials
   - 2028-04: 6,085 sampled signatures on 4,482 sheet serials
   - 2028-05: 6,553 sampled signatures on 4,846 sheet serials
   - 2028-06: 5,108 sampled signatures on 3,737 sheet serials

### petition_disposition_2028.png

1. Bridge from the signature lines filed to the projection, with the number required and both band lines drawn and labelled, the projection bar distinguished, and the title stating that the petition goes to a full count.
