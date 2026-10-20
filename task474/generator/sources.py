"""The clean truth: every monitored unit's 2026 hour by hour (standard time): running or not, gross load, heat input,
the NOx it emitted, and whether the analyzers were measuring. Nothing here knows about files or mess."""
import datetime as dt

import numpy as np

import world as W

T0 = dt.datetime(2026, 1, 1)
NH = 8760
HOURS = [T0 + dt.timedelta(hours=h) for h in range(NH)]
IN_SEASON = np.array([W.SEASON[0] <= t.date() <= W.SEASON[1] for t in HOURS])
START_W = np.array([0.0, .50, .33, .17])           # share of a start's excess NOx in hours 1, 2 and 3 after it
RAMP = np.array([1.0, .32, .58, .83])              # load in hours 1 to 3 as a share of the dispatched level


def schedule(rng, spw, run):
    """Running hours: starts arrive at the season's rate (half of it outside the season), runs last about `run`."""
    on = np.zeros(NH, bool)
    h = int(rng.integers(0, 30))
    while h < NH:
        rate = spw / 168 * (1.0 if IN_SEASON[h] else .5)
        if rng.random() < rate * 3:
            d = max(4, int(rng.gamma(2.0, run / 2.0)))
            on[h:h + d] = True
            h += d + int(rng.integers(5, 36))
        else:
            h += 3
    return on


def since_start(on):
    s = np.zeros(NH, int)
    c = 0
    for h in range(NH):
        c = c + 1 if on[h] else 0
        s[h] = c
    return s


def cc_unit(rng, key):
    plant, n, cap, spw, base, slb, pms, pmo, run = W.CC[key]
    adj = W.ADJ.get(key, 1.0)
    on = schedule(rng, spw, run)
    s = since_start(on)
    lvl = np.clip(rng.normal(.74, .14, NH), .42, 1.0)
    load = np.where(on, cap * lvl, 0.0)
    load = np.where((s >= 1) & (s <= 3), load * RAMP[np.minimum(s, 3)], load)
    load = np.round(load, 2)
    low = np.clip((cap * .72 - load) / cap, 0, 1)
    lb = np.where(on, base * load * (1 + .7 * low) * np.exp(rng.normal(0, .09, NH)), 0.0)
    st = (s >= 1) & (s <= 3)
    # each unit's own start-up shape, and each start its own size (how long the unit was down, how the operators
    # brought it up)
    vr = np.random.default_rng([W.SEED, 31, n, cap])
    shape = START_W * np.exp(vr.normal(0, .5, 4))
    shape = shape / shape[1:].sum()
    size = np.ones(NH)
    for h0 in np.where(s == 1)[0]:
        size[h0:h0 + 3] = np.exp(vr.normal(-.06, .35))
    lb = np.where(st, lb + adj * slb * shape[np.minimum(s, 3)] * size * np.exp(rng.normal(0, .22, NH)), lb)
    hr = np.where(on, 6.85 * (1 + .45 * low + np.where(st, .25, 0)) * np.exp(rng.normal(0, .02, NH)), 0)
    heat = np.round(load * hr, 1)
    # the analyzers: out for the first one to three hours after a start with chance pms (purge and calibration after
    # a shutdown), and in blocks of faults through the run at a rate giving about pmo of the other hours
    out = np.zeros(NH, bool)
    starts = np.where(s == 1)[0]
    for h in starts:
        if rng.random() < pms:
            out[h:h + int(rng.choice([1, 2, 3], p=[.12, .33, .55]))] = True
    h = 0
    while h < NH:
        if rng.random() < pmo / 9:
            out[h:h + int(rng.integers(1, 18))] = True
            h += 18
        h += 1
    out &= on
    status = np.where(~on, "OFF", np.where(out, rng.choice(["OOC", "MAINT", "CALFAIL", "COMM"], NH,
                                                          p=[.55, .15, .2, .1]), "OK"))
    return dict(on=on, since=s, load=load, heat=heat, lb=lb, out=out, status=status, plant=plant, cap=cap)


