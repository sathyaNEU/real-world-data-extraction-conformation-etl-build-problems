## Tags

**Domain:** Physical and environmental sciences (sensor calibration and measurement).
**Analytical objective:** Data quality monitoring and alerting.

## 1. Final Recommendation

**Flag BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1 and GAR-FW1 in the fourth-quarter 2027 return: these six treated-water channels read more than 0.005 mg/L as N off the water at their sample points.**
Each listed channel is 0.006 or more off and every other channel within 0.004 of zero, once each analyser's carryover from the two ports before a reading, its calibration error at the channel's own level and the ammonia its sample line takes before the cell are all counted. Not HOL-FI1: its carryover from the raw sample is cancelled by its filtered line's loss. Not HOL-FW1: its carryover from the raw sample two ports back is cancelled by Holmedale's zero error. Not CAL-FW1: Calderwood's calibration error is a span error, small at treated levels.

## 2. Critical Components

1. Five analysers (Brannock, Dunmere, Elstow, Garrick and Holmedale) do not empty their measuring cell between ports: each reading is a mix of its own sample with small shares of the two samples before it, so the channel read straight after raw water reads high, and at Garrick and Holmedale, with raw water two to three times the others', so does the channel read two ports after it.
2. Holmedale's analyser reads **0.008** low at every level, a zero error that cancels HOL-FW1's carryover; Calderwood's reads about **8 per cent** low, a span error.
3. Calderwood's and Holmedale's filtered sample lines take about 60 per cent and nearly all of the filtered water's ammonia before the cell once the line has grown its film again: their readings rise at every monthly line flush and fall back over the following days, on average about **0.010** and **0.019** below the water over the quarter.
4. With the line counted, CAL-FI1 reads **0.007** or more below its water and HOL-FI1 sits within **0.004** of zero.

## 3. Step-by-Step Solution

1. Read WQ-DS-04 sections 3 and 4 (the offset over the channel's G readings in the historian against the water at its sample point, flagged beyond 0.005 either way) and the register's port sequences and planned maintenance log; kept each slot's G row, a filled-in slot's G row standing over its F row, and took each reading's port from its sample point.
2. For each analyser, fitted the carryover as a mix in the cell: both treated ports' readings together on the readings of the two slots before them (check readings as the cell's content), one pair of shares for the analyser, each port with its own level and its own response to the raw readings 2 to 8 hours earlier; each channel's carryover offset is the shares of the differences between the two slots before it and its own reading, divided by one less both shares. Brannock, Dunmere, Elstow, Garrick and Holmedale carry about 7 per cent of the slot before and 2 per cent of the one before that, the other three under 1 per cent.
3. Took each analyser's check mean from analyser_verification_2027Q4.xlsx and set it beside the raw grabs in lims_ammonia_2027Q4.csv, each paired with the raw reading of its slot with the raw port's own carryover taken out: Holmedale's shortfall is the same at both levels (a zero error), Calderwood's in proportion (a span error), the other six within 0.002 of 0.100.
4. Took each treated reading's carryover and calibration error out and fitted what was left on the days since the last monthly line flush in the planned maintenance log (New Zealand time): a level, the raw readings 2 to 8 hours earlier, and a loss that grows back as one less an exponential in those days. Only Calderwood's and Holmedale's filtered channels rise at every flush (by 0.009 to 0.011 and 0.018 to 0.020, the six hours after it against the two days before) and fall back over the following days (a regrowth time of 2.0 days for both); no other channel moves at the flushes.
5. Added to each of those two channels its line's fitted loss averaged over its G readings (0.010 and 0.019 below the water), summed each channel's carryover, calibration error at its own level and line loss, and flagged beyond 0.005: BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1 and GAR-FW1.
6. For each plant's treated samples, moved the laboratory's analysis stamps forward an hour: some runs are stamped up to 53 minutes before reception logged their bottles and no result is released within 64 minutes of its stamp, so the stamps run behind the laboratory's other clocks and every shift in that range counts the same; mapped the October codes through the laboratory's notice; counted each bottle once, the 7 December round's treated bottles being logged a second time under the courier docket's pickup time with the same point, analysis stamp, result and release; and counted those analysed more than 24 hours after collection.
7. For each plant's filtered water port, treated as available to the PLC every slot except the check cycles and the slots no reading reached it: a failed poll later filled from the outstation, the historian's lost hours of 17 November and each run of unfilled F rows at every port that no check followed and across which the analyser's port sequence ran on unbroken (the November outstation changes) were the historian's alone, while the runs after which the sequence starts again at the raw water port (each analyser's stop on the storm night of 26 to 27 October or 3 to 4 December, until the morning reset) and the filtered port's own unfilled F rows, the other ports read between them (once at each plant), never reached the PLC; summed each gap between good readings beyond the two-hour hold.

## 4. Deliverable Answers

### ammonia_channel_offsets_2027Q4.xlsx

1. Flagged channels, six: BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1 and GAR-FW1.
2. Filtered and final water samples analysed more than 24 hours after collection, by plant:
   - Ashcombe: 14
   - Brannock: 9
   - Calderwood: 8
   - Dunmere: 12
   - Elstow: 11
   - Fenwick: 13
   - Garrick: 14
   - Holmedale: 11
3. Hours at the fixed chlorine dose because the filtered water ammonia reading was not available, by plant:
   - Ashcombe: 31.2
   - Brannock: 27.8
   - Calderwood: 35.8
   - Dunmere: 32.2
   - Elstow: 26.7
   - Fenwick: 34.8
   - Garrick: 31.3
   - Holmedale: 29.3

### ammonia_channel_offsets_2027Q4.png

1. Every treated channel's quarter offset by plant against the 0.005 band, the six flagged channels marked.
