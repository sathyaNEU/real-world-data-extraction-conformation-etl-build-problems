"""Prototype world 2 for task214 architecture 2 (candidate G3): closed landfills, leachate ammonium (scaled).
Wells around a retired coal plant. Daily water levels (logger system), quarterly boron (laboratory).
C: continuing source, leachate from a lined ash cell opened mid-2023 leaking through a defect; the plume
   reaches C in late 2024 and its boron follows the cell's winter leachate head, every winter.
D: decoy, old ash fill (a fixed store sitting above the historical water table) reached only when the
   water table, recovering after the plant shut its production wells in June 2023, climbs past the
   highest level it has reached at that well.
"""
import numpy as np, pandas as pd

LIMIT = 700.0
START, END = "2012-01-01", "2027-12-31"
WIN0, WIN1 = pd.Timestamp("2024-01-01"), pd.Timestamp("2027-12-31")
SHUT = pd.Timestamp("2023-06-15")
CELL = pd.Timestamp("2023-07-01")


def wetness(rng):
    yrs = list(range(2011, 2029)); w = {}; x = 0.0
    for y in yrs:
        x = 0.45 * x + rng.normal(0, 0.5); w[y] = x
    w[2014] = max(w.values()) + rng.uniform(1.0, 1.3)
    w[2022] = min(w[2022], -0.8 + rng.normal(0, 0.1)); w[2023] = min(w[2023], -0.6 + rng.normal(0, 0.1))
    for y in range(2015, 2024):
        w[y] = min(w[y], 0.05 + rng.normal(0, 0.05))
    w[2024] = 1.00 + rng.normal(0, 0.05); w[2025] = 0.45 + rng.normal(0, 0.05)
    w[2026] = 0.35 + rng.normal(0, 0.05); w[2027] = 0.75 + rng.normal(0, 0.05)
    for y in (2024, 2025, 2026, 2027):
        w[y] = min(w[y], w[2014] - 0.9)
    return w


def make(seed, P=None):
    P = P or {}
    rng = np.random.default_rng(seed)
    days = pd.date_range(START, END, freq="D"); n = len(days)
    doy = days.dayofyear.values
    seas = np.cos(2 * np.pi * (doy - 105) / 365.25)                 # peak about 15 April
    wy = np.where(days.month.values >= 10, days.year.values + 1, days.year.values)   # water year
    W = wetness(rng)
    wv = pd.Series([W[y] for y in wy]).rolling(61, center=True, min_periods=1).mean().values
    tyr = (days - SHUT).days.values / 365.25
    spec = [  # name, role, base, amp, gain, rebound depth
        ("UG-1", "bg", 41.0, 0.6, 0.55, 0.0), ("UG-2", "bg", 40.2, 0.5, 0.5, 0.0),
        ("C", "true", 36.0, 0.7, 0.8, 0.0),
        ("D", "decoy", 35.0, 0.6, 0.6, P.get("rebound_D", rng.uniform(2.7, 3.3))),
        ("D2", "decoy", 35.3, 0.55, 0.6, rng.uniform(2.4, 3.0)),
        ("D3", "decoy", 35.1, 0.6, 0.6, rng.uniform(2.5, 3.1)),
        ("F2", "finite_small_rebound", 35.6, 0.55, 0.55, 0.3), ("R", "rebound_nostore", 34.6, 0.6, 0.6, rng.uniform(2.5, 3.1)),
        ("N1", "clean", 36.8, 0.6, 0.6, 0.2), ("N2", "clean", 36.3, 0.5, 0.55, 0.0),
        ("N3", "natural", 35.9, 0.65, 0.6, 0.4), ("N4", "clean", 37.2, 0.55, 0.5, 0.0)]
    tau = P.get("tau", 1.4)
    lev = {}
    for name, role, base, amp, gain, dep in spec:
        x = base + amp * seas * (1 + 0.25 * wv) + gain * wv
        x = x + pd.Series(rng.normal(0, 0.05, n)).rolling(9, center=True, min_periods=1).mean().values
        if dep:
            x = x - dep + dep * np.where(tyr > 0, 1 - np.exp(-tyr / tau), 0)
        if role == "true":
            pass
        lev[name] = x
    # leachate head in the new cell: winter rain on the open cell, from July 2023
    hd = np.maximum(0, np.cos(2 * np.pi * (doy - 55) / 365.25) - 0.25) * (1 + 0.6 * wv)
    hd = np.where(days >= CELL, hd, 0.0)
    arrive = pd.Timestamp("2024-10-01") + pd.Timedelta(days=int(rng.integers(-40, 40)))
    ev = []
    for y in range(2012, 2028):
        for m, d in ((1, 15), (4, 15), (7, 15), (10, 15)):
            ev.append(pd.Timestamp(y, m, d) + pd.Timedelta(days=int(rng.integers(-6, 7))))
    k = np.arange(0, 70); g = (k / 21.0) ** 2 * np.exp(-2 * (k / 21.0 - 1)); g /= g.max()
    rows = []
    xc = pd.Series(lev["C"], index=days)
    pk = xc.groupby(wy).max()                      # water-year peaks at C
    ctx = {"zc": pk.loc[2025] + P.get("zc_gap", 0.03)}
    for name, role, *_ in spec:
        x = lev[name]; L = pd.Series(x, index=days)
        bg = {"bg": 55, "true": 70, "decoy": 80, "finite_small_rebound": 85, "rebound_nostore": 75,
              "clean": 90, "natural": 160}[role] * np.exp(rng.normal(0, 0.1))
        flush = np.zeros(n)
        if role in ("decoy", "finite_small_rebound"):
            floor = L[: "2013-12-31"].max() + 0.02                       # made ground sits above the 2012-13 water table
            above = np.maximum(L.cummax().values, floor)
            inc = np.diff(np.r_[above[0], above])
            dens = P.get("store_D", 15000.0) * (1 + 1.2 * np.clip((above - floor) / 3.0, 0, 2))
            flush = np.convolve(inc * dens, g)[:n]
        lag = int(P.get("lag", 45))
        for t in ev:
            i = (t - days[0]).days
            sd = 0.25 if role == "bg" else 0.18
            c = bg * np.exp(rng.normal(0, sd)) * (np.exp(0.35 * (x[i] - np.mean(x))) if role == "true" else 1.0)
            if role == "decoy":   # alluvial natural ammonium tracking the water table, below the limit
                c = 110 * np.exp(0.6 * (x[i] - np.mean(x))) * np.exp(rng.normal(0, 0.04))
            if role == "natural":
                c = 110 * np.exp(0.6 * (x[i] - np.mean(x))) * np.exp(rng.normal(0, 0.03))
            c += flush[i] * np.exp(rng.normal(0, 0.15))
            if role == "true":
                # waste base in contact only above zc (threshold contact)
                c += P.get("c_gain", 7000.0) * max(0.0, x[i] - ctx["zc"]) * np.exp(rng.normal(0, 0.15))
            rows.append((name, role, t, x[i], round(c, 0)))
    S = pd.DataFrame(rows, columns=["well", "role", "date", "level", "boron"])
    return S, pd.DataFrame(lev, index=days)
