"""The clock: which days carry which unit behaviour, where every designed wait sits, the gaps (empty
staffed beds), the planned lists and the background bed turnovers at each level-3 unit.

Everything is built forward. A unit is full except inside a designed gap; a bed that frees is assigned
the same minute (a turnover) unless a gap opens. The simulation in sim.py turns the event lists into
stays. Constraint checks here are cheap guards; checks.py asserts every property on the shipped files.
"""
import bisect
import datetime as dt
from collections import defaultdict

import numpy as np

from common import (DAY, LETTERS, RECORD0, RECORD1, FEED0, CAL1, GO_LIVE, PARALLEL0, PARALLEL1, WINTER0,
                    WINTER1, YEARS, BEDS, CORE_UNITS, FEED_UNITS, lm, day_of, tod, is_list_day, year_of,
                    own_unit, unit_open, crosses_dst, DST_WINDOWS, is_bst, rng)
import plan

LEGACY_END = dt.date(2024, 4, 1)        # last legacy decision date
BST_LEGACY_END = dt.date(2023, 10, 27)  # summer legacy months for the clock rows (clocks change 29 Oct)
WINTER_LEGACY0 = dt.date(2023, 11, 1)
WINTER_LEGACY1 = dt.date(2024, 3, 28)
F_UNIT_END = dt.date(2024, 3, 31)


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


class Unit:
    def __init__(self, code):
        self.code = code
        self.beds = BEDS[code]
        self.events = []          # sorted minutes of every timed event at the unit
        self.frozen = []          # (a, b): no admission or discharge strictly inside, except listed ones
        self.gaps = []            # dicts: open, close, close_kind, ref
        self.slots = []           # dicts: t, kind ('wait_end' | 'planned' | 'bg' | 'gap_close'), ref
        self.planned = []         # dicts: t, ref (readmission patient id or None), tag
        self.swaps = []           # dicts: t, need ('planned' | None), ref
        self.forced = []          # dicts: t, pid (a named patient leaves at t)

    def busy(self, t, tol=3):
        i = bisect.bisect_left(self.events, t - tol)
        return i < len(self.events) and self.events[i] <= t + tol

    def add_event(self, t):
        bisect.insort(self.events, t)

    def events_inside(self, a, b):
        i = bisect.bisect_right(self.events, a)
        return i < len(self.events) and self.events[i] < b

    def in_frozen(self, t):
        for a, b in self.frozen:
            if a < t < b:
                return True
        return False


