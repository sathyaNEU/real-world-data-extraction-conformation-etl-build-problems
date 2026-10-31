## Tags

> **Domain:** Education & Learning Sciences (item response theory and test equating).
> **Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Set the pass mark on Harrowgate Testing's theory paper at 38 out of 60.** It holds the standard of 65 on Brindle Assessment's scale under AP-3, read through the candidates who failed Brindle's paper and sat Harrowgate's next, against Brindle's own resits matched on the first score. Not 40, the mark that carries the 2025 first-time pass rate onto the 2026 first-time candidates, a stronger cohort.

## 2. Critical Components

1. The candidates measured on both papers are the 1,164 who failed their one Brindle sitting and sat Harrowgate's paper next; a second sitting reads higher than a first on any paper.
2. Brindle's resits of first-sitting fails in 2021 to 2025, matched on the first score, put **28.0 per cent** of those candidates at 65 or more on a second Brindle sitting.
3. On Harrowgate's paper 32.2 per cent of them reach 37 and 25.3 per cent reach 38, so **38** is the lowest raw mark no larger share reaches.

## 3. Step-by-Step Solution

1. Tied every sitting to a person through heatwise_candidate_register_2026-10-12.csv (Brindle and Harrowgate candidate numbers to board numbers; board numbers sharing surname, initials and date of birth as one person), kept Brindle's SAT rows and Harrowgate's cleared and released marks once per sitting_ref, dated by the UK local date.
2. Took the candidates whose only Brindle sitting was a fail (under 65) and whose next sitting was Harrowgate's paper, with their first scaled score and their raw mark.
3. Took every Brindle fail at a first sitting from 2021 to 2025 followed by a second Brindle sitting, and for each first score the share scoring 65 or more at the second.
4. Averaged that share over the cross-switch candidates' first scores (AP-3 section 2's equivalent group): 28.0 per cent.
5. Set the pass mark at the lowest raw mark the cross-switch candidates reach in no larger share: 38.
6. Counted, on the same people, each 2026 month's first-time and resitting candidates and each year's first sittings of Brindle's paper with their passes (a person's first sat sitting on either paper).
7. Recommended 38 out of 60.

## 4. Deliverable Answers

### theory_pass_mark_2027.pdf

1. Recommendation: set the pass mark on Harrowgate's theory paper at 38 out of 60.
2. Chart: the share of the candidates who sat Harrowgate's paper reaching each raw mark, with the pass mark of 38 drawn on it.
3. Candidates sitting the theory paper for the first time, and candidates resitting it, in each month of 2026 to September, whole numbers:
   - January 2026: 1,065 first time, 1,471 resitting
   - February 2026: 1,196 first time, 1,292 resitting
   - March 2026: 1,324 first time, 1,394 resitting
   - April 2026: 1,308 first time, 1,211 resitting
   - May 2026: 1,677 first time, 334 resitting
   - June 2026: 1,895 first time, 303 resitting
   - July 2026: 1,819 first time, 313 resitting
   - August 2026: 1,502 first time, 290 resitting
   - September 2026: 1,813 first time, 338 resitting
4. Candidates who first sat Brindle's paper in each year from 2021 to 2025, and how many of them passed at that sitting, whole numbers:
   - 2021: 6,721 first sat, 3,141 passed
   - 2022: 7,319 first sat, 3,356 passed
   - 2023: 7,913 first sat, 3,743 passed
   - 2024: 8,640 first sat, 4,038 passed
   - 2025: 10,935 first sat, 5,164 passed

### theory_results_2026.csv

1. Every 2026 sitting of the theory paper to 30 September, one row each: the person's board number, the board number at the sitting, the UK date, the provider, the scale, the mark, the attempt, whether it was the first sitting and the result (65 on Brindle's scale, 38 on Harrowgate's).
