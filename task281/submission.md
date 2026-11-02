## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a university library dividing a course e-textbook fund among faculties on the hold-weeks their students waited, where a cancelled hold's wait runs to the moment the platform would have offered it a copy).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Credit the Course Texts Fund 2027 of £180,000 as Arts and Humanities £19,000, Social Sciences £33,500, Ardmuir Business School £21,500, Law £19,200, Science and Engineering £45,800, Life Sciences £14,600, Medicine and Dentistry £15,400, Health Sciences £10,900.** Each cancelled hold waits until the earliest-placed-first rule would have reached it, and the record shows that moment: the first copy that came free after the cancellation and went to a hold placed after it, or to nobody. Not the survival estimate with cancellations treated as censored, which moves money between faculties (Medicine and Dentistry £14,000, Science and Engineering £47,100, among others), because the students who cancel are the ones who saw a long queue ahead of them, so the holds still waiting are not like the ones that left.

## 2. Critical Components

1. Holds counted (students, placed 12 January to 26 April 2026 by UK time): 40,697, of which 25,647 were offered a copy and 15,050 were cancelled.
2. Holds by faculty: Arts and Humanities **3,151**, Social Sciences **5,587**, Ardmuir Business School **7,369**, Law **4,542**, Science and Engineering **8,589**, Life Sciences **3,419**, Medicine and Dentistry **4,384**, Health Sciences **3,656**.
3. Hold-weeks by faculty, to the nearest 100: Arts and Humanities **12,200**, Social Sciences **21,500**, Ardmuir Business School **13,800**, Law **12,300**, Science and Engineering **29,500**, Life Sciences **9,400**, Medicine and Dentistry **9,900**, Health Sciences **7,000**.
4. Amounts by faculty, to the nearest £100: Arts and Humanities **£19,000**, Social Sciences **£33,500**, Ardmuir Business School **£21,500**, Law **£19,200**, Science and Engineering **£45,800**, Life Sciences **£14,600**, Medicine and Dentistry **£15,400**, Health Sciences **£10,900**.

## 3. Step-by-Step Solution

1. Took the holds in shelfmark_holds_20250901-20261031.csv placed from 12 January to 26 April 2026 by UK date, dropped patron type Staff, and gave each the faculty of its department code's school under Schedule 1 of UC-26-114_course_texts_fund_2027_terms.pdf.
2. Took a hold's wait to its offer_made_at where it was offered a copy (fulfilled or lapsed).
3. Listed, title by title, every instant a copy came free (ended_at in shelfmark_checkouts_20250901-20261031.csv and the expiry of every lapsed offer) and the hold placed earliest among those offered a copy at that instant.
4. Ended each cancelled hold's wait at the first such instant after its cancellation whose copy went to a hold placed after it or to no hold (Shelfmark terms 2.2).
5. Took hold-weeks as the wait capped at 84 days, less 14 days, in weeks and never below zero, summed them by faculty and divided £180,000 in proportion.
6. Spend: converted euro and dollar invoice lines at the month's Finance Office rate, mapped each fund code to its faculty from 1 August 2026 under Schedule 2, and shared each CT-CORE package line by the package's titles (KBART online identifiers) on each faculty's 2025-26 essential lists, an item's ISBN taken through the catalogue's related-record and preceding-edition links to its e-book.
7. Spring lists: counted each 2025-26 Semester 2 essential item whose work had no e-book of the cited edition or later licensed on 12 January 2026, by title line or by a package then in force.
8. 40-loan licences: took each licence bought before 1 September 2025 at its status-report figure (one absent from that report had lapsed) and later ones at 40, made every checkout to 30 October 2026 on the earliest-purchased licence not on loan with loans left, started a re-licence when a licence's fortieth loan ended (the title's re-licence dated that day, lowest reference first) and charged it to that licence's faculty, then summed the loans left on licences in force by faculty.

## 4. Deliverable Answers

### course_texts_fund_2027.csv

1. Credit by 2026-27 fund code, to the nearest £100:
   - CT-AHU (Arts and Humanities): £19,000
   - CT-SSC (Social Sciences): £33,500
   - CT-BUS (Ardmuir Business School): £21,500
   - CT-LAW (Law): £19,200
   - CT-SAE (Science and Engineering): £45,800
   - CT-LSC (Life Sciences): £14,600
   - CT-MED (Medicine and Dentistry): £15,400
   - CT-HSC (Health Sciences): £10,900

### course_texts_fund_2027.xlsx

1. Division sheet, holds counted, hold-weeks (nearest 100) and amount (nearest £100), with a bar chart of the amounts:
   - Arts and Humanities: 3,151 holds; 12,200 hold-weeks; £19,000
   - Social Sciences: 5,587 holds; 21,500 hold-weeks; £33,500
   - Ardmuir Business School: 7,369 holds; 13,800 hold-weeks; £21,500
   - Law: 4,542 holds; 12,300 hold-weeks; £19,200
   - Science and Engineering: 8,589 holds; 29,500 hold-weeks; £45,800
   - Life Sciences: 3,419 holds; 9,400 hold-weeks; £14,600
   - Medicine and Dentistry: 4,384 holds; 9,900 hold-weeks; £15,400
   - Health Sciences: 3,656 holds; 7,000 hold-weeks; £10,900
2. Course text spend on invoice lines dated 1 January to 31 October 2026, to the nearest £10:
   - Arts and Humanities: £9,810
   - Social Sciences: £25,270
   - Ardmuir Business School: £22,140
   - Law: £11,320
   - Science and Engineering: £20,210
   - Life Sciences: £5,380
   - Medicine and Dentistry: £12,540
   - Health Sciences: £11,630
3. Essential spring 2026 reading-list items the Library could not lend as an e-book on 12 January 2026:
   - Arts and Humanities: 24
   - Social Sciences: 27
   - Ardmuir Business School: 27
   - Law: 23
   - Science and Engineering: 35
   - Life Sciences: 15
   - Medicine and Dentistry: 14
   - Health Sciences: 13
4. Loans left on the 40-loan licences charged to each faculty and in force at the end of 30 October 2026:
   - Arts and Humanities: 1,133
   - Social Sciences: 2,352
   - Ardmuir Business School: 1,358
   - Law: 744
   - Science and Engineering: 1,215
   - Life Sciences: 801
   - Medicine and Dentistry: 1,087
   - Health Sciences: 1,069
