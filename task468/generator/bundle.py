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
            rows.append(dict(invoice=r[0], util=r[1], product=r[2], cls=r[3], channel=r[4], units=float(r[5]),
                             amount=float(r[6])))
    return pd.DataFrame(rows)


def rebates_2025(target, how="golden"):
    """Each class's rebates on 2025 utilization: the product's quarterly rebate once ("golden"), or every line summed
    ("lines")."""
    rb = rebates(target)
    rb = rb[rb["util"].str.startswith("2025")]
    if how == "lines":
        s = rb.groupby("cls")["amount"].sum()
    elif how == "invoiced":
        rb = rebates(target)
        rb = rb[rb["invoice"].str.startswith("2025")].drop_duplicates(["product", "util"])
        s = rb.groupby("cls")["amount"].sum()
    else:
        s = rb.drop_duplicates(["product", "util"]).groupby("cls")["amount"].sum()
    return {c: float(s.get(c, 0.0)) for c in W.CANDIDATES}
