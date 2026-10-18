"""The exports' rows, written from the clean truth in each system's own layout. Layer 1 mess is how each system
writes its file: the legacy capacity export dates a row by the morning report and codes surge as S1/S2; the new
capacity system keys by facility id and dates by census night; Crestfield's member shift report runs in UTC and bills
a night shift on two lines, one per calendar day; Inland Seas' weekly workbook dates a shift by its payroll day, a
night being paid on the day it ends. None of it moves the call (checks.py, R2)."""
from __future__ import annotations

import datetime as dt

import common as C
import world as W

D = dt.date

OLD_NAMES = {
    "GA-0412": "TALCOTT HOSP", "GA-0418": "TOLLIVER GEN HOSP", "GA-0425": "GILMARTIN MED CTR",
    "GA-0431": "SATTERFIELD MED CTR", "GA-0437": "HALDANE COMM HOSP", "GA-0442": "LATTIMORE MEM HOSP",
    "SC-0446": "BRENNAN MEM HOSP", "SC-0451": "KINARD HOSP", "SC-0455": "RUDDOCK HOSP",
    "TN-0503": "HAVERKAMP MED CTR", "TN-0508": "KASTNER HOSP", "KY-0514": "ELLERY MED CTR",
    "KY-0519": "BRINKERHOFF MEM HOSP", "WV-0523": "ZIELINSKI MEM HOSP", "WV-0528": "SPURLOCK MEM HOSP",
    "TN-0532": "CRUMLEY MEM HOSP", "MI-0604": "OSTRANDER MED CTR", "MI-0609": "LINDELL HOSP",
    "MI-0613": "ALPENA LAKESIDE HOSP", "MI-0617": "CALLISTER MEM HOSP", "MI-0622": "CLAM LAKE COMM HOSP",
    "MI-0626": "SUPERIOR SHORES MED CTR", "MI-0631": "LITTLE BAY DE NOC HOSP", "MI-0635": "ASHMUN BAY HOSP",
}
# Crestfield's client site codes and Inland Seas' facility short names
CRS_SITE = {
    "GA-0412": "CRS-ATL-0117", "GA-0418": "CRS-ATL-0122", "GA-0425": "CRS-MAR-0203", "GA-0431": "CRS-GWN-0310",
    "GA-0437": "CRS-MAC-0405", "GA-0442": "CRS-ROM-0412", "SC-0446": "CRS-COL-0131", "SC-0451": "CRS-GVL-0318",
    "SC-0455": "CRS-SPA-0209", "TN-0503": "CRS-KNX-0502", "TN-0508": "CRS-CHA-0516", "KY-0514": "CRS-LEX-0521",
    "KY-0519": "CRS-LOU-0533", "WV-0523": "CRS-CHS-0540", "WV-0528": "CRS-HTN-0548", "TN-0532": "CRS-JCY-0555",
    "MI-0604": "CRS-GTR-0711", "MI-0609": "CRS-EMM-0716", "MI-0613": "CRS-ALP-0720", "MI-0617": "CRS-OTS-0724",
    "MI-0622": "CRS-WEX-0729", "MI-0626": "CRS-MQT-0802", "MI-0631": "CRS-DEL-0807", "MI-0635": "CRS-CHP-0811",
}
ISN_NAME = {
    "GA-0412": "Talcott", "GA-0418": "Tolliver General", "GA-0425": "Gilmartin MC", "GA-0431": "Satterfield MC",
    "GA-0437": "Haldane Community", "GA-0442": "Lattimore Memorial", "SC-0446": "Brennan Memorial", "SC-0451": "Kinard",
    "SC-0455": "Ruddock", "TN-0503": "Haverkamp MC", "TN-0508": "Kastner", "KY-0514": "Ellery MC",
    "KY-0519": "Brinkerhoff Memorial", "WV-0523": "Zielinski Memorial", "WV-0528": "Spurlock Memorial",
    "TN-0532": "Crumley Memorial", "MI-0604": "Ostrander MC", "MI-0609": "Lindell", "MI-0613": "Alpena Lakeside",
    "MI-0617": "Callister Memorial", "MI-0622": "Clam Lake Community", "MI-0626": "Superior Shores MC",
    "MI-0631": "Little Bay de Noc", "MI-0635": "Ashmun Bay",
}


