"""task160 pack: every file the winter pool manager pulled on Monday 21 December 2026, written from the records."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as C
import docs as DOC
import postprocess as PP
import records as R
import world as W

D = dt.date

F_LEGACY = "capacity_reports_legacy_2021-07-02_2024-07-01.csv"
F_DAILY = "capacity_daily_2024-07-01_2026-12-20.csv"
F_DECL = "surge_declarations_2021-07-01_2026-12-20.csv"
F_MEMBERS = "trhc_members_2026-27.xlsx"
F_BLOCKS = "january_block_orders_2022-2026.xlsx"
F_CRS = "crestfield_member_shifts_2025-11-01_2026-12-20.csv"
F_ISN25 = "inland_seas_member_shifts_2025-26.xlsx"
F_ISN26 = "inland_seas_member_shifts_2026-27.xlsx"
F_WW = "wastewater_results_2021-09-06_2026-12-17.json"
F_OUTLOOK = "resp_admissions_outlook_2026-12-18.xlsx"
F_SURVEY = "rn_workforce_survey_2025q1_2026q3.xlsx"
F_MANIFEST = "extract_manifest_2026-12-21.csv"
F_DICT = "data_dictionary.xlsx"
DISTRACTORS = [F_SURVEY, DOC.F_RATES]

HEAD_FILL = PatternFill("solid", fgColor="DDE5EE")
BOLD = Font(name="Calibri", bold=True, size=11)
BODY = Font(name="Calibri", size=11)


def _csv(path, head, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(head)
    for r in rows:
        w.writerow([x.isoformat() if isinstance(x, D) else x for x in r])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return len(rows)


def _sheet(ws, head, rows, widths=None, start_row=1, fmt=None):
    for j, h in enumerate(head):
        c = ws.cell(row=start_row, column=j + 1, value=h)
        c.font = BOLD
        c.fill = HEAD_FILL
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = ws.cell(row=start_row + 1 + i, column=j + 1, value=v)
            c.font = BODY
            if isinstance(v, D):
                c.number_format = "m/d/yyyy"
            elif fmt and j in fmt:
                c.number_format = fmt[j]
    for j, h in enumerate(head):
        ws.column_dimensions[get_column_letter(j + 1)].width = (widths[j] if widths else max(10, len(h) + 2))


def _save(wb, path, creator, last_by, created, modified):
    wb.save(path)
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=C.ORG)


# ---------------------------------------------------------------------------------------------------- the roster
def write_members(out, hs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Members"
    head = ["member_no", "facility_id", "hospital", "city", "state", "county", "region", "staffed_med_surg_beds",
            "surge_unit", "pool_member_from", "crestfield_site_code", "inland_seas_facility"]
    rows = []
    for h in hs:
        rows.append([h["member_no"], h["facility_id"], h["name"], h["city"], h["state"], h["county"],
                     C.REGIONS[h["region"]], W.staffed_beds(h, C.CENSUS_END), h["surge_unit"],
                     C.NORTH_JOIN if h["region"] == "NO" else C.POOL_START, R.CRS_SITE[h["facility_id"]],
                     R.ISN_NAME[h["facility_id"]]])
    _sheet(ws, head, rows, [11, 11, 30, 16, 7, 15, 12, 12, 18, 14, 14, 20])
    ws.freeze_panes = "A2"
    _save(wb, os.path.join(out, F_MEMBERS), C.PEOPLE["pool_manager"], C.PEOPLE["pool_manager"],
          "2021-10-04T14:20:00Z", "2026-11-02T16:05:00Z")
    return len(rows)


# ---------------------------------------------------------------------------------------------------- block orders
FIRST_BLOCK = 2250      # 2021-22, the pool's first block, set from the members' surge plans before any pool January
FILED = {2022: D(2021, 12, 20), 2023: D(2022, 12, 19), 2024: D(2023, 12, 18), 2025: D(2024, 12, 20),
         2026: D(2025, 12, 19)}


def blocks(hs, truth):
    """The blocks the pool filed: the first from the members' surge plans, each later one the pool's draw over the last
    January's block weeks at the surge plans' staffing, rounded to the nearest 50 (the pool manager's practice)."""
    out = []
    for w in sorted(FILED):
        if w == min(FILED):
            blk = FIRST_BLOCK
        else:
            a, b = C.block_weeks(w - 1)
            drew = sum(h["grid"][r["level"] - 1] for h in hs if h["region"] != "NO"
                       for r in truth[h["facility_id"]] if a <= r["date"] <= b and r["level"])
            blk = int(50 * round(drew / 50.0))
        out.append((w, blk, FILED[w]))
    return out


def season_primary(hs, w):
    """Each southern member's primary agency in the season's Schedule A. Crestfield, the pool's first agency, held the
    first slot at every member in 2021-22; members moved their first slot to Inland Seas as their staffing contracts
    came up for renewal, two or three a season in member-number order, the last of them for 2026-27."""
    movers = [h["facility_id"] for h in hs if h["region"] != "NO" and h["agency"] == "I"]
    moved = {2022: 0, 2023: 2, 2024: 4, 2025: 4, 2026: 6, 2027: len(movers)}[w]
    return {h["facility_id"]: ("I" if h["facility_id"] in movers[:moved] else "C") if h["region"] != "NO" else h["agency"]
            for h in hs}


def block_split(hs, block, members, w):
    """Each agency's share of the block in proportion to the surge unit slots the season's Schedule A gave it at Level 1
    and 2; an agency that could not confirm its share confirmed what its roster allowed and the other took the rest."""
    prim = season_primary(hs, w)
    slots = {"C": 0, "I": 0}
    for h in hs:
        if h["facility_id"] not in members:
            continue
        for g in h["grid"]:
            n = g // 2
            first = prim[h["facility_id"]]
            second = "I" if first == "C" else "C"
            slots[first] += (n + 1) // 2
            slots[second] += n // 2
    slots["C"] += sum(1 for h in hs if h["facility_id"] in members)   # Crestfield's rapid-open skeleton slot
    c = int(round(block * slots["C"] / float(slots["C"] + slots["I"])))
    i = block - c
    r = W.rng(61, w)
    conf = {"C": min(1.0, r.uniform(0.86, 1.10)), "I": min(1.0, r.uniform(0.86, 1.10))}
    if conf["I"] < 1.0:
        short = int(i * conf["I"]) // 5 * 5
        c, i = c + (i - short), short
    elif conf["C"] < 1.0:
        short = int(c * conf["C"]) // 5 * 5
        c, i = short, i + (c - short)
    return c, i


def write_blocks(out, hs, truth):
    wb = Workbook()
    ws = wb.active
    ws.title = "Block orders"
    head = ["pool_season", "block_first_day", "block_last_day", "block_shifts", "crestfield_shifts",
            "inland_seas_shifts", "filed_on", "filed_by"]
    south = {h["facility_id"] for h in hs if h["region"] != "NO"}
    rows = []
    for w, blk, filed in blocks(hs, truth):
        a, b = C.block_weeks(w)
        c, i = block_split(hs, blk, south, w)
        rows.append(["%d-%02d" % (w - 1, w % 100), a, b, blk, c, i, filed, C.PEOPLE["pool_manager"]])
    rows.append(["2026-27", C.BLOCK_2027[0], C.BLOCK_2027[1], None, None, None, None, None])
    _sheet(ws, head, rows, [12, 15, 15, 13, 16, 17, 12, 16])
    ws.freeze_panes = "A2"
    _save(wb, os.path.join(out, F_BLOCKS), C.PEOPLE["pool_manager"], C.PEOPLE["pool_manager"],
          "2021-12-20T15:40:00Z", "2025-12-19T21:12:00Z")
    return len(rows)


# ---------------------------------------------------------------------------------------------------- Inland Seas
def write_inland_seas(out, hs, shifts, decl, s0, s1, fname, queried, created, modified):
    head, weeks = R.inland_seas_weeks(hs, shifts, s0, s1)
    wb = Workbook()
    wb.remove(wb.active)
    n = 0
    for wk in sorted(weeks):
        ws = wb.create_sheet("Wk %s" % wk.strftime("%m-%d-%y"))
        ws.cell(row=1, column=1, value="Inland Seas Nursing, Inc.: member shift report to %s" % C.ORG).font = BOLD
        ws.cell(row=2, column=1, value="Week %s to %s (payroll dates)" % (wk.strftime("%m/%d/%Y"),
                                                                           (wk + dt.timedelta(days=6)).strftime("%m/%d/%Y")))
        ws.cell(row=3, column=1, value="Run %s" % min(wk + dt.timedelta(days=8), C.AS_OF).strftime("%m/%d/%Y"))
        _sheet(ws, head, weeks[wk], [22, 18, 10, 13, 7, 7, 10, 11, 18], start_row=5, fmt={5: "0.00"})
        n += len(weeks[wk])
    if queried:
        qh, qr = R.inland_seas_queries(hs, shifts, decl, s0, s1)
        ws = wb.create_sheet("Timesheet detail")
        ws.cell(row=1, column=1, value="Timesheets queried by %s, %s to %s" % (
            C.ORG_SHORT, s0.strftime("%m/%d/%Y"), s1.strftime("%m/%d/%Y"))).font = BOLD
        _sheet(ws, qh, qr, [22, 18, 10, 17, 17, 13, 7, 12, 18], start_row=3)
    _save(wb, os.path.join(out, fname), "Inland Seas Nursing", "Inland Seas Nursing", created, modified)
    return n


# ---------------------------------------------------------------------------------------------------- wastewater
def write_wastewater(out, ww):
    res = []
    for x in sorted(ww, key=lambda z: (z["sample_date"], z["sewershed"], z["target"])):
        base = {"sewershed_id": x["sewershed"], "community": x["city"], "sample_date": x["sample_date"].isoformat(),
                "target": x["target"]}
        res.append(dict(base, concentration_copies_per_l=round(x["conc"], 0), pmmov_copies_per_l=int(round(x["pmmov"], -5)),
                        result_status="preliminary", posted=x["posted"].isoformat()))
        if x["revised"] is not None:
            res.append(dict(base, concentration_copies_per_l=round(x["revised"], 0),
                            pmmov_copies_per_l=int(round(x["pmmov"], -5)), result_status="revised",
                            posted=x["revised_posted"].isoformat()))
    doc = {"programme": "%s respiratory wastewater surveillance" % C.ORG_SHORT,
           "exported": "2026-12-21T06:52:00-05:00",
           "laboratory_method": "RT-ddPCR on primary influent composites; PMMoV run on every sample",
           "results": res}
    open(os.path.join(out, F_WW), "w", encoding="utf-8").write(json.dumps(doc, indent=1, sort_keys=False) + "\n")
    return len(res)


# ---------------------------------------------------------------------------------------------------- outlook
def write_outlook(out, ol):
    wb = Workbook()
    ws = wb.active
    ws.title = "Outlook"
    head = ["region", "date", "expected_resp_admissions", "range_low", "range_high"]
    rows = [[C.REGIONS[x["region"]], x["date"], round(x["expected"], 1), round(x["low"], 1), round(x["high"], 1)]
            for x in ol]
    _sheet(ws, head, rows, [17, 12, 24, 11, 11], fmt={2: "0.0", 3: "0.0", 4: "0.0"})
    ws2 = wb.create_sheet("Notes")
    notes = [
        "Respiratory admissions outlook, issued Friday 18 December 2026 by the %s surveillance unit (%s)." % (
            C.ORG_SHORT, C.PEOPLE["surveillance"]),
        "Expected daily admissions with influenza, COVID-19 or RSV at the members in each region for the 14 days from "
        "Saturday 19 December, from each region's admissions reported to 17 December and its wastewater results posted "
        "to 17 December.",
        "The range is the outlook's 80 per cent range.",
        "Next issue: Friday 1 January 2027 is a holiday; the next outlook is issued Monday 4 January.",
    ]
    for i, t in enumerate(notes):
        ws2.cell(row=i + 1, column=1, value=t).font = BODY
    ws2.column_dimensions["A"].width = 120
    _save(wb, os.path.join(out, F_OUTLOOK), C.PEOPLE["surveillance"], C.PEOPLE["surveillance"],
          "2026-12-18T15:02:00Z", "2026-12-18T19:46:00Z")
    return len(rows)


# ---------------------------------------------------------------------------------------------------- survey
def write_survey(out, hs):
    r = W.rng(95)
    wb = Workbook()
    ws = wb.active
    ws.title = "RN workforce"
    head = ["quarter", "member_no", "hospital", "rn_fte_budgeted", "rn_fte_filled", "rn_vacancy_pct",
            "agency_rn_hours_pct"]
    rows = []
    for h in hs:
        bud = round(h["beds"] * 1.62 + r.normal(0, 4), 1)
        vac0 = 0.095 + r.normal(0, 0.02)
        ag0 = 0.052 + r.normal(0, 0.012)
        for k, q in enumerate(["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]):
            vac = max(0.02, vac0 - 0.0045 * k + r.normal(0, 0.006))
            ag = max(0.008, ag0 - 0.0021 * k + r.normal(0, 0.004))
            rows.append([q, h["member_no"], h["name"], bud, round(bud * (1 - vac), 1), round(100 * vac, 1),
                         round(100 * ag, 1)])
    _sheet(ws, head, rows, [9, 11, 30, 15, 13, 14, 18], fmt={3: "0.0", 4: "0.0", 5: "0.0", 6: "0.0"})
    ws.freeze_panes = "A2"
    _save(wb, os.path.join(out, F_SURVEY), "Shawn Whitaker", "Shawn Whitaker", "2025-04-21T13:10:00Z",
          "2026-10-26T18:31:00Z")
    return len(rows)


# ---------------------------------------------------------------------------------------------------- dictionary
DICTIONARY = [
    (F_LEGACY, "member_no", "The cooperative's member number."),
    (F_LEGACY, "report_date", "The date of the morning capacity report that carried the row."),
    (F_LEGACY, "census_midnight", "Inpatients in the member's staffed medical and surgical beds at the midnight census."),
    (F_LEGACY, "staffed_beds", "Medical and surgical beds the member could staff that night."),
    (F_LEGACY, "surge_status", "The member's surge plan level at the midnight census: blank, S1 (Level 1) or S2 (Level 2)."),
    (F_LEGACY, "resp_admits", "Admissions with influenza, COVID-19 or RSV in the 24 hours to the midnight census."),
    (F_LEGACY, "submission", "O for the report as first submitted, R for a resubmission that replaces it."),
    (F_DAILY, "facility_id", "The member's facility id in the capacity system."),
    (F_DAILY, "census_date", "The census night."),
    (F_DAILY, "inpatients_midnight", "Inpatients in the member's staffed medical and surgical beds at the midnight census."),
    (F_DAILY, "surge_level", "The member's surge plan level at the midnight census: 0, 1 or 2."),
    (F_DAILY, "resp_admissions", "Admissions with influenza, COVID-19 or RSV in the 24 hours to the midnight census."),
    (F_DAILY, "record_status", "provisional until the member's report is final, seven days after the census night."),
    (F_DECL, "declared_at", "Eastern Time of the declaration, at the 06:45 bed huddle or the 14:45 bed meeting."),
    (F_DECL, "level_from", "The surge plan level before the declaration."),
    (F_DECL, "level_to", "The surge plan level the declaration sets."),
    (F_DECL, "request_no", "The surge request sent to both agencies when a pool member's plan is activated (SR-); "
                           "before a member joined the pool, its own activation number in the capacity system (CAP-)."),
    (F_CRS, "line_id", "Crestfield billing line."),
    (F_CRS, "timesheet_no", "Crestfield timesheet the line is billed from."),
    (F_CRS, "client_site", "Crestfield's code for the member (see the members workbook)."),
    (F_CRS, "unit", "The unit the shift was worked on, as signed on the timesheet."),
    (F_CRS, "shift_start_utc", "The line's start time, UTC."),
    (F_CRS, "shift_end_utc", "The line's end time, UTC."),
    (F_CRS, "hours", "Hours billed on the line."),
    (F_CRS, "booking_type", "SURGE for a shift booked against a surge request, STAFF otherwise."),
    (F_CRS, "bill_to", "TRHC POOL or FACILITY."),
    (F_CRS, "request_ref", "The surge request the shift was booked against."),
    (F_ISN25, "Facility", "Inland Seas' name for the member (see the members workbook)."),
    (F_ISN25, "Unit", "The unit the shift was worked on, as signed on the timesheet."),
    (F_ISN25, "Payroll date", "The date Inland Seas pays the shift under: the day the shift ends."),
    (F_ISN25, "Shift", "D for 07:00 to 19:00, N for 19:00 to 07:00."),
    (F_ISN25, "Booking", "Surge for a shift booked against a surge request, Staffing otherwise."),
    (F_ISN25, "Bill to", "TRHC Pool or Facility."),
    (F_ISN26, "Facility", "Inland Seas' name for the member (see the members workbook)."),
    (F_ISN26, "Unit", "The unit the shift was worked on, as signed on the timesheet."),
    (F_ISN26, "Payroll date", "The date Inland Seas pays the shift under: the day the shift ends."),
    (F_ISN26, "Shift", "D for 07:00 to 19:00, N for 19:00 to 07:00."),
    (F_ISN26, "Booking", "Surge for a shift booked against a surge request, Staffing otherwise."),
    (F_ISN26, "Bill to", "TRHC Pool or Facility."),
    (F_MEMBERS, "member_no", "The cooperative's member number (the legacy capacity system's key)."),
    (F_MEMBERS, "facility_id", "The member's facility id in the capacity system from 1 July 2024."),
    (F_MEMBERS, "staffed_med_surg_beds", "Medical and surgical beds the member can staff, as at 2 November 2026."),
    (F_MEMBERS, "surge_unit", "The unit the member's surge plan opens."),
    (F_MEMBERS, "pool_member_from", "First day of the member's first pool season. The eight northern members bought "
                                    "agency nurses through their own regional contract until it ended on 31 October "
                                    "2026, and joined the pool on 1 November 2026; all eight have reported to the "
                                    "capacity system since July 2021."),
    (F_MEMBERS, "crestfield_site_code", "Crestfield's client site code for the member."),
    (F_MEMBERS, "inland_seas_facility", "Inland Seas' facility name for the member."),
    (F_BLOCKS, "block_shifts", "The January block filed with the agencies, agency RN shifts."),
    (F_BLOCKS, "crestfield_shifts", "Crestfield's share of the block."),
    (F_BLOCKS, "inland_seas_shifts", "Inland Seas' share of the block."),
    (F_BLOCKS, "filed_on", "The date the block was filed with the agencies."),
]


FORMATS = {
    "date": ("report_date", "census_date", "Payroll date", "pool_member_from", "filed_on"),
    "date and time": ("declared_at", "shift_start_utc", "shift_end_utc"),
    "whole number": ("census_midnight", "staffed_beds", "resp_admits", "inpatients_midnight", "surge_level",
                     "resp_admissions", "level_from", "level_to", "staffed_med_surg_beds", "block_shifts",
                     "crestfield_shifts", "inland_seas_shifts"),
    "number, 2 decimals": ("hours",),
}


def field_format(field):
    for k, v in FORMATS.items():
        if field in v:
            return k
    return "text"


def write_dictionary(out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Field definitions"
    ws.cell(row=1, column=1, value="TRHC pool office: fields in the files pulled for the 2026-27 January block").font = BOLD
    _sheet(ws, ["file", "field", "format", "definition"], [[f, fl, field_format(fl), d] for f, fl, d in DICTIONARY],
           [44, 22, 16, 100], start_row=3)
    ws.freeze_panes = "A4"
    _save(wb, os.path.join(out, F_DICT), C.PEOPLE["pool_manager"], C.PEOPLE["pool_manager"], "2022-01-10T14:00:00Z",
          "2026-12-21T13:20:00Z")
    return len(DICTIONARY)


# ---------------------------------------------------------------------------------------------------- manifest
MANIFEST = [
    (F_LEGACY, "TRHC capacity system (legacy, retired 30 June 2024)", "census nights 1 July 2021 to 30 June 2024, each row dated by the next morning's report", "archive export"),
    (F_DAILY, "TRHC capacity system", "census nights 1 July 2024 to 20 December 2026", "pulled 21 Dec 2026 06:40 ET"),
    (F_DECL, "TRHC capacity system, surge declarations", "1 July 2021 to 20 December 2026", "pulled 21 Dec 2026 06:41 ET; legacy declarations migrated with the system"),
    (F_MEMBERS, "TRHC pool office", "members and keys for the 2026-27 season", "as at 2 Nov 2026"),
    (DOC.F_AGREEMENT, "TRHC pool office", "2026-27 season", "approved 24 Sep 2026"),
    (DOC.F_REGISTER, "TRHC pool office", "2026-27 season", "issued 2 Nov 2026"),
    (F_BLOCKS, "TRHC pool office", "January blocks filed 2021 to 2025", "the 2026-27 row is filed on 22 Dec 2026"),
    (F_CRS, "Crestfield Medical Staffing member shift report", "shifts starting 1 Nov 2025 to 31 Mar 2026 and 1 Nov 2026 to the day shift of 20 Dec 2026", "received 21 Dec 2026"),
    (F_ISN25, "Inland Seas Nursing member shift report", "payroll weeks 27 Oct 2025 to 5 Apr 2026", "received weekly"),
    (F_ISN26, "Inland Seas Nursing member shift report", "payroll weeks 26 Oct to 20 Dec 2026", "received weekly; week of 14 Dec received 21 Dec"),
    (F_WW, "TRHC surveillance unit", "samples 6 Sep 2021 to 17 Dec 2026", "exported 21 Dec 2026"),
    (F_OUTLOOK, "TRHC surveillance unit", "19 Dec 2026 to 1 Jan 2027", "issued 18 Dec 2026"),
    (F_SURVEY, "TRHC workforce survey", "2025 Q1 to 2026 Q3", "members' quarterly returns"),
    (DOC.F_RATES, "TRHC finance", "2026-27 season", "issued 1 Oct 2026"),
    (F_DICT, "TRHC pool office", "field definitions", "updated 21 Dec 2026"),
]


def write_manifest(out):
    return _csv(os.path.join(out, F_MANIFEST), ["file", "source", "covers", "note"], [list(x) for x in MANIFEST])


# ---------------------------------------------------------------------------------------------------- the pack
def build_pack(out):
    os.makedirs(out, exist_ok=True)
    hs, wp, truth = W.simulate()
    decl = W.declarations(hs, truth)
    shifts = W.agency_shifts(hs, truth, decl)
    n = {}
    h, rows = R.legacy_capacity(hs, truth)
    n[F_LEGACY] = _csv(os.path.join(out, F_LEGACY), h, rows)
    h, rows = R.new_capacity(hs, truth)
    n[F_DAILY] = _csv(os.path.join(out, F_DAILY), h, rows)
    h, rows = R.declaration_rows(hs, decl)
    n[F_DECL] = _csv(os.path.join(out, F_DECL), h, rows)
    h, rows = R.crestfield_lines(hs, shifts)
    n[F_CRS] = _csv(os.path.join(out, F_CRS), h, rows)
    n[F_MEMBERS] = write_members(out, hs)
    n[F_BLOCKS] = write_blocks(out, hs, truth)
    n[F_ISN25] = write_inland_seas(out, hs, shifts, decl, D(2025, 10, 27), D(2026, 4, 5), F_ISN25, True,
                                   "2025-11-04T13:30:00Z", "2026-04-07T14:15:00Z")
    n[F_ISN26] = write_inland_seas(out, hs, shifts, decl, D(2026, 10, 26), C.CENSUS_END, F_ISN26, False,
                                   "2026-11-03T13:30:00Z", "2026-12-21T14:05:00Z")
    n[F_WW] = write_wastewater(out, W.wastewater(hs, wp))
    n[F_OUTLOOK] = write_outlook(out, W.outlook(hs, wp, truth))
    n[F_SURVEY] = write_survey(out, hs)
    DOC.write_agreement(out, hs)
    DOC.write_register(out, hs)
    DOC.write_rates(out)
    n[F_DICT] = write_dictionary(out)
    n[F_MANIFEST] = write_manifest(out)
    return n


if __name__ == "__main__":
    import sys
    o = sys.argv[1] if len(sys.argv) > 1 else C.TARGET
    nn = build_pack(o)
    for f in sorted(os.listdir(o)):
        print("  %-52s %10d bytes %s" % (f, os.path.getsize(os.path.join(o, f)), ("%d rows" % nn[f]) if f in nn else ""))
