## Tags

**Domain:** Physical and environmental sciences (environmental monitoring and exceedance).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**We should allocate 3 articulated dump trucks to the Phase 4 haul road in January 2027.**
At 4.5 loaded movements a truck an hour, 3 trucks make 13.5 movements an hour and keep haulage at MP1 within the 44.0 dB share, while 4 trucks (18.0 an hour) exceed it. Not the much larger fleet that the pilot's average haul movement allows, because about nine in ten of those movements stayed in the pit or behind the bund. Not a prediction from the register's declared sound power, which is not the loaded climb's level. Not a north-face average, because more than a third of the north loads tipped on the stockpile in the pit.

## 2. Critical Components

1. Each pilot haul movement's route state, from its loaded run against the survey: north face loads tipped at the primary hopper climbed the North face ramp and ran **along Haul road 2 over the original ground**, and every other movement stayed in the pit or behind the plant compound bund.
2. One Haul road 2 movement carries **several times** the energy at MP1 of any other route's movement, apportioned from the hourly record with the plant and residual as the baseline.
3. The Phase 4 haul road in the scheme runs from the bench crest to the same hopper over the original ground, **the same length to within a metre** as Haul road 2 from the pit crest and **within a metre of its distance from MP1** all along it, with its access ramp below the bench crest as the North face ramp lies below the pit crest, so each Phase 4 movement carries the Haul road 2 energy.
4. The share's hourly energy holds more than **13.5** and fewer than **18.0** Haul road 2 movements, which is **3** trucks.

## 3. Step-by-Step Solution

1. Read mp1_ulverthorpe_lane_15min_2026.csv (UTC, period-end stamps) into local weekday hours from 7 am to 5 pm on haul days and summed each complete hour's quarter-hour energy.
2. Built each loaded run in adt_telematics_2026-05_2026-10.parquet (LOADED after EMPTY) and gave it the face nearest its first fix and the tip (primary crusher feed hopper or run-of-mine stockpile) nearest its last, from ravensby_topographic_survey_2026-04.geojson.
3. Fitted each hour's energy at MP1 to its counts of movements by face and tip, counted at the hour of the tip, with an intercept for plant and residual (fixing the baseline at the plant and residual levels the noise management plan files instead gives the same count): a north face to hopper movement (Haul road 2) carries several times the energy of any other.
4. Set the Phase 4 haul road and the bench's access ramp in phase4_working_scheme_2027-01_draft.docx against Haul road 2 and the North face ramp in the survey: the same length to within a metre, within a metre of the same distance from MP1 all along it, each ramp below its crest.
5. Divided the 44.0 dB share's hourly energy by one Haul road 2 movement's energy and by the scheme's 4.5 movements a truck: 3 trucks fit, and 4 at 18.0 movements an hour do not.
6. Primary feed by month: belt scale tonnes less only those of the wheel loader's unordered buckets that fall in a belt interval carrying tonnage, each bucket placed in the interval that starts at or before it (the export stamps interval starts), over the hopper tips in the telematics; and belt tonnes over crusher running hours from the PLC log, each run ending at the network operator's supply-lost time wherever an interruption in northfell_networks_interruption_notices_2026.pdf falls inside it.
7. January 2026 sales: each ticket's product comes from its code through the code-to-product pairing that most tickets show against sales_orders_2025-12_2026-01.xlsx, and its weigh date from axle_weigher_RWP2_export_2026-01.csv, matching each Monday ticket to one portable record, or to one vehicle's records that day summing to its net.
8. Recommendation: 3 articulated dump trucks on the Phase 4 haul road in January 2027.

## 4. Deliverable Answers

### extension_haul_dial.csv

1. One row per fleet size, loaded movements an hour, then within the 44.0 dB share:
   - 1 truck: 4.5, yes
   - 2 trucks: 9.0, yes
   - 3 trucks: 13.5, yes
   - 4 trucks: 18.0, no
   - 5 trucks: 22.5, no
   - 6 trucks: 27.0, no
   - 7 trucks: 31.5, no
   - 8 trucks: 36.0, no
   - 9 trucks: 40.5, no
   - 10 trucks: 45.0, no
   - 11 trucks: 49.5, no
   - 12 trucks: 54.0, no

### extension_scheme_note.pdf

1. Allocation: 3 articulated dump trucks on the Phase 4 haul road in January 2027; a fourth takes haulage at MP1 over the 44.0 dB share.
2. MP1's loudest hours: north face loads going to the primary up the North face ramp and along Haul road 2 over the original ground; the Phase 4 haul road is set out over the same ground, within a metre of Haul road 2's distance from MP1 all along it.
3. Chart on page 1: haulage level at MP1 against trucks allocated, with the 44.0 dB share marked and 3 trucks circled.
4. Tonnes per haul load tipped into the primary hopper, one decimal:
   - May 2026: 35.0
   - June 2026: 36.2
   - July 2026: 37.4
   - August 2026: 37.8
   - September 2026: 34.9
   - October 2026: 35.1
5. Primary tonnes per running hour, one decimal:
   - May 2026: 491.9
   - June 2026: 487.3
   - July 2026: 545.2
   - August 2026: 509.0
   - September 2026: 516.1
   - October 2026: 464.4
6. Tonnes sold in January 2026 by product as charged, nearest tonne:
   - 0-4 mm dust: 2,904
   - 10 mm clean: 1,966
   - 20 mm clean: 4,607
   - 40 mm clean: 2,426
   - 6F2 capping: 3,161
   - Scalpings: 3,120
   - Type 1 sub-base: 6,305
7. Tonnes sold in January 2026 by Monday to Sunday week of the day weighed, nearest tonne:
   - 1 to 4 January: 529
   - 5 to 11 January: 5,855
   - 12 to 18 January: 5,957
   - 19 to 25 January: 5,732
   - 26 to 31 January: 6,417
