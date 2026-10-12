# solver round: round 2

**Proxy score 79.7 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 37.7 of 58). Main call LANDED. 2 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Flag five series in the Q4 return, appointment views, test result views, clinic letter views, waiting list checks and digital check-ins, and notify the other five as continuous.

solver: Flag five of Drumlee's ten KPI series in the pre-notification to the programme due Friday 20 November 2026: Appointment views (+5%), Test result views (+5%), Clinic letter views (+7%), Waiting list checks (-7%) and Digital check-ins (-9%). Report Appointment change requests (-1%), Messages sent to care teams (0%), Repeat prescription requests (0%), Pre-assessment forms submitted (0%) and Notification opens (0%) as continuous. The settled changes come from 71,182 switched patients over weeks 41 to 46, with movement taken from same-segment patients still on Tallyfield who could have updated to 7.0.

tokens matched 1 of 1 (Flag)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| q4_series_break_prenotice.xlsx | 1 | 23 | 23 | 100% |
| q4_series_break_prenotice.xlsx | 2 | 14 | 15 | 93% |
| q4_prenotice_cover_note.pdf | 1 | 0 | 0 | 0% |
| q4_prenotice_cover_note.pdf | 2 | 2 | 3 | 67% |

## Solver's path

1. Release week = ISO week 41 (app_release_history.csv: 7.0.0 Android production on 2026-10-05; beta and store-review builds excluded under STD-07 2.2). Reference period W33-W40; measurement window W41-W46 (extract taken Monday 16 November).
2. Excluded 83 service accounts (service_accounts_register.xlsx) and 62 drumleehg.ie accounts (patient_app_accounts.parquet; staff test accounts per the register's Notes sheet).
3. Followed merges to the final account, including 70 merges into an already-merged account. Credited dependant rows to the carer's patient. Built the patient-week panel from app_kpi_weekly_by_account.parquet split by tracker.
4. Weekly active patient = any sign-in in the week; on new tracking = all of the patient's sign-ins on Dunnock. Gives W40-W46 counts of 87,189 to 95,957 (sum 640,890) and new-tracking counts of 15,560 to 55,940.
5. Handover week = first week with any Dunnock activity; settled weeks = later active weeks, all pure Dunnock. Switched patients = 71,182, with 184,869 settled patient-weeks.
6. Reference rate = each patient's W33-W40 events per active week. Movement per week = control events divided by the sum of control reference rates, stratified by CRM segment from crm_engagement_segments_20261001.csv ('none' for patients active only in W40). Control = active patients on all-Tallyfield in week w whose OS supports 7.0 (Android 10+ / iOS 16+); the old-OS group was excluded because its use rose faster from W41.
7. Settled change = sum(A)/sum(B) - 1: +5.11, -1.24, +4.88, +7.14, -0.14, -0.16, -7.17, -9.21, -0.30, -0.17%. Rounds to +5/-1/+5/+7/0/0/-7/-9/0/0. Unchanged under site, OS and exact-CRM-weeks stratification and under a never-switched-only control. Flags where |change| > 3 (STD-07 4.1): 5 series.
8. Q4-to-date values (STD-07 5.2): flagged series = (W40-46 Tallyfield events × (1 + rounded change) + Dunnock events) / 640,890; unflagged = recorded events / 640,890.

confidence: Medium-high. The flag set holds across every control that leaves out the old-OS group and stratifies by segment. It depends on two judgement calls, stratifying by CRM segment and leaving the old-OS patients out of the control group; a pooled or all-Tallyfield control would give a different flag set.

notes: The files don't say why old-OS patients' use rose faster from W41; I treated it as an operational effect of 6.8 being retired and left them out of the control. The filed Q3 return covers W27-W39 but the extract starts at W33, so Q3 could only be checked loosely (W33-W39 come out at roughly the filed values).

### q4_series_break_prenotice.xlsx (solver's answers)
- settled change per KPI, signed, whole %: Appointment views +5%; Appointment change requests -1%; Test result views +5%; Clinic letter views +7%; Messages sent to care teams 0%; Repeat prescription requests 0%; Waiting list checks -7%; Digital check-ins -9%; Pre-assessment forms submitted 0%; Notification opens 0%
- break flag per KPI: Yes: Appointment views, Test result views, Clinic letter views, Waiting list checks, Digital check-ins. No: Appointment change requests, Messages sent to care teams, Repeat prescription requests, Pre-assessment forms submitted, Notification opens
- Q4-to-date KPI value, events per weekly active patient, 2 dp: Appointment views 5.66; Appointment change requests 0.92; Test result views 4.75; Clinic letter views 2.32; Messages sent to care teams 1.38; Repeat prescription requests 1.43; Waiting list checks 1.42; Digital check-ins 1.11; Pre-assessment forms submitted 0.83; Notification opens 6.06 (flagged series on the new basis; denominator 640,890 weekly active patients summed over W40-W46)
- weekly active patients W40-W46: W40 87,189; W41 88,577; W42 89,973; W43 91,503; W44 92,888; W45 94,803; W46 95,957
- weekly active patients on new tracking from W41: W41 15,560; W42 27,974; W43 37,045; W44 44,405; W45 50,862; W46 55,940

### q4_prenotice_cover_note.pdf (solver's answers)
- first sentence: flagged series: Appointment views, Test result views, Clinic letter views, Waiting list checks and Digital check-ins carry a series break flag for Q4 2026
- chart bar labels: settled change per KPI against ±3% lines: Appointment views +5%; Appointment change requests -1%; Test result views +5%; Clinic letter views +7%; Messages sent 0%; Repeat prescription requests 0%; Waiting list checks -7%; Digital check-ins -9%; Pre-assessment forms 0%; Notification opens 0%; threshold lines at +3% and -3%
