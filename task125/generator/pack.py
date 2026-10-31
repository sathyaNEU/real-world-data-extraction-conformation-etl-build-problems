"""The pack's files, each in the layout of the system that produced it."""
import csv
import datetime as dt
import io
import math
import os
import re
import zipfile

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import world as W

FILES = {
    "lab": "umzimela_wq_lab_results_2025_26.csv",
    "runs": "umzimela_routine_run_log_2025_26.csv",
    "ec": "umzimela_ec_loggers_hourly_2025_26.csv",
    "service": "ec_logger_service_visits_2025_26.csv",
    "memory": "ec_logger_memory_downloads_2025_26.csv",
    "gauges": "umzimela_gauges_daily_2025_26.csv",
    "register": "umzimela_monitoring_network_register.xlsx",
    "schedule": "umzimela_sulfate_load_allocation_schedule_2025.pdf",
    "returns": "wul_discharge_returns_2025_26.csv",
    "wul": "wul_register_mine_discharges.xlsx",
    "inspections": "cma_compliance_inspections_2025_26.csv",
    "rain": "umzimela_raingauges_daily_2025_26.csv",
    "wtw": "nyathi_wtw_raw_water_log_2025_26.xlsx",
}
DISTRACTORS = ["rain", "wtw"]
EXPORT = dt.datetime(2026, 10, 9, 8, 40)          # the agency's extract for the 2025/26 assessment

SITES = []   # (site code, name, river, RU, weir, lat, lon, purpose)
WEIRS = []   # (weir code, station number, name, river, established)
_LAT0, _LON0 = -27.92, 30.48


def _site_tables():
    if SITES:
        return
    r = W.rng("sites")
    for n, (code, river, name, inflows, weir, alloc) in enumerate(W.RU):
        stn = "W%dH%03d" % (2 if code.startswith("MZ") or code in ("KH1", "SW1", "GB1") else 3, 18 + 7 * n)
        WEIRS.append((weir, stn, "%s at %s weir" % (river, name.split(" at ")[-1] if " at " in name else name),
                      river, "%d" % int(1968 + r.integers(0, 40))))
        lat = _LAT0 - 0.035 * n + float(r.normal(0, 0.01))
        lon = _LON0 + 0.04 * n + float(r.normal(0, 0.01))
        SITES.append(("UM%02d" % (n + 1), "%s at %s" % (river, stn), river, code, weir, round(lat, 5), round(lon, 5),
                      "boundary monitor, resource unit %s" % code))
    extra = [("UM15", "Khambule Stream at Ngcebo footbridge", "Khambule Stream", "KH1", "", "upstream trend"),
             ("UM16", "Ntsheketshe Stream at the R33 culvert", "Ntsheketshe Stream", "NT1", "", "upstream trend"),
             ("UM17", "Nyathi River at Mabhokweni WTW intake", "Nyathi River", "NY2", "", "abstraction point"),
             ("UM18", "Mzimela River at Ezinyosini Dam outlet", "Mzimela River", "MZ1", "", "reservoir release"),
             ("UM19", "Gubhu River at Esiqhingini", "Gubhu River", "GB1", "", "reference site"),
             ("UM20", "Mpafa Stream at the Mpafa siding", "Mpafa Stream", "MP1", "", "upstream trend")]
    # each extra site sits up its own river from that unit's boundary monitor (the abstraction point just above the
    # weir), surveyed to the same five decimals
    up = {"UM15": (0.047, -0.061), "UM16": (0.039, -0.052), "UM17": (0.006, -0.009), "UM18": (0.083, -0.117),
          "UM19": (0.064, -0.088), "UM20": (0.031, -0.044)}
    rx = W.rng("sites-extra")
    for c, nm, river, ru, weir, purpose in extra:
        b = [s for s in SITES if s[3] == ru][0]
        dlat, dlon = up[c]
        lat = b[5] + dlat * (1 + float(rx.normal(0, 0.15)))
        lon = b[6] + dlon * (1 + float(rx.normal(0, 0.15)))
        SITES.append((c, nm, river, ru, weir, round(lat, 5), round(lon, 5), purpose))


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def _xlsx(path, sheets, creator, created, modified):
    wb = Workbook()
    wb.remove(wb.active)
    for title, rows, widths in sheets:
        ws = wb.create_sheet(title)
        for row in rows:
            ws.append(list(row))
        for c in ws[1]:
            c.font = Font(bold=True)
        for i, wdt in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = wdt
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified
    wb.properties.title = None
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                        b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                        b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity>'
                        b'<ScaleCrop>false</ScaleCrop><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


