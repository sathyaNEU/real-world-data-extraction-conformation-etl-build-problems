# leak check, task465

**Verdict: REVIEW.** 15 files read, 56 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: published, withheld, district, service, totals, average, decisive, history, periods, export, failure, estimates, readable, sentence, bought, symbols, practice, missing, default, regression, reading, statistics, downloads, additive, structure

## 3 answer figures in the pack (REVIEW 13)
- **REVIEW** `apgc_risk_policy_2026.pdf`: golden figure 1.4 appears: ...unty only when its quoted premium rate is at most 1.4 times the cover's expected loss. 5.3 A cover's...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 593,300 appears: ...PRODUCTION, MEASURED IN BU",TOTAL,NOT SPECIFIED,"593,300",,2003-02-26 15:00:00.000 SURVEY,2002,YEAR,COUNTY...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 781,600 appears: ...RODUCTION, MEASURED IN BU",TOTAL,NOT SPECIFIED,"1,781,600",,2002-06-18 09:00:00.000 SURVEY,1995,YEAR,COUNTY...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 831,700 appears: ...RODUCTION, MEASURED IN BU",TOTAL,NOT SPECIFIED,"6,831,700",,2004-02-26 15:00:00.000 SURVEY,2003,YEAR,AGRICU...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 151,500 appears: ...RODUCTION, MEASURED IN BU",TOTAL,NOT SPECIFIED,"1,151,500",,2002-06-18 09:00:00.000 SURVEY,2000,YEAR,AGRICU...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 827,200 appears: ...PRODUCTION, MEASURED IN BU",TOTAL,NOT SPECIFIED,"827,200",,2002-06-18 09:00:00.000 SURVEY,1993,YEAR,COUNTY...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 43,000 appears: ...,,,CORN,CORN - ACRES PLANTED,TOTAL,NOT SPECIFIED,"43,000",,2005-02-20 15:00:00.000 SURVEY,2004,YEAR,AGRICU...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 19,600 appears: ...IRRIGATED - ACRES HARVESTED",TOTAL,NOT SPECIFIED,"19,600",,2002-06-18 09:00:00.000 SURVEY,1997,YEAR,COUNTY...
- **REVIEW** `clrs_county_estimates_pull_2024-03.csv`: golden figure 11,300 appears: ...41,CORN,CORN - ACRES PLANTED,TOTAL,NOT SPECIFIED,"11,300",,2002-06-18 09:00:00.000 SURVEY,1994,YEAR,COUNTY...
- **REVIEW** `clrs_county_estimates_pull_2026-10.csv`: golden figure 831,700 appears: ...RODUCTION, MEASURED IN BU",TOTAL,NOT SPECIFIED,"1,831,700",,2026-03-26 15:00:00.000 SURVEY,2020,YEAR,COUNTY...
- **REVIEW** `clrs_county_estimates_pull_2026-10.csv`: golden figure 19,600 appears: ...RODUCTION, MEASURED IN TONS",TOTAL,NOT SPECIFIED,"19,600",,2026-03-26 15:00:00.000 SURVEY,2017,YEAR,COUNTY...
- **REVIEW** `clrs_county_estimates_pull_2026-10.csv`: golden figure 11,300 appears: ..., IRRIGATED - ACRES PLANTED",TOTAL,NOT SPECIFIED,"11,300",,2026-03-26 15:00:00.000 SURVEY,2017,YEAR,COUNTY...
- **REVIEW** `quillfield_re_area_yield_term_sheet_2027.pdf`: carries 4 of 7 distinctive words of the committed call: "Buy the Ardley, Elster and Pallard covers and decline Corvin's and Tresham's."

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `apgc_risk_policy_2026.pdf`: 5 of 25 stump-paragraph terms appear (service, average, estimates, bought, statistics); read whether the document names the move
- **REVIEW** `clrs_county_estimates_methods_2026.pdf`: 11 of 25 stump-paragraph terms appear (published, withheld, district, service, totals, export); read whether the document names the move
- **REVIEW** `quillfield_re_area_yield_term_sheet_2027.pdf`: 3 of 25 stump-paragraph terms appear (service, estimates, bought); read whether the document names the move

## 8 column names (REVIEW 2)
- **REVIEW** `data_dictionary.csv`: Python-style nulls or booleans (nan/None/True/False) in the first rows
- **REVIEW** `drought_monitor_county_weeks_2000_2025.csv`: Python-style nulls or booleans (nan/None/True/False) in the first rows

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Isolated reader (general-purpose, Sonnet, medium), fresh copy of `prompt.txt` and `target/` only, architecture 1.

1. Decisive step: none quoted; nearest the methods note 2.1 ("A district's estimates are the totals of all the county
   estimates in the district ... whether or not a county estimate is published") and 6.1 ("a withheld estimate shows its
   symbol in place of a value"); nothing says to rebuild withheld county yields from district totals.
2. Ranking file: none; the quote schedule lists rates and expected yields without scoring the covers.
3. Helper-only file: none; the register's row counts read slightly like a hand-off manifest.
4. Answer-like figure: none; no expected loss appears anywhere.
5. Literal sentences: policy 5.3, the term sheet's index, trigger, payment and rating basis, methods 2.1, 2.2, 4.1 and 4.2;
   literal execution takes all 35 years, the October 2026 download where it holds a year, adds the trend times the years to
   2027, caps the share, averages; a withheld year is rebuilt as the district less its published counties (dropping it is
   not licensed by the text). Executes to the golden.
6. What decides: "an analytical choice ... partly rule application: once the district-differencing text is read, the steps
   are mechanical."

REVIEW lines: all harmless (filed buy rule; coincidental digits in raw production and acreage rows; the candidate set;
genre vocabulary; the methods note "harmless, or at most borderline"; the drought monitor's real "None" column).
Realism: register and dictionary slightly assembled; "duplicate county keys" (not reproduced: no key repeats in either
download). Ask readings: receipts over dryland or all-practice production; premium from the rounded liability (both
closed in the generator).

