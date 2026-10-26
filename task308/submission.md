## Tags

**Domain:** Product analytics (churn propensity and uplift modelling).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Put the 300 e-bikes on the University network: at 2025 demand they add USD 125,000 a year in net fare revenue there.**
A ride exists only when a rider finds a bike, and University's residence-hall hubs run empty at the class changes: its stations turned away about 29,600 requests in 2025, 14.4 per cent of its demand, and with e-bikes at every station those riders ride and pay a full fare. Central, which leads on the rides its stations served (USD 50,000 on that view), adds USD 75,000, because most of its e-bike rides would only replace a classic ride.

## 2. Critical Components

1. Rebuilt from the 03:00 audit, every undock and dock and every van move, University's stations stood empty while riders came for bikes: about **29,600** requests turned away in 2025 (**14.4** per cent of its demand of about **205,100**), against about **7,400** (**2.5** per cent) on Central.
2. The Harbour pilot measures what e-bikes do where every request finds a bike: **41.7** per cent of rides at pilot stations went on an e-bike, pilot stations drew **4.4** per cent more rides than comparison stations, and an e-bike ride paid **USD 0.11** more than a classic ride.
3. Net fare revenue a year at 2025 demand: University **USD 125,000**; Central **USD 75,000**; Riverside **USD 50,000**; Hillcrest **USD 25,000**; Old Town **USD 25,000**. On the rides the stations served alone, Central would lead at **USD 50,000**.

## 3. Step-by-Step Solution

1. Put the four trip exports on one footing: tripsys_export_2025Q1.csv and tripsys_export_2025Q2.csv (old trip system: station names, bike_no, account_no, fares in USD) and rides_2025Q3.csv and rides_2025Q4.csv (new platform: station codes, vehicle_id, account_id, fares in cents), every time as Central Time, stations through station_information.json and system_regions.json; an undock of under 60 seconds that ends where it started is a false start, kept as an undock and a dock but not counted as a ride or a request.
2. Rebuilt each station's classic bikes second by second: the count in audit_0300_2025.xlsx at 03:00 each day, less each classic undock, plus each classic dock, plus and minus the classic moves in dispatch_moves_2025.csv (UTC), an undock taken before a dock in the same second.
3. For each station, month, weekday or weekend and local hour: requests per stocked second (undocks over the seconds it held a bike), times the seconds it stood empty, is the requests it turned away; summed by network.
4. The pilot, from ebike_pilot_harbour_2025.pdf's station table: the e-bike share of the rides from pilot stations, the rides a pilot station drew over the rides a comparison station drew, less 1, and the mean e-bike fare less the mean classic fare at pilot stations.
5. Each network's net fare revenue: the requests turned away plus the uplift on demand, at the network's mean classic fare, plus the e-bike share of demand grown by the uplift, at the e-bike premium; demand is the classic rides plus the requests turned away. That is what riders would pay with the e-bikes less what they paid in 2025, at 2025 demand (board_paper_2026-12_item7_extract.pdf, section 2), rounded to the nearest USD 25,000.
6. People: the accounts in account_register_2025-12-31.csv with a ride in 2025 (January to June through legacy_account_no), one person per account except that accounts on one card_fingerprint are one person where the later account was opened after the earlier account's last ride; counted by home_area with case and spaces set aside.
7. Energy: the sessions in charging_sessions_harbour_2025.csv by the local month of plug_out_utc, each session once: a session whose station, point and meter_start_wh and meter_stop_wh repeat a session received earlier is a controller re-send; energy_kwh summed.
8. Workshop: the jobs in workshop_jobs_2025.csv by the local quarter of opened_utc and asset class, leaving out a job opened on a bike with no ride since its previous job closed (the repair's road test failing), over the rides of that class in that quarter (false starts out), per 10,000 rides.

## 4. Deliverable Answers

### ebike_deployment_2027.docx

1. The network for the e-bikes: University.
2. The net fare revenue they add there a year: USD 125,000.
3. Every network's net fare revenue a year, to the nearest USD 25,000:
   - Central: USD 75,000
   - University: USD 125,000
   - Riverside: USD 50,000
   - Old Town: USD 25,000
   - Hillcrest: USD 25,000

### ebike_deployment_2027.xlsx

4. People who rode with us in 2025, by the network they live in:
   - Central: 9,486
   - University: 4,853
   - Riverside: 7,759
   - Old Town: 5,102
   - Hillcrest: 3,258
5. Energy the Harbour pilot's charging points delivered in 2025, kWh:
   - January: 212
   - February: 220
   - March: 316
   - April: 357
   - May: 401
   - June: 426
   - July: 461
   - August: 451
   - September: 398
   - October: 374
   - November: 283
   - December: 224
6. Workshop jobs per 10,000 rides in 2025:
   - E-bikes, Q1: 49.1
   - E-bikes, Q2: 31.9
   - E-bikes, Q3: 46.8
   - E-bikes, Q4: 26.0
   - Classic bikes, Q1: 12.0
   - Classic bikes, Q2: 14.3
   - Classic bikes, Q3: 15.2
   - Classic bikes, Q4: 10.2
