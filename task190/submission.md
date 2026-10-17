# task190 submission

## Tags

**Domain:** Banking, Credit & Financial Risk, fraud and AML detection (placing a scarce specialist review against the financial crime caseload each business line is carrying unseen).
**Analytical objective:** Anomaly Detection & Diagnostics (which lines are carrying undetected cases, against which lines are finding them).

## 1. Final Recommendation

**The specialist review should cover Business lending, FX and remittance and Trade finance in its two weeks from 15 February 2027.**

Those three are expected to be carrying the most cases that have begun and that no one at the bank has yet seen, which is what framework clause 6.2 places the review on. They are not the three lines that confirm the most cases: Retail payments, Cards and Deposits confirm 142, 96 and 93 cases in the two complete quarters and are expected to be carrying 20.5, 19.2 and 18.7, because a card or payment case is seen within a month of beginning. Trade finance confirms 27 and is expected to be carrying 36.9, its cases going 9.0 months before anyone sees them.

## 2. Critical Components

1. The register holds **2,935** cases whose activity began in the months of the bank's completed look-back, each with both the month the activity began and the month anyone first saw it.
2. A case goes unseen for **0.8** months on Retail payments and **12.5** on Correspondent banking, against **9.0** on Trade finance and **6.6** on FX and remittance.
3. The three lines the review covers are expected to be carrying **46.5**, **42.3** and **36.9** cases.
4. **Private wealth** just misses, at 26.2, so the third line stands **41** per cent above the fourth.
5. Ranking the lines on the cases they confirm instead names Cards, Deposits and Retail payments, and shares no line with the placement.

## 3. Step-by-Step Solution

1. Read confirmed_case_register.csv, kept the latest version of each case and the cases the head of financial crime accepted, and resolved each record's line code to the line in force at the review date through line_structure_register.csv, which carries the lines merged and renamed on 1 July 2026.
2. Took one case per customer per typology as paragraph 2.3 defines it, crosswalking the case system's customer references to the alert system's through customer_id_crosswalk.csv.
3. Clause 6.2's count holds the cases nobody has yet seen whether or not the bank holds a record of them, and the register holds no such case, so the count has to be built rather than read: took the cases whose activity began in the months clause 6.3 states the bank's look-back has closed, 1 January 2021 to 31 January 2024, and confirmed every one of them has a first seen month on or before the extract date.
4. For each line, took how often a case begins there and how long one goes before anyone sees it, both from those months, the second as clause 6.2's first seen month rather than the confirmed month, and on the handbook's count of the month ends a case is carried past.
5. Put the two together into the cases each line is expected to be carrying unseen at 15 February 2027, and checked the same figure against those cohorts' own cases still unseen month by month.
6. Took the three highest, FX and remittance, Business lending and Trade finance, under clause 6.4's three-line capacity, with Private wealth fourth.
7. For the contract, took each quarter's hours from contractor_hours_ledger.csv against the hours contract_register.pdf allows, and the tickets billed at a rate the rate card does not carry.
8. For the screening lists, took each version in force at the screening date and counted the customers who matched an entry a later version removed; for the card disputes queue, counted alerts by month against clause 7.2's standard on the days bank_closed_days.csv leaves open, excluding the re-sent June batch.

## 4. Deliverable Answers

### review_placement_2027.xlsx

1. Business lines the review covers: **Business lending, FX and remittance, Trade finance**.
2. Cases confirmed in the two complete quarters, and whether the review covers the line:
   - Retail payments: 142, no
   - Cards: 96, no
   - Deposits: 93, no
   - Business lending: 57, yes
   - FX and remittance: 50, yes
   - Trade finance: 27, yes
   - Private wealth: 12, no
   - Correspondent banking: 5, no
3. Line that just misses: **Private wealth**.

### placement_overview.png

4. One bar for each line of the cases it confirmed in the two complete quarters, the three covered lines marked: Retail payments stands highest at 142 and is not covered; the covered lines stand at 57, 50 and 27.

### Also requested

5. Contractor hours by quarter:
   - 2026-Q1: 314.4 billed, 420.0 allowed, 1 outside the rate card
   - 2026-Q2: 335.0 billed, 420.0 allowed, 2 outside the rate card
   - 2026-Q3: 348.2 billed, 480.0 allowed, 2 outside the rate card
   - 2026-Q4: 340.2 billed, 480.0 allowed, 3 outside the rate card
6. Screening list versions, the customers who matched an entry a later version removed and how many of those were cleared:
   - v1: 12, 9
   - v2: 20, 15
   - v3: 13, 7
   - v4: 4, 3
   - v5: 0, 0
7. Card disputes queue by month of 2026, alerts raised, closed inside the five working day standard, and escalated:
   - 2026-01: 146, 121, 5
   - 2026-02: 128, 107, 7
   - 2026-03: 156, 124, 14
   - 2026-04: 134, 106, 6
   - 2026-05: 169, 137, 9
   - 2026-06: 143, 116, 12
   - 2026-07: 133, 107, 6
   - 2026-08: 151, 117, 18
   - 2026-09: 136, 113, 10
   - 2026-10: 174, 141, 13
   - 2026-11: 151, 127, 8
   - 2026-12: 171, 139, 11
