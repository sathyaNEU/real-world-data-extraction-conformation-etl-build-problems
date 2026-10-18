"""task162 golden from the shipped files only: the first-quarter forecast (every rung, the decisive restart model and
its variants, the out-of-sample check on the record's releases), the parallel-run asks (the golden and the cracker's
and the mirror's routes) and the pair ceiling. Reads <target>; never imports the world."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
F_EXPORT = "old_tracker_export_20251001_20261217.csv"
F_SHARES = "version_share_daily.csv"
F_INSTALLS = "active_installs_daily.csv"
F_DASH = "triage_dashboard_weekly.xlsx"
F_CALENDAR = "release_calendar_2025_2027.pdf"
F_NEWEXPORT = "newtracker_parallel_run_export.json"
F_GROUPS = "component_groups.xlsx"
F_ROTA = "triage_rota_2026-11.xlsx"
F_AGREEMENT = "triage_working_agreement.docx"

PLATFORMS = ("Windows", "macOS", "Linux")
Q1_START = dt.date(2027, 1, 4)
Q1_WEEKS = [Q1_START + dt.timedelta(days=7 * k) for k in range(13)]
STD = 120
RECORD_START = dt.date(2025, 10, 1)
LAST_DAY = dt.date(2026, 12, 17)


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def second_tuesday(y, m):
    d = dt.date(y, m, 1)
    while d.weekday() != 1:
        d += dt.timedelta(1)
    return d + dt.timedelta(7)


PATCH_TUESDAYS = sorted(second_tuesday(y, m) for y in range(2025, 2028) for m in range(1, 13))


def year_end(d):
    return (d.month == 12 and d.day >= 21) or (d.month == 1 and d.day <= 3)


def rd(target, f):
    with open(os.path.join(target, f), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def platform_of(op_sys):
    return "Windows" if op_sys.startswith("Windows") else "macOS" if op_sys.startswith("macOS") else "Linux"


# ------------------------------------------------------------------------------------------------------- loading
class Data:
    pass


def calendar_dates(target):
    """(major, release date) from the release calendar's table (pdfplumber)."""
    import pdfplumber
    out = []
    with pdfplumber.open(os.path.join(target, F_CALENDAR)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not row or not row[0] or not re.match(r"^\d+\.0$", row[0].strip()):
                        continue
                    d, m, y = (int(v) for v in row[2].strip().split("."))
                    out.append((int(row[0].split(".")[0]), dt.date(y, m, d)))
    return sorted(out)


def load(target):
    D = Data()
    D.target = target
    D.export = rd(target, F_EXPORT)
    D.days = [RECORD_START + dt.timedelta(days=i) for i in range((LAST_DAY - RECORD_START).days + 1)]
    D.di = {d: i for i, d in enumerate(D.days)}
    n = len(D.days)
    # daily triage items (every report, duplicates included, the security group out) by platform
    D.y = {p: np.zeros(n) for p in PLATFORMS}
    D.y_all = np.zeros(n)
    D.y_sec = np.zeros(n)
    for r in D.export:
        d = dt.date(int(r["opened"][:4]), int(r["opened"][5:7]), int(r["opened"][8:10]))
        i = D.di[d]
        if r["groups"] == "core-security":
            D.y_sec[i] += 1
            continue
        D.y[platform_of(r["op_sys"])][i] += 1
        D.y_all[i] += 1
    # the portal
    D.inst = {p: np.zeros(n) for p in PLATFORMS}
    for r in rd(target, F_INSTALLS):
        d = dt.date.fromisoformat(r["date"])
        D.inst[r["platform"]][D.di[d]] = 1000.0 * int(r["active_installs_thousands"])
    D.share = {p: [dict() for _ in range(n)] for p in PLATFORMS}
    for r in rd(target, F_SHARES):
        d = dt.date.fromisoformat(r["date"])
        D.share[r["platform"]][D.di[d]][r["version"]] = float(r["share_pct"]) / 100.0
    D.releases = calendar_dates(target)
    D.rel_date = dict(D.releases)
    return D


def major_share(D, p, i, m):
    return sum(s for v, s in D.share[p][i].items() if v != "older" and int(v.split(".")[0]) == m)


def weekly(D, arr, start=None, end=None):
    """Sums of a daily array over Monday-to-Sunday weeks fully inside the record."""
    out = {}
    for i, d in enumerate(D.days):
        w = monday(d)
        out.setdefault(w, [0.0, 0])
        out[w][0] += arr[i]
        out[w][1] += 1
    return {w: v[0] for w, v in out.items() if v[1] == 7 and (start is None or w >= start) and (end is None or w <= end)}


# ------------------------------------------------------------------------------------------------------- adoption
def reach_series(D):
    """Per platform: the share of active installs reaching the newest major each day (its share's rise), the share
    still pending before the day, and which major is newest."""
    n = len(D.days)
    R = {}
    rel = [(m, d) for m, d in D.releases if RECORD_START <= d <= LAST_DAY]
    for p in PLATFORMS:
        reach = np.zeros(n)
        pend = np.full(n, np.nan)
        newest = np.zeros(n, dtype=int)
        for k, (m, d0) in enumerate(rel):
            d1 = rel[k + 1][1] if k + 1 < len(rel) else LAST_DAY + dt.timedelta(days=1)
            i0 = D.di[d0]
            prev = major_share(D, p, i0 - 1, m) if i0 > 0 else 0.0
            for d in (D.days[j] for j in range(i0, D.di.get(d1, n))):
                i = D.di[d]
                s = major_share(D, p, i, m)
                reach[i] = max(0.0, s - prev)
                pend[i] = 1.0 - prev
                newest[i] = m
                prev = s
        R[p] = dict(reach=reach, pend=pend, newest=newest)
    return R


def day_type(D, d, p):
    """The day's kind for the restart model: the release day (the update out at 16:00), the Wednesday and Thursday
    after Patch Tuesday on Windows, a weekend day, a year-end day or an ordinary weekday."""
    if d in D.rel_date.values():
        return "release"
    if p == "Windows":
        for pt in PATCH_TUESDAYS:
            k = (d - pt).days
            if k == 1:
                return "burst1"
            if k == 2:
                return "burst2"
    if year_end(d):
        return "yearend_we" if d.weekday() >= 5 else "yearend"
    return "weekend" if d.weekday() >= 5 else "weekday"


def hazards(D, R, majors=None, stat="mean"):
    """The share of still-pending installs that update on each kind of day, per platform, from the record's releases
    (majors: which releases; default every release in the record)."""
    H = {}
    for p in PLATFORMS:
        vals = {}
        for i, d in enumerate(D.days):
            m = R[p]["newest"][i]
            if m == 0 or (majors is not None and m not in majors):
                continue
            pend = R[p]["pend"][i]
            if not pend or pend < 0.03:
                continue
            vals.setdefault(day_type(D, d, p), []).append(R[p]["reach"][i] / pend)
        H[p] = {k: (float(np.mean(v)) if stat == "mean" else float(np.median(v))) for k, v in vals.items()}
    return H


def simulate_adoption(D, H, release, days, p, start_pending=1.0):
    """The share of installs reaching a release each day from its release day, under hazards H."""
    pend = start_pending
    out = []
    for d in days:
        if d < release:
            out.append(0.0)
            continue
        kind = day_type_forward(d, p, release)
        h = H[p].get(kind, H[p]["weekday"])
        a = pend * h
        pend -= a
        out.append(a)
    return np.array(out)


def day_type_forward(d, p, release):
    if d == release:
        return "release"
    if p == "Windows":
        for pt in PATCH_TUESDAYS:
            k = (d - pt).days
            if k == 1:
                return "burst1"
            if k == 2:
                return "burst2"
    if year_end(d):
        return "yearend_we" if d.weekday() >= 5 else "yearend"
    return "weekend" if d.weekday() >= 5 else "weekday"


# ------------------------------------------------------------------------------------------------------- reports model
def fit_reports(D, R, lags=6, mode="platform", window=None):
    """The record's triage items on the installs and the installs reaching the newest version: a baseline per active
    install plus first-use reports per reaching install spread over the days after it reached (a distributed lag), by
    least squares. mode platform: daily rows per platform, a baseline per platform; total: daily rows of the three
    platforms together; weekly: weekly totals with the reach of the week and of the week before."""
    if mode == "weekly":
        reach_tot = sum(R[p]["reach"] * D.inst[p] for p in PLATFORMS)
        inst_tot = sum(D.inst[p] for p in PLATFORMS)
        wy, wi, wr = weekly(D, D.y_all), weekly(D, inst_tot), weekly(D, reach_tot)
        ws = sorted(w for w in wy if w - dt.timedelta(days=7) in wr and (not window or window[0] <= w <= window[1]))
        X = np.array([[wi[w] / 1e6, wr[w] / 1e3, wr[w - dt.timedelta(days=7)] / 1e3] for w in ws])
        y = np.array([wy[w] for w in ws])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        cov = hc0(X, y, beta)
        return dict(mode=mode, base={p: beta[0] / 1e6 for p in PLATFORMS}, kern=beta[1:] / 1e3,
                    rho=float(beta[1:].sum() / 1e3), cov=cov, scale=np.array([1e6, 1e3, 1e3]), n=len(y))
    rows, ys = [], []
    groups = [(p,) for p in PLATFORMS] if mode == "platform" else [PLATFORMS]
    for g in groups:
        reach_inst = sum(R[p]["reach"] * D.inst[p] for p in g)
        inst = sum(D.inst[p] for p in g)
        yy = sum(D.y[p] for p in g)
        for i in range(lags, len(D.days)):
            d = D.days[i]
            if window and not (window[0] <= d <= window[1]):
                continue
            x = [0.0] * len(groups)
            x[groups.index(g)] = inst[i] / 1e6
            x += [reach_inst[i - k] / 1e3 for k in range(lags)]
            rows.append(x)
            ys.append(yy[i])
    X = np.array(rows)
    y = np.array(ys)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    nb = len(groups)
    if mode == "platform":
        base = {p: beta[k] / 1e6 for k, p in enumerate(PLATFORMS)}
    else:
        base = {p: beta[0] / 1e6 for p in PLATFORMS}
    cov = hc0(X, y, beta)
    return dict(mode=mode, base=base, kern=beta[nb:] / 1e3, rho=float(beta[nb:].sum() / 1e3), cov=cov,
                scale=np.array([1e6] * nb + [1e3] * lags), n=len(y))


def hc0(X, y, beta):
    """Heteroskedasticity-robust covariance of the least-squares coefficients (the counts are Poisson-like)."""
    e = y - X @ beta
    XtX = np.linalg.inv(X.T @ X)
    return XtX @ (X.T * e ** 2) @ X @ XtX


def project_installs(D, days, lag=364, growth_window=56):
    """Active installs on forward days: the same weekday a year earlier, times each platform's growth over the last
    eight weeks against the same weeks a year earlier."""
    out = {}
    for p in PLATFORMS:
        a = D.inst[p][-growth_window:].sum()
        b = D.inst[p][-growth_window - lag:-lag].sum()
        g = a / b
        out[p] = np.array([D.inst[p][D.di[d - dt.timedelta(days=lag)]] * g for d in days])
    return out


def forward_days():
    start = LAST_DAY + dt.timedelta(days=1)
    return [start + dt.timedelta(days=i) for i in range((Q1_WEEKS[-1] + dt.timedelta(days=6) - start).days + 1)]


def forward_reach(D, R, H):
    """Per platform and forward day: the share of installs reaching the newest version (the version newest at the
    as-of keeps adopting until the first-quarter release; each release from its release day)."""
    days = forward_days()
    fwd = [(m, d) for m, d in D.releases if LAST_DAY < d <= days[-1]]
    last_m = max(m for m, d in D.releases if d <= LAST_DAY)
    out = {}
    for p in PLATFORMS:
        reach = np.zeros(len(days))
        segs = [(last_m, days[0], 1.0 - major_share(D, p, len(D.days) - 1, last_m))] + [(m, d, 1.0) for m, d in fwd]
        for k, (m, d0, p0) in enumerate(segs):
            d1 = segs[k + 1][1] if k + 1 < len(segs) else days[-1] + dt.timedelta(days=1)
            pend = p0
            for i, d in enumerate(days):
                if not (d0 <= d < d1):
                    continue
                kind = "release" if (m != last_m and d == d0) else day_type_forward(d, p, None)
                h = H[p].get(kind, H[p]["weekday"])
                reach[i] = pend * h
                pend -= reach[i]
        out[p] = reach
    return days, out


def apply_reports(D, R, fit, days, reach, inst):
    """Weekly triage items for the forward window from the fitted reports model."""
    if fit["mode"] == "weekly":
        reach_tot = sum(reach[p] * inst[p] for p in PLATFORMS)
        inst_tot = sum(inst[p] for p in PLATFORMS)
        hist_tot = sum(R[p]["reach"] * D.inst[p] for p in PLATFORMS)
        wr = {}
        for i, d in enumerate(D.days):
            wr[monday(d)] = wr.get(monday(d), 0.0) + hist_tot[i]
        wi = {}
        for i, d in enumerate(days):
            w = monday(d)
            wr[w] = wr.get(w, 0.0) + reach_tot[i] if d > LAST_DAY else wr.get(w, 0.0)
            wi[w] = wi.get(w, 0.0) + inst_tot[i]
        return {w: fit["base"]["Windows"] * wi[w] + fit["kern"][0] * wr[w] + fit["kern"][1] * wr[w - dt.timedelta(days=7)]
                for w in Q1_WEEKS}
    lags = len(fit["kern"])
    tot = np.zeros(len(days))
    for p in PLATFORMS:
        hist = R[p]["reach"][-lags:] * D.inst[p][-lags:]
        full = np.concatenate([hist, reach[p] * inst[p]])
        fu = np.array([sum(fit["kern"][k] * full[lags + i - k] for k in range(lags)) for i in range(len(days))])
        tot += fit["base"][p] * inst[p] + fu
    wk = {}
    for i, d in enumerate(days):
        w = monday(d)
        if w in Q1_WEEKS:
            wk[w] = wk.get(w, 0.0) + tot[i]
    return wk


def forecast(D, opt=None):
    """The decisive model: each first-quarter release's adoption from the record's restart hazards (the Windows burst
    on the Wednesday and Thursday after Patch Tuesday), carried through the fitted reports model."""
    opt = dict(opt or {})
    R = reach_series(D)
    H = hazards(D, R, majors=opt.get("majors"), stat=opt.get("stat", "mean"))
    fit = fit_reports(D, R, lags=opt.get("lags", 6), mode=opt.get("mode", "platform"), window=opt.get("window"))
    days, reach = forward_reach(D, R, H)
    inst = project_installs(D, days, growth_window=opt.get("growth_window", 56))
    wk = apply_reports(D, R, fit, days, reach, inst)
    busiest = max(wk, key=wk.get)
    out = dict(weeks=wk, busiest_week=busiest, busiest=wk[busiest], triagers=math.ceil(wk[busiest] / STD), H=H,
               fit=fit)
    out["sigma"] = forecast_sigma(D, R, fit, days, reach, inst, busiest)
    return out


def forecast_sigma(D, R, fit, days, reach, inst, week):
    """One standard error of the busiest week's forecast from the reports model's coefficients (robust covariance)."""
    k = len(fit["cov"])
    base = apply_reports(D, R, fit, days, reach, inst)[week]
    g = np.zeros(k)
    eps = 1e-3
    for j in range(k):
        f2 = dict(fit)
        b = np.concatenate([[fit["base"][p] for p in PLATFORMS] if fit["mode"] == "platform" else [fit["base"]["Windows"]],
                            fit["kern"]])
        b = b * 1.0
        b[j] += eps / fit["scale"][j]
        nb = 3 if fit["mode"] == "platform" else 1
        f2["base"] = ({p: b[i] for i, p in enumerate(PLATFORMS)} if fit["mode"] == "platform"
                      else {p: b[0] for p in PLATFORMS})
        f2["kern"] = b[nb:]
        g[j] = (apply_reports(D, R, f2, days, reach, inst)[week] - base) / eps
    return float(math.sqrt(g @ fit["cov"] @ g))


# ------------------------------------------------------------------------------------------------------- the rungs
def weekly_items(D):
    return weekly(D, D.y_all)


def install_growth(D, window=56, lag=364):
    a = sum(D.inst[p][-window:].sum() for p in PLATFORMS)
    b = sum(D.inst[p][-window - lag:-lag].sum() for p in PLATFORMS)
    return a / b


def rung_default(D):
    """R1: last year's busiest first-quarter week on the new counting, scaled by the growth in active installs."""
    wk = weekly_items(D)
    q1 = {w: v for w, v in wk.items() if dt.date(2026, 1, 5) <= w <= dt.date(2026, 3, 30)}
    w = max(q1, key=q1.get)
    v = q1[w] * install_growth(D)
    return dict(week=w, last_year=q1[w], busiest=v, triagers=math.ceil(v / STD))


def rung_dashboard(D):
    """R0: the old dashboard's busiest first-quarter 2026 week, scaled by install growth."""
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(D.target, F_DASH), read_only=True, data_only=False)
    ws = wb["Weekly"]
    best = None
    for row in ws.iter_rows(min_row=6, values_only=True):
        if not isinstance(row[0], dt.datetime):
            continue
        w = row[0].date()
        tot = sum(v for v in row[1:7] if isinstance(v, (int, float)))
        if dt.date(2026, 1, 5) <= w <= dt.date(2026, 3, 30) and (best is None or tot > best[1]):
            best = (w, tot)
    wb.close()
    v = best[1] * install_growth(D)
    return dict(week=best[0], dashboard=best[1], busiest=v, triagers=math.ceil(v / STD))


