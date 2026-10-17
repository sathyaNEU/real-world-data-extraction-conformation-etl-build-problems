"""The Statistics Office's quarterly national accounts: the latest estimates of every expenditure component, the
releases that came before them (advance, second and third estimates and the July annual updates), and what each
release said about each quarter. Goods trade and non-farm business inventories come from TBS's data in world.py;
the other components are the Office's own sources, drawn here.

A release's estimate of a quarter is the latest estimate moved back by every revision the later releases made, so
the latest estimate is the end of each quarter's path. Volumes are held internally in $m at 2025 prices; a release
publishes them at the average prices of its reference year (the year before its latest March quarter)."""
from __future__ import annotations

import calendar
import datetime as dt
import math

import numpy as np

import common as K
import world as WD

QUARTERS = K.quarter_list(K.Q0, "2026Q1")
QI = {q: i for i, q in enumerate(QUARTERS)}
NQ = len(QUARTERS)
QYEAR = np.array([int(q[:4]) for q in QUARTERS])
QNUM = np.array([int(q[-1]) for q in QUARTERS])

# code, title, 2026Q1 level ($m, 2025 prices, about), mean quarterly growth, sd, deflator growth a year
SMOOTH = [
    ("HFCE", "Household final consumption expenditure", 77900.0, 0.0050, 0.0028, 0.026),
    ("GFCE", "General government final consumption expenditure", 24900.0, 0.0057, 0.0024, 0.031),
    ("GFCF_DW", "Gross fixed capital formation: dwellings", 7300.0, 0.0036, 0.012, 0.042),
    ("GFCF_ME", "Gross fixed capital formation: machinery and equipment", 6500.0, 0.0046, 0.016, 0.012),
    ("GFCF_NDC", "Gross fixed capital formation: non-dwelling construction", 4100.0, 0.0040, 0.013, 0.041),
    ("GFCF_IPP", "Gross fixed capital formation: intellectual property products", 3600.0, 0.0090, 0.008, 0.019),
    ("GFCF_PUB", "Gross fixed capital formation: general government", 4400.0, 0.0056, 0.017, 0.036),
    ("X_S", "Exports of services", 7900.0, 0.0060, 0.010, 0.024),
    ("M_S", "Imports of services", 7600.0, 0.0059, 0.010, 0.021),
]
COVID = {   # 2020Q2, 2020Q3, 2020Q4 log changes added
    "HFCE": (-0.118, 0.092, 0.012), "GFCE": (0.012, 0.004, 0.0), "GFCF_DW": (-0.20, 0.16, 0.03),
    "GFCF_ME": (-0.15, 0.11, 0.02), "GFCF_NDC": (-0.11, 0.07, 0.01), "GFCF_IPP": (-0.03, 0.02, 0.0),
    "GFCF_PUB": (-0.06, 0.05, 0.0), "X_S": (-0.55, 0.05, 0.02), "M_S": (-0.62, 0.10, 0.03),
}
TITLES = {c: t for c, t, *_ in SMOOTH}
TITLES.update({
    "CIPI_NF": "Changes in inventories: non-farm business",
    "CIPI_FO": "Changes in inventories: farm and other",
    "X_G": "Exports of goods", "M_G": "Imports of goods",
    "GFCF_BUS": "Gross fixed capital formation: business",
    "GDP": "Gross domestic product",
})
ORDER = ["HFCE", "GFCE", "GFCF_DW", "GFCF_BUS", "GFCF_ME", "GFCF_NDC", "GFCF_IPP", "GFCF_PUB", "CIPI_NF",
         "CIPI_FO", "X_G", "X_S", "M_G", "M_S", "GDP"]
SIGN = {c: (-1.0 if c in ("M_G", "M_S") else 1.0) for c in ORDER}
BASE = ["HFCE", "GFCE", "GFCF_DW", "GFCF_ME", "GFCF_NDC", "GFCF_IPP", "GFCF_PUB", "CIPI_NF", "CIPI_FO", "X_G",
        "X_S", "M_G", "M_S"]
ADDITIVE = ("CIPI_NF", "CIPI_FO")          # revised and perturbed in $m, not in proportion


