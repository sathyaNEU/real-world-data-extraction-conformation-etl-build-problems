"""Each node's true ozone (following its site), its head's span and zero over time, and its readings (ppb)."""
import datetime as dt
from zoneinfo import ZoneInfo
import numpy as np
import params as P
import nodes as N
import sim

MAD = ZoneInfo("Europe/Madrid")


def exposure():
    """Each field site's escape from the night's surface layer: the analysers and plain nodes none, hill nodes most."""
    ex = [0.0] * 4 + [N.HILL.get(m, 0.0) for _, m, _, _ in N.NODES]
    ex += [N.HILL.get(dict((c, m) for c, m, _, _ in N.NODES)[c], 0.0) for c in sorted(N.MOVES)]
    return ex


def sites():
    """The field's sites: the four analysers, the 36 node sites as installed, then the two sites nodes moved to."""
    s = [(a[2], a[3]) for a in P.ANALYSERS] + [(x, y) for _, _, x, y in N.NODES]
    s += [(N.MOVES[c][0], N.MOVES[c][1]) for c in sorted(N.MOVES)]
    return s


def local_to_index(d):
    return sim.index(dt.datetime(d.year, d.month, d.day, tzinfo=MAD).astimezone(P.UTC))


def window():
    return local_to_index(P.WINDOW_LOCAL[0]), local_to_index(P.WINDOW_LOCAL[1])


def node_true(true, code):
    i = N.CODES.index(code)
    s = true[4 + i].copy()
    if code in N.MOVES:
        j = 4 + 36 + sorted(N.MOVES).index(code)
        k = local_to_index(N.MOVES[code][2]) + 11      # the node went back up at about 11:00 local
        s[k:] = true[j, k:]
    return s


def paths(code):
    """Span and zero (ppb) by hour: set at installation, drifting linearly through the middle of the window."""
    i = N.CODES.index(code)
    t0 = local_to_index(N.install_date(i)) + 12
    w0, w1 = window()
    mid = (w0 + w1) / 2.0
    h = np.arange(sim.HOURS, dtype=float)
    frac = np.clip((h - t0) / (mid - t0), 0, None)
    r = np.random.default_rng(1000 + i)
    left = 1.0 + r.normal(0, 0.006)
    span = left + (N.SPAN[code] - left) * frac
    zero = r.normal(0, 0.4) + (N.ZERO[code]) * frac
    return t0, span, zero


def readings(true, code, half=False):
    """Hourly (or half-hourly, two columns) readings in ppb before rounding; NaN before installation."""
    i = N.CODES.index(code)
    t0, span, zero = paths(code)
    s = node_true(true, code)
    r = np.random.default_rng(2000 + i)
    if half:
        e = r.standard_normal((2, sim.HOURS)) * P.NODE_NOISE * np.sqrt(2.0)
        out = span * s + zero + e
        out[:, :t0] = np.nan
        return out
    out = span * s + zero + r.standard_normal(sim.HOURS) * P.NODE_NOISE
    out[:t0] = np.nan
    return out
