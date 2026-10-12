"""The call, computed from the written pack only: the hours the January to March 2027 list will use under the SOW,
by maturity month, with every rung of the ladder and the estimator family the fork table names.

Golden route: wash the coming list's numbers against the register at the cut; price dialling per ordered callable
configuration from the seven closed campaigns (non-reaching dials and the chance of a conversation per released case);
scale by the share of listed deposits with a callable number that reach release; give each expected conversation
8 minutes plus 14 times the share of past conversations that went to the retention offer at the same drop from the
deposit's locked rate to the card it reinvests at (0.25-point bins), the coming list's drops read against the January
to March 2027 card."""
from __future__ import annotations

import math
import os
import re
from collections import defaultdict

import numpy as np
import pandas as pd
import pdfplumber

import world as W

TYPE_LETTER = {"MOBILE": "M", "HOME": "H", "WORK": "W", "Mobile": "M", "Home": "H", "Work": "W"}


# ---------------------------------------------------------------------------------------------------------------
def read_card(path):
    """The reinvestment card from a campaign brief PDF: term (years) -> rate (per cent)."""
    with pdfplumber.open(path) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    m = re.search(r"Rate % p\.a\.\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", text)
    if m:
        return {t: float(m.group(t)) for t in range(1, 6)}
    out = {}
    for t, v in re.findall(r"(\d) years?\s+([\d.]+)", text):
        out[int(t)] = float(v)
    assert sorted(out) == W.TERMS, (path, out)
    return out


def load_lists(target):
    """The seven closed campaigns' lists in one frame: the 2025 report layout and the 2026 core layout."""
    p = lambda f: os.path.join(target, f)
    a = pd.read_csv(p(W.F_LISTS_2025), dtype=str, keep_default_na=False)
    a = pd.DataFrame({
        "campaign": a["Campaign"].str.replace(r"TDR (\d{4})-Q(\d)", r"\1Q\2", regex=True),
        "account": a["Account No"].map(W.norm_acct), "customer_no": a["Customer No"],
        "term": a["Term (mths)"].astype(int) // 12, "rate": a["Rate %"].astype(float),
        "principal": a["Principal"].str.replace(",", "").astype(float),
        "maturity": pd.to_datetime(a["Maturity"], format="%d/%m/%Y")})
    b = pd.read_csv(p(W.F_LISTS_2026), dtype=str, keep_default_na=False)
    b = pd.DataFrame({
        "campaign": b["campaign"].str.replace("TDR-", ""), "account": b["account"], "customer_no": b["customer_no"],
        "term": b["term_months"].astype(int) // 12, "rate": (b["int_rate"].astype(float) * 100).round(2),
        "principal": b["principal"].astype(float), "maturity": pd.to_datetime(b["maturity_date"])})
    return pd.concat([a, b], ignore_index=True)


def load(target):
    p = lambda f: os.path.join(target, f)
    L = {}
    L["past_lists"] = load_lists(target)
    f = pd.read_csv(p(W.F_LIST_FWD), dtype=str)
    L["fwd"] = pd.DataFrame({
        "account": f["account"], "customer_no": f["customer_no"], "term": f["term_months"].astype(int) // 12,
        "rate": (f["int_rate"].astype(float) * 100).round(2), "principal": f["principal"].astype(float),
        "maturity": pd.to_datetime(f["maturity_date"])})
    L["release"] = pd.read_csv(p(W.F_RELEASE), dtype=str, keep_default_na=False)
    L["dials"] = pd.read_csv(p(W.F_DIALS), dtype={"case_ref": str, "kbs_ref": str, "outcome": str, "number": str},
                             keep_default_na=False)
    L["close"] = pd.read_csv(p(W.F_CLOSEOUT), dtype=str, keep_default_na=False)
    L["contacts"] = pd.read_csv(p(W.F_CONTACTS), dtype=str, keep_default_na=False)
    L["dnc"] = pd.read_csv(p(W.F_DNC), dtype=str, keep_default_na=False)
    L["cards"] = {q: read_card(p(W.brief_name(q))) for q in W.PAST + [W.FWD]}
    return L


