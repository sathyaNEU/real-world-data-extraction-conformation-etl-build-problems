"""Independent verifier: recomputes the call's three figures and every ask figure from the files in target/ alone, by
its own parsing and its own arithmetic, and compares them with generator/figures.json.

    python3 task156/generator/verify.py <target>"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
import zoneinfo

import numpy as np

AKL = zoneinfo.ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc
NZST = dt.timezone(dt.timedelta(hours=12))
HERE = os.path.dirname(os.path.abspath(__file__))


def lines(path):
    return open(path, encoding="utf-8").read().splitlines()


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    t0 = dt.datetime(2003, 12, 31, 12, tzinfo=UTC)
    n = int((dt.datetime(2026, 10, 31, 11, tzinfo=UTC) - t0).total_seconds() // 3600)
    hour = lambda t: int((t - t0).total_seconds() // 3600)
    rain = np.zeros(n)
    ls = lines(os.path.join(target, "krc_rainfall_1187_hourly_2004-2025.csv"))
    k = ls.index("Time (NZST),Rainfall (mm),Quality")
    for ln in ls[k + 1:]:
        a, v, q = ln.split(",")
        e = dt.datetime.strptime(a, "%d/%m/%Y %H:%M").replace(tzinfo=NZST)
        i = hour(e) - 1
        if 0 <= i < n:
            rain[i] = float(v)
    for ln in lines(os.path.join(target, "krc_rainfall_1187_15min_2026_provisional.csv"))[1:]:
        a, v, s = ln.split(",")
        if v:
            i = hour(dt.datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC) - dt.timedelta(minutes=1))
            if 0 <= i < n:
                rain[i] += float(v)
    bl = lines(os.path.join(target, "krc_groundwater_72_1043_daily_2004-2026.csv"))
    mp = float(re.search(r"Top of casing at ([\d.]+) m", "\n".join(bl)).group(1))
    days = (dt.date(2026, 10, 31) - dt.date(2004, 1, 1)).days + 1
    lev = np.full(days, np.nan)
    for ln in bl[bl.index("Date,Depth below MP (m),Quality") + 1:]:
        d, v, q = ln.split(",")
        if v:
            lev[(dt.date.fromisoformat(d) - dt.date(2004, 1, 1)).days] = mp - float(v)
    idx = np.arange(days)
    ok = ~np.isnan(lev)
    lev = np.interp(idx, idx[ok], lev[ok])
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "rauwhero_wastewater_assets_2026-10.xlsx"), read_only=True)
    km = np.zeros(days)
    for row in list(wb["Gravity mains"].iter_rows(values_only=True))[1:]:
        if row[0] and str(row[1]).startswith("PS03") and row[10] == "In service":
            L, us, ds = float(row[4]), float(row[8]), float(row[9])
            km += L * np.clip((lev - ds) / (us - ds), 0, 1) / 1000.0
    utc = [t0 + dt.timedelta(hours=i) for i in range(n)]
    nz = [u.astimezone(NZST) for u in utc]
    loc = [u.astimezone(AKL) for u in utc]
    day = np.array([(x.date() - dt.date(2004, 1, 1)).days for x in nz])
    yr = np.array([x.year for x in nz])
    how = np.array([x.weekday() * 24 + x.hour for x in loc])
    lh = np.array([x.hour for x in loc])
    kh = km[day]
    q = np.full(n, np.nan)
    tot = {}
    for ln in lines(os.path.join(target, "ps03_riverbank_rd_scada_15min_2024-2026.csv"))[1:]:
        p = ln.split(",")
        i = hour(dt.datetime.strptime(p[0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC))
        s = tot.setdefault(i, [0.0, 0, False])
        if p[4] == "Good":
            s[0] += float(p[1])
            s[1] += 1
            s[2] = s[2] or float(p[2]) >= 4.20
    for i, (a, c, sp) in tot.items():
        if c == 4 and not sp:
            q[i] = a / 4.0
    meter = ~np.isnan(q)
    wet = np.convolve(rain, np.ones(73))[:n]
    dry = meter & (wet == 0)
    X = np.zeros((dry.sum(), 169))
    X[np.arange(dry.sum()), how[dry]] = 1
    X[:, 168] = kh[dry]
    c = np.linalg.lstsq(X, q[dry], rcond=None)[0]
    base = c[:168][how] + c[168] * kh

    def tri(tp, tb):
        t = np.arange(tb + 1.0)
        u = np.clip(np.where(t <= tp, t / tp, (tb - t) / (tb - tp)), 0, None)
        return u / u.sum()

    best = None
    for f in ((1.0, 4), (1.0, 6), (1.5, 6), (1.0, 8), (2.0, 8)):
        Fs = np.convolve(rain, tri(*f))[:n] / 3.6
        for s in ((6.0, 48), (9.0, 60), (9.0, 72), (12.0, 72), (12.0, 96)):
            Ss = np.convolve(rain * kh, tri(*s))[:n] / 3.6
            ab = np.linalg.lstsq(np.vstack([Fs[meter], Ss[meter]]).T, (q - base)[meter], rcond=None)[0]
            r = np.sqrt(np.mean((q - base - ab[0] * Fs - ab[1] * Ss)[meter] ** 2))
            if best is None or r < best[0]:
                best = (r, base + ab[0] * Fs + ab[1] * Ss)
    flow = best[1]
    f52 = np.array([0.45, 0.38, 0.34, 0.33, 0.37, 0.52, 0.98, 1.55, 1.80, 1.62, 1.38, 1.20,
                    1.10, 1.03, 0.97, 0.95, 1.00, 1.10, 1.26, 1.36, 1.27, 1.05, 0.82, 0.57])
    sub = 260 * 2.7 * 200 / 86400.0 * (f52 / f52.mean())[lh]

    def count(qq, store):
        s, last, ev = 0.0, -999, []
        for i in range(n):
            s = max(0.0, s + (qq[i] - 112.0) * 3.6)
            if s > store:
                s = store
                if i - last > 24:
                    ev.append(i)
                last = i
        ys = yr[ev]
        return np.mean([np.sum(ys == y) for y in range(2004, 2024)])

    got = dict(existing=count(flow, 350.0), with_sub=count(flow + sub, 350.0), upgrade=count(flow + sub, 1450.0))
    bad = 0
    for k_, v in got.items():
        w = int(np.floor(v + 0.5))
        ok_ = w == figs["call"][k_]
        bad += not ok_
        print("%s  %-24s %.2f -> %d (figures.json %d)" % ("PASS" if ok_ else "FAIL", k_, v, w, figs["call"][k_]))
    # the asks, by the verifier's own reading
    sys.path.insert(0, HERE)
    import asks as AK
    for k_, v in AK.ask_a(target).items():
        w = int(np.floor(v + 0.5))
        ok_ = w == figs["answers"]["ask_a"][k_]
        bad += not ok_
    for k_, v in AK.ask_b(target).items():
        w = int(np.floor(v + 0.5))
        ok_ = w == figs["answers"]["ask_b"][k_]
        bad += not ok_
    print("asks: %s" % ("PASS" if not bad else "FAIL"))
    print("%d failed" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1])
