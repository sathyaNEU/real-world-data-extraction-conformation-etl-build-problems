"""task170 documents: Human Factors' forecast conventions, the ETCS rollout plan, the safety desk's reporting guidance
and Fleet Engineering's acceptance note (PDF), and the data dictionary (text). Their text is held here as data so
checks.py can quote it and verify.py can read it back."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import A4                                                  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as C            # noqa: E402
import postprocess as PP      # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Serif", "liberation/LiberationSerif-Regular.ttf"), ("Serif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("Sans", "liberation/LiberationSans-Regular.ttf"), ("Sans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1b1b")
GREY = colors.HexColor("#555555")


def _d(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


# ------------------------------------------------------------------ Human Factors' forecast conventions
COUNT_PIN = ("The forecast counts the train data entry errors the safety desk will record against the drivers on the "
             "six Phase 4 depots' rosters at 31 October 2026, in each depot's first twelve months on ETCS: from its "
             "go-live date in the rollout plan, that day included, to the day before the first anniversary of it. A "
             "train data entry error is a report in category TDE; a report withdrawn on review is not an error, and a "
             "report the desk links to an earlier report is the same error.")
WORK_PIN = ("After go-live each Phase 4 driver works the same turns as on the duties the driver worked from January to "
            "October 2026, at the same monthly number of cab activations, and each cab activation becomes one ETCS "
            "Start of Mission. A cancelled duty was not worked, and a re-issued duty replaces its earlier issue.")
ROSTER_PIN = ("A driver is counted at the depot on whose roster the driver stands at 31 October 2026; Resourcing plans "
              "no change to the six depots' establishments before go-live.")
CALL_PIN = "The forecast is the expected number of errors, reported to the nearest 250."

CONVENTIONS = [
    ("1. Purpose", [
        "The Phase 4 safety case to the %s carries a forecast of the train data entry errors the safety desk will "
        "record against Phase 4 drivers in each depot's first twelve months on ETCS. The Office's monitoring "
        "condition for Phases 1 to 3 asks that every recorded error is debriefed with the driver, and the forecast "
        "sizes the debriefing the six depots' driver managers plan for." % C.REGULATOR,
        "These conventions govern the forecast and the working files behind it."]),
    ("2. What is counted", [COUNT_PIN, CALL_PIN]),
    ("3. Drivers and turns", [ROSTER_PIN, WORK_PIN]),
]

ROLLOUT = [
    ("1. Scope", [
        "%s is fitting ETCS Level 2 route by route, with the lineside signals taken out as each route goes live. "
        "Each depot's drivers convert to ETCS before its go-live, and from go-live every train the depot's drivers "
        "work runs under ETCS." % C.OPERATOR]),
    ("2. Phases and go-live dates", ["Table 1 gives each depot's ETCS go-live date. Phases 1 to 3 fitted the "
                                     "suburban and intercity routes; Phase 4 fits the rural routes."]),
    ("Table 1", []),
    ("3. Phase 4", [
        "The six Phase 4 depots go live from February to June 2027 on the dates in Table 1. Their units, the "
        "Class 461 fleet, are fitted in the Phase 4 fitment programme. The Phase 4 diagrams do not change at "
        "go-live."]),
]


def rollout_table():
    rows = [("Phase", "Depot", "Code", "ETCS go-live")]
    for code, name, ph, gl in C.DEPOTS:
        rows.append(("Phase %d" % ph, name, code, _d(gl)))
    return rows


GUIDE = [
    ("1. Categories", [
        "TDE: train data entry at Start of Mission, a wrong value entered and confirmed in the train data (train "
        "category, length, maximum speed, brake percentage, axle load category, running number or loading gauge). "
        "LTR: a level transition the driver did not handle correctly. BRK: an ETCS brake intervention (overspeed, "
        "end of authority, release speed). TRK: a fault in trackside equipment. RBC: a fault in the radio block "
        "centre or the train radio."]),
    ("2. Reports", [
        "Reports reach the desk from drivers, signallers, the fleet data check and the recorder downloads. Each "
        "report is logged on the register with the time it was received, the reporter, the unit and the staff "
        "number of the driver of the train. The SoM Ref is the event reference the driver's display gives at Start "
        "of Mission: a driver's report carries it where the driver noted it, and the fleet data check carries it "
        "always."]),
    ("3. Linked and withdrawn reports", [
        "Where a driver and a signaller report the same event, or the fleet data check finds an error already "
        "reported, the desk links the later report to the first in Linked To; a linked report is not a second "
        "event. A report found on review not to describe an event is withdrawn and stays on the register with "
        "status Withdrawn."]),
]

ACCEPT_PIN = ("A unit is accepted for ETCS service when both of its driving vehicles carry accepted equipment. Until "
              "a vehicle's equipment is accepted, the programme's planned acceptance date is the date on which it "
              "will be.")
ACCEPT = [
    ("1. Fitment", [
        "Each Class 461 unit has two driving vehicles, the A-end and the B-end. The Phase 4 fitment programme fits "
        "ETCS on-board equipment to each driving vehicle at the works; the equipment is accepted after dynamic "
        "testing."]),
    ("2. Acceptance for service", [ACCEPT_PIN]),
]


def _styles():
    base = ParagraphStyle("b", fontName="Serif", fontSize=10.5, leading=14, textColor=INK, spaceAfter=6)
    head = ParagraphStyle("h", fontName="Serif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle("t", fontName="Sans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4)
    sub = ParagraphStyle("s", fontName="Sans", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=10)
    small = ParagraphStyle("f", fontName="Sans", fontSize=8.5, leading=11, textColor=GREY, spaceBefore=10)
    return base, head, title, sub, small


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pdf(path, title, sub, sections, foot=None, table=None, table_after=None, issued=None, author="", widths=None):
    base, head, tstyle, sstyle, small = _styles()
    story = [Paragraph(_esc(title), tstyle)]
    if sub:
        story.append(Paragraph(_esc(sub), sstyle))
    for h, paras in sections:
        if h and h != table_after:
            story.append(Paragraph(_esc(h), head))
        for p in paras:
            story.append(Paragraph(_esc(p), base))
        if table is not None and h == table_after:
            story.append(Paragraph(_esc(h + ". ETCS go-live by depot"), head))
            t = Table(table, hAlign="LEFT", colWidths=widths, repeatRows=1)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Sans-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Sans", 8.5),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(Spacer(1, 4))
            story.append(t)
            story.append(Spacer(1, 6))
    if foot:
        story.append(Paragraph(_esc(foot), small))

    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Sans", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, title)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    stamp = ("D:%04d%02d%02d%02d%02d%02d+00'00'" % (issued.year, issued.month, issued.day, 9, 40, 0)).encode()
    PP.normalize_pdf(path, stamp, stamp)


def write_conventions(path):
    _pdf(path, "Phase 4 ETCS Safety Case: Forecast Conventions",
         "%s, Human Factors. Issued 3 November 2026. Kate Potter, Human Factors Lead." % C.OPERATOR,
         CONVENTIONS, issued=dt.date(2026, 11, 3), author="Kate Potter",
         foot="Questions on these conventions go to Human Factors.")


def write_rollout(path):
    _pdf(path, "ETCS Rollout Plan 2024 to 2027",
         "%s, ETCS Programme. Revision 7, 14 September 2026. Charlie Coles, ETCS Programme Manager." % C.OPERATOR,
         ROLLOUT, table=rollout_table(), table_after="Table 1", issued=dt.date(2026, 9, 14), author="Charlie Coles",
         widths=[22 * mm, 45 * mm, 18 * mm, 40 * mm], foot="Revision 7 moves the Phase 4 go-live dates to 2027.")


def write_guidance(path):
    _pdf(path, "Safety Desk: ETCS Incident Reporting Guidance",
         "%s, Safety Desk. Issued 2 February 2024, revised 6 January 2026. Gillian Armstrong, Safety Desk Manager." % C.OPERATOR,
         GUIDE, issued=dt.date(2026, 1, 6), author="Gillian Armstrong")


def write_acceptance(path):
    _pdf(path, "Class 461 ETCS Fitment: Acceptance for Service",
         "%s, Fleet Engineering. Issued 18 August 2026." % C.OPERATOR, ACCEPT, issued=dt.date(2026, 8, 18),
         author="Fleet Engineering")


DICT = """DATA DICTIONARY, PHASE 4 ETCS SAFETY CASE (Human Factors, assembled 9 November 2026)

