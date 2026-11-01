"""task157 architecture 3: the autumn's operation, day by day, from the schedule in network.py.

Every board's vehicle runs its journeys; a journey leaves its first timing point when the timetable, the bus and
the driver allow (a relieving driver is ready when the piece of work he stepped off has arrived and he has walked to
the stand); links run at the day's traffic; buses running early hold at timing points. Incidents, weather and
lost mileage come from their own random streams. The same engine runs the closure world (the diversion and the
Ring Road delay imposed on the same days' draws), which the checks use to confirm the forecast's set is the set the
closure actually produces."""
from __future__ import annotations

from datetime import date, datetime, timedelta

import numpy as np

import network as N
import params as P

TURN = 1.0          # minutes a bus needs between arriving and leaving again
VARIAB = {"41": 1.45, "6": 0.95, "12": 0.95, "14": 1.0, "19": 1.05, "22": 1.0, "27": 1.0, "33": 1.05, "58": 1.0}
SLOW_P = {"41": 0.12, "6": 0.07, "12": 0.08, "14": 0.07, "19": 0.08, "22": 0.07, "27": 0.07, "33": 0.07, "58": 0.06}


def piece_links(S):
    """For each day type: piece id -> (predecessor piece id, scheduled gap) for joins shorter than 30 minutes, and
    the index from (board, journey code) to piece id."""
    out = {}
    for dt, s in S.items():
        pieces = s["pieces"]
        prev = {}
        for duty in s["duties"]:
            for a, b in zip(duty, duty[1:]):
                g = pieces[b]["on"] - pieces[a]["off"]
                prev[b] = (a, g)
        first = {}
        for p in pieces:
            first[(p["board"], p["journeys"][0]["code"])] = p["id"]
        out[dt] = dict(prev=prev, first=first)
    return out


def incidents(rng):
    """The autumn's road incidents on route 41's line and elsewhere, and the network-wide days."""
    ev = []
    # (date, route or None for all, links affected as (from, to) keys or None for all, start, end, added minutes)
    ev.append((date(2026, 9, 15), "41", [("RVR", "TQY"), ("TQY", "THR")], 7 * 60 + 50, 9 * 60 + 35, 11.0,
               "RTC Ravensholme Road"))
    ev.append((date(2026, 10, 8), "41", [("TNS", "THR"), ("THR", "TNS")], 13 * 60 + 5, 15 * 60 + 40, 8.0,
               "burst water main Tenter Street"))
    ev.append((date(2026, 10, 21), "41", [("THR", "TQY"), ("TQY", "THR")], 16 * 60 + 20, 18 * 60 + 10, 9.0,
               "broken-down HGV on Thornsby Bridge"))
    ev.append((date(2026, 11, 13), "41", [("RVR", "TQY")], 7 * 60 + 40, 9 * 60 + 5, 7.0,
               "temporary lights Ravensholme Road (emergency gas)"))
    ev.append((date(2026, 9, 24), "27", [("CSM", "SKR"), ("SKR", "CSM")], 10 * 60 + 15, 12 * 60 + 20, 9.0,
               "police closure Castle Mount"))
    ev.append((date(2026, 10, 14), "6", [("RJ4", "SML"), ("SML", "RJ4")], 16 * 60 + 5, 18 * 60 + 25, 7.0,
               "collision Ring Road crossing"))
    ev.append((date(2026, 11, 4), "58", [("CHS", "GRR"), ("GRR", "CHS")], 11 * 60 + 30, 13 * 60 + 10, 6.0,
               "burst main Garrow Lane"))
    ev.append((date(2026, 11, 26), "33", [("HLM", "UPC"), ("UPC", "HLM")], 15 * 60 + 40, 17 * 60 + 50, 8.0,
               "police incident Holm Lane"))
    ev.append((date(2026, 10, 2), "14", [("MLB", "MSL"), ("MSL", "MLB")], 8 * 60, 9 * 60 + 40, 7.0,
               "flooding Mill Bank"))
    ev.append((date(2026, 11, 19), "22", [("DYR", "HRR"), ("HRR", "DYR")], 7 * 60 + 35, 9 * 60 + 20, 6.0,
               "RTC Dyer Street"))
    wide = {date(2026, 10, 23): 1.22, date(2026, 11, 27): 1.18, date(2026, 12, 4): 1.16, date(2026, 9, 29): 1.12,
            date(2026, 11, 6): 1.10}
    return ev, wide


