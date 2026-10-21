"""The pack's CSV extracts, cut from the fleet's truth table the way each source system writes them: the Division
of Motor Vehicles' registration snapshot, the inspection program's test records, the county and body code lists,
the pilot dismantlers' invoice lines and three series the Department keeps beside its inventory work."""
import csv
import datetime as dt
import io

import numpy as np

import fleet as F
import stations as S
import vin as V
import world as W


def write_csv(path, cols, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return n


def iso(d):
    return d.isoformat() if d else ""


REG_COLS = ["record_id", "vin", "plate", "county_no", "record_status", "status_date", "model_year", "make", "model",
            "body_code", "gvwr_class", "fuel_code", "owner_type", "reg_expires", "title_issued"]


def registration_rows():
    T = F.build()
    rngs = {c: np.random.default_rng(W.SEED + 21 + W.CNO[c]) for c in W.NAMES}
    rows = []
    for v in T.itertuples(index=False):
        rng = rngs[v.county]
        base = [v.vin, v.plate, None, None, None, int(v.my), v.make, v.model, v.body, v.gvwr, v.fuel, v.owner]
        title = F.from_dec(max(v.first, 1994.0) if np.isnan(v.arrived) else v.arrived)
        if v.kind == "active" or (v.kind == "pilot" and v.reinstated):
            ren = F.from_dec(v.renewed)
            exp = dt.date(ren.year + 1, ren.month, min(ren.day, 28))
            if v.kind == "pilot":
                ren = v.surrendered + dt.timedelta(days=int(rng.integers(20, 160)))
                exp = dt.date(ren.year + 1, ren.month, min(ren.day, 28))
            rows.append((v.county, "ACTIVE", ren, base, exp, title))
            if isinstance(v.moved_from, str):
                mo = F.from_dec(v.moved_on)
                rows.append((v.moved_from, "TRANSFERRED", mo, base, dt.date(mo.year + 1, mo.month, min(mo.day, 28)), title))
        elif v.kind == "departed":
            lf = F.from_dec(v.left)
            if v.left_how == "CANCELLED":
                rows.append((v.county, "CANCELLED", lf, base, dt.date(lf.year, 12, 28) if lf.month > 6 else
                             dt.date(lf.year, 6, 28), title))
            else:
                rows.append((v.county, "EXPIRED", lf, base, lf, title))
        else:
            c = v.surrendered + dt.timedelta(days=int(rng.integers(6, 30)))
            rows.append((v.county, "CANCELLED", c, base, dt.date(2026, 3, 31) if c.month > 3 else dt.date(2025, 9, 30), title))
            if isinstance(v.moved_from, str):
                mo = F.from_dec(v.moved_on)
                rows.append((v.moved_from, "TRANSFERRED", mo, base, dt.date(mo.year + 1, mo.month, min(mo.day, 28)), title))
    rng = np.random.default_rng(W.SEED + 22)
    order = rng.permutation(len(rows))
    out = []
    for k, i in enumerate(order):
        county, status, sd, base, exp, title = rows[i]
        r = list(base)
        out.append(["VR%08d" % (31000000 + k * 7 + int(rng.integers(0, 7)))] + r[:2] + ["%02d" % W.CNO[county], status,
                    iso(sd)] + r[5:] + [iso(exp), iso(title)])
    out.sort(key=lambda r: (r[3], r[0]))
    return out


TEST_COLS = ["test_id", "station_no", "lane", "inspector_id", "test_start", "test_type", "vin", "vin_source", "plate",
             "model_year", "make", "odometer", "odometer_unit", "obd_mil", "dtc_count", "readiness", "result"]


def _inspectors():
    reg = S.register()
    rng = np.random.default_rng(W.SEED + 33)
    out = {}
    for x in reg.s:
        out[(x["no"], x["gen"])] = ["IN%04d" % int(rng.integers(1000, 9999)) for _ in range(int(rng.integers(2, 6)))]
    return out


def test_rows():
    T = F.build()
    reg = S.register()
    insp = _inspectors()
    rngs = {c: np.random.default_rng(W.SEED + 31 + W.CNO[c]) for c in W.NAMES}
    acc_rate = lambda age: max(W.ACC_NEW + W.ACC_SLOPE * age, W.ACC_FLOOR)
    rows = []
    for v in T[T["tested"]].itertuples(index=False):
        rng = rngs[v.county]
        d = v.test_date
        age = F.dec(d) - v.first
        st = int(v.station)
        holder = [x for x in reg.s if x["no"] == st and x["start"] <= d and (x["end"] is None or d <= x["end"])][0]
        ins = insp[(st, holder["gen"])]
        hh = int(rng.integers(7, 18))
        mm = int(rng.integers(0, 60))
        obd = v.my >= 2005 and rng.random() < 0.97
        slip = (not obd) and rng.random() < 0.045
        cap = V.mistype(rng, v.vin) if slip else v.vin
        unit = "KM" if rng.random() < 0.005 else "MI"
        odo = v.odo_true * (1.609344 if unit == "KM" else 1.0)
        reading = int(round(odo))
        if rng.random() < 0.0035:
            reading = int(rng.choice([0, 999999]))
        old = (2026 - v.my)
        fail = rng.random() < (0.02 + 0.006 * max(old - 5, 0))
        mil = "ON" if fail and rng.random() < 0.8 else "OFF"
        ready = "INC" if (fail and mil == "OFF") else "OK"
        dtc = int(rng.integers(1, 5)) if mil == "ON" else 0
        base = dict(station=st, lane=int(v.lane), insp=ins[int(rng.integers(0, len(ins)))], vin=cap,
                    src="OBD" if obd else "KEYED", plate=v.plate if slip else v.plate_test, my=int(v.my), make=v.make)
        t0 = dt.datetime(d.year, d.month, d.day, hh, mm)
        if rng.random() < 0.012:
            rows.append((t0 - dt.timedelta(minutes=int(rng.integers(8, 70))), "INITIAL", base, None, None, "OFF", 0, "OK",
                         "ABORT"))
        rows.append((t0, "INITIAL", base, reading, unit, mil, dtc, ready, "FAIL" if fail else "PASS"))
        if fail and rng.random() < 0.86:
            gap = int(rng.integers(2, 41))
            d2 = d + dt.timedelta(days=gap)
            if d2 <= W.CYCLE_END:
                more = v.k * acc_rate(age) * gap / 365.25
                r2 = int(round((v.odo_true + more) * (1.609344 if unit == "KM" else 1.0)))
                t2 = dt.datetime(d2.year, d2.month, d2.day, int(rng.integers(7, 18)), int(rng.integers(0, 60)))
                b2 = dict(base)
                b2["insp"] = ins[int(rng.integers(0, len(ins)))]
                rows.append((t2, "RETEST", b2, r2, unit, "OFF", 0, "OK", "PASS" if rng.random() < 0.93 else "FAIL"))
    rows.sort(key=lambda r: (r[0], r[2]["station"]))
    out = []
    seq = {2024: 0, 2025: 0}
    for t, typ, b, odo, unit, mil, dtc, ready, res in rows:
        seq[t.year] += 1
        out.append(["%d%07d" % (t.year, seq[t.year] * 3 + 11), b["station"], b["lane"], b["insp"], t.strftime("%Y-%m-%d %H:%M"),
                    typ, b["vin"], b["src"], b["plate"], b["my"], b["make"], odo, unit if odo is not None else None, mil,
                    dtc, ready, res])
    out.sort(key=lambda r: (r[4], r[0]))
    return out


COUNTY_COLS = ["county_no", "county", "fips_county", "county_seat", "in_nonattainment_area"]


def county_rows():
    return [["%02d" % no, name, fips, towns[0], "Y"] for name, no, fips, towns in sorted(W.COUNTIES, key=lambda c: c[1])]


BODY_COLS = ["body_code", "description", "program_class"]
BODY = [("2D", "Coupe, two door", "PC"), ("4D", "Sedan, four door", "PC"), ("HB", "Hatchback", "PC"),
        ("SW", "Station wagon", "PC"), ("CV", "Convertible", "PC"), ("UT", "Utility vehicle", "LT"),
        ("PK", "Pickup", "LT"), ("VN", "Van", "LT"), ("MV", "Minivan", "LT")]


def body_rows():
    return [list(b) for b in BODY]


VMT_COLS = ["county_no", "county", "functional_class", "centerline_miles", "annual_vmt_millions"]
FCLASS = [("Interstate", 0.22), ("Other freeway and expressway", 0.10), ("Principal arterial", 0.21),
          ("Minor arterial", 0.17), ("Major and minor collector", 0.16), ("Local", 0.14)]


def vmt_rows():
    rng = np.random.default_rng(W.SEED + 51)
    out = []
    for name, no, fips, towns in sorted(W.COUNTIES, key=lambda c: c[1]):
        n, shift, kc = W.FLEET[name]
        through = 1.0 + (0.55 if name in ("Halvering", "Dunmarsh", "Quarrybrook", "Marlbank") else 0.15)
        total = n * 1.12 * 10200 * kc * through * float(rng.uniform(0.93, 1.07)) / 1e6
        for fc, share in FCLASS:
            s = share * float(rng.uniform(0.8, 1.2))
            if fc.startswith("Interstate") and through < 1.3:
                s *= 0.35
            miles = (s * total * 1e6 / 365) / {"Interstate": 31000, "Other freeway and expressway": 18000,
                                               "Principal arterial": 9500, "Minor arterial": 5200,
                                               "Major and minor collector": 1600, "Local": 260}[fc]
            out.append(["%02d" % no, name, fc, "%.1f" % miles, "%.1f" % (s * total)])
    return out


FUEL_COLS = ["county_no", "county", "month", "taxable_gallons"]


def fuel_rows():
    rng = np.random.default_rng(W.SEED + 53)
    season = [0.92, 0.88, 0.98, 1.0, 1.05, 1.08, 1.12, 1.10, 1.01, 1.0, 0.94, 0.92]
    out = []
    for name, no, fips, towns in sorted(W.COUNTIES, key=lambda c: c[1]):
        n, shift, kc = W.FLEET[name]
        yearly = n * 470 * kc * float(rng.uniform(0.9, 1.15))
        for m in range(12):
            out.append(["%02d" % no, name, "2025-%02d" % (m + 1), int(round(yearly / 12 * season[m] * rng.uniform(0.97, 1.03)))])
    return out


POP_COLS = ["county_no", "county", "population_2020_census", "population_2025_estimate", "households_2025"]


def pop_rows():
    rng = np.random.default_rng(W.SEED + 57)
    out = []
    for name, no, fips, towns in sorted(W.COUNTIES, key=lambda c: c[1]):
        n, shift, kc = W.FLEET[name]
        p25 = int(n / 0.86 * float(rng.uniform(0.95, 1.05)))
        p20 = int(p25 / (1 + float(rng.normal(0.018, 0.02))))
        out.append(["%02d" % no, name, p20, p25, int(p25 / float(rng.uniform(2.35, 2.65)))])
    return out
