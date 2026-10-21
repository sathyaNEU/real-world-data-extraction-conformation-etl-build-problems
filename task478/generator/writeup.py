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
               "Kerbline's detections linked across passes and units, integrated with the fleet's segment traversals, the "
               "unit register, the review queue and the road inventory into a completed count of potholes per maintenance "
               "section, the potholes no unit recorded estimated from how often a second unit finds what a first one "
               "found).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Give dedicated spring patching crews to seven of the fourteen sections: %s.**" % join(des))
    out.append("Their state roadway held %s potholes per ten lane-miles in March 2027 against the program's %.1f line; the "
               "highest of the other seven is %s at %d. Not Carrow Point and Elmscourt alone, which counting every pass over "
               "a segment as an independent chance gives: a unit that recorded a pothole recorded it again on %.1f per cent "
               "of its later days, so a segment driven many times by one unit had that one unit's chance, and a second unit "
               "finds %.1f per cent of what another found.\n"
               % (rates, f["line"], c["highest_below"]["name"], c["highest_below"]["rate"], c["repeat_pct"],
                  c["find_rate_pct"]))
    out.append("## 2. Critical Components\n")
    out.append("1. The program's roadway is **{:,.1f}** lane-miles, the 2026 inventory less the five segments turned back "
               "on 15 March, holding **{:,}** confirmed potholes.".format(c["lane_miles"], c["confirmed"]))
    out.append("2. Potholes per ten lane-miles, completed over the distinct units that drove each segment: %s.\n"
               % ", ".join("%s **%d**" % (n, x["rate"]) for n, x in secs))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Took the roadway from road_inventory_2026.csv less the five segments in route_turnback_notice_2027-03.pdf, "
        "lane-miles as length times through lanes (program section 2): {:,.1f} lane-miles.".format(c["lane_miles"]),
        "Kept the potholes confirmed in kerbline_qa_review_2027-03.xlsx, folding each defect rejected as a duplicate into "
        "the defect it names, and placed each on its 2026 segment from its detections' road_ref and road_mp in "
        "kerbline_detections_2027-03.csv through road_inventory_crosswalk_2025_2026.csv: {:,} potholes.".format(c["confirmed"]),
        "Listed the units that drove each segment in March, district local time, from fleet_camera_traversals_2027-03.csv "
        "joined by vehicle to kerbline_unit_register.xlsx on its install and removal dates; every segment had at least one.",
        "Read the per-unit find rate from the potholes on segments two or more units drove: of the other units that drove "
        "a found pothole's segment, %.1f per cent found it, against %.1f per cent of a finding unit's own later days."
        % (c["find_rate_pct"], c["repeat_pct"]),
        "Counted each confirmed pothole as one over one minus %.3f to the power of the distinct units that drove its "
        "segment, and divided each section's total by its lane-miles over ten." % c["miss_rate"],
        "Cold patches from mms_cold_patch_orders_2027-03.csv, COMPLETE orders finished in March: an ext_ref missing from "
        "Kerbline's exports, a number from before Kerbline's 17 March renumbering, taken to the confirmed defect at the "
        "same route and milepost in the review export, each defect the reviewer rejected as a duplicate taken to the "
        "defect it names, so each pothole counts once; a multi-line order carrying the same pounds on every line counted "
        "once.",
        "Camera miles: dropped each traversal overlapping the same vehicle's earlier-numbered traversal of the same "
        "segment (the provider's re-run of 12 to 13 March), kept installed units' March passes on the program's roadway "
        "and summed inventory lengths.",
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
    out.append("3. Potholes cold patched in March, a pothole patched more than once counting once:")
    for n, x in secs:
        out.append("   - %d %s: %d" % (x["section"], n, x["cold_patched"]))
    out.append("4. Pounds of cold mix those patches used:")
    for n, x in secs:
        out.append("   - %d %s: {:,}".format(x["cold_mix_lb"]) % (x["section"], n))
    out.append("5. Miles the pilot's camera units were driven on the program's roadway in March, each pass at its "
               "segment's inventory length:")
    for n, x in secs:
        out.append("   - %d %s: {:,}".format(x["camera_miles"]) % (x["section"], n))
    out.append("")
    out.append("### tamsett_spring_patching_task_orders_2027.pdf\n")
    out.append("1. Bar chart on page 1 of every section's potholes per ten lane-miles against the program's %.1f line, the "
               "seven designated sections in dark blue." % f["line"])
    text = "\n".join(out) + "\n"
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write(text)
    return text


if __name__ == "__main__":
    print(main())