# ------------------------------------------------------------------ the routine monitoring record
ANALYTES = [("pH", "pH units", 0.1), ("EC", "mS/m", 0.5), ("SO4", "mg/L", 5.0), ("Cl", "mg/L", 2.0),
            ("Ca", "mg/L", 1.0), ("Mg", "mg/L", 1.0), ("Na", "mg/L", 1.0), ("Fe", "mg/L", 0.05),
            ("Mn", "mg/L", 0.02), ("Al", "mg/L", 0.05), ("Alk", "mg/L CaCO3", 5.0)]


def site_sulfate(S, code, i, rr):
    """the sulfate (mg/L) the site's sample carries on day index i"""
    ru = [s for s in SITES if s[0] == code][0]
    if code in [s[0] for s in SITES[:14]] and ru[3] in W.MIXING:
        return W.point_concentration(ru[3], i, S["Q"], S["C"], rr)
    base = S["C"][ru[3]][i]
    if code == "UM15":
        base = S["C"]["KH1"][i] * 1.08
    elif code == "UM16":
        base = S["C"]["NT1"][i] * 1.05
    elif code == "UM17":
        base = W.point_concentration("NY2", i, S["Q"], S["C"], rr) * 0.98
    elif code == "UM18":
        base = S["C"]["MZ1"][i] * 0.97
    elif code == "UM20":
        base = S["C"]["MP1"][i] * 1.06
    return base * (1.0 + rr.normal(0, 0.006))


def lab_and_runs(S, folder):
    """the laboratory's results (one row per analyte) and the field teams' run log, with what each run sampled"""
    _site_tables()
    r = W.rng("lab")
    rr = W.rng("bank")
    idx = {d: i for i, d in enumerate(W.DAYS)}
    lab, log, sampled = [], [], {}
    seq = 25001
    for rn, d in enumerate(W.runs(), start=1):
        i = idx[d]
        for k, site in enumerate(SITES):
            code = site[0]
            team = "A" if (site[2].startswith("Mzimela") or site[2] in ("Khambule Stream", "Silwane Stream",
                                                                       "Gubhu River")) else "B"
            t = dt.datetime.combine(d, dt.time(7, 40)) + dt.timedelta(minutes=int(26 * (k % 10) + r.integers(0, 15)))
            so4 = site_sulfate(S, code, i, rr)
            sampled[(code, d)] = so4
            ec_us = 115.0 + 1.31 * so4 + float(r.normal(0, 6.0))
            ph = 7.6 - 2.1 * min(1.0, so4 / 3000.0) + float(r.normal(0, 0.08))
            sid = "UMZ%06d" % seq
            seq += 1
            log.append([rn, d.strftime("%d/%m/%Y"), team, code, t.strftime("%H:%M"), "%.0f" % (ec_us * (1 + r.normal(0, 0.02))),
                        "%.1f" % ph, "%.1f" % (12.0 + 8.0 * math.cos((d.timetuple().tm_yday - 15) / 58.1) + r.normal(0, 0.6)),
                        ["low", "normal", "high"][0 if d.month in (6, 7, 8, 9) else (2 if S["rain"][i] > 15 else 1)],
                        ["S. Sikobi", "S. Mnyamande", "K. Msane", "T. Bele"][(rn + (team == "B")) % 4], ""])
            vals = {"pH": ph, "EC": ec_us / 10.0, "SO4": so4, "Cl": 9 + 0.012 * so4 + r.normal(0, 1.5),
                    "Ca": 18 + 0.21 * so4 + r.normal(0, 3), "Mg": 6 + 0.09 * so4 + r.normal(0, 1.5),
                    "Na": 11 + 0.02 * so4 + r.normal(0, 1.5), "Fe": max(0.0, 0.08 + 0.0009 * so4 + r.normal(0, 0.05)),
                    "Mn": max(0.0, 0.02 + 0.0011 * so4 + r.normal(0, 0.03)),
                    "Al": max(0.0, 0.03 + 0.0004 * so4 + r.normal(0, 0.03)), "Alk": max(5.0, 140 - 0.04 * so4 + r.normal(0, 8))}
            an_date = d + dt.timedelta(days=int(3 + r.integers(0, 6)))
            for a, unit, dl in ANALYTES:
                v = vals[a]
                if v < dl:
                    res, q = "<%s" % (("%g" % dl)), "<"
                else:
                    res = ("%.1f" % v) if a in ("pH", "EC", "Cl", "Ca", "Mg", "Na") else (
                        "%.0f" % v if a in ("SO4", "Alk") else "%.2f" % v)
                    q = ""
                lab.append([sid, code, d.strftime("%Y-%m-%d"), t.strftime("%H:%M"), a, res, unit, q,
                            an_date.strftime("%Y-%m-%d"), "B%04d" % (rn * 2 + (team == "B"))])
            # the laboratory re-runs about one sulfate result in twenty; the re-run is the reported value
            if r.random() < 0.05:
                rerun = so4 * (1 + r.normal(0, 0.012))
                orig = rerun * (1 + r.choice([-1, 1]) * r.uniform(0.04, 0.09))
                for row in lab[::-1]:
                    if row[0] == sid and row[4] == "SO4":
                        row[5] = "%.0f" % orig
                        break
                lab.append([sid + "-R", code, d.strftime("%Y-%m-%d"), t.strftime("%H:%M"), "SO4", "%.0f" % rerun,
                            "mg/L", "", (an_date + dt.timedelta(days=4)).strftime("%Y-%m-%d"), "B%04d" % (rn * 2 + 1)])
                sampled[(code, d)] = rerun
    _csv(os.path.join(folder, FILES["lab"]),
         ["lab_sample_id", "site_code", "sample_date", "sample_time", "analyte", "result", "unit", "qualifier",
          "analysed_date", "batch"], lab)
    _csv(os.path.join(folder, FILES["runs"]),
         ["run_no", "run_date", "team", "site_code", "time_on_site", "field_ec_uS_cm", "field_ph", "water_temperature_degC",
          "flow_condition", "sampled_by", "remarks"], log)
    return sampled


