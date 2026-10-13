"""Write the Brannoch pack's data files from a simulated world: the commission's laboratory results export, the gage
network's 15-minute and daily discharge (with the provisional pull the approved record replaced), the station
register (stations, streams, permitted facilities), the facilities' discharge monitoring reports, the practice
program's cover crop contracts and field mapping, and two distractors (precipitation, the lake's summer monitoring)."""
import csv
import datetime as dt

import numpy as np

import sim as S
import world as W

FILES = {
    "wq": "blc_water_quality_results_2027-01-08.csv",
    "uv": "merrifield_unit_values_wy2026_approved.csv",
    "dv": "merrifield_daily_values_wy2024-wy2025.csv",
    "prov": "merrifield_unit_values_2026-07_2026-09_provisional.csv",
    "register": "blc_station_register.xlsx",
    "agreement": "brannoch_lake_phosphorus_agreement.pdf",
    "program": "blc_tributary_monitoring_program_2024-2026.docx",
    "transmittal": "merrifield_data_transmittal_2026-12-14.txt",
    "dmr": "npdes_dmr_phosphorus_wy2026.csv",
    "contracts": "farm_practice_contracts_2024-2027.csv",
    "fields": "practice_field_watershed_acres.csv",
    "precip": "blc_weather_precipitation_wy2024-wy2026.csv",
    "lake": "lake_brannoch_summer_monitoring_2024-2026.xlsx",
}
DISTRACTORS = ("precip", "lake")


def _w(path, header, rows, comments=None):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        for c in comments or []:
            fh.write("# " + c + "\r\n")
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def sig3(x):
    """discharge as the hydrometric service publishes it: three significant figures"""
    if x <= 0:
        return "0"
    p = int(np.floor(np.log10(abs(x))))
    v = round(x, 2 - p)
    return ("%d" % v) if p >= 2 else ("%." + str(max(0, 2 - p)) + "f") % v


TRIB = {t[0]: t for t in W.TRIBS}


# ------------------------------------------------------------------------------------------ water quality
def wq_rows(world):
    out = []
    labname = {"BLC_old": W.LAB_OLD, "BLC_new": W.LAB_NEW, "ACWL": W.LAB}
    orgname = {"BLC": W.COMMISSION, "ACWL": W.LAB}
    for r in world["lab"]:
        new = r["org"] == "BLC" and r["date"] >= W.LAB_CHANGE
        lab = labname["BLC_new" if new else ("BLC_old" if r["org"] == "BLC" else "ACWL")]
        base = [r["org"], orgname[r["org"]], r["aid"], r["atype"], "Water", r["date"].isoformat(), r["time"], r["tz"],
                r["station"]]
        blank = r["atype"].endswith("Blank")

        def res(char, frac, val, unit, method, mdl=None, lab_=lab):
            if blank and char not in ("Temperature, water", "Specific conductance"):
                return base + [char, frac, "", unit, r["status"], "Not Detected", mdl if mdl else "", unit if mdl else "",
                               method, r["note"], lab_]
            return base + [char, frac, val, unit, r["status"], "", "", "", method, r["note"], lab_]
        if new:
            out.append(res("Total Phosphorus, mixed forms", "Total", "%d" % round(r["tp"] * 1000), "ug/L", "EPA 365.1", "5"))
            out.append(res("Orthophosphate", "Dissolved", "%d" % round(r["tdp"] * 1000 * 0.8), "ug/L", "EPA 365.1", "5"))
        else:
            out.append(res("Phosphorus", "Total", "%.3f" % r["tp"], "mg/L", "EPA 365.1" if r["org"] == "BLC" else "SM 4500-P E", "0.005"))
            out.append(res("Phosphorus", "Dissolved", "%.3f" % r["tdp"], "mg/L", "EPA 365.1" if r["org"] == "BLC" else "SM 4500-P E", "0.005"))
        out.append(res("Total suspended solids", "Non-filterable", "%.1f" % r["tss"], "mg/L", "SM 2540 D", "1.0"))
        out.append(res("Chloride", "Dissolved", "%.1f" % r["cl"], "mg/L", "EPA 300.0", "0.5"))
        out.append(res("Inorganic nitrogen (nitrate and nitrite)", "Dissolved", "%.3f" % r["no3"], "mg/L as N", "EPA 353.2", "0.02"))
        if not blank:
            out.append(res("Temperature, water", "", "%.1f" % r["temp"], "deg C", "Field meter", None, ""))
    return out


