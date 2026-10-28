"""The simulated Tamberlin County world: seventh graders, their enrollment spells and Pellmore accounts, every homework
skill-builder problem they started in 2024-25, 2025-26 and the 2026-27 fall to the as-of date, and the 2025-26 Math Lab
sessions. Seeded and deterministic; nothing here reads a shipped file."""
import datetime as dt
import math

import numpy as np

import params as P


def d(s):
    return dt.date.fromisoformat(s)


def expit(z):
    return 1.0 / (1.0 + math.exp(-z))


SB = {b[0]: b for b in P.SKILL_BUILDERS}


def _pools():
    """each skill builder's pool of problem numbers: its own size and gaps where problems were retired"""
    rng = np.random.default_rng([P.SEED, 6])
    out = {}
    for code, unit, title, a, g in P.SKILL_BUILDERS:
        size = int(rng.integers(148, 331))
        out[code] = sorted(int(x) for x in rng.choice(np.arange(1, int(size * 1.6)), size=size, replace=False))
    return out


POOL = _pools()
SB_INDEX = {b[0]: i for i, b in enumerate(P.SKILL_BUILDERS)}
SCH = [s[0] for s in P.SCHOOLS]


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self.students = []       # dicts
        self.spells = []         # (student_id, year, school, grade, entry, exit or None, exit_code)
        self.accounts = []       # dicts: user_id, student_id, opened, closed, kind
        self.events = []         # problem and scaffold rows
        self.lab = []            # Math Lab attendee rows
        self.staff = []          # staff test accounts
        self._sid = 4_407_311
        self._uid = 600_100
        self.build()

    # identities -----------------------------------------------------------------------------------------------
    def new_student(self, year, theta_shift, school):
        self._sid += int(self.rng.integers(3, 41))
        sch = P.SCHOOLS[SCH.index(school)]
        th = self.rng.normal(sch[3] + theta_shift, P.THETA_SD)
        eng = float(np.clip(self.rng.beta(4.0, 3.2) + 0.05 * th, 0.12, 0.97))
        s = {"id": "%07d" % self._sid, "year": year, "theta": float(th), "eng": eng,
             "quit": float(np.clip(self.rng.normal(1.0, 0.25), 0.4, 1.8)),
             "evening": float(self.rng.uniform(0.55, 0.95)), "no_hw": bool(self.rng.random() < P.P_NO_HOMEWORK)}
        self.students.append(s)
        return s

    def new_account(self, student_id, opened):
        self._uid += int(self.rng.integers(7, 300))
        a = {"user_id": "pm%06d" % self._uid, "student_id": student_id, "opened": opened, "closed": None}
        self.accounts.append(a)
        return a

    # enrollment ------------------------------------------------------------------------------------------------
    def enroll_year(self, year, until=None):
        self.rng = np.random.default_rng([P.SEED, 1, P.YEARS.index(year)])
        start, end = d(P.YEAR_START[year]), d(P.YEAR_END[year])
        last = until or end
        span = (last - start).days
        frac = span / float((end - start).days)
        out = []
        for code, name, n, off, win in P.SCHOOLS:
            for _ in range(n):
                s = self.new_student(year, P.COHORT_SHIFT[year], code)
                out.append([s, [(code, start, None, None)], [self.new_account(s["id"], start)]])
        # arrivals from outside the district
        n_arr = int(round(P.P_ARRIVE * sum(s[2] for s in P.SCHOOLS) * frac))
        for _ in range(n_arr):
            code = SCH[int(self.rng.integers(0, len(SCH)))]
            day = start + dt.timedelta(days=int(self.rng.integers(7, span)))
            s = self.new_student(year, P.COHORT_SHIFT[year] - 0.15, code)
            out.append([s, [(code, day, None, None)], [self.new_account(s["id"], day)]])
        movers = self.rng.permutation(len(out))
        n_tr = int(round(P.P_TRANSFER * len(out) * frac))
        n_lv = int(round(P.P_LEAVE * len(out) * frac))
        for k, idx in enumerate(movers[:n_tr + n_lv]):
            rec = out[idx]
            s, spells, accts = rec
            code0, entry0, _, _ = spells[0]
            lo = max((entry0 - start).days + 10, 10)
            if lo >= span - 3:
                continue
            day = start + dt.timedelta(days=int(self.rng.integers(lo, span - 2)))
            if k < n_tr:
                code1 = code0
                while code1 == code0:
                    code1 = SCH[int(self.rng.integers(0, len(SCH)))]
                gap = int(self.rng.choice([1, 1, 1, 3, 4, 6]))
                spells[0] = (code0, entry0, day, "T1")
                spells.append((code1, day + dt.timedelta(days=gap), None, None))
            else:
                spells[0] = (code0, entry0, day, "W2")
                accts[0]["closed"] = day
                if self.rng.random() < P.P_RETURN:
                    back = day + dt.timedelta(days=int(self.rng.integers(20, 75)))
                    if back < last - dt.timedelta(days=5):
                        code1 = code0 if self.rng.random() < 0.6 else SCH[int(self.rng.integers(0, len(SCH)))]
                        spells.append((code1, back, None, None))
                        accts.append(self.new_account(s["id"], back))
        for s, spells, accts in out:
            for code, a, b, why in spells:
                self.spells.append((s["id"], year, code, 7, a, b, why))
            s["spells"] = spells
            s["accounts"] = accts
        return out

    @staticmethod
    def school_on(spells, day):
        for code, a, b, why in spells:
            if a <= day and (b is None or day <= b):
                return code
        return None

    @staticmethod
    def account_on(accts, day):
        for a in accts:
            if a["opened"] <= day and (a["closed"] is None or day <= a["closed"]):
                return a
        return None

    # practice ----------------------------------------------------------------------------------------------------
    def sitting_start(self, s, day):
        if self.rng.random() < s["evening"]:
            mins = int(self.rng.integers(15 * 60 + 30, 21 * 60 + 50))
        else:
            mins = int(self.rng.integers(8 * 60 + 40, 14 * 60 + 40))
        return dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=mins, seconds=int(self.rng.integers(0, 60)))

    def practise(self, year, rec, unit, open_s, close_s, stop=None):
        s, spells, accts = rec
        self.rng = np.random.default_rng([P.SEED, 2, int(s["id"]), P.YEARS.index(year), SB_INDEX[unit]])
        if s["no_hw"]:
            return None
        code_, unit_no, title, a, g = SB[unit]
        open_d, close_d = d(open_s), d(close_s)
        e_prev, n, run, done = 0, 0, 0, False
        day = open_d
        last_day = min(close_d, stop) if stop else close_d
        while day <= last_day and not done:
            school = self.school_on(spells, day)
            if school is None and len(spells) > 1:
                past = [sp for sp in spells if sp[2] is not None and sp[2] < day and sp[3] == "T1"]
                ahead = [sp for sp in spells if sp[1] > day]
                if past and ahead:                  # between two district schools: homework goes on at home
                    school = past[-1][0]
            acct = self.account_on(accts, day)
            weekend = day.weekday() >= 5
            p_sit = s["eng"] * (0.45 if weekend else 1.0)
            if school is not None and acct is not None and self.rng.random() < p_sit:
                t = self.sitting_start(s, day)
                e_cur = 0
                while e_cur < P.CAP and not done:
                    z = s["theta"] + a + g * (e_cur + P.RHO * e_prev)
                    right = self.rng.random() < expit(z)
                    hint = (not right) and self.rng.random() < 0.22
                    secs = int(self.rng.integers(35, 200)) if right else int(self.rng.integers(60, 260))
                    attempts = 1 if right else int(self.rng.choice([1, 2, 2, 3])) + (0 if hint else 1)
                    self.events.append({"user_id": acct["user_id"], "student_id": s["id"], "year": year, "unit": unit,
                                        "school": school, "problem": n, "original": True, "hint": hint,
                                        "correct": bool(right), "attempts": attempts, "start": t,
                                        "end": t + dt.timedelta(seconds=secs),
                                        "pid": POOL[unit][(int(self.rng.integers(1, 360)) - 1) % len(POOL[unit])]})
                    t = t + dt.timedelta(seconds=secs + int(self.rng.integers(3, 25)))
                    if not right and not hint and self.rng.random() < 0.55:
                        for k in range(int(self.rng.choice([1, 1, 1, 2]))):
                            ss = int(self.rng.integers(20, 95))
                            self.events.append({"user_id": acct["user_id"], "student_id": s["id"], "year": year,
                                                "unit": unit, "school": school, "problem": n, "original": False,
                                                "hint": False, "correct": bool(self.rng.random() < 0.7),
                                                "attempts": int(self.rng.choice([1, 1, 2])), "start": t,
                                                "end": t + dt.timedelta(seconds=ss), "pid": -(k + 1)})
                            t = t + dt.timedelta(seconds=ss + int(self.rng.integers(2, 12)))
                    n += 1
                    e_cur += 1
                    run = run + 1 if right else 0
                    if run >= P.STREAK:
                        done = True
                    elif self.rng.random() < (0.07 if right else 0.15) * s["quit"]:
                        break
                e_prev += e_cur
            day += dt.timedelta(days=1)
        return done

    # the Math Lab (2025-26) ----------------------------------------------------------------------------------------
    def math_lab(self, year, cohort, results):
        """Attendee rows of the spring Math Lab: the ten school days after each spring skill builder closed, one WIN
        period a day, the unfinished seventh graders mixed with sixth and eighth graders. A session led by two
        interventionists is logged by each of them; an edited session is saved again and every save is kept."""
        rng = self.rng = np.random.default_rng([P.SEED, 3])
        cal = P.WINDOWS[year]
        rows = []
        staff_no = 3100
        lead = {}
        for code, name, n, off, win in P.SCHOOLS:
            staff_no += int(rng.integers(3, 30))
            second = staff_no + int(rng.integers(2, 9))
            lead[code] = ("INT-%04d" % staff_no, "INT-%04d" % second)
        others_pool = {}
        for code, name, n, off, win in P.SCHOOLS:
            others_pool[code] = ["%07d" % int(rng.integers(3_900_000, 4_399_999)) for _ in range(160)]
        for code, name, n, off, win in P.SCHOOLS:
            for unit in P.SPRING:
                close = d(cal[unit][1])
                days, day = [], close + dt.timedelta(days=1)
                while len(days) < 10:
                    if day.weekday() < 5:
                        days.append(day)
                    day += dt.timedelta(days=1)
                unfinished = [rec for rec in cohort if results.get((rec[0]["id"], unit, year)) is False]
                for day in days:
                    seven = [rec[0]["id"] for rec in unfinished
                             if self.school_on(rec[1], day) == code and rng.random() < 0.42]
                    n_oth = int(rng.integers(0, 6))
                    if not seven and n_oth == 0:
                        continue
                    oth = []
                    for _ in range(n_oth):
                        g = int(rng.choice([6, 8]))
                        oth.append((others_pool[code][int(rng.integers(0, 160))], g, "%d-%d" % (g, int(rng.integers(3, 8)))))
                    minutes = win if rng.random() > 0.06 else int(rng.choice([20, 25]))
                    att = [(sid, 7, "7-%s" % unit) for sid in seven] + oth
                    leads = [lead[code][0]]
                    if len(att) >= 9 and rng.random() < 0.55:
                        leads.append(lead[code][1])
                    saved = dt.datetime(day.year, day.month, day.day, 15, 5) + dt.timedelta(minutes=int(rng.integers(0, 140)))
                    saves = [(saved, minutes, att)]
                    r = rng.random()
                    if r < 0.05:                     # edited the same week: shorter session, the list unchanged
                        new_min = int(rng.choice([15, 20, 25]))
                        saves.append((saved + dt.timedelta(days=int(rng.integers(1, 4)), minutes=int(rng.integers(5, 300))),
                                      new_min, att))
                    elif r < 0.09:                   # edited to add a student who was missed
                        extra = (others_pool[code][int(rng.integers(0, 160))], 8, "8-%d" % int(rng.integers(3, 8)))
                        saves.append((saved + dt.timedelta(hours=int(rng.integers(2, 30))), minutes, att + [extra]))
                    for who in leads:
                        for sv, mins, lst in saves:
                            for sid, g, ul in lst:
                                rows.append({"school": code, "date": day, "period": "WIN", "staff": who, "unit": ul,
                                             "student_id": sid, "grade": g, "minutes": mins, "saved_at": sv})
        return rows

    # staff test accounts --------------------------------------------------------------------------------------------
    def staff_accounts(self):
        rng = self.rng = np.random.default_rng([P.SEED, 4])
        for code, name, n, off, win in P.SCHOOLS:
            for k in range(int(rng.integers(1, 3))):
                a = self.new_account(None, d("2025-08-18"))
                a["school"] = code
                self.staff.append(a)
                for year in P.YEARS:
                    for unit, (o, c) in P.WINDOWS[year].items():
                        if rng.random() < 0.35:
                            day = d(o) + dt.timedelta(days=int(rng.integers(0, 3)))
                            t = dt.datetime(day.year, day.month, day.day, 7, 20) + dt.timedelta(minutes=int(rng.integers(0, 50)))
                            run = 0
                            for j in range(int(rng.integers(3, 9))):
                                if run >= P.STREAK:
                                    break
                                right = rng.random() < 0.8
                                run = run + 1 if right else 0
                                self.events.append({"user_id": a["user_id"], "student_id": None, "year": year,
                                                    "unit": unit, "school": code, "problem": j, "original": True,
                                                    "hint": False, "correct": bool(right), "attempts": 1 if right else 2,
                                                    "start": t, "end": t + dt.timedelta(seconds=40),
                                                    "pid": POOL[unit][(int(rng.integers(1, 360)) - 1) % len(POOL[unit])]})
                                t = t + dt.timedelta(seconds=int(rng.integers(45, 90)))

    # the school an account carries in an export taken on a given day --------------------------------------------------
    def export_school(self, user_id, day):
        rec = self.by_user[user_id]
        if rec is None:
            return self.staff_school[user_id]
        s, spells, accts = rec
        a = [x for x in accts if x["user_id"] == user_id][0]
        if s["year"] == "2025-26" and day > d(P.YEAR_END["2025-26"]) and a["closed"] is None:
            return self.summer.get(s["id"], spells[-1][0])
        when = day if a["closed"] is None or day <= a["closed"] else a["closed"]
        code = self.school_on(spells, when)
        if code is None:      # between spells on the export day: the last school the account was synced to
            past = [sp for sp in spells if sp[1] <= when]
            code = past[-1][0] if past else spells[0][0]
        return code

    # the build -------------------------------------------------------------------------------------------------------
    def build(self):
        self.cohorts = {}
        self.results = {}
        for year in P.YEARS:
            until = P.AS_OF if year == "2026-27" else None
            cohort = self.enroll_year(year, until)
            self.cohorts[year] = cohort
            for unit, (o, c) in sorted(P.WINDOWS[year].items(), key=lambda kv: kv[1][0]):
                stop = P.AS_OF if year == "2026-27" else None
                for rec in cohort:
                    res = self.practise(year, rec, unit, o, c, stop)
                    if res is not None:
                        self.results[(rec[0]["id"], unit, year)] = res
        self.staff_accounts()
        rng = np.random.default_rng([P.SEED, 5])
        self.summer = {}
        for s, spells, accts in self.cohorts["2025-26"]:
            if spells[-1][2] is None:
                r = rng.random()
                if r < 0.065:
                    code = spells[-1][0]
                    while code == spells[-1][0]:
                        code = SCH[int(rng.integers(0, len(SCH)))]
                    self.summer[s["id"]] = code
        self.lab = self.math_lab("2025-26", self.cohorts["2025-26"], self.results)
        self.by_user = {}
        for year, cohort in self.cohorts.items():
            for rec in cohort:
                for a in rec[2]:
                    self.by_user[a["user_id"]] = rec
        self.staff_school = {a["user_id"]: a["school"] for a in self.staff}
        for a in self.staff:
            self.by_user[a["user_id"]] = None


if __name__ == "__main__":
    import time
    t0 = time.time()
    w = World()
    print("students", len(w.students), "spells", len(w.spells), "accounts", len(w.accounts), "events", len(w.events),
          "originals", sum(1 for e in w.events if e["original"]), "lab rows", len(w.lab), "staff", len(w.staff), "%.1fs" % (time.time() - t0))
    for y in P.YEARS:
        rs = [v for (sid, u, yy), v in w.results.items() if yy == y]
        print(y, "skill builders started", len(rs), "completed share %.3f" % (sum(rs) / max(1, len(rs))))
