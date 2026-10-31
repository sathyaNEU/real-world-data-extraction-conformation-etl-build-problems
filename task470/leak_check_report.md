# leak check, task470

**Verdict: REVIEW.** 14 files read, 51 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: section, household, statistics, fortnight, points, hourly, heating, design, office, sentence, cadastre, nothing, population, reading, family, statistic, record, consumption, golden, pattern, decides, residents, second, decisive, floors

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `regulation_vacant_dwelling_grant_2027.pdf`: golden figure 5.0 appears: ...qualifies for the grant when its vacancy share is 5.0 per cent or more. Section 7. Certification By 15...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `regulation_vacant_dwelling_grant_2027.pdf`: 8 of 25 stump-paragraph terms appear (section, statistics, fortnight, points, office, cadastre); read whether the document names the move

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


## Solver's-eye read

Architecture 2, read 1 on target.zip 26076f7e (isolated Sonnet reader, a fresh copy of prompt.txt and target/ only).

1. Decisive step: no sentence states it; the nearest are the regulation's Section 4 (vacant: nobody lived in the
   dwelling on any day of the reference fortnight, the population register not deciding it) and Section 5 (the hub's
   metered values for the dwelling's metering points, read with the cadastre): the definition and the evidence,
   not the method.
2. Ranking file: none; no vacancy share, flag or municipal summary anywhere; the outage sheet ranks nothing.
3. Helping file: none; the regulation and the ministry's email govern, the municipality list, spot prices and outage
   sheet read as context, the shareholder and business registers as the email's ownership sources.
4. Answer figure or name: none; the regulation's 5.0 per cent, NOK 40,000 and its dates only.
5. Population sentence: Section 6's share (counted dwellings vacant over counted dwellings, one decimal, 5.0 or more
   qualifies) over Section 3's counted dwellings; the literal result is the golden's population and threshold.
6. What decides: the reader put it nearest rule application with an analytical element, since turning metered
   values into "nobody lived there" is filed nowhere. Ruled: that unfiled step is the decisive analysis (the
   household's day against the dwelling's own night), and the judge's Gate H reads it as analytical.

Sweep line: Section 6's 5.0 is the regulation's own threshold, harmless.

Realism: the reader found the shareholder register too regular (the same three namesake suffixes in every
municipality, 30 shares a company, one partial holding); sim.py now varies the suffixes, the share counts and some
couples' companies without touching a random draw, every figure unchanged, re-cut as target.zip 52fc465d. Section 4's
register sentence reads as a clarification and stands, since it closes the register reading. The three-row outage
sheet and the clean municipality numbers are the county's own, kept.

Main thread on the REVIEW lines: sweep 3's 5.0 is the threshold Section 6 of the regulation files, a figure every
reading shares, harmless; sweep 4's terms (section, statistics, fortnight, points, office, cadastre) are the
regulation's own nouns for its sections, the office, the fortnight, the metering points and the cadastre, and none
names the decisive step, harmless.
