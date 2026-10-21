## Tags

**Domain:** Criminology and justice (crime incidence and hotspot analysis).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Commission Thursday 20:00 to 00:00, Saturday 00:00 to 04:00, Sunday 00:00 to 04:00, Sunday 20:00 to 00:00, Friday 12:00 to 16:00, Wednesday 20:00 to 00:00, Monday 20:00 to 00:00 and Tuesday 20:00 to 00:00, which together meet 5,700 of the offences the tasking contract covers in a season.**
The ninth slot by weight, Friday 16:00 to 20:00, carries 400 against the 500 of the weakest of the eight. Not the slate a flat reading of each occurrence window gives, which puts the patrol on Friday 12:00 to 16:00 and the afternoons and whose eight meet 4,250. Not the slate from the earliest time each offence can have happened: 2,700. Not the slate from the time each offence was found: 1,400. Not the slate from each window's midpoint: 3,150.

## 2. Critical Components

1. The contract covers **12,510** recorded offences a season in the quarter
2. The share of those offences whose record gives an occurrence window rather than a time is **80.1 per cent**
3. The share whose window runs longer than one patrol slot is **79.6 per cent**
4. The heaviest slot of the week meets **1,100** offences a season, and the lightest **50**
5. The eight commissioned slots meet **5,700** a season

## 3. Step-by-Step Solution

1. Took the offence classes the tasking contract covers from Annex B of harbourgate_patrol_tasking_contract_2027.pdf and the quarter's five locations from harbourgate_location_register.csv: five classes at five registered locations.
2. Kept the rows of kcp_rms_offence_extract_2027-01-22.csv in those classes whose location code is one of the register's five: 25,020 recorded offences over the two seasons, 12,510 a season.
3. Read occurred_from and occurred_to as kcp_rms_data_dictionary.csv defines them, the earliest and the latest time the offence can have occurred: 80.1 per cent of these offences carry a window rather than a time, and 79.6 per cent of them a window longer than a patrol slot, so no slot's count is in the record.
4. Laid the week's 42 four-hour slots down from harbourgate_tasking_schedule.csv and took the hour-of-week shares under which the windows the force recorded are the likeliest set of windows to have been recorded, iterating the shares against the record until they stopped moving, since the agreement builds the count from the force's record of those offences and from nothing else, and makes the time that governs the time the offence occurred.
5. Summed those shares by slot over both seasons and divided by two, as the question asks: the week's grid, from 1,100 a season in the heaviest slot to 50 in the lightest.
6. Took the eight heaviest slots, the number harbourgate_patrol_tasking_contract_2027.pdf buys: Thursday 20:00 to 00:00, Saturday 00:00 to 04:00, Sunday 00:00 to 04:00, Sunday 20:00 to 00:00, Friday 12:00 to 16:00, Wednesday 20:00 to 00:00, Monday 20:00 to 00:00 and Tuesday 20:00 to 00:00, meeting 5,700 a season, with Friday 16:00 to 20:00 ninth at 400.
7. Commissioned those eight slots for the 2027 season.

## 4. Deliverable Answers

### harbourgate_patrol_slate_2027.pdf

1. The eight slots to commission in the 2027 season, with the offences each meets a season, to the nearest fifty:
   - Thursday 20:00 to 00:00: 1,100
   - Saturday 00:00 to 04:00: 900
   - Sunday 00:00 to 04:00: 850
   - Sunday 20:00 to 00:00: 800
   - Friday 12:00 to 16:00: 550
   - Wednesday 20:00 to 00:00: 500
   - Monday 20:00 to 00:00: 500
   - Tuesday 20:00 to 00:00: 500
2. The eight together meet 5,700 offences a season.
3. Heatmap of the week on page 1, seven days across by six four-hour bands down, each cell labelled with the offences that slot meets a season and the eight commissioned cells outlined.

### harbourgate_slot_weights.xlsx

1. The offences each of the week's 42 slots meets a season, to the nearest fifty, in the order Monday first:
   - Monday: 00:00 to 04:00 50, 04:00 to 08:00 100, 08:00 to 12:00 150, 12:00 to 16:00 300, 16:00 to 20:00 300, 20:00 to 00:00 500
   - Tuesday: 00:00 to 04:00 200, 04:00 to 08:00 50, 08:00 to 12:00 150, 12:00 to 16:00 350, 16:00 to 20:00 300, 20:00 to 00:00 500
   - Wednesday: 00:00 to 04:00 100, 04:00 to 08:00 100, 08:00 to 12:00 150, 12:00 to 16:00 350, 16:00 to 20:00 250, 20:00 to 00:00 500
   - Thursday: 00:00 to 04:00 200, 04:00 to 08:00 50, 08:00 to 12:00 150, 12:00 to 16:00 350, 16:00 to 20:00 300, 20:00 to 00:00 1,100
   - Friday: 00:00 to 04:00 50, 04:00 to 08:00 100, 08:00 to 12:00 200, 12:00 to 16:00 550, 16:00 to 20:00 400, 20:00 to 00:00 100
   - Saturday: 00:00 to 04:00 900, 04:00 to 08:00 200, 08:00 to 12:00 150, 12:00 to 16:00 350, 16:00 to 20:00 300, 20:00 to 00:00 150
   - Sunday: 00:00 to 04:00 850, 04:00 to 08:00 150, 08:00 to 12:00 150, 12:00 to 16:00 300, 16:00 to 20:00 250, 20:00 to 00:00 800
2. The quarter's recorded offences of each class in the extract, each season, to the nearest ten:
   - Theft from a motor vehicle 2025: 2,520
   - Theft from a motor vehicle 2026: 2,680
   - Theft of a pedal cycle 2025: 2,040
   - Theft of a pedal cycle 2026: 2,160
   - Criminal damage 2025: 3,690
   - Criminal damage 2026: 3,910
   - Burglary business 2025: 2,580
   - Burglary business 2026: 2,740
   - Burglary residential 2025: 1,310
   - Burglary residential 2026: 1,390
   - Theft from the person 2025: 760
   - Theft from the person 2026: 800
   - Assault without injury 2025: 1,150
   - Assault without injury 2026: 1,220
   - Public order 2025: 1,420
   - Public order 2026: 1,510
   - Shoplifting 2025: 2,170
   - Shoplifting 2026: 2,310
3. The share of all the quarter's recorded offences at each of its five locations, each season, to one decimal place:
   - Harbourgate Street 2025: 35.8 per cent
   - Harbourgate Street 2026: 35.7 per cent
   - Quayside Multi-Storey 2025: 13.8 per cent
   - Quayside Multi-Storey 2026: 13.8 per cent
   - Lamphouse Lane 2025: 19.3 per cent
   - Lamphouse Lane 2026: 19.8 per cent
   - Fishmarket Square 2025: 21.2 per cent
   - Fishmarket Square 2026: 21.1 per cent
   - Netherbow Car Park 2025: 9.9 per cent
   - Netherbow Car Park 2026: 9.6 per cent
4. The footfall each sensor's location saw per trading hour, each season, to the nearest ten:
   - FG-01 2025: 1,320
   - FG-01 2026: 1,380
   - FG-02 2025: 860
   - FG-02 2026: 900
   - FG-04 2025: 600
   - FG-04 2026: 620
   - FG-07 2025: 480
   - FG-07 2026: 500
