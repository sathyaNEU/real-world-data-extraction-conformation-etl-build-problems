# solver round: round 2

**Proxy score 24.7 / 100** (recommendation 3.3 of 35, instruction 7.0 of 7, asks 14.4 of 58). Main call missed. 0 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Put a 2027 caseload of 133 groups to the committee: 133 of the 913 obligor groups in the monitored book at 30 September 2026 are expected to reach the watch list by 30 September 2027.

solver: 73 of the 913 obligor groups in the 30 September 2026 monitored book are expected to reach the watch list by 30 September 2027 (exactly 72.916): 62.3 from the 165 groups flagged in the September 2026 early-warning run at 157/416 = 0.3774 each and 10.6 from the 748 unflagged groups at 44/3092 = 0.01423 each. This flag-split basis beat a single book-wide rate on leave-one-cohort-out error over the 2022-2025 cohorts (worst miss 40.6% against 55.6%). The arrivals bring £2,208.0m of expected committed exposure, which is 6.1 analysts at twelve groups each, so 7 if rounded up.

tokens matched 4 of 6 (133, 133, 913, 30, 30, September)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| watchlist_inflow_2027.xlsx | 1 | 0 | 4 | 0% |
| watchlist_inflow_2027.xlsx | 2 | 10 | 26 | 38% |
| watchlist_inflow_2027.xlsx | 3 | 3 | 6 | 50% |
| watchlist_inflow_2027.svg | 1 | 0 | 0 | 0% |
| watchlist_inflow_2027.svg | 2 | 0 | 1 | 0% |
| watchlist_inflow_2027.svg | 3 | 3 | 5 | 60% |

## Solver's path

1. Monitored book per CRM-07 4.1, 4.2: cohorts 2022 846/119/58/17, 2023 871/98/32/11, 2024 889/95/28/8, 2025 902/104/39/8, 2026 913/165
2. Members per 2.2 incl. GLEIF ultimate and direct chains; 14 unbooked customers linked via GLEIF
3. Flags per 3.2 by LEI or CRN: 165 flagged at 2026-09-30
4. Basis per 5.2: leave-one-cohort-out over flag-split pooled rates vs single book rate; flag-split wins (40.6% vs 55.6%); p flagged 0.3774, p unflagged 0.01423
5. Exposure per 6.1 at end of 30 Sep UK time (before 23:00 UTC), excluding the 23:30 UTC start-of-day batch; each facility once per group; Treasury rates
6. Bands per 6.2: totals 72.916 -> 73; exposure 2,208.0

confidence: High on 73; medium-high on band split

notes: History starts Jan 2020; 2026 flag jump used as published.

### watchlist_inflow_2027.xlsx (solver's answers)
- headline caseload: Caseload = 73 groups (whole number; unrounded 72.916)
- band under £5m: groups 201; committed exposure £475.8m; expected arrivals flagged 12.8, not flagged 2.4 (total 15.2); exposure arrivals bring £38.2m
- band £5m to under £15m: groups 306; committed exposure £3,016.2m; expected arrivals flagged 20.4, not flagged 3.6 (total 24.0); exposure arrivals bring £223.7m
- band £15m to under £40m: groups 250; committed exposure £7,153.8m; expected arrivals flagged 17.7, not flagged 2.9 (total 20.6); exposure arrivals bring £612.0m
- band £40m to under £100m: groups 120; committed exposure £8,213.8m; expected arrivals flagged 7.5, not flagged 1.4 (total 9.0); exposure arrivals bring £609.7m
- band £100m and over: groups 36; committed exposure £6,640.9m; expected arrivals flagged 3.8, not flagged 0.4 (total 4.1); exposure arrivals bring £724.4m
- total row: groups 913; committed exposure £25,500.5m; expected arrivals flagged 62.3, not flagged 10.6, total 72.9; exposure arrivals bring £2,208.0m

### watchlist_inflow_2027.svg (solver's answers)
- stacked bars per band, flagged / not flagged: under £5m 12.8/2.4; £5m to under £15m 20.4/3.6; £15m to under £40m 17.7/2.9; £40m to under £100m 7.5/1.4; £100m and over 3.8/0.4 (expected groups, 1 dp)
- caseload on chart and quotable title: Caseload 73 groups; title: '73 monitored groups expected to reach the watch list by 30 September 2027, 62 of them already flagged in September's early-warning run'
