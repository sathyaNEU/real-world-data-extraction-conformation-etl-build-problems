# leak check, task464

**Verdict: REVIEW.** 13 files read, 35 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: section, current, export, architecture, half-hour, kestle, decisive, sections, conductor, closed, nothing, beyond, primary, metered, monitors, silent, register, substation, estate, settlement, replaced, measured, reading, construction, carries

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `hv_conductor_data_EDS-02-0310.pdf`: golden figure 500 appears: ...Cable, 3-core belted, Cu 0.0915 0.114 0.076 445 / 500 XLPE 95 AL 95 mm2 aluminium, XLPE, triplex Cable,...
- **REVIEW** `hv_conductor_data_EDS-02-0310.pdf`: golden figure 300 appears: ...2024. Supersedes issue 6 (2019); issue 7 adds the 300 mm2 triplex cable and corrects the 0.04 sq in rea...
- **REVIEW** `losses_programme_2027-28_brief.pdf`: golden figure 300 appears: ...q in copper, paper-insulated lead-covered, 3-core 300 mm2 aluminium, XLPE, triplex Ashlade CB 4 HV-2114...
- **REVIEW** `losses_programme_2027-28_brief.pdf`: candidate 'Copsewell Town' sits beside decision vocabulary: ...jects Feeder Breaker Sections replaced (network model IDs) Existing conductor Replacement Copsewell Town CB 3 HV-20543, HV-20609 0.1 sq in copper, paper-insulated lead-covered, 3-core 300 mm2 al...
- **REVIEW** `losses_programme_2027-28_brief.pdf`: carries 4 of 5 distinctive words of the committed call: 'Fund the Kestle reconductoring from the 2027/28 losses programme.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `hv_conductor_data_EDS-02-0310.pdf`: 3 of 25 stump-paragraph terms appear (conductor, register, construction); read whether the document names the move
- **REVIEW** `line_loss_factors_2025-26.pdf`: 5 of 25 stump-paragraph terms appear (export, metered, substation, settlement, measured); read whether the document names the move
- **REVIEW** `losses_programme_2027-28_brief.pdf`: 11 of 25 stump-paragraph terms appear (section, current, half-hour, kestle, sections, conductor); read whether the document names the move

## 6 ranking artifacts (REVIEW 4, INFO 1)
- **REVIEW** `customers_by_substation_2023-2026.csv`: names 4 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `hv_network_model.xlsx`: names 4 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `interruptions_2023-2026.csv`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `losses_programme_2027-28_brief.pdf`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `secondary_substations.csv`: names 5 of 8 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (general-purpose, sonnet, medium), 2026-10-28, on a fresh copy of prompt.txt and target/ only. It
flagged that the session's startup context (the repository's recent commit subjects) named the build's feeder, the
generation site and the mechanism before it opened a file, and that it cited only what it found in the copy.

1. Decisive-step sentence: none. Closest: the brief's selection rule and "the section's I2R loss is worked out at the current that section carried in that half-hour", stated identically for all eight; no file says a section's current must be rebuilt from topology rather than read off the breaker.
2. Ranking file: none.
3. Help file: iis_reporting_definitions_2025-26.pdf (definitions, not raw data); hv_conductor_data_EDS-02-0310.pdf decodes the model's conductor codes. Ruled harmless: the first is the network performance team's governing definitions for the return (an organisation's own rule, cited by the brief), the second the asset policy's engineering data sheet; neither describes a column or how the files join.
4. Answer-like figure or name: none.
5. Literal sentence: the brief's sizing paragraph fixes the window, the per-section per-half-hour paired comparison, the phase balance, 20 C and no loss or voltage-drop add-on, and leaves open how a section's current is obtained where it is not the breaker's reading. Ruled: the golden is that sentence's only physical execution (the current each replaced section carried, from every connection beyond it), so the literal reading is the golden.
6. What decides: an analytical choice; it falls out of combining the network model's topology with the generation connections in hv_connections.csv against a SCADA that meters only each breaker.
7. Realism: none (SCADA distributions, the solar meter's day and night profile, the hire log's dates and the PDFs' metadata read as ordinary exports; the brief reads as committee prose).

a to h: all harmless (the data sheet's constants, the losses value the prompt itself applies, the project table treating all eight alike, the customer, model and interruption files holding no saving, CI, CML or ranking).
