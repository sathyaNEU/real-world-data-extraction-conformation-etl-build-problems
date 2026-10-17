"""The golden path from the shipped files alone: each member council's residents who visited and its 2027-28 levy,
the three asks, and the wrong paths the checks and the design note quote. Every figure here is computed from
target/."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd

import common as K


def f(target, key):
    return os.path.join(target, K.FILES[key])


# ---------------------------------------------------------------------------------------------- the survey
def survey(target):
    """Both waves stacked on one key with the contractor's weights: council code, 12-month visit count, weight."""
    w1 = pd.read_excel(f(target, "wave1"), sheet_name="Interviews")
    w2 = pd.read_csv(f(target, "wave2"), dtype=str)
    wt = pd.read_csv(f(target, "weights"), dtype={"case_id": str})
    a = pd.DataFrame({"case": "1-" + w1["Interview No"].str.split("-").str[-1], "code": w1["Home area"],
                      "visits": w1["Visits to Authority parks, last 12 months (incl. today)"].astype(int),
                      "park": w1["Park"].map({v: k for k, v in K.PARK_NAME.items()}),
                      "date": pd.to_datetime(w1["Interview date"]).dt.date})
    b = pd.DataFrame({"case": "2-" + w2["case_ref"].str.split("/").str[-1], "code": w2["home_area_code"],
                      "visits": w2["q9_visits_12m"].astype(int), "park": w2["site_code"],
                      "date": pd.to_datetime(w2["int_date"], format="%d/%m/%Y").dt.date})
    d = pd.concat([a, b], ignore_index=True).merge(wt, left_on="case", right_on="case_id", validate="one_to_one")
    return d


def residents(d, how="golden"):
    """Each member council's estimated residents who visited. golden: each interview's weight over its own visit
    count. visits: the weights summed (adult visits). mean: visits over the council's weighted average visit
    count. raw: interviews counted. unweighted: each interview's inverse visit count, no weight."""
    m = d[d["code"].isin(K.CODES)]
    if how == "golden":
        s = (m["weight"] / m["visits"]).groupby(m["code"]).sum()
    elif how == "visits":
        s = m.groupby("code")["weight"].sum()
    elif how == "mean":
        v = m.groupby("code")["weight"].sum()
        avg = (m["weight"] * m["visits"]).groupby(m["code"]).sum() / v
        s = v / avg
    elif how == "raw":
        s = m.groupby("code").size().astype(float)
    elif how == "unweighted":
        s = (1.0 / m["visits"]).groupby(m["code"]).sum()
    else:
        raise ValueError(how)
    return {c: float(s.get(c, 0.0)) for c in K.CODES}


def levy(N, total=K.LEVY_2027):
    t = sum(N.values())
    return {c: total * N[c] / t for c in K.CODES}


def rounded(L):
    return {c: int(np.floor(L[c] + .5)) for c in K.CODES}


def outside(d):
    m = d[d["code"] == "OUT"]
    return float((m["weight"] / m["visits"]).sum())


# ---------------------------------------------------------------------------------------------- Ask A
def local_date(ts):
    """A UTC timestamp's date on the UK clock."""
    t = pd.to_datetime(ts, utc=True).dt.tz_convert("Europe/London")
    return t.dt.date


