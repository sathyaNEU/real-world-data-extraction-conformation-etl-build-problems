## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**List 12 hubs in the 2027 Availability Plan: Ballinkeel Main Street, Bunacurry Pier, Carrowkeel Business Park, Clonlea Leisure Centre, Derrylane Park and Ride, Glenfad Shopping Centre, Kilbeg Retail Park, Portavaddy Seafront, Rathmoy Station Road, Rossnabeg Harbour, Tobernalt Road and Tullymore Market Square.**
No HX150 hangs before day 76 after a power-up, and once the programme removes the RC50 and its monthly cabinet service, the
seven standard programme hubs' units run months between power-ups. Not the five hubs each unit's own hang rate gives,
because those rates were measured while the RC50's monthly service powered the units down; not the programme's motorway
hubs or its two rural spur hubs, whose visits every two months and frequent supply interruptions keep restarting them.

## 2. Critical Components

1. No HX150 on the record hung before day **76** after its last power-up (a pillar power-down, a power cycle or a
   repair).
2. The five hubs whose HX150 units hang two or three times a year on the record are the five where the RC50's service
   does not power them down:
   **Bunacurry Pier, Carrowkeel Business Park, Portavaddy Seafront, Rossnabeg Harbour, Tobernalt Road**.
3. Without the RC50, the seven standard programme hubs keep two planned visits a year and few supply interruptions, so
   their HX150 units fall below **99 per cent** in 2027.
4. The programme's three motorway hubs (visits every two months) and Annagh Cross and Cloonfin Crossroads (frequent
   supply interruptions) stay above **99 per cent**.

## 3. Step-by-Step Solution

1. Mapped previous and current IDs through charge_point_register.xlsx, kept one copy of each re-sent row in
   connector_status_history_2023-2026.csv and rebuilt each unit's Faulted, Unavailable and Offline spells.
2. Took each pillar power-down as the group of Offline rows, within six minutes, in which every unit at the hub that was
   up went Offline, and each hang as an HX150 Offline spell of three hours or more that a technician cleared by a power
   cycle (work_orders_2023-2026.xlsx, not a comms part replaced) or a power-down ended.
3. Read every hang with a power-up before it on record on the days since that power-up: none before day 76.
4. Built each hub's 2027 power-downs from the 2027 plan sheet of planned_maintenance_schedule.xlsx, its interruption rate
   in supply_interruptions_2023-2026.csv, the RC50's isolations where it stays and the works dates in
   asset_renewal_programme_2027.pdf.
5. Ran every 2027 HX150, new units included, through that regime with the hub's callout attendance and fault rate,
   availability per Schedule 4 of concession_agreement_schedules_4_and_6.pdf: 12 hubs have a unit below 99 per cent.
6. Counted charges in charging_sessions_2026.csv as Schedule 6 defines one (a vehicle's connection, counted once): one
   copy of each session number; a record joined to the one before it on its connector when it opens above that record's
   closing register (energy flowed while no record was open, so the vehicle never disconnected) or starts within five
   seconds of its close; the technicians' load bank tests out (records starting inside a work order's attendance window
   on the unit or a site visit at its hub, not a vehicle's connection); failed starts out; HX150 units only, begun
   January to October 2026 Irish time.
7. Took each charge's energy as Schedule 6 defines it (what the meter registered for it), from its first record's opening
   register to its last record's closing register, summed by hub in MWh. Listed the 12 hubs in the plan's letter and the
   return.

## 4. Deliverable Answers

### hub_availability_2027.csv

1. Each hub's side of the standard, its high-power charges begun January to October 2026 (whole charges) and their
   energy (MWh to one decimal), in the file's order:
   - NM103 Glenfad Shopping Centre: Yes; 3,397 charges; 109.3 MWh
   - NM104 Ardcree Services: No; 7,436 charges; 240.2 MWh
   - NM106 Ballyroe Town Park: No; 2,695 charges; 87.5 MWh
   - NM109 Kilbeg Retail Park: Yes; 1,528 charges; 49.1 MWh
   - NM112 Carrigvane Services: No; 4,653 charges; 150.3 MWh
   - NM114 Dromkeen Square: No; 2,327 charges; 75.3 MWh
   - NM117 Clonlea Leisure Centre: Yes; 2,679 charges; 86.9 MWh
   - NM118 Shanbally Community Centre: No; 2,090 charges; 68.8 MWh
   - NM119 Bunacurry Pier: Yes; 2,901 charges; 94.3 MWh
   - NM121 Tullymore Market Square: Yes; 2,997 charges; 95.3 MWh
   - NM122 Kilmeedy Church Street: No; 2,249 charges; 72.4 MWh
   - NM125 Annagh Cross: No; 1,786 charges; 57.5 MWh
   - NM127 Lismoy Services: No; 4,354 charges; 141.8 MWh
   - NM129 Corrabeg Business Park: No; 1,169 charges; 38.0 MWh
   - NM131 Portavaddy Seafront: Yes; 4,706 charges; 150.1 MWh
   - NM133 Drumtane Services: No; 6,907 charges; 223.4 MWh
   - NM135 Moyvalley Station: No; 1,230 charges; 40.3 MWh
   - NM137 Eskerbrook Shopping Centre: No; 5,317 charges; 169.9 MWh
   - NM138 Ballinkeel Main Street: Yes; 2,575 charges; 83.0 MWh
   - NM141 Knockvane Services: No; 4,525 charges; 145.6 MWh
   - NM144 Rossnabeg Harbour: Yes; 2,773 charges; 90.3 MWh
   - NM146 Rathmoy Station Road: Yes; 1,561 charges; 48.7 MWh
   - NM148 Gortnaclay Leisure Park: No; 1,259 charges; 41.3 MWh
   - NM150 Derrylane Park and Ride: Yes; 1,329 charges; 41.7 MWh
   - NM152 Lisduff Retail Park: No; 3,065 charges; 99.0 MWh
   - NM155 Carrowkeel Business Park: Yes; 2,756 charges; 88.7 MWh
   - NM158 Monaleen Services: No; 4,047 charges; 132.5 MWh
   - NM160 Templederry Green: No; 948 charges; 30.8 MWh
   - NM162 Cloonfin Crossroads: No; 2,507 charges; 81.0 MWh
   - NM166 Tobernalt Road: Yes; 2,846 charges; 92.6 MWh

### availability_plan_2027.pdf

1. The covering letter to the partnership names the 12 hubs the plan lists under Schedule 4: Ballinkeel Main Street, Bunacurry Pier, Carrowkeel Business Park, Clonlea Leisure Centre, Derrylane Park and Ride, Glenfad Shopping Centre, Kilbeg Retail Park, Portavaddy Seafront, Rathmoy Station Road, Rossnabeg Harbour, Tobernalt Road and Tullymore Market Square, with the action
   proposed at each.
