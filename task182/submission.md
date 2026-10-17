**Domain:** Physical and environmental sciences (environmental monitoring and exceedance).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The October acoustic treatment slot should cover NSL04, NSL11, NSL07, NSL02 and NSL13.**
Their specific sound levels are 53.1, 49.9, 47.9, 47.2, 46.0 dB LAeq, and NSL06 is the first dwelling off the list at 45.2 dB, 0.8 dB behind the fifth.
Not the five highest measured levels, which put NSL06 in and NSL13 out, because the measured level at a dwelling still holds its surroundings.
Not a background taken from the position's own record, which puts NSL03 and NSL12 in: the plant runs through every assessment minute, so that background contains it.
Not the complaints register, which is a record of what neighbours heard and not a measurement.

## 2. Critical Components

1. The measured sound level at NSL04 is **53.3 dB LAeq** over 6,460 valid assessment minutes
2. The residual sound at NSL04, from the 240 minutes inside the plant's weekly process stops, is **39.3 dB LAeq**
3. The specific sound level at NSL04 is **53.1 dB LAeq**
4. The fifth dwelling on the list stands **0.8 dB** above the sixth, NSL06

## 3. Step-by-Step Solution

1. Paired each of the 28 deployments in meter_deployments_2026.csv with its position, and applied the field-check correction plan 4.1 calls for to the two deployments that need one.
2. Read sound_levels_1min_2026.parquet, kept one copy of the repeated download, and took the meters' UTC stamps to local time as survey_notes.md states.
3. Dropped the minutes whose met record in weather_10min_2026.csv exceeds the plan's rain or wind limits, reading the replacement anemometer in km an hour from 20 September, per plan 4.2.
4. Energetically averaged each position's assessment-period minutes for its measured sound level, per plan 3.1 and 3.2.
5. Took each position's residual sound from the minutes inside the intervals in plant_equipment_events_2026.csv where the blowers, the centrifuges and the gas engine are all recorded down.
6. Subtracted residual from measured level in energy for the specific sound level at each position, per plan 3.1.
7. Ranked the fourteen positions on that level and took the five the slot reaches, per plan 6.1: NSL04, NSL11, NSL07, NSL02 and NSL13.
8. Recommended those five dwellings for the October slot, with NSL06 named as the first off the list.

## 4. Deliverable Answers

### specific_sound_levels.csv

1. One row for each of the 14 monitoring positions, in schedule order:
   - NSL01 (DW-114): 43.9 dB LAeq, 6460 valid minutes, 740 excluded, highest band 100 Hz, tone no
   - NSL02 (DW-103): 47.2 dB LAeq, 6460 valid minutes, 740 excluded, highest band 400 Hz, tone yes
   - NSL03 (DW-121): 43.6 dB LAeq, 6830 valid minutes, 370 excluded, highest band 100 Hz, tone no
   - NSL04 (DW-101): 53.1 dB LAeq, 6460 valid minutes, 740 excluded, highest band 400 Hz, tone yes
   - NSL05 (DW-130): 39.6 dB LAeq, 6460 valid minutes, 740 excluded, no band rows, so no highest band and no tone
   - NSL06 (DW-107): 45.2 dB LAeq, 6900 valid minutes, 300 excluded, highest band 100 Hz, tone no
   - NSL07 (DW-110): 47.9 dB LAeq, 6900 valid minutes, 300 excluded, highest band 100 Hz, tone yes
   - NSL08 (DW-126): 41.7 dB LAeq, 6900 valid minutes, 300 excluded, no band rows, so no highest band and no tone
   - NSL09 (DW-112): 44.6 dB LAeq, 6640 valid minutes, 560 excluded, highest band 100 Hz, tone yes
   - NSL10 (DW-134): 37.5 dB LAeq, 6640 valid minutes, 560 excluded, no band rows, so no highest band and no tone
   - NSL11 (DW-104): 49.9 dB LAeq, 6300 valid minutes, 900 excluded, highest band 400 Hz, tone yes
   - NSL12 (DW-118): 43.5 dB LAeq, 6300 valid minutes, 900 excluded, highest band 100 Hz, tone no
   - NSL13 (DW-105): 46.0 dB LAeq, 6560 valid minutes, 640 excluded, highest band 100 Hz, tone no
   - NSL14 (DW-128): 42.0 dB LAeq, 6190 valid minutes, 1010 excluded, no band rows, so no highest band and no tone

### mitigation_shortlist.pdf

1. The five dwellings the slot covers: NSL04 (DW-101) at 53.1 dB LAeq, NSL11 (DW-104) at 49.9 dB LAeq, NSL07 (DW-110) at 47.9 dB LAeq, NSL02 (DW-103) at 47.2 dB LAeq, NSL13 (DW-105) at 46.0 dB LAeq
2. The first dwelling off the list: NSL06 (DW-107) at 45.2 dB LAeq, 0.8 dB below the fifth
3. The plant through the six survey weeks:
   - Week beginning 31 August: biogas 35389 m3, blower air 689 thousand Nm3, 6 centrifuge runs
   - Week beginning 7 September: biogas 34821 m3, blower air 678 thousand Nm3, 6 centrifuge runs
   - Week beginning 14 September: biogas 34934 m3, blower air 679 thousand Nm3, 6 centrifuge runs
   - Week beginning 21 September: biogas 36030 m3, blower air 617 thousand Nm3, 5 centrifuge runs
   - Week beginning 28 September: biogas 34376 m3, blower air 669 thousand Nm3, 6 centrifuge runs
   - Week beginning 5 October: biogas 35229 m3, blower air 686 thousand Nm3, 6 centrifuge runs
4. Ranked bar chart of all fourteen specific sound levels with the five selected marked and the slot's reach drawn, on page 1