def machines(target, dedupe=True, sites="history"):
    """Machine payments with their park: replays dropped on the machine's own ticket number, and each machine placed
    where its takings show it stood (its charges against each park's tariff), not where the register has it now."""
    t = pd.read_csv(f(target, "machines"), dtype={"ticket_no": int})
    if dedupe:
        t = t.drop_duplicates(["machine_id", "ticket_no"])
    t["date"] = local_date(t["paid_at_utc"])
    reg = pd.read_csv(f(target, "assets"))
    site = dict(zip(reg["asset_id"], reg["site_code"]))
    t["park"] = t["machine_id"].map(site).map(K.CP_PARK)
    if sites == "history":
        tar = pd.read_excel(f(target, "tariffs"), sheet_name="Tariffs 2025-26")
        tar["park"] = tar["Car park code"].map(K.CP_PARK)
        charges = {p: set(np.round(tar.loc[tar["park"] == p, "Charge (GBP)"].astype(float), 2)) for p in K.CHARGING}
        g = t.groupby(["machine_id", "date"])["amount_gbp"].agg(lambda x: set(np.round(x.astype(float), 2)))
        fix = {}
        for (mid, d), amounts in g.items():
            own = K.CP_PARK[site[mid]]
            if not amounts <= charges[own]:
                fits = [p for p in K.CHARGING if amounts <= charges[p]]
                assert len(fits) == 1, (mid, d, amounts, fits)
                fix[(mid, d)] = fits[0]
        # a machine stands in one place for a run of days: every day up to its last misfit day was spent there
        for mid in sorted({k[0] for k in fix}):
            days = sorted(d for (m_, d) in fix if m_ == mid)
            parks = {fix[(mid, d)] for d in days}
            assert len(parks) == 1, (mid, parks)
            sel = (t["machine_id"] == mid) & (t["date"] <= days[-1])
            t.loc[sel, "park"] = parks.pop()
    return t


def app(target):
    a = pd.read_excel(f(target, "app"), sheet_name="Statement lines")
    a["cp"] = a["Location code"].str.replace("LOC-", "").str.replace(r"^([A-Z]{2})", r"\1-", regex=True)
    a["park"] = a["cp"].map(K.CP_PARK)
    return a


def parking_parts(target, vat_on_app=False, dedupe=True, sites="history"):
    """What parkers paid at each charging park for 2025-26 parking, net of VAT, by channel: machine takings without
    their VAT, and the app's parking income as the provider states it (already without VAT)."""
    t = machines(target, dedupe, sites)
    a = app(target)
    mac = t.groupby("park")["amount_gbp"].sum() / (1 + K.VAT)
    ap = a.groupby("park")["Parking income (GBP)"].sum()
    if vat_on_app:
        ap = ap / (1 + K.VAT)
    return {p: (float(mac.get(p, 0)), float(ap.get(p, 0))) for p in K.CHARGING}


def parking_income(target, **kw):
    return {p: m + a for p, (m, a) in parking_parts(target, **kw).items()}


# ---------------------------------------------------------------------------------------------- Ask B
def levy_collection(target, date_col="Value date", split="advice"):
    """Each council's 2025-26 levy, what it had paid toward it by 31 March 2026 and what it still owed that day.
    A receipt is a payment toward the levy when its reference quotes a 2025-26 levy invoice; it counts when the bank
    credited it (its value date); a transfer covering two councils' invoices is split by the payer's remittance
    advice. split="reference" credits a transfer to the invoice it quotes; split="even" halves it."""
    inv = pd.read_csv(f(target, "invoices"), dtype=str)
    inv["amount"] = inv["amount_gbp"].astype(float)
    owner = dict(zip(inv["invoice_no"], inv["customer_code"]))
    levy_ = inv.groupby("customer_code")["amount"].sum()
    rc = pd.read_csv(f(target, "receipts"), dtype=str)
    rc["amount"] = rc["Amount"].astype(float)
    rc["when"] = pd.to_datetime(rc[date_col], format="%d/%m/%Y").dt.date
    rc["value"] = pd.to_datetime(rc["Value date"], format="%d/%m/%Y").dt.date
    rc["inv"] = rc["Reference"].str.extract(r"(INV2[56]-\d{4})")[0]
    lv = rc[rc["inv"].isin(owner) & (rc["when"] <= dt.date(2026, 3, 31))]
    ra = pd.read_csv(f(target, "remittances"), dtype=str)
    ra["amount"] = ra["amount_gbp"].astype(float)
    ra["date"] = pd.to_datetime(ra["payment_date"]).dt.date
    paid = {c: 0.0 for c in K.CODES}
    for _, r in lv.iterrows():
        cov = ra[(ra["date"] == r["value"]) & (ra["invoice_no"] == r["inv"])]
        advice = ra[ra["advice_ref"].isin(cov["advice_ref"])]
        joint = len(advice) > 1 and abs(advice["amount"].sum() - r["amount"]) < .005
        if joint and split == "advice":
            for _, x in advice.iterrows():
                paid[owner[x["invoice_no"]]] += x["amount"]
        elif joint and split == "even":
            for _, x in advice.iterrows():
                paid[owner[x["invoice_no"]]] += r["amount"] / len(advice)
        else:
            paid[owner[r["inv"]]] += r["amount"]
    return {c: dict(levy=float(levy_[c]), paid=round(paid[c], 2), owed=round(float(levy_[c]) - paid[c], 2))
            for c in K.CODES}


