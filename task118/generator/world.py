"""The network, its working timetable and diagrams, the census, the autumn 2026 weekdays as they ran, and
the replays every rung runs on the record (never on the generator's hidden draws)."""
import datetime as dt
import numpy as np
import params as P

HM = P.HM
NST = 11


# ---------------------------------------------------------------------------------------------------------
# Working timetable and diagrams
# ---------------------------------------------------------------------------------------------------------

def _section_time(line, j, direction):
    a = (P.ALLOW_IN if direction == "in" else P.ALLOW_OUT)[line].get(j, 0)
    return P.SRT[line][j], a


def _run_between(line, s0, s1, direction):
    """SRT and allowance (half-minutes) from station s0 to s1 along the line in the given direction."""
    lo, hi = min(s0, s1), max(s0, s1)
    srt = sum(P.SRT[line][j] for j in range(lo, hi))
    allow = sum((P.ALLOW_IN if direction == "in" else P.ALLOW_OUT)[line].get(j, 0) for j in range(lo, hi))
    return srt, allow


def dwell_at(line, stop):
    return P.DWELL_AT[P.STATIONS[line][stop]]


def pathing(line, s0, s1):
    """The booked dwells of the stations a train passes between s0 and s1: it is pathed at stopping speed."""
    lo, hi = min(s0, s1), max(s0, s1)
    return sum(dwell_at(line, s) for s in range(lo + 1, hi))


def make_train(line, direction, kind, dep, stops):
    n = len(stops)
    barr = [None] * n
    bdep = [None] * n
    bdep[0] = dep
    t = dep
    for i in range(1, n):
        srt, allow = _run_between(line, stops[i - 1], stops[i], direction)
        t = t + srt + allow + pathing(line, stops[i - 1], stops[i])
        barr[i] = t
        if i < n - 1:
            bdep[i] = t + dwell_at(line, stops[i])
            t = bdep[i]
    return {"line": line, "dir": direction, "kind": kind, "stops": stops, "barr": barr, "bdep": bdep,
            "period": P.period_of(dep)}


def build_timetable():
    """Returns trains (list, in booked origin order per line) and planned diagrams {unit: [train ids]}."""
    trains = []
    diagrams = {}
    unit_no = {"N": 336101, "E": 336111, "S": 336127}
    HEADWAY = 6        # half-minutes: same-direction departures from a terminus at least three minutes apart
    for line in P.LINES:
        # event loop: each unit's next departure, in time order, held clear of the last departure that way
        pending = []
        for u in range(P.UNITS_PER_LINE):
            pending.append([P.FIRST_DEP + u * P.CYCLE_SPACING, u, "in" if u % 2 == 0 else "out"])
        last = {"in": -10 ** 9, "out": -10 ** 9}
        seqs = {u: [] for u in range(P.UNITS_PER_LINE)}
        while pending:
            pending.sort()
            t, u, d = pending.pop(0)
            if t > P.LAST_DEP:
                continue
            t = max(t, last[d] + HEADWAY)
            last[d] = t
            stops = list(range(NST)) if d == "in" else list(range(NST - 1, -1, -1))
            tr = make_train(line, d, "all", t, stops)
            arr = tr["barr"][-1]
            lay = (P.LAY_CENTRAL if d == "in" else P.LAY_OUTER)[line][P.period_of(arr)]
            tr["planned_unit"] = str(unit_no[line] + u)
            seqs[u].append(len(trains))
            trains.append(tr)
            pending.append([arr + lay, u, "out" if d == "in" else "in"])
        for u in range(P.UNITS_PER_LINE):
            seq = seqs[u]
            for a_, b_ in zip(seq, seq[1:]):
                trains[a_]["lay_after"] = trains[b_]["bdep"][0] - trains[a_]["barr"][-1]
            diagrams[str(unit_no[line] + u)] = seq
    # Ambrey line extras: morning inbound, evening outbound, one unit each
    for x in range(P.N_EXTRAS):
        unit = str(336121 + x)
        am = make_train("E", "in", "extra", P.EXTRA_FIRST + x * P.EXTRA_SPACING, list(P.EXTRA_STOPS))
        am["planned_unit"] = unit
        pm = make_train("E", "out", "extra", P.EXTRA_PM_FIRST + x * P.EXTRA_SPACING, list(reversed(P.EXTRA_STOPS)))
        pm["planned_unit"] = unit
        am["lay_after"] = pm["bdep"][0] - am["barr"][-1]
        pm["lay_after"] = None
        diagrams[unit] = [len(trains), len(trains) + 1]
        trains.append(am)
        trains.append(pm)
    # last working of each unit's day has no next working
    for unit, seq in diagrams.items():
        trains[seq[-1]]["lay_after"] = None
    # headcodes, unique per day: class 2, a letter by line and direction, a two-digit sequence in booked order
    letter = {("N", "in", "all"): "B", ("N", "out", "all"): "N", ("E", "in", "all"): "D", ("E", "out", "all"): "A",
              ("S", "in", "all"): "F", ("S", "out", "all"): "H", ("E", "in", "extra"): "X", ("E", "out", "extra"): "Y"}
    groups = {}
    for i, tr in enumerate(trains):
        groups.setdefault(letter[(tr["line"], tr["dir"], tr["kind"])], []).append(i)
    for L, ids in groups.items():
        ids.sort(key=lambda i: trains[i]["bdep"][0])
        for k, i in enumerate(ids):
            trains[i]["headcode"] = "2%s%02d" % (L, k + 1)
    for i, tr in enumerate(trains):
        tr["id"] = i
    return trains, diagrams


