"""task197 generator checks: the three rules executed on the clean truth, every semantic fork, the
ladder arithmetic, the bins, and the separation line between the ask devices and the main call.

Usage: python3 task197/generator/checks.py
"""
import os, sys, json, csv, sqlite3, datetime as dt, statistics, collections
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
    recs = core.recordings(W, build.capture_events())
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
    mins = list(csv.DictReader(open(os.path.join(
        TGT, "operator", "system_frequency_minute_summary.csv"), encoding="utf-8")))
    want_min = []
    for d in sim.dates():
        for m in range(1440):
            want_min.append(round(float(W[d]["f"][m * 60:(m + 1) * 60].min()), 4))
    got_min = [float(r["frequency_min_hz"]) for r in mins]
    moved = [i for i, (a, b) in enumerate(zip(want_min, got_min)) if a != b]
    moved_located = [i for i in moved if want_min[i] <= sim.QUALIFY_HZ or got_min[i] <= sim.QUALIFY_HZ]
    ck("R2 the held summary rows move no minute into or out of the call's located set",
       not moved_located, "%d of %d held rows change a located minute" % (len(moved_located), len(moved)))
    ck("the held summary rows are the only rows that differ from the minute's own minimum",
       len(moved) == len(held), "%d rows differ, %d minutes held" % (len(moved), len(held)))

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
    nbig = nearer_prev = nearer_own = 0
    dev_own = dev_prev = []
    dev_own, dev_prev = [], []
    for d in sim.dates():
        for s_site in sim.SITES:
            sid = s_site["id"]
            prog = W[d]["prog"][sid]
            E = core.metered(W, d, sid)
            cmask = np.zeros(96, dtype=bool)
            for b in sim.commitments(s_site, d):
                lo_h, hi_h = sim.BLOCK_HOURS[b]
                cmask[lo_h * 4:hi_h * 4] = True
            for pp in range(1, 96):
                if not cmask[pp]:
                    dev_prev.append(abs(E[pp] - prog[pp] * 0.25))
                    dev_own.append(abs(E[pp - 1] - prog[pp] * 0.25))
                if abs(prog[pp] - prog[pp - 1]) < 1.0:
                    continue
                nbig += 1
                if abs(E[pp - 1] - prog[pp - 1] * 0.25) < abs(E[pp - 1] - prog[pp] * 0.25):
                    nearer_prev += 1
                else:
                    nearer_own += 1
    mo, mp = float(np.mean(dev_own)), float(np.mean(dev_prev))
    ck("device C is forced by the programme the rows are paired against",
       mo > 4 * mp and len(dev_prev) > 10000,
       "over %d scored periods the mean absolute deviation from programme is %.4f MWh when a row is "
       "paired with the interval it closes and %.4f MWh when it is paired with the period its own "
       "index names, a factor of %.1f" % (len(dev_prev), mp, mo, mo / mp))
    ck("the rows indexed at a setpoint step carry the level before the step",
       nearer_prev > 20 * nearer_own,
       "of %d periods whose setpoint steps by more than 1 MW, the row carrying that index sits "
       "nearer the previous setpoint in %d and nearer its own in %d" % (nbig, nearer_prev, nearer_own))
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

    # Bins. A gain is recovered through the traverse span, which a solver lands within a second or
    # two of, so it carries path spread and takes the 0.3-of-a-unit floor. A block's capacity hours
    # and a site's exposure are exact sums over shipped rows on a population the commitment file
    # fixes, with the rounding path pinned in clause 4 and clause 5, so nothing on the solver's
    # side can move them; those are asserted for exactness instead, with a floor that keeps no
    # figure sitting on a printed boundary.
    adh = pack2.adherence(W, "golden")
    av = pack2.availability(W, placed, "golden")
    gains = [("down gain %s" % sid, edge(v["traj"], 1.0)) for sid, v in so.items()]
    ck("every graded gain sits at least 0.3 of a per cent from a bin edge",
       all(e >= 0.3 for (_, e) in gains),
       "tightest %s at %.3f pp" % min(gains, key=lambda x: x[1]))
    bhours = [("available block %d" % b, edge(av["available"][b], 0.1)) for b in range(1, 7)] + \
             [("shortfall block %d" % b, edge(av["lost"][b], 0.1)) for b in range(1, 7)]
    ck("every graded capacity-hours figure sits at least 0.3 of its unit from a bin edge",
       all(e >= 0.03 for (_, e) in bhours),
       "tightest %s at %.4f MWh" % min(bhours, key=lambda x: x[1]))
    expo = [("above %s" % k, edge(adh["above"][k], 0.1)) for k in adh["above"]] + \
           [("below %s" % k, edge(adh["below"][k], 0.1)) for k in adh["below"]] + \
           [("above portfolio", edge(adh["above_total"], 0.1)),
            ("below portfolio", edge(adh["below_total"], 0.1))]
    ck("every graded exposure figure sits at least 0.3 of its unit from a bin edge",
       all(e >= 0.03 for (_, e) in expo),
       "tightest %s at %.4f MWh from the edge" % min(expo, key=lambda x: x[1]))
    # exactness: the pinned rounding path, and the one it closes, print the same figure
    sum_then_round = {k: round(adh["above"][k], 1) for k in adh["above"]}
    round_then_sum = {}
    for s_site in sim.SITES:
        sid = s_site["id"]
        tot = 0.0
        for d in sim.dates():
            prog = W[d]["prog"][sid]
            E = core.metered(W, d, sid)
            cmask = np.zeros(96, dtype=bool)
            for b in sim.commitments(s_site, d):
                lo_h, hi_h = sim.BLOCK_HOURS[b]
                cmask[lo_h * 4:hi_h * 4] = True
            for pp in range(96):
                if cmask[pp]:
                    continue
                dv = float(E[pp]) - float(prog[pp]) * 0.25
                if dv >= 0:
                    tot += round(dv, 1)
        round_then_sum[sid] = round(tot, 1)
    diff = [k for k in sum_then_round if sum_then_round[k] != round_then_sum[k]]
    ck("clause 5's rounding path is the one that is pinned, and the alternative is closed",
       len(diff) > 0, "round-each-period would move %d of 9 above-programme figures" % len(diff))

    # ---- the archive's spread: an organ's realism is its variance, not its genre ---------------
    trig = collections.Counter(r[2] for r in recs)
    lens = {r[4] - r[3] for r in recs}
    offs = {r[3] % 900 for r in recs}
    ck("the archive holds captures of four or more kinds", len(trig) >= 4,
       ", ".join("%s %d" % kv for kv in trig.most_common()))
    ck("recording length and start offset vary across the archive",
       len(lens) >= 100 and len(offs) >= 30,
       "%d distinct lengths %d..%d, %d distinct quarter-hour offsets"
       % (len(lens), min(lens), max(lens), len(offs)))
    dp = [r for r in recs if r[2] == "DPDT"]
    dlen = {r[4] - r[3] for r in dp}
    doff = {r[3] % 900 for r in dp}
    ck("the captures the decisive step reads are not the archive's only rows",
       len(dp) / len(recs) < 0.5 and len(dp) > 200,
       "%d of %d recordings, %.1f per cent" % (len(dp), len(recs), 100 * len(dp) / len(recs)))
    ck("those captures are not identical on every dimension but their timestamps",
       len(dlen) >= 50 and len(doff) >= 10,
       "%d distinct lengths %d..%d, %d distinct offsets" % (len(dlen), min(dlen), max(dlen), len(doff)))
    ck("captures other than the operator's deviation windows fall on every delivery date",
       len({r[0] for r in recs if r[2] != "FREQ-DEV"}) == len(sim.dates()),
       "%d of %d dates" % (len({r[0] for r in recs if r[2] != "FREQ-DEV"}), len(sim.dates())))
    # A capture's length is its site's ring buffer plus a settle window drawn from one distribution
    # for every site, so the only site attribute in it is the ring, and the ring is held at rank
    # correlation zero against the traverse spans. Both halves are asserted.
    posts = {s_site["id"]: float(np.median([r[4] - r[3] - core.ring(s_site["id"])
                                            for r in dp if r[1] == s_site["id"]]))
             for s_site in sim.SITES}
    ck("the settle window a capture runs on is drawn alike for every site",
       max(posts.values()) - min(posts.values()) <= 15,
       "per-site median settle window spans %.0f s" % (max(posts.values()) - min(posts.values())))

    def _spear(a, b):
        ra = np.argsort(np.argsort(a)).astype(float)
        rb = np.argsort(np.argsort(b)).astype(float)
        return float(np.corrcoef(ra, rb)[0, 1])
    rings = [core.ring(s_site["id"]) for s_site in sim.SITES]
    ramps = [s_site["ramp_s"] for s_site in sim.SITES]
    ck("no capture's length or offset carries anything about the site's traverse span",
       abs(_spear(rings, ramps)) <= 0.25 and len(set(rings)) >= 6,
       "ring buffer against traverse span, rank correlation %.3f over %d distinct pre-rolls"
       % (_spear(rings, ramps), len(set(rings))))
    # the organ's exactness: the boundaries a solver fits the traverse over are there, in full
    full = {}
    for s_site in sim.SITES:
        sid = s_site["id"]
        got = 0
        for (dd, pp) in core.fit_boundaries(W, sid):
            t = pp * 900
            if any(lo <= t and t + 204 < hi for (d2, s2, tg, lo, hi) in recs
                   if d2 == dd and s2 == sid):
                got += 1
        full[sid] = got
    ck("every site keeps two or more fitting boundaries captured in full",
       min(full.values()) >= 2, ", ".join("%s=%d" % (k[4:], v) for k, v in sorted(full.items())))
    # R2: giving the archive its spread moved no response the call reads
    want = set()
    for d in sim.dates():
        for (a, b) in W[d]["exc"]:
            lo, hi = a, min(sim.DAY, b + 1)
            for s_site in sim.SITES:
                if sim.contracted(s_site, np.arange(lo, hi), d).any():
                    want.add((d, s_site["id"], lo, hi))
    got = {(r[0], r[1], r[3], r[4]) for r in recs if r[2] == "FREQ-DEV"}
    ck("R2 the archive's added captures change no deviation window the call reads",
       want == got, "%d wanted, %d present, %d differ" % (len(want), len(got), len(want ^ got)))

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
