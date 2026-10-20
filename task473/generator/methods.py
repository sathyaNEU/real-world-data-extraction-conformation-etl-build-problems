"""Every completion of the untested drivers, on one observed structure the truth and the pack's readers both build:

    crash = {"fips", "year", "deaths", "drivers": [{"killed", "identified", "tested", "bac", "arrested",
              "complete"}]}

`complete` marks a surviving driver of an agency that tests every surviving driver (the State Patrol and the
Corwin and Ossian sheriffs). A tested driver's `bac` is the reported blood result; an untested driver's is None.
Each route returns {fips: expected alcohol-impaired-driving deaths}; `rate` divides by the three years' miles."""
import math

import numpy as np

LO, HI = 0.080, 0.150


def band(b):
    return -1 if b is None or b < LO else (0 if b < HI else 1)


def drivers(cr):
    return [d for d in cr["drivers"] if d["identified"]]


def counted(cr):
    return any(d["tested"] and d["bac"] is not None and d["bac"] >= LO for d in drivers(cr))


def total(obs, q_of, combine="product"):
    """Deaths times the chance the crash had a driver at .08 or more, each untested driver at q_of(crash, driver)."""
    out = {}
    for cr in obs:
        if counted(cr):
            p = 1.0
        else:
            qs = [q_of(cr, d) for d in drivers(cr) if not d["tested"]]
            if combine == "product":
                p = 1.0 - float(np.prod([1.0 - q for q in qs])) if qs else 0.0
            else:
                p = min(1.0, sum(qs))
        out[cr["fips"]] = out.get(cr["fips"], 0.0) + cr["deaths"] * p
    return out


def rate(deaths_by, vmt_by):
    return {f: deaths_by.get(f, 0.0) / vmt_by[f] * 1e8 for f in vmt_by}


def _share(ds):
    t = [d for d in ds if d["tested"]]
    return sum(1 for d in t if d["bac"] >= LO) / len(t) if t else 0.0


def killed_share(obs):
    by = {}
    for cr in obs:
        by.setdefault(cr["fips"], []).extend(d for d in drivers(cr) if d["killed"])
    return {f: _share(v) for f, v in by.items()}


def _survivors(obs, complete=None):
    out = []
    for cr in obs:
        for d in drivers(cr):
            if not d["killed"] and (complete is None or d["complete"] == complete):
                out.append((cr, d))
    return out


def catch_rates(obs, subbands=None, agencies=None):
    """At the complete agencies: the share of drivers at each BAC band (or sub-band) arrested at the scene."""
    rows = [d for cr, d in _survivors(obs, True) if d["tested"] and (agencies is None or d.get("agency") in agencies)]
    if subbands:
        out = {}
        for i, (lo, hi) in enumerate(subbands):
            r = [d for d in rows if d["bac"] is not None and lo <= d["bac"] < hi]
            out[i] = sum(d["arrested"] for d in r) / len(r) if r else float("nan")
        return out
    out = {}
    for b in (0, 1):
        r = [d for d in rows if band(d["bac"]) == b]
        out[b] = sum(d["arrested"] for d in r) / len(r)
    return out


def missed(obs, weights):
    """Each county's untested impaired survivors at the arrest-only agencies: sum over its arrested positives of
    one over the catch rate at the positive's band, less the positive itself."""
    by = {}
    for cr, d in _survivors(obs, False):
        if d["tested"] and d["bac"] >= LO:
            by[cr["fips"]] = by.get(cr["fips"], 0.0) + weights(d) - 1.0
    return by


def unarrested_untested(obs):
    by = {}
    for cr, d in _survivors(obs, False):
        if not d["tested"]:
            by[cr["fips"]] = by.get(cr["fips"], 0) + 1
    return by


def _q_from_missed(obs, m):
    u = unarrested_untested(obs)
    return {f: (m.get(f, 0.0) / u[f] if u.get(f) else 0.0) for f in u}


