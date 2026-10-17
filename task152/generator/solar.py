"""Hourly solar resource for the Hadley Ranch site: geometry, clear sky, cloud regimes by season, the Erbs split of
global into direct and diffuse, Hay-Davies transposition onto the 25-degree south-facing tables, air and module
temperature, wind and rain. One stream per year so a year's weather never depends on another's draw."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

DEG = np.pi / 180.0


def hours_of_year(y):
    """Local (MST) hour starts of calendar year y as (date index, hour) arrays."""
    n = (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
    doy = np.repeat(np.arange(1, n + 1), 24)
    hour = np.tile(np.arange(24), n)
    return doy, hour, n


def geometry(doy, hour, y):
    """Solar geometry at the middle of each local hour: cos(zenith), cos(incidence on the tables), extraterrestrial
    normal irradiance."""
    ndays = 366 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 365
    g = 2 * np.pi * (doy - 1 + (hour + 0.5 - 12) / 24.0) / ndays
    decl = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
            + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    eot = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g) - 0.014615 * np.cos(2 * g)
                    - 0.040849 * np.sin(2 * g))
    solar_time = hour + 0.5 + (4.0 * (K.LON - (-105.0)) + eot) / 60.0
    w = (15.0 * (solar_time - 12.0)) * DEG
    lat, tilt = K.LAT * DEG, K.TILT * DEG
    cosz = np.sin(lat) * np.sin(decl) + np.cos(lat) * np.cos(decl) * np.cos(w)
    cost = np.sin(lat - tilt) * np.sin(decl) + np.cos(lat - tilt) * np.cos(decl) * np.cos(w)
    e0 = 1.000110 + 0.034221 * np.cos(g) + 0.001280 * np.sin(g) + 0.000719 * np.cos(2 * g) + 0.000077 * np.sin(2 * g)
    return cosz, cost, 1367.0 * e0


# monthly regime probabilities (clear, broken, overcast) for central Arizona: winter storms December to March, a dry
# spring, the July to September monsoon's afternoon build-ups, a dry autumn
REGIME = {1: (0.70, 0.17, 0.13), 2: (0.70, 0.18, 0.12), 3: (0.74, 0.17, 0.09), 4: (0.85, 0.11, 0.04),
          5: (0.89, 0.09, 0.02), 6: (0.91, 0.08, 0.01), 7: (0.54, 0.38, 0.08), 8: (0.56, 0.36, 0.08),
          9: (0.70, 0.24, 0.06), 10: (0.82, 0.13, 0.05), 11: (0.79, 0.13, 0.08), 12: (0.70, 0.16, 0.14)}
T_MONTH = {1: 12.6, 2: 14.9, 3: 18.4, 4: 22.6, 5: 27.6, 6: 32.6, 7: 34.3, 8: 33.6, 9: 30.6, 10: 24.4, 11: 17.3, 12: 12.3}
# the month's mean wind against the year's: calm winters, the spring winds from March to June
WIND_MONTH = {1: 0.85, 2: 0.95, 3: 1.10, 4: 1.20, 5: 1.25, 6: 1.20, 7: 1.10, 8: 1.00, 9: 0.95, 10: 0.90, 11: 0.85,
              12: 0.80}
CLOUD_YEAR_SD = 0.16        # a year's cloudiness against the usual, relative
HAZE_YEAR_SD = 0.0133       # a year's clear-sky transmittance against the usual (dust, smoke), relative
HAZE_DAY_MAX = 1.06         # the clearest air the site sees, against the usual
RAIN_P = {1: 0.55, 2: 0.55, 3: 0.50, 4: 0.30, 5: 0.15, 6: 0.15, 7: 0.40, 8: 0.45, 9: 0.40, 10: 0.35, 11: 0.40, 12: 0.55}


def year_weather(y):
    """One calendar year's hourly weather. Returns a dict of numpy arrays over the year's local hours."""
    r = K.rng("weather", y)
    doy, hour, n = hours_of_year(y)
    dates = [dt.date(y, 1, 1) + dt.timedelta(days=int(i)) for i in range(n)]
    month_d = np.array([d.month for d in dates])
    cosz, cost, i0 = geometry(doy, hour, y)
    # the year's own character: cloudier or clearer than usual, hazier or cleaner air
    cloud_year = float(np.clip(1.0 + r.normal(0.0, CLOUD_YEAR_SD), 0.6, 1.4))
    haze_year = float(r.normal(1.0, HAZE_YEAR_SD))
    # day regimes, with persistence
    regime = np.zeros(n, dtype=int)
    prev = 0
    for i in range(n):
        pc, pb, po = REGIME[int(month_d[i])]
        pb2, po2 = min(pb * cloud_year, 0.6), min(po * cloud_year, 0.5)
        if prev > 0 and r.random() < 0.35:
            regime[i] = prev
        else:
            u = r.random()
            regime[i] = 0 if u < 1 - pb2 - po2 else (1 if u < 1 - po2 else 2)
        prev = regime[i]
    # clear-sky global (Haurwitz), scaled for the site's clean desert air and the day's haze
    cz = np.clip(cosz, 0.0, None)
    with np.errstate(divide="ignore", over="ignore"):
        cs = np.where(cz > 0.01, 1098.0 * cz * np.exp(-0.057 / np.maximum(cz, 1e-3)), 0.0)
    day_haze = np.repeat(np.clip(r.normal(haze_year, 0.012, n), 0.93, HAZE_DAY_MAX), 24)
    cs = cs * 1.022 * day_haze
    # hourly cloud transmission by regime
    reg_h = np.repeat(regime, 24)
    mon_h = np.repeat(month_d, 24)
    k = np.ones(24 * n)
    noise = r.random(24 * n)
    ar = np.zeros(24 * n)
    e = r.normal(0, 1, 24 * n)
    for i in range(1, 24 * n):
        ar[i] = 0.72 * ar[i - 1] + 0.69 * e[i]
    broken = reg_h == 1
    monsoon_pm = broken & np.isin(mon_h, [7, 8, 9]) & (hour >= 12)
    k = np.where(broken, np.clip(0.82 + 0.20 * ar, 0.18, 1.03), k)
    k = np.where(monsoon_pm, np.clip(0.62 + 0.26 * ar, 0.12, 1.04), k)
    k = np.where(broken & np.isin(mon_h, [7, 8, 9]) & (hour < 12), np.clip(0.95 + 0.06 * ar, 0.6, 1.03), k)
    over = reg_h == 2
    k = np.where(over, np.clip(0.34 + 0.16 * ar, 0.08, 0.85), k)
    clear = reg_h == 0
    k = np.where(clear, np.clip(0.995 + 0.012 * ar, 0.94, 1.02), k)
    ghi = cs * k
    g0h = np.where(cz > 0.01, i0 * cz, 0.0)
    kt = np.where(g0h > 1.0, np.clip(ghi / np.maximum(g0h, 1.0), 0.0, 1.0), 0.0)
    kd = np.where(kt <= 0.22, 1.0 - 0.09 * kt,
                  np.where(kt <= 0.80, 0.9511 - 0.1604 * kt + 4.388 * kt ** 2 - 16.638 * kt ** 3 + 12.336 * kt ** 4,
                           0.165))
    dhi = ghi * kd
    dni = np.where(cz > 0.05, (ghi - dhi) / np.maximum(cz, 0.05), 0.0)
    ai = np.clip(dni / i0, 0.0, 1.0)
    rb = np.where(cz > 0.05, np.clip(cost, 0.0, None) / np.maximum(cz, 0.05), 0.0)
    tilt = K.TILT * DEG
    poa = (dni * np.clip(cost, 0.0, None) + dhi * (ai * rb + (1 - ai) * (1 + np.cos(tilt)) / 2.0)
           + ghi * K.ALBEDO * (1 - np.cos(tilt)) / 2.0)
    poa = np.where(cz > 0.0, np.clip(poa, 0.0, None), 0.0)
    # rear-side irradiance of a bifacial table: ground-reflected light seen through the rows and the sky behind
    rear = np.where(cz > 0.0, K.ALBEDO * ghi * 0.36 + dhi * 0.06, 0.0)
    # air temperature: the month's mean, a daily anomaly with persistence, a dry-climate diurnal swing, cloud cooling
    tm = np.array([T_MONTH[int(m)] for m in month_d], dtype=float)
    # smooth the monthly means into a daily curve
    tday = np.interp(np.arange(n), [dt.date(y, m, 15).timetuple().tm_yday - 1 for m in range(1, 13)],
                     [T_MONTH[m] for m in range(1, 13)], period=n)
    anom = np.zeros(n)
    ea = r.normal(0, 1, n)
    for i in range(1, n):
        anom[i] = 0.75 * anom[i - 1] + 1.3 * ea[i]
    tmean = tday + anom - 2.2 * (regime == 2) - 0.8 * (regime == 1) + float(r.normal(0, 0.12))
    swing = np.where(regime == 2, 4.0, 8.2)
    tmean_h, swing_h = np.repeat(tmean, 24), np.repeat(swing, 24)
    tamb = tmean_h + swing_h * np.sin(2 * np.pi * (hour - 9.0) / 24.0)
    wm = np.repeat(np.array([WIND_MONTH[int(m)] for m in month_d]), 24)
    wind = np.clip(r.weibull(2.0, 24 * n) * 3.1 * wm * (1.0 + 0.35 * np.sin(2 * np.pi * (hour - 10) / 24.0)), 0.2, 15.0)
    tmod = tamb + poa * np.exp(-3.47 - 0.0594 * wind)
    # rain on cloudy days: winter storm totals, monsoon cells
    rain_d = np.zeros(n)
    for i in range(n):
        m = int(month_d[i])
        if regime[i] >= 1 and r.random() < RAIN_P[m] * (1.0 if regime[i] == 2 else 0.55):
            amt = r.gamma(1.15, 6.5 if m in (7, 8, 9) else 5.0)
            rain_d[i] = round(float(amt), 1)
    return dict(y=y, n=n, dates=dates, doy=doy, hour=hour, ghi=ghi, dni=dni, dhi=dhi, poa=poa, rear=rear,
                tamb=tamb, tmod=tmod, wind=wind, rain=rain_d, regime=regime, cosz=cosz)


def years(a, b):
    return {y: year_weather(y) for y in range(a, b + 1)}
