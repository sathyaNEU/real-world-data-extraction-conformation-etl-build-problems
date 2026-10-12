"""Every day's probe travel times, October 2025 to September 2026, 05:30 to 09:25: the northbound route with the
I-264 merge queue that builds through the morning and spills back over the five segments ahead of it, the
downtown approach that slows towards 8:00, incidents, and lighter days in school breaks, summer, weekends and
holidays; the southbound deadhead route (counter-peak, nearly free-flowing), the I-264 collector ramp (queued in
the morning) and the other corridor segments; three vehicle classes."""
import numpy as np

import core

# the world's queue and noise parameters (stage 3 search, see the design note)
SEED = 30880
DEAD_SEED = 0          # stage 3 tuning of the ask-path streams (deadhead, split, ramp)
P = {"summer": 0.62, "dsd": 0.20620007411570063, "jit": 8.043693886636122, "onset": 31.940632038805653,
     "oslope": 30.38488599346781, "peak": 44.74103274255093, "qmax": 2716.0737410022743,
     "dthr": 0.5439846919423603, "shape": 1.0, "lag": 0.1, "art": 114.19612323610733,
     "segsd": 0.16504488204233564, "pinc": 0.12}
SHARES = [0.10, 0.15, 0.20, 0.25, 0.30]     # the queue's share by segment, upstream to just before the merge


def route_day(rng, kind, P):
    """One day's northbound route travel times (NE x 16, seconds) and whether an incident was logged."""
    ff = np.array([r[5] for r in core.ROUTE], float)
    tt = np.tile(ff, (core.NE, 1))
    tm = core.EPOCHS + 2.5
    if kind == "weekend":
        tt *= rng.lognormal(0, 0.03, size=tt.shape)
        return tt, False, 0.0
    light = {"school": 1.0, "break": P["summer"], "holiday": 0.42}[kind]
    d = float(rng.lognormal(0, P["dsd"])) * light
    shift = float(rng.normal(0, P["jit"]))
    t0 = 6 * 60 + P["onset"] + shift - P["oslope"] * (d - 1)
    tp = 7 * 60 + P["peak"] + shift + 12 * (d - 1)
    tc = 9 * 60 + 20 + 40 * (d - 1)
    peak = max(0.0, P["qmax"] * (d - P["dthr"]))
    f = np.where(tm <= tp, (tm - t0) / max(1.0, tp - t0), 1 - (tm - tp) / max(1.0, tc - tp))
    f = np.clip(f, 0, None) ** P["shape"]
    f[(tm <= t0) | (tm >= tc)] = 0.0
    q = peak * f
    for j, k in enumerate(reversed(core.QUEUE_SEGS)):
        lag = P["lag"] * j
        g = np.where(f < lag, 0.0, np.where(tm <= tp, (f - lag) / (1 - lag), f))
        tt[:, k] += q * SHARES[::-1][j] * g
    tt[:, core.BOTTLENECK] += 0.15 * q
    af = float(rng.lognormal(0, 0.45)) * (light if kind != "school" else 1.0)
    w = np.clip(1 - np.abs(tm - 8 * 60) / 40.0, 0, None) * ((tm >= 7 * 60 + 20) & (tm <= 8 * 60 + 40))
    for a, k in zip((1.0, 1.3, 0.9), core.ARTERIAL):
        tt[:, k] += a * P["art"] * w * af
    inc = (kind == "school" or kind == "break") and rng.random() < P["pinc"]
    if inc:
        k = int(rng.integers(0, 13))
        s = int(rng.integers(6 * 60, 7 * 60 + 50))
        L = int(rng.integers(30, 90))
        extra = float(rng.uniform(300, 1400))
        on = (core.EPOCHS >= s) & (core.EPOCHS < s + L)
        tt[on, k] += extra * (1 - (core.EPOCHS[on] - s) / (L + 15))
    tt *= rng.lognormal(0, P["segsd"], size=16)[None, :]
    tt *= rng.lognormal(0, 0.02, size=tt.shape)
    return tt, bool(inc), d


def deadhead_day(rng, kind):
    """The southbound deadhead segments in the 2025 release's order (NE x 9, seconds): counter-peak, a mild
    bump after 7:30 on school days."""
    ff = np.array([r[5] for r in core.DEADHEAD], float)
    tm = core.EPOCHS + 2.5
    bump = 0.0 if kind == "weekend" else (0.12 if kind == "school" else 0.06)
    prof = 1 + bump * np.clip(1 - np.abs(tm - (8 * 60 + 5)) / 50.0, 0, None)
    tt = np.outer(prof, ff) * rng.lognormal(0, 0.05, size=9)[None, :]
    return tt * rng.lognormal(0, 0.025, size=tt.shape)


def split_day(rng, stretch):
    """The two codes that replace the reissued deadhead code from the 2026 release: the stretch's time shared in
    proportion to their free-flow times, each with its own small noise."""
    a, b = core.T1_NEW[0][5], core.T1_NEW[1][5]
    w = np.array([a, b], float) / (a + b)
    return stretch[:, None] * w[None, :] * rng.lognormal(0, 0.02, size=(core.NE, 2))


