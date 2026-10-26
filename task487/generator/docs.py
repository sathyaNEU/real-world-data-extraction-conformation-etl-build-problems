"""The pack's documents: the Provincial Energy Board's Directive 17 on the release-event return and levy, and the
Kesmere field data team's notes on the exports."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.8, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10, alignment=0)

# the bands of a year's release-event methane, tonnes, and the next year's levy for each battery (Canadian dollars)
BANDS = [("A", 0, 36, 330), ("B", 36, 48, 640), ("C", 48, 60, 950), ("D", 60, 72, 1360), ("E", 72, None, 2000)]


def band(t):
    for b, lo, hi, levy in BANDS:
        if t >= lo and (hi is None or t < hi):
            return b, levy
    raise ValueError(t)


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=org, subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(20 * mm, 10 * mm, org + "  |  " + title)
        c.drawRightString(letter[0] - 20 * mm, 10 * mm, "%d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def P(text, style=BODY):
    return Paragraph(text, style)


def _table(rows, widths=None, size=8.2):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def directive(path):
    bands = [["Band", "Release-event methane in the year", "Levy for the following year, CAD for each battery"]]
    for b, lo, hi, levy in BANDS:
        rng = ("under %d t" % hi) if lo == 0 else ("%d t and over" % lo if hi is None else "%d t to under %d t" % (lo, hi))
        bands.append([b, rng, format(levy, ",")])
    s = [P("Directive 17: Release-Event Methane Return and Levy", T),
         P("Provincial Energy Board. 2025 edition, issued 14 March 2025, in force for the 2025 and later calendar years. "
           "Replaces the 2022 edition.", SMALL),
         P("1. Application", H),
         P("This directive applies to every licensee of an oil battery with atmospheric storage tanks. Each licensee files "
           "a return of its release events for each calendar year by 31 March of the following year, and the Board levies "
           "the licensee for the following year on the release-event methane in the return. Years and days in this "
           "directive are calendar years and days in local time."),
         P("2. Release events", H),
         P("2.1 A release event is tank vapour vented to the atmosphere through an open thief hatch, through a vapour "
           "combustor whose pilot is out, or through a tank pressure-vacuum relief valve that has not reseated."),
         P("2.2 A relief valve that lifts at its set pressure and reseats is routine venting and not a release event."),
         P("3. Schedule A: the release events", H),
         P("3.1 The return covers each release event found at the licensee's batteries in the calendar year, and gives "
           "for each event its battery, kind, start, closure and vented methane."),
         P("3.2 An event starts when its venting began. A relief valve that did not reseat starts at the tank pressure "
           "alarm at which it lifted, where the battery's tank pressure is telemetered. Where the licensee's records do "
           "not date an event's start, the return takes the start at its expected value given those records. An event "
           "closes when it was closed at the battery."),
         P("3.3 An event vents its battery's tank vapour methane in each hour from its start to its closure. On each day "
           "that is the day's oil production, times the flash gas-oil ratio of the battery's latest tank vapour analysis "
           "taken on or before the day, times that analysis's methane mole fraction, times 0.6785 kg a cubic metre "
           "(15 C and 101.325 kPa), spread evenly over the day's 24 hours."),
         P("3.4 The return's release-event methane is the sum of its events' vented methane, in tonnes."),
         P("4. The levy", H),
         P("The release-event methane in a calendar year's return sets the licensee's band for the following year (Table "
           "1). The levy for that year is the band's rate for each oil battery the licensee holds at the start of the "
           "year."),
         _table(bands, widths=[14 * mm, 56 * mm, 62 * mm]),
         Spacer(1, 6),
         P("5. Schedule B: fugitive emissions", H),
         P("5.1 Schedule B reports the licensee's fugitive emissions at its batteries and the wells that produce to them. "
           "It is not levied."),
         P("5.2 A leak is gas escaping from one component of a battery, or of a well producing to it, from when it "
           "starts until the component is repaired. An optical gas imaging (OGI) survey of the battery finds it, and a "
           "later survey that finds it again before it is repaired has found the same leak. A leak vents at the methane "
           "rate measured when it was first found, from the start of the day of the battery's last survey before it was "
           "first found until the start of the day it was repaired, or to the end of the year if it was not repaired in "
           "the year."),
         P("5.3 Schedule B gives each battery's fugitive methane in each half of the year, January to June and July to "
           "December, in tonnes."),
         P("6. Filing", H),
         P("The return is filed through the Board's portal in the Board's event schema, one row for each release event, "
           "with the year's release-event methane, its band and Schedule B. The Board may ask a licensee for the records "
           "behind any figure in its return."),
         Spacer(1, 8),
         P("Provincial Energy Board, Upstream Emissions Branch. Questions on this directive: emissions.returns@peb.example",
           SMALL)]
    _pdf(path, "Directive 17: Release-Event Methane Return and Levy", s, "Upstream Emissions Branch",
         "Provincial Energy Board")


NOTES = """KESMERE FIELD: DATA NOTES FOR THE 2026 RELEASE-EVENT RETURN
Vennholt Energy Ltd., production data team. Exports pulled 8 to 13 January 2027.

