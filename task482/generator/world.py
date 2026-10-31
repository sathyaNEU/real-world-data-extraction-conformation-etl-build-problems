"""task482 architecture 16: Brackwell Alloys' 2026 as it happened. Every process is simulated in UTC on the
works' local calendar; the gas meter sees only the sum of what the processes burned. The truth each family carries
under SCR-2 is kept here and never shipped."""
import datetime as dt
import math
from zoneinfo import ZoneInfo

import numpy as np

import params as P

LON = ZoneInfo(P.TZ)
UTC = dt.timezone.utc
STEP = dt.timedelta(minutes=15)
T0 = dt.datetime(P.YEAR, 1, 1, tzinfo=UTC)
T1 = dt.datetime(P.YEAR + 1, 1, 1, tzinfo=UTC)
N = int((T1 - T0) / STEP)


def loc(t):
    """UTC-aware to naive local wall time."""
    return t.astimezone(LON).replace(tzinfo=None)


def utc(naive):
    """Naive local wall time to UTC-aware (the first of two readings in the autumn hour)."""
    return naive.replace(tzinfo=LON).astimezone(UTC)


def idx(t):
    return int((t - T0) / STEP)


def spread(arr, t_start, t_end, kwh):
    """Add kwh to arr uniformly over [t_start, t_end), split exactly at interval edges."""
    if t_end <= t_start or kwh == 0:
        return
    total = (t_end - t_start).total_seconds()
    i = max(0, idx(t_start))
    while i < N:
        a = T0 + i * STEP
        b = a + STEP
        if a >= t_end:
            break
        lo, hi = max(a, t_start), min(b, t_end)
        if hi > lo:
            arr[i] += kwh * (hi - lo).total_seconds() / total
        i += 1


def shut(d):
    return d in P.SHUT_DAYS


def windows(day_rule):
    """Merge per-day local windows into continuous UTC windows. day_rule(date, prev_shut) -> (h0, h1) or None."""
    out = []
    d = dt.date(P.YEAR, 1, 1)
    cur = None
    while d.year == P.YEAR:
        prev_shut = shut(d - dt.timedelta(days=1))
        w = None if shut(d) else day_rule(d, prev_shut)
        if w:
            a = utc(dt.datetime.combine(d, dt.time()) + dt.timedelta(hours=w[0]))
            b = utc(dt.datetime.combine(d, dt.time()) + dt.timedelta(hours=w[1]))
            if cur and cur[1] == a:
                cur = (cur[0], b)
            else:
                if cur:
                    out.append(cur)
                cur = (a, b)
        else:
            if cur:
                out.append(cur)
            cur = None
        d += dt.timedelta(days=1)
    if cur:
        out.append(cur)
    return out


def casthouse_rule(d, prev_shut):
    """Monday 06:00 to Saturday 14:00; the casthouse's last heats before Christmas are on Saturday 19 December,
    so the homogenizing furnace clears the billet before the works shuts on the 24th."""
    wd = d.weekday()
    if wd == 6 or d >= dt.date(P.YEAR, 12, 20):
        return None
    start = 6.0 if (wd == 0 or prev_shut) else 0.0
    end = 14.0 if wd == 5 else 24.0
    if (d + dt.timedelta(days=1)) in P.SHUT_DAYS and wd != 5:
        end = 22.0            # the casthouse stops for a shutdown at the end of the back shift
    return (start, end)


def foundry_rule(d, prev_shut):
    """Monday to Friday, two shifts; the foundry's last casting day before Christmas is Friday 18 December."""
    if d.weekday() >= 5 or d >= dt.date(P.YEAR, 12, 19):
        return None
    return (6.0, 22.0)


def into_shut(a, b):
    da, db = loc(a).date(), loc(b).date()
    return any(shut(da + dt.timedelta(days=k)) for k in range((db - da).days + 1))


