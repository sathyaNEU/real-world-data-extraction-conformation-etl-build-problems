"""The asks' operational records, cut from the world: the TMS stop export and the stores' goods-in receipts (ask A),
the workforce system's paid hours with the clocking punches and the terminal register (ask B), and the two bus
operators' GTFS feeds (ask C). Each part also returns its truth, which the generator's checks hold the pack's answers
to."""
import datetime as dt
import math
import zoneinfo

import numpy as np

import geo
import params as P

LONDON = zoneinfo.ZoneInfo("Europe/London")
UTC = dt.timezone.utc


def local_to_utc(t):
    return t.replace(tzinfo=LONDON).astimezone(UTC).replace(tzinfo=None)


def utc_to_local(t):
    return t.replace(tzinfo=UTC).astimezone(LONDON).replace(tzinfo=None)


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


# ----------------------------------------------------------------- ask A: deliveries from the DC
PAIRS = [("103", "110"), ("104", "109"), ("107", "108"), ("102", "106"), ("101", "105"), ("108", "104"),
         ("110", "102"), ("105", "101"), ("106", "103"), ("109", "107")]
HANDHELD = {"103": dt.date(2025, 10, 20), "101": dt.date(2025, 11, 3), "102": dt.date(2025, 12, 1),
            "104": dt.date(2026, 1, 12), "105": dt.date(2026, 2, 2), "106": dt.date(2026, 3, 2)}
CAP = 1450          # cases a trailer carries
DOW = np.array([0.95, 0.95, 1.0, 1.1, 1.22, 1.05, 0.73])
PROMO = (48, 64, 72, 96, 120)     # a promotion top-up, in cases


def _season(d):
    if dt.date(2025, 12, 15) <= d <= dt.date(2025, 12, 23):
        return 1.32
    if d in (dt.date(2025, 12, 24), dt.date(2025, 12, 31)):
        return 1.10
    if d in (dt.date(2025, 12, 26), dt.date(2026, 1, 1)):
        return 0.55
    if dt.date(2026, 1, 2) <= d <= dt.date(2026, 1, 11):
        return 0.86
    return 1.0


def deliveries(T):
    """the stores' deliveries, day by day, then combined into trips"""
    rs = np.random.default_rng(P.OPS_SEED)
    own = {s["id"]: s for s in T["stores"] if s["kind"] == "own"}
    case_value = {sid: float(rs.uniform(22.0, 25.5)) for sid in sorted(own)}
    k_of = {s["id"]: k for k, s in enumerate(T["stores"])}
    weekly = {sid: T["res"][k_of[sid]] * (1 + T["eps"][sid]) * (1 + P.VFR) / 52.0 / case_value[sid] for sid in own}
    norm = DOW.sum() / 7.0
    days = list(daterange(P.TMS_FROM - dt.timedelta(days=2), P.TMS_TO + dt.timedelta(days=2)))
    dels = []          # (date, store, cases)
    for d in days:
        if d == dt.date(2025, 12, 25):
            continue
        for sid in sorted(own):
            daily = weekly[sid] / 7.0 * DOW[d.weekday()] / norm * _season(d) * rs.normal(1, 0.06)
            fresh = daily * float(rs.uniform(0.34, 0.44))
            for part in (daily - fresh, fresh):
                n = max(1, int(math.ceil(part / (CAP * 0.93))))
                for x in rs.dirichlet(np.full(n, 6.0)):
                    dels.append([d, sid, int(round(part * x))])
    trips = []
    by_day = {}
    for d, sid, c in dels:
        by_day.setdefault(d, {}).setdefault(sid, []).append(c)
    for d in sorted(by_day):
        pool = {sid: sorted(v) for sid, v in by_day[d].items()}
        for a, b in PAIRS:
            if a in pool and b in pool and pool[a] and pool[b] and rs.uniform() < 0.62:
                ca, cb = pool[a][0], pool[b][0]
                if ca + cb <= CAP:
                    pool[a].pop(0); pool[b].pop(0)
                    trips.append([d, [(a, ca), (b, cb)] if rs.uniform() < .5 else [(b, cb), (a, ca)]])
        for sid in sorted(pool):
            for c in pool[sid]:
                trips.append([d, [(sid, c)]])
    trips.sort(key=lambda t: (t[0], t[1][0][0], t[1][0][1]))
    return trips, case_value, weekly


def _travel_min(a, b):
    return 60.0 * P.ROADF * math.hypot(a[0] - b[0], a[1] - b[1]) / 46.0 + 9


def _dwell(rs, c):
    return float(rs.uniform(28, 55)) * (0.5 + c / CAP)


