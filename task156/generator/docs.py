"""task156 documents: the regional council's network discharge consent, PS03's data sheet, the council's Code of
Practice (wastewater section), the Ngaio Road servicing report, the Water Metering and Billing Policy and the PS03
storage upgrade brief. Each is the organisation's own document in its own genre; none describes the data. Their text is
kept here as data so checks.py can quote it."""
from __future__ import annotations

import io
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import codeofpractice as CP  # noqa: E402
import postprocess as PP     # noqa: E402
import records as R          # noqa: E402
import world as W            # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2329")
GREY = colors.HexColor("#5f6670")
KRC = colors.HexColor("#1d5a6e")
RDC = colors.HexColor("#3c5a2e")
ENG = colors.HexColor("#4a4a6a")
RULE = colors.HexColor("#a3abb5")
HEAD = colors.HexColor("#e9ecef")

F_CONSENT = "krc_consent_auth-2024-0418_network_overflows.pdf"
F_DATASHEET = "ps03_riverbank_rd_station_data_sheet.pdf"
F_COP = "rdc_code_of_practice_s5_wastewater_2022.pdf"
F_SERVICING = "rm26-0187_ngaio_road_servicing_report.pdf"
F_POLICY = "rdc_water_metering_billing_policy_2023.pdf"
F_BRIEF = "ps03_storage_upgrade_project_brief.docx"


def styles(font, bold, accent, size=10.0):
    return dict(
        body=ParagraphStyle("b" + font + str(size), fontName=font, fontSize=size, leading=size * 1.36, textColor=INK,
                            spaceAfter=6),
        h1=ParagraphStyle("h1" + font + str(size), fontName=bold, fontSize=14.0, leading=18.0, textColor=accent,
                          spaceAfter=3),
        sub=ParagraphStyle("s" + font + str(size), fontName=font, fontSize=8.9, leading=11.8, textColor=GREY,
                           spaceAfter=9),
        h2=ParagraphStyle("h2" + font + str(size), fontName=bold, fontSize=10.6, leading=14.0, textColor=accent,
                          spaceBefore=7, spaceAfter=3),
        cell=ParagraphStyle("c" + font + str(size), fontName=font, fontSize=8.8, leading=11.0, textColor=INK),
        cellb=ParagraphStyle("cb" + font + str(size), fontName=bold, fontSize=8.8, leading=11.0, textColor=INK),
        small=ParagraphStyle("sm" + font + str(size), fontName=font, fontSize=8.2, leading=10.6, textColor=GREY,
                             spaceAfter=4))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid(rows, widths, st, head=True):
    data = []
    for k, row in enumerate(rows):
        data.append([Paragraph(esc(str(c)), st["cellb"] if (head and k == 0) else st["cell"]) for c in row])
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


def _footer(left, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(2.0 * cm, 1.2 * cm, left)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _build(path, story, title, author, footer, font, stamp):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=1.8 * cm,
                            bottomMargin=2.0 * cm, title=title, author=author, subject="", creator="", producer="")
    f = _footer(footer, font)
    doc.build(story, onFirstPage=f, onLaterPages=f)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, stamp, stamp)


def _sections(st, sections):
    out = []
    for head, paras in sections:
        out.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            out.append(Paragraph(esc(p), st["body"]))
    return out


