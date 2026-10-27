"""task156 calculations from the shipped files only (the bundle under target/), never from the world.

The golden: each site's 2027 need is its handled flags at the plan's questions times the site's flag rate, plus its
routed community items, each 2027 month's inbox arrivals (the plan's questions times the site's items per question)
less what its reviewer pool can review. Review access is by invitation only from 1 September 2026, so the pool of
September 2026 only shrinks: each of its reviewers is carried on the monthly stop rate the roster shows at each tenure
(months since access was granted, each reviewer counted from the month the platform's record first sees them active),
each at the reviews a month reviewers complete when the inbox outruns them. Every other route the design names is
computed here too, for the checks."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import zipfile
import xml.etree.ElementTree as ET

import numpy as np

import common as K
import records as R

STD26, STD27 = K.STD_2026, K.STD_2027
T_CODE = {v: k for k, v in R.ITEM_CODE.items()}
OLD_TO_CODE = {K.SITE[c]["old"]: c for c in K.SITES}
OLD_TO_CODE[K.GRAPHICS_OLD] = "gamedev"
HIST_MONTHS = K.months(K.NEW_START, K.HIST_END)          # 2024-01 .. 2026-09
FWD_MONTHS = K.months(dt.date(2026, 10, 1), K.D_END)     # 2026-10 .. 2027-12
MIDX = {ym: k for k, ym in enumerate(HIST_MONTHS)}


def _rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ym_of(s):
    return int(s[:4]), int(s[5:7])


def mabs(s):
    """A month as a running count of months (year times 12 plus month less one)."""
    return int(s[:4]) * 12 + int(s[5:7]) - 1


M_JAN24, M_AUG25, M_SEP25, M_AUG26, M_SEP26 = (y * 12 + m - 1 for y, m in ((2024, 1), (2025, 8), (2025, 9), (2026, 8),
                                                                          (2026, 9)))
NT = 400                                 # tenure months held in a curve


def read_xlsx(path):
    """{sheet: [row tuples]} with openpyxl (values only)."""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    return {ws.title: [tuple(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}


class Data:
    pass


def load(target):
    p = lambda f: os.path.join(target, f)
    D = Data()
    # inbox, revised pull
    ent = {s: {t: np.zeros(len(HIST_MONTHS)) for t in K.ITEMS} for s in K.SITES}
    rev = {s: np.zeros(len(HIST_MONTHS)) for s in K.SITES}
    rout = {s: {t: np.zeros(len(HIST_MONTHS)) for t in K.ITEMS} for s in K.SITES}
    keys = set()
    for r in _rows(p(R.F_INBOX)):
        k = (r["site"], r["entry_date_utc"], r["item_type"])
        assert k not in keys
        keys.add(k)
        i = MIDX[ym_of(r["entry_date_utc"])]
        t = T_CODE[r["item_type"]]
        ent[r["site"]][t][i] += int(r["entered"])
        rev[r["site"]][i] += int(r["reviewed_by_volunteer"])
        rout[r["site"]][t][i] += int(r["routed_to_moderation"])
    D.ent, D.rev, D.rout = ent, rev, rout
    D.ent_all = {s: sum(ent[s][t] for t in K.ITEMS) for s in K.SITES}
    D.rout_all = {s: sum(rout[s][t] for t in K.ITEMS) for s in K.SITES}
    # flags
    fl = {s: np.zeros(len(HIST_MONTHS)) for s in K.SITES}
    for r in _rows(p(R.F_FLAGSUM)):
        fl[r["site"]][MIDX[ym_of(r["date_utc"])]] += int(r["handled_by_moderator"])
    D.flags = fl
    # questions
    q = {s: np.zeros(len(HIST_MONTHS)) for s in K.SITES}
    for r in _rows(p(R.F_POSTS)):
        q[r["site"]][MIDX[ym_of(r["month"])]] = int(r["questions"])
    D.q = q
    # roster: active reviewers by month, exits by last month, arrivals by first month (new grants)
    Rm = {s: np.zeros(len(HIST_MONTHS)) for s in K.SITES}
    exits = {s: np.zeros(len(HIST_MONTHS)) for s in K.SITES}
    joins = {s: np.zeros(len(HIST_MONTHS)) for s in K.SITES}
    for r in _rows(p(R.F_ROSTER)):
        s = r["site"]
        if not r["first_review_on_platform"]:
            continue                 # access open on 1 January 2024, no review on the platform: never active on it
        a, b = MIDX[ym_of(r["first_review_on_platform"])], MIDX[ym_of(r["last_review"])]
        Rm[s][a:b + 1] += 1
        if r["access_status"] == "lapsed":
            exits[s][b] += 1
        if r["access_granted"] >= "2024-01-01":
            joins[s][MIDX[ym_of(r["access_granted"])]] += 1
    D.R, D.exits, D.joins = Rm, exits, joins
    # each access spell: site, grant month, first and last month active on the platform, lapsed or still active
    sp = [(r["site"], mabs(r["access_granted"]), mabs(r["first_review_on_platform"]), mabs(r["last_review"]),
           r["access_status"] == "lapsed") for r in _rows(p(R.F_ROSTER)) if r["first_review_on_platform"]]
    D.sp_site = np.array([x[0] for x in sp])
    D.sp_g = np.array([x[1] for x in sp], dtype=np.int64)
    D.sp_a = np.array([x[2] for x in sp], dtype=np.int64)
    D.sp_b = np.array([x[3] for x in sp], dtype=np.int64)
    D.sp_lapsed = np.array([x[4] for x in sp], dtype=bool)
    # plan
    sh = read_xlsx(p(R.F_PLAN))["Plan 2027"]
    plan = {}
    for row in sh:
        if row and row[0] in K.SITES:
            plan[row[0]] = np.array([float(x) for x in row[2:14]])
    D.plan = plan
    out = {}
    for row in read_xlsx(p(R.F_PLAN))["Outlook Oct-Dec 2026"]:
        if row and row[0] in K.SITES:
            out[row[0]] = np.array([float(x) for x in row[2:5]])
    D.outlook = out
    # old workbook: reviews and active reviewers by site-month, entered and routed
    old, restated = {}, {}
    for name, rows in read_xlsx(p(R.F_OLD)).items():
        head, done, rhead = None, False, None
        for row in rows:
            if not row:
                continue
            if done:
                # below the sheet's notes: the statistics job's restated question counts, if the sheet carries any
                if row[0] == "Site" and len(row) > 1 and isinstance(row[1], str) and row[1].endswith(name):
                    rhead = list(row)
                elif rhead and row[0] in OLD_TO_CODE:
                    for h, v in zip(rhead[1:], row[1:]):
                        if h and v is not None:
                            restated[(row[0], int(name), K.MON3.index(str(h)[:3]))] = int(v)
                continue
            if row[0] == "All sites":
                done = True
                continue
            if row[0] == "Site":
                head = list(row)
                continue
            if head and row[0] in OLD_TO_CODE and row[1]:
                rec = dict(zip(head, row))
                y = int(name)
                m = K.MON3.index(str(rec["Month"])[:3])
                ent_ = sum(int(rec[c]) for c in head if c and c.endswith(" in"))
                rout_ = sum(int(rec[c]) for c in head if c and c.endswith(" to moderators"))
                old[(row[0], y, m)] = dict(ent=ent_, rout=rout_, R=int(rec["Active reviewers"]),
                                           vol=int(rec["Volunteer reviews"]), q=int(rec["Questions"]))
    D.old = old
    D.old_restated = restated
    return D


# ------------------------------------------------------------------------------------------------- estimators
def saturated_pace(D, cut=0.05, use_old=True, use_new=True):
    """Reviews a month an active reviewer completes when the inbox outruns the volunteers: reviews over active
    reviewers in every site-month whose routed share is above the cut."""
    num = den = 0.0
    n = 0
    if use_old:
        for (old, y, m), c in D.old.items():
            if c["ent"] and c["rout"] / c["ent"] > cut:
                num += c["vol"]
                den += c["R"]
                n += 1
    if use_new:
        for s in K.SITES:
            for i in range(len(HIST_MONTHS)):
                if D.ent_all[s][i] and D.rout_all[s][i] / D.ent_all[s][i] > cut:
                    num += D.rev[s][i]
                    den += D.R[s][i]
                    n += 1
    return num / den, n


def exit_rate(D, s, months=24):
    """Monthly exit rate over the months whose exits the roster can show (a reviewer active in September 2026 has
    not lapsed yet, so the last full month of exits is August 2026)."""
    hi = MIDX[(2026, 8)]
    lo = hi - months + 1
    ex = D.exits[s][lo:hi + 1].sum()
    risk = D.R[s][lo:hi + 1].sum()
    return ex / risk, ex


def tenure_counts(D, lo=M_JAN24, hi=M_AUG26, sites=None, trunc=True, shift=0):
    """Stops and reviewer-months by months since review access was granted, over the calendar months lo to hi.

    A reviewer is at risk at each tenure month they are seen active in the window, from their first month active on
    the platform (the record opens in January 2024, so a reviewer granted earlier enters at their tenure then) to their
    last review; a stop is the month of the last review of a reviewer whose access lapsed. trunc=False counts every
    reviewer from the month access was granted (the record's survivors read as whole cohorts). shift moves the stop to
    the month the access lapsed (two months after the last review)."""
    ev = np.zeros(NT)
    rk = np.zeros(NT)
    m = np.ones(len(D.sp_g), dtype=bool) if sites is None else np.isin(D.sp_site, sites)
    for g, a, b, lp in zip(D.sp_g[m], D.sp_a[m], D.sp_b[m], D.sp_lapsed[m]):
        start = max(a, lo) if trunc else g
        end = min(b + shift, hi)
        if end < start:
            continue
        rk[start - g:end - g + 1] += 1
        if lp and b + shift <= hi:
            ev[b + shift - g] += 1
    return ev, rk


def tenure_curve(ev, rk, band=1, tail=12):
    """Monthly stop rate at each tenure month (pooled over bands of `band` months); past the last tenure with
    reviewers at risk, the rate of the last `tail` tenure months observed."""
    h = np.zeros(NT)
    top = int(np.nonzero(rk)[0].max())
    for a in range(0, top + 1, band):
        e, r_ = ev[a:a + band].sum(), rk[a:a + band].sum()
        h[a:a + band] = e / r_ if r_ else 0.0
    lo = max(0, top - tail + 1)
    h[top + 1:] = ev[lo:top + 1].sum() / rk[lo:top + 1].sum()
    return h


def survival_from(h, tau0, k):
    """Chance that a reviewer active at tenure tau0 is still active k months later."""
    p = np.ones(len(tau0))
    out = []
    for j in range(k):
        p = p * (1.0 - h[np.minimum(tau0 + j, NT - 1)])
        out.append(p.sum())
    return np.array(out)


def active_at(D, s, month):
    m = (D.sp_site == s) & (D.sp_a <= month) & (D.sp_b >= month)
    return month - D.sp_g[m]


def grants_recent(D, s, months=1):
    """Review grants a month over the last `months` months to September 2026; one month is the invitations since
    access became invitation-only on 1 September 2026."""
    hi = MIDX[(2026, 9)]
    return D.joins[s][hi - months + 1:hi + 1].mean()


def project_tenure(D, s, h, inflow=True, months=1):
    """Active reviewers October 2026 to December 2027: each reviewer active in September 2026 carried on the tenure
    curve from their own tenure, and the invitations still coming carried on it from tenure 0."""
    k = len(FWD_MONTHS)
    pool = survival_from(h, active_at(D, s, M_SEP26), k)
    if inflow:
        lam = grants_recent(D, s, months)
        S = np.concatenate([[1.0], np.cumprod(1.0 - h[:k])])
        pool = pool + np.array([lam * S[:j + 1].sum() for j in range(k)])
    return pool


def mixture_fit(D, lo=M_JAN24, hi=M_AUG26):
    """Two kinds of reviewer, each with its own steady monthly stop rate, fitted by maximum likelihood on the
    window's spells with each reviewer conditioned on being active when the record first sees them."""
    from scipy.optimize import minimize
    g, a, b, lp = D.sp_g, D.sp_a, D.sp_b, D.sp_lapsed
    start = np.maximum(a, lo)
    keep = np.minimum(b, hi) >= start
    t0 = (start - g)[keep]
    n = (np.minimum(b, hi) - start)[keep]
    ev = (lp & (b <= hi))[keep]

    def nll(x):
        p = 1 / (1 + math.exp(-x[0]))
        tc, ts = 1 / (1 + math.exp(-x[1])), 1 / (1 + math.exp(-x[2]))
        lc = np.log(p) + t0 * np.log1p(-tc) + n * np.log1p(-tc) + np.where(ev, np.log(tc), np.log1p(-tc))
        ls = np.log(1 - p) + t0 * np.log1p(-ts) + n * np.log1p(-ts) + np.where(ev, np.log(ts), np.log1p(-ts))
        num = np.logaddexp(lc, ls)
        den = np.logaddexp(np.log(p) + t0 * np.log1p(-tc), np.log(1 - p) + t0 * np.log1p(-ts))
        return -(num - den).sum()
    best = None
    for x0 in ((1.0, -2.0, -5.0), (0.0, -1.5, -4.5), (2.0, -2.5, -5.5)):
        r_ = minimize(nll, np.array(x0), method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-7, maxiter=4000))
        if best is None or r_.fun < best.fun:
            best = r_
    x = best.x
    return 1 / (1 + math.exp(-x[0])), 1 / (1 + math.exp(-x[1])), 1 / (1 + math.exp(-x[2]))


