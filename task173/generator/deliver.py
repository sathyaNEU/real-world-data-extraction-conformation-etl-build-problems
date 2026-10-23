"""task173 goldens: the forecast workbook (the 2027 forecast with its working and the two Form 3B tables) and the
monthly chart, from calc.py's computations on the shipped pack. Returns the figures the write-up states."""
from __future__ import annotations

import datetime as dt
import json
import os
from collections import defaultdict

import numpy as np

import common as C
import calc

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def r_to(x, u):
    return int(u * round(x / float(u)))


def monthly(P, reps, ex, g):
    """the 2027 forecast by month: the base on the record's month shares, the added repairs on the schedule"""
    cnt = defaultdict(int)
    for s, d, c in reps:
        if d and calc.W0 <= d <= calc.W1:
            cnt[d.month] += 1
    tot = sum(cnt.values())
    base_m = [g["base"] * cnt[m] / tot for m in range(1, 13)]
    cdf = calc.delay_profile(P, reps, ex)
    grid = np.arange(0, 181, 10)
    add = np.zeros(12)
    for d in calc.ami_exchanges(P):
        d0 = d + dt.timedelta(days=2)
        for m in range(1, 13):
            a = (dt.date(2027, m, 1) - d0).days
            b = (dt.date(2027 + (m == 12), m % 12 + 1, 1) - d0).days
            add[m - 1] += np.interp(min(max(b, 0), 180), grid, cdf) - np.interp(min(max(a, 0), 180), grid, cdf)
    add = add * g["excess"]
    return base_m, list(add)


def history_monthly(reps):
    cnt = defaultdict(int)
    for s, d, c in reps:
        if d and d >= dt.date(2021, 1, 1):
            cnt[(d.year, d.month)] += 1
    return cnt


