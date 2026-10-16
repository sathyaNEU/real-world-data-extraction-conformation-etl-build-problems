"""The operating records the main call runs on, written as each system exports them: the legacy incident database and
the EHS platform's case exports, the workforce-management hours, the WMS weekly throughput, the industrial engineering
team's engineered labour standards, the FY2027 operating plan, the site register and the ITA Form 300A submissions."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os
import zoneinfo

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import common as K
import world as WD
import xlsx_util as XU

F_LEGACY = "ehs_legacy_case_export_fy21_2024-06-30.csv"
F_PLATFORM = "ehs_platform_cases_2024-07-01_2026-11-02.json"
F_WFM = "wfm_hours_by_dept_week_fy21_fy26.csv"
F_WMS = "wms_cases_shipped_by_category_week.parquet"
F_STD = "ie_engineered_labor_standards.xlsx"
F_PLAN = "fy2027_operating_plan_v3.xlsx"
F_REG = "site_register_2026-11-02.csv"
F_ITA = "ita_form300a_submissions_cy2021_cy2025.csv"

ZONES = {"OH": "America/New_York", "IN": "America/Indiana/Indianapolis", "MI": "America/Detroit",
         "PA": "America/New_York", "KY": "America/New_York", "GA": "America/New_York", "NC": "America/New_York",
         "IL": "America/Chicago", "TN": "America/Chicago", "TX": "America/Chicago", "WI": "America/Chicago"}
OSHA_TYPE_LEGACY = {"DAFW": "DAYS AWAY", "DJTR": "RESTRICTED-TRANSFER", "OTHER": "OTHER RECORDABLE"}
OSHA_TYPE_PLAT = {"DAFW": "Days away from work", "DJTR": "Job transfer or restriction", "OTHER": "Other recordable case"}


def dc_info(W):
    return W.dcs.set_index("dc_no")


def dc_no_at(dn, fy, wk):
    """The labour system's DC number in a given week (Rockford re-numbered from fiscal 2025 week 14)."""
    if dn == WD.RECODE_DC and (fy, wk) >= WD.RECODE_WEEK:
        return WD.RECODE_NEW_NO
    return dn


def loc_at(dn, code, fy, wk):
    if dn == WD.RECODE_DC and (fy, wk) >= WD.RECODE_WEEK:
        return WD.RECODE_NEW_CODE
    return code


def cat_code(cat, fy, wk):
    return K.OLD_CATS[cat] if (fy, wk) < K.CAT_RECODE else cat


