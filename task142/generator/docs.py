"""The pack's documents, each in its issuer's own genre: Stadswarmte's capacity procedure and the hydraulic test of OS
West, the consultant's concept heat-load study, Stadswarmte's 2026 tariff sheet and the programme's scope of works."""
import datetime as dt
import re
import zipfile

import params as P
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
        ("title", "Capacity test for new connections (CT-03), version 3"),
        ("small", "%s, Network Planning. Approved 12 May 2026, effective 1 June 2026. Owner: network capacity planner. "
                  "Supersedes version 2 (March 2023)." % P.HEATCO),
        ("h", "1. Scope"),
        ("p", "This procedure tests whether a station of a %s secondary network can supply new connections on the design "
              "day. It applies to every connection request and to every programme of connections planned over more than "
              "one heating season." % P.HEATCO_SHORT),
        ("h", "2. Definitions"),
        ("p", "<b>2.1 Heating season.</b> The twelve months from 1 October to 30 September, named by its two years (the "
              "2027-28 heating season runs from 1 October 2027 to 30 September 2028)."),
        ("p", "<b>2.2 Design day.</b> The day at the design outdoor temperature of -10 &deg;C, on which a station supplies "
              "at its maximum supply temperature."),
        ("p", "<b>2.3 Connection.</b> A building's delivery set on the network with its own heat meter. A block with a "
              "collective heating installation is one connection."),
        ("p", "<b>2.4 Meter year.</b> The twelve months from 1 October to 30 September of the heat meter readings."),
        ("h", "3. The test"),
        ("p", "<b>3.1</b> A station's design-day flow, in cubic metres an hour, is limited by its pumps and heat "
              "exchangers. The station's current hydraulic test states the design-day flow available for connections not "
              "yet in service."),
        ("p", "<b>3.2 Design-day flow of a connection.</b> The design-day flow of a connection, in m<super>3</super>/h, is "
              "its design heat load in kW divided by 1.163 times the temperature difference in K between the supply and the "
              "return that its heating installation makes at the connection on days with a daily mean outdoor temperature "
              "of 0 &deg;C or lower at the Lekstede weather station. For a connection in service the temperature difference "
              "is read from its heat meter on such days in the last full meter year. For a connection not yet in service it "
              "is the temperature difference its heating installation is expected to make in service on such days."),
        ("p", "<b>3.3 Season test.</b> A station runs short in a heating season when the design-day flows of the "
              "connections to be connected by the start of that season, added at full value, exceed the available "
              "design-day flow stated in the station's current hydraulic test. For a programme the planner reports the "
              "first heating season in which the station runs short, or that it does not run short in any season of the "
              "programme."),
        ("p", "<b>3.4 Design heat load.</b> The design heat load of a connection is the design heat loss of the building "
              "in its most recent heat-load study under NEN-EN 12831 at the design outdoor temperature of -10 &deg;C."),
        ("h", "4. Reporting"),
        ("p", "<b>4.1</b> The planner presents the test to the directors with the evidence it rests on, at the latest in "
              "the November before the first season of the programme. Flows are reported in m<super>3</super>/h."),
        ("p", "<b>4.2</b> Where a station runs short, Asset Management prepares the reinforcement (a third exchanger, "
              "larger pumps or both) so that it is in service before the start of that season."),
        ("small", "CT-03 v3. Next review May 2028."),
    ]
    write_pdf(path, "Capacity test for new connections CT-03 v3", "%s Network Planning" % P.HEATCO_SHORT, b,
              "D:20260512101500+00'00'")


