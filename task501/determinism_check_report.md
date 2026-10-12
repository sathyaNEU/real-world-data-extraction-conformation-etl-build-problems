# Verdict, task501 (judge-task501c)

**Verdict:** NOT_DETERMINISTIC, narrowly. The main recommendation (fund B) and every figure except three cells of supplementary ask 4 reproduce exactly. Label: competing_defensible_answer (supplementary ask 4, options C, D, E). Fix location: input_files.

**Disposition:** SEND_BACK (light). Close the six `Open` rows in gp_return_queries_mmr_2005-2027.csv (give each an outcome), or state a rule for them, then regenerate the ask-4 figures. This touches shipped data, so a rerun is needed. The main call, the R figures, asks 3 and 5 and the deck are unaffected.

**Why:** Three `Open` GP-return queries sit on loaded events for people in the option cohorts: GPR-202704-GP4595-001, GPR-202704-GP3925-001 and GPR-202704-GP4195-001. The golden keeps them, because only "Replaced by corrected line" and "Withdrawn by practice" are dropped. No shipped text says what to do with an unresolved query. Dropping them is equally defensible and moves C none/one 2,859/3,960 to 2,860/3,959, D one 7,302 to 7,304 (none unchanged at 4,971) and E one 11,788 to 11,790 (none unchanged at 8,530). Whichever way the dose figures land, they are not forced. The main call is forced by the files (B 0.89 against 1.29 to 1.31 for everything else).

## Evidence (recomputed from the bundle)
Literal reading first, then recomputation.

| Quantity | Result | Source | Reproduced |
|---|---|---|---|
| Susceptible share 15-19 on 1 Jan 2028 | 11.22% (age = 2027 - birth year, per the projection file) | population_projection + immunity_profile | yes (11.2) |
| Susceptible share, region | 5.408% | same | yes (5.4) |
| R, no catch-up (dominant eigenvalue of c_ij x s_j, scaled so s=1 gives 15) | 1.311 | NSCS Table 2 | yes (1.3) |
| R under A / B / C / D / E | 1.291 / 0.888 / 1.305 / 1.302 / 1.298 | made-immune from options paper removed pro rata from the option years' susceptibles | yes (1.3 / 0.9 / 1.3 / 1.3 / 1.3) |
| Residents 30 Jun 2027 (active, LHO read in the scheme in force on lho_recorded; LH27 before 1 Jul 2024 = Monaghan West) | A 35,346; B 33,217; C 29,398; D 30,625; E 57,865 | register_people + circular 03/2024 | yes, all five |
| No valid dose / exactly one | A 3,542/4,724; B 4,285/6,094; C 2,859/3,960; D 4,971/7,302; E 8,530/11,788 | events re-pointed through merge chains (3,946 events), replaced/withdrawn GP lines dropped (652), doses before first birthday, under 28 days, or after 30 Jun 2027 not counted | yes, all ten (Open queries kept) |
| Confirmed cases 2019-01-01 to 2027-06-30 / imported | A 9/2; B 10/2; C 11/3; D 10/3; E 16/5 | NDS cases, 32 back-entered 2019 records matched to migrated ones by legacy number and counted once; "Imported" only | yes, all ten |

Variants and what they give:
- Naive 2024 scheme (LH27 treated as Midlands): A 34,588 etc. Wrong, but the circular fixes the reading.
- Merges not re-pointed: one-dose counts inflate (B 6,753), so re-pointing is needed.
- Not dropping the replaced/withdrawn lines: B 4,274/6,074, so the query log matters.
- Counting the back-entered duplicates twice: A 15, B 14 and so on. The legacy numbers settle it.
- The two copies of a pair disagree on day/month of birth and sometimes on onset date, but never on birth year, classification or importation, so the counts do not depend on which copy is used.
- Counting "Import-related" as imported would make every case imported, but the NDS field notes define it separately, so "imported" is the literal Imported value.

Main-call forks:
- Homogeneous mixing, R = 15 x 0.0541 = 0.81, gives "no catch-up needed". The prompt and PS-07 do not name the age-structured method. The shipped Table 2 contact matrix, the immunity profile by year of birth and the 5-year age groups strongly force it, and the golden is the only reading that uses the matrix. This is a residual risk, not a failure, but a one-line pin ("the department's age-structured contact model") would remove it.
- Transposing the matrix, scaling by row or by column, and splitting E's made-immune across its two age groups all leave every R at the same 1 dp value.
- Off-by-one age mapping (using 2028) gives 1.245 and 0.904 and other wrong values, but the projection file labels age against birth year (age 0 = 2027), so it is closed.
- Cost tie-break (PS-07 3.6) is moot because only B is below one.

## Files/Hygiene: PASS
20 files, in csv, pdf, xlsx, docx and txt. Two files are large (22.9 MB events, 9.5 MB people). Distractors present and unused: stock return, uptake report, NMRL results, LHO code list as a trap for the old scheme. No authoring or provenance leakage found, and dates are coherent (extract 3 Jul 2027, options paper 9 Jun 2027, transmittal 12 Jul 2027). The options paper's lists for options D and E are slightly odd (E restates D's 1993-1997 row), but internally consistent. Not exclusion-level.

