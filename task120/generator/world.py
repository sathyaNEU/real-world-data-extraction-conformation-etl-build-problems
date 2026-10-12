"""The campus water system run for the year on a UTC 15-minute grid: each building's water by day, the zones'
demand by step, the wells staged on the main zone's level, the booster on the hill zone's, and the historian's
hourly samples. The late-August peak is set by the residence halls' move-in surge on 20 August."""
import datetime as dt

import numpy as np

import core

SEED = 1
TARGET = 4_470_300.0          # the campus's demand on 20 August 2026, gallons (tuned: see tune())
LEAK = 0.29e6                 # the mains' leakage, gallons a day
MOVEIN = {19: 0.55, 20: None, 21: 1.00, 22: 0.99, 23: 1.00}


def _norm(a):
    a = np.array(a, float)
    return a / a.sum()


SHAPES = {
    "res": _norm([1.5, 1.0, 0.8, 0.7, 0.8, 1.4, 3.6, 6.4, 7.0, 6.0, 5.0, 4.6, 4.6, 4.4, 4.3, 4.5, 5.0, 5.7, 6.3, 6.4,
                  6.0, 5.2, 4.1, 2.7]),
    "move": _norm([0.6, 0.4, 0.3, 0.3, 0.4, 0.8, 2.2, 4.6, 6.4, 7.4, 7.9, 8.1, 8.1, 8.0, 7.8, 7.4, 7.0, 6.6, 6.2, 5.6,
                   4.6, 3.4, 2.2, 1.2]),
    "aca": _norm([1.6, 1.5, 1.5, 1.5, 1.6, 2.1, 3.3, 5.1, 6.5, 6.9, 6.9, 6.7, 6.5, 6.5, 6.4, 6.2, 5.7, 4.8, 3.6, 3.1,
                  2.7, 2.3, 2.0, 1.7]),
    "lab": _norm([3.2, 3.1, 3.1, 3.1, 3.2, 3.4, 3.8, 4.5, 5.2, 5.5, 5.5, 5.4, 5.3, 5.3, 5.2, 5.1, 4.9, 4.5, 4.1, 3.8,
                  3.6, 3.4, 3.3, 3.2]),
    "ath": _norm([1.0, 0.8, 0.8, 0.8, 1.0, 2.0, 3.6, 4.8, 5.4, 5.6, 5.8, 5.9, 6.0, 6.0, 6.1, 6.4, 6.8, 6.9, 6.4, 5.4,
                  4.2, 3.0, 2.0, 1.3]),
    "cool": _norm([2.2, 2.0, 1.9, 1.9, 2.0, 2.2, 2.8, 3.6, 4.5, 5.4, 6.2, 6.8, 7.2, 7.4, 7.4, 7.2, 6.8, 6.1, 5.2, 4.3,
                   3.6, 3.0, 2.6, 2.3]),
    "flat": _norm(np.ones(24)),
    "oth": _norm([1.4, 1.2, 1.1, 1.1, 1.3, 2.0, 3.4, 5.2, 6.4, 6.8, 7.0, 7.1, 7.2, 7.0, 6.8, 6.5, 6.0, 5.2, 4.2, 3.4,
                  2.9, 2.4, 1.9, 1.6]),
    "irr": _norm([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]),
}
CAT_SHAPE = {"Residence Hall": "res", "Academic": "aca", "Research": "lab", "Athletics": "ath",
             "Administrative": "oth", "Student Life": "oth", "Auxiliary": "oth", "Arts and Culture": "oth",
             "Utilities": "oth"}