# ---------------------------------------------------------------------------------------------------- case numbering
def case_frame(W):
    """Every reported case with the identifiers, local and UTC times, entry dates and statuses the two EHS systems
    give it; the migrated cases (open at the 1 July 2024 go-live) flagged."""
    import asks_world as AW
    C = W.cases.copy()
    info = dc_info(W)
    r = K.rng("case_ids")
    C["local_dt"] = [dt.datetime.combine(d, dt.time(h_, m_)) for d, h_, m_ in zip(C.date, C.hour, C.minute)]
    # the event's local time on the night shift may fall after midnight: the date is the shift's calendar date
    zones = {dn: zoneinfo.ZoneInfo(ZONES[info.state[dn]]) for dn in info.index}
    C["utc_dt"] = [ld.replace(tzinfo=zones[dn]).astimezone(dt.timezone.utc) for ld, dn in zip(C.local_dt, C.dc_no)]
    lag = r.integers(0, 5, len(C))
    C["entered"] = [d + dt.timedelta(days=int(l_)) for d, l_ in zip(C.date, lag)]
    total_days = C.away_true.fillna(0) + C.restr_true.fillna(0)
    C["end_date"] = [d + dt.timedelta(days=int(n)) for d, n in zip(C.date, total_days)]
    C["legacy"] = C.date < K.MIGRATION
    C["migrated"] = C.legacy & (C.kind == "REC") & ((C.end_date >= K.MIGRATION) | (C.entered >= K.MIGRATION - dt.timedelta(days=6)))
    # legacy case numbers: location code, two-digit year, sequence per site and year in entry order
    C = C.sort_values(["entered", "date", "dc_no", "hour", "minute", "employee_id"]).reset_index(drop=True)
    seq = {}
    leg = []
    for row in C.itertuples():
        if not row.legacy:
            leg.append("")
            continue
        code = info.wms_code[row.dc_no]
        k = (code, row.date.year)
        seq[k] = seq.get(k, 0) + 1
        leg.append("%s-%02d-%04d" % (code, row.date.year % 100, seq[k]))
    C["legacy_no"] = leg
    # platform case ids: one network sequence by entry date; migrated cases took the first numbers at go-live
    plat = C[(~C.legacy) | C.migrated].copy()
    mig = plat[plat.migrated].sort_values(["date", "legacy_no"])
    rest = plat[~plat.migrated].sort_values(["entered", "utc_dt", "dc_no", "employee_id"])
    counters = {2024: 0, 2025: 0, 2026: 0}
    plat_id = {}
    for ix in list(mig.index) + list(rest.index):
        yr = 2024 if ix in mig.index else C.loc[ix, "entered"].year
        counters[yr] = counters[yr] + int(r.integers(1, 4))
        plat_id[ix] = "EHS-%d-%06d" % (yr, counters[yr])
    C["platform_id"] = [plat_id.get(ix, "") for ix in C.index]
    return C


# ---------------------------------------------------------------------------------------------------- legacy export
def write_legacy(W, C, out):
    info = dc_info(W)
    cols = ["CASE_NO", "ESTABLISHMENT", "INCIDENT_DATE", "INCIDENT_TIME", "EMPLOYEE_NO", "EMPLOYER", "JOB_TITLE", "DEPT",
            "CLASSIFICATION", "OSHA_CASE_TYPE", "INJURY_ILLNESS", "EVENT_CODE", "EVENT", "NATURE", "BODY_PART",
            "DAYS_AWAY", "DAYS_RESTRICTED", "CASE_STATUS", "PRIVACY_CASE", "DATE_ENTERED"]
    L = C[C.legacy].sort_values(["date", "dc_no", "hour", "minute", "legacy_no"])
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(cols)
    cut = K.MIGRATION - dt.timedelta(days=1)
    for c in L.itertuples():
        if c.kind == "FA":
            cls, typ, ii, da, dr, st = "FIRST AID", "", "", "", "", "CLOSED"
        else:
            cls = "RECORDABLE"
            typ = OSHA_TYPE_LEGACY[c.case_type]
            ii = "INJURY" if not c.illness else c.illness.upper()
            a, b = int(c.away_true or 0), int(c.restr_true or 0)
            # days as the legacy database held them at its last day
            span = (cut - c.date).days
            a2 = min(a, max(span, 0))
            b2 = min(b, max(span - a, 0))
            if a2 + b2 > 180:
                a2, b2 = (180, 0) if a2 >= 180 else (a2, 180 - a2)
            da, dr = str(a2), str(b2)
            st = "NOT WORK RELATED" if c.kind == "REMOVED" else ("OPEN" if c.migrated else "CLOSED")
        if c.kind == "REMOVED":
            typ = OSHA_TYPE_LEGACY["OTHER"]
            da, dr = "0", "0"
        w.writerow([c.legacy_no, info.ehs_site[c.dc_no], c.date.strftime("%m/%d/%Y"), "%02d:%02d" % (c.hour, c.minute),
                    c.employee_id, c.employer, c.job, c.dept, cls, typ, ii, c.event_code, c.event, c.nature, c.part,
                    da, dr, st, "Y" if (c.kind == "REC" and c.privacy) else "N", c.entered.strftime("%m/%d/%Y")])
    with open(os.path.join(out, F_LEGACY), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    return len(L)


# ---------------------------------------------------------------------------------------------------- platform export
def platform_days(c, upd):
    """The coordinator's 300 Log counts as of the day of the last update: calendar days from the day after the injury,
    capped at 180 in total."""
    a, b = int(c.away_true or 0), int(c.restr_true or 0)
    span = (upd - c.date).days
    sep = c.separated_after
    if sep is not None and sep >= 0 and sep < a + b:
        span = min(span, int(sep))          # the count ends when the associate leaves employment
    a2 = min(a, max(span, 0))
    b2 = min(b, max(span - a, 0))
    if a2 + b2 > 180:
        a2, b2 = (180, 0) if a2 >= 180 else (a2, 180 - a2)
    return a2, b2


def last_update(c, r):
    """When the site coordinator last touched the 300 Log entry. Closed cases are usually updated at closure; cases still
    away or restricted were last touched some time before the pull."""
    total = int(c.away_true or 0) + int(c.restr_true or 0)
    end = c.date + dt.timedelta(days=total)
    if c.separated_after is not None and c.separated_after >= 0 and c.separated_after < total:
        end = c.date + dt.timedelta(days=int(c.separated_after) + 1)
    pull = K.PULL_DATE
    if end < pull - dt.timedelta(days=9) and r.random() < 0.83:
        return min(end + dt.timedelta(days=int(r.integers(0, 6))), pull - dt.timedelta(days=1))
    lo = min(c.date + dt.timedelta(days=2), pull - dt.timedelta(days=1))
    hi = min(end, pull - dt.timedelta(days=1))
    if hi <= lo:
        return lo
    return lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))


