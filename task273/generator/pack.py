"""Writes the evidence pack under target/: the records the Kaitanga site and the regional council keep, in the
form each system exports them. The clean truth comes from world.py; record keeping is applied here."""
import datetime as dt
import math
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import io_util as IO
import params as P
import world as W

FILES = {
    "daily": "kaitanga_bores_daily_2014-2026.csv",
    "mb1": "MRC_MB1_groundwater_level_daily.csv",
    "register": "kaitanga_bore_register.xlsx",
    "test": "PB9_logger_LT5-2408817_2026-10.csv",
    "plan": "kaitanga_summer_bore_plan_2026-27.xlsx",
    "standard": "SWS-03_site_water_supply_security_standard.pdf",
    "permit": "MRC_water_permit_AUTH-117204.pdf",
    "telemetry": "MRC_permit_meter_telemetry_2025-26.csv",
    "icp": "pump_icp_interval_data_2025-26.csv",
    "icp_reg": "kaitanga_icp_meter_register.csv",
    "nitrate": "kaitanga_bore_nitrate_2016-2026.csv",
    "rain": "kaitanga_ews_rainfall_daily.csv",
}
DISTRACTORS = ["nitrate", "rain"]

E0, N0 = 1812640, 5808210          # NZTM2000 of PB1's headworks
SCADA_SWITCH = pd.Timestamp("2019-05-14")
OLD_TAG = {i: "KTG-BH%02d" % int(i[2:]) for i in W.ALL}
WATER_YEAR = (pd.Timestamp("2025-07-01"), pd.Timestamp("2026-06-30"))


# ---------------------------------------------------------------- the site's daily SCADA log (the spine)
def run_hours(q, cap):
    """Hours a pump ran to deliver q ML in a day at 97 per cent of its rated flow."""
    return min(24.0, 24.0 * q / (0.97 * cap)) if q > 0 else 0.0


def daily_rows(w):
    bt, takes, levels = w["bt"], w["takes"], w["levels"]
    rng = np.random.default_rng(P.SEED + 101)
    rows = []
    loggers = {i: "LT5-%d" % (2017400 + 37 * k + int(rng.integers(0, 30))) for k, i in enumerate(W.IDS)}
    swap6 = pd.Timestamp("2023-03-08")
    for d in w["days"]:
        for i in W.IDS:
            gap = rng.random() < 0.011
            # the radio links to the SB-3 and Paddock 14 headworks were replaced in June 2025 and have dropped no
            # day since; elsewhere a telemetry gap leaves no row for the bore that day
            if gap and not (i in ("PB5", "PB6", "PB7", "PB8") and d >= pd.Timestamp("2025-06-01")):
                continue
            q = takes.at[d, i]
            lev = bt.at[i, "mp_rl"] - levels.at[d, i]
            tag = OLD_TAG[i] if d < SCADA_SWITCH else i
            pwl = "" if rng.random() < 0.004 else "%.2f" % lev
            sn = loggers[i] if not (i == "PB6" and d >= swap6) else "LT5-2311864"
            rows.append([d.strftime("%Y-%m-%d"), tag, "%d" % round(q * 1000), pwl,
                         "%.1f" % run_hours(q, bt.at[i, "cap"]), sn])
    # A batch the telemetry gateway re-sent after the August 2021 outage arrives twice.
    resent = [r for r in rows if "2021-08-03" <= r[0] <= "2021-08-05"]
    out = []
    for r in rows:
        out.append(r)
        if r[0] == "2021-08-05" and r[1] == "PB8":
            out.extend(resent)
    return out


def write_daily(w, path):
    rows = daily_rows(w)
    return IO.write_csv(path, ["date_local", "tag", "take_m3", "pwl_mbmp", "pump_run_h", "logger_sn"], rows)


# ---------------------------------------------------------------- the council's monitoring bore
def write_mb1(w, path):
    rng = np.random.default_rng(P.SEED + 102)
    mb = w["mb"]
    rows = []
    for d, v in mb.items():
        protected = pd.Timestamp("2019-11-15") <= d <= pd.Timestamp("2020-04-15")
        if not protected and rng.random() < 0.012:
            continue
        q = 600 if rng.random() > 0.05 else (500 if rng.random() > 0.3 else 400)
        rows.append([d.strftime("%d/%m/%Y"), "%.3f" % v, q])
    pre = ["Site,MB1 Kaitanga Road monitoring bore (64.2119)", "Measurement,Groundwater Level [m NZVD2016]",
           "Statistic,Daily mean (NZST)", "Exported,02/11/2026 08:12", ""]
    return IO.write_csv(path, ["Date", "Value", "Quality"], rows, preamble=pre)


