"""The clean truth: the economy's prices, the businesses' physical stocks and what their accounts carry them at,
goods trade, the national accounts and every vintage the Statistics Office and TBS published. Nothing here is a
shipped file; records.py and docs.py write those from this state. Every stream is seeded from common.SEED by name.

Book values follow first-in, first-out at cost: the goods on hand at a month end were bought over the months the
business takes to sell its stock (its stock-to-sales ratio), uniformly in time, each month at that month's average
price, so a month-end book value is the physical stock times the average of the industry's input price index over
those months. The Office measures the change in inventories by revaluing each industry's book values that way."""
from __future__ import annotations

import math

import numpy as np

import common as K

MONTHS = K.month_list(K.MONTHS0, K.LAST)
MI = {m: i for i, m in enumerate(MONTHS)}
NM = len(MONTHS)
YEAR = np.array([int(m[:4]) for m in MONTHS])
MON = np.array([int(m[5:7]) for m in MONTHS])
QUARTERS = K.quarter_list(K.Q0, "2026Q2")
QI = {q: i for i, q in enumerate(QUARTERS)}


class World:
    pass


def ym(y, m):
    return MI["%04d-%02d" % (y, m)]


NEW_SYSTEM = "2026-01"     # TBS's new processing system compiles the statistics from this month


def tbs_month(series, m):
    """What TBS's statistics carry for month m of a periodic-entry series held by month of shipment: until the
    December 2025 month the entries lodged in the month (the previous month's cargoes), December 2025 with
    December's own cargoes added when the new system dated January's lodgements by shipment, and from January 2026
    the month's own cargoes."""
    if m >= MI[NEW_SYSTEM]:
        return series[m]
    if m == MI["2025-12"]:
        return series[m - 1] + series[m]
    return series[m - 1] if m > 0 else series[m]


# ---------------------------------------------------------------------------------------------------- drivers
def drivers(W):
    """The trade-weighted dollar, foreign prices in foreign currency by SITC section, world energy and dairy
    prices, and domestic inflation; monthly log changes."""
    r = K.rng("drivers")
    de = r.normal(0.0, 0.0055, NM)
    de[(YEAR == 2020) & (MON >= 2) & (MON <= 4)] += -0.016
    de[(YEAR == 2020) & (MON >= 6)] += 0.004
    de[YEAR == 2022] += -0.0058
    de[(YEAR == 2023) & (MON <= 7)] += 0.0035
    de[(YEAR == 2025) & (MON >= 9)] += 0.0012
    for mm, v in (("2026-01", 0.0021), ("2026-02", -0.0046), ("2026-03", -0.0220), ("2026-04", 0.0031),
                  ("2026-05", 0.0018), ("2026-06", -0.0720)):
        de[MI[mm]] = v                  # March: the Reserve Bank's surprise cut on 24 February; June: the downgrade
    W.dlog_e = de
    W.twi = 100.0 * np.exp(np.cumsum(de) - np.cumsum(de)[MI["2019-06"]])
    # world prices in foreign currency
    base = 0.0016 + np.where(YEAR == 2021, 0.0022, 0.0) + np.where(YEAR == 2022, 0.0045, 0.0) \
        + np.where(YEAR == 2023, 0.0010, 0.0)
    W.f_manuf = base + r.normal(0.0, 0.0011, NM)
    oil = r.normal(0.0, 0.035, NM)
    oil[(YEAR == 2020) & (MON >= 2) & (MON <= 4)] += -0.10
    oil[(YEAR == 2020) & (MON >= 6)] += 0.035
    oil[(YEAR == 2021)] += 0.018
    oil[(YEAR == 2022) & (MON <= 6)] += 0.040
    oil[(YEAR == 2022) & (MON >= 9)] += -0.030
    for mm, v in (("2026-01", 0.012), ("2026-02", -0.020), ("2026-03", 0.015), ("2026-04", -0.030),
                  ("2026-05", -0.050), ("2026-06", -0.020)):
        oil[MI[mm]] = v
    W.f_oil = oil
    coal = r.normal(0.0, 0.040, NM)
    coal[(YEAR == 2021) & (MON >= 7)] += 0.06
    coal[(YEAR == 2022) & (MON <= 8)] += 0.035
    coal[(YEAR == 2023)] += -0.045
    for mm, v in (("2026-01", -0.025), ("2026-02", -0.060), ("2026-03", -0.040), ("2026-04", 0.020),
                  ("2026-05", 0.030), ("2026-06", 0.015)):
        coal[MI[mm]] = v                # the coal slide behind the February cut, then a partial recovery
    W.f_coal = coal
    dairy = r.normal(0.0, 0.022, NM)
    dairy[(YEAR == 2021)] += 0.010
    dairy[(YEAR == 2023) & (MON <= 8)] += -0.012
    W.f_dairy = dairy
    food = 0.0018 + r.normal(0.0, 0.0030, NM) + np.where(YEAR == 2022, 0.004, 0.0)
    W.f_food = food
    dom = np.select([YEAR <= 2019, YEAR == 2020, YEAR == 2021, YEAR == 2022, YEAR == 2023, YEAR >= 2024],
                    [0.0016, 0.0006, 0.0036, 0.0060, 0.0030, 0.0020])
    W.dom = dom + r.normal(0.0, 0.0007, NM)


