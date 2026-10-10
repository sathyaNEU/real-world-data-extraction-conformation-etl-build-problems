"""task127 generator: the pilot calendar and the six meter crews' field orders, 2025 to 2026.

Standing work is generated as completions per working day and back-dated by its own scheduling lag,
so its level and lag are the same in every period. The July 2025 meter-exchange batches at Lakes and
Uplands, and the pilot's heat-pump rate meter orders, are worked in order of readiness from whatever the
day leaves after standing work.
"""
from collections import deque
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P
from world import holidays, workdays

SIM_START = date(2024, 12, 2)
SIM_END = date(2026, 12, 31)
PULL = date(2026, 12, 10)          # last completion date in the extract
HOL = holidays(2024) | holidays(2025) | holidays(2026)
BATCH_DAY = date(2025, 7, 7)
LAG_P = np.array([0.07, 0.24, 0.25, 0.18, 0.12, 0.08, 0.06])
READY_P = np.array([0.32, 0.26, 0.20, 0.13, 0.09])
PREFIX = {"NS": 10, "VA": 22, "LA": 31, "UP": 45, "RB": 57, "PW": 68}
AUTUMN_FIRST = date(2026, 9, 25)


def crew_days(c):
    return workdays(SIM_START, SIM_END, HOL, four_day=c in P.FOUR_DAY)


def premises_pool(c, n=9000):
    g = P.rng("premises|" + c)
    ids = g.choice(np.arange(10000, 99999), size=n, replace=False)
    return [f"{PREFIX[c[:2]]}{x}" for x in ids]


# ------------------------------------------------------------------ the pilot calendar

def _weekday_on_or_after(d):
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def pilot_dates(pi):
    """Purchase and install dates for every pilot install (frame from world.pilot_installs).

    Installs are spread evenly over each season's install span; the purchase precedes the install by the
    installer's lead time, inside the application window. Every neighbourhood's autumn installs begin on
    the installers' first autumn day, Friday 25 September 2026."""
    g = P.rng("pilot-dates")
    pur = [None] * len(pi)
    ins = [None] * len(pi)
    for c in P.COOPS:
        for season in ("spring", "autumn"):
            idx = g.permutation(np.flatnonzero((pi.coop.to_numpy() == c) & (pi.season.to_numpy() == season)))
            n = len(idx)
            if season == "spring":
                i0, span, w0, w1 = date(2026, 3, 23), 80, date(2026, 3, 1), date(2026, 4, 30)
            else:
                i0, span, w0, w1 = AUTUMN_FIRST, 66, date(2026, 9, 1), date(2026, 10, 15)
            for j, k in enumerate(idx):
                if season == "autumn" and j < 2:
                    i = AUTUMN_FIRST
                else:
                    i = i0 + timedelta(days=int(round((j + g.uniform(0.15, 0.85)) * span / n)))
                    i = _weekday_on_or_after(i)
                    if season == "autumn" and i <= AUTUMN_FIRST:
                        i = AUTUMN_FIRST + timedelta(days=3)
                lag = int(g.integers(22, 46))
                p = min(max(i - timedelta(days=lag), w0), w1)
                if season == "autumn" and j < 2:
                    p = w0
                pur[k], ins[k] = p, i
    pi = pi.copy()
    pi["purchase_date"] = pur
    pi["install_date"] = ins
    return pi


# ------------------------------------------------------------------ crews

def _standing_counts(c, days):
    g = P.rng("standing|" + c)
    if c in P.FOUR_DAY:
        block = np.array(P.STANDING_BLOCK[c])
        out = []
        while len(out) < len(days):
            out += g.permutation(block).tolist()
        return np.array(out[:len(days)])
    lam = np.full(len(days), P.STANDING_LEVEL[c])
    return g.poisson(lam)


def _surges(c, days):
    """Extra standing orders (count, type) by working day for the five-day crews' events."""
    extra = {}

    def add(d0, d1, per_day, typ):
        for d in days:
            if d0 <= d <= d1:
                extra.setdefault(d, []).append((per_day, typ))
    if c == "NS":                      # seasonal cabin reconnects every May
        add(date(2025, 5, 5), date(2025, 5, 30), 7, "RCON")
        add(date(2026, 5, 4), date(2026, 5, 29), 8, "RCON")
    if c == "VA":                      # spring 2025: new services for the Coulee Ridge subdivision
        add(date(2025, 4, 7), date(2025, 5, 2), 8, "NSVC")
    if c == "RB":                      # April 2026 high water: disconnects, then reconnects
        add(date(2026, 4, 6), date(2026, 4, 17), 9, "DISC")
        add(date(2026, 4, 20), date(2026, 5, 15), 12, "RCON")
    if c == "PW":                      # storm of 22 June 2026
        add(date(2026, 6, 23), date(2026, 7, 10), 9, "RCON")
    return extra


