"""The State's own records of the world: the timekeeping systems' FY2026 roster extract, HR's employee extract (one row an
employee and title spell), the FY2028 position control, the entry class calendar and the timekeeping status codes. Each
writer returns (header, rows)."""
import csv
import datetime as dt

import numpy as np

import common as K

REC_SEED = 11
MIGRATION_DAY = 188                     # Thornmere moved to ShiftLink on Monday 5 January 2026
CODES_ROSTERPRO = {"W": "WRK", "V": "VCN", "VAC": "ANL", "SICK": "SCK", "IOD": "IOD", "TRN": "TRN",
                   "FMLA": "FML", "MIL": "MIL"}
CODES_SHIFTLINK = {"W": "P", "V": "OPEN", "VAC": "VA", "SICK": "SL", "IOD": "WC", "TRN": "TR",
                   "FMLA": "LOA-F", "MIL": "LOA-M"}
CATEGORY = {"W": "Worked", "V": "Vacant line", "VAC": "Annual leave", "SICK": "Sick leave",
            "IOD": "Injury on duty", "TRN": "Training", "FMLA": "Family and medical leave", "MIL": "Military leave"}
DESC_ROSTERPRO = {"W": "Worked as scheduled", "V": "Line vacant", "VAC": "Annual leave", "SICK": "Sick leave",
                  "IOD": "Injured on duty (workers' compensation)", "TRN": "Training off post",
                  "FMLA": "FMLA leave", "MIL": "Military leave"}
DESC_SHIFTLINK = {"W": "Present", "V": "Open line", "VAC": "Vacation", "SICK": "Sick",
                  "IOD": "Workers comp", "TRN": "Training", "FMLA": "Leave of absence - FMLA",
                  "MIL": "Leave of absence - military"}
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
CLASS_ROW = {(t, c): (s, g, f) for t, c, s, g, f in K.CLASSES}
# the academies' usual start for a first-half and a second-half class: (month, weekday 0 Monday, which one)
ACADEMY_START = {"CO": ((3, 0, 2), (7, 0, 3)), "PCO": ((4, 0, 1), (10, 0, 3)), "FSA": ((4, 0, 3), (11, 0, 3)),
                 "HMW": ((5, 0, 3), (8, 0, 4))}


def iso(d):
    return d.isoformat() if d else ""


