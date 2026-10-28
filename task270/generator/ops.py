"""task270 operations, 2026: on-call crews' availability bookings and the crewing rule that puts each on-call engine on
or off the run, defects and workshop days, the wholetime crews' training mornings and home fire safety visits, the
standby moves into rural on-call stations that are off the run, and the year's incidents, each mobilising the nearest
free engine from wherever it stands. Every engine's year is a timeline of stays and drives in seconds from 00:00 UTC on
1 January 2026; records.py turns the timelines into the status log and the tracking export."""
from __future__ import annotations

import bisect
import datetime as dt

import numpy as np

import common as K
import world as W

M = K.MINUTES
S_YEAR = M * 60
BANK = [dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 4), dt.date(2026, 5, 25),
        dt.date(2026, 8, 31), dt.date(2026, 12, 25), dt.date(2026, 12, 28)]
BANK_DOY = {(d - dt.date(2026, 1, 1)).days for d in BANK}
DOW0 = 3                               # 1 January 2026 is a Thursday

OPS = dict(train_p=0.9, visit_p=0.9, vd_wp=3, vd_th=4, vd_c=2, rural_share=0.75, intown=0.9, v_start=13.0,
           v_end=17.5, sb_from=7.5, sb_to=19.0, sb_min=45, sb_max=2, sb_keep=1, incidents=4900)
# on-call crews: availability propensities by station (weekday day, weekday night, weekend)
CREW = dict(day_lo=0.18, day_hi=0.45, high_day=(0.70, 0.90), n_high=3, night=(0.72, 0.92), weekend=(0.55, 0.85),
            rural_day_boost=0.010, edit_p=0.06, size=(10, 13), quals=1)


def weekday_doy(d):
    return (d + DOW0) % 7 < 5 and d not in BANK_DOY


def lmin(d, h):
    """Minute index (UTC) of local clock time h hours on day-of-year d."""
    m = d * 1440 + int(round(h * 60))
    a, b = K.bst_minutes()
    return m - 60 if a + 60 <= m < b + 60 else m


# ------------------------------------------------------------------------------------------------- on-call crews
class Person:
    pass


