"""submission.md, drafted from figures.json: the tags, the call, the critical components, at most eight steps and
the deliverable answers grouped by file."""
import os


def write(task_dir, f):
    L = f["lines"]
    rows = []
    for permit in sorted(L):
        r = L[permit]
        rows.append("   - %s, %s: permitted %d l/s, passes forward %d l/s, met the permit %s, %d spills, %s hours of "
                    "discharge, monitored %s per cent" % (permit, r["overflow"], r["pff"], r["delivered"], r["met"],
                                                          r["spills"], r["hours"], r["operational"]))
    md = []
    md.append("## Tags\n")
    md.append("- **Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (storm overflow "
              "permit compliance at sewage pumping stations).")
    md.append("- **Analytical objective:** Anomaly Detection & Diagnostics.\n")
    md.append("## 1. Final Recommendation\n")
    md.append("**Self-report the %s (permit %s, condition 2.3.1): it discharged in 2026 while its station passed "
              "forward %d l/s against the %d l/s its permit sets.** Not none: Gallowfen's running pump is rated at "
              "%s l/s but delivers %d. Not %s, whose dry-day discharges came with the station pumping at its full "
              "rate. Not %s, the most frequent spiller (%d spills), whose station passes forward more than its "
              "permitted flow.\n" % (f["call"], f["call_permit"], f["call_delivered_ls"], f["call_pff_ls"],
                                     f["call_rated_ls"], f["call_delivered_ls"], f["dry_day_station"], f["high_spiller"],
                                     f["high_spiller_spills"]))
    md.append("## 2. Critical Components\n")
    md.append("1. Gallowfen's permit requires a pass forward flow of **%d l/s** before its overflow may discharge." % f["call_pff_ls"])
    md.append("2. Gallowfen's pumps deliver **%d l/s**, %d per cent of that flow, against a rated duty of **%s l/s**."
              % (f["call_delivered_ls"], f["call_share_of_pff_pct"], f["call_rated_ls"]))
    md.append("3. Every other pumping station passes forward at least its permitted flow; the closest is **%s at %d l/s "
              "against %d l/s**.\n" % (f["tightest_station"], f["tightest_delivered_ls"], f["tightest_pff_ls"]))
    md.append("## 3. Step-by-Step Solution\n")
    md.append("1. Took each overflow's pass forward flow from condition 2.3.1 in "
              "`registers/wastewater_discharge_consents_2026.csv`: Gallowfen %d l/s." % f["call_pff_ls"])
    md.append("2. From `registers/marsh_wolds_wastewater_assets.xlsx`, took each wet well's plan area from its internal "
              "dimensions and the volume between the duty pump's start and stop levels.")
    md.append("3. From `pump_event` in `telemetry/marsh_wolds_sps_telemetry_2026.sqlite`, exact duplicates dropped, took "
              "each clean cycle's delivered rate as that volume over the pump-on time plus that volume over the "
              "pump-off time before it, and each station's median: Gallowfen %d l/s against its %d." % (
                  f["call_delivered_ls"], f["call_pff_ls"]))
    md.append("4. Compared every station's delivered rate with its permitted flow: Gallowfen alone falls short, the "
              "closest of the rest %s at %d against %d." % (f["tightest_station"], f["tightest_delivered_ls"],
                                                            f["tightest_pff_ls"]))
    md.append("5. Mapped each retired serial in `edm/edm_monitor_list_2027-01-15.csv` to the overflow whose `alarm` "
              "OVERFLOW OPERATING periods its discharges coincide with, among the stations whose register monitor was "
              "installed in the week before it retired, and pooled every serial per overflow.")
    md.append("6. On each overflow's discharges from every serial, starts and ends converted from UK local time and "
              "overlapping periods counted once, applied WW-ENV-PR-014's 12/24 count and summed the hours, split by "
              "local month for the chart.")
    md.append("7. Monitoring percentage: for each local day the most hours any of the overflow's monitors reported in "
              "`edm/edm_monitor_daily_status_2026.csv`, summed over 2026, over 8,760 hours.")
    md.append("8. Self-reported %s, %d spills and %s hours of discharge in 2026.\n" % (
        f["call"], f["call_spills_12_24"], f["call_hours"]))
    md.append("## 4. Deliverable Answers\n")
    md.append("### overflow_self_report_2026.docx\n")
    md.append("1. Overflow and permit: %s, permit %s, condition 2.3.1." % (f["call"], f["call_permit"]))
    md.append("2. Pass forward flow the permit sets: %d l/s." % f["call_pff_ls"])
    md.append("3. Flow the station was passing forward while it spilled: %d l/s.\n" % f["call_delivered_ls"])
    md.append("### overflow_return_lines_2026.csv\n")
    md.append("1. One line per storm overflow, in permit order:")
    md.extend(rows)
    md.append("")
    md.append("### spill_hours_by_month_2026.svg\n")
    md.append("1. A grid of every overflow's hours of discharge in each month of 2026 (UK local time, every monitor "
              "that watched it), each cell labelled; the largest total %s, %s hours." % (
                  f["chart_top_overflow"], f["chart_top_hours"]))
    open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
