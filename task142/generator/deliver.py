"""The golden deliverable (os_west_debiet_2027-2029.xlsx) and generator/figures.json, both from analysis.py's figures
on the cut pack."""
import datetime as dt
import json
import os

import numpy as np

import analysis as A

BOOK = "os_west_debiet_2027-2029.xlsx"
STAMP = (2026, 10, 16, 16, 40, 0)


def owed(F, M, gas_block):
    """Every figure the write-up states, as the generator computed it."""
    fam = list(M["fam"].values())
    pre = M["pre"]
    f = dict(F)
    f["drop_family_lo"] = round(min(fam), 1)
    f["drop_family_hi"] = round(max(fam), 1)
    f["pre_mean"] = round(pre[("PRE", "mean")], 1)
    f["pre_res_harm"] = round(pre[("PRE_RES", "harm")], 1)
    f["net_flow"] = round(M["net"][("ALL", "flow")], 1)
    f["design_drop"] = 40
    f["textbook_drop"] = 20
    f["return_like_lo"] = round(min(r for r, nr in M["returns"] if nr in M["like"]), 1)
    f["return_like_hi"] = round(max(r for r, nr in M["returns"] if nr in M["like"]), 1)
    f["return_other_lo"] = round(min(r for r, nr in M["returns"] if nr not in M["like"]), 1)
    f["return_other_hi"] = round(max(r for r, nr in M["returns"] if nr not in M["like"]), 1)
    H = M["H"]
    for name, d in (("r0", 40.0), ("r1", M["net"][("ALL", "flow")]), ("r2", pre[("PRE_RES", "harm")]),
                    ("r2m", pre[("PRE", "mean")]), ("side", 20.0)):
        f["%s_f3" % name] = round(M["KA"] / (A.CP * d), 1)
        f["%s_f6" % name] = round(M["KAB"] / (A.CP * d), 1)
    f["committed_m3h"] = (F["capacity_m3h"] or 0) - H
    f["cp"] = A.CP
    f["shortfall_exact"] = round(F["flow_2028_29_exact"] - H, 1)
    f["sections"] = "3.2 3.3 3.4"
    f["rounding_units"] = [5, 10, 100, 1000]
    f["gas_total_m3"] = A.rnd(sum(F["gas_m3_exact"].values()), 1000)
    f["blocks_n"] = len(M["loads"])
    return f