def crew_orders(c, pilot):
    """All field orders for one crew, with completion dates, through SIM_END (open ones cut later)."""
    days = crew_days(c)
    pos = {d: i for i, d in enumerate(days)}
    g = P.rng("orders|" + c)
    st = _standing_counts(c, days)
    extra = _surges(c, days)
    types = list(P.STANDING_MIX)
    tp = np.array([P.STANDING_MIX[t] for t in types])
    pool = premises_pool(c)
    rows = []
    for i, d in enumerate(days):
        k = int(st[i])
        tt = g.choice(types, size=k, p=tp).tolist()
        for n, typ in extra.get(d, []):
            tt += [typ] * int(g.poisson(n))
        for typ in tt:
            lag = int(g.choice(len(LAG_P), p=LAG_P))
            req = days[max(0, i - lag)] if lag else d
            if lag and g.random() < 0.3:          # requests also land on non-working days
                req = req - timedelta(days=int(g.integers(1, 3)))
            rows.append(dict(coop=c, order_type=typ, premises_id=pool[int(g.integers(0, len(pool)))],
                             requested=req, completed=d, kind="standing"))
    if c == "VA":                      # meter-supply hold, March 2026: tests and new services wait
        hold0, hold1, back = date(2026, 2, 23), date(2026, 3, 20), date(2026, 3, 23)
        held = [r for r in rows if r["order_type"] in ("MTST", "NSVC") and hold0 <= r["completed"] <= hold1]
        held.sort(key=lambda r: (r["requested"], r["completed"]))
        catch = [d for d in days if d >= back][:6]
        for j, r in enumerate(held):
            r["completed"] = catch[j * len(catch) // max(1, len(held))]
    # work left after standing work on each day
    if c in P.FOUR_DAY:
        cyc = P.CEILING_CYCLE[c]
        cap = np.array([cyc[i % len(cyc)] for i in range(len(days))])
        done = pd.Series([r["completed"] for r in rows]).value_counts()
        spare = np.array([cap[i] - int(done.get(d, 0)) for i, d in enumerate(days)])
        assert spare.min() >= 0, (c, spare.min())
    else:
        spare = np.full(len(days), 99)
    queue = deque()
    arrivals = {}
    if c in P.BATCH:
        bpool = premises_pool(c + "-mx", 400)
        for j in range(P.BATCH[c]):
            arrivals.setdefault(days[pos[BATCH_DAY] + 1], []).append(
                dict(coop=c, order_type="MXCH", premises_id=bpool[j], requested=BATCH_DAY, kind="batch"))
    pg = P.rng("ready|" + c)
    for _, r in pilot[pilot.coop == c].sort_values(["install_date", "premises_id"]).iterrows():
        k = pos.get(r.install_date)
        if k is None:
            k = next(i for i, d in enumerate(days) if d > r.install_date) - 1
        ready = days[k + 1 + int(pg.choice(len(READY_P), p=READY_P))]
        arrivals.setdefault(ready, []).append(
            dict(coop=c, order_type="HPRM", premises_id=r.premises_id, requested=r.install_date, kind="pilot"))
    for i, d in enumerate(days):
        for o in arrivals.get(d, []):
            queue.append(o)
        k = int(spare[i])
        while k > 0 and queue:
            o = queue.popleft()
            o["completed"] = d
            rows.append(o)
            k -= 1
    assert not queue, c
    return pd.DataFrame(rows), days, (cap if c in P.FOUR_DAY else None)


def all_orders(pilot):
    frames, meta = [], {}
    for c in P.COOPS:
        df, days, cap = crew_orders(c, pilot)
        frames.append(df)
        meta[c] = dict(days=days, cap=cap)
    df = pd.concat(frames, ignore_index=True)
    df["crew"] = df.coop.map(P.CREW)
    # the extract: completed 1 Jan 2025 to the pull, plus orders open at the pull
    keep = ((df.completed >= date(2025, 1, 1)) & (df.completed <= PULL)) | \
           ((df.requested <= PULL) & (df.completed > PULL))
    df = df[keep].copy()
    df.loc[df.completed > PULL, "completed"] = None
    df = df.sort_values(["requested", "coop", "order_type", "premises_id"], kind="stable").reset_index(drop=True)
    seq = df.groupby(df.coop).cumcount()
    df["order_id"] = [f"{c}{r.year % 100:02d}-{100000 + 3 * int(s):06d}" for c, r, s in zip(df.coop, df.requested, seq)]
    return df, meta
