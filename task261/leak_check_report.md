# leak check, task261

**Verdict: REVIEW.** 14 files read, 49 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: replicate, errors, weights, person, medians, bulletin, implicates, design, asserted, quadrature, estimate, reference, committee, standard, variance, decisive, estimates, client, clusters, replicates, insurer, recomputed, domain, together, implicate

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `retirement_range_2027_brief.docx`: golden figure 1.96 appears: ...een their median household net worth is more than 1.96 times the standard error of that difference. Wher...
- **REVIEW** `retirement_range_2027_brief.docx`: carries 4 of 6 distinctive words of the committed call: "Set Kelvane Life's 2027 retirement range on five segments: under 35, 35 to 44, 45 to 54, 55 to 64, and 65 and over."

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `nhws2025_user_guide.pdf`: 12 of 25 stump-paragraph terms appear (replicate, errors, weights, person, implicates, estimate); read whether the document names the move
- **REVIEW** `retirement_range_2027_brief.docx`: 9 of 25 stump-paragraph terms appear (errors, person, medians, bulletin, estimate, reference); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (loop 0)

Isolated reader (sonnet, medium) on fresh copies of prompt.txt and target/ only.

1. Decisive step: no sentence names it. Nearest: the brief's placement ("A household is placed by the age of the older of its reference person and partner; a household with no partner is placed by its reference person.") and "Medians are weighted, and standard errors are estimated as the survey's user guide sets out." The brief states the placement rule, so it is not hidden.
2. Ranking file: none ranks the boundaries. The bulletin's Table 1 (then six groups by the reference person's age, medians and RSEs) gives no error of a difference and no verdict; a solver adding its RSEs in quadrature could reach a plausible wrong structure on the wrong basis, harmless if declared a wrong-basis distractor.
3. Files that only help: the user guide (section 7, the Queensland worked example), the data dictionary, the PDS and key facts (product terms for the asks), the customer research (context).
4. Answer-like figures: none; the bulletin's figures are on another basis and the guide's example is another quantity.
5. Filed sentence: the user guide's section 7 (an estimate on each implicate, averaged; 200 replicates on implicate 1; imputation variance at divisor 4; total = sampling + 1.2 x imputation) and the brief's rule (more than 1.96 times the standard error of that difference). The guide does not say how to get the error of a difference; applying the same recipe to the difference is a natural reading. Cannot tell the structure without solving.
6. What decides: an analytical choice, the older-partner placement and the difference's error from replicates and implicates rather than the bulletin's marginal RSEs or the two groups' errors added in quadrature; nothing planted. Noted risk: the brief and guide state the placement and the variance recipe nearly in full.
7. Data-handling phrase in the prompt: none ("placed by the age of its older partner at that date" is an estimand phrase; the register's deceased and merged records are left unstated).

REVIEW lines: the brief's 1.96, harmless (the committee's stated rule); the six group names, harmless (the setting, not a verdict); the user guide's terms, harmless (it gives an estimate's error, not a difference's); the brief's terms, harmless (states the rule and placement, not the move); the listing's later dates, harmless (deferred annuities' income start dates; no start date after the pull).

Realism tells: a few dates of birth on round days (1954-01-01, 1959-11-11), within chance; household totals summing exactly to the benchmark, plausible for a benchmarked survey; otherwise none.

Ruling: no fix for questions 1, 3 to 7; question 2 fixed in the generator (the bulletin regrouped to five age groups, 65 and over combined, so no six-group structure can be read from published figures; dataset-generation 8.3); re-read at loop 1.

## Solver's-eye read (loop 1, after the bulletin's regrouping)

Isolated reader (sonnet, medium) on fresh copies of prompt.txt and target/ only.