def simulate(seed=P.SEED):
    rng = np.random.default_rng(seed)
    comp = {k: np.zeros(N) for k in ("melt", "m3", "h1", "t1", "pilot", "space")}
    fam_gas = {f: 0.0 for f in P.FAM_CODES}            # truth: gas each family's processes burned (kWh)
    fam_part = {f: {"melt": 0.0, "m3": 0.0, "h1": 0.0, "t1": 0.0} for f in P.FAM_CODES}

    # ---------------------------------------------------------------- weather and space heating
    days = [dt.date(P.YEAR, 1, 1) + dt.timedelta(days=i) for i in range(365)]
    tmean, ar = [], 0.0
    for dday in days:
        doy = dday.timetuple().tm_yday
        ar = 0.72 * ar + rng.normal(0, 1.9)
        tmean.append(10.3 + 6.4 * math.sin(2 * math.pi * (doy - 112) / 365.0) + ar)
    tmean = np.array(tmean)
    for i in range(N):
        t = loc(T0 + i * STEP)
        di = (t.date() - days[0]).days
        h = t.hour + t.minute / 60.0
        temp = tmean[di] + 3.1 * math.sin(2 * math.pi * (h - 9.0) / 24.0)
        comp["space"][i] = P.SPACE_KW_PER_K * max(0.0, P.SPACE_BASE_C - temp) * 0.25
    comp["pilot"][:] = P.PILOT_KW * 0.25

    # ---------------------------------------------------------------- casthouse heats (M1, M2)
    heats = []
    fam_cycle = list(P.CASTHOUSE_MIX)
    probs = np.array([P.CASTHOUSE_MIX[f] for f in fam_cycle])
    heat_no = {"M1": 26001, "M2": 26001}
    for (wa, wb) in windows(casthouse_rule):
        for k, fur in enumerate(("M1", "M2")):
            t = wa + dt.timedelta(hours=0.4 + 2.6 * k + float(rng.uniform(0, 0.5)))
            while True:
                melt_h = max(4.6, rng.normal(*P.HEAT_MELT_H))
                done = t + dt.timedelta(hours=melt_h)
                if done + dt.timedelta(hours=1.2) > wb:
                    break
                fam = fam_cycle[int(rng.choice(len(fam_cycle), p=probs))]
                tonnes = round(float(np.clip(rng.normal(*P.HEAT_T), 33.0, 43.0)), 2)
                gas = P.MELT_KWH_PER_T * tonnes * float(1 + rng.normal(0, 0.05))
                spread(comp["melt"], t, done, gas)
                fam_gas[fam] += gas
                fam_part[fam]["melt"] += gas
                heats.append(dict(furnace=fur, heat=heat_no[fur], family=fam, charged=t, complete=done,
                                  tonnes=tonnes, gas=gas))
                heat_no[fur] += 1
                t = t + dt.timedelta(hours=max(melt_h + 1.6, rng.normal(*P.HEAT_CYCLE_H)))

    # ---------------------------------------------------------------- foundry tower melter (M3)
    m3 = []
    m3_no = 1
    for (wa, wb) in windows(foundry_rule):
        t = wa + dt.timedelta(minutes=int(rng.integers(5, 25)))
        while True:
            tonnes = round(float(np.clip(rng.normal(*P.M3_CHARGE_T), 1.2, 1.9)), 3)
            dur = dt.timedelta(hours=tonnes / P.M3_RATE_T_PER_H)
            if t + dur > wb:
                break
            gas = P.M3_KWH_PER_T * tonnes * float(1 + rng.normal(0, 0.06))
            spread(comp["m3"], t, t + dur, gas)
            fam_gas["CSTLM25"] += gas
            fam_part["CSTLM25"]["m3"] += gas
            m3.append(dict(charge=m3_no, charged=t, tonnes=tonnes, gas=gas, done=t + dur))
            m3_no += 1
            t = t + dur + dt.timedelta(minutes=int(rng.integers(0, 6)))

    # ---------------------------------------------------------------- production lots from the casthouse
    lots = []
    billet_queue = {"BIL6063": [], "BIL6082": []}
    for h in sorted(heats, key=lambda x: x["complete"]):
        good = round(h["tonnes"] / P.YIELD[h["family"]], 3)
        lot = dict(lot="%s-%s%04d" % ("B" if h["family"].startswith("BIL") else "I", h["furnace"], h["heat"] % 10000),
                   family=h["family"], cast=h["complete"] + dt.timedelta(hours=1.3), tonnes=good, heat=h)
        lots.append(lot)
        if h["family"] in billet_queue:
            billet_queue[h["family"]].append([lot["cast"], good, lot])

    # ---------------------------------------------------------------- homogenizing furnace (H1)
    h1 = []
    load_no = 1
    pending = {k: [list(x) for x in v] for k, v in billet_queue.items()}
    t = min(x[0] for q in pending.values() for x in q)
    while any(pending.values()):
        avail = {a: sum(x[1] for x in q if x[0] <= t) for a, q in pending.items()}
        future = [x[0] for q in pending.values() for x in q if x[0] > t]
        cand = [a for a in avail if avail[a] >= 47.5]
        if not cand:
            # a part load only when nothing more will arrive before a shutdown
            if future and not into_shut(t, min(future)):
                t = max(t + STEP, min(future))
                continue
            cand = [a for a in avail if avail[a] > 0]
            if not cand:
                t = min(future)
                continue
        alloy = max(cand, key=lambda a: (avail[a], a))
        cyc = max(5.0, rng.normal(*P.H1_CYCLE_H[alloy]))
        end = t + dt.timedelta(hours=cyc)
        if shut(loc(t).date()) or into_shut(t, end):
            t += dt.timedelta(minutes=30)
            continue
        target = float(np.clip(rng.normal(*P.H1_LOAD_T), 47.5, 52.5))
        q = pending[alloy]
        q.sort(key=lambda x: x[0])
        took, tonnes = [], 0.0
        while q and q[0][0] <= t and tonnes < target - 1e-9:
            take = min(q[0][1], target - tonnes)
            took.append((q[0][2]["lot"], round(take, 3)))
            tonnes += take
            q[0][1] -= take
            if q[0][1] <= 1e-6:
                q.pop(0)
        gas = P.H1_KW * cyc * float(1 + rng.normal(0, 0.03))
        spread(comp["h1"], t, end, gas)
        fam_gas[alloy] += gas
        fam_part[alloy]["h1"] += gas
        h1.append(dict(load=load_no, family=alloy, start=t, end=end, tonnes=round(tonnes, 3), lots=took, gas=gas))
        load_no += 1
        t = end + dt.timedelta(hours=P.H1_TURN_H + float(rng.uniform(0, 0.3)))
        assert loc(t).year == P.YEAR, "the homogenizing furnace ran past the year"

    # ---------------------------------------------------------------- castings and the solution oven (T1)
    cast_lots = []
    by_day = {}
    for c in m3:
        by_day.setdefault(loc(c["charged"]).date(), []).append(c)
    for dday in sorted(by_day):
        cs = by_day[dday]
        for shift, (h0, h1_) in enumerate(((6, 14), (14, 22))):
            melted = sum(c["tonnes"] for c in cs if h0 <= loc(c["charged"]).hour < h1_)
            if melted <= 0:
                continue
            good = round(melted / P.YIELD["CSTLM25"], 3)
            cast_lots.append(dict(lot="C%s%s" % (dday.strftime("%y%m%d"), "AB"[shift]), family="CSTLM25",
                                  cast=utc(dt.datetime.combine(dday, dt.time(h1_ - 1, 30))), tonnes=good))
    lots.extend(cast_lots)
    t1 = []
    queue = [[c["cast"] + dt.timedelta(hours=3), c["tonnes"], c] for c in cast_lots]
    t = min(x[0] for x in queue)
    batch_no = 1
    while queue:
        avail = sum(x[1] for x in queue if x[0] <= t)
        future = [x[0] for x in queue if x[0] > t]
        target = float(np.clip(rng.normal(*P.T1_BATCH_T), 6.0, 7.0))
        if avail < target:
            if future and not into_shut(t, min(future)) and (min(future) - t) < dt.timedelta(hours=20):
                t = max(t + STEP, min(future))
                continue
            if avail <= 0:
                t = min(future)
                continue
            target = avail
        cyc = max(14.0, rng.normal(*P.T1_CYCLE_H))
        end = t + dt.timedelta(hours=cyc)
        if shut(loc(t).date()) or into_shut(t, end):
            t += dt.timedelta(minutes=30)
            continue
        took, tonnes = [], 0.0
        queue.sort(key=lambda x: x[0])
        while queue and queue[0][0] <= t and tonnes < target - 1e-9:
            take = min(queue[0][1], target - tonnes)
            took.append((queue[0][2]["lot"], round(take, 3)))
            tonnes += take
            queue[0][1] -= take
            if queue[0][1] <= 1e-6:
                queue.pop(0)
        gas = P.T1_KW * cyc * float(1 + rng.normal(0, 0.03))
        spread(comp["t1"], t, end, gas)
        fam_gas["CSTLM25"] += gas
        fam_part["CSTLM25"]["t1"] += gas
        t1.append(dict(batch=batch_no, start=t, end=end, tonnes=round(tonnes, 3), lots=took, gas=gas,
                       pieces=int(round(tonnes * 1000 / float(rng.uniform(17.0, 24.0))))))
        batch_no += 1
        t = end + dt.timedelta(minutes=int(rng.integers(30, 90)))
        assert loc(t).year == P.YEAR, "the solution oven ran past the year"

    # ---------------------------------------------------------------- inspection
    insp = []
    h1_end = {}
    for ld in h1:
        for lot, _ in ld["lots"]:
            h1_end[lot] = max(h1_end.get(lot, ld["end"]), ld["end"])
    t1_end = {}
    for b in t1:
        for lot, _ in b["lots"]:
            t1_end[lot] = max(t1_end.get(lot, b["end"]), b["end"])
    produced = {f: 0.0 for f in P.FAM_CODES}
    for lot in lots:
        if lot["family"].startswith("BIL"):
            ready = h1_end[lot["lot"]]
        elif lot["family"] == "CSTLM25":
            ready = t1_end[lot["lot"]]
        else:
            ready = lot["cast"]
        at = ready + dt.timedelta(hours=float(rng.uniform(2.0, 20.0)))
        u = rng.random()
        rows = []
        if u < 0.014:
            rows.append(("REJECT", at))
            final = "REJECT"
        elif u < 0.044:
            rows.append(("REJECT", at))
            rows.append(("PASS", at + dt.timedelta(hours=float(rng.uniform(20, 70)))))
            final = "PASS"
        else:
            rows.append(("PASS", at))
            final = "PASS"
        lot["inspections"] = rows
        lot["final"] = final
        if final == "PASS":
            produced[lot["family"]] += lot["tonnes"]
        for _, when in rows:
            assert loc(when).year == P.YEAR and loc(when).date() < dt.date(P.YEAR, 12, 24), "inspection outside 2026"
    insp = None

    # ---------------------------------------------------------------- the meter
    total = sum(comp.values())
    noise = rng.normal(0, 0.012, N)
    metered = total * (1 + noise)
    base = comp["pilot"] + comp["space"]
    truth = {"fam_gas": fam_gas, "fam_part": fam_part, "produced": produced,
             "process_gas": {k: float(v.sum()) for k, v in comp.items()},
             "metered_kwh": float(metered.sum()), "noise_kwh": float((metered - total).sum()),
             "base_kwh": float(base.sum())}
    return dict(heats=heats, m3=m3, h1=h1, t1=t1, lots=lots, comp=comp, metered=metered, tmean=tmean, days=days,
                truth=truth, rng=rng)


def family_truth(w):
    """SCR-2 on the world: each family's own process gas, plus the gas no process burned (pilots, space heating
    and the meter's own noise) shared by the tonnes produced; tonnes of CO2 per tonne."""
    tr = w["truth"]
    prod = tr["produced"]
    allp = sum(prod.values())
    shared = tr["metered_kwh"] - sum(tr["fam_gas"].values())
    out = {}
    for f in P.FAM_CODES:
        kwh = tr["fam_gas"][f] + shared * prod[f] / allp
        out[f] = kwh * P.CO2_KG_PER_KWH / 1000.0 / prod[f]
    return out
