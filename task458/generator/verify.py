"""An independent recompute of every graded figure from the cut pack with the standard library and openpyxl only (no
pandas, no generator module but the file names and the dates fixed in the pack's documents), compared with
figures.json."""
import csv
import datetime as dt
import json
import os
from collections import defaultdict

from openpyxl import load_workbook

from pack import FILES

YE_RATE = 0.8648            # the rate table's year-end rate
AVG25 = 0.8573              # the rate table's 2025 average
SWITCH = dt.date(2025, 7, 7)
DAYS_2027 = 349 + 4 * 363   # the store plan's table
GROUP = {"Ashlund Home Ltd", "Ashlund Home Ireland Ltd", "Ashlund Home B.V.", "Valuehall Stores Ltd"}


def rows(path, delim=","):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


def nl(s):
    return float(s.replace(".", "").replace(",", "."))


def half_up(v, unit):
    q = v / unit
    return int(q + 0.5) * unit if q >= 0 else -int(-q + 0.5) * unit


def main(target, fig_path):
    f = json.load(open(fig_path))
    p = lambda k: os.path.join(target, FILES[k])
    master = {r["Item Code"]: r for r in rows(p("master"))}
    cur = {k: (r["Superseded By"] or k) for k, r in master.items()}
    xref = {r["Artikelnr"]: cur[r["Groepscode"]] for r in rows(p("ahb_xref"), ";")}
    # stock, eaches and value in the company's currency
    stock = defaultdict(lambda: [0, 0.0])
    for r in rows(p("ahl_stock")):
        stock[("AHL", r["Item Code"])][0] += int(r["Qty On Hand"])
        stock[("AHL", r["Item Code"])][1] += float(r["Stock Value"])
    ws = load_workbook(p("ahi_stock"), read_only=True).active
    for r in list(ws.iter_rows(values_only=True))[5:]:
        if r[0]:
            stock[("AHI", str(r[0]))][0] += int(r[5]) * int(r[4])
            stock[("AHI", str(r[0]))][1] += float(r[7])
    for r in rows(p("ahb_stock"), ";"):
        stock[("AHB", r["Artikelnr"])][0] += int(r["Voorraad"])
        stock[("AHB", r["Artikelnr"])][1] += nl(r["Waarde"])
    fx = {"AHL": 1.0, "AHI": YE_RATE, "AHB": YE_RATE}
    # 2026 net shipments to customers
    net = defaultdict(int)
    sales25_u, sales25_v = defaultdict(int), defaultdict(float)

    def div_of(code):
        return master[cur.get(code, code)]["Division"]

    ahl = [r for r in rows(p("ahl_orders")) if r["Status"] != "Cancelled" and r["Customer"] not in GROUP]
    for r in ahl:
        r["d"] = dt.datetime.strptime(r["Despatch Date"], "%d/%m/%Y").date()
    # the customer's price for each item before the April 2025 rise, from its own despatches
    before = {}
    for r in ahl:
        if r["Doc Type"] == "DESP" and r["d"] < dt.date(2025, 4, 1) and int(r["Qty"]) > 0:
            u = round(float(r["Line Value"]) / int(r["Qty"]), 2)
            k = (r["Customer"], r["Item Code"])
            before[k] = min(before.get(k, u), u)
    lines_of = defaultdict(list)
    for r in ahl:
        if r["Doc Type"] == "DESP":
            lines_of[(r["Order No"], r["Customer"])].append(r)
    for r in ahl:
        q = int(r["Qty"])
        if r["d"].year == 2026:
            net[("AHL", r["Item Code"])] += q
        elif r["d"].year == 2025:
            if r["Doc Type"] != "PRICE":
                sales25_u[div_of(r["Item Code"])] += q
                sales25_v[div_of(r["Item Code"])] += float(r["Line Value"])
                continue
            # a price credit on the non-stock code belongs to the one line of its order whose overcharge it equals
            hits = []
            for l in lines_of[(r["Order No"], r["Customer"])]:
                b = before.get((l["Customer"], l["Item Code"]))
                if b is not None and int(l["Qty"]) > 0 and l["d"] >= dt.date(2025, 4, 1):
                    over = round(float(l["Line Value"]) - int(l["Qty"]) * b, 2)
                    if abs(over + float(r["Line Value"])) < 0.006:
                        hits.append(l["Item Code"])
            assert len(hits) == 1, (r["Order No"], r["Line Value"], hits)
            sales25_v[div_of(hits[0])] += float(r["Line Value"])
    ws = load_workbook(p("ahi_ship26"), read_only=True).active
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[4] in GROUP:
            continue
        sign = -1 if r[1] == "Return Receipt" else 1
        net[("AHI", str(r[5]))] += sign * int(r[9]) * int(r[8])
    for r in rows(p("ahi_arch25")):
        if r["Cust Name"] in GROUP:
            continue
        d = dt.datetime.strptime(r["Doc Date"], "%d/%m/%Y").date()
        sign = -1 if r["Doc Type"] == "CRN" else 1
        q = int(r["Qty"]) * (int(master[r["Stock Code"]]["Case Qty"]) if d < SWITCH else 1)
        sales25_u[div_of(r["Stock Code"])] += sign * q
        sales25_v[div_of(r["Stock Code"])] += sign * float(r["Line Value"]) * AVG25
    for r in rows(p("ahb_orders"), ";"):
        if r["Status"] == "Geannuleerd" or r["Klantnaam"] in GROUP:
            continue
        d = dt.datetime.strptime(r["Leverdatum"], "%d-%m-%Y").date()
        q = int(r["Aantal"])
        if d.year == 2026:
            net[("AHB", r["Artikelnr"])] += q
        elif d.year == 2025:
            sales25_u[div_of(xref[r["Artikelnr"]])] += q
            sales25_v[div_of(xref[r["Artikelnr"]])] += nl(r["Bedrag"]) * AVG25
    gross = excess = 0.0
    by_sub = defaultdict(float)
    for (sub, key), (q, v) in stock.items():
        gbp = v * fx[sub]
        gross += gbp
        e = min(q, max(0, q - max(0, net.get((sub, key), 0))))
        val = e * (gbp / q) if q else 0.0
        excess += val
        by_sub[sub] += val
    # the outlet
    wk = rows(p("vh_weeks"))
    wk.sort(key=lambda r: (r["store"], r["week_commencing"]))
    prev, per_day, sold_c, sold_x = {}, [], 0.0, 0.0
    for r in wk:
        op = prev.get(r["store"], 0.0)
        days = int(r["trading_days"])
        if days == 7 and op + float(r["goods_in_at_cost"]) >= 30000:
            per_day.append(float(r["sales_at_cost"]) / 7)
        prev[r["store"]] = float(r["closing_stock_at_cost"])
        sold_c += float(r["sales_at_cost"])
        sold_x += float(r["sales_ex_vat"])
    last = max(r["week_commencing"] for r in wk)
    vh = sum(float(r["closing_stock_at_cost"]) for r in wk if r["week_commencing"] == last)
    rate = sum(per_day) / len(per_day)
    r_out = sold_x / sold_c
    ws = load_workbook(p("lots"), read_only=True).active
    lr = [r for r in list(ws.iter_rows(values_only=True))[1:] if r[0]]
    r_job = sum(float(r[6]) for r in lr) / sum(float(r[5]) for r in lr)
    drawn = int([r for r in rows(p("rcf")) if r["value_date"] == "2026-12-31"][0]["drawn_balance_gbp"])
    pool = excess + vh
    cap = min(pool, rate * DAYS_2027)
    prov = pool - (cap * r_out + (pool - cap) * r_job)
    gross += vh
    bb = 0.625 * (gross - prov)
    got = {
        "provision_gbp_m": half_up(prov, 1000000) / 1e6,
        "borrowing_base_gbp_m": half_up(bb, 500000) / 1e6,
        "shortfall_gbp_m": half_up(drawn - bb, 250000) / 1e6,
        "inventories_after_provision_gbp_m": half_up(gross - prov, 500000) / 1e6,
        "excess_by_company_gbp": {k: half_up(v, 10000) for k, v in by_sub.items()},
        "units_2025_by_division": {k: half_up(v, 1000) for k, v in sales25_u.items()},
        "sales_2025_gbp_by_division": {k: half_up(v, 1000) for k, v in sales25_v.items()},
    }
    bad = []
    for k, v in got.items():
        want = f[k]
        if isinstance(v, dict):
            for kk, vv in v.items():
                if abs(vv - want[kk]) > 1e-9:
                    bad.append("%s.%s %s against %s" % (k, kk, vv, want[kk]))
        elif abs(v - want) > 1e-9:
            bad.append("%s %s against %s" % (k, v, want))
    if f["call"] != ("seek a waiver" if drawn > bb else "no waiver needed"):
        bad.append("call")
    print("verify: %d figures recomputed independently, %d differ%s" % (
        3 + 1 + 3 + 10 + 2, len(bad), (": " + "; ".join(bad)) if bad else ""))
    return not bad
