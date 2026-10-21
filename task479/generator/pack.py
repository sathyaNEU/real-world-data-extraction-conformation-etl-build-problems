"""The pack's data files, written from the truth in world.py: the Lodging Monitor's two report exports (the legacy
system to March 2022, the current one since), the panel's property register, the vendor's id crosswalk, the
Department's county tax rates and the tourism bureau's visitor spending estimates."""
import calendar
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "legacy": "tla_monitor_reports_2018-01_to_2022-03.csv",
    "current": "tla_monitor_reports_2022-04_to_2026-09.csv",
    "register": "tla_monitor_properties_2026-10-02.csv",
    "xwalk": "innsight_property_id_crosswalk_2022-04.csv",
    "rates": "tdor_county_lodging_tax_rates_2018-2026.csv",
    "visitor": "ttb_visitor_spending_by_county_2019-2024.csv",
    "method": "tla_lodging_monitor_methods_2026.pdf",
    "program": "tla_rising_destinations_2027_program.docx",
    "dictionary": "tla_research_data_dictionary.csv",
    "manifest": "tla_research_extract_manifest_2026-10-02.csv",
}
for _y in W.BENCH:
    FILES["dor%d" % _y] = "tdor_taxable_lodging_receipts_ty%d.pdf" % _y
DOR_ISSUED = {2018: (2019, 12, 10), 2019: (2020, 12, 15), 2020: (2021, 12, 14), 2021: (2022, 12, 13),
              2022: (2023, 12, 12), 2023: (2024, 12, 10), 2024: (2025, 12, 9)}
EXTRACT = dt.datetime(2026, 10, 2, 6, 40)
COMPANY = "Tarrowind Lodging Association"

LEGACY_COLS = ["Property ID", "Property Name", "County", "Report Month", "Rooms Available", "Rooms Sold",
               "Room Revenue", "Received"]
CURRENT_COLS = ["submission_id", "prop_id", "period", "county_code", "avail_room_nights", "sold_room_nights",
                "room_revenue_cents", "submitted_at_utc"]
REGISTER_COLS = ["prop_id", "property_name", "street", "city", "county", "rooms", "management_company",
                 "panel_status"]
XWALK_COLS = ["legacy_property_id", "innsight_prop_id", "property_name_at_mapping", "mapped_on"]
RATES_COLS = ["county_code", "county", "state_rate_pct", "county_rate_pct", "effective_from", "effective_to"]
VISITOR_COLS = ["county", "year", "visitor_spending_usd_millions", "lodging_share_pct", "day_trip_share_pct",
                "estimate_status"]

TOWNS = {
    "Arvenne": ["Arvenne City", "Southgate", "Millbrook Park"], "Brisholt": ["Brisholt Beach", "Gullhaven"],
    "Corrigan Bay": ["Port Corrigan", "Sandreach"], "Delvane": ["Delvane Springs", "Highcroft"],
    "Elsmoor": ["Elsmoor Shores", "Dunlin Point"], "Fallowmere": ["Fallowmere", "Ridgewater"],
    "Grindell": ["Grindell", "Ashby Crossing"], "Hollin Ridge": ["Hollin", "Cedar Notch"],
    "Isterhaven": ["Isterhaven", "Riverside Heights"], "Jorvale": ["Jorvale", "Tamsin Mill"],
    "Kestholm": ["Kestholm", "North Kestholm"], "Larrowby": ["Larrowby", "Fenwick Corner"],
    "Marrowfield": ["Marrowfield", "Oatlands"], "Nethervane": ["Nethervane Beach", "Kittiwake"],
    "Orrin Falls": ["Orrin Falls", "Bluestem"], "Pellow Sound": ["Pellow", "Sound Harbor"],
}
STEMS = ["Harborview", "Seabright", "Pinecrest", "Lakeside", "Summit", "Willow Creek", "Bayfront", "Stonebridge",
         "Maple Grove", "Riverbend", "Lighthouse", "Cardinal", "Heritage", "Juniper", "Meadowlark", "Granite Peak",
         "Driftwood", "Saltmarsh", "Copper Kettle", "Old Mill", "Bluewater", "Timberline", "Sandpiper", "Foxglove",
         "Northstar", "Crescent", "Gateway", "Oak Hollow", "Tidewater", "Aspen", "Larkspur", "Hearthstone"]
KINDS = ["Inn", "Hotel", "Lodge", "Motor Inn", "Suites", "Resort", "Inn & Suites", "Cottages"]
STREETS = ["Main St", "Shore Rd", "Ocean Ave", "Highway 9", "Mill Rd", "Lake Dr", "Pine St", "Summit Way",
           "Harbor Blvd", "Route 41", "Bay St", "Market St", "Ridge Rd", "Station Ave", "Elm St", "Beach Rd"]
