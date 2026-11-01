"""The Matiri Forest Products world, drawn from a fixed seed: the fleet, FY2026's port loads and their scaling, the cartage
invoices, the domestic mill deliveries and the FY2028 harvest plan. Clean truth; pack.py and docs.py render it."""
import datetime as dt
import string

import numpy as np

import params as P


class World:
    pass


def _plate(rng, used):
    while True:
        p = "".join(rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ"), 3)) + str(int(rng.integers(100, 999)))
        if p not in used:
            used.add(p)
            return p


def working_days(rng, start, end):
    """Days the forests cart: weekdays and some Saturdays, less public holidays and the Christmas shutdown."""
    hol = {dt.date(2025, 10, 27), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 1, 2),
           dt.date(2026, 2, 6), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 4, 27), dt.date(2026, 6, 1),
           dt.date(2025, 10, 24)}
    out = []
    d = start
    while d <= end:
        shut = dt.date(2025, 12, 20) <= d <= dt.date(2026, 1, 6)
        if d not in hol and not shut and (d.weekday() < 5 or (d.weekday() == 5 and rng.random() < 0.35)):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    W = World()
    used = set()
    # ---------------------------------------------------------------- fleet
    counts = {"RLC": 14, "KRH": 12, "TTT": 11, "WHT": 9, "KNC": 8, "PLH": 8}
    units = []
    for car, n in counts.items():
        for j in range(n):
            nine = rng.random() < P.NINE_AXLE_SHARE[car]
            year = int(rng.integers(2011, 2026))
            bunks = int(rng.choice([4, 5], p=[0.45, 0.55] if nine else [0.8, 0.2]))
            # tare follows the axle set-up, the trailer's bunk count, its age (older steel trailers run heavier) and the
            # unit's fit-out (cab guard, toolboxes, a second fuel tank)
            tare = (18.25 if nine else 16.85) + 0.22 * (bunks == 5) + 0.035 * (2025 - year) + float(rng.normal(0, 0.28))
            tare = round(float(np.clip(tare, 17.3 if nine else 16.1, 19.9 if nine else 18.3)), 2)
            base = P.BUNK_VOLUME[(nine, bunks)]
            cap = {L: round(base[L] + float(rng.normal(0, 0.25)), 1) for L in (3.9, 5.9, 12.1)}
            units.append(dict(unit=None, carrier=car, rego=_plate(rng, used), prev="",
                              config="9-axle truck and trailer" if nine else "8-axle truck and trailer",
                              eligible=nine, tare=tare, cap=cap, bunks=bunks, year=year, trailer=_plate(rng, used)))
    # Matiri issues its truck numbers at induction, so the numbers run with the units' age across every carrier
    order = sorted(range(len(units)), key=lambda i: units[i]["year"] + float(rng.uniform(-1.5, 1.5)))
    no = 207
    for i in order:
        no += int(rng.integers(1, 6))
        units[i]["unit"] = str(no)
    # two units re-registered on 1 February 2026 (personalised plates on the head contractors' new livery)
    rereg = [next(u for u in units if u["carrier"] == "RLC"), next(u for u in units if u["carrier"] == "KRH")]
    for u, plate in zip(rereg, ("RUAHN1", "KERERU")):
        u["prev"] = u["rego"]
        u["rego"] = plate
    W.units = units
    W.rereg_date = dt.date(2026, 2, 1)

    # ---------------------------------------------------------------- FY2026 port loads
    days = working_days(rng, *P.FY26)
    per_day = {}
    loads = []
    wts = np.array([1.0 if u["carrier"] in ("RLC", "KRH", "TTT") else 0.85 for u in units])
    for fc, f in P.FORESTS.items():
        closed = set(d for d in days if rng.random() < 0.05)
        fdays = [d for d in days if d not in closed]
        grades = list(f["mix"])
        mix = np.array([f["mix"][g] for g in grades])
        tonnes_left = f["tonnes"]
        while tonnes_left > 0:
            g = grades[int(rng.choice(len(grades), p=mix))]
            k = int(rng.choice(len(units), p=wts / wts.sum()))
            u = units[k]
            gd = P.GRADES[g]
            dens = float(np.clip(rng.normal(gd["density"], 0.028), gd["density"] - 0.09, gd["density"] + 0.09))
            cap = u["cap"][gd["length"]]
            mass_pay = P.OLD_GROSS - u["tare"] - float(rng.uniform(0.0, P.LOAD_MARGIN_T))
            vol_pay = cap * dens * float(rng.uniform(1.0 - P.BUNK_FILL_SHORTFALL, 1.0))
            net = round(min(mass_pay, vol_pay) / 0.02) * 0.02
            jas = round(net / dens, 3)
            while True:
                d = fdays[int(rng.integers(len(fdays)))]
                if per_day.get((d, u["unit"]), 0) < 3:
                    break
            per_day[(d, u["unit"])] = per_day.get((d, u["unit"]), 0) + 1
            loads.append(dict(forest=fc, grade=g, unit=u["unit"], net=round(net, 2), jas=jas, dens=dens, date=d,
                              limited="mass" if mass_pay <= vol_pay else "volume"))
            tonnes_left -= net
    # times: each unit's loads on a day spaced by the forest's round trip
    loads.sort(key=lambda r: (r["date"], r["unit"], r["forest"]))
    by_ud = {}
    for r in loads:
        by_ud.setdefault((r["date"], r["unit"]), []).append(r)
    for (d, un), rs in by_ud.items():
        t = dt.datetime.combine(d, dt.time(6, 10)) + dt.timedelta(minutes=int(rng.integers(0, 70)))
        for r in rs:
            km = P.FORESTS[r["forest"]]["km"]
            t = t + dt.timedelta(minutes=int(km * 1.3 + rng.integers(25, 55)))
            r["wb_time"] = t
            t = t + dt.timedelta(minutes=int(km * 1.25 + rng.integers(30, 70)))
    unit_by = {u["unit"]: u for u in units}
    for r in loads:
        u = unit_by[r["unit"]]
        r["rego"] = u["prev"] if (u["prev"] and r["date"] < W.rereg_date) else u["rego"]
        r["scale_time"] = r["wb_time"] + dt.timedelta(minutes=int(rng.integers(4, 26)), seconds=int(rng.integers(0, 60)))
        r["pieces"] = max(8, int(round(r["jas"] / (P.GRADES[r["grade"]]["piece"] * float(rng.uniform(0.9, 1.1))))))
    loads.sort(key=lambda r: r["wb_time"])
    W.loads = loads

    # ---------------------------------------------------------------- cartage invoices (FY2026 loads)
    rate_km = {fc: round(P.RATE_BASE + P.RATE_PER_KM * f["km"], 2) for fc, f in P.FORESTS.items()}
    W.rates = rate_km
    W.invoice_lines = []
    for r in loads:
        u = unit_by[r["unit"]]
        billed = P.BILLED_BY.get(u["carrier"], u["carrier"])
        W.invoice_lines.append(dict(load=r, billed=billed, hauler=u["carrier"], rate=rate_km[r["forest"]],
                                    amount=round(r["net"] * rate_km[r["forest"]], 2)))
    W.dupes = [W.invoice_lines[int(i)] for i in sorted(rng.choice(len(W.invoice_lines), 7, replace=False))]

    # ---------------------------------------------------------------- domestic mill deliveries
    W.mill_loads = []
    mill_t = dict(P.MILL_TONNES)
    dom_days = working_days(np.random.default_rng([seed, 30]), dt.date(2025, 6, 16), dt.date(2026, 6, 30))
    W.dom_days = dom_days
    for k, (mc, tot) in enumerate(mill_t.items()):
        rng_m = np.random.default_rng([seed, 31, k])
        left = tot
        while left > 0:
            u = units[int(rng_m.integers(len(units)))]
            net = round(float(rng_m.uniform(22.5, 27.0)) / 0.02) * 0.02
            d = dom_days[int(rng_m.integers(len(dom_days)))]
            t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=int(rng_m.integers(0, 600)))
            post = d + dt.timedelta(days=int(rng_m.integers(1, 10)))
            while post.weekday() >= 5:
                post += dt.timedelta(days=1)
            fc = list(P.FORESTS)[int(rng_m.integers(len(P.FORESTS)))]
            W.mill_loads.append(dict(mill=mc, unit=u["unit"], rego=u["prev"] if (u["prev"] and d < W.rereg_date) else u["rego"],
                                     net=round(net, 2), time=t, date=d, posted=post, forest=fc,
                                     grade=str(rng_m.choice(["S30", "L28", "Pulp"], p=[.45, .35, .2]))))
            if P.FY26[0] <= d <= P.FY26[1]:
                left -= net
    W.mill_loads.sort(key=lambda r: r["time"])

    # ---------------------------------------------------------------- the FY2028 harvest plan (export tonnes)
    plan = {}
    for fc, f in P.FORESTS.items():
        tot = f["tonnes"] * P.PLAN_SCALE
        mix = {g: max(0.0, f["mix"][g] + P.PLAN_MIX_SHIFT[g]) for g in f["mix"]}
        s = sum(mix.values())
        for g in mix:
            plan[(fc, g)] = round(tot * mix[g] / s * P.PLAN_GRADE_ADJ[g] / 100) * 100
    W.plan = plan
    return W


# ---------------------------------------------------------------- truth for the call
def new_payload(u, dens, grade, mass_only=False):
    gross = P.NEW_GROSS if u["eligible"] else P.OLD_GROSS
    m = gross - u["tare"]
    if mass_only:
        return m
    return min(m, u["cap"][P.GRADES[grade]["length"]] * dens)


def truth_loads(W, mass_only=False):
    unit_by = {u["unit"]: u for u in W.units}
    pay = {g: [] for g in P.GRADE_ORDER}
    for r in W.loads:
        pay[r["grade"]].append(new_payload(unit_by[r["unit"]], r["net"] / r["jas"], r["grade"], mass_only))
    out = {}
    for g in P.GRADE_ORDER:
        tonnes = sum(v for (fc, gg), v in W.plan.items() if gg == g)
        out[g] = tonnes / (sum(pay[g]) / len(pay[g]))
    return out


def make(seed=P.SEED):
    return build(seed)