# ---------------------------------------------------------------- the bore register
HDR_FILL = PatternFill("solid", fgColor="DDE6EC")


def _sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for k, wdt in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wdt
    ws.freeze_panes = "A2"


def write_register(w, path):
    bt = w["bt"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Bores"
    drilled = {"PB1": "1988-03-21", "PB2": "1988-04-11", "PB3": "1996-10-02", "PB4": "1996-11-19",
               "PB5": "2004-02-09", "PB6": "2004-03-15", "PB7": "2011-08-30", "PB8": "2011-09-26",
               "PB9": "2026-08-27"}
    depth = {"PB1": 48.0, "PB2": 46.5, "PB3": 44.2, "PB4": 49.1, "PB5": 47.6, "PB6": 45.0, "PB7": 46.8,
             "PB8": 47.3, "PB9": 52.4}
    names = {"PB1": "No.1 Pumphouse", "PB2": "Bore 2", "PB3": "Mangarewa Rd bore", "PB4": "Bore 4",
             "PB5": "SB-3 east", "PB6": "SB-3 west", "PB7": "Paddock 14 north", "PB8": "Paddock 14 south",
             "PB9": "Bore 9 (new 2026)"}
    rows = []
    for i in W.ALL:
        top = round(depth[i] - 14.0 + (int(i[2]) % 3) * 0.6, 1)
        rows.append([i, names[i], "AUTH-117204", E0 + int(bt.at[i, "x"]), N0 + int(bt.at[i, "y"]), drilled[i],
                     depth[i], top, depth[i] - 0.5, round(bt.at[i, "ground"], 2), round(bt.at[i, "stick"], 2),
                     bt.at[i, "intake_mbmp"], bt.at[i, "mol_mbmp"], "in supply" if i != "PB9" else "commissioning"])
    _sheet(ws, ["Bore", "Name", "Permit", "Easting (NZTM2000)", "Northing (NZTM2000)", "Drilled", "Depth (m bgl)",
                "Screen top (m bgl)", "Screen base (m bgl)", "Ground RL (m, Moturiki 1953)", "MP above ground (m)",
                "Pump intake (m bmp)", "Minimum operating level (m bmp)", "Status"],
           rows, [7, 24, 12, 13, 13, 11, 9, 10, 10, 13, 10, 10, 13, 13])
    ws2 = wb.create_sheet("Pumps")
    prow = []
    models = {"PB1": "Grundfos SP 46-6", "PB2": "Grundfos SP 46-5", "PB3": "Lowara Z8 70/6", "PB4": "Lowara Z8 70/6",
              "PB5": "Grundfos SP 46-5", "PB6": "Grundfos SP 30-6", "PB7": "Grundfos SP 46-5",
              "PB8": "Grundfos SP 46-5", "PB9": "Grundfos SP 77-5"}
    inst = {"PB1": "2019-02-12", "PB2": "2016-06-20", "PB3": "2021-07-07", "PB4": "2018-06-25", "PB5": "2020-06-30",
            "PB6": "2017-07-11", "PB7": "2022-06-14", "PB8": "2015-07-02", "PB9": "2026-09-29"}
    for i in W.ALL:
        prow.append([i, models[i], int(bt.at[i, "kw"]), inst[i], round(bt.at[i, "cap"] * 1000 / 86.4, 1)])
    _sheet(ws2, ["Bore", "Pump", "Motor (kW)", "Installed", "Duty flow (L/s)"], prow, [7, 22, 10, 11, 12])
    ws3 = wb.create_sheet("Monitoring")
    _sheet(ws3, ["Site", "Operator", "Easting (NZTM2000)", "Northing (NZTM2000)", "Datum", "Use"],
           [["MB1", "Matarae Regional Council", E0 + 2140, N0 - 1630, "NZVD2016",
             "regional groundwater level, unpumped"]], [7, 26, 13, 13, 10, 30])
    for s in wb.worksheets:
        s.sheet_view.zoomScale = 90
    wb.save(path)
    IO.repack_ooxml(path, "Allan Morris", "Megan Pickering", "2011-10-04T21:13:00Z", "2026-10-29T03:41:00Z",
                    "Kaitanga bore register", "Ruawaro Dairy Co-operative Ltd")


# ---------------------------------------------------------------- PB9 commissioning test logger
def write_test(w, path):
    t = W.test_levels(w)
    mp = w["bt"].at["PB9", "mp_rl"]
    rows = []
    for _, r in t.iterrows():
        utc = r.local - pd.Timedelta(hours=13)
        rows.append([utc.strftime("%Y-%m-%d"), utc.strftime("%H:%M:%S"), "%.3f" % (mp - r.level_rl),
                     "%.1f" % r.discharge_ls, r.phase])
    pre = ["Logger,LT5-2408817 (PB9 pumping bore)", "Reference,measuring point (top of casing)",
           "Clock,UTC", "Operator,Waipa Drilling Ltd for Ruawaro Dairy Co-operative", ""]
    return IO.write_csv(path, ["Date", "Time", "Level_m_bmp", "Q_L_s", "Stage"], rows, preamble=pre)


# ---------------------------------------------------------------- the summer plan
def write_plan(plan, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bore plan"
    ws.append(["Kaitanga site: bore field operating plan, peak season 2026-27"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Average daily take by bore (ML/d). Prepared 28 Oct 2026 for the site drought committee."])
    ws.append([])
    months = ["Dec-26", "Jan-27", "Feb-27", "Mar-27"]
    ws.append(["Bore"] + months)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
    for i in W.ALL:
        ws.append([i] + [plan[m][i] for m in P.SUMMER_MONTHS])
    tot = ["Site total"] + [round(sum(plan[m][i] for i in W.ALL), 2) for m in P.SUMMER_MONTHS]
    ws.append(tot)
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.append([])
    ws.append(["PB9 into supply from 1 December 2026 once the UV plant on the PB9 line is signed off "
               "(expected 24 November). Dryer 4 at full rate from 7 December."])
    for k, wdt in enumerate([12, 10, 10, 10, 10], 1):
        ws.column_dimensions[get_column_letter(k)].width = wdt
    for r in ws.iter_rows(min_row=5, max_row=ws.max_row, min_col=2, max_col=5):
        for c in r:
            c.number_format = "0.00"
    wb.save(path)
    IO.repack_ooxml(path, "Megan Pickering", "Megan Pickering", "2026-10-21T22:05:00Z", "2026-10-28T02:17:00Z",
                    "Bore plan 2026-27", "Ruawaro Dairy Co-operative Ltd")


# ---------------------------------------------------------------- council permit meter telemetry (Ask B)
COUNCIL_METER = {"PB1": "WM-30455", "PB2": "WM-30456", "PB3": "WM-31690", "PB4": "WM-31702", "PB5": "WM-33119",
                 "PB6": "WM-33120", "PB7": "WM-35873", "PB8": "WM-35874"}
PB4_NEW_METER = "WM-40958"
PB4_SWAP = pd.Timestamp("2026-02-17 10:15")       # NZST
METER_BIAS = {"PB1": 1.021, "PB2": 0.986, "PB3": 1.014, "PB4": 0.979, "PB5": 1.009, "PB6": 0.992, "PB7": 1.026,
              "PB8": 0.983}
PB4_NEW_BIAS = 1.002
ROLL = {"PB1": 1_000_000.0, "PB7": 1_000_000.0}


def nz_dst(nzst):
    """True when NZ daylight time is in force at an instant given on the NZST clock: from 02:00 NZST on the last
    Sunday of September to 02:00 NZST on the first Sunday of April."""
    y = nzst.year
    d = pd.Timestamp(y, 9, 30)
    start = d - pd.Timedelta(days=(d.weekday() + 1) % 7) + pd.Timedelta(hours=2)
    d = pd.Timestamp(y, 4, 1)
    end = d + pd.Timedelta(days=(6 - d.weekday()) % 7) + pd.Timedelta(hours=2)
    return nzst >= start or nzst < end


def utc_grid():
    """Every half-hour of the 2025-26 year (local 1 July 2025 to local 30 June 2026), in UTC, with its local time."""
    u0 = WATER_YEAR[0] - pd.Timedelta(hours=12)
    u1 = WATER_YEAR[1] + pd.Timedelta(days=1) - pd.Timedelta(hours=12)
    utc = pd.date_range(u0, u1 - pd.Timedelta(minutes=30), freq="30min")
    local = pd.DatetimeIndex([u + pd.Timedelta(hours=13 if nz_dst(u + pd.Timedelta(hours=12)) else 12) for u in utc])
    return utc, local


def utc_to_local_index(utc):
    return pd.DatetimeIndex([u + pd.Timedelta(hours=13 if nz_dst(u + pd.Timedelta(hours=12)) else 12) for u in utc])


def pump_halfhours(w):
    """Per bore and UTC half-hour of the 2025-26 year, the fraction of the half-hour the pump ran: each local day's
    run hours as one block from the evening, wrapping to the small hours of the same local day."""
    bt, takes = w["bt"], w["takes"]
    rng = np.random.default_rng(P.SEED + 103)
    utc, local = utc_grid()
    ldate = local.normalize()
    groups = {}
    for k, d in enumerate(ldate):
        groups.setdefault(d, []).append(k)
    out = {}
    for i in W.IDS:
        frac = np.zeros(len(utc))
        for d, idx in groups.items():
            h = run_hours(takes.at[d, i], bt.at[i, "cap"])
            if h <= 0:
                continue
            n = len(idx)
            start = n - int(rng.integers(6, 9)) * 2           # 20:00 to 23:00 local
            need = h * 2
            k = 0
            while need > 1e-12:
                pos = idx[(start + k) % n]
                take = min(1.0, need)
                frac[pos] = take
                need -= take
                k += 1
        out[i] = frac
    return utc, local, out


def write_telemetry(w, utc, frac, path):
    """Council permit meters: cumulative totaliser every 15 minutes, NZST, for the 2025-26 year."""
    bt = w["bt"]
    rng = np.random.default_rng(P.SEED + 104)
    rows = []
    q_utc = pd.date_range(utc[0], utc[-1] + pd.Timedelta(minutes=15), freq="15min")
    nzst = q_utc + pd.Timedelta(hours=12)
    start0 = {"PB1": 971_284.3, "PB2": 412_058.9, "PB3": 655_190.1, "PB4": 288_407.6, "PB5": 503_377.0,
              "PB6": 190_662.4, "PB7": 948_811.7, "PB8": 377_120.5}
    truth = {}
    for mid0, i in PHYSICAL.items():
        rate = 0.97 * bt.at[i, "cap"] * 1000 / 48.0          # m3 per half-hour when running
        v = np.repeat(frac[i] * rate / 2.0, 2)               # m3 per quarter-hour
        tot, new_tot = start0[i], 0.0
        rec = np.zeros(len(v))
        for k, s in enumerate(nzst):
            end = s + pd.Timedelta(minutes=15)
            on_new = i == "PB4" and end > PB4_SWAP
            vol = v[k] * (PB4_NEW_BIAS if on_new else METER_BIAS[i])
            rec[k] = vol
            if on_new:
                new_tot += vol
                reading, mid = new_tot, PB4_NEW_METER
            else:
                tot += vol
                reading = tot % ROLL[i] if i in ROLL else tot
                mid = mid0
            if rng.random() < 0.0015:
                continue                                      # a missed poll
            rows.append([mid, end.strftime("%Y-%m-%d %H:%M"), "%.1f" % reading])
        truth[i] = rec
    rows.sort(key=lambda r: (r[0], r[1]))
    pre = ["Matarae Regional Council water use telemetry", "Consent holder,Ruawaro Dairy Co-operative Ltd",
           "Authorisation,AUTH-117204", "Time zone,NZST (UTC+12) all year", ""]
    return IO.write_csv(path, ["MeterID", "ReadingTime", "Totaliser_m3"], rows, preamble=pre), truth, q_utc


# ---------------------------------------------------------------- pump electricity (Ask A)
ICP = {"PB1": "0001408837KT6E1", "PB2": "0001408838KT921", "PB3": "0001408844KT3D0", "PB4": "0001408845KT9A2",
       "SB-3": "0001408861KT5C9", "SB-4": "0001408877KT0F4"}
ICP_OF = {"PB1": "PB1", "PB2": "PB2", "PB3": "PB3", "PB4": "PB4", "PB5": "SB-3", "PB6": "SB-3", "PB7": "SB-4",
          "PB8": "SB-4"}
LOAD = {"PB1": 0.915, "PB2": 0.947, "PB3": 0.882, "PB4": 0.931, "PB5": 0.906, "PB6": 0.906, "PB7": 0.921,
        "PB8": 0.921}
# The council's dataloggers were refitted in May 2023 and two pairs went back on each other's meters: the logger
# the permit lists for Bore 1 now reads Bore 2's meter and the reverse, and the same for Bores 5 and 6.
PHYSICAL = {"WM-30455": "PB2", "WM-30456": "PB1", "WM-31690": "PB3", "WM-31702": "PB4", "WM-33119": "PB6",
            "WM-33120": "PB5", "WM-35873": "PB7", "WM-35874": "PB8"}
PB2_CT = pd.Timestamp("2026-02-11 10:30")      # local; the new meter's register advance needs x40
PB2_MULT = 40


def pump_energy(w, utc, frac):
    """kWh each pump drew in each local half-hour: motor kW x load x the fraction it ran, with a slow wear
    drift on PB3 and PB7 through the year."""
    bt = w["bt"]
    out = {}
    n = len(utc)
    for i in W.IDS:
        wear = np.ones(n)
        if i == "PB3":
            wear = 1 + np.linspace(0, 0.06, n)
        out[i] = bt.at[i, "kw"] * LOAD[i] * 0.5 * frac[i] * wear
    return out


def write_icp(w, utc, local, energy, path):
    rng = np.random.default_rng(P.SEED + 105)
    rows = []
    for key, icp in ICP.items():
        members = [i for i, k in ICP_OF.items() if k == key]
        kwh = sum(energy[i] for i in members)
        base = 0.18 if key != "SB-3" else 0.31                    # headworks lighting, telemetry, heaters
        for k, s in enumerate(utc):
            v = kwh[k] + base + rng.normal(0, 0.01)
            meter = "M%s-01" % icp[-4:]
            if key == "PB2" and local[k] >= PB2_CT:
                v = v / PB2_MULT
                meter = "M%s-02" % icp[-4:]
            rows.append([icp, meter, s.strftime("%Y-%m-%dT%H:%MZ"), "%.3f" % max(v, 0.0)])
    return IO.write_csv(path, ["icp", "meter_serial", "interval_start_utc", "reg_advance"], rows)


def write_icp_register(path):
    rows = []
    for key, icp in ICP.items():
        where = {"SB-3": "Switchboard SB-3 (Bore 5 and Bore 6 pumps)",
                 "SB-4": "Switchboard SB-4, Paddock 14 (Bore 7 and Bore 8 pumps)"}.get(key, "%s pump switchboard" % key)
        rows.append([icp, where, "M%s-01" % icp[-4:], "2014-05-07" if key != "SB-4" else "2011-10-20",
                     "2026-02-11" if key == "PB2" else "", 1])
        if key == "PB2":
            rows.append([icp, where, "M%s-02" % icp[-4:], "2026-02-11", "", PB2_MULT])
    rows.append(["0001408903KTA17", "Bore 9 pump switchboard", "MA17-01", "2026-09-29", "", 1])
    return IO.write_csv(path, ["icp", "installation", "meter_serial", "installed", "removed", "multiplier"], rows)


# ---------------------------------------------------------------- distractors
def write_nitrate(path):
    rng = np.random.default_rng(P.SEED + 106)
    rows = []
    base = {"PB1": 6.1, "PB2": 7.4, "PB3": 5.2, "PB4": 4.8, "PB5": 8.9, "PB6": 9.6, "PB7": 7.7, "PB8": 6.6}
    for y in range(2016, 2027):
        for m in (2, 5, 8, 11):
            if y == 2026 and m == 11:
                continue
            for i in W.IDS:
                v = base[i] * (1 + 0.018 * (y - 2016)) * (1 + rng.normal(0, 0.06)) * (1.08 if m in (8, 11) else 1)
                rows.append(["%d-%02d-%02d" % (y, m, int(rng.integers(3, 25))), i, "%.2f" % v, "Hill Labs"])
    rows.append(["2026-09-30", "PB9", "3.42", "Hill Labs"])
    return IO.write_csv(path, ["sample_date", "bore", "nitrate_n_mg_l", "laboratory"], rows)


def write_rain(w, path):
    rng = np.random.default_rng(P.SEED + 107)
    rows = []
    for d in w["days"]:
        wet = rng.random() < (0.42 if d.month in (5, 6, 7, 8, 9) else 0.28)
        v = rng.gamma(0.8, 9.0) if wet else 0.0
        if d.year == 2020 and d.month in (1, 2, 3):
            v *= 0.35
        rows.append([d.strftime("%Y-%m-%d"), "%.1f" % v])
    return IO.write_csv(path, ["date", "rain_mm_9am"], rows)
