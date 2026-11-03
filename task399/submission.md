## Tags

**Domain:** Criminology & Justice (sentencing and bail disparity analysis).
**Analytical objective:** Root-Cause Analysis.

## 1. Final Recommendation

**Put the duty lawyer roster forward: a second rostered duty lawyer at Kestrel Bay District Court on every sitting day.** The region's gap widened from 3.6 to 9.5 points, and the widening sits in Kestrel Bay custody-list calls made while the AVL remand list sat in courtroom 2 (gap 38.6 points, against 2.9 for the other calls). Not a judge on the custody list: outside AVL time the community magistrate's gap is 3.5 points and the judges' 2.7. Not EM bail capacity: no first appearance decides EM bail.

## 2. Critical Components

1. The region's gap is **3.6** points in the year to September 2025 and **9.5** in the year to September 2026.
2. Kestrel Bay's gap is **3.6** then **13.9** points.
3. Kestrel Bay, year to September 2026: calls made while the AVL remand list sat **38.6** points, other calls **2.9**.
4. Outside AVL time the community magistrate's gap is **3.5** points and the judges' **2.7**; while the AVL list sat, **38.9** and **35.7**.

## 3. Step-by-Step Solution

1. In cms_appearances_oct2024_sep2026.csv took the "First appearance (custody)" rows by AppearanceDate, a remand in custody where Outcome is "Remanded in custody" and no lawyer of record where CounselOfRecord is blank, per section 3 of budget2027_bid_instructions_halsey_coast.pdf: the region's gap is 3.6 then 9.5 points.
2. By Court, the widening sits at Kestrel Bay (KBY): 3.6 to 13.9 points.
3. Set each Kestrel Bay custody-list first appearance's CalledAt against that day's AVL remand list sitting in court_sitting_calendar_2024-2026.xlsx (Courtroom 2, Start to Finish), with one duty lawyer rostered at Kestrel Bay each day in the duty lawyer returns: calls made while the AVL list sat show a gap of 38.6 points, other calls 2.9.
4. By JudicialOfficer within those two groups the community magistrate and the judges match: 3.5 and 2.7 outside AVL time, 38.9 and 35.7 while it sat.
5. No first appearance in the extract carries an EM bail assessment order; every order sits on a later appearance.
6. EM turnaround per section 2 of em_bail_service_standard_v4.pdf: each order's date from its "Remanded in custody, EM bail address assessment ordered" appearance in the extract (by CRN, else surname, first name and date of birth; orders carried into em_case_system_assessments.csv joined by their addresses), its report from the first "EM address assessment report" in em_document_uploads.csv on its New Zealand date, averaged by order month.
7. Occupied nights per clause 4 of bail_support_contract_schedule2.pdf: each placement from its "Resident arrived" incident to its exit incident in bail_house_incidents.csv, less nights in custody or hospital from the incidents and approved leave from the Away sheet of bail_house_register_2025-26.xlsx, by month.
8. The duty lawyer roster is the only shortlisted line that acts on a first appearance's representation, and the widening sits in calls made while the AVL list sat next door with one duty lawyer rostered that day: put it forward.

## 4. Deliverable Answers

### remand_gap_briefing.pdf

1. The call: the duty lawyer roster, a second rostered duty lawyer at Kestrel Bay District Court on every sitting day.
2. Chart on page 1: the gap for the region and each courthouse in both years, then Kestrel Bay's year to September 2026 split into calls made while the AVL remand list sat and other calls.

### remand_gap_drill.xlsx

1. Gap by courthouse, year to September 2025 then 2026, percentage points:
   - Halsey Coast region: 3.6, 9.5
   - Kestrel Bay: 3.6, 13.9
   - Dunmore: 2.9, 0.8
   - Ashgrove: 4.4, 5.4
   - Thornmere: 3.2, 6.5
2. Kestrel Bay custody list, year to September 2026, percentage points:
   - Called while the AVL remand list sat: 38.6
   - Called at other times: 2.9
3. EM bail assessment turnaround, average days by order month: Oct 2025 9.9, Nov 2025 19.8, Dec 2025 19.4, Jan 2026 20.5, Feb 2026 20.0, Mar 2026 20.3, Apr 2026 19.2, May 2026 18.6, Jun 2026 20.1, Jul 2026 19.7, Aug 2026 19.4, Sep 2026 19.8.
4. Occupied nights at the supported bail houses by month: Oct 2025 401, Nov 2025 401, Dec 2025 410, Jan 2026 401, Feb 2026 326, Mar 2026 391, Apr 2026 362, May 2026 373, Jun 2026 368, Jul 2026 407, Aug 2026 370, Sep 2026 395.