FLEET_POOL = {"41": 11, "6": 9, "12": 7, "14": 6, "19": 7, "22": 6, "27": 7, "33": 6, "58": 7}
SPARES = 9


def fleet(seed=P.SEED):
    """The depot's fleet: fleet number, registration, ticket machine unit, type, allocated route."""
    rng = np.random.RandomState(seed + 11)
    out = []
    num = 3101
    letters = "ABCDEFGHJKLMNOPRSTUVWXYZ"
    seen = set()
    for r in P.ROUTE_ORDER + ["SPARE"]:
        n = FLEET_POOL.get(r, SPARES)
        for _ in range(n):
            dd = r in ("41", "6", "SPARE") and rng.random_sample() < 0.8
            year = int(rng.choice([15, 16, 17, 18, 19, 21, 22, 23]))
            age = {15: "15", 16: "66", 17: "17", 18: "68", 19: "19", 21: "21", 22: "72", 23: "73"}[year]
            while True:
                reg = "Y%s%s %s" % (rng.choice(list("JKNXT")), age, "".join(rng.choice(list(letters), 3)))
                if reg not in seen:
                    seen.add(reg)
                    break
            out.append(dict(fleet=num, reg=reg, etm="TKR%05d" % int(rng.randint(10000, 99999)),
                            type=("Double deck" if dd else "Single deck"), route=r,
                            year=2000 + year))
            num += 1
    return out


FLEET = fleet()
OUTAGE_DAY = date(2026, 11, 17)


