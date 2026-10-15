"""The clean truth: every arrest of every person in the window, and for each arrest in the county its booking, screen,
first appearance before the magistrate on duty, the conditions set, the release or the stay, the cases and their
dispositions, the court dates and failures to appear, the monitoring and the boarding. Nothing here carries mess; the
exports in records.py are written from it.

The decisive structure: at each eligible first appearance the magistrate sees what the arrest affidavit and the
defendant in front of him show (`D`, an episode trait the scale does not see) and holds the defendants who show it far
more often, at a rate that differs by magistrate (`lam`); a held defendant's outcome is never recorded, and the duty
rota sends every magistrate the same mix of arrests."""
from __future__ import annotations

import bisect
import datetime as dt
import math
from dataclasses import dataclass, field

import numpy as np

import catalog as C
import common as K

DAY = dt.timedelta(days=1)

# ---------------------------------------------------------------------------------------------------- parameters
# the episode trait the magistrate sees and the scale does not, by new-criminal-activity score (index 0 is score 1)
D_SHARE = np.array([0.05, 0.09, 0.15, 0.30, 0.36, 0.42])
# probability of a new-offence arrest within the window (365 days or disposition) for an eligible defendant released at
# first appearance, by score, for D = 0 and D = 1; the hazards below are solved from these
P_WIN0 = np.array([0.045, 0.058, 0.070, 0.075, 0.160, 0.190])
P_WIN1 = np.array([0.17, 0.22, 0.30, 0.80, 0.80, 0.82])
# eligible: the magistrate's hold propensity (before his own strictness) by score, for D = 0 and D = 1
H0 = np.array([0.004, 0.008, 0.015, 0.030, 0.045, 0.065])
H1 = np.array([0.55, 0.75, 0.95, 1.60, 1.70, 1.80])
HOLD_CAP = 0.985
# ineligible charges: hold propensity by kind, scaled by the score and by D
HK = {"MX": 0.30, "FH": 0.33, "FX": 0.62, "DET": 1.0}
Q_POST = (0.30, 0.06)          # a secured bond posted within 24 hours, D = 0 and D = 1
L_POST = (0.50, 0.12)          # a held defendant posting later (day 3 to 60), D = 0 and D = 1
P_IN_COUNTY = 0.80
P_WARRANT = 0.07               # a later arrest that is on a warrant for an earlier offence
FTA_P = np.array([0.020, 0.036, 0.058, 0.085, 0.120, 0.165])   # per court date, by failure-to-appear score
EM_P = {"M": np.array([0.003, 0.006, 0.012, 0.025, 0.040, 0.060]), "MX": 0.09, "FH": 0.06, "FX": 0.16}
SWAP_RATE = 1 / 38.0           # equipment changes per monitored day
P_BOARD = 0.32                 # a stay crossing the boarding window's third day boarded at Halsey
P_RETURN = 0.55                # a boarded defendant returned to Dorrance before release
P_ANNEX = 0.35                 # a stay longer than four days moved to the annex
N_MAG = 32
SHIFT_ON = 4                   # magistrates on duty per twelve-hour shift
# stream offsets for the year the asks read, fixed once so every ask figure sits mid-bin: the first appearances from
# 1 October 2025 (their release, stay and cases), the failures to appear, the monitoring enrollments; none of them
# reaches a first appearance before 1 October 2025
OFFSETS = {"fy": 4, "fta": 4, "em": 1}


def lognorm(r, median, sigma, lo, hi):
    return float(min(hi, max(lo, median * math.exp(sigma * r.standard_normal()))))


def solve_hazard(p, median=105.0, sigma=0.6):
    """The daily hazard whose probability of an arrest inside min(365, LN(median, sigma)) days is p."""
    z = np.linspace(-4, 4, 801)
    w = np.exp(-0.5 * z ** 2)
    w /= w.sum()
    W = np.minimum(365.0, np.clip(median * np.exp(sigma * z), 7, 700))
    lo, hi = 1e-6, 0.1
    for _ in range(80):
        h = 0.5 * (lo + hi)
        if (w * (1 - np.exp(-h * W))).sum() < p:
            lo = h
        else:
            hi = h
    return 0.5 * (lo + hi)


