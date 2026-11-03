"""The two asks' worlds (recloser operations; crew callouts) and every route through them.

Times inside the world are local wall-clock minutes from 1 October 2020 (no DST jumps); `utc()` converts."""
import numpy as np
import pandas as pd

D0 = pd.Timestamp("2020-10-01")
TZ = "America/Chicago"
Y2 = (pd.Timestamp("2025-10-01") - D0).days
YE = (pd.Timestamp("2026-10-01") - D0).days
RESECT = (pd.Timestamp("2026-06-01") - D0).days
HOLIDAYS = ["2025-11-27", "2025-11-28", "2025-12-24", "2025-12-25", "2026-01-01", "2026-02-16", "2026-05-25",
            "2026-07-03", "2026-09-07"]


def local_ts(minutes):
    return D0 + pd.to_timedelta(np.asarray(minutes, float) * 60, "s")


def utc(minutes):
    lt = pd.DatetimeIndex(local_ts(minutes)).round("ms")
    return lt.tz_localize(TZ, ambiguous=False, nonexistent="shift_forward").tz_convert("UTC").tz_localize(None)


def quarter(ts_local):
    m = pd.DatetimeIndex(ts_local).month
    return np.select([np.isin(m, [10, 11, 12]), np.isin(m, [1, 2, 3]), np.isin(m, [4, 5, 6])], [1, 2, 3], 4)


# ---------------------------------------------------------------- Ask A: recloser operations
def scada(W, F, seed):
    """Operations of reclosing devices in fiscal 2026: substation breakers (whole feeder) and line reclosers (own
    section). Returns the operations frame (local minutes, device, op, seq id, lockout flag) and the truth's
    per-section event list."""
    rng = np.random.default_rng(seed)
    S = W["S"]
    nf = int(S.feeder.max()) + 1
    rcl = S.index[S.device == "RCLR"].values
    rows = []   # (minute, device, op, seq)
    seq = 0
    summer = lambda d: (D0 + pd.Timedelta(days=int(d))).month in (6, 7, 8)
    inst = S.groupby("feeder").inst_trip.first().reindex(range(nf)).fillna(False).values
    feeder_of_rcl = S.feeder.values
    truth_ops = []   # (minute, kind, id, seq, lockout) kind 'B' feeder breaker or 'R' section recloser
    def shots(t0, n, lock=False):
        ivs = [0.5, 2.0, 10.0]
        t = t0; out = [("TRIP", t)]
        k = 4 if lock else n
        for i in range(k - 1 if lock else n):
            t += ivs[min(i, 2)] / 60.0
            out.append(("CLOSE", t))
            if lock or i < n - 1:
                t += rng.uniform(0.05, 0.3) / 60.0
                out.append(("TRIP", t))
        if lock:
            out = out[:7]
        return out
    for d in range(Y2, YE):
        mult = 1.0 + (1.8 if summer(d) else 0.0) + 2.5 * min(W["storm"][d], 3.0) / 3.0
        nb = rng.poisson(0.011 * mult, nf)
        for f in np.repeat(np.arange(nf), nb):
            t0 = d * 1440 + rng.uniform(0, 1440)
            n = rng.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
            seq += 1
            for op, t in shots(t0, n):
                truth_ops.append((t, "B", f, seq, False, op))
        nr = rng.poisson(0.012 * mult, len(rcl))
        for s in np.repeat(rcl, nr):
            t0 = d * 1440 + rng.uniform(0, 1440)
            n = rng.choice([1, 2, 3], p=[0.72, 0.2, 0.08])
            seq += 1
            for op, t in shots(t0, n):
                truth_ops.append((t, "R", s, seq, False, op))
            if inst[feeder_of_rcl[s]] and rng.random() < 0.7:     # the breaker trips with it for the same fault
                seq += 1
                tb = t0 + rng.uniform(0.03, 0.2) / 60.0
                for op, t in shots(tb, 1):
                    truth_ops.append((t, "B", "F%d" % s, seq, False, op))   # feeder resolved at the time below
    # lockouts: each sustained unplanned interruption on a recloser section in the year
    fy = F[(F.level == "section") & ~F.planned & (F.start >= Y2 * 1440) & (F.start < YE * 1440)]
    for r in fy[fy.sec.isin(set(rcl))].itertuples():
        seq += 1
        t0 = r.start - 13.0 / 60.0
        for op, t in shots(t0, 4, lock=True):
            truth_ops.append((t, "R", r.sec, seq, True, op))
        truth_ops.append((r.end, "R", r.sec, seq, True, "CLOSE"))
    O = pd.DataFrame(truth_ops, columns=["t", "kind", "id", "seq", "lockout", "op"])
    # resolve feeder of breaker ops tied to a recloser fault, at the time
    def feeder_at(sec, t):
        return int(S.feeder_new.values[sec]) if t >= RESECT * 1440 else int(S.feeder.values[sec])
    fid = []
    for k, i, t in zip(O.kind.values, O.id.values, O.t.values):
        if k == "B" and isinstance(i, str):
            fid.append(feeder_at(int(i[1:]), t))
        else:
            fid.append(i)
    O["id"] = fid
    O = O[(O.t >= Y2 * 1440) & (O.t < YE * 1440)].sort_values("t").reset_index(drop=True)
    # a member sees two devices within five minutes only for one fault in the same second: other sequences that would
    # reach a member within five minutes of another device's sequence (or the same device's) are not in the world
    first = O.groupby("seq").agg(t=("t", "min"), kind=("kind", "first"), id=("id", "first"), lock=("lockout", "first"))
    def reach(k, i, t):
        if k == "R":
            return {int(i)}
        col = S.feeder_new.values if t >= RESECT * 1440 else S.feeder.values
        return set(np.where(col == int(i))[0])
    seen, keep = {}, set()          # member -> [(time, lockout)]
    order = first.assign(nl=~first.lock).sort_values(["nl", "t"])
    for sq, r in order.iterrows():
        mem = reach(r.kind, r.id, r.t)
        clash = any(abs(r.t - t2) <= 5.0 and not (abs(r.t - t2) < 1.0 / 60 and not (r.lock or l2))
                    for m in mem for t2, l2 in seen.get(m, ()))
        if clash and not r.lock:
            continue
        for m in mem:
            seen.setdefault(m, []).append((r.t, r.lock))
        keep.add(sq)
    return O[O.seq.isin(keep)].reset_index(drop=True)


