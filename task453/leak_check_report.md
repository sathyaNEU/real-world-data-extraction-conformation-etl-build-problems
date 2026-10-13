# leak check, task453

**Verdict: REVIEW.** 11 files read, 54 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: seasonal, change, workplace, pattern, series, january, months, statistics, rejected, placement, adjusted, account, returns, estimated, decisive, history, golden, monthly, seasonally, capital, adjustment, step-aware, asserted, design, employer

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `regional_rapid_response_program_regulation.pdf`: carries 8 of 9 distinctive words of the committed call: 'Certify Brennick Valley, the Capital and Pellmarsh Hills as designated for the first quarter of 2027.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `pra_release_note_place_of_work_2026-02.pdf`: 8 of 25 stump-paragraph terms appear (change, workplace, january, months, statistics, account); read whether the document names the move
- **REVIEW** `pra_transmittal_2027-05-07.txt`: 7 of 25 stump-paragraph terms appear (workplace, january, months, statistics, returns, monthly); read whether the document names the move
- **REVIEW** `regional_rapid_response_program_regulation.pdf`: 13 of 25 stump-paragraph terms appear (seasonal, workplace, january, months, statistics, adjusted); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Set out the certification in rapid_response_certification_2027q1.pdf, with the figures the Regulation requires for each certified region and a chart setting every region against the line, and list every region in regiona'

