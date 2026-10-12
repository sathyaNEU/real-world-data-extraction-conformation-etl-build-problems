"""Daily weather at the Kestrel Bend yard and at the state network's station 39 (about six miles south-west), 1 October
1995 to 31 January 2027, and reference evapotranspiration by the FAO-56 Penman-Monteith daily equation from each
station's own air temperature, humidity, wind and solar radiation.

Each water year (October to September) draws from its own stream, so a change to one year never re-rolls another.
The 2026-27 autumn and early winter is a dry one: its October to January rain is set by the water year's wetness
factor, like every other year, at a low draw."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

LAT = 36.32           # degrees north
ELEV_M = 110.0        # the yard station; station 39 sits at 104 m

# monthly climatology (index 0 = January)
TMAX_C = [13.9, 17.4, 20.6, 24.2, 28.6, 32.6, 35.2, 34.6, 31.8, 26.4, 18.8, 13.6]
TMIN_C = [2.6, 3.9, 6.0, 8.3, 11.8, 15.4, 18.2, 17.4, 14.6, 10.0, 5.0, 2.4]
RH_PCT = [83, 74, 67, 58, 50, 47, 46, 48, 50, 56, 70, 82]
WIND_MS = [1.40, 1.80, 2.00, 2.15, 2.15, 2.10, 1.90, 1.80, 1.70, 1.55, 1.40, 1.35]
CLEAR = [0.64, 0.75, 0.80, 0.86, 0.90, 0.93, 0.94, 0.93, 0.90, 0.84, 0.72, 0.62]   # Rs/Rso on a dry day
RAIN_IN = [2.15, 2.05, 1.95, 0.90, 0.38, 0.12, 0.01, 0.02, 0.20, 0.62, 1.10, 1.80]
WET_P = [0.29, 0.27, 0.25, 0.14, 0.07, 0.03, 0.006, 0.01, 0.04, 0.08, 0.15, 0.25]   # chance a day is wet
PERSIST = [0.48, 0.46, 0.44, 0.36, 0.30, 0.25, 0.10, 0.15, 0.25, 0.33, 0.40, 0.47]  # wet after wet

# the wetness of the 2026-27 water year (October to January in the record) is a draw like any other's, fixed here
DRY_WINTER_FACTOR = 0.10


def _days_in(y, m):
    return (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days


def _ra(doy):
    """Extraterrestrial radiation, MJ m-2 day-1 (FAO-56 eq. 21)."""
    phi = math.radians(LAT)
    dr = 1 + 0.033 * math.cos(2 * math.pi * doy / 365)
    d = 0.409 * math.sin(2 * math.pi * doy / 365 - 1.39)
    ws = math.acos(-math.tan(phi) * math.tan(d))
    return 24 * 60 / math.pi * 0.0820 * dr * (ws * math.sin(phi) * math.sin(d) + math.cos(phi) * math.cos(d) * math.sin(ws))


def _esat(t):
    return 0.6108 * math.exp(17.27 * t / (t + 237.3))


def et0_pm(tmax, tmin, rh, u2, rs, doy, elev):
    """FAO-56 Penman-Monteith daily reference ET (mm), soil heat flux taken as zero."""
    tmean = (tmax + tmin) / 2
    es = (_esat(tmax) + _esat(tmin)) / 2
    ea = rh / 100.0 * es
    delta = 4098 * _esat(tmean) / (tmean + 237.3) ** 2
    p = 101.3 * ((293 - 0.0065 * elev) / 293) ** 5.26
    gamma = 0.665e-3 * p
    ra = _ra(doy)
    rso = (0.75 + 2e-5 * elev) * ra
    rns = 0.77 * rs
    sigma = 4.903e-9
    rnl = sigma * ((tmax + 273.16) ** 4 + (tmin + 273.16) ** 4) / 2 * (0.34 - 0.14 * math.sqrt(ea)) * \
        (1.35 * min(rs / rso, 1.0) - 0.35)
    rn = rns - rnl
    et = (0.408 * delta * rn + gamma * 900 / (tmean + 273) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))
    return max(et, 0.05), rso


def simulate():
    """Returns {date: dict} for the yard (true local weather) and for station 39."""
    yard, st39 = {}, {}
    d = K.WEATHER_START
    wy_state = {}
    while d <= K.WEATHER_END:
        wy = d.year + (d.month >= 10)
        if wy not in wy_state:
            r = K.rng("weather", wy)
            wet = float(r.gamma(4.0, 0.25))
            if wy == 2027:
                wet = DRY_WINTER_FACTOR
            wy_state[wy] = dict(r=r, wet=wet, heat=float(r.normal(0, 0.9)), tanom=0.0, wet_prev=False)
        s = wy_state[wy]
        r = s["r"]
        m = d.month - 1
        doy = d.timetuple().tm_yday
        f = s["wet"]
        p_wet = min(0.92, WET_P[m] * (0.55 + 0.45 * f))
        if s["wet_prev"]:
            p_wet = min(0.95, PERSIST[m] * (0.7 + 0.3 * min(f, 2.0)))
        is_wet = r.random() < p_wet
        mean_amt = RAIN_IN[m] / max(WET_P[m] * _days_in(d.year, d.month), 0.04)
        amt = float(r.gamma(0.75, mean_amt / 0.75)) * f ** 0.45 if is_wet else 0.0
        if is_wet and amt < 0.01:
            amt = 0.01
        s["wet_prev"] = is_wet
        s["tanom"] = 0.72 * s["tanom"] + float(r.normal(0, 1.6))
        tmax = TMAX_C[m] + s["heat"] + s["tanom"] - (3.2 if is_wet else 0.0)
        tmin = TMIN_C[m] + 0.6 * s["heat"] + 0.7 * s["tanom"] + (1.2 if is_wet else 0.0) + float(r.normal(0, 0.8))
        tmin = min(tmin, tmax - 3.0)
        rh = RH_PCT[m] + (14 if is_wet else 0) + float(r.normal(0, 4)) - 0.8 * s["tanom"]
        rh = float(np.clip(rh, 18, 98))
        u2 = max(0.4, WIND_MS[m] * float(r.lognormal(0, 0.22)) + (0.4 if is_wet else 0))
        clear = CLEAR[m] * float(np.clip(r.normal(1.0, 0.07), 0.6, 1.08))
        if is_wet:
            clear *= float(r.uniform(0.38, 0.66))
        rso_dummy = (0.75 + 2e-5 * ELEV_M) * _ra(doy)
        rs = min(clear, 1.0) * rso_dummy
        e_mm, _ = et0_pm(tmax, tmin, rh, u2, rs, doy, ELEV_M)
        yard[d] = dict(tmax=tmax, tmin=tmin, rh=rh, u2=u2, rs=rs, rain_in=amt, et0_mm=e_mm)
        # station 39: the same storms with its own amounts, a little warmer and windier
        r2 = K.rng("st39", d.isoformat())
        rain39 = amt * float(r2.lognormal(0, 0.18)) if amt > 0 else (0.01 if r2.random() < 0.004 else 0.0)
        tmax39 = tmax + 0.35 + float(r2.normal(0, 0.4))
        tmin39 = tmin + 0.15 + float(r2.normal(0, 0.5))
        tmin39 = min(tmin39, tmax39 - 3.0)
        rh39 = float(np.clip(rh - 1.5 + float(r2.normal(0, 2.0)), 15, 99))
        u239 = max(0.4, u2 * 1.09 + float(r2.normal(0, 0.12)))
        rs39 = rs * float(np.clip(r2.normal(1.0, 0.025), 0.9, 1.1))
        e39, _ = et0_pm(tmax39, tmin39, rh39, u239, rs39, doy, 104.0)
        st39[d] = dict(tmax=tmax39, tmin=tmin39, rh=rh39, u2=u239, rs=rs39, rain_in=rain39, et0_mm=e39)
        d += dt.timedelta(days=1)
    return yard, st39


# days the yard logger did not record (battery, card or sensor failures); the record keeps no row for some and a
# blank row for others
YARD_GAPS_ABSENT = [(dt.date(2016, 7, 11), 4), (dt.date(2021, 2, 3), 2), (dt.date(2026, 12, 20), 2)]
YARD_GAPS_BLANK = [(dt.date(2019, 1, 15), 3), (dt.date(2022, 8, 22), 3), (dt.date(2024, 3, 6), 1)]


def yard_missing():
    out = set()
    for start, n in YARD_GAPS_ABSENT + YARD_GAPS_BLANK:
        for k in range(n):
            out.add(start + dt.timedelta(days=k))
    return out


def yard_absent():
    out = set()
    for start, n in YARD_GAPS_ABSENT:
        for k in range(n):
            out.add(start + dt.timedelta(days=k))
    return out


def reported(yard, st39):
    """What each station reports: station 39 in its export's units (mm, W/m2, C, m/s), ET0 and rain to 0.01 mm; the
    yard logger in inches, F, mph and langleys, ET0 and rain to 0.01 inch. Returns {date: (et0_in, rain_in)} for each
    station as the procedure reads it (station 39 converted from millimetres) plus the raw rows."""
    s39, yd = {}, {}
    for d, w in st39.items():
        s39[d] = dict(eto_mm=round(w["et0_mm"], 2), precip_mm=round(w["rain_in"] * 25.4, 2),
                      sol_wm2=round(w["rs"] * 1e6 / 86400, 1), tmax_c=round(w["tmax"], 1), tmin_c=round(w["tmin"], 1),
                      rh=int(round(w["rh"])), wind=round(w["u2"], 1))
    miss = yard_missing()
    for d, w in yard.items():
        if d < K.DISTRICT_STATION_START or d in miss:
            continue
        yd[d] = dict(et0_in=round(w["et0_mm"] / 25.4, 2), rain_in=round(w["rain_in"], 2),
                     tmax_f=round(w["tmax"] * 9 / 5 + 32, 1), tmin_f=round(w["tmin"] * 9 / 5 + 32, 1),
                     rh=round(w["rh"], 1), wind_mph=round(w["u2"] * 2.23694, 1), srad_ly=round(w["rs"] * 23.9006, 0))
    return s39, yd


def spliced(s39, yd):
    """The District's weather record (WOP 6.1): station 39 to 30 April 2014, the yard station from 1 May 2014, a day
    the yard did not record taking station 39's values. Inches."""
    out = {}
    for d in K.daterange(K.WEATHER_START, K.WEATHER_END):
        if d < K.SPLICE or d not in yd:
            out[d] = (s39[d]["eto_mm"] / 25.4, s39[d]["precip_mm"] / 25.4)
        else:
            out[d] = (yd[d]["et0_in"], yd[d]["rain_in"])
    return out
