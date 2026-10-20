"""The golden deliverable, computed from the shipped pack alone: halbrook_2027_hospital_quality_bonus.xlsx (the
determination, the linkage correction, the chart and the notes), and generator/figures.json with every figure the
write-up states."""
import json
import os
import sys

import openpyxl
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import DataPoint
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bundle as B   # noqa: E402
import methods as M  # noqa: E402
import world as W    # noqa: E402

CLS_NAME = {"ssn": "Social Security number on file", "simple": "No number on file, single surname",
            "compound": "No number on file, two-part surname"}
NAVY = "1F3A5F"
FILL_H = PatternFill("solid", fgColor="DDE5EC")
FILL_L = PatternFill("solid", fgColor="F6E3E3")
THIN = Side(style="thin", color="A9B4BC")


def r100(v):
    return int(round(v / 100.0)) * 100


def compute(target):
    P = B.Pack(target)
    g = P.determination()
    f = P.frame()
    R = g["rates"]
    U = f[~f["known_death"] & ~f["alive_after"]]
    cells = {}
    for (h, k), u in U.groupby(["hosp", "cls"]):
        r, fp = R[k][0], R[k][1]
        L, N = float(u["linked"].sum()), float(len(u))
        cells[(h, k)] = (int(N), int(L), (L - fp * N) / (r - fp))
    pay = P.payments()
    bonus = {h: W.BONUS_RATE * pay[h] for h in W.CANDIDATES}
    reflex = P.determination(how="reflex")
    pos = f[f["known_death"]].groupby("cls")["linked"].agg(["size", "sum"])
    neg = f[f["alive_after"]].groupby("cls")["linked"].agg(["size", "sum"])
    hosp = []
    for h in W.CANDIDATES:
        est = sum(cells.get((h, k), (0, 0, 0.0))[2] for k in M.CLASSES)
        hosp.append(dict(name=h, short=W.SHORT[h], index_admissions=int(g["n"][h]),
                         expected=round(float(g["expected"][h]), 1), known_deaths=int(g["known"][h]),
                         after_discharge=round(est, 1), deaths=round(float(g["deaths"][h]), 1),
                         ratio=round(float(g["ratio"][h]), 2), ratio_raw=float(g["ratio"][h]),
                         verdict="loses" if h in g["losers"] else "keeps", payments=round(pay[h], 2),
                         bonus=r100(bonus[h]), bonus_raw=bonus[h]))
    rates = {k: dict(recall=round(R[k][0], 3), false_link=round(R[k][1], 4), pos=int(pos.loc[k, "size"]),
                     pos_linked=int(pos.loc[k, "sum"]), neg=int(neg.loc[k, "size"]), neg_linked=int(neg.loc[k, "sum"]))
             for k in M.CLASSES}
    total_raw = sum(bonus.values())
    out = dict(count_lose=len(g["losers"]), lose=[W.SHORT[h] for h in g["losers"]],
               lose_full=list(g["losers"]), keep=[W.SHORT[h] for h in W.CANDIDATES if h not in g["losers"]],
               hospitals=hosp, total_bonus=r100(total_raw), total_bonus_raw=total_raw,
               rates=rates,
               cells={"%s|%s" % (h, k): v for (h, k), v in cells.items()},
               reflex=dict(lose=[W.SHORT[h] for h in reflex["losers"]], count=len(reflex["losers"])),
               index_total=int(sum(g["n"].values())), threshold=W.THRESHOLD, spec_sections=[2.1, 2.4, 5.2],
               model_version=3.2, rounding_dollars=100)
    return out


