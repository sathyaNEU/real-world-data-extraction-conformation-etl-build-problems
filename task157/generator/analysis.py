"""task157 architecture 3: the analysis a solver runs on the cut pack, written against plain record dictionaries so
the same code serves the generator (in memory) and verify.py (rebuilt from the shipped files).

A record is one operated journey: date, route, code, dir, board, tps (timing point keys in travel order), sched and
actual (minutes after local midnight; None where the AVL holds no event). The duty schedule is given as a map
from (day type, board, first journey code of a piece) to the piece that precedes it in its duty: (board, last journey
code, scheduled gap in minutes)."""
from __future__ import annotations

from collections import defaultdict

import params as P

ON_LO, ON_HI = -P.EARLY_S, P.LATE_S


def on_time(late_min):
    s = int(round(late_min * 60))
    return ON_LO <= s <= ON_HI


def punctuality(recs, drop=None, weights=None):
    """drop(route, tp) -> True for a timing point the closure leaves unserved. weights: day type -> weight."""
    n, ok = defaultdict(float), defaultdict(float)
    for x in recs:
        w = weights[x["dt"]] if weights else 1.0
        for i in range(x.get("last_idx", len(x["tps"]) - 1)):
            a = x["actual"][i]
            if a is None:
                continue
            if drop and drop(x["route"], x["tps"][i]):
                continue
            n[x["route"]] += w
            ok[x["route"]] += w * on_time(a - x["sched"][i])
    return {r: 100.0 * ok[r] / n[r] for r in n}


def unserved(route, tp):
    return route == "41" and tp in P.UNSERVED_TPS


def diversion_minutes(dt, minute):
    return P.DIV_MIN_PEAK if P.peak(dt, minute) else P.DIV_MIN_OFF


def imposed(x, scale=1.0, corridor=True, div=True):
    """The minutes the closure itself adds at each timing point of journey x (before any knock-on): route 41's
    diversion from the timing point where it leaves its line, the Ring Road crossing's peak delay on 6 and 12."""
    add = [0.0] * len(x["tps"])
    r = x["route"]
    if div and r == "41":
        start = P.DIV_FROM if x["dir"] == "O" else P.DIV_TO
        k = x["tps"].index(start)
        m = diversion_minutes(x["dt"], x["sched"][k]) * scale
        for i in range(k + 1, len(add)):
            add[i] = m
    if corridor and r in ("6", "12"):
        acc = 0.0
        for i in range(1, len(add)):
            a, b = x["tps"][i - 1], x["tps"][i]
            if (r, a, b) in P.CORRIDOR_LINKS or (r, b, a) in P.CORRIDOR_LINKS:
                if P.peak(x["dt"], x["sched"][i - 1]):
                    acc += P.CORRIDOR_MIN_PEAK
            add[i] = acc
    return add


def last_actual(x):
    """The journey's recorded arrival at its last timing point (where it ended early, the stop it ended at), or,
    where the AVL holds no event there, the last recorded event carried to the scheduled arrival."""
    li = x.get("last_idx", len(x["tps"]) - 1)
    if x["actual"][li] is not None:
        return x["actual"][li]
    for i in range(li, -1, -1):
        if x["actual"][i] is not None:
            return x["sched"][li] + (x["actual"][i] - x["sched"][i])
    return None


def first_actual(x):
    if x["actual"][0] is not None:
        return x["actual"][0]
    for i in range(len(x["actual"])):
        if x["actual"][i] is not None:
            return x["sched"][0] + (x["actual"][i] - x["sched"][i])
    return None


def replay(recs, prev_piece, knock=True, walk=0.0, turn=1.0, scale=1.0, carry_bus=True, gap_aware=True,
           corridor=True, max_gap=30.0, drivers=True):
    """The closure replayed on the recorded days. Every journey keeps its recorded running and the closure adds
    route 41's diversion and the crossing's delay. Where knock is set, the minutes a journey arrives later than it
    did are passed on: to the bus's next journey beyond the stand time it had in the record over turn minutes, and
    (drivers) to the piece of work the driver steps onto, for joins under max_gap minutes, beyond the time he had
    in the record over walk minutes. gap_aware=False passes the incoming minutes on in full whatever the gap (the
    over-corrected reading). Returns new records (actual replaced) with the added minutes at each timing point."""
    by_day = defaultdict(list)
    for x in recs:
        by_day[x["date"]].append(x)
    out = []
    for d, xs in sorted(by_day.items()):
        xs = sorted(xs, key=lambda x: (x["sched"][0], x["board"]))
        added_arr = {}        # code -> minutes later than recorded at the last timing point
        rec_arr = {}
        last_on_board = {}
        for x in xs:
            add = imposed(x, scale=scale, corridor=corridor)
            delta = 0.0
            dep = first_actual(x)
            if knock and dep is not None:
                if carry_bus and x["board"] in last_on_board:
                    pc = last_on_board[x["board"]]
                    if rec_arr.get(pc) is not None:
                        slack = max(0.0, dep - rec_arr[pc] - turn)
                        delta = max(delta, added_arr[pc] - slack)
                link = prev_piece.get((x["dt"], x["board"], x["code"])) if drivers else None
                if link is not None:
                    pboard, pcode, gap = link
                    if gap < max_gap and pcode in added_arr and rec_arr.get(pcode) is not None:
                        if gap_aware:
                            slack = max(0.0, dep - rec_arr[pcode] - walk)
                            delta = max(delta, added_arr[pcode] - slack)
                        else:
                            delta = max(delta, added_arr[pcode])
            delta = max(delta, 0.0)
            y = dict(x)
            y["added"] = [delta + a for a in add]
            y["actual"] = [None if a is None else a + y["added"][i] for i, a in enumerate(x["actual"])]
            added_arr[x["code"]] = y["added"][-1]
            rec_arr[x["code"]] = last_actual(x)
            last_on_board[x["board"]] = x["code"]
            out.append(y)
    return out


def route_level(recs):
    """Rung 0: the route-level disruption assessment, each route at its own record with the closure's direct
    minutes and no knock-on."""
    return replay(recs, {}, knock=False)


def designate(p):
    return sorted([r for r, v in p.items() if v < P.FLOOR], key=lambda r: int(r))
