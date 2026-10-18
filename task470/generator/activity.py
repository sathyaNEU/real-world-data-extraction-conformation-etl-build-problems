"""Every aircraft's year: flights and the operations they make at the valley's fields, with local and UTC times.

Calibrated per field so that the piston-airplane lead the receiver network can hear (based and visiting aircraft that
broadcast) meets the field's target, and the operations of the based piston airplanes that never broadcast meet
K_TARGET operations per such airplane (spread by a field's own small departure from it).
"""
import datetime as dt

import numpy as np

import fleet as FL
import world as W

MONTH_W = np.array([0.55, 0.60, 0.80, 1.00, 1.20, 1.35, 1.40, 1.35, 1.15, 0.95, 0.65, 0.55])
DAYS = [dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range(365)]
PAD_DAYS = [dt.date(2025, 12, 30), dt.date(2025, 12, 31), dt.date(2027, 1, 1), dt.date(2027, 1, 2)]


def _day_weights(role):
    w = np.array([MONTH_W[d.month - 1] for d in DAYS])
    wk = np.array([d.weekday() for d in DAYS])
    if role in ("private", "nd", "visitor"):
        w = w * np.where(wk >= 5, 1.7, 0.85)
    elif role == "school":
        w = w * np.where(wk == 6, 0.35, 1.0)
    elif role in ("charter", "turbine"):
        w = w * np.where(wk >= 5, 0.7, 1.1)
    return w / w.sum()


DAYW = {r: _day_weights(r) for r in ("private", "nd", "school", "charter", "turbine", "visitor")}


def flight_lead(cls, n_tg):
    """Lead (g) of a local flight at its field: one departure, n touch-and-goes (two operations each), one arrival."""
    if cls not in ("single", "multi"):
        return 0.0
    L = W.LEAD
    return L[(cls, "departure")] + L[(cls, "arrival")] + 2 * n_tg * L[(cls, "touch_and_go")]


def _op_lead(cls, kind):
    if cls not in ("single", "multi"):
        return 0.0
    return W.LEAD[(cls, kind)]