def station_name(tr, k):
    return P.STATIONS[tr["line"]][tr["stops"][k]]


# ---------------------------------------------------------------------------------------------------------
# Census
# ---------------------------------------------------------------------------------------------------------

STATION_WEIGHT = {s: 1.0 for line in P.LINES for s in P.STATIONS[line]}
for s, w in {"Ostley Lane": 1.3, "Brathwick Road": 1.6, "Ambrey Parkway": 1.2, "Pellingham": 1.4,
             "Holcroft Green": 1.2, "Saltgate": 1.7, "Hartlow": 1.1, "Quayside": 1.3, "Mill Wharf": 0.8,
             "Tanner's Row": 0.9, "Exchange Street": 0.9, "Thornell": 0.7, "Fellbrook": 0.8, "Marina": 1.1,
             "Ravelstoke Airport": 4.0, "Skyfield": 1.1}.items():
    STATION_WEIGHT[s] = w


def make_census(trains, rng):
    """ons, offs (integer arrays over each train's stops) for one autumn weekday. Inbound passengers board by
    each station's attraction and mostly ride to Ravelstoke Central; outbound passengers mostly board at
    Ravelstoke Central and alight in proportion to the attraction of the stations still ahead."""
    out = {}
    for tr in trains:
        n = len(tr["stops"])
        ons = np.zeros(n, dtype=int)
        offs = np.zeros(n, dtype=int)
        names = [station_name(tr, i) for i in range(n)]
        wts = np.array([STATION_WEIGHT[s] for s in names])
        if tr["kind"] == "extra":
            if tr["dir"] == "in":
                for i, st in enumerate(tr["stops"][:-1]):
                    ons[i] = rng.poisson(P.EXTRA_ON.get(st, 10))
                offs[-1] = ons.sum()
            else:
                ons[0] = rng.poisson(110)
                onb = ons[0]
                for i in range(1, n):
                    offs[i] = onb if i == n - 1 else int(onb * 0.45)
                    onb -= offs[i]
            out[tr["id"]] = (ons, offs)
            continue
        mult = P.LOAD[tr["line"]][tr["dir"]][tr["period"]]
        onb = 0
        if tr["dir"] == "in":
            for i in range(n):
                if i > 0:
                    if i == n - 1:
                        offs[i] = onb
                    else:
                        offs[i] = int(np.floor(onb * 0.05 * wts[i]))
                    onb -= offs[i]
                if i < n - 1:
                    ons[i] = rng.poisson(mult * P.LOAD_SCALE * wts[i])
                    onb += ons[i]
        else:
            ahead_total = wts[1:].sum()
            for i in range(n):
                if i > 0:
                    if i == n - 1:
                        offs[i] = onb
                    else:
                        rem = wts[i:].sum()
                        offs[i] = int(np.floor(onb * wts[i] / rem))
                    onb -= offs[i]
                if i < n - 1:
                    lam = mult * P.LOAD_SCALE * (0.85 * ahead_total if i == 0 else 0.12 * wts[i])
                    ons[i] = rng.poisson(lam)
                    onb += ons[i]
        out[tr["id"]] = (ons, offs)
    return _as_counted(out, trains)


