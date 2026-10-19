"""Every stop the two feeds hold and where it stands: the routes' full stop patterns (the timepoints and the stops
between them, each outbound stop with a twin across the street for the inbound trips), the spring timetable's far-side
moves (a stop keeps its code and its name and moves to the far side of its intersection), the stops it closed,
Facilities' bus stop amenity inventory as each stop was last inspected, and Capital Projects' shelter work orders."""
import datetime as dt
import math

import numpy as np

import world as W

LAT0, LON0 = 41.1189, -98.0021            # the Transit Mall, Main St & 4th St
SPEED = 330.0                             # metres a scheduled minute, away from the transfer points
POS = {"A": (0.0, 0.0), "B": (0.0, 520.0), "C": (700.0, -300.0), "D": (-2500.0, 2400.0), "E": (-4200.0, -600.0)}
BEARING = {"2": -90, "4": -20, "17": -135, "3": 180, "6": 45, "9": 5, "11": None, "14": 95, "22": -35, "12": 65,
           "31": 120, "40": 10, "51": -150, "60": 150}
MAIN_STREET = {"2": "Grand Ave", "4": "Lincoln Ave", "17": "Prairie Rd", "3": "Westside Dr", "6": "Oak St",
               "9": "Riverside Dr", "11": "University Ave", "14": "Elm Park Blvd", "22": "Fairgrounds Rd",
               "12": "Northgate Rd", "31": "College Hill Rd", "40": "Crosstown Blvd", "51": "Hillcrest Dr",
               "60": "Mill Creek Rd"}
CROSS = ["Adler St", "Bancroft Ave", "Bishop St", "Calloway Ave", "Carver St", "Chandler Ave", "Colfax St", "Dawson Ave",
         "Delmar St", "Draper Ave", "Easton St", "Emery Ave", "Fairview St", "Fletcher Ave", "Garland St", "Gilman Ave",
         "Granger St", "Hadley Ave", "Harmon St", "Hazel St", "Hollis Ave", "Irving St", "Jasper Ave", "Juniper St",
         "Keaton Ave", "Kimball St", "Lacey Ave", "Laurel St", "Linwood Ave", "Locust St", "Madison Ave", "Maple St",
         "Marlow Ave", "Monroe St", "Myrtle Ave", "Nolan St", "Norris Ave", "Orchard St", "Osage Ave", "Parker St",
         "Pierce Ave", "Poplar St", "Quincy Ave", "Ramsey St", "Redwood Ave", "Rowan St", "Sage Ave", "Sawtelle St",
         "Seward Ave", "Spruce St", "Sumner Ave", "Tamarack St", "Taylor Ave", "Thayer St", "Tilden Ave", "Union Ave",
         "Upton St", "Vale Ave", "Vernon St", "Wabash Ave", "Walnut St", "Warren Ave", "Waverly St", "Webster Ave",
         "Whitney St", "Willow Ave", "Wyatt St", "York Ave", "Yates St", "Zane Ave", "2nd St", "6th St", "10th St",
         "11th St", "13th St", "15th St", "17th St", "20th St", "23rd St", "24th St", "25th St", "26th St", "27th St",
         "28th St", "29th St", "31st St", "32nd St", "33rd St", "34th St", "35th St", "36th St", "38th St", "40th St",
         "42nd St", "44th St", "46th St", "48th St", "50th St"]
STOP_EVERY = 2.1                          # scheduled minutes between stops, roughly
INVENTORY_DATE = dt.date(2026, 7, 10)     # Facilities' extract
CUTOFF = dt.date(2026, 6, 30)             # the date the shelter ask is about
# the spring timetable's far-side moves on each route (outbound stops between timepoints) and the stops it closed
MOVES = {"2": 4, "4": 3, "17": 4, "6": 3, "9": 3, "11": 2, "14": 3, "22": 3, "31": 3, "40": 4, "51": 2, "3": 2,
         "12": 1, "60": 1}
CLOSED = {"3": 1, "12": 1, "60": 1, "2": 1, "40": 1, "17": 1}


def rng(k):
    return np.random.default_rng([W.SEED, 300, k])


def latlon(x, y):
    return (round(LAT0 + y / 111320.0, 6), round(LON0 + x / (111320.0 * math.cos(math.radians(LAT0))), 6))


def metres(a, b):
    """Distance in metres between two (lat, lon) points."""
    dy = (a[0] - b[0]) * 111320.0
    dx = (a[1] - b[1]) * 111320.0 * math.cos(math.radians(LAT0))
    return math.hypot(dx, dy)


