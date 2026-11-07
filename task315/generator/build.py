"""task315 pack builder: writes target/, golden/, generator/figures.json and metadata.json. Deterministic."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import zipfile

import numpy as np

import world as W
import routes as R
import records as RC
import remote as RM

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
EXPORT_TIME = (2026, 11, 5, 16, 42, 18)
EXPORT_TS = dt.datetime(*EXPORT_TIME).timestamp()

F_CFC = "cfc_session_export_2024-11-01_2026-10-31.csv"
F_NWE = "northway_transactions_2025-09-01_2026-10-31.jsonl"
F_CST = "cfc_charge_point_status_2025-09_2026-10.csv"
F_NST = "northway_status_notifications_2025-09_2026-10.csv"
F_REG = "svrd_fast_charging_site_register_2026-10-31.xlsx"
F_STR = "svrd_highway_stretches.csv"
F_ZEV = "zev_registrations_svrd_2026-09-30.xlsx"
F_REF = "svrd_ev_planning_reference_sheet_2026.xlsx"
F_PRJ = "long_distance_ev_trip_projection_2027.xlsx"
F_WX = "valley_weather_daily_2024-11_2026-10.csv"
F_MNT = "svrd_maintenance_window_approvals_2025-26.csv"
F_CON = "selkirk_power_connection_estimates_candidate_sites.xlsx"
F_RUL = "svrd_2027_site_package_scoring_rules.pdf"
F_AGR = "remote_site_operating_support_agreement_2024.pdf"
F_COV = "svrd_fast_charging_coverage_report_2026.pdf"

PRNG = np.random.default_rng(W.SEED + 90)


def write_csv(name, header, rows, crlf=False):
    with open(os.path.join(TARGET, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def normalise_zip(path, modified, member_time, app="Microsoft Excel", ver="16.0300"):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>" + ver.encode() + b"</AppVersion>", data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          b"\\g<1>" + modified.encode() + b"\\g<2>", data)
        out.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=member_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def wb_new(creator, title, created, modified):
    from openpyxl import Workbook
    wb = Workbook()
    p = wb.properties
    p.creator = creator
    p.lastModifiedBy = creator
    p.title = title
    p.created = created
    p.modified = modified
    return wb


def wb_save(wb, path, modified, member_time):
    wb.save(path)
    normalise_zip(path, modified, member_time)


# ------------------------------------------------------------------------------------------------ identities
def corridor_serials():
    """Charge point serials at the corridor sites, by (site code, charge point number)."""
    out = {}
    for node, sites in sorted(RC.CORRIDOR_SITES.items()):
        for svrd, code, name, n, kw in sites:
            yr = 21 + int(code[-2:]) % 3
            for j in range(1, n + 1):
                out[(code, j)] = "CP%d%05d" % (yr, int(PRNG.integers(1000, 99999)))
    return out


SERIALS = corridor_serials()
NODE_COMMUNITY = {k: v[0] for k, v in W.NODES.items()}


def _batch_time(local_end):
    """CFC exports each month's sessions in the first days of the next month."""
    y, m = local_end.year, local_end.month
    y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    day = 2 + (y * 31 + m * 7) % 4
    sec = (y * 131 + m * 977) % 7200
    return dt.datetime(y, m, day, 5, 0, 0) + dt.timedelta(seconds=sec)


