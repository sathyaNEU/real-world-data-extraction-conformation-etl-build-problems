"""The pack's documents: the Water Order Procedure and its tables, the growers' 2027 water requests, the meter shop's
log, the canal structures workbook, the 2026 operations log, the data dictionary, the working-files note and the
Authority's 2027 allocation notice."""
from __future__ import annotations

import datetime as dt

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402
import records as R  # noqa: E402
import world as WD   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("Carlito-Italic", "crosextra/Carlito-Italic.ttf"),
               ("LiberationSerif", "liberation/LiberationSerif-Regular.ttf"),
               ("LiberationSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
SANS, SANS_B, SANS_I = "Carlito", "Carlito-Bold", "Carlito-Italic"
SERIF, SERIF_B = "LiberationSerif", "LiberationSerif-Bold"
INK = colors.HexColor("#1f2421")
GREY = colors.HexColor("#5b625d")
GREEN = colors.HexColor("#2f5d3a")
RULE = colors.HexColor("#9ea79f")

BODY = ParagraphStyle("body", fontName=SERIF, fontSize=10.4, leading=13.6, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=28, firstLineIndent=-28)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=15, leading=19, textColor=GREEN, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName=SANS, fontSize=10.2, leading=13.2, textColor=GREY, spaceAfter=8)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=11.2, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
NOTE = ParagraphStyle("note", fontName=SANS_I, fontSize=8.8, leading=11.2, textColor=GREY, spaceBefore=4)
LTR = ParagraphStyle("ltr", fontName=SERIF, fontSize=10.6, leading=14.2, textColor=INK, spaceAfter=7)


def _footer(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(0.85 * inch, 0.55 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.85 * inch, 0.55 * inch, "%s  |  Page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                             topMargin=0.8 * inch, bottomMargin=0.9 * inch, title=title, author=author, subject="",
                             creator="", producer="")


# ---------------------------------------------------------------------------------------------------- the procedure

def write_wop(path):
    s = [Paragraph(K.DISTRICT, H1S), Paragraph("Water Order Procedure", H1),
         Paragraph("Adopted by the Board of Directors, Resolution 2019-07, 16 April 2019; revised by Resolution 2025-18, "
                   "9 December 2025. The tables are adopted each December for the coming season's order and are "
                   "issued with this procedure. Administered by the Water Resources Manager.", H1S)]

    def sec(title, clauses):
        s.append(Paragraph(title, H2))
        for no, text in clauses:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (no, text), CLAUSE))

    sec("1 Purpose", [
        ("1.1", "The District takes its surface supply from the Tolan Valley Canal under its water service contract with "
                "the Tolan Valley Water Authority, for a contract quantity of 241,000 acre-feet a year. Each year the District orders from the Authority the water it will take "
                "at its headgate in the coming irrigation season. This procedure sets how the order is calculated and how "
                "it is scheduled by month.")])
    sec("2 The season and the order", [
        ("2.1", "The irrigation season runs from 1 February to 31 October. The main canal and the laterals are dry from "
                "1 November to 31 January for maintenance."),
        ("2.2", "The order for a season is due at the Authority by 1 February of that year."),
        ("2.3", "The order is the smallest whole number of thousands of acre-feet that would have covered the season's "
                "headgate requirement in at least 24 of the thirty most recent complete weather years (for the 2027 order, "
                "1997 to 2026)."),
        ("2.4", "A weather year's headgate requirement is the water the District's headgate would take from 1 February "
                "to 31 October of the coming season if that weather year's weather from 1 February to 31 October fell "
                "on the coming season (a replay of that weather year, its 29 February included in a leap year): every "
                "field on the coming season's water requests is run day by day through the crop water model of Section 3, "
                "from its root zone as it stands at the end of 31 January, under that year's reference "
                "evapotranspiration and rainfall, and the fields' deliveries are carried to the headgate with the "
                "loss allowances of Section 4.")])
    sec("3 The crop water model", [
        ("3.1", "The model keeps a daily balance for each field of the water in its root zone, as the depletion below "
                "field capacity in inches. A day's depletion is the previous day's depletion plus the crop's "
                "evapotranspiration for the day less the day's rainfall. It is never less than zero, rain beyond field "
                "capacity draining below the root zone, and never more than the root zone's total available water."),
        ("3.2", "A crop's evapotranspiration for a day is the reference evapotranspiration the District's weather record "
                "reports for the day times the crop coefficient for the crop and the month (Table 1)."),
        ("3.3", "A root zone's total available water is the available water capacity of the field's soil unit (Table 3) "
                "times the rooting depth: the crop's root depth (Table 2) or the soil unit's depth limit (Table 3), "
                "whichever is less. Its allowable depletion is the crop's allowable depletion fraction (Table 2) times "
                "its total available water."),
        ("3.4", "In a replay, a field is irrigated on any day at whose end its depletion has reached or passed its "
                "allowable depletion, and the irrigation returns its root zone to field capacity: the field ends that "
                "day at zero depletion."),
        ("3.5", "The water a replay delivers to a field on the day of an irrigation is the depletion it replaces divided "
                "by the application efficiency of the field's irrigation method (Table 4), over the field's acres.")])
    sec("4 Losses", [
        ("4.1", "The water put into a lateral is the water its fields receive divided by one less the lateral's loss "
                "allowance (Table 5). The headgate requirement is the water put into the nine laterals divided by one "
                "less the main canal's loss allowance (Table 5)."),
        ("4.2", "The Board sets the allowances each December from the District's conveyance studies.")])
    sec("5 The monthly schedule", [
        ("5.1", "The order is scheduled by month. A month's share is that month's headgate requirement summed over the "
                "thirty replays, over the thirty replays' total. Each month's amount is the order times its share, "
                "rounded to the nearest 100 acre-feet; October takes the difference, so that the months add to the "
                "order."),
        ("5.2", "During the season the District may ask the Authority to move water between months. The order is not "
                "revised after 1 February.")])
    sec("6 Records", [
        ("6.1", "The District's weather record is station 39 of the state agricultural weather network (Kestrel Bend "
                "South) up to 30 April 2014 and the District's station at the Kestrel Bend yard from 1 May 2014. A day "
                "the yard station did not record takes station 39's values for that day."),
        ("6.2", "The fields, their turnouts, laterals and soil units are as the District's field register stands when "
                "the order is calculated. Each field's crop, irrigation method and acres are those on its water request "
                "for the coming season, in the latest version the District accepted. A field with no accepted request "
                "is not run."),
        ("6.3", "Growers file water requests for the coming season from mid-November to 15 January.")])
    sec("7 Submission", [
        ("7.1", "The Water Resources Manager submits the order and its monthly schedule to the Authority with the "
                "General Manager's approval, and files the working papers with the Board's next agenda.")])
    s.append(Spacer(1, 6))
    s.append(Paragraph("Tables 1 to 5: %s (adopted 9 December 2025 for the 2027 order)." % K.WOP_TABLES, NOTE))
    doc = _doc(path, "Water Order Procedure", K.PEOPLE["gm"])
    foot = _footer("Kestrel Bend Irrigation District  |  Water Order Procedure (Res. 2019-07, rev. Res. 2025-18)",
                   "WOP")
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