# ---------------------------------------------------------------------------------------------------- calendar
def last_weekday(y, m, wd):
    d = dt.date(y, m, calendar.monthrange(y, m)[1])
    while d.weekday() != wd:
        d -= dt.timedelta(days=1)
    return d


def nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    while d.weekday() != wd:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def release_calendar():
    """Every release from the March quarter 2019 advance estimate to the July 2026 annual update: id, date, type,
    the latest quarter it covers, its reference year."""
    rel = []
    for q in K.quarter_list("2019Q1", "2026Q1"):
        y, n = int(q[:4]), int(q[-1])
        months = [(y, 3 * n + k) if 3 * n + k <= 12 else (y + 1, 3 * n + k - 12) for k in (1, 2, 3)]
        for (yy, mm), kind in zip(months, ("advance", "second", "third")):
            d = last_weekday(yy, mm, 3)                      # the last Thursday
            if mm == 12:
                d = nth_weekday(yy, 12, 3, 3)                # the third Thursday in December
            rel.append({"date": d, "type": kind, "quarter": q})
    for y in range(2019, 2027):
        latest = "%dQ1" % y
        rel.append({"date": nth_weekday(y, 7, 1, 3), "type": "annual", "quarter": latest})
    rel.sort(key=lambda r: r["date"])
    for r in rel:
        d = r["date"]
        # the reference year moves to the previous year with each year's March quarter advance estimate
        r["ref"] = (d.year - 1) if (d.month, d.day) >= (4, 20) else (d.year - 2)
        r["id"] = "%s-%s" % (r["quarter"], {"advance": "A", "second": "S", "third": "T", "annual": "U"}[r["type"]])
        if r["type"] == "annual":
            r["id"] = "%d-U" % d.year
    return rel


# ---------------------------------------------------------------------------------------------------- latest
def latest(W):
    """The latest estimates (the July 2026 annual update) of every component, quarterly, $m at 2025 prices."""
    N = {}
    q1 = QI["2026Q1"]
    for code, title, lvl, mu, sd, defl in SMOOTH:
        r = K.rng("na", code)
        g = r.normal(mu, sd, NQ)
        if code in COVID:
            for k, v in zip(("2020Q2", "2020Q3", "2020Q4"), COVID[code]):
                g[QI[k]] += v
        if code == "X_S":
            g[(QYEAR == 2021) | (QYEAR == 2022)] += 0.035
        if code == "M_S":
            g[(QYEAR == 2021) | (QYEAR == 2022)] += 0.040
        g[0] = 0.0
        lv = np.cumsum(g)
        N[code] = np.exp(lv - lv[q1]) * lvl * math.exp(K.rng("na", code, "level").normal(0.0, 0.03))
    N["X_G"] = np.array([WD.goods_volume(W, q, "x") for q in QUARTERS])
    N["M_G"] = np.array([WD.goods_volume(W, q, "m") for q in QUARTERS])
    r = K.rng("na", "coverage")
    W.COVER = r.normal(0.0, 10.0, NQ)                # the Office's estimate for businesses outside TBS's survey
    N["CIPI_NF"] = np.array([WD.turnover_cipi(W, q) for q in QUARTERS]) + W.COVER
    r = K.rng("na", "CIPI_FO")
    fo = 35.0 + r.normal(0.0, 45.0, NQ)
    fo[QI["2020Q2"]] -= 120.0
    N["CIPI_FO"] = fo
    N["GFCF_BUS"] = N["GFCF_ME"] + N["GFCF_NDC"] + N["GFCF_IPP"]
    N["GDP"] = sum(SIGN[c] * N[c] for c in BASE)
    W.NA = N
    # implicit deflators (2025 average = 1), quarterly
    W.DEFL = {}
    t = np.arange(NQ) - QI["2025Q3"] + 0.5
    for code, title, lvl, mu, sd, defl in SMOOTH:
        r = K.rng("defl", code)
        W.DEFL[code] = np.exp(t * math.log(1 + defl) / 4.0 + np.cumsum(r.normal(0, 0.002, NQ)) * 0.5)
        W.DEFL[code] /= W.DEFL[code][QYEAR == 2025].mean()
    qm = {q: [WD.MI[m] for m in K.quarter_months(q)] for q in QUARTERS}
    W.DEFL["X_G"] = np.array([sum(W.VX[s][qm[q]].sum() for s in K.SITC_CODES) /
                              sum(W.XV[s][qm[q]].sum() for s in K.SITC_CODES) for q in QUARTERS])
    W.DEFL["M_G"] = np.array([sum(W.VM[s][qm[q]].sum() for s in K.SITC_CODES) /
                              sum(W.MV[s][qm[q]].sum() for s in K.SITC_CODES) for q in QUARTERS])
    stock_p = np.array([np.mean([W.P[c][qm[q]].mean() for c in K.IND_CODES]) for q in QUARTERS])
    W.DEFL["CIPI_NF"] = stock_p / stock_p[QYEAR == 2025].mean()
    W.DEFL["CIPI_FO"] = np.exp(t * math.log(1.02) / 4.0)
    W.DEFL["CIPI_FO"] /= W.DEFL["CIPI_FO"][QYEAR == 2025].mean()
    for c in ("X_G", "M_G"):
        W.DEFL[c] = W.DEFL[c] / W.DEFL[c][QYEAR == 2025].mean()
    W.DEFL["GFCF_BUS"] = (W.DEFL["GFCF_ME"] * N["GFCF_ME"] + W.DEFL["GFCF_NDC"] * N["GFCF_NDC"]
                          + W.DEFL["GFCF_IPP"] * N["GFCF_IPP"]) / N["GFCF_BUS"]
    nominal = sum(SIGN[c] * N[c] * W.DEFL[c] for c in BASE)
    W.DEFL["GDP"] = nominal / N["GDP"]


