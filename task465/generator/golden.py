"""The goldens, computed from the shipped pack (bundle.py), never from the generator's state: the decision workbook
(covers, the burn by year, liability and premium, receipts, notes, and a chart of each quoted rate against the rate at
which its call changes) and the conformed county yield record; and generator/figures.json, from which submission.md
is written."""
import json
import os

import bundle as B
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def r2(x):
    return float("%.2f" % (x + 1e-12))


def compute(target):
    ts = B.terms(target)
    q = B.quotes(target)
    cty, dist = B.sorghum(target)
    cd = B.county_district(target)
    rec = B.recovered(target)
    ser = B.yields(target, "golden")
    el = B.expected_loss(ser, ts)
    drop = B.expected_loss(B.yields(target, "drop"), ts)
    covers = {}
    for c in W.MEMBERS:
        lim = W.BUY_MULTIPLE * el[c]
        covers[c] = dict(expected=ts[c]["expected"], trend=ts[c]["trend"], trigger=round(W.COVERAGE * ts[c]["expected"], 2),
                         expected_loss=r2(el[c]), quote=r2(q[c]), multiple=r2(q[c] / el[c]), change_rate=r2(lim),
                         call="Buy" if q[c] <= lim else "Decline", el_raw=el[c], default_el=r2(drop[c]),
                         default_multiple=r2(q[c] / drop[c]))
    burn = []
    for c in W.MEMBERS:
        for y in range(1991, 2026):
            v = ser[c][y]
            adj = v + ts[c]["trend"] * (2027 - y)
            burn.append(dict(county=c, year=y, yld=v, source="Recovered from district totals" if (c, y) in rec
                             else "Published", adjusted=adj, share=B.share(c, y, v, ts)))
    acres, lia, prem = B.liability(target)
    shares = B.receipts_share(target)
    tr = {t["transfer_no"] for t in B.transfers(target)}
    rec_bu = {c: 0.0 for c in W.MEMBERS}
    for t in B.tickets(target):
        if t["commodity"] != "Sorghum" or (t["site"] == "MAIN" and t["reference"] in tr):
            continue
        rec_bu[t["origin_county"]] += float(t["net_lb"]) * (100 - float(t["moisture_pct"])) / (100 - W.STANDARD_MOISTURE) / W.BUSHEL_LB
    call_ct, _ = B.sorghum(target, practice="ALL")
    prod = {c: sum(call_ct[c][y]["production"] for y in range(2016, 2021)) for c in W.MEMBERS}
    record = []
    for c in W.MEMBERS:
        for y in range(1991, 2026):
            v = cty[c][y]
            if (c, y) in rec:
                h, p, yl, src = rec[(c, y)]["harvested"], rec[(c, y)]["production"], rec[(c, y)]["yld"], "recovered from district totals"
            else:
                h, p, yl, src = v["harvested"], v["production"], v["yield"], "published"
            record.append(dict(county=c, ansi=W.COUNTIES[c][0], district=cd[c], year=y, harvested=int(h),
                               production=int(p), yld=yl, source=src))
    F = dict(
        call=dict(buy=[c for c in W.MEMBERS if covers[c]["call"] == "Buy"],
                  decline=[c for c in W.MEMBERS if covers[c]["call"] == "Decline"]),
        covers=covers,
        recovered={"%s %d" % k: dict(harvested=int(v["harvested"]), production=int(v["production"]), yld=v["yld"])
                   for k, v in sorted(rec.items())},
        burn=burn, record=record,
        acres={c: round(acres[c], 1) for c in W.MEMBERS},
        liability={c: int(round(lia[c], -2)) for c in W.MEMBERS},
        premium={c: int(round(prem[c], -2)) for c in W.MEMBERS},
        price_per_bu=round(W.PRICE_CWT * W.BUSHEL_LB / 100.0, 4),
        receipts_bu={c: int(round(rec_bu[c])) for c in W.MEMBERS},
        production_2016_2020={c: int(prod[c]) for c in W.MEMBERS},
        receipts_share={c: float("%.1f" % shares[c]) for c in W.MEMBERS},
        withheld_count=len(rec),
        record_rows=len(record),
        stated=dict(policy_multiple=W.BUY_MULTIPLE, trigger_pct=int(round(100 * W.COVERAGE)),
                    standard_moisture_pct=int(W.STANDARD_MOISTURE), price_cwt=W.PRICE_CWT, bushel_lb=W.BUSHEL_LB,
                    cited=dict(methods_note=["2.1", "4.1", "5.1"], risk_policy=["5.2", "5.3"])),
    )
    return F


