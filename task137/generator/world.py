"""Calderwick Police's custody world: the force area's wards and LSOAs, the recorded crime and the force's own arrests
by LSOA, month and offence type, British Transport Police's crime at the railway stations, and the expected
2027-28 detentions at the Tanner Street hub. Everything here is the clean truth: no mess, no documents."""
import datetime as dt

import numpy as np

TYPES = ["Violence and sexual offences", "Public order", "Drugs", "Possession of weapons", "Robbery", "Burglary",
         "Criminal damage and arson", "Shoplifting", "Theft from the person", "Other theft", "Vehicle crime",
         "Bicycle theft", "Other crime"]
WARRANT_GROUP = "Warrant, recall or breach"
RATE = np.array([0.165, 0.20, 0.70, 0.55, 0.20, 0.07, 0.06, 0.12, 0.04, 0.035, 0.025, 0.015, 0.19])
INNER_MIX = np.array([0.34, 0.11, 0.05, 0.015, 0.02, 0.05, 0.08, 0.11, 0.03, 0.09, 0.06, 0.02, 0.025])
OUTER_MIX = np.array([0.36, 0.08, 0.035, 0.012, 0.01, 0.07, 0.11, 0.08, 0.01, 0.10, 0.09, 0.013, 0.03])
COUNTY_MIX = np.array([0.36, 0.075, 0.03, 0.01, 0.005, 0.075, 0.12, 0.07, 0.008, 0.10, 0.10, 0.012, 0.035])
STATION_MIX = np.array([0.30, 0.14, 0.05, 0.02, 0.025, 0.005, 0.07, 0.03, 0.12, 0.105, 0.03, 0.07, 0.035])
WARRANT = 0.05                      # share of arrests on a warrant, recall or breach, with no recorded crime of their own

HUB = ["Abbey Fields", "Castle", "Cathedral", "Mill Bank", "St Peter's", "Kingsway"]
OUTER = ["Northgate", "Highfield", "Brookside", "Parkway", "Ashgrove", "Elmwood", "Fernhill", "Glebe", "Hollins",
         "Ivydene", "Jubilee", "Lark Hill", "Marsh Lane", "Newtown", "Oakfield", "Eastmoor", "Quarry Bank", "Ravensdale"]
CITY = HUB + OUTER
_STEMS = ["Ald", "Ash", "Bar", "Brad", "Burn", "Chal", "Clay", "Cot", "Dal", "Den", "Elm", "Far", "Fen", "Gar", "Glen",
          "Hal", "Hat", "Hay", "Hol", "Kel", "Kings", "Lang", "Lid", "Mar", "Mel", "Mor", "New", "North", "Oak", "Ors",
          "Pen", "Pres", "Red", "Sand", "Shel", "Sted", "Sut", "Thorn", "Wal", "Wes"]