HAZ0 = np.array([solve_hazard(p) for p in P_WIN0])
HAZ1 = np.array([solve_hazard(p) for p in P_WIN1])


@dataclass
class Person:
    pid: int
    sid: str
    last: str
    first: str
    middle: str
    dob: dt.date
    sex: str
    cls: int                    # 0 low, 1 mid, 2 high propensity
    mult: float                 # the person's hazard multiplier
    misd_conv: list = field(default_factory=list)       # dates of convictions
    fel_conv: list = field(default_factory=list)
    viol_conv: list = field(default_factory=list)
    incarc: list = field(default_factory=list)
    ftas: list = field(default_factory=list)            # dates of failures to appear
    hist: dict = field(default_factory=dict)            # counts before the window
    open_cases: list = field(default_factory=list)      # (filed, disposed) pairs, any county


class World:
    pass


# ---------------------------------------------------------------------------------------------------- magistrates
def magistrates():
    from faker import Faker
    fk = Faker("en_US")
    fk.seed_instance(K.SEED + 7)
    r = K.rng("magistrates")
    out, used_init, used_names = [], {}, set()
    lam = np.sort(r.uniform(0.04, 1.30, N_MAG))
    order = r.permutation(N_MAG)
    for k in range(N_MAG):
        while True:
            first, last = fk.first_name(), fk.last_name()
            if (first, last) not in used_names and last not in {n[1] for n in used_names}:
                break
        used_names.add((first, last))
        mi = fk.random_uppercase_letter()
        ini = (first[0] + mi + last[0]).upper()
        if ini in used_init:
            used_init[ini] += 1
            ini_key = ini + str(used_init[ini])
        else:
            used_init[ini] = 1
            ini_key = ini
        out.append(dict(k=k, first=first, middle=mi, last=last, initials=ini_key, empno="MG%05d" % (20100 + 37 * k + r.integers(0, 30)),
                        lam=float(lam[order[k]])))
    # commissions: 25 serving at the start, 7 joining during the window, 6 leaving
    joins = sorted(r.choice(np.arange(25, N_MAG), 7, replace=False))
    for m in out:
        m["start"] = dt.date(2010 + int(r.integers(0, 11)), int(r.integers(1, 13)), 1)
        m["end"] = None
    days = (K.EXTRACT_END - K.HIST_START).days
    for i, k in enumerate(range(25, N_MAG)):
        out[k]["start"] = K.HIST_START + dt.timedelta(days=int(120 + i * (days - 400) / 7 + r.integers(0, 40)))
    leavers = r.choice(np.arange(0, 25), 6, replace=False)
    for i, k in enumerate(sorted(leavers)):
        out[k]["end"] = K.HIST_START + dt.timedelta(days=int(300 + i * (days - 500) / 6 + r.integers(0, 40)))
    return out


class Rota:
    """Twelve-hour shifts from 07:00 and 19:00, four magistrates on duty, taken in turn from those serving, so every
    magistrate works days, nights and weekends alike over the window."""

    def __init__(self, mags):
        self.mags = mags
        self.cache = {}
        self.ptr = 0
        self.order = list(range(len(mags)))
        self.shifts = {}
        t = K.d2dt(K.HIST_START) - dt.timedelta(hours=5)       # the 19:00 shift of 30 September 2021
        end = K.d2dt(K.EXTRACT_END + DAY, 7)
        while t < end:
            d = t.date()
            serving = [m["k"] for m in mags if m["start"] <= d and (m["end"] is None or d <= m["end"])]
            on = []
            while len(on) < SHIFT_ON:
                cand = self.order[self.ptr % len(self.order)]
                self.ptr += 1
                if cand in serving and cand not in on:
                    on.append(cand)
            self.shifts[t] = on
            t += dt.timedelta(hours=12)
        self.starts = sorted(self.shifts)

    def on_duty(self, t):
        i = bisect.bisect_right(self.starts, t) - 1
        return self.shifts[self.starts[i]]


