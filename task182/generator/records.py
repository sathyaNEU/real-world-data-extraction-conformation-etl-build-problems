"""The data files of the pack, written from the simulated world: the manual dips, the loggers and their
installations, the barometric logger, the climate, the metered take, the landholder bore register, the water
quality results and the landholder contact log."""
import csv
import datetime as dt

import numpy as np
import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import readings as RD
import sim as S
import world as W

DIPS = "water_level_dips_2012-2026.csv"
LOGGERS = "logger_pressure_2015-2026.parquet"
INSTALLS = "logger_installations.csv"
BARO = "barometric_logger_2015-2026.csv"
CLIMATE = "daily_climate_1990-2026.csv"
TAKE = "pit_dewatering_2022-2026.csv"
REGISTER = "landholder_bore_register.xlsx"
QUALITY = "groundwater_quality_2012-2026.csv"
CONTACTS = "landholder_contact_log_2026.xlsx"

DIP_COLUMNS = ["entry_no", "reading_date", "reading_time", "site", "dtw", "units", "remarks", "officer"]
HEAD = Font(bold=True)
TITLE = Font(bold=True, size=12)
GREY = PatternFill("solid", fgColor="E7EAEE")


def write_csv(path, rows, columns, fmt=None):
    fmt = fmt or {}
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(columns)
        for r in rows:
            w.writerow([(fmt[c] % r[c]) if (c in fmt and r[c] != "") else r[c] for c in columns])
    return len(rows)


# ------------------------------------------------------------------ dips

def write_dips(path, rows):
    return write_csv(path, rows, DIP_COLUMNS, {"dtw": "%.2f"})


# ------------------------------------------------------------------ loggers

def write_loggers(path, logs):
    serial, stamp, kpa, temp = [], [], [], []
    for s, lab, t, p, tc in sorted(logs, key=lambda x: x[0]):
        serial += [s] * len(t)
        stamp.append(np.array([x.replace(tzinfo=None) for x in t], dtype="datetime64[s]"))
        kpa.append(p)
        temp.append(tc)
    table = pa.table({"logger_serial": pa.array(serial, pa.string()),
                      "timestamp_utc": pa.array(np.concatenate(stamp), pa.timestamp("s")),
                      "pressure_kpa": pa.array(np.concatenate(kpa), pa.float64()),
                      "temperature_c": pa.array(np.concatenate(temp), pa.float64())})
    pq.write_table(table, path, compression="zstd", row_group_size=200_000, use_dictionary=["logger_serial"])
    return table.num_rows


def write_installs(path, installs):
    rows = []
    notes = {"2041881": "removed: no data since 2019-02-11 (battery); replaced by 2190446",
             "2041925": "removed at scheduled download, end of service life; replaced by 2213378 same visit",
             "2190446": "replacement for 2041881; cable re-cut, sensor 0.25 m higher",
             "2213378": "replacement for 2041925; new cable"}
    for i in sorted(installs, key=lambda x: (W.BY_LABEL[x["label"]]["code"], x["installed"])):
        rows.append(dict(logger_serial=i["serial"], site=W.BY_LABEL[i["label"]]["code"], installed_local=i["installed"],
                         removed_local=i["removed"], sensor_depth_below_mp_m="%.2f" % i["sensor"],
                         logger_type="absolute pressure (unvented), 0-300 kPa", comment=notes.get(i["serial"], "")))
    rows.append(dict(logger_serial=W.BARO_SERIAL, site="KV-SITE-OFFICE", installed_local=W.BARO_FROM, removed_local="",
                     sensor_depth_below_mp_m="", logger_type="barometric (absolute pressure), 0-120 kPa",
                     comment="site barometric logger, in the environment store at the site office"))
    cols = ["logger_serial", "site", "installed_local", "removed_local", "sensor_depth_below_mp_m", "logger_type", "comment"]
    return write_csv(path, rows, cols)


def write_baro(path, t, p, temp):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["timestamp_utc", "pressure_kpa", "air_temperature_c"])
        for a, b, c in zip(t, p, temp):
            w.writerow([a.strftime("%Y-%m-%dT%H:%M:%SZ"), "%.3f" % b, "%.1f" % c])
    return len(t)