obr_start_of_mission_log_2024-03_2026-10.csv  On-board recorder downloads: one row per ETCS Start of Mission on the
  Phase 1 to 3 fleet (Class 384), 4 March 2024 to 31 October 2026
  som_ref     event reference the driver's display gives at Start of Mission
  obr_utc     recorder time (UTC)
  unit        unit number
  cab         driving cab used (A or B end)
  driver_id   staff number entered at Start of Mission (a fleet technician's for a test)
  som_type    SVC service; DPT depot, preparing a train before it goes out; TST test by a fleet technician

safety_desk_register_2024-2026.xlsx  Safety desk register: one row per report received, March 2024 to October 2026
  Report No, Received (when the report was logged), Reporter, Category (see the reporting guidance), Depot (the
  driver's depot), Staff No (the driver's staff number), Unit, SoM Ref, Linked To (the first report of the same event),
  Status (Closed, Open or Withdrawn), Summary

driver_roster_2026-10-31.xlsx  Resourcing: every driver on a depot roster at 31 October 2026, all fourteen depots
  Staff No, Depot, Grade, Link, Contract, Date of Birth, Qualified (date qualified as a driver)

staff_number_crosswalk.csv  Resourcing: a driver who transfers is issued a staff number in the new depot's block
  old_staff_no, new_staff_no, effective, reason

phase4_duty_records_2026.csv  Crew management: one row per duty rostered for a Phase 4 depot driver, January to
  October 2026
  duty_date, staff_no, depot, duty_no
  cab_activations   the times the driver opened a cab desk to drive on the duty
  status            Worked or Cancelled
  issue             a duty re-issued after a timetable change carries issue 2

fleet_allocation_2027.csv  Fleet: Class 461 units allocated to each Phase 4 depot for the 2027 timetable
  unit, depot, allocated_from

etcs_fitment_works_records.xlsx  Fitment Programme Office: one row per Class 461 driving vehicle in the Phase 4
  fitment programme
  Vehicle, Unit (the vehicle's unit in the fitment programme), End (A or B), Works In, Works Out, Dynamic Test,
  Accepted, Planned Acceptance, Status (Accepted, In works or Planned)

unit_formations_2026-10-31.csv  Fleet Engineering: Class 461 unit formations at 31 October 2026
  unit, vehicle_a_end, vehicle_b_end, class

unit_renumbering_register.csv  Fleet Engineering: Class 461 units renumbered
  old_unit, new_unit, effective, reason

punctuality_by_depot_2024-2026.xlsx  Performance and Planning: trains planned and the public performance measure
  (per cent of trains arriving within five minutes of the timetable) by depot and month

depot_weather_daily_2024-2026.csv  Daily weather at each depot: maximum and minimum temperature (C), rain (mm),
  frost (Y where the minimum fell below zero)

etcs_rollout_plan_2024-2027.pdf  ETCS Programme
phase4_safety_case_conventions.pdf  Human Factors
safety_desk_reporting_guidance.pdf  Safety Desk
fleet_etcs_acceptance_note.pdf  Fleet Engineering
"""


def write_dict(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(DICT.replace("\n", "\r\n"))
