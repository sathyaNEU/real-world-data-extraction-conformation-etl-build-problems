## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Award the 2027-28 instructional investment grant to 214682, 214946, 216190, 216278 and 216454.**
They have the lowest fiscal 2026 instruction expense per FTE student. 216190, 216278 and 216454 are branch campuses whose instruction sits inside their parents' returns: each parent's instruction is split among the parent and its branches by the cost of the credit hours each taught, at the cost per credit hour by level the sixteen campuses that report alone show, and the branches teach mostly lower-division hours. Split by FTE students instead, the branches carry their systems' averages and the five would be 214506, 214682, 214858, 214946 and 215298.

## 2. Critical Components

1. Awarded: **214682**, **214946**, **216190**, **216278**, **216454**
2. Not awarded: every other reporting unit, 21 campuses
3. Instruction expense per FTE of the campuses reporting alone, whole dollars: 214330 12,777, 214418 12,953, 214506 8,838, 214594 11,034, 214682 8,471, 214770 11,639, 214858 9,575, 214946 8,020, 215034 11,780, 215122 9,605, 215210 10,907, 215298 9,042, 215386 12,667, 215474 10,114, 215562 10,639, 215650 9,725

## 3. Step-by-Step Solution

1. Took fiscal 2026 instruction (F1C011) from the finance return and 2025-26 FTE (FTEUG plus FTEGD) from the 12-month return; the branches carry PRCH_F 2 and zero, their parents PRCH_F 1.
2. Summed the board's credit hour file by campus and level, campus codes to UNITID through the code list; it ties to the 12-month return's credit hours.
3. Fitted instruction expense on lower-division, upper-division and graduate credit hours across the sixteen campuses that report alone (least squares, no intercept).
4. Split each parent's reported instruction among the parent and its branches in proportion to the fitted cost of the credit hours each taught, keeping the parent's total.
5. Divided by each campus's FTE and took the five lowest: 214682, 214946, 216190, 216278, 216454.
6. Ask A: the branches' fall 2026 census rows, a student's course counted once (a cross-listed course carries the student under both course numbers at one meeting), undergraduate hours over 15 plus graduate over 12.
7. Ask B: each student counted once per branch, the rows under the old and the new student id joined by birth date, sex and home ZIP code.

## 4. Deliverable Answers

### lhecb_2027-28_instructional_investment_awards.xlsx

1. The five awards: 214682, 214946, 216190, 216278, 216454.
2. Chart of every reporting unit's instruction expense per FTE, lowest first, the awards marked.
3. Fall 2026 FTE students at each branch campus (one decimal):
   - 216190: 3053.7
   - 216278: 2451.8
   - 216454: 2046.0
   - 216630: 1883.7
   - 216718: 1610.7
   - 216894: 2193.7
4. Unduplicated fall 2026 headcount at each branch campus:
   - 216190: 4,715
   - 216278: 3,805
   - 216454: 3,183
   - 216630: 2,909
   - 216718: 2,489
   - 216894: 3,400