def project_mixture(D, s, fit, inflow=True, months=1):
    p, tc, ts = fit
    tau0 = active_at(D, s, M_SEP26)
    wc = p * (1 - tc) ** tau0
    ws = (1 - p) * (1 - ts) ** tau0
    wc, ws = wc / (wc + ws), ws / (wc + ws)
    k = np.arange(1, len(FWD_MONTHS) + 1)
    pool = np.array([(wc * (1 - tc) ** kk + ws * (1 - ts) ** kk).sum() for kk in k])
    if inflow:
        lam = grants_recent(D, s, months)
        S0 = lambda n: p * (1 - tc) ** n + (1 - p) * (1 - ts) ** n
        pool = pool + np.array([lam * sum(S0(j) for j in range(kk)) for kk in k])
    return pool


def arrivals(D, s, months=12):
    hi = MIDX[(2026, 9)]
    return D.joins[s][hi - months + 1:hi + 1].mean()


def ratios(D, s, lo=(2024, 1), hi=(2026, 9)):
    a, b = MIDX[lo], MIDX[hi]
    items = {t: D.ent[s][t][a:b + 1].sum() / D.q[s][a:b + 1].sum() for t in K.ITEMS}
    flag = D.flags[s][a:b + 1].sum() / D.q[s][a:b + 1].sum()
    return items, flag


