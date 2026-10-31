"""task156 assertions on the built pack: the input gates, the three rules on the generator's clean truth (R1 to R3),
the semantic fork rows (SF1 to SF20) on the shipped files, the rungs, the ask devices and their margins, the
separation of the asks from the call, and the realism sweep. Exit 1 on any failure.

    python3 task156/generator/checks.py"""
from __future__ import annotations

import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK      # noqa: E402
import estim as E      # noqa: E402
import hydro as H      # noqa: E402
import records as R    # noqa: E402
import world as W      # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FAILS = []


def check(label, ok, detail=""):
    print("%s  %-58s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)


def rnd(x):
    return int(np.floor(x + 0.5))


def edge(x, unit=1.0):
    return abs((x / unit) % 1.0 - 0.5)


def main():
    files = sorted(os.listdir(T))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    # ------------------------------------------------------------------ input gates
    check("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[-1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = [f for f in files if f.endswith(".csv") and sum(1 for _ in open(os.path.join(T, f), encoding="utf-8")) >= 25000]
    check("gate: a 25,000-row file", bool(big), ", ".join(big))
    check("gate: 2 or more distractors in metadata", len(meta["distractor_files"]) >= 2, ", ".join(meta["distractor_files"]))
    bad = [f for f in files if any(w in f.lower() for w in ("readme", "dictionary", "notes", "manifest", "distractor",
                                                            "schema", "codebook"))]
    check("gate: no file describes the data or names its role", not bad, ", ".join(bad) or "none")
    mtxt = json.dumps({k: v for k, v in meta.items() if k not in ("files", "distractor_files")}).lower()
    mtxt += " ".join(f["source"] for f in meta["files"]).lower()
    leaks = [w for w in ("water table", "groundwater", "infiltration", "below the", "submerged", "invert") if w in mtxt]
    check("gate: metadata.json names no method word", not leaks, ", ".join(leaks) or "none")

    # ------------------------------------------------------------------ the golden and the rungs
    G = E.golden(T)
    sub = E.subdivision()
    ex, su, up = G["existing"]["mean"], G["with_sub"]["mean"], G["with_upgrade"]["mean"]
    check("call: with the subdivision above the limit (hold)", su > 2.0, "%.2f a year" % su)
    check("call: as connected now above the limit", ex > 2.0, "%.2f" % ex)
    check("call: after the upgrade inside the limit", up < 2.0, "%.2f" % up)
    for name, v in (("existing", ex), ("with_sub", su), ("upgrade", up)):
        check("margin: %s a quarter of a whole overflow from an edge" % name, edge(v) >= 0.249, "%.2f, %.2f" % (v, edge(v)))
    check("call: margin over the limit at least 40 per cent", su >= 2.8, "%.2f" % su)
    N = G["naive"]
    check("R3a: the single response files connect (default path)", G["naive_sub"]["mean"] < 1.5,
          "%.2f a year with the subdivision" % G["naive_sub"]["mean"])
    check("R3a: the single response reproduces the meter's logged overflows", G["naive_sub"]["meter"] == [0, 0, 2]
          and G["existing"]["meter"] == [0, 0, 2], "%s / %s" % (G["naive_existing"]["meter"], G["existing"]["meter"]))
    # rung 0: the station's own record carried forward
    logged = sum(G["existing"]["meter"])
    years = (E.H1 - E.dt.datetime(2023, 12, 31, 11, tzinfo=E.UTC)).total_seconds() / (365.25 * 86400)
    check("rung 0: the meter's own rate files connect", logged / years < 1.5, "%.2f a year" % (logged / years))
    # rung 2: one set of responses per season and the dry weather flow by month
    seas = seasonal(T)
    check("rung 2: seasonal responses and monthly base file connect", seas < 1.5, "%.2f a year" % seas)
    # the bore read as a level, straight
    lin = level_linear(T)
    check("rung 3a: the bore as a straight level files connect (the inverts are needed)", lin < 2.0, "%.2f" % lin)
    # R3b: the decisive step alone
    check("R3b: conditioning on the length below the water table alone files hold", su > 2.0, "%.2f" % su)

    # ------------------------------------------------------------------ the deciding configuration is in the record
    check("record: the meter's wettest day reaches the replay's", G["lsub_meter_max"] >= 0.97 * G["lsub_replay_max"],
          "%.2f against %.2f km" % (G["lsub_meter_max"], G["lsub_replay_max"]))
    C = E.clock()
    ls = G["model"]["ls_d"]
    import datetime as dt
    rd = np.array([dt.date(2004, 1, 1) + dt.timedelta(days=int(k)) <= dt.date(2023, 12, 31) for k in range(C.nd)])
    above = int(np.sum(ls[rd] > G["lsub_meter_max"]))
    check("record: replay days above the meter's maximum", above <= 5, "%d days" % above)
    capped = dict(G["model"])
    capped["ls_d"] = np.minimum(ls, G["lsub_meter_max"])
    cv = E.replay(T, capped, sub)["mean"]
    check("record: capping at the meter's maximum leaves the figure", rnd(cv) == rnd(su), "%.2f" % cv)

    # ------------------------------------------------------------------ semantic forks
    def same(label, M=None, extra=sub, store=E.STORE, call_only=False, note=""):
        M = M or G["model"]
        v = E.replay(T, M, extra, store)["mean"]
        ok = (v > 2.0) if call_only else (rnd(v) == rnd(su))
        check(label, ok, "%.2f %s" % (v, note))
        return v

    check("SF1 average a year is the twenty years' overflows over twenty",
          abs(su - G["with_sub"]["per_year"].sum() / 20) < 1e-9, "%d / 20" % G["with_sub"]["per_year"].sum())
    q = E.model_flow(T, G["model"], sub)
    for sep, lab in ((12, "12 hours"), (0, "no merging")):
        ev = E.overflows(q, sep=sep)
        yrs = C.year[ev]
        v = float(np.mean([np.sum(yrs == y) for y in range(2004, 2024)]))
        check("SF2 overflow separation %s keeps the call" % lab, v > 2.0, "%.2f" % v)
    ev = E.overflows(q)
    yrs = C.year[ev]
    v22 = float(np.mean([np.sum(yrs == y) for y in range(2004, 2026)]))
    check("SF3 the archive's 22 years in place of the consent's 20 keep the call", v22 > 2.0, "%.2f" % v22)
    same("SF4 the catchment's dwellings scaled to the snapshot keep the figure",
         extra=sub + 0.014 * G["model"]["base"][C.how])
    same("SF5 stage 1 alone keeps the call", extra=E.subdivision(96), call_only=True)
    same("SF6 the subdivision's flow flat through the day keeps the figure", extra=E.subdivision(profile="flat"))
    v = E.replay(T, G["model"], sub)
    s1 = E.overflows(E.model_flow(T, G["model"], sub), qp=61.8)
    check("SF7 one pump in place of both keeps the call", float(np.mean([np.sum(C.year[s1] == y) for y in range(2004, 2024)])) > 2.0)
    same("SF8 the chamber's 312 m3 alone keeps the call", store=312.0, call_only=True)
    check("SF9 the upgrade's tank fills before the weir (the brief): its 1,100 m3 add to the 350", up < 2.0, "%.2f" % up)
    same("SF10 the archive read as hour beginning keeps the figure", M=E.fit(T, True, rain_shift=-1))
    cen = E.fit(T, True, ref="centre")
    cro = E.fit(T, True, ref="crown")
    check("SF11 the centreline reference fits the meter worse", cen["rmse"] > 1.3 * G["model"]["rmse"],
          "%.2f against %.2f" % (cen["rmse"], G["model"]["rmse"]))
    check("SF11 the crown reference fits the meter worse", cro["rmse"] > 1.3 * G["model"]["rmse"],
          "%.2f against %.2f" % (cro["rmse"], G["model"]["rmse"]))
    same("SF12 the abandoned mains counted keep the figure", M=E.fit(T, True, include_abandoned=True))
    same("SF13 the PE mains left out keep the figure", M=E.fit(T, True, skip_pe=True))
    same("SF14 the domestic pattern on NZST keeps the figure", M=E.fit(T, True, profile_clock="nzst"))
    same("SF15 a 48-hour dry window keeps the figure", M=E.fit(T, True, dry_h=48))
    same("SF16 the weir-crest hours kept in the fit keep the figure", M=E.fit(T, True, keep_spill=True))
    near = []
    for sf in E.SHAPES_F:
        for ss in E.SHAPES_S:
            Mx = E.fit(T, True, shapes=(sf, ss))
            if Mx["rmse"] <= 1.05 * G["model"]["rmse"] and (sf, ss) != (G["model"]["sf"], G["model"]["ss"]):
                near.append((sf, ss, E.replay(T, Mx, sub)["mean"]))
    check("SF17 every shape within 5 per cent of the best fit keeps the figure", all(rnd(v) == rnd(su) for *_, v in near),
          "; ".join("%s %s %.2f" % (a, b, v) for a, b, v in near) or "no other shape that close")
    nv = E.replay(T, dict(G["model"], ls_d=np.where(rd, np.median(ls[~rd]), ls)), sub)["mean"]
    check("SF18 holding the meter's water table through the replay is the naive reading (condition 7 closes it)",
          nv < 2.0, "%.2f" % nv)
    lvl = E.water_level(T)
    check("SF19 bore gaps are short", int(np.isnan(lvl).sum()) == 0, "joined")
    check("SF20 the 2026 provisional gap sits in dry weather", gap_dry(), "")

    # ------------------------------------------------------------------ the asks
    A = AK.ask_a(T)
    As = AK.ask_a(T, dwellings="snapshot")
    check("Ask A: every quarter clear of its rounding edge", all(edge(v) >= 0.25 for v in A.values()),
          "min %.2f" % min(edge(v) for v in A.values()))
    check("Ask A: the snapshot's dwellings miss every quarter", all(rnd(A[k]) != rnd(As[k]) for k in A),
          "%d of %d" % (sum(rnd(A[k]) != rnd(As[k]) for k in A), len(A)))
    Ae = AK.ask_a(T, estimates=True)
    check("Ask A hazard: the estimates moved", sum(rnd(A[k]) != rnd(Ae[k]) for k in A) >= 1)
    B = AK.ask_b(T)
    Bc = AK.ask_b(T, icps="current")
    hrs = [v for k, v in B.items() if "hours" in k]
    check("Ask B: spill hours clear of the half hour", all(edge(v) >= 0.25 for v in hrs), "min %.2f" % min(edge(v) for v in hrs))
    miss = sum(rnd(B[k]) != rnd(Bc[k]) for k in B)
    check("Ask B: the register's current ICPs miss ten figures", miss == 10, "%d of %d" % (miss, len(B)))
    Bl = AK.ask_b(T, attribution="latest")
    check("Ask B hazard: monitors placed at their latest station", sum(rnd(B[k]) != rnd(Bl[k]) for k in B) >= 4)
    # separation: no device row in the call's population
    sms = [r for r in csv.reader(open(os.path.join(T, R.F_MONITOR), encoding="utf-8"))][1:]
    ps03 = [r for r in sms if r[2].startswith("OM-2971") and "SPILL" in r[2]]
    check("separation: PS03's monitor carries only its two 2026 overflows", len(ps03) == 4, "%d messages" % len(ps03))
    check("separation: PS03's ICP never changed", "PS03" not in R.ICP_OLD)
    check("separation: no PS03 emergency overflow", not any(s == "PS03" and k == "emergency" for s, *_, k in R.spills()))
    call_files = {E.F_SCADA, E.F_RAIN, E.F_RAIN26, E.F_BORE, E.F_ASSETS}
    ask_files = {R.F_READS, R.F_ACCOUNTS, R.F_RATING, R.F_BC, R.F_MONITOR, R.F_OUTAGES, R.F_ICPS}
    check("separation: the call reads no ask file", not (call_files & ask_files))
    # ------------------------------------------------------------------ realism
    tr = H.truth()
    check("realism: the annual rain is ordinary", 1050 < np.mean([tr.rain[H.clock().year == y].sum() for y in range(2004, 2024)]) < 1450)
    pipes = E.ps03_pipes(T)
    check("realism: every PS03 main falls downstream", all(u > d for _, d, u, *_ in pipes))
    print("%d failed" % len(FAILS))
    sys.exit(1 if FAILS else 0)


def seasonal(target):
    """Rung 2: the dry weather flow by month and hour of the week, and one fast and one slow response per millimetre
    for May to October and another for November to April, all as the meter ran."""
    C = E.clock()
    rain = E.rainfall(target)
    q, spill = E.scada_hourly(target)
    import datetime as dt
    month = np.array([(E.H0 + dt.timedelta(hours=i)).astimezone(E.NZST).month for i in range(E.NH)])
    good = C.meter & ~np.isnan(q) & ~spill
    dry = good & (np.convolve(rain, np.ones(73))[:E.NH] == 0)
    base = np.zeros((13, 168))
    flat = np.array([q[dry & (C.how == k)].mean() for k in range(168)])
    for m in range(1, 13):
        for k in range(168):
            s = dry & (C.how == k) & (month == m)
            base[m, k] = q[s].mean() if s.sum() >= 2 else flat[k]
    bh = base[month, C.how]
    F = np.convolve(rain, E.uh(1.0, 6))[:E.NH] / 3.6
    S = np.convolve(rain, E.uh(9.0, 72))[:E.NH] / 3.6
    win = (month >= 5) & (month <= 10)
    pred = bh.copy()
    for sel in (win, ~win):
        A = np.vstack([F[good & sel], S[good & sel]]).T
        a, b = np.linalg.lstsq(A, (q - bh)[good & sel], rcond=None)[0]
        pred = np.where(sel, bh + a * F + b * S, pred)
    ev = E.overflows(pred + E.subdivision())
    yrs = C.year[ev]
    return float(np.mean([np.sum(yrs == y) for y in range(2004, 2024)]))


def level_linear(target):
    """The bore's level itself, above its lowest meter reading, in place of the length below the water table."""
    lv = E.water_level(target)
    x = np.maximum(lv - np.percentile(lv[-1035:], 5), 0)
    M2 = E.fit(target, True, exposure=x)
    return E.replay(target, M2, E.subdivision())["mean"]


def gap_dry():
    g0, n = R.RAIN26_GAP
    i0 = int((g0 - W.H0).total_seconds() // 3600)
    return float(H.truth().rain[i0:i0 + n // 4 + 2].sum()) < 1.0


if __name__ == "__main__":
    main()
