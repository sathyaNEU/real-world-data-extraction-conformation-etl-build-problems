# leak check, task306

**Verdict: REVIEW.** 18 files read, 30 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: letter, take-off, sentence, started, provenance, carried, carries, specification, antipsychotic, golden, practice, architecture, population, second, checks, specialist, programme, decisive, million, outside, product, antipsychotics, reflex, receipt, orders

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `deprescribing_review_protocols_2026.pdf`: carries 12 of 17 distinctive words of the committed call: 'Run review B, benzodiazepines and Z-drugs in people aged 65 and over: it would take about 290 patients off their medicin'
- **REVIEW** `medicines_safety_programme_2027.pdf`: carries 15 of 17 distinctive words of the committed call: 'Run review B, benzodiazepines and Z-drugs in people aged 65 and over: it would take about 290 patients off their medicin'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `clun_valley_pilot_close_out_2026.pdf`: 4 of 25 stump-paragraph terms appear (antipsychotic, practice, checks, antipsychotics); read whether the document names the move
- **REVIEW** `deprescribing_review_protocols_2026.pdf`: 5 of 25 stump-paragraph terms appear (antipsychotic, practice, checks, programme, antipsychotics); read whether the document names the move
- **REVIEW** `medicines_safety_programme_2027.pdf`: 8 of 25 stump-paragraph terms appear (letter, specification, antipsychotic, practice, programme, outside); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "A short paper for the federation's board, medicines_safety_review_2027.pdf, should recommend the review to run, name the runner-up and the gap, chart for each review the patients it would take off their medicine beside t"

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `emergency_admissions_falls_65plus_2025-2026.csv`: names 5 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `member_practice_register_2026.csv`: names 5 of 5 answer-set candidates; confirm it does not rank them on the decision question

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

One isolated reader (Sonnet, medium effort), prompt.txt and the unzipped target.zip 0bacf975 only, 2026-11-08. It read the
prompt, the three PDFs and the three small CSVs in full and sampled the large files. Verdict: no leak.

1. Decisive step named: none. It quoted the specification's 3.3 (each patient's chance of being off the medicine six
   months after review times the table 1 rate, summed over the patients in scope) and 3.2 (the population), and said
   nothing filed says which off-rate to carry to patients not yet reviewed. It read the close-out's section 3 (no
   practice, age group or sex differed from its review's overall rate by more than chance) as nudging toward one pooled
   rate per review: that is the pilot's own measured result and the default path's step 3, not the decisive step.
2. A file ranking the candidates: none. The close-out's 40.0, 23.0 and 27.9 per cent are the pilot's own six-month
   rates and rank no review by harm avoided across the federation.
3. A file existing only to help the analyst: it named the protocols, the specification and the close-out. Ruled
   harmless: each is a document the federation keeps for its own work (the searches, the schedule agreed with the
   ICB, the pilot's report to the board), and none describes a column or how the files join.
4. A figure or name reading as the answer: none.
5. The literal reading: the patients registered outside Clun Valley who meet the protocol on 31 December 2026, every
   one reviewed; the first year from April 2027 at rates per 100 patient-years; expected patients off and expected
   serious harms, summed over patients; reviews A, B and C compared on harm avoided; left open, how to estimate the
   off-probability for unreviewed patients. This is the design note's estimand row.
6. The deciding kind: an analytical choice, which off-probability to carry to unreviewed patients and whether the
   pilot's rates transfer. It did not name who started the medicine. It called the close-out's sentence on the 53
   re-issued patients a mild pointer to the definition of off, which the specification's 3.4 files.

The three REVIEW lines: all harmless, the same rulings as the design note's Stage 4 section.

Machine-generated tells it listed, each measured on the cut and ruled:
- Practice codes M80 to M89, two practices closed on 1 April 2025: the register's merger (Layer 1), dated at the
  financial year's start; harmless.
- Invented trust, ICB and place names: the fiction; harmless.
- Clinical-system consultation times on a 15-minute grid, ids prefixed by the practice code: 7,482 of 9,301 times sit
  on the quarter hour (booked slots) and 1,819 do not; ids within a practice step by 1 to 978 (median 54), the
  practice system numbering every consultation and the extract keeping the pharmacists', and do not follow date
  order; harmless.
- Hub slot starts on the quarter hour: a booking system's slots; harmless.
- Smooth list growth: monthly changes run from minus 35 to plus 36 patients and 26 per cent of them are falls;
  harmless. The first-quarter falls peak is winter's and is not in every network (Wrekinside Central's 2026 Q1 sits
  below its Q2); harmless.
- PDFs without a logo or reference: the specification carries its version, date and owner and the close-out its
  date and author; harmless.
- The close-out's "No serious incidents were reported": a pilot report's patient-safety line; harmless.
- The group session register lists every attendee per session: what an attendance register is; harmless.

### Read 2, after the stage 4 fix

One isolated reader (Sonnet, medium effort), prompt.txt and the unzipped target.zip ea8155d7 only, 2026-11-08, after
the specification's section 4.3 gained its count-once sentence. Verdict: no leak.

1. Decisive step named: none. It quoted the specification's 3.3 and said no filed sentence says how to estimate the
   chance off from the pilot; it read the close-out's sections 2 and 3 as nudging toward the overall pilot rates (the
   default path).
2. A file ranking the candidates: none.
3. A file existing only to help the analyst: none; the close-out and the protocols read as ordinary organisational
   documents.
4. A figure or name reading as the answer: none.
5. The literal reading: the specification's 3.2 and 3.3 with the protocols; not filed, how to estimate the
   probability of being off. This is the design note's estimand row.
6. The deciding kind: mostly an analytical choice, how to estimate the probability of being off from the pilot. It
   did not name who started the medicine. It noted that the scope and the 3.3 sum are stated rules, which they are:
   the stump sits in the estimate they leave open.

The three REVIEW lines: all harmless, as in read 1.

Machine-generated tells it listed, ruled:
- Pseudonyms as 10-character hexadecimal in every file, and system ids with prefixes: a linkage service's pseudonyms
  and each system's own numbering, which steps by varying gaps (consultations 1 to 978 apart within a practice);
  harmless.
- One postcode district per network and 5 to 7 practices per network: a rural federation's networks are drawn by
  geography; harmless.
- The falls extract rectangular with smooth list sizes: a quarterly extract by network; harmless.
- The ePACT2 summary's label "0408010 Control of epilepsy (gabapentinoids)" is not the BNF's wording: corrected in
  the generator to "0408010 Control of the epilepsies: gabapentin and pregabalin", the paragraph's BNF name with the
  substances the line counts. A declared distractor that no figure reads.
- The close-out's tables sum and its "smallest p-value was 0.21": counts add up, and the sentence reports the tests
  the table rests on; harmless.
- Three one-page PDFs from LibreOffice Writer with one author and footer style: the federation's own template;
  harmless.
- dm+d codes such as 39778911000001102: the UK drug extension's form (namespace 1000001, partition 10, check digit);
  harmless.
