# leak check, task123

**Verdict: REVIEW.** 15 files read, 38 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: rejected, architecture, register, hardening, return, window, decisive, quarter, sentence, annual, device, balanced, record, nothing, census, co-funding, meters, schedule, records, section, government, identity, months, allocation, reading

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `OC1_electrification_capacity_standard_2026.pdf`: golden figure 253 appears: ...Supply voltage The statutory limits are 216 V to 253 V at the point of supply (Electricity Distributio...
- **REVIEW** `OC1_electrification_capacity_standard_2026.pdf`: golden figure 216 appears: ...phase. 6. Supply voltage The statutory limits are 216 V to 253 V at the point of supply (Electricity Di...
- **REVIEW** `OC1_electrification_capacity_standard_2026.pdf`: carries 9 of 10 distinctive words of the committed call: 'Rising mains A4, B2, C3 and C6 need re-phasing or a larger main before the 2027 chargers and cooktop conversions are con'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `OC1_electrification_capacity_standard_2026.pdf`: 5 of 25 stump-paragraph terms appear (register, record, schedule, records, section); read whether the document names the move
- **REVIEW** `switchboard_thermal_scan_June2025.pdf`: 3 of 25 stump-paragraph terms appear (annual, schedule, section); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (Leak reader, architecture 4 round 1 (2026-11-02, isolated, Sonnet at medium effort, on target.zip 1e6fa5a6))

1. Decisive step: none stated; the nearest is the capacity standard's section 2 ("A single-phase apartment draws its demand, existing and added, on the phase its supply is connected to"), which fixes how demand is assigned; no file says which phase any apartment is on or how to find it.
2. Nothing ranks or scores the candidates (raw and register-level data only; the workbook and chart the prompt names are deliverables, not in the pack).
3. Nothing exists only to help the analyst; context or distractor files: the switchboard thermal scan, the common-property submeters, the basement re-marking schedule, the meter exchanges, the power-quality events.
4. Nothing reads as the answer (ratings, register entries and meter reads only; the 80 per cent limit is the standard's own threshold).
5. The standard's sections 1 to 5 and 8 file the estimand (the highest weekday-evening half-hour summed demand of the apartments drawing on a phase, demand as twice the metered kWh, the additions per charger and cooktop conversion, ratings at 230 V, works where phase demand plus additions exceed 80 per cent of the per-phase rating, chargers to the apartment the car space is accessory to); none says how a phase is found.
6. An analytical choice: working out each single-phase apartment's phase (the register gives only 1PH or 3PH and an as-built board code, the interval file has no phase, the hourly voltage file has elements 1 to 3 only for three-phase meters); nothing planted.
Sweep flags: the standard is harmless (limits and definitions, no risers named, no method for the phase); the 2019 rising main schedule and the child meter register are harmless (ratings and levels served; 1PH or 3PH and a board code that a reader would have to test as a proxy, never the phase).
Minor: seven chargers in the works schedule sit at a storage cage and need the register and car spaces to place; unit identifiers differ in format across files (ordinary mess).
Realism: none generated (real export headers, genuine NEM12 structure, natural date formats and mixed address entries).

## Solver's-eye read (Leak reader, architecture 4 round 2 (2026-11-02, isolated, Sonnet at medium effort, on target.zip b5549311))

1. Decisive step: none stated; the nearest is the standard's section 5 test (works where, on any phase, phase demand plus added demand exceeds 80 per cent of the per-phase rating).
2. Nothing ranks the risers (the workbook and chart are deliverables, not shipped).
3. Nothing exists only to help the analyst.
4. Nothing reads as the answer (the 80 per cent threshold is a rule; the switchboard ratings are inputs).
5. Section 3 read literally: the highest weekday-evening half-hour summed demand of the apartments drawing on each phase, demand as twice the metered kWh; sections 2, 4 and 8 add the supply rule, the additions and the charger link.
6. The reader called the call mostly a stated procedure plus reconciliation, taking the register's "Board (as built 2004)" code (for example TC-DB23E) as the per-phase assignment. Main-session check: that code is tower, floor board and side (TC, DB23, E), not a phase; no file gives any apartment's phase, and round 1's reader and both judges found phase recovery from voltage co-movement decisive. The standard's sections 3, 4 and 8 file the WHAT (window, demand, additions, charger link) and no sentence assigns a supply to a phase.
Sweep flags: the reworded standard gives away no riser and no way to find a phase; the reads export's register and read-type descriptions and the event log read as the source systems' own exports (no note to the analyst); the applications register carries applicants' own free text with no resolver column.
Realism: none material; mild tell: the meter exchange log has seven rows for each of three reasons (sent to the author's realism list, not a gate).
