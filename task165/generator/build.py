"""task165 architecture 2: writes the evidence pack into a folder from the world.

    python3 task165/generator/build.py [folder]"""
import csv
import datetime as dt
import os
import sys

import numpy as np
import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl.styles import Font

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D     # noqa: E402
import ooxml         # noqa: E402
import params as P   # noqa: E402
import world as W    # noqa: E402

TASK = os.path.dirname(HERE)
F_METER = "outfall_014_flow_monitoring_2014-2025.parquet"
F_WRP = "wrp_influent_hourly_2014-2025.csv"
F_REG = "outfall_regulator_register.csv"
F_TM7 = "TM-7_clay_street_storage_alternatives.pdf"
F_APPC = "consent_decree_appendix_C_cso_control.pdf"
F_SCADA = "northside_tank_scada_2020-2025.csv"
F_OM = "northside_tank_om_manual_section4.pdf"
F_WO = "cmms_work_orders_2020-2025.csv"
F_TIPS = "rain_gauge_tips_2014-2025.csv"
F_INV = "rain_gauge_inventory.csv"
F_FIELD = "rain_gauge_field_service_2014-2025.xlsx"
F_RIVER = "wennick_river_stage_daily_2014-2025.csv"
F_NOTIF = "cso_overflow_notifications_2025.csv"
OLD_LOGGER, NEW_LOGGER = "FM-0142", "AV-3315"


def rs(k):
    return np.random.default_rng([P.SEED, 9000 + k])


