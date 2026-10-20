# leak check, task475

**Verdict: REVIEW.** 14 files read, 70 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: claims, amount, statewide, objective, window, decisive, childless, dictionary, close-out, residential, published, composition, decision, department, builds, agency, splits, quantity, closed, decomposition, lowest, paired, recovered, sentence, average

## 3 answer figures in the pack (REVIEW 9)
- **REVIEW** `cvcog_wap_py2025_closeout_summary.pdf`: golden figure 131 appears: ...79.00 786,199.50 Vehicles 89,740.82 41,283.54 131,024.36 Training 37,772.93 6,339.73 44,112.66 I...
- **REVIEW** `cvcog_wap_py2025_closeout_summary.pdf`: golden figure 114 appears: ...8,698.43 52,172.89 All spending 8,791,513.45 3,114,448.84 11,905,962.29 Notes Spending is counted i...
- **REVIEW** `data_dictionary.txt`: golden figure 200 appears: ...,000; 4 $75,000 under $100,000; 5 $100,000 under $200,000; 6 $200,000 or more N1 number...
- **REVIEW** `dor_individual_income_tax_statistics_ty2023.pdf`: golden figure 135 appears: ...credit amount Under $10,000 182,305 1,155,434 135,812 140,471 $10,000 under $20,000 312,068 4,68...
- **REVIEW** `dor_individual_income_tax_statistics_ty2023.pdf`: golden figure 129 appears: ...0 0 0 40,114 95,330 38,089 164,138 25,223 129,934 $50,000 under $75,000 0 0 728 188 2,666...
- **REVIEW** `dor_individual_income_tax_statistics_ty2023.pdf`: golden figure 131 appears: ...15,840 33,755 133,278 30,563 177,069 20,183 131,448 $20,000 under $25,000 387 67 15,796 61,25...
- **REVIEW** `dor_individual_income_tax_statistics_ty2023.pdf`: golden figure 114 appears: ...94 9,729 70,748 $25,000 under $50,000 0 0 40,114 95,330 38,089 164,138 25,223 129,934 $50,000...
- **REVIEW** `cvcog_weatherization_allocation_policy_rev4.pdf`: carries 18 of 20 distinctive words of the committed call: 'The Corran Valley Council of Governments should split the $20,000,000 2027 weatherization fund in proportion to each mem'
- **REVIEW** `data_dictionary.txt`: carries 14 of 20 distinctive words of the committed call: 'The Corran Valley Council of Governments should split the $20,000,000 2027 weatherization fund in proportion to each mem'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `cvcog_wap_py2025_closeout_summary.pdf`: 3 of 25 stump-paragraph terms appear (amount, close-out, department); read whether the document names the move
- **REVIEW** `cvcog_weatherization_allocation_policy_rev4.pdf`: 6 of 25 stump-paragraph terms appear (amount, close-out, residential, published, agency, closed); read whether the document names the move
- **REVIEW** `data_dictionary.txt`: 7 of 25 stump-paragraph terms appear (amount, dictionary, close-out, residential, published, department); read whether the document names the move
- **REVIEW** `dor_individual_income_tax_statistics_ty2023.pdf`: 4 of 25 stump-paragraph terms appear (amount, published, department, lowest); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Four isolated readers (general-purpose, sonnet, medium), each on a fresh copy of prompt.txt and target.zip, in two
rounds; each scored with score_reader.py before its verdict was read.

| Round | Reader | Call | Figures kept | score_reader |
|---|---|---|---|---|
| 1 | 1 | Tallis capped at 15.46 per cent (the default path) | 14 of 71: ask A | exit 0 |
| 1 | 2 | Tallis capped at 15.46 per cent | 28 of 71: asks A and B | exit 1 (asks re-sited) |
| 2 | 3 | Tallis capped at 15.46 per cent | 14 of 71: ask B | exit 0 |
| 2 | 4 | Tallis capped at 15.46 per cent | 14 of 71: ask B | exit 0 |

1. Decisive step announced: none, all four; each quoted policy 3.1 and Table 2 and chose the statewide share itself.
2. A file ranking the counties: none, all four.
3. Files only for the analyst: the data dictionary and the export manifest (registers the office keeps).
4. A figure or name reading as the answer: none.
5. Literal sentence: policy 3.1 with 4.1, 4.2 and 5.1 to 5.3, executed with the statewide share, giving Tallis capped;
   that is the easy route on the filed estimand, not another reading (the judge recomputed the golden from the same
   sentences twice).
6. What decided the main answer: an analytical choice, all four (estimating the returns with children); none used
   each county's own credit amount.
7. Realism: the conversion timestamps at about 05:00 on the move date and regular conversion notes, read as system
   artifacts; nothing fixed.
REVIEW lines: harmless in all four reads (digits inside larger numbers, the policy and dictionary defining the
allocation and its files, plain words in their own sense).

