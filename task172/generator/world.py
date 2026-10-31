"""TALON-2's world: the sites, every screening attempt, the randomised patients, their progression, scans,
treatment, laboratory samples and serious adverse events, up to the interim data cut and the snapshot taken for
the data monitoring committee. Everything is drawn from one seed; nothing here is read by the solver."""
import datetime as dt
import math

import numpy as np

SEED = 24
N_TARGET = 450
FINAL_EVENTS = 330
INTERIM_EVENTS = 165
MONTH = 30.4375
FPI = dt.date(2025, 6, 2)          # first patient randomised (a Monday); shifted by whole weeks to place the cut
ENROL_DAYS = 300
SHAPE = 1.2
MED_C = 7.0                        # control median PFS, months
HR_E, HR_L, T_SWITCH = 1.00, 0.45, 89   # ravolimab against placebo before and after day 89
DEATH_RATE = 0.0085                # deaths before progression, per month, both arms
DROP_RATE = 0.0045                 # withdrawal or loss to follow-up, per month
SNAPSHOT_LAG = 14                  # days from the cut to the DMC snapshot
STRATA_DS = ("Initially unresectable", "Recurrent")
STRATA_PS = ("Intrahepatic cholangiocarcinoma", "Extrahepatic cholangiocarcinoma", "Gallbladder cancer")
P_DS = (0.78, 0.22)
P_PS = (0.55, 0.20, 0.25)
HR_DS = (1.0, 0.74)
HR_PS = (1.0, 0.95, 1.30)

# country, code, sites, weight per site, first activation day, last activation day
COUNTRIES = [
    ("United Kingdom", "GB", 14, 0.85, 0, 70), ("Australia", "AU", 10, 0.80, 10, 90),
    ("New Zealand", "NZ", 3, 0.70, 20, 100), ("Ireland", "IE", 2, 0.75, 25, 110),
    ("France", "FR", 3, 1.00, 30, 110), ("Spain", "ES", 4, 1.00, 30, 100),
    ("Italy", "IT", 3, 0.95, 40, 120), ("Germany", "DE", 3, 0.90, 45, 125),
    ("Netherlands", "NL", 2, 0.95, 40, 110), ("Belgium", "BE", 2, 0.85, 50, 130),
    ("Poland", "PL", 2, 1.10, 55, 135), ("Czechia", "CZ", 1, 1.00, 60, 140),
    ("Sweden", "SE", 2, 0.95, 45, 120), ("Norway", "NO", 1, 0.90, 55, 130),
]
CITIES = {
    "GB": ["Kesterton", "Leeds", "Glasgow", "Birmingham", "Southampton", "Newcastle", "Cardiff", "Oxford", "Nottingham",
           "Sheffield", "Bristol", "Edinburgh", "Manchester", "Plymouth"],
    "AU": ["Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide", "Hobart", "Newcastle NSW", "Geelong", "Gold Coast",
           "Canberra"],
    "NZ": ["Auckland", "Christchurch", "Wellington"], "IE": ["Dublin", "Cork"], "FR": ["Lyon", "Lille", "Bordeaux"],
    "ES": ["Madrid", "Barcelona", "Valencia", "Seville"], "IT": ["Milan", "Bologna", "Rome"],
    "DE": ["Heidelberg", "Hamburg", "Munich"], "NL": ["Amsterdam", "Rotterdam"], "BE": ["Leuven", "Ghent"],
    "PL": ["Warsaw", "Gdansk"], "CZ": ["Prague"], "SE": ["Gothenburg", "Uppsala"], "NO": ["Oslo"],
}


def day(d0, n):
    return d0 + dt.timedelta(days=int(n))


def weekday_fix(d, back=False):
    """Move a weekend date onto a working day (Saturday to Friday, Sunday to Monday)."""
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1) if not back else d - dt.timedelta(days=2)
    return d


def sites(rng):
    out = []
    for country, code, n, w, a0, a1 in COUNTRIES:
        for i in range(n):
            act = int(a0 + (a1 - a0) * (i / max(n - 1, 1)) ** 1.3 + rng.integers(0, 15))
            out.append(dict(site_id="%s%02d" % (code, i + 1), country=country, code=code,
                            city=CITIES[code][i], weight=w * rng.uniform(0.6, 1.5), activation=act))
    return out


def piece_time(u, lam, hr_e, hr_l, start, t_switch=None):
    """Event time on a piecewise hazard (switch at t_switch), from follow-up time start, for unit-exponential u."""
    T_SWITCH_ = T_SWITCH if t_switch is None else t_switch
    le, ll = lam * hr_e, lam * hr_l
    t = np.empty_like(u)
    in_e = start < T_SWITCH_
    cap = np.where(in_e, le * (T_SWITCH_ - start), 0.0)
    a = in_e & (u < cap)
    t[a] = start[a] + u[a] / le[a]
    b = ~a
    base = np.where(in_e, T_SWITCH_, start)
    t[b] = base[b] + (u[b] - cap[b]) / ll[b]
    return t


def schedule_days(rng, horizon):
    """Scheduled tumour assessments: every 6 weeks to week 24, then every 8 weeks; +-5 day windows."""
    nominal = [42 * k for k in range(1, 5)] + list(range(168 + 56, int(horizon) + 400, 56))
    out = []
    for k, d in enumerate(nominal):
        out.append((k + 1, d, d + int(rng.integers(-5, 6))))
    return out


