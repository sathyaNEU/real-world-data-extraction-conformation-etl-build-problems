"""Generator assertions for task273 architecture 6, run on the built target/ and the world's clean truth.

    python3 task273/generator/checks.py     # exit 1 on any failed assertion
"""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402
import make_pack as M  # noqa: E402
import pack as PK  # noqa: E402
import params as PR  # noqa: E402
import world as W  # noqa: E402

RES = []


def ok(name, cond, detail=""):
    RES.append((name, bool(cond), detail))


def half(v):
    return math.floor(v * 2 + 0.5) / 2.0


def edge(v):
    r = v * 2
    return abs(r - math.floor(r) - 0.5) / 2


def main():
    P = A.Pack(TARGET)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    w = W.simulate()
    lev, coef, a9 = A.golden(P)
    gold = A.verdict(P, lev)
    r0 = A.verdict(P, A.rung0(P))
    r1l, _ = A.rung1(P)
    r1 = A.verdict(P, r1l)
    r2l, a9d, _ = A.rung2(P)
    r2 = A.verdict(P, r2l)

    # ---- the ladder
    ok("golden: PB3 fails February and March, nothing else", gold == [("PB3", 2), ("PB3", 3)], str(gold))
    ok("rung 0 (own drought curves, PB9 on its own test): the plan holds", r0 == [], str(r0))
    ok("rung 1 (interference among existing bores, PB9 left out): the plan holds", r1 == [], str(r1))
    ok("rung 2 (PB9 by log distance from the existing pairs): PB4 fails February only", r2 == [("PB4", 2)], str(r2))
    ok("each rung names a different answer", len({str(gold), str(r0), str(r2)}) == 3)
    ok("golden PB3 Feb and Mar at least 0.3 m below minimum", min(lev[("PB3", m)] - P.mol["PB3"] for m in (2, 3)) >= 0.3)
    ok("golden PB3 Dec and Jan at least 0.3 m above minimum", min(P.mol["PB3"] - lev[("PB3", m)] for m in (12, 1)) >= 0.3)
    ok("golden every other cell at least 0.3 m above minimum",
       min(P.mol[i] - lev[(i, m)] for i in A.ALL for m in A.MONTHS if (i, m) not in gold) >= 0.3)
    ok("rung 2 PB4 Feb at least 0.3 m below, PB3 at least 0.3 m above",
       r2l[("PB4", 2)] - P.mol["PB4"] >= 0.3 and min(P.mol["PB3"] - r2l[("PB3", m)] for m in A.MONTHS) >= 0.3)
    ok("rung 0 every cell at least 1.0 m above minimum",
       min(P.mol[i] - v for (i, m), v in A.rung0(P).items()) >= 1.0)
    ok("PB9 footprint on PB3 at least 1.6x what distance gives", a9["PB3"] >= 1.6 * a9d["PB3"])
    ok("PB9 footprint on PB4 under a third of what distance gives", a9["PB4"] <= a9d["PB4"] / 3)
    ok("golden recovers the world within 5 cm on every cell",
       max(abs(lev[k] - v) for k, v in M.truth_levels(w, P.plan).items()) < 0.05)
    ok("every graded level at least 0.1 m inside its half-metre bin",
       min(edge(lev[(i, m)]) for i in A.EXISTING for m in A.MONTHS) >= 0.1)
    ok("PB9 footprint figures inside their bins", min(edge(a9[i] * 4.4) for i in ("PB3", "PB4")) >= 0.1)

    # ---- the three rules, executed on the clean truth
    bt, a = w["bt"], w["a"]
    clean = {}
    for m in A.MONTHS:
        y = 2019 if m == 12 else 2020
        lo = float(w["mb"][(w["mb"].index.year == y) & (w["mb"].index.month == m)].min())
        for i in W.IDS:
            nb = sum(a.at[i, j] * P.plan[m][j] for j in W.IDS if j != i)
            clean[(i, m)] = bt.at[i, "mp_rl"] - (lo + PR.MB_DATUM_OFFSET + bt.at[i, "offset"]
                                                  - bt.at[i, "own"] * P.plan[m][i] - nb)
    easy = [(i, m) for (i, m), v in clean.items() if v > bt.at[i, "mol_mbmp"]]
    ok("R3a analyst test: the easy route (every bore's own response, PB9's own drawdown) on the clean truth holds",
       easy == [], str(easy))
    step = [(i, m) for (i, m), v in clean.items() if v + a.at[i, "PB9"] * P.plan[m]["PB9"] > bt.at[i, "mol_mbmp"]]
    ok("R3b the decisive step alone (PB9's footprint added) files the golden", sorted(step) == sorted(gold), str(step))
    cols = set()
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                for line in fh.read().splitlines()[:8]:
                    cols |= {c.strip().lower() for c in line.split(",")}
    ok("R1 no shipped column holds an interference or drawdown-on-neighbour quantity",
       not any(re.search(r"interf|neighbo|footprint|drawdown", c) for c in cols))
    ok("R1 the decisive computation reads the daily log and the PB9 test record",
       P.q9.max() > 4.0 and len(P.L) > 4000)
    ok("R3c no repeated block: no bore's level series repeats a 14-day run",
       not any(_repeats(P.L[i].dropna().round(2).values) for i in A.EXISTING))

    # ---- Layer 1, each item mishandled leaves the call where it was
    d = P.daily
    ok("R2 duplicates: the re-sent August 2021 batch is exact and dropping it or not leaves the call",
       len(d) == len(d.drop_duplicates()) and _call_with(P, dedupe=False) == gold)
    ok("R2 old SCADA tags: fitting only from the 2019 tag change leaves the call",
       _call_window(P, "2019-05-14") == gold)
    ok("R2 test clock: reading the logger's UTC as local time leaves the call", _call_utc(P) == gold)
    ok("R2 datum: MB1 on NZVD2016 against Moturiki reduced levels is a constant the fit absorbs",
       _call_shift_mb(P, 0.27) == gold)
    ok("R2 missing rows: the 1.1 per cent telemetry gaps fall on no design-drought day",
       all(P.mb.index.isin(pd.date_range("2019-12-01", "2020-03-31")).sum() == 122 for _ in [0]))

    # ---- semantic forks on the main call
    ok("SF1 daily mean level: the standard defines the pumping water level as the logger's daily mean",
       "daily mean water level" in IO.pdf_text(P.path("SWS-03")))
    P29 = _clone(P, mb=P.mb.drop(pd.Timestamp("2020-02-29")))
    l29 = A.golden(P29)[0]
    ok("SF2 29 February 2020: with or without the 29th, the same call and graded levels",
       A.verdict(P29, l29) == gold and all(half(l29[k]) == half(lev[k]) for k in lev if k[0] != "PB9"))
    ok("SF3 datum: shifting MB1 by the Moturiki offset moves no graded level",
       _levels_shift_mb(P, 0.27) == {k: half(v) for k, v in lev.items() if k[0] != "PB9"})
    ok("SF4 PB9 in scope: the standard covers a bore entering supply under the plan",
       "entering supply" in IO.pdf_text(P.path("SWS-03")))
    ok("SF5 planned take every day: the standard takes each bore at its planned take on every day",
       "on every day" in IO.pdf_text(P.path("SWS-03")))
    l9a = A.forecast(P, coef, a9, reciprocity=True)
    l9b = A.forecast(P, coef, a9, reciprocity=False)
    ok("SF6 PB9's own level: with or without its neighbours' take adjustment it holds by 2 m or more",
       min(P.mol["PB9"] - l[("PB9", m)] for l in (l9a, l9b) for m in A.MONTHS) >= 2.0)
    summer = A.fit_full(P, True, window=("2021-01-01", "2026-10-31"))
    lw = A.forecast(P, summer, {i: -summer[i]["PB9"] for i in A.EXISTING})
    ok("SF7 fit window: the last six years alone give the same graded levels",
       all(half(lw[k]) == half(lev[k]) for k in lev if k[0] != "PB9"))
    ok("SF8 PB9 footprint by regression or by the before-and-after dip: same graded figures",
       _dip_agrees(P, a9))
    ok("SF9 the test's UTC day boundaries against local days: same call", _call_utc(P) == gold)
    ok("SF10 below means deeper than the minimum operating level: no cell within 0.3 m of it",
       min(abs(lev[k] - P.mol[k[0]]) for k in lev) >= 0.3)

    # ---- the asks
    g = A.ask_meters(P)
    s = A.ask_meters(P, match=False)
    inc = A.meter_increments(P)
    mp = A.meter_map(P, inc)
    ok("Ask B: matching puts every bore on exactly one Schedule 1 meter, PB4 on two",
       sorted(mp.values()) == sorted(A.EXISTING + ["PB4"]))
    ok("Ask B: four Schedule 1 meters read another bore", sum(mp[k] != v for k, v in A.SCHEDULE.items()) == 4)
    ok("Ask B: Schedule 1 handling misses at least 16 of 32 figures",
       sum(round(g[k]) != round(s[k]) for k in g) >= 16)
    ok("Ask B: the SCADA total is a different whole-ML figure on at least 28 of 32 bore-quarters",
       sum(round(g[(i, q)]) != round(_scada_q(P, i, q)) for i in A.EXISTING for q in range(1, 5)) >= 28)
    ok("Ask B: every whole-ML volume at least 0.1 ML inside its bin", min(abs((v % 1) - 0.5) for v in g.values()) >= 0.1)
    gb = _meters_reading_day(P)
    ok("Ask B: a reading's own date or its quarter-hour's start date gives the same whole-ML figures",
       all(round(gb[k]) == round(g[k]) for k in g))
    ge = A.ask_energy(P, meters=g)
    gh = A.ask_energy(P, split="hours", meters=g)
    ok("Ask A: the run-hours split misses all 16 shared-board figures",
       sum(round(ge[(i, q)]) != round(gh[(i, q)]) for i in ("PB5", "PB6", "PB7", "PB8") for q in range(1, 5)) == 16)
    ok("Ask A: every electricity figure at least 0.15 kWh/ML inside its whole-number bin",
       min(abs((v % 1) - 0.5) for v in ge.values()) >= 0.15)
    wy = P.daily[(P.daily["date"] >= "2025-07-01") & (P.daily["date"] <= "2026-06-30")]
    ok("Ask A: every shared-board pump has a SCADA row on every day of the year to 30 June 2026",
       all(wy[wy["bore"] == b]["date"].nunique() == 365 for b in ("PB5", "PB6", "PB7", "PB8")))
    gm = A.ask_energy(P, multiplier=False, meters=g)
    ok("Ask A: leaving the CT multiplier off moves PB2 in the quarters after 11 February",
       round(gm[("PB2", 3)]) != round(ge[("PB2", 3)]) and round(gm[("PB2", 4)]) != round(ge[("PB2", 4)]))
    ok("Ask figures match figures.json",
       all(fig["permit_meter_ml"]["%s Q%d" % k] == int(round(v)) for k, v in g.items())
       and all(fig["energy_kwh_per_ml"]["%s Q%d" % k] == int(round(v)) for k, v in ge.items()))
    gq = A.ask_energy(P, split="hours_kw_quarter", meters=g)
    ok("Ask A: splitting each board on its quarter's hours times kW gives the same figures as day by day",
       all(round(gq[k]) == round(ge[k]) for k in ge))
    ok("separation: no ask device row sits in a file the call reads",
       all(not f.startswith(("MRC_permit", "pump_icp", "kaitanga_icp")) for f in _call_files()))

    # ---- input gates and realism
    files = os.listdir(TARGET)
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    ok("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok("input gate: a file of 25,000 rows or more", big >= 25000, str(big))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("input gate: two distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    ok("distractors: the golden reads neither", all(not _reads(x) for x in meta["distractor_files"]))
    ok("no file describes the data", not any(re.search(r"readme|dictionar|notes|manifest|schema", f, re.I)
                                             for f in files))
    ok("no id column with a constant step", _no_constant_step(P))
    ok("bore names take more than two shapes", len({re.sub(r"\d", "#", n) for n in P.reg["Name"]}) > 4)
    ok("daily takes are not uniform across bores", P.Q.loc["2025-12"].mean().std() > 0.1)
    ok("call figures match figures.json",
       fig["call"]["failing"] == ["%s %s" % (i, A.MONTH_NAME[m]) for i, m in gold]
       and all(fig["lowest_level_m_bmp"]["%s %s" % (i, A.MONTH_NAME[m])] == half(lev[(i, m)])
               for i in A.EXISTING for m in A.MONTHS))
    ok("design drought MB1 minimum above the permit's 30.00 m trigger",
       min(P.drought_min(m) for m in A.MONTHS) > 30.05)
    ok("plan total within the permit's 28,500 m3 a day", max(sum(P.plan[m].values()) for m in A.MONTHS) < 28.5)

    bad = [r for r in RES if not r[1]]
    for n, c, dd in RES:
        print(("PASS " if c else "FAIL ") + n + (("  " + dd) if dd and not c else ""))
    print("%d assertions, %d failed" % (len(RES), len(bad)))
    sys.exit(1 if bad else 0)


# ------------------------------------------------------------------ helpers
def _repeats(x, n=14):
    seen = set()
    for k in range(len(x) - n):
        t = tuple(x[k:k + n])
        if t in seen:
            return True
        seen.add(t)
    return False


def _call_with(P, dedupe=True):
    d = P.daily if dedupe else pd.concat([P.daily, P.daily[P.daily["date_local"].between("2021-08-03", "2021-08-05")]])
    Q = d.groupby(["date", "bore"])["q"].mean().unstack()
    L = d.groupby(["date", "bore"])["pwl_mbmp"].mean().unstack()
    P2 = _clone(P, Q=Q, L=L)
    return A.verdict(P2, A.golden(P2)[0])


def _call_window(P, start):
    lev, *_ = _golden_window(P, (start, "2026-10-31"))
    return A.verdict(P, lev)


def _golden_window(P, window):
    coef = A.fit_full(P, True, window=window)
    a9 = {i: -coef[i]["PB9"] for i in A.EXISTING}
    return A.forecast(P, coef, a9), coef, a9


def _call_utc(P):
    q9 = P.test.set_index("utc")["q"].resample("D").sum() * 3600 / 1e6
    P2 = _clone(P, q9=q9)
    return A.verdict(P2, A.golden(P2)[0])


def _call_shift_mb(P, s):
    P2 = _clone(P, mb=P.mb + s)
    return A.verdict(P2, A.golden(P2)[0])


def _levels_shift_mb(P, s):
    P2 = _clone(P, mb=P.mb + s)
    return {k: half(v) for k, v in A.golden(P2)[0].items() if k[0] != "PB9"}


def _dip_agrees(P, a9):
    df = P.frame(True)
    full = df[df["PB9"] > 4.3].index
    near = df[(df["PB9"] == 0) & (df.index >= full[0] - pd.Timedelta(days=10))
              & (df.index <= full[-1] + pd.Timedelta(days=10))].index
    coef = A.fit_full(P, False)
    out = {}
    for i in ("PB3", "PB4"):
        res = (P.mp_rl[i] - df["L_" + i]) - df["mb"] - coef[i]["const"] - sum(coef[i][j] * df[j] for j in A.EXISTING)
        out[i] = -(res[full].mean() - res[near].mean()) / df.loc[full, "PB9"].mean()
    return all(half(out[i] * 4.4) == half(a9[i] * 4.4) for i in out)


def _meters_reading_day(P):
    inc = A.meter_increments(P)
    mp = A.meter_map(P, inc)
    inc = inc.assign(bore=inc["meter"].map(mp), day=(inc["local"] + pd.Timedelta(minutes=15)).dt.normalize())
    out = {}
    for qi, (a, b) in enumerate(A.QUARTERS):
        s = inc[(inc["day"] >= a) & (inc["day"] <= b)].groupby("bore")["v"].sum() / 1000.0
        for k in A.EXISTING:
            out[(k, qi + 1)] = float(s.get(k, 0.0))
    return out


def _clone(P, **kw):
    import copy
    P2 = copy.copy(P)
    for k, v in kw.items():
        setattr(P2, k, v)
    return P2


def _scada_q(P, i, q):
    a, b = A.QUARTERS[q - 1]
    return float(P.Q.loc[a:b, i].sum())


def _call_files():
    return [v for k, v in PK.FILES.items() if k in ("daily", "mb1", "register", "test", "plan", "standard")]


def _reads(name):
    src = open(os.path.join(HERE, "analysis.py"), encoding="utf-8").read()
    stem = name.split("_2")[0].split(".")[0]
    return stem in src


def _no_constant_step(P):
    for col in ("Easting (NZTM2000)", "Northing (NZTM2000)"):
        v = np.sort(P.reg[col].astype(float).values)
        if len(set(np.diff(v))) == 1:
            return False
    return True


if __name__ == "__main__":
    main()