## 6 ranking artifacts (REVIEW 3, INFO 1)
- **REVIEW** `bsea_municipal_concordance.xlsx`: names 9 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `lfs_economic_region_estimates_2025-2027.csv`: names 9 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pra_workplace_returns_2026-03_2027-03.csv`: names 9 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `regional_rapid_response_program_regulation.pdf`: names 9 of 10 answer-set candidates; confirm it does not rank them on the decision question

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

### Pass 1


1. Decisive step: none announces it. Closest: Regulation s.2(1) "An economic region is designated for a quarter if its seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its payroll jobs for the preceding calendar year." It names the test but not how to get from the files to a comparable series. The release note (pra_release_note_place_of_work_2026-02.pdf) says "The change moves payroll jobs between municipalities and between economic regions" and "Statistics for reference months before January 2026 have not been revised", which tells a solver the series breaks but not what to do. The transmittal says the revision "replaces those three months in the April file". None says "rebuild the history on a workplace basis" or "seasonally adjust X way". Mild tilt: the release note makes the place-of-work break obvious; that is organisational context, not an instruction.

2. No file ranks or scores regions on the question. The concordance lists municipality to region; the LFS csv (employment_thousands, rates) is monthly levels by region with no comparison to a line or a designation; population file is by municipality. No designation list.

3. No hint/worked-method file. All files read as agency or bureau documents. The transmittal and release note are organisation-authored. LFS and population files are distractors (unused by the Regulation test).

4. Nothing reads as the answer. No region is flagged. The Regulation Schedule lists the 10 regions only.

5. Literal sentences:
 - s.1(1) "payroll jobs of an economic region for a month means the jobs on the monthly returns that employers file with the Agency for the month at workplaces in the region's municipalities": place-of-work basis, municipalities placed by the bureau concordance (Wexleigh 0803 and Dorran 0806 merged to 0814 from 2025; monthly csv has 45 municipality codes incl. 803/806 for 2024, revisions have 43).
 - s.1(2) "An economic region's payroll jobs for a quarter are the average of its payroll jobs for the three months of the quarter, and ... for a calendar year are the average of its payroll jobs for the twelve months of the year": quarter = mean of Jan, Feb, Mar 2027; preceding year = mean of the 12 months of 2026 (calendar 2026, not fiscal).
 - s.2(2) "The comparison in subsection (1) is made on unrounded figures."
 - s.3(2) "made on the returns, and the revisions to them, that the Agency has supplied to the bureau by the date of certification": the 7 May revised Jan to Mar 2027 (status R) replace the preliminary P months; 2026 months final F. Vintage = revised.
 - s.3(3): figures required per designated region: SA payroll jobs for the quarter and preceding-year payroll jobs.
 - Transmittal: "replaces those three months in the April file".
 - Seasonal adjustment method: NO filed sentence, read literally, fixes the method of seasonal adjustment. "seasonally adjusted" in s.2(1) is unspecified (no X-13, ratio, factor source, span). A literal reader must choose a method; data (2021-2023 yearly, 2024-2027 monthly) permit it, but nothing in the pack says which. This is a determinism concern for the author (the method is open with no forcing sentence, as far as the shipped text goes).
 - Also unfixed: how to put pre-2026 (account-address basis) months on a place-of-work basis; 2026 Jan/Feb have workplace basis per release note so 2026 is already workplace-based, but seasonal-adjustment history before 2026 (2021-2025) is account-address basis (and the 2021-23 yearly is industry-group layout). The Regulation fixes the numerator and base only; the history for seasonal factors is a solver choice.

6. What decides: an analytical choice (how to seasonally adjust a quarter's average against a calendar-year average, with a basis break at Jan 2026 in the history used to estimate seasonality, plus preliminary vs revised vintage and the amalgamated municipality). A careful reader following the Regulation literally still has to choose the seasonal-adjustment approach; the Regulation s.1 and s.3 rules (place of work, revised vintage, unrounded) are rule application but they are stated. No planted item found. Judgement: analytical, but the "which seasonal method" step is unfiled and the risk is that regions near the line flip with the method.

7. Realism notes (mostly fine):
 - Workplace file: 48,743 rows, no exact duplicates, no key duplicates, plausible names, suites in addresses, 15-char accounts, workplace_no zero-padded in file (pandas drops padding). Max 368 jobs. Public bodies repeat (Capital School Division 412 rows, Northline Health Authority 220 and Northern Regional Health Authority 220 identical counts, Provincial Services Agency 360): plausible for multi-site employers, the 220/220 tie is a small tell.
 - Fiction names (Saltmere, Wickmoor) are plausible but all-invented; municipality codes 4-digit with leading zeros in xlsx/workplace csv but integers (101) in monthly/revision csv: realistic mess.
 - Revision file has 2,580 rows = 3 months x 43 x 20, i.e. every cell filled, perfectly rectangular; monthly file 33,780 = 39 months x 45 x ~20 minus gaps? realistic enough.
 - File mtimes are 7 May 2027 (after "today"); a time-shifted stamp, harmless but a date tell relative to a scratch environment.
 - Statements like "33,780 rows", "2,580 rows", "48,743 rows" in the transmittal match the files exactly (rows verified: 33780, 2580, 48743).
 - No text addressing a solver, no hidden sheets, no comments.

8. Ask readings (do not compute).
 Facts from the workplace file: March 2026 23,665 rows, March 2027 25,078 rows; 22,874 workplace keys (account + workplace_no) in both; 791 keys only in 2026-03 (775 whole accounts absent, 16 workplaces absent from continuing accounts); 2,204 only in 2027-03; 268 rows in March 2027 carry payroll_jobs 0 (the field description: "Zero where the return lists the workplace with no employees paid"), 107 in March 2026; 7,188 continuing workplaces have fewer jobs in 2027-03. Municipality, address and sector never differ for a continuing key. One legal name per account; 22,726 distinct nine-digit business numbers vs 23,050 payroll accounts (324 BNs hold two accounts).
 (a) Employers with payroll jobs at the region's workplaces in March 2027:
   - R1: distinct payroll_account with sum payroll_jobs > 0 at workplaces in the region's municipalities in 2027-03 (counts an employer in each region where it has jobs).
   - R2: distinct nine-digit business number (employer = business; the field description defines payroll_account as "the business number (nine digits), the program identifier RP and a four-digit reference number", so the business number is the employer and RP0001/RP0002 are programs/accounts of one employer) with jobs > 0.
   - R3: distinct accounts with any listed row (including zero-job rows), i.e. not requiring jobs > 0; contradicted by "had payroll jobs".
   - R4: count at workplace level (not distinct); wrong unit.
   - Support: "had payroll jobs" supports >0 and excludes zero-job listed workplaces. Account vs business number: the field description defines the account by the business number and also "legal_name"/"operating_name" recorded on the account, so account vs BN differs in 324 cases; the files do not state which is an employer. A real fork.
 (b) Jobs lost March 2026 to March 2027, "workplaces with no payroll jobs in March 2027":
   - R1: workplaces with payroll_jobs 0 listed in 2027-03 and jobs > 0 in 2026-03 (loss = 2026 jobs); the 1,613 jobs.
   - R2: R1 plus workplaces in the 2026-03 schedule absent from the 2027-03 schedule (a workplace not on the return has no payroll jobs; loss = 2026 jobs; 791 keys, 10,406 jobs). The statement "The Agency does not hold ..." not relevant. The field description defines zero as listed with no employees paid, implying absent is a different state (closed or dropped from schedule), not stated.
   - R3: R1 only for continuing accounts, with accounts that disappeared treated as employer closure (R2 split between continuing accounts' dropped workplaces and entire absent accounts).
   - Support: "workplaces with no payroll jobs in March 2027" literally includes a workplace with no jobs whether or not it appears; the files' own definition of zero covers only listed rows. Both readings are supportable; this is an open fork.
 (c) "those with fewer": workplaces in both months with 2027 jobs > 0 and < 2026 jobs, loss = difference. Readings: (i) only continuing workplaces with decline (gross losses, ignoring gains at others); (ii) net change across all workplaces with positive 2027 (offsetting gains); (iii) include workplaces with 2026 jobs = 0 (cannot be fewer). Also whether new workplaces (2,204, absent in 2026-03) enter: they cannot have "lost". Gross losses (decline-only) is the natural reading of "lost"; net is a possible alternative.
 (d) Region assignment: municipality_code of the workplace via concordance (stable between months); 0803/0806 appear not to appear in 2026-27 workplace file (0814 used). Rounding: jobs to nearest 10 once at the end; percentages one decimal.

Mechanical sweep lines:
- Regulation PDF carries most region names and "designated", "quarter", "2027": harmless. The names are the Schedule list, "designated"/"quarter" the legal test; "2027" is the consolidation-date neighbour ("1 July 2026" only; "2027" in the PDF text? not seen in the extracted text, so the hit is from other text in the stated sweep, harmless).
- pra_release_note_place_of_work_2026-02.pdf uses change, January, months, statistics, workplace, monthly: harmless; it states the organisation's own methodology change and lists no figure. It does tell the solver there is a break, which is context the solver needs; does not prescribe handling.
- pra_transmittal_2027-05-07.txt uses January, months, statistics, workplace, returns, monthly: harmless; row counts and delivery description, with the "replaces those three months" sentence defining vintage (stated rule, not the stump).
- Regulation PDF uses seasonal, January, months, statistics, workplace, adjusted: harmless as vocabulary, but note it names "seasonally adjusted" without a method (no stated method), which is a determinism gap rather than a leak.
- bsea_municipal_concordance.xlsx, lfs_economic_region_estimates_2025-2027.csv and pra_workplace_returns_2026-03_2027-03.csv name regions/municipalities beside numbers but none ranks regions on the prompt's question: harmless. LFS is region levels by month (employment, unemployment, participation), not a comparison with the line; concordance has no numbers beyond codes; workplace returns carry municipality codes, not region names.

### Pass 2


1. Decisive step: no sentence announces it. Nearest pointers: the prompt's "now that the revenue agency's 7 May revision file is in" and the transmittal's "The revision file brings in returns for January to March 2027 received after 23 April and replaces those three months in the April file." The release note says "The change moves payroll jobs between municipalities and between economic regions. It does not change the province's total." and "Statistics for reference months before January 2026 have not been revised." The Regulation's s.2(1): "seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its payroll jobs for the preceding calendar year."

2. No file ranks or scores the regions on the designation question. The LFS CSV (employment, unemployment and participation per region and month), the population workbook and the monthly PRA table are inputs only.

3. Files that only help the analyst: pra_statistics_field_descriptions.csv, pra_transmittal_2027-05-07.txt, bsea_municipal_concordance.xlsx (mapping, with the 0803/0806 to 0814 amalgamation note), and the release note.

4. Nothing reads as the answer. No named region or figure is flagged as the result.

5. Filed sentences that fix the computation:
- Reg 1(1) "payroll jobs of an economic region for a month means the jobs on the monthly returns that employers file with the Agency for the month at workplaces in the region's municipalities". Literal result: place jobs by workplace municipality, mapped to regions through the concordance.
- Reg 1(2) "An economic region's payroll jobs for a quarter are the average of its payroll jobs for the three months of the quarter, and its payroll jobs for a calendar year are the average of its payroll jobs for the twelve months of the year." Literal result: Q1 2027 = mean of Jan, Feb and Mar 2027; the comparison year is calendar 2026, the mean of its 12 months.
- Reg 2(1) and (2): seasonally adjusted Q1 payroll jobs more than 1.0 per cent below the preceding calendar year, on unrounded figures.
- Reg 3(2) "The certification is made on the returns, and the revisions to them, that the Agency has supplied to the bureau by the date of certification." Literal result: use the 7 May revised Jan-Mar 2027 (the revision file replaces the April preliminary).
- Transmittal: the revision file "replaces those three months".
- Release note: statistics from Jan 2026 are by workplace municipality; earlier months are by account address.
Left open by every sentence: how to seasonally adjust (no method, factors or standard named). How to make 2026 months before the January 2026 change comparable to the by-workplace definition (the workplace file covers only March 2026 and March 2027, and the Regulation does not say how to bridge), and how to carry 2026 across the 2026 layout. The workplace file is not tied to the monthly table in any sentence either. These are method steps and are not closed.

6. Closest to an analytical choice. The monthly table mixes bases: 2026 and 2027 are by workplace per the release note, but 2024 and 2025 are by account address, and the Regulation's definition is by workplace. The seasonal-adjustment and base-year comparability steps have to be chosen by the analyst. No sentence tells you which; the release note and the Regulation's definition are what to read.

7. Realism tells:
- pra_workplace_returns: 47,932 rows; every payroll_account is exactly 15 characters and workplace_no is always 3 digits (regular, but plausible as a system export). 22,670 accounts under 22,378 business numbers; two reference numbers only ("0001" 45,810 and "0002" 2,122), which is a believable pattern. Employer names are template-like (a place or nature word + trade + Inc./Ltd./Limited/Corp.), e.g. "Sealwick Cove Cafe Inc.", "Summit Cafe Ltd.", "Briar Transport Inc.". Operating name is always the legal name with the suffix stripped, with no exceptions. Street addresses are a number + a short generic street name (Maple, Pine, Harbour). Employer names reuse place names from the concordance. 
- Jobs per workplace are integers with plausible skew (median 7, max 473); many 0 rows.
- Monthly file: per-month row counts vary (730, 744, 762), which is natural; the revision file has exactly 762 rows per month for the three months, a perfectly regular shape but consistent with "every cell of the months it covers".
- Concordance: all in-force-from dates are 2016-01-01 except the amalgamation; round and regular. Population workbook is balanced across all municipalities (every municipality has all three years).
- Regulation PDF: short, clean and neat; a few headline regions named in the Schedule with codes E01 to E10 exactly in order. "Consolidated to 1 July 2026; this consolidation is not an official version" is a plausible footer.
- Only the Capital region has a plain name; the other region names (Saltmere Coast, Brennick Valley, Dunfallow Bay) are fictional-sounding and uniformly styled.

8. Supplementary figures.
(a) Employers with payroll jobs at the region's workplaces in March 2027. Readings: (i) distinct payroll_account (15 char) with payroll_jobs > 0 at a workplace in the region; (ii) distinct business number (first nine digits) with jobs > 0 (292 business numbers hold more than one account, 108 of them under different legal names); (iii) distinct accounts or business numbers listed with any row, including zero rows; (iv) distinct legal_name. Support: field description "payroll_account: Payroll program account: the business number (nine digits) of the business that holds the account, the program identifier RP and a four-digit reference number." and "payroll_jobs ... Zero where the return lists the workplace with no employees paid." The Regulation says "employers" and "workplaces", and nothing defines "employer" as an account versus a business. The prompt's "employers that had payroll jobs" favours jobs > 0. Genuine fork between account and business-number keys: yes, unless a sentence elsewhere settles it. I found none that chooses between them.
(b) and (c) Jobs lost, March 2026 to March 2027, at workplaces whose jobs fell, split into those with none left in March 2027 and those that kept some. Readings: workplace key = (payroll_account, workplace_no) (field description "The workplace's sequence number on the account's workplace schedule"); alternative key = address; alternative = by business number. Loss = jobs 2026 minus jobs 2027 per workplace, summed over workplaces whose jobs fell; versus net change across all workplaces; versus including workplaces absent from the 2027 file as zero (field description says zero is written where listed, nothing says what an unlisted workplace means). "None left" = zero row in 2027 vs absent from 2027 file vs both. Workplace region = its municipality in each month (0803/0806 vs 0814 only matters for the monthly table). Support: "workplaces whose payroll jobs fell" in the prompt and the zero-row description. Genuine fork: the treatment of a workplace that is absent from March 2027 (closed, or renumbered) versus listed with zero is not chosen by any sentence; the key (account plus number vs address) is also not chosen. I flag this as a likely fork.

REVIEW items:
- regional_rapid_response_program_regulation.pdf, 8 of 9 call words: harmless. It is the governing regulation, and it states only the designation test and the region list; it names no region as designated or certified.
- pra_release_note_place_of_work_2026-02.pdf, 6 of 25 terms: leak-adjacent but not an answer leak. It does name the move ("The Agency's statistics now place payroll jobs in the municipality of the workplace ... moves payroll jobs between municipalities and between economic regions") from January 2026. It is a plain agency notice that a real file would carry, and it gives no figures. Harmless, but it does flag the basis change that matters for the 2025 and 2026 comparison.
- pra_transmittal_2027-05-07.txt, 6 of 25 terms: names the revision (replaces the three preliminary months) and that the 2021-2023 tables are "as published; the statistics have been produced in the monthly layout since January 2024". It does not name the place-of-work move. Harmless.
- regional_rapid_response_program_regulation.pdf, 12 of 25 terms: the Regulation states the definitions (seasonally adjusted, quarter averages, calendar-year average, workplaces). It does not name the basis move or give a method. Harmless; the sentences are the stated rules.
- bsea_municipal_concordance.xlsx: harmless, a mapping of municipalities to regions with the amalgamation note; no numbers about jobs, no ranking.
- lfs_economic_region_estimates_2025-2027.csv: harmless, monthly employment, unemployment and participation by region; no ranking, and it is not the Regulation's measure.
- pra_workplace_returns_2026-03_2027-03.csv: harmless, row-level workplace data; no ranking or per-region totals.

### Pass 3


1. Decisive step: no sentence announces it. The nearest is the release note: "From the January 2026 reference month, ... The Agency's statistics now place payroll jobs in the municipality of the workplace. For reference months to December 2025, the statistics placed all of an employer's payroll jobs in the municipality of its account address." and "Statistics for reference months before January 2026 have not been revised." The Regulation's s.2(1) comparison of a 2027Q1 figure with "its payroll jobs for the preceding calendar year" (2026, all on the workplace basis) is not itself broken by this. The note does name the basis change, but a 2026 comparison year lies wholly after it. The sentence that actually matters is s.2(1): "seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its payroll jobs for the preceding calendar year". The transmittal's "replaces those three months in the April file" is the vintage cue.

2. Ranking/scoring of regions on the question: none. The lfs file, the monthly CSV and the revisions file are raw series with no designation, gap or flag.

3. Exists only to help the analyst: pra_statistics_field_descriptions.csv; pra_transmittal_2027-05-07.txt (vintage and row counts); the "Economic regions" sheet and the Note column of bsea_municipal_concordance.xlsx.

4. Answer-like figures or names: none. "Capital", "Saltmere Coast" etc. appear only as the Schedule list and as labels in the series. Nothing reads as a verdict.

5. Literal sentences:
- Reg 1(1) "payroll jobs of an economic region for a month means the jobs on the monthly returns that employers file with the Agency for the month at workplaces in the region's municipalities": the monthly jobs by workplace municipality, mapped through the concordance.
- Reg 1(2) "An economic region's payroll jobs for a quarter are the average of its payroll jobs for the three months of the quarter, and ... for a calendar year are the average of ... the twelve months of the year": Jan-Mar 2027 mean; calendar 2026 mean (12 months, Jan-Dec 2026, all final, workplace basis).
- Reg 2(1)/(2): "seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its payroll jobs for the preceding calendar year", on unrounded figures: designated if SA(2027Q1) < 0.99 x avg 2026.
- Reg 3(2) "the returns, and the revisions to them, that the Agency has supplied ... by the date of certification" plus transmittal "replaces those three months in the April file": use the 7 May revised (R) Jan-Mar 2027, not the P rows.
- Reg 1(1) "made up of the municipalities that the bureau's municipal concordance places in it": the concordance in force (Wexleigh-Dorran 0814 from 2025-01-01 replaces 0803/0806).
Left open by every sentence: how "seasonally adjusted" is obtained. Nothing files a method (no factors, no X-13 spec); the only route is to derive seasonality from the 2021-2023 yearly tables and 2024-2026 monthly history. Also open: how to bridge the 2021-2023 account-address, industry-group layout to the monthly layout, and whether the 2026 comparison year needs any basis adjustment (it does not by the literal text).

6. Choice: an analytical choice (how to seasonally adjust a three-month average from a short, level-shifted history before comparing with the prior-year average). Deciding material: Reg 2(1) "seasonally adjusted payroll jobs for the quarter", with the 2021-2023 yearly tables and the monthly CSV as the only seasonality evidence. The rule-following parts (vintage, concordance, 1.0 per cent line) are stated.

7. Realism tells:
- pra_workplace_returns: 22,430 accounts but 22,124 business numbers; 306 BNs hold a second account whose operating name ends " - Hourly" (a recurring template suffix); 122 BNs carry differing legal names across accounts. Zero ties in workplace_no format (all 3-digit, perfectly regular). municipality_code in the CSV reads 904, 301 when parsed as numbers (leading zeros only if read as text; harmless). About 13% of legal names are "NNNNNNN Canada Inc." numbered companies (plausible).
- Street addresses are generic (Meadow Way, Orchard Drive, Granite Avenue); some repeat 6 times across firms (random draw).
- Monthly CSV: every month except the revisions has a fairly regular row count (730-762 per month), 2,286 revision rows = exactly 3 x 762; P rows 2,286 = same. Perfectly regular but coherent with the transmittal.
- LFS file: 27 months for each of 10 regions (270 rows, perfectly regular).
- Concordance: 4 municipalities for 7 of 10 regions (Capital 5, Brennick 5, Quillon 7): fairly even counts. Population file: three 1 July dates per municipality, regular.
- Free text in the release note and regulation is clean and plausible; transmittal row counts (29,118; 2,286; 47,647) match the files exactly.
- Names: Jacqueline Chaney, Ryan Bentley; invented place names (Wickmoor, Tallisford, Saltmere) look fictional, not real.

8. Supplementary figures.
(a) Employers with payroll jobs in the region in March 2027.
- Unit: business number (9 digits), per payroll_account description "the business number (nine digits) of the employer that holds the account"; this supports employer = BN, collapsing the 306 second ("- Hourly") accounts. Reading 2: count payroll_account (22,430 accounts); the description line makes that account-not-employer, so it is ruled out by that sentence. Reading 3: legal_name (122 BNs have name variants); ruled out because BN is stated to identify the employer.
- Population: "had payroll jobs" means payroll_jobs > 0 at a workplace in the region in 2027-03 (reading A); reading B counts any workplace row in the region including zero-job rows ("Zero where the return lists the workplace with no employees paid" supports that a listed zero-job row is not employing anyone, favouring A). An employer with workplaces in several regions counts once in each region (prompt: "at its workplaces"); a province-wide dedupe is not suggested by any sentence.
- Genuine fork: no on unit (description chooses BN); a weak residual fork on zero-job rows, mostly settled by "had payroll jobs".
(b) and (c) Jobs lost at workplaces whose jobs fell, split by none left / kept some.
- Key of workplace: (payroll_account, workplace_no), stable across both months (no address or municipality changes in the 22,423 matched pairs); alternative key BN + address gives the same result on the files read. "workplace_no: The workplace's sequence number on the account's workplace schedule."
- Loss measure: per-workplace decrease Mar 2026 minus Mar 2027, summed over workplaces with a decrease (prompt "workplaces whose payroll jobs fell"); alternative net change by region is ruled out by that phrase.
- Workplaces absent from 2027-03 (765 rows) versus listed with zero (260): "none left in March 2027" supports treating absent as zero; the files say only that zero is "where the return lists the workplace with no employees paid", so an absent workplace is not explicitly stated to be zero. A careful reader could exclude absent ones; most would count them (jobs went to none). This is the nearest thing to a fork; the prompt's "none left" reads in favour of including both.
- New workplaces in 2027 (2,036 rows) have no 2026 base and no loss; municipality is that of the workplace row, region via the concordance.
- Genuine fork: one soft fork (absent versus zero), not decided by a sentence in the files other than the prompt's "none left".

Mechanical sweep items:
- regional_rapid_response_program_regulation.pdf (8 of 9 call words): harmless, it is the governing regulation; it names regions only as the Schedule and states the 1.0 per cent test, certifies nothing.
- pra_release_note_place_of_work_2026-02.pdf: harmless on the stump but it does name the move (account address to workplace basis from January 2026, "The change moves payroll jobs between municipalities and between economic regions"). It gives no figures, direction or which regions; it is Layer 1 mess documentation. Flag only if the design's stump is that basis break; it does not say which side of the comparison is affected.
- pra_transmittal_2027-05-07.txt: harmless, names the vintage replacement and layout change in 2024 ("the statistics have been produced in the monthly layout since January 2024"), not the decisive step.
- regional_rapid_response_program_regulation.pdf (12 of 25 terms): harmless, the stated seasonal-adjustment, quarter, year and comparison definitions; it does not name any move or method.
- bsea_municipal_concordance.xlsx: harmless, a municipality-to-region mapping with no numbers on the decision question (only codes and dates).
- lfs_economic_region_estimates_2025-2027.csv: harmless, labour force survey employment, unemployment and participation per region and month; it does not rank regions or compute the payroll test (a possible distractor).
- pra_workplace_returns_2026-03_2027-03.csv: harmless, row-level workplace data, no totals by region or designation.
