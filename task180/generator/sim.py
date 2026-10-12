"""The simulation: injection, the seismicity it drives, what each network records of it, the automatic system's
origins, the stations and their gaps, and the two neighbouring files (the federal catalogue, the groundwater
levels). One random stream per component, so a change in one never moves another's draws."""
import calendar
import datetime as dt
import math

import numpy as np
import pandas as pd
from scipy.special import ndtr

import geo as G
import world as W

M_MIN, M_MAX = 0.0, 2.6
UTC0 = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)


def rng(k):
    return np.random.default_rng([W.SEED, k])


def months(start=(2023, 1), end=(2026, 9)):
    y, m = start
    out = []
    while (y, m) <= end:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def month_bounds_utc(y, m):
    a = dt.datetime(y, m, 1, tzinfo=W.LOCAL)
    b = dt.datetime(y + (m == 12), 1 if m == 12 else m + 1, 1, tzinfo=W.LOCAL)
    return int(a.timestamp()), int(b.timestamp())


def secs(d):
    return int(d.timestamp())


# ------------------------------------------------------------------------------------------------- injection
INJ_WELLS = {"MOS": [("MST-GT2", 0.58), ("MST-GT4", 0.42)], "PFB": [("PFB-GT2", 1.0)], "LZR": [("LZR-GT2", 1.0)],
             "WDR": [("WDR-GT2", 1.0)], "OTM": [("OTM-GT2", 1.0)]}
PROD_WELLS = {"MOS": ["MST-GT1", "MST-GT3"], "PFB": ["PFB-GT1"], "LZR": ["LZR-GT1"], "WDR": ["WDR-GT1"],
              "OTM": ["OTM-GT1"]}
PROD_TEMP = {"MOS": 118.0, "PFB": 104.0, "LZR": 131.0, "WDR": 97.0, "OTM": 139.0}
BASE_P = {"MOS": 6.0, "PFB": 9.5, "LZR": 4.0, "WDR": 11.0, "OTM": 7.5}


def month_factor(p, m):
    return W.MONTH_FACTOR[m] ** W.SEASON_SHARPNESS[p]


def hours_index():
    a = int(W.RECORD_START.timestamp())
    z = int(W.RECORD_END.timestamp())
    t = np.arange(a, z, 3600)
    loc = pd.to_datetime(t, unit="s", utc=True).tz_convert(W.LOCAL)
    return t, loc


def injection():
    """Hourly injection at each injection well (the plants' telemetry to the authority), and monthly volumes per
    well, metered at the wellhead, summed over local months."""
    r = rng(1)
    t, loc = hours_index()
    ly, lm, ld, lh = loc.year.to_numpy(), loc.month.to_numpy(), loc.day.to_numpy(), loc.hour.to_numpy()
    hourly = []
    for p in W.PLANTS:
        mean = np.empty(len(t))
        for (y, m) in months():
            sel = (ly == y) & (lm == m)
            mean[sel] = W.PEAK_FLOW[p] * month_factor(p, m) * W.YEAR_FACTOR[y] * (1 + 0.025 * r.standard_normal())
        diurnal = 1 + 0.07 * np.sin(2 * np.pi * (lh - 4) / 24) + 0.04 * np.sin(4 * np.pi * (lh - 5) / 24)
        flow = mean * diurnal * (1 + 0.035 * r.standard_normal(len(t)))
        on = np.ones(len(t), bool)
        mo, d0, nd = W.REVISION[p]
        for y in (2023, 2024, 2025, 2026):
            start = dt.datetime(y, mo, d0, 6, tzinfo=W.LOCAL).timestamp()
            on &= ~((t >= start) & (t < start + nd * 86400))
        for _ in range(r.poisson(3.2 * 3.75)):
            k = int(r.integers(0, len(t)))
            on[k:k + int(r.integers(4, 31))] = False
        flow = np.where(on, np.maximum(flow, 0.0), 0.0)
        wells = INJ_WELLS[p]
        if len(wells) == 1:
            split = [np.ones(len(t))]
        else:
            drift = np.repeat(0.58 + 0.015 * r.standard_normal(len(months())), 1)
            share = np.empty(len(t))
            for k, (y, m) in enumerate(months()):
                share[(ly == y) & (lm == m)] = drift[k]
            split = [share, 1 - share]
        for (w, _), sh in zip(wells, split):
            q = flow * sh
            pres = np.where(q > 0, BASE_P[p] + 0.11 * q + 0.5 * r.standard_normal(len(t)), 2.4 + 0.3 * r.random(len(t)))
            temp = np.where(q > 0, W.REINJECTION_TEMP_C[p] + 0.9 * r.standard_normal(len(t)), np.nan)
            hourly.append(pd.DataFrame(dict(plant=p, well=w, t=t, flow_ls=q, pressure_bar=pres, temp_c=temp,
                                            y=ly, m=lm)))
    hourly = pd.concat(hourly, ignore_index=True)
    vol = hourly.assign(v=hourly["flow_ls"] * 3.6).groupby(["plant", "well", "y", "m"])["v"].sum()
    rows = []
    for (p, w, y, m), v in vol.items():
        tm = hourly[(hourly.well == w) & (hourly.y == y) & (hourly.m == m)]
        tq = tm[tm.flow_ls > 0]
        rows.append(dict(plant=p, well=w, role="injection", year=int(y), month=int(m), volume_metered=float(v),
                         pressure_bar=float(tq["pressure_bar"].mean()) if len(tq) else float("nan"),
                         temp_c=float(tq["temp_c"].mean()) if len(tq) else float("nan")))
    monthly = pd.DataFrame(rows)
    prod = []
    tot = monthly.groupby(["plant", "year", "month"])["volume_metered"].sum()
    for (p, y, m), v in tot.items():
        for w in PROD_WELLS[p]:
            prod.append(dict(plant=p, well=w, role="production", year=y, month=m,
                             volume_metered=v * (1 + 0.006 * r.standard_normal()) / len(PROD_WELLS[p]),
                             pressure_bar=float("nan"), temp_c=PROD_TEMP[p] + 0.7 * r.standard_normal()))
    monthly = pd.concat([monthly, pd.DataFrame(prod)], ignore_index=True)
    return hourly.drop(columns=["y", "m"]), monthly


