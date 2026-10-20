"""The easy routes, each run from the pack on the conformed call histories: the respondents' share, weighting-class
adjustments, the late-reached and evening-reached respondents carried to the members not known, an extrapolation along
the attempt that reached the member, the subsets called by the vendor from the start or called in the evening, and the
textbook callback model with one answer rate per class. Each gives every region's share and its four lowest."""
import numpy as np
import statsmodels.api as sm

import models as M


def four(v):
    return tuple(sorted(np.argsort(v)[:4].tolist()))


def _carry(y, known, reg, donor, n_regions=10):
    """Known members keep their class; every member not known takes the donor group's share in the region."""
    out = np.zeros(n_regions)
    for r in range(n_regions):
        m = reg == r
        d = known & donor & m
        out[r] = (y[known & m].sum() + (m & ~known).sum() * y[d].mean()) / m.sum()
    return out


def run(c):
    """c: analysis.call output. Returns {route: shares by region}."""
    S, SS = c["S"], c["SS"]
    hist = c["hist"]
    y, out, reg = SS["y"], SS["out"], SS["reg"]
    age, sex = SS["age"], SS["sex"]
    known = y >= 0
    comp = out == 1
    cids = sorted(S)
    first_vendor = np.array([S[cid]["first"] == "Kestrelby" for cid in cids])
    attempt = np.array([len(h[5]) for h in hist])           # calls made up to and including the reaching call
    reach_combo = SS["hit"]
    any_eve = np.array([any(cmb in (2, 3) for cmb, _ in h[5]) for h in hist])
    R = {}
    R["respondents (interviews)"] = np.array([y[comp & (reg == r)].mean() for r in range(10)])
    R["respondents (interviews and key answers)"] = np.array([y[known & (reg == r)].mean() for r in range(10)])
    for name, extra in (("age and sex cells", None), ("age, sex and first-call centre cells", first_vendor)):
        v = np.zeros(10)
        for r in range(10):
            m = reg == r
            tot = 0.0
            for a in range(3):
                for s in range(2):
                    for e in ((False, True) if extra is not None else (None,)):
                        cell = m & (age == a) & (sex == s)
                        if e is not None:
                            cell = cell & (extra == e)
                        resp = cell & known
                        tot += cell.sum() * (y[resp].mean() if resp.sum() else y[known & m].mean())
            v[r] = tot / m.sum()
        R[name] = v
    R["reached at call 3 or later, carried"] = _carry(y, known, reg, attempt >= 3)
    R["reached at call 4 or later, carried"] = _carry(y, known, reg, attempt >= 4)
    R["reached in the evening or on Saturday, carried"] = _carry(y, known, reg, np.isin(reach_combo, (2, 3)))
    v = np.zeros(10)
    for r in range(10):
        m = reg == r
        X = sm.add_constant(attempt[known & m].astype(float))
        fit = sm.Logit(y[known & m].astype(float), X).fit(disp=0)
        k = attempt[m & ~known].astype(float) + 1
        v[r] = (y[known & m].sum() + fit.predict(sm.add_constant(k, has_constant="add")).sum()) / m.sum()
    R["logistic on the reaching call, extrapolated"] = v
    R["vendor-first members only"] = np.array([y[known & first_vendor & (reg == r)].mean() for r in range(10)])
    R["members ever called in the evening or on Saturday"] = np.array([y[known & any_eve & (reg == r)].mean()
                                                                       for r in range(10)])
    # a response-propensity weight: the chance a member's answer is known, on the member's evening and Saturday share
    # of calls, the number of calls, age band, sex and region; each known member weighted by its inverse
    eve_share = np.array([np.mean([cmb in (2, 3) for cmb, _ in h[5]]) for h in hist])
    X = np.column_stack([eve_share, attempt, (age == 1), (age == 2), sex] + [(reg == r) for r in range(1, 10)]).astype(float)
    fit = sm.Logit(known.astype(float), sm.add_constant(X)).fit(disp=0)
    pk = fit.predict(sm.add_constant(X))
    R["response propensity on the calls' evening share, inverse weights"] = np.array(
        [np.sum(y[known & (reg == r)] / pk[known & (reg == r)]) / np.sum(1 / pk[known & (reg == r)]) for r in range(10)])
    R["reached at the first call only"] = np.array([y[known & (attempt == 1) & (reg == r)].mean() for r in range(10)])
    R["callback model, one answer rate per class"] = M.em(SS, contact="none")[0]
    return R


def family(c):
    """The callback model's licensed variants, each to agree with the golden on the four and the graded percents."""
    SS = c["SS"]
    F = {nm: M.em(SS, **kw)[0] for nm, kw in M.FAMILY.items()}
    F["window, pooled, declining flat"] = M.em(SS, refusal="flat")[0]
    F["window, pooled, attempt effect"] = M.em_attempt(SS)[0]
    return F
