"""The exports in target/, each in the shape its producing system writes: the station's SCADA historian, the regional
council's climate and groundwater archives, the council's asset register, the overflow monitors' SMS log, the lines
company's outage notices, the council's electricity site list, and the water billing, rating and building consent
extracts. Every row is computed from hydro.py's world or from the records built here."""
from __future__ import annotations

import csv
import datetime as dt
import functools
import io

import numpy as np

import hydro as H
import world as W

F_SCADA = "ps03_riverbank_rd_scada_15min_2024-2026.csv"
F_RAIN = "krc_rainfall_1187_hourly_2004-2025.csv"
F_RAIN26 = "krc_rainfall_1187_15min_2026_provisional.csv"
F_BORE = "krc_groundwater_72_1043_daily_2004-2026.csv"
F_ASSETS = "rauwhero_wastewater_assets_2026-10.xlsx"
F_MONITOR = "overflow_monitor_sms_log_2024-2026.csv"
F_OUTAGES = "kahuwera_lines_outage_notices_2024-2026.csv"
F_ICPS = "council_electricity_sites_2026-10.csv"
F_READS = "water_meter_reads_2023-2026.csv"
F_ACCOUNTS = "water_accounts_2026-11.csv"
F_RATING = "rating_information_2026-10-31.csv"
F_BC = "building_consents_2023-2026.csv"
F_WWTP = "rauwhero_wwtp_inlet_daily_2024-2026.csv"
F_WORKS = "ps03_pump_work_orders_2024-2026.csv"


