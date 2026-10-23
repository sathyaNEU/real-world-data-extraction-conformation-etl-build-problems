## Tags

**Domain:** Energy Systems & Utilities (load forecasting).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**File 155,000 MWh as the irrigation class's April to September 2027 energy.** The Lone Bench services draw what they drew in 2022, when the district delivered nothing, and the bottomland plants make the diversion above a quarter of their allotments up from their own shallow wells, whose energy per acre-foot each plant's meter separates from its river lift's. Not the bench wells' energy per acre-foot carried onto the bottomland cut, which prices shallow water at deep lifts. Not each plant's energy over its water, which reads a river lift and a well on one meter as one pump.

## 2. Critical Components

1. The Lone Bench services draw **118,000 MWh** in a normal season with no district water.
2. The bottomland plants' wells make up **145,000 acre-feet** of diversion the order removes.

## 3. Step-by-Step Solution

1. Summed every read line in vvpud_ip_billing_2015-2026.csv by service and bill month, legacy accounts mapped through vvpud_cis_account_crosswalk_2020.csv, and kept the services ACTIVE in vvpud_ip_service_register_2026-09-30.xlsx; a service is a bottomland plant when varner_watermaster_diversion_statements_2015-2026.csv names it as a point's measure.
2. Took the April to September total of station247_daily_eto_2007-2026.csv in each season and their 2007 to 2026 mean, 38.97 in, as the normal season the forecast instructions define.
3. Put the Lone Bench services at their 2022 April to September energy times the normal over 2022's ET: 118,000 MWh.
4. Put each bottomland plant at its 2015 to 2026 seasons' energy, each at normal ET, averaged, and its diversion the same way; the order holds diversion to 25 per cent of the allotment in varner_decree_allotment_schedule_2026.xlsx, so the diversion above that is lost to the river and made up from a well where the plant has one in vsga_extraction_reports_wy2017-wy2026.xlsx: 145,000 acre-feet.
5. Fitted each plant's October to September energy, without intercept, on its season diversion and its metered well extraction for water years 2017 to 2026 to get its river lift's and its well's kWh per acre-foot (a plant with no well: its energy over its diversion).
6. Added each plant's well energy on the water made up and took off its river lift's energy on the diversion lost; with the Lone Bench services the class draws 155,000 MWh to the nearest 5,000.
7. Read hpa_dp_interval_export_2026.csv as meter standard time (every meter carries 96 intervals on 8 March 2026), moved daylight-time intervals an hour forward, kept the revenue meters (each point's check meter repeats its revenue meter one interval early; Bench's second bank adds its own meter from 15 June) and summed each billing month, and each posted peak's clock hour from hpa_2026_monthly_system_peaks.csv.
8. Put each service at the delivery point its feeder was supplied from through the season in vvpud_oms_feeder_sources.csv (two feeders moved by switching order, one in November 2025 and one in March 2026), not the GIS substation, and summed its April to September 2026 bills.

## 4. Deliverable Answers

### irrigation_forecast_2027.xlsx

1. Schedule IP energy, 1 April to 30 September 2027, normal season: 155,000 MWh.
2. Energy Halvern metered at each delivery point, billing months April to September 2026, kWh:
   - Riverside: April 4,337,023, May 4,792,475, June 4,918,970, July 5,198,818, August 4,883,322, September 4,371,873
   - Mill Slough: April 1,970,622, May 2,376,369, June 2,592,761, July 2,795,017, August 2,504,076, September 2,082,669
   - Bench: April 8,484,220, May 11,245,337, June 12,898,420, July 14,288,088, August 12,352,771, September 9,440,557
   - Corwin Road: April 8,454,690, May 11,548,010, June 13,611,445, July 15,148,942, August 12,767,482, September 9,500,821
3. Demand at each delivery point in Halvern's monthly system peak hour, April to September 2026, kW:
   - Riverside: April 7,369, May 8,963, June 8,319, July 8,557, August 7,703, September 7,444
   - Mill Slough: April 3,489, May 4,593, June 3,905, July 4,072, August 3,499, September 3,129
   - Bench: April 15,332, May 20,712, June 16,878, July 18,550, August 14,537, September 12,645
   - Corwin Road: April 14,084, May 21,893, June 16,380, July 18,058, August 14,481, September 12,235
4. Irrigation services each delivery point supplied through the 2026 season and their April to September 2026 billed energy:
   - Riverside: 186 services, 8,208.6 MWh
   - Mill Slough: 198 services, 8,136.8 MWh
   - Bench: 147 services, 55,488.3 MWh
   - Corwin Road: 149 services, 59,619.7 MWh
