"""Read the cut pack the way an analyst would and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the price register's two systems conformed into one table of sales, each with its
                            valuation record and electoral division
    change(b, route)        each area's price change, per cent, year to September 2026 on the year before
    designated(b, route)    the areas over 8 per cent
    ask(b, blocks_once)     each area's residential purchases in the year to September 2026 and the total paid"""
import csv
import datetime as dt
import os

import numpy as np

FILES = {
    "ppr_old": "ppr_residential_sales_filed_2024-10-01_to_2025-10-10.csv",
    "ppr_new": "ppr_residential_sales_filed_2025-10-01_to_2026-10-14.csv",
    "valuation": "valuation_register_dwellings_extract_2026-10-15.csv",
    "points": "address_points_buildings_extract_2026-10-15.csv",
    "eds": "bso_electoral_divisions_2026.csv",
    "census": "census_2022_dwelling_stock_by_area_and_type.xlsx",
}
Y1 = (dt.date(2024, 10, 1), dt.date(2025, 9, 30))
Y2 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
LINE = 8.0
VAT = 0.135
TYPES = ["Detached house", "Semi-detached house", "Terraced house", "Apartment"]
ROUTES = ("golden", "hedonic_built", "hedonic_second_hand", "hedonic_levels_check", "hedonic_monthly",
          "median", "per_m2", "type_weighted", "type_weighted_mean", "hedonic_no_location", "no_vat", "ed_type_cells")


def _csv(path, encoding="utf-8"):
    with open(path, newline="", encoding=encoding) as fh:
        return list(csv.DictReader(fh))


def eir(s):
    s = s.strip().upper().replace(" ", "")
    return s[:3] + " " + s[3:] if s else ""


def norm(a):
    return " ".join(a.lower().replace(",", " ").split())


def load(target, vat=True):
    import openpyxl
    val = _csv(os.path.join(target, FILES["valuation"]))
    by_pn = {r["property_number"]: r for r in val}
    by_eir = {r["eircode"]: r for r in val}
    by_addr = {norm(r["address"]): r for r in val}
    pts = {r["eircode"]: r for r in _csv(os.path.join(target, FILES["points"]))}
    sales = {}
    for r in _csv(os.path.join(target, FILES["ppr_old"]), encoding="cp1252"):
        v = by_eir.get(eir(r["Eircode"])) if r["Eircode"].strip() else by_addr.get(norm(r["Address"]))
        d = dt.datetime.strptime(r["Date of Sale (dd/mm/yyyy)"], "%d/%m/%Y").date()
        p = float(r["Price (€)"].replace("€", "").replace(",", ""))
        if r["VAT Exclusive"] == "Yes" and vat:
            p = round(p * (1 + VAT))
        sales[(v["property_number"], d)] = {"pn": v["property_number"], "date": d, "price": p,
                                            "market": r["Not Full Market Price"] == "No",
                                            "new": r["Description of Property"].startswith("New")}
    for r in _csv(os.path.join(target, FILES["ppr_new"])):
        d = dt.date.fromisoformat(r["sale_date"])
        sales[(r["property_number"], d)] = {"pn": r["property_number"], "date": d,
                                            "price": float(r["consideration_eur"]), "market": r["market_basis"] == "FMP",
                                            "new": r["dwelling_status"] == "NEW"}
    rows = []
    for s in sales.values():
        v = by_pn[s["pn"]]
        p = pts[v["eircode"]]
        s.update({"area": v["la_code"], "type": v["dwelling_type"], "floor": float(v["floor_area_m2"]),
                  "built": int(v["year_built"]), "ed": p["ed_code"], "building": p["building_id"]})
        rows.append(s)
    rows.sort(key=lambda s: (s["area"], s["date"], s["pn"]))
    ws = openpyxl.load_workbook(os.path.join(target, FILES["census"]), data_only=True)["Dwellings by type"]
    census = {r[0]: dict(zip(TYPES, r[2:6])) for r in ws.iter_rows(min_row=5, values_only=True) if r[0]}
    areas = sorted(set(s["area"] for s in rows))
    return {"sales": rows, "census": census, "areas": areas}


def _market(b, code):
    return [s for s in b["sales"] if s["area"] == code and s["market"] and Y1[0] <= s["date"] <= Y2[1]]