# ---------------------------------------------------------------------------------------- the CFC session export
def cfc_records(corridor, units):
    """Every CFC record as exported: corridor sessions, remote sessions (split where the fault split them), and
    the corrected re-send of the remote sites' October to March records. Returns rows and the session id map."""
    recs = []
    for s in corridor:
        site = s["site"]
        u0 = RM.to_utc(s["start"])
        u1 = RM.to_utc(s["end"])
        drv = s["drv"]
        emsp = drv["token"].split("*")[1]
        recs.append(dict(kind="corridor", t0=u0, t1=u1, code=site[1], name=site[2], cp=SERIALS[(site[1], s["cp"])],
                         conn=2 if drv["model"] in ("LF4", "LFP") and site[4] <= 100 else 1, kwh=round(s["kwh"], 3),
                         soc0=s["soc0"] if drv["soc_report"] else None, soc1=s["soc1"] if drv["soc_report"] else None,
                         veh=drv["vstring"] if emsp == "CFC" else "", tok=drv["token"],
                         stop="Local" if PRNG.random() < 0.62 else ("SOCLimitReached" if s["soc1"] >= 0.79 else "EVDisconnected"),
                         batch=_batch_time(s["end"])))
    for u in units:
        if u.op != "CFC":
            continue
        site = RM.SITE[u.svrd]
        for x in u.sessions:
            emsp = x["token"].split("*")[1]
            veh = ""
            if emsp == "CFC":
                vs = RC.VEHICLE_STRINGS[x["model"]]
                veh = vs[int(x["token"][-1]) % len(vs)]
            rep = PRNG.random() > 0.06
            base = dict(kind="remote", code=site["code"], name=site["name"], cp=u.uid,
                        conn=2 if x["model"] in ("LF4", "LFP") else 1, veh=veh, tok=x["token"], stop=x["stop"])
            local_end = RM.to_local(x["end"])[0]
            sp = x.get("split")
            if sp is None:
                recs.append(dict(base, t0=x["start"], t1=x["end"], kwh=x["kwh"], soc0=x["soc0"] if rep else None,
                                 soc1=x["soc1"] if rep else None, batch=_batch_time(local_end), sess=x))
            else:
                mid = x["soc0"] + sp["e1"] * 0.92 / W.FLEET[x["model"]][2]
                recs.append(dict(base, t0=x["start"], t1=sp["cut"], kwh=sp["e1"], soc0=x["soc0"] if rep else None,
                                 soc1=mid if rep else None, batch=_batch_time(local_end), sess=x, part=1,
                                 stop="Other"))
                recs.append(dict(base, t0=sp["resume"], t1=x["end"], kwh=sp["e2"], soc0=mid if rep else None,
                                 soc1=x["soc1"] if rep else None, batch=_batch_time(local_end), sess=x, part=2))
    # session ids in order of record start, across CFC's network (the gaps are other provinces' sessions)
    recs.sort(key=lambda r: (r["t0"], r["cp"]))
    sid = 41_388_204
    for r in recs:
        sid += int(PRNG.integers(2, 9))
        r["sid"] = sid
    # the corrected re-send: every remote October to March session once, a split one under its first record's id
    resend = []
    for r in recs:
        if r["kind"] != "remote" or not (RM.SPLIT_WIN[0] <= r["sess"]["end"] < RM.SPLIT_WIN[1]):
            continue
        if r.get("part") == 2:
            continue
        x = r["sess"]
        rr = dict(r, t1=x["end"], kwh=x["kwh"], batch=RM.RESEND_AT, stop=x["stop"])
        if r.get("part") == 1:
            rr["soc1"] = x["soc1"] if r["soc0"] is not None else None
        rr.pop("part", None)
        resend.append(rr)
    rows = recs + resend
    rows.sort(key=lambda r: (r["batch"], r["sid"]))
    return rows


def _pct(v):
    return "" if v is None else str(int(round(min(1.0, max(0.01, v)) * 100)))


def write_cfc(rows):
    hdr = ["Session ID", "Site Code", "Site Name", "Charge Point", "Connector", "Start", "End", "Energy (kWh)",
           "SoC Start (%)", "SoC End (%)", "Vehicle", "Auth ID", "Stop Reason", "Exported (UTC)"]
    out = []
    for r in rows:
        out.append([r["sid"], r["code"], r["name"], r["cp"], r["conn"], RM.fmt_local(r["t0"]), RM.fmt_local(r["t1"]),
                    "%.3f" % r["kwh"], _pct(r["soc0"]), _pct(r["soc1"]), r["veh"], r["tok"], r["stop"],
                    RM.fmt_utc(r["batch"])])
    write_csv(F_CFC, hdr, out)
    return len(out)


