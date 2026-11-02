"""Deterministic writers (csv, xlsx, docx, pdf), the grid conversion and the build clock."""
import csv
import datetime as dt
import io
import math
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ZIP_TIME = (2026, 3, 18, 9, 0, 0)
AS_OF = dt.date(2026, 3, 20)


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])


def normalise_zip(path, stamp):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name == "docProps/core.xml":
            s = data.decode("utf-8")
            s = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", r"\g<1>%s\g<2>" % stamp, s)
            s = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>%s\g<2>" % stamp, s)
            data = s.encode("utf-8")
        out.append((name, data))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def save_workbook(wb, path, when, creator):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = when
    wb.properties.modified = when
    wb.save(path)
    normalise_zip(path, when.strftime("%Y-%m-%dT%H:%M:%SZ"))


def save_docx(doc, path, when, author):
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.created = when
    cp.modified = when
    cp.revision = 1
    doc.save(path)
    normalise_zip(path, when.strftime("%Y-%m-%dT%H:%M:%SZ"))


def pdf_invariant():
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.pageCompression = 1


# ----- British National Grid (OSGB36) to WGS84 latitude and longitude -----
def bng_to_wgs84(E, N):
    a, b = 6377563.396, 6356256.909
    F0, lat0, lon0, N0, E0 = 0.9996012717, math.radians(49), math.radians(-2), -100000.0, 400000.0
    e2 = 1 - (b * b) / (a * a)
    n = (a - b) / (a + b)
    lat, M = lat0, 0.0
    while True:
        lat = (N - N0 - M) / (a * F0) + lat
        dl, sl = lat - lat0, lat + lat0
        M = b * F0 * ((1 + n + 1.25 * n ** 2 + 1.25 * n ** 3) * dl
                      - (3 * n + 3 * n ** 2 + 21 / 8 * n ** 3) * math.sin(dl) * math.cos(sl)
                      + (15 / 8 * n ** 2 + 15 / 8 * n ** 3) * math.sin(2 * dl) * math.cos(2 * sl)
                      - 35 / 24 * n ** 3 * math.sin(3 * dl) * math.cos(3 * sl))
        if abs(N - N0 - M) < 1e-5:
            break
    s = math.sin(lat)
    nu = a * F0 / math.sqrt(1 - e2 * s * s)
    rho = a * F0 * (1 - e2) / (1 - e2 * s * s) ** 1.5
    eta2 = nu / rho - 1
    t = math.tan(lat)
    sec = 1 / math.cos(lat)
    VII = t / (2 * rho * nu)
    VIII = t / (24 * rho * nu ** 3) * (5 + 3 * t * t + eta2 - 9 * t * t * eta2)
    IX = t / (720 * rho * nu ** 5) * (61 + 90 * t * t + 45 * t ** 4)
    X = sec / nu
    XI = sec / (6 * nu ** 3) * (nu / rho + 2 * t * t)
    XII = sec / (120 * nu ** 5) * (5 + 28 * t * t + 24 * t ** 4)
    XIIA = sec / (5040 * nu ** 7) * (61 + 662 * t * t + 1320 * t ** 4 + 720 * t ** 6)
    dE = E - E0
    lat1 = lat - VII * dE ** 2 + VIII * dE ** 4 - IX * dE ** 6
    lon1 = lon0 + X * dE - XI * dE ** 3 + XII * dE ** 5 - XIIA * dE ** 7
    # Helmert, OSGB36 to WGS84
    sp, cp_, sl_, cl = math.sin(lat1), math.cos(lat1), math.sin(lon1), math.cos(lon1)
    nu2 = a / math.sqrt(1 - e2 * sp * sp)
    x, y, z = nu2 * cp_ * cl, nu2 * cp_ * sl_, (1 - e2) * nu2 * sp
    tx, ty, tz, sc = 446.448, -125.157, 542.060, -20.4894e-6
    rx, ry, rz = [math.radians(v / 3600) for v in (0.1502, 0.2470, 0.8421)]
    x2 = tx + (1 + sc) * x - rz * y + ry * z
    y2 = ty + rz * x + (1 + sc) * y - rx * z
    z2 = tz - ry * x + rx * y + (1 + sc) * z
    aw, bw = 6378137.0, 6356752.3142
    e2w = 1 - (bw * bw) / (aw * aw)
    p = math.hypot(x2, y2)
    phi = math.atan2(z2, p * (1 - e2w))
    for _ in range(10):
        nuw = aw / math.sqrt(1 - e2w * math.sin(phi) ** 2)
        phi = math.atan2(z2 + e2w * nuw * math.sin(phi), p)
    return math.degrees(phi), math.degrees(math.atan2(y2, x2))