def plant_volume(monthly):
    """Metered injection per plant and month (m3)."""
    i = monthly[monthly["role"] == "injection"]
    return i.groupby(["plant", "year", "month"])["volume_metered"].sum()


def response():
    """Earthquakes of ML 1.0 or more per 100,000 m3 metered, from each plant's first-quarter target at 2026's flows."""
    out = {}
    for p in W.PLANTS:
        v = 0.0
        for m in (1, 2, 3):
            v += W.PEAK_FLOW[p] * month_factor(p, m) * W.YEAR_FACTOR[2026] * 1e-3 * calendar.monthrange(2026, m)[1] * 86400
        out[p] = W.TARGET_Q1[p] / (v / 1e5)
    return out


# ------------------------------------------------------------------------------------------------- seismicity
def _gr(r, n, b):
    beta = b * math.log(10)
    out = np.empty(n)
    k = 0
    while k < n:
        x = M_MIN + r.exponential(1 / beta, size=n - k)
        x = x[x <= M_MAX]
        out[k:k + len(x)] = x
        k += len(x)
    return out


def _cluster(r, n, seg):
    """Epicentres around an injection well's open-hole section: a point along the section, then an offset
    elongated along the reservoir's N20E fracture trend; nothing farther than 3 km from the section."""
    (la1, lo1, d1), (la2, lo2, d2) = seg
    lat0, lon0 = (la1 + la2) / 2, (lo1 + lo2) / 2
    ax, ay = G.to_xy(la1, lo1, lat0, lon0)
    bx, by = G.to_xy(la2, lo2, lat0, lon0)
    out_lat, out_lon, out_dep = [], [], []
    th = math.radians(20)
    need = n
    while need > 0:
        t = r.random(need)
        u = r.normal(0, 0.70, need)
        v = r.normal(0, 0.33, need)
        x = ax + t * (bx - ax) + u * math.sin(th) + v * math.cos(th)
        y = ay + t * (by - ay) + u * math.cos(th) - v * math.sin(th)
        dep = (d1 + t * (d2 - d1)) / 1000 + r.normal(0, 0.30, need)
        lat, lon = G.to_latlon(x, y, lat0, lon0)
        dd = G.dist_to_segment(lat, lon, seg)
        ok = dd <= 3.0
        out_lat.append(lat[ok]); out_lon.append(lon[ok]); out_dep.append(dep[ok])
        need -= int(ok.sum())
    return np.concatenate(out_lat)[:n], np.concatenate(out_lon)[:n], np.concatenate(out_dep)[:n]


def plant_events(monthly):
    """Every earthquake of ML 0.0 or more the reservoirs produce, January 2023 to September 2026."""
    r = rng(2)
    vol = plant_volume(monthly)
    resp = response()
    rows = []
    for p in W.PLANTS:
        b = W.B_VALUE[p]
        wells = W.OPEN_HOLE[p]
        share = [s for _, s in INJ_WELLS[p]]
        for (y, m) in months():
            v = vol[(p, y, m)]
            n1 = resp[p] * v / 1e5
            lam = n1 * 10 ** (b * (1.0 - M_MIN))
            n = r.poisson(lam)
            a, z = month_bounds_utc(y, m)
            t = np.sort(r.integers(a, z, size=n)) + r.random(n)
            mag = _gr(r, n, b)
            wi = r.choice(len(wells), size=n, p=share)
            lat = np.empty(n); lon = np.empty(n); dep = np.empty(n)
            for k in range(len(wells)):
                sel = wi == k
                lat[sel], lon[sel], dep[sel] = _cluster(r, int(sel.sum()), wells[k])
            rows.append(pd.DataFrame(dict(plant=p, t=t, ml=mag, lat=lat, lon=lon, depth=dep, kind="earthquake")))
    return pd.concat(rows, ignore_index=True)


