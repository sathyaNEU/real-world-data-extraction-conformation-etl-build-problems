"""Writes target/ from the world: the exports as the producing systems write them, and the documents."""
import datetime as dt
import math
import os

import numpy as np

import common as C
import docs
import world as WD

CENTRE = (389850.0, 279400.0)          # British National Grid, the town centre


def layout(W):
    """Positions in metres: junctions, then each counted section's ends and count point."""
    rng = np.random.default_rng([WD.SEED, 101])
    pos = {}
    for j in W.junctions:
        while True:
            p = (rng.uniform(-2300, 2300), rng.uniform(-1700, 1700))
            if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 380 for q in pos.values()):
                pos[j["id"]] = p
                break
    W.jpos = pos
    W.cp = {}
    for s in W.sections:
        L = s["length"] * 1000.0
        ang = rng.uniform(0, 2 * math.pi)
        if s["end_j"]:
            a = pos[s["end_j"]]
        elif s["setting"] == "rural":
            r = rng.uniform(3400, 4600)
            a = (r * math.cos(ang), r * math.sin(ang))
        else:
            while True:
                a = (rng.uniform(-2600, 2600), rng.uniform(-1900, 1900))
                if all(math.hypot(a[0] - q[0], a[1] - q[1]) > 300 for q in pos.values()):
                    break
        b = (a[0] + L * math.cos(ang), a[1] + L * math.sin(ang))
        f = rng.uniform(0.38, 0.62)
        m = (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]))
        W.cp[s["name"]] = (int(round(CENTRE[0] + m[0])), int(round(CENTRE[1] + m[1])))


def ids(W):
    rng = np.random.default_rng([WD.SEED, 103])
    used = set()
    W.cp_id = {}
    for s in W.sections:
        while True:
            v = int(rng.integers(300000, 990000))
            if v not in used:
                used.add(v)
                W.cp_id[s["name"]] = v
                break
    W.atc_id = {}
    for a in W.atcs:
        while True:
            v = "WRA%03d" % int(rng.integers(101, 899))
            if v not in used:
                used.add(v)
                W.atc_id[a["name"]] = v
                break
    for c in W.detectors:
        c["id"] = "WRN%s/%02d" % (W.refs[c["junction"]], c["channel"])
        if "old_channel" in c:
            c["old_id"] = "WRN%s/%02d" % (W.refs[c["junction"]], c["old_channel"])


# Older count points in the register that were not counted in 2025 (last counted 2021 to 2024).
OTHER_POINTS = [("Canal Street", "C", "Wharf Street", "Birmingham Road", 0.55, 2023), ("Rowley Street", "U", "Oakhill Road", "Northgate Road", 0.43, 2022),
                ("Lea Road", "B", "Western Avenue", "Castlegate Road", 1.12, 2024), ("Mill Street", "U", "Lichgate Road", "Heath End", 0.61, 2021),
                ("Tanyard Lane", "C", "Ring Road", "Hollins Lane", 0.92, 2023), ("Birch Street", "U", "Sandy Lane", "Station Street", 0.38, 2024),
                ("Weston Road", "C", "Ashby Road", "Weston", 1.64, 2022), ("Pelham Lane", "C", "Holloway Hill", "Pelham", 2.05, 2021),
                ("Northgate Road", "B", "Station Street", "Ring Road", 0.84, 2024), ("Market Way", "C", "Ring Road", "Station Street", 0.47, 2023),
                ("Heath End", "U", "Lower Heath Road", "Stafford Road", 1.21, 2022), ("Ashby Road", "B", "Birmingham Road", "Weston Road", 0.97, 2024)]


ABBREV = {"Avenue": "Ave", "Road": "Rd", "Street": "St", "Lane": "La", "Way": "Wy", "Hill": "Hl"}


def utc_name(road, rng):
    """The UTC asset register abbreviates street types on most records."""
    parts = road.split(" ")
    if parts[-1] in ABBREV and rng.random() < 0.8:
        parts[-1] = ABBREV[parts[-1]]
    return " ".join(parts)