# ---------------------------------------------------------------------------------------------------- people
def people(r):
    from faker import Faker
    fk = Faker("en_US")
    fk.seed_instance(K.SEED + 11)
    out = []
    n_ret, n_fresh = 38000, 62000
    for i in range(n_ret + n_fresh):
        fresh = i >= n_ret
        cls = int(r.choice(3, p=[0.52, 0.34, 0.14] if fresh else [0.18, 0.44, 0.38]))
        sex = "M" if r.random() < 0.74 else "F"
        first = fk.first_name_male() if sex == "M" else fk.first_name_female()
        last = fk.last_name()
        middle = fk.first_name_male() if sex == "M" else fk.first_name_female()
        age = (lognorm(r, 22.5, 0.17, 18, 45) if fresh else lognorm(r, 29, 0.28, 19, 72))
        p = Person(pid=i, sid="%08d" % (21000000 + int(r.integers(0, 78000000))), last=last, first=first,
                   middle=middle, dob=dt.date(2021, 10, 1) - dt.timedelta(days=int(age * 365.25)), sex=sex, cls=cls,
                   mult=float(math.exp(0.15 * r.standard_normal())))
        # a case pending somewhere the county's index does not hold (another county, a citation), by class
        p.pend_other = [0.08, 0.28, 0.52][cls] * (0.35 if fresh else 1.0)
        if fresh:
            p.hist = dict(misd=int(r.random() < [0.05, 0.15, 0.30][cls]), fel=0, viol=0, incarc=0,
                          fta2=int(r.random() < [0.02, 0.06, 0.12][cls]), fta_old=0)
            p.first_t = K.d2dt(K.HIST_START) + dt.timedelta(minutes=int(r.integers(0, ((K.EXTRACT_END - K.HIST_START).days + 1) * 1440)))
        else:
            mp = [0.55, 0.85, 0.96][cls]
            fp = [0.10, 0.38, 0.70][cls]
            vp = [0.06, 0.24, 0.50][cls]
            ip = [0.04, 0.22, 0.56][cls]
            p.hist = dict(misd=int(r.random() < mp), fel=int(r.random() < fp),
                          viol=(2 if r.random() < [0.0, 0.05, 0.22][cls] else int(r.random() < vp)),
                          incarc=int(r.random() < ip),
                          fta2=(2 if r.random() < [0.03, 0.09, 0.18][cls] else int(r.random() < [0.08, 0.20, 0.30][cls])),
                          fta_old=int(r.random() < [0.12, 0.34, 0.58][cls]))
            haz = [0.0011, 0.0018, 0.0031][cls] * p.mult
            if r.random() < 0.5:
                p.first_t = K.d2dt(K.HIST_START) + dt.timedelta(minutes=int(r.exponential(1 / haz) * 1440))
            else:
                p.first_t = K.d2dt(K.HIST_START) + dt.timedelta(minutes=int(r.integers(0, ((K.EXTRACT_END - K.HIST_START).days + 1) * 1440)))
        out.append(p)
    seen = set()
    for p in out:
        while p.sid in seen:
            p.sid = "%08d" % (int(p.sid) + 7919)
        seen.add(p.sid)
    return out


# ---------------------------------------------------------------------------------------------------- charges
def draw_charges(r, cls):
    kp = [[0.60, 0.18, 0.17, 0.05], [0.49, 0.17, 0.26, 0.08], [0.39, 0.15, 0.33, 0.13]][cls]
    kind = ["M", "MX", "FH", "FX"][int(r.choice(4, p=kp))]
    n = int(r.choice([1, 2, 3, 4], p=[0.56, 0.29, 0.12, 0.03]))
    codes = []

    def pick(k):
        lst = C.KIND_CODES[k]
        w = np.array([o[7] for o in lst], float)
        return lst[int(r.choice(len(lst), p=w / w.sum()))][0]
    codes.append(pick(kind))
    for _ in range(n - 1):
        if kind == "M":
            k2 = "M" if r.random() < 0.90 else "MX"
        elif kind == "MX":
            k2 = "M" if r.random() < 0.60 else "MX"
        else:
            k2 = "M" if r.random() < 0.55 else kind
        c = pick(k2)
        if c not in codes:
            codes.append(c)
    kinds = [C.BY_CODE[c][5] for c in codes]
    top = "FX" if "FX" in kinds else "FH" if "FH" in kinds else "MX" if "MX" in kinds else "M"
    return codes, top


