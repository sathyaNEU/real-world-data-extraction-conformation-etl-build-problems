"""The golden deliverable, computed from the cut pack through bundle.py: the cooperative's January 2027 contribution
review workbook (each district's expected plan year 2026 plan-paid PMPM against its 2026 claims component, the plan-year
factors it rests on, July to September 2026 member months and the 2026 advisories), and generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "mvshc_january_2027_contribution_review.xlsx"
INK = "1B2430"
GREEN = "2C5A3F"
PALE = "E7EFE9"
MUTED = "A3ACB8"
ACCENT = "B4452F"
NAMES = "mvshc_2026_contribution_rates.xlsx"


def r10(v):
    return int(10 * round(v / 10))


def compute(target):
    b = B.load(target)
    est = B.expected(b, "golden")
    k = B.factors_by_design(b)
    return {"b": b, "est": est, "k": k, "raised": B.raised(b, est), "a": B.ask_a(b), "bb": B.ask_b(b),
            "h1": {d: B.h1(b, d) for d in b["ids"]}}


def write_xlsx(path, G, target):
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b = G["b"]
    names = {}
    ws0 = openpyxl.load_workbook(os.path.join(target, NAMES), data_only=True)["2026 rates"]
    for r in ws0.iter_rows(min_row=5, values_only=True):
        if r[0]:
            names[r[0]] = r[1]
    wb = openpyxl.Workbook()
    hdr = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    hfill = PatternFill("solid", fgColor=GREEN)
    body = Font(name="Calibri", size=10, color=INK)
    bold = Font(name="Calibri", size=10, color=INK, bold=True)
    thin = Border(bottom=Side(style="thin", color="C3CAD3"))
    nfill = PatternFill("solid", fgColor=PALE)

    def head(ws, row, cols, widths):
        for i, (h, w) in enumerate(zip(cols, widths), 1):
            c = ws.cell(row=row, column=i, value=h)
            c.font, c.fill = hdr, hfill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i <= 2 else "right")
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.row_dimensions[row].height = 42

    def title(ws, t, sub):
        ws["A1"] = t
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=INK)
        ws["A2"] = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6470")

    ws = wb.active
    ws.title = "Contribution review"
    n = G["raised"]
    title(ws, "%d of 16 districts rise from 1 January 2027: %s" % (len(n), ", ".join(n)),
          "Expected plan year 2026 plan-paid claims per member per month: January to June 2026 incurred claims paid "
          "through 30 September 2026, completed by the plan-year factor of the districts that ran the same plan "
          "through 2025, against the claims component of the 2026 contribution rate.")
    cols = ["District", "District name", "2026 plan (deductible)", "Jan to Jun 2026 member months",
            "Jan to Jun 2026 plan paid ($)", "Jan to Jun 2026 PMPM ($)", "Plan-year factor",
            "Expected plan year 2026 PMPM ($)", "2026 claims component ($)", "Over (under) ($)", "Contribution rises"]
    head(ws, 4, cols, [8, 30, 12, 11, 14, 11, 9, 13, 12, 11, 10])
    for i, d in enumerate(b["ids"]):
        dz = b["design"][(d, 2026)]
        mm = sum(b["mm"].get((d, ym), 0) for ym in B.H1)
        pd = sum(b["paid"].get((d, ym), 0.0) for ym in B.H1)
        est, rate = G["est"][d], b["rates"][d]
        vals = [d, names[d], "%s ($%s)" % ({500: "MVA", 1500: "MVB", 3000: "MVC"}[dz], "{:,}".format(dz)), mm,
                round(pd), round(G["h1"][d], 2), round(G["k"][dz], 4), r10(est), rate, round(est - rate, 2),
                "yes" if d in n else "no"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            c.font = bold if (d in n and j in (1, 2, 11)) else body
            c.border = thin
            if d in n:
                c.fill = nfill
            if j in (4, 5, 8):
                c.number_format = "#,##0"
            elif j in (6, 9):
                c.number_format = "#,##0.00"
            elif j == 7:
                c.number_format = "0.0000"
            elif j == 10:
                c.number_format = "#,##0.00;(#,##0.00)"
            if j >= 3:
                c.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "C5"
    r0 = 5 + len(b["ids"]) + 1
    for k, t in enumerate([
        "The plan pays little in the first months of a plan year while members meet their deductibles, and less the "
        "higher the deductible, so January to June carries less of a plan MVC year than of a plan MVA year. "
        "Brantmoor, Farrowdale, Isenbrook and Northam Vale moved from plan MVA to plan MVC on 1 January 2026: "
        "their January to June 2026 claims are completed by the factor of Eversley Plains, Kestrel Point and Pellow "
        "Ridge, which ran plan MVC through 2025, not by their own 2025 on plan MVA.",
        "Over (under) is the expected PMPM unrounded less the claims component. Plan-paid claims are gross of "
        "specific stop-loss reimbursements and before pharmacy rebates (contribution review memo, section 2).",
    ]):
        c = ws.cell(row=r0 + k, column=1, value=t)
        c.font = Font(name="Calibri", size=9, color="5B6470")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + k, start_column=1, end_row=r0 + k, end_column=11)
        ws.row_dimensions[r0 + k].height = 40

    cs = wb.create_sheet("Chart data")
    cs.append(["District", "Expected plan year 2026 PMPM ($)", "2026 claims component ($)"])
    for d in b["ids"]:
        cs.append([d, round(G["est"][d], 2), b["rates"][d]])
    ch = BarChart()
    ch.type = "col"
    word = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}.get(len(n), str(len(n)))
    ch.title = "%s districts' expected 2026 claims run over their claims component" % word
    ch.y_axis.title = "Dollars per member per month"
    ch.y_axis.numFmt = "#,##0"
    ch.y_axis.scaling.min = 300
    ch.y_axis.delete = False
    ch.x_axis.delete = False
    ch.x_axis.tickLblSkip = 1
    data = Reference(cs, min_col=2, min_row=1, max_col=3, max_row=len(b["ids"]) + 1)
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(b["ids"]) + 1))
    ch.series[0].graphicalProperties = GraphicalProperties(solidFill=GREEN)
    for i, d in enumerate(b["ids"]):
        if d in n:
            pt = DataPoint(idx=i)
            pt.graphicalProperties = GraphicalProperties(solidFill=ACCENT)
            ch.series[0].dPt.append(pt)
    ch.series[1].graphicalProperties = GraphicalProperties(solidFill=MUTED)
    ch.gapWidth = 60
    ch.legend.position = "b"
    ch.height, ch.width = 10, 26
    ws.add_chart(ch, "A%d" % (r0 + 3))

    fs = wb.create_sheet("Plan-year factors")
    title(fs, "Plan year 2025: the plan-year PMPM over the January to June PMPM, by plan",
          "Claims incurred in 2025 and paid through 31 March 2026; each plan's factor pools the districts that ran it "
          "through 2025.")
    head(fs, 4, ["Plan", "Districts", "2025 member months", "2025 plan paid ($)", "Plan year PMPM ($)",
                 "Jan to Jun PMPM ($)", "Factor"], [8, 30, 12, 15, 12, 12, 10])
    row = 5
    for dz, code in ((500, "MVA"), (1500, "MVB"), (3000, "MVC")):
        ids = [i for i in b["ids"] if b["design"][(i, 2025)] == dz]
        mm = sum(b["mm"].get((i, ym), 0) for i in ids for ym in B.Y25)
        pd = sum(b["paid"].get((i, ym), 0.0) for i in ids for ym in B.Y25)
        mh = sum(b["mm"].get((i, ym), 0) for i in ids for ym in B.Y25[:6])
        ph = sum(b["paid"].get((i, ym), 0.0) for i in ids for ym in B.Y25[:6])
        vals = [code, ", ".join(ids), mm, round(pd), round(pd / mm, 2), round(ph / mh, 2), round(G["k"][dz], 4)]
        for j, v in enumerate(vals, 1):
            c = fs.cell(row=row, column=j, value=v)
            c.font, c.border = body, thin
            c.number_format = {3: "#,##0", 4: "#,##0", 5: "#,##0.00", 6: "#,##0.00", 7: "0.0000"}.get(j, "General")
        row += 1

    a = wb.create_sheet("Q3 2026 member months")
    title(a, "July to September 2026 member months", "Each person counted once a month: members reissued new ids when "
                                                     "their district moved payroll to the county system are one person "
                                                     "under both ids.")
    head(a, 4, ["District", "District name", "Member months"], [8, 30, 14])
    for i, d in enumerate(b["ids"]):
        for j, (v, fm) in enumerate(((d, None), (names[d], None), (G["a"][d], "#,##0")), 1):
            c = a.cell(row=5 + i, column=j, value=v)
            c.font, c.border = body, thin
            if fm:
                c.number_format = fm
    ad = wb.create_sheet("2026 advisories")
    title(ad, "Granfield's 2026 specific advisories", "Members flagged at $125,000, each counted once (a claimant file "
                                                      "reopened under a member's new id is the same member), at the "
                                                      "claims to date Granfield last reported.")
    head(ad, 4, ["District", "District name", "Members on advisory", "Claims to date ($)"], [8, 30, 12, 16])
    for i, d in enumerate(b["ids"]):
        for j, (v, fm) in enumerate(((d, None), (names[d], None), (G["bb"][d][0], "0"),
                                     (round(G["bb"][d][1]), "#,##0")), 1):
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
    dflt = B.expected(b, "default")
    return {
        "call": {"raised": G["raised"]},
        "expected_pmpm": {d: r10(G["est"][d]) for d in b["ids"]},
        "ask_a": {d: G["a"][d] for d in b["ids"]},
        "ask_b": {d: {"members": G["bb"][d][0], "claims_to_date": int(round(G["bb"][d][1]))} for d in b["ids"]},
        "default_path": {"raised": B.raised(b, dflt), "expected_pmpm": {d: r10(dflt[d]) for d in b["ids"]}},
        "claims_component": {d: "%.2f" % b["rates"][d] for d in b["ids"]},
        "conventions": {"deductibles": [500, 1500, 3000], "advisory": 125000, "specific": 250000,
                        "years": [2025, 2026, 2027], "counts": [4, 6, 16], "months": [3, 6, 30, 31], "rounding": [10]},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G, target)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Brady Cooper", "Brady Cooper", "2026-10-08T14:10:00Z",
                       "2026-10-12T20:35:00Z", excel=True, company=PP.COMPANY)
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