def write_csv(path, header, rows, eol="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator=eol)
        wr.writerow(header)
        wr.writerows(rows)


# ----------------------------------------------------------------------------------------------- Outfall 014 meter
def meter_rows():
    w = W.simulate()
    o = w["o14"]
    a, b = W.meter_swap()
    rng = rs(1)
    old_t, old_v, new_t, new_v = [], [], [], []
    for i in range(0, b + 1):
        old_t.append(W.est_of(i).strftime("%m/%d/%Y %H:%M"))
        v = o[i] / P.CFS_TO_MGD
        old_v.append(round(v * (1 + rng.normal(0, 0.01)) if v > 0 else 0.0, 2))
    for i in range(a, W.N):
        new_t.append(W.utc_of(i).strftime("%Y-%m-%d %H:%M:%S"))
        v = o[i]
        new_v.append(round(v * (1 + rng.normal(0, 0.008)) if v > 0 else 0.0, 3))
    return old_t, old_v, new_t, new_v


def write_meter(out):
    old_t, old_v, new_t, new_v = meter_rows()
    n0, n1 = len(old_t), len(new_t)
    tbl = pa.table({"site_id": pa.array(["OF-014"] * (n0 + n1)),
                    "logger_id": pa.array([OLD_LOGGER] * n0 + [NEW_LOGGER] * n1),
                    "reading_time": pa.array(old_t + new_t),
                    "flow": pa.array(old_v + new_v, type=pa.float64()),
                    "flow_unit": pa.array(["cfs"] * n0 + ["MGD"] * n1)})
    pq.write_table(tbl, os.path.join(out, F_METER), compression="snappy", use_dictionary=True)
    return n0 + n1


# ----------------------------------------------------------------------------------------------- plant historian
def plant_readings():
    """Each plant's hourly influent as the historian logged it: (utc hour index, value, quality)."""
    w = W.simulate()
    rng = rs(2)
    out = {}
    for plant, arr, cap in (("SS", w["ss"], P.SS_CAP), ("NS", w["ns"], P.NS_CAP)):
        vals = []
        for h in range(W.NH):
            v = arr[h]
            if v >= cap - 1e-9:
                v = cap - abs(rng.normal(0, 0.12))
            vals.append(round(v, 2))
        out[plant] = vals
    # dry-weather hours the historian lost (BAD quality, value 0): ten a plant, in settled weather
    bad = {}
    rain_h = w["rain"].mean(axis=0).reshape(W.NH, W.STEPS_PER_H).sum(axis=1)
    cum = np.convolve(rain_h, np.ones(24 * 7))[:W.NH]
    for plant, arr in (("SS", w["ss_raw"]), ("NS", w["ns"])):
        cand = np.flatnonzero((cum == 0) & (np.arange(W.NH) > 24 * 30))
        pick = sorted(rng.choice(cand, size=10, replace=False).tolist())
        bad[plant] = set()
        for h in pick:
            for k in range(int(rng.integers(1, 4))):
                if h + k < W.NH and cum[h + k] == 0:
                    bad[plant].add(h + k)
    return out, bad


def tag_of(plant, local):
    if local < dt.datetime(2021, 3, 15, 0, 0):
        return {"SS": "SS_INF_FLOW_TOT", "NS": "NS_INF_FLOW_TOT"}[plant]
    return {"SS": "SSWRP.HW.INF.Q", "NS": "NSWRP.HW.INF.Q"}[plant]


def write_wrp(out):
    vals, bad = plant_readings()
    rows = []
    for h in range(W.NH):
        u = P.START_UTC + dt.timedelta(hours=h)
        loc = u.astimezone(W.NY).replace(tzinfo=None)
        for plant in ("SS", "NS"):
            if h in bad[plant]:
                rows.append([tag_of(plant, loc), loc.strftime("%Y-%m-%d %H:%M"), "0.00", "BAD"])
            else:
                rows.append([tag_of(plant, loc), loc.strftime("%Y-%m-%d %H:%M"), "%.2f" % vals[plant][h], "GOOD"])
    write_csv(os.path.join(out, F_WRP), ["tag", "time_local", "value_mgd", "quality"], rows)
    return len(rows)


# ----------------------------------------------------------------------------------------------- register
REGISTER = [("R-01", "001", "Front Street at Mill Race", "Northside Interceptor", "Northside WRP", 5.5),
            ("R-02", "002", "Cannery Lane", "Northside Interceptor", "Northside WRP", 3.0),
            ("R-03", "003", "Bridge Street east abutment", "Northside Interceptor", "Northside WRP", 6.0),
            ("R-04", "004", "Water Street", "Northside Interceptor", "Northside WRP", 4.2),
            ("R-05", "005", "Locust Avenue", "Northside Interceptor", "Northside WRP", 3.6),
            ("R-06", "006", "Pike Street (Northside tank)", "Northside Interceptor", "Northside WRP", 7.5),
            ("R-07", "007", "Tanner Street", "Northside Interceptor", "Northside WRP", 2.4),
            ("R-08", "008", "Market Street", "Southside Interceptor", "Southside WRP", 8.0),
            ("R-09A", "009", "Ferry Street north", "Southside Interceptor", "Southside WRP", 4.5),
            ("R-09B", "009", "Ferry Street south", "Southside Interceptor", "Southside WRP", 3.5),
            ("R-10", "010", "Orchard Avenue", "Southside Interceptor", "Southside WRP", 6.5),
            ("R-11", "011", "Depot Street", "Riverside Relief Sewer", "Southside WRP", 5.0),
            ("R-12", "012", "Riverside Park", "Riverside Relief Sewer", "Southside WRP", 2.8),
            ("R-13", "013", "Wennick Avenue", "Southside Interceptor", "Southside WRP", 9.5),
            ("R-14", "014", "Clay Street", "Southside Interceptor", "Southside WRP", P.O14_REG)]


def write_register(out):
    rows = [[r, o, loc, ic, pl, "%.1f" % q, "weir and orifice" if r != "R-09B" else "orifice"]
            for r, o, loc, ic, pl, q in REGISTER]
    write_csv(os.path.join(out, F_REG), ["regulator_id", "outfall", "location", "receiving_sewer", "plant",
                                         "design_diversion_mgd", "regulator_type"], rows)
    return len(rows)


# ----------------------------------------------------------------------------------------------- Northside SCADA
def scada_rows():
    nt = W.northside_tank()
    i0 = nt["i0"]
    ioff = W.index_of_local(P.NT_TRANSDUCER_LOCAL)
    ca, cb = (W.index_of_local(x) for x in P.NT_CLEANOUT_LOCAL)
    rng = rs(3)
    rows = []
    for k in range(len(nt["vol"])):
        i = i0 + k
        loc = W.local_of(i)
        depth = W.nt_depth_of_volume(nt["vol"][k])
        if ca <= i < cb:
            level = ""
        else:
            level = "%.2f" % (depth + (P.NT_TRANSDUCER_OFFSET if i >= ioff else 0.0))
        q = nt["inflow"][k]
        fi = "%.3f" % (q * (1 + rng.normal(0, 0.01))) if q > 0 else "0.000"
        r = nt["run"][k]
        rows.append([loc.strftime("%Y-%m-%d %H:%M"), level, fi, int(r[0]), int(r[1]), int(r[2]),
                     1 if nt["over"][k] > 0 else 0])
    return rows


def write_scada(out):
    rows = scada_rows()
    write_csv(os.path.join(out, F_SCADA), ["Timestamp", "NT_LIT601_FT", "NT_FIT600_MGD", "NT_P1_RUN", "NT_P2_RUN",
                                           "NT_P3_RUN", "OF006_LSH"], rows)
    return len(rows)


# ----------------------------------------------------------------------------------------------- work orders
WO_ASSETS = [("NTPS-P1", "Northside tank pump station, pump P-1"), ("NTPS-P2", "Northside tank pump station, pump P-2"),
             ("NTPS-P3", "Northside tank pump station, pump P-3"), ("NT-TANK", "Northside storage tank"),
             ("NT-LIT601", "Northside tank level transducer"), ("NT-FIT600", "Northside tank inflow meter"),
             ("OF006-LSH", "Outfall 006 overflow detector"), ("R-14", "Clay Street regulator"),
             ("OF014-FM", "Outfall 014 flow meter"), ("SSWRP-HW", "Southside WRP headworks"),
             ("SSWRP-BS1", "Southside WRP bar screen 1"), ("NSWRP-INF", "Northside WRP influent pump station"),
             ("R-08", "Market Street regulator"), ("R-13", "Wennick Avenue regulator")]
WO_ROUTINE = ["Quarterly PM: inspect, megger test, check seals", "PM: clean and inspect, no defects",
              "Inspect after storm, cleared debris", "Annual PM, lubricate, check alignment",
              "Check calibration against portable meter, within tolerance", "Cleared rag ball at inlet",
              "Replace desiccant, check cable", "Exercise gate, grease stem"]


def write_wo(out):
    rng = rs(4)
    rows = []
    d = dt.date(2020, 5, 4)
    n = 0
    while d < dt.date(2025, 12, 31):
        a = WO_ASSETS[int(rng.integers(0, len(WO_ASSETS)))]
        n += 1
        rows.append((d, a[0], a[1], "PM" if rng.random() < 0.7 else "CM", WO_ROUTINE[int(rng.integers(0, len(WO_ROUTINE)))]))
        d += dt.timedelta(days=int(rng.integers(3, 12)))
    rows += [(dt.date(2023, 3, 6), "NTPS-P2", "Northside tank pump station, pump P-2", "CM",
              "P-2 high vibration and low amps on lead. Pulled P-2, sent to Keystone Pump Service for rebuild. Station "
              "on P-1 and P-3."),
             (dt.date(2023, 3, 14), "NTPS-P2", "Northside tank pump station, pump P-2", "CM",
              "P-2 returned from rebuild: new bearings and seals, wear rings replaced, impeller trimmed to 11.25 in "
              "after cavitation damage. Reinstalled, rotation checked, returned to service."),
             (dt.date(2023, 8, 14), "NT-TANK", "Northside storage tank", "PM",
              "Annual cleanout. Diversion closed, tank isolated and washed down. LIT-601 removed for access."),
             (dt.date(2023, 8, 23), "NT-LIT601", "Northside tank level transducer", "CM",
              "LIT-601 re-installed on new stainless bracket (old bracket corroded). Loop checked, reading OK. Tank "
              "returned to service, diversion opened."),
             (dt.date(2022, 11, 2), "NT-FIT600", "Northside tank inflow meter", "PM",
              "Verified FIT-600 against portable meter during dewatering test, within 2 percent.")]
    rows.sort(key=lambda r: (r[0], r[1]))
    out_rows = []
    for k, (d, asset, desc, typ, text) in enumerate(rows):
        wo = ("WO-%06d" % (18000 + k)) if d < dt.date(2022, 7, 1) else ("%d-%05d" % (d.year, 1000 + k))
        out_rows.append([wo, asset, desc, typ, d.strftime("%m/%d/%Y") if d < dt.date(2022, 7, 1) else d.isoformat(),
                         text])
    write_csv(os.path.join(out, F_WO), ["work_order", "asset_id", "asset_description", "type", "completed", "description"],
              out_rows)
    return len(out_rows)


# ----------------------------------------------------------------------------------------------- rain gauges
def tip_rows():
    rg = W.rain_gauges()
    rng = rs(5)
    rows = []
    for g, _, _ in P.GAUGES:
        d = rg["tips"][g]
        ts = [W.logged_time(g, s).strftime("%Y-%m-%d %H:%M:%S") for s in d["sec"]]
        rows += [[g, t] for t in ts]
        new = dict((x[0], x[2]) for x in P.GAUGES)[g]
        if new is not None:
            # the cellular platform re-sent a few buffered batches after communication gaps
            idx = [j for j, s in enumerate(d["sec"]) if W.logged_time(g, s) >= new]
            for _ in range(4):
                j = idx[int(rng.integers(0, len(idx) - 40))]
                k = int(rng.integers(8, 30))
                rows += [[g, ts[x]] for x in range(j, j + k)]
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def write_tips(out):
    rows = tip_rows()
    write_csv(os.path.join(out, F_TIPS), ["gauge_id", "tip_time"], rows)
    return len(rows)


def write_inventory(out):
    rows = [["RG-1", "Northside WRP, operations building roof", "40.4521", "-76.9310", "8", "0.01", "HOBO RG3-M",
             "2013-11-14"],
            ["RG-2", "Clay Street pump station, fenced yard", "40.4307", "-76.9126", "8", "0.01", "HOBO RG3-M",
             "2013-11-14"],
            ["RG-3", "Southside WRP, lab building lawn", "40.4148", "-76.9243", "8", "0.01", "TipLink C200",
             "2024-05-07"],
            ["RG-4", "Midtown public works yard", "40.4389", "-76.8997", "8", "0.01", "TipLink C200", "2024-05-08"]]
    write_csv(os.path.join(out, F_INV), ["gauge_id", "site", "latitude", "longitude", "orifice_in", "depth_per_tip_in",
                                         "logger_model", "logger_installed"], rows)
    return len(rows)


def write_field(out):
    rg = W.rain_gauges()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Visits"
    ws.append(["Date", "Gauge", "Technician", "Arrived", "Departed", "Notes"])
    for c in ws[1]:
        c.font = Font(bold=True)
    techs = {2014: "N. Hernandez", 2015: "N. Hernandez", 2016: "R. Okafor"}
    for v in rg["visits"]:
        y = v["date"].year
        tech = techs.get(y, "N. Hernandez" if y >= 2019 else "R. Okafor")
        ws.append([v["date"], v["gauge"], tech, v["arrive"].strftime("%H:%M"), v["depart"].strftime("%H:%M"),
                   v["note"]])
        ws.cell(ws.max_row, 1).number_format = "mm/dd/yyyy"
    ws.column_dimensions["F"].width = 90
    wb.properties.creator = "Nicholas Hernandez"
    wb.properties.lastModifiedBy = "Nicholas Hernandez"
    wb.properties.created = dt.datetime(2014, 1, 6, 15, 0)
    wb.properties.modified = dt.datetime(2026, 1, 9, 15, 20)
    wb.save(os.path.join(out, F_FIELD))
    ooxml.normalize(os.path.join(out, F_FIELD), dt.datetime(2014, 1, 6, 20, 0), dt.datetime(2026, 1, 9, 20, 20))
    return len(rg["visits"])


# ----------------------------------------------------------------------------------------------- distractors
def write_river(out):
    w = W.simulate()
    rng = rs(6)
    rain_d = w["rain"].mean(axis=0).reshape(-1, 96).sum(axis=1)
    s = 0.0
    rows = []
    for k, r in enumerate(rain_d):
        s = s * 0.86 + r
        d = dt.date(2014, 1, 1) + dt.timedelta(days=k)
        stage = 3.1 + 0.6 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 85) / 365.25) + 1.9 * s + rng.normal(0, 0.05)
        rows.append([d.isoformat(), "%.2f" % stage, "A" if d.year < 2025 else "P"])
    write_csv(os.path.join(out, F_RIVER), ["date", "mean_stage_ft", "approval"], rows)
    return len(rows)


