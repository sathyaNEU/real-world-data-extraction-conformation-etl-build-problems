"""The world behind task281: lines, holders, rotas and every scheduled shift's status in FY2026, the July 2025
academy class, and the FY2028 position control. Status codes per scheduled line-shift: W worked, V vacant, and the
leave kinds VAC, SICK, IOD (injured on duty), TRN (in-service training), FMLA, MIL."""
import numpy as np
import common as K

D = K.FY26_DAYS
WEEKDAY0 = K.FY26_START.weekday()            # 1 July 2025 is a Tuesday

# per unit: years-of-service mix (share senior), sick base, injury rate, vacation season, FY2026 separations, new
# FY2028 lines and their fill (fiscal week of FY2028, lines filled)
PARAM = {
    "HRC": dict(senior=0.65, sick=0.030, iod=0.050, vac_peak="summer", seps=4, new=3, fill=(16, 3)),
    "ACF": dict(senior=0.55, sick=0.026, iod=0.040, vac_peak="summer", seps=6, new=3, fill=(30, 3)),
    "TWC": dict(senior=0.60, sick=0.028, iod=0.030, vac_peak="holiday", seps=2, new=2, fill=(16, 2)),
    "PCN": dict(senior=0.40, sick=0.022, iod=0.005, vac_peak="summer", seps=4, new=1, fill=(23, 1)),
    "PCS": dict(senior=0.45, sick=0.024, iod=0.005, vac_peak="summer", seps=1, new=2, fill=(23, 2)),
    "FFH": dict(senior=0.55, sick=0.032, iod=0.030, vac_peak="flu", seps=3, new=2, fill=(10, 2)),
    "OXG": dict(senior=0.50, sick=0.020, iod=0.035, vac_peak="summer_only", seps=0, new=1, fill=(40, 1)),
    "KPG": dict(senior=0.50, sick=0.020, iod=0.035, vac_peak="summer_only", seps=0, new=0, fill=None),
}
CLASS_FILLS_FY26 = {"CO": (128, 247), "PCO": (198,), "FSA": (92, 214), "HMW": (99,)}   # day indexes classes post


def weekday(i):
    return (WEEKDAY0 + i) % 7


