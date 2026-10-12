# task230 submission

## Tags

**Domain:** Human Factors & Ergonomics (human reliability assessment: first-pass human verification of OCR-captured insurance-claim key fields).
**Analytical objective:** Data Quality Monitoring & Alerting (which client streams get second-pass verification next month).

## 1. Final Recommendation

**Put five streams on second-pass verification for November, Brightmoor Comp's first reports (BMC-FROI), Wattlebird's extras claims (WBH-EXTR), Coolabah's income protection claims (CIP-IPCL), Whinfell's pet claims (WPC-PETC) and Hollings & Pryce's typed claims (HPY-TYPD), and leave the other six off.**

Their November first-pass forecasts run 1.22 to 1.26 times their limits; the other six sit at 0.73 to 0.80. Not Kessington, Northgate and Harbison, though they ran over their limits in the third quarter: the motor claims lift the night queue's OCR error rate to 5.2% and its verifiers miss less. Not the motor claims on nights, for the same reason. Not Hollings & Pryce at its pilot residual: the diluted day queue (OCR error rate 1.9%) misses more, and QCP-04 section 4 forecasts every stream by one method.

## 2. Critical Components

1. The day queue's key-field OCR error rate falls from **4.3%** in the third quarter to **1.9%** under the November plan
2. The night queue's rises from **2.5%** to **5.2%**
3. November forecast over limit: BMC-FROI **1.22**, WBH-EXTR **1.26**, CIP-IPCL **1.25**, WPC-PETC **1.26**, HPY-TYPD **1.22**, every other stream under 1

## 3. Step-by-Step Solution

1. Kept the submitted screens in first_pass_verifications_2026q3.parquet, dated night screens to the shift's start and resolved badges to employees through workforce_register.xlsx by date.
2. Joined blind_rekey_audit_2026q3.parquet to those screens by document: OCR errors are result codes C and R, first-pass misses are R.
3. Each queue's shift-day OCR error rate is every stream's audited error share weighted by its key fields screened: 4.3% on days and 2.5% on nights over the quarter.
4. Fitted the miss log-odds on the log of that rate with form family, field type, verifier and tenure (slope 0.63); models on the attributes alone (queue, day type, time on shift, workload) do at least 1.52 times worse on held-out shift-days.
5. Rebuilt November's rates from november_operating_plan.xlsx (routing, daily key fields) and each stream's audited error rate: 1.9% on days, 5.2% on nights.
6. Forecast each stream over its November shift-days with the plan's roster and compared it with its limit in client_quality_schedules_2026.pdf under QCP-04 section 4: five streams exceed.
7. Hours are plan documents (form version key fields) times September minutes per document for the form family, each session part counted once; credit is the schedule's percentage of the November invoice at the November band with indexation; client audit rates count capture codes on claims delivered in the quarter by the client's local date, re-reviews replacing originals.
8. Recommendation: second pass for BMC-FROI, WBH-EXTR, CIP-IPCL, WPC-PETC and HPY-TYPD.

## 4. Deliverable Answers

### november_second_pass_plan.xlsx

1. Second pass in November:
   - KBA-INST (Kessington institutional claims): no
   - KBA-PROF (Kessington professional claims): no
   - NDS-DENT (Northgate dental claims): no
   - BMC-FROI (Brightmoor Comp workers' compensation first reports): yes
   - HPB-UCF (Harbison pharmacy claim forms): no
   - WBH-HOSP (Wattlebird hospital claims): no
   - WBH-EXTR (Wattlebird extras claims): yes
   - CIP-IPCL (Coolabah income protection claims): yes
   - WPC-PETC (Whinfell pet claims): yes
   - TCM-FNOL (Thistlecombe motor claims): no
   - HPY-TYPD (Hollings & Pryce typed claims): yes
2. Second-pass hours November would take, whole hours:
   - KBA-INST: 963
   - KBA-PROF: 857
   - NDS-DENT: 754
   - BMC-FROI: 340
   - HPB-UCF: 576
   - WBH-HOSP: 1,989
   - WBH-EXTR: 3,009
   - CIP-IPCL: 1,113
   - WPC-PETC: 1,682
   - TCM-FNOL: 2,168
   - HPY-TYPD: 2,449
3. Service credit at stake if the stream broke its limit in November, contract currency, whole units:
   - KBA-INST: USD 1,274
   - KBA-PROF: USD 646
   - NDS-DENT: USD 687
   - BMC-FROI: USD 745
   - HPB-UCF: USD 435
   - WBH-HOSP: AUD 3,579
   - WBH-EXTR: AUD 2,900
   - CIP-IPCL: AUD 3,069
   - WPC-PETC: GBP 1,332
   - TCM-FNOL: GBP 4,091
   - HPY-TYPD: GBP 2,644
4. Third-quarter residual as the client's own audit counted it, errors per thousand key fields, one decimal:
   - KBA-INST: 0.3
   - KBA-PROF: 0.6
   - NDS-DENT: 1.6
   - BMC-FROI: 1.3
   - HPB-UCF: 0.7
   - WBH-HOSP: 1.6
   - WBH-EXTR: 4.3
   - CIP-IPCL: 6.7
   - WPC-PETC: 3.9
   - TCM-FNOL: 14.5
   - HPY-TYPD: none, its schedule starts client audits in 2027

### second_pass_november.pptx

1. One slide charting every stream's second-pass hours against its credit at stake (credit compared at the plan's budget rates), streams ordered by credit at stake, highest first: TCM-FNOL, HPY-TYPD, WBH-HOSP, CIP-IPCL, WBH-EXTR, WPC-PETC, KBA-INST, BMC-FROI, NDS-DENT, KBA-PROF, HPB-UCF.
2. Title names TCM-FNOL (Thistlecombe motor claims) as the stream carrying the most credit at stake.