def write_platform(W, C, out):
    info = dc_info(W)
    r = K.rng("platform_updates")
    P = C[(~C.legacy) | C.migrated].copy()
    P = P.sort_values(["platform_id"])
    recs = []
    for c in P.itertuples():
        site_no = c.dc_no
        if c.dc_no == WD.RECODE_DC and c.date >= K.week_start(*WD.RECODE_WEEK):
            site_no = WD.RECODE_NEW_NO
        rep = c.utc_dt + dt.timedelta(minutes=int(r.integers(20, 600)))
        rec = {"case_id": c.platform_id,
               "legacy_case_ref": c.legacy_no if c.migrated else None,
               "site": {"site_code": "DC%d" % site_no, "establishment": info.ehs_site[c.dc_no]},
               "occurred_at": c.utc_dt.strftime("%Y-%m-%dT%H:%M:00Z"),
               "reported_at": rep.strftime("%Y-%m-%dT%H:%M:00Z"),
               "person": {"associate_no": c.employee_id, "employer": c.employer, "job_title": c.job,
                          "department": c.dept},
               "classification": {}, "oiics": {"event_code": c.event_code, "event": c.event, "nature": c.nature,
                                               "body_part": c.part}}
        if c.kind == "FA":
            rec["classification"] = {"category": "First Aid", "osha_case_type": None, "injury_illness_type": None}
            rec["osha_log"] = None
            rec["status"] = "Closed"
        else:
            typ = "OTHER" if c.kind == "REMOVED" else c.case_type
            rec["classification"] = {"category": "Recordable", "osha_case_type": OSHA_TYPE_PLAT[typ],
                                     "injury_illness_type": "Injury" if not c.illness else c.illness}
            upd = last_update(c, r) if c.kind == "REC" else min(c.entered + dt.timedelta(days=int(r.integers(8, 40))),
                                                                 K.PULL_DATE - dt.timedelta(days=1))
            if c.migrated:
                upd = max(upd, K.MIGRATION)
            a2, b2 = platform_days(c, upd) if c.kind == "REC" else (0, 0)
            rec["osha_log"] = {"days_away_from_work": a2, "days_job_transfer_restriction": b2,
                               "days_last_updated": upd.isoformat(), "privacy_case": bool(c.kind == "REC" and c.privacy)}
            total = int(c.away_true or 0) + int(c.restr_true or 0)
            if c.kind == "REMOVED":
                rec["status"] = "Removed - not work-related"
            else:
                still = c.date + dt.timedelta(days=total) >= K.PULL_DATE
                rec["status"] = "Open" if (still or upd < c.date + dt.timedelta(days=total)) else "Closed"
        recs.append(rec)
    doc = {"export": {"system": "EHS platform", "report": "Incident cases - full extract", "exported_at": "2026-11-02T13:41:07Z",
                      "exported_by": "jdelgado", "filters": {"occurred_on_or_after": "2024-07-01", "include_migrated": True},
                      "record_count": len(recs)},
           "cases": recs}
    with open(os.path.join(out, F_PLATFORM), "w", encoding="utf-8", newline="\n") as f:
        f.write('{"export": ' + json.dumps(doc["export"], ensure_ascii=False, separators=(",", ":")) + ',\n"cases": [\n')
        for i, rec in enumerate(recs):
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + (",\n" if i < len(recs) - 1 else "\n"))
        f.write("]}\n")
    return len(recs)