def write_notifications(out):
    """The 2025 public notifications the overflow detectors raised, one per outfall event (no tank at 014)."""
    w = W.simulate()
    rng = rs(7)
    i25 = W.index_of_local(dt.datetime(2025, 1, 1))
    rows = []
    n = 0
    for of, factor, reg in [("014", 1.0, P.O14_REG), ("008", 0.55, 0.0), ("010", 0.7, 0.0), ("013", 0.9, 0.0),
                            ("001", 0.5, 0.0), ("003", 0.6, 0.0)]:
        if of == "014":
            series = w["o14"][i25:]
        else:
            series = np.maximum(0.0, w["o14"][i25:] * factor - rng.uniform(0.5, 3.0))
        starts = W.events(series)
        for s0 in starts:
            e = s0
            while e + 1 < len(series) and series[e + 1] > 0:
                e += 1
            n += 1
            st = W.local_of(i25 + s0)
            en = W.local_of(i25 + e + 1)
            rows.append(["N25-%04d" % n, "Outfall %s" % of, st.strftime("%m/%d/%Y %I:%M %p"),
                         en.strftime("%m/%d/%Y %I:%M %p"), "Posted to website and alert subscribers"])
    rows.sort(key=lambda r: dt.datetime.strptime(r[2], "%m/%d/%Y %I:%M %p"))
    write_csv(os.path.join(out, F_NOTIF), ["notice_id", "outfall", "discharge_start", "discharge_end", "action"], rows)
    return len(rows)


# ----------------------------------------------------------------------------------------------- the pack
def build_pack(out):
    os.makedirs(out, exist_ok=True)
    n = {}
    n[F_METER] = write_meter(out)
    n[F_WRP] = write_wrp(out)
    n[F_REG] = write_register(out)
    n[F_SCADA] = write_scada(out)
    n[F_WO] = write_wo(out)
    n[F_TIPS] = write_tips(out)
    n[F_INV] = write_inventory(out)
    n[F_FIELD] = write_field(out)
    n[F_RIVER] = write_river(out)
    n[F_NOTIF] = write_notifications(out)
    D.appendix_c(os.path.join(out, F_APPC))
    D.tm7(os.path.join(out, F_TM7))
    D.om_section4(os.path.join(out, F_OM))
    return n


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    n = build_pack(out)
    for f in sorted(os.listdir(out)):
        print("  %-52s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if f in n else ""))
