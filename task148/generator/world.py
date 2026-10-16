"""The clean truth: every 911 call presented to the agency from 1 January 2025 to 30 September 2026, the floor roster,
the queue each call met, the location records of the north-east's wireless calls, the callback desk's tasks and the
administrative line. Nothing here is a file; records.py writes the exports from it.

Arrivals are Poisson by clock hour. Each caller's patience and each answered call's busy time (answer to ready) are
exponential and independent of everything else, the patience's mean set by the hour's call mix (common.patience_mean:
about two minutes on Friday and Saturday nights from 22:00 to 06:00, about ten the rest of the week); one in five of the
callers who hang up redial, most within a minute (common.REDIAL_P and REDIAL_DELAY). Calls are answered first
come, first served by the call-takers on the floor in the roster's block."""
from __future__ import annotations

import datetime as dt
import heapq
import math

import numpy as np

import common as K
import geo as G
import levels as LV

KINDS = ["wireless", "voip", "residence", "business", "mlts", "telematics"]
KIND_P = [0.748, 0.083, 0.099, 0.042, 0.016, 0.012]
XFER_IN_P = 0.024
XFER_IN_FROM = [("wexley", 0.45), ("patrol", 0.35), ("hollin", 0.12), ("garrick", 0.08)]
CB_KEY = "cbtask-9"    # the callback desk's stream (stamp lags, dial delays): one whose monthly shares sit off
                       # whole numbers and one-decimal rounding edges, both asserted in checks.py
BOX_P = 0.087                                       # a wireless call's chance of falling in the north-east box
AREA_P = [("main", 0.300), ("detached", 0.034), ("tamsen", 0.120), ("tavish", 0.440), ("wexley", 0.106)]
XFER_OUT = {"main": 0.92, "detached": 0.92, "wexley": 0.96}
WEX_ALT = 0.12                                      # share of Wexley transfers landing on its alternate
OTHER_OUT = [("patrol", 0.0040), ("garrick", 0.0025), ("hollin", 0.0030)]
GARRICK_ALT = 0.15


def lam_hist(loc):
    """Expected 911 calls presented in the clock hour starting at local time loc."""
    h = loc.hour
    nd = K.night_of(loc)
    if K.is_frisat_late(loc):
        return LV.LATE_LEVEL[nd.month] * K.HOUR_PROFILE[h] * K.NIGHT_FACTOR[nd.weekday()] * K.trend(nd)
    wd = loc.weekday()
    base = K.WEEKDAY[h]
    if wd in (4, 5) and 14 <= h < 22:
        base *= 1.06
    elif wd == 6 and h < 12:
        base *= 0.93
    return base * K.SEAS[loc.month] * K.trend(loc.date())


class World:
    pass


def _roster(W):
    """Call-takers on the floor by (date, block): the plan, a call-taker short where a sick call was not backfilled,
    one over on holiday overtime."""
    ros = {}
    d = K.HIST_START.date() - dt.timedelta(days=1)
    while d < K.HIST_END.date():
        for blk in [b[2] for b in K.BLOCKS] + [K.LATE_BLOCK]:
            r = K.rng("roster", d.isoformat(), blk)
            c = K.plan_c(d, blk)
            u = r.random()
            note = ""
            if u < 0.035 and blk == K.LATE_BLOCK and d.weekday() in (4, 5):
                note = "sick call, grant position backfilled on overtime"
            elif u < 0.035:
                c -= 1
                note = "sick call, not backfilled"
            elif u > 0.986:
                c += 1
                note = "overtime"
            ros[(d, blk)] = (c, note)
        d += dt.timedelta(days=1)
    W.roster = ros


