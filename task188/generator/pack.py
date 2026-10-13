"""The rest of the pack: the 2026 site register, the zone map, the export manifest and three files a surveillance
analyst would weigh and this question does not use (the airport's daily weather, dead bird reports and past aerial
applications)."""
import csv
import datetime as dt
import json
import math

import ecology as E
import world as W

REGISTER = "RCVCD_site_register_2026.xlsx"
ZONEMAP = "RCVCD_zones_2026.geojson"
WEATHER = "FJE_airport_daily_weather_2026.csv"
BIRDS = "dead_bird_reports_2026.csv"
FLIGHTS = "aerial_applications_2024_2026.csv"
MANIFEST = "extract_manifest_2026-08-17.csv"


def write_register(path, sites):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Sites"
    ws.append(["Site ID", "Zone", "Trap type", "Habitat", "Section", "Latitude", "Longitude", "In service from"])
    for s in sorted(sites, key=lambda s: (W.ZONES.index(s["zone"]), s["trap_type"], s["site_id"])):
        ws.append([s["site_id"], s["zone"], "CO2 light trap" if s["trap_type"] == "CO2" else "Gravid trap", s["habitat"],
                   s["section"], s["lat"], s["lon"], 2024])
    for i, w in enumerate([9, 16, 15, 22, 16, 10, 11, 14]):
        ws.column_dimensions[chr(65 + i)].width = w
    cw = wb.create_sheet("Crosswalk")
    cw.append(["Legacy code", "Site ID", "Migrated"])
    for s in sorted(sites, key=lambda s: s["legacy"]):
        cw.append([s["legacy"], s["site_id"], dt.date(2026, 6, 15)])
    for row in cw.iter_rows(min_row=2):
        row[2].number_format = "yyyy-mm-dd"
    cw.column_dimensions["A"].width = 12
    cw.column_dimensions["B"].width = 10
    cw.column_dimensions["C"].width = 12
    zs = wb.create_sheet("Zone sections")
    zs.append(["Section", "Township", "Range", "Section no.", "Zone", "Effective"])
    for y in range(W.NY - 1, -1, -1):
        for x in range(W.NX):
            t, r, sec = W.township_range(x, y)
            zs.append([W.section_label(x, y), "T%dN" % t, "R%dW" % r, sec, W.zone2026(x, y), dt.date(2026, 5, 1)])
    for row in zs.iter_rows(min_row=2):
        row[5].number_format = "yyyy-mm-dd"
    for i, w in enumerate([16, 10, 8, 11, 16, 12]):
        zs.column_dimensions[chr(65 + i)].width = w
    for sh in (ws, cw, zs):
        for c in sh[1]:
            c.font = Font(bold=True)
        sh.freeze_panes = "A2"
    wb.save(path)


def write_zonemap(path):
    """Each zone as a multipolygon of its sections, each row of sections merged into one rectangle."""
    feats = []
    for z in W.ZONES:
        polys = []
        for y in range(W.NY):
            x = 0
            while x < W.NX:
                if W.zone2026(x, y) != z:
                    x += 1
                    continue
                x0 = x
                while x < W.NX and W.zone2026(x, y) == z:
                    x += 1
                lat0 = W.SW_LAT + y * W.DLAT
                lat1 = lat0 + W.DLAT
                lon0 = W.SW_LON + x0 * W.DLON
                lon1 = W.SW_LON + x * W.DLON
                ring = [[round(lon0, 6), round(lat0, 6)], [round(lon1, 6), round(lat0, 6)], [round(lon1, 6), round(lat1, 6)],
                        [round(lon0, 6), round(lat1, 6)], [round(lon0, 6), round(lat0, 6)]]
                polys.append([ring])
        n = sum(1 for x in range(W.NX) for y in range(W.NY) if W.zone2026(x, y) == z)
        feats.append({"type": "Feature", "properties": {"zone": z, "code": W.ZCODE[z], "sections": n,
                                                        "effective": "2026-05-01"},
                      "geometry": {"type": "MultiPolygon", "coordinates": polys}})
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"type": "FeatureCollection", "name": "RCVCD treatment zones 2026", "features": feats}, fh,
                  separators=(",", ":"))
        fh.write("\n")