# ---------------------------------------------------------------------------------------------------- the simulation
def items_at(p, t, pending):
    d = t.date()
    age = (d - p.dob).days / 365.25
    misd = int(p.hist["misd"] > 0 or any(x < d for x in p.misd_conv))
    fel = int(p.hist["fel"] > 0 or any(x < d for x in p.fel_conv))
    nv = p.hist["viol"] + sum(1 for x in p.viol_conv if x < d)
    viol = 2 if nv >= 3 or p.hist["viol"] == 2 else (1 if nv >= 1 else 0)
    inc = int(p.hist["incarc"] > 0 or any(x < d for x in p.incarc))
    nca = dict(age_22_or_under=int(age < 23), pending_charge=int(pending), prior_misd_conviction=misd,
               prior_felony_conviction=fel, prior_violent_conviction=viol, prior_incarceration=inc)
    raw = sum(dict(C.NCA_ITEMS[i][2])[nca[C.NCA_ITEMS[i][0]]] for i in range(len(C.NCA_ITEMS)))
    return nca, raw, C.band(raw, C.NCA_BANDS)


def fta_items_at(p, t, pending, nca):
    d = t.date()
    recent = sum(1 for x in p.ftas if (d - x).days <= 730 and x < d)
    older = sum(1 for x in p.ftas if (d - x).days > 730)
    f2 = min(2, recent + (p.hist["fta2"] if (d - K.HIST_START).days <= 730 else 0))
    fo = int(older > 0 or p.hist["fta_old"] > 0 or (p.hist["fta2"] > 0 and (d - K.HIST_START).days > 730))
    it = dict(pending_charge=int(pending), prior_conviction=int(nca["prior_misd_conviction"] or nca["prior_felony_conviction"]),
              fta_past_2_years=f2, fta_older=fo)
    raw = sum(dict(C.FTA_ITEMS[i][2])[it[C.FTA_ITEMS[i][0]]] for i in range(len(C.FTA_ITEMS)))
    return it, raw, C.band(raw, C.FTA_BANDS)


def simulate():
    W = World()
    W.mags = magistrates()
    rota = Rota(W.mags)
    W.rota = rota
    r = K.rng("world")
    persons = people(K.rng("people"))
    W.persons = persons
    W.n_eps = 0
    end_t = K.d2dt(K.EXTRACT_END + DAY)
    eps, arrests, stays, cases = [], [], [], []
    for p in persons:
        t = p.first_t
        first = True
        ak = -1
        while t < end_t:
            ak += 1
            rr = K.rng("p", p.pid, ak)
            in_county = first or rr.random() < P_IN_COUNTY
            warrant = (not first) and rr.random() < P_WARRANT
            codes, top = draw_charges(rr, p.cls)
            off_date = (t.date() - dt.timedelta(days=int(rr.integers(14, 240)))) if warrant else t.date()
            a = dict(pid=p.pid, t=t, offence_date=off_date, codes=codes, type="WARRANT" if warrant else "NEW",
                     county=K.COUNTY if in_county else None, ep=None)
            arrests.append(a)
            first = False
            if not in_county:
                # held or cited elsewhere; a case pending there for a while
                p.open_cases.append((t.date(), t.date() + dt.timedelta(days=int(lognorm(rr, 110, 0.6, 10, 500)))))
                liberty = t + dt.timedelta(hours=int(rr.integers(3, 30)))
                if rr.random() < 0.12:
                    liberty += dt.timedelta(days=int(lognorm(rr, 12, 0.8, 2, 120)))
                haz = 0.0018 * p.mult
                t = liberty + dt.timedelta(minutes=int(rr.exponential(1 / haz) * 1440))
                continue
            e = episode(W, p, a, codes, top, rr, rota, cases, ak)
            if e is None:
                break
            a["ep"] = e["eid"]
            eps.append(e)
            stays.extend(e["stays"])
            t = e["next_t"]
    W.eps, W.arrests, W.stays, W.cases = eps, arrests, stays, cases
    court_dates(W)
    finish_ftas(W)
    monitoring(W)
    return W