def grid():
    n = int((core.T1 - core.T0).total_seconds() // (core.STEP * 60))
    t_utc = [core.T0 + dt.timedelta(minutes=core.STEP * i) for i in range(n + 1)]
    t_loc = [core.local(t) for t in t_utc]
    ldate = [t.date() for t in t_loc[:-1]]
    lhour = np.array([t.hour for t in t_loc[:-1]])
    days = sorted(set(ldate))
    dix = {d: k for k, d in enumerate(days)}
    di = np.array([dix[d] for d in ldate])
    cnt = {}
    for k, h in zip(di, lhour):
        cnt[(k, h)] = cnt.get((k, h), 0) + 1
    nin = np.array([cnt[(k, h)] for k, h in zip(di, lhour)], float)
    return dict(n=n, t_utc=t_utc, t_loc=t_loc, days=days, dix=dix, di=di, lhour=lhour, nin=nin)


def weather(rng, days):
    T = []
    for d in days:
        doy = (d - dt.date(2026, 1, 1)).days
        t = 59.5 + 25.5 * np.sin(2 * np.pi * (doy - 110) / 365.25) + rng.normal(0, 4.0)
        if dt.date(2026, 8, 16) <= d <= dt.date(2026, 8, 25):
            t = [90, 92, 93, 95, 97, 91, 89, 87, 86, 84][(d - dt.date(2026, 8, 16)).days] + rng.normal(0, 0.6)
        T.append(t)
    T = np.round(np.array(T), 1)
    rain = rng.random(len(days)) < 0.28
    return T, rain


def daily(rng, days, T, rain, target, leak_base=LEAK):
    """Category totals by day, then each building's share. Returns {building no: {shape: vols by day}} and the
    unmetered daily volumes."""
    nd = len(days)
    occ = np.zeros(nd); res = np.zeros(nd); aca = np.zeros(nd); lab = np.zeros(nd); ath = np.zeros(nd)
    cep_b = np.zeros(nd); cep_c = np.zeros(nd); oth = np.zeros(nd); irr = np.zeros(nd); leak = np.zeros(nd)
    game = np.zeros(nd)
    for k, d in enumerate(days):
        s, wd = core.season(d), d.weekday()
        o = {"term": 1.0, "finals": 0.9, "thanks": 0.18, "winter": 0.10, "spring": 0.22, "summer": 0.27}.get(s, 1.0)
        if s == "movein":
            o = MOVEIN[d.day] if MOVEIN[d.day] is not None else 1.70
        occ[k] = o
        res[k] = 1.10e6 * o * (1 + rng.normal(0, 0.025))
        fa = {"term": 1.0, "finals": 0.93, "thanks": 0.62, "winter": 0.55, "spring": 0.70, "summer": 0.68,
              "movein": 0.92}[s]
        fr = {"term": 1.0, "finals": 1.0, "thanks": 0.86, "winter": 0.82, "spring": 0.95, "summer": 0.97,
              "movein": 1.0}[s]
        aca[k] = 0.75e6 * fa * (0.62 if wd >= 5 else 1.0) * (1 + rng.normal(0, 0.03))
        lab[k] = 0.45e6 * fr * (0.90 if wd >= 5 else 1.0) * (1 + rng.normal(0, 0.025))
        doy = (d - dt.date(2026, 1, 1)).days % 365
        ath[k] = (0.075e6 + (0.006e6 * max(0.0, T[k] - 70) if 105 <= doy <= 288 else 0.0)
                  + (0.05e6 if s == "movein" else 0.0)) * (1 + rng.normal(0, 0.03))
        game[k] = 0.06e6 * (1 + rng.normal(0, 0.05)) if d in core.HOME_GAMES else 0.0
        cep_b[k] = (0.16e6 + (0.03e6 if T[k] < 50 else 0.0)) * (1 + rng.normal(0, 0.03))
        cool_on = (105 <= doy <= 304) and T[k] > 64
        cep_c[k] = 0.011e6 * max(0.0, T[k] - 64) * (1 + rng.normal(0, 0.04)) if cool_on else 0.0
        fo = {"term": 1.0, "finals": 0.95, "thanks": 0.75, "winter": 0.70, "spring": 0.85, "summer": 0.82,
              "movein": 1.0}[s]
        oth[k] = 0.40e6 * fo * (0.75 if wd >= 5 else 1.0) * (1 + rng.normal(0, 0.03))
        irr_season = dt.date(2026, 4, 20) <= d <= dt.date(2026, 10, 10) or d <= dt.date(2025, 10, 12)
        irr[k] = 0.0 if (not irr_season or rain[k]) else max(0.0, 0.12e6 + 0.012e6 * (T[k] - 75))
        leak[k] = leak_base * (1 + rng.normal(0, 0.02))
    return dict(occ=occ, res=res, aca=aca, lab=lab, ath=ath, game=game, cep_b=cep_b, cep_c=cep_c, oth=oth, irr=irr,
                leak=leak)


def buildings(rng, days, C):
    """Each building's water by day and shape. The annex runs to its removal; Larch Hall from its meter's
    install. Returns {no: {shape: array}} with the building's active window applied at the step level later."""
    nd = len(days)
    allb = core.B + [core.ANNEX]
    vols = {b["no"] if b is not core.ANNEX else "annex": {} for b in allb}

    def active_w(b, d):
        if b is core.ANNEX:
            if d > core.ANNEX_REMOVED.date():
                return 0.0
            return b["w"] * (0.08 if d >= core.ANNEX_WINDDOWN else 1.0)
        if b["no"] == 47:
            if d < core.LARCH_RAS:
                return 0.0
            return b["w"] * (0.15 if d < core.LARCH_OCCUPIED else 1.0)
        return b["w"]

    groups = {"Residence Hall": "res", "Academic": "aca", "Research": "lab", "Athletics": "ath"}
    oth_cats = {"Administrative", "Student Life", "Auxiliary", "Arts and Culture"}
    for cat, key in list(groups.items()) + [("_oth", "oth")]:
        members = [b for b in allb if (b["cat"] == cat if cat != "_oth" else
                                        (b["cat"] in oth_cats or b["no"] in (502, 503)))]
        noise = np.exp(rng.normal(0, 0.06, (nd, len(members))))
        for k, d in enumerate(days):
            w = np.array([active_w(b, d) for b in members]) * noise[k]
            w = w / w.sum()
            for j, b in enumerate(members):
                key_b = "annex" if b is core.ANNEX else b["no"]
                shape = CAT_SHAPE[b["cat"]]
                if b["cat"] == "Residence Hall" and core.season(d) == "movein":
                    shape = "move"
                vols[key_b].setdefault(shape, np.zeros(nd))[k] += C[key][k] * w[j]
    # Larch Hall before its residents: commissioning and flushing water from the meter's install
    for k, d in enumerate(days):
        if core.LARCH_INSTALL.date() <= d < core.LARCH_RAS:
            vols[47].setdefault("flat", np.zeros(nd))[k] += 5200.0 * (1 + rng.normal(0, 0.15))
    # the stadium's game days
    vols[401].setdefault("ath", np.zeros(nd))
    vols[401]["ath"] += C["game"]
    # the central energy plant: boiler and process make-up flat, cooling-tower make-up on the cooling shape
    vols[501] = {"flat": C["cep_b"].copy(), "cool": C["cep_c"].copy()}
    return vols


def demand_steps(G, vols, C):
    """The zones' demand in each 15-minute step, and each building's water in each step."""
    n, di, lh, nin = G["n"], G["di"], G["lhour"], G["nin"]
    zone = {b["no"]: b["zone"] for b in core.B}
    zone["annex"] = core.ANNEX["zone"]
    bsteps = {}
    dm = np.zeros(n); dh = np.zeros(n)
    removed = core.ANNEX_REMOVED.replace(tzinfo=core.ET)
    installed = core.LARCH_INSTALL.replace(tzinfo=core.ET)
    for key, parts in vols.items():
        s = np.zeros(n)
        for shape, v in parts.items():
            s += v[di] * SHAPES[shape][lh] / nin
        if key == "annex":
            cut = np.array([t >= removed for t in G["t_loc"][:-1]])
            s[cut] = 0.0
        if key == 47:
            s[np.array([t < installed for t in G["t_loc"][:-1]])] = 0.0
        bsteps[key] = s
        if zone[key] == "hill":
            dh += s
        else:
            dm += s
    # unmetered: grounds irrigation, leakage, main breaks, hydrant flushing
    irr = C["irr"][di] * SHAPES["irr"][lh] / nin
    leak = C["leak"][di] * SHAPES["flat"][lh] / nin
    dm += 0.85 * irr + 0.75 * leak
    dh += 0.15 * irr + 0.25 * leak
    loc = G["t_loc"][:-1]
    for a, b, gpm, z, _ in core.MAIN_BREAKS:
        a, b = a.replace(tzinfo=core.ET), b.replace(tzinfo=core.ET)
        m = np.array([a <= t < b for t in loc], float) * gpm * core.STEP
        if z == "hill":
            dh += m
        else:
            dm += m
    for d in core.FLUSHING:
        a = dt.datetime(d.year, d.month, d.day, 8, 0, tzinfo=core.ET)
        b = dt.datetime(d.year, d.month, d.day, 15, 0, tzinfo=core.ET)
        dm += np.array([a <= t < b for t in loc], float) * 165.0 * core.STEP
    return dm, dh, bsteps


def control(rng, G, dm, dh):
    """Wells staged on the main zone's hydraulic grade, the booster's duty pump and standby on the hill zone's."""
    n, days = G["n"], G["days"]
    nd = len(days)
    tested = np.array([core.TESTED[w] for w in core.WELLS], float)
    deliv = np.array([core.DELIVERED[w] for w in core.WELLS])
    rate = tested * deliv * (1 + rng.normal(0, 0.003, (nd, 5)))
    for k, d in enumerate(days):                       # Well 1 before its rehabilitation ran on its worn pump
        if d < core.W1_OUT[0]:
            frac = (d - days[0]).days / (core.W1_OUT[0] - days[0]).days
            rate[k, 0] = (1050 - 45 * frac) * core.DELIVERED["W1"] * (1 + rng.normal(0, 0.003))
    w_on = np.array([1153.0, 1150.5, 1148.0, 1145.5, 1143.0])
    w_off = np.array([1157.5, 1156.5, 1155.5, 1154.5, 1153.5])
    b_on, b_off = np.array([1252.0, 1240.0]), np.array([1259.0, 1250.0])
    hm, hh = 1155.6, 1257.4
    gpf_m = core.GPF["A"] + core.GPF["B"]
    gpf_h = core.GPF["C"] + core.GPF["D"]
    won = np.zeros(5, bool); pon = np.zeros(2, bool)
    q_rec = np.zeros((n, 5)); run = np.zeros((n, 5), bool); prun = np.zeros((n, 2), bool)
    HM = np.zeros(n + 1); HH = np.zeros(n + 1)
    HM[0], HH[0] = hm, hh
    di = G["di"]
    for i in range(n):
        d = days[di[i]]
        shift = 0.0
        if core.WINTER_SETPOINTS[0] <= d <= core.WINTER_SETPOINTS[1]:
            shift = -5.0
        elif d >= core.FALL_SETPOINT:
            shift = -3.0
        avail = np.ones(5, bool)
        if core.W1_OUT[0] <= d <= core.W1_OUT[1]:
            avail[0] = False
        if d == core.W4_OUT:
            avail[3] = False
        for j in range(5):
            if not avail[j]:
                won[j] = False
            elif hm < w_on[j] + shift:
                won[j] = True
            elif hm > w_off[j] + shift:
                won[j] = False
        duty = 0 if d.month % 2 == 1 else 1                      # the duty pump alternates monthly
        order = [duty, 1 - duty]
        p_out = core.BPS_P1_OUT[0] <= d <= core.BPS_P1_OUT[1]
        for r, j in enumerate(order):
            if j == 0 and p_out:
                pon[j] = False
            elif hh < b_on[r]:
                pon[j] = True
            elif hh > b_off[r]:
                pon[j] = False
        q = rate[di[i]] * won * core.STEP
        b = pon.sum() * core.BOOSTER_RATE * core.STEP
        q_rec[i] = q; run[i] = won; prun[i] = pon
        hm = min(core.MAIN_OVF - 0.4, hm + (q.sum() - b - dm[i]) / gpf_m)
        hh = min(core.HILL_OVF - 0.4, hh + (b - dh[i]) / gpf_h)
        HM[i + 1], HH[i + 1] = hm, hh
    return dict(rate=rate, q=q_rec, run=run, prun=prun, HM=HM, HH=HH)


def samples(rng, G, S):
    """The historian's hourly samples at each UTC hour: levels to 0.01 ft, totalizers whole gallons, flows and run
    status at the instant, booster and zone pressures, entry-point chlorine."""
    hr = np.arange(0, G["n"] + 1, 4)
    t = [G["t_utc"][i] for i in hr]
    cum = np.vstack([np.zeros(5), np.cumsum(S["q"], axis=0)])[hr]
    lev = {}
    for tk in core.TANKS:
        h = (S["HM"] if core.ZONE_OF_TANK[tk] == "main" else S["HH"])[hr] - core.BASE[tk]
        lev[tk] = np.round(h + rng.normal(0, 0.02, len(hr)), 2)
    # totalizers: W3's 8-digit register is set so it rolls over at the stated moment
    roll_i = next(i for i, x in enumerate(G["t_loc"]) if x >= core.W3_ROLLOVER.replace(tzinfo=core.ET))
    w3_at_roll = np.cumsum(S["q"][:, 2])[roll_i - 1]
    w3_0 = core.W3_REGISTER - w3_at_roll - 1830.0
    tot = {}
    for j, w in enumerate(core.WELLS):
        base = core.TOT0[w] if w != "W3" else w3_0
        g = np.floor(base + cum[:, j]).astype(np.int64)
        if w == "W3":
            g = g % core.W3_REGISTER
        tot[w] = g
    runh = S["run"][np.minimum(hr, G["n"] - 1)]
    prunh = S["prun"][np.minimum(hr, G["n"] - 1)]
    flow = {}
    for j, w in enumerate(core.WELLS):
        k = G["di"][np.minimum(hr, G["n"] - 1)]
        f = S["rate"][k, j] * (1 + rng.normal(0, 0.004, len(hr)))
        flow[w] = np.round(np.where(runh[:, j], f, 0.0), 1)
    bflow = np.round(prunh.sum(1) * core.BOOSTER_RATE * (1 + rng.normal(0, 0.006, len(hr))), 1)
    hm, hh = S["HM"][hr], S["HH"][hr]
    suct = np.round((hm - 1032.0) / 2.31 + rng.normal(0, 0.15, len(hr)), 1)
    disch = np.round((hh - 1032.0) / 2.31 + prunh.sum(1) * 2.2 + rng.normal(0, 0.15, len(hr)), 1)
    mz = np.round((hm - 1004.0) / 2.31 - 3.0 * (bflow > 1000) + rng.normal(0, 0.3, len(hr)), 1)
    hz = np.round((hh - 1121.0) / 2.31 + rng.normal(0, 0.3, len(hr)), 1)
    cl = np.round(np.clip(1.05 + np.cumsum(rng.normal(0, 0.012, len(hr))) * 0.15 + rng.normal(0, 0.03, len(hr)),
                          0.62, 1.48), 2)
    return dict(hr=hr, t=t, lev=lev, tot=tot, flow=flow, run=runh, prun=prunh, bflow=bflow, suct=suct, disch=disch,
                mz=mz, hz=hz, cl=cl, w3_0=w3_0)


def balance(G, H):
    """Each evaluation day's production, storage change and use from the samples at its Eastern midnights; the
    rungs' figures beside them."""
    t = H["t"]
    pos = {x: i for i, x in enumerate(t)}
    loc_mid = [i for i, x in enumerate(t) if core.local(x).hour == 0]
    by_date = {core.local(t[i]).date(): i for i in loc_mid}
    days = core.eval_days()
    store = {tk: (core.GPF[tk] // 100) * np.round(H["lev"][tk] * 100).astype(np.int64) for tk in core.TANKS}
    S_all = sum(store.values())
    S_main = store["A"] + store["B"]

    def prod(i0, i1):
        out = 0
        for w in core.WELLS:
            a, b = int(H["tot"][w][i0]), int(H["tot"][w][i1])
            if b < a:
                b += core.W3_REGISTER
            out += b - a
        return out

    P, dS, dSm, U = [], [], [], []
    for d in days:
        i0, i1 = by_date[d], by_date[d + dt.timedelta(1)]
        p = prod(i0, i1)
        P.append(p); dS.append(S_all[i1] - S_all[i0]); dSm.append(S_main[i1] - S_main[i0])
    P = np.array(P, dtype=np.int64); dS = np.array(dS, dtype=np.int64); dSm = np.array(dSm, dtype=np.int64)
    U = P - dS
    # UTC days
    Pu, Uu = [], []
    for d in days:
        a = dt.datetime(d.year, d.month, d.day, tzinfo=core.UTC)
        b = a + dt.timedelta(1)
        if a not in pos or b not in pos:
            Pu.append(np.nan); Uu.append(np.nan)
            continue
        i0, i1 = pos[a], pos[b]
        p = prod(i0, i1)
        Pu.append(p); Uu.append(p - (S_all[i1] - S_all[i0]))
    # daily mean storage (the local day's hourly samples)
    Sbar = []
    for d in days + [days[-1] + dt.timedelta(1)]:
        i0 = by_date[d]
        i1 = by_date.get(d + dt.timedelta(1), i0 + 24)
        Sbar.append(S_all[i0:i1].mean())
    Sbar = np.array(Sbar)
    Ub = P - (Sbar[1:] - Sbar[:-1])
    return dict(days=days, P=P, dS=dS, dSm=dSm, U=U, Um=P - dSm, Uu=np.array(Uu, float), Pu=np.array(Pu, float),
                Ub=Ub, S_all=S_all, by_date=by_date)


_GRID = {}


def build(seed=SEED, target=TARGET, leak=LEAK):
    rng = np.random.default_rng(seed)
    if "G" not in _GRID:
        _GRID["G"] = grid()
    G = _GRID["G"]
    T, rain = weather(rng, G["days"])
    C = daily(rng, G["days"], T, rain, target, leak)
    vols = buildings(rng, G["days"], C)
    # the peak: the residence halls' move-in surge sets 20 August's demand on the target
    kp = G["dix"][dt.date(2026, 8, 20)]
    other = sum(v[kp] for key, parts in vols.items() for v in parts.values()) - C["res"][kp] + C["irr"][kp] + C["leak"][kp]
    scale = (target - other) / C["res"][kp]
    for key, parts in vols.items():
        b = next((x for x in core.B if x["no"] == key), None)
        if b is not None and b["cat"] == "Residence Hall" and "move" in parts:
            parts["move"][kp] *= scale
    C["res"][kp] *= scale
    dm, dh, bsteps = demand_steps(G, vols, C)
    S = control(rng, G, dm, dh)
    H = samples(rng, G, S)
    Bal = balance(G, H)
    return dict(seed=seed, target=target, leak=leak, G=G, T=T, rain=rain, C=C, vols=vols, dm=dm, dh=dh, bsteps=bsteps, S=S,
                H=H, Bal=Bal)


def summary(W):
    """The main call's acceptance figures."""
    Bal = W["Bal"]
    days, P, U = Bal["days"], Bal["P"], Bal["U"]
    firm = core.FIRM * 1440
    ig, i0 = int(np.argmax(U)), int(np.argmax(P))
    gap = U[ig] / 1440 - core.FIRM
    srt = np.sort(U)
    out = dict(gold_day=days[ig], gold_use=U[ig], gold_P=P[ig], gold_dS=Bal["dS"][ig], gap=gap,
               r0_day=days[i0], r0_P=P[i0], r0_gap=P[i0] / 1440 - core.FIRM,
               gold_prod_rank=int((P > P[ig]).sum()) + 1, second_ratio=srt[-2] / srt[-1],
               r1=np.nanmax(Bal["Um"]) / 1440 - core.FIRM, r1_day=days[int(np.nanargmax(Bal["Um"]))],
               r2=np.nanmax(Bal["Uu"]) / 1440 - core.FIRM, r2_day=days[int(np.nanargmax(Bal["Uu"]))],
               r3=np.nanmax(Bal["Ub"]) / 1440 - core.FIRM, r3_day=days[int(np.nanargmax(Bal["Ub"]))],
               firm=firm)
    ms = [k for k, d in enumerate(days) if d.day == 1] + [len(days)]
    out["month_dS"] = [float(Bal["dS"][a:b].sum()) for a, b in zip(ms[:-1], ms[1:])]
    out["year_dS"] = float(Bal["dS"].sum())
    return out


def acceptable(s):
    frac = s["gap"] - np.floor(s["gap"])
    return (s["gold_day"] == dt.date(2026, 8, 20) and 4.45e6 <= s["gold_use"] <= 4.49e6 and 0.55 <= frac <= 0.95
            and s["r0_P"] <= s["firm"] - 57600 and s["r0_day"] != dt.date(2026, 8, 20) and s["gold_prod_rank"] >= 3
            and s["second_ratio"] <= 0.95
            and all(abs(s[k] - s["gap"]) >= 11 for k in ("r1", "r2", "r3"))
            and min(abs(x) for x in s["month_dS"]) >= 5000 and abs(s["year_dS"]) >= 5000)


def tune(seeds=range(1, 200), targets=None):
    """The search that fixed SEED and TARGET (run by hand; the build uses the constants)."""
    targets = targets or [4_469_800.0 + 155.0 * k for k in range(9)]
    for sd in seeds:
        for tg in targets:
            s = summary(build(sd, tg))
            if acceptable(s):
                return sd, tg, s
    return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "tune":
        print(tune(range(int(sys.argv[2]), int(sys.argv[3]))))
    else:
        s = summary(build())
        for k, v in s.items():
            print(k, v)
        print("acceptable", acceptable(s))
