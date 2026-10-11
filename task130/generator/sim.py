"""The plan's population and its health care, member by member and month by month, January 2024 to March 2028.

Costs come from events: routine professional care, labs, imaging, emergency visits and admissions; chronic
conditions that cost something every month; and episodes that end (a cancer course, a transplant, a premature
birth, trauma, a joint replacement, a heart attack, a hepatitis C cure, a pregnancy). Each event becomes one or
more claims, each with its own paid lag, so what the plan knows about a month at any cut-off is the claims paid by
then. 2024 and the 2027-28 programme year are simulated and never shipped."""
import datetime as dt
import math

import numpy as np

import world as W

DAY = dt.timedelta(days=1)

CHRONIC = ("diabetes", "htn", "lipid", "asthma", "depression", "thyroid", "esrd", "hiv", "autoimmune",
           "hemophilia", "cf", "afib", "cad", "liver", "hepc", "kidney_tx", "liver_tx", "cancer_hx", "chf", "copd")


class Person:
    __slots__ = ("pid", "fid", "rel", "sex", "dob", "code", "legacy", "legacy2", "member_id", "start", "end",
                 "death", "frailty", "conds", "regs", "eps", "nchronic", "dis_until")

    def __init__(self, pid, fid, rel, sex, dob):
        self.pid, self.fid, self.rel, self.sex, self.dob = pid, fid, rel, sex, dob
        self.code = None
        self.legacy = None
        self.legacy2 = None
        self.member_id = None
        self.start = None
        self.end = None
        self.death = None
        self.frailty = 1.0
        self.conds = {}      # condition -> onset date
        self.regs = {}       # regimen key -> [drug, days supply, last fill date allowed or None, next fill date]
        self.eps = []        # active episodes
        self.nchronic = 0
        self.dis_until = None  # an employee off work after a serious illness, at higher risk of leaving

    def covered_on(self, d):
        return self.start is not None and self.start <= d and (self.end is None or d <= self.end)

    def age(self, d):
        a = d.year - self.dob.year
        if (d.month, d.day) < (self.dob.month, self.dob.day):
            a -= 1
        return a


class Family:
    __slots__ = ("fid", "emp", "cls", "members", "hist", "root", "active", "cls_hist")

    def __init__(self, fid, emp, cls):
        self.fid, self.emp, self.cls = fid, emp, cls
        self.members = []
        self.hist = []        # (effective date, plan, coverage tier)
        self.root = None      # Bramwell subscriber number
        self.active = True
        self.cls_hist = []    # (effective date, employee class)


