"""task178 documents: the station description, the design standard's hydrology section and the crossing alternatives
study (PDFs), the levels log (text) and the data dictionary (Excel). Their text is held here as data so checks.py can
quote it and verify.py can read it back."""
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
ACCENT = colors.HexColor("#22543d")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_stamp(d, hh=10, mi=0):
    a, b = C.dst_bounds_pst(d.year)
    off = -7 if a.date() <= d < b.date() else -8
    return ("D:%04d%02d%02d%02d%02d00%+03d'00'" % (d.year, d.month, d.day, hh, mi, off)).encode()


STYLES = dict(
    org=ParagraphStyle("org", fontName="Carlito-Bold", fontSize=9.5, leading=12, textColor=ACCENT, spaceAfter=2),
    h1=ParagraphStyle("h1", fontName="LibSans-Bold", fontSize=14.5, leading=18.5, textColor=INK, spaceAfter=4),
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
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5efe8")))
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


def text_blocks(blocks):
    """the plain text of a document's blocks, the way checks.py and the leak sweep read them"""
    out = []
    for b in blocks:
        if b[0] == "table":
            out.extend(" | ".join(str(c) for c in r) for r in b[1])
        else:
            out.append(b[1])
    return "\n".join(out)


# ------------------------------------------------------------------------------------- the station description
STATION_DATE = dt.date(2024, 3, 18)
STATION_TITLE = "TUM-02 Tumwick River near Sauer: Station Description"


def station_blocks():
    hist = [["Period", "Gage-height sensor", "Recording"],
            ["Oct 1979 to Jun 1993", "Float in 24 in steel well, punched-paper recorder", "15 min, tape read at the office"],
            ["Jul 1993 to Apr 2008", "Gas-purge pressure sensor (bubbler), orifice in the pool", "Data logger, 15 min"],
            ["May 2008 to present", "Gas-purge pressure sensor, new orifice line (see Datum)", "Data logger, 15 min; cellular telemetry from 2011"]]
    return [
        ("h2", "Location"),
        ("p", "Lat 47 38 12, long 121 49 05, on the left bank 0.6 mi upstream of the Sauer mill intake and 900 ft upstream "
              "of the Sauer pipe bridge (the mill's 36-inch raw-water main). No tributary enters between the gage and the "
              "pipe bridge. Drainage area 238 square miles."),
        ("h2", "Establishment and operation"),
        ("p", "Established October 1979 by Callender Paper Company for the Sauer mill's water right and intake operations. "
              "Operated by the mill's Water Resources group. Discharge measurements are made by wading or from the cableway 120 "
              "ft upstream of the gage at medium and high flows, by ADCP from water year 2005."),
        ("h2", "Gage"),
        ("table", hist, [36 * mm, 76 * mm, 58 * mm]),
        ("p", "Reference gages: a 0 to 14 ft enamel staff in the pool, read at each visit; a crest-stage gage on the shelter "
              "pier, serviced at visits. Logger clock set to Pacific Standard Time throughout the year."),
        ("h2", "Datum"),
        ("p", "Gage datum is 182.40 ft NAVD88 from 1 October 2009. From October 1979 to 30 September 2009 the datum was "
              "184.40 ft NAVD88; it was lowered 2.00 ft when the orifice was reset below the low-water line after the "
              "2008 gravel removal downstream. Records are kept on the datum in use at the time."),
        ("h2", "Control"),
        ("p", "Low water: bedrock ledge across the channel 140 ft below the gage, stable. Medium and high water: the channel "
              "for about 1,200 ft below the gage. Right bank high, on a wooded terrace. Left bank a fenced pasture with "
              "a farm road to the cableway."),
        ("h2", "Records"),
        ("p", "Annual peak stages for water years 1980 to 2015 are kept in the annual peak register. From water year 2016 "
              "the 15-minute stage record is held in the hydrologic database; its record review is outstanding and the "
              "series carries the provisional grade. Discharge measurements to water year 2004 are in the transcribed field "
              "notes; from water year 2005 in the measurement database."),
        ("small", "Revised 18 March 2024 (S. Huber): telemetry and records sections updated. Previous revision 14 June 2011."),
    ]


def write_station(out):
    _build(os.path.join(out, C.F_STATION), STATION_TITLE, "Water Resources", C.COMPANY + " | " + C.DIVISION,
           "Station TUM-02. Revised 18 March 2024.", station_blocks(), "TUM-02 station description, rev. 2024-03",
           pdf_stamp(STATION_DATE, 15, 7))


# ------------------------------------------------------------------------------- the design standard, section 4
STANDARD_DATE = dt.date(2021, 4, 26)
STANDARD_TITLE = "Engineering Standard, Section 4: Hydrology"


def mse_table():
    return [["|G|", "A", "B"],
            ["0.00 to 0.90", "-0.33 + 0.08 |G|", "0.94 - 0.26 |G|"],
            ["0.90 to 1.50", "-0.52 + 0.30 |G|", "0.94 - 0.26 |G|"],
            ["above 1.50", "-0.52 + 0.30 |G|", "0.55"]]


def standard_blocks():
    return [
        ("h2", "4.1 Scope"),
        ("p", "This section sets the design floods for company structures in or over rivers and streams: intakes, "
              "pipelines, pipe bridges and their piers and abutments at company mills."),
        ("h2", "4.2 Design flood for crossings"),
        ("p", "4.2.1 A crossing is designed to pass the peak discharge with a 1 percent annual exceedance probability at "
              "the structure."),
        ("p", "4.2.2 Where the company gages the river at the structure, the design flood is estimated from that gage's "
              "annual peak series: the largest instantaneous discharge in each complete water year (1 October to 30 "
              "September) of the period the project names."),
        ("p", "4.2.3 The annual peaks are fitted with the log-Pearson Type III distribution by the method of moments of "
              "the base-10 logarithms of the peaks: the mean, the standard deviation (divisor n - 1) and the station skew "
              "G = n S(x - m)^3 / ((n - 1)(n - 2) s^3)."),
        ("p", "4.2.4 The station skew is weighted with the generalized skew for western Washington, %.2f, whose mean "
              "square error is %.3f: Gw = (%.3f G + MSE_G (%.2f)) / (%.3f + MSE_G), with MSE_G = 10^(A - B log10(n/10)) "
              "from Table 4.2." % (C.REG_SKEW, C.REG_SKEW_MSE, C.REG_SKEW_MSE, C.REG_SKEW, C.REG_SKEW_MSE)),
        ("table", mse_table(), [34 * mm, 50 * mm, 50 * mm]),
        ("p", "4.2.5 The design discharge is 10^(m + K s), with K the Pearson Type III frequency factor at the weighted "
              "skew for a 1 percent exceedance probability."),
        ("p", "4.2.6 The series is checked for monotonic trend by the Mann-Kendall test at the 5 percent level, two-sided. "
              "A significant trend is referred to the Manager, Water Resources, before the design flood is used."),
        ("h2", "4.3 Other streams"),
        ("p", "Ungaged streams use the state's regional regression equations at the structure's drainage area, with the "
              "standard error stated in the design memorandum."),
        ("small", "Issue 3, 26 April 2021. Supersedes Issue 2 (2014). Approved: Director of Engineering."),
    ]


def write_standard(out):
    _build(os.path.join(out, C.F_STANDARD), STANDARD_TITLE, "Engineering", C.COMPANY + " | Engineering",
           "Issue 3, 26 April 2021.", standard_blocks(), "Callender Engineering Standard 4, issue 3",
           pdf_stamp(STANDARD_DATE, 9, 48))


# ------------------------------------------------------------------------------ the crossing alternatives study
STUDY_DATE = dt.date(2025, 12, 12)
STUDY_TITLE = "Sauer Pipe Bridge Replacement: Waterway Alternatives Study"
STUDY_CONFIG = {"A": ("two spans, one pier at the channel's right third", 196.10),
                "B": ("two spans, pier at the left bank", 196.40),
                "C": ("three spans, two piers left of the channel", 196.70),
                "D": ("single 210 ft span, abutments set back 40 ft", 197.10),
                "E": ("single 240 ft span, left abutment on the terrace", 197.40),
                "F": ("single 240 ft span, raised profile", 197.90),
                "G": ("single 270 ft span, raised profile", 198.30)}


def study_blocks():
    alts = [["Alternative", "Configuration", "Pipe soffit (ft NAVD88)", "Capacity (cfs)"]]
    for name, cap in C.ALTERNATIVES:
        cfg, soffit = STUDY_CONFIG[name]
        alts.append([name, cfg, "%.2f" % soffit, "{:,}".format(cap)])
    return [
        ("h2", "1. Background"),
        ("p", "The Sauer mill's 36-inch raw-water main crosses the Tumwick River on a 1968 steel truss pipe bridge 900 ft "
              "downstream of the company's stage gage TUM-02. In the flood of 8 January 2025 drift struck the truss "
              "and the pipe; the main was isolated, the pipe re-supported, and the main returned to service on temporary "
              "supports. The bridge is to be replaced, with in-water work in the 2027 season."),
        ("h2", "2. Waterway alternatives"),
        ("p", "Each alternative's capacity is the discharge its waterway passes with 3.0 ft between the water surface and "
              "the pipe soffit, from the reach model (HEC-RAS, steady flow, cross sections surveyed October 2025)."),
        ("table", alts, [24 * mm, 76 * mm, 36 * mm, 30 * mm]),
        ("h2", "3. Design discharge and selection"),
        ("p", "The design discharge is the peak discharge at TUM-02 with a 1 percent chance of being exceeded in any year, "
              "estimated by Callender Water Resources under Engineering Standard 4.2 from the gage's annual peaks of water "
              "years 1980 to 2025. The crossing's drainage area is the gage's. The alternative carried to design is the "
              "smallest whose capacity is at least the design discharge."),
        ("h2", "4. Model calibration"),
        ("p", "The reach model is checked against the water levels observed at the crest of each water year 2020 to 2025: "
              "the stage at TUM-02 at the reading that recorded the water year's highest stage, and the water level at the "
              "existing pipe bridge's radar at the same moment."),
        ("h2", "5. Construction"),
        ("p", "In-water work is limited to 15 July to 15 September. The contractor's work-area isolation is set from the "
              "highest stage the river reached at TUM-02 in the 15 July to 15 September window of each year 2016 to 2025."),
        ("h2", "6. Next steps"),
        ("p", "Callender to confirm the design discharge and the alternative; preliminary design of the selected "
              "alternative; HPA and shoreline permit applications in spring 2026."),
        ("small", "Crandell Hyde Engineering for Callender Paper Company. Draft for owner review, 12 December 2025."),
    ]


def write_study(out):
    _build(os.path.join(out, C.F_STUDY), STUDY_TITLE, "Crandell Hyde Engineering", C.COMPANY + " | Sauer crossing",
           "Project NW-2025-14. Draft for owner review, 12 December 2025.", study_blocks(),
           "NW-2025-14 Sauer pipe bridge, waterway alternatives (draft)", pdf_stamp(STUDY_DATE, 16, 41))


# ------------------------------------------------------------------------------------------------ the levels log
def levels_text():
    L = [
        "TUM-02 TUMWICK RIVER NEAR SAUER -- LEVELS",
        "Callender Paper Company, Sauer Mill Water Resources",
        "Elevations in feet, NAVD88 (levels before 2004 converted from NGVD29 by +3.52, VERTCON at the gage).",
        "",
        "Reference marks",
        "  RM1  chiseled cross on bedrock outcrop, left bank 60 ft upstream of shelter ........ 199.86",
        "  RM2  brass disk in shelter pier, top of pier ............................................ 197.42",
        "  RM3  rebar with cap, farm road at cableway anchor ........................................ 201.13",
        "",
        "Date        By     Run                                Result",
        "1979-10-04  RK     establish datum                    gage datum 184.40; staff zero set to datum",
        "1984-08-21  RK     annual check                       staff and well tape within 0.01",
        "1989-09-12  RK     annual check                       staff +0.01, left",
        "1993-07-14  RK     bubbler installed                  orifice referenced to staff; no offset",
        "1998-08-25  SH     check                              staff 0.00; orifice 0.00",
        "2003-09-09  SH     check                              staff -0.01, left",
        "2008-05-13  SH     new orifice line after gravel removal  orifice referenced to staff; no offset",
        "2009-09-29  SH     datum lowered                      gage datum 182.40 from 2009-10-01; staff renumbered (+2.00)",
        "2013-08-20  SH     check                              staff 0.00; orifice 0.00",
        "2017-08-16  SH     check                              staff +0.01, left; CSG reference 0.00",
        "2019-03-12  SH/GW  pipe bridge radar RAD-1 installed  sensor face 199.34 (shot from RM2)",
        "2021-08-24  GW     check                              staff 0.00; orifice 0.00",
        "2023-05-03  GW/DM  check; pipe bridge radar           staff 0.00; RAD-1 sensor face 199.84 (shot from RM2)",
        "2025-08-27  GW     after controller swap             orifice referenced to staff; offset reset (see visit)",
        "",
    ]
    return "\r\n".join(L)


def write_levels(out):
    with open(os.path.join(out, C.F_LEVELS), "w", encoding="utf-8", newline="") as fh:
        fh.write(levels_text())


# ------------------------------------------------------------------------------------------- the data dictionary
DICT = {
    C.F_PEAKS: [("WY", "water year (1 October to 30 September), named for the year it ends"),
                ("Date, Time", "date and local time of the peak"),
                ("Gage height (ft)", "peak gage height, feet above the gage datum in use on the date"),
                ("Remarks", "how the peak was obtained where not from the recorder")],
    C.F_STAGE: [("timestamp", "time of the reading (see file header)"), ("stage_ft", "gage height recorded by the logger, feet"),
                ("grade", "P provisional"), ("qualifier", "blank, or E estimated")],
    C.F_MEAS_OLD: [("(sheets by decade)", "discharge measurement notes transcribed from the field forms, 1980 to 2004"),
                   ("Gage ht", "mean gage height during the measurement, feet"), ("Discharge", "cubic feet per second"),
                   ("Rated", "the hydrographer's rating of the measurement: E excellent, G good, F fair, P poor")],
    C.F_MEAS_NEW: [("meas_no", "measurement number, continuing the field-note series"),
                   ("start_time, end_time", "local time"),
                   ("mean_gh_ft", "mean gage height during the measurement, feet"),
                   ("discharge, discharge_unit", "measured discharge and its unit"),
                   ("area, width, mean_velocity", "in the units of the discharge (square metres or square feet, metres or feet)"),
                   ("quality", "Good, Fair, Poor"), ("control_condition", "condition of the control at the visit")],
    C.F_VISITS: [("arrive, depart", "time on site"), ("staff_gage_ft", "staff reading on arrival"),
                 ("logger_ft", "logger reading on arrival"), ("meas_no", "discharge measurement made at the visit"),
                 ("work_done", "work at the visit"), ("notes", "free text")],
    C.F_SCADA: [("Timestamp", "historian timestamp"), ("SAUER_RAD1_DIST.PV", "radar RAD-1, distance from sensor to water, ft"),
                ("SAUER_RAD1_LVL.PV", "radar RAD-1, water level, ft NAVD88 (computed in SCADA)"),
                ("SAUER_36IN_FLOW.PV", "raw-water main flow at the crossing meter, MGD"),
                ("SAUER_36IN_PRESS.PV", "raw-water main pressure at the crossing, psi")],
    C.F_WO: [("wo_no", "work order"), ("asset", "asset tag"), ("opened, completed", "local date and time"),
             ("type", "PM preventive, CM corrective, PR project"), ("description", "as entered")],
}


def write_dict(out, wb_factory):
    sheets = {}
    for f, cols in DICT.items():
        sheets[f.split(".")[0][:31]] = [("File", "Field", "Meaning")] + [(f, c, m) for c, m in cols]
    return wb_factory(os.path.join(out, C.F_DICT), sheets, ("Stacy Huber", "Gary Wagner",
                      "2016-03-02T17:44:09Z", "2025-11-04T23:10:52Z"))