def sequences(ev):
    """Each plant's earthquakes keep at least MIN_SEPARATION_S between them, except the second shocks: a share of
    the earthquakes is followed seconds later by another at the same spot (its own magnitude from the same law).
    Second shocks are appended after every first-pass event, so the detection draws of the others never move."""
    r = rng(13)
    ev = ev.copy()
    for p in W.PLANTS:
        idx = ev.index[ev["plant"] == p]
        t = ev.loc[idx, "t"].to_numpy().copy()
        order = np.argsort(t, kind="stable")
        tt = t[order]
        for k in range(1, len(tt)):
            if tt[k] - tt[k - 1] < W.MIN_SEPARATION_S:
                tt[k] = tt[k - 1] + W.MIN_SEPARATION_S + 0.37 * (k % 7)
        t[order] = tt
        ev.loc[idx, "t"] = t
    end = secs(W.RECORD_END)
    ev = ev[ev["t"] < end - 60].reset_index(drop=True)
    rows = []
    for p in W.PLANTS:
        e = ev[ev["plant"] == p]
        pick = r.random(len(e)) < W.DOUBLET_SHARE
        e = e[pick]
        n = len(e)
        dt_s = r.uniform(*W.DOUBLET_DELAY_S, n)
        dx, dy = r.normal(0, 0.12, n), r.normal(0, 0.12, n)
        lat = e["lat"].to_numpy() + dy / G.KM_LAT
        lon = e["lon"].to_numpy() + dx / np.array([G.km_lon(x) for x in e["lat"].to_numpy()])
        rows.append(pd.DataFrame(dict(plant=p, t=e["t"].to_numpy() + dt_s, ml=_gr(r, n, W.B_VALUE[p]), lat=lat,
                                      lon=lon, depth=e["depth"].to_numpy() + r.normal(0, 0.08, n), kind="earthquake")))
    second = pd.concat(rows, ignore_index=True)
    second = second[second["t"] < end - 1].reset_index(drop=True)
    return pd.concat([ev, second], ignore_index=True)


def background_events():
    """Natural seismicity of the region (deeper, sparse), kept six kilometres or more from every open hole."""
    r = rng(3)
    a, z = secs(W.RECORD_START), secs(W.RECORD_END)
    n = r.poisson(0.22 * (z - a) / 86400)
    t = np.sort(r.integers(a, z, size=n)) + r.random(n)
    mag = 0.5 + r.exponential(1 / (1.0 * math.log(10)), size=n)
    mag = np.minimum(mag, 3.4)
    lat = np.empty(n); lon = np.empty(n)
    k = 0
    while k < n:
        la = r.uniform(47.80, 48.16, n - k); lo = r.uniform(11.28, 12.06, n - k)
        dmin = np.full(len(la), 99.0)
        for p in W.PLANTS:
            for seg in W.OPEN_HOLE[p]:
                dmin = np.minimum(dmin, G.dist_to_segment(la, lo, seg))
        ok = dmin >= 6.0
        m_ = int(ok.sum())
        lat[k:k + m_] = la[ok][:n - k]; lon[k:k + m_] = lo[ok][:n - k]
        k += m_
    dep = r.uniform(6.0, 14.5, n)
    return pd.DataFrame(dict(plant="", t=t, ml=mag, lat=lat, lon=lon, depth=dep, kind="earthquake"))


QUARRY = W.QUARRY


def blasts():
    """Production blasts at the two limestone quarries: working days, late morning to mid afternoon."""
    r = rng(4)
    rows = []
    d = W.RECORD_START.date()
    while d < W.RECORD_END.date():
        if d.weekday() < 5 and d not in W.HOLIDAYS:
            for q, (la, lo) in QUARRY.items():
                for _ in range(r.poisson(0.55)):
                    hh = r.uniform(10.0, 15.0)
                    tl = dt.datetime(d.year, d.month, d.day, tzinfo=W.LOCAL) + dt.timedelta(hours=hh)
                    x, y = r.normal(0, 0.18, 2)
                    lat, lon = G.to_latlon(x, y, la, lo)
                    rows.append(dict(plant="", t=tl.timestamp(), ml=float(np.clip(r.normal(1.12, 0.24), 0.62, 1.78)),
                                     lat=float(lat), lon=float(lon), depth=0.0, kind="explosion", quarry=q))
        d += dt.timedelta(days=1)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------- detection