# ---------------------------------------------------------------------------------------------------------------
def forward_frame(L):
    cut = pd.Timestamp(W.CUT_FWD)
    dnc = L["dnc"]
    rec = pd.to_datetime(dnc["recorded"])
    wd = pd.to_datetime(dnc["withdrawn"].replace("", None))
    active = dnc.loc[(rec <= cut) & (wd.isna() | (wd > cut)), "number"].map(W.norm_phone)
    blocked = set(active)
    c = L["contacts"].copy()
    c["e164"] = c["number"].map(W.norm_phone)
    c["prio"] = c["priority"].astype(int)
    c = c[~c["e164"].isin(blocked)].sort_values(["customer_no", "prio"])
    cfg = c.groupby("customer_no")["contact_type"].apply(lambda s: "-".join(TYPE_LETTER[x] for x in s))
    F = L["fwd"].copy()
    F["cfg"] = F["customer_no"].map(cfg).fillna("")
    F["drop"] = (F["rate"] - F["term"].map(L["cards"][W.FWD])).round(2)
    F["month"] = F["maturity"].dt.month
    return F


def past_cases(L):
    """One row per released case of the closed campaigns: its ordered configuration, non-reaching dials, and whether
    it reached a conversation and a retention conversation; joined to its listed deposit's rate, term and drop. A
    deposit reinvested on its own account can be listed again a year or more later, so the keys carry the campaign:
    release log to close-out on account and release date, close-out to dials on the case reference."""
    rel = L["release"]
    rr = rel[rel["status"] == "RELEASED"].copy()
    tcols = ["type_%d" % k for k in range(1, 5)]
    rr["cfg"] = rr[tcols].apply(lambda r: "-".join(TYPE_LETTER[x] for x in r if x), axis=1)
    rr["campaign"] = rr["campaign"].str.replace("TDR-", "")
    cl = L["close"].copy()
    cl["account"] = cl["kbs_ref"].map(W.norm_acct)
    key = cl.set_index(["account", "released"])["case_ref"]
    rr["case_ref"] = [key[(a, d)] for a, d in zip(rr["account"], rr["release_date"])]
    d = L["dials"]
    nr = d["outcome"].isin(W.NOT_REACHED)
    conv = d["outcome"].isin(W.CONVERSATION + W.RETENTION)
    ret = d["outcome"].isin(W.RETENTION)
    g = pd.DataFrame({"case_ref": d["case_ref"], "nr": nr, "conv": conv, "ret": ret}).groupby("case_ref").agg(
        nr=("nr", "sum"), conv=("conv", "max"), ret=("ret", "max"))
    rr = rr.join(g, on="case_ref")
    rr["nr"] = rr["nr"].fillna(0).astype(int)
    for k in ("conv", "ret"):
        rr[k] = rr[k].fillna(False).astype(bool)
    pl = L["past_lists"].set_index(["campaign", "account"])
    assert pl.index.is_unique
    rr = rr.join(pl[["term", "rate", "principal"]], on=["campaign", "account"])
    assert not rr["rate"].isna().any()
    rr["card"] = [L["cards"][q][t] for q, t in zip(rr["campaign"], rr["term"])]
    rr["drop"] = (rr["rate"] - rr["card"]).round(2)
    rr["n_callable"] = rr["cfg"].str.count("-") + 1
    return rr


def release_share(L, campaigns=None):
    rel = L["release"]
    if campaigns:
        rel = rel[rel["campaign"].str.replace("TDR-", "").isin(campaigns)]
    with_num = rel[(rel["status"] == "RELEASED") | (rel["reason"] == "INSTRUCTED")]
    return float((with_num["status"] == "RELEASED").mean())


# ---------------------------------------------------------------------------------------------------------------
# Dialling estimators
def yields_by(cases, key):
    g = cases.groupby(key).agg(U=("nr", "mean"), C=("conv", "mean"), n=("nr", "size"))
    return g


def cfg_key(kind, cfg):
    if kind == "ordered":
        return cfg
    if kind == "unordered":
        return "-".join(sorted(cfg.split("-"))) if cfg else ""
    if kind == "count":
        return str(cfg.count("-") + 1) if cfg else "0"
    raise ValueError(kind)