# ---------------------------------------------------------------------------------------------------- WFM hours
IND_SHARES = {"INV": 0.31, "MNT": 0.24, "SAN": 0.33, "TRN": 0.12}


def wfm_frame(W):
    h = W.hist
    info = dc_info(W)
    rows = []
    for dn, hd in h.groupby("dc_no"):
        r = K.rng("wfm", int(dn))
        agy = float(info.agy_share[dn])
        nw = len(hd)
        peak = np.clip(hd.surge.values - 1, 0, None)
        agy_w = np.clip(agy * (1 + 2.2 * peak) * np.exp(r.normal(0, 0.12, nw)), 0, 0.45)
        ot_w = np.clip(0.035 + 0.32 * peak + r.normal(0, 0.012, nw), 0.004, 0.2)
        ind_split = {k: IND_SHARES[k] * np.exp(r.normal(0, 0.08, nw)) for k in K.INDIRECT}
        tot_split = sum(ind_split.values())
        for i, row in enumerate(hd.itertuples()):
            fy, wk = row.fy, row.wk
            wend = K.week_start(fy, wk) + dt.timedelta(days=6)
            no = dc_no_at(int(dn), fy, wk)
            for f in K.FUNCS:
                hrs = getattr(row, "h_" + f)
                a = hrs * agy_w[i]
                e = hrs - a
                o = e * ot_w[i]
                rows.append((no, fy, wk, wend, f, e - o, o, a))
            for k in K.INDIRECT:
                hrs = row.indirect * ind_split[k][i] / tot_split[i]
                o = hrs * ot_w[i] * 0.6
                rows.append((no, fy, wk, wend, k, hrs - o, o, 0.0))
    F = pd.DataFrame(rows, columns=["DC_NO", "FISCAL_YEAR", "FISCAL_WEEK", "WEEK_ENDING", "DEPT", "REG_HRS", "OT_HRS",
                                    "AGY_HRS"])
    for c in ["REG_HRS", "OT_HRS", "AGY_HRS"]:
        F[c] = F[c].round(2)
    return F


