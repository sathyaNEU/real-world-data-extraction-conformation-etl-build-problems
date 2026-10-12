"""The simulation: the card book, each month's 30-day entries, the holds, each centre's dialler list in load order,
the dialler's day (records it cannot dial are skipped only when it reaches them, the team's capacity, results and
attempts), the outcomes two cycle dates on, the arrangements, the capacity log and the delinquency history."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

P30_0 = -4.6
BASE, CAMP_RISK, SKIP_RISK, U_RISK, SCORE_K = -2.0, 0.9, 1.45, 0.6, 55.0
HOLD_RISK = {"ARR": -0.3, "DSP": 0.2, "INS": 2.0, "DEC": 2.6}
HOLD_P = 0.06
HOLD_MIX = (("ARR", 0.45), ("DSP", 0.20), ("INS", 0.25), ("DEC", 0.10))
SEASON = {1: 0.20, 2: 0.15, 12: 0.08}
REACH0 = 0.1
CAP_SD = 0.10
RPC_MIX = (("PTP", 0.38), ("ARR", 0.22), ("RTP", 0.14), ("CBK", 0.08), ("RPC", 0.18))
NC_MIX = (("NOA", 0.46), ("MACH", 0.34), ("BSY", 0.08), ("WRN", 0.07), ("DIS", 0.05))


def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))


SALT = {"entry": 11, "score": 12, "score2": 13, "hold": 14, "holdtype": 15, "key": 16, "jit": 17, "reach": 18,
        "roll": 19, "cap": 20, "cap2": 21}


def u01(ids, month, purpose):
    """A uniform draw fixed by (id, month, purpose), so a parameter change moves only the draws it touches."""
    with np.errstate(over="ignore"):
        x = (np.asarray(ids, dtype=np.uint64) * np.uint64(1000003) + np.uint64(month * 97 + SALT[purpose] * 7919)
             + np.uint64(W.SEED) * np.uint64(0x9E3779B97F4A7C15))
        x = x * np.uint64(0x9E3779B97F4A7C15)
        x ^= x >> np.uint64(30)
        x *= np.uint64(0xBF58476D1CE4E5B9)
        x ^= x >> np.uint64(27)
        x *= np.uint64(0x94D049BB133111EB)
        x ^= x >> np.uint64(31)
    return ((x >> np.uint64(11)).astype(np.float64) + 0.5) / 2.0 ** 53


def n01(ids, month, a, b):
    u1, u2 = u01(ids, month, a), u01(ids, month, b)
    return np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)


def book(rng, campshare=None):
    N = W.N_ACCOUNTS
    centre = rng.choice(5, N, p=W.SHARE)
    camp = rng.random(N) < np.array(campshare or W.CAMP)[centre]
    cycle = rng.integers(1, W.N_CYCLES + 1, N)
    cycle[camp] = rng.choice(W.CAMPAIGN_CYCLES, int(camp.sum()))
    score0 = rng.normal(690, 50, N) - 30 * camp
    u = rng.normal(0, 1, N)
    r = rng.random(N)
    dnc, ndn = np.array(W.DNC)[centre], np.array(W.NDN)[centre]
    skip = np.where(r < dnc, 1, np.where(r < dnc + ndn, 2, 0))          # 1 do-not-call file, 2 no diallable number
    rp = rng.random(N)
    product = np.where(camp, "VSD", np.where(rp < 0.040, "VUSD", np.where(rp < 0.52, "VCL", np.where(rp < 0.86, "VGD", "VIF"))))
    return pd.DataFrame(dict(centre=centre, camp=camp, cycle=cycle, score0=score0, u=u, skip=skip, product=product))


def load_keys(E, mi, mode):
    """The card platform's extract order. 'random': a fresh random order per list. 'strat': each list's records spread
    evenly across it within their kind (skip status, score band), with jitter."""
    r = u01(E.acct.values, mi, "key")
    if mode == "random":
        return r
    band = np.digitize(E.score.values, [600, 650, 700])
    stratum = E.skip.values * 10 + band
    g = pd.DataFrame(dict(c=E.centre.values, d=E.day.values, s=stratum, r=r))
    rank = g.groupby(["c", "d", "s"]).r.rank(method="first").values - 1
    n = g.groupby(["c", "d", "s"]).r.transform("size").values
    return (rank + u01(E.acct.values, mi, "jit")) / n


def simulate(caps=None, delta=None, camp=None, order="strat", reach_c=None):
    caps = list(caps or W.CAP)
    delta = list(delta or W.DELTA)
    reach_c = np.array(reach_c or W.REACH_C)
    rng = np.random.default_rng(W.SEED)
    A = book(rng, camp)
    N = len(A)
    closed = np.zeros(N, bool)
    last = np.full(N, -99)
    rows = []
    for mi, (y, m) in enumerate(W.LIST_MONTHS):
        ids = np.arange(N)
        score_m = A.score0.values + 12 * n01(ids, mi, "score", "score2")
        elig = ~closed & (last < mi - 2)
        p30 = logistic(P30_0 + (660 - score_m) / 40 + 0.55 * A.camp.values + SEASON.get(m, 0.0))
        hit = np.nonzero(elig & (u01(ids, mi, "entry") < p30))[0]
        last[hit] = mi
        E = pd.DataFrame(dict(acct=hit, centre=A.centre.values[hit], cycle=A.cycle.values[hit], camp=A.camp.values[hit],
                              u=A.u.values[hit], skip=A.skip.values[hit], product=A["product"].values[hit],
                              score=np.clip(np.round(score_m[hit]), 420, 880).astype(int)))
        E["mi"] = mi
        cd = {k: W.collections_day(y, m, k) for k in range(1, W.N_CYCLES + 1)}
        E["day"] = E.cycle.map(cd)
        hr = u01(E.acct.values, mi, "hold")
        hold = np.full(len(E), "", object)
        held = hr < HOLD_P
        hx = u01(E.acct.values, mi, "holdtype")
        acc = 0.0
        for code, w in HOLD_MIX:
            hold[held & (hx >= acc) & (hx < acc + w)] = code
            acc += w
        E["hold"] = hold
        E["onlist"] = ~held
        E["key"] = load_keys(E, mi, order)
        E = E.sort_values(["centre", "day", "key"]).reset_index(drop=True)
        on = E.onlist.values
        E["seq"] = 0
        E.loc[on, "seq"] = E[on].groupby(["centre", "day"]).cumcount().values + 1
        dial = on & (E.skip.values == 0)
        E["dial_rank"] = 0
        E.loc[dial, "dial_rank"] = E[dial].groupby(["centre", "day"]).cumcount().values + 1
        days = E[["centre", "day"]].drop_duplicates().reset_index(drop=True)
        did = days.centre.values * 1000000 + np.array([d.toordinal() for d in days.day])
        days["cap"] = np.round(np.array(caps)[days.centre.values] * (1 + CAP_SD * n01(did, 0, "cap", "cap2"))).astype(int)
        E = E.merge(days, on=["centre", "day"], how="left")
        E["dialled"] = dial & (E.dial_rank.values <= E.cap.values)
        E["over"] = E.groupby(["centre", "day"]).dial_rank.transform("max").values > E.cap.values
        cut = E[E.dialled].groupby(["centre", "day"]).seq.max().rename("cut")
        E = E.join(cut, on=["centre", "day"])
        E["left"] = on & E.over.values & (E.seq.values > E.cut.fillna(0).values)
        E["skipped"] = on & (E.skip.values > 0) & ~E.left.values
        E["reached"] = E.dialled.values & (u01(E.acct.values, mi, "reach") < logistic(REACH0 + reach_c[E.centre.values] + 0.9 * E.u.values))
        hrisk = E.hold.map(lambda h: HOLD_RISK.get(h, 0.0)).values
        p0 = logistic(BASE + (660 - E.score.values) / SCORE_K + CAMP_RISK * E.camp.values - U_RISK * E.u.values
                      + SKIP_RISK * (E.skip.values > 0) + hrisk)
        E["p0"] = p0
        p = np.clip(p0 - np.array(delta)[E.centre.values] * E.reached.values, 0.001, 0.999)
        E["roll"] = u01(E.acct.values, mi, "roll") < p
        closed[E.acct.values[E.roll.values | E.hold.isin(["INS", "DEC"]).values]] = True
        rows.append(E)
    E = pd.concat(rows, ignore_index=True)
    return A, E, caps