def route(obs, name, **kw):
    ks = killed_share(obs)
    def killed_or(qsurv):
        def q(cr, d):
            if d["killed"]:
                return ks.get(cr["fips"], 0.0)
            return qsurv(cr, d)
        return q
    if name == "R0":                                     # tested drivers only
        return total(obs, lambda cr, d: 0.0)
    if name == "R1":                                     # untested at the county's tested share
        by = {}
        for cr, d in _survivors(obs):
            by.setdefault(cr["fips"], []).append(d)
        ss = {f: _share(v) for f, v in by.items()}
        return total(obs, killed_or(lambda cr, d: ss.get(cr["fips"], 0.0)))
    if name in ("R6", "R6c"):                            # the complete agencies' unarrested share
        rows = [(cr, d) for cr, d in _survivors(obs, True) if d["tested"] and not d["arrested"]]
        if name == "R6":
            q0 = sum(1 for cr, d in rows if d["bac"] >= LO) / len(rows)
            return total(obs, killed_or(lambda cr, d: q0))
        byc = {}
        for cr, d in rows:
            byc.setdefault(cr["fips"], []).append(d)
        qc = {f: sum(1 for d in v if d["bac"] >= LO) / len(v) for f, v in byc.items()}
        q0 = sum(1 for cr, d in rows if d["bac"] >= LO) / len(rows)
        return total(obs, killed_or(lambda cr, d: qc.get(cr["fips"], q0)))
    if name == "R2":                                     # logistic: .08 or more on arrest and county
        b, idx = logit_arrest_county(obs)
        return total(obs, killed_or(lambda cr, d: 1 / (1 + math.exp(-(b[idx[cr["fips"]]] + b[-1] * d["arrested"])))))
    if name == "R8":                                     # one catch rate for every BAC
        rows = [d for cr, d in _survivors(obs, True) if d["tested"] and d["bac"] >= LO]
        dbar = sum(d["arrested"] for d in rows) / len(rows)
        q = _q_from_missed(obs, missed(obs, lambda d: 1.0 / dbar))
        return total(obs, killed_or(lambda cr, d: q.get(cr["fips"], 0.0)))
    if name == "R5":                                     # the complete agencies' prevalence for every survivor
        rows = [d for cr, d in _survivors(obs, True) if d["tested"]]
        p0 = _share(rows)
        loc = {}
        found = {}
        for cr, d in _survivors(obs, False):
            loc[cr["fips"]] = loc.get(cr["fips"], 0) + 1
            if d["tested"] and d["bac"] >= LO:
                found[cr["fips"]] = found.get(cr["fips"], 0) + 1
        m = {f: max(0.0, p0 * loc[f] - found.get(f, 0)) for f in loc}
        q = _q_from_missed(obs, m)
        return total(obs, killed_or(lambda cr, d: q.get(cr["fips"], 0.0)))
    if name == "R4":                                     # untested at the complete agencies' tested share
        p0 = _share([d for cr, d in _survivors(obs, True) if d["tested"]])
        return total(obs, killed_or(lambda cr, d: p0))
    if name == "R3":                                     # untested survivors at the county's killed share
        return total(obs, killed_or(lambda cr, d: ks.get(cr["fips"], 0.0)))
    if name == "G":                                      # the catch rate at each positive's own band
        cr_ = kw.get("catch") or catch_rates(obs, agencies=kw.get("agencies"))
        if kw.get("subbands"):
            sb = kw["subbands"]
            rates_sb = catch_rates(obs, subbands=sb, agencies=kw.get("agencies"))
            def w(d):
                for i, (lo, hi) in enumerate(sb):
                    if lo <= d["bac"] < hi:
                        return 1.0 / rates_sb[i]
                raise ValueError(d["bac"])
        else:
            def w(d):
                return 1.0 / cr_[band(d["bac"])]
        m = missed(obs, w)
        if kw.get("weighted_by_deaths"):
            return _ht_deaths(obs, w, ks)
        if kw.get("spread") == "uncounted":
            u = {}
            for cr in obs:
                if not counted(cr):
                    for d in drivers(cr):
                        if not d["killed"] and not d["complete"] and not d["tested"]:
                            u[cr["fips"]] = u.get(cr["fips"], 0) + 1
            q = {f: m.get(f, 0.0) / u[f] for f in u}
        else:
            q = _q_from_missed(obs, m)
        return total(obs, killed_or(lambda cr, d: q.get(cr["fips"], 0.0)), combine=kw.get("combine", "product"))
    raise KeyError(name)


# the golden completion's family: the catch rates pooled, from the State Patrol alone or the two sheriffs alone, by
# two bands or by sub-bands; the missed drivers spread evenly over the unarrested drivers, over those in crashes not
# otherwise counted, or carried at the found drivers' crash deaths; a crash's drivers combined or summed
G_FAMILY = {
    "pooled": {},
    "state_patrol": {"agencies": {"SP"}},
    "sheriffs": {"agencies": {"SO00500", "SO01900"}},
    "six_subbands": {"subbands": ((0.080, 0.100), (0.100, 0.120), (0.120, 0.150), (0.150, 0.200), (0.200, 0.250),
                                  (0.250, 0.600))},
    "four_subbands": {"subbands": ((0.080, 0.100), (0.100, 0.150), (0.150, 0.200), (0.200, 0.600))},
    "by_crash_deaths": {"weighted_by_deaths": True},
    "uncounted_crashes": {"spread": "uncounted"},
    "summed": {"combine": "sum"},
}


def g_family(obs):
    return {k: route(obs, "G", **kw) for k, kw in G_FAMILY.items()}


def _ht_deaths(obs, w, ks):
    """Variant: the missed drivers' crashes carry the found drivers' crash deaths, each found positive at w - 1."""
    base = total(obs, lambda cr, d: 0.0)
    for cr in obs:
        for d in drivers(cr):
            if not d["killed"] and not d["complete"] and d["tested"] and d["bac"] >= LO:
                base[cr["fips"]] = base.get(cr["fips"], 0.0) + cr["deaths"] * (w(d) - 1.0)
    return base


def logit_arrest_county(obs):
    """Maximum likelihood logistic regression of .08 or more on county (one intercept each) and arrest at the scene,
    fitted to every tested surviving driver."""
    fips = sorted({cr["fips"] for cr in obs})
    idx = {f: i for i, f in enumerate(fips)}
    X, y = [], []
    for cr, d in _survivors(obs):
        if d["tested"]:
            row = [0.0] * (len(fips) + 1)
            row[idx[cr["fips"]]] = 1.0
            row[-1] = 1.0 if d["arrested"] else 0.0
            X.append(row)
            y.append(1.0 if d["bac"] >= LO else 0.0)
    X, y = np.array(X), np.array(y)
    b = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (y - p)
        H = X.T @ (X * (p * (1 - p))[:, None]) + 1e-8 * np.eye(len(b))
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-12:
            break
    return b, idx


ROUTES = ("R0", "R1", "R6", "R6c", "R2", "R8", "R5", "R4", "R3", "G")
