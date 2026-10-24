"""The golden deliverables: the 2025-26 periodic inventory workbook (the EIS nonpoint layout by area and SCC, the
recalculated 2014 base year beside it, the counties' remainder, the 2014 counts traced to the registry) and the
determinations file; returns every graded figure for figures.json."""
import csv

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import world as W
import golden as G

AREA = {a[0]: a for a in W.AREAS}


def r1(x):
    return float(round(x + 1e-9, 1))


def write(path, ev, aa, ab):
    import pack as P
    figs = dict(call=dict(triggered=sorted(AREA[c][1] for c in W.CODES if ev[c]["trigger"])), areas={}, cells={},
                ask_a={}, ask_b={}, constants=dict(tons_per_cord=W.TONS_PER_CORD, bag_lb=int(W.BAG_LB),
                                                   tool_secondary=P.TOOL_SECONDARY))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory 2025-26"
    ws.append(["Selwick Basin Clean Air Agency: residential wood combustion, 2025-26 periodic inventory and the 2014 "
               "base year recalculated on its methods"])
    ws.append([])
    head = ["Maintenance area", "County", "SCC", "SCC description", "Appliances 2025-26", "Wood burned 2025-26 (tons)",
            "PM2.5 2025-26 (tons)", "Appliances 2014", "Wood burned 2014 (tons)", "PM2.5 2014 (tons)"]
    ws.append(head)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for code in W.CODES:
        x = ev[code]
        for cl in W.CL:
            k = x["cls"][cl]
            w26, w14 = W.tons_of(cl, k["a26"]), W.tons_of(cl, k["a14"])
            ws.append([x["name"], x["county"], W.CLASSES[cl][0], W.CLASSES[cl][1], k["n26"], r1(w26), r1(k["pm26"]),
                       k["n14"], r1(w14), r1(k["pm14"])])
            figs["cells"]["%s.%s" % (x["name"], W.CLASSES[cl][0])] = dict(wood26=r1(w26), pm26=r1(k["pm26"]),
                                                                          wood14=r1(w14), pm14=r1(k["pm14"]))
        ws.append([x["name"] + " total", x["county"], None, None, None, None, r1(x["pm26"]), None, None, r1(x["pm14"])])
        for c in ws[ws.max_row]:
            c.font = Font(bold=True)
    for i, w in enumerate([18, 10, 12, 50, 12, 14, 12, 12, 14, 12], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A4"
    rm = wb.create_sheet("Remainder 2025-26")
    rm.append(["County", "SCC", "SCC description", "Wood burned 2025-26 (tons)", "PM2.5 2025-26 (tons)"])
    for c in rm[1]:
        c.font = Font(bold=True)
    for county in W.COUNTIES:
        for cl in W.CL:
            b = ab[county, cl]
            rm.append([county, W.CLASSES[cl][0], W.CLASSES[cl][1], r1(b["wood"]), r1(b["pm"])])
            figs["ask_b"]["%s.%s" % (county, W.CLASSES[cl][0])] = dict(wood=r1(b["wood"]), pm=r1(b["pm"]))
    for i, w in enumerate([10, 12, 50, 16, 14], 1):
        rm.column_dimensions[get_column_letter(i)].width = w
    cn = wb.create_sheet("2014 counts")
    cn.append(["Maintenance area", "SCC", "Plan's 2014 count", "Registry, in place in 2014 (2020 boundaries)",
               "Registered after the plan's extract", "Parcel left the area in 2020"])
    for c in cn[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for code in W.CODES:
        for cl in W.CL:
            a = aa[code, cl]
            cn.append([AREA[code][1], W.CLASSES[cl][0], a["plan"], a["registry"], a["late"], a["left"]])
            figs["ask_a"]["%s.%s" % (AREA[code][1], W.CLASSES[cl][0])] = dict(registry=a["registry"], late=a["late"],
                                                                              left=a["left"])
    for i, w in enumerate([18, 12, 14, 22, 20, 18], 1):
        cn.column_dimensions[get_column_letter(i)].width = w
    nt = wb.create_sheet("Notes")
    for line in ["Season 1 October 2025 to 30 April 2026; appliances in place in the season on the 2020 boundaries, each "
                 "device once (the registry of 30 June 2026 and the parcel crosswalk).",
                 "Activity: the 2024-25 household survey, each area's respondents by appliance class, face cords at a "
                 "third of a cord, pickup loads at half, 1.163 tons per cord, pellets in tons (40-pound bags).",
                 "2014 base year: the plan's 2014 count, each appliance at the survey's wood burned for its class; the "
                 "stoves and outdoor boilers changed out since 2015 at the survey's wood burned for their class and the "
                 "heat status on their applications, the certified and pellet stoves at the survey's units installed by "
                 "2014.",
                 "Factors: the 2023 table. Tons and percentages rounded to one decimal for display; determinations on "
                 "unrounded values."]:
        nt.append([line])
    nt.column_dimensions["A"].width = 120
    wb.save(path("inventory"))
    with open(path("determinations"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["maintenance_area", "county", "pm25_2014_base_tons", "pm25_2025_26_tons", "reduction_pct",
                    "commitment_pct", "determination", "effective_season"])
        for code in W.CODES:
            x = ev[code]
            det = "TRIGGERED" if x["trigger"] else "NOT TRIGGERED"
            w.writerow([x["name"], x["county"], "%.1f" % x["pm14"], "%.1f" % x["pm26"], "%.1f" % x["reduction"],
                        x["commit"], det, "2026-27"])
            figs["areas"][x["name"]] = dict(pm14=r1(x["pm14"]), pm26=r1(x["pm26"]), reduction=r1(x["reduction"]),
                                            commitment=x["commit"], determination=det,
                                            rungs={k: r1(v) for k, v in x["rungs"].items()})
    return figs
