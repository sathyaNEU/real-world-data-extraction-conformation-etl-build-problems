"""Writes the shipped data files from the world's objects, each in the layout and the vocabulary of the system that
keeps it: the county's device registry and burn zone parcel list, the survey vendor's response file, three propane
distributors' exports, the airport station's readings, the state's fuel and factor tables, the Census files the state
tool reads, and two files the program keeps for other work."""
import csv
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import world as W

SURVEY_LABEL = dict(UNC="Wood stove (not EPA certified)", CNC="Wood stove, EPA certified (non-catalytic)",
                    CAT="Wood stove, EPA certified (catalytic)", PEL="Pellet stove", FPL="Fireplace (open)",
                    HYD="Outdoor wood boiler")
FUEL_LABEL = dict(propane="Propane", gas="Natural gas", electric="Electricity", wood="Wood")
TOOL_SHARE = {True: dict(UNC=0.32, CNC=0.30, CAT=0.07, PEL=0.17, FPL=0.0, HYD=0.14),
              False: dict(UNC=0.20, CNC=0.24, CAT=0.05, PEL=0.09, FPL=0.42, HYD=0.0)}
TOOL_USE = {True: dict(UNC=4.1, CNC=3.7, CAT=3.6, PEL=3.1, FPL=0.9, HYD=7.4),
            False: dict(UNC=1.2, CNC=1.0, CAT=1.0, PEL=0.8, FPL=0.35, HYD=0.0)}
TOOL_SECONDARY = 2.2
STATION = "KHLV"
LONG = {"N": "North", "S": "South", "St": "Street", "Ave": "Avenue", "Dr": "Drive", "Ln": "Lane", "Rd": "Road",
        "Trl": "Trail", "Loop": "Loop"}
D1_NAME, D2_NAME, D3_NAME = "Wapiti Propane", "Coldwater Fuel & Propane", "Halvard Valley Farmers Cooperative"


def iso(d):
    return d.isoformat() if d else ""


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def long_form(a):
    """The cooperative's billing system writes street words out in full."""
    return " ".join(LONG.get(p, p) for p in a.split(" "))


def nodash(g):
    return g.replace("-", "")


# ---------------------------------------------------------------- the county's files

def registry_csv(path, devices):
    rows = []
    for d in devices:
        h = d.home
        inst = d.installed.isoformat() if d.installed.year >= 2008 else str(d.installed.year)
        if d.removed:
            status, sdate, reason = "Removed", iso(d.removed), d.reason
        else:
            status, sdate, reason = "Active", "", ""
        rows.append([d.did, h.parcel, h.address, W.ZNAME[h.zone], W.CLASSES[d.cl][2], d.cert or "", inst,
                     iso(d.registered), status, sdate, reason, d.replaced_by.did if d.replaced_by else ""])
    write_csv(path, ["device_id", "geocode", "site_address", "burn_zone", "device_code", "epa_cert_no", "installed",
                     "registered_on", "status", "status_date", "status_reason", "replaced_by_device"], rows)


def zone_parcels_csv(path, homes, acc):
    rows = [[h.parcel, h.address.upper(), W.ZNAME[h.zone], "Residential"] for h in homes]
    rows += [[a["parcel"], a["address"].upper(), W.ZNAME[a["zone"]], "Commercial"] for a in acc if a["cls"] == "COM"]
    rows.sort(key=lambda x: x[0])
    write_csv(path, ["geocode", "situs_address", "burn_zone", "land_use"], rows)


def scc_csv(path):
    write_csv(path, ["device_code", "device_description", "scc", "scc_description"],
              [[W.CLASSES[c][2], SURVEY_LABEL[c], W.CLASSES[c][0], W.CLASSES[c][1]] for c in W.CL])


# ---------------------------------------------------------------- the survey vendor's file

