"""task270 records: the files the service's systems export, written from the world and the 2026 operations. Nothing here
decides the answer; calc.py reads the files back."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import ops as O
import world as W

M = K.MINUTES
STATUS = {"AV": ("1", "Available"), "MB": ("3", "Mobilised"), "AT": ("5", "In attendance"), "OR": ("8", "Off the run")}
REASON = {1: "Crew", 2: "Defect", 3: "Workshop"}


def utc(t_s):
    return K.T0 + dt.timedelta(seconds=float(t_s))


def ts_utc(t_s):
    return K.stamp(utc(round(t_s)))


def ts_local(t_s):
    return K.stamp(K.local(utc(round(t_s))))


def ts_local_offset(t_s):
    """Local clock time with its UTC offset, as the tracking system writes it."""
    u = utc(round(t_s))
    off = "+01:00" if K.bst(u) else "+00:00"
    return K.local(u).strftime("%Y-%m-%dT%H:%M:%S") + off


def ts_local_min(m_local):
    """A local clock minute index (minutes from local midnight on 1 January 2026) as text."""
    return K.stamp(K.T0 + dt.timedelta(minutes=int(m_local)))


def grid(xy):
    return int(round(K.E0 + xy[0] * 1000.0)), int(round(K.N0 + xy[1] * 1000.0))


# ------------------------------------------------------------------------------------------------- incidents 2026
def gapped(n, key, start=1):
    """n increasing reference numbers with the gaps a live system leaves (calls closed without an incident, records
    voided, ids taken by other record types)."""
    r = K.rng("refs", key)
    return start + np.cumsum(r.choice([1, 1, 1, 1, 1, 2, 2, 3], n)) - 1


def number_incidents(sim):
    inc = sorted(sim["incidents"], key=lambda I: I["t"])
    nums = gapped(len(inc), "inc-2026")
    for I, k in zip(inc, nums):
        I["number"] = "26/%05d" % k


# ------------------------------------------------------------------------------------------------- status log
def status_events(Wd, sim):
    """Per engine, the status changes in seconds: (t, key, reason, incident)."""
    avail, reason = sim["avail"], sim["reason"]
    ev = {e: [] for e in range(Wd.nE)}
    busy = {e: [] for e in range(Wd.nE)}
    for I in sim["incidents"]:
        for s in I["sent"]:
            busy[s["engine"]].append((s["alert"], s["arrive"], s["done"], I["number"]))
    for e in range(Wd.nE):
        # base status by minute from crew rule, defects and workshop: changes land on the minute (booking times)
        base = np.where(avail[:, e], 0, reason[:, e].astype(int))
        ch = np.r_[0, np.where(np.diff(base) != 0)[0] + 1]
        segs = [(int(m) * 60, int(base[m])) for m in ch]
        # overlay incidents: alert..arrive Mobilised, arrive..done In attendance
        out = []
        bi = sorted(busy[e])
        k = 0
        cur_t = 0
        events = []
        for t, b in segs:
            events.append((t, "base", b, None))
        for a, r_, d, num in bi:
            events.append((a, "alert", None, num))
            events.append((r_, "arrive", None, num))
            # an engine whose crew is not complete when it is booked available goes off the run, and the
            # availability system sets that status at the turn of the minute
            md = int(d // 60)
            if md < M and base[md] != 0:
                d = float((md + 1) * 60) if d > md * 60 else float(d)
            events.append((d, "done", None, num))
        events.sort(key=lambda x: (x[0], {"base": 1, "alert": 0, "arrive": 0, "done": 0}[x[1]]))
        base_now, inc_now, phase = 0, None, None
        last = None
        for t, kind, b, num in events:
            if kind == "base":
                base_now = b
            elif kind == "alert":
                inc_now, phase = num, "MB"
            elif kind == "arrive":
                phase = "AT"
            elif kind == "done":
                inc_now, phase = None, None
            if phase is not None:
                state = (phase, 0, inc_now)
            elif base_now == 0:
                state = ("AV", 0, None)
            else:
                state = ("OR", base_now, None)
            if state != last:
                out.append((t, state))
                last = state
        ev[e] = out
    return ev


def status_rows(Wd, sim):
    ev = status_events(Wd, sim)
    rows = []
    hb = 4 * 3600
    for e in range(Wd.nE):
        cs = Wd.engines[e]["call_sign"]
        lst = ev[e]
        jit = K.rng("resend", e)
        allrows = []
        for k, (t, (key, rs, num)) in enumerate(lst):
            allrows.append((t, key, rs, num))
            # the mobilising system re-sends an unchanged status four hours after the engine's last message
            t_next = lst[k + 1][0] if k + 1 < len(lst) else M * 60
            b = t + hb + float(jit.integers(0, 9))
            while b < t_next - 60:
                allrows.append((b, key, rs, num))
                b += hb + float(jit.integers(0, 9))
        allrows.sort(key=lambda x: x[0])
        for t, key, rs, num in allrows:
            code, text = STATUS[key]
            rows.append((t, cs, code, text, REASON.get(rs, "") if key == "OR" else "", num or ""))
    return [(r[0], r[1], "Status", r[2], r[3], r[4], r[5], "", "", "") for r in rows]


# ------------------------------------------------------------------------------------------------- tracking export
def tracking_rows(Wd, sim):
    """Location reports while each engine is out of its base: Left base, a report a minute while moving and every ten
    minutes while stopped, then Arrived base. A stop at the station shorter than a minute is part of the trip."""
    rows = []
    for e, tl in enumerate(sim["T"]):
        home = Wd.home[e]
        sxy = Wd.stations[Wd.engines[e]["station"]]["xy"]
        cs = Wd.engines[e]["call_sign"]
        r = K.rng("gps", e)
        rs = K.rng("gps-speed", e)
        segs = [s for s in tl.seg if s[2] - s[1] >= 1.0]
        base = [s[0] == "stay" and s[3] == home and (s[5] == 0 or np.allclose(s[4], Wd.nodes[home])) for s in segs]
        for k, s in enumerate(segs):            # a short stop at base between two legs of a trip is part of the trip
            if base[k] and s[2] - s[1] < 60 and 0 < k < len(segs) - 1 and not base[k - 1] and not base[k + 1]:
                base[k] = False
        seq = 0
        i = 0
        while i < len(segs):
            if base[i]:
                i += 1
                continue
            j = i
            while j < len(segs) and not base[j]:
                j += 1
            ta, tb = segs[i][1], segs[j - 1][2]
            lb = ta + float(rs.integers(3, 31))
            ep = [(ta, "Left base", sxy, 0.0)]
            for s in segs[i:j]:
                if s[0] == "move":
                    t = s[1] + float(r.integers(45, 76))
                    while t < s[2]:
                        if r.random() > 0.01:                 # a report now and then lost in a signal gap
                            node, pt = tl.where(t, Wd)
                            ep.append((t, "Location", pt + r.normal(0, 0.004, 2), _gps_speed(rs, _speed(Wd, s, t))))
                        t += float(r.integers(45, 76))
                else:
                    t = s[1] if s[1] > ta else s[1] + float(r.integers(540, 661))
                    while t < s[2]:
                        if r.random() > 0.01:
                            ep.append((t, "Location", np.asarray(s[4]) + r.normal(0, 0.004, 2), _gps_speed(rs, 0.0)))
                        t += float(r.integers(540, 661))
            if tb < O.S_YEAR:
                ep.append((tb, "Arrived base", sxy, 0.0))
            ep = [x for x in ep if x[0] < O.S_YEAR and (x[1] != "Location" or ta < x[0] < tb)]
            # the unit registers leaving the station's geofence a few seconds after the engine moves off, before its
            # first report on the road
            first = min([x[0] for x in ep if x[1] == "Location"] + [ta + (tb - ta) / 3.0])
            ep[0] = (min(lb, (ta + first) / 2.0),) + ep[0][1:]
            for t, ev, xy, sp in ep:
                e_, n_ = grid(xy)
                rows.append((t, cs, ev, "", "", "", "", e_, n_, "%.0f" % sp, seq))
                seq += 1
            i = j
    return rows


def log_rows(Wd, sim):
    """The mobilising system's resource log: each engine's status messages (with the four-hourly re-sends) and the
    vehicle location reports its tracking unit sends while the engine is out of its base, in time order."""
    st = [x + (k,) for k, x in enumerate(status_rows(Wd, sim))]
    tr = tracking_rows(Wd, sim)
    rows = [(round(x[0]), x[1], 0, x[10], x) for x in st] + [(round(x[0]), x[1], 1, x[10], x) for x in tr]
    rows.sort(key=lambda z: (z[0], z[1], z[2], z[3]))
    return [(ts_utc(x[0]), x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]) for _t, _c, _k, _s, x in rows]


def _gps_speed(rs, v):
    """The speed the tracking unit reports: the road's pace with the traffic, bends and junctions on it, and a
    standing vehicle's drift."""
    if v <= 0.0:
        return float(rs.integers(1, 4)) if rs.random() < 0.12 else 0.0
    return float(max(2.0, v * rs.normal(0.92, 0.14) + rs.normal(0.0, 2.5)))


