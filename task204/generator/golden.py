"""Golden deliverables: series_assessment_2026.xlsx and summer_series_deployment_memo.docx."""
import datetime as dt
import os

import docx
import openpyxl
from docx.shared import Pt
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import params as P
from pack_data import normalise_zip

THIN = Side(style="thin", color="A6A6A6")
HDR = PatternFill("solid", fgColor="DDE3EA")
BOLD = Font(name="Calibri", size=10, bold=True)
NORM = Font(name="Calibri", size=10)


def _team_label(t):
    if len(t["districts"]) > 1:
        return "Eastline group"
    st = t["stations"]
    if st == ["Cobb Street"]:
        return "Cobb Street station group"
    if st == ["Hollin"]:
        return "Hollin station group"
    return "District %s street robbery group" % t["districts"][0][1:]


def team_rows(res):
    rows = []
    for t in res["golden"]:
        rows.append({"label": _team_label(t), "districts": t["districts"], "n": t["n"], "stations": t["stations"]})
    order = {"Eastline group": 0, "Hollin station group": 1, "Cobb Street station group": 2}
    rows.sort(key=lambda r: (order.get(r["label"], 3), -r["n"]))
    return rows


def district_text(ds):
    nums = [d[1:] for d in ds]
    if len(nums) == 1:
        return "District %s" % nums[0]
    return "Districts %s and %s" % (", ".join(nums[:-1]), nums[-1])


def write_xlsx(path, res):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Series teams"
    ws["A1"] = "OPS-41 series assessment, summer deployment plan 2026"
    ws["A1"].font = Font(name="Calibri", size=12, bold=True)
    ws["A2"] = "Assessment date 4 May 2026. Review period 9 February to 3 May 2026. Crime Analysis Unit."
    ws["A2"].font = NORM
    ws.append([])
    ws.append(["Team", "Offender group", "Ground (patrol districts)", "Series offences in review period", "Where"])
    for c in ws[4]:
        c.font = BOLD
        c.fill = HDR
    for i, t in enumerate(team_rows(res), start=1):
        where = ", ".join(t["stations"]) + " stations" if t["stations"] else "street, late night"
        if t["label"] == "Eastline group":
            where = "platforms at %s (on the same trains)" % ", ".join(t["stations"])
        ws.append(["Team %d" % i, t["label"], ", ".join(d.replace("D", "") for d in t["districts"]), t["n"], where])
    n_teams = len(res["golden"])
    ws.append([])
    ws.append(["Series teams required", n_teams])
    ws.cell(ws.max_row, 1).font = BOLD
    covered = sorted({d for t in res["golden"] for d in t["districts"]}, key=lambda s: int(s[1:]))
    none = [d for d in ["D%d" % k for k in range(1, 11)] if d not in covered]
    ws.append(["Patrol districts with no series", ", ".join(d.replace("D", "") for d in none)])
    for col, w in zip("ABCDE", (10, 30, 24, 30, 52)):
        ws.column_dimensions[col].width = w

    ws2 = wb.create_sheet("2025 by district")
    ws2["A1"] = "Robbery and theft from the person with a phone taken, 10 February to 4 May 2025, 2026 patrol districts"
    ws2["A1"].font = BOLD
    ws2.append([])
    ws2.append(["Patrol district", "10 Feb - 9 Mar 2025", "10 Mar - 6 Apr 2025", "7 Apr - 4 May 2025", "Total"])
    for c in ws2[3]:
        c.font = BOLD
        c.fill = HDR
    for d in ["D%d" % k for k in range(1, 11)]:
        v = res["ask_a"][d]
        ws2.append([d.replace("D", "District "), v[0], v[1], v[2], sum(v)])
    ws2.append(["All districts"] + [sum(res["ask_a"][d][k] for d in res["ask_a"]) for k in range(3)]
               + [sum(sum(v) for v in res["ask_a"].values())])
    for c in ws2[ws2.max_row]:
        c.font = BOLD
    for col, w in zip("ABCDE", (18, 20, 20, 20, 10)):
        ws2.column_dimensions[col].width = w

    ws3 = wb.create_sheet("Eastline stations")
    ws3["A1"] = "Eastline stations, 9 February to 3 May 2026 (local time)"
    ws3["A1"].font = BOLD
    ws3.append([])
    ws3.append(["Station", "Fare-gate entries", "Scheduled Eastline departures (both directions)"])
    for c in ws3[3]:
        c.font = BOLD
        c.fill = HDR
    for s in ["Westgate", "Centre Square", "Union Yards", "Millbrook", "Fairgrounds", "Cobb Street", "Ashford Road",
              "Ridgeview", "Prairie Gate"]:
        ws3.append([s, res["ask_b"][s], res["ask_c"][s]])
    for r in ws3.iter_rows(min_row=4, max_row=ws3.max_row):
        r[1].number_format = "#,##0"
        r[2].number_format = "#,##0"
    ws3.append([])
    ws3.append(["Fairgrounds opened 29 March 2026."])
    for col, w in zip("ABC", (18, 18, 44)):
        ws3.column_dimensions[col].width = w
    wb.properties.creator = "Carvale Police Service - Crime Analysis Unit"
    wb.properties.lastModifiedBy = "J. Jackson"
    wb.properties.created = dt.datetime(2026, 5, 15, 16, 22, 0)
    wb.properties.modified = dt.datetime(2026, 5, 15, 16, 48, 0)
    wb.save(path)
    normalise_zip(path)


