"""Writes the data files of task134's pack (the documents are in docs.py)."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

import params as P
from io_util import save_xlsx, write_csv
from world import licence_year, month_iter, uk_offset_hours

SURV_A = "holmwood_channel_surveys_2016-2023.csv"
SURV_B = "seaward_channel_surveys_2023-2026.csv"
CERTS = "maintenance_dredging_certificates_2016-2026.xlsx"
LOADS = "dunmarsh_load_log_2023-2026.csv"
REVISION = "FE_dry_solids_revision_20260330.csv"
SAMPLING = "sediment_sampling_2025-2026.xlsx"
LAB = "aldern_results_FEN26.csv"
TIDE = "fendmouth_pier_tide_gauge_2016-2026.csv"
FLOW = "river_fend_haddon_weir_flows_2016-2026.csv"
CALLS = "vessel_arrivals_2024-2026.csv"

NAMES = {"OC": "Outer Channel", "FR": "Fend Roads", "MR": "Middle Reach", "IR": "Inner Reach", "TB": "Turning Basin",
         "NQ1": "North Quay Berth 1", "NQ2": "North Quay Berth 2", "NQ3": "North Quay Berth 3",
         "CT5": "Container Terminal Berth 5"}
AREAS = ["OC", "FR", "MR", "IR", "TB", "NQ1", "NQ2", "NQ3", "CT5"]


def write_surveys(W, out):
    rows_a, rows_b = [], []
    for sv in W.surveys:
        d = sv["date"]
        order = np.lexsort((sv["E"], -sv["N"]))
        if sv["contractor"] == "A":
            ref = "HH-FEN-%s" % d.strftime("%y%m")
            for i in order:
                z = sv["depth"][i]
                val = "-99.99" if np.isnan(z) else "%.2f" % z
                rows_a.append([ref, d.strftime("%d/%m/%Y"), "%.0f" % sv["E"][i], "%.0f" % sv["N"][i], val])
        else:
            ref = "SGD-%s-FEN" % d.strftime("%y%m")
            for i in order:
                z = sv["depth"][i]
                if np.isnan(z):
                    continue
                rows_b.append([ref, d.isoformat(), "%.1f" % sv["E"][i], "%.1f" % sv["N"][i], "%.2f" % (-(z + P.CD_BELOW_ODN))])
    write_csv(os.path.join(out, SURV_A), ["SURVEY_REF", "SURVEY_DATE", "EASTING", "NORTHING", "DEPTH_M_BCD"], rows_a)
    write_csv(os.path.join(out, SURV_B), ["survey_id", "survey_date", "x_osgb36", "y_osgb36", "z_m_odn"], rows_b)
    return len(rows_a), len(rows_b)


def certificate_rows(W):
    """Monthly certificate rows April 2016 to September 2026: (date, area, loads, dry solids, in-situ m3, certificate)."""
    rng = np.random.default_rng(P.SEED + 7)
    load_count, load_tds = {}, {}
    for r in W.loads:
        k = (r["area"], r["t_load"].year, r["t_load"].month)
        load_count[k] = load_count.get(k, 0) + 1
        tds = r["tds_logged"] if r["tds_logged"] is not None else r["tds_true"]
        load_tds[k] = load_tds.get(k, 0.0) + tds
    rows = []
    for y, m in month_iter(2016, 4, 2026, 9):
        for a in AREAS:
            key = (a, y, m)
            if key not in W.monthly:
                continue
            v = W.monthly[key]
            if (y, m) >= (2023, 10):
                n = load_count.get(key, 0)
                tds = load_tds.get(key, 0.0)
            else:
                tds = v * W.dry_density[a] * (1.0 + 0.012 * rng.standard_normal())
                n = max(1, int(round(tds / P.LOAD_TDS)))
            new = (y, m) >= (2021, 4)
            code = P.CODES_2021[a] if new else a
            cert = "DDL/%02d%02d/%s" % (y % 100, m, code)
            rows.append(dict(date=dt.date(y, m, 1), area=a, code=code, loads=n, tds=round(tds), vol=round(v), cert=cert))
    # the October 2024 Middle Reach certificate was re-issued with a corrected survey volume
    for r in rows:
        if r["date"] == dt.date(2024, 10, 1) and r["area"] == "MR":
            orig = dict(r)
            orig["vol"] = round(r["vol"] / 1.041)
            r["cert"] = r["cert"] + "/R1"
            rows.insert(rows.index(r), orig)
            break
    return rows


def write_certificates(W, out):
    rows = certificate_rows(W)
    wb = Workbook()
    wb.remove(wb.active)
    bold = Font(bold=True)
    fys = sorted({r["date"].year if r["date"].month >= 4 else r["date"].year - 1 for r in rows})
    for fy in fys:
        ws = wb.create_sheet("%d-%02d" % (fy, (fy + 1) % 100))
        ws["A1"] = "%s: monthly maintenance dredging certificates, %s, financial year %d-%02d" % (P.CONTRACTOR, P.PORT, fy, (fy + 1) % 100)
        ws["A1"].font = bold
        ws["A2"] = "In situ volume by pre- and post-dredge survey; dry solids by loading monitor"
        hdr = ["Month", "Area", "Loads", "Dry solids (t)", "In situ volume (m3)", "Certificate"]
        ws.append([])
        ws.append(hdr)
        for c in range(1, len(hdr) + 1):
            ws.cell(row=4, column=c).font = bold
        for r in rows:
            f = r["date"].year if r["date"].month >= 4 else r["date"].year - 1
            if f != fy:
                continue
            area = NAMES[r["area"]] if r["code"] == r["area"] else r["code"]
            ws.append([r["date"], area, r["loads"], r["tds"], r["vol"], r["cert"]])
            ws.cell(row=ws.max_row, column=1).number_format = "mmm-yy"
        for i, wdt in enumerate([10, 26, 8, 15, 19, 20], start=1):
            ws.column_dimensions[get_column_letter(i)].width = wdt
    ws = wb.create_sheet("Area codes")
    ws.append(["Code from April 2021", "Area"])
    for a in AREAS:
        ws.append([P.CODES_2021[a], NAMES[a]])
    save_xlsx(wb, os.path.join(out, CERTS), "Maintenance dredging certificates", P.PEOPLE["contractor_pm"],
              "2016-05-06T09:15:00Z", company=P.CONTRACTOR, modified="2026-10-14T10:05:00Z")
    return rows


def write_loads(W, out):
    rows, rev = [], []
    for r in W.loads:
        tl = r["t_load"].strftime("%Y-%m-%dT%H:%M:00Z")
        td = r["t_dump"].strftime("%Y-%m-%dT%H:%M:00Z")
        rho = "" if r["rho_m"] is None else "%.3f" % r["rho_m"]
        tds = "" if r["tds_logged"] is None else "%.0f" % r["tds_logged"]
        rows.append([r["load_ref"], r["vessel"], tl, P.CODES_2021[r["area"]], "%.0f" % r["hopper_m3"], rho, tds,
                     P.SITES[r["route"]][0], td, "%.5f" % r["lat"], "%.5f" % r["lon"]])
        if r.get("fault"):
            rev.append([r["trip_ref"], "%.0f" % r["tds_true"]])
    write_csv(os.path.join(out, LOADS), ["load_ref", "vessel", "loading_start_utc", "area", "hopper_m3",
                                          "mixture_density_t_m3", "dry_solids_t", "planned_site", "dump_start_utc",
                                          "dump_lat", "dump_lon"], rows)
    write_csv(os.path.join(out, REVISION), ["trip_ref", "dry_solids_t_revised"], rev)
    return len(rows), len(rev)


def write_sampling(W, out):
    wb = Workbook()
    wb.remove(wb.active)
    bold = Font(bold=True)
    ws = wb.create_sheet("Station plan")
    ws.append(["Station", "Area", "Easting", "Northing"])
    for st in W.stations:
        ws.append([st["station"], NAMES[st["part"]], st["E"], st["N"]])
    ws = wb.create_sheet("Field log 2026")
    ws.append(["Sample ref", "Station", "Date", "Time", "Easting", "Northing", "Water depth (m)", "Sampler"])
    for x in sorted(W.samples, key=lambda x: x["t"]):
        wd = 12.3 if x["part"] in ("OC", "FR", "MR", "IR", "TB") else (14.3 if x["part"] == "CT5" else 12.8)
        ws.append([x["ref"], x["station"], x["t"].date(), x["t"].strftime("%H:%M"), x["E"], x["N"],
                   round(wd + 2.4 + 0.3 * np.sin(x["E"]), 1), "Day grab 0.1 m2"])
        ws.cell(row=ws.max_row, column=3).number_format = "dd/mm/yyyy"
    ws = wb.create_sheet("Area summary")
    ws.append(["Campaign", "Completed", "Results reported", "Area", "Dry solids fraction (by mass)"])
    for yr in (2025, 2026):
        c0, c1, rep = P.SAMPLING[yr]
        for a in ["OC", "FR", "MR", "IR", "TB", "NQ1", "NQ3", "CT5"]:
            ws.append([yr, dt.date(*c1), dt.date(*rep), NAMES[a], W.ds_summary[(yr, a)]])
            ws.cell(row=ws.max_row, column=2).number_format = "dd/mm/yyyy"
            ws.cell(row=ws.max_row, column=3).number_format = "dd/mm/yyyy"
    for sh in wb.worksheets:
        for c in range(1, 9):
            sh.cell(row=1, column=c).font = bold
            sh.column_dimensions[get_column_letter(c)].width = 16
    save_xlsx(wb, os.path.join(out, SAMPLING), "Sediment sampling 2025-2026", P.PEOPLE["manager"], "2025-03-18T09:10:00Z",
              modified="2026-04-06T15:30:00Z")


def write_lab(W, out):
    rows = []
    batch1 = {"OC", "FR", "MR"}
    lab_no = 26031100
    gaps = np.random.default_rng(P.SEED + 3000).integers(1, 9, size=len(W.samples))   # other clients' samples between ours
    for i, x in enumerate(sorted(W.samples, key=lambda x: x["ref"])):
        lab_no += int(gaps[i])
        b2 = (x["part"] not in batch1) if not x["qa"] else (x["primary"].split("-")[1] not in batch1)
        received = "19/03/2026" if b2 else "16/03/2026"
        for det, unit in (("Dry solids", "%"), ("Cadmium", "mg/kg"), ("Mercury", "mg/kg"), ("Lead", "mg/kg"),
                          ("Copper", "mg/kg"), ("Zinc", "mg/kg"), ("Arsenic", "mg/kg"), ("Chromium", "mg/kg"),
                          ("Nickel", "mg/kg")):
            key = {"Dry solids": "DS", "Cadmium": "Cd", "Mercury": "Hg", "Lead": "Pb", "Copper": "Cu", "Zinc": "Zn",
                   "Arsenic": "As", "Chromium": "Cr", "Nickel": "Ni"}[det]
            v = x["rep"][key]
            if det == "Dry solids":
                txt = "%.1f" % v
            elif det in ("Cadmium", "Mercury"):
                if det == "Mercury" and b2:
                    txt, unit = "%.0f" % round(v * 1000.0), "ug/kg"
                else:
                    txt = "%.3f" % v
            else:
                txt = "%.2f" % v
            rows.append([str(lab_no), x["ref"], received, det, txt, unit, "dry weight" if det != "Dry solids" else "as received"])
    write_csv(os.path.join(out, LAB), ["lab_no", "client_ref", "received", "determinand", "result", "units", "basis"], rows)
    return len(rows)


def write_distractors(W, out):
    t0, lev = W.tide
    rows = [[(t0 + dt.timedelta(hours=i)).strftime("%Y-%m-%d %H:%M"), "%.2f" % lev[i]] for i in range(len(lev))]
    write_csv(os.path.join(out, TIDE), ["datetime_gmt", "level_m_above_cd"], rows)
    d0, q = W.flow
    rows = [[(d0 + dt.timedelta(days=i)).isoformat(), "%.2f" % q[i]] for i in range(len(q))]
    write_csv(os.path.join(out, FLOW), ["date", "mean_flow_m3s"], rows)
    rows = [[d.strftime("%d/%m/%Y %H:%M"), nm, kind, "%.1f" % loa, "%.1f" % dr, berth] for d, nm, kind, loa, dr, berth in W.calls]
    write_csv(os.path.join(out, CALLS), ["arrival_local", "vessel", "type", "loa_m", "arrival_draught_m", "berth"], rows)