def feeder_members(S, as_of_new):
    col = "feeder_new" if as_of_new else "feeder"
    return S.groupby(col).members.sum()


def maifi(O, S, route="golden"):
    """MAIFIe by district (0..3) and quarter (1..4) under a route.

    golden: per member, operations of every device upstream at the time within five minutes are one event;
            sequences ending in lockout are not momentary; quarters on local dates; feeders as they stood.
    full:   per member, but feeders as the register stands at year end.
    cracker: per device (five-minute sequences, lockouts out, local quarters), feeders at year end.
    norepair: every trip row an event, lockouts in, UTC quarters, feeders at year end."""
    dist_m = S.groupby("district").members.sum()
    out = np.zeros((4, 4))
    ops = O.copy()
    if route == "norepair":
        tr = ops[ops.op == "TRIP"]
        q = quarter(utc(tr.t.values))
        for k, i, qq in zip(tr.kind.values, tr.id.values, q):
            secs = S.index[S.feeder_new == i] if k == "B" else [i]
            for s in secs:
                out[S.district.values[s], qq - 1] += S.members.values[s]
        return out / dist_m.values[:, None]
    ops = ops[~ops.lockout]
    # sequences: a device's operations within five minutes of the sequence's first trip
    ops = ops[ops.op == "TRIP"].sort_values(["kind", "id", "t"])
    ev = []
    for (k, i), g in ops.groupby(["kind", "id"]):
        start = -1e9
        for t in g.t.values:
            if t - start > 5.0:
                start = t
                ev.append((k, i, t))
    E = pd.DataFrame(ev, columns=["kind", "id", "t"])
    E["q"] = quarter(local_ts(E.t.values))
    if route == "cracker":
        for k, i, qq in zip(E.kind.values, E.id.values, E.q.values):
            secs = S.index[S.feeder_new == i] if k == "B" else [i]
            for s in secs:
                out[S.district.values[s], qq - 1] += S.members.values[s]
        return out / dist_m.values[:, None]
    asof = route == "golden"
    per_sec = {}
    for k, i, t in zip(E.kind.values, E.id.values, E.t.values):
        if k == "B":
            if asof:
                col = S.feeder_new.values if t >= RESECT * 1440 else S.feeder.values
            else:
                col = S.feeder_new.values
            secs = np.where(col == i)[0]
        else:
            secs = [i]
        for s in secs:
            per_sec.setdefault(s, []).append(t)
    for s, ts in per_sec.items():
        ts = sorted(ts)
        start = -1e9
        for t in ts:
            if t - start > 5.0:
                start = t
                qq = quarter(local_ts([t]))[0]
                out[S.district.values[s], qq - 1] += S.members.values[s]
    return out / dist_m.values[:, None]


