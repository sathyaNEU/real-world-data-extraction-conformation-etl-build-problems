"""The independent verifier: recompute the call, every scenario figure, the flip, the conformed record and the Stage 2
figures from target/ alone, with its own reading of the files (pandas, pdftotext) and its own log-Pearson Type III
likelihood (written out from the gamma function, no generator module), and compare them with the goldens.

    python3 task466/generator/verify.py
"""
import csv
import datetime as dt
import math
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import optimize, special

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CFS_TO_MGD = 7.48051948 * 86400 / 1e6          # one cubic foot per second in million gallons a day


def text(path):
    out = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", " ", out)


def find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


# ---------------------------------------------------------------- the river's record
def gauge_lows(path):
    """{climatic year: 7-day low flow} for the complete climatic years whose every day is approved."""
    df = pd.read_csv(path, sep="\t", comment="#", dtype=str).iloc[1:]
    df["date"] = pd.to_datetime(df["date"])
    df["q"] = df["discharge_cfs"].astype(float)
    df = df.sort_values("date").reset_index(drop=True)
    assert (df["date"].diff().dropna() == pd.Timedelta(days=1)).all()
    df["m7"] = df["q"].rolling(7).mean()
    df["cy"] = np.where(df["date"].dt.month >= 4, df["date"].dt.year, df["date"].dt.year - 1)
    out = {}
    for y, g in df.groupby("cy"):
        need = (dt.date(y + 1, 4, 1) - dt.date(y, 4, 1)).days
        if len(g) != need or not g["qual"].str.startswith("A").all():
            continue
        out[int(y)] = float(g["m7"].min())          # the windows whose last day falls in the year
    return out


def reports(path):
    """{year: ("measured", cfs) | ("none", None) | ("missing", None)}."""
    t = text(path)
    out = {}
    for m in re.finditer(r"\b(1[89]\d\d) (Report not found|No stoppage|[A-Z][a-z]+\.? \d+ to [^0-9]*?\d+"
                         r"(?:; [A-Z][a-z]+\.? \d+ to [A-Z][a-z]+\.? \d+)?) ?(?:([\d,]{7,}) gal\.|(\d\.\d\d) sec\.-ft\.)?", t):
        y = int(m.group(1))
        if y < 1894 or y > 1950 or y in out:
            continue
        if m.group(2) == "Report not found":
            out[y] = ("missing", None)
        elif m.group(2) == "No stoppage":
            out[y] = ("none", None)
        elif m.group(3):
            out[y] = ("measured", int(m.group(3).replace(",", "")) / 1e6 / CFS_TO_MGD)
        else:
            out[y] = ("measured", float(m.group(4)))
    assert sorted(out) == list(range(1894, 1951)), sorted(set(range(1894, 1951)) - set(out))
    return out


# ---------------------------------------------------------------- log-Pearson Type III, written out
def p3_parts(mu, sd, g):
    a = 4.0 / g ** 2
    b = sd * g / 2.0                     # negative for a negative skew: the logarithms have an upper bound xi
    xi = mu - 2.0 * sd / g
    return a, b, xi


def loglik(par, x, n_above, lt, g):
    mu, sd = par[0], math.exp(par[1])
    a, b, xi = p3_parts(mu, sd, g)
    y = (x - xi) / b
    if np.any(y <= 0):
        return -1e300
    ll = np.sum((a - 1) * np.log(y) - y - special.gammaln(a) - math.log(abs(b)))
    if n_above:
        yt = (lt - xi) / b
        if yt <= 0:
            return -1e300
        ll += n_above * math.log(special.gammainc(a, yt))        # P(log flow > lt) = P(Y < yt) when b < 0
    return ll


def fit(x, n_above, lt, g):
    x = np.asarray(x, float)
    start = np.array([x.mean(), math.log(x.std(ddof=1))])
    r = optimize.minimize(lambda p: -loglik(p, x, n_above, lt, g), start, method="Powell",
                          options=dict(xtol=1e-12, ftol=1e-14, maxiter=200000))
    r = optimize.minimize(lambda p: -loglik(p, x, n_above, lt, g), r.x, method="BFGS", options=dict(gtol=1e-10))
    return float(r.x[0]), float(math.exp(r.x[1]))


