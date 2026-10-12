# solver round: round 1

**Proxy score 80.7 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 38.7 of 58). Main call LANDED. 2 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Flag four series in the Q4 return, appointment views, clinic letter views, waiting list checks and digital check-ins, and notify the other six as continuous.

solver: Flag four of Drumlee's ten series in the Q4 pre-notification: Appointment views (+6%), Clinic letter views (+7%), Waiting list checks (-7%) and Digital check-ins (-9%) all exceed the 3% NPAP-STD-07 threshold for the 77,045 switched patients over ISO weeks 41-46 against reference weeks 33-40, with the counterfactual trended by CRM engagement segment; Appointment change requests (-1%), Test result views (-1%), Messages sent (0%), Repeat prescription requests (0%), Pre-assessment forms (0%) and Notification opens (+1%) are published as continuous.

tokens matched 1 of 1 (Flag)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| q4_series_break_prenotice.xlsx | 1 | 22 | 22 | 100% |
| q4_series_break_prenotice.xlsx | 2 | 15 | 15 | 100% |
| q4_prenotice_cover_note.pdf | 1 | 0 | 0 | 0% |
| q4_prenotice_cover_note.pdf | 2 | 2 | 3 | 67% |

## Solver's path

1. Release week from app_release_history.csv: 7.0.0 Android production 2026-10-05 = ISO W41 (betas and store review excluded per STD-07 2.2); reference W33-W40; measurement window W41-W46 (extract taken Mon 16 Nov)
2. Excluded the 83 service_accounts_register.xlsx accounts plus the 62 drumleehg.ie accounts in patient_app_accounts.parquet (145 in total)
3. Mapped dependants to carer_ref and merged accounts through merged_into chains (70 two-step chains) to the surviving account, applied to every week
4. Aggregated app_kpi_weekly_by_account.parquet to patient-week: weekly active patients W40-46 = 87,096 to 95,943; on new tracking (no Tallyfield sign-ins) W41-46 = 16,929 to 60,836; Q4-to-date denominator 640,670
5. Handover week = first week with a Dunnock row; settled weeks = active weeks after handover to W46; switched patients = active in W33-40 with at least one settled week: 77,045 patients and 200,194 settled patient-weeks
6. Baseline = each patient's events per active week in W33-40; trend index by crm_engagement_segments_20261001.csv segment and week from patients still on Tallyfield (occasional index rises to about 1.6 by W46, frequent stays about 0.98)
7. B = sum of baseline x segment-week index over settled weeks; A = Dunnock events in settled weeks; settled change = A/B-1: +5.78, -1.20, -0.87, +7.29, +0.27, -0.22, -7.19, -9.20, -0.20, +0.81%
8. Robustness: a never-switched control or a group-rate index moves each change by less than 0.5 points and no flag changes; pooled and no-trend variants rejected because they flip the flags

confidence: High on the flag set: four KPIs are 2.8 to 6.2 points beyond the threshold and the six unflagged ones sit within 1.2% under every segment-stratified variant. Moderate only on whether the intended counterfactual is the segment-stratified trend; a pooled or no-trend B gives a different flag set.

notes: Patients with no CRM segment (650 of the switched patients) were treated as their own stratum; counting them as occasional changes nothing. The Q3 return can't be reconciled exactly because the extract starts at W33, and Appointment views' Q4-to-date value of 5.4695 sits on the rounding edge to 5.47.

### q4_series_break_prenotice.xlsx (solver's answers)
- Settled change per KPI, signed, nearest whole %: Appointment views +6%; Appointment change requests -1%; Test result views -1%; Clinic letter views +7%; Messages sent to care teams 0%; Repeat prescription requests 0%; Waiting list checks -7%; Digital check-ins -9%; Pre-assessment forms submitted 0%; Notification opens +1%
- Break flag per KPI: Yes: Appointment views, Clinic letter views, Waiting list checks, Digital check-ins. No: Appointment change requests, Test result views, Messages sent to care teams, Repeat prescription requests, Pre-assessment forms submitted, Notification opens
- Q4-to-date KPI value (events per weekly active patient, 2 dp): Appointment views 5.47; Appointment change requests 0.91; Test result views 4.46; Clinic letter views 2.24; Messages sent to care teams 1.38; Repeat prescription requests 1.43; Waiting list checks 1.47; Digital check-ins 1.16; Pre-assessment forms submitted 0.83; Notification opens 6.02 (weeks 40-46, denominator 640,670 active patient-weeks)
- Weekly active patients, ISO weeks 40-46: W40 87,096; W41 88,550; W42 89,949; W43 91,444; W44 92,909; W45 94,779; W46 95,943
- Weekly active patients on new tracking, weeks 41-46: W41 16,929; W42 30,510; W43 40,286; W44 48,352; W45 55,265; W46 60,836

### q4_prenotice_cover_note.pdf (solver's answers)
- First sentence naming flagged series: Four series carry a break flag: Appointment views (+6%), Clinic letter views (+7%), Waiting list checks (-7%) and Digital check-ins (-9%)
- Chart of settled change vs +/-3% lines, bars labelled: Ten bars labelled +6%, -1%, -1%, +7%, 0%, 0%, -7%, -9%, 0%, +1% (Appointment views, Appointment change requests, Test result views, Clinic letter views, Messages sent, Repeat prescription requests, Waiting list checks, Digital check-ins, Pre-assessment forms, Notification opens) with reference lines at +3% and -3%