# ---------------------------------------------------------------- Ask B: crew callouts
CLASSES = {"Line Foreman": 61.42, "Journeyman Lineworker": 55.87, "Apprentice Lineworker (6th step)": 50.28,
           "Apprentice Lineworker (4th step)": 44.69, "Equipment Operator": 46.15}


def crew(W, F, seed):
    """Callout chains for outages that began outside scheduled hours in fiscal 2026, one row per employee per job.
    Returns the rows (truth, before corrections and duplicates are added by pack.py) and the chains."""
    rng = np.random.default_rng(seed)
    S = W["S"]
    emp = []
    for dist in range(4):
        for k in range(12):
            cls = list(CLASSES)[[0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 1, 1][k]]
            emp.append(("E%05d" % int(rng.integers(10000, 99999)), dist, cls, k // 6))
    EMP = pd.DataFrame(emp, columns=["emp", "district", "cls", "crew"]).drop_duplicates("emp")
    fy = F[(F.start >= Y2 * 1440) & (F.start < YE * 1440) & ~F.planned].copy()
    lt = local_ts(fy.start.values)
    after = (lt.hour < 7) | (lt.hour >= 16) | (lt.dayofweek >= 5)
    fy = fy[np.asarray(after)]
    fy = fy[(fy.level == "section") | (rng.random(len(fy)) < 0.95)]
    fy["district"] = S.district.values[fy.sec.values.astype(int)]
    rows, chains = [], []
    cid = 0
    hol = set((pd.Timestamp(h) - D0).days for h in HOLIDAYS)
    for dist in range(4):
        cur = {0: None, 1: None}
        for r in fy[fy.district == dist].sort_values("start").itertuples():
            js = r.start + rng.uniform(18, 40)
            je = max(r.start + r.repair + rng.uniform(8, 20), js + rng.uniform(25, 60))
            placed = False
            for c in (0, 1):
                ch = cur[c]
                if ch is not None and ch["end"] - 240 <= js and js - ch["end"] < 15:
                    s0 = ch["end"] + rng.uniform(3, 13.4)
                    e0 = max(je, s0 + 20)
                    ch["jobs"].append((r.Index, s0, e0)); ch["end"] = e0
                    placed = True
                    break
            if placed:
                continue
            for c in (0, 1):
                if cur[c] is None or js - cur[c]["end"] >= 240:
                    if cur[c] is not None:
                        chains.append(cur[c])
                    cid += 1
                    cur[c] = dict(cid=cid, dist=dist, crew=c, jobs=[(r.Index, js, je)], end=je)
                    break
        for c in (0, 1):
            if cur[c] is not None:
                chains.append(cur[c])
    def ok(ch):
        s = round(ch["jobs"][0][1]); e = round(ch["end"])
        d0, d1 = int(s // 1440), int((e - 1) // 1440)
        m0 = (D0 + pd.Timedelta(days=d0)).month; m1 = (D0 + pd.Timedelta(days=d1)).month
        if m0 != m1 or e >= YE * 1440:
            return False
        if d0 != d1 and ((d0 in hol) != (d1 in hol)):
            return False
        if e - s < 120 and (d0 in hol or d1 in hol):
            return False
        return True
    chains = [ch for ch in chains if ok(ch)]
    for ch in chains:
        team = EMP[(EMP.district == ch["dist"]) & (EMP.crew == ch["crew"])]
        k = 3 if any(F.level.values[F.index.get_loc(j[0])] == "section" for j in ch["jobs"]) else 2
        members = team.sample(n=min(k, len(team)), random_state=int(rng.integers(1 << 30)))
        for ev_i, s0, e0 in ch["jobs"]:
            r = F.loc[ev_i]
            for m in members.itertuples():
                rows.append((m.emp, m.cls, s0, e0, ev_i, "OUTAGE", ch["cid"]))
    R = pd.DataFrame(rows, columns=["emp", "cls", "s", "e", "ev", "wo_type", "chain"])
    R["s"] = np.round(R.s.values); R["e"] = np.round(R.e.values)
    return R, EMP, chains


def _split_by_day(s, e):
    """Minutes of [s, e) on each local date."""
    out = []
    t = s
    while t < e:
        nxt = min(e, (t // 1440 + 1) * 1440)
        out.append((int(t // 1440), nxt - t))
        t = nxt
    return out


def callout_figures(R, route="golden"):
    """Hours and pay by month (1..12 fiscal order: Oct..Sep) under a route.

    golden:   a callout is an employee's chain of jobs with gaps under 15 minutes, from first start to release,
              travel included; restoration work is every job of the chain (capital replacement rows inside an
              outage included); the two-hour minimum per callout; double time on holidays.
    full:     chains, but only outage-order rows (capital rows out, the chain split where they sat).
    cracker:  each row its own callout (minimum per row, row hours only), outage-order rows only.
    norepair: outage-order rows, row hours, time and one-half, no minimum, no holiday."""
    hol = set((pd.Timestamp(h) - D0).days for h in HOLIDAYS)
    hrs = np.zeros(12); pay = np.zeros(12)
    rate = R.cls.map(CLASSES).values
    R = R.assign(rate=rate)
    if route in ("full", "cracker", "norepair"):
        R = R[R.wo_type == "OUTAGE"]
    def fmon(d):
        m = (D0 + pd.Timedelta(days=int(d))).month
        return (m - 10) % 12
    if route in ("cracker", "norepair"):
        for r in R.itertuples():
            mins = r.e - r.s
            for d, mm in _split_by_day(r.s, r.e):
                hrs[fmon(d)] += mm / 60.0
            if route == "norepair":
                pay[fmon(r.s // 1440)] += mins / 60.0 * r.rate * 1.5
                continue
            if mins < 120:
                pay[fmon(r.s // 1440)] += 2.0 * r.rate * 1.5
            else:
                for d, mm in _split_by_day(r.s, r.e):
                    pay[fmon(d)] += mm / 60.0 * r.rate * (2.0 if d in hol else 1.5)
        return hrs, pay
    for emp, g in R.sort_values(["emp", "s"]).groupby("emp"):
        cs, ce, rt = None, None, None
        spans = []
        for r in g.itertuples():
            if cs is not None and r.s - ce < 15:
                ce = max(ce, r.e)
            else:
                if cs is not None:
                    spans.append((cs, ce, rt))
                cs, ce, rt = r.s, r.e, r.rate
        if cs is not None:
            spans.append((cs, ce, rt))
        for cs, ce, rt in spans:
            for d, mm in _split_by_day(cs, ce):
                hrs[fmon(d)] += mm / 60.0
            if ce - cs < 120:
                pay[fmon(cs // 1440)] += 2.0 * rt * 1.5
            else:
                for d, mm in _split_by_day(cs, ce):
                    pay[fmon(d)] += mm / 60.0 * rt * (2.0 if d in hol else 1.5)
    return hrs, pay