COMPANIES = ["Harbor & Pine Hospitality", "Coastline Hotel Group", "Bramwell Lodging", "Summit Ridge Hospitality",
             "Northgate Inns"]


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def names(x):
    """Each property's name, street, city and management company, and the legacy name where the property was
    renamed between its legacy reports and the register."""
    rng = np.random.default_rng(W.SEED + 11)
    used = set()
    for p in x["props"]:
        while True:
            nm = "%s %s" % (STEMS[int(rng.integers(0, len(STEMS)))], KINDS[int(rng.integers(0, len(KINDS)))])
            if (p["county"], nm) not in used:
                used.add((p["county"], nm))
                break
        p["name"] = nm
        towns = TOWNS[p["county"]]
        p["city"] = towns[int(rng.integers(0, len(towns)))]
        p["street"] = "%d %s" % (int(rng.integers(10, 2900)), STREETS[int(rng.integers(0, len(STREETS)))])
        p["company"] = COMPANIES[1 + int(rng.integers(0, 4))] if rng.random() < 0.28 else ""
        p["legacy_name"] = nm
    for p in x["props"]:
        if p["k"] in x["mgmt"]:
            p["company"] = "Harbor & Pine Hospitality"
        elif p["company"] == "" and p["county"] == W.MGMT_COUNTY and rng.random() < 0.3:
            p["company"] = "Harbor & Pine Hospitality"
    # rebrands: the property's legacy name differs from the register's; the crosswalk gaps all rebranded, and so
    # did properties the crosswalk maps
    for p in x["props"]:
        if p["k"] in x["xwalk_gap"] or (rng.random() < 0.05 and (p["close"] is None or p["close"] > (2022, 3))):
            stem = STEMS[int(rng.integers(0, len(STEMS)))]
            p["legacy_name"] = "%s %s" % (stem, KINDS[int(rng.integers(0, len(KINDS)))])
            if p["legacy_name"] == p["name"]:
                p["legacy_name"] = p["name"] + " Motel"


def county_name_legacy(c):
    return c.upper() if c in ("Jorvale", "Larrowby", "Marrowfield") else c


def legacy_rows(x):
    """The legacy reporting system, January 2018 to March 2022: one row per report received, a revised report
    beside the one it revises and a report sent twice beside itself, received stamps in local time."""
    rng = np.random.default_rng(W.SEED + 21)
    pk = {p["k"]: p for p in x["props"]}
    out = []
    for r in x["rep"]:
        if (r["y"], r["m"]) > (2022, 3):
            continue
        p = pk[r["k"]]
        due = W.month_end(r["y"], r["m"]) + dt.timedelta(days=int(rng.integers(3, 24)))
        rec = dt.datetime(due.year, due.month, due.day, int(rng.integers(7, 19)), int(rng.integers(0, 60)))
        kind, f = x["resub"].get((r["k"], r["y"], r["m"]), (None, 0.0))
        subs = []
        if kind == "revised":
            subs.append((W.submitted_report(r, kind, f), rec))
            subs.append((r, rec + dt.timedelta(days=int(rng.integers(6, 50)), hours=int(rng.integers(1, 9)))))
        elif kind == "repeat":
            subs.append((r, rec))
            subs.append((r, rec + dt.timedelta(minutes=int(rng.integers(2, 300)))))
        else:
            subs.append((r, rec))
        for s, when in subs:
            out.append((p["old_id"], p["legacy_name"], county_name_legacy(p["county"]), "%02d/%d" % (r["m"], r["y"]),
                        s["avail"], s["sold"], "%.2f" % s["rev"], when.strftime("%m/%d/%Y %H:%M"), when))
    out.sort(key=lambda t: (t[8], t[0]))
    return [t[:8] for t in out]


