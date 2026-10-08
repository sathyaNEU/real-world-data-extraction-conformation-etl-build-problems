# Exemplars: Policy & Education

> 8 accepted tasks in this domain, sorted by the current model's measured mean, lowest (hardest) first. Each is the client's own record. Index and the shared architecture: `index.md`.

## Refer npi 1508302506 for the review year 2024 level-mix records review at a settled 100.00 Per cent share

**Medicare Billing Integrity Review**, Batch 14, Healthcare & Life Sciences, model mean **0.18** over 4 runs (0.26, 0.26, 0.22, 0.26).

### What makes it strong (the client's note)

The trap is the provider-and-service file read on its own, as last year's paper did: it shows 111 eligible providers at 100.0 per cent, and the tie rule would refer NPI 1669718201 (Nurse Practitioner) at 631 of 631.
Standard 2.4 takes the share at the lowest value consistent with all files of record. The provider summary file shows 920 services for NPI 1669718201 against 873 in the provider-and-service file, so its lowest consistent share is 631 of 678 (93.07 per cent).
The computation chain: screen HCPCS 99211 to 99215 at both places of service, keep providers with at least 100 established office visits (6,390), reconcile each provider's summary total to its service-file rows, count the unexplained services as established visits below level five, then rank.
Determinism pins: NPI 1508302506 is the only one of the 111 whose summary total equals its service-file rows (298 of 298, 100.00 per cent); runner-up NPI 1790357432 at 99.60 per cent (250 of 251); tenth share 97.42 per cent; 46 providers above ninety per cent and 104 above eighty (144 and 223 at face value).

### Stakeholder ask (the prompt, verbatim)

I run the review office for the Front Range Medicare Integrity Compact and the Review Panel meets Thursday to make the review year 2024 referral under Schedule 2 of our Level-Mix Review Standard. One provider gets referred for a records review, the member plans get the name the same day, and the Panel does not reconvene. Files attached: the Standard, last year's determination and the chart that went with it, and the CMS Medicare Physician & Other Practitioners public use files for Colorado for 2022, 2023 and 2024 (provider-and-service, provider summary, state service summary), plus the office-visit code list.

Three things from you.

First, the referral paper as a DOCX. Lead with the provider you refer, the level-five share the referral rests on, and the counts behind it, written as prose the way you'd put it to the Panel, not a filled-in template. Carry in it the runner-up and its share; the ten eligible providers with the highest shares, each with NPI, provider type, share and the two counts; how many eligible providers sit above ninety per cent and how many above eighty; and the records review Schedule 3 sets.

Second, a CSV with one row per provider for those ten, giving NPI, provider type, level-five visits, established office visits and share, ranked.

Third, one chart as a PNG the Panel can read at a glance: the ten providers as horizontal bars of level-five share, the referred provider marked, with the ninety and eighty per cent lines drawn.

One provider, one share. Don't hand me a shortlist or an "if". They'll send it back and there's no time for that.

Deliverables: RY2024_referral_determination.docx, RY2024_top_ten.csv, level_five_share_2024.png.

### Deliverables

