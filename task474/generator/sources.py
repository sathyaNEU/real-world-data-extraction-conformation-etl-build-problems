"""The clean truth: every member's first half of 2026, month by month: covered or not, on the plan's roster or not,
the group the roster assigns, the paid medical cost of the month's services; and the events behind them (renewal
lapses reinstated back to the lapse, departures, deaths). Nothing here knows about files or mess."""
import numpy as np

import world as W

NM = len(W.MONTHS)


def members(rng):
    out = []
    mid = 700100000
    for g, (name, county, n0, base, p_lapse, p_death, p_leave) in W.GROUPS.items():
        n_join = int(n0 * .012 * NM)
        for k in range(n0 + n_join):
            mid += int(rng.integers(1, 40))
            start = 0 if k < n0 else int(rng.integers(1, NM))
            ann = start if k >= n0 else int(rng.integers(0, 12))     # renewal falls on the enrollment anniversary
            risk = float(np.exp(rng.normal(-.32, .8)))
            cov = np.zeros(NM, bool)
            cov[start:] = True
            roster = cov.copy()
            lapse = np.zeros(NM, bool)
            event = None
            if k < n0 and ann < NM:
                u = rng.random()
                if u < p_lapse:
                    L = int(rng.choice([1, 2, 3], p=[.4, .38, .22]))
                    lapse[ann:ann + L] = True
                    roster[ann:ann + L] = False
                    event = ("lapse", ann, min(NM, ann + L))
                elif u < p_lapse + p_leave:
                    cov[ann:] = False
                    roster[ann:] = False
                    event = ("leave", ann)
            dead = None
            if event is None and rng.random() < p_death * (3.0 if g in W.LAG else 1.0):
                d = int(rng.integers(start, NM))
                cov[d + 1:] = False
                lags = W.LAG.get(g, (1, 2, 2))
                lag = int(rng.choice(lags))
                roster[d + 1:d + 1 + lag] = True
                roster[d + 1 + lag:] = False
                dead = d
            # the month's paid cost: deferred care while the member believes the coverage gone, end-of-life care in
            # the month of death
            cost = np.zeros(NM)
            for m in range(NM):
                if cov[m]:
                    # most member-months carry no claim at all; the rest carry the month's care
                    c = 0.0 if rng.random() < .55 else float(rng.gamma(.55, base * risk / (.45 * .55)))
                    if lapse[m]:
                        c *= .18 if rng.random() < .7 else 0.0
                    if dead == m:
                        c *= 3.5
                    if c > 0:
                        c = max(c, float(rng.uniform(14, 45)))     # the smallest claim a month carries
                    cost[m] = c
            out.append(dict(mid=mid, group=g, start=start, ann=ann, cov=cov, roster=roster, lapse=lapse,
                            event=event, dead=dead, cost=cost, risk=risk))
    return out


def exposure(ms, route):
    """{group: member-months}: "golden" the covered months; "roster" the roster's months; "retro" the roster's months
    plus the reinstated lapse months; "orphan" the roster's months plus off-roster months with any paid cost."""
    out = {}
    for x in ms:
        if route == "golden":
            v = x["cov"].sum()
        elif route == "roster":
            v = x["roster"].sum()
        elif route == "retro":
            v = (x["roster"] | x["lapse"]).sum()
        elif route == "orphan":
            v = (x["roster"] | (x["cost"] > 0)).sum()
        out[x["group"]] = out.get(x["group"], 0) + int(v)
    return out


def pmpm(ms, route):
    cost = {}
    for x in ms:
        cost[x["group"]] = cost.get(x["group"], 0.0) + float(x["cost"].sum())
    ex = exposure(ms, route)
    return {g: cost[g] / ex[g] for g in cost}
