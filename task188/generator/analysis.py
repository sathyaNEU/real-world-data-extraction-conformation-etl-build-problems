"""Every graded figure and every rung, computed from the shipped files under target/ alone.

golden.py and checks.py both call this module; verify.py recomputes the same figures on its own code path.
"""
import datetime as dt
import os
import zipfile

import numpy as np
import openpyxl
import pandas as pd

import common as C
import pack

CASH_CODES = ("DEP", "ATMD", "NDEP", "COIN")
CARD_PREFIX = ("CASCADIA MERCH DEP", "NORTHGATE PAY STLMT")
PLATFORM_PREFIX = ("DASHDROP CANADA PAYOUT", "PLATEPASS REMIT")
THRESHOLD_CAD = 100_000
TIMES_PRODUCED = 2.0
LCTR_CASH = 10_000


def load(target):
    p = pd.read_csv(os.path.join(target, pack.P_POSTINGS), dtype={"account_number": str, "transit": str,
                                                                   "terminal_id": str, "cheque_items": str})
    p["effective_date"] = pd.to_datetime(p["effective_date"])
    p["posted_at_utc"] = pd.to_datetime(p["posted_at_utc"].str.replace("Z", "", regex=False))
    for c in ("debit", "credit", "cash_portion"):
        p[c] = pd.to_numeric(p[c], errors="coerce")
    wb = openpyxl.load_workbook(os.path.join(target, pack.P_REGISTER), read_only=True)
    mem = pd.DataFrame(list(wb["Members"].iter_rows(min_row=2, values_only=True)),
                       columns=[c.value for c in next(wb["Members"].iter_rows(max_row=1))])
    acc = pd.DataFrame(list(wb["Accounts"].iter_rows(min_row=2, values_only=True)),
                       columns=[c.value for c in next(wb["Accounts"].iter_rows(max_row=1))])
    p["member_number"] = p["account_number"].map(dict(zip(acc.account_number, acc.member_number)))
    return p, mem, acc


def year_rows(p):
    return p[p.effective_date.dt.year == C.YEAR]


def member_year(p, mem):
    y = year_rows(p)
    cash_rows = y[y.transaction_code.isin(CASH_CODES)]
    cash = cash_rows.groupby("member_number").cash_portion.sum()
    desc = y.description.fillna("")
    card = y[desc.str.startswith(CARD_PREFIX)].groupby("member_number").credit.sum()
    plat = y[desc.str.startswith(PLATFORM_PREFIX)].groupby("member_number").credit.sum()
    credits = y.groupby("member_number").credit.sum()
    df = pd.DataFrame({"cash": cash, "card": card, "platform": plat, "credits": credits}).reindex(mem.member_number).fillna(0.0)
    df["trade"] = list(mem.set_index("member_number").loc[df.index, "business_type_code"])
    df["name"] = list(mem.set_index("member_number").loc[df.index, "operating_name"])
    df["noncash"] = df.credits - df.cash
    return df


def produced(df, flow, how="median"):
    """The cash each member's trade produced, read from a flow through its trade's relation of cash to it."""
    r = df.cash / flow
    if how == "median":
        return r.groupby(df.trade).transform("median") * flow
    if how == "totals":
        return df.trade.map(df.cash.groupby(df.trade).sum() / flow.groupby(df.trade).sum()) * flow
    if how == "mean":
        return r.groupby(df.trade).transform("mean") * flow
    if how == "trim":
        return r.groupby(df.trade).transform(lambda x: x[x <= x.quantile(0.9)].median()) * flow
    if how == "loo":
        out = pd.Series(index=df.index, dtype=float)
        for t, sub in r.groupby(df.trade):
            for i in sub.index:
                out[i] = sub.drop(i).median()
        return out * flow
    if how == "ols_origin":
        out = pd.Series(index=df.index, dtype=float)
        for t, sub in df.groupby("trade"):
            x, yv = flow[sub.index], df.cash[sub.index]
            out[sub.index] = (x * yv).sum() / (x * x).sum() * x
        return out
    if how == "loglog":
        out = pd.Series(index=df.index, dtype=float)
        for t, sub in df.groupby("trade"):
            x = np.log(flow[sub.index]); yv = np.log(df.cash[sub.index])
            b, a = np.polyfit(x, yv, 1)
            res = yv - (a + b * x)
            k = res <= res.quantile(0.9)
            b, a = np.polyfit(x[k], yv[k], 1)
            out[sub.index] = np.exp(a + b * x)
        return out
    if how == "trimmed_totals":
        out = pd.Series(index=df.index, dtype=float)
        for t, sub in df.groupby("trade"):
            rr = r[sub.index]
            keep = rr <= rr.quantile(0.9)
            out[sub.index] = sub.cash[keep].sum() / flow[sub.index][keep].sum() * flow[sub.index]
        return out
    raise ValueError(how)


FAMILY = ("median", "totals", "trim", "loo", "ols_origin", "trimmed_totals", "loglog", "mean")


