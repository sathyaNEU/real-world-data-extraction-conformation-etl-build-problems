## Tags

**Domain:** Survey Research & Official Statistics, sample design, allocation and weighting (how a regional park authority's 2027-28 levy is shared among its nine member councils by each council's adult residents who visited the parks in 2025-26, estimated from an exit survey that samples visits, so each adult's chance of interview rises with how often they come).
**Analytical objective:** Descriptive & Distribution Analysis (how the adults who visited the Authority's parks in 2025-26, each counted once, are distributed across the nine member councils, and the levy that follows).

## 1. Final Recommendation

**Charge the 2027-28 levy of £7,416,300 as follows: Keldmere District Council £1,252,070, Ravenwick Borough Council £1,540,108, Snelgarth District Council £968,963, Larkstead Borough Council £716,993, Grinbury District Council £741,438, Hornmere District Council £675,709, Chaldale District Council £547,403, Wendstow District Council £492,870 and Ferncote Borough Council £480,746.**
Keldmere, Ravenwick and Snelgarth's residents are 50.7 per cent of the nine councils' adult residents who visited in 2025-26, so those three pay 50.7 per cent of the levy. Not 25.0 per cent, which dividing each council's expanded visits by its respondents' average visit count, weighted by their expansion weights, gives, because in an exit survey that average is weighted towards the people who come most and overstates how often the valley councils' residents come. Not 55.5 per cent, from each interview's weight over its visits to the park where it was interviewed alone, which counts a resident who visits two parks once at each, though the survey could meet them leaving either. Not 85.1 per cent, from the expanded visits themselves, which counts visits rather than residents. Not 53.4 per cent, from each interview's inverse visit count without its weight, because the survey interviewed a different share of the visits in each park, season and day type.

## 2. Critical Components

1. Interviews with residents of the nine member councils, the sample each council's estimate is built from: **3,973** of **4,470**
2. Keldmere, Ravenwick and Snelgarth's share of the nine councils' adult residents who visited, each counted once: **50.7 per cent**, so their levies total **£3,761,141**

## 3. Step-by-Step Solution

1. Stacked dvrpa_visitor_survey_2025-26_wave1.xlsx and dvrpa_visitor_survey_2025-26_wave2.csv (4,470 interviews) and joined each interview's expansion weight from survey_weights_2025-26.csv by wave and serial.
2. Kept the 3,973 interviews whose coded home area is one of the nine member councils; visitors from outside them and homes that could not be placed are not counted (resolution 14/2026, paragraphs 4 and 6, in levy_papers_2027-28.pdf).
3. Counted each interview as its expansion weight divided by the respondent's visits to the six parks in the last 12 months including that day (Q9, the six parks' answers added), since the interviewer approached every eighth adult leaving each park (fieldwork_and_weighting_note_2025-26.pdf) and each adult's chance of interview is in proportion to their visits to all six; summed by council, the three valley councils hold 50.7 per cent of the nine councils' residents who visited.
4. Shared the £7,416,300 levy requirement (the budget table in levy_papers_2027-28.pdf) in proportion to each council's unrounded estimate and rounded each levy to the pound (paragraph 5).
5. Parking income: each machine's ticket counted once in pay_machine_transactions_2025-26.csv, placed at the park whose charges in car_park_tariffs_2025-26.xlsx its takings match (PM-2103's takings are at Gorthfield's charges until 31 August 2025, though the register now has it at the Water Park), divided by 1.2, plus the parking income in parking_app_statements_2025-26.xlsx as stated (sessions times charge over 1.2 on every line, so already net of VAT): £1,832,957 in all.
6. Levy collection: each receipt in cash_book_receipts_2025-26.csv counted once against the invoices it is allocated to in member_council_invoices_2025-26.csv (where a payment run paid a sundry invoice with an instalment, the receipt's amount stands on both lines and the instalment takes its own amount), dated by the day the bank credited it in bank_credits_main_account_2025-26.csv (matched on the reference and amount; the cash book posts a day later), and the 31 March credits, posted after the cash book's year, taken from the bank's report against each payer's open invoices; on time when credited on or before the invoice's due date and late when after it but by 31 March 2026: seven councils paid at least one instalment late.
7. Vehicles: entries in car_park_counts_hourly_2025-26.csv over the survey year, with counter C-09's counts halved (from 18 August 2025 its counts per paying vehicle run at twice C-04's, so it counts vehicles in and out), the hours C-05 and C-10 report the same count at Gorthfield's lakeside entrance counted once, and C-07 placed at Thruscote Hall until 14 October 2025 (its counts follow Thruscote's payments until C-11 is installed there): 598,533 vehicles.
8. The 2027-28 levy is charged in proportion to each council's residents who visited, Ravenwick the largest at £1,540,108 and Ferncote the smallest at £480,746.

## 4. Deliverable Answers

### levy_apportionment_2027-28.xlsx

1. Each member council's 2027-28 levy and the adult residents who visited in 2025-26 that its share rests on (to the nearest hundred):
   - Keldmere District Council: £1,252,070, 45,500 residents
   - Ravenwick Borough Council: £1,540,108, 55,900 residents
   - Snelgarth District Council: £968,963, 35,200 residents
   - Larkstead Borough Council: £716,993, 26,000 residents
   - Grinbury District Council: £741,438, 26,900 residents
   - Hornmere District Council: £675,709, 24,500 residents
   - Chaldale District Council: £547,403, 19,900 residents
   - Wendstow District Council: £492,870, 17,900 residents
   - Ferncote Borough Council: £480,746, 17,500 residents
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
5. Each member council's 2025-26 levy paid by each instalment's due date and paid after the due date but by 31 March 2026:
   - Keldmere District Council: on time £498,214, late £166,071
   - Ravenwick Borough Council: on time £667,764, late £222,587
   - Snelgarth District Council: on time £566,832, late £0
   - Larkstead Borough Council: on time £1,097,888, late £0
   - Grinbury District Council: on time £190,819, late £381,638
   - Hornmere District Council: on time £723,591, late £241,197
   - Chaldale District Council: on time £382,336, late £128,596
   - Wendstow District Council: on time £616,024, late £205,341
   - Ferncote Borough Council: on time £524,421, late £174,806

### levy_report_2027-28.docx

1. The report to members recommending the levy schedule above, explaining that each interview is counted as its weight over its visits to the six parks, with a bar chart of each council's share of the 2027-28 levy beside its 2026-27 share on population, and tables of the parking income, vehicles and the 2025-26 levy paid on time and late above.
