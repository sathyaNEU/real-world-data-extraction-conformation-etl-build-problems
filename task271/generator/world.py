"""task271 world: the clean truth before any export writes it.

Every angling party on every lake on every day of the 2026 open-water season (15 May to 31 August) is simulated: when
it started and finished, from a boat or from shore, how many anglers, what it caught. The survey then observes that
world the way the society's protocol does: two Vellacott Air count loops on each survey day, each lake passed at the
time its place on the route brings the aircraft over it, and a clerk at one lake's main access on each interview day
who interviews the parties that leave by it. Nothing is placed for anyone to catch: the anglers fish when anglers on
that kind of lake fish, and the counts fall when the route brings the aircraft over.

The ask organs (the hatchery's release trips and raceway samples, the temperature loggers, the charter flights) are
simulated here too, each from its own process."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# ------------------------------------------------------------------------------------------------- lakes
# code, name, class, area (ha), designed season angler-hours per hectare, route position (Vellacott lake number),
# elevation (m), access, campground, launch, main-access share of parties, Vellacott's own lake name spelling
LAKES = [
    ("PP-03", "Tessaly Lake", "general", 31.4, 820, 4, 1185, "paved", "yes", "concrete ramp", 0.46),
    ("PP-07", "Kesterway Lake", "general", 46.2, 760, 9, 1240, "gravel", "yes", "concrete ramp", 0.42),
    ("PP-11", "Brackwater Lake", "general", 27.9, 700, 7, 1150, "paved", "yes", "concrete ramp", 0.50),
    ("PP-14", "Galloran Lake", "general", 18.6, 400, 10, 1210, "gravel", "yes", "gravel ramp", 0.92),
    ("PP-18", "Nockell Lake", "general", 35.8, 404, 12, 1265, "gravel", "yes", "gravel ramp", 0.90),
    ("PP-22", "Ostrum Lake", "general", 22.4, 242, 13, 1195, "paved", "yes", "concrete ramp", 0.88),
    ("PP-24", "Farrowdale Lake", "general", 51.2, 331, 11, 1230, "gravel", "yes", "gravel ramp", 0.86),
    ("PP-27", "Pillory Lake", "general", 26.3, 205, 18, 1290, "gravel", "no", "gravel ramp", 0.90),
    ("PP-31", "Saddlebank Lake", "general", 33.1, 206, 21, 1320, "4x4", "no", "car-top", 0.93),
    ("PP-33", "Copperjack Lake", "general", 19.8, 227, 15, 1275, "gravel", "yes", "gravel ramp", 0.90),
    ("PP-05", "Ellerdine Lake", "fly", 24.9, 595, 5, 1305, "gravel", "yes", "gravel ramp", 0.45),
    ("PP-09", "Quorrin Lake", "fly", 29.6, 678, 6, 1340, "gravel", "yes", "gravel ramp", 0.40),
    ("PP-16", "Ravensky Lake", "fly", 17.3, 818, 16, 1380, "4x4", "no", "car-top", 0.47),
    ("PP-20", "Inverkeld Lake", "fly", 21.8, 800, 19, 1355, "gravel", "yes", "gravel ramp", 0.44),
    ("PP-26", "Kittiwake Lake", "fly", 15.6, 1150, 2, 1295, "paved", "yes", "concrete ramp", 0.38),
    ("PP-29", "Mosswater Lake", "fly", 30.9, 205, 22, 1410, "4x4", "no", "car-top", 0.92),
    ("PP-35", "Driftpine Lake", "fly", 23.7, 235, 24, 1425, "walk-in", "no", "none", 0.95),
    ("PP-37", "Merganser Lake", "fly", 12.4, 165, 23, 1395, "walk-in", "no", "none", 0.95),
    ("PP-02", "Corriemore Lake", "quality", 19.2, 760, 3, 1260, "gravel", "yes", "gravel ramp", 0.55),
    ("PP-12", "Pinewhistle Lake", "quality", 22.0, 790, 8, 1285, "gravel", "yes", "gravel ramp", 0.50),
    ("PP-19", "Kelloran Lake", "quality", 25.3, 278, 14, 1310, "gravel", "no", "gravel ramp", 0.90),
    ("PP-28", "Bufflehead Lake", "quality", 54.8, 300, 17, 1345, "gravel", "yes", "gravel ramp", 0.88),
    ("PP-30", "Canvasback Lake", "quality", 21.4, 290, 20, 1330, "4x4", "no", "car-top", 0.91),
    ("PP-34", "Thornhollow Lake", "quality", 47.9, 260, 1, 1220, "paved", "yes", "concrete ramp", 0.90),
]
REG_TEXT = {"general": "General", "fly": "Fly fishing only", "quality": "Electric motor only; single barbless hook"}

# when each class's parties fish: (centre, sd, weight, mean duration h); centres given as clock hours, or tied to
# sunrise ("sr+x") or sunset ("ss-x")
PROFILE = {
    "general": [("sr+2.2", 1.0, 0.08, 3.0), (10.8, 0.95, 0.50, 3.4), (14.0, 1.15, 0.34, 3.2), ("ss-3.0", 1.0, 0.08, 2.6)],
    "fly": [("sr+0.55", 0.55, 0.39, 2.6), (11.8, 2.0, 0.22, 3.2), ("ss-2.4", 0.8, 0.39, 2.8)],
    "quality": [("sr+1.2", 0.8, 0.27, 2.9), (11.2, 1.7, 0.43, 3.3), ("ss-2.8", 1.0, 0.30, 2.8)],
}
BOAT_SIZE = {"general": (2.4, 6), "fly": (1.6, 3), "quality": (1.9, 4)}   # mean anglers per boat party, cap
SHORE_SHARE = {"general": 0.30, "fly": 0.07, "quality": 0.15}
DAYTYPE_F = {"weekday": 1.0, "weekend": 1.85}
MONTH_F = {5: 0.82, 6: 1.12, 7: 1.08, 8: 0.94}
CPUE = {"general": 0.62, "fly": 0.48, "quality": 0.41}    # rainbow trout caught per angler-hour
KEEP = {"general": 0.58, "fly": 0.20, "quality": 0.04}    # share of caught fish kept (quotas and habits)
CLIPPED = {"general": 0.78, "fly": 0.55, "quality": 0.36} # hatchery share of kept fish


def _centre(spec, sr, ss):
    if isinstance(spec, str):
        base = sr if spec.startswith("sr") else ss
        return base + float(spec[2:])
    return spec


def lake_jitter():
    g = K.rng_for("jitter")
    return {L[0]: (g.normal(0, 0.18), g.normal(0, 0.025)) for L in LAKES}


def weather():
    """one draw per day, shared by every lake: cool wet days and the August smoke keep anglers home"""
    g = K.rng_for("weather")
    f = {}
    for d in K.SEASON_DAYS:
        x = math.exp(g.normal(0, 0.16))
        if dt.date(2026, 8, 10) <= d <= dt.date(2026, 8, 16):
            x *= 0.72          # wildfire smoke settled on the plateau
        f[d] = x
    return f


def party_hours_mean(cls):
    """expected angler-hours per party, by a fixed Monte Carlo draw"""
    g = K.rng_for("ph", cls)
    d = dt.date(2026, 7, 1)
    sr, ss = K.sun_times(d)
    tot = 0.0
    n = 40000
    comps = PROFILE[cls]
    w = np.array([c[2] for c in comps])
    k = g.choice(len(comps), size=n, p=w / w.sum())
    for idx in range(len(comps)):
        m = k == idx
        cen = _centre(comps[idx][0], sr, ss)
        st = np.clip(g.normal(cen, comps[idx][1], m.sum()), K.DAY_OPEN, K.DAY_CLOSE - 0.6)
        du = np.clip(g.lognormal(math.log(comps[idx][3]) - 0.06, 0.35, m.sum()), 0.6, 9)
        en = np.minimum(st + du, K.DAY_CLOSE)
        shore = g.random(m.sum()) < SHORE_SHARE[cls]
        mu, cap = BOAT_SIZE[cls]
        size = np.where(shore, g.choice([1, 1, 1, 2, 2, 3], m.sum()), np.clip(g.poisson(mu - 1, m.sum()) + 1, 1, cap))
        tot += float(np.sum((en - st) * size))
    return tot / n


def simulate_trips():
    """every party on every lake on every season day; each day's party count and each party's attributes come from
    their own streams, so a lake's level can be set without reshuffling the parties already drawn"""
    from scipy.stats import poisson
    W = weather()
    J = lake_jitter()
    mph = {c: party_hours_mean(c) for c in PROFILE}
    trips = {}
    for code, name, cls, area, target, pos, elev, access, *_ in LAKES:
        dmult = 1.55 if access == "walk-in" else 1.0
        dayw = np.array([DAYTYPE_F[K.day_type(d)] * MONTH_F[d.month] * W[d] for d in K.SEASON_DAYS])
        base = target * area / (dayw.sum() * mph[cls] * (1.42 if access == "walk-in" else 1.0))
        shift, dw = J[code]
        comps = PROFILE[cls]
        wts = np.array([c[2] for c in comps], float)
        wts[0] += dw
        wts[-1] -= dw
        wts = np.clip(wts, 0.02, None)
        wts /= wts.sum()
        cw = np.cumsum(wts)
        mu, cap = BOAT_SIZE[cls]
        rows = []
        for j, d in enumerate(K.SEASON_DAYS):
            gd = K.rng_for("day", code, d.isoformat())
            lam = base * dayw[j] * math.exp(gd.normal(0, 0.12))
            n = int(poisson.ppf(gd.random(), lam))
            if n == 0:
                continue
            sr, ss = K.sun_times(d)
            cpue_day = math.exp(gd.normal(0, 0.1))
            for q in range(n):
                g = K.rng_for("party", code, d.isoformat(), q)
                k = int(np.searchsorted(cw, g.random()))
                k = min(k, len(comps) - 1)
                cen = _centre(comps[k][0], sr, ss) + shift
                st = min(max(g.normal(cen, comps[k][1]), K.DAY_OPEN), K.DAY_CLOSE - 0.6)
                du = min(max(g.lognormal(math.log(comps[k][3] * dmult) - 0.06, 0.35), 0.6), 9.0)
                en = min(st + du, K.DAY_CLOSE)
                shore = bool(g.random() < SHORE_SHARE[cls])
                if shore:
                    size = int([1, 1, 1, 2, 2, 3][int(g.integers(0, 6))])
                else:
                    size = int(min(max(g.poisson(mu - 1) + 1, 1), cap))
                hrs = (en - st) * size
                caught = int(g.poisson(max(hrs * CPUE[cls] * cpue_day, 0.01)))
                kept = int(g.binomial(caught, KEEP[cls]))
                clipped = int(g.binomial(kept, CLIPPED[cls]))
                rows.append((d, float(st), float(en), shore, size, caught, kept, clipped, float(g.random()), k,
                             float(g.random()), float(g.random())))
        trips[code] = rows
    return trips