def _as_counted(out, trains):
    """The census as the counters recorded it: a counter now and then misses or double-counts a passenger or two
    at a stop, so a train's boarders and alighters seldom balance exactly. Drawn on its own stream after every
    train's flows, so no other draw moves."""
    rng = np.random.default_rng(P.SEED + 11)
    for tr in sorted(trains, key=lambda t: t["id"]):
        ons, offs = out[tr["id"]]
        for arr in (ons, offs):
            for i in range(len(arr)):
                if arr[i] > 0 and rng.random() < 0.065:
                    arr[i] = max(0, arr[i] + int(rng.choice([-2, -1, 1, 1, 2])))
    return out


# ---------------------------------------------------------------------------------------------------------
# The weekdays as they ran
# ---------------------------------------------------------------------------------------------------------

def weekdays():
    d = P.RECORD_START
    out = []
    while d <= P.RECORD_END:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def _hm(minutes):
    return int(round(minutes * HM))


def _overrun_mean(tr, k):
    name = station_name(tr, k)
    if name in P.OVERRUN:
        return P.OVERRUN[name][tr["kind"]][tr["dir"]][tr["period"]]
    return P.BASE_OVERRUN


def simulate_day(trains, diagrams, day, rng):
    """One weekday as it ran. Returns {train id: dict(arr=[...], dep=[...], unit=...)} on the half-minute grid."""
    rec = {}
    # disruption increments: (train id, section stop index) -> extra half-minutes
    extra_inc = {}
    for (d, line, direction, t_from, sec, mins) in P.DISRUPTIONS:
        if d != day:
            continue
        cand = sorted([tr for tr in trains if tr["line"] == line and tr["dir"] == direction and tr["kind"] == "all"
                       and tr["bdep"][0] >= t_from], key=lambda tr: tr["bdep"][0])
        for tr, m in zip(cand, mins):
            # the section is identified by its inbound index; find the stop index i whose arrival ends it
            for i in range(1, len(tr["stops"])):
                lo, hi = sorted((tr["stops"][i - 1], tr["stops"][i]))
                if lo <= sec < hi:
                    extra_inc[(tr["id"], i)] = _hm(m)
                    break
    failed = {}
    for (d, line, uidx, t_from) in P.UNIT_FAILURES:
        if d == day:
            base = {"N": 336101, "E": 336111, "S": 336127}[line]
            failed[str(base + uidx)] = (t_from, P.SPARES[len(failed) % len(P.SPARES)])
    for unit, seq in diagrams.items():
        prev_arr = None
        prev_actual_unit = None
        for idx in seq:
            tr = trains[idx]
            actual_unit = unit
            if unit in failed and tr["bdep"][0] >= failed[unit][0]:
                actual_unit = failed[unit][1]
            n = len(tr["stops"])
            arr = [None] * n
            dep = [None] * n
            B0 = tr["bdep"][0]
            chained = prev_arr is not None and actual_unit == prev_actual_unit
            min_dep = prev_arr + P.MIN_TURN if chained else None
            if min_dep is not None and min_dep > B0:
                dep[0] = min_dep
            else:
                od = 0
                if not chained and rng.random() < P.P_ORIGIN:
                    od = _hm(rng.exponential(P.ORIGIN_MEAN))     # late off the depot or sidings
                dep[0] = B0 + od
            t = dep[0]
            for i in range(1, n):
                srt, _ = _run_between(tr["line"], tr["stops"][i - 1], tr["stops"][i], tr["dir"])
                inc = 0
                nsec = abs(tr["stops"][i] - tr["stops"][i - 1])
                for _ in range(nsec):
                    if rng.random() < P.P_INCIDENT:
                        inc += _hm(rng.exponential(P.INCIDENT_MEAN))
                inc += extra_inc.get((tr["id"], i), 0)
                a = t + srt + pathing(tr["line"], tr["stops"][i - 1], tr["stops"][i]) + inc   # held to its path
                arr[i] = a
                if i < n - 1:
                    m = _overrun_mean(tr, i)
                    o = _hm(rng.gamma(2.0, m / 2.0)) if m > 0 else 0
                    dep[i] = max(tr["bdep"][i], a + (tr["bdep"][i] - tr["barr"][i]) + o)
                    t = dep[i]
            rec[idx] = {"arr": arr, "dep": dep, "unit": actual_unit}
            prev_arr = arr[-1]
            prev_actual_unit = actual_unit
    return rec


# ---------------------------------------------------------------------------------------------------------
# Replays on the record
# ---------------------------------------------------------------------------------------------------------

def unit_days(trains, rec, planned_diagrams=None):
    """Each unit's workings that day in time order, from the record's unit numbers (or the planned diagrams)."""
    if planned_diagrams is not None:
        return [list(seq) for seq in planned_diagrams.values()]
    by = {}
    for idx, r in rec.items():
        by.setdefault(r["unit"], []).append(idx)
    return [sorted(v, key=lambda i: rec[i]["dep"][0]) for v in by.values()]


