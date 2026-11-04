"""Governing documents and context artefacts for task210: SRM-07, the January 2027 pick timetable, the station
normals and the operations dashboard. PDFs are written in reportlab's invariant mode with scrubbed metadata; the
workbook's properties are fixed and its zip re-cut with fixed entry times."""
import datetime as dt
import io
import os
import zipfile
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab import rl_config
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import world as W
import simulate as S

rl_config.invariant = 1
FIXED = dt.datetime(2026, 11, 2, 9, 0, 0)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=5)
    h = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
    t = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14, leading=17, spaceAfter=6)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    return body, h, t, small


def _pdf(path, story, title, created, modified):
    """Write the PDF, then set its own creation and modification stamps (the issuing office's, local time with the
    offset) in place of the invariant-mode date, and blank the writer's comment lines; both at equal byte length, so
    the cross-reference offsets stand."""
    import re
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                            bottomMargin=0.8 * inch, title=title, author="", subject="", creator="", producer="")
    doc.build(story)
    b = open(path, "rb").read()
    n0 = len(b)
    inv = b"D:20000101000000+00'00'"
    for key, stamp in ((b"/CreationDate (", created), (b"/ModDate (", modified)):
        s = stamp.encode()
        assert len(s) == len(inv) and b.count(key + inv) == 1
        b = b.replace(key + inv, key + s)
    b = re.sub(rb"(?m)^(%[^\n]*?)( ?ReportLab [^\n]*)$", lambda m: m.group(1) + b" " * len(m.group(2)), b)
    assert len(b) == n0 and b"ReportLab" not in b
    open(path, "wb").write(b)


def _tbl(rows, widths=None, fs=8.5):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", fs), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", fs),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def srm07(path):
    body, h, t, small = _styles()
    P = lambda s: Paragraph(s, body)
    st = [Paragraph("Ashcombe Regional Transit<br/>Safety Risk Management Procedure SRM-07: Seasonal Restricted Speed Orders (Streetcar)", t),
          Paragraph("Revision 4. Effective 1 October 2026. Procedure owner: Chief Safety Officer. Approved by the Accountable "
                    "Executive under the Agency Safety Plan, section 5 (Safety Risk Management).", small), Spacer(1, 6),
          Paragraph("1. Purpose", h),
          P("This procedure sets how the Rail Safety Office places Restricted Speed Orders (RSOs) on the streetcar for each service "
            "pick, as a seasonal hazard control under the Agency Safety Plan."),
          Paragraph("2. Scope", h),
          P("Every revenue track section of the Juniper Line and the Foundry Line, in each direction of travel, as listed in the current "
            "streetcar track survey."),
          Paragraph("3. Definitions", h),
          P("3.1 <b>Section.</b> The track between two consecutive stops, as listed in the track survey. The survey lists each "
            "section's coordinates in outbound order."),
          P("3.2 <b>Direction of travel.</b> Outbound runs from Mesa Park toward Union Yard on the Juniper Line and from Northfield "
            "toward Foundry Loop on the Foundry Line; inbound is the reverse."),
          P("3.3 <b>Pass.</b> One train's traverse of a section in one direction of travel, whether the train runs as one car or two."),
          P("3.4 <b>Firm brake.</b> A brake application the car's event data recorder flags with code FB (a deceleration of 1.3 m/s2 "
            "or more held for one second), recorded by the car whose cab is active. One FB event is one firm brake. The recorder's "
            "other codes are EB, an emergency brake application (the emergency loop opened), which on a two-car train each car's "
            "recorder records, and OS, an overspeed (3 mph or more over the posted limit)."),
          P("3.5 <b>Weekday peak.</b> The AM peak, 06:30 to 08:59, and the PM peak, 16:00 to 18:29, on a day the pick runs its "
            "weekday timetable, by the time the train enters the section, Mountain local time."),
          P("3.6 <b>Section-direction peak.</b> One section, in one direction of travel, in one weekday peak."),
          P("3.7 <b>Rate.</b> Firm brakes per 1,000 passes."),
          Paragraph("4. Assessment", h),
          P("4.1 Before each pick the Chief Safety Officer assesses every section-direction peak's expected rate for that pick: the rate "
            "its passes are expected to see at the pick's scheduled times on the pick's weekdays, in the weather normal for those weeks "
            "(the station normals in Appendix C)."),
          P("4.2 The assessment draws on the event data recorder record since the recorders were commissioned on 1 April 2026, the "
            "AVL section-pass log and the agency's other operating records."),
          Paragraph("5. Orders", h),
          P("5.1 RSOs are placed on the section-direction peaks with the highest expected rates, as many as the pick's running-time "
            "supplement carries. For the January 2027 pick (4 January to 26 February 2027) the supplement carries four."),
          P("5.2 An RSO limits trains to 10 mph through the section in that direction of travel during that peak, on every weekday of "
            "the pick."),
          Paragraph("6. Records", h),
          P("The assessment, the slot plan and the record extracts it used are kept for three years by the Rail Safety Office."),
          Paragraph("Appendix C. Station normals: Ashcombe Municipal Airport (ASH), 1991 to 2020, published separately with this procedure.", small)]
    _pdf(path, st, "SRM-07 Seasonal Restricted Speed Orders", "D:20260916101204-06'00'", "D:20260924163548-06'00'")


