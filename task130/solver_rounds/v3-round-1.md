# solver round: v3 round 1

**Proxy score 100.0 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 58.0 of 58). Main call LANDED. 4 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Certify a programme baseline of $4,060 per member per month for the 140 enrolled members ($1,438 medical, $2,622 pharmacy), built tier by tier from what the 140 members Northcourt's model flagged on 2024 claims for its 2025 proposal, never enrolled, cost from April 2025 to March 2026, trended 24 months.

solver: Certify a Programme Baseline of $4,060 PMPM across Northcourt's 140 Final Enrolment List members (medical $1,438, pharmacy $2,622; members by tier 34/37/38/31), built from the April 2025 to March 2026 experience of each risk tier of the cancelled RFP 2025-07 cohort tiered on 2024 claims (tier medical PMPM $2,660.23/$1,099.62/$578.50/$787.53, pharmacy $2,719.27/$1,965.45/$2,332.42/$1,778.69), trended 24 months at the renewal's 6.5% medical and 9.0% pharmacy, rather than the list's own regression-inflated 2026 PMPM ($4,842 medical, $3,219 pharmacy; about $8,830 trended).

tokens matched 10 of 10 (4,060, 140, 1,438, 2,622, 140, 24, Certify, Northcourt's, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| cohort_baseline_2027.xlsx | 1 | 23 | 23 | 100% |
| cohort_baseline_2027.xlsx | 2 | 5 | 5 | 100% |
| baseline_certification_memo.docx | 1 | 3 | 3 | 100% |
| baseline_certification_memo.docx | 2 | 1 | 1 | 100% |

## Solver's path

1. Read Schedule C: baseline is per tier, from the experience of members in that tier, trended by (1+trend)^(months between period midpoints / 12); trend comes from the latest renewal (6.5% medical, 9.0% pharmacy); member month means enrolled on the 1st; no rounding before the final whole-dollar figure
2. Medical file: dropped claims named as original by frequency 7 or 8 and the frequency 8 voids themselves; netting as of 31 Jan 2027 matches the renewal exactly ($34,651,441 for 2025, $32,288,225 for 2026); no allowed dollars fall outside coverage
3. Pharmacy file: summed signed GROSS_AMT_DUE (B2 reversals net out); matched to members on employee number (last 6 of CARDHOLDER_ID) + PERSON_CD with fill date inside the span, 107,747 of 107,747 matched; matches renewal $12,996,375 / $14,580,544; member months 70,904 / 71,200 match
4. Final Enrolment List (final xlsx): tiers 34/37/38/31; 2026 claims paid through 28 Feb 2027 over 2026 member months (389/429/433/361) give medical $9,613/$4,335/$3,495/$1,919 and pharmacy $2,696/$3,242/$2,551/$4,556
5. RFP 2025-07 list (2024 claims, same model and cut-offs, cancelled so no programme effect) linked to member_id through the crosswalk on subscriber number + suffix: 140/140 matched, birth dates agree; tiers 41/30/23/46
6. RFP cohort experience in its proposed programme year, Apr 2025 to Mar 2026 (member months 440/333/253/528): medical PMPM $2,660.23/$1,099.62/$578.50/$787.53, pharmacy $2,719.27/$1,965.45/$2,332.42/$1,778.69
7. Trended 24 months (1 Oct 2025 to 1 Oct 2027): x1.134225 medical, x1.1881 pharmacy, giving baselines medical $3,017/$1,247/$656/$893 and pharmacy $3,231/$2,335/$2,771/$2,113
8. Weighted by the final list's counts 34/37/38/31: medical $1,438.28, pharmacy $2,621.87, total $4,060.14, so $1,438 / $2,622 / $4,060

confidence: Medium. Every input reconciles to the renewal to the dollar and the crosswalk link is clean. The main judgment call is using the RFP cohort's April 2025 to March 2026 year: calendar 2025 trended 27 months gives about $4,427 total, and trending the list's own 2026 experience gives about $8,830.

notes: Schedule C does not name which earlier period or cohort the baseline should come from; I used the cancelled RFP's own proposed programme year because its timing matches the new programme year. Tier 3's medical baseline ($656) falls below Tier 4's ($893) on this data, which Northcourt may question.

### cohort_baseline_2027.xlsx (solver's answers)
- Enrolled members per tier: Tier 1: 34; Tier 2: 37; Tier 3: 38; Tier 4: 31; total 140
- 2026 allowed PMPM, medical, per tier: Tier 1 $9,613; Tier 2 $4,335; Tier 3 $3,495; Tier 4 $1,919 (whole dollars; incurred 2026, paid through 28 Feb 2027, not completed)
- 2026 allowed PMPM, pharmacy, per tier: Tier 1 $2,696; Tier 2 $3,242; Tier 3 $2,551; Tier 4 $4,556 (whole dollars)
- Baseline PMPM, medical, per tier: Tier 1 $3,017; Tier 2 $1,247; Tier 3 $656; Tier 4 $893 (whole dollars)
- Baseline PMPM, pharmacy, per tier: Tier 1 $3,231; Tier 2 $2,335; Tier 3 $2,771; Tier 4 $2,113 (whole dollars)
- Programme baseline across 140: Medical $1,438 PMPM; pharmacy $2,622 PMPM; total $4,060 PMPM (whole dollars, unrounded $4,060.14)

### baseline_certification_memo.docx (solver's answers)
- Total programme baseline first: Programme Baseline $4,060 PMPM total (medical $1,438, pharmacy $2,622), 140 members, Programme Year 1 Apr 2027 to 31 Mar 2028
- Chart: each tier's 2026 PMPM beside its baseline: Medical 2026 vs baseline: T1 $9,613 vs $3,017; T2 $4,335 vs $1,247; T3 $3,495 vs $656; T4 $1,919 vs $893. Pharmacy 2026 vs baseline: T1 $2,696 vs $3,231; T2 $3,242 vs $2,335; T3 $2,551 vs $2,771; T4 $4,556 vs $2,113