class World:
    def __init__(self, seed=K.SEED, P=None):
        self.rng = np.random.default_rng(seed)
        self.P = {u: dict(PARAM[u], **((P or {}).get(u, {}))) for u in K.UNIT_CODES}
        self.lines = []          # dicts: id, unit, shift, offset (first day-off weekday), group
        self.emps = {}           # id -> dict(hire_year_service, class, unit, ...)
        self._build_lines()
        self._build_people()
        self._simulate()
        self._fy28()

    # ---------------------------------------------------------------------------------------------- lines and people
    def _build_lines(self):
        for code, name, title, posts in K.UNITS:
            posts = self.P[code].get("posts", posts)
            for s, p in zip(K.SHIFTS, posts):
                groups = p // 5
                n = 0
                for g in range(groups):
                    for k in range(7):
                        n += 1
                        self.lines.append(dict(id="%s-%s%02d" % (code, s, n), unit=code, shift=s, offset=k, group=g))
        self.L = len(self.lines)
        self.on = np.zeros((self.L, D), dtype=bool)          # scheduled to work
        for j, ln in enumerate(self.lines):
            off = {ln["offset"], (ln["offset"] + 1) % 7}
            for i in range(D):
                self.on[j, i] = weekday(i) not in off

    def _build_people(self):
        rng = self.rng
        self.holder = np.full((self.L, D), -1, dtype=int)  # employee index holding the line that day, -1 vacant
        self.people = []                                   # dicts: unit, title, service (years at 1 July 2025), cls
        for j, ln in enumerate(self.lines):
            u = ln["unit"]; P = self.P[u]
            if rng.uniform() < P["senior"]:
                svc = int(rng.integers(6, 28))
            else:
                svc = int(rng.integers(1, 6))
            self.people.append(dict(unit=u, title=K.UNIT_TITLE[u], service=svc, cls=None, start=0, end=D))
            self.holder[j, :] = len(self.people) - 1
        # the July 2025 academy class: a share of each unit's junior lines were vacant on 30 June and are posted on
        # 1 July 2025 to first-year officers
        self.jul25 = []
        for u in K.UNIT_CODES:
            js = [j for j, ln in enumerate(self.lines) if ln["unit"] == u]
            juniors = [j for j in js if self.people[self.holder[j, 0]]["service"] < 6]
            k = max(2, len(js) // 9)
            for j in rng.choice(juniors, size=min(k, len(juniors)), replace=False):
                self.people[self.holder[j, 0]].update(service=0, cls="2025-1")
                self.jul25.append(self.holder[j, 0])
        # FY2026 separations: a holder leaves on a day, the line stands vacant until a later class posts to it
        for u in K.UNIT_CODES:
            P = self.P[u]
            js = [j for j, ln in enumerate(self.lines) if ln["unit"] == u
                  and self.people[self.holder[j, 0]]["cls"] is None]
            fills = CLASS_FILLS_FY26[K.UNIT_TITLE[u]]
            for j in rng.choice(js, size=P["seps"], replace=False):
                leave_day = int(rng.integers(20, 150))
                later = [f for f in fills if f > leave_day + 30]
                fill_day = later[0] if later else int(min(D - 1, leave_day + 200))
                old = self.holder[j, 0]
                self.people[old]["end"] = leave_day
                self.holder[j, leave_day:fill_day] = -1
                self.people.append(dict(unit=u, title=K.UNIT_TITLE[u], service=0, cls="2026-%d" % (1 + fills.index(fill_day)) if fill_day in fills else "lateral",
                                        start=fill_day, end=D))
                self.holder[j, fill_day:] = len(self.people) - 1

    # ---------------------------------------------------------------------------------------------- leave
    def _season(self, kind):
        d = np.arange(D)
        if kind == "summer":
            return 1 + 1.6 * np.exp(-0.5 * ((d - 30) / 18.0) ** 2) + 0.6 * np.exp(-0.5 * ((d - 178) / 6.0) ** 2)
        if kind == "summer_only":
            return 0.2 + 2.6 * np.exp(-0.5 * ((d - 35) / 20.0) ** 2) + 0.4 * (d > 300)
        if kind == "holiday":
            return 1 + 0.6 * np.exp(-0.5 * ((d - 35) / 15.0) ** 2) + 1.8 * np.exp(-0.5 * ((d - 175) / 7.0) ** 2)
        if kind == "flu":
            return 1 + 0.8 * np.exp(-0.5 * ((d - 35) / 15.0) ** 2) + 0.5 * np.exp(-0.5 * ((d - 200) / 25.0) ** 2)
        return np.ones(D)

    def _simulate(self):
        rng = self.rng
        self.status = np.full((self.L, D), "", dtype=object)
        flu = 1 + 0.7 * np.exp(-0.5 * ((np.arange(D) - 205) / 22.0) ** 2)
        for j, ln in enumerate(self.lines):
            u = ln["unit"]; P = self.P[u]
            vs = self._season(P["vac_peak"]); vs = vs / vs.mean()
            e_prev = None
            for i in range(D):
                if not self.on[j, i]:
                    continue
                e = self.holder[j, i]
                if e < 0:
                    self.status[j, i] = "V"; continue
                self.status[j, i] = "W"
            # per holder spell on the line: vacation blocks, sick days, injuries, training
            spells = []
            i0 = 0
            while i0 < D:
                e = self.holder[j, i0]; i1 = i0
                while i1 < D and self.holder[j, i1] == e:
                    i1 += 1
                if e >= 0:
                    spells.append((e, i0, i1))
                i0 = i1
            for e, a, b in spells:
                pe = self.people[e]
                svc = pe["service"]
                first = pe["cls"] is not None and svc == 0
                days = np.array([i for i in range(a, b) if self.on[j, i]])
                if len(days) == 0:
                    continue
                frac = len(days) / max(1, self.on[j].sum())
                # vacation weeks
                if first:
                    vac_h = 40.0 if pe["start"] < 183 else 0.0
                else:
                    vac_h = 80.0 if svc < 2 else 120.0 if svc < 6 else 160.0 if svc < 11 else 200.0 if svc < 16 else 240.0
                vac_h *= frac
                nweeks = int(round(vac_h / 40.0))
                w = vs[days] * (1.0 + (0.6 if svc >= 11 else 0.0) * (vs[days] > 1.3))
                if first:
                    w = np.where(days > 183, 1.0, 1e-6)
                w = w / w.sum()
                for _ in range(nweeks):
                    c = int(rng.choice(days, p=w))
                    for i in range(c, min(b, c + 7)):
                        if self.on[j, i] and self.status[j, i] == "W":
                            self.status[j, i] = "VAC"
                # sick days
                ps = P["sick"] * (0.75 if first else (1.0 + 0.015 * svc)) * flu[days]
                for i, p in zip(days, ps):
                    if self.status[j, i] == "W" and rng.uniform() < p:
                        self.status[j, i] = "SICK"
                # injury on duty: one long spell for some
                if not first and rng.uniform() < P["iod"] * (1.0 + 0.03 * svc) * frac * 4:
                    st = int(rng.choice(days)); ln_days = int(rng.integers(20, 120))
                    for i in range(st, min(b, st + ln_days)):
                        if self.on[j, i] and self.status[j, i] in ("W", "SICK"):
                            self.status[j, i] = "IOD"
                # post-academy field training: a first-year officer spends ten shifts in its first quarter off the post
                if first:
                    n = 0
                    for i in range(a + 10, b):
                        if self.on[j, i] and self.status[j, i] == "W" and rng.uniform() < 0.25:
                            self.status[j, i] = "TRN"; n += 1
                            if n == 10: break
                # in-service training, five shifts in the spring for every holder past their first year
                if not first and b - a > 300:
                    st = int(rng.integers(250, 320))
                    n = 0
                    for i in range(st, b):
                        if self.on[j, i] and self.status[j, i] == "W":
                            self.status[j, i] = "TRN"; n += 1
                            if n == 5: break
                # family and military leave, rare
                if rng.uniform() < 0.04 * frac:
                    st = int(rng.choice(days)); ln_days = int(rng.integers(10, 60))
                    code = "MIL" if rng.uniform() < 0.3 else "FMLA"
                    for i in range(st, min(b, st + ln_days)):
                        if self.on[j, i] and self.status[j, i] == "W":
                            self.status[j, i] = code

    # ---------------------------------------------------------------------------------------------- FY2028
    def _fy28(self):
        """the position control: new lines authorized for FY2028, vacant on 1 July 2027 and filled by a class"""
        self.new_lines = []
        for u in K.UNIT_CODES:
            P = self.P[u]
            if not P["new"]:
                continue
            wk, n = P["fill"]
            for k in range(P["new"]):
                self.new_lines.append(dict(unit=u, id="%s-X%02d" % (u, k + 1), offset=k % 7, fill_week=wk))

    # ---------------------------------------------------------------------------------------------- truth helpers
    def weekly(self, unit, codes):
        js = [j for j, ln in enumerate(self.lines) if ln["unit"] == unit]
        out = np.zeros(K.WEEKS)
        for j in js:
            for i in range(K.WEEKS * 7):
                if self.on[j, i] and self.status[j, i] in codes:
                    out[i // 7] += K.SHIFT_H
        return out

    def availability(self, unit, who):
        js = [j for j, ln in enumerate(self.lines) if ln["unit"] == unit]
        sched = absent = 0.0
        for j in js:
            for i in range(D):
                if not self.on[j, i]:
                    continue
                e = self.holder[j, i]
                if e < 0:
                    continue
                pe = self.people[e]
                if who == "jul25" and pe["cls"] != "2025-1":
                    continue
                if who == "first" and not (pe["cls"] is not None and pe["service"] == 0):
                    continue
                sched += 1
                if self.status[j, i] not in ("W",):
                    absent += 1
        return 1.0 - absent / sched