def pick(path):
    body, h, t, small = _styles()
    geo = S.geometry()
    runs = S.section_runs(geo, W.PICK_RUN_ADJ)
    st = [Paragraph("Ashcombe Regional Transit: Streetcar Service Pick, January 2027", t),
          Paragraph("Pick dates: Monday 4 January to Friday 26 February 2027. Scheduling Department, issued 2 November 2026.", small), Spacer(1, 6),
          Paragraph("Service pattern (both lines, both directions)", h),
          _tbl([["Day", "Span", "Headway"], ["Weekday", "06:00 to 06:30", "every 10 min"], ["Weekday", "06:30 to 19:00", "every 7.5 min"],
                ["Weekday", "19:00 to 24:00", "every 10 min"], ["Saturday", "06:00 to 24:00", "every 10 min"],
                ["Sunday and holidays", "07:00 to 23:00", "every 15 min"]], [1.7 * inch, 1.6 * inch, 1.4 * inch]),
          Spacer(1, 4),
          Paragraph("Trips leave each line's outer stops on the headway from the start of each span. Holidays in this pick (Sunday "
                    "timetable): Monday 18 January and Monday 15 February 2027. Blocks J01 and J02 run as two-car trains on "
                    "weekday trips leaving 06:30 to 09:29 and 15:30 to 18:44.", body),
          Paragraph("Scheduled running times (seconds, stop to stop, dwell included)", h)]
    rows = [["Line", "Section", "From", "To", "Outbound s", "Inbound s"]]
    for line in ("J", "F"):
        ro, ri = dict(runs[(line, "O")]), dict(runs[(line, "I")])
        for _, g in geo[geo["line"] == line].iterrows():
            rows.append([W.LINES[line][0], g["section"], g["from_stop"], g["to_stop"], f"{ro[g['section']]:.0f}", f"{ri[g['section']]:.0f}"])
    st.append(_tbl(rows, [1.1 * inch, 0.6 * inch, 1.3 * inch, 1.3 * inch, 0.9 * inch, 0.9 * inch]))
    _pdf(path, st, "January 2027 streetcar pick", "D:20261027140951-06'00'", "D:20261102081733-07'00'")


def normals(path):
    body, h, t, small = _styles()
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    temp = [30.1, 32.4, 39.7, 46.3, 55.8, 66.0, 71.6, 69.4, 61.7, 49.8, 38.4, 30.6]
    prcp = [0.32, 0.38, 1.02, 1.54, 2.21, 2.32, 2.89, 3.11, 1.36, 0.83, 0.47, 0.36]
    snow = [5.1, 5.8, 7.9, 5.4, 1.2, 0.0, 0.0, 0.0, 0.2, 3.1, 5.0, 5.5]
    rows = [["", *months], ["Mean temperature, F", *[f"{v:.1f}" for v in temp]],
            ["Precipitation, in", *[f"{v:.2f}" for v in prcp]], ["Snowfall, in", *[f"{v:.1f}" for v in snow]],
            ["Possible sunshine, %", *[str(W.SUN_NORM[i + 1]) for i in range(12)]]]
    st = [Paragraph("Ashcombe Municipal Airport (ASH): Climate Normals 1991 to 2020", t),
          Paragraph("Monthly normals. Possible sunshine is the share of the hours between sunrise and sunset with the sun not obscured.", small), Spacer(1, 6),
          _tbl(rows, [1.45 * inch] + [0.42 * inch] * 12, fs=7.5)]
    _pdf(path, st, "ASH climate normals 1991-2020", "D:20210504112617-06'00'", "D:20210611090258-06'00'")