def rung_record_max(D):
    wk = weekly_items(D)
    w = max(wk, key=wk.get)
    v = wk[w] * install_growth(D)
    return dict(week=w, busiest=v, triagers=math.ceil(v / STD))


def rung_last_quarter(D):
    wk = weekly_items(D)
    q4 = {w: v for w, v in wk.items() if w >= dt.date(2026, 9, 28)}
    w = max(q4, key=q4.get)
    v = q4[w] * install_growth(D, window=56, lag=364) ** 0.25
    return dict(week=w, busiest=v, triagers=math.ceil(v / STD))


def rung_per_install_max(D):
    """The record's busiest week per active install, on the first quarter's busiest projected installs."""
    inst = sum(D.inst[p] for p in PLATFORMS)
    wk = weekly_items(D)
    wi = weekly(D, inst)
    w = max(wk, key=lambda w: wk[w] / wi[w])
    start = LAST_DAY + dt.timedelta(days=1)
    days = [start + dt.timedelta(days=i) for i in range((Q1_WEEKS[-1] + dt.timedelta(days=6) - start).days + 1)]
    pi = project_installs(D, days)
    q = {}
    for i, d in enumerate(days):
        m = monday(d)
        if m in Q1_WEEKS:
            q[m] = q.get(m, 0.0) + sum(pi[p][i] for p in PLATFORMS)
    v = max(wk[w] / wi[w] * q[m] for m in Q1_WEEKS)
    return dict(week=w, busiest=v, triagers=math.ceil(v / STD))


