# Leak reader notes, task464

1. Decisive step. The prompt asks only the outcome. network_agreement_2027_capacity_terms.pdf 4.2 states: "Deliverable treatment positions means the treatment positions a Site is able to operate simultaneously." and 4.3 gives the 1.15 times demand standard. No sentence names the decisive step as "sweep the intervals".

2. Ranking file. None ranks areas on adequacy. state_adequacy_filing_2026.xlsx Area Summary gives 2026-position counts (contracted_sites, licensed_stations, treatments_delivered_2025) per area, not a ranking.

3. Helper-only files. enrolment_projection_2027.csv (growth factors), staffing_roster_2026q4.csv (sessions per week), encounter_extract_transmittal.json (row counts, timestamp convention), out_of_network_payments_reconciliation_2026.xlsx (control totals).

4. Reads as the answer. Nothing. Closest: the filing's "licensed_stations" and the directory's "attested_stations" read as the capacity input, which is context.

5. Literal fixing sentences. 4.2: "A Site's weekly treatment slots are the treatments the Site can deliver in a week, being its deliverable treatment positions multiplied by the treatment sessions its roster staffs in a week and by the treatments a position delivers in a session for the Site's service category." Result: positions x roster sessions x (1 for haemodialysis, 2 for infusion). 4.3: "at or above 1.15 times the area's projected 2027 weekly treatment demand"; demand is 2026 calendar-year treatments a week (one fifty-second of the year) of in-scope sites times the growth factor. 4.1 selects sites with a 2027 contract intent on the current attestation cycle, in the area recorded on that cycle. 4.4: "Encounters recorded without a stop time or a recorded length are not delivered treatments."

6. What decides the main answer. Mostly the choice of how to measure "deliverable positions" (analytical, via 4.2 definition), plus following stated rules (4.1 scope, 4.4 delivered definition, 4.3 formula). The stated rule application is heavy; the deciding step is the positions estimate. No planted item found.

## Hardest look 1: licensed count not equal to runnable positions
Yes, fairly plainly. 4.2 defines positions as "the treatment positions a Site is able to operate simultaneously" and separately says "A Site's licensed station count, where used, is the count on the Site's own facility licence row at its service address, and not a count held at a corporate holder." The words "where used" and the separate definition tell the solver licensed stations are a different concept (and that a stations figure is only optional). The directory column is named "attested_stations", the register "licensed_stations", the PDF fee schedule says fees are "charged on the station count entered on the facility's licence row". Nothing states that stations exceed runnable positions, but the contrast between "stations" and "positions able to operate simultaneously" is a strong hint.

## Hardest look 2: invitation to sweep intervals for concurrency
Yes, by shape and by the same definition. The word "simultaneously" in 4.2 is the only text pointer. The 2023-24 table has service_start and service_stop (local clock, strings), the 2025-26 table has service_start (UTC offset) and service_minutes; the transmittal json has "timestamp_convention" noting the two clock conventions. Those make an interval-overlap sweep feasible and the timestamp note invites normalising times, but no sentence says "concurrent", "peak", "overlap" or "maximum at one time". Counting/summing is the other obvious reading of the same data.

## Other items
- File names describing data not org record: encounter_extract_transmittal.json is a transmittal, acceptable; "out_of_network_payments_reconciliation_2026.xlsx" is fine. None flagged.
- Hidden sheets, comments, tracked changes: none (all sheets visible, no comment parts, no tracked changes).
- Four-plus digit figures reading as committed answers: none in documents. Filing Area Summary shows 2025 treatment totals and station totals (context for the 2026 position). Reconciliation totals (11855 lines) are control totals.
- Dates later than setting: files are mtime 2027-02-16 and position date is 2027-02-19, consistent with the setting. Directory 2026 cycle attested_on up to 2026-11-18; encounters pulled 2027-01-05. No anomaly.
- Machine-generated signs: all three xlsx are openpyxl output (default theme, workbook.xml with fullCalcOnLoad, creator "Wrenlow Community Health Plan", register creator "State licensing authority"); PDFs have blank Title/Author, Producer set to "Wrenlow Community Health Plan" even for the state fee schedule (a state document produced by the plan). The fee schedule PDF and the licensing register's creator mismatch is a mild tell. Locality names/operators look procedurally generated (e.g. "Kestrel Flats Infusion Suite" operator of a dialysis centre, same operator for several unrelated sites).