def dial_terms(F, cases, kind="ordered", fallback=False):
    ck = cases.assign(k=cases["cfg"].map(lambda c: cfg_key(kind, c)))
    y = yields_by(ck, "k")
    k = F["cfg"].map(lambda c: cfg_key(kind, c))
    U = k.map(y["U"])
    C = k.map(y["C"])
    if fallback and (U.isna() & (F["cfg"] != "")).any():
        yc = yields_by(cases.assign(k=cases["cfg"].map(lambda c: cfg_key("count", c))), "k")
        kc = F["cfg"].map(lambda c: cfg_key("count", c))
        U = U.fillna(kc.map(yc["U"]))
        C = C.fillna(kc.map(yc["C"]))
    none = F["cfg"] == ""
    U[none], C[none] = 0.0, 0.0
    assert not U.isna().any(), sorted(set(k[U.isna()]))
    return U.astype(float), C.astype(float)


def structural_params(L, cases):
    """A per-number fit of the dialling rules from the dial log: per type, the share of numbers found disconnected at
    the first dial, the share of answered numbers answered by someone else, the chance a dial on a working number is
    answered; and the daily withdrawal rate per open case."""
    d = L["dials"]
    slot_type = {}
    for ref, cfg in zip(cases["case_ref"], cases["cfg"]):
        for i, t in enumerate(cfg.split("-")):
            slot_type[(ref, i + 1)] = t
    d = d.assign(t=[slot_type[(ref, int(sl))] for ref, sl in zip(d["case_ref"], d["slot"])])
    ans_codes = set(W.CONVERSATION + W.RETENTION + (W.WRONG_CODE,))
    par = {}
    per_num = d.groupby(["case_ref", "slot"]).agg(t=("t", "first"), first=("outcome", "first"),
                                                  wp=("outcome", lambda s: W.WRONG_CODE in set(s)),
                                                  ans=("outcome", lambda s: bool(set(s) & ans_codes)))
    for t in "MHW":
        pn = per_num[per_num["t"] == t]
        p_dead = float((pn["first"] == W.DEAD_CODE).mean())
        p_wrong = float(pn["wp"].sum() / max(pn["ans"].sum(), 1)) * (1 - p_dead)
        dt_ = d[(d["t"] == t) & (d["outcome"] != W.DEAD_CODE)]
        p_ans = float(dt_["outcome"].isin(ans_codes).mean())
        par[t] = (p_dead, p_wrong, p_ans)
    # withdrawals per case-day: WITHDRAWN closures over the dialling days the cases were open
    cl = L["close"]
    days = 0
    for a, b in zip(cl["released"], cl["closed"]):
        a, b = pd.Timestamp(a).date(), pd.Timestamp(b).date()
        k = a
        while k <= b:
            days += W.dialling_day(k)
            k = k + pd.Timedelta(days=1).to_pytimedelta()
    h = float((cl["close_reason"] == "WITHDRAWN").sum()) / days
    return par, h


def structural_expect(cfg, par, h):
    """Exact expected non-reaching dials and chance of a conversation for one ordered configuration under the
    schedule 1 rules, with each number's state drawn once and a constant daily withdrawal rate."""
    import itertools
    from functools import lru_cache
    types = cfg.split("-") if cfg else []
    n = len(types)
    if n == 0:
        return 0.0, 0.0
    E_nr, P_c = 0.0, 0.0
    for states in itertools.product("DXV", repeat=n):
        pr = 1.0
        for t, s_ in zip(types, states):
            pd_, pw, _ = par[t]
            pr *= {"D": pd_, "X": pw, "V": 1 - pd_ - pw}[s_]
        if pr == 0:
            continue

        @lru_cache(maxsize=None)
        def day(k, open_):
            # returns (expected non-reaching dials from here, probability of a conversation from here)
            if k >= W.DIALS_PER_NUMBER or not open_:
                return 0.0, 0.0
            e_tot, c_tot = 0.0, 0.0
            # withdrawal before the day's dials
            stay = 1 - h

            def walk(i, open_next, prob, nr):
                # process the open numbers in order from position i
                nonlocal e_tot, c_tot
                if i == len(open_):
                    e2, c2 = day(k + 1, tuple(open_next))
                    e_tot += prob * (nr + e2)
                    c_tot += prob * c2
                    return
                j = open_[i]
                s_, t = states[j], types[j]
                pa = par[t][2]
                if s_ == "D":
                    walk(i + 1, open_next, prob, nr + 1)
                elif s_ == "X":
                    walk(i + 1, open_next, prob * pa, nr + 1)
                    walk(i + 1, open_next + [j], prob * (1 - pa), nr + 1)
                else:
                    e_tot += prob * pa * nr
                    c_tot += prob * pa
                    walk(i + 1, open_next + [j], prob * (1 - pa), nr + 1)
            walk(0, [], stay, 0)
            return e_tot, c_tot
        e, c = day(0, tuple(range(n)))
        E_nr += pr * e
        P_c += pr * c
    return E_nr, P_c


