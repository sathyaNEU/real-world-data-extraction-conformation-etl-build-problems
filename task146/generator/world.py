"""task146 architecture 3: the HB-231 world. The VELA-2 phase 2b trial (Nordic sites) and the VELA-3 phase 3
feasibility candidates (North American sites). Every recorded number is accurate; the truth below is what the
records are drawn from.

Truth: clearance rises with body weight, CL = 0.32 L/day x (W/85)^1.1 x exp(eta); the week-16 trough follows the
dose over clearance; PASI 75 at week 16 follows the trough through an Emax curve; rescue and early discontinuation
count as non-response (the SAP's composite)."""
import datetime as dt
import math

import numpy as np

SEED = 23146
ARMS = [("PBO", 0), ("HB25", 25), ("HB50", 50), ("HB100", 100), ("HB200", 200)]
PER_ARM = 100
CL0, WEXP, OMEGA, RESID = 0.32, 1.1, 0.28, 0.14
ACC = {4: 0.62, 8: 0.85, 12: 0.94, 16: 0.98}
E0, EMAX, EC50, HILL = 0.05, 0.95, 5.4, 2.7
SIGMA = 1.55           # spread of the latent improvement
LLOQ = 0.10            # micrograms per mL
FIRST = dt.date(2025, 9, 1)
LAST = dt.date(2026, 2, 27)

SITES = [  # code, country, city, timezone, PASI recorded as, eCRF build
    ("DK01", "DK", "Copenhagen (Bispebjerg)", "Europe/Copenhagen", "dec", "std"),
    ("DK02", "DK", "Copenhagen (Gentofte)", "Europe/Copenhagen", "dec", "std"),
    ("DK03", "DK", "Aarhus", "Europe/Copenhagen", "dec", "std"),
    ("DK04", "DK", "Odense", "Europe/Copenhagen", "int", "std"),
    ("DK05", "DK", "Aalborg", "Europe/Copenhagen", "dec", "std"),
    ("DK06", "DK", "Roskilde", "Europe/Copenhagen", "int", "std"),
    ("DK07", "DK", "Vejle", "Europe/Copenhagen", "dec", "std"),
    ("SE01", "SE", "Stockholm (Karolinska)", "Europe/Stockholm", "dec", "std"),
    ("SE02", "SE", "Stockholm (Danderyd)", "Europe/Stockholm", "dec", "std"),
    ("SE03", "SE", "Gothenburg", "Europe/Stockholm", "int", "std"),
    ("SE04", "SE", "Malmo", "Europe/Stockholm", "dec", "std"),
    ("SE05", "SE", "Lund", "Europe/Stockholm", "dec", "std"),
    ("SE06", "SE", "Uppsala", "Europe/Stockholm", "dec", "std"),
    ("SE07", "SE", "Linkoping", "Europe/Stockholm", "int", "std"),
    ("FI01", "FI", "Helsinki", "Europe/Helsinki", "dec", "fi"),
    ("FI02", "FI", "Tampere", "Europe/Helsinki", "dec", "fi"),
    ("FI03", "FI", "Turku", "Europe/Helsinki", "int", "fi"),
    ("FI04", "FI", "Oulu", "Europe/Helsinki", "dec", "fi"),
    ("NO01", "NO", "Oslo", "Europe/Oslo", "dec", "no"),
    ("NO02", "NO", "Bergen", "Europe/Oslo", "dec", "no"),
    ("NO03", "NO", "Trondheim", "Europe/Oslo", "int", "no"),
]
SITE_WEIGHT = [7, 6, 6, 5, 5, 4, 4, 7, 6, 6, 5, 5, 4, 4, 8, 7, 6, 6, 7, 6, 5]


def p75(c):
    c = np.maximum(c, 0.0)
    return E0 + (EMAX - E0) * c ** HILL / (EC50 ** HILL + c ** HILL)


IMP_LO, IMP_SPAN = -0.15, 1.15     # improvement = IMP_LO + IMP_SPAN * sigmoid(L)


