"""British National Grid to WGS84 (OSGB36 transverse Mercator inverse, then a Helmert shift), for the bus stops."""
import math


def _osgb36_latlon(E, N):
    a, b = 6377563.396, 6356256.909
    F0, lat0, lon0 = 0.9996012717, math.radians(49), math.radians(-2)
    N0, E0 = -100000, 400000
    e2 = 1 - (b * b) / (a * a)
    n = (a - b) / (a + b)
    lat, M = lat0, 0
    while N - N0 - M >= 0.00001:
        lat = (N - N0 - M) / (a * F0) + lat
        Ma = (1 + n + (5 / 4) * n ** 2 + (5 / 4) * n ** 3) * (lat - lat0)
        Mb = (3 * n + 3 * n * n + (21 / 8) * n ** 3) * math.sin(lat - lat0) * math.cos(lat + lat0)
        Mc = ((15 / 8) * n ** 2 + (15 / 8) * n ** 3) * math.sin(2 * (lat - lat0)) * math.cos(2 * (lat + lat0))
        Md = (35 / 24) * n ** 3 * math.sin(3 * (lat - lat0)) * math.cos(3 * (lat + lat0))
        M = b * F0 * (Ma - Mb + Mc - Md)
    cosl, sinl, tanl = math.cos(lat), math.sin(lat), math.tan(lat)
    nu = a * F0 / math.sqrt(1 - e2 * sinl ** 2)
    rho = a * F0 * (1 - e2) / (1 - e2 * sinl ** 2) ** 1.5
    eta2 = nu / rho - 1
    VII = tanl / (2 * rho * nu)
    VIII = tanl / (24 * rho * nu ** 3) * (5 + 3 * tanl ** 2 + eta2 - 9 * tanl ** 2 * eta2)
    IX = tanl / (720 * rho * nu ** 5) * (61 + 90 * tanl ** 2 + 45 * tanl ** 4)
    X = 1 / (cosl * nu)
    XI = 1 / (cosl * 6 * nu ** 3) * (nu / rho + 2 * tanl ** 2)
    XII = 1 / (cosl * 120 * nu ** 5) * (5 + 28 * tanl ** 2 + 24 * tanl ** 4)
    XIIA = 1 / (cosl * 5040 * nu ** 7) * (61 + 662 * tanl ** 2 + 1320 * tanl ** 4 + 720 * tanl ** 6)
    dE = E - E0
    lat = lat - VII * dE ** 2 + VIII * dE ** 4 - IX * dE ** 6
    lon = lon0 + X * dE - XI * dE ** 3 + XII * dE ** 5 - XIIA * dE ** 7
    return lat, lon


def bng_to_wgs84(E, N):
    lat, lon = _osgb36_latlon(E, N)
    a, b = 6377563.396, 6356256.909
    e2 = 1 - (b * b) / (a * a)
    nu = a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
    x = nu * math.cos(lat) * math.cos(lon)
    y = nu * math.cos(lat) * math.sin(lon)
    z = (1 - e2) * nu * math.sin(lat)
    tx, ty, tz, s = 446.448, -125.157, 542.060, -20.4894e-6
    rx, ry, rz = [math.radians(v / 3600) for v in (0.1502, 0.2470, 0.8421)]
    x2 = tx + (1 + s) * x - rz * y + ry * z
    y2 = ty + rz * x + (1 + s) * y - rx * z
    z2 = tz - ry * x + rx * y + (1 + s) * z
    a2, b2 = 6378137.000, 6356752.3142
    e22 = 1 - (b2 * b2) / (a2 * a2)
    p = math.sqrt(x2 * x2 + y2 * y2)
    lat2 = math.atan2(z2, p * (1 - e22))
    for _ in range(10):
        nu2 = a2 / math.sqrt(1 - e22 * math.sin(lat2) ** 2)
        lat2 = math.atan2(z2 + e22 * nu2 * math.sin(lat2), p)
    lon2 = math.atan2(y2, x2)
    return math.degrees(lat2), math.degrees(lon2)


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371008.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))
