"""Write the golden deliverables from golden.compute: the KPI report workbook and the covering letter to the bank with
its chart; and generator/figures.json, which the write-up is drafted from."""
import json
import os

import golden as G
import world as W

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LONG = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
        "December"]


def figures(c, target):
    k = c["kpi"]
    imp = G.hh_monthly(target)
    sub = {m: imp[m] - c["monthly"][m] for m in range(1, 13)}
    nested = sum(G.base_building(target, "golden").values()) - sum(G.base_building(target, "all").values())
    return {
        "call": {"kpi_kg_m2": round(k["kpi"], 1), "target_kg_m2": W.TARGET_KG_M2, "missed": bool(k["missed"]),
                 "margin_kg_m2": round(k["margin"], 1)},
        "components": {"base_building_mwh": round(k["mwh"]), "import_mwh": round(sum(imp.values()) / 1000.0),
                       "tenancy_supplies_mwh": round(sum(sub.values()) / 1000.0),
                       "nested_rooms_mwh": round(nested / 1000.0), "scope2_t": round(k["scope2_t"], 1)},
        "base_building_mwh_month": {MONTHS[m - 1]: round(c["monthly"][m] / 1000.0) for m in range(1, 13)},
        "diesel_l": {"Q%d" % q: round(v) for q, v in c["diesel"].items()},
        "diesel_kg_co2e": {"Q%d" % q: round(v * W.DIESEL_KG_PER_L) for q, v in c["diesel"].items()},
        "refrigerant_kg": {ch: round(v, 1) for ch, v in sorted(c["refrigerant"].items())},
        "refrigerant_kg_co2e": {ch: round(v * W.GWP_R134A) for ch, v in sorted(c["refrigerant"].items())},
        "rungs_kpi_kg_m2": {m: round(r["kpi"], 1) for m, r in c["rungs"].items()},
        "constants": {"nla_m2": W.NLA_M2, "factor_kg_per_kwh": W.FACTOR_KG_PER_KWH, "target_kg_m2": W.TARGET_KG_M2,
                      "diesel_kg_per_l": W.DIESEL_KG_PER_L, "gwp_r134a": W.GWP_R134A, "wh_per_kwh": 1000},
    }


