# leak check, task313

**Verdict: REVIEW.** 15 files read, 26 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: report, effect, receipt, eligible, window, office, hospital, sentence, allocation, community, notification, contact, nothing, planning, admissions, extract, health, reachable, notifications, outcomes, carries, ravensby, decision, transitional-care, reading

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `Neonatal outreach service specification 2027-28.pdf`: carries 18 of 19 distinctive words of the committed call: 'Give Kellingworth University Hospital 9 of the 30 outreach posts, Ravensby Royal Infirmary 7, Sedgefold Hospital 6, Wenn'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `Copperfield neonatal outreach trial final report.pdf`: 13 of 25 stump-paragraph terms appear (report, effect, eligible, office, hospital, allocation); read whether the document names the move
- **REVIEW** `Neonatal outreach service specification 2027-28.pdf`: 13 of 25 stump-paragraph terms appear (report, eligible, office, hospital, allocation, community); read whether the document names the move

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

### Second read, on the FIX_NOW cut

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 79a5e3bbe368164d434a4300b46992295945603092ac36b5396990737f71df32), after the trial report and the specification were rewritten. Sweep 4's lines were kept out of the brief and ruled in the main thread. Verdict: no leak; question 6 an analytical choice; item d (the trial report's 2.7 single-effect sentence) borderline and not a leak, since it settles the ratio and not which readmissions it applies to.

# Leak read, task313 r3 (read and quote only; nothing solved)

1. Decisive step stated? Only the spec's allocation rule, which is a procedure, not an announcement of a trap. Spec section 7 (Neonatal outreach service specification 2027-28.pdf): "Each unit's share of the 30 posts follows its share of the readmissions the service is expected to avoid among the unit's eligible babies over the planning basis year. Each unit takes the whole posts in its share; the posts left over go one at a time to the units with the largest remaining fractions." Nothing says how to carry the trial effect to the units. Closest hint (trial report s2.7): "The primary analysis estimated one treatment effect for all babies analysed as randomised... The pre-specified subgroups ... were examined only as tests for interaction and were not used to adjust or divide the primary estimate." That reads as an invitation to a single pooled ratio; it is a mild steer toward the easy route, not a stated answer.

2. Ranks or scores candidates on the question? None. The dashboard has births, breastfeeding, smoking, term neonatal-unit admissions, caesarean share only. Trial report Table 4 subgroups (RR 0.23 vs 0.50 by gestation) are trial-level, not unit-level.

3. File that exists only to help the analyst? Closest are the small lookups: newborn_risk_reasons.csv, outreach_contact_types.csv ("NA, Home visit attempted, no access"; "TNA, Telephone call, no answer"), admission_method_codes.csv, site_codes.csv. All are ordinary reference tables; none explains the method. Distractor-like: community_midwifery_establishment_2026-10.csv, lmns_maternity_dashboard_2025-26.xlsx.

4. Figure or name that reads as the answer? None. The headline "57 per cent" / "risk ratio of 0.43 (95 per cent confidence interval 0.31 to 0.61)" in the trial report is the trial's own result, context, and the pooled number is what a careless reader would apply. Spec "30 whole-time ... posts" is in the prompt.

5. Filed sentences that fix the figure or population:
- Spec s3: "Every baby discharged home from the maternity units at Ravensby Royal Infirmary, Kellingworth University Hospital, Sedgefold Hospital, St Aldric's Hospital and Wennby Community Hospital with the newborn feeding or jaundice risk flag recorded on the discharge record. Twins and other multiple births are eligible." Fixes five units (Copperfield excluded, s2 "outside this specification"), flagged babies, twins in.
- Spec s5: "An unplanned readmission is an emergency admission of the baby to any hospital in the Ravensby and Weald area within 28 days of discharge home. A baby counts once ... a transfer between hospitals during one stay is part of that admission." Fixes outcome, window, unit.
- Spec s8: "babies discharged home from 1 October 2025 to 30 September 2026 inclusive." Fixes the planning population and window.
- Spec s7: largest-remainder rounding of shares to 30 whole posts.
- Trial report s2.5: "Process measures ... home visits in which the nurse saw the baby, and telephone calls that reached a parent, in the 28 days after discharge"; "a baby counts once"; Table 2 and s3.1 define analysed babies (4,226, withdrawals removed, twins excluded).
Literal result: the unit shares are shares of expected avoided readmissions in the 12-month eligible population; the method of estimating "expected to avoid" is not filed.

6. What decides the main answer: an analytical choice. Spec s7 says "readmissions the service is expected to avoid" but no sentence says which readmissions the service can affect or how to carry the trial effect (one pooled ratio against a per-unit, per-reason or per-cause expectation). The trial report's s2.7 and Table 4 / "estimates by main risk reason are in supplementary table S2" (not shipped) leave that to the analyst. Part of the work is also rule application (spec s5, s7, s8) and data reading (flag, twins, transfers), but the open step is the estimate. No planted item seen.

