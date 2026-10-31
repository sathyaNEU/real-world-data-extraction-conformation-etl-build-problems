"""Write the data files of target/: the vendor's twelve monthly exports and its TMC table, the planning team's
route file, the operator's deadhead route and 2027 charges, the HR holiday calendars and staff extract, the
parking office's reassignment workbook, and the two neighbouring files (the staff commute survey and the express
route timetable)."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

import asks as A
import core
import postprocess as PP
import world as WD

ORG = "Beargrass Medical Center"
VENDOR = "Trelvane Mobility Data"
OPERATOR = "Ridgeline Transit Services"
MONTHS = [(2025, m) for m in (10, 11, 12)] + [(2026, m) for m in range(1, 10)]
FILES = {"probe_%d-%02d" % ym: "trelvane_tmc_export_%d-%02d.csv" % ym for ym in MONTHS}
FILES.update({
    "tmc": "TMC_Identification.csv",
    "route": "route_cedar_grove_to_brook_st.xlsx",
    "deadhead": "ridgeline_deadhead_route_brook_st_yard.xlsx",
    "standard": "staff_shuttle_service_standard.docx",
    "budget": "shuttle_service_budget_note_2027.docx",
    "notice": "chestnut_garage_closure_notice.pdf",
    "charges": "ridgeline_schedule_of_charges_2027.xlsx",
    "holidays": "hr_holiday_calendars.xlsx",
    "hr": "hr_staff_extract_2026-10-02.csv",
    "reassign": "cedar_grove_reassignment_list.xlsx",
    "survey": "staff_commute_survey_2026.csv",
    "transit": "route_40x_southwest_express_timetable.pdf",
})
DISTRACTORS = ["survey", "transit"]
RELEASE_2025, RELEASE_2026 = "2025.2", "2026.1"


def _csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def _sheet(wb, title, header, rows, widths, note=None, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    r0 = 1
    if note:
        for line in note:
            ws.cell(row=r0, column=1, value=line)
            r0 += 1
        r0 += 1
    for j, h in enumerate(header, start=1):
        c = ws.cell(row=r0, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for i, row in enumerate(rows, start=r0 + 1):
        for j, v in enumerate(row, start=1):
            c = ws.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "mm/dd/yyyy"
    for j, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)
    return ws


# --------------------------------------------------------------------------------------------- the vendor export
def segment_arrays(W, i):
    """Day i's passenger travel times for every code valid that day, as {code: (NE,) array}."""
    d = W["days"][i]
    out = {}
    for k, r in enumerate(core.ROUTE):
        out[r[0]] = W["route"][i][:, k]
    for k, r in enumerate(core.OTHER):
        out[r[0]] = W["other"][i][:, k]
    if d < core.RELEASE_2026:
        for k, r in enumerate(core.DEADHEAD):
            out[r[0]] = W["dead"][i][:, k]
        out[core.RAMP_2025] = W["ramp"][i]
    else:
        for k, r in enumerate(core.DEADHEAD):
            if k != core.T1_INDEX:
                out[r[0]] = W["dead"][i][:, k]
        for j, r in enumerate(core.T1_NEW):
            out[r[0]] = W["split"][i][:, j]
        out[core.RAMP_2026] = W["ramp"][i]
    return out


def segment_records(d):
    recs = {r[0]: r for r in core.codes_for(d)}
    return recs


def density(code, kind, t):
    """A for most rows; B for thin periods; C for the arterial and ramp segments before 6:00 and every segment
    before 6:30 on weekends and holidays (too few probe vehicles; the vendor fills from history)."""
    arterial = code in {core.ROUTE[k][0] for k in core.ARTERIAL} or code in (core.RAMP_2025, core.RAMP_2026, "121P04801")
    if kind in ("weekend", "holiday"):
        return "C" if t < 6 * 60 + 30 else "B"
    if arterial and t < 6 * 60:
        return "C"
    if t < 6 * 60 + 15 or t >= 9 * 60 + 10:
        return "B"
    return "A"


ROUTE_CODES = {r[0] for r in core.ROUTE}


def omitted(rg, code, kind, t):
    """An epoch with no probe vehicles and no usable history is left out of the export: now and then on the
    ramps, the arterials and the counter-peak direction early in the morning, and on the route itself only
    before 6:30 on weekends and holidays."""
    quiet = kind in ("weekend", "holiday")
    if code in ROUTE_CODES:
        return quiet and t < 6 * 60 + 30 and rg.random() < 0.03
    return rg.random() < (0.006 if (quiet or t < 6 * 60 + 15) else 0.0008)


