# task446 submission

## Tags

**Domain:** Banking, Credit & Financial Risk (obligor-group credit concentration and house-limit monitoring).
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).
**Axis 2:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Credit committee should approve GBP 21.8m of Kelderby Facilities Ltd's GBP 30.0m term loan.**

Kelderby's projected 31 December 2026 exposure is GBP 148.1m against its GBP 170.0m house limit. Not GBP 15.0m, which builds each past quarter on the group as it stood then, so the Tarrant Hydraulics purchase reads as growth. Not the full GBP 30.0m, which would take Kelderby over its limit.

## 2. Critical Components

1. At 30 September 2026 the Kelderby group includes Tarrant Hydraulics Ltd and no longer includes Norbeck Coatings Ltd
2. Kelderby's quarter-end exposures on that membership are **139.4, 141.5, 140.4, 144.5, 146.4** (GBP m, 30 Sep 2025 to 30 Sep 2026)
3. Kelderby's projected 31 December 2026 exposure is **GBP 148.1m**, utilisation **87.1%** of the GBP 170.0m limit
4. The approvable term loan is **GBP 21.8m**

## 3. Step-by-Step Solution

1. Took the six Part B requests and borrower LEIs from credit_committee_agenda_20261104.docx and each group's limit from house_limit_register_20260930.xlsx.
2. Resolved every LEI to its Obligor Group on the 30 September 2026 GLEIF archive under Policy section 2 (consolidation chains, branches to head office, managed funds alone, lapsed records kept, merged LEIs to successors): Tarrant Hydraulics is Kelderby's, Norbeck Coatings is Meridale's.
3. Measured each quarter-end's exposure under Policy section 3 from the loan extracts (the late Dublin file included, migrated facilities once), the treasury positions (ISIN file for blank issuer LEIs), the R2 rerun for the 30 Sep 2026 netting sets in GBP thousands less cash CSA collateral, all converted at Treasury rates.
4. Assigned all five quarter-ends to the groups as constituted at 30 September 2026 (LMS-03 2.3): Kelderby runs 139.4, 141.5, 140.4, 144.5, 146.4.
5. Projected 31 December 2026 as the 30 September exposure plus the least-squares slope (LMS-03 2.2): Kelderby GBP 148.1m, 87.1% of GBP 170.0m.
6. Applied LMS-03 3.1 and 3.2 (term 100%, revolver 50%, GBP 0.1m steps, capped at the request) to every request.
7. Recommendation: approve GBP 21.8m of Kelderby's GBP 30.0m term loan.

## 4. Deliverable Answers

### limit_check_2026-11-04.xlsx
1. Kelderby: approve GBP 21.8m of the GBP 30.0m term loan
2. One row per request, highest projected utilisation first, GBP m to one decimal:
   - B4 Corrin Freight Ltd (Corrin Logistics Group plc): drawn loans 73.5, undrawn commitments 8.0, securities 0.0, derivatives 1.5; quarter-end exposures 30 Sep 2025 88.1, 31 Dec 2025 87.4, 31 Mar 2026 86.0, 30 Jun 2026 83.2, 30 Sep 2026 83.1; projected 31 Dec 2026 81.6; utilisation 90.7%; approvable 16.7 of 25.0 requested
   - B5 Pellow Distribution Ltd (Pellow Foods Group plc): drawn loans 59.6, undrawn commitments 5.7, securities 9.8, derivatives 0.0; quarter-end exposures 30 Sep 2025 77.4, 31 Dec 2025 77.3, 31 Mar 2026 74.7, 30 Jun 2026 75.5, 30 Sep 2026 75.1; projected 31 Dec 2026 74.4; utilisation 87.6%; approvable 10.5 of 14.0 requested
   - B1 Kelderby Facilities Ltd (Kelderby Group plc): drawn loans 128.2, undrawn commitments 18.2, securities 0.0, derivatives 0.0; quarter-end exposures 30 Sep 2025 139.4, 31 Dec 2025 141.5, 31 Mar 2026 140.4, 30 Jun 2026 144.5, 30 Sep 2026 146.4; projected 31 Dec 2026 148.1; utilisation 87.1%; approvable 21.8 of 30.0 requested
   - B2 Meridale Packaging Ltd (Meridale Holdings Ltd): drawn loans 68.3, undrawn commitments 6.3, securities 0.0, derivatives 0.0; quarter-end exposures 30 Sep 2025 78.0, 31 Dec 2025 77.6, 31 Mar 2026 75.3, 30 Jun 2026 75.4, 30 Sep 2026 74.6; projected 31 Dec 2026 73.7; utilisation 86.7%; approvable 11.2 of 12.0 requested
   - B3 Brauneck Antriebstechnik AG (Brauneck Holding SE): drawn loans 78.5, undrawn commitments 4.6, securities 0.0, derivatives 0.0; quarter-end exposures 30 Sep 2025 80.2, 31 Dec 2025 81.3, 31 Mar 2026 79.2, 30 Jun 2026 81.5, 30 Sep 2026 83.1; projected 31 Dec 2026 83.7; utilisation 83.7%; approvable 16.2 of 20.0 requested
   - B6 Stannard Capital Management Ltd (Stannard Capital Group plc): drawn loans 17.4, undrawn commitments 2.8, securities 0.0, derivatives 1.3; quarter-end exposures 30 Sep 2025 21.6, 31 Dec 2025 21.0, 31 Mar 2026 20.5, 30 Jun 2026 21.0, 30 Sep 2026 21.5; projected 31 Dec 2026 21.5; utilisation 71.6%; approvable 17.0 of 20.0 requested

### projected_utilisation_2026Q4.png
1. Horizontal bars of projected utilisation per group in the workbook's order (Corrin 90.7%, Pellow 87.6%, Kelderby 87.1%, Meridale 86.7%, Brauneck 83.7%, Stannard 71.6%), the house limit line marked at 100%, Kelderby's bar annotated "Approve GBP 21.8m of GBP 30.0m", titled "Kelderby can take GBP 21.8m of its GBP 30.0m term loan".
