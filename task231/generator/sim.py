"""task231 simulation: the Business Conditions Survey panel from March 2017 to the September 2026 round.

Each firm carries a response propensity, a closure date (exponential from recruitment) and the date the business register
records the closure (a route-specific lag). Rounds invite every panel firm not yet withdrawn, retired or recorded closed;
firms still trading return with their propensity; the contact centre calls the firms still out on day 15. The truth is
kept beside every record so the checks can test each estimator against it."""
from datetime import date, timedelta
import numpy as np

import params as P


def round_dates():
    out = []
    y, m = P.BURN_IN.year, P.BURN_IN.month
    while date(y, m, 1) <= P.CURRENT:
        out.append(date(y, m, 1))
        m += 3
        if m > 12:
            y, m = y + 1, m - 12
    return out


def close_of(frame):
    """The main fieldwork close: the Friday on or before day 25 of the round month, or 23 December when that Friday is
    Christmas Eve or Christmas Day."""
    d = frame + timedelta(days=24)
    while d.weekday() != 4:
        d -= timedelta(days=1)
    if d.month == 12 and d.day in (24, 25):
        d = date(d.year, 12, 23)
    return d


def end_of(frame):
    """The round's data cut-off: the Friday on or after day 42, after which late returns no longer enter the round."""
    d = frame + timedelta(days=42)
    while d.weekday() != 4:
        d += timedelta(days=1)
    return d


def call_days(frame, close):
    """The contact centre's reminder-call days: the working days from day 15 of the round to the main close, as day
    offsets from the frame date."""
    out = []
    d = frame + timedelta(days=P.CALL_DAY)
    while d <= close:
        if d.weekday() < 5:
            out.append((d - frame).days)
        d += timedelta(days=1)
    return out


class Panel:
    def __init__(self, seed=P.SEED, region_seeds=None):
        """Each region draws from its own three streams (firms, returns, calls), so a region can be tuned without
        moving any other region's records."""
        offs = P.REGION_SEEDS if region_seeds is None else region_seeds
        self.streams = {}
        for i, r in enumerate(P.REGIONS):
            base = seed + 1000 * (i + 1) + 7919 * offs.get(r[0], 0)
            self.streams[r[0]] = (np.random.default_rng(base), np.random.default_rng(base + 1), np.random.default_rng(base + 2))
        self.rng = np.random.default_rng(seed)
        self.rounds = round_dates()
        self.firms = []
        self.outcomes = []      # one dict per invited firm per round
        self.calls = []         # one dict per call made

    # ------------------------------------------------------------------ firms
    def recruit(self, region_idx, frame, wave):
        code, name, _, (a, b), hm = P.REGIONS[region_idx]
        rng = self.streams[code][0]
        ind = P.INDUSTRIES[rng.choice(len(P.INDUSTRIES), p=[x[2] for x in P.INDUSTRIES])][0]
        si = rng.choice(len(P.SIZES), p=[x[2] for x in P.SIZES])
        size = P.SIZES[si][0]
        p = float(rng.beta(a, b) ** (1.0 / P.SIZES[si][3]))
        h = P.HAZARD * P.SIZE_HAZARD[size] * hm
        life = rng.exponential(91.31 / h)
        ceased = frame + timedelta(days=int(life))
        u = rng.random()
        acc = 0.0
        for route, share, med, sd in P.LAG_ROUTES:
            acc += share
            if u <= acc:
                break
        lag = int(rng.lognormal(np.log(med), sd))
        f = dict(fid=len(self.firms), region=code, industry=ind, size=size, p=p, joined=frame, wave=wave,
                 ceased=ceased, route=route, registered=ceased + timedelta(days=lag), withdrawn=None, retired=None,
                 silent=0, history=[])
        self.firms.append(f)
        return f

    # ------------------------------------------------------------------ rounds
    def run(self):
        removed_since = {r[0]: 0 for r in P.REGIONS}
        for ri, (code, name, n0, _, _h) in enumerate(P.REGIONS):
            for _ in range(n0):
                self.recruit(ri, P.BURN_IN, "2014")
        for frame in self.rounds:
            if frame.month == 3 and frame > P.BURN_IN:
                for ri, (code, name, n0, _, _h) in enumerate(P.REGIONS):
                    n = removed_since[code]
                    if frame == P.EXPANSION_ROUND:
                        n += int(round(n0 * P.EXPANSION_SHARE))
                    for _ in range(n):
                        self.recruit(ri, frame, "expansion" if frame == P.EXPANSION_ROUND else "refresh")
                    removed_since[code] = 0
            close = close_of(frame)
            current = frame == P.CURRENT
            for f in self.firms:
                if f["joined"] > frame or f["withdrawn"] is not None or f["retired"] is not None:
                    continue
                if f["registered"] < frame:
                    if f.get("removed") is None:
                        f["removed"] = frame
                        removed_since[f["region"]] += 1
                    continue
                self.invite(f, frame, close, current)
            # retirements and withdrawals after the round
            for f in self.firms:
                if f["joined"] > frame or f["withdrawn"] is not None or f["retired"] is not None or f.get("removed") is not None:
                    continue
                if f["silent"] >= P.RETIRE_AFTER:
                    f["retired"] = frame
                    removed_since[f["region"]] += 1
                elif f["ceased"] > frame and self.streams[f["region"]][0].random() < P.WITHDRAW:
                    f["withdrawn"] = frame + timedelta(days=int(self.streams[f["region"]][0].uniform(30, 85)))
                    removed_since[f["region"]] += 1
        return self

    def invite(self, f, frame, close, current):
        _, rr, rc = self.streams[f["region"]]
        alive = f["ceased"] > frame
        o = dict(fid=f["fid"], region=f["region"], frame=frame, close=close, end=end_of(frame), alive=alive, k=f["silent"],
                 ret_day=None, mode=None, call=None, call_day=None)
        horizon = 24 if current else 40
        if alive and rr.random() < f["p"] * 0.74:
            o["ret_day"] = int(min(rr.geometric(0.16), 14))
            o["mode"] = "web" if rr.random() < 0.82 else "post"
        else:
            # still out on day 15: the contact centre calls
            tab = P.CALL_ALIVE if alive else P.CALL_CLOSED
            keys = list(tab)
            outc = keys[rc.choice(len(keys), p=[tab[k] for k in keys])]
            o["call"] = outc
            days = call_days(frame, close)
            o["call_day"] = days[int(rc.integers(0, len(days)))]
            if outc == "returned":
                o["ret_day"], o["mode"] = o["call_day"], "phone"
            elif alive:
                q = f["p"] * 0.18 + (P.CALL_RETURN_LIFT if outc == "promised" else 0.0)
                if rr.random() < q:
                    d = o["call_day"] + int(rr.integers(1, 10))
                    if d <= 24 or not current:
                        o["ret_day"] = min(d, horizon)
                        o["mode"] = "web" if rr.random() < 0.7 else "post"
        returned_by_close = o["ret_day"] is not None and frame + timedelta(days=o["ret_day"]) <= close
        o["by_close"] = returned_by_close
        if not current:
            f["silent"] = 0 if o["ret_day"] is not None else f["silent"] + 1
        if frame >= P.FIRST_ROUND:
            self.outcomes.append(o)
            if o["call"] is not None:
                self.calls.append(o)
