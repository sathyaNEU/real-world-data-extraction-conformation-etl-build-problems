"""Emits submission.md from the golden's computed values, so no figure in the write-up is typed."""
import est


def names(lst):
    return ", ".join(lst[:-1]) + " and " + lst[-1]


WORDS = {7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven"}


def write(G, path):
    secs = {s["road"]: s for s in G["sections"]}
    over = G["over"]
    det = [s for s in G["sections"] if s["basis"].startswith("section")]
    flips_in = [s["road"] for s in det if s["over"] and s["default"] <= 3.0]
    flips_out = [s["road"] for s in det if not s["over"] and s["default"] > 3.0]
    L = ["## Tags", "",
         "**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
         "## 1. Final Recommendation", "",
         "**%s of the sections the Council counted in 2025 carried more than three million vehicles and go into the noise "
         "mapping contract's scope: %s.** Not the set the permanent counters' factors give, which puts %s over the line and "
         "leaves %s under it: those sections' weeks and years follow the school, the campus, the retail park, the leisure park "
         "and the hospital at their ends, not the commuter roads the counters sit on, and each one's own year is on the signal "
         "detectors of its approach." % (WORDS[len(over)], names(over), names(flips_out), names(flips_in)), "",
         "## 2. Critical Components", ""]
    L.append("1. Over the line on their own detectors: %s." % "; ".join(
        "%s %s million" % (r, "%.1f" % secs[r]["annual"]) for r in flips_in))
    L.append("2. Under it on their own detectors: %s." % "; ".join(
        "%s %s million" % (r, "%.1f" % secs[r]["annual"]) for r in flips_out + ["Castlegate Road"]))
    L.append("3. The other sections over %s million: %s." % ("3.0", "; ".join(
        "%s %s" % (r, "%.1f" % secs[r]["annual"]) for r in over if r not in flips_in)))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Read traffic_estimate_terms_2025.pdf (a section's annual traffic is every motor vehicle passing along it, both directions, on all days of the year) and noise_mapping_2026_scope.pdf (every section counted in 2025; over three million vehicle passages is mapped).")
    L.append("2. Summed each section's 2025 manual count in manual_counts_2025.csv (all motor vehicles, 07:00 to 19:00, both directions) by count point.")
    L.append("3. Found each section's own approach in utc_asset_register_2025.xlsx: the junction named by the section's road and one of its end roads in count_points_2025.xlsx (street types abbreviated in the register), and on it the detectors whose approach is the section's road; %s have one." % names([s["road"] for s in det]))
    L.append("4. For those sections: the count times the detectors' mean full day over 2025 in utc_detector_daily_2025.csv, over the same detectors' 07:00 to 19:00 flow on the count day (the detectors see one approach, so their level cancels).")
    L.append("5. For the rest: the count times the same-day ratio of the permanent counters in the section's setting (atc_daily_2025.csv, atc_sites_2025.csv), their annual mean over their 07:00 to 19:00 flow on the count day.")
    L.append("6. Annual traffic is the daily flow times %d; %d sections are over %s million." % (365, G["n_over"], "3.0"))
    L.append("7. Counters' heavy goods vehicles: classes 5 to 7 of the legacy table until %s, when the outstations' channel 5 switched from two-axle rigid lorries to buses, and classes 6 to 8 of the TX-8 table from it, averaged over each counter's recorded days." % G["switch"])
    L.append("8. The two renewed junctions: the channels' series before each renewal grouped into approaches by their day-to-day co-movement and matched to the register's current approaches on level, weekend shares and 07:00 to 19:00 share across the dark days, then each approach's recorded vehicles summed over 2025.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### noise_round_sections_2025.csv")
    L.append("")
    L.append("1. 2025 annual traffic, millions of vehicles, and whether over three million:")
    for s in G["sections"]:
        L.append("   - %s (count point %d, %s km): %s, %s" % (s["road"], s["cp"], "%.2f" % s["length"], "%.1f" % s["annual"],
                                                       "yes" if s["over"] else "no"))
    L.append("")
    L.append("### section_traffic_2025.png")
    L.append("")
    L.append("1. One horizontal bar per counted section with its 2025 traffic, a dashed line at %s million and the sections over it in red." % "3.0")
    L.append("")
    L.append("### traffic_network_2025.xlsx")
    L.append("")
    L.append("1. Counters, heavy goods vehicles a day in 2025:")
    for c in G["counters"]:
        L.append("   - %s (%s): %d" % (c["site"], c["road"], c["hgv"]))
    L.append("2. Vehicles recorded on each approach in 2025, thousands:")
    for a in G["approaches"]:
        L.append("   - %s, %s: %s" % (a["junction"], a["approach"], "{:,}".format(a["thousands"])))
    L.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