def designate(df, expected):
    exc = df.cash - expected
    keep = (exc >= THRESHOLD_CAD) & (exc >= TIMES_PRODUCED * expected)
    return list(exc[keep].sort_values(ascending=False).index), exc


def golden_call(df):
    exp = produced(df, df.card, "median")
    ref, exc = designate(df, exp)
    rest = exc.drop(ref)
    near = rest.idxmax()
    return {"referred": ref, "expected": exp, "excess": exc, "near": near}


def quarterly_cash(p, members):
    y = year_rows(p)
    y = y[y.transaction_code.isin(CASH_CODES) & y.member_number.isin(members)]
    q = y.effective_date.dt.quarter
    return y.groupby([y.member_number, q]).cash_portion.sum()


# --- the large cash transaction ask ------------------------------------------------------------------------

def lctr_required(p, mem, how="window", quarter_clock="pacific"):
    """Reports the segment's cash required in 2026, by quarter.

    window (the programme's s.6.2): a window opens at a member's first cash receipt and runs 24 hours across
    every account and channel, a night deposit received when its bag is counted (its posting time); a
    window whose cash reaches CAD 10,000 needs one report, in the quarter it opens on Pacific time.
    The other handlings are the readings a response may take: account_window (windows per account),
    member_bizday and account_bizday (one report per member or account and business date),
    member_localday (per member and Pacific calendar day of receipt)."""
    rows = p[p.transaction_code.isin(CASH_CODES) & (p.cash_portion > 0) & p.member_number.isin(mem.member_number)]
    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    out = []
    if how in ("window", "account_window"):
        key = "member_number" if how == "window" else "account_number"
        rows = rows.sort_values([key, "posted_at_utc", "posting_id"])
        windows = []
        for m, sub in rows.groupby(key):
            start, total = None, 0.0
            for t, cash in zip(sub.posted_at_utc, sub.cash_portion):
                t = t.to_pydatetime()
                if start is None or t >= start + dt.timedelta(hours=24):
                    if start is not None and total >= LCTR_CASH:
                        windows.append((m, start, total))
                    start, total = t, 0.0
                total += cash
            if start is not None and total >= LCTR_CASH:
                windows.append((m, start, total))
        for m, start, total in windows:
            loc = C.utc_to_local(start) if quarter_clock == "pacific" else start
            if loc.year == C.YEAR:
                counts[C.quarter_of(loc.date())] += 1
                out.append((m, start, total))
        return counts, out
    if how in ("member_bizday", "account_bizday"):
        key = "member_number" if how == "member_bizday" else "account_number"
        g = rows.groupby([key, rows.effective_date.dt.date]).cash_portion.sum()
        for (m, d), v in g.items():
            if v >= LCTR_CASH and d.year == C.YEAR:
                counts[C.quarter_of(d)] += 1
                out.append((m, d, v))
        return counts, out
    if how == "member_localday":
        ld = [C.utc_to_local(t.to_pydatetime()).date() for t in rows.posted_at_utc]
        g = rows.assign(ld=ld).groupby(["member_number", "ld"]).cash_portion.sum()
        for (m, d), v in g.items():
            if v >= LCTR_CASH and d.year == C.YEAR:
                counts[C.quarter_of(d)] += 1
                out.append((m, d, v))
        return counts, out
    raise ValueError(how)


def receipt_day(p):
    """(account, business date) -> the Pacific day the first cash credited to the account that business date was
    received: a deposit ATM's cash after 18:00 or on a non-business day posts to the next business date, and the
    report the old module made carries that business date as its transaction date."""
    rows = p[p.transaction_code.isin(CASH_CODES) & (p.cash_portion > 0)]
    first = rows.groupby([rows.account_number, rows.effective_date.dt.date]).posted_at_utc.min()
    return {k: C.utc_to_local(v.to_pydatetime()).date() for k, v in first.items()}


def lctr_filed(target, mem, acc=None, p=None, key="account", late_from="receipt", by="transaction", dedupe=True):
    """Reports filed for the segment's cash, by the quarter of the transaction date each reports (programme s.6.2),
    and how many of them went in more than 15 calendar days after the day the first cash they report was
    received. A report is the segment's when the account it reports is a segment account: a report keyed at a
    branch carries the conductor's own membership in the member field. Each reference is one report (a re-sent
    Original is the same report, a Correction amends it).

    The rival handlings: key=member (the member field), late_from=transaction (the log's transaction date),
    by=submitted (the quarter it went in), dedupe=False (every Original row)."""
    lg = pd.read_csv(os.path.join(target, pack.P_LCTR), dtype={"report_reference": str, "account_number": str})
    if key == "account":
        lg = lg[lg.account_number.isin(set(acc.account_number))]
    else:
        lg = lg[lg.member_number.isin(mem.member_number)]
    lg = lg[lg.report_version == "Original"]
    if dedupe:
        lg = lg.drop_duplicates(subset=["report_reference"])
    lg = lg.assign(transaction_date=pd.to_datetime(lg.transaction_date), submitted_date=pd.to_datetime(lg.submitted_date))
    col = lg.transaction_date if by == "transaction" else lg.submitted_date
    keep = col.dt.year == C.YEAR
    lg, col = lg[keep], col[keep]
    q = col.dt.quarter
    filed = lg.groupby(q).size().reindex([1, 2, 3, 4]).fillna(0).astype(int).to_dict()
    if late_from == "receipt":
        rd = receipt_day(p)
        start = pd.to_datetime(pd.Series([rd.get((a, d.date()), d.date()) for a, d in zip(lg.account_number, lg.transaction_date)],
                                         index=lg.index))
    else:
        start = lg.transaction_date
    late = lg[(lg.submitted_date - start).dt.days > 15]
    late_q = late.groupby(q[late.index]).size().reindex([1, 2, 3, 4]).fillna(0).astype(int).to_dict()
    return filed, late_q


