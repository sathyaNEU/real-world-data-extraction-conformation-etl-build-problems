# leak check, task304

**Verdict: REVIEW.** 12 files read, 0 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, laboratory, record, golden, first-time, positives, person, workbook, arrears, family, antibody, prison, pinned, corvane, arrivals, second, treated, decisive, window, accounts, arrival, asserted, inside, payment, carried

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `find_and_treat_van_2027_plan.pdf`: carries 11 of 12 distinctive words of the committed call: "The van should work the needle exchange pharmacies' new registrants in 2027, where it would start about 50 people on hep"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `fenwold_hcv_pathway_2026.pdf`: 6 of 25 stump-paragraph terms appear (register, record, person, antibody, prison, corvane); read whether the document names the move
- **REVIEW** `find_and_treat_van_2027_plan.pdf`: 7 of 25 stump-paragraph terms appear (register, person, antibody, prison, arrivals, arrival); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `corvane_hcv_courses_2017-2026.xlsx`: 16 ISO dates after 2026-10-12, e.g. 2026-10-13, 2026-10-16, 2026-10-21, 2026-10-22, 2026-10-23
- **REVIEW** `hcv_treatment_register_2015-2026.csv`: 31 ISO dates after 2026-10-12, e.g. 2026-10-13, 2026-10-14, 2026-10-18, 2026-10-19, 2026-10-20

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Pass 1 (target.zip a159a58b, isolated copy, sonnet at medium)

1. Decisive step: the plan's "We will place the van where it starts the most people on hepatitis C treatment in 2027" (section 2), the filed comparison rule; no sentence states which setting it picks.
2. None: no file ranks or scores the four settings; the only comparative table compares the two 2018-19 pilot sites.
3. None: every file reads as a record its organisation would keep.
4. None: nothing pairs a setting name with a count.
5. The plan's sentences fix the comparison (starts), the unit (a person once a year), the window (the two-year average, 2027 arrivals like those years), found and started (RNA detected at the van's test, a course within twelve weeks), the exclusion of people part-way through a course, and two of three rates from the pilot (silent on the share found with an active infection); the pathway fixes a course's end and what counts as confirmed.
6. An analytical choice: building each setting's own active-infection share among its own linked arrivals, rather than carrying a pooled rate; Corvane's records read against the approved premises a second complication.
7. Realism good (day-first hostel dates, two workbook layouts, free-text venues, repeat arrivals, non-round counts); two lost-to-follow-up rows with a later twelve-week result read as a plausible re-contact.
8. Forks: "courses that finished" against the pathway's "ends", for courses lost to follow-up (no stopped date): closed in the fix pass by the pathway's sentence that a course lost to follow-up has no last dose on record (SF20).
Sweeps: answer words harmless (the plan names the four candidates; no sentence pairs a setting with a figure); register dates harmless (planned ends of courses on treatment).

### Pass 2 (target.zip b93a12c2, after the fix pass that added the pathway's lost-to-follow-up sentence)

1. None, read literally: the plan fixes the arithmetic shell and never says how each setting's own share with an active infection is found.
2. None. 3. None. 4. None (the nurse's 70 courses is an operating constraint).
5. The plan's sentences fix one count per person per year, the two-year average from the providers' returns, found and started at the van's own RNA test and twelve weeks, the exclusion of people part-way through a course, and the pilot's test and start shares; the pathway fixes a course's end (completed, stopped, and none for a course lost to follow-up) and a confirmed cure as a laboratory event.
6. An analytical choice: each setting's own active-infection share among its arrivals, built from the register and the laboratory's records, nothing planted.
7. Realism good: metadata matches the issuing bodies, no hidden content, about 800 exact duplicate laboratory rows read as ordinary re-sends, irregular pilot counts.
8. Forks raised: the needle exchange arrivals from the pharmacies' paper registrations against the providers' returns (ruled out by the plan's "from the returns each provider sends the commissioners", call unchanged, asserted SF22); "finished" read as completed only against completed and stopped (the prompt now says "ended", the pathway's own word, asserted SF23); the register's keyed result against the pathway's laboratory test (the pathway defines a confirmed cure as the RNA test, which the golden reads in both records; the ask's hazard, not a fork).
Sweeps: all three harmless (the plan names the candidates; the workbook's and the register's late dates are planned course ends).

### Pass 3 (target.zip b93a12c2, after the prompt's "finished" became "ended")

1. The plan's "We will place the van where it starts the most people on hepatitis C treatment in 2027": the decision rule, not an outcome; no file names a winning setting or a figure.
2. None. 3. None. 4. None.
5. The plan's sentences fix the two-year average carried forward, one person once a year, started as the van's own RNA test and twelve weeks, the exclusion of people part-way through a course, and the pilot's two shares.
6. An analytical choice: each setting's own share of arrivals with an active infection, built from the linked testing and laboratory records; the exclusion of handovers is a linkage task, not a field read.
7. One mild tell: the laboratory's sibling requesting sites (16 GP practices, two antenatal, two sexual health, three drug service hubs) each carried near-identical counts. Fixed in the generator: each person keeps one site, and sites take shares by their size (practices from 1,865 to 9,633 samples); no graded figure moved (figures.json byte-identical), asserted as realism.sites_uneven.
8. Forks: the register's keyed twelve-week result against the pathway's RNA test read through the laboratory file. The pathway defines a confirmed cure as the RNA test, and the golden reads it in both records (the keyed result where there is one, the laboratory's first test twelve weeks on otherwise): the register-only reading is the ask's hazard (D4), not a licensed second reading. The city hostels and the approved premises sort cleanly. None on the main question.
Sweeps: all three harmless (the plan names the candidates and states only the rule; the workbook's and the register's late dates are planned ends of courses still open at the cut).

### Rulings (main thread)

- Question 1 in all three passes quotes the plan's filed comparison, the estimand's WHAT; no sentence names the decisive step. Harmless.
- Questions 2 to 4: none in all three passes.
- Question 5: every quoted sentence executes to the golden (asserted as SF1, SF2, SF5, SF8, SF11, SF13, SF20, SF22, SF23).
- Question 6: an analytical choice in all three passes.
- Realism: the one tell (even site counts) fixed in the generator; the lost-to-follow-up rows were re-contacts in pass 1 and carry no twelve-week result for people outside the settings since the fix.
- Forks: lost to follow-up (SF20, the pathway's sentence), the needle exchange arrivals' source (SF22, the plan), completed only (SF23, the prompt's ended and the pathway), the register-only cure (the ask's hazard D4).
- Sweep 4 (stump vocabulary, ruled here and never sent to the reader): the pathway and the plan carry the world's nouns and state true operational facts (the register holds the network's courses; Corvane provides healthcare in three prisons; the van takes on handovers in the approved premises); neither says an antibody outlives a cure or that a setting's positives were treated inside. Harmless.

