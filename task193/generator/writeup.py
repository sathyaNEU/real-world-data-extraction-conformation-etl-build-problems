"""submission.md, rendered from figures.json so no figure in it can drift from the pack."""
import json
import os

import world as W

NAME = {c: n for c, n, _h, _a, _k, _e in W.PRODUCTS}
NAME[W.DOMINANT] = W.DOM_NAME
NAME[W.RENAMED[0]] = W.RENAMED[2]
HOLDER = {}
for _c, _n, _h, _a, _k, _e in W.PRODUCTS:
    HOLDER[_c] = _h


def write(task_dir, g):
    masked = [tuple(x) for x in g["masked_pairs"]]
    sig = g["signals"]
    hid = [s for s in sig if (s["code"], s["reaction"]) in masked]
    kept = [s for s in sig if (s["code"], s["reaction"]) not in masked]
    lo_hid = min(s["prr_crude"] for s in hid)
    hi_hid = max(s["prr_crude"] for s in hid)
    lo_corr = min(s["prr"] for s in hid)
    hi_corr = max(s["prr"] for s in hid)
    lowest = min(s["prr"] for s in sig)
    cs = g["campaign_share"]
    four = sorted(cs[s["reaction"]] for s in hid)

    L = []
    L.append("# task193 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Pharmacology & Safety, safety signal detection (triaging which "
             "disproportionate reporting signals a capped assessment desk takes forward when one "
             "product holds two fifths of the quarter's reports).")
    L.append("**Analytical objective:** Anomaly Detection & Diagnostics (separating a real "
             "disproportion in reporting from what the database's own composition produces).\n")

    L.append("## 1. Final Recommendation\n")
    L.append("**Take %d signals forward to the assessment desk, and the desk can take all of them: "
             "they fill %d of its %d slots for the quarter.**\n" %
             (g["taken_forward"], g["taken_forward"], g["capacity"]))
    L.append("The quarter's reports are dominated by one product. The autumn booster accounts for "
             "**%.1f** per cent of the %s cases the agency received between 1 July and 30 September, "
             "and it holds between **%.1f** and **%.1f** per cent of every report naming the four "
             "reactions its own reactogenicity produces. Measured against a database that includes "
             "it, four pairs that meet the standard's criteria sit below the threshold: their ratios "
             "run from **%.2f** to **%.2f** against the whole database and from **%.2f** to **%.2f** "
             "once the booster's reporting is out of what they are compared with. Those four are "
             "%s. The run that leaves the booster in the comparison takes only **%d** forward and "
             "leaves five of the desk's slots idle.\n" %
             (g["dominant_share"], "{:,}".format(g["cases"]), four[0], four[-1],
              lo_hid, hi_hid, lo_corr, hi_corr,
              ", ".join("%s on %s" % (NAME[s["code"]], s["reaction"].lower()) for s in hid),
              g["crude_count"]))

    L.append("## 2. Critical Components\n")
    L.append("1. **%d** pairs meet all three criteria in paragraph 3.2 once the measure is taken "
             "against the reporting of the products the quarter is not dominated by, against **%d** "
             "when it is taken against every report in the database." %
             (g["taken_forward"], g["crude_count"]))
    L.append("2. The four the booster holds down are %s, at **%d**, **%d**, **%d** and **%d** "
             "reports." % (", ".join("**%s** on %s" % (NAME[s["code"]], s["reaction"].lower())
                                     for s in hid), *[s["reports"] for s in hid]))
    L.append("3. The booster is **%.1f** per cent of the quarter's reports, and on the four "
             "reactions in question it holds **%.1f**, **%.1f**, **%.1f** and **%.1f** per cent of "
             "every report naming them." % (g["dominant_share"], *four))
    L.append("4. Reading the reporter's own words as the reaction, instead of the preferred term the "
             "dictionary gives, takes **%d** pairs forward, more than the desk's **%d** slots; the "
             "reporting odds ratio against the whole database takes **%d**, which finds two of the "
             "four and not the other two." % (g["rung0_count"], g["capacity"], g["ror_count"]))
    L.append("5. The nearest pair to the threshold on the basis the answer rests on is **%.2f** "
             "above it, and the lowest ratio taken forward is **%.2f**, so no pair turns on the "
             "rounding.\n" % (g["nearest_to_threshold"], lowest))

    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Kept the submissions in `report_master.csv` whose receipt date falls between 1 July "
             "and 30 September 2026, which is the run's window under paragraph 2.1 of "
             "`signal_standard.pdf`. The report date and the coding date do not bear on it.")
    L.append("2. Collapsed the submissions of one case onto one report on the case number, as "
             "paragraph 2.2 requires: %s cases reached the agency through %s submissions, many of "
             "them reported by the clinician and by the licence holder both." %
             ("{:,}".format(g["cases"]), "{:,}".format(g["submissions"])))
    L.append("3. Took each reaction as the preferred term `reaction_dictionary.csv` gives for the "
             "reporter's verbatim term at the dictionary version the case was coded at, per "
             "paragraph 2.3, and carried the product renamed on its licence transfer onto one code "
             "through `product_register.csv`, per paragraph 2.4.")
    L.append("4. Built the two by two table for every product and reaction pair named on %d or more "
             "of those reports and computed the proportional reporting ratio and the chi-square of "
             "the same table." % W.N_MIN)
    L.append("5. Left out the pairs `product_information_listed.csv` already describes, which "
             "paragraph 3.3 keeps out of the run, and the pairs `closed_assessments_register.csv` "
             "closed inside the previous twelve months, which paragraph 3.4 keeps out: the register "
             "names no pair that meets the criteria on either basis.")
    L.append("6. Looked at what the comparison was carrying. One product holds **%.1f** per cent of "
             "the quarter's reports, and on six reactions it holds between **%.1f** and **%.1f** per "
             "cent of every report naming them, so for those reactions the rate the rest of the "
             "database is said to report at is mostly that one product's own reactogenicity." %
             (g["dominant_share"], min(cs.values()), max(cs.values())))
    L.append("7. Recomputed every pair with that product's reports out of what the pair is compared "
             "with. **%d** pairs meet the criteria, the **%d** the whole-database comparison already "
             "took plus four it held below 2.00. The list is stable: leaving out the two largest "
             "products, the three largest, or every product holding more than a tenth or a twentieth "
             "of the quarter gives the same %d, and leaving out any single other product moves no "
             "pair across." % (g["taken_forward"], g["crude_count"], g["taken_forward"]))
    L.append("8. Checked the two readings a careful run would also take: pooling the ratio over the "
             "report's channel, reporter type, age band, region or sex lands on the same **%d**, and "
             "the reporting odds ratio against the whole database lands on **%d**. Neither reaches "
             "the four, because neither changes what the comparison is carrying.\n" %
             (g["crude_count"], g["ror_count"]))

    L.append("## 4. Deliverable Answers\n")
    L.append("### signal_list_2026Q3.xlsx\n")
    L.append("| Product | Reaction | Reports | Ratio | Chi-square | Against the whole database |")
    L.append("|---|---|---|---|---|---|")
    for s in sig:
        tag = "%.2f, below 2.00" % s["prr_crude"] if (s["code"], s["reaction"]) in masked else ""
        L.append("| %s | %s | %d | %.2f | %.1f | %s |" %
                 (NAME[s["code"]], s["reaction"], s["reports"], s["prr"], s["chi"], tag))
    L.append("")
    L.append("Pairs taken forward **%d**, the desk's capacity **%d**, slots left **%d**. The "
             "whole-database comparison alone takes **%d**.\n" %
             (g["taken_forward"], g["capacity"], g["slots_left"], g["crude_count"]))
    L.append("### signal_overview.png\n")
    L.append("One horizontal bar for each of the %d pairs taken forward, ordered by its ratio, with "
             "the paragraph 3.2 threshold drawn at 2.00. The four the booster held down are shown in "
             "a second colour, each with a marker at the ratio it reaches against the whole database "
             "(%.2f, %.2f, %.2f and %.2f), so the gap the comparison set makes reads at a glance.\n"
             % (g["taken_forward"], *[s["prr_crude"] for s in hid]))

    L.append("### Submissions by channel and month\n")
    L.append("| Channel | Month | Submissions received | Could not be coded | Mean days to coding |")
    L.append("|---|---|---|---|---|")
    for key in sorted(g["a1_channels"]):
        ch, mo = key.split("|")
        v = g["a1_channels"][key]
        L.append("| %s | %s | %d | %d | %.1f |" % (ch, mo, v["received"], v["not_coded"],
                                                   v["mean_days"]))
    L.append("")
    L.append("### Licence holders\n")
    L.append("| Licence holder | Submissions filed | Filed after the quarter closed | Fee due (DKK) |")
    L.append("|---|---|---|---|")
    for h in sorted(g["a2_holders"]):
        v = g["a2_holders"][h]
        L.append("| %s | %d | %d | %d |" % (h, v["filed"], v["after_close"], v["fee"]))
    L.append("")
    L.append("### Cases by region and age group\n")
    L.append("| Region | Age group | Cases | Share naming a serious reaction |")
    L.append("|---|---|---|---|")
    for key in sorted(g["a3_cells"]):
        reg, band = key.split("|")
        v = g["a3_cells"][key]
        L.append("| %s | %s | %d | %.1f per cent |" % (reg, band, v["cases"], v["serious_share"]))
    L.append("")
    with open(os.path.join(task_dir, "submission.md"), "w") as f:
        f.write("\n".join(L))
