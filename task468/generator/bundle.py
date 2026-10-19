"""Read the shipped pack as a solver would: both PBMs' claim files conformed into one record of fills (plan member ID,
class, date dispensed, days' supply, units, 11-digit NDC) with reversed claims removed and every fill priced at the
2026 schedule; the drug list, the price schedule and the rebate statement."""
import datetime as dt
import os

import pandas as pd

import world as W


def path(target, key):
    return os.path.join(target, W.FILES[key])


def ndc11(ndc10):
    """Orrin's 10-digit hyphenated NDC (5-3-2) to 11 digits."""
    a, b, c = ndc10.split("-")
    return a.zfill(5) + b.zfill(4) + c.zfill(2)


def drugs(target):
    return pd.read_csv(path(target, "drugs"), dtype=str, keep_default_na=False).set_index("ndc11")


def prices(target):
    from openpyxl import load_workbook
    ws = load_workbook(path(target, "prices"), data_only=True).active
    out = {}
    for r in ws.iter_rows(min_row=4, values_only=True):
        if r and r[0]:
            out[str(r[0])] = (float(r[2]), float(r[3]))
    return out


def crosswalk(target):
    x = pd.read_csv(path(target, "crosswalk"), dtype=str, keep_default_na=False)
    return (dict(zip(x["orrin_member_key"], x["plan_member_id"])),
            dict(zip(x["tallis_member_no"], x["plan_member_id"])))


def fills(target):
    """The conformed record: one row per fill that stands (reversed claims out), priced at the 2026 schedule."""
    to_plan_o, to_plan_t = crosswalk(target)
    dl = drugs(target)
    pr = prices(target)
    o = pd.read_csv(path(target, "orrin"), dtype=str, keep_default_na=False)
    rev = set(o.loc[o["line_type"] == "REVERSAL", "claim_no"])
    o = o[~o["claim_no"].isin(rev)]
    o = pd.DataFrame({"member": o["member_key"].map(to_plan_o), "ndc11": [ndc11(v) for v in o["ndc"]],
                      "date": pd.to_datetime(o["fill_date"]).dt.date, "days": o["days_supply"].astype(int),
                      "units": o["qty"].astype(float), "source": "Orrin"})
    t = pd.read_csv(path(target, "tallis"), dtype=str, keep_default_na=False)
    rev = set(t.loc[t["Status"] == "R", "ClaimID"])
    t = t[~t["ClaimID"].isin(rev)]
    t = pd.DataFrame({"member": t["MemberNo"].map(to_plan_t), "ndc11": t["NDC11"],
                      "date": pd.to_datetime(t["DateOfService"], format="%m/%d/%Y").dt.date,
                      "days": t["DaysSupply"].astype(int), "units": t["Quantity"].astype(float), "source": "Tallis"})
    f = pd.concat([o, t], ignore_index=True)
    f["cls"] = f["ndc11"].map(dl["class_code"])
    f["paid26"] = [round(u * pr[n][0], 2) + pr[n][1] for u, n in zip(f["units"], f["ndc11"])]
    return f.sort_values(["date", "member", "ndc11"], kind="stable").reset_index(drop=True)


def rebates(target):
    from openpyxl import load_workbook
    ws = load_workbook(path(target, "rebates"), data_only=True).active
    rows = []
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r and r[0]:
            rows.append(dict(invoice=r[0], cq=r[1], product=r[2], cls=r[3], channel=r[4], units=float(r[5]),
                             amount=float(r[6])))
    return pd.DataFrame(rows)


def rebates_2025(target, how="golden"):
    """Each class's rebates on its fills dispensed in calendar 2025. The statement's contract year runs February to
    January (its units by contract quarter tie to the claims' units only on that calendar), and each product's
    quarterly rebate stands on every channel line: the golden takes contract quarters 2025-Q1 to 2025-Q4 once each
    and January 2025's share of contract quarter 2024-Q4 at that quarter's rebate per unit ("golden"); the contract
    year read as the calendar year, each product-quarter once ("calendar"); every 2025 line summed ("lines"); the
    2025 invoices, each product-quarter once ("invoiced")."""
    rb = rebates(target)
    once = rb.drop_duplicates(["product", "cq"])
    if how == "lines":
        s = rb[rb["cq"].str.startswith("2025")].groupby("cls")["amount"].sum()
    elif how == "invoiced":
        s = once[once["invoice"].str.startswith("2025")].groupby("cls")["amount"].sum()
    elif how == "calendar":
        s = once[once["cq"].str.startswith("2025")].groupby("cls")["amount"].sum()
    else:
        s = once[once["cq"].str.startswith("2025")].groupby("cls")["amount"].sum()
        q4 = rb[rb["cq"] == "2024-Q4"].groupby(["product", "cls"]).agg(units=("units", "sum"), amount=("amount", "first"))
        f = fills(target)
        dl = drugs(target)
        jan = f[(f["date"] >= dt.date(2025, 1, 1)) & (f["date"] < dt.date(2025, 2, 1))]
        jan_units = jan.groupby(jan["ndc11"].map(dl["product_name"]))["units"].sum()
        s = s.copy()
        for (prod, cls), r in q4.iterrows():
            s[cls] = s.get(cls, 0.0) + r["amount"] / r["units"] * float(jan_units.get(prod, 0.0))
    return {c: float(s.get(c, 0.0)) for c in W.CANDIDATES}
