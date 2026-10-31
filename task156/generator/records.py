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


# ------------------------------------------------------------------------------------------------- asset register
STATIONS = [
    # id, name, address, overflow point, storage hours at average dry weather flow, standby generator
    ("PS01", "Domain Road", "2 Domain Road", "EO-01", 2.5),
    ("PS02", "Mill Street", "61 Mill Street", "EO-02", 1.8),
    ("PS03", "Riverbank Road", "118 Riverbank Road", "EO-03", 2.2),
    ("PS04", "Totara Avenue", "40A Totara Avenue", "EO-04", 3.0),
    ("PS05", "Station Road", "9 Station Road", "EO-05", 2.2),
    ("PS06", "Kowhai Street", "77 Kowhai Street", "EO-06", 3.5),
]
# ICPs: the current one, and for three stations the one closed when the supply was renewed in 2025
ICP_NOW = {"PS01": "0001836204KWD7C", "PS02": "0004410917KW3E2", "PS03": "0001836212KW9A6",
           "PS04": "0004418829KW51F", "PS05": "0001836239KWB04", "PS06": "0004421376KW8D9"}
ICP_OLD = {"PS02": ("0001836220KW2B8", dt.date(2025, 5, 12)), "PS04": ("0001836247KW6C1", dt.date(2025, 6, 3)),
           "PS06": ("0001836255KWE47", dt.date(2025, 8, 19))}
MONITORS = [  # serial, station, installed, removed
    ("OM-2114", "PS01", dt.date(2021, 9, 2), None),
    ("OM-3318", "PS02", dt.date(2022, 2, 14), dt.date(2025, 3, 20)),
    ("OM-4402", "PS02", dt.date(2025, 3, 20), None),
    ("OM-2971", "PS03", dt.date(2021, 9, 2), None),
    ("OM-2208", "PS04", dt.date(2021, 9, 6), None),
    ("OM-2207", "PS05", dt.date(2021, 9, 3), dt.date(2025, 6, 11)),
    ("OM-3318", "PS05", dt.date(2025, 6, 11), None),
    ("OM-3050", "PS06", dt.date(2021, 11, 22), None),
]


def mh_id(catch, k):
    return "MH%s-%04d" % (catch[-2:], k + 1)


@functools.lru_cache(maxsize=1)
def register():
    """The gravity mains, manholes and pump stations as the council's asset system holds them. PS03's low terrace
    sewers come from hydro's network; its upper terrace sewers and the other five catchments are drawn here, all
    above any water level the terrace bore records. A few PS03 mains replaced in place stay on the register as
    abandoned beside their replacements."""
    g = W.rng("register")
    pipes, mhs = [], []
    net = H.terrace_network()
    mhv = H.terrace_network.manholes
    n_mh = {"PS03": 0}
    t_mh_map = {}
    for k in sorted(mhv):
        t_mh_map[k] = mh_id("PS03", k)
        mhs.append(["PS03", t_mh_map[k], round(mhv[k] + g.uniform(1.6, 3.4), 2), round(mhv[k], 2)])
    n_mh["PS03"] = len(mhv)
    for p in net:
        pipes.append(dict(catch="PS03", us=t_mh_map[p["us_mh"]], ds=t_mh_map[p["ds_mh"]], L=p["L"], dia=p["dia"],
                          mat=p["mat"], yr=p["yr"], usi=p["usi"], dsi=p["dsi"], status="In service"))
    # PS03's upper terrace: a branch network draining down the escarpment into the trunk's head
    head = t_mh_map[max(k for k in mhv if k < 46)]
    base = 18.4
    for b in range(9):
        down = head
        inv = base + g.uniform(0.0, 1.2)
        for _ in range(int(g.integers(12, 24))):
            L = round(float(g.uniform(35, 95)), 1)
            rise = L * g.uniform(0.004, 0.012)
            k = n_mh["PS03"]
            n_mh["PS03"] += 1
            up = mh_id("PS03", k)
            mhs.append(["PS03", up, round(inv + rise + g.uniform(1.4, 2.8), 2), round(inv + rise, 2)])
            yr = int(g.choice([1966, 1972, 1979, 1985, 1994, 2001, 2008, 2015], p=[.1, .15, .15, .15, .15, .12, .1, .08]))
            mat = "AC" if yr < 1975 else ("PVC" if yr < 2005 else "PE")
            pipes.append(dict(catch="PS03", us=up, ds=down, L=L, dia=int(g.choice([150, 225], p=[.75, .25])), mat=mat,
                              yr=yr, usi=round(inv + rise, 3), dsi=round(inv, 3), status="In service"))
            down = up
            inv += rise
    # abandoned mains left on the register after a replacement in place (same manholes, older record)
    for p in g.choice([x for x in pipes if x["catch"] == "PS03" and x["yr"] < 1975], 11, replace=False):
        q = dict(p)
        q["status"] = "Abandoned"
        q["mat"] = "AC" if p["mat"] != "AC" else "VC"
        q["yr"] = p["yr"] - int(g.integers(8, 20))
        p["yr"] = int(g.choice([2009, 2012, 2016, 2019]))
        p["mat"] = "PE"
        pipes.append(q)
    # the other catchments
    sizes = {"PS01": 260, "PS02": 190, "PS04": 230, "PS05": 210, "PS06": 170}
    for catch, n in sizes.items():
        n_mh[catch] = 0
        k0 = n_mh[catch]
        mhs.append([catch, mh_id(catch, 0), round(g.uniform(19, 23), 2), round(g.uniform(15.6, 17.2), 2)])
        n_mh[catch] = 1
        frontier = [(mh_id(catch, k0), mhs[-1][3])]
        while len([x for x in pipes if x["catch"] == catch]) < n:
            ds, inv = frontier[int(g.integers(0, len(frontier)))]
            L = round(float(g.uniform(30, 105)), 1)
            rise = L * g.uniform(0.003, 0.011)
            up = mh_id(catch, n_mh[catch])
            n_mh[catch] += 1
            mhs.append([catch, up, round(inv + rise + g.uniform(1.3, 3.0), 2), round(inv + rise, 2)])
            yr = int(g.choice([1961, 1968, 1974, 1981, 1990, 1999, 2007, 2016], p=[.1, .14, .14, .14, .14, .12, .12, .1]))
            mat = "AC" if yr < 1975 else ("VC" if yr < 1980 else ("PVC" if yr < 2003 else "PE"))
            pipes.append(dict(catch=catch, us=up, ds=ds, L=L, dia=int(g.choice([150, 225, 300], p=[.6, .3, .1])),
                              mat=mat, yr=yr, usi=round(inv + rise, 3), dsi=round(inv, 3), status="In service"))
            frontier.append((up, inv + rise))
    order = g.permutation(len(pipes))
    out = []
    for n_, i in enumerate(sorted(range(len(pipes)), key=lambda i: (pipes[i]["catch"], order[i]))):
        p = pipes[i]
        out.append(["WW-GM-%06d" % (310000 + 7 * n_ + int(order[i]) % 7), "%s %s" % (p["catch"], dict(
            (s[0], s[1]) for s in STATIONS)[p["catch"]]), p["us"], p["ds"], "%.1f" % p["L"], p["dia"], p["mat"],
            p["yr"], "%.3f" % p["usi"], "%.3f" % p["dsi"], p["status"], "Council"])
    return out, mhs