def tms(T, G):
    """the TMS stop export, the handheld receipts and the cases each store was delivered. A store sometimes turns a
    night delivery away (no goods-in team, a late arrival, a chilled load out of temperature): the driver closes the
    stop and takes the load back, and the DC sends it again the next day on a trip of its own"""
    rs = np.random.default_rng(P.OPS_SEED + 1)
    trips, case_value, weekly = deliveries(T)
    own = {s["id"]: (s["x"], s["y"]) for s in T["stores"] if s["kind"] == "own"}
    dc = (P.DC[1], P.DC[2])
    trailers = ["T%03d" % n for n in (104, 107, 111, 112, 118, 121, 123, 126, 130, 131, 134, 139, 142, 147, 150, 153)]
    # the turned-away deliveries: one to three a store, on night trips its handheld receipts do not cover
    rr = np.random.default_rng(P.OPS_SEED + 5)
    at = {}
    for ti, (d, stops) in enumerate(trips):
        for j, (sid, c) in enumerate(stops):
            at.setdefault((sid, d), []).append((ti, j, c))
    refused = set()
    for sid in sorted(own):
        cover = HANDHELD.get(sid)
        days = [d for d in daterange(P.TMS_FROM + dt.timedelta(days=2), P.TMS_TO - dt.timedelta(days=3))
                if (cover is None or d < cover - dt.timedelta(days=1)) and (sid, d) in at
                and not (dt.date(2025, 12, 22) <= d <= dt.date(2025, 12, 28))]
        k = 1 if len(days) < 30 else int(rr.integers(2, 4))
        got = 0
        for p in rr.permutation(len(days)):
            big = max(at[(sid, days[int(p)])], key=lambda x: x[2])
            if big[2] >= 250:
                refused.add(big[:2])
                got += 1
            if got == k:
                break
    rows, recs, truth = [], [], {}
    again, seq = [], 0

    def receipt(sid, arrive_local, trailer, c):
        if sid in HANDHELD and HANDHELD[sid] <= arrive_local.date() <= P.TMS_TO:
            recs.append([sid, arrive_local + dt.timedelta(minutes=int(rs.integers(6, 25))), trailer, c])

    def count(sid, arrive_local, c):
        if P.TMS_FROM <= arrive_local.date() <= P.TMS_TO:
            truth[sid] = truth.get(sid, 0) + c

    for ti, (d, stops) in enumerate(trips):
        seq += 1
        trip_id = "%s%04d" % (d.strftime("%y%m%d"), seq % 10000)
        # night and early-morning slots, local time; some trips the evening before
        start = dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(minutes=int(rs.choice(
            [-210, -150, -90, -30, 30, 90, 150, 210, 270, 330, 390, 450, 600, 720, 840])) + int(rs.integers(0, 50)))
        for bound in (dt.datetime.combine(P.TMS_FROM, dt.time(0, 0)),
                      dt.datetime.combine(P.TMS_TO + dt.timedelta(days=1), dt.time(0, 0))):
            if bound - dt.timedelta(hours=4) <= start <= bound + dt.timedelta(hours=2):
                start = bound + dt.timedelta(hours=2, minutes=int(rs.integers(5, 50)))
        # the trip runs on the system's clock, UTC
        t, here = local_to_utc(start), dc
        trailer = trailers[int(rs.integers(0, len(trailers)))]
        depart_dc = t
        for j, (sid, c) in enumerate(stops):
            t = t + dt.timedelta(minutes=_travel_min(here, own[sid]) + float(rs.uniform(-4, 9)))
            arrive = t
            arrive_local = utc_to_local(arrive)
            turned = (ti, j) in refused
            t = t + dt.timedelta(minutes=float(rs.uniform(3, 7)) if turned else _dwell(rs, c))
            rows.append([trip_id, trailer, depart_dc, j + 1, sid, arrive, t, "DEL", "COMPLETE", c,
                         int(math.ceil(c / 55.0))])
            if turned:
                again.append((arrive_local.date() + dt.timedelta(days=1), sid, c))
            else:
                count(sid, arrive_local, c)
                receipt(sid, arrive_local, trailer, c)
            here = own[sid]
    # the turned-away loads go out again the next day, each on a trip of its own; and the promotion top-ups, a few
    # pallets on consecutive days, on daytime trips
    tp = np.random.default_rng(P.OPS_SEED + 6)
    extra = [(d2, sid, c, 510 + int(tp.integers(0, 240))) for d2, sid, c in again]
    for sid in sorted(own):
        for _ in range(int(tp.integers(2, 4))):
            d0 = P.TMS_FROM + dt.timedelta(days=int(tp.integers(4, 168)))
            if dt.date(2025, 12, 20) <= d0 <= dt.date(2025, 12, 29):
                d0 += dt.timedelta(days=14)
            c = int(PROMO[int(tp.integers(0, len(PROMO)))])
            for k in range(2):
                extra.append((d0 + dt.timedelta(days=k), sid, c, 600 + int(tp.integers(0, 270))))
    for d2, sid, c, minute in sorted(extra):
        seq += 1
        start = local_to_utc(dt.datetime.combine(d2, dt.time(0, 0)) + dt.timedelta(minutes=minute))
        arr = start + dt.timedelta(minutes=_travel_min(dc, own[sid]) + float(tp.uniform(-4, 9)))
        dw = _dwell(tp, c) if c >= 250 else float(tp.uniform(9, 16))
        trailer = trailers[int(tp.integers(0, len(trailers)))]
        rows.append(["%s%04d" % (d2.strftime("%y%m%d"), seq % 10000), trailer, start, 1, sid, arr,
                     arr + dt.timedelta(minutes=dw), "DEL", "COMPLETE", c, int(math.ceil(c / 55.0))])
        count(sid, utc_to_local(arr), c)
        receipt(sid, utc_to_local(arr), trailer, c)
    # backhaul collections: cages and recyclables back to the DC, nothing delivered
    for k in range(int(len(trips) * 0.07)):
        d = trips[int(rs.integers(0, len(trips)))][0]
        sid = sorted(own)[int(rs.integers(0, len(own)))]
        seq += 1
        start = local_to_utc(dt.datetime.combine(d, dt.time(int(rs.integers(9, 16)), int(rs.integers(0, 60)))))
        arr = start + dt.timedelta(minutes=_travel_min(dc, own[sid]))
        rows.append(["%s%04d" % (d.strftime("%y%m%d"), seq % 10000), trailers[int(rs.integers(0, len(trailers)))],
                     start, 1, sid, arr, arr + dt.timedelta(minutes=25), "COL", "COMPLETE", 0, 0])
    # export window: trips leaving the DC from the go-live
    lo = local_to_utc(dt.datetime.combine(P.TMS_FROM, dt.time(0, 0))) - dt.timedelta(hours=8)
    hi = local_to_utc(dt.datetime.combine(P.TMS_TO + dt.timedelta(days=1), dt.time(0, 0))) + dt.timedelta(hours=6)
    rows = [r for r in rows if lo <= r[2] <= hi]
    rows.sort(key=lambda r: (r[2], r[0], r[3]))
    # the TMS numbers a trip when it is planned, in the order trips leave the DC
    renum, n = {}, 100
    for r in rows:
        if r[0] not in renum:
            n += 1
            renum[r[0]] = r[0][:6] + "%04d" % (n % 10000)
        r[0] = renum[r[0]]
    recs = [r for r in recs if r[1].date() >= P.TMS_FROM and r[1] <= dt.datetime.combine(P.TMS_TO, dt.time(23, 59))]
    recs.sort(key=lambda r: (r[1], r[0]))
    # receipt and delivery-note numbers: the stores' handhelds and the WMS keep their own sequences
    out_recs, rn, dn = [], {sid: 4100 + 1000 * i for i, sid in enumerate(sorted(HANDHELD))}, 7731000
    for r in recs:
        rn[r[0]] += int(rs.integers(1, 3))
        dn += int(rs.integers(1, 40))
        out_recs.append(["GR%s-%05d" % (r[0], rn[r[0]]), r[0], r[1], r[2], "DN%d" % dn, r[3]])
    return rows, out_recs, dict(cases=truth, weekly=weekly, case_value=case_value, refused=len(refused),
                                turned=sorted(again))


