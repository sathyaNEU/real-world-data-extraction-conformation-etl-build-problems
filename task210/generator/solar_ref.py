"""External solar reference for task210's checks and verifier: NOAA's solar calculator (the spreadsheet) equations, in
Julian centuries, a separate implementation from generator/solar.py (NOAA's General Solar Position fractional-year
approximation, which builds the pack) and from verify.py's Astronomical Almanac formulae. The generator never imports
it. Geometric elevation, no refraction, as solar.py; sunrise and sunset at minus 0.833 degrees.

    sun(datetime_utc, lat, lon) -> (elevation, azimuth clockwise from north), degrees
    rise_set(date, lat, lon)    -> (sunrise_utc, sunset_utc) for that UTC-noon-centred day
"""
import datetime as dt
import math

TOL_DEG = 0.5      # the agreement asserted between this reference and each solar implementation, degrees


def _jd(t):
    y, m = t.year, t.month
    d = t.day + (t.hour + t.minute / 60 + t.second / 3600) / 24
    if m <= 2:
        y, m = y - 1, m + 12
    a = y // 100
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + 2 - a + a // 4 - 1524.5


def sun(t, lat, lon):
    T = (_jd(t) - 2451545.0) / 36525.0
    L0 = (280.46646 + T * (36000.76983 + T * 0.0003032)) % 360
    M = 357.52911 + T * (35999.05029 - 0.0001537 * T)
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)
    r = math.radians
    C = (math.sin(r(M)) * (1.914602 - T * (0.004817 + 0.000014 * T)) + math.sin(r(2 * M)) * (0.019993 - 0.000101 * T)
         + math.sin(r(3 * M)) * 0.000289)
    omega = 125.04 - 1934.136 * T
    lam = L0 + C - 0.00569 - 0.00478 * math.sin(r(omega))
    eps = 23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60) / 60 + 0.00256 * math.cos(r(omega))
    dec = math.degrees(math.asin(math.sin(r(eps)) * math.sin(r(lam))))
    yv = math.tan(r(eps / 2)) ** 2
    eqt = 4 * math.degrees(yv * math.sin(2 * r(L0)) - 2 * e * math.sin(r(M)) + 4 * e * yv * math.sin(r(M)) * math.cos(2 * r(L0))
                           - 0.5 * yv * yv * math.sin(4 * r(L0)) - 1.25 * e * e * math.sin(2 * r(M)))
    tst = (t.hour * 60 + t.minute + t.second / 60 + eqt + 4 * lon) % 1440
    ha = tst / 4 + 180 if tst / 4 < 0 else tst / 4 - 180
    cz = math.sin(r(lat)) * math.sin(r(dec)) + math.cos(r(lat)) * math.cos(r(dec)) * math.cos(r(ha))
    zen = math.degrees(math.acos(max(-1.0, min(1.0, cz))))
    x = (math.sin(r(lat)) * math.cos(r(zen)) - math.sin(r(dec))) / (math.cos(r(lat)) * math.sin(r(zen)))
    a = math.degrees(math.acos(max(-1.0, min(1.0, x))))
    az = (a + 180) % 360 if ha > 0 else (540 - a) % 360
    return 90 - zen, az


def _cross(lat, lon, t0, t1, rising):
    for _ in range(40):
        tm = t0 + (t1 - t0) / 2
        up = sun(tm, lat, lon)[0] > -0.833
        if up == rising:
            t1 = tm
        else:
            t0 = tm
    return t0 + (t1 - t0) / 2


def rise_set(day, lat, lon):
    """Sunrise and sunset (UTC) of the local day at a western longitude, found by bisection on this reference."""
    noon = dt.datetime(day.year, day.month, day.day, 12) - dt.timedelta(minutes=4 * lon)
    return (_cross(lat, lon, noon - dt.timedelta(hours=11), noon, True),
            _cross(lat, lon, noon, noon + dt.timedelta(hours=11), False))