def hydraulic(path, w):
    conns = w["conns"]
    res = [c for c in conns if c["cat"] == "Woningen"]
    uti = [c for c in conns if c["cat"] == "Utiliteit"]
    flows = w["committed_by_conn"]
    fr = sum(flows[c["idx"]] for c in res)
    fu = sum(flows[c["idx"]] for c in uti)
    tot = w["committed_int"]
    cold = w["cold_days"]
    b = [
        ("title", "Hydraulic test OS West, heating season 2026-27"),
        ("small", "%s, Network Planning. 9 October 2026. Prepared by %s. Supersedes the test of 6 October 2025." %
         (P.HEATCO, P.PEOPLE["planner"])),
        ("h", "1. Station"),
        ("p", "OS West feeds %s from the Lekstede transport line through two plate heat exchangers and three distribution "
              "pumps (two duty, one standby). Its design-day flow is %s m<super>3</super>/h, set by the exchangers at their "
              "design pressure drop." % (P.NETWORK, "{:,}".format(w["capacity"]))),
        ("h", "2. Design basis"),
        ("p", "The supply temperature follows the weather-compensated curve 90 - 1.2 x the outdoor temperature (&deg;C), "
              "between 70 and 90 &deg;C, so the network supplies 90 &deg;C at a daily mean of 0 &deg;C and below. The "
              "network was designed for 90/50 &deg;C at -10 &deg;C."),
        ("h", "3. Committed design-day flow"),
        ("p", "Every connection in service on 1 October 2026 is carried at its contracted capacity over 1.163 times the "
              "temperature difference read from its heat meter on the %d days of the 2025-26 meter year with a daily mean "
              "of 0 &deg;C or lower (CT-03 3.2)." % cold),
        ("table", [["Category", "Connections", "Contracted (kW)", "Design-day flow (m3/h)"],
                   ["Woningen", str(len(res)), "{:,}".format(sum(c["kw"] for c in res)), "%.0f" % fr],
                   ["Utiliteit", str(len(uti)), "{:,}".format(sum(c["kw"] for c in uti)), "%.0f" % fu],
                   ["Total", str(len(conns)), "{:,}".format(sum(c["kw"] for c in conns)), str(tot)]]),
        ("h", "4. Available design-day flow"),
        ("p", "Design-day flow available at OS West for connections from 1 October 2026: %s - %d = <b>%d m<super>3</super>"
              "/h</b>." % ("{:,}".format(w["capacity"]), tot, w["H"])),
        ("h", "5. Reporting"),
        ("p", "Heat taken by the connections is reported by gas year, 1 October to 1 October. Distribution losses are "
              "reported in the annual network report."),
        ("small", "This test states the design-day flow available at OS West on 1 October 2026; it does not test "
                  "connections that are not yet contracted."),
    ]
    write_pdf(path, "Hydraulic test OS West 2026-27", "%s Network Planning" % P.HEATCO_SHORT, b,
              "D:20261009143000+00'00'")


def concept(path, w):
    rows = [["Object", "Complex", "Woningen", "Ontwerpwarmteverlies (kW)"]]
    for bl in sorted(w["blocks"], key=lambda x: x["code"]):
        rows.append(["%s %d-%d" % (bl["street"], bl["from"], bl["to"]), bl["code"], str(bl["dwellings"]),
                     str(bl["prelim"])])
    b = [
        ("title", "Warmteverliesberekening Weidehaven aardgasvrij, concept"),
        ("small", "%s for %s. 27 March 2026. Concept for discussion; building data from the corporation's archive "
                  "drawings, site surveys to follow." % (P.CONSULT, P.CORP)),
        ("h", "Uitgangspunten"),
        ("p", "Design heat loss under NEN-EN 12831 at a design outdoor temperature of -10 &deg;C, indoor design "
              "temperatures 20 &deg;C (living rooms, kitchens), 22 &deg;C (bathrooms) and 15 &deg;C (stairwells heated), "
              "U-values from the construction year and the archive drawings, natural ventilation with mechanical "
              "extraction in kitchens and bathrooms, heating-up allowance on the living areas."),
        ("h", "Resultaten"),
        ("table", rows),
        ("p", "The figures will be revised after the site surveys planned for June and July 2026."),
    ]
    write_pdf(path, "Warmteverliesberekening Weidehaven concept", P.CONSULT, b, "D:20260327160000+00'00'")


