"""The seeded world before any file is written: routes, runs, journeys, collisions, claims, repairs, recoveries and the
2027 schedule. The darkness that drives the collisions is the handbook table's (astro.TABLE)."""
import datetime as dt
import math

import numpy as np

import astro as A
import params as P

DAY0 = dt.date(2000, 1, 1)


def daynum(d):
    return (d - DAY0).days


def working_days(start, end):
    out, d = [], start
    while d <= end:
        if d.weekday() < 6 and (d.month, d.day) not in P.NO_RUN_DAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def band_of(h):
    for i in range(len(P.BAND_EDGES) - 1):
        if P.BAND_EDGES[i] <= h < P.BAND_EDGES[i + 1]:
            return i
    return len(P.BAND_EDGES) - 2


def segments(date, depot, t0_local, t1_local):
    """Split a stretch of driving [t0, t1) in local clock hours on date at depot into pieces with one traffic band and
    one light state. Returns [(start local h, end local h, band, dark)]."""
    off = A.bst_offset(date)
    rise, sett = A.TABLE[(depot, A.row_of(date))]
    rise_l, sett_l = rise / 60.0 + off, sett / 60.0 + off
    cuts = sorted({t0_local, t1_local} | {x for x in P.BAND_EDGES if t0_local < x < t1_local}
                  | {x for x in (rise_l, sett_l) if t0_local < x < t1_local})
    out = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        m = (a + b) / 2
        dark = 1 if (m < rise_l or m > sett_l) else 0
        out.append((a, b, band_of(m % 24), dark))
    return out


def simulate(seed=P.SEED):
    rng = np.random.default_rng([seed, 1])
    W = {"seed": seed}
    # vehicles and routes
    vehicles, routes = [], []
    letters = "ABCDEFGHJKLMNOPRSTUVWXYZ"
    area = {"CRA": ["NA", "NB", "NC", "ND", "NE", "NG"], "GAT": ["NH", "NJ", "NK", "NL", "NM", "NO"],
            "CAR": ["PU", "PV", "PW", "PX", "PY"], "DAR": ["NU", "NV", "NW", "NX", "NY"]}
    ages = ["19", "69", "20", "70", "21", "71", "22", "72", "23", "73"]
    used = set()

    def new_reg(depot, age=None):
        while True:
            r = "%s%s %s" % (rng.choice(area[depot]), age or rng.choice(ages), "".join(rng.choice(list(letters), 3)))
            if r not in used:
                used.add(r)
                return r
    fleet_no = 4100
    for code, name, site, pc, lat, lon, n in P.DEPOTS:
        n_spare = max(3, int(round(n * P.SPARE_SHARE)))
        for i in range(n):
            fleet_no += int(rng.integers(1, 4))
            reg = new_reg(code)
            v = {"reg": reg, "fleet_no": "T%d" % fleet_no, "depot": code, "spare": i >= n - n_spare,
                 "from": P.REC_START - dt.timedelta(days=int(rng.integers(60, 1500))), "to": None}
            vehicles.append(v)
            if not v["spare"]:
                std = round(float(rng.uniform(*P.STD_DEP)) * 4) / 4
                summ = round(float(rng.uniform(*P.SUM_DEP)) * 4) / 4
                plan = round(float(rng.uniform(*P.PLAN_DEP)) * 4) / 4
                dur = float(rng.uniform(*P.DUR_H))
                kmh = float(rng.uniform(*P.KM_PER_H))
                routes.append({"route": "%s%02d" % (code, len(routes) % 100 + 1), "depot": code, "home": reg,
                               "std": std, "summer": summ, "plan": plan, "dur": dur, "km": round(dur * kmh)})
    # unique route ids per depot
    k = {}
    for r in routes:
        k[r["depot"]] = k.get(r["depot"], 0) + 1
        r["route"] = "%s-%03d" % (r["depot"], 100 + 7 * k[r["depot"]] + int(rng.integers(0, 6)))
    W["vehicles"], W["routes"] = vehicles, routes
    days = working_days(P.REC_START, P.LISTING_AS_AT)      # driven to the listing date; the telematics ship to REC_END
    W["days"] = days
    rate = np.array(P.TRAFFIC) * P.BASE_PER_KM
    # runs, journeys, collisions (vehicle assignment later)
    runs = []
    for d in days:
        summer = d.month in P.SUMMER_MONTHS
        for r in routes:
            dep = (r["summer"] if summer else r["std"]) + rng.normal(0, 0.17)
            dur = r["dur"] + rng.normal(0, 0.40)
            km = r["km"] * (1 + rng.normal(0, 0.05))
            a, b = dep, dep + dur
            lam, segs = 0.0, []
            for x, y, band, dark in segments(d, r["depot"], a, b):
                l = rate[band] * (P.DARK_MULT if dark else 1.0) * km * (y - x) / (b - a)
                segs.append((x, y, l))
                lam += l
            n = rng.poisson(lam)
            hits = []
            for _ in range(n):
                u = rng.uniform(0, lam)
                acc = 0.0
                for x, y, l in segs:
                    if u <= acc + l:
                        hits.append(x + (u - acc) / l * (y - x))
                        break
                    acc += l
            # the platform's day summary: journeys between ignition-off stops of over ten minutes, and idle minutes
            nj = int(rng.choice([1, 2, 2, 3, 3, 4]))
            runs.append({"date": d, "route": r["route"], "depot": r["depot"], "home": r["home"],
                         "journeys": [(a, b, km, sorted(hits))], "nj": nj,
                         "drive_min": int(round(dur * 60 * rng.uniform(0.72, 0.84)))})
    W["runs"] = runs
    assign(W, rng)
    return W


