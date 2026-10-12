# leak check, task116

**Verdict: REVIEW.** 16 files read, 48 golden figures and 21 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: academies, agreement, agreements, condition, offers, decisive, academy, asserted, clause, closed, eligibility, candidate, reading, generator, golden, prompt, planned, trust-wide, cluster, platform, graded, stopping, design, invoice, second

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `revenue_ops_export_guide.md`: candidate 'Trust Licence' sits beside decision vocabulary: ...he CRM from January 2022. `opportunity_type` is New business, Renewal, Cluster Licence or Trust Licence. `amount_gbp` is the annual value quoted. `lost_reason` is the CRM picklist value chosen...
- **REVIEW** `tb_weekly_usage_2025-09_2026-10.parquet`: golden figure 14,233 appears: ...-38,2026-09-22 06:17:00 TBS-246847,140257,2026-09-14,233,UXW-2026-38,2026-09-22 06:42:00 TBS-247138,121134...
- **REVIEW** `tb_weekly_usage_2025-09_2026-10.parquet`: golden figure 24,100 appears: ...-48,2025-12-02 06:22:00 TBS-343765,119636,2025-11-24,100,UXW-2025-48,2025-12-02 06:33:00 TBS-344454,137853...
- **REVIEW** `tb_weekly_usage_2025-09_2026-10.parquet`: golden figure 13,590 appears: ...-42,2025-10-21 06:18:00 TBS-569352,102207,2025-10-13,590,UXW-2025-42,2025-10-21 06:24:00 TBS-570315,122076...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `about_this_folder.txt`: 4 of 25 stump-paragraph terms appear (agreement, agreements, offers, platform); read whether the document names the move
- **REVIEW** `revenue_ops_export_guide.md`: 8 of 25 stump-paragraph terms appear (academies, agreement, agreements, offers, closed, cluster); read whether the document names the move
- **REVIEW** `tallybridge_trust_licence_terms_2026.pdf`: 7 of 25 stump-paragraph terms appear (academies, agreement, agreements, academy, clause, cluster); read whether the document names the move
- **REVIEW** `trust_partnerships_plan_2027.docx`: 7 of 25 stump-paragraph terms appear (academies, agreement, agreements, offers, academy, closed); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `allgroupsdata20261007.csv`: names 16 of 21 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `edubasealldata20261007.csv`: names 15 of 21 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 8 column names (REVIEW 1)
- **REVIEW** `edubasealldata20261007.csv`: Python-style nulls or booleans (nan/None/True/False) in the first rows

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `tb_agreements_2026-10-01.csv`: 2148 ISO dates after 2026-10-20, e.g. 2026-10-31, 2026-12-31, 2027-01-31, 2027-02-28, 2027-03-31
- **REVIEW** `tb_crm_opportunities_2022-2026.csv`: 67 ISO dates after 2026-10-20, e.g. 2026-10-21, 2026-10-23, 2026-10-24, 2026-10-25, 2026-10-26

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 11 prompt form (clean)
