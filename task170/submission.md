## Tags

**Domain:** Epidemiology and public health (health burden and impact modelling).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**The March 2027 LulaNet R campaign will avert about 11,000 Ombeni fever cases among the people sleeping under its nets in Ruvari County from April to December 2027, 21 per cent of the 53,042 the county expects.**
It rests on a per-bite protection of 0.80 against the 0.36 of a resident's bites that arrive in bed. Not the trial's pooled 56.7 per cent efficacy (about 22,000 cases averted), which was measured where most bites arrived after people were in bed.

## 2. Critical Components

1. The per-bite protection the five KINGA-5 sites share is **0.80**.
2. The share of a Ruvari resident's exposure that arrives in bed is **0.36**.

## 3. Step-by-Step Solution

1. Read each KINGA-5 site's protective efficacy from Table 1 of kinga5_final_report_2024.pdf (pooled 56.7 per cent) and its share of bites in bed from Tables 2a to 3b (bites indoors at each hour times members in bed, over bites indoors times members indoors plus bites outdoors times members outdoors).
2. Fitted each site's efficacy as a multiple of its in-bed share through the origin, weighted by the inverse variance of the site's efficacy: a per-bite protection of 0.80.
3. Built the county's An. ruvariensis landings per minute collected by hour and position from hlc_sentinel_2024_2026.csv (re-keyed sheets counted once, rows with no catch dropped).
4. Read members indoors and in bed at each half hour from both rounds of human_behaviour_survey_2025.xlsx, and computed the county's in-bed share the same way as the sites': 0.36.
5. Multiplied each sub-county's expected cases by month in obf_planning_baseline_2027.xlsx by the planned use in Table 2 of lulanet_r_distribution_plan_2027.docx and by the per-bite protection times the in-bed share: 11,000 cases averted, 21 per cent of 53,042.
6. Nets from nets_registration_2026.parquet under the plan's allocation rule, with replayed records counted once and each mop-up registration matching a main-round household on its ward, dwelling mark, usual members, under-fives and sleeping spaces counted as that household.
7. Confirmed cases January to September 2026 from khis_moh705_obf_2024_2026.csv by each facility's sub-county in facility_list_2026.csv, the June 2026 re-entry of the realigned ward's returns counted once, and the parent hospitals' January to March 2026 returns marked as including outreach net of their outreach clinics' own returns.
8. The campaign will avert about 11,000 Ombeni fever cases among net users from April to December 2027.

## 4. Deliverable Answers

### ruvari_cases_averted_2027.xlsx

1. Cases averted among net users, April to December 2027, county: 11,000
2. Share of the county's expected cases in the period: 21 per cent
3. Cases averted by sub-county, to the nearest hundred:
   - Ruvari Town: 1,500
   - Mwiri: 1,800
   - Kendagi: 1,400
   - Oyamo: 2,200
   - Ndira: 1,200
   - Kobura: 1,900
   - Wakula: 1,200
4. Nets the campaign will hand out by sub-county:
   - Ruvari Town: 91,751
   - Mwiri: 82,268
   - Kendagi: 70,802
   - Oyamo: 88,345
   - Ndira: 64,708
   - Kobura: 86,129
   - Wakula: 71,965
5. Confirmed Ombeni fever cases reported by each sub-county's facilities, January to September 2026:
   - Ruvari Town: 3,746
   - Mwiri: 4,447
   - Kendagi: 4,866
   - Oyamo: 7,913
   - Ndira: 5,465
   - Kobura: 7,319
   - Wakula: 5,575

### cases_averted_by_subcounty.png

1. One bar per sub-county, labelled with its cases averted to the nearest hundred, the county figure in the title.
