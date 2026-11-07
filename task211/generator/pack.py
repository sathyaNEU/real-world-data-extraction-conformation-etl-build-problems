"""Cut the bundle under target/ from the clean truth: the files as the network's platform, the water company's
telemetry, the engineers, the pump controllers and the radiochemistry laboratory each write them."""
import csv
import datetime as dt
import io
import json
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import sim
import world as W

FILES = {
    "export": "mvgn_dose_rate_10min_2026Q3.csv",
    "register": "mvgn_station_register.xlsx",
    "migration": "station_code_migration_2025.csv",
    "alarm": "mvgn_alarm_config_2026Q3.json",
    "gauges": "northvale_water_raingauges_15min_2026Q3.csv",
    "gauge_sites": "northvale_water_raingauge_sites.csv",
    "procedure": "MVGN-OP-04_network_operating_procedure.pdf",
    "agreement": "MVJC_service_agreement_schedule2.pdf",
    "visits": "source_check_visits_2026Q3.xlsx",
    "certs": "check_source_certificates.pdf",
    "kits": "field_kits_register.csv",
    "sources": "sealed_source_register_2026.csv",
    "ingest": "platform_ingest_log_2026Q3.csv",
    "field": "air_sampler_field_sheets_2026Q3.xlsx",
    "pump": "air_pump_controller_log_2026Q3.csv",
    "beta": "gross_beta_results_2026Q3.xlsx",
    "national": "mvgn_annual_report_2025.pdf",
    "gammaspec": "air_filter_gamma_spectrometry_2026Q3.pdf",
}
DISTRACTORS = ["national", "gammaspec"]
HEAD = Font(bold=True)
FILL = PatternFill("solid", fgColor="DDE7F0")


def ensure(path):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)


def iso_z(t):
    return sim.when(t).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_csv(path, header, rows):
    ensure(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def sheet(wb, title, header, rows, widths=None, first=False, freeze=True, filt=True, fmts=None):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.append(header)
    for c in range(1, len(header) + 1):
        ws.cell(row=1, column=c).font = HEAD
        ws.cell(row=1, column=c).fill = FILL
        ws.cell(row=1, column=c).alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append([None if v == "" else v for v in r])
    if fmts:
        for col, fmt in fmts.items():
            for row in range(2, len(rows) + 2):
                ws.cell(row=row, column=col).number_format = fmt
    if widths:
        for k, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(k)].width = w
    if freeze:
        ws.freeze_panes = "A2"
    if filt and rows:
        ws.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(header)), len(rows) + 1)
    return ws


# ---------------------------------------------------------------- the network's own records

def export(tgt, T):
    """The platform's ten-minute export: one row per value it holds, labelled by the interval's start in UTC.
    Outstations on the old firmware send microsieverts per hour and the platform stores what it is sent. Four
    station-days were ingested twice when the platform re-read a delayed backfill."""
    S = T["S"]; R = T["rec"]
    rows = []
    a, b = R["exchange_t"]
    reingest = {(c, d) for c, d in W.REINGEST}
    for i, s in enumerate(S):
        code = s["code"]
        micro = code in W.MICRO_UNIT_STATIONS
        for t in range(W.N10):
            v = R["value"][i, t]
            if R["lost"][i, t]:
                continue
            probe = R["probe"][code]
            if code == W.PROBE_EXCHANGE[0] and t >= a:
                probe = R["probe_after"]
            unit = "uSv/h" if micro else "nSv/h"
            if math.isnan(v):
                val = ""
            elif micro:
                val = "%.3f" % (v / 1000.0)
            else:
                val = "%d" % int(v)
            row = (code, iso_z(t), val, unit, R["status"][i, t], probe)
            rows.append(row)
            if (code, sim.when(t).date()) in reingest:
                rows.append(row)
    write_csv(os.path.join(tgt, FILES["export"]),
              ["station_code", "interval_start_utc", "dose_rate", "dose_rate_unit", "status_code", "probe_serial"], rows)
    return len(rows)


