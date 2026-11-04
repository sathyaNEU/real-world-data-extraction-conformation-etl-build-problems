"""The operating year, from 1 April 2025 to 30 September 2026: every signaller route request and what the control
system made of it, every operating incident with the trains it delayed, the delay attribution reviews, the ARS
sub-areas switched off and on, and the control system's server changes. The clean truth; pack.py writes the
systems' own exports from it."""
import bisect
import datetime as dt
import math

import numpy as np

import staffing as S
import world as W

P_SLIP = 1 / 72.0         # a selection of an exit drawn within CLOSE_MAX of another exit of the entrance
P_SLIP_CAUGHT = 0.83       # caught on the screen within seconds and reset
P_MISTAKE_FY = 1 / 1500.0  # a wrong exit chosen, first two years since qualifying
P_MISTAKE_EXP = 1 / 7500.0
P_MISTAKE_CAUGHT = 0.16
PEAK_H = (7, 8, 16, 17, 18)
SIM_SEED = 15
CLOSE_BASE, CLOSE_PEAK = 1.05, 2.2   # the drawn-close routes: the December 2025 peak services over the crossovers
TYPES = ("RS1", "RS2", "RS3", "RG1", "CM1", "AR1", "EQ1")


def hour_weight(h, peak):
    w = 0.26 if (h < 6 or h >= 23) else 1.0
    if h in PEAK_H:
        w *= 1.6 * peak
    return w


def local_hours(a, b):
    """Every local wall-clock hour start between two dates, with its UTC start and length in seconds (the
    repeated October hour and the missing March hour handled on the clock)."""
    out = []
    t = W.local_to_utc(dt.datetime(a.year, a.month, a.day, 0))
    end = W.local_to_utc(dt.datetime(b.year, b.month, b.day, 0) + dt.timedelta(days=1))
    while t < end:
        loc = W.utc_to_local(t)
        out.append((t, loc))
        t += dt.timedelta(hours=1)
    return out


class Trains:
    """Headcodes of the trains on each workstation's area, drawn per day."""

    def __init__(self, r):
        self.r = r
        self.cache = {}

    def headcode(self, ws, day):
        key = (ws, day)
        if key not in self.cache:
            letters = {"W01": "FGP", "W02": "CJK", "W03": "HMT", "W04": "LNR", "W05": "KVW", "W06": "SWX"}[ws]
            pool = []
            for _ in range(160):
                cls = self.r.choice(["1", "2", "2", "2", "5", "6"])
                pool.append("%s%s%02d" % (cls, letters[int(self.r.integers(0, 3))], int(self.r.integers(1, 99))))
            self.cache[key] = pool
        p = self.cache[key]
        return p[int(self.r.integers(0, len(p)))]


