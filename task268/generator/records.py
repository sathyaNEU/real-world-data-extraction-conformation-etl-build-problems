"""The pack's record files as the organisation's systems export them: the grid of Annex A, the paper tow sheets
transcribed for 2019 to 2022, the members' e-logbook hauls from 2023, the autumn survey's tows, the members' list, the
conversion table and the sea temperatures the members' net sensors log. Each writer returns its row count."""
import csv
import datetime as dt
import math

import numpy as np

import common as K
import world as W


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def dm(x):
    return "%.4f" % x


# ---------------------------------------------------------------------------------------------- Annex A
def grid_rows(T):
    rows = []
    for c in T["cells"]:
        rows.append([c["code"], c["rect"], "%d" % c["sub"], K.GROUND_CODE[c["ground"]], c["ground"], c["band"],
                     c["depth"], dm(c["lat_n"]), dm(c["lat_s"]), dm(c["lon_w"]), dm(c["lon_e"]), "%.2f" % c["area"]])
    order = {g: i for i, g in enumerate(K.GROUND_NAMES)}
    rows.sort(key=lambda r: (order[r[4]], r[1], int(r[2])))
    return rows


def write_grid(path, T):
    return _csv(path, ["cell", "rectangle", "sub_square", "ground_code", "ground", "depth_band", "charted_depth_m",
                       "lat_north", "lat_south", "lon_west", "lon_east", "area_km2"], grid_rows(T))


# ---------------------------------------------------------------------------------------------- the paper tow sheets
def vessel_by_rss(T):
    return {v["rss"]: v for v in T["vessels"]}


def landing_port(T, trip, rng_key):
    """The port a trip lands at: the boat's home port that day, now and then another (weather, a buyer's order)."""
    v = vessel_by_rss(T)[trip["vessel"]]
    home = W.port_on(v, trip["end"])
    h = (trip["id"] * 2654435761 + rng_key) % 1000
    if h < 80:
        others = [p for p in K.PORT_NAMES if p != home]
        return others[h % 3]
    return home


def paper_rows(T):
    rows = []
    V = vessel_by_rss(T)
    seq = {}
    for t in T["trips"]:
        if t["year"] not in K.PAPER_YEARS:
            continue
        v = V[t["vessel"]]
        agg = {}
        for hi in t["hauls"]:
            h = T["hauls"][hi]
            a = agg.setdefault(h["cell"], [0.0, 0.0, 0.0, 0.0, 0.0])
            a[0] += h["hours"]
            a[1] += h["had"]
            a[2] += h["cod"]
            a[3] += h["whg"]
            a[4] += h["pok"]
        yy = t["end"].year
        seq[yy] = seq.get(yy, 0) + 1
        sheet = "TS%02d-%04d" % (yy % 100, seq[yy])
        port = landing_port(T, t, 17)
        for c in sorted(agg, key=lambda c: T["cells"][c]["code"]):
            a = agg[c]
            cell = T["cells"][c]
            r5 = lambda x: int(5 * round(x / 5))
            rows.append([sheet, W.pln_on(v, t["end"]), t["start"].isoformat(), t["end"].isoformat(), port, cell["rect"],
                         "%d" % cell["sub"], "%.1f" % (round(a[0] * 2) / 2), r5(a[1]), r5(a[2]), r5(a[3]), r5(a[4])])
    return rows


def write_paper(path, T):
    return _csv(path, ["sheet_no", "vessel_pln", "departed", "landed", "landing_port", "rectangle", "sub_square",
                       "hours_fished", "haddock_kg", "cod_kg", "whiting_kg", "saithe_kg"], paper_rows(T))


# ---------------------------------------------------------------------------------------------- the e-logbook
def elog_rows(T):
    rows = []
    rng = np.random.default_rng(T["seed"] * 7 + 3)
    hid = {}
    for t in T["trips"]:
        if t["year"] not in K.ELOG_YEARS:
            continue
        yy = t["start"].year
        tref = "DV%02d%05d" % (yy % 100, t["id"])
        for hi in t["hauls"]:
            h = T["hauls"][hi]
            cell = T["cells"][h["cell"]]
            lat = cell["lat_s"] + (cell["lat_n"] - cell["lat_s"]) * float(rng.uniform(0.05, 0.95))
            lon = cell["lon_w"] + (cell["lon_e"] - cell["lon_w"]) * float(rng.uniform(0.05, 0.95))
            start = h["start"].replace(second=0, microsecond=0)
            end = (h["start"] + dt.timedelta(hours=h["hours"])).replace(second=0, microsecond=0)
            hid[yy] = hid.get(yy, 0) + 1
            g = lambda x: int(round(x / 1.17))
            rows.append(["H%02d-%06d" % (yy % 100, hid[yy]), tref, t["vessel"], start.strftime("%Y-%m-%dT%H:%MZ"),
                         end.strftime("%Y-%m-%dT%H:%MZ"), "%.4f" % lat, "%.4f" % lon, cell["code"], "OTB", 120,
                         g(h["had"]), g(h["cod"]), g(h["whg"]), g(h["pok"])])
    return rows


def write_elog(path, T):
    return _csv(path, ["haul_id", "trip_ref", "vessel_rss", "haul_start_utc", "haul_end_utc", "shot_lat", "shot_lon",
                       "cell", "gear", "mesh_mm", "had_gutted_kg", "cod_gutted_kg", "whg_gutted_kg", "pok_gutted_kg"],
                elog_rows(T))