def assign(W, rng):
    """Chronological pass: each route runs on its home truck unless that truck is off the road, then on a depot spare;
    a collision with own damage sends the truck to the bodyshop; a written-off truck is replaced."""
    vehicles = {v["reg"]: v for v in W["vehicles"]}
    off = {reg: [] for reg in vehicles}            # [(first day off, last day off)]
    spares = {code: [v["reg"] for v in W["vehicles"] if v["spare"] and v["depot"] == code] for code, *_ in P.DEPOTS}
    route_home = {r["route"]: r["home"] for r in W["routes"]}
    claims, repl = [], []

    def is_off(reg, d):
        return any(a <= d <= b for a, b in off[reg][-3:]) or (vehicles[reg]["to"] is not None and d > vehicles[reg]["to"])

    by_day = {}
    for run in W["runs"]:
        by_day.setdefault(run["date"], []).append(run)
    for d in W["days"]:
        busy = set()
        for run in by_day[d]:
            reg = route_home[run["route"]]
            if is_off(reg, d):
                pool = [s for s in spares[run["depot"]] if s not in busy and not is_off(s, d)]
                reg = pool[0] if pool else reg
            busy.add(reg)
            run["reg"] = reg
            for a, b, kmj, hits in run["journeys"]:
                for h in hits:
                    c = collision(W, rng, d, run, reg, h)
                    claims.append(c)
                    if c["od"]:
                        if c["write_off"]:
                            vehicles[reg]["to"] = d
                            off[reg].append((d, d + dt.timedelta(days=3650)))
                            code = run["depot"]
                            nv = {"reg": None, "fleet_no": None, "depot": code, "spare": vehicles[reg]["spare"],
                                  "from": d + dt.timedelta(days=int(rng.integers(21, 49))), "to": None}
                            repl.append((reg, nv))
                        else:
                            delay = 0 if c["towed"] else int(rng.integers(1, 9))
                            a0 = d + dt.timedelta(days=delay)
                            b0 = a0 + dt.timedelta(days=int(rng.integers(3, 15)))
                            off[reg].append((a0, b0))
                            c["shop_in"], c["shop_out"] = a0, b0
        # replacements arrive
        for old, nv in list(repl):
            if nv["reg"] is None and nv["from"] <= d:
                letters = "ABCDEFGHJKLMNOPRSTUVWXYZ"
                age = "24" if nv["from"] < dt.date(2025, 3, 1) else ("74" if nv["from"] < dt.date(2025, 9, 1) else
                                                                     ("25" if nv["from"] < dt.date(2026, 3, 1) else "75"))
                reg = old[:2] + age + " " + "".join(rng.choice(list(letters), 3))
                nv["reg"] = reg
                nv["fleet_no"] = vehicles[old]["fleet_no"] + "R"
                vehicles[reg] = nv
                off[reg] = []
                W["vehicles"].append(nv)
                for r in W["routes"]:
                    if r["home"] == old:
                        r["home"] = reg
                        route_home[r["route"]] = reg
                for code in spares:
                    if old in spares[code]:
                        spares[code] = [reg if x == old else x for x in spares[code]]
                repl.remove((old, nv))
    W["claims"] = claims
    W["off"] = off


def collision(W, rng, d, run, reg, h_local):
    lia = rng.choice([x for x, _ in P.LIABILITY], p=[p for _, p in P.LIABILITY])
    share = None
    if lia == "shared":
        share = [s for s, _ in P.SHARES][int(rng.choice(len(P.SHARES), p=[p for _, p in P.SHARES]))]
    od = bool(rng.random() < P.P_OD) or lia == "no_tp"
    tppd = lia != "no_tp" and bool(rng.random() < (P.P_TPPD / 0.92))
    tpi = lia != "no_tp" and bool(rng.random() < (P.P_TPI / 0.92))
    if lia != "no_tp" and not (tppd or tpi or od):
        tppd = True
    tp_ins = None
    if lia != "no_tp":
        tp_ins = P.TP_INSURERS[int(rng.choice(len(P.TP_INSURERS), p=P.TP_WEIGHTS))]
    hh = h_local % 24
    return {"date": d, "time_h": hh, "depot": run["depot"], "route": run["route"], "reg": reg, "liability": lia,
            "share": share, "od": od, "tppd": tppd, "tpi": tpi, "tp_insurer": tp_ins,
            "write_off": od and bool(rng.random() < P.P_WRITE_OFF), "towed": bool(rng.random() < 0.35),
            "shop_in": None, "shop_out": None}


def plan_2027():
    """The 2027 schedule's route-days, from each route's planned departure, duration and kilometres."""
    return working_days(dt.date(P.FUND_YEAR, 1, 1), dt.date(P.FUND_YEAR, 12, 31))
