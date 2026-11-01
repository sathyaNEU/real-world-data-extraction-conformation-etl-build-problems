"""The world's clean truth for task138 architecture 2.

Annual peaks: every water year's main flood is drawn at Coyle Bridge; it reaches Orrinsford with the intervening
area's contribution added and, while the old agricultural levees still overtopped, less the share of every cfs above
their overtopping level that the floodplain behind them held back. Each district's crown raise takes its floodplain
out of that storage from the next water year, so from water year 2009 the reach passes every flood the way it does
today. A few years' Orrinsford peak came from a storm on the intervening area alone.

Everything else the pack carries is drawn here too: the hydraulic study's water surface table, the Orrinsford levee's
2024 and 2016 crown surveys, the benchmark list, the levee inventory, ten water years of hourly telemetry at both
gauges, the other basin gauges and the distractors.
"""
import math

import numpy as np
import pandas as pd
from scipy import stats

import lp3 as L
import params as PR


# ------------------------------------------------------------------ annual peaks
def floodplain_share(wy):
    """Share of the reach's agricultural floodplain still behind the old (overtopping) levees in water year wy."""
    tot = sum(d[7] for d in PR.DISTRICTS)
    still = sum(d[7] for d in PR.DISTRICTS if d[6] >= wy)
    return still / tot


def _season_day(rng):
    """Day of the water year (0 = 1 October) of a main flood: mostly March to June, some autumn and summer."""
    u = rng.random()
    if u < 0.78:
        return int(np.clip(rng.normal(205, 32), 150, 275))
    if u < 0.90:
        return int(np.clip(rng.normal(285, 18), 260, 330))
    return int(np.clip(rng.normal(45, 20), 5, 100))


def peaks(seed=None):
    rng = np.random.default_rng(PR.SEED if seed is None else seed)
    rows = []
    for wy in range(PR.FIRST_WY, PR.LAST_WY + 1):
        z = float(stats.pearson3.rvs(PR.COY_LOG_SKEW, random_state=rng))
        u = 10 ** (PR.COY_LOG_MEAN + PR.COY_LOG_SD * z)
        day = _season_day(rng)
        hour = int(rng.integers(0, 24))
        r = float(np.clip(rng.normal(PR.LOCAL_MEAN, PR.LOCAL_SD), PR.LOCAL_LO, PR.LOCAL_HI))
        f = floodplain_share(wy)
        held = PR.ATTEN * (1 - PR.ATTEN_SPREAD / 2 + PR.ATTEN_SPREAD * rng.random())
        over = max(u - PR.OVERTOP_CFS, 0.0)
        t_main = (u * (1 + r) - held * f * over) * (1 + rng.normal(0, PR.NOISE_T))
        lag_h = int(round(30 + 14 * rng.random() + 10 * f * min(over / 30000.0, 1.0)))
        local = rng.random() < PR.LOCAL_EVENT_P
        t_loc = float(rng.uniform(0.48, 0.78) * 10 ** PR.COY_LOG_MEAN) if local else 0.0
        if local and t_loc > t_main:
            lday = int(np.clip(day + rng.integers(-60, 60), 0, 364))
            t_day, t_hour, t_val, src = lday, int(rng.integers(0, 24)), t_loc, "local"
        else:
            t_day, t_hour, t_val, src = day, hour, t_main, "main"
        start = pd.Timestamp(year=wy - 1, month=10, day=1)
        c_time = start + pd.Timedelta(days=day, hours=hour)
        h_time = (start + pd.Timedelta(days=t_day, hours=t_hour)
                  + (pd.Timedelta(hours=lag_h) if src == "main" else pd.Timedelta(0)))
        rows.append({"wy": wy, "coy_q": u, "coy_time": c_time, "hal_q": t_val, "hal_time": h_time, "src": src,
                     "share": f, "local_r": r, "held": held, "lag_h": lag_h, "t_present": u * (1 + r)})
    return pd.DataFrame(rows)