def profile_model(D, majors=None):
    """R2a: the record's release-week profile: each week's items over the reports model's baseline, by week since the
    release, per active install, averaged over the record's releases, on the first quarter's baseline."""
    R = reach_series(D)
    fit = fit_reports(D, R)
    base = sum(fit["base"][p] * D.inst[p] for p in PLATFORMS)
    wk_y = weekly(D, D.y_all)
    wk_b = weekly(D, base)
    wk_i = weekly(D, sum(D.inst[p] for p in PLATFORMS))
    rel = [(m, d) for m, d in D.releases if RECORD_START + dt.timedelta(days=7) <= d <= dt.date(2026, 11, 3)]
    if majors is not None:
        rel = [(m, d) for m, d in rel if m in majors]
    prof = np.zeros(4)
    for m, d in rel:
        w0 = monday(d)
        for k in range(4):
            w = w0 + dt.timedelta(days=7 * k)
            prof[k] += (wk_y[w] - wk_b[w]) / wk_i[w]
    prof /= len(rel)
    start = LAST_DAY + dt.timedelta(days=1)
    days = [start + dt.timedelta(days=i) for i in range((Q1_WEEKS[-1] + dt.timedelta(days=6) - start).days + 1)]
    pi = project_installs(D, days)
    qb, qi = {}, {}
    for i, d in enumerate(days):
        m = monday(d)
        if m in Q1_WEEKS:
            qb[m] = qb.get(m, 0.0) + sum(fit["base"][p] * pi[p][i] for p in PLATFORMS)
            qi[m] = qi.get(m, 0.0) + sum(pi[p][i] for p in PLATFORMS)
    q = dict(qb)
    for mj, d in D.releases:
        if Q1_WEEKS[0] <= d <= Q1_WEEKS[-1] + dt.timedelta(days=6):
            w0 = monday(d)
            for k in range(4):
                w = w0 + dt.timedelta(days=7 * k)
                if w in q:
                    q[w] += prof[k] * qi[w]
    w = max(q, key=q.get)
    return dict(week=w, busiest=q[w], triagers=math.ceil(q[w] / STD), profile=prof.tolist())


