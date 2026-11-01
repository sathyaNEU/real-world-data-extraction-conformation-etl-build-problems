"""Writes the evidence pack (target/) from the world's clean truth, each file in its source system's own form."""
import os

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font

import docs as D
import io_util as IO
import params as PR
import world as W

SITES = {
    "ASH": ("05431500", "TAMSEN RIVER NEAR ASHBY", "Ostrand", 3880),
    "COY": ("05432100", "TAMSEN RIVER AT COYLE BRIDGE", "Pell", 4930),
    "GALE": ("05432400", "GALE CREEK NEAR PELHAM", "Pell", 412),
    "HAL": ("05433000", "TAMSEN RIVER AT ORRINSFORD", "Marrow", 6480),
    "FEN": ("05433500", "TAMSEN RIVER AT FENWICK", "Marrow", 7050),
}
NICE = {"ASH": "Tamsen River near Ashby", "COY": "Tamsen River at Coyle Bridge", "GALE": "Gale Creek near Pelham",
        "HAL": "Tamsen River at Orrinsford", "FEN": "Tamsen River at Fenwick"}
RIVER_MILE = {"ASH": 63.2, "COY": 41.0, "GALE": None, "HAL": 12.6, "FEN": 3.4}

FILES = {
    "peaks": "SWS_annual_peaks_Tamsen_basin_2026-10-28.csv",
    "standard": "OLDD_LS-02_levee_standard_rev3.pdf",
    "skew": "SWS_SW-16-03_regional_skew_update.pdf",
    "table4": "HWE-1907_hydraulic_update_2019_Table4.pdf",
    "inventory": "DNR_levee_inventory_Tamsen_2025.xlsx",
    "crown24": "OLDD_crown_certification_survey_2024.csv",
    "crown16": "OLDD_crown_survey_2016.csv",
    "bench": "OLDD_benchmark_list.csv",
    "coyle": "SWS_05432100_hourly_WY2017-2026.csv",
    "halbrook": "ORF2_logger_export_20261005.csv",
    "procedure": "OLDD_OP-04_flood_warning_closure.pdf",
    "precip": "coop_daily_precip_Orrinsford_Coyle.csv",
    "inspection": "OLDD_2025_annual_inspection_summary.pdf",
}


def _peak_rows(pk, og):
    rows = []

    def add(key, wy, ts, q, est=False):
        site, name, _, _ = SITES[key]
        ts = pd.Timestamp(ts)
        tm = "" if (wy < 1971 and key in ("ASH", "FEN", "GALE")) else ts.strftime("%H:%M")
        code = "2" if est else ""
        appr = "P" if wy == PR.LAST_WY else "A"
        rows.append((key, ts, ["SWS", site, name, ts.strftime("%Y-%m-%d"), tm, W.sig3(q), code, appr]))
    for _, r in pk.iterrows():
        wy = int(r["wy"])
        add("COY", wy, r["coy_time"], r["coy_q"])
        add("HAL", wy, r["hal_time"], r["hal_q"])
    for _, r in og.iterrows():
        est = (r["gauge"] == "GALE" and int(r["wy"]) in (1974, 1975)) or (r["gauge"] == "ASH" and int(r["wy"]) in
                                                                           (1962, 1963, 1966)) or \
            (r["gauge"] == "FEN" and int(r["wy"]) in (1962, 1980))
        add(r["gauge"], int(r["wy"]), r["time"], r["q"], est=est)
    order = {"ASH": 0, "COY": 1, "GALE": 2, "HAL": 3, "FEN": 4}
    rows.sort(key=lambda x: (order[x[0]], x[1]))
    return [r[2] for r in rows]


def write_peaks(path, pk, og):
    pre = ["# State Water Survey, Surface Water Section: annual peak streamflow",
           "# Retrieved 2026-10-28 for the Orrinsford Levee and Drainage District",
           "# Sites in this file:",
           ]
    for k in ("ASH", "COY", "GALE", "HAL", "FEN"):
        site, name, county, da = SITES[k]
        pre.append("#   %s  %s  (%s County, drainage area %s sq mi)" % (site, NICE[k], county, "{:,}".format(da)))
    pre += ["# peak_dt   -- Date of peak streamflow (YYYY-MM-DD)",
            "# peak_tm   -- Time of peak streamflow (24 hour, local standard time)",
            "# peak_va   -- Annual peak streamflow value in cfs",
            "# peak_cd   -- Peak discharge qualification codes: 2 -- Discharge is an estimate",
            "# approval  -- A -- Approved, P -- Provisional, subject to revision"]
    hdr = ["agency_cd", "site_no", "station_nm", "peak_dt", "peak_tm", "peak_va", "peak_cd", "approval"]
    return IO.write_csv(path, hdr, _peak_rows(pk, og), preamble=pre)