def simulate(net, staff, rosters):
    r = W.rng(SIM_SEED)
    byp = {p["staff_no"]: p for p in staff}
    idx = S.on_duty_index(rosters["spans"])
    hours = local_hours(W.SIM_START, W.SIM_END)
    n_h = len(hours)
    loc_h = np.array([lc.hour for _, lc in hours])
    wkend = np.array([lc.weekday() >= 5 for _, lc in hours])
    after_tt = np.array([lc.date() >= W.TT_CHANGE for _, lc in hours])
    trains = Trains(W.rng(11))
    # request volumes: routes at junctions busier than plain line, the drawn-close routes busy in the peaks and
    # given more work by the December 2025 timetable (more stopping services over the junction crossovers)
    routes = net["routes"]
    base = {}
    for rt in routes:
        g = float(r.lognormal(0.0, 0.75))
        if rt["close"]:
            g = g ** 0.45      # the crossover routes the timetable uses every hour vary less
        b = g * (1.0 if rt["multi"] else 0.55) * W.TRAFFIC[rt["ws"]]
        if rt["close"]:
            b *= CLOSE_BASE
        base[rt["route_id"]] = b
    peak = {rt["route_id"]: (CLOSE_PEAK if rt["close"] else float(r.choice([0.8, 1.0, 1.15, 1.35]))) for rt in routes}
    growth = {rt["route_id"]: (1.22 if rt["close"] else float(r.choice([0.96, 1.0, 1.04, 1.08]))) for rt in routes}
    scale = 0.0282
    req = []   # (utc, ws, staff_no, route)
    for rt in routes:
        rid = rt["route_id"]
        hw = np.array([hour_weight(h, peak[rid]) for h in range(24)])[loc_h]
        lam = scale * base[rid] * hw * np.where(wkend, 0.72, 1.0) * np.where(after_tt, growth[rid], 1.0)
        counts = r.poisson(lam)
        for k in np.nonzero(counts)[0]:
            t0, _ = hours[int(k)]
            for _ in range(int(counts[k])):
                req.append((t0 + dt.timedelta(seconds=float(r.uniform(0, 3599.0))), rt["ws"], rid))
    req.sort()
    rmap = {rt["route_id"]: rt for rt in routes}
    by_ent = net["by_ent"]
    events = []        # control system actions: (utc, ws, user, event, entrance, exit, route_id, headcode)
    incidents = []
    nreq = 0
    stats = dict(requests=0, slips=0, slips_caught=0, mistakes=0, mistakes_caught=0)
    for t, ws, rid in req:
        sn, s0, how = S.who_at(idx, ws, t)
        if sn is None:
            continue
        rt = rmap[rid]
        day = W.utc_to_local(t).date()
        fy = W.first_two_years(byp[sn], day)
        hc = trains.headcode(ws, day) if r.random() < 0.93 else ""
        stats["requests"] += 1
        ent = rt["entrance"]
        wrong = None
        kind = None
        edge = W.near_window_edge(t)
        if rt["close"] and r.random() < P_SLIP:
            if not edge:
                wrong = rmap[rt["neighbour"]]
                kind = "slip"
        elif rt["multi"] and not any(o["close"] for o in by_ent[ent]):
            p = P_MISTAKE_FY if fy else P_MISTAKE_EXP
            if r.random() < p and not edge:
                others = [o for o in by_ent[ent] if o["route_id"] != rid]
                wrong = others[int(r.integers(0, len(others)))]
                kind = "mistake"
        if r.random() < 0.014 and wrong is None:
            # rejected: the route was not available; asked again a little later
            events.append((t, ws, sn, "RQ", ent, rt["exit"], rid, hc))
            events.append((t + dt.timedelta(seconds=float(r.uniform(0.4, 1.6))), ws, sn, "RJ", ent, rt["exit"], rid, hc))
            t = t + dt.timedelta(seconds=float(r.uniform(22, 280)))
        if wrong is None:
            events.append((t, ws, sn, "RQ", ent, rt["exit"], rid, hc))
            ts = t + dt.timedelta(seconds=float(r.uniform(0.6, 2.4)))
            events.append((ts, ws, sn, "ST", ent, rt["exit"], rid, hc))
            if r.random() < 0.021:
                # regulating: the route taken off and the train sent another way, minutes later
                tc = ts + dt.timedelta(seconds=float(r.uniform(65, 1150)))
                events.append((tc, ws, sn, "CN", ent, rt["exit"], rid, hc))
                others = [o for o in by_ent[ent] if o["route_id"] != rid]
                if others and r.random() < 0.6:
                    o = others[int(r.integers(0, len(others)))]
                    tq = tc + dt.timedelta(seconds=float(r.uniform(35, 600)))
                    events.append((tq, ws, sn, "RQ", ent, o["exit"], o["route_id"], hc))
                    events.append((tq + dt.timedelta(seconds=float(r.uniform(0.6, 2.4))), ws, sn, "ST", ent, o["exit"],
                                   o["route_id"], hc))
            continue
        # a wrong exit selected
        events.append((t, ws, sn, "RQ", ent, wrong["exit"], wrong["route_id"], hc))
        ts = t + dt.timedelta(seconds=float(r.uniform(0.6, 2.4)))
        events.append((ts, ws, sn, "ST", ent, wrong["exit"], wrong["route_id"], hc))
        caught = r.random() < (P_SLIP_CAUGHT if kind == "slip" else P_MISTAKE_CAUGHT)
        stats[kind + "s"] += 1
        if caught:
            stats[kind + "s_caught"] += 1
            if kind == "slip":
                tc = ts + dt.timedelta(seconds=float(r.uniform(2.6, 13.8)))
                tq = tc + dt.timedelta(seconds=float(r.uniform(1.4, 6.2)))
            else:
                tc = ts + dt.timedelta(seconds=float(r.uniform(70, 420)))
                tq = tc + dt.timedelta(seconds=float(r.uniform(40, 300)))
            events.append((tc, ws, sn, "CN", ent, wrong["exit"], wrong["route_id"], hc))
            events.append((tq, ws, sn, "RQ", ent, rt["exit"], rid, hc))
            events.append((tq + dt.timedelta(seconds=float(r.uniform(0.6, 2.4))), ws, sn, "ST", ent, rt["exit"], rid, hc))
            continue
        ti = ts + dt.timedelta(seconds=float(r.uniform(70, 540)))
        incidents.append(dict(type="RS1", mech=kind, utc=ti, ws=ws, staff_no=sn, fy=fy, route_set=wrong["route_id"],
                              route_required=rid, headcode=hc or trains.headcode(ws, day), junction=rt["junction"],
                              shift_start=s0, how=how))
    incidents += other_incidents(W.rng(12), net, staff, idx, hours, trains, byp)
    return dict(events=events, incidents=incidents, stats=stats, base=base, peak=peak, growth=growth)