# ------------------------------------------------------------------------------------------ Northway exports
def write_northway(units):
    recs = []
    reg = {}
    for u in units:
        if u.op != "NWE":
            continue
        reg[u.uid] = int(PRNG.integers(3_000_000, 26_000_000))
        for x in u.sessions:
            recs.append((x["start"], u, x))
    recs.sort(key=lambda r: (r[0], r[1].uid))
    tid = 5_120_331
    lines = []
    for t0, u, x in recs:
        tid += int(PRNG.integers(1, 4))
        wh = int(round(x["kwh"] * 1000))
        reg[u.uid] += int(PRNG.integers(0, 40))
        m0 = reg[u.uid]
        reg[u.uid] += wh
        rec = {"transaction_id": tid, "charge_box_id": u.station, "connector_id": int(u.uid.rsplit("*", 1)[1]),
               "evse_id": u.uid, "id_tag": x["token"], "start_timestamp": RM.fmt_utc(x["start"]),
               "stop_timestamp": RM.fmt_utc(x["end"]), "meter_start": m0, "meter_stop": reg[u.uid],
               "stop_reason": x["stop"]}
        lines.append(json.dumps(rec, separators=(",", ":")))
    with open(os.path.join(TARGET, F_NWE), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)


def write_status(cfc_status, nwe_status):
    vend = {"Faulted": ["", "E-217", "E-104", "IMD fault", "rectifier module 2", "E-311"], "Unavailable": ["maintenance"],
            "Available": [""]}
    rows = []
    for r in sorted(cfc_status, key=lambda r: (r["t"], r["cp"])):
        info = vend.get(r["status"], [""])[int(r["t"].timestamp()) % len(vend.get(r["status"], [""]))]
        rows.append([RM.fmt_local(r["t"]), r["cp"], r["status"], r["code"], info])
    write_csv(F_CST, ["Event Time", "Charge Point", "Status", "Error Code", "Vendor Info"], rows)
    rows = [[RM.fmt_utc(r["t"]), r["box"], r["conn"], r["status"], r["code"]]
            for r in sorted(nwe_status, key=lambda r: (r["t"], r["box"], r["conn"]))]
    write_csv(F_NST, ["timestamp_utc", "charge_box_id", "connector_id", "status", "error_code"], rows)
    return len(cfc_status), len(nwe_status)