def write_workbook(path, fig):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Determination"
    words = {4: "Four", 5: "Five", 6: "Six"}
    ws["A1"] = ("%s of 14 network hospitals lose the 2027 Hospital Quality Bonus on fiscal 2026 mortality" %
                words.get(fig["count_lose"], str(fig["count_lose"])))
    ws["A1"].font = Font(bold=True, size=13, color=NAVY)
    ws["A2"] = ("%s and %s. Quality Measurement, October 9, 2026, for the value-based payment filing due November 1, "
                "2026." % (", ".join(fig["lose"][:-1]), fig["lose"][-1]))
    ws["A2"].font = Font(size=10, italic=True)
    head = ["Hospital", "Index admissions", "Expected deaths", "Deaths on the bills", "Deaths after discharge, "
            "linkage corrected", "Deaths", "Mortality ratio", "2027 bonus", "Halbrook inpatient payments, stays "
            "discharged fiscal 2026", "Bonus at stake (2 per cent, nearest $100)"]
    for j, h in enumerate(head, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = FILL_H
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if j > 1 else "left")
        c.border = Border(bottom=THIN)
    for i, r in enumerate(fig["hospitals"], 5):
        vals = [r["name"], r["index_admissions"], r["expected"], r["known_deaths"], r["after_discharge"], r["deaths"],
                r["ratio"], "Loses" if r["verdict"] == "loses" else "Keeps", r["payments"], r["bonus"]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i, column=j, value=v)
            c.number_format = {2: "#,##0", 3: "#,##0.0", 4: "#,##0", 5: "#,##0.0", 6: "#,##0.0", 7: "0.00",
                               9: "$#,##0", 10: "$#,##0"}.get(j, "General")
            if j == 8:
                c.alignment = Alignment(horizontal="center")
            if r["verdict"] == "loses":
                c.fill = FILL_L
    t = 5 + len(fig["hospitals"])
    ws.cell(row=t, column=1, value="Network").font = Font(bold=True)
    for j, key in ((2, "index_admissions"), (3, "expected"), (4, "known_deaths"), (9, "payments")):
        c = ws.cell(row=t, column=j, value=round(sum(r[key] for r in fig["hospitals"]), 2))
        c.number_format = {2: "#,##0", 3: "#,##0.0", 4: "#,##0", 9: "$#,##0"}[j]
        c.font = Font(bold=True)
    c = ws.cell(row=t, column=10, value=fig["total_bonus"])
    c.number_format = "$#,##0"
    c.font = Font(bold=True)
    ws.cell(row=t + 2, column=1, value=("A hospital loses the bonus when its mortality ratio, deaths over expected "
                                        "deaths, exceeds %.2f (specification 5.2). Rows shaded are the hospitals that "
                                        "lose it." % W.THRESHOLD)).font = Font(size=9, italic=True)
    ws.cell(row=t + 3, column=1, value=("The network total at stake is 2 per cent of all fourteen hospitals' payments, "
                                        "rounded once; it equals the sum of the fourteen rounded figures.")).font = Font(
        size=9, italic=True)
    widths = [30, 11, 10, 10, 13, 9, 10, 9, 17, 15]
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.row_dimensions[4].height = 58
    ws.freeze_panes = "B5"

    lc = wb.create_sheet("Linkage correction")
    lc["A1"] = "The linkage's error rates by identifier class, and each hospital's deaths after discharge"
    lc["A1"].font = Font(bold=True, size=12, color=NAVY)
    hdr = ["Identifier class", "Deaths the bills record", "of them linked", "Share linked",
           "Members alive after day 30", "of them linked", "Share linked"]
    for j, h in enumerate(hdr, 1):
        c = lc.cell(row=3, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = FILL_H
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, k in enumerate(M.CLASSES, 4):
        r = fig["rates"][k]
        for j, v in enumerate([CLS_NAME[k], r["pos"], r["pos_linked"], r["pos_linked"] / r["pos"], r["neg"],
                               r["neg_linked"], r["neg_linked"] / r["neg"]], 1):
            c = lc.cell(row=i, column=j, value=v)
            if j in (4, 7):
                c.number_format = "0.0%" if j == 4 else "0.00%"
    lc.cell(row=8, column=1, value=("Deaths the bills record: index admissions whose bill, or a later bill within the "
                                    "30 days, closed with patient status 20. Alive after day 30: members with a service "
                                    "line, an admission or a live discharge after day 30. Each class's share of "
                                    "recorded deaths linked is the linkage's chance of finding a death; its share of "
                                    "members alive after day 30 linked is its chance of linking a living member to a "
                                    "death."))
    lc.cell(row=8, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    lc.merge_cells("A8:G8")
    lc.row_dimensions[8].height = 54
    h2 = ["Hospital", "Identifier class", "Index admissions neither recorded dead nor seen after day 30", "Linked",
          "Deaths after discharge estimated"]
    for j, h in enumerate(h2, 1):
        c = lc.cell(row=10, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = FILL_H
        c.alignment = Alignment(wrap_text=True, vertical="center")
    row = 11
    for h in W.CANDIDATES:
        for k in M.CLASSES:
            key = "%s|%s" % (h, k)
            if key not in fig["cells"]:
                continue
            n, l, e = fig["cells"][key]
            for j, v in enumerate([h, CLS_NAME[k], n, l, round(e, 2)], 1):
                c = lc.cell(row=row, column=j, value=v)
                if j == 5:
                    c.number_format = "0.00"
            row += 1
    lc.cell(row=row + 1, column=1, value=("Estimated deaths in a cell: (linked less the class's false-link share times "
                                          "the admissions) divided by (the class's share of deaths linked less its "
                                          "false-link share)."))
    for j, w in enumerate([30, 34, 22, 12, 22, 16, 12], 1):
        lc.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    lc.row_dimensions[3].height = 32
    lc.row_dimensions[10].height = 44
    lc.freeze_panes = "A4"

    ch = wb.create_sheet("Chart")
    ch["A1"] = "Hospital"
    ch["B1"] = "Mortality ratio"
    ch["C1"] = "Bonus line"
    for i, r in enumerate(fig["hospitals"], 2):
        ch.cell(row=i, column=1, value=r["short"])
        ch.cell(row=i, column=2, value=r["ratio"]).number_format = "0.00"
        ch.cell(row=i, column=3, value=W.THRESHOLD).number_format = "0.00"
    n = len(fig["hospitals"])
    bar = BarChart()
    bar.type = "col"
    bar.title = "Fiscal 2026 mortality ratio by hospital against the 1.15 bonus line"
    bar.y_axis.title = "Deaths over expected deaths"
    bar.y_axis.numFmt = "0.00"
    bar.y_axis.scaling.min = 0
    bar.y_axis.scaling.max = 1.8
    data = Reference(ch, min_col=2, min_row=1, max_row=n + 1)
    cats = Reference(ch, min_col=1, min_row=2, max_row=n + 1)
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(cats)
    s = bar.series[0]
    s.graphicalProperties.solidFill = "7F93A8"
    s.graphicalProperties.line.solidFill = "7F93A8"
    for i, r in enumerate(fig["hospitals"]):
        if r["verdict"] == "loses":
            pt = DataPoint(idx=i)
            pt.graphicalProperties.solidFill = "A23B3B"
            pt.graphicalProperties.line.solidFill = "A23B3B"
            s.dPt.append(pt)
    s.dLbls = DataLabelList()
    s.dLbls.showVal = True
    s.dLbls.numFmt = "0.00"
    line = LineChart()
    line.add_data(Reference(ch, min_col=3, min_row=1, max_row=n + 1), titles_from_data=True)
    ls = line.series[0]
    ls.graphicalProperties.line.solidFill = "1B1D1F"
    ls.graphicalProperties.line.dashStyle = "dash"
    ls.graphicalProperties.line.width = 19050
    ls.smooth = False
    bar += line
    bar.legend.position = "b"
    bar.width = 26
    bar.height = 12
    ch.add_chart(bar, "E2")
    ch.column_dimensions["A"].width = 16
    ch.column_dimensions["B"].width = 15
    ch.column_dimensions["C"].width = 11

    nt = wb.create_sheet("Notes")
    notes = [
        ("Notes", True),
        ("Measure: Halbrook Hospital Quality Bonus, contract year 2027, measure specification v1.0 (May 12, 2025).",
         False),
        ("Index admissions: specification 2.1 to 2.4, from Halbrook's inpatient claims (extract of October 5, 2026) and "
         "Carrisford Medical Group's inpatient encounters (file of October 6, 2026), each stay as last corrected, "
         "voided and deleted bills left out; Mercy Valley's two NPIs both mapped to Mercy Valley.", False),
        ("Expected deaths: HIMM 3.2 scores (run of October 2, 2026), summed over each hospital's index admissions.",
         False),
        ("Deaths: deaths the bills and encounters record (patient status 20 on the stay, a transfer stay or a later "
         "stay inside the 30 days), plus deaths after discharge estimated from the Office of Vital Records' return of "
         "October 7, 2026, corrected class by class for the links that find no death and the deaths no link finds, at "
         "the rates the 'Linkage correction' sheet measures on the recorded deaths and on the members seen alive after "
         "day 30.", False),
        ("Bonus at stake: 2 per cent of the payments Halbrook made for inpatient stays discharged July 1, 2025 to June "
         "30, 2026 (specification 5.3), Carrisford's stays left out. Bills as each system recorded them: a CPS "
         "replacement carries the change in payment and adds to its original, a platform replacement carries the "
         "stay's full payment and stands in its original's place, a voided bill pays nothing. Added: the additional "
         "payments Provider Disputes' log shows made by September 30, 2026 on those stays, except where the payment "
         "was the replacement bill itself (paid the same day, its change the additional payment), which the bills "
         "already count.", False),
        ("Rounding: ratios to two decimals, deaths and expected deaths to one, bonus figures to the nearest $100 from "
         "the unrounded payments.", False),
    ]
    for i, (t, b) in enumerate(notes, 1):
        c = nt.cell(row=i, column=1, value=t)
        c.font = Font(bold=b, size=12 if b else 10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 120
    wb.save(path)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    fig = compute(target)
    out = os.path.join(gdir, W.GOLDEN["workbook"])
    write_workbook(out, fig)
    import postprocess as PP
    PP.normalize_ooxml(out, W.PEOPLE["analyst"], W.PEOPLE["analyst"], "2026-10-08T15:12:00Z", "2026-10-09T21:47:36Z",
                       excel=True, company=W.PLAN)
    slim = {"call": {"lose": sorted(fig["lose_full"]), "count_in_set": fig["count_lose"]},
            "bonus": {r["name"]: r["bonus"] for r in fig["hospitals"]}}
    slim.update({k: v for k, v in fig.items() if k != "cells"})
    for r in slim["hospitals"]:
        r.pop("ratio_raw", None)
        r["bonus_raw"] = round(r["bonus_raw"], 2)
    slim["total_bonus_raw"] = round(slim["total_bonus_raw"], 2)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(slim, fh, indent=1)
        fh.write("\n")
    return fig


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
