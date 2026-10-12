"""The two asks, computed from the written pack only, with every stop the ask sheet names.

Ask A: for each closed campaign, how many listed deposits, and how much of their principal, were still on term
deposit with the society 30 days after maturity. Golden: a deposit reinvested on its own account at maturity and not
broken or closed in the 30 days after counts its principal; otherwise the maturity proceeds it paid into term deposits
opened with them that day, still open 30 days after, count at the amount transferred.

Ask B: the principal on term deposits and investment certificates together maturing in each month of January to March
2027, and how much of it is not on the list. Golden: the holdings view once per account (TD and KIC), plus the legacy
register's certificates maturing in the month that no migration batch moved; the list's principal taken off."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd

import calc as C
import world as W

DAYS = 30


def load(target):
    p = lambda f: os.path.join(target, f)
    A = {}
    A["lists"] = C.load_lists(target)
    A["events"] = pd.read_csv(p(W.F_EVENTS), dtype=str, keep_default_na=False)
    A["events"]["amount"] = A["events"]["amount"].astype(float)
    A["events"]["date"] = pd.to_datetime(A["events"]["event_date"])
    A["transfers"] = pd.read_csv(p(W.F_TRANSFERS), dtype=str, keep_default_na=False)
    A["transfers"]["amount"] = A["transfers"]["amount"].astype(float)
    A["transfers"]["date"] = pd.to_datetime(A["transfers"]["value_date"])
    A["hold"] = pd.read_csv(p(W.F_HOLDINGS), dtype=str, keep_default_na=False)
    A["hold"]["principal"] = A["hold"]["principal"].astype(float)
    A["kip"] = pd.read_csv(p(W.F_KIP), dtype=str, keep_default_na=False)
    A["kip"]["principal"] = A["kip"]["principal"].astype(float)
    A["batches"] = pd.read_csv(p(W.F_BATCHES), dtype=str, keep_default_na=False)
    A["fwd"] = pd.read_csv(p(W.F_LIST_FWD), dtype=str, keep_default_na=False)
    A["fwd"]["principal"] = A["fwd"]["principal"].astype(float)
    return A


# ---------------------------------------------------------------------------------------------------------------
def _index(A):
    if "_idx" in A:
        return A["_idx"]
    ev = A["events"]
    reinv, gone, opens, by_holder = set(), {}, {}, {}
    for a, cust, d, t, amt in zip(ev["account"], ev["customer_no"], ev["event_date"], ev["event_type"], ev["amount"]):
        d = dt.date.fromisoformat(d)
        if t == "REINVEST":
            reinv.add((a, d))
        elif t in ("BREAK", "CLOSE"):
            gone.setdefault(a, []).append(d)
        elif t == "OPEN":
            opens[a] = (d, float(amt))
            by_holder.setdefault(cust, []).append((d, a, float(amt)))
    out = {}
    tr = A["transfers"]
    for d, fa, ta, amt in zip(tr["value_date"], tr["from_account"], tr["to_account"], tr["amount"]):
        out.setdefault((fa, dt.date.fromisoformat(d)), []).append((ta, float(amt)))
    A["_idx"] = (reinv, gone, opens, by_holder, out)
    return A["_idx"]


def ask_a(A, mode="golden"):
    """mode: golden; own (the deposit's own account only); holder (own-account reinvestments plus any term deposit
    the holder opened within 30 days after maturity, at its whole principal); whole (proceeds followed into new term
    deposits but each counted at its whole opening principal); nobreak (the golden without the 30-day survival check);
    anyreinv (the golden with a reinvestment found anywhere on the account, not at this maturity); fullonly (the
    golden, a deposit counted only when all its principal stayed on term deposit); fullprin (the golden, a deposit that
    moved part of its principal counted at its whole principal); clause (the prompt's clause executed on the extracts:
    a deposit counts when any of its principal sits on a term deposit with the society 30 days after maturity, on its
    own account after a reinvestment or paid out of it in the 30 days into any account of the term deposit events
    extract, opened that day or not, and only that part counts)."""
    reinv, gone, opens, by_holder, out = _index(A)
    reinv_any = {a for a, _ in reinv}
    if mode == "clause":
        td_accts = set(A["events"]["account"])
    lists = A["lists"]
    res = {}
    for q in W.PAST:
        L = lists[lists["campaign"] == q]
        n, amt = 0, 0.0
        for a, cust, prin, mat in zip(L["account"], L["customer_no"], L["principal"], L["maturity"]):
            m = mat.date()
            lim = m + dt.timedelta(days=DAYS)

            def alive(acct):
                if mode == "nobreak":
                    return True
                return not any(m < d <= lim for d in gone.get(acct, []))
            hit = (a in reinv_any) if mode == "anyreinv" else ((a, m) in reinv)
            kept = prin if (hit and alive(a)) else 0.0
            if mode == "holder":
                for d, acct, am in by_holder.get(cust, []):
                    if m <= d <= lim and acct != a and alive(acct):
                        kept += am
            elif mode == "clause" and kept == 0.0:
                for k in range(DAYS + 1):
                    for to, am in out.get((a, m + dt.timedelta(days=k)), []):
                        if to in td_accts and to != a and alive(to):
                            kept += am
            elif mode in ("golden", "whole", "nobreak", "anyreinv", "fullonly", "fullprin") and kept == 0.0:
                for to, am in out.get((a, m), []):
                    if to in opens and opens[to][0] == m and alive(to):
                        kept += opens[to][1] if mode == "whole" else am
                if kept > 0 and abs(kept - prin) > 0.005:
                    if mode == "fullonly":
                        kept = 0.0
                    elif mode == "fullprin":
                        kept = prin
            if kept > 0:
                n += 1
                amt += kept
        res[q] = (n, round(amt, 2))
    return res


# ---------------------------------------------------------------------------------------------------------------
def ask_b(A, mode="golden"):
    """mode: golden; rows_both (holdings rows summed, legacy register added whole); dedup_both (once per account,
    legacy added whole); dedup_core (once per account, core only); rows_core (rows summed, core only); deferred
    (once per account, the legacy certificates added when a batch deferred them or no batch lists them)."""
    h = A["hold"].copy()
    h["mat"] = pd.to_datetime(h["maturity_date"])
    q1 = h[(h["mat"] >= "2027-01-01") & (h["mat"] <= "2027-03-31")]
    if mode in ("golden", "dedup_both", "dedup_core", "deferred"):
        q1 = q1.drop_duplicates("account")
    core = q1.groupby(q1["mat"].dt.month)["principal"].sum()
    k = A["kip"].copy()
    k["mat"] = pd.to_datetime(k["maturity_date"])
    k = k[(k["mat"] >= "2027-01-01") & (k["mat"] <= "2027-03-31")]
    moved = set(A["batches"].loc[A["batches"]["status"] == "MIGRATED", "cert_no"])
    if mode == "golden":
        k = k[~k["cert_no"].isin(moved)]
    elif mode == "deferred":
        held = set(A["batches"].loc[A["batches"]["status"] == "DEFERRED", "cert_no"])
        k = k[k["cert_no"].isin(held) | ~k["cert_no"].isin(set(A["batches"]["cert_no"]))]
    elif mode in ("dedup_core", "rows_core"):
        k = k.iloc[0:0]
    legacy = k.groupby(k["mat"].dt.month)["principal"].sum()
    f = A["fwd"].copy()
    f["mat"] = pd.to_datetime(f["maturity_date"])
    lst = f.groupby(f["mat"].dt.month)["principal"].sum()
    out = {}
    for m in (1, 2, 3):
        tot = float(core.get(m, 0.0) + legacy.get(m, 0.0))
        out[m] = (round(tot, 2), round(tot - float(lst.get(m, 0.0)), 2))
    return out


def all_stops(A):
    return dict(A={m: ask_a(A, m) for m in A_MODES}, B={m: ask_b(A, m) for m in B_MODES})


A_MODES = ("golden", "own", "holder", "whole", "nobreak", "anyreinv", "fullonly", "fullprin", "clause")
B_MODES = ("golden", "rows_both", "dedup_both", "dedup_core", "rows_core", "deferred")
