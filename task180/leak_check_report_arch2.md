# leak check, task180

**Verdict: REVIEW.** 11 files read, 100 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, decisive, heating, attribution, main-tank, acetylene, supply, manager, related, written, ranked, architecture, network, sentence, ranking, reader, screen, account, outages, decomposition, source, pattern, remedy, domain, diagnosis

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `ES-DGA-02_fleet_dga_condition_standard.pdf`: 8 of 25 stump-paragraph terms appear (register, main-tank, acetylene, manager, written, network); read whether the document names the move

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

## Solver's-eye read (pass 6, isolated reader, hardening loop 2)

1. none. ES-DGA-02 5.2 sets the rule; "No file says how to tell a main-tank fault from other gassing, or that the analysis turns on it."
2. none (the thermal survey's Priority 1-4 scale covers switchboards; transformers out of scope).
3. none (oil_results_notes.md defines fields without drawing conclusions; listed under "documents copied" in the run report).
4. none (no document names or scores a transformer; the bookings say "To be advised").
REVIEW lines: all three harmless (the standard's own vocabulary, naming no contamination test, ratio or transformer; a normal label field whose second issues change it; a forward booking sheet).
Plan: the IEC 60599 acetylene-to-hydrogen indicator and acetylene steps against the tap counters, the vacuum unit as no source, and "check the maintenance log for events that distort the increases, such as oil processing and the LST-T2 radiator change". No step attributes each gas to its own source or reads the hydrogen's timing against the acetylene.
