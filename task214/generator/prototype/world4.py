"""Candidate 4, world 1 (task214 architecture 2): a retired US coal plant's ash units, arrangement only.

Daily water levels (logger system) and quarterly boron with a field water level at sampling (laboratory system).
The plant's production wells pumped until SHUT; every well near the plant recovers after it (the ordinary cause).
A river flood in spring 2019 lifts the wells beside the river (the pond side) far more than the inland wells.

  C   (pond unit, true): ash left in the closed pond's base is a continuing source; whenever groundwater stands
      above the base (z_c) boron answers, every time. Its highest level is the 2019 flood; its window peaks
      rise with the recovery but stay below it.
  D, D2, D3 (fill unit, decoy): old ash fill under the former coal yard, a fixed store above the pumped water
      table. It answers only when groundwater climbs past every earlier height (2019 bump first, then each
      window year as the recovery continues), and that slice is then spent. Natural level-tracking background.
  F2  (north unit): a small fixed store reached by a small recovery.
  R   (north unit): recovers strongly, no store.  N1..N5 clean, N3 natural, UG-1/UG-2 upgradient.

Both C and the D wells exceed in the 2019 spring sample and once in each window year: the same years and the
same counts; only the order of each unit's own peaks (C's highest first, D's rising) separates them.
"""
import numpy as np, pandas as pd

LIMIT = 700.0
START, END = "2012-01-01", "2027-12-31"
WIN0, WIN1 = pd.Timestamp("2024-01-01"), pd.Timestamp("2027-12-31")
SHUT = pd.Timestamp("2023-06-15")
UNIT = {"C": "pond", "N2": "pond", "N5": "pond",
        "D": "fill", "D2": "fill", "D3": "fill", "N1": "fill",
        "F2": "north", "R": "north", "N3": "north", "N4": "north",
        "UG-1": "upgradient", "UG-2": "upgradient"}
TRUE, DECOY = "pond", "fill"

DEF = dict(
    dep_C=(2.3, 2.7), tau_C=(0.9, 1.2), dep_D=(2.8, 3.2), tau_D=(1.8, 2.4),
    flood_C=(3.3, 3.7), flood_D=(0.75, 0.95), flood_day=(-6, 6),
    zc_h1=(0.22, 0.32),          # C's base sits this far below its 2024 spring peak
    floor_gap=(0.08, 0.14),      # the fill base sits this far below each D well's 2019 flood peak
    c_sat=1500.0, c_scale=0.25,  # C's contact response: c_sat * (1 - exp(-(x - z_c) / c_scale))
    store=2600.0, dens_slope=0.9, dens_scale=1.0,   # D's flush per metre of new height, rising with height
    kpk=21.0,                    # flush kernel peak (days)
    bgD=330.0, bgD_k=0.55, bgD_sd=(0.03, 0.06, 0.10),  # D wells' natural level-tracking background
    bgC=95.0, bgC_k=0.35, bgC_sd=0.10,
)


def U(rng, lohi):
    return rng.uniform(*lohi) if isinstance(lohi, tuple) else lohi


def wetness(rng):
    w = {}; x = 0.0
    for y in range(2011, 2029):
        x = 0.45 * x + rng.normal(0, 0.4); w[y] = float(np.clip(x, -0.9, 0.6))
    w[2012] = -0.9 + rng.normal(0, 0.05)          # the 2012 drought
    w[2019] = 0.75 + rng.normal(0, 0.05)          # the wet spring of the flood
    for y in (2024, 2025, 2026, 2027):            # ordinary to wet recovery years, close together
        w[y] = 0.25 + rng.normal(0, 0.06)
    return w


def flood_pulse(days, rng, P):
    pk = pd.Timestamp("2019-04-24") + pd.Timedelta(days=int(rng.integers(*P["flood_day"])))
    t = (days - pk).days.values.astype(float)
    rise = np.clip(1 + t / 22.0, 0, 1)                         # 22 days of rise
    fall = np.clip(1 - (t - 26) / 36.0, 0, 1)                  # 26 days near crest, 36 days of recession
    return np.where(t <= 0, rise, np.where(t <= 26, 1.0, fall)) ** 1.0


