"""The ask-side records: October 2026's ticket-machine log-ons with the HR depot assignments, the incident register
with the insurer's monthly bordereau, and the diversions log beside the contract's service return. Generator truth;
build.py writes the files."""
import datetime as dt

from common import days, rng
from world import DEPOTS, NIGHT, DEPOT_NAME

OCT0, OCT1 = dt.date(2026, 10, 1), dt.date(2026, 11, 1)
DST_END = dt.datetime(2026, 10, 25, 3, 0, 0)      # local wall clock at which CEST returns to CET


def staff(world):
    """Employee numbers by depot, with the transfers HR recorded during the year."""
    r = rng("staff")
    emp = []
    n = 0
    home = {}
    for dep, _ in DEPOTS:
        size = 128 if dep not in ("QUI", "TEN") else 118
        for _ in range(size):
            n += 1
            e = "%05d" % (40000 + int(r.integers(0, 9999)) * 0 + n * 7 + 13)
            emp.append(e)
            home[e] = dep
    assign = {e: [(dt.date(2010, 1, 1), dt.date(2099, 12, 31), home[e])] for e in emp}
    # Route 25's drivers moved from El Quiñón to Las Tenerías with the route at Red 2026.
    qui = [e for e in emp if home[e] == "QUI"]
    for e in qui[:20]:
        assign[e] = [(dt.date(2010, 1, 1), dt.date(2025, 12, 13), "QUI"), (dt.date(2025, 12, 14), dt.date(2099, 12, 31), "TEN")]
    # Transfers on Monday 19 October 2026.
    deps = [d for d, _ in DEPOTS]
    moved = []
    for k in r.permutation(len(emp))[:9]:
        e = emp[int(k)]
        if len(assign[e]) > 1:
            continue
        a = assign[e][0][2]
        b = deps[(deps.index(a) + 1 + int(r.integers(0, 6))) % 7]
        assign[e] = [(dt.date(2010, 1, 1), dt.date(2026, 10, 18), a), (dt.date(2026, 10, 19), dt.date(2099, 12, 31), b)]
        moved.append(e)
    return emp, assign, moved


def depot_of(assign, e, day):
    for a, b, d in assign[e]:
        if a <= day <= b:
            return d
    raise KeyError((e, day))


