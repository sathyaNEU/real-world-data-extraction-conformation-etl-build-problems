# leak check, task483

**Verdict: REVIEW.** 10 files read, 0 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: program, course, completers, quarter, programs, laboratory, median, objective, records, system, short-term, pooled, outcome, federation, degree, earnings, antibiotic, cultures, designation, selection, resistance, record, window, population, infections

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `uti_pathway_specification_2027-28.pdf`: carries 12 of 18 distinctive words of the committed call: 'Place the two UTI pathway pharmacists in Morrow Cross and Tamsey from 1 April 2027. Moving their 2026 first courses on o'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `uti_pathway_specification_2027-28.pdf`: 6 of 25 stump-paragraph terms appear (course, quarter, laboratory, federation, resistance, record); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `member_practice_register_2026.xlsx`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question

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

Isolated reader (general-purpose, Sonnet, medium) on fresh copies of prompt.txt and target/ only, 2026-11-02, read on
the final pack after the stage 4 fix (pack digest 0add17a8f4c9dc60; specification 3.2 and the prompt's ask changed). An
earlier read of the pre-fix pack (digest bd8e11e1bcfb421b) found no leak and named the decisive step an analytical
choice.

1. Decisive step: no sentence names it. The nearest is specification 3.2 ("the chance that a first course on it meets an
   organism the laboratory reports resistant to it, taken over all the federation's first courses whichever
   antibacterial each was in fact issued"), which reads as filed estimand text and not as a hint at a trap.
2. No file ranks or scores the networks on the question; no network-level resistance or mismatch table ships.
3. No readme, manifest or data dictionary; the pathway code lists, the laboratory's code tables and the register's
   Networks sheet are plausible real artefacts. ENTE (3,734 rows) is not in the organism table; the enterococcus ask
   turns on reading it.
4. Nothing reads as the answer.
5. Specifications 2.1, 2.2, 3.2 and 4.1 fix the population, the network, the unit and the pricing; the link between a
   course and a culture (window, which sample) is not stated.
6. What decides the main answer: an analytical choice (the reader names the estimate of the chance over the first
   courses); the semantic and rule items it lists sit in the asks.
7. Realism: 73,705 culture rows with uneven requesters, mixed specimen types, 203 accession numbers carrying more than
   one row, dd/mm/yyyy dates before the system change and ISO after; 118,996 issue rows with 136 dosage strings, varied
   quantities and monthly counts 2,957 to 3,461 ("a little regular but acceptable"); nothing uniform or round.

Verdicts on the REVIEW lines: uti_pathway_specification_2027-28.pdf harmless (the governing document the prompt points
to; no network, figure or result); member_practice_register_2026.xlsx harmless (practice counts and list sizes, no
ranking on the question). The design-note vocabulary line (six generic words in the specification) was ruled by the
main thread: harmless, the specification names no culture, window, antibiogram or prescribing history.

Main thread rulings: question 6 answers analytical, so rule 3 holds; the unstated course-to-culture link in question 5
is the open HOW the design leaves to the analyst, its window closed by SF4 (every window from the day of issue to two
days either side selects the same cultures); the 203 multi-row accession numbers are specimens that grew two organisms,
one row per organism by design; J83386 appears as a requester only before its merger; the monthly regularity is a
spread about twice Poisson in a process with no season (harmless). Verdict: NO LEAK.