def write_inventory(path, c24):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Segments"
    hdr = ["Segment ID", "Sponsor", "Bank", "From RM", "To RM", "Year built", "Crown raised", "Level of protection",
           "Protected area (acres)", "Last inspection"]
    ws.append(hdr)
    raised_txt = {1996: "1996", 1998: "Oct 1998", 2001: "2001", 2003: "2003-11", 2005: "Sept 2005", 2008: "Oct 2008",
                  2002: "2002"}
    insp = ["Jun 2024", "Jul 2024", "May 2024", "Aug 2024", "Jun 2023", "Jul 2024", "Sep 2024", "Jun 2024",
            "Oct 2024", "Aug 2023"]
    allseg = PR.OTHER_LEVEES[:2] + PR.DISTRICTS + PR.OTHER_LEVEES[2:]
    for i, (sid, sp, bank, a, b, built, raised, acres) in enumerate(allseg):
        lop = "1% + 2 ft" if raised else "about 10-yr"
        ws.append([sid, sp, bank, a, b, built, raised_txt.get(raised, "") if raised else "", lop, acres, insp[i]])
    ws.append(["TR-L-10", "Orrinsford Levee and Drainage District", "Left", 14.0, 10.6, 1964, "1993",
               "1% + 3 ft (LS-02)", 2140, "Aug 2024"])
    for c, w in zip("ABCDEFGHIJ", (11, 44, 7, 9, 9, 11, 13, 19, 21, 15)):
        ws.column_dimensions[c].width = w
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"

    wc = wb.create_sheet("Orrinsford crown")
    wc.append(["Station", "Cross-section", "Crown elevation (ft NAVD 88)", "Source"])
    lab = {6240: "Main Street closure", 11870: "P&W Railroad closure"}
    z = c24.set_index(["sta", "code"])["elev"]
    for s in PR.TABLE4_STATIONS:
        if s == 6240:
            e = z.loc[(s, "MAIN ST CLOSURE")]
        elif s == 11870:
            e = z.loc[(s, "P&W RR CLOSURE")]
        else:
            e = z.loc[(s, "CL")]
        wc.append([D.sta_str(s), lab.get(s, "Levee"), float(e), "2024 certification survey"])
    for c, w in zip("ABCD", (10, 22, 26, 26)):
        wc.column_dimensions[c].width = w
    for cell in wc[1]:
        cell.font = Font(bold=True)

    wg = wb.create_sheet("Gauges")
    wg.append(["Site", "Name", "River mile", "Drainage area (sq mi)", "Peak record"])
    recs = {"ASH": "1962-", "COY": "1962-", "GALE": "1974-1996", "HAL": "1962-", "FEN": "1962- (1977-79 missing)"}
    for k in ("ASH", "COY", "GALE", "HAL", "FEN"):
        site, name, _, da = SITES[k]
        rm = RIVER_MILE[k] if RIVER_MILE[k] is not None else "trib. at RM 30.8"
        wg.append([site, NICE[k], rm, da, recs[k]])
    for c, w in zip("ABCDE", (11, 32, 16, 20, 24)):
        wg.column_dimensions[c].width = w
    for cell in wg[1]:
        cell.font = Font(bold=True)

    wsx = wb.create_sheet("Structures")
    wsx.append(["Segment ID", "Station", "Structure", "Type"])
    for row in (["TR-L-10", "18+30", "Pump Station 1", "Pump station with gravity outlet"],
                ["TR-L-10", "62+40", "Main Street bridge and closure", "Stoplog closure"],
                ["TR-L-10", "118+70", "Prairie and Western Railroad bridge and closure", "Swing gate closure"],
                ["TR-L-10", "161+20", "Pump Station 2", "Pump station with gravity outlet"]):
        wsx.append(row)
    for c, w in zip("ABCD", (11, 10, 44, 30)):
        wsx.column_dimensions[c].width = w
    for cell in wsx[1]:
        cell.font = Font(bold=True)

    wb.save(path)
    IO.repack_ooxml(path, "DNR Levee Safety", "DNR Levee Safety", "2025-03-14T15:20:00Z", "2025-03-14T16:02:00Z",
                    "Tamsen River levee inventory", "State Department of Natural Resources")


def write_crown24(path, c24):
    pre = ["# Orrinsford levee crown certification survey, May 2024",
           "# Orrinsford Levee and Drainage District; survey by Lucas Land Surveying, Kristin Lucas PLS",
           "# Stations: 2019 as-built levee stationing; elevations: ft NAVD 88"]
    rows = [[D.sta_str(int(r.sta)), "%.2f" % r.elev, r.code, r.reach] for r in c24.itertuples()]
    return IO.write_csv(path, ["station", "elev_ft", "code", "reach"], rows, preamble=pre)


