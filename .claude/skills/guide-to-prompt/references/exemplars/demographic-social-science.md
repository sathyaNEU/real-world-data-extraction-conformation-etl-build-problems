# Exemplars: Demographic & Social Science

> 5 accepted tasks in this domain, sorted by the current model's measured mean, lowest (hardest) first. Each is the client's own record. Index and the shared architecture: `index.md`.

## Send the field-support cycle to middle atlantic metro 1m+

**County Domestic Migration**, Batch 14, Demographics & Social Science, model mean **0.19** over 4 runs (0.21, 0.20, 0.19, 0.16).

### What makes it strong (the client's note)

The trap is the averaging basis: the March pack's +2.35 per 1,000 is a mean of county rates, while the resident-weighted national rate is -0.005 (net -1,610 on 331,390,416). Averaged over counties both metro (+4.35) and nonmetro (+1.11) gain, which is impossible in a closed system, and a county-average ranking sends the cycle to a small rural Pacific group instead.
The computation chain: take the IRS 97/000 Total Migration-US summary records (n2, exemptions) per county on both sides, net them, join the long-format RUCC 2023 file for population and class (with Connecticut's nine planning regions), map divisions many-to-one, then aggregate net and population by group before dividing.
Determinism pins: Middle Atlantic metro 1m+ at -6.58 per 1,000 (46 counties, 30,341,805 residents, net -199,640), Pacific metro 1m+ at -5.29 (net -205,958), gap 1.29, and 39,239 residents of movement into the Middle Atlantic group to close it.
The binding constraint is rate, not level: Pacific loses more residents in absolute terms but on a larger base, so a ranking by net loss would pick the wrong group.

### Stakeholder ask (the prompt, verbatim)

One member group takes next year's field-support cycle, and I want the decision made off the migration numbers, not argued in the room. Our member groups are census division crossed with rural-urban class, same as always. We have capacity for exactly one group, and the cycle should go where we are losing people worst, not where it is easiest or most comfortable to send it.

I run the county indicators program here, and on Monday I have to tell the board where the cycle goes. Name the single member group that takes it, based on net domestic migration per 1,000 residents from 2022 to 2023.

Start with loss_concentration.pdf, the one-pager the board reads. Name the group receiving the cycle and the group just behind it, then show how far apart they are and what it would take for the runner-up to close the gap. Show how the national number breaks down to the group you picked, because the first question I will get is why the cycle is not going to somebody else's patch. Put the national picture at the top in one sentence. Our March pack has been telling members that counties gained about 2.35 people per thousand on average last year.

Then segment_drilldown.csv, the file that goes around to members. Include every group with its counties, residents, and rate so a state office can find itself in the file. Also include the counties that make up the group receiving the cycle.

Put the determination on drilldown_path.png as well. Show how the national number breaks down and where the selected group sits against the rest. Put the committed group and its rate in the title.

### Deliverables

`loss_concentration.pdf`, `segment_drilldown.csv`, `drilldown_path.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A county indicators program has capacity for one field-support cycle and must send it to the member group (census division crossed with rural-urban class) losing residents worst on net domestic migration per 1,000 residents, 2022 to 2023. Working from the IRS SOI county inflow and outflow files, the USDA ERS 2023 Rural-Urban Continuum Codes (population and class), and the Census county geography file, the analyst must collapse the county-pair files to county net migrants, attach population, RUCC and division, score every group, and name the winner and the runner-up with the gap and what would close it. The board also needs the national figure traced down to the chosen group, and a one-sentence national picture that squares the March pack's +2.35 per 1,000 county average with what residents actually did. Deliverables are `loss_concentration.pdf` (the board one-pager), `segment_drilldown.csv` (every group with counties, residents and rate, plus the counties in the chosen group), and `drilldown_path.png` (the breakdown and ranking, with the committed group and its rate in the title).)

`14 files, 12.9 MB`, `2223inpublicmigdoc.pdf`, `2361.csv`, `Ruralurbancontinuumcodes2023.csv`, `county_geography.csv`, `countyinflow2223.csv`, `countyoutflow2223.csv`, `data_dictionary.json`, `overview.xlsx`, `permits_by_county_year_structure.csv`, `region_division_codes.csv`, `ruralurbancodes2013.xls`, `series_types.csv`, `structure_types.csv`, `years.csv`

### Final recommendation

Send next year's field-support cycle to the Middle Atlantic metro 1m+ group, the 46 metro counties of a million or more in New York, New Jersey and Pennsylvania, which lost a net 199,640 residents on 30,341,805 for -6.58 per 1,000, the deepest rate of any group and 1.29 ahead of Pacific metro 1m+.

### Step-by-step solution

1. Collapse the IRS county-pair files to county grain using the 97/000 Total Migration-US summary record on each side (3,096 inflow and 3,111 outflow records), with n2 (exemptions) as the person count; no suppressed values appear in those records.
2. Compute net domestic migrants as inflow minus outflow per county.
3. Join Population_2020 and RUCC_2023 from the 2023 rural-urban file, giving 3,087 units and 331,390,416 residents; Connecticut is carried as nine planning regions.
4. Attach census divisions from the county geography file; 87 units with no division match are kept as their own group.
5. Compute the national figure both ways: +2.35 per 1,000 as a county mean, -0.005 per 1,000 weighted by residents (net -1,610).
6. Test both bases: county averaging puts metro at +4.35 and nonmetro at +1.11, both gaining against a negative national net, so the county basis fails; resident weighting gives -0.38 and +2.36, which reconcile.
7. Score every division by rural-urban group as group net over group population times 1,000 and rank.
8. Read off the winner: Middle Atlantic metro 1m+ at -6.58 (46 counties, 30,341,805 residents, net -199,640).
9. Identify the runner-up, Pacific metro 1m+ at -5.29 (net -205,958), a gap of 1.29 per 1,000, equal to 39,239 residents of net movement into the Middle Atlantic group.
10. Trace the breakdown: national to metro (-0.38) to RUCC 1 metro 1m+ (-1.95, net -368,877) to Middle Atlantic, which holds 54.1 percent of the metro 1m+ net loss from 10.4 percent of its counties.
11. Write the PDF, the CSV with group rows and the 46 county rows, and the PNG.

### Key traps (what the model did)

- Collapsed the rural-urban class into a binary Metro (RUCC 1-3) / Nonmetro split, so the member groups became 18 coarse division x metro cells instead of division x RUCC code; every figure (rate -5.18, runner-up -4.30, gap 0.88) was computed on the wrong segment.
- Avoided the county-average trap (used resident weighting) but never quantified or refuted the March +2.35 county-average figure: did not show that county averages make both metro (+4.35) and nonmetro positive, impossible in a closed system.

### Justification

The board asked for the group losing people worst, which is a question about residents, so the rate has to be total net over total population for each group. That basis reconciles to the near-zero national net that a closed domestic system requires, while averaging county rates does not and sends the cycle to a 165,404-resident rural Pacific group. On the resident basis Middle Atlantic metro 1m+ leads outright at -6.58 per 1,000. Pacific metro 1m+ loses slightly more people in total but on a population 8.6 million larger, so its rate is lower and it comes second. The March figure of +2.35 is accurate as a county average, but it describes the typical county, not where residents went.

## Act on the brennan hale move to wyburn gate with a site travel plan and bus link

**Commuting and Travel Survey Analysis**, Batch 14, Demographics & Social Science, model mean **0.21** over 4 runs (0.27, 0.26, 0.26, 0.26).

### What makes it strong (the client's note)

The trap is the tabulation: the journey file invites a mean over journeys with every work-purpose journey counted, which returns only 24 of the 32 published means and leaves R1 (the Fellbridge line closure) standing; the published measure is a mean across respondents of each respondent's diary-week mean, counting only journeys ending in the usual workplace zone or a neighbour, and only that combination returns 32 of 32.
The computation chain runs from joining four survey files and the zone neighbour lists, through respondent-level means, to group-versus-rest differences on full-year, half-year, prior-year and paper-only subsets, then scale as direction times group share.
Determinism pins: R2 direction 8.8, scale 0.6, persistence 0.9, prior movement -3.4, recording 14.0; R5 scale 0.3; R1 persistence -1.4; area-wide rise 1.5 minutes.
The binding constraint is Protocol paragraph 8 (act only on the candidate consistent on every line): R5 holds on four lines but fails scale, and the call would turn if R2 explained no more than 0.3 minutes.

### Stakeholder ask (the prompt, verbatim)

Which of the five changes on the register lies behind the rise in journey times to work between 2024-25 and 2025-26, what response goes with it, and how many minutes of the rise does it account for? The Housing and Transport Committee takes that call in September. Nothing for 2025-26 has been released, so the supporting analysis has to come from the survey extracts in the folder.

Put it in journey_time_cause_note.docx, short enough for the Committee's papers. Lead with the cause, its response and the minutes behind it. Then the strongest rival, the line of evidence that rival fails, the margin between them on the minutes each explains, and the figure at which the call would turn. Include the area-wide movement between the years, and every sector's 2025-26 mean beside its 2024-25 mean. I need to know whether your working returns all thirty-two published sector means, and which ones it misses if any, and what setting the app diaries aside would do to the minutes you have put behind the cause.

For the room, journey_time_evidence_review.pptx, a handful of slides. The centrepiece is a grid of the five candidate causes against the five lines of evidence, each cell showing its figure in minutes to a tenth and whether it is consistent, with the chosen cause highlighted. Beneath it, plot the quarterly mean journey time for that cause's group against everyone else across both years.

### Deliverables

`journey_time_cause_note.docx`, `journey_time_evidence_review.pptx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A city region's Housing and Transport Committee must decide in September which of five registered changes lies behind the rise in journey times to work between 2024-25 and 2025-26, and which response to agree. No 2025-26 figures have been released, so the analyst has to work from household travel survey extracts (journeys, respondents, households, employment module, zone system) under the Production Rules, which allow only a tabulation that returns every published sector mean, and the Attribution Protocol, which tests each candidate on direction, scale, persistence, prior movement and recording. The analyst must find the tabulation that reproduces all 32 published means, compute the 25 grid figures, pick the one candidate consistent on every line, size the minutes it explains against the strongest rival and the turning point, and test the councillor's proposal to set the app diaries aside. Deliverables are `journey_time_cause_note.docx` (cause, response and minutes first, then the rival, its failing line, the margin, the turning figure, the area-wide movement, all eight sectors for both years, the 32-mean check and the app-diary effect) and `journey_time_evidence_review.pptx` (the five-by-five grid with R2 highlighted and a quarterly chart of R2's group against everyone else).)

`14 files, 16.3 MB`, `attribution_protocol_2024.pdf`, `brennan_hale_relocation_letter_2025-03.txt`, `calvermoor_zone_system_2021.json`, `change_register_2025-26.xlsx`, `fellbridge_line_closure_notice_2025.txt`, `housing_transport_committee_minute_2026-07-14.pdf`, `hts_data_dictionary.txt`, `hts_employment_module_2021-2026.tsv`, `hts_fieldwork_note_2025-26.txt`, `hts_households_2021-2026.csv`, `hts_journeys_work_purpose_2021-2026.csv`, `hts_respondents_2021-2026.csv`, `hts_statistical_release_sector_times.csv`, `travel_statistics_production_rules_2020.pdf`

### Final recommendation

Act on R2, the Brennan Hale operations centre move to Wyburn Gate, by agreeing a site travel plan with Brennan Hale that includes a scheduled bus link from the city centre; it accounts for 0.6 of the 1.5 minute rise.

### Step-by-step solution

1. Define the movement to explain: the change in the area-wide mean journey time to work between 2024-25 and 2025-26, with sector, survey year, quarter, journey time and rounding fixed by Production Rules 3, 4, 5 and 7.
2. Take the five register changes as candidates, each with the group the register defines on survey fields, and the Protocol's five tests.
3. Find a tabulation that returns all 32 published means (rules 11 and 12): a per-journey mean over all work-purpose journeys returns 24; the mean across respondents of each respondent's diary-week mean, counting only journeys ending in the usual workplace zone or a neighbouring zone, returns 32.
4. Compute the 25 grid figures on that tabulation. R2: direction 8.8, scale 0.6, persistence 0.9, prior movement -3.4, recording 14.0, consistent on all five.
5. Rule out the rivals: R1 fails scale, persistence and prior movement; R3 fails direction, scale, prior movement and recording; R4 fails direction, scale and prior movement; R5 fails scale only (0.3 minutes).
6. Report that R2 accounts for 0.6 of the 1.5 minute rise, 0.3 more than R5, and that the call would turn if R2 explained no more than 0.3 minutes.
7. Tabulate each sector for both years (CEN 14.4 to 15.4, KES 28.9 to 31.5, GRY 28.6 to 31.0, FEL 26.8 to 29.7, PEL 26.9 to 28.0, WYB 27.1 to 28.1, LAN 29.6 to 29.3, STN 28.9 to 30.0).
8. Test the app-diary proposal: on paper diaries alone R2 explains 0.9 minutes, but that tabulation returns only 29 of the 32 published means, so it cannot be relied on.
9. Write the note leading with the cause, response and minutes, and build the slides with the highlighted grid and the quarterly chart (R2's group rises from 26.8 to 27.4 minutes in early 2024-25 to 38.4 to 40.2 minutes in 2025-26, while everyone else stays between 26.2 and 27.7).

### Key traps (what the model did)

- Tabulated journey time as a mean over journeys with every work-purpose journey counted, which points to R1 (Fellbridge closure), and adopted it while openly stating the working returned only 24 of 32 published sector means.
- Carried the wrong tabulation through to every downstream figure: area-wide rise 2.5 vs 1.5 minutes, R2 scale 0.2 vs 0.6, wrong response (rail bus-priority plan).

### Justification

The Protocol picks the candidate consistent on all five lines, and the Production Rules allow only a tabulation that reproduces every published figure. On the one tabulation that returns all 32 published means, R2 is the only candidate that passes every test: its group's journey times rose 8.8 minutes more than everyone else's, the gap held among paper diarists and widened after the staff shuttle was withdrawn at the end of September, and it accounts for 0.6 minutes, more than any rival. R5 comes closest but explains only 0.3 minutes and fails scale. The journey-level reading that would point to the Fellbridge closure, and the paper-only reading that would inflate R2 to 0.9, both miss published figures and are barred.

## Determine beltrami, becker, hubbard, clearwater, mahnomen & Lake of the woods counties, mn for the continuation phase at 2.764323

**Employment Program Evaluation**, Batch 14, Demographics & Social Science, model mean **0.31** over 1 runs (0.35).

### What makes it strong (the client's note)

Two decoys each name a different leader: the interim certification puts Porter County, IN first at 1.814695, and the field briefing, which uses raw changes with no comparison group, puts Kent County (North), MI first at 3.885217; a single-pass construction also hands the round to Kent County (North) at 2.246758 and reproduces only 1 of the 23 certified figures.
The comparison-group construction has to be recovered from the certified record: parts drawn from the service model's recorded respects, a counting floor, a nearest-areas share of the undesignated same-state field, and alternating application until stable, with the comparison rate standardized to the site's base-window composition.
Computation chain: filter 1,686,803 person records to a 1,019,300-person universe (group quarters identified by RELP in the 2013 to 2018 files and RELSHIPP from 2019), aggregate by area, year and part, rebuild 23 certified figures, then compute seven final-basis figures.
Determinism pins: determined site 2.764323 (own change 2.789650, base 83.152, follow-up 85.941, 24 comparison areas moving 0.025327); challenger 1.563883 (own 2.114383, 37 areas moving 0.550500); distance 1.200440, 43.43 percent of the determined figure.

### Stakeholder ask (the prompt, verbatim)

Our Evaluation Panel meets shortly and I need the 2017 round of the Work Reattachment Initiative settled before it does.

Background: the Halverdine Trust has run the Initiative since 2016. Sites are named in rounds, a caseworker team goes in for three years, then the Panel certifies an adjusted employment change for each site, once when two follow-up survey years exist and again when there are three. One site from whichever round is still outstanding then gets the continuation phase.

2016 is finished on both bases. The 2017 round was certified on the interim basis in November 2023 and has sat there since, because the Trust suspended the continuation phase that spring and only restarted it this year. Seven sites. The 2018 round can't be certified at all, EP-4 says why, so leave it.

I'm the Panel's secretary rather than an analyst, and whoever ran the last two cycles retired in the spring without leaving working papers, so you're starting cold. It's all in inputs/.

Read EP-4 and the two Panel reports before you go near the microdata. The protocol settles the population, the universe, the outcome, both windows and the arithmetic. What it won't tell you is how the Panel assembles a comparison group, and that's deliberate. Paragraph 5.3 makes the certified record the test instead: twenty-three figures are certified between the two reports, and a construction is only ours if it returns every one. So rebuild the record first, then carry the same construction across to certify 2017 on the final basis. Nothing gets adjusted afterwards.

Two warnings. Don't assume the interim order carries over, the Panel says as much in its report. And there's a field briefing in the program folder, our program officer's, from August: worth reading, but it isn't a determination and wasn't made under EP-4.

Three files.

continuation_determination_2026.docx is what the Panel votes on, so lead with the determination. Which site, its adjusted employment change on the final basis, the own change behind it with both window rates, how many areas its comparison group holds and how far the group moved. Then the same for the closest challenger, the distance between the two, what that distance comes to as a percentage of the determined figure, and how far the challenger would have to come up to take it. Say whether the construction reproduced all twenty-three certified figures; the line-by-line reconciliation goes in the workbook. And since the interim certification and the field briefing each put a different site on top, explain why yours differs from both.

site_effect_chart.png. One horizontal bar per site, ranked on the final basis, the determined site picked out, a zero line, each bar labeled with its adjusted change and the size of its comparison group. Mark each site's own change and its comparison group's change on the same scale too, so the Panel can see where the difference comes from. Determination in the title.

evaluation_worksheet_2026.xlsx holds the numbers. First sheet named sites, a row per site, columns rank, site_code, site, state, base_rate, followup_rate, own_change, comparison_areas, comparison_change, counted_parts, certified_interim, adjusted_change and movement, movement being the final figure less the interim. Second sheet named record, a row per certified figure, columns site_code, site, state, round, basis, certified and rebuilt.

Six decimals throughout, apart from the window rates, which go to three. Name sites the way the area reference names them, then a comma and the two-letter state.

Last thing, the Trust is strict on it. EP-4 8.2 says nothing prepared for the Panel may set out how a comparison group is assembled, and that binds all three files. Sizes, movements, counted parts, the figures themselves, all fine. Not the method.

### Deliverables

`continuation_determination_2026.docx`, `site_effect_chart.png`, `evaluation_worksheet_2026.xlsx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A charitable trust's Evaluation Panel must determine which of the seven 2017-round sites of its Work Reattachment Initiative receives the continuation phase, on the final basis that became possible once the 2021 survey year arrived. Protocol EP-4 fixes the universe (persons aged 25 to 54 in housing units with employment status recorded, weighted by PWGTP), the windows (base 2014 to 2016, follow-up 2018, 2019 and 2021 with 2020 absent) and the arithmetic (own change less comparison-group change), but it deliberately does not say how a comparison group is assembled; instead, paragraph 5.3 makes the twenty-three certified figures in two Panel reports the test any construction must pass to six decimals. Working from 48 files of Census person microdata across six states, the analyst must rebuild that record, carry the same construction to the 2017 final basis, determine the site with its figure, challenger and distance, and explain why the interim certification and a program officer's field briefing each put a different site on top, all without disclosing the construction (EP-4 8.2). Deliverables are `continuation_determination_2026.docx` (the memo the Panel votes on), `site_effect_chart.png` (ranked horizontal bars with own and comparison changes marked) and `evaluation_worksheet_2026.xlsx` (a sites sheet and a 23-row record sheet).)

`79 files, 90.7 MB`, `archive_manifest.csv`, `2021ACS_PUMS_User_Guide.pdf`, `ACS2013_PUMS_README.pdf`, `ACS2014_PUMS_README.pdf`, `ACS2015_PUMS_README.pdf`, `ACS2016_PUMS_README.pdf`, `ACS2017_PUMS_README.pdf`, `ACS2018_PUMS_README.pdf`, `ACS2019_PUMS_README.pdf`, `A_Note_on_2020_ACS_1yr_PUMS.pdf`, `PUMSDataDict13.txt`, `PUMSDataDict14.txt`, `PUMSDataDict15.txt`, `PUMSDataDict16.txt`, `PUMSEQ10_18.txt`, `PUMSEQ10_19.txt`, `PUMSEQ10_26.txt`, `PUMSEQ10_27.txt`, `PUMSEQ10_29.txt`, `PUMSEQ10_55.txt`, `PUMS_Data_Dictionary_2017.csv`, `PUMS_Data_Dictionary_2018.csv`, `PUMS_Data_Dictionary_2019.csv`, `PUMS_Data_Dictionary_2021.csv`, `pums_person_ia_2013.csv`, `pums_person_ia_2014.csv`, `pums_person_ia_2015.csv`, `pums_person_ia_2016.csv`, `pums_person_ia_2017.csv`, `pums_person_ia_2018.csv`, `pums_person_ia_2019.csv`, `pums_person_ia_2021.csv`, `pums_person_in_2013.csv`, `pums_person_in_2014.csv`, `pums_person_in_2015.csv`, `pums_person_in_2016.csv`, `pums_person_in_2017.csv`, `pums_person_in_2018.csv`, `pums_person_in_2019.csv`, `pums_person_in_2021.csv`, `pums_person_mi_2013.csv`, `pums_person_mi_2014.csv`, `pums_person_mi_2015.csv`, `pums_person_mi_2016.csv`, `pums_person_mi_2017.csv`, `pums_person_mi_2018.csv`, `pums_person_mi_2019.csv`, `pums_person_mi_2021.csv`, `pums_person_mn_2013.csv`, `pums_person_mn_2014.csv`, `pums_person_mn_2015.csv`, `pums_person_mn_2016.csv`, `pums_person_mn_2017.csv`, `pums_person_mn_2018.csv`, `pums_person_mn_2019.csv`, `pums_person_mn_2021.csv`, `pums_person_mo_2013.csv`, `pums_person_mo_2014.csv`, `pums_person_mo_2015.csv`, `pums_person_mo_2016.csv`, `pums_person_mo_2017.csv`, `pums_person_mo_2018.csv`, `pums_person_mo_2019.csv`, `pums_person_mo_2021.csv`, `pums_person_wi_2013.csv`, `pums_person_wi_2014.csv`, `pums_person_wi_2015.csv`, `pums_person_wi_2016.csv`, `pums_person_wi_2017.csv`, `pums_person_wi_2018.csv`, `pums_person_wi_2019.csv`, `pums_person_wi_2021.csv`, `final_evaluation_report_2023.pdf`, `interim_evaluation_report_2021.pdf`, `area_reference.xlsx`, `designation_record.csv`, `field_briefing_2026.docx`, `evaluation_protocol_EP4.pdf`, `service_model.docx`

### Final recommendation

Determine Beltrami, Becker, Hubbard, Clearwater, Mahnomen & Lake of the Woods Counties, MN for the continuation phase at a final-basis adjusted employment change of 2.764323 percentage points, with Kent County (North), MI the closest challenger at 1.563883 and a distance of 1.200440 points.

### Step-by-step solution

1. Read EP-4 and the two Panel reports to fix the universe, the windows, the arithmetic and the 23-figure test: 16 figures for the 2016 round on both bases and 7 for the 2017 round on the interim basis.
2. Apply the universe to the microdata: 1,686,803 records across 270 areas reduce to 1,019,300 persons aged 25 to 54 in housing units with employment status recorded, with group quarters identified as RELP 16 and 17 up to 2018 and RELSHIPP 37 and 38 from 2019.
3. Use the service model's recorded respects and fixed categories and the area reference to define each site's comparison pool as its own state's never-designated areas.
4. Aggregate to area by year by part, holding unweighted counts, weights and employed weights.
5. Search candidate constructions against the certified record; the one that returns all 23 figures to six decimals is iterated, and a single-pass version fails.
6. Certify the 2017 round on the final basis with that construction unchanged: Beltrami et al., MN 2.764323; Kent County (North), MI 1.563883; Porter County, IN 1.538381; Ionia et al., MI 0.364181; Grant, Miami & Wabash, IN -0.328522; Racine County, WI -0.341774; Noble et al., IN -0.899153.
7. Decompose the determined site: own rate 83.152 to 85.941, a change of 2.789650, against 24 comparison areas moving 0.025327 over 12 counted parts.
8. Decompose the challenger: own change 2.114383 against 37 areas moving 0.550500. The distance is 1.200440, 43.43 percent of the determined figure, which is also the rise the challenger would need.
9. Compare bases: Porter County falls from 1.814695 to 1.538381 (movement -0.276315) while the determined site rises 1.050473 from 1.713851.
10. Compare with the field briefing: Kent County (North)'s raw rise of 3.885217 becomes 2.114383 on the counted parts, and its comparison group rose 0.550500 against 0.025327 for the determined site's.
11. Produce the memo (determination first, conformance statement, the two explanations, no construction details), the chart, and the two-sheet workbook.

### Key traps (what the model did)

- Named the right site and challenger but with a comparison-group construction that reproduced none of the 23 certified figures; carried the non-reproducing construction forward and stated the failure openly (determined 3.163180 vs 2.764323, distance 1.276067 vs 1.200440, wrong group sizes).

### Justification

EP-4 certifies an adjusted figure, so the raw changes in the field briefing cannot settle the round, and the Panel's own report says the interim order is not a forecast of the final one. The only admissible construction is one that returns every certified figure, and the construction that does so gives the Minnesota site 2.764323 because almost its entire 2.789650 own rise survives a comparison group that barely moved, while Kent County (North)'s smaller rise on the counted parts is offset by a comparison group that gained 0.550500. The resulting 1.200440 distance is 43 percent of the determined figure, a clear margin rather than a near tie.

## Name kelnbrook the 2025 leading origin over eastwick by a 2.72 Movement gap

**Internal Migration Statistics**, Batch 14, Demographics & Social Science, model mean **0.54** over 4 runs (0.98, 0.18, 0.93, 0.15).

### What makes it strong (the client's note)

The trap is Redwater: it has the largest movement (+7.57), but its 2025 flow of 795 persons falls below the 900-person reliability threshold set by the Disclosure Control Policy, so it cannot be determined on.
A second rival is Eastwick, which sends the most relocations and has the largest from-address rise. On the Standard's person-grain basis its movement is only +3.88 per thousand of a 72,400 base.
The attribution basis matters: 304 of Kelnbrook's 1,035 residents reached the city on relocations recorded from other districts, so a from-address count understates Kelnbrook's rise.
The computation chain covers record-version deduplication, postcode normalisation and gazetteer resolution, register attribution at the reference date, rates rounded to two decimals, movement, qualification, and tie-break rules (Articles 5.4 to 5.6).

### Stakeholder ask (the prompt, verbatim)

I need help working out which district the Office will name as the leading origin under the Standard.

the supplied materials includes the relocation returns for both years, a person-level register extract and the published area counts that should reconcile against it, a time-versioned postcode gazetteer, the Office's disclosure control policy, an area directory, and a data dictionary.

Once the leading origin is determined, its liaison officer must receive the determination and the underlying figures a week before the Division sends its formal letter to them. Flag the date this needs to go out by.

Put the determination in leading_origin_determination.pdf, a short memo on Office letterhead with a reference for the meeting pack. Open with the leading origin, its movement, the runner-up and the gap between them, in migration rate per thousand as the Standard defines it, to two decimal places. Then rank all districts by movement, showing each district's flow in whole persons, its migration rate in each of the two years and whether it qualified. Include one chart of movement by district with the leading origin and the runner-up marked, styled to be readable when projected for the meeting. Close with how many more persons the runner-up would have needed in the determination year to be named instead, and how many fewer persons the leading origin could have had that year and still qualified.

Also, give me leading_origin_determination.py. It should take the path to the supplied materials as its only argument and print the same determination and ranked table from the files as shipped. Nothing should be hard-coded or depend on where it is run, and it should work unchanged on next year's pack.

Use two decimal places for rates and movements and whole persons for flows, and keep the figures the same across the paper, the chart and the script.

### Deliverables

`leading_origin_determination.pdf`, `leading_origin_determination.py` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A regional statistics office must determine which of twelve districts is the leading origin of migration to the city of Halden for 2025 under its Internal Migration Compilation Standard. The pack holds the 2024 and 2025 relocation returns, a person-level register extract with the published area counts it should reconcile against, a postcode gazetteer, the Disclosure Control Policy, an area directory and a data dictionary. The analyst must keep the applying version of each relocation record, resolve messy postcodes to areas, attribute every person bound for the city to their register district of usual residence at the reference date, compute migration rates per thousand and their movement, apply the 900-person reliability threshold, and rank the districts. The determination goes in `leading_origin_determination.pdf` (an Office letterhead memo with a meeting-pack reference, the headline determination, the twelve-district ranked table, one projection-ready chart and the two in-hand figures), and `leading_origin_determination.py` must reproduce it from the pack path alone. The analyst must also flag the date by which the liaison officer needs the figures.)

`12 files, 8.2 MB`, `SOURCES.csv`, `area_directory.json`, `data_dictionary.md`, `determination_notice_2025.pdf`, `disclosure_control_policy.pdf`, `internal_migration_compilation_standard.pdf`, `postcode_gazetteer.xlsx`, `register_counts_by_area.csv`, `register_extract_relocating_persons.csv`, `relocation_reason_codes.csv`, `relocations_2024.csv`, `relocations_2025.csv`

### Final recommendation

Name Kelnbrook (KLN) the 2025 leading origin with a movement of +6.60 per thousand; Eastwick (EST) is runner-up at +3.88, a gap of 2.72, and Redwater is excluded because its 795-person flow is below the 900-person threshold.

### Step-by-step solution

1. Read the notice (determination year 2025, comparison year 2024, reference dates 1 January) and the Policy's 900-person reliability threshold.
2. Keep the highest-version record for each relocation identifier, keep relocations dated in the year, normalise postcodes for case and spacing, and resolve destinations through the gazetteer. This leaves 7,173 city-bound relocations in 2024 and 7,429 in 2025.
3. Attribute each person on those records to their register district of usual residence at the reference date: 18,432 persons in 2024 and 19,239 in 2025.
4. Compute each district's rate per thousand of its published resident count, to two decimals, and the movement. Kelnbrook goes from 31.59 to 38.19 (+6.60), Eastwick from 31.18 to 35.06 (+3.88) and Redwater from 33.84 to 41.41 (+7.57).
5. Apply the qualifying rule. Redwater's 2025 flow of 795 is below 900, so it does not qualify. Every other district is above 900.
6. Rank the qualifying districts by movement: Kelnbrook first, Eastwick second, gap 2.72. The full table runs Redwater, Kelnbrook, Eastwick, Northolme, Coldharbour, Grendale, Langmere, Oakfield, Farrowmere, Hathersett, Brenmoor, Marston.
7. Test the margins. Eastwick needs 198 more 2025 persons to overtake (at 197 the movements tie at +6.60 and Article 5.5 favours Kelnbrook's higher 2025 rate, 38.19 against 37.78). Kelnbrook could lose 135 persons and still meet the threshold.
8. Flag the send-by date for Kelnbrook's liaison officer as one week before the Division's formal letter.
9. Write the letterhead memo with the table and chart, and the script that rebuilds the determination and table from the pack path.

### Key traps (what the model did)

- Attributed migrants by from-address on the relocation returns instead of placing persons by the register at the reference date, which understates Kelnbrook (movement 1.08-1.34 vs 6.60) and crowns Eastwick, with Northolme as runner-up.

### Justification

The Standard measures each district by the persons the register places there at the reference date, per thousand residents, and only districts with at least 900 persons in the 2025 flow can be determined on. On that basis Redwater has the largest movement but is too small to qualify. Eastwick sends the most people, but per thousand residents its movement is modest. Kelnbrook's rate rose 6.60 points, much of it from residents who moved via addresses in other districts. That is 2.72 points ahead of Eastwick, with 198 persons of margin against an Eastwick overtake and 135 persons of headroom over the threshold.

## Block-contract 899 beds for residents aged 85 and over in 2032/33 And publish the 47-Bed gap

**Adult Social Care Capacity Planning**, Batch 14, Demographics & Social Science, model mean **0.62** over 4 runs (0.79, 0.79, 0.73, 0.23).

### What makes it strong (the client's note)

The trap is stopping at the demand model. The requirement plus margin gives 946 beds for 2032/33, but five homes have given notice to deregister, so only 899 block beds will exist, and the brief forbids contracting for beds that do not exist.
The computation chain runs from a five-year single-age roll-forward (8,853 to 10,000 residents aged 85 and over), through three log-linear rate projections labelled by the 31 March year end, to a Home First effect converted from a 12 percent admissions cut to a 6.86 percent caseload cut using the 57.1 percent of placements begun within two years.
Hidden data traps: the population's age 100 is open ended, so the register's 95 and over group must keep the 32 residents aged 101 and over (0.30400, not 0.26133). Mortality improvement is the council's recorded 0.27 percent a year, not the national 1.25 percent.
Determinism pins: contract 899, demand-based 946, requirement 919, margin 2.872 percent, capacity 1,014 / 1,013 / 994 / 953 / 899 with 2028/29 the peak, 63 below today's 962.

### Stakeholder ask (the prompt, verbatim)

Determine the residential and nursing bed capacity Calderwyn should block-contract for residents age 85 and over in 2032/33. I need one whole-number capacity figure; the Market Position Statement will be held to it for five years.

Use the same method to calculate capacity for every year from 2028/29 through 2031/32 and identify the highest year. Keep the population assumption and rate of use separate so the driver of the result is visible. For 2032/33, show whether the answer is above or below today's contracted capacity, by how many beds, and what causes the difference.

Four other figures are already circulating,from the Integrated Care Board, Finance, the Provider Forum, and the 2023 plan rolled forward,but none has been adopted. For each one, identify where its method diverges from the required method and quantify the effect of that difference in beds. Also separate the portion of the 2032/33 requirement that is already determined by people currently alive in Calderwyn from the portion that depends on forecast population.

Build the calculation from Calderwyn's own data using the conventions in the methods note; those conventions are binding. Do not use any of the four circulating figures as the starting point.

Provide a CSV in the layout used by the Statement, with one row per year showing population, rate, and capacity. Also provide one chart for the appendix.

The source data include single-year-of-age and sex mid-year estimates, ward breakdowns, registered deaths, births, migration flows, the placement register, care-home register, historical block-contract capacity versus actual placements, and the commissioning brief setting the required standard.

Report beds as whole numbers and rates to four decimal places.

### Deliverables

`answer.md`, `calderwyn_mps_capacity_85plus_2028_29_to_2032_33.csv`, `mps_appendix_capacity_chart.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A local council's demography team must set the residential and nursing block capacity for residents aged 85 and over that its Market Position Statement will be held to for five years, with 2032/33 as the year providers negotiate against. Four competing figures (Integrated Care Board, Finance, Provider Forum, and the 2023 plan rolled forward) are circulating, and none has been adopted. The analyst must project the population by cohort-component roll-forward on the council's own mortality and migration record, compute and project rates of use separately for ages 85 to 89, 90 to 94 and 95 and over from the placement register, convert the Home First admissions effect into a caseload effect, apply the brief's margin, check the result against the block beds that will still be registered, and do this for every year from 2028/29. They must also price each circulating figure's departure in beds and separate what is already settled by people alive today from what depends on forecasts. Deliverables are a CSV in the Statement's table layout (one row per year with population, rate and capacity) and one appendix chart.)

`14 files, 1.4 MB`, `adult_social_care_commissioning_brief.docx`, `births_registered_2011_2027.csv`, `care_home_register.csv`, `commissioned_capacity_and_placements.xlsx`, `deaths_registered_2011_2027.csv`, `demand_estimates_on_the_table.xlsx`, `demography_methods_note.pdf`, `home_first_evaluation.docx`, `migration_flows_2011_2027.csv`, `placement_register.csv`, `population_and_placement_data_dictionary.json`, `population_and_placements_2011_2027.png`, `population_estimates_la_single_year_2011_2027.csv`, `population_estimates_ward_2011_2027.csv`

### Final recommendation

Block-contract 899 beds for residents aged 85 and over in 2032/33, 63 fewer than the 962 held today. The requirement plus margin is 946 beds, but only 899 block beds will still be registered, so the Statement must publish the 47-bed gap beside the figure.

### Step-by-step solution

1. Treat the methods note and commissioning brief as binding. Take the mid-2027 single-year estimate as the base: 8,853 residents aged 85 and over (5,629 / 2,470 / 754).
2. Derive mortality improvement from the mean of the two sexes' age-standardised rates over 2023 to 2027 (log-linear, minus 0.266 percent a year). Pool deaths over population at risk for 2025 to 2027 at each single age to get base death probabilities.
3. Derive net migration rates by band over the five years to mid-2027 (85 and over: minus 0.000046), applied after survival.
4. Roll forward five years with no fertility term: 9,042, 9,254, 9,230, 9,513 and 10,000 residents aged 85 and over at mid-2028 to mid-2032.
5. Rebuild the stock at each 31 March from 2015 to 2027 from the placement register, with age last birthday from date of birth and 95 and over left open ended (1,003 at 31 March 2027: 394 / 381 / 228).
6. Compute rates as stock over the preceding June population (2026/27: 0.07160, 0.15698, 0.30400) and project each group log-linearly. The 2032/33 rates (at 31 March 2033) are 0.06374, 0.13641 and 0.26541, applied to mid-2032 population.
7. Requirement before Home First: 985, 984, 966, 966, 986. Home First starts 1 April 2031, and its 12 percent admissions effect bears on the 34.1 percent (one year) and 57.1 percent (two years) of the stock begun within the period. That is 4.09 percent in 2031/32 and 6.86 percent in 2032/33, giving requirements of 985, 984, 966, 926 and 919.
8. Apply the margin, the second highest placements-above-block share over 2023/24 to 2027/28 (28 of 975, 2.872 percent), and round up: 1,014, 1,013, 994, 953, 946.
9. From the care home register, block beds still registered are 1,044, 1,024, 1,024, 999 and 899 after the five deregistrations. Capacity to contract is the lower of the two: 1,014, 1,013, 994, 953, 899. 2028/29 is the peak and 2032/33 has a 47-bed gap.
10. Price each circulating figure against 919: Provider Forum 1,417 (+498), ICB 1,209 (+290), Finance 1,133 (+214), 2023 plan 1,060 (+141). Then size the settled and forecast parts: migration moves the 2032 population by 21 and the full mortality range by 257 (2.6 percent), while holding the rate moves beds by 169.
11. Write the five-row CSV and one appendix chart.

### Key traps (what the model did)

- Built the demand model correctly (946 beds) and stopped there, without capping at registered supply. Five homes (145 block beds) have given notice to deregister, so only 899 beds will exist. One run saw the 899 cap and explicitly declined to apply it. A fourth run also got the margin wrong (931).

### Justification

The population aged 85 and over rises 12.9 percent, but age-specific rates of use have fallen in every recorded year, and the two nearly cancel (986 before Home First against 1,003 today). The funded Home First programme then takes 68 placements off the 2032/33 caseload once its admissions effect is converted to a stock effect, leaving 919 and, with the 2.872 percent margin, 946 beds. The binding constraint is supply. Five homes with 145 block beds have firm deregistration dates, and the brief allows no capital programme, so 899 is the most the council can contract in 2032/33. Every circulating figure overstates need, mostly by holding or reversing the rate of use, and none counts Home First or checks whether the beds will exist.
