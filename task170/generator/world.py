"""task170 world: Corran Vale Railways (fictional, Arnhallow) from the first ETCS go-live (4 March 2024) to the
record's end (31 October 2026), and the six Phase 4 depots that go live from February to June 2027.

What the record carries and the decision turns on: every Start of Mission on an ETCS-fitted unit is logged by the
on-board recorder with the staff number the driver enters, and a driver's chance of a train data entry error at a
Start of Mission falls with the number of ETCS starts the driver has made before it (a shifted power law). The
suburban and intercity diagrams of Phases 1 to 3 run a driver past several hundred starts within months; the rural
Phase 4 diagrams give each driver about a third of that pace, so the forward drivers spend much of their first year
where the record's drivers spent their first weeks. The record's spare-turn drivers, instructors and managers ran up
starts slowly inside fast depots and err at their count, not at their month. Nothing in the record names it.

The asks' worlds: the Class 461 fitment programme for the Phase 4 fleet (vehicles fitted one at a time, units reformed
so fitted vehicles run together, the contractor's records keeping the programme's own unit numbers) and the other
ETCS driver events of 2026 (level transition errors and brake interventions), reported by drivers, signallers and,
without a link, by the recorder downloads in the recorder's own time (UTC)."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

import numpy as np

import common as C

# the error probability per Start of Mission at a driver's n-th ETCS start (n from 0): F (C0 + A0 (1 + n / S0)^-B0),
# times the driver's own error-proneness (lognormal, sd 0.25 on the log scale)
CURVE = dict(F=1.72, C0=0.0026, A0=0.024, S0=60.0, B0=1.6, FRAIL=0.25)
LTR_P, BRK_P = 0.0014, 0.0021          # per service start, flat: the asks' events
OBR_CAPTURE, DRIVER_REPORT = 0.88, 0.72
REPEAT_LTR, REPEAT_BRK = 0.26, 0.18    # a second event on the return working, same driver, unit and day
SLOW_LINKS = ("SPARE", "INSTR", "MGR", "RESTR")


def p_err(n, frail=1.0):
    k = CURVE
    return k["F"] * (k["C0"] + k["A0"] * (1.0 + np.asarray(n, float) / k["S0"]) ** (-k["B0"])) * frail


def month_iter(start, end):
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        a = max(start, dt.date(y, m, 1))
        nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
        b = min(end, nxt - dt.timedelta(days=1))
        yield a, b
        y, m = nxt.year, nxt.month


class Driver:
    __slots__ = ("pid", "numbers", "depots", "link", "contract", "dob", "qualified", "pace", "frail", "start",
                 "end", "shift", "phase4", "moves", "pace4")


class World:
    def __init__(self):
        self.g = C.stream("world")
        self._units()
        self._record_drivers()
        self._phase4_drivers()
        self._starts()
        self._errors()
        self._events()
        self._duties()
        self._fleet461()

    # ------------------------------------------------------------------ units on the Phase 1 to 3 routes
    def _units(self):
        self.units384 = {}
        k = 1
        for code in C.REC_CODES:
            self.units384[code] = ["384%03d" % (k + i) for i in range(12)]
            k += 12

    # ------------------------------------------------------------------ people
    def _new_number(self, depot, used):
        g = self.g
        while True:
            s = "%02d%04d" % (C.BLOCK[depot], int(g.integers(100, 10000)))
            if s not in used:
                used.add(s)
                return s

    def _person(self, depot, link, contract, start, used, pace_base, phase4=False):
        g = self.g
        d = Driver()
        d.pid = len(self.people)
        d.numbers = [(start, self._new_number(depot, used))]
        d.depots = [(start, depot)]
        d.link, d.contract = link, contract
        age = int(g.integers(24, 64))
        d.dob = dt.date(2026 - age, int(g.integers(1, 13)), int(g.integers(1, 29)))
        yrs = int(min(g.integers(1, 40), age - 21))
        d.qualified = dt.date(2026 - yrs, int(g.integers(1, 13)), int(g.integers(1, 29)))
        d.frail = float(g.lognormal(0, CURVE["FRAIL"]))
        d.pace = self._pace(link, contract, pace_base, phase4)
        d.start, d.end, d.phase4, d.moves, d.pace4 = start, C.RECORD_END, phase4, [], None
        d.shift = int(g.integers(0, 3))
        self.people.append(d)
        return d

    def _pace(self, link, contract, base, phase4):
        g = self.g
        if link == "MAIN":
            v = base * g.lognormal(0, 0.15 if phase4 else 0.18)
            if contract == "PT":
                v *= 0.72
            return float(np.clip(v, 24, 66) if phase4 else v)
        lo, hi = {"SPARE": (5, 14) if phase4 else (6, 20), "INSTR": (6, 12) if phase4 else (8, 18),
                  "MGR": (3, 7) if phase4 else (4, 10), "RESTR": (4, 9) if phase4 else (5, 12)}[link]
        return float(np.exp(g.uniform(np.log(lo), np.log(hi))))

    def _link(self, phase4):
        g = self.g
        r = g.random()
        cuts = (0.82, 0.92, 0.96, 0.98) if phase4 else (0.78, 0.90, 0.94, 0.97)
        link = "MAIN" if r < cuts[0] else "SPARE" if r < cuts[1] else "INSTR" if r < cuts[2] else \
            "MGR" if r < cuts[3] else "RESTR"
        contract = "PT" if link == "MAIN" and g.random() < 0.06 else "FT"
        return link, contract

    def _record_drivers(self):
        g = self.g
        self.people = []
        self.used = set()
        self.base = {}
        for code, name, ph, golive in C.RECORD_DEPOTS:
            self.base[code] = float(g.uniform(95, 160))
            for _ in range(int(g.integers(34, 51))):
                link, contract = self._link(False)
                self._person(code, link, contract, golive, self.used, self.base[code])
            # newly qualified drivers joining after go-live
            for _ in range(int(g.integers(3, 7))):
                start = golive + dt.timedelta(days=int(g.integers(40, (C.RECORD_END - golive).days - 60)))
                self._person(code, "MAIN", "FT", start, self.used, self.base[code])
        rec = [p for p in self.people]
        # leavers: retirements and resignations, about four in a hundred a year
        for p in rec:
            span = (C.RECORD_END - p.start).days
            if g.random() < 0.04 * span / 365.0:
                p.end = p.start + dt.timedelta(days=int(g.integers(30, max(31, span - 5))))
        # transfers between record depots (Resourcing issues a number in the new depot's block)
        movers = [p for p in rec if p.end == C.RECORD_END and p.link == "MAIN"]
        g.shuffle(movers)
        for p in movers[:9]:
            here = p.depots[0][1]
            to = [c for c in C.REC_CODES if c != here and C.DEPOT[c][3] < p.start + dt.timedelta(days=200)]
            to = [c for c in to if c != here]
            if not to:
                continue
            dest = to[int(g.integers(len(to)))]
            when = p.start + dt.timedelta(days=int(g.integers(120, max(121, (C.RECORD_END - p.start).days - 60))))
            if when < C.DEPOT[dest][3]:
                when = C.DEPOT[dest][3] + dt.timedelta(days=7)
            if when >= C.RECORD_END - dt.timedelta(days=30):
                continue
            p.numbers.append((when, self._new_number(dest, self.used)))
            p.depots.append((when, dest))
            p.moves.append((when, here, dest))
            p.pace = float(self.base[dest] * g.lognormal(0, 0.18))
        self.movers_rec = [p for p in rec if p.moves]

    def _phase4_drivers(self):
        g = self.g
        self.base4 = {}
        for code, name, ph, golive in C.PHASE4_DEPOTS:
            self.base4[code] = float(g.uniform(32, 46))
            for _ in range(int(g.integers(38, 53))):
                link, contract = self._link(True)
                self._person(code, link, contract, dt.date(2025, 12, 1), self.used, self.base4[code], phase4=True)
        # one or two drivers from the record depots move to each Phase 4 depot in late 2025, carrying their ETCS starts
        rec = [p for p in self.people if not p.phase4 and p.end == C.RECORD_END and not p.moves and p.link == "MAIN"
               and p.start < dt.date(2025, 6, 1)]
        g.shuffle(rec)
        k = 0
        self.movers_p4 = []
        for code in C.P4_CODES:
            for _ in range(1 + int(g.random() < 0.5)):
                p = rec[k]
                k += 1
                when = dt.date(2025, int(g.integers(11, 13)), int(g.integers(1, 28)))
                here = p.depots[-1][1]
                p.numbers.append((when, self._new_number(code, self.used)))
                p.depots.append((when, code))
                p.moves.append((when, here, code))
                p.phase4 = True
                p.pace4 = float(np.clip(self.base4[code] * g.lognormal(0, 0.15), 24, 66))
                self.movers_p4.append(p)
        # fleet technicians who run test starts
        self.techs = ["%02d%04d" % (C.FLEET_BLOCK, x) for x in g.choice(np.arange(1000, 9999), 24, replace=False)]

    # ------------------------------------------------------------------ Starts of Mission on the recorders
    def number_on(self, p, day):
        cur = p.numbers[0][1]
        for when, num in p.numbers:
            if day >= when:
                cur = num
        return cur

    def depot_on(self, p, day):
        cur = p.depots[0][1]
        for when, dep in p.depots:
            if day >= when:
                cur = dep
        return cur

    def _starts(self):
        """each record driver's ETCS starts, month by month at the driver's pace, timestamped in UTC"""
        g = C.stream("starts")
        rows = []                       # (utc datetime, pid or -1, staff number, unit, cab, type)
        for p in self.people:
            if p.phase4 and not p.moves:
                continue
            end = p.end
            if p.moves and p.phase4:
                end = min(end, p.moves[-1][0] - dt.timedelta(days=1))
            if end < p.start:
                continue
            for a, b in month_iter(p.start, end):
                dep = self.depot_on(p, a)
                if C.DEPOT[dep][2] == 4:
                    continue
                days = (b - a).days + 1
                lam = p.pace * days / 30.44
                u = int(g.poisson(lam))
                if u == 0:
                    continue
                dd = g.integers(0, days, u)
                shift_start = [5.0, 10.5, 15.0][(p.shift + a.month) % 3]
                hrs = shift_start + g.uniform(0, 8.6, u)
                secs = (hrs * 3600).astype(int)
                locs = sorted(dt.datetime.combine(a + dt.timedelta(days=int(dd[i])), dt.time(0, 0))
                              + dt.timedelta(seconds=int(secs[i])) for i in range(u))
                # a driver's next start is at least five minutes after the last (a cab change takes that long)
                for j in range(1, u):
                    if (locs[j] - locs[j - 1]).total_seconds() < 300:
                        locs[j] = locs[j - 1] + dt.timedelta(seconds=300 + (j * 53) % 300)
                for i in range(u):
                    local = locs[i]
                    day = local.date()
                    t = C.local_to_utc(local)
                    unit = self.units384[dep][int(g.integers(12))]
                    rows.append((t, p.pid, self.number_on(p, day), unit, "AB"[int(g.integers(2))],
                                 "DPT" if g.random() < 0.14 else "SVC"))
        # test starts by fleet technicians at the depots, after each depot's go-live
        for code, name, ph, golive in C.RECORD_DEPOTS:
            ndays = (C.RECORD_END - golive).days
            for _ in range(int(ndays * 0.9)):
                day = golive + dt.timedelta(days=int(g.integers(ndays)))
                local = dt.datetime.combine(day, dt.time(int(g.integers(7, 18)), int(g.integers(60)), int(g.integers(60))))
                rows.append((C.local_to_utc(local), -1, self.techs[int(g.integers(len(self.techs)))],
                             self.units384[code][int(g.integers(12))], "AB"[int(g.integers(2))], "TST"))
        rows.sort(key=lambda r: (r[0], r[3], r[2]))
        self.starts = rows
        # each driver's count before each start, over every ETCS start the driver made at any depot
        count = defaultdict(int)
        self.start_n = []
        for r in rows:
            if r[1] >= 0:
                self.start_n.append(count[r[1]])
                count[r[1]] += 1
            else:
                self.start_n.append(-1)
        self.prior = dict(count)

    # ------------------------------------------------------------------ train data entry errors and their reports
    def _errors(self):
        g = C.stream("errors")
        fr = np.array([p.frail for p in self.people])
        n = np.array(self.start_n)
        pid = np.array([r[1] for r in self.starts])
        drv = n >= 0
        pr = np.zeros(len(n))
        pr[drv] = p_err(n[drv], fr[pid[drv]])
        hit = g.random(len(n)) < pr
        self.errors = [int(i) for i in np.where(hit & drv)[0]]          # indices into starts
        kinds = ["Train length", "Train category", "Maximum speed", "Brake percentage", "Axle load category",
                 "Train running number", "Loading gauge"]
        reports = []
        for i in self.errors:
            t, pid, staff, unit, cab, typ = self.starts[i]
            local = C.utc_to_local(t)
            ref = "SM%09d" % (i + 104000000)
            rep = []
            drv = g.random() < 0.62
            sig = g.random() < (0.25 if typ == "SVC" else 0.03)
            fleet = (not drv and not sig) or g.random() < 0.02
            what = kinds[int(g.choice(len(kinds), p=[0.30, 0.18, 0.16, 0.14, 0.10, 0.08, 0.04]))]
            if drv:
                rep.append(("Driver", local + dt.timedelta(minutes=float(g.uniform(2, 40))),
                            ref if g.random() < 0.85 else ""))
            if sig:
                rep.append(("Signaller", local + dt.timedelta(minutes=float(g.uniform(1, 8))), ""))
            if fleet:
                d = local.date() + dt.timedelta(days=int(g.integers(1, 10)))
                rep.append(("Fleet data check", dt.datetime.combine(d, dt.time(int(g.integers(9, 16)), int(g.integers(60)))), ref))
            rep.sort(key=lambda x: x[1])
            dep = self.depot_on(self.people[pid], local.date())
            for j, (who, when, sref) in enumerate(rep):
                reports.append(dict(cat="TDE", who=who, when=when, ref=sref, staff=staff, unit=unit, depot=dep,
                                    primary=(j == 0), event=("TDE", i), what="Train data: " + what.lower()))
        # reports withdrawn on review (no error): a driver's or signaller's report of a correct entry
        n_w = int(0.03 * len(self.errors))
        drv_starts = [i for i, n in enumerate(self.start_n) if n >= 0]
        for i in g.choice(drv_starts, n_w, replace=False):
            t, pid, staff, unit, cab, typ = self.starts[i]
            local = C.utc_to_local(t)
            reports.append(dict(cat="TDE", who=["Driver", "Signaller"][int(g.integers(2))],
                                when=local + dt.timedelta(minutes=float(g.uniform(2, 30))), ref="", staff=staff,
                                unit=unit, depot=self.depot_on(self.people[pid], local.date()), primary=True,
                                event=("WD", int(i)), what="Train data: train length", withdrawn=True))
        self.tde_reports = reports

    # ------------------------------------------------------------------ the asks' events: level transitions, brakes
    def _events(self):
        g = C.stream("events")
        evs = []
        svc = np.array([i for i, (r, n) in enumerate(zip(self.starts, self.start_n)) if n >= 0 and r[5] == "SVC"])
        for cat, pr in (("LTR", LTR_P), ("BRK", BRK_P)):
            for i in svc[g.random(len(svc)) < pr]:
                t = self.starts[int(i)][0] + dt.timedelta(minutes=float(g.uniform(6, 55)))
                evs.append((cat, t, int(i)))
                # the same driver meets the same transition or the same speed board on the return working with the
                # same unit later that day: a second event
                if g.random() < (REPEAT_LTR if cat == "LTR" else REPEAT_BRK):
                    evs.append((cat, t + dt.timedelta(minutes=float(g.uniform(70, 200))), int(i)))
        evs.sort(key=lambda e: (e[1], e[0], e[2]))
        reports = []
        for k, (cat, t, i) in enumerate(evs):
            _, pid, staff, unit, cab, typ = self.starts[i]
            local = C.utc_to_local(t)
            dep = self.depot_on(self.people[pid], local.date())
            rep = []
            if g.random() < OBR_CAPTURE:
                rep.append(("OBR download", t.replace(second=0, microsecond=0)))        # the recorder's own time
            if g.random() < DRIVER_REPORT:
                rep.append(("Driver", local + dt.timedelta(minutes=float(g.uniform(1, 25)))))
            if cat == "LTR" and g.random() < 0.22:
                rep.append(("Signaller", local + dt.timedelta(minutes=float(g.uniform(0.5, 6)))))
            if not rep:
                rep.append(("Driver", local + dt.timedelta(minutes=float(g.uniform(1, 25)))))
            manual = sorted([x for x in rep if x[0] != "OBR download"], key=lambda x: x[1])
            what = {"LTR": ["Level transition not acknowledged", "Level transition: wrong level selected",
                            "Level transition: entered unfitted area without acknowledgement"],
                    "BRK": ["Brake intervention: overspeed", "Brake intervention: end of authority approached",
                            "Brake intervention: release speed exceeded"]}[cat]
            text = what[int(g.integers(len(what)))]
            for x in rep:
                is_obr = x[0] == "OBR download"
                primary = is_obr or (manual and x is manual[0])
                reports.append(dict(cat=cat, who=x[0], when=x[1], ref="", staff=staff, unit=unit, depot=dep,
                                    primary=primary, event=(cat, k), what=text))
        # trackside and radio faults the signallers report (not driver events)
        for code, name, ph, golive in C.RECORD_DEPOTS:
            ndays = (C.RECORD_END - golive).days
            for _ in range(int(ndays * 0.12)):
                day = golive + dt.timedelta(days=int(g.integers(ndays)))
                when = dt.datetime.combine(day, dt.time(int(g.integers(5, 23)), int(g.integers(60))))
                cat = "TRK" if g.random() < 0.6 else "RBC"
                reports.append(dict(cat=cat, who="Signaller", when=when, ref="", staff="",
                                    unit=self.units384[code][int(g.integers(12))], depot=code, primary=True,
                                    event=(cat, -1), what="Balise group fault" if cat == "TRK" else "Radio connection lost"))
        self.events = evs
        self.event_reports = reports

    # ------------------------------------------------------------------ the Phase 4 depots' 2026 duties
    def _duties(self):
        g = C.stream("duties")
        rows = []
        self.p4_drivers = [p for p in self.people if p.phase4]
        days = [C.DUTY_START + dt.timedelta(days=i) for i in range((C.DUTY_END - C.DUTY_START).days + 1)]
        for p in self.p4_drivers:
            dep = p.depots[-1][1]
            pace = getattr(p, "pace4", None) or p.pace
            worked = [d for d in days if g.random() < (0.68 if p.link == "MAIN" else 0.62)]
            per = pace * len(days) / 30.44 / max(1, len(worked))
            absent = None
            if g.random() < 0.05:                                    # a long absence
                s = int(g.integers(0, len(days) - 60))
                absent = (days[s], days[s] + dt.timedelta(days=int(g.integers(28, 90))))
            for d in worked:
                if absent and absent[0] <= d <= absent[1]:
                    continue
                ca = int(g.poisson(per))
                duty = "%s-%03d" % (dep, int(g.integers(101, 199)))
                status = "Cancelled" if g.random() < 0.03 else "Worked"
                staff = self.number_on(p, d)
                if status == "Worked" and g.random() < 0.05:
                    rows.append((d, staff, dep, duty, int(g.poisson(per)), "Worked", 1))
                    rows.append((d, staff, dep, duty, ca, "Worked", 2))
                else:
                    rows.append((d, staff, dep, duty, ca, status, 1))
        rows.sort(key=lambda r: (r[0], r[2], r[3], r[1], r[6]))
        self.duties = rows

    # ------------------------------------------------------------------ Class 461 and the Phase 4 fitment programme
    def _fleet461(self):
        g = C.stream("fleet")
        n_by = {c: int(g.integers(10, 15)) for c in C.P4_CODES}
        units, k = [], 1
        for c in C.P4_CODES:
            for _ in range(n_by[c]):
                units.append(dict(base="461%03d" % k, a="51%03d" % k, b="52%03d" % k, depot=c))
                k += 1
        # refurbished units renumbered 461/0 to 461/1 in mid-2025, three again to 461/2 in 2026
        renum = []
        refurb = sorted(g.choice(len(units), 30, replace=False))
        for i in refurb:
            u = units[i]
            new = "4611" + u["base"][4:]
            renum.append((u["base"], new, dt.date(2025, int(g.integers(6, 10)), int(g.integers(1, 28))), "Refurbishment"))
            u["now"] = new
        for i in refurb[:3]:
            u = units[i]
            new = "4612" + u["base"][4:]
            renum.append((u["now"], new, dt.date(2026, int(g.integers(3, 9)), int(g.integers(1, 28))), "Interior upgrade"))
            u["now"] = new
        for u in units:
            u.setdefault("now", u["base"])
        # vehicle acceptance dates: done ones before the record's end, the rest planned up to mid-2027
        golive = {c: C.DEPOT[c][3] for c in C.P4_CODES}
        veh = {}

        def done():
            return dt.date(2026, 1, 5) + dt.timedelta(days=int(g.integers(0, 290)))

        def before(gl):
            return C.RECORD_END + dt.timedelta(days=int(g.integers(10, max(11, (gl - C.RECORD_END).days - 5))))

        def after(gl):
            return gl + dt.timedelta(days=int(g.integers(7, 120)))
        # each depot's programme: two or three pairs of units left half fitted when the B-end and A-end kits ran
        # short in 2026 (one unit with its A-end fitted and its B-end due after go-live, one the other way round)
        for c in C.P4_CODES:
            gl = golive[c]
            mine = [u for u in units if u["depot"] == c]
            order = list(g.permutation(len(mine)))
            npair = int(g.integers(2, 4))
            nlate = int(g.integers(1, 3))
            for j, u in enumerate(mine):
                pos = order.index(j)
                if pos < 2 * npair:
                    first = pos % 2 == 0
                    da, db = (done(), after(gl)) if first else (after(gl), done())
                elif pos < 2 * npair + nlate:
                    # neither vehicle fitted yet, one booked into the works before go-live and one after it
                    da, db = (before(gl), after(gl)) if g.random() < 0.5 else (after(gl), before(gl))
                else:
                    da, db = [done() if r < 0.40 else before(gl) if r < 0.80 else after(gl) for r in g.random(2)]
                    # a unit whose two vehicles fall either side of the cutoff with one already fitted is not left
                    # half fitted by the programme: its second vehicle is brought forward to before go-live
                    if (da <= C.RECORD_END < db and db > gl) or (db <= C.RECORD_END < da and da > gl):
                        if db > gl:
                            db = before(gl)
                        else:
                            da = before(gl)
                veh[u["a"]] = dict(vehicle=u["a"], unit=u["base"], end="A", accepted=da)
                veh[u["b"]] = dict(vehicle=u["b"], unit=u["base"], end="B", accepted=db)
        # reformations by the fleet team at each depot: a fitted A-end and a fitted B-end whose partners are still to be
        # fitted after the depot's go-live are put together, and their unfitted partners together
        form = {u["now"]: [u["a"], u["b"]] for u in units}
        depot_of = {u["now"]: u["depot"] for u in units}
        self.reformed = []
        for c in C.P4_CODES:
            gl = golive[c]
            half_a = [u for u in units if u["depot"] == c and veh[u["a"]]["accepted"] <= C.RECORD_END
                      and veh[u["b"]]["accepted"] > gl]
            half_b = [u for u in units if u["depot"] == c and veh[u["b"]]["accepted"] <= C.RECORD_END
                      and veh[u["a"]]["accepted"] > gl]
            for ua, ub in zip(half_a, half_b):
                form[ua["now"]] = [ua["a"], ub["b"]]
                form[ub["now"]] = [ub["a"], ua["b"]]
                self.reformed.append((c, ua["now"], ub["now"]))
        self.units461 = units
        self.veh461 = veh
        self.form461 = form
        self.depot461 = depot_of
        self.renum461 = renum
        self.golive = golive
