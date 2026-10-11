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
    notes = {"2041881": "low battery warning at the 2019-02-11 visit; pulled for repair; replaced by 2190446",
             "2041925": "removed at scheduled download, end of service life; replaced by 2213378 same visit",
             "2190446": "replacement for 2041881; cable re-cut, sensor 0.25 m higher",
             "2213378": "replacement for 2041925; new cable",
             "2041956": "battery flat 2018-08-27, new battery at the October 2018 download; out 2023-05-09 to "
                        "2023-05-22 for headworks repair",
             "2041964": "deep sensor for the pit perimeter; out 2024-06-11 to 2024-06-20 for perimeter road works"}
    # the pit perimeter coal-measure bore needs a deeper sensor: about 50 m of water over it before dewatering
    ranges = {"2041964": "0-1000 kPa"}
    for i in sorted(installs, key=lambda x: (W.BY_LABEL[x["label"]]["code"], x["installed"])):
        rows.append(dict(logger_serial=i["serial"], site=W.BY_LABEL[i["label"]]["code"], installed_local=i["installed"],
                         removed_local=i["removed"], sensor_depth_below_mp_m="%.2f" % i["sensor"],
                         logger_type="absolute pressure (unvented), %s" % ranges.get(i["serial"], "0-300 kPa"),
                         comment=notes.get(i["serial"], "")))
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


TAKE_COLUMNS = ["date", "source_id", "source", "meter_serial", "volume_ml", "volume_basis", "comment"]
# AD03 and AD04 came on in March 2023 with AD01 and AD02, on temporary pumps through temporary meters, until their
# permanent pumps and meters went in on the dates in world.SOURCES. What they pumped before then came out of the pit
# sumps on the same day, so the daily take is the simulated take to the litre.
EARLY = {"AD03": ("2023-03-27", "MAG-23-0110", "PS2"), "AD04": ("2023-03-29", "MAG-23-0111", "PS2")}
OFF_REASONS = {"PS": ["sump pump pulled for repair", "pump off: cable fault", "pump off: sump relocated"],
               "AD": ["pump off: scheduled maintenance", "pump tripped overnight, reset next day", "pump off: cable fault",
                      "pump off: generator service"]}
LOW_REASONS = {"PS": ["pump tripped, restarted", "power dip, pump restarted", "run hours reduced, sump low"],
               "AD": ["pump tripped, restarted", "pump tripped on high temperature", "power dip, pump restarted"]}


