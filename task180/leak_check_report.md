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

## Solver's-eye read (pass 5, isolated reader, after the judge's hygiene fix)

1. none. Nearest: ES-DGA-02 5.2 "Internal inspection outages are allocated to the code 3 transformers with such a fault, in descending order of severity score." "one of about a dozen rules given equal weight, and it does not say which test or which transformer decides the slate."
2. none (the thermal survey ranks switchboard hot spots; "Transformers, their tanks, radiators and tap changers were not part of the scope.").
3. none (oil_results_notes.md a handover note; the run report an ordinary extract log).
4. none (people are document owners, crews and planners; bookings sites "To be advised"; the ten monthly-sampled units a watch-list under 3.1).
REVIEW lines: all three harmless (ordinary standard wording; the label temperature a normal field with 122 blanks; a forward booking sheet).
Plan step 4: "Keep only code 3 units whose gas shows a main-tank fault (5.1-5.2). Check tap-changer type and service history before trusting main-tank acetylene." No step reads the gas the acetylene arrives with.
