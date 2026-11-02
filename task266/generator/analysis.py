"""The golden and every rival, computed forward from the shipped files: the latency estimates the register supports
(the doubly truncated nonparametric maximum likelihood estimate, and the readings a solver reaches first), the
horizon each one sets, and the asks' figures with their devices handled and mishandled."""
import csv
import datetime as dt
import math
import os
import re

import numpy as np
from openpyxl import load_workbook

import common as K

MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def pdate(s):
    s = (s or "").strip()
    if not s:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return dt.date.fromisoformat(s)
    m = re.fullmatch(r"(\d{2})-([A-Z][a-z]{2})-(\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), MON[m.group(2)], int(m.group(1)))
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    raise ValueError(s)


def _rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------ the register
def load_cases(target):
    """One record per register case: ref (as the histories key it), diagnosis date, exposure category, first
    exposure (None where no period of work is assessed exposed)."""
    cases = []
    for r in _rows(os.path.join(target, K.FILES["register"])):
        cases.append(dict(ref=r["fund_ref"], D=pdate(r["date_of_diagnosis"]), cat=r["exposure_category"],
                          sex=r["sex"]))
    wb = load_workbook(os.path.join(target, K.FILES["legacy"]), read_only=True)
    ws = wb["Register"]
    code = {"OCC": "Occupational", "DOM": "Domestic", "ENV": "Environmental", "NIL": "No exposure identified"}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if not row or not row[0]:
            continue
        ref = str(row[0]).replace("DD/", "DD").replace("/", "-")
        cases.append(dict(ref=ref, D=pdate(row[5]), cat=code[row[10]], sex={"M": "Male", "F": "Female"}[row[3]]))
    first = {}
    for h in _rows(os.path.join(target, K.FILES["histories"])):
        if h["asbestos_exposure"] in ("Y", "Yes"):
            d = pdate(h["started"])
            if h["case_ref"] not in first or d < first[h["case_ref"]]:
                first[h["case_ref"]] = d
    for c in cases:
        c["E"] = first.get(c["ref"])
    return cases


def in_scope(cases):
    return [c for c in cases if c["cat"] == "Occupational" and c["E"] is not None and c["E"] < K.COHORT_END]


def arrays(sc):
    S, C = K.REG_START, K.REG_END
    t = np.array([(c["D"] - c["E"]).days for c in sc], dtype=float)
    u = np.array([(S - c["E"]).days for c in sc], dtype=float)
    v = np.array([(C - c["E"]).days for c in sc], dtype=float)
    return t, u, v


# ------------------------------------------------------------------------------------------ estimators
def npmle_dt(t, u, v, tol=1e-12, iters=200000):
    """Efron and Petrosian's nonparametric maximum likelihood estimate of a distribution observed under double
    truncation: mass f on the distinct observed values x; each case i is seen only inside [u_i, v_i]. Each
    iteration is O(n) through the windows' index ranges on the sorted values."""
    x, cnt = np.unique(t, return_counts=True)
    a = np.searchsorted(x, u, side="left")           # first value index inside the window
    b = np.searchsorted(x, v, side="right") - 1      # last value index inside the window
    f = cnt / cnt.sum()
    m = len(x)
    for _ in range(iters):
        cf = np.concatenate([[0.0], np.cumsum(f)])
        Fi = cf[b + 1] - cf[a]
        w = 1.0 / Fi
        acc = np.zeros(m + 1)
        np.add.at(acc, a, w)
        np.add.at(acc, b + 1, -w)
        denom = np.cumsum(acc)[:m]
        fn = cnt / denom
        fn /= fn.sum()
        if np.max(np.abs(fn - f)) < tol:
            f = fn
            break
        f = fn
    return x, f


def cdf_at(x, f, days):
    i = np.searchsorted(x, days, side="right")
    return float(f[:i].sum())


def empirical(t):
    x, cnt = np.unique(t, return_counts=True)
    return x, cnt / cnt.sum()


def delayed_entry(t, u):
    """The product-limit curve with each case at risk only from its window's start (delayed entry)."""
    x, d = np.unique(t, return_counts=True)
    order_u = np.sort(u)
    order_t = np.sort(t)
    surv, f = 1.0, []
    for xi, di in zip(x, d):
        at_risk = np.searchsorted(order_u, xi, side="right") - np.searchsorted(order_t, xi, side="left")
        h = di / at_risk
        f.append(surv * h)
        surv *= 1 - h
    f = np.array(f)
    return x, f / f.sum() if f.sum() > 0 else f


def reverse_time(t, v):
    """The reverse-time product-limit curve that corrects for the window's end alone."""
    x, d = np.unique(t, return_counts=True)
    order_v = np.sort(v)
    order_t = np.sort(t)
    F, Fs = 1.0, np.empty(len(x))
    for j in range(len(x) - 1, -1, -1):
        Fs[j] = F
        r = np.searchsorted(order_t, x[j], side="right") - np.searchsorted(order_v, x[j], side="left")
        F *= 1 - d[j] / r
    f = np.diff(np.concatenate([[0.0], Fs]))
    return x, f / f.sum()


def parametric(t, u, v, family):
    """The doubly truncated maximum likelihood fit of a parametric family (years)."""
    from scipy import optimize, stats
    ty, uy, vy = t / K.YEAR, u / K.YEAR, v / K.YEAR

    def dist(th):
        if family == "lognormal":
            return stats.lognorm(th[1], scale=math.exp(th[0]))
        if family == "gamma":
            return stats.gamma(th[0], scale=th[1])
        if family == "loglogistic":
            return stats.fisk(th[0], scale=th[1])
        return stats.weibull_min(th[0], scale=th[1])

    def nll(th):
        if min(th[1:]) <= 0 or (family != "lognormal" and th[0] <= 0):
            return 1e18
        D = dist(th)
        p = D.cdf(vy) - D.cdf(np.maximum(uy, 0))
        return -(np.sum(D.logpdf(ty)) - np.sum(np.log(np.maximum(p, 1e-300))))

    x0 = {"lognormal": [math.log(np.median(ty)), 0.25], "gamma": [18.0, 2.5], "loglogistic": [8.0, 45.0],
          "weibull": [5.0, 50.0]}[family]
    r = optimize.minimize(nll, x0, method="Nelder-Mead", options=dict(maxiter=8000, xatol=1e-9, fatol=1e-9))
    return dist(r.x), float(r.fun)


def coverage(x, f):
    return {H: cdf_at(x, f, H * K.YEAR) for H in K.SETTINGS}


def setting(cov):
    for H in K.SETTINGS:
        if cov[H] >= K.COVER:
            return H
    return None


def main_call(target):
    sc = in_scope(load_cases(target))
    t, u, v = arrays(sc)
    out = dict(n=len(sc))
    x, f = npmle_dt(t, u, v)
    out["golden"] = coverage(x, f)
    out["curve"] = (x, f)
    xe, fe = empirical(t)
    out["empirical"] = coverage(xe, fe)
    xd, fd = delayed_entry(t, u)
    out["delayed"] = coverage(xd, fd)
    xr, fr = reverse_time(t, v)
    out["reverse"] = coverage(xr, fr)
    for k in ("golden", "empirical", "delayed", "reverse"):
        out[k + "_setting"] = setting(out[k])
    return out


# ------------------------------------------------------------------------------------------ the program
def load_program(target):
    appts = _rows(os.path.join(target, K.FILES["appointments"]))
    members = {m["member_no"]: m for m in _rows(os.path.join(target, K.FILES["members"]))}
    wb = load_workbook(os.path.join(target, K.FILES["card"]), read_only=True)
    card = []
    for row in wb["Transactions"].iter_rows(min_row=5, values_only=True):
        if row and row[0]:
            card.append(dict(date=dt.date.fromisoformat(row[0]), time=row[1], merchant=row[2], location=row[3],
                             category=row[4], amount=row[7]))
    wb = load_workbook(os.path.join(target, K.FILES["qa"]), read_only=True)
    qa = {}
    for name in wb.sheetnames:
        for row in wb[name].iter_rows(min_row=4, values_only=True):
            if row and row[0]:
                qa[pdate(str(row[0]))] = dict(start=int(row[2]), end=int(row[3]), tests=int(row[4]))
    return appts, members, card, qa


def fy_rows(appts):
    return [a for a in appts if K.FY_START.isoformat() <= a["appointment_date"] <= K.FY_END.isoformat()]


def unit_days(appts):
    out = {}
    for a in fy_rows(appts):
        if a["site"] == K.UNIT_SITE:
            out.setdefault(dt.date.fromisoformat(a["appointment_date"]), []).append(a)
    return out


def counter_reviews(q):
    """Reviews a day's X-ray counter allows: two views a review, after the day's QC exposures (retakes on top)."""
    return (q["end"] - q["start"] - q["tests"]) / 2.0


def blanks_reviewed(rows, q):
    """Whether a unit day's blank attendance rows were reviews: the day's counter, two exposures a review with a few
    retakes, fits the Attended rows alone or the Attended and blank rows together, never both."""
    att = sum(1 for a in rows if a["attendance"] == "Attended")
    blank = sum(1 for a in rows if a["attendance"] == "")
    n = counter_reviews(q)
    fits_att = att <= n <= att * 1.08 + 1.5
    fits_all = (att + blank) <= n <= (att + blank) * 1.08 + 1.5
    return fits_all and not fits_att, fits_att, fits_all


MIDDAY = ("11:30", "14:00")


def unit_town(day, published, card):
    """Where the unit stood on a working day: the town of the day's midday purchases (11:30 to 14:00), where there
    are any; otherwise the published town."""
    mid = [c for c in card if c["date"] == day and MIDDAY[0] <= c["time"] <= MIDDAY[1]]
    towns = {c["location"] for c in mid}
    if len(towns) == 1:
        return towns.pop()
    return published


def published_town(schedule):
    """date -> town from the published schedule rows (each with its days)."""
    out = {}
    for v in schedule:
        for d in v["days"]:
            out[d] = v["town"]
    return out


def ask_reviews(target, schedule, handle_swaps=True, handle_blanks=True, blanks_all=False, town_by="midday"):
    appts, members, card, qa = load_program(target)
    pub = published_town(schedule)
    days = unit_days(appts)
    out = {t: 0 for t in K.CIRCUIT}
    for d, rows in days.items():
        if town_by == "midday":
            town = unit_town(d, pub[d], card) if handle_swaps else pub[d]
        else:   # any card location that day, the first one
            locs = [c["location"] for c in card if c["date"] == d]
            town = locs[0] if locs else pub[d]
        off = blanks_reviewed(rows, qa[d])[0] if handle_blanks else False
        n = sum(1 for a in rows if a["attendance"] == "Attended" or (a["attendance"] == "" and (off or blanks_all)))
        out[town] = out.get(town, 0) + n
    return out


def ask_members(target, schedule, handle_blanks=True, blanks_all=False):
    appts, members, card, qa = load_program(target)
    days = unit_days(appts)
    off_days = {d for d, rows in days.items() if blanks_reviewed(rows, qa[d])[0]} if handle_blanks else set()
    seen = set()
    for a in fy_rows(appts):
        st = a["attendance"]
        d = dt.date.fromisoformat(a["appointment_date"])
        if st == "Attended" or (st == "" and (blanks_all or (a["site"] == K.UNIT_SITE and d in off_days))):
            seen.add(a["member_no"])
    out = {}
    for H in K.ASK_SETTINGS:
        n = 0
        for m in seen:
            e = dt.date.fromisoformat(members[m]["first_exposure"])
            if (K.TERM_START - e).days / K.YEAR < H:
                n += 1
        out[H] = n
    return out, len(seen), sorted(seen)