def local_hour(t):
    ts = pd.to_datetime(np.asarray(t), unit="s", utc=True).tz_convert(W.LOCAL)
    return ts, ts.hour + ts.minute / 60 + ts.second / 3600


def detect_params(plant, t):
    """The magnitude half the earthquakes are recorded at, and its spread, for each event's plant and local time."""
    ts, h = local_hour(t)
    n = len(h)
    m50 = np.full(n, W.RURAL_DETECT["day"][0]); sg = np.full(n, 0.12)
    night = (h >= 22) | (h < 6)
    m50[night] = W.RURAL_DETECT["night"][0]
    plant = np.asarray(plant)
    pfb = plant == "PFB"
    if pfb.any():
        dates = ts.date
        free = np.array([(d.weekday() >= 5) or (d in W.HOLIDAYS) for d in dates])
        quiet = (h >= W.QUIET_HOURS[0]) | (h < W.QUIET_HOURS[1])
        sh = ((h >= W.SHOULDER[0][0]) & (h < W.SHOULDER[0][1])) | ((h >= W.SHOULDER[1][0]) & (h < W.SHOULDER[1][1]))
        day = ~quiet & ~sh
        for mask, key in ((quiet, "quiet"), (sh, "shoulder")):
            sel = pfb & mask
            m50[sel], sg[sel] = W.PFB_DETECT[key]
        sel = pfb & day & ~free
        m50[sel], sg[sel] = W.PFB_DETECT["day"]
        sel = pfb & day & free
        m50[sel], sg[sel] = W.PFB_DETECT["day_free"]
    lzr_old = (plant == "LZR") & (np.asarray(t) < W.LZR_NEW_STATION.timestamp())
    m50[lzr_old], sg[lzr_old] = W.LZR_OLD_DETECT
    return m50, sg


def detect(ev, k=5):
    r = rng(k)
    m50, sg = detect_params(ev["plant"].to_numpy(), ev["t"].to_numpy())
    p = ndtr((ev["ml"].to_numpy() - m50) / sg)
    return r.random(len(ev)) < p


def simulate():
    hourly, inj = injection()
    ev = sequences(plant_events(inj))
    bg = background_events()
    bl = blasts()
    ev["detected"] = detect(ev, 5)
    bg["detected"] = detect(bg.assign(plant="MOS"), 6)           # the regional networks see them as a rural one
    bl["detected"] = True
    return dict(hourly=hourly, inj=inj, ev=ev, bg=bg, bl=bl)


if __name__ == "__main__":
    w = simulate()
    ev = w["ev"]
    for p in W.PLANTS:
        e = ev[(ev.plant == p)]
        n1 = (e.ml >= 1.0).sum(); d1 = ((e.ml >= 1.0) & e.detected).sum()
        print(p, "true ML>=1", n1, "recorded", d1, "share %.3f" % (d1 / n1), "events total", len(e), "detected", e.detected.sum())
    print("background", len(w["bg"]), w["bg"].detected.sum(), "blasts", len(w["bl"]))


# ------------------------------------------------------------------------------------------------- the networks
# station code, plant network, offset from the plant's wellhead (km east, km north), site
STATIONS = [
    ("MOS1", "MOS", (-3.1, 2.4), "Hof Ostermaier, Kellerraum"), ("MOS2", "MOS", (2.9, 1.8), "Hochbehälter Moorstetten"),
    ("MOS3", "MOS", (1.2, -3.6), "Waldparkplatz Lindenholz"), ("MOS4", "MOS", (-2.0, -2.2), "Kläranlage Moorstetten"),
    ("PFB1", "PFB", (0.6, 0.9), "Grundschule Pfeilbrunn, Kellerraum"), ("PFB2", "PFB", (2.1, -0.4), "Wasserwerk Pfeilbrunn"),
    ("PFB3", "PFB", (-0.9, -1.1), "Feuerwache Pfeilbrunn"), ("PFB4", "PFB", (1.4, 1.9), "Bauhof Pfeilbrunn"),
    ("LZR1", "LZR", (-2.6, 2.7), "Hof Wiesmaier, Kellerraum"), ("LZR2", "LZR", (3.3, 0.9), "Pumpwerk Lanzenried"),
    ("LZR3", "LZR", (0.4, -4.1), "Forsthütte Hochfilz"), ("LZR4", "LZR", (-3.4, -1.3), "Umspannwerk Lanzenried"),
    ("LZR5", "LZR", (0.9, -1.2), "Feldstation Lanzenried Süd"),
    ("WDR1", "WDR", (-2.2, 3.0), "Hof Brandlmaier, Kellerraum"), ("WDR2", "WDR", (3.4, 1.5), "Hochbehälter Wendelsried"),
    ("WDR3", "WDR", (1.6, -3.2), "Jagdhütte Moosleiten"), ("WDR4", "WDR", (-3.0, -1.7), "Wertstoffhof Wendelsried"),
    ("OTM1", "OTM", (-2.8, 2.2), "Hof Kreitmaier, Kellerraum"), ("OTM2", "OTM", (3.1, 2.4), "Pumpwerk Ottenmoos"),
    ("OTM3", "OTM", (2.2, -3.0), "Forsthaus Ottenmoos"), ("OTM4", "OTM", (-1.7, -3.3), "Sportplatz Ottenmoos"),
    ("LGX1", "", None, "Regionalstation Hohenleiten"), ("LGX2", "", None, "Regionalstation Grafenberg"),
]
REGIONAL_POS = {"LGX1": (48.0123, 11.7562), "LGX2": (47.9055, 11.8461)}
INSTALL = {"MOS": dt.datetime(2019, 9, 24, 10, 15, tzinfo=W.LOCAL), "PFB": dt.datetime(2021, 6, 15, 9, 40, tzinfo=W.LOCAL),
           "LZR": dt.datetime(2020, 3, 11, 13, 5, tzinfo=W.LOCAL), "WDR": dt.datetime(2021, 10, 5, 11, 30, tzinfo=W.LOCAL),
           "OTM": dt.datetime(2022, 4, 26, 10, 50, tzinfo=W.LOCAL), "": dt.datetime(2016, 5, 18, 12, 0, tzinfo=W.LOCAL)}