def _speed(Wd, s, t):
    path, cum = s[3], s[4]
    el = t - s[6]
    k = int(np.searchsorted(cum, el, side="right")) - 1
    k = min(max(k, 0), len(path) - 2)
    if len(path) < 2:
        return 0.0
    a, b = path[k], path[k + 1]
    dist = np.hypot(*(Wd.nodes[a] - Wd.nodes[b])) * 1000.0
    dt_ = max(cum[k + 1] - cum[k], 1e-6)
    return float(min(110.0, dist / dt_ * 3.6))


# ------------------------------------------------------------------------------------------------- bookings and crew
def booking_rows(Wd, sim):
    code = {i: s["code"] for i, s in enumerate(Wd.stations)}
    bk = sorted(sim["bookings"], key=lambda b: (b["entered"], b["staff"], b["f"]))
    rows = []
    refs = gapped(len(bk), "bookings", 2604100)
    for k, b in zip(refs, bk):
        rows.append(("B%07d" % k, b["staff"], code[b["station"]], ts_local_min(b["f"]), ts_local_min(b["t"]),
                     ts_local_min(b["entered"])))
    return rows


def crew_rows(Wd, sim):
    code = {i: s["code"] for i, s in enumerate(Wd.stations)}
    crew, changes = [], []
    for p in sorted(sim["staff"], key=lambda p: (code[p.station], p.staff)):
        role0 = p.role_hist[0][1]
        drv = "" if p.driver_from is None else (dt.date(2026, 1, 1) + dt.timedelta(days=p.driver_from)).isoformat() \
            if p.driver_from > 0 else _passed(p.staff)
        crew.append((p.staff, code[p.station], p.role_hist[-1][1], "Yes" if p.ba else "No", drv))
        for d0, rl in p.role_hist:
            if d0 > 0:
                changes.append((p.staff, code[p.station], rl, (dt.date(2026, 1, 1) + dt.timedelta(days=d0)).isoformat()))
    return crew, changes