def legacy_capacity(hs, truth):
    """The legacy capacity system's export, census nights 1 July 2021 to 30 June 2024. A row is dated by the morning
    report that carried it (the census is the previous midnight's). A member that corrected a report resubmitted it;
    the export keeps both, the resubmission marked R."""
    r = W.rng(80)
    rows = []
    for h in hs:
        fid = h["facility_id"]
        for x in truth[fid]:
            d = x["date"]
            if d >= C.NEW_SYSTEM:
                continue
            rep = d + dt.timedelta(days=1)
            stat = {0: "", 1: "S1", 2: "S2"}[x["level"]]
            if r.random() < 0.004:
                typo = x["census"] + int(r.choice([-11, -3, 2, 9, 10]))
                rows.append([h["member_no"], OLD_NAMES[fid], rep, typo, x["beds"], stat, x["resp_admits"], "O"])
                rows.append([h["member_no"], OLD_NAMES[fid], rep, x["census"], x["beds"], stat, x["resp_admits"], "R"])
            else:
                rows.append([h["member_no"], OLD_NAMES[fid], rep, x["census"], x["beds"], stat, x["resp_admits"], "O"])
    rows.sort(key=lambda z: (z[2], z[0], z[7]))
    return ["member_no", "hospital_name", "report_date", "census_midnight", "staffed_beds", "surge_status",
            "resp_admits", "submission"], rows


def new_capacity(hs, truth):
    rows = []
    for h in hs:
        fid = h["facility_id"]
        for x in truth[fid]:
            d = x["date"]
            if d < C.NEW_SYSTEM or d > C.CENSUS_END:
                continue
            status = "provisional" if (C.CENSUS_END - d).days < 7 else "final"
            rows.append([fid, d, x["census"], x["beds"], x["level"], x["resp_admits"], status])
    rows.sort(key=lambda z: (z[1], z[0]))
    return ["facility_id", "census_date", "inpatients_midnight", "staffed_beds", "surge_level", "resp_admissions",
            "record_status"], rows


def declaration_rows(hs, decl):
    r = W.rng(81)
    ini = {}
    rows = []
    for x in decl:
        if x["declared_at"].date() > C.CENSUS_END:
            continue
        fid = x["facility_id"]
        if fid not in ini:
            ini[fid] = ["%s%s" % (chr(65 + int(r.integers(0, 26))), chr(65 + int(r.integers(0, 26)))) for _ in range(5)]
        who = ini[fid][int(r.integers(0, 5))]
        huddle = "bed huddle" if x["declared_at"].time() == dt.time(6, 45) else "bed meeting"
        rows.append([x["declared_at"].strftime("%Y-%m-%d %H:%M"), fid, x["level_from"], x["level_to"], x["request_no"],
                     huddle, who])
    return ["declared_at", "facility_id", "level_from", "level_to", "request_no", "meeting", "entered_by"], rows


# ------------------------------------------------------------------------------------------------- agency reports
def _utc(t):
    return W.to_utc(t).strftime("%Y-%m-%dT%H:%M:%SZ")


