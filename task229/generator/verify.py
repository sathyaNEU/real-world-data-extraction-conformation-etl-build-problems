"""task229 independent verifier: reads only the bundle (target/) and recomputes the call and both asks on its own code
path (no generator module is imported). With --record it compares against the generator's record.

    python3 task229/generator/verify.py <target dir> [--record record.json]"""
import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd
import pypdf
from zoneinfo import ZoneInfo

LINES = []


def say(ok, label):
    LINES.append(("PASS" if ok else "FAIL", label))
    return ok


def text(path):
    return "\n".join(p.extract_text() for p in pypdf.PdfReader(path).pages)


def find(tgt, pat):
    for f in os.listdir(tgt):
        if re.search(pat, f):
            return os.path.join(tgt, f)
    raise SystemExit("missing %s" % pat)


# ------------------------------------------------------------------------------------------------ documents
def read_standard(tgt):
    t = text(find(tgt, r"standard.*\.pdf$")).replace("\n", " ")
    pct = float(re.search(r"within (\d+(?:\.\d+)?) per cent of the month's true mean discharge", t).group(1)) / 100
    mult = {"one and a half": 1.5, "two": 2.0}[re.search(r"exceeds (one and a half|two) times the largest discharge gauged", t).group(1)]
    return pct, mult


def read_ratings(tgt):
    t = text(find(tgt, r"rating_book.*\.pdf$"))
    toks = [x.strip() for x in t.split("\n") if x.strip()]
    rat, top = {}, {}
    for i, tok in enumerate(toks):
        if re.fullmatch(r"C\d{3}-R\d+", tok):
            st = tok.split("-")[0]
            if st in rat:
                continue
            C, e, b = float(toks[i + 2]), float(toks[i + 3]), float(toks[i + 4])
            rng_ = toks[i + 5]
            m = re.fullmatch(r"([\d.]+) to ([\d.]+)", rng_)
            rat[st] = (C, e, b)
            top[st] = float(m.group(2))
    eff = re.search(r"Ratings in force from (\d+ \w+ \d{4})", t.replace("\n", " ")).group(1)
    eff = datetime.strptime(eff, "%d %B %Y").date()
    return rat, top, eff


def read_plan(tgt):
    t = text(find(tgt, r"operating_plan.*\.pdf$")).replace("\n", " ")
    w = re.search(r"two windows, (\d\d):(\d\d) to (\d\d):(\d\d) and (\d\d):(\d\d) to (\d\d):(\d\d) local time", t)
    wins = ((int(w.group(1)) + int(w.group(2)) / 60, int(w.group(3)) + int(w.group(4)) / 60),
            (int(w.group(5)) + int(w.group(6)) / 60, int(w.group(7)) + int(w.group(8)) / 60))
    ramp = int(re.search(r"over (\d+) minutes at the start and at the end of each window", t).group(1)) / 60.0
    tal = re.search(r"Talbot Canyon Generating Station Corriston River ([\d.]+) (\d+) ([\d.]+) (\d{4})", t)
    mer = re.search(r"Merrin Falls Generating Station Merrin Creek ([\d.]+) (\d+) ([\d.]+) 1 June 2027", t)
    plants = {"talbot": {"km": float(tal.group(1)), "cap": float(tal.group(2)), "fmin": float(tal.group(3))},
              "merrin": {"km": float(mer.group(1)), "cap": float(mer.group(2)), "fmin": float(mer.group(3))}}
    cont = re.search(r"From 1 (\w+) to 30 (\w+) the forebays", t)
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    cmonths = set(range(months.index(cont.group(1)) + 1, months.index(cont.group(2)) + 2))
    in_service = date(2027, 6, 1) if "enters service on 1 June 2027" in t else None
    return wins, ramp, plants, cmonths, in_service


def read_outlook(tgt):
    x = pd.read_excel(find(tgt, r"outlook.*\.xlsx$"), sheet_name=0, header=4)
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return {r.station: [float(r[m]) for m in mon] for _, r in x.iterrows()}


