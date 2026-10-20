"""The pack's data files, cut from the truth."""
import csv
import datetime as dt
import functools

import numpy as np

import records as R
import sources as S
import world as W

STATION_COLS = ["station_id", "date", "hour_ending", "direction", "vehicle_class", "volume"]
DOT_COLS = ["site_id", "count_date", "hour", "direction", "class_1_3", "class_4_7", "class_8_13"]
CONS_COLS = ["site_code", "interval_start", "lane", "class_code", "volume"]
GATE_COLS = ["report_date", "terminal", "trucks_in", "trucks_out", "container_moves"]
FLEET_COLS = ["registration_id", "truck_id", "vin", "motor_carrier", "registered_from", "registered_to",
              "engine_family", "model_year"]
COMPLAINT_COLS = ["request_id", "received", "street", "cross_street", "category", "status"]
NO2_COLS = ["aqs_site_id", "date_local", "hour_local", "no2_ppb", "qualifier"]

# each link's site id in its count programme's numbering
SITE = {"L01": "CTY-117", "L02": "HC-0412", "L03": "HC-0407", "L04": "MTD-B20-03", "L05": "HC-0398",
        "L06": "MTD-B30-01", "L07": "CTY-142", "L08": "HC-0408", "L09": "CTY-158", "L10": "MTD-RY-02",
        "L11": "CTY-163", "L12": "HC-0421", "L13": "MTD-RY-05", "L14": "CTY-171"}
DIRS = {"freeway": ("NB", "SB"), "arterial": ("EB", "WB")}


@functools.lru_cache(None)
def everything():
    x = S.world(np.random.default_rng(W.SEED), np.random.default_rng(W.GATE_SEED))
    reg = S.registry(np.random.default_rng(W.SEED + 60))
    return dict(x=x, reg=reg, st=R.stations(np.random.default_rng(W.SEED + 1), x),
                cnt=R.counts(np.random.default_rng(W.SEED + 2), x),
                gates=R.gate_report(np.random.default_rng(W.SEED + 3), x["gates"]))


def station_rows(e):
    return [[s, d.isoformat(), h, di, c, v] for s, d, h, di, c, v in e["st"]]


def dot_rows(e):
    rows = []
    for k in sorted(W.LINKS):
        if W.PROGRAM[k] != "dot":
            continue
        d0 = W.COUNT_DAY[k]
        dirs = DIRS[W.LINKS[k][1]]
        for h in range(48):
            d = d0 + dt.timedelta(h // 24)
            for j, dn in enumerate(dirs):
                rows.append([SITE[k], d.isoformat(), "%02d:00" % (h % 24), dn] +
                            [int(e["cnt"][k][c][j][h]) for c in W.CLASSES])
    return rows


def consultant_rows(e):
    rng = np.random.default_rng(W.SEED + 5)
    rows = []
    for k in sorted(W.LINKS):
        if W.PROGRAM[k] != "consultant":
            continue
        d0 = W.COUNT_DAY[k]
        for h in range(48):
            d = d0 + dt.timedelta(h // 24)
            off = "-04:00" if R.us_eastern_dst(d) else "-05:00"
            ts = "%sT%02d:00:00%s" % (d.isoformat(), h % 24, off)
            for j in range(2):
                for c in W.CLASSES:
                    v = int(e["cnt"][k][c][j][h])
                    a = int(rng.binomial(v, .58)) if v else 0
                    for lane, val in ((2 * j + 1, a), (2 * j + 2, v - a)):
                        rows.append([SITE[k], ts, lane, c, val])
    return rows


def county_tables(e):
    """{link: (site, [(date, 'HH:MM', [6 values])])}: 15-minute rows, the two directions side by side."""
    rng = np.random.default_rng(W.SEED + 6)
    out = {}
    for k in sorted(W.LINKS):
        if W.PROGRAM[k] != "county":
            continue
        d0 = W.COUNT_DAY[k]
        rows = []
        for h in range(48):
            d = d0 + dt.timedelta(h // 24)
            q = np.zeros((4, 6), int)
            for j in range(2):
                for ci, c in enumerate(W.CLASSES):
                    q[:, 3 * j + ci] = rng.multinomial(int(e["cnt"][k][c][j][h]), [.25] * 4)
            for m in range(4):
                rows.append((d, "%02d:%02d" % (h % 24, 15 * m), [int(v) for v in q[m]]))
        out[k] = (SITE[k], rows)
    return out


def gate_rows(e):
    return [[d.isoformat(), t, a, b, m] for d, t, a, b, m in sorted(e["gates"], key=lambda r: (r[0], r[1]))]


def fleet_rows(e):
    rng = np.random.default_rng(W.SEED + 8)
    rows = []
    n = 5100
    for g in sorted(e["reg"]["regs"], key=lambda g: (g["start"], g["truck"])):
        n += int(rng.integers(1, 6))
        rows.append(["R%06d" % n, "DT%06d" % g["truck"], g["vin"], g["car"], g["start"].isoformat(),
                     g["end"].isoformat() if g["end"] else "", g["fam"], "" if g["legacy"] else g["vy"]])
    return rows


def cert_rows(e):
    rng = np.random.default_rng(W.SEED + 13)
    makers = {"A": "Allison-Cummins", "B": "Brightline Diesel", "C": "Cummins Inc.", "D": "Detroit Diesel Corp.",
              "H": "Hino Motors", "M": "Mack Trucks", "N": "Navistar Inc.", "P": "PACCAR Inc.", "V": "Volvo Powertrain",
              "W": "Westport Fuel Systems"}
    rows = []
    for code, my in sorted(e["reg"]["fams"].items()):
        std = 0.20 if my >= 2010 else (1.2 if my >= 2007 else 2.0)
        rows.append([code, makers[code[1]], my, float(code[5:9]), std, "EPA" if rng.random() < .7 else "EPA, CARB"])
    return rows


def no2_rows(e):
    rng = np.random.default_rng(W.SEED + 9)
    rows = []
    for site, base in (("34-017-0011", 21.0), ("34-017-0024", 15.5)):
        for d in W.DAYS:
            for h in range(24):
                v = base * (1.25 if d.month in (11, 12, 1, 2) else .9) * (1.4 if h in (6, 7, 8, 17, 18) else 1.0) * \
                    float(rng.lognormal(0, .45))
                q = ""
                if rng.random() < .012:
                    rows.append([site, d.isoformat(), h, "", "AN"])
                    continue
                rows.append([site, d.isoformat(), h, "%.1f" % v, q])
    return rows


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)


def complaint_rows(e):
    rng = np.random.default_rng(W.SEED + 12)
    streets = ["Terminal Way", "Harbor Boulevard", "Port Avenue", "Cargo Drive", "7th Street", "Delmar Road",
               "Ridley Avenue", "Quarry Road", "Selby Street", "Pell Road", "Mill Street", "12th Street"]
    cats = ["Truck idling", "Truck parking", "Truck noise", "Dust or debris", "Truck route violation"]
    rows = []
    n = 2610000
    for d in W.DAYS:
        for _ in range(int(rng.poisson(3.1))):
            n += int(rng.integers(1, 40))
            s = streets[int(rng.integers(0, len(streets)))]
            c = streets[int(rng.integers(0, len(streets)))]
            rows.append(["SR-%d" % n, "%s %02d:%02d" % (d.isoformat(), int(rng.integers(6, 23)), int(rng.integers(0, 60))),
                         s, c if c != s else "", cats[int(rng.choice(5, p=[.34, .27, .18, .12, .09]))],
                         "Closed" if rng.random() < .86 else "Open"])
    return rows
