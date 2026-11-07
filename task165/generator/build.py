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
import parquetfix    # noqa: E402
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
CONTRACTOR = "Ridgeline Hydrometric Services"
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
    pq.write_table(tbl, os.path.join(out, F_METER), compression="snappy", use_dictionary=True, store_schema=False)
    parquetfix.drop_created_by(os.path.join(out, F_METER))
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
WO_ASSETS = [("NTPS-P1", "Northside tank pump station, pump P-1", "pump"),
             ("NTPS-P2", "Northside tank pump station, pump P-2", "pump"),
             ("NTPS-P3", "Northside tank pump station, pump P-3", "pump"), ("NT-TANK", "Northside storage tank", "tank"),
             ("NT-LIT601", "Northside tank level transducer", "instrument"),
             ("NT-FIT600", "Northside tank inflow meter", "meter"),
             ("OF006-LSH", "Outfall 006 overflow detector", "instrument"), ("R-14", "Clay Street regulator", "regulator"),
             ("OF014-FM", "Outfall 014 flow meter", "meter"), ("SSWRP-HW", "Southside WRP headworks", "headworks"),
             ("SSWRP-BS1", "Southside WRP bar screen 1", "screen"),
             ("NSWRP-INF", "Northside WRP influent pump station", "pump"),
             ("R-08", "Market Street regulator", "regulator"), ("R-13", "Wennick Avenue regulator", "regulator")]
WO_ASSETS += [("CSPS-P1", "Clay Street pump station, pump 1", "pump"), ("CSPS-P2", "Clay Street pump station, pump 2", "pump"),
              ("LAPS-P1", "Locust Avenue pump station, pump 1", "pump"), ("RVPS-P1", "Riverside pump station, pump 1", "pump"),
              ("RVPS-P2", "Riverside pump station, pump 2", "pump"), ("CLPS-P1", "Cannery Lane pump station, pump 1", "pump"),
              ("R-01", "Front Street regulator", "regulator"), ("R-03", "Bridge Street regulator", "regulator"),
              ("R-05", "Locust Avenue regulator", "regulator"), ("R-07", "Tanner Street regulator", "regulator"),
              ("R-09A", "Ferry Street north regulator", "regulator"), ("R-10", "Orchard Avenue regulator", "regulator"),
              ("R-11", "Depot Street regulator", "regulator"), ("R-12", "Riverside Park regulator", "regulator"),
              ("NSWRP-BS1", "Northside WRP bar screen 1", "screen"), ("NSWRP-BS2", "Northside WRP bar screen 2", "screen"),
              ("SSWRP-BS2", "Southside WRP bar screen 2", "screen"), ("SSWRP-GEN", "Southside WRP standby generator", "generator"),
              ("NSWRP-GEN", "Northside WRP standby generator", "generator"), ("RVPS-GEN", "Riverside PS standby generator", "generator"),
              ("OF003-FM", "Outfall 003 flow meter", "meter"), ("OF010-FM", "Outfall 010 flow meter", "meter"),
              ("NSWRP-EFM", "Northside WRP effluent flow meter", "meter"), ("SSWRP-EFM", "Southside WRP effluent flow meter", "meter"),
              ("OF008-LSH", "Outfall 008 overflow detector", "instrument"), ("OF013-LSH", "Outfall 013 overflow detector", "instrument")]
FIT_REPORTS = [
    "FIT-600 showing about 0.3 MGD with no rain for days, lead pump short cycling. Checked meter zero, fine. "
    "Suspect SG-600, passed to mechanical crew.",
    "Op on rounds: inflow meter reading flow in dry weather and P-1 cycling every few hours. Meter verified against "
    "portable, OK. Mechanical to look at the gate.",
    "Dry weather flow showing at FIT-600 (~0.3 MGD) and lead pump starting several times a day. Instrument tech "
    "checked meter, reads true. WO raised for SG-600.",
    "Northside tank: FIT-600 not at zero after storm drained down, steady trickle all week, pumps cycling. Meter OK "
    "per I&C. Refer gate to mech.",
    "Trickle into tank in dry weather again (FIT-600 ~0.35 MGD), lead pump cycling. Meter checked good. Mech to "
    "inspect SG-600 seals."]
