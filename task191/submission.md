## Tags

> **Domain:** Banking, credit and financial risk, fraud and AML detection.
> **Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Put CRY-OFF, CSH-VEL, DRM-REA and PRF-DEV into the 2027 tuning, and no other scenario.**
Each is below the 3 per cent productivity floor over the twelve months to 30 September 2026 with every alert counted by how it will end. Not RMF-P2P, MUL-INF and MER-RND: their SARs so far are under 3 per cent of their decided alerts, but their investigations run longest, and the alerts still open on 2 November are mostly SARs to come.

## 2. Critical Components

1. Read over the alerts already decided, RMF-P2P, MUL-INF and MER-RND fall below the floor as well as CRY-OFF, CSH-VEL, DRM-REA and PRF-DEV.
2. On 2 November RMF-P2P, MUL-INF and MER-RND had 91, 127 and 82 alerts from the year still under investigation.
3. In those scenarios an alert ending in a SAR is decided months after it is raised, while one closed without a SAR is closed within weeks, so an alert still undecided is far more likely than the scenario's average to end in a SAR.
4. Counted by how they will end, RMF-P2P, MUL-INF and MER-RND clear the floor and CRY-OFF, CSH-VEL, DRM-REA and PRF-DEV stay below it.

## 3. Step-by-Step Solution

1. Dated each alert in tm_alerts_2025-07_2026-10.csv by the business date of its run in tm_monitoring_runs_2025-07_2026-10.csv, left out the copies closed as duplicates and read XB-HRJ2 with XB-HRJ.
2. Carried each escalated alert to its investigation in fcm_cases_export_2026-11-02.json: it ends in a SAR when the investigation's disposition is SAR filed; an alert still in triage or in an open investigation is undecided.
3. For each scenario, read its alerts raised at least 330 days before the extract whose outcome is in: those that ended in a SAR were decided months after the alert, those that did not within weeks.
4. Counted each undecided alert at the share of those older alerts of its scenario, still undecided at the same age, that ended in a SAR, and divided the SARs and expected SARs by the scenario's alerts in the year.
5. Sent the scenarios below 3 per cent to the 2027 tuning.
6. Investigations by quarter: each investigation in the export opened from 1 October 2025 to 30 September 2026 (Eastern date), counted once for the scenario of the alert whose escalation opened it (the alert whose triage closed at the investigation's opening).
7. SARs by month: each filing in sar_filings_2025-07_2026-10.csv by its Eastern filing date, read along its investigation's filings in date order: the first is the initial report, a later one covering activity after the previous report is a continuing activity report whether or not its prior report field is filled, and one covering the same activity as the report it cites is a correction, left out.
8. Recommended CRY-OFF, CSH-VEL, DRM-REA and PRF-DEV for the 2027 tuning.

## 4. Deliverable Answers

### tuning_scenarios_2027.docx

1. Scenarios going into the 2027 tuning: CRY-OFF, CSH-VEL, DRM-REA and PRF-DEV.
2. Scenarios staying out: ATM-WDL, CHB-ABU, CSH-LDS, ELD-EXP, FAN-OUT, GMB-SPL, MER-RND, MUL-INF, RMF-P2P and XB-HRJ (with XB-HRJ2).
3. Chart: each scenario's estimated productivity against the 3 per cent floor, CRY-OFF, CSH-VEL, DRM-REA and PRF-DEV in red, the only bars under the line.

### tm_alert_figures_2026.xlsx

4. Investigations each scenario's alerts opened, by quarter, whole numbers:
   - CSH-LDS: 2025 Q4 426, 2026 Q1 399, 2026 Q2 404, 2026 Q3 401
   - CSH-VEL: 2025 Q4 163, 2026 Q1 143, 2026 Q2 148, 2026 Q3 144
   - XB-HRJ (with XB-HRJ2): 2025 Q4 118, 2026 Q1 153, 2026 Q2 146, 2026 Q3 133
   - RMF-P2P: 2025 Q4 322, 2026 Q1 304, 2026 Q2 292, 2026 Q3 311
   - MUL-INF: 2025 Q4 391, 2026 Q1 366, 2026 Q2 345, 2026 Q3 391
   - FAN-OUT: 2025 Q4 154, 2026 Q1 192, 2026 Q2 184, 2026 Q3 162
   - CHB-ABU: 2025 Q4 108, 2026 Q1 95, 2026 Q2 99, 2026 Q3 105
   - ATM-WDL: 2025 Q4 90, 2026 Q1 96, 2026 Q2 111, 2026 Q3 126
   - PRF-DEV: 2025 Q4 166, 2026 Q1 184, 2026 Q2 188, 2026 Q3 177
   - DRM-REA: 2025 Q4 71, 2026 Q1 80, 2026 Q2 77, 2026 Q3 71
   - MER-RND: 2025 Q4 329, 2026 Q1 329, 2026 Q2 287, 2026 Q3 331
   - CRY-OFF: 2025 Q4 72, 2026 Q1 84, 2026 Q2 73, 2026 Q3 69
   - ELD-EXP: 2025 Q4 108, 2026 Q1 98, 2026 Q2 109, 2026 Q3 94
   - GMB-SPL: 2025 Q4 76, 2026 Q1 79, 2026 Q2 80, 2026 Q3 83
5. SARs filed in 2026 by month, initial and continuing activity, whole numbers:
   - January: initial 161, continuing activity 85
   - February: initial 135, continuing activity 93
   - March: initial 161, continuing activity 70
   - April: initial 152, continuing activity 76
   - May: initial 157, continuing activity 86
   - June: initial 168, continuing activity 89
   - July: initial 133, continuing activity 85
   - August: initial 163, continuing activity 102
   - September: initial 162, continuing activity 88
   - October: initial 143, continuing activity 79
