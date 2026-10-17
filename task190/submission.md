# task190 submission

## Tags

**Domain:** Banking, Credit & Financial Risk, fraud and AML detection (placing a scarce specialist review against the financial crime caseload each business line is carrying unseen).
**Analytical objective:** Anomaly Detection & Diagnostics (which lines are carrying undetected cases, against which lines are finding them).

## 1. Final Recommendation

**The specialist review should cover Business lending, FX and remittance and Trade finance in its two weeks from 15 February 2027.**

Those three are expected to be carrying the most cases that have begun and that no one at the bank has yet seen, which is what framework clause 6.2 places the review on. They are not the three lines that confirm the most cases: Retail payments, Cards and Deposits confirm 146, 108 and 68 cases in the two complete quarters and are expected to be carrying 19.2, 18.2 and 20.3, because a card or payment case is seen within a month of beginning. Trade finance confirms 24 and is expected to be carrying 38.4, its cases going 9.0 months before anyone sees them.

## 2. Critical Components

1. The closed record clause 6.3 names holds **2,890** cases, with both the month the activity began and the month anyone first saw it.
2. A case goes unseen for **0.8** months on Retail payments and **12.5** on Correspondent banking, against **9.0** on Trade finance and **6.6** on FX and remittance.
3. The three lines the review covers are expected to be carrying **46.2**, **43.0** and **38.4** cases.
4. **Private wealth** just misses, at 26.1, so the third line stands **47** per cent above the fourth.
5. Ranking the lines on the cases they confirm instead names Cards, Deposits and Retail payments, and shares no line with the placement.

## 3. Step-by-Step Solution

1. Read confirmed_case_register.csv, kept the latest version of each case, and resolved each record's line code to the line in force at the review date through line_structure_register.csv, which carries the lines merged and renamed on 1 July 2026.
2. Took one case per customer per typology as paragraph 2.3 defines it, crosswalking the case system's customer references to the alert system's through customer_id_crosswalk.csv.
3. Took the closed record of clause 6.3, the cases whose activity began between 1 January 2021 and 31 January 2024, and confirmed every one of them has a first seen month on or before the extract date.
4. For each line, took how often a case begins there and how long one goes before anyone sees it, both from that closed record, the second as clause 6.2's first seen month rather than the confirmed month.
5. Put the two together into the cases each line is expected to be carrying unseen at 15 February 2027, and checked the same figure against the closed record's own cohorts still unseen month by month.
6. Took the three highest, Business lending, FX and remittance and Trade finance, under clause 6.4's three-line capacity, with Private wealth fourth.
7. For the contract, took each quarter's hours from contractor_hours_ledger.csv counting a reissued credit note once, against the hours contract_register.pdf allows, and the tickets billed at a rate the rate card does not carry.
8. For the screening lists, took each version in force at the screening date and counted the customers who matched an entry a later version removed; for the card disputes queue, counted alerts by month on working days, excluding the re-sent June batch.

## 4. Deliverable Answers

### review_placement_2027.xlsx

1. Business lines the review covers: **Business lending, FX and remittance, Trade finance**.
2. Cases confirmed in the two complete quarters, and whether the review covers the line:
   - Retail payments: 146, no
   - Cards: 108, no
   - Deposits: 68, no
   - Business lending: 47, yes
   - FX and remittance: 48, yes
   - Trade finance: 24, yes
   - Private wealth: 12, no
   - Correspondent banking: 8, no
3. Line that just misses: **Private wealth**.

### placement_overview.png

4. One bar for each line of the cases it confirmed in the two complete quarters, the three covered lines marked: Retail payments stands highest at 146 and is not covered; the covered lines stand at 48, 47 and 24.

### Also requested

5. Contractor hours by quarter:
   - 2026-Q1: 254.7 billed, 420.0 allowed, 4 outside the rate card
   - 2026-Q2: 228.4 billed, 420.0 allowed, 4 outside the rate card
   - 2026-Q3: 226.2 billed, 480.0 allowed, 3 outside the rate card
   - 2026-Q4: 202.2 billed, 480.0 allowed, 3 outside the rate card
6. Screening list versions, the customers who matched an entry a later version removed and how many of those were cleared:
   - v1: 10, 6
   - v2: 14, 11
   - v3: 14, 12
   - v4: 7, 3
   - v5: 0, 0
7. Card disputes queue by month of 2026, alerts raised, closed inside the five working day standard, and escalated:
   - 2026-01: 133, 86, 7
   - 2026-02: 166, 129, 8
   - 2026-03: 148, 110, 4
   - 2026-04: 175, 133, 10
   - 2026-05: 123, 85, 9
   - 2026-06: 170, 124, 8
   - 2026-07: 140, 90, 5
   - 2026-08: 159, 114, 13
   - 2026-09: 140, 95, 9
   - 2026-10: 139, 102, 7
   - 2026-11: 151, 106, 8
   - 2026-12: 130, 105, 6
