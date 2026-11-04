"""Cut the evidence pack under target/ from the world's truth. Each file is written the way its producing system
writes it: its own clock, units, layout and keys. Nothing here describes the data."""
import csv
import datetime as dt
import io
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import plant as PL
import postprocess as PP
import world as W

FILES = {
    "tr01": "hydro/TR-01_tessel_r_halvard_br_2026.csv",
    "fc02": "hydro/FC-02_fennick_cr_cr_w38_2026.csv",
    "oc03": "hydro/OC-03_oxley_cr_lisle_2026.csv",
    "dc04": "hydro/DC-04_logger_2087445_2026.csv",
    "lb05": "hydro/LB-05_logger_2087519_2026.csv",
    "ratings": "hydro/DC-04_LB-05_ratings_and_field_visits.xlsx",
    "shl": "lab/SHL_EDD_brennick_source_water_2026.csv",
    "city": "lab/city_lab_ELISA_tributaries_2026.xlsx",
    "field": "lab/field_sampling_log_2026.xlsx",
    "isco": "lab/autosampler_run_logs_2026.csv",
    "lims_old": "plant/raw_water_log_2026-01-01_to_2026-05-26.csv",
    "lims_new": "plant/LIMS_raw_water_2026-05-20_to_2026-10-31.xlsx",
    "ops": "plant/daily_operating_report_2026.xlsx",
    "pac_sp": "plant/scada_pac_dose_setpoint_2026.csv",
    "alarms": "plant/scada_alarm_event_history_2026.csv",
    "buoy": "lake/MERRIN_BUOY_Hourly_2026.dat",
    "buoy_log": "lake/buoy_service_log_2026.csv",
    "dam": "lake/merrin_dam_daily_log_2026.xlsx",
    "acap": "lake/lake_merrin_area_capacity_2019_survey.csv",
    "drawing": "lake/intake_tower_record_drawing_S-4.pdf",
    "plan": "program/source_water_protection_plan_rev2.pdf",
    "sop": "plant/SOP-WQ-07_powdered_carbon_feed.pdf",
    "survey": "program/haldane_extension_atrazine_use_survey_2026.xlsx",
    "rain": "lake/merrin_dam_precip_daily_2026.txt",
    "nitrate": "lab/tributary_nitrate_2026.csv",
    "beach": "lake/merrin_beach_ecoli_2026.csv",
}
DISTRACTORS = ["nitrate", "beach"]
EXPORT_STAMP = (2026, 11, 2, 8, 14)


def path(target, key):
    return os.path.join(target, FILES[key])


def ensure(p):
    os.makedirs(os.path.dirname(p), exist_ok=True)


def write_csv(p, rows, header=None, preamble=(), newline="\r\n"):
    ensure(p)
    buf = io.StringIO()
    for line in preamble:
        buf.write(line + newline)
    w = csv.writer(buf, lineterminator=newline)
    if header:
        w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


# ------------------------------------------------------------------ clocks
DST_ON = dt.datetime(2026, 3, 8, 2, 0)      # local standard time when clocks go forward
DST_OFF = dt.datetime(2026, 11, 1, 2, 0)


def is_cdt(local):
    return DST_ON <= local < DST_OFF


def local_to_utc(local):
    return local + dt.timedelta(hours=5 if is_cdt(local) else 6)


def utc_to_local(utc):
    if dt.datetime(2026, 3, 8, 8, 0) <= utc < dt.datetime(2026, 11, 1, 7, 0):
        return utc - dt.timedelta(hours=5)
    return utc - dt.timedelta(hours=6)


def local_steps():
    """Every 15-minute local clock time from 1 January 00:00 to 31 October 23:45 (the spring gap left out)."""
    t = dt.datetime(2026, 1, 1, 0, 0)
    end = dt.datetime(2026, 11, 1, 0, 0)
    out = []
    while t < end:
        if not (DST_ON <= t < DST_ON + dt.timedelta(hours=1)):
            out.append(t)
        t += dt.timedelta(minutes=15)
    return out


STEPS = local_steps()
STORM_HOUR = {}


# ------------------------------------------------------------------ 15-minute series from the daily truth
def storm_starts(ST, rng):
    for d, mm, fac in ST:
        STORM_HOUR[d] = float(rng.uniform(14.0, 21.5))


def series15(world, k, rng):
    """Discharge (m3/s), water temperature (C) and atrazine (ug/L) at each local 15-minute step, continuous in time:
    the daily baseflow, temperature and concentration run smoothly between their midday values, and each storm's
    runoff is a hydrograph that rises from the storm's start hour and recedes over the following days, its volume
    the world's storm volume."""
    Q, QS, T, C = world["Q"][k], world["QS"][k], world["T"][k], world["C"][k]
    n = W.ND
    t_ref = dt.datetime.combine(W.D0, dt.time(0))
    x = np.array([(t - t_ref).total_seconds() / 86400.0 for t in STEPS])
    mid = np.arange(n) + 0.5
    hrs = (x % 1.0) * 24.0
    base = np.interp(x, mid, Q - QS) * (1 - 0.018 * np.sin(2 * math.pi * (hrs - 9) / 24))
    rise = dict(TES=16.0, FEN=5.0, OXL=3.5, DUN=4.5, LAD=5.5)[k] / 24.0
    tau_s = W.TAU[k]
    quick_int = rise * math.e ** 2 / 4.0
    slow_int = tau_s ** 2 / (rise + tau_s)
    storm = np.zeros(len(x))
    for d, mm, fac in world["ST"]:
        wet = 1.0 if W.di(4, 1) <= d <= W.di(7, 15) else 0.75
        vol = W.RRATIO[k] * wet * mm / 1000.0 * W.AREA_KM2[k] * 1e6 * fac[k]
        t0 = d + STORM_HOUR.get(d, 18.0) / 24.0
        tau = np.clip(x - t0, 0.0, None)
        g = tau / rise
        quick = g ** 2 * np.exp(2 * (1 - g))
        slow = (1 - np.exp(-g)) * np.exp(-tau / tau_s)
        storm += vol / 86400.0 * (0.45 * quick / quick_int + 0.55 * slow / slow_int)
    q = base + storm
    tt = np.interp(x, mid, T) + W.DIURNAL[k] * np.cos(2 * math.pi * (hrs - 16.0) / 24.0) + rng.normal(0, 0.04, len(x))
    share = np.where(q > 0, storm / q, 0.0)
    cc = np.interp(x, mid, C) * (0.7 + 0.6 * share)
    kappa = float(np.sum(C * Q)) / max(float(np.sum(cc * q)) / 96.0, 1e-12)
    cc = cc * kappa
    return q, tt, cc