def write_wq(world, path):
    hdr = ["OrganizationIdentifier", "OrganizationFormalName", "ActivityIdentifier", "ActivityTypeCode", "ActivityMediaName",
           "ActivityStartDate", "ActivityStartTime/Time", "ActivityStartTime/TimeZoneCode", "MonitoringLocationIdentifier",
           "CharacteristicName", "ResultSampleFractionText", "ResultMeasureValue", "ResultMeasure/MeasureUnitCode",
           "ResultStatusIdentifier", "ResultDetectionConditionText", "DetectionQuantitationLimitMeasure/MeasureValue",
           "DetectionQuantitationLimitMeasure/MeasureUnitCode", "ResultAnalyticalMethod/MethodIdentifier",
           "ResultCommentText", "LaboratoryName"]
    rows = sorted(wq_rows(world), key=lambda r: (r[5], r[6], r[8], r[2], r[9], r[10]))
    return _w(path, hdr, rows)


# ------------------------------------------------------------------------------------------------ discharge
def write_uv(world, path):
    rows = []
    ice = world["ice"]
    for code in W.CODES:
        g = TRIB[code][4]
        a, b = ice.get(code, (None, None))
        for t, v in world["UV"][code]:
            loc = W.local_of(t)
            ql = "A:e" if (a and a <= loc.date() <= b) else "A"
            rows.append([g, t.strftime("%Y-%m-%d %H:%M"), sig3(v), ql])
    com = ["Merrifield Hydrometrics, approved unit values for water year 2026 (1 October 2025 to 30 September 2026),",
           "delivered to the Brannoch Lake Commission 14 December 2026. Discharge in cubic feet per second at 15-minute",
           "intervals; datetime_utc in Coordinated Universal Time. Qualifiers: A approved, e estimated (ice-affected).",
           "These values replace the provisional values delivered 6 October 2026."]
    return _w(path, ["gage_id", "datetime_utc", "discharge_cfs", "qualifiers"], rows, com)


def write_prov(world, path):
    """the provisional pull of 6 October 2026 for July to September: before the autumn field measurements shifted two
    gages' ratings"""
    rng = np.random.default_rng(W.SEED + 7)
    rows = []
    shift = {"KES": 1.06, "AMB": 0.95}
    for code in W.CODES:
        g = TRIB[code][4]
        f = shift.get(code, 1.0)
        for t, v in world["UV"][code]:
            loc = W.local_of(t)
            if loc.date() >= W.D(2026, 7, 1):
                ff = f if loc.date() >= W.D(2026, 8, 1) else 1.0
                rows.append([g, t.strftime("%Y-%m-%d %H:%M"), sig3(v * ff * float(np.exp(rng.normal(0, 0.003)))), "P"])
    com = ["Merrifield Hydrometrics, provisional unit values, 1 July to 30 September 2026, pulled 6 October 2026.",
           "Provisional data are subject to revision. Discharge in cubic feet per second; datetime_utc in UTC."]
    return _w(path, ["gage_id", "datetime_utc", "discharge_cfs", "qualifiers"], rows, com)