def in_team_hours(t):
    return P.TEAM_FROM <= t < P.TEAM_TO


def replay(trains, rec, census, team=None, mode="full", share=P.TEAM_SHARE, seqs=None, min_turn=P.MIN_TURN):
    """Passenger lateness (passenger-minutes) over the day, every train, with the team at `team` (line, index).

    mode: "full" follows each unit into every later working, "same" never leaves the train, "hop1" carries a
    change the team made on a train into the unit's next working and no further."""
    seqs = seqs if seqs is not None else unit_days(trains, rec)
    total = 0.0
    for seq in seqs:
        prev_rec_arr = None
        prev_cf_arr = None
        prev_direct = False
        for idx in seq:
            tr = trains[idx]
            r = rec[idx]
            n = len(tr["stops"])
            B0 = tr["bdep"][0]
            dep_cf = r["dep"][0]
            bound = prev_rec_arr is not None and r["dep"][0] > B0 and r["dep"][0] == prev_rec_arr + min_turn
            if bound and (mode == "full" or (mode == "hop1" and prev_direct)):
                dep_cf = max(B0, prev_cf_arr + min_turn)
            direct = False
            lat = 0.0
            cf_t = dep_cf
            a_cf = None
            for i in range(1, n):
                run = r["arr"][i] - r["dep"][i - 1]
                a_cf = cf_t + run
                late = a_cf - tr["barr"][i]
                if late > 0:
                    lat += census[idx][1][i] * late
                if i < n - 1:
                    if r["dep"][i] > tr["bdep"][i]:
                        bd = tr["bdep"][i] - tr["barr"][i]
                        o = r["dep"][i] - r["arr"][i] - bd
                        if team is not None and tr["line"] == team[0] and tr["stops"][i] == team[1] \
                                and in_team_hours(tr["bdep"][i]) and o > 0:
                            o = o * (1.0 - share)
                            direct = True
                        cf_t = max(tr["bdep"][i], a_cf + bd + o)
                    else:
                        cf_t = tr["bdep"][i]
            total += lat
            prev_rec_arr = r["arr"][-1]
            prev_cf_arr = a_cf
            prev_direct = direct
    return total / HM


def local_figs(trains, rec, census, team, share=P.TEAM_SHARE):
    """Train-minutes removed and passenger-minutes on board leaving the station, that day."""
    tm = pm = 0.0
    for idx, r in rec.items():
        tr = trains[idx]
        if tr["line"] != team[0]:
            continue
        for i in range(1, len(tr["stops"]) - 1):
            if tr["stops"][i] == team[1] and in_team_hours(tr["bdep"][i]) and r["dep"][i] > tr["bdep"][i]:
                o = r["dep"][i] - r["arr"][i] - (tr["bdep"][i] - tr["barr"][i])
                rem = share * o / HM
                ons, offs = census[idx]
                onb = int(ons[:i + 1].sum() - offs[:i + 1].sum())
                tm += rem
                pm += rem * onb
    return tm, pm


def reactionary(trains, rec):
    """Train-minutes: primary delay put on by each train itself, and lateness its unit brought into its start."""
    prim = {}
    reac = {}
    for seq in unit_days(trains, rec):
        prev_arr = None
        for idx in seq:
            tr = trains[idx]
            r = rec[idx]
            key = (tr["line"], tr["period"])
            B0 = tr["bdep"][0]
            inherited = 0
            if prev_arr is not None and r["dep"][0] > B0 and r["dep"][0] == prev_arr + P.MIN_TURN:
                inherited = r["dep"][0] - B0
            else:
                prim[key] = prim.get(key, 0) + (r["dep"][0] - B0)
            reac[key] = reac.get(key, 0) + inherited
            for i in range(1, len(tr["stops"])):
                run = r["arr"][i] - r["dep"][i - 1]
                srt, _ = _run_between(tr["line"], tr["stops"][i - 1], tr["stops"][i], tr["dir"])
                srt += pathing(tr["line"], tr["stops"][i - 1], tr["stops"][i])
                prim[key] = prim.get(key, 0) + (run - srt)
                if i < len(tr["stops"]) - 1 and r["dep"][i] > tr["bdep"][i]:
                    prim[key] = prim.get(key, 0) + (r["dep"][i] - r["arr"][i] - (tr["bdep"][i] - tr["barr"][i]))
            prev_arr = r["arr"][-1]
    return prim, reac


