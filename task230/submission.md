# task230 submission

## Tags

**Domain:** Human Factors & Ergonomics (human reliability assessment: first-pass human verification of OCR-captured insurance-claim key fields).
**Analytical objective:** Data Quality Monitoring & Alerting (which client streams get second-pass verification next month).

## 1. Final Recommendation

**Put five streams on second-pass verification for November, Brightmoor Comp's first reports (BMC-FROI), Wattlebird's extras claims (WBH-EXTR), Coolabah's income protection claims (CIP-IPCL), Whinfell's pet claims (WPC-PETC) and Hollings & Pryce's typed claims (HPY-TYPD), and leave the other six off.**

Their November first-pass forecasts run more than 1.1 times their limits; the other six sit below 0.9 times theirs. Not Kessington, Northgate and Harbison, though they ran over their limits in the third quarter: the motor claims lift the night queue's OCR error rate to 5.2% and its verifiers miss less. Not the motor claims on nights, for the same reason. Not Hollings & Pryce at its pilot residual: the diluted day queue (OCR error rate 1.9%) misses more, and QCP-04 section 4 forecasts every stream by one method.

## 2. Critical Components

1. The day queue's key-field OCR error rate falls from **4.3%** in the third quarter to **1.9%** under the November plan
2. The night queue's rises from **2.5%** to **5.2%**
3. November forecast over limit: BMC-FROI, WBH-EXTR, CIP-IPCL, WPC-PETC and HPY-TYPD above **1.1**, every other stream below **0.9**

## 3. Step-by-Step Solution

1. Kept the submitted screens in first_pass_verifications_2026q3.parquet, dated night screens to the shift's start and resolved badges to employees through workforce_register.xlsx by date.
2. Joined blind_rekey_audit_2026q3.parquet to those screens by document: OCR errors are result codes C and R, first-pass misses are R.
3. Each queue's shift-day OCR error rate is every stream's audited error share weighted by its key fields screened: 4.3% on days and 2.5% on nights over the quarter.
4. Fitted the miss log-odds on the log of that rate with form family, field type, verifier and tenure (slope -0.63: verifiers miss more as the queue's error rate falls); models on the attributes alone (queue, day type, time on shift, workload) fit held-out shift-days worse, and their queue term vanishes once the rate is in.
5. Rebuilt November's rates from november_operating_plan.xlsx (routing, daily key fields) and each stream's audited error rate: 1.9% on days, 5.2% on nights.
6. Forecast each stream's own documents over its November shift-days with the plan's roster and compared it with its limit in client_quality_schedules_2026.pdf under QCP-04 section 4: five streams exceed.
7. Hours are plan documents (key fields over the form version's key fields per document) times September minutes per document for the form family, each document's stream taken from the first-pass log by document_id, every handling line counted and each document once; client-audit residuals count capture-code findings, re-reviews replacing originals, on sampled claims delivered in July to September by the manifests' transmission time in the client's zone, over the key fields on every document of each claim in delivery_index_2026q3.parquet (key fields per document from form_specifications.xlsx for the version in force on the claim's shift-day).
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
   - KBA-INST: 985
   - KBA-PROF: 882
   - NDS-DENT: 771
   - BMC-FROI: 348
   - HPB-UCF: 589
   - WBH-HOSP: 2,035
   - WBH-EXTR: 3,097
   - CIP-IPCL: 1,139
   - WPC-PETC: 1,731
   - TCM-FNOL: 2,217
   - HPY-TYPD: 2,526
3. Third-quarter residual as the client's own audit counted it, errors per thousand key fields, two decimals:
   - KBA-INST: 0.14
   - KBA-PROF: 0.97
   - NDS-DENT: 1.29
   - BMC-FROI: 1.45
   - HPB-UCF: 0.19
   - WBH-HOSP: 1.52
   - WBH-EXTR: 3.89
   - CIP-IPCL: 5.73
   - WPC-PETC: 4.27
   - TCM-FNOL: 14.53
   - HPY-TYPD: none, its client audits start in 2027

### second_pass_november.pptx

1. One slide charting every stream's second-pass hours, most to fewest: WBH-EXTR, HPY-TYPD, TCM-FNOL, WBH-HOSP, WPC-PETC, CIP-IPCL, KBA-INST, KBA-PROF, NDS-DENT, HPB-UCF, BMC-FROI.
2. Title names WBH-EXTR (Wattlebird extras claims) as the stream that would take the most hours.
