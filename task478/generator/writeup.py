"""submission.md, every figure read from generator/figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CODES = ["%02d" % i for i in range(1, 13)]


def join(xs, word="and"):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " %s " % word + xs[-1]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    by = {x["section"]: (n, x) for n, x in f["sections"].items()}
    five = [by[c][0] for c in CODES if by[c][1]["equip"] == "Yes"]
    S = lambda n: f["sections"][n]
    c = f["components"]
    six = c["sixth"]
    raw_in = [n for n in f["default"]["equip"] if n not in five]
    pooled_in = [n for n in f["pooled"]["equip"] if n not in five]
    heavy = [n for n in raw_in]
    light = [n for n in five if n not in f["default"]["equip"]]
    low = min(S(n)["share_pct"] for n in five)
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** General Statistics & Data Science (data integration: a turnpike authority's twelve "
               "weigh-in-motion stations of two sensor types conformed onto the static scale's weight basis through each "
               "station's loaded class 9 steer axles against the scale houses' tickets, then counted against the 80,000-lb "
               "gross limit by section).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Equip %s with the 2027 virtual weigh stations.**" % join(five))
    out.append("With each station's weights on the static scale's basis, %s per cent of the class 9 trucks their "
               "stations weighed in 2026 ran over 80,000 lb, against %s's %d per cent in sixth. Not %s, which lead on "
               "the weights as recorded (%s per cent) only because their stations read %s per cent heavy; not %s, which "
               "comes in only when the steer axles of empty and loaded tractors are pooled.\n"
               % (join(["%d" % S(n)["share_pct"] for n in five]), six["name"], six["share_pct"], join(raw_in, "or"),
                  join(["%d" % S(n)["raw_share_pct"] for n in raw_in]), join(["%d" % S(n)["reads_pct"] for n in heavy]),
                  join(pooled_in, "or")))
    out.append("## 2. Critical Components\n")
    out.append("1. Against the scale houses' loaded static tickets, on the steer axles of loaded class 9 trucks, %s "
               "stations read **%s** per cent heavy and %s **%s** per cent light."
               % (join(["%s's" % n for n in heavy]), join(["%d" % S(n)["reads_pct"] for n in heavy]),
                  join(["%s's" % n for n in light]), join(["%d" % -S(n)["reads_pct"] for n in light])))
    out.append("2. The lowest of the five shares is **%d** per cent, against %s's **%d** in sixth.\n"
               % (low, six["name"], six["share_pct"]))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Read ctpa_wim_piezo_2026.txt (fixed width, tens of pounds) and ctpa_wim_bendingplate_2026.csv (kilograms), "
        "kept the class 9 weighings the controllers did not reject and put each station in its section by its milepost "
        "in ctpa_wim_stations.csv: {:,} class 9 trucks weighed.".format(c["class9_weighed"]),
        "Took the loaded trucks in ctpa_scale_house_tickets_2026.xlsx (five axles summing over 50,000 lb): their steer "
        "axle's median on the static scale is {:,} lb.".format(c["ticket_loaded_steer_lb"]),
        "Divided each station's median steer axle of its loaded class 9 trucks (gross over 50,000 lb as recorded) by "
        "that median: factors from %s (%s) to %s (%s)." % (c["factor_low"]["factor"], c["factor_low"]["name"],
                                                           c["factor_high"]["factor"], c["factor_high"]["name"]),
        "Divided every weighing's gross by its station's factor and took each section's share over 80,000 lb (program "
        "3.2): %s lead, %s is sixth at %d per cent."
        % (join(["%s %d" % (n, S(n)["share_pct"]) for n in five]), six["name"], six["share_pct"]),
        "For the weekday entries, took each entry in ctpa_toll_entries_5axle_2026.csv once: a T26 row stamped up to 16 "
        "minutes before a numeric-id row of the same tag and plaza is the new host's backfill of that entry (the plazas "
        "moved one by one in May and June) and goes; the numeric-id rows are the old host's local stamps and the other "
        "T26 rows UTC; placed plaza P23 at Brannock Road to 30 April (ctpa_toll_schedule_2025.pdf) and at Halbrook East "
        "from 1 September (ctpa_toll_plazas.csv), and averaged over the 261 weekdays (program 5): {:,} five-axle entries "
        "a weekday on the turnpike.".format(c["entries_weekday_total"]),
        "For the citations, placed each violation G row of ctpa_citations_2026.csv at its tag's last toll entry before "
        "the stop, the trip weighed (program 6.2), on those entries with the old host's stamps read as local time (read "
        "as UTC, the entry a cited truck makes coming back through the barrier after offloading falls before its stop), "
        "not at its entry_plaza, which the toll system returned when the citation was keyed: {:,} gross overweight "
        "citations.".format(c["gross_citations_total"]),
        "Recommended the five highest shares: %s." % join(five),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### ctpa_vws_sections_2027.xlsx\n")
    out.append("1. The five sections to equip: %s." % join(five))
    out.append("2. Share of the class 9 trucks each section's station weighed in 2026 that were over 80,000 lb, whole "
               "per cent:")
    for code in CODES:
        n, x = by[code]
        out.append("   - %s: %d per cent" % (n, x["share_pct"]))
    out.append("3. Average five-axle trucks a weekday entering at each section's interchanges in 2026, whole trucks:")
    for code in CODES:
        n, x = by[code]
        out.append("   - %s: %d" % (n, x["weekday_entries"]))
    out.append("4. Gross overweight citations the scale houses issued in 2026 to five-axle trucks that had entered at "
               "each section, whole citations:")
    for code in CODES:
        n, x = by[code]
        out.append("   - %s: %d" % (n, x["gross_citations"]))
    out.append("\n### ctpa_section_overweight_2026.csv\n")
    out.append("5. Twelve rows, one per section west to east, each with its share as in item 2.")
    out.append("\n### ctpa_overweight_share_2026.svg\n")
    out.append("6. Bar chart of the twelve shares west to east, each labelled with its whole per cent, the five sections "
               "to equip in blue and the others in grey.")
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