# the 2026 digitiser exchange: one station of each plant network per quarter; the fourth in October
UPGRADE_DAY = {"MOS1": (2, 17), "MOS2": (5, 12), "MOS3": (8, 25), "MOS4": (10, 20),
               "PFB1": (3, 3), "PFB2": (4, 21), "PFB3": (7, 8), "PFB4": (10, 13),
               "LZR1": (2, 24), "LZR2": (6, 9), "LZR3": (9, 1), "LZR5": (10, 27),
               "WDR1": (3, 10), "WDR2": (5, 5), "WDR3": (7, 21), "WDR4": (10, 6),
               "OTM1": (2, 10), "OTM2": (6, 23), "OTM3": (9, 15), "OTM4": (10, 29)}


def stations():
    """The inventory: each station with its epochs (location code 00 until the 2026 digitiser exchange, 10 after).
    LZR4 was taken out when LZR5 went in nearer the Lanzenried well (15 July 2025)."""
    r = rng(7)
    rows = []
    for code, plant, off, site in STATIONS:
        if plant:
            lat0, lon0 = W.WELLHEAD[plant]
            lat, lon = G.to_latlon(off[0], off[1], lat0, lon0)
        else:
            lat, lon = REGIONAL_POS[code]
        elev = float(r.uniform(520, 690))
        start = INSTALL[plant] + dt.timedelta(days=int(r.integers(0, 9)), minutes=int(r.integers(0, 300)))
        base = dict(station=code, plant=plant, site=site, lat=float(lat), lon=float(lon), elev=elev)
        if code == "LZR5":
            start = W.LZR_NEW_STATION + dt.timedelta(minutes=int(r.integers(5, 40)))
        if code == "LZR4":
            rows.append(dict(base, loc="00", start=start, end=W.LZR_NEW_STATION - dt.timedelta(minutes=int(r.integers(30, 90)))))
            continue
        if code in UPGRADE_DAY:
            mo, d = UPGRADE_DAY[code]
            vs = dt.datetime(2026, mo, d, tzinfo=W.LOCAL) + dt.timedelta(hours=float(r.uniform(8.3, 10.6)))
            ve = vs + dt.timedelta(hours=float(r.uniform(2.1, 4.8)))
            vs = vs.replace(second=0, microsecond=0); ve = ve.replace(second=0, microsecond=0)
            off_end = vs + dt.timedelta(minutes=int(r.integers(18, 34)))
            if ve.date() < W.EXTRACT_DATE:
                rows.append(dict(base, loc="00", start=start, end=off_end, visit=(vs, ve)))
                rows.append(dict(base, loc="10", start=ve, end=None))
                continue
        rows.append(dict(base, loc="00", start=start, end=None))
    return rows