def write_wfm(W, out):
    F = wfm_frame(W)
    F = F.sort_values(["FISCAL_YEAR", "FISCAL_WEEK", "DC_NO", "DEPT"], kind="mergesort")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(list(F.columns))
    for row in F.itertuples(index=False):
        w.writerow([row.DC_NO, row.FISCAL_YEAR, row.FISCAL_WEEK, row.WEEK_ENDING.isoformat(), row.DEPT,
                    "%.2f" % row.REG_HRS, "%.2f" % row.OT_HRS, "%.2f" % row.AGY_HRS])
    with open(os.path.join(out, F_WFM), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    return F


# ---------------------------------------------------------------------------------------------------- WMS throughput
def wms_frame(W):
    h = W.hist
    info = dc_info(W)
    rows = []
    for row in h.itertuples():
        code = loc_at(row.dc_no, info.wms_code[row.dc_no], row.fy, row.wk)
        for c in K.CATS:
            rows.append((code, row.fy, row.wk, cat_code(c, row.fy, row.wk), int(round(getattr(row, "c_" + c)))))
    return pd.DataFrame(rows, columns=["loc_code", "fiscal_year", "fiscal_week", "category_code", "cases_shipped"])


def write_wms(W, out):
    F = wms_frame(W).sort_values(["fiscal_year", "fiscal_week", "loc_code", "category_code"], kind="mergesort")
    tbl = pa.Table.from_pandas(F.reset_index(drop=True), preserve_index=False,
                               schema=pa.schema([("loc_code", pa.string()), ("fiscal_year", pa.int16()),
                                                 ("fiscal_week", pa.int8()), ("category_code", pa.string()),
                                                 ("cases_shipped", pa.int32())]))
    tbl = tbl.replace_schema_metadata({"source": "WMS weekly throughput by product category", "pulled": "2026-11-02"})
    pq.write_table(tbl, os.path.join(out, F_WMS), compression="snappy", use_dictionary=True, write_statistics=False)
    return F


# ---------------------------------------------------------------------------------------------------- standards
def write_standards(W, out):
    info = dc_info(W)
    wb = XU.Workbook()
    ws = wb.sheet("Minutes per case")
    ws.rows.append(["Engineered labor standards - minutes per case shipped", None, None, None, None])
    ws.rows.append(["Library ELS-2019.2, effective 2019-08-04. Industrial Engineering.", None, None, None, None])
    ws.rows.append([None, None, None, None, None])
    ws.rows.append(["Function", "AMB", "CHL", "FRZ", "HVB"])
    for f in K.FUNCS:
        ws.rows.append([f] + [K.STD_BASE[f][c] for c in K.CATS])
    ws.rows.append([None, None, None, None, None])
    ws.rows.append(["RCV receiving, PUT putaway and replenishment, SEL order selection, LOD loading.", None, None, None, None])
    ws.widths = [18, 10, 10, 10, 10]
    ws2 = wb.sheet("Site factors")
    ws2.rows.append(["DC_NO", "DC_NAME", "FUNCTION", "FACTOR", "EFFECTIVE_FROM", "EFFECTIVE_TO", "STUDY_REF"])
    for dn in sorted(info.index):
        nm = info.ehs_site[dn]
        lay = float(info.layout[dn])
        ref = "IE-%s-%d" % (info.wms_code[dn][:3], 2019 if dn % 3 else 2020)
        if dn == WD.RESTUDY_DC:
            cut = K.week_start(*WD.RESTUDY_WEEK)
            new = round(lay * 0.93, 3)
            for f in ("PUT", "SEL"):
                ws2.rows.append([dn, nm, f, lay, "2019-08-04", (cut - dt.timedelta(days=1)).isoformat(), ref])
                ws2.rows.append([dn, nm, f, new, cut.isoformat(), None, "IE-LBN-2024-03"])
        elif dn == WD.RECODE_DC:
            cut = K.week_start(*WD.RECODE_WEEK)
            for f in ("PUT", "SEL"):
                ws2.rows.append([dn, nm, f, lay, "2019-08-04", (cut - dt.timedelta(days=1)).isoformat(), ref])
                ws2.rows.append([WD.RECODE_NEW_NO, nm, f, lay, cut.isoformat(), None, ref])
        else:
            for f in ("PUT", "SEL"):
                ws2.rows.append([dn, nm, f, lay, "2019-08-04", None, ref])
    ws2.widths = [8, 22, 10, 8, 14, 14, 16]
    ws3 = wb.sheet("Notes")
    for line in [
        "Minutes per case shipped, by direct labor function and WMS product category (codes as from FY2023 period 7; before",
        "then DRYG = AMB, PERI = CHL, FROZ = FRZ, BULK = HVB).",
        "A DC's standard hours for a week = sum over categories of cases shipped x the function's minutes / 60, summed over",
        "RCV, PUT, SEL and LOD; PUT and SEL minutes are multiplied by the DC's site factor in force that week.",
        "Site factors reflect slot layout and travel; a re-study replaces the factor from its effective date.",
        "RCV and LOD carry no site factor.",
        "Used for labor budgets in the operating plan. Questions to Kurt Gilbert, Industrial Engineering.",
    ]:
        ws3.rows.append([line])
    ws3.widths = [118]
    wb.save(os.path.join(out, F_STD), title="Engineered labor standards", creator=K.ORG)


# ---------------------------------------------------------------------------------------------------- the plan
def write_plan(W, out):
    P = W.plan
    info = dc_info(W)
    wb = XU.Workbook()
    rm = wb.sheet("Read me")
    for line in [
        "FY2027 Operating Plan - DC volume and labor (version 3)",
        "Approved by the executive team 10/23/2026. Operations Planning (FP&A): Nichole Sandoval.",
        "",
        "Volume: cases shipped by DC, fiscal period and WMS product category, from the commercial team's FY2027 forecast by",
        "account. The Dunleavy Club and Pruett Family Grocers accounts start in period 1 at the DCs carrying them.",
        "Labor hours: direct labor hours (receiving, putaway and replenishment, order selection, loading) by DC and period",
        "from the FY2027 labor model, version 3; indirect hours (inventory control, maintenance, sanitation, training) by DC",
        "and period. Hours are Ostrander and agency associates' hours together, as the WFM system records them.",
        "Fiscal 2027 runs Sunday 12/27/2026 to Saturday 12/25/2027, 52 weeks in 4-4-5 periods (Periods sheet).",
    ]:
        rm.rows.append([line if line else None])
    rm.widths = [120]
    vs = wb.sheet("Volume")
    vs.rows.append(["DC_NO", "DC_NAME", "PERIOD", "CATEGORY", "CASES"])
    for row in P.sort_values(["dc_no", "per"]).itertuples():
        no = WD.RECODE_NEW_NO if row.dc_no == WD.RECODE_DC else row.dc_no
        for c in K.CATS:
            vs.rows.append([no, info.ehs_site[row.dc_no], row.per, c, int(getattr(row, "c_" + c))])
    vs.widths = [8, 22, 8, 10, 12]
    hs = wb.sheet("Labor hours")
    hs.rows.append(["DC_NO", "DC_NAME", "PERIOD", "DIRECT_HOURS", "INDIRECT_HOURS"])
    for row in P.sort_values(["dc_no", "per"]).itertuples():
        no = WD.RECODE_NEW_NO if row.dc_no == WD.RECODE_DC else row.dc_no
        hs.rows.append([no, info.ehs_site[row.dc_no], row.per, float(row.direct), float(row.indirect)])
    hs.widths = [8, 22, 8, 14, 16]
    ps = wb.sheet("Periods")
    ps.rows.append(["PERIOD", "FIRST_DAY", "LAST_DAY", "WEEKS"])
    for p in range(1, 13):
        wks = K.period_weeks(2027, p)
        a = K.week_start(2027, wks[0])
        b = K.week_start(2027, wks[-1]) + dt.timedelta(days=6)
        ps.rows.append([p, a.isoformat(), b.isoformat(), len(wks)])
    ps.widths = [8, 12, 12, 8]
    wb.save(os.path.join(out, F_PLAN), title="FY2027 Operating Plan v3", creator=K.ORG)


# ---------------------------------------------------------------------------------------------------- register
def write_register(W, out):
    info = dc_info(W)
    cols = ["DC_NO", "DC_NAME", "WMS_LOC", "EHS_ESTABLISHMENT", "CITY", "STATE", "SQ_FT", "OPENED", "CLIENTS",
            "TEMPERATURE_ZONES", "ERGO_PROGRAM_FY27", "NOTES"]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cols)
    r = K.rng("register")
    for dn in sorted(info.index):
        d = info.loc[dn]
        zones = "Ambient; Cooler; Freezer" if d.mix_FRZ > 0.10 else "Ambient; Cooler"
        note = ""
        no, loc = dn, d.wms_code
        if dn == WD.RECODE_DC:
            note = "Re-numbered 318 / RKF2 from FY2025 wk 14 (client transition); 311 / RKF1 before"
            no, loc = "311; 318", "RKF1; RKF2"
        if dn == WD.RESTUDY_DC:
            note = "Re-slot and IE re-study FY2024 P7"
        w.writerow([no, d.ehs_site.replace(" DC", ""), loc, d.ehs_site, d.city, d.state,
                    int(d.sqft), int(d.opened), d.clients, zones, "Y" if d.programme else "N", note])
    with open(os.path.join(out, F_REG), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())