`RY2024_referral_determination.docx`, `RY2024_top_ten.csv`, `level_five_share_2024.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A regional Medicare integrity compact's Review Panel must refer exactly one Colorado provider for a records review under Schedule 2 of its Level-Mix Review Standard, based on each eligible provider's level-five share of established office visits in review year 2024. The analyst works from the Standard, last year's referral determination and chart, the office-visit code list, and the CMS Medicare Physician & Other Practitioners public use files for Colorado for 2022 to 2024 (provider-and-service, provider summary and state service summary). The analyst must apply the Standard's share definition, name the referred provider and its share, the runner-up, the ten highest shares with counts, and the number of eligible providers above ninety and eighty per cent. Deliverables are `RY2024_referral_determination.docx` (a prose referral paper that leads with the provider, share and counts and states the Schedule 3 records review), `RY2024_top_ten.csv` (ten ranked rows with NPI, provider type, both counts and share) and `level_five_share_2024.png` (horizontal bars for the ten providers with the referred provider marked and ninety and eighty per cent lines).)

`13 files, 39.0 MB`, `EM_office_visit_codes.xlsx`, `Level_Mix_Review_Standard.docx`, `MUP_PHY_R25_P05_V10_D22_Geo_Svc_CO.csv`, `MUP_PHY_R25_P05_V10_D22_Prov_CO.csv`, `MUP_PHY_R25_P05_V10_D22_Prov_Svc_CO.csv`, `MUP_PHY_R25_P05_V10_D23_Geo_Svc_CO.csv`, `MUP_PHY_R25_P05_V10_D23_Prov_CO.csv`, `MUP_PHY_R25_P05_V10_D23_Prov_Svc_CO.csv`, `MUP_PHY_R25_P05_V10_D24_Geo_Svc_CO.csv`, `MUP_PHY_R25_P05_V10_D24_Prov_CO.csv`, `MUP_PHY_R25_P05_V10_D24_Prov_Svc_CO.csv`, `RY2023_Referral_Determination.docx`, `RY2023_top_ten_chart.png`

### Final recommendation

Refer NPI 1508302506 (Physician Assistant) for the review year 2024 records review under Schedule 3 at a level-five share of 100.00 per cent (298 of 298 established office visits), the only eligible provider whose share the files of record settle at 100 per cent; the runner-up is NPI 1790357432 at 99.60 per cent.

### Step-by-step solution

1. Screen the 2024 Colorado provider-and-service file for HCPCS 99211 to 99215 at both places of service, sum services per rendering NPI, and keep the 6,390 providers with at least 100 established office visits.
2. Compute face-value shares (99215 over the family): 111 providers show 100.0 per cent, the largest NPI 1669718201 at 631 of 631.
3. Apply Standard 2.4: compare each provider's total services in the provider summary file with the sum of its provider-and-service rows. The summary exceeds the service file for nearly every provider (by 47 services for NPI 1669718201), and the state service summary confirms services not carried for every office-visit code.
4. Count services outside the service file as established office visits below level five (capped where relevant by the statewide residual in the 99211 to 99214 cells the provider does not show) and recompute every share. NPI 1669718201 falls to 631 of 678, 93.07 per cent.
5. Identify NPI 1508302506 (Physician Assistant) as the one face-value 100 per cent provider with no services outside the service file: 298 of 298, 100.00 per cent.
6. Rank the rest: runner-up NPI 1790357432 at 99.60 per cent (250 of 251), then 99.45, 99.42, 98.86, 98.75, 98.37, 98.21, 97.54 and 97.42 per cent. Count 46 eligible providers above ninety per cent and 104 above eighty.
7. State Schedule 3: full 2024 established office visit records requested, a sixty-visit certified-coder sample, findings to member plans within ninety days.
8. Write the referral paper, the ten-row CSV and the horizontal bar chart with NPI 1508302506 marked and lines at ninety and eighty per cent.

### Key traps (what the model did)

- Computed level-five share from the provider-and-service file alone, found 111 providers tied at 100%, and resolved the tie with the volume tie-break. Never reconciled each provider's summary-file service total to its detail rows, so services missing from the detail file never got counted as below-level-five visits.
- Explicitly considered the conservative lowest-value rule and dismissed it as not applicable, so the whole top-ten table became a face-value tie list.

### Justification

The Standard defines the share by what the files of record support and, where they do not settle a figure, by the lowest consistent value. The provider-and-service file omits services that the provider summary file records, so a face-value 100 per cent is unproven for every provider except the one whose two totals agree. NPI 1508302506 is that provider, settled at 298 of 298, and no other eligible provider reaches 100 per cent on the lowest consistent basis. Referring the largest face-value provider by the tie rule would repeat last year's method, which the Standard's share definition does not support.

## Award the fy2024 district cost pressure reserve to virginia on the certified budget pressure forecast

**School District Finance Forecasting**, Batch 14, Policy & Education Analysis, model mean **0.2** over 3 runs (0.30, 0.28, 0.21).

### What makes it strong (the client's note)

The trap is the working persistence note: carrying realized 2022-23 growth forward puts Delaware first (enrollment-weighted P80 13.117081), but the standard states that the certified forecast controls when the two disagree, and on the certified forecast Delaware ranks seventh at 8.373373.
The computation chain: five predictors (log enrollment, per-pupil current spending, instruction share, federal share, balance per pupil), training-median fill, robust scaling, peers restricted to the same training-enrollment quartile, Euclidean distance with the own state excluded, five nearest peers weighted by inverse distance, a leave-state-out quartile-median residual calibration, and an enrollment-weighted 80th percentile per state.
Determinism pins: that treatment reproduces all eight signed 2023 values (for example AK 22.918049, FL 14.492788, WY 13.349490), and rival treatments reproduce none; FY2024 BPF VA 10.867418, IA 10.665377, WI 10.569376, MN 10.348927, MD 10.107994, GA 9.863109, DE 8.373373, KY 7.471745; gap 0.202041.
The binding constraint is the standard's production continuity clause: a treatment that does not reproduce every signed 2023 reference-state BPF at six decimals is not the Council forecast, and the recovered treatment must be applied unchanged at the FY2023 origin.

### Stakeholder ask (the prompt, verbatim)

Budget hearing is Monday and I need one clean call on the FY2024 District Cost Pressure Reserve. Use the district transition and forecast-origin ledgers with the signed 2023 certification to recover the production Budget Pressure Forecast, then carry that treatment forward at the FY2023 origin for the eight states on the candidate slate. The working persistence note is already circulating, so tell me whether it actually controls the decision.

I need the selected state, its certified BPF, the runner-up and the gap. Give me the full eight-state ranking with each state's median district forecast, enrollment share in districts forecast at or above 10% growth, number of districts at or above 10%, districts scored, and enrollment scored. For the winning state, call out the three districts with the highest predicted growth so I can answer the obvious follow-up in the room.

Leave me reserve_recommendation_memo.docx, state_pressure_forecast.csv, and forecast_pressure_ranking.png. Use six decimals for forecast percentages and gaps, whole numbers for district counts and enrollment, and the exact state codes from the slate. Keep the memo decision-focused rather than turning it into a forecasting tutorial.

### Deliverables

`reserve_recommendation_memo.docx`, `state_pressure_forecast.csv`, `forecast_pressure_ranking.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (An education planning council must make one call on the FY2024 District Cost Pressure Reserve before a Monday budget hearing, choosing among eight candidate states. The analyst works from district transition and forecast-origin ledgers built from the US Census Bureau Annual Survey of School System Finances, the Council's forecast standard, the signed 2023 certification of eight reference-state Budget Pressure Forecasts (BPF), the candidate slate, Census source documentation and errata, and a working persistence note that is already circulating. The production BPF method is not documented, so the analyst must recover it by reproducing every signed 2023 value to six decimals, carry it forward unchanged at the FY2023 origin, and say whether the persistence note controls. The answer needs the selected state, its BPF, the runner-up and the gap, the full eight-state ranking with each state's median district forecast, enrollment share and count of districts forecast at or above 10 percent growth, districts scored and enrollment scored, and the winning state's top three districts. Deliverables are `reserve_recommendation_memo.docx` (decision-focused), `state_pressure_forecast.csv` (eight state rows) and `forecast_pressure_ranking.png` (the ranked BPF chart).)

`16 files, 12.2 MB`, `certified_forecast_record_2023.csv`, `district_transition_2021_2022.csv`, `district_transition_2022_2023.csv`, `errata_report21.xls`, `errata_report22.xlsx`, `errata_report23.xlsx`, `f33_form_2024.pdf`, `file_manifest.csv`, `forecast_ledger_dictionary.csv`, `forecast_origin_2022.csv`, `forecast_origin_2023.csv`, `northstead_forecast_standard.docx`, `reserve_candidate_slate_2024.csv`, `school23doc.docx`, `source_register.csv`, `working_persistence_note.docx`

### Final recommendation

Award the FY2024 District Cost Pressure Reserve slot to VA (Virginia), with a certified Budget Pressure Forecast of 10.867418; IA (Iowa) is runner-up at 10.665377, a gap of 0.202041 percentage points.

### Step-by-step solution

1. Use FY2022 as the origin with the 2021 to 2022 transition as training to reproduce the signed FY2023 certification, then FY2023 as the origin with the 2022 to 2023 transition as training for FY2024.
2. Recover the treatment by requiring all eight signed FY2023 BPF values to reproduce at six decimals: predictors log_enrollment, pp_current, instruction_share, federal_share and balance_pp, with missing values filled by the training median and robust scaling on training median and interquartile range.
3. Restrict each query district's peers to its training-enrollment quartile, exclude its own state, take the five nearest by Euclidean distance, and forecast growth as their inverse-distance-weighted mean.
4. Add the leave-state-out median residual for the district's enrollment quartile, then aggregate to each state's enrollment-weighted 80th percentile.
5. Apply the treatment unchanged at the FY2023 origin: VA 10.867418, IA 10.665377, WI 10.569376, MN 10.348927, MD 10.107994, GA 9.863109, DE 8.373373, KY 7.471745.
6. Rank on unrounded values: Virginia first, Iowa second, gap 0.202041.
7. Report the state measures. Virginia: median district forecast 8.200766 (enrollment-weighted), 36.648628 percent of enrollment in districts forecast at or above 10 percent, 17 such districts, 131 districts and 1,260,290 enrollment scored.
8. Name Virginia's top three districts: Buchanan County 17.412013 percent, Highland County 14.743185 percent, Lee County 12.209249 percent.
9. Test the persistence note: its carry-forward screen selects Delaware, does not reproduce the certified treatment, and does not control, because the certified forecast governs.
10. Write the memo, the eight-row CSV and the ranked chart with six-decimal labels.

### Key traps (what the model did)

- Built a peer-analog forecast whose treatment did not reproduce the eight signed 2023 BPF values, then ranked the slate on it anyway. The three runs each landed on a different winner (WI, GA, DE). The memo correctly said the persistence note does not control, but the 'certified' forecast it substituted was not the production treatment.
- One run also took the persistence-note leader (Delaware, 13.117081) as the certified winner.

### Justification

The Council standard defines its forecast by continuity with the signed 2023 certification, and only one peer-analog treatment reproduces all eight signed values exactly. Carried forward unchanged, it ranks Virginia first by 0.202041 points over Iowa. The persistence note answers a different question with realized growth and points to Delaware, but the standard says the certified forecast controls when the two disagree, so the reserve goes to Virginia.

## Award the 2026 grant to hermann area district hospital, not stroud regional medical center

**Hospital Uncompensated Care Policy**, Batch 14, Policy & Education Analysis, model mean **0.26** over 4 runs (0.29, 0.27, 0.37, 0.29).

### What makes it strong (the client's note)

The trap is the staff first look: it treats fiscal year files as reporting periods, counts a 334-day and a 396-day report, and compares against a statewide class average, which pushes Stroud's own change to +1.71 and its score to +2.87; under the standard Stroud's own change is -0.83 and it ranks third among members at +0.39.
The computation chain runs from raw HCRIS cells (S-10 line 30 and line 6, G-3 line 4, C Part I line 202 column 8) through period screens (360 to 371 days, all four cells present, latest processed report per period end), per-state windows, per-hospital pool eligibility read at each pool hospital's own span end, SD-scaled three-measure profiles, and a greedy reference group build run over all 201 designees jointly in descending base burden with a two-use cap.
Determinism pins: Hermann residual burden +0.80 (own change -1.80, reference change -2.60, group of 4), Missouri Delta +0.56, gap 0.23, overtaking threshold -2.36, pools of 1,258 and 1,202, and 201 designees (103 OK, 98 MO).
The binding constraint is section 11: only a construction that reproduces Franklin Medical Center 3.48 and Acadia-St. Landry 0.66 (88 designees) and Inova Alexandria 0.59 and Inova Fair Oaks 0.10 (75 designees) counts. Running the states separately, dropping the SD scaling, or admitting only never-expanded states each moves the award to a different hospital.

### Stakeholder ask (the prompt, verbatim)

The board adopts the 2026 award in November, and I'd like the determination done outside the office this time.

Owen on my staff sent round a first look last week, staff_note_2026_first_look.docx. It ranks our twelve member hospitals in the Oklahoma and Missouri cycle and puts Stroud Regional Medical Center on top. To be fair to him, he says it's a quick pass. I don't think it follows the standard though, and the board reads these notes, so if I'm the one who's wrong I'd like to know before November.

Work to award_determination_standard.docx as written. People tend to skip section 11, the part about matching what we've already certified for Louisiana and Virginia. Please don't. README.txt explains the rest of the supplied materials.

I need three files back.

determination_memo_2026.docx, two pages at most because it goes in the board materials. Which member wins, with its CCN, city, class, reference group size, base and post burden, own change, reference change and residual burden. Then the runner-up and its residual burden, the gap, and how far the winner's reference change would have to move for the runner-up to overtake. Just one line on whether your construction gives back both certifications as published. What I most want to read is why Owen's note ends up on Stroud and what changes under the standard.

residual_burden_workbook_2026.xlsx with sheets named Members 2026, Reference groups and Prior cycles. Members 2026 is a row per member in rank order: rank, CCN, hospital, city, state, class, group size, base burden, post burden, own change, reference change, residual burden. Reference groups gets a row per reference hospital, with the member's CCN and name and then the reference hospital's CCN, name, state, class, base burden, post burden and own change. Prior cycles has a row for each earlier cycle giving the cycle, the winner with our certified value and yours, the runner-up the same way, the number of designees, and whether the other members come back in their published order.

residual_burden_chart_2026.png. Horizontal bars of residual burden for the twelve in rank order, winner highlighted, a line at zero, and the determination as the title.

Two decimals on all percentages and points. Hospital names as they appear on the cost report, with the CCN beside them, since there are a few Parklands and a lot of Mercys in these two states.

If you and Owen land on different hospitals, which I expect, tell me which one the board should go with. And if part of the standard won't work on the data as it comes, say so.

Marla Quintrell

### Deliverables

`determination_memo_2026.docx`, `residual_burden_workbook_2026.xlsx`, `residual_burden_chart_2026.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A fictional hospital trust must certify its 2026 Post-Expansion Stabilization Award for the joint Oklahoma and Missouri Medicaid expansion cycle, and a staff first look has already put Stroud Regional Medical Center on top. Working from raw CMS HCRIS cost report files (fiscal years 2013 to 2024, headerless report, numeric and text tables) and the trust's written determination standard, the analyst must screen reports, build each designee's base and post windows around its state's effective date, assemble a matched reference group from same-class hospitals in non-expansion states, and rank all 201 designees on residual burden (own change minus reference change) to read off the twelve members. The construction has to return the trust's two published certifications for Louisiana 2019 and Virginia 2022, as section 11 of the standard requires. The analyst must decide which member wins, explain why the first look lands on Stroud, and say where the standard does not run on the data as written. Deliverables are `determination_memo_2026.docx` (two pages at most), `residual_burden_workbook_2026.xlsx` (sheets Members 2026, Reference groups, Prior cycles), and `residual_burden_chart_2026.png` (horizontal residual burden bars with the winner highlighted).)

`52 files, 102.2 MB`, `README.txt`, `HCRIS_DataDictionary.csv`, `HCRIS_Data_model.pdf`, `HCRIS_FACILITY_NUMBERING.csv`, `HCRIS_STATE_CODES.csv`, `HCRIS_TABLE_DESCRIPTIONS_AND_SQL.txt`, `HOSP2010_README.txt`, `HOSP2010_Worksheet_Codes.pdf`, `prm15-2_ch40_s4012_worksheet_S-10_excerpt.pdf`, `award_determination_standard.docx`, `certification_louisiana_2019.pdf`, `certification_virginia_2022.pdf`, `medicaid_expansion_effective_dates.xlsx`, `member_roster_2026.xlsx`, `staff_note_2026_first_look.docx`, `HOSP10_2013_ALPHA.CSV`, `HOSP10_2013_NMRC.CSV`, `HOSP10_2013_RPT.CSV`, `HOSP10_2014_ALPHA.CSV`, `HOSP10_2014_NMRC.CSV`, `HOSP10_2014_RPT.CSV`, `HOSP10_2015_ALPHA.CSV`, `HOSP10_2015_NMRC.CSV`, `HOSP10_2015_RPT.CSV`, `HOSP10_2016_ALPHA.CSV`, `HOSP10_2016_NMRC.CSV`, `HOSP10_2016_RPT.CSV`, `HOSP10_2017_ALPHA.CSV`, `HOSP10_2017_NMRC.CSV`, `HOSP10_2017_RPT.CSV`, `HOSP10_2018_ALPHA.CSV`, `HOSP10_2018_NMRC.CSV`, `HOSP10_2018_RPT.CSV`, `HOSP10_2019_ALPHA.CSV`, `HOSP10_2019_NMRC.CSV`, `HOSP10_2019_RPT.CSV`, `HOSP10_2020_ALPHA.CSV`, `HOSP10_2020_NMRC.CSV`, `HOSP10_2020_RPT.CSV`, `HOSP10_2021_ALPHA.CSV`, `HOSP10_2021_NMRC.CSV`, `HOSP10_2021_RPT.CSV`, `HOSP10_2022_ALPHA.CSV`, `HOSP10_2022_NMRC.CSV`, `HOSP10_2022_RPT.CSV`, `HOSP10_2023_ALPHA.CSV`, `HOSP10_2023_NMRC.CSV`, `HOSP10_2023_RPT.CSV`, `HOSP10_2024_ALPHA.CSV`, `HOSP10_2024_NMRC.CSV`, `HOSP10_2024_RPT.CSV`, `source_register.csv`

### Final recommendation

Hermann Area District Hospital (CCN 261314, Hermann, MO, critical access) takes the 2026 award at a residual burden of +0.80 points, with Missouri Delta Medical Center (CCN 260113) runner-up at +0.56; the board should adopt this rather than the first look's Stroud Regional Medical Center, which ranks third under the standard.

### Step-by-step solution

1. Read the three headerless tables in every fiscal year file using the CMS data dictionary column order, join numeric and text cells to the report record, and attach provider number, period dates, and processed date.
2. Classify providers by the last four CCN digits: 0001 to 0879 general acute, 1300 to 1399 critical access; drop all others.
3. Screen reports: 360 to 371 days, all four cells present (S-10 line 30, G-3 line 4, S-10 line 6, C Part I line 202 column 8), neither denominator at zero or below, and the latest processed report per hospital and period end. From FY2023 read S-10 Part I (entire complex), not Part II.
4. Build base windows (three latest counting periods ending on or before the effective date: 2021-07-01 OK, 2021-10-01 MO) and post windows (first two beginning on or after it), setting aside straddling periods. This yields 201 designees (103 OK, 98 MO), and 88 and 75 in the prior cycles.
5. Build each designee's pool: same class, state outside the cycle, and no expansion in effect on or before the last day of that pool hospital's own span. Pools are 1,258 for Oklahoma and 1,202 for Missouri designees.
6. Compute the base window profile (burden, Medicaid share, mean log operating expenses) and divide each measure by its sample SD over the designee's pool.
7. Process all 201 designees together in descending base burden. Grow each group one hospital at a time toward the designee's profile, stop when no addition brings the group average closer (never below three), cap each pool hospital at two uses across the cycle, and break ties on lowest CCN.
8. Compute residual burden as own change minus the group's mean own change, rank all designees, and read off the members: Hermann +0.80, Missouri Delta +0.56, gap 0.23.
9. Run the same construction on Louisiana 2019 and Virginia 2022: Franklin 3.48, Acadia-St. Landry 0.66, Inova Alexandria 0.59, Inova Fair Oaks 0.10, with listed members back in their published places.
10. Rebuild the first look on its own basis to isolate the difference: Stroud +2.87 there versus +0.39 under the standard, driven by its own change.
11. Find the overtaking threshold: the runner-up passes Hermann if Hermann's reference change rises to -2.36 from -2.60.
12. Write the memo, the three-sheet workbook, and the chart.

### Key traps (what the model did)

- Correctly rejected the staff note's Stroud pick, but built its own reference-group construction that failed the section-11 controls (LA 3.23/0.85 vs certified 3.48/0.66; VA 0.24 vs 0.59), openly said it did not reproduce the certifications, and still named a winner off it (Southwestern, groups of 3 instead of 4).

### Justification

The standard scores each member against a reference group matched on base burden, Medicaid share, and size, using full-year reports aligned to its own state's effective date, and section 11 accepts only a construction that reproduces the two certified cycles. The construction above does so exactly, and on it Hermann's burden fell 1.80 points while its matched group fell 2.60, leaving the largest residual among members. Stroud tops the first look only because that note counted partial-year reports in file years, which inflated its post burden, and compared it with a flat statewide class average. Once its windows are built from full years around 2021-07-01, its own change turns negative and its residual drops to +0.39. The margin over Missouri Delta is thin (0.23 points), so the memo should state the -2.36 threshold, but the result follows the standard as written and matches the certified record.

## Award the 2024 district continuity reserve to barbers hill isd on the continuity forecast

**District Spending Continuity Forecasting**, Batch 14, Policy & Education Analysis, model mean **0.3** over 3 runs (0.34, 0.32, 0.34).

### What makes it strong (the client's note)

The trap is the planning snapshot: North Posey leads observed FY2022 to FY2023 growth at 12.879137 percent, while Barbers Hill sits at 7.540220 percent; the standard awards on the continuity forecast, under which Barbers Hill leads.
The computation chain: gate donors by exact match on metro class and funding mix, rank ten profile fields as within-pool percentiles, take the 43 nearest seeds by L1 distance, apply the coherence control (average-linkage Euclidean clustering on six coherence fields cut to three clusters, keeping the cluster nearest the target), cap at four peers per state in seed order, and forecast as the inverse-distance-weighted mean of peers' prior-cycle growth with weights 1 / (distance + 0.01).
Determinism pins: that treatment reproduces all five certified references on peer count and forecast (Canton Central 11 and 6.166521 percent, Monroe Co 10 and 3.784403, Huber Heights 19 and 6.816939, Robinson CUSD 2 24 and 5.536525, Albertville City 23 and 10.326033); Barbers Hill 12.809757 percent from 13 peers, North Posey 12.300864 percent from 5, gap 0.508893; Barbers Hill FY2024 PPCSTOT 16137.44.
The binding constraint is the standard's continuity requirement: only a treatment that returns every certified reference exactly is the production forecast, and the margin between the top two is about half a point.

### Stakeholder ask (the prompt, verbatim)

Finance call is tomorrow morning and I told them the 2024 District Continuity Reserve pick would be locked before then, so I need this closed today. You'll see the observed growth snapshot in the supplied files, people keep quoting it, but it's a planning read and it doesn't decide the award. The standard does, along with last year's certified FY2023 record, and the eight districts in candidate_register.csv are the only ones on the table.

Short Word brief for the call, one page if you can manage it. Name the district, give me its forecast growth and the runner-up's and how far apart they are, and a couple of sentences on why the snapshot isn't the answer because that question is coming. The workbook is where the detail lives. Rank all eight with observed FY2022-FY2023 growth, how many approved peers each one ended up with, final forecast growth, forecast minus observed in points, and the FY2024 PPCSTOT that implies. A plain ranked bar chart of forecast growth is fine. Then a winner audit tab with the peers that are actually carrying the winning number, each with its prior cycle growth, distance to the target and weight share, and a continuity tab where I can see your figures next to the five certified references, because if those don't line up nothing else in the file matters.

Six decimals on percentages and point differences, two on PPCSTOT, work the differences off unrounded numbers. Call the files reserve_forecast_brief.docx and reserve_forecast_workbook.xlsx.

### Deliverables

`reserve_forecast_brief.docx`, `reserve_forecast_workbook.xlsx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A finance lead must lock the 2024 District Continuity Reserve pick before a finance call, choosing among the eight districts in the candidate register. The award follows the forecast record standard and the certified FY2023 forecast record, not the observed growth planning snapshot that people keep quoting. The analyst works from the district fiscal ledger (FY2021 to FY2023 profiles built from the US Census Bureau Annual Survey of School System Finances), the raw Census tables and documentation, the field guide, the standard and the certified record, and must recover the production peer-analog treatment by reproducing the five certified references before forecasting FY2023 to FY2024 per-pupil current spending (PPCSTOT) growth for the slate. Deliverables are `reserve_forecast_brief.docx` (about one page: the district, its forecast and the runner-up's, the gap, and why the snapshot is not the answer) and `reserve_forecast_workbook.xlsx` (a ranking of all eight with observed growth, approved peer count, forecast growth, forecast minus observed and implied FY2024 PPCSTOT, a ranked bar chart, a winner audit tab and a continuity tab against the certified references).)

`12 files, 18.4 MB`, `candidate_register.csv`, `certified_2023_forecast_record.csv`, `district_fiscal_ledger.csv`, `elsec21t.txt`, `elsec22t.txt`, `elsec23t.txt`, `f33_form_2024.pdf`, `field_guide.txt`, `forecast_record_standard.docx`, `planning_snapshot.docx`, `school23doc.docx`, `source_register.csv`

### Final recommendation

Award the 2024 District Continuity Reserve to Barbers Hill ISD 902 (NCESID 4809450), with forecast FY2023 to FY2024 PPCSTOT growth of 12.809757% from 13 approved peers (FY2024 PPCSTOT 16137.44); North Posey County Schools (1807950) is runner-up at 12.300864%, a gap of 0.508893 percentage points.

### Step-by-step solution

1. Use the district fiscal ledger as shipped (15,933 district-year rows). For a forecast at origin year t, each target's profile is its year t record and donors are districts with a year t-1 profile and realized growth from t-1 to t, excluding the target.
2. Recover the production treatment by testing seed depth, coherence fields, clustering conventions, cluster count, target inclusion, operation order and geographic caps against the five certified FY2023 references until all ten checkpoints reproduce exactly.
3. Gate donors on metro_class and funding_mix, rank the ten continuous fields as right-inclusive percentiles within the pool, and take the 43 nearest seeds by L1 distance, ties by ascending NCESID.
4. Cluster the seeds on fed_share, state_share, local_share, debt_pp_log, pp_current_log and log_enroll (average linkage, Euclidean, three clusters), keep the cluster whose centroid is nearest the target, then keep at most four peers per state in seed order.
5. Forecast each district as the weighted mean of its approved peers' prior-cycle growth with weights 1 / (distance + 0.01), and grow FY2023 PPCSTOT by that rate.
6. Carry the treatment forward to the eight slate districts at origin FY2023: Barbers Hill 12.809757 (13 peers), North Posey 12.300864 (5), Lapeer 11.398725 (18), Byers 10.348889 (11), Carrollton 9.321846 (25), Reef Sunset 7.967844 (23), Sisters 6.629507 (23), Piqua 5.053303 (17).
7. Rank on unrounded forecasts: Barbers Hill first by 0.508893 points over North Posey.
8. Reconcile the snapshot: North Posey's observed 12.879137 percent leads the planning read, but its forecast is 0.578273 points below that; Barbers Hill's forecast is 5.269537 points above its observed 7.540220 percent.
9. Audit the winner's 13 peers, from Ladue City (prior-cycle growth 2.832125 percent, distance 0.918033, weight share 0.120414) to Santa Clara (13.258175 percent, distance 1.752402, share 0.063407), with shares summing to 1.
10. Write the one-page brief and the workbook with the ranking, chart, winner audit and continuity tabs.

### Key traps (what the model did)

- Implemented a peer-forecast pipeline that visibly failed the five certified continuity references. The continuity tab even disclosed the mismatches ('only 3 of 5 counts and no rates reproduce'), yet the runs still ranked the slate and awarded on that non-conforming treatment (Lapeer x2, Byers x1).
- All runs correctly rejected the observed-growth planning snapshot, so the intended trap was avoided. The loss came entirely from the forecast-reproduction failure above.

### Justification

The standard defines the award by the production continuity forecast, and only one treatment reproduces every certified FY2023 reference on both peer count and forecast rate. Applied to the slate, it places Barbers Hill first at 12.809757 percent, ahead of North Posey by 0.508893 points. The planning snapshot measures each district's own past spending growth with no peer evidence behind it, so North Posey's observed lead is context rather than the basis for the award.

## Select jurupa unified school district for the cycle 3 fiscal diagnostic review

**School District Finance Review**, Batch 14, Policy & Education Analysis, model mean **0.41** over 1 runs (0.44).

### What makes it strong (the client's note)

The trap is the working sheet: it ranks the 28 on published spending per pupil growth and is led by Compton Unified at 32.8 percent, but under the measure Compton returns 14.25 points and places eighth of 25.
The measure is not documented: it must be rebuilt against Annex 2 until all 16 transmitted entries return (regular systems, at least 10,000 pupils in both years, a same-state peer pool within 1.5 times earlier-year size, widening to the whole state below 10 members, an iterative drop of members more than 8 points above the running median, and a median benchmark).
The data vintage fork: the served Bureau files carry original amounts, so cycle 2 reproduces as served, while the FY2022 and FY2023 errata must be applied for cycle 3.
Determinism pins: Jurupa 20.06 points against a 12.41 percent benchmark over 80 peers; Lansing 19.90 against 11.82 percent over 12 peers; gap 0.16; Corpus Christi third at 19.18; 127 set aside in total; 8 widened pools; 17 above 10.00 points; median 12.21; 3 not assessable in Tennessee and Virginia; 7 systems with an FY2022 errata correction, the largest Jurupa AE1 at 481 thousand dollars.

### Stakeholder ask (the prompt, verbatim)

You are the new analyst on the program team and cycle 3 is yours. The Program Committee meets in October and expects one system named for the diagnostic review, with the figures the Selection Policy calls for. This note tells you where things stand.

The measure we select on is the Structural Spending Variance, and we did not build it. Pellworth Analytics LLC built it for the Fund and ran it for cycle 2, then closed its education practice in June last year. Under the engagement letter the code and the models behind the cycle-2 figures were the firm's work product, and none of it was ever delivered to us. I took that as far as it would go with the firm's administrator and there is nothing left to obtain, so please do not spend the cycle looking for it.

What we do have is in the supplied materials. The policy in its second edition, with Annex 1 and Annex 2. The results Pellworth transmitted on 19 July 2024, in the workbook the firm sent. The Census Bureau survey files those results were computed on, held as a fixed snapshot, together with the FY2023 file, the Bureau's technical documentation, its survey form and its errata reports. The source register lists every file and where it came from.

Paragraph 18 of the policy is the part that governs how you work. The transmitted cycle-2 results, taken with the data they were computed from, are what fixes the measure for the Fund. An implementation that does not return those results on that data is not the Structural Spending Variance, however close it comes and whatever it is called, and no selection may rest on it. The first thing you owe the Committee is therefore an implementation that does return them. Everything you report for cycle 3 follows from that and is worth nothing without it.

Cycle 3 covers FY2022 to FY2023. Annex 1 carries the twenty-eight systems referred this cycle by the regional program officers and by the associate's growth screen. Only those systems are in play, and every one of them has to be accounted for in what you send us, whether or not it can be assessed.

You will also find the associate's working sheet in the supplied materials. It sorts the twenty-eight on published spending per pupil growth and carries some context against each name. It is orientation for the pre-read and nothing beyond that. Do not let its order shape yours.

Three things go to the Committee.

cycle3_selection_memorandum.docx, the selection memorandum.
Open by naming the system you have selected and the system that comes second, giving each one's Variance in points to two decimals and the gap between the two in points to two decimals.
Give the benchmark growth the selected system is set against, in percent to two decimals, and the size of its peer group as a whole number, then give both figures for the second-placed system.
Give the number of systems set aside from each of those two peer groups as unusual movers, as whole numbers, and the total number set aside across the peer groups of every assessed referred system.
Give the number of referred systems whose peer group widened to the whole state, as a whole number, and name them.
Name the system in third place and give its Variance in points to two decimals.
Give the number of assessed referred systems sitting above 10.00 points, as a whole number, and the Variance value in points to two decimals that has as many assessed referred systems above it as below it.
Name the system that leads the associate's working sheet on published spending per pupil growth, give that published growth in percent to one decimal, give the same system's Variance in points to two decimals, and say where it places under the measure.
Give the number of referred systems that are not assessable this cycle, as a whole number, and name the states they sit in.
Give the number of referred systems that carried an FY2022 errata correction to an input of the Variance, as a whole number, and identify the largest such correction by system, by the item corrected and by its size in thousand dollars.
Include a table with one row per referred system, giving its growth, the benchmark growth it is set against, the size of its peer group, the number set aside from that group and its Variance, to two decimals except the two whole-number columns, and show a system that cannot be assessed as such rather than leaving its row empty.
variance_ranking.png, the ranking chart.
One bar per assessed referred system, ordered from the highest Variance to the lowest, with a line drawn at zero.
Show the Variance of the selected system and of the second-placed system against their own bars, in points to two decimals.
Mark the systems whose peer group widened to the whole state so that they read as different from the rest, and put their count in the legend entry that describes them.
Put a note on the chart giving the number of assessed referred systems above 10.00 points, as a whole number.
Give the chart a title that carries the name of the selected system.
cycle3_candidate_assessment.csv, the assessment table.
One row per referred system, carrying its name, its NCES identifier, its state and its status.
For every assessed system give its fall membership in each of the two fiscal years as whole numbers, its relief-excluded current spending per pupil in each of the two fiscal years in whole dollars, its growth and the benchmark growth it is set against in percent to two decimals, the size of its peer group as a whole number and its Variance in points to two decimals, under exactly these column names: name, ncesid, state, status, fall_membership_fy2022, fall_membership_fy2023, structural_pp_fy2022_usd, structural_pp_fy2023_usd, growth_pct, benchmark_growth_pct, peer_pool_size, set_aside_count, pool_widened, ssv_points.
For every assessed system give the number of systems set aside from its peer group as a whole number, and whether its peer group widened to the whole state, as yes or no.
Order the rows by Variance from highest to lowest, with the systems that cannot be assessed placed last.
Report the Variance and every growth figure to two decimals unless a bullet above asks for something else, give per pupil amounts as whole dollars, and check before you send that any figure appearing in more than one of the three files reads the same in each of them.

### Deliverables

`cycle3_selection_memorandum.docx`, `variance_ranking.png`, `cycle3_candidate_assessment.csv` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A grant-making fund's Program Committee must name one school system for its cycle 3 fiscal diagnostic review, chosen on the Structural Spending Variance, a peer-benchmarked measure of growth in relief-excluded current spending per pupil. The consultancy that built the measure has closed and never delivered its code, and the Selection Policy (paragraph 18) says the measure is whatever implementation returns the transmitted cycle 2 results on the data they were computed from. The analyst works from the policy and its annexes, the cycle 2 transmittal workbook, the Census Bureau Annual Survey of School System Finances files for FY2021 to FY2023 with their documentation, survey form and errata reports, an associate's working sheet and a source register. The analyst must rebuild the measure, then score the 28 referred systems for FY2022 to FY2023. Deliverables are `cycle3_selection_memorandum.docx` (the selection, runner-up, gap, benchmarks, peer group sizes, set-aside counts, widened pools, third place, count above 10.00 points, the middle value, the working-sheet leader, the not-assessable systems, the errata count and the largest correction, and a 28-row table), `variance_ranking.png` (a ranked bar chart of the assessed systems) and `cycle3_candidate_assessment.csv` (28 rows under fixed column names).)

`16 files, 43.9 MB`, `cycle2_results_transmittal.xlsx`, `cycle3_longlist_working.xlsx`, `elsec21.txt`, `elsec21t.txt`, `elsec22.xlsx`, `elsec22t.txt`, `elsec23.txt`, `elsec23t.txt`, `errata_report21.xls`, `errata_report22.xlsx`, `errata_report23.xlsx`, `evaluation_partner_transition_memo.docx`, `f33_form_2024.pdf`, `school23doc.docx`, `selection_policy_2nd_edition.pdf`, `source_register.csv`

### Final recommendation

Select Jurupa Unif School Dist (CA, NCES 0619260) for the cycle 3 diagnostic review at a Structural Spending Variance of 20.06 points, 0.16 points ahead of Lansing Public School District (MI) at 19.90.

### Step-by-step solution

1. Read the FY2021, FY2022 and FY2023 Bureau files under their own documentation, using the FY2022 Excel release because the comma-delimited release is incomplete, and join on the NCES identifier.
2. Rebuild the measure against Annex 2 until one definition returns all 16 transmitted entries: relief-excluded current spending per pupil on each year's own membership, regular systems with at least 10,000 pupils in both years, same-state peers within 1.5 times earlier-year size, widening to the whole state when fewer than 10 peers remain before set-aside, iterative removal of peers more than 8 points above the running median, and the median of the survivors as benchmark.
3. Confirm the served files carry original amounts (correcting cycle 2 breaks the reproduction), then apply every FY2022 and FY2023 errata correction before computing cycle 3.
4. Mark Robertson County and Hamilton County (Tennessee) and Roanoke City (Virginia) as not assessable, because their states' reporting does not separate relief spending in both years.
5. Score the 25 assessable referred systems: Jurupa 20.06 (benchmark 12.41 percent, 80 peers, 10 set aside), Lansing 19.90 (11.82 percent, 12 peers, 2 set aside), Corpus Christi 19.18.
6. Report 127 set aside across all assessed peer groups, 8 widened pools (Lansing, Christiana, Brockton, Baltimore City, Idaho Falls, Lynn, Clayton County, Gadsden), 17 systems above 10.00 points and a median of 12.21.
7. Place the working-sheet leader: Compton Unified at 32.8 percent published growth returns 14.25 points, eighth of 25.
8. Count 7 referred systems with an FY2022 errata correction to a Variance input; the largest is Jurupa, item AE1, 481 thousand dollars.
9. Produce the memorandum, the ranking chart and the 28-row CSV from one computation and check that shared figures agree.

### Key traps (what the model did)

- Rebuilt the undocumented Structural Spending Variance with an incomplete peer-pool rule set (widening to whole-state applied to 2 systems instead of 8, too few unusual movers set aside), so the implementation did not return all 16 Annex 2 entries; the winner held but runner-up, values and counts were wrong.

### Justification

Paragraph 18 makes the cycle 2 results the definition of the measure, so the only admissible implementation is the one that returns all 16 Annex 2 entries on the cycle 2 data. On that implementation, with the published errata applied for cycle 3, Jurupa has the highest Variance at 20.06 points. Relaxed variants that hand the lead to Lansing or Corpus Christi each fail Annex 2 and are not the measure, and the working sheet's growth ranking is not what the program selects on.

## Certify the fy2026 adult completion administration charge on the thirty institutions at $1,885,190

**State Higher Education Formula Funding**, Batch 14, Policy & Education Analysis, model mean **0.44** over 4 runs (0.54, 0.54, 0.53, 0.54).

### What makes it strong (the client's note)

The trap is section 9's circularity: the administration charge recovered from a participant counts as part of its allocation for the cycle, so chargeable allocation must be taken on the allocation including the charge. On printed allocations alone nobody reaches the ceiling; solving the charge consistently puts Delgado Community College, the LSU System office and the LCTCS System office at the $3,125,000 ceiling, each carrying $239,592.26.
The learner base must be certified, not reported: keep adults (age codes 8 to 13), count each hosted adult once by removing fall-term cross-enrolled guests at the host, take amended register pairs once, and assign tiers on the certified headcount (32,497 learners priced at $22,345,800 on Schedule A).
The method is validated by replay: the same pipeline on fall 2019 and fall 2021 reproduces the FY2022 and FY2024 statements to the dollar, including the FY2024 floor (four institutions, $47,550) and section 9 charges.
The FY2026 transition floor is 94.6 percent of the FY2024 allocation under sections 4 to 7: ten institutions are floored at a reserve cost of $483,491, taking the thirty to $22,829,291.

### Stakeholder ask (the prompt, verbatim)

Certification goes to the Finance Committee on the fifteenth and the schedule must be finalized using base fall 2023 across our thirty public institutions. Regent Keller wants one number before she votes, the section 9 line for the institutions: the administration charge recovered from the thirty institutions for FY2026, in whole dollars, the total of the schedule's charge column. Lead with that figure and put the work under it.

Some background. I sit in the Office of Finance at the Board of Regents. Schedule A settles every per-learner amount, section 5 the tier ranges, section 7 the transition floor, and the committee fixed the pool and the ceiling in June, so none of that is open. What is open is what each participant ends up certified at once the guidelines have been worked all the way through.

Back the figure with the certification schedule as a CSV, a row per institution, age category and attendance status, carrying the reported undergraduate learners, the certified adult learners, the enrollment tier, the per-learner amount, the Schedule A amount, the transition floor where it applies, the administration charge assigned to the row, and the amount finally certified.

Then a short memo in Word for the committee pack. Lead with the same figure and, beside it, what the four system offices carry between them. Under it a table of every participant, its allocation under sections 4 to 7, its administration charge, and what it is certified at, with a total line for the thirty that ties to the figure. Below that the institutions certified at the transition floor and what the floor cost the reserve. Regent Keller will also ask which participants sit at the chargeable ceiling and which institution is nearest the ceiling without reaching it, and by how much, so put those in.

Last, chart it for her slide, a PNG. One bar per participant in descending order of the amount certified, the administration charge drawn as a hatched segment at the top of each bar, the participants at the ceiling marked, the four system offices in a second colour, and the figure and the thirty institutions' share of the pool in the title.

### Deliverables

`adult_completion_fy2026_certification_schedule.csv`, `adult_completion_fy2026_section9.png`, `adult_completion_memo_fy2026.docx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A state Board of Regents must certify FY2026 adult completion allocations for its thirty public institutions and four system offices, and a Regent wants one number: the section 9 administration charge recovered from the thirty institutions, in whole dollars. The Program Guidelines settle per-learner amounts (Schedule A), tier ranges and a transition floor, and the June minutes fix the transition percentage, the $2,655,000 administration pool and the $3,125,000 chargeable ceiling. The analyst must build the certified adult learner base from the fall 2023 IPEDS age-by-attendance extract and the cross-enrollment register, apply the floor against the FY2024 statement, and recover the pool from all 34 participants in proportion to chargeable allocation. Deliverables are a CSV certification schedule (one row per institution, age category and attendance status with every listed column), a Word memo (the figure and the system offices' total, a 34-participant table with a thirty-institution total line, the floored institutions and reserve cost, the ceiling set and the institution nearest the ceiling), and a PNG chart (descending bars per participant with hatched charge segments, ceiling marks, system offices in a second colour, and the figure and the thirty's pool share in the title).)

`21 files, 14.2 MB`, `adult_completion_allocation_guidelines.docx`, `data_dictionary.json`, `dim_institution.csv`, `dim_value_label.csv`, `dim_variable.csv`, `ef2019b_la_extract.csv`, `ef2021b_la_extract.csv`, `fact_enrollment_age.csv`, `fact_enrollment_residence.csv`, `fy2022_allocation_statement.xlsx`, `fy2024_allocation_statement.xlsx`, `fy2026_certification_working_file.xlsx`, `ipeds_ef_survey_materials_2023_2year.pdf`, `ipeds_ef_survey_materials_2023_4year.pdf`, `management_board_crosswalk.csv`, `overview.xlsx`, `regents_cross_enrollment_circular_2019-04.docx`, `regents_finance_committee_minutes_2025-06.docx`, `statewide_cross_enrollment_register_2019.csv`, `statewide_cross_enrollment_register_2021.csv`, `statewide_cross_enrollment_register_2023.csv`

### Final recommendation

Certify the FY2026 administration charge recovered from the thirty institutions at $1,885,190, with the four system offices carrying $769,810; Delgado Community College, the LSU System office and the LCTCS System office sit at the $3,125,000 chargeable ceiling.

### Step-by-step solution

1. Read the Program Guidelines, Circular 2019-04, the June 2025 minutes, the management board crosswalk and the FY2026 working file: thirty institutions and four system offices participate, with a 94.6 percent transition percentage, a $2,655,000 pool and a $3,125,000 chargeable ceiling.
2. Build the fall 2023 certified adult learner base: keep undergraduate adults (age codes 8 to 13) for the thirty institutions, remove fall-term cross-enrolled adult guests at the host (amended register pairs counted once), assign tiers on certified headcount, and price on Schedule A: 32,497 learners and $22,345,800.
3. Replay FY2022 and FY2024 on fall 2019 and fall 2021 and confirm both statements reproduce to the dollar, including the FY2024 76 percent floor (four institutions, $47,550).
4. Apply the FY2026 floor at 94.6 percent of each FY2024 allocation under sections 4 to 7: ten institutions are floored, the reserve cost is $483,491, and the thirty total $22,829,291.
5. Apply section 9: recover the pool from all 34 participants in proportion to chargeable allocation, capped at $3,125,000 on the allocation including the charge, and solve until the charges reproduce themselves. Delgado, the LSU System office and the LCTCS System office sit at the ceiling at $239,592.26 each.
6. Assign each institution's charge across its twelve age-by-attendance rows in proportion to Schedule A amount; the 360-row charge column totals $1,885,190, and the four system offices carry $769,810.
7. Identify Baton Rouge Community College as the institution nearest the ceiling without reaching it, by $990,055.
8. Write the CSV schedule, the memo leading with $1,885,190 and $769,810, and the chart titled with $1,885,190 and the thirty's 71.01 percent pool share.

### Key traps (what the model did)

- Applied the section 9 administration charge to printed allocations in one pass. The guideline makes the charge part of the allocation, which makes it circular and requires a fixed-point solve with a ceiling cap. Without that solve nobody reaches the $3.125M ceiling, so the charge spreads proportionally and too much lands on the system offices. Every other stage (learner base, tiers, floor, replay) was correct.

### Justification

The guidelines and minutes fix every parameter, so the only open question is how the participants end up certified once the rules are worked through. The learner base and floor are validated by reproducing the FY2022 and FY2024 statements exactly. Section 9 counts the charge as part of allocation, so a self-consistent solution caps the three largest participants at the ceiling and shifts more of the pool onto the rest. The thirty institutions then carry $1,885,190, which is the total of the schedule's charge column.

## Commit to 102 seniors brought to a regular diploma by the 2027-28 Recovery schedule

**Credit Recovery Program Planning**, Batch 14, Policy & Education Analysis, model mean **0.45** over 4 runs (0.52, 0.52, 0.52, 0.52).

### What makes it strong (the client's note)

The trap is counting areas rather than students' timetables: 251 short seniors owe at most one credit in every area they are short in, but each senior can hold only one place per period, and 30 of them owe two areas that both meet in period 3, so the schedule could bring only 221 even with unlimited places.
A second trap is the offer order: under operations note 3.1 every one of the 286 short seniors is offered a place in each area they are short in and takes what is open, so the 35 who owe more than one credit in an area still consume 54 places. Leaving them out (143), taking every offered place regardless of periods (121), doing both (166) or allocating freely (192 or 186) all miss the filed walk.
The computation chain: build the 761 seniors from open eleventh-grade enrolment spans at the placement school, compute each one's Board Policy 218 shortfall by area (repeated courses counted once, senior timetable credit subtracted), read the 36 sections with their places and periods, then run the filed walk (most credits outstanding first, then student number; the area owed most first, level areas in policy order; released places re-offered).
Determinism pins: 286 short seniors; 221 could-bring; 102 brought; 119 for whom the places ran out (Raystown 60/18/42, Trough Creek 49/19/30, Standing Stone 39/16/23, Warriors Ridge 31/21/10, Sideling Hill 22/14/8, Cyber Academy 20/14/6); 12 of 36 sections turn students away; 1,260 places carried, 266 filled and 994 empty.

### Stakeholder ask (the prompt, verbatim)

Nothing about next year's recovery schedule is still open. The sections are staffed, the budget closed in June, and the offers go out in the order the office has used since the consolidation. What I cannot tell the board is what any of it buys. They vote the improvement plan on 29 September and mine is the name on the number, so what I need from you is how many of next year's seniors the 2027-28 recovery schedule brings to a regular high school diploma, as a whole number of students.

That number leads recovery_plan_2027_28.xlsx. Under it, the seniors who came out of the eleventh grade short of the board's graduation schedule in at least one subject area, and how many of those the schedule as it stands could bring to a diploma if none of its sections ran out of places, both as whole numbers. Then every school: the students the schedule could bring if no section ran out of places, the students the funded places do bring, and the gap between the two, worst first by that gap, then the subject areas where that school runs out of room, and a total row that ties back to the top.

The curriculum office will argue with me section by section, so those get their own sheet. Every school and every subject area the schedule runs, the places the section carries, the places the plan fills, the places left empty, and the students that area turns away, all whole numbers. My registrar reads rows rather than summaries, so the sheet after it is one row per senior who came out short, with the school we would place them at, the subject areas they are short in, the credits they still owe to two decimal places, and whether the plan gets them to the schedule.

The board will not vote this without knowing what the closed years delivered, so that goes in too, a row for each year and school. The places the schedule carried, the places students took, the places left unused. Then the students who took a place, the places that earned their credit, the students who cleared everything they owed that year, and the ones who passed one place and failed another the same year. Whole numbers, with a row across all the years at the foot.

Our number is only as good as the credit behind it, so two more sheets. Every school and subject area with the credit these seniors brought in from outside the district and our principals accepted, to two decimal places, and the seniors carrying it as whole numbers, then every outside school that sent any of it with the credit from each, most first and alphabetically where two are level. Then every school and subject area with the courses these seniors failed and later passed, as whole numbers, with the seniors behind them. Count both at the school we would place the student at, and give both a total row.

recovery_plan_review.png is what the board sees first. One bar per school on the students the schedule could bring if no section ran out of places, split into the ones the funded places get to a diploma and the ones the places ran out for, worst first, with both counts written on the bar. Beside it, every section where the places run out, the places that section carries drawn against the students who need it, both figures written at the bar. Title it with the number we are committing to.

### Deliverables

`recovery_plan_2027_28.xlsx`, `recovery_plan_review.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A school district's 2027-28 credit recovery schedule is fixed: sections are staffed, the budget is closed and offers go out in the order the recovery office files. Before the board votes the improvement plan, the official whose name is on the number needs how many of next year's seniors the schedule will bring to a regular diploma, as a whole number. The analyst works from enrolment spans, course credits, a legacy student information export, the graduation policy, the recovery register and schedule, the operations note, school references and other district records. Deliverables are `recovery_plan_2027_28.xlsx` (the headline first, then short and could-bring counts, a per-school table worst first by gap with a total row, a sections sheet, a one-row-per-senior registrar sheet, a closed-years sheet, an outside-credit sheet and a failed-then-passed sheet) and `recovery_plan_review.png` (school bars split between seniors the funded places bring and those the places run out for, beside the sections that run out, titled with the committed number).)