def write_station(target, key, k, q, tt, rng):
    st = W.STATION[k]
    title = {"TES": "Tessel River at Halvard Bridge", "FEN": "Fennick Creek at County Road W38",
             "OXL": "Oxley Creek at Lisle"}[k]
    pre = ["# Brennick Water hydrometric network: continuous record export",
           "# Station %s  %s" % (st, title),
           "# Drainage area %.1f sq mi" % (W.AREA_KM2[k] / 2.589988),
           "# Parameters: discharge (ft3/s, qual), water temperature (deg C, qual)",
           "# Times are local clock times; utc_offset gives the offset in force",
           "# Exported 2026-11-02 08:14 by r.dixon"]
    rows = []
    gap = None
    if k == "OXL":
        gap = (dt.datetime(2026, 10, 16, 13, 0), dt.datetime(2026, 10, 18, 9, 30))
    for t, qq, tc in zip(STEPS, q, tt):
        qual = "A" if t < dt.datetime(2026, 7, 1) else "P"
        tq = qual
        cfs = qq / W.CFS
        if gap and gap[0] <= t < gap[1]:
            rows.append([t.strftime("%Y-%m-%d %H:%M"), "-05:00" if is_cdt(t) else "-06:00", "", "Eqp", "", "Eqp"])
            continue
        if t.month <= 2 and k in ("TES", "OXL") and tc < 0.3:
            qual = "A:e"
        rows.append([t.strftime("%Y-%m-%d %H:%M"), "-05:00" if is_cdt(t) else "-06:00",
                     ("%.1f" % cfs) if cfs < 1000 else ("%.0f" % cfs), qual, "%.1f" % max(tc, 0.0), tq])
    write_csv(path(target, key), rows,
              header=["datetime_local", "utc_offset", "discharge_cfs", "discharge_qual", "water_temp_c", "temp_qual"],
              preamble=pre)
    return len(rows)


# ------------------------------------------------------------------ creek loggers and their ratings
RATING = {
    ("DUN", 1): dict(a=46.0, h0=0.62, b=1.62, start=dt.datetime(2025, 7, 10, 12, 0), end=dt.datetime(2026, 6, 2, 11, 30)),
    ("DUN", 2): dict(a=51.5, h0=0.79, b=1.58, start=dt.datetime(2026, 6, 2, 11, 30), end=None),
    ("LAD", 1): dict(a=23.0, h0=0.41, b=1.71, start=dt.datetime(2025, 8, 21, 10, 0), end=None),
}
LOGGER_OFFSET_FT = dict(DUN=1.36, LAD=0.94)       # gage height minus the logger's level reading
# the DC-04 logger slid 0.25 ft down its pipe on a dry afternoon in July (a cow or debris against the housing);
# nobody saw it until the record was reviewed, and the visits after it read the new offset
DUN_SLIP = dt.datetime(2026, 7, 3, 14, 15)
DUN_SLIP_FT = 0.25


def logger_offset_ft(k, local_t):
    if k == "DUN" and local_t >= DUN_SLIP:
        return LOGGER_OFFSET_FT[k] - DUN_SLIP_FT
    return LOGGER_OFFSET_FT[k]


def rating_for(k, local_t):
    for (kk, n), r in sorted(RATING.items()):
        if kk != k:
            continue
        if r["start"] <= local_t and (r["end"] is None or local_t < r["end"]):
            return n, r
    raise KeyError((k, local_t))


def stage_of(k, local_t, q_cfs):
    n, r = rating_for(k, local_t)
    return r["h0"] + (max(q_cfs, 0.0) / r["a"]) ** (1.0 / r["b"])


def control_shift():
    """When the 27 May flood moved Dunmore Creek's control: its peak, a few hours after the storm began."""
    d = W.di(5, 27)
    return dt.datetime.combine(W.day(d), dt.time(0)) + dt.timedelta(hours=STORM_HOUR.get(d, 18.0) + 4.5)


def stage_true(k, local_t, q_cfs):
    """The water's stage at the gage: the channel's own stage-discharge relation, which for Dunmore Creek moved
    with the flood while the rating in the record moved at the next visit."""
    if k == "DUN":
        r = RATING[("DUN", 2)] if local_t >= control_shift() else RATING[("DUN", 1)]
        return r["h0"] + (max(q_cfs, 0.0) / r["a"]) ** (1.0 / r["b"])
    return stage_of(k, local_t, q_cfs)