def episode(W, p, a, codes, top, rr, rota, cases, ak):
    t = a["t"]
    eid = W.n_eps
    booking = t + dt.timedelta(minutes=int(rr.integers(30, 150)))
    pending = any(f <= t.date() < dd for f, dd in p.open_cases) or rr.random() < p.pend_other
    nca_it, nca_raw, nca = items_at(p, t, pending)
    detainer = rr.random() < 0.03
    eligible = all(C.eligible_charge(c) for c in codes) and not detainer
    D = bool(rr.random() < D_SHARE[nca - 1])
    screened = rr.random() < 0.966
    screen_t = booking + dt.timedelta(minutes=int(rr.integers(25, 110)))
    fa = screen_t + dt.timedelta(minutes=int(rr.integers(20, 330)))
    if fa >= K.d2dt(K.EXTRACT_END + DAY):
        return None
    W.n_eps += 1
    if fa.date() >= K.FY26_START:
        rr = K.rng("fy", p.pid, ak, OFFSETS["fy"])
    on = rota.on_duty(fa)
    mag = on[int(rr.integers(0, len(on)))]
    lam = W.mags[mag]["lam"]
    if eligible:
        ph = min(HOLD_CAP, (H1 if D else H0)[nca - 1] * lam)
    else:
        k = "DET" if detainer else top
        ph = min(HOLD_CAP, HK[k] * (0.7 + 0.12 * nca) * (1.9 if D else 1.0) * (0.55 + 0.6 * lam) if k != "DET" else 1.0)
    q = Q_POST[1 if D else 0]
    p_sec = 1.0 if detainer else min(1.0, ph / (1 - q))
    secured = rr.random() < p_sec
    if secured:
        cond = "SECURED"
        bond = int(rr.choice([500, 750, 1000, 1500, 2000, 2500, 3000, 5000, 7500, 10000],
                             p=[0.18, 0.08, 0.22, 0.12, 0.10, 0.08, 0.07, 0.09, 0.03, 0.03]))
        if top in ("FH", "FX"):
            bond *= int(rr.choice([2, 3, 5, 10]))
        posted = (not detainer) and rr.random() < q
    else:
        cond = ["WRITTEN_PROMISE", "UNSECURED", "CUSTODY"][int(rr.choice(3, p=[0.70, 0.26, 0.04]))]
        bond = int(rr.choice([500, 1000, 1500, 2000, 2500, 5000], p=[0.25, 0.35, 0.12, 0.12, 0.08, 0.08])) if cond == "UNSECURED" else 0
        posted = False
    released24 = (not secured) or posted
    # the case(s): a felony and its misdemeanours can share a file; some split into two files
    felony = top in ("FH", "FX")
    split = felony and len(codes) > 1 and rr.random() < 0.45
    groups = [codes]
    if split:
        fcodes = [c for c in codes if C.BY_CODE[c][5] in ("FH", "FX")]
        mcodes = [c for c in codes if c not in fcodes]
        groups = [fcodes, mcodes] if mcodes else [codes]
    # durations
    if released24:
        rel_t = fa + (dt.timedelta(minutes=int(rr.integers(30, 240))) if not secured else
                      dt.timedelta(minutes=int(rr.integers(120, 1200))))
    else:
        rel_t = None
    misd_dur_rel = lognorm(rr, 105, 0.6, 7, 700)
    fel_dur = lognorm(rr, 125, 0.6, 10, 700)
    held_plea = lognorm(rr, 16, 0.7, 3, 120)
    later_post = (not released24) and (not detainer) and rr.random() < L_POST[1 if D else 0]
    later_days = lognorm(rr, 6, 0.7, 3, 60)
    indicted = felony and rr.random() < (0.85 if top == "FX" else 0.55)
    ind_day = int(rr.integers(18, 76))
    sup_dur = lognorm(rr, 240, 0.5, 40, 900)
    case_recs = []
    for gi, g in enumerate(groups):
        gfel = any(C.BY_CODE[c][5] in ("FH", "FX") for c in g)
        if gfel and indicted:
            ddate = fa.date() + dt.timedelta(days=ind_day)
            while ddate.weekday() >= 5:
                ddate -= DAY
            code = "IND"
        elif released24 or later_post:
            dur = fel_dur if gfel else misd_dur_rel
            ddate = fa.date() + dt.timedelta(days=int(dur))
            code = None
        else:
            dur = (lognorm(rr, 60, 0.6, 10, 400) if gfel else held_plea)
            ddate = fa.date() + dt.timedelta(days=int(dur))
            code = None
        cr = dict(cid=len(cases), eid=eid, pid=p.pid, court="D", filed=fa, codes=g, felony=gfel, disposed=ddate,
                  code=code, parent=None)
        cases.append(cr)
        case_recs.append(cr)
        if gfel and indicted:
            sc = dict(cid=len(cases), eid=eid, pid=p.pid, court="S", filed=K.d2dt(ddate, 9) + dt.timedelta(minutes=int(rr.integers(0, 420))),
                      codes=g, felony=True, disposed=ddate + dt.timedelta(days=int(sup_dur)), code=None, parent=cr["cid"])
            cases.append(sc)
            case_recs.append(sc)
    for c in case_recs:
        while c["disposed"].weekday() >= 5:
            c["disposed"] += DAY
    last_disp = max(c["disposed"] for c in case_recs)
    # disposition codes and convictions
    for c in case_recs:
        if c["code"] is None:
            held_case = not (released24 or later_post)
            if held_case:
                c["code"] = str(rr.choice(["GP", "VD", "GP", "GP", "DD"], p=[0.5, 0.2, 0.1, 0.1, 0.1]))
            else:
                c["code"] = str(rr.choice(["GP", "VD", "DD", "GT", "NG"], p=[0.50, 0.33, 0.08, 0.06, 0.03]))
        if c["code"] in ("GP", "GT") and c["disposed"] <= K.EXTRACT_END:
            if c["felony"]:
                p.fel_conv.append(c["disposed"])
            else:
                p.misd_conv.append(c["disposed"])
            if any(C.BY_CODE[x][6] for x in c["codes"]):
                p.viol_conv.append(c["disposed"])
            if c["felony"] and rr.random() < 0.35:
                p.incarc.append(c["disposed"])
    for c in case_recs:
        p.open_cases.append((fa.date(), c["disposed"]))
    # custody
    if released24:
        free_t = rel_t
        rel_type = {"WRITTEN_PROMISE": "WPA", "UNSECURED": "UNSEC", "CUSTODY": "CUST", "SECURED": "BOND"}[cond]
    elif detainer:
        free_t = fa + dt.timedelta(hours=int(rr.integers(10, 60)))
        rel_type = "XFER"
    elif later_post:
        free_t = fa + dt.timedelta(days=later_days, minutes=int(rr.integers(0, 600)))
        rel_type = "BOND"
    else:
        hold_end = last_disp if not indicted else min(last_disp, fa.date() + dt.timedelta(days=int(lognorm(rr, 70, 0.6, 15, 400))))
        free_t = K.d2dt(hold_end, int(rr.integers(10, 18)), int(rr.integers(0, 60)))
        if free_t <= fa:
            free_t = fa + dt.timedelta(hours=30)
        rel_type = "TS" if any(c["code"] in ("GP", "GT") for c in case_recs) else "DISM"
    stays = custody(rr, p, booking, free_t, rel_type, released24)
    # the at-risk process after release
    h = (HAZ1 if D else HAZ0)[nca - 1] * p.mult
    next_t = free_t + dt.timedelta(minutes=int(rr.exponential(1 / h) * 1440))
    # the window: from release (first appearance or later) to 365 days or the last charge's disposition
    e = dict(eid=eid, pid=p.pid, arrest_t=t, booking_t=booking, screened=screened, screen_t=screen_t, fa_t=fa,
             mag=mag, lam=lam, codes=codes, top=top, detainer=detainer, eligible=eligible, D=D, nca=nca,
             nca_items=nca_it, nca_raw=nca_raw, pending=int(pending), cond=cond, bond=bond, secured=secured,
             posted=posted, released24=released24, rel_t=rel_t, free_t=free_t, rel_type=rel_type,
             cases=[c["cid"] for c in case_recs], last_disp=last_disp, indicted=indicted, stays=stays,
             next_t=next_t, misd_dur_rel=misd_dur_rel)
    # the counterfactual (the clean truth only): a new-offence arrest within the window had the defendant been
    # released at first appearance, with a released defendant's case length
    if released24:
        e["cf"] = None
    else:
        cr2 = K.rng("cf", p.pid, ak)
        wdays = min(K.WINDOW_DAYS, misd_dur_rel if not felony else fel_dur)
        e["cf"] = bool(cr2.exponential(1 / h) < wdays)
    return e