def read_register(tgt):
    return pd.read_excel(find(tgt, r"register.*\.xlsx$"), sheet_name="Stations", dtype={"replaced_by": str})


# ------------------------------------------------------------------------------------------------ the call
def call(tgt):
    pct, mult = read_standard(tgt)
    rat, top, _ = read_ratings(tgt)
    wins, ramp, plants, cmonths, in_service = read_plan(tgt)
    out = read_outlook(tgt)
    reg = read_register(tgt)
    st = reg[reg.status == "active"].set_index("station")
    # which stations sit below which plant: same river, downstream of the tailrace
    below = {}
    for s, r in st.iterrows():
        for k, name in (("talbot", "Corriston River"), ("merrin", "Merrin Creek")):
            if r.river == name and r.river_km < plants[k]["km"]:
                below[s] = k
    node = {"talbot": out["TAL-FB"], "merrin": out["MER-HP"]}
    n = 1440
    hours = (np.arange(n) + 0.5) / 60.0
    w = np.zeros(n)
    for a, z in wins:
        up = np.clip((hours - a) / ramp, 0, 1)
        dn = np.clip((z - hours) / ramp, 0, 1)
        w += np.minimum(up, dn) * ((hours > a) & (hours < z))
    first = {}
    errs = {}
    for s in st.index:
        short = []
        for m in range(1, 13):
            Q = out[s][m - 1]
            k = below.get(s)
            peaking = k is not None and m not in cmonths and not (k == "merrin" and date(2027, m, 1) < in_service)
            if peaking:
                I = node[k][m - 1]
                L = Q - I
                fmin = plants[k]["fmin"]
                F = fmin + 24 * (I - fmin) / (w.mean() * 24)
                assert F <= plants[k]["cap"]
                q = fmin + (F - fmin) * w + L
                C, e, b = rat[s]
                h = e + (q / C) ** (1 / b)
                pub = C * (h.mean() - e) ** b
                err = pub / q.mean() - 1
            else:
                err = 0.0
            errs[(s, m)] = err
            if abs(err) > pct or Q > mult * top[s]:
                short.append(m)
        first[s] = min(short) if short else None
    return first, errs


# ------------------------------------------------------------------------------------------------ Ask A
def ask_a(tgt):
    d = pd.read_csv(find(tgt, r"daily_records.*\.csv$"), dtype=str)
    reg = read_register(tgt)
    chain = {r.station: r.replaced_by for _, r in reg.iterrows() if isinstance(r.replaced_by, str) and r.replaced_by}
    d = d[(d.date >= "2025-10-01") & (d.date <= "2026-09-30")].copy()
    start = pd.to_datetime(d.date)
    hours = np.where(d.platform == "GOES", 24, 32)        # the UTC day ends at 00:00Z; the local standard day at 08:00Z
    end = start + pd.to_timedelta(hours, unit="h")
    got = pd.to_datetime(d.received_utc.str.rstrip("Z"))
    d = d[(got >= end).values]
    d["st"] = d.station.map(lambda s: chain.get(s, s))
    d = d.drop_duplicates(["st", "date"])
    return d.groupby(d.date.str[:7]).size().to_dict()


