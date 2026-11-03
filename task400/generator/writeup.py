"""submission.md, drafted from figures.json's values only."""
import golden as G

MONTHS = {7: "July", 8: "August", 9: "September", 10: "October"}


def extra_figures(P, resp):
    F = {}
    rr = G.route_rates(P)
    for rt, key in (("S-ORE>ROM", "sore"), ("N-WST>NWD", "nwst")):
        for y in (2025, 2026):
            n, d = rr[(rt, y)]
            F["rate_%s_%d" % (key, y)] = round(1000.0 * n / d, 1)
    return F


def submission(F):
    L = []
    L.append("# task400 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Human Factors & Ergonomics, safety incident and error analysis (vehicle interaction incidents "
             "between haul trucks and other vehicles at an open-pit iron ore mine).  ")
    L.append("**Analytical objective:** Root-Cause Analysis (the driver of the 2026 rise in vehicle interaction incidents, "
             "and the programme the site's review terms assign to it).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Mount Bracken should fund programme C, the collision avoidance alerting review on the haul truck units, "
             "for 2027.**\n")
    L.append("Vehicle interaction incidents rose from %d in July to October 2025 to %d in July to October 2026, and the "
             "one change in operator behaviour that the records show is in the response to critical alerts on units "
             "running firmware 5.0.2: while it went on, the same crews slowed for about %d per cent of critical alerts from "
             "units still on 4.3 and about %d per cent from units already on 5.0.2, and from July critical alerts nobody "
             "slowed for ran at more than five times their 2025 level. Not B: the North ramp junction has the most "
             "incidents, but incidents per truck shift rose about fourfold on the South pit ore route, which never passes "
             "the junction. Not A: the same operators kept slowing on 4.3 units. Not D or E: the fall in slowing came with "
             "the firmware on day shifts as on nights, and the crusher pad's share of incidents fell.\n"
             % (F["vi_jul_oct_2025"], F["vi_jul_oct_2026"], F["resp_window_v43_pct"], F["resp_window_v5_pct"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Vehicle interaction incidents, July to October 2025: **%d**" % F["vi_jul_oct_2025"])
    L.append("2. Vehicle interaction incidents, July to October 2026: **%d**" % F["vi_jul_oct_2026"])
    L.append("3. Firmware 5.0.2 went on the haul truck units between **%s**" % F["rollout_days"])
    L.append("4. Critical alerts followed by the truck slowing, 2 to 23 June 2026, to the nearest 5 per cent: **%d%%** on "
             "4.3 units, **%d%%** on 5.0.2 units\n" % (F["resp_window_v43_pct"], F["resp_window_v5_pct"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Counted the entries in incident_register_2025-01_2026-10.xlsx classified VI-COL or VI-SPI by month of "
             "occurrence (vi_review_terms_2026.docx 2.1): %d in July to October 2025 and %d in July to October 2026, the "
             "rise starting in June 2026." % (F["vi_jul_oct_2025"], F["vi_jul_oct_2026"]))
    L.append("2. Placed each incident on the dispatch shift its haul truck (the first vehicle named) was working in "
             "dispatch_shift_summary_2025-2026.csv: per 1,000 truck shifts in July to October the S-ORE>ROM route went from "
             "%.1f to %.1f and N-WST>NWD, the route through the North ramp junction, from %.1f to %.1f, so the junction's "
             "extra traffic does not carry the rise." % (F["rate_sore_2025"], F["rate_sore_2026"], F["rate_nwst_2025"],
                                                        F["rate_nwst_2026"]))
    L.append("3. Put each CRIT alert in cas_alert_events_2025-01_2026-10.parquet on its truck through the Devices sheet of "
             "cas_device_register_2026-10-31.xlsx (installed and removed dates), took the unit's firmware at onset from "
             "the Firmware sheet, moved onset from UTC to Western Australian time (UTC+8) and matched the CAS_CRITICAL "
             "window in fms_event_windows_2025-2026.parquet that opened on the same truck within 3 seconds after onset.")
    L.append("4. Counted an alert as acted on where the speed at t_offset_s 6 was at least 6 km/h below the speed at 0 "
             "(any drop of 4 to 10 km/h read at 4, 6 or 8 seconds gives the same figures): between 2 and 23 June "
             "2026, with both firmwares running, %d per cent of critical alerts on 4.3 units against %d per cent on 5.0.2 "
             "units, to the nearest 5 per cent." % (F["resp_window_v43_pct"], F["resp_window_v5_pct"]))
    L.append("5. For the gate figures, read only IN reads in pit_gate_reads_2026-07_2026-10.csv and counted an NG-2 read "
             "2 to 13 seconds after an NG-1 read as the same entry whatever plate each reader returned (the two North gate "
             "readers read one vehicle seconds apart, and no two vehicles pass a gate within 16 seconds); a trip with an "
             "empty cas_tag is one with no tag detected.")
    L.append("6. For the ramp figures, took each OVERSPEED window on NRP or SRP for a DT truck in "
             "fms_event_windows_2025-2026.parquet, joined a window to the run before it only where it opens on the sample "
             "that closed the same truck's last window on that ramp (ten seconds later) with the truck still over the limit "
             "at that sample, took each run's highest speed, and compared it with the limit in force that day in "
             "haul_road_speed_limits.csv.")
    L.append("7. The response to critical alerts is the only measured change in operator behaviour, it follows the "
             "firmware rather than the crews, and critical alerts nobody slowed for rose more than fivefold in July to "
             "October against almost fourfold for the incidents; programme C answers the alerts (vi_review_terms_2026.docx "
             "section 4): fund C.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### vi_programme_paper_2027.docx\n")
    L.append("1. Call: fund programme C, the collision avoidance alerting review on the haul truck units, for 2027")
    L.append("2. Vehicle interaction incidents: %d in July to October 2026, %d in July to October 2025"
             % (F["vi_jul_oct_2026"], F["vi_jul_oct_2025"]))
    L.append("3. Bar chart of vehicle interaction incidents by month from January 2025 to October 2026, each bar labelled "
             "with its count\n")
    L.append("### vi_workings_2026.xlsx\n")
    L.append("1. Light-vehicle trips into the pits, and trips by vehicles whose collision avoidance tag the gate did not "
             "detect:")
    for m in (7, 8, 9, 10):
        L.append("   - %s 2026: %s trips, %d with no tag detected" % (MONTHS[m], "{:,}".format(F["trips_%02d" % m]),
                                                                    F["trips_notag_%02d" % m]))
    L.append("2. Haul truck times over the speed limit in force on each pit ramp, and how many peaked more than 5 km/h "
             "over it:")
    for seg, name in (("NRP", "North pit ramp"), ("SRP", "South pit ramp")):
        for m in (7, 8, 9, 10):
            L.append("   - %s, %s 2026: %d times, %d more than 5 km/h over" % (name, MONTHS[m], F["os_%s_%02d" % (seg, m)],
                                                                            F["os5_%s_%02d" % (seg, m)]))
    return "\n".join(L) + "\n"