def floor_share(D):
    """The routed share where the volunteers had room to spare (site-months with fewer than one item in 60 left
    unreviewed): the items no volunteer picks up."""
    num = den = 0.0
    for s in K.SITES:
        for i in range(len(HIST_MONTHS)):
            if D.ent_all[s][i] and D.rout_all[s][i] / D.ent_all[s][i] < 1 / 60.0:
                num += D.rout_all[s][i]
                den += D.ent_all[s][i]
    return num / den


def project_pool(D, s, mode="tenure", months=24, hz_mult=1.0, inflow=True):
    """Active reviewers for October 2026 to December 2027 (15 months). The golden is the tenure curve (`D.h`); the
    other modes are the rivals and checks: a flat exit rate over the last `months` months, or a log-linear trend of
    the pool."""
    if mode == "tenure":
        return project_tenure(D, s, D.h, inflow=inflow)
    R0 = D.R[s][MIDX[(2026, 9)]]
    if mode == "exits":
        h, _ = exit_rate(D, s, months)
        h *= hz_mult
        inf = arrivals(D, s) if inflow else 0.0
        out, x = [], R0
        for _ in FWD_MONTHS:
            x = x * (1 - h) + inf
            out.append(x)
        return np.array(out)
    lo = {"trend_all": MIDX[(2024, 1)], "trend12": MIDX[(2026, 9)] - 11, "trend21": MIDX[(2025, 1)],
          "trend18": MIDX[(2026, 9)] - 17}[mode]
    ts = np.arange(lo, MIDX[(2026, 9)] + 1)
    b = np.polyfit(ts, np.log(D.R[s][lo:MIDX[(2026, 9)] + 1]), 1)
    fut = np.arange(MIDX[(2026, 9)] + 1, MIDX[(2026, 9)] + 1 + len(FWD_MONTHS))
    return np.exp(np.polyval(b, fut))