# ---------------------------------------------------------------------------------------------------- prices
# import and export pass-through of the dollar by SITC section, and each section's foreign driver
IMP_DRIVER = {"0": "food", "1": "food", "2": "manuf", "3": "oil", "4": "food", "5": "manuf", "6": "manuf",
              "7": "manuf", "8": "manuf", "9": "manuf"}
IMP_PASS = {"0": 0.85, "1": 0.80, "2": 0.85, "3": 1.00, "4": 0.85, "5": 0.80, "6": 0.85, "7": 0.80, "8": 0.75,
            "9": 0.70}
EXP_DRIVER = {"0": "dairy", "1": "food", "2": "manuf", "3": "coal", "4": "food", "5": "manuf", "6": "manuf",
              "7": "manuf", "8": "manuf", "9": "manuf"}
EXP_PASS = {"0": 0.90, "1": 0.60, "2": 0.85, "3": 1.00, "4": 0.80, "5": 0.55, "6": 0.90, "7": 0.50, "8": 0.45,
            "9": 0.50}
# each industry's purchases: the import sections it buys (weights) and the share that moves with import prices
IND_IMPORTS = {
    "WFG": {"0": 0.8, "1": 0.2}, "WFP": {"3": 1.0}, "WME": {"7": 1.0}, "WMV": {"7": 1.0},
    "WOT": {"6": 0.5, "8": 0.5}, "RFD": {"0": 1.0}, "ROT": {"8": 0.6, "7": 0.25, "6": 0.15},
    "MFG": {"2": 0.25, "5": 0.30, "6": 0.30, "7": 0.15},
}


def _driver(W, name):
    return {"food": W.f_food, "manuf": W.f_manuf, "oil": W.f_oil, "coal": W.f_coal, "dairy": W.f_dairy}[name]


def _rebase(p):
    return p / p[YEAR == 2025].mean()


def prices(W):
    """Monthly average price indexes, 2025 average = 1 internally (published on the 2019 base): import and export
    prices by SITC section, and the producer price index of each industry's purchases."""
    W.PM, W.PX, W.P = {}, {}, {}
    lag = np.r_[0.0, W.dlog_e[:-1]]
    for s in K.SITC_CODES:
        r = K.rng("pm", s)
        b = IMP_PASS[s]
        d = _driver(W, IMP_DRIVER[s]) - b * (0.78 * W.dlog_e + 0.22 * lag) + r.normal(0.0, 0.0018, NM)
        W.PM[s] = _rebase(np.exp(np.cumsum(d)))
        r = K.rng("px", s)
        b = EXP_PASS[s]
        d = _driver(W, EXP_DRIVER[s]) - b * W.dlog_e + r.normal(0.0, 0.0025, NM)
        W.PX[s] = _rebase(np.exp(np.cumsum(d)))
    dlpm = {s: np.r_[0.0, np.diff(np.log(W.PM[s]))] for s in K.SITC_CODES}
    dlpx0 = np.r_[0.0, np.diff(np.log(W.PX["0"]))]
    for code, name, s0, T, ims in K.INDUSTRIES:
        r = K.rng("pin", code)
        imp = sum(w * dlpm[s] for s, w in IND_IMPORTS[code].items())
        domestic = W.dom + (0.30 * dlpx0 if code in ("WFG", "RFD") else 0.0)
        d = ims * imp + (1.0 - ims) * domestic + r.normal(0.0, 0.0010, NM)
        W.P[code] = _rebase(np.exp(np.cumsum(d)))
    # the producer price index of each industry's outputs: its input prices passed on with a lag, plus margins
    W.POUT = {}
    for code in K.IND_CODES:
        r = K.rng("pout", code)
        dl = np.r_[0.0, np.diff(np.log(W.P[code]))]
        lagged = np.r_[0.0, dl[:-1]]
        d = 0.55 * dl + 0.30 * lagged + 0.15 * W.dom + r.normal(0.0, 0.0012, NM)
        W.POUT[code] = _rebase(np.exp(np.cumsum(d)))


