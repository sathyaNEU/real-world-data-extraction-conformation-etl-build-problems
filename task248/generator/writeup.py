"""figures.json, submission.md and metadata.json, each emitted from the analysis results (nothing typed)."""
import os

PRODS = ["REC-90 ethanol-free", "E10 unleaded", "Diesel"]
AS_OF = "2027-01-12"
STAMP = "2027-01-11"

SOURCES = {
    "atg_inventory_2026.csv": ("evidence", "Highbank Marinas automatic tank gauge consoles, 2026 inventory reports as exported by the "
                               "monitoring portal on 11 January 2027; synthetic, built for this task"),
    "atg_deliveries_2026.csv": ("evidence", "Highbank Marinas automatic tank gauge consoles, 2026 delivery reports; synthetic"),
    "atg_leak_tests_2026.csv": ("evidence", "Monitoring portal log of the consoles' 0.2 gal/h in-tank leak tests, 2026; synthetic"),
    "atg_tank_setup.csv": ("evidence", "Monitoring portal console and tank setup history; synthetic"),
    "bols_2026.csv": ("evidence", "Fuel distributor's 2026 bill of lading export for the Highbank Marinas accounts; synthetic"),
    "dock_sales_legacy_2026.csv": ("evidence", "Legacy dock point-of-sale transaction export, 1 January to go-live on 16 November 2026; synthetic"),
    "dock_sales_2026-11-09_2026-12-31.jsonl": ("evidence", "New dock point-of-sale transaction export from the shadow week to "
                                               "31 December 2026; synthetic"),
    "pos_grades.csv": ("evidence", "New point-of-sale grade table as held at export; synthetic"),
    "dock_piping.xlsx": ("evidence", "Highbank Marinas fuel dock piping record, hose to tank; synthetic"),
    "tank_register.xlsx": ("evidence", "Highbank Marinas underground storage tank register; synthetic"),
    "tank_charts.csv": ("evidence", "Gauge chart tables as loaded in the consoles, quarter-inch steps; synthetic"),
    "FS-3_fuel_systems_standard.pdf": ("evidence", "Highbank Marinas FS-3 fuel systems standard, revision 6, approved 14 September 2026; synthetic"),
    "wetstock_onboarding_2027.pdf": ("evidence", "Clearline Wetstock Services onboarding letter of 3 December 2026; synthetic"),
    "lake_levels_2026.csv": ("distractor", "Daily pool elevation and outflow for Lake Wenning and Tolliver Lake, 2026; synthetic"),
    "monthly_closeouts_2026.xlsx": ("distractor", "Marina managers' monthly book-to-gauge fuel close-outs, 2026 season; synthetic"),
}
DELIVERABLES = ["recharting_list_2027.csv", "cutover_readiness_2027.pdf"]


def a3_cells(res):
    marinas = sorted({k.split("|")[0] for k in res["A3"]})
    return [(m, p, int(round(res["A3"]["%s|%s" % (m, p)]))) for m in marinas for p in PRODS if "%s|%s" % (m, p) in res["A3"]]


def figures(res, pk):
    listed = res["golden_list"]
    return {
        "call": {"count": len(listed), "listed": listed,
                 "pairs": {t: res["tanks"][t]["gold_pair"] for t in listed}},
        "limit_gal": 25,
        "filed": {"fs3_recharting_section": 3.4, "reference_temperature_f": 60},
        "unlisted_count": len(pk.reg) - len(listed),
        "capacities_gal": {t: int(pk.reg[t]["cap"]) for t in listed},
        "rungs": {"monthly_reconciliation": res["R0_list"], "delivery_check": res["R1_list"],
                  "intervals_alone": res["R2_list"]},
        "A1": {t: int(v) for t, v in sorted(res["A1"].items())},
        "A2": {m: int(v) for m, v in sorted(res["A2"].items())},
        "A3": {"%s|%s" % (m, p): v for m, p, v in a3_cells(res)},
    }


def _names(ts):
    return ", ".join(ts[:-1]) + " and " + ts[-1] if len(ts) > 1 else ts[0]