def gaps(st):
    """Data gaps of 60 s or more in 2026 (to 30 September, local), per station epoch and channel, UTC. Outages take
    every channel; recentring the horizontal masses takes a few minutes on the horizontals only; an exchange visit
    powers the station down a quarter of an hour before its old epoch ends, and the new epoch starts when it is back."""
    r = rng(8)
    a, z = secs(W.YEAR_START_2026), secs(W.RECORD_END)
    rows, visits = [], []
    for e in st:
        es = max(a, int(e["start"].timestamp()))
        ee = min(z, int(e["end"].timestamp())) if e["end"] else z
        if ee <= es:
            continue
        span = ee - es
        n = r.poisson(1.15 * span / (30 * 86400))
        for _ in range(n):
            s0 = int(r.integers(es, ee))
            dur = float(np.exp(r.normal(math.log(4300), 1.0)))
            if r.random() < 0.04:
                dur = float(r.uniform(20, 70)) * 3600
            s1 = min(ee, s0 + int(dur))
            for ch in ("HHZ", "HHN", "HHE"):
                rows.append((e["station"], e["loc"], ch, s0, s1))
        for _ in range(r.poisson(2.0 * span / (30 * 86400))):
            s0 = int(r.integers(es, ee))
            s1 = s0 + int(r.uniform(120, 720))
            for ch in ("HHN", "HHE"):
                rows.append((e["station"], e["loc"], ch, s0, min(ee, s1)))
        if e.get("visit") and e["end"] is not None:
            vs, ve = e["visit"]
            if vs.timestamp() < z:
                rows.extend((e["station"], e["loc"], ch, int(vs.timestamp()), min(z, int(e["end"].timestamp())))
                            for ch in ("HHZ", "HHN", "HHE"))
            visits.append(dict(station=e["station"], plant=e["plant"], start=vs, end=ve, kind="exchange"))
    # service visits (battery, enclosure): each plant station once or twice in the period, downtime logged as gaps
    for e in st:
        if not e["plant"] or e["end"] is not None and e["end"].timestamp() < a:
            continue
        es = max(a, int(e["start"].timestamp()))
        ee = min(z, int(e["end"].timestamp())) if e["end"] else z
        if ee - es < 3 * 86400:
            continue
        for _ in range(int(r.integers(1, 3))):
            day = dt.datetime.fromtimestamp(int(r.integers(es, ee - 86400)), W.LOCAL).date()
            if day.weekday() >= 5 or day in W.HOLIDAYS:
                continue
            vs = dt.datetime(day.year, day.month, day.day, tzinfo=W.LOCAL) + dt.timedelta(hours=float(r.uniform(8.5, 14.5)))
            vs = vs.replace(second=0, microsecond=0)
            ve = vs + dt.timedelta(minutes=int(r.integers(35, 95)))
            if not (es <= vs.timestamp() and ve.timestamp() <= ee):
                continue
            rows.extend((e["station"], e["loc"], ch, int(vs.timestamp()), int(ve.timestamp())) for ch in ("HHZ", "HHN", "HHE"))
            visits.append(dict(station=e["station"], plant=e["plant"], start=vs, end=ve, kind="service"))
    g = pd.DataFrame(rows, columns=["station", "loc", "channel", "s", "e"])
    g = g[(g.e - g.s) >= 60].sort_values(["s", "station", "channel"]).reset_index(drop=True)
    return g, sorted(visits, key=lambda v: v["start"])


# ------------------------------------------------------------------------------------------------- catalogues
LETTERS = np.array(list("abcdefghijklmnopqrstuvwxyz"))


def _ids(r, prefix_by_year, years):
    seen = set()
    out = []
    for y in years:
        while True:
            s = "%s%d%s" % (prefix_by_year, y, "".join(r.choice(LETTERS, 4)))
            if s not in seen:
                seen.add(s)
                out.append(s)
                break
    return out


def region_name(lat, lon):
    best, bd = "Alpenvorland", 10.0
    for p in W.PLANTS:
        d = float(G.dist_to_point(lat, lon, W.WELLHEAD[p]))
        if d < bd:
            best, bd = "%s (Molassebecken)" % W.NAME[p], d
    return best