# ---------------------------------------------------------------------------------------------------- business stocks
STOCK_BUILD = {"WME": 0.012, "WMV": 0.010, "ROT": 0.006, "WOT": 0.004}       # March quarter 2026
STOCK_CUT = {"WME": -0.026, "WMV": -0.022, "ROT": -0.014, "WOT": -0.008}     # June quarter 2026


def stocks(W):
    """Physical stocks ($m at 2025 average prices), stock-to-sales ratios, book values and cost of sales."""
    W.X, W.T, W.B, W.S = {}, {}, {}, {}
    for code, name, s0, T, ims in K.INDUSTRIES:
        r = K.rng("stock", code)
        g = r.normal(0.0018, 0.0045, NM)
        g[(YEAR == 2020) & (MON >= 3) & (MON <= 6)] += -0.009
        g[(YEAR == 2021)] += 0.0015
        lx = np.cumsum(g)
        x = np.exp(lx - lx[MI["2025-12"]])
        for mm in ("2026-01", "2026-02", "2026-03"):
            x[MI[mm]:] *= math.exp(STOCK_BUILD.get(code, 0.0) / 3.0)
        for mm in ("2026-04", "2026-05", "2026-06"):
            x[MI[mm]:] *= math.exp(STOCK_CUT.get(code, 0.0) / 3.0)
        drift = 1.0 + 0.025 * np.sin(np.arange(NM) / 11.0 + r.uniform(0, 6.28))
        tt = T * drift * np.exp(r.normal(0.0, 0.010, NM))
        W.T[code] = np.round(tt, 2)           # the ratio TBS publishes (two decimals) is the turnover itself
        p = W.P[code]
        b_mar = K.window_avg(p, MI["2026-03"], W.T[code][MI["2026-03"]])
        x = x / x[MI["2026-03"]]
        level = s0 * math.exp(K.rng("stock", code, "level").normal(0.0, 0.02))   # end-March 2026 book value, $m
        W.X[code] = x * level / b_mar
        W.B[code] = np.array([W.X[code][m] * K.window_avg(p, m, W.T[code][m]) if m >= 3 else np.nan
                              for m in range(NM)])
        W.S[code] = W.B[code] / W.T[code]


def true_cipi(W, q):
    """Business change in inventories in quarter q: the change in physical stock, $m at 2025 prices."""
    m1 = MI[K.quarter_end(q)]
    m0 = m1 - 3
    return sum(W.X[c][m1] - W.X[c][m0] for c in K.IND_CODES)


# ---------------------------------------------------------------------------------------------------- energy exports
COAL_T = 6.6e6           # tonnes a month, 2018
LNG_CARGO_T = 70000.0    # tonnes a cargo
USD_2025 = 1.62          # local dollars a US dollar, 2025 average


def energy(W):
    """Coal, LNG and condensate shipments: tonnes and cargoes by month of shipment, their prices in local dollars,
    and SITC section 3's export price index (2025 value weights). Every coal miner and both LNG projects lodge
    periodic export entries."""
    r = K.rng("energy")
    t = np.arange(NM)
    ar = np.zeros(NM)
    eps = r.normal(0.0, 0.040, NM)
    for i in range(1, NM):
        ar[i] = 0.55 * ar[i - 1] + eps[i]
    coal = COAL_T * np.exp(0.0012 * t + ar)
    coal[(YEAR == 2020) & (MON >= 4) & (MON <= 5)] *= 0.92
    coal[MI["2026-02"]] *= 0.85            # February's floods at the coal ports
    coal[MI["2026-03"]] *= 0.96
    lam = 27.6 + 0.022 * t
    lam[(YEAR == 2023) & (MON == 10)] -= 5.0       # planned maintenance, train 2
    lam[(YEAR == 2025) & (MON == 6)] -= 10.0       # planned maintenance, train 1 (three weeks)
    cargoes = np.maximum(0, np.round(lam + r.normal(0.0, 1.4, NM))).astype(int)
    sizes = [LNG_CARGO_T * (1.0 + r.normal(0.0, 0.012, k)) for k in cargoes]
    lng = np.array([s.sum() for s in sizes])
    cond = 1.7e5 * np.exp(r.normal(0.0, 0.05, NM))
    usd = np.exp(-np.cumsum(W.dlog_e))
    usd = usd / usd[YEAR == 2025].mean() * USD_2025
    lag3 = np.r_[np.zeros(3), W.f_oil[:-3]]
    p_coal = np.exp(np.cumsum(W.f_coal + r.normal(0.0, 0.004, NM)))
    p_lng = np.exp(np.cumsum(0.7 * lag3 + 0.3 * W.f_oil + r.normal(0.0, 0.004, NM)))
    p_cond = np.exp(np.cumsum(W.f_oil + r.normal(0.0, 0.004, NM)))
    p_coal = p_coal / p_coal[YEAR == 2025].mean() * 150.0 * usd
    p_lng = p_lng / p_lng[YEAR == 2025].mean() * 520.0 * usd
    p_cond = p_cond / p_cond[YEAR == 2025].mean() * 560.0 * usd
    W.E_T = {"32": coal, "34": lng, "33": cond}
    W.E_P = {"32": p_coal, "34": p_lng, "33": p_cond}
    W.E_V = {k: W.E_T[k] * W.E_P[k] / 1e6 for k in W.E_T}          # $m, month of shipment
    W.LNG_CARGOES = cargoes
    W.LNG_SIZES = sizes
    w25 = {k: W.E_V[k][YEAR == 2025].sum() for k in W.E_V}
    tot = sum(w25.values())
    px3 = sum(w25[k] / tot * W.E_P[k] / W.E_P[k][YEAR == 2025].mean() for k in W.E_P)
    W.PX["3"] = px3 / px3[YEAR == 2025].mean()
    W.USD = usd


