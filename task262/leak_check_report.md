# leak check, task262

**Verdict: REVIEW.** 14 files read, 32 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: census, history, variance, family, families, transitory, reliability, filers, spread, carries, population, sample, measured, halverston, selvane, valley, five-year, decisive, foundation, centre, extract, torvale, correction, cracker, covers

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `opportunity_pathways_brief_2027.docx`: candidate 'Opportunity Pathways' sits beside decision vocabulary: ...The board meets on 26 November to choose the region for the first three years of Opportunity Pathways (2027 to 2029). As agreed at the September retreat, the program goes to one region: the r...
- **REVIEW** `opportunity_pathways_brief_2027.docx`: carries 3 of 5 distinctive words of the committed call: 'Opportunity Pathways goes to Selvane Valley in 2027.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `bridges_close_out_summary_2024.pdf`: 3 of 25 stump-paragraph terms appear (foundation, centre, covers); read whether the document names the move
- **REVIEW** `linked_extract_user_guide_2026.pdf`: 7 of 25 stump-paragraph terms appear (census, history, families, carries, population, centre); read whether the document names the move
- **REVIEW** `opportunity_pathways_brief_2027.docx`: 5 of 25 stump-paragraph terms appear (census, family, foundation, centre, extract); read whether the document names the move
- **REVIEW** `youth_aspirations_survey_2023.pdf`: 6 of 25 stump-paragraph terms appear (family, halverston, selvane, valley, foundation, torvale); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 3)
- **REVIEW** `regional_economic_indicators_2021.xlsx`: names 6 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `bridges_offices.csv`: names 6 of 8 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `region_recode_2001_2021.csv`: names 6 of 8 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `youth_aspirations_survey_2023.pdf`: names 6 of 8 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read, loop 1

One isolated reader (Sonnet, medium effort) saw only fresh copies of prompt.txt and target/.

1. **Decisive step named?** None. The nearest text is the brief's estimand ("the slope of the logarithm of a child's
   earnings as an adult on the logarithm of the parents' long-run income, across every child of the region. A
   family's long-run income is the level its yearly income moves around from one year to the next"), which fixes the
   estimand, not the step; the user guide's section 3 states the history's coverage as a plain fact.
2. **A file ranking the regions on the question?** None. The regional economic indicators and the aspirations
   survey rank nothing on persistence; no file holds an elasticity.
3. **A file that only helps the analyst?** None. The guidelines' counting and spending rules are the Bridges asks'
   governing text (the WHAT).
4. **A figure or name reading as the answer?** None.
5. **Literal execution.** The reader computed the history's five-year average among the families that have it
   (Halverston 0.345) and the census year for every child (Torvale Metro 0.332), and noted that the brief's "across
   every child of the region" cannot be met by the history reading alone and that one census year is not the level
   income moves around: each easy reading violates a quoted clause of the brief, and neither is the golden.
6. **What decides the main answer?** "An analytical choice": how to estimate the elasticity on long-run income when
   the multi-year history covers a regionally selective subset (27 to 91 per cent) and the census year is a noisy
   proxy. No sentence announces it and no field reading flips it.

Realism notes and what was done:
- The brief carried the writing library's template parts (a thumbnail, a Word 2010 effects stylesheet, SharePoint
  custom XML): stripped in the generator, with their relationships and content types, and Word's XML declaration
  written on every part.
- The data dictionary was one line per column: it now carries each column's type, unit and notes (universe, codes,
  zero and negative values).
- The central cost centre's licence, system and evaluation lines were booked to "Materials": now "Systems" and
  "Professional services".
- Plans still open at the program's end showed "Active": the brief now says the participant export was taken when
  the program closed, and the close-out says plans still running on 31 December 2023 ended with the program, each
  with a final bursary.
- Kept as they are: whole-dollar earnings and complete year rows (the guide records a year without a return as
  zero, and the history holds only families with all five years); the close-out's follow-up count (a survey summary
  that ships no survey file); the central cost centre's net negative mentor fees (the year-end reversals, the ask's
  device, found by exactly this inconsistency).

Verdicts on the REVIEW lines: the brief's program name and call words are the program's own name (not an answer);
the guide's and the brief's data terms describe the sources, not the move; the aspirations survey names regions in a
table of plans after school; the regional economic indicators publish medians and rates, not persistence (a declared
distractor). No line hands over the decisive step.

## Solver's-eye read, loop 2 (after the realism fixes)

A fresh reader on the rebuilt pack: no sentence names the decisive step; no file ranks the regions on persistence;
nothing exists only to help the analyst; nothing reads as the answer. Literal execution: the history's five-year mean
among the families that have it names Halverston (0.345) and the census year for every child Torvale Metro (0.332);
the reader noted the tension with "across every child of the region" (the history reading drops 24,278 of 58,202
children), which is the default path and the stump, ruled out by the brief's population. What decides: "an
analytical choice". Realism: the brief's app.xml still carried the writing library's statistics (no words, no
characters, the company appended out of order), now written as Word writes them with the document's own counts; the
aspirations survey's stated respondents did not add up to its table (now the table's total). Kept: a dictionary
drafted before its release date, the close-out's follow-up count, plans open at the close.

