"""task159 checks: the generator's assertions on the built pack (target/) and on the clean truth (world.py, sim.py).

The three-rules block (R1 to R3c), the ladder and its rivals, the out-of-sample test, the golden's family and its
one-sigma corridor, every semantic fork row (SF1 to SF12), both asks with their devices and stops, the separation
line, the input gates, the realism sweep, the document dates and the distractors' deletion test."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import statistics as stx
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402
import docs as DOC      # noqa: E402
import pack as PK       # noqa: E402
import sim as S         # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


GOLD_TOTAL = 26
GOLD_WD = {"Mon": 4, "Tue": 6, "Wed": 6, "Thu": 6, "Fri": 4}
R0_TOTAL = 35


def nearest(fc):
    return min(abs(fc[c][w] - C.THRESH) for c in fc for w in C.WD)


def main():
    M = C.Model(TARGET)
    fc = M.forecast()
    total, per_wd, posts = C.tally(fc)

    # ------------------------------------------------------------------------------------------ the golden
    check("GOLD total shifts a week", total == GOLD_TOTAL, "%d" % total)
    check("GOLD shifts by weekday", per_wd == GOLD_WD, str(per_wd))
    five = sorted(c for c in posts if posts[c] == C.WD)
    three = sorted(c for c in posts if posts[c] == ["Tue", "Wed", "Thu"])
    check("GOLD posted every weekday", five == ["ALB-6", "COR-2", "GAR-2", "QUA-6"], str(five))
    check("GOLD posted Tuesday to Thursday", three == ["SAL-1S", "SAL-4S"], str(three))
    check("GOLD COR-5W not posted", posts["COR-5W"] == [], "%s" % ["%.3f" % fc["COR-5W"][w] for w in C.WD])
    check("GOLD nearest platform-weekday to the line", nearest(fc) >= 0.10, "%.3f" % nearest(fc))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    check("GOLD figures.json carries the call", figs["shifts_per_week"] == total)

    # ------------------------------------------------------------------------------------------ R1
    heads = []
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            heads += open(p, encoding="utf-8").readline().strip().lower().split(",")
    xl = pd.ExcelFile(os.path.join(TARGET, PK.F_COUNTS))
    for sh in xl.sheet_names:
        if sh != "Method":
            heads += [str(c).lower() for c in xl.parse(sh, nrows=1).columns]
    heads += [str(c).lower() for c in pd.read_excel(os.path.join(TARGET, PK.F_CENSUS), nrows=1).columns]
    bad = [h for h in heads if re.search(r"left|behind|backlog|room|queue|unable|board(ed|ings)|load_in", h)]
    check("R1 no shipped column holds a backlog, a room or boardings", not bad, str(bad))
    check("R1 the census ships platform flows by quarter-hour", len(M.P.census) > 4000 and
          set(M.P.census.Direction) == {"to platform", "from platform", "passage"}, "%d rows" % len(M.P.census))
    check("R1 the timetable ships every trip", len(M.P.tt) > 30000, "%d rows" % len(M.P.tt))
    check("R1 the fare export ships hourly entries per complex", len(M.P.fare) > 700000, "%d rows" % len(M.P.fare))

    # ------------------------------------------------------------------------------------------ R3 on clean truth
    ref = W.year_level(dt.date(2026, 10, 15))

    def season(wd):
        ds = [d for d in K.pick_dates() if K.WD[d.weekday()] == wd]
        return stx.mean(W.MONTH[d.month] * W.year_level(d) / ref for d in ds)

    def truth(plan, wd, mult=1.0, room=None):
        out, _a, _x, _t = S.run_all(lambda s: W.weekday_factor(s, wd) * season(wd) * mult, plan=plan)
        return {k: S.peak_quarter(S.platform_series(out, k))[0] / W.CAPACITY[k] for k in W.WATCH_KEYS}

    gt = {wd: truth("spring2027", wd) for wd in C.WD}
    g_total = sum(1 for wd in C.WD for k in W.WATCH_KEYS if gt[wd][k] > 0.85)
    check("R3b the queue on the clean truth files the golden", g_total == GOLD_TOTAL, "%d" % g_total)
    # the easy route on the clean truth: mid-week autumn peaks carried by weekday and season
    aut_lv = stx.mean(W.MONTH[m] for m in (10, 11))
    mids = {}
    for wd in ("Tue", "Wed", "Thu"):
        out, _a, _x, _t = S.run_all(lambda s: W.weekday_factor(s, wd) * aut_lv, plan="autumn2026")
        for k in W.WATCH_KEYS:
            mids.setdefault(k, []).append((S.peak_quarter(S.platform_series(out, k))[0], W.weekday_factor(k.split("|")[0], wd)))
    r0 = 0
    for k in W.WATCH_KEYS:
        st = k.split("|")[0]
        mid_pk = np.mean([x for x, _f in mids[k]])
        mid_f = np.mean([f for _x, f in mids[k]])
        for wd in C.WD:
            v = mid_pk * W.weekday_factor(st, wd) / mid_f * season(wd) / aut_lv / W.CAPACITY[k]
            r0 += v > 0.85
    check("R3a the easy route on the clean truth files the default path", r0 == R0_TOTAL, "%d" % r0)
    nq = 0
    for wd in C.WD:
        out, _a, _x, _t = S.run_all(lambda s: W.weekday_factor(s, wd) * season(wd), plan="spring2027", car_max=10 ** 6)
        nq += sum(1 for k in W.WATCH_KEYS if S.peak_quarter(S.platform_series(out, k))[0] / W.CAPACITY[k] > 0.85)
    check("R3b one headway's arrivals on the clean truth stays wrong", nq == 20, "%d" % nq)
    six = sum(1 for wd in C.WD for k, v in truth("autumn2026", wd).items() if v > 0.85)
    check("R3b the queue on six-car Line 5 stays wrong", six == 29, "%d" % six)
    band = {}
    for mult in (0.94, 0.97, 1.03, 1.06):
        band[mult] = sum(1 for wd in C.WD for k in W.WATCH_KEYS if truth("spring2027", wd, mult)[k] > 0.85)
    check("R3b the golden holds from 6 per cent under to 6 per cent over", all(v == GOLD_TOTAL for v in band.values()),
          str(band))
    docs_text = " ".join(" ".join(p) for _h, p in DOC.STANDARD + DOC.MANUAL) + " " + " ".join(
        " ".join(T["notes"]) + T["pick"] for T in DOC.PLAN_TEXT.values())
    check("R3c no shipped document states a shift count or a forecast",
          not re.search(r"\b\d+\s+(shifts|conductors|postings)\b", docs_text), "")
    check("R3c no document says how a crowd responds to fewer riders or longer trains",
          not re.search(r"left behind|unable to board|backlog|wait for the next|queue", docs_text, re.I), "")

    # ------------------------------------------------------------------------------------------ R2 mess neutrality
    r2 = {"the fare export's UTC hours read as local": C.Model(TARGET, tz_mode="utc_as_local"),
          "the fare export converted at four hours all year": C.Model(TARGET, tz_mode="fixed4"),
          "the census's quarter-hours read as ending at their label": C.Model(TARGET, quarter_shift=-1)}
    for name, Mx in r2.items():
        t = C.tally(Mx.forecast())
        check("R2 %s: same call" % name[:40], t[0] == total and t[2] == posts, "%d" % t[0])
    leg = pd.read_csv(os.path.join(TARGET, PK.F_LEGACY))
    leg = leg[leg.period_end.isin(["08:00", "12:00"])]
    leg["d"] = pd.to_datetime(leg.svc_date).dt.date
    byd = leg.groupby("d").entries.sum()
    fed = C.FEDERAL | {dt.date(2023, 11, 23), dt.date(2023, 11, 24), dt.date(2023, 10, 9), dt.date(2023, 11, 10),
                       dt.date(2024, 5, 27), dt.date(2024, 6, 19)}

    def lmean(a, b):
        return np.mean([v for d, v in byd.items() if a <= d <= b and d.weekday() < 5 and d not in fed])
    r_leg = lmean(dt.date(2024, 3, 1), dt.date(2024, 6, 25)) / lmean(dt.date(2023, 9, 8), dt.date(2023, 12, 18))
    t = C.tally(C.Model(TARGET, spring_year_ratio=r_leg).forecast())
    check("R2 a spring ratio read off the legacy reads (2024 over 2023): same call", t[0] == total and t[2] == posts,
          "ratio %.4f" % r_leg)

    # ------------------------------------------------------------------------------------------ the ladder
    lad = {}
    lad["R0"] = C.tally(C.default_path(M))[0]
    lad["R0 hybrid days"] = C.tally(C.default_path(M, use_hybrid=True))[0]
    lad["R0 eight-car scaled"] = C.tally(C.default_path(M, scale_8car=True))[0]
    lad["R0 counts as they are"] = C.tally(C.rival_counts_as_is(M))[0]
    lad["R1 one headway"] = C.tally(C.forecast_no_queue(M))[0]
    lad["R2 queue, six-car Line 5"] = C.tally(M.forecast(plan="AUT26"))[0]
    lad["R2 queue, constant room"] = C.tally(C.forecast_constant_room(M))[0]
    lad["R2 queue, planning load"] = C.tally(M.forecast(car_load=110))[0]
    lad["R2 complex level"] = C.tally(C.rival_complex_level(M))[0]
    lad["R2 equal split"] = C.tally(C.rival_equal_split(M))[0]
    lad["R2 weekly average of R0"] = C.tally(C.rival_weekly_average(C.default_path(M)))[0]
    lad["R2 weekly average of the golden"] = C.tally(C.rival_weekly_average(fc))[0]
    osc, k1 = C.rival_one_scalar(M)
    lad["R2 one-scalar calibration"] = C.tally(osc)[0]
    lad["R2 per-platform calibration"] = C.tally(C.rival_per_platform_scalar(M))[0]
    check("LADDER default path", lad["R0"] == R0_TOTAL, "%d" % lad["R0"])
    for name, v in lad.items():
        check("LADDER %s misses the golden" % name, v != GOLD_TOTAL, "%d" % v)

    # ------------------------------------------------------------------------------------------ out of sample
    fa = M.forecast(plan="AUT26", spring=False)
    pk = C.count_peaks(M.P, "COR-5W")
    cap = M.caps["COR-5W"]
    obs = {C.WD[d.weekday()]: v[0] / cap for d, v in pk.items()}
    r0a = C.default_path(M, spring=1.0)
    check("OOS hybrid Monday and Friday at COR-5W reject the proportional carry (counted under half of it)",
          all(r0a["COR-5W"][w] > 2 * obs[w] for w in ("Mon", "Fri")),
          "R0 %.2f/%.2f, counted %.2f/%.2f" % (r0a["COR-5W"]["Mon"], r0a["COR-5W"]["Fri"], obs["Mon"], obs["Fri"]))
    check("OOS the queue model meets the hybrid days at COR-5W",
          all(abs(fa["COR-5W"][w] - obs[w]) < 0.08 for w in ("Mon", "Fri")),
          "model %.2f/%.2f" % (fa["COR-5W"]["Mon"], fa["COR-5W"]["Fri"]))
    mid_obs = {}
    for code in ("SAL-1S", "SAL-4S", "COR-5W"):
        p2 = C.count_peaks(M.P, code)
        mid_obs[code] = np.mean([v[0] for d, v in p2.items() if d.weekday() in (1, 2, 3)]) / M.caps[code]
    nqa = C.forecast_no_queue_plan(M, "AUT26", spring=False)
    check("OOS one headway's arrivals misses the mid-week counts (counted over twice it)",
          all(mid_obs[c] > 2 * max(nqa[c][w] for w in C.WD) for c in mid_obs),
          "counted %s, one headway at most %s" % ({c: round(float(v), 2) for c, v in mid_obs.items()},
                                                  {c: round(max(nqa[c][w] for w in C.WD), 2) for c in mid_obs}))
    check("OOS the queue model builds a mid-week backlog where it was counted",
          all(min(fa[c][w] for w in ("Tue", "Wed", "Thu")) > 1.0 for c in mid_obs), "")
    e_q = e_r = 0.0
    for code in ("GAR-2", "HES-3", "COR-5W", "FER-5W", "ALB-6", "QUA-6"):
        p3 = C.count_peaks(M.P, code)
        for d, v in p3.items():
            if d.weekday() in (0, 4):
                wd = C.WD[d.weekday()]
                o = v[0] / M.caps[code]
                e_q += abs(fa[code][wd] - o)
                e_r += abs(r0a[code][wd] - o)
    check("OOS over the hybrid-day sample the queue model errs under half the proportional carry", e_q < e_r / 2,
          "mean abs error %.3f against %.3f" % (e_q / 12, e_r / 12))

    # ------------------------------------------------------------------------------------------ the family
    fam = {}
    for sp in (0.3, 0.7):
        fam["island split %.1f" % sp] = C.Model(TARGET, island_split=sp).forecast()
    for name, r in (("spring 2025 ratio", M.r2025), ("spring flat", 1.0), ("spring 0.985", 0.985),
                    ("spring 1.03", 1.03), ("spring mean", (M.r2025 + M.r2026) / 2)):
        fam[name] = C.Model(TARGET, spring_year_ratio=r).forecast()
    fam["hours 07-09"] = C.Model(TARGET, hours=(7, 8, 9)).forecast()
    fam["hours 05-10"] = C.Model(TARGET, hours=(5, 6, 7, 8, 9, 10)).forecast()
    for L in (120, 135, 145):
        fam["load %d a car" % L] = M.forecast(car_load=L)
    for name, f in fam.items():
        t = C.tally(f)
        check("FAMILY %s files the golden" % name, t[0] == GOLD_TOTAL and t[1] == GOLD_WD and t[2] == posts,
              "%d, nearest %.3f" % (t[0], nearest(f)))
    check("FAMILY nearest cell across the family", min(nearest(f) for f in fam.values()) >= 0.07,
          "%.3f" % min(nearest(f) for f in fam.values()))
    # one sigma: the spring ratio's year-to-year spread and the census normalisation's day noise
    sig = abs(M.r2025 - M.r2026) + 0.02
    for s_ in (1 - sig, 1 + sig):
        f = C.Model(TARGET, spring_year_ratio=M.r2026 * s_).forecast()
        check("SIGMA spring level x%.3f files the golden" % s_, C.tally(f)[0] == GOLD_TOTAL, "")

    # ------------------------------------------------------------------------------------------ car load
    # the queue model across the load per car: the landing range of the golden, and the counts' back-cast at the
    # three platforms with a mid-week backlog (SAL-1S, SAL-4S, COR-5W) against the counted mid-week mean
    land = {}
    err = {}
    for L in range(110, 161, 5):
        land[L] = C.tally(M.forecast(car_load=L))
        fa_L = M.forecast(plan="AUT26", spring=False, car_load=L)
        err[L] = {c: np.mean([fa_L[c][w] for w in ("Tue", "Wed", "Thu")]) / mid_obs[c] - 1 for c in mid_obs}
    inside = [L for L in land if land[L][0] == GOLD_TOTAL and land[L][2] == posts]
    check("CARLOAD the golden at every load from 120 to 155 a car", all(L in inside for L in range(120, 156, 5)),
          "landing %d to %d" % (min(inside), max(inside)))
    check("CARLOAD the fleet register's planning load (110) misses", 110 not in inside, "%d" % land[110][0])
    fit = min(err, key=lambda L: np.mean([abs(v) for v in err[L].values()]))
    check("CARLOAD the counts' best fit lies 20 a car or more inside the landing range",
          fit in inside and fit - 20 >= min(inside) and fit <= 150,
          "best fit %d (mean error %.2f)" % (fit, np.mean([abs(v) for v in err[fit].values()])))
    check("CARLOAD under the landing range the back-cast is over twice the mid-week counts at every backlog platform",
          all(err[L][c] > 1.0 for L in land if L < min(inside) for c in mid_obs),
          str({L: [round(v, 2) for v in err[L].values()] for L in land if L < min(inside)}))
    check("CARLOAD the sweep (shifts; back-cast against the counts at SAL-1S, SAL-4S, COR-5W)", True,
          "; ".join("%d: %d (%s)" % (L, land[L][0], ", ".join("%+.2f" % v for v in err[L].values())) for L in land))
    check("CARLOAD over the register's maximum (160 a car) the call moves", 160 not in inside, "%d" % land[160][0])
    check("CARLOAD at the register's maximum (150) the back-cast reads under the counts at every backlog platform",
          all(v < 0 for v in err[150].values()), "")
    held = [L for L in land if np.mean([abs(v) for v in err[L].values()]) <= 0.20]
    check("CARLOAD every load the counts hold within 20 per cent on average files the golden",
          held and all(L in inside for L in held), str(held))

    # ------------------------------------------------------------------------------------------ semantic forks
    sf = {}
    sf["SF1"] = (total == sum(len(posts[c]) for c in posts), "one shift a week per platform-weekday posted")
    strict = sum(1 for c in fc for w in C.WD if fc[c][w] >= C.THRESH)
    sf["SF2"] = (strict == total, "more than 85 per cent against at least: same call")
    cap_now = dict(M.caps)
    cap_now["FER-4S"] = 300
    alt = {c: {w: fc[c][w] * M.caps[c] / cap_now[c] for w in C.WD} for c in fc}
    sf["SF3"] = (C.tally(alt)[0] == total, "rated capacity on 1 March 2027 against the rating in force at the pull")
    # SF4 quarter-hours: hour-long windows would be another estimand; the filed quarter-hour vs a 15-minute window
    # sliding on the minute
    sf["SF4"] = ("among the quarter-hours starting at 07:00, 07:15 and so on to 09:30, local time" in docs_text,
                 "quarter-hours starting 07:00 to 09:30, filed in the standard")
    # SF5 island: everyone on the island against the arriving direction's riders only
    out_t = C.run_all(M.P, M.C, "SPR27", M.factor("Fri"))
    isl = {}
    for code, st, lab in C.WATCH:
        line, d = C.plat_key(lab)
        if d is None:
            d1, d2 = C.LINE_DIRS[line]
            ser = sorted([(t, c) for (t, c, _l) in out_t[(line, d1)][st]] + [(t, c) for (t, c, _l) in out_t[(line, d2)][st]])
            isl[code] = C.peak_quarter(ser)[0] / M.caps[code]
    sf["SF5"] = (all(v < 0.85 for v in isl.values()) and all(fc[c]["Fri"] > 0.85 for c in ("GAR-2", "COR-2", "ALB-6", "QUA-6")),
                 "everyone on the island (filed): the arriving direction alone is a different estimand, ruled out by the standard")
    # SF6 average weekday: the forecast at each spring month's level against the pick's average
    ok6 = True
    for r in (0.95 * M.r2026 / 0.985, 1.0 * M.r2026 / 0.985):
        f = C.Model(TARGET, spring_year_ratio=r).forecast()
        ok6 &= C.tally(f)[0] == total
    sf["SF6"] = (ok6, "an average weekday of the pick against March's and June's levels: same call")
    sf["SF7"] = ("09:30, local time" in docs_text and "All times are local" in " ".join(
        str(x) for x in pd.read_excel(os.path.join(TARGET, PK.F_COUNTS), sheet_name="Method", header=None)[0]),
        "local time for the quarter-hours, filed in the standard and the counts")
    sf["SF8"] = ("Every weekday on which the weekday timetable runs is a weekday of the pick" in docs_text and
                 "Memorial Day, Monday 31 May" in docs_text,
                 "weekdays of the pick: the weekday timetable runs (Memorial Day out, Juneteenth in), filed")
    # SF9 the morning peak as the mean over a quarter's trains against the largest single train's crowd
    mx = {}
    outs = {wd: C.run_all(M.P, M.C, "SPR27", M.factor(wd)) for wd in ("Mon", "Fri")}
    for code, st, lab in C.WATCH:
        ser = C.platform_series(outs["Mon"], st, lab)
        mx[code] = max(c for (t, c) in ser if 420 <= t < 585) / M.caps[code]
    sf["SF9"] = (mx["SAL-1S"] < 0.85 and mx["SAL-4S"] < 0.85 and mx["COR-5W"] < 0.85,
                 "mean over a quarter's trains (filed); the largest train's crowd posts the same queue platforms")
    sf["SF10"] = ("the number of people on the platform as a train arrives, before its doors open" in docs_text,
                  "accumulation before the doors open (filed); after the doors close is another quantity")
    sf["SF11"] = (C.tally(C.Model(TARGET, hours=(7, 8, 9)).forecast())[0] == total,
                  "the fare export's morning window for the weekday index: same call")
    hol = C.Model(TARGET)
    hol.idx = C.weekday_index(hol.me, sorted(hol.P.name_of), drop=set())
    sf["SF12"] = (C.tally(hol.forecast())[0] == total, "federal holidays kept in the weekday index: same call")
    for k_, (ok, txt) in sf.items():
        check("%s %s" % (k_, txt[:44]), ok, "")

    # ------------------------------------------------------------------------------------------ the asks
    A = C.ask_a(TARGET)
    for route in ("natural", "dir_only", "speed_only"):
        r = C.ask_a(TARGET, route)
        miss = all(r[cx][i] != A[cx][i] for cx in C.WATCH_COMPLEXES for i in (0, 1))
        check("ASK A the %s route misses every figure" % route, miss, "")
    vals = [A[cx][i] for cx in C.WATCH_COMPLEXES for i in (0, 1)]
    top = max(vals.count(v) for v in vals)
    check("ASK A no constant response keeps more than two figures", top <= 2, "%d" % top)
    B = C.ask_b(TARGET)
    for route in ("work_orders", "monitoring"):
        r = C.ask_b(TARGET, route)
        gap = min(abs(r[cx] - B[cx]) for cx in C.WATCH_COMPLEXES)
        check("ASK B the %s route misses every figure by 0.15 h or more" % route, gap >= 0.15, "%.2f" % gap)
    edge = min(0.05 - abs(B[cx] - round(B[cx], 1)) for cx in C.WATCH_COMPLEXES)
    check("ASK B every figure clear of its rounding edge", edge >= 0.004, "%.4f h" % edge)
    dirs = C.escalator_directions_peak(TARGET)
    check("ASK A every platform escalator keeps one direction from 07:00 to 09:30 on every autumn weekday",
          all(len(v) == 1 for v in dirs.values()), "")
    au = C.ask_a(TARGET, unrounded=True)
    ea = min(0.5 - abs(v - round(v)) for cx in C.WATCH_COMPLEXES for v in au[cx])
    check("ASK A every figure a whole number of people a minute before rounding", ea >= 0.499, "%.2f" % ea)
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    manual = " ".join(" ".join(p) for _h, p in DOC.MANUAL)

    MOVED = {}

    def moved_a(route):
        r = C.ask_a(TARGET, route)
        mv = ["%s %s %d" % (cx, ("down", "up")[i], r[cx][i]) for cx in C.WATCH_COMPLEXES for i in (0, 1)
              if r[cx][i] != A[cx][i]]
        MOVED[("A", route)] = mv
        return len(mv)

    def moved_b(route):
        r = C.ask_b(TARGET, route)
        mv = ["%s %.1f" % (cx, r[cx]) for cx in C.WATCH_COMPLEXES if round(r[cx], 1) != round(B[cx], 1)]
        MOVED[("B", route)] = mv
        return len(mv)

    check("ASK A weighted over the window with no allowance for stoppages: the golden", moved_a("time_weighted") == 0, "")
    closes = [
        ("A", "fault_deducted", "fault minutes deducted", "make no allowance for stoppages" in manual),
        ("A", "watch_only", "watch-list platforms only", "between its mezzanines and any of its platforms" in prompt),
        ("A", "with_holidays", "holiday-timetable days in",
         "the days of the autumn 2026 pick that ran the weekday timetable" in prompt),
        ("A", "utc_window", "the log's UTC as local", "all times local" in prompt),
        ("B", "with_holidays", "holiday-timetable days in",
         "the days of the autumn 2026 pick that ran the weekday timetable" in prompt),
        ("B", "mean_per_day", "a mean per morning", "the total elevator-hours" in prompt),
        ("B", "platform_only", "street elevators out", "all its elevators" in prompt),
        ("B", "utc_window", "the logs' UTC as local", "all times local" in prompt),
        ("B", "summed", "overlaps counted twice", "more than one reason at once counts once" in manual),
    ]
    for ask, route, what, filed in closes:
        n = moved_a(route) if ask == "A" else moved_b(route)
        check("ASK %s %s moves %d figures, closed by filed text" % (ask, what, n), n >= 1 and filed,
              "; ".join(MOVED[(ask, route)]) if n <= 5 else "")
    gb = C.ask_b(TARGET, "with_holidays")
    check("ASK B holiday days in: Garnett Street %.1f against %.1f" % (gb["Garnett Street"], B["Garnett Street"]),
          round(gb["Garnett Street"], 1) != round(B["Garnett Street"], 1), "")
    check("ASK B out of service from the stop: the manual's union of fault and maintenance",
          "from the moment it stops on a fault, or is taken out of service for maintenance" in manual, "")
    main_files = {C.F_FARE, C.F_CENSUS, C.F_COUNTS, C.F_CAP, C.F_TT, C.F_FLEET, C.F_COMPLEX}
    ask_files = {C.F_INV, C.F_ASSET, C.F_CTRL, C.F_WO, C.F_MON}
    src = open(os.path.join(HERE, "calc.py")).read()
    pack_cls = src[src.index("class Pack"):src.index("def fare_local")]
    check("SEPARATION the golden reads none of the ask files", not any(f in pack_cls for f in
                                                                       ("F_INV", "F_ASSET", "F_CTRL", "F_WO", "F_MON")), "")
    check("SEPARATION the asks read none of the main call's records",
          not any(x in src[src.index("# ---------------------------------------------------------------------------------------------------- Ask A"):]
                  for x in ("F_CENSUS", "F_COUNTS", "F_FARE", "F_TT")), "")

    # ------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(TARGET))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("GATES ten or more files", len(files) >= 10, "%d" % len(files))
    check("GATES three or more formats", len(fmts) >= 3, str(sorted(fmts)))
    check("GATES a file of 25,000 rows or more", meta["input_gates"]["largest_file_rows"] >= 25000,
          "%s %d" % (meta["input_gates"]["largest_file"], meta["input_gates"]["largest_file_rows"]))
    dis = meta["distractor_files"]
    check("GATES two distractors, shipped, none named as such", len(dis) >= 2 and all(d in files for d in dis) and
          not any("distract" in f for f in files), str(dis))

    # ------------------------------------------------------------------------------------------ distractor deletion
    tmp = tempfile.mkdtemp(prefix="nodis_", dir=TASK)
    try:
        for f in files:
            if f not in dis:
                os.symlink(os.path.join(TARGET, f), os.path.join(tmp, f))
        M2 = C.Model(tmp)
        t2 = C.tally(M2.forecast())
        check("DISTRACTORS deleted: the golden unchanged", t2[0] == total and t2[2] == posts, "%d" % t2[0])
        check("DISTRACTORS deleted: both asks unchanged", C.ask_a(tmp) == A and C.ask_b(tmp) == B, "")
    finally:
        for f in os.listdir(tmp):
            os.unlink(os.path.join(tmp, f))
        os.rmdir(tmp)

    # ------------------------------------------------------------------------------------------ realism sweep
    f = M.P.fare
    loc_d = f.hour_utc.dt.tz_convert("America/New_York").dt.date
    vec = f.assign(ld=loc_d).groupby(["complex_id", "ld"]).entries.apply(tuple)
    vec = vec[vec.map(len) >= 10]
    check("REALISM no complex-day of the fare export repeats another's hours", not vec.duplicated().any(),
          "%d complex-days" % len(vec))
    cen = M.P.census
    blocks = cen.groupby(["Location ID", "Direction"]).People.apply(tuple)
    blocks = blocks[blocks.map(sum) > 0]
    check("REALISM no census location repeats another's quarter-hours", not blocks.duplicated().any(),
          "%d counted blocks" % len(blocks))
    cnt = pd.concat(M.P.counts.values())
    check("REALISM count sheets carry estimates in tens and counts below 200",
          set(cnt.People[cnt.Est == "E"] % 10) == {0} and (cnt.People[cnt.Est != "E"] < 210).all(), "")
    tot = int(f.entries.sum())
    check("REALISM the export's total is not round", tot % 1000 != 0, "%d" % tot)
    names = ["Beth Lewis", "Ralph Chambers", "Mary Wheeler", "Caleb Rowe"]
    text = ""
    for fn in files:
        if fn.endswith(".pdf"):
            text += open(os.path.join(TARGET, fn), "rb").read().decode("latin-1")
    check("REALISM no shipped file carries an em or en dash", not any(
        "\u2014" in open(os.path.join(TARGET, fn), encoding="utf-8", errors="ignore").read() or
        "\u2013" in open(os.path.join(TARGET, fn), encoding="utf-8", errors="ignore").read()
        for fn in files if fn.endswith(".csv")), "")
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("REALISM the submission carries no em dash", "\u2014" not in sub and "\u2013" not in sub, "")

    capreg = pd.read_csv(os.path.join(TARGET, PK.F_CAP))
    check("REALISM the capacity register states its rating basis on every row",
          capreg.basis.str.contains("1 person per sq m of").all(), "")
    cnt_text = " ".join(str(x) for x in pd.read_excel(os.path.join(TARGET, PK.F_COUNTS), sheet_name="Method",
                                                      header=None)[0])
    check("REALISM the count contractor is Tollison Field Data", "Tollison Field Data" in cnt_text and
          "Halvorsen" not in cnt_text, "")

    # ------------------------------------------------------------------------------------------ dates
    last_fare = f.hour_utc.max()
    check("DATES the fare export ends with the 10 January service day's last hour (00:00 local on the 11th)",
          last_fare.tz_convert("America/New_York").strftime("%Y-%m-%d %H") == "2027-01-11 00", str(last_fare))
    ctrl = pd.read_csv(os.path.join(TARGET, PK.F_CTRL))
    wo = pd.read_csv(os.path.join(TARGET, PK.F_WO))
    check("DATES no log record after the pull", max(ctrl.event_utc.max(), wo.in_service_at.max()) < "2027-01-11 14:40",
          "%s %s" % (ctrl.event_utc.max(), wo.in_service_at.max()))
    late = set()
    for fn in files:
        if fn.endswith(".csv"):
            txt = open(os.path.join(TARGET, fn), encoding="utf-8").read()
            if any(d > "2027-01-11" for d in re.findall(r"\b20\d\d-\d\d-\d\d\b", txt)):
                late.add(fn)
    check("DATES only the forward-looking registers carry dates after the pull (H16 allow-list)",
          late == {PK.F_CAP, PK.F_CHANGES}, str(sorted(late)))
    check("DATES every document issued before the pull", max(DOC.STANDARD_DATE, DOC.MANUAL_DATE,
                                                             DOC.PLAN_TEXT["spring2027"]["date"]) < K.AS_OF, "")
    check("DATES the standard's revision precedes the counts it schedules",
          DOC.STANDARD_DATE < min(min(v) for v in __import__("records").COUNT_PLAN.values()), "")

    n_fail = sum(1 for _l, ok, _d in RESULTS if not ok)
    print("checks: %d run, %d failed" % (len(RESULTS), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
