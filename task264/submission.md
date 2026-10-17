## Tags

**Domain:** Survey Research & Official Statistics, sample design, allocation and weighting (how a regional park authority's 2027-28 levy is shared among its nine member councils by each council's adult residents who visited the parks in 2025-26, estimated from an exit survey that samples visits, so each adult's chance of interview rises with how often they come).
**Analytical objective:** Descriptive & Distribution Analysis (how the adults who visited the Authority's parks in 2025-26, each counted once, are distributed across the nine member councils, and the levy that follows).

## 1. Final Recommendation

**Charge the 2027-28 levy of £7,416,300 as follows: Keldmere District Council £1,250,310, Ravenwick Borough Council £1,525,314, Snelgarth District Council £977,169, Larkstead Borough Council £717,236, Grinbury District Council £743,901, Hornmere District Council £650,135, Chaldale District Council £549,836, Wendstow District Council £513,321 and Ferncote Borough Council £489,078.**
Keldmere, Ravenwick and Snelgarth's residents are 50.6 per cent of the nine councils' adult residents who visited in 2025-26, so those three pay 50.6 per cent of the levy. Not 24.9 per cent, which dividing each council's expanded visits by its respondents' average visit count, weighted by their expansion weights, gives, because in an exit survey that average is weighted towards the people who come most and overstates how often the valley councils' residents come. Not 85.1 per cent, from the expanded visits themselves, which counts visits rather than residents. Not 53.4 per cent, from each interview's inverse visit count without its weight, because the survey interviewed a different share of the visits in each park, season and day type.

## 2. Critical Components

1. Interviews with residents of the nine member councils, the sample each council's estimate is built from: **3,973** of **4,470**
2. Keldmere, Ravenwick and Snelgarth's share of the nine councils' adult residents who visited, each counted once: **50.6 per cent**, so their levies total **£3,752,793**

## 3. Step-by-Step Solution

1. Stacked dvrpa_visitor_survey_2025-26_wave1.xlsx and dvrpa_visitor_survey_2025-26_wave2.csv (4,470 interviews) and joined each interview's expansion weight from survey_weights_2025-26.csv by wave and serial.
2. Kept the 3,973 interviews whose coded home area is one of the nine member councils; visitors from outside them and homes that could not be placed are not counted (resolution 14/2026, paragraphs 4 and 6, in levy_papers_2027-28.pdf).
3. Counted each interview as its expansion weight divided by the respondent's visits in the last 12 months including that day (Q9), since the interviewer approached every eighth adult leaving (fieldwork_and_weighting_note_2025-26.pdf) and each adult's chance of interview is in proportion to their visits; summed by council, the three valley councils hold 50.6 per cent of the nine councils' residents who visited.
4. Shared the £7,416,300 levy requirement (the budget table in levy_papers_2027-28.pdf) in proportion to each council's unrounded estimate and rounded each levy to the pound (paragraph 5).
5. Parking income: each machine's ticket counted once in pay_machine_transactions_2025-26.csv, placed at the park whose charges in car_park_tariffs_2025-26.xlsx its takings match (PM-2103's takings are at Gorthfield's charges until 31 August 2025, though the register now has it at the Water Park), divided by 1.2, plus the parking income in parking_app_statements_2025-26.xlsx as stated (sessions times charge over 1.2 on every line, so already net of VAT): £1,832,957 in all.
6. Levy collection: receipts in bank_receipts_2025-26.csv quoting the invoices in levy_invoices_2025-26.csv, taken by value date to 31 March 2026, with the shared finance service's transfers split by remittance_advices_2025-26.csv: every council had paid in full except Chaldale, which owed £3,455.
7. Vehicles: entries in car_park_counts_hourly_2025-26.csv over the survey year, with counter C-09's counts halved (from 18 August 2025 its counts per paying vehicle run at twice C-04's, so it counts vehicles in and out), the hours C-05 and C-10 report the same count at Gorthfield's lakeside entrance counted once, and C-07 placed at Thruscote Hall until 14 October 2025 (its counts follow Thruscote's payments until C-11 is installed there): 598,533 vehicles.
8. The 2027-28 levy is charged in proportion to each council's residents who visited, Ravenwick the largest at £1,525,314 and Ferncote the smallest at £489,078.

## 4. Deliverable Answers

### levy_apportionment_2027-28.xlsx

1. Each member council's 2027-28 levy and the adult residents who visited in 2025-26 that its share rests on (to the nearest hundred):
   - Keldmere District Council: £1,250,310, 45,800 residents
   - Ravenwick Borough Council: £1,525,314, 55,900 residents
   - Snelgarth District Council: £977,169, 35,800 residents
   - Larkstead Borough Council: £717,236, 26,300 residents
   - Grinbury District Council: £743,901, 27,300 residents
   - Hornmere District Council: £650,135, 23,800 residents
   - Chaldale District Council: £549,836, 20,200 residents
   - Wendstow District Council: £513,321, 18,800 residents
   - Ferncote Borough Council: £489,078, 17,900 residents
2. Total: £7,416,300
3. What parkers paid at each charging park's car parks for 2025-26 parking through the pay machines and the parking app, net of VAT:
   - Gorthfield Country Park: £439,313
   - Daskbeck Water Park: £543,124
   - Lockshaw Moor: £449,759
   - Thruscote Hall: £400,761
4. Vehicles that entered each charging park's car parks in 2025-26:
   - Gorthfield Country Park: 171,505
   - Daskbeck Water Park: 134,156
   - Lockshaw Moor: 166,487
   - Thruscote Hall: 126,385
5. Each member council's payments toward its 2025-26 levy by 31 March 2026 and what it still owed that day:
   - Keldmere District Council: paid £664,285, owed £0
   - Ravenwick Borough Council: paid £890,351, owed £0
   - Snelgarth District Council: paid £566,832, owed £0
   - Larkstead Borough Council: paid £1,097,888, owed £0
   - Grinbury District Council: paid £763,277, owed £0
   - Hornmere District Council: paid £964,788, owed £0
   - Chaldale District Council: paid £510,932, owed £3,455
   - Wendstow District Council: paid £821,365, owed £0
   - Ferncote Borough Council: paid £699,227, owed £0

### levy_report_2027-28.docx

1. The report to members recommending the levy schedule above, explaining that each interview is counted as its weight over its own visit count, with a bar chart of each council's share of the 2027-28 levy beside its 2026-27 share on population, and tables of the parking income, vehicles and 2025-26 collection figures above.