def write_report(path, c, fig, target):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    imp = G.hh_monthly(target)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "KPI 2026"
    bold = Font(name="Calibri", bold=True)
    head = PatternFill("solid", fgColor="DCE6EA")
    thin = Border(top=Side(style="thin", color="7F8C8D"))
    ws["A1"] = "Pellow House: base building electricity and Scope 2 KPI, 2026"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws["A2"] = "Facility agreement Schedule 9. Months on the building's local clock; MWh from unrounded kWh."
    cols = ["Month", "Import (MWh)", "Tenancy supplies (MWh)", "Base building (MWh)"]
    for j, h in enumerate(cols, start=1):
        cell = ws.cell(row=4, column=j, value=h)
        cell.font, cell.fill = bold, head
        cell.alignment = Alignment(wrap_text=True, horizontal="center")
    for m in range(1, 13):
        r = 4 + m
        ws.cell(row=r, column=1, value=LONG[m - 1])
        ws.cell(row=r, column=2, value=imp[m] / 1000.0).number_format = "#,##0"
        ws.cell(row=r, column=3, value=(imp[m] - c["monthly"][m]) / 1000.0).number_format = "#,##0"
        ws.cell(row=r, column=4, value=c["monthly"][m] / 1000.0).number_format = "#,##0"
    ws.cell(row=17, column=1, value="Year").font = bold
    for j, v in ((2, sum(imp.values()) / 1000.0), (3, (sum(imp.values()) - sum(c["monthly"].values())) / 1000.0),
                 (4, c["kpi"]["mwh"])):
        cell = ws.cell(row=17, column=j, value=v)
        cell.number_format, cell.font, cell.border = "#,##0", bold, thin
    ws.cell(row=17, column=1).border = thin
    k = c["kpi"]
    block = [("Base Building Electricity (MWh)", k["mwh"], "#,##0"),
             ("Base Building Scope 2 Emissions (t CO2e)", k["scope2_t"], "#,##0.0"),
             ("Net Lettable Area (m2)", W.NLA_M2, "#,##0"),
             ("KPI (kg CO2e per m2)", k["kpi"], "0.0"),
             ("2026 Target (kg CO2e per m2, not more than)", W.TARGET_KG_M2, "0.0"),
             ("KPI less Target (kg CO2e per m2)", k["margin"], "+0.0;-0.0"),
             ("Result", "Target missed" if k["missed"] else "Target met", None)]
    for i, (lab, v, f) in enumerate(block):
        ws.cell(row=19 + i, column=1, value=lab)
        cell = ws.cell(row=19 + i, column=4, value=v)
        if f:
            cell.number_format = f
        if lab.startswith(("KPI (", "Result")):
            ws.cell(row=19 + i, column=1).font = bold
            cell.font = bold
    for col, w in zip("ABCD", (44, 13, 15, 15)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "B5"
    s1 = wb.create_sheet("Scope 1 2026")
    s1["A1"] = "Pellow House: Scope 1 lines, 2026"
    s1["A1"].font = Font(name="Calibri", bold=True, size=13)
    for j, h in enumerate(["Standby generator, gas oil", "Burned (litres)", "Emissions (kg CO2e)"], start=1):
        cell = s1.cell(row=3, column=j, value=h)
        cell.font, cell.fill = bold, head
    for q in range(1, 5):
        s1.cell(row=3 + q, column=1, value="Q%d 2026" % q)
        s1.cell(row=3 + q, column=2, value=c["diesel"][q]).number_format = "#,##0"
        s1.cell(row=3 + q, column=3, value=c["diesel"][q] * W.DIESEL_KG_PER_L).number_format = "#,##0"
    for j, h in enumerate(["Chiller, R-134a", "Released (kg)", "Emissions (kg CO2e)"], start=1):
        cell = s1.cell(row=9, column=j, value=h)
        cell.font, cell.fill = bold, head
    for i, ch in enumerate(sorted(c["refrigerant"])):
        s1.cell(row=10 + i, column=1, value=ch)
        s1.cell(row=10 + i, column=2, value=c["refrigerant"][ch]).number_format = "0.0"
        s1.cell(row=10 + i, column=3, value=c["refrigerant"][ch] * W.GWP_R134A).number_format = "#,##0"
    s1["A15"] = ("Gas oil at %s kg CO2e per litre and R-134a at a GWP of %s (Schedule 9, 4.2 and 4.3). Refrigerant "
                 "released is the charge added less the charge recovered to cylinders." % (W.DIESEL_KG_PER_L, W.GWP_R134A))
    for col, w in zip("ABC", (30, 15, 19)):
        s1.column_dimensions[col].width = w
    wb.save(path)


def chart_png(path, c, fig):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task461"})
    vals = [c["monthly"][m] / 1000.0 for m in range(1, 13)]
    figp, ax = plt.subplots(figsize=(6.6, 3.0), dpi=200)
    ax.bar(range(12), vals, width=0.62, color="#2a78d6", edgecolor="#fcfcfb", linewidth=0.8)
    for i, v in enumerate(vals):
        ax.text(i, v + 2, "%d" % round(v), ha="center", va="bottom", fontsize=7, color="#52514e")
    ax.set_xticks(range(12))
    ax.set_xticklabels(MONTHS)
    ax.set_ylabel("MWh")
    ax.set_ylim(0, max(vals) * 1.17)
    ax.grid(axis="y", color="#e4e3df", linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9b9a96")
    ax.tick_params(colors="#52514e")
    ax.set_title("Base building electricity by month, 2026: %s MWh for the year" % "{:,}".format(
        fig["components"]["base_building_mwh"]), fontsize=9, color="#0b0b0b", loc="left")
    figp.tight_layout()
    figp.savefig(path, metadata={"Software": None}, facecolor="#fcfcfb")
    plt.close(figp)


def write_letter(path, c, fig, png):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs as DC   # noqa: F401  (registers the fonts)
    ink, grey = colors.HexColor("#1b1d1f"), colors.HexColor("#5b6066")
    body = ParagraphStyle("b", fontName="LiberationSerif", fontSize=10.4, leading=14, textColor=ink, spaceAfter=6)
    small = ParagraphStyle("s", fontName="LiberationSans", fontSize=8, leading=10.4, textColor=grey)
    title = ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=12.6, leading=16, textColor=ink, spaceAfter=6)
    cell = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.8, leading=11, textColor=ink)
    k, f = c["kpi"], fig

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.4)
        canvas.setFillColor(grey)
        canvas.drawString(20 * mm, 11 * mm, "%s  |  22 Tanner Row, Wexmoor WX1 4DN  |  Ref WOT-SLL-2027-01" % W.ORG)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm,
                          bottomMargin=20 * mm, title="Pellow House KPI report 2026", author=W.ORG, subject="",
                          creator="", producer="")
    s = [Paragraph("%s<br/>Sustainability-Linked Loans, Agency<br/>15 January 2027" % W.BANK, small), Spacer(1, 8),
         Paragraph("Pellow House missed its 2026 emissions target: %.1f kg CO2e per square metre against %.1f"
                   % (f["call"]["kpi_kg_m2"], W.TARGET_KG_M2), title),
         Paragraph("We enclose the 2026 KPI report for Pellow House under Schedule 9 of the facility agreement. The "
                   "base building used %s MWh of electricity in 2026, which at the schedule's factor is %.1f tonnes of "
                   "CO2e, or <b>%.1f kg CO2e per square metre</b> of net lettable area. That is <b>%.1f kg over the "
                   "2026 target</b> of %.1f kg, so under paragraph 3.1 the margin steps up by 2.5 basis points for "
                   "2027." % ("{:,}".format(f["components"]["base_building_mwh"]), k["scope2_t"], f["call"]["kpi_kg_m2"],
                              f["call"]["margin_kg_m2"], W.TARGET_KG_M2), body),
         Paragraph("The base building figure is the import through the revenue meter less the electricity supplied to "
                   "the tenancies, each tenancy's supply counted once. Three occupiers' comms rooms are metered by the "
                   "building management system for recharge, inside those occupiers' own supply meters, so they are "
                   "already within the tenancy supplies and are not taken off a second time. The roof licensee's "
                   "equipment room is a supply of its own and is taken off.", body),
         Image(png, width=166 * mm, height=166 * mm * 3.0 / 6.6), Spacer(1, 4)]
    rows = [["Line", "2026"], ["Base building electricity", "%s MWh" % "{:,}".format(f["components"]["base_building_mwh"])],
            ["Base building Scope 2 emissions", "%.1f t CO2e" % k["scope2_t"]],
            ["KPI against target", "%.1f against %.1f kg CO2e per m2" % (f["call"]["kpi_kg_m2"], W.TARGET_KG_M2)],
            ["Standby generator gas oil", "%s litres, %s kg CO2e" % ("{:,}".format(sum(f["diesel_l"].values())),
                                                                   "{:,}".format(sum(f["diesel_kg_co2e"].values())))],
            ["Chiller refrigerant (R-134a)", "%.1f kg, %s kg CO2e" % (sum(c["refrigerant"].values()),
                                                                     "{:,}".format(sum(f["refrigerant_kg_co2e"].values())))]]
    t = Table([[Paragraph(str(x), cell) for x in r] for r in rows], colWidths=[70 * mm, 90 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, ink), ("LINEBELOW", (0, -1), (-1, -1), 0.4, grey),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    s += [t, Spacer(1, 4),
          Paragraph("Source: the supplier's half-hourly data for MPAN %s and the building management system's meter "
                    "registers; quarters and months on the building's local clock. The Scope 1 detail is in the "
                    "enclosed workbook." % W.MPAN, small), Spacer(1, 10),
          Paragraph("%s<br/>%s, %s" % (W.PEOPLE["sustainability"], W.TITLES["sustainability"], W.ORG_SHORT), body)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def main(target, gdir, fig_path):
    import postprocess as PP
    import tempfile
    os.makedirs(gdir, exist_ok=True)
    c = G.compute(target)
    fig = figures(c, target)
    with open(fig_path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
    write_report(os.path.join(gdir, W.GOLDEN["report"]), c, fig, target)
    png = os.path.join(tempfile.mkdtemp(), "chart.png")
    chart_png(png, c, fig)
    write_letter(os.path.join(gdir, W.GOLDEN["letter"]), c, fig, png)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["report"]), W.PEOPLE["sustainability"], W.PEOPLE["sustainability"],
                       "2027-01-12T09:05:00Z", "2027-01-15T08:31:00Z", excel=True, company=W.ORG)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["letter"]), b"D:20270115083000+00'00'", b"D:20270115083000+00'00'")
    return c, fig
