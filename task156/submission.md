## Tags

**Domain:** Physical and environmental sciences (hydrology and flood frequency).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Hold the Ngaio Road connection until the PS03 storage upgrade is commissioned: replayed through 2004 to 2023 each day as it occurred, PS03 overflows about 3 times a year with the subdivision, above the consent's limit of 2.**
Not the station's own record of 2 overflows since 2024, nor one response per millimetre fitted on the meter (about 1 a year): both carry the meter's low water table into years when it stood far higher. After the upgrade the station overflows about 1 a year with the subdivision.

## 2. Critical Components

1. PS03's dry weather infiltration rises by **4.2 L/s** for each kilometre of its sewer below the water table.
2. The median day had **0.2 km** of sewer below the water table in 2024 to 2026 against **2.1 km** in 2004 to 2023, with about **21 km** at the wettest in both.
3. The station overflows about **3** times a year as connected now, **3** with Ngaio Road and **1** with Ngaio Road after the upgrade.
4. Held out of each fit, the June 2025 high-river weeks are missed by **43 L/s** on average by one response per millimetre and by **0.2 L/s** by the conditioned model.

## 3. Step-by-Step Solution

1. Averaged the SCADA export's good 15-minute inflow into UTC hours, setting aside hours with the wet well at the weir crest, beside the climate station's hourly rain (archive NZST hour ending, 2026 provisional 15-minute UTC).
2. Turned bore 72_1043's depth below its measuring point into the water level and, against the asset register's PS03 in-service mains, into each day's kilometres of sewer below it: medians 0.2 km (2024 to 2026) and 2.1 km (2004 to 2023).
3. Fitted the dry hours (no rain in the previous 72 hours) as a weekly domestic pattern plus 4.2 L/s per km below the water table, then the rest as a fast rain response (30 m3 per mm) and a slow one scaled by those kilometres (6.0 m3 per mm per km).
4. Refitted both models without the June 2025 high-river weeks and scored them there and on 2026: mean errors 0.2 and 0.0 L/s for the conditioned model, 43 and 1.1 L/s for one response per millimetre.
5. Ran the model through every hour of 2004 to 2023, each day with its own water table, at the data sheet's 112.0 L/s and 350 m3, counting overflows under consent condition 3: 58 in 20 years as connected now, 64 with the subdivision's 260 dwellings at the code of practice's 2.7 persons, 200 litres and Table 5.2, 15 after adding the upgrade's 1,100 m3.
6. Water use per dwelling per the billing policy's section 4, each rating unit's dwellings dated by the building consents' code compliance certificates rather than carried back from the 31 October 2026 rating snapshot.
7. Other stations from the monitors' own NZST message times, each serial placed by the monitor installation history, an overflow emergency where it began inside an outage at any ICP the council's electricity site list gives the station's address.
8. With the subdivision the replay averages 3.20 overflows a year against condition 6's limit of 2, so condition 8 bars the connection until the upgrade, which brings it to about 1.

## 4. Deliverable Answers

### ps03_ngaio_road_connection_2027.xlsx

1. Average wet weather overflows a year over the consent's 2004 to 2023 replay, whole numbers:
   - Without the subdivision: 3
   - With the subdivision: 3
   - With the subdivision after the upgrade: 1
2. Residential water use per dwelling per day, litres:
   - 2024 Q1: 448
   - 2024 Q2: 381
   - 2024 Q3: 340
   - 2024 Q4: 414
   - 2025 Q1: 456
   - 2025 Q2: 394
   - 2025 Q3: 315
   - 2025 Q4: 419
   - 2026 Q1: 477
   - 2026 Q2: 374
   - 2026 Q3: 313
3. Other stations' wet weather overflows and spill hours (whole hours):
   - PS01 2024: 3 overflows, 9 spill hours
   - PS01 2025: 2 overflows, 7 spill hours
   - PS02 2024: 6 overflows, 16 spill hours
   - PS02 2025: 5 overflows, 16 spill hours
   - PS04 2024: 2 overflows, 6 spill hours
   - PS04 2025: 2 overflows, 6 spill hours
   - PS05 2024: 4 overflows, 11 spill hours
   - PS05 2025: 5 overflows, 13 spill hours
   - PS06 2024: 1 overflows, 2 spill hours
   - PS06 2025: 2 overflows, 6 spill hours
4. Network emergency overflows: 2024: 3; 2025: 3

### council_report_ngaio_road_2027.docx

1. Recommends deferring the Ngaio Road connection until the PS03 storage upgrade is commissioned, with the three replay figures (about 3, 3 and 1 a year) and the chart.

### replay_overflows_2004-2023.png

1. Bars for each year 2004 to 2023, PS03 as connected now and with Ngaio Road, the consent limit of 2 drawn across, titled with the 3.2 a year the subdivision brings.