# ---------------------------------------------------------------------------------------------------- goods trade
EXP_SHARE = {"0": 0.262, "1": 0.021, "2": 0.083, "3": 0.338, "4": 0.006, "5": 0.041, "6": 0.081, "7": 0.061,
             "8": 0.039, "9": 0.068}
IMP_SHARE = {"0": 0.071, "1": 0.015, "2": 0.021, "3": 0.118, "4": 0.006, "5": 0.121, "6": 0.119, "7": 0.352,
             "8": 0.129, "9": 0.048}
EXP_Q1_2026 = 9690.0          # $m a month at 2025 prices, March quarter 2026 average
IMP_Q1_2026 = 9205.0
# the June quarter on the March quarter, by section, in volume (the coal ports back after February's floods;
# importers running stocks down after the June leg)
EXP_Q2_MOVE = {"0": 0.002, "1": 0.004, "2": 0.006, "3": 0.031, "4": 0.0, "5": 0.003, "6": -0.004, "7": 0.006,
               "8": 0.002, "9": 0.001}
IMP_Q2_MOVE = {"0": 0.004, "1": 0.002, "2": -0.003, "3": -0.012, "4": 0.0, "5": -0.004, "6": -0.009,
               "7": -0.036, "8": -0.019, "9": -0.002}


def trade(W):
    """Monthly seasonally adjusted export and import volumes by SITC section ($m at 2025 prices) and values."""
    W.VX, W.VM, W.XV, W.MV = {}, {}, {}, {}
    q1 = [MI[m] for m in K.quarter_months("2026Q1")]
    q2 = [MI[m] for m in K.quarter_months("2026Q2")]
    for flow, share, lvl, move, out_v, out_val, pr in (
            ("x", EXP_SHARE, EXP_Q1_2026, EXP_Q2_MOVE, W.XV, W.VX, W.PX),
            ("m", IMP_SHARE, IMP_Q1_2026, IMP_Q2_MOVE, W.MV, W.VM, W.PM)):
        for s in K.SITC_CODES:
            if flow == "x" and s == "3":
                out_val[s] = sum(W.E_V.values())
                out_v[s] = out_val[s] / pr[s]
                continue
            r = K.rng("trade", flow, s)
            g = r.normal(0.0024, 0.013 if s == "3" else 0.008, NM)
            g[(YEAR == 2020) & (MON >= 3) & (MON <= 5)] += -0.045 if flow == "m" else -0.030
            g[(YEAR == 2020) & (MON >= 6) & (MON <= 9)] += 0.030
            lv = np.cumsum(g)
            v = np.exp(lv - lv[q1].mean())
            v = v / v[q1].mean() * share[s] * lvl
            # the June quarter's move on the March quarter, spread over its three months
            target = v[q1].mean() * (1.0 + move[s])
            v[q2] = v[q2] * (target / v[q2].mean())
            out_v[s] = v
            out_val[s] = v * pr[s]


