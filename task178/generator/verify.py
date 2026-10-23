"""task178 independent verifier: reads only the shipped bundle (target/), with its own readers and fits, and recomputes
the call, the critical component and every ask figure, then compares them with generator/figures.json.

    python3 task178/generator/verify.py [target]"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
OK = [0, 0]


def chk(label, cond, detail=""):
    OK[0] += 1
    if not cond:
        OK[1] += 1
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + detail + "]") if detail else ""))


def text(path):
    return " ".join(subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True, check=True).stdout.split())


def pst_offset(t):
    """hours to subtract from a Pacific wall-clock time to reach PST (1 in daylight time, 0 otherwise)"""
    y = t.year
    mar = dt.datetime(y, 3, 1) + dt.timedelta(days=(6 - dt.datetime(y, 3, 1).weekday()) % 7 + 7)
    nov = dt.datetime(y, 11, 1) + dt.timedelta(days=(6 - dt.datetime(y, 11, 1).weekday()) % 7)
    return 1 if mar.replace(hour=3) <= t < nov.replace(hour=1) else 0


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    p = lambda f: os.path.join(target, f)
    files = os.listdir(target)
    find = lambda pat: [f for f in files if re.search(pat, f)][0]

    # the standard and the study
    std = text(p(find(r"engineering_standard")))
    m = re.search(r"western Washington, (-?[\d.]+), whose mean square error is ([\d.]+)", std)
    greg, mreg = float(m.group(1)), float(m.group(2))
    chk("standard: generalized skew and its MSE read", (greg, mreg) == (figs["regional_skew"], figs["regional_skew_mse"]))
    study = subprocess.run(["pdftotext", "-layout", p(find(r"alternatives_study")), "-"], capture_output=True, text=True).stdout
    alts = [(a, int(c.replace(",", ""))) for a, c in re.findall(r"^\s+([A-G])\s{3,}.*?\s([\d]{2},\d{3})\s*$", study, re.M)]
    chk("study: seven alternatives read", len(alts) == 7, str(alts))
    chk("study: the selection rule read", "smallest whose capacity is at least the design discharge" in " ".join(study.split()))

    # the peak stages
    reg = pd.read_csv(p(find(r"annual_peaks_wy1980")), skiprows=4)
    reg["h"] = reg["Gage height (ft)"] + np.where(reg["WY"] < 2010, 2.0, 0.0)
    sta = text(p(find(r"station_description")))
    chk("station description: the 2009 datum lowering of 2.00 ft read", "lowered 2.00 ft" in sta)
    s15 = pd.read_csv(p(find(r"stage_15min")), comment="#")
    s15 = s15.drop_duplicates("timestamp")
    s15["t"] = pd.to_datetime(s15["timestamp"])
    s15["wy"] = s15["t"].dt.year + (s15["t"].dt.month >= 10).astype(int)
    rec = s15.loc[s15.groupby("wy")["stage_ft"].idxmax()]
    peaks = np.concatenate([reg["h"].values, rec["stage_ft"].values])
    chk("46 annual peak stages", len(peaks) == 46)

    # the measurements
    xl = pd.read_excel(p(find(r"measurement_notes")), sheet_name=None)
    gh, q = [], []
    for name, df in xl.items():
        gcol = [c for c in df.columns if c in ("Gage ht (ft)", "Mean GH")][0]
        qcol = [c for c in df.columns if c in ("Discharge (cfs)", "Q (cfs)")][0]
        gh += list(df[gcol] + 2.0)
        q += list(df[qcol])
    db = pd.read_csv(p(find(r"measurements_wy2005")))
    d = pd.to_datetime(db["meas_date"])
    gh += list(db["mean_gh_ft"] + np.where(d < "2009-10-01", 2.0, 0.0))
    q += list(db["discharge"] * np.where(db["discharge_unit"] == "m3/s", 35.3147, 1.0))
    gh, q = np.array(gh), np.array(q)
    chk("measurements read", len(q) == figs["measurements"], "%d" % len(q))

    def pl(hh, qq):
        f = lambda x, la, e, b: la + b * np.log(np.maximum(x - e, 1e-6))
        popt, _ = optimize.curve_fit(f, hh, np.log(qq), p0=[4.6, min(hh) - 0.4, 1.8],
                                     bounds=([-10, -5, 0.3], [20, min(hh) - 1e-3, 6]), maxfev=20000)
        return lambda x: np.exp(f(np.asarray(x, float), *popt))

    def compound(hh, qq, hb):
        lo = hh < hb
        fc = pl(hh[lo], qq[lo])
        g = lambda x, a, b: np.log(fc(x) + a * np.maximum(x - hb, 0) ** b)
        popt, _ = optimize.curve_fit(g, hh[~lo], np.log(qq[~lo]), p0=[800, 1.7], bounds=([1, 0.5], [1e5, 4]), maxfev=20000)
        sse = np.sum(np.log(qq[lo] / fc(hh[lo])) ** 2) + np.sum((np.log(qq[~lo]) - g(hh[~lo], *popt)) ** 2)
        return sse, (lambda x: np.exp(g(np.asarray(x, float), *popt)))

    def lp3q(qp):
        x = np.log10(qp)
        n = len(x)
        mu, sd = x.mean(), x.std(ddof=1)
        g = n * np.sum((x - mu) ** 3) / ((n - 1) * (n - 2) * sd ** 3)
        ag = abs(g)
        A = -0.33 + 0.08 * ag if ag <= 0.9 else -0.52 + 0.30 * ag
        B = 0.94 - 0.26 * ag if ag <= 1.5 else 0.55
        mg = 10 ** (A - B * np.log10(n / 10))
        gw = (mreg * g + mg * greg) / (mreg + mg)
        return 10 ** (mu + stats.pearson3.ppf(0.99, gw) * sd), g

    best = min((compound(gh, q, hb) + (hb,) for hb in np.arange(9.6, 11.0, 0.05)), key=lambda x: x[0])
    q100, g = lp3q(best[1](peaks))
    chk("golden: the 1 per cent flood rounds to the figures.json value", int(round(q100, -3)) == figs["call"]["design_discharge_cfs"], "%.0f" % q100)
    pick = [a for a, c in alts if c >= q100][0]
    chk("golden: the alternative", pick == figs["call"]["alternative"], pick)
    chk("golden: the station skew", round(g, 1) == figs["crit"]["station_skew"], "%.3f" % g)
    qd, gd = lp3q(pl(gh, q)(peaks))
    chk("default: one power law files the default's alternative", [a for a, c in alts if c >= qd][0] == figs["default"]["alternative"], "%.0f" % qd)

    # ask A: drop readings during visits (their local times put on PST), take off the controller offset
    vis = pd.read_csv(p(find(r"site_visits")))
    t = s15["t"].values
    h = s15["stage_ft"].values.copy()
    drop = np.zeros(len(h), bool)
    for _, v in vis.iterrows():
        a = dt.datetime.strptime(v["visit_date"] + " " + v["arrive"], "%Y-%m-%d %H:%M")
        b = dt.datetime.strptime(v["visit_date"] + " " + v["depart"], "%Y-%m-%d %H:%M")
        a -= dt.timedelta(hours=pst_offset(a))
        b -= dt.timedelta(hours=pst_offset(b))
        drop |= (t >= np.datetime64(a)) & (t <= np.datetime64(b))
    sw = vis[vis["notes"].fillna("").str.contains("Controller replaced")].iloc[0]
    fx = vis[vis["notes"].fillna("").str.contains("offset reset")].iloc[0]
    off = round(fx["logger_ft"] - fx["staff_gage_ft"], 2)
    a = dt.datetime.strptime(sw["visit_date"] + " " + sw["depart"], "%Y-%m-%d %H:%M")
    b = dt.datetime.strptime(fx["visit_date"] + " " + fx["depart"], "%Y-%m-%d %H:%M")
    a -= dt.timedelta(hours=pst_offset(a))
    b -= dt.timedelta(hours=pst_offset(b))
    mm = (t > np.datetime64(a)) & (t < np.datetime64(b))
    h[mm] = np.round(h[mm] - off, 2)
    for y in range(2016, 2026):
        lo = np.datetime64(dt.datetime(y, 7, 14, 23, 0))
        hi = np.datetime64(dt.datetime(y, 9, 15, 23, 0))
        idx = np.flatnonzero((t >= lo) & (t < hi) & ~drop)
        k = idx[np.argmax(h[idx])]
        tl = pd.Timestamp(t[k]).to_pydatetime() + dt.timedelta(hours=1)
        fa = figs["ask_a"][str(y)]
        chk("ask A %d: %.2f ft on %s" % (y, fa["stage_ft"], fa["date"]), round(float(h[k]), 2) == fa["stage_ft"] and tl.date().isoformat() == fa["date"],
            "%.2f %s" % (h[k], tl.date()))

    # ask B: historian stamps UTC before the June 2022 replacement, local after; the level from the face less the distance
    sc = pd.read_csv(p(find(r"scada_sauer")), skiprows=3)
    ts = pd.to_datetime(sc["Timestamp"])
    up = dt.datetime(2022, 6, 21, 10, 0)
    pst = [x.to_pydatetime() - dt.timedelta(hours=8) if x.to_pydatetime() < up else
           x.to_pydatetime() - dt.timedelta(hours=pst_offset(x.to_pydatetime())) for x in ts]
    lev = re.findall(r"sensor face (\d+\.\d\d)", open(p(find(r"levels_log"))).read())
    f0, f1 = float(lev[0]), float(lev[1])
    br = dt.datetime(2022, 11, 16, 9, 30)
    level = {}
    for tt, dist in zip(pst, sc["SAUER_RAD1_DIST.PV"].values):
        level.setdefault(tt, round((f1 if tt >= br else f0) - dist, 2))
    for wy in range(2020, 2026):
        r = rec[rec["wy"] == wy].iloc[0]
        L = level.get(r["t"].to_pydatetime())
        fb = figs["ask_b"][str(wy)]
        fall = round(182.40 + r["stage_ft"] - L, 2) if L is not None else None
        chk("ask B %d: %.2f ft, fall %.2f" % (wy, fb["pipe_level_ft"], fb["fall_ft"]), L == fb["pipe_level_ft"] and fall == fb["fall_ft"],
            "%s %s" % (L, fall))
    print("%d verified, %d failed" % (OK[0], OK[1]))
    return 1 if OK[1] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
