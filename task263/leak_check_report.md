# leak check, task263

**Verdict: REVIEW.** 12 files read, 34 golden figures and 15 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: samples, sample, balance, sources, pumping, average, asserted, mixture, inventory, collection, records, blends, source, entry-point, beside, results, golden, register, decisive, proportions, sentence, mixing, nothing, environmental, mixtures

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: candidate 'Torvik Water Utility' sits beside decision vocabulary: ...FAS priority list Rank PWS ID System County Population served Priority points 1 4626844 Torvik Water Utility Hedstrom 6,538 92 2 4664327 City of Halvorsen Water Department Engvall 8,917 88 3 4...
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: carries 13 of 18 distinctive words of the committed call: 'The $36 million reaches 16 of the 20 systems on the 2027 PFAS priority list, Torvik Water Utility through Valdahl Sanita'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: 7 of 25 stump-paragraph terms appear (average, inventory, records, source, register, nothing); read whether the document names the move
- **REVIEW** `pfas_initial_monitoring_sampling_guide_rev2.pdf`: 11 of 25 stump-paragraph terms appear (samples, sample, sources, pumping, inventory, collection); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `monthly_operating_reports_2025.csv`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pfas_entry_point_results_2024-2026.csv`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pfas_field_collection_records_2024-2026.csv`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `source_facility_inventory_2026.xlsx`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `wholesale_connections_2026.csv`: names 8 of 15 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: each of the N: "How many of the twenty"; the N things: "the twenty systems" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'png+xlsx' at 21% of 196 prompts (cap 20%); reword at the role level, not the verb

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

Two isolated readers (Sonnet, medium effort), each with a fresh copy of prompt.txt and target/ and nothing else.

### Loop 1 (the first cut)

1. Decisive step: none stated. The plan's 6.3 ("A well's own water is the water the well itself pumps") and the
   guide's record fields name what a solver works from; the reader had to work out for itself that every result is
   an entry-point blend and each well's level has to be separated from the blends.
2. Ranking file: none. Table 6-1 orders the systems by priority points (the funding order the plan files); no file
   gives a grant, a reach or a well's level.
3. Analyst-only file: the department's transmittal note is the likeliest, and the reader judged it plausible as a
   real cover note.
4. Reads as the answer: nothing; the $36 million, $2.4 million per MGD and $6 million cap are inputs.
5. Literal sentence: 6.3 with 6.4; its literal execution is the golden's procedure (active wells, each analyte's own
   level over 4.0, rated capacity to MGD, the cap, the walk with a stop). The open points it named (non-detects, the
   averaging, the estimator) all converge on the same wells (checks SF3, SF14, SF16, convergence).
6. What decides: an analytical choice, unmixing each entry point's blends rather than giving a well the entry-point
   result.
Realism notes acted on: one style of invented name throughout, six counties statewide, priority points falling one or
two at a time, a percentage in the plan implying an unexplained base (all fixed, no graded figure moved).

### Loop 2 (after the fix pass)

