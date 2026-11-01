"""task157 architecture 3: the registered timetable, the vehicle workings (running boards) and the duty schedule.

Journeys are timed from each route's headway pattern; buses are chained into running boards first in first out at
each terminus; each board is cut into pieces of work at its relief points and the pieces are joined into duties.
At Merchant Row Interchange most of route 27's and route 58's pieces are taken over by drivers stepping off a
route 41 arrival a few minutes earlier (a running changeover), route 33's after a personal needs break, and route
22's after a meal relief; that is how the depot, which sits at the Ravensholme end of route 41, crews its city
routes. Nothing in this module knows about the closure."""
from __future__ import annotations

import numpy as np

import params as P

MIN_LAYOVER = {"41": (14, 14), "27": (3, 3), "58": (3, 3), "33": (4, 4), "22": (4, 4), "6": (6, 3), "12": (6, 4),
               "14": (4, 4), "19": (4, 4)}          # (city end, outer end)
IDLE_PULL_IN = 75                                   # a bus idle longer than this runs to the depot
OUTER_STAND = {"27": 4, "58": 4, "33": 5, "22": 5, "6": 7, "12": 8, "14": 6, "19": 5}


def run_times(route, dt, direction, minute):
    R = P.ROUTES[route]
    pk = P.peak(dt, minute)
    rt = list(R["run_pk"] if pk else R["run_off"])
    if direction == "I":
        rt = rt[::-1]
    return rt


def times_from_dep(route, dt, direction, dep):
    """Scheduled times at each timing point in travel order, from the departure."""
    R = P.ROUTES[route]
    n = len(R["tps"])
    t = [dep]
    for i in range(n - 1):
        pk = P.peak(dt, t[-1])
        rt = R["run_pk"] if pk else R["run_off"]
        link = i if direction == "O" else (n - 2 - i)
        t.append(t[-1] + rt[link] + (R["inbound_extra"][link] if direction == "I" else 0))
    return t


def times_to_arr(route, dt, direction, arr):
    """Scheduled times anchored on the arrival at the last timing point (route 41 inbound is timed to its
    Merchant Row arrival)."""
    dep = arr - sum(run_times(route, dt, direction, arr - 30))
    for _ in range(4):
        t = times_from_dep(route, dt, direction, dep)
        dep += arr - t[-1]
    return times_from_dep(route, dt, direction, dep)


def tp_keys(route, direction):
    keys = [k for k, _ in P.ROUTES[route]["tps"]]
    return keys if direction == "O" else keys[::-1]


