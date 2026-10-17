"""The clean truth and the records it leaves: every bus departure from the designated stops from January to June 2026
(the timetable each service day operated, less the trips cancelled), each bus's lateness, the bus that ran it, whether
the AVL vendor's trip matcher tied the stop event to its scheduled trip, the buses that passed through out of service,
and Service Quality's monthly review of the stop events the matchers left without a trip."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import gtfs as G
import world as W

DAYS = [W.FIRST_DAY + dt.timedelta(days=i) for i in range((W.LAST_DAY - W.FIRST_DAY).days + 1)]


def rngs():
    return {k: np.random.default_rng([W.SEED, i]) for i, k in enumerate(
        ("cancel", "late", "match", "vehicles", "review", "ids", "seconds", "deadhead", "files"))}


def everything(review_days=None, take=None):
    R = rngs()
    rows = []
    for d in DAYS:
        deps = G.departures(d)
        kind = W.day_type(d)
        order = [W.FLEET[i] for i in R["vehicles"].permutation(len(W.FLEET))]
        used = 0
        for pool in W.INTERLINE:
            mine = [x for x in deps if x[0] in pool]
            peak = len([x for x in mine if 15 * 60 <= x[1] < 18 * 60])
            k = max(2, int(math.ceil(peak / 3.0 * 0.9)))
            buses = order[used:used + k]
            used += k
            for i, (r, m, key) in enumerate(mine):
                bus = buses[i % len(buses)]
                if R["cancel"].random() < W.cancel_p(r, m // 60, kind):
                    continue
                h = min(m // 60, 23)
                late = R["late"].normal(W.LATE[r][W.band(h)], W.LATE_SD)
                late = max(late, -1.5)
                fault = R["match"].random() < W.LOGON_FAULT
                matched = (abs(late) <= W.WINDOW_MIN) and not fault
                sec = int(round((m + late) * 60)) + int(R["seconds"].integers(0, 60))
                rows.append((d, W.STOP_OF[r], r, key, m, sec, bus, matched, fault, True))
        # buses running out of service through the stops (garage runs, reliefs, changeovers), any bus out that day
        out_today = order[:used]
        for stop, rate in W.OUT_OF_SERVICE.items():
            share = {"WK": 1.0, "FR": 1.0, "SA": W.SATURDAY_SHARE, "SU": W.SUNDAY_SHARE}[W.day_type(d)]
            n = int(R["deadhead"].poisson(rate * 19 * share))
            for t in np.sort(R["deadhead"].integers(5 * 3600, 24 * 3600, n)):
                bus = out_today[int(R["deadhead"].integers(0, len(out_today)))]
                rows.append((d, stop, "", "", -1, int(t), bus, False, False, False))
    ev = pd.DataFrame(rows, columns=["day", "stop", "route", "trip", "sched_min", "sec", "vehicle", "matched", "fault",
                                     "revenue"])
    # a bus passing out of service never meets its own stop event there within two minutes
    ev = ev.sort_values(["vehicle", "stop", "day", "sec"], kind="stable").reset_index(drop=True)
    near = (ev["vehicle"].eq(ev["vehicle"].shift()) & ev["stop"].eq(ev["stop"].shift()) & ev["day"].eq(ev["day"].shift())
            & (ev["sec"] - ev["sec"].shift()).abs().le(120))
    near = near | near.shift(-1, fill_value=False)
    ev = ev[~(near & ~ev["revenue"])].reset_index(drop=True)
    ev["time"] = pd.to_datetime(ev["day"]) + pd.to_timedelta(ev["sec"], unit="s")
    ev["hour"] = ev["time"].dt.hour
    ev["local_day"] = ev["time"].dt.date
    ev = ev.sort_values(["time", "stop", "vehicle"], kind="stable").reset_index(drop=True)
    ev["event_id"] = 7_310_000 + np.arange(len(ev)) * 3 + R["ids"].integers(0, 3, len(ev))
    review = review_sample(ev, R["review"], review_days or W.REVIEW_BUS_DAYS, take or W.REVIEW_TAKE)
    return dict(ev=ev, review=review, R=R)


def review_sample(ev, r, n_days, take):
    """Each month Service Quality lists the bus-days (bus and service day) with at least one stop event the matcher
    left without a trip at the five stops, draws `n_days` of them at random, and reviews `take` of each one's unmatched
    events, chosen at random, against the bus's CCTV."""
    un = ev[~ev["matched"]].copy()
    un["month"] = pd.to_datetime(un["day"]).dt.month
    picks = []
    for mth, g in un.groupby("month"):
        vd = g.groupby(["vehicle", "day"]).size().reset_index(name="u")
        idx = r.choice(len(vd), size=min(n_days, len(vd)), replace=False)
        for j in np.sort(idx):
            v, sd = vd.iloc[j]["vehicle"], vd.iloc[j]["day"]
            rows = g[(g["vehicle"] == v) & (g["day"] == sd)]
            k = min(take, len(rows))
            pick = r.choice(len(rows), size=k, replace=False)
            picks.append(rows.iloc[np.sort(pick)].assign(vd_u=len(rows), frame=len(vd), drawn=min(n_days, len(vd))))
    return pd.concat(picks, ignore_index=True)


def counting(ev):
    """The main population: departures at the designated stops on the counting days, 6 a.m. to 7 p.m."""
    wd = set(W.weekdays())
    m = np.array([d in wd for d in ev["day"]]) & ev["hour"].between(6, 18).to_numpy() & (ev["sec"] < 86400).to_numpy()
    return ev[m]
