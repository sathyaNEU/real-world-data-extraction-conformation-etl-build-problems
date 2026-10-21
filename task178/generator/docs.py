"""task178 documents: the gauge's datum sheet, the city's sea-level guidance and the trestle design basis (PDFs), the
station log and the data dictionary (Excel). Their text is held here as data so checks.py can quote it and
verify.py can read it back."""
from __future__ import annotations

import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import letter                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as C          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2329")
GREY = colors.HexColor("#5a626b")
ACCENT = colors.HexColor("#1f4e6e")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_stamp(d, hh=10, mi=0):
    off = -4 if 3 < d.month < 11 or (d.month == 3 and d.day >= 9) or (d.month == 11 and d.day < 2) else -5
    return ("D:%04d%02d%02d%02d%02d00%+03d'00'" % (d.year, d.month, d.day, hh, mi, off)).encode()


STYLES = dict(
    org=ParagraphStyle("org", fontName="Carlito-Bold", fontSize=9.5, leading=12, textColor=ACCENT, spaceAfter=2),
    h1=ParagraphStyle("h1", fontName="LibSans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4),
    sub=ParagraphStyle("sub", fontName="Carlito", fontSize=9.2, leading=12, textColor=GREY, spaceAfter=10),
    h2=ParagraphStyle("h2", fontName="LibSans-Bold", fontSize=10.5, leading=13.5, textColor=ACCENT, spaceBefore=8,
                      spaceAfter=3),
    body=ParagraphStyle("body", fontName="Carlito", fontSize=10.6, leading=14, textColor=INK, spaceAfter=5),
    cell=ParagraphStyle("cell", fontName="Carlito", fontSize=9.2, leading=11.2, textColor=INK),
    small=ParagraphStyle("small", fontName="Carlito", fontSize=8.4, leading=10.5, textColor=GREY, spaceBefore=8))


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Carlito", 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 11 * mm, text)
        canvas.drawRightString(letter[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths, header=True):
    data = [[Paragraph(esc(str(c)), STYLES["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b9c2cc")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6edf3")))
    t.setStyle(TableStyle(st))
    return t


def _build(path, title, author, head, sub, blocks, foot, stamp):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    story = [Paragraph(esc(head), STYLES["org"]), Paragraph(esc(title), STYLES["h1"]), Paragraph(esc(sub), STYLES["sub"])]
    for b in blocks:
        kind = b[0]
        if kind == "h2":
            story.append(Paragraph(esc(b[1]), STYLES["h2"]))
        elif kind == "p":
            story.append(Paragraph(esc(b[1]), STYLES["body"]))
        elif kind == "small":
            story.append(Paragraph(esc(b[1]), STYLES["small"]))
        elif kind == "table":
            story.append(_table(b[1], b[2]))
            story.append(Spacer(1, 5))
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, stamp, stamp)


# ------------------------------------------------------------------------------------------- the datum sheet
DATUM_DATE = dt.date(2026, 6, 15)
DATUM_TITLE = "Tide Gauge PTG-01: Datum Sheet"


def datum_blocks(dat):
    """dat: datums in ft above MLLW"""
    stnd = C.STND_BELOW_MLLW
    rows = [["Datum", "ft above STND (1995)", "ft above MLLW"]]
    for k in ("MHHW", "MHW", "MSL", "MLW", "MLLW"):
        rows.append([k, "%.2f" % (dat[k] + stnd), "%.2f" % dat[k]])
    rows.append(["NAVD88", "%.2f" % (C.NAVD88_ABOVE_MLLW + stnd), "%.2f" % C.NAVD88_ABOVE_MLLW])
    lev = [["Date", "Run", "Sensor reference against BM PTG 3", "Action"],
           ["2013-05-21", "annual", "+0.01 ft", "none"], ["2014-05-13", "annual", "0.00 ft", "none"],
           ["2015-05-19", "annual", "-0.01 ft", "none"], ["2016-05-24", "annual", "+0.01 ft", "none"],
           ["2017-05-16", "annual", "0.00 ft", "none"], ["2018-03-12", "brought forward", "-0.08 ft", "sensor reset to reference"],
           ["2019-05-14", "annual", "+0.01 ft", "none"], ["2020-06-09", "annual (delayed)", "0.00 ft", "none"],
           ["2021-05-18", "annual", "-0.01 ft", "none"], ["2022-05-17", "annual", "+0.01 ft", "none"],
           ["2023-05-23", "annual", "0.00 ft", "none"], ["2024-05-21", "annual", "-0.01 ft", "none"],
           ["2025-05-20", "annual", "0.00 ft", "none"],
           ["2026-04-28", "after pier repair", "new mount", "station datum re-established (STND 2026)"]]
    bms = [["Bench mark", "Description", "ft above MLLW"],
           ["PTG 1", "disk in granite curb, Cutler Wharf head", "15.94"], ["PTG 3", "disk in gauge pier cap", "13.27"],
           ["PTG 4", "chiseled square, Town Landing steps", "18.62"], ["H 117", "regional survey disk, Ropewalk Rd", "21.05"]]
    return [
        ("h2", "Station"),
        ("p", "PTG-01 is the City of Port Tessaly's tide gauge on the gauge pier at the head of Cutler Wharf, installed "
              "in November 1994 and run by the Waterfront and Harbor Engineering division of the Department of Public "
              "Works. The primary sensor is in a stilling well on the pier: a float and encoder from 1994, an acoustic "
              "sensor from 14 August 2012 and a radar sensor on the new mount from 28 April 2026. Readings are logged "
              "every six minutes; the verified product carries one reading every 15 minutes."),
        ("h2", "Tidal datums"),
        ("p", "Datums are on the 1983-2001 National Tidal Datum Epoch, computed by comparison of simultaneous "
              "observations with the regional control station. Heights are in feet."),
        ("table", rows, [48 * mm, 50 * mm, 40 * mm]),
        ("h2", "Station datum"),
        ("p", "STND (1995) is 4.21 ft below MLLW. After the gauge pier repair the sensor was remounted and on 28 April "
              "2026 the station datum was re-established 0.12 ft above STND (1995); STND 2026 is 4.09 ft below MLLW."),
        ("h2", "Harbormaster tide board"),
        ("p", "The harbormaster's float tide board on the gauge pier reads in feet above its own zero, which is 3.00 ft "
              "below MLLW (levelled 2015-03-17, checked each spring since)."),
        ("h2", "Levelling"),
        ("table", lev, [24 * mm, 30 * mm, 52 * mm, 62 * mm]),
        ("h2", "Bench marks"),
        ("table", bms, [24 * mm, 92 * mm, 30 * mm]),
        ("small", "Revision 2026-06, 15 June 2026: station datum STND 2026 added; levelling of 28 April 2026 added. "
                  "Revision 2019-06: levelling table extended. Revision 2013-01: acoustic sensor."),
    ]


def write_datums(out, dat):
    _build(os.path.join(out, C.F_DATUMS), DATUM_TITLE, "Waterfront and Harbor Engineering",
           C.CITY + " | " + C.DEPT, "Port Tessaly tide gauge, Cutler Wharf. Revision 2026-06.", datum_blocks(dat),
           "PTG-01 datum sheet, revision 2026-06", pdf_stamp(DATUM_DATE, 14, 12))


# ------------------------------------------------------------------------------------ the sea-level guidance
SLR_DATE = dt.date(2026, 9, 3)
SLR_TITLE = "Sea Level and Coastal Flooding Guidance, 2026 Update"


def slr_blocks(annual, design, trend_ft):
    t1 = [["Year", "Annual mean sea level (ft MLLW)", "Year", "Annual mean sea level (ft MLLW)"]]
    ys = sorted(annual)
    half = (len(ys) + 1) // 2
    for i in range(half):
        a = ys[i]
        b = ys[i + half] if i + half < len(ys) else None
        t1.append([a, "%.2f" % annual[a], b if b else "", ("%.2f" % annual[b]) if b else ""])
    proj = [["Year", "Intermediate-Low (ft MLLW)", "Intermediate (ft MLLW)", "High (ft MLLW)"],
            ["2030", "5.48", "5.55", "5.66"], ["2050", "5.71", "6.02", "6.52"], ["2070", "5.96", "6.66", "7.86"],
            ["2100", "6.43", "7.95", "10.21"]]
    return [
        ("h2", "1. Purpose"),
        ("p", "This guidance gives city departments the sea level to design to for projects built, used or rebuilt "
              "on the waterfront, and the flooding levels the city uses for its streets and wharves. It replaces the "
              "2021 update."),
        ("h2", "2. The record"),
        ("p", "Mean sea level at the Port Tessaly gauge (PTG-01) has risen %.4f ft a year since 1995. Table 1 gives "
              "the annual means from the verified record." % trend_ft),
        ("table", t1, [18 * mm, 58 * mm, 18 * mm, 58 * mm]),
        ("h2", "3. Design mean sea level"),
        ("p", "Projects built or in use in 2027 are designed to a mean sea level of %.2f ft MLLW at the gauge, the "
              "record's trend line at mid-2027." % design),
        ("h2", "4. Projections"),
        ("p", "For assets with a design life past 2030 use Table 2, which follows the state's 2024 sea-level scenarios "
              "applied to the gauge."),
        ("table", proj, [18 * mm, 46 * mm, 46 * mm, 40 * mm]),
        ("h2", "5. Flooding levels"),
        ("p", "Front Street floods at its low point near Cutler Wharf when the water at the gauge reaches about "
              "11.8 ft MLLW. Ferry Lane floods at about 12.4 ft MLLW and Water Street at about 12.9 ft MLLW."),
        ("small", "Prepared by Waterfront and Harbor Engineering with the Office of Sustainability. Issued 3 September "
                  "2026."),
    ]


def write_slr(out, annual, design, trend_ft):
    _build(os.path.join(out, C.F_SLR), SLR_TITLE, "Waterfront and Harbor Engineering", C.CITY + " | " + C.DEPT,
           "Issued 3 September 2026. Applies to city projects from 1 October 2026.", slr_blocks(annual, design, trend_ft),
           "City of Port Tessaly, sea level guidance 2026", pdf_stamp(SLR_DATE, 11, 26))


# ---------------------------------------------------------------------------------- the trestle design basis
BASIS_DATE = dt.date(2026, 11, 20)
BASIS_TITLE = "Granite Wharf Reconstruction: Temporary Work Trestle Design Basis"


def basis_blocks():
    settings = ", ".join("%.2f" % s for s in C.DECK_SETTINGS)
    return [
        ("h2", "1. The work"),
        ("p", "The Granite Wharf deck, pile caps and timber bulkhead are replaced in 2027. The contractor works from a "
              "temporary pile-supported trestle along the wharf face from 1 April to 31 May 2027. The dates are set by "
              "the lobster fleet's return to the wharf moorings on 1 June and by the delivery of the new steel."),
        ("h2", "2. Deck elevation"),
        ("p", "The trestle piles are cut off to one of the deck elevations on the pile schedule: %s ft MLLW. The deck is "
              "set at the lowest of these at which high water is expected to reach the deck on no more than one tide "
              "between 00:00 on 1 April 2027 and 24:00 on 31 May 2027." % settings),
        ("p", "Water levels are those at the Port Tessaly gauge (PTG-01), in feet above MLLW of the 1983-2001 epoch, "
              "at the 2027 design mean sea level of the city's 2026 sea level guidance. A tide reaches the deck when the "
              "gauge's highest 15-minute reading at that high water is at or above the deck elevation."),
        ("h2", "3. Survival check"),
        ("p", "The trestle frame and bracing are checked for the five highest tides at the gauge from 1 November 2016 "
              "to 30 November 2026, taking no two within three days of each other."),
        ("h2", "4. Access"),
        ("p", "Materials reach the trestle by Front Street, which DPW closes when it floods. The schedule's access "
              "allowance is taken from the street's closures in the six years 2017 to 2022."),
        ("h2", "5. Program"),
        ("p", "Pile order to the fabricator: 15 January 2027. Mobilization: 22 March 2027. Trestle removed by 7 June 2027."),
        ("small", "Revision B, 20 November 2026. Revision A (2 October 2026) gave a work period of 8 March to 28 May; the "
                  "steel delivery moved it."),
    ]


def write_basis(out):
    _build(os.path.join(out, C.F_BASIS), BASIS_TITLE, "Waterfront and Harbor Engineering", C.CITY + " | " + C.DEPT,
           "Project WF-2025-07. Revision B, 20 November 2026.", basis_blocks(),
           "WF-2025-07 Granite Wharf, trestle design basis rev B", pdf_stamp(BASIS_DATE, 16, 3))


# ---------------------------------------------------------------------------------------------- station log
LOG = [
    ("1994-11-18", "RL", "Gauge installed on the gauge pier, Cutler Wharf. Float and encoder in 12 in stilling well. Logging 6 min."),
    ("1994-12-02", "RL", "Station datum set; first levelling to BM PTG 1 and PTG 3."),
    ("1995-01-01", "RL", "Verified product begins (15 min)."),
    ("1997-03-04", "RL", "Float wire replaced."),
    ("1999-10-12", "RL", "Logger replaced (same model). Clock checked against GPS."),
    ("2001-02-06", "RL", "Ice in well 2/4 to 2/6, heater element replaced."),
    ("2003-12-09", "RL", "Modem replaced after lightning."),
    ("2006-07-18", "RL", "Stilling well intake cleaned (mussels)."),
    ("2008-11-25", "RL", "Pier ladder and well bracket repainted."),
    ("2010-04-02", "RL", "Shore power upgrade on the gauge pier."),
    ("2012-08-14", "SH", "Acoustic sensor installed beside float; datum transferred by simultaneous readings over 30 days, no offset."),
    ("2012-09-13", "SH", "Float and encoder removed."),
    ("2014-01-03", "SH", "Ice in well, heater reset."),
    ("2015-03-17", "SH", "Harbormaster tide board float levelled; hourly logging at the office begins."),
    ("2016-02-08", "SH", "Comms down 0300 to 1100, logger buffered."),
    ("2017-10-30", "SH", "After the storm: sensor mount bracket found loose on the well, re-secured 1500."),
    ("2018-01-05", "SH", "Storm of 1/4: no damage to gauge. Pier deck damaged at Cutler Wharf."),
    ("2018-03-12", "SH", "Levelling brought forward. Sensor reference -0.08 ft against PTG 3. Sensor reset to reference 1430."),
    ("2019-07-22", "SH", "Data system migrated to the new server; verified product exports unchanged."),
    ("2020-06-09", "SH", "Annual levelling (delayed by building access)."),
    ("2021-02-02", "SH", "Ice in well, heater replaced."),
    ("2022-12-23", "SH", "Storm. Gauge ran through. Water over Front St and Cutler Wharf head."),
    ("2024-01-10", "SH", "Storm. Gauge ran through."),
    ("2024-01-13", "SH", "Storm. Shore power dipped twice on the pier; logger rode through on battery."),
    ("2024-01-16", "SH", "UPS on order for the gauge pier."),
    ("2024-03-05", "SH", "UPS installed."),
    ("2025-09-30", "SH", "Gauge pier repair contract awarded; gauge to stay in service except during the remount."),
    ("2026-04-21", "SH", "Sensor off for the pier cap replacement 4/21 to 4/28."),
    ("2026-04-28", "SH", "Radar sensor installed on new mount. Levelling: new station datum (see datum sheet rev 2026-06)."),
    ("2026-05-01", "SH", "6-min telemetry feed to the city data system starts (provisional)."),
    ("2026-07-14", "SH", "Verified product through June 2026 issued."),
    ("2026-10-28", "SH", "Storm. Gauge ran through; telemetry continuous."),
]


def write_log(out, wb_factory):
    rows = [("Date", "By", "Entry")] + [(d, by, txt) for d, by, txt in LOG]
    return wb_factory(os.path.join(out, C.F_LOG), {"Log": rows}, ("Stacy Huber", "Stacy Huber",
                      "2012-08-20T13:02:11Z", "2026-11-02T19:41:37Z"))


DICT = {
    C.F_VER: [("timestamp_utc", "time of the reading, UTC"), ("water_level_ft", "height of the water above the station datum STND (1995), feet"),
              ("quality", "V verified; I interpolated across a gap of six hours or less; M missing")],
    C.F_TEL: [("time_utc", "time of the reading, UTC"), ("wl_m", "height of the water above the station datum, metres"),
              ("qc", "P provisional (not yet verified)")],
    C.F_BOARD: [("reading_time", "harbormaster's office clock"), ("board_ft", "reading on the float tide board, feet")],
    C.F_TABLES: [("(each sheet)", "one year's predicted high and low waters as published in the harbor's tide tables; heights in feet above MLLW; times local")],
    C.F_CLOSE: [("wo_number", "work order number"), ("system", "work order system holding the record"),
                ("source", "who asked for the closure: DPW crew, or HM the harbormaster"),
                ("opened", "date and time the work order was opened, as recorded by the system"),
                ("closed", "date and time the work order was closed, as recorded by the system"),
                ("location", "street location as entered"), ("reason", "closure reason code"), ("notes", "free text")],
    C.F_WX: [("date", "local date"), ("tmax_f", "maximum temperature, F"), ("tmin_f", "minimum temperature, F"),
             ("precip_in", "precipitation, inches"), ("slp_mb_mean", "mean sea-level pressure, mb"),
             ("gust_mph", "peak gust, mph"), ("gust_dir_deg", "direction of the peak gust, degrees")],
    C.F_RIVER: [("date", "local date"), ("discharge_cfs", "daily mean discharge, cubic feet per second"),
                ("code", "A approved, P provisional, e estimated")],
}


def write_dict(out, wb_factory):
    sheets = {}
    for f, cols in DICT.items():
        name = f.split("_")[0][:10] + "_" + f.split("_")[1][:8] if "_" in f else f[:20]
        sheets[name[:31]] = [("File", "Column", "Meaning")] + [(f, c, m) for c, m in cols]
    return wb_factory(os.path.join(out, C.F_DICT), sheets, ("Stacy Huber", "Stacy Huber",
                      "2019-07-29T15:20:03Z", "2026-11-30T21:08:45Z"))