# ---------------------------------------------------------------------------------------------------- ITA submissions
def write_ita(W, C, out):
    """Form 300A summaries as submitted to OSHA's Injury Tracking Application, by calendar year."""
    info = dc_info(W)
    h = W.hist
    r = K.rng("ita")
    # hours by calendar year: each fiscal week's hours spread over its seven days
    rows = []
    hours = {}
    for row in h.itertuples():
        d0 = row.week_start
        per_day = row.hours / 7.0
        for k in range(7):
            d = d0 + dt.timedelta(days=k)
            hours[(row.dc_no, d.year)] = hours.get((row.dc_no, d.year), 0.0) + per_day
    salaried = {dn: float(np.clip(r.normal(0.062, 0.012), 0.03, 0.1)) for dn in info.index}
    rec = C[C.kind == "REC"]
    cols = ["year_filing_for", "establishment_name", "company_name", "city", "state",
            "naics_code", "industry_description", "establishment_type", "size", "annual_average_employees",
            "total_hours_worked", "total_deaths", "total_dafw_cases", "total_djtr_cases",
            "total_other_cases", "total_dafw_days", "total_djtr_days", "total_injuries", "total_skin_disorders",
            "total_respiratory_conditions", "total_poisonings", "total_hearing_loss", "total_other_illnesses",
            "submission_date"]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cols)
    for yr in range(2021, 2026):
        for dn in sorted(info.index):
            d = info.loc[dn]
            hrs = hours.get((dn, yr), 0.0) * (1 + salaried[dn])
            cs = rec[(rec.dc_no == dn) & (rec.date >= dt.date(yr, 1, 1)) & (rec.date <= dt.date(yr, 12, 31))]
            dafw = int((cs.case_type == "DAFW").sum())
            djtr = int((cs.case_type == "DJTR").sum())
            oth = int((cs.case_type == "OTHER").sum())
            cert = dt.date(yr + 1, 2, 10)
            da = db = 0
            for c in cs.itertuples():
                a, b = platform_days(c, cert)
                da += a
                db += b
            skin = int((cs.illness == "Skin disorder").sum())
            othill = int((cs.illness == "All other illnesses").sum())
            inj = len(cs) - skin - othill
            naics = "493120" if d.mix_FRZ > 0.17 else "493110"
            desc = "Refrigerated Warehousing and Storage" if naics == "493120" else "General Warehousing and Storage"
            sub = dt.date(yr + 1, 2, 18) + dt.timedelta(days=int(r.integers(0, 12)))
            w.writerow([yr, d.ehs_site.upper(), K.ORG_LEGAL.upper(), d.city.upper(), d.state,
                        naics, desc, 1, 3, int(round(hrs / 2000.0)), int(round(hrs)), 0, dafw,
                        djtr, oth, da, db, inj, skin, 0, 0, 0, othill, sub.isoformat()])
    with open(os.path.join(out, F_ITA), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