def etm_sessions(world, emp, assign):
    """Driver sessions on buses, 1 October to 1 November 2026, local wall-clock times (naive datetimes).

    Each session: dict(fleet, emp, route, on, off, kind) where kind is service, positioning or training. A driver
    relieved onto another bus mid-duty leaves the first bus's session open until the next driver logs on to it,
    which is when the machine writes the first session's log-off; `true_off` keeps the real end."""
    r = rng("etm")
    out = []
    by_day = {}
    for (d0, route, dr), trips in sorted(world.trips.items()):
        if dt.date(2026, 9, 30) <= d0 <= OCT1 and dr == "IDA" and trips:
            by_day.setdefault(d0, []).append((route, trips))
    for day in days(dt.date(2026, 9, 30), OCT1):
        # Drivers available per depot that day, shuffled.
        pool = {}
        for dep, _ in DEPOTS:
            es = [e for e in emp if depot_of(assign, e, day) == dep]
            pool[dep] = [es[int(i)] for i in r.permutation(len(es))]
        ptr = {dep: 0 for dep, _ in DEPOTS}

        def take(dep):
            e = pool[dep][ptr[dep] % len(pool[dep])]
            ptr[dep] += 1
            return e

        base = dt.datetime(day.year, day.month, day.day)
        # Buses that ran each route that day, from the operated service.
        for route, trips in by_day.get(day, []):
            dep = world.fleet.depot_on(trips[0][1], day)
            buses = sorted({b for _, b in trips})
            for b in buses:
                if route in NIGHT:
                    on = base + dt.timedelta(hours=23, minutes=int(r.integers(5, 20)))
                    off = base + dt.timedelta(days=1, hours=6, minutes=int(r.integers(35, 55)))
                    out.append(dict(fleet=b, emp=take(dep), route=route, on=on, off=off, kind="service"))
                    continue
                e1, e2 = take(dep), take(dep)
                on1 = base + dt.timedelta(hours=5, minutes=int(r.integers(38, 62)))
                ch = base + dt.timedelta(hours=14, minutes=int(r.integers(0, 40)))
                off2 = base + dt.timedelta(hours=23, minutes=int(r.integers(20, 58)))
                out.append(dict(fleet=b, emp=e1, route=route, on=on1, off=ch, kind="service"))
                out.append(dict(fleet=b, emp=e2, route=route, on=ch + dt.timedelta(minutes=int(r.integers(1, 4))),
                                off=off2, kind="service"))
            # Positioning moves and the driving school.
        for dep, _ in DEPOTS:
            for _ in range(int(r.integers(5, 10))):
                e = take(dep)
                bs = world.fleet.buses_of(dep, day)
                b = bs[int(r.integers(0, len(bs)))]
                on = base + dt.timedelta(hours=int(r.integers(9, 19)), minutes=int(r.integers(0, 60)))
                out.append(dict(fleet=b, emp=e, route="000", on=on, off=on + dt.timedelta(minutes=int(r.integers(14, 46))),
                                kind="positioning"))
            if day.weekday() < 5 and r.random() < 0.5:
                e = take(dep)
                bs = world.fleet.buses_of(dep, day)
                b = bs[int(r.integers(0, len(bs)))]
                on = base + dt.timedelta(hours=9, minutes=int(r.integers(0, 30)))
                out.append(dict(fleet=b, emp=e, route="ESC", on=on, off=on + dt.timedelta(hours=3, minutes=int(r.integers(0, 50))),
                                kind="training"))
    for s in out:
        s["true_off"] = s["off"]
    # Reliefs: an early driver is taken off bus A at t and logs on to bus B, whose early driver goes home. Bus B's
    # machine closes the earlier session at t; bus A's machine keeps the relieved driver logged on until the late
    # driver logs on to A, and writes that time as the log-off.
    early = {}
    late = {}
    for s in out:
        if s["kind"] == "service" and s["route"] not in NIGHT:
            (early if s["on"].hour < 8 else late)[(s["on"].date(), s["fleet"])] = s
    keys = sorted(k for k in early if OCT0 <= k[0] <= OCT1)
    pick = sorted(int(i) for i in r.permutation(len(keys))[: int(len(keys) * 0.02)])
    done = set()
    for i in pick:
        day, a = keys[i]
        sa = early[(day, a)]
        if (day, a) in done:
            continue
        cands = [k for k in keys if k[0] == day and k[1] != a and k not in done
                 and world.fleet.depot_on(k[1], day) == world.fleet.depot_on(a, day)]
        if not cands:
            continue
        kb = cands[int(r.integers(0, len(cands)))]
        sb = early[kb]
        t = max(sa["on"], sb["on"]) + dt.timedelta(hours=int(r.integers(2, 5)), minutes=int(r.integers(0, 60)))
        if t >= sb["off"] - dt.timedelta(minutes=30) or (day, a) not in late or kb not in late:
            continue
        # Bus B: its early driver goes home at t, and the relieved driver takes it until the late driver.
        sb["off"] = sb["true_off"] = t
        out.append(dict(fleet=sb["fleet"], emp=sa["emp"], route=sb["route"], on=t, off=late[kb]["on"],
                        true_off=late[kb]["on"], kind="service", relief=True))
        # Bus A: the machine writes the late driver's log-on as the relieved driver's log-off.
        sa["off"] = late[(day, a)]["on"]
        sa["true_off"] = t
        sa["relief"] = True
        done.add((day, a))
        done.add(kb)
    out.sort(key=lambda s: (s["on"], s["fleet"], s["emp"]))
    return out


def true_hours(s):
    """Elapsed hours of a session: the wall clock gains an hour when CEST ends at 03:00 on 25 October."""
    h = (s["true_off"] - s["on"]).total_seconds() / 3600.0
    if s["on"] < DST_END <= s["true_off"]:
        h += 1.0
    return h