def structural_terms(L, F, cases):
    par, h = structural_params(L, cases)
    cache = {}
    U, C = [], []
    for cfg in F["cfg"]:
        if cfg not in cache:
            cache[cfg] = structural_expect(cfg, par, h)
        U.append(cache[cfg][0])
        C.append(cache[cfg][1])
    return pd.Series(U, index=F.index), pd.Series(C, index=F.index), par, h


# ---------------------------------------------------------------------------------------------------------------
# Retention share estimators
def share_bins(cases, width, offset=0.0, campaigns=None):
    cv = cases[cases["conv"]]
    if campaigns:
        cv = cv[cv["campaign"].isin(campaigns)]
    b = np.floor((cv["drop"] - offset) / width + 1e-9)
    s = cv.groupby(b)["ret"].agg(["mean", "size"])
    return s


def p_from_bins(drops, s, width, offset=0.0, fallback=False):
    """Each forward drop's share from the past conversations in the same bin. With fallback, a bin the past never
    carried takes its nearest carried bin (a solver's natural repair); the golden's bins need none (asserted)."""
    b = np.floor((drops - offset) / width + 1e-9)
    out = b.map(s["mean"])
    if fallback and out.isna().any():
        keys = np.array(sorted(s.index))
        out = out.fillna(b.map(lambda k: s["mean"][keys[np.argmin(np.abs(keys - k))]]))
    assert not out.isna().any(), sorted(set(drops[out.isna()]))
    return out.astype(float)


def logistic_fit(x, y, extra=None, iters=60):
    X = np.column_stack([np.ones(len(x)), x] + ([] if extra is None else [extra]))
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        z = X @ beta
        pz = 1 / (1 + np.exp(-z))
        wv = pz * (1 - pz)
        H = X.T @ (X * wv[:, None]) + 1e-9 * np.eye(X.shape[1])
        g = X.T @ (y - pz)
        step = np.linalg.solve(H, g)
        beta += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return beta


def p_logistic(cases, drops, terms=None, with_term=False):
    cv = cases[cases["conv"]]
    y = cv["ret"].astype(float).values
    if not with_term:
        b = logistic_fit(cv["drop"].values, y)
        return 1 / (1 + np.exp(-(b[0] + b[1] * drops.values)))
    # term dummies
    T = pd.get_dummies(cv["term"].astype(int)).reindex(columns=W.TERMS, fill_value=0).values[:, 1:].astype(float)
    X = np.column_stack([np.ones(len(cv)), cv["drop"].values, T])
    beta = np.zeros(X.shape[1])
    for _ in range(80):
        pz = 1 / (1 + np.exp(-(X @ beta)))
        wv = pz * (1 - pz)
        H = X.T @ (X * wv[:, None]) + 1e-9 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - pz))
        beta += step
        if np.max(np.abs(step)) < 1e-10:
            break
    Tf = pd.get_dummies(terms.astype(int)).reindex(columns=W.TERMS, fill_value=0).values[:, 1:].astype(float)
    Xf = np.column_stack([np.ones(len(drops)), drops.values, Tf])
    return 1 / (1 + np.exp(-(Xf @ beta)))


