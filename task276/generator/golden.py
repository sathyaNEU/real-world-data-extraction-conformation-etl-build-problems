"""The golden deliverables (the committee workbook and its printed chart) and figures.json, all from solve.py's output."""
import json
import os

import pandas as pd

import office as O
import params as P

XLSX = "cab_fit_2027.xlsx"
PDF = "cab_fit_2027.pdf"
LABEL = {c["id"]: "%s on %s" % (c["converter"], c["chassis"]) for c in P.CABS}
SHORT = {c["id"]: "%s %s" % (c["converter"].split()[0], c["chassis"]) for c in P.CABS}
CONVERTERS = ["Pennick Coachbuild", "Ostrel Vehicle Conversions"]
CHASSIS = ["FD35", "RD43"]


def r1(x):
    return float("%.1f" % (x + 1e-9))


def answers(S):
    fit = S["fit"]
    best, second, gap = S["call"]
    F = S["fleet"]
    A = {"cabs": [{"id": c["id"], "cab": LABEL[c["id"]], "fail": fit[c["id"]]["fail"], "women": fit[c["id"]]["women"]}
                  for c in P.CABS],
         "best": best, "second": second, "gap": gap,
         "converters": [], "chassis": []}
    for c in CONVERTERS:
        f = F["converters"][c]
        A["converters"].append({"converter": c, "jobs": list(f["jobs"]), "miles": int(round(f["miles"] / 100.0)) * 100,
                                "miles_exact": f["miles"], "rate": float("%.2f" % (f["rate"] + 1e-9)), "rate_exact": f["rate"]})
    for c in CHASSIS:
        f = F["chassis"][c]
        A["chassis"].append({"chassis": c, "days": list(f["days"]), "vehicle_years": r1(f["vehicle_years"]),
                             "vy_exact": f["vehicle_years"], "rate": r1(f["rate"]), "rate_exact": f["rate"]})
    A["default"] = S["default_call"]
    A["rungs"] = S["rungs"]
    A["drivers"] = S["drivers"]
    return A