# ------------------------------------------------------------------ continuous EC loggers and their service visits
TRIGGERS = {"ECL-03": 270, "ECL-06": 240, "ECL-08": 230, "ECL-10": 1400, "ECL-11": 310, "ECL-14": 410}
LOGGERS = [("ECL-03", "UM03"), ("ECL-06", "UM06"), ("ECL-08", "UM08"), ("ECL-10", "UM10"), ("ECL-11", "UM11"),
           ("ECL-14", "UM14")]


def ec_loggers(S, folder):
    """hourly EC (uS/cm) at six boundary monitors: the water's EC plus a fouling drift that grows between service
    visits and is cleaned off at each; timestamps in UTC as the telemetry server stores them"""
    _site_tables()
    rows, visits, truth, memory = [], [], {}, []
    site_ru = {s[0]: s[3] for s in SITES}
    for lid, site in LOGGERS:
        r = W.rng("logger-" + lid)
        rr = W.rng("logger-bank-" + lid)
        # service visits every five to seven weeks; the drift rate differs visit to visit
        vdays = []
        d = W.YEAR0 + dt.timedelta(days=int(r.integers(8, 20)))
        while d <= W.YEAR1:
            vdays.append(d)
            d += dt.timedelta(days=int(r.integers(35, 50)))
        vtimes = [dt.datetime.combine(v, dt.time(10, 0)) + dt.timedelta(minutes=int(r.integers(0, 300))) for v in vdays]
        if site in [s_[0] for s_ in SITES[:14]] and site_ru[site] in W.MIXING:
            med = float(np.median([W.point_concentration(site_ru[site], i, S["Q"], S["C"], W.rng("med-" + lid))
                                   for i in range(0, len(W.DAYS), 7)]))
        else:
            med = float(np.median(S["C"][site_ru[site]]))
        scale = 115.0 + 1.31 * med
        rates = [float(r.uniform(0.06, 0.15)) * scale / 42.0 for _ in range(len(vtimes) + 1)]     # uS/cm a day
        t = dt.datetime(2025, 9, 30, 22, 0)          # 00:00 SAST on 1 October in UTC
        end = dt.datetime(2026, 9, 30, 22, 0)
        prev = dt.datetime(2025, 9, 20, 9, 0)
        vi = 0
        # telemetry outages in the wet season: the hours stay in the logger's memory and come down at the next visit
        gaps = []
        for g in range(2):
            g0 = dt.datetime(2025, 11, 10) + dt.timedelta(days=int(r.integers(0, 150)), hours=int(r.integers(0, 24)))
            gaps.append((g0, g0 + dt.timedelta(hours=int(r.integers(70, 220)))))
        while t < end:
            local = t + dt.timedelta(hours=2)
            i = (local.date() - W.YEAR0).days
            if site in [s[0] for s in SITES[:14]] and site_ru[site] in W.MIXING:
                so4 = W.point_concentration(site_ru[site], i, S["Q"], S["C"], rr)
            else:
                so4 = S["C"][site_ru[site]][i]
            hour = local.hour
            ec_true = (115.0 + 1.31 * so4) * (1.0 + 0.012 * math.sin((hour - 4) / 24 * 2 * math.pi)) + r.normal(0, 4.0)
            while vi < len(vtimes) and local >= vtimes[vi]:
                prev = vtimes[vi]
                vi += 1
            drift = rates[vi] * (local - prev).total_seconds() / 86400.0
            truth[(lid, local)] = ec_true
            gap = [g for g in gaps if g[0] <= local < g[1]]
            if gap:
                nxt_visit = [v for v in vtimes if v > gap[0][1]]
                memory.append([lid, (nxt_visit[0] if nxt_visit else gap[0][1]).strftime("%Y-%m-%d %H:%M"),
                               local.strftime("%Y-%m-%d %H:%M"), "%.0f" % (ec_true + drift)])
                t += dt.timedelta(hours=1)
                continue
            rows.append([lid, site, t.strftime("%Y-%m-%dT%H:%M:%SZ"), "%.0f" % (ec_true + drift),
                         "%.1f" % (14 + 7 * math.cos((local.timetuple().tm_yday - 20) / 58.1) +
                                   2.2 * math.sin((hour - 9) / 24 * 2 * math.pi)), "%.2f" % (12.9 - 0.0004 * len(rows) % 0.6)])
            t += dt.timedelta(hours=1)
        visits.append([lid, site, "2025-09-20 09:00", "", "", "1413", "%.0f" % (1413 + r.normal(0, 6)), "N. Mahaye",
                       "probe replaced with a calibrated spare; logger restarted"])
        for k, vt in enumerate(vtimes):
            p0 = vtimes[k - 1] if k else dt.datetime(2025, 9, 20, 9, 0)
            acc = rates[k] * (vt - p0).total_seconds() / 86400.0
            i = min((vt.date() - W.YEAR0).days, len(W.DAYS) - 1)
            so4 = (W.point_concentration(site_ru[site], i, S["Q"], S["C"], W.rng("svc-" + lid + str(k)))
                   if site_ru[site] in W.MIXING else S["C"][site_ru[site]][i])
            base = 115.0 + 1.31 * so4
            visits.append([lid, site, vt.strftime("%Y-%m-%d %H:%M"), "%.0f" % (base + acc), "%.0f" % base,
                           "1413", "%.0f" % (1413 + r.normal(0, 6)), ["N. Mahaye", "Z. Dludla"][k % 2],
                           "wiped and rinsed; probe returned to stilling tube"])
    _csv(os.path.join(folder, FILES["ec"]), ["logger_id", "site_code", "timestamp", "ec_uS_cm", "temperature_degC",
                                             "battery_v"], rows)
    _csv(os.path.join(folder, FILES["memory"]), ["logger_id", "downloaded_local", "reading_local", "ec_uS_cm"], memory)
    _csv(os.path.join(folder, FILES["service"]),
         ["logger_id", "site_code", "visit_local", "reading_before_clean_uS_cm", "reading_after_clean_uS_cm",
          "check_standard_uS_cm", "check_reading_uS_cm", "technician", "notes"], visits)
    return truth