def sig3(x):
    """The gauging agency's published precision: three significant figures."""
    x = float(x)
    if x <= 0:
        return 0
    d = int(math.floor(math.log10(x))) - 2
    return int(round(x / 10 ** d) * 10 ** d) if d > 0 else int(round(x))


# ------------------------------------------------------------------ hydraulics
# the water surface falls more steeply through some reaches than others (the step-backwater model's profile)
REACH_SLOPES = [(0, 2000, 0.000232), (2000, 4500, 0.000187), (4500, 6240, 0.000262), (6240, 8500, 0.000205),
                (8500, 11870, 0.000176), (11870, 13500, 0.000248), (13500, 16000, 0.000221), (16000, 18000, 0.000196)]


def fall(sta):
    """Water-surface fall (ft) from a station to the levee's downstream end."""
    tot = 0.0
    for a, b, s in REACH_SLOPES:
        lo = max(a, sta)
        if b > lo:
            tot += s * (b - lo)
    return tot


def _xs_params():
    """Each modelled cross-section's own departure from the reach profile: a depth factor and an offset that grows or
    shrinks with discharge (expansions, contractions, the floodwall reach)."""
    rng = np.random.default_rng(PR.OTHER_SEED + 11)
    out = {}
    for s in PR.TABLE4_STATIONS:
        out[s] = (1.0 + rng.normal(0, 0.009), rng.normal(0, 0.07), rng.normal(0, 0.06))
    return out


XS = _xs_params()


def wse(q, sta):
    """Design water surface (ft NAVD 88) at a cross-section for a discharge (the 2019 hydraulic study's model)."""
    k, o0, oq = XS.get(sta, (1.0, 0.0, 0.0))
    z = PR.WS_BASE_Z + fall(sta) + PR.WS_C * k * (q / 10000.0) ** PR.WS_EXP + o0 + oq * (q / 100000.0 - 1.0)
    if sta in PR.AFFLUX:
        a, b = PR.AFFLUX[sta]
        z += a + b * (q / 100000.0) ** 2
    return z


def table4():
    return pd.DataFrame([[round(wse(q, s), 2) for q in PR.TABLE4_Q] for s in PR.TABLE4_STATIONS],
                        index=PR.TABLE4_STATIONS, columns=PR.TABLE4_Q)


def table_wse(t4, q, sta):
    """Linear interpolation in discharge between Table 4 columns (the standard's rule)."""
    qs = list(t4.columns)
    row = t4.loc[sta].values
    return float(np.interp(q, qs, row))


def required_freeboard(sta):
    fb = PR.FREEBOARD_BRIDGE if any(abs(sta - b) <= 100 for b in PR.BRIDGES.values()) else PR.FREEBOARD
    return fb + PR.FREEBOARD_UPSTREAM_EXTRA * (1 - sta / PR.LEVEE_LEN_FT)


def wse_open(q, sta):
    """The reach profile without cross-section effects or bridge afflux (the grade the crown was built to follow)."""
    s = np.asarray(sta, float)
    f = np.vectorize(fall)(s) if s.ndim else fall(float(s))
    return PR.WS_BASE_Z + f + PR.WS_C * (q / 10000.0) ** PR.WS_EXP


def taper(sta):
    return PR.FREEBOARD_UPSTREAM_EXTRA * (1 - np.asarray(sta, float) / PR.LEVEE_LEN_FT)


def _wiggle(sta):
    """Smooth departure of the as-built crown from its design grade (ft)."""
    s = np.asarray(sta, float)
    return 0.16 * np.sin(2 * np.pi * s / 9300.0 + 0.6) + 0.09 * np.cos(2 * np.pi * s / 4100.0 + 1.3)