WB_CREATED = dt.datetime(2026, 5, 1, 5, 52, 11)      # UTC: the first month-end download (23:52 on 30 April, MDT)
WB_MODIFIED = "2026-11-01T05:14:37Z"                  # the October download (23:14 on 31 October, MDT)


def dashboard(path, T, Rr, target):
    """The month-end downloads: each month's trips and section passes as the AVL system logged them (by service day)
    and the recorder system's FB, EB and OS counts (by the recorder's UTC month), April to October."""
    import openpyxl
    A = pd.read_parquet(os.path.join(target, "avl_section_passes_2026.parquet"),
                        columns=["service_date", "line", "trip_id", "section_id"])
    A["month"] = pd.to_datetime(A["service_date"]).dt.strftime("%Y-%m")
    A["linen"] = A["line"].astype(str).map({"JUN": "Juniper", "FDY": "Foundry"})
    E = Rr["edr"]
    E = E.assign(month=E["t_utc"].dt.strftime("%Y-%m"), line=E["car"].astype(int).map(lambda c: "Juniper" if c < 120 else "Foundry"))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Monthly KPIs"
    ws.append(["Rail Operations dashboard, streetcar, 2026 (figures as downloaded at each month end)"])
    ws.append([])
    ws.append(["Month", "Line", "Revenue trips (AVL)", "Section passes (AVL)", "FB events (EDR)", "FB per 1,000 passes",
               "EB events (EDR)", "OS events (EDR)"])
    for m in ["2026-%02d" % k for k in range(4, 11)]:
        for ln in ("Juniper", "Foundry"):
            p = A[(A["month"] == m) & (A["linen"] == ln)]
            e = E[(E["month"] == m) & (E["line"] == ln)]
            fb = int((e["code"] == "FB").sum())
            ws.append([m, ln, int(p[["service_date", "trip_id"]].drop_duplicates().shape[0]), int(len(p)), fb,
                       round(fb / max(len(p), 1) * 1000, 2), int((e["code"] == "EB").sum()), int((e["code"] == "OS").sum())])
    wb.properties.creator = ""
    wb.properties.lastModifiedBy = ""
    wb.properties.created = WB_CREATED
    wb.properties.modified = WB_CREATED
    bio = io.BytesIO()
    wb.save(bio)
    _recut_zip(bio.getvalue(), path)


def _recut_zip(data, path):
    """Re-cut the workbook with fixed entry times; openpyxl stamps the save time as the modified date, so the core
    properties are reset to the last download, and the extended properties name the spreadsheet application the
    office keeps the dashboard in, with that application's own version."""
    import re
    src = zipfile.ZipFile(io.BytesIO(data))
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for n in sorted(src.namelist()):
            body = src.read(n)
            if n == "docProps/core.xml":
                body = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + WB_MODIFIED.encode() + rb"\g<2>", body)
            if n == "docProps/app.xml":
                body = re.sub(rb"<Application>[^<]*</Application><AppVersion>[^<]*</AppVersion>",
                              b"<Application>Microsoft Excel</Application><AppVersion>16.0300</AppVersion>", body)
                assert b"penpyxl" not in body
            zi = zipfile.ZipInfo(n, date_time=(2026, 10, 31, 23, 14, 36))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, body)


def write_documents(target, files, T, Rr):
    srm07(os.path.join(target, files["srm"]))
    pick(os.path.join(target, files["pick"]))
    normals(os.path.join(target, files["normals"]))
    dashboard(os.path.join(target, files["dash"]), T, Rr, target)