def _passed(staff):
    """The date a driver qualified on the LGV, before 2026."""
    rl = K.rng("lgv", staff)
    y = 2025 - min(int(rl.exponential(5.5)), 20)
    return (dt.date(y, 1, 1) + dt.timedelta(days=int(rl.integers(0, 365)))).isoformat()


# ------------------------------------------------------------------------------------------------- addresses, network
CLASS_R = ["RD02", "RD03", "RD04", "RD06"]
CLASS_C = ["CR", "CO", "CI", "CA", "CE", "CH", "CM", "CC"]


def address_rows(Wd):
    r = K.rng("address-classes")
    n = len(Wd.axy)
    intown = np.array([W.in_town(p) for p in Wd.axy])
    rows = []
    r.integers(1, 40, n)
    Wd.uprn = _uprns(Wd)
    order = np.lexsort((Wd.axy[:, 0], Wd.axy[:, 1]))
    for k, i in enumerate(order):
        if Wd.akind[i] == "V":
            c = "CI"
        elif Wd.akind[i] == "R":
            if intown[i]:
                c = CLASS_R[r.choice(4, p=[0.12, 0.33, 0.33, 0.22])]
            else:
                c = CLASS_R[r.choice(4, p=[0.45, 0.33, 0.17, 0.05])]
        else:
            c = CLASS_C[r.choice(8, p=[0.30, 0.20, 0.15, 0.12, 0.05, 0.05, 0.05, 0.08])] if intown[i] else \
                CLASS_C[r.choice(8, p=[0.10, 0.05, 0.10, 0.55, 0.05, 0.05, 0.03, 0.07])]
        e_, n_ = grid(Wd.axy[i])
        rows.append((int(Wd.uprn[i]), e_, n_, c, Wd.oa21[Wd.aoa[i]]))
    rows.sort()
    return rows


UPRN_FROM = [100090000000, 100071000000, 100062000000, 100080000000, 100121000000, 100110000000, 100100000000]
UPRN_NEW = [10090000000, 10023100000, 10024300000, 10093400000, 10011700000, 10013600000, 10070800000]


