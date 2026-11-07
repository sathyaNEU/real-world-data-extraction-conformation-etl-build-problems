# leak check, task286

**Verdict: REVIEW.** 13 files read, 6 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: litres, steady, decisive, census, volume, reference, orrimouth, population, reading, checks, ellingsea, housing, agency, sentence, signature, record, golden, gazetteer, question, measurement, status, family, answered, counts, margin

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `homes_in_use_pilot_terms_of_reference_v1-2.pdf`: 9 of 25 stump-paragraph terms appear (census, reference, orrimouth, ellingsea, housing, agency); read whether the document names the move
- **REVIEW** `housing_needs_assessment_2024_summary.pdf`: 5 of 25 stump-paragraph terms appear (census, orrimouth, population, ellingsea, housing); read whether the document names the move
- **REVIEW** `pennimouth_water_data_sharing_agreement_PW-DSA-2026-014.pdf`: 5 of 25 stump-paragraph terms appear (housing, agency, record, gazetteer, counts); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no roll call: 1 attributed opinion(s)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'png+xlsx' at 22% of 207 prompts (cap 20%); reword at the role level, not the verb

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

The isolated leak reader (medium effort) read prompt.txt and the 13 files of target.zip (sha256 216a2882290dc4781ae8fc2a88b7a6ea9ccfdfa52a53f9dea16eacbfafeb058e) on 2026-11-07, quoting only, solving nothing. Verdict: no LEAK. Sweep 4's design-note vocabulary lines were ruled by the orchestrator: the terms of reference, the data sharing agreement, the taxbase returns and the housing needs assessment use the words as ordinary context and none says how use shows in the meter data.

1. Decisive step: none stated. Closest is the ToR 4.3 definition of a week of use ("A week counts as a week of use if anybody lived in, stayed at or used the home on any day of it, for however short a time."), which fixes the unit but not how use shows in the meter data. No file says how to read the meter.
2. Ranking/scoring of candidates on the prompt's question: none. (HNA Table 4.1 ranks areas by census no-usual-residents share, a different quantity; see b.)
3. File that exists only to help: none. The meter data carries only PROPERTY_REF, METER_SERIAL, READ_DATE_UTC, CONSUMPTION_L, READ_TYPE (ACTUAL/ESTIMATED), with no flag or note interpreting it.
4. Reads as the answer: none. Nearest context is HNA 4.1 "Tarnhithe and Kittlesea stand out, reflecting their holiday lets and second homes", about the 2021 census with the lockdown caveat stated ("when some owners were living in their second homes and few lets were occupied").
5. Filed sentence fixing the figure: ToR 4.1 "The pilot will run in the shortlisted community area with the most homes that nobody used for at least 26 of the 52 weeks from Monday 29 September 2025 to Sunday 27 September 2026." with 4.2 "A home is a self-contained dwelling on the county address gazetteer, however it is taxed or rated and however it is let." and 4.3 (Monday to Sunday week, any use on any day counts). Literal result: population is gazetteer self-contained dwellings in the 8 shortlisted areas (4.4), window 52 Monday-Sunday weeks, unit is the home, criterion is at least 26 weeks with no use. How use is inferred from meter reads is not filed.
6. Decider: an analytical choice. Council tax status is expressly not the evidence (ToR 5.1 "which is not always how a home is used"); the call rests on inferring use from daily metered consumption (including keys, i.e. PW-to-UPRN match, the Teversby system change, and ESTIMATED reads), which no document states. Nothing is planted and no sentence tells the method. Layer-1 mess (two councils' layouts, legacy archive, UTC reads, best-fit lookup) is only cleaning.

a. harmless, because it names the shortlist (4.4) and defines the week and the window but does not rank areas, point at one, or say how to tell use from no use in meter data; 5.1 only says council tax is not always how a home is used (direction, not method).
b. harmless, because HNA Table 4.1 ranks by 2021 census household spaces with no usual residents (a different measure, with the lockdown caveat), and the census OA csv is bare counts by OA. Neither addresses 26 of 52 weeks of non-use. Mild: the HNA ordering (Tarnhithe, Kittlesea first) could pull toward a wrong answer, which is realistic context rather than a leak.
c. harmless, because the DSA 3.1 only lists fields (consumption "on each meter day", serial, "whether the head end received that day's read"); it says nothing on what a reading means for use, leaks, flows or thresholds. Its "head end received" wording faintly hints at missing/estimated reads, a field description only.
d. harmless, because prompt.txt only fixes the question, the window, the deliverable layout, the council tax long-term empty definition by reference ("as the Council Taxbase return defines them"), and "Every count is in whole homes." It gives no method and does not describe the data. Minor note: it says "the homes on the business rates list that day as self-catering holiday lets", which names the NDR list but is an ask, not a method.

Realism: none that reads as machine-made. The four PDFs have letterheads, document refs (CRI/HEB/2025/31, HIU-TOR-v1.2, TP-2391-HNA-SUM-F, PW-DSA-2026-014 v1.0), page numbering, version/document control, sign-off blocks, personal authors in metadata, and creation dates that fit each document; Creator/Producer fields are blank. Sources differ in system style (Teversby legacy dd/mm/yyyy csv, new xlsx with "Revenues and Benefits" as author, Swanholt ISO csv, UPPERCASE NDR, water company PROPERTY_REF scheme), so they read as separate systems. Minor tells: the Terms of Reference page 2 risks table has truncated cells ("the board may move leasing budget to grants at the six-month"), and the Teversby xlsx is a single "Liabilities" sheet (plausible). I did not finish a uniformity check of the meter parquet (2,286,365 rows, 2,132 ESTIMATED reads, min consumption 0).

Orchestrator's check of the reader's realism note: rendering page 2 of homes_in_use_pilot_terms_of_reference_v1-2.pdf confirms the defect is in the PDF, not pdftotext. Risks row 2's mitigation runs past its cell and off the page ("at the six-month" is clipped), risks row 3's mitigation crosses the cell border, and the document control row 1.2's change text runs into the By column ("risks addeM. Robson"). The other three PDFs show no overflow, overlap or rule crossing. Fix in the generator: wrap every table cell, complete the clipped sentence, and assert no text crosses a table rule or the page margin.
