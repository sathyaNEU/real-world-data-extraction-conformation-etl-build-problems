## Tags

- **Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (storm overflow permit compliance at sewage pumping stations).
- **Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Self-report the Gallowfen PS storm overflow (permit EPRWW4412BK, condition 2.3.1): it discharged in 2026 while its station passed forward 48 l/s against the 72 l/s its permit sets.** Not none: Gallowfen's running pump is rated at 85.3 l/s but delivers 48. Not Hagworth Wold, whose wet well draws down slowly because groundwater runs in through every cycle, and whose pumps deliver 36 l/s against the 31 its permit sets through its dry-day discharges. Not Marram End, the most frequent spiller (57 spills), whose station passes forward more than its permitted flow.

## 2. Critical Components

1. Gallowfen's permit requires a pass forward flow of **72 l/s** before its overflow may discharge.
2. Gallowfen's pumps deliver **48 l/s**, 67 per cent of that flow, against a rated duty of **85.3 l/s**.
3. Every other pumping station passes forward at least its permitted flow; the closest is **Sallowholme at 57 l/s against 50 l/s**.

## 3. Step-by-Step Solution

1. Took each overflow's pass forward flow from condition 2.3.1 in `registers/wastewater_discharge_consents_2026.csv`: Gallowfen 72 l/s.
2. From `registers/marsh_wolds_wastewater_assets.xlsx`, took each wet well's plan area from its internal dimensions and the volume between the duty pump's start and stop levels.
3. From `pump_event` in `telemetry/marsh_wolds_sps_telemetry_2026.sqlite`, exact duplicates dropped, took each clean cycle's delivered rate as that volume over the pump-on time plus that volume over the pump-off time before it, and each station's median: Gallowfen 48 l/s against its 72.
4. Compared every station's delivered rate with its permitted flow: Gallowfen alone falls short, the closest of the rest Sallowholme at 57 against 50.
5. Mapped each retired serial in `edm/edm_monitor_list_2027-01-15.csv` to the overflow whose `alarm` OVERFLOW OPERATING periods its discharges coincide with, among the stations whose register monitor was installed in the nine days before it retired (one crew batch per retirement date, six to eight days before it in every batch), and pooled every serial per overflow.
6. On each overflow's discharges from every serial, starts and ends converted from UK local time and overlapping periods counted once, applied WW-ENV-PR-014's 12/24 count and summed the hours, split by local month for the chart.
7. Monitoring percentage: for each local day the most hours any of the overflow's monitors reported in `edm/edm_monitor_daily_status_2026.csv`, summed over 2026, over 8,760 hours.
8. Self-reported Gallowfen PS storm overflow, 12 spills and 20.4 hours of discharge in 2026.

## 4. Deliverable Answers

### overflow_self_report_2026.docx

1. Overflow and permit: Gallowfen PS storm overflow, permit EPRWW4412BK, condition 2.3.1.
2. Pass forward flow the permit sets: 72 l/s.
3. Flow the station was passing forward while it spilled: 48 l/s.

### overflow_return_lines_2026.csv

1. One line per storm overflow, in permit order:
   - EPRWW4407AX, Scarrow Leas PS storm overflow: permitted 35 l/s, passes forward 41 l/s, met the permit Yes, 15 spills, 28.9 hours of discharge, monitored 100.0 per cent
   - EPRWW4412BK, Gallowfen PS storm overflow: permitted 72 l/s, passes forward 48 l/s, met the permit No, 12 spills, 20.4 hours of discharge, monitored 99.5 per cent
   - EPRWW4415CG, Hagworth Wold PS storm overflow: permitted 31 l/s, passes forward 36 l/s, met the permit Yes, 30 spills, 97.9 hours of discharge, monitored 99.9 per cent
   - EPRWW4419AD, Marram End PS storm overflow: permitted 16 l/s, passes forward 19 l/s, met the permit Yes, 57 spills, 198.2 hours of discharge, monitored 98.0 per cent
   - EPRWW4421BN, Cressfleet PS storm overflow: permitted 39 l/s, passes forward 45 l/s, met the permit Yes, 15 spills, 24.1 hours of discharge, monitored 97.4 per cent
   - EPRWW4426CF, Sallowholme PS storm overflow: permitted 50 l/s, passes forward 57 l/s, met the permit Yes, 13 spills, 15.9 hours of discharge, monitored 99.8 per cent
   - EPRWW4428AT, Northwade Bank PS storm overflow: permitted 101 l/s, passes forward 118 l/s, met the permit Yes, 11 spills, 15.1 hours of discharge, monitored 98.5 per cent
   - EPRWW4433BW, Brackenings PS storm overflow: permitted 23 l/s, passes forward 29 l/s, met the permit Yes, 14 spills, 29.0 hours of discharge, monitored 99.4 per cent
   - EPRWW4437CQ, Thornmarsh PS storm overflow: permitted 73 l/s, passes forward 84 l/s, met the permit Yes, 13 spills, 19.7 hours of discharge, monitored 98.8 per cent
   - EPRWW4440AH, Kettlewade PS storm overflow: permitted 28 l/s, passes forward 32 l/s, met the permit Yes, 17 spills, 23.3 hours of discharge, monitored 99.9 per cent
   - EPRWW4444BR, Saltwade PS storm overflow: permitted 44 l/s, passes forward 52 l/s, met the permit Yes, 9 spills, 17.4 hours of discharge, monitored 100.0 per cent
   - EPRWW4449CJ, Reedhaven PS storm overflow: permitted 19 l/s, passes forward 22 l/s, met the permit Yes, 20 spills, 31.5 hours of discharge, monitored 99.4 per cent
   - EPRWW4452AM, Sedgefleet PS storm overflow: permitted 56 l/s, passes forward 67 l/s, met the permit Yes, 9 spills, 12.3 hours of discharge, monitored 99.7 per cent
   - EPRWW4458BE, Swathe Drove PS storm overflow: permitted 37 l/s, passes forward 43 l/s, met the permit Yes, 11 spills, 20.9 hours of discharge, monitored 99.8 per cent

### spill_hours_by_month_2026.svg

1. A grid of every overflow's hours of discharge in each month of 2026 (UK local time, every monitor that watched it), each cell labelled; the largest total Marram End PS storm overflow, 198.2 hours.