def weather_rows():
    g = W.rng("weather")
    out = []
    d = dt.date(2026, 5, 1)
    while d <= dt.date(2026, 8, 16):
        doy = d.timetuple().tm_yday
        tmax = 51.0 + 32.0 * math.cos((doy - 200) / 365.0 * 2 * math.pi) + g.normal(0, 5.2)
        tmin = tmax - 22.0 + g.normal(0, 3.4)
        rain = g.random() < 0.27
        pr = round(float(g.gamma(0.9, 0.32)), 2) if rain else 0.0
        wind = max(2.0, g.normal(11.5, 3.6))
        gust = wind + abs(g.normal(8.0, 3.0))
        dew = tmin + g.normal(1.5, 2.5)
        trace = (not rain) and g.random() < 0.05
        out.append([d.isoformat(), round(tmax), round(tmin), round(dew), "T" if trace else "%.2f" % pr, "%.1f" % wind,
                    round(gust)])
        d += dt.timedelta(days=1)
    return out


def write_weather(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["date", "tmax_f", "tmin_f", "dewpoint_f", "precip_in", "wind_avg_mph", "gust_mph"])
        w.writerows(weather_rows())


BIRD_SPECIES = ["American crow", "Blue jay", "American robin", "House sparrow", "Common grackle", "Black-billed magpie",
                "Mourning dove", "Red-tailed hawk"]


def bird_rows():
    g = W.rng("birds")
    res = W.residents()
    secs = sorted(res)
    weights = [res[s] for s in secs]
    tot = float(sum(weights))
    out = []
    n = 46
    days = sorted(int(g.integers(0, 76)) for _ in range(n))
    for k, dd in enumerate(days):
        d = dt.date(2026, 6, 1) + dt.timedelta(days=dd)
        i = int(g.choice(len(secs), p=[w / tot for w in weights]))
        sp = BIRD_SPECIES[int(g.choice(len(BIRD_SPECIES), p=[0.34, 0.2, 0.14, 0.1, 0.08, 0.06, 0.05, 0.03]))]
        fresh = g.random() < 0.55 and sp in ("American crow", "Blue jay", "Black-billed magpie", "Common grackle")
        if fresh and d >= dt.date(2026, 6, 20):
            res_t = "WNV positive" if g.random() < (0.12 + 0.5 * (d - dt.date(2026, 6, 20)).days / 56.0) else "WNV negative"
            tested = "Y"
        else:
            res_t, tested = "", "N"
        out.append(["DB-26-%03d" % (k + 1), d.isoformat(), sp, W.section_label(*secs[i]), tested, res_t,
                    "" if tested == "Y" else ("not collected" if g.random() < 0.6 else "too decomposed")])
    return out


def write_birds(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["report_id", "reported", "species", "section", "tested", "result", "reason_not_tested"])
        w.writerows(bird_rows())


FLIGHT_ROWS = [
    ("2024-07-25", "South Prairie", "flown", 9.4), ("2024-08-08", "Old Town", "flown", 6.1),
    ("2024-08-15", "Riverside South", "flown", 5.2), ("2024-08-22", "", "no block designated", None),
    ("2025-07-17", "North Bottoms", "flown", 7.8), ("2025-07-31", "Coulee Hills", "flown", 8.3),
    ("2025-08-07", "Old Town", "lapsed, wind", None), ("2025-08-14", "Maple Ridge", "flown", 4.9),
    ("2025-08-21", "Westbrook", "flown", 6.6),
    ("2026-07-02", "", "no block designated", None), ("2026-07-09", "", "no block designated", None),
    ("2026-07-16", "Coulee Hills", "flown", 8.9), ("2026-07-23", "Coulee Hills", "flown", 7.2),
    ("2026-07-30", "", "no block designated", None), ("2026-08-06", "Maple Ridge", "flown, Friday night", 5.6),
    ("2026-08-13", "North Bottoms", "lapsed, rain", None),
]


def zone_acres(z):
    return sum(640 for x in range(W.NX) for y in range(W.NY) if W.zone2026(x, y) == z)


def write_flights(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["flight_thursday", "block", "outcome", "acres_treated", "wind_mph_at_release", "aircraft"])
        for d, z, outc, wind in FLIGHT_ROWS:
            acres = ""
            if outc.startswith("flown"):
                acres = int(zone_acres(z) * (0.93 if d >= "2026" else 0.9)) if z else ""
            w.writerow([d, z, outc, acres, "" if wind is None else "%.1f" % wind,
                        "N44OA" if outc.startswith("flown") else ""])


def write_manifest(path, entries):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["file", "content", "from", "as_of", "rows"])
        for e in entries:
            w.writerow(e)
