# task455 design note

## Draw

- **Status:** paused before registration. The guard blocks the draft card on ban.pairing: survey-research-official-statistics x ETL repeats task453, which is among the last three draws. The seed's world needs the register-quality task type (vital registration as an administrative register), and no other ETL task type carries a cause-of-death certification (epidemiology has none; payment claims, test equating, data integration and emissions inventories do not hold death certificates). Re-homing it in payment claims would drop the world; recording it under a house domain that maps to SROS would dodge the ban in name only. task458 and task459 are drawn first, then this one.
- **Draft pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / ETL; the client's pattern census-register-administrative-data-quality/2 (net and gross classification error differ).
- **Draft world:** Tamsworth County Public Health Department certifies to the county council, under its opioid settlement spending plan, whether residents' opioid overdose deaths in 2026 fell at least 20 per cent below their 2021 to 2023 average; phase two of the Overdose Reduction Initiative is released on the certification. People drawn with `guard.py names --geo "United States" --seed 455`: Rebecca Barber, Patrick Elliott, Tammie Mcneil, Jesse Mcdonald (two first names WARN against older builds; redraw if still flagged).
- **Draft mechanism:** death certificates miss about one opioid overdose death in eight and certify as opioid overdoses some stimulant and other drug deaths with an incidental opioid listed, a pool that stays level while opioid deaths fall, so the certified count understates the fall; the medical examiner's record reviews (two-phase samples, 2022 and 2025) show sensitivity and specificity steady while net error and predictive values move with the count; each year corrected by the steady rates meets the target, and the certified count, the net ratio or the 2022 predictive values each fall short.
- **Data-native sentence (draft):** the false positives are drawn from the stimulant and other drug deaths, a population the initiative does not touch, so their number stays level as opioid deaths fall, and only a measurement whose error rates are estimated on records, not on totals, separates the two.

## Tried and rejected

- 2026-10-13, draw: the seed's ICD-9 to ICD-10 comparability bridge as the mechanism. Rejected: a documented-break bridge is the family task453 spent (a level shift removed before seasonal adjustment).
- 2026-10-13, draw: the provisional-count completion for deaths pending investigation. Rejected: task451's driver (a period total not yet observed, completed from the history of how amounts arrive).
- 2026-10-13, draw: survey-research-official-statistics x ETL now. Rejected by the guard (ban.pairing against task453); the build waits two draws.