def take_rows(q):
    """The meter records, day by day: {date index: {source: [thousandths of a ML, meter, basis, comment]}}, with
    every day's total equal to the simulated take, and the (day, source) values that must not be nudged."""
    r = W.rng("take-records")
    i0, i1 = S.idx(W.TAKE_START), S.idx(W.LAST_DAY)
    start = {sid: S.idx(dt.date.fromisoformat(s)) for sid, _, s in W.SOURCES}
    days = {i: {sid: [int(round(q[sid][i] * 1000)), METERS[sid], "meter", ""] for sid, _, _ in W.SOURCES
                if i >= start[sid]} for i in range(i0, i1 + 1)}
    touched = {i: set() for i in days}
    fixed = set()
    # the advance bores on temporary pumps from March 2023
    for sid, (s0, meter, partner) in EARLY.items():
        first = S.idx(dt.date.fromisoformat(s0))
        for i in range(first, start[sid]):
            v = 0 if (r.random() < 0.3 and i > first) else int(r.integers(140, 430))
            other = partner if days[i][partner][0] >= v + 600 else ("PS1" if partner == "PS2" else "PS2")
            days[i][other][0] -= v
            days[i][sid] = [v, meter, "meter", "temporary pump" if i == first else ""]
            touched[i] |= {sid, other}
            if v == 0:
                fixed.add((i, sid))
        days[start[sid]][sid][3] = "permanent pump installed; meter %s in service" % METERS[sid]
    # pumps off for the day (what the source would have pumped went through its neighbour) and short days
    for i in range(i0 + 10, i1 + 1):
        for sid in list(days[i]):
            v = days[i][sid][0]
            if i - start[sid] < 10 or sid in touched[i] or v == 0:
                continue
            recent = [days[j][sid][0] for j in range(i - 10, i) if sid in days[j]]
            if v >= 0.35 * float(np.median(recent)):
                continue
            fam = sid[:2]
            mates = [m for m in days[i] if m[:2] == fam and m != sid and m not in touched[i] and days[i][m][0] > 600]
            if mates and r.random() < 0.55:
                m = mates[int(r.integers(0, len(mates)))]
                days[i][m][0] += v
                days[i][sid][0] = 0
                days[i][sid][3] = OFF_REASONS[fam][int(r.integers(0, len(OFF_REASONS[fam])))]
                touched[i] |= {sid, m}
                fixed.add((i, sid))
            elif r.random() < 0.5:
                days[i][sid][3] = LOW_REASONS[fam][int(r.integers(0, len(LOW_REASONS[fam])))]
                touched[i].add(sid)
    # telemetry outages: the volume over the outage from the totaliser, split evenly over its days
    srcs = [x[0] for x in W.SOURCES]
    for _ in range(9):
        sid = srcs[int(r.integers(0, len(srcs)))]
        n = int(r.integers(2, 6))
        a = int(r.integers(max(start[sid] + 20, i0 + 30), i1 - 10))
        block = list(range(a, a + n))
        if any(sid in touched[i] or len(days[i]) < 3 for i in block):
            continue
        tot = sum(days[i][sid][0] for i in block)
        split = [tot // n + (k < tot % n) for k in range(n)]
        mates = {}
        for k, i in enumerate(block):
            d = split[k] - days[i][sid][0]
            cand = [m for m in days[i] if m != sid and m not in touched[i] and days[i][m][0] > abs(d) + 600]
            if cand:
                mates[i] = (max(cand, key=lambda x: days[i][x][0]), d)
        if len(mates) < n:
            continue
        for k, i in enumerate(block):
            m, d = mates[i]
            days[i][m][0] -= d
            days[i][sid][0] = split[k]
            days[i][sid][2] = "estimated"
            days[i][sid][3] = "telemetry outage; volume from the totaliser, split evenly" if k == 0 else ""
            touched[i] |= {sid, m}
            fixed.add((i, sid))
    # meter faults: the volume estimated from the pump's run hours
    for _ in range(5):
        sid = srcs[int(r.integers(0, len(srcs)))]
        n = int(r.integers(3, 9))
        a = int(r.integers(max(start[sid] + 20, i0 + 30), i1 - 10))
        block = list(range(a, a + n))
        if any(sid in touched[i] for i in block):
            continue
        for k, i in enumerate(block):
            days[i][sid][2] = "estimated"
            days[i][sid][3] = "meter fault; volume from pump run hours" if k == 0 else ""
            touched[i].add(sid)
    for i in days:
        assert sum(v[0] for v in days[i].values()) == sum(int(round(q[s][i] * 1000)) for s in srcs if i >= start[s])
        assert all(v[0] >= 0 for v in days[i].values())
    return days, fixed


def _take_csv(days, simple=False):
    import io
    names = {sid: name for sid, name, _ in W.SOURCES}
    order = [x[0] for x in W.SOURCES]
    fh = io.StringIO()
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(TAKE_COLUMNS[:5] if simple else TAKE_COLUMNS)
    for i in sorted(days):
        for sid in sorted(days[i], key=order.index):
            v, meter, basis, comment = days[i][sid]
            row = [S.DATES[i].isoformat(), sid, names[sid], meter, "%.3f" % (v / 1000.0)]
            w.writerow(row if simple else row + [basis, comment])
    return fh.getvalue()


def daily_take(text):
    """The daily total the way the analysis reads the file (pandas, summed by date)."""
    import io
    import pandas as pd
    t = pd.read_csv(io.StringIO(text))
    return t.groupby("date")["volume_ml"].sum()


def old_take_csv(q):
    """The file as first cut (one row per source in service, its simulated volume): the reference for the daily
    totals the re-split must keep."""
    import io
    fh = io.StringIO()
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(TAKE_COLUMNS[:5])
    for i in range(S.idx(W.TAKE_START), S.idx(W.LAST_DAY) + 1):
        for sid, name, start in W.SOURCES:
            if S.DATES[i] >= dt.date.fromisoformat(start):
                w.writerow([S.DATES[i].isoformat(), sid, name, METERS[sid], "%.3f" % q[sid][i]])
    return fh.getvalue()


def kahan(xs):
    """pandas sums a group the compensated way, in file order; this is the same arithmetic."""
    s = c = 0.0
    for v in xs:
        y = v - c
        t = s + y
        c = t - s - y
        s = t
    return s


def write_take(path, q):
    days, fixed = take_rows(q)
    want = daily_take(old_take_csv(q))
    order = [x[0] for x in W.SOURCES]
    # a day's total is the same number of litres either way; where the compensated sum of the printed volumes lands
    # on a different double, move the fewest litres between two of the day's meters that bring it back
    for d in want.index:
        i = S.idx(dt.date.fromisoformat(d))
        srcs = sorted(days[i], key=order.index)
        vals = [days[i][s][0] for s in srcs]
        if kahan([float("%.3f" % (v / 1000.0)) for v in vals]) == want[d]:
            continue
        free = [j for j, s in enumerate(srcs) if vals[j] > 50 and (i, s) not in fixed]
        best = None
        for k in range(1, 400):
            for a_ in free:
                for b_ in free:
                    if a_ == b_ or vals[a_] - k < 0:
                        continue
                    v2 = list(vals)
                    v2[a_] -= k
                    v2[b_] += k
                    if kahan([float("%.3f" % (v / 1000.0)) for v in v2]) == want[d]:
                        best = v2
                        break
                if best:
                    break
            if best:
                break
        assert best, "no split reproduces the daily take on %s" % d
        for j, s in enumerate(srcs):
            days[i][s][0] = best[j]
    text = _take_csv(days)
    got = daily_take(text)
    assert list(got.index) == list(want.index) and (got.values == want.values).all(), "daily take moved"
    with open(path, "w", newline="") as fh:
        fh.write(text)
    return text.count("\n") - 1


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
                "(MG-02 5.1).", cols)
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

