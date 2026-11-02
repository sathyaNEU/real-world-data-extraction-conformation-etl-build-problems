"""The pack's documents (architecture 3), each in its issuer's own genre: the board's pupil forecast procedure, the
school's accommodation plan, the municipality's district profile, the school calendar and the board's draft
accommodation request."""
import datetime as dt
import re

import params as P
import world as W
from pack import normalise_zip


def write_pdf(path, title, issuer, blocks, stamp_date):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5)
    head = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14,
                          spaceBefore=8, spaceAfter=3)
    ttl = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14, leading=17)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    story = []
    for kind, val in blocks:
        if kind == "title":
            story += [Paragraph(val, ttl), Spacer(1, 4)]
        elif kind == "h":
            story.append(Paragraph(val, head))
        elif kind == "p":
            story += [Paragraph(val, body), Spacer(1, 3)]
        elif kind == "small":
            story.append(Paragraph(val, small))
        elif kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
                                   ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story += [t, Spacer(1, 5)]

    def stamp(canvas, doc):
        canvas.setAuthor(issuer)
        canvas.setCreator(issuer)
        canvas.setProducer(issuer)
        canvas.setTitle(title)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(2 * cm, 1.2 * cm, "%s  |  %s  |  page %d" % (issuer, title, doc.page))

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.8 * cm, invariant=1, title=title, author=issuer, creator=issuer,
                            producer=issuer)
    doc.build(story, onFirstPage=stamp, onLaterPages=stamp)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    for key in (b"/CreationDate", b"/ModDate"):
        def sub(m):
            new = stamp_date.encode()
            assert len(new) == len(m.group(1)), (m.group(1), new)
            return key + b" (" + new + b")"
        data = re.sub(re.escape(key) + rb" \(([^)]*)\)", sub, data)
    open(path, "wb").write(data)


def procedure(path):
    b = [
        ("title", "Pupil forecast for accommodation requests (PV-2), version 2"),
        ("small", "%s, bureau Huisvesting. Adopted by the executive board on 14 April 2026. Owner: beleidsmedewerker "
                  "huisvesting. Replaces version 1 (2022)." % P.BOARD),
        ("h", "1. Scope"),
        ("p", "This procedure sets how the board forecasts a school's pupils for its accommodation requests to the "
              "municipality of %s, for the three 1 October counts after the latest count." % P.CITY),
        ("h", "2. Definitions"),
        ("p", "<b>2.1 Count.</b> The pupils on the school's roll on 1 October of a school year."),
        ("p", "<b>2.2 Catchment.</b> The postcode areas the school serves, as listed in its accommodation plan."),
        ("p", "<b>2.3 Intake.</b> The intake of a count is the children who first count at it: the children who turned "
              "four in the twelve months to that 1 October."),
        ("p", "<b>2.4 Household.</b> A household as the municipal population register records it."),
        ("h", "3. The forecast"),
        ("p", "<b>3.1</b> The forecast pupils at a count are the pupils on the roll at the latest count who will not yet "
              "have completed group 8, plus the expected entrants from the catchment, plus the entrants from outside the "
              "catchment."),
        ("p", "<b>3.2</b> Each child living in the catchment on the latest 1 October who will first count at or before "
              "the forecast count is an expected entrant at the share of the children of the last five intakes in the "
              "same circumstance who entered the school, the share taken over the five intakes together. The circumstance "
              "is whether a brother or sister from the same household is on the school's roll at the count at which the "
              "child first counts; for a coming count, a brother or sister on the roll at the latest count who will not "
              "yet have completed group 8 at it."),
        ("p", "<b>3.3</b> The children of an intake are those living in the catchment on the 1 October of their count."),
        ("p", "<b>3.4</b> Entrants from outside the catchment are forecast at their average over the last five intakes, "
              "for each count."),
        ("p", "<b>3.5</b> A school is short of accommodation at a count when its forecast pupils exceed the capacity in "
              "its accommodation plan. The board requests extra accommodation from the first such count."),
        ("h", "4. Reporting"),
        ("p", "The bureau reports the forecast with the request; the municipality's form asks for pupils to the nearest "
              "ten."),
        ("small", "PV-2 v2. Next review April 2028."),
    ]
    write_pdf(path, "Pupil forecast procedure PV-2 v2", "%s bureau Huisvesting" % P.BOARD_SHORT, b,
              "D:20260414110000+00'00'")