def p_isotonic(cases, drops):
    cv = cases[cases["conv"]].sort_values("drop")
    g = cv.groupby("drop")["ret"].agg(["sum", "size"]).reset_index()
    xs = list(g["drop"])
    blocks = [[s, n, x, x] for s, n, x in zip(g["sum"], g["size"], xs)]
    stack = []
    for b in blocks:
        stack.append(b)
        while len(stack) > 1 and stack[-2][0] / stack[-2][1] > stack[-1][0] / stack[-1][1]:
            s2 = stack.pop()
            s1 = stack.pop()
            stack.append([s1[0] + s2[0], s1[1] + s2[1], s1[2], s2[3]])
    pts = [(b[2], b[3], b[0] / b[1]) for b in stack]

    def f(x):
        for lo, hi, v in pts:
            if lo <= x <= hi:
                return v
        # between blocks: the nearer block's value
        best = min(pts, key=lambda t: min(abs(x - t[0]), abs(x - t[1])))
        return best[2]
    return np.array([f(x) for x in drops.values])


def p_linear(cases, drops):
    cv = cases[cases["conv"]]
    A = np.column_stack([np.ones(len(cv)), cv["drop"].values])
    coef, *_ = np.linalg.lstsq(A, cv["ret"].astype(float).values, rcond=None)
    return coef[0] + coef[1] * drops.values, coef


# ---------------------------------------------------------------------------------------------------------------
def minutes(F, U, C, R, p):
    has = F["cfg"] != ""
    m = np.where(has, R * (W.MIN_NOT_REACHED * U + C * (W.MIN_CONVERSATION + (W.MIN_RETENTION - W.MIN_CONVERSATION) * p)),
                 0.0)
    return pd.Series(m, index=F.index)


def hours(F, m):
    tot = float(m.sum() / 60.0)
    by_month = {int(k): float(v / 60.0) for k, v in m.groupby(F["month"]).sum().items()}
    return tot, by_month


def golden(L, F=None, cases=None):
    F = forward_frame(L) if F is None else F
    cases = past_cases(L) if cases is None else cases
    U, C = dial_terms(F, cases, "unordered")
    R = release_share(L)
    s = share_bins(cases, 0.25)
    p = p_from_bins(F["drop"], s, 0.25)
    m = minutes(F, U, C, R, p)
    tot, by_month = hours(F, m)
    return dict(F=F, cases=cases, U=U, C=C, R=R, p=p, m=m, total=tot, months=by_month,
                conv=float((np.where(F["cfg"] != "", R * C, 0.0)).sum()),
                ret=float((np.where(F["cfg"] != "", R * C * p, 0.0)).sum()),
                nr=float((np.where(F["cfg"] != "", R * U, 0.0)).sum()))