`20 files, 9.3 MB`, `accountability_guidance_2026_04.pdf`, `assessment_results.csv`, `board_policy_218_graduation.pdf`, `certification_thread.txt`, `course_credits_2019_2027.csv`, `data_dictionary.md`, `diplomas_conferred.csv`, `district_calendar.json`, `enrollment_spans_2019_2027.csv`, `export_manifest.csv`, `institution_directory.csv`, `legacy_sis_export_2019_2021.xlsx`, `records_requests_log.csv`, `recovery_operations_note.pdf`, `recovery_register_2020_2027.csv`, `recovery_schedule_2020_2028.csv`, `school_reference.csv`, `sis_draft_certification_2027.csv`, `state_report_cards_2023_2026.xlsx`, `students_2019_2027.csv`

### Final recommendation

The 2027-28 recovery schedule brings 102 of next year's seniors to a regular high school diploma: of the 286 seniors short of the Board Policy 218 schedule, 221 could be brought if no section ran out of places, and the funded places run out for 119 of them.

### Step-by-step solution

1. Build next year's seniors from the enrolment spans: students whose eleventh-grade enrolment was still open at the pull, at the school that enrols them (operations note 1.3), 761 students.
2. Compute each senior's shortfall against Board Policy 218 by area, counting a repeated course once and subtracting what the senior timetable carries: 286 are short in at least one area, and 251 owe at most one credit in every area they are short in.
3. Read the 2027-28 schedule: 36 year-term sections, six per school, with places and periods (English Language Arts in period 1, Mathematics in period 2, the other four areas in period 3).
4. Run the filed walk with unlimited places, one place per area and one per period: 221 could be brought; 65 could not, 35 because they owe more than one credit in an area and 30 because two of their areas meet in period 3.
5. Run the walk with the funded places over all 286 short seniors in the filed order: 102 end the year holding every credit they owed; 29 offers are declined for a period clash, 124 refused because the section is full, and 12 sections turn students away.
6. Take the per-school difference: the places run out for 119 of the 221, 42 of them at Raystown.
7. Build the remaining sheets (sections, registrar rows, closed years 2020-21 to 2026-27, outside credit, failed-then-passed courses) and the chart titled with 102.

