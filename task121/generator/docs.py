"""The district's documents: the odor complaint procedure (CP-14 rev. 4), the station's readme, the complaint
export's field reference."""
import io
import re
import zipfile

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate

import core
import postprocess as PP

PROCEDURE = [
    ("t", "Compliance Procedure CP-14: Odor Complaint Response"),
    ("s", "Revision 4, effective January 5, 2026. Supersedes revision 3 (March 12, 2024). Approved by Erica Schmitt, "
          "Compliance Manager."),
    ("h", "1. Purpose"),
    ("p", "This procedure sets out how the District logs and responds to complaints about odors and how it assembles "
          "the record it relies on when it asks the Hearing Board for an order for abatement under Health and Safety "
          "Code section 41700 and District Rule 402 (Nuisance)."),
    ("h", "2. Intake"),
    ("p", "Complaints reach the District by telephone (the office line during business hours and the after-hours "
          "line, whose messages staff log the next business morning), through the web form on the District's site "
          "and, from January 2026, through the District's complaint app. Each complaint is logged in the complaint "
          "system with the complainant's service address, the time the complainant noticed the odor and the "
          "complainant's description. Staff ask callers for the time they noticed the odor and log the time they "
          "give."),
    ("p", "The District acts on complaints from addresses inside its boundary. Complaints from outside the boundary "
          "are referred to the air district concerned."),
    ("h", "3. Definitions"),
    ("p", "<b>Complaint.</b> One person's report of an odor. A report that reaches the District more than once is "
          "one complaint."),
    ("p", "<b>Household.</b> The service address of the complaint, including any unit number."),
    ("p", "<b>Time noticed.</b> The date and time the complainant noticed the odor, in local time."),
    ("p", "<b>Odor event.</b> A household's complaints whose times noticed fall within two hours of the time "
          "noticed of the household's first complaint in the event. A complaint noticed more than two hours after "
          "that first complaint starts a new event. An event takes the time noticed and the location of its first "
          "complaint."),
    ("p", "<b>Event hour.</b> The clock hour, local time, containing the event's time noticed."),
    ("p", "<b>Usable wind measurement.</b> A 5-minute record of the wind as the station's wind monitor measured it."),
    ("p", "<b>Hourly wind.</b> The vector average of the Harlow Falls station's 5-minute winds for the clock hour: "
          "each 5-minute wind is taken as a vector of its speed and direction, and the hourly wind has the speed "
          "and direction of the average vector. An hour has a usable wind when at least nine of its twelve 5-minute "
          "records are usable wind measurements."),
    ("p", "<b>Calm.</b> An hour with a usable wind whose speed is below 0.5 m/s. A calm hour has no wind direction."),
    ("p", "<b>Upwind check.</b> A permitted source lies upwind of a household in an hour when the hourly wind "
          "direction is within 30 degrees of the compass bearing from the household's location, as the complaint "
          "system geocodes it, to the source's location in the District's odor source list. No source lies upwind "
          "in a calm hour or in an hour without a usable wind."),
    ("p", "An upwind check shows that a source could have reached the household in that hour. On its own it does not "
          "show which source did."),
    ("p", "The description is the complainant's account of the odor; it is not a finding of its source."),
    ("h", "4. Response"),
    ("p", "The duty inspector reviews new complaints each business day, calls back where the complainant asked, and "
          "visits where an odor may still be present. Inspectors record what they find on arrival. Odors in the "
          "valley are often gone by the time an inspector arrives; a visit that finds no odor does not close the "
          "question of the complaint."),
    ("h", "5. Abatement"),
    ("p", "When the District's records show that a permitted source is responsible for odor reaching a considerable "
          "number of households, the Compliance Manager may petition the Hearing Board for an order for abatement, "
          "with the District's determination of the source and the record behind it. An order issued before May 1 "
          "governs the following odor season."),
    ("h", "6. Records"),
    ("p", "The complaint system export, the Harlow Falls station's 5-minute records and maintenance log, and the "
          "District's odor source list are the record for a determination. The Harlow Falls station is the "
          "District's wind record for the valley floor; the regional airport's observations are not used for the "
          "upwind check."),
    ("p", "Complaint records are kept for five years after the year in which they are logged, and the station's "
          "records for five years after the year in which they are taken."),
    ("h", "7. Confidentiality"),
    ("p", "A complainant's name, telephone number and e-mail address are confidential. When the District releases "
          "its complaint records, it gives each complaint's dates, general location and description, and not who "
          "made it."),
    ("h", "Revision history"),
    ("p", "Revision 4 (January 5, 2026): the District's complaint app added to intake; the Harlow Falls station's "
          "5-minute records made the wind record for the upwind check. Revision 3 (March 12, 2024): messages on the "
          "after-hours line logged the next business morning. Revision 2 (August 1, 2019): the web form added."),
]