def crews(Wd, rng_name="crews"):
    """Each on-call station's firefighters (roles with promotion dates, LGV drivers with qualification dates, BA
    wearers) and their 2026 bookings: the bookings that stood and the ones a later booking replaced."""
    staff = []
    bookings = []           # dict rows: staff, station, from_min_local, to_min_local, entered_min_local, stood
    oc_stations = [i for i, s in enumerate(Wd.stations) if s["duty"] == "On-call"]
    num = 100
    for si in oc_stations:
        s = Wd.stations[si]
        r = K.rng(rng_name, s["code"])
        n = int(r.integers(CREW["size"][0], CREW["size"][1] + 1))
        rural = s["district"] in K.RURAL
        people = []
        for k in range(n):
            p = Person()
            num += int(r.integers(3, 40))
            p.staff = "%05d" % (40000 + num)
            p.station = si
            p.role_hist = [(0, "Firefighter")]
            p.driver_from = None
            p.ba = True
            people.append(p)
        order = r.permutation(n)                              # roles fall where they fall in the staff list
        people[order[0]].role_hist = [(0, "Watch Commander")]
        people[order[1]].role_hist = [(0, "Crew Commander")]
        people[order[2]].role_hist = [(0, "Crew Commander")]
        if r.random() < 0.7:                                  # a promotion part-way through the year
            d = 20 + (int(r.integers(60, 300)) - 60) * 4 // 3
            people[order[3]].role_hist = [(0, "Firefighter"), (d, "Crew Commander")]
        drivers = r.choice(np.arange(n), 5, replace=False)
        for j, k in enumerate(drivers):
            people[k].driver_from = 0 if j < 4 else int(r.integers(40, 320))
        for k in r.choice(order[3:], 1, replace=False):
            people[k].ba = False
        # the LGV drivers and BA wearers each station's crew happens to hold
        rx = K.rng("crew-quals-%d" % CREW["quals"], s["code"])
        d_new = people[drivers[4]].driver_from
        pool = list(drivers[:4]) + [int(k) for k in rx.permutation(n) if k not in drivers[:4]]
        n_pre, new = int(rx.choice([3, 4, 4, 5, 6])), rx.random() < 0.55
        for p in people:
            p.driver_from = None
        for k in pool[:n_pre]:
            people[k].driver_from = 0
        if new:
            people[next(k for k in pool[n_pre:])].driver_from = d_new
        non_ba = [k for k in order[3:] if not people[k].ba]
        for k in [int(x) for x in rx.permutation(order[3:]) if not people[x].ba is False][:int(rx.choice([0, 0, 1, 2]))]:
            people[k].ba = False
        if rx.random() < 0.2:
            people[non_ba[0]].ba = True
        hi = set(r.choice(np.arange(n), CREW["n_high"], replace=False).tolist())
        for k, p in enumerate(people):
            p.p_day = r.uniform(*CREW["high_day"]) if k in hi else r.uniform(CREW["day_lo"], CREW["day_hi"])
            if rural:
                p.p_day = min(0.95, p.p_day + CREW["rural_day_boost"])
            p.p_night = r.uniform(*CREW["night"])
            p.p_we = r.uniform(*CREW["weekend"])
            # annual leave: three blocks of a week
            p.leave = set()
            for _ in range(3):
                d0 = int(r.integers(0, 358))
                p.leave |= set(range(d0, d0 + 7))
        for p in people:
            for d in range(365):
                if d in p.leave:
                    continue
                wk = (d + DOW0) % 7 < 5
                blocks = []
                if wk:
                    if r.random() < p.p_day:
                        kind = r.random()
                        if kind < 0.6:
                            blocks.append((7.0, 18.5))
                        elif kind < 0.8:
                            blocks.append((7.0, 13.0))
                        else:
                            blocks.append((12.5, 18.5))
                    if r.random() < p.p_night:
                        blocks.append((18.5, 31.0))
                else:
                    if r.random() < p.p_we:
                        blocks.append((7.0, 19.0))
                    if r.random() < p.p_we:
                        blocks.append((19.0, 31.0))
                for a, b in blocks:
                    f = d * 1440 + int(a * 60); t = d * 1440 + int(b * 60)
                    ent = f - int(r.integers(1, 8)) * 1440 + int(r.integers(6 * 60, 23 * 60)) - int(a * 60)
                    if r.random() < CREW["edit_p"] and t - f >= 240:
                        # entered first as booked, then replaced before it began by a shorter booking inside it
                        # most re-bookings trim a little off either end, a few a good deal, to the quarter hour
                        span = t - f
                        f2 = f + max(30, int(span * _trim(r.uniform(0.08, 0.35))) // 15 * 15)
                        t2 = t - max(30, int(span * _trim(r.uniform(0.08, 0.35))) // 15 * 15)
                        ent2 = f - int(r.integers(30, 600))
                        if ent2 <= ent + 30:
                            ent2 = ent + 30
                        bookings.append(dict(staff=p.staff, station=si, f=f, t=t, entered=ent, stood=False))
                        bookings.append(dict(staff=p.staff, station=si, f=f2, t=t2, entered=ent2, stood=True))
                    else:
                        bookings.append(dict(staff=p.staff, station=si, f=f, t=t, entered=ent, stood=True))
        staff += people
    # merge each person's standing bookings that abut (a day block ending 18:30 and the night block from 18:30 stay
    # two bookings, as entered)
    return staff, bookings


def _trim(u):
    """The share of a booking a re-booking trims from one end, from a uniform draw on 0.08 to 0.35: small trims
    common, large ones rare."""
    v = (u - 0.08) / 0.27
    return 0.03 + 0.42 * v ** 2.2


def role_at(p, d):
    cur = p.role_hist[0][1]
    for d0, rl in p.role_hist:
        if d >= d0:
            cur = rl
    return cur


def crew_counts(Wd, staff, bookings):
    """Per on-call station, per UTC minute: firefighters booked (standing bookings only), and the crew rule met."""
    a, b = K.bst_minutes()
    by_station = {}
    pers = {p.staff: p for p in staff}
    for si in set(p.station for p in staff):
        by_station[si] = dict(n=np.zeros(M, np.int16), oic=np.zeros(M, np.int16), drv=np.zeros(M, np.int16),
                              ba=np.zeros(M, np.int16))
    for bk in bookings:
        if not bk["stood"]:
            continue
        p = pers[bk["staff"]]
        c = by_station[p.station]
        f, t = bk["f"], bk["t"]
        # local minutes to UTC minutes
        fu = f - 60 if a + 60 <= f < b + 60 else f
        tu = t - 60 if a + 60 <= t < b + 60 else t
        fu, tu = max(0, fu), min(M, tu)
        if tu <= fu:
            continue
        c["n"][fu:tu] += 1
        if p.ba:
            c["ba"][fu:tu] += 1
        if p.driver_from is not None:
            c["drv"][max(fu, p.driver_from * 1440):tu] += 1
        # officer in charge: crew commander or above at the time
        for k, (d0, rl) in enumerate(p.role_hist):
            d1 = p.role_hist[k + 1][0] if k + 1 < len(p.role_hist) else 400
            if rl != "Firefighter":
                lo, hi = max(fu, d0 * 1440), min(tu, d1 * 1440)
                if hi > lo:
                    c["oic"][lo:hi] += 1
    rule = {}
    for si, c in by_station.items():
        rule[si] = (c["n"] >= 4) & (c["oic"] >= 1) & (c["drv"] >= 1) & (c["ba"] >= 2)
    return by_station, rule


# ------------------------------------------------------------------------------------------------- timelines
class Timeline:
    """One engine's year as contiguous segments: ('stay', t0, t1, node, xy, kind) or ('move', t0, t1, path, cum,
    kind, t_start), in seconds; kind 0 home, 1 training, 2 visit, 3 standby, 4 incident (turnout, drive and
    attendance), 5 returning. A move's cum is the drive time to each node of its path from t_start."""

    def __init__(self, e, home, xy):
        self.e = e
        self.home = home
        self.hxy = xy
        self.seg = [("stay", 0, S_YEAR, home, xy, 0)]
        self._st = [0]

    def at(self, t):
        return self.seg[bisect.bisect_right(self._st, t) - 1]

    def index(self, t):
        return bisect.bisect_right(self._st, t) - 1

    def where(self, t, Wd):
        """Node the engine is at or passing at time t, and its point."""
        s = self.at(t)
        if s[0] == "stay":
            return s[3], s[4]
        path, cum = s[3], s[4]
        el = t - s[6]
        k = int(np.searchsorted(cum, el, side="right")) - 1
        k = min(max(k, 0), len(path) - 1)
        if k >= len(path) - 1:
            return path[-1], Wd.nodes[path[-1]]
        fr = (el - cum[k]) / max(cum[k + 1] - cum[k], 1e-9)
        pt = Wd.nodes[path[k]] + fr * (Wd.nodes[path[k + 1]] - Wd.nodes[path[k]])
        return (path[k] if fr < 0.5 else path[k + 1]), pt

    def trip_end(self, t0, t1):
        """End of every away trip (a run of segments that are not at home) overlapping [t0, t1)."""
        i = self.index(t0)
        end = t1
        while i < len(self.seg) and self.seg[i][1] < end:
            s = self.seg[i]
            if s[5] != 0:
                j = i
                while j + 1 < len(self.seg) and self.seg[j + 1][5] != 0:
                    j += 1
                end = max(end, self.seg[j][2])
                i = j + 1
            else:
                i += 1
        return end

    def replace(self, t0, t1, new):
        """Replace whatever the timeline holds in [t0, t1) by the segments in new, which tile [t0, t1)."""
        out = []
        for s in self.seg:
            if s[2] <= t0 or s[1] >= t1:
                out.append(s)
                continue
            if s[1] < t0:
                out.append(_cut(s, s[1], t0))
            if s[2] > t1:
                out.append(_cut(s, t1, s[2]))
        out += new
        out.sort(key=lambda s: s[1])
        self.seg = out
        self._st = [s[1] for s in out]


def _cut(s, a, b):
    if s[0] == "stay":
        return ("stay", a, b, s[3], s[4], s[5])
    return ("move", a, b, s[3], s[4], s[5], s[6])


def drive(Wd, t0, a_node, b_node, kind):
    p = W.path(Wd, a_node, b_node)
    cum = np.r_[0.0, np.cumsum([Wd.D[p[i], p[i + 1]] for i in range(len(p) - 1)])]
    return ("move", t0, t0 + cum[-1], p, cum, kind, t0), t0 + cum[-1]


# ------------------------------------------------------------------------------------------------- the year
def simulate(Wd, ops=None):
    ops = dict(OPS if ops is None else ops)
    staff, bookings = crews(Wd)
    counts, rule = crew_counts(Wd, staff, bookings)
    nE = Wd.nE
    T = [Timeline(e, Wd.home[e], Wd.nodes[Wd.home[e]]) for e in range(nE)]
    st_of = np.array([Wd.engines[e]["station"] for e in range(nE)])
    # base availability by minute: crew rule for on-call engines, defects and workshop days for all
    avail = np.ones((M, nE), bool)
    reason = np.zeros((M, nE), np.int8)       # 0 none, 1 crew, 2 defect, 3 workshop
    for e in range(nE):
        if not Wd.ewt[e]:
            ok = rule[st_of[e]]
            avail[~ok, e] = False
            reason[~ok, e] = 1
        r = K.rng("defects", e)
        d0 = int(r.integers(10, 340))
        for d in range(d0, d0 + int(r.integers(2, 4))):         # annual service days, 08:00 to 17:00 local
            lo, hi = lmin(d, 8.0), lmin(d, 17.0)
            avail[lo:hi, e] = False; reason[lo:hi, e] = 3
        for _ in range(int(r.integers(1, 4))):                    # defects, a few hours
            m0 = int(r.integers(0, M - 600)); m1 = m0 + int(r.integers(90, 420))
            avail[m0:m1, e] = False; reason[m0:m1, e] = 2
    # wholetime plans: training mornings and home fire safety visits
    wt = np.where(Wd.ewt)[0]
    rng = K.rng("plans")
    hd = Wd.adist
    res = Wd.akind == "R"
    intown = np.array([W.in_town(p) for p in Wd.axy])
    tday = dict(zip(wt, [0, 1, 2, 3, 4, 0, 1, 2]))
    area_of = {"Wrenfold": ("Skirwold", ops["vd_wp"]), "Pelmarsh": ("Altmoor", ops["vd_wp"]),
               "Tollesham": (None, ops["vd_th"]), "Hollinbury": (None, ops["vd_th"]),
               "Calderstow": (None, ops["vd_c"]), "Calderstow East": (None, ops["vd_c"])}
    for e in wt:
        s = Wd.stations[st_of[e]]
        area, ndays = area_of[s["name"]]
        di = K.DISTRICTS.index(s["district"])
        others = [d for d in range(5) if d != tday[e]]
        vdays = set(rng.choice(others, ndays, replace=False).tolist())
        own_town = np.where(res & (hd == di) & intown)[0]
        own_vill = np.where(res & (hd == di) & ~intown)[0]
        rural = np.where(res & (hd == K.DISTRICTS.index(area)))[0] if area else None
        for d in range(365):
            if not weekday_doy(d):
                continue
            dw = (d + DOW0) % 7
            if dw == tday[e] and rng.random() < ops["train_p"]:
                t = lmin(d, 9.0) * 60 - 25 * 60
                mv, arr = drive(Wd, t, Wd.home[e], Wd.training_node, 1)
                end = lmin(d, 13.0) * 60
                if arr < end:
                    st = ("stay", arr, end, Wd.training_node, Wd.nodes[Wd.training_node], 1)
                    back, arr2 = drive(Wd, end, Wd.training_node, Wd.home[e], 1)
                    T[e].replace(t, arr2, [mv, st, back])
            elif dw in vdays and rng.random() < ops["visit_p"]:
                t = lmin(d, ops["v_start"]) * 60
                endday = lmin(d, ops["v_end"]) * 60
                cur = Wd.home[e]
                segs = []
                t_cur = t
                for _ in range(6):
                    if area and rng.random() < ops["rural_share"]:
                        o = int(rng.choice(rural))
                    elif not area and rng.random() < ops["intown"]:
                        o = int(rng.choice(own_town))
                    else:
                        o = int(rng.choice(own_vill))
                    mv, arr = drive(Wd, t_cur, cur, Wd.anode[o], 2)
                    stay = int(rng.integers(40, 60)) * 60
                    segs += [mv, ("stay", arr, arr + stay, Wd.anode[o], Wd.axy[o].copy(), 2)]
                    t_cur = arr + stay; cur = Wd.anode[o]
                    if t_cur > endday - 45 * 60:
                        break
                back, arr2 = drive(Wd, t_cur, cur, Wd.home[e], 2)
                segs.append(back)
                T[e].replace(t, arr2, segs)
    # workshop days: the engine is driven to the service's workshops at Brandeth for its annual service and back
    for e in range(nE):
        ws = np.where(reason[:, e] == 3)[0]
        if not len(ws):
            continue
        cuts = np.where(np.diff(ws) > 1)[0]
        for lo, hi in zip(np.r_[ws[0], ws[cuts + 1]], np.r_[ws[cuts], ws[-1]]):
            t0 = int(lo) * 60
            mv, arr = drive(Wd, t0, Wd.home[e], Wd.training_node, 6)
            t1 = (int(hi) + 1) * 60
            if arr >= t1:
                continue
            st = ("stay", arr, t1, Wd.training_node, Wd.nodes[Wd.training_node], 6)
            back, arr2 = drive(Wd, t1, Wd.training_node, Wd.home[e], 6)
            end = T[e].trip_end(t0, arr2)
            new = [mv, st, back]
            if end > arr2:
                new.append(("stay", arr2, end, Wd.home[e], Wd.nodes[Wd.home[e]], 0))
            T[e].replace(t0, end, new)
    # standby moves: a Calderstow engine stands by at a rural on-call station that is off the run for its crew
    cty = [e for e in wt if Wd.stations[st_of[e]]["name"].startswith("Calderstow")]
    rural_oc = [e for e in range(nE) if not Wd.ewt[e] and Wd.stations[st_of[e]]["district"] in K.RURAL]
    sb_until = {}
    for d in range(365):
        if not weekday_doy(d):
            continue
        order = list(rng.permutation(rural_oc))
        m_lo, m_hi = lmin(d, ops["sb_from"]), lmin(d, ops["sb_to"])
        for m in range(m_lo, m_hi - 60, 15):
            t = m * 60
            active = [c for c in cty if sb_until.get(c, -1) > t]
            if len(active) >= ops["sb_max"]:
                continue
            for rr in order:
                if reason[m, rr] != 1:
                    continue
                if any(T[c].at(t)[0] == "stay" and T[c].at(t)[3] == Wd.home[rr] for c in cty):
                    continue
                seg = reason[m:m_hi, rr] != 1
                back_m = m + int(np.argmax(seg)) if seg.any() else m_hi
                if back_m - m < ops["sb_min"]:
                    continue
                home_free = [c for c in cty if T[c].at(t)[0] == "stay" and T[c].at(t)[5] == 0 and avail[m, c]]
                if len(home_free) < ops["sb_keep"] + 1:
                    break
                c = home_free[0]
                mv, arr = drive(Wd, t, Wd.home[c], Wd.home[rr], 3)
                tb = back_m * 60
                if arr >= tb:
                    continue
                st = ("stay", arr, tb, Wd.home[rr], Wd.nodes[Wd.home[rr]], 3)
                back, arr2 = drive(Wd, tb, Wd.home[rr], Wd.home[c], 3)
                T[c].replace(t, arr2, [mv, st, back])
                sb_until[c] = arr2
                break
    # incidents: each mobilises the nearest free engines from where they stand
    inc = incidents_2026(Wd, ops)
    busy_until = np.zeros(nE)
    committed = np.zeros((M, nE), bool)
    log = []
    for I in inc:
        t = I["t"]
        m = min(int(t // 60), M - 1)
        cand = [e for e in range(nE) if avail[m, e] and t >= busy_until[e]]
        if not cand:
            I["sent"] = []
            log.append(I)
            continue
        here = {e: T[e].where(t, Wd) for e in cand}
        resp = np.array([Wd.D[here[e][0], I["node"]] + Wd.turn_s[e] for e in cand])
        order = np.argsort(resp, kind="stable")
        sent = []
        for k in order[:I["engines"]]:
            e = cand[k]
            node0, pt0 = here[e]
            cur = T[e].at(t)
            t_go = t + Wd.turn_s[e]
            hold = ("stay", t, t_go, node0, (cur[4] if cur[0] == "stay" else pt0), cur[5] if cur[0] == "stay" else 4)
            mv, arr = drive(Wd, t_go, node0, I["node"], 4)
            done = arr + I["dur"][len(sent)]
            st = ("stay", arr, done, I["node"], I["xy"], 4)
            back, arr2 = drive(Wd, done, I["node"], Wd.home[e], 5)
            end = T[e].trip_end(t, arr2)
            new = [hold, mv, st, back]
            if end > arr2:
                new.append(("stay", arr2, end, Wd.home[e], Wd.nodes[Wd.home[e]], 0))
            T[e].replace(t, end, new)
            busy_until[e] = done
            committed[int(np.ceil(t / 60.0)):int(np.ceil(done / 60.0)), e] = True
            sent.append(dict(engine=e, alert=t, mobile=t_go, arrive=arr, done=done, back=arr2))
        I["sent"] = sent
        log.append(I)
    return dict(T=T, avail=avail, reason=reason, committed=committed, incidents=log, staff=staff, bookings=bookings,
                counts=counts, rule=rule)


ASK_C = dict(second_call=0.05, again=0.06)
INC_TYPES = [   # (class, share, engines, minutes lo-hi, where)
    ("Primary fire - dwelling", 0.038, 2, (60, 150), "home"),
    ("Primary fire - other building", 0.022, 2, (60, 180), "commercial"),
    ("Primary fire - road vehicle", 0.030, 1, (40, 90), "road"),
    ("Secondary fire", 0.140, 1, (25, 70), "road"),
    ("Chimney fire", 0.012, 1, (40, 90), "home"),
    ("False alarm - apparatus", 0.360, 1, (15, 40), "mixed"),
    ("False alarm - good intent", 0.150, 1, (15, 40), "mixed"),
    ("False alarm - malicious", 0.012, 1, (15, 30), "road"),
    ("Road traffic collision", 0.070, 1, (50, 120), "road"),
    ("Other special service", 0.166, 1, (30, 90), "mixed"),
]


def incidents_2026(Wd, ops):
    r = K.rng("incidents-2026")
    n = int(ops["incidents"])
    hour_w = np.array([2, 1.5, 1.2, 1, 0.9, 0.9, 1.2, 1.6, 2.0, 2.4, 2.6, 2.8, 3.0, 3.0, 3.0, 3.1, 3.3, 3.6, 3.8, 3.8,
                       3.5, 3.1, 2.6, 2.2])
    days = r.integers(0, 365, n)
    hours = r.choice(24, n, p=hour_w / hour_w.sum())
    secs = r.integers(0, 3600, n)
    ts = np.sort(days * 86400 + hours * 3600 + secs)
    res = np.where(Wd.akind == "R")[0]
    com = np.where(Wd.akind == "C")[0]
    shares = np.array([x[1] for x in INC_TYPES]); shares /= shares.sum()
    out = []
    for k, t in enumerate(ts):
        ty = INC_TYPES[r.choice(len(INC_TYPES), p=shares)]
        where = ty[4]
        if where == "mixed":
            if ty[0] == "False alarm - apparatus":
                where = "home" if r.random() < 0.3 else "commercial"
            else:
                where = "home" if r.random() < 0.45 else ("commercial" if r.random() < 0.7 else "road")
        if where == "home":
            a = int(r.choice(res)); node = int(Wd.anode[a]); xy = Wd.axy[a].copy(); uprn_i = a
        elif where == "commercial":
            a = int(r.choice(com)); node = int(Wd.anode[a]); xy = Wd.axy[a].copy(); uprn_i = a
        else:
            node = int(r.integers(Wd.N)); xy = Wd.nodes[node] + r.normal(0, 0.05, 2); uprn_i = None
        eng = ty[2]
        dur = [int(r.integers(*ty[3])) * 60 for _ in range(eng)]
        out.append(dict(t=int(t), cls=ty[0], node=node, xy=xy, addr=uprn_i, engines=eng, dur=dur, where=where,
                        twin=None))
    # a fire alarm at non-domestic premises reported again minutes later (the alarm receiving centre and the premises
    # both call) and logged as its own incident, and the same alarm actuating again later the same day
    extra = []
    for k, I in enumerate(out):
        if I["cls"] != "False alarm - apparatus" or I["where"] != "commercial":
            continue
        u = r.random()
        if u < ASK_C["second_call"]:
            extra.append(dict(I, t=I["t"] + int(r.integers(2 * 60, 9 * 60)), engines=1,
                              dur=[int(r.integers(12, 30)) * 60], twin=("second call", k)))
        elif u < ASK_C["second_call"] + ASK_C["again"]:
            extra.append(dict(I, t=I["t"] + int(r.integers(90 * 60, 8 * 3600)), engines=1,
                              dur=[int(r.integers(15, 40)) * 60], twin=("again", k)))
    out = sorted(out + [e for e in extra if e["t"] < S_YEAR], key=lambda I: I["t"])
    return out


# ------------------------------------------------------------------------------------------------- minute arrays
def minute_arrays(Wd, sim):
    """Free (Available at the minute's start) and the node each engine stood at, from the timelines (internal: used
    for calibration only; the golden reads the shipped files)."""
    nE = Wd.nE
    free = sim["avail"] & ~sim["committed"]
    pos = np.zeros((M, nE), np.int32)
    kind = np.zeros((M, nE), np.int8)
    for e, tl in enumerate(sim["T"]):
        for s in tl.seg:
            m0 = int(np.ceil(s[1] / 60.0)); m1 = int(np.ceil(s[2] / 60.0))
            m0, m1 = max(0, m0), min(M, m1)
            if m1 <= m0:
                continue
            if s[0] == "stay":
                pos[m0:m1, e] = s[3]
            else:
                path, cum = s[3], s[4]
                t_start = s[6] if len(s) > 6 else s[1]
                ts = np.arange(m0, m1) * 60.0 - t_start
                k = np.clip(np.searchsorted(cum, ts, side="right") - 1, 0, len(path) - 1)
                pos[m0:m1, e] = np.array(path)[k]
            kind[m0:m1, e] = s[5]
    return free, pos, kind