def other_unit(rng, key):
    plant, kind, cap = W.OTHER[key]
    spw, run, base, slb = (3.0, 7, .55, 160) if kind == "simple cycle" else (.05, 900, .35, 900)
    on = schedule(rng, spw, run)
    s = since_start(on)
    load = np.round(np.where(on, cap * np.clip(rng.normal(.8, .12, NH), .45, 1), 0.0), 1)
    lb = np.where(on, base * load * np.exp(rng.normal(0, .1, NH)), 0.0)
    lb = np.where((s >= 1) & (s <= 2), lb + slb * .5, lb)
    hrng = np.random.default_rng([W.SEED, 51, cap])
    heat = np.round(load * np.where(on, (10.4 if kind == "simple cycle" else 10.1) *
                                    np.exp(hrng.normal(0, .025, NH)), 0), 1)
    out = on & (rng.random(NH) < .03)
    status = np.where(~on, "OFF", np.where(out, "OOC", "OK"))
    return dict(on=on, since=s, load=load, heat=heat, lb=lb, out=out, status=status, plant=plant, cap=cap)


def air_events(rng, units):
    """Plant instrument air losses: the header trips on hot afternoons (the compressor's discharge temperature), mostly
    while the plant's units run, and is back after a few hours. {plant: [(first hour, hours)]}."""
    ev = {}
    for plant, (n, mean) in W.AIR.items():
        us = [u for u in units if units[u]["plant"] == plant]
        on = np.array([units[u]["on"] for u in us])
        steady = np.array([units[u]["since"] >= 4 for u in us])
        run = np.where(on.any(axis=0) & (steady | ~on).all(axis=0) & IN_SEASON)[0]
        hs = []
        while len(hs) < n:
            h0 = int(rng.choice(run))
            if not 11 <= HOURS[h0].hour <= 17 or any(abs(h0 - a) < 30 for a, _ in hs):
                continue
            hs.append((h0, int(max(2, round(rng.gamma(4.0, mean / 4.0))))))
        ev[plant] = sorted(hs)
    return ev


def apply_air(rng, x, events, unc):
    """While the header is down the analyzers' dilution probes have no air and the SCR's ammonia flow valves close, so
    the unit runs uncontrolled and unmeasured; the probes come back with the air, and ammonia injection resumes once
    the vaporizer is back to temperature, an hour or two later, so the first measured hours are still uncontrolled."""
    on, heat = x["on"], x["heat"]
    air = np.zeros(NH, bool)
    tail = np.zeros(NH, float)
    for h0, d in events:
        air[h0:h0 + d] = True
        k = h0 + d
        if k < NH:
            tail[k] = 1.0
        if k + 1 < NH and rng.random() < .5:
            tail[k + 1] = rng.uniform(.25, .7)
    air &= on
    tail = np.where(on & ~air, tail, 0.0)
    free = unc * heat * np.exp(rng.normal(0, .045, NH))
    x["lb"] = np.where(air, free, np.where(tail > 0, tail * free + (1 - tail) * x["lb"], x["lb"]))
    x["out"] = np.where(tail > 0, False, x["out"]) | air
    x["status"] = np.where(air, rng.choice(["OOC", "MAINT", "CALFAIL", "COMM"], NH, p=[.55, .15, .2, .1]),
                           np.where(tail > 0, "OK", x["status"]))
    x["air"], x["tail"] = air, tail
    return x


def fleet(rng):
    units = {k: cc_unit(rng, k) for k in W.CC}
    units.update({k: other_unit(rng, k) for k in W.OTHER})
    ev = air_events(rng, {k: v for k, v in units.items() if k in W.CC})
    for k in W.CC:
        units[k] = apply_air(rng, units[k], ev[units[k]["plant"]], W.UNC[k])
        units[k]["air_events"] = ev[units[k]["plant"]]
    # one status for the whole of each outage: the DAHS flags an outage by its cause, not hour by hour
    srng = np.random.default_rng(W.SEED + 5)
    for k in units:
        x = units[k]
        st = np.array(x["status"], dtype=object)
        h = 0
        while h < NH:
            if x["on"][h] and x["out"][h]:
                j = h
                while j + 1 < NH and x["on"][j + 1] and x["out"][j + 1]:
                    j += 1
                p = [.7, .1, .1, .1] if x.get("air", np.zeros(NH, bool))[h] else [.55, .15, .2, .1]
                st[h:j + 1] = str(srng.choice(["OOC", "MAINT", "CALFAIL", "COMM"], p=p))
                h = j
            h += 1
        x["status"] = st
    return units