def _street(name):
    return name.split(" & ")[0] if " & " in name and "(" not in name else None


def _timepoints():
    import gtfs as G
    return {r: G.pattern_stops(r) for r in W.SCHED}


def _place_timepoints(tps):
    """Positions in metres of every timepoint name: the transfer points fixed, the rest along each route's bearing
    from the nearest placed stop, shared names placed once."""
    fixed = {W.STOPS[k][3]: POS[k] for k in POS}
    placed = dict(fixed)
    order = sorted(W.SCHED, key=lambda r: (W.OFFSET[r] == 0 and r != "11", int(r)))
    for r in order:
        pat = tps[r]
        b = BEARING[r]
        if b is None:                       # the University Connector runs from Union Station to the campus
            cx, cy = POS["C"]
            dx, dy = POS["D"][0] - cx, POS["D"][1] - cy
            b = math.degrees(math.atan2(dy, dx))
        ux, uy = math.cos(math.radians(b)), math.sin(math.radians(b))
        known = [i for i, (nm, _) in enumerate(pat) if nm in placed]
        assert known, r
        for i, (nm, mm) in enumerate(pat):
            if nm in placed:
                continue
            after = [k for k in known if k < i]
            before = [k for k in known if k > i]
            if after and before:
                a, c = after[-1], before[0]
                pa, pc = placed[pat[a][0]], placed[pat[c][0]]
                f = (mm - pat[a][1]) / float(pat[c][1] - pat[a][1])
                placed[nm] = (pa[0] + f * (pc[0] - pa[0]) + 60, pa[1] + f * (pc[1] - pa[1]) - 40)
            elif after:
                a = after[-1]
                pa = placed[pat[a][0]]
                d = SPEED * (mm - pat[a][1])
                placed[nm] = (pa[0] + ux * d, pa[1] + uy * d)
            else:
                c = before[0]
                pc = placed[pat[c][0]]
                d = SPEED * (pat[c][1] - mm)
                placed[nm] = (pc[0] - uy * d * 0.3 - ux * d, pc[1] + ux * d * 0.3 - uy * d)
            known = sorted(known + [i])
    return placed