# ------------------------------------------------------------------ climate and take

def write_climate(path, clim):
    i0, i1 = S.idx(W.CLIMATE_START), S.idx(W.LAST_DAY)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["date", "rain_mm", "morton_apet_mm", "tmax_c", "tmin_c"])
        for i in range(i0, i1 + 1):
            w.writerow([S.DATES[i].isoformat(), "%.1f" % clim["rain"][i], "%.1f" % clim["pet"][i],
                        "%.1f" % clim["tmax"][i], "%.1f" % clim["tmin"][i]])
    return i1 - i0 + 1


METERS = {"PS1": "MAG-22-0417", "PS2": "MAG-23-0052", "AD01": "MAG-23-0108", "AD02": "MAG-23-0109",
          "AD03": "MAG-23-0311", "AD04": "MAG-24-0026"}


def write_take(path, q):
    rows = []
    for i in range(S.idx(W.TAKE_START), S.idx(W.LAST_DAY) + 1):
        for sid, name, start in W.SOURCES:
            if S.DATES[i] >= dt.date.fromisoformat(start):
                rows.append([S.DATES[i].isoformat(), sid, name, METERS[sid], "%.3f" % q[sid][i]])
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["date", "source_id", "source", "meter_serial", "volume_ml"])
        w.writerows(rows)
    return len(rows)


# ------------------------------------------------------------------ the register

BORE_YEAR = {"CM1": 1979, "CM2": 1986, "CM3": 1974, "CM4": 1991, "CM5": 1983, "A1": 1968, "A2": 1972, "A3": 1965,
             "A4": 1988, "A5": 1977, "A6": 1969, "A7": 1981, "A8": 1962, "A9": 1966, "B1": 1984, "B2": 1976,
             "B3": 1993, "B4": 1971, "RA1": 1987, "RA2": 1990, "RB1": 1989, "MA1": 2011, "MA2": 2011, "MC1": 2011,
             "MC2": 2011, "MC3": 2012, "MC4": 2012}
YIELD = {"CM1": 0.6, "CM2": 0.45, "CM3": 0.7, "CM4": 0.35, "CM5": 0.5, "A1": 3.2, "A2": 2.6, "A3": 2.9, "A4": 2.1,
         "A5": 2.4, "A6": 1.8, "A7": 2.2, "A8": 3.8, "A9": 3.5, "B1": 1.1, "B2": 0.8, "B3": 0.9, "B4": 1.3}
EC = {"CM1": 5480, "CM2": 6210, "CM3": 4930, "CM4": 7120, "CM5": 5860, "A1": 1240, "A2": 980, "A3": 1110, "A4": 1350,
      "A5": 1020, "A6": 1490, "A7": 1270, "A8": 860, "A9": 910, "B1": 1640, "B2": 1820, "B3": 1550, "B4": 1390,
      "RA1": 1050, "RA2": 1180, "RB1": 1710, "MA1": 1430, "MA2": 1380, "MC1": 6020, "MC2": 5770, "MC3": 6340, "MC4": 5590}
CASING = {"alluvium": "PVC 100 mm, slotted", "basalt": "steel 150 mm, open hole below casing",
          "coal": "steel 150 mm, slotted"}
MP_DESC = "top of casing, north side"


def _sheet_head(ws, title, note, row_cols):
    ws["A1"] = title
    ws["A1"].font = TITLE
    ws["A2"] = note
    ws["A2"].alignment = Alignment(wrap_text=False)
    for j, (name, width) in enumerate(row_cols, 1):
        c = ws.cell(row=4, column=j, value=name)
        c.font = HEAD
        c.fill = GREY
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.column_dimensions[get_column_letter(j)].width = width
    ws.row_dimensions[4].height = 30
    ws.freeze_panes = "B5"