## Flagged items
a. Spec PDF: harmless, because it names the five units only as the eligible list in s3, gives no share of posts, rank, score or avoided-readmission figure; "30" is already in the prompt. Its s7 rule is a procedure the analyst must still feed with data.
b. Dashboard: harmless, because it holds only monthly births, breastfeeding, smoking, term neonatal-unit admission and caesarean percentages per unit (April 2025 to March 2026); no posts, no readmissions, no ranking.
c. NB_RISK_FLAG: harmless, because it reads as a normal maternity-system extract column, sitting beside NB_RISK_CODES and uppercase like the rest (SITE, MRN, BABY_DOB_DTTM); the other trust's workbook uses "Feeding/jaundice risk" / "Newborn risk flag" (Yes/No then Y/N), which fits two different systems.
d. Trial report: partial. It does not say which readmissions the service can or cannot affect (it only says readmissions are "mostly for jaundice and for feeding problems with weight loss"). It does say how the result was estimated (one pooled effect, subgroups "not used to adjust or divide the primary estimate", s2.7) and recommends only that the board "considers the service for the other maternity units" (s5). That is context the trial authors would write, but s2.7 and the "effect did not differ" line (s3.4, s4) lean toward the pooled route; judge as borderline, not a leak of the answer.

## Realism
No file clearly reads as generated. Minor tells: both PDFs have empty Creator and Producer fields (PDF 1.4, tiny files, 4 and 2 pages, A4), probably a scrubbed library output; the spec was "Issued 20 October 2026" but the provider signs "22 October 2026" and the board approval is 15 October (plausible but odd); signature blocks are typed names only. Trial report is complete for a final report except supplementary S2 and appendix B, which it says are published separately (not in the folder). Letterhead, page footers, version block and sign-off are present in both. The organisations' files do read as different systems: RK csv (DD/MM/YYYY HH:MM, GEST "40+4", g), SW xlsx with changing layout across tabs, UTC-stamped notifications, PAS admissions, a trial-office xlsx, a LMNS dashboard.

### Third read, on the ship cut

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 2152e65ee1e724d7ebb8bc3cabda103266f137df70c02207ba7c0cf49996c853), after the prompt's closing sentence gained the rounding convention and the specification's provider signature was re-dated. Verdict: no leak; the new prompt sentence harmless; question 6 an analytical choice.

# Leak read, task313 r4

1. Decisive step named: none as a sentence. Nearest: Copperfield report 2.7 "The primary analysis estimated one treatment effect for all babies analysed as randomised... subgroups ... were examined only as tests for interaction and were not used to adjust or divide the primary estimate", and 3.4 "the estimates by main risk reason are in supplementary table S2" (S2 not shipped). These describe the trial, not the task's step.
2. Ranks or scores candidates on the prompt's question: none. The dashboard has births, breastfeeding, smoking, term NNU admissions, caesarean % by unit-month only. The trial report gives overall RR 0.43 and subgroup RRs (gestation, feeding), not by risk reason and not by unit.
3. Exists only to help the analyst: none really. Closest are the code tables (newborn_risk_reasons.csv, outreach_contact_types.csv, admission_method_codes.csv, site_codes.csv), which are ordinary lookups.
4. Reads as the answer: the report's headline "risk ratio of 0.43 (95 per cent confidence interval 0.31 to 0.61)" and "cut unplanned readmission within 28 days by about 57 per cent" are context but a pooled figure a careless solver could reuse; they are not the asked per-reason ratios. Nothing reads as a post allocation.
5. Spec section 7: "Each unit's share of the 30 posts follows its share of the readmissions the service is expected to avoid among the unit's eligible babies over the planning basis year. Each unit takes the whole posts in its share; the posts left over go one at a time to the units with the largest remaining fractions." With section 8 "babies discharged home from 1 October 2025 to 30 September 2026 inclusive", section 3 (five units, Copperfield excluded, twins eligible, flagged babies), section 5 (28-day emergency readmission, baby counts once, transfers merged). It fixes population, window, outcome and largest-remainder rounding; the expected avoided readmissions per unit is left to be estimated (the report 2.7 and S2 withhold per-reason effects). Literal result: posts proportional to each unit's expected avoided readmissions, largest remainder.
6. Decides the main answer: an analytical choice. Spec section 7 says avoided readmissions per unit, and the report 2.7 "one treatment effect for all babies" with "not used to adjust or divide the primary estimate" vs the unit case mix is the choice of how to estimate the effect and baseline risk for non-Copperfield units. Mixed with some rule application (largest remainder, stated). No planted decoy seen.

a. harmless, because it only fixes what is asked, files, and rounding ("Work every figure from the counts and round only at the end"); it names no method for the unit allocation and describes no data.
b. harmless, because the spec lists the five units only in a sentence (section 3) with no numbers beside them and no per-unit posts, shares, ranks or scores; the only figure is 30 posts total, a given. It says allocation follows expected avoided readmissions, a stated rule, not an answer.
c. harmless, because the dashboard shows births, breastfeeding, smoking, term NNU admission and caesarean percentages by unit and month, no readmission or risk-flag measure, no ranking, total row or score. (Its 2025-26 span does not match the planning window, a context mismatch, not a leak.)
d. harmless, because NB_RISK_FLAG with NB_RISK_CODES (Y/N plus semicolon codes) reads as a plausible maternity system extract field; the SW workbook equivalents ("Feeding/jaundice risk", "Newborn risk flag") are phrased differently by year, which looks organic.

Realism: none that reads as machine-generated. Minor tells: spec PDF and trial report both very tidy; the dashboard metrics are noise-like but plausible; site_codes.csv has two parallel maternity-system code columns, which looks like a real conformation aid but is the one file that exists mainly to map keys.
