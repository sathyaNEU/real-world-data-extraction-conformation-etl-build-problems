"""The operating world: two working timetables, the fleet and its daily formations, each train's passengers by
origin and destination (so its load after every departure), its movements against the timetable, its on-board
crew and the fares. Every draw comes from a stream keyed on the thing it describes, so adding one train or one
day moves nothing else."""
import datetime as dt
import hashlib
import numpy as np
import common as K


def rng_for(*key):
    h = hashlib.sha256(("|".join(str(k) for k in (K.SEED,) + key)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def hm(m):
    m = int(round(m)) % (24 * 60)
    return "%02d:%02d" % (m // 60, m % 60)


def day_type(d):
    if d in K.BANK_HOLIDAYS:
        return "SU"
    return "SU" if d.weekday() == 6 else ("SA" if d.weekday() == 5 else "WD")


def time_band(d, minute, inbound):
    if day_type(d) != "WD":
        return 4
    if 6 * 60 + 30 <= minute < 9 * 60 + 30:
        return 0
    if 16 * 60 + 30 <= minute < 19 * 60:
        return 2
    if minute >= 19 * 60:
        return 3
    return 1


def fare_table():
    """Fares by flow and ticket type, before and after the change of 4 January 2026, in pence: each ticket type's
    scale on the flow's distance, rounded to 10p, and the change applied and rounded to 10p again."""
    out = {}
    for g in K.GROUP_ORDER:
        calls = K.GROUPS[g]["calls"]
        for i, (a, ma) in enumerate(calls):
            for b, mb in calls[i + 1:]:
                key = tuple(sorted((a, b)))
                if any((key, tt) in out for tt in K.TICKETS):
                    continue
                km = abs(mb - ma) * 0.95
                base = {"Season": 2050 + 330 * km, "Anytime": 390 + 21.5 * km, "Off-Peak": 280 + 14.2 * km,
                        "Advance": 220 + 9.1 * km}
                for tt in K.TICKETS:
                    before = int(round(base[tt] / 10.0)) * 10
                    after = int(round(before * (1 + K.FARE_CHANGE[tt] / 100.0) / 10.0)) * 10
                    out[(key, tt)] = (before, after)
    return out


FARES = fare_table()


def fare_change(a, b, ticket):
    before, after = FARES[(tuple(sorted((a, b))), ticket)]
    return (after / before - 1.0) * 100.0


class Timetable:
    """One working timetable: every train's calls with public times (local), by day type."""

    def __init__(self, label, recast):
        self.label = label
        self.trains = []          # dicts: uid, headcode, group, dir, daytype, calls [(station, arr_min, dep_min)]
        rg = rng_for("tt", label)
        uid_base = {"Dec24": 41000, "Dec25": 57000}[label]
        n = 0
        for g in K.GROUP_ORDER:
            calls = K.GROUPS[g]["calls"]
            run = calls[-1][1]
            extra = {"MAIN": 2, "LINK": 3}.get(g, 0) if recast else 0     # the Dec25 recast adds running time
            for dtp in ("WD", "SA", "SU"):
                deps = self.departures(g, dtp, recast)
                for direction in ("up", "down"):
                    seq = calls if direction == "down" else [(s, run - m) for s, m in reversed(calls)]
                    offs = 0 if direction == "down" else {"MAIN": 25, "VALE": 20, "COAST": 30, "BRANCH": 28, "LINK": 34}[g]
                    for i, d0 in enumerate(deps):
                        start = d0 + offs
                        cl = []
                        for j, (st, m) in enumerate(seq):
                            t = start + m * (1 + extra / max(run, 1)) if m else start
                            arr = None if j == 0 else round(t)
                            dep = None if j == len(seq) - 1 else round(t) + (1 if 0 < j else 0)
                            cl.append((st, arr, dep))
                        n += 1
                        self.trains.append(dict(uid="C%05d" % (uid_base + n), group=g, dir=direction, daytype=dtp,
                                                calls=cl, start=start, idx=i))
        # the last train out of each group's hub, timed to reach the far end just before midnight
        for g in K.GROUP_ORDER:
            calls = K.GROUPS[g]["calls"]
            run = calls[-1][1]
            extra = {"MAIN": 2, "LINK": 3}.get(g, 0) if recast else 0
            arrive = {"MAIN": 23 * 60 + 56, "VALE": 23 * 60 + 55, "COAST": 23 * 60 + 57, "BRANCH": 23 * 60 + 56,
                      "LINK": 23 * 60 + 58}[g]
            start = arrive - round(run * (1 + extra / max(run, 1)))
            for dtp in ("WD", "SA", "SU"):
                cl = []
                for j, (st, m) in enumerate(calls):
                    t = start + m * (1 + extra / max(run, 1)) if m else start
                    arr = None if j == 0 else round(t)
                    dep = None if j == len(calls) - 1 else round(t) + (1 if 0 < j else 0)
                    cl.append((st, arr, dep))
                n_late = {"WD": 0, "SA": 1, "SU": 2}[dtp] + 3 * K.GROUP_ORDER.index(g)
                self.trains.append(dict(uid="C%05d" % (uid_base + 900 + n_late), group=g, dir="down", daytype=dtp,
                                        calls=cl, start=start, idx=99))
        self.assign_headcodes(rg, recast)

    @staticmethod
    def departures(g, dtp, recast):
        first, last = {"MAIN": (6 * 60, 22 * 60), "VALE": (6 * 60 + 15, 22 * 60 + 15),
                       "COAST": (6 * 60 + 40, 21 * 60 + 40), "BRANCH": (6 * 60 + 50, 22 * 60 + 50),
                       "LINK": (6 * 60 + 5, 21 * 60 + 5)}[g]
        if dtp == "SU":
            first += 120
        base = list(range(first, last + 1, 60))
        if dtp != "WD":
            return base
        peaks = []
        if g in ("MAIN", "VALE", "LINK") or (g == "COAST" and recast):
            for m in base:
                if 6 * 60 + 30 <= m <= 8 * 60 + 45 or 16 * 60 + 15 <= m <= 18 * 60 + 15:
                    peaks.append(m + 30)
        return sorted(base + peaks)

    def assign_headcodes(self, rg, recast):
        """Headcodes are reused across groups' day types; the Dec25 timetable renumbers each group from a new
        start, so a 2025 headcode names another train in 2026."""
        for g in K.GROUP_ORDER:
            pre = K.GROUPS[g]["prefix"]
            for dtp in ("WD", "SA", "SU"):
                for direction in ("up", "down"):
                    ts = sorted([t for t in self.trains if t["group"] == g and t["daytype"] == dtp and t["dir"] == direction],
                                key=lambda t: t["start"])
                    base = (10 if direction == "down" else 50) + (7 if recast else 0)
                    for k, t in enumerate(ts):
                        t["headcode"] = "%s%02d" % (pre, (base + k) % 100)

    def for_day(self, d):
        dtp = day_type(d)
        return [t for t in self.trains if t["daytype"] == dtp]


class World:
    def __init__(self):
        self.tt = {"Dec24": Timetable("Dec24", False), "Dec25": Timetable("Dec25", True)}
        self.fleet = self.make_fleet()
        self.unit_by_no = {u["unit"]: u for u in self.fleet}
        self.runs = []            # one dict per train run on a day
        for d in K.ALL_DAYS:
            tt = self.tt["Dec24"] if d < K.TIMETABLE_CHANGE else self.tt["Dec25"]
            for t in tt.for_day(d):
                self.runs.append(dict(date=d, t=t, uid=t["uid"], headcode=t["headcode"], group=t["group"]))
        self.diagrams()
        self.formations()
        self.demand()
        self.movements()
        self.crew()

    # ---------------------------------------------------------------- fleet
    def make_fleet(self):
        units = []
        for i in range(12):        # class 166: six go off lease at the October 2025 cascade
            units.append(dict(unit="166%03d" % (201 + i), cls="166", off=K.CASCADE if i >= 6 else None, on=None))
        for i in range(22):        # class 158: four refurbished in summer 2026 (fewer seats, cycle space)
            units.append(dict(unit="158%03d" % (831 + i), cls="158", off=None, on=None))
        for i in range(16):        # class 150/2: twelve arrive at the cascade
            units.append(dict(unit="150%03d" % (241 + i), cls="150/2", off=None, on=K.CASCADE if i >= 4 else None))
        refurb = [("158834", dt.date(2026, 6, 1), dt.date(2026, 6, 26)), ("158838", dt.date(2026, 6, 29), dt.date(2026, 7, 24)),
                  ("158841", dt.date(2026, 7, 27), dt.date(2026, 8, 21)), ("158845", dt.date(2026, 8, 24), dt.date(2026, 9, 18))]
        for u in units:
            u["refurb"] = None
            for un, a, b in refurb:
                if u["unit"] == un:
                    u["refurb"] = (a, b)
        return units

    def unit_class(self, unit, d):
        u = self.unit_by_no[unit]
        if u["refurb"] and d >= u["refurb"][1]:
            return "158/9"
        return u["cls"]

    def available(self, cls, d):
        out = []
        for u in self.fleet:
            if u["cls"] != cls:
                continue
            if u["off"] and d >= u["off"]:
                continue
            if u["on"] and d < u["on"]:
                continue
            if u["refurb"] and u["refurb"][0] <= d < u["refurb"][1]:
                continue
            if rng_for("maint", d.isoformat(), u["unit"]).random() < 0.07:
                continue
            out.append(u["unit"])
        return out

    # ---------------------------------------------------------------- diagrams and formations
    def lead_class(self, g, d, k):
        """The class a group's k-th diagram is planned on: VALE lost its class 166s at the cascade, COAST kept
        them on its first three diagrams."""
        if g in ("MAIN", "LINK"):
            return "158"
        if g == "BRANCH":
            return "150/2"
        if d < K.CASCADE:
            return "166"
        if g == "COAST" and k < 3:
            return "166"
        return "150/2"

    @staticmethod
    def chain(rs):
        """Chain runs into unit workings: a unit turns at a terminal after 8 minutes or more."""
        rs = sorted(rs, key=lambda r: r["t"]["start"])
        chains = []
        for r in rs:
            first = r["t"]["calls"][0]
            for c in chains:
                prev = c[-1]["t"]
                if prev["calls"][-1][0] == first[0] and prev["calls"][-1][1] + 8 <= first[2]:
                    c.append(r)
                    break
            else:
                chains.append([r])
        return chains

    def diagrams(self):
        by_day = {}
        for r in self.runs:
            by_day.setdefault((r["date"], r["group"]), []).append(r)
        for (d, g), rs in by_day.items():
            for k, c in enumerate(self.chain(rs)):
                for r in c:
                    r["diagram"] = "%s%03d" % (g[0] + g[-1], 101 + k)
                    r["diag_k"] = k

    def formations(self):
        """Units per run, without a unit in two places: one lead unit per diagram, then the units left over
        strengthen the peak trains planned for two units, chain by chain; chains the day's pool cannot cover run
        short-formed on their lead unit alone."""
        self.unit_by_no = {u["unit"]: u for u in self.fleet}
        self.substitutions = []
        days_ = sorted({r["date"] for r in self.runs})
        by_day = {}
        for r in self.runs:
            by_day.setdefault(r["date"], []).append(r)
        for d in days_:
            rs = by_day[d]
            pools = {}
            for cls in ("166", "158", "150/2"):
                pool = self.available(cls, d)
                rng_for("pool", d.isoformat(), cls).shuffle(pool)
                pools[cls] = pool
            lead = {}
            for g in K.GROUP_ORDER:
                ks = sorted({r["diag_k"] for r in rs if r["group"] == g})
                for k in ks:
                    cls = self.lead_class(g, d, k)
                    for c2 in (cls, "158", "150/2", "166"):
                        if pools[c2]:
                            lead[(g, k)] = pools[c2].pop(0)
                            if c2 != cls:
                                self.substitutions.append((d, g, k, cls, c2))
                            break
            for r in rs:
                u = lead[(r["group"], r["diag_k"])]
                r["units"] = [u]
            for g in K.GROUP_ORDER:
                need = []
                for r in rs:
                    if r["group"] != g or time_band(d, r["t"]["start"], True) not in (0, 2):
                        continue
                    cls = self.unit_class(r["units"][0], d)
                    if g in ("MAIN", "LINK") or (cls == "150/2" and g in ("VALE", "COAST")):
                        need.append(r)
                for c in self.chain(need):
                    cls = "158" if g in ("MAIN", "LINK") else "150/2"
                    if pools[cls]:
                        u = pools[cls].pop(0)
                        for r in c:
                            r["units"].append(u)
                            r.setdefault("tag", {})[u] = c[0]["headcode"]   # the attached unit's recorder keeps
                                                                             # the headcode it was attached under
                    else:
                        for r in c:
                            r["short"] = True
            for r in rs:
                r.setdefault("short", False)
                r["seats"] = sum(K.CLASSES[self.unit_class(u, d)][1] for u in r["units"])

    # ---------------------------------------------------------------- passengers
    BOARD = {   # passengers boarding per station per train, by group, inbound peak (scaled by band and direction)
        "MAIN": 83.0, "VALE": 46.0, "COAST": 40.0, "BRANCH": 18.0, "LINK": 68.0}
    GROWTH = {"MAIN": 1.18, "VALE": 1.07, "COAST": 1.05, "BRANCH": 1.04, "LINK": 1.17}

    def demand(self):
        """Each run's passengers by origin and destination (Poisson), its load after every departure."""
        for r in self.runs:
            t, d, g = r["t"], r["date"], r["group"]
            calls = [c[0] for c in t["calls"]]
            n = len(calls)
            inbound = calls[-1] in ("MVC", "SEN")
            band = time_band(d, t["start"], inbound)
            hub = n - 1 if inbound else 0
            bf = {0: 1.0 if inbound else 0.40, 1: 0.30, 2: 1.0 if not inbound else 0.38, 3: 0.19, 4: 0.33}[band]
            if day_type(d) == "SU":
                bf *= 0.85
            grow = self.GROWTH[g] if d >= K.WAVES[2026][0] else 1.0
            if d >= K.LATEST[0]:
                grow *= 1.02
            base = self.BOARD[g] * bf * grow
            rg = rng_for("od", d.isoformat(), r["uid"])
            day_f = float(np.exp(rg.normal(0, 0.16)))
            od = np.zeros((n, n), dtype=int)
            for i in range(n - 1):
                dests = np.arange(i + 1, n)
                w = np.where(dests == hub, 3.2, 1.0) * (1.0 + 0.15 * (dests - i))
                lam = base * day_f * (1.25 if i == 0 and not inbound else 1.0) * (0.55 if inbound and i == 0 else 1.0)
                if not inbound and i == 0:
                    lam *= 3.0
                tot = rg.poisson(lam)
                if tot:
                    od[i, dests] = rg.multinomial(tot, w / w.sum())
            load = [int(od[:i + 1, i + 1:].sum()) for i in range(n - 1)]
            r["od"] = od
            r["load"] = load                 # passengers on board after departing call i (i = 0 .. n-2)

    # ---------------------------------------------------------------- movements
    def movements(self):
        """Delay at the origin and along the run, cancellations in full or part. The Dec25 recast on MAIN and
        LINK lengthened the run but dwell times run longer than planned, so lateness rises there."""
        for r in self.runs:
            t, d, g = r["t"], r["date"], r["group"]
            rg = rng_for("mv", d.isoformat(), r["uid"])
            u = rg.random()
            r["cancel"] = None
            if u < 0.011:
                r["cancel"] = "full"
            elif u < 0.017:
                r["cancel"] = "part"
            worse = 1.0
            if d >= K.TIMETABLE_CHANGE and g in ("MAIN", "LINK"):
                worse = 1.9
            elif d >= K.TIMETABLE_CHANGE:
                worse = 1.25
            x = rg.random()
            delay = 0.0 if x < 0.62 else (rg.uniform(0, 2.5) if x < 0.90 else (rg.uniform(2, 7) if x < 0.975 else rg.uniform(5, 22)))
            acts = []
            for j, (st, arr, dep) in enumerate(t["calls"]):
                if j:
                    delay = max(0.0, delay + rg.normal(0.12 * worse, 0.40 * worse) + (rg.exponential(2.5 * worse) if rg.random() < 0.02 * worse else 0.0) - 0.12)
                a = None if arr is None else arr + delay
                dd = None if dep is None else dep + delay + (rg.uniform(0, 0.8) if j else 0)
                acts.append((st, a, dd))
            if r["cancel"] == "part":
                stop = int(rg.integers(1, len(acts) - 1))
                acts = acts[:stop + 1]
                acts[-1] = (acts[-1][0], acts[-1][1], None)
            r["acts"] = acts

    # ---------------------------------------------------------------- crew
    def crew(self):
        """On-board staff by run. In the waves (the as-worked archive) every train carried a conductor unless the
        turn went uncovered until the February 2026 host model, after which VALE, COAST and BRANCH trains carry a
        host on part of their diagrams. In the baseline window (the new rostering platform) a turn belongs to a
        diagram: rostered, or off sick or never filled, when a spare may cover it by amendment."""
        host_from = dt.date(2026, 2, 8)
        latest = set(K.WINDOWS["latest"])
        turns = {}
        for r in self.runs:
            d, g = r["date"], r["group"]
            if d in latest:
                key = (d, r["diagram"])
                if key not in turns:
                    rg = rng_for("turn", d.isoformat(), r["diagram"])
                    conductor = g in ("MAIN", "LINK")
                    exists = rg.random() < (0.97 if conductor else 0.46)
                    t = None
                    if exists:
                        u = rg.random()
                        status = "Rostered" if u < 0.88 else ("Sick" if u < 0.96 else "Vacant")
                        staff = "%s%05d" % ("C" if conductor else "H", int(rg.integers(10000, 99999))) if status != "Vacant" else ""
                        cover = ""
                        if status != "Rostered" and rg.random() < 0.6:
                            cover = "S%05d" % int(rg.integers(10000, 99999))
                        eve = bool(cover) and (status == "Vacant" or rg.random() < 0.45)   # a vacancy is known the day before
                        t = dict(grade="Conductor" if conductor else "Host", staff=staff, status=status, cover=cover,
                                 reason={"Sick": "Sickness", "Vacant": "Vacancy"}.get(status, ""),
                                 logged=hm(int(rg.integers(19 * 60, 22 * 60 + 30)) if eve else
                                           int(rg.integers(4 * 60 + 30, 7 * 60))),
                                 logged_day_before=eve)
                    turns[key] = t
                t = turns[key]
                r["turn"] = t
                r["staffed"] = bool(t and (t["status"] == "Rostered" or t["cover"]))
                r["role"] = t["grade"] if r["staffed"] else ""
                r["staff_ref"] = (t["staff"] if t["status"] == "Rostered" else t["cover"]) if r["staffed"] else ""
                continue
            rg = rng_for("crew", d.isoformat(), r["diagram"])
            r2 = rng_for("crewrun", d.isoformat(), r["uid"])
            if d < host_from or g in ("MAIN", "LINK"):
                p_none = 0.10 if g in ("BRANCH",) else 0.085
                if d >= host_from:
                    p_none = 0.17
                role = "Conductor"
            else:
                p_none = {"VALE": 0.64, "COAST": 0.60, "BRANCH": 0.55}[g]
                role = "Host"
            r["staffed"] = bool(r2.random() >= p_none)
            r["role"] = role if r["staffed"] else ""
            r["staff_ref"] = ("%s%05d" % ("C" if role == "Conductor" else "H", int(rg.integers(10000, 99999)))) if r["staffed"] else ""
