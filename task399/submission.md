## Tags

**Domain:** Human Factors & Ergonomics, safety incident and error analysis (signaller error at a rail operating centre).
**Analytical objective:** Root-Cause Analysis.

## 1. Final Recommendation

**Fund programme B, the workstation display renewal: its cause produced 8,985 of the operating centre's delay minutes in the twelve months to 30 September 2026.** Not signaller competence training (A), which the local investigations' findings put first, because the wrong routes they book to competence are slips onto an exit drawn beside the one required, made as often by experienced signallers. Not the seventh workstation (E), whose case rests on peak-hour error rates that come from those drawn-close routes carrying the peaks' requests. Not eight-hour shifts (C) or the ARS data rebuild (D), whose incidents carry fewer minutes even counted in full.

## 2. Critical Components

1. Wrong routes set onto the exit drawn beside the required one: **76** incidents, **8,173** minutes.
2. Workstation display faults: **10** incidents, **812** minutes.
3. The display renewal's minutes are highest on **W03 Hatherby**, at **3,544**, where its delivery begins.

## 3. Step-by-Step Solution

1. Kept the incidents in both operating incident registers that occurred from 1 October 2025 to 30 September 2026, UK time, per terms of reference 2.2.
2. Totalled each incident's primary and reactionary minutes in ocf_delay_records_2025-04_2026-09.csv and applied the moves attribution_reviews_2025-26_2026-27.csv records as agreed, per terms of reference 2.4.
3. Mapped each wrong route's route set and route required to their exit signals through the routes in workstation_layout_export_r8.2.1.json and measured the two exits' buttons on their screen: 76 were drawn 8.0 to 11.5 pixels apart, the other 14 wrong routes 60 pixels or more.
4. Read roc_signaller_actions_20251001_20260930.csv: of the 360 routes cancelled within twenty seconds of being set, all but three were followed from the same entrance by a request for the exit drawn beside the one cancelled, and at the drawn-close routes slips run alike for first-two-years and other signallers and in quiet and busy hours, so only the renewal's redraw would have prevented the 76, per terms of reference 2.3.
5. Added the workstation display faults the renewal's new display system removes: the display renewal's cause produced 8,985 minutes, more than any other programme's cause.
6. Split those minutes by the register's workstation: W03 Hatherby leads with 3,544, so delivery begins there, per terms of reference 2.5.
7. Rebuilt each workstation's shifts from both roster workbooks and roster_changes_2025-26_2026-27.csv, took each shift's signaller as the one whose actions roc_signaller_actions_20251001_20260930.csv shows on that workstation (which also places every relief duty and the changes made on the day that the changes list lacks), counted hours on the clock across both clock changes, and split each signaller's hours at the second anniversary of the date qualified in signaller_competence_register.xlsx.
8. Read server B's stamps in ars_status_log_20251001_20260930.csv as Central European time (its copies of server A's events sit one hour behind in winter and two in summer), merged both servers into one event per change, mapped the old sub-area codes through the layout export, applied each workstation-wide switch-off to all of that workstation's sub-areas, and summed each sub-area's hours off within each UK calendar quarter.

## 4. Deliverable Answers

### improvement_plan_case_2027.pptx

1. Programme B, the workstation display renewal, 8,985 delay minutes.
2. Bar chart of those minutes by workstation, marking W03 Hatherby, where delivery begins:
   - W03 Hatherby: 3,544
   - W05 Kestrow: 1,487
   - W01 Fenmoor: 1,266
   - W06 Wellanby: 1,230
   - W02 Callowby: 762
   - W04 Tollinghurst: 696

### staffing_and_ars_2025-26.xlsx

3. Hours worked by workstation, by signallers then in their first two years since qualifying and by everyone else:
   - W01 Fenmoor: 1,296.0 and 7,464.0
   - W02 Callowby: 1,828.0 and 6,932.0
   - W03 Hatherby: 1,729.5 and 7,030.5
   - W04 Tollinghurst: 3,947.5 and 4,812.5
   - W05 Kestrow: 1,143.5 and 7,616.5
   - W06 Wellanby: 1,975.5 and 6,784.5
4. Sub-area hours with automatic route setting switched off, in total for each workstation, October to December 2025, January to March, April to June and July to September 2026:
   - W01 Fenmoor: 296.0, 308.5, 305.1 and 241.9
   - W02 Callowby: 220.2, 226.9, 233.1 and 165.4
   - W03 Hatherby: 336.7, 279.5, 339.1 and 291.5
   - W04 Tollinghurst: 168.7, 219.1, 175.5 and 176.8
   - W05 Kestrow: 195.5, 150.9, 224.2 and 176.9
   - W06 Wellanby: 260.0, 282.7, 286.0 and 314.9