def network():
    """The stops and the patterns. Returns dict(stops, outbound, inbound): stops[key] = dict(code, jan, apr, name,
    route, kind, pos_jan, pos_apr) (a position is (lat, lon), None where the feed does not hold the stop);
    outbound[fd][route] and inbound[fd][route] = [(key, minutes from the trip's first stop, timepoint)]."""
    if "_NET" in globals():
        return globals()["_NET"]
    import gtfs as G
    tps = _timepoints()
    xy = _place_timepoints(tps)
    stops = {}
    for k, c, j, a, nm in G.stop_table():
        if k in POS:
            p = latlon(*POS[k])
        elif k.endswith("o") and k[:-1] in POS:
            x, y = POS[k[:-1]]
            p = latlon(x + 14.0, y - 9.0)
        else:
            p = latlon(*xy[nm])
        stops[k] = dict(code=c, jan=j, apr=a, name=nm, route=None, kind="transfer" if k[0] in POS and len(k) <= 2
                        else "timepoint", pos_jan=p, pos_apr=p)
    by_name = {v["name"]: k for k, v in stops.items()}
    used_codes = {v["code"] for v in stops.values()}
    r_codes = rng(1)
    pool = [c for c in range(5004, 8996) if "%04d" % c not in used_codes]
    pool = list(r_codes.permutation(pool))
    seq = 0
    outbound = {"2601": {}, "2604": {}}
    inbound = {"2601": {}, "2604": {}}
    r_names = rng(2)
    r_jit = rng(3)
    for r in sorted(W.SCHED, key=int):
        pat = tps[r]
        crosses = [c_ for c_ in r_names.permutation(CROSS) if c_.split()[0] not in MAIN_STREET[r]]
        seen_names = set(by_name)
        out = []
        for i, (nm, mm) in enumerate(pat):
            tp = i in (0, len(pat) - 1) or (W.OFFSET[r] > 0 and mm == W.OFFSET[r])
            out.append((by_name[nm], mm, "1" if tp else "0"))
            if i + 1 == len(pat):
                break
            nm2, mm2 = pat[i + 1]
            gap = mm2 - mm
            k = max(0, int(round(gap / STOP_EVERY)) - 1)
            st = _street(nm) if by_name[nm] not in POS else None
            st = st or (_street(nm2) if by_name[nm2] not in POS else None) or MAIN_STREET[r]
            pa, pb = xy[nm], xy[nm2]
            dx, dy = pb[0] - pa[0], pb[1] - pa[1]
            ln = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / ln, dx / ln
            for j in range(k):
                f = (j + 1) / float(k + 1)
                m_ = int(round(mm + f * gap))
                m_ = min(max(m_, mm), mm2)
                cross = crosses.pop(0)
                while "%s & %s" % (st, cross) in seen_names:
                    cross = crosses.pop(0)
                name = "%s & %s" % (st, cross)
                seen_names.add(name)
                jt = float(r_jit.normal(0, 4.0))
                x, y = pa[0] + f * dx + nx * jt, pa[1] + f * dy + ny * jt
                code = "%04d" % pool[seq]
                twin = "%04d" % pool[seq + 1]
                key = "s%s" % code
                tkey = "s%s" % twin
                stops[key] = dict(code=code, jan="%d" % (int(code) * 10 + 7), apr="%d" % (8000 + seq), name=name,
                                  route=r, kind="outbound", pos_jan=latlon(x, y), pos_apr=latlon(x, y),
                                  seg=(dx / ln, dy / ln), twin=tkey)
                stops[tkey] = dict(code=twin, jan="%d" % (int(twin) * 10 + 7), apr="%d" % (8001 + seq), name=name,
                                   route=r, kind="inbound", pos_jan=latlon(x - nx * 16.0, y - ny * 16.0),
                                   pos_apr=latlon(x - nx * 16.0, y - ny * 16.0), twin=key)
                seq += 2
                out.append((key, m_, "0"))
        # the spring timetable: far-side moves and closed stops on the route's own stops
        mid = [kk for kk, _, _ in out if stops[kk]["kind"] == "outbound"]
        rr = rng(10 + int(r))
        pick = list(rr.permutation(mid))
        closed = set(pick[:CLOSED.get(r, 0)])
        moved = pick[CLOSED.get(r, 0):CLOSED.get(r, 0) + MOVES.get(r, 0)]
        for kk in moved:
            s = stops[kk]
            ux_, uy_ = s["seg"]
            d = float(rr.uniform(58, 112))
            y0 = (s["pos_jan"][0] - LAT0) * 111320.0
            x0 = (s["pos_jan"][1] - LON0) * 111320.0 * math.cos(math.radians(LAT0))
            s["pos_apr"] = latlon(x0 + ux_ * d, y0 + uy_ * d)
            s["moved"] = True
        for kk in closed:
            for k3 in (kk, stops[kk]["twin"]):
                stops[k3]["pos_apr"] = None
                stops[k3]["closed"] = True
        outbound["2601"][r] = out
        outbound["2604"][r] = [o for o in out if o[0] not in closed]
        for fd in ("2601", "2604"):
            inv = []
            for kk, mm, tp in reversed(outbound[fd][r]):
                s = stops[kk]
                if s["kind"] == "outbound":
                    k2 = s["twin"]
                elif kk in POS:
                    k2 = kk + "o"
                else:
                    k2 = kk
                inv.append((k2, W.RUN_MIN[r] - mm, "0"))
            inv = [(k2, mm, "1" if i in (0, len(inv) - 1) else "0") for i, (k2, mm, _) in enumerate(inv)]
            inbound[fd][r] = inv
    codes = [v["code"] for v in stops.values()]
    assert len(codes) == len(set(codes))
    assert len({v["jan"] for v in stops.values()}) == len(stops) and len({v["apr"] for v in stops.values()}) == len(stops)
    net = dict(stops=stops, outbound=outbound, inbound=inbound)
    globals()["_NET"] = net
    return net


def serving(net, fd):
    """Routes serving each stop key in a feed (either direction)."""
    out = {}
    for d in ("outbound", "inbound"):
        for r, pat in net[d][fd].items():
            for kk, _, _ in pat:
                out.setdefault(kk, set()).add(r)
    return out


# ---------------------------------------------------------------- shelters: the world, the inventory, the work orders
def _bday(r, a, b):
    """A random weekday between two dates."""
    while True:
        d = a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))
        if d.weekday() < 5:
            return d