def _sample_point(r, area):
    """A caller's true location (km) in an area of the box, at least 150 m from every township edge."""
    x0, y0, x1, y1 = G.BOX
    bounds = {"main": (0, -0.4, 9.6, 9.4), "detached": (6.6, 10.4, 9.6, 12.9), "tamsen": (4.0, 2.6, 7.0, 5.3),
              "tavish": (x0, y0, G.COUNTY_LINE_X, y1), "wexley": (G.COUNTY_LINE_X + 0.15, y0, x1, y1)}[area]
    for _ in range(10000):
        x = r.uniform(bounds[0], bounds[2])
        y = r.uniform(bounds[1], bounds[3])
        if G.area_of(x, y) != area:
            continue
        if G.edge_dist_km(x, y) < 0.15:
            continue
        return x, y
    raise RuntimeError(area)


def _sector_for(r, x, y):
    d = sorted(((math.hypot(x - sx, y - sy), i) for i, (_, sx, sy, _) in enumerate(G.SECTORS)))[:4]
    w = np.array([1.0 / (dd * dd + 1.0) for dd, _ in d])
    return d[int(r.choice(len(d), p=w / w.sum()))][1]


def simulate():
    W = World()
    _roster(W)
    t0 = K.HIST_START.astimezone(K.UTC).timestamp()
    tend = K.HIST_END.astimezone(K.UTC).timestamp()
    nh = int(round((tend - t0) / 3600))
    W.t0, W.nh = t0, nh
    # call-takers on duty by UTC hour index
    ch = np.zeros(nh, dtype=int)
    for k in range(nh):
        loc = K.to_local(t0 + 3600 * k)
        ch[k] = W.roster[K.block_of(loc)][0]
    W.chour = ch
    # ------------------------------------------------------------------ first calls
    arrivals = []          # (t, caller, kind, xfer_in, area, patience, busy, talk_frac, redial_no)
    caller = 0
    for k in range(nh):
        loc = K.to_local(t0 + 3600 * k)
        lam = lam_hist(loc)
        r = K.rng("arr", k)
        n = int(r.poisson(lam))
        ts = np.sort(r.uniform(0, 3600, n)) + t0 + 3600 * k
        kinds = r.choice(len(KINDS), size=n, p=KIND_P)
        xin = r.random(n) < XFER_IN_P
        xsrc = r.choice(len(XFER_IN_FROM), size=n, p=[p for _, p in XFER_IN_FROM])
        inbox = r.random(n) < BOX_P
        area = r.choice(len(AREA_P), size=n, p=[p for _, p in AREA_P])
        pat = r.exponential(K.patience_mean(loc), n)
        busy = r.exponential(K.AHT, n)
        talk = r.beta(*K.TALK_BETA, n)
        for i in range(n):
            kd = KINDS[kinds[i]]
            xi = XFER_IN_FROM[xsrc[i]][0] if xin[i] else ""
            ar = AREA_P[area[i]][0] if (kd == "wireless" and not xi and inbox[i]) else ""
            arrivals.append((float(ts[i]), caller, kd, xi, ar, float(pat[i]), float(busy[i]), float(talk[i]), 0))
            caller += 1
    W.n_callers = caller
    # ------------------------------------------------------------------ the queue, first come first served
    CMAX = int(ch.max()) + 1
    nxt_on = []
    chl = ch.tolist()
    for j in range(CMAX):
        nx = [nh] * (nh + 1)
        for k in range(nh - 1, -1, -1):
            nx[k] = k if chl[k] > j else nx[k + 1]
        nxt_on.append(nx)
    free = [t0] * CMAX
    heap = [(a[0], idx, a) for idx, a in enumerate(arrivals)]
    heapq.heapify(heap)
    seq = len(arrivals)
    calls = []
    while heap:
        _, _, a = heapq.heappop(heap)
        t, cid, kd, xi, ar, p, s, tf, rd = a
        bs, best = 1e30, -1
        for j in range(CMAX):
            f = free[j]
            st = f if f > t else t
            kk = int((st - t0) // 3600)
            if kk >= nh:
                kk = nh - 1
            k2 = nxt_on[j][kk]
            if k2 != kk:
                st = t0 + 3600.0 * k2
            if st < bs:
                bs, best = st, j
                if st <= t:
                    break
        w = bs - t
        if w > p:
            calls.append((t, cid, kd, xi, ar, p, s, tf, rd, 1, p, -1))
            rr = K.rng("redial", cid, rd)
            if rr.random() < K.REDIAL_P:
                tr = t + p + K.REDIAL_DELAY[0] + rr.exponential(K.REDIAL_DELAY[1])
                if tr < tend:
                    na = (tr, cid, kd, "", ar, float(rr.exponential(K.patience_mean(K.to_local(tr)))),
                          float(rr.exponential(K.AHT)), float(rr.beta(*K.TALK_BETA)), rd + 1)
                    heapq.heappush(heap, (tr, seq, na))
                    seq += 1
        else:
            calls.append((t, cid, kd, xi, ar, p, s, tf, rd, 0, w, best))
            free[best] = bs + s
    calls.sort(key=lambda c: (c[0], c[1], c[8]))
    n = len(calls)
    W.N = n
    W.t = np.array([c[0] for c in calls])
    W.caller = np.array([c[1] for c in calls], dtype=np.int64)
    W.kind = np.array([c[2] for c in calls], dtype=object)
    W.xin = np.array([c[3] for c in calls], dtype=object)
    W.area = np.array([c[4] for c in calls], dtype=object)
    W.patience = np.array([c[5] for c in calls])
    W.busy = np.array([c[6] for c in calls])
    W.talkf = np.array([c[7] for c in calls])
    W.redial = np.array([c[8] for c in calls], dtype=np.int64)
    W.ab = np.array([c[9] for c in calls], dtype=bool)
    W.wait = np.array([c[10] for c in calls])
    W.server = np.array([c[11] for c in calls], dtype=np.int64)
    W.ans_t = np.where(W.ab, np.nan, W.t + W.wait)
    W.rel_t = np.where(W.ab, np.nan, W.ans_t + W.busy * W.talkf)
    W.ready_t = np.where(W.ab, np.nan, W.ans_t + W.busy)
    W.hang_t = np.where(W.ab, W.t + W.wait, np.nan)
    W.hour = ((W.t - t0) // 3600).astype(np.int64)
    _transfers_out(W)
    _positions(W)
    _tests(W)
    _locations(W)
    _admin(W)
    _escalations(W)
    _callbacks(W)
    _cad(W)
    return W


def _transfers_out(W):
    out = np.full(W.N, "", dtype=object)
    alt = np.zeros(W.N, dtype=bool)
    xat = np.full(W.N, np.nan)
    for i in range(W.N):
        if W.ab[i]:
            continue
        r = K.rng("xout", int(W.caller[i]), int(W.redial[i]))
        u = r.random()
        ar = W.area[i]
        dest = ""
        if ar in XFER_OUT:
            if u < XFER_OUT[ar]:
                dest = "wexley"
        elif not ar and not W.xin[i]:
            acc = 0.0
            for d, p in OTHER_OUT:
                acc += p
                if u < acc:
                    dest = d
                    break
        if dest:
            out[i] = dest
            v = r.random()
            alt[i] = (dest == "wexley" and v < WEX_ALT) or (dest == "garrick" and v < GARRICK_ALT)
            xat[i] = W.ans_t[i] + W.busy[i] * W.talkf[i] * r.uniform(0.25, 0.8)
    W.xout, W.xout_alt, W.xout_t = out, alt, xat


def _positions(W):
    """The position each answered call was delivered to: server slots map to the positions staffed that block."""
    pos = np.full(W.N, "", dtype=object)
    cache = {}
    for i in range(W.N):
        if W.ab[i]:
            continue
        loc = K.to_local(W.ans_t[i])
        b = K.block_of(loc)
        if b not in cache:
            r = K.rng("seats", b[0].isoformat(), b[1])
            cache[b] = ["CT%02d" % x for x in r.permutation(np.arange(1, 13))]
        pos[i] = cache[b][int(W.server[i]) % 12]
    W.position = pos


def _tests(W):
    """Test calls: ESInet test responder calls on i3 and CAMA trunk tests before the cutover, answered by the
    responder or the test position, never by a call-taker."""
    tests = []
    d = K.HIST_START.date()
    while d < K.HIST_END.date():
        r = K.rng("tests", d.isoformat())
        n = int(r.poisson(2.6))
        for _ in range(n):
            sec = float(r.uniform(0, 86400))
            loc = dt.datetime(d.year, d.month, d.day, tzinfo=K.TZ) + dt.timedelta(seconds=sec)
            ts = loc.astimezone(K.UTC).timestamp()
            if ts >= K.HIST_END.astimezone(K.UTC).timestamp():
                continue
            dur = float(r.uniform(6, 15))
            tests.append((ts, dur, int(r.integers(1, 10 ** 9))))
        d += dt.timedelta(days=1)
    W.tests = sorted(tests)


def _locations(W):
    """For wireless calls in the north-east box: the true handset location, the routing sector and the location
    records the call-handling system stored (the routing location, then the handset fixes)."""
    loc_true = {}
    recs = {}
    for i in np.nonzero(W.area != "")[0]:
        cid = int(W.caller[i])
        if cid not in loc_true:
            r = K.rng("where", cid)
            x, y = _sample_point(r, W.area[i])
            loc_true[cid] = (x, y, r.random())
        x, y, u = loc_true[cid]
        r = K.rng("loc", cid, int(W.redial[i]))
        si = _sector_for(r, x, y)
        sid, sx, sy, srad = G.SECTORS[si]
        rows = [("cell", W.t[i] + r.uniform(0.2, 1.4), sx, sy, srad, 90)]
        n_fix = 1
        if not W.ab[i] and W.rel_t[i] - W.ans_t[i] >= 40.0:
            n_fix += int(r.choice([0, 1, 2], p=[0.35, 0.45, 0.20]))
        last = W.t[i]
        for f in range(n_fix):
            if f == 0:
                when = W.t[i] + r.uniform(2.0, 12.0)
                method = "device" if r.random() < 0.7 else "gnss"
                rad = float(r.uniform(9, 48)) if method == "device" else float(r.uniform(5, 22))
            else:
                lo = max(last + 5.0, W.ans_t[i] + 15.0)
                hi = max(lo + 1.0, W.rel_t[i] - 1.0)
                when = r.uniform(lo, hi)
                method = "gnss"
                rad = float(r.uniform(4, 18))
            for _ in range(100):
                ang = r.uniform(0, 2 * math.pi)
                dist = abs(r.normal(0, rad / 2.5)) / 1000.0
                fx, fy = x + dist * math.cos(ang), y + dist * math.sin(ang)
                if G.area_of(fx, fy) == W.area[i] and G.edge_dist_km(fx, fy) >= 0.05:
                    break
            else:
                fx, fy = x, y
            rows.append((method, when, fx, fy, rad, int(r.integers(68, 96))))
            last = when
        recs[i] = (sid, rows)
    W.loc_true = loc_true
    W.locrecs = recs


def _admin(W):
    """The administrative (non-emergency) line, answered at the admin desk: its own ACD queue."""
    rows = []
    t0, tend = W.t0, K.HIST_END.astimezone(K.UTC).timestamp()
    prof = [1.2, 0.9, 0.7, 0.6, 0.5, 0.6, 1.4, 3.1, 5.6, 7.4, 8.1, 8.3, 7.9, 7.6, 7.8, 7.7, 7.1, 6.2, 4.9, 4.1, 3.4,
            2.8, 2.1, 1.6]
    k = 0
    while t0 + 3600 * k < tend:
        loc = K.to_local(t0 + 3600 * k)
        r = K.rng("admin", k)
        n = int(r.poisson(prof[loc.hour] * (0.8 if loc.weekday() >= 5 else 1.0)))
        for ts in np.sort(r.uniform(0, 3600, n)) + t0 + 3600 * k:
            w = float(r.exponential(31.0))
            p = float(r.exponential(150.0))
            if w > p:
                rows.append((float(ts), p, 1, 0.0, int(r.integers(1, 10 ** 9)), -1))
            else:
                rows.append((float(ts), w, 0, float(r.exponential(165.0)), int(r.integers(1, 10 ** 9)), -1))
        k += 1
    W.admin = rows


ESC_P = 0.12       # a 911 abandon whose caller had just given up on the administrative line


def _escalations(W):
    """Callers who gave up waiting on the administrative line and dialled 911 within a couple of minutes, then hung
    up on 911 too: the administrative-line call (abandoned) precedes the 911 call from the same number. Only the
    callback window (January to June 2026) is drawn; the administrative line's export carries the call like any
    other."""
    lo = dt.datetime(2026, 1, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp()
    hi = dt.datetime(2026, 7, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp()
    extra = []
    for i in np.nonzero(W.ab)[0]:
        if not (lo + 600 <= W.t[i] < hi - 600) or W.wait[i] <= 5.0 or W.xin[i]:
            continue
        r = K.rng("escalate", int(i))
        if r.random() >= ESC_P:
            continue
        gap = float(r.uniform(60.0, 150.0))
        w = float(r.uniform(15.0, 45.0))
        extra.append((float(W.t[i]) - gap, w, 1, 0.0, 0, int(W.caller[i])))
    W.admin = sorted(W.admin + extra, key=lambda a: (a[0], a[5]))
    W.n_escalations = len(extra)


def _callbacks(W):
    """The callback desk's tasks for abandoned 911 calls and abandoned administrative-line calls hung up from
    1 January to 30 June 2026 (local). A repeat abandon from a number whose task has not dialled yet joins that
    task. A task is stamped when the callback module takes the abandon, 1 to 21 seconds after the hang-up; the first
    dial follows the desk's queue, abandons shorter than 5 seconds queued behind the others; a task whose caller gets
    through on a redial before the first dial closes without a dial."""
    lo = dt.datetime(2026, 1, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp()
    hi = dt.datetime(2026, 7, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp()
    ev = []    # (hang time, line, index)
    for i in np.nonzero(W.ab)[0]:
        if lo <= W.hang_t[i] < hi:
            ev.append((float(W.hang_t[i]), "911", int(i)))
    for j, a in enumerate(W.admin):
        if a[2] == 1 and lo <= a[0] + a[1] < hi:
            ev.append((a[0] + a[1], "ADMIN", j))
    ev.sort()
    # answered calls per number (to auto-close a task when the caller gets through)
    answered_by_caller = {}
    for i in np.nonzero(~W.ab)[0]:
        if lo - 3600 <= W.t[i] < hi + 3600:
            answered_by_caller.setdefault(int(W.caller[i]), []).append(float(W.t[i]))
    open_tasks = {}     # number key -> task index (not yet dialled)
    tasks = []
    member = {}         # (line, index) -> task index
    for th, line, idx in ev:
        if line == "911":
            key = ("C", int(W.caller[idx]))
        else:
            key = ("C", W.admin[idx][5]) if W.admin[idx][5] >= 0 else ("A", W.admin[idx][4])
        tk = open_tasks.get(key)
        if tk is not None and tasks[tk]["first_dial"] is not None and tasks[tk]["first_dial"] <= th:
            tk = None
        if tk is not None and tasks[tk]["closed_nodial"] is not None and tasks[tk]["closed_nodial"] <= th:
            tk = None
        if tk is not None:
            tasks[tk]["members"].append((line, idx, th))
            member[(line, idx)] = tk
            continue
        r = K.rng(CB_KEY, line, idx)
        lag = 1.0 + float(r.uniform(0.0, 20.0))     # the module polls the call-handling system every 20 seconds
        created = th + lag
        if line == "911":
            short = W.wait[idx] <= 5.0
        else:
            short = W.admin[idx][1] <= 5.0
        loc = K.to_local(th)
        night = 1.25 if (loc.hour >= 23 or loc.hour < 6) else 1.0
        if short:
            delay = 45.0 + r.gamma(2.2, 52.0) * night
        else:
            delay = 14.0 + r.gamma(2.2, 40.0) * night
        fd = created + delay
        # keep every dial clear of the two-minute mark for the call that opened the task
        while abs((fd - th) - 120.0) < 1.5:
            fd += 3.0
        # auto-close when the caller gets through first
        closed_nodial = None
        if line == "911":
            for ta in answered_by_caller.get(int(W.caller[idx]), []):
                if th < ta < fd:
                    closed_nodial = ta
                    break
        task = {"line": line, "opener": idx, "created": created, "first_dial": None if closed_nodial else fd,
                "closed_nodial": closed_nodial, "members": [(line, idx, th)], "seed": int(r.integers(1, 10 ** 9))}
        tasks.append(task)
        open_tasks[key] = len(tasks) - 1
        member[(line, idx)] = len(tasks) - 1
    # members that joined a task: the first dial must be clear of their own two-minute mark too
    for task in tasks:
        if task["first_dial"] is None:
            continue
        for _ in range(20):
            bad = [m for m in task["members"] if abs((task["first_dial"] - m[2]) - 120.0) < 1.5
                   or 0.0 <= task["first_dial"] - m[2] < 2.0]
            if not bad:
                break
            task["first_dial"] += 3.0
        r = K.rng("cbres", task["seed"])
        task["attempts"] = int(r.choice([1, 2, 3], p=[0.62, 0.27, 0.11]))
        task["result"] = str(r.choice(["reached", "no answer", "voicemail", "busy"], p=[0.58, 0.24, 0.13, 0.05]))
        task["closed"] = task["first_dial"] + float(r.uniform(20, 400)) + 180 * (task["attempts"] - 1)
    for task in tasks:
        if task["first_dial"] is None:
            task["attempts"] = 0
            task["result"] = "caller called in"
            task["closed"] = task["closed_nodial"]
    W.cb_tasks = tasks
    W.cb_member = member
    W.cb_window = (lo, hi)


def _cad(W):
    """CAD incidents opened from 911 calls answered on Friday and Saturday late shifts in fiscal 2026."""
    lo = dt.datetime(2025, 7, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp()
    hi = dt.datetime(2026, 7, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp()
    types = [("MEDICAL", 0.31, 2), ("TRAFFIC CRASH", 0.12, 2), ("DISTURBANCE", 0.11, 2), ("WELFARE CHECK", 0.08, 3),
             ("ASSAULT", 0.05, 1), ("FIRE ALARM", 0.04, 2), ("SUSPICIOUS", 0.09, 3), ("INTOX PERSON", 0.07, 3),
             ("DOMESTIC", 0.06, 1), ("NOISE", 0.05, 4), ("STRUCTURE FIRE", 0.02, 1)]
    rows = []
    for i in np.nonzero(~W.ab)[0]:
        if not (lo <= W.t[i] < hi):
            continue
        loc = K.to_local(W.t[i])
        if not K.is_frisat_late(loc):
            continue
        r = K.rng("cad", int(i))
        if r.random() > 0.72:
            continue
        ti = int(r.choice(len(types), p=[x[1] for x in types]))
        created = W.ans_t[i] + float(r.uniform(25, 110))
        disp = created + float(r.gamma(2.0, 40.0)) * (1 if types[ti][2] <= 2 else 2.2)
        rows.append((int(i), types[ti][0], types[ti][2], created, disp, int(r.integers(1, 4))))
    W.cad = rows