def site_need(D, s, pace=None, pool=None, grain="monthly", ratio_lo=(2024, 1), floor=None):
    """2027 hours: handled flags and routed items at the 2027 standards; also October to December 2026 (2026
    standards) for the chart. Returns (hours by month for 2026-10..2027-12, 2027 hours)."""
    items, flag = ratios(D, s, ratio_lo)
    pace = pace if pace is not None else D.pace
    pool = pool if pool is not None else project_pool(D, s)
    floor = D.floor if floor is None else floor
    plan_fwd = []
    for (y, m) in FWD_MONTHS:
        if y == 2027:
            plan_fwd.append(D.plan[s][m - 1])
        else:
            plan_fwd.append(D.outlook[s][m - 10])
    plan_fwd = np.array(plan_fwd)
    A = plan_fwd * sum(items.values())
    cap = pool * pace
    if grain == "monthly":
        share = np.maximum(floor, 1 - cap / A)
    else:
        idx27 = [k for k, (y, m) in enumerate(FWD_MONTHS) if y == 2027]
        share27 = max(floor, 1 - cap[idx27].sum() / A[idx27].sum())
        share = np.maximum(floor, 1 - cap / A)
        share[idx27] = share27
    mix = {t: items[t] / sum(items.values()) for t in K.ITEMS}
    hours = []
    for k, (y, m) in enumerate(FWD_MONTHS):
        std = STD27 if y == 2027 else STD26
        mins = flag * plan_fwd[k] * std["flag"] + A[k] * share[k] * sum(mix[t] * std[t] for t in K.ITEMS)
        hours.append(mins / 60.0)
    hours = np.array(hours)
    h27 = hours[[k for k, (y, m) in enumerate(FWD_MONTHS) if y == 2027]].sum()
    return hours, h27


