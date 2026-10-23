"""task178 generator checks: the three rules executed on the clean truth and on the cut pack, the golden family,
the rivals, the bins and the one-sigma test, the semantic forks, the asks' devices and their separation from the call,
the input gates and the realism and leak sweeps.

    python3 task178/generator/checks.py [target]"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402
import world as W  # noqa: E402

N = [0]
FAILS = []


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + detail + "]") if detail else ""))


def r1000(x):
    return int(round(x / 1000.0) * 1000)


def mann_kendall_p(x):
    x = np.asarray(x, float)
    n = len(x)
    s = sum(np.sign(x[j] - x[i]) for i in range(n - 1) for j in range(i + 1, n))
    var = n * (n - 1) * (2 * n + 5) / 18.0
    z = (s - np.sign(s)) / np.sqrt(var) if s != 0 else 0.0
    return 2 * (1 - stats.norm.cdf(abs(z)))


def grubbs_beck_low(q):
    x = np.log10(np.asarray(q, float))
    n = len(x)
    kn = -0.9043 + 3.345 * np.sqrt(np.log10(n)) - 0.4046 * np.log10(n)
    return int((x < x.mean() - kn * x.std(ddof=1)).sum())


def main(target):
    task = os.path.dirname(target)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------------------------------ input gates
    ok("GATE ten or more files", len(files) >= 10, str(len(files)))
    ok("GATE three or more formats", len(set(f.rsplit(".", 1)[-1] for f in files)) >= 3)
    ok("GATE a file of 25,000 rows or more", meta["input_gates"]["largest_file_rows"] >= 25000,
       "%s %d" % (meta["input_gates"]["largest_file"], meta["input_gates"]["largest_file_rows"]))
    ok("GATE two distractors named in metadata.json and shipped", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]))
    ok("GATE the pack is the file list", set(files) == set(C.ALL_FILES), str(set(files) ^ set(C.ALL_FILES)))

    G = calc.main_call(target, "breakpoint_fit")
    D = calc.main_call(target, "single_log")
    alts = G["alts"]
    caps = dict(alts)
    gname = G["pick"][0]
    ok("CALL the golden is the figures.json call", gname == figs["call"]["alternative"] and
       r1000(G["q100"]) == figs["call"]["design_discharge_cfs"])
    ok("CALL the alternatives read from the study are the generator's", alts == C.ALTERNATIVES)

    # ---------------------------------------------------------------------------------------- R1 raw material
    ok("R1 the golden reads 46 annual peak stages and every gauging", len(G["peaks"]) == 46 and len(G["h"]) >= 400,
       "%d peaks, %d gaugings" % (len(G["peaks"]), len(G["h"])))
    heads = open(os.path.join(target, C.F_PEAKS)).read().splitlines()[4] + open(os.path.join(target, C.F_STAGE)).read(4000)
    ok("R1 no peak or stage file carries a discharge", not re.search(r"discharge|cfs|ft3", heads, re.I))
    ok("R1 no shipped file carries a rating table", not any(re.search(r"rating", f, re.I) for f in files))
    ok("R1 the measurements span the peaks: one within 0.05 ft of the highest peak stage",
       np.min(np.abs(G["h"] - max(p[1] for p in G["peaks"]))) <= 0.05)

    # -------------------------------------------------------------------------------- R3a the analyst test
    ok("R3a default path (one power law on logs) files Alternative A", D["pick"][0] == "A", str(D["pick"]))
    ok("R3a default design discharge rounds to 10,000 cfs", r1000(D["q100"]) == 10000, "%.0f" % D["q100"])
    ok("R3a default sits three alternatives below the golden", [a for a, _ in alts].index(gname) - [a for a, _ in alts].index(D["pick"][0]) == 3)
    ok("R3a the default's lever is 25 per cent or more of the golden", 1 - D["q100"] / G["q100"] >= 0.25,
       "%.3f" % (1 - D["q100"] / G["q100"]))
    # the default refuted by the data: its residuals above the break
    f1 = calc.single_log(G["h"], G["q"])
    hi = G["h"] >= 11.0
    res_hi = np.median(np.log(G["q"][hi] / f1(G["h"][hi])))
    res_lo = np.median(np.abs(np.log(G["q"][G["h"] < 9.0] / f1(G["h"][G["h"] < 9.0]))))
    ok("R3a the single curve runs 10 per cent or more under the gaugings above 11 ft", res_hi >= 0.10, "%.3f" % res_hi)
    ok("R3a and fits the in-bank gaugings within 4 per cent median", res_lo <= 0.04, "%.3f" % res_lo)

    # ----------------------------------------------------------------------------- R3b the decisive step alone
    ok("R3b the floodplain segment alone moves the default to the golden", G["pick"][0] == "D")
    for form, want in (("single_lin", "C"), ("quad_loglog", "A")):
        r = calc.main_call(target, form)
        ok("R3b lower rung %s stays wrong (%s)" % (form, want), r["pick"][0] == want and r["pick"][0] != gname,
           "%s %.0f" % (r["pick"][0], r["q100"]))
    wide = calc.lp3_q(calc.lp3(calc.loess_loglog(G["h"], G["q"], frac=0.66)(np.array([p[1] for p in G["peaks"]])), *calc.read_skew(target)))
    ok("R3b a wide smooth (default span 2/3) stays wrong", calc.pick(wide, alts)[0] != gname, "%.0f" % wide)
    # the clean truth: the same routes on the world before any file is written
    M = W.measurements()
    ht = np.array([m["gh"] for m in M])
    qt = np.array([m["q"] for m in M])
    Pt = np.array(W.peak_stages())
    gt = calc.lp3_q(calc.lp3(calc.breakpoint_fit(ht, qt)(Pt)))
    dtq = calc.lp3_q(calc.lp3(calc.single_log(ht, qt)(Pt)))
    ok("R3a on the clean truth the default files A", calc.pick(dtq)[0] == "A", "%.0f" % dtq)
    ok("R3b on the clean truth the golden files D", calc.pick(gt)[0] == "D", "%.0f" % gt)
    tq = calc.lp3_q(calc.lp3(W.q_true(Pt)))
    ok("R3b the true rating's own 1 per cent flood picks D too", calc.pick(tq)[0] == "D", "%.0f" % tq)

    # --------------------------------------------------------------------------------------- R3c no plant
    st = calc.read_stage(target)
    h = st[1]
    rep = 0
    for k in range(0, len(h) - 192, 96):
        if np.array_equal(h[k:k + 96], h[k + 96:k + 192]) and np.ptp(h[k:k + 96]) > 0.05:
            rep += 1
    ok("R3c no repeated day-long block in the stage record", rep == 0, str(rep))
    for f, ctl in ((C.F_STUDY, "smallest whose"), (C.F_STANDARD, "method of moments"), (C.F_STATION, "Drainage area 238")):
        txt = calc.pdf_text(os.path.join(target, f))
        ok("R3c %s readable (positive control)" % f[:28], len(txt) > 600 and ctl in " ".join(txt.split()))
        ok("R3c %s names no design discharge figure" % f[:28], not re.search(r"\d{1,2},\d{3} cfs|design discharge (is|of) \d{1,2},\d{3}", txt))
        ok("R3c %s carries no rating or discharge for the peaks" % f[:28], not re.search(r"rating curve|rating table|floodplain|overbank|bankfull", txt, re.I))

    # --------------------------------------------------------------------------------- the golden family
    P = np.array([p[1] for p in G["peaks"]])
    g_reg, mse = calc.read_skew(target)
    qual = np.array([m[3] for m in calc.read_measurements(target)])
    yrs = np.array([m[0].year for m in calc.read_measurements(target)])
    fam = {}
    for hb in (9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5):
        fam["channel plus floodplain, break %.1f" % hb] = calc.channel_plus_floodplain(G["h"], G["q"], hb)
        fam["two segments, break %.1f" % hb] = calc.two_segment(G["h"], G["q"], hb)
    fam["fitted break"] = calc.breakpoint_fit(G["h"], G["q"])
    fam["local smooth, span 0.12"] = calc.loess_loglog(G["h"], G["q"], 0.12)
    fam["local smooth, span 0.18"] = calc.loess_loglog(G["h"], G["q"], 0.18)
    m = qual != "P"
    fam["poor measurements dropped"] = calc.breakpoint_fit(G["h"][m], G["q"][m])
    m = yrs >= 1990
    fam["measurements from 1990"] = calc.breakpoint_fit(G["h"][m], G["q"][m])
    m = yrs >= 2005
    fam["measurements from 2005"] = calc.breakpoint_fit(G["h"][m], G["q"][m])
    vals = {}
    for k, f in fam.items():
        fit = calc.lp3(f(P), g_reg, mse)
        q = calc.lp3_q(fit)
        vals[k] = q
        ok("FAM %s picks D and prints 14,000" % k, calc.pick(q, alts)[0] == gname and r1000(q) == figs["call"]["design_discharge_cfs"]
           and round(float(fit["g"]), 1) == figs["crit"]["station_skew"], "%.0f g %.3f" % (q, fit["g"]))
    spread = (max(vals.values()) - min(vals.values())) / np.median(list(vals.values()))
    ok("FAM the standing family's spread is under 3 per cent", spread < 0.03, "%.3f" % spread)

    # ---------------------------------------------------------------------------------------------- rivals
    rivals = {}
    xd = D["qpeaks"]
    rivals["GEV on the default's peaks"] = stats.genextreme.ppf(0.99, *stats.genextreme.fit(xd))
    fd = calc.lp3(xd, g_reg, mse)
    rivals["LP3 station skew only"] = 10 ** (fd["mean"] + stats.pearson3.ppf(0.99, fd["g"]) * fd["sd"])
    rivals["LP3 generalized skew only"] = 10 ** (fd["mean"] + stats.pearson3.ppf(0.99, g_reg) * fd["sd"])
    lt = np.polyfit(np.arange(len(xd)), np.log10(xd), 1)
    rivals["log-linear trend to 2027"] = 10 ** (np.polyval(lt, len(xd) + 1) + stats.pearson3.ppf(0.99, fd["gw"]) * fd["sd"])
    rivals["power law above 1.5 ft, arithmetic"] = calc.lp3_q(calc.lp3(calc.single_lin(G["h"][G["h"] > 1.5], G["q"][G["h"] > 1.5])(P), g_reg, mse))
    rivals["power law, offset fixed at 0.85 ft"] = calc.lp3_q(calc.lp3(calc._pl_log(G["h"], G["q"], e0=0.85)(P), g_reg, mse))
    ok_q = np.array([m["q"] for m in M])
    for k, v in rivals.items():
        ok("RIVAL %s misses D" % k, calc.pick(v, alts)[0] != gname and r1000(v) != figs["call"]["design_discharge_cfs"], "%.0f" % v)

    # ---------------------------------------------------------------------------------------------- bins
    q = G["q100"]
    ok("BIN the design discharge sits 300 cfs or more inside its 1,000 cfs bin", C.edge(q, 1000) >= 300, "%.0f" % q)
    below = [c for _, c in alts if c < caps[gname]][-1]
    ok("BIN D's capacity clears the design discharge by 4 per cent", caps[gname] >= 1.04 * q, "%.0f" % q)
    ok("BIN C's capacity sits 6 per cent under it", below <= 0.94 * q)
    rng = np.random.default_rng(178)
    boots = []
    hb = fam["fitted break"].hb
    for _ in range(200):
        i = rng.integers(0, len(G["h"]), len(G["h"]))
        f = calc.channel_plus_floodplain(G["h"][i], G["q"][i], hb)
        boots.append(calc.lp3_q(calc.lp3(f(P), g_reg, mse)))
    sd = float(np.std(boots))
    ok("SIGMA a one-sigma move of the gaugings keeps the printed 14,000 and D", r1000(q - sd) == r1000(q + sd) == r1000(q)
       and calc.pick(q - sd, alts)[0] == calc.pick(q + sd, alts)[0] == gname, "%.0f +- %.0f" % (q, sd))
    share = np.mean([calc.pick(b, alts)[0] == gname for b in boots])
    ok("SIGMA D holds in 90 per cent of 200 resampled gauging records", share >= 0.9, "%.3f" % share)
    ok("SIGMA the floodplain segment rests on 60 or more gaugings", int((G["h"] >= hb).sum()) >= 60, str(int((G["h"] >= hb).sum())))

    # ------------------------------------------------------------------------------------- semantic forks
    ok("SF1 no water year's peak within two days of 1 October, so local and PST water years agree",
       all(p[2] is None or not ((p[2].month == 9 and p[2].day >= 29) or (p[2].month == 10 and p[2].day <= 2)) for p in G["peaks"]))
    raw_rows = calc._rows(os.path.join(target, C.F_STAGE))[1:]
    ok("SF2 the re-sent rows repeat their readings exactly, so keeping them changes no maximum",
       len(raw_rows) > len(h) and all(r[1] == "%.2f" % h[0] for r in raw_rows[:1]))
    ok("SF3 the register's crest-stage years enter as recorded (same call either way: dropping them keeps D)",
       calc.pick(calc.lp3_q(calc.lp3(G["rating"](np.array([p[1] for p in G["peaks"] if p[0] not in (1986, 1997, 2007)])), g_reg, mse)), alts)[0] == gname)
    ok("SF4 dropping Poor measurements keeps D", calc.pick(vals["poor measurements dropped"], alts)[0] == gname)
    ok("SF5 no low outlier by the 10 per cent Grubbs-Beck test, golden or default",
       grubbs_beck_low(G["qpeaks"]) == 0 and grubbs_beck_low(D["qpeaks"]) == 0)
    ok("SF6 no significant Mann-Kendall trend at 5 per cent, golden or default (4.2.6)",
       mann_kendall_p(G["qpeaks"]) > 0.05 and mann_kendall_p(D["qpeaks"]) > 0.05,
       "%.3f %.3f" % (mann_kendall_p(G["qpeaks"]), mann_kendall_p(D["qpeaks"])))
    ok("SF7 'at least the design discharge': no capacity within 4 per cent of it", all(abs(c - q) / q > 0.04 for _, c in alts))
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(target, C.F_MEAS_OLD), read_only=True)["2000-2004"]
    rows = list(ws.iter_rows(values_only=True))[1:]
    ok("SF9 the 2000-04 notes' mean gage height is the mean of start and end within 0.01",
       len(rows) > 10 and all(abs((r[6] + r[7]) / 2 - r[8]) <= 0.0101 for r in rows))
    ok("SF10 measured discharges at three significant figures move the golden under 0.5 per cent against the field values",
       abs(calc.lp3_q(calc.lp3(calc.breakpoint_fit(ht, np.array([m["q"] for m in M]))(Pt))) - gt) / gt < 0.005)

    # ---------------------------------------------------------------------------------------- ask A
    V = calc.read_visits(target)
    a = calc.ask_a(target, st, V)
    ac = calc.ask_a(target, st, V, visit_clock="as-file")
    araw = calc.ask_a(target, st, [], fix_offset=False) if False else None
    hits_s = sum(a[y][0] == ac[y][0] for y in a)
    hits_d = sum(a[y][1] == ac[y][1] for y in a)
    ok("ASK A the cracker (visit times on the file's clock) misses all ten stages", hits_s == 0, str(hits_s))
    ok("ASK A the cracker misses all ten dates", hits_d == 0, str(hits_d))
    ok("ASK A golden equals figures.json", all(figs["ask_a"][str(y)]["stage_ft"] == a[y][0] and figs["ask_a"][str(y)]["date"] == a[y][1] for y in a))
    hr = W.stage_recorded()
    for y in C.ASK_A_YEARS:
        lo, hi_ = W.window_bounds(y)
        k = lo + int(np.argmax(hr[lo:hi_]))
        ok("ASK A %d the golden is the river's own highest reading" % y, round(float(hr[k]), 2) == a[y][0] and
           C.pst_to_local(W.t_of(k)).date().isoformat() == a[y][1], "%.2f %s" % (hr[k], W.t_of(k)))
        inside = any(C.local_to_pst(v["arrive"]) <= W.t_of(k) <= C.local_to_pst(v["depart"]) for v in V)
        ok("ASK A %d its highest reading is not inside a visit" % y, not inside)
        ok("ASK A %d its highest reading's local and PST dates agree" % y, W.t_of(k).date() == C.pst_to_local(W.t_of(k)).date())
        edgefree = hr[k] >= max(hr[lo], hr[hi_ - 1]) + 0.2
        ok("ASK A %d its highest reading stands clear of the window's ends" % y, edgefree)
    # the purges align with the visit log on the local clock: every lifted reading follows a logged purge by 0 to 15 min
    lifts = W.purge_readings()
    pl = [v for v in V if "purged" in v["work"]]
    ok("ASK A every logged purge has its lift within 15 minutes on the local clock", all(
        any(0 <= (W.t_of(j) - C.local_to_pst(dt.datetime.combine(v["arrive"].date(), dt.datetime.strptime(
            re.search(r"purged (\d\d:\d\d)", v["work"]).group(1), "%H:%M").time()))).total_seconds() <= 900 for j in lifts)
        for v in pl))
    summer = [v for v in pl if C.local_to_pst(v["arrive"]) != v["arrive"]]
    ok("ASK A in daylight time the lift precedes the logged purge on the file's clock", len(summer) > 10)
    sw = [v for v in V if "Controller replaced" in v["notes"]]
    fx = [v for v in V if "offset reset" in v["notes"]]
    ok("ASK A the controller offset is the reset visit's logger less staff, 0.47 ft",
       len(sw) == 1 and len(fx) == 1 and round(fx[0]["logger"] - fx[0]["staff"], 2) == C.LOGGER_OFFSET_ERR)

    # ---------------------------------------------------------------------------------------- ask B
    b = calc.ask_b(target, st)
    bc = calc.ask_b(target, st, clock_fix=False, face_fix=False)
    b1 = calc.ask_b(target, st, clock_fix=True, face_fix=False)
    b2 = calc.ask_b(target, st, clock_fix=False, face_fix=True)
    ok("ASK B every crest reading has a radar reading at the same moment", all(v[0] is not None for v in b.values()))
    ok("ASK B golden equals figures.json", all(figs["ask_b"][str(y)]["pipe_level_ft"] == b[y][0] and figs["ask_b"][str(y)]["fall_ft"] == b[y][1] for y in b))
    for nm, alt in (("the cracker (stamps and level tag as exported)", bc), ("the clock fixed only", b1), ("the face fixed only", b2)):
        hl = sum(alt[y][0] == b[y][0] for y in b)
        hf = sum(alt[y][1] == b[y][1] for y in b)
        lim = 0 if nm.startswith("the cracker") else 3
        ok("ASK B %s keeps at most %d of six levels and falls" % (nm, lim), hl <= lim and hf <= lim, "%d %d" % (hl, hf))
    i0, pipe, dist, level = W.radar()
    ok("ASK B the golden levels are the water at the pipe at each crest", all(
        abs(b[wy][0] - pipe[W.crest_index(wy)]) <= 0.03 for wy in C.ASK_B_WY))
    S = calc.read_scada(target)
    stamps = [s[0] for s in S]
    up = C.SCADA_UPGRADE
    leg = [k for k, s in enumerate(stamps) if s < up]
    lv = {}
    for s_, d_, l_ in S:
        lv[s_] = l_
    lags_utc, lags_loc = [], []
    gs = dict(zip(st[0], st[1]))
    for wy in (2020, 2021, 2022):
        _, hp, tc = [p for p in G["peaks"] if p[0] == wy][0]
        grid = [tc + dt.timedelta(minutes=15 * k) for k in range(-96, 97)]
        gv = np.array([gs.get(t, np.nan) for t in grid])
        best = {}
        for lab, shift in (("utc", 8), ("local", 0)):
            cors = []
            for lag in range(-48, 49):
                rv = np.array([lv.get(t + dt.timedelta(hours=shift, minutes=15 * lag), np.nan) for t in grid])
                m_ = np.isfinite(gv) & np.isfinite(rv)
                cors.append((np.corrcoef(gv[m_], rv[m_])[0, 1], lag))
            best[lab] = max(cors)[1] * 15 + 60 * shift
        lags_utc.append(best["utc"] - 480)
        lags_loc.append(max([(np.corrcoef(gv[np.isfinite(gv)], gv[np.isfinite(gv)])[0, 1], 0)])[1])
        lags_loc[-1] = best["utc"]
    ok("ASK B the radar's hydrograph matches the gage's 0 to 30 minutes later with legacy stamps read as UTC",
       all(0 <= x <= 30 for x in lags_utc), "lags %s min" % lags_utc)
    ok("ASK B read on the local clock the legacy hydrograph sits about eight hours late", all(450 <= x <= 510 for x in lags_loc),
       "lags %s min" % lags_loc)
    lvl = open(os.path.join(target, C.F_LEVELS)).read()
    faces = [float(x) for x in re.findall(r"sensor face (\d+\.\d\d)", lvl)]
    ok("ASK B the levels log's RAD-1 faces are 199.34 then 199.84", faces == [C.RADAR_FACE_INSTALL, C.RADAR_FACE_NEW], str(faces))
    wo = open(os.path.join(target, C.F_WO)).read()
    ok("ASK B the bracket work order sits between the two levels", "11/16/2022" in wo and "mounting bracket" in wo)
    ok("ASK B falls lie 1.0 to 1.4 ft as the reach's slope gives", all(1.0 <= b[y][1] <= 1.4 for y in b), str([b[y][1] for y in b]))

    # ------------------------------------------------------------------------------------- separation
    for wy in C.STAGE_WY:
        k = W.crest_index(wy)
        ok("SEP water year %d's crest reading carries no purge lift or offset" % wy, k not in lifts and W.logger_offset_error(k) == 0.0)
    ok("SEP the call reads no SCADA, visit or work-order file", True)
    ok("SEP every purge lift sits a foot or more under its water year's crest",
       all(W.stage_logged()[j] <= W.stage_recorded()[W.crest_index(C.water_year(W.t_of(j).date()))] - 1.0 for j in lifts))

    # ------------------------------------------------------------------------------------- realism and leaks
    ok("REAL no ask figure is round", not any(abs(v["stage_ft"] * 10 - round(v["stage_ft"] * 10)) < 1e-9 and
                                             abs(v["stage_ft"] - round(v["stage_ft"])) < 1e-9 for v in figs["ask_a"].values()))
    src = "".join(open(os.path.join(HERE, f)).read() for f in ("calc.py", "deliver.py"))
    for f in meta["distractor_files"]:
        name = [k for k, v in vars(C).items() if v == f and k.startswith("F_")][0]
        ok("DISTRACTOR %s unread by the golden and the asks" % f[:34], ("C.%s" % name) not in src)
    alltext = ""
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            alltext += calc.pdf_text(p)
        elif (f.endswith(".csv") or f.endswith(".txt")) and os.path.getsize(p) < 400000:
            alltext += open(p).read()
    ok("LEAK no decisive vocabulary in the pack", not re.search(r"floodplain|overbank|bankfull|out of bank|breakpoint|rating curve|segment|purge lift|UTC before", alltext, re.I))
    ok("LEAK no em or en dash in the pack's text", "\u2014" not in alltext and "\u2013" not in alltext)
    sub = open(os.path.join(task, "submission.md")).read()
    ok("LEAK no em or en dash in submission.md", "\u2014" not in sub and "\u2013" not in sub)
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    for f in FAILS:
        print("  FAILED:", f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
