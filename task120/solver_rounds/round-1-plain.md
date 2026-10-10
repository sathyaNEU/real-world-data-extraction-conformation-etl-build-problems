# solver round: round 1, plain

**Proxy score 96.8 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 54.8 of 58). Main call LANDED. 8 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Adopt TY2025 tier floors of $214,000, $318,000 and $742,000 for the top 10, 5 and 1 per cent of full-year resident household units.

solver: Adopt the TY2025 income-tax tier floors of $214,000 (top 10 per cent), $318,000 (top 5 per cent) and $742,000 (top 1 per cent). They are drawn on 582,544 full-year resident household units: a federal unit with both spouses' separate state returns merged, plus the returns filed by its claimed dependents. This construction rebuilds all 69 of 69 published Household Income Tables cells for 2022 to 2024. Manuel's raw-return count ($179k/$262k/$551k) and the LFO's federal-unit basis ($197k/$293k/$594k) both miss the published tables.

tokens matched 5 of 5 (214,000, 318,000, 742,000, 5, Adopt)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| tier_schedule.xlsx | 1 | 7 | 7 | 100% |
| tier_schedule.xlsx | 2 | 4 | 4 | 100% |
| tier_schedule.xlsx | 3 | 21 | 21 | 100% |
| tier_schedule.xlsx | 4 | 6 | 6 | 100% |
| tier_schedule.xlsx | 5 | 8 | 8 | 100% |
| tier_floors.png | 1 | 1 | 2 | 50% |
| tier_floors.png | 2 | 3 | 3 | 100% |
| tier_floors.png | 3 | 4 | 4 | 100% |
| tier_floors.png | 4 | 3 | 3 | 100% |

## Solver's path

1. Read the methodology PDF, the record layouts and the correspondence. Tiers are drawn on full-year resident household units at the 10/5/1% marks, every unit counts, and adoption requires reproducing every published cell of the HIT 2022-2024.
2. Tested unit definitions against household_income_tables_ty2022-2024. Raw returns matched 1/19 per year and federal units (filer_tin grouped with federal_primary_tin) matched 17/19. Federal units plus each dependent's own return, joined through dependents_schedule dependent_tin = filer_tin (union-find), matched 19/19 in every year. The 2024 Appendix A matched 12/12 when county comes from the unit's federal-primary non-dependent return, so 69/69 overall.
3. Built TY2025 the same way from returns_processed_ty2025 and dependents_schedule_ty2025, keeping residency_code=1 (no unit mixes residencies). This gives 582,544 units. The 10/5/1% rank values are 214,063, 318,081 and 742,043, which round to $214k/$318k/$742k under every quantile convention.
4. Checked the processed file is as of record: the latest ACCEPTED amended version's AGI equals the processed AGI on all 27,664 amended returns. Capital gain uses amount_in_agi from the version of record. Rows come from the amended log where a return was amended (blank = 0), otherwise from schedule_d_extract. This gives $5,113,633,720 in total, against $4,826,549,546 if latest-received versions are used naively.
5. Withholding: 1,083,466 efile statements plus 73,102 paper statements parsed by fixed width. Both channels tie to the employer reconciliations ($1,394,690,352 + $93,587,882). Statements were mapped to units by filer_tin or spouse_tin, plus RESOLVED WAGE_STATEMENT TIN cases. OPEN cases and 13,839 statements from non-filers were left unattributed.
6. Estimated tax: TY2025 ES payments plus 5,511 payments ($10,172,700) misposted to 2024 and transferred in, timed at their original receipt. I excluded the 13,035 overpayment-credit transfers from 2024 returns ($18,265,400). I removed 11,148 returned items unless they were re-presented PAID (2,818 items, $5,069,530). Payments map to units through resolved PAYMENT TIN cases; 803 open-case payments ($1,378,260) stay unattributed.
7. Instalments: UTC was converted to Central time and compared against due dates of 2025-04-15, 2025-06-16 (June 15 is a Sunday), 2025-09-15 and 2026-01-15 at 23:59:59. Each payment goes to the first due date it arrives by, and Q4 also takes later receipts. Statewide: Q1 $110,937,650, Q2 $117,082,790, Q3 $115,695,320, Q4 $120,589,530.
8. Tiers use the rounded floors: T1 AGI >= 742,000; T2 318,000-741,999; T3 214,000-317,999. I summed receipts, withholding and capital gain by tier, and the shares are 30.4%, 10.1% and 4.5% of tier AGI.

confidence: High on the floors, because the construction reproduces all 69 published cells. Medium-high on the tier-base asks, which depend on the treatment of returned items and transfers.

notes: I assumed no state holidays fall on the due dates, since the folder lists none. Timing of re-presented PAID items makes no difference to any instalment. The 13,839 wage statements with no filer and no TIN case carry $1,476,307 of withholding, and I left them out of the tiers.

### tier_schedule.xlsx (solver's answers)
- 2025 tier schedule (floors, nearest $1,000): Tier 3 (10% floor) $214,000; Tier 2 (5% floor) $318,000; Tier 1 (1% floor) $742,000. Unrounded rank values are $214,063, $318,081 and $742,043, from N=582,544 units. Tier unit counts are T1 5,826, T2 23,302 and T3 29,127. Tier AGI is T1 $10,356,865,342, T2 $9,837,059,854 and T3 $7,492,715,926.
- Published 2022-2024 cells rebuilt and match count: 69 of 69 published cells match. Table 1 has 9 classes x (units + AGI $000) + total AGI = 19 cells per year, so 57 cells, and every one matches. 2024 Appendix A adds 12 county counts, with the county taken from the federal-primary non-dependent return, and all 12 match. Totals in $ thousands: 2022 55,604,953; 2023 58,991,964; 2024 63,898,078.
- 2025 estimated-tax receipts by instalment per tier (whole $): Tier 1: Q1 (Apr 15) $57,100,430; Q2 (Jun 16) $60,982,470; Q3 (Sep 15) $59,690,330; Q4 (Jan 15 2026 + later) $62,279,690. Tier 2: $27,130,950; $28,344,190; $28,273,480; $29,413,200. Tier 3: $12,597,420; $13,026,520; $13,083,940; $13,625,350.
- 2025 withholding per tier (whole $): Tier 1 $135,364,253; Tier 2 $229,035,640; Tier 3 $184,720,391
- 2025 net capital gain per tier (whole $) and share of tier AGI (1 dp): Tier 1 $3,147,270,635, 30.4%; Tier 2 $995,783,766, 10.1%; Tier 3 $339,052,645, 4.5%

### tier_floors.png (solver's answers)
- Floors drawn as vertical lines, band labels and title: The chart is a log-log plot of the count of units at or above each AGI from $100,000 up. Vertical lines mark $214,000, $318,000 and $742,000. Band labels are Tier 3 CG share 4.5%, Tier 2 10.1% and Tier 1 30.4%. Title: TY2025 tiers: $214,000 / $318,000 / $742,000.