QUALITY_COLUMNS = ["sample_id", "site", "sample_date", "ec_us_cm", "ph", "tds_mg_l", "na_mg_l", "k_mg_l", "ca_mg_l",
                   "mg_mg_l", "cl_mg_l", "so4_mg_l", "hco3_mg_l", "f_mg_l", "no3_n_mg_l", "fe_mg_l", "lab_batch"]
SAMPLE_ORDER = ["MC1", "MC2", "MC3", "MC4", "MA1", "MA2", "CM1", "CM3", "CM4", "CM2", "A1", "A2", "A5", "A3", "A4", "A6",
                "A7", "A8", "A9", "RA2", "CM5", "B3", "B2", "B1", "B4", "RA1", "RB1"]


def quality_rounds():
    """Sampling campaigns: (round month, bores). The consultant sampled every bore each EIS quarter; since September
    2014 the mine's bores are sampled quarterly, the landholder bores in March and September and the reference bores
    in September."""
    out = [((y, m), list(SAMPLE_ORDER)) for (y, m) in W.EIS_ROUNDS]
    y, m = 2014, 9
    while (y, m) <= (2026, 9):
        if m in (3, 6, 9, 12):
            sel = [x for x in SAMPLE_ORDER if W.BY_LABEL[x]["kind"] == "mine"
                   or (W.BY_LABEL[x]["kind"] == "landholder" and m in (3, 9))
                   or (W.BY_LABEL[x]["kind"] == "reference" and m == 9)]
            out.append(((y, m), sel))
        y, m = (y + (m == 12), m % 12 + 1)
    return out


