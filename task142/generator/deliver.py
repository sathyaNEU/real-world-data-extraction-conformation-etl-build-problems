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
    f["gas_total_m3"] = A.rnd(sum(F["gas_m3_exact"].values()), 1000)
    f["blocks_n"] = len(M["loads"])
    return f


def workbook(F, M, gas_block, path):
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.chart.label import DataLabelList
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    hdr_fill = PatternFill("solid", fgColor="DDE6F0")
    bold = Font(bold=True)

    def header(ws, row, vals):
        for i, v in enumerate(vals, start=1):
            c = ws.cell(row=row, column=i, value=v)
            c.font = bold
            c.fill = hdr_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)

    H = M["H"]
    L = M["loads"]
    # ---- Seizoenen
    ws = wb.active
    ws.title = "Seizoenen"
    ws["A1"] = "OS West: design-day flow of the Weidehaven blocks against the available flow"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Hydraulic test of 9 October 2026 (available %d m3/h); rev2 heat-load study of 18 September 2026; "
                "drop %.1f K, the cold-day drop of the network's original-radiator connections (sheet Retourregime)."
                % (H, F["drop_K"]))
    ws["A3"] = "First season short: %s" % F["call"]
    ws["A3"].font = bold
    header(ws, 5, ["Heating season", "Phases connected by 1 October", "Design heat load (kW)",
                   "Design-day flow (m3/h)", "Available flow (m3/h)", "Shortfall (m3/h)", "Result"])
    ws.append(["2027-28", "1-3", M["KA"], F["flow_2027_28"], H, 0, "holds"])
    ws.append(["2028-29", "1-6", M["KAB"], F["flow_2028_29"], H, F["shortfall_2028_29"], "short"])
    for r in ws.iter_rows(min_row=6, max_row=7, min_col=3, max_col=6):
        for c in r:
            c.number_format = "#,##0"
    ws.cell(row=9, column=1, value="Flows rounded to the nearest 10 m3/h; the test compares unrounded flows "
                                   "(%.1f and %.1f m3/h) with the available flow." % (F["flow_2027_28_exact"],
                                                                                        F["flow_2028_29_exact"]))
    ch = BarChart()
    ch.type = "col"
    ch.title = "OS West design-day flow by heating season"
    ch.y_axis.title = "m3/h"
    ch.x_axis.title = "Heating season"
    data = Reference(ws, min_col=4, min_row=5, max_row=7)
    cats = Reference(ws, min_col=1, min_row=6, max_row=7)
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ln = LineChart()
    ln.add_data(Reference(ws, min_col=5, min_row=5, max_row=7), titles_from_data=True)
    ch.y_axis.scaling.min = 0
    ch.y_axis.scaling.max = 250
    ch += ln
    ch.height, ch.width = 8.5, 15
    ws.add_chart(ch, "A11")
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
    for r in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        r[0].number_format = "dd-mm-yyyy"
    for r in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        r[0].number_format = "0.0"
    ws.cell(row=9, column=1, value="Design-day flow = design heat load / (1.163 x drop), CT-03 3.2; rounded to the "
                                   "nearest 5 m3/h.")
    for col, wdt in zip("ABCDEF", (7, 26, 17, 18, 9, 18)):
        ws.column_dimensions[col].width = wdt
    # ---- Retourregime
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
    n = len(rows) + 3
    ws.cell(row=n, column=1, value="Cold days: daily mean at the Lekstede station of 0 C or lower, 2025-26 (%d days)."
                                   % F["cold_days"])
    ws.cell(row=n + 1, column=1, value="Original-radiator connections: mean cold-day drop %.1f K (%d connections)."
                                       % (F["drop_K"], F["like_n"]))
    for col, wdt in zip("ABCDEF", (15, 34, 10, 19, 18, 17)):
        ws.column_dimensions[col].width = wdt
    # ---- Gas
    ws = wb.create_sheet("Gas")
    header(ws, 1, ["Phase", "Complexes", "Gas 1 Oct 2025 to 1 Oct 2026 (m3)"])
    for ph in range(1, 7):
        bl = [b for b in L if b["phase"] == ph]
        ws.append([ph, ", ".join(b["code"] for b in bl), F["gas_m3"][str(ph)]])
    for r in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        r[0].number_format = "#,##0"
    ws.cell(row=9, column=1, value="Boiler-room meters including the EANs re-registered in 2026 and the meters "
                                   "exchanged in 2025-26; rounded to the nearest 1,000 m3.")
    for col, wdt in zip("ABC", (7, 26, 30)):
        ws.column_dimensions[col].width = wdt
    # ---- Warmte
    ws = wb.create_sheet("Warmte")
    header(ws, 1, ["Category", "2024-25 (MWh)", "2025-26 (MWh)", "Change (MWh)"])
    for k in ("Woningen", "Utiliteit"):
        ws.append([k, F["heat_2425_MWh"][k], F["heat_2526_MWh"][k], F["heat_change_MWh"][k]])
    for r in ws.iter_rows(min_row=2, min_col=2, max_col=4):
        for c in r:
            c.number_format = "#,##0"
    ws.cell(row=5, column=1, value="Gas years 1 October to 1 October; Woningen to the nearest 1,000 MWh, Utiliteit to "
                                   "the nearest 100 MWh.")
    for col, wdt in zip("ABCD", (12, 15, 15, 14)):
        ws.column_dimensions[col].width = wdt
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