def other_incidents(r, net, staff, idx, hours, trains, byp):
    """Late route setting under load, routes not set late in a long shift, regulating and communication errors,
    ARS routing the wrong way, and the workstations' own equipment faults."""
    out = []
    rm = [rt for rt in net["routes"] if rt["multi"]]
    for t, lc in hours:
        d = lc.date()
        h = lc.hour
        wk = lc.weekday() >= 5
        for ws in W.WS_IDS:
            sn, s0, how = S.who_at(idx, ws, t + dt.timedelta(minutes=30))
            if sn is None:
                continue
            fy = W.first_two_years(byp[sn], d)
            load = W.TRAFFIC[ws] * hour_weight(h, 1.25) * (0.72 if wk else 1.0) * (1.05 if d >= W.TT_CHANGE else 1.0)
            if ws == "W03":
                load *= 1.12
            lam_late = 0.0118 * max(0.0, load - 0.85) ** 2.1
            tin = (t - W.local_to_utc(s0)).total_seconds() / 3600.0
            night_late = (s0.hour == 19) and tin >= 8
            lam_omit = 0.00071 * (5.2 if night_late else (1.6 if tin >= 8 else 1.0))
            lam_reg = 0.00036 * (2.9 if fy else 1.0) * (1.0 if 6 <= h < 23 else 0.25) * min(load, 2.0)
            lam_com = 0.00041 * (1.7 if fy else 1.0)
            for typ, lam in (("RS2", lam_late), ("RS3", lam_omit), ("RG1", lam_reg), ("CM1", lam_com)):
                n = int(r.poisson(lam))
                for _ in range(n):
                    ti = t + dt.timedelta(seconds=float(r.uniform(0, 3599)))
                    sn2, s02, how2 = S.who_at(idx, ws, ti)
                    rt = rm[int(r.integers(0, len(rm)))]
                    while rt["ws"] != ws:
                        rt = rm[int(r.integers(0, len(rm)))]
                    out.append(dict(type=typ, mech={"RS2": "workload", "RS3": "fatigue", "RG1": "regulation",
                                                    "CM1": "communication"}[typ],
                                    utc=ti, ws=ws, staff_no=sn2, fy=W.first_two_years(byp[sn2], W.utc_to_local(ti).date()),
                                    route_set="", route_required="", headcode=trains.headcode(ws, d),
                                    junction=rt["junction"], shift_start=s02, how=how2))
    # ARS wrong routes: timetable data sending a train the wrong way, at any junction
    n_ars = int(r.integers(30, 37))
    for _ in range(n_ars):
        t, lc = hours[int(r.integers(0, len(hours)))]
        ti = t + dt.timedelta(seconds=float(r.uniform(0, 3599)))
        rt = rm[int(r.integers(0, len(rm)))]
        while any(o["close"] for o in net["by_ent"][rt["entrance"]]):
            rt = rm[int(r.integers(0, len(rm)))]
        others = [o for o in net["by_ent"][rt["entrance"]] if o["route_id"] != rt["route_id"]]
        wrong = others[int(r.integers(0, len(others)))]
        sn, s0, how = S.who_at(idx, rt["ws"], ti)
        out.append(dict(type="AR1", mech="ars", utc=ti, ws=rt["ws"], staff_no=sn,
                        fy=W.first_two_years(byp[sn], W.utc_to_local(ti).date()), route_set=wrong["route_id"],
                        route_required=rt["route_id"], headcode=trains.headcode(rt["ws"], lc.date()),
                        junction=rt["junction"], shift_start=s0, how=how))
    # the workstations' display equipment: screens freezing, a workstation dropping to its standby display
    n_eq = int(r.integers(17, 21))
    for _ in range(n_eq):
        t, lc = hours[int(r.integers(0, len(hours)))]
        ti = t + dt.timedelta(seconds=float(r.uniform(0, 3599)))
        ws = W.WS_IDS[int(r.integers(0, 6))]
        sn, s0, how = S.who_at(idx, ws, ti)
        out.append(dict(type="EQ1", mech="display", utc=ti, ws=ws, staff_no=sn,
                        fy=W.first_two_years(byp[sn], W.utc_to_local(ti).date()), route_set="", route_required="",
                        headcode=trains.headcode(ws, lc.date()), junction=W.JUNCTIONS[ws][int(r.integers(0, 3))],
                        shift_start=s0, how=how))
    return [i for i in out if not W.near_window_edge(i["utc"])]


