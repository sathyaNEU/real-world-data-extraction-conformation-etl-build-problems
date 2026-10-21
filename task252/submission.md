## Tags

**Domain:** Physical and environmental sciences (sensor calibration and measurement).
**Analytical objective:** Data quality monitoring and alerting.

## 1. Final Recommendation

**Flag BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1 in the fourth-quarter 2027 return: these six treated-water channels read more than 0.005 mg/L as N off the water they sample.**
Each listed channel is 0.007 or more off and every other channel within 0.003 of zero, once each analyser's carryover from the two ports before a reading and its calibration error at the channel's own level are both counted. Not HOL-FW1: its carryover from the raw sample two ports back is cancelled by Holmedale's zero error. Not CAL-FI1 or CAL-FW1: Calderwood's error is a span error, about 0.002 at treated levels.

## 2. Critical Components

1. Five analysers (Brannock, Dunmere, Elstow, Garrick and Holmedale) do not empty their measuring cell between ports: each reading is a mix of its own sample with small shares of the two samples before it, so it is off by those shares of the differences between those samples and its own; the channel read straight after raw water reads high, and at Garrick and Holmedale, with raw water two to three times the others', so does the channel read two ports after it.
2. Holmedale's analyser reads **0.008** low at every level, a zero error: its checks read that much low at 0.100, and its raw port, once its own carryover from the treated ports ahead of it is taken out, falls short of the laboratory's raw grabs by about the same amount, far less than 8 per cent of their level.
3. Calderwood's analyser reads about **8 per cent** low, a span error: its raw port falls short of the raw grabs in proportion to their level, and it has no carryover.
4. HOL-FW1's carryover from the raw sample two ports back is about the size of Holmedale's zero error, so the two cancel and HOL-FW1 sits within **0.003** of zero.

## 3. Step-by-Step Solution

1. Read WQ-DS-04 sections 3 and 4 (the offset over the channel's G readings in the historian, flagged beyond 0.005 either way) and the register's port sequences; kept each slot's G row, a filled-in slot's G row standing over its F row.
2. For each analyser, fitted the carryover as a mix in the cell: both treated ports' readings together on the readings of the two slots before them (check readings as the cell's content), one pair of shares for the analyser, each port with its own level and its own response to the raw readings 2 to 8 hours earlier; each channel's carryover offset is the shares of the differences between the two slots before it and its own reading, divided by one less both shares. Brannock, Dunmere, Elstow, Garrick and Holmedale carry about 7 per cent of the slot before and 2 per cent of the one before that, the other three under 1 per cent.
3. Took each analyser's check mean from analyser_verification_2027Q4.xlsx: Holmedale and Calderwood read about 8 per cent low, the other six within 0.002 of 0.100.
4. Paired each raw grab in lims_ammonia_2027Q4.csv with the raw reading of its slot, took the raw port's own carryover from the two slots before it out of the reading with the analyser's shares, and compared the shortfall left with the check's: constant at Holmedale (a zero error), in proportion at Calderwood (a span error).
5. Added each analyser's calibration error at the channel's own level to the carryover offset and flagged beyond 0.005: BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1.
6. For each plant's treated samples, moved the laboratory's analysis stamps forward an hour: some runs are stamped up to 53 minutes before reception logged their bottles and no result is released within 64 minutes of its stamp, so the stamps run behind the laboratory's other clocks and every shift in that range counts the same; mapped the October codes through the laboratory's notice; counted each bottle once, the 7 December round's treated bottles being logged a second time under the courier docket's pickup time with the same point, analysis stamp, result and release; and counted those analysed more than 24 hours after collection.
7. For each plant's filtered water port, treated as available to the PLC every slot except the check cycles and the slots no reading reached it: a failed poll later filled from the outstation, the historian's lost hours of 17 November and each run of unfilled F rows at every port that no check followed (a failed poll takes the plant's whole record and a fault is followed by the technician's check, so these were the telemetry's, one a plant in November) were the historian's alone, while the filtered port's own unfilled F rows, the other ports read between them, never reached the PLC (once at each plant); summed each gap between good readings beyond the two-hour hold.

## 4. Deliverable Answers

### ammonia_channel_offsets_2027Q4.xlsx

1. Flagged channels, six: BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1.
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
   - Ashcombe: 25.0
   - Brannock: 23.0
   - Calderwood: 22.0
   - Dunmere: 28.5
   - Elstow: 20.5
   - Fenwick: 41.0
   - Garrick: 17.5
   - Holmedale: 22.0

### ammonia_channel_offsets_2027Q4.png

1. Every treated channel's quarter offset by plant against the 0.005 band, the six flagged channels marked.