def write_quality(path, hd):
    """Field and laboratory results. A campaign samples about six bores a field day from early in the round month,
    so a long one runs into the next month; the samples go to the laboratory every two or three field days, one
    batch each, and the sample numbers skip the duplicates and blanks sent with each batch. The pit perimeter coal
    measure bores take up sulfate, salt and iron and lose a little pH as dewatering draws them down."""
    r = W.rng("quality-2")
    rows = []
    serial = 37
    eis_no = 0
    for (y, m), bores in quality_rounds():
        eis = (y, m) in [tuple(x) for x in W.EIS_ROUNDS]
        d0 = dt.date(y, m, int(r.integers(3, 25)) if (y, m) != (2026, 9) else 1)
        field_days, d = [], d0
        per_day = int(r.integers(5, 8))
        need = -(-len(bores) // per_day)
        while len(field_days) < need:
            if d.weekday() < 5 and r.random() > 0.15:
                field_days.append(d)
            d += dt.timedelta(days=1)
        batches = []
        k = 0
        while k < len(field_days):
            n = int(r.integers(2, 4))
            batches.append(field_days[k:k + n])
            k += n
        batch_of = {}
        for grp in batches:
            last = grp[-1] + dt.timedelta(days=1)
            code = "EB%02d%02d-%03d" % (last.year % 100, last.month, int(r.integers(100, 999)))
            for fd in grp:
                batch_of[fd] = code
        prev_batch = None
        for j, lab in enumerate(bores):
            day = field_days[min(j // per_day, len(field_days) - 1)]
            if r.random() < 0.035:
                continue
            b = W.BY_LABEL[lab]
            unit = b["unit"]
            dd = 0.0
            if b["kind"] == "mine" and unit == "coal" and day >= W.TAKE_START:
                dd = max(float(hd[lab]["dd"][S.idx(day)]), 0.0)
            ec = EC[lab] * float(np.exp(r.normal(0, 0.05))) * (1 + 0.004 * (day.year - 2012) * (unit == "coal")) \
                * (1 + 0.005 * dd)
            tds = ec * (0.64 if unit != "coal" else 0.67)
            cl = ec * (0.21 if unit != "coal" else 0.31) * float(np.exp(r.normal(0, 0.04)))
            na = cl * 0.62 * float(np.exp(r.normal(0, 0.05)))
            hco3 = (310 if unit == "basalt" else 240 if unit == "alluvium" else 520) * float(np.exp(r.normal(0, 0.08)))
            ca = (58 if unit != "coal" else 46) * float(np.exp(r.normal(0, 0.1)))
            mgv = (41 if unit == "basalt" else 29) * float(np.exp(r.normal(0, 0.1)))
            so4 = (35 if unit != "coal" else 2.2) * float(np.exp(r.normal(0, 0.15 if unit != "coal" else 0.6))) \
                + 4.5 * max(dd - 3.0, 0.0)
            ph = {"alluvium": 7.2, "basalt": 7.5, "coal": 7.9}[unit] + r.normal(0, 0.12) - 0.012 * dd
            f = {"alluvium": 0.25, "basalt": 0.4, "coal": 1.4}[unit] * float(np.exp(r.normal(0, 0.2)))
            no3 = {"alluvium": 0.6, "basalt": 0.4, "coal": 0.004}[unit] * float(np.exp(r.normal(0, 0.7)))
            fe = {"alluvium": 0.03, "basalt": 0.04, "coal": 0.9}[unit] * float(np.exp(r.normal(0, 0.6))) + 0.02 * dd
            if eis:
                eis_no += 1
                sid = "EIS-%04d" % eis_no
            else:
                if prev_batch is not None and batch_of[day] != prev_batch:
                    serial += int(r.integers(1, 3))
                serial += 1
                sid = "KVGW-%05d" % serial
            prev_batch = batch_of[day]
            rows.append(dict(sample_id=sid, site=b["code"], sample_date=day.isoformat(), ec_us_cm=int(round(ec)),
                             ph="%.2f" % ph, tds_mg_l=int(round(tds)), na_mg_l=int(round(na)),
                             k_mg_l="%.1f" % (4 + 3 * r.random()), ca_mg_l=int(round(ca)), mg_mg_l=int(round(mgv)),
                             cl_mg_l=int(round(cl)), so4_mg_l=("<1" if so4 < 1 else str(int(round(so4)))),
                             hco3_mg_l=int(round(hco3)), f_mg_l=("<0.1" if f < 0.1 else "%.1f" % f),
                             no3_n_mg_l=("<0.01" if no3 < 0.01 else "%.2f" % no3),
                             fe_mg_l=("<0.05" if fe < 0.05 else "%.2f" % fe), lab_batch=batch_of[day]))
        serial += int(r.integers(1, 3))
    return write_csv(path, rows, QUALITY_COLUMNS)


# ------------------------------------------------------------------ the landholder contact log (2026)

WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
SHARED_ROAD = "Ghost Gum, Saltbush Flat, Brolga Plains"
BLAST_AREAS = ["pit east", "pit north", "the eastern box cut", "ramp 2", "pit south"]
ROAD_WORKS = [("6 am to 6 pm", "for grading"), ("7 am to 3 pm", "while the dragline walks across"),
              ("all day", "for culvert repairs; use the northern track"), ("6 am to 2 pm", "for power line works"),
              ("7 am to 5 pm", "for the water cart fill point move")]


def _weekday_before(day, lo, hi, r):
    d = day - dt.timedelta(days=int(r.integers(lo, hi + 1)))
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


def _span(days):
    a, b = min(days), max(days)
    if a == b:
        return "%d %s" % (a.day, a.strftime("%B"))
    if a.month == b.month:
        return "%d to %d %s" % (a.day, b.day, b.strftime("%B"))
    return "%d %s to %d %s" % (a.day, a.strftime("%B"), b.day, b.strftime("%B"))


def contact_rows():
    """The environment team's 2026 log: the landholders' own calls, emails and visits, and the team's routine notices
    (blasts, bore runs, the shared access road, dust results), each on a working day with its own dates. Where an
    entry speaks of a field visit it is the visit in the dips file, by the officer who made it."""
    P = W.PEOPLE
    vis = RD.schedule()
    hm = lambda when, mins: (when + dt.timedelta(minutes=mins)).strftime("%H:%M")
    by = lambda when: {"NC": P["tech"], "EM": P["env"]}[RD.officer(when, "monthly")]
    first = lambda lab, cond: min(w for l_, w, _ in vis if l_ == lab and cond(w.date()))
    apr = first("CM1", lambda d_: (d_.year, d_.month) == (2026, 4))
    jul = first("B3", lambda d_: d_ > dt.date(2026, 6, 22))
    sep2 = first("A5", lambda d_: d_ == dt.date(2026, 9, 2))
    others = [k for k, d_ in W.COMPLAINTS.items() if d_ < dt.date(2026, 9, 7) and W.BY_LABEL[k]["prop"] != "Ghost Gum"]
    E = [
        ("05/01/2026", "09:12", "Phone", "Bellbird Downs", "office", "Dust", "Dust over the eastern boundary fence from the haul road on 3 and 4 January.", "Water cart run doubled on the eastern haul road; called back 06/01.", P["env"]),
        ("13/01/2026", "14:40", "Email", "Tondara", "owner's office", "Access", "Requested the date of the next bore visit so the dogs can be tied up.", "Run dates sent for the year.", P["env"]),
        ("22/01/2026", "07:55", "Phone", "Saltbush Flat", P["walker"], "Blasting", "Asked for the blast schedule for February; cattle being moved near the lease boundary.", "Added to the blast notification list.", P["env"]),
        ("03/02/2026", "11:20", "Visit", "Ghost Gum", P["lewis"], "Road", "Grid on the shared access road damaged by a contractor's truck.", "Contractor notified; grid repaired 09/02.", P["env"]),
        ("19/02/2026", "16:05", "Phone", "Coolibah Springs", "manager", "Water", "Asked whether the mine draws from the lagoon reach of the creek.", "Explained the licensed take is from the pit and the dewatering bores only; offered a site visit.", P["hydro"]),
        ("02/03/2026", "08:45", "Email", "Gidgee Creek", "office", "Monitoring", "Asked for copies of the quarterly levels at the north and shed bores.", "Sent the levels to 31/12/2025.", P["env"]),
        ("16/03/2026", "10:30", "Phone", "Wilga Vale", "owner's agent", "Noise", "Night noise from the dragline audible at the homestead in still conditions.", "Noise monitor placed 18/03 to 01/04; results sent.", P["env"]),
        (apr.strftime("%d/%m/%Y"), hm(apr, 15), "Visit", "Yarrowmere", "manager", "Monitoring", "Logger visit at the house bore; manager asked how the readings are used.", "Explained the network and the MG-02 assessments.", by(apr)),
        ("27/04/2026", "09:50", "Phone", "Brolga Plains", "office", "Stock", "Cattle got through the lease fence near the yards bore track.", "Fence repaired 28/04.", P["env"]),
        ("14/05/2026", "15:35", "Email", "Bottletree", "office", "Blasting", "Dust and fume from a blast on 13 May drifted over the ridge paddock.", "Blast log checked; wind conditions reviewed with the drill and blast supervisor.", P["env"]),
        ("03/06/2026", "08:10", "Phone", "Saltbush Flat", P["walker"], "Water", "Creek has stopped running at the crossing; asked when it last stopped.", "Told him the creek gauge records are with the department.", P["env"]),
        ("22/06/2026", "12:00", "Visit", "Kurrajong Park", "manager", "Monitoring", "Asked for the ridge paddock bore to be dipped while the pump is serviced.", "Dipped on the July run, %s; levels sent." % jul.strftime("%d/%m"), by(dt.datetime(2026, 6, 22, 12))),
        ("09/07/2026", "10:25", "Email", "Lancewood Flat", "owner's office", "Monitoring", "Headworks at the windmill bore need the casing extension painted.", "Logged for the next run.", P["env"]),
        ("28/07/2026", "17:20", "Phone", "Cypress Ridge", "trust office", "Water", "Asked for the levels at the creek bore for the trust's annual report.", "Sent the levels to 30/06/2026.", P["env"]),
        ("03/08/2026", "07:40", "Phone", "Saltbush Flat", P["walker"], "Bore complaint", "House bore sucking air since the last week of July; pump cutting out in the afternoons. Wants to know if the mine has taken his water.", "Recorded as a complaint under MG-02 7.1; fortnightly dips from 10 August.", P["env"]),
        ("06/08/2026", "11:05", "Visit", "Saltbush Flat", P["walker"], "Bore complaint", "Site visit with the field technician; pump lowered by the landholder's contractor in July.", "Explained the assessment under MG-02 and the timing.", P["hydro"]),
        ("19/08/2026", "14:30", "Email", "Brolga Plains", "office", "Bore complaint", "Yards bore sucking air at the windmill; trough not filling for two days in seven.", "Recorded as a complaint under MG-02 7.1; acknowledged 20/08.", P["env"]),
        ("25/08/2026", "09:15", "Phone", "Bellbird Downs", "office", "Dust", "Dust from the topsoil stockpile on 24 August.", "Stockpile watered; called back.", P["env"]),
        (sep2.strftime("%d/%m/%Y"), hm(sep2, 16), "Visit", "Ghost Gum", P["lewis"], "Bore complaint", "Garden bore sucking air; pump running on and off when the field team arrived.", "Recorded as a complaint under MG-02 7.1.", by(sep2)),
        ("07/09/2026", "16:40", "Phone", "Ghost Gum", P["lewis"], "Bore complaint", "Asked whether neighbours have the same problem.", "Told him %s other landholders have raised bores and each is being assessed." % WORDS[len(others)], P["env"]),
        ("15/09/2026", "10:55", "Email", "Bottletree", "office", "Bore complaint", "Ridge bore sucking air at the windmill since early September; stock water carted to the ridge paddock.", "Recorded as a complaint under MG-02 7.1.", P["env"]),
        ("21/09/2026", "13:10", "Phone", "Yarrowmere", "manager", "Monitoring", "Asked for the logger readings at the house bore and the Ten Mile bore.", "Will be sent after the October download.", P["env"]),
        ("30/09/2026", "15:25", "Email", "Brolga Plains", "office", "Bore complaint", "Asked when the assessment will be finished.", "Assessments to the executive team on 26 October; written reply to follow.", P["hydro"]),
        ("06/10/2026", "09:30", "Phone", "Saltbush Flat", P["walker"], "Bore complaint", "Asked for the result of the assessment.", "Told him the assessment is with the executive team on 26 October.", P["env"]),
        ("08/10/2026", "11:45", "Email", "Bottletree", "office", "Bore complaint", "Asked for the September readings at the ridge bore.", "Readings to follow with the assessment letter.", P["env"]),
    ]
    rows = [dict(date=dt.datetime.strptime(a, "%d/%m/%Y").date(), time=b, contact=c, property=d, contact_person=e,
                 topic=f, summary=g, action=h, logged_by=i) for a, b, c, d, e, f, g, h, i in E]
    r = W.rng("contacts-2")
    note = lambda day, time, contact, prop, topic, summary, action: rows.append(dict(
        date=day, time=time, contact=contact, property=prop, contact_person="", topic=topic, summary=summary,
        action=action, logged_by=P["env"]))
    clock = lambda: "%02d:%02d" % (8 + int(r.integers(0, 8)), int(r.integers(0, 12)) * 5)
    # blast notifications to the notification list, sent late in the week before the shots
    monday = dt.date(2026, 1, 12)
    while monday <= dt.date(2026, 10, 5):
        must = monday <= dt.date(2026, 5, 13) < monday + dt.timedelta(days=7)
        if must or r.random() < 0.3:
            shots = sorted({monday + dt.timedelta(days=int(r.integers(1, 4))) for _ in range(int(r.integers(1, 3)))})
            if must:
                shots = sorted(set(shots) | {dt.date(2026, 5, 13)})
            sent = monday - dt.timedelta(days=int(r.integers(3, 5)))
            if sent <= dt.date(2026, 10, 8) and sent >= dt.date(2026, 1, 8):
                if shots[0].month == shots[-1].month:
                    days_ = " and ".join("%s %d" % (x.strftime("%a"), x.day) for x in shots) + " " + shots[-1].strftime("%B")
                else:
                    days_ = " and ".join("%s %d %s" % (x.strftime("%a"), x.day, x.strftime("%B")) for x in shots)
                note(sent, clock(), "Email", "notification list", "Blasting",
                     "Blast notification for the week of %d %s: shots %s, 1 pm to 3 pm, %s." % (
                         monday.day, monday.strftime("%B"), days_, BLAST_AREAS[int(r.integers(0, len(BLAST_AREAS)))]),
                     "Sent")
        monday += dt.timedelta(days=7)
    # bore run notices to the landholders, from the runs in the dips file
    run_days = sorted({(when.date(), purpose == "fortnightly") for lab, when, purpose in vis if when.year == 2026
                       and W.BY_LABEL[lab]["kind"] == "landholder" and purpose in ("monthly", "monthly-dl", "fortnightly")})
    runs = []
    for day, fortnightly in run_days:
        if runs and runs[-1][1] == fortnightly and (day - runs[-1][0][-1]).days <= 4:
            runs[-1][0].append(day)
        else:
            runs.append(([day], fortnightly))
    for days_, fortnightly in runs:
        if min(days_) < dt.date(2026, 2, 1) or not (fortnightly or r.random() < 0.6):
            continue
        sent = _weekday_before(min(days_), 3, 6, r)
        note(sent, clock(), "Email", "landholders", "Monitoring",
             "%s run notice: landholder bores to be dipped %s." % ("Fortnightly" if fortnightly else "Bore", _span(days_)),
             "Sent")
    # closures of the haul road crossing on the shared access road
    for k, start in enumerate((dt.date(2026, 2, 23), dt.date(2026, 4, 14), dt.date(2026, 5, 25), dt.date(2026, 7, 27),
                               dt.date(2026, 9, 7))):
        day = start + dt.timedelta(days=int(r.integers(0, 10)))
        while day.weekday() >= 5:
            day += dt.timedelta(days=1)
        n = int(r.integers(1, 4))
        closed = [day + dt.timedelta(days=j) for j in range(n)]
        hours, why = ROAD_WORKS[k]
        note(_weekday_before(day, 2, 5, r), clock(), "Email" if r.random() < 0.7 else "Letter", SHARED_ROAD, "Road",
             "Haul road crossing on the shared access road closed %s, %s, %s." % (_span(closed), hours, why), "Notice sent")
    # dust deposition results, posted each month
    for m in range(1, 10):
        if r.random() < 0.15:
            continue
        posted = _weekday_before(dt.date(2026 + (m == 12), m % 12 + 1, 1) + dt.timedelta(days=int(r.integers(12, 20))), 0, 0, r)
        if posted <= dt.date(2026, 10, 8):
            note(posted, clock(), "Email", "all neighbours", "Dust",
                 "Dust deposition results for %s posted to the community page." % dt.date(2026, m, 1).strftime("%B"),
                 "Community")
    rows.sort(key=lambda x: (x["date"], x["time"]))
    assert all(x["date"].weekday() < 5 for x in rows)
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