def _reg(ss, location=True, built=False, levels=False, monthly=False):
    y = np.array([s["date"] >= Y2[0] for s in ss])
    tt = np.array([s["type"] for s in ss])
    cols = [np.ones(len(ss))]
    if monthly:
        months = sorted(set((s["date"].year, s["date"].month) for s in ss))
        mm = [(s["date"].year, s["date"].month) for s in ss]
        cols += [np.array([m == k for m in mm], float) for k in months[1:]]
    else:
        cols.append(y.astype(float))
    cols += [np.log(np.array([s["floor"] for s in ss]) / 100.0), np.array([s["new"] for s in ss], float)]
    cols += [(tt == t).astype(float) for t in TYPES[1:]]
    if built:
        cols.append(np.array([min(s["built"], 2026) - 1990 for s in ss], float) / 10.0)
    if location:
        ee = np.array([s["ed"] for s in ss])
        cols += [(ee == e).astype(float) for e in sorted(set(ee))[1:]]
    X = np.column_stack(cols)
    p = np.array([s["price"] for s in ss])
    if levels:
        bb = np.linalg.lstsq(X, p, rcond=None)[0]
        fit0 = X.copy()
        fit0[:, 1] = 0
        return 100 * bb[1] / float(np.mean(fit0 @ bb))
    bb = np.linalg.lstsq(X, np.log(p), rcond=None)[0]
    if monthly:
        months = sorted(set((s["date"].year, s["date"].month) for s in ss))
        eff = np.concatenate([[0.0], bb[1:len(months)]])
        m1 = [eff[i] for i, k in enumerate(months) if dt.date(k[0], k[1], 1) < Y2[0]]
        m2 = [eff[i] for i, k in enumerate(months) if dt.date(k[0], k[1], 1) >= Y2[0]]
        return 100 * (np.mean(np.exp(m2)) / np.mean(np.exp(m1)) - 1)
    return 100 * (np.exp(bb[1]) - 1)


def change(b, route="golden"):
    out = {}
    for code in b["areas"]:
        ss = _market(b, code)
        y = np.array([s["date"] >= Y2[0] for s in ss])
        p = np.array([s["price"] for s in ss])
        fl = np.array([s["floor"] for s in ss])
        tt = np.array([s["type"] for s in ss])
        if route in ("golden", "no_vat"):
            v = _reg(ss)
        elif route == "hedonic_built":
            v = _reg(ss, built=True)
        elif route == "hedonic_second_hand":
            v = _reg([s for s in ss if not s["new"]])
        elif route == "hedonic_levels_check":
            v = _reg(ss, levels=True)
        elif route == "hedonic_monthly":
            v = _reg(ss, monthly=True)
        elif route == "hedonic_no_location":
            v = _reg(ss, location=False)
        elif route == "median":
            v = 100 * (np.median(p[y]) / np.median(p[~y]) - 1)
        elif route == "per_m2":
            v = 100 * (np.median((p / fl)[y]) / np.median((p / fl)[~y]) - 1)
        elif route in ("type_weighted", "type_weighted_mean"):
            w = b["census"][code]
            tot = sum(w.values())
            f = np.median if route == "type_weighted" else np.mean
            v = 100 * sum(w[t] / tot * (f(p[(tt == t) & y]) / f(p[(tt == t) & ~y]) - 1) for t in TYPES)
        elif route == "ed_type_cells":
            ee = np.array([s["ed"] for s in ss])
            lp = np.log(p)
            acc, wt = 0.0, 0
            for e in sorted(set(ee)):
                for t in TYPES:
                    m = (ee == e) & (tt == t)
                    if (m & y).sum() and (m & ~y).sum():
                        acc += (m & ~y).sum() * (lp[m & y].mean() - lp[m & ~y].mean())
                        wt += (m & ~y).sum()
            v = 100 * (np.exp(acc / wt) - 1)
        out[code] = float(v)
    return out


def designated(b, route="golden"):
    c = change(b, route)
    return sorted(k for k, v in c.items() if round(v, 1) > LINE)


def ask(b, blocks_once=True):
    """Each area's residential purchases in the year to September 2026, any basis, and the total paid including VAT;
    a block of apartments bought in one purchase carries the purchase's consideration on each apartment's line, so it
    is one purchase and its consideration is paid once."""
    out = {code: [0, 0.0] for code in b["areas"]}
    groups = {}
    for s in b["sales"]:
        if Y2[0] <= s["date"] <= Y2[1]:
            groups.setdefault((s["building"], s["date"], s["price"], s["market"]), []).append(s)
    for key, ss in groups.items():
        if blocks_once and len(ss) > 1 and not key[3]:
            out[ss[0]["area"]][0] += 1
            out[ss[0]["area"]][1] += ss[0]["price"]
        else:
            out[ss[0]["area"]][0] += len(ss)
            out[ss[0]["area"]][1] += sum(s["price"] for s in ss)
    return {k: (v[0], v[1]) for k, v in out.items()}
