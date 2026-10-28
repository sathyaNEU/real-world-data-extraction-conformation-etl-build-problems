"""task162 truth: the Northern zone hour by hour (GMT), 1 April 2025 to 31 March 2026. Nothing here is shipped.

Thornholme service reservoir (top water level 128 m AOD) feeds the Thornholme to Brackenby trunk main. Each district's
inlet pressure is the reservoir's head less the inlet's ground level less the trunk main's loss to the off-take, which
grows with the main's flow (to its 1.85 power) and with the off-take's distance down the main. The main's flow is the
zone's household demand plus Brackenby Paper Mill's two weekday shifts (06:00 to 22:00 local), so on working days the
far districts' inlets sit well under their night level from the morning into the evening. Each district's average
zone pressure and critical point pressure fall further with its own flow. Leakage follows FAVAD: background leakage
and every running burst scale with the average zone pressure to the district's N1.

Phase 3's 22 districts get fixed-outlet valves whose settings come from Coldbeck's design rule (20 m at the critical
point at the design peak, the record's peak flow grown to 2035 with an 8 l/s fire flow drawn at the critical point).
The twelve districts nearer Thornholme (outside Phase 3) carry the year's ordinary changes: new homes connected,
NZ04's second inlet still logged under its retired code NZ04A, and nine January days when NZ09 was fed through NZ10."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

START = K.YEAR_START
END = K.YEAR_END
HOURS = int((END - START).total_seconds() // 3600)
DAYS = HOURS // 24
TWL = 128.0
DESIGN_GROWTH = 1.10
DESIGN_CP = 20.0
EXISTING_MIN = 10.0
OPEN_BOUNDARY = (dt.date(2026, 1, 12), dt.date(2026, 1, 21))   # NZ09 fed through NZ10 (repair at NZ09's inlet), days [a, b)
METER_REG = 0.978         # customer meters' registration on the true use
MILL_LPS = 167.804        # Brackenby Paper Mill's draw on shift, l/s       | the zone balance's three calibration
TRUNK_LOSS = 0.3228       # the trunk main's own losses, Ml/d               | knobs, from tune.py's balance run
BAND_SHIFT = 0.00595      # unmeasured households in band 3 not band 2      | (every Ask B figure mid-bin)
LEAK_TUNE = {   # per-district multipliers on background leakage, from tune.py (every graded figure mid-bin)
    "NZ01": 0.9997, "NZ02": 1.0008, "NZ03": 1.0002, "NZ04": 1.0008, "NZ05": 1.0034, "NZ06": 0.997,
    "NZ07": 0.9992, "NZ08": 1.0048, "NZ09": 1.0034, "NZ10": 0.9975, "NZ11": 0.9997, "NZ12": 0.9965,
    "NZ13": 1.0, "NZ14": 1.0, "NZ15": 1.0, "NZ16": 1.0, "NZ17": 1.0, "NZ18": 1.0,
    "NZ19": 1.0, "NZ20": 1.0, "NZ21": 1.0, "NZ22": 1.0, "NZ23": 1.0, "NZ24": 1.0,
    "NZ25": 1.0, "NZ26": 1.0, "NZ27": 1.0, "NZ28": 1.0, "NZ29": 1.0, "NZ30": 1.0,
    "NZ31": 1.0, "NZ32": 1.0, "NZ33": 1.0, "NZ34": 1.0,
}

# (code, name, chainage km, households on 1 April 2025, non-households, phase)
DISTRICTS = [
    ("NZ01", "Orlesby Village", 0.6, 1420, 38, 4), ("NZ02", "Kessington Lane", 1.4, 980, 21, 4),
    ("NZ03", "Halverby Park", 2.1, 2310, 64, 4), ("NZ04", "Wrenfold", 2.9, 1170, 30, 4),
    ("NZ05", "Stainmoor Ings", 3.6, 1640, 45, 4), ("NZ06", "Kestle Road", 4.4, 860, 17, 4),
    ("NZ07", "Sorrelby End", 5.1, 2050, 52, 4), ("NZ08", "Cragthwaite Top", 5.9, 740, 12, 4),
    ("NZ09", "Linmere Green", 6.6, 1310, 33, 4), ("NZ10", "Barrowside", 7.2, 1880, 47, 4),
    ("NZ11", "Old Mill Fields", 7.9, 1020, 26, 4), ("NZ12", "Ravens Clough", 8.5, 1460, 35, 4),
    ("NZ13", "Hepsley Moor", 9.2, 1190, 22, 3), ("NZ14", "Skelderby Bank", 9.8, 2240, 58, 3),
    ("NZ15", "Fellstone", 10.3, 870, 14, 3), ("NZ16", "Jessop Bridge", 10.9, 1530, 39, 3),
    ("NZ17", "Woolmere Town", 11.4, 2680, 81, 3), ("NZ18", "Hawkdale Edge", 11.9, 640, 9, 3),
    ("NZ19", "Tolleby", 12.3, 1110, 23, 3), ("NZ20", "Underhow", 12.8, 1770, 44, 3),
    ("NZ21", "Chapelrigg", 13.2, 980, 18, 3), ("NZ22", "Netherskell Rise", 13.7, 2390, 63, 3),
    ("NZ23", "Thornsike Bridge", 14.1, 1650, 41, 3), ("NZ24", "Brockmere Lane", 14.6, 1240, 29, 3),
    ("NZ25", "Hagg Wood", 15.0, 760, 11, 3), ("NZ26", "Fendyke", 15.4, 2060, 55, 3),
    ("NZ27", "Holmwick", 15.9, 1380, 32, 3), ("NZ28", "Yarrowholme", 16.3, 590, 8, 3),
    ("NZ29", "Austerby", 16.7, 1090, 21, 3), ("NZ30", "Wensike", 17.1, 1860, 47, 3),
    ("NZ31", "Dimmock Edge", 17.4, 720, 13, 3), ("NZ32", "Brackenby South", 17.8, 2410, 70, 3),
    ("NZ33", "Brackenby Moor", 18.1, 1330, 30, 3), ("NZ34", "Brackenby Town", 18.4, 3150, 96, 3),
]
PHASE3 = [d[0] for d in DISTRICTS if d[5] == 3]
NEAR = [d[0] for d in DISTRICTS if d[5] == 4]


def hour_index():
    return [START + dt.timedelta(hours=h) for h in range(HOURS)]


def diurnal(lh, weekend):
    """Household demand shape by local hour."""
    return (0.22 + 0.95 * np.exp(-((lh - (8.0 + 0.7 * weekend)) / 1.5) ** 2)
            + 0.62 * np.exp(-((lh - 19.2) / 2.1) ** 2) + 0.30 * ((lh > 10) & (lh < 17)))


def district_params():
    out = []
    r = K.rng("districts")
    for code, name, ch, hh, nhh, ph in DISTRICTS:
        g = r.uniform(0, 1, 16)
        p = dict(code=code, name=name, chainage=ch, households=hh, nonhh=nhh, phase=ph)
        if ph == 3:
            night = 62.0 + 22.0 * g[0]
            group = "day" if int(code[2:]) % 2 == 1 or int(code[2:]) in (14, 22, 30) else "peak"
            p["group"] = group
            p["design_red"] = (8.0 + 3.5 * g[1]) if group == "day" else (12.0 + 6.0 * g[1])
            p["trunk"] = None
        else:
            night = 46.0 + 24.0 * g[0]
            p["group"] = None
            p["design_red"] = None
            p["trunk"] = 2.0 + 10.0 * (ch / 9.0) * (0.7 + 0.6 * g[2])
        p["_g_trunk"] = g[2]
        p["fire"] = 7.0 + 4.0 * g[3]
        p["cp_loss"] = 4.0 + 5.0 * g[4]
        p["ground"] = TWL - night
        p["night_static"] = night
        p["azp_dz"] = -4.0 + 8.0 * g[5]
        p["azp_loss"] = 0.8 + 2.4 * g[6]
        p["n1"] = round(0.90 + 0.70 * g[7], 2)
        p["percap"] = 300.0 + 60.0 * g[9]            # litres a household a day
        p["night_use"] = 1.45 + 0.5 * g[10]            # true household night use, l/h (the allowance is 1.7)
        p["nhh_night"] = 5.0 + 6.0 * g[8]              # true non-household night use, l/h (the allowance is 8.0)
        p["bg_leak"] = ((0.0010 + 0.0014 * g[11]) * hh ** 0.92 + 0.5 * g[12]) * LEAK_TUNE.get(code, 1.0)
        p["_g_cp"] = g[13]
        p["new_homes"] = int(120 + 200 * g[14]) if ph == 4 else 0
        out.append(p)
    return out


def _new_connections(p, r):
    """Dated new-build connections through the year (the near districts' estates), as day offsets from START."""
    if not p["new_homes"]:
        return np.zeros(DAYS, int), []
    days = np.sort(r.integers(10, DAYS - 5, p["new_homes"]))
    daily = np.zeros(DAYS, int)
    for d in days:
        daily[d:] += 1
    return daily, [int(d) for d in days]


def simulate():
    T = {}
    idx = hour_index()
    n = len(idx)
    hod = np.array([t.hour for t in idx])
    summer = np.array([1 if K.bst(t) else 0 for t in idx])
    lh = (hod + summer) % 24
    dow = np.array([t.weekday() for t in idx])
    day = np.array([(t.date() - START.date()).days for t in idx])
    weekend = (dow >= 5).astype(float)
    r = K.rng("weather")
    heat = np.zeros(DAYS)
    for k in range(DAYS):
        d = START.date() + dt.timedelta(k)
        seas = np.cos(2 * np.pi * (d.timetuple().tm_yday - 200) / 365.25)
        heat[k] = max(0.0, seas) * (1.0 + (0.6 if (d.year == 2025 and d.month in (6, 7, 8)) else 0.15))
    wx = np.clip(1.0 + 0.06 * r.standard_normal(DAYS), 0.85, 1.2)
    garden = 0.55 * heat[day] * np.exp(-((lh - 19.0) / 1.8) ** 2)
    resid = (diurnal(lh, weekend) + garden) * wx[day] * (1.0 - 0.04 * weekend)
    resid = resid / np.percentile(resid, 99.5)
    # Brackenby Paper Mill: two shifts on weekdays, shut at Christmas, the bank holidays and the August fortnight
    shut = np.zeros(DAYS, bool)
    for k in range(DAYS):
        d = START.date() + dt.timedelta(k)
        if (d.month == 12 and d.day >= 23) or (d.month == 1 and d.day <= 2) or (d.month == 8 and 4 <= d.day <= 17) \
                or d in (dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5), dt.date(2025, 5, 26),
                         dt.date(2025, 8, 25), dt.date(2026, 3, 30), dt.date(2026, 3, 31)):
            shut[k] = True
    ind = np.where((weekend == 0) & (lh >= 6) & (lh < 22), 1.0, 0.18)
    ind = np.where(shut[day], 0.12, ind) * (1.0 + 0.04 * r.standard_normal(n))
    Z = 0.55 * resid + 0.45 * ind
    Z = Z / np.percentile(Z, 99.5)
    res = TWL - 1.6 * np.convolve(Z, np.ones(6) / 6, mode="same") + 0.25 * K.rng("res").standard_normal(n)
    T.update(idx=idx, hod=hod, lh=lh, day=day, summer=summer, weekend=weekend, Z=Z, res=res, ind=ind, shut=shut, wx=wx)
    T["mill_lps"] = MILL_LPS * ind                                  # the mill's draw on its own off-take, l/s
    P = district_params()
    T["P"] = P
    zmax = np.max(Z) ** 1.85
    # background leakage rises through the winter (ground movement, frost) and eases in the summer
    season = 1.0 + 0.07 * np.cos(2 * np.pi * (np.array([(START.date() + dt.timedelta(k)).timetuple().tm_yday
                                                       for k in range(DAYS)]) - 25) / 365.25)
    ob = np.array([OPEN_BOUNDARY[0] <= (START.date() + dt.timedelta(int(d))) < OPEN_BOUNDARY[1] for d in day])
    T["open_boundary"] = ob
    for p in P:
        rr = K.rng("district", p["code"])
        q_shape = np.clip(Z * (0.92 + 0.16 * rr.uniform()) + 0.03 * rr.standard_normal(n), 0.05, None)
        noise_in = 0.18 * rr.standard_normal(n)
        qpk = np.percentile(q_shape, 99.9)
        if p["phase"] == 3:
            red = p["design_red"]
            slack = (DESIGN_CP - EXISTING_MIN) + p["fire"] + p["cp_loss"] * ((DESIGN_GROWTH * qpk) ** 1.85 - qpk ** 1.85)
            hi = (red + slack) / zmax - 2.5
            lo = (1.9 * red) if p["group"] == "day" else (red + 2.0)
            hi = max(hi, lo + 0.5)
            p["trunk"] = lo + (hi - lo) * p["_g_trunk"]
            p["setting"] = float(round(p["night_static"] - red))
            p["cp_dz"] = p["setting"] - DESIGN_CP - p["fire"] - p["cp_loss"] * (DESIGN_GROWTH * qpk) ** 1.85
        else:
            p["setting"] = None
            p["cp_dz"] = -2.0 + 10.0 * p["_g_cp"]
        inlet = T["res"] - p["ground"] - p["trunk"] * Z ** 1.85 + noise_in
        azp = inlet - p["azp_dz"] - p["azp_loss"] * q_shape ** 1.85 + 0.12 * rr.standard_normal(n)
        cp = inlet - p["cp_dz"] - p["cp_loss"] * q_shape ** 1.85 + 0.15 * rr.standard_normal(n)
        added, conn_days = _new_connections(p, K.rng("connections", p["code"]))
        # the year's ordinary turnover: single infill houses connected in the far districts, a few demolitions anywhere
        ri = K.rng("infill", p["code"])
        infill_days = sorted(int(x) for x in ri.integers(15, DAYS - 10, int(ri.integers(2, 9)))) if p["phase"] == 3 else []
        demol_days = sorted(int(x) for x in ri.integers(15, DAYS - 10, int(ri.integers(0, 4))))
        turnover = np.zeros(DAYS, int)
        for d in infill_days:
            turnover[d:] += 1
        for d in demol_days:
            turnover[d:] -= 1
        hh_day = p["households"] + added + turnover
        hh = hh_day[day]
        # household use by local hour: the night use through the small hours, the day's use on top of it, so a
        # dwelling's mean is its per-household figure
        excess = np.clip(diurnal(lh, weekend) + garden - 0.24, 0.0, None) * wx[day]
        nu_lps = p["night_use"] / 3600.0
        cons = hh * (nu_lps + (p["percap"] / 86400.0 - nu_lps) / excess.mean() * excess) \
            * (1.0 + 0.08 * rr.standard_normal(n))
        night = (hod == K.NIGHT_HOUR)
        on_shift = ((lh >= 7) & (lh <= 18) & (weekend == 0)).astype(float)
        nonhh = p["nonhh"] * (p["nhh_night"] / 3600.0 + 0.010 * on_shift)
        ref = np.median(azp[night])
        bursts = np.zeros(n)
        rb = K.rng("bursts", p["code"])
        t = 0
        while True:
            t += int(rb.exponential(24 * 365 / (5.0 + p["households"] / 350.0)))
            if t >= n:
                break
            bursts[t:t + int(24 * rb.uniform(1, 20))] += rb.uniform(0.06, 0.7)
        leak = (p["bg_leak"] * season[day] + bursts) * np.clip(azp / ref, 0.05, None) ** p["n1"]
        flow = cons + nonhh + leak
        T[p["code"]] = dict(inlet=inlet, azp=azp, cp=cp, flow=flow, leak=leak, cons=cons + nonhh, qshape=q_shape,
                            hh_day=hh_day, conn_days=conn_days, infill_days=infill_days, demol_days=demol_days, ref=ref)
    # NZ09 fed through NZ10 for nine January days: NZ09's inlet closed for a repair in its meter chamber, its whole
    # demand coming in through the boundary valve and NZ10's inlet meter; NZ09's pressures fall with the longer path
    a, b = T["NZ09"], T["NZ10"]
    a["flow_inlet"] = np.where(ob, 0.02 * K.rng("ob").random(n), a["flow"])
    b["flow_inlet"] = np.where(ob, b["flow"] + a["flow"], b["flow"])
    a["azp"] = np.where(ob, a["azp"] - 4.5 - 2.0 * Z, a["azp"])
    for p in P:
        T[p["code"]].setdefault("flow_inlet", T[p["code"]]["flow"])
    # NZ04's second inlet, still logged under its retired code NZ04A: 41 per cent of the district's inflow
    d4 = T["NZ04"]
    d4["flow_inlet_a"] = 0.41 * d4["flow_inlet"]
    d4["flow_inlet"] = d4["flow_inlet"] - d4["flow_inlet_a"]
    return T


def setting(T, p):
    """Coldbeck's design rule, re-derived from the truth: the lowest whole-metre outlet setting that holds DESIGN_CP at
    the critical point at the district's design peak with the fire flow drawn there."""
    qd = np.percentile(T[p["code"]]["qshape"], 99.9) * DESIGN_GROWTH
    return float(np.ceil(DESIGN_CP + p["cp_dz"] + p["cp_loss"] * qd ** 1.85 + p["fire"] - 1e-9))