MEAN_MIN = {"RS1": 108, "RS2": 12.5, "RS3": 27, "RG1": 44, "CM1": 19, "AR1": 63, "EQ1": 74}
REACT = {"RS1": 3.2, "RS2": 0.7, "RS3": 1.1, "RG1": 1.9, "CM1": 0.8, "AR1": 2.4, "EQ1": 3.6}


def delays(incidents, trains):
    """Each incident's delay records: the train it struck and the trains held behind it, whole minutes."""
    r = W.rng(13)
    for inc in sorted(incidents, key=lambda x: x["utc"]):
        typ = inc["type"]
        total = max(3, int(round(float(r.lognormal(math.log(MEAN_MIN[typ]) - 0.22, 0.66)))))
        n_r = int(r.poisson(REACT[typ]))
        recs = []
        day = W.utc_to_local(inc["utc"]).date()
        if n_r == 0:
            recs.append((inc["headcode"], "P", total))
        else:
            share = r.dirichlet(np.ones(n_r + 1) * 1.4)
            share[0] += 0.35
            share = share / share.sum()
            mins = np.maximum(1, np.round(share * total)).astype(int)
            recs.append((inc["headcode"], "P", int(mins[0])))
            used = {inc["headcode"]}
            for k in range(1, n_r + 1):
                hc = trains.headcode(inc["ws"], day)
                while hc in used:
                    hc = trains.headcode(inc["ws"], day)
                used.add(hc)
                recs.append((hc, "R", int(mins[k])))
        inc["delay_records"] = recs
        inc["minutes"] = sum(m for _, _, m in recs)
    return incidents


def number_incidents(incidents):
    """TRUST numbers are drawn route-wide in time order, so the operating centre's numbers rise with gaps; the
    registers number their own entries in order of report within each financial year."""
    r = W.rng(14)
    cur = 403117
    for inc in sorted(incidents, key=lambda x: x["utc"]):
        cur += int(r.integers(31, 97))
        inc["trust"] = cur
    for fy in (2025, 2026):
        lst = [i for i in incidents if W.railway_period(W.utc_to_local(i["utc"]).date())[0] == fy]
        lst.sort(key=lambda x: x["utc"])
        n = int(r.integers(3, 9))
        for i in lst:
            n += 1 if r.random() < 0.93 else 2
            i["ref"] = "FROC/%02d/%04d" % (fy % 100, n)
    return incidents