def survey_csv(path, resp):
    rows = []
    for i, x in enumerate(sorted(resp, key=lambda x: (x["dev"].home.zone, x["dev"].did))):
        d = x["dev"]
        amt = ("%g" % x["amount"])
        rows.append(["HS25-%04d" % (i + 1), W.ZNAME[d.home.zone], d.did, SURVEY_LABEL[d.cl],
                     FUEL_LABEL[d.home.fuel], amt, x["unit"], "%.3f" % x["weight"]])
    write_csv(path, ["respondent_id", "burn_zone", "device_id", "appliance", "main_heating_fuel",
                     "amount_burned_2024_25", "unit", "weight"], rows)


# ---------------------------------------------------------------- the distributors' exports

def wapiti(paths, acc, tk):
    """Wapiti's ticket system: one row per delivery ticket, and its account list."""
    mine = [a for a in acc if a["dist"] == "D1"]
    rows = []
    for a in sorted(mine, key=lambda a: a["no"]):
        rows.append([a["no"], "Commercial" if a["cls"] == "COM" else "Residential", a["address"],
                     a.get("town") or "Halvard", a["parcel"], iso(a["opened"])])
    write_csv(paths["acct"], ["account_no", "account_class", "service_address", "town", "geocode", "opened"], rows)
    r = np.random.default_rng(W.SEED + 61)
    out, n = [], 7_400_000
    for x in tk:
        if x["acct"]["dist"] != "D1":
            continue
        n += int(r.integers(1, 4))
        out.append([str(n), x["acct"]["no"], x["date"].strftime("%m/%d/%Y"), "%.1f" % x["gal"], "PROPANE",
                    "T%02d" % int(r.integers(1, 15))])
    write_csv(paths["tickets"], ["ticket_no", "account_no", "delivery_date", "gallons", "product", "truck"], out)


