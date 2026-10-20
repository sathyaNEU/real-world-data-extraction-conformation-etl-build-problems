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
GATE_COLS = ["transaction_id", "terminal", "truck_tag", "in_lane", "gate_in", "out_lane", "gate_out", "move_type",
             "container_no"]
FLEET_COLS = ["truck_id", "tag_number", "tag_effective", "tag_expires", "engine_model_year", "motor_carrier"]
COMPLAINT_COLS = ["request_id", "received", "street", "cross_street", "category", "status"]
NO2_COLS = ["aqs_site_id", "date_local", "hour_local", "no2_ppb", "qualifier"]

# each link's site id in its count programme's numbering
SITE = {"L01": "CTY-117", "L02": "HC-0412", "L03": "HC-0407", "L04": "MTD-B20-03", "L05": "HC-0398",
        "L06": "MTD-B30-01", "L07": "CTY-142", "L08": "HC-0408", "L09": "CTY-158", "L10": "MTD-RY-02",
        "L11": "CTY-163", "L12": "HC-0421", "L13": "MTD-RY-05", "L14": "CTY-171"}
DIRS = {"freeway": ("NB", "SB"), "arterial": ("EB", "WB")}


@functools.lru_cache(None)
def everything():
    x = S.world(np.random.default_rng(W.SEED))
    g = S.gate_world(np.random.default_rng(W.GATE_SEED))
    return dict(x=x, g=g, st=R.stations(np.random.default_rng(W.SEED + 1), x),
                cnt=R.counts(np.random.default_rng(W.SEED + 2), x),
                gates=R.gates(np.random.default_rng(W.SEED + 3), g))


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
    f = "%Y-%m-%d %H:%M:%S"
    return [[t, term, tag, il, a.strftime(f), ol, b.strftime(f), mv, cn] for t, term, tag, il, a, ol, b, mv, cn in e["gates"]]


def fleet_rows(e):
    rng = np.random.default_rng(W.SEED + 8)
    carriers = ["Harborline Drayage", "Tri-County Cartage", "Seaboard Intermodal", "Coastal Haul LLC", "Bay Freight Co",
                "Northpoint Logistics", "Rivera Trucking", "Atlantic Port Services"]
    my = {t["truck"]: t["model_year"] for t in e["g"]["trucks"]}
    car = {t: carriers[int(rng.integers(0, len(carriers)))] for t in sorted(my)}
    rows = []
    for tag, truck, a, b in e["g"]["tags"]:
        rows.append([truck, tag, a.isoformat(), "" if b == W.DAYS[-1] else b.isoformat(), my[truck], car[truck]])
    rows.sort(key=lambda r: (r[0], r[2]))
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