def reviews(incidents):
    """The delay attribution reviews: minutes on one train moved between incidents once agreed with the train
    operator, out of the operating centre's incidents and into them."""
    r = W.rng(19)
    moves = []
    pool = sorted(incidents, key=lambda x: x["utc"])
    n_ref = 2207
    def nearby(t):
        # another of the route's incidents, numbered within the same few minutes of logging
        return t + int(r.choice([-1, 1])) * int(r.integers(1, 30))

    for inc in pool:
        u = r.random()
        st = "Agreed"
        v = r.random()
        if v < 0.06:
            st = "Rejected"
        elif v < 0.09 and W.utc_to_local(inc["utc"]).date() > dt.date(2026, 7, 20):
            st = "Under review"
        if u < 0.07 and len(inc["delay_records"]) > 1:
            hc, ev, m = inc["delay_records"][int(r.integers(1, len(inc["delay_records"])))]
            moved = m if r.random() < 0.6 else max(1, int(m * float(r.uniform(0.3, 0.8))))
            n_ref += int(r.integers(2, 9))
            moves.append(dict(ref="DAR-%05d" % n_ref, inc=inc, out=True, headcode=hc, minutes=moved,
                              other=nearby(inc["trust"]), status=st,
                              agreed=W.utc_to_local(inc["utc"]).date() + dt.timedelta(days=int(r.integers(9, 47)))))
        elif u < 0.11:
            hc = inc["delay_records"][0][0]
            moved = int(r.integers(3, 38))
            n_ref += int(r.integers(2, 9))
            moves.append(dict(ref="DAR-%05d" % n_ref, inc=inc, out=False, headcode=hc, minutes=moved,
                              other=nearby(inc["trust"]), status=st,
                              agreed=W.utc_to_local(inc["utc"]).date() + dt.timedelta(days=int(r.integers(9, 47)))))
    for mv in moves:
        if mv["agreed"] > dt.date(2026, 10, 6):
            mv["status"] = "Under review"
        if mv["status"] == "Under review":
            mv["agreed"] = None
    for inc in incidents:
        inc["final_minutes"] = inc["minutes"]
    for mv in moves:
        if mv["status"] == "Agreed":
            mv["inc"]["final_minutes"] += (-mv["minutes"] if mv["out"] else mv["minutes"])
    return moves


def investigate(incidents):
    """Each local investigation's underlying-cause finding, reached from what an investigator sees: the
    signaller's experience, the hour, how long into the shift, the category. An investigator cannot tell a wrong
    exit selected by mistake from one selected by a slip of the hand."""
    r = W.rng(16)
    for inc in sorted(incidents, key=lambda x: x["utc"]):
        loc = W.utc_to_local(inc["utc"])
        peak = loc.hour in PEAK_H
        tin = (loc - inc["shift_start"]).total_seconds() / 3600.0 if inc["shift_start"] else 0
        u = r.random()
        typ = inc["type"]
        if typ == "AR1":
            f = "ars"
        elif typ == "EQ1":
            f = "equipment"
        elif typ == "RS2":
            f = "workload" if u < 0.68 else ("distraction" if u < 0.9 else "competence")
        elif typ == "RS3":
            if tin >= 8:
                f = "fatigue" if u < 0.62 else ("distraction" if u < 0.9 else "competence")
            else:
                f = "distraction" if u < 0.55 else ("competence" if u < 0.85 else "not determined")
        elif typ in ("RG1", "CM1"):
            f = "competence" if u < (0.78 if inc["fy"] else 0.55) else ("distraction" if u < 0.95 else "workload")
        else:   # wrong routes
            if inc["fy"]:
                f = "competence" if u < 0.8 else ("distraction" if u < 0.95 else "workload")
            elif peak:
                f = "competence" if u < 0.42 else ("distraction" if u < 0.74 else "workload")
            elif tin >= 8:
                f = "fatigue" if u < 0.35 else ("competence" if u < 0.7 else "distraction")
            else:
                f = "competence" if u < 0.55 else ("distraction" if u < 0.93 else "not determined")
        inc["finding"] = f
    return incidents


NEW_FINDING = {"competence": None, "distraction": "Distraction", "workload": "Workload", "fatigue": "Fatigue",
               "ars": "ARS timetable data", "equipment": "Workstation equipment", "not determined": "Not determined"}


def register_fields(incidents, net, narrate):
    """What the register keeps beside each incident: the delay estimated when it was logged, the local
    investigation's reference and closing date, the narrative."""
    r = W.rng(17)
    lab = None
    n_li = {2025: int(r.integers(11, 40)), 2026: int(r.integers(4, 30))}
    for inc in sorted(incidents, key=lambda x: x["ref"]):
        fy = W.railway_period(W.utc_to_local(inc["utc"]).date())[0]
        p = inc["delay_records"][0][2]
        inc["initial"] = int(max(0, 5 * round((p * float(r.uniform(0.7, 1.15))) / 5)))
        n_li[fy] += 1 if r.random() < 0.9 else 2
        inc["li"] = "LI-%02d-%03d" % (fy % 100, n_li[fy])
        d = W.utc_to_local(inc["utc"]).date() + dt.timedelta(days=int(r.integers(8, 64)))
        inc["li_closed"] = d if d <= dt.date(2026, 10, 6) else None
        f = inc["finding"]
        if f == "competence":
            inc["finding26"] = "Competence - regulating" if inc["type"] == "RG1" else "Competence - route setting"
        else:
            inc["finding26"] = NEW_FINDING[f]
    for inc in incidents:
        inc["summary"] = narrate(r, inc)
    return incidents


