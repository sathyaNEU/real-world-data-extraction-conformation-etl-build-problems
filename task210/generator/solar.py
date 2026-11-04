"""NOAA solar position (General Solar Position Calculations), vectorised.

sun_position(utc_datetimes (numpy datetime64[s]), lat_deg, lon_deg) -> (elevation_deg, azimuth_deg)
Azimuth is measured clockwise from true north. Refraction is ignored (it moves the
apparent sun by under 0.6 degrees near the horizon only).
"""
import numpy as np


def sun_position(t_utc, lat, lon):
    t = np.asarray(t_utc, dtype="datetime64[s]")
    # fractional day of year and hour
    year_start = t.astype("datetime64[Y]").astype("datetime64[s]")
    doy = ((t - year_start).astype(np.int64) / 86400.0)  # 0-based day + fraction
    hour = (t - t.astype("datetime64[D]").astype("datetime64[s]")).astype(np.int64) / 3600.0
    yr = t.astype("datetime64[Y]").astype(int) + 1970
    ndays = np.where(((yr % 4 == 0) & (yr % 100 != 0)) | (yr % 400 == 0), 366.0, 365.0)
    g = 2.0 * np.pi / ndays * (np.floor(doy) + (hour - 12.0) / 24.0)
    eqtime = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g)
                       - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    decl = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
            + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    time_offset = eqtime + 4.0 * lon  # minutes
    tst = hour * 60.0 + time_offset
    ha = np.radians(tst / 4.0 - 180.0)
    phi = np.radians(lat)
    cos_zen = np.sin(phi) * np.sin(decl) + np.cos(phi) * np.cos(decl) * np.cos(ha)
    cos_zen = np.clip(cos_zen, -1.0, 1.0)
    zen = np.arccos(cos_zen)
    elev = 90.0 - np.degrees(zen)
    # azimuth clockwise from north
    sin_zen = np.sin(zen)
    sin_zen = np.where(sin_zen < 1e-9, 1e-9, sin_zen)
    cos_az = (np.sin(decl) - np.sin(phi) * cos_zen) / (np.cos(phi) * sin_zen)
    cos_az = np.clip(cos_az, -1.0, 1.0)
    az = np.degrees(np.arccos(cos_az))
    az = np.where(ha > 0, 360.0 - az, az)
    return elev, az


if __name__ == "__main__":
    # sanity: Sheffield-ish 53.38N, -1.47E; 2026-12-21 12:00 UTC should be ~13.1 deg elevation, az ~180
    t = np.array(["2026-12-21T12:06:00", "2026-06-21T12:06:00", "2026-03-20T06:00:00", "2026-10-15T08:00:00", "2027-01-15T09:00:00"], dtype="datetime64[s]")
    e, a = sun_position(t, 53.38, -1.47)
    for ti, ei, ai in zip(t, e, a):
        print(ti, round(float(ei), 2), round(float(ai), 1))
