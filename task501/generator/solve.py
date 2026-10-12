"""Computes every graded figure of task501 from the shipped files alone (pandas): the main call with its ladder and
golden family, and the ask with its stops. The independent verifier (verify.py) shares no code with this file."""
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
PLAN_DATE = date(2026, 12, 31)
RESERVE = 150_000_000.0
MARGIN = 0.10
MENU = list(range(50, 401, 25))
COMMIT_FEE, ARRANGE_FEE = 0.0030, 0.0015
STRATS = ("BO", "GR", "PC", "IN")
QUARTERS = (1, 2, 3, 4)


def mi(d):
    return d.year * 12 + d.month - 1


PLAN_I = mi(PLAN_DATE)
WIN = list(range(PLAN_I + 1, PLAN_I + 13))


class Pack:
    def __init__(self, root=T):
        self.root = root
        lg = pd.read_csv(os.path.join(root, "kapitalabrufe_ausschuettungen_2015-2026.csv"), dtype=str, keep_default_na=False)
        for c in ("notice_date", "value_date"):
            lg[c] = pd.to_datetime(lg[c]).dt.date
        lg["amount"] = lg["amount"].astype(float)
        lg["currency"] = lg["currency"].str.upper().str.strip()
        self.ledger = lg
        self.calls = lg[(lg["notice_type"] == "CAPITAL_CALL") & (lg["status"] == "ISSUED")].copy()
        self.dists = lg[(lg["notice_type"] == "DISTRIBUTION")].copy()
        reg = pd.read_excel(os.path.join(root, "fondsregister_2026-12-31.xlsx"), sheet_name="Fonds")
        for c in ("first_close", "final_close", "investment_period_end", "term_end"):
            reg[c] = pd.to_datetime(reg[c]).dt.date
        self.reg = reg.set_index("fund_id")
        fx = pd.read_csv(os.path.join(root, "fx_referenzkurse_tagesende.csv"))
        fx["rate_date"] = pd.to_datetime(fx["rate_date"]).dt.date
        fx = fx[fx["currency"].isin(["USD", "EUR"])].copy()
        fx["per_one"] = fx["rate_chf"] / fx["unit"]
        wide = fx.pivot(index="rate_date", columns="currency", values="per_one")
        self.fx = {d: (r["USD"], r["EUR"]) for d, r in wide.iterrows()}
        cu = pd.read_csv(os.path.join(root, "programmkonto_lindenhof_2025-2026.csv"), sep=";", dtype=str, keep_default_na=False)
        for c in ("Buchungsdatum", "Valuta"):
            cu[c] = pd.to_datetime(cu[c]).dt.date
        cu["amount"] = pd.to_numeric(cu["Betrag CHF"].replace("", np.nan))
        self.custody = cu

    def rate(self, d, ccy):
        if ccy == "CHF":
            return 1.0
        while d not in self.fx:
            d -= timedelta(days=1)
        u, e = self.fx[d]
        return u if ccy == "USD" else e

    # ------------------------------------------------------------ the main call
    def funds(self, by="value_date"):
        """Per fund: commitment and calls by month of the value date, in CHF at the plan-date rate."""
        out = []
        for fid, r in self.reg.iterrows():
            rate = self.rate(PLAN_DATE, r["currency"])
            sub = self.calls[self.calls["fund_id"] == fid]
            m = {}
            for d, a in zip(sub[by], sub["amount"]):
                m[mi(d)] = m.get(mi(d), 0.0) + a * rate
            first = min(m) if m else None
            out.append(dict(fid=fid, code=r["fund_code"], s=r["strategy"], ccy=r["currency"], C=float(r["commitment"]) * rate,
                            C_fcy=float(r["commitment"]), calls=m, first=first, fc=mi(r["first_close"]),
                            ip=mi(r["investment_period_end"]), ip_date=r["investment_period_end"]))
        return out

    def closed_shares(self, fs, by="value_date"):
        out = {}
        for d in fs:
            if d["ip_date"] <= PLAN_DATE:
                sub = self.calls[(self.calls["fund_id"] == d["fid"]) & (self.calls[by] <= d["ip_date"])]
                out[d["code"]] = float(sub["amount"].sum()) / d["C_fcy"]
        return out