# ---------------------------------------------------------------------------------------------------- the consent
CONSENT = [
    ("Consent", [
        "Discharge permit AUTH-2024-0418 under section 15 of the Resource Management Act 1991, granted to Rauwhero "
        "District Council to discharge untreated wastewater from the engineered overflow points of the Rauwhero "
        "wastewater network to the Kahuwera River and its tributaries, at the locations in condition 1, for a term "
        "expiring on 31 March 2059.",
    ]),
    ("Conditions", [
        "1. The engineered overflow points are EO-01 at the Domain Road pump station (PS01), EO-02 at Mill Street "
        "(PS02), EO-03 at Riverbank Road (PS03), EO-04 at Totara Avenue (PS04), EO-05 at Station Road (PS05) and EO-06 "
        "at Kowhai Street (PS06).",
        "2. A discharge shall occur only when the inflow to a pump station exceeds what it can pump and store, or in "
        "an emergency.",
        "3. An overflow is a discharge through an engineered overflow point. Discharges at the same point less than 24 "
        "hours apart are one overflow, which begins when its first discharge begins. An emergency overflow is an "
        "overflow that begins while the pump station at that point is without mains power or has a pump out of "
        "service. Every other overflow is a wet weather overflow. The spill hours of an overflow are the hours its "
        "discharges lasted.",
        "4. The consent holder shall keep an overflow monitor at each engineered overflow point that records the start "
        "and stop of every discharge, and shall keep its records for the term of this consent.",
        "5. By 31 March each year the consent holder shall report to the Kahuwera Regional Council, for the previous "
        "calendar year, each engineered overflow point's wet weather overflows and their spill hours, and the "
        "network's emergency overflows.",
        "6. The average number of wet weather overflows a year at an engineered overflow point, assessed under "
        "condition 7, shall not exceed two.",
        "7. The frequency at an engineered overflow point is assessed by running the network that drains to it, as "
        "connected at the time of the assessment and with any connection assessed under condition 8, through every "
        "hour of the rainfall record of the climate station Rauwhero at Treatment Plant (KRC 1187) from 1 January 2004 "
        "to 31 December 2023, each day as it occurred. The average is the number of wet weather overflows the run "
        "produces divided by twenty.",
        "8. Before accepting a new connection of 50 or more dwellings to a catchment that drains to an engineered "
        "overflow point, the consent holder shall assess the frequency at that point with the connection at its full "
        "development and its design flows from the consent holder's Code of Practice for Land Development and "
        "Subdivision, and shall not accept the connection while the frequency so assessed exceeds the limit in "
        "condition 6.",
        "9. The consent holder shall complete the storage works at PS03 Riverbank Road in its network improvement plan "
        "by 30 June 2029 and shall report their progress with each annual report under condition 5.",
        "10. The Kahuwera Regional Council may review these conditions in March 2029 and in March of every fifth year "
        "after.",
    ]),
]


def write_consent(path):
    st = styles("LibSerif", "LibSerif-Bold", KRC, 10.2)
    s = [Paragraph("Kahuwera Regional Council", st["h1"]),
         Paragraph("Resource consent AUTH-2024-0418 | Discharge permit | Granted 18 March 2024", st["sub"])]
    s += _sections(st, CONSENT)
    s += [Spacer(1, 10), Paragraph("Signed for the Kahuwera Regional Council under delegated authority", st["body"]),
          Paragraph("%s, Consents Officer, 18 March 2024" % W.PEOPLE["consents"], st["body"])]
    _build(path, s, "AUTH-2024-0418 Rauwhero wastewater network overflows", "Kahuwera Regional Council",
           "Kahuwera Regional Council | AUTH-2024-0418 | Rauwhero District Council wastewater network", "LibSerif",
           b"D:20240318104512+13'00'")


def consent_text():
    return "\n".join(p for _, ps in CONSENT for p in ps)