def crestfield_lines(hs, shifts):
    """Crestfield's member shift report, its billing lines. Day shifts are one line; a night shift is billed on two lines,
    one for each calendar day it covers, under the night's timesheet number; a booking cancelled after the cut-off is
    one line of four hours against the booked shift. Times are UTC."""
    r = W.rng(90)
    lines = []
    ts = 4471003
    ln = 30012411
    for s in shifts:
        if s["agency"] != "C":
            continue
        if s["start"] > dt.datetime.combine(C.CENSUS_END, dt.time(7)):
            continue                                   # the night of 20 December was still being worked at the pull
        fid = s["facility_id"]
        ts += int(r.integers(1, 4))
        bill = "TRHC POOL" if s["bill"] == "POOL" else "FACILITY"
        book = "SURGE" if s["code"] == "SURGE" else "STAFF"
        a = s["start"]
        if s.get("cancelled"):
            # a booking cancelled after the cut-off: four hours billed against the booked shift, on one line
            ln += int(r.integers(1, 3))
            lines.append(["CL%08d" % ln, "T%07d" % ts, CRS_SITE[fid], s["unit"], s["nurse"], _utc(a),
                          _utc(a + dt.timedelta(hours=12)), "4.00", book, bill, s["request_no"]])
            continue
        if s["shift"] == "D":
            segs = [(a, a + dt.timedelta(hours=12))]
        else:
            mid = dt.datetime.combine(a.date() + dt.timedelta(days=1), dt.time(0))
            segs = [(a, mid), (mid, a + dt.timedelta(hours=12))]
        for b0, b1 in segs:
            ln += int(r.integers(1, 3))
            worked = (W.to_utc(b1) - W.to_utc(b0)).total_seconds() / 3600.0     # 13 or 11 across a clock change
            lines.append(["CL%08d" % ln, "T%07d" % ts, CRS_SITE[fid], s["unit"], s["nurse"], _utc(b0), _utc(b1),
                          "%.2f" % worked, book, bill, s["request_no"]])
    return ["line_id", "timesheet_no", "client_site", "unit", "worker_id", "shift_start_utc", "shift_end_utc",
            "hours", "booking_type", "bill_to", "request_ref"], lines


def payroll_date(s):
    """Inland Seas pays a night shift on the day it ends."""
    return s["start"].date() + (dt.timedelta(days=1) if s["shift"] == "N" else dt.timedelta(0))


def inland_seas_weeks(hs, shifts, s0, s1):
    """Inland Seas' weekly member shift sheets (Monday to Sunday by payroll date) for one winter."""
    weeks = {}
    for s in shifts:
        if s["agency"] != "I" or s.get("cancelled"):
            continue                                   # Inland Seas invoices late cancellations on its monthly statement
        pd = payroll_date(s)
        if not (s0 <= pd <= s1):
            continue
        wk = pd - dt.timedelta(days=pd.weekday())
        book = "Surge" if s["code"] == "SURGE" else "Staffing"
        bill = "TRHC Pool" if s["bill"] == "POOL" else "Facility"
        weeks.setdefault(wk, []).append([ISN_NAME[s["facility_id"]], s["unit"], s["nurse"], pd, s["shift"], 12.0, book,
                                         bill, s["request_no"]])
    for wk in weeks:
        weeks[wk].sort(key=lambda z: (z[3], z[4], z[0], z[1], z[2]))
    return ["Facility", "Unit", "Nurse ID", "Payroll date", "Shift", "Hours", "Booking", "Bill to", "Request ref"], weeks


def inland_seas_queries(hs, shifts, decl, s0, s1, n=14):
    """The shifts the cooperative queried with Inland Seas in the winter, with their clock times from the agency's
    timekeeping: shifts on a surge unit at the edges of an activation, picked by the settlement review."""
    r = W.rng(91)
    cand = [s for s in shifts if s["agency"] == "I" and s["surge_unit"] and not s.get("cancelled")
            and s0 <= s["start"].date() <= s1]
    edges = [s for s in cand if s["kind"] in ("after", "skeleton")]
    nights = [s for s in cand if s["shift"] == "N" and s["kind"] == "active"]
    pick = []
    for pool, k in ((edges, 5), (nights, n - 5)):
        idx = sorted(r.choice(len(pool), size=min(k, len(pool)), replace=False).tolist()) if pool else []
        pick.extend(pool[i] for i in idx)
    rows = []
    order = 482113
    for s in sorted(pick, key=lambda z: z["start"]):
        cin = s["start"] - dt.timedelta(minutes=int(r.integers(2, 14)))
        cout = s["start"] + dt.timedelta(hours=12, minutes=int(r.integers(4, 28)))
        order += int(r.integers(40, 900))
        rows.append([ISN_NAME[s["facility_id"]], s["unit"], s["nurse"], cin.strftime("%m/%d/%Y %H:%M"),
                     cout.strftime("%m/%d/%Y %H:%M"), payroll_date(s), s["shift"], "ISO-%d" % order,
                     s["request_no"] or None])
    return ["Facility", "Unit", "Nurse ID", "Clock in", "Clock out", "Payroll date", "Shift", "Order no.",
            "Request ref"], rows