# ---------------------------------------------------------------------------------------------------- published
def published(W):
    """Price indexes as the Office publishes them (2019 average = 100, one decimal), and the same rebased to the
    2025 average as the national accounts use them; TBS's book values and cost of sales to one decimal ($m)."""
    def pub(p):
        return np.round(p / p[YEAR == 2019].mean() * 100.0, 1)
    W.PUB_P = {c: pub(W.P[c]) for c in K.IND_CODES}
    W.PUB_PM = {s: pub(W.PM[s]) for s in K.SITC_CODES}
    W.PUB_PX = {s: pub(W.PX[s]) for s in K.SITC_CODES}
    W.R25_P = {c: v / v[YEAR == 2025].mean() for c, v in W.PUB_P.items()}
    W.R25_PM = {s: v / v[YEAR == 2025].mean() for s, v in W.PUB_PM.items()}
    W.R25_PX = {s: v / v[YEAR == 2025].mean() for s, v in W.PUB_PX.items()}
    W.PUB_B = {c: np.round(W.B[c], 1) for c in K.IND_CODES}
    W.PUB_S = {c: np.round(W.S[c], 1) for c in K.IND_CODES}
    W.PUB_POUT = {c: pub(W.POUT[c]) for c in K.IND_CODES}
    # the Office's goods exports and imports: shipments, seasonally adjusted, $m one decimal
    W.SHIP_VX = {s: np.round(W.VX[s], 1) for s in K.SITC_CODES}
    W.SHIP_VM = {s: np.round(W.VM[s], 1) for s in K.SITC_CODES}
    # TBS's published exports: every coal, LNG and condensate export is on a periodic entry, which TBS's old
    # system recorded in the month it was lodged (the month after the cargoes sailed); the new system, from the
    # January 2026 month, dates them by their shipments, and December 2025 took December's cargoes as well
    W.PUB_VX = {s: W.SHIP_VX[s].copy() for s in K.SITC_CODES}
    W.PUB_VX["3"] = np.round(np.array([tbs_month(W.VX["3"], m) for m in range(NM)]), 1)
    W.PUB_VM = {s: W.SHIP_VM[s].copy() for s in K.SITC_CODES}


def portal_vintage(W):
    """The desk's pull of TBS's portal on 24 June: April 2026 as revised in the May bulletin and May 2026 as first
    published; the June bulletin revised both again. Earlier months are final in both."""
    r = K.rng("portal")
    am = [MI["2026-04"], MI["2026-05"]]
    W.PORTAL_VX, W.PORTAL_VM, W.PORTAL_B, W.PORTAL_S = {}, {}, {}, {}
    for s in K.SITC_CODES:
        for src, dst, flow in ((W.PUB_VX, W.PORTAL_VX, "x"), (W.PUB_VM, W.PORTAL_VM, "m")):
            v = src[s].copy()
            for m, sd in zip(am, (0.0004, 0.0009)):
                e = r.normal(0.0, sd)
                if not (flow == "x" and s == "3"):          # coal, LNG and condensate were not revised
                    v[m] = round(v[m] * (1.0 + e), 1)
            dst[s] = v
    for c in K.IND_CODES:
        b = W.PUB_B[c].copy()
        sl = W.PUB_S[c].copy()
        for m, sd in zip(am, (0.0010, 0.0025)):
            f = 1.0 + r.normal(0.0, sd)
            b[m] = round(W.B[c][m] * f, 1)
            sl[m] = round(W.S[c][m] * (1.0 + r.normal(0.0, sd)), 1)
        W.PORTAL_B[c] = b
        W.PORTAL_S[c] = sl


def turnover_volume(W, c, m, B=None, T=None):
    """An industry's month-end stock at 2025 prices: the book value over the average of its input price index
    (2025 = 1, as published) across the months its stock-to-sales ratio covers."""
    b = W.PUB_B[c][m] if B is None else B
    t = W.T[c][m] if T is None else T
    return b / K.window_avg(W.R25_P[c], m, t)


def turnover_cipi(W, q):
    m1 = MI[K.quarter_end(q)]
    return sum(turnover_volume(W, c, m1) - turnover_volume(W, c, m1 - 3) for c in K.IND_CODES)


def goods_volume(W, q, flow):
    """The Office's goods exports or imports in quarter q at 2025 prices (shipments, as TBS's unit records date
    them), each SITC section's value over its price index rebased to 2025."""
    ms = [MI[m] for m in K.quarter_months(q)]
    if flow == "x":
        return sum(W.SHIP_VX[s][m] / W.R25_PX[s][m] for s in K.SITC_CODES for m in ms)
    return sum(W.SHIP_VM[s][m] / W.R25_PM[s][m] for s in K.SITC_CODES for m in ms)


def simulate():
    W = World()
    drivers(W)
    prices(W)
    energy(W)
    stocks(W)
    trade(W)
    published(W)
    portal_vintage(W)
    return W