# low spots a certification survey finds (station, depth ft, half-width ft), none within 400 ft of a bridge
LOW_SPOTS = [(2650, 0.22, 150), (4880, 0.31, 120), (10250, 0.18, 200), (14700, 0.27, 140), (17250, 0.20, 160)]
TIE_IN_END = 350            # the 2019 north tie-in, built 0.35 ft above the old grade
FLOODWALL = (8500, 9700)    # the Cedar Street floodwall: a level top


def _relief(sta):
    s = np.asarray(sta, float)
    d = -sum(dep * np.exp(-((s - c) / w) ** 2) for c, dep, w in LOW_SPOTS)
    return d + np.where(s <= TIE_IN_END, 0.35, 0.0)


def golden_design_flood(pk):
    """The present river's 1 per cent flood at Orrinsford, the way the design note's golden builds it from the published
    (three-figure) peaks; used only to place the crown, a world parameter, so that the railroad bridge station needs
    NEED_11870 of raise."""
    wy = pk["wy"].values
    u = np.array([sig3(v) for v in pk["coy_q"]], float)
    t = np.array([sig3(v) for v in pk["hal_q"]], float)
    post = wy >= 2009
    r = np.sum(t[post] * u[post]) / np.sum(u[post] ** 2)
    ser = np.where(post, t, r * u)
    return L.quantile(L.fit(ser, PR.REGIONAL_SKEW, PR.REGIONAL_SKEW_MSE), PR.AEP)


def crown_true(t4, q_design):
    """The 2024 crown as a function of station: the design grade (the reach profile for the design flood, plus 3 ft,
    plus the upstream taper), a smooth as-built departure, the low spots, the 2019 tie-in and the floodwall's level
    top, placed so the railroad bridge station sits NEED_11870 below its requirement."""
    s0 = PR.BRIDGES["Prairie and Western Railroad bridge"]
    want = table_wse(t4, q_design, s0) + required_freeboard(s0) - PR.NEED_11870

    def grade(s):
        return wse_open(q_design, s) + PR.FREEBOARD + taper(s) + _wiggle(s)
    m0 = want - (float(grade(s0)) + float(_relief(s0)))
    wall = float(grade(FLOODWALL[0])) + 0.10

    def f(sta):
        s = np.asarray(sta, float)
        g = grade(s)
        g = np.where((s >= FLOODWALL[0]) & (s <= FLOODWALL[1]), wall, g)
        return g + m0 + _relief(s)
    return f


# ------------------------------------------------------------------ crown surveys
REACHES = [("R1", 0, 2000, "North tie-in to Pump Station 1"), ("R2", 2000, 4500, "Riverside Park"),
           ("R3", 4500, 6240, "Front Street to the Main Street closure"),
           ("R4", 6240, 8500, "Main Street closure to Cedar Street"),
           ("R5", 8500, 11870, "Cedar Street to the railroad closure"),
           ("R6", 11870, 13500, "Railroad closure to the grain terminal"),
           ("R7", 13500, 16000, "Grain terminal to Pump Station 2"),
           ("R8", 16000, 18001, "Pump Station 2 to the south tie-in")]
# crown settlement between the 2016 and 2024 surveys, ft (reach constants; the realised reach means are what the
# ask grades, and these are tuned so each sits mid-bin at 0.01 ft)
SETTLE = {"R1": 0.0686, "R2": 0.1214, "R3": 0.1588, "R4": 0.2106, "R5": 0.2889, "R6": 0.2450, "R7": 0.1408, "R8": 0.0898}
FEATURES = [(1830, "PS-1 OUTLET"), (6240, "MAIN ST CLOSURE"), (11870, "P&W RR CLOSURE"), (16120, "PS-2 OUTLET")]


def reach_of(sta):
    for name, a, b, _ in REACHES:
        if a <= sta < b:
            return name
    return None


def settle_at(sta, adj=None):
    adj = adj or {}
    r = reach_of(max(sta, 0))
    return SETTLE[r] + adj.get(r, 0.0) + 0.012 * math.sin(2 * math.pi * sta / 2700.0)