# ------------------------------------------------------------------------------------------- district files
def write_register():
    wb = wb_new("Infrastructure Services", "Fast charging site register", dt.datetime(2023, 3, 14, 10, 7, 52),
                dt.datetime(2026, 11, 2, 9, 18, 37))
    ws = wb.active
    ws.title = "Sites"
    cols = ["Site ID", "Site Name", "Community", "Highway", "Operator", "Operator Site Code", "Programme", "In Service",
            "Charge Points", "Power (kW)", "Charge Point IDs"]
    ws.append(cols)
    hw = {}
    for name, seq in W.HIGHWAYS.items():
        for n in seq:
            hw.setdefault(n, name)
    rows = []
    insvc = {"SV-FC-01": (2021, 9, 14), "SV-FC-03": (2022, 6, 2), "SV-FC-06": (2021, 11, 23), "SV-FC-07": (2022, 8, 30),
             "SV-FC-09": (2022, 10, 18), "SV-FC-11": (2022, 5, 11), "SV-FC-12": (2023, 7, 6), "SV-FC-14": (2023, 4, 19),
             "SV-FC-16": (2023, 9, 26), "SV-FC-19": (2024, 3, 12)}
    for node, sites in RC.CORRIDOR_SITES.items():
        for svrd, code, name, n, kw in sites:
            ids = ", ".join(SERIALS[(code, j)] for j in range(1, n + 1))
            rows.append([svrd, name, NODE_COMMUNITY[node], hw[node], "Columbia Fast Charge Ltd.", code, "Corridor",
                         dt.datetime(*insvc[svrd]), n, kw, ids])
    for s in RM.SITES:
        op = "Columbia Fast Charge Ltd." if s["op"] == "CFC" else "Northway EV Networks Inc."
        rows.append([s["svrd"], s["name"] + (" Community Hall" if s["name"] == "Glenrae" else ""), s["name"], "",
                     op, s["code"], "Remote Operating Support 2024",
                     dt.datetime(s["commissioned"].year, s["commissioned"].month, s["commissioned"].day),
                     len(s["units"]), s["kw"], ", ".join(s["units"])])
    rows.sort(key=lambda r: r[0])
    for r in rows:
        ws.append(r)
    for c in ws["H"][1:]:
        c.number_format = "yyyy-mm-dd"
    for col, wdt in zip("ABCDEFGHIJK", [10, 30, 16, 20, 27, 18, 30, 12, 13, 11, 44]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A2"
    wb_save(wb, os.path.join(TARGET, F_REG), "2026-11-02T17:18:37Z", (2026, 11, 2, 9, 18, 38))


def write_stretches():
    rows = []
    for sid, (a, b, hwy, km, cl, de, ex) in W.STRETCHES.items():
        rows.append([sid, hwy, W.NODES[a][0], W.NODES[b][0], "%.1f" % km, W.NODES[a][1], W.NODES[b][1], cl, de,
                     80 if hwy == "Cedar Pass Highway" else (90 if hwy == "Sable Highway" else 100)])
    write_csv(F_STR, ["stretch_id", "highway", "from_community", "to_community", "length_km", "from_elevation_m",
                      "to_elevation_m", "climb_m", "descent_m", "posted_kmh"], rows)


PHEV = [("TOYOTA", "RAV4 PRIME", 214), ("MITSUBISHI", "OUTLANDER PHEV", 163), ("CHRYSLER", "PACIFICA PHEV", 58),
        ("FORD", "ESCAPE PHEV", 77)]


def write_zev():
    wb = wb_new("Data and Analytics", "ZEV registrations by model", dt.datetime(2026, 10, 14, 13, 2, 19),
                dt.datetime(2026, 10, 14, 13, 2, 19))
    ws = wb.active
    ws.title = "Registrations"
    ws.append(["Zero-emission light-duty vehicles registered in the Selkirk Valley Regional District at 30 September 2026"])
    ws.append([])
    ws.append(["Make", "Model", "Model Year", "Fuel Type", "Registered"])
    rows = []
    allm = dict(W.FLEET)
    allm.update(W.SMALL_MODELS)
    for k, v in allm.items():
        make, model = v[1].split(" ", 1)
        if make in ("FORD", "VOLKSWAGEN") and model.startswith(("MUSTANG", "F-150", "ID.4")):
            pass
        years = list(range(2019, 2027)) if k not in ("EQX", "R1S", "F15", "MME", "IQ5", "EV6", "ID4") else list(range(2021, 2027))
        if k == "EQX":
            years = [2024, 2025, 2026]
        w = PRNG.dirichlet(np.ones(len(years)) * 2.5)
        cnt = np.floor(w * v[5]).astype(int)
        cnt[int(np.argmax(w))] += v[5] - int(cnt.sum())
        for y, c in zip(years, cnt):
            if c > 0:
                rows.append([make, model, int(y), "BEV", int(c)])
    for make, model, n in PHEV:
        rows.append([make, model, 2023, "PHEV", n // 2])
        rows.append([make, model, 2025, "PHEV", n - n // 2])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    for r in rows:
        ws.append(r)
    ws.append([])
    ws.append(["Counts are vehicles with a valid registration and an address in the regional district on the extract date."])
    for col, wdt in zip("ABCDE", [14, 26, 12, 10, 12]):
        ws.column_dimensions[col].width = wdt
    wb_save(wb, os.path.join(TARGET, F_ZEV), "2026-10-14T20:02:19Z", (2026, 10, 14, 13, 2, 20))
    return rows


def write_reference():
    wb = wb_new("Leah Hansen", "EV planning reference sheet", dt.datetime(2024, 2, 7, 15, 41, 3),
                dt.datetime(2026, 9, 28, 11, 26, 44))
    ws = wb.active
    ws.title = "Models"
    ws.append(["Make and model", "Usable battery (kWh)", "Rated combined (kWh/100 km)", "Kerb mass (kg)", "DC connector"])
    allm = dict(W.FLEET)
    allm.update(W.SMALL_MODELS)
    for k, v in sorted(allm.items(), key=lambda kv: kv[1][0]):
        conn = "CHAdeMO" if k in ("LF4", "LFP", "LF3") else ("NACS" if k in ("MY", "M3L", "M3S") else "CCS1")
        ws.append([v[0], v[2], v[3], v[4], conn])
    for col, wdt in zip("ABCDE", [40, 20, 26, 15, 13]):
        ws.column_dimensions[col].width = wdt
    wb_save(wb, os.path.join(TARGET, F_REF), "2026-09-28T18:26:44Z", (2026, 9, 28, 11, 26, 45))


def projection_cells():
    """The contractor's 2027 projection: two-way trips by pair and month (integers) and the annual figure."""
    out = []
    for a, b, annual, prof in W.OD:
        months = [int(round(W.od_month_trips(a, b, annual, prof, m))) for m in W.MONTHS]
        out.append((a, b, months, annual))
    return out


def write_projection():
    from openpyxl.styles import Alignment, Font
    wb = wb_new("Jessica Williams", "SVRD long-distance travel projection 2027", dt.datetime(2026, 5, 19, 9, 3, 27),
                dt.datetime(2026, 6, 30, 16, 48, 55))
    ws = wb.active
    ws.title = "Table 3"
    ws.append(["Selkirk Valley Regional District: Long-Distance Travel Study 2026"])
    ws.append(["Table 3. Projected 2027 long-distance trips by battery-electric car between district communities, by month"])
    ws.append(["Origin-destination pair", None, "Trips (two-way)"] + [None] * 12)
    ws.append(["Community A", "Community B"] + [W.MONTH_NAMES[m - 1][:3] for m in W.MONTHS] + ["Year"])
    ws.merge_cells("A1:O1")
    ws.merge_cells("A2:O2")
    ws.merge_cells("A3:B3")
    ws.merge_cells("C3:O3")
    for c in ("A1", "A2"):
        ws[c].font = Font(bold=True)
    ws["C3"].alignment = Alignment(horizontal="center")
    for a, b, months, annual in projection_cells():
        ws.append([W.NODES[a][0], W.NODES[b][0]] + months + [annual])
    ws.append([])
    ws.append(["Trips are one-way journeys of 50 km or more between the two communities, both directions together; the "
               "2024 household and visitor surveys found no difference between the directions on any pair."])
    ws.append(["Year totals are the annual projection rounded to the nearest 10 trips and may differ from the sum of "
               "the months."])
    ws.append(["Source: Long-Distance Travel Study 2026, household survey (n = 2,184), visitor intercept survey "
               "(n = 1,377) and permanent count stations, projected to 2027 at the provincial ZEV share."])
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 18
    wb_save(wb, os.path.join(TARGET, F_PRJ), "2026-06-30T23:48:55Z", (2026, 6, 30, 16, 48, 56))


def write_weather():
    rows = []
    for node, (name, elev, off) in RC.STATIONS.items():
        sid = {"CAL": "1171393", "COR": "1172047", "TAM": "1178019", "MIR": "1175232"}[node]
        for d in RC.DAYS:
            t = RC.valley_temp(d, node)
            spread = 4.2 + 2.1 * (d.month in (5, 6, 7, 8, 9)) + float(PRNG.uniform(-1.2, 1.2))
            p = RC.WX[d]["precip"] * (1.25 if node == "COR" else 1.0)
            snow = p if t < 0.5 else 0.0
            rows.append([sid, name, d.isoformat(), "%.1f" % (t + spread), "%.1f" % (t - spread), "%.1f" % t,
                         "%.1f" % (p - snow), "%.1f" % snow])
    write_csv(F_WX, ["climate_id", "station_name", "date", "max_temp_c", "min_temp_c", "mean_temp_c", "total_rain_mm",
                     "total_snow_cm"], rows)


def write_maintenance():
    rows = []
    for i, (svrd, w0, w1, appr) in enumerate(RM.MAINT):
        s = RM.SITE[svrd]
        work = {"SV-RS-27": "Cable and holster replacement, both units", "SV-RS-21": "Cabinet filter and coolant service",
                "SV-RS-22": "Firmware update and RFID reader swap", "SV-RS-24": "Transformer inspection (utility)",
                "SV-RS-28": "Annual service and payment terminal upgrade"}[svrd]
        rows.append(["MW-%s-%03d" % (w0.year, 17 + i * 9), svrd, s["name"],
                     "Columbia Fast Charge Ltd." if s["op"] == "CFC" else "Northway EV Networks Inc.",
                     w0.strftime("%Y-%m-%d %H:%M"), w1.strftime("%Y-%m-%d %H:%M"), work, appr.isoformat(),
                     ["L. Hansen", "K. Mcdonald"][i % 2]])
    write_csv(F_MNT, ["Request No", "Site ID", "Site Name", "Operator", "Window Start (Pacific)", "Window End (Pacific)",
                      "Work", "Approved On", "Approved By"], rows)


def write_connection():
    wb = wb_new("Distribution Planning", "Service connection estimates", dt.datetime(2026, 8, 3, 8, 22, 9),
                dt.datetime(2026, 8, 12, 14, 51, 36))
    ws = wb.active
    ws.title = "Estimates"
    ws.append(["Selkirk Power & Light Co.: Class 4 service connection estimates, SVRD 2027 charging candidates"])
    ws.append(["Estimate No", "Location", "Requested Load (kVA)", "Existing Supply", "Works", "Estimate (CAD)",
               "Lead Time (weeks)", "Valid Until"])
    est = [("SPL-26-0418", "Kestrel Flats, Sorrel Valley Road", 500, "25 kV three-phase at road", "Pad transformer, 60 m lateral", 186400, 34),
           ("SPL-26-0419", "Halvorsen Bridge, Sorrel Valley Road", 500, "25 kV single-phase", "Three-phase extension 2.3 km, pad transformer", 612900, 52),
           ("SPL-26-0420", "Sable Summit, Sable Highway", 300, "Highways maintenance yard service", "Upgrade to 600 A, pad transformer", 241700, 41),
           ("SPL-26-0421", "Cedar Pass, Cedar Pass Highway", 300, "Ski area substation", "Feeder bay and 0.4 km lateral", 318200, 46)]
    for e in est:
        ws.append(list(e) + [dt.datetime(2027, 2, 12)])
    for c in ws["H"][2:]:
        c.number_format = "yyyy-mm-dd"
    for col, wdt in zip("ABCDEFGH", [13, 36, 20, 34, 44, 15, 18, 12]):
        ws.column_dimensions[col].width = wdt
    wb_save(wb, os.path.join(TARGET, F_CON), "2026-08-12T21:51:36Z", (2026, 8, 12, 14, 51, 37))


# ----------------------------------------------------------------------------------------------- metadata
def write_metadata():
    src = "constructed for this task (an invented regional district, its operators, utility and contractor)"
    files = {
        F_CFC: ("Columbia Fast Charge Ltd. session export for its sites in the district, monthly batches and re-sends", "2026-11-03"),
        F_NWE: ("Northway EV Networks Inc. transaction export, one JSON record per transaction", "2026-11-04"),
        F_CST: ("Columbia Fast Charge Ltd. charge point status notifications for the agreement's sites", "2026-11-03"),
        F_NST: ("Northway EV Networks Inc. status notifications for its stations in the export region", "2026-11-04"),
        F_REG: ("district fast charging site register, sites in service at 31 October 2026", "2026-11-02"),
        F_STR: ("district highway stretches between communities and candidate sites", "2025-04-22"),
        F_ZEV: ("zero-emission vehicle registrations in the district by make, model and model year", "2026-10-14"),
        F_REF: ("district EV planning reference sheet: usable battery and rated consumption by model", "2026-09-28"),
        F_PRJ: ("Long-Distance Travel Study 2026, Table 3, projected 2027 trips by pair and month", "2026-06-30"),
        F_WX: ("daily weather at four valley stations", "2026-11-02"),
        F_MNT: ("district log of maintenance windows requested by the operators and their approval dates", "2026-10-06"),
        F_CON: ("utility service connection estimates for the four candidate sites", "2026-08-12"),
        F_RUL: ("district 2027 Fast Charging Site Package scoring rules, as adopted", "2026-09-17"),
        F_AGR: ("Remote Community Fast Charging Operating Support Agreement (2024), with Schedules A to C", "2024-07-30"),
        F_COV: ("district Fast Charging Coverage Report 2026", "2026-03-24"),
    }
    meta = {
        "task": "task315",
        "decision": "which 2027 fast charging site package the regional district funds",
        "deliverables": ["site_package_2027_note.pdf", "site_package_2027.xlsx"],
        "distractor_files": ["target/" + F_WX, "target/" + F_CON, "target/" + F_COV],
        "wrong_basis_distractor": {
            "file": "target/" + F_COV,
            "basis": "the gaps between today's fast chargers ranked by length, which puts the Sorrel Valley gap first "
                     "and the Cedar Pass gap second; a gap's length is not the trips a site makes completable",
            "ruled_out_by": "scoring rules sections 2 and 4 (" + F_RUL + "): a package is scored on the 2027 trips in the "
                            "Long-Distance Travel Study projection that it makes completable and today's network does not",
        },
        "files": {("target/" + k): {"source": src, "covers": v[0], "date": v[1],
                                    "licence": "CC BY 4.0 (constructed for this task)"} for k, v in sorted(files.items())},
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    return sorted(files)


def cut_zip():
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=EXPORT_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, fn), "rb").read())
    os.utime(path, (EXPORT_TS, EXPORT_TS))


def generate():
    corridor, trips = RC.simulate_corridor()
    units, cfc_status, nwe_status = RM.build_all()
    return corridor, trips, units, cfc_status, nwe_status


def main():
    import docs as D
    import golden as G
    for folder in (TARGET, GOLDEN):
        if os.path.isdir(folder):
            shutil.rmtree(folder)
    os.makedirs(TARGET)
    os.makedirs(GOLDEN)
    corridor, trips, units, cfc_status, nwe_status = generate()
    n_cfc = write_cfc(cfc_records(corridor, units))
    n_nwe = write_northway(units)
    n_cs, n_ns = write_status(cfc_status, nwe_status)
    write_register()
    write_stretches()
    write_zev()
    write_reference()
    write_projection()
    write_weather()
    write_maintenance()
    write_connection()
    D.write_all(TARGET, F_RUL, F_AGR, F_COV)
    figs = G.figures(TARGET)
    figs["rows"] = {"cfc": n_cfc, "northway": n_nwe, "cfc_status": n_cs, "northway_status": n_ns}
    G.write_golden(GOLDEN, figs)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    names = write_metadata()
    for folder in (TARGET, GOLDEN):
        for fn in os.listdir(folder):
            os.utime(os.path.join(folder, fn), (EXPORT_TS, EXPORT_TS))
    assert sorted(os.listdir(TARGET)) == names, (sorted(os.listdir(TARGET)), names)
    cut_zip()
    print("built %d files, %d CFC rows, %d Northway rows; call %s" % (len(names), n_cfc, n_nwe, figs["call"]))


if __name__ == "__main__":
    main()