def visit_name(k, d):
    return "Week %d" % (d // 7)


class World:
    def __init__(self, seed=SEED, hr_e=HR_E, hr_l=HR_L, med_c=MED_C, enrol_days=ENROL_DAYS, shape=SHAPE, t_switch=T_SWITCH):
        self.seed = seed
        rng = np.random.default_rng(seed)
        self.rng = rng
        self.sites = sites(rng)
        lam0 = math.log(2) / (med_c * MONTH)
        # randomisation days: ramp (beta-like) over enrol_days, each patient at an active site
        u = np.sort(rng.uniform(0, 1, N_TARGET))
        rdays = np.floor(enrol_days * u ** (1 / shape)).astype(int)
        rdays = np.array([(weekday_fix(day(FPI, r)) - FPI).days for r in rdays])
        w = np.array([s["weight"] for s in self.sites])
        act = np.array([s["activation"] for s in self.sites])
        pts = []
        block = {}
        for i, rd in enumerate(rdays):
            ok = act <= rd
            if not ok.any():
                ok = act == act.min()
            p = w * ok
            si = int(rng.choice(len(self.sites), p=p / p.sum()))
            ds = int(rng.choice(2, p=P_DS))
            ps = int(rng.choice(3, p=P_PS))
            key = (ds, ps)
            if not block.get(key):
                b = [0, 0, 1, 1]
                rng.shuffle(b)
                block[key] = b
            arm = block[key].pop()
            pts.append(dict(i=i, rday=int(rd), site=si, ds=ds, ps=ps, arm=arm))
        self.pts = pts
        n = len(pts)
        arm = np.array([p["arm"] for p in pts])
        mult = np.array([HR_DS[p["ds"]] * HR_PS[p["ps"]] for p in pts])
        lam = lam0 * mult
        up = rng.exponential(1.0, n)
        hre = np.where(arm == 1, hr_e, 1.0)
        hrl = np.where(arm == 1, hr_l, 1.0)
        tprog = piece_time(up, lam, hre, hrl, np.zeros(n), t_switch)
        tdeath = rng.exponential(MONTH / DEATH_RATE, n)
        tdrop = rng.exponential(MONTH / DROP_RATE, n)
        self.lam0 = lam0
        for k, p in enumerate(pts):
            p.update(tprog=float(tprog[k]), tdeath=float(tdeath[k]), tdrop=float(tdrop[k]), lam=float(lam[k]))
        # tumour assessments and the BICR's reading of each
        for p in pts:
            sched = schedule_days(rng, 900)
            sched = [(k, nom, (weekday_fix(day(FPI, p["rday"] + act)) - FPI).days - p["rday"]) for k, nom, act in sched]
            scans = []
            missed_run = 0
            pd_found = None
            for k, nominal, actual in sched:
                if actual >= min(p["tdeath"], p["tdrop"]):
                    break
                if rng.uniform() < 0.025:
                    # images not received or not readable: the BICR records the timepoint as not evaluable
                    scans.append(dict(k=k, nominal=nominal, day=actual, done=True, resp="NE"))
                    continue
                if actual >= p["tprog"]:
                    resp = "PD" if rng.uniform() < 0.97 or any(s.get("resp") == "NE*" for s in scans) else "NE*"
                else:
                    r = rng.uniform()
                    resp = "NE" if r < 0.015 else ("PR" if r < 0.015 + 0.22 * min(1, actual / 120) else "SD")
                    if resp == "PR" and actual > 200 and rng.uniform() < 0.15:
                        resp = "CR"
                scans.append(dict(k=k, nominal=nominal, day=actual, done=True, resp=resp))
                if resp == "PD":
                    pd_found = actual
                    break
            for s in scans:
                if s.get("resp") == "NE*":
                    s["resp"] = "NE"
            p["scans"] = scans
            p["pd_day"] = pd_found
        self._place_cut()

    def _place_cut(self):
        """The CTU counts events the way the SAP does; the cut is the day of the 165th, shifted onto a weekday
        calendar so that it falls within a few days of 16 November 2026."""
        evs = []
        for p in self.pts:
            t, kind = self.event_day(p)
            if t is not None:
                evs.append(p["rday"] + t)
        evs.sort()
        cut_rel = evs[INTERIM_EVENTS - 1]
        # the cut must not tie with the 166th event
        self.tie_ok = evs[INTERIM_EVENTS] > cut_rel
        target = dt.date(2026, 11, 16)
        shift = (target - day(FPI, cut_rel)).days
        shift = 7 * round(shift / 7)
        self.fpi = day(FPI, shift)
        self.cut_rel = cut_rel
        self.cut = day(self.fpi, cut_rel)
        self.snapshot = day(self.cut, SNAPSHOT_LAG)

    @staticmethod
    def event_day(p, cut_rel=None):
        """PFS under the SAP from the truth: (day, kind) or (None, censor day) within an optional cut."""
        scans = [s for s in p["scans"] if cut_rel is None or p["rday"] + s["day"] <= cut_rel]
        last_adequate = 0
        missed = 0
        for s in scans:
            if s["resp"] == "NE":
                missed += 1
                continue
            if s["resp"] == "PD":
                if missed >= 2:
                    return None, last_adequate
                return s["day"], "PD"
            last_adequate = s["day"]
            missed = 0
        # death before progression
        dday = int(math.floor(p["tdeath"]))
        if p["tdeath"] < p["tdrop"] and (p["pd_day"] is None or dday < p["pd_day"]):
            if cut_rel is None or p["rday"] + dday <= cut_rel:
                # missed assessments before death: two scheduled scans passed since the last adequate one
                passed = [s for s in p["scans"] if s["day"] < dday and s["day"] > last_adequate]
                run = 0
                for s in passed:
                    run = run + 1 if s["resp"] == "NE" else 0
                if run >= 2:
                    return None, last_adequate
                return dday, "Death"
        return None, last_adequate


if __name__ == "__main__":
    w = World()
    print("fpi", w.fpi, "cut", w.cut, "tie_ok", w.tie_ok)