def shelters():
    """Shelter history for every stop key and the records it leaves. Returns dict(wo, inv, truth, roles):
    wo: work orders [dict(wo, code, key, work, status, issued, completed)]; inv: {key: dict(date, pos, shelter, bench,
    sign, routes, in_service)}; truth[key] = shelter at the stop's spring position on CUTOFF; roles[key] = the
    moved stops' role."""
    if "_SH" in globals():
        return globals()["_SH"]
    net = network()
    st = net["stops"]
    r = rng(40)
    move_day = W.TIMETABLE_CHANGE
    s0 = {}
    for k in sorted(st):
        v = st[k]
        if v["kind"] == "transfer" or k.endswith("o"):
            p = 1.0
        elif v["kind"] == "timepoint":
            p = 0.65
        elif v["kind"] == "outbound":
            p = 0.36
        else:
            p = 0.30
        s0[k] = bool(r.random() < p)
    # roles of the moved stops: the shelter left at the old pad (with or without a relocation still to come), the
    # shelter relocated by a work order before the cutoff, the stop inspected again after the move, no shelter to move
    roles = {}
    for rt in sorted(W.SCHED, key=int):
        mv = sorted([k for k, v in st.items() if v.get("moved") and v["route"] == rt], key=lambda k: st[k]["code"])
        rr = rng(60 + int(rt))
        order = list(rr.permutation(mv))
        for i, k in enumerate(order):
            if i == 0 and rt in W.CANDIDATES:
                roles[k] = "left"
            else:
                roles[k] = ["left", "relocated", "reinspected", "none", "left_sched", "reloc_july"][
                    int(rr.integers(0, 6))]
            if roles[k] in ("left", "relocated", "left_sched", "reloc_july"):
                s0[k] = True
            if roles[k] == "none":
                s0[k] = False
    inspected = {}
    for k in sorted(st):
        inspected[k] = _bday(r, dt.date(2025, 7, 14), dt.date(2026, 7, 9))
    for k, role in roles.items():
        rr = rng(80 + int(st[k]["code"]))
        if role in ("left", "relocated", "left_sched", "reloc_july"):
            inspected[k] = _bday(rr, dt.date(2025, 7, 14), dt.date(2026, 3, 27))
        elif role == "reinspected":
            inspected[k] = _bday(rr, dt.date(2026, 4, 13), dt.date(2026, 7, 9))
    wos = []

    def add(k, work, status, issued, completed=None):
        wos.append(dict(code=st[k]["code"], key=k, work=work, status=status, issued=issued, completed=completed))

    for k, role in sorted(roles.items()):
        rr = rng(120 + int(st[k]["code"]))
        if role == "relocated":
            c = _bday(rr, dt.date(2026, 4, 20), dt.date(2026, 6, 26))
            add(k, "Relocate shelter", "Completed", c - dt.timedelta(days=int(rr.integers(20, 45))), c)
        elif role == "left_sched":
            add(k, "Relocate shelter", "Scheduled", _bday(rr, dt.date(2026, 5, 4), dt.date(2026, 6, 19)))
        elif role == "reloc_july":
            c = _bday(rr, dt.date(2026, 7, 1), dt.date(2026, 7, 8))
            add(k, "Relocate shelter", "Completed", c - dt.timedelta(days=int(rr.integers(20, 45))), c)
    # new shelters and removals across the network, and work that leaves the shelter count alone
    plain = sorted(k for k, v in st.items() if k not in roles and not v.get("closed") and
                   v["kind"] in ("outbound", "inbound", "timepoint"))
    rr = rng(200)
    no_shelter = [k for k in plain if not s0[k]]
    has_shelter = [k for k in plain if s0[k]]
    for k in list(rr.choice(no_shelter, size=26, replace=False)):
        c = _bday(rr, dt.date(2025, 9, 8), dt.date(2026, 7, 9))
        add(k, "Install shelter", "Completed", c - dt.timedelta(days=int(rr.integers(25, 70))), c)
    # two shelters finished in the first week of July at stops Facilities inspected days later
    late = [k for k in no_shelter if st[k]["kind"] == "outbound" and st[k]["route"] in ("4", "22")
            and not any(w["key"] == k for w in wos)]
    for k in list(rr.choice(late, size=2, replace=False)):
        c = _bday(rr, dt.date(2026, 7, 1), dt.date(2026, 7, 3))
        add(k, "Install shelter", "Completed", c - dt.timedelta(days=int(rr.integers(25, 50))), c)
        d_ = c + dt.timedelta(days=int(rr.integers(4, 7)))
        inspected[k] = d_ + dt.timedelta(days=(7 - d_.weekday()) % 7 if d_.weekday() >= 5 else 0)
    for k in list(rr.choice([k for k in no_shelter if not any(w["key"] == k for w in wos)], size=7, replace=False)):
        add(k, "Install shelter", "Scheduled", _bday(rr, dt.date(2026, 5, 1), dt.date(2026, 7, 2)))
    for k in list(rr.choice([k for k in no_shelter if not any(w["key"] == k for w in wos)], size=3, replace=False)):
        add(k, "Install shelter", "Cancelled", _bday(rr, dt.date(2025, 11, 3), dt.date(2026, 3, 13)))
    for k in list(rr.choice(has_shelter, size=5, replace=False)):
        c = _bday(rr, dt.date(2025, 10, 6), dt.date(2026, 6, 12))
        add(k, "Remove shelter", "Completed", c - dt.timedelta(days=int(rr.integers(10, 30))), c)
    for k in sorted(k for k, v in st.items() if v.get("closed") and s0[k]):
        c = _bday(rr, dt.date(2026, 4, 13), dt.date(2026, 5, 29))
        add(k, "Remove shelter", "Completed", c - dt.timedelta(days=int(rr.integers(5, 15))), c)
    for k in list(rr.choice(has_shelter, size=14, replace=False)):
        work = ["Replace glazing", "Repair roof panel", "Replace bench", "Install solar light"][int(rr.integers(0, 4))]
        c = _bday(rr, dt.date(2025, 8, 4), dt.date(2026, 7, 9))
        add(k, work, "Completed", c - dt.timedelta(days=int(rr.integers(7, 30))), c)
    wos.sort(key=lambda w: (w["issued"], w["code"]))
    for i, w in enumerate(wos):
        w["wo"] = "CP-SH-%04d" % (2101 + i * 3 + int(rr.integers(0, 3)))
    # each stop's shelter over time: at the old position, and for a moved stop at the new one from the move
    changes = {}
    for w in wos:
        if w["status"] == "Completed" and w["work"] in ("Install shelter", "Remove shelter", "Relocate shelter"):
            changes.setdefault(w["key"], []).append((w["completed"], w["work"]))

    def state(k, day):
        """(position, shelter) of stop key k on a day."""
        moved = st[k].get("moved") and day >= move_day
        old, new = s0[k], False
        for d, work in sorted(changes.get(k, [])):
            if d > day:
                break
            if work == "Relocate shelter":
                old, new = False, True
            elif work == "Install shelter":
                if st[k].get("moved") and d >= move_day:
                    new = True
                else:
                    old = True
            else:
                if st[k].get("moved") and d >= move_day:
                    new = False
                else:
                    old = False
        if moved:
            return st[k]["pos_apr"], new
        return st[k]["pos_jan"], old

    truth = {k: state(k, CUTOFF)[1] for k in st if st[k]["pos_apr"] is not None}
    served_jan, served_apr = serving(net, "2601"), serving(net, "2604")
    rn = rng(220)
    inv = {}
    for k in sorted(st):
        d = inspected[k]
        pos, sh = state(k, d)
        noise = (float(rn.normal(0, 3.0)), float(rn.normal(0, 3.0)))
        lat = round(pos[0] + noise[1] / 111320.0, 6)
        lon = round(pos[1] + noise[0] / (111320.0 * math.cos(math.radians(LAT0))), 6)
        srv = served_apr if d >= move_day else served_jan
        open_ = not st[k].get("closed") or d < move_day
        bench = sh or bool(rn.random() < 0.25)
        sign = st[k]["kind"] == "transfer" or k.endswith("o") or (sh and st[k]["kind"] == "timepoint" and
                                                                    bool(rn.random() < 0.3))
        inv[k] = dict(date=d, pos=(lat, lon), shelter=sh, bench=bench, sign=sign,
                      routes=sorted(srv.get(k, set()), key=int) if open_ else [], in_service=open_)
    out = dict(wo=wos, inv=inv, truth=truth, roles=roles, s0=s0, state=state)
    globals()["_SH"] = out
    return out


def outbound_codes(fd="2604"):
    """Each route's outbound stop keys in a feed."""
    net = network()
    return {r: [k for k, _, _ in pat] for r, pat in net["outbound"][fd].items()}


def no_shelter_counts():
    """The golden: for each candidate, its spring outbound stops with no shelter on the cutoff."""
    sh = shelters()
    ob = outbound_codes()
    return {r: sum(1 for k in ob[r] if not sh["truth"][k]) for r in W.CANDIDATES}