def _uprns(Wd):
    """Each address's UPRN as its district council allocated it: the council's own range, the first load numbered
    neighbourhood by neighbourhood, and later builds from the council's newer range."""
    ru = K.rng("uprn")
    out = np.zeros(len(Wd.axy), np.int64)
    for d in range(len(K.DISTRICTS)):
        idx = np.where(Wd.adist == d)[0]
        cell = np.floor(Wd.axy[idx, 0] / 0.8).astype(int) * 10000 + np.floor(Wd.axy[idx, 1] / 0.8).astype(int)
        cells = np.unique(cell)
        rank = dict(zip(ru.permutation(cells).tolist(), range(len(cells))))
        later = ru.random(len(idx)) < 0.07
        o = np.lexsort((Wd.axy[idx, 0], Wd.axy[idx, 1], np.array([rank[c] for c in cell.tolist()])))
        first = idx[o[~later[o]]]
        built = idx[o[later[o]]]
        out[first] = UPRN_FROM[d] + np.cumsum(ru.integers(1, 12, len(first)))
        out[built] = UPRN_NEW[d] + np.cumsum(ru.integers(1, 6, len(built)))
    assert len(np.unique(out)) == len(out) and (out > 0).all()
    return out


def node_ids(Wd):
    if not hasattr(Wd, "_nid"):
        Wd._nid = ["N%05d" % k for k in gapped(Wd.N, "nodes", 10001)]
    return Wd._nid


def node_rows(Wd):
    nid = node_ids(Wd)
    return [(nid[i], *grid(Wd.nodes[i])) for i in range(Wd.N)]


def link_rows(Wd):
    rows = []
    nid = node_ids(Wd)
    lid = gapped(len(Wd.edges), "links", 200001)
    for k, (a, b) in enumerate(Wd.edges):
        rows.append(("L%06d" % lid[k], nid[a], nid[b], str(Wd.cls[k]), int(round(Wd.L[k])),
                     "%.1f" % Wd.drive_s[k], "Y" if Wd.oneway[k] else "N"))
    return rows


# ------------------------------------------------------------------------------------------------- incidents 2022-2026
OLD = {"Primary fire - dwelling": {"Accidental": "F01", "Deliberate": "F02"},
       "Primary fire - other building": "F03", "Primary fire - road vehicle": "F04", "Secondary fire": "F05",
       "Chimney fire": "F06", "False alarm - apparatus": "A01", "False alarm - good intent": "A02",
       "False alarm - malicious": "A03", "Road traffic collision": "S01", "Other special service": "S02"}
NEW = {"Primary fire - dwelling": "PFD", "Primary fire - other building": "PFO", "Primary fire - road vehicle": "PFV",
       "Secondary fire": "SEC", "Chimney fire": "CHM", "False alarm - apparatus": "FAA",
       "False alarm - good intent": "FAG", "False alarm - malicious": "FAM", "Road traffic collision": "RTC",
       "Other special service": "SSO"}
CODES_FROM = dt.datetime(2024, 4, 1)
OA21_FROM = dt.datetime(2023, 4, 1)
FIRES = ("Primary fire - dwelling", "Primary fire - other building", "Primary fire - road vehicle", "Secondary fire",
         "Chimney fire")


def _cause(r, cls):
    if cls == "Primary fire - dwelling":
        u = r.random()
        return "Accidental" if u < 0.86 else ("Deliberate" if u < 0.95 else "Not known")
    if cls in FIRES:
        u = r.random()
        return "Accidental" if u < 0.55 else ("Deliberate" if u < 0.9 else "Not known")
    return ""