def _title_rows(ws, title, sub, note=None):
    ws.append([title])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append([sub])
    ws["A2"].font = Font(name="Calibri", italic=True, size=10, color="595959")
    if note:
        ws.append([note])
        ws.cell(row=ws.max_row, column=1).font = Font(name="Calibri", size=9, color="595959")
    ws.append([])


def _head(ws, cols, widths=None):
    ws.append(cols)
    row = ws.max_row
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name="Calibri", bold=True)
        cell.fill = PatternFill("solid", fgColor="D9E1D9")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return row


def write_wop_tables(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "T1 Crop coefficients"
    _title_rows(ws, "Table 1. Crop coefficients by month", "Water Order Procedure, tables for the 2027 order. Adopted "
                "9 December 2025 (Resolution 2025-18).", "Coefficient on the day's reference evapotranspiration, constant "
                "through each calendar month.")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    _head(ws, ["Code", "Crop"] + months, [7, 22] + [6.5] * 12)
    for c in K.CROPS:
        ws.append([c, K.CROP_NAME[c]] + K.KC[c])
    ws2 = wb.create_sheet("T2 Crops")
    _title_rows(ws2, "Table 2. Root depth and allowable depletion", "Water Order Procedure, tables for the 2027 order.")
    _head(ws2, ["Code", "Crop", "Root depth (ft)", "Allowable depletion fraction"], [7, 22, 15, 26])
    for c in K.CROPS:
        ws2.append([c, K.CROP_NAME[c], K.ROOT_FT[c], K.MAD[c]])
    ws3 = wb.create_sheet("T3 Soil units")
    _title_rows(ws3, "Table 3. Soil units", "Water Order Procedure, tables for the 2027 order. Map units of the county "
                "soil survey as they occur in the District.", "Depth limit: depth to a duripan that roots do not pass; "
                "none where roots are not limited above 6 ft.")
    _head(ws3, ["Map unit", "Name", "Available water capacity (in/ft)", "Depth limit (ft)"], [9, 46, 18, 15])
    for k, (name, awc, lim) in K.SOILS.items():
        ws3.append([int(k), name, awc, lim if lim is not None else "none"])
    ws4 = wb.create_sheet("T4 Application efficiency")
    _title_rows(ws4, "Table 4. Application efficiency", "Water Order Procedure, tables for the 2027 order.",
                "Design application efficiency of each irrigation method, as WOP 3.5 uses it.")
    _head(ws4, ["Irrigation method", "Application efficiency"], [22, 22])
    for m in K.METHODS:
        ws4.append([m, K.EA[m]])
    ws5 = wb.create_sheet("T5 Loss allowances")
    _title_rows(ws5, "Table 5. Loss allowances", "Water Order Procedure, tables for the 2027 order.",
                "Per cent of the water put into the lateral (main canal: of the water taken at the headgate).")
    _head(ws5, ["Conveyance", "Loss allowance (%)"], [22, 18])
    for l in K.LATERALS:
        ws5.append([K.LATERAL_NAME[l], round(K.LOSS[l] * 100, 1)])
    ws5.append(["Main canal", round(K.MAIN_LOSS * 100, 1)])
    for w in (ws, ws2, ws3, ws4, ws5):
        w.freeze_panes = None
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- requests

def write_requests(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Requests"
    _title_rows(ws, "Kestrel Bend Irrigation District: 2027 water requests",
                "Requests received 16 November 2026 to 15 January 2027; exported 1 February 2027 from the request log.",
                "One row per request version. Crop codes and irrigation methods as in the Water Order Procedure tables.")
    cols = ["Request no.", "Version", "Status", "Received", "Grower account", "Ranch", "Field", "Turnout", "Crop code",
            "Crop", "Irrigation method", "Acres", "Remarks"]
    hr = _head(ws, cols, [12, 8, 11, 11, 12, 22, 9, 9, 9, 18, 16, 8, 20])
    for x in sorted(W.requests, key=lambda x: (x["no"], x["version"])):
        ws.append([x["no"], x["version"], x["status"], x["received"], x["acct"], x["ranch"], x["field"], x["turnout"],
                   x["crop"], K.CROP_NAME[x["crop"]], x["method"], round(x["acres"], 2), x["remarks"] or None])
        ws.cell(row=ws.max_row, column=4).number_format = "yyyy-mm-dd"
        ws.cell(row=ws.max_row, column=12).number_format = "0.00"
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    ws.auto_filter.ref = "A%d:M%d" % (hr, ws.max_row)
    ws2 = wb.create_sheet("Crop codes")
    ws2.append(["Code", "Crop"])
    for c in K.CROPS:
        ws2.append([c, K.CROP_NAME[c]])
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- meter shop log

def write_shop_log(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Work orders 2026"
    _title_rows(ws, "Meter shop work orders, 2026 season",
                "Kestrel Bend Irrigation District, Water Master's office. Registers as the shop read them on site.")
    hr = _head(ws, ["WO no.", "Date", "Time", "Turnout", "Work", "Meter out", "Reg. out", "Meter in", "Reg. in",
                    "Reason", "Unit"], [9, 11, 7, 9, 26, 11, 11, 11, 11, 24, 9])
    rows = []
    for c in W.changes:
        rows.append((c["when"], R.tid_gis(c["turnout"]), "Meter changed", c["removed_serial"], c["removal"],
                     c["installed_serial"], c["installation"], c["reason"], c["unit"]))
    for o in W.shop_other:
        rows.append((o["when"], R.tid_gis(o["turnout"]), o["work"], None, None, None, None, o["reason"], None))
    rows.sort(key=lambda x: (x[0], x[1]))
    for k, x in enumerate(rows):
        ws.append(["26-%03d" % (k + 14), x[0].date(), x[0].strftime("%H:%M")] + list(x[1:]))
        ws.cell(row=ws.max_row, column=2).number_format = "yyyy-mm-dd"
        ws.cell(row=ws.max_row, column=7).number_format = "0.00"
        ws.cell(row=ws.max_row, column=9).number_format = "0.00"
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    ws2 = wb.create_sheet("Meter inventory")
    _title_rows(ws2, "Turnout meters in service at 1 February 2026 and installed since",
                "Register units and the register's capacity (the reading after the largest value is zero).")
    _head(ws2, ["Meter", "Turnout", "Type", "Register units", "Register capacity", "Installed", "Removed"],
          [12, 9, 22, 16, 18, 11, 11])
    for m in sorted(W.meters, key=lambda m: (m["turnout"], m["installed"])):
        typ = "Propeller, mechanical register" if m["kind"] == "P" else "Magnetic flowmeter"
        units = "acre-feet" if m["units"] == "AF" else "hundred cubic feet"
        cap = "10,000.00" if m["units"] == "AF" else "10,000,000"
        ws2.append([m["serial"], R.tid_gis(m["turnout"]), typ, units, cap, m["installed"], m["removed"]])
        ws2.cell(row=ws2.max_row, column=6).number_format = "yyyy-mm-dd"
        ws2.cell(row=ws2.max_row, column=7).number_format = "yyyy-mm-dd"
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- structures

def write_structures(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tail weirs"
    _title_rows(ws, "Lateral tail weirs", "Kestrel Bend Irrigation District, District Engineer's structures inventory "
                "(revised March 2025).", "Sharp-crested rectangular weirs, free discharge: Q (cfs) = C x L x H^1.5, "
                "H the head over the crest in feet.")
    _head(ws, ["Lateral", "Weir", "Crest length L (ft)", "Crest gauge reading (ft)", "Coefficient C",
               "Spills to"], [11, 22, 17, 21, 13, 24])
    drains = {"L1": "Cottonwood Drain", "L2": "Cottonwood Drain", "L3": "Mill Slough", "L4": "Mill Slough",
              "L5": "South Drain", "L6": "South Drain", "L7": "Badger Drain", "L8": "Badger Drain", "L9": "Heron Slough"}
    for l in K.LATERALS:
        L, crest = WD.WEIR[l]
        ws.append([K.LATERAL_NAME[l], "%s tail weir" % K.LATERAL_NAME[l], L, crest, WD.WEIR_C, drains[l]])
    ws2 = wb.create_sheet("Lateral headings")
    _title_rows(ws2, "Lateral heading structures", "Each heading's flume logs to the SCADA system; daily volumes are "
                "the logger's totals.")
    _head(ws2, ["Lateral", "Heading structure", "Throat width (ft)", "Logger since", "Length (mi)"], [11, 18, 16, 13, 12])
    widths = {"L1": 3.0, "L2": 4.0, "L3": 3.0, "L4": 5.0, "L5": 4.0, "L6": 4.0, "L7": 3.0, "L8": 3.0, "L9": 4.0}
    lengths = {"L1": 6.4, "L2": 8.1, "L3": 4.2, "L4": 11.3, "L5": 7.6, "L6": 8.8, "L7": 6.0, "L8": 6.9, "L9": 9.7}
    for l in K.LATERALS:
        ws2.append([K.LATERAL_NAME[l], R.HEAD_STRUCT[l], widths[l], 2011 if l in ("L1", "L4") else 2013, lengths[l]])
    ws3 = wb.create_sheet("Main canal")
    _title_rows(ws3, "Main canal", "Headgate on the Tolan Valley Canal at milepost 41.2.")
    _head(ws3, ["Structure", "Type", "Capacity (cfs)"], [26, 30, 15])
    for row in [("Headgate", "Radial gates (2) and Parshall flume", 820), ("Check 1 (Lateral 1 and 2 turnouts)",
                "Overshot gates", 790), ("Check 2 (Lateral 3 and 4)", "Overshot gates", 640),
                ("Check 3 (Lateral 5 and 6)", "Overshot gates", 470), ("Check 4 (Lateral 7, 8 and 9)", "Overshot gates", 300)]:
        ws3.append(list(row))
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- operations log

def ops_entries(W):
    """The Water Master's 2026 log: (date, time, initials, entry), each entry written when it happened. A figure quoted
    in an entry is read from the records (the yard's rain, the Water Master's heading estimates)."""
    rain = {d: W.yard_rep[d]["rain_in"] for d in W.yard_rep if dt.date(2026, 2, 1) <= d <= dt.date(2026, 4, 30)}
    storm = max(sorted(rain), key=lambda d: rain[d])
    D = dt.date
    e = [
        (D(2026, 1, 26), "07:20", "CR", "Main canal fill started at the headgate, 120 cfs."),
        (D(2026, 1, 26), "14:15", "CR", "Fill water at Check 2. Walked the main canal from the headgate to Check 2; no "
                                        "seepage at the Road 152 crossing."),
        (D(2026, 1, 27), "07:30", "CR", "Gopher holes packed on the Lateral 2 bank at station 41."),
        (D(2026, 1, 28), "16:05", "CR", "Laterals 1 to 4 filled."),
        (D(2026, 1, 29), "15:40", "CR", "Laterals 5 to 9 filled."),
        (D(2026, 1, 30), "16:30", "CR", "Opening reads taken on every turnout meter this week on the usual route days."),
        (D(2026, 2, 1), "06:00", "CR", "Deliveries open for the 2026 season."),
        (D(2026, 2, 3), "08:45", "CR", "Trash rack at the headgate cleaned."),
        (storm, "13:30", "CR", "Storm, %.2f in at the yard. Bank roads on Laterals 7 and 8 closed to trucks until they "
                               "dry." % rain[storm]),
        (storm + dt.timedelta(days=3), "08:10", "CR", "Bank roads on Laterals 7 and 8 open to trucks again."),
        (D(2026, 3, 9), "10:30", "DZ", "Check 2 overshot gate actuator replaced; no interruption to deliveries."),
        (D(2026, 3, 24), "09:00", "CR", "Aquatic weed treatment on Laterals 2 and 3 under the District's permit."),
        (D(2026, 4, 2), "11:20", "CR", "Gopher damage on the Lateral 8 bank near turnout 08-019 repaired."),
        (D(2026, 5, 20), "16:30", "CR", "Lateral 4 turnout 04-031 gate stem broken; repaired same day."),
        (D(2026, 5, 26), "07:15", "CR", "Wind overnight; trash racks at Checks 3 and 4 cleared."),
        (D(2026, 6, 13), "06:30", "CR", "Lateral 5 west spur shut off at the spur head gate for the connector tie-in."),
        (D(2026, 6, 15), "16:20", "CR", "Lateral 5 to 6 connector in service. Turnouts 05-021 to 05-034 on the west spur "
                                        "now fed from Lateral 6 through the connector; the spur head gate on Lateral 5 "
                                        "closed and locked. Meters on the spur read today."),
        (D(2026, 6, 24), "07:00", "CR", "Safety tailgate meeting with the ditch riders; canal rescue gear checked."),
        (D(2026, 7, 14), "11:05", "CR", "Small bank slough on Lateral 3 at station 22 repaired; deliveries kept on."),
        (D(2026, 9, 2), "14:00", "CR", "Almond harvest under way; orders falling on Laterals 1, 4 and 9."),
        (D(2026, 9, 22), "10:15", "CR", "Bank mowing on Laterals 5 and 6 done."),
        (D(2026, 11, 1), "00:10", "CR", "Deliveries closed for the season at midnight. Headgate closed."),
        (D(2026, 11, 6), "16:35", "CR", "Closing reads taken on every turnout meter this week on the usual route days."),
        (D(2026, 11, 9), "08:00", "TG", "Winter maintenance: Lateral 7 lining repairs (stations 112 to 140) and Check "
                                        "3 gate seals."),
        (D(2026, 11, 30), "16:00", "CR", "Meter book closed for 2026."),
        (D(2026, 12, 4), "15:20", "TG", "Lateral 7 lining repairs complete."),
        (D(2026, 12, 14), "13:00", "TG", "Lateral 4 culvert at Road 156 replaced."),
        (D(2027, 1, 11), "15:45", "CR", "Weed control on the main canal banks complete."),
        (D(2027, 1, 20), "11:30", "TG", "Check 3 gate seals replaced and the gates worked through their travel."),
        (D(2027, 1, 25), "09:10", "CR", "Main canal fill for the 2027 season scheduled from 28 January."),
    ]
    # each heading logger's outage: logged when it stopped reporting, and the Water Master's daily estimates from the
    # heading gate opening and the check level logged when it came back, each entry in its writer's own words
    def est(lat, style):
        s0, n = WD.OUTAGES[lat]
        ds = [s0 + dt.timedelta(days=k) for k in range(n)]
        v = [W.heading_estimates[(lat, d)] for d in ds]
        if style == "dmy":
            return ", ".join("%d %s %.1f" % (d.day, d.strftime("%B"), x) for d, x in zip(ds, v))
        if style == "dmy_short":
            return ", ".join("%d %s %.1f" % (d.day, d.strftime("%b"), x) for d, x in zip(ds, v))
        if style == "dmy_af":
            return ", ".join("%d %s %.1f af" % (d.day, d.strftime("%B"), x) for d, x in zip(ds, v))
        if style == "mdy":
            return ", ".join("%s %d %.1f" % (d.strftime("%b"), d.day, x) for d, x in zip(ds, v))
        if style == "slash":
            return ", ".join("%d/%d %.1f" % (d.month, d.day, x) for d, x in zip(ds, v))
        if style == "and":
            parts = ["%d %s %.1f" % (d.day, d.strftime("%B"), x) for d, x in zip(ds, v)]
            return ", ".join(parts[:-1]) + " and " + parts[-1]
        raise ValueError(style)
    O = {lat: WD.OUTAGES[lat][0] for lat in WD.OUTAGES}
    back = {lat: WD.OUTAGES[lat][0] + dt.timedelta(days=WD.OUTAGES[lat][1]) for lat in WD.OUTAGES}
    e += [
        (O["L9"], "08:42", "DZ", "L9 heading flume level sensor failed overnight; no logger total today. Water Master "
                                 "estimating Lateral 9 from the gate opening and Check 4."),
        (back["L9"], "11:45", "DZ", "New level sensor in at the Lateral 9 flume 1640 yesterday, logging again from "
                                    "0000. CR's estimates for L9 while it was out (af): %s." % est("L9", "dmy_short")),
        (O["L1"], "09:03", "DZ", "Lateral 1 heading logger dead, solar regulator. Water Master estimating the heading "
                                 "from the gate opening and the Check 1 level until it is back."),
        (back["L1"], "10:51", "CR", "Lateral 1 regulator replaced, logger reporting from midnight. Heading estimates, "
                                    "acre-feet: %s." % est("L1", "dmy")),
        (O["L4"], "07:38", "DZ", "Lat 4 flume logger lost power (battery flat). CR estimating from the gate position and "
                                 "Check 2."),
        (back["L4"], "08:23", "DZ", "Battery replaced at the Lat 4 heading late yesterday; totals again from 0000 today. "
                                    "Estimated heading for the outage: %s." % est("L4", "dmy_af")),
        (O["L7"], "09:15", "DZ", "Lateral 7 heading logger off again, regulator failed. Water Master estimating L7 from "
                                 "the gate and the Check 4 level."),
        (back["L7"], "08:31", "CR", "L7 regulator swapped yesterday afternoon; logger totals from midnight. Lateral 7 "
                                    "estimated, acre-feet: %s." % est("L7", "slash")),
        (O["L3"], "08:03", "DZ", "Lateral 3 heading level sensor reading zero since early morning. No total for L3; CR "
                                 "estimating from the gate opening and Check 2."),
        (back["L3"], "08:43", "DZ", "Lateral 3 level sensor replaced 1715 yesterday; logging from midnight. Estimates "
                                    "while it was down (af): %s." % est("L3", "dmy")),
        (O["L2"], "07:57", "DZ", "Logger card fault at the Lateral 2 flume, no total for today. Estimating L2 from the "
                                 "gate opening and Check 1."),
        (back["L2"], "09:15", "CR", "New card in the L2 heading logger yesterday evening; totals again from midnight. "
                                    "CR's L2 estimates, acre-feet: %s." % est("L2", "mdy")),
        (O["L6"], "09:19", "DZ", "Lateral 6 flume stilling well silted up and the level sensor stuck. L6 heading "
                                 "estimated from the gate opening and the Check 3 level until the well is cleaned."),
        (back["L6"], "10:32", "DZ", "Lat 6 stilling well cleaned out and the sensor checked against the staff gauge "
                                    "yesterday; logger totals from midnight. Water Master's estimates (af): %s."
                                    % est("L6", "dmy_short")),
        (O["L5"], "07:58", "DZ", "L5 heading logger card fault, no total. CR estimating from the gate and Check 3."),
        (back["L5"], "11:35", "CR", "Lateral 5 logger card replaced; totals from midnight. Heading estimates %s "
                                    "acre-feet." % est("L5", "and")),
        (O["L8"], "09:48", "DZ", "Lateral 8 heading logger stopped recording after a firmware fault. Estimating L8 from "
                                 "the gate opening and the Check 4 level."),
        (back["L8"], "09:11", "CR", "L8 logger reloaded by DZ yesterday evening, recording from midnight. Estimates for "
                                    "Lateral 8, acre-feet: %s." % est("L8", "dmy_short")),
    ]
    return sorted(e, key=lambda x: (x[0], x[1]))


def write_ops_log(path, W):
    import docx
    from docx.shared import Inches, Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    d.add_heading("Kestrel Bend Irrigation District: canal operations log, 2026 season", level=1)
    d.add_paragraph("Water Master's office. Entries as logged; times are local.")
    t = d.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    t.autofit = False
    widths = (Inches(0.95), Inches(0.55), Inches(4.55), Inches(0.45))
    for k, h in enumerate(("Date", "Time", "Entry", "By")):
        t.rows[0].cells[k].text = h
    for day, time, by, text in ops_entries(W):
        row = t.add_row().cells
        row[0].text = day.isoformat()
        row[1].text = time
        row[2].text = text
        row[3].text = by
    for r_ in t.rows:
        for k, w in enumerate(widths):
            r_.cells[k].width = w
    d.core_properties.author = K.PEOPLE["watermaster"]
    d.core_properties.title = "Canal operations log 2026"
    d.save(path)


# ---------------------------------------------------------------------------------------------------- soil moisture network

def write_stations(path, W):
    """The Water Conservation program's platform export: the network's sites and every station's daily readings."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sites"
    _title_rows(ws, "KBID soil moisture network: sites", "Water Conservation, irrigation scheduling program. Stations "
                "installed 2024 under the state's on-farm water conservation grant.")
    _head(ws, ["Station", "Grower block", "APN", "Crop", "Irrigation", "Installed", "Sensors (in)", "Profile to (in)",
               "Full point (in)", "Notes"], [10, 34, 12, 10, 16, 11, 26, 14, 14, 52])
    for x in W.stations:
        ws.append([x["station"], x["block"], x["apn"], K.CROP_NAME[x["crop"]], x["method"], x["installed"],
                   ", ".join(str(v) for v in x["sensors"]), x["depth_in"], x["full"], x["note"] or None])
        ws.cell(row=ws.max_row, column=6).number_format = "yyyy-mm-dd"
        ws.cell(row=ws.max_row, column=9).number_format = "0.00"
    ws2 = wb.create_sheet("Daily")
    ws2.append(["Station", "Reading (UTC)", "Profile water (in)"])
    for c in range(1, 4):
        ws2.cell(row=1, column=c).font = Font(name="Calibri", bold=True)
    for w_, col in zip((10, 22, 18), "ABC"):
        ws2.column_dimensions[col].width = w_
    for x in sorted(W.station_reads, key=lambda x: (x["station"], x["utc"])):
        ws2.append([x["station"], x["utc"].strftime("%Y-%m-%dT%H:%M:%SZ"), x["profile"]])
        ws2.cell(row=ws2.max_row, column=3).number_format = "0.00"
    ws2.freeze_panes = "A2"
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- dictionary

DICT = [
    (K.REQUESTS, "Request no.", "The request's number; a revised request keeps its number and takes the next version."),
    (K.REQUESTS, "Version", "1 for the first filing, 2 for a revision."),
    (K.REQUESTS, "Status", "Accepted: the version the District accepted. Superseded: replaced by a later version of the "
                           "same request. Withdrawn: withdrawn by the grower; no water requested."),
    (K.REQUESTS, "Field", "Field id in the field register."),
    (K.REQUESTS, "Turnout", "Turnout as numbered in the ordering system (lateral-number)."),
    (K.REQUESTS, "Acres", "Acres to be irrigated, as requested."),
    (K.REGISTER, "field_id", "Field id (since the March 2025 re-mapping)."),
    (K.REGISTER, "former_field_id", "The field's id before the March 2025 re-mapping; a parcel split in 2025 gave two "
                                    "fields the same former id."),
    (K.REGISTER, "turnout_id", "Turnout asset id in the GIS (T + lateral number + turnout number)."),
    (K.REGISTER, "lateral", "The lateral the turnout is on."),
    (K.REGISTER, "soil_unit", "Soil survey map unit covering most of the field."),
    (K.REGISTER, "gis_acres", "Field area measured in the GIS."),
    (K.REGISTER, "last_edit", "Date the record was last edited."),
    (K.ORDERS, "order_no", "Order number (season-sequence)."),
    (K.ORDERS, "field_id", "Field the set waters: the former field id on the 2023 and 2024 seasons' orders, the current "
                           "id from the 2025 season (the ordering system was re-keyed with the March 2025 re-mapping)."),
    (K.ORDERS, "ordered_cfs", "Flow ordered for the set, cubic feet per second; the rider sets the turnout to it."),
    (K.ORDERS, "set_start", "Start of the set (water on at the turnout), local time."),
    (K.ORDERS, "set_end", "End of the set (water off at the turnout), local time."),
    (K.ORDERS, "status", "Delivered: water ran for the set. Cancelled: cancelled before water ran; no water was "
                         "delivered."),
    (K.ST39, "ETo (mm), Precip (mm)", "Daily reference evapotranspiration and precipitation as published by the state "
                                      "agricultural weather network, millimetres (25.4 millimetres to the inch)."),
    (K.ST39, "qc", "Network quality flag for the value to its left: blank, passed; Y, moderate outlier (value kept)."),
    (K.YARD, "ETo_in, Rain_in", "Daily reference evapotranspiration and rainfall at the Kestrel Bend yard station, "
                                "inches. The logger computes ETo from the day's weather."),
    (K.YARD, "Flag", "M: the logger did not record the day and the values are blank. Days absent from the file were "
                     "not recorded either."),
    (K.METER_BOOK, "turnout", "Turnout as written in the riders' books (lateral-number)."),
    (K.METER_BOOK, "meter", "Serial of the meter read."),
    (K.METER_BOOK, "reading", "The meter's register at the read."),
    (K.METER_BOOK, "reg_units", "Register units: AF, acre-feet; CCF, hundred cubic feet."),
    (K.HEADINGS, "volume_af", "Water that passed the lateral's heading structure on the day, acre-feet (the heading "
                              "logger's daily total)."),
    (K.WEIRS, "gauge_ft", "Staff gauge at the tail weir, feet, read at read_time. A reading stands for its day and for "
                          "each following day until the weir's next reading."),
    (K.WEIRS, "remarks", "The rider's notes."),
    (K.STATIONS, "Station", "Soil moisture station (capacitance probe in an access tube in the tree or vine row, or "
                            "mid-field in pasture and alfalfa)."),
    (K.STATIONS, "APN", "Assessor's parcel number of the block the station is in, as the grower gave it at sign-up."),
    (K.STATIONS, "Profile to (in)", "Depth the station's profile water is summed to, inches."),
    (K.STATIONS, "Full point (in)", "The station's profile water at field capacity, set from its readings two days after "
                                    "the 2025-26 winter's last storm."),
    (K.STATIONS, "Reading (UTC)", "Time of the reading, UTC. The station logs once a day at midnight local time."),
    (K.STATIONS, "Profile water (in)", "Water held in the profile to the station's profile depth at the reading, inches."),
    (K.GROUNDWATER, "depth_to_water_ft", "Depth from the reference point to water, feet."),
    (K.CROP_REPORT, "irrigated_acres", "Acres irrigated in the 2026 season as reported in the District's crop survey."),
]


def write_dictionary(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fields"
    _title_rows(ws, "Data dictionary for the order working files", "Kestrel Bend Irrigation District, Water Resources.")
    _head(ws, ["File", "Field", "Definition"], [38, 26, 100])
    for f, c, d in DICT:
        ws.append([f, c, d])
        ws.cell(row=ws.max_row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- notice

def write_notice(path):
    s = [Paragraph("TOLAN VALLEY WATER AUTHORITY", ParagraphStyle("lh", fontName=SANS_B, fontSize=13, leading=16,
                                                                 textColor=GREEN)),
         Paragraph("Water Accounting and Scheduling", H1S),
         Paragraph("December 15, 2026", LTR),
         Paragraph("To: Tolan Valley Project contractors", LTR),
         Paragraph("<b>2027 initial allocation and water orders</b>", LTR),
         Paragraph("The Authority's initial allocation for the 2027 contract year is 100 percent of each contractor's "
                   "contract quantity, based on storage in the Project's reservoirs on December 1. The allocation will be "
                   "reviewed monthly from February with the snow survey.", LTR),
         Paragraph("Contractors' 2027 water orders, with a monthly schedule for February through October, are due at the "
                   "Authority's Water Accounting office by February 1, 2027. An order may not exceed the contractor's "
                   "allocated quantity. Monthly schedules may be changed during the season on two weeks' notice.", LTR),
         Paragraph("Ordered water is charged at the 2027 rates adopted by the Authority's board in November. Water taken "
                   "above a contractor's order in any month is charged at the overrun rate.", LTR),
         Paragraph("Questions on orders and schedules may be directed to Water Accounting.", LTR),
         Spacer(1, 10),
         Paragraph(K.PEOPLE["authority"], LTR),
         Paragraph("Water Accounting Manager", LTR)]
    doc = _doc(path, "2027 initial allocation and water orders", K.PEOPLE["authority"])
    doc.build(s)


def write_readme(path, files):
    lines = ["Kestrel Bend Irrigation District, Water Resources",
             "2027 order: working files, compiled 1 February 2027",
             "",
             "File, what it is, where it came from:",
             ""]
    for name, what, source in files:
        lines.append("%s" % name)
        lines.append("    %s. %s." % (what, source))
    lines.append("")
    lines.append("Station 39 data are published by the state agricultural weather network and used as published.")
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(lines) + "\n")