def custody(rr, p, booking, free_t, rel_type, released24):
    """The jail's custody segments for one stay: the booking at intake, an annex move, a boarding at Halsey and a
    return. Each segment: (start, end, booking_type, release_type, facility, where)."""
    segs = []
    start = booking
    if released24:
        return [dict(pid=p.pid, start=booking, end=free_t, btype="NEW", rtype=rel_type, fac="DCDC", where="DC")]
    t = booking
    fac = "DCDC"
    btype = "NEW"
    length = (free_t - booking).total_seconds() / 86400
    if length > 4 and rr.random() < P_ANNEX:
        mv = booking + dt.timedelta(days=float(rr.uniform(2.0, 4.0)))
        mv = mv.replace(second=0, microsecond=0)
        segs.append(dict(pid=p.pid, start=t, end=mv, btype=btype, rtype="TRF", fac=fac, where="DC"))
        t, fac, btype = mv, "DCDC-ANNEX", "TRF"
    bday = (t + dt.timedelta(days=float(rr.uniform(1.0, 6.0)))).date()
    bstart = K.d2dt(bday, int(rr.integers(8, 16)), int(rr.integers(0, 60)))
    if (free_t - t).total_seconds() / 86400 > 3 and bstart.date() >= K.BOARDING_START and bstart > t \
            and bstart < free_t - dt.timedelta(days=1) and rr.random() < P_BOARD:
        segs.append(dict(pid=p.pid, start=t, end=bstart, btype=btype, rtype="BO", fac=fac, where="DC"))
        if rr.random() < P_RETURN and (free_t - bstart).total_seconds() / 86400 > 6:
            span = (free_t - bstart).total_seconds() / 86400
            bk = (bstart + dt.timedelta(days=float(rr.uniform(3.0, max(3.5, min(45.0, span - 1)))))).date()
            back = K.d2dt(bk, int(rr.integers(9, 17)), int(rr.integers(0, 60)))
            if back >= free_t:
                back = free_t - dt.timedelta(hours=6)
            segs.append(dict(pid=p.pid, start=bstart, end=back, btype=None, rtype=None, fac="HALSEY", where="HC"))
            segs.append(dict(pid=p.pid, start=back, end=free_t, btype="BI", rtype=rel_type, fac="DCDC", where="DC"))
        else:
            segs.append(dict(pid=p.pid, start=bstart, end=free_t, btype=None, rtype=rel_type, fac="HALSEY", where="HC"))
    else:
        segs.append(dict(pid=p.pid, start=t, end=free_t, btype=btype, rtype=rel_type, fac=fac, where="DC"))
    return segs