def thr(frac):
    """The latent L at which the improvement reaches frac."""
    s = (frac - IMP_LO) / IMP_SPAN
    return math.log(s / (1 - s))


T75, T90 = thr(0.75), thr(0.90)


def norm_ppf(p):
    from statistics import NormalDist
    return NormalDist().inv_cdf(min(max(p, 1e-9), 1 - 1e-9))


class World:
    def __init__(self, seed=SEED):
        r = np.random.default_rng(seed)
        self.r = r
        self.sites = SITES
        n = PER_ARM * len(ARMS)
        # randomisation: permuted blocks of five across the enrolment window, sites by weight
        arms = []
        for b in range(n // 5):
            blk = [a for a, _ in ARMS]
            r.shuffle(blk)
            arms += blk
        days = sorted(r.integers(0, (LAST - FIRST).days + 1, n))
        site_p = np.array(SITE_WEIGHT, float) / sum(SITE_WEIGHT)
        self.pat = []
        dose_of = dict(ARMS)
        for i in range(n):
            s = SITES[int(r.choice(len(SITES), p=site_p))]
            sex = "M" if r.random() < 0.62 else "F"
            mean_w = 90.0 if sex == "M" else 74.0
            w = float(np.exp(r.normal(math.log(mean_w) - 0.015, 0.17)))
            h = float(r.normal(179 if sex == "M" else 166, 7))
            age = int(min(78, max(18, r.normal(45, 13))))
            pasi0 = float(min(48, max(12.0, r.gamma(6.0, 3.4))))
            eta = float(r.normal(0, OMEGA))
            arm = arms[i]
            d = dose_of[arm]
            rdate = FIRST + dt.timedelta(days=int(days[i]))
            # first dose: the randomisation day, except at the Norwegian sites, whose hospital pharmacies dispensed
            # one to three working days later
            lag = int(r.integers(2, 7)) if s[1] == "NO" else 0
            d1 = rdate + dt.timedelta(days=lag)
            cl = CL0 * (w / 85.0) ** WEXP * math.exp(eta)
            c16_true = d * ACC[16] / (cl * 28.0)
            p = float(p75(np.array([c16_true]))[0]) if d > 0 else E0
            a = T75 + SIGMA * norm_ppf(p)
            L = a + SIGMA * float(r.normal())
            imp = IMP_LO + IMP_SPAN / (1 + math.exp(-L))
            disc = r.random() < (0.07 if d == 0 else 0.035)
            resc = (not disc) and r.random() < (0.11 if d == 0 else 0.03) * (1.6 if imp < 0.5 else 0.6)
            self.pat.append({"i": i, "site": s[0], "country": s[1], "tz": s[3], "pasi_fmt": s[4], "ecrf": s[5],
                             "arm": arm, "dose": d, "sex": sex, "weight": w, "height": h, "age": age,
                             "pasi0": pasi0, "eta": eta, "cl": cl, "c16_true": c16_true, "p75_true": p,
                             "imp16": imp, "disc": bool(disc), "resc": bool(resc), "rdate": rdate, "d1": d1,
                             "prior_bio": bool(r.random() < 0.31)})
        self.cand = self._phase3(r)

    def _phase3(self, r):
        """The VELA-3 feasibility survey: candidates the North American sites listed from their own records."""
        out = []
        sites = [("US%02d" % k, "US") for k in range(1, 27)] + [("CA%02d" % k, "CA") for k in range(1, 9)]
        for code, ctry in sites:
            m = int(r.integers(22, 48))
            for _ in range(m):
                sex = "M" if r.random() < 0.58 else "F"
                mean_w = 117.0 if sex == "M" else 102.0
                w = float(np.exp(r.normal(math.log(mean_w) - 0.02, 0.21)))
                w = min(w, 182.0)
                out.append({"site": code, "country": ctry, "sex": sex, "weight": w,
                            "age": int(min(80, max(18, r.normal(48, 13)))),
                            "pasi": float(min(50, max(12.0, r.gamma(6.2, 3.3)))),
                            "prior_bio": bool(r.random() < 0.36)})
        return out
