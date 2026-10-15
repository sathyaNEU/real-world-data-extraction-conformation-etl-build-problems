# leak check, task261

**Verdict: REVIEW.** 14 files read, 49 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: replicate, weights, errors, person, implicates, medians, bulletin, design, reference, quadrature, standard, estimates, asserted, committee, variance, estimate, clusters, decisive, recomputed, replicates, clustered, published, client, domain, implicate

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `retirement_range_2027_brief.docx`: golden figure 1.96 appears: ...een their median household net worth is more than 1.96 times the standard error of that difference. Wher...
- **REVIEW** `retirement_range_2027_brief.docx`: carries 4 of 6 distinctive words of the committed call: "Set Kelvane Life's 2027 retirement range on five segments: under 35, 35 to 44, 45 to 54, 55 to 64, and 65 and over."

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `nhws2025_user_guide.pdf`: 12 of 25 stump-paragraph terms appear (replicate, weights, errors, person, implicates, reference); read whether the document names the move
- **REVIEW** `retirement_range_2027_brief.docx`: 9 of 25 stump-paragraph terms appear (errors, person, medians, bulletin, reference, standard); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `lifetime_annuity_lives_20270112.csv`: 107 ISO dates after 2027-01-13, e.g. 2030-04-01, 2030-12-01, 2032-01-01, 2032-05-01, 2032-07-01

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