# ---------------------------------------------------------------------------------------------------- the courts
def court_dates(W):
    """Every case's court dates to its disposition: a district setting 18 to 35 days after the first appearance and
    every four to eight weeks after, a superior court arraignment 25 to 50 days after the indictment and every five to
    nine weeks after."""
    r = K.rng("courtdates")
    W.court = []
    for c in W.cases:
        e = W.eps[c["eid"]]
        start = c["filed"].date() + dt.timedelta(days=int(r.integers(18, 36) if c["court"] == "D" else r.integers(25, 51)))
        d = start
        while d < c["disposed"]:
            if d.weekday() >= 5:
                d += dt.timedelta(days=7 - d.weekday())
            if d >= c["disposed"]:
                break
            W.court.append(dict(cid=c["cid"], date=d, eid=c["eid"], pid=c["pid"], fta=False))
            d += dt.timedelta(days=int(r.integers(28, 57) if c["court"] == "D" else r.integers(35, 64)))


def finish_ftas(W):
    """Failures to appear, in time order per person: a court date the defendant is at liberty for is missed with the
    probability his failure-to-appear score carries; the score at each first appearance counts the failures before it.
    In custody on the day (a later stay), the jail brings him and the date is kept."""
    r = K.rng("ftas", OFFSETS["fta"])
    for cd in W.court:
        cd["fta"] = False
    by_p = {}
    for e in W.eps:
        by_p.setdefault(e["pid"], []).append(("fa", e["fa_t"], e["eid"]))
    for k, cd in enumerate(W.court):
        by_p.setdefault(cd["pid"], []).append(("cd", K.d2dt(cd["date"], 9), k))
    custody_by_p = {}
    for s in W.stays:
        custody_by_p.setdefault(s["pid"], []).append((s["start"], s["end"]))
    persons = W.persons
    for pid, evs in by_p.items():
        p = persons[pid]
        p.ftas = []
        evs.sort(key=lambda x: (x[1], 0 if x[0] == "fa" else 1))
        cust = custody_by_p.get(pid, [])
        for kind, t, k in evs:
            if kind == "fa":
                e = W.eps[k]
                it, raw, sc = fta_items_at(p, t, e["pending"], e["nca_items"])
                e["fta_items"], e["fta_raw"], e["fta"] = it, raw, sc
            else:
                cd = W.court[k]
                e = W.eps[cd["eid"]]
                if any(a <= t <= b for a, b in cust):
                    continue
                pf = FTA_P[e["fta"] - 1] * (1.35 if e["D"] else 1.0)
                if r.random() < pf:
                    cd["fta"] = True
                    p.ftas.append(cd["date"])


