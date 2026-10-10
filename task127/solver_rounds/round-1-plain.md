# solver round: round 1, plain

**Proxy score 47.3 / 100** (recommendation 4.0 of 35, instruction 7.0 of 7, asks 36.3 of 58). Main call missed. 3 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Place 1,170 of the 1,800 slots in 2027: North Shore 160, Valley 180, Lakes 240, Uplands 170, Riverbend 340, Pinewood 80, with 630 left unallocated.

solver: Place 1,360 of the 1,800 slots in 2027 and hold 440 unallocated. The split is Riverbend 390, Valley 290, Lakes 210, Uplands 200, North Shore 190 and Pinewood 80. Riverbend takes the most, 100 ahead of Valley. Uplands does have the most qualifying homes (about 11,500 outside its pilot area), but its pilot take-up was low (3.2%), two of its feeders are short on hosting capacity, and its meter crew has spare room for only about 7.5 meter sets a week. That limits Uplands to about 198 earned rebates in 2027, which rounds to 200.

tokens matched 8 of 10 (1,170, 1,800, 630, Place, North Shore, Valley, Lakes, Uplands, Riverbend, Pinewood)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| slot_split_board_note_2027.docx | 1 | 7 | 7 | 100% |
| slot_split_board_note_2027.docx | 2 | 2 | 4 | 50% |
| slot_split_board_note_2027.docx | 3 | 1 | 2 | 50% |
| slot_split_board_note_2027.docx | 4 | 3 | 3 | 100% |
| coop_slot_split_2027.csv | 1 | 37 | 44 | 84% |
| coop_slots_2027.svg | 1 | 7 | 13 | 54% |
| coop_slots_2027.svg | 2 | 1 | 2 | 50% |
| coop_slots_2027.svg | 3 | 0 | 0 | 0% |
| coop_slots_2027.svg | 4 | 3 | 4 | 75% |

## Solver's path