# ---------------------------------------------------------------------------------------------- Ask C
def vehicles(target, halve=True, history=True, once=True):
    """Vehicles that entered each charging park's car parks: each counter's hours placed at the car park it stood
    at in that hour, the Water Park's replacement loop's passes halved (it counts every vehicle in and out), and an
    entrance counted once while its old and new counters ran side by side."""
    c = pd.read_csv(f(target, "counts"))
    c["hour"] = pd.to_datetime(c["hour_start_utc"])
    reg = pd.read_csv(f(target, "assets"))
    reg = reg[reg["asset_type"] == "Vehicle counter"]
    site = dict(zip(reg["asset_id"], reg["site_code"]))
    model = dict(zip(reg["asset_id"], reg["model"]))
    installed = {r.asset_id: pd.Timestamp(r.installed) for r in reg.itertuples()}
    removed = {r.asset_id: pd.Timestamp(r.removed) for r in reg.itertuples() if isinstance(r.removed, str)}
    first = c.groupby("counter_id")["hour"].min()
    c["cp"] = c["counter_id"].map(site)
    if history:
        # two counters recording at one car park before one of them was removed: the other stood where a counter
        # was installed on that day, until that counter's first hour
        for x in site:
            for y, ry in removed.items():
                if y == x or site[y] != site[x] or not installed[x] < ry or not first[x] < ry:
                    continue
                took = [z for z in site if installed[z] == ry and z not in (x, y) and site[z] != site[x]]
                if took:
                    c.loc[(c["counter_id"] == x) & (c["hour"] < first[took[0]]), "cp"] = site[took[0]]
    c["vehicles"] = c["vehicles"].astype(float)
    if halve:
        c.loc[c["counter_id"].map(model) == "BX-2", "vehicles"] = c["vehicles"] / 2
    if once:
        newer = c.groupby(["cp", "hour"])["counter_id"].transform("max")
        c = c[c["counter_id"] == newer]
    c["park"] = c["cp"].map(K.CP_PARK)
    s = c.groupby("park")["vehicles"].sum()
    return {p: float(s.get(p, 0)) for p in K.CHARGING}


# ---------------------------------------------------------------------------------------------- everything
def compute(target):
    d = survey(target)
    N = residents(d, "golden")
    L = levy(N)
    out = dict(survey=d, N=N, levy=L, levy_r=rounded(L), outside=outside(d))
    out["rungs"] = {}
    for how in ("raw", "visits", "mean", "unweighted"):
        n = residents(d, how)
        out["rungs"][how] = dict(N=n, levy=levy(n))
    out["valley"] = {k: 100 * sum(v["levy"][c] for c in K.VALLEY) / K.LEVY_2027 for k, v in out["rungs"].items()}
    out["valley"]["golden"] = 100 * sum(L[c] for c in K.VALLEY) / K.LEVY_2027
    out["parts"] = parking_parts(target)
    out["income"] = {p: m + a for p, (m, a) in out["parts"].items()}
    out["collection"] = levy_collection(target)
    out["vehicles"] = vehicles(target)
    return out
