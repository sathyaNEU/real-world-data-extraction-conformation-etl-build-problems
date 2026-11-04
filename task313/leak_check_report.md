# leak check, task313

**Verdict: REVIEW.** 15 files read, 26 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: report, effect, receipt, eligible, office, window, hospital, allocation, notification, community, sentence, contact, nothing, planning, extract, health, reachable, notifications, outcomes, carries, ravensby, decision, transitional-care, reading, population

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `Neonatal outreach service specification 2027-28.pdf`: carries 18 of 19 distinctive words of the committed call: 'Give Kellingworth University Hospital 9 of the 30 outreach posts, Ravensby Royal Infirmary 7, Sedgefold Hospital 6, Wenn'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `Copperfield neonatal outreach trial final report.pdf`: 12 of 25 stump-paragraph terms appear (report, effect, eligible, office, hospital, allocation); read whether the document names the move
- **REVIEW** `Neonatal outreach service specification 2027-28.pdf`: 12 of 25 stump-paragraph terms appear (report, eligible, office, hospital, allocation, notification); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 2)
- **REVIEW** `Neonatal outreach service specification 2027-28.pdf`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `lmns_maternity_dashboard_2025-26.xlsx`: names 6 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `neonatal_paediatric_admissions_2024-04_2026-10.csv`: names 6 of 8 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `site_codes.csv`: names 6 of 8 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 1)
- **REVIEW** `rk_maternity_postnatal_discharges_2024-04_2026-10.csv`: columns a generator names and an organisation does not: NB_RISK_FLAG

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 e0d62b0dae0b29b19c5a399bde7e8b5090bc07c8fd59a404980685223a600493). Sweep 4's lines were kept out of the brief and ruled in the main thread. Verdict: no leak; the decisive step is read as an analytical choice; the realism tells below go to the generator.

1. Decisive step: spec section 7, "Each unit's share of the 30 posts follows its share of the readmissions the service is expected to avoid among the unit's eligible babies over the planning basis year." It states the allocation rule and its basis, not a hidden method. The trial report's "The effect did not differ by gestation, feeding at discharge or the primary risk reason recorded at randomisation (tests for interaction p = 0.12, 0.53 and 0.26)" and its Table 3 subgroup rate ratios (0.23 vs 0.50) are the nearest hint about how to take the effect, and read as context.
2. None. The dashboard has no ranking. The trial report's Table 3 gives pooled subgroup ratios by gestation and feeding only, not by unit. No file shares out posts.
3. newborn_risk_reasons.csv, outreach_contact_types.csv, admission_method_codes.csv and site_codes.csv are lookups. site_codes.csv is the crosswalk between the maternity-system codes (RVY, KLW), the names (Sedgefold, St Aldric's, Wennby), the community office codes and the PAS names, and exists mainly to help the analyst join.
4. None reads as the answer. Closest are the trial report's headline "a risk ratio of 0.43 (95 per cent confidence interval 0.31 to 0.61)" and "cut unplanned readmission ... by about 57 per cent". These are the published pooled effect, stated context.
5. Spec section 8: "Activity for 2027/28 is planned at the level of the twelve months to 30 September 2026: babies discharged home from 1 October 2025 to 30 September 2026 inclusive." It fixes the window and unit (babies discharged home, five units, Copperfield excluded per section 2).
   Section 3: "Every baby discharged home from the maternity units at Ravensby Royal Infirmary, Kellingworth University Hospital, Sedgefold Hospital, St Aldric's Hospital and Wennby Community Hospital with the newborn feeding or jaundice risk flag recorded on the discharge record. Twins and other multiple births are eligible." It fixes the population as flagged babies, with multiples included.
   Section 5 fixes the outcome: "A baby counts once however many admissions it has, and a transfer between hospitals during one stay is part of that admission."
   Section 7 fixes the allocation by share of expected avoided readmissions, whole posts first, then remainders to the largest fractions. The expected-avoided figure per unit is left to the analyst (baseline readmission rate x effect, grain not filed).
6. Mostly an analytical choice about how the expected avoided readmissions are estimated per unit (what baseline rate, what effect, by which risk grouping), plus stated-rule following for the allocation and window. The sentence is spec section 7 "expected to avoid among the unit's eligible babies", with the trial report's "did not differ" p-values as the pointer. The reading-a-field element (codes, unit crosswalk, twins eligible against excluded in the trial) is data mess.

a. harmless, because it gives no unit's share or post count, only the unit list, the 30 total and the allocation rule. Section 6 says posts are "sized to offer the service to every eligible baby", which is context.
b. harmless, because the monthly sheet holds births, breastfeeding, smoking, term neonatal admissions and caesarean percentages per unit, with no posts and no readmission or avoidance figures. It is a distractor.
c. harmless, because the RK extract uses upper-case headers (SITE, MRN, NB_RISK_FLAG, NB_RISK_CODES) beside the other trust's "Feeding/jaundice risk" and "Newborn risk flag". "NB_RISK_FLAG" reads as a plausible maternity-system column, with codes in the companion column. A mild tell is that the same concept is named differently per system, which is realistic.

Realism: mostly none of note. Minor tells, all low severity: (1) both PDFs have Creator and Producer set to the organisation name with no real authoring tool, PDF 1.4, untagged, tiny files (5.8 KB and 3.9 KB), with CreationDate on the round time 08:30:00 and 09:15:00 UTC. (2) The trial report's page 2 is almost empty, with a stray paragraph, "Outreach contacts were recorded by the nurses on the service tablet application; the contact log is held by ...", and a two-line conclusion. (3) Signature blocks in the spec give typed names, and the provider's director of nursing is unnamed. (4) The spec carries a version 1.2 with no revision history block. (5) Trial report Table 3 says subgroups include the primary risk reason but lists only gestation and feeding. The data files do read as different systems: RK csv with DD/MM/YYYY and upper-case headers, SW xlsx with split date and time columns, spaced NHS numbers and a schema change in the third sheet, and an MPI and notifications feed with UTC stamps.