def plan_disruptions(S, d, seed, force_late=()):
    """The day's lost mileage and its causes, drawn on its own stream so the running draws never move.
    Returns dict(board_k -> event) where an event is (kind, cause, first_lost_tp, last_lost_tp) and the uncovered
    duties for the depot's return."""
    dt = P.day_type(d)
    s = S[dt]
    rng = np.random.RandomState(seed)
    school = P.is_school_day(d)
    boards = [b for b in s["boards"] if not (b.get("school") and not school)]
    ev, _ = incidents(None)
    lost = {}
    meta = dict(uncovered=[], breakdowns=[], ill=[], curtail=[])
    # uncovered duties: no driver; each piece is covered by a spare or lost, some covered part way through
    n_unc = rng.poisson({"MF": 0.5, "SA": 0.45, "SU": 0.3}[dt])
    pieces = s["pieces"]
    duties = s["duties"]
    for di in rng.choice(len(duties), size=min(n_unc, len(duties)), replace=False):
        for pn, pid in enumerate(duties[di], 1):
            p = pieces[pid]
            if p.get("school") and not school:
                continue
            u = rng.random_sample()
            u_late, u_first = rng.random_sample(), rng.random_sample()
            if u < 0.42:
                continue                                   # a spare covered the piece
            bidx = {j["code"]: k for k, j in enumerate(next(b for b in s["boards"] if b["board"] == p["board"])["journeys"])}
            ks = [bidx[j["code"]] for j in p["journeys"]]
            covered_from = None
            late = None
            if (u_late < 0.30 or p["route"] in force_late) and d != OUTAGE_DAY and u <= 0.80:
                # the depot returned the piece uncovered; the control room found a spare later that morning
                late = p["journeys"][0]["dep"] if u_first < 0.5 or len(ks) < 3 else p["journeys"][1]["dep"]
                ks = [] if late == p["journeys"][0]["dep"] else ks[:1]
            elif u > 0.80 and len(ks) > 2:
                cut = int(rng.randint(1, len(ks) - 1))
                covered_from = p["journeys"][cut]["dep"]
                ks = ks[:cut]
            for k in ks:
                lost.setdefault((p["board"], k), ("whole", "SS", 0, len(p["journeys"][0]["tps"]) - 1))
            meta["uncovered"].append((int(di), pn, pid, covered_from, late))
    # a route with no late cover yet in the autumn gets one: a piece of one of its duties returned uncovered and
    # covered by a spare from its first or second journey
    have = {s["pieces"][u[2]]["route"] for u in meta["uncovered"] if u[4] is not None}
    for r in force_late:
        if r in have or dt != "MF" or d == OUTAGE_DAY:
            continue
        cand = [(i, pn) for i, duty in enumerate(duties) for pn, pid in enumerate(duty, 1)
                if pieces[pid]["route"] == r and not pieces[pid].get("school") and len(pieces[pid]["journeys"]) >= 3]
        if not cand:
            continue
        di, pn = cand[int(rng.randint(len(cand)))]
        p = pieces[duties[di][pn - 1]]
        second = rng.random_sample() < 0.5
        late = p["journeys"][1]["dep"] if second else p["journeys"][0]["dep"]
        if second:
            bidx = {j["code"]: k for k, j in enumerate(next(b for b in s["boards"] if b["board"] == p["board"])["journeys"])}
            k0 = bidx[p["journeys"][0]["code"]]
            lost.setdefault((p["board"], k0), ("whole", "SS", 0, len(p["journeys"][0]["tps"]) - 1))
        meta["uncovered"].append((int(di), pn, duties[di][pn - 1], None, late))
    # drivers taken ill part way through a piece: one or two journeys lost before a spare arrives
    for _ in range(rng.poisson({"MF": 0.3, "SA": 0.25, "SU": 0.15}[dt])):
        b = boards[int(rng.randint(len(boards)))]
        js = b["journeys"]
        if len(js) < 4:
            continue
        k0 = int(rng.randint(1, len(js) - 2))
        for k in range(k0, k0 + int(rng.randint(1, 3))):
            lost.setdefault((b["board"], k), ("whole", "SI", 0, len(js[k]["tps"]) - 1))
        meta["ill"].append((b["board"], k0))
    # vehicle defects: the journey is lost from the timing point after the failure, the board's next journey too
    for b in boards:
        js = b["journeys"]
        for k in range(1, len(js)):
            if rng.random_sample() < 0.0007 and (b["board"], k) not in lost and (b["board"], k + 1) not in lost:
                i = int(rng.randint(1, len(js[k]["tps"])))
                lost[(b["board"], k)] = ("part", "VD", i, len(js[k]["tps"]) - 1)
                if k + 1 < len(js):
                    lost[(b["board"], k + 1)] = ("whole", "VD", 0, len(js[k + 1]["tps"]) - 1)
                meta["breakdowns"].append((b["board"], k, i))
                break
    # journeys turned short: at a road incident on the route, or to restore a late service
    for (ed, er, elinks, es, ee, add, why) in ev:
        if ed != d:
            continue
        for b in boards:
            if b["route"] != er:
                continue
            js = b["journeys"]
            for k, j in enumerate(js):
                if not (es - 20 <= j["dep"] < ee) or (b["board"], k) in lost or k + 1 >= len(js):
                    continue
                if rng.random_sample() < 0.3:
                    tps = j["tps"]
                    idx = [i for i in range(1, len(tps)) if (tps[i - 1], tps[i]) in elinks]
                    if not idx:
                        continue
                    i = idx[0]
                    lost[(b["board"], k)] = ("part", "PC", i, len(tps) - 1)
                    # the return journey starts from the stop where it turned
                    nj = js[k + 1]
                    t2 = nj["tps"]
                    stop = tps[i - 1]
                    if stop in t2 and (b["board"], k + 1) not in lost:
                        lost[(b["board"], k + 1)] = ("start", "PC", 0, t2.index(stop) - 1)
                    meta["curtail"].append((b["board"], k, why))
    for _ in range(rng.poisson({"MF": 0.7, "SA": 0.5, "SU": 0.2}[dt])):
        b = boards[int(rng.randint(len(boards)))]
        js = b["journeys"]
        if len(js) < 3:
            continue
        k = int(rng.randint(1, len(js) - 1))
        j = js[k]
        if (b["board"], k) in lost or (b["board"], k + 1) in lost:
            continue
        tps = j["tps"]
        i = int(rng.randint(2, len(tps))) if len(tps) > 2 else 1
        lost[(b["board"], k)] = ("part", "TR", i, len(tps) - 1)
        nj = js[k + 1]
        stop = tps[i - 1]
        if stop in nj["tps"]:
            lost[(b["board"], k + 1)] = ("start", "TR", 0, nj["tps"].index(stop) - 1)
        meta["curtail"].append((b["board"], k, "late running"))
    return lost, meta