def accommodation(path, w):
    b = [
        ("title", "Huisvestingsplan De Kwikstaart 2026"),
        ("small", "%s, bureau Huisvesting, with the school's director. 28 September 2026. Prepared by %s." %
         (P.BOARD, P.PEOPLE["planner"])),
        ("h", "1. The school"),
        ("p", "%s (BRIN 21KW) is a public primary school in Molenwijk, %s. It serves the postcode areas 3841 "
              "(Molenwijk) and 3842 (Rietveld)." % (P.SCHOOL, P.DISTRICT)),
        ("h", "2. Buildings"),
        ("table", [["Building", "Address", "Classrooms", "Gross floor area (m2)", "Built"],
                   ["Hoofdgebouw", "Molenwiek 2", "12", "2,184", "1979, renovated 2014"],
                   ["Dependance", "Molenwiek 4", "8", "1,322", "1996"]]),
        ("p", "The dependance also houses the after-school care (BSO) of %s." % P.PROVIDER),
        ("h", "3. Capacity"),
        ("p", "Under the municipal accommodation ordinance the two buildings give the school a capacity of <b>%d "
              "pupils</b> on a 1 October count." % w["capacity"]),
        ("h", "4. Counts"),
        ("table", [["1 October", "2022", "2023", "2024", "2025", "2026"],
                   ["Pupils"] + [str(len(W.roll(w["kids"], y))) for y in (2022, 2023, 2024, 2025, 2026)]]),
        ("small", "This plan states the buildings and their capacity on 28 September 2026; it does not forecast pupils."),
    ]
    write_pdf(path, "Huisvestingsplan De Kwikstaart 2026", "%s bureau Huisvesting" % P.BOARD_SHORT, b,
              "D:20260928120000+00'00'")


def district(path, w):
    rows = [["Wijk", "Inwoners", "0-3 jaar", "4-11 jaar", "12-17 jaar", "65+"]]
    day = dt.date(2026, 1, 1)
    for wijk in P.WIJKEN:
        ps = [p for p in w["persons"] if p["hh"]["wijk"] == wijk and W.lives_in(p, day)]
        age = lambda p: (day - p["birth"]).days / 365.25
        rows.append([wijk, "{:,}".format(len(ps)), str(sum(1 for p in ps if age(p) < 4)),
                     str(sum(1 for p in ps if 4 <= age(p) < 12)), str(sum(1 for p in ps if 12 <= age(p) < 18)),
                     str(sum(1 for p in ps if age(p) >= 65))])
    b = [
        ("title", "Wijkprofiel Veenhaven-Noord 2026"),
        ("small", "Gemeente %s, Onderzoek en Statistiek. Population on 1 January 2026 from the municipal population "
                  "register. Published 3 March 2026." % P.CITY),
        ("h", "Bevolking naar leeftijd"),
        ("table", rows),
        ("p", "Rietveld, completed between 2017 and 2019, has the youngest population of the district; Noorderpark the "
              "oldest."),
        ("small", "Figures for statistical use; small differences with the register arise from the reference date."),
    ]
    write_pdf(path, "Wijkprofiel Veenhaven-Noord 2026", "Gemeente %s, Onderzoek en Statistiek" % P.CITY, b,
              "D:20260303090000+00'00'")


def calendar(path):
    b = [
        ("title", "Schoolkalender De Kwikstaart 2026-2027"),
        ("small", "%s. Vakanties regio noord." % P.SCHOOL),
        ("table", [["Periode", "Van", "Tot en met"],
                   ["Herfstvakantie", "17 oktober 2026", "25 oktober 2026"],
                   ["Kerstvakantie", "19 december 2026", "3 januari 2027"],
                   ["Voorjaarsvakantie", "13 februari 2027", "21 februari 2027"],
                   ["Meivakantie", "24 april 2027", "9 mei 2027"],
                   ["Zomervakantie", "10 juli 2027", "22 augustus 2027"]]),
        ("p", "Studiedagen (geen school): 2 november 2026, 15 maart 2027, 25 juni 2027."),
    ]
    write_pdf(path, "Schoolkalender 2026-2027", P.SCHOOL, b, "D:20260615090000+00'00'")


def request(path, w):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(10.5)
    doc.add_heading("Aanvraag voorziening huisvesting 2028: De Kwikstaart (concept)", level=1)
    doc.add_paragraph("%s to the municipality of %s. Draft of 15 October 2026; the request is due by 31 January 2027. "
                      "Contact: %s." % (P.BOARD, P.CITY, P.PEOPLE["planner"]))
    doc.add_heading("1. Pupil forecast", level=2)
    doc.add_paragraph("The forecast for the counts of 1 October 2027, 2028 and 2029 follows the board's procedure PV-2 "
                      "and the capacity in the school's accommodation plan.")
    doc.add_heading("2. Use of the buildings", level=2)
    doc.add_paragraph("The municipality asks for the buildings' gas use in each of the last three school years, a school "
                      "year running from 1 August to 1 August, from the meter registers of the hoofdgebouw and the "
                      "dependance together.")
    doc.add_paragraph("It also asks how much the school's pupils use the after-school care in the dependance: the "
                      "attendances of De Kwikstaart pupils there on each weekday (all Mondays, all Tuesdays and so on) in "
                      "October 2026, one attendance being one pupil on one day.")
    doc.add_heading("3. Request", level=2)
    doc.add_paragraph("To be completed when the forecast is final.")
    cp = doc.core_properties
    cp.author = cp.last_modified_by = P.PEOPLE["planner"]
    cp.title = "Aanvraag huisvesting 2028 concept"
    cp.created = cp.modified = dt.datetime(2026, 10, 15, 14, 0)
    cp.revision = 3
    cp.comments = ""
    doc.save(path)
    normalise_zip(path, "2026-10-15T12:00:00Z", app="Microsoft Office Word")


def write_all(F, w):
    procedure(F["procedure"])
    accommodation(F["accommodation"], w)
    district(F["district"], w)
    calendar(F["calendar"])
    request(F["request"], w)