def reviewed(w):
    """The survey's reviewed catalogue: every event a network recorded, as the analyst finalised it."""
    r = rng(9)
    ev = w["ev"][w["ev"]["detected"]]
    bg = w["bg"][w["bg"]["detected"]]
    bl = w["bl"].assign(detected=True)
    allv = pd.concat([ev, bg, bl], ignore_index=True).sort_values("t").reset_index(drop=True)
    n = len(allv)
    t = allv["t"].to_numpy() + r.normal(0, 0.04, n)
    lat0, lon0 = allv["lat"].to_numpy(), allv["lon"].to_numpy()
    ex, ey = r.normal(0, 0.20, n), r.normal(0, 0.20, n)
    lat = lat0 + ey / G.KM_LAT
    lon = lon0 + ex / np.array([G.km_lon(x) for x in lat0])
    blast = (allv["kind"] == "explosion").to_numpy()
    dep = np.where(blast, 0.0, np.maximum(0.6, allv["depth"].to_numpy() + r.normal(0, 0.35, n)))
    ml = np.round(allv["ml"].to_numpy() + r.normal(0, 0.05, n), 2)
    years = pd.to_datetime(t, unit="s", utc=True).year
    ids = _ids(r, "lg", years)
    nsta = np.clip(4 + r.poisson(np.clip(2.4 * (allv["ml"].to_numpy() - 0.3), 0.2, None)), 4, 12)
    gap = np.clip(r.normal(118, 32, n) - 18 * (nsta - 4), 38, 290).round(0)
    rms = np.round(np.abs(r.normal(0.045, 0.018, n)) + 0.012, 3)
    herr = np.round(np.abs(r.normal(0.25, 0.08, n)) + 0.06 + 0.25 * (nsta == 4), 2)
    analyst = np.where(r.random(n) < 0.61, "ga", "ae")
    reviewed_at = t + r.uniform(2, 13, n) * 86400
    cat = pd.DataFrame(dict(event_id=ids, t=t, lat=lat, lon=lon, depth_km=np.round(dep, 2), ml=ml, ml_n_sta=nsta,
                            n_phases=nsta * 2 - r.integers(0, 3, n), az_gap_deg=gap, rms_s=rms, h_err_km=herr,
                            event_type=np.where(blast, "explosion", "earthquake"),
                            depth_fixed=np.where(blast, "yes", "no"), analyst=analyst, reviewed_at=reviewed_at,
                            plant=allv["plant"].to_numpy(), kind=allv["kind"].to_numpy(), ml_true=allv["ml"].to_numpy(),
                            t_true=allv["t"].to_numpy()))
    cat["region"] = [region_name(a, b) for a, b in zip(cat.lat, cat.lon)]
    return cat


def automatic(cat):
    """The real-time system's origins: every event it picked up has one to four origins, each a fresh solution as
    further picks arrive, with its own public id (creation time, process counter). Analysts delete false triggers
    from the database, so every origin here belongs to an event the review kept; nothing in a row names its event.
    ev_key (the reviewed event) and step are the generator's own columns and never ship. The analysts' origins
    follow (manual_origins)."""
    r = rng(10)
    p_auto = ndtr((cat["ml"].to_numpy() - 0.62) / 0.18)
    take = r.random(len(cat)) < p_auto
    src = cat[take].reset_index(drop=True)
    rows = []
    sig_loc = [0.75, 0.45, 0.30, 0.22]
    sig_ml = [0.22, 0.14, 0.10, 0.08]
    for e in src.itertuples():
        q = float(np.clip(0.14 + 0.12 * (e.ml - 0.8), 0.08, 0.60))
        k = 1 + r.binomial(3, q)
        created = e.t + r.uniform(22, 64)
        picks = int(5 + r.integers(0, 3))
        for j in range(k):
            sx, sy = r.normal(0, sig_loc[j], 2)
            la = e.lat + sy / G.KM_LAT
            lo = e.lon + sx / G.km_lon(e.lat)
            de = max(0.5, e.depth_km + r.normal(0, 0.9 / (j + 1)))
            rows.append(dict(ev_key=e.event_id, step=j, created=created, t=e.t + r.normal(0, 0.15 / (j + 1)),
                             lat=la, lon=lo, depth_km=round(de, 1), ml_auto=round(e.ml + 0.06 + r.normal(0, sig_ml[j]), 2),
                             n_picks=picks, az_gap=float(np.clip(r.normal(150, 40) - 25 * j, 40, 330))))
            created += r.uniform(70, 540)
            picks += int(2 + r.integers(0, 3))
    out = pd.DataFrame(rows).sort_values(["created"]).reset_index(drop=True)
    a, z = secs(W.RECORD_START), secs(W.RECORD_END)
    out = out[(out.t >= a) & (out.t < z)].reset_index(drop=True)
    # public ids as the system writes them: creation time to the microsecond and the locator's running counter
    micro = r.integers(0, 1000000, len(out))
    counter = 40000 + np.cumsum(r.integers(1, 4, len(out)))
    cr = pd.to_datetime(np.floor(out["created"].to_numpy()), unit="s", utc=True)
    out["origin_id"] = ["Origin/%s.%06d.%d" % (c.strftime("%Y%m%d%H%M%S"), m, n) for c, m, n in zip(cr, micro, counter)]
    out["created"] = np.floor(out["created"].to_numpy()) + micro / 1e6
    out["author"] = "scautoloc@lgrt1"
    return pd.concat([out, manual_origins(cat, out)], ignore_index=True)


