"""The plan's population and its health care, member by member and month by month, January 2024 to March 2028.

Costs come from events: routine professional care, labs, imaging, emergency visits and admissions; chronic
conditions that cost something every month; and episodes that end (a cancer course, a transplant, a premature
birth, trauma, a joint replacement, a heart attack, a hepatitis C cure, a pregnancy). Each event is coded and priced
by coding.py into the claims the plan pays for it, each with its own payment lag, so what the plan knows about a
month at any cut-off is the claims paid by then. Clinic care happens on business days, emergencies on any day, and a
member is never in two hospital stays at once. 2023 and 2024 and the 2027-28 programme year are simulated and never shipped; 2023 is there so that the members who
are mid-way through a course of treatment on 1 January 2024 are, as in any plan, already in it."""
import bisect
import datetime as dt
import math

import numpy as np

import catalog as K
import coding as CD
import world as W

DAY = dt.timedelta(days=1)

CHRONIC = ("diabetes", "htn", "lipid", "asthma", "depression", "thyroid", "esrd", "hiv", "autoimmune",
           "hemophilia", "cf", "afib", "cad", "liver", "hepc", "kidney_tx", "liver_tx", "cancer_hx", "chf", "copd",
           "urticaria")
# weekday weights (Monday first), the weight on a day the clinics close, and the factor on a reduced day
PROFILES = {
    "clinic": ((1.08, 1.0, 0.97, 1.0, 0.9, 0.05, 0.0), 0.0, 0.35),
    "lab": ((1.1, 1.0, 1.0, 1.0, 0.92, 0.1, 0.0), 0.0, 0.4),
    "urgent": ((1.1, 0.95, 0.9, 0.9, 0.95, 1.05, 0.95), 0.75, 0.9),
    "any": ((1.08, 1.0, 0.97, 0.97, 1.0, 1.02, 1.02), 1.0, 1.0),
    "elective": ((1.0, 1.0, 1.0, 1.0, 0.85, 0.0, 0.0), 0.0, 0.15),
    "imaging": ((1.0, 1.0, 1.0, 1.0, 0.95, 0.12, 0.02), 0.03, 0.4),
    "therapy": ((1.0, 1.0, 1.0, 1.0, 0.8, 0.04, 0.0), 0.0, 0.2),
}
NO_TWICE = {"office", "office_spec", "preventive", "lab", "urgent", "pt", "therapy", "prenatal", "chemo", "infusion",
            "img_xray", "img_ct", "img_mri", "img_us", "op_surgery", "op_hospital", "cardiac_rehab", "biopsy",
            "home_health", "radiation", "er"}
STAY_KINDS = {"admit", "admit_trauma", "admit_cardiac", "admit_surgery", "joint", "transplant", "delivery", "newborn",
              "nicu", "postacute_facility"}
RESP = ("J06", "J02", "J01", "J20", "R05", "J00", "B34", "H66", "H65", "J21", "J05", "J03", "J18")
SLOT = {"office_spec": "visit", "office": "visit", "prenatal": "visit"}
# a chemotherapy or infusion day is also that day's visit with the treating specialist
OCCUPY = {"chemo": ("chemo", "visit"), "infusion": ("infusion", "visit")}


def slots_of(kind):
    return OCCUPY.get(kind, (SLOT.get(kind, kind),))
REHAB_SPEC = {"Z98.1": "neurosurg", "Z95.2": "cardiology", "Z48.815": "gensurg", "Z98.84": "gensurg", "I69.351": "neuro"}


class Person:
    __slots__ = ("pid", "fid", "rel", "sex", "dob", "code", "legacy", "legacy2", "member_id", "start", "end",
                 "death", "frailty", "conds", "regs", "eps", "nchronic", "dis_until", "stays", "slots", "adhd", "past",
                 "readd")

    def __init__(self, pid, fid, rel, sex, dob):
        self.pid, self.fid, self.rel, self.sex, self.dob = pid, fid, rel, sex, dob
        self.code = None
        self.legacy = None
        self.legacy2 = None
        self.member_id = None
        self.start = None     # the current (latest) coverage span
        self.end = None
        self.past = []        # earlier coverage spans, closed: (start, end)
        self.readd = None     # first of the month a dropped dependent is added back
        self.death = None
        self.frailty = 1.0
        self.conds = {}      # condition -> onset date
        self.regs = {}       # regimen key -> [drug, days supply, last fill date allowed or None, next fill date]
        self.eps = []        # active episodes
        self.nchronic = 0
        self.dis_until = None  # an employee off work after a serious illness, at higher risk of leaving
        self.stays = []      # inpatient stays (admission date, discharge date)
        self.slots = {}      # date -> kinds of visit already on that date
        self.adhd = None     # ADHD diagnosis code, when treated

    def covered_on(self, d):
        if self.start is not None and self.start <= d and (self.end is None or d <= self.end):
            return True
        return any(s <= d <= e for s, e in self.past)

    def spans(self):
        """every coverage span in date order, the last one open when end is None"""
        return list(self.past) + ([(self.start, self.end)] if self.start is not None else [])

    def first_start(self):
        return self.past[0][0] if self.past else self.start

    def reinstate(self, d):
        """coverage starts again on d after a gap"""
        self.past.append((self.start, self.end))
        self.start, self.end = d, None

    def age(self, d):
        a = d.year - self.dob.year
        if (d.month, d.day) < (self.dob.month, self.dob.day):
            a -= 1
        return a


class Family:
    __slots__ = ("fid", "emp", "cls", "members", "hist", "root", "active", "cls_hist", "pending", "rehire", "cobra_end",
                 "left")

    def __init__(self, fid, emp, cls):
        self.fid, self.emp, self.cls = fid, emp, cls
        self.members = []
        self.hist = []        # (effective date, plan, coverage tier), in date order
        self.root = None      # Bramwell subscriber number
        self.active = True
        self.cls_hist = []    # (effective date, employee class)
        self.pending = None   # a spouse joining on the first of the next month
        self.rehire = None    # (first day of coverage on return, employee class) for an employee rehired after a gap
        self.cobra_end = None  # last day COBRA continuation can run to
        self.left = []        # members whose coverage ended with the family's last termination


def state_at(fam, d):
    plan, tier = fam.hist[0][1], fam.hist[0][2]
    for eff, pl, ti in fam.hist:
        if eff <= d:
            plan, tier = pl, ti
    return plan, tier


