## Tags

**Domain:** General Statistics & Data Science (data integration: an NHS integrated care board's summer 2026 deaths by date of occurrence, integrated from the death registrations and two medical examiner offices' logs that share no key).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate Ashwold, Thornley Vale and Calderholt for the 2027 heat resilience grants; Hollinsgate, Brinmoor and Moorbridge take the standard heat-health allocation.** Ashwold's residents had 666 deaths from 1 June to 31 August 2026 against 589 expected, 13.1 per cent over, but 72 of those deaths were not on the register at the close of 9 October: the medical examiner offices referred them to the coroner, who is holding them for inquest, and the logs name each one. Completed instead with the earlier summers' share registered by 9 October (94.9 per cent), Ashwold reads 6.3 per cent and is left out.

## 2. Critical Components

1. The deaths counted are each place's residents' deaths by date of death in the window, registered or not, each once: the register's entries (version 1) plus the residents' summer deaths in the two offices' logs that no entry matches on surname, forenames, date of birth and date of death.
2. Deaths, Table 1 expected deaths and excess by place: Hollinsgate 891, 828, 7.6 per cent; Ashwold 666, 589, 13.1 per cent; Thornley Vale 345, 304, 13.5 per cent; Brinmoor 409, 383, 6.8 per cent; Calderholt 595, 528, 12.7 per cent; Moorbridge 364, 345, 5.5 per cent.
3. Deaths not yet registered at the count, found only in the logs: Hollinsgate 60, Ashwold 72, Thornley Vale 15, Brinmoor 21, Calderholt 20, Moorbridge 14 (202 in all).
4. Ellesmoor in all: 3,270 deaths, 9.8 per cent over Table 1's total.

## 3. Step-by-Step Solution

1. Read the register in both date formats, kept version 1 of each entry (district and entry number), and took residents by usual_residence_code with a date of death from 1 June to 31 August 2026.
2. Read the north log (Deceased split at its comma, Excel dates) and the south export (UTC stamps to local dates), and placed each case by its usual postcode through the lookup, terminated postcodes included; non-residents fall outside it.
3. Matched the logs' residents' summer deaths to the register on case-folded surname, forenames, date of birth and date of death, and added each unmatched death once to its place.
4. Took each place's excess over Table 1 as a percentage and designated the places at 10.0 per cent or more.
5. Counted each place's deaths by month of death for the CSV.
6. For each office and quarter of 2025-26, merged into one death any cases that share a coroner's reference or the same person, and counted each death in the quarter its scrutiny was first completed.
7. Read each 2025 register entry as it now stands (the latest version's fields, version 1's registration date), and took, by place and quarter of death, the share of residents' deaths with a medical certificate registered no more than five days after the date of death.

## 4. Deliverable Answers

### heat_resilience_grants_2027.xlsx

1. Qualifying places: Ashwold, Thornley Vale, Calderholt.
2. Scorecard (deaths, expected, excess per cent, qualifies):
   - Hollinsgate: 891, 828, 7.6, No
   - Ashwold: 666, 589, 13.1, Yes
   - Thornley Vale: 345, 304, 13.5, Yes
   - Brinmoor: 409, 383, 6.8, No
   - Calderholt: 595, 528, 12.7, Yes
   - Moorbridge: 364, 345, 5.5, No
   - Ellesmoor: 3,270 deaths, 9.8 per cent over
3. Chart: each place's excess against the 10.0 per cent line; Ashwold, Thornley Vale and Calderholt above it.
4. Deaths scrutinised by quarter of 2025-26 (April to June, July to September, October to December, January to March):
   - North Ellesmoor Medical Examiner Office: 1,924, 1,812, 2,170, 2,183 (8,089 in the year)
   - South Ellesmoor Medical Examiner Office: 1,454, 1,349, 1,713, 1,633 (6,149 in the year)
5. Residents' deaths with a medical certificate in each quarter of 2025 registered no more than five days after the date of death, per cent (January to March, April to June, July to September, October to December):
   - Hollinsgate: 59.3, 59.1, 59.8, 57.7
   - Ashwold: 62.0, 62.5, 64.4, 60.0
   - Thornley Vale: 63.9, 63.1, 63.8, 62.0
   - Brinmoor: 60.4, 59.9, 59.4, 64.8
   - Calderholt: 61.7, 63.6, 57.5, 61.1
   - Moorbridge: 61.7, 60.9, 59.9, 65.5

### summer_2026_deaths_by_place.csv

1. Deaths by month of death (June, July, August 2026):
   - Hollinsgate: 297, 327, 267
   - Ashwold: 168, 301, 197
   - Thornley Vale: 101, 130, 114
   - Brinmoor: 117, 155, 137
   - Calderholt: 185, 237, 173
   - Moorbridge: 110, 147, 107