def _styles():
    ss = getSampleStyleSheet()
    return dict(
        body=ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.8, spaceAfter=7),
        head=ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13, spaceAfter=3,
                            spaceBefore=5),
        title=ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=16,
                             spaceAfter=3),
        small=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica-Oblique", fontSize=8.6, leading=11,
                             spaceAfter=10),
        lh=ParagraphStyle("lh", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=12,
                          textColor=colors.HexColor("#24543A")),
        lh2=ParagraphStyle("lh2", parent=ss["Normal"], fontName="Helvetica", fontSize=8, leading=10,
                           textColor=colors.HexColor("#24543A"), spaceAfter=14),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.9 * inch, 0.55 * inch, text)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def procedure_pdf(path):
    st = _styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.85 * inch, title="CP-14 Odor Complaint Response, rev. 4",
                            author="Compliance Division", creator="Compliance Division", producer="Compliance Division")
    story = [Paragraph(core.ORG, st["lh"]), Paragraph("Compliance Division, 1180 Mill Street, Harlow Falls", st["lh2"])]
    for kind, text in PROCEDURE:
        sty = {"t": st["title"], "s": st["small"], "h": st["head"]}.get(kind, st["body"])
        story.append(Paragraph(text, sty))
    doc.build(story, onFirstPage=_footer("CP-14 rev. 4, January 5, 2026"), onLaterPages=_footer("CP-14 rev. 4, January 5, 2026"))
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, b"D:20260105091500-08'00'", "Compliance Division")


def procedure_text():
    return "\n".join(re.sub(r"<[^>]+>", "", t) for _, t in PROCEDURE)


README = """Harlow Falls meteorological station (HFS)
Upper Kestrel Valley Air Quality Management District, Monitoring Section

Location: district office yard, 1180 Mill Street, Harlow Falls; 39.74612 N, 121.61937 W; ground 412 m above sea level.
Siting: the tower stands on the valley floor, about 140 m from the nearest building, with open fetch up and down the
valley.

Instruments
  Wind: propeller and vane wind monitor on a 10 m tower (replaced June 2026, same model).
  Temperature: aspirated probes at 2 m and 10 m.
  Solar radiation: pyranometer at 2 m.
  Logger: samples every second and writes a record every 5 minutes.

Export: hfs_met_5min_2026-01-01_2026-09-30.csv, {rows:,} records, one per 5 minutes, 1 January 2026 00:00 to
30 September 2026 23:55.

Columns
  datetime_pst      start of the 5-minute period. All times are Pacific Standard Time (UTC-8) throughout the year;
                    the station's clock does not change for daylight saving.
  ws_ms             mean wind speed over the period, m/s
  wd_deg            mean wind direction over the period, degrees from true north, the direction the wind blows from
  sigma_theta_deg   standard deviation of the wind direction over the period, degrees
  t2m_c, t10m_c     air temperature at 2 m and 10 m, degrees C
  solar_wm2         solar radiation, W/m2
  qc                V: the record passed the logger's range checks; M: no record was written (values blank)

"""

FIELDS = """Complaint system export: fields
Upper Kestrel Valley Air Quality Management District, Compliance Division
Export of {export}

complaint_no     the system's number for the record, given when the record is created
received         date and time the record was created in the system, Pacific time
channel          Phone, Web form or App
noticed          date and time the complainant noticed the odor, Pacific time, as the complainant gave it
contact_id       the contact record the complaint came in under (a phone number, an e-mail address or an app
                 registration)
address          service address as the complainant gave it
city, zip        mailing city and ZIP code
latitude,
longitude        the address as the system geocoded it (WGS 84)
geocode_match    Parcel: matched to the parcel; Street segment: placed along the street segment
description      the complainant's description, as entered
intensity        1 (faint) to 5 (overwhelming), as the complainant rated it
duration         how long the complainant said the odor lasted
follow_up        Call back or Site visit, where staff followed up
finding          what the inspector found on arrival, for site visits
staff            initials of the staff member who followed up
status           Open or Closed
"""


def normalize_docx(data, path):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        parts = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    drop = {"word/stylesWithEffects.xml", "docProps/thumbnail.jpeg"}
    drop |= {n for n, _ in parts if n.startswith("customXml/")}
    out = []
    for name, b in parts:
        if name in drop:
            continue
        if name.endswith(".rels") or name == "[Content_Types].xml":
            b = re.sub(rb'<Relationship [^>]*Target="[^"]*(stylesWithEffects\.xml|thumbnail\.jpeg|customXml/[^"]*)"/>',
                       b"", b)
            b = re.sub(rb'<Override PartName="/(word/stylesWithEffects\.xml|docProps/thumbnail\.jpeg|customXml/[^"]*)"'
                       rb'[^>]*/>', b"", b)
            b = re.sub(rb'<Default Extension="jpeg"[^>]*/>', b"", b)
        if name.endswith((".xml", ".rels")):
            b = b.replace(b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n", PP.DECL)
        if name == "docProps/app.xml":
            b = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Office Word</Application>", b)
            b = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0000</AppVersion>", b)
            b = re.sub(rb"<Company>[^<]*</Company>", b"", b)
        if name == "docProps/core.xml":
            b = re.sub(rb"<cp:lastPrinted>[^<]*</cp:lastPrinted>", b"", b)
            b = b.replace(b"python-docx", b"")
        out.append((name, b))
    with zipfile.ZipFile(path, "w") as z:
        for name, b in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, b)