# ----------------------------------------------------------------- ask B: paid hours
XS_SEED = P.OPS_SEED + 14         # second shifts and forgotten punches
STAFF = {"101": 86, "102": 72, "103": 68, "104": 70, "105": 58, "106": 61, "107": 57, "108": 47, "109": 41, "110": 39}
RELIEF = 9                      # the region's relief team, on store 101's location
CONTRACTS = [37.5, 30, 24, 20, 16, 12, 8]
CONTRACT_P = [.20, .12, .12, .17, .18, .13, .08]
PATTERN = {37.5: (5, 8.0), 30: (4, 8.0), 24: (4, 6.5), 20: (4, 5.0), 16: (4, 4.0), 12: (3, 4.0), 8: (2, 4.0)}


def _paid(start, end):
    """paid hours: the elapsed time, less a 30-minute unpaid break on a shift of six hours or more"""
    a = start.replace(tzinfo=LONDON).astimezone(UTC)
    b = end.replace(tzinfo=LONDON).astimezone(UTC)
    h = (b - a).total_seconds() / 3600.0
    return h - (0.5 if h >= 6 else 0.0), (30 if h >= 6 else 0)


def staffing(T):
    """the workforce system's paid hours report by colleague and date, the clocking terminals' punches and the
    terminal register. Each line carries the colleague's location; relief colleagues, cover shifts and colleagues who
    moved store work shifts at other stores, and only the terminal they clock on at says where"""
    rs = np.random.default_rng(P.OPS_SEED + 2)
    own = {s["id"]: (s["x"], s["y"]) for s in T["stores"] if s["kind"] == "own"}
    ids = sorted(own)
    near = {s: min((o for o in ids if o != s), key=lambda o: math.hypot(own[o][0] - own[s][0], own[o][1] - own[s][1]))
            for s in ids}
    big = {o[0] for o in P.OWN if o[4] >= 1400}
    opened = {o[0]: o[5] for o in P.OWN}
    nums = list(rs.permutation(np.arange(310, 410)))
    term = {}
    register = []
    ts = np.random.default_rng(P.OPS_SEED + 15)
    for s in ids:
        # the terminals each store has: one at the staff entrance, a second at the warehouse door in the larger
        # stores, a third at the goods-in office in the largest; each fitted when the store opened or replaced since
        doors = ["staff entrance"] + (["warehouse"] if s in big or ts.uniform() < .5 else []) + \
            (["goods in office"] if STAFF[s] >= 68 else [])
        for door in doors:
            yr = int(ts.integers(max(opened[s], 2016), 2025)) if ts.uniform() < .7 else max(opened[s], 2012)
            inst = "%d-%02d-%02d" % (yr, int(ts.integers(1, 13)), int(ts.integers(1, 28)))
            tid = "TA%04d" % int(nums.pop())
            term.setdefault(s, []).append(tid)
            register.append([tid, s, door, inst])
    register.sort()
    emps = []
    eno = 20431
    for s in ids:
        for k in range(STAFF[s]):
            eno += int(rs.integers(1, 30))
            night = k < (max(4, STAFF[s] // 9) if s in big else 3)
            contract = 37.5 if night else float(rs.choice(CONTRACTS, p=CONTRACT_P))
            role = "Night Replenishment" if night else str(rs.choice(
                ["Customer Assistant", "Customer Assistant", "Customer Assistant", "Fresh Food", "Team Leader",
                 "Checkout Supervisor"]))
            emps.append(dict(no="E%06d" % eno, home=s, contract=contract, role=role, night=night, relief=False,
                             move=None))
    for k in range(RELIEF):
        eno += int(rs.integers(1, 30))
        emps.append(dict(no="E%06d" % eno, home="101", contract=37.5, role="Relief Team Leader" if k < 3 else
                         "Relief Colleague", night=False, relief=True, move=None))
    # employee numbers run in the order colleagues were taken on, across the estate
    pool = sorted(e["no"] for e in emps)
    for e, no in zip(emps, np.random.default_rng(P.OPS_SEED + 7).permutation(pool)):
        e["no"] = str(no)
    # colleagues who moved store: the location the workforce system holds is the store they are at now
    movers = [e for e in emps if not e["night"] and not e["relief"]]
    for i in rs.choice(len(movers), size=10, replace=False):
        e = movers[int(i)]
        to = str(rs.choice([o for o in ids if o != e["home"]]))
        e["move"] = (P.TMS_FROM + dt.timedelta(days=int(rs.integers(28, 140))), e["home"])
        e["home"] = to
    weeks = [P.TMS_FROM + dt.timedelta(days=7 * w) for w in range(25)]
    shifts, truth = [], {}
    # the relief team covers by store size, the larger stores more often
    rot = [s for s in ids for _ in range(max(1, STAFF[s] // 20))]
    vs = np.random.default_rng(P.OPS_SEED + 16)
    # a minority of colleagues pick up cover at the neighbouring store; most never do
    cover = {e["no"]: (vs.uniform() < 0.22) for e in emps}
    for e in emps:
        for wi, wk in enumerate(weeks):
            if rs.uniform() < 0.10:
                continue                                  # annual leave
            n, length = PATTERN[e["contract"]]
            if e["night"]:
                days = sorted(rs.choice(5, size=n, replace=False))          # Monday to Friday nights
            else:
                days = sorted(rs.choice(7, size=n, replace=False))
            extra = rs.uniform() < 0.08 and n < 7 and not e["night"]
            if extra:
                days = sorted(set(days) | {int(rs.choice([d for d in range(7) if d not in days]))})
            relief_store = rot[(wi * 3 + int(e["no"][1:]) % 7) % len(rot)] if e["relief"] else None
            for di in days:
                d = wk + dt.timedelta(days=int(di))
                if d == dt.date(2025, 12, 25) or (e["night"] and d == dt.date(2025, 12, 24)) or rs.uniform() < 0.025:
                    continue                              # Christmas Day and the night before it; sickness
                ln = 4.0 if (extra and di == days[-1] and not e["night"]) else length
                if not e["night"] and ln >= 5.0:
                    ln += float(vs.choice([-1.0, -0.5, 0.0, 0.0, 0.0, 0.5, 1.0]))
                if e["night"]:
                    st = dt.datetime.combine(d, dt.time(22, 0))
                elif d.weekday() == 6:
                    st = dt.datetime.combine(d, dt.time(9, 30)) + dt.timedelta(minutes=30 * int(rs.integers(0, 2)))
                    ln = min(ln, 6.5)
                else:
                    latest = 22.5 - ln
                    st = dt.datetime.combine(d, dt.time(6, 0)) + dt.timedelta(
                        minutes=30 * int(rs.integers(0, int((latest - 6.0) * 2) + 1)))
                en = st + dt.timedelta(hours=ln)
                if e["relief"]:
                    worked = relief_store
                elif e["move"] and d < e["move"][0]:
                    worked = e["move"][1]
                elif cover[e["no"]] and vs.uniform() < 0.11:
                    worked = near[e["home"]]
                else:
                    worked = e["home"]
                paid, brk = _paid(st, en)
                shifts.append([e["no"], e["home"], d, st, en, brk, paid, e["role"], worked])
                truth[worked] = truth.get(worked, 0.0) + paid
    shifts.sort(key=lambda r: (r[2], r[3], r[0]))
    # a part-timer's second shift on the same day (an evening cover on a morning shift's day); the clocking terminals
    # record what was worked
    xs = np.random.default_rng(XS_SEED)
    worked_rows = []
    for r in shifts:
        worked_rows.append(r)
        e_part = r[7] in ("Customer Assistant", "Fresh Food") and r[3].hour <= 9 and r[4].hour <= 14 and r[4] > r[3]
        if e_part and xs.uniform() < 0.08:
            st2 = dt.datetime.combine(r[2], dt.time(17, 0)) + dt.timedelta(minutes=30 * int(xs.integers(0, 3)))
            en2 = st2 + dt.timedelta(hours=4)
            paid2, brk2 = _paid(st2, en2)
            worked_rows.append([r[0], r[1], r[2], st2, en2, brk2, paid2, r[7], r[8]])
    truth = {}
    for r in worked_rows:
        truth[r[8]] = truth.get(r[8], 0.0) + r[6]
    # the workforce system's paid hours report: one line per colleague, date and shift, built by joining each shift to
    # the calendar dates it covers, so a night shift is listed against the date it starts and again against the date
    # it ends, each line carrying the shift's paid hours
    lines, night_lines = [], 0
    for r in worked_rows:
        lines.append([r[0], r[1], r[2], r[7], r[6]])
        if r[4].date() > r[2]:
            lines.append([r[0], r[1], r[4].date(), r[7], r[6]])
            night_lines += 1
    lines.sort(key=lambda x: (x[2], x[1], x[0]))
    punches = []
    two = {}
    for r in worked_rows:
        two[(r[0], r[2])] = two.get((r[0], r[2]), 0) + 1
    made = []
    for r in worked_rows:
        tl = term[r[8]]
        tid = tl[0] if (len(tl) == 1 or rs.uniform() < 0.8) else tl[1 + int(rs.integers(0, len(tl) - 1))]
        p_in = [r[0], tid, r[3] - dt.timedelta(minutes=int(rs.integers(1, 13))), "IN"]
        tid2 = tl[0] if (len(tl) == 1 or rs.uniform() < 0.8) else tl[1 + int(rs.integers(0, len(tl) - 1))]
        p_out = [r[0], tid2, r[4] + dt.timedelta(minutes=int(rs.integers(0, 10))), "OUT"]
        made.append((r, p_in, p_out, xs.uniform()))
    # a forgotten clock-in or clock-out, confirmed by the manager: only on a day shift that is the colleague's one shift
    # that day, and never on the colleague's shift after another with a forgotten punch
    order = {}
    for i, (r, _, _, _) in enumerate(made):
        order.setdefault(r[0], []).append(i)
    drop = {}
    for e, idx in order.items():
        idx.sort(key=lambda i: made[i][0][3])
        before = False
        for i in idx:
            r, _, _, miss = made[i]
            lone = two[(r[0], r[2])] == 1 and r[4].date() == r[2]
            want = "IN" if (lone and miss < 0.006) else ("OUT" if (lone and miss < 0.016) else None)
            if want and not before:
                drop[i] = want
                before = True
            else:
                before = False
    for i, (r, p_in, p_out, miss) in enumerate(made):
        if drop.get(i) == "IN":
            punches.append(p_out)
        elif drop.get(i) == "OUT":
            punches.append(p_in)
        else:
            punches += [p_in, p_out]
    punches.sort(key=lambda p: (p[2], p[0], p[3]))
    return lines, punches, register, dict(hours=truth, weeks=25, night_lines=night_lines,
                                         split=len(worked_rows) - len(shifts))


# ----------------------------------------------------------------- ask C: buses
def _site_xy():
    return {s[0]: (s[3], s[4]) for s in P.SITES}


ROUTES = [  # number, operator, joint, waypoints (km), weekday service: (first, last, headway minutes), stop spacing km
    ("4", "LB", True, [(12.0, 14.2), (15.85, 16.9), (16.2, 24.0), (30.0, 23.4), (36.0, 22.1), (38.8, 22.8),
                       (40.0, 12.2), (56.8, 13.3), (60.0, 12.0)], (6 * 60 + 30, 22 * 60 + 30, 30), 0.55),
    ("41", "PDC", True, [(17.7, 33.1), (21.8, 33.2), (22.0, 30.0), (30.0, 25.0), (36.0, 22.1), (39.2, 22.3),
                         (50.05, 28.48), (44.0, 38.0), (65.7, 41.6), (66.0, 42.0), (68.5, 43.6)],
     (6 * 60 + 45, 21 * 60 + 45, 60), 0.6),
    ("7", "LB", False, [(36.0, 22.1), (38.7, 22.7), (37.6, 24.6), (34.8, 24.0), (34.2, 21.2), (36.0, 22.1)],
     (7 * 60, 19 * 60, 20), 0.45),
    ("12", "LB", False, [(22.0, 30.0), (22.2, 32.8), (14.0, 36.0), (6.0, 40.0)], (7 * 60 + 10, 19 * 60 + 10, 60), 0.7),
    ("15", "LB", False, [(36.0, 22.1), (28.0, 8.0), (40.0, 12.2)], (7 * 60 + 5, 18 * 60 + 5, 60), 0.8),
    ("22", "PDC", False, [(50.0, 28.3), (50.4, 28.8), (57.2, 12.8), (60.0, 12.0), (54.0, 4.0)],
     (7 * 60 + 20, 17 * 60 + 20, 120), 0.8),
    ("9", "PDC", False, [(66.0, 42.0), (66.3, 41.6), (44.0, 38.0)], (8 * 60 + 5, 17 * 60 + 5, 120), 0.9),
]
ROUTE_ORDER = {"4": 0, "41": 1, "7": 2, "12": 3, "15": 4, "22": 5, "9": 6, "S41": 7}
SCHOOL = ("S41", "PDC", [(66.0, 42.0), (66.2, 41.9), (44.0, 38.0)], [(7 * 60 + 40,), (15 * 60 + 35,)], 0.9)
# the two inter-town routes' late journeys, service-day minutes from midnight: one a direction Monday to Thursday,
# two a direction on Friday nights and on Saturday nights
LATE = {"4": {"mtl": [23 * 60], "fl": [23 * 60 + 40, 24 * 60 + 40], "sl": [23 * 60 + 40, 24 * 60 + 40]},
        "41": {"mtl": [22 * 60 + 50], "fl": [23 * 60 + 30, 24 * 60 + 30], "sl": [23 * 60 + 30, 24 * 60 + 30]}}
# where each late route's Friday-late timetable begins in Sallowmere Motor Services' export: its own late journeys and
# the weekday journeys from this time on, so on a Friday those weekday journeys are listed twice, on the same blocks
FL_FROM = {"4": 21 * 60, "41": 20 * 60}
BLOCK_BASE = {"LB": 300, "PDC": 600}


def _along(wps, spacing, rs):
    pts = []
    for (x0, y0), (x1, y1) in zip(wps[:-1], wps[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(round(L / spacing)))
        for i in range(n):
            f = i / n
            pts.append((x0 + f * (x1 - x0) + rs.normal(0, .03), y0 + f * (y1 - y0) + rs.normal(0, .03)))
    pts.append(wps[-1])
    return pts


def buses(T):
    rs = np.random.default_rng(P.OPS_SEED + 3)
    sites = _site_xy()
    stops = {}            # key -> (x, y, name)
    patterns = []         # (route, operator, joint, direction, [stop keys], first, last, headway, school)
    names = ["Church", "Market Place", "The Green", "Station Road", "School", "Post Office", "Crossroads", "Bridge",
             "Mill", "Recreation Ground", "Health Centre", "Library", "Fire Station", "Garage", "Farm Lane",
             "Primary School", "Village Hall", "Chapel", "Allotments", "Industrial Estate", "Hospital", "Park"]

    def stop_key(x, y):
        for k, (sx, sy, _) in stops.items():
            if math.hypot(sx - x, sy - y) < 0.12:
                return k
        k = "S%03d" % (len(stops) + 1)
        stops[k] = (x, y, names[len(stops) % len(names)])
        return k
    for num, op, joint, wps, svc, spacing in ROUTES:
        pts = _along(wps, spacing, rs)
        # no stop sits in the band 370 to 430 metres from a site
        clean = []
        for (x, y) in pts:
            ok = True
            for sx, sy in sites.values():
                dd = 1000 * math.hypot(x - sx, y - sy)
                if 360 <= dd <= 440:
                    ok = False
            if ok:
                clean.append((x, y))
        # a stop at each site the route passes within 300 metres, at the nearest point of the route
        for sx, sy in sites.values():
            best = None
            for (x0, y0), (x1, y1) in zip(wps[:-1], wps[1:]):
                L2 = (x1 - x0) ** 2 + (y1 - y0) ** 2
                f = 0.0 if L2 == 0 else max(0.0, min(1.0, ((sx - x0) * (x1 - x0) + (sy - y0) * (y1 - y0)) / L2))
                px, py = x0 + f * (x1 - x0), y0 + f * (y1 - y0)
                dd = math.hypot(px - sx, py - sy)
                if best is None or dd < best[0]:
                    best = (dd, px, py)
            if best[0] <= 0.30:
                ins = min(range(len(clean)), key=lambda i: math.hypot(clean[i][0] - best[1], clean[i][1] - best[2]))
                if math.hypot(clean[ins][0] - best[1], clean[ins][1] - best[2]) > 0.12:
                    clean.insert(ins + (1 if ins < len(clean) - 1 else 0), (best[1] + 0.01, best[2] + 0.01))
        # one stop inside 400 metres of a site per route: the nearest
        for sx, sy in sites.values():
            inside = [i for i, (x, y) in enumerate(clean) if 1000 * math.hypot(x - sx, y - sy) <= P.BUS_RADIUS]
            if len(inside) > 1:
                keep = min(inside, key=lambda i: math.hypot(clean[i][0] - sx, clean[i][1] - sy))
                clean = [c for i, c in enumerate(clean) if i not in inside or i == keep]
        keys = [stop_key(x, y) for x, y in clean]
        loop = wps[0] == wps[-1]
        patterns.append((num, op, joint, 0, keys, svc, False))
        if not loop:
            patterns.append((num, op, joint, 1, keys[::-1], svc, False))
    num, op, wps, times, spacing = SCHOOL
    pts = [(x, y) for x, y in _along(wps, spacing, rs)
           if all(not (360 <= 1000 * math.hypot(x - sx, y - sy) <= 440) for sx, sy in sites.values())]
    for sx, sy in sites.values():
        inside = [i for i, (x, y) in enumerate(pts) if 1000 * math.hypot(x - sx, y - sy) <= P.BUS_RADIUS]
        if len(inside) > 1:
            keep = min(inside, key=lambda i: math.hypot(pts[i][0] - sx, pts[i][1] - sy))
            pts = [c for i, c in enumerate(pts) if i not in inside or i == keep]
    keys = [stop_key(x, y) for x, y in pts]
    patterns.append((num, op, False, 0, keys, (times[0][0], times[0][0], 999), True))
    patterns.append((num, op, False, 1, keys[::-1], (times[1][0], times[1][0], 999), True))
    # timetables: weekday, Saturday and Sunday journeys
    def journeys(svc, day, num=None):
        if day in ("mtl", "fl", "sl"):
            return LATE.get(num, {}).get(day, [])
        first, last, hw = svc
        if hw == 999:
            return [first] if day == "wk" else []
        if day == "sat":
            first, hw = first + 30, hw
        if day == "sun":
            first, last, hw = first + 120, min(last, 18 * 60), max(hw * 2, 60)
        out, t = [], first
        while t <= last:
            out.append(t)
            t += hw
        return out
    truth = {k: 0 for k in sites}
    stop_xy = {k: (v[0], v[1]) for k, v in stops.items()}
    near = {sk: {k for k, (x, y) in stop_xy.items() if 1000 * math.hypot(x - sx, y - sy) <= P.BUS_RADIUS}
            for sk, (sx, sy) in sites.items()}
    jn = 0
    dup_done, dups = set(), {k: 0 for k in sites}
    alls = []
    for num, op, joint, direction, keys, svc, school in patterns:
        for day in ("wk", "sat", "sun", "mtl", "fl", "sl"):
            for t0 in journeys(svc, day, num):
                jn += 1
                times, t = [], float(t0)
                prev = stop_xy[keys[0]]
                for k in keys:
                    x, y = stop_xy[k]
                    t += 60 * 1.3 * math.hypot(x - prev[0], y - prev[1]) / 28.0 + 0.4
                    times.append(int(round(t)))
                    prev = (x, y)
                alls.append(dict(num=num, op=op, joint=joint, direction=direction, day=day, school=school, keys=keys,
                                 times=times, jn=jn, t0=t0, duplicate=False))
                # departures on the ask's day, a Friday, by the clock: the weekday journeys whole (the Thursday
                # journeys' calls after midnight replace the Friday ones', the same timetable), the Friday late
                # journeys' calls before midnight and the Monday to Thursday late journeys' calls after it
                for i, (k, m) in enumerate(zip(keys, times)):
                    if i == len(keys) - 1:
                        continue
                    if day == "wk" or (day == "fl" and m < 1440) or (day == "mtl" and m >= 1440):
                        for sk in sites:
                            if k in near[sk]:
                                truth[sk] += 1
                # on school days the lead operator puts a second bus on the joint routes' school-time journeys, on
                # the same timetable: a duplicate, which only its own operator's data carries
                if joint and day == "wk" and (7 * 60 <= t0 < 8 * 60 or 15 * 60 <= t0 < 16 * 60) and \
                        (num, direction, t0 // 480) not in dup_done:
                    dup_done.add((num, direction, t0 // 480))
                    jn += 1
                    alls.append(dict(num=num, op=op, joint=False, direction=direction, day=day, school=True, keys=keys,
                                     times=times, jn=jn, t0=t0, duplicate=True))
                    for i, (k, m) in enumerate(zip(keys, times)):
                        if i < len(keys) - 1:
                            for sk in sites:
                                if k in near[sk]:
                                    truth[sk] += 1
                                    dups[sk] += 1
    # vehicle blocks: each operator's buses work a route's journeys in turn, a bus taking the next journey from where
    # its last one ended after a five-minute stand; the late journeys continue the day's buses (Monday to Thursday,
    # Friday and Saturday duties), a school duplicate and the school route each have a bus of their own
    def chain(js, state=None):
        veh = [list(v) for v in (state or [])]
        for j in sorted(js, key=lambda j: (j["times"][0], j["direction"], j["jn"])):
            free = [v for v in veh if v[1] == j["keys"][0] and v[0] + 5 <= j["times"][0]]
            if free:
                v = min(free, key=lambda v: (v[0], v[2]))
            else:
                v = [None, None, len(veh)]
                veh.append(v)
            j["bno"] = v[2]
            v[0], v[1] = j["times"][-1], j["keys"][-1]
        return veh
    by_route = {}
    for j in alls:
        by_route.setdefault((j["op"], j["num"]), []).append(j)
    bcount = {"LB": 0, "PDC": 0}
    for (op, num), js in sorted(by_route.items(), key=lambda x: (x[0][0], ROUTE_ORDER[x[0][1]])):
        base = BLOCK_BASE[op] + bcount[op]
        reg = [j for j in js if not j["duplicate"]]
        wk = chain([j for j in reg if j["day"] == "wk"])
        chain([j for j in reg if j["day"] == "mtl"], wk)
        chain([j for j in reg if j["day"] == "fl"], wk)
        sat = chain([j for j in reg if j["day"] == "sat"])
        chain([j for j in reg if j["day"] == "sl"], sat)
        chain([j for j in reg if j["day"] == "sun"])
        used = 1 + max(j["bno"] for j in reg)
        for j in reg:
            j["block"] = "%d" % (base + j["bno"])
        for i, j in enumerate(sorted([j for j in js if j["duplicate"]], key=lambda j: (j["t0"], j["direction"]))):
            j["block"] = "%d" % (base + used + i)
        bcount[op] += used + sum(1 for j in js if j["duplicate"]) + 3
    feeds = {"LB": dict(trips=[], stop_times=[]), "PDC": dict(trips=[], stop_times=[])}
    seam = {k: 0 for k in sites}
    for j in alls:
        owners = [j["op"]] + (["LB" if j["op"] == "PDC" else "PDC"] if j["joint"] else [])
        for owner in owners:
            feeds[owner]["trips"].append(dict(j, owner=owner))
        # Sallowmere Motor Services' Friday-late timetable starts with the weekday journeys from FL_FROM on, the same
        # buses on the same blocks, so its data lists those journeys twice on a Friday
        if j["day"] == "wk" and not j["duplicate"] and j["num"] in FL_FROM and j["t0"] >= FL_FROM[j["num"]] and \
                "LB" in owners:
            jn += 1
            feeds["LB"]["trips"].append(dict(j, owner="LB", day="fl", jn=jn, seam=True))
            for i, (k, m) in enumerate(zip(j["keys"], j["times"])):
                if i < len(j["keys"]) - 1 and m < 1440:
                    for sk in sites:
                        if k in near[sk]:
                            seam[sk] += 1
    return feeds, stops, truth, near, dups, seam