def truth_hours(trips):
    return {c: sum((r[2] - r[1]) * r[4] for r in rows) for c, rows in trips.items()}


# ------------------------------------------------------------------------------------------------- the survey
def survey_days():
    """three days a stratum (month by weekday or weekend day), drawn by the protocol's own random draw"""
    g = K.rng_for("surveydays")
    strata = {}
    for d in K.SEASON_DAYS:
        strata.setdefault(K.stratum(d), []).append(d)
    out = []
    for key in sorted(strata):
        days = strata[key]
        pick = sorted(g.choice(len(days), size=3, replace=False))
        out += [days[i] for i in pick]
    return sorted(out)


FOG_DAY = None        # set below once the survey days are drawn: the one AM loop that never left the dock
SMOKE_DAYS = []       # survey days inside the smoke, when the PM loop could not see the plateau's east lakes


def flights(sdays):
    """each loop's departure and the time the aircraft passed each lake; lakes it could not count are left blank"""
    g = K.rng_for("flights")
    out = []
    pos = {L[0]: L[5] for L in LAKES}
    fog = [d for d in sdays if d.month == 6 and K.day_type(d) == "weekday"][1]
    smoke = [d for d in sdays if dt.date(2026, 8, 10) <= d <= dt.date(2026, 8, 16)]
    global FOG_DAY, SMOKE_DAYS
    FOG_DAY, SMOKE_DAYS = fog, smoke
    for d in sdays:
        for loop, dep0 in (("AM", 9 + 20 / 60), ("PM", 14 + 15 / 60)):
            dep = dep0 + g.normal(0, 0.06)
            pace = 0.105 * math.exp(g.normal(0, 0.03))
            lakes = {}
            for code, p in pos.items():
                t = dep + 0.21 + (p - 1) * pace + g.normal(0, 0.025)
                counted = True
                if loop == "AM" and d == fog:
                    counted = False
                if loop == "PM" and d in smoke and p >= 20:
                    counted = False
                lakes[code] = (t, counted)
            out.append({"date": d, "loop": loop, "dep": dep, "lakes": lakes, "aborted": (loop == "AM" and d == fog)})
    return out