def rungs(L, G):
    F, cases = G["F"], G["cases"]
    U, C, R = G["U"], G["C"], G["R"]
    out = {}
    # R0: hours per listed deposit of the latest campaign, and of all seven
    d = L["dials"]
    mins_dial = d["outcome"].map(W.billed_minutes)
    camp = d["case_ref"].str[2:6]
    listed = L["past_lists"].groupby("campaign").size()
    per = {}
    for q in W.PAST:
        key = q[2:4] + q[-2:]
        per[q] = float(mins_dial[camp == key].sum()) / listed[q]
    out["R0_latest"] = per["2026Q3"] * len(F) / 60.0
    out["R0_all"] = sum(per[q] * listed[q] for q in W.PAST) / listed.sum() * len(F) / 60.0
    cv = cases[cases["conv"]]
    pooled = float(cv["ret"].mean())
    out["R1_pooled"] = float(minutes(F, U, C, R, pooled).sum() / 60.0)
    latest = float(cv[cv["campaign"] == "2026Q3"]["ret"].mean())
    out["R2a_latest"] = float(minutes(F, U, C, R, latest).sum() / 60.0)
    ts = cv.groupby("term")["ret"].mean()
    out["R2b_term"] = float(minutes(F, U, C, R, F["term"].map(ts)).sum() / 60.0)
    lb = np.floor(cv["rate"] / 0.25 + 1e-9)
    ls = cv.groupby(lb)["ret"].mean()
    fl = np.floor(F["rate"] / 0.25 + 1e-9).map(ls)
    if fl.isna().any():   # a locked-rate band the past never carried: the nearest band
        keys = np.array(sorted(ls.index))
        fl = fl.fillna(np.floor(F["rate"] / 0.25 + 1e-9).map(lambda k: ls[keys[np.argmin(np.abs(keys - k))]]))
    out["R2c_locked"] = float(minutes(F, U, C, R, fl).sum() / 60.0)
    qs = cv.groupby("campaign")["ret"].mean().reindex(W.PAST)
    x = np.arange(len(W.PAST))
    a, b = np.polyfit(x, qs.values, 1)
    trend = float(np.clip(b + a * (len(W.PAST) + 1), 0, 1))     # 2026Q3 is x=6; 2027Q1 is x=8
    out["R2d_trend"] = float(minutes(F, U, C, R, trend).sum() / 60.0)
    out["shares"] = dict(pooled=pooled, latest=latest, trend=trend, by_term={int(k): float(v) for k, v in ts.items()},
                         by_campaign={k: float(v) for k, v in qs.items()})
    # the drop without the release share (a second error)
    out["R3_no_release"] = float(minutes(F, U, C, 1.0, G["p"]).sum() / 60.0)
    return out


def family(L, G):
    """Every member of the estimator family the fork table names (SF7, SF8, SF9): hours total and by month."""
    F, cases = G["F"], G["cases"]
    R = G["R"]
    res = {}
    U0, C0 = G["U"], G["C"]
    for kind in ("ordered", "unordered", "count"):
        U, C = dial_terms(F, cases, kind, fallback=(kind == "ordered"))
        for w in (0.20, 0.25, 0.50):
            for off in ((0.0, 0.10) if w != 0.25 else (0.0, 0.125)):
                s = share_bins(cases, w, off)
                p = p_from_bins(F["drop"], s, w, off, fallback=True)
                m = minutes(F, U, C, R, p)
                res["%s/bins%.2f+%.3f" % (kind, w, off)] = hours(F, m)
        for nm, p in (("logit", p_logistic(cases, F["drop"])),
                      ("logit+term", p_logistic(cases, F["drop"], F["term"], with_term=True)),
                      ("isotonic", p_isotonic(cases, F["drop"]))):
            res["%s/%s" % (kind, nm)] = hours(F, minutes(F, U, C, R, p))
    # the share by band of drop within each term, a cell with fewer than 30 past conversations taking its band's share
    cvv = cases[cases["conv"]]
    bk = np.floor(cvv["drop"] / 0.25 + 1e-9)
    cell = cvv.groupby([bk, cvv["term"]])["ret"].agg(["mean", "size"])
    band_s = cvv.groupby(bk)["ret"].mean()
    fb = np.floor(F["drop"] / 0.25 + 1e-9)
    p_dt = np.array([cell.loc[(k, t), "mean"] if (k, t) in cell.index and cell.loc[(k, t), "size"] >= 30 else band_s[k]
                     for k, t in zip(fb, F["term"])])
    res["unordered/bins0.25xterm"] = hours(F, minutes(F, U0, C0, R, p_dt))
    Us, Cs, _, _ = structural_terms(L, F, cases)
    s = share_bins(cases, 0.25)
    res["structural/bins0.25+0.000"] = hours(F, minutes(F, Us, Cs, R, p_from_bins(F["drop"], s, 0.25)))
    # campaign subsets (SF7) on the golden estimator
    for nm, qs in (("latest4", W.PAST[-4:]), ("2026", W.PAST[-3:]), ("2025", W.PAST[:4])):
        sub = cases[cases["campaign"].isin(qs)]
        U, C = dial_terms(F, sub, "unordered", fallback=True)
        s = share_bins(sub, 0.25)
        p = p_from_bins(F["drop"], s, 0.25, fallback=True)
        res["subset/%s" % nm] = hours(F, minutes(F, U, C, release_share(L, qs), p))
    return res
