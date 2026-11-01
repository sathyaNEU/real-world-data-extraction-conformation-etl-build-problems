"""The trial's records, drawn from the world: the CTU's screening log, the IRT's randomisation and drug
administration logs, the BICR's timepoint reads, the investigators' reads, the EDC's status, dosing, local
laboratory, sample tracking and adverse event pages, the central laboratory's transfer and the pharmacovigilance
safety database. Each record family draws from its own stream so that adding one never moves another."""
import datetime as dt
import math
import string

from zoneinfo import ZoneInfo

import numpy as np

import world as W

TZ = {"GB": "Europe/London", "IE": "Europe/Dublin", "FR": "Europe/Paris", "ES": "Europe/Madrid", "IT": "Europe/Rome",
      "DE": "Europe/Berlin", "NL": "Europe/Amsterdam", "BE": "Europe/Brussels", "PL": "Europe/Warsaw",
      "CZ": "Europe/Prague", "SE": "Europe/Stockholm", "NO": "Europe/Oslo", "NZ": "Pacific/Auckland"}
AU_TZ = {"Melbourne": "Australia/Melbourne", "Sydney": "Australia/Sydney", "Brisbane": "Australia/Brisbane",
         "Perth": "Australia/Perth", "Adelaide": "Australia/Adelaide", "Hobart": "Australia/Hobart",
         "Newcastle NSW": "Australia/Sydney", "Geelong": "Australia/Melbourne", "Gold Coast": "Australia/Brisbane",
         "Canberra": "Australia/Sydney"}
TZ = {city: (AU_TZ[city] if code == "AU" else TZ[code]) for code, cities in W.CITIES.items() for city in cities}

LETTERS = [c for c in string.ascii_uppercase if c not in "QXZ"]
SCREEN_FAIL_REASONS = [
    ("Measurable disease not confirmed on screening CT", False), ("ECOG performance status 2", True),
    ("Total bilirubin above 1.5 x ULN (biliary drainage pending)", True), ("Creatinine clearance below 50 mL/min", True),
    ("Prior systemic therapy for advanced disease", False), ("Active autoimmune disease requiring treatment", False),
    ("Haemoglobin below 9.0 g/dL", True), ("Cholangitis within 14 days of screening", True),
    ("Patient decision before randomisation", False), ("Ampullary carcinoma on central pathology review", False),
    ("Uncontrolled hepatitis B infection", False), ("Brain metastases on screening imaging", False),
]
RESCREEN_REASONS = [r for r, ok in SCREEN_FAIL_REASONS if ok]
BACKLOG = {"FR02": dt.date(2026, 9, 7), "IT01": dt.date(2026, 9, 21), "PL02": dt.date(2026, 8, 31)}


def rng_for(w, k):
    return np.random.default_rng([w.seed, k])


def cal(w, rel):
    return W.day(w.fpi, rel)


def wk(d):
    return W.weekday_fix(d)


