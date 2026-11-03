# task276 submission

## Tags

**Domain:** Urban & Regional Science (network analysis: the road-user delay each shortlisted level crossing's barrier closures impose on the roads through it).
**Analytical objective:** Descriptive & Distribution Analysis (how school-day morning closure delay is distributed across the programme's shortlisted crossings, choosing the 2027 replacement, with each crossing's closure frequency, fault-held closure hours and heavy goods vehicle share).

## 1. Final Recommendation

**Replace Mill Lane in 2027.**

Its closures cost road users **10,000 vehicle-hours** on school-day mornings 07:00 to 10:00 in 2025/26, against Station Road's **7,000**, a gap of **3,000**. Not Station Road, which leads only when every held queue leaves at the road's own saturation flow once the barriers rise (7,000 against Mill Lane's 5,000); Mill Lane's queues can only leave in the greens of the river bridge's shuttle signals 42 metres beyond the crossing.

## 2. Critical Components

1. Mill Lane's section between its count sites holds the shuttle-signalled single-track bridge: a **100**-second cycle, **32** seconds of westbound and **48** of eastbound green, **7** vehicles of storage between the bridge stop line and the barriers.
2. Delay by crossing: Mill Lane **10,000**; Station Road **7,000**; Moor Road **4,000**; Long Drove **4,000**; Church Lane **2,000**; Common Road **2,000**.
3. No other shortlisted crossing has a control between its count sites.

## 3. Step-by-Step Solution

1. Paired each LOWERED event in barrier_events_2025_26.csv with the next RAISED event per crossing, dropping repeats of the same event within three seconds, and converted UTC to UK local time.
2. Took each crossing's school days from term_dates_2025_26.xlsx for its county in crossing_register_2025.pdf, weekdays in term outside half terms and bank holidays (crossing_programme_2027.docx 3.3).
3. Spread each quarter hour's vehicles in approach_counts_2025_26.csv evenly across it at the count sites network_register_2026.xlsx gives each crossing (road_delay_appraisal_conventions.pdf 3).
4. Matched each crossing to its node in network_nodes.csv by grid reference and walked network_links.csv between its two count sites: only Mill Lane's section holds a signal site, SS 2207, whose single-track link is the bridge, 42 metres from the crossing.
5. Replayed every school morning from 06:00, each vehicle passing the barriers when raised at 1,800 vehicles an hour per lane and, at Mill Lane, the bridge stop line only in its direction's green at the register's 1,800, with 7 vehicles of storage between the two stop lines; delay is each vehicle's exit time against the same morning with no closures (crossing_programme_2027.docx 3.2), summed over vehicles counted 07:00 to 10:00.
6. Fault-held hours: the barrier closures during which a BFR, ODF or PWR fault in lx_work_orders_2025_26.csv was reported (the renewed Long Drove machine, LXB/5203, matched by the closure held down at that minute) or which ended at a signaller's reset in signaller_occurrences_2025_26.xlsx, summed over the year.
7. Heavy goods share: the veh_hgv column over veh_total for the quarter hours between 07:00 and 10:00 on school days, both approaches; at the QT-40 sites, and at an RX-5 site's rows before its counter's install date, the column is a whole-number percentage of the interval's vehicles, converted at veh_hgv times veh_total over 100.
8. Mill Lane leads at 10,000 vehicle-hours against Station Road's 7,000: replace Mill Lane in 2027.

## 4. Deliverable Answers

### crossing_delay_2025_26.xlsx

1. Each shortlisted crossing, ranked by delay: delay to the nearest thousand vehicle-hours, closures begun between 07:00 and 10:00 per school morning, hours barriers were down 1 September 2025 to 31 August 2026 in closures a fault held down, heavy goods vehicles as a share of vehicles counted on school-day mornings:
   - Mill Lane: 10,000 vehicle-hours, 11.8 closures per school morning, 4.0 fault-held hours, 7.2% heavy goods vehicles
   - Station Road: 7,000 vehicle-hours, 11.8 closures per school morning, 3.3 fault-held hours, 5.6% heavy goods vehicles
   - Moor Road: 4,000 vehicle-hours, 11.8 closures per school morning, 1.8 fault-held hours, 6.7% heavy goods vehicles
   - Long Drove: 4,000 vehicle-hours, 8.9 closures per school morning, 2.4 fault-held hours, 8.2% heavy goods vehicles
   - Church Lane: 2,000 vehicle-hours, 14.8 closures per school morning, 3.6 fault-held hours, 4.8% heavy goods vehicles
   - Common Road: 2,000 vehicle-hours, 17.7 closures per school morning, 3.7 fault-held hours, 6.1% heavy goods vehicles

### crossing_choice_2027.docx

1. Recommendation: replace Mill Lane in 2027.
2. Runner-up: Station Road.
3. Gap between them: 3,000 vehicle-hours.