def write_crown16(path, c16):
    pre = ["# ORRINSFORD LEVEE - CROWN PROFILE SURVEY",
           "# Field dates 10/11/2016 - 10/14/2016   Lucas Land Surveying for Orrinsford L&DD",
           "# Levee stationing from north tie-in; vertical datum NGVD 29 (ft)"]
    rows = [[D.sta_str(int(r.old_sta)), "%.2f" % r.elev, r.code] for r in c16.itertuples()]
    return IO.write_csv(path, ["STA", "ELEV", "DESC"], rows, preamble=pre)


def write_bench(path, bm):
    rows = [[r.id, r.desc, "%.2f" % r.ngvd, "%.2f" % r.navd, r.set] for r in bm.itertuples()]
    return IO.write_csv(path, ["benchmark", "description", "elev_ngvd29_ft", "elev_navd88_ft", "year_set"], rows,
                        preamble=["# Orrinsford Levee and Drainage District vertical control, as re-leveled 2019"])


def write_coyle(path, tel):
    idx = pd.DatetimeIndex(tel["utc"])
    keep = np.ones(len(tel), bool)
    for a, b in (("2018-08-14 06:00", "2018-08-14 13:00"), ("2023-09-02 17:00", "2023-09-02 21:00")):
        keep &= ~((idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b)))
    appr = np.where(idx >= pd.Timestamp("2025-10-01"), "P", "A")
    qv = [W.sig3(q) for q in tel["qc"]]
    rows = [[idx[i].strftime("%Y-%m-%d %H:%M"), "%.2f" % tel["stage_c"].iat[i], qv[i], appr[i]]
            for i in np.nonzero(keep)[0]]
    pre = ["# State Water Survey 05432100 Tamsen River at Coyle Bridge",
           "# Hourly values, water years 2017-2026. Times UTC.",
           "# Gauge datum 638.00 ft above NGVD 29",
           "# Data-value qualification codes included in this output: A approved for publication, P provisional "
           "data subject to revision"]
    return IO.write_csv(path, ["datetime_utc", "stage_ft", "discharge_cfs", "approval"], rows, preamble=pre)


def write_halbrook(path, tel):
    idx = pd.DatetimeIndex(tel["utc"])
    up = pd.Timestamp(PR.HAL_LOGGER_UPGRADE_UTC)
    swap = (idx >= up - pd.Timedelta(hours=7)) & (idx < up)
    stamp = idx.where(idx >= up, idx - pd.Timedelta(hours=6))
    rows = [[stamp[i].strftime("%m/%d/%Y %H:%M"), "%.2f" % tel["stage_h"].iat[i]] for i in np.nonzero(~swap)[0]]
    pre = ["Site: ORF2 Tamsen R at Orrinsford (SWS 05433000), Main St bridge",
           "Export: 2026-10-05 08:12, all records",
           "Gauge datum: %.2f ft NGVD 29" % (PR.HAL_GAUGE_DATUM - PR.NGVD_TO_NAVD),
           "Time zone: UTC"]
    return IO.write_csv(path, ["Timestamp (UTC)", "Stage (ft)"], rows, preamble=pre)


def write_precip(path):
    rng = np.random.default_rng(PR.OTHER_SEED + 7)
    days = pd.date_range("2016-10-01", "2026-09-30", freq="D")
    rows = []
    for sid, name, scale in (("ORFD2NE", "ORRINSFORD 2 NE", 1.0), ("COYLE1W", "COYLE 1 W", 0.94)):
        for d in days:
            wet = rng.random() < (0.27 + 0.08 * np.cos(2 * np.pi * (d.dayofyear - 150) / 365.25))
            v = rng.gamma(0.75, 0.42) * scale if wet else 0.0
            if rng.random() < 0.004:
                s = "M"
            elif 0 < v < 0.005:
                s = "T"
            else:
                s = "%.2f" % v
            rows.append([sid, name, d.strftime("%Y-%m-%d"), s])
    return IO.write_csv(path, ["station", "name", "date", "prcp_in"], rows,
                        preamble=["# Cooperative observer network, daily precipitation (in.), 7 a.m. observation",
                                  "# T = trace, M = missing"])


def write_pack(S, out):
    os.makedirs(out, exist_ok=True)
    f = {k: os.path.join(out, v) for k, v in FILES.items()}
    n = {}
    n["peaks"] = write_peaks(f["peaks"], S["pk"], S["og"])
    D.standard(f["standard"])
    D.skew_study(f["skew"])
    D.table4(f["table4"], S["t4"], S["pk"])
    write_inventory(f["inventory"], S["c24"])
    n["crown24"] = write_crown24(f["crown24"], S["c24"])
    n["crown16"] = write_crown16(f["crown16"], S["c16"])
    n["bench"] = write_bench(f["bench"], S["bm"])
    n["coyle"] = write_coyle(f["coyle"], S["tel"])
    n["halbrook"] = write_halbrook(f["halbrook"], S["tel"])
    D.procedure(f["procedure"])
    n["precip"] = write_precip(f["precip"])
    D.inspection(f["inspection"])
    return n
