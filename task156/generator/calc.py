"""task156 calculations from the shipped files only (the bundle under target/), never from the world.

The golden: each site's 2027 need is its handled flags at the plan's questions times the site's flag rate, plus its
routed community items, each 2027 month's inbox arrivals (the plan's questions times the site's items per question)
less what its reviewer pool can review: the pool carried from September 2026 at the exit rate the roster shows and the
reviewers still arriving, each reviewer at the reviews a month reviewers complete when the inbox outruns them. Every
other route the design names is computed here too, for the checks."""
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
    old = {}
    for name, rows in read_xlsx(p(R.F_OLD)).items():
        head = None
        for row in rows:
            if row and row[0] == "Site":
                head = list(row)
                continue
            if head and row and row[0] in OLD_TO_CODE and row[1]:
                rec = dict(zip(head, row))
                y = int(name)
                m = K.MON3.index(str(rec["Month"])[:3])
                ent_ = sum(int(rec[c]) for c in head if c and c.endswith(" in"))
                rout_ = sum(int(rec[c]) for c in head if c and c.endswith(" to moderators"))
                old[(row[0], y, m)] = dict(ent=ent_, rout=rout_, R=int(rec["Active reviewers"]),
                                           vol=int(rec["Volunteer reviews"]), q=int(rec["Questions"]))
    D.old = old
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


def project_pool(D, s, mode="exits", months=24, hz_mult=1.0, inflow=True):
    """Active reviewers for October 2026 to December 2027 (15 months)."""
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
            wb[OLD_TO_CODE[old]] += c["q"]
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
    """Every route the design names: per-site FTE and the rounded request under each."""
    D = X.D
    out = {}

    def req(f):
        v = {s: f(s) for s in K.SITES}
        return dict(fte=v, request=sum(int(K.round_half_up(x)) for x in v.values()), total=sum(v.values()))

    out["golden"] = req(lambda s: X.need_fte[s])
    out["naive12"] = req(lambda s: fte(naive(D, s, 12)))
    out["naive9"] = req(lambda s: fte(naive(D, s, 9)))
    out["share_trend"] = req(lambda s: fte(share_trend(D, s)))
    out["hours_trend"] = req(lambda s: fte(hours_trend(D, s)))
    out["pool_trend_all"] = req(lambda s: fte(site_need(D, s, pool=project_pool(D, s, "trend_all"))[1]))
    out["pace_censored"] = req(lambda s: fte(site_need(D, s, pace=censored_pace(D, s))[1]))
    out["pace_censored_trend_all"] = req(lambda s: fte(site_need(D, s, pace=censored_pace(D, s),
                                                                pool=project_pool(D, s, "trend_all"))[1]))
    # the convergent constructions
    out["exits12"] = req(lambda s: fte(site_need(D, s, pool=project_pool(D, s, "exits", 12))[1]))
    out["exits18"] = req(lambda s: fte(site_need(D, s, pool=project_pool(D, s, "exits", 18))[1]))
    out["trend12"] = req(lambda s: fte(site_need(D, s, pool=project_pool(D, s, "trend12"))[1]))
    out["trend18"] = req(lambda s: fte(site_need(D, s, pool=project_pool(D, s, "trend18"))[1]))
    out["trend21"] = req(lambda s: fte(site_need(D, s, pool=project_pool(D, s, "trend21"))[1]))
    out["no_inflow"] = req(lambda s: fte(site_need(D, s, pool=project_pool(D, s, inflow=False))[1]))
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
    for sign, tag in ((1, "plus"), (-1, "minus")):
        def f(s, sign=sign):
            _, ex = exit_rate(D, s)
            return fte(site_need(D, s, pool=project_pool(D, s, hz_mult=1 + sign / math.sqrt(ex)))[1])
        out["exit_1se_" + tag] = req(f)
    return out
