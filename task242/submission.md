# task242 submission

## Tags

**Domain:** Epidemiology & Public Health (disease surveillance: a city's post-season dengue IgM household serosurvey and the quality flags on the infection shares published from it).
**Analytical objective:** Data Quality Monitoring & Alerting (which zones' published dengue infection shares carry the misclassification flag, with each zone's November larval index and the survey's household response rate beside them).

## 1. Final Recommendation

**Six of the 12 zones' published 2027 dengue infection shares carry the misclassification flag (M): IV Melmangalam, V Vadakkupatti, VII Velliyanur, VIII Chinnakulam, IX Periyamalai and XI Sengalur. Their published IgM shares stand for well under two thirds of the residents infected since 1 January; the other six zones' values go to the committee without the flag.**

The register says each zone's value, the share of tested residents with a reactive IgM, stands for the share of residents infected with dengue between 1 January 2027 and the collection of their specimen, and SOP-EPI-07 puts the M flag on when that share, estimated with allowance for the test's misclassification as the laboratory measured it, is more than one and a half times the published value or less than two thirds of it. The laboratory's verification panel shows the IgM assay finding 85 to 94 per cent of infections between one and four weeks after onset, 46 per cent at about 75 days and almost none after four months. A zone's residents were therefore read through a sensitivity set by when its own epidemic ran against its fieldwork: the panel's curve by days since onset, averaged over the zone's cases by onset date from 1 January up to each specimen's collection. In the flagged zones 46 to 100 per cent of the year's cases up to each resident's collection had begun more than 60 days before it (in Vadakkupatti and Sengalur an August wave nearly as large as their November one), against at most 41 per cent in the others, and the share infected is 1.85 to 3.28 times the published value; in the others it is at most 1.29 times (Puthanpalli). Correcting every zone with one sensitivity from the panel, pooled over all its sera (0.677), from the fifth day of illness (0.708) or over the kit's 5 to 60 day window (0.868), puts every zone between 0.82 and 1.37 times its published value and flags none. Reading each zone at the sensitivity of its median day since onset flags four and misses Sengalur and Vadakkupatti, whose November waves were days old at fieldwork while their August waves were long past; at its peak day it flags five, Puthanpalli among them; at its mean day seven, Kottaivayal among them, whose January wave drags the mean back; a fixed 90-day window flags three; the city's pooled epidemic curve flags nine.

## 2. Critical Components

1. IV Melmangalam: published **5.7** per cent; estimated share infected since 1 January **17.0** per cent, **3.00** times the published value.
2. V Vadakkupatti: published **9.3** per cent; estimated share infected since 1 January **18.7** per cent, **2.02** times the published value.
3. VII Velliyanur: published **4.4** per cent; estimated share infected since 1 January **11.9** per cent, **2.71** times the published value.
4. VIII Chinnakulam: published **4.7** per cent; estimated share infected since 1 January **15.5** per cent, **3.28** times the published value.
5. IX Periyamalai: published **6.7** per cent; estimated share infected since 1 January **20.1** per cent, **3.00** times the published value.
6. XI Sengalur: published **7.4** per cent; estimated share infected since 1 January **13.8** per cent, **1.85** times the published value.
7. The largest multiple among the other six zones is **1.29** (III Puthanpalli: published 12.3, estimated 15.9 per cent).

Estimated shares are accepted within 15 per cent of these values: smoothing the panel's curve another reasonable way (steps, fixed bins, a fitted rise and fade, a kernel), counting confirmed cases only, dropping repeat notifications, or reading each zone at its middle fieldwork day moves no estimate by more than that, and every such reading flags the same six zones.

## 3. Step-by-Step Solution

1. Published values: residents tested and IgM reactive by zone in serosurvey_2027_igm_results.csv (4,952 residents tested, 440 reactive), which reproduce Table 1 of dengue_bulletin_dec2027.pdf; the quantity each stands for is SERO-D1's in epi_cell_indicator_register.xlsx and the flag rule is SOP-EPI-07's M flag (sop_epi_07_quality_flags.pdf).
2. The assay's sensitivity: 557 confirmed-case sera from 216 patients in ngmc_igm_lot_verification_panel.csv, days since onset taken as collected_on less onset_date, the final result (the repeat reading for a grey-zone first reading). By scheduled visit: day 3 (2 to 4, 30 sera) 0.133; day 7 (6 to 8, 80 sera) 0.850; day 14 (13 to 15, 90 sera) 0.944; day 21 (20 to 22, 75 sera) 0.920; day 30 (28 to 32, 62 sera) 0.919; day 45 (43 to 47, 48 sera) 0.812; day 60 (58 to 62, 46 sera) 0.587; day 75 (73 to 77, 46 sera) 0.457; day 90 (87 to 93, 40 sera) 0.150; day 120 (117 to 123, 24 sera) 0.042; day 150 (147 to 152, 16 sera) 0.000. Specificity: 4 of the 300 control sera reactive, 0.9867.
3. The curve: the visits' sensitivities joined by straight lines at each visit's mean day since onset, zero at onset.
4. Each zone's 2027 epidemic: 44,196 rows in ncmc_dengue_line_list_2026_27.csv; zone spellings mapped to the 12 zones, the 1,476 notifications of non-residents left out, and resident cases with onset before 1 January 2027 (7,554) left out: 35,166 cases by onset date.
5. Effective sensitivity: for each tested resident, the curve at each day since onset averaged over the zone's cases with onset from 1 January up to the day before the specimen's collection, weighted by cases; each zone's mean over its tested residents: Kadalur 0.760; Thenkarai 0.783; Puthanpalli 0.703; Melmangalam 0.268; Vadakkupatti 0.438; Kizhakkoor 0.808; Velliyanur 0.271; Chinnakulam 0.232; Periyamalai 0.280; Kottaivayal 0.594; Sengalur 0.457; Aranmanai 0.764.
6. Estimated share infected since 1 January: (p + Sp - 1) / (Se + Sp - 1), with p the published share, Se the zone's effective sensitivity and Sp 0.9867; its multiple of the published value; the M flag where the multiple is more than 1.5 or less than two thirds: six zones.
7. Breteau index, November 2027 round: 15,544 forms in dbc_house_inspections_nov2027.csv, 123 of them exact repeats of another row and dropped. Forms dated before 16 November 2027 carry the earlier ward number (the ward master's former_ward_nos); the zone is read from the premise's assessment number (its first two digits), which agrees with the ward map in force on each form's date. A LOCKED call is not an inspection (813), and each house counts once, at its first inspection in the month (later forms for the same house are follow-ups after source reduction): 13,250 houses. Positive containers per 100 houses, by zone.
8. Household response rate: the 2,178 sampled households in serosurvey_2027_household_sample.csv; each household's last call in serosurvey_2027_visits_kobo_export.csv (57 submissions sent twice counted once); 83 found vacant and 58 not a dwelling are left out, and 25 never called on stay in (2,037 households). A household responded when at least one member's specimen reached the laboratory (ngmc_serology_specimen_register_survey.csv), whether tested or rejected: 1,564 households. By zone.

## 4. Deliverable Answers

### dengue_igm_flag_review_2027.xlsx

1. Each zone: published share (per cent); estimated share infected since 1 January (per cent, accepted within 15 per cent of the value); flag:
   - I Kadalur: 14.2; 17.2; no flag
   - II Thenkarai: 12.7; 14.7; no flag
   - III Puthanpalli: 12.3; 15.9; no flag
   - IV Melmangalam: 5.7; 17.0; M
   - V Vadakkupatti: 9.3; 18.7; M
   - VI Kizhakkoor: 10.2; 11.1; no flag
   - VII Velliyanur: 4.4; 11.9; M
   - VIII Chinnakulam: 4.7; 15.5; M
   - IX Periyamalai: 6.7; 20.1; M
   - X Kottaivayal: 5.1; 6.5; no flag
   - XI Sengalur: 7.4; 13.8; M
   - XII Aranmanai: 13.2; 15.8; no flag
2. Breteau index for the November 2027 round, by zone: Kadalur 18.9; Thenkarai 18.5; Puthanpalli 22.4; Melmangalam 21.2; Vadakkupatti 17.6; Kizhakkoor 10.6; Velliyanur 24.2; Chinnakulam 24.8; Periyamalai 17.0; Kottaivayal 14.9; Sengalur 23.8; Aranmanai 16.7.
3. Household response rate, by zone (per cent): Kadalur 75.7; Thenkarai 77.6; Puthanpalli 77.2; Melmangalam 76.9; Vadakkupatti 74.3; Kizhakkoor 74.7; Velliyanur 79.0; Chinnakulam 80.4; Periyamalai 73.8; Kottaivayal 75.3; Sengalur 78.9; Aranmanai 77.5.

### dengue_igm_flags_health_committee.pptx

4. One slide: each zone's published and estimated shares side by side, each zone's flag limits (two thirds and one and a half times the published value) marked, and the six flagged zones (Melmangalam, Vadakkupatti, Velliyanur, Chinnakulam, Periyamalai and Sengalur) marked M.
