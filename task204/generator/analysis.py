#!/usr/bin/env python3
"""Every estimate of the Tulrohan Block's outdoor-air supply per occupant present, computed from one
session frame so that the rungs, the rival family and the golden family are all the same arithmetic on
the same rows.

A session frame is one dict per timetabled session: the space, the date, the period, the occupants
present, the session length in seconds and the carbon dioxide excess over the outdoor baseline at each
five-minute stamp from the session's first reading to its last, inclusive.

All rates are returned in litres per second per occupant present. The block aggregate is total outdoor
air supplied over total occupant-seconds.
"""
import math

import params as P

VOL = {s[0]: s[4] for s in P.SPACES}
G = P.GENERATION_M3_PER_S


# ----------------------------------------------------------------- quadratures

def trapz(vals, dt):
    if len(vals) < 2:
        return 0.0
    return dt * (sum(vals) - 0.5 * (vals[0] + vals[-1]))


def left_rect(vals, dt):
    return dt * sum(vals[:-1])


def right_rect(vals, dt):
    return dt * sum(vals[1:])


def simpson(vals, dt):
    n = len(vals) - 1
    if n < 2:
        return trapz(vals, dt)
    if n % 2:                      # fall back to the trapezoid on the last interval
        return simpson(vals[:-1], dt) + dt * 0.5 * (vals[-2] + vals[-1])
    tot = vals[0] + vals[-1]
    for i in range(1, n):
        tot += (4 if i % 2 else 2) * vals[i]
    return tot * dt / 3.0


def decimate(vals, every):
    out = vals[::every]
    if out[-1] != vals[-1]:
        out = out + [vals[-1]]
    return out


QUAD = {"trapezoid": trapz, "left rectangle": left_rect, "right rectangle": right_rect,
        "Simpson": simpson}


# ----------------------------------------------------------------- per-session supply estimates

def q_integrated(f, quad="trapezoid", every=1):
    """The session-integrated unsteady balance: the decisive construction.

    V dC/dt = 1e6 N G - Q C integrated across the session gives
    Q = (N G T - V dC) / integral(C dt), with the stored term carrying its own sign.
    """
    vals = f["readings"] if every == 1 else decimate(f["readings"], every)
    dt = f["seconds"] / (len(vals) - 1)
    integral = QUAD[quad](vals, dt) * 1e-6
    if integral <= 0:
        return None
    stored = VOL[f["space"]] * (vals[-1] - vals[0]) * 1e-6
    generated = f["occupants"] * G * f["seconds"]
    return (generated - stored) / integral


def q_regression(frames):
    """The same balance fitted step by step instead of integrated: regress the volume-weighted
    derivative on the excess, per space, through the generation term."""
    num, den = {}, {}
    for f in frames:
        vals, V = f["readings"], VOL[f["space"]]
        dt = f["seconds"] / (len(vals) - 1)
        for i in range(len(vals) - 1):
            y = V * (vals[i + 1] - vals[i]) * 1e-6 / dt
            x = 0.5 * (vals[i] + vals[i + 1]) * 1e-6
            g = f["occupants"] * G
            num[f["space"]] = num.get(f["space"], 0.0) + x * (g - y)
            den[f["space"]] = den.get(f["space"], 0.0) + x * x
    return {k: num[k] / den[k] for k in num if den[k] > 0}


def q_steady(f, basis="session mean"):
    """The field's steady-state read: the per-person generation rate divided by the excess, which
    holds only where the space has settled."""
    vals = f["readings"]
    dt = f["seconds"] / (len(vals) - 1)
    if basis == "session mean":
        c = trapz(vals, dt) / f["seconds"]
    elif basis == "final 15 minutes":
        c = sum(vals[-4:]) / len(vals[-4:])
    elif basis == "last sample":
        c = vals[-1]
    elif basis == "peak sample":
        c = max(vals)
    elif basis == "median sample":
        s = sorted(vals)
        n = len(s)
        c = s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])
    elif basis == "95th percentile":
        s = sorted(vals)
        c = s[min(len(s) - 1, int(math.ceil(0.95 * len(s))) - 1)]
    else:
        raise ValueError(basis)
    if c <= 0:
        return None
    return f["occupants"] * G / (c * 1e-6)


# ----------------------------------------------------------------- aggregation

def aggregate(frames, per_session_q, spaces=None):
    """Total outdoor air supplied over total occupant-seconds, litres per second per occupant."""
    air = occ_s = 0.0
    for f in frames:
        if spaces is not None and f["space"] not in spaces:
            continue
        q = per_session_q(f)
        if q is None:
            continue
        air += q * f["seconds"]
        occ_s += f["occupants"] * f["seconds"]
    return 1000.0 * air / occ_s if occ_s else None


def aggregate_mean_of_rates(frames, per_session_q, spaces=None):
    """An occupant-weighted mean of the session rates rather than a ratio of totals."""
    num = den = 0.0
    for f in frames:
        if spaces is not None and f["space"] not in spaces:
            continue
        q = per_session_q(f)
        if q is None or f["occupants"] == 0:
            continue
        w = f["occupants"] * f["seconds"]
        num += 1000.0 * q / f["occupants"] * w
        den += w
    return num / den if den else None


def per_space(frames, per_session_q):
    air, occ_s = {}, {}
    for f in frames:
        q = per_session_q(f)
        if q is None:
            continue
        air[f["space"]] = air.get(f["space"], 0.0) + q * f["seconds"]
        occ_s[f["space"]] = occ_s.get(f["space"], 0.0) + f["occupants"] * f["seconds"]
    return {k: 1000.0 * air[k] / occ_s[k] for k in air if occ_s.get(k)}


def block_frames(frames):
    return [f for f in frames if f["space"] in P.BLOCK_SPACES]


# ----------------------------------------------------------------- the named readings

def golden(frames):
    return aggregate(block_frames(frames), lambda f: q_integrated(f))


def rung(frames, name):
    basis = {"R0": "session mean", "R1": "final 15 minutes", "R2": "peak sample"}[name]
    return aggregate(block_frames(frames), lambda f: q_steady(f, basis))


def rival_family(frames):
    out = {}
    for basis in ("session mean", "final 15 minutes", "last sample", "peak sample",
                  "median sample", "95th percentile"):
        out[basis] = aggregate(block_frames(frames), lambda f, b=basis: q_steady(f, b))
    return out


def golden_family(frames):
    bf = block_frames(frames)
    out = {}
    for quad in QUAD:
        out["%s quadrature" % quad] = aggregate(bf, lambda f, q=quad: q_integrated(f, quad=q))
    for every in (2, 3):
        out["%d minute decimation" % (5 * every)] = aggregate(
            bf, lambda f, e=every: q_integrated(f, every=e))
    reg = q_regression(bf)
    air = occ_s = 0.0
    for f in bf:
        air += reg[f["space"]] * f["seconds"]
        occ_s += f["occupants"] * f["seconds"]
    out["derivative regression"] = 1000.0 * air / occ_s
    return out


def rounded(v, bin_=None):
    b = bin_ or P.RATE_BIN
    return round(v / b) * b


def bin_edge_distance(v, bin_=None):
    """Distance from v to the nearest edge of its printed cell (determinism-check section 3)."""
    b = bin_ or P.RATE_BIN
    centre = round(v / b) * b
    return b / 2.0 - abs(v - centre)
