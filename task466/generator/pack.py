"""Write the pack's data files: the State Hydrologic Survey's daily values for the gauge, the select board's drought
notices, the treatment plant's SCADA daily totals, Elm Hollow's master meter reads, the Hollow Road operator's log, and
the town weather station's monthly precipitation (a distractor)."""
import csv
import datetime as dt
import math

import numpy as np

import sim as S
import world as W


def write_csv(path, header, rows, lineterminator="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator=lineterminator)
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def _rng(*key):
    return np.random.default_rng([W.SEED, 70] + [int(k) for k in key])


def fmt_dv(v):
    if v < 10:
        return "%.2f" % v
    if v < 100:
        return "%.1f" % v
    return "%d" % int(v)


# ---------------------------------------------------------------- the Survey's daily values
def ice_days(days):
    """Days the Survey estimated for ice, by winter: a cold winter's spell of backwater at the control."""
    out = set()
    winters = sorted({d.year for d in days if d.month == 12})
    for y in winters:
        rng = _rng(1, y)
        if rng.random() < 0.42:
            start = dt.date(y, 12, 10) + dt.timedelta(days=int(rng.integers(0, 30)))
            for k in range(int(rng.integers(9, 48))):
                out.add(start + dt.timedelta(days=k))
    return out


GAUGE_HEADER = [
    "# ---------------------------------- NOTICE ----------------------------------",
    "# Data from the State Hydrologic Survey's water data system. Data qualified as",
    "# provisional have not received final review and are subject to revision.",
    "# Approved data are final and will not change except for errors found later.",
    "# ----------------------------------------------------------------------------",
    "#",
    "# Station %s, %s" % (W.STATION_NO, W.STATION),
    "# Drainage area 41.6 square miles",
    "# Parameter: discharge, cubic feet per second, daily mean",
    "# Day: midnight to midnight, local standard time",
    "#",
    "# Qualification codes in this output:",
    "#   A   approved for publication, review complete",
    "#   P   provisional, subject to revision",
    "#   e   value estimated (combined with A or P, e.g. A:e)",
    "#",
    "# Retrieved 2026-10-16 07:12 EDT",
    "#",
]


def gauge_rows(x):
    ice = ice_days(x["days"])
    rows = []
    for d, v in zip(x["days"], x["values"]):
        code = "A" if d <= W.APPROVED_THROUGH else "P"
        if d in ice:
            code += ":e"
        rows.append(["SHS", W.STATION_NO, d.isoformat(), fmt_dv(v), code])
    return rows


def write_gauge(path, x):
    rows = gauge_rows(x)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        for line in GAUGE_HEADER:
            fh.write(line + "\n")
        fh.write("agency\tstation\tdate\tdischarge_cfs\tqual\n")
        fh.write("5s\t12s\t10d\t12n\t6s\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    return len(rows)


# ---------------------------------------------------------------- the select board's drought notices
NOTICE_COLS = ["notice_no", "posted", "stage", "action", "in_effect_from", "in_effect_through", "basis"]


def notice_rows(x):
    """Each notice as the board's clerk entered it. A declaration quotes the provisional 7-day mean the superintendent
    saw on the Survey's real-time page the day before posting, which was below the stage's level (the provisional
    value runs a little off the approved one); a rescission cites the 14 days at or above the level."""
    rows, seq = [], {}
    days = x["days"]
    m7 = np.convolve(x["values"], np.ones(7) / 7, mode="full")[:len(x["values"])]
    say_declare = ["7-day mean flow %.2f cfs on the Survey's real-time page, %s",
                   "Real-time 7-day mean %.2f cfs (%s)", "Survey real-time 7-day average %.2f cfs on %s",
                   "7-day mean %.2f cfs, provisional, %s"]
    say_rescind = ["7-day mean flow at or above %.1f cfs for 14 days (real-time page)",
                   "14 consecutive days at or above %.1f cfs, 7-day mean",
                   "Real-time 7-day mean back above %.1f cfs for two weeks"]
    for k, (posted, stage, action, eff) in enumerate(x["notices"]):
        seq[posted.year] = seq.get(posted.year, 0) + 1
        no = "DN-%d-%02d" % (posted.year, seq[posted.year])
        rng = _rng(2, posted.toordinal())
        level = W.TRIGGER_STAGE2_CFS if stage == 2 else W.TRIGGER_STAGE1_CFS
        if action == "declared":
            seen_day = posted - dt.timedelta(days=1)
            i = days.index(seen_day)
            seen = min(m7[j] for j in range(i - 3, i + 1)) * math.exp(rng.normal(0.0, 0.012))
            if seen >= level - 0.005:
                seen = level - rng.uniform(0.02, 0.09)
            basis = say_declare[k % len(say_declare)] % (seen, seen_day.isoformat())
            rows.append([no, posted.isoformat(), "Stage %d" % stage, "Declared", eff.isoformat(), "", basis])
        else:
            basis = say_rescind[k % len(say_rescind)] % level
            rows.append([no, posted.isoformat(), "Stage %d" % stage, "Rescinded", "", eff.isoformat(), basis])
    return rows


# ---------------------------------------------------------------- the plant's SCADA daily totals
SCADA_COLS = ["RecordID", "Date", "Tag", "Description", "DailyTotal", "Units"]
TAGS = [("WTP_RAW_TOTAL", "Raw water from river intake"), ("WTP_FIN_TOTAL", "Finished water, clearwell effluent"),
        ("HR_WELLS_TOTAL", "Hollow Road wellfield to system")]


def scada_rows(x):
    o = x["ops"]
    rows, rid = [], 4810227
    vals = {"WTP_RAW_TOTAL": o["raw"], "WTP_FIN_TOTAL": o["fin"], "HR_WELLS_TOTAL": x["scada_wells"]}
    restore = []
    for i, d in enumerate(o["days"]):
        for tag, desc in TAGS:
            rid += 1
            row = [rid, d.isoformat(), tag, desc, "%.3f" % vals[tag][i], "MG"]
            rows.append(row)
            if W.RESTORE[0] <= d <= W.RESTORE[1]:
                restore.append(row)
    # the August 2020 historian restore re-sent three weeks under new record numbers, appended where it ran
    at = next(k for k, r in enumerate(rows) if r[1] == "2020-09-02")
    resent = [[4810227 + len(rows) + 1 + k] + r[1:] for k, r in enumerate(restore)]
    rows = rows[:at] + resent + rows[at:]
    return rows


# ---------------------------------------------------------------- Elm Hollow's master meter
EH_COLS = ["read_date", "meter_id", "consumption_kgal", "read_type"]


def elm_rows(x):
    o = x["ops"]
    rows = []
    for i, d in enumerate(o["days"]):
        rng = _rng(3, d.toordinal())
        kind = "Estimated" if rng.random() < 0.012 else "Actual"
        rows.append([d.isoformat(), "EH-01", "%.1f" % (o["elm"][i] * 1000), kind])
    return rows


# ---------------------------------------------------------------- the Hollow Road operator's log
LOG_COLS = ["log_date", "reading_time", "totalizer_gal", "remarks"]


ROUTINE_NOTES = ["Chlorine residual checked at the station", "Bacteria sample taken", "Generator exercised 30 minutes",
                 "Station heater checked", "Grass cut around the well house", "Pump 2 packing adjusted"]
ONE_OFF_NOTES = ["Radio still down; reading phoned in to the plant", "Vendor on site for the radio, not repaired",
                 "Totalizer glass fogged, read with a flashlight", "Wellhouse door latch replaced",
                 "Pump 1 bearing noise, reported to the superintendent"]


def log_rows(x):
    """Daily rounds since the radio failed: the wellfield totalizer read at the start of the day shift. The reading on
    a day closes the previous day's pumping."""
    o = x["ops"]
    i0 = o["days"].index(W.RADIO_FAILED)
    pool = ROUTINE_NOTES * 4 + ONE_OFF_NOTES
    notes = [pool[k] for k in _rng(4, 0).permutation(len(pool))]
    total = int(round(84612300 + float(np.sum(o["wells"][:i0])) * 1e6))   # pumped since the meter went in, June 2010
    rows = []
    for i in range(i0, len(o["days"])):
        d = o["days"][i]
        rng = _rng(4, d.toordinal())
        t = "07:%02d" % int(rng.integers(20, 50))
        remark = ""
        if i == i0:
            remark = "Telemetry down at the wellfield; totalizer read on rounds"
        elif rng.random() < 0.025 and notes:
            remark = notes.pop()
        rows.append([d.isoformat(), t, "%d" % total, remark])
        total += int(round(o["wells"][i] * 1e6))
    return rows


def well_log_daily(rows):
    """{day: gallons pumped} from the operator's readings: the difference to the next morning's reading."""
    out = {}
    for a, b in zip(rows, rows[1:]):
        out[dt.date.fromisoformat(a[0])] = int(b[2]) - int(a[2])
    return out


# ---------------------------------------------------------------- the weather station (distractor)
PRECIP_COLS = ["station", "year", "month", "precip_in", "attributes"]


def precip_rows(x):
    rows = []
    low = {y: v for y, v in x["gauge_targets"].items()}
    low.update({y: v for y, v in x["report_targets"].items()})
    for y in range(1895, 2026):
        for m in range(1, 13):
            rng = _rng(5, y, m)
            base = [3.4, 3.1, 3.9, 3.8, 3.7, 3.9, 3.8, 3.7, 3.6, 4.1, 3.9, 3.7][m - 1]
            dry = 1.0
            if 6 <= m <= 9 and y in low:
                dry = min(1.25, max(0.45, (low[y] / 5.5) ** 0.45))
            v = max(0.05, base * dry * rng.gamma(6.0, 1 / 6.0))
            flag = ""
            if rng.random() < 0.006:
                rows.append(["QUILLFIELD 2 NW", y, m, "", "M"])
                continue
            rows.append(["QUILLFIELD 2 NW", y, m, "%.2f" % v, flag])
    return rows