# ------------------------------------------------------------------------------------------------ Ask B
def ask_b(tgt):
    rat, top, eff = read_ratings(tgt)
    t = text(find(tgt, r"rating_book.*\.pdf$")).replace("\n", " ")
    c122_from = date(2026, 6, 4) if "C122) from 4 June 2026" in t else None
    d = pd.read_csv(find(tgt, r"daily_records.*\.csv$"), dtype={"station": str, "date": str})
    g = pd.read_csv(find(tgt, r"gaugings.*\.csv$"), dtype={"station": str, "gauging_no": str, "unit": str}, keep_default_na=False)
    reg = read_register(tgt)
    chain = {r.station: r.replaced_by for _, r in reg.iterrows() if isinstance(r.replaced_by, str) and r.replaced_by}
    # superseded ratings: the curve through each site's published pairs before the effective date
    from scipy.optimize import least_squares
    old = {}
    pre = d[d.date < eff.isoformat()]
    for s, x in pre.groupby("station"):
        x = x.drop_duplicates(["water_level_m", "discharge_m3s"])
        h, q = x.water_level_m.values.astype(float), x.discharge_m3s.values.astype(float)
        def resid(p):
            C, e, b = p
            return np.log(C * np.clip(h - e, 1e-9, None) ** b) - np.log(q)
        e0 = h.min() - 0.3
        sol = least_squares(resid, x0=[q.mean() / (h.mean() - e0) ** 1.8, e0, 1.8],
                            bounds=([1e-6, -5, 0.5], [1e4, h.min() - 1e-4, 4.0]), xtol=1e-14, ftol=1e-14, gtol=1e-14)
        old[s] = tuple(sol.x)
    g["q"] = np.where(g.unit == "L/s", g.discharge.astype(float) / 1000, g.discharge.astype(float))
    g["t"] = pd.to_datetime(g.measured_utc.str.rstrip("Z")) - pd.Timedelta(hours=8)
    gg = g.groupby("gauging_no").agg(station=("station", "first"), t=("t", "first"), gh=("gh_m", "first"), q=("q", "sum")).reset_index()
    gg["day"] = gg.t.dt.date
    gg = gg[(gg.day >= date(2025, 10, 1)) & (gg.day <= date(2026, 9, 30))]
    out = {}
    for _, r in gg.iterrows():
        par = old[r.station] if (r.day < eff and r.station in old and not (r.station == "C122")) else rat.get(r.station)
        if par is None and r.station == "C110":
            # the closed site's rating from 1 April: the rating book's closed-sites line
            m = re.search(r"C110 Mattin Creek at the gravel pit C110-R\d+ 1 Apr 2026 ([\d.]+) ([\d.]+) ([\d.]+)", t)
            par = tuple(float(m.group(i)) for i in (1, 2, 3))
        C, e, b = par
        qr = C * (r.gh - e) ** b
        s = chain.get(r.station, r.station)
        out.setdefault(s, []).append(100 * (r.q - qr) / qr)
    return {s: float(np.mean(v)) for s, v in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--record")
    a = ap.parse_args()
    first, errs = call(a.target)
    A = ask_a(a.target)
    B = ask_b(a.target)
    golden = {"C104": 1, "C105": 1, "C107": 5, "C112": 7, "C113": 7}
    say({k: v for k, v in first.items() if v} == golden, "call: C104 and C105 from January, C107 from May, C112 and C113 from July, 18 hold")
    say(len(first) == 23, "call: 23 stations")
    if a.record:
        rec = json.load(open(a.record))
        months = ["2025-10", "2025-11", "2025-12"] + ["2026-%02d" % m for m in range(1, 10)]
        labs = ["Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "May 2026", "Jun 2026",
                "Jul 2026", "Aug 2026", "Sep 2026"]
        for ym, lab in zip(months, labs):
            say(A.get(ym) == rec["A"][lab], "Ask A %s: %s" % (lab, A.get(ym)))
        for s, v in rec["B"].items():
            say(round(B[s], 1) == round(v, 1) and abs(B[s] - v) < 0.01, "Ask B %s: %.3f against %.3f" % (s, B[s], v))
        for s in rec["call"]["errs"]:
            for m in range(1, 13):
                gv = rec["call"]["errs"][s][str(m)] if str(m) in rec["call"]["errs"][s] else rec["call"]["errs"][s][m]
                say(abs(errs[(s, m)] - gv) < 1e-6, "call error %s month %d" % (s, m))
    fails = [l for l in LINES if l[0] == "FAIL"]
    for l in fails[:20]:
        print("FAIL", l[1])
    print("verify: %d checks, %d FAIL" % (len(LINES), len(fails)))
    print("VERIFY %s" % ("PASS" if not fails else "FAIL"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
