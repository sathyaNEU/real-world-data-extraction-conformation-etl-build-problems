"""The world behind task236's pack: each region's influenza, RSV and other respiratory illness by day of onset, the day
the ill reach a general practitioner, an emergency department or a drive-through clinic, who is tested there and by
which method under each region's testing regime, and the sentinel practices' influenza-like-illness consultations and
protocol swabs, which come from the same general practice visits. The clean truth (each region's share of influenza
infections notified under each regime) stays here for the checks."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

ILLS = ("flu", "rsv", "oth")


def iso_week_start(week, year=2027):
    return dt.date.fromisocalendar(year, week, 1)


def days(lead=7):
    """the simulated days: a week of onsets before the pack's first day, so care in the first week has its ill"""
    start = P.D0 - dt.timedelta(days=lead)
    n = (P.D1 - start).days + 1
    return [start + dt.timedelta(days=i) for i in range(n)]


def curve(ds, peak_week, total_thousands, sd_days):
    """an epidemic's symptomatic onsets per day: a bell around the peak, the season's total in thousands"""
    peak = iso_week_start(int(peak_week)) + dt.timedelta(days=(peak_week - int(peak_week)) * 7 + 3)
    x = np.array([(d - peak).days for d in ds], dtype=float)
    return total_thousands * 1000.0 * np.exp(-0.5 * (x / sd_days) ** 2) / (sd_days * np.sqrt(2 * np.pi))


def to_care(onset, ds, delays, open_days):
    """move onsets to the day care is reached: a delay drawn from `delays` (days: share), and a closed day passing
    its visits on to the next open day"""
    out = np.zeros_like(onset)
    n = len(ds)
    for lag, share in delays.items():
        for i in range(n - lag):
            j = i + lag
            while j < n and ds[j].weekday() not in open_days:
                j += 1
            if j < n:
                out[j] += onset[i] * share
    return out


GP_DELAY = {1: 0.35, 2: 0.40, 3: 0.25}
ED_DELAY = {1: 0.30, 2: 0.42, 3: 0.28}
DT_DELAY = {1: 0.34, 2: 0.41, 3: 0.25}
GP_OPEN = {0, 1, 2, 3, 4, 5}         # general practices open Monday to Saturday
ED_OPEN = {0, 1, 2, 3, 4, 5, 6}
DT_OPEN = {0, 1, 2, 3, 4, 5}          # the clinics close on Sundays


def ascertainment(code, regime):
    """the expected share of a region's symptomatic influenza infections that a positive test notifies, by regime"""
    r = {x[0]: x for x in P.REGIONS}[code]
    dts = r[10]
    gp, ed = P.CARE["flu"]["gp"], P.CARE["flu"]["ed"]
    s = P.SENS
    gp_part = gp * P.TEST["gp"]["flu"] * s["pcr"]
    if regime == "poc":
        gp_part = gp * (P.TEST["gp"]["flu"] * P.POC_PCR_DROP * s["pcr"] + P.POC["flu"] * s["poc"])
    ed_part = ed * (P.PANEL["flu"] * s["panel"] if regime == "panel" else P.TEST["ed"]["flu"] * s["pcr"])
    dt_part = dts * P.TEST["dt"]["flu"] * s["pcr"] * (P.HOURS_DT if regime == "hours" else 1.0)
    if regime == "closure":
        dt_part = 0.0
        gp_part += P.CLOSURE_TO_GP * dts * P.TEST["gp"]["flu"] * s["pcr"]
    return gp_part + ed_part + dt_part