def flow_of(k, local_t, stage_ft):
    n, r = rating_for(k, local_t)
    return r["a"] * max(stage_ft - r["h0"], 0.0) ** r["b"]


def write_logger(target, key, k, q, tt, rng):
    serial = {"DUN": "2087445", "LAD": "2087519"}[k]
    loc = {"DUN": "DC-04 Dunmore Cr at 230th St", "LAD": "LB-05 Ladd Br at Merrin Park Rd"}[k]
    pre = ["Serial_number:", serial, "Project ID:", "Brennick Water source water", "Location:", loc,
           "LEVEL", "UNIT: ft", "Offset: 0.000 ft", "TEMPERATURE", "UNIT: Deg C", ""]
    rows = []
    for t, qq, tc in zip(STEPS, q, tt):
        utc = local_to_utc(t)
        h = stage_true(k, t, qq / W.CFS) - logger_offset_ft(k, t) + float(rng.normal(0, 0.004))
        rows.append([utc.strftime("%Y/%m/%d"), utc.strftime("%H:%M:%S"), "0", "%.4f" % h, "%.3f" % max(tc, 0.0)])
    rows.sort(key=lambda r: (r[0], r[1]))
    write_csv(path(target, key), rows, header=["Date", "Time", "ms", "LEVEL", "TEMPERATURE"], preamble=pre)
    return len(rows)


def xlsx_save(wb, p, creator, company, created, modified, title=None):
    ensure(p)
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if cell.value == "":
                    cell.value = None
    wb.save(p)
    PP.normalize_ooxml(p, creator, creator, created, modified, title=title, excel=True, company=company)


def header_style(ws, ncol, row=1):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="D9E1F2")
        cell.alignment = Alignment(wrap_text=True, vertical="top")


def write_ratings(target, rng, visits):
    wb = openpyxl.Workbook()
    first = True
    for (k, n), r in sorted(RATING.items()):
        name = "%s rating %d" % (W.STATION[k], n)
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = name
        ws.append(["Station", W.STATION[k], "", "Rating", n])
        ws.append(["Effective from", r["start"].strftime("%Y-%m-%d %H:%M") + " CDT" if is_cdt(r["start"]) else
                   r["start"].strftime("%Y-%m-%d %H:%M") + " CST",
                   "", "Superseded", (r["end"].strftime("%Y-%m-%d %H:%M") + " CDT") if r["end"] else ""])
        ws.append([])
        ws.append(["Gage height (ft)", "Discharge (ft3/s)"])
        header_style(ws, 2, row=4)
        h = round(r["h0"] + 0.02, 2)
        while h <= 6.0:
            ws.append([round(h, 2), round(r["a"] * (h - r["h0"]) ** r["b"], 2)])
            h = round(h + 0.02, 2)
        ws.column_dimensions["A"].width = 18
        ws.column_dimensions["B"].width = 18
    ws = wb.create_sheet("Field visits")
    ws.append(["Station", "Date", "Time (local)", "Staff gage (ft)", "Logger level (ft)", "Measured discharge (ft3/s)",
               "Method", "Party", "Remarks"])
    header_style(ws, 9)
    for v in visits:
        ws.append(v)
    for col, wdt in zip("ABCDEFGHI", (9, 12, 12, 14, 15, 22, 16, 10, 40)):
        ws.column_dimensions[col].width = wdt
    xlsx_save(wb, path(target, "ratings"), "Rhonda Dixon", W.DEPT, "2025-07-14T15:02:11Z", "2026-10-29T19:40:52Z")


def field_visits(world, q15, rng):
    out = []
    for k in ("DUN", "LAD"):
        dates = [dt.datetime(2026, m, d, int(rng.integers(9, 15)), int(rng.integers(0, 59)))
                 for m, d in ((3, 24), (4, 21), (5, 19), (6, 2), (6, 30), (7, 28), (8, 25), (9, 22), (10, 20))]
        if k == "LAD":
            dates = [x for x in dates if x.month != 6 or x.day != 2]
        for t in dates:
            j = min(range(len(STEPS)), key=lambda n: abs((STEPS[n] - t).total_seconds()))
            qc = q15[k][j] / W.CFS
            hh = stage_true(k, STEPS[j], qc)
            rem = ""
            if k == "DUN" and t == dates[3]:
                rem = "Gravel bar at riffle after 27-28 May high water; measurement off rating 1; rating 2 from this visit"
            meas = qc * float(np.exp(rng.normal(0, 0.035)))
            out.append([W.STATION[k], t.strftime("%Y-%m-%d"), t.strftime("%H:%M"), round(hh + float(rng.normal(0, 0.003)), 2),
                        round(hh - logger_offset_ft(k, STEPS[j]) + float(rng.normal(0, 0.003)), 3), round(meas, 2),
                        "FlowTracker2" if qc < 60 else "ADCP (RiverRay)",
                        "RD/GL" if rng.random() < 0.6 else "RD", rem])
    out.sort(key=lambda r: (r[1], r[0]))
    return out


# ------------------------------------------------------------------ the sampling program
SITE = dict(TES="TES-HB", FEN="FEN-38", OXL="OXL-LS", DUN="DUN-230", LAD="LAD-MP")