# ---------------------------------------------------------------- the workbook
def write_workbook(path, F):
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.label import DataLabelList
    from openpyxl.chart.text import RichText, Text
    from openpyxl.chart.title import Title
    from openpyxl.drawing.text import CharacterProperties, Paragraph, ParagraphProperties, RegularTextRun
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.properties import PageSetupProperties
    wb = openpyxl.Workbook()
    thin = Side(style="thin", color="A6A6A6")
    head_fill = PatternFill("solid", fgColor="E3EAE4")
    buy_fill = PatternFill("solid", fgColor="EAF3EA")

    def title(ws, t, sub):
        ws.cell(row=1, column=1, value=t).font = Font(name="Calibri", size=14, bold=True, color="1F3A2B")
        ws.cell(row=2, column=1, value=sub).font = Font(name="Calibri", size=9.5, italic=True, color="595959")

    def header(ws, row, names, widths):
        for j, (n, w) in enumerate(zip(names, widths), start=1):
            c = ws.cell(row=row, column=j, value=n)
            c.font = Font(name="Calibri", size=10, bold=True)
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="bottom")
            c.border = Border(bottom=thin)
            ws.column_dimensions[c.column_letter].width = w
        ws.row_dimensions[row].height = 42

    ws = wb.active
    ws.title = "Covers"
    buy = F["call"]["buy"]
    dec = F["call"]["decline"]
    title(ws, "Buy the %s covers; decline %s" % (", ".join(buy[:-1]) + " and " + buy[-1],
                                                     " and ".join(dec)),
          "2027 area-yield drought covers on dryland grain sorghum. Quillfield Re quotes of 14 October 2026 against "
          "the risk policy's rule (5.2): buy where the quoted rate is at most 1.4 times the expected loss (5.3).")
    names = ["County", "Expected 2027 yield (bu/acre)", "Trigger yield (bu/acre)", "Expected loss (% of liability)",
             "Quoted rate (% of liability)", "Quoted rate / expected loss", "Rate at which the call changes "
             "(% of liability)", "Call"]
    header(ws, 4, names, [12, 13, 12, 14, 13, 13, 17, 10])
    for i, c in enumerate(W.MEMBERS, start=5):
        v = F["covers"][c]
        vals = [c, v["expected"], v["trigger"], v["expected_loss"] / 100, v["quote"] / 100, v["multiple"],
                v["change_rate"] / 100, v["call"]]
        fmts = [None, "0.0", "0.00", "0.00%", "0.00%", "0.00", "0.00%", None]
        for j, (val, fm) in enumerate(zip(vals, fmts), start=1):
            cell = ws.cell(row=i, column=j, value=val)
            cell.font = Font(name="Calibri", size=10, bold=(j in (1, 8)))
            if fm:
                cell.number_format = fm
                cell.alignment = Alignment(horizontal="right")
            if v["call"] == "Buy":
                cell.fill = buy_fill
    ws.cell(row=11, column=1, value="Expected loss: the average indemnity share over the crop years 1991 to 2025, each "
            "year's county yield brought to 2027 by the term sheet's trend; the ten county-years the service withheld "
            "are taken from their districts' totals less the districts' published counties (Burn sheet).").font = \
        Font(name="Calibri", size=9, color="404040")
    ws.merge_cells("A11:H11")
    ws.cell(row=11, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[11].height = 26
    ws.cell(row=12, column=1, value="The rate at which the call changes is 1.4 times the expected loss.").font = \
        Font(name="Calibri", size=9, color="404040")
    ws.freeze_panes = "B5"
    ch = BarChart()
    ch.type = "col"
    ch.grouping = "clustered"
    cp = CharacterProperties(sz=1150, b=True)
    ch.title = Title(tx=Text(rich=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), r=[RegularTextRun(
        rPr=cp, t="%s are quoted under the rate at which the call changes" % (", ".join(buy[:-1]) + " and " + buy[-1]))])])),
        overlay=False)
    ch.y_axis.title = "Per cent of liability"
    ch.x_axis.title = "County cover"
    ch.y_axis.number_format = "0.0%"
    ch.y_axis.majorGridlines = None
    data = Reference(ws, min_col=5, min_row=4, max_row=9)
    data2 = Reference(ws, min_col=7, min_row=4, max_row=9)
    cats = Reference(ws, min_col=1, min_row=5, max_row=9)
    ch.add_data(data, titles_from_data=True)
    ch.add_data(data2, titles_from_data=True)
    ch.set_categories(cats)
    ch.series[0].graphicalProperties.solidFill = "2F5D3A"
    ch.series[0].graphicalProperties.line.solidFill = "2F5D3A"
    ch.series[1].graphicalProperties.solidFill = "B8C4BB"
    ch.series[1].graphicalProperties.line.solidFill = "B8C4BB"
    for s in ch.series:
        s.dLbls = DataLabelList()
        s.dLbls.showVal = True
        s.dLbls.showSerName = False
        s.dLbls.showCatName = False
        s.dLbls.showLegendKey = False
        s.dLbls.showPercent = False
        s.dLbls.position = "outEnd"
        s.dLbls.numFmt = "0.00%"
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.legend.position = "b"
    ch.height = 8.5
    ch.width = 17.5
    ws.add_chart(ch, "A14")

    ws2 = wb.create_sheet("Burn")
    title(ws2, "Indemnity share by crop year, 1991 to 2025",
          "County yields as the service estimates them; withheld years recovered from the district's harvested acres "
          "and production less its published counties'.")
    header(ws2, 4, ["County", "Crop year", "Yield (bu/acre)", "Source", "Yield at 2027 level (bu/acre)",
                    "Indemnity share of liability"], [11, 9, 11, 28, 15, 15])
    for i, b in enumerate(F["burn"], start=5):
        for j, (val, fm) in enumerate(zip([b["county"], b["year"], b["yld"], b["source"], b["adjusted"], b["share"]],
                                          [None, "0", "0.0", None, "0.00", "0.0%"]), start=1):
            cell = ws2.cell(row=i, column=j, value=val)
            cell.font = Font(name="Calibri", size=10)
            if fm:
                cell.number_format = fm
    ws2.freeze_panes = "A5"
    ws2.auto_filter.ref = "A4:F%d" % (4 + len(F["burn"]))

    ws3 = wb.create_sheet("Liability and premium")
    title(ws3, "2027 liability and premium by county cover",
          "Acres enrolled through the member portal before the 5:00 p.m. Central close on 30 October 2026, each "
          "field's latest submission, dryland fields only; price $7.75 per hundredweight at 56 pounds a bushel.")
    header(ws3, 4, ["County", "Enrolled dryland acres", "Expected 2027 yield (bu/acre)", "Coverage level",
                    "Projected price ($/bu)", "Liability ($)", "Quoted rate (% of liability)", "Premium ($)"],
           [11, 12, 13, 10, 12, 14, 13, 12])
    for i, c in enumerate(W.MEMBERS, start=5):
        vals = [c, F["acres"][c], F["covers"][c]["expected"], W.COVERAGE, F["price_per_bu"], F["liability"][c],
                F["covers"][c]["quote"] / 100, F["premium"][c]]
        fmts = [None, "#,##0.0", "0.0", "0%", "$0.000", "$#,##0", "0.00%", "$#,##0"]
        for j, (val, fm) in enumerate(zip(vals, fmts), start=1):
            cell = ws3.cell(row=i, column=j, value=val)
            cell.font = Font(name="Calibri", size=10)
            if fm:
                cell.number_format = fm
    ws3.cell(row=11, column=1, value="Dollars rounded to the nearest hundred.").font = Font(name="Calibri", size=9,
                                                                                             color="404040")
    ws3.freeze_panes = "B5"

    ws4 = wb.create_sheet("Receipts 2016-2020")
    title(ws4, "Grain sorghum received from each county, 2016 to 2020, against the county's production",
          "Scale tickets at all sites at 14 per cent moisture, the terminal's tickets for grain moved in from the "
          "satellite sites counted once; production all practices, the service's October 2026 estimates.")
    header(ws4, 4, ["County", "Received (bushels at 14% moisture)", "County production 2016 to 2020 (bushels)",
                    "Received as a share of production"], [11, 18, 20, 16])
    for i, c in enumerate(W.MEMBERS, start=5):
        vals = [c, F["receipts_bu"][c], F["production_2016_2020"][c], F["receipts_share"][c] / 100]
        fmts = [None, "#,##0", "#,##0", "0.0%"]
        for j, (val, fm) in enumerate(zip(vals, fmts), start=1):
            cell = ws4.cell(row=i, column=j, value=val)
            cell.font = Font(name="Calibri", size=10)
            if fm:
                cell.number_format = fm
    ws4.freeze_panes = "B5"

    ws5 = wb.create_sheet("Notes")
    title(ws5, "Notes", "Prepared for the Board meeting of 19 November 2026.")
    notes = [
        ("Sources", "Crop and Livestock Reporting Service county estimates (downloads of March 2024 and October 2026; "
                    "the later download for 2016 to 2025, which holds the 2017 to 2021 revisions); Quillfield Re term "
                    "sheet and quote schedule of 14 October 2026; risk policy of 21 January 2026; member portal export "
                    "of 2 November 2026; elevator scale tickets and transfer log 2016 to 2020."),
        ("Withheld years", "The service did not publish Ardley's dryland estimates for 2002, 2011 and 2022, Elster's for "
                           "2002, 2011 and 2022, Pallard's for 2003 and 2011 and Tresham's for 2006 and 2011 (below "
                           "its publication standard, methods note 3.1). Its district estimates are the totals of all "
                           "their counties' estimates (methods note 2.1), so each withheld year is the district's "
                           "harvested acres and production less those of the district's published counties."),
        ("Trend", "Each year's yield is brought to 2027 by adding the term sheet's trend per year (rating basis)."),
        ("Preliminary", "The 2025 county estimates are the service's preliminary estimates of 24 February 2026."),
        ("Rounding", "Expected losses and rates to two decimals of a per cent, multiples to two decimals, shares to one "
                     "decimal of a per cent, dollars to the nearest hundred; calls are made on unrounded figures."),
    ]
    header(ws5, 4, ["Item", "Note"], [16, 110])
    for i, (k, v) in enumerate(notes, start=5):
        ws5.cell(row=i, column=1, value=k).font = Font(name="Calibri", size=10, bold=True)
        cell = ws5.cell(row=i, column=2, value=v)
        cell.font = Font(name="Calibri", size=10)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws5.row_dimensions[i].height = 14 * (1 + len(v) // 150)
    ws2.print_title_rows = "4:4"
    for sh in wb.worksheets:
        sh.page_setup.orientation = "landscape"
        sh.page_setup.paperSize = sh.PAPERSIZE_LETTER
        sh.page_setup.fitToWidth = 1
        sh.page_setup.fitToHeight = 0
        sh.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    wb.save(path)


def write_record(path, F):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["county", "county_ansi", "ag_district_code", "crop_year", "harvested_acres", "production_bu",
                     "yield_bu_per_acre", "source"])
        for r in F["record"]:
            wr.writerow([r["county"], r["ansi"], r["district"], r["year"], r["harvested"], r["production"],
                         "%.1f" % r["yld"], r["source"]])


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    F = compute(target)
    write_workbook(os.path.join(gdir, W.GOLDEN["workbook"]), F)
    write_record(os.path.join(gdir, W.GOLDEN["record"]), F)
    slim = {k: v for k, v in F.items() if k not in ("burn", "record")}
    for c in slim["covers"]:
        slim["covers"][c] = {k: v for k, v in slim["covers"][c].items() if k != "el_raw"}
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(slim, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return F