def history_hours(D, s):
    """Paid review hours by month, January 2024 to September 2026, at the standards in force (2026's)."""
    out = []
    for i in range(len(HIST_MONTHS)):
        mins = D.flags[s][i] * STD26["flag"] + sum(D.rout[s][t][i] * STD26[t] for t in K.ITEMS)
        out.append(mins / 60.0)
    return np.array(out)


def fte(h):
    return h / K.FTE_HOURS


# ------------------------------------------------------------------------------------------------- the rivals
def naive(D, s, window=12):
    hi = MIDX[(2026, 9)]
    lo = hi - window + 1
    mins = 0.0
    for i in range(lo, hi + 1):
        mins += D.flags[s][i] * STD27["flag"] + sum(D.rout[s][t][i] * STD27[t] for t in K.ITEMS)
    return mins / 60.0 / D.q[s][lo:hi + 1].sum() * D.plan[s].sum()


def share_trend(D, s):
    hi = MIDX[(2026, 9)]
    l12, p12 = slice(hi - 11, hi + 1), slice(hi - 23, hi - 11)
    s1 = D.rout_all[s][l12].sum() / D.ent_all[s][l12].sum()
    s0 = D.rout_all[s][p12].sum() / D.ent_all[s][p12].sum()
    s27 = max(D.floor, 2 * s1 - s0)
    items, flag = ratios(D, s, (2025, 10))
    mix = {t: items[t] / sum(items.values()) for t in K.ITEMS}
    plan = D.plan[s].sum()
    mins = flag * plan * STD27["flag"] + sum(items.values()) * plan * s27 * sum(mix[t] * STD27[t] for t in K.ITEMS)
    return mins / 60.0


def hours_trend(D, s):
    lo, hi = MIDX[(2025, 1)], MIDX[(2026, 9)]
    hh = []
    for i in range(lo, hi + 1):
        y, m = HIST_MONTHS[i]
        mins = D.flags[s][i] * STD27["flag"] + sum(D.rout[s][t][i] * STD27[t] for t in K.ITEMS)
        hh.append(mins / 60.0 / K.SEAS[m])
    b = np.polyfit(np.arange(lo, hi + 1), np.log(np.array(hh)), 1)
    tot = 0.0
    for k, (y, m) in enumerate(FWD_MONTHS):
        if y == 2027:
            tot += math.exp(np.polyval(b, hi + 1 + k)) * K.SEAS[m]
    return tot


def censored_pace(D, s):
    w = slice(MIDX[(2026, 1)], MIDX[(2026, 9)] + 1)
    return D.rev[s][w].sum() / D.R[s][w].sum()