# ------------------------------------------------------------------ gauges
def gauges(S, folder):
    _site_tables()
    rows = []
    for (weir, stn, nm, river, est), (code, *_r) in zip(WEIRS, W.RU):
        r = W.rng("stage-" + weir)
        a, b, h0 = float(r.uniform(4.0, 9.0)), float(r.uniform(1.45, 1.75)), float(r.uniform(0.05, 0.22))
        for i, d in enumerate(W.DAYS):
            q = S["Q"][code][i] * S["gauge_noise"][code][i]
            h = h0 + (q / a) ** (1.0 / b)
            rows.append([stn, d.strftime("%Y-%m-%d"), "%.3f" % h, "%.3f" % q, "A"])
    _csv(os.path.join(folder, FILES["gauges"]), ["station", "date", "mean_stage_m", "mean_flow_m3s", "quality"], rows)


def register(folder):
    _site_tables()
    sites = [("site_code", "site_name", "river", "resource_unit", "weir", "latitude", "longitude", "purpose",
              "ec_logger", "ec_trigger_uS_cm")]
    logger_at = {site: lid for lid, site in LOGGERS}
    for s in SITES:
        lid = logger_at.get(s[0], "")
        sites.append(tuple(s) + (lid, TRIGGERS.get(lid, "")))
    weirs = [("weir", "station", "name", "river", "in_service_since")] + [w for w in WEIRS]
    units = [("resource_unit", "river", "name", "lower_boundary_weir", "length_km", "upstream_units")]
    lengths = {"MZ1": 21.4, "KH1": 9.8, "MZ2": 2.6, "MZ3": 17.9, "SW1": 7.2, "MZ4": 3.1, "GB1": 26.5, "MZ5": 22.8,
               "NY1": 31.2, "NT1": 11.6, "NY2": 2.2, "MP1": 6.4, "NY3": 1.8, "NY4": 19.5}
    for code, river, name, inflows, weir, alloc in W.RU:
        units.append((code, river, name, weir, lengths[code], ", ".join(inflows)))
    _xlsx(os.path.join(folder, FILES["register"]),
          [("Sites", sites, [10, 44, 20, 14, 8, 11, 11, 34, 10, 16]), ("Weirs", weirs, [8, 10, 44, 20, 16]),
           ("Resource units", units, [14, 20, 30, 18, 10, 18])],
          "Umzimela CMA Water Quality", dt.datetime(2023, 3, 2, 9, 12), dt.datetime(2026, 7, 21, 14, 3))


