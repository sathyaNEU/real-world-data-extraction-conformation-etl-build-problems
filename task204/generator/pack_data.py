"""Write the data files of target/ from the world (CSV, XLSX, GTFS, GeoJSON)."""
import csv
import datetime as dt
import io
import json
import os
import zipfile

import numpy as np
import openpyxl

import params as P
import world_net as N
import world_events as E
import world_other as O

FIXED_ZIP_TIME = (2026, 5, 11, 9, 0, 0)

POLICE_STN = {"WG": "WESTGATE LRT STN", "CS": "CENTRE SQ LRT STN", "UY": "UNION YARDS LRT STN",
              "MB": "MILLBROOK LRT STN", "FG": "FAIRGROUNDS LRT STN", "CB": "COBB ST LRT STN",
              "AR": "ASHFORD RD LRT STN", "RV": "RIDGEVIEW LRT STN", "PG": "PRAIRIE GATE LRT STN",
              "SH": "STATION HILL LRT STN", "KP": "KERR PARK LRT STN", "HL": "HOLLIN LRT STN",
              "LM": "LARCHMONT LRT STN"}
STREETS_NS = ["STREET", "ST", "ST"]
MO_DESC = {"SNATCH": "SNATCH", "STREET": "STREET-CONFRONT", "STREET-WEAPON": "STREET-WEAPON", "PICKPOCKET": "STEALTH"}


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def normalise_zip(path):
    """Rewrite an Office file with fixed entry times and order so rebuilds are byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def fmt(t):
    return t.strftime("%Y-%m-%d %H:%M")


def block_address(rng, x, y):
    av = int((y - 5926000) / 100) + 1
    st = int((x - 318000) / 100) + 1
    quad = ("N" if y > 5935000 else "S") + ("E" if x > 330000 else "W")
    if rng.random() < 0.5:
        return "%d00 BLK %d ST %s" % (max(1, av % 140), max(1, st % 180), quad)
    return "%d00 BLK %d AV %s" % (max(1, st % 180), max(1, av % 140), quad)


def rms_rows(world):
    """The RMS extract: every phone offence that reached the police plus every other occurrence."""
    rng = np.random.default_rng(P.SEED + 101)
    recs = []
    for e in world.ev.events:
        if not e["in_rms"]:
            continue
        lag = int(rng.integers(6, 48)) if e["mo"] != "PICKPOCKET" else int(rng.integers(20, 300))
        prop = "CELL PHONE" if rng.random() < 0.82 else ("CELL PHONE; WALLET" if rng.random() < 0.6 else "CELL PHONE; EARBUDS")
        recs.append({"t_rep": e["t_occ"] + dt.timedelta(minutes=lag), "t_from": e["t_occ"], "t_to": e["t_occ"],
                     "offence": e["offence"], "loc": e["loc"], "station": e["station"], "x": e["x"], "y": e["y"],
                     "mo": MO_DESC[e["mo"]], "sus": e["suspects"], "alo": e["age_low"], "ahi": e["age_high"],
                     "sex": e["sex"], "weapon": e["weapon"], "prop": prop,
                     "value": int(rng.integers(26, 165)) * 10, "phone": True, "ev": e})
    for o in world.other:
        span = 0 if o["offence"] in ("ROB-PERS", "THFT-PERS", "ASLT-1", "ASLT-2", "DIST", "ROB-COM", "DRUG-POSS",
                                     "TRAF-CRIM", "UTTER") else int(rng.integers(0, 14 * 60))
        lag = int(rng.integers(10, 3 * 24 * 60)) if span else int(rng.integers(8, 180))
        val = "" if o["property"] == "NONE" else str(int(rng.integers(3, 300)) * 10)
        recs.append({"t_rep": o["t_occ"] + dt.timedelta(minutes=span + lag), "t_from": o["t_occ"],
                     "t_to": o["t_occ"] + dt.timedelta(minutes=span), "offence": o["offence"], "loc": o["loc"],
                     "station": o["station"], "x": o["x"], "y": o["y"], "mo": "", "sus": o["suspects"],
                     "alo": "", "ahi": "", "sex": "", "weapon": o["weapon"], "prop": o["property"], "value": val,
                     "phone": False, "ev": None})
    recs.sort(key=lambda r: (r["t_rep"], r["x"]))
    out = []
    index = {}
    seq = {2025: 10417, 2026: 9862}
    for r in recs:
        yr = r["t_rep"].year
        seq[yr] += int(rng.integers(1, 6))
        occ = "CP%02d-%06d" % (yr % 100, seq[yr])
        if r["ev"] is not None:
            index[id(r["ev"])] = occ
        layout = P.D25 if r["t_from"].year == 2025 else P.D26
        dist = N.district_of(r["x"], r["y"], layout)
        if r["station"]:
            loc_txt = POLICE_STN[r["station"]]
            if r["loc"] == "LRT TRAIN":
                loc_txt = loc_txt + " (ON TRAIN)"
        else:
            loc_txt = block_address(rng, r["x"], r["y"])
        sus = r["sus"] if r["sus"] else ""
        out.append([occ, fmt(r["t_rep"]), fmt(r["t_from"]), fmt(r["t_to"]), r["offence"], O.DESC[r["offence"]],
                    r["loc"], loc_txt, int(round(r["x"])), int(round(r["y"])), dist, r["mo"], sus,
                    r["alo"], r["ahi"], r["sex"], r["weapon"], r["prop"], r["value"],
                    "OPEN" if rng.random() < 0.83 else ("CLEARED-CHARGE" if rng.random() < 0.7 else "CLEARED-OTHER")])
    return out, index


RMS_HEADER = ["occurrence_no", "reported_local", "occurred_from_local", "occurred_to_local", "offence_code",
              "offence_desc", "location_type", "location_text", "x_utm12n", "y_utm12n", "patrol_district",
              "mo_code", "num_suspects", "suspect_age_from", "suspect_age_to", "suspect_sex", "weapon",
              "property_taken", "property_value_cad", "clearance_status"]


def station_code_on(st, d):
    """Carvale Transit's station code (the code of the station's main gate) in force on date d."""
    ent, before, after = P.GATES[st][0]
    return before if d < P.SPRING_CHANGE else after


TPO_CATS = [("FARE EVASION", 9.0), ("DISTURBANCE", 3.0), ("INTOXICATED PERSON", 2.6), ("TRESPASS", 1.4),
            ("ASSIST POLICE", 0.8), ("MEDICAL ASSIST", 1.1), ("SUSPICIOUS PERSON", 1.5), ("LOST PROPERTY", 1.2)]


def tpo_rows(world, rms_index):
    rng = np.random.default_rng(P.SEED + 202)
    recs = []
    for e in world.ev.events:
        if not e["tpo"]:
            continue
        k = e["tpo"]["kind"]
        cat = "THEFT FROM PERSON" if e["offence"] == "THFT-PERS" else "ROBBERY"
        loc = "ON TRAIN" if e["loc"] == "LRT TRAIN" else "PLATFORM"
        refd = "Y" if k in ("REF_NUM", "REF_BLANK") else "N"
        fileno = rms_index[id(e)] if k == "REF_NUM" else ""
        recs.append({"t": e["tpo"]["t_logged"], "st": e["station"], "loc": loc, "cat": cat, "prop": "CELL PHONE",
                     "sus": e["suspects"], "ref": refd, "file": fileno})
    stations = sorted(N.STN)
    w = np.array([c[1] for c in TPO_CATS])
    w = w / w.sum()
    for (a, b) in (P.X25, P.X26):
        for d in E.dates(a, b):
            for _ in range(int(rng.poisson(21.0))):
                st = stations[int(rng.integers(0, len(stations)))]
                if st == "FG" and d < P.SPRING_CHANGE:
                    st = "MB"
                cat = TPO_CATS[int(rng.choice(len(TPO_CATS), p=w))][0]
                t = dt.datetime(d.year, d.month, d.day, int(rng.integers(5, 24)), int(rng.integers(0, 60)))
                loc = ["PLATFORM", "ON TRAIN", "CONCOURSE", "PARK AND RIDE"][int(rng.choice(4, p=[0.5, 0.3, 0.15, 0.05]))]
                ref = "Y" if (cat in ("DISTURBANCE", "ASSIST POLICE") and rng.random() < 0.3) else "N"
                recs.append({"t": t, "st": st, "loc": loc, "cat": cat, "prop": "WALLET" if cat == "LOST PROPERTY" and rng.random() < 0.4 else "",
                             "sus": "" if cat in ("MEDICAL ASSIST", "LOST PROPERTY") else 1, "ref": ref, "file": ""})
    recs.sort(key=lambda r: (r["t"], r["st"]))
    out = []
    seq = {2025: 2210, 2026: 1987}
    badges = ["TPO %d" % b for b in rng.choice(np.arange(1104, 1199), size=26, replace=False)]
    for r in recs:
        yr = r["t"].year
        seq[yr] += int(rng.integers(1, 4))
        tu = E.to_utc(r["t"])
        out.append(["TPO-%d-%05d" % (yr, seq[yr]), tu.strftime("%Y-%m-%dT%H:%MZ"), station_code_on(r["st"], r["t"].date()),
                    r["loc"], r["cat"], r["prop"], r["sus"], r["ref"], r["file"], badges[int(rng.integers(0, len(badges)))]])
    return out


TPO_HEADER = ["TPO Log #", "Logged (UTC)", "Station Code", "Location", "Category", "Property", "Suspects",
              "Referred To Police", "CPS File #", "Officer"]


def write_tpo_xlsx(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Occurrences"
    ws.append(["Carvale Transit - Transit Peace Officer occurrence log, export 2026-05-11 09:40 MDT"])
    ws.append(TPO_HEADER)
    for r in rows:
        ws.append(r)
    ws.column_dimensions["B"].width = 19
    ws.column_dimensions["E"].width = 20
    wb.properties.creator = "Carvale Transit Security Operations"
    wb.properties.lastModifiedBy = "Carvale Transit Security Operations"
    wb.properties.created = dt.datetime(2026, 5, 11, 15, 40, 11)
    wb.properties.modified = dt.datetime(2026, 5, 11, 15, 40, 11)
    wb.save(path)
    normalise_zip(path)


def write_codes_xlsx(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stations"
    ws.append(["station_code", "station_name", "line", "effective_from", "effective_to"])
    rows = []
    for st in sorted(P.GATES):
        name = N.STN[st]["name"]
        line = "Eastline / Northline" if st == "CS" else ("Northline" if st in ("SH", "KP", "HL", "LM") else "Eastline")
        ent, before, after = P.GATES[st][0]
        if before == after:
            rows.append([before, name, line, "2008-04-27", ""])
        else:
            if before:
                rows.append([before, name, line, "2008-04-27", "2026-03-28"])
            rows.append([after, name, line, "2026-03-29", ""])
    rows.sort(key=lambda r: (r[0], r[3]))
    for r in rows:
        ws.append(r)
    ws2 = wb.create_sheet("Fare gates")
    ws2.append(["gate_code", "station_name", "entrance", "effective_from", "effective_to"])
    rows = []
    for st in sorted(P.GATES):
        for ent, before, after in P.GATES[st]:
            name = N.STN[st]["name"]
            if before == after:
                rows.append([before, name, ent, "2014-09-02", ""])
            else:
                if before:
                    rows.append([before, name, ent, "2014-09-02", "2026-03-28"])
                rows.append([after, name, ent, "2026-03-29", ""])
    rows.sort(key=lambda r: (r[0], r[3]))
    for r in rows:
        ws2.append(r)
    wb.properties.creator = "Carvale Transit Fare Systems"
    wb.properties.lastModifiedBy = "Carvale Transit Fare Systems"
    wb.properties.created = dt.datetime(2026, 3, 30, 16, 2, 40)
    wb.properties.modified = dt.datetime(2026, 3, 30, 16, 2, 40)
    wb.save(path)
    normalise_zip(path)


def entries_rows(world):
    out = []
    for (code, tu), n in sorted(world.entries.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        out.append([code, tu.strftime("%Y-%m-%dT%H:00Z"), n])
    return out


# ---- GTFS ---------------------------------------------------------------------------------------------
STOP_IDS = {}


def gtfs_files(world, folder):
    rng = np.random.default_rng(P.SEED + 303)
    os.makedirs(folder, exist_ok=True)
    trips = [t for t in world.trips if t["period"] in ("W26", "S26")]
    # platform stop ids: one per station and direction, opaque numbers
    ids = rng.choice(np.arange(2100, 2999), size=40, replace=False)
    k = 0
    stops = []
    for line, seq in (("EL", N.LINE_STOPS["EL"]), ("NL", N.LINE_STOPS["NL"])):
        for st in seq:
            for dirn in (0, 1):
                key = (line, st, dirn)
                if key in STOP_IDS:
                    continue
                STOP_IDS[key] = str(int(ids[k]))
                k += 1
    for (line, st, dirn), sid in sorted(STOP_IDS.items(), key=lambda kv: kv[1]):
        lat, lon = N.utm_to_latlon(N.STN[st]["x"] + (8 if dirn else -8), N.STN[st]["y"])
        plat = {("EL", 0): "Eastbound", ("EL", 1): "Westbound", ("NL", 0): "Northbound", ("NL", 1): "Southbound"}[(line, dirn)]
        stops.append([sid, "%s Station %s" % (N.STN[st]["name"], plat), "%.6f" % lat, "%.6f" % lon, "0"])
    write_csv(os.path.join(folder, "stops.txt"), ["stop_id", "stop_name", "stop_lat", "stop_lon", "location_type"], stops)
    write_csv(os.path.join(folder, "agency.txt"), ["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang"],
              [["CT", "Carvale Transit", "https://www.carvaletransit.ca", P.TZ, "en"]])
    write_csv(os.path.join(folder, "routes.txt"), ["route_id", "agency_id", "route_short_name", "route_long_name", "route_type"],
              [["201", "CT", "Eastline", "Westgate - Prairie Gate", "0"], ["202", "CT", "Northline", "Centre Square - Larchmont", "0"]])
    sid_of = {("W26", "WKD"): "26WIN-WK", ("W26", "SAT"): "26WIN-SA", ("W26", "SUN"): "26WIN-SU",
              ("S26", "WKD"): "26SPR-WK", ("S26", "SAT"): "26SPR-SA", ("S26", "SUN"): "26SPR-SU"}
    cal = []
    for (per, dtp), sid in sorted(sid_of.items(), key=lambda kv: kv[1]):
        a, b = P.SERVICE[per]
        days = {"WKD": [1, 1, 1, 1, 1, 0, 0], "SAT": [0, 0, 0, 0, 0, 1, 0], "SUN": [0, 0, 0, 0, 0, 0, 1]}[dtp]
        cal.append([sid] + days + [a.strftime("%Y%m%d"), b.strftime("%Y%m%d")])
    write_csv(os.path.join(folder, "calendar.txt"),
              ["service_id", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "start_date", "end_date"], cal)
    cdates = []
    for d, name in sorted(P.HOLIDAYS.items()):
        per = N.period_of(d)
        if per not in ("W26", "S26"):
            continue
        cdates.append([sid_of[(per, "WKD")], d.strftime("%Y%m%d"), "2"])
        cdates.append([sid_of[(per, "SUN")], d.strftime("%Y%m%d"), "1"])
    write_csv(os.path.join(folder, "calendar_dates.txt"), ["service_id", "date", "exception_type"], cdates)
    trows, strows = [], []
    for tr in sorted(trips, key=lambda t: t["trip_id"]):
        route = "201" if tr["line"] == "EL" else "202"
        last = tr["stops"][-1][0]
        head = N.STN[last]["name"]
        trows.append([route, sid_of[(tr["period"], tr["daytype"])], tr["trip_id"], head, str(tr["direction"]), tr["block_id"]])
        n = len(tr["stops"])
        for i, (st, arr, dep) in enumerate(tr["stops"]):
            strows.append([tr["trip_id"], N.gtfs_time(arr), N.gtfs_time(dep), STOP_IDS[(tr["line"], st, tr["direction"])],
                           str(i + 1), "1" if i == n - 1 else "0", "1" if i == 0 else "0"])
    write_csv(os.path.join(folder, "trips.txt"), ["route_id", "service_id", "trip_id", "trip_headsign", "direction_id", "block_id"], trows)
    write_csv(os.path.join(folder, "stop_times.txt"),
              ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "pickup_type", "drop_off_type"], strows)
    write_csv(os.path.join(folder, "feed_info.txt"),
              ["feed_publisher_name", "feed_publisher_url", "feed_lang", "feed_start_date", "feed_end_date", "feed_version"],
              [["Carvale Transit", "https://www.carvaletransit.ca", "en", "20260104", "20260627", "2026.03.29-r2"]])
    return len(strows)


def write_geojson(path, layout, eff_from, eff_to):
    feats = []
    names = {"D1": "Downtown", "D2": "West", "D3": "Station Hill", "D4": "Union Yards", "D5": "Hollin",
             "D6": "Millbrook", "D7": "Ashford", "D8": "Cobb", "D9": "Ridgeview", "D10": "Larchmont"}
    for d in sorted(layout, key=lambda s: int(s[1:])):
        polys = []
        for (x0, y0, x1, y1) in layout[d]:
            polys.append([[[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]])
        props = {"DISTRICT": d, "DIST_NAME": "District %s - %s" % (d[1:], names[d]), "EFF_FROM": eff_from}
        if eff_to:
            props["EFF_TO"] = eff_to
        feats.append({"type": "Feature", "properties": props, "geometry": {"type": "MultiPolygon", "coordinates": polys}})
    fc = {"type": "FeatureCollection", "name": os.path.basename(path).replace(".geojson", ""),
          "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::26912"}}, "features": feats}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fc, f, indent=1)
        f.write("\n")


def pawn_rows():
    """Second-hand dealer returns for phones bought in Q1 2026 (the bylaw return the dealers file monthly)."""
    rng = np.random.default_rng(P.SEED + 404)
    makes = [("Apple", ["iPhone 13", "iPhone 14", "iPhone 15", "iPhone 15 Pro", "iPhone 12"]),
             ("Samsung", ["Galaxy S23", "Galaxy S22", "Galaxy A54", "Galaxy S24"]), ("Google", ["Pixel 7", "Pixel 8"]),
             ("Motorola", ["moto g power", "edge 2023"])]
    dealers = ["SHD-0%d" % n for n in rng.choice(np.arange(212, 299), size=11, replace=False)]
    rows = []
    d = dt.date(2026, 1, 2)
    while d <= dt.date(2026, 3, 31):
        for _ in range(int(rng.poisson(9.5))):
            mk, models = makes[int(rng.choice(len(makes), p=[0.55, 0.32, 0.08, 0.05]))]
            rows.append([dealers[int(rng.integers(0, len(dealers)))], d.isoformat(), mk, models[int(rng.integers(0, len(models)))],
                         "35%06d*******" % int(rng.integers(0, 999999)), "S%07d" % int(rng.integers(1000000, 9999999)),
                         int(rng.integers(4, 60)) * 10])
        d += dt.timedelta(days=1)
    return rows