def uplift_model(D):
    """R2b: the 1 December release's busiest week over its week before, on each first-quarter release's week before
    (last year's week before the release in the same place in the train, scaled for growth)."""
    wk = weekly(D, D.y_all)
    w0 = monday(D.rel_date[48])
    pre = wk[w0 - dt.timedelta(days=7)]
    peak = max(wk[w0], wk.get(w0 + dt.timedelta(days=7), 0))
    ratio = peak / pre
    g = install_growth(D)
    best = None
    for m in (49, 50, 51):
        ly = monday(D.rel_date[m - 12]) - dt.timedelta(days=7)
        v = wk[ly] * g * ratio
        if best is None or v > best[1]:
            best = (m, v)
    return dict(ratio=ratio, release=best[0], busiest=best[1], triagers=math.ceil(best[1] / STD))


def typical_reach_model(D):
    """R2c: the exposure model with the record's typical release-week reach: each first-quarter release reaches, in
    its release week and the weeks after, the shares the record's releases reached on average."""
    R = reach_series(D)
    fit = fit_reports(D, R)
    rel = [(m, d) for m, d in D.releases if RECORD_START + dt.timedelta(days=7) <= d <= dt.date(2026, 11, 3)]
    prof = {p: np.zeros(28) for p in PLATFORMS}
    for m, d in rel:
        i0 = D.di[d]
        for p in PLATFORMS:
            prof[p] += R[p]["reach"][i0:i0 + 28] / len(rel)
    start = LAST_DAY + dt.timedelta(days=1)
    days = [start + dt.timedelta(days=i) for i in range((Q1_WEEKS[-1] + dt.timedelta(days=6) - start).days + 1)]
    pi = project_installs(D, days)
    lags = len(fit["kern"])
    tot = np.zeros(len(days))
    fwd = [(m, d) for m, d in D.releases if Q1_WEEKS[0] <= d <= Q1_WEEKS[-1] + dt.timedelta(days=6)]
    for p in PLATFORMS:
        reach = np.zeros(len(days))
        for m, d in fwd:
            i0 = days.index(d)
            for k in range(28):
                if i0 + k < len(days):
                    reach[i0 + k] += prof[p][k]
        ri = reach * pi[p]
        full = np.concatenate([np.zeros(lags), ri])
        fu = np.array([sum(fit["kern"][k] * full[lags + i - k] for k in range(lags)) for i in range(len(days))])
        tot += fit["base"][p] * pi[p] + fu
    wk = {}
    for i, d in enumerate(days):
        w = monday(d)
        if w in Q1_WEEKS:
            wk[w] = wk.get(w, 0.0) + tot[i]
    w = max(wk, key=wk.get)
    return dict(week=w, busiest=wk[w], triagers=math.ceil(wk[w] / STD))


