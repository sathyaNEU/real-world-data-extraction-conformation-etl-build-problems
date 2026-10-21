"""submission.md, every figure read from generator/figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    secs = sorted(f["sections"].items(), key=lambda kv: kv[1]["section"])
    des = f["call"]["designated"]
    c = f["components"]
    rates = ", ".join("%d" % f["sections"][n]["rate"] for n in des[:-1]) + " and %d" % f["sections"][des[-1]]["rate"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** General Statistics & Data Science (data integration: a state DOT district's camera pilot, "
               "Kerbline's detections linked into defects and reviewed, integrated with the fleet's segment traversals, "
               "the unit register and the road inventory into a completed count of potholes per maintenance section, "
               "the potholes no unit recorded estimated with each kind of vehicle, not each unit, as one capture "
               "occasion).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Give dedicated spring patching crews to seven of the fourteen sections: %s.**" % join(des))
    out.append("Their state roadway held %s potholes per ten lane-miles in March 2027 against the program's %.1f line; the "
               "highest of the other seven is %s at %d. Not %s, which counting every installed unit as an independent "
               "chance gives: two units on the same kind of vehicle record %.1f per cent of the same potholes against "
               "%.1f per cent across kinds, so a segment's chances are its kinds of vehicle. Not %s, which counting "
               "every pass gives.\n"
               % (rates, f["line"], c["highest_below"]["name"], c["highest_below"]["rate"], join(f["units"]["designated"]),
                  c["same_fleet_pct"], c["cross_fleet_pct"], join(f["default"]["designated"])))
    out.append("## 2. Critical Components\n")
    out.append("1. The program's roadway is **{:,.1f}** lane-miles, the 2026 inventory less the five segments turned back "
               "on 15 March, holding **{:,}** confirmed potholes.".format(c["lane_miles"], c["confirmed"]))
    out.append("2. Potholes per ten lane-miles, completed over the distinct fleet groups that drove each segment: %s.\n"
               % ", ".join("%s **%d**" % (n, x["rate"]) for n, x in secs))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Took the roadway from road_inventory_2026.csv less the five segments in route_turnback_notice_2027-03.pdf, "
        "lane-miles as length times through lanes (program section 2): {:,.1f} lane-miles.".format(c["lane_miles"]),
        "Kept the potholes confirmed in kerbline_qa_review_2027-03.xlsx, folding each defect rejected as a duplicate into "
        "the confirmed defect nearest it on its route, and placed each on its 2026 segment from its detections' road_ref "
        "and road_mp in kerbline_detections_2027-03.csv through road_inventory_crosswalk_2025_2026.csv: {:,} potholes."
        .format(c["confirmed"]),
        "Listed the units that drove each segment in March, district local time, from fleet_camera_traversals_2027-03.csv "
        "joined by vehicle to kerbline_unit_register.xlsx on its install and removal dates, and their fleet groups.",
        "Read the recaptures: where two units drove a segment, the second recorded %.1f per cent of the first's potholes "
        "when both were in one fleet group and %.1f per cent across groups, so each fleet group that drove a segment is "
        "one capture occasion." % (c["same_fleet_pct"], c["cross_fleet_pct"]),
        "Read the per-group find rate from the potholes on segments two or more groups drove: %.1f per cent." % c["find_rate_pct"],
        "Counted each confirmed pothole as one over one minus %.3f to the power of the distinct fleet groups that drove "
        "its segment, and divided each section's total by its lane-miles over ten." % c["miss_rate"],
        "Pounds of cold mix from mms_cold_patch_orders_2027-03.csv, COMPLETE orders finished in March: a multi-line order "
        "carrying one figure on every line counted it once where the figure is more than any single-line order used on a "
        "pothole of its lines' severities in the detections (the mobile app's order total; an ext_ref Kerbline no longer "
        "carries taken to the defect at the same route and milepost in the review export), and summed its lines "
        "otherwise.",
        "Designated the sections at %.1f or more: %s." % (f["line"], join(des)),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### tamsett_spring_patching_sections_2027.csv\n")
    out.append("1. Potholes per ten lane-miles of state roadway, March 2027, whole numbers:")
    for n, x in secs:
        out.append("   - %d %s: %d" % (x["section"], n, x["rate"]))
    out.append("2. Dedicated crew:")
    for n, x in secs:
        out.append("   - %d %s: %s" % (x["section"], n, x["crew"]))
    out.append("3. Pounds of cold mix the section's March cold patches used:")
    for n, x in secs:
        out.append("   - %d %s: {:,}".format(x["cold_mix_lb"]) % (x["section"], n))
    out.append("")
    out.append("### tamsett_spring_patching_task_orders_2027.pdf\n")
    out.append("1. Bar chart on page 1 of every section's potholes per ten lane-miles against the program's %.1f line, the "
               "seven designated sections in dark blue." % f["line"])
    text = "\n".join(out) + "\n"
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write(text)
    return text


if __name__ == "__main__":
    print(main())
