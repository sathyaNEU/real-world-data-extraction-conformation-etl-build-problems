"""Readers for the cut pack: every figure the golden, the checks, the verifier and the ceiling compute is read from
target/ through these, never from the generator's truth."""
import datetime as dt
import os

import pandas as pd

from pack import FILES
from world import *

_C = {}
VALUEHALL = "Valuehall Stores Ltd"
GROUP_COS = ("Ashlund Home Ltd", "Ashlund Home Ireland Ltd", "Ashlund Home B.V.", VALUEHALL)


def _p(target, key):
    return os.path.join(target, FILES[key])


def _num_nl(s):
    return pd.to_numeric(s.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False))


def cached(fn):
    def w(target, *a, **k):
        key = (fn.__name__, target, a, tuple(sorted(k.items())))
        if key not in _C:
            _C[key] = fn(target, *a, **k)
        return _C[key]
    return w


@cached
def master(target):
    m = pd.read_csv(_p(target, "master"), dtype=str)
    m["Case Qty"] = m["Case Qty"].astype(int)
    return m


@cached
def current_code(target):
    """Group code -> current code (a superseded code resolves to its successor)."""
    m = master(target)
    out = dict(zip(m["Item Code"], m["Item Code"]))
    for _, r in m[m["Status"] == "Superseded"].iterrows():
        out[r["Item Code"]] = r["Superseded By"]
    return out


@cached
def division(target):
    m = master(target)
    return dict(zip(m["Item Code"], m["Division"]))


@cached
def case_qty(target):
    m = master(target)
    return dict(zip(m["Item Code"], m["Case Qty"]))


@cached
def ahb_xref(target):
    x = pd.read_csv(_p(target, "ahb_xref"), sep=";", dtype=str)
    cur = current_code(target)
    return {a: cur[g] for a, g in zip(x["Artikelnr"], x["Groepscode"])}


# ---------------------------------------------------------------- stock at 31 December 2026

@cached
def stock(target):
    """One row per trading company and line: quantity in eaches, value in the company's currency and in sterling."""
    out = []
    a = pd.read_csv(_p(target, "ahl_stock"), dtype={"Item Code": str})
    g = a.groupby("Item Code").agg(qty=("Qty On Hand", "sum"), value=("Stock Value", "sum")).reset_index()
    for _, r in g.iterrows():
        out.append(dict(sub="AHL", key=r["Item Code"], code=r["Item Code"], qty=int(r["qty"]), value_ccy=float(r["value"])))
    i = pd.read_excel(_p(target, "ahi_stock"), header=4, dtype={"Item No.": str})
    i["each"] = i["Quantity"] * i["Qty. per Unit of Measure"]
    g = i.groupby("Item No.").agg(qty=("each", "sum"), value=("Cost Amount", "sum")).reset_index()
    for _, r in g.iterrows():
        out.append(dict(sub="AHI", key=r["Item No."], code=r["Item No."], qty=int(r["qty"]), value_ccy=float(r["value"])))
    b = pd.read_csv(_p(target, "ahb_stock"), sep=";", dtype=str)
    b["qty"] = b["Voorraad"].astype(int)
    b["value"] = _num_nl(b["Waarde"])
    xr = ahb_xref(target)
    g = b.groupby("Artikelnr").agg(qty=("qty", "sum"), value=("value", "sum")).reset_index()
    for _, r in g.iterrows():
        out.append(dict(sub="AHB", key=r["Artikelnr"], code=xr[r["Artikelnr"]], qty=int(r["qty"]), value_ccy=float(r["value"])))
    df = pd.DataFrame(out)
    df["fx"] = df["sub"].map({"AHL": 1.0, "AHI": FX_CLOSE, "AHB": FX_CLOSE})
    df["value_gbp"] = df["value_ccy"] * df["fx"]
    df["division"] = df["code"].map(division(target))
    return df


# ---------------------------------------------------------------- order lines, every company on one footing

