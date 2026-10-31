"""The pack's documents: the programme's terms of reference, the camera supplier's firmware release notes, the Red 2026
service notice, HR's note on hours on service, the broker's reporting notes and the contract's annex on kilometres."""
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from common import scrub_pdf, set_mtime

PDF_DATE = "D:20261109091500+01'00'"

ST = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444")),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=10.5),
}


def _pdf(path, story, title, author):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator=author,
                            producer=author, invariant=1)
    doc.build(story)
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + PDF_DATE.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + PDF_DATE.encode() + b")", data)
    open(path, "wb").write(data)
    scrub_pdf(path)
    set_mtime(path)


def _table(rows, widths):
    t = Table([[Paragraph(str(c), ST["cell"]) for c in r] for r in rows], colWidths=[w * mm for w in widths])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def terms_pdf(path):
    s = [Paragraph("EMPRESA MUNICIPAL DE AUTOBUSES DE LORVEGA, S.A.", ST["small"]),
         Paragraph("Driver-Attention Programme 2027: terms of reference", ST["h1"]),
         Paragraph("Management Committee, issued for the committee of 24 November 2026. Safety and Training.",
                   ST["small"]), Spacer(1, 6)]
    s.append(Paragraph("1. Purpose", ST["h2"]))
    s.append(Paragraph(
        "The Driver-Attention Programme is a twelve-week course of in-cab observation, hazard-perception sessions and "
        "coaching for the drivers of a depot. It is run at the depots where drivers are not acting on the collision "
        "warnings the buses' driver-assistance cameras give them.", ST["p"]))
    s.append(Paragraph("2. The depots the programme takes", ST["h2"]))
    s.append(Paragraph(
        "The 2027 programme runs at every depot whose drivers, between 1 January and 31 October 2026, did not brake "
        "on genuine collision warnings at 1.3 times the fleet's rate or more. If no depot reaches that level, the "
        "programme does not run in 2027 and its budget returns to the training plan.", ST["p"]))
    s.append(Paragraph("3. Definitions", ST["h2"]))
    rows = [["Term", "Meaning"],
            ["Collision warning", "A forward-collision warning or a pedestrian and cyclist collision warning raised by a "
             "bus's driver-assistance camera. Lane-departure and headway warnings are not collision warnings."],
            ["Genuine collision warning", "A collision warning raised when a vehicle, a cyclist or a pedestrian was in the "
             "bus's path."],
            ["One warning", "One camera event."],
            ["Not braked on", "No service brake application within two seconds of the warning."],
            ["A depot's warnings", "The warnings raised on buses allocated to the depot on the day of the warning."],
            ["The fleet's rate", "The share of all depots' genuine collision warnings, taken together, that were not "
             "braked on."],
            ["A depot's rate", "The share of the depot's genuine collision warnings that were not braked on."],
            ["Dates and times", "Lorvega local time."]]
    s.append(_table(rows, [45, 125]))
    s.append(Paragraph("4. Timetable", ST["h2"]))
    s.append(Paragraph(
        "The Management Committee approves the depots on Tuesday 24 November 2026. Depot managers release drivers for "
        "the programme from Monday 11 January 2027, in groups of twelve, until every driver assigned to the depot on "
        "that date has completed it.", ST["p"]))
    _pdf(path, s, "Driver-Attention Programme 2027: terms of reference", "EMAL Safety and Training")


def codes_pdf(path):
    s = [Paragraph("FLEETVIEW TELEMATICS, FORWARD CAMERA INTEGRATION", ST["small"]),
         Paragraph("Forward camera firmware 2.3: release notes", ST["h1"]),
         Paragraph("Customer bulletin CB-2026-04, 21 April 2026. Distribution: fleet engineering and safety contacts, "
                   "EMAL Lorvega.", ST["small"]), Spacer(1, 6)]
    s.append(Paragraph("Rollout", ST["h2"]))
    s.append(Paragraph(
        "Firmware 2.3 is installed over the air when a vehicle next connects at its depot after the customer releases "
        "it. Vehicles fitted with the earlier camera module (hardware revision A) stay on firmware 1.9 and continue to "
        "report as before. Both versions report to the same platform and the same customer export from the day of "
        "installation.", ST["p"]))
    s.append(Paragraph("What changes in the warnings reported", ST["h2"]))
    for t in [
        "Warnings are reported under the platform's descriptive type codes: FWD_COLL for a forward collision warning, "
        "PED_COLL for a pedestrian and cyclist collision warning, LANE_DEP for a lane departure warning and HEADWAY for "
        "a headway warning, in place of FCW, PCW, LDW and HMW. The conditions that raise each warning do not change.",
        "The brake response is reported as a reaction time: the milliseconds from the warning to the driver's first "
        "service-brake application, measured over a capture of three seconds after the warning and left empty when the "
        "brake is not applied within it. Firmware 1.9 reports only whether the service brake was applied within two "
        "seconds of the warning, as yes or no.",
    ]:
        s.append(Paragraph("&bull; " + t, ST["p"]))
    s.append(Paragraph("Warning conditions (both versions)", ST["h2"]))
    s.append(Paragraph(
        "A forward collision warning is given when the time to collision with the vehicle ahead falls below 2.7 "
        "seconds. A pedestrian and cyclist collision warning is given when a pedestrian or a cyclist is detected in or "
        "entering the vehicle's path with a time to collision below 2.0 seconds. A headway warning is given when the "
        "time gap to the vehicle ahead stays below the configured headway; a lane departure warning when a lane "
        "marking is crossed without the indicator.", ST["p"]))
    _pdf(path, s, "Forward camera firmware 2.3: release notes", "FleetView Telematics")