def workbook(F, M, gas_block, path):
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.chart.label import DataLabelList
    from openpyxl.chart.series import SeriesLabel
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.line import LineProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    hdr_fill = PatternFill("solid", fgColor="DDE6F0")
    bold = Font(bold=True)
    note = Font(italic=True, size=9, color="52514E")
    BLUE, ORANGE = "2A78D6", "EB6834"

    def header(ws, row, vals):
        for i, v in enumerate(vals, start=1):
            c = ws.cell(row=row, column=i, value=v)
            c.font = bold
            c.fill = hdr_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)

    H = M["H"]
    L = M["loads"]
    # ---- Seizoenen: the finding
    ws = wb.active
    ws.title = "Seizoenen"
    ws["A1"] = "OS West first runs short in the 2028-29 heating season"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Blocks connected by 1 October 2028 need %d m3/h of design-day flow against %d m3/h available; "
                "2027-28 holds at %d m3/h." % (F["flow_2028_29"], H, F["flow_2027_28"]))
    ws["A3"] = ("Sources: hydraulische toets OS West 9-10-2026 (available flow), warmteverliesberekening rev2 "
                "18-09-2026 (loads), fasering 30-09-2026 (phases), AMR meter year 2025-26 (drop %.1f K)." % F["drop_K"])
    ws["A3"].font = note
    header(ws, 5, ["Heating season", "Phases connected by 1 October", "Design heat load (kW)",
                   "Design-day flow (m3/h)", "Available flow (m3/h)", "Shortfall (m3/h)", "Result"])
    ws.append(["2027-28", "1-3", M["KA"], F["flow_2027_28"], H, 0, "holds"])
    ws.append(["2028-29", "1-6", M["KAB"], F["flow_2028_29"], H, F["shortfall_2028_29"], "short"])
    for r in ws.iter_rows(min_row=6, max_row=7, min_col=3, max_col=6):
        for c in r:
            c.number_format = "#,##0"
    ws.cell(row=7, column=7).font = Font(bold=True, color="9C2B10")
    ws.cell(row=9, column=1, value="Flows to the nearest 10 m3/h. CT-03 3.3 compares the unrounded flows (%.1f and "
                                   "%.1f m3/h) with the available flow." % (F["flow_2027_28_exact"],
                                                                         F["flow_2028_29_exact"])).font = note
    ch = BarChart()
    ch.type = "col"
    ch.title = "2028-29: %d m3/h against %d available" % (F["flow_2028_29"], H)
    ch.y_axis.title = "Design-day flow (m3/h)"
    ch.x_axis.title = "Heating season"
    ch.add_data(Reference(ws, min_col=4, min_row=5, max_row=7), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=6, max_row=7))
    bar = ch.series[0]
    bar.graphicalProperties = GraphicalProperties(solidFill=BLUE)
    bar.graphicalProperties.line = LineProperties(solidFill=BLUE)
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.showCatName = False
    ch.dataLabels.showSerName = False
    ch.dataLabels.showLegendKey = False
    ch.dataLabels.showPercent = False
    ch.dataLabels.position = "inEnd"
    ch.gapWidth = 120
    ln = LineChart()
    ln.add_data(Reference(ws, min_col=5, min_row=6, max_row=7), titles_from_data=False)
    ls = ln.series[0]
    ls.tx = SeriesLabel(v="Available flow, %d m3/h" % H)
    ls.graphicalProperties = GraphicalProperties()
    ls.graphicalProperties.line = LineProperties(solidFill=ORANGE, w=28575)
    ls.smooth = False
    ch.y_axis.scaling.min = 0
    ch.y_axis.scaling.max = 250
    ch.y_axis.majorUnit = 50
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="E3E2DE"))
    ch.y_axis.delete = False
    ch.x_axis.delete = False
    ch.legend.position = "b"
    ch += ln
    ch.height, ch.width = 8.5, 15.5
    ws.add_chart(ch, "A11")
    ws.freeze_panes = "A6"
    for col, wdt in zip("ABCDEFG", (15, 16, 14, 14, 14, 13, 9)):
        ws.column_dimensions[col].width = wdt
    # ---- Fasen
    ws = wb.create_sheet("Fasen")
    header(ws, 1, ["Phase", "Complexes", "Planned connection", "Design heat load (kW)", "Drop (K)",
                   "Design-day flow (m3/h)"])
    for ph in range(1, 7):
        bl = [b for b in L if b["phase"] == ph]
        ws.append([ph, ", ".join(b["code"] for b in bl), max(b["date"] for b in bl), F["phase_load_kW"][str(ph)],
                   F["drop_K"], F["phase_flow"][str(ph)]])
    ws.append(["Phases 1-3", None, None, M["KA"], None, None])
    ws.append(["Phases 1-6", None, None, M["KAB"], None, None])
    for r in (8, 9):
        ws.cell(row=r, column=1).font = bold
        ws.cell(row=r, column=4).font = bold
    for r in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        r[0].number_format = "dd-mm-yyyy"
    for r in ws.iter_rows(min_row=2, min_col=4, max_col=4):
        r[0].number_format = "#,##0"
    for r in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        r[0].number_format = "0.0"
    ws.cell(row=11, column=1, value="Design-day flow = design heat load / (1.163 x drop), CT-03 3.2; each phase to the "
                                    "nearest 5 m3/h. Planned connection is the phase's last complex.").font = note
    ws.freeze_panes = "A2"
    for col, wdt in zip("ABCDEF", (11, 26, 17, 18, 9, 18)):
        ws.column_dimensions[col].width = wdt
    # ---- Retourregime: the evidence for the drop
    ws = wb.create_sheet("Retourregime")
    header(ws, 1, ["Aansluitnummer", "Object", "Bouwjaar", "Return, cold days (C)", "Drop, cold days (K)",
                   "Original radiators"])
    T = M["T"]
    obj = {c["aansluitnummer"]: c["object"] for c in T["conns"]}
    per = A.per_connection(T, 0.0)
    rows = sorted(((float(np.mean(per[nr]["tr"])), nr) for nr in per), reverse=True)
    for r_, nr in rows:
        ws.append([nr, obj[nr], M["by"][nr], round(r_, 1), round(float(np.mean(per[nr]["dt"])), 1),
                   "yes" if nr in M["like"] else ""])
    for r in ws.iter_rows(min_row=2, min_col=4, max_col=5):
        for c in r:
            c.number_format = "0.0"
    n = len(rows) + 3
    ws.cell(row=n, column=1, value="Cold days: daily mean at the Lekstede weather station of 0 C or lower in the "
                                   "2025-26 meter year (%d days). Returns split between %.1f and %.1f C." %
                                   (F["cold_days"], F["return_gap_C"][0], F["return_gap_C"][1])).font = note
    ws.cell(row=n + 1, column=1, value="Original-radiator connections: mean cold-day drop %.1f K over %d connections."
                                       % (F["drop_K"], F["like_n"])).font = note
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:F%d" % (len(rows) + 1)
    for col, wdt in zip("ABCDEF", (15, 34, 10, 19, 18, 17)):
        ws.column_dimensions[col].width = wdt
    # ---- Gas
    ws = wb.create_sheet("Gas")
    header(ws, 1, ["Phase", "Complexes", "Gas 1 Oct 2025 to 1 Oct 2026 (m3)"])
    for ph in range(1, 7):
        bl = [b for b in L if b["phase"] == ph]
        ws.append([ph, ", ".join(b["code"] for b in bl), F["gas_m3"][str(ph)]])
    tot = A.rnd(sum(F["gas_m3_exact"].values()), 1000)
    ws.append(["Total", None, tot])
    ws.cell(row=8, column=1).font = bold
    ws.cell(row=8, column=3).font = bold
    for r in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        r[0].number_format = "#,##0"
    ws.cell(row=10, column=1, value="Boiler-room meters, with the old EANs of the two boiler rooms re-registered in "
                                    "2026 and the four meters exchanged in 2025-26; each phase to the nearest 1,000 "
                                    "m3, the total from the unrounded phases.").font = note
    ws.freeze_panes = "A2"
    for col, wdt in zip("ABC", (7, 26, 30)):
        ws.column_dimensions[col].width = wdt
    # ---- Warmte
    ws = wb.create_sheet("Warmte")
    header(ws, 1, ["Category", "2024-25 (MWh)", "2025-26 (MWh)", "Change (MWh)"])
    for k in ("Woningen", "Utiliteit"):
        ws.append([k, F["heat_2425_MWh"][k], F["heat_2526_MWh"][k], F["heat_change_MWh"][k]])
    for r in ws.iter_rows(min_row=2, min_col=2, max_col=4):
        for c in r:
            c.number_format = "#,##0;-#,##0"
    ws.cell(row=5, column=1, value="Gas years 1 October to 1 October. 2024-25 runs from the drive-by annual reads to the "
                                   "AMR opening registers across the summer 2025 migration; Woningen to the nearest "
                                   "1,000 MWh, Utiliteit to the nearest 100 MWh.").font = note
    ws.freeze_panes = "A2"
    for col, wdt in zip("ABCD", (12, 15, 15, 14)):
        ws.column_dimensions[col].width = wdt
    # ---- Toelichting
    ws = wb.create_sheet("Toelichting")
    notes = [
        ("Question", "First heating season in which OS West runs short of design-day flow as the Weidehaven blocks "
                     "connect (CT-03 v3, 3.3)."),
        ("Design-day flow", "Design heat load / (1.163 x drop the installation makes at the connection on days with a "
                            "daily mean of 0 C or lower), CT-03 3.2."),
        ("Drop used", "%.1f K: the blocks keep their radiators (scope v1.2, section 2); the network's connections on "
                      "original radiators are the high-return group on sheet Retourregime." % F["drop_K"]),
        ("Available flow", "%d m3/h, hydraulic test OS West of 9 October 2026 (capacity %s less committed %d)." %
         (H, "{:,}".format(F["capacity_m3h"]), F["capacity_m3h"] - H)),
        ("Loads", "Design heat loss, revision 2 of 18 September 2026 (replaces the March concept, CT-03 3.4)."),
        ("As of", "16 October 2026."),
        ("Prepared by", "Elif Meeusen, Network Planning."),
    ]
    header(ws, 1, ["Item", "Note"])
    for a, b in notes:
        ws.append([a, b])
    for r in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        r[0].alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 100
    when = dt.datetime(2026, 10, 16, 16, 40)
    for k in ("creator", "lastModifiedBy"):
        setattr(wb.properties, k, "Elif Meeusen")
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.title = "OS West design-day flow 2027-2029"
    wb.save(path)
    from pack import normalise_zip
    normalise_zip(path, "2026-10-16T14:40:00Z")


def write_all(target, golden_dir, gen_dir):
    os.makedirs(golden_dir, exist_ok=True)
    os.makedirs(gen_dir, exist_ok=True)
    F, M, gas_block = A.figures(target)
    workbook(F, M, gas_block, os.path.join(golden_dir, BOOK))
    fo = owed(F, M, gas_block)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(fo, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return F, M