def ramp_day(rng, kind):
    """The I-264 westbound collector ramp: queued from about 7:00 to 9:30 on working days, worst near 8:20."""
    ff = core.RAMP[4]
    tm = core.EPOCHS + 2.5
    amp = {"school": 1.0, "break": 0.55, "holiday": 0.25, "weekend": 0.0}[kind] * float(rng.lognormal(0, 0.25))
    q = 420.0 * amp * np.clip(1 - np.abs(tm - (8 * 60 + 20)) / 80.0, 0, None) ** 1.2
    return (ff + q) * rng.lognormal(0, 0.03, size=core.NE)


def other_day(rng, kind):
    ff = np.array([r[5] for r in core.OTHER], float)
    tm = core.EPOCHS + 2.5
    lvl = {"school": 1.0, "break": 0.6, "holiday": 0.3, "weekend": 0.05}[kind]
    hump = np.clip(1 - np.abs(tm - (7 * 60 + 50)) / 60.0, 0, None)
    amp = np.array([0.6, 0.9, 0.5, 1.1, 0.7, 0.8, 0.9, 0.2]) * lvl * float(rng.lognormal(0, 0.2))
    tt = ff[None, :] * (1 + np.outer(hump, amp))
    return tt * rng.lognormal(0, 0.03, size=tt.shape)


def kind_of(d):
    if d.weekday() >= 5:
        return "weekend"
    if not core.working(d):
        return "holiday"
    return "school" if core.school_day(d) else "break"


def build(seed, P=P, dead_seed=None):
    days = core.days()
    rng = np.random.default_rng([seed, 1])
    ds = DEAD_SEED if dead_seed is None else dead_seed
    rr = np.random.default_rng([seed, 2, ds])
    rd = np.random.default_rng([seed, 3, ds])
    ro = np.random.default_rng([seed, 4])
    rs = np.random.default_rng([seed, 5, ds])
    route, dead, split, ramp, other, inc, dem = [], [], [], [], [], [], []
    for d in days:
        k = kind_of(d)
        tt, i, dd = route_day(rng, k, P)
        route.append(tt)
        inc.append(i)
        dem.append(dd)
        dh = deadhead_day(rd, k)
        dead.append(dh)
        split.append(split_day(rs, dh[:, core.T1_INDEX]))
        ramp.append(ramp_day(rr, k))
        other.append(other_day(ro, k))
    W = {"days": days, "route": np.stack(route), "dead": np.stack(dead), "split": np.stack(split),
         "ramp": np.stack(ramp),
         "other": np.stack(other), "incident": np.array(inc), "demand": np.array(dem),
         "kind": np.array([kind_of(d) for d in days])}
    W["work"] = np.array([core.working(d) for d in days])
    return W


def add_classes(W, seed):
    """The route's all-vehicle and freight times (after herding), on their own stream."""
    rc = np.random.default_rng([seed, 6])
    allv, frt = [], []
    for tt in W["route"]:
        a, f = classes(tt, rc)
        allv.append(a)
        frt.append(f)
    W["route_all"], W["route_frt"] = np.stack(allv), np.stack(frt)
    return W


VARIANTS = ("entry", "mid", "exit", "interp")
HERD_DEPS = tuple(d for d in core.DEPARTURES if d >= 6 * 60 + 50)      # every departure the asks grade
MARGIN = 0.25                               # minutes (15 seconds) beyond the variants' own spread


def _clear(tt1, ff):
    """True when, for one day, every walk variant puts each herded departure's arrival on the same side of 8:00
    by at least MARGIN, and no departure from 6:30 to 7:20 arrives within a second of 8:00 under any variant."""
    for dep in core.DEPARTURES:
        arr = np.array([core.walk(tt1[None], dep, v)[0] for v in VARIANTS])
        if np.min(np.abs(arr - core.BAR_TIME)) < 1.0 / 60:
            return False
        if dep in HERD_DEPS and not ((arr <= core.BAR_TIME - MARGIN).all() or (arr > core.BAR_TIME + MARGIN).all()):
            return False
    return True


def herd(W):
    """Scale a working day's congestion (time above free flow) by the factor nearest 1 that clears it; record the
    factors. The day stays the day it was drawn, a few per cent heavier or lighter in its queues."""
    ff = np.array([r[5] for r in core.ROUTE], float)
    grid = [1.0] + [1.0 + s * k / 100.0 for k in range(1, 26) for s in (-1, 1)]
    moved = {}
    for i in np.where(W["work"])[0]:
        tt = W["route"][i]
        for lam in grid:
            cand = ff[None, :] + lam * (tt - ff[None, :])
            if _clear(cand, ff):
                if lam != 1.0:
                    W["route"][i] = cand
                    moved[int(i)] = lam
                break
        else:
            raise AssertionError("no herding factor clears day %d" % i)
    W["herded"] = moved
    return W


def classes(tt, rng):
    """All vehicles and freight from the passenger times: trucks are slower, more so in congestion."""
    ff = tt.min(axis=1, keepdims=True)
    cong = np.clip(tt / ff - 1, 0, None)
    allv = tt * (1.02 + 0.02 * np.tanh(cong)) * rng.lognormal(0, 0.01, size=tt.shape)
    frt = tt * (1.10 + 0.06 * np.tanh(cong)) * rng.lognormal(0, 0.02, size=tt.shape)
    return allv, frt