# --------------------------------------------------------------------------------------------- ARS sub-areas

def ars(idx):
    """ARS off and on per sub-area: switched off by the signaller when trains run out of course, under
    engineering possessions and when the ARS timetable data is wrong, each sub-area on its own; and now and then
    the whole workstation's ARS drops at once (one event for the workstation), after which the signaller brings
    each sub-area back separately. Truth: one interval per sub-area, UTC."""
    r = W.rng(20)
    t0 = W.local_to_utc(dt.datetime(2025, 9, 12, 0))
    t1 = W.local_to_utc(dt.datetime(2026, 10, 9, 0))
    periods = []
    drops = []
    quiet = quiet_windows()

    def clear(a, b):
        return all(b <= x or a >= y for x, y in quiet)

    for ws in W.WS_IDS:
        # whole-workstation drops first, so the sub-area intervals can be laid around them
        t = t0 + dt.timedelta(days=float(r.uniform(5, 40)))
        while t < t1:
            a = t.replace(second=int(r.integers(0, 60)), microsecond=0)
            ons = {sa: a + dt.timedelta(minutes=float(r.lognormal(math.log(48), 0.7))) + dt.timedelta(
                minutes=float(k * r.uniform(2, 9))) for k, sa in enumerate(W.SUBAREAS[ws])}
            if not clear(a, max(ons.values())):
                t += dt.timedelta(hours=6)
                continue
            sn, _, _ = S.who_at(idx, ws, a)
            drops.append(dict(ws=ws, off=a, ons=ons, user_off=sn))
            t += dt.timedelta(days=float(r.uniform(38, 95)))
    for ws in W.WS_IDS:
        mine = sorted([d for d in drops if d["ws"] == ws], key=lambda d: d["off"])
        for sa in W.SUBAREAS[ws]:
            blocked = [(d["off"] - dt.timedelta(minutes=5), d["ons"][sa] + dt.timedelta(minutes=5)) for d in mine]
            blocked += quiet
            for d in mine:
                sn2, _, _ = S.who_at(idx, ws, d["ons"][sa])
                periods.append(dict(ws=ws, sa=sa, off=d["off"], on=d["ons"][sa], kind="drop", user_off=d["user_off"],
                                    user_on=sn2, ws_event=True))
            t = t0 + dt.timedelta(hours=float(r.uniform(0, 30)))
            busy_until = t0
            while t < t1:
                t += dt.timedelta(hours=float(r.exponential(33.0)))
                kind = r.choice(["ooc", "data", "poss"], p=[0.82, 0.09, 0.09])
                if kind == "ooc":
                    dur = float(r.lognormal(math.log(0.6), 0.8))
                elif kind == "data":
                    dur = float(r.lognormal(math.log(3.2), 0.6))
                else:
                    dur = float(r.lognormal(math.log(5.8), 0.3))
                a = max(t, busy_until + dt.timedelta(minutes=3))
                if kind == "poss":
                    # engineering possessions are taken at night: the line handed over between 23:00 and 01:40
                    lc = W.utc_to_local(a)
                    night = dt.datetime(lc.year, lc.month, lc.day, 23, 0) + dt.timedelta(minutes=float(r.uniform(0, 160)))
                    if night < lc:
                        night += dt.timedelta(days=1)
                    a = W.local_to_utc(night.replace(microsecond=0))
                b = a + dt.timedelta(hours=dur)
                if b > t1:
                    break
                if any(not (b <= x or a >= y) for x, y in blocked):
                    t = b
                    continue
                sn, _, _ = S.who_at(idx, ws, a)
                sn2, _, _ = S.who_at(idx, ws, b)
                periods.append(dict(ws=ws, sa=sa, off=a, on=b, kind=str(kind), user_off=sn, user_on=sn2,
                                    ws_event=False))
                busy_until = b
                t = b
    rm = W.rng(22)

    def ms(t):
        return t.replace(microsecond=int(rm.integers(0, 1000)) * 1000)
    for d in drops:
        d["off"] = ms(d["off"])
        d["ons"] = {sa: ms(t) for sa, t in d["ons"].items()}
    for p in periods:
        if p.get("ws_event"):
            continue
        p["off"], p["on"] = ms(p["off"]), ms(p["on"])
    for p in periods:
        if p.get("ws_event"):
            d = [x for x in drops if x["ws"] == p["ws"] and abs((x["off"] - p["off"]).total_seconds()) < 1.0][0]
            p["off"], p["on"] = d["off"], d["ons"][p["sa"]]
    periods.sort(key=lambda p: (p["off"], p["sa"]))
    nudge_mid_bin(periods)
    return periods, drops


