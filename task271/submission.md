## Tags

**Domain:** Survey Research & Official Statistics (sample design, allocation and weighting: a lake-stocking society's creel survey, each lake's open-water angler-hours per hectare expanded from route-timed aerial counts).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Put Corriemore, Tessaly, Ellerdine, Kesterway, Quorrin, Brackwater, Pinewhistle, Ravensky, Inverkeld and Kittiwake into the 2027 high-use tier; every other lake that takes catchables stays standard.** Each of the ten was fished for more than 500 angler-hours per hectare from 15 May to 31 August 2026 once each flight count is read against the hours that lake's own anglers fish, and it stays above 550 however a count's time is read against those hours; the standard lakes stay below 480. Depending on that reading, the high-use lake nearest the line is Ravensky, Kesterway, Ellerdine or Brackwater, and the standard lake nearest it Galloran, Nockell or Farrowdale. Not the plain expansion's list: each count times the 17-hour day puts Galloran, Nockell and Farrowdale in and leaves Ellerdine, Quorrin, Ravensky and Inverkeld out, because the flights pass every lake between about 09:30 and 17:00, the general lakes' busy hours and the fly-only lakes' quiet ones.

## 2. Critical Components

1. Each lake is counted at the time its place on the Vellacott route brings the aircraft over it, so every count falls between about 09:30 and 12:00 or 14:30 and 17:00; the interviews' start and finish times show the fly-only lakes fished mostly at dawn and dusk and the general lakes through the middle of the day.
2. Each count is divided by the share of that lake's interviewed angler-hours present at the time it was made (boats times the lake's own anglers per boat, plus shore anglers), averaged by survey day and expanded by weekday and weekend day in each month, then divided by the register's area.
3. Ellerdine, Quorrin, Ravensky and Inverkeld come in above 550 angler-hours per hectare and Galloran, Nockell and Farrowdale fall below 480, whether a count's time is read by its hour, the nearest hour, interpolated, over the hour around it or at its minute, and with each lake's own hours or its regulation class's.
4. The plain expansion puts Galloran, Nockell and Farrowdale above 550 and leaves Ellerdine, Quorrin, Ravensky and Inverkeld below 460, however the boats are turned into anglers and the blank counts are read; spreading the counts by the survey's pooled hourly profile leaves that list unchanged.

## 3. Step-by-Step Solution

1. Matched survey_flight_counts_2026.csv (Vellacott numbers) and creel_interviews_2026.csv (tablet names) to lake_register_2026.xlsx, left out the loop and the lakes entered with no count, and where an interview gives no start took the finish less the hours fished.
2. Turned each count into anglers: boats times the lake's mean party size among boat parties, plus shore anglers.
3. For each lake, shared every interviewed party's anglers over the hours of 05:00 to 22:00 it fished and took each hour's share of the lake's interviewed angler-hours.
4. Divided each count by its lake's share for the hour of the count, averaged the counts of each survey day, took the mean survey day in each month's weekday and weekend strata, multiplied by the stratum's days and summed over 15 May to 31 August.
5. Divided by the register's surface area and set each lake that takes catchables against 500 (catchable_allocation_policy_2026.pdf, 2.2 and 2.3); every other reading of a count's time against the hours keeps each high-use lake above 550 and each standard lake below 480.
6. Releases: each trip's net load at its raceway's latest Monday sample count (fish per kg), reading trip sheet raceway numbers before the tank temperature column began as the old numbers (quillet_creek_raceway_numbers.csv), shared between drops by the drop crew's nets, less the dead fish counted at the drop.
7. Warm days: assigned each logger reading to the deployment its serial was in at that moment (logger_deployments_2026.csv), put loggers 20184409 and 20184421 from UTC onto Pacific time, and counted the July and August days whose 1 m readings averaged above 20 C.
8. Recommended the ten lakes above for the high-use tier.

## 4. Deliverable Answers

### stocking_tiers_2027.xlsx

1. High-use tier for 2027: Corriemore, Tessaly, Ellerdine, Kesterway, Quorrin, Brackwater, Pinewhistle, Ravensky, Inverkeld and Kittiwake.
2. Standard: Galloran, Nockell, Kelloran, Ostrum, Farrowdale, Pillory, Bufflehead, Mosswater, Canvasback, Saddlebank, Copperjack and Thornhollow.
3. Angler-hours per hectare, 2026 open-water season: every high-use lake above 550 and every standard lake below 480.
4. Catchable rainbow trout released alive in 2026, nearest 100:
   - Brackwater: 5,000
   - Bufflehead: 1,800
   - Canvasback: 4,400
   - Copperjack: 2,300
   - Corriemore: 3,000
   - Ellerdine: 1,000
   - Farrowdale: 1,600
   - Galloran: 3,100
   - Inverkeld: 3,200
   - Kelloran: 3,200
   - Kesterway: 3,300
   - Kittiwake: 2,800
   - Mosswater: 4,500
   - Nockell: 3,100
   - Ostrum: 2,300
   - Pillory: 4,800
   - Pinewhistle: 2,900
   - Quorrin: 1,900
   - Ravensky: 2,000
   - Saddlebank: 3,200
   - Tessaly: 3,000
   - Thornhollow: 2,300
5. Days in July and August with the 1 m water averaging above 20 C (Pacific-time days):
   - Brackwater: 57
   - Corriemore: 19
   - Inverkeld: 6
   - Kelloran: 11
   - Kesterway: 19
   - Kittiwake: 19
   - Mosswater: 2
   - Quorrin: 6
   - Tessaly: 57

### stocking_board_note_2027.docx

1. Recommendation: Corriemore, Tessaly, Ellerdine, Kesterway, Quorrin, Brackwater, Pinewhistle, Ravensky, Inverkeld and Kittiwake into the 2027 high-use tier; every other lake standard.
2. Chart: a bar for each lake's angler-hours per hectare against the 500 line, the high-use lakes shaded dark.
