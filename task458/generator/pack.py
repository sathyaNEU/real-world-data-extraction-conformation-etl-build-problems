"""Write the pack's data files, each in the layout of the system that produces it.

AHL runs a UK ERP (comma CSV, sterling, eaches); AHI moved to a new ERP on 1 January 2026 (its 2026 files are Excel
exports in euro with a unit of measure on every line) and its 2025 sales come from the old system's archive; AHB runs
a Dutch ERP (semicolon CSV, decimal comma, its own article numbers, mapped to group codes by its own table). Valuehall's
store weeks come from its stock system, the trade lots and the rate table from group finance, the utilisation from
treasury.
"""
import csv
import datetime as dt
import math

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

from world import *

FILES = {
    "ahl_stock": "AHL_stock_valuation_2026-12-31.csv",
    "ahi_stock": "AHI_Inventory_Valuation_31-12-2026.xlsx",
    "ahb_stock": "AHB_voorraadwaardering_31122026.csv",
    "ahb_xref": "AHB_artikel_groepscode.csv",
    "master": "group_item_master_2027-01-11.csv",
    "ahl_orders": "AHL_sales_order_lines_2025-2026.csv",
    "ahi_ship26": "AHI_Sales_Shipment_Lines_2026.xlsx",
    "ahi_arch25": "AHI_legacy_sales_archive_2025.csv",
    "ahb_orders": "AHB_verkooporderregels_2025-2026.csv",
    "vh_weeks": "valuehall_store_weeks_2021-2026.csv",
    "lots": "trade_lot_register_2021-2026.xlsx",
    "fx": "group_fx_rates_EURGBP_2025-2026.xlsx",
    "rcf": "rcf_daily_utilisation_2026.csv",
    "policy": "FIN-07_Stock_Provisioning_Policy.pdf",
    "facility": "RCF_Facility_Agreement_extract.pdf",
    "vhplan": "Valuehall_2027_Store_Plan.pdf",
    "open_po": "AHL_open_purchase_orders_2027.csv",
    "pallets": "dc_pallet_occupancy_2026.csv",
}
DISTRACTORS = ("open_po", "pallets")


