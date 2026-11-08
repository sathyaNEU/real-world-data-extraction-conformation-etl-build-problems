"""The golden: figures.json, the provision workbook and the one-page note to the audit committee, all computed from
the cut pack through calc.py."""
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import bundle as B
import calc as C
from world import *

GOLDEN = {"workbook": "Ashlund_FY2026_stock_provision.xlsx", "note": "FY2026_stock_provision_note.pdf"}
SUBNAME = {"AHL": "Ashlund Home Ltd", "AHI": "Ashlund Home Ireland Ltd", "AHB": "Ashlund Home B.V."}


UNIT = {"provision": 1_000_000, "inventories": 500_000, "bb": 500_000, "shortfall": 250_000}


def mu(v, key):
    return round(C.rnd(v, UNIT[key]) / 1e6, 2)


def m1(v):
    return round(C.rnd(v, 100_000) / 1e6, 1)


def k10(v):
    return C.rnd(v, 10_000)


def rungs(target):
    out = {}
    for k in ("none", "blended", "fit", "sales2026", "jobber"):
        r = C.compute(target, capacity=k)
        out[k] = {"provision_m": m1(r["provision"]), "headroom_m": m1(r["headroom"]), "waiver": bool(r["waiver"]),
                  "provision": round(r["provision"], 2)}
    return out


def backtest_2023(target, g):
    w = B.vh_weeks(target)
    w = w[w["week"].map(lambda d: d.year) == 2023]
    return {"goods_in": round(float(w["goods_in_at_cost"].sum()), 0), "sold": round(float(w["sales_at_cost"].sum()), 0),
            "predicted": round(g["per_day"] * float(w["trading_days"].sum()), 0)}


def figures(target):
    g = C.compute(target)
    u25, v25 = C.shipped_2025(target)
    fig = {
        "call": "seek a waiver" if g["waiver"] else "no waiver needed",
        "provision_gbp_m": mu(g["provision"], "provision"),
        "borrowing_base_gbp_m": mu(g["bb"], "bb"),
        "drawn_gbp_m": round(g["drawn"] / 1e6, 2),
        "shortfall_gbp_m": mu(-g["headroom"], "shortfall") if g["waiver"] else 0.0,
        "headroom_gbp_m": mu(g["headroom"], "shortfall") if not g["waiver"] else 0.0,
        "inventories_after_provision_gbp_m": mu(g["carried"], "inventories"),
        "stock_at_cost_gbp": {**{k: k10(v) for k, v in g["gross_sub"].items()}, "VH": k10(g["vh_stock"]),
                              "total": k10(g["gross"])},
        "excess_by_company_gbp": {k: k10(v) for k, v in g["excess_sub"].items()},
        "excess_by_division_gbp": {d: k10(g["excess_div"].get(d, 0.0)) for d in DIVISIONS},
        "excess_total_gbp": k10(g["excess"]),
        "surplus_pool_gbp": k10(g["pool"]),
        "surplus_pool_gbp_m": m1(g["pool"]),
        "through_valuehall_gbp_m": m1(g["cap"]),
        "to_trade_buyers_gbp_m": m1(g["pool"] - g["cap"]),
        "through_valuehall_gbp": k10(g["cap"]),
        "to_trade_buyers_gbp": k10(g["pool"] - g["cap"]),
        "valuehall_per_trading_day_gbp": round(g["per_day"], 0),
        "valuehall_recovery": round(g["r_out"], 3),
        "trade_recovery": round(g["r_job"], 3),
        "store_days_2027": g["days27"],
        "units_2025_by_division": {d: C.rnd(u25[d], 1000) for d in DIVISIONS},
        "sales_2025_gbp_by_division": {d: C.rnd(v25[d], 1000) for d in DIVISIONS},
        "advance_pct": 62.5,
        "stocked_threshold_gbp": C.STOCKED,
        "fx_close": FX_CLOSE,
        "fx_avg_2025": FX_AVG_2025,
        "rungs": rungs(target),
        "backtest_2023": backtest_2023(target, g),
        "exact": {"provision": round(g["provision"], 2), "bb": round(g["bb"], 2), "headroom": round(g["headroom"], 2),
                  "gross": round(g["gross"], 2), "pool": round(g["pool"], 2), "cap": round(g["cap"], 2),
                  "units_2025": u25, "sales_2025": {d: round(v, 2) for d, v in v25.items()}},
    }
    return fig, g