def probe(path, W, ym):
    rng = np.random.default_rng([WD.SEED, 61, ym[0], ym[1]])
    rg = np.random.default_rng([WD.SEED, 62, ym[0], ym[1]])
    rows = []
    for i, d in enumerate(W["days"]):
        if (d.year, d.month) != ym:
            continue
        arrs = segment_arrays(W, i)
        recs = segment_records(d)
        kind = W["kind"][i]
        codes = sorted(arrs)
        tt = np.stack([arrs[c] for c in codes], axis=1)          # NE x codes
        allv, frt = WD.classes(tt, rng)
        for k, r in enumerate(core.ROUTE):                        # the route's classes as the analysis reads them
            j = codes.index(r[0])
            allv[:, j], frt[:, j] = W["route_all"][i][:, k], W["route_frt"][i][:, k]
        miles = np.array([recs[c][4] for c in codes])
        ref = np.array([round(recs[c][4] / recs[c][5] * 3600, 1) for c in codes])
        for e in range(core.NE):
            t = int(core.EPOCHS[e])
            stamp = "%s %02d:%02d:00" % (d.isoformat(), t // 60, t % 60)
            for j, c in enumerate(codes):
                if omitted(rg, c, kind, t):
                    continue
                sp = miles[j] / tt[e, j] * 3600
                rows.append((c, stamp, "%.2f" % (miles[j] / allv[e, j] * 3600), "%.2f" % allv[e, j], "%.2f" % sp,
                             "%.2f" % tt[e, j], "%.2f" % (miles[j] / frt[e, j] * 3600), "%.2f" % frt[e, j],
                             "%.1f" % ref[j], density(c, kind, t)))
    rows.sort(key=lambda r: (r[0], r[1]))
    _csv(path, ["tmc_code", "measurement_tstamp_local", "speed_all", "travel_time_all", "speed_passenger",
                "travel_time_passenger", "speed_freight", "travel_time_freight", "reference_speed", "data_density"],
         rows)


ROAD_ORDER = {("I-65", "NORTHBOUND"): ["121P04501", "121P04502", "121P04503", "121P04504", "121P04505", "121P04506",
                                        "121P04507", "121P04508", "121P04509", "121P04510", "121P04511", "121P04512",
                                        "121P04513", "121P04517", "121P04518", "121P04519"],
              ("S Brook St", "NORTHBOUND"): ["121P04514", "121P04515", "121P04516"],
              ("I-264", "EASTBOUND"): ["121P04210", "121P04212"],
              ("KY-480", "EASTBOUND"): ["121P04801"]}


def road_order(codes):
    """Each code's position along its road and direction in a release (I-65 southbound from Broadway, I-264
    westbound from Poplar Level Road with the collector ramp at the interchange)."""
    out = {}
    for (road, direc), seq in ROAD_ORDER.items():
        for k, c in enumerate(seq, start=1):
            out[c] = k
    have = {r[0] for r in codes}
    sb = [r[0] for r in core.DEADHEAD]
    if core.T1_NEW[0][0] in have:
        sb = sb[:core.T1_INDEX] + [r[0] for r in core.T1_NEW] + sb[core.T1_INDEX + 1:]
    for k, c in enumerate(sb, start=1):
        out[c] = k
    wb = ["121N04213"] + [r[0] for r in codes if r[1] == "I-264" and r[2] == "WESTBOUND" and r[0] not in
                          ("121N04213", "121N04211")] + ["121N04211"]
    for k, c in enumerate(wb, start=1):
        out[c] = k
    return out


def tmc_table(path):
    rows = []
    for rel, eff, day in ((RELEASE_2025, "2025-07-01", dt.date(2025, 12, 1)),
                          (RELEASE_2026, "2026-04-01", dt.date(2026, 6, 1))):
        codes = core.codes_for(day)
        ro = road_order(codes)
        for r in sorted(codes, key=lambda x: x[0]):
            county = "Bullitt" if r[0] in ("121P04501", "121P04801") else "Jefferson"
            rows.append([r[0], rel, eff, r[1], r[2], r[3], "KY", county, "%.3f" % r[4], ro[r[0]], r[6]])
    rows.sort(key=lambda x: (x[1], x[0]))
    _csv(path, ["tmc", "network_release", "effective_date", "road", "direction", "intersection", "state", "county",
                "miles", "road_order", "f_system"], rows)


# --------------------------------------------------------------------------------------------- the route files
def route_file(path):
    wb = Workbook()
    rows = [[1, "Leg", "Cedar Grove park-and-ride, boarding bay to I-65 N on-ramp (KY-480)", None, 4]]
    for k, r in enumerate(core.ROUTE, start=2):
        rows.append([k, "TMC", r[3], r[0], None])
    rows.append([len(core.ROUTE) + 2, "Leg", "S Brook St at E Chestnut St to the Brook Street shuttle bay", None, 3])
    _sheet(wb, "Route", ["Seq", "Type", "Description", "TMC", "Fixed minutes"], rows, [6, 8, 70, 13, 14],
           first=True, note=["Staff shuttle route: Cedar Grove park-and-ride to Brook Street stop (morning run)",
                             "Transportation Planning, October 2026. TMC codes as in the vendor's 2026.1 release; "
                             "fixed legs timed on the operator's test runs"])
    wb.save(path)
    PP.normalize_xlsx(path, "Ebony Robinson", "2026-10-06T14:12:00Z", "2026-10-09T19:40:00Z", company=ORG)


def deadhead_file(path):
    wb = Workbook()
    rows = [[1, "Leg", "Brook Street shuttle bay to I-65 S on-ramp at Broadway", None, A.LEG_MILES_IN]]
    for k, r in enumerate(core.DEADHEAD, start=2):
        rows.append([k, "TMC", r[3], r[0], None])
    rows.append([len(core.DEADHEAD) + 2, "Leg", "I-65 Exit 128 (Fern Valley Rd) to Fern Valley yard", None,
                 A.LEG_MILES_OUT])
    _sheet(wb, "Deadhead", ["Seq", "Type", "Description", "TMC", "Leg miles"], rows, [6, 8, 66, 13, 11],
           first=True, note=["%s: deadhead route, Brook Street stop to Fern Valley yard" % OPERATOR,
                             "Set up for the hospital's shuttle proposal, October 2025 (Bethany Thompson)"])
    wb.save(path)
    PP.normalize_xlsx(path, "Bethany Thompson", "2025-10-14T15:31:00Z", "2025-10-14T16:02:00Z", company=OPERATOR)


def charges_file(path):
    wb = Workbook()
    rows = [["Vehicle", "28-passenger cutaway (seated), wheelchair lift", None, None],
            ["Seats per vehicle", None, A.SEATS, "seated passengers; no standees"],
            ["Day charge, morning run", "per vehicle per service day, pull-out to the Brook Street stop", A.DAY_RATE,
             "USD"],
            ["Deadhead to yard", "per vehicle-mile, Brook Street stop to the Fern Valley yard", A.MILE_RATE,
             "USD, on the deadhead route"],
            ["Early-run differential", "per vehicle per service day, morning runs leaving Cedar Grove before 6:00 a.m.",
             31.00, "USD"],
            ["Cancellation", "service days cancelled by the hospital with less than 24 hours' notice", 214.00,
             "USD per vehicle"],
            ["Term", "4 January 2027 to 31 December 2027", None, None]]
    _sheet(wb, "Charges 2027", ["Item", "Basis", "Amount", "Unit / remarks"], rows, [30, 62, 12, 30], first=True,
           note=["%s: schedule of charges, Beargrass Medical Center staff shuttle, 2027" % OPERATOR,
                 "Issued 18 September 2026 with the 2027 service order draft"])
    wb.save(path)
    PP.normalize_xlsx(path, "Bethany Thompson", "2026-09-18T13:05:00Z", "2026-09-18T13:47:00Z", company=OPERATOR)


def holidays_file(path):
    wb = Workbook()
    rows = [[d, d.strftime("%A"), n] for d, n in core.HOLIDAYS]
    _sheet(wb, "2025-26", ["Date", "Day", "Holiday"], rows, [12, 12, 34], first=True,
           note=["Hospital holidays, October 2025 to September 2026 (observed dates)", "Human Resources"])
    rows = [[d, d.strftime("%A"), n] for d, n in core.HOLIDAYS_2027]
    _sheet(wb, "2027", ["Date", "Day", "Holiday"], rows, [12, 12, 34],
           note=["Hospital holidays, calendar 2027 (observed dates)", "Human Resources"])
    wb.save(path)
    PP.normalize_xlsx(path, "Andrew Brown", "2025-08-11T15:00:00Z", "2026-08-24T18:22:00Z", company=ORG)


# ------------------------------------------------------------------------------------------------- staff files
CC = {"Nursing": ["4110 4 East Med-Surg", "4120 5 West Med-Surg", "4130 Cardiac Step-Down", "4140 Surgical Services",
                  "4150 Outpatient Infusion"],
      "Imaging": ["5210 Diagnostic Radiology", "5220 CT and MRI"], "Laboratory": ["5310 Core Laboratory",
                                                                                  "5320 Pathology"],
      "Pharmacy": ["5410 Inpatient Pharmacy"], "Rehabilitation": ["5510 Physical Therapy", "5520 Occupational Therapy"],
      "Support Services": ["6110 Environmental Services", "6120 Food and Nutrition", "6130 Patient Transport"],
      "Administration": ["7110 Patient Access", "7120 Health Information", "7130 Finance"]}
JOB = {"Nursing": "Clinical", "Imaging": "Clinical", "Laboratory": "Clinical", "Pharmacy": "Clinical",
       "Rehabilitation": "Clinical", "Support Services": "Support", "Administration": "Administrative"}


def hr_file(path, S):
    rng = np.random.default_rng([WD.SEED, 71])
    rows = []
    for h in sorted(S["hr"], key=lambda x: x["employee_no"]):
        cc = CC[h["department"]][int(rng.integers(len(CC[h["department"]])))]
        fte = rng.choice(["1.00", "1.00", "1.00", "0.90", "0.80", "0.60"])
        rows.append([h["employee_no"], h["payroll_id"], h["department"], cc, JOB[h["department"]], h["start"], fte])
    _csv(path, ["employee_no", "payroll_id", "department", "cost_center", "job_family", "sched_start_hhmm", "fte"],
         rows)


def reassign_file(path, S):
    rng = np.random.default_rng([WD.SEED, 72])
    wb = Workbook()
    roll = list(S["permit"])
    permits = rng.choice(np.arange(20100, 29900), size=len(roll), replace=False)
    rows = sorted([["CG-%05d" % p, r["employee_no"], r["department"], "%02d:%02d" % (r["start"] // 100, r["start"] % 100)]
                   for p, r in zip(permits, roll)], key=lambda x: x[0])
    _sheet(wb, "Permit roll", ["Permit", "Employee no.", "Department", "Start"], rows, [11, 13, 18, 8], first=True,
           note=["Chestnut Street garage permit holders reassigned to Cedar Grove from 4 January 2027",
                 "Parking Services, permit system export 25 September 2026"])
    req = list(S["late"])
    order = rng.permutation(len(req))
    base = dt.date(2026, 9, 28)
    recs = []
    for i in order:
        recs.append((base + dt.timedelta(days=int(rng.integers(0, 17))), int(i)))
    recs.sort()
    rows = []
    for n, (day, i) in enumerate(recs):
        r = req[i]
        h, m = r["start"] // 100, r["start"] % 100
        rows.append(["LR-%04d" % (311 + n), r["payroll_id"], r["department"], "%d:%02d AM" % (h, m), day])
    _sheet(wb, "Late requests", ["Request", "Payroll ID", "Department", "Start", "Received"], rows,
           [10, 12, 18, 10, 12], note=["Cedar Grove spaces granted on requests through the HR Service Center form "
                                       "after the permit export", "HR Service Center, to 14 October 2026"])
    rows = [[r["employee_no"], base + dt.timedelta(days=int(rng.integers(2, 19))),
             ["Transit pass", "Carpool", "Bicycle", "Dropped off"][int(rng.integers(4))]] for r in S["optout"]]
    rows.sort(key=lambda x: (x[1], x[0]))
    _sheet(wb, "Opt-outs", ["Employee no.", "Date", "Instead"], rows, [13, 12, 14],
           note=["Permit holders who have opted out of Cedar Grove", "Parking Services, to 16 October 2026"])
    wb.save(path)
    PP.normalize_xlsx(path, "Andrew Brown", "2026-09-25T14:10:00Z", "2026-10-16T20:31:00Z", company=ORG)


def survey_file(path):
    rng = np.random.default_rng([WD.SEED, 81])
    rows = []
    modes = ["Drive alone", "Carpool", "Bus", "Bicycle", "Walk", "Dropped off"]
    zips = ["40118", "40165", "40109", "40219", "40229", "40214", "40217", "40204", "40208", "40047", "40150"]
    for k in range(1187):
        rows.append(["R%05d" % (1000 + k), ["Clinical", "Support", "Administrative"][int(rng.integers(3))],
                     modes[int(rng.choice(6, p=[0.71, 0.09, 0.08, 0.03, 0.03, 0.06]))],
                     zips[int(rng.integers(len(zips)))], int(rng.integers(8, 75)),
                     ["Yes", "No", "Maybe"][int(rng.integers(3))]])
    _csv(path, ["response_id", "job_family", "usual_mode", "home_zip", "usual_commute_min",
                "would_use_park_and_ride"], rows)


def write(W, S, target):
    os.makedirs(target, exist_ok=True)
    P = lambda k: os.path.join(target, FILES[k])
    for ym in MONTHS:
        probe(P("probe_%d-%02d" % ym), W, ym)
    tmc_table(P("tmc"))
    route_file(P("route"))
    deadhead_file(P("deadhead"))
    charges_file(P("charges"))
    holidays_file(P("holidays"))
    hr_file(P("hr"), S)
    reassign_file(P("reassign"), S)
    survey_file(P("survey"))