# ---------------------------------------------------------------------------------------------------- vintages
# the log-level (or $m for inventories) standard deviation of the revision each release type makes to a quarter
REV_SD = {
    #           second  third  annual  next (a later estimate's revision to an earlier quarter)
    "HFCE": (0.0013, 0.0006, 0.0016, 0.0003),
    "GFCE": (0.0011, 0.0005, 0.0020, 0.0003),
    "GFCF_DW": (0.0050, 0.0025, 0.0045, 0.0010),
    "GFCF_ME": (0.0075, 0.0035, 0.0055, 0.0015),
    "GFCF_NDC": (0.0060, 0.0030, 0.0050, 0.0012),
    "GFCF_IPP": (0.0030, 0.0015, 0.0040, 0.0005),
    "GFCF_PUB": (0.0070, 0.0030, 0.0055, 0.0015),
    "X_S": (0.0040, 0.0020, 0.0040, 0.0008),
    "M_S": (0.0040, 0.0020, 0.0040, 0.0008),
    "X_G": (0.0015, 0.0006, 0.0, 0.0003),
    "M_G": (0.0015, 0.0006, 0.0, 0.0003),
    "CIPI_NF": (22.0, 8.0, 0.0, 4.0),
    "CIPI_FO": (24.0, 12.0, 14.0, 5.0),
}
BENCHMARKED = ("HFCE", "GFCE", "GFCF_DW", "GFCF_ME", "GFCF_NDC", "GFCF_IPP", "GFCF_PUB", "X_S", "M_S", "CIPI_FO")


def _qidx(q):
    return QI[q]


def revision_window(rel, k):
    """The revision type a release makes to quarter k (index), or None."""
    q = QI[rel["quarter"]]
    t = rel["type"]
    if t == "advance":
        return None                              # the advance estimate revises no earlier quarter
    if t == "second":
        return "second" if k == q else ("next" if k == q - 1 else None)
    if t == "third":
        return "third" if k == q else ("next" if k in (q - 1, q - 2) else None)
    if t == "annual":
        y = rel["date"].year
        first = QI.get("%dQ2" % (y - 3), 0)
        return "annual" if first <= k <= q else None
    return None


