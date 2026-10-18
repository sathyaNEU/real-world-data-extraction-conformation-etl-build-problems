## Tags

**Domain:** General Statistics & Data Science, exploratory data analysis and distribution assessment (member-service case queue performance).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Contribution queries takes the one process re-engineering review in the first half of 2027; its FY2026 breach share is 12.4 per cent, on the 6,480 cases it received between 1 April 2025 and 31 March 2026.**
It carried 15.0 positions-equivalents of offered load against 16 rostered positions in each quarter of FY2026, the load it has run at on those positions since FY2023, so clause 4.2 of the assurance framework reads its FY2026 share against its own quarters at that load and it stands furthest above them, under every number of matched quarters.
Not Investment switches at 29.8 per cent, the largest share answered late, whose 3.8 positions-equivalents on 4 rostered positions is the heaviest load it has carried.
Not Member data corrections at 25.8 per cent, which carried 4.7 positions-equivalents on 5 positions in FY2026 against 13.0 on 14 positions in FY2025, while the member data remediation programme ran.
Not Transfers in at 13.4 per cent, which answers a larger share late than the candidate and is the worst queue on elapsed working days before the standard's clock exclusions are applied.

## 2. Critical Components

1. Cases received in FY2026, the window 1 April 2025 to 31 March 2026, are **19,222**, with the **506** cases held in both platform extracts at the 1 April 2024 cutover counted once.
2. Cases received in FY2026 and answered later than target are **1,799** across the operation.
3. Contribution queries received **6,480** cases in FY2026 and answered **12.4** per cent of them later than its 6 working day target.
4. Contribution queries carried an offered load of **15.0** positions-equivalents against **16** rostered positions in each FY2026 quarter.

## 3. Step-by-Step Solution

1. Stacked both case extracts and resolved the 1 April 2024 platform cutover on legacy_case_ref: 82,035 distinct cases, 506 of them held in both files.
2. Converted the Orbit received_utc stamps to Irish local time before taking each case's receipt day, per clause 2.1 of member_service_standard_2025.pdf.
3. Applied the service clock of clauses 3.1, 3.3, 3.4 and 3.6 against each queue's target in clause 3.2, using public_holidays_ie_2022_2026.csv: 19,222 cases received in FY2026, 1,799 answered later than target.
4. Built each queue-quarter's offered load from the standard minutes, 420 productive minutes and the 0.88 net factor in work_measurement_standard_2022.pdf over the positions in rostered_capacity_by_queue.xlsx, converting the FY2023 and FY2024 monthly hours at the workbook's 7.0 hours a position a day.
5. Ranked the nine queues as clause 4.2 of service_assurance_framework_2026.pdf states, each queue's FY2026 share against the share the same queue reached in its FY2023 to FY2025 quarters that carried the same offered load: Contribution queries stands furthest above, first under one, two, three, four and five matched quarters.
6. Recovered the chargeable cases the FY2026 charges cover by dividing each line in scheme_charges_fy2026.csv by the per case rate for its rate period in fee_schedule_2025.pdf: 7,291 cases on 4,364 lines.
7. Took the ten largest participating schemes by FY2026 cases received, rolling the master trust's five sub-codes up to RMT-000 per data_dictionary.csv, with active members at 31 March 2026 from trustee_report_membership_2026.pdf.
8. Recommendation: commission the H1 2027 process re-engineering review on Contribution queries, at a 12.4 per cent FY2026 breach share on 6,480 cases received.

## 4. Deliverable Answers

### fy2026_service_level_replay.xlsx

1. Cases received in FY2026 and answered later than target, across the operation, whole cases: 1,799
2. Chargeable cases the scheme charging covers in each FY2026 financial quarter, whole cases:
   - FY2026 Q1: 1,593
   - FY2026 Q2: 1,967
   - FY2026 Q3: 1,920
   - FY2026 Q4: 1,811
3. The ten largest participating schemes by FY2026 cases received, with active members at 31 March 2026 and cases received per 1,000 active members to one decimal place:
   - RMT-000 Rathbroe Master Trust: 41,789 active members, 125.4 per 1,000
   - SC-001 Shanakill Industries Pension Scheme: 9,402 active members, 182.4 per 1,000
   - SC-002 Drumacool Engineering Pension Scheme: 7,101 active members, 185.6 per 1,000
   - SC-003 Kilbaylet Retail Pension Scheme: 5,904 active members, 183.1 per 1,000
   - SC-004 Monavalley Plastics Pension Scheme: 5,197 active members, 167.6 per 1,000
   - SC-005 Carrowbeg Hotels Pension Scheme: 4,598 active members, 175.3 per 1,000
   - SC-006 Tullowmore Printing Pension Scheme: 4,098 active members, 169.1 per 1,000
   - SC-007 Ardnacrusha Metals Pension Scheme: 3,698 active members, 173.6 per 1,000
   - SC-008 Rossanure Haulage Pension Scheme: 3,298 active members, 159.5 per 1,000
   - SC-009 Clonmacken Chemicals Pension Scheme: 2,993 active members, 171.4 per 1,000

### queue_review_recommendation.docx

4. Queue selected for the H1 2027 process re-engineering review: Contribution queries
5. That queue's FY2026 breach share, to one decimal place: 12.4 per cent
6. Cases that queue received in FY2026, whole cases: 6,480

### queue_breach_shares_fy2026.png

7. Bar chart of the FY2026 breach share for each of the nine member-service queues, in descending order, with Contribution queries marked as the review candidate and the share its own FY2023 to FY2025 quarters at the same offered load reached shown against each bar; the shares are those carried in the workbook's FY2026 by quarter sheet.