def crown2024(cf, rng):
    """2024 certification survey (NAVD 88, present stationing): every 100 ft along the centreline plus the
    structures; each point carries its reach."""
    rows = []
    for s in range(0, PR.LEVEE_LEN_FT + 1, 100):
        z = float(cf(s)) + rng.normal(0, 0.008)
        rows.append({"sta": s, "elev": round(z, 2), "code": "CL", "reach": reach_of(s)})
    for s, c in FEATURES:
        rows.append({"sta": s, "elev": round(float(cf(s)), 2), "code": c, "reach": reach_of(s)})
    df = pd.DataFrame(rows).sort_values(["sta", "code"]).reset_index(drop=True)
    return df


def crown2016(c24, cf, rng, adj=None):
    """2016 crown survey as the district's surveyor delivered it: every 100 ft on the stationing then in use (0+00 at
    the old north tie-in, 700 ft north of today's), elevations on NGVD 29, structures and benchmark check shots in
    the same list. Every shot on today's levee sits on a 2024 shot's position."""
    z24 = c24.set_index(["sta", "code"])["elev"]
    rows = []
    top = PR.LEVEE_LEN_FT + PR.OLD_STATION_SHIFT
    for o in range(0, top + 1, 100):
        s = o - PR.OLD_STATION_SHIFT
        if s >= 0:
            base = float(z24.loc[(s, "CL")])
        else:
            base = float(cf(0)) - 0.35 + 0.05 * (-s) / 700.0    # the old north tie-in, out of service since 2019
        navd = base + settle_at(s, adj) + rng.normal(0, 0.008)
        rows.append({"old_sta": o, "elev": round(navd - PR.NGVD_TO_NAVD, 2), "code": "CL"})
    for s, c in FEATURES:
        base = float(z24.loc[(s, c)])
        navd = base + settle_at(s, adj)
        rows.append({"old_sta": s + PR.OLD_STATION_SHIFT, "elev": round(navd - PR.NGVD_TO_NAVD, 2), "code": c})
    for bid, sta in (("OL-3", 6240), ("OL-6A", 11870)):
        bm = [b for b in BENCHMARKS if b[0] == bid][0]
        rows.append({"old_sta": sta + PR.OLD_STATION_SHIFT + 35, "elev": round(bm[2] + rng.normal(0, 0.004), 2),
                     "code": "BM %s CHK" % bid})
    return pd.DataFrame(rows).sort_values(["old_sta", "code"]).reset_index(drop=True)


BENCHMARKS = [
    # id, description, NGVD 29 elevation (ft), year set
    ("OL-1", "Brass disk in north wingwall, Pump Station 1 outlet", 612.84, 1964),
    ("OL-3", "Brass disk, Main Street bridge west abutment, top of curb", 624.37, 1964),
    ("OL-4", "Chiseled square, Cedar Street floodwall footing", 619.92, 1971),
    ("OL-6A", "Brass disk, P&W Railroad bridge north abutment (reset 1997)", 626.15, 1997),
    ("OL-11", "Rod mark in sleeve, Pump Station 2 control building", 611.48, 1988),
    ("TV-22", "Brass disk, County Road 14 culvert headwall", 638.71, 1957),
    ("TV-31", "Brass disk, Orrinsford water tower base", 641.06, 1959),
]


def benchmarks():
    return pd.DataFrame([{"id": b, "desc": d, "ngvd": z, "navd": round(z + PR.NGVD_TO_NAVD, 2), "set": y}
                         for b, d, z, y in BENCHMARKS])