def incidents(world):
    """The incident register for January to October 2026 and the insurer's claims on them."""
    r = rng("incidents")
    inc = []
    for day in days(dt.date(2026, 1, 1), dt.date(2026, 10, 31)):
        for dep, _ in DEPOTS:
            lam = 0.150 if dep != "SLZ" else 0.165
            for _ in range(int(r.poisson(lam / 1.0 if day.weekday() < 5 else lam * 0.7))):
                bs = world.fleet.buses_of(dep, day)
                b = bs[int(r.integers(0, len(bs)))]
                t = dt.datetime(day.year, day.month, day.day, int(r.integers(6, 23)), int(r.integers(0, 60)))
                u = r.random()
                fault = "A" if u < 0.38 else ("C" if u < 0.50 else ("N" if u < 0.91 else "R"))
                kind = ["Alcance", "Roce lateral", "Golpe con objeto fijo", "Contacto con peatón", "Retrovisor",
                        "Maniobra en parada"][int(r.choice(6, p=[0.24, 0.27, 0.15, 0.04, 0.2, 0.1]))]
                inc.append(dict(day=day, t=t, fleet=b, dep=dep, fault=fault, kind=kind,
                                street=["Calle Real", "Avenida de Andalucía", "Ronda Norte", "Calle Ancha",
                                        "Avenida del Río", "Calle Mayor", "Avenida de Córdoba", "Calle Feria",
                                        "Avenida de Sevilla", "Calle Toledo"][int(r.integers(0, 10))],
                                num=int(r.integers(2, 140))))
    # Claims: third-party claims on most at-fault incidents, own-damage claims on some others.
    claims = []
    k = 0
    for i, x in enumerate(inc):
        p = 0.86 if x["fault"] in ("A", "C") else (0.22 if x["fault"] == "N" else 0.6)
        if r.random() >= p:
            continue
        k += 1
        notified = x["day"] + dt.timedelta(days=int(r.integers(2, 25)))
        if notified > dt.date(2026, 10, 31):
            continue
        amount = float(round(r.lognormal(7.1, 0.85), 2)) if x["fault"] != "R" else float(round(r.lognormal(6.9, 0.8), 2))
        if x["kind"] == "Contacto con peatón":
            amount = float(round(amount * 3.5, 2))
        claims.append(dict(inc=i, no="SIN-26-%05d" % (4100 + k * 3), notified=notified, total=amount, reopen=None))
    # Some closed claims reopen under a new number that carries the earlier payments forward.
    base = [c for c in claims if (c["notified"] < dt.date(2026, 7, 15))]
    for j in sorted(int(i) for i in r.permutation(len(base))[: int(len(base) * 0.15)]):
        c = base[j]
        extra = float(round(r.lognormal(6.4, 0.7), 2))
        k += 1
        reo = dt.date(2026, 7, 20) + dt.timedelta(days=int(r.integers(0, 80)))
        claims.append(dict(inc=c["inc"], no="SIN-26-%05d" % (4100 + k * 3), notified=reo, total=extra,
                           reopen=c["no"]))
    # Duplicate incident reports: the driver's own report and the supervisor's, minutes apart.
    dups = []
    for j in sorted(int(i) for i in r.permutation(len(inc))[: int(len(inc) * 0.085)]):
        x = inc[j]
        y = dict(x)
        y["t"] = x["t"] + dt.timedelta(minutes=int(r.choice([-1, 1])) * int(r.integers(3, 16)))
        y["dup_of"] = j
        dups.append(y)
    return inc, claims, dups


def diversions():
    """Authorised diversions in July to October 2026 (works and events), with the change in each trip's length."""
    r = rng("diversions")
    reasons = ["Obras de saneamiento", "Renovación de pavimento", "Corte por obras del colector", "Mercadillo",
               "Obras de la red de agua", "Prueba deportiva", "Fiestas del barrio", "Poda y obras de alumbrado",
               "Cierre de puente", "Obras de accesibilidad"]
    streets = ["Calle Granada", "Avenida de la Paz", "Calle San Pablo", "Calle Ciprés", "Avenida del Río",
               "Calle Toledo", "Calle Huerta", "Avenida de Europa", "Calle Arenal", "Calle Victoria"]
    out = []
    k = 30
    from world import ROUTES
    for dep, lines in sorted(ROUTES.items()):
        for month in (7, 8, 9, 10):
            k += 1
            pick = [lines[int(i)] for i in sorted(r.permutation(len(lines))[: int(r.integers(1, 3))])]
            a = dt.date(2026, month, int(r.integers(1, 20)))
            e = min(a + dt.timedelta(days=int(r.integers(4, 26))), dt.date(2026, 10, 31))
            km = float(r.choice([-0.6, -0.4, 0.5, 0.7, 0.9, 1.1, 1.4, 1.8, 2.1]))
            dirs = ["IDA", "VUELTA"] if r.random() < 0.6 else [["IDA"], ["VUELTA"]][int(r.integers(0, 2))]
            out.append(dict(id="DV-2026-%03d" % k, routes=pick, dirs=dirs, start=a, end=e, km=km,
                            reason="%s, %s" % (reasons[int(r.integers(0, len(reasons)))],
                                               streets[int(r.integers(0, len(streets)))])))
    out.sort(key=lambda d: (d["start"], d["id"]))
    return out
