"""The golden deliverables, computed from target/ alone: pdl_2027_net_cost.xlsx (the net cost table with the preferred
product in each class, the rebate guarantee check and the members by class and account) and pdl_2027_trustees.pptx
(the two slides for the Board). Returns the figures for figures.json."""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import analysis as A
import world as W

GOLD = dict(workbook="pdl_2027_net_cost.xlsx", slides="pdl_2027_trustees.pptx")
QLAB = {"FQ1": "Jul-Sep 2025", "FQ2": "Oct-Dec 2025", "FQ3": "Jan-Mar 2026", "FQ4": "Apr-Jun 2026"}
CH_LAB = {"RETAIL30": "Retail, under 84 days", "RETAIL90": "Retail, 84 days or more", "MAIL": "Mail order",
          "SPECIALTY": "Specialty"}


def r10(x):
    return int(round(x / 10.0)) * 10


def compute(target):
    pk = A.Pack(target)
    g = pk.golden()
    pk.rates = A.exhibit_rates(target)
    gq = pk.guarantee(pk.rates)
    mem = pk.members()
    return pk, g, gq, mem


def figures(pk, g, gq, mem):
    f = {}
    for c, v in g["picks"].items():
        f["call." + c] = v["pick"]
        f["runner." + c] = v["runner"]
    for b in pk.compared:
        f["net." + b] = r10(g["net"][b])
        f["net_exact." + b] = round(g["net"][b], 2)
        f["u30." + b] = round(pk.u30[b], 1)
        f["ingr." + b] = round(pk.ingr[b], 2)
        f["rebate." + b] = round(g["rebates"][b], 2)
        f["rate30." + b] = round(g["rate"][b], 2)
    for k, v in gq.items():
        for ch in A.CHANNELS:
            f["guar.%s.%s" % (k, ch)] = v["n"][ch]
        f["guar.%s.guarantee" % k] = int(round(v["guarantee"]))
        f["guar.%s.remitted" % k] = int(round(v["remitted"]))
        f["guar.%s.shortfall" % k] = int(round(v["shortfall"]))
    for (c, a), n in mem.items():
        f["members.%s.%s" % (c, a)] = n
    for ch, v in pk.rates.items():
        f["rate." + ch] = v
    for c, bs in pk.classes.items():
        for b in bs:
            f["class." + b] = c
    f["group_codes"] = ["100", "200", "300", "400"]
    f["const.days_90"] = 84
    f["const.days_30"] = 30
    return f