def workbook(folder, A):
    best = A["best"]
    cabs = sorted(A["cabs"], key=lambda r: r["fail"])
    low = min(r["fail"] for r in cabs)
    t1 = pd.DataFrame([(r["cab"].split(" on ")[0], r["cab"].split(" on ")[1], r["fail"], r["women"], r["fail"] - r["women"],
                        r["fail"] - low, "Recommended" if r["id"] == best else ("Runner-up" if r["id"] == A["second"] else ""))
                       for r in cabs],
                      columns=["Converter", "Chassis-cab", "Drivers it fails to fit", "of whom women", "of whom men",
                               "More than the recommended cab", "Note"])
    t2 = pd.DataFrame([(r["converter"], *r["jobs"], sum(r["jobs"]), r["miles"], r["rate"]) for r in A["converters"]],
                      columns=["Converter", "Q1 Apr-Jun", "Q2 Jul-Sep", "Q3 Oct-Dec", "Q4 Jan-Mar", "Year",
                               "Miles run 2025-26", "Jobs per 100,000 miles"])
    t3 = pd.DataFrame([(r["chassis"], *r["days"], sum(r["days"]), r["vehicle_years"], r["rate"]) for r in A["chassis"]],
                      columns=["Chassis-cab", "Q1 Apr-Jun", "Q2 Jul-Sep", "Q3 Oct-Dec", "Q4 Jan-Mar", "Year",
                               "Vehicle-years in service", "Days off the road per vehicle-year"])
    gap = A["gap"]
    fails = dict((r["id"], r["fail"]) for r in A["cabs"])
    notes = {
        "Cab fit": ["%s fails the fewest of our rostered drivers: %d, against %d for %s" % (
                        LABEL[best], fails[best], fails[A["second"]], LABEL[A["second"]]),
                    "Front-line driving roster of 1 October 2026 (%s drivers), each driver's latest cab fit measurement, "
                    "cab fit standard issue 2. A driver fails a cab when they cannot be seated in the posture the "
                    "posture model predicts for them with the eye point inside the vision zone." % format(A["drivers"], ",")],
        "Converters": ["Seat and cab-structure defect jobs (B12, B30) raised on each shortlisted converter's front-line "
                       "vehicles, 2025-26, by quarter raised"],
        "Chassis": ["Days off the road, front-line vehicles on each shortlisted chassis-cab, 2025-26"],
    }
    t4 = pd.DataFrame([
        ("Drivers", "Front-line driving roster published 1 October 2026; latest measurement from the cab fit measurement "
                    "programme, March 2025 to September 2026, former Vennerley staff numbers mapped through HR's crosswalk."),
        ("Cabs", "Package data from tender HAS-F-2026-04; Wrenfold's dimensions moved from each cab's seating reference "
                 "point to the accelerator heel point."),
        ("Fleet", "Front-line vehicles in the fleet at any time from 1 April 2025 to 31 March 2026, from the fleet register, "
                  "the disposals list and the Vennerley asset list; Fleet Services performance reporting standard, issue 4."),
        ("Not shown", "Wrenfold Bodies has no vehicles in our fleet. Corvane Coachworks vehicles count in the chassis figures "
                      "only, Corvane not being on the shortlist."),
        ("Rounding", "Drivers, jobs and days whole; miles to the nearest hundred; jobs per 100,000 miles to two decimals; "
                     "vehicle-years and days per vehicle-year to one decimal.")], columns=["Item", "Note"])
    O.xlsx(os.path.join(folder, XLSX), [("Cab fit", t1), ("Converters", t2), ("Chassis", t3), ("Notes", t4)], author="Brenda Ward",
           created="2026-10-09T08:12:00Z", modified="2026-10-09T15:46:00Z", last="Brenda Ward",
           widths={"Cab fit": [28, 12, 22, 15, 13, 26, 14], "Converters": [28, 11, 11, 11, 11, 8, 17, 21],
                   "Chassis": [12, 11, 11, 11, 11, 8, 22, 31], "Notes": [12, 120]},
           number_formats={"Converters": {"Miles run 2025-26": "#,##0", "Jobs per 100,000 miles": "0.00"},
                           "Chassis": {"Vehicle-years in service": "0.0", "Days off the road per vehicle-year": "0.0"}},
           notes_rows=notes, title="2027 cab specification: fit and fleet record")