## Solver's-eye read, loop 3 (the final pack)

### 1. Decisive analytical step
No sentence names it. The nearest text is in opportunity_pathways_brief_2027.docx: "A family's long-run income is the level its yearly income moves around from one year to the next." It defines the concept without saying how to measure it. The user guide says census income is a single year ("total income in 2000") and that the history covers only families in which a parent filed in each of 2001-2005 ("Families in which no parent filed in one of those years are not in the history. The history holds 25,290 families."). A solver would infer that the five-year history is the long-run measure and the census figure is not. Nothing says what to do about the children whose families are missing from the history. The brief's "across every child of the region" pulls the other way. Neither the guide nor the brief states a rule for this, so the choice is left to the solver. Nothing in the files announces the choice.

### 2. Files that already rank or score the regions
None ranks regions on the elasticity question.
- regional_economic_indicators_2021.xlsx has levels (income, low-income rate, unemployment, credential, median age), not mobility. The aspirations survey PDF has stated plans by region and says it "asked about plans and worries, not about family income". Both are context and distractors, and neither points to a winner.
- The Bridges ledger and participants files carry only program counts and spending.
- No file contains an elasticity. Every region's elasticity has to be computed.

### 3. Files that exist only to help the analyst
None. There is no answer key, hint, worked method or note naming a trap. All fifteen files read as source documents. The brief's one definitional sentence on long-run income is the closest thing to guidance. The Bridges guidelines (section 4: "counted once, as a start in the region of the office where they first enrolled"; central team's costs "shared among the regions by the number of young people each started") are a stated rule. That is a rule for the ask, not a hint for the main call.

### 4. Figures or names that read as the answer
None. No region is named as the target and no elasticity is stated anywhere.
- The brief's "the region where children's earnings as adults depend most on their parents' long-run income" repeats the prompt's wording.
- The close-out gives program totals only ($6,908,544; 2024 spend $44,816). These match the ledger sum exactly, so they are context and not an answer.

### 5. Sentence that fixes the computation, and the literal result
The filed sentences are in the brief. Elasticity is "the slope of the logarithm of a child's earnings as an adult on the logarithm of the parents' long-run income, across every child of the region". The children are "born from 1984 to 1988 who lived with a parent in the region at the 2001 census ... a child counts where the parents' census income was above zero and the child had earnings in at least one year from age 30 to 34". Earnings are "the average of the yearly earnings at ages 30 to 34 in constant 2005 dollars, a year without earnings counting as zero". Long-run income is "the level its yearly income moves around".

I computed with CPI to 2005 dollars, ages 30-34 as tax_year minus birth_year, and the 2021 region names from the recode. Every child has five years in the window. 7 children have no earnings and 232 have census income of zero or below. Everyone with any earnings has a positive mean.

| Region | A. Census 2000 income, all filing children | n | B. 5-year history mean (children with a history) | n | C. Census income, history-family children only |
|---|---|---|---|---|---|
| Caskell Coast | 0.150 | 5,549 | 0.257 | 2,420 | 0.123 |
| Danholt Lakes | 0.232 | 7,726 | 0.298 | 4,326 | 0.195 |
| Halverston | 0.286 | 6,868 | **0.345** | 5,721 | 0.279 |
| Kestry North | 0.181 | 4,220 | 0.195 | 1,642 | 0.076 |
| Ostler Plains | 0.215 | 7,152 | 0.298 | 6,484 | 0.208 |
| Selvane Valley | 0.229 | 6,106 | 0.242 | 4,714 | 0.113 |
| Torvale Metro | **0.332** | 15,320 | 0.289 | 7,189 | 0.206 |
| Wendmoor | 0.153 | 5,261 | 0.234 | 1,428 | 0.074 |

- Reading A (the census single-year figure applied to "every child") makes Torvale Metro highest at 0.33. It is not the concept the brief defines.
- Reading B makes Halverston highest at 0.34 or 0.35 (0.345 before rounding, so the second decimal is sensitive). The ranking is not stable across the readings. The most literal reading of "long-run income" is B, because only the history has several years.
- The brief never says how to treat the 33 or so thousand children without a history. Whether they are dropped, and whether the history is a selected subset, is left open. History coverage varies a lot by region. Ostler Plains has 6,484 of 7,152 children, while Kestry North has 1,642 of 4,220 and Wendmoor 1,428 of 5,261.
- Bridges, read literally per the guidelines, needs the ID or cross-system mapping to count first enrolments only. Raw rows by office (all rows) give TVL 377, DAN 236, OST 208, SEL 194, HAL 183, CAS 157, KES 151, WEN 134 (1,640 rows in total). Excluding rows with a transfer_from gives 1,586 rows and 373, 229, 199, 184, 177, 151, 145, 128 by office. That count still includes the Northstar migration re-keys (below), so it overstates. Ledger by cost centre (dollars, all postings 2019 to 2024): CAS 632,287; CEN 623,430; DAN 878,276; HAL 757,296; KES 630,475; OST 781,371; SEL 737,873; TVL 1,301,059; WEN 566,479. The central team's costs (CEN) are shared by starts.

