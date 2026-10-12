"""Traffic: each flow's scheduled services, operated day by day with the seasonal and yearly factors, and every
flight's traversals of the eight sectors (entry and exit times in whole seconds UTC, entry and exit flight levels).
The record runs 1 January 2025 to 30 September 2026; the summer 2027 planning traffic is built the same way from
the summer 2027 schedules (the new Brekka base included) for the local season."""
import datetime as dt
import math

import numpy as np

import world as W

EPOCH = dt.datetime(2025, 1, 1, tzinfo=W.UTC)
SEED = 18104


def secs(t):
    return int((t - EPOCH).total_seconds())


def at(s):
    return EPOCH + dt.timedelta(seconds=int(s))


class Service:
    __slots__ = ("flow", "callsign", "adep", "ades", "actype", "minute", "level", "alt", "offset", "op")


def _hour_minutes(rng, n):
    p = np.repeat(np.array(W.HOURS, float) / sum(W.HOURS) / 60.0, 60)
    p /= p.sum()
    return rng.choice(24 * 60, size=n, p=p)


def schedules():
    """Every flow's services with their callsigns, airports, aircraft types, usual minute of the day (local) and usual
    cruise level. Callsigns are unique except the cargo and charter rotations that fly out and back under one
    callsign on the same day."""
    rng = np.random.default_rng(SEED)
    used = set()
    out = {}
    for f, spec in W.FLOWS.items():
        n = int(math.ceil(spec["base"] * 1.12))
        mins = np.sort(_hour_minutes(rng, n))
        svcs = []
        for k in range(n):
            s = Service()
            s.flow = f
            s.op = spec["ops"][int(rng.integers(len(spec["ops"])))]
            while True:
                if s.op in ("VSK", "PXR", "ZBL", "NLY") and rng.random() < 0.45:
                    cs = "%s%d%s" % (s.op, rng.integers(1, 99), "ABCDEFGHJKLMNPRTWX"[int(rng.integers(18))])
                elif s.op in ("AMK", "MRN", "LNX", "BRT"):
                    cs = "%s%d" % (s.op, rng.integers(100, 1999))
                else:
                    cs = "%s%d" % (s.op, rng.integers(10, 9899))
                if cs not in used:
                    used.add(cs)
                    break
            s.callsign = cs
            s.adep = spec["dep"][int(rng.integers(len(spec["dep"])))]
            s.ades = spec["arr"][int(rng.integers(len(spec["arr"])))]
            if s.op == "OVN":
                pool = W.TYPES["long"]
            elif s.op in ("KRB", "RFX"):
                pool = ["B763", "A332", "B738", "B744"]
            elif s.op in ("MRN", "LNX", "BRT"):
                pool = W.TYPES["regional"]
            elif s.op in ("HXA", "GML", "TQA") and spec["kind"] == "mix" and rng.random() < 0.2:
                pool = W.TYPES["long"]
            elif s.op == "AMK" and rng.random() < 0.3:
                pool = W.TYPES["regional"]
            elif s.op in ("VSK", "PXR", "ZBL", "NLY", "DXT", "CWA"):
                pool = ["A320", "A20N", "B738", "B38M", "A321", "A21N"]
            else:
                pool = W.TYPES["short"]
            s.actype = pool[int(rng.integers(len(pool)))]
            s.minute = int(mins[k])
            lv = spec["lv"]
            s.level = int(rng.choice(lv, p=spec["w"]))
            s.alt = int(rng.choice(lv))
            # minutes from off-block to entering the first sector of the path
            if s.adep in (W.HUB, W.BREKKA, W.SKARNES):
                s.offset = int(rng.integers(18, 33))
            else:
                s.offset = int(rng.integers(45, 170))
            svcs.append(s)
        out[f] = svcs
    # out-and-back rotations under one callsign (cargo and charter)
    pairs = [("DG_SW", "DG_NE", "KRB"), ("DG_NE", "DG_SW", "KRB"), ("NS_S", "NS_N", "DXT"), ("NS_N", "NS_S", "CWA"),
             ("EW_E", "EW_W", "RFX"), ("DG_SW", "DG_NE", "LNX"), ("NS_S", "NS_N", "DXT"), ("EW_W", "EW_E", "RFX"),
             ("NS_S", "NS_N", "CWA"), ("DG_NE", "DG_SW", "KRB"), ("EW_E", "EW_W", "RFX"), ("NS_N", "NS_S", "DXT")]
    taken = set()
    for a, b, op in pairs:
        cand_a = [s for s in out[a] if s.op == op and id(s) not in taken]
        cand_b = [s for s in out[b] if id(s) not in taken]
        if not cand_a:
            cand_a = [s for s in out[a] if id(s) not in taken]
        sa = cand_a[int(rng.integers(len(cand_a)))]
        taken.add(id(sa))
        later = [s for s in cand_b if 180 <= s.minute - sa.minute <= 420]
        sb = later[int(rng.integers(len(later)))] if later else cand_b[0]
        taken.add(id(sb))
        sb.op = sa.op
        sb.callsign = sa.callsign
        sb.adep, sb.ades = sa.ades, sa.adep
        sb.actype = sa.actype
    return out