1. Decisive step: none names it. The brief states the test and the merge rule and that "standard errors are estimated as the survey's user guide sets out"; the user guide (7.2) gives the standard error of a single estimate only, so how to get the error of a difference is left open. No sentence names a pitfall.
2. Ranking file: none. The bulletin's Table 1 has five groups by the reference person's age, 65 and over as one; it cannot split 65 to 74 from 75 and over, gives no error of any difference, and a six-group structure cannot be computed from published figures.
3. Files that only help: the user guide and the data dictionary, ordinary documentation; the bulletin is context.
4. Answer-like figures: none; no file states a structure or an error of a difference.
5. Filed sentences: the brief's rule and placement, the user guide's 7.1, 7.2 and median definition. Read literally, the guide gives each group's median and error; applied to the difference, the replicate difference is taken replicate by replicate with the implicates' variance of the difference; 7.3's replicate design points the same way. Whether two errors added as independent give another structure cannot be told without solving. The reader left the fork-or-analysis question to the author.
6. What decides: an analytical choice, treating the two groups as independent (quadrature) or using the replicate and implicate structure for the difference; not planted. The older-partner placement is a filed definition built from the person file.
7. Data-handling phrase in the prompt: none.

REVIEW lines: all harmless (the committee's 1.96; the six group names are the candidate set; the guide never says how to obtain the error of a difference; the brief names no method; the listing's later dates are deferred annuities' income start dates, start dates all before the pull).

Realism tells: a round design (60 strata, two areas each, 200 replicates), plausible; the bulletin's 55 to 64 and 65 and over medians close (888 and 882 thousand), within survey noise; nominee names and client numbers acceptable; otherwise none.

Ruling: no fix. On question 5 the method is the stump, not a fork: the difference is itself an estimate, the user guide's method applied to it gives the golden, and the alternative (two errors added as if the groups were independent) is no reading of a filed sentence but an assumption the replicate weights refute (the 55 to 64 and 65 to 74 medians correlate 0.70 across the replicates); determinism-check section 1, HOW forced by the design.

## Solver's-eye read (loop 2, after the judge's r2 fix to the data dictionary)

Isolated reader (sonnet, medium) on fresh copies of prompt.txt and target/ only, the dictionary's two new sentences named.

1. Decisive step: none names it; the brief files the rule and the user guide the error of an estimate, nothing names the error of a difference or a covariance.
2. Ranking file: none; the bulletin's five reference-person groups cannot split 65 to 74 from 75 and over and give no error of a difference.
3. Files that only help: the user guide, the data dictionary, the bulletin as a sanity check.
4. Answer-like figures: none.
5. Filed sentences: the brief's placement and rule and the user guide's 7.1 and 7.2; not computable without solving.
6. What decides: an analytical choice (the difference's error from the shared replicates and implicates; the older-partner placement rebuilt from the person file); the reader noted the user guide gives the procedure step by step, the difference and covariance not spelled out.
7. Dictionary narration: mild, on the two new sentences ("A nomination stays current until the member replaces or revokes it, including after a nominee's death"; "Spouse or De facto partner (the member's partner)"): read as hints on using the nominations for a partner's age, and as authored for the task rather than a typical dictionary.

REVIEW lines: all harmless (as at loop 1). Realism tells: the brief's empty document title; the bulletin's two equal relative errors; the two new dictionary sentences.

Ruling: question 7 fixed in the generator; the two sentences rewritten as a dictionary holds them (the relationship codes defined, Spouse the member's husband or wife and De facto partner a person the member lives with as a couple; nominee details as the member gave them, not updated by the fund) and the register's household defined at a date (its partners alive on that date), which also closes the judge's deceased-partner fork in so many words; every figure unchanged; re-read at loop 3. The brief's empty title is the house template's (harmless); the bulletin's equal relative errors are rounded to whole per cents (harmless).

## Solver's-eye read (loop 3, the dictionary's second wording)

Isolated reader (sonnet, medium) on fresh copies of prompt.txt and target/ only.

1. Decisive step: none names it; the brief files the rule, the user guide its method, nothing says what the test shows or that the groups' medians covary.
2. Ranking file: none; the bulletin's five reference-person groups have no 65 to 74 and 75 and over split and no error of a difference.
3. Files that only help: the data dictionary; the user guide's worked example (it matches the bulletin's Queensland row).
4. Answer-like figures: none.
5. Filed sentences: the brief's rule and placement; each neighbouring pair's difference in weighted median net worth against 1.96 errors of it, households placed from the person file; not computable without solving.
6. What decides: an analytical choice; the reader itself took the two groups' covariance as zero "because the groups are disjoint", the easy route's belief, and named the bulletin's reference-person groups and independent errors as the shortcuts.
7. Dictionary narration: the register's household line (then "The household's partners at any date are those alive on that date") read as telling the solver to drop a partner who died before 31 December 2026; the nominations line mildly procedural, arguably a definition; the relationship codes a definition, nothing given away.
8. Realism of the reworded lines: the relationship codes and the nominations line read like a real fund's dictionary; the household line somewhat procedural.

Realism tells: the household line; the survey's tidy design (60 strata, two areas each, 200 half-sample replicates, five implicates) and the 1.2 factor; otherwise none.

Ruling: the household line is the household's definition at a date that the judge's r2 fork required filed, stated once in the ask files' own dictionary; it settles a hazard the cracker already handles and no primary device. The judge's r3 then read that line as limiting a household's partners to register clients and asked for the source of a partner who is not a client to be filed: the line now reads "A household's partners at any date, our clients or not, are those alive on that date", and the nominations file's About line says a member's spouse or de facto partner who is not a client is known only from the nominations; the nominee placement is thereby filed and stops being a silent device (every ask stop and the cracker's path still miss every Ask A and B figure, asserted). The survey design is a standard paired-area replicate design and the 1.2 factor is 1 + 1/5 for five implicates, harmless. Re-read at loop 4 on the final wording.

## Solver's-eye read (loop 4, the partner filed)

Isolated reader (sonnet, medium) on fresh copies of prompt.txt and target/ only.

1. Decisive step: none; the brief names the user guide for the errors and neither says where the boundaries fall.
2. Ranking file: none; the bulletin's five coarse groups give no six-group split and no error of a difference (context that could nudge a solver to merge from 55).
3. Files that only help: the user guide and its worked example.
4. Answer-like figures: none.
5. Filed sentences: the brief's placement and rule, the user guide's 7.2; a test of each neighbouring pair's difference in weighted medians; not computable without solving.
6. What decides: an analytical choice (the older partner from the person file; the error of a difference of medians across the implicates and replicates); nothing planted; the customer figures lean on semantics, in the asks.
7. The dictionary bears on the main question: none (it covers the customer files only).
8. The dictionary's household lines, probed for a second reading: a nominee's death is not recorded for a non-client (read as alive, or ignored as unverifiable); a stale nomination as evidence of a partner; which nomination types the non-client partner line covers; a merged record's household; a nomination effective after 31 December 2026.

Realism tells: the nominations line reads as an author's pointer; the survey's replicate design and the user guide's worked example look constructed; the research summary's "preferences, not finances" line; the brief and the dictionary very clean.

Ruling: questions 1 to 7 clean. Of question 8, the nomination types are closed in the text (the non-client partner line now ends "whatever their type"); the rest are closed by the records and need no sentence: a single-client member who names a spouse or de facto partner is always recorded Married or De facto and never with two partners (asserted), effective dates all fall before December 2026, merged numbers resolve through the register's merged_into (a hazard the cracker repairs), and nothing marks any non-client nominee dead, so the only reading of the records is the nominee alive at 31 December. The realism tells are the price of the judge's filed convention (the nominations line) or the survey's standard design, harmless. Re-read at loop 5 on the final wording.

## Solver's-eye read (loop 5, the nomination types filed)

Isolated reader (sonnet, medium) on fresh copies of prompt.txt and target/ only.

1. Decisive step: the reader quoted the brief's rule and the user guide's 7.1 to 7.3 as the procedure; neither names the error of a difference, a covariance or shared areas.
2. Ranking file: the bulletin's Table 1, then by the reference person's age in five groups (55 to 64 at $888,000 and 65 and over at $882,000), read as a partial ranking on the wrong basis; nothing ranks the brief's neighbouring pairs.
3. Files that only help: the user guide and its worked example, the data dictionary.
4. Answer-like figures: the bulletin's Table 1 medians, on the reference person's basis with 65 and over merged.
5. Filed sentences: the brief's rule with the user guide's method; not computable without solving; the reader took the bulletin's 888 against 882 as a hint that 55 to 64 and the older groups share a segment.
6. What decides: mostly an analytical choice (the older partner from the person file, the error of a difference of medians); nothing planted.
7. The dictionary's household, nominations and relationship lines: largely determinate; residual probes on a nominee who is also a client (none in the data: every spouse nominee in a two-client household is the other client, asserted), a stale nominee against the register's marital status (none: every single-client member naming a partner is recorded Married or De facto, asserted) and merged member numbers (resolved through merged_into).

Realism tells: the bulletin's 55 to 64 and 65 and over medians nearly equal, a visible nudge; the documents tidy; otherwise none.

Ruling: question 2, 4 and 5 fixed in the generator. A wrong-basis distractor's own answer may be neither the golden nor rung 0's (dataset-generation 8.3), and the bulletin's five groups, their errors added, gave rung 0's four segments (55 and over as one). The bulletin's Table 1 now uses the centre's ten-year bands from 30 (under 30 to 70 and over) by the reference person's age, none sharing a boundary with the brief's groups (asserted), so no structure for the brief's groups reads off it; it stays declared, ruled out by the brief's placement. Every figure unchanged; re-read at loop 6. Question 7's residual readings are closed by the records (asserted) and need no sentence.

## Solver's-eye read (loop 6, the bulletin's bands moved)

Isolated reader (sonnet, medium) on fresh copies of prompt.txt and target/ only.

1. Decisive step: none; the brief states the rule and the placement, the user guide the error of an estimate; no file says which boundaries survive the test.
2. Ranking file: none; the bulletin's Table 1 runs under 30 to 70 and over by the reference person's age, its bands do not map onto the brief's groups, it gives no difference or error of one, and no segment membership can be read off it.
3. Files that only help: the user guide and its worked example, the data dictionary, the bulletin as a check on the estimation; the customer research reads as a distractor.
4. Answer-like figures: none.
5. Filed sentences: the brief's weighting and error sentence, the user guide's 6, 7.1, 7.2 and median definition, the brief's placement; read literally they give each group's estimate and, for each neighbouring pair, a difference with its error against 1.96; the guide's recipe applied to the difference closes how; not computable without solving.
6. What decides: an analytical choice (the older-partner age rebuilt from the person file; each pair's difference estimated jointly over the replicates and implicates); not one field, a planted item or a stated rule alone.

Realism tells: none strong (the bulletin's bands differing from the brief's read as the survey's own tabulation).

Ruling: no fix. The stage 4 reads end here: nothing names the decisive step, no file ranks the boundaries, every question-5 sentence executes to the golden.

**Reader (wave 3 audit, after the asks' re-cut).** Q1 none (the brief's rule and the guide's section 7 give the standard and the error of an estimate, never the error of a difference or the groups' covariance); Q2 none (the bulletin's ten-year bands from 30 by the reference person, context); Q3 the user guide, the dictionary and the brief as ordinary supporting files; Q4 none; Q5 the guide's variance formula applied to the difference, the combination left open; Q6 an analytical choice (the unit and the error of the difference). Q7 on the book: the partner known only from nominations, stale nominations, deaths after 31 December, deferred annuities, the January increases, the reversionary life's status; each settled by the dictionary, the PDS or the fact sheet, and none of the cut's two silent devices named. Q8 none planted; the dictionary's partner notes read careful rather than placed. Every REVIEW line harmless.
