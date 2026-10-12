# task229: Thornacre peak gate 2026

## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Hinckley, Daventry, Bellshill, Magor, Warrington and Avonmouth meet Thornacre's peak stock-record standard and run replenishment unattended through the freeze; Thurrock and Doncaster stay on supervised replenishment.**

Thurrock and Doncaster both estimate at 96% against the 97.0% line at 06:00 on 7 December 2026. Not the share of count tasks that matched, which reads each record before the count corrected it and passes no centre. Not the routine counts weighted to the A, B and C mix, which measures records at the end of their cycle rather than at the stand-down and passes only Magor and Hinckley.

## 2. Critical Components

1. In-scope faces at 06:00 on 7 December under SCS-07 4.1: **26,188**
2. A count posts the confirmed quantity as the record, so each face's state at 06:00 runs from its own last count of any kind
3. The per-day chance of a record going wrong is fitted by class from the CYC counts, each measured from the face's previous count of any kind; exception counts (SHP, NEG, EMP, OVR) reset faces but are not fitted
4. Record accuracy at the stand-down: Hinckley 99%, Daventry 98%, Bellshill 98%, Thurrock 96%, Magor 99%, Warrington 98%, Avonmouth 98%, Doncaster 96%

## 3. Step-by-Step Solution

1. Took the SCS-07 4.1 faces from wms_location_master_THN_eff.csv (PICK, client THN, a Thornacre line, ACTIVE on 2026-12-07): 26,188 faces.
2. Joined THN_pickface_count_history_20260601_20261207.csv to them on site and location, each count on the trading day of its counted_utc in UK time (06:00 to 06:00).
3. For every CYC count with an earlier count of any kind on the same face, took the trading days since that count as exposure and fitted per centre and class the per-day chance p of a VARIANCE result by maximum likelihood on P(MATCH) = (1 - p)^days.
4. Gave each in-scope face (1 - p)^d, d the trading days from its last count of any kind to the night of 6 December, and averaged by centre: Hinckley 99%, Daventry 98%, Bellshill 98%, Thurrock 96%, Magor 99%, Warrington 98%, Avonmouth 98%, Doncaster 96%.
5. Compared each with 97.0 per cent (SCS-07 5.1): Hinckley, Daventry, Bellshill, Magor, Warrington and Avonmouth qualify.
6. Stock value: WMS_stock_by_location_THN_20261207_0600.csv qty once per gate face, eaches divided by the case size valid on 7 December, times cost per case from THN_cost_price_list_20261128.csv overridden by THN_cost_changes_P10_2026.csv (effective 6 December).
7. Forecast cases: THN_store_replen_forecast_run_20261123.csv for 7 December to 3 January, depot from THN_store_servicing_map.csv valid on each trading date, EA rows divided by units_per_case, store-days CLOSED in THN_store_trading_calendar_2026_27.csv removed.
8. Recommendation: Hinckley, Daventry, Bellshill, Magor, Warrington and Avonmouth run unattended; Thurrock and Doncaster are supervised.

## 4. Deliverable Answers

### freeze_gate_2026.html
1. Share of correct records at 06:00 on 7 December, whole per cents, against the 97.0% line:
   - Hinckley: 99%, qualifies
   - Daventry: 98%, qualifies
   - Bellshill: 98%, qualifies
   - Thurrock: 96%, does not qualify
   - Magor: 99%, qualifies
   - Warrington: 98%, qualifies
   - Avonmouth: 98%, qualifies
   - Doncaster: 96%, does not qualify
2. Thornacre stock value on the gate's faces, nearest £1,000:
   - Hinckley: £1,174,000
   - Daventry: £1,292,000
   - Bellshill: £939,000
   - Thurrock: £1,068,000
   - Magor: £877,000
   - Warrington: £1,241,000
   - Avonmouth: £1,001,000
   - Doncaster: £1,086,000
3. Cases forecast to be drawn over the freeze, nearest hundred:
   - Hinckley: 1,119,600 cases
   - Daventry: 666,000 cases
   - Bellshill: 450,800 cases
   - Thurrock: 923,100 cases
   - Magor: 203,300 cases
   - Warrington: 435,500 cases
   - Avonmouth: 398,600 cases
   - Doncaster: 362,500 cases
4. Bar chart of the forecast cases, one bar per centre, largest first (Hinckley, Thurrock, Daventry, Bellshill, Warrington, Avonmouth, Doncaster, Magor), each bar labelled with its value, titled "Hinckley draws the most over the freeze".