# ---------------------------------------------------------------------------------------------------- data sheet
def datasheet_rows():
    return [
        ["Item", "Value"],
        ["Pumps", "Two submersible pumps, duty and assist, alternating duty"],
        ["Drawdown test, 7 November 2023", "Pump 1 alone 61.8 L/s; pump 2 alone 60.9 L/s; both together %.1f L/s" % W.QP],
        ["Wet well floor", "RL %.2f m" % W.FLOOR_RL],
        ["Duty pump start", "%.2f m above the floor" % W.DUTY_START],
        ["Assist pump start", "1.60 m above the floor"],
        ["High level alarm", "3.30 m above the floor"],
        ["Emergency storage chamber invert", "3.45 m above the floor"],
        ["Overflow weir crest (EO-03)", "%.2f m above the floor (RL %.2f m)" % (W.WEIR_ABOVE_FLOOR, W.FLOOR_RL + W.WEIR_ABOVE_FLOOR)],
        ["Storage, duty start to chamber invert", "%.0f m3 (wet well)" % W.WET_WELL_STORE],
        ["Storage, chamber invert to weir crest", "%.0f m3 (emergency storage chamber)" % (W.STORE - W.WET_WELL_STORE)],
        ["Storage, duty start to weir crest", "%.0f m3" % W.STORE],
        ["Overflow weir", "Sharp crested, 1.6 m long, to the Kahuwera River through a flap valve"],
        ["Rising main", "300 mm PE, 2.1 km to the treatment plant inlet"],
        ["Mains supply", "ICP %s" % R.ICP_NOW["PS03"]],
        ["SCADA", "Inflow is calculated by the RTU from the pumps' run and the wet well level every 15 minutes"],
    ]


def write_datasheet(path):
    st = styles("LibSans", "LibSans-Bold", RDC, 9.6)
    s = [Paragraph("Rauwhero District Council | Three Waters", st["sub"]),
         Paragraph("Pump station data sheet: PS03 Riverbank Road", st["h1"]),
         Paragraph("118 Riverbank Road, Rauwhero. Terminal station for the river terrace catchment. Revision 4, "
                   "7 November 2023.", st["sub"]),
         grid(datasheet_rows(), [6.0, 10.6], st),
         Spacer(1, 10),
         Paragraph("Levels are above the wet well floor unless given as RL (NZVD2016). Prepared by %s, Wastewater "
                   "Network Engineer." % W.PEOPLE["network"], st["small"])]
    _build(path, s, "PS03 Riverbank Road pump station data sheet", "Rauwhero District Council",
           "Rauwhero District Council | Three Waters | PS03 data sheet rev 4", "LibSans", b"D:20231107151840+13'00'")


# ---------------------------------------------------------------------------------------------------- code of practice
COP_TEXT = [
    ("5.1 Scope", [
        "This section sets the design standards for wastewater networks built for subdivision and land development "
        "in the Rauwhero District and vested in the council, and the design flows the council uses when it assesses "
        "a development's connection to an existing network.",
    ]),
    ("5.2 Design flows", [
        "The design occupancy is %.1f persons a dwelling and the average dry weather flow %d litres a person a day." %
        (CP.OCCUPANCY, CP.LPD),
        "A development's flow through the day is its average dry weather flow times the factors in Table 5.2, hour by "
        "hour in New Zealand time.",
        "Pipes are sized for a peak dry weather flow of %.1f times the average dry weather flow and checked for the "
        "self-cleansing velocity at the average." % CP.PDWF_FACTOR,
    ]),
    ("5.3 Materials and construction", [
        "Gravity mains in new networks are PE100 SDR17 with electrofusion or butt-welded joints, or PVC-U SN16 with "
        "solvent-welded joints where the council approves; manholes are precast with sealed lids where the council "
        "requires.",
    ]),
    ("5.4 Connection to the existing network", [
        "The council assesses the capacity of the existing network downstream of the connection point for each "
        "development, including its pump stations and their consented overflow limits, and may defer a connection "
        "until the works the council's network improvement plan schedules are complete.",
    ]),
]


