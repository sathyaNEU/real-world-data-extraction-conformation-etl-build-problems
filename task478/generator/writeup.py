"""submission.md, every figure read from generator/figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


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
    out.append("**Domain:** General Statistics & Data Science (data integration and entity resolution: a state DOT "
               "district's camera pilot, Kerbline's raw detections resolved into distinct potholes with a linkage tolerance "
               "set by each unit's positional error, measured on the surveyed utility covers, and conformed to the road "
               "inventory as at 31 March into potholes per maintenance section).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    n_out = f["call"]["of"] - f["call"]["count"]
    out.append("**Give dedicated spring patching crews to %s of the fourteen sections: %s.**" % (WORDS[len(des)], join(des)))
    out.append("Their state roadway held %s potholes per ten lane-miles in March 2027 against the program's %.1f line; the "
               "highest of the other %s is %s at %d. Not the five sections (%s) that joining every unit's detections "
               "at one distance of %d feet designates: the street sweepers' units place a pothole %d to %d feet either way "
               "against %d to %d feet for every other unit, so no one distance both keeps a sweeper's reports of one "
               "pothole together and keeps neighbouring bridge-deck potholes apart.\n"
               % (rates, f["line"], WORDS[n_out], c["highest_below"]["name"], c["highest_below"]["rate"],
                  join(f["default"]["designated"]), f["default"]["tolerance_ft"], c["sweeper_error_ft"][0],
                  c["sweeper_error_ft"][1], c["other_error_ft"][0], c["other_error_ft"][1]))
    out.append("## 2. Critical Components\n")
    out.append("1. The program's roadway is **{:,.1f}** lane-miles, the 2026 inventory less the five segments turned back "
               "on 15 March, on which the pilot's units recorded **{:,}** distinct potholes in March.".format(
                   c["lane_miles"], c["potholes"]))
    out.append("2. Potholes per ten lane-miles: %s.\n" % ", ".join("%s **%d**" % (n, x["rate"]) for n, x in secs))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Took the roadway from road_inventory_2026.csv less the five segments in route_turnback_notice_2027-03.pdf, "
        "lane-miles as length times through lanes (program section 2): {:,.1f} lane-miles.".format(c["lane_miles"]),
        "Measured each unit's milepost error from its utility_cover detections in kerbline_detections_2027-03.csv against "
        "the nearest surveyed cover on the same route in utility_cover_inventory_2026.csv: the six street sweepers' units "
        "%d to %d feet, every other unit %d to %d feet." % (c["sweeper_error_ft"][0], c["sweeper_error_ft"][1],
                                                         c["other_error_ft"][0], c["other_error_ft"][1]),
        "Sorted the March pothole detections (district local time) on each route by road_mp and joined each to the one "
        "before it when the gap was within three times the root sum of squares of the two units' errors; each run of "
        "joined detections is one pothole.",
        "Placed each pothole on the 2026 segment holding its median milepost and kept those on the roadway: {:,} "
        "potholes; divided each section's count by its lane-miles over ten.".format(c["potholes"]),
        "Pounds of cold mix from mms_cold_patch_orders_2027-03.csv, COMPLETE orders finished in March: a multi-line order "
        "carrying one figure on every line counted it once where the figure is more than any single-line order used on a "
        "pothole of its lines' severities (the severity of the ext_ref detection; the mobile app's order total), and "
        "summed its lines otherwise.",
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
               "%s designated sections in dark blue." % (f["line"], WORDS[len(des)]))
    text = "\n".join(out) + "\n"
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write(text)
    return text


if __name__ == "__main__":
    print(main())