# ------------------------------------------------------------------ mines: licences, returns, inspections
def mines(S, folder):
    """monthly discharge returns per licensed point: the flow totaliser reading at month end and the month's
    composite sulfate, as each mine's laboratory reports it"""
    r = W.rng("mines")
    rows, insp, truth = [], [], {}
    months = [(2025, m) for m in (9, 10, 11, 12)] + [(2026, m) for m in range(1, 10)]
    quarters = {"Q1": [(2025, 10), (2025, 11), (2025, 12)], "Q2": [(2026, 1), (2026, 2), (2026, 3)],
                "Q3": [(2026, 4), (2026, 5), (2026, 6)], "Q4": [(2026, 7), (2026, 8), (2026, 9)]}
    for mine, short, points in W.MINES:
        for pt, unit, qbase in points:
            reading0 = float(r.integers(800_000, 4_000_000))
            base = []
            for (y, m) in months:
                d0 = dt.date(y, m, 1)
                d1 = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1))
                i0, i1 = max(0, (d0 - W.YEAR0).days), max(0, (d1 - W.YEAR0).days)
                q = float(np.mean(S["Q"][unit][i0:i1 + 1]))
                ndays = (d1 - d0).days + 1
                vol = qbase * (q / W.SOURCES[unit][0]) ** 0.35 * 86400 * ndays * (1 + r.normal(0, 0.03))
                conc = float(np.mean(S["C"][unit][i0:i1 + 1])) * float(r.uniform(1.04, 1.16))
                if pt == "NCH-DP2" and (y, m) == (2026, 3):
                    conc *= 1.11          # the corrected composite the resubmission carries
                as_s = short in W.LAB_AS_S_MINES and d0 >= W.LAB_AS_S_FROM
                rep = round(conc / W.S_TO_SO4) if as_s else round(conc)
                base.append((y, m, d0, d1, ndays, vol, conc, rep, as_s))

            def tonnes(fac):
                out = {}
                for qn, ms in quarters.items():
                    t = 0.0
                    for (y, m, d0, d1, nd, vol, conc, rep, as_s) in base:
                        if (y, m) in ms:
                            t += vol * fac * (rep * W.S_TO_SO4 if as_s else rep) / 1e6
                    out[qn] = t
                return out
            # the point's discharge scale is set so no quarter sits within 2 t of a ten-tonne rounding edge
            fac = 1.0
            for k in range(400):
                cand = 0.97 + 0.00015 * k
                if all(abs((v % 10) - 5) >= 2.0 for v in tonnes(cand).values()):
                    fac = cand
                    break
            reading, meter_new = reading0, None
            for (y, m, d0, d1, ndays, vol, conc, rep, as_s) in base:
                vol *= fac
                truth[(pt, y, m)] = (vol, conc)
                if pt == W.METER_SWAP[0] and (y, m) == (2026, 2):
                    sw = W.METER_SWAP[1]
                    part = vol * (sw.day - 0.5) / ndays
                    old_final = reading + part
                    insp.append([sw.strftime("%Y-%m-%d"), mine, pt, "S. Sikhunyana",
                                 "Totaliser failed its accuracy check and was replaced during the visit. Old meter "
                                 "serial EM-77302 final reading %.0f m3; new meter serial EM-90418 installed reading "
                                 "0 m3." % old_final])
                    meter_new = vol - part
                    reading_out = meter_new
                elif meter_new is not None:
                    meter_new += vol
                    reading_out = meter_new
                else:
                    reading += vol
                    reading_out = reading
                ec = (115.0 + 1.31 * conc) / 10.0 * (1 + r.normal(0, 0.015))
                sub = min(d1 + dt.timedelta(days=int(r.integers(9, 26))), dt.date(2026, 10, 8))
                shown = rep
                if pt == "NCH-DP2" and (y, m) == (2026, 3):
                    shown = round(conc / 1.11 / W.S_TO_SO4)   # the first return carried the uncorrected composite
                rows.append(["%s/%04d%02d" % (pt, y, m), mine, "WUL-%s-%s" % (short, "2019" if short != "SAM" else "2021"),
                             pt, "%04d-%02d" % (y, m), "%.0f" % reading_out, "%d" % shown, "%.1f" % ec,
                             "%.1f" % (6.9 - 2.0 * min(1, conc / 3000) + r.normal(0, 0.1)), sub.strftime("%Y-%m-%d")])
    # one resubmission: the mine corrected a month's composite sulfate after its laboratory re-ran the sample
    fix = [x for x in rows if x[3] == "NCH-DP2" and x[4] == "2026-03"][0]
    corr = list(fix)
    corr[6] = "%d" % round(truth[("NCH-DP2", 2026, 3)][1] / W.S_TO_SO4)
    corr[0] = fix[0] + "-C1"
    corr[9] = (dt.date.fromisoformat(fix[9]) + dt.timedelta(days=17)).strftime("%Y-%m-%d")
    rows.append(corr)
    rows.sort(key=lambda x: (x[9], x[0]))
    other = [[d, mine, pt, insp_by, note] for (d, mine, pt, insp_by, note) in ([
        ("2025-10-22", "Khambule Colliery (Pty) Ltd", "KHC-DP1", "M. Nzimande", "Discharge clear; sampling tap and V-notch in order."),
        ("2025-11-19", "Ntsheketshe Coal Holdings", "NCH-DP1", "S. Sikhunyana", "Seepage below the pollution control dam wall noted; mine to report."),
        ("2026-01-28", "Mpafa Mining Company", "MMC-DP1", "M. Nzimande", "Totaliser reading confirmed against the mine's return."),
        ("2026-03-11", "Khambule Colliery (Pty) Ltd", "KHC-DP2", "S. Sikhunyana", "Second discharge running; pump schedule on file."),
        ("2026-05-20", "Ntsheketshe Coal Holdings", "NCH-DP2", "M. Nzimande", "No observations."),
        ("2026-08-05", "Silwane Anthracite Mine", "SAM-DP1", "S. Sikhunyana", "New totaliser sealed; seal number recorded."),
    ])]
    _csv(os.path.join(folder, FILES["returns"]),
         ["return_id", "holder", "licence_no", "discharge_point", "month", "totaliser_m3", "sulphate_mg_l",
          "ec_ms_m", "ph", "submitted_on"], rows)
    # the agency numbers its inspections across every catchment in the order they are made, so this extract's
    # numbers run in date order with the other catchments' inspections between them
    ri = W.rng("inspection-ids")
    nxt, visits = 2001, []
    for v in sorted(other + insp, key=lambda x: x[0]):
        visits.append(["INS-%04d" % nxt] + v)
        nxt += int(ri.integers(3, 11))
    _csv(os.path.join(folder, FILES["inspections"]),
         ["inspection_id", "date", "holder", "discharge_point", "inspector", "findings"], visits)
    lic = [("licence_no", "holder", "discharge_point", "receiving_watercourse", "resource_unit",
            "max_volume_m3_per_month", "max_sulphate_mg_l", "issued")]
    for mine, short, points in W.MINES:
        for pt, unit, qbase in points:
            lic.append(("WUL-%s-%s" % (short, "2019" if short != "SAM" else "2021"), mine, pt,
                        W.RU_BY[unit][1], unit, int(round(qbase * 86400 * 31 * 1.6, -3)), 3000 if unit != "SW1" else 2000,
                        "2019-06-14" if short != "SAM" else "2021-02-03"))
    notes = [("Licence conditions common to the mine discharges",),
             ("Each holder submits a return for every month by the 25th of the following month.",),
             ("A return gives the discharge's flow totaliser reading at the end of the month and the sulfate of the "
              "month's flow-proportional composite sample; the sulfate a discharge sent out in a month is the month's "
              "metered volume at that composite.",),
             ("A holder may correct a return by submitting it again; the later submission replaces the earlier.",)]
    _xlsx(os.path.join(folder, FILES["wul"]), [("Discharges", lic, [16, 30, 12, 22, 14, 22, 18, 12]),
                                              ("Conditions", notes, [120])],
          "Umzimela CMA Water Use", dt.datetime(2021, 2, 4, 11, 30), dt.datetime(2025, 11, 3, 9, 48))
    return truth