def assign_vehicles(S, d, seed, school, lost):
    """Each board's vehicle for the day, from its route's allocation (spares fill in); a board whose bus failed
    takes a spare for the rest of the day."""
    dt = P.day_type(d)
    rng = np.random.RandomState(seed)
    fl = FLEET
    pool = {r: [v for v in fl if v["route"] == r] for r in P.ROUTE_ORDER}
    spares = [v for v in fl if v["route"] == "SPARE"]
    rng.shuffle(spares)
    out = {}
    used = set()
    for r in P.ROUTE_ORDER:
        vs = list(pool[r])
        rng.shuffle(vs)
        # a few buses spend the day off their own route
        bds = [b for b in S[dt]["boards"] if b["route"] == r and not (b.get("school") and not school)]
        for b in bds:
            # boards that run at different times can share a bus; keep it simple: one bus per board
            while vs and vs[0]["fleet"] in used:
                vs.pop(0)
            v = vs.pop(0) if vs else spares.pop(0)
            used.add(v["fleet"])
            failed = False
            for k, j in enumerate(b["journeys"]):
                ls = lost.get((b["board"], k))
                if failed is False and ls is not None and ls[1] == "VD" and ls[0] == "part":
                    out[(b["board"], k)] = v["reg"]
                    failed = True
                    v = spares.pop(0) if spares else v
                    used.add(v["fleet"])
                    continue
                out[(b["board"], k)] = v["reg"]
    return out


