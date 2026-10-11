# leak check, task180

**Verdict: REVIEW.** 11 files read, 100 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: heating, register, decisive, supply, manager, related, ranked, attribution, architecture, network, sentence, reader, screen, account, written, main-tank, pattern, remedy, bookings, stated, operator, compartment, points, ranking, attack

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `ES-DGA-02_fleet_dga_condition_standard.pdf`: 6 of 25 stump-paragraph terms appear (register, manager, network, written, main-tank, remedy); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `dga_main_tank_results_2021-2026.csv`: columns a generator names and an organisation does not: oil_temp_c

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `mobile_substation_bookings_2027-28.xlsx`: 18 ISO dates after 2026-10-16, e.g. 2027-04-05, 2027-04-09, 2027-04-12, 2027-05-21, 2027-06-07

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt form (clean)

## Solver's-eye read (pass 4, isolated reader on the hardened pack, hardening loop 1)

1. Nearest: ES-DGA-02 5.2 "Internal inspection outages are allocated to the code 3 transformers with such a fault, in descending order of severity score." with 5.1 "is the remedy for a fault in the main tank" -- "the condition for qualifying, not how to test it. No file says how to tell a main-tank fault from tap-changer diverter oil leaking into the tank. That test is only in the data: a quick look shows the acetylene in DSL-T1, LST-T2 and RLS-T2 rising in step with the SCADA tap operations."
2. none (thermal survey ranks switchboard hot spots; "Transformers, their tanks, radiators and tap changers were not part of the scope.")
3. none (oil_results_notes.md an ordinary handover note; fields only).
4. none (no slate names, codes or severities; held windows "To be advised").
REVIEW: ES-DGA-02 stump terms harmless (ordinary wording; never mentions tap-changer contamination, gas tracking or any transformer); oil_temp_c harmless (label temperature, 122 blanks); bookings dates harmless (forward sheet, Apr 2027-Mar 2028).
Plan step 3: "Main-tank test (5.1-5.2): for each code 3 transformer with an in-oil tap changer, compare the acetylene increases between monthly samples with the SCADA tap operations over the same intervals. Acetylene that tracks tap operations is diverter leakage, so those transformers are excluded." -> drops DSL-T1, LST-T2 AND RLS-T2 = rung 3b (SBG-T2, CGT-T1, SPN-T2). The hardened rung holds against the reader's plan; no gas-ratio step planned.
