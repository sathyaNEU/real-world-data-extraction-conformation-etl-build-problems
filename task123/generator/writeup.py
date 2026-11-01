"""submission.md and the figure list behind it, every number taken from F."""
import pack as P


def fmt(n):
    return "{:,}".format(int(n))


def write(F, path):
    q = [x for x in F["comuni"] if x["qualifies"]]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Survey Research & Official Statistics (official time-series production: a monthly "
             "accommodation series benchmarked to quarterly administrative totals).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**%d member comuni qualify for the 2027 peak-month services co-financing: %s.**" % (
        len(q), ", ".join("%s (%.1f guest nights per resident in August 2026)" % (x["name"], x["npr_r"]) for x in q)))
    L.append("%s is the comune closest to the line, %.1f nights per resident against 30; every other member comune is "
             "below 30.\n" % (F["nearest"]["name"], F["nearest"]["npr_r"]))
    L.append("## 2. Critical Components\n")
    L.append("1. August 2026 guest nights and nights per resident by member comune: " + "; ".join(
        "%s %s and %.1f" % (x["name"], fmt(x["nights_r"]), x["npr_r"]) for x in F["comuni"]) + ".")
    L.append("2. Qualifying (30 or more): %s; closest to the line: %s at %.1f." % (
        ", ".join(x["name"] for x in q), F["nearest"]["name"], F["nearest"]["npr_r"]))
    L.append("3. Each comune's August 2026 nights are its July to September 2026 declared nights (latest filing for "
             "each category) less its reported July and September returns, which are complete; the comuni without "
             "the tourist tax (Collebruno, San Gaudenzio, Fontecupa) take their August returns as filed, all of which "
             "were filed.\n")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read %s, kept for each establishment and month the rows of its latest submission "
             "(PROGR_INVIO), and summed PRESENZE over residence groups." % P.F_SURVEY)
    L.append("2. Matched July to September 2026 returns (CIN codes) to %s; every establishment on the register "
             "filed July and September, and some open in August filed no August return." % P.F_REGISTER)
    L.append("3. Read the quarterly tourist-tax declarations from the five tax-office files (the concessionaire's "
             "workbook, Porto Levarna's and Sant'Elvira a Mare's csv files, the hill comuni's shared file and Lido di "
             "Arzena's pdf), keeping for each comune, quarter and category the filing received last, and took total "
             "nights (liable and exempt), as the union's regulation (art. 3) counts every night.")
    L.append("4. Where every establishment of a comune filed every month, its survey quarter equals its declared "
             "quarter; set each comune's August 2026 nights to its declared July to September 2026 nights less its "
             "reported July and September nights.")
    L.append("5. Divided by residents at 1 January 2026 (%s, with Alvea Salvina as one comune) and compared "
             "with 30 (regulation art. 2)." % P.F_POP)
    L.append("6. January to April 2026: summed the latest returns of every establishment by the comune code in "
             "its CIR (the first three digits after 112), mapping 006 and 007 to Alvea Salvina (%s), so the "
             "establishments that closed before the May code change, absent from the register, still count." % P.F_VAR)
    L.append("7. October 2025 occupancy: October nights over bed-places available on the days each register "
             "establishment was open, with the bed-places in force in October (VARIAZIONI), no days for the "
             "suspended establishments and the opening period's closing day.")
    L.append("8. 2025 tourist tax: each comune's liable nights per quarter and category from the last filing, "
             "times the rate in force that quarter (%s), Torre Alvea and Salvina Marina included.\n" % P.F_RATES)
    L.append("## 4. Deliverable Answers\n")
    L.append("### august_2026_guest_nights.xlsx\n")
    L.append("1. August 2026 by member comune (guest nights; nights per resident; qualifies):")
    for x in F["comuni"]:
        L.append("   - %s: %s; %.1f; %s" % (x["name"], fmt(x["nights_r"]), x["npr_r"], "yes" if x["qualifies"] else "no"))
    L.append("2. Qualifying comuni: %s." % ", ".join(x["name"] for x in q))
    L.append("3. Closest to the line: %s, %.1f nights per resident." % (F["nearest"]["name"], F["nearest"]["npr_r"]))
    L.append("4. Guest nights for January to April 2026 by member comune:")
    for x in F["janapr"]:
        L.append("   - %s: %s" % (x["name"], fmt(x["nights_r"])))
    L.append("5. Net bed-place occupancy in October 2025 by type of establishment (per cent):")
    for x in F["occupancy"]:
        L.append("   - %s: %.1f" % (x["type"], x["pct_r"]))
    L.append("6. Tourist tax due to the member comuni in 2025 (EUR):")
    for x in F["tax"]:
        L.append("   - Q%d: %s" % (x["q"], fmt(x["eur_r"])))
    L.append("\n### peak_cofinancing_2027_note.pdf\n")
    L.append("1. Decision: %s qualify; %s is closest to the line at %.1f." % (
        ", ".join(x["name"] for x in q), F["nearest"]["name"], F["nearest"]["npr_r"]))
    L.append("2. Chart: horizontal bars of August 2026 guest nights per resident for every member comune, the "
             "qualifying comuni highlighted, a dashed line at 30, each bar labelled with its value.")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def figure_values(F):
    vals = []
    for x in F["comuni"]:
        vals += [x["nights_r"], fmt(x["nights_r"]), x["npr_r"]]
    vals += [F["nearest"]["npr_r"], len([x for x in F["comuni"] if x["qualifies"]]), 30]
    for x in F["janapr"]:
        vals += [x["nights_r"], fmt(x["nights_r"])]
    for x in F["occupancy"]:
        vals.append(x["pct_r"])
    for x in F["tax"]:
        vals += [x["eur_r"], fmt(x["eur_r"])]
    vals += [112, 6, 7, 3, 12, 2025, 2026, 2027]
    return vals
