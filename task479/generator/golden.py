"""The golden deliverable, computed from the cut pack through bundle.py: Client Finance's 2027 funding true-up
workbook (each group's expected 2027 retained claims PMPM against its elected claims rate, the large claimants it
rests on, January to August 2026, and the 2026 advisories), and generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "mba_2027_funding_true_up.xlsx"
INK = "1B2430"
NAVY = "22395C"
PALE = "E6ECF4"
MUTED = "A3ACB8"
RED = "B4452F"


def compute(target):
    b = B.load(target)
    mm, gross = B.experience(b)
    cl = B.claimants(b)
    est = B.retained27(b, "golden")
    ret25 = {g: (gross[g] - sum(e for t, e, p in cl.get(g, []))) / mm[g] for g in b["groups"]}
    return {"b": b, "mm": mm, "gross": gross, "cl": cl, "est": est, "ret25": ret25,
            "notice": B.notices(b, est), "a": B.ask_a(b), "bb": B.ask_b(b)}


def write_xlsx(path, G):
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b = G["b"]
    wb = openpyxl.Workbook()
    hdr = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    hfill = PatternFill("solid", fgColor=NAVY)
    body = Font(name="Calibri", size=10, color=INK)
    bold = Font(name="Calibri", size=10, color=INK, bold=True)
    thin = Border(bottom=Side(style="thin", color="C3CAD3"))
    nfill = PatternFill("solid", fgColor=PALE)
    import csv
    emp = {}
    with open(os.path.join(os.path.dirname(path), "..", "target", "mba_group_roster_2026-10.csv")) as fh:
        for r in csv.DictReader(fh):
            emp[r["group_no"]] = r["employer"]

    def head(ws, row, cols, widths):
        for i, (h, w) in enumerate(zip(cols, widths), 1):
            c = ws.cell(row=row, column=i, value=h)
            c.font, c.fill = hdr, hfill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i <= 2 else "right")
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.row_dimensions[row].height = 32

    def title(ws, t, sub):
        ws["A1"] = t
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=INK)
        ws["A2"] = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6470")

    ws = wb.active
    ws.title = "True-up notices"
    n = G["notice"]
    title(ws, "%d of 16 groups get a 2027 funding true-up notice: %s" % (len(n), ", ".join(n)),
          "Expected 2027 retained claims per member per month on 2025 experience (incurred 2025, paid through "
          "31 March 2026) at 7.5 per cent trend a year, net of specific stop-loss at $250,000, against the claims "
          "component of each group's elected 2027 funding rate.")
    cols = ["Group", "Employer", "2025 member months", "2025 incurred claims ($)", "2025 retained PMPM ($)",
            "Members over $250,000 in 2027", "2027 expected retained PMPM ($)", "2027 claims component ($)",
            "Over (under) ($)", "Notice"]
    head(ws, 4, cols, [8, 30, 11, 15, 12, 12, 13, 13, 11, 8])
    F = B.F
    for i, g in enumerate(b["groups"]):
        over27 = sum(1 for t, e, p in G["cl"].get(g, []) if F * t > B.ATTACH)
        est, rate = G["est"][g], b["rates"][g]
        vals = [g, emp[g], G["mm"][g], round(G["gross"][g]), round(G["ret25"][g], 2), over27, round(est, 2), rate,
                round(est - rate, 2), "yes" if g in n else "no"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            c.font = bold if (g in n and j in (1, 2, 10)) else body
            c.border = thin
            if g in n:
                c.fill = nfill
            if j in (3, 4, 6):
                c.number_format = "#,##0"
            elif j in (5, 7, 8):
                c.number_format = "#,##0.00"
            elif j == 9:
                c.number_format = "#,##0.00;(#,##0.00)"
            if j >= 3:
                c.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "C5"
    r0 = 5 + len(b["groups"]) + 1
    for k, t in enumerate([
        "Each member's 2025 claims are trended two years at 7.5 per cent before the $250,000 specific deductible is "
        "applied: a member already over it costs the plan $250,000 in 2027 whatever the trend. Members under "
        "$100,000 in 2025 cannot reach the deductible at this trend, so the large claimant report carries every "
        "member the deductible touches.",
        "Pharmacy rebates are credited to the funding accounts and are not netted (assumptions memo, section 4). "
        "Claims paid after 31 March 2026 are outside the experience (section 2).",
    ]):
        c = ws.cell(row=r0 + k, column=1, value=t)
        c.font = Font(name="Calibri", size=9, color="5B6470")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + k, start_column=1, end_row=r0 + k, end_column=10)
        ws.row_dimensions[r0 + k].height = 38

    cs = wb.create_sheet("Chart data")
    cs.append(["Group", "2027 expected retained PMPM ($)", "2027 claims component ($)"])
    for g in b["groups"]:
        cs.append([g, round(G["est"][g], 2), b["rates"][g]])
    ch = BarChart()
    ch.type = "col"
    ch.title = "2027 expected retained claims PMPM against the elected claims component"
    ch.y_axis.title = "Dollars per member per month"
    ch.y_axis.numFmt = "#,##0"
    ch.y_axis.delete = False
    ch.x_axis.delete = False
    ch.x_axis.tickLblSkip = 1
    data = Reference(cs, min_col=2, min_row=1, max_col=3, max_row=len(b["groups"]) + 1)
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(b["groups"]) + 1))
    ch.series[0].graphicalProperties = GraphicalProperties(solidFill=NAVY)
    ch.series[1].graphicalProperties = GraphicalProperties(solidFill=MUTED)
    ch.gapWidth = 60
    ch.legend.position = "b"
    ch.height, ch.width = 10, 24
    ws.add_chart(ch, "A%d" % (r0 + 3))

    ls = wb.create_sheet("Large claimants")
    title(ls, "2025 large claimants carried to 2027", "Arbor Ridge's 2025 large claimant report; each member's claims "
                                                      "trended two years, the specific deductible applied after.")
    head(ls, 4, ["Group", "Claimant", "2025 claims ($)", "2027 claims ($)", "2027 retained ($)", "2027 excess ($)"],
         [8, 14, 14, 14, 14, 14])
    row = 5
    for r in sorted(b["lcr"], key=lambda r: (b["pol"][(r["policy_no"], 2025)], r["claimant_no"])):
        t = float(r["total_incurred"])
        vals = [b["pol"][(r["policy_no"], 2025)], r["claimant_no"], t, round(F * t, 2), round(min(F * t, B.ATTACH), 2),
                round(max(0.0, F * t - B.ATTACH), 2)]
        for j, v in enumerate(vals, 1):
            c = ls.cell(row=row, column=j, value=v)
            c.font, c.border = body, thin
            if j >= 3:
                c.number_format = "#,##0.00"
        row += 1
    ls.freeze_panes = "A5"

    a = wb.create_sheet("2026 to date")
    title(a, "January to August 2026", "Member months count each person once a month (members reissued new ids when "
                                       "their employer changed payroll vendor are counted once); paid claims are 2026 "
                                       "incurred claims paid through September 2026.")
    head(a, 4, ["Group", "Member months", "Paid claims PMPM ($)"], [8, 14, 16])
    for i, g in enumerate(b["groups"]):
        for j, (v, fm) in enumerate(((g, None), (G["a"][g][0], "#,##0"), (round(G["a"][g][1], 2), "#,##0.00")), 1):
            c = a.cell(row=5 + i, column=j, value=v)
            c.font, c.border = body, thin
            if fm:
                c.number_format = fm
    ad = wb.create_sheet("2026 advisories")
    title(ad, "Arbor Ridge's 2026 specific advisories", "Members flagged at $125,000, each counted once (a claimant "
                                                        "file reopened under a member's new id is the same member), at "
                                                        "the claims to date the carrier last reported.")
    head(ad, 4, ["Group", "Members flagged", "Claims to date ($)"], [8, 14, 16])
    for i, g in enumerate(b["groups"]):
        for j, (v, fm) in enumerate(((g, None), (G["bb"][g][0], "0"), (round(G["bb"][g][1]), "#,##0")), 1):
            c = ad.cell(row=5 + i, column=j, value=v)
            c.font, c.border = body, thin
            if fm:
                c.number_format = fm
    for w in wb.worksheets:
        w.sheet_view.showGridLines = False
        w.page_setup.orientation = "landscape"
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def figures(G):
    b = G["b"]
    dflt = B.retained27(b, "default")
    return {
        "call": {"notices": G["notice"]},
        "retained_pmpm": {g: "%d" % round(G["est"][g]) for g in b["groups"]},
        "ask_a": {g: {"member_months": G["a"][g][0], "paid_pmpm": "%.2f" % G["a"][g][1]} for g in b["groups"]},
        "ask_b": {g: {"members": G["bb"][g][0], "claims_to_date": int(round(G["bb"][g][1]))} for g in b["groups"]},
        "default_path": {"notices": B.notices(b, dflt), "retained_pmpm": {g: "%d" % round(dflt[g]) for g in b["groups"]}},
        "rates": {g: "%d" % round(b["rates"][g]) for g in b["groups"]},
        "conventions": {"trend_pct": 7.5, "deductible": 250000, "advisory": 125000, "lcr_floor": 100000,
                        "years": [2025, 2026, 2027], "counts": [2, 16]},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Claire Grant", "Claire Grant", "2026-10-07T18:40:00Z",
                       "2026-10-08T13:55:00Z", excel=True, company="Marlowe Benefit Administrators")
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