def oos(D):
    """Out of sample on the record's two releases shipped two weeks before Patch Tuesday (29 September and 27 October
    2026): the release-week profile and the restart model, each fitted on the other releases, against the weeks the
    two releases actually brought (items over the baseline, weeks 0 to 3)."""
    R = reach_series(D)
    late = [46, 47]
    fit = fit_reports(D, R)
    base = sum(fit["base"][p] * D.inst[p] for p in PLATFORMS)
    wk_y = weekly(D, D.y_all)
    wk_b = weekly(D, base)
    wk_i = weekly(D, sum(D.inst[p] for p in PLATFORMS))
    early = [m for m, d in D.releases if RECORD_START + dt.timedelta(days=7) <= d <= dt.date(2026, 9, 1)]
    prof = np.zeros(4)
    for m in early:
        w0 = monday(D.rel_date[m])
        for k in range(4):
            w = w0 + dt.timedelta(days=7 * k)
            prof[k] += (wk_y[w] - wk_b[w]) / wk_i[w]
    prof /= len(early)
    H = hazards(D, R, majors=set(early))
    out = {}
    for m in late:
        d0 = D.rel_date[m]
        w0 = monday(d0)
        nxt = D.rel_date[m + 1]
        seg = [d for d in D.days if d0 <= d < nxt]
        excess_model = {}
        lags = len(fit["kern"])
        fu_total = np.zeros(len(D.days))
        for p in PLATFORMS:
            pend0 = R[p]["pend"][D.di[d0]]
            a = simulate_adoption(D, H, d0, seg, p, start_pending=pend0)
            ri = np.zeros(len(D.days))
            for d, x in zip(seg, a):
                ri[D.di[d]] = x * D.inst[p][D.di[d]]
            for i in range(len(D.days)):
                fu_total[i] += sum(fit["kern"][k] * ri[i - k] for k in range(lags) if i - k >= 0)
        wk_fu = weekly(D, fu_total)
        rows = []
        for k in range(4):
            w = w0 + dt.timedelta(days=7 * k)
            actual = wk_y[w] - wk_b[w]
            rows.append(dict(week=w, actual=actual, profile=prof[k] * wk_i[w], restart=wk_fu[w]))
        out[m] = rows
    return out