def monitoring(W):
    """Electronic monitoring for released defendants with the condition: an enrollment from the day after release
    (or a few days on) to the disposition, a violation or the extract; each equipment change ends the enrollment
    and opens another under a new participant number the same day."""
    r = K.rng("em", OFFSETS["em"])
    W.em = []
    for e in W.eps:
        if not e["released24"] or e["fa_t"].date() < K.FY26_START or e["fa_t"].date() > K.EXTRACT_END:
            continue
        pe = EM_P["M"][e["nca"] - 1] if e["top"] == "M" else EM_P[e["top"]]
        if r.random() >= pe:
            continue
        start = e["rel_t"].date() + dt.timedelta(days=int(r.choice([0, 1, 1, 2, 3])))
        end = min(e["last_disp"], e["next_t"].date())
        if r.random() < 0.18:
            end = min(end, start + dt.timedelta(days=int(r.integers(10, 90))))
        if end <= start:
            continue
        seg_start = start
        while True:
            days_left = (end - seg_start).days
            gap = int(r.exponential(1 / SWAP_RATE))
            if gap >= days_left or seg_start + dt.timedelta(days=gap) > K.EXTRACT_END:
                W.em.append(dict(eid=e["eid"], pid=e["pid"], start=seg_start, end=end if end <= K.EXTRACT_END else None))
                break
            swap = seg_start + dt.timedelta(days=max(1, gap))
            W.em.append(dict(eid=e["eid"], pid=e["pid"], start=seg_start, end=swap))
            seg_start = swap
