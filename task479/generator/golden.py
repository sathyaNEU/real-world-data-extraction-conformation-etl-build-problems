"""The golden deliverable, computed from the cut pack through bundle.py: the trust's 2027 renewal surcharge workbook
(each employer's 2023 to 2025 retained claims trended to 2027, its credibility and expected 2027 retained claims against
its elected claims component, July to September 2026 member months and the 2026 high-cost claimants), and
generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "crbht_2027_renewal_surcharges.xlsx"
INK = "1B2430"
GREEN = "2C5A3F"
PALE = "E7EFE9"
MUTED = "A3ACB8"
ACCENT = "B4452F"
RATES = "crbht_2027_contribution_elections.xlsx"


def compute(target):
    b = B.load(target)
    ex = B.experience(b)
    c = B.credibility(b, ex)
    est = c["est"]
    return {"b": b, "ex": ex, "c": c, "est": est, "sur": B.surcharged(b, est), "a": B.ask_a(b), "bb": B.ask_b(b)}


def write_xlsx(path, G, target):
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b, c, ex = G["b"], G["c"], G["ex"]
    names = {}
    for r in openpyxl.load_workbook(os.path.join(target, RATES), data_only=True)["2027 elections"].iter_rows(
            min_row=5, values_only=True):
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
            cl = ws.cell(row=row, column=i, value=h)
            cl.font, cl.fill = hdr, hfill
            cl.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i <= 2 else "right")
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.row_dimensions[row].height = 42

    def title(ws, t, sub):
        ws["A1"] = t
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=INK)
        ws["A2"] = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6470")

    ws = wb.active
    ws.title = "Renewal review"
    n = G["sur"]
    title(ws, "%d of 18 employers are surcharged from 1 January 2027: %s" % (len(n), ", ".join(n)),
          "Expected 2027 retained claims per member per month: each employer's 2023 to 2025 retained claims trended "
          "at 7 per cent a year, weighed against the trust's by its credibility (Buhlmann-Straub), against the claims "
          "component of its elected 2027 contribution.")
    cols = ["Employer", "Employer name", "2023 to 2025 member months", "2023 to 2025 retained claims ($)",
            "Experience PMPM trended to 2027 ($)", "Credibility", "Expected 2027 PMPM ($)", "2027 claims component ($)",
            "Over (under) ($)", "Surcharged"]
    head(ws, 4, cols, [9, 32, 12, 15, 13, 10, 12, 12, 11, 10])
    for i, e in enumerate(b["ids"]):
        mm = sum(ex[(e, y)]["mm"] for y in B.YEARS)
        ret = sum(ex[(e, y)]["ret"] for y in B.YEARS)
        est, rate = G["est"][e], b["rates"][e]
        vals = [e, names[e], mm, round(ret), round(c["own"][e]), round(c["z"][e], 2), round(est), rate,
                round(est - rate, 2), "yes" if e in n else "no"]
        for j, v in enumerate(vals, 1):
            cl = ws.cell(row=5 + i, column=j, value=v)
            cl.font = bold if (e in n and j in (1, 2, 10)) else body
            cl.border = thin
            if e in n:
                cl.fill = nfill
            cl.number_format = {3: "#,##0", 4: "#,##0", 5: "#,##0", 6: "0.00", 7: "#,##0", 8: "#,##0.00",
                                9: "#,##0.00;(#,##0.00)"}.get(j, "General")
            if j >= 3:
                cl.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "C5"
    r0 = 5 + len(b["ids"]) + 1
    for k, t in enumerate([
        "Most member employers cover fewer than three hundred members, and one member's large claim moves a small "
        "employer's year by more than the employers truly differ: the three years' spread within an employer "
        "(expected process variance %.0f) against the spread between employers' true levels (%.0f) gives each employer "
        "a credibility of its member months over its member months plus %.0f. An employer's expected 2027 claims are "
        "its credibility times its own trended experience plus the rest times the trust's, $%.2f." % (
            c["epv"], c["vhm"], c["k"], c["xbar"]),
        "Over (under) is the expected PMPM unrounded less the claims component. Retained claims are net of Westerby's "
        "specific reimbursements and before pharmacy rebates (renewal review memo, section 2).",
    ]):
        cl = ws.cell(row=r0 + k, column=1, value=t)
        cl.font = Font(name="Calibri", size=9, color="5B6470")
        cl.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + k, start_column=1, end_row=r0 + k, end_column=10)
        ws.row_dimensions[r0 + k].height = 52

    cs = wb.create_sheet("Chart data")
    cs.append(["Employer", "Expected 2027 PMPM ($)", "2027 claims component ($)"])
    for e in b["ids"]:
        cs.append([e, round(G["est"][e], 2), b["rates"][e]])
    ch = BarChart()
    ch.type = "col"
    word = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}.get(len(n), str(len(n)))
    ch.title = "%s employers' expected 2027 claims run over their claims component" % word
    ch.y_axis.title = "Dollars per member per month"
    ch.y_axis.numFmt = "#,##0"
    ch.y_axis.scaling.min = 300
    ch.y_axis.delete = False
    ch.x_axis.delete = False
    ch.x_axis.tickLblSkip = 1
    ch.add_data(Reference(cs, min_col=2, min_row=1, max_col=3, max_row=len(b["ids"]) + 1), titles_from_data=True)
    ch.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(b["ids"]) + 1))
    ch.series[0].graphicalProperties = GraphicalProperties(solidFill=GREEN)
    for i, e in enumerate(b["ids"]):
        if e in n:
            pt = DataPoint(idx=i)
            pt.graphicalProperties = GraphicalProperties(solidFill=ACCENT)
            ch.series[0].dPt.append(pt)
    ch.series[1].graphicalProperties = GraphicalProperties(solidFill=MUTED)
    ch.gapWidth = 60
    ch.legend.position = "b"
    ch.height, ch.width = 10, 28
    ws.add_chart(ch, "A%d" % (r0 + 3))

    ys = wb.create_sheet("Experience by year")
    title(ys, "Retained claims per member per month by plan year, trended to 2027",
          "Claims incurred in the year and paid through 31 March of the next, less Westerby's reimbursements, at 7 per "
          "cent a year to 2027.")
    head(ys, 4, ["Employer", "2023 member months", "2023 PMPM ($)", "2024 member months", "2024 PMPM ($)",
                 "2025 member months", "2025 PMPM ($)"], [9, 11, 11, 11, 11, 11, 11])
    for i, e in enumerate(b["ids"]):
        vals = [e]
        for y in B.YEARS:
            vals += [ex[(e, y)]["mm"], round(ex[(e, y)]["x"])]
        for j, v in enumerate(vals, 1):
            cl = ys.cell(row=5 + i, column=j, value=v)
            cl.font, cl.border = body, thin
            if j > 1:
                cl.number_format = "#,##0"

    a = wb.create_sheet("Q3 2026 member months")
    title(a, "July to September 2026 member months", "Each person counted once a month: members Hallam reissued new ids "
                                                     "at the summer 2026 eligibility move are one person under both.")
    head(a, 4, ["Employer", "Employer name", "Member months"], [9, 32, 14])
    for i, e in enumerate(b["ids"]):
        for j, (v, fm) in enumerate(((e, None), (names[e], None), (G["a"][e], "#,##0")), 1):
            cl = a.cell(row=5 + i, column=j, value=v)
            cl.font, cl.border = body, thin
            if fm:
                cl.number_format = fm
    hc = wb.create_sheet("2026 high-cost claimants")
    title(hc, "Hallam's 2026 high-cost claimant report", "Members with $25,000 or more of 2026 claims, each counted "
                                                         "once (a member reported under a new id is the same member), "
                                                         "at the claims to date last reported.")
    head(hc, 4, ["Employer", "Employer name", "Members", "Claims to date ($)"], [9, 32, 10, 16])
    for i, e in enumerate(b["ids"]):
        for j, (v, fm) in enumerate(((e, None), (names[e], None), (G["bb"][e][0], "0"),
                                     (round(G["bb"][e][1]), "#,##0")), 1):
            cl = hc.cell(row=5 + i, column=j, value=v)
            cl.font, cl.border = body, thin
            if fm:
                cl.number_format = fm
    for w in wb.worksheets:
        w.sheet_view.showGridLines = False
        w.page_setup.orientation = "landscape"
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def figures(G):
    b = G["b"]
    dflt = B.expected(b, "own_experience")
    return {
        "call": {"surcharged": G["sur"]},
        "experience_pmpm": {e: int(round(G["c"]["own"][e])) for e in b["ids"]},
        "ask_a": {e: G["a"][e] for e in b["ids"]},
        "ask_b": {e: {"members": G["bb"][e][0], "claims_to_date": int(round(G["bb"][e][1]))} for e in b["ids"]},
        "default_path": {"surcharged": B.surcharged(b, dflt)},
        "claims_component": {e: "%.2f" % b["rates"][e] for e in b["ids"]},
        "conventions": {"trend_pct": 7, "specific": 150000, "hcc": 25000, "years": [2023, 2024, 2025, 2026, 2027],
                        "counts": [18], "months": [3, 31], "lives": [1000, 3000]},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G, target)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Steven Coleman", "Steven Coleman", "2026-10-08T14:10:00Z",
                       "2026-10-13T20:35:00Z", excel=True, company=PP.COMPANY)
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