# ------------------------------------------------------------------------------------------------------- the asks
RUN_FROM = dt.datetime(2026, 11, 2, 0, 0)
RUN_TO = dt.datetime(2026, 11, 30, 0, 0)
RUN_WEEKS = [dt.date(2026, 11, 2) + dt.timedelta(days=7 * k) for k in range(4)]
GROUPS = ["Rendering and Layout", "Graphics and Media", "Networking", "Script and Web APIs", "Browser Interface",
          "Extensions", "Developer Tools", "Platform and Updates"]
TRIAGE_FIELDS = ("status", "resolution", "Component", "priority")
CLOSED = ("Resolved", "Closed")


def jt(s):
    """A new-tracker timestamp (UTC) as Helsinki local time (EET in November, UTC+2)."""
    u = dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
    return u + dt.timedelta(hours=2)


def load_asks(target, D=None):
    import openpyxl
    A = Data()
    with open(os.path.join(target, F_NEWEXPORT), encoding="utf-8") as fh:
        A.issues = json.load(fh)["issues"]
    wb = openpyxl.load_workbook(os.path.join(target, F_ROTA), read_only=True)
    names = set()
    for row in wb["Rota"].iter_rows(min_row=4, values_only=True):
        if row[3]:
            names |= {x.strip() for x in str(row[3]).split(",")}
    wb.close()
    A.triagers = names
    wb = openpyxl.load_workbook(os.path.join(target, F_GROUPS), read_only=True)
    A.group = {}
    for row in wb["Component groups"].iter_rows(min_row=5, values_only=True):
        if row[0] in GROUPS and row[1]:
            A.group[row[1]] = row[0]
    wb.close()
    A.opened = {}
    for r in (D.export if D is not None else rd(target, F_EXPORT)):
        A.opened[int(r["bug_id"])] = dt.datetime.strptime(r["opened"], "%Y-%m-%d %H:%M:%S")
    return A