class World:
    def __init__(self, seed=P.WORLD_SEED):
        self.rng = np.random.default_rng(seed)
        self.ds = days()
        self.regions = {r[0]: r for r in P.REGIONS}

    def illness(self):
        """onsets per day, and the visits each setting receives per day"""
        out, care = {}, {}
        doy = np.array([d.timetuple().tm_yday for d in self.ds], dtype=float)
        for code, name, pop, fp, ft, fsd, rp, rt, rsd, oth, dts in P.REGIONS:
            on = {"flu": curve(self.ds, fp, ft, fsd), "rsv": curve(self.ds, rp, rt, rsd),
                  "oth": oth * pop / 1000.0 * (1 + 0.22 * np.cos(2 * np.pi * (doy - 196) / 365.0))}
            out[code] = on
            care[code] = {}
            for k in ILLS:
                care[code][k] = {"gp": to_care(P.CARE[k]["gp"] * on[k], self.ds, GP_DELAY, GP_OPEN),
                                 "ed": to_care(P.CARE[k]["ed"] * on[k], self.ds, ED_DELAY, ED_OPEN),
                                 "dt": to_care(dts * on[k], self.ds, DT_DELAY, DT_OPEN)}
        self.onsets, self.care = out, care
        return out

    def regime(self, code, d):
        ch = P.CHANGES.get(code)
        return ch[1] if ch and d >= ch[0] else None

    def tests(self):
        """tests per care day by region, illness, setting and method, drawn from each regime's testing rates"""
        rows = []
        rng = self.rng
        for code in self.regions:
            for i, d in enumerate(self.ds):
                if d < P.D0:
                    continue
                reg = self.regime(code, d)
                for k in ILLS:
                    c = self.care[code][k]
                    gp, ed, dtc = c["gp"][i], c["ed"][i], c["dt"][i]
                    lam = {}
                    gp_pcr = gp * P.TEST["gp"][k]
                    if reg == "poc":
                        lam[("gp", "poc")] = gp * P.POC[k]
                        gp_pcr *= P.POC_PCR_DROP
                    if reg == "closure":
                        gp_pcr += P.CLOSURE_TO_GP * dtc * P.TEST["gp"][k]
                    else:
                        lam[("dt", "pcr")] = dtc * P.TEST["dt"][k] * (P.HOURS_DT if reg == "hours" else 1.0)
                    lam[("gp", "pcr")] = gp_pcr
                    if reg == "panel":
                        lam[("ed", "panel")] = ed * P.PANEL[k]
                    else:
                        lam[("ed", "pcr")] = ed * P.TEST["ed"][k]
                    for (setting, method), x in sorted(lam.items()):
                        cnt = int(rng.poisson(x))
                        if not cnt:
                            continue
                        p = P.SENS[method] if k == "flu" else P.FALSE_POS[method]
                        rows.append((code, d, k, setting, method, cnt, int(rng.binomial(cnt, p))))
        self.test_counts = pd.DataFrame(rows, columns=["region", "date", "illness", "setting", "method", "tested", "positive"])
        return self.test_counts

    def sentinel(self):
        """each sentinel practice's week: its general practice visits for each illness (the region's visits in the
        practice's share of the population), those meeting the influenza-like-illness definition, the protocol
        swabs (the first two such patients each weekday) and each swab's virus"""
        rng = self.rng
        rows, swabs = [], []
        weeks = sorted({d.isocalendar()[1] for d in self.ds if d >= P.D0})
        widx = {w: [i for i, d in enumerate(self.ds) if d >= P.D0 and d.isocalendar()[1] == w] for w in weeks}
        for code, name, pop, *_ in P.REGIONS:
            n_pr = P.SENTINEL_PRACTICES[code]
            sizes = rng.integers(4200, 15800, size=n_pr)
            for j in range(n_pr):
                share = sizes[j] / pop
                for w in weeks:
                    lam = {k: share * sum(self.care[code][k]["gp"][i] for i in widx[w]) for k in ILLS}
                    ili = {k: int(rng.poisson(lam[k] * P.ILI_DEF[k])) for k in ILLS}
                    total_ili = sum(ili.values())
                    allc = int(rng.poisson(sizes[j] * 0.052 + sum(lam.values()) * 0.9))
                    returned = bool(rng.random() >= P.SENTINEL_MISS)
                    n_sw = min(total_ili, P.SWAB_CAP)
                    got = rng.multivariate_hypergeometric([ili[k] for k in ILLS], n_sw) if n_sw else [0, 0, 0]
                    rows.append((code, j, int(sizes[j]), w, allc + total_ili, total_ili, returned, n_sw))
                    for kk, cnt in enumerate(got):
                        k = ILLS[kk]
                        for _ in range(int(cnt)):
                            flu_pos = rng.random() < (P.SENS["pcr"] if k == "flu" else P.FALSE_POS["pcr"])
                            swabs.append((code, j, w, k, bool(flu_pos)))
        self.practices = pd.DataFrame(rows, columns=["region", "practice", "list_size", "week", "consultations", "ili",
                                                     "returned", "swabs"])
        self.swabs = pd.DataFrame(swabs, columns=["region", "practice", "week", "illness", "flu_positive"])
        return self.practices, self.swabs

    def truth(self):
        """each changed region's share notified under its new regime over its old one, from the testing rates"""
        out = {}
        for code, (when, kind, text) in P.CHANGES.items():
            out[code] = ascertainment(code, kind) / ascertainment(code, None)
        return out


def make(seed=P.WORLD_SEED):
    W = World(seed)
    W.illness()
    W.tests()
    W.sentinel()
    return W