### 6. What decides the main answer
An analytical choice. The decision turns on how long-run income is measured and which children the slope rests on. Using the single-year census income gives Torvale, using the five-year average gives Halverston. The census figure is a noisy single year and the history is a selected subset of families, so the choice is about estimand and sample. No single field, code or unit decides it: the CPI conversions and the age window are stated, and the region recode is trivial. The brief's one defining sentence ("the level its yearly income moves around") is the only text bearing on it. It does not prescribe a procedure. The picked procedure is not a planted decoy, since the census-income route is a legitimate-looking choice and not announced as wrong.
One caution: the brief and the guide together make the five-year history the obvious source for "long-run income", and an observant solver may take that route without noticing the selection. The brief's "across every child of the region" does not tell them what to do with the missing-history children.

### Realism and consistency notes
- The DOCX has no comments, tracked changes or hidden text. Its core properties give the creator as Monique Webb with Word metadata (Normal.dotm, Company Wrenmore Foundation). The created and modified dates (4 and 6 Nov 2026) match the memo's date of 6 November 2026. The memo text is plausible for a foundation.
- Both XLSX files have one visible sheet each for the economic indicators and six for the dictionary, with no hidden sheets or comments. The dictionary's core properties name Lawrence Ferguson, matching the contact in the user guide. Creation date 2026-05-28 precedes the 22 June 2026 release, which is plausible. The indicators file is attributed to "Research and Evaluation" at the foundation.
- The close-out says that "624 young people answered the six-month follow-up; 72 per cent of them were in work, training or study", but I could not verify that from any file, and no file holds follow-up data. This is minor.
- The close-out cites the April 2021 system change ("went smoothly... the offices kept every open plan going through it"). The participants file shows otherwise. Northstar rows start 2020-03-30 (earlier than April 2021), and the Northstar P-prefixed refs match CaseTrack rows on date of birth, office and intake date (for example P104204 = BR-20-0053, TVL, 2020-03-30). That is, open plans were re-keyed with new refs and no cross-reference, which inflates a raw count. The close-out's reassurance sits in tension with the data. It is realistic as an organisation's self-description, and it is the dataset's Layer 1 mess. It does not announce the dedup step.
- The brief and the user guide agree on the cohort. Guide: 58,441 children (file has exactly 58,441 unique children), 25,290 families in the history (matches), 43,407 families (not checked). Aspirations survey respondents add to 1,976 as stated. No internal inconsistency found in those.
- Mildly odd: the user guide states the long-form questionnaire went to one household in five "drawn at the same rate everywhere" (so no weights). It fits the data but reads as an author's reassurance.
- The Bridges ledger has 4 negative postings, no duplicate journals, and 21 Systems rows. The PDFs and CSVs read as plausible administrative products. I saw nothing that reads as machine-generated beyond the generic region names.

## Verdict on the reader loops

No reader found a sentence naming the decisive step, a file ranking the regions on the question, a helper file or an
answer figure, and every loop judged the deciding step an analytical choice. Each loop's literal computation landed on
the default path (Halverston, the filers' five-year averages) or on the census year as it stands (Torvale Metro); both
are rungs of the ladder, each ruled out by a quoted clause of the brief (every child of the region; long-run income as
the level yearly income moves around), and the determinism judge executed the same text to the golden. Realism tells
found in loops 1 and 2 were fixed in the generator; loop 3 found none.

### Read of 2026-10-31 (reship under the 10-30 gates, pack 14 files)

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and `target/`; it did not solve the task.

1. Decisive step: none; the brief's definitions and the guide's coverage lines point at the data's structure and name no step.
2. Ranking file: none (the regional indicators and the aspirations survey are per-region context, no elasticity or ordering).
3. Helper-only file: none (the recode, office list and price index are plain lookups).
4. Answer-like figure or name: none.
5. Literal sentences: the brief's elasticity across every child of the region and its earnings definition, and the 2019 guidelines' start and cost-sharing rules for the asks: each files the WHAT.
6. What decides: an analytical choice (reaching every child from the one-year census income and the partial history); nothing planted.

Item rulings: the brief and the regional indicators harmless. Realism: the brief reads as a full specification (mild); the close-out's "as posted" line and the guide's "No boundary changed" read as designed to the reader, both outside the main call and kept; no LLM tells.