Local time is UTC-7 until 8 March 2026 and UTC-6 from then on: the province kept its
clocks at UTC-6 when they would have gone back on 1 November 2026.

battery_register_20270108.csv
  One row per tank battery as at 8 January 2027: licence, route, visit schedule, tanks,
  tank pressure telemetry, vapour combustor. BT-0907 was re-licensed as BT-0907A on
  17 August 2026 (new tanks); systems that keyed it by code changed on that day.

route_app_visits_20251215_20260630.csv
  The route app, the lease operators' visit app until it was retired on 30 June 2026.
  One row per site visit as the lease operator tapped in and out, local time.
  Pulled from 15 December 2025.

checkin_app_visits_20260615_20270112.jsonl
  The check-in app, in use from 1 July 2026 (routes R03 and R09 from 15 June, beside the
  route app until 30 June). One record per check-in: geofence entry and exit, or a
  manual check-in when the phone had no fix. Times are local with their UTC offset.
  Sites are in checkin_app_sites.csv.

release_event_register_2026.xlsx
  The office's register of release events found in 2026, imported from the lease
  operators' event reports in each app; Found and Closed keep the app's time format.

scada_alarm_journal_20251215_20270112.csv
  SCADA host journal for the telemetered batteries: tank pressure points (PIT-101, high
  alarm at the relief valves' set pressure) and RTU communications. Time is UTC.

battery_daily_production_20251215_20261231.csv
  Daily production by battery (production accounting). Volumes at 15 C and 101.325 kPa;
  gas in thousands of cubic metres; HoursOn is the battery's producing hours.

tank_vapour_analyses_2025_2026.xlsx
  Laboratory results for tank vapour (flash) samples: flash gas-oil ratio and composition
  in mole per cent.

maintenance_work_orders_2026.csv
  The maintenance system's work orders completed in 2026, numbered as they were raised.
  Reference is the notification the order was raised on (N, or EHS for the leak
  program), its maintenance plan (PM), or the contractor's field ticket (FT).

ldar_surveys_2025_2026.csv
  The camera crews' OGI sessions at the batteries and the wells producing to them,
  September 2025 to December 2026: the points each session screened and the leaks it
  tagged.

ldar_leak_tracker_20270112.xlsx
  The leak tracker as at 12 January 2027: one row per tag hung at a survey, with the
  camera's methane rate estimate. Received is the day the tag reached the tracker from
  the crew's tablet; Closed is the day the tag was closed against its work order. A
  repair that needs a shutdown waits for the battery's next one.

hauler_load_tickets_2026.csv
  Kesmere Fluid Haulers' load tickets from the batteries.

sales_gas_meter_statements_2026.csv
  Monthly statements for the field's three sales gas meters.
"""


def notes(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(NOTES)
