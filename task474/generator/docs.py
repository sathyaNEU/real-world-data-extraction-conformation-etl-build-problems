"""The pack's documents and workbooks: the program rules (PDF), the data notes (txt), the station register, the link
register and the county's count workbook (xlsx)."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate        # noqa: E402
from openpyxl import Workbook                                       # noqa: E402
from openpyxl.styles import Font                                    # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

SECTIONS = {"links": "2.1", "nox": "2.2", "line": "2.3", "fleet": "3.1"}
BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.5, spaceAfter=6)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)


def _doc(path, title, org):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.9 * inch, bottomMargin=0.9 * inch, title=title, author=org,
                          creator=org, producer=org, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.95 * inch, 0.55 * inch, "%s  |  %s" % (org, title))
        c.drawRightString(letter[0] - 0.95 * inch, 0.55 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def write_rules(path):
    title = "Air Corridor Program 2027: Program Rules"
    d, frame = _doc(path, title, W.PORT)
    s = [Paragraph("Air Corridor Program, 2027: Program Rules", TITLE),
         Paragraph("%s, %s. Adopted by the Board of Commissioners %s." % (W.PORT, W.DEPT, W.RULES_DATE), SUB),
         Paragraph("1. Purpose", HEAD),
         Paragraph("The Air Corridor Program funds, from the 2027 capital budget, zero-emission truck charging, idle "
                   "enforcement and roadside vegetation barriers along the roadway links around the port's terminals "
                   "that carry the most nitrogen oxides from on-road vehicles.", BODY),
         Paragraph("2. Designation", HEAD),
         Paragraph("2.1 <b>Links.</b> Every link in the port roadway link register.", BODY),
         Paragraph("2.2 <b>NOx per mile.</b> A link's program-year NOx is the NOx emitted by on-road vehicles "
                   "traveling the link from 1 October 2025 to 30 September 2026: the vehicle-miles each vehicle class "
                   "traveled on the link in those twelve months times the class's NOx emission rate in the 2026 "
                   "emission rate table, in metric tonnes. A link's NOx per mile is its program-year NOx divided by "
                   "its length in miles. The vehicle classes are passenger vehicles (FHWA classes 1 to 3), "
                   "single-unit trucks (4 to 7) and combination trucks (8 to 13).", BODY),
         Paragraph("2.3 <b>Designation.</b> A link whose NOx per mile is %.2f tonnes or more is designated for the "
                   "program." % W.LINE, BODY),
         Paragraph("3. The drayage fleet", HEAD),
         Paragraph("3.1 For the Board's sizing of the 2027 truck replacement grants beside the designations: the number "
                   "of drayage trucks registered with the port on the last day of each quarter of the program year (31 "
                   "December 2025, 31 March, 30 June and 30 September 2026) and how many of them have engines of model "
                   "year 2009 or older; and, on 30 September 2026, the same two numbers for each motor carrier. A "
                   "truck counts once, under the motor carrier of its latest registration.", BODY),
         Paragraph("4. Timetable", HEAD),
         Paragraph("Environmental Planning presents the designations with the 2027 capital budget.", BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_notes(path, n):
    F = W.FILES
    lines = ["Bayline Port Authority, Environmental Planning: data notes for the 2027 Air Corridor Program",
             "Compiled 2026-10-26.",
             "",
             "%s (%d rows)" % (F["stations"], n["stations"]),
             "  Hourly volumes at the state's continuous count stations in the metro area, October 2025 to",
             "  September 2026, as the state DOT publishes them: hour_ending 1 to 24, local standard time,",
             "  direction 1 (northbound or eastbound) and 5 (southbound or westbound). Classifying stations",
             "  report FHWA class groups 1-3, 4-7 and 8-13; the others report total volume (ALL). A day absent",
             "  for a station is a detector outage. See %s." % F["register"],
             "",
             "%s (%d rows)" % (F["dot"], n["dot"]),
             "  State DOT short-duration classification counts at port sites: one row per site, hour and",
             "  direction, hour starting, local time.",
             "",
             "%s" % F["county"],
             "  Harbor County Public Works classification counts, one sheet per site, 15-minute intervals.",
             "",
             "%s (%d rows)" % (F["consultant"], n["consultant"]),
             "  Classification counts at terminal access sites taken for the port by %s:" % W.CONSULTANT,
             "  one row per site, hour, lane and class (P passenger, SU single-unit, CU combination).",
             "",
             "%s" % F["links"],
             "  The port roadway link register: each link's length and the count programme and site that",
             "  counted it in the program year.",
             "",
             "%s" % F["rates"],
             "  NOx emission rates by vehicle class group for calendar year 2026 (Harbor County fleet, annual",
             "  average over all road types and speeds).",
             "",
             "%s (%d rows)" % (F["gates"], n["gates"]),
             "  The three container terminals' daily gate reports: trucks through the in-gate and the out-gate",
             "  and container moves, by terminal and day.",
             "",
             "%s (%d rows)" % (F["fleet"], n["fleet"]),
             "  The port's drayage truck registry: one row per registration, with the truck's VIN, motor carrier,",
             "  registration dates (registered_to is the last day in force, blank while in force), the engine",
             "  family, and the truck's model year (none on registrations taken before the 2024 form change).",
             "",
             "%s" % F["certs"],
             "  The Clean Truck Program's reference list of heavy-duty engine families and their certification.",
             "",
             "%s (%d rows)" % (F["complaints"], n["complaints"]),
             "  City 311 service requests about trucks on port-area streets.",
             "",
             "%s (%d rows)" % (F["no2"], n["no2"]),
             "  Hourly NO2 at the two near-port monitors, local standard time; qualifier AN = no data.",
             "",
             "Contact: Environmental Planning."]
    open(path, "w", encoding="utf-8", newline="\r\n").write("\n".join(lines) + "\n")


def write_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stations"
    ws.append(["Continuous count stations, Bayline metro area"])
    ws.append(["%s. Station list as of 1 July 2026." % W.DOT])
    ws.append([])
    ws.append(["Station ID", "Location", "Road type", "Classifies", "Lanes", "Factor group"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for s, (route, rt, aadt, su, cu, cls) in W.STATIONS.items():
        ws.append([s, route, rt.capitalize(), "Yes" if cls else "No", 6 if rt == "freeway" else 4, "Urban"])
    for col, w in zip("ABCDEF", (11, 28, 11, 11, 7, 13)):
        ws.column_dimensions[col].width = w
    wb.save(path)


def write_links(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Links"
    ws.append(["Port roadway link register, program year October 2025 to September 2026"])
    ws.append([])
    ws.append(["Link ID", "Link", "Road type", "Length (mi)", "Count programme", "Count site", "Terminal access"])
    for c in ws[3]:
        c.font = Font(bold=True)
    rng = __import__("numpy").random.default_rng(W.SEED + 21)
    prog = {"dot": "State DOT", "county": "Harbor County", "consultant": W.CONSULTANT}
    for k, (name, rt, *_r) in W.LINKS.items():
        ws.append([k, name, rt.capitalize(), round(float(rng.uniform(.35, 2.4)), 2), prog[W.PROGRAM[k]], P.SITE[k],
                   W.TERMINALS[W.ACCESS[k][0]][0] if k in W.ACCESS else None])
    for col, w in zip("ABCDEFG", (8, 40, 10, 11, 22, 13, 40)):
        ws.column_dimensions[col].width = w
    wb.save(path)


def write_county(path, tables):
    wb = Workbook()
    wb.remove(wb.active)
    for k, (site, rows) in sorted(tables.items(), key=lambda t: t[1][0]):
        ws = wb.create_sheet(site)
        d1, d2 = P.DIRS[W.LINKS[k][1]]
        ws.append([COUNTY_TITLE])
        ws.append(["Vehicle classification count, site %s: %s" % (site, W.LINKS[k][0])])
        ws.append(["Count began %s 00:00, 48 hours" % rows[0][0].isoformat()])
        ws.append([])
        ws.append(["Date", "Time", "%s Passenger" % d1, "%s Single Unit" % d1, "%s Combination" % d1,
                   "%s Passenger" % d2, "%s Single Unit" % d2, "%s Combination" % d2])
        for c in ws[5]:
            c.font = Font(bold=True)
        for d, t, v in rows:
            ws.append([d.strftime("%m/%d/%Y"), t] + v)
        ws.column_dimensions["A"].width = 11
    wb.save(path)


COUNTY_TITLE = "Harbor County Public Works, Traffic Engineering"


def write_certs(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Engine families"
    ws.append(["Engine family", "Manufacturer", "Model year", "Displacement (L)", "NOx standard (g/bhp-hr)",
               "Certified by"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    for col, w in zip("ABCDEF", (14, 24, 11, 15, 22, 12)):
        ws.column_dimensions[col].width = w
    wb.save(path)