def issue_view(i):
    """The parts of an issue the asks read: its histories in time order (Helsinki), and its components at creation
    (the current components with every later component change undone)."""
    f = i["fields"]
    hs = sorted(i["changelog"]["histories"], key=lambda h: (h["created"], int(h["id"])))
    comps = {c["name"] for c in f["components"]}
    for h in reversed(hs):
        for it in reversed(h["items"]):
            if it["field"] == "Component":
                if it["toString"]:
                    comps.discard(it["toString"])
                if it["fromString"]:
                    comps.add(it["fromString"])
    return hs, comps


def legacy_id(i, key):
    """The old bug number an issue was copied from: the Legacy bug field; with key all, also the value the bridge wrote
    into the field (a move to WEBC drops it from the field, not from the changelog) and the label a catch-up copy
    carries instead (legacy-NNNNNNN)."""
    v = i["fields"].get("customfield_10410")
    if v is not None:
        return int(v)
    if key == "all":
        for h in i["changelog"]["histories"]:
            for it in h["items"]:
                if it["field"] == "Legacy bug" and it["toString"]:
                    return int(it["toString"])
        for lab in i["fields"].get("labels") or []:
            if lab.startswith("legacy-"):
                return int(lab[7:])
    if key == "history":
        for h in i["changelog"]["histories"]:
            for it in h["items"]:
                if it["field"] == "Legacy bug" and it["toString"]:
                    return int(it["toString"])
    return None


def ask_figures(A, filing="legacy", key="all", moved=True, first="triage", closed="replay", comps="replay"):
    """Ask A by week (no triage action within 24 hours of filing; closed by the run's end) and Ask B by group (the
    run's items in the group's components at the run's end). The golden is the default: the old bug number from the
    field or its changelog, the filing time from the old tracker, moved reports included, a triage action as the
    working agreement defines it, the state at the run's end replayed from the changelog. Other settings are the
    wrong routes: filing created (the new tracker's own created), hybrid (the old tracker's time where the field holds
    the number, created otherwise); key fields (the field only)."""
    end = dt.datetime(2026, 11, 29, 23, 59, 59)
    seen = set()
    items = []
    for i in sorted(A.issues, key=lambda i: (i["fields"]["created"], int(i["id"]))):
        f = i["fields"]
        if f["issuetype"]["name"] != "Bug" or f["security"] is not None:
            continue
        hs = i["changelog"]["histories"]
        was_brw = f["project"]["key"] == "BRW" or any(it["field"] == "project" and it["fromString"] == "Browser intake"
                                                      for h in hs for it in h["items"])
        if not was_brw or (f["project"]["key"] == "WEBC" and not moved):
            continue
        lb = legacy_id(i, key)
        if lb is not None:
            if lb in seen:
                continue
            seen.add(lb)
        if filing == "legacy" or (filing == "hybrid" and lb is not None):
            if lb is None or lb not in A.opened:
                continue
            t_file = A.opened[lb]
        else:
            t_file = jt(f["created"])
        if not (RUN_FROM <= t_file < RUN_TO):
            continue
        items.append((i, t_file))
    na = {w: 0 for w in RUN_WEEKS}
    nc = {w: 0 for w in RUN_WEEKS}
    ng = {g: 0 for g in GROUPS}
    nm = {g: 0 for g in GROUPS}
    n_items = {w: 0 for w in RUN_WEEKS}
    for i, t_file in items:
        w = monday(t_file.date())
        n_items[w] += 1
        hs, comps0 = issue_view(i)
        fa = None
        for h in hs:
            if h["author"]["displayName"] not in A.triagers:
                continue
            fields = {it["field"] for it in h["items"]}
            if first == "any" or (fields & set(TRIAGE_FIELDS)) or "project" in fields:
                fa = jt(h["created"])
                break
        if fa is None or fa - t_file > dt.timedelta(hours=24):
            na[w] += 1
        if closed == "replay":
            st, proj = None, None
            for h in hs:
                if jt(h["created"]) > end:
                    break
                for it in h["items"]:
                    if it["field"] == "status":
                        st = it["toString"]
                    if it["field"] == "project":
                        proj = it["toString"]
            if st in CLOSED or proj == "Web compatibility":
                nc[w] += 1
        else:
            f = i["fields"]
            if f["resolution"] is not None and f["resolutiondate"] and jt(f["resolutiondate"]) <= end:
                nc[w] += 1
        # Ask B: the component the bridge wrote the report into (the creation components: the current ones with
        # every later component change undone); the mirror reads the components as they are now
        cs = set(comps0) if comps == "replay" else {c["name"] for c in i["fields"]["components"]}
        for g in {A.group.get(c) for c in cs} - {None}:
            ng[g] += 1
        for h in hs:
            if any(it["field"] == "project" and it["toString"] == "Web compatibility" for it in h["items"]):
                src = {it["fromString"] for it in h["items"] if it["field"] == "Component" and it["fromString"]}
                for g in {A.group.get(c) for c in src} - {None}:
                    nm[g] += 1
                break
    return dict(no_action=na, closed=nc, groups=ng, moved=nm, items=n_items)


