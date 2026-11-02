## Tags

**Domain:** Education & Learning Sciences (item response theory and test equating: the optional questions of a written accreditation paper put on one mark scale when each candidate chooses which questions to answer).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Approve the November 2026 Paper 2 results with the optional questions moved Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -1, Q8 -3 marks: 393 of the 714 candidates who sat pass.** Not the moves set from each question's mean mark (Q6 +1, Q8 -1, 417 passing): the stronger candidates chose Question 6 and the weaker chose Question 8, and the candidates who answered Question 6 averaged 13.5 on their other answers against 10.1 on it, while Question 8's averaged 9.0 against 12.1. Not the unmoved marks (433 passing).

## 2. Critical Components

1. Each question's difficulty for the candidates who sat, from a candidate-plus-question fit of the November marks of record, set against the average question counted once and rounded: **Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -1, Q8 -3**.
2. Candidates who sat Paper 2: **714**; with the moves applied and held within 0 and 20, **393** reach 50 and pass.
3. The candidates who answered Question 6 average **13.5** on their other answers and **10.1** on Question 6; Question 8's average **9.0** and **12.1**.

## 3. Step-by-Step Solution

1. Took the NOV26 rows of cae_marking_export_2026.csv and summed each candidate's part marks per question, the last mark entered for each part (regulation 11.2), a no-response part counting nothing: 714 candidates sat.
2. Fitted each mark as a candidate effect plus a question effect over every answer, set each question's effect against the average of the question effects and rounded to the nearest whole mark (regulation 14.1): Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -1, Q8 -3.
3. Applied each move to every answer to its question, held within 0 and 20 (regulation 14.2), summed and passed totals of 50 or more (regulation 12): 393 pass and 321 fail.
4. For each centre's Paper 2 entries in cae_entries_nov2026.csv, counted as withdrawn the entries withdrawn by a request in portal_requests_nov2026.json received before 7 November, Sydney time (regulation 17.1; submitted is UTC, and requests sent in the last week were actioned on 9 and 10 November), and as absent the other entries with no NOV26 marks (regulation 17.3): 61 withdrawals and 31 absentees in all.
5. Matched each November sitter to cae_candidates_may2026.xlsx on member number where both carry one, otherwise on family name, first given name and date of birth, and kept May candidates with MAY26 marks in the export (regulation 2, marked present): 150 had sat Paper 2 in May.
6. Resolved each request in results_review_requests_2026.csv to its May candidate by candidate number and family name (3 numbers keyed with two digits transposed) and compared the result on the marks of record at issue on 30 June with the result after review, both with the minutes' May moves: 11 results changed, each from fail to pass.
7. Refunded under regulation 19.4 the fees of those 11 reviews and of the 4 requests received after 21 July; card fees as paid, account fees at Schedule 1's fee for the day received less the firm's discount in corporate_accounts.csv (each account line repeats its invoice total): AUD 2,625.
8. Recommend approving the moves and the 393 passes.

## 4. Deliverable Answers

### nov2026_paper2_results.csv

1. One row for each of the 714 candidates who sat, with the moved mark counted on each question answered, the total and Pass or Fail: 393 Pass, 321 Fail.

### paper2_results_committee_paper.docx

1. Moves, whole marks: Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -1, Q8 -3.
2. Number passing: 393 of 714.
3. Bar chart of the moves by question (Figure 1, section 2).
4. By centre, withdrawals, absentees and sitters who had also sat Paper 2 in May:
   - Sydney: 11, 4, 33
   - Western Sydney: 4, 3, 16
   - Melbourne: 23, 8, 34
   - Brisbane: 8, 9, 25
   - Perth: 7, 3, 20
   - Adelaide: 8, 4, 22
5. May results changed on review: yes, 11, each from fail to pass.
6. Review fees to refund: AUD 2,625.