def write_cop(path):
    st = styles("LibSans", "LibSans-Bold", RDC, 9.8)
    s = [Paragraph("Rauwhero District Council", st["sub"]),
         Paragraph("Code of Practice for Land Development and Subdivision", st["h1"]),
         Paragraph("Section 5: Wastewater. Effective 1 July 2022.", st["sub"])]
    s += _sections(st, COP_TEXT[:2])
    rows = [["Hour beginning", "Factor", "Hour beginning", "Factor"]]
    for h in range(12):
        rows.append(["%02d:00" % h, "%.2f" % CP.TABLE_5_2[h], "%02d:00" % (h + 12), "%.2f" % CP.TABLE_5_2[h + 12]])
    s += [Paragraph("Table 5.2 Hourly factors on the average dry weather flow", st["h2"]), grid(rows, [3.6, 2.4, 3.6, 2.4], st)]
    s += _sections(st, COP_TEXT[2:])
    _build(path, s, "Code of Practice for Land Development and Subdivision, Section 5", "Rauwhero District Council",
           "Rauwhero District Council | Code of Practice | Section 5 Wastewater | July 2022", "LibSans",
           b"D:20220701090000+12'00'")


# ---------------------------------------------------------------------------------------------------- servicing report
def write_servicing(path):
    st = styles("Carlito", "Carlito-Bold", ENG, 10.4)
    lots = W.SUB_DWELLINGS
    adwf = sum(lots) * CP.OCCUPANCY * CP.LPD / 86400.0
    s = [Paragraph("Ngaio Road subdivision, RM26-0187", st["h1"]),
         Paragraph("Infrastructure servicing report: wastewater. Prepared for the applicant by %s CPEng, 21 September "
                   "2026." % W.PEOPLE["engineer"], st["sub"]),
         Paragraph("1. The development", st["h2"]),
         Paragraph("The applicant proposes 260 residential lots on the former Ngaio Road orchard at the eastern edge of "
                   "the river terrace, each with one dwelling, built in three stages. The applicant asks the council to "
                   "accept the connection of stage 1 to the public network from March 2027.", st["body"]),
         grid([["Stage", "Lots and dwellings", "Titles expected"], ["1", str(lots[0]), "March 2027"],
               ["2", str(lots[1]), "April 2028"], ["3", str(lots[2]), "May 2029"], ["Total", str(sum(lots)), ""]],
              [3.0, 5.0, 5.0], st),
         Paragraph("2. Network", st["h2"]),
         Paragraph("The development's gravity mains are PE100 with welded joints at 1.2 to 2.4 m deep, draining to a "
                   "single connection at the council's manhole on the Riverbank Road trunk sewer, in the catchment of "
                   "the PS03 Riverbank Road pump station. No pump station is proposed within the development.",
                   st["body"]),
         Paragraph("3. Design flows", st["h2"]),
         Paragraph("Under section 5.2 of the council's Code of Practice the development at full occupation has an "
                   "average dry weather flow of %d x %.1f x %d litres a day, %.1f m3 a day or %.2f L/s, and a peak dry "
                   "weather flow of %.2f L/s." % (sum(lots), CP.OCCUPANCY, CP.LPD, adwf * 86.4, adwf,
                                                   adwf * CP.PDWF_FACTOR), st["body"]),
         Paragraph("4. Downstream capacity", st["h2"]),
         Paragraph("The capacity of the PS03 Riverbank Road pump station and its consented overflow limit are for the "
                   "council to assess under its Code of Practice and its discharge permit; the applicant has not "
                   "modelled them.", st["body"])]
    _build(path, s, "RM26-0187 Ngaio Road servicing report: wastewater", W.PEOPLE["engineer"],
           "RM26-0187 Ngaio Road subdivision | Wastewater servicing report", "Carlito", b"D:20260921163005+12'00'")