@cached
def orders(target, ahi_cases="each"):
    """Every order line of 2025 and 2026: company, date, customer, line key and group code, signed quantity in
    eaches, signed value and its currency, whether the line is a customer line, a transfer or cancelled, and for AHL
    the order number and document type.

    ahi_cases: how the AHI 2025 archive's quantities are read ("each" multiplies lines dated before the unit switch by
    the case quantity, "label" reads every line as labelled, "all" multiplies every archive line)."""
    rows = []
    a = pd.read_csv(_p(target, "ahl_orders"), dtype={"Item Code": str, "Account": str, "Order No": str})
    a["date"] = pd.to_datetime(a["Despatch Date"], format="%d/%m/%Y").dt.date
    for r in a.itertuples(index=False):
        rows.append(("AHL", r.date, r.Customer, r[6], r[6], int(r.Qty), float(r[9]), "GBP",
                     "cancelled" if r.Status == "Cancelled" else ("transfer" if r.Customer in GROUP_COS else "customer"),
                     r[0], r[2]))
    i = pd.read_excel(_p(target, "ahi_ship26"), dtype={"No.": str})
    for r in i.itertuples(index=False):
        sign = -1 if r[1] == "Return Receipt" else 1
        q = int(r[9]) * int(r[8]) * sign
        d = r[0].date() if hasattr(r[0], "date") else r[0]
        rows.append(("AHI", d, r[4], r[5], r[5], q, float(r[10]) * sign, "EUR",
                     "transfer" if r[4] in GROUP_COS else "customer", None, r[1]))
    h = pd.read_csv(_p(target, "ahi_arch25"), dtype={"Stock Code": str})
    h["date"] = pd.to_datetime(h["Doc Date"], format="%d/%m/%Y").dt.date
    cq = case_qty(target)
    for r in h.itertuples(index=False):
        sign = -1 if r[0] == "CRN" else 1
        q = int(r.Qty)
        if ahi_cases == "all" or (ahi_cases == "each" and r.date < AHI_UOM_SWITCH):
            q = q * cq[r[5]]
        rows.append(("AHI", r.date, r[4], r[5], r[5], q * sign, float(r[9]) * sign, "EUR",
                     "transfer" if r[4] in GROUP_COS else "customer", r[1], r[0]))
    b = pd.read_csv(_p(target, "ahb_orders"), sep=";", dtype=str)
    b["date"] = pd.to_datetime(b["Leverdatum"], format="%d-%m-%Y").dt.date
    b["q"] = b["Aantal"].astype(int)
    b["v"] = _num_nl(b["Bedrag"])
    xr = ahb_xref(target)
    for r in b.itertuples(index=False):
        rows.append(("AHB", r.date, r.Klantnaam, r.Artikelnr, xr[r.Artikelnr], int(r.q), float(r.v), "EUR",
                     "cancelled" if r.Status == "Geannuleerd" else ("transfer" if r.Klantnaam in GROUP_COS else "customer"),
                     r.Ordernr, r.Soort))
    df = pd.DataFrame(rows, columns=["sub", "date", "customer", "key", "code", "qty", "value", "cur", "kind", "doc",
                                     "dtype"])
    df["year"] = [d.year for d in df["date"]]
    return df


def net_2026(target):
    o = orders(target)
    o = o[(o.kind == "customer") & (o.year == 2026)]
    return o.groupby(["sub", "key"])["qty"].sum().to_dict()


# ---------------------------------------------------------------- the outlet, the lots, the facility

@cached
def vh_weeks(target):
    w = pd.read_csv(_p(target, "vh_weeks"), dtype={"promotion": str}, keep_default_na=False)
    w["week"] = pd.to_datetime(w["week_commencing"]).dt.date
    return w


def vh_year_end_stock(target):
    w = vh_weeks(target)
    last = w[w["week"] == w["week"].max()]
    return float(last["closing_stock_at_cost"].sum())


@cached
def lots(target):
    return pd.read_excel(_p(target, "lots"))


@cached
def drawn(target):
    r = pd.read_csv(_p(target, "rcf"))
    return int(r[r["value_date"] == "2026-12-31"]["drawn_balance_gbp"].iloc[0])


PLAN_DAYS_2027 = {"VH01": 349, "VH02": 363, "VH03": 363, "VH04": 363, "VH05": 363}   # the store plan's table
