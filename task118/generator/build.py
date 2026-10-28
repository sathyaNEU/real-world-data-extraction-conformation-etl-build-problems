"""Write the pack: the Statistics Office's quarterly series (two layouts), the duty and GST rates, the Treasury's
appraisal manual, the thread, Customs' declarations with the procedure codes, CE14 and the warehouse register, and three
files the solution never uses."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import docs
import params as P
import postprocess
import world as W

FILES = P.FILES
PACK = list(FILES)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def _xlsx(path, sheets, made, saved, person, fmts=None):
    wb = Workbook()
    for i, (title, header, rows, widths) in enumerate(sheets):
        ws = wb.active if i == 0 else wb.create_sheet()
        ws.title = title
        if header:
            ws.append(header)
            for c in ws[1]:
                c.font = Font(bold=True)
                c.fill = PatternFill("solid", fgColor="DCE3EC")
                c.alignment = Alignment(vertical="top", wrap_text=True)
        for r in rows:
            ws.append(list(r))
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
        if header:
            ws.freeze_panes = "A2"
    wb.properties.creator = person
    wb.properties.lastModifiedBy = person
    wb.save(path)
    postprocess.scrub(path, P.ORG, saved[:10])
    postprocess.finish_office(path, made, saved, P.ORG, person=person)


def iso(d):
    return d.isoformat() if d else ""


def build(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    S = W.series()
    rates = W.rate_history(S)
    names = {c: n for c, n, *_ in P.DUTIES}
    # the Statistics Office: 2012 onwards as published (long), the 2008-2011 back series (one sheet per duty)
    new = []
    for t in range(P.NEW_FROM, P.QUARTERS):
        for code, *_ in P.DUTIES:
            status = "Preliminary" if t >= P.QUARTERS - 2 else "Revised"
            new.append([W.qlabel(t), names[code], "%.1f" % (S[code]["volume"][t] / 1000.0),
                        "%.3f" % S[code]["price"][t], status])
    _csv(F["series_new"], ["quarter", "duty", "duty_paid_clearances_thousand_litres",
                           "average_shelf_price_gbp_per_litre_2026_prices", "status"], new)
    sheets = []
    for code, *_ in P.DUTIES:
        rows = [["%d Q%d" % (P.FIRST_YEAR + t // 4, t % 4 + 1), round(S[code]["volume"][t] / 1000.0, 1),
                 round(float(S[code]["price"][t]), 3)] for t in range(0, P.NEW_FROM)]
        sheets.append((names[code], ["Quarter", "Duty-paid clearances (000 litres)",
                                     "Average shelf price (GBP per litre, 2026 prices)"], rows, [12, 22, 26]))
    _xlsx(F["series_old"], sheets, "2026-04-08T09:20:00Z", "2026-04-09T14:05:00Z", P.PEOPLE["stats"])
    # rates
    _xlsx(F["rates"], [("Duty rates", ["Duty", "Effective from", "Rate (GBP per litre)", "Set in"],
                        [[names[c], d, r, "Budget %d" % (d.year - 1 if d.month == 1 else d.year)] for c, d, r in rates],
                        [14, 14, 18, 14]),
                       ("GST", ["Effective from", "Rate"], [[dt.date(2008, 6, 1), 0.03], [dt.date(2011, 4, 1), 0.05]],
                        [14, 10])],
          "2019-03-11T10:00:00Z", "2026-03-04T16:30:00Z", P.TREASURY_UNIT)
    # documents
    docs.manual(F["manual"])
    postprocess.scrub(F["manual"], "Microsoft Word 2016", "2026-04-14T11:10:00")
    docs.ce14(F["cpc_note"])
    postprocess.scrub(F["cpc_note"], "Microsoft Word 2016", "2025-01-20T09:45:00")
    with open(F["thread"], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(docs.thread())
    # the declarations
    lines, truth, whs = W.declarations(S, rates)
    _csv(F["declarations"], ["declaration_no", "item_no", "cpc", "duty_code", "accepted_at_utc", "trader",
                             "warehouse_from", "warehouse_to", "quantity_litres", "method_of_payment", "duty_gbp",
                             "related_declaration", "status"],
         [[x["declaration"], x["item"], x["cpc"], x["duty_code"],
           x["accepted_utc"].strftime("%Y-%m-%dT%H:%M:%SZ"), x["trader"], x["warehouse_from"], x["warehouse_to"],
           x["quantity_litres"], x["method_of_payment"], "%.2f" % x["duty_gbp"], x["reference"], x["status"]]
          for x in lines])
    _csv(F["cpc"], ["cpc", "description", "duty"], [list(x) for x in W.CPC])
    _xlsx(F["warehouses"], [("Approved warehouses", ["Warehouse", "Name", "Premises", "Goods", "Approved from",
                                                     "Approval ended"],
                             [[w["id"], w["name"], w["premises"], w["goods"], w["approved"], w["ended"] or ""]
                              for w in whs], [11, 30, 44, 11, 14, 15]),
                            ("Duty codes", ["Code", "Duty"], [[c, names[c]] for c, *_ in P.DUTIES] +
                             [["REBF", "Marked gas oil (rebated)"]], [8, 26])],
          "2018-05-02T09:00:00Z", "2026-09-29T15:40:00Z", P.PEOPLE["customs"])
    # distractors: monthly cash receipts, the retail price survey's shop quotes, travellers' allowance declarations
    rs = np.random.default_rng(P.SEED + 50)
    rec = []
    for y in range(2020, 2027):
        for m in range(1, 13):
            if (y, m) > (2026, 9):
                break
            t = (y - P.FIRST_YEAR) * 4 + (m - 1) // 3
            for code, *_ in P.DUTIES:
                vol = S[code]["volume"][min(t, P.QUARTERS - 1)] / 3.0
                cash = vol * S[code]["duty"][min(t, P.QUARTERS - 1)] * rs.normal(1.0, 0.04)
                rec.append(["%d-%02d" % (y, m), names[code], "%.0f" % cash])
    _csv(F["receipts"], ["month_received", "duty", "receipts_gbp"], rec)
    quotes = []
    shops = ["Harbour Stores", "Quayside Wines", "Ardvane Stores", "Northgate Superstore", "Port Haverel Market",
             "Mill Lane Off Licence", "Moorside Garage", "Eastquay Fuels", "Ropewalk Deli", "Marine Parade Stores"]
    items = {"BEER": ["Lager 4 x 440ml", "Bitter 500ml", "Pilsner 6 x 330ml"], "CIDR": ["Cider 500ml", "Cider 4 x 440ml"],
             "WINE": ["Red wine 75cl", "White wine 75cl", "Rose wine 75cl"], "SPIR": ["Whisky 70cl", "Gin 70cl", "Vodka 70cl"],
             "FUEL": ["Unleaded petrol (litre)", "Diesel (litre)"]}
    for mo in range(1, 10):
        for sh in shops:
            for code, its in items.items():
                if code == "FUEL" and "Garage" not in sh and "Fuels" not in sh:
                    continue
                for it in its:
                    base = {"BEER": 5.6, "CIDR": 2.4, "WINE": 7.4, "SPIR": 14.3, "FUEL": 1.42}[code]
                    quotes.append(["2026-%02d" % mo, sh, names[code], it, "%.2f" % (base * rs.normal(1.0, 0.07))])
    _csv(F["price_quotes"], ["month", "shop", "duty", "item", "price_gbp"], quotes)
    pas = []
    d0 = dt.date(2025, 1, 1)
    for k in range(5200):
        day = d0 + dt.timedelta(days=int(rs.integers(0, 638)))
        port = ["Port Haverel ferry", "Eskerholm Airport"][int(rs.random() < 0.45)]
        pas.append(["PA%07d" % (2100000 + k * 3), iso(day), port, int(rs.integers(1, 5)),
                    "%.1f" % max(0.0, rs.normal(1.1, 0.9)), "%.1f" % max(0.0, rs.normal(2.8, 2.0)),
                    "%.0f" % max(0, rs.normal(160, 120))])
    _csv(F["passengers"], ["declaration_ref", "arrival_date", "port", "travellers", "spirits_litres", "wine_litres",
                           "cigarettes"], pas)
    return dict(S=S, rates=rates, lines=lines, truth=truth, whs=whs)
