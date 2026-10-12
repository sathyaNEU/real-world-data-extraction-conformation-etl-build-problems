# task111 submission

## Tags

**Domain:** Business & Operations Analytics, field service and maintenance (appointment keeping in a residential heating repair region).
**Analytical objective:** Root-Cause Analysis.

## 1. Final Recommendation

**The cause that will be behind the most missed appointments over January to March if nothing changes is Parts & van stock, 322 of the July to September misses: engineers collecting parts at merchants since the vans went to fortnightly top-ups, so the change before January is to put the vans back on weekly top-ups.**

Not Rota & cover, which caused the most July to September misses (571) but stops over the winter: from October to May the contractor panel takes the evening calls standby cannot reach, so no day-roster engineer clears a call-out late and the eleven-hour rest never delays a log-on. Not punctuality (246) or the routing engine (187), which carry into the winter below it.

## 2. Critical Components

1. July to September missed appointments tracing to Parts & van stock, the largest cause that carries into January to March: **322**
2. July to September missed appointments tracing to the rest after a late out-of-hours call-out (Rota & cover), none of which recur over January to March: **571**
3. Rota & cover missed appointments in any month from October 2025 to May 2026 under the same trace: **0**
4. The cause that comes second over the peak, Engineer attendance & punctuality: **246**

## 3. Step-by-Step Solution

1. Took every attended appointment (Completed or No access) dated 1 July to 30 September 2026 in field_appointments_2025-07_2026-09.csv whose on_site_at is after its arrival window (FS-07 1.1, 1.2).
2. Traced each miss back along its engineer's day to its originating event (FS-07 3.1, 3.2), using the log-on in engineer_day_log_2025-07_2026-09.csv and the travel, on-site and job times against planned travel and booked minutes: every missed day has exactly one.
3. Matched each late log-on to ooh_desk_callouts_2025-07_2026-10.xlsx through the payroll number in field_workforce_register.xlsx: 571 misses follow a call-out cleared after 21:00 with the log-on 11h00 to 11h04 later, which HR-FS-03 3.1 and 6.3 put outside the engineer's control, so they go to Rota & cover; Parts & van stock is next with 322.
4. Ran the same trace over October 2025 to May 2026: no Rota & cover miss in any month, because in those months the contractor panel took the evening calls standby could not reach and no call-out-list attendance cleared after 21:00.
5. Read the out-of-hours desk record for the nights of 1 to 4 October 2026: the contractor panel is attending again, so the Rota & cover misses do not carry into January to March.
6. Ranked the causes that do carry: Parts & van stock 322, Engineer attendance & punctuality 246, Travel & routing 187.
7. Checked the trace against missed_appointment_verification_jan-may_2026.csv: it reproduces all 200 verified January to May cases.
8. Recommendation: Parts & van stock is the cause to fix before January (322 of the July to September misses); put the vans back on weekly top-ups.

## 4. Deliverable Answers

### missed_appointments_q3_2026.docx

1. Opens on the cause: Parts & van stock, 322 of the July to September missed appointments, the largest of the causes that carry into January to March.
2. The change before January: put the vans back on weekly top-ups.
3. The cause that comes second over the peak: Engineer attendance & punctuality, 246.
4. Every cause family in FS-07, July to September 2026 missed appointments, goodwill credits paid on those misses in whole pounds, and complaints:
   - Rota & cover: 571 missed, 18,160 pounds, 110 complaints
   - Parts & van stock: 322 missed, 10,060 pounds, 59 complaints
   - Engineer attendance & punctuality: 246 missed, 7,740 pounds, 45 complaints
   - Travel & routing: 187 missed, 6,020 pounds, 51 complaints
   - Job duration & standards: 153 missed, 4,820 pounds, 34 complaints
   - Other: 65 missed, 2,060 pounds, 16 complaints
   - Customer access: 30 missed, 930 pounds, 11 complaints
5. Each patch, July to September missed appointments from Parts & van stock, the patch as it stood on the appointment date:
   - Glasgow North & West: 39
   - Glasgow South & East: 49
   - Lanarkshire: 61
   - Ayrshire & Renfrewshire: 42
   - Edinburgh & Lothians: 72
   - Fife & Forth Valley: 59

### missed_appointments_q3_2026.png

1. A stacked bar for every reporting week (Thursday to Wednesday) from 1 January to 24 September 2026, split into the seven cause families with a legend.
2. The 1 July go-live drawn as a vertical line and labelled.
3. The worst week annotated: the week of 3 September 2026, 190 missed appointments.
4. Title: "Late out-of-hours call-outs drove the summer rise and stop with the winter panel; van stock is what carries into January".