def current_rows(x):
    """The current system (InnSight), April 2022 to September 2026: revenue in cents, submission stamps in UTC,
    September 2026 only from the properties that had reported by the extract. Harbor & Pine's portal account files
    its properties under its own office county from April 2026."""
    rng = np.random.default_rng(W.SEED + 31)
    pk = {p["k"]: p for p in x["props"]}
    out = []
    sept = {}
    for p in x["props"]:
        sept[p["k"]] = rng.random() < 0.58
    reps = [r for r in x["rep"] if (r["y"], r["m"]) >= (2022, 4)]
    # September 2026 is the month after the last full one: generated here from August's pattern
    extra = []
    for r in reps:
        if (r["y"], r["m"]) == W.LAST and sept[r["k"]]:
            s = dict(r)
            s["m"] = 9
            days = 30
            s["avail"] = r["avail"] // 31 * days
            s["sold"] = int(round(s["avail"] * r["sold"] / r["avail"] * 0.84))
            s["rev"] = round(r["rev"] / r["sold"] * s["sold"] * 0.97, 2) if r["sold"] else 0.0
            extra.append(s)
    n = 0
    for r in reps + extra:
        p = pk[r["k"]]
        local = W.month_end(r["y"], r["m"]) + dt.timedelta(days=int(rng.integers(2, 21)))
        if (r["y"], r["m"]) == (2026, 9):
            local = dt.date(2026, 10, int(rng.integers(1, 3)))
        hh = int(rng.integers(12, 24)) if (r["y"], r["m"]) != (2026, 9) else int(rng.integers(0, 10))
        utc = dt.datetime(local.year, local.month, local.day, hh, int(rng.integers(0, 60)), int(rng.integers(0, 60)))
        if utc > EXTRACT:
            utc = EXTRACT - dt.timedelta(minutes=int(rng.integers(5, 300)))
        code = W.CODE[p["county"]]
        if p["k"] in x["mgmt"] and (r["y"], r["m"]) >= W.MGMT_TAKEOVER:
            code = W.CODE[W.MGMT_COUNTY]
        kind, f = x["resub"].get((r["k"], r["y"], r["m"]), (None, 0.0))
        subs = []
        if kind == "revised" and (r["y"], r["m"]) < (2026, 9):
            later = utc + dt.timedelta(days=int(rng.integers(4, 40)), hours=int(rng.integers(1, 9)))
            if later > EXTRACT:
                later = EXTRACT - dt.timedelta(minutes=17)
            subs = [(W.submitted_report(r, kind, f), utc), (r, later)]
        elif kind == "repeat":
            subs = [(r, utc), (r, utc + dt.timedelta(seconds=int(rng.integers(20, 4000))))]
        else:
            subs = [(r, utc)]
        for s, when in subs:
            n += 1
            out.append([None, p["new_id"], "%d-%02d" % (r["y"], r["m"]), code, s["avail"], s["sold"],
                        int(round(s["rev"] * 100)), when.strftime("%Y-%m-%dT%H:%M:%SZ"), when])
    out.sort(key=lambda t: (t[8], t[1]))
    for i, t in enumerate(out):
        t[0] = "S%07d" % (4410023 + 7 * i)
    return [t[:8] for t in out]


def register_rows(x):
    """The panel's property register as InnSight holds it on the extract day: every property that came across in
    April 2022, its county and its rooms today."""
    rows = []
    for p in sorted(x["props"], key=lambda p: p["new_id"]):
        if not (p["close"] is None or p["close"] > (2022, 3)):
            continue
        rp = p["rooms_path"]
        rooms = rp["rooms"] if rp else p["rooms"]
        status = "reporting" if p["close"] is None else "closed"
        rows.append((p["new_id"], p["name"], p["street"], p["city"], p["county"], rooms, p["company"], status))
    return rows


def xwalk_rows(x):
    rows = []
    for p in sorted(x["props"], key=lambda p: p["old_id"]):
        if not (p["close"] is None or p["close"] > (2022, 3)) or p["k"] in x["xwalk_gap"]:
            continue
        rows.append((p["old_id"], p["new_id"], p["legacy_name"], "2022-04-01"))
    return rows


RATE_CHANGES = {"Brisholt": (2022, 7, 1.0), "Elsmoor": (2023, 1, 0.5), "Fallowmere": (2021, 7, 1.0),
                "Corrigan Bay": (2024, 7, -0.5), "Arvenne": (2020, 1, 0.5), "Delvane": (2025, 1, 1.0)}
BASE_RATE = {n: 2.0 + (i * 7 % 5) * 0.5 for i, n in enumerate(W.NAMES)}


def rate_on(name, y, m=7):
    r = BASE_RATE[name]
    if name in RATE_CHANGES:
        cy, cm, d = RATE_CHANGES[name]
        if (y, m) >= (cy, cm):
            r += d
    return r


def rates_rows():
    rows = []
    for n in W.NAMES:
        if n in RATE_CHANGES:
            cy, cm, d = RATE_CHANGES[n]
            end = dt.date(cy, cm, 1) - dt.timedelta(days=1)
            rows.append((W.CODE[n], n, "6.00", "%.2f" % BASE_RATE[n], "2018-01-01", end.isoformat()))
            rows.append((W.CODE[n], n, "6.00", "%.2f" % (BASE_RATE[n] + d), "%d-%02d-01" % (cy, cm), ""))
        else:
            rows.append((W.CODE[n], n, "6.00", "%.2f" % BASE_RATE[n], "2018-01-01", ""))
    return rows


def visitor_rows(x):
    """The state tourism bureau's visitor spending estimates (all spending by visitors, not lodging receipts):
    through 2024 only, the latest year preliminary."""
    rng = np.random.default_rng(W.SEED + 41)
    rows = []
    for n in W.NAMES:
        for y in range(2019, 2025):
            base = x["first"][(n, y)] / 1e6
            spend = base * float(rng.uniform(2.6, 3.4)) * (1 + 0.02 * (y - 2019))
            lodge = 100 * base / spend * float(rng.uniform(0.92, 1.05))
            rows.append((n, y, "%.1f" % spend, "%.1f" % lodge, "%.1f" % float(rng.uniform(18, 46)),
                         "preliminary" if y == 2024 else "final"))
    return rows