def nth_weekday(year, month, weekday, n):
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def write_csv(path, head, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        w.writerows(rows)


class Records:
    def __init__(self, w, seed=REC_SEED):
        self.w = w
        self.rng = np.random.default_rng(seed)
        self._classes()
        self._rehires()
        self._ids()
        self._movers()
        self.reinstated = None

    # ---------------------------------------------------------------------------------------------- people
    def _classes(self):
        """each person's entry class: the July 2025 classes, the FY2026 mid-year classes the world filled lines from"""
        w = self.w
        self.cls = []
        for p in w.people:
            if p["cls"] == "2025-1":
                self.cls.append("2025-1")
            elif p["cls"] is not None and p["service"] == 0:
                self.cls.append(K.FY26_FILL_CLASS[(p["title"], p["start"])])
            else:
                self.cls.append(None)

    def _rehires(self):
        """one FY2026 resignation in each title with separations came back: the line the officer left was filled on a
        class's posting day by the same officer, rehired under a new employee number with the seniority date restored"""
        w = self.w
        rng = np.random.default_rng(REC_SEED + 7)
        self.rehire_of = {}                      # new person index -> separated person index
        for t in K.TITLE_ORDER:
            pairs = []
            for j, ln in enumerate(w.lines):
                if K.UNIT_TITLE[ln["unit"]] != t:
                    continue
                hs = []
                for i in range(K.FY26_DAYS):
                    e = w.holder[j, i]
                    if e >= 0 and (not hs or hs[-1] != e):
                        hs.append(e)
                if len(hs) == 2:
                    old, new = hs
                    po = w.people[old]
                    if po["service"] < 20 and 40 <= po["end"] <= 140 and self.cls[new] is not None:
                        pairs.append((old, new))
            if pairs:
                old, new = pairs[int(rng.integers(0, len(pairs)))]
                self.rehire_of[new] = old
                self.cls[new] = None

    def _ids(self):
        """employee numbers, hire dates (an entry class's academy start), seniority dates and class labels"""
        rng = self.rng
        w = self.w
        nums = rng.choice(np.arange(102000, 189999), size=len(w.people), replace=False)
        self.emp_id = ["E%06d" % n for n in nums]
        self.hire = []
        self.cls_label = []
        for e, p in enumerate(w.people):
            t = p["title"]
            c = self.cls[e]
            if e in self.rehire_of:
                self.hire.append(K.fy26_day(p["start"]))
                self.cls_label.append("")
            elif c is not None:
                self.hire.append(dt.date.fromisoformat(CLASS_ROW[(t, c)][0]))
                self.cls_label.append("%s %s" % (t, c))
            else:
                yr = 2025 - p["service"] - (1 if rng.uniform() < 0.5 else 0)
                half = 1 if rng.uniform() < 0.5 else 2
                m, wd, n = ACADEMY_START[t][half - 1]
                self.hire.append(nth_weekday(yr, m, wd, n))
                self.cls_label.append("%s %d-%d" % (t, yr, half) if yr >= 2009 else "")
        self.seniority = list(self.hire)
        for new, old in self.rehire_of.items():
            self.seniority[new] = self.seniority[old]

    def _movers(self):
        """officers who left the eight units for another title after FY2026 (HR keeps a row for each title held)"""
        w = self.w
        rng = np.random.default_rng(REC_SEED + 13)
        taken = set(self.rehire_of) | set(self.rehire_of.values())
        self.movers = {}                         # person index -> (new title, new unit, date)
        self.earlier = {}                        # person index -> (earlier title, earlier unit, date the FY2026 title began)
        for unit, title, new_unit, date, before in K.MOVERS:
            lo = 8 if before else 3
            cand = [e for e, p in enumerate(w.people) if p["unit"] == unit and self.cls[e] is None and
                    p["end"] >= K.FY26_DAYS and p["start"] == 0 and e not in taken and lo <= p["service"] <= 18]
            e = int(cand[int(rng.integers(0, len(cand)))])
            self.movers[e] = (title, new_unit, dt.date.fromisoformat(date))
            taken.add(e)
            if before:
                t0, u0 = before
                h = self.hire[e]
                m, wd, n = ACADEMY_START[t0][0 if h.month <= 6 else 1]
                h = nth_weekday(h.year, m, wd, n)
                self.hire[e] = self.seniority[e] = h
                self.cls_label[e] = "%s %d-%d" % (t0, h.year, 1 if h.month <= 6 else 2) if h.year >= 2009 else ""
                moved = h + dt.timedelta(days=int(0.45 * (dt.date(2025, 7, 1) - h).days))
                moved += dt.timedelta(days=(7 - moved.weekday()) % 7)
                self.earlier[e] = (t0, u0, moved)

    def holder_on(self, j, i):
        e = self.w.holder[j, i]
        return self.id_on(e, K.fy26_day(i)) if e >= 0 else ""

    def reinstate(self, e, left, back):
        """an officer who resigned on `left` and was reinstated to the same line on `back`, under a new employee number
        with the seniority date restored"""
        rng = np.random.default_rng(REC_SEED + 11)
        taken = set(self.emp_id)
        new = "E%06d" % int(rng.integers(102000, 189999))
        while new in taken:
            new = "E%06d" % int(rng.integers(102000, 189999))
        self.reinstated = (e, left, back, new)

    def id_on(self, e, d):
        """the employee number a person was rostered and paid under on date d"""
        r = self.reinstated
        if r is not None and e == r[0] and d >= r[2]:
            return r[3]
        return self.emp_id[e]

    # ---------------------------------------------------------------------------------------------- rosters
    def roster_rows(self):
        w = self.w
        rng = self.rng
        rows = []
        for j, ln in enumerate(w.lines):
            for i in range(K.FY26_DAYS):
                if not w.on[j, i]:
                    continue
                st = w.status[j, i]
                e = w.holder[j, i]
                sl = ln["unit"] == "TWC" and i >= MIGRATION_DAY
                code = (CODES_SHIFTLINK if sl else CODES_ROSTERPRO)[st]
                d = K.fy26_day(i)
                exported = d + dt.timedelta(days=int(rng.integers(1, 4)))
                rows.append([iso(d), ln["unit"], ln["id"], ln["shift"], K.SHIFT_START[ln["shift"]], "8.0",
                             self.id_on(e, d) if e >= 0 else "", code, "ShiftLink" if sl else "RosterPro",
                             exported.isoformat() + "T02:%02d:00" % int(rng.integers(0, 60))])
        # the RosterPro nightly export re-ran for three days in February after an interface outage, and the
        # re-run's rows were appended rather than replacing the first run's
        rerun = [K.fy26_day(i).isoformat() for i in (222, 223, 224)]
        extra = [r[:9] + [(dt.date.fromisoformat(r[0]) + dt.timedelta(days=6)).isoformat() + "T03:15:00"]
                 for r in rows if r[0] in rerun and r[8] == "RosterPro"]
        rows += extra
        rows.sort(key=lambda r: (r[0], r[1], r[2], r[9]))
        return (["shift_date", "unit_code", "line_id", "shift", "shift_start", "scheduled_hours", "employee_id",
                 "status_code", "source_system", "exported_at"], rows)

    # ---------------------------------------------------------------------------------------------- employees
    def employee_rows(self):
        w = self.w
        rows = []
        for e, p in enumerate(w.people):
            sep = K.fy26_day(p["end"]) if p["end"] < K.FY26_DAYS else None
            reason = "" if sep is None else ("Retirement" if p["service"] >= 20 else "Resignation")
            base = [self.emp_id[e]]
            tail = [iso(self.hire[e]), iso(self.seniority[e]), self.cls_label[e]]
            if e in self.movers:
                t2, u2, d2 = self.movers[e]
                start = self.hire[e]
                if e in self.earlier:
                    t0, u0, d0 = self.earlier[e]
                    rows.append(base + [t0, K.TITLES[t0], iso(start), iso(d0 - dt.timedelta(days=1)), u0] + tail +
                                ["", ""])
                    start = d0
                rows.append(base + [p["title"], K.TITLES[p["title"]], iso(start),
                                    iso(d2 - dt.timedelta(days=1)), p["unit"]] + tail + ["", ""])
                rows.append(base + [t2, K.TITLES[t2], iso(d2), "", u2] + tail + ["", ""])
            elif self.reinstated is not None and e == self.reinstated[0]:
                _, left, back, new = self.reinstated
                rows.append(base + [p["title"], K.TITLES[p["title"]], iso(self.hire[e]), iso(left), p["unit"]] + tail +
                            [iso(left), "Resignation"])
                rows.append([new, p["title"], K.TITLES[p["title"]], iso(back), "", p["unit"], iso(back),
                             iso(self.seniority[e]), "", "", ""])
            else:
                rows.append(base + [p["title"], K.TITLES[p["title"]], iso(self.hire[e]), iso(sep), p["unit"]] +
                            tail + [iso(sep), reason])
        rows.sort(key=lambda r: (r[0], r[3]))
        return (["employee_id", "title_code", "title", "title_effective_from", "title_effective_to", "home_unit",
                 "hire_date", "seniority_date", "academy_class", "separation_date", "separation_reason"], rows)

    def title_on(self, e, d):
        """the title an employee held on date d"""
        if e in self.movers and d >= self.movers[e][2]:
            return self.movers[e][0]
        if e in self.earlier and d < self.earlier[e][2]:
            return self.earlier[e][0]
        return self.w.people[e]["title"]

    # ---------------------------------------------------------------------------------------------- FY2028
    def new_line_ids(self):
        """the position control's numbers for the FY2028 lines (the next line number on each shift) and each line's
        first shift on post: its first scheduled day on or after its class's posting day"""
        out = []
        count = {}
        for x in self.w.new_lines:
            u = x["unit"]
            k = sum(1 for y in out if y["unit"] == u)
            s = K.SHIFTS[k % 3]
            n = count.get((u, s), 7) + 1
            count[(u, s)] = n
            t = K.UNIT_TITLE[u]
            cls = K.FY28_FILL_CLASS[(t, x["fill_week"])]
            post = dt.date.fromisoformat(CLASS_ROW[(t, cls)][2])
            off = {x["offset"], (x["offset"] + 1) % 7}
            first = post
            while first.weekday() in off:
                first += dt.timedelta(days=1)
            out.append(dict(x, shift=s, line_id="%s-%s%02d" % (u, s, n), cls=cls, first=first, off=off))
        return out

    def position_control_rows(self):
        w = self.w
        rng = np.random.default_rng(REC_SEED + 3)
        rows = []
        auth = {}
        for u in K.UNIT_CODES:
            auth[u] = dt.date(int(rng.integers(1994, 2012)), 7, 1)
        refill = {"CO": "2026-3", "PCO": "2027-0", "FSA": "2027-0", "HMW": "2026-3"}
        for j, ln in enumerate(w.lines):
            off = "%s/%s" % (DAYS[(ln["offset"]) % 7], DAYS[(ln["offset"] + 1) % 7])
            a = auth[ln["unit"]] if rng.uniform() < 0.8 else dt.date(int(rng.integers(2012, 2024)), 7, 1)
            e = w.holder[j, K.FY26_DAYS - 1]
            t = K.UNIT_TITLE[ln["unit"]]
            if e in self.movers:
                c = refill[t]
                rows.append([ln["id"], ln["unit"], t, ln["shift"], off, a.isoformat(), "Filled", "", "%s %s" % (t, c),
                             CLASS_ROW[(t, c)][2]])
            else:
                rows.append([ln["id"], ln["unit"], t, ln["shift"], off, a.isoformat(), "Filled",
                             self.holder_on(j, K.FY26_DAYS - 1), "", ""])
        for x in self.new_line_ids():
            u = x["unit"]
            t = K.UNIT_TITLE[u]
            off = "%s/%s" % (DAYS[x["offset"]], DAYS[(x["offset"] + 1) % 7])
            rows.append([x["line_id"], u, t, x["shift"], off, "2027-07-01", "Vacant", "", "%s %s" % (t, x["cls"]),
                         x["first"].isoformat()])
        rows.sort(key=lambda r: (K.UNIT_CODES.index(r[1]), "DEN".index(r[3]), r[0]))
        return (["line_id", "unit_code", "title_code", "shift", "days_off", "authorized_from", "status_fy2028_start",
                 "incumbent_employee_id", "filled_by_class", "first_shift_on_post"], rows)

    def class_rows(self):
        rows = []
        for t, c, s, g, f in K.CLASSES:
            rows.append([K.AGENCY[t], t, "%s %s" % (t, c), s, g, f])
        return (["agency", "title_code", "class_id", "academy_start", "graduation_date", "first_shift_on_post"], rows)

    def code_rows(self):
        rows = []
        for k in ("W", "V", "VAC", "SICK", "IOD", "TRN", "FMLA", "MIL"):
            rows.append(["RosterPro", CODES_ROSTERPRO[k], DESC_ROSTERPRO[k], CATEGORY[k]])
        for k in ("W", "V", "VAC", "SICK", "IOD", "TRN", "FMLA", "MIL"):
            rows.append(["ShiftLink", CODES_SHIFTLINK[k], DESC_SHIFTLINK[k], CATEGORY[k]])
        return (["source_system", "status_code", "description", "state_category"], rows)