### Key traps (what the model did)

- Counted recoverability area by area and ignored that each senior can hold one place per period, so 30 seniors owing two period-3 areas were counted as recoverable (251 instead of 221); the clash was at most mentioned as a risk.
- Ran the allocation walk but let offered places be taken regardless of period clashes, landing on 121 (a card-named wrong route) instead of 102; gap 130 instead of 119.

### Justification

The schedule is fixed and the offers follow the order the office files, so the committed number has to come from running that order over every short senior with the funded places and the periods sections actually meet in. Students who cannot be helped still take places, and students who owe two period 3 areas cannot be cleared in one year, so the answer is lower than any area-by-area count. On the filed walk, 102 seniors finish the year holding every credit they owed, and that is the number to put before the board.

## Fund the pre-proposal pathway that moves elevated r3/r4 concerns into division-chief proposal review

**Vehicle Safety Defect Investigation**, Batch 14, Public Safety & Justice, model mean **0.55** over 4 runs (0.54, 0.54, 0.55, 0.71).

### What makes it strong (the client's note)

The trap is the coarse escalation rate: elevated R3/R4 concerns turning into formal investigations fell from 42.9% to 20.0%, which points at the division-chief open/decline decision, but splitting that step at division-chief proposal review (a REV event by a DCH role in the log) shows the loss is entry into review, not the decision.
The computation chain: count each concern once by its primary issue record, assign it to its opening year, link formal openings to investigations.csv for recall outcomes, then trace R3/R4 concerns through division-chief proposal review to formal opening.
Determinism pins: 154 of 287 (53.7%) vs 82 of 285 (28.8%) reached division-chief proposal review; post-review yield 66.9% (103 of 154) vs 69.5% (57 of 82); median review-to-decision 9 days in both periods; restoring entry recovers about 49 openings, restoring yield recovers none.
Rivals the data rule out: intake was flat (1,518 vs 1,570 concerns, R3/R4 287 vs 285), and investigation-to-recall conversion moved only from 52.4% to 46.3%, about 5 of the 59 fewer recalls.

