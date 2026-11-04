"""submission.md, drafted from figures.json and nothing else."""
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MONTHS = ("April", "May", "June", "July")
SAMPLED = ("Tessel River", "Fennick Creek", "Oxley Creek", "Dunmore Creek")


def fmt(n):
    return "{:,}".format(int(n))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    per = F["per_sub"]
    loads = F["loads_kg"]
    lm = F["loads_month_kg"]
    pac = F["pac_lb"]
    others = [k for k in per if k != F["call"]]
    sf = dt.date.fromisoformat(F["strat_first"])
    sl = dt.date.fromisoformat(F["strat_last"])
    off = F["dun_offsets_ft"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences, pollution source attribution.  ")
    L.append("**Analytical objective:** Root-Cause Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Place the 2027 atrazine cost-share program in the %s sub-watershed.** %s's atrazine was behind all %d of "
             "the 2026 season's days on which the raw water was above the 3.0 ug/L trigger, and no other "
             "sub-watershed's was behind any. Not the Tessel River, which carried the most atrazine past its station "
             "in every month from April to July but whose warm water spread over the stratified lake's surface layer, "
             "above the intake; not Oxley or Dunmore Creek, whose water also entered above the intake's layer; not "
             "Ladd Branch, whose water ran to the bottom.\n" % (F["call"], F["call"], F["call_days"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Days in the 15 April to 31 October season with the raw-water result above 3.0 ug/L: **%d**."
             % F["days_total"])
    L.append("2. The lake was stratified at the dam from **%s** to **%s**, and on every day above the trigger %s was "
             "the only sub-watershed whose water had entered the lake within the intake's layer." %
             (sf.strftime("%-d %B"), sl.strftime("%-d %B"), F["call"]))
    L.append("3. Days above the trigger each sub-watershed's atrazine caused: %s **%d**; %s.\n"
             % (F["call"], F["call_days"], "; ".join("%s **%d**" % (k, per[k]) for k in others)))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took each day's raw-water result from raw_water_log_2026-01-01_to_2026-05-26.csv and "
             "LIMS_raw_water_2026-05-20_to_2026-10-31.xlsx as SOP-WQ-07 2.3 sets it (the GC/MS confirmation where "
             "one was run, otherwise the ELISA screen) and counted the season's days above 3.0 ug/L (plan 5.2): %d."
             % F["days_total"])
    L.append("2. Built the lake's daily mean temperature profile from MERRIN_BUOY_Hourly_2026.dat (logger clock on CST; "
             "sensor depths from buoy_service_log_2026.csv, 0.5 to 15.5 m before the 10 June re-hang and 1 to 16 m "
             "after) and the intake's daily depth below the surface from the pool elevation in "
             "merrin_dam_daily_log_2026.xlsx (NGVD29) less the intake centreline on intake_tower_record_drawing_S-4.pdf "
             "(829.24 ft NAVD88, NGVD29 plus 0.24 ft): stratified from %s to %s, the intake %.1f to %.1f m down in "
             "June and July." % (sf.strftime("%-d %B"), sl.strftime("%-d %B"), F["intake_depth_m"][0],
                                 F["intake_depth_m"][1]))
    L.append("3. Placed each tributary's water each day at the depth where that day's profile was as warm as the "
             "tributary's daily mean temperature (TR-01, FC-02 and OC-03 exports on local time; the DC-04 and LB-05 "
             "loggers on UTC), and on each day above the trigger listed the sub-watersheds whose water had entered "
             "within two metres of the intake's depth since the lake stratified, looking back up to 30 days: %s "
             "alone on all %d days, so without its atrazine the raw water keeps only the lake's spring residue and "
             "each day counts for %s and no other sub-watershed (plan 5.1)." % (F["call"], F["days_total"], F["call"]))
    L.append("4. For the station atrazine, took each bottle's value from SHL_EDD_brennick_source_water_2026.csv "
             "(Client_Sample_ID without its hyphens) where the State laboratory ran it and from "
             "city_lab_ELISA_tributaries_2026.xlsx otherwise, not detected as zero (plan 3.2); a routine grab's time "
             "is its logged time in field_sampling_log_2026.xlsx, and a storm bottle's is its sample time in "
             "autosampler_run_logs_2026.csv, each carousel's bottles in number order matched to the positions that "
             "drew a sample (NO LIQUID positions hold no bottle).")
    L.append("5. Took DC-04 discharge from gage height through the rating in force in "
             "DC-04_LB-05_ratings_and_field_visits.xlsx (rating 2 from 2 June 11:30 CDT), gage height being the "
             "logger's level plus the staff-gage offset from the field visits: %.2f ft until %s, when "
             "the logger's level steps up %.2f ft between two readings with no rain, and %.2f ft after; then summed "
             "each 15-minute discharge times the concentration interpolated linearly between the samples either side "
             "of it, by local month from 1 April to 31 July: the monthly figures for atrazine_sources_2026.xlsx in "
             "section 4, Ladd Branch not sampled." % (off[0], dt.datetime.fromisoformat(F["dun_step_at"]).strftime("%H:%M on %-d %B"), F["dun_step_ft"], off[1]))
    L.append("6. For the carbon, applied each dose setpoint in scada_pac_dose_setpoint_2026.csv (UTC) to the plant "
             "day's raw water pumped in daily_operating_report_2026.xlsx (06:00 to 06:00 next day) at 8.34 lb per "
             "million gallons per mg/L (SOP-WQ-07 3.2), minute by minute, over the minutes the feeder in "
             "scada_alarm_event_history_2026.csv was running with carbon: stopped from a MOTOR OVERLOAD TRIP until "
             "its next RUN STATUS ON, and feeding nothing from a HOPPER LEVEL LOW-LOW NO FEED alarm to its return: "
             "%s lb in May, %s in June, %s in July and %s in August." % (fmt(pac["May"]), fmt(pac["June"]),
                                                                       fmt(pac["July"]), fmt(pac["August"])))
    L.append("7. %s gets the program: %d days of %d, every other sub-watershed none.\n"
             % (F["call"], F["call_days"], F["days_total"]))
    L.append("## 4. Deliverable Answers\n")
    L.append("### cost_share_placement_2027.docx\n")
    L.append("1. The 2027 cost-share program goes to the %s sub-watershed." % F["call"])
    L.append("2. Days above the trigger each sub-watershed's atrazine caused:")
    for k in [F["call"]] + others:
        L.append("   - %s: %d" % (k, per[k]))
    L.append("")
    L.append("### atrazine_sources_2026.xlsx\n")
    L.append("1. Atrazine past each sub-watershed's station by month, 2026, kilograms:")
    for k in SAMPLED:
        L.append("   - %s: %s" % (k, ", ".join("%s %s" % (m, fmt(lm[k][m])) for m in MONTHS)))
    L.append("   - Ladd Branch: not sampled")
    L.append("2. Powdered activated carbon fed, pounds:")
    for m in ("May", "June", "July", "August"):
        L.append("   - %s: %s" % (m, fmt(pac[m])))
    L.append("")
    L.append("### raw_water_atrazine_2026.png\n")
    L.append("1. The daily raw-water result from 15 April to 31 October 2026 against the 3.0 ug/L trigger line, the %d "
             "days above it marked." % F["days_total"])
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