def incident_rows(Wd, sim):
    """Every incident 2022 to 2026: 2026's from the year's operations, 2022 to 2025 drawn alike."""
    r = K.rng("incident-records")
    rc = K.rng("incident-closed")
    res = np.where(Wd.akind == "R")[0]
    com = np.where(Wd.akind == "C")[0]
    recs = []
    for I in sim["incidents"]:
        sent = I["sent"]
        closed = max((s["done"] for s in sent), default=I["t"] + 20 * 60)
        recs.append(dict(number=I["number"], call=utc(I["t"]), closed=utc(closed), cls=I["cls"], addr=I["addr"],
                         xy=I["xy"], twin=I["twin"], key=I["number"]))
    shares = np.array([x[1] for x in O.INC_TYPES]); shares /= shares.sum()
    hour_w = np.array([2, 1.5, 1.2, 1, 0.9, 0.9, 1.2, 1.6, 2.0, 2.4, 2.6, 2.8, 3.0, 3.0, 3.0, 3.1, 3.3, 3.6, 3.8, 3.8,
                       3.5, 3.1, 2.6, 2.2])
    for y in (2022, 2023, 2024, 2025):
        n = int(r.normal(4900, 120))
        days = (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
        base = []
        for k in range(n):
            ty = O.INC_TYPES[r.choice(len(O.INC_TYPES), p=shares)]
            where = ty[4]
            if where == "mixed":
                if ty[0] == "False alarm - apparatus":
                    where = "home" if r.random() < 0.3 else "commercial"
                else:
                    where = "home" if r.random() < 0.45 else ("commercial" if r.random() < 0.7 else "road")
            if where == "home":
                a = int(r.choice(res)); xy = Wd.axy[a].copy()
            elif where == "commercial":
                a = int(r.choice(com)); xy = Wd.axy[a].copy()
            else:
                a = None; xy = Wd.nodes[int(r.integers(Wd.N))] + r.normal(0, 0.05, 2)
            t = dt.datetime(y, 1, 1) + dt.timedelta(days=int(r.integers(days)), hours=int(r.choice(24, p=hour_w / hour_w.sum())),
                                                    seconds=int(r.integers(3600)))
            dur = int(r.integers(*ty[3])) + int(r.integers(5, 25))
            base.append(dict(call=t, closed=t + dt.timedelta(minutes=dur, seconds=int(rc.integers(0, 60))), cls=ty[0],
                             addr=a, xy=xy, twin=None, where=where))
        extra = []
        for k, B in enumerate(base):
            if B["cls"] != "False alarm - apparatus" or B["where"] != "commercial":
                continue
            u = r.random()
            if u < O.ASK_C["second_call"]:
                c2 = B["call"] + dt.timedelta(seconds=int(r.integers(120, 540)))
                extra.append(dict(B, call=c2, closed=max(c2 + dt.timedelta(minutes=int(r.integers(8, 20)),
                                                                            seconds=int(rc.integers(0, 60))),
                                                          B["closed"] - dt.timedelta(minutes=int(r.integers(0, 6)),
                                                                                     seconds=int(rc.integers(0, 60)))),
                                  twin=("second call", k)))
            elif u < O.ASK_C["second_call"] + O.ASK_C["again"]:
                c2 = B["closed"] + dt.timedelta(seconds=int(r.integers(60 * 60, 8 * 3600)))
                extra.append(dict(B, call=c2, closed=c2 + dt.timedelta(minutes=int(r.integers(15, 40)),
                                                                     seconds=int(rc.integers(0, 60))),
                                  twin=("again", k)))
        allr = sorted(base + extra, key=lambda B: B["call"])
        for k, B in zip(gapped(len(allr), "inc-%d" % y), allr):
            B["number"] = "%02d/%05d" % (y % 100, k)
            recs.append(B)
    # a second record copies its first's classification and cause; others draw their own
    by_first = {}
    out = []
    recs.sort(key=lambda B: B["call"])
    first_cause = {}
    for B in recs:
        local_call = K.local(B["call"]) if B["call"].year == 2026 else _loc(B["call"])
        local_closed = K.local(B["closed"]) if B["closed"].year == 2026 else _loc(B["closed"])
        cause = _cause(r, B["cls"])
        key = (B["addr"], B["cls"], B["call"].date())
        if B["twin"] is not None and B["twin"][0] == "second call":
            cause = first_cause.get(key, cause)
        first_cause.setdefault(key, cause)
        if B["call"] < CODES_FROM:
            code = OLD[B["cls"]]
            if isinstance(code, dict):
                code = code.get(cause, "F01" if cause == "Not known" else code["Accidental"])
                if cause == "Not known":
                    code = "F07"
            cause_out = ""
        else:
            code = NEW[B["cls"]]
            cause_out = cause
        if B["addr"] is not None:
            uprn = int(Wd.uprn[B["addr"]])
            oa_i = Wd.aoa[B["addr"]]
        else:
            uprn = ""
            oa_i = Wd.aoa[int(np.argmin(((Wd.axy - B["xy"]) ** 2).sum(1)))]
        oa = Wd.oa21[oa_i] if B["call"] >= OA21_FROM else Wd.oa11[oa_i]
        e_, n_ = grid(B["xy"])
        out.append((B["number"], K.stamp(local_call), K.stamp(local_closed), code, cause_out, uprn, e_, n_, oa,
                    B["twin"]))
    return out


def _loc(t):
    y = t.year
    a = dt.datetime.combine(K._last_sunday(y, 3), dt.time(1))
    b = dt.datetime.combine(K._last_sunday(y, 10), dt.time(1))
    return t + dt.timedelta(hours=1) if a <= t < b else t