def submission(res, pk, f):
    listed = f["call"]["listed"]
    n = f["call"]["count"]
    words = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}
    mid = [t for t in listed if f["call"]["pairs"][t] == "reorder and half-full"]
    full = [t for t in listed if f["call"]["pairs"][t] == "reorder and normal fill"]
    other = [t for t in listed if t not in mid and t not in full]
    assert not other
    r2 = f["rungs"]["intervals_alone"]
    r2_extra = [t for t in r2 if t not in listed]
    r2_missed = [t for t in listed if t not in r2]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Physical & Environmental Sciences (sensor calibration and measurement).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**%s tanks need their gauge charts redone before the 2027 season: %s.**" % (words[n], _names(listed)))
    L.append("Each misstates the change in stock by more than 25 gallons between two of its reorder, half-full and normal "
             "fill heights once the 2026 sales intervals are anchored on the deliveries. Not none, as the monthly "
             "reconciliations read: every fill-and-draw cycle cancels both kinds of chart error. Not %s alone, as the "
             "delivery check reads: %s misstate most through the middle of the range, which every delivery spans end to "
             "end. Not the %d tanks the sales intervals alone give: that fit charges %s's dock meter errors to their charts "
             "and drops %s." % (_names(full), _names(mid), len(r2), _names(r2_extra), _names(r2_missed)))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. %s misstate most between the reorder and half-full heights, each by more than **25** gallons." % _names(mid))
    L.append("2. %s misstate most between the reorder and normal fill heights, each by more than **25** gallons." % _names(full))
    L.append("3. The other **%d** tanks misstate less than 25 gallons between every pair of the three heights." % f["unlisted_count"])
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took each tank's reorder, half-full and normal fill heights from tank_register.xlsx and its chart from "
             "tank_charts.csv, keyed console tank numbers to tanks by the dates in atg_tank_setup.csv, and read the 2026 "
             "season, 1 April to 31 October (FS-3 section 3.4).")
    L.append("2. Paired consecutive two-hour readings in atg_inventory_2026.csv that no delivery overlaps and summed the gallons "
             "each tank's hoses metered between them in dock_sales_legacy_2026.csv (hoses to tanks by dock_piping.xlsx), "
             "corrected to 60 F with FS-3 Table 1.")
    L.append("3. Set each delivery's net rise in atg_deliveries_2026.csv against its bill of lading's net gallons in "
             "bols_2026.csv.")
    L.append("4. Fitted each tank's chart error as a piecewise-linear function of height (3-inch knots, the three register "
             "heights among them) to the intervals with a dock meter factor and to the deliveries without one, together: "
             "%d tanks misstate more than 25 gallons between two heights." % n)
    L.append("5. For the gauge feed, re-dated each console's rows stamped 2016 after the 24 January storm along its record "
             "sequence, kept Dellwood's tanks apart either side of the 17 February console change by atg_tank_setup.csv, "
             "and counted each tank's local days of 2026 with no reading.")
    L.append("6. For leak tests, kept one row per console, tank and test number in atg_leak_tests_2026.csv, dated each test "
             "by its own Sunday-night row or, for a test logged only when re-polled after an outage, by the weekly test "
             "numbers, and counted each marina's tank-months with no PASS.")
    L.append("7. For dock gallons, took the legacy export to go-live and the new export after the last legacy sale (its "
             "shadow-week card copies dropped), dated card sales to the day before their settlement stamp, and read each "
             "new-export row's product from its price, because pos_grades.csv lists Ashby Hollow's and Gilliam Creek's "
             "former E10 grade as REC-90.")
    L.append("8. Re-chart %s before the service starts on 1 April 2027." % _names(listed))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### recharting_list_2027.csv")
    L.append("")
    L.append("1. %s rows:" % words[n])
    for t in listed:
        g = pk.reg[t]
        L.append("   - %s: %s, %s, %s gallons, %s" % (t, g["marina"], g["product"], "{:,}".format(int(g["cap"])),
                                                     f["call"]["pairs"][t]))
    L.append("")
    L.append("### cutover_readiness_2027.pdf")
    L.append("")
    L.append("1. Number: %d tanks need their charts redone." % n)
    L.append("2. Chart: paired bars of each listed tank's misstatement over reorder to half-full and over half-full to "
             "normal fill, with the 25-gallon lines.")
    L.append("3. Days of 2026 each tank's gauge sent no inventory reading:")
    for t, v in f["A1"].items():
        L.append("   - %s: %d days" % (t, v))
    L.append("4. Tank-months of 2026 without a passing monthly leak test, by marina:")
    for m, v in f["A2"].items():
        L.append("   - %s: %d" % (m, v))
    L.append("5. 2026 dock gallons by marina and product, to the nearest gallon:")
    by_m = {}
    for k, v in f["A3"].items():
        m, p = k.split("|")
        by_m.setdefault(m, []).append("%s %s" % (p, "{:,}".format(v)))
    for m in sorted(by_m):
        L.append("   - %s: %s" % (m, "; ".join(by_m[m])))
    L.append("")
    return "\n".join(L)


def metadata(target, res):
    rows = {}
    for fn in sorted(os.listdir(target)):
        if fn.endswith((".csv", ".jsonl")):
            with open(os.path.join(target, fn), encoding="utf-8") as fh:
                rows[fn] = sum(1 for _ in fh) - (1 if fn.endswith(".csv") else 0)
    big = max(rows, key=rows.get)
    files = {}
    for fn in sorted(os.listdir(target)):
        role, src = SOURCES[fn]
        files[fn] = {"source": src, "date": STAMP, "license": "synthetic, CC0", "role": role}
    return {
        "task": "task248", "architecture": 2, "as_of": AS_OF,
        "decision": "which of the marina group's underground fuel tanks need their gauge charts redone before the wetstock "
                    "monitoring service starts on 1 April 2027",
        "deliverables": DELIVERABLES,
        "files": files,
        "distractor_files": sorted(fn for fn, (role, _s) in SOURCES.items() if role == "distractor"),
        "largest_file": {"name": big, "rows": rows[big]},
        "row_counts": rows,
    }