def register(tgt, T):
    S = T["S"]; R = T["rec"]
    r = sim.rng("register")
    grounds = {"upland": ["heather moorland", "rough grass over granite", "short grass, peaty soil"],
               "coastal": ["grass, sandy soil", "short turf above the cliff", "grass over shingle"],
               "lowland": ["mown grass", "grass verge", "pasture", "grass, clay soil"]}
    rows = []
    for s in S:
        g = grounds[s["kind"]][int(r.integers(0, len(grounds[s["kind"]])))]
        commissioned = dt.date(2009, 3, 2) + dt.timedelta(days=int(r.integers(0, 3600)))
        serial = R["probe_after"] if s["code"] == W.PROBE_EXCHANGE[0] else R["probe"][s["code"]]
        council = W.COUNCILS[s["county"]]
        rows.append((s["code"], s["name"], council, s["e"], s["n"], s["alt"], g, "GTP-6 (GM)", serial,
                     commissioned.strftime("%d/%m/%Y"), "4G" + (" + LoRa" if T["ingest"]["backup"][s["code"]] else "")))
    rows.sort(key=lambda z: (z[2], z[1]))
    wb = Workbook()
    sheet(wb, "Stations", ["Station code", "Site name", "Council area", "Easting", "Northing", "Altitude (m)", "Ground cover",
                           "Probe type", "Probe serial", "Commissioned", "Telemetry link"], rows,
          widths=[12, 24, 30, 10, 10, 11, 26, 13, 13, 13, 12], first=True)
    path = os.path.join(tgt, FILES["register"])
    ensure(path)
    wb.save(path)


def migration(tgt):
    rows = sorted(((old, new, "14/05/2025") for new, old in W.OLD_CODES.items()), key=lambda z: z[0])
    write_csv(os.path.join(tgt, FILES["migration"]), ["outstation_code", "platform_code", "migrated_on"], rows)


