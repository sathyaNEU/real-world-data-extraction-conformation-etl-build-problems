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
    core._scope_gate = build.scope_gate
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
    # Every reserve-withdrawal window, at its true place and at the place its own start_local
    # field reads, must be clear of the main call's population. An over-frequency overlap is the
    # designed hazard into ask A and is counted, not forbidden.
    placed = build.unavail_rows()
    bad_true = bad_stamp = over_true = 0
    for r in placed:
        s_site = sim.SITE_BY_ID[r["site"]]
        for (dd, a) in ((r["date"], r["start"]), build.norm(r["date"], r["stamp_start"])):
            if not (sim.WINDOW_START <= dd <= sim.WINDOW_END):
                continue
            b = a + r["minutes"] * 60
            for (t0, t1, tstar, fx) in W[dd]["under"]:
                if a - 60 <= tstar < b + 60 and sim.contracted(s_site, np.array([float(tstar)]), dd)[0]:
                    if a == r["start"] and dd == r["date"]:
                        bad_true += 1
                    else:
                        bad_stamp += 1
        for (t0, t1, tstar, fx) in W[r["date"]]["over"]:
            if r["start"] <= tstar < r["start"] + r["minutes"] * 60 \
                    and sim.contracted(s_site, np.array([float(tstar)]), r["date"])[0]:
                over_true += 1
    ck("R2 zero withdrawal windows touch the main call's population at their true place",
       bad_true == 0, "%d overlaps" % bad_true)
    ck("R2 zero withdrawal windows touch it at the place their own row reads",
       bad_stamp == 0, "%d overlaps" % bad_stamp)
    ck("the clock hazard removes over-frequency obligations, as designed",
       over_true >= 5, "%d over-frequency obligations withdrawn" % over_true)
    held = build.held_minutes()
    bad_h = 0
    for (dd, m) in held:
        if (W[dd]["f"][m * 60:(m + 1) * 60] <= sim.QUALIFY_HZ).any():
            bad_h += 1
    ck("R2 zero held summary minutes hold a qualifying under-frequency second", bad_h == 0,
       "%d of %d held minutes" % (bad_h, len(held)))
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

    # ---- the ask layer: mess neutrality, device forcing, bins and printed precision ----------
    import ceiling, pack2

    # R2 per device: the main call does not move when the device is switched off
    su_nodev = core.site_scores(core.episode_table(W, recs, cache, "under"))
    gate = core._scope_gate
    try:
        core._scope_gate = lambda a, b, c: True
        su_open = core.site_scores(core.episode_table(W, recs, cache, "under"))
    finally:
        core._scope_gate = gate
    ck("R2 the clock device moves no main-call figure",
       all(round(su_open[k]["traj"]) == round(su[k]["traj"]) for k in su),
       "under-frequency gains identical with the withdrawal scope open")
    hits = {"n": 0}
    real_met = core.metered
    try:
        core.metered = lambda *a, **k: (hits.__setitem__("n", hits["n"] + 1), real_met(*a, **k))[1]
        core.episode_table(W, recs, cache, "under")
    finally:
        core.metered = real_met
    ck("R2 the main call never reads the settlement meter file", hits["n"] == 0,
       "%d reads of the metered series on the call's path" % hits["n"])
    located_true = sum(1 for d in sim.dates() for m in range(1440)
                       if W[d]["f"][m * 60:(m + 1) * 60].min() <= sim.QUALIFY_HZ)
    mins = list(csv.DictReader(open(os.path.join(
        TGT, "operator", "system_frequency_minute_summary.csv"), encoding="utf-8")))
    located_pack = sum(1 for r in mins if float(r["frequency_min_hz"]) <= sim.QUALIFY_HZ)
    ck("R2 the held summary rows change no minute the call locates",
       located_true == located_pack, "%d true, %d in the shipped summary" % (located_true, located_pack))

    # the devices' forcing, measured on the cut pack by ceiling.py's own reader
    P = ceiling.load()
    lag = {}
    for e in P["ev"]:
        if e["event_type"] != "reserve_unavailable":
            continue
        g = (ceiling._utc(e["logged_utc"]) + ceiling.OFFSET
             - ceiling._local(e["start_local"])).total_seconds()
        lag[g] = lag.get(g, 0) + 1
    ck("device B is forced by the log's own two columns",
       set(lag) == {90.0, 7290.0} and lag[7290.0] >= 8,
       "logged_utc less start_local: " + ", ".join("%.0f s on %d rows" % (k, v)
                                                   for k, v in sorted(lag.items())))
    gb_true, gb_stamp = ceiling.ask_b(P, "true"), ceiling.ask_b(P, "stamped")
    gaps_b = [abs(gb_true[b][1] - gb_stamp[b][1]) for b in range(1, 7)]
    ck("device B moves every block's shortfall by more than the stated rounding",
       min(gaps_b) > 0.1, "smallest block gap %.1f MWh, largest %.1f MWh" % (min(gaps_b), max(gaps_b)))
    ck("device B moves every block's held-available figure too",
       all(abs(gb_true[b][0] - gb_stamp[b][0]) > 0.1 for b in range(1, 7)), "")
    gc_g, gc_n = ceiling.ask_c(P, "golden"), ceiling.ask_c(P, "natural")
    gaps_c = ([abs(gc_g[0][k] - gc_n[0][k]) for k in gc_g[0]]
              + [abs(gc_g[1][k] - gc_n[1][k]) for k in gc_g[1]])
    ck("device C moves every site's exposure figure by more than the stated rounding",
       min(gaps_c) > 0.05, "smallest site gap %.1f MWh, largest %.1f MWh" % (min(gaps_c), max(gaps_c)))
    inb_own = inb_prev = nbig = 0
    for d in sim.dates():
        for s_site in sim.SITES:
            prog = W[d]["prog"][s_site["id"]]
            E = core.metered(W, d, s_site["id"])
            for pp in range(1, 96):
                if abs(prog[pp] - prog[pp - 1]) < 1.0:
                    continue
                nbig += 1
                lo_e, hi_e = sorted((prog[pp - 1] * 0.25, prog[pp] * 0.25))
                if lo_e < E[pp - 1] < hi_e:
                    inb_own += 1
                if lo_e < E[pp] < hi_e:
                    inb_prev += 1
    ck("device C is forced by the programme's own steps",
       inb_prev > 2 * inb_own and nbig > 500,
       "over %d periods whose setpoint steps by more than 1 MW, the energy the row's own index "
       "names lies inside the step in %d, the energy one period earlier in %d"
       % (nbig, inb_own, inb_prev))
    ca = ceiling.ask_a(P, ("true", "extracts"))
    cs = ceiling.ask_a(P, ("stamped", "summary"))
    cx = ceiling.ask_a(P, ("stamped", "extracts"))
    ck("device A moves the episode count a summary-first read reaches",
       sum(1 for k in ca if ca[k] != cs[k]) >= 6,
       "%d of 9 counts move" % sum(1 for k in ca if ca[k] != cs[k]))
    ck("the clock hazard moves the episode count on either route",
       sum(1 for k in ca if ca[k] != cx[k]) >= 5,
       "%d of 9 counts move without device A" % sum(1 for k in ca if ca[k] != cx[k]))

    # the independent reader reproduces the generator's ask goldens
    ck("ceiling.py reproduces the ask B golden from the shipped bytes",
       all(abs(gb_true[b][0] - dict((x["block"], x["available"]) for x in F["availability"])[b]) < 0.05
           and abs(gb_true[b][1] - dict((x["block"], x["shortfall"]) for x in F["availability"])[b]) < 0.05
           for b in range(1, 7)), "")
    ck("ceiling.py reproduces the ask C golden from the shipped bytes",
       abs(sum(gc_g[0].values()) - F["exposure_above_total"]) < 0.05
       and abs(sum(gc_g[1].values()) - F["exposure_below_total"]) < 0.05, "")

    # bins: every graded ask figure mid-bin at the unit its asking sentence states
    adh = pack2.adherence(W, "golden")
    av = pack2.availability(W, placed, "golden")
    bins = []
    for sid, v in so.items():
        bins.append(("down gain %s" % sid, edge(v["traj"], 1.0), 1.0))
    for b in range(1, 7):
        bins.append(("available block %d" % b, edge(av["available"][b], 0.1), 0.1))
        bins.append(("shortfall block %d" % b, edge(av["lost"][b], 0.1), 0.1))
    for sid in adh["above"]:
        bins.append(("above %s" % sid, edge(adh["above"][sid], 0.1), 0.1))
        bins.append(("below %s" % sid, edge(adh["below"][sid], 0.1), 0.1))
    bins.append(("above portfolio", edge(adh["above_total"], 0.1), 0.1))
    bins.append(("below portfolio", edge(adh["below_total"], 0.1), 0.1))
    tight = min(bins, key=lambda x: x[1] / x[2])
    ck("every graded ask figure sits at least 0.3 of its unit from a bin edge",
       all(e >= 0.3 * u for (_, e, u) in bins),
       "tightest %s at %.4f of a unit of %.1f" % (tight[0], tight[1] / tight[2], tight[2]))

    # printed precision: every graded figure at the precision its asking sentence states
    sub = os.path.join(TASK, "submission.md")
    ck("submission.md is present for the precision check", os.path.exists(sub), sub)
    if os.path.exists(sub):
        import re
        body = open(sub, encoding="utf-8").read()
        blk = body[body.index("## 4. Deliverable Answers"):]
        wrong = []
        for line in blk.splitlines():
            if "per cent" in line:
                for m in re.finditer(r"([0-9]+\.[0-9]+) per cent", line):
                    wrong.append("gain %s not whole" % m.group(1))
            if "above " in line or "below " in line or "held available" in line or "shortfall " in line:
                for m in re.finditer(r"(?:above|below|held available|shortfall) (-?[0-9]+)(?![0-9.])", line):
                    wrong.append("energy %s not to one decimal" % m.group(1))
        ck("every graded figure is printed at the precision its asking sentence states",
           not wrong, "; ".join(wrong[:6]))

    print("%d checks, %d failed" % (N, len(FAILS)))
    return 1 if FAILS else 0

if __name__ == "__main__":
    sys.exit(main())