def write_pack(W, out):
    os.makedirs(out, exist_ok=True)
    layout(W)
    ids(W)
    rng = np.random.default_rng([WD.SEED, 107])
    days = WD.DAYS

    # 1. UTC detector daily summary (the bulk file). The export was pulled in two half-year parts.
    det_rows = []
    for c in sorted(W.detectors, key=lambda c: (c["junction"], c["channel"])):
        pass
    by_id = {}
    for c in W.detectors:
        jsw = WD.REFURBISHED.get(c["junction"])
        for i, d in enumerate(days):
            if jsw is not None and d < jsw:
                did = c["old_id"]
            else:
                did = c["id"]
            av = int(c["avail"][i])
            f12 = None if av == 0 else int(c["obs12"][i])
            f24 = None if av == 0 else int(c["obs24"][i])
            by_id.setdefault(did, []).append((d, f12, f24, av))
    header = ["detector", "date", "flow_0700_1900", "flow_0000_2400", "availability_pct"]
    rows_h1, rows_h2 = [], []
    for did in sorted(by_id):
        for d, f12, f24, av in sorted(by_id[did]):
            r = [did, d.strftime("%d/%m/%Y"), f12, f24, av]
            (rows_h1 if d.month <= 6 else rows_h2).append(r)
    path = os.path.join(out, "utc_detector_daily_2025.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        import csv
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows_h1:
            w.writerow(["" if v is None else v for v in r])
        w.writerow(header)
        for r in rows_h2:
            w.writerow(["" if v is None else v for v in r])
    W.n_detector_rows = len(rows_h1) + len(rows_h2)

    # 2. UTC asset register
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Junctions"
    ws.append(["junction_ref", "junction", "control", "latitude", "longitude", "controller_installed", "record_updated"])
    jrng = np.random.default_rng([WD.SEED, 109])
    for j in sorted(W.junctions, key=lambda j: W.refs[j["id"]]):
        x, y = W.jpos[j["id"]]
        lat, lon = C.bng_to_wgs84(CENTRE[0] + x, CENTRE[1] + y)
        if j["id"] in WD.REFURBISHED:
            inst = WD.REFURBISHED[j["id"]]
        else:
            inst = dt.date(int(jrng.integers(2009, 2023)), int(jrng.integers(1, 13)), int(jrng.integers(1, 28)))
        upd = max(inst, dt.date(2025, int(jrng.integers(1, 12)), int(jrng.integers(1, 28))))
        name = " / ".join(utc_name(p, jrng) for p in j["name"].split(" / "))
        ws.append(["WRN" + W.refs[j["id"]], name, j["control"], round(lat, 6), round(lon, 6), inst, upd])
    ws2 = wb.create_sheet("Detectors")
    ws2.append(["detector", "junction_ref", "channel", "arm", "approach", "heading", "lane", "loop_type", "position", "commissioned"])
    for c in sorted(W.detectors, key=lambda c: c["id"]):
        jsw = WD.REFURBISHED.get(c["junction"])
        if jsw is not None:
            com = jsw
        else:
            com = dt.date(int(jrng.integers(2009, 2024)), int(jrng.integers(1, 13)), int(jrng.integers(1, 28)))
        ws2.append([c["id"], "WRN" + W.refs[c["junction"]], c["channel"], c["arm"], utc_name(c["road"], jrng), c["heading"],
                    c["lane"], "inductive loop", "stop line", com])
    for wsx in (ws, ws2):
        for row in wsx.iter_rows(min_row=2):
            for cell in row:
                if isinstance(cell.value, dt.date):
                    cell.number_format = "dd/mm/yyyy"
    C.save_workbook(wb, os.path.join(out, "utc_asset_register_2025.xlsx"), dt.datetime(2026, 1, 12, 10, 4), "Melanie Watts")

    # 3. permanent counter daily export and site list
    atc_rows = []
    for a in sorted(W.atcs, key=lambda a: W.atc_id[a["name"]]):
        sid = W.atc_id[a["name"]]
        for i, d in enumerate(days):
            if np.isnan(a["obs24"][i]):
                continue
            atc_rows.append([sid, d.isoformat(), int(a["obs12"][i]), int(a["obs24"][i])] + [int(v) for v in a["channels"][i]])
    C.write_csv(os.path.join(out, "atc_daily_2025.csv"),
                ["site_id", "date", "mv_0700_1900", "mv_0000_2400"] + ["class_%d" % k for k in range(1, 9)], atc_rows)
    srng = np.random.default_rng([WD.SEED, 113])
    site_rows = []
    for a in sorted(W.atcs, key=lambda a: W.atc_id[a["name"]]):
        r = srng.uniform(1200, 3600) if a["setting"] == "urban" else srng.uniform(3900, 5600)
        ang = srng.uniform(0, 2 * math.pi)
        site_rows.append([W.atc_id[a["name"]], "%s %s" % (a["name"], ["north", "south", "east", "west"][int(srng.integers(0, 4))]),
                          a["name"], a["road_class"], a["setting"], int(CENTRE[0] + r * math.cos(ang)), int(CENTRE[1] + r * math.sin(ang)),
                          "TX-200", a["installed"].isoformat(), "TX-8", 2 if a["road_class"] != "C" else 2])
    C.write_csv(os.path.join(out, "atc_sites_2025.csv"),
                ["site_id", "site_name", "road", "road_class", "setting", "easting", "northing", "equipment", "installed", "class_scheme", "lanes"],
                site_rows)
    C.write_csv(os.path.join(out, "classifier_schemes.csv"),
                ["scheme", "equipment", "class", "description", "group"],
                [["ARD-8", "Ardent LC4", 1, "two-wheeled motor vehicle", "motorcycle"],
                 ["ARD-8", "Ardent LC4", 2, "car or taxi, two axles", "car"],
                 ["ARD-8", "Ardent LC4", 3, "car or light van towing", "car"],
                 ["ARD-8", "Ardent LC4", 4, "light goods vehicle, up to 3.5 t", "lgv"],
                 ["ARD-8", "Ardent LC4", 5, "rigid goods vehicle, two axles", "hgv"],
                 ["ARD-8", "Ardent LC4", 6, "rigid goods vehicle, three or more axles", "hgv"],
                 ["ARD-8", "Ardent LC4", 7, "articulated goods vehicle", "hgv"],
                 ["ARD-8", "Ardent LC4", 8, "bus or coach", "bus"],
                 ["TX-8", "TX-200", 1, "two-wheeled motor vehicle", "motorcycle"],
                 ["TX-8", "TX-200", 2, "vehicle up to 5.2 m", "car"],
                 ["TX-8", "TX-200", 3, "vehicle 5.2 m to 6.6 m, two axles", "lgv"],
                 ["TX-8", "TX-200", 4, "vehicle towing, up to 3.5 t", "car"],
                 ["TX-8", "TX-200", 5, "bus or coach", "bus"],
                 ["TX-8", "TX-200", 6, "rigid goods vehicle, two axles, over 6.6 m", "hgv"],
                 ["TX-8", "TX-200", 7, "rigid or articulated goods vehicle, three or four axles", "hgv"],
                 ["TX-8", "TX-200", 8, "articulated goods vehicle, five or more axles", "hgv"]])

    # 4. manual classified counts
    mc_rows = []
    heads = {}
    for s in W.sections:
        hd = WD.section_heading(s["name"]) if s["end_j"] else ["NB", "EB"][int(rng.integers(0, 2))]
        pair = {"NB": ("N", "S"), "SB": ("S", "N"), "EB": ("E", "W"), "WB": ("W", "E")}[hd]
        heads[s["name"]] = pair
        d = W.count_day[s["name"]]
        for direction, hour, cyc, v in s["count_rows"]:
            mc, car, bus, lgv = int(v[0]), int(v[1]), int(v[2]), int(v[3])
            h = [int(x) for x in v[4:]]
            mc_rows.append([W.cp_id[s["name"]], d.isoformat(), pair[direction], hour, cyc, mc, car, bus, lgv] + h + [sum(h), int(v.sum())])
    mc_rows.sort(key=lambda r: (r[1], r[0], r[2], r[3]))
    C.write_csv(os.path.join(out, "manual_counts_2025.csv"),
                ["count_point_id", "count_date", "direction_of_travel", "hour", "pedal_cycles", "two_wheeled_motor_vehicles",
                 "cars_and_taxis", "buses_and_coaches", "lgvs", "hgvs_2_rigid_axle", "hgvs_3_rigid_axle",
                 "hgvs_4_or_more_rigid_axle", "hgvs_3_or_4_articulated_axle", "hgvs_5_articulated_axle",
                 "hgvs_6_articulated_axle", "all_hgvs", "all_motor_vehicles"], mc_rows)

    # 5. count point register
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Count points"
    ws.append(["count_point_id", "road_name", "road_class", "start_junction_road_name", "end_junction_road_name",
               "easting", "northing", "link_length_km", "setting", "last_counted"])
    reg = []
    for s in W.sections:
        e, n = W.cp[s["name"]]
        if s["end_j"] and rng.random() < 0.5:
            a, b = s["from"], s["to"]
        else:
            a, b = (s["to"], s["from"]) if rng.random() < 0.5 else (s["from"], s["to"])
        reg.append([W.cp_id[s["name"]], s["name"], s["road_class"], a, b, e, n, s["length"], s["setting"], 2025])
    prng = np.random.default_rng([WD.SEED, 127])
    used = set(W.cp_id.values())
    for road, cls, a, b, L, yr in OTHER_POINTS:
        while True:
            v = int(prng.integers(300000, 990000))
            if v not in used:
                used.add(v)
                break
        reg.append([v, road, cls, a, b, int(CENTRE[0] + prng.uniform(-2600, 2600)), int(CENTRE[1] + prng.uniform(-1900, 1900)),
                    L, "rural" if road in ("Weston Road", "Pelham Lane", "Heath End") else "urban", yr])
    reg.sort(key=lambda r: r[1])
    for r in reg:
        ws.append(r)
    C.save_workbook(wb, os.path.join(out, "count_points_2025.xlsx"), dt.datetime(2026, 1, 15, 14, 22), "Melanie Watts")

    # 6. documents and side files
    docs.write_docs(W, out)
    W.heads = heads
