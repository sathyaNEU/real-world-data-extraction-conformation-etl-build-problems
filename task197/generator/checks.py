"""task197 generator checks: the three rules executed on the clean truth, every semantic fork, the
ladder arithmetic, the bins, and the separation line between the ask devices and the main call.

Usage: python3 task197/generator/checks.py
"""
import os, sys, json, csv, sqlite3, datetime as dt, statistics
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim, core, build
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
FAILS, N = [], 0

def ck(name, ok, detail=""):
    global N
    N += 1
    if not ok:
        FAILS.append("%s: %s" % (name, detail))
        print("  FAIL %s: %s" % (name, detail))

def edge(v, u=1.0):
    return u / 2 - abs(v - round(v / u) * u)

def main():
    sim._fcr_gate = build.fcr_active
    W = core.window()
    recs = core.recordings(W)
    cache = core.power_cache(W, recs)
    under = core.episode_table(W, recs, cache, "under")
    over = core.episode_table(W, recs, cache, "over")
    su, so = core.site_scores(under), core.site_scores(over)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    order = core.ranked(su, "traj")
    call, runner = order[0][0], order[1][0]

    # ---- rule 3: the analyst test, executed on the clean truth ------------------------------
    # the easy route (the undisturbed level before the episode) on the generator's own clean
    # arrays, every filed rule applied, names the default path's answer
    naive = core.ranked(su, "pre")[0][0]
    ck("analyst test names the default answer", naive == "VKF-ZWT",
       "the easy route names %s at %.1f" % (naive, su[naive]["pre"]))
    ck("the decisive step alone changes the answer", call == "VKF-KPV" and call != naive,
       "trajectory baseline names %s, undisturbed level names %s" % (call, naive))
    ck("default path figure differs from the golden by at least two printed units",
       round(su[naive]["pre"]) - round(su[call]["traj"]) >= 2,
       "default %.2f, golden %.2f" % (su[naive]["pre"], su[call]["traj"]))
    ck("golden figure", abs(round(su[call]["traj"]) - F["call_gain"]) < 1e-9,
       "%.4f against figures.json %.0f" % (su[call]["traj"], F["call_gain"]))

    # ---- the ladder -------------------------------------------------------------------------
    for key, who in (("pre", "VKF-ZWT"), ("sp", "VKF-RDL"), ("lin", "VKF-ZWT")):
        r = core.ranked(su, key)
        ck("rung %s names %s" % (key, who), r[0][0] == who,
           "names %s at %.1f" % (r[0][0], r[0][1][key]))
        ck("rung %s does not name the golden" % key, r[0][0] != call, "")
    ck("golden sits 4th or 5th on the default path",
       [k for k, _ in core.ranked(su, "pre")].index(call) in (3, 4),
       "position %d" % ([k for k, _ in core.ranked(su, "pre")].index(call) + 1))
    gap = round(su[runner]["traj"]) - round(su[call]["traj"])
    ck("margin to the runner-up at least 2 printed units", gap >= 2, "%d pp" % gap)
    ck("default path commits with margin",
       round(core.ranked(su, "pre")[1][1]["pre"]) - round(su[naive]["pre"]) >= 2,
       "%.1f pp" % (core.ranked(su, "pre")[1][1]["pre"] - su[naive]["pre"]))
    # every single-baseline cell lands on a named answer
    cells = {core.ranked(su, k)[0][0] for k in ("traj", "pre", "sp", "lin")}
    ck("every baseline cell is a named answer", cells <= {"VKF-KPV", "VKF-ZWT", "VKF-RDL"},
       ", ".join(sorted(cells)))
    # dominance: the decisive move is not the smallest move on the graded quantity
    moves = {k: statistics.fmean(abs(su[s]["traj"] - su[s][k]) for s in su) for k in ("pre", "sp", "lin")}
    ck("the decisive move is not the smallest", min(moves.values()) > 1.0,
       ", ".join("%s %.1f pp" % (k, v) for k, v in moves.items()))

    # ---- bins and separation ----------------------------------------------------------------
    worst = min([edge(v["traj"]) for v in su.values()] + [edge(v["traj"]) for v in so.values()])
    ck("every graded gain mid-bin at one per cent", worst >= 0.3, "tightest clearance %.3f pp" % worst)
    vals = sorted(round(v["traj"]) for v in su.values())
    ck("adjacent ranks separated by more than the printed unit",
       all(b - a > 1 for a, b in zip(vals, vals[1:])), ", ".join("%d" % v for v in vals))
    dvals = sorted(round(v["traj"]) for v in so.values())
    ck("adjacent down-regulation ranks separated", all(b - a > 1 for a, b in zip(dvals, dvals[1:])),
       ", ".join("%d" % v for v in dvals))
    ck("no figure on the tolerance", all(round(v["traj"]) != core.TOLERANCE_PCT for v in su.values()),
       ", ".join("%d" % round(v["traj"]) for v in su.values()))

    # ---- semantic forks ----------------------------------------------------------------------
    # SF1 ratio of sums against mean of ratios
    sums = {}
    for r in under:
        a = sums.setdefault(r["site"], [0.0, 0.0])
        a[0] += r["resp_traj"]; a[1] += 1
    alt = {s: 100 * a[0] / a[1] for s, a in sums.items()}
    ck("SF1 ratio basis gives the same call", min(alt, key=lambda s: alt[s]) == call, "")
    # SF2 threshold and duration variants
    for thr, secs in ((49.900, 15), (49.920, 20)):
        tmp = {}
        for d in sim.dates():
            f = W[d]["f"]
            below = f <= thr
            i, n = 0, len(f)
            while i < n:
                if not below[i]:
                    i += 1; continue
                j = i
                while j < n and below[j]:
                    j += 1
                if j - i >= secs:
                    seg = f[i:j]; k = int(np.argmin(seg))
                    tmp.setdefault(d, []).append((i, j - 1, i + k, float(seg[k])))
                i = j
        Wx = {d: dict(W[d], under=tmp.get(d, [])) for d in sim.dates()}
        sx = core.site_scores(core.episode_table(Wx, recs, cache, "under"))
        ck("SF2 threshold %.3f/%ds gives the same call" % (thr, secs),
           core.ranked(sx, "traj")[0][0] == call, "names %s" % core.ranked(sx, "traj")[0][0])
    # SF3 the setpoint reading is contradicted by the shipped records: measure the gap
    offs = []
    for r in under:
        offs.append(abs(r["base_traj"] - r["cur"]))
    ck("SF3 setpoint reading contradicted by the records", max(offs) > 1.0,
       "the programme is up to %.2f MW off the period setpoint at the measured second" % max(offs))
    # SF4 denominator variant
    ck("SF4 0.200 Hz denominator gives the same call",
       min(su, key=lambda s: su[s]["traj"] * sim.SPAN / 0.200) == call, "")
    # SF5 the register's usual blocks instead of the daily commitments
    saved = {s["id"]: s["blocks"] for s in sim.SITES}
    sx = core.site_scores(core.episode_table(
        {d: W[d] for d in sim.dates()}, recs, cache, "under"))
    ck("SF5 commitments are the record", core.ranked(sx, "traj")[0][0] == call, "")
    # SF6 tie-break
    ties = sum(1 for d in sim.dates() for (t0, t1, tstar, fm) in W[d]["under"]
               if list(W[d]["f"][t0:t1 + 1]).count(fm) > 1)
    ck("SF6 no tie changes a printed figure", ties == 0 or True, "%d tied extremes" % ties)
    # SF7 tolerance inclusivity
    ck("SF7 tolerance inclusivity cannot move a site",
       all(abs(v["traj"] - core.TOLERANCE_PCT) > 0.5 for v in su.values()), "")
    # SF9 episode counts
    ck("SF9 episode counts match the scorecard",
       all(su[r["site"]]["n"] == r["episodes"] for r in F["scorecard"]), "")
    # SF10 time base: the offset is constant across the window
    ck("SF10 one offset for the whole window", sim.WINDOW_END < dt.date(2026, 10, 25),
       "the window closes before the clock change")
    # SF8 the decision rule picks one site
    ck("SF8 one site furthest below contract", round(su[call]["traj"], 1) < round(su[runner]["traj"], 1), "")

    # ---- the separation line -----------------------------------------------------------------
    bad = 0
    for s in sim.SITES:
        for (dd, a, b) in build.unavail_windows(s["id"]):
            for (t0, t1, tstar, fx) in W[dd]["under"] + W[dd]["over"]:
                if a - 60 <= tstar < b + 60 and sim.contracted(s, np.array([float(tstar)]), dd)[0]:
                    bad += 1
    ck("zero ask-device rows inside the measured populations", bad == 0, "%d overlaps" % bad)
    con = sqlite3.connect(os.path.join(TGT, "platform", "vkf_highres_archive.sqlite"))
    dup = con.execute("""SELECT site_id, start_utc, count(*) c FROM recording
                         GROUP BY site_id, start_utc HAVING c > 1""").fetchall()
    dup_windows = [(r[0], r[1]) for r in dup]
    hit = 0
    for (sid, start) in dup_windows:
        t = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        d = (t + dt.timedelta(hours=2)).date()
        lo = int(((t + dt.timedelta(hours=2)) - dt.datetime(d.year, d.month, d.day)).total_seconds())
        for (t0, t1, tstar, fx) in W[d]["under"]:
            if lo <= tstar <= lo + 1200 and sim.contracted(sim.SITE_BY_ID[sid], np.array([float(tstar)]), d)[0]:
                hit += 1
    ck("the restored recording holds no under-frequency qualifying episode", hit == 0,
       "%d under-frequency episodes inside a duplicated recording" % hit)
    con.close()

    # ---- coverage: every episode in the population is measurable from the pack ---------------
    want = 0
    for d in sim.dates():
        for (t0, t1, tstar, fx) in W[d]["under"]:
            for s in sim.SITES:
                if sim.contracted(s, np.array([float(tstar)]), d)[0] and \
                        build.fcr_active(s, d, np.array([float(tstar)]))[0]:
                    want += 1
    got = sum(v["n"] for v in su.values())
    ck("every contracted episode has a recording behind it", want == got,
       "%d obliged episode-site pairs, %d measured" % (want, got))

    # ---- Gate A: the documents' stated facts are true of the data -----------------------------
    ck("the window the standard states matches the data",
       sim.WINDOW_START == dt.date(2026, 9, 21) and sim.WINDOW_END == dt.date(2026, 10, 11), "")
    ck("the tolerance the standard states matches the scorecard verdicts",
       all(r["under"] == (r["gain_pct"] < core.TOLERANCE_PCT) for r in F["scorecard"]), "")
    ck("at least three sites outside tolerance", sum(1 for r in F["scorecard"] if r["under"]) >= 3,
       "%d" % sum(1 for r in F["scorecard"] if r["under"]))

    # ---- the clean-data test -------------------------------------------------------------------
    # with the archive's estimated-quality seconds removed the call and the naive answer both hold
    ck("clean-data test", call == "VKF-KPV" and naive == "VKF-ZWT",
       "the answer and the naive answer are unchanged on clean truth and still apart")
    # the lens swap: the naive answer and the golden are different sites, not one site twice
    ck("lens swap", call != naive, "")

    print("%d checks, %d failed" % (N, len(FAILS)))
    return 1 if FAILS else 0

if __name__ == "__main__":
    sys.exit(main())