def write_csv(path, header, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delim, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


def nl(v, dp=2):
    s = ("%." + str(dp) + "f") % v
    ip, fp = s.split(".") if "." in s else (s, "")
    neg = ip.startswith("-")
    ip = ip.lstrip("-")
    return ("-" if neg else "") + ip + ("," + fp if fp else "")


def ukd(d):
    return d.strftime("%d/%m/%Y")


def nld(d):
    return d.strftime("%d-%m-%Y")


# ---------------------------------------------------------------- keys the systems assign

def ahb_numbers(x):
    """AHB's own article numbers for the group lines it stocks or sells, and the superseded group codes some still map to."""
    rng = np.random.default_rng(SEED + 101)
    codes = sorted({r["code"] for r in x["rows"] if r["sub"] == "AHB"} |
                   {s["code"] for s in x["ship"] if s["sub"] == "AHB"} |
                   {t["code"] for t in x["transfers"] if t["sub"] == "AHB"})
    num, out = 310000, {}
    for c in codes:
        num += int(rng.integers(1, 9))
        out[c] = "%06d" % num
    return out


def superseded(x):
    """Group codes retired when a line was re-sourced: old code -> current code (the master lists both)."""
    rng = np.random.default_rng(SEED + 103)
    cand = [it for it in x["items"] if not it["lumio"]]
    pick = sorted(rng.choice(len(cand), 26, replace=False))
    out = {}
    for k in pick:
        it = cand[int(k)]
        old = "AH0%04d" % int(rng.integers(2000, 9999))
        while old in out:
            old = "AH0%04d" % int(rng.integers(2000, 9999))
        out[old] = it["code"]
    return out


# ---------------------------------------------------------------- stock registers

def write_ahl_stock(x, path):
    rng = np.random.default_rng(SEED + 111)
    rows = []
    for r in [r for r in x["rows"] if r["sub"] == "AHL"]:
        q = r["stock"]
        aisle = "%s-%02d-%02d" % ("ABCDEFGH"[int(rng.integers(8))], int(rng.integers(1, 41)), int(rng.integers(1, 7)))
        if q > 0 and rng.random() < 0.3:
            q1 = int(q * rng.uniform(0.15, 0.4))
            res = "R%s-%02d" % ("JKLM"[int(rng.integers(4))], int(rng.integers(1, 60)))
            parts = [(aisle, q1), (res, q - q1)]
        else:
            parts = [(aisle, q)]
        for b, qq in parts:
            rows.append([r["code"], r["desc"], b, qq, "%.2f" % r["cost"], "%.2f" % (qq * r["cost"])])
    rows.sort(key=lambda a: (a[0], a[2]))
    return write_csv(path, ["Item Code", "Description", "Bin", "Qty On Hand", "Unit Cost", "Stock Value"], rows)


def ahi_cs_rows(x):
    rng = np.random.default_rng(SEED + 113)
    return {r["code"] for r in x["rows"] if r["sub"] == "AHI" and r["case"] > 1 and rng.random() < 0.22}


def write_ahi_stock(x, path):
    cs = ahi_cs_rows(x)
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventory Valuation"
    ws.append(["Ashlund Home Ireland Ltd"])
    ws.append(["Inventory Valuation - Cost Specification"])
    ws.append(["As of 31/12/2026", None, None, None, None, None, None, "Currency: EUR"])
    ws.append([])
    hdr = ["Item No.", "Description", "Location Code", "Unit of Measure Code", "Qty. per Unit of Measure", "Quantity",
           "Unit Cost", "Cost Amount"]
    ws.append(hdr)
    for c in ws[5]:
        c.font = Font(bold=True)
    n = 0
    for r in sorted([r for r in x["rows"] if r["sub"] == "AHI"], key=lambda a: a["code"]):
        if r["code"] in cs and r["stock"] >= r["case"]:
            q = r["stock"] // r["case"]
            loose = r["stock"] - q * r["case"]
            ws.append([r["code"], r["desc"], "DUB-MAIN", "CS", r["case"], q, round(r["ucost"] * r["case"], 4),
                       round(q * r["case"] * r["ucost"], 2)])
            n += 1
            if loose:
                ws.append([r["code"], r["desc"], "DUB-PICK", "EA", 1, loose, round(r["ucost"], 4), round(loose * r["ucost"], 2)])
                n += 1
        else:
            ws.append([r["code"], r["desc"], "DUB-MAIN", "EA", 1, r["stock"], round(r["ucost"], 4),
                       round(r["stock"] * r["ucost"], 2)])
            n += 1
    for col, wd in zip("ABCDEFGH", (11, 34, 13, 12, 12, 10, 11, 13)):
        ws.column_dimensions[col].width = wd
    wb.save(path)
    return n


def write_ahb_stock(x, path, nums):
    rng = np.random.default_rng(SEED + 117)
    rows = []
    for r in sorted([r for r in x["rows"] if r["sub"] == "AHB"], key=lambda a: nums[a["code"]]):
        mag = "TLB" if rng.random() < 0.86 else "TLB-BUFFER"
        rows.append([nums[r["code"]], r["desc"].upper()[:30], mag, r["stock"], "ST", nl(r["ucost"], 4),
                     nl(r["stock"] * r["ucost"], 2)])
    return write_csv(path, ["Artikelnr", "Omschrijving", "Magazijn", "Voorraad", "Eenheid", "Kostprijs", "Waarde"], rows,
                     delim=";")


def write_ahb_xref(x, path, nums, sup):
    back = {}
    for old, new in sup.items():
        back.setdefault(new, old)
    rng = np.random.default_rng(SEED + 119)
    by_code = {it["code"]: it for it in x["items"]}
    rows = []
    for code, n in sorted(nums.items(), key=lambda a: a[1]):
        g = code
        if code in back and rng.random() < 0.6:
            g = back[code]
        rows.append([n, g, by_code[code]["desc"].upper()[:30]])
    return write_csv(path, ["Artikelnr", "Groepscode", "Omschrijving"], rows, delim=";")


def write_master(x, path, sup):
    rows = []
    for it in x["items"]:
        rows.append([it["code"], it["desc"], it["div"], it["case"], "Active", "", it["launch"].strftime("%Y-%m-%d")])
    by_code = {it["code"]: it for it in x["items"]}
    for old, new in sup.items():
        it = by_code[new]
        rows.append([old, it["desc"], it["div"], it["case"], "Superseded", new, it["launch"].strftime("%Y-%m-%d")])
    rows.sort(key=lambda a: a[0])
    return write_csv(path, ["Item Code", "Description", "Division", "Case Qty", "Status", "Superseded By", "First Received"],
                     rows)


# ---------------------------------------------------------------- order books

def lines_for(x, sub, years):
    out = [s for s in x["ship"] if s["sub"] == sub and s["date"].year in years]
    out += [t for t in x["transfers"] if t["sub"] == sub and t["date"].year in years]
    out.sort(key=lambda a: (a["date"], a["acct"], a["kind"] == "return", a["code"], a["qty"]))
    return out


def number_orders(lines, prefix, start):
    """Group a day's lines for one customer and kind into one document; number documents and lines."""
    docs, k = {}, start
    out = []
    for ln in lines:
        key = (ln["date"], ln["acct"], ln["kind"])
        if key not in docs:
            k += 1
            docs[key] = [prefix % k, 0]
        docs[key][1] += 1
        out.append((docs[key][0], docs[key][1], ln))
    return out


def write_ahl_orders(x, path):
    """AHL's order line report. A price-only credit is raised from the original order's credit screen on the non-stock
    code; the report prints it under that order, with the credit's own date and a line number from 990."""
    by_code = {it["code"]: it for it in x["items"]}
    lines = [ln for ln in lines_for(x, "AHL", (2025, 2026)) if ln["kind"] != "price"]
    numbered = number_orders(lines, "SO%07d", 2510400)
    doc_of = {}
    for doc, ln_no, ln in numbered:
        if ln["kind"] == "ship":
            doc_of.setdefault((ln["date"], ln["acct"]), doc)
    rows = []
    for doc, ln_no, ln in numbered:
        kind = ln["kind"]
        dtype = "RTN" if kind == "return" else "DESP"
        status = "Cancelled" if kind == "cancelled" else "Invoiced"
        rows.append([doc, ln_no * 10, dtype, ukd(ln["date"]), ln["acct"], ln["cust"], ln["code"], by_code[ln["code"]]["desc"],
                     ln["qty"], "%.2f" % ln["value"], status])
    nxt = {}
    for ln in [c for c in x["ship"] if c["sub"] == "AHL" and c["kind"] == "price"]:
        doc = doc_of[ln["orig"]]
        nxt[doc] = nxt.get(doc, 980) + 10
        rows.append([doc, nxt[doc], "PRICE", ukd(ln["date"]), ln["acct"], ln["cust"], ln["code"], "PRICE ADJUSTMENT", 0,
                     "%.2f" % ln["value"], "Invoiced"])
    rows.sort(key=lambda r: (r[3][6:] + r[3][3:5] + r[3][:2], r[0], r[1]))
    return write_csv(path, ["Order No", "Line", "Doc Type", "Despatch Date", "Account", "Customer", "Item Code",
                            "Description", "Qty", "Line Value", "Status"], rows)


def write_ahi_ship26(x, path):
    by_code = {it["code"]: it for it in x["items"]}
    cs = ahi_cs_rows(x)
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales Shipment Lines"
    hdr = ["Posting Date", "Document Type", "Document No.", "Sell-to Customer No.", "Customer Name", "No.", "Description",
           "Unit of Measure Code", "Qty. per Unit of Measure", "Quantity", "Line Amount"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    n, k_s, k_r = 0, 260000, 260000
    seen = {}
    for ln in lines_for(x, "AHI", (2026,)):
        if ln["kind"] == "cancelled":
            continue
        key = (ln["date"], ln["acct"], ln["kind"])
        if key not in seen:
            if ln["kind"] == "return":
                k_r += 1
                seen[key] = "RRCPT-%06d" % k_r
            else:
                k_s += 1
                seen[key] = "SSHPT-%06d" % k_s
        case = by_code[ln["code"]]["case"]
        q = abs(ln["qty"])
        if ln["code"] in cs and q % case == 0 and ln["kind"] != "transfer":
            uom, per, qq = "CS", case, q // case
        else:
            uom, per, qq = "EA", 1, q
        dtype = "Return Receipt" if ln["kind"] == "return" else "Shipment"
        ws.append([ln["date"], dtype, seen[key], ln["acct"], ln["cust"], ln["code"], by_code[ln["code"]]["desc"], uom, per, qq,
                   round(abs(ln["value"]), 2)])
        ws.cell(row=ws.max_row, column=1).number_format = "dd/mm/yyyy"
        n += 1
    for col, wd in zip("ABCDEFGHIJK", (12, 15, 14, 12, 26, 10, 34, 10, 10, 10, 12)):
        ws.column_dimensions[col].width = wd
    wb.save(path)
    return n


def write_ahi_arch25(x, path):
    """The old system's archive of 2025 invoices and credit notes; its report prints each item's current stock unit."""
    by_code = {it["code"]: it for it in x["items"]}
    rows = []
    k_i, k_c = 70400, 9100
    seen = {}
    for ln in lines_for(x, "AHI", (2025,)):
        if ln["kind"] == "cancelled":
            continue
        key = (ln["date"], ln["acct"], ln["kind"])
        if key not in seen:
            if ln["kind"] == "return":
                k_c += 1
                seen[key] = "CRN%06d" % k_c
            else:
                k_i += 1
                seen[key] = "INV%06d" % k_i
        case = by_code[ln["code"]]["case"]
        q = abs(ln["qty"])
        if ln["date"] < AHI_UOM_SWITCH:
            q = q // case
        rows.append(["CRN" if ln["kind"] == "return" else "INV", seen[key], ukd(ln["date"]), ln["acct"], ln["cust"],
                     ln["code"], by_code[ln["code"]]["desc"], q, "EA", "%.2f" % abs(ln["value"])])
    return write_csv(path, ["Doc Type", "Doc No", "Doc Date", "Cust Code", "Cust Name", "Stock Code", "Description", "Qty",
                            "UOM", "Line Value"], rows)


def write_ahb_orders(x, path, nums):
    by_code = {it["code"]: it for it in x["items"]}
    rows = []
    for doc, ln_no, ln in number_orders(lines_for(x, "AHB", (2025, 2026)), "%07d", 4100500):
        kind = ln["kind"]
        soort = "Retour" if kind == "return" else "Levering"
        status = "Geannuleerd" if kind == "cancelled" else "Gefactureerd"
        rows.append([doc, ln_no, ln["acct"], ln["cust"], nums[ln["code"]], by_code[ln["code"]]["desc"].upper()[:30],
                     ln["qty"], "ST", nl(ln["value"], 2), nld(ln["date"]), soort, status])
    return write_csv(path, ["Ordernr", "Regel", "Klantnr", "Klantnaam", "Artikelnr", "Omschrijving", "Aantal", "Eenheid",
                            "Bedrag", "Leverdatum", "Soort", "Status"], rows, delim=";")


# ---------------------------------------------------------------- outlet, lots, rates, facility

def write_vh_weeks(x, path):
    name = {s[0]: s[1] for s in STORES}
    rows = []
    for w in sorted(x["weeks"], key=lambda a: (a["week"], a["store"])):
        rows.append([w["store"], name[w["store"]], w["week"].strftime("%Y-%m-%d"), w["days"], "%.2f" % w["goods_in"],
                     "%.2f" % w["sales_cost"], "%.2f" % w["sales_exvat"], "%.2f" % w["jobbed"], "%.2f" % w["close"],
                     w["band"]])
    return write_csv(path, ["store", "store_name", "week_commencing", "trading_days", "goods_in_at_cost", "sales_at_cost",
                            "sales_ex_vat", "to_trade_buyers_at_cost", "closing_stock_at_cost", "promotion"], rows)


def write_lots(x, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lots"
    ws.append(["Lot", "Contract date", "Seller", "Buyer", "Pallets", "Stock at cost (GBP)", "Price ex VAT (GBP)", "Collected"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for o in x["lots"]:
        ws.append([o["lot"], o["date"], o["seller"], o["buyer"], o["pallets"], round(o["cost"], 2), o["price"], o["collected"]])
        ws.cell(row=ws.max_row, column=2).number_format = "dd/mm/yyyy"
        ws.cell(row=ws.max_row, column=8).number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDEFGH", (8, 13, 26, 24, 8, 18, 18, 12)):
        ws.column_dimensions[col].width = wd
    wb.save(path)
    return len(x["lots"])


def write_fx(x, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "EURGBP"
    ws.append(["Group rate table: pounds sterling per euro"])
    ws.append(["Income statement items are translated at the year's average rate and balance sheet items at the "
               "year-end rate."])
    ws.append([])
    ws.append(["Month", "Average rate", "Month-end rate"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for o in x["fx"]:
        ws.append([dt.date(o["year"], o["month"], 1).strftime("%b %Y"), o["avg"], o["close"]])
    ws.append([])
    ws.append(["Year 2025 average", FX_AVG_2025, None])
    ws.append(["Year 2026 average", FX_AVG_2026, None])
    ws.append(["Year-end rate 31 December 2026", None, FX_CLOSE])
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 15
    wb.save(path)
    return len(x["fx"])


def write_rcf(x, path):
    rows = [[u["date"].strftime("%Y-%m-%d"), "%d" % u["drawn"]] for u in x["util"]]
    return write_csv(path, ["value_date", "drawn_balance_gbp"], rows)


def write_open_po(x, path):
    rng = np.random.default_rng(SEED + 131)
    sup = ["Ningbo Everbright Housewares Co", "Foshan Meiling Ceramics", "Xiamen Brightway Lighting",
           "Yongkang Toolmaster Industrial", "Binh Duong Rattan Export JSC", "Moradabad Metal Crafts Pvt"]
    rows = []
    norm = [r for r in x["rows"] if r["sub"] == "AHL" and r["kind"] == "normal"]
    k = 88200
    for i in range(240):
        r = norm[int(rng.integers(len(norm)))]
        k += int(rng.integers(1, 4))
        due = dt.date(2027, int(rng.integers(1, 7)), int(rng.integers(1, 28)))
        q = int(r["case"] * max(1, round(r["wk"] * rng.uniform(4, 12) / r["case"])))
        rows.append(["PO%06d" % k, sup[int(rng.integers(len(sup)))], r["code"], q, "%.2f" % (r["cost"] * 0.82),
                     "USD" if rng.random() < 0.85 else "GBP", due.strftime("%d/%m/%Y")])
    return write_csv(path, ["PO No", "Supplier", "Item Code", "Qty Outstanding", "Unit Price", "Currency", "Due Date"], rows)


def write_pallets(x, path):
    rng = np.random.default_rng(SEED + 137)
    rows = []
    cap = {"Leicester DC": 14200, "Dublin DC": 2600, "Tilburg DC": 4100}
    for m in [d for d in [dt.date(2026, 1, 5) + dt.timedelta(days=7 * k) for k in range(52)]]:
        for dc, c in cap.items():
            occ = int(c * min(0.99, 0.78 + 0.12 * (m.month >= 9) + rng.normal(0, 0.025)))
            rows.append([m.strftime("%Y-%m-%d"), dc, c, occ])
    return write_csv(path, ["week_commencing", "site", "pallet_positions", "positions_occupied"], rows)