def build(root, target):
    P = calc.Pack(target)
    reps = P.repairs()
    ex = P.exchanges()
    g = calc.golden(P, reps=reps, ex=ex)
    dflt = calc.default_path(P, reps)
    br = calc.ask_breaks(P)
    rs = calc.ask_restoration(target)
    base_m, add_m = monthly(P, reps, ex, g)
    figs = {
        "call.service_leak_repairs_2027": r_to(g["total"], 250),
        "step.forecast_2027_unrounded": round(g["total"], 1),
        "component.base_2027": r_to(g["base"], 100),
        "component.base_2027_unrounded": round(g["base"], 1),
        "component.ami_exchanges_2027": g["n_ami"],
        "component.added_per_100_exchanges": round(100 * g["excess"], 1),
        "component.added_per_100_exchanges_unrounded": round(100 * g["excess"], 3),
        "component.added_repairs_2027": r_to(g["induced"], 100),
        "step.record_repairs_per_year": round(dflt, 1),
        "step.record_exchanges_per_year": int(round(g["ex_per_year"])),
        "step.history_exchanges": g["n_exch_hist"],
        "step.history_window_repairs": g["hits"],
        "step.default_path": r_to(dflt, 250),
    }
    for (c, m), v in br.items():
        figs["ask_breaks.%s.%s" % (c.lower(), calc.MON[m].lower())] = v
    for c in C.CENTERS:
        figs["ask_breaks.%s.total" % c.lower()] = sum(br[(c, m)] for m in calc.FY_MONTHS)
    figs["ask_breaks.total"] = sum(br.values())
    for (gname, q), v in rs.items():
        figs["ask_restoration.%s.q%d" % (gname.lower().replace(" ", "_"), q)] = r_to(v, 10)
    figs["_monthly_2027"] = [round(a + b, 1) for a, b in zip(base_m, add_m)]
    gold = os.path.join(root, "golden")
    os.makedirs(gold, exist_ok=True)
    write_xlsx(os.path.join(gold, C.DELIV_XLSX), figs, g, dflt, br, rs, base_m, add_m)
    write_png(os.path.join(gold, C.DELIV_PNG), history_monthly(reps), base_m, add_m, figs)
    with open(os.path.join(root, "generator", "figures.json"), "w") as f:
        json.dump({k: v for k, v in figs.items() if not k.startswith("_")}, f, indent=1, sort_keys=True)
        f.write("\n")
    meta = {"task": "task173", "distractor_files": ["target/" + x for x in C.DISTRACTORS],
            "deliverables": [C.DELIV_XLSX, C.DELIV_PNG], "objective": "Forecasting & Predictive Modeling",
            "domain": "Energy Systems & Utilities / Asset Condition & Maintenance"}
    with open(os.path.join(root, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    return figs


def write_xlsx(path, figs, g, dflt, br, rs, base_m, add_m):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    import postprocess as PP
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 forecast"
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DDEBF7")
    thin = Side(style="thin", color="999999")
    ws["A1"] = "Item 101 water service leak repairs, calendar 2027 estimated quantity"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Distribution Division working file for ITB 27-0114. Record to 30 Sep 2026."
    rows = [
        ("Service leak repairs a year in the record, Oct 2024 to Sep 2026", round(dflt, 1), "EAM, one per leak repaired"),
        ("Meter exchanges a year in the same window", round(g["ex_per_year"], 1), "CIS meter history"),
        ("Added repairs per 100 meter exchanges (120 days after the new meter is set, less each service's base)",
         round(100 * g["excess"], 2), "%d exchanges 2012 to May 2026" % g["n_exch_hist"]),
        ("2027 repairs without exchange visits", round(g["base"], 1), "record rate less its own exchange-visit repairs"),
        ("AMI meter exchanges scheduled Feb to Jul 2027", g["n_ami"], "Halvorsen schedule rev. 4"),
        ("Added repairs from the AMI exchanges falling in 2027", round(g["induced"], 1), "delay profile from the record"),
        ("2027 service leak repairs", round(g["total"], 1), ""),
        ("Estimated quantity, Item 101 (nearest 250)", figs["call.service_leak_repairs_2027"], ""),
    ]
    ws.append([])
    ws.append(["", "Value", "Source"])
    for c in ws[4]:
        c.font = bold
        c.fill = head_fill
    for r in rows:
        ws.append(list(r))
    ws.cell(row=12, column=1).font = bold
    ws.cell(row=12, column=2).font = bold
    ws.append([])
    ws.append(["2027 by month", "Without exchange visits", "Added by AMI exchanges", "Forecast"])
    hr = ws.max_row
    for c in ws[hr]:
        c.font = bold
        c.fill = head_fill
    for i in range(12):
        ws.append([MONTHS[i] + " 2027", round(base_m[i], 1), round(add_m[i], 1), round(base_m[i] + add_m[i], 1)])
    ws.append(["Total", round(sum(base_m), 1), round(sum(add_m), 1), round(sum(base_m) + sum(add_m), 1)])
    for c in ws[ws.max_row]:
        c.font = bold
    ws.column_dimensions["A"].width = 64
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 30
    ws.column_dimensions["D"].width = 12
    for row in ws.iter_rows(min_row=5, max_row=12):
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
        v = row[1]
        if isinstance(v.value, float):
            v.number_format = "#,##0.0" if v.row != 7 else "0.00"
        elif isinstance(v.value, int):
            v.number_format = "#,##0"
    for row in ws.iter_rows(min_row=15, max_row=ws.max_row):
        for c in row[1:4]:
            c.number_format = "#,##0.0"
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Form 3B Item 201")
    ws2["A1"] = "Item 201 main break repairs, fiscal 2026, by service centre area and month of permanent repair"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    ws2.append(["Month"] + [c.title() for c in C.CENTERS] + ["Total"])
    for c in ws2[3]:
        c.font = bold
        c.fill = head_fill
    for m in calc.FY_MONTHS:
        v = [br[(cen, m)] for cen in C.CENTERS]
        ws2.append(["%s %d" % (calc.MON[m], 2025 if m >= 10 else 2026)] + v + [sum(v)])
    ws2.append(["FY 2026"] + [sum(br[(c, m)] for m in calc.FY_MONTHS) for c in C.CENTERS] + [sum(br.values())])
    for c in ws2[ws2.max_row]:
        c.font = bold
    ws2.column_dimensions["A"].width = 14
    for col in "BCDE":
        ws2.column_dimensions[col].width = 11

    ws3 = wb.create_sheet("Form 3B Items 301-305")
    ws3["A1"] = "Restoration accepted in pay estimates, fiscal 2026, square yards by surface type and quarter completed"
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.append([])
    ws3.append(["Surface type", "Q1 Oct-Dec", "Q2 Jan-Mar", "Q3 Apr-Jun", "Q4 Jul-Sep", "FY 2026"])
    for c in ws3[3]:
        c.font = bold
        c.fill = head_fill
    for gname in calc.GROUP_ORDER:
        v = [r_to(rs[(gname, q)], 10) for q in (1, 2, 3, 4)]
        ws3.append([gname] + v + [sum(v)])
    ws3.column_dimensions["A"].width = 24
    for col in "BCDEF":
        ws3.column_dimensions[col].width = 12
    ws3.append([])
    ws3.append(["Items 301 and 302 asphalt and concrete pavement, 303 and 304 sidewalk and driveway, 305 sod. "
                "Quantities as accepted (the revision Finance paid)."])
    ws4 = wb.create_sheet("Notes")
    notes = [
        "Item 101 counts one leak per repair on the City's side of the service (corporation stop through the meter "
        "outlet coupling), by completion date, City crews and contractor together (ITB 27-0114, sections 01 and 02).",
        "Record: EAM work orders from 17 May 2021 and the legacy system before it, to 30 Sep 2026; MIGRATED legacy "
        "orders counted once, in EAM; cancelled orders out.",
        "Exchange visits: a REMOVE and the next SET at a premise in the CIS meter history (new services excluded), "
        "tied to the GIS service through the premise's SERVICE_ID or its address.",
        "AMI: METER EXCHANGE rows of the Halvorsen schedule rev. 4 only; ENDPOINT RETROFIT leaves the meter in place "
        "and HOLD - CIP 2027 premises are reset by the main contractor.",
        "Form 3B Item 201: one break per main and report across its crew and contractor repair orders, at the "
        "permanent repair; centre from the GIS main layer.",
        "Form 3B Items 301 to 305: the revision Finance paid, matched to the voucher gross (two months on one "
        "invoice where the contractor billed them together); quarter of the restoration's completion.",
    ]
    ws4["A1"] = "Notes"
    ws4["A1"].font = bold
    for i, t in enumerate(notes, 3):
        ws4.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 110
    wb.save(path)
    PP.normalize_ooxml(path, "Mario Barnett", "Mario Barnett", "2026-10-21T14:12:00Z", "2026-10-21T19:47:00Z", excel=True)


def write_png(path, hist, base_m, add_m, figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    matplotlib.rcParams["svg.hashsalt"] = "task173"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    INK, MUTED, GRID, SURF = "#1f1f1e", "#6b6a63", "#e6e5df", "#fcfcfb"
    xs, ys = [], []
    y, m = 2021, 1
    while (y, m) <= (2026, 9):
        xs.append(dt.date(y, m, 15))
        ys.append(hist.get((y, m), 0))
        y, m = (y + (m == 12), m % 12 + 1)
    fx = [dt.date(2027, mm, 15) for mm in range(1, 13)]
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=120)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ax.plot(xs, ys, color="#2a78d6", lw=2, label="Repairs completed, Jan 2021 to Sep 2026")
    ax.bar(fx, base_m, width=25, color="#1baf7a", edgecolor=SURF, linewidth=1.5, label="2027 forecast without exchange visits")
    ax.bar(fx, add_m, width=25, bottom=base_m, color="#eb6834", edgecolor=SURF, linewidth=1.5,
           label="2027 forecast added by AMI meter exchanges (Feb to Jul)")
    peak = int(np.argmax(np.array(base_m) + np.array(add_m)))
    ax.annotate("%s in 2027" % "{:,}".format(figs["call.service_leak_repairs_2027"]),
                xy=(fx[peak], base_m[peak] + add_m[peak]), xytext=(0, 8), textcoords="offset points",
                ha="center", fontsize=9, color=INK)
    ax.axvspan(dt.date(2027, 2, 1), dt.date(2027, 7, 31), color="#f2f1ec", zorder=0)
    ax.set_ylabel("Service leak repairs per month", color=MUTED, fontsize=9)
    ax.set_title("Service leak repairs: about %s in 2027 as the AMI meter exchanges add to the usual workload"
                 % "{:,}".format(figs["call.service_leak_repairs_2027"]), fontsize=11, color=INK, loc="left")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(colors=MUTED, labelsize=8.5)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(0.22, 1.0), labelcolor=INK)
    fig.text(0.01, 0.01, "Source: EAM and legacy work orders, CIS meter history, AMI deployment schedule rev. 4. "
             "Shaded: AMI installation window.", fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, metadata={"Software": None}, facecolor=SURF)
    plt.close(fig)
