"""The two asks, computed from the written pack only, with every stop the ask sheet names.

Ask A: for each closed campaign, how much of the principal on its list was still on term deposit with the society 30
days after maturity, and from how many of its deposits. Golden: a deposit reinvested on its own account at maturity and
not broken or closed in the 30 days after keeps its principal; otherwise the maturity proceeds the payments system paid
for it that day (the settlement account's payments naming it in their narrative) into term deposits opened that day and
still open 30 days after count, at the amount paid.

Ask B: the principal on term deposits and investment certificates together maturing in each month of January to March
2027, and how much of the quarter's total is not on the list. Golden: the core holdings view once per account (TD and
KIC), plus the legacy register's certificates maturing in the quarter that are not in the core (not moved by a
migration batch, and matching no core certificate on issue date, maturity date, rate and term); the list's principal
taken off the quarter's total."""
from __future__ import annotations

import datetime as dt
import os
import re

import numpy as np
import pandas as pd

import calc as C
import world as W

DAYS = 30
REF = re.compile(r"(\d{2}-\d{4}-\d{7}-\d{3})")


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


def source_of(from_account, narrative):
    """The account a transfer pays out of: the settlement account's payments name it in the narrative."""
    m = REF.search(narrative)
    if from_account == W.SETTLEMENT and m:
        return W.norm_acct(m.group(1))
    return from_account


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
    out, direct = {}, {}
    tr = A["transfers"]
    for d, fa, ta, amt, nar in zip(tr["value_date"], tr["from_account"], tr["to_account"], tr["amount"],
                                   tr["narrative"]):
        d = dt.date.fromisoformat(d)
        out.setdefault((source_of(fa, nar), d), []).append((ta, float(amt)))
        direct.setdefault((fa, d), []).append((ta, float(amt)))
    A["_idx"] = (reinv, gone, opens, by_holder, out, direct)
    return A["_idx"]


def ask_a(A, mode="golden"):
    """mode: golden; own (the deposit's own account only); direct (own, plus transfers whose from_account is the
    deposit, the round-trip a payments view without the settlement account would show); holder (own-account
    reinvestments plus any term deposit the holder opened within 30 days after maturity, at its whole principal); whole
    (proceeds followed into new term deposits, each counted at its whole opening principal); nobreak (the golden without
    the 30-day survival check); anyreinv (the golden with a reinvestment found anywhere on the account, not at this
    maturity); fullonly (the golden, a deposit counted only when all its principal stayed on term deposit); fullprin (the
    golden, a deposit that moved part of its principal counted at its whole principal); literal (the prompt executed on
    the extracts: any of a deposit's principal on a term deposit with the society 30 days after maturity, on its own
    account after a reinvestment or paid for it in the 30 days into any account of the term deposit events extract,
    opened that day or not, and only that part)."""
    reinv, gone, opens, by_holder, out, direct = _index(A)
    reinv_any = {a for a, _ in reinv}
    if mode == "literal":
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
            elif mode == "literal" and kept == 0.0:
                for k in range(DAYS + 1):
                    for to, am in out.get((a, m + dt.timedelta(days=k)), []):
                        if to in td_accts and to != a and alive(to):
                            kept += am
            elif mode == "direct" and kept == 0.0:
                for to, am in direct.get((a, m), []):
                    if to in opens and opens[to][0] == m and alive(to):
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
    """Returns {1, 2, 3: principal maturing in the month, "off": the quarter's principal not on the list}.
    mode: golden (once per account, core TD and KIC, plus the register's certificates maturing in the month that are
    not in the core: not MIGRATED in the batches and matching no core certificate on issue date, maturity date, rate and
    term); rows_both (holdings rows summed, register added whole); dedup_both (once per account, register added whole);
    dedup_log (once per account, register less the batches' MIGRATED certificates); register_first (the core's term
    deposits once per account and every register certificate, the core's certificates dropped); dedup_core (once per
    account, core only); rows_core (rows summed, core only); deferred (once per account, the register's certificates a
    batch deferred or no batch lists)."""
    h = A["hold"].copy()
    h["mat"] = pd.to_datetime(h["maturity_date"])
    q1 = h[(h["mat"] >= "2027-01-01") & (h["mat"] <= "2027-03-31")]
    if mode not in ("rows_both", "rows_core"):
        q1 = q1.drop_duplicates("account")
    if mode == "register_first":
        q1 = q1[q1["product"] == "TD"]
    core = q1.groupby(q1["mat"].dt.month)["principal"].sum()
    k = A["kip"].copy()
    k["mat"] = pd.to_datetime(k["maturity_date"])
    k = k[(k["mat"] >= "2027-01-01") & (k["mat"] <= "2027-03-31")]
    moved = set(A["batches"].loc[A["batches"]["status"] == "MIGRATED", "cert_no"])
    if mode == "golden":
        hk = A["hold"][A["hold"]["product"] == "KIC"].drop_duplicates("account")
        key = set(zip(hk["start_date"], hk["maturity_date"], (hk["int_rate"].astype(float) * 100).round(2),
                      hk["term_months"].astype(int)))
        in_core = np.array([(i, m, round(float(rt), 2), int(t)) in key for i, m, rt, t in
                            zip(k["issue_date"], k["maturity_date"], k["rate"], k["term_months"])], dtype=bool)
        k = k[~k["cert_no"].isin(moved).values & ~in_core]
    elif mode == "dedup_log":
        k = k[~k["cert_no"].isin(moved)]
    elif mode == "deferred":
        held = set(A["batches"].loc[A["batches"]["status"] == "DEFERRED", "cert_no"])
        k = k[k["cert_no"].isin(held) | ~k["cert_no"].isin(set(A["batches"]["cert_no"]))]
    elif mode in ("dedup_core", "rows_core"):
        k = k.iloc[0:0]
    legacy = k.groupby(k["mat"].dt.month)["principal"].sum()
    f = A["fwd"].copy()
    f["mat"] = pd.to_datetime(f["maturity_date"])
    out = {}
    for m in (1, 2, 3):
        out[m] = round(float(core.get(m, 0.0) + legacy.get(m, 0.0)), 2)
    out["off"] = round(sum(out[m] for m in (1, 2, 3)) - float(f["principal"].sum()), 2)
    return out


def all_stops(A):
    return dict(A={m: ask_a(A, m) for m in A_MODES}, B={m: ask_b(A, m) for m in B_MODES})


A_MODES = ("golden", "own", "direct", "holder", "whole", "nobreak", "anyreinv", "fullonly", "fullprin", "literal")
B_MODES = ("golden", "rows_both", "dedup_both", "dedup_log", "register_first", "dedup_core", "rows_core", "deferred")