def chart(folder, A):
    from reportlab.graphics.shapes import Drawing, String
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.lib import colors
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    O.word_fonts()
    cabs = [r for r in A["cabs"]]
    best = A["best"]

    def story():
        base = ParagraphStyle("b", fontName="Calibri", fontSize=10, leading=13)
        head = ParagraphStyle("h", parent=base, fontName="Calibri-Bold", fontSize=13, leading=17)
        d = Drawing(170 * mm, 105 * mm)
        bc = VerticalBarChart()
        bc.x, bc.y, bc.width, bc.height = 18 * mm, 18 * mm, 145 * mm, 78 * mm
        bc.data = [[r["fail"] for r in cabs]]
        bc.categoryAxis.categoryNames = [SHORT[r["id"]] for r in cabs]
        bc.categoryAxis.labels.fontName = "Calibri"
        bc.categoryAxis.labels.fontSize = 8.5
        bc.valueAxis.labels.fontName = "Calibri"
        bc.valueAxis.labels.fontSize = 8
        top = max(r["fail"] for r in cabs)
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = int((top // 100 + 1) * 100)
        bc.valueAxis.valueStep = 100
        bc.bars[0].fillColor = colors.HexColor("#8A8F98")
        bc.bars[0].strokeColor = None
        bc.barLabelFormat = "%d"
        bc.barLabels.fontName = "Calibri"
        bc.barLabels.fontSize = 8.5
        bc.barLabels.nudge = 7
        for i, r in enumerate(cabs):
            if r["id"] == best:
                bc.bars[(0, i)].fillColor = colors.HexColor("#2F5597")
        d.add(bc)
        d.add(String(bc.x - 2 * mm, bc.y + bc.height + 4 * mm, "Drivers who fail to fit", fontName="Calibri",
                     fontSize=8.5, textAnchor="start"))
        i = [r["id"] for r in cabs].index(best)
        step = bc.width / len(cabs)
        xm = bc.x + step * (i + 0.5)
        d.add(String(xm, bc.y + bc.height * cabs[i]["fail"] / bc.valueAxis.valueMax + 9 * mm, "Recommended",
                     fontName="Calibri-Bold", fontSize=9, fillColor=colors.HexColor("#2F5597"), textAnchor="middle"))
        small = ParagraphStyle("s", parent=base, fontSize=8, leading=10, textColor=colors.HexColor("#555555"))
        fail_best = [r["fail"] for r in cabs if r["id"] == best][0]
        return [Paragraph("%s fails %d of our %s rostered drivers, the fewest on the 2027 shortlist" % (
                    LABEL[best], fail_best, format(A["drivers"], ",")), head),
                Paragraph("Rostered drivers each shortlisted cab fails to fit under the cab fit standard (issue 2). The "
                          "recommended cab is shown in blue.", base),
                Spacer(1, 4 * mm), d, Spacer(1, 2 * mm),
                Paragraph("Sources: front-line driving roster, 1 October 2026; cab fit measurement programme, March 2025 to "
                          "September 2026; package data, tender HAS-F-2026-04; driver posture model, report EHF-2507.", small)]
    O.pdf(os.path.join(folder, PDF), story, title="2027 cab fit: drivers each shortlisted cab fails", author="Brenda Ward",
          created_pdf="20261009154900", producer="Microsoft® Excel® for Microsoft 365",
          creator="Microsoft® Excel® for Microsoft 365", footer="Fleet Services  Fleet and Estates Committee, 2027 cab "
          "specification", footer_font="Calibri")


def write_goldens(folder, A):
    os.makedirs(folder, exist_ok=True)
    workbook(folder, A)
    chart(folder, A)


def figures(gen_dir, A, S):
    fit = {r["id"]: r for r in A["cabs"]}
    fig = {"call": LABEL[A["best"]], "call_fail": fit[A["best"]]["fail"], "runner_up": LABEL[A["second"]],
           "runner_up_fail": fit[A["second"]]["fail"], "gap": A["gap"], "drivers": A["drivers"],
           "default_call": LABEL[A["default"][0]], "default_fail": S["rungs"]["R2"][A["default"][0]]["fail"],
           "default_runner_up_fail": S["rungs"]["R2"][A["default"][1]]["fail"],
           "decisive_extra": fit[A["default"][0]]["fail"] - S["rungs"]["R2"][A["default"][0]]["fail"],
           "vision_up_deg": int(P.VISION["up_deg"]), "vision_down_deg": int(P.VISION["down_deg"]),
           "backrest_along_in": P.SEAT_IN["backrest_along"], "backrest_behind_in": P.SEAT_IN["backrest_behind"],
           "wrenfold_sgrp_x": P.WRENFOLD_SGRP["FD35"][0], "wrenfold_sgrp_z": P.WRENFOLD_SGRP["FD35"][1],
           "rate_miles_unit": 100000}
    for r in A["cabs"]:
        fig["fail_%s" % r["id"]] = r["fail"]
        fig["women_%s" % r["id"]] = r["women"]
    for r in A["converters"]:
        k = r["converter"].split()[0].lower()
        for i, q in enumerate(r["jobs"]):
            fig["jobs_%s_q%d" % (k, i + 1)] = q
        fig["miles_%s" % k] = r["miles"]
        fig["jobs_rate_%s" % k] = r["rate"]
    for r in A["chassis"]:
        k = r["chassis"].lower()
        for i, q in enumerate(r["days"]):
            fig["vor_%s_q%d" % (k, i + 1)] = q
        fig["vy_%s" % k] = r["vehicle_years"]
        fig["vor_rate_%s" % k] = r["rate"]
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return fig