def alarm_config(tgt, T):
    """The platform's alarm configuration for the quarter: each station's reference level (set from its
    second-quarter median) and its investigation and alert levels."""
    S = T["S"]
    r = sim.rng("alarm")
    st = []
    for s in sorted(S, key=lambda z: z["code"]):
        resp = T["resp"][s["code"]]
        if s["code"] == W.PROBE_EXCHANGE[0]:
            resp = 1.0
        ref = int(round(s["bg"] * resp * r.normal(0.985, 0.006)))
        st.append({"siteId": s["code"], "referenceLevel": ref, "investigationLevel": ref + 30,
                   "alertLevel": max(200, ref * 2), "validFrom": "2026-07-01T00:00:00Z"})
    doc = {"platformVersion": "4.8.2", "networkId": W.NETWORK_SHORT, "exportedAt": "2026-10-09T07:40:13Z",
           "levelUnit": "nSv/h", "sites": st}
    path = os.path.join(tgt, FILES["alarm"])
    ensure(path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    return {d["siteId"]: d["referenceLevel"] for d in st}


# ---------------------------------------------------------------- the water company's rain gauges

def gauges(tgt, T):
    """Northvale Water's tipping-bucket gauges: fifteen-minute totals at 0.2 mm, stamped in UK clock time."""
    rows = []
    for k, (gid, name, e, n) in enumerate(W.GAUGES):
        mm10 = T["rain_g"][k] * (10.0 / 60.0)
        cum = np.concatenate([[0.0], np.cumsum(mm10)])           # mm at each ten-minute boundary
        q = np.arange(0, W.N10 * 10 + 1, 15)
        cq = np.interp(q, np.arange(0, W.N10 * 10 + 1, 10), cum)
        tips = np.floor(cq / 0.2 + 1e-9)
        per = np.diff(tips) * 0.2
        for j, mm in enumerate(per):
            local = W.Q_START + dt.timedelta(minutes=15 * j) + W.BST
            rows.append((gid, local.strftime("%d/%m/%Y %H:%M"), "%.1f" % mm))
    write_csv(os.path.join(tgt, FILES["gauges"]), ["Gauge ref", "Time (GMT/BST)", "Rainfall (mm)"], rows)
    sites = [(gid, name, e, n, "tipping bucket", "0.2") for gid, name, e, n in W.GAUGES]
    write_csv(os.path.join(tgt, FILES["gauge_sites"]),
              ["gauge_id", "site_name", "easting", "northing", "gauge_type", "tip_mm"], sites)
    return len(rows)


# ---------------------------------------------------------------- source checks

def visits(tgt, T):
    """The engineers' visit sheets. Julia French records in nSv/h against platform codes and notes her jig;
    Antony Connolly records in microsieverts per hour against the outstation codes he has always used, and his
    sheet has no jig column (his kit carries one jig)."""
    a_rows, b_rows = [], []
    for c in sorted(T["checks"], key=lambda z: z["local"]):
        d = c["local"].strftime("%d/%m/%Y"); tm = c["local"].strftime("%H:%M")
        probe = T["rec"]["probe_after"] if c["code"] == W.PROBE_EXCHANGE[0] else T["rec"]["probe"][c["code"]]
        n_try = len(c["readings"])
        for k, reading in enumerate(c["readings"]):
            note = ""
            if n_try == 2 and k == 0:
                note = "source not fully seated, reseated and repeated"
            elif n_try == 2 and k == 1:
                note = "repeat"
            if c["code"] == W.PROBE_EXCHANGE[0]:
                note = "probe exchanged before check (old probe %s returned to lab)" % T["rec"]["probe"][c["code"]]
            if c["eng"] == "eng_a":
                a_rows.append((d, tm, c["code"], probe, c["kit"], c["jig"], int(round(c["background"])),
                               int(round(reading)), note))
            else:
                b_rows.append((d, tm, W.OLD_CODES[c["code"]], probe, c["kit"],
                               round(c["background"] / 1000.0, 3), round(reading / 1000.0, 3), note))
    wb = Workbook()
    sheet(wb, "A Connolly", ["Date of visit", "Time on site", "Site code", "Probe S/N", "Kit used", "Bkg (uSv/h)",
                             "Reading (uSv/h)", "Comments"], b_rows, widths=[11, 7, 9, 11, 7, 11, 13, 40],
          fmts={6: "0.000", 7: "0.000"}, first=True)
    sheet(wb, "J French", ["Visit date", "Arrived", "Station", "Probe no.", "Kit no.", "Jig", "Background (nSv/h)",
                           "With source (nSv/h)", "Remarks"], a_rows, widths=[11, 7, 9, 11, 7, 5, 12, 12, 46])
    path = os.path.join(tgt, FILES["visits"])
    ensure(path)
    wb.save(path)
    rows = [("KIT-1", "laboratory spare", "CS-0417", "J1 clamp", "12/01/2023"),
            ("KIT-2", W.PEOPLE["eng_a"], "CS-0583", "J1 clamp", "06/03/2024"),
            ("KIT-3", W.PEOPLE["eng_b"], "CS-0729", "J2 sleeve", "06/03/2024")]
    write_csv(os.path.join(tgt, FILES["kits"]), ["kit_id", "held_by", "check_source", "jig", "issued_on"], rows)
    rps = W.RPS
    rows = []
    loc = {"CS-0417": "KIT-1", "CS-0583": "KIT-2", "CS-0729": "KIT-3"}
    stock = [dt.date(2026, 1, 16), dt.date(2026, 2, 20), dt.date(2026, 3, 20), dt.date(2026, 4, 17),
             dt.date(2026, 5, 15), dt.date(2026, 6, 19), dt.date(2026, 7, 17), dt.date(2026, 8, 21),
             dt.date(2026, 9, 18)]
    events = [(d, "stock check") for d in stock] + [(dt.date(2026, 1, 9), "leak test"), (dt.date(2026, 7, 9), "leak test")]
    away0, back = W.CS0583_AWAY
    for d, what in sorted(events):
        for src_ in ("CS-0417", "CS-0583", "CS-0729"):
            where = loc[src_]
            if away0 <= d < back:
                where = {"CS-0417": "KIT-2", "CS-0583": W.RMU, "CS-0729": "KIT-3"}[src_]
            if what == "leak test":
                note = "wipe < 20 Bq, pass"
            else:
                note = "present" if where != W.RMU else "on loan for calibration"
            rows.append((d.strftime("%d/%m/%Y"), src_, "Cs-137", what, where, note, rps))
    rows.append((away0.strftime("%d/%m/%Y"), "CS-0583", "Cs-137", "transfer out", W.RMU,
                 "for calibration, carrier consignment HX/26/0412", rps))
    rows.append((back.strftime("%d/%m/%Y"), "CS-0583", "Cs-137", "transfer in", "KIT-2",
                 "returned with certificate HCX-CAL-26-0164, refitted in KIT-2", rps))
    rows.sort(key=lambda z: (dt.datetime.strptime(z[0], "%d/%m/%Y"), z[1], z[3]))
    write_csv(os.path.join(tgt, FILES["sources"]), ["entry_date", "source_serial", "nuclide", "entry_type", "held_at", "remarks",
                                                   "recorded_by"], rows)


# ---------------------------------------------------------------- telemetry receipts

def ingest(tgt, T):
    """The platform's ingest log: one row per batch received. The 4G gateway stamps receipt in UTC; the LoRa
    backup gateway, an older box, stamps it in UK clock time."""
    rows = []
    for bid, code, ch, ints, rec in T["ingest"]["rows"]:
        when = W.Q_START + dt.timedelta(minutes=rec)
        if ch == "primary":
            stamp = when.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            stamp = (when + W.BST).strftime("%d/%m/%Y %H:%M:%S")
        rows.append(("B%07d" % bid, code, "4G" if ch == "primary" else "LoRa", iso_z(min(ints)), iso_z(max(ints)),
                     len(ints), stamp))
    rows.sort(key=lambda z: z[0])
    write_csv(os.path.join(tgt, FILES["ingest"]), ["batch_id", "station_code", "link", "first_interval_start",
                                                   "last_interval_start", "n_records", "received_at"], rows)
    return len(rows)


# ---------------------------------------------------------------- air sampling

REISSUED = ("AF1-26-033", "AF3-26-032")


def clear_activity(meas, vols, factor):
    """The counted activity to the 0.001 Bq the laboratory reports, kept clear of a rounding line of the
    concentration, under every way of filling a flow dropout, by a step or two of the counting statistics."""
    for adj in (0.0, 0.002, -0.002, 0.004, -0.004, 0.006, -0.006, 0.008, -0.008):
        v = round(meas + adj, 3)
        if factor != 1.0:
            v = round(v * factor, 3)
        concs = [v / vol * 1000.0 for vol in vols]
        if all(abs((c * 100.0) % 1.0 - 0.5) / 100.0 > 0.0012 for c in concs) and \
                len({round(c, 2) for c in concs}) == 1:
            return meas + adj
    raise AssertionError("no clear activity for %r" % (vols,))


def air(tgt, T):
    wb = Workbook()
    first = True
    pump_rows = []
    lab_rows = []
    r = sim.rng("labnos")
    labno = 26_04_117
    for sampler, code, flow, style in W.AIR:
        A = T["air"][sampler]
        rows = []
        for f in A["filters"]:
            fid = "%s-26-%03d" % (sampler.replace("AS", "AF"), int(f["off"].strftime("%W")))
            f["fid"] = fid
            on, off = f["on"].strftime("%d/%m/%Y %H:%M"), f["off"].strftime("%d/%m/%Y %H:%M")
            who = W.PEOPLE["eng_a"] if f["k"] % 2 else W.PEOPLE["eng_b"]
            if style == "hourmeter":
                rows.append((fid, on, off, round(f["hm_on"], 1), round(f["hm_off"], 1), round(f["set_vol"], 0), who, ""))
            else:
                note = ""
                if sampler == "AS1" and f["on"] < dt.datetime(2026, 8, 20, 17, 0) < f["off"]:
                    note = "Pump fault 18/08; controller replaced 20/08"
                rows.append((fid, on, off, round(f["tot_on"] % 100000.0, 1), round(f["tot_off"] % 100000.0, 1),
                             who, note))
        if style == "hourmeter":
            sheet(wb, sampler, ["Filter ID", "On (local)", "Off (local)", "Hour meter on", "Hour meter off",
                                "Volume at set flow (m3)", "Changed by", "Remarks"], rows, widths=[13, 17, 17, 13, 13, 14, 16, 30],
                  first=first)
        else:
            sheet(wb, sampler, ["Filter ID", "On (local)", "Off (local)", "Totaliser on (m3)", "Totaliser off (m3)",
                                "Changed by", "Remarks"], rows, widths=[13, 17, 17, 16, 16, 16, 40], first=first)
        first = False
        for q in range(len(A["status"])):
            when = A["start"] + dt.timedelta(minutes=15 * q)
            if when >= W.Q_END:
                break
            tot = "" if sampler == "AS2" else "%.1f" % (A["tot"][q] % 100000.0)
            fl = "" if A["drop"][q] else "%.2f" % A["flows"][q]
            pump_rows.append((sampler, when.strftime("%Y-%m-%dT%H:%M:%SZ"), A["status"][q], fl, tot))
        for f in A["filters"]:
            factor = 1.083 if f["fid"] in REISSUED else 1.0
            f["meas"] = clear_activity(f["meas"], list(f["vols"].values()), factor)
            labno += int(r.integers(2, 9))
            received = (f["off"] + dt.timedelta(days=int(r.integers(1, 3)))).date()
            counted = received + dt.timedelta(days=int(r.integers(5, 8)))
            unc = max(0.04, f["meas"] * r.uniform(0.07, 0.11))
            lab_rows.append(["RS%d" % labno, f["fid"], sampler, received.strftime("%d/%m/%Y"),
                             counted.strftime("%d/%m/%Y"), round(f["meas"], 3), round(unc, 3),
                             "RCS-26-Q3-%02d" % ((f["k"] - 1) // 4 + 1), 1])
            f["labno"] = "RS%d" % labno
    path = os.path.join(tgt, FILES["field"])
    ensure(path)
    wb.save(path)
    pump_rows.sort(key=lambda z: (z[0], z[1]))
    write_csv(os.path.join(tgt, FILES["pump"]), ["sampler_id", "timestamp_utc", "pump_state", "measured_flow_m3_h", "run_totaliser_at_set_flow_m3"],
              pump_rows)
    # a recount: the laboratory re-issued report RCS-26-Q3-02 for two filters after a counter efficiency check
    reissue = []
    for row in lab_rows:
        if row[7] == "RCS-26-Q3-02" and row[1] in REISSUED:
            rr = list(row)
            rr[5] = round(row[5] * 1.083, 3)
            rr[8] = 2
            reissue.append(rr)
    lab_rows = lab_rows + reissue
    wb2 = Workbook()
    sheet(wb2, "Gross beta", ["Lab No", "Client ref", "Sampler ref", "Date received", "Date counted", "Gross beta (Bq)",
                              "Uncertainty (Bq, k=2)", "Report no.", "Issue"], lab_rows,
          widths=[11, 12, 8, 11, 11, 13, 16, 14, 8], first=True, fmts={6: "0.000", 7: "0.000"})
    path2 = os.path.join(tgt, FILES["beta"])
    wb2.save(path2)
    return len(pump_rows)


def extras(T):
    """Rows for the two distractor documents: the network's 2025 annual means and the quarter's monthly filter
    gamma spectrometry."""
    r = sim.rng("extras")
    annual = []
    q3 = {c: round(n / W.N10 * 100.0, 1) for c, n in sim.timely_counts(T).items()}
    for s in sorted(T["S"], key=lambda z: (z["county"], z["name"])):
        resp = 1.0 if s["code"] == W.PROBE_EXCHANGE[0] else T["resp"][s["code"]]
        mean = s["bg"] * resp * r.normal(1.006, 0.008)
        capture = r.uniform(95.6, 99.8)
        if round(capture, 1) == q3[s["code"]]:           # a different year's measure; keep it off this year's figure
            capture -= 0.3
        annual.append((s["code"], s["name"], mean, capture))
    gs = []
    for sampler, code, flow, style in W.AIR:
        for month in ("July", "August", "September"):
            gs.append((sampler, month, "%.2f" % r.uniform(2.1, 4.8), "%.3f" % r.uniform(0.31, 0.72),
                       "%.4f" % r.uniform(0.004, 0.011), "<%.4f" % r.uniform(0.0016, 0.0024),
                       "<%.4f" % r.uniform(0.0027, 0.0039)))
    return {"annual": annual, "gammaspec": gs}


def cut(tgt, T):
    info = {}
    info["export_rows"] = export(tgt, T)
    register(tgt, T)
    migration(tgt)
    info["reference"] = alarm_config(tgt, T)
    info["gauge_rows"] = gauges(tgt, T)
    visits(tgt, T)
    info["ingest_rows"] = ingest(tgt, T)
    info["pump_rows"] = air(tgt, T)
    return info