def coldwater(paths, acc, tk):
    """Coldwater's legacy billing export: fixed-width, an A record per account and a T record per transaction posted
    to it. Statement accounts post a month's deliveries on the first of the next month."""
    lines = []
    mine = sorted([a for a in acc if a["dist"] == "D2"], key=lambda a: a["no"])
    for a in mine:
        lines.append("A%-8s%s%-32s%-16s%-17s%s" % (a["no"], "C" if a["cls"] == "COM" else "R", a["address"].upper()[:32],
                                                   (a.get("town") or "HALVARD").upper()[:16], nodash(a["parcel"]),
                                                   a["opened"].strftime("%Y%m%d")))
    seq = {}
    trans = []
    for x in tk:
        a = x["acct"]
        if a["dist"] != "D2":
            continue
        d = x["date"]
        k = (d.year, d.month, d.day)
        seq[k] = seq.get(k, 400) + 1 + (len(trans) % 3)
        ref = "T%s-%04d" % (d.strftime("%y%m%d"), seq[k])
        if a["statement"]:
            post = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        else:
            post = d
        trans.append((a["no"], post, ref, "T%-8s%s%s%07d%s" % (a["no"], ref, post.strftime("%Y%m%d"),
                                                             int(round(x["gal"] * 10)), "LPG")))
    trans.sort(key=lambda t: (t[0], t[1], t[2]))
    lines += [t[3] for t in trans]
    with open(paths["export"], "w", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
    layout = [
        "COLDWATER FUEL & PROPANE - CUSTOMER ACTIVITY EXPORT - RECORD LAYOUT (rev. 2019-03)",
        "Fixed width, ASCII, CR LF line ends. Record type in column 1.",
        "",
        "A record (account master)",
        "  col   1      REC-TYPE        'A'",
        "  col   2-9    ACCT-NO         account number",
        "  col  10      ACCT-CLASS      R residential, C commercial",
        "  col  11-42   SERV-ADDR       service address",
        "  col  43-58   SERV-TOWN       service town",
        "  col  59-75   GEOCODE         Montana property geocode, no separators",
        "  col  76-83   OPEN-DT         account opened, CCYYMMDD",
        "",
        "T record (transaction)",
        "  col   1      REC-TYPE        'T'",
        "  col   2-9    ACCT-NO         account number",
        "  col  10-21   TKT-REF         delivery ticket reference",
        "  col  22-29   TRANS-DT        transaction date, CCYYMMDD",
        "  col  30-36   QTY             gallons, 9(6)V9 (one implied decimal)",
        "  col  37-39   PROD            product code (LPG propane)",
        "",
        "Extract: all accounts with activity 07/01/2023 through 06/30/2026, Halvard Valley service area, prepared for",
        "the Halvard County Air Quality Program under the data sharing agreement of 2019.",
    ]
    with open(paths["layout"], "w", newline="") as f:
        f.write("\r\n".join(layout) + "\r\n")


def cooperative(path, acc, tk):
    """The cooperative's propane division: gallons delivered by member account and month, one sheet per fill year."""
    mine = sorted([a for a in acc if a["dist"] == "D3"], key=lambda a: a["no"])
    by = {}
    for x in tk:
        a = x["acct"]
        if a["dist"] != "D3":
            continue
        by[a["no"], x["date"].year, x["date"].month] = by.get((a["no"], x["date"].year, x["date"].month), 0) + \
            int(round(x["gal"] * 10))
    wb = openpyxl.Workbook()
    first = True
    months = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    mname = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    for fy in (2023, 2024, 2025):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "FY%d-%02d" % (fy, (fy + 1) % 100)
        ws.append(["Halvard Valley Farmers Cooperative, propane division: gallons delivered by member account and "
                   "month, fiscal year July %d to June %d" % (fy, fy + 1)])
        ws.append([])
        ws.append(["Member account", "Class", "Service address", "Town"] + mname)
        for c in ws[3]:
            c.font = Font(bold=True)
        for a in mine:
            vals = []
            for m in months:
                y = fy if m >= 7 else fy + 1
                v = by.get((a["no"], y, m), 0)
                vals.append(v / 10.0 if v else None)
            ws.append([a["no"], "Commercial" if a["cls"] == "COM" else "Residential", long_form(a["address"]),
                       a.get("town") or "Halvard"] + vals)
        for i, w in enumerate([15, 12, 34, 13] + [9] * 12, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
        for row in ws.iter_rows(min_row=4, min_col=5):
            for c in row:
                c.number_format = "#,##0.0"
        ws.freeze_panes = "E4"
    wb.save(path)


# ---------------------------------------------------------------- weather, fuels, factors

def temperatures_csv(path, temps):
    r = np.random.default_rng(W.SEED + 71)
    rows = []
    for i, d in enumerate(temps["days"]):
        mx, mn = int(temps["tmax"][i]), int(temps["tmin"][i])
        if d.month in (6, 7, 8) and r.random() < 0.012:
            rows.append([STATION, iso(d), "", "", "M"])
            continue
        rows.append([STATION, iso(d), mx, mn, ""])
    write_csv(path, ["station", "date", "tmax_f", "tmin_f", "flag"], rows)


def fuel_equivalents_csv(path):
    rows = [["Propane", "gallon", 91500, "Furnace or boiler, existing", 85],
            ["Natural gas", "therm", 100000, "Furnace or boiler, existing", 82],
            ["Heating oil", "gallon", 138500, "Furnace or boiler, existing", 83],
            ["Electricity", "kWh", 3412, "Baseboard or wall heater", 100],
            ["Electricity", "kWh", 3412, "Air-source heat pump (seasonal)", 230]]
    write_csv(path, ["fuel", "unit", "btu_per_unit", "appliance", "seasonal_efficiency_pct"], rows)


FACTORS_PROPANE = {"Residential": dict(NOx=0.131, CO=0.082, PM25=0.0077, VOC=0.0055),
                   "Commercial/institutional": dict(NOx=0.142, CO=0.082, PM25=0.0077, VOC=0.0055)}
FACTORS_RWC_OTHER = dict(UNC=(230.8, 53.0), CNC=(140.8, 12.0), CAT=(107.0, 15.0), PEL=(15.9, 0.4), FPL=(149.0, 22.9),
                         HYD=(160.0, 28.0))


def factors_csv(path):
    rows = []
    for c in W.CL:
        scc, desc, code, eff, ef, med, sub = W.CLASSES[c]
        rows.append(["Residential wood combustion", scc, desc, "PM2.5", "%.1f" % ef, "lb/ton of wood burned"])
        rows.append(["Residential wood combustion", scc, desc, "CO", "%.1f" % FACTORS_RWC_OTHER[c][0], "lb/ton of wood burned"])
        rows.append(["Residential wood combustion", scc, desc, "VOC", "%.1f" % FACTORS_RWC_OTHER[c][1], "lb/ton of wood burned"])
    for cat, scc in (("Residential", "2104007000"), ("Commercial/institutional", "2103007000")):
        for p, v in FACTORS_PROPANE[cat].items():
            rows.append([cat + " propane combustion", scc, cat + " heating: liquefied petroleum gas",
                         "PM2.5" if p == "PM25" else p, "%.4f" % v, "lb/MMBtu heat input"])
    write_csv(path, ["category", "scc", "scc_description", "pollutant", "factor", "unit"], rows)


# ---------------------------------------------------------------- the Census files the state tool reads

def acs_csv(path, rem, which):
    rows = []
    for b in rem["bg20"]:
        total = b["hu"] - int(b["hu"] * 0.08)
        est = b["acs1923"] if which == "1923" else b["acs2024"]
        moe = b["moe1923"] if which == "1923" else b["moe2024"]
        tr = int(b["geoid"][5:11])
        rows.append(["1500000US" + b["geoid"], "Block Group %s; Census Tract %s; Halvard County; Montana" %
                     (b["geoid"][-1], ("%.2f" % (tr / 100.0)).rstrip("0").rstrip(".")),
                     total, int(total * 0.05) + 12, est, moe])
    write_csv(path, ["GEO_ID", "NAME", "B25040_001E", "B25040_001M", "B25040_008E", "B25040_008M"], rows)


def assessor_csv(path, rem):
    rows = []
    for b in rem["bg10"]:
        if b["inside"]:
            rows.append([b["geoid"], "Inside", b["inside"]])
        if b["hu"] - b["inside"]:
            rows.append([b["geoid"], "", b["hu"] - b["inside"]])
    write_csv(path, ["block_group", "maintenance_area", "housing_units"], rows)


def relationship_csv(path, rem):
    write_csv(path, ["GEOID_BG_20", "GEOID_BG_10", "HU_20_OVERLAP"],
              [[o["g20"], o["g10"], o["hu"]] for o in sorted(rem["ov"], key=lambda o: (o["g20"], o["g10"]))])


# ---------------------------------------------------------------- kept for other work

def distractor_csvs(paths, temps):
    r = np.random.default_rng(W.SEED + 41)
    rows = []
    for t, (a, b) in W.SEASONS.items():
        d = a
        while d <= b:
            i = temps["days"].index(d)
            cold = (temps["tmax"][i] + temps["tmin"][i]) / 2 < 22
            if (d.month in (11, 12, 1, 2) and r.random() < (0.16 if cold else 0.05)) or r.random() < 0.01:
                rows.append([iso(d), str(r.choice(["Stage 1", "Stage 1", "Stage 2"])), "Valley-wide",
                             "Stagnation forecast" if r.random() < 0.7 else "Monitor above 35 ug/m3"])
            d += dt.timedelta(days=1)
    write_csv(paths["curtail"], ["call_date", "stage", "zones", "basis"], rows)
    out = []
    for y in range(2019, 2026):
        for dist, base in (("Halvard Ranger District", 1240), ("Coldwater Ranger District", 1030)):
            n = int(base * (1 + 0.012 * (y - 2022)) * r.uniform(0.95, 1.05))
            out.append([y, dist, n, int(n * r.uniform(3.3, 3.6))])
    write_csv(paths["permits"], ["calendar_year", "ranger_district", "personal_use_permits", "cords_authorized"], out)