### Stakeholder ask (the prompt, verbatim)

NHTSA Defect Investigation Outcome Review

The number of formal defect investigations ending in a recall fell sharply after 2015. Leadership can fund one specific process-improvement workstream inside ODI's existing investigation process and needs to know where it should go.

Compare concerns opened in calendar years 2011-2015 with concerns opened in calendar years 2016-2020. Treat July 31, 2026 as the as-of date for investigations still open.

Deliverable:

Concise Word leadership note with the recommendation, supporting evidence, and one decision-useful visual.

Stick to supplied files.

### Deliverables

`ODI_Leadership_Note.docx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (NHTSA's Office of Defects Investigation (ODI) saw the number of formal defect investigations ending in a recall fall sharply after 2015, and leadership can fund one process-improvement workstream inside the existing investigation process. The analyst must compare concerns opened in 2011-2015 with concerns opened in 2016-2020, using an issue evaluation event log, its code list, ODI investigation and recall extracts, and the 2015 OIG report on ODI's defect process, treating July 31, 2026 as the as-of date for investigations still open. The analyst has to find the stage where the pipeline broke and name the workstream to fund. The deliverable is a concise Word leadership note with the recommendation, supporting evidence, and one decision-useful visual.)

`8 files, 15.9 MB`, `2015_OIG_Safety_Related_Vehicle_Defects_Report.pdf`, `Issue_Evaluation_Codes.csv`, `Issue_Evaluation_Log.csv`, `components.csv`, `investigation_vehicles.csv`, `investigations.csv`, `odi_flat_file_record_layout.txt`, `recalls.csv`

### Final recommendation

Fund the pre-proposal development and evidence-assembly pathway that moves elevated R3/R4 concerns into division-chief proposal review, not the division-chief open/decline decision or downstream investigation cycle-time management; entry into that review fell from 53.7% to 28.8% while post-review opening yield held at 66.9% vs 69.5%.

### Step-by-step solution

1. Count each concern once by its primary (PRI) issue record in Issue_Evaluation_Log.csv and assign it to its opening year: 1,518 concerns in 2011-2015 and 1,570 in 2016-2020, with 287 and 285 elevated R3/R4 concerns.
2. Link formal openings (FOP events with an action number) to investigations.csv: 185 vs 82 formal investigations (12.2% vs 5.2% of concerns), 97 vs 38 ending in a recall. PE19010, still open at July 31, 2026, counts as not ending in a recall.
3. Test investigation conduct: investigation-to-recall conversion fell only from 52.4% to 46.3%, about 5 of the 59 fewer recalls, so the loss is upstream of investigation.
4. For R3/R4 concerns, the formal-opening rate fell from 42.9% (123 of 287) to 20.0% (57 of 285). Split that step at division-chief proposal review (REV event, DCH role): 53.7% vs 28.8% reached review.
5. Among concerns that reached review, formal-opening yield was 66.9% vs 69.5%, and median review-to-decision time was 9 days in both periods, so the decision gate did not deteriorate.
6. Estimate recovery: restoring 2011-2015 entry adds about 49 formal openings; restoring 2011-2015 post-review yield adds none.
7. Locate the lost escalations: R3/R4 concerns ending in monitor status rose from 18 to 68, and in 2016-2020 R3/R4 concerns whose first step took more than 30 days reached review 19.0% of the time (32 of 168) vs 42.7% (50 of 117) when timely.
8. Recommend funding the pre-proposal pathway and write the note with the recommendation first, the evidence, a workstream comparison table, and one pipeline chart of R3/R4 concerns, review entries and formal openings for both periods.

### Key traps (what the model did)

- Diagnosed the funnel at the coarse stage the data naturally offers (R3/R4 concern -> formal investigation/PE opening) and funded the open/decline gate; never split that step at the division-chief proposal-review event (REV by DCH role) that sits inside it.

### Justification

Recalls fell because far fewer concerns became formal investigations, not because investigations converted worse or intake shrank. Inside the escalation step, the break sits before division-chief proposal review: half as many elevated concerns reached review in 2016-2020, while those that did were opened at the same rate and decided just as fast. Funding the open/decline decision or review speed would target a stage that did not deteriorate. The pre-proposal pathway, where elevated concerns are developed and routed into review, is where restoring performance recovers about 49 openings, consistent with the 2015 OIG finding on weak pre-investigation analysis and supervision.