class Records:
    def __init__(self, w):
        self.w = w
        self.site = {i: s for i, s in enumerate(w.sites)}
        self._people()
        self._screening()
        self._efficacy()
        self._dosing()
        self._labs()
        self._safety()

    # ------------------------------------------------------------------ people and screening
    def _people(self):
        r = rng_for(self.w, 1)
        for p in self.w.pts:
            p["sex"] = "F" if r.uniform() < 0.47 else "M"
            age = int(np.clip(r.normal(64, 9.5), 33, 85))
            p["rand_date"] = cal(self.w, p["rday"])
            p["yob"] = p["rand_date"].year - age - (1 if r.uniform() < 0.5 else 0)
            p["initials"] = r.choice(LETTERS) + r.choice(LETTERS)
            p["ecog"] = 0 if r.uniform() < 0.46 else 1
            p["weight"] = round(float(np.clip(r.normal(74 if p["sex"] == "M" else 63, 12), 40, 130)), 1)
            p["height"] = int(np.clip(r.normal(175 if p["sex"] == "M" else 162, 7), 145, 200))
            p["bsa"] = round(math.sqrt(p["weight"] * p["height"] / 3600.0), 2)
            p["liver_mets"] = r.uniform() < 0.48
            p["site_id"] = self.site[p["site"]]["site_id"]
            p["code"] = self.site[p["site"]]["code"]
            tz = ZoneInfo(TZ[self.site[p["site"]]["city"]])
            local = dt.datetime.combine(p["rand_date"], dt.time(int(r.integers(8, 18)), int(r.integers(0, 60))), tzinfo=tz)
            p["rand_utc"] = local.astimezone(dt.timezone.utc).replace(tzinfo=None)
        self.w.pts.sort(key=lambda p: (p["rday"], p["i"]))
        for k, p in enumerate(self.w.pts):
            p["rand_no"] = "TL2-%04d" % (k + 1)
        # IRT stratum entry errors: the site picked the neighbouring option on the IRT screen
        for p in self.w.pts:
            p["irt_ds"], p["irt_ps"] = p["ds"], p["ps"]
        for k in r.choice(len(self.w.pts), 9, replace=False):
            p = self.w.pts[int(k)]
            if r.uniform() < 0.5:
                p["irt_ds"] = 1 - p["ds"]
            else:
                p["irt_ps"] = (p["ps"] + 1) % 3

    def _screening(self):
        r = rng_for(self.w, 2)
        attempts = []
        for p in self.w.pts:
            sd = wk(p["rand_date"] - dt.timedelta(days=int(r.integers(4, 22))))
            attempts.append(dict(site_id=p["site_id"], date=sd, sex=p["sex"], yob=p["yob"], initials=p["initials"],
                                 outcome="Randomised", reason="", pt=p))
        # re-screens: a failed first attempt three to ten weeks before the randomised one
        cands = [p for p in self.w.pts if p["rday"] > 60]
        idx = r.choice(len(cands), 16, replace=False)
        self.rescreened = []
        for k in sorted(idx):
            p = cands[int(k)]
            first = [a for a in attempts if a["pt"] is p][0]
            d0 = wk(first["date"] - dt.timedelta(days=int(r.integers(21, 71))))
            attempts.append(dict(site_id=p["site_id"], date=d0, sex=p["sex"], yob=p["yob"], initials=p["initials"],
                                 outcome="Screen failure", reason=str(r.choice(RESCREEN_REASONS)), pt=p, first=True))
            self.rescreened.append(p)
        # genuine screen failures, spread over the enrolment period at sites already open
        start = min(p["rday"] for p in self.w.pts)
        end = max(p["rday"] for p in self.w.pts)
        for _ in range(171):
            rd = int(r.integers(start - 10, end + 1))
            open_sites = [s for s in self.w.sites if s["activation"] <= rd] or self.w.sites[:3]
            wts = np.array([s["weight"] for s in open_sites])
            s = open_sites[int(r.choice(len(open_sites), p=wts / wts.sum()))]
            sex = "F" if r.uniform() < 0.47 else "M"
            yob = int(cal(self.w, rd).year - np.clip(r.normal(65, 10), 33, 86))
            reason, _ok = SCREEN_FAIL_REASONS[int(r.integers(0, len(SCREEN_FAIL_REASONS)))]
            outcome = "Withdrew before randomisation" if reason.startswith("Patient decision") else "Screen failure"
            attempts.append(dict(site_id=s["site_id"], date=wk(cal(self.w, rd)), sex=sex, yob=yob,
                                 initials=r.choice(LETTERS) + r.choice(LETTERS), outcome=outcome, reason=reason, pt=None))
        attempts.sort(key=lambda a: (a["date"], a["site_id"], a["initials"]))
        seq = {}
        for a in attempts:
            seq[a["site_id"]] = seq.get(a["site_id"], 0) + 1
            a["screening_no"] = "%s-%03d" % (a["site_id"], seq[a["site_id"]])
            if a["pt"] is not None:
                if a.get("first"):
                    a["pt"]["first_screening_no"] = a["screening_no"]
                else:
                    a["pt"]["screening_no"] = a["screening_no"]
        # a screening attempt can only be dated on or after its site's activation; the log keeps the CTU's order
        self.screening = attempts
        # screen-failure SAEs (reported during screening, never randomised)
        self.sf_attempts = [a for a in attempts if a["pt"] is None]

    # ------------------------------------------------------------------ efficacy records
    def _efficacy(self):
        r = rng_for(self.w, 3)
        w = self.w
        self.bicr, self.inv = [], []
        for p in w.pts:
            for s in p["scans"]:
                sd = cal(w, p["rday"] + s["day"])
                if sd > w.snapshot - dt.timedelta(days=3):
                    continue
                label = "Week %d" % (s["nominal"] // 7)
                read = sd + dt.timedelta(days=int(r.integers(4, 19)))
                read = min(read, w.snapshot - dt.timedelta(days=1))
                self.bicr.append(dict(rand_no=p["rand_no"], timepoint=label, scan_date=sd, response=s["resp"],
                                      read_date=read))
                # the investigator's own read: calls progression earlier for some flares, misses some
                ir = s["resp"]
                if ir == "SD" and s["day"] < 100 and r.uniform() < 0.06:
                    ir = "PD"
                elif ir == "PD" and r.uniform() < 0.07:
                    ir = "SD"
                elif ir == "NE":
                    ir = "SD" if r.uniform() < 0.7 else "NE"
                self.inv.append(dict(rand_no=p["rand_no"], timepoint=label, assessment_date=sd, response=ir))
        # deaths, withdrawals, treatment status
        for p in w.pts:
            pd_cal = cal(w, p["rday"] + p["pd_day"]) if p["pd_day"] is not None else None
            p["pd_cal"] = pd_cal
            # death: before progression (the world's own time) or after it (survival after progression)
            if pd_cal is not None:
                p["death_rel"] = p["rday"] + p["pd_day"] + float(r.exponential(150))
            else:
                p["death_rel"] = p["rday"] + p["tdeath"] if p["tdeath"] < p["tdrop"] else None
            p["death_date"] = cal(w, int(p["death_rel"])) if p["death_rel"] is not None else None
            if p["death_date"] is not None and p["death_date"] > w.snapshot:
                p["death_date"] = None
            p["withdraw_date"] = cal(w, p["rday"] + int(p["tdrop"])) if p["tdrop"] < p["tdeath"] else None
            if p["withdraw_date"] is not None and p["withdraw_date"] > w.snapshot:
                p["withdraw_date"] = None
            if p["withdraw_date"] is not None and p["death_date"] is not None and p["withdraw_date"] < p["death_date"]:
                p["death_date"] = None
            if p["death_date"] is not None and p["pd_cal"] is None:
                p["death_cause"] = "Adverse event" if r.uniform() < 0.35 else ("Disease progression (clinical)" if r.uniform() < 0.6 else "Other")
            elif p["death_date"] is not None:
                p["death_cause"] = "Disease progression"
            else:
                p["death_cause"] = ""

    # ------------------------------------------------------------------ treatment: EDC dosing and IRT administration
    def _dosing(self):
        r = rng_for(self.w, 4)
        w = self.w
        self.dose_edc, self.dose_irt = [], []
        site_lag = {s["site_id"]: float(r.uniform(5, 26)) for s in w.sites}
        for sid in ("FR02", "IT01", "PL02"):
            site_lag[sid] = float(r.uniform(38, 55))
        kit = 400000
        for p in w.pts:
            first = wk(p["rand_date"] + dt.timedelta(days=int(r.integers(1, 8))))
            stop = []
            if p["pd_cal"] is not None:
                stop.append(p["pd_cal"] + dt.timedelta(days=int(r.integers(3, 12))))
            if p["death_date"] is not None:
                stop.append(p["death_date"])
            if p["withdraw_date"] is not None:
                stop.append(p["withdraw_date"])
            if r.uniform() < 0.09:
                stop.append(first + dt.timedelta(days=int(r.integers(30, 260))))
            stop.append(w.cut + dt.timedelta(days=1))
            end = min(stop)
            p["first_dose"] = first if first <= w.cut and first < end else None
            doses = []
            d = first
            cyc = 1
            while d < end and d <= w.cut:
                if cyc <= 8:
                    doses.append((d, "C%dD1" % cyc, cyc, "D1"))
                    d8 = wk(d + dt.timedelta(days=7))
                    if d8 < end and d8 <= w.cut and r.uniform() > 0.08:
                        doses.append((d8, "C%dD8" % cyc, cyc, "D8"))
                    d = wk(d + dt.timedelta(days=21 + (int(r.integers(1, 8)) if r.uniform() < 0.2 else 0)))
                else:
                    doses.append((d, "M%d" % (cyc - 8), cyc, "D1"))
                    d = wk(d + dt.timedelta(days=28 + (int(r.integers(1, 8)) if r.uniform() < 0.15 else 0)))
                cyc += 1
            p["doses"] = doses
            backlog = BACKLOG.get(p["site_id"])
            for (dd, visit, c, dday) in doses:
                lag = r.exponential(site_lag[p["site_id"]])
                entered = dd + dt.timedelta(days=int(lag))
                if backlog is not None and dd >= backlog:
                    # the site's research nurse post fell vacant: its dosing pages from this date were keyed later
                    entered = w.snapshot + dt.timedelta(days=int(r.integers(3, 30)))
                in_edc = entered <= w.snapshot
                if dday == "D1":
                    kit += int(r.integers(1, 9))
                    self.dose_irt.append(dict(rand_no=p["rand_no"], site_id=p["site_id"], visit=visit, kit_no="K%06d" % kit,
                                              dispensed=dd, status="Administered"))
                    if r.uniform() < 0.012:
                        # a damaged kit replaced at the same visit
                        kit += 1
                        self.dose_irt.append(dict(rand_no=p["rand_no"], site_id=p["site_id"], visit=visit,
                                                  kit_no="K%06d" % kit, dispensed=dd, status="Not administered - replaced"))
                    if in_edc:
                        self.dose_edc.append(dict(rand_no=p["rand_no"], visit=visit, drug="Ravolimab/placebo",
                                                  admin_date=dd, dose=1500.0, unit="mg", entered=entered))
                if c <= 8 and in_edc:
                    for drug, mg in (("Gemcitabine", 1000.0), ("Cisplatin", 25.0)):
                        red = 0.8 if r.uniform() < 0.1 else 1.0
                        self.dose_edc.append(dict(rand_no=p["rand_no"], visit=visit, drug=drug, admin_date=dd,
                                                  dose=round(mg * red * p["bsa"], 0), unit="mg", entered=entered))
            p["last_dose"] = doses[-1][0] if doses else None
            p["on_treatment"] = bool(doses) and end > w.cut

    # ------------------------------------------------------------------ laboratory samples
    def _labs(self):
        r = rng_for(self.w, 5)
        w = self.w
        self.central, self.local, self.sample_log = [], [], []
        acc = 6100000
        ref = {"ALT": {"M": 50, "F": 35}, "AST": {"M": 40, "F": 32}, "TBIL": 21, "ALP": 130, "ALB": (35, 50),
               "CREAT": {"M": 110, "F": 90}, "HGB": {"M": (130, 170), "F": (115, 155)}, "WBC": (4.0, 11.0),
               "NEUT": (2.0, 7.5), "PLAT": (150, 400)}
        units = {"ALT": "U/L", "AST": "U/L", "TBIL": "umol/L", "ALP": "U/L", "ALB": "g/L", "CREAT": "umol/L",
                 "HGB": "g/L", "WBC": "10^9/L", "NEUT": "10^9/L", "PLAT": "10^9/L"}
        names = {"ALT": "Alanine aminotransferase", "AST": "Aspartate aminotransferase", "TBIL": "Bilirubin, total",
                 "ALP": "Alkaline phosphatase", "ALB": "Albumin", "CREAT": "Creatinine", "HGB": "Haemoglobin",
                 "WBC": "Leukocytes", "NEUT": "Neutrophils", "PLAT": "Platelets"}
        self.lab_names, self.lab_units = names, units
        for p in w.pts:
            base_alt = float(np.exp(r.normal(np.log(32 if not p["liver_mets"] else 48), 0.45)))
            base_ast = float(np.exp(r.normal(np.log(30 if not p["liver_mets"] else 44), 0.4)))
            base_bil = float(np.exp(r.normal(np.log(11), 0.4)))
            # episodes on treatment: immune hepatitis (more on ravolimab), cholangitis or stent occlusion
            ep = []
            if p["first_dose"] is not None and p["doses"]:
                span = (p["doses"][-1][0] - p["first_dose"]).days + 30
                if r.uniform() < (0.085 if p["arm"] == 1 else 0.02) and span > 40:
                    t0 = p["first_dose"] + dt.timedelta(days=int(r.integers(35, max(36, span))))
                    ep.append(("hep", t0, float(r.uniform(5.3, 14)), int(r.integers(14, 35))))
                if r.uniform() < 0.11 and span > 20:
                    t0 = p["first_dose"] + dt.timedelta(days=int(r.integers(10, max(11, span))))
                    ep.append(("chol", t0, float(r.uniform(3.2, 8)), int(r.integers(7, 21))))
            p["episodes"] = ep
            # the central samples: screening, each D1 visit, C1D8, and the safety follow-up 30 days after the last dose
            visits = []
            sd = [a for a in self.screening if a["pt"] is p and not a.get("first")][0]["date"]
            visits.append(("SCR", sd))
            for (dd, visit, c, dday) in p["doses"]:
                if dday == "D1" or visit == "C1D8":
                    visits.append((visit, dd))
            if p["doses"] and not p["on_treatment"]:
                sfu = wk(p["doses"][-1][0] + dt.timedelta(days=int(30 + r.integers(-4, 8))))
                if sfu <= w.cut and (p["death_date"] is None or sfu < p["death_date"]):
                    visits.append(("SFU", sfu))
            # the pre-dose spike: a raised liver panel on the morning of the first dose, dosed on the local result
            p["predose_spike"] = None
            if p["first_dose"] is not None and r.uniform() < 0.075:
                p["predose_spike"] = (str(r.choice(["ALT", "AST", "TBIL", "ALT+AST"])), float(r.uniform(1.03, 1.35)))
            melb = p["code"] in ("AU", "NZ")
            p["visits"] = visits
            p["_base"] = (base_alt, base_ast, base_bil)
        self._cover_spikes(r)
        for p in w.pts:
            base_alt, base_ast, base_bil = p["_base"]
            visits = p["visits"]
            melb = p["code"] in ("AU", "NZ")
            for visit, d in visits:
                if d > w.cut:
                    continue
                acc += int(r.integers(1, 40))
                accession = "HB%07d" % acc
                coll_time = "%02d:%02d" % (int(r.integers(7, 12)), int(r.integers(0, 60)))
                recv = d + dt.timedelta(days=int(r.choice([1, 1, 1, 2, 2, 3])) + (2 if d.weekday() == 4 else 0))
                self.sample_log.append(dict(rand_no=p["rand_no"], visit=visit, accession_no=accession, collected=d,
                                            time=coll_time))
                vals = self._values(r, p, d, visit, base_alt, base_ast, base_bil, ref)
                for an in ("HGB", "WBC", "NEUT", "PLAT", "ALT", "AST", "ALP", "TBIL", "ALB", "CREAT"):
                    lo, hi = self._range(ref[an], p["sex"])
                    self.central.append(dict(lab="Halden Bioanalytical, Melbourne" if melb else "Halden Bioanalytical, Edinburgh",
                                             accession_no=accession, screening_no=p["screening_no"], visit=visit,
                                             date=recv if melb else d, test_code=an, test_name=names[an],
                                             result=vals[an], unit=units[an], ref_low=lo, ref_high=hi))
            # local hepatic panels: unscheduled bloods at the trial hospital (fever, jaundice, a dosing check)
            nloc = int(r.poisson(1.1 if p["code"] in ("SE", "NO") else 0.45))
            for _ in range(nloc):
                if not p["doses"]:
                    break
                span = max(1, (min(p["doses"][-1][0] + dt.timedelta(days=30), w.cut) - p["first_dose"]).days)
                d = wk(p["first_dose"] + dt.timedelta(days=int(r.integers(1, span + 1))))
                if d > w.cut:
                    continue
                vals = self._values(r, p, d, "UNS", base_alt, base_ast, base_bil, ref)
                nordic = p["code"] in ("SE", "NO")
                for an in ("ALT", "AST", "TBIL"):
                    lo, hi = self._range(ref[an], p["sex"])
                    v = vals[an]
                    unit = units[an]
                    if nordic and an in ("ALT", "AST"):
                        v, hi, unit = round(v / 60.0, 2), round((0.70 if p["sex"] == "M" else 0.55) if an == "ALT" else (0.75 if p["sex"] == "M" else 0.60), 2), "ukat/L"
                    elif an == "TBIL" and nordic:
                        hi = 25
                    self.local.append(dict(rand_no=p["rand_no"], lab="Local laboratory " + p["site_id"], collected=d,
                                           test_name=names[an], result=v, unit=unit, uln=hi))

    def _cover_spikes(self, r):
        """Every arm and liver test carries at least two Melbourne patients whose raised value was the pre-dose one."""
        w = self.w
        for arm in (0, 1):
            for an in ("ALT", "AST", "TBIL"):
                have = [p for p in w.pts if p["code"] in ("AU", "NZ") and p["arm"] == arm and p.get("predose_spike")
                        and an in p["predose_spike"][0].split("+") and not p["episodes"]]
                pool = [p for p in w.pts if p["code"] in ("AU", "NZ") and p["arm"] == arm and not p.get("predose_spike")
                        and not p["episodes"] and p["first_dose"] is not None and p["first_dose"] < w.cut - dt.timedelta(days=30)]
                for k in range(max(0, 2 - len(have))):
                    p = pool.pop(int(r.integers(0, len(pool))))
                    p["predose_spike"] = (an, float(r.uniform(1.04, 1.3)))

    @staticmethod
    def _range(spec, sex):
        if isinstance(spec, dict):
            spec = spec[sex]
        if isinstance(spec, tuple):
            return spec
        return (None, spec)

    def _values(self, r, p, d, visit, b_alt, b_ast, b_bil, ref):
        alt, ast, bil = b_alt * float(np.exp(r.normal(0, 0.18))), b_ast * float(np.exp(r.normal(0, 0.16))), b_bil * float(np.exp(r.normal(0, 0.2)))
        uln_alt, uln_ast, uln_bil = ref["ALT"][p["sex"]], ref["AST"][p["sex"]], ref["TBIL"]
        # eligibility caps the pre-treatment panel (ALT and AST at 5 x ULN with liver involvement, bilirubin 1.5 x)
        if visit == "SCR":
            alt, ast, bil = min(alt, 4.6 * uln_alt), min(ast, 4.6 * uln_ast), min(bil, 1.45 * uln_bil)
        if visit == "C1D1" and p.get("predose_spike"):
            which, f = p["predose_spike"]
            if "ALT" in which:
                alt = 5.0 * uln_alt * f
            if "AST" in which:
                ast = 5.0 * uln_ast * f
            if which == "TBIL":
                bil = 3.0 * uln_bil * f
        elif visit != "SCR":
            alt, ast, bil = min(alt, 4.8 * uln_alt), min(ast, 4.8 * uln_ast), min(bil, 2.8 * uln_bil)
        for kind, t0, mult, dur in p.get("episodes", []):
            if t0 <= d <= t0 + dt.timedelta(days=dur):
                if kind == "hep":
                    alt, ast = max(alt, mult * uln_alt * float(r.uniform(0.9, 1.1))), max(ast, mult * 0.8 * uln_ast * float(r.uniform(0.9, 1.1)))
                else:
                    bil = max(bil, mult * uln_bil * float(r.uniform(0.9, 1.1)))
                    alt, ast = max(alt, 0.6 * mult * uln_alt), max(ast, 0.55 * mult * uln_ast)
        hgb = float(np.clip(r.normal(118 if p["sex"] == "F" else 128, 12), 70, 170))
        wbc = float(np.clip(r.lognormal(np.log(6.5), 0.35), 0.8, 25))
        neut = float(np.clip(wbc * r.uniform(0.5, 0.75), 0.2, 20))
        plat = float(np.clip(r.lognormal(np.log(240), 0.35), 25, 700))
        return {"ALT": int(round(alt)), "AST": int(round(ast)), "TBIL": int(round(bil)), "ALP": int(round(float(r.lognormal(np.log(180), 0.5)))),
                "ALB": int(round(float(np.clip(r.normal(36, 4), 22, 48)))), "CREAT": int(round(float(np.clip(r.normal(78, 18), 40, 190)))),
                "HGB": int(round(hgb)), "WBC": round(wbc, 1), "NEUT": round(neut, 2), "PLAT": int(round(plat))}

    # ------------------------------------------------------------------ serious adverse events
    def _safety(self):
        r = rng_for(self.w, 6)
        w = self.w
        catalogue = [
            ("Cholangitis", "Hepatobiliary disorders", 0.20, 1.0), ("Biliary obstruction", "Hepatobiliary disorders", 0.08, 1.0),
            ("Immune-mediated hepatitis", "Hepatobiliary disorders", 0.0, 1.0),
            ("Sepsis", "Infections and infestations", 0.07, 1.0), ("Pneumonia", "Infections and infestations", 0.05, 1.0),
            ("Biliary sepsis", "Infections and infestations", 0.05, 1.0), ("Urinary tract infection", "Infections and infestations", 0.02, 1.0),
            ("Febrile neutropenia", "Blood and lymphatic system disorders", 0.07, 1.0), ("Anaemia", "Blood and lymphatic system disorders", 0.04, 1.0),
            ("Thrombocytopenia", "Blood and lymphatic system disorders", 0.02, 1.0),
            ("Vomiting", "Gastrointestinal disorders", 0.04, 1.0), ("Colitis", "Gastrointestinal disorders", 0.01, 3.5),
            ("Gastric outlet obstruction", "Gastrointestinal disorders", 0.03, 1.0), ("Diarrhoea", "Gastrointestinal disorders", 0.02, 1.6),
            ("Pulmonary embolism", "Respiratory, thoracic and mediastinal disorders", 0.03, 1.0),
            ("Pneumonitis", "Respiratory, thoracic and mediastinal disorders", 0.003, 6.0),
            ("Acute kidney injury", "Renal and urinary disorders", 0.03, 1.0), ("Pyrexia", "General disorders and administration site conditions", 0.04, 1.0),
            ("Fatigue", "General disorders and administration site conditions", 0.01, 1.0),
        ]
        upgrade = {"Pyrexia": ("Biliary sepsis", "Infections and infestations"), "Vomiting": ("Gastric outlet obstruction", "Gastrointestinal disorders")}
        events = []
        for p in w.pts:
            if p["first_dose"] is None:
                continue
            end = min([x for x in (p["death_date"], w.snapshot) if x is not None])
            span = (end - p["rand_date"]).days
            for term, soc, rate, ravo in catalogue:
                lam = rate * (ravo if p["arm"] == 1 else 1.0) * span / 180.0
                for _ in range(int(r.poisson(lam))):
                    onset = p["rand_date"] + dt.timedelta(days=int(r.integers(2, max(3, span))))
                    events.append(dict(pt=p, term=term, soc=soc, onset=onset))
            for kind, t0, mult, dur in p.get("episodes", []):
                if kind == "hep" and r.uniform() < 0.55:
                    events.append(dict(pt=p, term="Immune-mediated hepatitis", soc="Hepatobiliary disorders", onset=t0))
        # the re-screened patients whose sites kept the first number: make their SAEs cover every class in both arms
        dosed = [p for p in self.rescreened if p["first_dose"] is not None and p["first_dose"] < w.cut - dt.timedelta(days=60)]
        firstno = [p for p in dosed if p["arm"] == 0][:3] + [p for p in dosed if p["arm"] == 1][:3]
        need = {(a, soc) for a in (0, 1) for soc in ("Infections and infestations", "Hepatobiliary disorders",
                                                      "Gastrointestinal disorders", "Blood and lymphatic system disorders")}
        have = {(e["pt"]["arm"], e["soc"]) for e in events if e["pt"] in firstno and e["onset"] <= w.cut}
        pick = {"Infections and infestations": "Pneumonia", "Hepatobiliary disorders": "Cholangitis",
                "Gastrointestinal disorders": "Vomiting", "Blood and lymphatic system disorders": "Febrile neutropenia"}
        for a, soc in sorted(need - have):
            cand = [p for p in firstno if p["arm"] == a and p["first_dose"] is not None]
            p = cand[int(r.integers(0, len(cand)))]
            lo = p["first_dose"] + dt.timedelta(days=5)
            hi = min([x for x in (p["death_date"], w.cut) if x is not None])
            onset = lo + dt.timedelta(days=int(r.integers(0, max(1, (hi - lo).days))))
            events.append(dict(pt=p, term=pick[soc], soc=soc, onset=onset))
        self.firstno = firstno
        # screening-period SAEs of patients never randomised (reported, and never in an arm)
        sf_events = []
        for a in r.choice(len(self.sf_attempts), 7, replace=False):
            at = self.sf_attempts[int(a)]
            sf_events.append(dict(sf=at, term=str(r.choice(["Cholangitis", "Biliary obstruction", "Sepsis", "Pyrexia"])),
                                  onset=at["date"] + dt.timedelta(days=int(r.integers(1, 9)))))
        for e in sf_events:
            e["soc"] = dict((t, s) for t, s, _a, _b in catalogue)[e["term"]]
        # pharmacovigilance: one case per event, an initial report and follow-ups, some recoded on medical review
        self.pv, self.ae_edc = [], []
        case = 2026000
        events.sort(key=lambda e: (e["onset"], e["pt"]["rand_no"] if "pt" in e else ""))
        allev = [("pt", e) for e in events] + [("sf", e) for e in sf_events]
        allev.sort(key=lambda x: x[1]["onset"])
        site_lag = {s["site_id"]: float(r.uniform(6, 30)) for s in w.sites}
        nullify = set(int(x) for x in r.choice(len(allev), 4, replace=False))
        for k, (kind, e) in enumerate(allev):
            case += int(r.integers(1, 6))
            recv = e["onset"] + dt.timedelta(days=int(r.integers(0, 3)))
            if recv > w.snapshot:
                continue
            if kind == "pt":
                p = e["pt"]
                sno = p["first_screening_no"] if p in self.firstno else p["screening_no"]
                site, sex, yob = p["site_id"], p["sex"], p["yob"]
            else:
                at = e["sf"]
                sno, site, sex, yob = at["screening_no"], at["site_id"], at["sex"], at["yob"]
            term0, soc0 = e["term"], e["soc"]
            want_up = term0 in upgrade and r.uniform() < 0.7
            nfu = int(r.choice([0, 1, 1, 2, 3]))
            dates = [recv]
            for j in range(nfu):
                dates.append(dates[-1] + dt.timedelta(days=int(r.integers(4, 30))))
            dates = [d for d in dates if d <= w.snapshot]
            upgraded = want_up and len(dates) >= 2
            final_term, final_soc = upgrade[term0] if upgraded else (term0, soc0)
            reported = term0
            null = k in nullify and kind == "pt" and len(dates) >= 2
            for j, d in enumerate(dates):
                last = j == len(dates) - 1
                t, s_ = (final_term, final_soc) if (upgraded and j >= 1) else (term0, soc0)
                status = "Nullified" if (null and last) else ("Closed" if last and d < w.snapshot - dt.timedelta(days=20) else "Open")
                self.pv.append(dict(case_no="TL2-SAE-%d" % case, version="Initial" if j == 0 else "Follow-up %d" % j,
                                    receipt_date=d, site_id=site, screening_no=sno, sex=sex, year_of_birth=yob,
                                    reported_term=reported, meddra_pt=t, meddra_soc=s_, onset_date=e["onset"],
                                    seriousness="Hospitalisation" if r.uniform() < 0.85 else "Life-threatening",
                                    case_status=status))
            e["case"] = "TL2-SAE-%d" % case
            e["null"] = null
            e["final"] = (final_term, final_soc)
            e["pv_dates"] = dates
            if kind == "pt":
                ent = e["onset"] + dt.timedelta(days=int(r.exponential(site_lag[p["site_id"]])) + 3)
                if ent <= w.snapshot:
                    self.ae_edc.append(dict(rand_no=p["rand_no"], term=e["final"][0], soc=e["final"][1], onset=e["onset"],
                                            grade=int(r.choice([3, 3, 3, 4])), serious="Y" if not null else "Y"))
        self.events = events
        self.sf_events = sf_events
        # non-serious adverse events for the EDC listing
        ns = [("Fatigue", "General disorders and administration site conditions"), ("Nausea", "Gastrointestinal disorders"),
              ("Neutrophil count decreased", "Investigations"), ("Anaemia", "Blood and lymphatic system disorders"),
              ("Decreased appetite", "Metabolism and nutrition disorders"), ("Pruritus", "Skin and subcutaneous tissue disorders"),
              ("Rash", "Skin and subcutaneous tissue disorders"), ("Constipation", "Gastrointestinal disorders"),
              ("Hypothyroidism", "Endocrine disorders"), ("Peripheral sensory neuropathy", "Nervous system disorders"),
              ("Diarrhoea", "Gastrointestinal disorders"), ("Alanine aminotransferase increased", "Investigations")]
        for p in w.pts:
            if p["first_dose"] is None:
                continue
            for term, soc in ns:
                if r.uniform() < (0.35 if term in ("Fatigue", "Nausea") else 0.15):
                    on = p["first_dose"] + dt.timedelta(days=int(r.integers(1, 200)))
                    if on <= w.cut:
                        ent = on + dt.timedelta(days=int(r.exponential(site_lag[p["site_id"]])) + 3)
                        if ent <= w.snapshot:
                            self.ae_edc.append(dict(rand_no=p["rand_no"], term=term, soc=soc, onset=on,
                                                    grade=int(r.choice([1, 1, 2, 2, 3])), serious="N"))