# ---------------------------------------------------------------------------------------------------- billing policy
POLICY = [
    ("1. Purpose", [
        "This policy sets how the council meters, reads and bills water supplied from the Rauwhero public supply, and "
        "how it reports water use.",
    ]),
    ("2. Meters and readings", [
        "Every connection to the public supply is metered. One meter may supply several rating units where the council "
        "has approved it; each of those rating units then has its own account carrying its share of the meter.",
        "Meters are read every quarter by the council's meter readers until the council's automatic meter reading "
        "begins, and every month after it. A reading the reader could not take is estimated by the billing system "
        "and replaced by the next actual reading. When a meter is exchanged, its removal reading and the new meter's "
        "installation reading are recorded on the day of the exchange.",
    ]),
    ("3. Billing", [
        "Water is billed on each account's share of its meter's consumption between actual readings, at the volumetric "
        "rate in the council's fees and charges for the year.",
    ]),
    ("4. Reporting water use", [
        "The council reports average residential water use per dwelling for a period as the water the meters supplying "
        "residential rating units recorded over the period, each meter's consumption between two consecutive actual "
        "readings, a meter exchange's removal and installation readings among them, spread evenly over the days from "
        "the day of the first reading to the day before the second, divided by the number of days in the period and "
        "by the average number of dwellings those meters supplied over the period. A dwelling is a separately used or "
        "inhabited part of a residential rating unit.",
    ]),
]


def write_policy(path):
    st = styles("LibSans", "LibSans-Bold", RDC, 9.8)
    s = [Paragraph("Rauwhero District Council", st["sub"]),
         Paragraph("Water Metering and Billing Policy", st["h1"]),
         Paragraph("Adopted by the council on 29 June 2023, effective 1 July 2023.", st["sub"])]
    s += _sections(st, POLICY)
    _build(path, s, "Water Metering and Billing Policy", "Rauwhero District Council",
           "Rauwhero District Council | Water Metering and Billing Policy | July 2023", "LibSans",
           b"D:20230630112210+12'00'")


def policy_text():
    return "\n".join(p for _, ps in POLICY for p in ps)


# ---------------------------------------------------------------------------------------------------- upgrade brief
BRIEF = [
    ("Project", "PS03 Riverbank Road storage augmentation, Long-Term Plan project 3W-2029-04."),
    ("Purpose", "Complete the storage works at PS03 that condition 9 of discharge permit AUTH-2024-0418 requires by 30 "
                "June 2029."),
    ("Scope", "A buried storage tank of 1,100 m3 beside the PS03 wet well, connected below the overflow weir crest so "
              "that the whole tank fills before the weir; return by gravity to the wet well as the station draws down; "
              "washdown, odour control and level instruments on the station's RTU."),
    ("Design inputs", "Tank base about RL 11.0 m; the flotation check against the design groundwater level, taken as the "
                      "highest daily level the regional council's terrace bore 72_1043 has recorded since 2004 plus 0.3 "
                      "m; construction dewatering in the gravels of the river terrace; the station's 2023 drawdown "
                      "test."),
    ("Programme", "Concept design December 2026; detailed design by September 2027; construction October 2028 to May "
                  "2029; commissioning by 30 June 2029."),
    ("Budget", "NZD 4.6 million in the Long-Term Plan, years 2027/28 to 2028/29."),
    ("Owner", "Three Waters, network operations; reporting to the Infrastructure Committee."),
]


def write_brief(path):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("PS03 Riverbank Road storage augmentation: project brief", level=1)
    d.add_paragraph("Rauwhero District Council, Three Waters. Version 2, 12 August 2026.")
    t = d.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for k, v in BRIEF:
        row = t.add_row().cells
        row[0].text = k
        row[1].text = v
    d.add_paragraph("")
    d.add_paragraph("The brief goes to the Infrastructure Committee with the concept design.")
    d.save(path)
    PP.normalize_docx(path, "Three Waters", "Three Waters", "2026-07-20T22:14:00Z", "2026-08-12T03:40:00Z", 3, 214,
                      seed="brief", title="PS03 storage augmentation project brief", company=W.COUNCIL)


def write_all(out):
    import os
    write_consent(os.path.join(out, F_CONSENT))
    write_datasheet(os.path.join(out, F_DATASHEET))
    write_cop(os.path.join(out, F_COP))
    write_servicing(os.path.join(out, F_SERVICING))
    write_policy(os.path.join(out, F_POLICY))
    write_brief(os.path.join(out, F_BRIEF))