def vintages(W):
    """est[release id][component] is an array over QUARTERS ($m at 2025 prices), NaN where the release does not
    cover the quarter."""
    rel = release_calendar()
    W.RELEASES = rel
    est = {r["id"]: {} for r in rel}
    order = {r["id"]: i for i, r in enumerate(rel)}
    for c in BASE:
        r = K.rng("rev", c)
        sd = REV_SD[c]
        for k in range(NQ):
            q = QUARTERS[k]
            # releases covering quarter k, in date order (from its advance estimate, or from the first release)
            cover = [x for x in rel if QI[x["quarter"]] >= k]
            # walk back from the latest release
            e = 0.0
            vals = {}
            for x in reversed(cover):
                vals[x["id"]] = e
                w = revision_window(x, k)
                if w is None:
                    continue
                s = {"second": sd[0], "third": sd[1], "annual": sd[2], "next": sd[3]}[w]
                if w == "annual" and c not in BENCHMARKED:
                    s = 0.0
                if x["id"] == "2026-U":
                    s = 0.0                      # the July 2026 benchmark is drawn separately below
                e = e - r.normal(0.0, s) if s > 0 else e
            for x in cover:
                est[x["id"]].setdefault(c, np.full(NQ, np.nan))
                ev = vals[x["id"]]
                est[x["id"]][c][k] = W.NA[c][k] + ev if c in ADDITIVE else W.NA[c][k] * math.exp(ev)
    W.EST = est
    benchmark_2026(W)
    for rid in est:
        e = est[rid]
        e["GFCF_BUS"] = e["GFCF_ME"] + e["GFCF_NDC"] + e["GFCF_IPP"]
        e["GDP"] = sum(SIGN[c] * e[c] for c in BASE)


# the July 2026 update: each benchmarked year's annual level revision to household and government consumption, spread
# through the year and carried into 2026, plus the seasonal factors re-estimated with the extra year
BENCH_ANNUAL = {"HFCE": {2023: 0.0020, 2024: 0.0075, 2025: 0.0100, 2026: 0.0100},
                "GFCE": {2023: -0.0010, 2024: 0.0035, 2025: 0.0020, 2026: 0.0020}}
BENCH_WSD = {"HFCE": 0.0016, "GFCE": 0.0012}


def benchmark_2026(W):
    """The July 2026 annual update: the annual benchmarks move the Office's own components from the June quarter
    2023; goods trade and non-farm inventories (TBS's data) are not benchmarked. Every release before it carries the
    pre-benchmark estimates of those quarters."""
    r = K.rng("bench", "2026")
    first = QI["2023Q2"]
    n = NQ - first
    qs = QUARTERS[first:]
    annual, wsd = BENCH_ANNUAL, BENCH_WSD
    path = {}
    for c in ("HFCE", "GFCE"):
        lv = np.array([annual[c][int(q[:4])] for q in qs])
        t = np.arange(n)
        sm = np.convolve(np.r_[lv[0], lv, lv[-1]], [0.25, 0.5, 0.25], mode="valid")
        path[c] = np.r_[np.zeros(first), sm + r.normal(0.0, wsd[c], n)]
    for c, s in (("GFCF_DW", 0.0070), ("GFCF_ME", 0.0090), ("GFCF_NDC", 0.0080), ("GFCF_IPP", 0.0070),
                 ("GFCF_PUB", 0.0090), ("X_S", 0.0060), ("M_S", 0.0060)):
        path[c] = np.r_[np.zeros(first), np.cumsum(r.normal(0.0, s, n)) * 0.35]
    fo = np.r_[np.zeros(first), r.normal(0.0, 18.0, n)]
    pre = [x["id"] for x in W.RELEASES if x["id"] != "2026-U"]
    for rid in pre:
        for c in path:
            v = W.EST[rid][c]
            ok = ~np.isnan(v)
            W.EST[rid][c][ok] = v[ok] / np.exp(path[c][ok])
        v = W.EST[rid]["CIPI_FO"]
        ok = ~np.isnan(v)
        W.EST[rid]["CIPI_FO"][ok] = v[ok] - fo[ok]
    W.BENCH = path


def growth_ann(gdp, k):
    return K.annualise((gdp[k] / gdp[k - 1] - 1.0) * 100.0)


def simulate(W):
    latest(W)
    vintages(W)
    return W