## Stump power
Good. The easy routes both give a wrong main call: homogeneous mixing gives 0.81 (no catch-up), and ranking by people made immune or by the largest susceptible cohort picks E (2,890) or D (1,980). Only the age-structured eigenvalue shows that teens (15 to 19, with the highest within-group contact, 7.9 a day) carry the transmission, so B alone works. A strong model plausibly falls for either route.

## Stumping type
`mechanism: method_or_model_selection` (age-structured next-generation matrix against homogeneous mixing), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported inputs are all fine, and on clean data the task still stumps. The register, merge, query-log and case-dedup work are lower-layer messy-data steps feeding the asks.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails as it should, because a next-generation matrix with an age-specific contact survey and a catch-up cohort is the infectious-disease modelling the field does. Layer 1 is the LHO recode, merges, query log and legacy case duplicates, and Layer 2 is the age-structured reproduction number. The easy route, 15 x 5.4% = 0.81, gives "no catch-up".

## Fix
input_files: resolve or rule on the six `Open` rows (three bite), or add a filed sentence saying unresolved queries stand. Consider a one-line prompt pin for the age-structured method. Then regenerate ask-4 figures and rebuild.

## Disposition

Fixed in one generator pass by the build session and committed PAUSED for the main session's re-judge (the judge's light
send-back, location input_files). The main call (option B), the stump, the ladder, the six reproduction numbers and every
graded ask figure are unchanged: `freeze.py check task501 --mode determinism` PASS.

1. **The ask fork (supplementary ask 4; the design note's Ask 2, fork row SF17).** Closed in the data, as the register
   would close it, with no document edited. The register now chases every query a practice had confirmed but the office
   had not closed when the 30 June extract was prepared, and closes it by the as-at date with its outcome. The six `Open`
   rows are now:

   | Query | Line | Raised | Outcome | Closed | On a loaded event |
   |---|---|---|---|---|---|
   | Q27-11855 | GPR-202703-GP4806-091 | 2027-05-19 | Confirmed as sent | 2027-06-22 | no |
   | Q27-11858 | GPR-202704-GP4595-001 | 2027-05-26 | Confirmed as sent | 2027-06-11 | yes |
   | Q27-11859 | GPR-202704-GP4195-001 | 2027-05-30 | Confirmed as sent | 2027-06-16 | yes |
   | Q27-11860 | GPR-202704-GP1313-032 | 2027-06-21 | Confirmed as sent | 2027-06-28 | no |
   | Q27-11861 | GPR-202704-GP3925-001 | 2027-06-21 | Confirmed as sent | 2027-06-30 | yes |
   | Q27-11862 | GPR-202705-GP1942-025 | 2027-06-21 | Confirmed as sent | 2027-06-30 | no |

   Every query in the log now has an outcome and a closing date on or before 30 June 2027, so no line is under an open
   query. The three lines that bit stand as the golden counted them, and the ten ask-4 figures are unchanged (C
   2,859/3,960, D 4,971/7,302, E 8,530/11,788). The drop reading (C 2,860/3,959, D one 7,304, E one 11,790) now goes
   against the log, which shows each of those lines confirmed as sent. Asserted in `checks.py` (SF17): no query open;
   every query closed after it was raised and by 30 June 2027; dropping every line not closed as confirmed by then moves
   no ask-4 figure; the chased queries on extract lines are exactly the three named above, and dropping them would have
   moved C by 1 and D and E by 2. `verify.py` recomputes the dose counts under that reading on its own code path.

2. **The optional method pin.** Declined. No prompt or standard sentence names the age-structured method, because the
   data forces it: Table 2's contacts by five-year group, the profile's immunity by year of birth (PS-07 3.4), the
   projection by age and year of birth on the assessment date (3.3) and R0 for the region with nobody immune (3.2).
   A pin would file the decisive step as a rule to execute. The judge rated this a residual risk, not a failure.

3. **Realism (this report's Files/Hygiene note and the leak reader).** Presentation only, no figure moved:
   - `mmr_catch_up_options_autumn_2027.pdf`: option E is one row (born 1993 to 2002, 67,249 people, 7,441 estimated
     susceptible, 40% expected uptake, 2,890 expected made immune, EUR 459,000). The note under the table gives its split:
     "Of option E's 2,890 expected people made immune, 1,980 are among those born 1993 to 1997 and 910 among those born
     1998 to 2002." E no longer restates D's row. Paragraph 4.3 now says invitation lists for the option funded will be
     drawn from the register.
   - `nscs_2023_published_tables.xlsx`: Table 1's population column carries the statistics office's estimates by group,
     5,186,322 in all. Table 2's values are unchanged and still reciprocal on Table 1 to their two-decimal rounding. The
     weighted shares are unchanged.

4. **Rebuild and free gates.** `checks.py` 212 PASS; `verify.py` PASS; two builds byte-identical; `figures_check.py`
   exit 0; `precut.py` exit 0; `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK, sweep 11 clean); `guard.py surface`
   0 hard tells; `guard.py heart` PASS. Changed under `target/`: the query log (six rows), the options paper and the
   survey workbook. Every other pack file, both goldens, `figures.json` and `submission.md` are byte-identical. The
   leak reader re-reads the two changed documents before the re-judge.
