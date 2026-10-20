"""submission.md, drafted from figures.json's own values."""
import world as W

TAGS = ("> **Domain:** Physical & Environmental Sciences (emissions inventory).\n"
        "> **Analytical objective:** Data Extraction & Conformation (ETL).")


def write(path, x):
    import golden as GD
    g = GD.figures(x)
    F = W.FILES
    rec = g["call"]
    rows = {r["district"]: r for r in g["rows"]}
    late = [d for d in rec if W.DISTRICTS[d][0] >= 8]
    import methods as M
    import pack as P
    mi = P.miles(x)
    mid = M.methane(P.inventory_rows(x), "mid", x["fig"]["profile"], W.RATE, W.END)
    extra = sorted(d for d in mi if mid.get(d, 0) / mi[d] >= W.LINE and d not in rec)
    L = ["## Tags", "", TAGS, "",
         "## 1. Final Recommendation", "",
         "**Designate %s of the 12 districts for the 2027 to 2029 Accelerated Main Replacement Program: %s.**" % (
             GD.WORDS[g["n_call"]], ", ".join(rec[:-1]) + " and " + rec[-1]),
         "Each emitted %s tonnes or more of 2026 leak methane per mile of cast-iron and bare-steel main once each "
         "surveyed leak is dated from the season leaks begin in. Not %s, which the midpoint start between surveys "
         "puts over the line: leaks begin mostly in December to March (%s per cent of odor-reported starts), so a "
         "district walked in spring finds young leaks, while %s, walked late in the year, found leaks that had emitted "
         "since the winter." % (g["line"], " or ".join(extra), g["frost_share"], ", ".join(late[:-1]) + " and " + late[-1]),
         "",
         "## 2. Critical Components", "",
         "1. Odor-reported leak starts in December to March: **%s%%** of the 2016 to 2026 starts." % g["frost_share"],
         "2. Districts at or above the line: **%d** of 12." % g["n_call"],
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Read the guidelines (%s): leaks found in 2026 on cast-iron and bare-steel mains, each from its start to its "
         "repair or 31 December 2026 at its Table 1 rate for the grade when found, per mile of in-service cast-iron and "
         "bare-steel main, designated at %s or more." % (F["guidelines"], g["line"]),
         "2. Took the 2026 leaks from %s (survey finds) and %s (confirmed calls, UTC converted to local time), each "
         "leak's segment and district from %s, and its repair from the REPAIRED visit in %s." % (
             F["finds"], F["odor"], F["mains"], F["repairs"]),
         "3. Took the monthly profile of leak starts from the confirmed odor calls of 2016 to 2026 (a called leak starts "
         "at the call, guidelines %s): %s per cent in December to March." % (g["sections"]["methane"],
                                                                        g["frost_share"]),
         "4. Dated each surveyed leak's start as its expected start between its segment's 2025 survey (%s) and the "
         "find, each day weighted by its month's share of the profile." % F["schedule"],
         "5. Summed each leak's rate times its hours from start to repair or year end by district, and divided by the "
         "district's cast-iron and bare-steel miles in %s: %s at or above the line." % (
             F["mains"], ", ".join(rec)),
         "6. From %s, took each work order's cost of each type at the end of 2026 less at the end of 2025 (each line is "
         "the cost to date, as the closing totals in %s confirm), by the leak's own district: the repair costs below." % (
             F["costs"], F["closeouts"]),
         "7. From %s, counted each service address shut off for a leak repair once per leak (dispatch and the field "
         "crew sometimes both opened a ticket) and the meters behind it in %s: the customer interruptions below." % (
             F["tickets"], F["meters"]),
         "8. Designated the districts at or above the line: %s." % ", ".join(rec),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. Each district: leaks found in 2026, designated, 2026 leak repair cost, 2026 customer interruptions:"]
    for r in g["rows"]:
        L.append("   - %s: %d; %s; $%s; %d" % (r["district"], r["leaks"], "yes" if r["designated"] else "no",
                                               "{:,}".format(g["ask_a"][r["district"]]), g["ask_b"][r["district"]]))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. Designates %s of 12: %s." % (GD.WORDS[g["n_call"]], ", ".join(rec)),
          "2. Bar chart of the 12 districts' methane per mile against the %s line, designated districts highlighted, on "
          "page 1; the district table beneath it." % g["line"], ""]
    open(path, "w", encoding="utf-8").write("\n".join(L))