def build_world():
    rng = np.random.default_rng(P.SEED)
    trains, diagrams = build_timetable()
    census = make_census(trains, np.random.default_rng(P.SEED + 1))
    days = weekdays()
    records = {}
    for d in days:
        records[d] = simulate_day(trains, diagrams, d, np.random.default_rng([P.SEED, d.toordinal(), P.DRAW]))
    return {"trains": trains, "diagrams": diagrams, "census": census, "days": days, "records": records}


def rungs(W):
    trains, census, days, records = W["trains"], W["census"], W["days"], W["records"]
    C = list(P.SHORTLIST)
    S = {c: {k: 0.0 for k in ["R0b", "R0", "R1", "R2a", "R2", "R2plan"]} for c in C}
    prim_t, reac_t = {}, {}
    S1p = {c: {} for c in C}
    base = {"full": 0.0, "same": 0.0}
    for d in days:
        rec = records[d]
        bf = replay(trains, rec, census, None, "full")
        bs = replay(trains, rec, census, None, "same")
        bh = replay(trains, rec, census, None, "hop1")
        bp = replay(trains, rec, census, None, "full", seqs=unit_days(trains, rec, W["diagrams"]))
        base["full"] += bf
        pr, re_ = reactionary(trains, rec)
        for k in pr:
            prim_t[k] = prim_t.get(k, 0) + pr[k]
            reac_t[k] = reac_t.get(k, 0) + re_[k]
        for c in C:
            team = P.SHORTLIST[c]
            tm, pmn = local_figs(trains, rec, census, team)
            S[c]["R0b"] += tm
            S[c]["R0"] += pmn
            S[c]["R1"] += bs - replay(trains, rec, census, team, "same")
            S[c]["R2a"] += bh - replay(trains, rec, census, team, "hop1")
            S[c]["R2"] += bf - replay(trains, rec, census, team, "full")
            S[c]["R2plan"] += bp - replay(trains, rec, census, team, "full",
                                          seqs=unit_days(trains, rec, W["diagrams"]))
    n = len(days)
    for c in C:
        for k in S[c]:
            S[c][k] /= n
    net = sum(reac_t.values()) / sum(prim_t.values())
    line_r = {}
    for ln in P.LINES:
        p_ = sum(v for k, v in prim_t.items() if k[0] == ln)
        r_ = sum(v for k, v in reac_t.items() if k[0] == ln)
        line_r[ln] = r_ / p_
    lp = {k: reac_t[k] / prim_t[k] for k in prim_t if prim_t[k] > 0}
    for c in C:
        ln = P.SHORTLIST[c][0]
        S[c]["RNF"] = S[c]["R1"] * (1 + net)
        S[c]["RLF"] = S[c]["R1"] * (1 + line_r[ln])
    # line-by-period scaling needs the same-train saving split by the period of the trains that carry it
    for d in days:
        rec = records[d]
        for c in C:
            team = P.SHORTLIST[c]
            for idx in rec:
                tr = trains[idx]
                if tr["line"] != team[0] or team[1] not in tr["stops"][1:-1]:
                    continue
                one = {idx: rec[idx]}
                b = replay(trains, one, census, None, "same", seqs=[[idx]])
                a = replay(trains, one, census, team, "same", seqs=[[idx]])
                if b != a:
                    key = (tr["line"], tr["period"])
                    S1p[c][key] = S1p[c].get(key, 0.0) + (b - a) / n
    for c in C:
        S[c]["RPF"] = sum(v * (1 + lp.get(k, 0.0)) for k, v in S1p[c].items())
    info = {"net": net, "line": line_r, "lp": {"%s-%s" % k: v for k, v in lp.items()}, "base_full": base["full"] / n}
    return S, info


if __name__ == "__main__":
    import time
    t0 = time.time()
    W = build_world()
    t1 = time.time()
    S, info = rungs(W)
    print("build %.1fs rungs %.1fs trains/day %d" % (t1 - t0, time.time() - t1, len(W["trains"])))
    for c in S:
        print("%-15s" % c, {k: round(v) for k, v in S[c].items()})
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in info.items() if k != "lp"})
    for r in ["R0b", "R0", "R1", "RNF", "RLF", "RPF", "R2a", "R2", "R2plan"]:
        o = sorted(S, key=lambda c: -S[c][r])
        print("%-6s %-15s %.3f over %s" % (r, o[0], S[o[0]][r] / S[o[1]][r], o[1]))