def tariff(path):
    b = [
        ("title", "Tarievenblad warmte 2026"),
        ("small", "%s. Tariffs from 1 January 2026, within the maximum tariffs set by ACM for 2026. Amounts include "
                  "VAT." % P.HEATCO),
        ("h", "Kleinverbruik (contracted capacity up to 100 kW)"),
        ("table", [["Component", "Unit", "Amount (EUR)"],
                   ["Vastrecht", "per connection per year", "561.84"],
                   ["Meettarief", "per meter per year", "29.76"],
                   ["Warmte", "per GJ", "47.48"],
                   ["Huur afleverset", "per year", "176.04"]]),
        ("h", "Grootverbruik (contracted capacity above 100 kW)"),
        ("table", [["Component", "Unit", "Amount (EUR)"],
                   ["Vastrecht", "per connection per year", "1,284.00"],
                   ["Capaciteitstarief", "per contracted kW per year", "38.52"],
                   ["Warmte", "per GJ", "39.15"],
                   ["Meettarief", "per meter per year", "312.00"]]),
        ("h", "Eenmalige bijdragen"),
        ("p", "Aansluitbijdrage for a collective connection: on quotation. Disconnection: EUR 1,135.00 per connection."),
        ("small", "Questions about tariffs: klantenservice@stadswarmte-lekstede.nl"),
    ]
    write_pdf(path, "Tarievenblad warmte 2026", P.HEATCO, b, "D:20251201090000+00'00'")


def scope(path, w):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    n_ph = max(b["phase"] for b in w["blocks"])
    doc.add_heading("Aardgasvrij Weidehaven 2027-2028: scope of works", level=1)
    doc.add_paragraph("%s and %s. Version 1.2, 30 September 2026. Programme manager: %s." %
                      (P.CORP, P.HEATCO, P.PEOPLE["corp"]))
    doc.add_heading("1. Purpose", level=2)
    doc.add_paragraph("Weidehaven connects %d of its complexes in the Vogelbuurt to %s in %d phases between May 2027 and "
                      "September 2028. After a phase is connected its collective gas boiler rooms are taken out of "
                      "service." % (len(w["blocks"]), P.NETWORK, n_ph))
    doc.add_heading("2. Works in each complex", level=2)
    doc.add_paragraph("In each boiler room the gas boilers, burners and flues are removed and a %s delivery set is "
                      "installed: an indirect connection through a plate heat exchanger with its own heat meter, on the "
                      "block's existing heating installation." % P.HEATCO_SHORT)
    doc.add_paragraph("The block's distribution piping, risers and radiators remain in service. Hot tap water in the "
                      "dwellings stays individual (electric). No insulation or other envelope works are part of this "
                      "programme; Weidehaven's envelope programme for these complexes is planned after 2030.")
    doc.add_heading("3. Phasing", level=2)
    doc.add_paragraph("The phases and their planned connection dates are those of the schedule (Fasering, stand "
                      "30-09-2026). A phase is connected when every delivery set in it is in service.")
    doc.add_heading("4. Heat-load study", level=2)
    doc.add_paragraph("%s computes each complex's design heat loss under NEN-EN 12831. Revision 2 (18 September 2026) "
                      "follows the site surveys of June and July 2026 and replaces the concept of March 2026." % P.CONSULT)
    doc.add_heading("5. Gas", level=2)
    doc.add_paragraph("After a phase is connected %s removes the boiler rooms' gas connections. The gas the programme "
                      "takes off the grid is reported per phase as the boiler rooms' metered gas consumption over the gas "
                      "year 1 October 2025 to 1 October 2026." % P.GRIDOP)
    doc.add_heading("6. Tenants", level=2)
    doc.add_paragraph("Each complex's tenants are informed six months before its phase; the works in a boiler room take "
                      "one working day without heat, scheduled outside the heating season.")
    cp = doc.core_properties
    cp.author = P.PEOPLE["corp"]
    cp.last_modified_by = P.PEOPLE["corp"]
    cp.title = "Aardgasvrij Weidehaven scope of works"
    cp.created = dt.datetime(2026, 9, 30, 10, 0)
    cp.modified = dt.datetime(2026, 9, 30, 10, 0)
    cp.revision = 4
    cp.comments = ""
    doc.save(path)
    normalise_zip(path, "2026-09-30T08:00:00Z", app="Microsoft Office Word")


def write_all(F, w):
    procedure(F["procedure"])
    hydraulic(F["hydraulic"], w)
    concept(F["prelim"], w)
    tariff(F["tariff"])
    scope(F["scope"], w)