BOUNDS = [dt.date(2025, 10, 1), dt.date(2026, 1, 1), dt.date(2026, 4, 1), dt.date(2026, 7, 1), dt.date(2026, 10, 1)]


def quiet_windows():
    """Two hours either side of each quarter's first midnight, UK time, in UTC, and three either side of each
    clock change."""
    out = []
    for b in BOUNDS:
        t = W.local_to_utc(dt.datetime(b.year, b.month, b.day))
        out.append((t - dt.timedelta(hours=2), t + dt.timedelta(hours=2)))
    for t in (dt.datetime(2025, 10, 26, 1), dt.datetime(2026, 3, 29, 1)):
        out.append((t - dt.timedelta(hours=3), t + dt.timedelta(hours=3)))
    return out


def ars_cells(periods):
    cells = {}
    for p in periods:
        for k in range(4):
            q0 = W.local_to_utc(dt.datetime.combine(BOUNDS[k], dt.time(0)))
            q1 = W.local_to_utc(dt.datetime.combine(BOUNDS[k + 1], dt.time(0)))
            x, y = max(p["off"], q0), min(p["on"], q1)
            if y > x:
                cells[(p["ws"], k)] = cells.get((p["ws"], k), 0.0) + (y - x).total_seconds()
    return cells


def nudge_mid_bin(periods):
    """Each workstation's quarterly sub-area hours sit near the middle of their tenth-of-an-hour bin: one
    ordinary switch-on in the cell moved by a few minutes, never near another event on its sub-area."""
    r = W.rng(23)
    cells = ars_cells(periods)
    by_sa = {}
    for p in periods:
        by_sa.setdefault(p["sa"], []).append(p)
    for lst in by_sa.values():
        lst.sort(key=lambda p: p["off"])
    used = set()
    for (ws, k), secs in sorted(cells.items()):
        target_off = float(r.uniform(-60, 60))
        resid = (secs % 360.0)
        resid = resid - 360.0 if resid > 180.0 else resid
        delta = round(target_off - resid, 3)
        # no two cells print the same tenth of an hour
        while round((secs + delta) / 360.0) in used:
            delta += 360.0
        used.add(round((secs + delta) / 360.0))
        q0 = W.local_to_utc(dt.datetime.combine(BOUNDS[k], dt.time(0))) + dt.timedelta(hours=3)
        q1 = W.local_to_utc(dt.datetime.combine(BOUNDS[k + 1], dt.time(0))) - dt.timedelta(hours=3)
        done = False
        for p in sorted((p for p in periods if p["ws"] == ws and not p.get("ws_event") and q0 < p["off"] and p["on"] < q1),
                        key=lambda p: -(p["on"] - p["off"]).total_seconds()):
            lst = by_sa[p["sa"]]
            i = lst.index(p)
            nxt = lst[i + 1]["off"] if i + 1 < len(lst) else None
            new_on = p["on"] + dt.timedelta(milliseconds=int(round(delta * 1000)))
            if new_on <= p["off"] + dt.timedelta(minutes=5):
                continue
            if nxt is not None and new_on > nxt - dt.timedelta(minutes=8):
                continue
            p["on"] = new_on
            done = True
            break
        assert done, (ws, k)



def failovers():
    """The control system's server changes: server A is the normal master; it hands over to B for its monthly
    maintenance night, between half past midnight and six in the morning."""
    r = W.rng(21)
    out = []
    for k in range(12):
        y, m = 2025 + (9 + k) // 12, (9 + k) % 12 + 1
        while True:
            day = dt.date(y, m, int(r.integers(4, 27)))
            if day not in (dt.date(2025, 10, 26), dt.date(2026, 3, 29)):
                break
        start = dt.datetime(day.year, day.month, day.day, 0, 30) + dt.timedelta(minutes=float(r.uniform(4, 85)))
        d = W.local_to_utc(start.replace(microsecond=0))
        out.append(dict(a_down=d, a_up=d + dt.timedelta(minutes=float(r.uniform(195, 320)))))
    return out