def write_memo(path, res):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    rows = team_rows(res)
    p = d.add_paragraph()
    p.add_run("Carvale Police Service, Crime Analysis Unit").bold = True
    d.add_paragraph("To: Deputy Chief (Operations) %s\nFrom: %s, Crime Analysis Unit\nDate: 15 May 2026\n"
                    "Subject: Summer deployment plan, OPS-41 series teams" % (P.PEOPLE["deputy_chief"], P.PEOPLE["cau_supervisor"]))
    p = d.add_paragraph()
    p.add_run("The plan needs %s series teams for 1 June to 27 September." % _word(len(rows))).bold = True
    for i, t in enumerate(rows, start=1):
        d.add_paragraph("Team %d, %s: %s, %d offences in the review period." % (i, t["label"], district_text(t["districts"]), t["n"]),
                        style="List Number")
    e = next(t for t in rows if t["label"] == "Eastline group")
    d.add_paragraph(
        "The station figures look like four separate local groups, one at each of %s. They are one group: on %d "
        "evenings two or three of these snatches fell on the departures of a single westbound train, so the same "
        "people rode the line and struck as the doors closed. Their team needs ground in %s."
        % (", ".join(e["stations"][:-1]) + " and " + e["stations"][-1], len(res["runs"]), district_text(e["districts"])))
    sim = max((len(v) for v in res["simultaneous"].values()), default=0)
    d.add_paragraph(
        "The Cobb Street group is a different group with the same method. None of its snatches sits on one of those "
        "trains, and on %s evenings it struck at Cobb Street within three minutes of the Eastline group striking at "
        "Union Yards, two stops and more than eight minutes apart by train." % _word(sim))
    covered = sorted({x for t in rows for x in t["districts"]}, key=lambda s: int(s[1:]))
    none = [x for x in ["D%d" % k for k in range(1, 11)] if x not in covered]
    d.add_paragraph("Districts %s have no series in the review period; their phone offences stay with district "
                    "investigators. The 2025 comparison for the Commission and the Eastline station figures for "
                    "Transit are in the workbook." % (", ".join(x[1:] for x in none[:-1]) + " and " + none[-1][1:]))
    cp = d.core_properties
    cp.author = "J. Jackson"
    cp.last_modified_by = "J. Jackson"
    cp.title = "Summer deployment plan, OPS-41 series teams"
    cp.created = dt.datetime(2026, 5, 15, 15, 40, 0)
    cp.modified = dt.datetime(2026, 5, 15, 16, 55, 0)
    cp.revision = 3
    d.save(path)
    normalise_zip(path)


def _word(n):
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}.get(n, str(n))


def write_golden(folder, res):
    os.makedirs(folder, exist_ok=True)
    write_xlsx(os.path.join(folder, "series_assessment_2026.xlsx"), res)
    write_memo(os.path.join(folder, "summer_series_deployment_memo.docx"), res)
    ts = dt.datetime(2026, 5, 15, 17, 0, 0).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (ts, ts))
