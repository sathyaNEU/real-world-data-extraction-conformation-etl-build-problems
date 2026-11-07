## Tags

- **Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (ambient gamma dose-rate monitoring network, natural against artificial increases).
- **Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Yes: notify increases of artificial origin at MV334 Headland Lookout on 6 days (08/07/2026, 17/07/2026, 20/07/2026, 22/07/2026, 07/08/2026, 13/08/2026), highest ten-minute value 155 nSv/h, and at MV129 Old Brickworks on 5 days (24/08/2026, 28/08/2026, 13/09/2026, 14/09/2026, 17/09/2026), highest 164 nSv/h.** No other station recorded one; clearing increases on rain at the nearest gauge would notify many more stations and clear five of these days.

## 2. Critical Components

1. A natural excess (rain-washed radon progeny) never fell by more than **41 per cent** in one ten-minute step anywhere in the quarter.
2. Each of the **11** detection days ended with the excess falling by **85 per cent or more** in one step and staying down.
3. On **5** of those days the nearest rain gauge recorded rain within an hour of the increase, so rain coincidence does not decide origin.

## 3. Step-by-Step Solution

1. Read `mvgn_dose_rate_10min_2026Q3.csv`, exact duplicate rows once, microsieverts converted, T and F records set aside.
2. Took each station's excess over its centred 48-hour running median of valid values.
3. Flagged every step where an excess of 30 nSv/h or more fell by more than half and the next value stayed below half of it; none occurs outside MV334 and MV129 (natural falls stop at 41 per cent).
4. Walked back from each flagged step over values more than 15 nSv/h above the median; dated each increase by its start and took its highest ten-minute value.
5. Source checks: each kit's source is the kit register's, except while `sealed_source_register_2026.csv` has it out: CS-0583 went out 5 August and back into KIT-2 4 September, so KIT-2 carried the spare CS-0417 (21 August stock check); certificate in force by date of issue, jig, Cs-137 decay; repeat is the check.
6. Telemetry: earliest receipt per interval from `platform_ingest_log_2026Q3.csv`, LoRa receipts read as UK clock time and all others as UTC (OP-04 section 2), against the interval's end; test-mode (T) values count (the agreement's timeliness clause); an F record carries no value, so it is not a received value (OP-04 section 2); over the quarter's 13,248 intervals.
7. Air filters: air drawn is `measured_flow_m3_h` in `air_pump_controller_log_2026Q3.csv` integrated from filter on to off, the transmitter's blank RUN rows filled by linear interpolation (the set-flow totaliser and AS2's set-flow volume do not measure it); latest result version.
8. Notified MV334 and MV129 with their dates and highest values.

## 4. Deliverable Answers

### artificial_detections_2026Q3.docx

1. MV334 Headland Lookout: 08/07/2026, 17/07/2026, 20/07/2026, 22/07/2026, 07/08/2026, 13/08/2026; highest ten-minute value 155 nSv/h (13/08/2026).
2. MV129 Old Brickworks: 24/08/2026, 28/08/2026, 13/09/2026, 14/09/2026, 17/09/2026; highest ten-minute value 164 nSv/h (24/08/2026).
3. No other station recorded an increase of artificial origin.

### network_quarter_2026Q3.xlsx

1. Source checks, per cent of expected and result:
   - MV103 (20/07/2026): 97.6, Pass
   - MV112 (17/09/2026): 100.7, Pass
   - MV118 (21/08/2026): 99.3, Pass
   - MV129 (17/07/2026): 97.5, Pass
   - MV135 (24/08/2026): 97.9, Pass
   - MV142 (22/09/2026): 101.6, Pass
   - MV149 (17/09/2026): 101.2, Pass
   - MV157 (11/08/2026): 99.4, Pass
   - MV158 (02/09/2026): 102.6, Pass
   - MV166 (06/08/2026): 96.8, Pass
   - MV171 (08/09/2026): 98.4, Pass
   - MV176 (07/07/2026): 103.4, Pass
   - MV184 (11/09/2026): 112.6, Fail
   - MV192 (01/09/2026): 95.8, Pass
   - MV207 (31/08/2026): 103.4, Pass
   - MV214 (16/07/2026): 106.2, Pass
   - MV226 (10/09/2026): 99.1, Pass
   - MV231 (03/08/2026): 99.8, Pass
   - MV243 (24/07/2026): 89.5, Fail
   - MV305 (08/07/2026): 104.2, Pass
   - MV311 (21/09/2026): 96.6, Pass
   - MV318 (04/08/2026): 101.6, Pass
   - MV327 (27/08/2026): 99.9, Pass
   - MV334 (03/09/2026): 102.8, Pass
2. Telemetry, per cent of the quarter's intervals received within 60 minutes:
   - MV103 98.6; MV112 99.4; MV118 99.0; MV129 99.8; MV135 96.9; MV142 97.8; MV149 97.7; MV157 99.9; MV158 98.4; MV166 99.0; MV171 99.8; MV176 95.9; MV184 99.4; MV192 99.9; MV207 98.7; MV214 96.8; MV226 99.9; MV231 99.7; MV243 99.5; MV305 99.1; MV311 98.6; MV318 100.0; MV327 98.9; MV334 100.0
3. Gross beta, mBq/m3 by filter:
   - AS1: AF1-26-027 0.64; AF1-26-028 0.35; AF1-26-029 0.70; AF1-26-030 0.59; AF1-26-031 0.52; AF1-26-032 0.54; AF1-26-033 0.48; AF1-26-034 0.37; AF1-26-035 0.37; AF1-26-036 0.95; AF1-26-037 0.64; AF1-26-038 0.55; AF1-26-039 1.04
   - AS2: AF2-26-027 0.62; AF2-26-028 0.66; AF2-26-029 0.52; AF2-26-030 0.50; AF2-26-031 0.44; AF2-26-032 0.47; AF2-26-033 0.67; AF2-26-034 0.57; AF2-26-035 0.41; AF2-26-036 0.54; AF2-26-037 0.54; AF2-26-038 0.45; AF2-26-039 0.54
   - AS3: AF3-26-027 0.43; AF3-26-028 0.52; AF3-26-029 0.46; AF3-26-030 0.35; AF3-26-031 0.25; AF3-26-032 0.33; AF3-26-033 0.25; AF3-26-034 0.61; AF3-26-035 0.29; AF3-26-036 0.51; AF3-26-037 0.33; AF3-26-038 0.54; AF3-26-039 0.46

### excursion_traces_2026Q3.svg

1. One panel per detection day (11), the ten-minute record from two hours before to two hours after, the step that ended each increase marked; titled with the 85 and 41 per cent falls.