# ------------------------------------------------------------------ telemetry
COY_EVENTS_EXTRA = [
    # (UTC peak at Coyle Bridge, Coyle peak cfs, departure of the Orrinsford/Coyle factor from the relation, lag hours,
    # rise hours) for the floods that were not a water year's annual peak; the annual peak floods come from the peaks
    ("2017-02-21 10:00", 15800, 0.002, 33, 46), ("2017-04-30 04:00", 17400, -0.003, 34, 52),
    ("2018-04-27 20:00", 11900, 0.001, 32, 44), ("2019-05-21 06:00", 19100, -0.002, 35, 50),
    ("2020-03-14 02:00", 42600, 0.003, 34, 58), ("2020-06-29 15:00", 35300, -0.001, 33, 54),
    ("2021-05-30 08:00", 16700, 0.002, 32, 47), ("2022-05-27 12:00", 21300, -0.003, 33, 49),
    ("2023-05-03 19:00", 12800, 0.001, 34, 45), ("2024-02-29 05:00", 38100, 0.002, 34, 56),
    ("2024-06-15 23:00", 49200, -0.002, 33, 60), ("2025-03-19 16:00", 22600, 0.003, 34, 50),
    ("2026-05-14 03:00", 17900, -0.001, 33, 48),
]
# a storm on the town's own tributaries while both Orrinsford loggers were running (UTC peak, cfs added, rise hours)
LOCAL_JUNE_2021 = ("2021-06-09 20:00", 2600.0, 20.0)


def _shape(t, tp, rise, k=3.2, tail=2.6, crest=0.8):
    """Unimodal flood shape, 0 to 1 at tp: a gamma-like rise over `rise` hours that still climbs into its crest hour
    (crest sets how sharply), and a slower recession."""
    tau = (t - (tp - rise)) / rise
    out = np.zeros_like(t, dtype=float)
    m = tau > 0
    x = tau[m]
    up = x ** k * np.exp(k * (1 - x)) * (1 - crest * (1 - x))
    out[m] = np.where(x <= 1, np.maximum(up, 0.0), np.exp(-(x - 1) * k / tail))
    return out


def coy_stage_old(q):
    a, b, c = PR.COY_RATING
    return a + b * np.power(np.maximum(q, 1.0), c)


def coy_q_at_stage_old(h):
    a, b, c = PR.COY_RATING
    return ((h - a) / b) ** (1.0 / c)


def hal_q_at_ws(z):
    from scipy.optimize import brentq
    return brentq(lambda q: wse(q, 6240) - z, 1000, 400000)


def _assemble(events, idx, t, base_c, base_h):
    qc = base_c.copy()
    qh = base_h.copy()
    t0 = idx[0]
    for e in events:
        ic = (e["tp_c"] - t0) / pd.Timedelta(hours=1)
        ih = (e["tp_h"] - t0) / pd.Timedelta(hours=1)
        sc = _shape(t, ic, e["rise"], crest=e["crest"])
        sh = _shape(t, ih, e["rise"] * 1.12, tail=2.9, crest=e["crest"])
        qc += (e["cp"] - float(np.interp(ic, t, base_c))) * sc
        qh += (e["hp"] - float(np.interp(ih, t, base_h))) * sh
    tl, add, rise = LOCAL_JUNE_2021
    qh += add * _shape(t, (pd.Timestamp(tl) - t0) / pd.Timedelta(hours=1), rise, crest=0.8)
    return qc, qh


def _crossing(series, thr, i0, i1):
    """First upward crossing of thr between hour indexes i0 and i1: (index of first hour at or above, fraction of
    the hour before it at which the straight line between the two readings meets thr)."""
    seg = series[i0:i1]
    above = np.nonzero(seg >= thr)[0]
    if len(above) == 0:
        return None
    j = i0 + int(above[0])
    lo, hi = series[j - 1], series[j]
    return j, (thr - lo) / (hi - lo)


def _unique_top(vals, i, w=72):
    """True when hour i is the only highest value within w hours either side."""
    lo, hi = max(i - w, 0), min(i + w + 1, len(vals))
    seg = vals[lo:hi]
    top = seg.max()
    return vals[i] == top and int(np.sum(seg == top)) == 1