def count_lake(rows, d, t):
    boats = 0
    shore = 0
    for r in rows:
        if r[0] != d:
            continue
        if r[1] <= t < r[2]:
            if r[3]:
                shore += r[4]
            else:
                boats += 1
    return boats, shore


def interview_days():
    """the clerks' rotation: the clerks on duty pair up, one on the early shift (06:00 to 14:00) and one on the late
    shift (14:00 to 22:00), at one lake's main access each pair, the lake that has had the fewest interview days so
    far (weekend days counted apart), never two pairs at one lake"""
    g = K.rng_for("idays")
    codes = [L[0] for L in LAKES]
    off = {c: (i * 3) % 7 for i, c in enumerate(K.CLERKS)}     # each clerk's two days off a week, staggered
    done = {c: {"weekday": 0, "weekend": 0} for c in codes}
    sched = {}
    for d in K.SEASON_DAYS:
        dtp = K.day_type(d)
        on = [c for c in K.CLERKS if d.weekday() not in (off[c], (off[c] + 1) % 7)]
        rot = (d - K.SEASON_START).days % len(on)
        on = on[rot:] + on[:rot]
        taken = set()
        for p in range(len(on) // 2):
            early, late = on[2 * p], on[2 * p + 1]
            free = [c for c in codes if c not in taken]
            least = min(done[c][dtp] for c in free)
            cand = [c for c in free if done[c][dtp] == least]
            pick = cand[int(g.integers(0, len(cand)))]
            taken.add(pick)
            done[pick][dtp] += 1
            sched[(pick, d)] = (early, late)
    return sched


def interviews(trips, idays):
    out = []
    access = {L[0]: L[10] for L in LAKES}
    for code, rows in trips.items():
        dset = {d for (c, d) in idays if c == code}
        for r in rows:
            d, st, en, shore, size, caught, kept, clipped, u, comp, u_consent, u_spare = r
            if d not in dset:
                continue
            if u >= access[code]:
                continue          # left by another access
            if en < 6.0 or en > 22.0:
                continue
            if u_consent > 0.92:
                continue          # declined
            early, late = idays[(code, d)]
            out.append({"lake": code, "date": d, "start": st, "end": en, "shore": shore, "size": size,
                        "caught": caught, "kept": kept, "clipped": clipped, "clerk": early if en < 14.0 else late,
                        "u": u_spare})
    return out


# ------------------------------------------------------------------------------------------------- hatchery (ask)
# Raceways are numbered 1 to 8; when the new headbox came into use on 22 June 2026 the hatchery renumbered them from the
# intake end, so the old raceway n became raceway 9 - n. The world keeps each batch under its 2026 (new) number.
def old_number(rw_new):
    return 9 - rw_new


FPK0 = {1: 4.30, 2: 2.55, 3: 3.80, 4: 2.70, 5: 3.70, 6: 2.60, 7: 3.45, 8: 2.75}       # fish per kg on 4 May
GROWTH = {1: .0036, 2: .0026, 3: .0033, 4: .0028, 5: .0034, 6: .0027, 7: .0031, 8: .0029}
ONHAND0 = {1: 30400, 2: 27100, 3: 33800, 4: 26300, 5: 31900, 6: 28800, 7: 29500, 8: 27700}
SAMPLE_DAY0 = dt.date(2026, 5, 4)


def fpk_true(rw_new, d):
    return FPK0[rw_new] * math.exp(-GROWTH[rw_new] * (d - SAMPLE_DAY0).days)


def _truck_days(a, b):
    out = []
    d = a
    while d <= b:
        if d.weekday() in (1, 2, 3, 4):        # trucks run Tuesday to Friday; Monday is sampling day
            out.append(d)
        d += dt.timedelta(days=1)
    return out


EARLY = _truck_days(dt.date(2026, 5, 5), dt.date(2026, 6, 19))
MID = _truck_days(dt.date(2026, 6, 23), dt.date(2026, 8, 14))
LATE = _truck_days(dt.date(2026, 8, 18), dt.date(2026, 8, 28))


def hatchery_plan():
    """each stocked lake's releases for 2026: two to four, one of them in the summer top-up"""
    g = K.rng_for("plan")
    rel = []
    for L in LAKES:
        if L[7] == "walk-in":
            continue
        k = 2 + int(g.integers(0, 3))
        periods = ["mid"] + [["early", "mid", "late"][int(np.searchsorted([0.5, 0.8, 1.0], g.random()))]
                             for _ in range(k - 1)]
        for p in periods:
            pool = {"early": EARLY, "mid": MID, "late": LATE}[p]
            rel.append((pool[int(g.integers(0, len(pool)))], L[0]))
    rel.sort()
    return rel


LOAD_PLAN = {}    # planned net loads (kg) by trip, where the plan set them


def hatchery_trips():
    """release trips: each truck load from one raceway, to one lake or split between two; loads are the hatchery's
    planned net loads, kept in the plan file so the season can be replayed"""
    g = K.rng_for("hatchery")
    rel = hatchery_plan()
    onhand = dict(ONHAND0)
    last = SAMPLE_DAY0
    trips = []
    busy = {}
    i = 0
    tno = 2601
    while i < len(rel):
        d, lake = rel[i]
        split = (i + 1 < len(rel) and rel[i + 1][1] != lake and (rel[i + 1][0] - d).days <= 6 and g.random() < 0.34)
        dests = [lake, rel[i + 1][1]] if split else [lake]
        i += 2 if split else 1
        while busy.get(d, 0) >= 2 or d.weekday() not in (1, 2, 3, 4):
            d += dt.timedelta(days=1)
        truck = "T1" if busy.get(d, 0) == 0 else "T2"
        busy[d] = busy.get(d, 0) + 1
        trips.append({"trip": "QC-%d" % tno, "date": d, "truck": truck, "dests": dests})
        tno += 1
    trips.sort(key=lambda t: (t["date"], t["truck"]))
    out = []
    for t in trips:
        d = t["date"]
        # mortality since the last trip day
        for k in onhand:
            onhand[k] *= math.exp(-0.0006 * (d - last).days)
        last = d
        rw = int(g.integers(1, 9))
        load = float(np.round(g.uniform(300, 520), 1))
        if t["trip"] in LOAD_PLAN:
            load = LOAD_PLAN[t["trip"]]
        nets_total = int(round(load / 9.5 + g.integers(-2, 3)))
        if len(t["dests"]) == 2:
            n1 = int(round(nets_total * g.uniform(0.35, 0.65)))
            nets = [n1, nets_total - n1]
        else:
            nets = [nets_total]
        onhand[rw] -= load * fpk_true(rw, d)
        hot = d.month in (7, 8)
        drops = []
        for dest, nn in zip(t["dests"], nets):
            drops.append({"lake": dest, "nets": nn, "doa_u": float(g.random()), "hot": hot})
        out.append({"trip": t["trip"], "date": d, "truck": t["truck"], "rw_new": rw, "load": load,
                    "nets_total": nets_total, "drops": drops, "tank_temp": round(float(g.normal(11.5, 0.8)), 1)})
    return out


def raceway_samples(trips):
    """Monday's sample count of every raceway, with the inventory's fish on hand after the week's loads"""
    g = K.rng_for("samples")
    out = []
    onhand = {k: float(v) for k, v in ONHAND0.items()}
    loads = {}
    for t in trips:
        loads.setdefault(t["date"], []).append(t)
    d = SAMPLE_DAY0
    prev = d
    while d <= dt.date(2026, 8, 31):
        # apply the loads and mortality since the previous Monday
        x = prev
        while x < d:
            for k in onhand:
                onhand[k] *= math.exp(-0.0006)
            for t in loads.get(x, []):
                onhand[t["rw_new"]] -= t["load"] * fpk_true(t["rw_new"], x)
            x += dt.timedelta(days=1)
        for rw in range(1, 9):
            grams = float(np.round(g.uniform(2400, 3600), 0))
            n = int(round(fpk_true(rw, d) * grams / 1000 * math.exp(g.normal(0, 0.012))))
            out.append({"date": d, "rw_new": rw, "grams": grams, "count": n, "onhand": int(round(onhand[rw], -1))})
        prev = d
        d += dt.timedelta(days=7)
    return out


def fish_per_kg(samples, rw_new, d):
    """the hatchery's own figure for a load: its raceway's latest Monday sample on or before the loading day"""
    best = None
    for s in samples:
        if s["rw_new"] == rw_new and s["date"] <= d and (best is None or s["date"] > best["date"]):
            best = s
    return best["count"] / (best["grams"] / 1000.0)


def settle_drops(trips, samples):
    """dead fish counted at each drop, from the fish the hatchery's figure puts in the drop"""
    for t in trips:
        fpk = fish_per_kg(samples, t["rw_new"], t["date"])
        for dr in t["drops"]:
            fish = t["load"] * dr["nets"] / t["nets_total"] * fpk
            rate = 0.011 if dr["hot"] else 0.004
            # a Poisson draw by inversion of the drop's own uniform, so a load change moves only its own count
            lam = fish * rate
            k, p, c = 0, math.exp(-lam), math.exp(-lam)
            while c < dr["doa_u"] and k < 400:
                k += 1
                p *= lam / k
                c += p
            dr["doa"] = k
            dr["fish"] = fish
    return trips


# ------------------------------------------------------------------------------------------------- loggers (ask)
# each logger: the clock it was launched on, when it started logging (in the office) and when it was stopped at download
SERIALS = {
    "20184402": ("local", dt.datetime(2026, 5, 27, 8, 40), dt.datetime(2026, 9, 10, 9, 20)),
    "20184470": ("local", dt.datetime(2026, 5, 27, 8, 55), dt.datetime(2026, 9, 11, 15, 30)),
    "20184409": ("utc", dt.datetime(2026, 5, 28, 7, 30), dt.datetime(2026, 9, 10, 9, 40)),
    "20184533": ("local", dt.datetime(2026, 5, 28, 7, 35), dt.datetime(2026, 9, 10, 15, 10)),
    "20184417": ("local", dt.datetime(2026, 5, 29, 7, 50), dt.datetime(2026, 6, 3, 2, 15)),    # battery failed
    "20184421": ("utc", dt.datetime(2026, 5, 29, 8, 0), dt.datetime(2026, 9, 11, 9, 0)),
    "20184425": ("local", dt.datetime(2026, 5, 29, 8, 5), dt.datetime(2026, 9, 11, 9, 5)),
    "20184438": ("local", dt.datetime(2026, 5, 27, 9, 10), dt.datetime(2026, 9, 10, 9, 30)),
    "20184441": ("local", dt.datetime(2026, 5, 28, 8, 20), dt.datetime(2026, 9, 10, 9, 45)),
    "20184452": ("local", dt.datetime(2026, 5, 30, 8, 15), dt.datetime(2026, 9, 12, 10, 5)),
    "20184457": ("local", dt.datetime(2026, 5, 31, 8, 25), dt.datetime(2026, 9, 12, 10, 15)),
}
# deployments: serial, lake, depth (m), into the water, out of the water (None: not recovered)
DEPLOYMENTS = [
    ("20184402", "PP-03", 1.0, dt.datetime(2026, 5, 27, 14, 0), dt.datetime(2026, 9, 9, 10, 15)),
    ("20184470", "PP-03", 1.0, dt.datetime(2026, 5, 27, 14, 10), dt.datetime(2026, 7, 22, 9, 10)),
    ("20184470", "PP-20", 1.0, dt.datetime(2026, 7, 22, 13, 20), dt.datetime(2026, 9, 11, 10, 0)),
    ("20184409", "PP-11", 1.0, dt.datetime(2026, 5, 28, 11, 0), dt.datetime(2026, 9, 9, 13, 30)),
    ("20184533", "PP-11", 1.0, dt.datetime(2026, 5, 28, 11, 15), dt.datetime(2026, 7, 14, 8, 30)),
    ("20184533", "PP-19", 1.0, dt.datetime(2026, 7, 14, 12, 45), dt.datetime(2026, 9, 10, 9, 45)),
    ("20184417", "PP-19", 1.0, dt.datetime(2026, 5, 29, 10, 30), dt.datetime(2026, 7, 14, 12, 30)),
    ("20184421", "PP-09", 1.0, dt.datetime(2026, 5, 29, 13, 45), dt.datetime(2026, 9, 10, 12, 0)),
    ("20184425", "PP-09", 3.0, dt.datetime(2026, 5, 29, 14, 0), dt.datetime(2026, 9, 10, 12, 15)),
    ("20184438", "PP-26", 1.0, dt.datetime(2026, 5, 27, 16, 15), dt.datetime(2026, 9, 9, 15, 0)),
    ("20184441", "PP-07", 1.0, dt.datetime(2026, 5, 28, 15, 30), dt.datetime(2026, 9, 9, 11, 30)),
    ("20184446", "PP-20", 1.0, dt.datetime(2026, 5, 30, 10, 45), None),
    ("20184452", "PP-02", 1.0, dt.datetime(2026, 5, 30, 13, 15), dt.datetime(2026, 9, 11, 13, 45)),
    ("20184457", "PP-29", 1.0, dt.datetime(2026, 5, 31, 12, 30), dt.datetime(2026, 9, 11, 15, 15)),
]
PEAK_DOY = 207.0
# each logger's reading error against a reference thermometer, inside the +/-0.53 C a pendant logger is specified to
CALIBRATION = {"20184452": -0.30, "20184402": 0.00, "20184470": -0.04, "20184441": -0.31, "20184421": 0.00,
               "20184409": 0.18, "20184533": 0.02, "20184438": 0.03, "20184457": -0.05, "20184417": 0.07,
               "20184425": -0.12}


def water_temps():
    """15-minute readings of every logger from launch to download: lake water while deployed, air otherwise"""
    g = K.rng_for("water")
    elev = {L[0]: L[6] for L in LAKES}
    anomaly = {}
    a = 0.0
    for d in [dt.date(2026, 5, 20) + dt.timedelta(days=i) for i in range(125)]:
        a = 0.82 * a + g.normal(0, 0.55)
        anomaly[d] = a

    def anom(t):
        x = (t - dt.datetime(2026, 5, 20, 12, 0)).total_seconds() / 86400.0
        i = int(math.floor(x))
        f = x - i
        d0 = dt.date(2026, 5, 20) + dt.timedelta(days=i)
        return anomaly[d0] * (1 - f) + anomaly[d0 + dt.timedelta(days=1)] * f

    lake_peak = {}
    for L in LAKES:
        gl = K.rng_for("lakepeak", L[0])
        lake_peak[L[0]] = 21.55 - (elev[L[0]] - 1150) * 0.0105 + gl.normal(0, 0.2)

    def water(code, depth, t, off, gg):
        doy = t.timetuple().tm_yday + t.hour / 24.0 + t.minute / 1440.0
        seasonal = max(lake_peak[code] - 9.5 * ((doy - PEAK_DOY) / 62.0) ** 2, 9.0)
        diurnal = (0.55 if depth < 2 else 0.12) * math.cos(2 * math.pi * ((t.hour + t.minute / 60.0) - 17.0) / 24.0)
        deep = 0.0 if depth < 2 else -(2.4 + 0.8 * max(0.0, (doy - 160) / 60.0))
        return seasonal + diurnal + deep + anom(t) * (0.9 if depth < 2 else 0.4) + off + gg.normal(0, 0.05)

    def air(t, gg):
        h = t.hour + t.minute / 60.0
        if 8.0 <= h <= 18.0:
            return 23.5 + 3.5 * math.sin(math.pi * (h - 8.0) / 10.0) + gg.normal(0, 0.6)    # truck and dock
        return 21.4 + gg.normal(0, 0.3)                                                      # office

    series = {}
    for serial, (clock, start, stop) in SERIALS.items():
        gg = K.rng_for("logger", serial)
        off = CALIBRATION.get(serial, 0.0)
        deps = [x for x in DEPLOYMENTS if x[0] == serial]
        recs = []
        t = start
        while t <= stop:
            where = None
            for s, code, depth, a0, b0 in deps:
                if a0 <= t and (b0 is None or t <= b0):
                    where = (code, depth)
                    break
            v = water(where[0], where[1], t, off, gg) if where else air(t, gg)
            recs.append((t, round(v, 2), where))
            t += dt.timedelta(minutes=15)
        series[serial] = recs
    return series


# ------------------------------------------------------------------------------------------------- charter (ask)
FLEET = {"C-FVAB": "DHC-2 Beaver", "C-GVAK": "Cessna A185F"}
RATE = {"DHC-2 Beaver": 1180.0, "Cessna A185F": 795.0}
POSITIONING = 260.0
MINIMUM_BLOCK = 0.5


def charter(fl):
    """block times of every survey loop, with the 185 standing in while the Beaver was in for its 100-hour check"""
    g = K.rng_for("charter")
    out = []
    fno = 4101
    for f in fl:
        d = f["date"]
        dep = f["dep"]
        if f["aborted"]:
            blocks = [(dep - 0.18, dep + 0.27)]
        else:
            last = max(t for t, c in f["lakes"].values())
            off = dep - 0.16 + g.normal(0, 0.02)
            on = last + 0.38 + g.normal(0, 0.04)
            if d in SMOKE_DAYS and f["loop"] == "PM":
                mid = off + (on - off) * 0.48
                blocks = [(off, mid), (mid + 0.62 + g.normal(0, 0.05), on + 0.62)]
            else:
                blocks = [(off, on)]
        reg = "C-GVAK" if dt.date(2026, 7, 6) <= d <= dt.date(2026, 7, 24) else "C-FVAB"
        out.append({"flight": "VA%d" % fno, "date": d, "loop": f["loop"], "reg": reg, "blocks": blocks,
                    "aborted": f["aborted"]})
        fno += 1
    return out


def simulate():
    trips = simulate_trips()
    sd = survey_days()
    fl = flights(sd)
    counts = []
    for f in fl:
        for code, (t, ok) in f["lakes"].items():
            if ok:
                b, s = count_lake(trips[code], f["date"], t)
            else:
                b, s = None, None
            counts.append({"date": f["date"], "loop": f["loop"], "lake": code, "t": t, "boats": b, "shore": s})
    idays = interview_days()
    iv = interviews(trips, idays)
    ht = hatchery_trips()
    samples = raceway_samples(ht)
    settle_drops(ht, samples)
    temps = water_temps()
    ch = charter(fl)
    return {"trips": trips, "truth": truth_hours(trips), "survey_days": sd, "flights": fl, "counts": counts,
            "idays": idays, "interviews": iv, "hatchery": ht, "samples": samples, "temps": temps, "charter": ch}
