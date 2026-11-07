## Tags

**Domain:** General Statistics & Data Science, exploratory data analysis and distribution assessment (a Spanish parcel carrier's outbound cage audits and the one sortation engineering survey slot before the 2026 peak).  
**Analytical objective:** Anomaly Detection & Diagnostics (whose sorter causes the audited damage excess, and what its repairs stop over the peak).

## 1. Final Recommendation

**Send the sortation engineering survey to Ribarroja del Turia; its repairs would stop about 800 damaged parcels a week over peak weeks 48 to 52.** At equal load in the cage its sorter damages about 50 parcels per 10,000 inspected more than the network does, and no other hub comes within 30 of it. Not Zaragoza Plaza, which leads on audited damage because cartons loaded on top of its cages crush the parcels beneath, and sits below the network at equal load. Not Dos Hermanas, whose excess is the same crush under cases loaded part way through the cage.

## 2. Critical Components

1. Each audited parcel's load is the DWS weight of the parcels scanned into its cage after it, read from the cage build log; at equal load Zaragoza Plaza sits below the network and Dos Hermanas close to it.
2. Ribarroja's own sorter damage is **50 per 10,000 parcels inspected** above the network at equal load.
3. Ribarroja's planned parcels a week over peak weeks 48 to 52 average **161,620**.
4. The survey's repairs stop **800 damaged parcels a week** over the peak.

## 3. Step-by-Step Solution

1. Took the routine audits in audit_headers_q3_2026.csv and their OK and DAMAGED lines in audit_findings_q3_2026.parquet (any damage code, old or new list), per the audit procedure.
2. Joined each parcel's first DWS weighing (dws_induction_q3_2026.parquet, grams), shape and size, and its service and fragile flag from shipment_lines_q3_2026.parquet, by barcode.
3. Ordered each cage's LOAD scans in cage_build_log_q3_2026.parquet and summed the DWS weights of the parcels scanned after each parcel: its load on top.
4. Fitted the six-hub logistic expectation on shape, log weight, fragility, service and the heavy-carton flag with the load in each form tried (steps at several weights, linear, log, cartons above, heaviest parcel above, with and without packaging terms, with the position and cage-weight terms added) and kept the lowest BIC, per the programme: 60 kg or more on top, by packaging; Ribarroja 50 per 10,000 above, no other hub within 30 of it.
5. Applied that rate to Ribarroja's mean planned parcels over weeks 48 to 52 in peak_plan_2026.xlsx (161,620): 800 damaged parcels a week.
6. Claims, per note CS-FIN 07: charged each parcel's first case in damage_claims_cases_2026-10-23.csv approved by 20 October to the hub and sorting night of its first SORT in tracking_events_claimed_parcels.parquet and counted a flat-rate account's case as its damaged cartons, the approved amount over the account's rate in flat_rate_damage_terms.xlsx; the euros paid by 20 October are the transfers in claims_transfers_2026.xlsx by value date, net of returned ones, and the card refund in card_refunds_settlement_2026-07-01_2026-10-22.csv of each private sender's approved amount made on or after its decision.
7. Stoppages, per standard ENG-11: took the PLC's STOP to RUN spells in sorter_event_log_q3_2026.csv, started each PLC RUN no STOP precedes at the safety system's TRIP before it, and added each corrective order in sorter_work_orders_q3_2026.xlsx that matches no logged spell.
8. Recommended the survey for Ribarroja del Turia.

## 4. Deliverable Answers

### survey_case_note.pdf

1. Survey hub: Ribarroja del Turia.
2. Damaged parcels a week its repairs stop over the peak: 800.
3. Bar chart of each hub's audited damage per 10,000 parcels inspected beside the part its own sorter accounts for (50 at Ribarroja, none at the other hubs) on page 1.

### hub_damage_q3_2026.xlsx

1. Damaged parcels with an approved claim, by hub:
   - Zaragoza Plaza: 1,267
   - Ribarroja: 888
   - Dos Hermanas: 967
   - San Fernando: 1,449
   - El Prat: 1,081
   - Basauri: 464
2. Euros paid on them, by hub:
   - Zaragoza Plaza: EUR 52,428
   - Ribarroja: EUR 35,436
   - Dos Hermanas: EUR 34,581
   - San Fernando: EUR 57,409
   - El Prat: EUR 42,131
   - Basauri: EUR 17,349
3. Sorter stoppages, by hub:
   - Zaragoza Plaza: 158
   - Ribarroja: 178
   - Dos Hermanas: 185
   - San Fernando: 229
   - El Prat: 199
   - Basauri: 153
4. Hours stood, by hub:
   - Zaragoza Plaza: 32.0
   - Ribarroja: 39.4
   - Dos Hermanas: 34.8
   - San Fernando: 32.7
   - El Prat: 35.2
   - Basauri: 27.0