def quantile(p, mu, sd, g):
    a, b, xi = p3_parts(mu, sd, g)
    return 10 ** (xi + b * special.gammainccinv(a, p))      # P(log flow <= x) = P(Y >= y) = Q(a, y)


def nonexceed(q, mu, sd, g):
    a, b, xi = p3_parts(mu, sd, g)
    return float(special.gammaincc(a, (math.log10(q) - xi) / b))


def half_up(v, nd=2):
    return "%.*f" % (nd, math.floor(v * 10 ** nd + 0.5 + 1e-9) / 10 ** nd)


# ---------------------------------------------------------------- the town's records
def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def stage2_periods(path):
    out, start = [], None
    for r in sorted(read_csv(path), key=lambda r: (r["posted"], r["notice_no"])):
        if r["stage"] == "Stage 2" and r["action"] == "Declared":
            start = r["in_effect_from"]
        elif r["stage"] == "Stage 2" and r["action"] == "Rescinded":
            out.append((start, r["in_effect_through"]))
            start = None
    return [(dt.date.fromisoformat(a), dt.date.fromisoformat(b)) for a, b in out]


def own_supply(target):
    sc = pd.read_csv(find(target, r"scada_daily"), dtype={"DailyTotal": float})
    sc = sc.drop_duplicates(subset=["Date", "Tag", "DailyTotal"])
    assert not sc.duplicated(subset=["Date", "Tag"]).any()
    piv = sc.pivot(index="Date", columns="Tag", values="DailyTotal")
    eh = pd.read_csv(find(target, r"master_meter"))
    eh = eh.set_index("read_date")["consumption_kgal"] / 1000.0
    log = pd.read_csv(find(target, r"operator_log"), dtype={"totalizer_gal": "int64"}).sort_values("log_date")
    switch = log["log_date"].iloc[0]
    pumped = (log["totalizer_gal"].shift(-1) - log["totalizer_gal"]) / 1e6
    logd = dict(zip(log["log_date"], pumped))
    out = {}
    for d, r in piv.iterrows():
        if d not in eh.index:
            continue
        w = r["HR_WELLS_TOTAL"] if d < switch else logd.get(d)
        if w is None or (isinstance(w, float) and math.isnan(w)):
            continue
        out[dt.date.fromisoformat(d)] = r["WTP_FIN_TOTAL"] - eh[d] + w
    return out