WO_TEXT_EXTRA = {
    ("generator", "PM"): ["Monthly exercise under load 30 min, no alarms", "Annual PM: oil and filters, coolant tested, load bank 2 h"],
    ("generator", "CM"): ["Failed to start on test, replaced battery, retested OK", "Block heater out, replaced element"]}
# the maintenance planner's task texts, by asset class and order type
WO_TEXT = {
    ("pump", "PM"): ["Quarterly PM: megger test motor, check seal chamber, vibration readings normal",
                     "Annual PM: lift pump, inspect impeller and wear ring, lubricate, reinstall",
                     "Quarterly PM: check amps under load, inspect cable and float switches"],
    ("pump", "CM"): ["Pump tripped on overload, cleared rag ball from impeller, reset and tested",
                     "Seal fail alarm, moisture probe dried and reset, monitor",
                     "Lead pump not starting, replaced contactor, tested OK"],
    ("tank", "PM"): ["Monthly inspection: hatches, vents and odor control, no defects",
                     "Washdown after event, sediment flushed to sump"],
    ("tank", "CM"): ["Debris on inlet screen after storm, cleared", "Odor complaint, carbon unit media checked and topped up"],
    ("instrument", "PM"): ["Quarterly check against staff gauge, within tolerance, cleaned sensor face",
                           "Replace desiccant pack, check cable and junction box"],
    ("instrument", "CM"): ["Signal dropping out, reseated connector, loop checked",
                           "Alarm stuck on, cleaned float and housing, tested"],
    ("meter", "PM"): ["Verify calibration against portable meter, within tolerance",
                      "Clean sensor, check velocity profile, download and clear logger"],
    ("meter", "CM"): ["No data to SCADA, replaced modem battery, communication restored",
                      "Readings flat, sensor fouled with grease, cleaned and verified"],
    ("regulator", "PM"): ["Quarterly inspection: weir and orifice clear, exercised tide gate",
                          "Inspect after storm season, removed grit from chamber"],
    ("regulator", "CM"): ["Dry weather overflow reported, cleared blockage at orifice",
                          "Tide gate hung open, freed and greased hinge pins"],
    ("headworks", "PM"): ["Monthly PM: grit classifier and channel gates, lubricate, no defects",
                          "Exercise influent gates, grease stems, check limit switches"],
    ("headworks", "CM"): ["Influent gate actuator fault, reset torque switch, tested", "Grit pump plugged, cleared and restarted"],
    ("screen", "PM"): ["Monthly PM: lubricate rake chain, check tension and shear pin",
                       "Inspect rake teeth and screenings conveyor, no defects"],
    ("screen", "CM"): ["Rake jammed on rag mat, cleared, replaced shear pin", "Conveyor belt tracking off, adjusted"],
}


WO_TEXT.update(WO_TEXT_EXTRA)