_SUF = ["ton", "ley", "ford", "field", "bury", "worth", "ham", "wick", "thorpe", "by"]
COUNTY = []
_i = 0
while len(COUNTY) < 100:
    _n = _STEMS[_i % 40] + _SUF[(_i * 3 + _i // 40) % 10]
    if _n not in COUNTY and _n not in CITY:
        COUNTY.append(_n)
    _i += 1
WARDS = CITY + COUNTY
DISTRICTS = ["Calderwick", "North Carvell", "Wendlebury", "South Carvell", "Moorhaven"]
DISTRICT = {w: "Calderwick" for w in CITY}
for _j, _w in enumerate(COUNTY):
    DISTRICT[_w] = DISTRICTS[1 + _j // 25]
SUITES = ["Northgate", "Eastmoor", "Southfields", "Wendle Cross"]
HUB_SUITE = "Tanner Street"
SUITE_NOW = {}
for _w in HUB:
    SUITE_NOW[_w] = "Eastmoor" if _w == "St Peter's" else "Northgate"
for _j, _w in enumerate(OUTER):
    SUITE_NOW[_w] = "Northgate" if _j < 9 else "Eastmoor"
for _w in COUNTY:
    SUITE_NOW[_w] = "Wendle Cross" if DISTRICT[_w] in ("North Carvell", "Wendlebury") else "Southfields"
SUITE_2027 = {w: (HUB_SUITE if w in HUB else s) for w, s in SUITE_NOW.items()}
# the railway stations: name, ward, share of the main station's recorded crime
STATIONS = [("Calderwick", "Abbey Fields", 1.0), ("Kingsway", "Kingsway", 0.07), ("Northgate", "Northgate", 0.05),
            ("Eastmoor", "Eastmoor", 0.045)] + [(COUNTY[j] + (" Road" if j % 3 == 0 else ""), COUNTY[j], f) for j, f in
            [(3, 0.016), (11, 0.012), (27, 0.014), (38, 0.010), (52, 0.013), (64, 0.009), (77, 0.011), (90, 0.008)]]

NM = 66                                                                    # April 2021 to September 2026
MONTHS = [(2021 + (3 + k) // 12, (3 + k) % 12 + 1) for k in range(NM)]
K25 = list(range(48, 60))                                                  # April 2025 to March 2026
SEASON = 1 + 0.08 * np.cos(2 * np.pi * (np.arange(12) - 6.5) / 12)        # summer a little higher
# the last COVID-19 months: pubs open outdoors only until 17 May 2021, every restriction lifted on 19 July,
# Plan B guidance from 8 December 2021 to 27 January 2022 (k = 0 is April 2021)
COVID = {0: 0.80, 1: 0.86, 2: 0.93, 3: 0.98, 8: 0.95, 9: 0.97}
# wards whose night-time economy moved: Kingsway lost its clubs to the Kingsway Quarter redevelopment from 2022,
# Mill Bank's canal-side bars opened from 2023
WARD_TREND = {"Kingsway": -0.045, "Mill Bank": 0.035, "Castle": 0.01, "St Peter's": -0.01}
FYS = [2021, 2022, 2023, 2024, 2025, 2026]


def fy_of(y, m):
    return y if m >= 4 else y - 1


FYK = np.array([fy_of(*MONTHS[k]) for k in range(NM)])


def world(seed, btp_main=1600.0, hub_lam=300.0, shock_sd=0.022):
    """The draw: LSOAs with their crime level, mix and trend; the year-to-year swing in how many arrests the force
    makes per crime (staffing, operations); BTP's crime at each station."""
    rng = np.random.default_rng(seed)
    lsoas = []
    for w in WARDS:
        n = int(rng.integers(11, 15)) if w in CITY else int(rng.integers(9, 13))
        for k in range(n):
            if w in HUB:
                lam, mix = rng.lognormal(np.log(hub_lam), 0.5), INNER_MIX
            elif w in CITY:
                lam, mix = rng.lognormal(np.log(115), 0.5), OUTER_MIX
            else:
                lam, mix = rng.lognormal(np.log(88), 0.5), COUNTY_MIX
            lsoas.append(dict(ward=w, lam=lam, mix=mix, trend=WARD_TREND.get(w, 0.0) + rng.normal(0.0, 0.008)))
    for name, ward, f in STATIONS:
        [l for l in lsoas if l["ward"] == ward][0]["station"] = name
    shock = {fy: float(np.exp(rng.normal(0.0, shock_sd))) for fy in FYS}
    btp = {name: btp_main * f for name, ward, f in STATIONS}
    return dict(seed=seed, lsoas=lsoas, btp=btp, shock=shock, btp_main=btp_main, hub_lam=hub_lam)


def lam_months(l, ks):
    ks = np.asarray(ks)
    mon = np.array([(3 + k) % 12 for k in ks])
    cov = np.array([COVID.get(int(k), 1.0) for k in ks])
    return l["lam"] * (1 + l["trend"]) ** (ks / 12.0) * SEASON[mon] * cov / 12.0


def counts(W):
    """Crime and the force's arrests by LSOA (months x types, plus warrants); BTP crime and arrests by station."""
    rng = np.random.default_rng(W["seed"] + 17)
    fc, ar, wa = [], [], []
    ks = np.arange(NM)
    sh = np.array([W["shock"][fy] for fy in FYK])
    for l in W["lsoas"]:
        n = rng.poisson(lam_months(l, ks)[:, None] * l["mix"][None, :])
        a = rng.poisson(n * RATE[None, :] * sh[:, None])
        fc.append(n)
        ar.append(a)
        wa.append(rng.poisson(a.sum(1) * WARRANT / (1 - WARRANT)))
    mon = np.array([(3 + k) % 12 for k in ks])
    bc, ba = {}, {}
    for name, ward, f in STATIONS:
        c = rng.poisson((W["btp"][name] * SEASON[mon] / 12.0)[:, None] * STATION_MIX[None, :])
        bc[name] = c
        b = rng.poisson(c * RATE[None, :])
        ba[name] = b.sum(1) + rng.poisson(b.sum(1) * WARRANT / (1 - WARRANT))
    return dict(fc=fc, ar=ar, wa=wa, bc=bc, ba=ba)


def truth_2027(W):
    """Expected detentions at Tanner Street from 1 April 2027 to 31 March 2028: the force's arrests in the six wards
    (at no year shock) and BTP's arrests at the stations in them, warrants included on both."""
    force = 0.0
    for l in W["lsoas"]:
        if l["ward"] in HUB:
            lam = lam_months(l, np.arange(72, 84))
            force += float(lam.sum() * (l["mix"] * RATE).sum()) / (1 - WARRANT)
    btp = sum(W["btp"][n] * float((STATION_MIX * RATE).sum()) / (1 - WARRANT) for n, w, f in STATIONS if w in HUB)
    return dict(force=force, btp=btp, total=force + btp)


# ---------------------------------------------------------------------------------------------------------------
# the routes on aggregates, for the seed search (the file-based routes are golden.py's)
def _model(wardmonths, base, ahead, cap=0.10):
    tot = 0.0
    for v in wardmonths.values():
        b = v[FYK == base].sum()
        b3 = v[FYK == base - 3].sum()
        ch = (b / b3) ** (1 / 3) - 1
        if cap is not None:
            ch = min(cap, max(-cap, ch))
        tot += b * (1 + ch) ** ahead
    return tot


def routes_agg(W, C=None, hw=True):
    C = C or counts(W)
    L = W["lsoas"]
    hubw, mon = {}, np.zeros(NM)
    suites = {}
    for i, l in enumerate(L):
        a = C["ar"][i].sum(1) + C["wa"][i]
        if l["ward"] in HUB:
            hubw.setdefault(l["ward"], np.zeros(NM))
            hubw[l["ward"]] += a
            mon += a
        suites.setdefault(SUITE_NOW[l["ward"]], {}).setdefault(l["ward"], np.zeros(NM))
        suites[SUITE_NOW[l["ward"]]][l["ward"]] += a
    fyt = {y: float(mon[FYK == y].sum()) for y in range(2021, 2026)}
    force_fy = {y: sum(float((C["ar"][i].sum(1) + C["wa"][i])[FYK == y].sum()) for i in range(len(L)))
                for y in (2022, 2025)}
    F = {"F1": _model(hubw, 2025, 2), "F2": fyt[2025], "F3": float(np.mean([fyt[2023], fyt[2024], fyt[2025]])),
         "F4": float(np.polyval(np.polyfit(range(2021, 2026), [fyt[y] for y in range(2021, 2026)], 1), 2027)),
         "F6": float(mon[-12:].sum()), "F7": _model(hubw, 2025, 2, None),
         "F8": fyt[2025] * (force_fy[2025] / force_fy[2022]) ** (2 / 3), "F9": float(np.mean([fyt[2024], fyt[2025]]))}
    if hw:
        import warnings
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        warnings.filterwarnings("ignore")
        m = ExponentialSmoothing(mon.astype(float), trend="add", damped_trend=True, seasonal="add",
                                 seasonal_periods=12).fit()
        F["F5"] = float(m.forecast(18)[6:18].sum())
    sel = np.isin(np.arange(NM), K25)
    ar_t, cr_t, war, hub_ar, hub_cr = np.zeros(13), np.zeros(13), 0.0, 0.0, 0.0
    for i, l in enumerate(L):
        ar_t += C["ar"][i][sel].sum(0)
        cr_t += C["fc"][i][sel].sum(0)
        war += C["wa"][i][sel].sum()
        if l["ward"] in HUB:
            hub_ar += C["ar"][i][sel].sum() + C["wa"][i][sel].sum()
            hub_cr += C["fc"][i][sel].sum()
    b25 = sum(C["bc"][n][sel].sum(0) for n, w, f in STATIONS if w in HUB)
    ball = sum(C["bc"][n][sel].sum(0) for n, w, f in STATIONS)
    rate_t = np.where(cr_t > 0, ar_t / np.maximum(cr_t, 1), 0)
    overall = (ar_t.sum() + war) / cr_t.sum()
    B = {"B1": float((b25 * rate_t).sum()), "B2": float((b25 * rate_t).sum() * (1 + war / ar_t.sum())),
         "B3": float(b25.sum() * overall), "B4": float(b25.sum() * hub_ar / hub_cr)}
    G = {"%s+%s" % (f, b): F[f] + B[b] for f in ("F1", "F2", "F3", "F5", "F6") if f in F for b in B}
    share = ball.sum() / (ball.sum() + cr_t.sum())
    R = {"R0": F["F1"], "R1": F["F1"] * (1 + share), "R2": F["F1"] + float(ball.sum() * overall)}
    val = {}
    for s in SUITES:
        fc_ = _model(suites[s], 2024, 1)
        act = sum(v[FYK == 2025].sum() for v in suites[s].values())
        val[s] = (fc_, act, fc_ / act)
    return dict(F=F, B=B, G=G, R=R, share=share, overall=overall, truth=truth_2027(W), val=val, fyt=fyt,
                btp_hub=float(b25.sum()), btp_all=float(ball.sum()), crime=float(cr_t.sum()))


def binned(x, b=250):
    return int(np.floor(x / b + 0.5))


def judge(r, b=250, margin=30, gap=1, share=(0.007, 0.02), frame_keys=None):
    """Check 2 on a routes result: the frame family in one printed cell with margin, the golden family in a cell at
    least `gap` above it with margin, R1 in the frame's cell, the truth in the golden's, the validation within 3%."""
    fr = [v for k, v in r["F"].items() if frame_keys is None or k in frame_keys]
    go = list(r["G"].values())

    def one_bin(xs):
        ks = {binned(x, b) for x in xs}
        if len(ks) != 1:
            return None, 0.0
        k = ks.pop()
        lo, hi = (k - 0.5) * b, (k + 0.5) * b
        return k, min(min(xs) - lo, hi - max(xs))
    kf, mf = one_bin(fr)
    kg, mg = one_bin(go)
    ok = (kf is not None and kg is not None and mf >= margin and mg >= margin and kg - kf >= gap
          and binned(r["R"]["R1"], b) == kf and binned(r["truth"]["total"], b) == kg
          and share[0] <= r["share"] <= share[1] and all(0.97 <= v[2] <= 1.03 for v in r["val"].values()))
    return ok, kf, mf, kg, mg


def local_dt(y, m, d, hh, mi):
    return dt.datetime(y, m, d, hh, mi)