def manual_origins(cat, auto):
    """The analysts' origins: the review stores each finalised solution as a further origin of the event, created
    when the event was finalised, with the reviewer's login as author. Same table, same id scheme."""
    r = rng(18)
    a, z = secs(W.RECORD_START), secs(W.RECORD_END)
    c = cat[(cat["t"] >= a) & (cat["t"] < z)].reset_index(drop=True)
    micro = r.integers(0, 1000000, len(c))
    created = np.floor(c["reviewed_at"].to_numpy())
    order = np.argsort(created, kind="stable")
    counter = np.empty(len(c), int)
    counter[order] = 61000 + np.cumsum(r.integers(1, 4, len(c)))
    cr = pd.to_datetime(created, unit="s", utc=True)
    m = pd.DataFrame(dict(ev_key=c["event_id"], step=99, created=created + micro / 1e6, t=c["t"], lat=c["lat"],
                          lon=c["lon"], depth_km=c["depth_km"], ml_auto=c["ml"], n_picks=c["n_phases"],
                          az_gap=c["az_gap_deg"], author=c["analyst"] + "@lgrt1"))
    m["origin_id"] = ["Origin/%s.%06d.%d" % (x.strftime("%Y%m%d%H%M%S"), u, n) for x, u, n in zip(cr, micro, counter)]
    assert not set(m["origin_id"]) & set(auto["origin_id"])
    return m


def federal(cat):
    """The federal agency's catalogue of the wider region, magnitude 2.0 and over: the survey's larger events under
    the agency's own ids and magnitudes, and natural earthquakes beyond the plants' zones."""
    r = rng(11)
    big = cat[(cat.ml >= 2.0) & (cat.event_type == "earthquake")]
    rows = []
    for e in big.itertuples():
        mw = e.ml >= 2.4
        mag = round(e.ml - 0.21 + r.normal(0, 0.06), 1) if mw else round(e.ml + r.normal(0, 0.08), 1)
        rows.append(dict(t=e.t + r.normal(0, 0.25), lat=round(e.lat + r.normal(0, 0.006), 2),
                         lon=round(e.lon + r.normal(0, 0.008), 2), depth_km=10.0 if r.random() < 0.3 else round(e.depth_km + r.normal(0, 1.0), 1),
                         mag=mag, mag_type="Mw" if mw else "ML"))
    a, z = secs(W.RECORD_START), secs(W.RECORD_END)
    for _ in range(r.poisson(46 * 3.75)):
        rows.append(dict(t=float(r.integers(a, z)), lat=round(float(r.uniform(47.3, 48.9)), 2),
                         lon=round(float(r.uniform(10.2, 13.4)), 2), depth_km=round(float(r.uniform(4, 22)), 1),
                         mag=round(float(2.0 + r.exponential(0.42)), 1), mag_type="ML"))
    f = pd.DataFrame(rows).sort_values("t").reset_index(drop=True)
    f = f[f["mag"] >= 2.0].reset_index(drop=True)                   # the agency lists its own magnitude 2.0 and over
    f["mag_type"] = np.where(f["mag"] >= 2.8, "Mw", f["mag_type"])
    f["evid"] = ["FSD%d%05d" % (pd.Timestamp(x, unit="s", tz="UTC").year, 10 + 7 * k) for k, x in enumerate(f.t)]
    return f


def groundwater():
    """Shallow groundwater monitoring at each plant (the water-law permit's condition), monthly, 2025 to 2026."""
    r = rng(12)
    rows = []
    for p in W.PLANTS:
        for k in (1, 2):
            base = float(r.uniform(3.2, 11.8))
            for (y, m) in months((2025, 1), (2026, 9)):
                lvl = base + 0.55 * math.cos(2 * math.pi * (m - 4) / 12) + 0.18 * r.standard_normal()
                rows.append(dict(plant=p, well="%s-GWM%d" % (p, k), year=y, month=m, level_m_bgl=round(lvl, 2),
                                 temp_c=round(9.6 + 0.9 * math.sin(2 * math.pi * (m - 5) / 12) + 0.2 * r.standard_normal(), 1),
                                 ec_us_cm=int(round(512 + 40 * r.standard_normal()))))
    return pd.DataFrame(rows)


def field_log(visits):
    """The field crew's visit log: arrival and departure at the site, in local time as the crew writes it; the
    station goes down after arrival and is back before departure."""
    r = rng(15)
    rows = []
    for v in visits:
        arr = v["start"] - dt.timedelta(minutes=int(r.integers(6, 26)))
        dep = v["end"] + dt.timedelta(minutes=int(r.integers(10, 41)))
        rows.append(dict(v, arrival=arr, departure=dep))
    return rows


def meter_readings(monthly):
    """Each well's monthly volume from its meter, which the operator reports; the hourly flows the plant's control
    system transmits integrate to within a few parts per thousand of it."""
    r = rng(14)
    m = monthly.copy()
    m["volume_reported"] = np.round(m["volume_metered"] * (1 + 0.0025 * r.standard_normal(len(m)))).astype(int)
    return m


def simulate_all():
    w = simulate()
    w["cat"] = reviewed(w)
    w["auto"] = automatic(w["cat"])
    w["stations"] = stations()
    w["gaps"], w["visits"] = gaps(w["stations"])
    w["field"] = field_log(w["visits"])
    w["inj"] = meter_readings(w["inj"])
    w["federal"] = federal(w["cat"])
    w["gw"] = groundwater()
    return w
