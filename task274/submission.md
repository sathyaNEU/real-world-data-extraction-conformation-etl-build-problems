# task274 submission

## Tags

**Domain:** Criminology & Justice (intervention, policing and policy evaluation).  
**Analytical objective:** Experiment & Causal Analysis.

## 1. Final Recommendation

**We should renew Nethercote's pretrial diversion agreement for 2027 at the pilot's scale.**
Being offered a place lowers the share of listed defendants convicted in the referred case by 18 percentage points, 56% not offered against 38% offered, above the resolution's 15-point floor and short of its 25 points for full scale. Not full scale on the shares the docket records by 31 August 2026 (53% against 18%) or on each group's cumulative incidence of conviction at the longest follow-up (31 points), which count open offered cases as unconvicted while most of them are participants the program has not yet terminated or completed. Not a lapse on the cases already ended, which keep the terminated participants and leave out those still in the program.

## 2. Critical Components

1. Share convicted at final disposition among defendants not offered a place: **56%**
2. Share convicted at final disposition among defendants offered a place: **38%**
3. Chance a participant is terminated within the twelve-month term: **39%**
4. Share of terminated cases ending in conviction: **91%**

## 3. Step-by-Step Solution

1. Took each draw's list and result from diversion_lottery_draws_2025_2026.xlsx and joined both docket extracts (legacy_docket_events_2025_2026.csv and cms_docket_events_2026.csv) on the case number in either format, with the new system's UTC stamps on Central dates and one event per date and kind: 1,801 defendants offered a place and 1,807 not offered.
2. Ended each case at its first disposition event (a guilty plea, a guilty verdict or a guilty finding on the stipulated record convicted; a dismissal, nolle prosequi, acquittal or dismissal on completion not) and completed open not-offered and declined cases at their own group's disposed rate: 56% not offered, and 55% for the 12% of offered defendants who declined.
3. Built a life table of terminations by program month from each agreement's term in its docket entry and each termination's date: the final review terminates 23% of the participants who reach it, and the chance of termination within the term is 39%.
4. Took the conviction rate of terminated cases already disposed: 91%.
5. Completed the offered group through those rates, as Resolution 2025-31 section 3 counts every listed defendant at final disposition: 38% convicted, a reduction of 18 percentage points.
6. Classed each case filed in fiscal 2026 by its count 1 under PDU-2026-01's 2026 sections, reading a section in the new system's record of a case converted at go-live as a 2026 section and every other section in the numbering in force on its offense date through penal_code_conversion_table_2026.csv, giving the class and division counts in block 4.
7. Took each Nethercote site's fiscal 2026 hours as each participant's last running total in the new system's workbooks plus the old system's monthly hours for participants who left before 16 January 2026, and its restitution as the old system's receipts plus the new system's amounts divided by 0.95 (agreement clause 6), both January 2026 reports included, giving the site figures in block 4.
8. Applied Resolution 2025-31 section 5: 18 points is at least 15 and under 25, so the agreement is renewed at the pilot's scale.

## 4. Deliverable Answers

### diversion_renewal_memo_2027.docx

1. Call: renew Nethercote's pretrial diversion agreement for 2027 at the pilot's scale.
2. Reduction in the share convicted from being offered a place: 18 percentage points.
3. Share convicted among defendants offered a place: 38%.
4. Share convicted among defendants not offered a place: 56%.
5. Cases filed in fiscal 2026 by eligible class of the lead charge, whole cases:
   - Theft and fraud: 1,962
   - Criminal damage: 655
   - Drug possession: 1,219
   - Public order: 1,125
   - License and driving: 947
6. Eligible cases filed in fiscal 2026 by court division, whole cases:
   - Larkmoor City: 2,325
   - Bramwick: 1,445
   - Wendmoor: 1,219
   - Strandham: 919
7. Community service hours participants worked in fiscal 2026 by Nethercote site, whole hours:
   - Larkmoor City: 8,051
   - Bramwick: 5,194
   - Wendmoor: 4,926
   - Strandham: 3,339
8. Restitution participants paid in fiscal 2026 by Nethercote site, whole dollars:
   - Larkmoor City: 37,165
   - Bramwick: 33,175
   - Wendmoor: 25,530
   - Strandham: 19,325

### conviction_by_arm_2027.png

1. Line chart of each group's share convicted in the referred case by month since its draw, months 0 to 14, as recorded to 31 August 2026, with each group's share at final disposition (56% not offered, 38% offered) as a dashed line and the 18-point reduction marked between them.