def fmt(m):
    m = int(round(m))
    return "%02d%02d" % (m // 60, m % 60)


def journeys(route, dt):
    out = []
    for a, b, h in P.HEADWAYS[route][dt]:
        t = a
        while t <= b:
            out.append(dict(route=route, dt=dt, dir="O", times=times_from_dep(route, dt, "O", t), school=False))
            t += h
    if route == "41":
        # inbound is timed to its Merchant Row arrival, so the city routes' departures can be timed off it
        for a, b, h in P.HEADWAYS[route][dt]:
            t = a
            while t <= b:
                out.append(dict(route=route, dt=dt, dir="I", times=times_to_arr(route, dt, "I", t + 44), school=False))
                t += h
        if dt == "MF":
            for t in P.EARLY_INBOUND["41"]:
                out.append(dict(route=route, dt=dt, dir="I", times=times_from_dep(route, dt, "I", t), school=False))
    else:
        # every other route turns at its outer stand after the route's stand time
        for j in [j for j in out if j["dir"] == "O"]:
            t = j["times"][-1] + OUTER_STAND[route]
            out.append(dict(route=route, dt=dt, dir="I", times=times_from_dep(route, dt, "I", t), school=False))
        if dt == "MF" and route in P.EARLY_INBOUND:
            for t in P.EARLY_INBOUND[route]:
                out.append(dict(route=route, dt=dt, dir="I", times=times_from_dep(route, dt, "I", t), school=False))
    if dt == "MF" and route in ("22", "19"):
        extra = {"22": [("O", 8 * 60 + 20), ("I", 15 * 60 + 35)], "19": [("I", 7 * 60 + 58), ("O", 15 * 60 + 30)]}[route]
        for d, t in extra:
            out.append(dict(route=route, dt=dt, dir=d, times=times_from_dep(route, dt, d, t), school=True))
    for j in out:
        j["tps"] = tp_keys(route, j["dir"])
        j["dep"] = j["times"][0]
        j["arr"] = j["times"][-1]
        j["code"] = "%s-%s-%s-%s%s" % (route, dt, j["dir"], fmt(j["dep"]), "S" if j["school"] else "")
    out.sort(key=lambda j: (j["dep"], j["dir"]))
    codes = [j["code"] for j in out]
    assert len(codes) == len(set(codes)), route
    return out


def blocks(route, dt, js):
    """First in, first out at each terminus; a bus idle longer than IDLE_PULL_IN runs in to the depot. School-day
    journeys run on their own boards."""
    lay_a, lay_b = MIN_LAYOVER[route]
    boards = []
    idle = {"A": [], "B": []}          # (ready, board index, arrived)
    for j in sorted([j for j in js if not j["school"]], key=lambda j: j["dep"]):
        end = "A" if j["dir"] == "O" else "B"
        cands = [x for x in idle[end] if x[0] <= j["dep"]]
        # buses idle too long have gone in
        cands = [x for x in cands if j["dep"] - x[2] <= IDLE_PULL_IN]
        if cands:
            # the bus that turned most recently takes the departure, so a bus no longer needed after the peak
            # stands idle and runs in
            x = max(cands, key=lambda x: (x[0], -x[1]))
            idle[end].remove(x)
            bi = x[1]
        else:
            boards.append([])
            bi = len(boards) - 1
        boards[bi].append(j)
        dest = "B" if j["dir"] == "O" else "A"
        lay = lay_b if dest == "B" else lay_a
        # drop stale entries for this board
        for e in ("A", "B"):
            idle[e] = [x for x in idle[e] if x[1] != bi]
        idle[dest].append((j["arr"] + lay, bi, j["arr"]))
    # a board whose consecutive journeys are more than IDLE_PULL_IN apart is two boards
    split = []
    for b in boards:
        cur = [b[0]]
        for j in b[1:]:
            if j["dep"] - cur[-1]["arr"] > IDLE_PULL_IN:
                split.append(cur)
                cur = [j]
            else:
                cur.append(j)
        split.append(cur)
    split.sort(key=lambda b: b[0]["dep"])
    school = [j for j in js if j["school"]]
    out = []
    for k, b in enumerate(split, 1):
        name = "%s/%02d" % (route, k)
        for j in b:
            j["board"] = name
        out.append(dict(route=route, dt=dt, board=name, journeys=b))
    for k, j in enumerate(sorted(school, key=lambda j: j["dep"]), 1):
        name = "%s/S%d" % (route, k)
        j["board"] = name
        out.append(dict(route=route, dt=dt, board=name, journeys=[j], school=True))
    return out


RELIEF_HUB = {r: "MRI" for r in P.MRI_ROUTES}
RELIEF_HUB.update({r: "GBS" for r in P.GBS_ROUTES})


def city_stand(route):
    return P.ROUTES[route]["tps"][0][0]


def pieces_of(board, cuts):
    """cuts: indexes i such that the board is relieved between journey i-1 and journey i (at the city stand)."""
    js = board["journeys"]
    bounds = [0] + sorted(cuts) + [len(js)]
    out = []
    for a, b in zip(bounds, bounds[1:]):
        if a == b:
            continue
        seg = js[a:b]
        out.append(dict(route=board["route"], board=board["board"], dt=board["dt"], journeys=seg,
                        on=seg[0]["dep"], off=seg[-1]["arr"], on_at=seg[0]["tps"][0], off_at=seg[-1]["tps"][-1],
                        first=a == 0, last=b == len(js), school=board.get("school", False)))
    return out


def city_departures(board):
    """Indexes of the board's journeys that depart the city stand and are not its first journey: the places
    a relief can be made (the incoming driver takes the departure, the outgoing driver stepped off the arrival)."""
    js = board["journeys"]
    return [i for i in range(1, len(js)) if js[i]["dir"] == "O" and js[i - 1]["dir"] == "I"]


def outer_departures(board):
    """Indexes where a route 41 board can be relieved at Ravensholme Bus Station (between an outbound arrival and
    the inbound departure), the depot end of the route."""
    js = board["journeys"]
    return [i for i in range(1, len(js)) if js[i]["dir"] == "I" and js[i - 1]["dir"] == "O"]


def duty_schedule(dt, all_boards, rng):
    """Cut every board into pieces and join the pieces into duties. Returns (pieces, duties, feeds).

    The depot sits at the Ravensholme end of route 41, so route 41 is how the depot's drivers reach the city: a
    driver takes over a 41 at Ravensholme Bus Station, works it into Merchant Row Interchange and steps straight
    onto a route 27 departure three minutes after the arrival or a route 58 departure four minutes after it; a
    driver with a long piece behind him takes a personal needs break before a route 33 departure. The city routes'
    reliefs are placed first, every two to three and a half hours; each is crewed off a route 41 arrival where one
    fits; route 41's boards are cut at those arrivals and at Ravensholme; every remaining long piece is cut; then
    the remaining piece ends and starts are joined by changeovers, meal reliefs and split duties."""
    by_route = {}
    for b in all_boards:
        by_route.setdefault(b["route"], []).append(b)
    cuts = {b["board"]: set() for b in all_boards}
    feeds = []

    def span(b, i, j):
        js = b["journeys"]
        return js[j - 1]["arr"] - js[i]["dep"]

    def bounds(b):
        return [0] + sorted(cuts[b["board"]]) + [len(b["journeys"])]

    def piece_of(b, i):
        bs = bounds(b)
        for a, z in zip(bs, bs[1:]):
            if a <= i < z:
                return a, z
        return None

    # 1. the city routes' reliefs at the interchange, each crewed from a route 41 arrival where one fits (one
    # driver steps off each arrival, so a relief that would need an arrival already used moves to the board's next
    # departure from the interchange)
    plan = {"27": (100, 165), "58": (72, 130), "33": (120, 210)}
    gaps = {"27": (3, 3), "58": (4, 4), "33": (4 + P.PNB, 4 + P.PNB + 11)}
    share = {"27": 0.96, "58": 0.96, "33": 0.55}
    arrivals = []
    for b in by_route.get("41", []):
        if b.get("school"):
            continue
        for k, j in enumerate(b["journeys"]):
            if j["dir"] == "I" and k + 1 < len(b["journeys"]):
                arrivals.append((j["arr"], b, k))
    used = set()
    state = {}
    for r in plan:
        for b in by_route.get(r, []):
            if not b.get("school"):
                state[b["board"]] = dict(r=r, b=b, last=0, target=rng.uniform(*plan[r]))
    events = sorted([(st["b"]["journeys"][i]["dep"], st["r"], name, i) for name, st in state.items()
                     for i in city_departures(st["b"])], key=lambda x: (x[0], x[1], x[2]))
    pending = {}
    for d, r, name, i in events:
        st = state[name]
        b = st["b"]
        js = b["journeys"]
        if span(b, st["last"], i) < st["target"] or span(b, i, len(js)) < 75:
            continue
        fed = rng.random_sample() <= share[r]
        lo, hi = gaps[r]
        opts = [(a, b41, k) for a, b41, k in arrivals if lo <= d - a <= hi and (b41["board"], k) not in used]
        if fed and not opts and span(b, st["last"], i) < plan[r][1] + 25:
            continue                      # wait for the next departure, which an arrival can crew
        cuts[name].add(i)
        st["last"] = i
        st["target"] = rng.uniform(*plan[r])
        if fed and opts:
            a, b41, k = max(opts, key=lambda x: (x[0], x[1]["board"]))
            used.add((b41["board"], k))
            cuts[b41["board"]].add(k + 1)
            feeds.append((b41, k, b, i, r, int(round(d - a))))
    # 3. route 41: the piece ending at a feeding arrival starts at Ravensholme when it would otherwise run long
    for b in by_route.get("41", []):
        if b.get("school"):
            continue
        js = b["journeys"]
        feed_ks = sorted(k for b41, k, *_ in feeds if b41 is b)
        for k in feed_ks:
            a, z = piece_of(b, k)
            if span(b, a, k + 1) > rng.uniform(75, 150):
                cand = [i for i in outer_departures(b) if a < i <= k]
                if cand:
                    cuts[b["board"]].add(max(cand) if rng.random_sample() < 0.6 else min(cand))
    # 4. every board's remaining long pieces
    for b in all_boards:
        if b.get("school"):
            continue
        hi = 270 if b["route"] != "41" else 200
        changed = True
        while changed:
            changed = False
            for a, z in zip(bounds(b), bounds(b)[1:]):
                if span(b, a, z) > hi:
                    cand = [i for i in city_departures(b) if a < i < z]
                    if b["route"] == "41":
                        cand += [i for i in outer_departures(b) if a < i < z]
                    cand = [i for i in cand if span(b, a, i) >= 60 and span(b, i, z) >= 60]
                    if cand:
                        pick = min(cand, key=lambda i: abs(span(b, a, i) - rng.uniform(130, 210)))
                        cuts[b["board"]].add(pick)
                        changed = True
                        break
    # 5. pieces
    pieces = []
    first_of, last_of = {}, {}
    for b in all_boards:
        for p in pieces_of(b, cuts[b["board"]]):
            p["id"] = len(pieces)
            pieces.append(p)
            first_of[(b["board"], b["journeys"].index(p["journeys"][0]))] = p["id"]
            last_of[(b["board"], b["journeys"].index(p["journeys"][-1]))] = p["id"]
    nxt, prv = {}, {}
    for b41, k, b, i, r, g in feeds:
        a, z = last_of[(b41["board"], k)], first_of[(b["board"], i)]
        nxt[a], prv[z] = z, a

    def place(p, end):
        if end:
            return "DEPOT" if p["last"] else p["off_at"]
        return "DEPOT" if p["first"] else p["on_at"]

    def hub(stand):
        if stand in ("RBS", "DEPOT"):
            return "DEPOT"
        return stand[:3]

    def run_back(pid):
        tot = pieces[pid]["off"] - pieces[pid]["on"]
        while pid in prv:
            q = prv[pid]
            if pieces[pid]["on"] - pieces[q]["off"] >= 30:
                break
            pid = q
            tot += pieces[pid]["off"] - pieces[pid]["on"]
        return tot

    def head(pid):
        while pid in prv:
            pid = prv[pid]
        return pid

    def count(pid):
        n = 1
        while pid in prv:
            pid = prv[pid]
            n += 1
        return n

    def tail(pid):
        while pid in nxt:
            pid = nxt[pid]
        return pid

    # 6. the other joins: a changeover at the same place (straight on at the bus station; with a personal needs
    # break at the interchange), a meal relief, a split duty
    for kind in ("change", "meal", "split"):
        ends = sorted([p for p in pieces if p["id"] not in nxt and place(p, True) != "DEPOT"], key=lambda p: p["off"])
        for p in ends:
            if p["id"] in nxt or count(p["id"]) >= 4:
                continue
            best = None
            for q in sorted([q for q in pieces if q["id"] not in prv and place(q, False) != "DEPOT"
                             and q["id"] != p["id"] and hub(place(q, False)) == hub(place(p, True))
                             and q["on"] > p["off"]], key=lambda q: q["on"]):
                gap = q["on"] - p["off"]
                if gap > 430:
                    break
                w = P.WALK.get((p["off_at"], q["on_at"]), 0)
                t = pieces[tail(q["id"])]
                spread = t["off"] - pieces[head(p["id"])]["on"]
                n_after = 1
                z = q["id"]
                while z in nxt:
                    z = nxt[z]
                    n_after += 1
                if count(p["id"]) + n_after > 4:
                    continue
                if q["id"] in nxt:
                    continue
                if kind == "change":
                    at_mri = hub(place(p, True)) == "MRI"
                    lo_g, hi_g = (w + P.PNB, w + P.PNB + 10) if at_mri else (w + 2, w + 8)
                    if q["route"] != p["route"] and lo_g <= gap <= hi_g and \
                            run_back(p["id"]) + (q["off"] - q["on"]) <= 330 and spread <= 600:
                        best = q
                        break
                elif kind == "meal":
                    if 32 <= gap <= 70 and spread <= 640:
                        best = q
                        break
                else:
                    if 150 <= gap <= 420 and spread <= 760 and count(p["id"]) == 1:
                        best = q
                        break
            if best is not None:
                nxt[p["id"]], prv[best["id"]] = best["id"], p["id"]
    duties = []
    for p in sorted(pieces, key=lambda p: p["on"]):
        if p["id"] in prv:
            continue
        chain = [p["id"]]
        while chain[-1] in nxt:
            chain.append(nxt[chain[-1]])
        duties.append(chain)
    return pieces, duties, feeds


def _chain_count(pid, prv):
    n = 1
    while pid in prv:
        pid = prv[pid]
        n += 1
    return n


def _chain_len(pid, prv, pieces):
    """platform minutes of the run of pieces joined by running changeovers ending at pid"""
    tot = pieces[pid]["off"] - pieces[pid]["on"]
    while pid in prv:
        q = prv[pid]
        if pieces[pid]["on"] - pieces[q]["off"] >= 30:
            break
        pid = q
        tot += pieces[pid]["off"] - pieces[pid]["on"]
    return tot


def build(seed=P.SEED):
    """The whole schedule for the three day types."""
    rng = np.random.RandomState(seed)
    out = {}
    for dt in ("MF", "SA", "SU"):
        js = {r: journeys(r, dt) for r in P.ROUTE_ORDER}
        bds = []
        for r in P.ROUTE_ORDER:
            bds += blocks(r, dt, js[r])
        pieces, duties, feeds = duty_schedule(dt, bds, rng)
        out[dt] = dict(journeys=js, boards=bds, pieces=pieces, duties=duties, feeds=feeds)
    return out


if __name__ == "__main__":
    S = build()
    for dt in ("MF", "SA", "SU"):
        s = S[dt]
        nj = sum(len(v) for v in s["journeys"].values())
        print(dt, "journeys", nj, "boards", len(s["boards"]), "pieces", len(s["pieces"]), "duties", len(s["duties"]),
              "feeds", len(s["feeds"]))
        from collections import Counter
        print("  boards per route", Counter(b["route"] for b in s["boards"]))
        print("  feeds per route", Counter(f[4] for f in s["feeds"]), Counter(f[5] for f in s["feeds"]))
        pcs = s["pieces"]
        starts = Counter(p["route"] for p in pcs if not p["first"])
        print("  relieved pieces per route", starts)
        lens = [p["off"] - p["on"] for p in pcs]
        print("  piece length min/median/max", min(lens), np.median(lens), max(lens))
        dl = Counter(len(d) for d in s["duties"])
        print("  duty sizes", dl)