class World:
    def __init__(self):
        self.r = rng("world")
        self.units = {u: Unit(u) for u in FEED_UNITS}
        self.days = {}
        self.waits = []
        self.gap_windows = []     # (unit, open, close) across the network
        self.golden_iv = []       # (dta, end, wid) of every wait inside the remit
        self.trust_iv = defaultdict(list)   # own-unit trust -> [(dta, end, wid)] of all its long-ish waits
        self.nid = 0
        self.swaps_done = []
        self.waits_by_id = {}

    def index(self):
        self.waits_by_id = {w["wid"]: w for w in self.waits}

    # ------------------------------------------------------------------------------------ days
    def build_days(self):
        r = self.r
        for d in daterange(FEED0, CAL1):
            self.days[d] = {"list": is_list_day(d), "cvac": False, "role": None, "gvac": False,
                            "cgaps": [], "limit": None}
        # C's morning vacancies: most list days in the record
        for d in daterange(RECORD0 - dt.timedelta(days=30), CAL1):
            if self.days[d]["list"] and r.random() < 0.78:
                self.days[d]["cvac"] = True

    def nonlist_days(self, a, b):
        return [d for d in daterange(a, b) if not self.days[d]["list"] and not crosses_dst(lm(d, 0, 0), lm(d, 23, 59))]

    def assign_roles(self):
        """Non-list days that carry an own-unit gap: G, A, F, H, C own-empty waits and the summer
        spurious-wait gaps. Returns role-day lists per (role, year)."""
        r = self.r
        need = {1: {"G": 45, "A": 3, "F": 20, "H": 10 + 2, "SPE": 6},
                2: {"G": 59, "A": 10, "C": 3},
                3: {"G": 52, "A": 7}}
        self.role_days = defaultdict(list)
        for y in (1, 2, 3):
            a, b = YEARS[y]
            pool = self.nonlist_days(a + dt.timedelta(days=1), b - dt.timedelta(days=1))
            r.shuffle(pool)
            used = set()

            def take(cands, n, role):
                cands = [d for d in cands if d not in used and not any(abs((d - u).days) == 0 for u in used)]
                assert len(cands) >= n, (y, role, len(cands), n)
                pick = sorted(cands[:n])
                for d in pick:
                    used.add(d)
                    self.days[d]["role"] = role
                self.role_days[(role, y)] = pick
                return pick

            if y == 1:
                nonpar = [d for d in pool if not (PARALLEL0 <= d <= PARALLEL1)]
                take([d for d in nonpar if d <= BST_LEGACY_END], need[1]["SPE"], "SPE")
                take([d for d in nonpar if WINTER0 <= d <= WINTER1], need[1]["H"], "H")
                take([d for d in nonpar if d <= F_UNIT_END], need[1]["F"], "F")
                first = take([d for d in nonpar if d <= LEGACY_END], 1, "A")
                more = take(pool, need[1]["A"] - 1, "A")
                self.role_days[("A", 1)] = sorted(first + more)
                take(pool, need[1]["G"], "G")
            else:
                for role in ("A", "C"):
                    if role in need[y]:
                        take(pool, need[y][role], role)
                take(pool, need[y]["G"], "G")
        # G days whose 08:00 return already shows the empty bed (opened before 08:00)
        for y in (1, 2, 3):
            gd = list(self.role_days[("G", y)])
            r.shuffle(gd)
            n = {1: 9, 2: 11, 3: 12}[y]
            for d in gd[:n]:
                self.days[d]["gvac"] = True

    # ------------------------------------------------------------------------------- C morning gaps
    def build_c_gaps(self):
        r = self.r
        U = self.units["BRK-ACC"]
        for d in daterange(FEED0, RECORD1):
            info = self.days[d]
            if not info["cvac"] or crosses_dst(lm(d, 4, 0), lm(d, 12, 0)):
                continue
            k = int(r.choice([1, 2, 3], p=[0.45, 0.4, 0.15]))
            opens = sorted(lm(d, 5, 10) + int(x) for x in r.integers(0, 160, size=k))
            closes = sorted(lm(d, 8, 20) + int(x) for x in r.integers(0, 130, size=k))
            for o, c in zip(opens, closes):
                g = {"open": o, "close": c, "close_kind": "bg", "ref": None, "kind": "cmorning"}
                U.gaps.append(g)
                self.gap_windows.append(("BRK-ACC", o, c))
                U.add_event(o)
                U.add_event(c)
            info["cgaps"] = list(zip(opens, closes))
            U.frozen.append((opens[0], closes[-1]))

    def morning_limit(self, d):
        """Latest minute a wait running overnight into date d may end."""
        info = self.days.get(d)
        lim = lm(d, 7, 15)
        if info is None:
            return lim
        for o, _ in info["cgaps"]:
            lim = min(lim, o - 10)
        for (u, o, c) in self.gap_windows:
            if day_of(o) == d and o < lm(d, 12, 0):
                lim = min(lim, o - 10)
        return lim

    # ------------------------------------------------------------------------------- constraints
    def gap_overlap(self, a, b, except_unit=None, pad=0):
        for (u, o, c) in self.gap_windows:
            if u == except_unit:
                continue
            if a - pad < c and b + pad > o:
                return True
        return False

    def own_overlap(self, letter, a, b, pad=10):
        for (x, y, _) in self.trust_iv[letter]:
            if a - pad < y and b + pad > x:
                return True
        return False

    def golden_overlap(self, a, b):
        for (x, y, _) in self.golden_iv:
            if a < y and b > x:
                return True
        return False

    def new_wait(self, **kw):
        w = {"wid": self.nid, "tags": set(), "golden": True, "outcome": "admitted", "unit": None,
             "gap_open": None, "planned_inside": [], "pid": None, "level_req": 3, "level_dec": 3}
        w.update(kw)
        self.nid += 1
        self.waits.append(w)
        return w

    def commit(self, w):
        L = w["letter"]
        d = day_of(w["dta"])
        ou = own_unit(L, d)
        w["own_unit"] = ou
        if ou is not None:
            self.trust_iv[L].append((w["dta"], w["end"], w["wid"]))
        if w["golden"]:
            self.golden_iv.append((w["dta"], w["end"], w["wid"]))

    # ------------------------------------------------------------------------------- the waits
    def build_specs(self):
        """Lay out every wait as a spec, before timing."""
        specs = []
        r = rng("specs")
        # golden device rows (year 1, legacy months)
        dev = defaultdict(list)
        for tag, L, cls, died, n in plan.GOLDEN_DEVICE_ROWS:
            for _ in range(n):
                dev[(L, cls)].append((tag, died))
        for y in (1, 2, 3):
            for L in LETTERS:
                for cls, (n, nd) in plan.COMPOSITION[y][L].items():
                    rows = dev.pop((L, cls), []) if y == 1 else []
                    dd = sum(1 for t, x in rows if x)
                    na = len(rows) - dd
                    assert dd <= nd and na <= n - nd, (y, L, cls)
                    for tag, died in rows:
                        specs.append({"letter": L, "year": y, "cls": cls, "died": died, "tags": {tag}})
                    for i in range(nd - dd):
                        specs.append({"letter": L, "year": y, "cls": cls, "died": True, "tags": set()})
                    for i in range(n - nd - na):
                        specs.append({"letter": L, "year": y, "cls": cls, "died": False, "tags": set()})
        assert not dev, dev
        # capacity waits through which the own unit admitted a transfer the bed bureau allocated
        for y, m in plan.TX_INSIDE.items():
            for L, (kd, ka) in m.items():
                dead = [s for s in specs if s["year"] == y and s["letter"] == L and s["cls"] == "cap"
                        and not s["tags"] and s["died"]]
                alive = [s for s in specs if s["year"] == y and s["letter"] == L and s["cls"] == "cap"
                         and not s["tags"] and not s["died"]]
                assert len(dead) >= kd and len(alive) >= ka, (y, L, len(dead), len(alive))
                for s in dead[:kd] + alive[:ka]:
                    s["tx"] = True
        for (y, L, tag), kd in plan.TX_TAGGED.items():
            dead = [s for s in specs if s["year"] == y and s["letter"] == L and s["cls"] == "cap"
                    and s["tags"] == {tag} and s["died"]]
            assert len(dead) >= kd, (y, L, tag, len(dead))
            for s in dead[:kd]:
                s["tx"] = True
        # deaths before a bed was assigned
        for y, m in plan.DIED_WAITING.items():
            for L, k in m.items():
                cands = [s for s in specs if s["year"] == y and s["letter"] == L and s["died"] and not s["tags"]
                         and s["cls"] == "cap"]
                r.shuffle(cands)
                for s in cands[:k]:
                    s["outcome"] = "died_waiting"
        return specs

    def place_all(self):
        specs = self.build_specs()
        r = self.r
        by = defaultdict(list)
        for s in specs:
            by[(s["year"], s["letter"], s["cls"])].append(s)
        # 0. the spring clock-change nights (DV5), registered before any designed wait
        self.place_dst()
        # 1. own-empty waits on role days
        for y in (1, 2, 3):
            for L, role in (("G", "G"), ("A", "A"), ("F", "F"), ("H", "H"), ("C", "C")):
                ss = by.pop((y, L, "own"), [])
                if not ss:
                    continue
                days = list(self.role_days[(role, y)])
                if L == "H":
                    days = days[:len(ss)]
                assert len(days) >= len(ss), (y, L, len(days), len(ss))
                self.place_own(ss, days, y, L)
        # 2. allocation waits on list days
        for y in (1, 2, 3):
            for L in ("D", "A", "C", "G"):
                ss = by.pop((y, L, "alloc"), [])
                if ss:
                    self.place_alloc(ss, y, L)
        # 3. capacity waits
        caps = []
        for key in sorted(by, key=lambda k: (k[0], k[1])):
            caps.extend(by[key])
        self.place_caps(caps)
        # 4. genuine repeat patients (DV7): a second long wait months later under the same verified key
        self.place_dv7()

    # ------------------------------------------------------------------ own-empty waits (role days)
    def place_own(self, ss, days, y, L):
        r = self.r
        unit = own_unit(L, days[0]) if L != "H" else "PEL-W3"
        # legacy-tagged first, onto legacy days that suit them
        ss = sorted(ss, key=lambda s: (0 if s["tags"] else 1))
        if L == "G" and y == 3:
            # the dead G waits on days whose 08:00 return showed the empty bed: exactly four
            dead = [s for s in ss if s["died"]]
            alive = [s for s in ss if not s["died"]]
            gv = [d for d in days if self.days[d]["gvac"]]
            ng = [d for d in days if not self.days[d]["gvac"]]
            r.shuffle(gv)
            r.shuffle(ng)
            early = lambda d: (YEARS[y][1] - d).days >= 26
            gv = sorted(gv, key=lambda d: not early(d))
            ng = sorted(ng, key=lambda d: not early(d))
            k = plan.Y3_G_OWNVAC_DEATHS
            assign = list(zip(dead[:k], gv[:k])) + list(zip(dead[k:], ng[:len(dead) - k]))
            rest_days = gv[k:] + ng[len(dead) - k:]
            r.shuffle(rest_days)
            assign += list(zip(alive, rest_days))
        else:
            dd = list(days)
            legacy_days = [d for d in dd if d <= LEGACY_END and not (PARALLEL0 <= d <= PARALLEL1)]
            assign = []
            ss = sorted(ss, key=lambda s: (0 if s["tags"] else 1, 0 if s["died"] else 1))
            for s in ss:
                if s["tags"]:
                    pool = [d for d in legacy_days if d in dd]
                    if L == "H":
                        pool = [d for d in pool if WINTER0 <= d <= WINTER1]
                    d = pool[0]
                elif s["died"]:
                    d = [x for x in dd if (YEARS[y][1] - x).days >= 26][0]
                else:
                    d = dd[0]
                dd.remove(d)
                if d in legacy_days:
                    legacy_days.remove(d)
                assign.append((s, d))
        for s, d in assign:
            self.place_one_own(s, d, unit)

    def place_one_own(self, s, d, unit):
        r = self.r
        L = s["letter"]
        U = self.units[unit]
        gvac = self.days[d]["gvac"] and L == "G"
        for attempt in range(400):
            if L == "G":
                g0 = lm(d, 6, 20) + int(r.integers(0, 90)) if gvac else lm(d, 10, 30) + int(r.integers(0, 70))
                dta = lm(d, 11, 45) + int(r.integers(0, 150))
                wmax = min(6 * 60 + 30, lm(d, 18, 40) - dta)
            else:
                g0 = lm(d, 8, 15) + int(r.integers(0, 40))
                dta = max(g0 + 5, lm(d, 8, 30) + int(r.integers(0, 70)))
                wmax = 5 * 60 + 40
            W = int(r.integers(250, max(251, wmax + 1)))
            end = dta + W
            if W < 250 or self.gap_overlap(g0, end) or self.golden_overlap(g0, end):
                continue
            if U.events_inside(g0 - 4, end + 4) or self.own_overlap(L, g0, end):
                continue
            if crosses_dst(g0, end):
                continue
            break
        else:
            raise RuntimeError("own placement failed %s %s" % (L, d))
        w = self.new_wait(letter=L, year=s["year"], cls="own", died=s["died"], tags=set(s["tags"]),
                          dta=dta, end=end, unit=unit, gap_open=g0, outcome="admitted")
        self.commit(w)
        U.gaps.append({"open": g0, "close": end, "close_kind": "wait", "ref": w["wid"], "kind": "own"})
        U.frozen.append((g0, end))
        U.add_event(g0)
        U.add_event(end)
        U.slots.append({"t": end, "kind": "gap_close_wait", "ref": w["wid"]})
        self.gap_windows.append((unit, g0, end))
        return w

    # ------------------------------------------------------------------ allocation waits (list days)
    def alloc_days(self, y, L, n, legacy_tags):
        a, b = YEARS[y]
        cands = [d for d in daterange(a + dt.timedelta(days=1), b - dt.timedelta(days=1))
                 if self.days[d]["list"] and not crosses_dst(lm(d, 0, 0), lm(d, 23, 59))]
        return cands

    def place_alloc(self, ss, y, L):
        r = self.r
        unit = own_unit(L, YEARS[y][0])
        cands = self.alloc_days(y, L, len(ss), None)
        used = {day_of(w["dta"]) for w in self.waits if w["cls"] == "alloc"}
        legacy = [d for d in cands if d <= LEGACY_END and d not in used]
        nonpar = [d for d in legacy if not (PARALLEL0 <= d <= PARALLEL1)]
        par = [d for d in legacy if PARALLEL0 <= d <= PARALLEL1]
        winter = [d for d in nonpar if WINTER_LEGACY0 <= d <= WINTER_LEGACY1]
        r.shuffle(nonpar)
        r.shuffle(par)
        r.shuffle(winter)
        free = [d for d in cands if d not in used]
        r.shuffle(free)
        late = {d for d in cands if (YEARS[y][1] - d).days < 26}
        ss = sorted(ss, key=lambda s: (0 if s["tags"] else 1))
        taken = set(used)
        for s in ss:
            tags = s["tags"]
            if "HZ2" in tags:
                pool = par
            elif "DV1oc" in tags:
                pool = winter
            elif tags:
                pool = nonpar
            else:
                pool = free
            for d in list(pool):
                if d in taken or (s["died"] and d in late):
                    continue
                w = self.try_alloc(s, d, unit)
                if w is not None:
                    taken.add(d)
                    if "DV2b" in tags:
                        # the same patient's second long wait, under the verified key, months later
                        later = [x for x in nonpar if x not in taken and (x - d).days >= 45]
                        if not later:
                            later = [x for x in nonpar if x not in taken and (x - d).days >= 20]
                        for d2 in later:
                            s2 = dict(s, tags={"DV2b2"})
                            w2 = self.try_alloc(s2, d2, unit)
                            if w2 is not None:
                                taken.add(d2)
                                w["pair"] = w2["wid"]
                                w2["pair"] = w["wid"]
                                w["tags"] = {"DV2b1"}
                                break
                        else:
                            raise RuntimeError("DV2b second alloc failed")
                    break
            else:
                raise RuntimeError("alloc placement failed %s %s %s" % (y, L, tags))

    def try_alloc(self, s, d, unit):
        r = self.r
        L = s["letter"]
        winter_oc = "DV1oc" in s["tags"]
        for attempt in range(60):
            dta = lm(d, 10, 45) + int(r.integers(0, 150))
            if L != "D":
                dta = lm(d, 11, 0) + int(r.integers(0, 120))
            if winter_oc:
                W = int(r.integers(250, 291))
            elif d <= LEGACY_END and WINTER_LEGACY0 <= d <= WINTER_LEGACY1:
                W = int(r.integers(310, 400))
            else:
                W = int(r.integers(250, 400))
            end = dta + W
            if end > lm(d, 19, 55):
                continue
            if self.gap_overlap(dta - 5, end + 5) or self.own_overlap(L, dta, end):
                continue
            if crosses_dst(dta, end) or self.units[unit].events_inside(dta - 4, end + 4):
                continue
            # the waiting patient sees planned admissions to its own unit inside the first four hours
            if "HZ1oc" in s["tags"]:
                tp = [dta + int(r.integers(70, min(W - 30, 220)))]
            else:
                k = int(r.choice([1, 2], p=[0.55, 0.45])) if L == "D" else 1
                tp = sorted(dta + int(x) for x in r.choice(np.arange(25, min(W - 20, 235)), size=k, replace=False))
            U = self.units[unit]
            if any(U.busy(t) for t in tp + [end]):
                continue
            w = self.new_wait(letter=L, year=s["year"], cls="alloc", died=s["died"], tags=set(s["tags"]),
                              dta=dta, end=end, unit=unit, outcome="admitted")
            self.commit(w)
            U.frozen.append((dta, end))
            U.add_event(end)
            U.slots.append({"t": end, "kind": "wait_end", "ref": w["wid"]})
            for t in tp:
                U.add_event(t)
                U.planned.append({"t": t, "ref": None, "tag": "inside", "wid": w["wid"],
                                  "readmit": "HZ1oc" in s["tags"]})
            w["planned_inside"] = tp
            return w
        return None

    # ------------------------------------------------------------------ capacity waits
    def day_kind(self, d):
        info = self.days[d]
        if info["list"]:
            return "cvac" if info["cvac"] else "novac"
        if info["role"] in ("G",):
            return "gvac" if info["gvac"] else "role"
        if info["role"]:
            return "role"
        return "plain"

    def vacancy_day(self, d):
        """Any level-3 unit's 08:00 return shows an empty staffed bed on date d."""
        info = self.days[d]
        if info["cvac"]:
            return True
        if info["role"] == "G" and info["gvac"]:
            return True
        return False

    def place_caps(self, caps):
        r = self.r
        rr = rng("caps")
        # timing windows per tag
        tasks = []
        for s in caps:
            tasks.append(s)
        # deterministic order: tagged first, then by year and letter
        tasks.sort(key=lambda s: (0 if s["tags"] else 1, s["year"], s["letter"], sorted(s["tags"])))
        # year-3 day-type quotas
        self.y3_plan = self.plan_y3_days([s for s in tasks if s["year"] == 3 and not s["tags"]])
        for s in tasks:
            self.place_cap(s)
        # non-golden device waits
        self.place_dv4()
        self.place_spurious()

    def plan_y3_days(self, specs):
        """Pick, for each year-3 capacity wait, the kind of day it sits on."""
        r = rng("y3days")
        out = {}
        for L in LETTERS:
            ss = [s for s in specs if s["letter"] == L]
            dead = [s for s in ss if s["died"]]
            alive = [s for s in ss if not s["died"]]
            if L == "C":
                for i, s in enumerate(dead):
                    out[id(s)] = "cvac" if i < plan.Y3_C_VAC_DEATHS else "novac_any"
                for s in alive:
                    out[id(s)] = "cvac" if r.random() < 0.93 else "novac_any"
            elif L == "E":
                for i, s in enumerate(dead):
                    out[id(s)] = "vac_any" if i < plan.Y3_E_VAC_DEATHS else "novac_any"
                for s in alive:
                    out[id(s)] = "vac_any" if r.random() < 0.4 else "novac_any"
            elif L == "A":
                for i, s in enumerate(dead):
                    out[id(s)] = "vac_any" if i < 13 else "novac_any"
                for s in alive:
                    out[id(s)] = "vac_any" if r.random() < 0.35 else "novac_any"
            elif L == "G":
                for s in ss:
                    out[id(s)] = "not_gvac"
            else:
                for s in ss:
                    out[id(s)] = "any"
        return out

    def cap_day_pool(self, s):
        y = s["year"]
        a, b = YEARS[y]
        tags = s["tags"]
        a1, b1 = a + dt.timedelta(days=1), b - dt.timedelta(days=1)
        if "HZ2" in tags:
            a1, b1 = PARALLEL0, PARALLEL1
        elif "DV1oc" in tags:
            a1, b1 = WINTER_LEGACY0, WINTER_LEGACY1
        elif "DV1rc" in tags:
            a1, b1 = dt.date(2023, 7, 3), BST_LEGACY_END
        elif tags:
            a1, b1 = dt.date(2023, 7, 3), dt.date(2024, 3, 30)
        pool = [d for d in daterange(a1, b1) if not crosses_dst(lm(d, 12, 0), lm(d + dt.timedelta(days=1), 9, 0))]
        if tags and "HZ2" not in tags:
            pool = [d for d in pool if not (PARALLEL0 <= d <= PARALLEL1)]
        if s["letter"] == "F" and "HZ2" in tags:
            pool = [d for d in pool if d <= F_UNIT_END]
        if s["letter"] == "H" and "HZ2" in tags:
            pool = [d for d in pool if WINTER0 <= d <= WINTER1]
        if "DV1rc" in tags or "HZ1" in tags:
            pool = [d for d in pool if self.days[d]["list"]]
        if s.get("died"):
            pool = [d for d in pool if (YEARS[y][1] - d).days >= 26]
        if y == 3 and not tags:
            kind = self.y3_plan[id(s)]
            if kind == "cvac":
                pool = [d for d in pool if self.days[d]["cvac"]]
            elif kind == "vac_any":
                pool = [d for d in pool if self.vacancy_day(d)]
            elif kind == "novac_any":
                pool = [d for d in pool if not self.vacancy_day(d)]
            elif kind == "not_gvac":
                pool = [d for d in pool if not self.days[d]["gvac"]]
        elif s["letter"] == "C":
            pool = [d for d in pool if self.days[d]["cvac"] or self.r.random() < 0.15]
        return pool

    def place_cap(self, s):
        r = self.r
        L = s["letter"]
        pool = self.cap_day_pool(s)
        order = list(pool)
        r.shuffle(order)
        for d in order[:400]:
            w = self.try_cap(s, d)
            if w is not None:
                if "DV2b" in s["tags"]:
                    self.place_dv2b_second(w, s)
                return w
        raise RuntimeError("cap placement failed %s" % ({k: v for k, v in s.items() if k != 'tags'}, s["tags"]))

    def place_dv2b_second(self, w, s):
        r = self.r
        d0 = day_of(w["dta"])
        pool = [d for d in daterange(d0 + dt.timedelta(days=45), dt.date(2024, 3, 30))
                if not (PARALLEL0 <= d <= PARALLEL1)]
        if len(pool) < 10:
            pool = [d for d in daterange(dt.date(2023, 7, 3), d0 - dt.timedelta(days=45))
                    if not (PARALLEL0 <= d <= PARALLEL1)]
        r.shuffle(pool)
        s2 = dict(s, tags={"DV2b2"})
        for d in pool:
            w2 = self.try_cap(s2, d)
            if w2 is not None:
                w["pair"] = w2["wid"]
                w2["pair"] = w["wid"]
                w["tags"] = {"DV2b1"}
                return
        raise RuntimeError("DV2b second failed")

    def try_cap(self, s, d):
        r = self.r
        L = s["letter"]
        tags = s["tags"]
        info = self.days[d]
        legacy = d <= LEGACY_END
        bst_legacy = legacy and is_bst(lm(d, 12, 0))
        winter_legacy = legacy and not bst_legacy
        ou = own_unit(L, d)
        for attempt in range(12):
            daytime = (not info["list"]) and info["role"] is None and r.random() < 0.45 and "DV1rc" not in tags
            if "DV1rc" in tags:
                dta = lm(d, 17, 40) + int(r.integers(0, 20))
            elif daytime:
                dta = lm(d, 8, 30) + int(r.integers(0, 300))
            else:
                dta = lm(d, 18, 45) + int(r.integers(0, 300))
            if "DV1oc" in tags:
                W = int(r.integers(250, 291))
            elif winter_legacy:
                W = int(r.integers(310, 470))
            else:
                W = int(r.integers(250, 470))
            end = dta + W
            if daytime:
                if end > lm(d, 19, 30):
                    continue
            else:
                lim = self.morning_limit(d + dt.timedelta(days=1))
                if end > lim:
                    W = lim - dta
                    end = lim
                    if W < 250 or ("DV1oc" in tags and W > 290) or (winter_legacy and "DV1oc" not in tags and W < 310):
                        continue
            if crosses_dst(dta - 70, end + 10):
                continue
            if self.gap_overlap(dta - 5, end + 5):
                continue
            if ou is not None and self.own_overlap(L, dta, end):
                continue
            if ou is not None and self.units[ou].events_inside(dta - 4, end + 4):
                continue
            if bst_legacy and ou is not None and self.gap_overlap(dta - 70, dta, pad=0):
                continue
            # no planned admission may fall inside it; planned admissions are placed later and avoid it
            outcome = s.get("outcome", "admitted")
            if bst_legacy and ou is not None and outcome == "died_waiting":
                outcome = "admitted"
            unit = None
            if outcome == "admitted":
                if ou is not None:
                    unit = ou
                    if self.units[unit].busy(end):
                        continue
                else:
                    unit = self.pick_unit(end, d)
                    if unit is None:
                        continue
            w = self.new_wait(letter=L, year=s["year"], cls="cap", died=s["died"], tags=set(tags), dta=dta,
                              end=end, unit=unit, outcome=outcome)
            self.commit(w)
            if ou is not None:
                self.units[ou].frozen.append((dta, end))
            if unit is not None:
                U = self.units[unit]
                U.add_event(end)
                U.slots.append({"t": end, "kind": "wait_end", "ref": w["wid"]})
            if "DV1rc" in tags:
                # a planned admission to the own unit in the hour before the decision
                tp = dta - int(r.integers(10, 50))
                U = self.units[ou]
                if U.busy(tp) or self.gap_overlap(tp - 1, tp + 1):
                    self.undo(w)
                    continue
                U.add_event(tp)
                U.planned.append({"t": tp, "ref": None, "tag": "DV1rc", "wid": w["wid"], "readmit": False})
                w["planned_before"] = tp
            if "HZ1" in tags:
                # a planned patient moves bed inside the wait; a planned admission earlier that day keeps one present
                ts = dta + int(r.integers(40, W - 40))
                U = self.units[ou]
                if U.busy(ts):
                    self.undo(w)
                    continue
                U.add_event(ts)
                U.swaps.append({"t": ts, "need": "planned", "ref": w["wid"]})
                w["swap_at"] = ts
            if s.get("tx"):
                # a bed frees inside the wait and the bed bureau allocates it to a patient from another trust
                # who had been waiting longer
                U = self.units[ou]
                for k in range(40):
                    tt = dta + int(r.integers(20, 151))
                    if U.busy(tt) or crosses_dst(dta - 250, tt + 5):
                        continue
                    break
                else:
                    self.undo(w)
                    continue
                U.add_event(tt)
                U.slots.append({"t": tt, "kind": "tx_in", "ref": w["wid"]})
                w["tx_at"] = tt
            return w
        return None

    def undo(self, w):
        L = w["letter"]
        self.waits.remove(w)
        self.trust_iv[L] = [x for x in self.trust_iv[L] if x[2] != w["wid"]]
        self.golden_iv = [x for x in self.golden_iv if x[2] != w["wid"]]
        if w["own_unit"] is not None:
            U = self.units[w["own_unit"]]
            U.frozen = [f for f in U.frozen if f != (w["dta"], w["end"])]
        if w["unit"] is not None:
            U = self.units[w["unit"]]
            U.slots = [x for x in U.slots if x.get("ref") != w["wid"]]
            if w["end"] in U.events:
                U.events.remove(w["end"])

    def pick_unit(self, t, d):
        """A unit to admit a patient from a trust without its own level-3 beds at minute t."""
        r = self.r
        units = ["RIS-ACC", "STN-ACC", "BRK-ACC", "PRW-ACC"]
        p = np.array([0.45, 0.2, 0.2, 0.15])
        order = list(r.choice(units, size=4, replace=False, p=p))
        for u in order:
            U = self.units[u]
            if U.in_frozen(t) or U.busy(t):
                continue
            if not unit_open(u, d):
                continue
            return u
        return None

    # ------------------------------------------------------------------ DV4: de-escalated legacy waits
    def place_dv4(self):
        r = rng("dv4")
        for L, kind in plan.DV4_ROWS.items():
            placed = 0
            if kind == "own_dw":
                days = [d for d in self.role_days[("H", 1)]
                        if not any(day_of(w["dta"]) == d and w["cls"] == "own" for w in self.waits)]
                for d in days[:2]:
                    U = self.units["PEL-W3"]
                    for attempt in range(200):
                        g0 = lm(d, 8, 15) + int(r.integers(0, 40))
                        dta = g0 + 5 + int(r.integers(0, 50))
                        W = int(r.integers(260, 330))
                        end = dta + W
                        if self.gap_overlap(g0, end + 95) or self.golden_overlap(g0, end + 95):
                            continue
                        if U.events_inside(g0 - 4, end + 95):
                            continue
                        break
                    else:
                        raise RuntimeError("H DV4 gap")
                    w = self.new_wait(letter=L, year=1, cls="own", died=True, tags={"DV4"}, dta=dta, end=end,
                                      unit=None, outcome="died_waiting", golden=False, level_req=3, level_dec=2)
                    self.commit(w)
                    # the winter level-3 beds stand empty through the wait; closed later by a background admission
                    close = end + int(r.integers(20, 90))
                    U.gaps.append({"open": g0, "close": close, "close_kind": "bg", "ref": None, "kind": "dv4"})
                    U.frozen.append((g0, close))
                    U.add_event(g0)
                    U.add_event(close)
                    self.gap_windows.append(("PEL-W3", g0, close))
                    placed += 1
                assert placed == 2
                continue
            for i in range(2):
                s = {"letter": L, "year": 1, "cls": kind if kind != "dw" else "cap", "died": True,
                     "tags": {"DV4"}, "outcome": "died_waiting" if kind == "dw" else "admitted"}
                pool = [d for d in daterange(dt.date(2023, 7, 3), dt.date(2024, 3, 30))
                        if not (PARALLEL0 <= d <= PARALLEL1)]
                if L == "F":
                    pool = [d for d in pool if d <= F_UNIT_END]
                if kind == "alloc":
                    pool = [d for d in pool if self.days[d]["list"]]
                r.shuffle(pool)
                for d in pool:
                    if kind == "alloc":
                        if any(day_of(w["dta"]) == d and w["cls"] == "alloc" for w in self.waits):
                            continue
                        w = self.try_alloc(s, d, "STN-ACC")
                    else:
                        w = self.try_cap(s, d)
                    if w is not None:
                        w["golden"] = False
                        self.golden_iv = [x for x in self.golden_iv if x[2] != w["wid"]]
                        w["level_req"], w["level_dec"] = 3, 2
                        break
                else:
                    raise RuntimeError("DV4 failed %s" % L)

    # ------------------------------------------------------------------ DV1: summer legacy short waits
    def place_spurious(self):
        r = rng("spurious")
        spe_days = list(self.role_days[("SPE", 1)])
        for L, kind, died in plan.DV1_SPURIOUS:
            ou = own_unit(L, dt.date(2023, 8, 1))
            if kind == "empty":
                d = spe_days.pop(0)
                U = self.units[ou]
                for attempt in range(300):
                    dta = lm(d, 10, 0) + int(r.integers(0, 90))
                    g0 = dta - 60 - int(r.integers(5, 40))
                    W = int(r.integers(190, 231))
                    end = dta + W
                    if self.gap_overlap(g0, end) or self.golden_overlap(g0, end) or self.own_overlap(L, g0, end):
                        continue
                    if U.events_inside(g0 - 4, end + 4):
                        continue
                    break
                else:
                    raise RuntimeError("spurious empty")
                w = self.new_wait(letter=L, year=1, cls="own", died=died, tags={"DV1sp", "DV1sp_empty"}, dta=dta,
                                  end=end, unit=ou, gap_open=g0, golden=False, outcome="admitted")
                self.commit(w)
                U.gaps.append({"open": g0, "close": end, "close_kind": "wait", "ref": w["wid"], "kind": "spe"})
                U.frozen.append((g0, end))
                U.add_event(g0)
                U.add_event(end)
                U.slots.append({"t": end, "kind": "gap_close_wait", "ref": w["wid"]})
                self.gap_windows.append((ou, g0, end))
                continue
            pool = [d for d in daterange(dt.date(2023, 7, 3), BST_LEGACY_END) if self.days[d]["list"]]
            r.shuffle(pool)
            for d in pool:
                if any(day_of(w["dta"]) == d and w["letter"] == L for w in self.waits):
                    continue
                dta = lm(d, 12, 0) + int(r.integers(0, 90))
                W = int(r.integers(190, 231))
                end = dta + W
                if self.gap_overlap(dta - 70, end + 5) or crosses_dst(dta - 70, end):
                    continue
                if ou is not None and self.own_overlap(L, dta - 70, end):
                    continue
                if ou is not None:
                    unit = ou
                    if self.units[unit].busy(end) or self.units[unit].in_frozen(end):
                        continue
                else:
                    unit = self.pick_unit(end, d)
                    if unit is None:
                        continue
                w = self.new_wait(letter=L, year=1, cls="cap", died=died, tags={"DV1sp", "DV1sp_" + kind},
                                  dta=dta, end=end, unit=unit, golden=False, outcome="admitted")
                self.commit(w)
                U = self.units[unit]
                U.add_event(end)
                U.slots.append({"t": end, "kind": "wait_end", "ref": w["wid"]})
                if kind == "planned":
                    tp = dta - int(r.integers(10, 50))
                    U2 = self.units[ou]
                    U2.add_event(tp)
                    U2.planned.append({"t": tp, "ref": None, "tag": "DV1sp", "wid": w["wid"], "readmit": False})
                    w["planned_before"] = tp
                break
            else:
                raise RuntimeError("spurious %s" % L)

    # ------------------------------------------------------------------ DV5: the spring clock-change nights
    def place_dst(self):
        """One wait per trust on the evening before each spring clock change in the record outside the
        latest four quarters. The wall clock reads 4h10 to 4h50, the elapsed wait is an hour shorter. Nothing
        is timed inside the change window itself; the waits span it."""
        r = rng("dv5")
        for day_s, rows in plan.DV5_NIGHTS.items():
            d0 = dt.date.fromisoformat(day_s)
            d1 = d0 + dt.timedelta(days=1)
            night = {}            # this night's DV5 waits per trust: two may share an own unit's empty beds
            for L, kind, died in rows:
                ou = own_unit(L, d0)
                assert (ou is None) == (kind == "none"), (L, kind, d0)
                mine = night.setdefault(L, [])
                mine_ev = {t for w0 in mine for t in (w0["gap_open"], w0["end"]) if t is not None}
                for attempt in range(400):
                    dta = lm(d0, 22, 30) + int(r.integers(0, 100))
                    end = dta + int(r.integers(250, 291))
                    if any(a0 <= x < b0 for a0, b0 in DST_WINDOWS for x in (dta, end)):
                        continue
                    g0 = dta - int(r.integers(20, 61)) if kind == "own" else dta
                    # waits outside the remit: only the own unit's state matters to any reading of them
                    if ou is not None and any(u == ou and g0 - 5 < c and end + 5 > o and not
                                              any(o == w0["gap_open"] for w0 in mine)
                                              for (u, o, c) in self.gap_windows):
                        continue
                    if self.golden_overlap(g0, end):
                        continue
                    if ou is not None:
                        U0 = self.units[ou]
                        others = [x for x in U0.events if g0 - 4 < x < end + 4 and x not in mine_ev]
                        clash = [x for x in (g0, end) for y in mine_ev if abs(x - y) <= 3]
                        if others or clash:
                            continue
                        if any(a - 10 < end and b + 10 > g0 for (a, b, wid) in self.trust_iv[L]
                               if wid not in {w0["wid"] for w0 in mine}):
                            continue
                    if kind == "none":
                        unit = self.pick_unit(end, d1)
                        if unit is None:
                            continue
                    else:
                        unit = ou
                        if self.units[unit].busy(end) or self.units[unit].busy(g0):
                            continue
                    break
                else:
                    raise RuntimeError("dv5 %s %s" % (L, day_s))
                w = self.new_wait(letter=L, year=year_of(d0), cls="own" if kind == "own" else "cap", died=died,
                                  tags={"DV5", "DV5_" + kind}, dta=dta, end=end, unit=unit,
                                  gap_open=g0 if kind == "own" else None, golden=False, outcome="admitted")
                self.commit(w)
                mine.append(w)
                U = self.units[unit]
                if kind == "own":
                    U.gaps.append({"open": g0, "close": end, "close_kind": "wait", "ref": w["wid"], "kind": "dv5"})
                    U.frozen.append((g0, end))
                    U.add_event(g0)
                    U.add_event(end)
                    U.slots.append({"t": end, "kind": "gap_close_wait", "ref": w["wid"]})
                    self.gap_windows.append((unit, g0, end))
                else:
                    if ou is not None:
                        self.units[ou].frozen.append((dta, end))
                    U.add_event(end)
                    U.slots.append({"t": end, "kind": "wait_end", "ref": w["wid"]})

    # ------------------------------------------------------------------ DV7: genuine repeat patients
    def place_dv7(self):
        """Two year-2 survivors per trust come back months later with a second long wait at the same trust,
        under the same verified key, and survive it."""
        r = rng("dv7")
        a2, b2 = YEARS[2]
        for L in LETTERS:
            firsts = [w for w in self.waits if w["letter"] == L and w["year"] == 2 and w["golden"] and not w["tags"]
                      and not w["died"] and w["outcome"] == "admitted" and "tx_at" not in w
                      and w["cls"] in ("cap", "alloc") and day_of(w["dta"]) <= b2 - dt.timedelta(days=120)]
            firsts.sort(key=lambda w: w["dta"])
            picked = 0
            for w1 in firsts[::7]:
                if picked == plan.DV7_PER_TRUST:
                    break
                d1 = day_of(w1["dta"])
                pool = [d for d in daterange(d1 + dt.timedelta(days=45), b2 - dt.timedelta(days=1))
                        if not crosses_dst(lm(d, 0, 0), lm(d + dt.timedelta(days=1), 9, 0))]
                if w1["cls"] == "alloc":
                    used = {day_of(w["dta"]) for w in self.waits if w["cls"] == "alloc"}
                    pool = [d for d in pool if self.days[d]["list"] and d not in used]
                r.shuffle(pool)
                s2 = {"letter": L, "year": 2, "cls": w1["cls"], "died": False, "tags": {"DV7b"}}
                for d in pool[:300]:
                    if w1["cls"] == "alloc":
                        w2 = self.try_alloc(s2, d, w1["unit"])
                    else:
                        w2 = self.try_cap(s2, d)
                    if w2 is not None:
                        break
                else:
                    continue
                w1["tags"] = {"DV7a"}
                w1["pair"], w2["pair"] = w2["wid"], w1["wid"]
                picked += 1
            assert picked == plan.DV7_PER_TRUST, ("dv7", L, picked)

    # ------------------------------------------------------------------ planned lists
    def build_planned(self):
        r = rng("planned")
        nond = [(w["dta"], w["end"]) for w in self.waits if w["letter"] != "D"]
        nond.sort()
        starts = [a for a, b in nond]

        def inside_nond(t):
            i = bisect.bisect_right(starts, t + 70)
            for j in range(max(0, i - 40), i):
                a, b = nond[j]
                if a - 70 < t < b + 5:
                    return True
            return False

        rates = {"STN-ACC": (3, 5, lm(RECORD0, 10, 50) % DAY, lm(RECORD0, 18, 0) % DAY),
                 "RIS-ACC": (0, 2, lm(RECORD0, 10, 30) % DAY, lm(RECORD0, 17, 15) % DAY),
                 "BRK-ACC": (0, 1, lm(RECORD0, 11, 0) % DAY, lm(RECORD0, 16, 30) % DAY),
                 "PRW-ACC": (0, 1, lm(RECORD0, 11, 0) % DAY, lm(RECORD0, 16, 0) % DAY),
                 "ELL-ACC": (0, 1, lm(RECORD0, 11, 0) % DAY, lm(RECORD0, 16, 0) % DAY)}
        probs = {"STN-ACC": None, "RIS-ACC": [0.3, 0.45, 0.25], "BRK-ACC": [0.8, 0.2], "PRW-ACC": [0.9, 0.1],
                 "ELL-ACC": [0.92, 0.08]}
        for d in daterange(FEED0, RECORD1):
            if not self.days[d]["list"]:
                continue
            for u, (lo, hi, t0, t1) in rates.items():
                if not unit_open(u, d):
                    continue
                U = self.units[u]
                if probs[u] is None:
                    k = int(r.integers(lo, hi + 1))
                else:
                    k = int(r.choice(np.arange(lo, hi + 1), p=probs[u]))
                # D already holds the in-wait admissions on its wait days
                if u == "STN-ACC":
                    k -= sum(1 for p in U.planned if day_of(p["t"]) == d)
                for _ in range(max(0, k)):
                    for attempt in range(30):
                        t = lm(d) + t0 + int(r.integers(0, t1 - t0))
                        if U.busy(t) or U.in_frozen(t) or inside_nond(t) or self.gap_overlap(t - 1, t + 1):
                            continue
                        U.add_event(t)
                        U.planned.append({"t": t, "ref": None, "tag": "list", "wid": None, "readmit": False})
                        break
        # a planned patient present through every HZ1 wait (admitted that morning, held past the wait)
        for w in self.waits:
            if "HZ1" in w["tags"]:
                U = self.units[w["own_unit"]]
                d = day_of(w["dta"])
                for attempt in range(300):
                    t = w["dta"] - int(r.integers(150, 600 if attempt < 100 else 1300))
                    if U.busy(t) or U.in_frozen(t) or inside_nond(t) or self.gap_overlap(t - 1, t + 1):
                        continue
                    U.add_event(t)
                    U.planned.append({"t": t, "ref": None, "tag": "hold", "wid": w["wid"], "readmit": False,
                                      "hold_until": w["end"] + 60})
                    break
                else:
                    raise RuntimeError("HZ1 hold")
        # the patient readmitted inside each HZ1oc wait left the unit for theatre hours earlier
        for w in self.waits:
            if "HZ1oc" in w["tags"]:
                U = self.units[w["unit"]]
                p = [x for x in U.planned if x.get("wid") == w["wid"] and x["readmit"]][0]
                for attempt in range(600):
                    t_admit = w["dta"] - int(r.integers(900, 2700))
                    t_leave = w["dta"] - int(r.integers(90, 260))
                    if any(U.busy(x) or U.in_frozen(x) or inside_nond(x) or self.gap_overlap(x - 1, x + 1)
                           for x in (t_admit, t_leave)):
                        continue
                    break
                else:
                    raise RuntimeError("HZ1oc")
                U.add_event(t_admit)
                U.add_event(t_leave)
                rid = "R%d" % w["wid"]
                U.planned.append({"t": t_admit, "ref": rid, "tag": "first", "wid": w["wid"], "readmit": False,
                                  "hold_until": t_leave})
                U.forced.append({"t": t_leave, "pid": rid})
                U.slots.append({"t": t_leave, "kind": "gap_close_bg", "ref": None})
                p["ref"] = rid

    # ------------------------------------------------------------------ background turnovers and swaps
    def build_background(self):
        rates = {"RIS-ACC": 5.0, "BRK-ACC": 2.6, "STN-ACC": 2.2, "PRW-ACC": 2.3, "ELL-ACC": 1.6, "PEL-W3": 0.45}
        hour_w = np.array([0.35, 0.3, 0.25, 0.25, 0.25, 0.3, 0.4, 0.6, 0.9, 1.3, 1.6, 1.7, 1.7, 1.6, 1.6, 1.5, 1.5,
                           1.4, 1.2, 1.0, 0.8, 0.7, 0.55, 0.45])
        hour_p = hour_w / hour_w.sum()
        for u, rate in rates.items():
            r = rng("bg", u)
            U = self.units[u]
            for d in daterange(FEED0, RECORD1):
                if not unit_open(u, d):
                    continue
                k = int(r.poisson(rate))
                for _ in range(k):
                    for attempt in range(8):
                        h = int(r.choice(24, p=hour_p))
                        t = lm(d) + h * 60 + int(r.integers(0, 60))
                        if U.busy(t) or U.in_frozen(t) or any(a <= t < b for a, b in DST_WINDOWS):
                            continue
                        U.add_event(t)
                        U.slots.append({"t": t, "kind": "bg", "ref": None})
                        break
            # C's morning gaps close with background admissions; the winter-bed gap after the DV4 rows too
            for g in U.gaps:
                if g["close_kind"] == "bg":
                    U.slots.append({"t": g["close"], "kind": "gap_close_bg", "ref": None})
        # legacy bed moves (two patients swap beds), outside every own-unit wait
        for u in FEED_UNITS:
            r = rng("swap", u)
            U = self.units[u]
            for d in daterange(FEED0, dt.date(2024, 3, 25)):
                if not unit_open(u, d) or r.random() > {"RIS-ACC": 0.55, "PEL-W3": 0.05}.get(u, 0.35):
                    continue
                for attempt in range(8):
                    t = lm(d, 9, 0) + int(r.integers(0, 660))
                    if U.busy(t) or U.in_frozen(t):
                        continue
                    if any(a - 5 < t < b + 5 for a, b, _ in self.all_own_iv(u)):
                        continue
                    U.add_event(t)
                    U.swaps.append({"t": t, "need": None, "ref": None})
                    break

    def all_own_iv(self, u):
        out = []
        for w in self.waits:
            if w.get("own_unit") == u:
                out.append((w["dta"], w["end"], w["wid"]))
        return out
