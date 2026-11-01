"""task304 architecture 4: the clean truth.

Brolga Parcel Network's six sortation hubs, their workforce, who worked which shift, who staffed which induct
station when (the sorter control system's operator sessions), and each worker's noise exposure computed from the
time they actually spent at induct. Nothing here is mess: pack.py writes the files the organisation keeps.
"""
import datetime as dt
import math
import zoneinfo
from collections import defaultdict

import numpy as np
import pandas as pd
from faker import Faker

import params as P


def lex(t_induct, Li, Lf, La, work=7.0, brk=1.0):
    """LAeq,8h of a shift with t_induct hours at the induct line, the rest of the working time on the floor and the
    breaks in the amenities."""
    t = min(max(t_induct, 0.0), work)
    e = t * 10 ** (Li / 10) + (work - t) * 10 ** (Lf / 10) + brk * 10 ** (La / 10)
    return 10 * math.log10(e / P.SHIFT_HOURS)


def weekdays(a, b):
    d, out = a, []
    while d <= b:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self.fake = Faker("en_AU")
        Faker.seed(seed)
        self.hubs = {h["code"]: h for h in P.HUBS}
        self.days = weekdays(P.LOG_START, P.LOG_END)
        self.people = []        # dicts: pid, kind (EMP/LH/CON), hub, title, team, group
        self.shifts = []        # dicts: pid, hub, date, shift, status (WORKED/LEAVE/SICK)
        self.sessions = []      # dicts: hub, station_no, pid, start_local(datetime naive), end_local, end_type
        self._names = set()
        self.cover_count = defaultdict(int)
        self._build_people()
        self._build_days()

    # ------------------------------------------------------------------ people
    def _name(self):
        while True:
            n = "%s %s" % (self.fake.first_name(), self.fake.last_name())
            if n not in self._names:
                self._names.add(n)
                return n

    def _add(self, **kw):
        kw["pid"] = len(self.people)
        kw["name"] = self._name()
        self.people.append(kw)
        return kw["pid"]

    def _build_people(self):
        rng = self.rng
        self.teams = defaultdict(lambda: defaultdict(list))   # hub -> (team, group) -> [pid]
        relief_count = {"LAR": 2, "ECR": 2, "TRU": 1, "WFD": 0, "KEW": 2, "BFD": 0}
        for code, h in self.hubs.items():
            T = P.TITLES[code]
            for team in ("AM", "PM", "NT"):
                n_ind = h["stations"] + h["spares"]
                for _ in range(n_ind):
                    pid = self._add(kind="EMP", hub=code, title=T["induct"], team=team, group="induct")
                    self.teams[code][(team, "induct")].append(pid)
                for _ in range(relief_count[code]):
                    pid = self._add(kind="EMP", hub=code, title=T["relief"], team=team, group="relief")
                    self.teams[code][(team, "relief")].append(pid)
                # rotation and cover groups drawn from the floor titles
                rot = {"am_rotation": ("loader", 30 if team == "AM" else 0),
                       "sorter_relief": ("sorter", 6),
                       "break_buddies": ("loader", 24),
                       "half_shift": ("loader", h["stations"] + 4),
                       "dedicated": ("loader", 0),
                       "agency_pm": ("loader", 0)}[h["scheme"]]
                n_load = h["loaders"] + int(rng.integers(-3, 4))
                n_sort = h["sorters"] + int(rng.integers(-2, 3))
                for i in range(n_load):
                    grp = "rotation" if (rot[0] == "loader" and i < rot[1]) else "floor"
                    pid = self._add(kind="EMP", hub=code, title=T["loader"], team=team, group=grp)
                    self.teams[code][(team, grp)].append(pid)
                for i in range(n_sort):
                    grp = "rotation" if (rot[0] == "sorter" and i < rot[1]) else "floor"
                    pid = self._add(kind="EMP", hub=code, title=T["sorter"], team=team, group=grp)
                    self.teams[code][(team, grp)].append(pid)
                for _ in range(h["forklift"]):
                    pid = self._add(kind="EMP", hub=code, title=T["forklift"], team=team, group="floor")
                    self.teams[code][(team, "floor")].append(pid)
                for _ in range(h["leads"]):
                    grp = "lead_relief" if h["scheme"] == "agency_pm" else "lead"
                    pid = self._add(kind="EMP", hub=code, title=T["lead"], team=team, group=grp)
                    self.teams[code][(team, grp)].append(pid)
                # labour-hire operatives on the hub's call list for this shift
                n_ag = h["agency"] + (6 if (h["scheme"] == "agency_pm" and team == "PM") else 0)
                for i in range(n_ag):
                    grp = "agency_induct" if (h["scheme"] == "agency_pm" and team == "PM" and i < 13) else "agency_floor"
                    agency = "Tasman Workforce" if rng.random() < 0.6 else "Meridian Labour Hire"
                    pid = self._add(kind="LH", hub=code, title="Operative", team=team, group=grp, agency=agency)
                    self.teams[code][(team, grp)].append(pid)

    # ------------------------------------------------------------------ days
    def _present(self, pids, show):
        rng = self.rng
        return [p for p in pids if rng.random() < show]

    def _build_days(self):
        rng = self.rng
        # a week of annual leave for some employees, inside the log window
        leave_week = {}
        for p in self.people:
            if p["kind"] == "EMP" and rng.random() < 0.18:
                wk = int(rng.integers(0, 6))
                leave_week[p["pid"]] = wk
        for code, h in self.hubs.items():
            for d in self.days:
                wk = (d - P.LOG_START).days // 7
                for team in ("AM", "PM", "NT"):
                    groups = self.teams[code]
                    present = {}
                    for (tm, grp), pids in groups.items():
                        if tm != team:
                            continue
                        keep = []
                        for pid in pids:
                            person = self.people[pid]
                            if person["kind"] == "EMP":
                                if leave_week.get(pid) == wk:
                                    self.shifts.append(dict(pid=pid, hub=code, date=d, shift=team, status="LEAVE"))
                                    continue
                                if rng.random() < P.ABSENCE:
                                    self.shifts.append(dict(pid=pid, hub=code, date=d, shift=team, status="SICK"))
                                    continue
                                self.shifts.append(dict(pid=pid, hub=code, date=d, shift=team, status="WORKED"))
                                keep.append(pid)
                            else:
                                if rng.random() < P.AGENCY_SHOW:
                                    self.shifts.append(dict(pid=pid, hub=code, date=d, shift=team, status="WORKED"))
                                    keep.append(pid)
                        present[grp] = keep
                    self._staff_shift(code, h, d, team, present)

    def _t(self, d, team, minutes):
        start = dt.datetime(d.year, d.month, d.day, P.SHIFTS[team])
        return start + dt.timedelta(minutes=float(minutes))

    def _sess(self, code, st, pid, d, team, a, b, end_type="OPERATOR"):
        rng = self.rng
        ja = float(rng.uniform(0.2, 3.5))
        jb = float(rng.uniform(-2.5, 0.5))
        start = self._t(d, team, a + ja)
        end = self._t(d, team, b + jb)
        if end_type == "AUTO":
            end = self._t(d, team, b + 10.0)
        self.sessions.append(dict(hub=code, station_no=st, pid=pid, start=start, end=end, end_type=end_type))

    def _staff_shift(self, code, h, d, team, pres):
        rng = self.rng
        n = h["stations"]
        meal_a, meal_b = P.MEAL_AT * 60, (P.MEAL_AT + P.MEAL_LEN) * 60
        scheme = h["scheme"]
        ind = list(pres.get("induct", []))
        rng.shuffle(ind)
        rotation = list(pres.get("rotation", []))
        rng.shuffle(rotation)
        primaries = ind[:n]
        floor_loaders = [p for p in pres.get("floor", []) if self.people[p]["title"] == P.TITLES[code]["loader"]]
        rng.shuffle(floor_loaders)
        # cover is shared out: the loader who has covered least so far goes first
        floor_loaders.sort(key=lambda p: self.cover_count[p])
        if len(primaries) < n:      # a short induct team is covered from the rotation group, then off the floor
            need = n - len(primaries)
            if scheme in ("am_rotation", "sorter_relief") and rotation:
                take = rotation[:need]
                rotation = rotation[need:]
                primaries += take
                need -= len(take)
            for p in floor_loaders[:need]:
                self.cover_count[p] += 1
            primaries += floor_loaders[:need]
            floor_loaders = floor_loaders[need:]
        if scheme == "half_shift" and len(rotation) < n:   # a short rotation group is made up from the floor
            need = n - len(rotation)
            for p in floor_loaders[:need]:
                self.cover_count[p] += 1
            rotation += floor_loaders[:need]
            floor_loaders = floor_loaders[need:]
        # break slots: two 15-minute breaks per station, first in the first half, second in the second half
        b1 = [60 + 15 * (k % 10) + 5 * (k // 10) for k in range(n)]
        b2 = [270 + 15 * (k % 12) + 5 * (k // 12) for k in range(n)]
        relief = list(pres.get("relief", []))
        lead_relief = list(pres.get("lead_relief", []))
        buddies = list(pres.get("rotation", [])) if scheme == "break_buddies" else []
        rng.shuffle(buddies)
        ag_ind = list(pres.get("agency_induct", []))
        rng.shuffle(ag_ind)
        auto_end = rng.random() < 0.35
        for k in range(n):
            op = primaries[k]
            # the station's run of the shift for its primary, with its two breaks and the meal stop
            blocks = []
            if scheme == "half_shift":
                partner = rotation[k] if k < len(rotation) else None
                first_half = (d.toordinal() + k) % 2 == 0
                a_op, b_op = (op, partner) if first_half else (partner, op)
                if a_op is None:
                    a_op = op
                if b_op is None:
                    b_op = op
                blocks = [(a_op, 0, b1[k]), (a_op, b1[k] + 15, meal_a), (b_op, meal_b, b2[k]), (b_op, b2[k] + 15, 480)]
            elif scheme == "am_rotation" and team == "AM" and k < len(rotation):
                r = rotation[k]
                ra, rb = (120, 210) if k % 2 == 0 else (300, 390)
                if ra < b1[k] < rb or ra < b2[k] < rb:
                    ra, rb = (300, 390) if ra == 120 else (120, 210)
                segs = sorted([(0, b1[k]), (b1[k] + 15, meal_a), (meal_b, b2[k]), (b2[k] + 15, 480)])
                for a, b in segs:
                    if b <= ra or a >= rb:
                        blocks.append((op, a, b))
                    else:
                        if a < ra:
                            blocks.append((op, a, ra))
                        blocks.append((r, max(a, ra), min(b, rb)))
                        if b > rb:
                            blocks.append((op, rb, b))
            elif scheme == "sorter_relief" and rotation:
                r = rotation[(k // 3) % len(rotation)] if (k // 3) < len(rotation) else None
                ra = 60 + 60 * (k % 3) if k % 2 == 0 else 270 + 60 * (k % 3)
                rb = ra + 60
                segs = sorted([(0, b1[k]), (b1[k] + 15, meal_a), (meal_b, b2[k]), (b2[k] + 15, 480)])
                for a, b in segs:
                    if r is None or b <= ra or a >= rb:
                        blocks.append((op, a, b))
                    else:
                        if a < ra:
                            blocks.append((op, a, ra))
                        blocks.append((r, max(a, ra), min(b, rb)))
                        if b > rb:
                            blocks.append((op, rb, b))
            elif scheme == "agency_pm" and team == "PM" and k < len(ag_ind):
                ag = ag_ind[k]
                blocks = [(op, 0, b1[k]), (op, b1[k] + 15, meal_a), (ag, meal_b, b2[k]), (ag, b2[k] + 15, 480)]
            else:
                blocks = [(op, 0, b1[k]), (op, b1[k] + 15, meal_a), (op, meal_b, b2[k]), (op, b2[k] + 15, 480)]
            for who, a, b in blocks:
                if b - a < 4:
                    continue
                et = "OPERATOR"
                if (b == meal_a or b == 480) and auto_end and rng.random() < 0.5:
                    et = "AUTO"
                self._sess(code, k + 1, who, d, team, a, b, et)
            # break cover
            for (ba, bb) in ((b1[k], b1[k] + 15), (b2[k], b2[k] + 15)):
                if scheme == "break_buddies":
                    who = buddies[(2 * k + (0 if ba == b1[k] else 1)) % len(buddies)] if buddies else op
                elif scheme == "agency_pm" or (not relief):
                    who = lead_relief[k % len(lead_relief)] if lead_relief else None
                else:
                    who = relief[k % len(relief)]
                if who is None:
                    continue
                self._sess(code, k + 1, who, d, team, ba, bb, "OPERATOR")

    # ------------------------------------------------------------------ the clean truth
    def frames(self):
        people = pd.DataFrame(self.people)
        shifts = pd.DataFrame(self.shifts)
        sess = pd.DataFrame(self.sessions)
        return people, shifts, sess


def shift_start_date(row):
    return row


def exposures(people, shifts, sess, hubs, tail="keep", window=(P.REF_START, P.REF_END)):
    """Each worker's mean induct hours per worked shift in the window and their LAeq before and after."""
    s = sess.copy()
    if tail == "trim":
        m = s["end_type"] == "AUTO"
        s.loc[m, "end"] = s.loc[m, "end"] - pd.Timedelta(minutes=10)
    s["hours"] = (s["end"] - s["start"]).dt.total_seconds() / 3600.0
    # a session belongs to the shift that began on the date its shift started (night shifts begin the evening before)
    def sdate(ts):
        return (ts - pd.Timedelta(hours=5)).date() if True else None
    s["shift_date"] = [((t - dt.timedelta(hours=5)).date()) for t in s["start"]]
    inwin = s[(s["shift_date"] >= window[0]) & (s["shift_date"] <= window[1])]
    ih = inwin.groupby("pid")["hours"].sum()
    w = shifts[(shifts["status"] == "WORKED") & (shifts["date"] >= window[0]) & (shifts["date"] <= window[1])]
    ns = w.groupby("pid").size()
    out = people.set_index("pid").copy()
    out["shifts"] = ns
    out["induct_hours"] = ih
    out = out[out["shifts"].notna()].copy()
    out["induct_hours"] = out["induct_hours"].fillna(0.0)
    out["t_mean"] = out["induct_hours"] / out["shifts"]
    pre, post = [], []
    for pid, r in out.iterrows():
        h = hubs[r["hub"]]
        pre.append(lex(r["t_mean"], h["Li"], h["Lf"], h["La"]))
        post.append(lex(r["t_mean"], h["Lp"], h["Lf"], h["La"]))
    out["lex_pre"] = pre
    out["lex_post"] = post
    return out