def called_to(d, upto):
    return sum(v for k, v in d["calls"].items() if k <= upto)


def bkey(d, i, key, band, age_from):
    a0 = d["first"] if age_from == "first_call" else d["fc"]
    if key == "age":
        return (i - a0) // band
    if key == "toip":
        return (d["ip"] - i) // band if i <= d["ip"] else -1 - (i - d["ip"]) // band
    if key == "ipstatus":
        return ((i - a0) // band, i > d["ip"])


def rates(fs, plan_i=PLAN_I, est0=None, band=12, key="age", by_strat=False, age_from="first_call", weight="sum"):
    num, den, per = {}, {}, {}
    for d in fs:
        if d["first"] is None or d["first"] > plan_i:
            continue
        cum = 0.0
        for i in range(d["first"], plan_i + 1):
            unf = d["C"] - cum
            c = d["calls"].get(i, 0.0)
            if (est0 is None or i >= est0) and unf > 1.0:
                b = bkey(d, i, key, band, age_from)
                if by_strat:
                    b = (d["s"], b)
                num[b] = num.get(b, 0.0) + c
                den[b] = den.get(b, 0.0) + unf
                per.setdefault(b, []).append(c / unf)
            cum += c
    if weight == "mean":
        return {b: float(np.mean(v)) for b, v in per.items()}
    return {b: num[b] / den[b] for b in num if den[b] > 0}


def _n(k, by_strat):
    x = k[1] if by_strat else k
    return x[0] if isinstance(x, tuple) else x


def lookup(R, b, by_strat, s):
    k = (s, b) if by_strat else b
    if k in R:
        return R[k]
    cands = [kk for kk in R if (kk[0] == s if by_strat else True)]
    if isinstance(b, tuple):
        cands = [kk for kk in cands if (kk[1] if by_strat else kk)[1] == b[1]] or cands
    bb = b[0] if isinstance(b, tuple) else b
    lower = [kk for kk in cands if _n(kk, by_strat) <= bb]
    if lower:
        return R[max(lower, key=lambda kk: _n(kk, by_strat))]
    return R[min(cands, key=lambda kk: _n(kk, by_strat))] if cands else 0.0


def ta(d, R, months, unf0, band=12, key="age", by_strat=False, age_from="first_call"):
    unf, s = unf0, 0.0
    for i in months:
        r = lookup(R, bkey(d, i, key, band, age_from), by_strat, d["s"])
        c = min(unf, r * unf)
        unf -= c
        s += c
    return s


def forecast(pk, fs, method="golden", plan_i=PLAN_I, tau=None, band=12, by_strat=False, age_from="first_call", est0=None, key="age",
             weight="sum", detail=False):
    R = rates(fs, plan_i, est0, band, key, by_strat, age_from, weight)
    sh = pk.closed_shares(fs)
    tau_v = float(np.mean(list(sh.values()))) if not isinstance(tau, (int, float)) else float(tau)
    smean = {}
    for st in STRATS:
        v = [x for d in fs for c, x in sh.items() if c == d["code"] and d["s"] == st]
        smean[st] = float(np.mean(v)) if v else tau_v
    win = list(range(plan_i + 1, plan_i + 13))
    tot = grp = 0.0
    per = {}
    for d in fs:
        if d["first"] is None or d["first"] > plan_i:
            continue
        called = called_to(d, plan_i)
        unf = d["C"] - called
        in_win = win[0] <= d["ip"] <= win[-1]
        if method == "golden" and in_win:
            t = smean[d["s"]] if tau == "strategy" else tau_v
            need = max(0.0, t * d["C"] - called)
            post_months = [i for i in win if i > d["ip"]]
            post = ta(d, R, post_months, max(0.0, unf - need), band, key, by_strat, age_from) if post_months else 0.0
            s = need + post
        else:
            s = ta(d, R, win, unf, band, key, by_strat, age_from)
        if in_win:
            grp += s
        per[d["code"]] = s
        tot += s
    if detail:
        return tot, grp, per, tau_v
    return tot, grp


def requirement(E, reserve=RESERVE, margin=MARGIN):
    return (1 + margin) * E - reserve


def amount(E, **kw):
    r = requirement(E, **kw)
    for a in MENU:
        if a * 1e6 >= r:
            return a
    return None


def golden_family(pk, fs):
    sh = pk.closed_shares(fs)
    v = np.array(list(sh.values()))
    est19 = 2019 * 12
    est21 = 2021 * 12
    members = [("canonical: 12-month age bands, pooled, first call, all records, mean drawn share", {}),
               ("6-month age bands", dict(band=6)), ("age bands by strategy", dict(by_strat=True)),
               ("age from the first close", dict(age_from="first_close")), ("median drawn share", dict(tau=float(np.median(v)))),
               ("drawn share by strategy", dict(tau="strategy")), ("records from 2019", dict(est0=est19)), ("records from 2021", dict(est0=est21)),
               ("6-month bands by strategy", dict(by_strat=True, band=6)), ("mean of fund-month rates", dict(weight="mean")),
               ("lowest drawn share", dict(tau=float(v.min()))), ("highest drawn share", dict(tau=float(v.max())))]
    return [(nm, forecast(pk, fs, "golden", **kw)[0]) for nm, kw in members]


def ladder(pk, fs):
    t26 = sum(v for d in fs for k, v in d["calls"].items() if PLAN_I - 11 <= k <= PLAN_I)
    cells = {"R0": ("the programme's 2026 calls carried forward", t26)}
    for nm, label, kw in [("R1", "age-band call rates on unfunded commitment (12-month bands from the first call, pooled)", {}),
                          ("R1-6", "the same with 6-month bands", dict(band=6)),
                          ("R1s", "age-band rates by strategy", dict(by_strat=True)),
                          ("R1fc", "age from the first close", dict(age_from="first_close")),
                          ("R1b", "age bands split by in or after the investment period", dict(key="ipstatus")),
                          ("R1m", "mean of fund-month rates", dict(weight="mean")),
                          ("R2-12", "rates by months to the investment-period end, 12-month bands", dict(key="toip")),
                          ("R2-6", "rates by months to the investment-period end, 6-month bands", dict(key="toip", band=6)),
                          ("R2-3", "rates by months to the investment-period end, 3-month bands", dict(key="toip", band=3)),
                          ("R2s-6", "months to the investment-period end by strategy, 6-month bands", dict(key="toip", band=6, by_strat=True))]:
        cells[nm] = (label, forecast(pk, fs, "ta", **kw)[0])
    cells["X1"] = ("every undrawn franc of the deadline group called by the deadline", forecast(pk, fs, "golden", tau=1.0)[0])
    # own pace: each fund's calls over 2026 on its unfunded commitment at the end of 2025, carried to 2027
    own = 0.0
    for d in fs:
        if d["first"] is None:
            continue
        u25 = d["C"] - called_to(d, PLAN_I - 12)
        c26 = sum(v for k, v in d["calls"].items() if PLAN_I - 11 <= k <= PLAN_I)
        r = c26 / u25 if u25 > 1 and d["first"] <= PLAN_I - 12 else None
        unf = d["C"] - called_to(d, PLAN_I)
        if r is None:
            own += ta(d, rates(fs), WIN, unf)
        else:
            own += min(unf, r * unf)
    cells["R3own"] = ("each fund's own 2026 call rate on its unfunded commitment", own)
    # the deadline balance spread evenly to every in-period fund's own deadline
    sh = pk.closed_shares(fs)
    tau = float(np.mean(list(sh.values())))
    R = rates(fs)
    lin = 0.0
    for d in fs:
        if d["first"] is None:
            continue
        called = called_to(d, PLAN_I)
        if d["ip"] >= WIN[0]:
            rem = max(0.0, tau * d["C"] - called)
            months = d["ip"] - PLAN_I
            lin += rem * min(12, months) / months
        else:
            lin += ta(d, R, WIN, d["C"] - called)
    cells["X2"] = ("the balance to the drawn share spread evenly to every in-period fund's own deadline", lin)
    return cells


def backtest(pk, fs, year):
    bi = (year - 1) * 12 + 11
    fl = [d for d in fs if d["first"] is not None and d["first"] <= bi]
    R = rates(fs, plan_i=bi)
    fc = sum(ta(d, R, list(range(bi + 1, bi + 13)), d["C"] - called_to(d, bi)) for d in fl)
    real = sum(d["calls"].get(i, 0.0) for d in fl for i in range(bi + 1, bi + 13))
    return fc, real


# ------------------------------------------------------------ the ask: distributions received in 2026
def quarter(d):
    return (d.month - 1) // 3 + 1


def _grid():
    return {s: {q: 0.0 for q in QUARTERS} for s in STRATS}


def ask_golden(pk, detail=False):
    cu = pk.custody
    cr = cu[(cu["Buchungstext"] == "Gutschrift Ausschuettung") & (cu["Valuta"] >= date(2026, 1, 1)) & (cu["Valuta"] <= PLAN_DATE)]
    lg = pk.dists[pk.dists["status"] == "ISSUED"]
    cash = lg[lg["line_type"] != "IN_KIND"]
    tot_by_notice = cash.groupby("notice_id")["amount"].sum().to_dict()
    fund_by_notice = cash.groupby("notice_id")["fund_id"].first().to_dict()
    g = _grid()
    rows = []
    for r in cr.itertuples():
        tref = r.Transaktionsreferenz
        nid = r.Referenz.split(" ")[0]
        amts = [tot_by_notice[k] for k in (tref, nid) if k in tot_by_notice]
        fids = {fund_by_notice[k] for k in (tref, nid) if k in fund_by_notice}
        assert amts and len(fids) == 1, (tref, nid)
        assert max(amts) - min(amts) < 0.005, (tref, nid, amts)
        fid = fids.pop()
        ccy = pk.reg.loc[fid, "currency"]
        s = pk.reg.loc[fid, "strategy"]
        chf = amts[0] * pk.rate(r.Valuta, ccy)
        g[s][quarter(r.Valuta)] += chf
        rows.append((r.Valuta, fid, nid, tref, amts[0], ccy, chf, len(amts)))
    if detail:
        return g, rows
    return g


def ask_ledger(pk, date_rule="value", keep="both", cash_only=True, issued_only=True):
    """The ledger-only stops: s1 (both records, the ledger's value date), s2 and s3 (notice-level dedupe, keeping the clerk's
    or the feed's record), s5 (lazy: in specie and withdrawn kept)."""
    lg = pk.dists.copy()
    if issued_only:
        lg = lg[lg["status"] == "ISSUED"]
    if cash_only:
        lg = lg[lg["line_type"] != "IN_KIND"]
    notes = lg.groupby("notice_id").agg(fund_id=("fund_id", "first"), value_date=("value_date", "first"), amount=("amount", "sum"),
                                         n=("line_no", "count"), ref=("investment_ref", lambda x: "".join(x))).reset_index()
    notes["feed"] = notes["ref"] == ""
    if keep in ("clerk", "feed"):
        drop = set()
        for fid, grp in notes.groupby("fund_id"):
            feeds = grp[grp["feed"]]
            clerks = grp[~grp["feed"]]
            for fr in feeds.itertuples():
                m = clerks[(abs(clerks["amount"] - fr.amount) < 0.005) & (clerks["value_date"].apply(lambda d: abs((d - fr.value_date).days) <= 6))]
                if len(m):
                    drop.add(fr.notice_id if keep == "clerk" else m.iloc[0]["notice_id"])
        notes = notes[~notes["notice_id"].isin(drop)]
    g = _grid()
    for r in notes.itertuples():
        if not (date(2026, 1, 1) <= r.value_date <= PLAN_DATE):
            continue
        ccy = pk.reg.loc[r.fund_id, "currency"]
        g[pk.reg.loc[r.fund_id, "strategy"]][quarter(r.value_date)] += r.amount * pk.rate(r.value_date, ccy)
    return g


def ask_custody_chf(pk):
    """s4: the custodian's francs at its dealing rates, attributed to strategies through the ledger."""
    cu = pk.custody
    cr = cu[(cu["Buchungstext"] == "Gutschrift Ausschuettung") & (cu["Valuta"] >= date(2026, 1, 1)) & (cu["Valuta"] <= PLAN_DATE)]
    lg = pk.dists[pk.dists["status"] == "ISSUED"]
    fund_by_notice = lg.groupby("notice_id")["fund_id"].first().to_dict()
    g = _grid()
    for r in cr.itertuples():
        nid = r.Referenz.split(" ")[0]
        fid = fund_by_notice.get(r.Transaktionsreferenz) or fund_by_notice.get(nid)
        g[pk.reg.loc[fid, "strategy"]][quarter(r.Valuta)] += r.amount
    return g


def grid_figures(g):
    """The 20 graded figures in CHF thousand: four quarters and the year for each strategy, and the four quarter totals."""
    out = {}
    for s in STRATS:
        for q in QUARTERS:
            out[f"{s}_Q{q}"] = g[s][q] / 1000.0
        out[f"{s}_year"] = sum(g[s].values()) / 1000.0
    for q in QUARTERS:
        out[f"total_Q{q}"] = sum(g[s][q] for s in STRATS) / 1000.0
    out["top_strategy"] = max(STRATS, key=lambda s: sum(g[s].values()))
    return out


# ------------------------------------------------------------ figures for the documents
def h1_2025_bridge(pk):
    nav = pd.read_csv(os.path.join(pk.root, "nav_register_quartal.csv"))
    nav["period_end"] = pd.to_datetime(nav["period_end"]).dt.date
    out = {s: dict(opening=0.0, calls=0.0, dists=0.0, closing=0.0) for s in STRATS}
    for r in nav.itertuples():
        s = pk.reg.loc[r.fund_id, "strategy"]
        if r.period_end == date(2024, 12, 31):
            out[s]["opening"] += r.nav_fund_ccy * pk.rate(date(2024, 12, 31), r.currency)
        if r.period_end == date(2025, 6, 30):
            out[s]["closing"] += r.nav_fund_ccy * pk.rate(date(2025, 6, 30), r.currency)
    lg = pk.ledger[(pk.ledger["status"] == "ISSUED") & (pk.ledger["value_date"] >= date(2025, 1, 1)) & (pk.ledger["value_date"] <= date(2025, 6, 30))]
    for r in lg.itertuples():
        s = pk.reg.loc[r.fund_id, "strategy"]
        v = r.amount * pk.rate(r.value_date, r.currency)
        if r.notice_type == "CAPITAL_CALL":
            out[s]["calls"] += v
        elif r.line_type != "IN_KIND":
            out[s]["dists"] += v
    tot = dict(opening=0.0, calls=0.0, dists=0.0, closing=0.0)
    for s in STRATS:
        b = out[s]
        b["valuation"] = b["closing"] - b["opening"] - b["calls"] + b["dists"]
        for k in tot:
            tot[k] += b[k]
    tot["valuation"] = tot["closing"] - tot["opening"] - tot["calls"] + tot["dists"]
    out["TOTAL"] = tot
    return out


def half_years_net_out(pk, last=(2025, 1)):
    """How many half-years running, to the one named (year, half), distributions exceeded calls (value-date rates)."""
    lg = pk.ledger[pk.ledger["status"] == "ISSUED"]
    y, h = last
    n = 0
    while True:
        a, b = (date(y, 1, 1), date(y, 6, 30)) if h == 1 else (date(y, 7, 1), date(y, 12, 31))
        x = lg[(lg["value_date"] >= a) & (lg["value_date"] <= b)]
        calls = sum(r.amount * pk.rate(r.value_date, r.currency) for r in x[x["notice_type"] == "CAPITAL_CALL"].itertuples())
        dists = sum(r.amount * pk.rate(r.value_date, r.currency) for r in x[(x["notice_type"] == "DISTRIBUTION") & (x["line_type"] != "IN_KIND")].itertuples())
        if dists <= calls:
            return n
        n += 1
        y, h = (y, 1) if h == 2 else (y - 1, 2)


def september_event(pk):
    cu = pk.custody
    dr = cu[cu["Buchungstext"] == "Ziehung Standby-Fazilitaet"]
    rp = cu[cu["Buchungstext"] == "Rueckzahlung Standby-Fazilitaet"]
    d0 = dr["Valuta"].min()
    week = cu[(cu["Buchungstext"] == "Zahlung Kapitalabruf") & (cu["Valuta"] >= d0 - timedelta(days=d0.weekday())) & (cu["Valuta"] <= d0 - timedelta(days=d0.weekday()) + timedelta(days=4))]
    return dict(date=d0, drawn=float(dr["amount"].sum()), repaid=rp["Valuta"].min(), calls=float(-week["amount"].sum()),
                first=d0 - timedelta(days=d0.weekday()))


def ask_variant(pk, dedupe=True, dates="arrival", inkind=False, withdrawn=False, chf="reference"):
    """One handling of the ask's devices: dedupe the feed's advices against the clerks' notices (P1), date by the cash's
    arrival or by the ledger's value date (h1), keep the in-specie line (h2), keep the withdrawn notice (h3), take the
    custodian's francs at its dealing rates (h4). The golden is dedupe, arrival, neither kept, reference rates."""
    cu = pk.custody
    cr = cu[(cu["Buchungstext"] == "Gutschrift Ausschuettung")]
    arrival, dealing = {}, {}
    for r in cr.itertuples():
        for k in (r.Transaktionsreferenz, r.Referenz.split(" ")[0]):
            arrival[k] = r.Valuta
            dealing[k] = r.amount
    lg = pk.dists if withdrawn else pk.dists[pk.dists["status"] == "ISSUED"]
    if not inkind:
        lg = lg[lg["line_type"] != "IN_KIND"]
    notes = lg.groupby("notice_id").agg(fund_id=("fund_id", "first"), value_date=("value_date", "first"), amount=("amount", "sum"),
                                         ref=("investment_ref", lambda x: "".join(x))).reset_index()
    notes["feed"] = notes["ref"] == ""
    if dedupe:
        # a feed advice and a clerk's notice for the same cash share one custodian credit
        credit_of = {}
        for r in cr.itertuples():
            credit_of.setdefault(r.Transaktionsreferenz, r.Transaktionsreferenz)
            credit_of.setdefault(r.Referenz.split(" ")[0], r.Transaktionsreferenz)
        notes["credit"] = notes["notice_id"].map(credit_of)
        dup = notes[notes["credit"].notna()].groupby("credit")["notice_id"].count()
        dup_credits = set(dup[dup > 1].index)
        notes = notes[~(notes["feed"] & notes["credit"].isin(dup_credits))]
    g = _grid()
    for r in notes.itertuples():
        if dates == "arrival":
            if r.notice_id not in arrival:
                continue      # no credit on the 2025-2026 statement: the cash arrived after it (or the line was never cash)
            d = arrival[r.notice_id]
        else:
            d = r.value_date
        if not (date(2026, 1, 1) <= d <= PLAN_DATE):
            continue
        s = pk.reg.loc[r.fund_id, "strategy"]
        if chf == "dealing" and r.notice_id in dealing:
            g[s][quarter(d)] += dealing[r.notice_id]
        else:
            g[s][quarter(d)] += r.amount * pk.rate(d, pk.reg.loc[r.fund_id, "currency"])
    return g