1. Programme rules s.2 and the household survey records: counted weighted qualifying homes (owner-occupied, single-family detached, heated by propane furnace, propane boiler or electric resistance, income $35,000-$149,999) by neighbourhood. Totals: North Shore 11,110; Valley 10,498; Lakes 8,794; Uplands 12,491; Riverbend 7,688; Pinewood 7,696. Table H1 counts were not used (that is the state energy office's read).
2. Pilot take-up = 2026 pilot rebated installs (412, all matched one-to-one to HPRM meter-set field orders) / qualifying homes in each co-op's pilot neighbourhood: North Shore 100/1,470 = 6.80%; Valley 88/1,318 = 6.68%; Lakes 40/1,194 = 3.35%; Uplands 32/991 = 3.23%; Riverbend 92/1,388 = 6.63%; Pinewood 60/2,096 = 2.86%.
3. Applied each rate to qualifying homes outside the pilot neighbourhoods (pilot areas are excluded in year 2). Demand: North Shore 655.8; Valley 612.9; Lakes 254.6; Uplands 371.3; Riverbend 417.6; Pinewood 160.3.
4. Joined neighbourhoods to feeders with area_feeder_map.csv and the 30 Nov hosting filings, at 5 kW per install (participation terms s.3). Capped each feeder at floor(kW/5): NS-411 35, NS-414 25, VA-205 15, VA-206 25, UP-101 36, UP-104 40, RB-501 40, PW-601 22, PW-603 18. The 2028 reinforcements were ignored. After the caps: North Shore 193.3; Valley 292.3; Lakes 254.6; Uplands 275.2; Riverbend 390.0; Pinewood 76.3.
5. Meter-set constraint (a rebate is earned only once the meter is set by 31 Dec 2027). In the field orders, the Lakes and Uplands crews (four 10-hour days a week) peak at 42 and 35 orders a week. During the July 2025 meter-exchange batch, routine orders kept normal lags while the batch drained on spare capacity. Routine non-HPRM demand is 31.5 a week at Lakes and 27.5 at Uplands, which leaves 10.5 and 7.5 spare meter sets a week. The other four crews show no ceiling.
6. Ran a day-by-day 2027 queue: HPRM arrivals follow the pilot's install-date profile (window 1 about 25%, window 2 about 75%), each set uses only spare crew capacity on Mon-Thu working days net of holidays, and the count stops at 30 Dec. Earned in 2027: Lakes about 208-209 and Uplands about 196-198.
7. Rounded each co-op to the nearest ten: Riverbend 390, Valley 290, Lakes 210, Uplands 200, North Shore 190, Pinewood 80. The sum is 1,360, under 1,800, so no proportional sharing was needed; 440 stay unallocated with the fund.
8. Installed cost: used the invoice of record (latest accepted version; 14 unaccepted v2s dropped). Counted the system price once for the IN-1126 accounting-export multi-zone invoices, where the export repeats the full system price on each indoor-head line. Kept the legitimate second 240 V circuit lines. Divided by pilot installs. Rebate share = Schedule B entitlement (plus $1,000 for income $35,000-$74,999) / installed cost.
9. Rebates paid: took ledger payments with cleared_at converted from UTC to America/Chicago and cleared before 1 Dec 2026 Central. Excluded the 24 payments in the bank's ACH return notices and counted cheque reissues as new payments. Summed by co-op and counted the distinct rebate_ids covered; every covered install was fully paid, with no partial legs.

confidence: Medium. The take-up rates, feeder caps, costs and payments come straight from the data. The Lakes and Uplands meter-set limits depend on a modelling choice: that heat-pump meter sets get only the crew capacity left after routine work, which the 2025 meter-exchange backlog supports. With heat-pump sets queued first-come-first-served alongside routine orders instead, those two co-ops would not be limited by their crews.

notes: Two results sit near a rounding boundary. Lakes (about 203-209) and Uplands (about 194-198) can move by ten depending on the assumed install-arrival profile and the routine-load rate; with the pilot's own arrival profile they come out at 210 and 200. The rebate share uses Schedule B entitlements, which match the ledger: no install was paid more than its entitlement.

### slot_split_board_note_2027.docx (solver's answers)
- 2027 slots per co-op, in tens: Riverbend 390; Valley 290; Lakes 210; Uplands 200; North Shore 190; Pinewood 80
- total placed and unallocated: 1,360 slots placed in 2027; 440 of the 1,800 left unallocated
- co-op taking the most slots and its lead over the next: Riverbend, 390 slots, 100 ahead of Valley (290)

### coop_slot_split_2027.csv (solver's answers)
- 2027 slots per co-op plus total row: North Shore 190; Valley 290; Lakes 210; Uplands 200; Riverbend 390; Pinewood 80; total 1,360 (unallocated 440, which with the total makes 1,800)
- 2026 pilot average installed cost per rebated install (whole $): North Shore $16,962; Valley $16,952; Lakes $14,786; Uplands $15,062; Riverbend $16,794; Pinewood $14,263; all co-ops $16,170
- rebate as a share of installed cost, % to 1 dp: North Shore 23.6%; Valley 23.8%; Lakes 29.7%; Uplands 29.2%; Riverbend 24.0%; Pinewood 31.7%; all co-ops 25.7%
- rebate dollars paid through 30 Nov 2026 (whole $) and pilot installs covered: North Shore $326,400 for 82 installs; Valley $295,200 for 74; Lakes $143,800 for 32; Uplands $121,000 for 27; Riverbend $290,800 for 72; Pinewood $219,000 for 49; total $1,396,200 for 336 installs
- 2026 pilot rebated installs (context): North Shore 100; Valley 88; Lakes 40; Uplands 32; Riverbend 92; Pinewood 60; total 412

### coop_slots_2027.svg (solver's answers)
- bar pairs, largest allocation first (2027 slots, 2026 pilot installs): Riverbend 390, 92; Valley 290, 88; Lakes 210, 40; Uplands 200, 32; North Shore 190, 100; Pinewood 80, 60; separate unallocated bar 440
- total placed in title: 1,360 slots placed in 2027 (of 1,800)
