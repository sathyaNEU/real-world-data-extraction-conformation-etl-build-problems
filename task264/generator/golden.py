"""The golden path from the shipped files alone: each member council's residents who visited and its 2027-28 levy,
the three asks, and the wrong paths the checks and the design note quote. Every figure here is computed from
target/."""
from __future__ import annotations

import collections
import datetime as dt
import itertools
import os
import re

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
                      "park": w1["Park"].map({v: k for k, v in K.PARK_NAME.items()}),
                      "date": pd.to_datetime(w1["Interview date"]).dt.date})
    b = pd.DataFrame({"case": "2-" + w2["case_ref"].str.split("/").str[-1], "code": w2["home_area_code"],
                      "park": w2["site_code"], "date": pd.to_datetime(w2["int_date"], format="%d/%m/%Y").dt.date})
    for q in K.PARK_CODES:
        a["v_" + q] = w1["Visits, last 12 months (incl. today): %s" % K.PARK_NAME[q]].astype(int)
        b["v_" + q] = w2["q9_%s" % q.lower()].astype(int)
    d = pd.concat([a, b], ignore_index=True).merge(wt, left_on="case", right_on="case_id", validate="one_to_one")
    d["visits"] = d[["v_" + q for q in K.PARK_CODES]].sum(axis=1)
    d["here"] = [int(r["v_" + r["park"]]) for _, r in d.iterrows()]
    return d


def residents(d, how="golden"):
    """Each member council's estimated residents who visited. golden: each interview's weight over its own visit
    count (its visits to the six parks added). here: each interview's weight over its visits to the park it was
    interviewed at. visits: the weights summed (adult visits). mean: visits over the council's weighted average visit
    count. raw: interviews counted. unweighted: each interview's inverse visit count, no weight."""
    m = d[d["code"].isin(K.CODES)]
    if how == "golden":
        s = (m["weight"] / m["visits"]).groupby(m["code"]).sum()
    elif how == "here":
        s = (m["weight"] / m["here"]).groupby(m["code"]).sum()
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
def payers(remitter, names):
    """The member councils a bank remitter is: each council whose name's first word the remitter carries."""
    return [c for c, n in names.items() if n.split()[0].upper() in remitter.upper()]


def levy_timeliness(target, dates="bank", lines="receipt", yearend="payer"):
    """Each council's 2025-26 levy paid by each instalment's due date (on time) and paid after its due date but by 31
    March 2026 (late). A receipt is dated by the day the bank credited it (dates="bank": the bank's report, matched on
    the receipt's reference and amount) or by the day the finance system posted it (dates="posted"). The cash book
    prints a receipt on one line for each invoice it pays with the receipt's amount on every line: lines="receipt"
    takes the receipt once and pays each of its invoices in full (one invoice takes the whole receipt); lines="line"
    adds up the lines. The cash book's year ends on 31 March by posting date, so credits of 31 March are in the bank's
    report only: yearend="payer" takes each against the paying council's open invoices that make up its amount,
    "reference" against the invoice its reference quotes, "none" leaves them out."""
    inv = pd.read_csv(f(target, "invoices"), dtype=str)
    inv["amount"] = inv["amount_gbp"].astype(float)
    inv["due"] = pd.to_datetime(inv["due_date"]).dt.date
    owner = dict(zip(inv["invoice_no"], inv["customer_code"]))
    amount = dict(zip(inv["invoice_no"], inv["amount"]))
    levy = inv[inv["description"].str.startswith("Levy 2025-26")]
    due = dict(zip(levy["invoice_no"], levy["due"]))
    names = dict(zip(inv["customer_code"], inv["customer"]))
    cb = pd.read_csv(f(target, "cashbook"), dtype=str)
    cb["amount"] = cb["Amount"].astype(float)
    cb["posted"] = pd.to_datetime(cb["Posting date"], format="%d/%m/%Y").dt.date
    bk = pd.read_csv(f(target, "bank"), dtype=str)
    bk["amount"] = bk["Amount"].astype(float)
    bk["value"] = pd.to_datetime(bk["Value date"], format="%d/%m/%Y").dt.date
    credit = {}
    for k, r in bk.iterrows():
        credit.setdefault((r["Reference"], round(r["amount"], 2)), []).append((r["value"], k))
    used = set()
    paid = []                                   # (invoice, day, amount)
    for _rno, g in cb.groupby("Receipt no", sort=False):
        narr, posted, amt = g["Narrative"].iloc[0], g["posted"].iloc[0], round(g["amount"].iloc[0], 2)
        # the receipt's credit: the bank's credit with its reference and amount, the latest on or before the posting
        cand = [x for x in credit.get((narr, amt), []) if x[0] <= posted]
        value = max(cand)[0] if cand else None
        if cand:
            used.add(max(cand)[1])
        day = value if dates == "bank" else posted
        nos = [n for n in g["Invoice"] if isinstance(n, str) and n in owner]
        if lines == "line":
            paid += [(r["Invoice"], day, r["amount"]) for _, r in g.iterrows() if r["Invoice"] in owner]
        elif len(nos) == 1:
            paid.append((nos[0], day, amt))
        else:
            paid += [(n, day, amount[n]) for n in nos]
    if yearend != "none":
        for k, r in bk.iterrows():
            if k in used or not K.YEAR0 <= r["value"] <= K.YEAR1:
                continue
            who = payers(r["Remitter"], names)
            if not who:
                continue
            if yearend == "reference":
                m = re.search(r"INV2[56]-\d{4}", r["Reference"])
                if m and m.group(0) in owner:
                    paid.append((m.group(0), r["value"], r["amount"]))
                continue
            got = collections.defaultdict(float)
            for n, _d, a in paid:
                got[n] += a
            open_ = [n for n in owner if owner[n] in who and amount[n] - got[n] > .005]
            fits = [s for k_ in (1, 2, 3) for s in itertools.combinations(open_, k_)
                    if abs(sum(amount[n] - got[n] for n in s) - r["amount"]) < .005]
            if len(fits) == 1:
                paid += [(n, r["value"], amount[n] - got[n]) for n in fits[0]]
    out = {c: dict(on_time=0.0, late=0.0) for c in K.CODES}
    for no, day, amt in paid:
        if no not in due or day is None or day > K.YEAR1:
            continue
        out[owner[no]]["on_time" if day <= due[no] else "late"] += amt
    levy_ = levy.groupby("customer_code")["amount"].sum()
    return {c: dict({k: round(v, 2) for k, v in out[c].items()}, levy=float(levy_[c]),
                    unpaid=round(float(levy_[c]) - out[c]["on_time"] - out[c]["late"], 2)) for c in K.CODES}


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
    for how in ("raw", "visits", "mean", "unweighted", "here"):
        n = residents(d, how)
        out["rungs"][how] = dict(N=n, levy=levy(n))
    out["valley"] = {k: 100 * sum(v["levy"][c] for c in K.VALLEY) / K.LEVY_2027 for k, v in out["rungs"].items()}
    out["valley"]["golden"] = 100 * sum(L[c] for c in K.VALLEY) / K.LEVY_2027
    out["parts"] = parking_parts(target)
    out["income"] = {p: m + a for p, (m, a) in out["parts"].items()}
    out["collection"] = levy_timeliness(target)
    out["vehicles"] = vehicles(target)
    return out