def telemetry(pk):
    rng = np.random.default_rng(PR.TELEM_SEED)
    idx = pd.date_range(PR.TELEM_START, PR.TELEM_END, freq="h")
    n = len(idx)
    t = np.arange(n, dtype=float)
    doy = idx.dayofyear.values
    seas = 5600 + 3900 * np.cos(2 * np.pi * (doy - 112) / 365.25)
    drift = np.cumsum(rng.normal(0, 18, n))
    drift = drift - pd.Series(drift).rolling(24 * 45, min_periods=1, center=True).mean().values
    base_c = np.maximum(seas + drift * 0.6, 1600)
    base_h = base_c * (1.0 + PR.LOCAL_MEAN * 1.5) + 380
    events = []
    for _, r in pk[pk["wy"] >= 2017].iterrows():
        events.append({"tp_c": pd.Timestamp(r["coy_time"]) + pd.Timedelta(hours=6),   # standard time to UTC
                       "cp": float(sig3(r["coy_q"])),
                       "tp_h": pd.Timestamp(r["hal_time"]) + pd.Timedelta(hours=6),
                       "hp": float(sig3(r["hal_q"])), "rise": float(round(50 + 8 * rng.random())), "crest": 0.8,
                       "annual": int(r["wy"])})
    for ts, cp, dev, lag, rise in COY_EVENTS_EXTRA:
        tp = pd.Timestamp(ts)
        events.append({"tp_c": tp, "cp": float(cp), "tp_h": tp + pd.Timedelta(hours=lag),
                       "hp": float(round(cp * (1 + PR.LOCAL_MEAN + dev))), "rise": float(rise), "crest": 0.8,
                       "annual": 0})
    events.sort(key=lambda e: e["tp_c"])
    noise_c = rng.normal(0, 0.004, n)
    noise_h = rng.normal(0, 0.004, n)
    chg = idx >= pd.Timestamp(PR.COY_DATUM_CHANGE)
    warn_new = np.where(chg, PR.WARNING_STAGE_OLD + PR.COY_DATUM_SHIFT, PR.WARNING_STAGE_OLD)
    sill_stage = PR.MAIN_ST_SILL - PR.HAL_GAUGE_DATUM
    # free shape parameters per flood (its rise in whole hours, its crest's sharpness) are stepped until (a) every
    # flood that reaches the Main Street sill crosses the sill and the warning level inside an hour, the sill's
    # fraction 0.1 to 0.4 h later in its hour than the warning's, so every crossing and rounding convention gives one
    # whole-hour lead; (b) every annual peak is a single top hour in each shipped series
    for it in range(80):
        qc, qh = _assemble(events, idx, t, base_c, base_h)
        st_c = np.round(coy_stage_old(qc) + noise_c + np.where(chg, PR.COY_DATUM_SHIFT, 0.0), 2)
        st_h = np.round(wse(qh, 6240) + noise_h - PR.HAL_GAUGE_DATUM, 2)
        q3 = np.array([sig3(v) for v in qc])
        bad = False
        for e in events:
            ih = int((e["tp_h"] - idx[0]) / pd.Timedelta(hours=1))
            ic = int((e["tp_c"] - idx[0]) / pd.Timedelta(hours=1))
            if e["annual"]:
                jc = int(np.argmax(qc[max(ic - 72, 0):ic + 73])) + max(ic - 72, 0)
                jh = int(np.argmax(qh[max(ih - 72, 0):ih + 73])) + max(ih - 72, 0)
                ok = (_unique_top(st_c, jc) and _unique_top(q3, jc) and _unique_top(st_h, jh))
                if not ok:
                    e["crest"] = min(e["crest"] + 0.05, 1.0)
                    if e["crest"] >= 1.0:
                        e["rise"] += 1.0
                        e["crest"] = 0.8
                    bad = True
                    continue
            if e["hp"] < 30000:
                continue
            ch = _crossing(st_h, sill_stage, max(ih - 120, 1), ih + 1)
            cc = _crossing(st_c, warn_new[ic], max(ic - 120, 1), ic + 1)
            if ch is None or cc is None:
                continue
            fh, fc = ch[1], cc[1]
            ok = 0.1 <= fh <= 0.9 and 0.1 <= fc <= 0.9 and 0.1 <= fh - fc <= 0.4
            ok = ok and st_h[ch[0]] != sill_stage and st_c[cc[0]] != warn_new[ic]
            if not ok:
                e["rise"] += 1.0
                bad = True
        if not bad:
            break
    else:
        raise RuntimeError("telemetry shape search did not settle")
    # the hour each water year's annual peak sits on, as the agency's own record shows it (UTC)
    tops = {}
    for e in events:
        if e["annual"]:
            ih = int((e["tp_h"] - idx[0]) / pd.Timedelta(hours=1))
            ic = int((e["tp_c"] - idx[0]) / pd.Timedelta(hours=1))
            jc = int(np.argmax(qc[max(ic - 72, 0):ic + 73])) + max(ic - 72, 0)
            jh = int(np.argmax(qh[max(ih - 72, 0):ih + 73])) + max(ih - 72, 0)
            tops[e["annual"]] = (idx[jc], idx[jh])
    out = pd.DataFrame({"utc": idx, "qc": qc, "stage_c": st_c, "qh": qh, "stage_h": st_h})
    ev = pd.DataFrame(events)
    return out, ev, tops