class Year:
    def __init__(self, x, seed=4711):
        self.x = x
        self.ac = x["aircraft"]
        self.rng = np.random.default_rng(seed)
        self.flights = []        # (aid, kind, role, n_tg or destination), the year's flights
        self.ops = []            # (aid, lid, local datetime, kind, itinerant flag, flight id); flight id dropped at the end
        self.fid = 0

    # ------------------------------------------------------------------ helpers
    def _begin(self):
        self.fid += 1

    def _op(self, aid, lid, t, kind, itin):
        self.ops.append((aid, lid, t, kind, itin, self.fid))

    def _when(self, d, role):
        r = self.rng
        if role == "nd":
            h = r.uniform(9.0, 16.5)
        elif role == "school":
            h = r.uniform(8.0, 18.5)
        elif role in ("charter", "turbine"):
            h = r.uniform(5.5, 21.5)
        else:
            lo, hi = (8.0, 19.5) if 4 <= d.month <= 9 else (8.5, 16.5)
            h = r.uniform(lo, hi)
        return dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(h * 60))

    def _active_window(self, a):
        lo = a.get("arrives_on", dt.date(2026, 1, 1))
        hi = dt.date(2026, 12, 31)
        if "leaves_on" in a:
            hi = a["leaves_on"] - dt.timedelta(days=1)
        if "exported_on" in a:
            hi = a["exported_on"] - dt.timedelta(days=3)
        if "cancelled_on" in a:
            hi = a["cancelled_on"] - dt.timedelta(days=1)
        return lo, hi

    def _pick_day(self, a, role):
        lo, hi = self._active_window(a)
        w = DAYW[role].copy()
        mask = np.array([lo <= d <= hi for d in DAYS])
        w = w * mask
        return DAYS[int(self.rng.choice(365, p=w / w.sum()))]

    def _dest(self, home, weight_by="B"):
        lids = [f["lid"] for f in W.F if f["lid"] != home]
        w = np.array([W.BY_LID[l]["B"] ** 0.8 for l in lids], dtype=float)
        return lids[int(self.rng.choice(len(lids), p=w / w.sum()))]

    def local_flight(self, a, role, n_tg, day=None):
        if day is None:
            self.flights.append((a["id"], "local", role, n_tg))
        d = day or self._pick_day(a, role if role in DAYW else "private")
        t = self._when(d, role)
        self._begin()
        self._op(*(a["id"], a["home"], t, "departure", False))
        for i in range(n_tg):
            t = t + dt.timedelta(minutes=int(6 + self.rng.integers(0, 3)))
            self._op(*(a["id"], a["home"], t, "touch_and_go", False))
        t = t + dt.timedelta(minutes=int(8 + self.rng.integers(0, 40)))
        self._op(*(a["id"], a["home"], t, "arrival", False))

    def cross_country(self, a, role, dest=None, day=None):
        if day is None:
            self.flights.append((a["id"], "xc", role, dest))
        d = day or self._pick_day(a, role if role in DAYW else "private")
        t = self._when(d, role)
        home = a["home"]
        self._begin()
        if home:
            self._op(*(a["id"], home, t, "departure", True))
        if dest is None and home and not a.get("mover"):
            dest = self._dest(home) if self.rng.random() < 0.6 else None
        leg = dt.timedelta(minutes=int(25 + self.rng.integers(0, 70)))
        if dest:
            t = t + leg
            self._op(*(a["id"], dest, t, "arrival", True))
            t = t + dt.timedelta(minutes=int(30 + self.rng.integers(0, 180)))
            self._op(*(a["id"], dest, t, "departure", True))
        else:
            t = t + dt.timedelta(minutes=int(80 + self.rng.integers(0, 300)))
        if home:
            t = t + leg
            self._op(*(a["id"], home, t, "arrival", True))

    # ------------------------------------------------------------------ the year
    def run(self):
        r = self.rng
        ac = self.ac
        by_home = {}
        for a in ac:
            by_home.setdefault(a["home"], []).append(a)
        # 1. itinerant flying by aircraft that broadcast
        for a in ac:
            if (not a["broadcasts"] and a["piston_airplane"]) or not a["active"]:
                continue
            role = a["role"]
            if a.get("mover"):
                # the airplanes whose number moved: busy at home until the move, away only out of the valley
                for _ in range(int(r.integers(20, 40))):
                    self.cross_country(a, "charter" if role != "mover" else "private", dest=None)
                if role == "survey":
                    for _ in range(int(r.integers(320, 360))):
                        self.local_flight(a, "charter", 0)
                else:
                    for _ in range(int(r.integers(150, 190))):
                        self.local_flight(a, "charter" if role == "charter" else "private",
                                          int(r.choice([0, 0, 1, 2])))
                continue
            if role in ("visitor", "strip"):
                if not a["broadcasts"]:
                    continue
                for _ in range(int(r.integers(1, 8) if role == "visitor" else r.integers(2, 10))):
                    dest = self._dest(None)
                    self.flights.append((a["id"], "visit", "visitor", dest))
                    d = self._pick_day(a, "visitor")
                    t = self._when(d, "visitor")
                    self._begin()
                    self._op(*(a["id"], dest, t, "arrival", True))
                    self._op(*(a["id"], dest, t + dt.timedelta(minutes=int(40 + r.integers(0, 240))),
                                     "departure", True))
                continue
            if a["family"] == "glider":
                continue
            if role == "charter":
                n = int(r.integers(75, 130))
                for _ in range(n):
                    self.cross_country(a, "charter", dest=None if r.random() < 0.85 else self._dest(a["home"]))
                continue
            if a["cls"] == "turbine":
                for _ in range(int(r.integers(15, 45))):
                    self.cross_country(a, "turbine")
                continue
            if a["cls"] == "rotor":
                for _ in range(int(r.integers(20, 60))):
                    self.local_flight(a, "private", 0)
                for _ in range(int(r.integers(3, 12))):
                    self.cross_country(a, "private")
                continue
            if role == "towplane":
                continue
            if role == "school":
                for _ in range(int(r.integers(8, 18))):
                    self.cross_country(a, "school", dest=self._dest(a["home"]))
                continue
            for _ in range(int(max(1, r.lognormal(np.log(4), 0.6)))):
                self.cross_country(a, "private")
        # glider tows at Lanthorne
        gl = [a for a in ac if a["home"] == "L08" and a["family"] in ("glider", "towplane")]
        tow = [a for a in gl if a["family"] == "towplane"][0]
        for _ in range(130):
            d = self._pick_day(tow, "private")
            t = self._when(d, "private")
            for g in gl:
                if g["family"] == "glider" and r.random() < 0.5:
                    self._begin()
                    self._op(*(g["id"], "L08", t, "departure", False))
                    self._op(*(g["id"], "L08", t + dt.timedelta(minutes=int(30 + r.integers(0, 60))),
                                     "arrival", False))
                    break
            self._begin()
            self._op(*(tow["id"], "L08", t, "departure", False))
            self._op(*(tow["id"], "L08", t + dt.timedelta(minutes=int(12 + r.integers(0, 8))), "arrival",
                             False))
        # 2. local flying by broadcasting based piston airplanes, to each field's heard-lead target
        heard = self.heard_lead()
        for f in W.F:
            lid = f["lid"]
            need = f["H"] * 1000.0 - heard.get(lid, 0.0)
            pool = [a for a in by_home.get(lid, []) if a["broadcasts"] and a["piston_airplane"] and a["active"]
                    and a["role"] in ("private", "school", "charter") and not a.get("mover")]
            schools = [a for a in pool if a["role"] == "school"]
            privates = [a for a in pool if a["role"] != "school"]
            if need < 0:
                raise SystemExit("field %s already over its heard target by %.0f g" % (lid, -need))
            # schools take most of a school field's local flying
            share_sch = 0.80 if f["kind"] == "school" else (0.55 if schools else 0.0)
            budgets = [(schools, need * share_sch, "school"), (privates, need * (1 - share_sch), "private")]
            filled = 0.0
            for grp, budget, role in budgets:
                if not grp or budget <= 0:
                    continue
                wts = r.lognormal(0, 0.6 if role == "private" else 0.2, len(grp))
                wts = wts / wts.sum()
                for a, w in zip(grp, wts):
                    target = budget * w
                    got = 0.0
                    while got < target - 0.5:
                        if role == "school":
                            n_tg = int(r.choice([3, 4, 5, 6, 7, 8]))
                        else:
                            n_tg = int(r.choice([0, 0, 0, 1, 2, 3, 4], p=[0.2, 0.2, 0.15, 0.15, 0.12, 0.1, 0.08]))
                        lead = flight_lead(a["cls"], n_tg)
                        if got + lead > target + 0.5:
                            # finish with the smallest flight that fits
                            for n2 in range(n_tg, -1, -1):
                                if got + flight_lead(a["cls"], n2) <= target + 0.5:
                                    self.local_flight(a, role, n2)
                                    got += flight_lead(a["cls"], n2)
                                    break
                            else:
                                break
                            continue
                        self.local_flight(a, role, n_tg)
                        got += lead
                    filled += got
            # top up to the field's target with full-stop circuits by its broadcasting single-engine airplanes
            singles = [a for a in pool if a["cls"] == "single"]
            left = need - filled
            while left >= flight_lead("single", 0) and singles:
                a = singles[int(r.integers(0, len(singles)))]
                self.local_flight(a, "school" if a["role"] == "school" else "private", 0)
                left -= flight_lead("single", 0)
        # 3. local flying by the based piston airplanes that never broadcast, to K_TARGET per airplane
        rr = np.random.default_rng(4729)
        eps_other = {f["lid"]: float(rr.uniform(-0.06, 0.06)) for f in W.F}
        self.missing_target = {}
        for f in W.F:
            lid = f["lid"]
            nd = [a for a in by_home.get(lid, []) if not a["broadcasts"] and a["piston_airplane"]]
            eps = W.K_EPS.get(lid, eps_other[lid])
            target_ops = W.K_TARGET * len(nd) * (1 + eps)
            self.missing_target[lid] = target_ops
            if not nd:
                continue
            active = [a for a in nd if r.random() > 0.15]
            for a in nd:
                a["active"] = a in active
            if not active:
                continue
            wts = r.lognormal(0, 0.35, len(active))
            wts = wts / wts.sum()
            alloc = np.floor(wts * target_ops / 2.0).astype(int) * 2          # whole flights' worth of ops
            short = int(round(target_ops)) - int(alloc.sum())
            i = 0
            while short >= 2:
                alloc[i % len(alloc)] += 2
                short -= 2
                i += 1
            for a, n_ops in zip(active, alloc):
                left = int(n_ops)
                while left >= 2:
                    n_tg = int(r.choice([0, 0, 1, 2, 3]))
                    n_tg = min(n_tg, (left - 2) // 2)
                    self.local_flight(a, "nd", n_tg)
                    left -= 2 + 2 * n_tg
        # 4. the export's padding days, two either side of the year: each aircraft that broadcasts flies its own kinds
        # of flight at its December or January rate
        self._padding()
        self._overnight()
        self._sequence()
        return self

    def _padding(self):
        r = np.random.default_rng(4733)
        ac = self.ac
        per = {}
        for fl in self.flights:
            per.setdefault(fl[0], []).append(fl)
        idx = {d: i for i, d in enumerate(DAYS)}
        for p in PAD_DAYS:
            twin = dt.date(2026, p.month, p.day)
            for aid in sorted(per):
                a = ac[aid]
                if not a["broadcasts"]:
                    continue
                if p.year == 2025 and "arrives_on" in a:
                    continue
                if p.year == 2027 and any(k in a for k in ("leaves_on", "exported_on", "cancelled_on")):
                    continue
                fls = per[aid]
                key = fls[0][2] if fls[0][2] in DAYW else "private"
                lam = len(fls) * DAYW[key][idx[twin]]
                for _ in range(int(r.poisson(lam))):
                    fl = fls[int(r.integers(0, len(fls)))]
                    if fl[1] == "local":
                        self.local_flight(a, fl[2], fl[3], day=p)
                    elif fl[1] == "xc":
                        self.cross_country(a, fl[2], dest=fl[3], day=p)
                    else:
                        t = self._when(p, "visitor")
                        self._begin()
                        self._op(*(aid, fl[3], t, "arrival", True))
                        self._op(*(aid, fl[3], t + dt.timedelta(minutes=int(40 + r.integers(0, 240))),
                                   "departure", True))

    def _overnight(self):
        """Some trips last more than a day: a based airplane away for one to three nights, a visitor or a valley
        trip staying overnight at the field it flew to. Applied only where the aircraft has no other flight in the
        span and its registration does not change in it."""
        r = np.random.default_rng(4761)
        ac = self.ac
        by = {}
        for o in self.ops:
            by.setdefault(o[5], []).append(o)
        spans = {}
        for fid, ops in by.items():
            ops.sort(key=lambda o: o[2])
            spans.setdefault(ops[0][0], []).append((ops[0][2], ops[-1][2], fid))
        for aid in spans:
            spans[aid].sort()
        stable = lambda a: not any(k in a for k in ("leaves_on", "exported_on", "cancelled_on", "changed_on",
                                                     "arrives_on"))
        moved = {}
        for fid in sorted(by):
            ops = by[fid]
            a = ac[ops[0][0]]
            if not a["broadcasts"] or not stable(a) or a["family"] in ("glider", "towplane"):
                continue
            kinds = [o[3] for o in ops]
            home = a["home"]
            if kinds == ["departure", "arrival"] and ops[0][4] and ops[0][1] == home and ops[1][1] == home:
                if r.random() >= 0.30:
                    continue
                nights = int(r.integers(1, 4))
                d = ops[0][2].date() + dt.timedelta(days=nights)
                back = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(r.uniform(10.5, 19.0) * 60))
                cut = 1
            elif kinds == ["arrival", "departure"] or (len(ops) == 4 and kinds == ["departure", "arrival",
                                                                                   "departure", "arrival"]):
                if r.random() >= (0.35 if kinds[0] == "arrival" else 0.2):
                    continue
                i = 1 if kinds[0] == "arrival" else 2
                d = ops[i - 1][2].date() + dt.timedelta(days=1)
                back = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(r.uniform(8.5, 12.0) * 60))
                cut = i
            else:
                continue
            start = ops[0][2]
            shift = back - ops[cut][2]
            end = ops[-1][2] + shift
            clash = any(fid2 != fid and s2 < end + dt.timedelta(hours=1) and e2 > start - dt.timedelta(minutes=20)
                        for s2, e2, fid2 in spans[a["id"]])
            if clash or shift <= dt.timedelta(0):
                continue
            moved[fid] = (cut, shift)
            spans[a["id"]] = sorted([z for z in spans[a["id"]] if z[2] != fid] + [(start, end, fid)])
        out = []
        for o in self.ops:
            if o[5] in moved:
                cut, shift = moved[o[5]]
                ops = by[o[5]]
                if ops.index(o) >= cut:
                    o = (o[0], o[1], o[2] + shift, o[3], o[4], o[5])
            out.append(o)
        self.ops = out
        self.overnight = len(moved)

    def _sequence(self):
        """An aircraft flies one flight at a time. Flights are placed in the order of their drawn start: a flight
        keeps its time when the aircraft is free, otherwise takes the next free start the same day (ten minutes after
        the last flight ends), otherwise the same time on the nearest free day inside the aircraft's window; a trip
        over several days is one block."""
        import bisect
        by = {}
        for o in self.ops:
            by.setdefault(o[5], []).append(o)
        per = {}
        for fid in sorted(by):
            ops = sorted(by[fid], key=lambda o: o[2])
            per.setdefault(ops[0][0], []).append(ops)
        gap = dt.timedelta(minutes=10)
        out = []
        for aid in sorted(per):
            a = self.ac[aid]
            late = dt.timedelta(hours=23, minutes=30) if a["role"] in ("charter",) or a["cls"] == "turbine" \
                else dt.timedelta(hours=21, minutes=30)
            lo, hi = self._active_window(a) if a["home"] in W.BY_LID or a["role"] in ("visitor", "strip") else \
                (dt.date(2026, 1, 1), dt.date(2026, 12, 31))
            starts, ends = [], []           # placed blocks, sorted by start

            def free(s, e):
                k = bisect.bisect_left(starts, e + gap)
                return k == 0 or ends[k - 1] + gap <= s

            for ops in sorted(per[aid], key=lambda f: (f[0][2], f[0][5])):
                s0, dur = ops[0][2], ops[-1][2] - ops[0][2]
                pad = s0.year != 2026
                place = None
                if free(s0, s0 + dur):
                    place = s0
                else:
                    k = bisect.bisect_left(starts, s0)
                    cand = max(ends[k - 1] + gap, s0) if k else s0
                    day0 = dt.datetime(s0.year, s0.month, s0.day)
                    for _ in range(40):
                        if cand + dur > day0 + late or not free(cand, cand + dur):
                            k = bisect.bisect_right(starts, cand)
                            if k and ends[k - 1] + gap > cand:
                                cand = ends[k - 1] + gap
                                if cand + dur <= day0 + late and free(cand, cand + dur):
                                    place = cand
                                    break
                                continue
                            if cand + dur > day0 + late:
                                break
                        else:
                            place = cand
                            break
                    if place is None:
                        tod = s0 - day0
                        for off in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9, 10, -10]:
                            d = s0.date() + dt.timedelta(days=off)
                            if not pad and not (lo <= d <= hi and d.year == 2026):
                                continue
                            if pad and d.year == 2026:
                                continue
                            c = dt.datetime(d.year, d.month, d.day) + tod
                            if free(c, c + dur):
                                place = c
                                break
                if place is None:
                    place = s0
                sh = place - s0
                k = bisect.bisect_left(starts, place)
                starts.insert(k, place)
                ends.insert(k, place + dur)
                for o in ops:
                    out.append((o[0], o[1], o[2] + sh, o[3], o[4]))
        out.sort(key=lambda o: (o[2], o[1], o[0]))
        self.ops = out

    def heard_lead(self):
        out = {}
        ac = self.ac
        for o in self.ops:
            aid, lid, t, kind = o[0], o[1], o[2], o[3]
            a = ac[aid]
            if not a["broadcasts"] or not a["piston_airplane"] or t.year != 2026:
                continue
            g = _op_lead(a["cls"], kind)
            if kind == "touch_and_go":
                g = 2 * g
            out[lid] = out.get(lid, 0.0) + g
        return out


def simulate():
    x = FL.build()
    y = Year(x).run()
    x["ops"] = y.ops
    x["missing_target"] = y.missing_target
    return x


_CACHE = {}


def world():
    """The simulated world, built once per process."""
    if "x" not in _CACHE:
        _CACHE["x"] = simulate()
    return _CACHE["x"]


if __name__ == "__main__":
    import time
    t0 = time.time()
    x = simulate()
    ops = x["ops"]
    print("%d operation rows (a touch-and-go one row) in %.1f s" % (len(ops), time.time() - t0))
    ac = x["aircraft"]
    by = {}
    for aid, lid, t, kind, itin in ops:
        a = ac[aid]
        n = 2 if kind == "touch_and_go" else 1
        k = "heard" if a["broadcasts"] else "missing"
        if a["piston_airplane"]:
            by.setdefault(lid, {}).setdefault(k, 0)
            by[lid][k] += n
    for f in W.F:
        d = by.get(f["lid"], {})
        print(f["lid"], f["kind"], d.get("heard", 0), d.get("missing", 0), round(x["missing_target"][f["lid"]]))