def sampling(world, c15, rng):
    """Bottles: routine Tuesday grabs at every site, storm grabs at the four larger sites after the April to
    August storms, a QA split to both laboratories on about one storm bottle in four. Returns bottles with the
    truth concentration at the moment of collection."""
    bottles = []
    tues = [dt.date(2026, 3, 31) + dt.timedelta(days=7 * n) for n in range(31)]
    route = ["FEN", "OXL", "DUN", "TES"]
    idx = {t: n for n, t in enumerate(STEPS)}
    for d in tues:
        t = dt.datetime.combine(d, dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 40)))
        for k in route:
            t = t + dt.timedelta(minutes=int(rng.integers(28, 55)))
            bottles.append(dict(k=k, t=t, logged=t, kind="Routine grab", labs="SHL"))
    runs = []
    sampler = dict(TES="ISCO 6712 #A1043", FEN="ISCO 6712 #A1167", OXL="ISCO 6712 #A0988", DUN="ISCO 3700 #3G2210")
    for d, mm, fac in world["ST"]:
        if not (W.di(4, 20) <= d <= W.di(9, 30)):
            continue
        h0 = STORM_HOUR.get(d, 18.0)
        for k in ("TES", "FEN", "OXL", "DUN"):
            enable = dt.datetime.combine(W.day(d), dt.time(0, 0)) + dt.timedelta(
                hours=h0 + float(rng.uniform(0.6, 2.4)) * dict(TES=3.0, FEN=1.0, OXL=0.8, DUN=1.0)[k])
            enable = enable.replace(second=0, microsecond=0)
            interval = dict(TES=8, FEN=6, OXL=4, DUN=5)[k]
            npos = int(rng.integers(5, 8))
            fills = []
            for pos in range(1, npos + 1):
                ft = enable + dt.timedelta(minutes=int(interval * 60 * (pos - 1)))
                status = "NO LIQUID" if (pos > 1 and rng.random() < 0.16) else "OK"
                fills.append(dict(pos=pos, t=ft, status=status))
            last = fills[-1]["t"]
            retrieve = dt.datetime.combine((last + dt.timedelta(hours=10)).date(), dt.time(int(rng.integers(8, 11)),
                                                                                         int(rng.integers(0, 59))))
            if retrieve <= last:
                retrieve = last + dt.timedelta(hours=3, minutes=int(rng.integers(0, 50)))
            runs.append(dict(k=k, sampler=sampler[k], enable=enable, fills=fills, retrieve=retrieve))
            for f in fills:
                if f["status"] != "OK":
                    continue
                lab = "City"
                if rng.random() < 0.27:
                    lab = "SHL + City"
                bottles.append(dict(k=k, t=f["t"], logged=retrieve, kind="Storm (ISCO)", labs=lab,
                                    run=len(runs) - 1, pos=f["pos"]))
    world["isco_runs"] = runs
    bottles.sort(key=lambda b: (b["logged"], b["k"], b["t"]))
    for n, b in enumerate(bottles):
        b["bottle"] = "BW-26-%04d" % (n + 1)
        # truth at the nearest 15-minute step
        tt = b["t"].replace(minute=(b["t"].minute // 15) * 15)
        j = idx.get(tt)
        if j is None:
            j = min(range(len(STEPS)), key=lambda m: abs((STEPS[m] - b["t"]).total_seconds()))
        b["truth"] = float(c15[b["k"]][j])
        b["ftemp"] = None
    return bottles


def lab_results(bottles, rng):
    """Each bottle's results at the laboratories it went to."""
    for b in bottles:
        b["shl"] = None
        b["elisa"] = None
        if "SHL" in b["labs"]:
            v = b["truth"] * math.exp(rng.normal(0, 0.04))
            b["shl"] = v
        if "City" in b["labs"]:
            v = b["truth"] * 1.07 * math.exp(rng.normal(0, 0.06))
            b["elisa"] = v
    return bottles


def write_isco(target, runs, rng):
    rows = []
    for r in runs:
        st = W.STATION[r["k"]]
        for f in r["fills"]:
            vol = int(rng.integers(780, 960)) if f["status"] == "OK" else 0
            rows.append([st, r["sampler"], r["enable"].strftime("%Y-%m-%d %H:%M"), f["pos"], f["t"].strftime("%Y-%m-%d %H:%M"),
                         f["status"], vol, r["retrieve"].strftime("%Y-%m-%d %H:%M")])
    rows.sort(key=lambda x: (x[2], x[0], x[3]))
    write_csv(path(target, "isco"), rows, header=["Station", "Sampler", "Program enabled", "Bottle position",
                                                  "Sample time", "Status", "Volume (mL)", "Carousel removed"])
    return len(rows)


def write_field_log(target, bottles, T15, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2026 bottles"
    ws.append(["Bottle ID", "Site", "Date logged", "Time logged", "Sample type", "Sent to", "Water temp (C)", "Collector",
               "Notes"])
    header_style(ws, 9)
    idx = {t: n for n, t in enumerate(STEPS)}
    notes = ["", "", "", "", "", "", "", "high water", "sampled from bridge deck", "staff gage read", "turbid",
             "light rain", "cooler on ice", "bank sample, bridge closed"]
    sampler_of = dict(TES="ISCO A1043", FEN="ISCO A1167", OXL="ISCO A0988", DUN="ISCO 3G2210")
    for b in bottles:
        lt = b["logged"]
        tt = lt.replace(minute=(lt.minute // 15) * 15)
        j = idx.get(tt, 0)
        ftemp = T15[b["k"]][j] + float(rng.normal(0, 0.15))
        note = notes[int(rng.integers(0, len(notes)))]
        if b["kind"].startswith("Storm"):
            note = "%s carousel" % sampler_of[b["k"]]
        ws.append([b["bottle"], SITE[b["k"]], lt.strftime("%m/%d/%Y"), lt.strftime("%H:%M"), b["kind"],
                   b["labs"], round(ftemp, 1), "RD" if rng.random() < 0.45 else ("BD" if rng.random() < 0.55 else "GL"),
                   note])
    for col, wdt in zip("ABCDEFGHI", (12, 9, 11, 7, 13, 11, 13, 9, 26)):
        ws.column_dimensions[col].width = wdt
    xlsx_save(wb, path(target, "field"), "Brandi Dougherty", W.DEPT, "2026-03-30T13:20:07Z", "2026-10-28T21:11:46Z")


def write_shl(target, bottles, rng):
    """The State Hygienic Laboratory's electronic data deliverable: one row per analyte, keyed by its own lab
    number and the client's bottle number as the lab keys it, dated by login."""
    rows = []
    labno = 0
    for b in bottles:
        if b["shl"] is None:
            continue
        labno += int(rng.integers(1, 9))
        lab_id = "26W%05d" % (4100 + labno)
        recv = b["logged"] + dt.timedelta(hours=float(rng.uniform(18, 30)))
        if recv.weekday() >= 5:
            recv = recv + dt.timedelta(days=7 - recv.weekday())
        recv = recv.replace(hour=int(rng.integers(8, 11)), minute=int(rng.integers(0, 59)))
        anal = recv + dt.timedelta(days=int(rng.integers(2, 6)))
        rep = anal + dt.timedelta(days=int(rng.integers(1, 4)))
        client = b["bottle"].replace("-", "")
        for analyte, cas, frac in (("Atrazine", "1912-24-9", 1.0), ("Desethylatrazine", "6190-65-4", 0.21),
                                   ("Metolachlor", "51218-45-2", 0.62), ("Acetochlor", "34256-82-1", 0.18)):
            v = b["shl"] * frac * (1.0 if analyte == "Atrazine" else math.exp(rng.normal(0, 0.25)))
            if v < 0.10:
                res, q = "0.10", "U"
            else:
                res, q = ("%.2f" % v) if v < 10 else ("%.1f" % v), ""
            rows.append([lab_id, client, recv.strftime("%m/%d/%Y %H:%M"), anal.strftime("%m/%d/%Y"), analyte, cas, res,
                         "ug/L", "0.10", q, "EPA 525.3", "1", rep.strftime("%m/%d/%Y")])
    write_csv(path(target, "shl"), rows,
              header=["Lab_Sample_ID", "Client_Sample_ID", "Login_Date", "Analysis_Date", "Analyte", "CAS_No",
                      "Result", "Units", "Reporting_Limit", "Qualifier", "Method", "Dilution", "Report_Date"])
    return len(rows)


def write_city(target, bottles, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Results"
    ws.append(["LIMS ID", "Bottle", "Site", "Logged in", "Test", "Result", "Units", "RL", "Flag", "Analyst",
               "Kit lot"])
    header_style(ws, 11)
    n = 1180
    lots = ["ATZ-25K118", "ATZ-26B044", "ATZ-26E201"]
    for b in bottles:
        if b["elisa"] is None:
            continue
        n += int(rng.integers(1, 4))
        v = b["elisa"]
        if v < 0.05:
            res, fl = 0.05, "<"
        else:
            res, fl = round(v, 2), ""
        login = b["logged"] + dt.timedelta(minutes=int(rng.integers(70, 260)))
        if login.hour >= 17:
            login = (login + dt.timedelta(days=1)).replace(hour=7, minute=int(rng.integers(30, 59)))
        ws.append(["SW26-%04d" % n, b["bottle"], SITE[b["k"]], login.strftime("%m/%d/%Y %H:%M"), "Atrazine ELISA",
                   res, "ppb", 0.05, fl, "BD" if rng.random() < 0.7 else "BC",
                   lots[0] if b["logged"].month < 5 else (lots[1] if b["logged"].month < 7 else lots[2])])
    for col, wdt in zip("ABCDEFGHIJK", (11, 12, 9, 17, 15, 8, 6, 5, 5, 8, 12)):
        ws.column_dimensions[col].width = wdt
    xlsx_save(wb, path(target, "city"), "Brandi Dougherty", W.DEPT, "2026-04-29T16:02:33Z", "2026-10-30T14:47:20Z")


# ------------------------------------------------------------------ the plant
def write_lims_old(target, res, rng):
    rows = []
    for r in res:
        if r["date"] > dt.date(2026, 5, 26):
            break
        f = r["raw_temp"] * 9 / 5 + 32
        turb = max(0.8, float(rng.lognormal(math.log(6.0), 0.45)))
        ph = 7.9 + float(rng.normal(0, 0.12))
        alk = 214 + float(rng.normal(0, 9))
        hard = 268 + float(rng.normal(0, 12))
        rows.append([r["date"].strftime("%m/%d/%Y"), r["t"].strftime("%H:%M"), "%.1f" % f, "%.1f" % turb, "%.2f" % ph,
                     "%.0f" % alk, "%.0f" % hard,
                     ("%.2f" % r["screen"]) if r["screen"] is not None else "",
                     ("%.2f" % r["conf"]) if r["conf"] is not None else "",
                     ["JS", "TG", "BD", "ZF"][int(rng.integers(0, 4))]])
    write_csv(path(target, "lims_old"), rows,
              header=["Date", "Time", "Raw Temp (F)", "Raw Turb (NTU)", "Raw pH", "Raw Alk (mg/L)", "Raw Hard (mg/L)",
                      "Atrazine ELISA (ppb)", "Atrazine GC/MS SHL (ug/L)", "Analyst"])
    return len(rows)


def write_lims_new(target, res, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Export"
    ws.append(["Sample ID", "Sample Point", "Collected", "Analysis", "Result", "Units", "Method", "Analyst", "Status"])
    header_style(ws, 9)
    sid = 26050
    for r in res:
        if r["date"] < dt.date(2026, 5, 20):
            continue
        sid += 1
        coll = dt.datetime.combine(r["date"], r["t"]).strftime("%m/%d/%Y %H:%M")
        an = ["JS", "TG", "BD", "ZF", "BC"][int(rng.integers(0, 5))]
        ws.append(["RW-%d" % sid, "RAW-01", coll, "Temperature", round(r["raw_temp"], 1), "C", "SM 2550 B", an, "Approved"])
        ws.append(["RW-%d" % sid, "RAW-01", coll, "Turbidity", round(max(0.8, float(rng.lognormal(math.log(5.0), 0.4))), 2),
                   "NTU", "EPA 180.1", an, "Approved"])
        ws.append(["RW-%d" % sid, "RAW-01", coll, "pH", round(8.0 + float(rng.normal(0, 0.12)), 2), "SU", "SM 4500-H+ B",
                   an, "Approved"])
        if r["screen"] is not None:
            ws.append(["RW-%d" % sid, "RAW-01", coll, "Atrazine (screen)", r["screen"], "ug/L", "ELISA", an, "Approved"])
        if r["conf"] is not None:
            ws.append(["RW-%d" % sid, "RAW-01", coll, "Atrazine (confirmation)", r["conf"], "ug/L", "EPA 525.3 (SHL)",
                       "SHL", "Approved"])
    for col, wdt in zip("ABCDEFGHI", (10, 12, 17, 24, 8, 6, 17, 8, 10)):
        ws.column_dimensions[col].width = wdt
    xlsx_save(wb, path(target, "lims_new"), "Brandi Dougherty", W.DEPT, "2026-05-20T13:01:44Z", "2026-11-02T07:58:10Z")


def write_ops(target, mgd, world, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2026"
    ws.append(["Plant day (06:00 to 06:00 next day)", "Raw water pumped (MG)", "Finished water (MG)", "Alum (lb)", "Lime (lb)",
               "Chlorine (lb)", "Fluoride (lb)", "Shift lead"])
    header_style(ws, 8)
    for i, q in enumerate(mgd):
        d = W.day(i)
        fin = q * (1 - 0.034 - 0.01 * float(rng.random()))
        ws.append([d.strftime("%Y-%m-%d"), round(q, 2), round(fin, 2), int(q * 1000 * 8.34 * 22 / 1000 + rng.normal(0, 30)),
                   int(q * 1000 * 8.34 * 160 / 1000 + rng.normal(0, 200)), int(q * 8.34 * 4.1 + rng.normal(0, 8)),
                   int(q * 8.34 * 0.72 + rng.normal(0, 2)), ["Sullivan", "Frederick", "Solis", "Glass"][int(rng.integers(0, 4))]])
    for col, wdt in zip("ABCDEFGH", (30, 20, 18, 10, 10, 12, 12, 10)):
        ws.column_dimensions[col].width = wdt
    xlsx_save(wb, path(target, "ops"), "Carl Newman", W.DEPT, "2026-01-02T14:10:00Z", "2026-11-01T13:22:41Z")


def write_pac_setpoints(target, setpoints, rng):
    rows = []
    for t, v in setpoints:
        utc = local_to_utc(t)
        rows.append([utc.strftime("%Y-%m-%d %H:%M"), "PAC-FDR-1.DOSE_SP", "%.1f" % v, "Good"])
    write_csv(path(target, "pac_sp"), rows, header=["Timestamp (UTC)", "Tag", "Value", "Quality"])
    return len(rows)


def write_alarms(target, rows_local):
    """The historian's alarm and event export: UTC, to the minute, in the order the events were logged."""
    rows = []
    ops = ["", "", "", "jsullivan", "zfrederick", "bdougherty", "jsolis", "tglass"]
    last_pac = None
    for n, (t, tag, desc, kind) in enumerate(rows_local):
        utc = local_to_utc(t)
        who = ops[(n * 7 + len(desc)) % len(ops)] if kind == "ACK" else ""
        if kind == "EVT" and "RUN STATUS" in desc:
            if tag == "PAC-FDR-1":
                tripped = (desc == "RUN STATUS OFF" and last_pac is not None and last_pac[1] == "MOTOR OVERLOAD TRIP"
                           and last_pac[2] == "ALM" and (t - last_pac[0]).total_seconds() < 60)
                who = "" if tripped else ops[3 + (n % 5)]
            elif (n * 13) % 10 < 4:
                who = ops[3 + (n % 5)]
        if tag == "PAC-FDR-1":
            last_pac = (t, desc, kind)
        rows.append([utc.strftime("%Y-%m-%d %H:%M"), tag, desc, kind, who])
    write_csv(path(target, "alarms"), rows, header=["Time (UTC)", "Tag", "Description", "Type", "Operator"])
    return len(rows)


# ------------------------------------------------------------------ the lake
BUOY_DEPLOY = dt.datetime(2026, 4, 2, 13, 0)        # CST
BUOY_REHANG = dt.datetime(2026, 6, 10, 10, 0)       # CST


def buoy_depths(t_cst):
    if t_cst < BUOY_REHANG:
        return [0.5 + n for n in range(16)]
    return [1.0 + n for n in range(16)]


def write_buoy(target, rng):
    pre = ['"TOA5","MERRIN_BUOY","CR1000X","18732","CR1000X.Std.07.02","CPU:MerrinBuoy_v4.CR1X","40417","Hourly"',
           '"TIMESTAMP","RECORD","BattV_Min","PTemp_C"' + "".join(',"Temp_C(%d)"' % n for n in range(1, 17)),
           '"TS","RN","Volts","Deg C"' + ',"Deg C"' * 16,
           '"","","Min","Smp"' + ',"Smp"' * 16]
    t = BUOY_DEPLOY
    end = dt.datetime(2026, 10, 31, 23, 0)
    rec = 0
    lines = []
    dead = (dt.datetime(2026, 7, 21, 4, 0), dt.datetime(2026, 8, 1, 15, 0))
    phase = float(rng.uniform(0, 2 * math.pi))
    while t <= end:
        local = t + dt.timedelta(hours=1) if is_cdt(t) else t
        i = (local.date() - W.D0).days
        frac = (local.hour + local.minute / 60.0) / 24.0
        disp = 0.28 * math.sin(2 * math.pi * (frac + 0.12) + phase) + float(rng.normal(0, 0.05))
        vals = []
        for n, z in enumerate(buoy_depths(t)):
            zz = max(0.05, z + disp * min(1.0, z / 4.0))
            v = W.temp_at(i, zz)
            if z < 3.0:
                v += 0.9 * math.exp(-z / 1.2) * math.cos(2 * math.pi * (frac - 0.66))
            v += float(rng.normal(0, 0.02))
            if n == 8 and dead[0] <= t < dead[1]:
                vals.append('"NAN"')
            else:
                vals.append("%.3f" % v)
        batt = 12.6 + 0.6 * math.sin(2 * math.pi * (frac - 0.55)) + float(rng.normal(0, 0.03))
        ptemp = 20 + 8 * math.sin(2 * math.pi * (frac - 0.4)) + float(rng.normal(0, 0.4))
        lines.append('"%s",%d,%.2f,%.2f,%s' % (t.strftime("%Y-%m-%d %H:%M:%S"), rec, batt, ptemp, ",".join(vals)))
        rec += 1
        t += dt.timedelta(hours=1)
        if dt.datetime(2026, 6, 10, 8, 0) <= t < BUOY_REHANG:
            t = BUOY_REHANG
    p = path(target, "buoy")
    ensure(p)
    with open(p, "w", encoding="ascii", newline="") as fh:
        fh.write("\r\n".join(pre + lines) + "\r\n")
    return len(lines)


def write_buoy_log(target):
    rows = [["2026-04-02", "11:20", "Deployed", "RD/GL",
             "Float at dam buoy anchor DB-1; thermistor string 16 sensors, 1 m spacing, sensor 1 at 0.5 m below the waterline; logger on CST"],
            ["2026-04-02", "13:05", "Logging started", "RD", "Hourly table"],
            ["2026-05-12", "10:15", "Downloaded; sensors wiped", "RD", ""],
            ["2026-06-10", "08:10", "Float repair", "RD/GL", "Cracked float collar replaced; string re-hung on new collar"],
            ["2026-06-10", "10:00", "Logging restarted", "RD", "Sensor 1 now at 1.0 m below the waterline, 1 m spacing kept"],
            ["2026-07-08", "09:40", "Downloaded; sensors wiped", "GL", ""],
            ["2026-08-01", "14:55", "Sensor 9 replaced", "RD", "Sensor 9 reading NAN since 21 Jul; spare fitted at same position"],
            ["2026-09-02", "10:30", "Downloaded; sensors wiped", "RD", ""],
            ["2026-10-06", "11:10", "Downloaded", "GL", "Mixing to bottom expected within the week"],
            ["2026-10-31", "16:00", "Downloaded", "RD", "Recovery planned 2026-11-09"]]
    write_csv(path(target, "buoy_log"), rows, header=["Date", "Time (CST)", "Action", "By", "Notes"])


def spill_cfs(elev_ft):
    h = max(0.0, elev_ft - W.FULL_POOL_FT)
    return W.SPILL_C * W.SPILL_L_FT * h ** 1.5


def elev_for_spill(q_cfs):
    if q_cfs <= 0:
        return W.FULL_POOL_FT
    return W.FULL_POOL_FT + (q_cfs / (W.SPILL_C * W.SPILL_L_FT)) ** (2.0 / 3.0)


def write_dam(target, rec, rain_mm, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Daily 0800"
    ws.append([W.DAM + " daily log 2026 (readings at 08:00)"])
    ws.append(["Date", "Pool elev (ft NGVD29)", "Storage (ac-ft)", "Outlet release (cfs)", "Spillway (cfs)",
               "City withdrawal (MGD)", "Precip (in)", "Remarks"])
    header_style(ws, 8, row=2)
    elevs = []
    for r in rec:
        sp = r["spill_m3s"] / W.CFS
        el = r["surf_m"] / W.FT
        if sp > 0.5:
            el = elev_for_spill(sp)
        elevs.append(el)
        stor = W.storage_ft(min(el, W.FULL_POOL_FT)) / 1233.48 + max(0.0, el - W.FULL_POOL_FT) * W.area_ft(W.FULL_POOL_FT) / 4046.86
        rem = ""
        if r["date"] == dt.date(2026, 5, 28):
            rem = "Spillway flow over crest, debris on boom"
        if r["date"] == dt.date(2026, 9, 14):
            rem = "Outlet gate exercised"
        ws.append([r["date"].strftime("%Y-%m-%d"), round(el, 2), int(round(stor)), round(r["rel_m3s"] / W.CFS),
                   round(sp) if sp > 0.5 else 0, round(r["city_m3s"] / W.MGD, 2), round(rain_mm[r["i"]] / 25.4, 2), rem])
    for col, wdt in zip("ABCDEFGH", (11, 17, 14, 17, 13, 18, 10, 36)):
        ws.column_dimensions[col].width = wdt
    xlsx_save(wb, path(target, "dam"), "Rhonda Dixon", W.DEPT, "2026-01-02T15:31:08Z", "2026-11-01T14:02:55Z")
    return elevs


def write_acap(target):
    rows = []
    e = 801.0
    while e <= 866.0 + 1e-9:
        a = W.area_ft(min(e, W.FULL_POOL_FT)) * (1.0 + 0.0025 * max(0.0, e - W.FULL_POOL_FT))
        s = W.storage_ft(min(e, W.FULL_POOL_FT)) + max(0.0, e - W.FULL_POOL_FT) * W.FT * W.area_ft(W.FULL_POOL_FT)
        rows.append(["%.1f" % e, "%.1f" % (a / 4046.86), "%.0f" % (s / 1233.48)])
        e = round(e + 0.5, 1)
    write_csv(path(target, "acap"), rows, header=["Elevation (ft NGVD29)", "Area (acres)", "Capacity (acre-ft)"],
              preamble=["Lake Merrin area-capacity table, from the 2019 bathymetric survey (multibeam and RTK shoreline)",
                        "Prepared for the City of Brennick by Ball & Frye Engineers, March 2020"])


def write_rain(target, rain_mm):
    lines = ["MERRIN DAM IA  COOP ID 13-5528  ELEV 870 FT  OBS AT 0700 LST",
             "DAILY PRECIPITATION (INCHES)  2026",
             "DATE        PRCP"]
    for i, mm in enumerate(rain_mm):
        d = W.day(i)
        inch = mm / 25.4
        s = "T" if 0 < inch < 0.005 else "%.2f" % inch
        lines.append("%s  %6s" % (d.strftime("%Y-%m-%d"), s))
    p = path(target, "rain")
    ensure(p)
    with open(p, "w", encoding="ascii", newline="") as fh:
        fh.write("\n".join(lines) + "\n")


def write_survey(target, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "By sub-watershed"
    ws.append(["Haldane County Extension and Outreach: 2026 corn herbicide use survey, Lake Merrin sub-watersheds"])
    ws.append(["Sub-watershed", "Cropland (ac)", "Corn (ac)", "Corn treated with atrazine (ac)",
               "Mean atrazine rate (lb a.i./ac)", "Respondents", "Corn acres represented (%)"])
    header_style(ws, 7, row=2)
    for k in W.SUBS:
        applied_lb = W.APPLIED[k] / 0.45359237
        rate = {"TES": 0.92, "FEN": 0.88, "OXL": 0.95, "DUN": 0.81, "LAD": 0.70}[k]
        treated = applied_lb / rate
        corn = treated / {"TES": 0.56, "FEN": 0.61, "OXL": 0.58, "DUN": 0.49, "LAD": 0.33}[k]
        crop = corn / {"TES": 0.54, "FEN": 0.57, "OXL": 0.55, "DUN": 0.41, "LAD": 0.30}[k]
        ws.append([W.NAME[k], int(round(crop, -1)), int(round(corn, -1)), int(round(treated, -1)), rate,
                   int(rng.integers(14, 96)), int(rng.integers(61, 88))])
    ws.append([])
    ws.append(["Rates are pounds of active ingredient per treated acre, all atrazine products combined."])
    for col, wdt in zip("ABCDEFG", (18, 14, 12, 30, 28, 12, 26)):
        ws.column_dimensions[col].width = wdt
    xlsx_save(wb, path(target, "survey"), "Veronica Hunt", "Haldane County Extension and Outreach",
              "2026-09-10T18:22:00Z", "2026-09-24T20:05:13Z")


def write_nitrate(target, bottles, rng):
    rows = []
    base = dict(TES=6.8, FEN=9.4, OXL=7.9, DUN=5.6, LAD=3.1)
    for b in bottles:
        if b["kind"] != "Routine grab":
            continue
        v = base[b["k"]] * math.exp(rng.normal(0, 0.18)) * (1.3 if b["t"].month in (5, 6) else 1.0)
        rows.append([b["bottle"], SITE[b["k"]], b["t"].strftime("%m/%d/%Y"), "%.1f" % v, "mg/L as N", "SM 4500-NO3 F"])
    write_csv(path(target, "nitrate"), rows, header=["Bottle", "Site", "Collected", "Nitrate+Nitrite", "Units", "Method"])


def write_beach(target, rng):
    rows = []
    d = dt.date(2026, 5, 26)
    while d <= dt.date(2026, 9, 7):
        if d.weekday() == 0:
            for site in ("Merrin Park Beach N", "Merrin Park Beach S"):
                v = float(rng.lognormal(math.log(48), 0.9))
                rows.append([d.strftime("%Y-%m-%d"), site, "%d" % max(1, round(v)), "MPN/100 mL", "Colilert-18"])
        d += dt.timedelta(days=1)
    write_csv(path(target, "beach"), rows, header=["Date", "Site", "E. coli", "Units", "Method"])