# ---------------------------------------------------------------- the verification
def main(target, golden):
    guid = text(find(target, r"guidance_wr14"))
    g = float(re.search(r"regional low-flow skew, (-?\d\.\d\d)", guid).group(1))
    p_design = float(re.search(r"with a probability of (0\.\d\d)\. 3\. Estimation", guid).group(1))
    permit = text(find(target, r"permit_wd0417"))
    qmax = float(re.search(r"shall not exceed (\d\.\d\d) million gallons a day", permit).group(1))
    passby = float(re.search(r"at least (\d\.\d\d) cubic feet per second", permit).group(1))
    plan = text(find(target, r"drought_management_plan"))
    demand = float(re.search(r"\b2027 (\d\.\d\d) \d\.\d\d \d\.\d\d\b", plan).group(1))
    offer = text(find(target, r"interconnect_offer"))
    blk = float(re.search(r"blocks of (\d\.\d) million gallons a day", offer).group(1))
    rep_text = text(find(target, r"water_works_reports"))
    assert "two millions of gallons in twenty-four hours" in rep_text
    lt = math.log10(2.0 / CFS_TO_MGD)

    lows = gauge_lows(find(target, r"daily_values\.txt$"))
    lows = {y: v for y, v in lows.items() if y >= 1951}
    reps = reports(find(target, r"water_works_reports"))
    xg = np.log10([lows[y] for y in sorted(lows)])
    xm = np.log10([v for y, (k, v) in sorted(reps.items()) if k == "measured"])
    silent = sum(1 for k, _ in reps.values() if k == "none")
    mu, sd = fit(np.concatenate([xg, xm]), silent, lt, g)

    def withdrawal(q):
        return min(qmax, max(0.0, q - passby) * CFS_TO_MGD)
    scen = {}
    for t in (10, 25, 50, 100):
        q = quantile(1.0 / t, mu, sd, g)
        scen[t] = (q, withdrawal(q), max(0.0, demand - withdrawal(q)))
    assert abs(1.0 / 50 - p_design) < 1e-12
    short = scen[50][2]
    block = math.ceil(short / blk - 1e-9) * blk
    q_flip = passby + (demand - block) / CFS_TO_MGD
    flip = 1.0 / nonexceed(q_flip, mu, sd, g)
    # the default route (silent years dropped) and the gauge alone, for the rivals the write-up names
    mu1, sd1 = fit(np.concatenate([xg, xm]), 0, lt, g)
    mu0, sd0 = fit(xg, 0, lt, g)
    rivals = {}
    for k, (m, s) in {"R1": (mu1, sd1), "R0": (mu0, sd0)}.items():
        q = quantile(0.02, m, s, g)
        rivals[k] = (q, math.ceil(max(0.0, demand - withdrawal(q)) / blk - 1e-9) * blk)

    periods = stage2_periods(find(target, r"drought_notices"))
    sup = own_supply(target)
    ask = []
    for a, b in periods:
        v = [sup[a + dt.timedelta(days=i)] for i in range((b - a).days + 1)]
        ask.append((a, b, len(v), float(np.mean(v)), float(np.max(v))))

    # ---------------------------------------------------------------- against the goldens
    memo = text(os.path.join(golden, "quillfield_interconnect_reservation_2027.pdf"))
    errs = []

    def want(s, where=memo, label=""):
        if s not in where:
            errs.append("%s: %r not in the memo" % (label, s))
    want("Reserve %.1f million gallons a day" % block, label="block")
    want("50-year 7-day low flow of %s cubic feet per second" % half_up(scen[50][0]), label="design flow")
    want("take %s MGD, %s MGD short" % (half_up(scen[50][1]), half_up(short)), label="withdrawal and shortfall")
    for t in (10, 25, 50, 100):
        q, w, s = scen[t]
        want("%d years %s %s %s" % (t, half_up(q), half_up(w), half_up(s) if s > 0 else "none"), label="%d-year row" % t)
    want("rarer than the %d-year 7-day low flow (%s cfs)" % (int(math.floor(flip + 0.5)), half_up(q_flip)), label="flip")
    for a, b, n, av, hi in ask:
        want("%s to %s %d %s %s" % (a.isoformat(), b.isoformat(), n, half_up(av), half_up(hi)), label="Stage 2 %s" % a)
    with open(os.path.join(golden, "varrow_river_annual_low_flows.csv"), encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert [int(r["climatic_year"]) for r in rows] == list(range(1894, 2025)), "conformed years"
    for r in rows:
        y = int(r["climatic_year"])
        if y >= 1951:
            exp = half_up(lows[y])
        else:
            k, v = reps[y]
            exp = half_up(v) if k == "measured" else ""
        if r["seven_day_low_flow_cfs"] != exp:
            errs.append("conformed %d: %r, expected %r" % (y, r["seven_day_low_flow_cfs"], exp))
    import json
    fj = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    for k, (q, b) in rivals.items():
        if fj["rivals"][k]["design_flow_cfs"] != half_up(q) or fj["rivals"][k]["block_mgd"] != "%.1f" % b:
            errs.append("rival %s: figures.json %s, verifier %s %.1f" % (k, fj["rivals"][k], half_up(q), b))
    print("verify: %d gauged years, %d measured report years, %d without a stoppage; ML fit mu %.5f sd %.5f" % (
        len(xg), len(xm), silent, mu, sd))
    print("verify: 50-year flow %.4f cfs, withdrawal %.4f MGD, shortfall %.4f MGD, block %.1f MGD, flip %.2f years "
          "(%.4f cfs)" % (scen[50][0], scen[50][1], short, block, flip, q_flip))
    print("verify: rivals R1 %.4f cfs (%.1f MGD), R0 %.4f cfs (%.1f MGD)" % (rivals["R1"][0], rivals["R1"][1],
                                                                          rivals["R0"][0], rivals["R0"][1]))
    for a, b, n, av, hi in ask:
        print("verify: Stage 2 %s to %s, %d days: average %.4f, highest %.4f" % (a, b, n, av, hi))
    if errs:
        for e in errs:
            print("VERIFY FAIL:", e)
        raise SystemExit("verify: %d mismatches" % len(errs))
    print("verify: every graded figure in the memo, the conformed record and the rivals recomputed from target/ alone")


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
