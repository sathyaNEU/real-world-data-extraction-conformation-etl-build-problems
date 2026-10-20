## Tags

**Domain:** Energy Systems & Utilities (a community wind farm's production accounting: blade performance against the warranted curve, reconciled to the revenue counters and the connection meter).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Book the summer 2027 leading-edge repair campaign on CH04; the repaired blades should recover 100 MWh (to the nearest 50 MWh) over the twelve months after the work.**
Compared with the same turbine in the same winds with its blades as new (each ten-minute record at its own turbulence), CH04's blades cost 89 MWh over its normal operation in October 2025 to September 2026, the largest blade loss on the farm; CH02's cost 65 MWh. Not CH07, whose 235 MWh shortfall against the warranted curve at the same mean wind is the plantation's turbulence, not its blades: at its own turbulence it loses less than 1 MWh.

## 2. Critical Components

1. Turbine for the 2027 campaign: **CH04**.
2. Energy the repaired blades recover over the twelve months after the work: **100 MWh** (to the nearest 50 MWh).

## 3. Step-by-Step Solution

1. Read OM-07_blade_campaigns_and_lost_production.pdf: a campaign is valued on the turbine's last twelve months of normal operation (states 10 and 20) as the energy it would have produced in the same winds with its blades as new, less what it produced (2.4); a blade set fitted within the twelve months is measured on its own months (2.5).
2. Aligned scada_10min_2025-10_2026-09.parquet to UTC: its timestamps are interval ends in UK local time up to the platform change of 3 February 2026 (the repeated hour at the October 2025 clock change shows it) and UTC after it (no hour is missing at the March 2026 change). Joined metmast_M1_10min_2025-10_2026-09.csv (UTC, interval starts) for air density and corrected each nacelle wind to 1.225 kg/m3 as v(rho/1.225)^(1/3).
3. Took CH09 from 25 April 2026: crane_lift_log_2026.xlsx lifts a pool rotor onto pad P08, which site_layout_pads.csv gives as CH09, after the main-bearing exchange in work_orders_2025-10_2026-09.csv.
4. Built each turbine's shortfall against TSA_schedule_3_warranted_power_curve.pdf at the same mean wind by the method of bins: CH07 235 MWh, CH01 115, CH05 114, CH04 93, CH02 71, the rest under 10. This is not the blade loss: CH07, CH05 and CH01 run above the warranted curve from 4 to 8.5 m/s and below it from 9.5 to 12 m/s, the signature of a ten-minute power averaged over high turbulence (CH07's nacelle turbulence intensity in south-westerly and westerly winds is 2.3 times that of the turbines in open air).
5. Measured each record's turbulence intensity as wind_speed_sd over wind_speed_mean and fitted the zero-turbulence curve (power coefficient 0.470, cut-in 3.0 m/s, rated 2,300 kW) that reproduces Schedule 3 when averaged over the mast's median turbulence by bin (IEC 61400-12-1 Annex M). Averaged over each record's own turbulence it gives the as-new power in the same winds; summed less the power made, it is each turbine's blade loss: CH04 89 MWh, CH02 65 MWh, every other turbine within 1 MWh of nothing. Comparing each turbine with the fleet in the same 0.5 m/s and turbulence bins gives CH04 83 MWh and the same order.
6. Booked the campaign on CH04 and valued it at 89 MWh, 100 MWh to the nearest 50 MWh. CH02 leads any cut below rated (77 MWh against CH04's 42 between 3 and 10 m/s) because the loch gives it the smoothest air on the site, which lowers a ten-minute power at low wind; CH02 stands upwind of CH04 at three and a half rotor diameters, and its wake lifts CH04's low-wind power by about what CH04's blades lose there.
7. The asks: each turbine's metered generation over the ten months 1 November 2025 to 31 August 2026 is its revenue counter's span between the November and September rounds, taken to the window's own ends with the energy in the two part-windows from the ten-minute record, because the round reads the pads over two days from the month's first working day and not at the month end; the farm's metered export by month is the connection meter's export register summed on the month each half-hour falls in locally, the file being stamped in UTC and the register carrying export only, with the farm's own demand on the import register.

## 4. Deliverable Answers

### le_repair_campaign_2027.pdf

1. The 2027 campaign goes to CH04.
2. Energy the repaired blades recover over the twelve months after the work: 100 MWh (to the nearest 50 MWh).
3. Chart: each turbine's metered generation over the ten months from 1 November 2025 to 31 August 2026, one bar per turbine (CH01 to CH10), in MWh, each bar labelled with its figure.

### metered_generation_2025_26.xlsx

1. Metered generation, the ten months 1 November 2025 to 31 August 2026, MWh:
   - CH01: 6,708
   - CH02: 6,770
   - CH03: 6,554
   - CH04: 6,327
   - CH05: 6,404
   - CH06: 5,966
   - CH07: 6,394
   - CH08: 6,398
   - CH09: 5,938
   - CH10: 6,394
2. The farm's metered export, by month (site local time), MWh:
   - November 2025: 6,960
   - December 2025: 9,765
   - January 2026: 5,121
   - February 2026: 6,819
   - March 2026: 8,310
   - April 2026: 5,868
   - May 2026: 2,513
   - June 2026: 3,267
   - July 2026: 5,634
   - August 2026: 6,334