# ------------------------------------------------------------------------------------------------- the asks
def ask_a(target):
    """Share of flags raised in July, August and September 2026 answered within 24 hours, by site and month."""
    p = lambda f: os.path.join(target, f)
    seen = {}
    for f in (R.F_FLAGS1, R.F_FLAGS2):
        for r in _rows(p(f)):
            seen[r["flag_id"]] = r          # the 15 August rows are the same rows in both parts
    first = {r["flag_id"]: r["first_action_at_utc"] for r in _rows(p(R.F_REVIEWS))}
    num, den = {}, {}
    for fid, r in seen.items():
        if r["outcome"] == "closed_post_deleted":
            continue
        raised = dt.datetime.fromisoformat(r["raised_at_utc"])
        act = dt.datetime.fromisoformat(first.get(fid, r["handled_at_utc"]))
        k = (r["site"], raised.month)
        den[k] = den.get(k, 0) + 1
        if act - raised <= dt.timedelta(hours=24):
            num[k] = num.get(k, 0) + 1
    return {k: 100.0 * num.get(k, 0) / den[k] for k in den}


def ask_b(target):
    """Hours worked by site and quarter, January to September 2026: approved lines, each shift to the site the
    moderator was assigned to on the shift's start day (HR), in the quarter of that day (Toronto time)."""
    p = lambda f: os.path.join(target, f)
    name_to_code = {K.SITE[c]["name"]: c for c in K.SITES}
    hist = {}
    for r in _rows(p(R.F_ASSIGN)):
        hist.setdefault(r["employee_no"], []).append((r["effective_from"], r["effective_to"] or "9999-12-31",
                                                      name_to_code[r["site"]]))
    out = {}
    for r in _rows(p(R.F_WFM)):
        if r["line_status"] != "approved":
            continue
        d = r["shift_date"]
        site = [c for a, b, c in hist[r["employee_no"]] if a <= d <= b]
        assert len(site) == 1, (r, hist[r["employee_no"]])
        qn = (int(d[5:7]) - 1) // 3 + 1
        k = (site[0], qn)
        out[k] = out.get(k, 0.0) + float(r["paid_hours"])
    return out


def ask_c(target, D=None):
    """Each site's questions in January to September 2026 as a percentage of the same months of 2022, each question
    once, on the site it is on today, in the month first asked."""
    p = lambda f: os.path.join(target, f)
    D = D or load(target)
    q26 = {s: D.q[s][MIDX[(2026, 1)]:MIDX[(2026, 9)] + 1].sum() for s in K.SITES}
    wb = {s: 0 for s in K.SITES}
    for (old, y, m), c in D.old.items():
        if y == 2022 and m <= 9:
            wb[OLD_TO_CODE[old]] += D.old_restated.get((old, y, m), c["q"])   # the rerun's count where it restated
    adj = {s: 0 for s in K.SITES}
    win = lambda t: t.year == 2022 and t.month <= 9
    for r in _rows(p(R.F_MOVES)):
        a = dt.datetime.fromisoformat(r["asked_at_utc"])
        b = dt.datetime.fromisoformat(r["moved_at_utc"])
        src, dst = OLD_TO_CODE[r["from_site"]], OLD_TO_CODE[r["to_site"]]
        if win(a):
            adj[src] -= 1            # the original stays in the source's count for the month it was asked
            adj[dst] += 1            # the question lives on the destination, in the month it was asked
        if win(b):
            adj[dst] -= 1            # the copy the old system counted at the destination in the month it moved
    q22 = {s: wb[s] + adj[s] for s in K.SITES}
    return {s: 100.0 * q26[s] / q22[s] for s in K.SITES}, q22, wb, q26


# ------------------------------------------------------------------------------------------------- everything
def compute(target):
    D = load(target)
    D.pace, D.n_sat = saturated_pace(D)
    D.floor = floor_share(D)
    D.ev, D.rk = tenure_counts(D)
    D.h = tenure_curve(D.ev, D.rk)
    D.fit = mixture_fit(D)
    X = Data()
    X.D = D
    X.need_h, X.need_fte, X.need_round, X.fwd_hours = {}, {}, {}, {}
    for s in K.SITES:
        hrs, h27 = site_need(D, s)
        X.fwd_hours[s] = hrs
        X.need_h[s] = h27
        X.need_fte[s] = fte(h27)
        X.need_round[s] = int(K.round_half_up(fte(h27)))
    X.request = sum(X.need_round.values())
    X.total_fte = sum(X.need_fte.values())
    X.gap = X.request - K.ENVELOPE_2027
    X.hist_hours = {s: history_hours(D, s) for s in K.SITES}
    X.ask_a = ask_a(target)
    X.ask_b = ask_b(target)
    X.ask_c, X.q22, X.q22_wb, X.q26 = ask_c(target, D)
    return X


