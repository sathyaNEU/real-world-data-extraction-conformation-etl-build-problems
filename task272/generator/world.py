"""The world: each member hospital's financial-assistance counsellors and the determinations they recorded in 2025.

A counsellor works a queue of applications on the days the counsellor sits on determinations. A working day's
applications come from that day's intake (presumptive Medicaid referrals, outreach events, mailed balances, walk-ins),
so the chance of approving moves from day to day around the counsellor's own level; inside a day the applications are
taken in the order they became complete, which is unrelated to their merit. At the hospitals whose counsellors are
swayed by their own last determination, an application decided right after an approval is approved less often, and one
decided right after a denial more often, than the day's applications alone would give.

Every hospital is drawn, then its golden family is computed on its clean determinations and the hospital is redrawn
until every member sits on the same side of the six-point line as the hospital's own tendency, by 1.5 points or more."""
import datetime as dt

import numpy as np

import common as K
import models as M

SEED = 27201
N_SWAYED = 11
MARGIN = 1.5
FAMILY_CHECK = ("excess", "excess_fe", "per_day_excess", "cond_logit", "random_day_ml", "jackknife",
                "leave_one_out", "leave_two_out")


def workdays(year=K.YEAR):
    d, out = dt.date(year, 1, 1), []
    while d.year == year:
        if d.weekday() < 5 and d not in K.HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


WORKDAYS = workdays()


def counsellor_days(r, n_days):
    """The days a counsellor sits on determinations: two leave blocks, other duties on about one day in two."""
    sit = np.ones(n_days, bool)
    for _ in range(2):
        s = int(r.integers(0, n_days - 12))
        sit[s:s + int(r.integers(5, 11))] = False
    sit &= r.random(n_days) < 0.48
    return np.flatnonzero(sit)


def chain(r, n, p, e, recon):
    """One day's determinations: recon flags the reconsiderations (a fuller file, more often approved)."""
    y = np.zeros(n)
    u = r.random(n)
    for t in range(n):
        q = p + (0.15 if recon[t] else 0.0)
        if t:
            q += e * (0.5 - y[t - 1])
        y[t] = u[t] < min(max(q, 0.01), 0.99)
    return y


def draw_hospital(code, swayed, seed, attempt):
    r = np.random.default_rng([seed, int(code[1:]), attempt])
    e = r.uniform(0.095, 0.125) if swayed else r.uniform(0.0, 0.02)
    mu = float(r.uniform(8, 32))
    C = int(r.choice([2, 2, 3]) if mu > 20 else r.choice([2, 3, 3, 4]))
    if code == K.MIGRATED:
        C = 3
    sd = float(r.uniform(0.10, 0.20))
    couns = []
    for c in range(C):
        base = float(r.uniform(0.52, 0.80))
        days = []
        for di in counsellor_days(r, len(WORKDAYS)):
            n = max(2, int(r.poisson(mu)))
            p = float(np.clip(base + r.normal(0, sd), 0.10, 0.92))
            recon = r.random(n) < 0.10
            days.append(dict(date=WORKDAYS[di], p=p, recon=recon, y=chain(r, n, p, e, recon)))
        couns.append(dict(base=base, days=days))
    return dict(code=code, swayed=swayed, e=e, C=C, mu=mu, sd=sd, couns=couns, attempt=attempt)


def clean_days(h):
    return [(c, d["date"], d["y"]) for c, co in enumerate(h["couns"]) for d in co["days"]]


def world(seed=SEED, verbose=False):
    r = np.random.default_rng(seed)
    flags = np.array([True] * N_SWAYED + [False] * (len(K.CODES) - N_SWAYED))
    r.shuffle(flags)
    out = []
    for code, sw in zip(K.CODES, flags):
        attempt = 0
        while True:
            h = draw_hospital(code, bool(sw), seed, attempt)
            fam = M.family(clean_days(h), FAMILY_CHECK)
            side = {v >= K.THRESHOLD for v in fam.values()}
            if side == {bool(sw)} and min(abs(v - K.THRESHOLD) for v in fam.values()) >= MARGIN:
                h["family"] = fam
                out.append(h)
                break
            attempt += 1
        if verbose:
            print(code, "swayed" if sw else "steady", "attempts", attempt + 1,
                  {k: round(v, 2) for k, v in fam.items()}, flush=True)
    return out