class Sim:
    def __init__(self, seed=W.SEED):
        self.rp = np.random.default_rng(seed)          # population and life events
        self.rh = np.random.default_rng(seed + 11)     # health events
        self.rc = np.random.default_rng(seed + 23)     # claim lags
        self.people = []
        self.fams = []
        self.events = []
        self.emp_used, self.root_used, self.mid_used = set(), set(), set()
        self.cond_years = {}

    # ---------------------------------------------------------------- identifiers
    def new_emp(self):
        while True:
            e = "%06d" % self.rp.integers(100200, 248900)
            if e not in self.emp_used:
                self.emp_used.add(e)
                return e

    def new_root(self):
        while True:
            r = "%08d" % self.rp.integers(60100000, 64990000)
            if r not in self.root_used:
                self.root_used.add(r)
                return r

    def new_member_id(self):
        while True:
            m = "RCV%07d" % self.rp.integers(1000000, 9999999)
            if m not in self.mid_used:
                self.mid_used.add(m)
                return m

    # ---------------------------------------------------------------- population
    def add_person(self, fam, rel, sex, dob, start):
        p = Person(len(self.people), fam.fid, rel, sex, dob)
        p.start = start
        p.frailty = float(self.rp.gamma(1.6, 1 / 1.6))
        self.people.append(p)
        fam.members.append(p.pid)
        self.seed_conditions(p, start)
        return p

    def new_family(self, start, cls=None, hired=True):
        r = self.rp
        if cls is None:
            cls = str(r.choice(["T", "S", "A"], p=[0.56, 0.40, 0.04]))
        fam = Family(len(self.fams), self.new_emp(), cls)
        self.fams.append(fam)
        if cls == "R":
            age = int(r.integers(55, 65))
        elif hired:
            age = int(min(62, 22 + r.gamma(2.0, 6.0)))
        else:
            age = int(min(66, max(22, r.normal(44, 10.5))))
        female = r.random() < (0.76 if cls == "T" else 0.66 if cls == "S" else 0.55)
        dob = start - dt.timedelta(days=int(age * 365.25 + r.integers(0, 365)))
        self.add_person(fam, "R" if cls == "R" else "E", "F" if female else "M", dob, start)
        pr_sp = 0.62 if 30 <= age <= 60 else 0.35 if age < 30 else 0.55
        has_sp = r.random() < pr_sp
        nkids = 0 if (cls == "R" or not 26 <= age <= 56) else int(r.choice([0, 1, 2, 3, 4], p=[0.34, 0.24, 0.27, 0.11, 0.04]))
        if has_sp:
            sa = int(min(70, max(21, age + r.normal(0, 3.5))))
            sdob = start - dt.timedelta(days=int(sa * 365.25 + r.integers(0, 365)))
            self.add_person(fam, "S", "M" if female else "F", sdob, start)
        if nkids:
            oldest = min(25, max(0, age - int(r.integers(24, 34))))
            for k in range(nkids):
                ka = max(0, oldest - k * int(r.integers(1, 5)))
                kdob = start - dt.timedelta(days=int(ka * 365.25 + r.integers(0, 365)))
                if kdob >= start:
                    kdob = start - dt.timedelta(days=int(r.integers(30, 300)))
                self.add_person(fam, "C", "F" if r.random() < 0.49 else "M", kdob, start)
        tier = "FAM" if has_sp and nkids else "ES" if has_sp else "EC" if nkids else "EE"
        fam.cls_hist.append((start, cls))
        plan = "HDHP" if r.random() < (0.52 if age < 35 else 0.36 if age < 50 else 0.24) else "PPO"
        fam.hist.append((start, plan, tier))
        return fam

    def seed_conditions(self, p, d):
        """conditions a member already has when coverage begins"""
        r = self.rp
        a = p.age(d)
        pr = {
            "diabetes": 0.0 if a < 20 else 0.03 if a < 40 else 0.075 if a < 50 else 0.12,
            "htn": 0.01 if a < 30 else 0.08 if a < 40 else 0.18 if a < 50 else 0.31,
            "lipid": 0.0 if a < 30 else 0.07 if a < 40 else 0.17 if a < 50 else 0.29,
            "asthma": 0.08 if a < 18 else 0.07,
            "depression": 0.02 if a < 12 else 0.09 if a < 18 else 0.115,
            "thyroid": 0.0 if a < 20 else 0.05 if p.sex == "F" else 0.012,
            "esrd": 0.0 if a < 25 else 0.0011 if a < 50 else 0.0026,
            "hiv": 0.0 if a < 20 else 0.0034,
            "autoimmune": 0.005 if a < 18 else 0.026,
            "hemophilia": 0.0003 if p.sex == "M" else 0.0,
            "cf": 0.00045 if a < 40 else 0.0,
            "afib": 0.0 if a < 40 else 0.008 if a < 55 else 0.022,
            "cad": 0.0 if a < 40 else 0.006 if a < 55 else 0.02,
            "liver": 0.0 if a < 30 else 0.0016,
            "hepc": 0.0 if a < 20 else 0.0032,
            "kidney_tx": 0.0 if a < 25 else 0.0005,
            "chf": 0.0 if a < 40 else 0.003 if a < 55 else 0.009,
            "copd": 0.0 if a < 40 else 0.004 if a < 55 else 0.011,
        }
        for c, q in pr.items():
            if r.random() < q:
                p.conds[c] = d - dt.timedelta(days=int(r.integers(200, 3000)))
        if "esrd" in p.conds and "kidney_tx" in p.conds:
            del p.conds["esrd"]
        if "esrd" in p.conds:
            p.conds.setdefault("htn", p.conds["esrd"])
        for c in list(p.conds):
            self.start_regimen(p, c, d)
        p.nchronic = sum(1 for c in p.conds if c in CHRONIC)

    def reg(self, p, key, drug, days, d, until=None):
        first = d + dt.timedelta(days=int(self.rp.integers(0, max(1, min(days, 30)))))
        p.regs[key] = [drug, days, until, first]

    def start_regimen(self, p, c, d):
        r = self.rp
        days90 = r.random() < 0.38
        if c == "diabetes":
            self.reg(p, "metformin", "metformin_er" if r.random() < 0.3 else "metformin", 90 if days90 else 30, d)
            u = r.random()
            if u < 0.42:
                self.reg(p, "glp1", str(r.choice(["ozempic_05", "ozempic_1", "ozempic_2", "mounjaro_5", "mounjaro_10"])), 28, d)
            elif u < 0.55:
                self.reg(p, "insulin", "lantus", 30, d)
            if r.random() < 0.14:
                self.reg(p, "sglt2", "jardiance", 30, d)
        elif c == "htn":
            self.reg(p, "htn", str(r.choice(["lisinopril", "amlodipine", "losartan"])), 90 if days90 else 30, d)
        elif c in ("lipid", "cad"):
            self.reg(p, "lipid", "atorvastatin", 90 if days90 else 30, d)
        elif c == "asthma":
            self.reg(p, "albuterol", "albuterol", 75, d)
            if r.random() < 0.35:
                self.reg(p, "montelukast", "montelukast", 30, d)
            if r.random() < 0.05:
                self.reg(p, "dupixent", "dupixent", 28, d)
            elif r.random() < 0.16:
                self.reg(p, "inhaler", "trelegy", 30, d)
        elif c == "depression":
            if r.random() < 0.7:
                self.reg(p, "ssri", str(r.choice(["sertraline", "escitalopram"])), 90 if days90 else 30, d)
        elif c == "thyroid":
            self.reg(p, "thyroid", "levothyroxine", 90 if days90 else 30, d)
        elif c == "hiv":
            self.reg(p, "art", "biktarvy", 30, d)
        elif c == "autoimmune":
            u = r.random()
            if u < 0.5:
                self.reg(p, "biologic", str(r.choice(["humira", "enbrel", "stelara", "dupixent"], p=[0.42, 0.24, 0.2, 0.14])),
                         84 if False else 28, d)
                if p.regs["biologic"][0] == "stelara":
                    p.regs["biologic"][1] = 84
            elif u < 0.57:
                p.regs["infusion"] = ["infliximab", 56, None, d]
        elif c == "hemophilia":
            self.reg(p, "factor", "hemlibra", 28, d)
        elif c == "cf":
            self.reg(p, "cftr", "trikafta", 28, d)
        elif c == "afib":
            self.reg(p, "anticoag", "eliquis", 30, d)
        elif c == "copd":
            self.reg(p, "albuterol", "albuterol", 75, d)
            if r.random() < 0.7:
                self.reg(p, "inhaler", "trelegy", 30, d)
        elif c == "chf":
            if r.random() < 0.55:
                self.reg(p, "arni", "entresto", 30, d)
            else:
                self.reg(p, "htn", "losartan", 30, d)
            if r.random() < 0.3:
                self.reg(p, "sglt2", "jardiance", 30, d)
        elif c in ("kidney_tx", "liver_tx"):
            self.reg(p, "tac", "tacrolimus", 30, d)
            self.reg(p, "mmf", "mycophenolate", 30, d)

    # ---------------------------------------------------------------- recording an event
    def add(self, p, d0, d1, ben, kind, amount, info=None, parts=None):
        """one service event. parts: (claim type P/I/R, provider kind, share of the allowed amount)"""
        if amount <= 0:
            return
        yrs = (d0 - dt.date(2025, 7, 1)).days / 365.25
        amt = amount * (W.TREND_MED ** yrs if ben == "M" else W.TREND_RX ** yrs)
        if parts is None:
            parts = [("P", "primary", 1.0)]
        rc = self.rc
        comps = []
        for ct, prov, share in parts:
            if ben == "R":
                lag = 0
            elif ct == "I":
                lag = int(min(240, 5 + rc.lognormal(math.log(31), 0.55)))
            else:
                lag = int(min(200, 3 + rc.lognormal(math.log(17), 0.62)))
            comps.append((ct, prov, round(amt * share, 2), lag))
        self.events.append((p.pid, d0, d1, ben, kind, tuple(comps), info))

    # ---------------------------------------------------------------- the run
    def run(self):
        r = self.rp
        while sum(len(f.members) for f in self.fams) < 5905:
            self.new_family(W.SIM_START, cls="R" if r.random() < 0.075 else None, hired=False)
        for fam in self.fams:
            fam.root = self.new_root()
        for m in range(W.N_MONTHS):
            self.month(m)
        self.finish()

    def month(self, m):
        r = self.rp
        ms, me = W.month_start(m), W.month_end(m)
        for fam in list(self.fams):
            if fam.active:
                self.life(fam, ms, me)
        n_cov = sum(1 for p in self.people if p.covered_on(ms))
        gap = 5905 + 3.0 * m - n_cov
        if ms.month == 9:
            n_new = max(0, int(gap / 2.25) + int(r.integers(4, 10)))
        else:
            n_new = max(0, int(gap / 2.25 * 0.25)) + (1 if r.random() < 0.5 else 0)
        for _ in range(n_new):
            fam = self.new_family(ms)
            if ms < W.CONVERSION:
                fam.root = self.new_root()
        i = 0
        while i < len(self.people):          # newborns join the list during the month and are seen the same month
            p = self.people[i]
            i += 1
            if p.start is None or p.start > me or (p.end is not None and p.end < ms):
                continue
            self.health(p, ms, me)

    # ---------------------------------------------------------------- life events
    def life(self, fam, ms, me):
        r = self.rp
        mem = [self.people[i] for i in fam.members if self.people[i].end is None]
        sub = self.people[fam.members[0]]
        if not mem or sub.end is not None:
            fam.active = False
            for p in mem:
                p.end = me
            return
        a = sub.age(ms)
        if fam.cls == "R":
            if ms == W.D(sub.dob.year + 65, sub.dob.month, 1):
                self.end_family(fam, ms - DAY)
                return
        else:
            q = 0.16 if a < 30 else 0.075 if a < 55 else 0.06
            if a >= 55:
                q += 0.07 if a < 62 else 0.16 if a < 65 else 0.34
            q_m = 1 - (1 - q) ** (1 / 12)
            q_m *= 2.6 if ms.month in (6, 7) else 0.66
            if sub.dis_until is not None and ms <= sub.dis_until:
                q_m += 0.022
            if r.random() < q_m:
                if 55 <= a < 64 and r.random() < 0.5:
                    fam.cls = "R"
                    fam.cls_hist.append((W.add_months(ms, 1), "R"))
                else:
                    end = W.D(ms.year, 8, 31) if (fam.cls == "T" and ms.month in (6, 7)) else me
                    self.end_family(fam, end)
                    return
        for p in mem:
            if p.rel == "C" and p.age(me) >= 26:
                p.end = me
        plan, tier = fam.hist[-1][1], fam.hist[-1][2]
        if tier in ("EE", "EC") and 24 <= a <= 52 and r.random() < 0.0011:
            wd = ms + dt.timedelta(days=int(r.integers(0, (me - ms).days + 1)))
            sa = int(min(60, max(22, a + r.normal(0, 4))))
            self.add_person(fam, "S", "M" if sub.sex == "F" else "F",
                            wd - dt.timedelta(days=int(sa * 365.25 + r.integers(0, 365))), wd)
            self.set_tier(fam, wd)
        if ms.month == 7 and r.random() < 0.045:
            fam.hist.append((ms, "PPO" if plan == "HDHP" else "HDHP", fam.hist[-1][2]))
        self.set_tier(fam, ms)

    def set_tier(self, fam, d):
        mem = [self.people[i] for i in fam.members]
        mem = [p for p in mem if p.start <= d and (p.end is None or p.end >= d)]
        has_sp = any(p.rel == "S" for p in mem)
        has_ch = any(p.rel == "C" for p in mem)
        tier = "FAM" if has_sp and has_ch else "ES" if has_sp else "EC" if has_ch else "EE"
        if tier != fam.hist[-1][2]:
            fam.hist.append((d, fam.hist[-1][1], tier))

    def end_family(self, fam, end):
        for i in fam.members:
            p = self.people[i]
            if p.end is None:
                p.end = end
        fam.active = False

    def die(self, p, d):
        p.death = d
        p.end = d
        fam = self.fams[p.fid]
        if p.rel in ("E", "R"):
            last = W.month_end(W.month_index(d))
            for i in fam.members:
                q = self.people[i]
                if q.end is None:
                    q.end = last
            fam.active = False
        elif fam.active:
            self.set_tier(fam, d + DAY)

    def birth(self, mother, d):
        fam = self.fams[mother.fid]
        sub = self.people[fam.members[0]]
        if not fam.active or (sub.end is not None and sub.end < d) or (mother.end is not None and mother.end < d):
            return None
        baby = self.add_person(fam, "C", "F" if self.rp.random() < 0.49 else "M", d, d)
        self.set_tier(fam, d)
        return baby

    # ---------------------------------------------------------------- health
    def health(self, p, ms, me):
        r = self.rh
        d0 = max(ms, p.start)
        d1 = me if p.end is None else min(me, p.end)
        if d1 < d0:
            return
        span = (d1 - d0).days + 1
        frac = span / ((me - ms).days + 1)

        def day():
            return d0 + dt.timedelta(days=int(r.integers(0, span)))

        a = p.age(d0)
        if self.mortality(p, a, d0, d1, frac):
            return
        f = p.frailty
        nc = p.nchronic
        if a < 2:
            lam = 0.42
        elif a < 18:
            lam = 0.15
        elif a < 40:
            lam = 0.17 if p.sex == "M" else 0.25
        else:
            lam = 0.24 if p.sex == "M" else 0.30
        for _ in range(r.poisson(1.12 * lam * f * (1 + 0.32 * nc) * frac)):
            dd = day()
            spec = r.random() < 0.36 + 0.05 * nc
            self.add(p, dd, dd, "M", "office_spec" if spec else "office", r.lognormal(math.log(171 if spec else 139), 0.28),
                     {"dx": self.pick_dx(p)}, [("P", "specialist" if spec else "primary", 1.0)])
        if p.dob.month == ms.month and p.covered_on(ms) and r.random() < (0.86 if a < 18 else 0.6):
            dd = day()
            self.add(p, dd, dd, "M", "preventive", r.lognormal(math.log(268 if a < 18 else 236), 0.18),
                     {"dx": "Z00.129" if a < 18 else "Z00.00"}, [("P", "primary", 1.0)])
        for _ in range(r.poisson(0.11 * f * (1 + 0.65 * nc) * frac)):
            dd = day()
            self.add(p, dd, dd, "M", "lab", r.lognormal(math.log(96), 0.55), {"dx": self.pick_dx(p)}, [("P", "lab", 1.0)])
        for _ in range(r.poisson(0.027 * f * (1 + 0.3 * nc) * frac)):
            dd = day()
            kind = str(r.choice(["xray", "ct", "mri", "us"], p=[0.5, 0.18, 0.17, 0.15]))
            base = {"xray": 140, "ct": 760, "mri": 1180, "us": 390}[kind]
            self.add(p, dd, dd, "M", "img_" + kind, r.lognormal(math.log(base), 0.3), {"dx": self.pick_dx(p)},
                     [("I", "hospital", 0.82), ("P", "imaging", 0.18)])
        lam_er = (0.026 if a < 5 else 0.013 if a < 18 else 0.016) * math.sqrt(f) * (1 + 0.25 * nc) * frac
        for _ in range(r.poisson(lam_er)):
            dd = day()
            self.add(p, dd, dd, "M", "er", r.lognormal(math.log(2880), 0.5), {"dx": str(r.choice(W.ICD["er"]))},
                     [("I", "hospital", 0.78), ("P", "specialist", 0.22)])
        for _ in range(r.poisson(0.028 * f * frac)):
            dd = day()
            self.add(p, dd, dd, "M", "urgent", r.lognormal(math.log(205), 0.2), {"dx": str(r.choice(W.ICD["acute"]))},
                     [("P", "urgent", 1.0)])
        lam_op = (0.0037 if a < 30 else 0.0088 if a < 50 else 0.0155) * f * frac
        for _ in range(r.poisson(lam_op)):
            dd = day()
            self.add(p, dd, dd, "M", "op_surgery", r.lognormal(math.log(5600), 0.45), {"dx": self.pick_dx(p)},
                     [("I", "asc" if r.random() < 0.5 else "hospital", 0.74), ("P", "specialist", 0.2), ("P", "anesthesia", 0.06)])
        lam_ip = (0.0014 if a < 18 else 0.0022 if a < 45 else 0.0039) * math.sqrt(f) * (1 + 0.4 * nc) * frac
        for _ in range(r.poisson(lam_ip)):
            self.admission(p, day(), r.lognormal(math.log(25500), 0.55), str(r.choice(W.ICD["admit_misc"])))
        # hospital outpatient services: endoscopy suites, cardiac testing, sleep studies, wound care, infusion chairs
        for _ in range(r.poisson(0.021 * f * (1 + 0.45 * nc) * frac)):
            dd = day()
            self.add(p, dd, dd, "M", "op_hospital", r.lognormal(math.log(1250), 0.6), {"dx": self.pick_dx(p)},
                     [("I", "hospital", 0.86), ("P", "specialist", 0.14)])
        if a >= 12 and r.random() < 0.0055 * frac:
            self.course(p, ms, "pt", int(r.integers(6, 12)), 132, 2)
        if "depression" in p.conds and r.random() < 0.06 * frac:
            self.course(p, ms, "therapy", int(r.integers(5, 16)), 128, int(r.integers(2, 6)))
        self.chronic(p, a, d0, d1, frac, day)
        self.incidence(p, a, d0, d1, frac, day)
        self.episodes(p, d0, d1, frac, day)
        self.pharmacy(p, a, d0, d1)
        ys = self.cond_years.setdefault((p.pid, d0.year), set())
        ys.update(c for c in p.conds if c in CHRONIC)
        if any(e["kind"] == "cancer" for e in p.eps):
            ys.add("cancer")

    def pick_dx(self, p):
        r = self.rh
        cs = [c for c in p.conds if c in W.ICD]
        if cs and r.random() < 0.55:
            return str(r.choice(W.ICD[str(r.choice(cs))]))
        return str(r.choice(W.ICD["acute"]))

    def admission(self, p, d, amount, dx, los=None, icu=False, kind="admit", followup=True):
        r = self.rh
        if los is None:
            los = int(max(1, min(14, round(r.lognormal(math.log(3.2), 0.5)))))
        d1 = d + dt.timedelta(days=los)
        if p.end is not None and d1 > p.end:
            d1 = max(d, p.end)
        self.add(p, d, d1, "M", kind, amount, {"dx": dx, "los": (d1 - d).days, "icu": icu},
                 [("I", "hospital", 0.84), ("P", "specialist", 0.12), ("P", "primary", 0.04)])
        if followup and amount > 20000:
            p.eps.append({"kind": "postacute", "m": 0, "start": d1, "big": amount > 45000 or kind != "admit", "dx": dx})
            if r.random() < 0.55:
                drug = str(r.choice(["eliquis", "enoxaparin", "ondansetron", "amoxicillin"], p=[0.45, 0.25, 0.15, 0.15]))
                n = int(r.integers(1, 4)) if drug == "eliquis" else 1
                self.reg(p, "discharge", drug, 30 if drug != "enoxaparin" else 10, d1 + DAY, until=d1 + dt.timedelta(days=30 * n))
            if amount > 45000 and p.rel == "E":
                p.dis_until = d1 + dt.timedelta(days=420)

    def course(self, p, ms, kind, n, base, per_month):
        r = self.rh
        k, mo = 0, 0
        while k < n:
            mstart = W.add_months(ms, mo)
            for _ in range(per_month):
                if k >= n:
                    break
                dd = mstart + dt.timedelta(days=int(r.integers(0, 27)))
                if (p.end is not None and dd > p.end) or dd > W.SIM_END:
                    return
                if dd < p.start:
                    continue
                self.add(p, dd, dd, "M", kind, r.lognormal(math.log(base), 0.15),
                         {"dx": str(r.choice(W.ICD["pt"])) if kind == "pt" else "F33.1"},
                         [("P", "therapy" if kind == "pt" else "behavioral", 1.0)])
                k += 1
            mo += 1

    # ---------------------------------------------------------------- mortality
    def mortality(self, p, a, d0, d1, frac):
        r = self.rh
        q = 0.0002 if a < 1 else 0.0003 if a < 25 else 0.0009 if a < 45 else 0.0026 if a < 55 else 0.0058
        q_m = 1 - (1 - q) ** (1 / 12)
        if "esrd" in p.conds:
            q_m += 0.0095
        if "liver" in p.conds:
            q_m += 0.004
        if "chf" in p.conds:
            q_m += 0.003
        for e in p.eps:
            q_m += e.get("hazard", 0.0)
        if r.random() >= q_m * frac:
            return False
        dd = d0 + dt.timedelta(days=int(r.integers(0, (d1 - d0).days + 1)))
        if q_m > 0.004 and r.random() < 0.7:
            st = max(d0, dd - dt.timedelta(days=int(r.integers(2, 12))))
            self.add(p, st, dd, "M", "admit", r.lognormal(math.log(46000), 0.5),
                     {"dx": self.pick_dx(p), "los": (dd - st).days, "icu": True},
                     [("I", "hospital", 0.85), ("P", "specialist", 0.15)])
        self.die(p, dd)
        return True

    # ---------------------------------------------------------------- chronic care
    def chronic(self, p, a, d0, d1, frac, day):
        r = self.rh
        c = p.conds
        if r.random() < 0.33 * frac and any(k in c for k in ("diabetes", "htn", "lipid", "thyroid", "afib", "cad", "hiv", "autoimmune")):
            dd = day()
            sp = "hiv" in c or "autoimmune" in c
            self.add(p, dd, dd, "M", "office_spec" if sp else "office", r.lognormal(math.log(165), 0.2),
                     {"dx": self.pick_dx(p)}, [("P", "specialist" if sp else "primary", 1.0)])
            self.add(p, dd, dd, "M", "lab", r.lognormal(math.log(118), 0.3), {"dx": self.pick_dx(p)}, [("P", "lab", 1.0)])
        if "esrd" in c:
            sessions = max(1, int(round(13 * frac)))
            self.add(p, d0, d1, "M", "dialysis", 1075.0 * sessions * r.lognormal(0, 0.05), {"dx": "N18.6", "sessions": sessions},
                     [("I", "dialysis", 0.96), ("P", "specialist", 0.04)])
            if r.random() < 0.045 * frac:
                self.admission(p, day(), r.lognormal(math.log(36000), 0.45), "N18.6")
            if a < 66 and r.random() < 0.0045 * frac:
                p.eps.append({"kind": "transplant", "organ": "kidney", "m": 0, "start": day()})
                del c["esrd"]
        if "liver" in c:
            if r.random() < 0.35 * frac:
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(240), 0.2), {"dx": "K74.60"}, [("P", "specialist", 1.0)])
            if r.random() < 0.028 * frac:
                self.admission(p, day(), r.lognormal(math.log(31000), 0.5), "K74.60")
            if a < 66 and r.random() < 0.0065 * frac:
                p.eps.append({"kind": "transplant", "organ": "liver", "m": 0, "start": day()})
                del c["liver"]
        for k_, dxk in (("chf", "I50.22"), ("copd", "J44.1")):
            if k_ in c:
                for _ in range(r.poisson(0.9 * frac)):
                    dd = day()
                    self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(205), 0.25), {"dx": dxk}, [("P", "specialist", 1.0)])
                if r.random() < 0.05 * frac:
                    dd = day()
                    self.add(p, dd, dd, "M", "er", r.lognormal(math.log(3100), 0.4), {"dx": dxk},
                             [("I", "hospital", 0.78), ("P", "specialist", 0.22)])
                if r.random() < 0.038 * frac:
                    self.admission(p, day(), r.lognormal(math.log(27000), 0.45), dxk)
                if r.random() < 0.12 * frac:
                    dd = day()
                    self.add(p, dd, dd, "M", "op_hospital", r.lognormal(math.log(1500), 0.4), {"dx": dxk},
                             [("I", "hospital", 0.86), ("P", "specialist", 0.14)])
        if "hemophilia" in c:
            if r.random() < 0.25 * frac:
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(320), 0.2), {"dx": "D66"}, [("P", "specialist", 1.0)])
            if r.random() < 0.012 * frac:
                self.admission(p, day(), r.lognormal(math.log(28000), 0.5), "D66")
        if "cf" in c:
            if r.random() < 0.34 * frac:
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(410), 0.25), {"dx": "E84.0"}, [("P", "specialist", 1.0)])
            if r.random() < 0.012 * frac:
                self.admission(p, day(), r.lognormal(math.log(42000), 0.5), "E84.0")
        if "kidney_tx" in c or "liver_tx" in c:
            dx = "Z94.0" if "kidney_tx" in c else "Z94.4"
            if r.random() < 0.4 * frac:
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(330), 0.25), {"dx": dx}, [("P", "transplant", 1.0)])
                self.add(p, dd, dd, "M", "lab", r.lognormal(math.log(260), 0.3), {"dx": dx}, [("P", "lab", 1.0)])
        inf = p.regs.get("infusion")
        if inf is not None:
            while inf[3] <= d1:
                if inf[3] >= d0:
                    self.add(p, inf[3], inf[3], "M", "infusion", r.lognormal(math.log(6400), 0.12), {"dx": "K50.90"},
                             [("I", "hospital", 0.94), ("P", "specialist", 0.06)])
                inf[3] = inf[3] + dt.timedelta(days=56 + int(r.integers(-3, 6)))
        if "cancer_hx" in c and not any(e["kind"] == "cancer" for e in p.eps) and r.random() < 0.12 * frac:
            dd = day()
            self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(260), 0.25), {"dx": "Z08"}, [("P", "oncology", 1.0)])
            if r.random() < 0.35:
                self.add(p, dd, dd, "M", "img_ct", r.lognormal(math.log(820), 0.25), {"dx": "Z08"},
                         [("I", "hospital", 0.82), ("P", "imaging", 0.18)])

    # ---------------------------------------------------------------- new conditions and episodes
    def incidence(self, p, a, d0, d1, frac, day):
        r = self.rh

        def hit(annual):
            return r.random() < (1 - (1 - annual) ** (1 / 12)) * frac

        c = p.conds
        if a >= 25 and not any(e["kind"] == "cancer" for e in p.eps):
            inc = 0.0011 if a < 40 else 0.0027 if a < 50 else 0.0058 if a < 60 else 0.0092
            if p.sex == "M" and a >= 50:
                inc += 0.0025
            if hit(inc):
                self.start_cancer(p, a, day())
        for cond, test, annual in (("diabetes", a >= 30, 0.004 if a < 45 else 0.008),
                                   ("htn", a >= 25, 0.006 if a < 45 else 0.014),
                                   ("depression", a >= 12, 0.012),
                                   ("autoimmune", a >= 18, 0.0011),
                                   ("afib", a >= 45, 0.0015 if a < 55 else 0.003),
                                   ("chf", a >= 45, 0.0007 if a < 55 else 0.0016),
                                   ("copd", a >= 45, 0.0008 if a < 55 else 0.0018)):
            if test and cond not in c and hit(annual):
                c[cond] = d0
                self.start_regimen(p, cond, d0)
        if "diabetes" in c and "esrd" not in c and "kidney_tx" not in c and a >= 35 and hit(0.0016):
            c["esrd"] = d0
        if a >= 30 and "liver" not in c and "liver_tx" not in c and hit(0.00018):
            c["liver"] = d0
        if "hepc" in c and hit(0.17):
            p.eps.append({"kind": "hepc", "m": 0, "start": day(), "drug": "mavyret" if r.random() < 0.55 else "epclusa"})
            del c["hepc"]
        if a >= 5 and hit(0.0011 + (0.0018 if (p.sex == "M" and 16 <= a <= 30) else 0.0)):
            self.trauma(p, day())
        if a >= 30 and hit(0.0016 if a < 45 else 0.0036 if a < 55 else 0.0062):
            self.major_surgery(p, day())
        if a >= 45 and hit(0.0011 if a < 55 else 0.0024):
            self.stroke(p, day())
        if a >= 50 and hit(0.0042 if a < 58 else 0.0078):
            p.eps.append({"kind": "joint", "m": 0, "start": day(), "site": "knee" if r.random() < 0.6 else "hip"})
        if a >= 35 and hit((0.0006 if a < 45 else 0.0022 if a < 55 else 0.0042) * (1.8 if p.sex == "M" else 0.6)):
            self.heart_attack(p, day())
        if p.sex == "F" and 20 <= a <= 43 and p.rel in ("E", "S") and not any(e["kind"] == "preg" for e in p.eps):
            if hit(0.115 if a < 33 else 0.072 if a < 38 else 0.025):
                self.pregnancy(p, day())
        p.nchronic = sum(1 for k in c if k in CHRONIC)

    def start_cancer(self, p, a, d):
        r = self.rh
        if p.sex == "F" and r.random() < 0.42:
            site = "breast"
        elif p.sex == "M" and a >= 50 and r.random() < 0.38:
            site = "prostate"
        else:
            site = str(r.choice(["colon", "lung", "lymphoma", "cll", "breast" if p.sex == "F" else "colon"],
                                p=[0.3, 0.22, 0.2, 0.12, 0.16]))
        meta = r.random() < {"breast": 0.12, "colon": 0.2, "lung": 0.48, "lymphoma": 0.1, "cll": 0.0, "prostate": 0.08}[site]
        e = {"kind": "cancer", "site": site, "meta": meta, "m": 0, "start": d,
             "tx": {"breast": int(r.integers(6, 13)), "colon": int(r.integers(5, 8)), "lymphoma": int(r.integers(5, 8)),
                    "lung": int(r.integers(6, 13)), "prostate": int(r.integers(2, 4))}.get(site, 3),
             "hazard": 0.032 if meta else 0.0015, "oral": None}
        if p.rel == "E" and site != "cll":
            p.dis_until = d + dt.timedelta(days=480)
        if site == "cll" and r.random() < 0.55:
            e["oral"] = "imbruvica"
        if meta and site == "breast":
            e["oral"] = "ibrance"
        if meta and site == "prostate":
            e["oral"] = "xtandi"
        p.eps.append(e)

    def trauma(self, p, d):
        r = self.rh
        amt = r.lognormal(math.log(52000), 0.75)
        self.add(p, d, d, "M", "ambulance", r.lognormal(math.log(1650), 0.2), {"dx": "V43.52XA"}, [("P", "ambulance", 1.0)])
        los = int(max(2, min(30, round(r.lognormal(math.log(5), 0.6)))))
        self.admission(p, d, amt, str(r.choice(W.ICD["trauma"])), los=los, icu=amt > 90000, kind="admit_trauma")
        p.eps.append({"kind": "rehab", "m": 0, "start": d, "months": int(r.integers(2, 5)), "hazard": 0.004})

    def major_surgery(self, p, d):
        """spinal fusion, valve or bypass surgery, bariatric and complex abdominal surgery: one stay, then recovery"""
        r = self.rh
        what = str(r.choice(["spine", "cardiac", "abdominal", "bariatric"], p=[0.38, 0.22, 0.28, 0.12]))
        base = {"spine": 78000, "cardiac": 118000, "abdominal": 54000, "bariatric": 31000}[what]
        dx = {"spine": "M48.062", "cardiac": "I35.0", "abdominal": "K57.20", "bariatric": "E66.01"}[what]
        self.admission(p, d, r.lognormal(math.log(base), 0.35), dx, los=int(r.integers(2, 9)), icu=what == "cardiac",
                       kind="admit_surgery")
        p.eps.append({"kind": "rehab", "m": 0, "start": d, "months": int(r.integers(1, 4)), "hazard": 0.003})

    def stroke(self, p, d):
        r = self.rh
        self.add(p, d, d, "M", "ambulance", r.lognormal(math.log(1700), 0.2), {"dx": "I63.9"}, [("P", "ambulance", 1.0)])
        self.admission(p, d, r.lognormal(math.log(61000), 0.45), "I63.9", los=int(r.integers(3, 10)), icu=True,
                       kind="admit_cardiac")
        p.eps.append({"kind": "rehab", "m": 0, "start": d, "months": int(r.integers(2, 5)), "hazard": 0.012})
        if "afib" not in p.conds and r.random() < 0.3:
            p.conds["afib"] = d
            self.start_regimen(p, "afib", d)

    def heart_attack(self, p, d):
        r = self.rh
        self.add(p, d, d, "M", "ambulance", r.lognormal(math.log(1700), 0.2), {"dx": "I21.4"}, [("P", "ambulance", 1.0)])
        self.admission(p, d, r.lognormal(math.log(68000), 0.45), "I21.4", los=int(r.integers(2, 7)), icu=True, kind="admit_cardiac")
        p.conds["cad"] = d
        self.start_regimen(p, "cad", d)
        p.eps.append({"kind": "cardiac_rehab", "m": 0, "start": d, "months": 3, "hazard": 0.006})

    def pregnancy(self, p, d):
        r = self.rh
        pre = r.random() < 0.095
        weeks = int(r.integers(25, 36)) if pre else int(r.integers(37, 41))
        p.eps.append({"kind": "preg", "m": 0, "start": d, "due": d + dt.timedelta(days=weeks * 7 - 14),
                      "loss": r.random() < 0.13, "pre": pre, "weeks": weeks, "csec": r.random() < (0.45 if pre else 0.3)})

    # ---------------------------------------------------------------- episode care
    def episodes(self, p, d0, d1, frac, day):
        r = self.rh
        keep = []
        for e in p.eps:
            k = e["kind"]
            if k == "cancer":
                alive = self.cancer_month(p, e, d0, d1, frac, day)
            elif k == "transplant":
                alive = self.transplant_month(p, e, d0, d1, day)
            elif k == "rehab":
                if e["m"] >= 1:
                    for _ in range(int(r.integers(3, 8))):
                        dd = day()
                        self.add(p, dd, dd, "M", "pt", r.lognormal(math.log(138), 0.15), {"dx": "M25.561"}, [("P", "therapy", 1.0)])
                    if r.random() < 0.5:
                        dd = day()
                        self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(210), 0.2), {"dx": "Z47.89"}, [("P", "specialist", 1.0)])
                    e["hazard"] = 0.0
                alive = e["m"] < e["months"]
            elif k == "cardiac_rehab":
                if e["m"] >= 1:
                    dd = day()
                    self.add(p, dd, dd, "M", "cardiac_rehab", r.lognormal(math.log(1450), 0.2), {"dx": "I25.10"},
                             [("I", "hospital", 0.9), ("P", "specialist", 0.1)])
                    e["hazard"] = 0.0
                alive = e["m"] < e["months"]
            elif k == "joint":
                if e["m"] == 0:
                    dd = max(e["start"], d0)
                    self.add(p, dd, dd + dt.timedelta(days=int(r.integers(1, 3))), "M", "joint", r.lognormal(math.log(41000), 0.2),
                             {"dx": "M17.11" if e["site"] == "knee" else "M16.11", "site": e["site"]},
                             [("I", "hospital", 0.82), ("P", "specialist", 0.13), ("P", "anesthesia", 0.05)])
                elif e["m"] <= 3:
                    for _ in range(int(r.integers(4, 9))):
                        dd = day()
                        self.add(p, dd, dd, "M", "pt", r.lognormal(math.log(141), 0.15), {"dx": "Z47.1"}, [("P", "therapy", 1.0)])
                alive = e["m"] < 3
            elif k == "hepc":
                fills = 2 if e["drug"] == "mavyret" else 3
                if e["m"] == 0:
                    dd = max(e["start"], d0)
                    self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(330), 0.2), {"dx": "B18.2"}, [("P", "specialist", 1.0)])
                    self.add(p, dd, dd, "M", "lab", r.lognormal(math.log(420), 0.2), {"dx": "B18.2"}, [("P", "lab", 1.0)])
                    p.regs["hcv"] = [e["drug"], 28, None, dd + dt.timedelta(days=int(r.integers(3, 12)))]
                    e["fills"] = 0
                alive = e["m"] < fills + 1
            elif k == "postacute":
                alive = self.postacute_month(p, e, d0, d1, day)
            elif k == "preg":
                alive = self.pregnancy_month(p, e, d0, d1, day)
            elif k == "nicu":
                alive = self.nicu_month(p, e, day)
            else:
                alive = False
            e["m"] += 1
            if alive:
                keep.append(e)
        p.eps = keep
        p.nchronic = sum(1 for c in p.conds if c in CHRONIC) + (1 if any(e["kind"] == "cancer" for e in p.eps) else 0)

    def cancer_month(self, p, e, d0, d1, frac, day):
        r = self.rh
        m, site = e["m"], e["site"]
        dx = W.ICD[site][0] if site != "breast" else W.ICD["breast"][p.pid % 2]
        if m == 0:
            dd = max(d0, e["start"])
            self.add(p, dd, dd, "M", "img_ct", r.lognormal(math.log(2400), 0.3), {"dx": dx},
                     [("I", "hospital", 0.82), ("P", "imaging", 0.18)])
            self.add(p, dd, dd, "M", "biopsy", r.lognormal(math.log(3300), 0.35), {"dx": dx},
                     [("I", "hospital", 0.7), ("P", "specialist", 0.3)])
            self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(420), 0.2), {"dx": dx}, [("P", "oncology", 1.0)])
            return True
        surg = site in ("breast", "colon", "lung", "prostate") and not (e["meta"] and site == "lung")
        if surg and m == 1:
            base = {"breast": 26000, "colon": 47000, "lung": 52000, "prostate": 29000}[site]
            self.admission(p, day(), r.lognormal(math.log(base), 0.3), dx, los=int(r.integers(1, 5)), kind="admit_surgery")
            return True
        if e["meta"] or site == "cll":
            if e["oral"] and "onc" not in p.regs:
                p.regs["onc"] = [e["oral"], 28, None, day()]
            if e["meta"] and not e["oral"]:
                dd = day()
                self.add(p, dd, dd, "M", "chemo", r.lognormal(math.log(16500), 0.3) * frac, {"dx": dx, "site": site},
                         [("I", "hospital", 0.9), ("P", "oncology", 0.1)])
            if r.random() < (0.5 if e["meta"] else 0.25):
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(380), 0.2), {"dx": dx}, [("P", "oncology", 1.0)])
            if e["meta"] and r.random() < 0.06 * frac:
                self.admission(p, day(), r.lognormal(math.log(39000), 0.45), dx)
            if site == "cll" and m > 24:
                e["hazard"] = 0.0005
            return True
        first = 2 if surg else 1
        tx = e["tx"]
        if first <= m < first + tx:
            dd = day()
            if site == "prostate":
                self.add(p, dd, dd, "M", "radiation", r.lognormal(math.log(14500), 0.25) * frac, {"dx": dx},
                         [("I", "hospital", 0.86), ("P", "oncology", 0.14)])
            else:
                if "support" not in p.regs:
                    self.reg(p, "support", "ondansetron", 30, dd, until=dd + dt.timedelta(days=30 * (first + tx - m)))
                base = {"breast": 15500, "colon": 12800, "lung": 17500, "lymphoma": 24500}[site]
                if m - first >= 4:
                    base *= 0.55      # maintenance: the targeted or immune agent alone, every three weeks
                self.add(p, dd, dd, "M", "chemo", r.lognormal(math.log(base), 0.28) * frac, {"dx": dx, "site": site},
                         [("I", "hospital", 0.9), ("P", "oncology", 0.1)])
                if r.random() < 0.05:
                    self.admission(p, day(), r.lognormal(math.log(29000), 0.45), dx)
            return True
        if site == "breast" and first + tx <= m < first + tx + 2:
            dd = day()
            self.add(p, dd, dd, "M", "radiation", r.lognormal(math.log(11800), 0.25) * frac, {"dx": dx},
                     [("I", "hospital", 0.86), ("P", "oncology", 0.14)])
            return True
        p.conds["cancer_hx"] = d0
        return False

    def transplant_month(self, p, e, d0, d1, day):
        r = self.rh
        m = e["m"]
        kid = e["organ"] == "kidney"
        dx = "Z94.0" if kid else "Z94.4"
        if m == 0:
            dd = max(d0, e["start"])
            los = int(r.integers(4, 9) if kid else r.integers(9, 22))
            self.add(p, dd, dd + dt.timedelta(days=los), "M", "transplant", r.lognormal(math.log(385000 if kid else 760000), 0.18),
                     {"dx": "N18.6" if kid else "K74.60", "organ": e["organ"], "los": los},
                     [("I", "hospital", 0.86), ("P", "transplant", 0.11), ("P", "anesthesia", 0.03)])
            p.conds["kidney_tx" if kid else "liver_tx"] = dd
            self.start_regimen(p, "kidney_tx", dd)
            e["hazard"] = 0.006
            return True
        if m <= 3:
            for _ in range(int(r.integers(3, 6))):
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(560), 0.3), {"dx": dx}, [("P", "transplant", 1.0)])
            dd = day()
            self.add(p, dd, dd, "M", "lab", r.lognormal(math.log(1400), 0.3), {"dx": dx}, [("P", "lab", 1.0)])
            if r.random() < 0.18:
                self.admission(p, day(), r.lognormal(math.log(41000), 0.4), dx)
            return True
        if m <= 12:
            dd = day()
            self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(900), 0.3), {"dx": dx}, [("P", "transplant", 1.0)])
            e["hazard"] = 0.0015
            return True
        return False

    def postacute_month(self, p, e, d0, d1, day):
        """the months after a large stay: follow-up visits and labs, home health or a rehabilitation or nursing
        facility stay, and a readmission for some"""
        r = self.rh
        m = e["m"]
        if m == 0:
            if e["big"] and r.random() < 0.3:
                st = max(d0, e["start"])
                stay = int(r.integers(7, 21))
                self.add(p, st, st + dt.timedelta(days=stay), "M", "postacute_facility", r.lognormal(math.log(1650), 0.25) * stay,
                         {"dx": e["dx"], "los": stay}, [("I", "postacute", 0.93), ("P", "primary", 0.07)])
            return True
        if m <= 3:
            for _ in range(int(r.integers(1, 4))):
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(215), 0.25), {"dx": e["dx"]}, [("P", "specialist", 1.0)])
            if e["big"] and r.random() < 0.35:
                dd = day()
                self.add(p, dd, dd, "M", "home_health", r.lognormal(math.log(2300), 0.35), {"dx": e["dx"]},
                         [("I", "homehealth", 1.0)])
            if r.random() < (0.07 if m == 1 else 0.035):
                self.admission(p, day(), r.lognormal(math.log(24000), 0.5), e["dx"], followup=False)
            return m < 3
        return False

    def pregnancy_month(self, p, e, d0, d1, day):
        r = self.rh
        m = e["m"]
        if e["loss"] and m == 2:
            dd = day()
            self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(640), 0.3), {"dx": "O03.9"}, [("P", "obgyn", 1.0)])
            return False
        due = e["due"]
        if due > d1:
            if m >= 1:
                dd = day()
                self.add(p, dd, dd, "M", "prenatal", r.lognormal(math.log(185), 0.25), {"dx": "Z34.80"}, [("P", "obgyn", 1.0)])
                if m in (3, 6):
                    self.add(p, dd, dd, "M", "img_us", r.lognormal(math.log(380), 0.2), {"dx": "Z34.80"},
                             [("I", "hospital", 0.7), ("P", "imaging", 0.3)])
            return True
        if due < d0:
            return False
        cs = e["csec"]
        stay = int(r.integers(2, 4)) if cs else int(r.integers(1, 3))
        amt = r.lognormal(math.log(19500 if cs else 13600), 0.18) * (1.35 if e["pre"] else 1.0)
        self.add(p, due, due + dt.timedelta(days=stay), "M", "delivery", amt, {"dx": "O82" if cs else "O80", "csec": cs, "los": stay},
                 [("I", "hospital", 0.72), ("P", "obgyn", 0.21), ("P", "anesthesia", 0.07)])
        baby = self.birth(p, due)
        if baby is not None:
            if e["pre"]:
                days = int(max(8, min(95, r.lognormal(math.log(31 - (e["weeks"] - 30) * 3.2), 0.38))))
                baby.eps.append({"kind": "nicu", "m": 0, "start": due, "days": days, "weeks": e["weeks"], "hazard": 0.004})
            elif r.random() < 0.035:
                baby.eps.append({"kind": "nicu", "m": 0, "start": due, "days": int(r.integers(4, 15)), "weeks": e["weeks"], "hazard": 0.0})
            else:
                self.add(baby, due, due + dt.timedelta(days=stay), "M", "newborn", r.lognormal(math.log(3600), 0.25),
                         {"dx": "Z38.01" if cs else "Z38.00", "los": stay}, [("I", "hospital", 0.86), ("P", "primary", 0.14)])
        return False

    def nicu_month(self, p, e, day):
        r = self.rh
        m = e["m"]
        if m == 0:
            dd, days = e["start"], e["days"]
            self.add(p, dd, dd + dt.timedelta(days=days), "M", "nicu", days * r.lognormal(math.log(4350), 0.15),
                     {"dx": "P07.33" if e["weeks"] >= 30 else "P07.32", "los": days},
                     [("I", "hospital", 0.88), ("P", "neonatal", 0.12)])
            return True
        if m <= 8:
            for _ in range(int(r.integers(1, 4))):
                dd = day()
                self.add(p, dd, dd, "M", "office_spec", r.lognormal(math.log(310), 0.3), {"dx": "P07.33"}, [("P", "specialist", 1.0)])
            if r.random() < 0.07:
                self.admission(p, day(), r.lognormal(math.log(26000), 0.5), "P22.0")
            e["hazard"] = 0.0004
            return True
        return False

    # ---------------------------------------------------------------- pharmacy
    def pharmacy(self, p, a, d0, d1):
        r = self.rh
        for key in list(p.regs):
            rg = p.regs[key]
            drug, days, until, nxt = rg
            if drug == "infliximab":
                continue
            while nxt <= d1:
                if nxt >= d0 and (rg[2] is None or nxt <= rg[2]):
                    name, ndc, qty, price, bg, spec = W.DRUGS[drug]
                    ds = 25 if drug == "albuterol" else days
                    if bg == "B" or drug in W.PER_FILL:
                        amt, q = price, qty
                    else:
                        amt, q = price * ds / 30.0 * r.lognormal(0, 0.05), round(qty * ds / 30.0)
                    self.add(p, nxt, nxt, "R", "fill", amt, {"drug": drug, "qty": q, "days": ds}, [("R", "pharmacy", 1.0)])
                    if key == "hcv":
                        ep = [e for e in p.eps if e["kind"] == "hepc"]
                        if ep:
                            ep[0]["fills"] = ep[0].get("fills", 0) + 1
                            if ep[0]["fills"] >= (2 if drug == "mavyret" else 3):
                                rg[2] = nxt
                gap = int(r.integers(-2, 4)) if r.random() < 0.85 else int(r.integers(5, 25))
                nxt = nxt + dt.timedelta(days=max(20, (25 if drug == "albuterol" else days) + gap + (45 if drug == "albuterol" else 0)))
                rg[3] = nxt
            if until is not None and nxt > until:
                del p.regs[key]
        if r.random() < 0.075 * p.frailty * (1.3 if a < 12 else 1.0):
            dd = d0 + dt.timedelta(days=int(r.integers(0, (d1 - d0).days + 1)))
            self.add(p, dd, dd, "R", "fill", W.DRUGS["amoxicillin"][3] * r.lognormal(0, 0.1),
                     {"drug": "amoxicillin", "qty": 30, "days": 10}, [("R", "pharmacy", 1.0)])
        if a >= 18 and r.random() < 0.05 * p.frailty * (1 + 0.4 * p.nchronic):
            dd = d0 + dt.timedelta(days=int(r.integers(0, (d1 - d0).days + 1)))
            drug = str(r.choice(["omeprazole", "escitalopram", "montelukast", "amlodipine"]))
            self.add(p, dd, dd, "R", "fill", W.DRUGS[drug][3] * r.lognormal(0, 0.1), {"drug": drug, "qty": 30, "days": 30},
                     [("R", "pharmacy", 1.0)])

    # ---------------------------------------------------------------- identifiers after the run
    def finish(self):
        r = self.rp
        conv = W.CONVERSION - DAY
        for fam in self.fams:
            mem = [self.people[i] for i in fam.members]
            onconv = [p for p in mem if p.start <= conv and (p.end is None or p.end >= W.CONVERSION)]
            if onconv:
                if fam.root is None:
                    fam.root = self.new_root()
                kids = sorted([p for p in onconv if p.rel == "C"], key=lambda q: q.dob)
                if len(kids) > 1 and r.random() < 0.15:          # a stepchild or late enrolment out of birth order
                    kids = kids[1:] + kids[:1]
                nxt = 3 + (1 if r.random() < 0.12 else 0)          # a dependent removed before 2024 left a gap
                for p in onconv:
                    if p.rel in ("E", "R"):
                        p.legacy = fam.root + "-01"
                    elif p.rel == "S":
                        p.legacy = fam.root + "-02"
                for p in kids:
                    p.legacy = fam.root + "-%02d" % nxt
                    nxt += 1 + (1 if r.random() < 0.05 else 0)
            # Ellery numbers and person codes: subscriber 01, spouse 02, children by date of birth from 03
            live = [p for p in mem if p.end is None or p.end >= W.CONVERSION]
            kids = sorted([p for p in live if p.rel == "C"], key=lambda q: (q.start > conv, q.dob, q.pid))
            for p in live:
                p.member_id = self.new_member_id()
                p.code = "01" if p.rel in ("E", "R") else "02" if p.rel == "S" else None
            for k, p in enumerate(kids):
                p.code = "%02d" % (3 + k)
        self.events.sort(key=lambda e: (e[1], e[0], e[4]))


def simulate(seed=W.SEED):
    s = Sim(seed)
    s.run()
    return s
