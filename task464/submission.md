## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (medication adherence and persistence).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Place the 2027 statin continuity sessions at Marrick House Surgery, with Cobbet Street Surgery next in line.**
1,232 of Marrick House Surgery's 1,648 patients in the brief's population are on a statin repeat of six 56-day issues authorised in February or March 2026, so their repeats run out together before March 2027, and 12% of statin repeats that run out are not re-authorised. Not Cobbet Street Surgery, whose six-issue repeats bring its reviews round through the whole year rather than together. Not Fennbridge Medical Centre, the largest list, whose summer switch to atorvastatin re-authorised most of its statin patients for a year.

## 2. Critical Components

1. **12%** of statin repeats whose authorised issues were all issued were not re-authorised within 60 days.
2. Marrick House Surgery has **1,648** patients in the brief's population, **1,232** of them on a repeat of six 56-day issues authorised in February or March 2026.

## 3. Step-by-Step Solution

1. Stacked both systems' issue extracts through cvd_product_lookup.csv and took the patients registered on 30 November 2026 in patient_register_2026-12-01.csv who were issued a statin by that practice from 1 September to 30 November 2026: 8,648 patients across the seven practices.
2. Matched each statin repeat authorised from January 2024 in repeat_authorisations_system_a.csv and repeat_authorisations_system_b.csv whose authorised issues were all issued, the last by 3 July 2026, to a new statin repeat for the patient within 60 days of its supply running out: 12% were not re-authorised.
3. Measured stops between reviews as statin repeats left with issues unused and no statin issued for 150 days, per 28 days of statin supply, separately for a new start's first six months.
4. Ran each patient's current repeat, the one their latest statin issue was on, forward from that issue at the record's mean request interval to the request after its last authorised issue, counting a stop or a failed re-authorisation that follows a last issue before 1 March 2027 and a repeat that ran out over three weeks before the searches with no new repeat as not issued, scaled by the record's seven-month stay on the register.
5. Summed by practice: Marrick House Surgery has the largest expected number and Cobbet Street Surgery the next.
6. R1: rebuilt the dosage each ACE inhibitor or ARB issue was prescribed at by walking repeat_changes_2024-01_to_2026-11.csv back from the dosage on the authorisation, dropped the items in eps_item_cancellations_2024-2026.csv, carried supply forward within the drug and counted the days of 2025 covered per the return specification: each practice's R1 percentage below.
7. R2: took each start from the 'Ticagrelor 90mg twice daily started in secondary care' entries in cvd_clinical_events_2023-2026.csv within three days of a myocardial infarction, both inside the window, at the practice coded on the entry, and counted the patients issued ticagrelor 90mg on a day later than its first anniversary: each practice's R2 percentage below.
8. Placed the sessions at Marrick House Surgery.

## 4. Deliverable Answers

### statin_sessions_2027.xlsx

1. Patients in the brief's population, by practice:
   - Thistlecombe Surgery (P81066): 1,017
   - Pellow Green Surgery (P81177): 829
   - Larkspur Road Practice (P81283): 877
   - Fennbridge Medical Centre (P81402): 1,961
   - Marrick House Surgery (P81555): 1,648
   - Cobbet Street Surgery (P81719): 1,192
   - Wyndhollow Health Centre (P81940): 1,124
2. Sessions placed at Marrick House Surgery.
3. Runner-up: Cobbet Street Surgery.
4. Bar chart of the seven practices on the brief's figure, Marrick House Surgery highlighted, on the Placement sheet.

### cvd_repeat_returns_2025.csv

1. R1, ACE inhibitor or angiotensin II receptor blocker adherence in 2025, percentage to one decimal place:
   - Thistlecombe Surgery (P81066): 81.0
   - Pellow Green Surgery (P81177): 80.3
   - Larkspur Road Practice (P81283): 81.9
   - Fennbridge Medical Centre (P81402): 77.8
   - Marrick House Surgery (P81555): 79.9
   - Cobbet Street Surgery (P81719): 75.8
   - Wyndhollow Health Centre (P81940): 92.9
2. R2, ticagrelor 90mg issued after the first anniversary of starting it, percentage to a whole number:
   - Thistlecombe Surgery (P81066): 82
   - Pellow Green Surgery (P81177): 83
   - Larkspur Road Practice (P81283): 83
   - Fennbridge Medical Centre (P81402): 71
   - Marrick House Surgery (P81555): 84
   - Cobbet Street Surgery (P81719): 58
   - Wyndhollow Health Centre (P81940): 55