# ------------------------------------------------------------------ the other basin gauges
def other_gauges(pk):
    """Annual peaks at Ashby (above Coyle Bridge), Gale Creek (a tributary, 1974-1996) and Fenwick (below Orrinsford,
    with the reach's levee history in it too)."""
    rng = np.random.default_rng(PR.OTHER_SEED)
    rows = []
    for _, r in pk.iterrows():
        wy = int(r["wy"])
        ash = r["coy_q"] * (0.80 + rng.normal(0, 0.035))
        rows.append(("ASH", wy, pd.Timestamp(r["coy_time"]) - pd.Timedelta(hours=int(18 + 8 * rng.random())), ash))
        if 1974 <= wy <= 1996:
            g = r["coy_q"] * (0.075 + rng.normal(0, 0.03)) + 600 * rng.random()
            rows.append(("GALE", wy, pd.Timestamp(r["coy_time"]) - pd.Timedelta(days=int(rng.integers(0, 6))),
                         max(g, 350)))
        if not (1977 <= wy <= 1979):
            fen = r["hal_q"] * (1.045 + rng.normal(0, 0.015))
            rows.append(("FEN", wy, pd.Timestamp(r["hal_time"]) + pd.Timedelta(hours=int(9 + 6 * rng.random())),
                         fen))
    return pd.DataFrame(rows, columns=["gauge", "wy", "time", "q"])


def simulate():
    pk = peaks()
    t4 = table4()
    qd = golden_design_flood(pk)
    cf = crown_true(t4, qd)
    rng = np.random.default_rng(PR.SURVEY_SEED)
    c24 = crown2024(cf, rng)
    c16 = crown2016(c24, cf, rng)
    bm = benchmarks()
    tel, ev, tops = telemetry(pk)
    # the agency publishes each annual peak at the hour its own record tops out, in local standard time
    for wy, (tc, th) in tops.items():
        i = pk.index[pk["wy"] == wy][0]
        pk.at[i, "coy_time"] = tc - pd.Timedelta(hours=6)
        pk.at[i, "hal_time"] = th - pd.Timedelta(hours=6)
    og = other_gauges(pk)
    return {"pk": pk, "t4": t4, "q_design": qd, "cf": cf, "c24": c24, "c16": c16, "bm": bm, "tel": tel,
            "events": ev, "og": og}