def simulate(S, closure=False, seed=P.SEED, days=None, want_meta=False):
    """Run every day. Returns a list of journey records: dict(date, dt, route, code, dir, board, tps, sched,
    actual (minutes after local midnight, float), lost (None or index of the first lost timing point), vehicle)."""
    links = piece_links(S)
    meta_all = {}
    ev, wide = incidents(None)
    days = list(days or P.days(P.AVL_FIRST, P.AVL_LAST))
    master = np.random.RandomState(seed)
    day_seeds = {d: int(master.randint(0, 2 ** 31 - 1)) for d in P.days(P.AVL_FIRST, P.AVL_LAST)}
    route_level = {r: master.normal(0, 0.035) for r in P.ROUTE_ORDER}
    route_level.update({'19': 0.0472, '6': 0.0341, '12': 0.054, '41': 0.0191, '27': -0.0704, '58': -0.0577, '33': 0.081, '22': 0.0265, '14': 0.0248})
    out = []
    out_lost = []
    late_seen = set()
    for d in days:
        dt = P.day_type(d)
        s = S[dt]
        rng = np.random.RandomState(day_seeds[d])
        school = P.is_school_day(d)
        dayf = rng.normal(0.0, 0.05) + (wide.get(d, 1.0) - 1.0)
        # hourly traffic shape per route (shared across links of a route)
        hour_f = {r: rng.normal(0, 0.06, 26) for r in P.ROUTE_ORDER}
        lk = links[dt]
        recs = {}
        arr_of = {}         # journey code -> actual arrival at the last timing point (for drivers)
        # boards in order of first departure; drivers chain across boards, so process journeys globally in time
        # order of scheduled departure, which respects every dependency (a driver's next piece starts after the
        # arrival that frees him, a bus's next journey after its arrival)
        todo = []
        for b in s["boards"]:
            if b.get("school") and not school:
                continue
            for k, j in enumerate(b["journeys"]):
                todo.append((j["dep"], b["board"], k, j))
        todo.sort(key=lambda x: (x[0], x[1]))
        bus_ready = {}
        force = tuple(r for r in P.ROUTE_ORDER if r not in late_seen) if d >= date(2026, 11, 2) else ()
        lost, _meta = plan_disruptions(S, d, day_seeds[d] + 7, force_late=force)
        for u in _meta["uncovered"]:
            if u[4] is not None:
                late_seen.add(s["pieces"][u[2]]["route"])
        veh = assign_vehicles(S, d, day_seeds[d] + 13, school, lost)
        for dep, board, k, j in todo:
            r = j["route"]
            sched = j["times"]
            tps = j["tps"]
            ls = lost.get((board, k))
            if ls is not None and ls[0] == "whole":
                bus_ready.pop(board, None)        # the next journey leaves on time (a replacement, or a spare)
                out_lost.append(dict(date=d, dt=dt, route=r, code=j["code"], dir=j["dir"], board=board, tps=tps,
                                     sched=sched, lost=ls, k=k))
                continue
            ready = sched[0]
            if board in bus_ready:
                ready = max(ready, bus_ready[board])
            pid = lk["first"].get((board, j["code"]))
            if pid is not None and pid in lk["prev"]:
                a, g = lk["prev"][pid]
                pa = s["pieces"][a]
                last_code = pa["journeys"][-1]["code"]
                if g < 30 and last_code in arr_of:
                    w = P.WALK.get((pa["off_at"], s["pieces"][pid]["on_at"]), 2)
                    ready = max(ready, arr_of[last_code] + w + 0.3)
            # departure noise: most leave on time to a minute late
            u, s_a, s_b, s_c = rng.random_sample(), rng.uniform(-0.2, 1.1), rng.uniform(1.1, 3.0), rng.uniform(0.0, 0.4)
            start = sched[0] + (s_a if u < 0.93 else s_b)
            act = [max(start, ready + s_c) if ready > sched[0] else start]
            for i in range(1, len(tps)):
                a_key, b_key = tps[i - 1], tps[i]
                run = sched[i] - sched[i - 1]
                if closure and r == "41":
                    pass
                hour = int(act[-1] // 60)
                f = 1.0 + route_level[r] + dayf + hour_f[r][min(hour, 25)]
                if P.peak(dt, sched[i - 1]):
                    f += 0.09
                if school and r in ("22", "19", "33") and (8 * 60 <= sched[i - 1] < 9 * 60 or 15 * 60 <= sched[i - 1] < 16 * 60):
                    f += 0.06
                z_run, z_slow, z_gam, z_ev, z_cor, z_div = (rng.normal(0, 1), rng.random_sample(),
                                                             rng.gamma(2.0, 1.4), rng.uniform(0.75, 1.25),
                                                             rng.uniform(0.8, 1.2), rng.uniform(0.85, 1.15))
                x = run * f + z_run * (0.17 * run + 0.25) * VARIAB[r]
                if z_slow < SLOW_P[r]:
                    x += z_gam
                x = max(x, 0.72 * run)
                for (ed, er, elinks, es, ee, add, _) in ev:
                    if ed == d and er == r and (a_key, b_key) in elinks and es <= act[-1] < ee:
                        x += add * z_ev
                if closure:
                    if (r, a_key, b_key) in P.CORRIDOR_LINKS or (r, b_key, a_key) in P.CORRIDOR_LINKS:
                        if P.peak(dt, sched[i - 1]):
                            x += P.CORRIDOR_MIN_PEAK * z_cor
                    if r == "41" and ((j["dir"] == "O" and a_key == P.DIV_FROM and b_key == "THR")
                                      or (j["dir"] == "I" and a_key == P.DIV_TO and b_key == "TQY")):
                        x += (P.DIV_MIN_PEAK if P.peak(dt, sched[i - 1]) else P.DIV_MIN_OFF) * z_div
                t = act[-1] + x
                h_u, h_a, h_b, h_c = (rng.random_sample(), rng.uniform(-0.4, 0.3), rng.uniform(0.6, 2.2),
                                      rng.uniform(0.0, 0.5))
                if i < len(tps) - 1:
                    # hold at a timing point when early (most drivers do, a few leave a little early)
                    if t < sched[i] - 0.3:
                        if h_u < 0.9:
                            t = sched[i] + h_a
                        else:
                            t = max(t, sched[i] - h_b)
                    else:
                        t += h_c      # dwell when on time or late
                act.append(t)
            if ls is not None and ls[0] == "part":
                act = [a if i < ls[2] else None for i, a in enumerate(act)]
                bus_ready.pop(board, None)
            elif ls is not None and ls[0] == "start":
                # the bus picks the journey up at the stop where it turned: no events before it
                act = [None if i <= ls[3] else a for i, a in enumerate(act)]
                bus_ready[board] = act[-1] + TURN
            else:
                bus_ready[board] = act[-1] + TURN
            if act[-1] is not None:
                arr_of[j["code"]] = act[-1]
            recs[(board, k)] = dict(date=d, dt=dt, route=r, code=j["code"], dir=j["dir"], board=board, tps=tps,
                                    sched=sched, actual=act, lost=ls, vehicle=veh[(board, k)], k=k)
        out.extend(recs.values())
        for (board, k), ls in lost.items():
            if ls[0] != "whole" and (board, k) in recs:
                rec = recs[(board, k)]
                out_lost.append(dict(date=d, dt=dt, route=rec["route"], code=rec["code"], dir=rec["dir"], board=board,
                                     tps=rec["tps"], sched=rec["sched"], lost=ls, k=k))
        meta_all[d] = _meta
    if want_meta:
        return out, out_lost, meta_all
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    S = N.build()
    base = simulate(S)
    print("simulated", len(base), "journeys in %.1fs" % (time.time() - t0))
    import analysis as A
    pb = A.punctuality(base)
    clo = simulate(S, closure=True)
    pc = A.punctuality(clo, drop=A.unserved)
    for r in P.ROUTE_ORDER:
        print("%3s  autumn %5.1f   closure world %5.1f" % (r, pb[r], pc[r]))
