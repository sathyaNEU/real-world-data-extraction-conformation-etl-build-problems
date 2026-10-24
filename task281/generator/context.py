"""The agencies' own context series that came with the pack: the Division of Correction's average daily population,
the State Police communications centers' call volume, the State Highway Administration's winter operations log and
the Comptroller's overtime expenditure table. None of them is read by the placement."""
import datetime as dt

import numpy as np

import common as K

CTX_SEED = 41
FACILITIES = [("HRC", "Harlan Road Correctional Facility", 1288), ("ACF", "Avesford Correctional Facility", 1032),
              ("TWC", "Thornmere Women's Correctional Center", 744), ("MCI", "Merrimont Correctional Institution", 1710),
              ("BRF", "Brannock Ridge Pre-Release Facility", 520), ("CDC", "Capital District Detention Center", 960),
              ("WSF", "Wexley Springs Facility", 612), ("SCU", "Special Confinement Unit", 288)]
GARAGES = [("OXG", "Oxbow Bend"), ("KPG", "Kettle Pass"), ("LMG", "Lamberton Mills"), ("SHG", "Shadwell"),
           ("NCG", "Norcross Gap"), ("PRG", "Pell River")]
MONTHS = [dt.date(2025, 7, 1) + dt.timedelta(days=31 * k) for k in range(12)]


def month_starts():
    out = []
    y, m = 2025, 7
    for _ in range(12):
        out.append(dt.date(y, m, 1))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def inmate_rows():
    rng = np.random.default_rng(CTX_SEED)
    rows = []
    for code, name, cap in FACILITIES:
        level = cap * rng.uniform(0.86, 1.04)
        for m in month_starts():
            level = level * (1 + rng.normal(0.0, 0.012))
            rows.append([m.strftime("%Y-%m"), code, name, "%.1f" % level, str(cap)])
    rows.sort(key=lambda r: (r[0], r[1]))
    return (["month", "facility_code", "facility", "average_daily_population", "rated_capacity"], rows)


def cad_rows():
    rng = np.random.default_rng(CTX_SEED + 1)
    rows = []
    for c, base in (("North", 610.0), ("South", 455.0)):
        for i in range(K.FY26_DAYS):
            d = K.fy26_day(i)
            wk = 1.12 if d.weekday() >= 4 else 1.0
            summer = 1 + 0.10 * np.cos(2 * np.pi * (i - 20) / 365)
            calls = rng.poisson(base * wk * summer)
            ten = rng.poisson(calls * 1.35)
            radio = rng.poisson(calls * 4.8)
            rows.append([d.isoformat(), c, str(calls), str(ten), str(radio)])
    rows.sort(key=lambda r: (r[0], r[1]))
    return (["date", "center", "calls_911", "calls_ten_digit", "radio_transmissions"], rows)


def winter_rows():
    rng = np.random.default_rng(CTX_SEED + 2)
    rows = []
    n = 0
    d = dt.datetime(2025, 11, 9, 0, 0)
    while d < dt.datetime(2026, 3, 28):
        d += dt.timedelta(hours=float(rng.uniform(70, 260)))
        dur = float(rng.uniform(6, 40))
        for code, name in GARAGES:
            if rng.uniform() < 0.72:
                n += 1
                start = d + dt.timedelta(minutes=int(rng.integers(-180, 180)))
                end = start + dt.timedelta(hours=dur * rng.uniform(0.8, 1.25))
                crews = int(rng.integers(4, 15))
                miles = int(crews * rng.uniform(38, 70))
                salt = round(miles * rng.uniform(0.18, 0.42), 1)
                rows.append(["W26-%04d" % n, code, name, start.strftime("%Y-%m-%d %H:%M"),
                             end.strftime("%Y-%m-%d %H:%M"), str(crews), str(miles), "%.1f" % salt])
    rows.sort(key=lambda r: (r[3], r[1]))
    return (["event_id", "garage_code", "garage", "event_start", "event_end", "crews_out", "lane_miles_treated",
             "salt_tons"], rows)


def otprog_rows():
    rng = np.random.default_rng(CTX_SEED + 3)
    progs = [("Department of Public Safety", "Division of Correction, custody operations"),
             ("Department of Public Safety", "Division of Correction, pretrial detention"),
             ("Department of Public Safety", "Merrimont State Police, field operations"),
             ("Department of Public Safety", "Merrimont State Police, communications"),
             ("Department of Health", "Behavioral Health Administration, forensic services"),
             ("Department of Health", "Developmental Disabilities Administration, residential centers"),
             ("Department of Transportation", "State Highway Administration, maintenance"),
             ("Department of Transportation", "Transit Administration, operations"),
             ("Department of Juvenile Services", "Residential operations"),
             ("Department of Natural Resources", "Natural Resources Police")]
    rows = []
    for a, p in progs:
        h = float(rng.uniform(40000, 900000))
        rows.append((a, p, int(round(h)), int(round(h * rng.uniform(46, 61)))))
    return rows
