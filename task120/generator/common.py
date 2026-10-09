"""Shared helpers for the task120 generator: seeded streams, rank arithmetic, quantile
conventions, the assertion registry and the piecewise distribution sampler.

Nothing here touches the shipped bundle. The independent verifier (verify_pack.py) imports
nothing from this module.
"""
import math
import zlib

import numpy as np

SEED = 120
YEARS = (2022, 2023, 2024, 2025)
PCTS = (10, 5, 1)                  # top 10, 5 and 1 per cent
AS_OF = "2026-11-09"               # the prompt's moment
EXPORT_DATE = "2026-11-06"         # mtime of every shipped file (the share as assembled)
EXTRACT_DATE = "2026-10-22"        # the Department's TY2025 research extract


def stream(name):
    """A generator seeded from the build seed and a stable name, so adding a stream never
    moves another one."""
    return np.random.default_rng([SEED, zlib.crc32(name.encode())])


def k_top(n, pct):
    """Rank of the floor unit: ceil(n * pct / 100) in integers, never in floats."""
    return (n * pct + 99) // 100


def round_thousand(x):
    """Half up to the nearest $1,000 (x is never on a half: asserted where it is used)."""
    return int(math.floor(x / 1000.0 + 0.5)) * 1000


HF_METHODS = ("inverted_cdf", "averaged_inverted_cdf", "closest_observation",
              "interpolated_inverted_cdf", "hazen", "weibull", "linear",
              "median_unbiased", "normal_unbiased")


def floor_conventions(values, pct):
    """Every quantile convention a solver might use for the floor of the top pct per cent:
    nearest rank at k-1, k, k+1, Hyndman-Fan types 1 to 9 at 1 - pct/100, and the midpoint of
    ranks k and k+1. Returns a dict name -> value (float)."""
    v = np.sort(np.asarray(values, dtype=np.float64))[::-1]
    n = len(v)
    k = k_top(n, pct)
    out = {"rank_k-1": v[k - 2], "rank_k": v[k - 1], "rank_k+1": v[k],
           "midpoint_k_k+1": (v[k - 1] + v[k]) / 2.0}
    asc = v[::-1]
    q = 1.0 - pct / 100.0
    for m in HF_METHODS:
        out["hf_" + m] = float(np.quantile(asc, q, method=m))
    return out


class Checks:
    """Every assertion in the build goes through here, so the build can report its count and
    fail loudly at the first one that does not hold."""

    def __init__(self):
        self.items = []

    def __call__(self, cond, name, detail=""):
        ok = bool(cond)
        self.items.append((name, ok, str(detail)))
        if not ok:
            raise AssertionError(f"[{name}] {detail}")
        return ok

    def count(self):
        return len(self.items)

    def groups(self):
        out = {}
        for name, _, _ in self.items:
            g = name.split(".")[0]
            out[g] = out.get(g, 0) + 1
        return out


# ------------------------------------------------------------------ distribution sampler

def piecewise_values(anchors_desc, n, rng, top_cap_s=0.6):
    """Values for ranks 1..n (rank 1 the largest) from a survival function given at anchors.

    anchors_desc: list of (x, S, mode) with x descending and S ascending, S = count of units at or
    above x; mode 'log' interpolates log S against log x on the segment below this anchor,
    'lin' interpolates S against x. The last anchor must have S == n.

    Rank i takes the value at survival position i - u (u uniform), so the count of values at or
    above each anchor x equals S exactly before any rounding."""
    xs = np.array([a[0] for a in anchors_desc], dtype=np.float64)
    ss = np.array([a[1] for a in anchors_desc], dtype=np.float64)
    modes = [a[2] for a in anchors_desc]
    assert ss[-1] == n, (ss[-1], n)
    u = rng.random(n)
    s = np.arange(1, n + 1, dtype=np.float64) - u
    s[0] = max(s[0], top_cap_s)
    out = np.empty(n, dtype=np.float64)
    # above the first anchor: extend the first segment's slope
    for j in range(len(xs)):
        lo_s = ss[j - 1] if j > 0 else 0.0
        hi_s = ss[j]
        sel = (s > lo_s) & (s <= hi_s)
        if not sel.any():
            continue
        if j == 0:
            # extrapolate with the slope of segment (0,1)
            x0, x1, s0, s1 = xs[0], xs[1], ss[0], ss[1]
            slope = (math.log(x1) - math.log(x0)) / (math.log(s1) - math.log(s0))
            out[sel] = np.exp(math.log(x0) + (np.log(s[sel]) - math.log(s0)) * slope)
            continue
        x0, x1, s0, s1 = xs[j - 1], xs[j], ss[j - 1], ss[j]
        if modes[j] == "log":
            slope = (math.log(x1) - math.log(x0)) / (math.log(s1) - math.log(s0))
            out[sel] = np.exp(math.log(x0) + (np.log(s[sel]) - math.log(s0)) * slope)
        else:
            out[sel] = x0 + (s[sel] - s0) * (x1 - x0) / (s1 - s0)
    return out


# ------------------------------------------------------------------ identifiers

def make_tins(rng, n):
    """Unique nine-digit SSN-shaped numbers (area 100-899 except 666, group 01-99, serial
    0001-9999), so no TIN carries a leading zero in any file."""
    got = np.empty(0, dtype=np.int64)
    while len(got) < n:
        m = int((n - len(got)) * 1.15) + 1000
        area = rng.integers(100, 900, m)
        area = area[area != 666]
        k = len(area)
        group = rng.integers(1, 100, k)
        serial = rng.integers(1, 10000, k)
        cand = area * 1_000_000 + group * 10_000 + serial
        got = np.concatenate([got, cand])
        _, first = np.unique(got, return_index=True)
        got = got[np.sort(first)]
    return got[:n]


def make_itins(rng, n, avoid):
    out = set()
    avoid = set(avoid.tolist()) if hasattr(avoid, "tolist") else set(avoid)
    groups = list(range(70, 89)) + [90, 91, 92] + list(range(94, 100))
    while len(out) < n:
        v = (900 + int(rng.integers(0, 100))) * 1_000_000 + int(rng.choice(groups)) * 10_000 + int(rng.integers(1, 10000))
        if v not in avoid:
            out.add(v)
    return np.array(sorted(out), dtype=np.int64)[rng.permutation(n)]


EIN_PREFIXES = [10, 11, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34,
                35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57,
                58, 59, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 81, 82, 83,
                84, 85, 86, 87, 88, 91, 92, 93, 94, 95, 98, 99]


def make_eins(rng, n):
    seen, out = set(), []
    while len(out) < n:
        v = int(rng.choice(EIN_PREFIXES)) * 10_000_000 + int(rng.integers(0, 10_000_000))
        if v not in seen:
            seen.add(v)
            out.append(v)
    return np.array(out, dtype=np.int64)


def tin_str(a):
    return np.char.zfill(np.asarray(a).astype(np.int64).astype(str), 9)