def make(seed, P=None):
    P = {**DEF, **(P or {})}
    rng = np.random.default_rng(seed)
    days = pd.date_range(START, END, freq="D"); n = len(days)
    doy = days.dayofyear.values
    seas = np.cos(2 * np.pi * (doy - 105) / 365.25)
    wy = np.where(days.month.values >= 10, days.year.values + 1, days.year.values)
    W = wetness(rng)
    wv = pd.Series([W[y] for y in wy]).rolling(61, center=True, min_periods=1).mean().values
    tyr = (days - SHUT).days.values / 365.25
    F = flood_pulse(days, rng, P)
    # name, base, amp, gain, dep, tau, flood amplitude
    spec = {
        "UG-1": (41.0, 0.55, 0.5, 0.3, 1.0, 0.2), "UG-2": (40.2, 0.5, 0.5, 0.25, 1.0, 0.2),
        "C": (36.0, 0.62, 0.55, U(rng, P["dep_C"]), U(rng, P["tau_C"]), U(rng, P["flood_C"])),
        "N2": (36.4, 0.6, 0.55, 2.4, 1.0, 3.0), "N5": (36.9, 0.6, 0.55, 2.2, 1.0, 2.6),
        "D": (35.0, 0.6, 0.55, U(rng, P["dep_D"]), U(rng, P["tau_D"]), U(rng, P["flood_D"])),
        "D2": (35.3, 0.58, 0.55, U(rng, P["dep_D"]), U(rng, P["tau_D"]), U(rng, P["flood_D"])),
        "D3": (35.1, 0.6, 0.55, U(rng, P["dep_D"]), U(rng, P["tau_D"]), U(rng, P["flood_D"])),
        "N1": (36.8, 0.6, 0.6, 2.9, 2.0, 0.8),
        "F2": (35.6, 0.55, 0.55, rng.uniform(0.9, 1.1), 1.5, 0.5), "R": (34.6, 0.6, 0.6, rng.uniform(2.6, 3.1), 2.0, 0.6),
        "N3": (35.9, 0.65, 0.6, 1.0, 1.5, 0.6), "N4": (37.2, 0.55, 0.5, 0.8, 1.5, 0.5),
    }
    lev = {}
    for w, (base, amp, gain, dep, tau, fa) in spec.items():
        x = base + amp * seas * (1 + 0.25 * wv) + gain * wv
        x = x + pd.Series(rng.normal(0, 0.05, n)).rolling(9, center=True, min_periods=1).mean().values
        x = x - dep * np.where(tyr > 0, np.exp(-np.maximum(tyr, 0) / tau), 1.0)
        x = x + fa * F
        lev[w] = x
    Lv = pd.DataFrame(lev, index=days)
    ev = []
    for y in range(2012, 2028):
        for m, d in ((1, 15), (4, 15), (7, 15), (10, 15)):
            ev.append(pd.Timestamp(y, m, d) + pd.Timedelta(days=int(rng.integers(-6, 7))))
    k = np.arange(0, 90); g = (k / P["kpk"]) ** 2 * np.exp(-2 * (k / P["kpk"] - 1)); g /= g.max()
    # C's base: below its 2024 spring peak by h1
    xc = Lv["C"]; pk24 = xc["2024-02-01":"2024-06-30"].max()
    zc = pk24 - U(rng, P["zc_h1"])
    rows = []; meta = {"zc": zc}
    for w in spec:
        x = lev[w]; L = Lv[w]; mx = float(np.mean(x))
        flush = np.zeros(n)
        if w in ("D", "D2", "D3", "F2"):
            floor = L["2019-03-01":"2019-07-31"].max() - (U(rng, P["floor_gap"]) if w != "F2" else 0.05)
            above = np.maximum(L.cummax().values, floor)
            inc = np.diff(np.r_[above[0], above])
            dens = P["store"] * (1 + P["dens_slope"] * np.clip((above - floor) / P["dens_scale"], 0, 3))
            if w == "F2":
                dens = dens * 0.5
            flush = np.convolve(inc * dens, g)[:n]
            meta[w] = floor
        sdD = dict(zip(("D", "D2", "D3"), P["bgD_sd"]))
        bg0 = {"UG-1": 55, "UG-2": 60, "N1": 80, "N2": 85, "N4": 75, "N5": 90, "R": 85, "F2": 120}
        for t in ev:
            i = (t - days[0]).days
            if w in sdD:
                c = P["bgD"] * np.exp(P["bgD_k"] * (x[i] - mx)) * np.exp(rng.normal(0, sdD[w]))
            elif w == "C":
                c = P["bgC"] * np.exp(P["bgC_k"] * (x[i] - mx)) * np.exp(rng.normal(0, P["bgC_sd"]))
                if x[i] > zc:
                    c += P["c_sat"] * (1 - np.exp(-(x[i] - zc) / P["c_scale"])) * np.exp(rng.normal(0, 0.12))
            elif w == "N3":
                c = 160 * np.exp(0.6 * (x[i] - mx)) * np.exp(rng.normal(0, 0.08))
            else:
                c = bg0[w] * np.exp(rng.normal(0, 0.22 if w.startswith("UG") else 0.16))
            c += flush[i] * np.exp(rng.normal(0, 0.12))
            dip = x[i] + rng.normal(0, 0.02)                     # field water level at sampling
            rows.append((w, UNIT[w], t, dip, round(float(c), 0)))
    S = pd.DataFrame(rows, columns=["well", "unit", "date", "level", "boron"])
    return S, Lv, meta