def write_csv(path, cols, rows, head=None, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    for line in head or []:
        buf.write(line + ("\r\n" if crlf else "\n"))
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return n


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------------------------------------- SCADA
SCADA_GAPS = [  # comms outages: (start UTC, hours)
    (dt.datetime(2024, 3, 14, 2, 30, tzinfo=W.UTC), 7.5),
    (dt.datetime(2024, 9, 2, 21, 0, tzinfo=W.UTC), 19.25),
    (dt.datetime(2025, 1, 23, 4, 15, tzinfo=W.UTC), 3.0),
    (dt.datetime(2025, 7, 30, 13, 45, tzinfo=W.UTC), 26.5),
    (dt.datetime(2026, 2, 11, 0, 0, tzinfo=W.UTC), 5.75),
    (dt.datetime(2026, 8, 7, 18, 30, tzinfo=W.UTC), 11.0),
]


@functools.lru_cache(maxsize=1)
def scada():
    """The historian's 15-minute record: the RTU's calculated inflow (pumped flow plus the change in store, so it reads
    the pumps alone while the station spills), the wet well level and the pumps' running time, with the RTU's own
    measurement noise and the comms outages left blank."""
    M = H.meter15()
    g = W.rng("scada noise")
    calc = np.empty(M.n)
    calc[0] = M.pumped[0]
    calc[1:] = M.pumped[1:] + np.diff(M.store) / 0.9
    e = np.zeros(M.n)
    a = 0.0
    eps = g.normal(0, 1, M.n)
    for j in range(M.n):
        a = 0.6 * a + 0.8 * eps[j]
        e[j] = a
    obs = np.maximum(0.0, calc * (1 + 0.025 * e) + g.normal(0, 0.35, M.n))
    lvl = M.level + g.normal(0, 0.004, M.n)
    pumps = np.clip(M.pumped / 56.0, 0, 2)
    bad = np.zeros(M.n, dtype=bool)
    for t0, hrs in SCADA_GAPS:
        j0 = int((t0 - M.utc0).total_seconds() // 900)
        bad[j0:j0 + int(hrs * 4)] = True
    S = type("Scada", (), {})()
    S.t = [M.utc0 + dt.timedelta(minutes=15 * j) for j in range(M.n)]
    S.inflow, S.level, S.pumps, S.bad = obs, lvl, pumps, bad
    return S


def scada_rows():
    S = scada()
    for j in range(len(S.t)):
        if S.bad[j]:
            yield [iso_z(S.t[j]), "", "", "", "Bad"]
        else:
            yield [iso_z(S.t[j]), "%.1f" % S.inflow[j], "%.3f" % S.level[j], "%.2f" % S.pumps[j], "Good"]


SCADA_COLS = ["timestamp_utc", "ps03_inflow_calc_ls", "ps03_wet_well_level_m", "ps03_pumps_running", "quality"]


# ------------------------------------------------------------------------------------------------- rainfall
INFILLED = [(dt.date(2009, 4, 2), 6), (dt.date(2014, 10, 19), 3), (dt.date(2019, 1, 7), 9), (dt.date(2023, 6, 12), 2)]


def rain_archive_rows():
    """Hourly totals, NZST, stamped at the hour's end, quality coded the NEMS way: 600 verified, 500 a gap infilled
    from the Ngahere Road gauge (values present), 400 accumulated across a logger fault and spread by the archive."""
    C = H.clock()
    T = H.truth()
    infill = set()
    for d0, n in INFILLED:
        for k in range(n):
            infill.add(d0 + dt.timedelta(days=k))
    for i in range(C.n):
        if C.year[i] > 2025:
            break
        end = (C.utc[i] + dt.timedelta(hours=1)).astimezone(W.NZST)
        if end.year > 2025 and not (end.month == 1 and end.day == 1 and end.hour == 0):
            break
        d = (C.utc[i]).astimezone(W.NZST).date()
        q = "500" if d in infill else "600"
        yield [end.strftime("%d/%m/%Y %H:%M"), "%.1f" % T.rain[i], q]


RAIN_HEAD = ["Kahuwera Regional Council - Hydrometric Archive Export",
             "Site,%s (%s)" % (W.CLIMATE_SITE, W.CLIMATE_ID),
             "Measurement,Rainfall total (mm)",
             "Interval,1 hour",
             "Time zone,NZST (UTC+12:00); each total is stamped at the end of its hour",
             "Period,01/01/2004 01:00 to 01/01/2026 00:00",
             "Exported,03/11/2026 08:42",
             ""]
RAIN_COLS = ["Time (NZST)", "Rainfall (mm)", "Quality"]

RAIN26_GAP = (dt.datetime(2026, 3, 18, 23, 0, tzinfo=W.UTC), 52)   # logger fault, 15-minute steps left blank


@functools.lru_cache(maxsize=1)
def rain15_2026():
    """The 2026 telemetry at 15 minutes (UTC, interval end), each hour's tips spread over its quarters."""
    C = H.clock()
    T = H.truth()
    g = W.rng("rain 15")
    start = dt.datetime(2025, 12, 31, 11, tzinfo=W.UTC)
    i0 = int((start - W.H0).total_seconds() // 3600)
    out = []
    for i in range(i0, C.n):
        tips = int(round(T.rain[i] / 0.2))
        if tips:
            w = g.dirichlet(np.ones(4) * 0.8)
            k = g.multinomial(tips, w)
        else:
            k = [0, 0, 0, 0]
        for q in range(4):
            out.append((C.utc[i] + dt.timedelta(minutes=15 * (q + 1)), k[q] * 0.2))
    return out


def rain26_rows():
    g0, n = RAIN26_GAP
    gap_end = g0 + dt.timedelta(minutes=15 * n)
    for t, v in rain15_2026():
        if g0 < t <= gap_end:
            yield [iso_z(t), "", "Missing"]
        else:
            yield [iso_z(t), "%.1f" % v, "Provisional"]


RAIN26_COLS = ["interval_end_utc", "rainfall_mm", "status"]


# ------------------------------------------------------------------------------------------------- bore
MP_RL = 17.86       # top of casing, m NZVD2016
GROUND_RL = 17.44
BORE_MISSING = [(dt.date(2006, 2, 13), 4), (dt.date(2012, 1, 30), 9), (dt.date(2016, 3, 2), 3),
                (dt.date(2020, 2, 18), 6), (dt.date(2024, 2, 26), 2)]


def bore_rows():
    C = H.clock()
    T = H.truth()
    g = W.rng("bore")
    miss = set()
    for d0, n in BORE_MISSING:
        for k in range(n):
            miss.add(d0 + dt.timedelta(days=k))
    for i, d in enumerate(C.dates):
        if d > W.METER_D1:
            break
        if d in miss:
            yield [d.strftime("%Y-%m-%d"), "", "100"]
            continue
        depth = MP_RL - T.wt[i] + g.normal(0, 0.004)
        yield [d.strftime("%Y-%m-%d"), "%.3f" % depth, "600" if d.year < 2026 else "300"]


BORE_HEAD = ["Kahuwera Regional Council - Groundwater Level Export",
             "Site,%s (bore %s)" % (W.BORE_NAME, W.BORE),
             "Aquifer,Unconfined terrace gravels",
             "Measuring point,Top of casing at %.2f m NZVD2016 (ground %.2f m NZVD2016)" % (MP_RL, GROUND_RL),
             "Measurement,Depth to water below the measuring point (m); daily mean of 15-minute logger readings",
             "Day,NZST calendar day",
             "Exported,04/11/2026 09:15",
             ""]
BORE_COLS = ["Date", "Depth below MP (m)", "Quality"]
