# leak check, task197

**Verdict: REVIEW.** 11 files read, 7 golden figures and 16 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: second, window, months, carries, device, record, exposures, traverse, exposure, seconds, counts, published, extract, register, measured, inside, export, population, sentence, checks, printed, clause, episodes, archive, delivery

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `network/case_export_watched_products.csv`: golden figure 40864 appears: ...01 06:04,Own residence,1,20,Female,1,EMBERCALM,MP-40864,Unintentional - general,Ingestion,Managed on site...
- **REVIEW** `network/case_export_watched_products.csv`: golden figure 40211 appears: ...1 16:19,Own residence,9,,Female,1,FEVERKIND JR,MP-40211,Adverse reaction - drug,Ingestion,Already in or e...
- **REVIEW** `register/watched_products_register.xlsx`: golden figure 40864 appears: ...hild-resistant dropper bottle, new tamper band MP-40864 Embercalm Nicotine Polacrilex Lozenge Mint Holbro...
- **REVIEW** `register/watched_products_register.xlsx`: golden figure 40211 appears: ...e form Pack UPC First marketed Current closure MP-40211 Feverkind Junior Strength Acetaminophen Oral Susp...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `packaging_review/crp_referral_procedure_issue4.pdf`: 6 of 25 stump-paragraph terms appear (months, record, exposures, exposure, counts, register); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `register/watched_products_register.xlsx`: names 11 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `hospitals/network_hospitals.csv`: names 4 of 16 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `packaging_review/adverse_event_reports_watched_products.csv`: names 11 of 16 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)
