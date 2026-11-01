## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment: a state household survey's multiple-jobholding rate by workforce area, on the respondent's own reporting basis when another household member answers for adults who are out at the interview).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Certify Northern Basin, Silver Creek, Upper River and Eastern Prairie for the 2027 portable benefits pilot; Capital Region, High Plains, Southwest Lakes and Timber Country do not qualify.** Counted as residents would report it themselves, 7% of the state's employed residents held more than one job over 2025Q4 to 2026Q3, against 5.5% as collected. Not the as-collected shares, the self-answered shares or shares imputed from self-answering residents alike in age, sex, hours and occupation, which all leave Silver Creek alone at 7.0% or more: the residents answered for hold second jobs more often, and the answers given for them carry only 56% of the second jobs those same residents report in the quarters they answer for themselves. Not carrying each resident's own answer from another quarter, which adds Upper River but leaves Northern Basin and Eastern Prairie below 7.0% because about half of the answered-for residents never answer for themselves.

## 2. Critical Components

1. Answered-for reports carry **56%** of the second jobs the same adults report themselves: in adjacent quarters where an employed adult answered for themselves in one and was answered for in the other (either order), the answered-for report carries the self-reported second job 54.4% of the time, divided by the 97% of self-reported second jobs still self-reported in the adjacent quarter.
2. Under every proxy sensitivity from 53% to 59% (the 95% interval of the within-person estimate), Northern Basin, Silver Creek, Upper River and Eastern Prairie each clear 7.0% on the residents' own reporting basis and Capital Region, High Plains, Southwest Lakes and Timber Country each stay below it.
3. Statewide share on the same basis **7%** (as collected 5.5%).

## 3. Step-by-Step Solution

1. Kept employed residents (LFSTAT 1 or 2) in HES_PERSON_2025Q1_2026Q3.csv for 2025Q4 to 2026Q3 and joined each to its FWGT in HES_FINAL_WEIGHTS_2025Q4_2026Q3.xlsx by quarter, CASEID and LINENO, using the 2026Q3 rev sheet that HES_TECHNICAL_NOTE_2026-09.pdf says replaces the first issue; a record is the resident's own answer when RESPLINE equals LINENO.
2. Followed each adult across quarters by case and line number, carrying the CAPI 2026 case numbers back through HES_CASEID_CROSSWALK_CAPI2026.csv and breaking the chain where sex changes or age moves by other than 0 or 1 (a new household reuses line numbers).
3. Among adults employed in two adjacent quarters who answered for themselves in one and were answered for in the other (either order), the answered-for report carried the second job the adult reported themselves 54.4% of the time; dividing by the 97% of self-reported second jobs still self-reported in the adjacent quarter gives 56%, and second jobs reported for adults who report none themselves, net of new second jobs, run at 0.2%.
4. In each area, corrected the weighted share of answered-for residents reported with a second job as (reported share minus 0.2%) divided by (56% minus 0.2%), kept every self-answered record as given and combined both on the final weights: Northern Basin 7.8, Silver Creek 9.3, Upper River 8.3, Eastern Prairie 8.0; Capital Region 5.8, High Plains 4.4, Southwest Lakes 5.6, Timber Country 6.5.
5. Applied the same correction statewide: 7% against 5.5% as collected.
6. For the survey quality sheet, counted each housing unit once per quarter by FRAMEID in HES_HOUSEHOLD_DISPOSITIONS_2025Q1_2026Q3.csv (an interview code in any of its rows makes it interviewed, which covers converted refusals and the old system's second record of some 2026Q2 interviews), placed it by CTY with county 59041 split by ZIP (TDLI_WORKFORCE_AREAS_2026.xlsx), and took as not eligible the units coded vacant, demolished or not a housing unit plus, per the response-rate definitions in HES_TECHNICAL_NOTE_2026-09.pdf, the units the master address file as finally corrected shows removed as vacant or demolished on or before the visit date, replaying HES_FRAME_MAINTENANCE_2024-07_2026-09.csv in date order with each RESTORE (DELETED IN ERROR) cancelling the removal it follows from that removal's date; response rate is interviewed over eligible, noncontact rate is eligible units coded no one home (3 or 216) over eligible.
7. Recommended certifying Northern Basin, Silver Creek, Upper River and Eastern Prairie, the areas at or above 7.0%.

## 4. Deliverable Answers

### pba_pilot_areas_2027.xlsx

1. Qualify for the 2027 pilot: Northern Basin, Silver Creek, Upper River and Eastern Prairie.
2. Do not qualify: Capital Region, High Plains, Southwest Lakes and Timber Country.
3. Statewide share of employed residents holding more than one job on the rule's basis: 7%.
4. Household response rate by workforce area, 2025Q4 to 2026Q3, percent to one decimal:
   - Capital Region: 76.6
   - Northern Basin: 67.5
   - Silver Creek: 76.1
   - High Plains: 74.3
   - Upper River: 74.7
   - Southwest Lakes: 69.7
   - Eastern Prairie: 68.8
   - Timber Country: 83.8
5. Noncontact rate by workforce area, 2025Q4 to 2026Q3, percent to one decimal:
   - Capital Region: 11.9
   - Northern Basin: 19.5
   - Silver Creek: 11.7
   - High Plains: 13.2
   - Upper River: 13.4
   - Southwest Lakes: 16.6
   - Eastern Prairie: 17.8
   - Timber Country: 5.8

### pba_pilot_certification_2027.docx

6. Memo to the commissioner recommending Northern Basin, Silver Creek, Upper River and Eastern Prairie, with a bar chart of every area's share against the 7 percent line on page 1, qualifying areas in dark bars.
