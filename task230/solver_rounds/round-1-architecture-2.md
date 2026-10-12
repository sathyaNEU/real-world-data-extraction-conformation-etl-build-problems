# solver round: round 1 (architecture 2)

**Proxy score 62.7 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 53.2 of 58). Main call missed. 5 of 6 ask items cracked (80 per cent of tokens). Ask share kept 92%. Gate: ASKS LEAK.

## Main call

golden: Put five streams on second-pass verification for November, Brightmoor Comp's first reports (BMC-FROI), Wattlebird's extras claims (WBH-EXTR), Coolabah's income protection claims (CIP-IPCL), Whinfell's pet claims (WPC-PETC) and Hollings & Pryce's typed claims (HPY-TYPD), and leave the other six off.

solver: Put six streams on second-pass verification for November: KBA-INST, KBA-PROF, NDS-DENT, BMC-FROI and HPB-UCF, because the November night queue (now including TCM-FNOL) forecasts 8.851 errors per 1,000 key fields, above their limits of 2.0, 5.2, 8.3, 7.4 and 2.3; and HPY-TYPD, because the day queue forecasts 2.521, above its 0.77 limit. Keep WBH-HOSP (3.8), WBH-EXTR (4.6), CIP-IPCL (8.3), WPC-PETC (5.1) and TCM-FNOL (18.9) off. The six streams need about 5,939 second-pass hours, and Thistlecombe Motor's TCM-FNOL carries the largest credit at stake, GBP 4,091 (about INR 456,506).