# ------------------------------------------------------------------ distractors
def distractors(S, folder):
    r = W.rng("raingauges")
    rows = []
    for g, f in (("RG-Ngcebo", 1.0), ("RG-Esikhotheni", 0.92), ("RG-Mabhokweni", 1.08)):
        for i, d in enumerate(W.DAYS):
            v = S["rain"][i] * f * (0.7 + 0.6 * r.random()) if S["rain"][i] > 0 else (
                round(float(r.uniform(0.2, 1.4)), 1) if r.random() < 0.03 else 0.0)
            rows.append([g, d.strftime("%d/%m/%Y"), "%.1f" % v])
    _csv(os.path.join(folder, FILES["rain"]), ["gauge", "date", "rain_mm"], rows)
    wtw = [("date", "raw_turbidity_NTU", "raw_ec_mS_m", "raw_ph", "abstracted_Ml", "operator")]
    for i, d in enumerate(W.DAYS):
        so4 = W.point_concentration("NY2", i, S["Q"], S["C"], r) * 0.98
        wtw.append((d.strftime("%Y-%m-%d"), round(float(4 + 40 * min(1, S["rain"][i] / 30) + r.normal(0, 1.5)), 1),
                    round((115 + 1.31 * so4) / 10 * (1 + float(r.normal(0, 0.03))), 1),
                    round(float(7.3 - 0.4 * min(1, so4 / 1500) + r.normal(0, 0.1)), 1),
                    round(float(6.2 + r.normal(0, 0.4)), 2), ["S. Mabhodla", "S. Gcugcwa", "D. Nzama"][i % 3]))
    _xlsx(os.path.join(folder, FILES["wtw"]), [("Daily log", wtw, [12, 18, 14, 10, 14, 12])],
          "Mabhokweni WTW", dt.datetime(2025, 10, 1, 7, 2), dt.datetime(2026, 10, 2, 16, 25))