def workbook(path, pk, g, gq, mem):
    wb = Workbook()
    ws = wb.active
    ws.title = "Net cost FY2026"
    bold = Font(bold=True)
    thin = Side(style="thin", color="999999")
    ws.append(["2027 preferred drug list: fiscal 2026 net cost per 30-day supply (claims filled 1 July 2025 to 30 June "
               "2026, rebates remitted through the April to June 2026 statement)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    hdr = ["Class", "Product", "Manufacturer", "30-day supplies", "Ingredient cost paid (USD)",
           "Manufacturer rebates (USD)", "Net cost per 30-day supply (USD)", "2027 status"]
    ws.append(hdr)
    for cell in ws[3]:
        cell.font = bold
        cell.alignment = Alignment(wrap_text=True, vertical="bottom")
        cell.border = Border(bottom=thin)
    fill = PatternFill("solid", fgColor="E2EFDA")
    for c, bs in pk.classes.items():
        for b in sorted(bs, key=lambda x: g["net"][x]):
            pref = g["picks"][c]["pick"] == b
            ws.append([c, b, pk.labeler_of[b], round(pk.u30[b], 1), round(pk.ingr[b], 2), round(g["rebates"][b], 2),
                       r10(g["net"][b]), "Preferred" if pref else "Non-preferred"])
            if pref:
                for cell in ws[ws.max_row]:
                    cell.fill = fill
    for row in ws.iter_rows(min_row=4, min_col=4, max_col=4):
        for cell in row:
            cell.number_format = "#,##0.0"
    for row in ws.iter_rows(min_row=4, min_col=5, max_col=6):
        for cell in row:
            cell.number_format = "#,##0.00"
    for row in ws.iter_rows(min_row=4, min_col=7, max_col=7):
        for cell in row:
            cell.number_format = "#,##0"
    for i, wd in enumerate([40, 22, 32, 14, 20, 20, 18, 14], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A4"
    last = ws.max_row + 2
    ws.cell(row=last, column=1, value="Rebates are each manufacturer's remittances for fiscal 2026 claims (current "
            "quarter and prior period lines, by quarter of service and plan account) attributed to its products by "
            "least squares on each product's 30-day supplies in the same account and quarter.")
    ws.cell(row=last, column=1).font = Font(italic=True, size=9)

    s2 = wb.create_sheet("Rebate guarantee")
    s2.append(["Exhibit C minimum rebate guarantee, fiscal 2026 brand claims by quarter of service"])
    s2["A1"].font = Font(bold=True, size=12)
    s2.append([])
    s2.append(["Quarter", "Retail claims, under 84 days", "Retail claims, 84 days or more", "Mail order claims",
               "Specialty claims", "Guaranteed rebate (USD)", "Rebates remitted for the quarter's claims (USD)",
               "Shortfall owed (USD)"])
    for cell in s2[3]:
        cell.font = bold
        cell.alignment = Alignment(wrap_text=True, vertical="bottom")
        cell.border = Border(bottom=thin)
    for k, v in gq.items():
        s2.append([QLAB[k]] + [v["n"][ch] for ch in A.CHANNELS] +
                  [int(round(v["guarantee"])), int(round(v["remitted"])),
                   int(round(v["shortfall"])) if v["shortfall"] > 0 else "None"])
    for row in s2.iter_rows(min_row=4, min_col=2, max_col=8):
        for cell in row:
            if isinstance(cell.value, (int, float)):
                cell.number_format = "#,##0"
    for i, wd in enumerate([16, 15, 15, 13, 12, 18, 22, 15], 1):
        s2.column_dimensions[get_column_letter(i)].width = wd
    s2.cell(row=10, column=1, value="Channel is the dispensing pharmacy's network on the date of service; the three "
            "hospital outpatient pharmacies that joined the specialty network on 1 March 2026 are retail before it.")
    s2.cell(row=10, column=1).font = Font(italic=True, size=9)

    s3 = wb.create_sheet("Members")
    s3.append(["Members with a paid fiscal 2026 claim in each reviewed class, by employer account"])
    s3["A1"].font = Font(bold=True, size=12)
    s3.append([])
    s3.append(["Class"] + A.ACC_ORDER)
    for cell in s3[3]:
        cell.font = bold
        cell.border = Border(bottom=thin)
    for c in pk.classes:
        s3.append([c] + [mem[(c, a)] for a in A.ACC_ORDER])
    for i, wd in enumerate([42, 16, 18, 18, 22], 1):
        s3.column_dimensions[get_column_letter(i)].width = wd
    s3.cell(row=11, column=1, value="A member counted once per class and account; claims before 1 January 2026 carry "
            "the old cardholder numbers and person codes, matched to the new roster through the subscriber's legacy "
            "cardholder number and the member's birth date and gender.")
    s3.cell(row=11, column=1).font = Font(italic=True, size=9)
    wb.save(path)


def slides(path, pk, g):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.util import Inches, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]

    def title(slide, text, sub=None):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.text = text
        tf.paragraphs[0].runs[0].font.size = Pt(26)
        tf.paragraphs[0].runs[0].font.bold = True
        if sub:
            p2 = tf.add_paragraph()
            p2.text = sub
            p2.runs[0].font.size = Pt(13)
            p2.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    s1 = prs.slides.add_slide(blank)
    changes = [c for c, v in g["picks"].items()]
    title(s1, "2027 preferred drug list: the recommended preferred product in each class",
          "Lowest fiscal 2026 net cost per 30-day supply after manufacturer rebates (policy EB-RX-04, section 3)")
    rows = len(pk.classes) + 1
    tbl = s1.shapes.add_table(rows, 4, Inches(0.6), Inches(1.7), Inches(12.1), Inches(4.6)).table
    for j, h in enumerate(["Class", "Preferred product", "Net cost per 30-day supply", "Next lowest"]):
        tbl.cell(0, j).text = h
    for i, (c, v) in enumerate(g["picks"].items(), 1):
        tbl.cell(i, 0).text = c
        tbl.cell(i, 1).text = v["pick"]
        tbl.cell(i, 2).text = "${:,}".format(r10(g["net"][v["pick"]]))
        tbl.cell(i, 3).text = "%s, ${:,}".format(r10(g["net"][v["runner"]])) % v["runner"]
    for r_ in range(rows):
        for c_ in range(4):
            for para in tbl.cell(r_, c_).text_frame.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(15 if r_ else 15)
                    run.font.bold = (r_ == 0)
    tbl.columns[0].width = Inches(4.3)
    tbl.columns[1].width = Inches(2.6)
    tbl.columns[2].width = Inches(2.3)
    tbl.columns[3].width = Inches(2.9)

    s2 = prs.slides.add_slide(blank)
    title(s2, "Fiscal 2026 net cost per 30-day supply of every product compared",
          "The preferred product is the lowest bar in each class; adalimumab products are on their own scale")
    short = {"GLP-1 receptor agonists": "GLP-1 RAs", "SGLT2 inhibitors": "SGLT2 inhibitors",
             "Long-acting insulins": "Long-acting insulins", "Direct oral anticoagulants": "Oral anticoagulants",
             "Inhaled corticosteroid and LABA combinations": "ICS/LABA inhalers", "Adalimumab products": "Adalimumab"}
    main = [c for c in pk.classes if c != "Adalimumab products"]
    cd = CategoryChartData()
    labels, vals = [], []
    for c in main:
        for b in sorted(pk.classes[c], key=lambda x: g["net"][x]):
            labels.append("%s: %s" % (short[c], b))
            vals.append(r10(g["net"][b]))
    cd.categories = labels
    cd.add_series("Net cost per 30-day supply (USD)", vals)
    gf = s2.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.5), Inches(1.5), Inches(8.6), Inches(5.7), cd)
    ch = gf.chart
    ch.has_legend = False
    plot = ch.plots[0]
    plot.has_data_labels = True
    plot.data_labels.font.size = Pt(9)
    plot.data_labels.number_format = '"$"#,##0'
    plot.data_labels.number_format_is_linked = False
    ch.category_axis.tick_labels.font.size = Pt(9)
    ch.category_axis.reverse_order = True
    ch.value_axis.tick_labels.font.size = Pt(9)
    ch.value_axis.has_major_gridlines = False
    pts = plot.series[0].points
    k = 0
    for c in main:
        for b in sorted(pk.classes[c], key=lambda x: g["net"][x]):
            pts[k].format.fill.solid()
            pts[k].format.fill.fore_color.rgb = RGBColor(0x2E, 0x7D, 0x32) if g["picks"][c]["pick"] == b \
                else RGBColor(0xA6, 0xA6, 0xA6)
            k += 1
    cd2 = CategoryChartData()
    ada = sorted(pk.classes["Adalimumab products"], key=lambda x: g["net"][x])
    cd2.categories = ada
    cd2.add_series("Net cost per 30-day supply (USD)", [r10(g["net"][b]) for b in ada])
    gf2 = s2.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(9.3), Inches(1.5), Inches(3.6), Inches(3.0), cd2)
    c2 = gf2.chart
    c2.has_legend = False
    c2.has_title = True
    c2.chart_title.text_frame.text = "Adalimumab products"
    c2.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
    p2 = c2.plots[0]
    p2.has_data_labels = True
    p2.data_labels.font.size = Pt(9)
    p2.data_labels.number_format = '"$"#,##0'
    p2.data_labels.number_format_is_linked = False
    c2.category_axis.tick_labels.font.size = Pt(9)
    c2.category_axis.reverse_order = True
    c2.value_axis.tick_labels.font.size = Pt(8)
    c2.value_axis.has_major_gridlines = False
    for i, b in enumerate(ada):
        pt = p2.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor(0x2E, 0x7D, 0x32) if i == 0 else RGBColor(0xA6, 0xA6, 0xA6)
    note = s2.shapes.add_textbox(Inches(9.3), Inches(4.8), Inches(3.6), Inches(2.0)).text_frame
    note.word_wrap = True
    note.text = "Green: preferred for 2027. Net cost is the ingredient cost the Plan paid less the manufacturer's " \
                "rebates on those claims, per 30-day supply, fiscal 2026."
    note.paragraphs[0].runs[0].font.size = Pt(10)
    prs.save(path)


def write(golden_dir, target):
    import postprocess as PP
    import shutil
    shutil.rmtree(golden_dir, ignore_errors=True)
    os.makedirs(golden_dir)
    pk, g, gq, mem = compute(target)
    wbp = os.path.join(golden_dir, GOLD["workbook"])
    workbook(wbp, pk, g, gq, mem)
    PP.normalize_ooxml(wbp, "Maria Burgess", "Maria Burgess", "2026-10-15T13:02:00Z", "2026-10-19T21:40:00Z",
                       title="2027 PDL net cost", excel=True, company=W.OFFICE)
    sp = os.path.join(golden_dir, GOLD["slides"])
    slides(sp, pk, g)
    PP.normalize_ooxml(sp, "Maria Burgess", "Maria Burgess", "2026-10-16T14:20:00Z", "2026-10-19T22:05:00Z",
                       title="2027 preferred drug list", company=W.OFFICE)
    return figures(pk, g, gq, mem)
