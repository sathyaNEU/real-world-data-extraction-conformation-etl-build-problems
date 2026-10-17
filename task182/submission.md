**Domain:** Physical and environmental sciences (environmental monitoring and exceedance).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The October acoustic treatment slot should cover NSL04, NSL11, NSL07, NSL02 and NSL13.**
Their specific sound levels are 53.0, 49.9, 47.8, 47.3, 46.0 dB LAeq, and NSL06 is the first dwelling off the list at 44.7 dB, 1.3 dB behind the fifth.
Not the five highest measured levels, which put NSL06 in and NSL13 out, because the measured level at a dwelling still holds its surroundings.
Not a background taken from the position's own record, which puts NSL03 and NSL12 in: the plant runs through every assessment minute, so that background contains it.
Not the complaints register, which is a record of what neighbours heard and not a measurement.

## 2. Critical Components

1. The measured sound level at NSL04 is **53.2 dB LAeq** over 6,130 valid assessment minutes
2. The residual sound at NSL04, from the 240 minutes inside the plant's weekly process stops, is **40.5 dB LAeq**
3. The specific sound level at NSL04 is **53.0 dB LAeq**
4. The fifth dwelling on the list stands **1.3 dB** above the sixth, NSL06

## 3. Step-by-Step Solution

1. Paired each of the 28 deployments in meter_deployments_2026.csv with its position, and took each deployment's field-check deviation off its levels where plan 4.1 calls for it, which is 11 of them.
2. Read sound_levels_1min_2026.parquet, kept one copy of the repeated download, and took the meters' UTC stamps to local time as survey_notes.md states.
3. Dropped the minutes whose ten-minute record in weather_10min_2026.csv counted rain or ran above the plan's wind limit, reading the replacement anemometer in km an hour from 20 September, and the minutes the meter recorded no measurement for, per plan 4.2.
4. Energetically averaged each position's assessment-period minutes for its measured sound level, per plan 3.1 and 3.2.
5. Took each position's residual sound from the minutes inside the intervals in plant_equipment_events_2026.csv where the blowers, the centrifuges and the gas engine are all recorded down, and read the plant's running state over each position's assessment period from the same log, per plan 5.2.
6. Subtracted residual from measured level in energy for the specific sound level at each position, per plan 3.1.
7. Ranked the fourteen positions on that level and took the five the slot reaches, per plan 7.1: NSL04, NSL11, NSL07, NSL02 and NSL13.
8. Recommended those five dwellings for the October slot, with NSL06 named as the first off the list.

## 4. Deliverable Answers

### specific_sound_levels.csv

1. One row for each of the 14 monitoring positions, in schedule order:
   - NSL01 (DW-114): 43.9 dB LAeq, 4,306 minutes with a centrifuge running, 14 runs
   - NSL02 (DW-103): 47.3 dB LAeq, 4,306 minutes with a centrifuge running, 14 runs
   - NSL03 (DW-121): 43.6 dB LAeq, 4,024 minutes with a centrifuge running, 11 runs
   - NSL04 (DW-101): 53.0 dB LAeq, 4,306 minutes with a centrifuge running, 14 runs
   - NSL05 (DW-130): 38.7 dB LAeq, 4,268 minutes with a centrifuge running, 14 runs
   - NSL06 (DW-107): 44.7 dB LAeq, 3,973 minutes with a centrifuge running, 9 runs
   - NSL07 (DW-110): 47.8 dB LAeq, 3,973 minutes with a centrifuge running, 9 runs
   - NSL08 (DW-126): 41.4 dB LAeq, 3,973 minutes with a centrifuge running, 9 runs
   - NSL09 (DW-112): 44.6 dB LAeq, 3,885 minutes with a centrifuge running, 11 runs
   - NSL10 (DW-134): 37.4 dB LAeq, 3,902 minutes with a centrifuge running, 11 runs
   - NSL11 (DW-104): 49.9 dB LAeq, 3,515 minutes with a centrifuge running, 10 runs
   - NSL12 (DW-118): 43.3 dB LAeq, 3,515 minutes with a centrifuge running, 10 runs
   - NSL13 (DW-105): 46.0 dB LAeq, 3,586 minutes with a centrifuge running, 8 runs
   - NSL14 (DW-128): 42.0 dB LAeq, 3,868 minutes with a centrifuge running, 11 runs

### mitigation_shortlist.pdf

1. The five dwellings the slot covers: NSL04 (DW-101) at 53.0 dB LAeq, NSL11 (DW-104) at 49.9 dB LAeq, NSL07 (DW-110) at 47.8 dB LAeq, NSL02 (DW-103) at 47.3 dB LAeq, NSL13 (DW-105) at 46.0 dB LAeq
2. The first dwelling off the list: NSL06 (DW-107) at 44.7 dB LAeq, 1.3 dB below the fifth
3. A tone is prominent at 6 of the fourteen positions, NSL02, NSL03, NSL04, NSL07, NSL09, NSL11, and in every case in the 400 Hz band
4. The plant through the six survey weeks:
   - Week beginning 31 August: blower air 689 thousand Nm3, 12 centrifuge runs, engine 164.3 hours
   - Week beginning 7 September: blower air 678 thousand Nm3, 13 centrifuge runs, engine 162.0 hours
   - Week beginning 14 September: blower air 679 thousand Nm3, 9 centrifuge runs, engine 166.0 hours
   - Week beginning 21 September: blower air 700 thousand Nm3, 12 centrifuge runs, engine 163.2 hours
   - Week beginning 28 September: blower air 668 thousand Nm3, 8 centrifuge runs, engine 160.5 hours
   - Week beginning 5 October: blower air 686 thousand Nm3, 13 centrifuge runs, engine 164.7 hours
5. Ranked bar chart of all fourteen specific sound levels with the five selected marked and the slot's reach drawn, on page 1