The same six answers: no decisive-step sentence, no ranking file, nothing reading as the answer, the literal sentence
executing to the golden's procedure, Q6 analytical. Realism notes acted on: four stock remarks on the field records
(varied field notes added), every register row active (six closed systems added), every connection dated the first
of a month (days varied). Notes left as they are: samplers writing in their own style (each sampler's habit), sampler
ids rather than names (the department's export), facility ids issued in sequence, wells named Well 1 to Well n,
meter readings carrying over month to month (each is what the systems' own records hold).

### Verdicts on the REVIEW lines

- 3, the plan names the candidates beside decision words, and carries 13 of 18 words of the call: Table 6-1 is the
  list itself (rank, PWS id, system, county, population, points); it states no grant, wells or reach. Harmless.
- 4, stump-paragraph terms in the notes, the plan and the guide: domain words (samples, sources, collection,
  average); neither reader found a sentence naming the move. Harmless.
- 6, data files naming every candidate beside numbers: exports and the inventory at their own grain, no ranking on
  the decision. Harmless.

Verdict after the read: no LEAK; the decisive step is not stated anywhere in the pack; the deciding step is analytical
in both loops.

### Loop 3 (wave 3 audit: Ask B re-cut, ask 6 now "people living in the county ... any of those wells")

One isolated reader (Sonnet, medium) on fresh copies of prompt.txt and target/.

1. Decisive step: none stated. It quotes 6.3's own-water definition and the guide's sources-in-service field as what
   a solver works from; nothing says how a well's own level is obtained.
2. Ranking file: none (Table 6-1 orders the systems by priority only).
3. Analyst-only file: none clearly; the department's notes read as a covering email.
4. Reads as the answer: nothing; the $36 million and the 4.0 ng/L line are inputs.
5. Literal sentence: 6.3 with 6.4, executing to the golden's procedure (active wells whose own PFOA or PFOS averaged
   over 4.0 ng/L, rated capacity to MGD, the cap, the walk with a stop); the per-sample or per-day mean it raised
   leaves the same 23 wells (convergence, asserted).
6. What decides: an analytical choice (separating each well's own water from the entry-point blends), with cleaning
   around it; it could not tell without computing whether cleaning moves the call. It does not: every Layer 1 item
   mishandled leaves the same 23 wells and the same walk (R2, asserted).
7. County figures: (a) the listed systems' own populations against adding the systems that buy all their water from
   them (the "listed systems only" stop, under by 586 to 3,871; "get their water from any of those wells" takes in
   every full-purchase buyer), and "any of those wells" read as the wells over the line, which files the same
   figures (each of the twenty listed systems has a well over the line and a population is counted by system);
   (b) all the listed systems' wells against active wells only (the Kesselring emergency well, the judge's soft
   reading: the clause says "the listed systems' wells" where the chart sentence says "each active well").
   It named the wholesale chain, the buyers' counties, the inactive buyer ids and the meter register as what makes
   the county figures hard, without saying how any of them resolves.

Realism notes, each harmless: invented names in one Scandinavian-settled style beside English ones (the fiction's
state; H21 screened); register names in capitals (the state register's own style); ids stored as text in the
workbook (leading-zero ids); section 6 is a two-page extract of the draft plan (its file name says so); round
populations on a few systems (registers carry estimates); the notes state the export's row count (a transmittal).

Verdict after loop 3: no LEAK; nothing names the decisive step or either ask's device; Q6 analytical.

### Reship reads (2026-11-01, Sonnet at medium, fresh copies of prompt.txt and target.zip, the covering notes and the inventory's Notes sheet no longer shipped)

First cut (81d61969): the reader read the pump sentence the repair had filed at the end of the plan's 6.3 ("Well pumps in the state's community systems are constant-speed: a well pumps at its rated capacity whenever it runs.") together with 6.3's "A well's own water is the water the well itself pumps" as a mild hint toward recovering each well's water from the blends. The fact moved to the inventory's own `pump` column (every well constant speed), 6.3 went back to its shipped wording, and the plan keeps only the population-served note under Table 6-1.

Final cut (c38b7092): 1 none states the move (the nearest it names is 6.3's own-water sentence with the guide's sources-in-service field, read as pointing at samples where one well ran alone, the default path's own route); 2 none (Table 6-1 ranks by priority points, the funding order the prompt takes as given); 3 no dictionary, readme, manifest or notes sheet, the sampling guide and the laboratories list read as agency artifacts; 4 none; 5 the plan's 6.1, 6.3, 6.4 and the note under Table 6-1, and the guide's sections 5 and 7, each executed as written; 6 an analytical choice (each well's own water inferred from the entry-point blends), nothing planted. The pump column drew no remark. Its supplementary readings are settled per judge pass 3: the county water counts every well of the listed systems that pumped, Kesselring's emergency Well 3 included, since "active" governs only the grant and the chart; the county population takes each renumbered buyer at its active record; the non-detect convention moves no flagged well or grant; the wholesale buyers' customers are the ask's own step. Its realism notes (the placeholder geography, the QC ratios matching the guide, the identical analyte lists) are on files this reship did not change.

### Ask-rework read, 2026-11-02 (the cut 2c87c47f; the final cut 7a18885f changed only the operating reports' gallons)

One isolated reader on prompt.txt and target/ only, nothing computed. Questions 1 to 4: none (IUP section 6.3 files
the grant rule and "a well's own water", not how to recover it; no file ranks the systems or computes a grant; the
sampling guide is the programme's own procedure). Question 6: an analytical choice, each well's own water recovered
from the entry-point samples and the sources in service; the easy route, the entry-point average for every well,
is wrong. On the water ask: no shipped sentence or column says a well discharges through another's wellhouse (the
device silent); the register's common discharge headers are stated as written. Realism notes (recorded): invented
names, sequential facility ids, round populations, a short IUP excerpt. Verdict: clean.