# --- the branch cash ask ----------------------------------------------------------------------------------

def branch_cash(target, p, night="manifest", atm="asof", counter="transit", mem=None, acc=None):
    """Each branch's 2026 segment cash by channel, on the business date of each credit.

    counter: the transit the teller deposit posted at. atm: the site the terminal stood at on the day of the
    deposit (the directory lists a terminal once per installation). night: bags counted at a branch post at
    its transit; a bag counted at Regional Cash Services is placed at the depository the armoured car took it
    from that morning (its pickup manifest, bag and date). The other handlings are a response's readings:
    night=bag_register (the bag's issuing transit), home (the member's home transit), domicile (the account's
    transit), drop (cash-centre bags left out); atm=last or first (one row per terminal kept); counter=home."""
    wb = openpyxl.load_workbook(os.path.join(target, pack.P_DIR), read_only=True)
    br = list(wb["Branches"].iter_rows(min_row=2, values_only=True))
    atms = list(wb["ATMs"].iter_rows(min_row=2, values_only=True))
    depos = list(wb["Night depositories"].iter_rows(min_row=2, values_only=True))
    branches = [r[0] for r in br if r[6] != "n/a"]
    term = {}
    for tid, loc, tr, inst, rem, takes in atms:
        term.setdefault(str(tid), []).append((_day(inst), str(tr)))
    for v in term.values():
        v.sort()
    depo = {r[0]: r[1] for r in depos}

    def site(tid, day):
        rows = term[str(tid)]
        if atm == "last":
            return rows[-1][1]
        if atm == "first":
            return rows[0][1]
        best = None
        for inst, tr in rows:
            if inst <= day:
                best = tr
        return best
    cit = pd.read_csv(os.path.join(target, pack.P_CIT), dtype={"depository_id": str})
    cit_map = {(int(b), d): depo[x] for b, d, x in zip(cit.bag_number, cit.pickup_date, cit.depository_id)}
    bagreg = pd.read_csv(os.path.join(target, pack.P_BAGS), dtype={"issuing_transit": str})
    bag_tr = dict(zip(bagreg.bag_number, bagreg.issuing_transit))
    if mem is not None:
        home = dict(zip(mem.member_number, mem.home_transit.astype(str)))
    y = year_rows(p)
    y = y[y.transaction_code.isin(CASH_CODES) & y.member_number.notna()]
    out = {b: {"counter": 0.0, "atm": 0.0, "night": 0.0} for b in branches}
    local_day = [C.utc_to_local(t.to_pydatetime()).date() for t in y.posted_at_utc]
    for code, ch, tr, tid, desc, cash, eff, ld, mn, an in zip(
            y.transaction_code, y.channel, y.transit, y.terminal_id, y.description, y.cash_portion,
            y.effective_date, local_day, y.member_number, y.account_number):
        if ch == "TELLER":
            b = str(tr) if counter == "transit" else home[mn]
            out.setdefault(b, {"counter": 0.0, "atm": 0.0, "night": 0.0})["counter"] += cash
        elif ch == "ATM":
            out[site(tid, ld)]["atm"] += cash
        elif ch == "NIGHT":
            if str(tr) in out:
                out[str(tr)]["night"] += cash
                continue
            bag = int(desc.split("BAG ")[1].split()[0])
            if night == "manifest":
                b = cit_map[(bag, eff.date().isoformat())]
            elif night == "bag_register":
                b = bag_tr[bag]
            elif night == "home":
                b = home[mn]
            elif night == "domicile":
                b = an.split("-")[0]
            elif night == "drop":
                continue
            else:
                raise ValueError(night)
            out.setdefault(b, {"counter": 0.0, "atm": 0.0, "night": 0.0})["night"] += cash
    return {b: out[b] for b in branches}


def _day(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return dt.date.fromisoformat(str(v)[:10])


def read_cdd(target):
    c = pd.read_csv(os.path.join(target, pack.P_CDD))
    return c.set_index("member_number")