class Sim:
    def __init__(self, seed=W.SEED):
        self.rp = np.random.default_rng(seed)          # population and life events
        self.rh = np.random.default_rng(seed + 11)     # health events
        self.coder = CD.Coder(seed)                    # codes, providers, amounts and payment lags
        self.people = []
        self.fams = []
        self.events = []
        self.emp_used, self.root_used, self.mid_used = set(), set(), set()
        self.cond_years = {}
        self.hx_site = {}
        self.pp_visits = {}
        self.rehires = {}     # first of a month -> families whose employee returns that day
        self.bio_start = {}   # member -> the day the current biologic was started on the plan

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
        """conditions a member already has when coverage begins, at the ages they occur"""
        r = self.rp
        a = p.age(d)
        pr = {
            "diabetes": 0.0 if a < 20 else 0.03 if a < 40 else 0.075 if a < 50 else 0.12,
            "htn": 0.0 if a < 18 else 0.01 if a < 30 else 0.08 if a < 40 else 0.18 if a < 50 else 0.31,
            "lipid": 0.0 if a < 30 else 0.07 if a < 40 else 0.17 if a < 50 else 0.29,
            "asthma": 0.0 if a < 2 else 0.08 if a < 18 else 0.07,
            "depression": 0.0 if a < 12 else 0.09 if a < 18 else 0.115,
            "thyroid": 0.0 if a < 20 else 0.05 if p.sex == "F" else 0.012,
            "esrd": 0.0 if a < 25 else 0.0005 if a < 50 else 0.0012,
            "hiv": 0.0 if a < 20 else 0.0034,
            "autoimmune": 0.0 if a < 6 else 0.005 if a < 18 else 0.026,
            "obesity": 0.0 if a < 20 else 0.33 if a < 40 else 0.41,
            "hemophilia": 0.00006 if p.sex == "M" else 0.0,
            "cf": 0.00008,
            "afib": 0.0 if a < 40 else 0.008 if a < 55 else 0.022,
            "cad": 0.0 if a < 40 else 0.006 if a < 55 else 0.02,
            "liver": 0.0 if a < 30 else 0.0016,
            "hepc": 0.0 if a < 20 else 0.007,
            "urticaria": 0.003 if 18 <= a <= 65 else 0.0,
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
        self.lifestyle_regimens(p, d, a)
        p.nchronic = sum(1 for c in p.conds if c in CHRONIC)

    def lifestyle_regimens(self, p, d, a):
        """prescriptions that are not tied to a costly condition: contraception, attention, reflux, migraine,
        prostate, acne and sleep"""
        r = self.rp
        if p.sex == "F" and 15 <= a <= 44 and r.random() < 0.24:
            self.reg(p, "contra", str(r.choice(["norgestimate_ee", "levonorgestrel_ee", "norethindrone"], p=[0.5, 0.35, 0.15])),
                     28 if r.random() < 0.8 else 84, d)
        if (6 <= a <= 17 and r.random() < 0.075) or (18 <= a <= 35 and r.random() < 0.03):
            p.adhd = "F90.2" if r.random() < 0.6 else "F90.0"
            drug = str(r.choice(["methylphenidate_er_36", "amphet_salts_20", "amphet_salts_er_20", "lisdexamfetamine_30"],
                                p=[0.34, 0.22, 0.22, 0.22]))
            self.reg(p, "adhd", drug, 30, d)
            if a < 18 and r.random() < 0.12:
                self.reg(p, "adhd2", "guanfacine_er_2", 30, d)
        if a >= 25 and r.random() < 0.05:
            self.reg(p, "gerd", str(r.choice(["omeprazole_20", "omeprazole_40", "pantoprazole_40", "famotidine_20"])),
                     90 if r.random() < 0.4 else 30, d)
        if p.sex == "F" and 16 <= a <= 55 and r.random() < 0.05:
            self.reg(p, "migraine", "sumatriptan_50", 45, d)
            if r.random() < 0.3:
                self.reg(p, "migraine2", "topiramate_25", 30, d)
        if p.sex == "M" and a >= 55 and r.random() < 0.12:
            self.reg(p, "bph", "tamsulosin_04", 90 if r.random() < 0.5 else 30, d)
            if r.random() < 0.3:
                self.reg(p, "bph2", "finasteride_5", 90, d)
        if 13 <= a <= 25 and r.random() < 0.05:
            self.reg(p, "acne", "tretinoin_cream", 60, d)
        if a >= 30 and r.random() < 0.025:
            self.reg(p, "sleep", "trazodone_50" if r.random() < 0.7 else "zolpidem_10", 30, d)

    def reg(self, p, key, drug, days, d, until=None):
        first = d + dt.timedelta(days=int(self.rp.integers(0, max(1, min(days, 30)))))
        p.regs[key] = [drug, days, until, first]

    def start_biologic(self, p, drug, d):
        self.reg(p, "biologic", drug, 84 if drug in ("stelara", "skyrizi") else 28, d)
        self.bio_start[p.pid] = p.regs["biologic"][3]
        self.loading(p, drug, p.regs["biologic"][3])

    def loading(self, p, drug, first):
        """the starter dose of a biologic: one extra fill dispensed with the first"""
        when = first + dt.timedelta(days=14)
        p.regs["loading"] = [drug, 28, when, when]

    def start_regimen(self, p, c, d, new=False):
        r = self.rp
        a = p.age(d)
        days90 = r.random() < 0.38
        dd = 90 if days90 else 30
        if c == "diabetes":
            self.reg(p, "metformin", str(r.choice(["metformin_500", "metformin_1000", "metformin_er_500", "metformin_er_750"],
                                                  p=[0.4, 0.25, 0.22, 0.13])), dd, d)
            u = r.random()
            if u < 0.42:
                self.reg(p, "glp1", str(r.choice(["ozempic_05", "ozempic_1", "ozempic_2", "mounjaro_5", "mounjaro_10",
                                                  "trulicity_15"], p=[0.2, 0.22, 0.14, 0.18, 0.14, 0.12])), 28, d)
            elif u < 0.55:
                self.reg(p, "insulin", "lantus" if r.random() < 0.6 else "basaglar", 30, d)
            if r.random() < 0.14:
                self.reg(p, "sglt2", "jardiance" if r.random() < 0.6 else "farxiga", 30, d)
            if r.random() < 0.08:
                self.reg(p, "su", "glipizide_5", dd, d)
        elif c == "htn":
            self.reg(p, "htn", str(r.choice(["lisinopril_10", "lisinopril_20", "lisinopril_40", "amlodipine_5", "amlodipine_10",
                                             "losartan_50", "losartan_100", "lisinopril_hctz", "losartan_hctz", "hctz_25"],
                                            p=[0.16, 0.12, 0.05, 0.15, 0.07, 0.15, 0.08, 0.08, 0.06, 0.08])), dd, d)
            if r.random() < 0.25:
                self.reg(p, "htn2", str(r.choice(["amlodipine_5", "hctz_25", "metoprolol_er_25"])), dd, d)
        elif c in ("lipid", "cad"):
            self.reg(p, "lipid", str(r.choice(["atorvastatin_10", "atorvastatin_20", "atorvastatin_40", "atorvastatin_80",
                                               "rosuvastatin_10", "rosuvastatin_20", "simvastatin_20", "pravastatin_40"],
                                              p=[0.14, 0.2, 0.18, 0.06, 0.14, 0.1, 0.1, 0.08])), dd, d)
            if c == "cad":
                self.reg(p, "bb", "metoprolol_er_25" if r.random() < 0.6 else "metoprolol_er_50", dd, d)
        elif c == "asthma":
            self.reg(p, "albuterol", "albuterol", 75, d)
            if r.random() < 0.35:
                self.reg(p, "montelukast", "montelukast_10" if a >= 15 else "montelukast_5" if a >= 6 else "montelukast_4", 30, d)
            if a >= 12 and r.random() < 0.05:
                self.reg(p, "dupixent", "dupixent", 28, d)
            elif r.random() < 0.18:
                ctl = "fluticasone_hfa" if a < 18 else str(r.choice(["fluticasone_hfa", "budesonide_formoterol", "trelegy", "breo"],
                                                                     p=[0.3, 0.35, 0.15, 0.2]))
                self.reg(p, "inhaler", ctl, 30, d)
        elif c == "depression":
            if r.random() < 0.7:
                opts = ["sertraline_50", "escitalopram_10", "fluoxetine_20"] if a < 18 else \
                    ["sertraline_50", "sertraline_100", "escitalopram_10", "escitalopram_20", "fluoxetine_20", "bupropion_xl_150",
                     "bupropion_xl_300", "citalopram_20", "venlafaxine_er_75", "duloxetine_60"]
                self.reg(p, "ssri", str(r.choice(opts)), dd, d)
                if a >= 18 and r.random() < 0.15:
                    self.reg(p, "anx", "buspirone_10" if r.random() < 0.6 else "trazodone_50", 30, d)
        elif c == "thyroid":
            self.reg(p, "thyroid", str(r.choice(["levothyroxine_50", "levothyroxine_75", "levothyroxine_100", "levothyroxine_125"],
                                                p=[0.32, 0.28, 0.24, 0.16])), dd, d)
        elif c == "hiv":
            self.reg(p, "art", "biktarvy", 30, d)
        elif c == "autoimmune":
            code, wt, drugs, infl = CD.autoimmune_type(p.pid)
            u = r.random()
            if u < 0.5:
                drug = str(r.choice(list(drugs)))
                if drug == "humira" and r.random() < 0.35:
                    drug = "hyrimoz"
                if new:
                    self.start_biologic(p, drug, d)
                else:
                    self.reg(p, "biologic", drug, 84 if drug in ("stelara", "skyrizi") else 28, d)
            elif u < 0.57 and infl:
                p.regs["infusion"] = ["infliximab", 56, None, d]
            if code.startswith("M0") and r.random() < 0.55:
                self.reg(p, "mtx", "methotrexate", 28, d)
                self.reg(p, "folic", "folic_acid", 90, d)
                if r.random() < 0.3:
                    self.reg(p, "hcq", "hydroxychloroquine", 30, d)
        elif c == "hemophilia":
            self.reg(p, "factor", "hemlibra", 28, d)
        elif c == "cf":
            self.reg(p, "cftr", "trikafta", 28, d)
        elif c == "afib":
            self.reg(p, "anticoag", "eliquis" if r.random() < 0.75 else "xarelto", 30, d)
            if r.random() < 0.6:
                self.reg(p, "rate", "metoprolol_er_50" if r.random() < 0.7 else "diltiazem_er_180", dd, d)
        elif c == "copd":
            self.reg(p, "albuterol", "albuterol", 75, d)
            if r.random() < 0.7:
                self.reg(p, "inhaler", str(r.choice(["trelegy", "breo", "spiriva"], p=[0.5, 0.3, 0.2])), 30, d)
        elif c == "chf":
            if r.random() < 0.55:
                self.reg(p, "arni", "entresto", 30, d)
            else:
                self.reg(p, "htn", "losartan_50", 30, d)
            if r.random() < 0.6:
                self.reg(p, "bb", "carvedilol_12", 30, d)
            if r.random() < 0.7:
                self.reg(p, "diuretic", "furosemide_40", 30, d)
            if r.random() < 0.35:
                self.reg(p, "mra", "spironolactone_25", 30, d)
            if r.random() < 0.3:
                self.reg(p, "sglt2", "jardiance" if r.random() < 0.6 else "farxiga", 30, d)
        elif c in ("kidney_tx", "liver_tx"):
            self.reg(p, "tac", "tacrolimus", 30, d)
            self.reg(p, "mmf", "mycophenolate", 30, d)
            self.reg(p, "pred", "prednisone_5", 30, d)
        elif c == "esrd":
            if r.random() < 0.7:
                self.reg(p, "binder", "sevelamer", 30, d)
            if r.random() < 0.4:
                self.reg(p, "vitd", "calcitriol", 30, d)
        elif c == "urticaria":
            if r.random() < 0.45:
                self.reg(p, "xolair", "xolair", 28, d)
        elif c == "liver":
            if r.random() < 0.5:
                self.reg(p, "lactulose", "lactulose", 30, d)
            if r.random() < 0.35:
                self.reg(p, "rifaximin", "xifaxan", 30, d)
            if r.random() < 0.4:
                self.reg(p, "mra", "spironolactone_25", 30, d)

    # ---------------------------------------------------------------- the calendar of care
    def pick_day(self, p, d0, d1, profile, kind=None):
        """one day in [d0, d1] weighted by the day of the week and the holiday calendar, never inside one of the
        member's hospital stays, and never a second visit of the same kind on one day; None when no day is open"""
        r = self.rh
        wd, closed, reduced = PROFILES[profile]
        days, wts = [], []
        d = d0
        while d <= d1:
            w = wd[d.weekday()]
            if d in W.CLINIC_CLOSED:
                w = w * closed if profile == "any" else min(w, closed)
            elif d in W.CLINIC_REDUCED:
                w *= reduced
            if w > 0 and kind in NO_TWICE and any(x in p.slots.get(d, ()) for x in slots_of(kind)):
                w = 0.0
            if w > 0 and kind not in STAY_KINDS and kind != "ambulance" and self.in_stay(p, d):
                w = 0.0
            if w > 0:
                days.append(d)
                wts.append(w)
            d += DAY
        u = r.random()
        if not days:
            return None
        u *= sum(wts)
        acc = 0.0
        for d, w in zip(days, wts):
            acc += w
            if u < acc:
                return d
        return days[-1]

    def in_stay(self, p, d):
        return any(s <= d < e or s == d for s, e in p.stays[-6:])

    def stay_free(self, p, s, e):
        """no stay of the member's overlaps [s, e); a discharge and an admission on the same day do not overlap"""
        return all(not (s < b and a < e) and a != s for a, b in p.stays[-8:])

    # ---------------------------------------------------------------- recording an event
    def add(self, p, d0, d1, ben, kind, amount, info=None, parts=None):
        """one service event, coded and priced into its claim components"""
        if ben == "R" and amount <= 0:
            return False
        if parts is None:
            parts = [("P", "clinic", 1.0)]
        if kind in NO_TWICE and any(x in p.slots.get(d0, ()) for x in slots_of(kind)):
            return False
        if kind in STAY_KINDS:
            if not self.stay_free(p, d0, max(d1, d0 + DAY)):
                return False
            p.stays.append((d0, max(d1, d0 + DAY)))
        yrs = (d0 - dt.date(2025, 7, 1)).days / 365.25
        amt = amount * (W.TREND_MED ** yrs if ben == "M" else W.TREND_RX ** yrs)
        comps = self.coder.components(p, d0, d1, ben, kind, amt, info or {}, parts)
        if kind in NO_TWICE:
            p.slots.setdefault(d0, set()).update(slots_of(kind))
        self.events.append((p.pid, d0, d1, ben, kind, comps, info))
        return True

    def fill(self, p, d, drug, days=None):
        """one prescription filled, priced per fill or per 30 days of supply"""
        if not p.covered_on(d) or self.in_stay(p, d):
            return False
        r = self.rh
        name, q30, price, bg, spec, per_fill = K.drug(drug)
        ds = days or 30
        if per_fill or bg == "B":
            amt, q = price * r.lognormal(0, 0.02), q30
        else:
            amt, q = price * ds / 30.0 * r.lognormal(0, 0.05), round(q30 * ds / 30.0)
        return self.add(p, d, d, "R", "fill", amt, {"drug": drug, "qty": q, "days": ds}, [("R", "pharmacy", 1.0)])

    def rx_day(self, d):
        """the day a prescription is picked up: on the day it is due or within a few days, busiest on Mondays and
        Fridays, quieter on Saturdays, quietest on Sundays and holidays"""
        r = self.rh
        days = [d + dt.timedelta(days=k) for k in range(5)]
        wts = []
        for k, x in enumerate(days):
            dow = (1.12, 1.0, 0.98, 0.98, 1.08, 0.82, 0.42)[x.weekday()]
            if x in W.CLINIC_CLOSED:
                dow = 0.12
            wts.append((0.46, 0.24, 0.14, 0.09, 0.07)[k] * dow)
        u = r.random() * sum(wts)
        acc = 0.0
        for x, w in zip(days, wts):
            acc += w
            if u < acc:
                return x
        return days[-1]

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
        for fam in self.rehires.pop(ms, ()):
            self.return_to_work(fam, ms)
        for fam in list(self.fams):
            if fam.active:
                self.life(fam, ms, me)
        n_cov = sum(1 for p in self.people if p.covered_on(ms))
        gap = 5905 + 3.0 * max(0, m - 12) - n_cov
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
            if len(p.slots) > 40:
                for d in sorted(p.slots)[:-20]:
                    del p.slots[d]

    # ---------------------------------------------------------------- life events
    def life(self, fam, ms, me):
        r = self.rp
        sub = self.people[fam.members[0]]
        if fam.pending is not None:
            sex, sdob = fam.pending
            fam.pending = None
            if sub.end is None:
                self.add_person(fam, "S", sex, sdob, ms)
                self.set_tier(fam, ms)
        mem = [self.people[i] for i in fam.members if self.people[i].end is None]
        if not mem or sub.end is not None:
            fam.active = False
            for p in mem:
                p.end = me
            return
        # a dependent dropped at an earlier open enrolment comes back on a special enrolment
        for i in fam.members:
            p = self.people[i]
            if p.readd == ms:
                p.readd = None
                if p.end is not None and p.death is None and (p.rel != "C" or p.age(ms) < 26):
                    p.reinstate(ms)
                    p.eps = []
        mem = [self.people[i] for i in fam.members if self.people[i].end is None]
        a = sub.age(ms)
        if fam.cls == "C":
            # COBRA continuation: up to 18 months, most members leave it early for another employer's plan
            start, last = fam.cobra_end
            if ms >= start and (me >= last or r.random() < 0.065):
                self.end_family(fam, me)
                return
        elif fam.cls == "R":
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
                    self.leave(fam, end, ms)
                    if not fam.active:
                        return
        for p in mem:
            if p.rel == "C" and p.age(me) >= 26:
                p.end = me
        if ms.month == 7 and fam.cls != "C":
            # open enrolment: an adult child or a spouse with coverage of their own comes off the plan on 30 June
            for p in mem:
                if p.end is not None or p.rel == "E":
                    continue
                q = 0.035 if (p.rel == "C" and 19 <= p.age(ms) <= 25) else 0.015 if p.rel == "S" else 0.0
                if q and r.random() < q:
                    p.end = ms - DAY
                    if r.random() < (0.3 if p.rel == "C" else 0.25):
                        p.readd = W.add_months(ms, int(r.integers(3, 19)))
        self.set_tier(fam, ms)
        plan, tier = state_at(fam, ms)
        if tier in ("EE", "EC") and 24 <= a <= 52 and r.random() < 0.0011 and fam.pending is None and fam.cls != "C":
            # a marriage: the spouse is covered from the first of the following month
            sa = int(min(60, max(22, a + r.normal(0, 4))))
            nxt = W.add_months(ms, 1)
            fam.pending = ("M" if sub.sex == "F" else "F", nxt - dt.timedelta(days=int(sa * 365.25 + r.integers(0, 365))))
        if ms.month == 7 and r.random() < 0.045:
            self.change(fam, ms, plan="PPO" if plan == "HDHP" else "HDHP")

    def tier_on(self, fam, d):
        mem = [self.people[i] for i in fam.members]
        mem = [p for p in mem if p.covered_on(d)]
        has_sp = any(p.rel == "S" for p in mem)
        has_ch = any(p.rel == "C" for p in mem)
        return "FAM" if has_sp and has_ch else "ES" if has_sp else "EC" if has_ch else "EE"

    def change(self, fam, d, plan=None):
        """record a plan or tier change effective d, keeping the history in date order and every later entry's tier
        true to the members covered on its date"""
        cur_plan, cur_tier = state_at(fam, d)
        new = (d, plan or cur_plan, self.tier_on(fam, d))
        if new[1:] == (cur_plan, cur_tier):
            return
        i = bisect.bisect_right([e[0] for e in fam.hist], d)
        fam.hist.insert(i, new)
        for j in range(i + 1, len(fam.hist)):
            eff, pl, _ = fam.hist[j]
            fam.hist[j] = (eff, pl, self.tier_on(fam, eff))

    def set_tier(self, fam, d):
        if self.tier_on(fam, d) != state_at(fam, d)[1]:
            self.change(fam, d)

    def end_family(self, fam, end):
        fam.left = []
        for i in fam.members:
            p = self.people[i]
            p.readd = None
            if p.end is None:
                p.end = end
                fam.left.append(p.pid)
        fam.active = False

    def leave(self, fam, end, ms):
        """an employee leaves the District: coverage ends on `end`, or continues under COBRA, and a few come back to
        work after a gap"""
        r = self.rp
        mem = [self.people[i] for i in fam.members if self.people[i].end is None]
        costly = any(c in p.conds for p in mem for c in ("esrd", "hiv", "autoimmune", "cf", "hemophilia", "liver", "chf",
                                                           "kidney_tx", "liver_tx")) or \
            any(e["kind"] in ("cancer", "preg", "transplant", "nicu", "hepc") for p in mem for e in p.eps)
        if r.random() < (0.45 if costly else 0.07):
            start = end + DAY
            fam.cls = "C"
            fam.cls_hist.append((start, "C"))
            fam.cobra_end = (start, W.add_months(start, 18) - DAY)
            return
        cls = fam.cls
        self.end_family(fam, end)
        if r.random() < {"S": 0.10, "T": 0.06, "A": 0.03}.get(cls, 0.0):
            back = end + DAY
            if cls == "T" and r.random() < 0.5:
                k = 12                                  # a year's leave, back for the next school year
            else:
                k = int(r.integers(2, 8)) if cls == "S" else int(r.integers(3, 10))
            when = W.add_months(back, k)
            fam.rehire = (when, cls)
            self.rehires.setdefault(when, []).append(fam)

    def return_to_work(self, fam, d):
        """a rehired employee's coverage starts again on the first of the month, with the dependents still eligible"""
        when, cls = fam.rehire
        fam.rehire = None
        sub = self.people[fam.members[0]]
        if sub.death is not None or sub.pid not in fam.left:
            return
        for pid in fam.left:
            p = self.people[pid]
            if p.death is None and (p.rel != "C" or p.age(d) < 26):
                p.reinstate(d)
                p.eps = []
        fam.left = []
        fam.active = True
        fam.cls = cls
        fam.cls_hist.append((d, cls))
        self.change(fam, d, plan=state_at(fam, d)[0])

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

    # ---------------------------------------------------------------- diagnoses
    def acute_dx(self, p, a, d, lst=None):
        r = self.rh
        opts = CD.gated(lst or K.ACUTE, a, p.sex)
        winter = d.month in (11, 12, 1, 2, 3)
        summer = d.month in (6, 7, 8)
        items = []
        for code, w, *_ in opts:
            if code.startswith(RESP):
                w *= 1.5 if winter else 0.65 if summer else 1.0
            elif code == "J10.1":
                w *= 3.0 if d.month in (12, 1, 2) else 1.2 if d.month in (11, 3) else 0.05
            elif code.startswith("J30"):
                w *= 2.2 if d.month in (4, 5, 6, 8, 9) else 0.5
            elif code.startswith("S"):
                w *= 1.3 if 5 <= d.month <= 9 else 0.85
            items.append((code, w))
        return CD.wpick(items, r.random())

    def visit_dx(self, p, a, d):
        r = self.rh
        if (d - p.dob).days < 29:
            return CD.wpick(K.NEWBORN_VISIT, r.random())
        cs = [c for c in sorted(p.conds) if c in K.COND_CODES or c == "autoimmune"]
        if p.adhd:
            cs.append("_adhd")
        if cs and r.random() < 0.55:
            c = cs[int(r.integers(0, len(cs)))]
            if c == "_adhd":
                return p.adhd
            if c == "autoimmune":
                return CD.autoimmune_type(p.pid)[0]
            return CD.cond_code(p.pid, c)
        return self.acute_dx(p, a, d)

    def acute_rx(self, p, a, d, dx):
        """the prescription a visit for an acute problem is written for, when one is"""
        r = self.rh
        kid = a < 12
        u = r.random()
        drug = None
        if dx == "J02.0":
            drug = ("amoxicillin_susp" if kid else "amoxicillin_500") if u < 0.8 else "azithromycin_susp" if kid else "azithromycin_250"
        elif dx in ("J02.9", "J03.90") and u < 0.35:
            drug = "amoxicillin_susp" if kid else "amoxicillin_500"
        elif dx == "J01.90" and u < 0.62:
            if r.random() < 0.6:
                drug = "amox_clav_susp" if kid else "amox_clav_875"
            else:
                drug = "azithromycin_susp" if kid else "doxycycline_100" if a >= 18 and r.random() < 0.5 else "azithromycin_250"
        elif dx.startswith("H66") and u < 0.82:
            if kid:
                drug = "amoxicillin_susp" if r.random() < 0.75 else "amox_clav_susp" if r.random() < 0.6 else "cefdinir_susp"
            else:
                drug = "amoxicillin_875"
        elif dx == "J20.9" and u < 0.55:
            drug = "azithromycin_250" if (a >= 12 and r.random() < 0.5) else "benzonatate_100" if a >= 10 else "azithromycin_susp"
        elif dx in ("R05.9", "J06.9") and a >= 10 and u < 0.14:
            drug = "benzonatate_100" if r.random() < 0.6 else "azithromycin_250"
        elif dx == "J10.1" and u < 0.55:
            drug = "oseltamivir_75" if a >= 13 else "oseltamivir_susp"
        elif dx in ("N39.0", "R30.0") and u < 0.85:
            drug = (str(r.choice(["nitrofurantoin_100", "smx_tmp_ds", "ciprofloxacin_500", "cephalexin_500"], p=[0.5, 0.3, 0.1, 0.1]))
                    if a >= 16 else "cefdinir_susp")
        elif dx in ("L03.115", "L03.116") and u < 0.9:
            drug = "cephalexin_500" if r.random() < 0.65 else "smx_tmp_ds"
        elif dx == "L01.00" and u < 0.8:
            drug = "mupirocin"
        elif dx in ("L30.9", "L20.9", "R21", "L20.83") and u < 0.45:
            drug = "triamcinolone_cream"
        elif dx == "L70.0" and u < 0.4:
            drug = "tretinoin_cream" if r.random() < 0.6 else "doxycycline_100"
        elif dx.startswith("H10") and u < 0.7:
            drug = "polytrim_ophth"
        elif dx == "H60.331" and u < 0.8:
            drug = "ofloxacin_otic"
        elif dx in ("M54.50", "M54.2", "M54.41", "M54.42", "M54.16", "S39.012A", "S16.1XXA", "M62.830") and u < 0.6 and a >= 16:
            drug = str(r.choice(["cyclobenzaprine_10", "ibuprofen_800", "naproxen_500", "meloxicam_15", "methylpred_4", "tramadol_50"],
                                p=[0.36, 0.2, 0.14, 0.14, 0.11, 0.05]))
        elif dx.startswith(("S93", "S63", "M25.5", "M77", "M72", "M75")) and u < 0.45 and a >= 12:
            drug = str(r.choice(["ibuprofen_800", "naproxen_500", "meloxicam_15"]))
        elif dx == "G43.909" and u < 0.5:
            drug = "sumatriptan_50"
        elif dx in ("A08.4", "R11.2", "R11.10") and u < 0.5:
            drug = "ondansetron_odt"
        elif dx in ("J30.9", "J30.2") and u < 0.6:
            drug = "fluticasone_nasal"
        elif dx in ("B37.31", "N76.0") and u < 0.85:
            drug = "fluconazole_150" if r.random() < 0.65 else "metronidazole_500"
        elif dx in ("F41.9", "F41.0", "F43.23") and u < 0.25 and a >= 18:
            drug = "hydroxyzine_25"
        elif dx == "G47.00" and u < 0.4:
            drug = "trazodone_50" if r.random() < 0.7 else "zolpidem_10"
        elif dx == "B02.9" and u < 0.85:
            drug = "valacyclovir_1g"
        elif dx == "J18.9" and u < 0.9:
            drug = "amoxicillin_susp" if kid else ("amoxicillin_875" if r.random() < 0.5 else "azithromycin_250")
        elif dx.startswith("J45") and dx.endswith("1") and u < 0.7:
            drug = "prednisolone_soln" if kid else "prednisone_20"
        elif dx == "J05.0" and u < 0.4:
            drug = "prednisolone_soln"
        elif dx == "T78.40XA" and u < 0.3:
            drug = "methylpred_4"
        elif dx == "F17.210" and u < 0.2:
            drug = "varenicline"
        elif dx == "U07.1" and a >= 18 and (a >= 50 or p.nchronic) and u < 0.45:
            drug = "paxlovid"
        elif dx == "K21.9" and u < 0.4 and a >= 12:
            drug = "omeprazole_20" if r.random() < 0.6 else "famotidine_20"
        if drug:
            fd = d if r.random() < 0.72 else d + DAY
            self.fill(p, self.rx_day(fd), drug)

    # ---------------------------------------------------------------- health
    def health(self, p, ms, me):
        d0 = max(ms, p.start)
        d1 = me if p.end is None else min(me, p.end)
        if d1 < d0:
            return
        span = (d1 - d0).days + 1
        frac = span / ((me - ms).days + 1)
        a = p.age(d0)
        if self.mortality(p, a, d0, d1, frac):
            return
        self.episodes(p, d0, d1, frac)
        self.incidence(p, a, d0, d1, frac)
        self.chronic(p, a, d0, d1, frac)
        self.routine(p, a, d0, d1, frac, ms)
        self.pharmacy(p, a, d0, d1)
        ys = self.cond_years.setdefault((p.pid, d0.year), set())
        ys.update(c for c in p.conds if c in CHRONIC)
        if any(e["kind"] == "cancer" for e in p.eps):
            ys.add("cancer")

    def visit(self, p, d0, d1, kind, profile, dx=None, spec=None, rx=True, extra=None):
        dd = self.pick_day(p, d0, d1, profile, kind)
        if dd is None:
            return None
        a = p.age(dd)
        dx = dx or self.visit_dx(p, a, dd)
        info = {"dx": dx}
        if spec:
            info["spec"] = spec
        if extra:
            info.update(extra)
        if self.add(p, dd, dd, "M", kind, 1.0, info, [("P", "clinic", 1.0)]) and rx and not dx.startswith("Z"):
            self.acute_rx(p, a, dd, dx)
        return dd

    def routine(self, p, a, d0, d1, frac, ms):
        r = self.rh
        f = p.frailty
        nc = p.nchronic
        if a < 2:
            lam = 0.24
        elif a < 18:
            lam = 0.15
        elif a < 40:
            lam = 0.17 if p.sex == "M" else 0.25
        else:
            lam = 0.24 if p.sex == "M" else 0.30
        for _ in range(r.poisson(1.12 * lam * f * (1 + 0.32 * nc) * frac)):
            spec = r.random() < (0.36 + 0.05 * nc if a >= 2 else 0.08)
            self.visit(p, d0, d1, "office_spec" if spec else "office", "clinic")
        # preventive care: the infant schedule, then once a year in the birthday month
        if a < 2:
            months = (d0.year - p.dob.year) * 12 + d0.month - p.dob.month
            if months in (0, 1, 2, 4, 6, 9, 12, 15, 18) and r.random() < 0.9:
                lo = max(d0, p.dob + dt.timedelta(days=3 if months == 0 else 0))
                if lo <= d1:
                    self.visit(p, lo, d1, "preventive", "clinic", dx="Z00.129", rx=False)
        elif p.dob.month == ms.month and p.covered_on(ms) and r.random() < (0.86 if a < 18 else 0.6):
            self.visit(p, d0, d1, "preventive", "clinic", dx="Z00.00", rx=False)
        if p.sex == "F" and a >= 40 and (p.dob.month + 4) % 12 + 1 == ms.month and r.random() < 0.55:
            dd = self.pick_day(p, d0, d1, "imaging", "img_xray")
            if dd:
                self.add(p, dd, dd, "M", "img_xray", 1.0, {"code": "77067", "dx": "Z12.31"}, [("I", "hospital", 1.0)])
        for _ in range(r.poisson(0.11 * f * (1 + 0.65 * nc) * frac * (0.25 if a < 2 else 1.0))):
            dd = self.pick_day(p, d0, d1, "lab", "lab")
            if dd:
                self.add(p, dd, dd, "M", "lab", 1.0, {}, [("P", "lab", 1.0)])
        kid_f = 0.35 if a < 2 else 0.6 if a < 18 else 1.0
        for _ in range(r.poisson(0.027 * f * (1 + 0.3 * nc) * frac * kid_f)):
            kind = str(r.choice(["xray", "ct", "mri", "us"], p=[0.5, 0.18, 0.17, 0.15]))
            dd = self.pick_day(p, d0, d1, "imaging", "img_" + kind)
            if dd:
                self.add(p, dd, dd, "M", "img_" + kind, 1.0, {}, [("I", "hospital", 1.0)])
        lam_er = (0.026 if a < 5 else 0.013 if a < 18 else 0.016) * math.sqrt(f) * (1 + 0.25 * nc) * frac
        for _ in range(r.poisson(lam_er)):
            dd = self.pick_day(p, d0, d1, "any", "er")
            if dd:
                dx = self.acute_dx(p, p.age(dd), dd, K.ER)
                if self.add(p, dd, dd, "M", "er", r.lognormal(math.log(2880), 0.5), {"dx": dx},
                            [("I", "hospital", 0.78), ("P", "emergency", 0.22)]):
                    self.acute_rx(p, p.age(dd), dd, dx)
        for _ in range(r.poisson(0.028 * f * frac)):
            dd = self.pick_day(p, d0, d1, "urgent", "urgent")
            if dd:
                dx = self.acute_dx(p, p.age(dd), dd)
                if self.add(p, dd, dd, "M", "urgent", 1.0, {"dx": dx}, [("P", "urgent", 1.0)]):
                    self.acute_rx(p, p.age(dd), dd, dx)
        lam_op = (0.0 if a < 1 else 0.0037 if a < 30 else 0.0088 if a < 50 else 0.0155) * f * frac
        for _ in range(r.poisson(lam_op)):
            dd = self.pick_day(p, d0, d1, "elective", "op_surgery")
            if dd and self.add(p, dd, dd, "M", "op_surgery", 1.0, {}, [("I", "asc", 1.0)]) and r.random() < 0.3 and a >= 12:
                self.fill(p, self.rx_day(dd), "hydrocodone_apap" if r.random() < 0.6 else "ibuprofen_800")
        lam_ip = (0.0014 if a < 18 else 0.0022 if a < 45 else 0.0039) * math.sqrt(f) * (1 + 0.4 * nc) * frac
        for _ in range(r.poisson(lam_ip)):
            dd = self.pick_day(p, d0, d1, "any", "admit")
            if dd:
                self.admission(p, dd, r.lognormal(math.log(25500), 0.55), self.admit_dx(p, p.age(dd)))
        # hospital outpatient services: cardiac testing, sleep studies, wound care, infusion chairs
        for _ in range(r.poisson(0.021 * f * (1 + 0.45 * nc) * frac * (0.1 if a < 2 else 0.35 if a < 18 else 1.0))):
            dd = self.pick_day(p, d0, d1, "elective", "op_hospital")
            if dd:
                self.add(p, dd, dd, "M", "op_hospital", 1.0, {}, [("I", "hospital", 1.0)])
        if a >= 12 and r.random() < 0.0055 * frac:
            dx = self.acute_dx(p, a, d0, [x for x in K.ACUTE if x[0].startswith(("M", "S"))])
            self.course(p, ms, "pt", int(r.integers(6, 12)), 2, dx)
        if "depression" in p.conds and r.random() < 0.06 * frac:
            self.course(p, ms, "therapy", int(r.integers(5, 16)), int(r.integers(2, 6)), CD.cond_code(p.pid, "depression"))

    def admit_dx(self, p, a):
        r = self.rh
        own = [c for c in sorted(p.conds) if c in K.ADMIT_COND]
        if own and r.random() < 0.3:
            c = own[int(r.integers(0, len(own)))]
            if c == "asthma":
                return "J45.21" if a < 18 else "J45.901"
            if c == "liver":
                return CD.cond_code(p.pid, "liver")
            return K.ADMIT_COND[c]
        if a < 1:
            return CD.wpick(K.ADMIT_INFANT, r.random())
        lst = K.ADMIT_CHILD if a < 18 else K.ADMIT_ADULT
        return CD.wpick([(x[0], x[1]) for x in CD.gated(lst, a, p.sex)], r.random())

    def admission(self, p, d, amount, dx, los=None, icu=False, kind="admit", followup=True, dx2=None):
        r = self.rh
        if los is None:
            los = int(max(1, min(14, round(r.lognormal(math.log(3.2), 0.5)))))
        d1 = d + dt.timedelta(days=los)
        if p.end is not None and d1 > p.end:
            d1 = max(d, p.end)
        info = {"dx": dx, "los": (d1 - d).days, "icu": icu}
        if dx2:
            info["dx2"] = dx2
        if "er" in p.slots.get(d, ()):
            info["no_ed"] = True
        if not self.add(p, d, d1, "M", kind, amount, info,
                        [("I", "hospital", 0.84), ("P", "hospitalist", 0.12), ("P", "hospitalist", 0.04)]):
            return False
        if dx == "I26.99":
            self.reg(p, "anticoag_pe", "eliquis", 30, d1 + DAY, until=d1 + dt.timedelta(days=180))
        if followup and amount > 20000:
            big = amount > 45000 or kind != "admit"
            p.eps.append({"kind": "postacute", "m": 0, "start": d1, "big": big, "dx": dx,
                          "irf": big and kind in ("admit_trauma", "admit_cardiac") and r.random() < 0.5})
            if r.random() < 0.55:
                drug = str(r.choice(["eliquis", "enoxaparin", "ondansetron", "cephalexin_500", "oxycodone_5"],
                                    p=[0.3, 0.2, 0.15, 0.15, 0.2]))
                n = int(r.integers(1, 4)) if drug == "eliquis" else 1
                self.reg(p, "discharge", drug, 30 if drug in ("eliquis", "ondansetron") else 10, d1 + DAY,
                         until=d1 + dt.timedelta(days=30 * n))
            if amount > 45000 and p.rel == "E":
                p.dis_until = d1 + dt.timedelta(days=420)
        return True

    def course(self, p, ms, kind, n, per_month, dx):
        k, mo = 0, 0
        while k < n and mo < 14:
            mstart = W.add_months(ms, mo)
            mend = W.month_end(W.month_index(mstart))
            lo = max(mstart, p.start)
            hi = mend if p.end is None else min(mend, p.end)
            if hi < lo or lo > W.SIM_END:
                return
            for _ in range(per_month):
                if k >= n:
                    break
                dd = self.pick_day(p, lo, hi, "therapy", kind)
                if dd is None:
                    continue
                self.add(p, dd, dd, "M", kind, 1.0, {"dx": dx, "first": k == 0}, [("P", kind, 1.0)])
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
        if any(s <= dd and e > dd for s, e in p.stays[-6:]):
            return False
        if q_m > 0.004 and r.random() < 0.7:
            st = max(d0, dd - dt.timedelta(days=int(r.integers(2, 12))))
            if self.stay_free(p, st, dd + DAY):
                self.add(p, st, dd, "M", "admit", r.lognormal(math.log(46000), 0.5),
                         {"dx": self.ep_dx(p) if p.eps else self.admit_dx(p, a), "los": (dd - st).days, "icu": True},
                         [("I", "hospital", 0.85), ("P", "hospitalist", 0.15)])
        self.die(p, dd)
        return True

    def ep_dx(self, p):
        for e in p.eps:
            if e["kind"] == "cancer":
                return e["code"]
        for e in p.eps:
            dx = e.get("dx", "")
            if dx and not dx.startswith(("Z", "O", "P")) and not dx.endswith("D"):
                return dx
        return "A41.9"

    # ---------------------------------------------------------------- chronic care
    def chronic(self, p, a, d0, d1, frac):
        r = self.rh
        c = p.conds
        if r.random() < 0.33 * frac and any(k in c for k in ("diabetes", "htn", "lipid", "thyroid", "afib", "cad", "hiv", "autoimmune")):
            sp = "hiv" in c or "autoimmune" in c
            key = "hiv" if "hiv" in c else "autoimmune" if "autoimmune" in c else \
                [k for k in ("diabetes", "htn", "lipid", "thyroid", "afib", "cad") if k in c][0]
            dx = CD.autoimmune_type(p.pid)[0] if key == "autoimmune" else CD.cond_code(p.pid, key)
            dd = self.visit(p, d0, d1, "office_spec" if sp else "office", "clinic", dx=dx, rx=False)
            if dd:
                self.add(p, dd, dd, "M", "lab", 1.0, {}, [("P", "lab", 1.0)])
        listed = any(e["kind"] == "transplant" for e in p.eps)
        if "esrd" in c:
            sessions = max(1, int(round(13 * frac)))
            self.add(p, d0, d1, "M", "dialysis", 1075.0 * sessions * r.lognormal(0, 0.05), {"dx": "N18.6", "sessions": sessions},
                     [("I", "dialysis", 0.96), ("P", "nephro", 0.04)])
            if r.random() < 0.045 * frac:
                dd = self.pick_day(p, d0, d1, "any", "admit")
                if dd:
                    self.admission(p, dd, r.lognormal(math.log(36000), 0.45), "N18.6", dx2="Z99.2")
            if a < 66 and not listed and r.random() < 0.0045 * frac:
                p.eps.append({"kind": "transplant", "organ": "kidney", "m": 0, "start": d1})
        if "liver" in c:
            code = CD.cond_code(p.pid, "liver")
            if r.random() < 0.35 * frac:
                self.visit(p, d0, d1, "office_spec", "clinic", dx=code, spec="gastro", rx=False)
            if r.random() < 0.028 * frac:
                dd = self.pick_day(p, d0, d1, "any", "admit")
                if dd:
                    self.admission(p, dd, r.lognormal(math.log(31000), 0.5), code)
            if a < 66 and not listed and r.random() < 0.0065 * frac:
                p.eps.append({"kind": "transplant", "organ": "liver", "m": 0, "start": d1})
        for k_, spec in (("chf", "cardiology"), ("copd", "pulm")):
            if k_ in c:
                code = CD.cond_code(p.pid, k_)
                for _ in range(r.poisson(0.9 * frac)):
                    self.visit(p, d0, d1, "office_spec", "clinic", dx=code, spec=spec, rx=False)
                if r.random() < 0.05 * frac:
                    dd = self.pick_day(p, d0, d1, "any", "er")
                    if dd:
                        self.add(p, dd, dd, "M", "er", r.lognormal(math.log(3100), 0.4), {"dx": "I50.23" if k_ == "chf" else "J44.1"},
                                 [("I", "hospital", 0.78), ("P", "emergency", 0.22)])
                if r.random() < 0.038 * frac:
                    dd = self.pick_day(p, d0, d1, "any", "admit")
                    if dd:
                        self.admission(p, dd, r.lognormal(math.log(27000), 0.45), "I50.23" if k_ == "chf" else "J44.1")
                if r.random() < 0.12 * frac:
                    dd = self.pick_day(p, d0, d1, "elective", "op_hospital")
                    if dd:
                        self.add(p, dd, dd, "M", "op_hospital", 1.0, {"cond": k_}, [("I", "hospital", 1.0)])
        if "hemophilia" in c:
            if r.random() < 0.25 * frac:
                self.visit(p, d0, d1, "office_spec", "clinic", dx="D66", spec="hematology" if a >= 18 else "peds_sub", rx=False)
            if r.random() < 0.012 * frac:
                dd = self.pick_day(p, d0, d1, "any", "admit")
                if dd:
                    self.admission(p, dd, r.lognormal(math.log(28000), 0.5), "D66")
        if "cf" in c:
            code = CD.cond_code(p.pid, "cf")
            if r.random() < 0.34 * frac:
                self.visit(p, d0, d1, "office_spec", "clinic", dx=code, spec="pulm" if a >= 18 else "peds_sub", rx=False)
            if r.random() < 0.012 * frac:
                dd = self.pick_day(p, d0, d1, "any", "admit")
                if dd:
                    self.admission(p, dd, r.lognormal(math.log(42000), 0.5), code)
        if "kidney_tx" in c or "liver_tx" in c:
            dx = "Z94.0" if "kidney_tx" in c else "Z94.4"
            if r.random() < 0.4 * frac:
                dd = self.visit(p, d0, d1, "office_spec", "clinic", dx=dx, spec="transplant", rx=False)
                if dd:
                    self.add(p, dd, dd, "M", "lab", 1.0, {"ind": "transplant"}, [("P", "lab", 1.0)])
        inf = p.regs.get("infusion")
        if inf is not None:
            while inf[3] <= d1:
                if inf[3] >= d0:
                    dd = W.next_business_day(inf[3])
                    if dd <= d1 and not self.in_stay(p, dd) and "infusion" not in p.slots.get(dd, ()):
                        self.add(p, dd, dd, "M", "infusion", r.lognormal(math.log(6400), 0.12),
                                 {"dx": CD.autoimmune_type(p.pid)[0]}, [("I", "hospital", 0.94), ("P", "gastro", 0.06)])
                inf[3] = inf[3] + dt.timedelta(days=56 + int(r.integers(-3, 6)))
        if "urticaria" in c:
            if r.random() < 0.2 * frac:
                self.visit(p, d0, d1, "office_spec", "clinic", dx=CD.cond_code(p.pid, "urticaria"), spec="allergy", rx=False)
            if r.random() < 0.045 * frac:
                del c["urticaria"]
                p.regs.pop("xolair", None)
        if "cancer_hx" in c and not any(e["kind"] == "cancer" for e in p.eps) and r.random() < 0.12 * frac:
            hx = K.CANCER_HX[self.hx_site.get(p.pid, "breast")]
            dd = self.visit(p, d0, d1, "office_spec", "clinic", dx="Z08", spec="oncology", rx=False, extra={"dx2": hx})
            if dd and r.random() < 0.35:
                self.add(p, dd, dd, "M", "img_ct", 1.0, {"code": "74177" if r.random() < 0.6 else "71260", "dx": "Z08",
                                                          "dx2": hx}, [("I", "hospital", 1.0)])

    # ---------------------------------------------------------------- new conditions and episodes
    def incidence(self, p, a, d0, d1, frac):
        r = self.rh

        def hit(annual):
            return r.random() < (1 - (1 - annual) ** (1 / 12)) * frac

        c = p.conds
        if a >= 25 and not any(e["kind"] == "cancer" for e in p.eps):
            inc = 0.0011 if a < 40 else 0.0027 if a < 50 else 0.0058 if a < 60 else 0.0092
            if p.sex == "M" and a >= 50:
                inc += 0.0025
            if hit(inc):
                dd = self.pick_day(p, d0, d1, "clinic", "img_ct")
                if dd:
                    self.start_cancer(p, a, dd)
        for cond, test, annual in (("diabetes", a >= 30, 0.004 if a < 45 else 0.008),
                                   ("htn", a >= 25, 0.006 if a < 45 else 0.014),
                                   ("depression", a >= 12, 0.012),
                                   ("autoimmune", a >= 18, 0.0011),
                                   ("afib", a >= 45, 0.0015 if a < 55 else 0.003),
                                   ("chf", a >= 45, 0.0007 if a < 55 else 0.0016),
                                   ("copd", a >= 45, 0.0008 if a < 55 else 0.0018)):
            if test and cond not in c and hit(annual):
                c[cond] = d0
                self.start_regimen(p, cond, d0, new=True)
        if 18 <= a <= 65 and "urticaria" not in c and hit(0.0011):
            c["urticaria"] = d0
            self.start_regimen(p, "urticaria", d0)
        if "diabetes" in c and "esrd" not in c and "kidney_tx" not in c and a >= 35 and hit(0.0008):
            c["esrd"] = d0
            self.start_regimen(p, "esrd", d0)
        if a >= 30 and "liver" not in c and "liver_tx" not in c and hit(0.00018):
            c["liver"] = d0
            self.start_regimen(p, "liver", d0)
        if "hepc" in c and hit(0.2):
            dd = self.pick_day(p, d0, d1, "clinic", "office_spec")
            if dd:
                p.eps.append({"kind": "hepc", "m": 0, "start": dd, "drug": "mavyret" if r.random() < 0.55 else "epclusa"})
                del c["hepc"]
        if a >= 5 and hit(0.0011 + (0.0018 if (p.sex == "M" and 16 <= a <= 30) else 0.0)):
            dd = self.pick_day(p, d0, d1, "any", "admit_trauma")
            if dd:
                self.trauma(p, dd, a)
        if a >= 30 and hit(0.0016 if a < 45 else 0.0036 if a < 55 else 0.0062):
            self.major_surgery(p, d0, d1)
        if a >= 45 and hit(0.0011 if a < 55 else 0.0024):
            dd = self.pick_day(p, d0, d1, "any", "admit_cardiac")
            if dd:
                self.stroke(p, dd)
        if a >= 50 and hit(0.0042 if a < 58 else 0.0078) and not any(e["kind"] == "joint" for e in p.eps):
            # a joint replacement, scheduled six to ten weeks out on a surgical day
            when = W.next_business_day(d0 + dt.timedelta(days=int(r.integers(42, 72))))
            p.eps.append({"kind": "joint", "m": 0, "start": when, "site": "knee" if r.random() < 0.6 else "hip"})
        if a >= 35 and hit((0.0006 if a < 45 else 0.0022 if a < 55 else 0.0042) * (1.8 if p.sex == "M" else 0.6)):
            dd = self.pick_day(p, d0, d1, "any", "admit_cardiac")
            if dd:
                self.heart_attack(p, dd)
        if p.sex == "F" and 20 <= a <= 43 and p.rel in ("E", "S") and not any(e["kind"] == "preg" for e in p.eps):
            if hit(0.115 if a < 33 else 0.072 if a < 38 else 0.025):
                self.pregnancy(p, d0 + dt.timedelta(days=int(r.integers(0, (d1 - d0).days + 1))), a)
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
        codes = K.CANCER[site]
        e = {"kind": "cancer", "site": site, "meta": meta, "m": 0, "start": d, "code": codes[CD.h("site", p.pid) % len(codes)],
             "tx": {"breast": int(r.integers(6, 13)), "colon": int(r.integers(5, 8)), "lymphoma": int(r.integers(5, 8)),
                    "lung": int(r.integers(6, 13)), "prostate": int(r.integers(2, 4))}.get(site, 3),
             "hazard": 0.032 if meta else 0.0015, "oral": None}
        if p.rel == "E" and site != "cll":
            p.dis_until = d + dt.timedelta(days=480)
        if site == "cll":
            u = r.random()
            if u < 0.4:
                e["oral"] = "imbruvica"
            elif u < 0.75:
                e["oral"] = "venclexta"
                e["oral_until"] = d + dt.timedelta(days=int(r.integers(380, 420)))
        if meta and site == "breast":
            e["oral"] = "ibrance"
        if meta and site == "prostate":
            e["oral"] = "xtandi"
        self.hx_site[p.pid] = site
        p.eps.append(e)

    def trauma(self, p, d, a):
        r = self.rh
        amt = r.lognormal(math.log(52000), 0.75)
        dx = str(r.choice(K.TRAUMA)) if a < 60 or r.random() < 0.5 else "S72.001A"
        cause = "V43.52XA" if (a < 60 or r.random() < 0.5) else "W19.XXXA"
        los = int(max(2, min(30, round(r.lognormal(math.log(5), 0.6)))))
        if not self.stay_free(p, d, d + dt.timedelta(days=los)):
            return
        self.add(p, d, d, "M", "ambulance", r.lognormal(math.log(1650), 0.2), {"dx": dx, "dx2": cause}, [("P", "ambulance", 1.0)])
        self.admission(p, d, amt, dx, los=los, icu=amt > 90000, kind="admit_trauma", dx2=cause)
        if dx == "S72.001A" and p.sex == "F" and a >= 55 and r.random() < 0.2:
            self.reg(p, "osteo", "forteo", 28, d + dt.timedelta(days=30), until=d + dt.timedelta(days=760))
        p.eps.append({"kind": "rehab", "m": 0, "start": d, "months": int(r.integers(2, 5)), "hazard": 0.004,
                      "dx": dx[:-1] + "D"})

    def major_surgery(self, p, d0, d1):
        """spinal fusion, valve surgery, bariatric and complex abdominal surgery: one stay, then recovery"""
        r = self.rh
        what = str(r.choice(["spine", "cardiac", "abdominal", "bariatric"], p=[0.38, 0.22, 0.28, 0.12]))
        base = {"spine": 78000, "cardiac": 118000, "abdominal": 54000, "bariatric": 31000}[what]
        dx = {"spine": "M48.062", "cardiac": "I35.0", "abdominal": "K57.20", "bariatric": "E66.01"}[what]
        dd = self.pick_day(p, d0, d1, "any" if what == "abdominal" else "elective", "admit_surgery")
        if dd is None:
            return
        if self.admission(p, dd, r.lognormal(math.log(base), 0.35), dx, los=int(r.integers(2, 9)), icu=what == "cardiac",
                          kind="admit_surgery", dx2="Z68.41" if what == "bariatric" else None):
            p.eps.append({"kind": "rehab", "m": 0, "start": dd, "months": int(r.integers(1, 4)), "hazard": 0.003,
                          "dx": {"spine": "Z98.1", "cardiac": "Z95.2", "abdominal": "Z48.815", "bariatric": "Z98.84"}[what]})

    def stroke(self, p, d):
        r = self.rh
        if not self.stay_free(p, d, d + dt.timedelta(days=3)):
            return
        self.add(p, d, d, "M", "ambulance", r.lognormal(math.log(1700), 0.2), {"dx": "I63.9"}, [("P", "ambulance", 1.0)])
        if self.admission(p, d, r.lognormal(math.log(61000), 0.45), "I63.9", los=int(r.integers(3, 10)), icu=True,
                          kind="admit_cardiac"):
            p.eps.append({"kind": "rehab", "m": 0, "start": d, "months": int(r.integers(2, 5)), "hazard": 0.012, "dx": "I69.351"})
            if "afib" not in p.conds and r.random() < 0.3:
                p.conds["afib"] = d
                self.start_regimen(p, "afib", d)

    def heart_attack(self, p, d):
        r = self.rh
        if not self.stay_free(p, d, d + dt.timedelta(days=2)):
            return
        self.add(p, d, d, "M", "ambulance", r.lognormal(math.log(1700), 0.2), {"dx": "I21.4"}, [("P", "ambulance", 1.0)])
        if self.admission(p, d, r.lognormal(math.log(68000), 0.45), "I21.4", los=int(r.integers(2, 7)), icu=True,
                          kind="admit_cardiac"):
            p.conds["cad"] = d
            self.start_regimen(p, "cad", d)
            self.reg(p, "p2y12", "clopidogrel_75" if r.random() < 0.55 else "brilinta", 30, d + DAY,
                     until=d + dt.timedelta(days=365))
            p.eps.append({"kind": "cardiac_rehab", "m": 0, "start": d, "months": 3, "hazard": 0.006})

    def pregnancy(self, p, d, a):
        r = self.rh
        pre = r.random() < 0.095
        if pre:
            # preterm births by gestational age: most late preterm, few extremely preterm
            u = r.random()
            weeks = int(r.integers(34, 37)) if u < 0.72 else int(r.integers(32, 34)) if u < 0.84 else \
                int(r.integers(28, 32)) if u < 0.95 else int(r.integers(24, 28))
        else:
            weeks = int(r.integers(37, 42))
        lmp = d - dt.timedelta(days=14)
        p.eps.append({"kind": "preg", "m": 0, "start": d, "lmp": lmp, "due": lmp + dt.timedelta(days=weeks * 7),
                      "loss": r.random() < 0.13, "pre": pre, "weeks": weeks, "csec": r.random() < (0.45 if pre else 0.3),
                      "first": r.random() < 0.4, "older": a >= 35, "gdm": r.random() < 0.06})

    # ---------------------------------------------------------------- episode care
    def episodes(self, p, d0, d1, frac):
        r = self.rh
        keep = []
        for e in p.eps:
            k = e["kind"]
            if k == "cancer":
                alive = self.cancer_month(p, e, d0, d1, frac)
            elif k == "transplant":
                alive = self.transplant_month(p, e, d0, d1)
            elif k == "rehab":
                if e["m"] >= 1:
                    for i in range(int(r.integers(3, 8))):
                        dd = self.pick_day(p, d0, d1, "therapy", "pt")
                        if dd:
                            self.add(p, dd, dd, "M", "pt", 1.0, {"dx": e["dx"], "first": e["m"] == 1 and i == 0}, [("P", "pt", 1.0)])
                    if r.random() < 0.5:
                        self.visit(p, d0, d1, "office_spec", "clinic", dx=e["dx"], rx=False,
                                   spec=REHAB_SPEC.get(e["dx"], "ortho"))
                    e["hazard"] = 0.0
                alive = e["m"] < e["months"]
            elif k == "cardiac_rehab":
                if e["m"] >= 1:
                    dd = self.pick_day(p, d0, d1, "elective", "cardiac_rehab")
                    if dd:
                        self.add(p, dd, dd, "M", "cardiac_rehab", r.lognormal(math.log(1450), 0.2), {"dx": "I25.2"},
                                 [("I", "hospital", 0.9), ("P", "cardiology", 0.1)])
                    e["hazard"] = 0.0
                alive = e["m"] < e["months"]
            elif k == "joint":
                if e.get("done"):
                    for i in range(int(r.integers(4, 9))):
                        dd = self.pick_day(p, d0, d1, "therapy", "pt")
                        if dd:
                            self.add(p, dd, dd, "M", "pt", 1.0, {"dx": "Z47.1", "first": e.get("after", 0) == 0 and i == 0},
                                     [("P", "pt", 1.0)])
                    e["after"] = e.get("after", 0) + 1
                    alive = e["after"] < 3
                elif e["start"] <= d1:
                    dd = W.next_business_day(max(e["start"], d0))
                    los = int(r.integers(1, 3))
                    if dd <= d1 and self.add(p, dd, dd + dt.timedelta(days=los), "M", "joint", r.lognormal(math.log(41000), 0.2),
                                             {"dx": "M17.11" if e["site"] == "knee" else "M16.11", "site": e["site"], "los": los},
                                             [("I", "hospital", 0.82), ("P", "ortho", 0.13), ("P", "anesthesia", 0.05)]):
                        e["done"] = True
                        self.fill(p, self.rx_day(dd + dt.timedelta(days=los)), "oxycodone_5")
                        self.reg(p, "discharge", "enoxaparin", 10, dd + dt.timedelta(days=los), until=dd + dt.timedelta(days=30))
                    alive = e["m"] < 5
                else:
                    alive = True
            elif k == "hepc":
                fills = 2 if e["drug"] == "mavyret" else 3
                if e["m"] == 0:
                    dd = W.next_business_day(max(e["start"], d0))
                    if self.add(p, dd, dd, "M", "office_spec", 1.0, {"dx": "B18.2", "spec": "gastro"}, [("P", "gastro", 1.0)]):
                        self.add(p, dd, dd, "M", "lab", 1.0, {"ind": "hepc"}, [("P", "lab", 1.0)])
                    p.regs["hcv"] = [e["drug"], 28, None, dd + dt.timedelta(days=int(r.integers(3, 12)))]
                    e["fills"] = 0
                alive = e["m"] < fills + 1
            elif k == "postacute":
                alive = self.postacute_month(p, e, d0, d1)
            elif k == "preg":
                alive = self.pregnancy_month(p, e, d0, d1)
            elif k == "nicu":
                alive = self.nicu_month(p, e, d0, d1)
            else:
                alive = False
            e["m"] += 1
            if alive:
                keep.append(e)
        p.eps = keep
        p.nchronic = sum(1 for c in p.conds if c in CHRONIC) + (1 if any(e["kind"] == "cancer" for e in p.eps) else 0)

    def cancer_month(self, p, e, d0, d1, frac):
        r = self.rh
        m, site = e["m"], e["site"]
        dx = e["code"]
        dx2 = ("C78.7" if site in ("colon", "breast") else "C79.51") if e["meta"] else ""
        spec = K.CANCER_SPEC[site]
        if m == 0:
            dd = max(d0, e["start"])
            self.add(p, dd, dd, "M", "img_ct", 1.0, {"code": "71260" if site == "lung" else "74177", "dx": dx}, [("I", "hospital", 1.0)])
            bd = self.pick_day(p, dd + DAY, d1, "elective", "biopsy") if dd < d1 else None
            if bd:
                self.add(p, bd, bd, "M", "biopsy", r.lognormal(math.log(3300), 0.35), {"dx": dx},
                         [("I", "hospital", 0.7), ("P", "specialist", 0.3)])
            vd = self.pick_day(p, bd or dd, d1, "clinic", "office_spec")
            if vd:
                self.add(p, vd, vd, "M", "office_spec", 1.0, {"dx": dx, "spec": spec, "dx2": dx2}, [("P", "oncology", 1.0)])
            return True
        surg = site in ("breast", "colon", "lung", "prostate") and not (e["meta"] and site == "lung")
        if surg and m == 1:
            dd = self.pick_day(p, d0, d1, "elective", "admit_surgery")
            if dd:
                self.admission(p, dd, r.lognormal(math.log({"breast": 26000, "colon": 47000, "lung": 52000, "prostate": 29000}[site]), 0.3),
                               dx, los=int(r.integers(1, 5)), kind="admit_surgery")
            return True
        if e["meta"] or site == "cll":
            if e["oral"] and "onc" not in p.regs and not e.get("oral_done"):
                p.regs["onc"] = [e["oral"], 28, e.get("oral_until"), self.pick_day(p, d0, d1, "clinic") or d0]
                e["oral_done"] = True
            if e["meta"] and not e["oral"]:
                dd = self.pick_day(p, d0, d1, "elective", "chemo")
                if dd:
                    self.add(p, dd, dd, "M", "chemo", r.lognormal(math.log(16500), 0.3) * frac, {"dx": dx, "site": site},
                             [("I", "hospital", 0.9), ("P", "oncology", 0.1)])
                    if site in ("breast", "lymphoma") and m < 7 and e.setdefault("gcsf_m", r.random() < 0.5):
                        self.fill(p, W.next_business_day(dd + DAY), "udenyca" if r.random() < 0.6 else "fulphila")
            if r.random() < (0.5 if e["meta"] else 0.25):
                self.visit(p, d0, d1, "office_spec", "clinic", dx=dx, spec=spec, rx=False, extra={"dx2": dx2})
            if e["meta"] and r.random() < 0.06 * frac:
                dd = self.pick_day(p, d0, d1, "any", "admit")
                if dd:
                    self.admission(p, dd, r.lognormal(math.log(39000), 0.45), self.cancer_admit_dx(site), dx2=dx)
            if site == "cll" and m > 24:
                e["hazard"] = 0.0005
            return True
        first = 2 if surg else 1
        tx = e["tx"]
        if first <= m < first + tx:
            dd = self.pick_day(p, d0, d1, "elective", "chemo" if site != "prostate" else "radiation")
            if site == "prostate":
                if dd:
                    self.add(p, dd, dd, "M", "radiation", r.lognormal(math.log(14500), 0.25) * frac, {"dx": dx, "first": m == first},
                             [("I", "hospital", 0.86), ("P", "radonc", 0.14)])
            else:
                if "support" not in p.regs and dd:
                    self.reg(p, "support", "ondansetron", 30, dd, until=dd + dt.timedelta(days=30 * (first + tx - m)))
                base = {"breast": 15500, "colon": 12800, "lung": 17500, "lymphoma": 24500}[site]
                if m - first >= 4:
                    base *= 0.55      # maintenance: the targeted or immune agent alone, every three weeks
                if dd:
                    self.add(p, dd, dd, "M", "chemo", r.lognormal(math.log(base), 0.28) * frac, {"dx": dx, "site": site},
                             [("I", "hospital", 0.9), ("P", "oncology", 0.1)])
                    if "gcsf" not in e:
                        e["gcsf"] = r.random() < {"breast": 0.75, "colon": 0.35, "lymphoma": 0.85, "lung": 0.3}.get(site, 0.0)
                    if e["gcsf"] and m - first < 5:
                        self.fill(p, W.next_business_day(dd + DAY), "udenyca" if r.random() < 0.6 else "fulphila")
                    if site == "colon" and m - first < 6 and e.setdefault("capox", r.random() < 0.45):
                        self.fill(p, self.rx_day(dd), "capecitabine")
                if r.random() < 0.05:
                    ad = self.pick_day(p, d0, d1, "any", "admit")
                    if ad:
                        u = r.random()
                        self.admission(p, ad, r.lognormal(math.log(29000), 0.45),
                                       "D70.1" if u < 0.6 else "E86.0" if u < 0.8 else "A41.9", dx2=dx)
            return True
        if site == "breast" and first + tx <= m < first + tx + 2:
            dd = self.pick_day(p, d0, d1, "elective", "radiation")
            if dd:
                self.add(p, dd, dd, "M", "radiation", r.lognormal(math.log(11800), 0.25) * frac, {"dx": dx, "first": m == first + tx},
                         [("I", "hospital", 0.86), ("P", "radonc", 0.14)])
            return True
        p.conds["cancer_hx"] = d0
        u = r.random()
        if site == "breast":
            self.reg(p, "hormonal", "tamoxifen" if p.age(d0) < 50 else ("anastrozole" if r.random() < 0.6 else "letrozole"),
                     90 if r.random() < 0.5 else 30, d0)
            if u < 0.1:
                self.reg(p, "adjuvant", "verzenio", 28, d0, until=d0 + dt.timedelta(days=730))
            elif u < 0.14:
                self.reg(p, "adjuvant", "lynparza", 30, d0, until=d0 + dt.timedelta(days=365))
        elif site == "lung" and u < 0.12:
            self.reg(p, "adjuvant", "tagrisso", 30, d0, until=d0 + dt.timedelta(days=1095))
        elif site == "lung" and u < 0.16:
            self.reg(p, "adjuvant", "alecensa", 30, d0, until=d0 + dt.timedelta(days=730))
        return False

    def cancer_admit_dx(self, site):
        """the principal diagnosis of a stay for a complication of a cancer that has spread"""
        u = self.rh.random()
        if u < 0.3:
            return "G89.3"
        if u < 0.5:
            return {"colon": "K56.699", "lung": "J91.0", "breast": "J91.0", "lymphoma": "R50.9"}.get(site, "E86.0")
        if u < 0.7:
            return "A41.9"
        if u < 0.85:
            return "E86.0"
        return "J18.9"

    def transplant_month(self, p, e, d0, d1):
        r = self.rh
        m = e["m"]
        kid = e["organ"] == "kidney"
        dx = "Z94.0" if kid else "Z94.4"
        if not e.get("done"):
            dd = self.pick_day(p, d0, d1, "any", "transplant")
            if dd is None:
                return m < 6
            los = int(r.integers(4, 9) if kid else r.integers(9, 22))
            pre = "N18.6" if kid else CD.cond_code(p.pid, "liver")
            if self.add(p, dd, dd + dt.timedelta(days=los), "M", "transplant", r.lognormal(math.log(385000 if kid else 760000), 0.18),
                        {"dx": pre, "organ": e["organ"], "los": los},
                        [("I", "hospital", 0.86), ("P", "transplant", 0.11), ("P", "anesthesia", 0.03)]):
                e["done"] = m
                p.conds.pop("esrd" if kid else "liver", None)
                p.conds["kidney_tx" if kid else "liver_tx"] = dd
                for k in ("binder", "vitd", "lactulose", "rifaximin"):
                    p.regs.pop(k, None)
                self.start_regimen(p, "kidney_tx", dd)
                if r.random() < 0.3:
                    self.reg(p, "cmv", "prevymis", 28, dd + dt.timedelta(days=los), until=dd + dt.timedelta(days=200))
                else:
                    self.reg(p, "cmv", "valganciclovir", 30, dd + dt.timedelta(days=los), until=dd + dt.timedelta(days=180))
                self.reg(p, "pjp", "smx_tmp_ss", 30, dd + dt.timedelta(days=los), until=dd + dt.timedelta(days=270))
                e["hazard"] = 0.006
            return True
        since = m - e["done"]
        if since <= 3:
            for _ in range(int(r.integers(3, 6))):
                self.visit(p, d0, d1, "office_spec", "clinic", dx=dx, spec="transplant", rx=False)
            dd = self.pick_day(p, d0, d1, "lab", "lab")
            if dd:
                self.add(p, dd, dd, "M", "lab", 1.0, {"ind": "transplant"}, [("P", "lab", 1.0)])
            if r.random() < 0.18:
                ad = self.pick_day(p, d0, d1, "any", "admit")
                if ad:
                    self.admission(p, ad, r.lognormal(math.log(41000), 0.4), "T86.11" if kid else "T86.41", followup=False, dx2=dx)
            return True
        if since <= 12:
            self.visit(p, d0, d1, "office_spec", "clinic", dx=dx, spec="transplant", rx=False)
            e["hazard"] = 0.0015
            return True
        return False

    def postacute_month(self, p, e, d0, d1):
        """the months after a large stay: follow-up visits and labs, home health or a rehabilitation or nursing
        facility stay, and a readmission for some"""
        r = self.rh
        m = e["m"]
        dx = e["dx"]
        fu = dx[:-1] + "D" if dx.startswith("S") and dx.endswith("A") else "Z09"
        if m == 0:
            if e["big"] and r.random() < 0.3:
                st = max(d0, e["start"])
                stay = int(r.integers(7, 21))
                self.add(p, st, st + dt.timedelta(days=stay), "M", "postacute_facility", r.lognormal(math.log(1650), 0.25) * stay,
                         {"dx": dx, "los": stay, "irf": e.get("irf", False)}, [("I", "postacute", 0.93), ("P", "pmr", 0.07)])
            return True
        if m <= 3:
            for _ in range(int(r.integers(1, 4))):
                self.visit(p, d0, d1, "office_spec", "clinic", dx=fu, rx=False, extra={"dx2": dx if fu == "Z09" else ""},
                           spec=CD.specialty_for(dx, p.age(d0)))
            if e["big"] and r.random() < 0.35:
                dd = self.pick_day(p, d0, d1, "therapy", "home_health")
                if dd:
                    self.add(p, dd, min(d1, dd + dt.timedelta(days=int(r.integers(6, 20)))), "M", "home_health",
                             r.lognormal(math.log(2300), 0.35), {"dx": fu, "dx2": dx if fu == "Z09" else ""},
                             [("I", "homehealth", 1.0)])
            if r.random() < (0.07 if m == 1 else 0.035):
                dd = self.pick_day(p, d0, d1, "any", "admit")
                if dd:
                    self.admission(p, dd, r.lognormal(math.log(24000), 0.5), dx if not dx.startswith(("Z", "S", "O", "P")) else
                                   self.admit_dx(p, p.age(dd)), followup=False)
            return m < 3
        return False

    def pregnancy_month(self, p, e, d0, d1):
        r = self.rh
        m = e["m"]
        if e["loss"] and m == 2:
            dd = self.pick_day(p, d0, d1, "clinic", "office_spec")
            if dd:
                self.add(p, dd, dd, "M", "office_spec", 1.0, {"dx": "O03.9" if r.random() < 0.7 else "O02.1", "spec": "obgyn"},
                         [("P", "obgyn", 1.0)])
            return False
        due = e["due"]
        lmp = e["lmp"]

        def ga(d):
            return (d - lmp).days // 7

        def visit_dx(d):
            w = ga(d)
            tri = 1 if w < 14 else 2 if w < 28 else 3
            if e["gdm"] and w >= 26:
                return "O24.410"
            if e["older"]:
                return ("O09.51%d" if e["first"] else "O09.52%d") % tri
            return ("Z34.0%d" if e["first"] else "Z34.8%d") % tri

        if due > d1:
            if m >= 1:
                dd = self.pick_day(p, d0, d1, "clinic", "prenatal")
                if dd:
                    w = ga(dd)
                    wk = "Z3A.%02d" % max(8, min(42, w))
                    self.add(p, dd, dd, "M", "prenatal", 1.0, {"dx": visit_dx(dd), "dx2": wk}, [("P", "obgyn", 1.0)])
                    if m == 1:
                        self.add(p, dd, dd, "M", "lab", 1.0, {"ind": "prenatal", "dx": visit_dx(dd)}, [("P", "lab", 1.0)])
                    elif 24 <= w <= 28 and not e.get("gtt"):
                        e["gtt"] = True
                        self.add(p, dd, dd, "M", "lab", 1.0, {"ind": "glucose_tolerance", "dx": visit_dx(dd)}, [("P", "lab", 1.0)])
                    elif 35 <= w <= 37 and not e.get("gbs"):
                        e["gbs"] = True
                        self.add(p, dd, dd, "M", "lab", 1.0, {"ind": "gbs", "dx": visit_dx(dd)}, [("P", "lab", 1.0)])
                    if m in (3, 6):
                        self.add(p, dd, dd, "M", "img_us", 1.0, {"ob": True, "dx2": wk}, [("I", "hospital", 1.0)])
                    if m == 2 and r.random() < 0.12:
                        self.fill(p, self.rx_day(dd), "doxylamine_pyridoxine")
            return True
        if due < d0:
            return False
        cs = e["csec"]
        stay = int(r.integers(2, 4)) if cs else int(r.integers(1, 3))
        amt = r.lognormal(math.log(19500 if cs else 13600), 0.18) * (1.35 if e["pre"] else 1.0)
        w = e["weeks"]
        if e["pre"]:
            dx = "O60.14X0" if w >= 28 else "O60.12X0"
        elif cs:
            dx = str(r.choice(["O34.211", "O32.1XX0", "O82", "O62.0", "O63.1"], p=[0.38, 0.14, 0.18, 0.18, 0.12]))
        elif w >= 41:
            dx = "O48.0"
        else:
            dx = "O80" if r.random() < 0.78 else "O70.1"
        # a planned caesarean is scheduled on a weekday; labour starts when it starts
        if cs and not e["pre"] and due.weekday() >= 5 and due + dt.timedelta(days=7 - due.weekday()) <= d1:
            due = due + dt.timedelta(days=7 - due.weekday())
        if not self.add(p, due, due + dt.timedelta(days=stay), "M", "delivery", amt, {"dx": dx, "csec": cs, "los": stay},
                        [("I", "hospital", 0.72), ("P", "obgyn", 0.21), ("P", "anesthesia", 0.07)]):
            return False
        pp = W.next_business_day(due + dt.timedelta(days=int(r.integers(38, 50))))
        self.pp_visits.setdefault(p.pid, []).append(pp)
        baby = self.birth(p, due)
        if baby is not None:
            if e["pre"]:
                # a preterm baby goes home at about 36 to 39 weeks after the mother's last period, later the earlier it
                # was born
                home = 39.0 if w < 28 else 37.5 if w < 32 else 36.5
                days = int(max(5, min(140, round(7 * (home - w) * r.lognormal(0, 0.16)))))
                baby.eps.append({"kind": "nicu", "m": 0, "start": due, "days": days, "weeks": w, "hazard": 0.004, "csec": cs})
            elif r.random() < 0.035:
                baby.eps.append({"kind": "nicu", "m": 0, "start": due, "days": int(r.integers(4, 15)), "weeks": w, "hazard": 0.0,
                                 "csec": cs})
            else:
                self.add(baby, due, due + dt.timedelta(days=stay), "M", "newborn", r.lognormal(math.log(3600), 0.25),
                         {"dx": "Z38.01" if cs else "Z38.00", "los": stay}, [("I", "hospital", 0.86), ("P", "pediatrics", 0.14)])
        return False

    def nicu_month(self, p, e, d0, d1):
        r = self.rh
        m = e["m"]
        w = e["weeks"]
        if m == 0:
            dd, days = e["start"], e["days"]
            if w < 28:
                code = {23: "P07.22", 24: "P07.23", 25: "P07.24", 26: "P07.25", 27: "P07.26"}.get(w, "P07.26")
            elif w <= 36:
                code = "P07.3%d" % (w - 27)
            else:
                code = str(r.choice(["P22.1", "P70.4", "P36.9", "P59.9"], p=[0.4, 0.2, 0.2, 0.2]))
            second = "P22.0" if w < 34 else "P22.1" if w <= 36 else "P92.9"
            if w < 30 and r.random() < 0.4:
                second = "P27.1"
            self.add(p, dd, dd + dt.timedelta(days=days), "M", "nicu", days * r.lognormal(math.log(4350), 0.15),
                     {"dx": code, "dx2": second, "los": days, "weeks": w, "csec": e.get("csec", False)},
                     [("I", "hospital", 0.88), ("P", "neonatology", 0.12)])
            e["code"] = code if w <= 36 else "Z09"
            return True
        if m <= 8:
            for _ in range(int(r.integers(1, 4))):
                self.visit(p, d0, d1, "office_spec", "clinic", dx=e["code"], rx=False,
                           spec="peds_sub" if w < 32 else "pediatrics")
            if r.random() < 0.07:
                dd = self.pick_day(p, d0, d1, "any", "admit")
                if dd:
                    self.admission(p, dd, r.lognormal(math.log(26000), 0.5), CD.wpick(K.ADMIT_INFANT, r.random()))
            e["hazard"] = 0.0004
            return True
        return False

    # ---------------------------------------------------------------- pharmacy
    def pharmacy(self, p, a, d0, d1):
        r = self.rh
        bio = p.regs.get("biologic")
        if bio is not None:
            started = self.bio_start.get(p.pid)
            early = started is not None and (d0 - started).days < 365
            if r.random() < (0.035 if early else 0.012):
                del p.regs["biologic"]
                self.bio_start.pop(p.pid, None)
                if "autoimmune" in p.conds and r.random() < 0.4:
                    drugs = [x for x in CD.autoimmune_type(p.pid)[2] if x not in (bio[0], "hyrimoz")]
                    if drugs:
                        self.start_biologic(p, drugs[int(r.integers(0, len(drugs)))],
                                            d1 + dt.timedelta(days=int(r.integers(5, 30))))
        elif "autoimmune" in p.conds and "infusion" not in p.regs and r.random() < 0.009:
            # stepped up from conventional treatment to a biologic
            drugs = CD.autoimmune_type(p.pid)[2]
            self.start_biologic(p, drugs[int(r.integers(0, len(drugs)))], d0 + dt.timedelta(days=int(r.integers(0, 20))))
        if "glp1" in p.regs and r.random() < 0.018:
            del p.regs["glp1"]
        # a weight-loss GLP-1 under the plan's obesity coverage: started on a prescriber's request, often stopped
        if "glp1_wl" in p.regs:
            if r.random() < 0.035:
                del p.regs["glp1_wl"]
        elif "obesity" in p.conds and "glp1" not in p.regs and 20 <= a < 65 and r.random() < 0.0045:
            self.reg(p, "glp1_wl", "wegovy" if r.random() < 0.55 else "zepbound", 28, d0)
        for pp in [x for x in self.pp_visits.get(p.pid, ()) if d0 <= x <= d1]:
            self.pp_visits[p.pid].remove(pp)
            if not self.in_stay(p, pp):
                self.add(p, pp, pp, "M", "office_spec", 1.0, {"dx": "Z39.2", "spec": "obgyn"}, [("P", "obgyn", 1.0)])
        for key in list(p.regs):
            rg = p.regs[key]
            drug, days, until, nxt = rg
            if drug == "infliximab":
                continue
            while nxt <= d1:
                if nxt >= d0 and (rg[2] is None or nxt <= rg[2]):
                    ds = 25 if drug == "albuterol" else days
                    self.fill(p, self.rx_day(nxt), drug, days=ds)
                    if key == "hcv":
                        ep = [e for e in p.eps if e["kind"] == "hepc"]
                        if ep:
                            ep[0]["fills"] = ep[0].get("fills", 0) + 1
                            if ep[0]["fills"] >= (2 if drug == "mavyret" else 3):
                                rg[2] = nxt
                gap = int(r.integers(-2, 4)) if r.random() < 0.85 else int(r.integers(5, 25))
                step = 25 if drug == "albuterol" else 60 if drug == "tretinoin_cream" else days
                nxt = nxt + dt.timedelta(days=max(20, step + gap + (45 if drug == "albuterol" else 0)))
                rg[3] = nxt
            if until is not None and nxt > until:
                del p.regs[key]

    # ---------------------------------------------------------------- identifiers after the run
    def finish(self):
        r = self.rp
        conv = W.CONVERSION - DAY
        for fam in self.fams:
            mem = [self.people[i] for i in fam.members]
            onconv = [p for p in mem if p.covered_on(conv) and p.covered_on(W.CONVERSION)]
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
            kids = sorted([p for p in live if p.rel == "C"], key=lambda q: (q.first_start() > conv, q.dob, q.pid))
            for p in live:
                p.member_id = self.new_member_id()
                p.code = "01" if p.rel in ("E", "R") else "02" if p.rel == "S" else None
            for k, p in enumerate(kids):
                p.code = "%02d" % (3 + k)
        # a service is billed only for a day the member is covered: a course of visits booked before a death, a
        # termination or a gap, and a prescription picked up a few days after coverage ended, never reach the plan
        self.events = [e for e in self.events if self.people[e[0]].covered_on(e[1])]
        self.events.sort(key=lambda e: (e[1], e[0], e[4]))


def simulate(seed=W.SEED):
    s = Sim(seed)
    s.run()
    return s