# ---------------------------------------------------------------------------------------------- the survey
def survey_rows(T):
    rows = []
    for y in K.YEARS:
        ts = sorted([t for t in T["tows"] if t["year"] == y], key=lambda t: (t["date"], t["time"]))
        for k, t in enumerate(ts, 1):
            rows.append([y, "%d/%03d" % (y, k), t["station"], K.GROUND_CODE[t["ground"]], t["date"].isoformat(), t["time"],
                         "%.4f" % t["lat"], "%.4f" % t["lon"], t["depth"], 30, "%.1f" % t["had_kg"], t["had_n"],
                         t["had_juv"], "%.1f" % t["cod_kg"], "%.1f" % t["whg_kg"], "%.1f" % t["pok_kg"], t["spurdog_n"],
                         "%.1f" % t["skate_kg"], t["porpoise_n"], t["seabird_n"]])
    return rows


def write_survey(path, T):
    return _csv(path, ["survey_year", "tow", "station", "ground_code", "date", "shot_time", "shot_lat", "shot_lon",
                       "depth_m", "duration_min", "haddock_kg", "haddock_n", "haddock_under_30cm_n", "cod_kg",
                       "whiting_kg", "saithe_kg", "spurdog_n", "skates_rays_kg", "porpoise_n", "seabird_n"],
                survey_rows(T))


# ---------------------------------------------------------------------------------------------- conversion factors
FACTORS = [("HAD", "WHL", 1.00), ("HAD", "GUT", 1.17), ("COD", "WHL", 1.00), ("COD", "GUT", 1.17),
           ("WHG", "WHL", 1.00), ("WHG", "GUT", 1.18), ("POK", "WHL", 1.00), ("POK", "GUT", 1.19),
           ("HKE", "WHL", 1.00), ("HKE", "GUT", 1.11), ("MON", "WHL", 1.00), ("MON", "GUT", 1.22),
           ("MON", "TAL", 3.00), ("LEM", "WHL", 1.00), ("LEM", "GUT", 1.05), ("PLE", "WHL", 1.00),
           ("PLE", "GUT", 1.05), ("WIT", "WHL", 1.00), ("WIT", "GUT", 1.06)]
PRES = {"WHL": "whole", "GUT": "gutted, head on", "TAL": "tails"}


def write_factors(path):
    rows = [[sp, K.SPECIES[sp], pr, PRES[pr], "%.2f" % f, "2018-01-01"] for sp, pr, f in FACTORS]
    return _csv(path, ["species_code", "species", "presentation_code", "presentation", "factor_to_live", "valid_from"], rows)


# ---------------------------------------------------------------------------------------------- the members' list
def write_members(path, T, licences):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Vessels"
    ws.append(["Vessel", "PLN", "RSS no", "Length (m)", "Home port", "Licence no", "Pool", "Member since"])
    lic_of = {l["vessel"]: l for l in licences if l["vessel"]}
    for v in sorted(T["vessels"], key=lambda v: v["name"]):
        ws.append([v["name"], v["pln"], v["rss"], v["length"], v["port"], lic_of[v["rss"]]["no"], v["pool"],
                   v["since"]])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, w in zip("ABCDEFGH", (18, 9, 9, 10, 11, 10, 6, 13)):
        ws.column_dimensions[col].width = w
    hs = wb.create_sheet("Registration history")
    hs.append(["Vessel", "RSS no", "PLN", "Port", "Registered from", "Registered to"])
    for v in sorted(T["vessels"], key=lambda v: v["name"]):
        for pln, start, end, port in v["history"]:
            hs.append([v["name"], v["rss"], pln, port, start if start else v["registered"], end])
    for c in hs[1]:
        c.font = Font(bold=True)
    for col, w in zip("ABCDEF", (18, 9, 9, 11, 15, 13)):
        hs.column_dimensions[col].width = w
    for row in hs.iter_rows(min_row=2):
        for c in row[4:6]:
            c.number_format = "dd/mm/yyyy"
    for row in ws.iter_rows(min_row=2):
        row[7].number_format = "dd/mm/yyyy"
    ls = wb.create_sheet("Licences")
    ls.append(["Licence no", "Holder", "Vessel RSS no", "Pool", "Pool name"])
    pname = dict(K.POOLS)
    for l in sorted(licences, key=lambda l: l["no"]):
        ls.append([l["no"], l["holder"], l["vessel"] or None, l["pool"], pname[l["pool"]]])
    for c in ls[1]:
        c.font = Font(bold=True)
    for col, w in zip("ABCDE", (10, 30, 13, 6, 13)):
        ls.column_dimensions[col].width = w
    wb.save(path)
    return len(T["vessels"])


# ---------------------------------------------------------------------------------------------- sea temperature
def write_temperature(path, T):
    rng = np.random.default_rng(T["seed"] * 11 + 5)
    rects = sorted({c["rect"] for c in T["cells"]})
    rows = []
    for r in rects:
        off = float(rng.normal(0, 0.25))
        for y in K.YEARS:
            for m in range(1, 13):
                if y == 2026 and m > 10:
                    continue
                n = int(rng.integers(0, 140))
                if n == 0:
                    rows.append([r, y, m, "", "", 0])
                    continue
                trend = 0.04 * (y - 2019)
                bot = 7.6 + 0.9 * math.sin(2 * math.pi * (m - 7) / 12) + off + trend + float(rng.normal(0, 0.18))
                sst = 9.8 + 3.4 * math.sin(2 * math.pi * (m - 5.2) / 12) + off + trend + float(rng.normal(0, 0.3))
                rows.append([r, y, m, "%.2f" % bot, "%.2f" % sst, n])
    return _csv(path, ["rectangle", "year", "month", "bottom_temperature_c", "surface_temperature_c", "n_readings"], rows)