# ---------------------------------------------------------------- workbook

THIN = Side(style="thin", color="9AA3AD")
HEAD = PatternFill("solid", fgColor="DCE3EA")
BOLD = Font(name="Calibri", bold=True, size=11)
NORM = Font(name="Calibri", size=11)
GBP = '#,##0;(#,##0);"-"'
GBPM = '#,##0.0;(#,##0.0)'


def _head(ws, row, vals):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=j, value=v if v != "" else None)
        c.font = BOLD
        c.fill = HEAD
        c.border = Border(bottom=THIN)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")


def write_workbook(target, fig, g, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bridge"
    ws["A1"] = "Ashlund Home Group plc: stock provision and borrowing base at 31 December 2026"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws["A2"] = "Sterling. Euro stock at the year-end rate of %.4f. Draft for the audit committee." % FX_CLOSE
    _head(ws, 4, ["", "GBP"])
    rows = [("Stock at cost", None, True)]
    for k in SUBS:
        rows.append(("  " + SUBNAME[k], g["gross_sub"][k], False))
    rows.append(("  Valuehall Stores Ltd", g["vh_stock"], False))
    rows.append(("Total stock at cost", g["gross"], True))
    rows.append(("", None, False))
    rows.append(("Excess stock at cost (beyond twelve months' net shipments)", None, True))
    for k in SUBS:
        rows.append(("  " + SUBNAME[k], g["excess_sub"][k], False))
    rows.append(("  Valuehall Stores Ltd stock", g["vh_stock"], False))
    rows.append(("Surplus to dispose of in 2027", g["pool"], True))
    rows.append(("  through Valuehall stores", g["cap"], False))
    rows.append(("  through trade buyers", g["pool"] - g["cap"], False))
    rows.append(("Expected proceeds ex VAT", None, True))
    rows.append(("  Valuehall stores", g["cap"] * g["r_out"], False))
    rows.append(("  trade buyers", (g["pool"] - g["cap"]) * g["r_job"], False))
    rows.append(("Provision", g["provision"], True))
    rows.append(("", None, False))
    rows.append(("Inventories after provision", g["carried"], True))
    rows.append(("Borrowing base (62.5%)", g["bb"], True))
    rows.append(("Drawn at 31 December 2026", g["drawn"], False))
    rows.append(("Headroom / (shortfall)", g["headroom"], True))
    r = 5
    for label, v, bold in rows:
        if label:
            ws.cell(row=r, column=1, value=label).font = BOLD if bold else NORM
        if v is not None:
            c = ws.cell(row=r, column=2, value=round(float(v), 0))
            c.number_format = GBP
            c.font = BOLD if bold else NORM
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Reported figures (GBP million: provision to the nearest million, inventories and "
            "borrowing base to the nearest 0.5 million, shortfall to the nearest 0.25 million)").font = BOLD
    r += 1
    for label, v in (("Provision", fig["provision_gbp_m"]),
                     ("Inventories after provision", fig["inventories_after_provision_gbp_m"]),
                     ("Borrowing base", fig["borrowing_base_gbp_m"]),
                     ("Drawn", fig["drawn_gbp_m"]),
                     ("Shortfall" if g["waiver"] else "Headroom", fig["shortfall_gbp_m"] if g["waiver"] else fig["headroom_gbp_m"])):
        ws.cell(row=r, column=1, value="  " + label)
        c = ws.cell(row=r, column=2, value=v)
        c.number_format = "0.00" if label in ("Drawn", "Shortfall", "Headroom") else "0.0"
        r += 1
    ws.cell(row=r + 1, column=1, value="Conclusion: the borrowing base is below the drawn balance; a waiver of clause 21.1 "
            "is needed before the audited accounts are delivered." if g["waiver"] else
            "Conclusion: the borrowing base covers the drawn balance; no waiver is needed.").font = BOLD
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 16

    ws = wb.create_sheet("Excess by division")
    ws["A1"] = "Excess stock at cost by company and division, GBP"
    ws["A1"].font = BOLD
    ex = C.excess_lines(target)
    piv = ex.groupby(["sub", "division"])["excess_gbp"].sum()
    _head(ws, 3, ["Division"] + [SUBNAME[k] for k in SUBS] + ["Group"])
    names = {"KD": "Kitchen and Dining", "SL": "Storage and Laundry", "LE": "Lighting and Electrical",
             "TH": "Tools and Hardware", "GO": "Garden and Outdoor"}
    r = 4
    for d in DIVISIONS:
        ws.cell(row=r, column=1, value="%s %s" % (d, names[d]))
        tot = 0.0
        for j, k in enumerate(SUBS, 2):
            v = float(piv.get((k, d), 0.0))
            tot += v
            ws.cell(row=r, column=j, value=round(v, 0)).number_format = GBP
        ws.cell(row=r, column=5, value=round(tot, 0)).number_format = GBP
        r += 1
    ws.cell(row=r, column=1, value="Total").font = BOLD
    for j, k in enumerate(SUBS, 2):
        c = ws.cell(row=r, column=j, value=round(g["excess_sub"][k], 0))
        c.number_format = GBP
        c.font = BOLD
    c = ws.cell(row=r, column=5, value=round(g["excess"], 0))
    c.number_format = GBP
    c.font = BOLD
    ws.column_dimensions["A"].width = 28
    for col in "BCDE":
        ws.column_dimensions[col].width = 18

    ws = wb.create_sheet("Disposal in 2027")
    ws["A1"] = "How the surplus is expected to go in 2027"
    ws["A1"].font = BOLD
    w = C.outlet_weeks(target)
    yr = w["week"].map(lambda d: d.year)
    full = w[(w.trading_days == 7) & (w.available >= C.STOCKED)]
    lines = [
        ("Valuehall sales at cost per trading day, full weeks with at least GBP 30,000 of stock to sell", round(g["per_day"], 2)),
        ("Store weeks behind that figure", g["n_weeks"]),
        ("Store trading days in 2027 (store plan)", g["days27"]),
        ("Valuehall sales at cost in 2027", round(g["cap"], 0)),
        ("Valuehall proceeds ex VAT over cost of sales, 2021 to 2026", round(g["r_out"], 4)),
        ("Trade buyer prices over stock at cost, all lots 2021 to 2026", round(g["r_job"], 4)),
    ]
    r = 3
    for label, v in lines:
        ws.cell(row=r, column=1, value=label)
        ws.cell(row=r, column=2, value=v)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Valuehall by year: what the stores were sent and sold").font = BOLD
    r += 1
    _head(ws, r, ["Year", "Goods in at cost", "Sales at cost", "Trading days", "Sales at cost per trading day",
                  "Sales at the stocked daily rate", "Sent to trade buyers at cost"])
    r += 1
    for y in sorted(set(yr)):
        sub = w[yr == y]
        cells = [y, round(sub.goods_in_at_cost.sum(), 0), round(sub.sales_at_cost.sum(), 0), int(sub.trading_days.sum()),
                 round(sub.sales_at_cost.sum() / sub.trading_days.sum(), 1), round(g["per_day"] * sub.trading_days.sum(), 0),
                 round(sub.to_trade_buyers_at_cost.sum(), 0)]
        for j, v in enumerate(cells, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j in (2, 3, 6, 7):
                c.number_format = GBP
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Stocked full weeks by store").font = BOLD
    r += 1
    _head(ws, r, ["Store", "Weeks", "Sales at cost per trading day"])
    r += 1
    for s, grp in full.groupby("store"):
        ws.cell(row=r, column=1, value=s)
        ws.cell(row=r, column=2, value=int(len(grp)))
        ws.cell(row=r, column=3, value=round(float((grp.sales_at_cost / grp.trading_days).mean()), 1))
        r += 1
    ws.column_dimensions["A"].width = 70
    for col in "BCDEFG":
        ws.column_dimensions[col].width = 17

    ws = wb.create_sheet("2025 shipments")
    ws["A1"] = ("Net shipments to customers in 2025 by division, net of returns and price credits (euro at the 2025 "
                "average rate of %.4f)" % FX_AVG_2025)
    ws["A1"].font = BOLD
    _head(ws, 3, ["Division", "Units", "GBP"])
    r = 4
    for d in DIVISIONS:
        ws.cell(row=r, column=1, value="%s %s" % (d, names[d]))
        ws.cell(row=r, column=2, value=fig["exact"]["units_2025"][d]).number_format = "#,##0"
        ws.cell(row=r, column=3, value=round(fig["exact"]["sales_2025"][d], 0)).number_format = GBP
        r += 1
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 16

    ws = wb.create_sheet("Excess lines")
    _head(ws, 1, ["Company", "Line key", "Group code", "Division", "Stock (each)", "Net shipments 2026 (each)",
                  "Excess (each)", "Unit cost GBP", "Excess at cost GBP"])
    r = 2
    for row in ex[ex.excess_qty > 0].sort_values(["sub", "code", "key"]).itertuples(index=False):
        vals = [row.sub, row.key, row.code, row.division, int(row.qty), int(row.net26), int(row.excess_qty),
                round(row.unit_gbp, 4), round(row.excess_gbp, 2)]
        for j, v in enumerate(vals, 1):
            ws.cell(row=r, column=j, value=v)
        r += 1
    for col, wd in zip("ABCDEFGHI", (9, 10, 11, 9, 12, 14, 12, 12, 15)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    wb.save(path)


# ---------------------------------------------------------------- the note

def write_note(fig, g, path):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs  # noqa: F401  (registers the fonts)
    ink = colors.HexColor("#1d1d1f")
    body = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.4, leading=12.6, textColor=ink, spaceAfter=5)
    h = ParagraphStyle("h", fontName="LiberationSans-Bold", fontSize=12.5, leading=15.5, textColor=colors.HexColor("#1f3a5f"),
                       spaceAfter=3)
    small = ParagraphStyle("s", fontName="LiberationSans", fontSize=7.8, leading=10, textColor=colors.HexColor("#5b5f66"))
    cell = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.6, leading=10.6, textColor=ink)
    cellb = ParagraphStyle("cb", parent=cell, fontName="LiberationSans-Bold")

    def gm(v):
        return "%.1f" % (C.rnd(v, 100_000) / 1e6)

    def gu(v, key):
        x = C.rnd(v, UNIT[key]) / 1e6
        return ("%.0f" % x) if key == "provision" else ("%.2f" % x).rstrip("0").rstrip(".") if key == "shortfall" \
            else "%.1f" % x

    t_rows = [[Paragraph("GBP million", cellb), Paragraph("", cellb)],
              [Paragraph("Stock at cost, group", cell), Paragraph(gm(g["gross"]), cell)],
              [Paragraph("Surplus to clear in 2027 (excess lines plus Valuehall's own stock)", cell), Paragraph(gm(g["pool"]), cell)],
              [Paragraph("of which Valuehall can sell in 2027", cell), Paragraph(gm(g["cap"]), cell)],
              [Paragraph("of which goes to trade buyers", cell), Paragraph(gm(g["pool"] - g["cap"]), cell)],
              [Paragraph("Provision (nearest million)", cellb), Paragraph(gu(g["provision"], "provision"), cellb)],
              [Paragraph("Inventories after provision (nearest 0.5 million)", cell), Paragraph(gu(g["carried"], "inventories"), cell)],
              [Paragraph("Borrowing base at 62.5 per cent (nearest 0.5 million)", cellb), Paragraph(gu(g["bb"], "bb"), cellb)],
              [Paragraph("Drawn at 31 December 2026", cell), Paragraph("%.2f" % (g["drawn"] / 1e6), cell)],
              [Paragraph(("Shortfall" if g["waiver"] else "Headroom") + " (nearest 0.25 million)", cellb),
               Paragraph(gu(abs(g["headroom"]), "shortfall"), cellb)]]
    t = Table(t_rows, colWidths=[118 * mm, 30 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#1f3a5f")),
                           ("ALIGN", (1, 0), (1, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]))
    s = [Paragraph("Ashlund Home Group plc: audit committee, 10 February 2027", small),
         Paragraph("FY2026 stock provision and the borrowing base test", h),
         Paragraph("<b>%s.</b> On the provision below, inventories after provision are about GBP %sm and the borrowing "
                   "base about GBP %sm against GBP %.2fm drawn at 31 December, a shortfall of about GBP %sm. Clause 21.1 is "
                   "breached on the audited accounts unless Northgate waives it in writing before they are delivered, so the "
                   "request should go to the bank now." % ("We need a waiver" if g["waiver"] else "No waiver is needed",
                                                          gu(g["carried"], "inventories"), gu(g["bb"], "bb"), g["drawn"] / 1e6,
                                                          gu(abs(g["headroom"]), "shortfall")), body),
         Paragraph("<b>Provision about GBP %sm.</b> Excess stock under FIN-07 (stock beyond twelve months' net shipments to "
                   "customers, transfers excluded) is GBP %sm at cost across the three trading companies, most of it the "
                   "Lumio range and the lines bought for the Kestrel programme. With Valuehall's own year-end stock the "
                   "surplus to clear in 2027 is GBP %sm." % (gu(g["provision"], "provision"), gm(g["excess"]), gm(g["pool"])),
                   body),
         Paragraph("<b>Why the provision is not the Valuehall rate on the whole surplus.</b> Valuehall has recovered about "
                   "%d pence in the pound on what it sells, in every year since 2021, and applying that to the whole surplus "
                   "would give a provision of about GBP %sm and no breach. But a stocked Valuehall store sells about GBP "
                   "%s of stock at cost a trading day however much it holds, at full price or in the January sale, and "
                   "its yearly sales grew only as stores opened. The five stores have %s trading days in 2027, so they "
                   "can take about GBP %sm of the surplus. In 2023, the one year the stores were sent more than they could "
                   "sell, they sold what that daily rate predicts and the rest went to trade buyers the following February. "
                   "The balance of GBP %sm goes to trade buyers, who have paid about %d pence in the pound on every lot "
                   "since 2021, large or small." % (round(100 * g["r_out"]), gm(g["pool"] * (1 - g["r_out"])),
                                                    "{:,.0f}".format(g["per_day"]), "{:,}".format(g["days27"]),
                                                    gm(g["cap"]), gm(g["pool"] - g["cap"]), round(100 * g["r_job"])), body),
         Spacer(1, 2 * mm), t, Spacer(1, 3 * mm),
         Paragraph("Workings, by company and division, and the line-level excess are in the provision workbook. Euro stock "
                   "is at the year-end rate of %.4f." % FX_CLOSE, small),
         Paragraph("Group Finance, 22 January 2027", small)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title="FY2026 stock provision", author="Group Finance", subject="",
                            creator="", producer="")
    doc.build(s)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    fig, g = figures(target)
    write_workbook(target, fig, g, os.path.join(gdir, GOLDEN["workbook"]))
    write_note(fig, g, os.path.join(gdir, GOLDEN["note"]))
    with open(fig_path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True, default=lambda o: int(o) if isinstance(o, np.integer) else float(o))
        f.write("\n")
    return fig, g