def volume(flow, day):
    """Flights a day the flow carries on this local date, before the seasonal and weekday factors."""
    base = W.FLOWS[flow]["base"]
    after = dt.datetime.combine(day, dt.time(12), tzinfo=W.LOCAL) >= W.REROUTE_W
    if flow == "HUB_ARR_W":
        return 30 if after else 16
    if flow == "HUB_ARR_WK":
        return 0 if after else 10
    if flow in W.NEW_2027:
        return base if day.year == 2027 else 0
    return base


def factor(day, flow):
    if flow in W.NEW_2027:
        return 1.0
    return W.MONTH[day.month] * W.YEAR[day.year] * W.WEEKDAY[day.weekday()]


class Traffic:
    """Flights and traversals as parallel arrays. Flight arrays: callsign, adep, ades, actype, flow, eobt (s), level.
    Traversal arrays: flight index, sector index, t0, t1 (s), a, b (flight levels)."""

    def __init__(self):
        self.f = {k: [] for k in ("callsign", "adep", "ades", "actype", "flow", "eobt", "level", "day")}
        self.t = {k: [] for k in ("fi", "sec", "t0", "t1", "a", "b")}

    def arrays(self):
        f = {k: np.array(v) for k, v in self.f.items()}
        t = {k: np.array(v) for k, v in self.t.items()}
        for k in ("fi", "sec", "t0", "t1", "a", "b"):
            t[k] = t[k].astype(np.int64)
        f["eobt"] = f["eobt"].astype(np.int64)
        return f, t


def _days(d0, d1):
    d = d0
    while d <= d1:
        yield d
        d += dt.timedelta(days=1)


def fly(svcs, days, rng, planning=False):
    """Operate the services on each local date. Planning traffic keeps the schedule's minute with a small spread;
    the record carries the day's operating spread."""
    tr = Traffic()
    sidx = {s: i for i, s in enumerate(W.SECTORS)}
    for day in days:
        mid = dt.datetime.combine(day, dt.time(0), tzinfo=W.LOCAL)
        for flow, lst in svcs.items():
            v = volume(flow, day)
            if v == 0:
                continue
            p = min(1.0, v * factor(day, flow) / len(lst))
            if planning and flow in W.NEW_2027:
                p = 1.0
            go = rng.random(len(lst)) < p
            path = W.FLOWS[flow]["path"]
            for s, g in zip(lst, go):
                if not g:
                    continue
                spread = rng.normal(0, 4 if planning else 9)
                late = 0 if planning or rng.random() > 0.12 else rng.exponential(25)
                t_first = mid + dt.timedelta(minutes=s.minute + spread + late)
                start = secs(t_first.astimezone(W.UTC)) + int(rng.integers(0, 60))
                lvl = s.level if rng.random() < 0.72 else s.alt
                fi = len(tr.f["callsign"])
                tr.f["callsign"].append(s.callsign)
                tr.f["adep"].append(s.adep)
                tr.f["ades"].append(s.ades)
                tr.f["actype"].append(s.actype)
                tr.f["flow"].append(flow)
                tr.f["eobt"].append(start - 60 * s.offset - int(rng.integers(0, 300)))
                tr.f["level"].append(lvl)
                tr.f["day"].append(day.toordinal())
                t = start
                step = flow.startswith(("EW", "NS")) and rng.random() < 0.04
                step_at = int(rng.integers(len(path))) if step else -1
                cur = lvl
                for k, (sec, a, b, m) in enumerate(path):
                    a2 = cur if a == "C" else (245 + min(int(rng.exponential(5)), 30) if a == 245 else a)
                    b2 = lvl if b == "C" else b
                    if a == "C" and b == "C":
                        a2 = b2 = cur
                        if k == step_at:
                            b2 = cur + (20 if rng.random() < 0.6 else -20)
                            cur = b2
                    elif b == "C":
                        cur = b2
                    d = int(round(60 * m * rng.uniform(0.93, 1.07)))
                    tr.t["fi"].append(fi)
                    tr.t["sec"].append(sidx[sec])
                    tr.t["t0"].append(t)
                    tr.t["t1"].append(t + d)
                    tr.t["a"].append(a2)
                    tr.t["b"].append(b2)
                    t += d
    return tr


def record():
    svcs = schedules()
    rng = np.random.default_rng(SEED + 1)
    d0 = (W.ACTUAL_START - dt.timedelta(days=1)).date()
    d1 = (W.ACTUAL_END + dt.timedelta(days=1)).date()
    tr = fly(svcs, _days(d0, d1), rng)
    f, t = tr.arrays()
    lo, hi = secs(W.ACTUAL_START), secs(W.ACTUAL_END)
    # the extract holds the traversals entered in the window
    keep = (t["t0"] >= lo) & (t["t0"] < hi)
    return svcs, f, {k: v[keep] for k, v in t.items()}


def planning(svcs):
    rng = np.random.default_rng(SEED + 2)
    a, b = W.season(2027)
    d0, d1 = (a - dt.timedelta(days=1)).date(), (b + dt.timedelta(days=1)).date()
    tr = fly(svcs, _days(d0, d1), rng, planning=True)
    f, t = tr.arrays()
    keep = (t["t0"] >= secs(a)) & (t["t0"] < secs(b))
    return f, {k: v[keep] for k, v in t.items()}