def write_dv(world, path):
    rows = []
    for code in W.CODES:
        g = TRIB[code][4]
        for i, d in enumerate(S.DAYS):
            if S.WYR[i] < 2026:
                ql = "A:e" if (d.month in (1, 2) and code in ("KES", "TAM", "COR", "HES") and 8 <= d.day <= 24) else "A"
                rows.append([g, d.isoformat(), sig3(world["Q"][code][i]), ql])
    com = ["Merrifield Hydrometrics, approved daily mean discharge, water years 2024 and 2025 (1 October 2023 to",
           "30 September 2025). Daily means are for local calendar days. Qualifiers: A approved, e estimated (ice-affected)."]
    return _w(path, ["gage_id", "date", "discharge_cfs", "qualifiers"], rows, com)


# ------------------------------------------------------------------------------------------ station register
def write_register(world, path):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stations"
    ws["A1"] = "Brannoch Lake Commission: tributary monitoring stations"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Compliance stations under the phosphorus agreement, with the stations each organisation reports them under and the serving gage."
    hdr = ["Tributary", "Commission station", "College station", "Gage", "Station drainage area (km2)",
           "Gage drainage area (km2)", "Station river km above lake", "Latitude", "Longitude", "Notes"]
    for j, h in enumerate(hdr, 1):
        ws.cell(row=4, column=j, value=h).font = Font(bold=True)
    rng = np.random.default_rng(W.SEED + 13)
    for i, t in enumerate(W.TRIBS, 5):
        code, name, st, lab, gage, da_s, da_g = t[:7]
        note = None
        if da_s != da_g:
            note = "Sampling station 4.2 km downstream of gage %s." % gage
        vals = [name, st, lab, gage, da_s, da_g, W.STATION_RKM[code], round(44.62 + rng.uniform(-0.25, 0.25), 4),
                round(-72.41 + rng.uniform(-0.3, 0.3), 4), note]
        for j, v in enumerate(vals, 1):
            ws.cell(row=i, column=j, value=v)
    for col, w in zip("ABCDEFGHIJ", [20, 17, 15, 10, 14, 14, 14, 10, 11, 44]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "B5"
    s2 = wb.create_sheet("Streams")
    s2["A1"] = "Streams joining the monitored tributaries"
    s2["A1"].font = Font(bold=True, size=12)
    s2["A2"] = "River km are measured upstream from a stream's mouth; a tributary's mouth is the lake."
    for j, h in enumerate(["Stream", "Flows into", "Joins at river km"], 1):
        s2.cell(row=3, column=j, value=h).font = Font(bold=True)
    for i, (s, into, rkm) in enumerate(W.SUBSTREAMS, 4):
        for j, v in enumerate((s, into, rkm), 1):
            s2.cell(row=i, column=j, value=v)
    for col, w in zip("ABC", [30, 20, 16]):
        s2.column_dimensions[col].width = w
    s3 = wb.create_sheet("Facilities")
    s3["A1"] = "Permitted discharges in the basin"
    s3["A1"].font = Font(bold=True, size=12)
    s3["A2"] = "Outfall river km is on the receiving water, measured upstream from its mouth."
    for j, h in enumerate(["Permit", "Facility", "Outfall", "Receiving water", "Outfall river km", "In service from",
                           "In service to"], 1):
        s3.cell(row=3, column=j, value=h).font = Font(bold=True)
    r = 4
    for pid, fname, rw, rkm, mgd, tp, mode, resub, reloc in W.FACILITIES:
        if reloc:
            k, rkm2 = reloc
            sw = W.D(2026, 4, 1)
            rows = [(pid, fname, "001", rw, rkm, "1998-06-01", (sw - dt.timedelta(days=1)).isoformat()),
                    (pid, fname, "002", rw, rkm2, sw.isoformat(), None)]
        else:
            rows = [(pid, fname, "001", rw, rkm, "%d-%02d-01" % (1972 + (int(pid[-3:]) % 40), 1 + int(pid[-2:]) % 12), None)]
        for row in rows:
            for j, v in enumerate(row, 1):
                s3.cell(row=r, column=j, value=v)
            r += 1
    for col, w in zip("ABCDEFG", [12, 44, 8, 28, 15, 14, 14]):
        s3.column_dimensions[col].width = w
    wb.save(path)
    return len(W.TRIBS)


# -------------------------------------------------------------------------------------------------- reports
def write_dmr(world, path):
    rows = []
    for r in world["dmr"]:
        pid, fname, outfall, start, end, par, stat, val, unit, recv, sub = r
        rows.append([pid, fname, outfall, start.isoformat(), end.isoformat(), par, stat, val, unit, recv.isoformat(), sub])
    # the relocated facility reports its new outfall from April 2026
    reloc = {f[0] for f in W.FACILITIES if f[8]}
    for row in rows:
        if row[0] in reloc and row[3] >= "2026-04-01":
            row[2] = "002"
    rows.sort(key=lambda r: (r[0], r[4], r[9], r[5], r[6]))
    hdr = ["PERMIT_ID", "FACILITY_NAME", "OUTFALL", "MONITORING_PERIOD_START_DATE", "MONITORING_PERIOD_END_DATE",
           "PARAMETER_DESC", "STATISTICAL_BASE", "DMR_VALUE", "DMR_UNIT", "RECEIVED_DATE", "SUBMISSION_TYPE"]
    return _w(path, hdr, rows)


def write_contracts(world, path):
    contracts, fields = world["practices"]
    rows = []
    for c in contracts:
        for k, fl in enumerate(c["versions"]):
            acres = sum(fields[f]["acres"] for f in fl)
            num = int(c["cid"][3:])
            on = "" if k == 0 else "%d-%02d-%02d" % (c["start"], 2 + (num * 7 + k) % 10, 1 + (num * 11 + 5 * k) % 27)
            for f in fl:
                rows.append([c["cid"], c["farm"], f, W.PRACTICE_CODE, "Cover Crop", "%.1f" % acres, c["start"], c["end"],
                             W.NAME[fields[f]["code"]], k, on])
    hdr = ["contract_id", "farm_id", "field_id", "practice_code", "practice", "contracted_acres", "first_crop_year",
           "last_crop_year", "watershed", "amendment_no", "amended_on"]
    com = ["%s: cover crop contracts (practice 340), crop years 2024 to 2027. Exported 8 January 2027." % W.PROGRAM,
           "Contracts enrol whole fields. Amendment 0 is the contract as signed; an amendment restates the contract, "
           "and the latest amendment is the contract in force for every crop year it covers."]
    return _w(path, hdr, rows, com)


def write_fields(world, path):
    contracts, fields = world["practices"]
    rows = []
    for f in sorted(fields):
        for code, share in fields[f]["split"]:
            rows.append([f, "%.1f" % fields[f]["acres"], W.NAME[code], "%.2f" % share])
    return _w(path, ["field_id", "field_acres", "watershed", "share_of_field"], rows)


def write_precip(world, path):
    rows = [[sid, d.isoformat(), "%.1f" % v] for sid, d, v in world["precip"]]
    return _w(path, ["station_id", "date", "precipitation_mm"], rows)


def write_lake(world, path):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summer monitoring"
    ws["A1"] = "Lake Brannoch: open-water monitoring, May to October"
    ws["A1"].font = Font(bold=True, size=12)
    hdr = ["Station", "Basin", "Date", "Total phosphorus (ug/L)", "Chlorophyll a (ug/L)", "Secchi depth (m)"]
    for j, h in enumerate(hdr, 1):
        ws.cell(row=3, column=j, value=h).font = Font(bold=True)
    for i, r in enumerate(world["lake"], 4):
        for j, v in enumerate(r, 1):
            c = ws.cell(row=i, column=j, value=v)
            if j == 3:
                c.number_format = "mm/dd/yyyy"
    for col, w in zip("ABCDEF", [9, 14, 12, 22, 20, 16]):
        ws.column_dimensions[col].width = w
    wb.save(path)
    return len(world["lake"])