def notice_pdf(path):
    s = [Paragraph("EMPRESA MUNICIPAL DE AUTOBUSES DE LORVEGA, S.A.", ST["small"]),
         Paragraph("Red 2026: the new bus network from Sunday 14 December 2025", ST["h1"]),
         Paragraph("Service notice for staff, Planning and Operations, 1 December 2025.", ST["small"]), Spacer(1, 6)]
    s.append(Paragraph("What changes", ST["h2"]))
    for t in [
        "Every stop takes a new five-digit code. Stop poles, the app and the timetable show the new codes from 14 "
        "December; the old codes stay on the poles until the end of January.",
        "Line 27 serves the Almadraba industrial estate, reaching it by the new bus-only underpass beneath the "
        "railway.",
        "Line 33 runs over the hill by the new Los Molinos link road, a bus-only road, instead of the Calle Huerta "
        "loop.",
        "Line 25 moves from the El Quiñón depot to Las Tenerías, with its buses and drivers.",
        "Line 40 will use the Vía Verde busway, with automatic bollard gates at its ends, once the city hands it over "
        "(expected in early summer 2026). Until then it keeps its present route.",
        "From Monday 2 March 2026 Calle Feria and the Plaza de Abastos become a shared space on market days (Monday to "
        "Saturday until 15:00). Lines 1, 3, 7 and 9 keep their route through it at walking pace.",
    ]:
        s.append(Paragraph("&bull; " + t, ST["p"]))
    s.append(Paragraph("Depots", ST["h2"]))
    rows = [["Depot", "Lines from 14 December 2025"],
            ["San Lázaro", "1, 3, 7, 9 and night line N1"], ["Hornacho", "12, 14, 27, 33 and night line N2"],
            ["Valdeolmos", "40, 41, 44, 46 and night line N3"], ["El Quiñón", "5, 16, 21 and night line N4"],
            ["Las Tenerías", "2, 8, 19, 23, 25 and night line N5"], ["La Ribera", "4, 10, 17, 29 and night line N6"],
            ["Santa Clara", "6, 11, 31, 35 and night line N7"]]
    s.append(_table(rows, [45, 125]))
    _pdf(path, s, "Red 2026 service notice", "EMAL Planning and Operations")


def payroll_txt(path):
    txt = (
        "EMAL HUMAN RESOURCES\r\n"
        "Duty and payroll returns: hours on service\r\n"
        "Issued 12 January 2026\r\n"
        "\r\n"
        "A driver's hours on service are the time the driver is logged on to a bus's ticket machine on a service line.\r\n"
        "Sessions on line 000 (positioning between the depot and the line) and on ESC (the driving school) are not\r\n"
        "service. A session counts in the week, Monday to Sunday, in which it starts. A driver's depot is the depot HR\r\n"
        "assigns the driver to on the date the session starts.\r\n"
        "\r\n"
        "Queries to Payroll (Nominas), extension 2214.\r\n"
    )
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(txt)
    set_mtime(path)


def insurance_pdf(path):
    s = [Paragraph("ARCOS & VELA CORREDURÍA DE SEGUROS", ST["small"]),
         Paragraph("EMAL fleet motor policy: reporting notes for the 2027 renewal", ST["h1"]),
         Paragraph("Policy FL-0331-LOR. Prepared for EMAL Finance, October 2026.", ST["small"]), Spacer(1, 6)]
    s.append(Paragraph("What the insurer asks for", ST["h2"]))
    s.append(Paragraph(
        "The insurer prices the 2027 renewal on each depot's own record rather than on the fleet as a whole. For each "
        "depot it asks for the at-fault collisions of January to October 2026 and the claims paid on them, set against "
        "the depot's kilometres in service over the same months.", ST["p"]))
    s.append(Paragraph("As agreed with the insurer", ST["h2"]))
    for t in [
        "An at-fault collision is an incident EMAL's incident review records as at fault, wholly (code A) or in part "
        "(code C). Code N is not at fault and code R is still under review; neither is reported.",
        "The claims paid on a collision are the amounts the insurer has paid on the claims arising from it, as at the "
        "October 2026 bordereau. Reserves are not reported.",
        "A collision belongs to the depot its bus was allocated to on the day.",
    ]:
        s.append(Paragraph("&bull; " + t, ST["p"]))
    s.append(Paragraph("Timetable", ST["h2"]))
    s.append(Paragraph(
        "EMAL Finance sends the figures to us by Friday 20 November 2026. We present them to the insurer with the "
        "renewal submission on 1 December and expect terms before the policy year ends on 31 December.", ST["p"]))
    _pdf(path, s, "Fleet motor policy: reporting notes", "Arcos & Vela Correduría de Seguros")


def annex_pdf(path):
    s = [Paragraph("AYUNTAMIENTO DE LORVEGA, CONTRATO DE GESTIÓN DEL SERVICIO DE AUTOBUSES URBANOS", ST["small"]),
         Paragraph("Annex IV: kilometres in service and the monthly return", ST["h1"]),
         Paragraph("English working translation for EMAL Finance.", ST["small"]), Spacer(1, 6)]
    s.append(Paragraph(
        "IV.1 The City pays the operator for the kilometres in service it runs each calendar month. The kilometres in "
        "service are the kilometres the buses ran on service trips: positioning runs to and from the depots are not "
        "service.", ST["p"]))
    s.append(Paragraph(
        "IV.2 The operator files a monthly service return with one row for each date, line and direction, giving the "
        "trips programmed, the trips operated and the kilometres run.", ST["p"]))
    s.append(Paragraph(
        "IV.3 Each depot's kilometres are reported for the lines it operates.", ST["p"]))
    _pdf(path, s, "Annex IV: kilometres in service", "Ayuntamiento de Lorvega")