ROUTES = {
    "golden": dict(),
    # the cracker executes every filed definition, drops the re-sent copies on the old bug number, finds the moved
    # reports, replays the state at the run's end; its two natural readings of a report's filing time:
    "cracker_created": dict(filing="created", key="fields"),       # the new tracker's created
    "cracker_legacy": dict(filing="legacy", key="fields"),         # the old tracker's opened, through Legacy bug
    "cracker_hybrid": dict(filing="hybrid", key="fields"),         # the old tracker's where Legacy bug holds it
    # the old number of a moved report read from its changelog as well
    "cracker_history": dict(filing="legacy", key="history"),
    "cracker_history_hybrid": dict(filing="hybrid", key="history"),
    # every device found (and the catch-up copies' labels): the golden
    "cracker_full": dict(filing="legacy", key="all"),
    # the mirror: the triage project as it stands, any change by a triager, resolved by the resolution date,
    # components as they are now
    "mirror": dict(filing="created", key="fields", moved=False, first="any", closed="resolution", comps="current"),
}
CRACKER_PATHS = ("cracker_created", "cracker_legacy", "cracker_hybrid", "cracker_history", "cracker_history_hybrid")


def ask_routes(A):
    return {k: ask_figures(A, **v) for k, v in ROUTES.items()}


ASK_CRITERIA = {"A": 8, "B": 8, "chart_content": 1, "chart_parts": 1}
W_CALL, W_INSTR, W_ASK, R_WRONG_CALL = 38.0, 7.0, 55.0, 5.0


def kept(fig, gold):
    k = sum(fig["no_action"][w] == gold["no_action"][w] for w in RUN_WEEKS) + \
        sum(fig["closed"][w] == gold["closed"][w] for w in RUN_WEEKS)
    kb = sum(fig["groups"][g] == gold["groups"][g] for g in GROUPS)
    chart = int(k == 8)
    return dict(A=k, B=kb, chart_content=chart, chart_parts=1)


def ceiling_report(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    D = load(target)
    A = load_asks(target, D)
    R = ask_routes(A)
    g = R["golden"]
    n = sum(ASK_CRITERIA.values())
    kept_by = {name: kept(R[name], g) for name in R if name != "golden"}
    s = R_WRONG_CALL + W_INSTR + W_ASK * sum(kept_by["mirror"].values()) / n
    pairs = {}
    for name in CRACKER_PATHS + ("cracker_full",):
        c = W_CALL + W_INSTR + W_ASK * sum(kept_by[name].values()) / n
        pairs[name] = dict(cracker=c, pair=(c + s) / 2,
                           pair_mirror_on_path=(c + R_WRONG_CALL + W_INSTR + W_ASK * sum(kept_by[name].values()) / n) / 2)
    rep = dict(kept=kept_by, mirror=s, pairs=pairs, pair=max(pairs[p]["pair"] for p in CRACKER_PATHS),
               mirror_leakage=100.0 * sum(kept_by["mirror"].values()) / n, routes=R)
    if not quiet:
        for name in R:
            f = R[name]
            print("%-16s A no action %s closed %s | B %s" % (name, [f["no_action"][w] for w in RUN_WEEKS],
                                                               [f["closed"][w] for w in RUN_WEEKS],
                                                               [f["groups"][gg] for gg in GROUPS]))
        for name in kept_by:
            print("  kept %-16s %s" % (name, kept_by[name]))
        for name, v in pairs.items():
            print("  %-16s cracker %.1f  pair %.1f  (mirror on the same path %.1f)" % (name, v["cracker"], v["pair"],
                                                                                 v["pair_mirror_on_path"]))
        print("mirror %.1f  pair ceiling %.1f  mirror leakage %.1f per cent" % (s, rep["pair"], rep["mirror_leakage"]))
    return rep


def rungs(D):
    return dict(R0=rung_dashboard(D), R1=rung_default(D), R2a=profile_model(D), R2b=uplift_model(D),
                R2c=typical_reach_model(D), R3=forecast(D), max=rung_record_max(D), q4=rung_last_quarter(D),
                per_install=rung_per_install_max(D))


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    D = load(target)
    for k, v in rungs(D).items():
        print(k, {a: (round(b, 1) if isinstance(b, float) else b) for a, b in v.items()
                  if a not in ("weeks", "H", "fit", "profile")})