tokens matched 6 of 12 (November, Brightmoor Comp's, BMC-FROI, Wattlebird's, WBH-EXTR, Coolabah's, CIP-IPCL, Whinfell's, WPC-PETC, Hollings, Pryce's, HPY-TYPD)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| november_second_pass_plan.xlsx | 1 | 12 | 22 | 55% |
| november_second_pass_plan.xlsx | 2 | 22 | 22 | 100% |
| november_second_pass_plan.xlsx | 3 | 23 | 24 | 96% |
| november_second_pass_plan.xlsx | 4 | 21 | 21 | 100% |
| second_pass_november.pptx | 1 | 11 | 11 | 100% |
| second_pass_november.pptx | 2 | 3 | 3 | 100% |

## Solver's path

1. Q3 stream residuals: blind_rekey_audit_2026q3.parquet, (R+V)/audited key fields x1000, every audited document matched to its submitted first-pass screen. KBA-INST 2.256, KBA-PROF 5.786, NDS-DENT 9.371, BMC-FROI 12.210, HPB-UCF 2.563, WBH-HOSP 1.883, WBH-EXTR 3.807, CIP-IPCL 6.932, WPC-PETC 4.269, TCM-FNOL 15.533, HPY-TYPD 0.688.
2. QCP-04 4.1 read literally (residual over every document the plan routes to the stream's queue), with November routing from november_operating_plan.xlsx (TCM-FNOL on Night, HPY-TYPD on Day). Each queue rate is the Q3 stream rates weighted by November plan key fields: Night 18,258.7 errors / 2,062,787 key fields = 8.851; Day 10,353.4 / 4,106,283 = 2.521. Compared with the limits in client_quality_schedules_2026.pdf using strict greater-than, giving six streams ON.
3. Checked for verifier, tenure or roster effects (badge resolved to employee by validity date, then rota and November roster): day and night verifiers both run at 1.00 of expected errors, so no other mechanism changes the queue forecast.
4. November documents: plan daily key fields divided by key fields per document of the form version in force each shift-day (form_specifications.xlsx; KBA-PROF 12 from 16 Nov, WBH-EXTR 9 from 9 Nov, WPC-PETC 11 from 16 Nov, HPY-TYPD 13 from 23 Nov, NDS-DENT 13, CIP-IPCL 16). KBA-INST 37,250; KBA-PROF 24,470; NDS-DENT 14,814; BMC-FROI 6,689; HPB-UCF 22,288; WBH-HOSP 76,960; WBH-EXTR 85,919; CIP-IPCL 21,886; WPC-PETC 48,036; TCM-FNOL 42,610; HPY-TYPD 122,421.
5. Minutes per document: second_pass_sessions_2026_09.csv, productive_min counted once per (session_ref, half_shift) because it repeats on every document row, divided by documents worked, by form family. Printed 1.5510, mixed 2.1010, handwritten 3.0522, typed (HPY pilot) 1.2003. Hours = documents x minutes / 60.
6. Invoice = November documents x unit price at the band set by the account's November documents (client_rate_cards_2026.pdf). KBA 61,720 = K2 (0.57/0.44); WBH 162,879 = T3 (0.62/0.45); HPY Band 3 0.24; TCM Plus 0.80; NDS S 0.58; BMC Std 1.10; HPB A 0.39; CIP Base 1.36; WPC A 0.34. Indexation for documents from the anniversary shift-day: BMC 1.1374 from 20 Nov, CIP 1.4158 from 9 Nov, WPC 0.3533 from 16 Nov. Credit = schedule percentage x invoice; ranked at the budget INR rates in the plan.
7. Client-audit Q3 residuals: all audit timestamps are UTC (matched to transmitted_at in delivery_manifests_2026q3.csv), converted to each contract's zone and filtered to delivery dates 1 Jul to 30 Sep. Only the latest or active review of each finding counts, and only the schedule's capture codes. Denominator is key fields per claim by form version (Kessington Form column; NDS 13 from shift-day 10 Aug, CIP 16 from 1 Sep via batch shift date). Errors over key fields: KBA-INST 7/22,512; KBA-PROF 6/10,318; NDS 17/10,785; BMC 13/10,185; HPB 7/9,990; WBH-HOSP 40/24,648; WBH-EXTR 68/15,872; CIP 128/19,117; WPC 93/24,050; TCM 387/26,730; HPY 49/71,196 from the blind re-key audit.

confidence: Medium-high. All figures reproduce exactly. The main call depends on reading QCP-04 4.1 at queue level, which is what puts HPY-TYPD on; a stream-by-stream reading would drop it and leave the five night streams.

notes: The plan of record carries the R2 client forecasts, not the later R3 revisions; I used the plan, as QCP-04 and the labour planning note require. Each indexation clause was applied only to the client block it sits under in the rate-card PDF (Brightmoor, Coolabah, Whinfell), and Wattlebird's T3 band clears its threshold by only 879 documents.

### november_second_pass_plan.xlsx (solver's answers)
- November second-pass call: ON: KBA-INST, KBA-PROF, NDS-DENT, BMC-FROI, HPB-UCF, HPY-TYPD. OFF: WBH-HOSP, WBH-EXTR, CIP-IPCL, WPC-PETC, TCM-FNOL. Forecast residual per 1,000 key fields: night queue 8.851, day queue 2.521.
- Second-pass hours, November (nearest hour): KBA-INST 963 h; KBA-PROF 857 h; NDS-DENT 754 h; BMC-FROI 340 h; HPB-UCF 576 h; WBH-HOSP 1,989 h; WBH-EXTR 3,009 h; CIP-IPCL 1,113 h; WPC-PETC 1,682 h; TCM-FNOL 2,168 h; HPY-TYPD 2,449 h. Total for the six ON streams 5,939 h.
- Credit at stake if the limit is broken in November (whole contract currency units): KBA-INST USD 1,274; KBA-PROF USD 646; NDS-DENT USD 687; BMC-FROI USD 745; HPB-UCF USD 435; WBH-HOSP AUD 3,579; WBH-EXTR AUD 2,900; CIP-IPCL AUD 3,069; WPC-PETC GBP 1,332; TCM-FNOL GBP 4,091; HPY-TYPD GBP 2,644
- Q3 residual as the client's audit counted it (errors per 1,000 key fields, 1 dp): KBA-INST 0.3; KBA-PROF 0.6; NDS-DENT 1.6; BMC-FROI 1.3; HPB-UCF 0.7; WBH-HOSP 1.6; WBH-EXTR 4.3; CIP-IPCL 6.7; WPC-PETC 3.9; TCM-FNOL 14.5; HPY-TYPD 0.7 (supplier blind re-key audit, which is the contract measure until 2027)

### second_pass_november.pptx (solver's answers)
- Chart of hours against credit at stake, ordered by credit (budget INR rates for ordering): Order by credit in INR: TCM-FNOL (GBP 4,091; 2,168 h), HPY-TYPD (GBP 2,644; 2,449 h), WBH-HOSP (AUD 3,579; 1,989 h), CIP-IPCL (AUD 3,069; 1,113 h), WBH-EXTR (AUD 2,900; 3,009 h), WPC-PETC (GBP 1,332; 1,682 h), KBA-INST (USD 1,274; 963 h), BMC-FROI (USD 745; 340 h), NDS-DENT (USD 687; 754 h), KBA-PROF (USD 646; 857 h), HPB-UCF (USD 435; 576 h)
- Title naming the stream with the most credit: Thistlecombe Motor TCM-FNOL carries the most credit at stake: GBP 4,091 (about INR 456,506 at the budget rate of 111.6)