def routes(X):
    """Every route the design names: per-site FTE and the rounded request under each. The rivals first (the ladder),
    then every defensible construction of the golden (the convergence set)."""
    D = X.D
    out = {}

    def req(f):
        v = {s: f(s) for s in K.SITES}
        return dict(fte=v, request=sum(int(K.round_half_up(x)) for x in v.values()), total=sum(v.values()))

    def with_pool(pools, **kw):
        return req(lambda s: fte(site_need(D, s, pool=pools[s], **kw)[1]))

    out["golden"] = req(lambda s: X.need_fte[s])
    # the rivals
    out["naive12"] = req(lambda s: fte(naive(D, s, 12)))
    out["naive9"] = req(lambda s: fte(naive(D, s, 9)))
    out["share_trend"] = req(lambda s: fte(share_trend(D, s)))
    out["hours_trend"] = req(lambda s: fte(hours_trend(D, s)))
    out["pace_censored"] = req(lambda s: fte(site_need(D, s, pace=censored_pace(D, s))[1]))
    for n in (24, 12, 3):
        out["flat%d" % n] = with_pool({s: project_pool(D, s, "exits", n, inflow=False) for s in K.SITES})
    out["flat24_open"] = with_pool({s: project_pool(D, s, "exits", 24) for s in K.SITES})
    out["pool_trend_all"] = with_pool({s: project_pool(D, s, "trend_all") for s in K.SITES})
    out["pool_trend12"] = with_pool({s: project_pool(D, s, "trend12") for s in K.SITES})
    ev, rk = tenure_counts(D, trunc=False)
    out["no_truncation"] = with_pool({s: project_tenure(D, s, tenure_curve(ev, rk)) for s in K.SITES})
    # the convergent constructions
    for band in (3, 6, 12):
        h = tenure_curve(D.ev, D.rk, band=band)
        out["band%d" % band] = with_pool({s: project_tenure(D, s, h) for s in K.SITES})
    own = {}
    for s in K.SITES:
        e, r = tenure_counts(D, sites=[s])
        own[s] = project_tenure(D, s, tenure_curve(e, r))
    out["own_site_curve"] = with_pool(own)
    e, r = tenure_counts(D, shift=2)
    out["lapse_date"] = with_pool({s: project_tenure(D, s, tenure_curve(e, r)) for s in K.SITES})
    for lo, tag in ((M_AUG26 - 23, "window24"), (M_AUG26 - 17, "window18")):
        e, r = tenure_counts(D, lo=lo)
        out[tag] = with_pool({s: project_tenure(D, s, tenure_curve(e, r)) for s in K.SITES})
    for tail in (6, 24):
        h = tenure_curve(D.ev, D.rk, tail=tail)
        out["tail%d" % tail] = with_pool({s: project_tenure(D, s, h) for s in K.SITES})
    out["no_invitations"] = with_pool({s: project_tenure(D, s, D.h, inflow=False) for s in K.SITES})
    out["mixture"] = with_pool({s: project_mixture(D, s, D.fit) for s in K.SITES})
    se = 1.0 / math.sqrt(D.ev.sum())
    for sign, tag in ((1, "plus"), (-1, "minus")):
        out["curve_1se_" + tag] = with_pool({s: project_tenure(D, s, D.h * (1 + sign * se)) for s in K.SITES})
    out["annual"] = req(lambda s: fte(site_need(D, s, grain="annual")[1]))
    for cut in (0.01, 0.02, 0.10, 0.15):
        pc, _ = saturated_pace(D, cut)
        out["pace_cut_%02d" % int(cut * 100)] = req(lambda s, pc=pc: fte(site_need(D, s, pace=pc)[1]))
    po, _ = saturated_pace(D, use_new=False)
    pn, _ = saturated_pace(D, use_old=False)
    out["pace_old_only"] = req(lambda s: fte(site_need(D, s, pace=po)[1]))
    out["pace_new_only"] = req(lambda s: fte(site_need(D, s, pace=pn)[1]))
    out["ratios_2025"] = req(lambda s: fte(site_need(D, s, ratio_lo=(2025, 1))[1]))
    out["floor_zero"] = req(lambda s: fte(site_need(D, s, floor=0.0)[1]))
    return out