PIPE_COLS = ["Asset ID", "Catchment", "Upstream MH", "Downstream MH", "Length (m)", "Diameter (mm)", "Material",
             "Install year", "US invert (m NZVD2016)", "DS invert (m NZVD2016)", "Status", "Owner"]
MH_COLS = ["Catchment", "Manhole ID", "Lid level (m NZVD2016)", "Invert level (m NZVD2016)"]
STATION_COLS = ["Station ID", "Name", "Address", "Engineered overflow", "ICP", "Overflow monitor (current)"]
MONITOR_COLS = ["Monitor serial", "Station ID", "Installed", "Removed"]


def write_assets(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    pipes, mhs = register()
    wb = Workbook()
    ws = wb.active
    ws.title = "Gravity mains"
    ws.append(PIPE_COLS)
    for r in pipes:
        ws.append([r[0], r[1], r[2], r[3], float(r[4]), r[5], r[6], r[7], float(r[8]), float(r[9]), r[10], r[11]])
    ws2 = wb.create_sheet("Manholes")
    ws2.append(MH_COLS)
    for c, m, lid, inv in mhs:
        ws2.append(["%s %s" % (c, dict((s[0], s[1]) for s in STATIONS)[c]), m, lid, inv])
    ws3 = wb.create_sheet("Pump stations")
    ws3.append(STATION_COLS)
    cur = {s: ser for ser, s, a, b in MONITORS if b is None}
    for sid, name, addr, eo, _ in STATIONS:
        ws3.append([sid, name, addr, eo, ICP_NOW[sid], cur[sid]])
    ws4 = wb.create_sheet("Overflow monitors")
    ws4.append(MONITOR_COLS)
    for ser, s, a, b in MONITORS:
        ws4.append([ser, s, a.strftime("%Y-%m-%d"), b.strftime("%Y-%m-%d") if b else ""])
    for w in (ws, ws2, ws3, ws4):
        for c in w[1]:
            c.font = Font(bold=True)
        w.freeze_panes = "A2"
    wb.save(path)
    return len(pipes)


# ------------------------------------------------------------------------------------------------- overflow monitors
SITE_THRESH = {"PS01": 33.0, "PS02": 29.0, "PS04": 36.0, "PS05": 31.0, "PS06": 40.0}   # mm in 6 hours
SIM = {"OM-2114": "+64 21 806 4412", "OM-3318": "+64 21 806 7730", "OM-4402": "+64 22 391 0058",
       "OM-2971": "+64 21 806 4419", "OM-2208": "+64 21 806 4487", "OM-2207": "+64 21 806 4471",
       "OM-3050": "+64 21 806 5096"}
# outages at the stations' ICPs: station, local start, hours, planned?  (those long enough spill)
OUTAGES = [
    ("PS05", dt.datetime(2024, 4, 3, 13, 10), 4.6, False),
    ("PS02", dt.datetime(2024, 7, 11, 2, 25), 4.2, False),
    ("PS01", dt.datetime(2024, 9, 18, 9, 0), 1.5, True),
    ("PS06", dt.datetime(2024, 11, 23, 8, 30), 6.0, True),
    ("PS04", dt.datetime(2024, 12, 9, 16, 40), 0.8, False),
    ("PS03", dt.datetime(2025, 1, 29, 10, 0), 1.0, True),
    ("PS01", dt.datetime(2025, 2, 14, 18, 5), 5.1, False),
    ("PS04", dt.datetime(2025, 3, 2, 14, 45), 5.0, False),
    ("PS05", dt.datetime(2025, 5, 21, 9, 30), 1.6, True),
    ("PS06", dt.datetime(2025, 6, 30, 22, 50), 4.5, False),
    ("PS02", dt.datetime(2025, 10, 8, 11, 15), 0.6, False),
    ("PS04", dt.datetime(2025, 11, 4, 9, 0), 2.5, True),
    ("PS03", dt.datetime(2026, 2, 3, 6, 40), 0.7, False),
    ("PS05", dt.datetime(2026, 4, 22, 3, 5), 3.1, False),
    ("PS06", dt.datetime(2026, 7, 14, 9, 0), 2.0, True),
]


def local_to_utc(t):
    return t.replace(tzinfo=H.AKL).astimezone(W.UTC)


def icp_at(station, d):
    if station in ICP_OLD and d < ICP_OLD[station][1]:
        return ICP_OLD[station][0]
    return ICP_NOW[station]


def monitor_at(station, d):
    for ser, s, a, b in MONITORS:
        if s == station and a <= d and (b is None or d < b):
            return ser
    raise KeyError((station, d))


@functools.lru_cache(maxsize=1)
def spills():
    """Every station's spill runs (station, start UTC, stop UTC, kind) for 2024 to October 2026: PS03's from the
    15-minute routing, the others' from the climate station's rain at each station's own threshold, with the float
    switch's chatter, plus the emergency spills of the outages longer than a station's storage."""
    C = H.clock()
    T = H.truth()
    g = W.rng("other stations", STATION_SALT)
    out = []
    M = H.meter15()
    runs, _ = H.spills15(M)
    for a, b in runs:
        t0 = M.utc0 + dt.timedelta(minutes=15 * a + int(g.integers(0, 15)))
        t1 = M.utc0 + dt.timedelta(minutes=15 * b - int(g.integers(0, 15)))
        out.append(("PS03", t0, max(t1, t0 + dt.timedelta(minutes=6)), "wet"))
    i0 = int((dt.datetime(2023, 12, 31, 11, tzinfo=W.UTC) - W.H0).total_seconds() // 3600)
    r6 = np.convolve(T.rain, np.ones(6))[:C.n]
    storage = {s[0]: s[4] for s in STATIONS}
    for st, thr in SITE_THRESH.items():
        i = i0
        while i < C.n:
            if r6[i] >= thr:
                j = i
                while j < C.n and r6[j] >= thr * 0.75:
                    j += 1
                excess = float(r6[i:j].max() - thr)
                start = C.utc[i] - dt.timedelta(hours=float(g.uniform(0.5, 2.5)))
                total = 0.6 + 0.16 * excess + float(g.uniform(0, 0.8)) + 0.12 * (j - i)
                n_runs = int(g.choice([1, 1, 2, 2, 3, 4]))
                parts = g.dirichlet(np.ones(n_runs)) * total
                t = start
                for k in range(n_runs):
                    t1 = t + dt.timedelta(hours=float(parts[k]))
                    out.append((st, t, t1, "wet"))
                    t = t1 + dt.timedelta(minutes=int(g.integers(6, 110)))
                i = j + 36
            else:
                i += 1
    for st, t_loc, hrs, planned in OUTAGES:
        if hrs > storage[st]:
            t0 = local_to_utc(t_loc + dt.timedelta(hours=storage[st] + float(g.uniform(-0.2, 0.2))))
            t1 = local_to_utc(t_loc + dt.timedelta(hours=hrs + float(g.uniform(0.15, 0.5))))
            out.append((st, t0, t1, "emergency"))
    # the monitors keep whole minutes
    out = [(s, t0.replace(second=0, microsecond=0), t1.replace(second=0, microsecond=0), k) for s, t0, t1, k in out]
    out.sort(key=lambda r: (r[0], r[1]))
    # each other station's yearly wet weather spill hours drawn clear of the half hour: the year's longest wet run
    # ends a few minutes earlier or later (the float switch's own timing)
    for st in SITE_THRESH:
        for y in (2024, 2025):
            idx = [i for i, r in enumerate(out) if r[0] == st and r[3] == "wet" and r[1].astimezone(W.NZST).year == y]
            if not idx:
                continue
            tot = sum((out[i][2] - out[i][1]).total_seconds() / 3600 for i in idx)
            target = np.floor(tot + 0.5) + float(g.uniform(-0.18, 0.18))
            dm = int(round((target - tot) * 60))
            k = max(idx, key=lambda i: out[i][2] - out[i][1])
            s, t0, t1, kind = out[k]
            nxt = [out[i][1] for i in range(len(out)) if out[i][0] == st and out[i][1] > t1]
            new_t1 = t1 + dt.timedelta(minutes=dm)
            if nxt:
                new_t1 = min(new_t1, min(nxt) - dt.timedelta(minutes=6))
            out[k] = (s, t0, max(new_t1, t0 + dt.timedelta(minutes=10)), kind)
    return out


def sms_rows():
    """The council's SMS gateway log of the monitors' messages: the sender's SIM, the received time (UTC) and the
    message text, which carries the monitor's own clock (NZST all year). A message waits in the monitor while the
    mobile network is down."""
    g = W.rng("sms", STATION_SALT)
    rows = []
    for st, t0, t1, kind in spills():
        ser = monitor_at(st, t0.astimezone(W.NZST).date())
        for word, t in (("SPILL START", t0), ("SPILL STOP", t1)):
            if t.astimezone(W.UTC) > dt.datetime(2026, 10, 31, 11, tzinfo=W.UTC):
                continue
            lag = dt.timedelta(seconds=int(g.integers(4, 70)))
            if kind == "emergency" and word == "SPILL START" and g.random() < 0.6:
                lag = dt.timedelta(minutes=int(g.integers(40, 260)))    # the cell site lost power too
            local = t.astimezone(W.NZST)
            msg = "%s %s EO %s %s" % (ser, word, local.strftime("%H:%M"), local.strftime("%d/%m/%y"))
            rows.append((t + lag, SIM[ser], msg))
    # battery and test messages
    for ser in SIM:
        d = dt.datetime(2024, 1, 15, 21, tzinfo=W.UTC)
        while d < dt.datetime(2026, 10, 31, tzinfo=W.UTC):
            st = [s for x, s, a, b in MONITORS if x == ser and a <= d.date() and (b is None or d.date() < b)]
            if st:
                local = d.astimezone(W.NZST)
                rows.append((d + dt.timedelta(seconds=int(g.integers(3, 40))), SIM[ser],
                             "%s DAILY TEST OK BATT %.2fV %s" % (ser, float(g.uniform(12.4, 13.1)), local.strftime("%d/%m/%y"))))
            d += dt.timedelta(days=int(g.integers(27, 35)))
    rows.sort()
    for t, sim, msg in rows:
        yield [iso_z(t), sim, msg]


SMS_COLS = ["received_utc", "from", "message"]


def outage_rows():
    g = W.rng("outage notices")
    n = 0
    for st, t_loc, hrs, planned in sorted(OUTAGES, key=lambda r: r[1]):
        n += 1
        end = t_loc + dt.timedelta(hours=hrs)
        icp = icp_at(st, t_loc.date())
        cause = "Planned maintenance" if planned else str(g.choice(["Equipment fault", "Vegetation", "Weather",
                                                                     "Vehicle vs pole", "Unknown"]))
        yield ["KLN-%s-%04d" % (t_loc.year, 4100 + 37 * n), icp, "Planned" if planned else "Unplanned",
               t_loc.strftime("%Y-%m-%d %H:%M"), end.strftime("%Y-%m-%d %H:%M"), cause]
    # outages at other council sites (reservoirs, the library) for the same export
    others = ["0001836263KW0F5", "0001836271KW4A9", "0004407731KWC21"]
    d = dt.datetime(2024, 2, 7, 10, 0)
    while d < dt.datetime(2026, 10, 1):
        n += 1
        hrs = float(g.uniform(0.4, 5.0))
        planned = g.random() < 0.4
        yield ["KLN-%s-%04d" % (d.year, 4100 + 37 * n), str(g.choice(others)), "Planned" if planned else "Unplanned",
               d.strftime("%Y-%m-%d %H:%M"), (d + dt.timedelta(hours=hrs)).strftime("%Y-%m-%d %H:%M"),
               "Planned maintenance" if planned else "Equipment fault"]
        d += dt.timedelta(days=int(g.integers(40, 110)), minutes=int(g.integers(0, 600)))


OUTAGE_COLS = ["notice_id", "icp", "type", "start_local", "end_local", "cause"]


def icp_rows():
    rows = []
    for sid, name, addr, eo, _ in STATIONS:
        if sid in ICP_OLD:
            old, d = ICP_OLD[sid]
            rows.append([old, "Wastewater pump station", addr + ", Rauwhero", "2009-07-01", d.strftime("%Y-%m-%d"),
                         "Low user, 3-phase"])
            rows.append([ICP_NOW[sid], "Wastewater pump station", addr + ", Rauwhero", d.strftime("%Y-%m-%d"), "",
                         "General, 3-phase"])
        else:
            rows.append([ICP_NOW[sid], "Wastewater pump station", addr + ", Rauwhero", "2009-07-01", "",
                         "Low user, 3-phase"])
    rows += [["0001836263KW0F5", "Water reservoir", "Reservoir Road, Rauwhero", "2009-07-01", "", "Low user"],
             ["0001836271KW4A9", "Water treatment plant", "15 Waterworks Road, Rauwhero", "2009-07-01", "",
              "General, 3-phase"],
             ["0004407731KWC21", "Library and service centre", "30 Main Street, Rauwhero", "2014-03-12", "",
              "General"]]
    rows.sort(key=lambda r: r[0])
    return rows


ICP_COLS = ["icp", "site", "address", "account_start", "account_end", "price_category"]


# ------------------------------------------------------------------------------------------------- water and rating
STREETS = ["Riverbank Road", "Ngaio Street", "Totara Street", "Kauri Place", "Rimu Street", "Matai Crescent",
           "Kahikatea Drive", "Puriri Road", "Miro Street", "Tawa Lane", "Hinau Street", "Rewarewa Road",
           "Manuka Close", "Karaka Street", "Titoki Avenue", "Mahoe Street", "Ponga Road", "Raupo Way",
           "Harakeke Street", "Toetoe Place", "Weir Street", "Wharf Road", "Ferry Street", "Terrace Road"]
OTHER_STREETS = ["Domain Road", "Mill Street", "Main Street", "Station Road", "Kowhai Street", "Totara Avenue",
                 "Hill Road", "School Road", "Church Street", "Park Avenue", "Ridge Road", "Bush Road"]
D0, D1 = dt.date(2023, 10, 1), W.METER_D1
WATER_SALT = 0      # the draw of the water world that leaves every Ask A figure clear of its rounding edges
STATION_SALT = 0    # the same for the other stations and Ask B


@functools.lru_cache(maxsize=1)
def water_world():
    """PS03's rating units, the dwellings each has on each day, the meters that supply them, the accounts and the
    reads, and the district's building consents. Returns one object with every list the exports print."""
    g = W.rng("water world", WATER_SALT)
    X = type("Water", (), {})()
    rus = []        # dict(vref, addr, use, suip_now, adds=[(ccc_date)], kind, catch)
    roll = 4210
    k = 0

    def vref():
        nonlocal k
        k += 1
        return "%05d/%03d.%02d" % (roll + (k // 180), (k * 7) % 900 + 1, (k * 3) % 4 * 25 % 100)

    pools = {}

    def addr(streets):
        key = tuple(streets)
        if key not in pools:
            pairs = [(s, n) for s in streets for n in range(1, 260)]
            pools[key] = [pairs[i] for i in g.permutation(len(pairs))]
        s, n = pools[key].pop()
        return "%d %s" % (n, s)

    def ccc_in_period():
        span = (dt.date(2026, 9, 30) - dt.date(2024, 1, 10)).days
        return dt.date(2024, 1, 10) + dt.timedelta(days=int(g.integers(0, span)))

    for i in range(1721):
        r = dict(vref=vref(), addr=addr(STREETS), use="Residential", base=1, adds=[], kind="house", catch="PS03")
        rus.append(r)
    for r in g.choice([r for r in rus if r["kind"] == "house"], 24, replace=False):
        r["adds"].append(ccc_in_period())
        r["kind"] = "house+minor"
    for i in range(110):
        rus.append(dict(vref=vref(), addr=addr(STREETS), use="Residential", base=2, adds=[], kind="house+minor",
                        catch="PS03"))
    flats = []
    for i in range(28):
        r = dict(vref=vref(), addr=addr(STREETS), use="Residential", base=int(g.integers(3, 7)), adds=[], kind="flats",
                 catch="PS03")
        rus.append(r)
        flats.append(r)
    for r in g.choice(flats, 4, replace=False):
        r["adds"].append(ccc_in_period())
    # Q3 2026 additions so the last quarter carries the snapshot's lead too
    late = [r for r in rus if r["kind"] == "house" and not r["adds"]]
    for r in g.choice(late, 8, replace=False):
        r["adds"].append(dt.date(2026, 7, 1) + dt.timedelta(days=int(g.integers(5, 80))))
        r["kind"] = "house+minor"
    xl = []
    for grp in range(29):
        base_addr = addr(STREETS)
        members = []
        for f in range(int(g.choice([2, 2, 3]))):
            r = dict(vref=vref(), addr="%d/%s" % (f + 1, base_addr), use="Residential", base=1, adds=[],
                     kind="cross-lease", catch="PS03", grp=grp)
            rus.append(r)
            members.append(r)
        xl.append(members)
    vacant = []
    for i in range(6):
        r = dict(vref=vref(), addr=addr(STREETS), use="Residential", base=0, adds=[], kind="vacant", catch="PS03")
        rus.append(r)
        vacant.append(r)
    for r in vacant[:4]:
        r["adds"].append(ccc_in_period())
        r["kind"] = "new house"
    for i in range(52):
        rus.append(dict(vref=vref(), addr=addr(["Riverbank Road", "Wharf Road", "Ferry Street", "Weir Street"]),
                        use=str(g.choice(["Commercial"] * 40 + ["Industrial"] * 8 + ["Community"] * 4)), base=0,
                        adds=[], kind="nonres", catch="PS03"))
    others = []
    for i in range(2650):
        others.append(dict(vref=vref(), addr=addr(OTHER_STREETS), use=str(g.choice(["Residential"] * 9 + ["Commercial"])),
                           base=int(g.choice([1] * 12 + [2, 3])), adds=[], kind="other", catch="other"))
    village = dict(vref=vref(), addr="200 Riverbank Road", use="Residential", base=38, adds=[], kind="village",
                   catch="PS03")
    rus.append(village)
    for r in rus + others:
        r["suip_now"] = r["base"] + len([d for d in r["adds"] if d <= dt.date(2026, 10, 31)])
        if r["use"] != "Residential":
            r["suip_now"] = 0 if r["kind"] == "nonres" else r["suip_now"]
    X.rus, X.others, X.xl = rus, others, xl

    # meters: one per rating unit, one per cross-lease group, a new one at each new house's connection
    meters = []
    for r in rus:
        if r["kind"] == "cross-lease":
            continue
        if r["kind"] == "vacant":
            continue
        start = D0 - dt.timedelta(days=400) if r["kind"] != "new house" else r["adds"][0] - dt.timedelta(
            days=int(g.integers(20, 60)))
        meters.append(dict(no="WM%05d" % (10000 + len(meters) * 3 + 1), rus=[r], start=start))
    for members in xl:
        meters.append(dict(no="WM%05d" % (10000 + len(meters) * 3 + 1), rus=members, start=D0 - dt.timedelta(days=400)))
    X.meters = meters

    def dwellings(r, d):
        return r["base"] + len([a for a in r["adds"] if a <= d])

    X.dwellings = dwellings
    # daily use (litres) per meter: each dwelling's own level, the season, a weekly wobble
    days = [(D0 + dt.timedelta(days=i)) for i in range((D1 - D0).days + 1)]
    X.days = days
    seas = np.array([1.0 + 0.24 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 30) / 365.25) for d in days])
    for m in meters:
        lv = []
        for r in m["rus"]:
            per = 395.0 * float(g.lognormal(0, 0.3))
            if r["use"] != "Residential":
                per = 1400.0 * float(g.lognormal(0, 0.6))
            lv.append((r, per))
        use = np.zeros(len(days))
        for i, d in enumerate(days):
            tot = 0.0
            for r, per in lv:
                n = dwellings(r, d) if r["use"] == "Residential" else 1
                tot += per * n * (0.62 if (r["kind"] == "house+minor" and n > 1) else 1.0)
            use[i] = tot * seas[i] * float(g.lognormal(0, 0.08))
        if m["start"] > D0:
            use[:(m["start"] - D0).days] = 0.0
        m["use"] = use
        m["cum0"] = float(g.uniform(80, 2400)) if m["start"] <= D0 else 0.0

    # reads: manual rounds to May 2025, the drive-by AMR monthly from July 2025, exchanges and estimates
    reads = []
    rounds = [(2023, 11), (2024, 2), (2024, 5), (2024, 8), (2024, 11), (2025, 2), (2025, 5)]
    amr = [(y, m) for y in (2025, 2026) for m in range(1, 13) if (y, m) >= (2025, 7) and (y, m) <= (2026, 10)]
    exch = set(int(i) for i in g.choice(len(meters), 70, replace=False))
    for mi, m in enumerate(meters):
        route = int(g.integers(4, 26))
        cum = np.concatenate([[m["cum0"]], m["cum0"] + np.cumsum(m["use"]) / 1000.0])
        serial = "%02dM%06d" % (int(g.integers(9, 20)), int(g.integers(100000, 999999)))
        ex_day = None
        if mi in exch:
            ex_day = D0 + dt.timedelta(days=int(g.integers(60, (D1 - D0).days - 60)))
        offset = 0.0

        def reading(d):
            return cum[(d - D0).days] - offset

        evs = []
        if m["rus"][0]["kind"] == "village":       # a large meter, read on the first of every month
            m["village"] = True
            for k in range(36):
                y, mo = 2023 + (10 + k) // 12, (10 + k) % 12 + 1
                if dt.date(y, mo, 1) <= D1:
                    evs.append((dt.date(y, mo, 1), "amr"))
            ex_day = None
        else:
            for y, mo in rounds:
                d = dt.date(y, mo, 1) + dt.timedelta(days=route + int(g.integers(-2, 3)))
                evs.append((d, "manual"))
            for y, mo in amr:
                evs.append((dt.date(y, mo, 1) + dt.timedelta(days=int(g.integers(0, 6))), "amr"))
        if ex_day:
            evs.append((ex_day, "exchange"))
        evs.sort()
        for d, kind in evs:
            if d < m["start"] or d > D1:
                continue
            if m["start"] > D0 and not reads_started(reads, m["no"]):
                reads.append([m["no"], serial, m["start"], 0.004, "I"])
            if kind == "exchange":
                reads.append([m["no"], serial, d, reading(d), "R"])
                serial = "%02dM%06d" % (int(g.integers(24, 27)), int(g.integers(100000, 999999)))
                init = round(float(g.uniform(0.0, 0.012)), 3)
                offset = cum[(d - D0).days] - init
                reads.append([m["no"], serial, d, init, "I"])
                continue
            if kind == "manual":
                if g.random() < 0.03:
                    reads.append([m["no"], serial, d, None, "E"])
                    continue
                reads.append([m["no"], serial, d, float(np.floor(reading(d))), "A"])
            else:
                reads.append([m["no"], serial, d, round(reading(d), 3), "A"])
    # the estimates the billing system wrote: the last actual plus the meter's average a day since
    last = {}
    for r in reads:
        if r[4] == "E":
            p = last.get(r[0])
            r[3] = round(p[1] + (r[2] - p[0]).days * 0.9, 0) if p else 0.0
        else:
            last[r[0]] = (r[2], r[3])
    X.reads = reads

    # accounts: one per rating unit at a time, a sale closes one and opens the next on the settlement day
    accts = []
    meter_of = {}
    for m in meters:
        for r in m["rus"]:
            meter_of[r["vref"]] = m
    n_acct = 0
    for r in rus:
        if r["vref"] not in meter_of:
            continue
        m = meter_of[r["vref"]]
        share = 100 if len(m["rus"]) == 1 else round(100.0 / len(m["rus"]), 1)
        opened = m["start"] if m["start"] > D0 else D0 - dt.timedelta(days=int(g.integers(200, 4000)))
        sales = []
        d = opened
        while True:
            d += dt.timedelta(days=int(g.exponential(4800)) + 60)
            if d > D1:
                break
            sales.append(d)
        start = opened
        for s in sales + [None]:
            n_acct += 1
            accts.append(["%07d" % (2400000 + n_acct * 13), r["vref"], m["no"], share, start, s])
            start = s
    X.accounts = accts

    # building consents across the district
    bcs = []
    n_bc = 0

    def bc(r, work, new, granted, ccc):
        nonlocal n_bc
        n_bc += 1
        bcs.append(["BC%02d%04d" % (granted.year % 100, 180 + n_bc * 3), r["vref"], r["addr"], work, new, granted, ccc])

    for r in rus:
        for a in r["adds"]:
            work = {"house+minor": "New minor dwelling", "flats": "Additional unit (conversion)",
                    "new house": "New dwelling"}[r["kind"] if r["kind"] != "house" else "house+minor"]
            bc(r, work, 1, a - dt.timedelta(days=int(g.integers(120, 330))), a)
    pool = [r for r in rus if r["use"] == "Residential"]
    for i in range(140):
        r = pool[int(g.integers(0, len(pool)))]
        gr = D0 + dt.timedelta(days=int(g.integers(-200, (D1 - D0).days - 30)))
        ccc = gr + dt.timedelta(days=int(g.integers(30, 260)))
        bc(r, str(g.choice(["Alterations", "New garage", "Deck", "Solar panels", "Bathroom renovation",
                            "Wood burner", "Retaining wall"])), 0, gr, ccc if ccc <= D1 else None)
    for i in range(6):     # minor dwellings under construction at the extract
        r = pool[int(g.integers(0, len(pool)))]
        bc(r, "New minor dwelling", 1, dt.date(2026, 3, 1) + dt.timedelta(days=int(g.integers(0, 150))), None)
    for i in range(310):
        r = others[int(g.integers(0, len(others)))]
        gr = D0 + dt.timedelta(days=int(g.integers(-200, (D1 - D0).days - 30)))
        ccc = gr + dt.timedelta(days=int(g.integers(30, 300)))
        work = str(g.choice(["Alterations", "New garage", "Deck", "New dwelling", "New minor dwelling",
                             "Commercial fit-out", "Solar panels"]))
        bc(r, work, 1 if work in ("New dwelling", "New minor dwelling") else 0, gr, ccc if ccc <= D1 else None)
    bcs.sort(key=lambda b: (b[5], b[0]))
    X.bcs = bcs
    calibrate_village(X, g)
    return X


def calibrate_village(X, g):
    """The retirement village's meter is read on the first of each month, so its quarters are exact; its monthly use
    is drawn so that each quarter's water use per dwelling sits clear of the half litre."""
    import asks as AK
    vm = next(m for m in X.meters if m.get("village"))
    for _ in range(2):
        fig = AK.water_use(_account_rows(X), _rating_rows(X), _bc_rows(X), _read_rows(X), with_dwellings=True)
        changed = False
        for key, (val, days, avg_dw, a, b) in fig.items():
            target = np.floor(val + 0.5) + float(g.uniform(-0.2, 0.2))
            if abs((val % 1.0) - 0.5) >= 0.27 and _ == 1:
                continue
            delta_l = (target - val) * days * avg_dw
            i0, i1 = (a - D0).days, (b - D0).days
            vm["use"][i0:i1] += delta_l / (i1 - i0)
            changed = True
        cum = np.concatenate([[vm["cum0"]], vm["cum0"] + np.cumsum(vm["use"]) / 1000.0])
        for r in X.reads:
            if r[0] == vm["no"]:
                r[3] = round(float(cum[(r[2] - D0).days]), 3)
        if not changed:
            break


def reads_started(reads, no):
    for r in reversed(reads[-6:]):
        if r[0] == no:
            return True
    return False


def _read_rows(X):
    out = []
    for no, serial, d, v, t in sorted(X.reads, key=lambda r: (r[0], r[2], r[4] != "R")):
        out.append([no, serial, d.strftime("%d/%m/%Y"), ("%.3f" % v) if t in ("A", "R", "I") and v % 1 else "%d" % v, t])
    return out


def read_rows():
    return _read_rows(water_world())


READ_COLS = ["meter_no", "meter_serial", "read_date", "reading_m3", "read_type"]


def _account_rows(X):
    return [[a, v, m, ("%d" % s) if s == 100 else "%.1f" % s, o.strftime("%Y-%m-%d"), c.strftime("%Y-%m-%d") if c else ""]
            for a, v, m, s, o, c in sorted(X.accounts)]


def account_rows():
    return _account_rows(water_world())


ACCOUNT_COLS = ["account_no", "valuation_ref", "meter_no", "share_pct", "opened", "closed"]


def _rating_rows(X):
    return [[r["vref"], r["addr"], r["use"], str(r["suip_now"])] for r in sorted(X.rus + X.others, key=lambda r: r["vref"])]


def rating_rows():
    return _rating_rows(water_world())


RATING_COLS = ["valuation_ref", "location", "land_use", "suip"]


def _bc_rows(X):
    return [[c, v, a, w, str(n), gr.strftime("%Y-%m-%d"), ccc.strftime("%Y-%m-%d") if ccc else ""]
            for c, v, a, w, n, gr, ccc in X.bcs]


def bc_rows():
    return _bc_rows(water_world())


BC_COLS = ["consent_no", "valuation_ref", "address", "work", "new_dwellings", "granted", "ccc_issued"]


# ------------------------------------------------------------------------------------------------- distractors
def wwtp_rows():
    """The treatment plant's daily inlet meter reading at 09:00: the whole town's flow, every station plus the gravity
    area by the plant."""
    C = H.clock()
    T = H.truth()
    g = W.rng("wwtp")
    d0 = dt.date(2024, 1, 1)
    qd = np.bincount(C.nzst_date, weights=T.q, minlength=C.nd) * 3.6
    for i in range((W.METER_D1 - d0).days):
        d = d0 + dt.timedelta(days=i)
        j = (d - dt.date(2004, 1, 1)).days
        town = qd[j] * 2.05 + 1800.0 * float(g.lognormal(0, 0.05))
        yield [d.strftime("%Y-%m-%d"), "09:00", "%.0f" % town, "Inlet magflow FT-101"]


WWTP_COLS = ["date", "reading_time", "inlet_volume_m3", "instrument"]


def works_rows():
    g = W.rng("work orders")
    items = ["Pump 1 seal replaced", "Pump 2 impeller cleared of rags", "Wet well washdown", "Float switch cleaned",
             "Level transmitter checked against dip", "Non-return valve serviced", "Odour filter media replaced",
             "Generator plug test", "Switchboard thermal scan", "Pump 1 bearing noise investigated",
             "Rising main air valve serviced", "Emergency storage chamber inspected"]
    d = dt.date(2024, 1, 9)
    n = 0
    while d < W.METER_D1:
        n += 1
        it = str(g.choice(items))
        yield ["WO-%d-%05d" % (d.year, 1200 + n * 11), d.strftime("%Y-%m-%d"), "PS03", it,
               str(g.choice(["Planned", "Planned", "Reactive"])), "%.1f" % float(g.uniform(0.5, 6.0))]
        d += dt.timedelta(days=int(g.integers(9, 40)))


WORKS_COLS = ["work_order", "date", "site", "task", "type", "hours"]