def write_wo(out):
    rng = rs(4)
    rows = []
    d = dt.date(2020, 5, 4)
    n = 0
    while d < dt.date(2025, 12, 31):
        a = WO_ASSETS[int(rng.integers(0, len(WO_ASSETS)))]
        n += 1
        typ = "PM" if rng.random() < 0.7 else "CM"
        texts = WO_TEXT[(a[2], typ)]
        rows.append((d, a[0], a[1], typ, texts[int(rng.integers(0, len(texts)))]))
        d += dt.timedelta(days=int(rng.integers(1, 5)))
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
    seal_texts = ["SG-600 sluice gate seals worn, gate passing flow in dry weather. Replaced side and invert seals, "
                  "gate closed tight, checked FIT-600 at zero.",
                  "Replaced SG-600 seals (leaking past closed gate). Adjusted wedges, tested closed.",
                  "SG-600 leaking by in dry weather per operators. New seal kit installed, gate re-seated.",
                  "Sluice gate SG-600: invert seal torn, replaced. Leak-by stopped.",
                  "SG-600 seals replaced under contract; gate stroked and tested."]
    for k, (a, b, q) in enumerate(P.NT_LEAKS):
        if b.year < 2026 and b < dt.datetime(2025, 12, 31):
            rows.append((b.date(), "NT-SG600", "Northside tank diversion sluice gate", "CM", seal_texts[k]))
        rows.append(((a + dt.timedelta(days=int(rs(10 + k).integers(9, 30)))).date(), "NT-FIT600",
                     "Northside tank inflow meter", "CM",
                     FIT_REPORTS[k]))
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
    # the field maintenance contractor keeps the log from its mobilisation, the authority's history loaded into it
    wb.properties.creator = CONTRACTOR
    wb.properties.lastModifiedBy = CONTRACTOR
    wb.properties.created = dt.datetime(2025, 6, 24, 15, 10)
    wb.properties.modified = dt.datetime(2026, 1, 9, 15, 20)
    wb.save(os.path.join(out, F_FIELD))
    ooxml.normalize(os.path.join(out, F_FIELD), dt.datetime(2025, 6, 24, 19, 10), dt.datetime(2026, 1, 9, 20, 20))
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
    """The 2025 public notifications the overflow detectors raised, one per outfall event (no tank at 014). Each
    outfall's detector sees its own storm: a lag behind Clay Street, its own threshold and its own tail."""
    w = W.simulate()
    rng = rs(7)
    i25 = W.index_of_local(dt.datetime(2025, 1, 1))
    actions = {"014": ["Posted to website and Clay St alert list", "Website posting; Clay Street sign lit",
                       "Posted; Orchard Hill neighborhood list emailed"],
               "008": ["Website and alert sent; Market St sign lit", "Posted to website",
                       "Posted; marina office called"],
               "010": ["Posted to website and alert subscribers", "Website posting; text and email alert sent"],
               "013": ["Website and alert sent; downstream water intake notified",
                       "Posted; Wennick Ave boat launch sign lit", "Posted; intake operator notified by phone"],
               "001": ["Posted; county health department notified by email", "Posted to website",
                       "Alert sent to subscribers, Front St sign lit"],
               "003": ["Alert sent to subscribers, sign posted at outfall", "Website posting; Bridge St sign lit"]}
    rows = []
    n = 0
    for of, factor, lag, tail in [("014", 1.0, 0, 0), ("008", 0.55, 2, 3), ("010", 0.7, -1, 5), ("013", 0.9, 1, -2),
                                  ("001", 0.5, 3, 6), ("003", 0.6, -2, 1)]:
        if of == "014":
            series = w["o14"][i25:]
        else:
            base = np.roll(w["o14"], lag)[i25:]
            kern = np.ones(max(1, 1 + tail)) / max(1, 1 + tail) if tail > 0 else np.ones(1)
            sm = np.convolve(base, kern)[:len(base)]
            series = np.maximum(0.0, sm * factor * rng.uniform(0.9, 1.1) - rng.uniform(0.5, 3.0))
        starts = W.events(series)
        for s0 in starts:
            e = s0
            while e + 1 < len(series) and series[e + 1] > 0:
                e += 1
            n += 1
            # the detector's own trip and reset minutes, inside the first and last overflowing quarter hours
            st = W.local_of(i25 + s0) + dt.timedelta(minutes=int(rng.integers(0, 15)))
            en = W.local_of(i25 + e) + dt.timedelta(minutes=int(rng.integers(1, 15)))
            rows.append(["", "Outfall %s" % of, st.strftime("%m/%d/%Y %I:%M %p"),
                         en.strftime("%m/%d/%Y %I:%M %p"), actions[of][int(rng.integers(0, len(actions[of])))]])
    rows.sort(key=lambda r: (dt.datetime.strptime(r[2], "%m/%d/%Y %I:%M %p"), r[1]))
    for k, r in enumerate(rows):
        r[0] = "N25-%04d" % (k + 1)
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