def write_register(path, baseline):
    """baseline: label -> (date, depth below the measuring point, m)."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Landholder bores"
    cols = [("Bore", 10), ("Registered number", 12), ("Landholder's name for the bore", 20), ("Property", 16),
            ("Owner", 30), ("Aquifer", 34), ("Aquifer class", 15), ("Easting (MGA55)", 11), ("Northing (MGA55)", 12),
            ("Ground level (m AHD)", 11), ("Drilled", 8), ("Depth (m)", 8), ("Screen from (m bgl)", 9),
            ("Screen to (m bgl)", 9), ("Construction", 30), ("Pump", 20), ("Baseline assessment", 12),
            ("Baseline static water level (m below MP)", 14), ("Baseline yield (L/s)", 10), ("Baseline EC (uS/cm)", 10),
            ("Complaint received (MG-02 7.1)", 13)]
    _sheet_head(ws, "Kelvale Mine: landholder bore register (MG-02)",
                "The landholder bores within the scope of MG-02 1.2, with each bore's baseline assessment as recorded "
                "(MG-02 5.1). The register holds no current water levels and no assessment results.", cols)
    r = 5
    for lab in sorted(W.LANDHOLDER, key=lambda k: W.BY_LABEL[k]["code"]):
        b = W.BY_LABEL[lab]
        unit, cls = W.UNITS[b["unit"]]
        bd, depth = baseline[lab]
        vals = [b["code"], b["rn"], b["name"], b["prop"], b["owner"], unit, cls, int(b["xy"][0]), int(b["xy"][1]),
                b["gl"], BORE_YEAR[lab], b["depth"], b["screen"][0], b["screen"][1], CASING[b["unit"]], b["pump"],
                bd, depth, YIELD[lab], EC[lab], W.COMPLAINTS.get(lab)]
        for j, v in enumerate(vals, 1):
            if v in ("", None):
                continue
            c = ws.cell(row=r, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "dd/mm/yyyy"
            elif j in (10, 18):
                c.number_format = "0.00"
            elif j in (12, 13, 14, 19):
                c.number_format = "0.0"
        r += 1
    ws.cell(row=r + 1, column=1, value="Maintained by %s, Environment. Revised 09/10/2026." % W.PEOPLE["env"]).font = Font(italic=True, size=9)
    ws.auto_filter.ref = "A4:%s%d" % (get_column_letter(len(cols)), r - 1)

    ws2 = wb.create_sheet("Measuring points")
    cols2 = [("Bore", 10), ("Measuring point", 30), ("MP elevation (m AHD)", 12), ("In force from", 12),
             ("In force to", 12), ("Survey note", 70)]
    _sheet_head(ws2, "Measuring points (surveyed, m AHD)",
                "A dip is a depth to water below the measuring point in force on the reading date.", cols2)
    r = 5
    for b in sorted(W.BORES, key=lambda x: x["code"]):
        lab = b["label"]
        mp0 = round(b["gl"] + W.MP_STICKUP[lab], 3)
        first = dt.date(2011, 11, 22) if b["kind"] == "mine" else dt.date(2012, 2, 14)
        if lab in W.MP_RESURVEY:
            when, stick, note = W.MP_RESURVEY[lab]
            rows = [(MP_DESC, mp0, first, when - dt.timedelta(days=1), "EIS baseline survey"),
                    (note.split(";")[1].strip() if ";" in note else MP_DESC, round(b["gl"] + stick, 3), when, None,
                     "resurveyed: " + note.split(";")[0])]
        else:
            rows = [(MP_DESC, mp0, first, None, "EIS baseline survey" if b["kind"] != "mine" else "as-constructed survey")]
        for desc, elev, fr, to, note in rows:
            vals = [b["code"], desc, elev, fr, to, note]
            for j, v in enumerate(vals, 1):
                if v in ("", None):
                    continue
                c = ws2.cell(row=r, column=j, value=v)
                if isinstance(v, dt.date):
                    c.number_format = "dd/mm/yyyy"
                elif j == 3:
                    c.number_format = "0.000"
            r += 1

    ws3 = wb.create_sheet("Network bores")
    cols3 = [("Bore", 10), ("Registered number", 12), ("Type", 26), ("Aquifer", 34), ("Aquifer class", 15),
             ("Easting (MGA55)", 11), ("Northing (MGA55)", 12), ("Ground level (m AHD)", 11), ("Drilled", 8),
             ("Depth (m)", 8), ("Screen from (m bgl)", 9), ("Screen to (m bgl)", 9), ("Note", 46)]
    _sheet_head(ws3, "Other bores in the monitoring network",
                "State reference bores (read by the field team under arrangement with the department) and the mine's "
                "own monitoring bores; outside MG-02.", cols3)
    r = 5
    for b in sorted(W.BORES, key=lambda x: x["code"]):
        if b["kind"] == "landholder":
            continue
        unit, cls = W.UNITS[b["unit"]]
        typ = "state reference bore" if b["kind"] == "reference" else "mine monitoring bore"
        note = {"reference": "outside the EIS predicted drawdown; %s" % b["prop"],
                "mine": "mining lease, pit perimeter network"}[b["kind"]]
        vals = [b["code"], b["rn"], typ, unit, cls, int(b["xy"][0]), int(b["xy"][1]), b["gl"], BORE_YEAR[b["label"]],
                b["depth"], b["screen"][0], b["screen"][1], note]
        for j, v in enumerate(vals, 1):
            c = ws3.cell(row=r, column=j, value=v)
            if j == 8:
                c.number_format = "0.00"
            elif j in (10, 11, 12):
                c.number_format = "0.0"
        r += 1
    wb.save(path)


# ------------------------------------------------------------------ water quality (field and laboratory results)

def write_quality(path):
    r = W.rng("quality")
    rows = []
    n = 0
    rounds = [dt.date(y, m, 1) for (y, m) in W.EIS_ROUNDS]
    for y in range(2014, 2027):
        for m in (3, 9):
            if dt.date(y, m, 1) > dt.date(2014, 6, 30) and dt.date(y, m, 1) <= dt.date(2026, 9, 1):
                rounds.append(dt.date(y, m, 1))
    for rd in rounds:
        for b in sorted(W.BORES, key=lambda x: x["code"]):
            lab = b["label"]
            if r.random() < 0.04:
                continue
            day = rd + dt.timedelta(days=int(r.integers(6, 20)))
            ec = EC[lab] * float(np.exp(r.normal(0, 0.05))) * (1 + 0.004 * (day.year - 2012) * (b["unit"] == "coal"))
            tds = ec * (0.64 if b["unit"] != "coal" else 0.67)
            cl = ec * (0.21 if b["unit"] != "coal" else 0.31) * float(np.exp(r.normal(0, 0.04)))
            na = cl * 0.62 * float(np.exp(r.normal(0, 0.05)))
            hco3 = (310 if b["unit"] == "basalt" else 240 if b["unit"] == "alluvium" else 520) * float(np.exp(r.normal(0, 0.08)))
            ca = (58 if b["unit"] != "coal" else 46) * float(np.exp(r.normal(0, 0.1)))
            mg = (41 if b["unit"] == "basalt" else 29) * float(np.exp(r.normal(0, 0.1)))
            so4 = (35 if b["unit"] != "coal" else 18) * float(np.exp(r.normal(0, 0.15)))
            n += 1
            rows.append(dict(sample_id="KVGW-%05d" % (n * 7 + 31), site=b["code"], sample_date=day.isoformat(),
                             ec_us_cm=int(round(ec)), ph="%.2f" % (7.2 + 0.3 * (b["unit"] == "basalt") + r.normal(0, 0.12)),
                             tds_mg_l=int(round(tds)), na_mg_l=int(round(na)),
                             k_mg_l="%.1f" % (4 + 3 * r.random()), ca_mg_l=int(round(ca)), mg_mg_l=int(round(mg)),
                             cl_mg_l=int(round(cl)), so4_mg_l=int(round(so4)), hco3_mg_l=int(round(hco3)),
                             lab_batch="EB%02d%02d-%03d" % (day.year % 100, day.month, int(r.integers(100, 999)))))
    cols = ["sample_id", "site", "sample_date", "ec_us_cm", "ph", "tds_mg_l", "na_mg_l", "k_mg_l", "ca_mg_l", "mg_mg_l",
            "cl_mg_l", "so4_mg_l", "hco3_mg_l", "lab_batch"]
    return write_csv(path, rows, cols)


# ------------------------------------------------------------------ the landholder contact log (2026)

def contact_rows():
    P = W.PEOPLE
    E = [
        ("05/01/2026", "09:12", "Phone", "Bellbird Downs", "office", "Dust", "Dust over the eastern boundary fence from the haul road on 3 and 4 January.", "Water cart run doubled on the eastern haul road; called back 06/01.", P["env"]),
        ("13/01/2026", "14:40", "Email", "Tondara", "owner's office", "Access", "Requested the date of the next bore visit so the dogs can be tied up.", "Run dates sent for the year.", P["env"]),
        ("22/01/2026", "07:55", "Phone", "Saltbush Flat", P["walker"], "Blasting", "Asked for the blast schedule for February; cattle being moved near the lease boundary.", "Added to the blast notification list.", P["env"]),
        ("03/02/2026", "11:20", "Visit", "Ghost Gum", P["lewis"], "Road", "Grid on the shared access road damaged by a contractor's truck.", "Contractor notified; grid repaired 09/02.", P["env"]),
        ("19/02/2026", "16:05", "Phone", "Coolibah Springs", "manager", "Water", "Asked whether the mine draws from the lagoon reach of the creek.", "Explained the licensed take is from the pit and the dewatering bores only; offered a site visit.", P["hydro"]),
        ("02/03/2026", "08:45", "Email", "Gidgee Creek", "office", "Monitoring", "Asked for copies of the quarterly levels at the north and shed bores.", "Sent the levels to 31/12/2025.", P["env"]),
        ("16/03/2026", "10:30", "Phone", "Wilga Vale", "owner's agent", "Noise", "Night noise from the dragline audible at the homestead in still conditions.", "Noise monitor placed 18/03 to 01/04; results sent.", P["env"]),
        ("08/04/2026", "13:15", "Visit", "Yarrowmere", "manager", "Monitoring", "Logger visit at the house bore; manager asked how the readings are used.", "Explained the network and the MG-02 assessments.", P["tech"]),
        ("27/04/2026", "09:50", "Phone", "Brolga Plains", "office", "Stock", "Cattle got through the lease fence near the yards bore track.", "Fence repaired 28/04.", P["env"]),
        ("14/05/2026", "15:35", "Email", "Bottletree", "office", "Blasting", "Dust and fume from a blast on 13 May drifted over the ridge paddock.", "Blast log checked; wind conditions reviewed with the drill and blast supervisor.", P["env"]),
        ("03/06/2026", "08:10", "Phone", "Saltbush Flat", P["walker"], "Water", "Creek has stopped running at the crossing; asked when it last stopped.", "Told him the creek gauge records are with the department.", P["env"]),
        ("22/06/2026", "12:00", "Visit", "Kurrajong Park", "manager", "Monitoring", "Asked for the ridge paddock bore to be dipped while the pump is serviced.", "Dipped 23/06; levels sent.", P["tech"]),
        ("09/07/2026", "10:25", "Email", "Lancewood Flat", "owner's office", "Monitoring", "Headworks at the windmill bore need the casing extension painted.", "Logged for the next run.", P["env"]),
        ("28/07/2026", "17:20", "Phone", "Cypress Ridge", "trust office", "Water", "Asked for the levels at the creek bore for the trust's annual report.", "Sent the levels to 30/06/2026.", P["env"]),
        ("03/08/2026", "07:40", "Phone", "Saltbush Flat", P["walker"], "Bore complaint", "House bore sucking air since the last week of July; pump cutting out in the afternoons. Wants to know if the mine has taken his water.", "Recorded as a complaint under MG-02 7.1; fortnightly dips from 10 August.", P["env"]),
        ("06/08/2026", "11:05", "Visit", "Saltbush Flat", P["walker"], "Bore complaint", "Site visit with the field technician; pump lowered by the landholder's contractor in July.", "Explained the assessment under MG-02 and the timing.", P["hydro"]),
        ("19/08/2026", "14:30", "Email", "Brolga Plains", "office", "Bore complaint", "Yards bore sucking air at the windmill; trough not filling for two days in seven.", "Recorded as a complaint under MG-02 7.1; acknowledged 20/08.", P["env"]),
        ("25/08/2026", "09:15", "Phone", "Bellbird Downs", "office", "Dust", "Dust from the topsoil stockpile on 24 August.", "Stockpile watered; called back.", P["env"]),
        ("02/09/2026", "08:20", "Visit", "Ghost Gum", P["lewis"], "Bore complaint", "Garden bore sucking air; pump running on and off when the field team arrived.", "Recorded as a complaint under MG-02 7.1.", P["tech"]),
        ("07/09/2026", "16:40", "Phone", "Ghost Gum", P["lewis"], "Bore complaint", "Asked whether neighbours have the same problem.", "Told him three other landholders have raised bores and each is being assessed.", P["env"]),
        ("15/09/2026", "10:55", "Email", "Bottletree", "office", "Bore complaint", "Ridge bore sucking air at the windmill since early September; stock water carted to the ridge paddock.", "Recorded as a complaint under MG-02 7.1.", P["env"]),
        ("21/09/2026", "13:10", "Phone", "Yarrowmere", "manager", "Monitoring", "Asked for the logger readings at the house bore and the Ten Mile bore.", "Will be sent after the October download.", P["env"]),
        ("30/09/2026", "15:25", "Email", "Brolga Plains", "office", "Bore complaint", "Asked when the assessment will be finished.", "Assessments to the executive team on 26 October; written reply to follow.", P["hydro"]),
        ("06/10/2026", "09:30", "Phone", "Saltbush Flat", P["walker"], "Bore complaint", "Asked for the result of the assessment.", "Told him the assessment is with the executive team on 26 October.", P["env"]),
        ("08/10/2026", "11:45", "Email", "Bottletree", "office", "Bore complaint", "Asked for the September readings at the ridge bore.", "Readings to follow with the assessment letter.", P["env"]),
    ]
    rows = [dict(date=dt.datetime.strptime(a, "%d/%m/%Y").date(), time=b, contact=c, property=d, contact_person=e,
                 topic=f, summary=g, action=h, logged_by=i) for a, b, c, d, e, f, g, h, i in E]
    r = W.rng("contacts")
    routine = [("Blasting", "Blast notification sent for the coming week.", "Notification list"),
               ("Monitoring", "Monthly bore run notice sent.", "Monitoring"),
               ("Road", "Haul road crossing closed for maintenance on the shared access road.", "Notice"),
               ("Dust", "Dust monitor results for the month posted to the community page.", "Community")]
    day = dt.date(2026, 1, 8)
    while day <= dt.date(2026, 10, 8):
        if r.random() < 0.28:
            t, s, who = routine[int(r.integers(0, len(routine)))]
            props = ["Saltbush Flat", "Brolga Plains", "Wilga Vale", "Ghost Gum", "Lancewood Flat", "Bellbird Downs",
                     "Coolibah Springs", "Cypress Ridge", "Yarrowmere", "Tondara", "Bluebush Downs", "Gidgee Creek",
                     "Kurrajong Park", "Bottletree"]
            rows.append(dict(date=day, time="%02d:%02d" % (8 + int(r.integers(0, 8)), int(r.integers(0, 12)) * 5),
                             contact="Email" if r.random() < 0.7 else "Letter", property="all neighbours" if t != "Road" else props[int(r.integers(0, len(props)))],
                             contact_person="", topic=t, summary=s, action=who, logged_by=P["env"]))
        day += dt.timedelta(days=int(r.integers(2, 6)))
    rows.sort(key=lambda x: (x["date"], x["time"]))
    return rows


def write_contacts(path):
    rows = contact_rows()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contacts 2026"
    cols = [("Date", 11), ("Time", 7), ("Contact", 9), ("Property", 18), ("Contact person", 18), ("Topic", 14),
            ("Summary", 70), ("Action", 60), ("Logged by", 16)]
    _sheet_head(ws, "Kelvale Mine: landholder and community contact log, 2026",
                "Calls, emails, letters and visits from neighbours, as logged by the environment team.", cols)
    for i, rr in enumerate(rows, 5):
        vals = [rr["date"], rr["time"], rr["contact"], rr["property"], rr["contact_person"], rr["topic"], rr["summary"],
                rr["action"], rr["logged_by"]]
        for j, v in enumerate(vals, 1):
            if v in ("", None):
                continue
            c = ws.cell(row=i, column=j, value=v)
            if j == 1:
                c.number_format = "dd/mm/yyyy"
            if j in (7, 8):
                c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.auto_filter.ref = "A4:I%d" % (4 + len(rows))
    wb.save(path)
    return len(rows)
