"""The pack's documents: the Crane Replacement Program's placement rules, the Harbor Master's General Directions,
the data dictionary for the Terminal Equipment extracts, and the export manifest."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P      # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1f24")
GREY = colors.HexColor("#59606a")
NAVY = colors.HexColor("#1f3b5c")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.6, leading=14.4, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=9.8, leading=13.0, textColor=INK, spaceAfter=5)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.4, leading=10.6, textColor=INK)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=15, leading=19, textColor=NAVY, spaceAfter=3)
H1S = ParagraphStyle("h1s", fontName="LiberationSans", fontSize=9.2, leading=12.4, textColor=GREY, spaceAfter=12)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=9,
                    spaceAfter=4)

RULES = [
    ("1. Purpose", [
        "1.1 The Crane Replacement Program renews the Authority's ship-to-shore cranes in orders that the Board of "
        "Commissioners awards. These rules decide the terminal at which the cranes of an order are placed. They do not "
        "decide which cranes are retired, which the Director of Terminal Equipment proposes with the placement.",
    ]),
    ("2. Placement", [
        "2.1 The cranes of an order are placed together at the one terminal where they would have saved the most berth "
        "hours on the large-vessel calls of the last closed fiscal year.",
        "2.2 The Director of Terminal Equipment brings the placement to the Board with the order and with each "
        "terminal's berth hours saved.",
    ]),
    ("3. Definitions", [
        "3.1 A call is one vessel's stay alongside one terminal's berths, from all fast to let go.",
        "3.2 A large vessel is a container vessel whose nominal capacity in the Authority's vessel register is 10,000 "
        "TEU or more.",
        "3.3 A call belongs to the fiscal year in which its first container move falls, in Eastern time. The "
        "Authority's fiscal year runs from 1 July to 30 June; fiscal year 2026 is 1 July 2025 to 30 June 2026.",
        "3.4 A call's cargo work runs from its first container move to its last, on whichever cranes worked it.",
        "3.5 A replacement set is taken to complete a call's cargo work, starting when it started, in four fifths of "
        "the time the call's cargo work took.",
        "3.6 The berth hours a replacement set would have saved on a call are the hours by which the call would have "
        "been shorter had its cargo work taken four fifths of the time it took.",
        "3.7 A terminal's berth hours saved are the sum over its large-vessel calls of the fiscal year, added "
        "unrounded; the total is reported in whole hours.",
    ]),
    ("4. Records", [
        "4.1 The program uses the Authority's records as kept.",
    ]),
]
SCHEDULE_A = [
    "A.1 The 2027 order is for six ship-to-shore cranes, for delivery in 2027 and 2028.",
    "A.2 The 2027 order is placed on fiscal year 2026, the year ending 30 June 2026.",
    "A.3 The Board awards the 2027 order at its meeting of 27 October 2026; the supplier's contract names the "
    "receiving terminal.",
]
CONTROL = [["Revision", "Adopted", "Resolution", "Change"],
           ["1", "12 March 2019", "2019-07", "First issue: Ore Dock, Pine Neck, Gannet Point and Halyard"],
           ["2", "14 May 2024", "2024-31", "Saltworks and Millrace added after their purchase"],
           ["3", "9 June 2026", "2026-22", "Placement on berth hours saved; Schedule A, the 2027 order"]]

DIRECTIONS = [
    ("1. Application and terms", [
        "1.1 These Directions are given by the Harbor Master under the Port of Ternmouth Harbor Ordinance and apply to "
        "every vessel within the harbor limits, including the Salt River to the head of navigation at Millrace.",
        "1.2 In these Directions, local time is Eastern time as kept in Ternmouth; length is length overall; draft is "
        "the vessel's deepest draft, forward or aft.",
        "1.3 A vessel's master remains responsible for the safe navigation of the vessel at all times.",
    ]),
    ("2. Reporting", [
        "2.1 Vessels shall report to Ternmouth Harbor Control on VHF channel 12 one hour before reaching the pilot "
        "boarding area, on leaving a berth, on passing Salt Point, and on anchoring or weighing anchor.",
        "2.2 Harbor Control keeps a listening watch on VHF channel 16 and broadcasts navigational warnings on channel "
        "12 at 0300, 0900, 1500 and 2100 local time.",
    ]),
    ("3. Pilotage", [
        "3.1 Pilotage is compulsory for vessels of 300 gross tons and more, and for every vessel carrying dangerous "
        "goods in bulk.",
        "3.2 Pilots board and land in the pilot boarding area, two nautical miles south of Ternmouth Light.",
        "3.3 Arrivals: the agent shall give the pilot station an estimated time of arrival 24 hours ahead and confirm "
        "it four hours ahead.",
        "3.4 Sailings: the agent shall notify the pilot station when the vessel is ready to sail. A pilot is not "
        "provided at less than one hour's notice. The pilot station gives the vessel its sailing time.",
        "3.5 A shift between berths is booked with the pilot station as a sailing.",
    ]),
    ("4. Speed", [
        "4.1 The speed limit is 10 knots through the water in the harbor and 8 knots in the Salt River above Salt "
        "Point. Vessels shall reduce speed when passing berths, dredgers and small craft.",
    ]),
    ("5. Anchorages", [
        "5.1 Anchorages Alpha, Bravo and Charlie lie in the outer harbor. Vessels of 1,250 feet in length or more "
        "anchor in Charlie only.",
        "5.2 The Lower Reach anchorage in the Salt River is for vessels of less than 700 feet in length.",
    ]),
    ("6. Tugs", [
        "6.1 Vessels of 900 feet in length or more berth and unberth with at least two tugs, and vessels of 1,250 feet "
        "or more with at least three. Vessels berthing at Saltworks or Millrace take one tug more than this table.",
    ]),
    ("7. Weather", [
        "7.1 No vessel of 900 feet in length or more shall berth or unberth when the sustained wind at the berth "
        "exceeds 30 knots, or move in the harbor when visibility is less than one nautical mile.",
    ]),
    ("8. The harbor: vessels of 1,250 feet or more", [
        "8.1 Vessels of 1,250 feet in length or more shall berth and unberth only between 0600 and 2000 local time.",
        "8.2 Two such vessels shall not move in the main channel at the same time.",
    ]),
    ("9. The Salt River", [
        "9.1 The Salt River channel is maintained to 46 feet below mean lower low water from Salt Point to the "
        "Millrace turning basin.",
        "9.2 A vessel with a draft of 41 feet or more shall pass Salt Point only between one hour thirty minutes before "
        "and thirty minutes after the time of high water at Salt Point, as predicted in the Authority's tide "
        "predictions.",
        "9.3 Passage times at the river speed limit are: from the Saltworks berths to Salt Point, 1 hour 50 minutes; "
        "from the Millrace berths to Salt Point, 2 hours 40 minutes. The pilot station sets the sailing time of a "
        "vessel to which 9.2 applies on these passage times.",
        "9.4 Vessels of more than 800 feet in length shall not meet or overtake between Salt Point and the Saltworks "
        "reach.",
    ]),
    ("10. Dangerous goods and bunkering", [
        "10.1 Vessels shall declare dangerous goods to Harbor Control 24 hours before arrival. Bunkering alongside a "
        "container berth requires the terminal's consent and Harbor Control's permission, and stops when a vessel "
        "moves on an adjacent berth.",
    ]),
    ("11. Pollution and incidents", [
        "11.1 Any discharge, collision, grounding, contact with a berth or crane, or fire shall be reported to Harbor "
        "Control at once on VHF channel 12 and in writing within 24 hours.",
    ]),
]
DIR_CONTROL = [["Edition", "In force", "Change"],
               ["2023", "1 March 2023", "Consolidated edition"],
               ["2024", "1 April 2024", "Saltworks and Millrace brought within the harbor limits; section 9"],
               ["2025", "1 May 2025", "8.1 and 9.2 restated; 6.1 tug table for the river berths"]]


def _doc(path, title, footer, author):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.6)
        canvas.drawString(0.95 * inch, 0.62 * inch, footer)
        canvas.drawRightString(letter[0] - 0.95 * inch, 0.62 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.85 * inch, bottomMargin=0.95 * inch, title=title,
                          author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths):
    data = [[Paragraph(str(v), CELLB if i == 0 else CELL) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa3ad")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e3e9f0")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def write_rules(path):
    d, frame = _doc(path, "Crane Replacement Program: Placement Rules",
                    "Ternmouth Port Authority  |  Crane Replacement Program  |  Placement Rules, Revision 3",
                    "Ternmouth Port Authority")
    story = [Paragraph("Crane Replacement Program: Placement Rules", H1),
             Paragraph("Ternmouth Port Authority, Terminal Equipment. Revision 3, adopted by the Board of Commissioners "
                       "on 9 June 2026 (Resolution 2026-22), with Schedule A. Owner: Director, Terminal Equipment.",
                       H1S)]
    for head, paras in RULES:
        story.append(Paragraph(head, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    story.append(Paragraph("Schedule A. The 2027 order", H2))
    for p in SCHEDULE_A:
        story.append(Paragraph(p, BODY))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Document control", H2))
    story.append(_table(CONTROL, [1.0 * inch, 1.15 * inch, 0.95 * inch, 3.4 * inch]))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_directions(path):
    d, frame = _doc(path, "Port of Ternmouth: Harbor Master's General Directions 2025",
                    "Port of Ternmouth  |  Harbor Master's General Directions  |  2025 edition, in force 1 May 2025",
                    "Office of the Harbor Master, Port of Ternmouth")
    story = [Paragraph("Port of Ternmouth: Harbor Master's General Directions", H1),
             Paragraph("2025 edition, in force from 1 May 2025 until replaced. Issued by the Office of the Harbor "
                       "Master, Ternmouth Port Authority, under the Port of Ternmouth Harbor Ordinance. Notices to "
                       "Mariners issued since this edition are listed on the Authority's website.", H1S)]
    for head, paras in DIRECTIONS:
        story.append(Paragraph(head, H2))
        for p in paras:
            story.append(Paragraph(p, SMALL))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Editions", H2))
    story.append(_table(DIR_CONTROL, [0.9 * inch, 1.2 * inch, 4.4 * inch]))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def rules_text():
    out = []
    for _, paras in RULES:
        out.extend(paras)
    return out + SCHEDULE_A


def directions_text():
    out = []
    for _, paras in DIRECTIONS:
        out.extend(paras)
    return out


DICTIONARY = """TERNMOUTH PORT AUTHORITY - TERMINAL EQUIPMENT
Data dictionary for the Terminal Equipment extracts pulled 5 and 6 October 2026
Maintained by Vessel Operations (T. Abbott). Issue 8, 6 October 2026.

Times: the Authority's terminal operating system, maintenance system and the pilot station's dispatch system
record Eastern time (EST/EDT, the clock on the wall at the terminal). The SRT systems, the AIS pipeline and
anything ending _UTC record UTC. The tide predictions carry their own time zone in their header.

---------------------------------------------------------------------------------------------------------------
tos_crane_activity_2026.csv
Authority terminal operating system, crane activity extract. Ore Dock, Pine Neck, Gannet Point and Halyard.
One row per ship-to-shore crane, vessel visit and clock hour in which the crane made at least one container
move. Hours run 23 June 2025 to 6 July 2026.
  TERMINAL        ORD Ore Dock, PNC Pine Neck, GNP Gannet Point, HLY Halyard
  VISIT_ID        vessel visit (see tos_vessel_visits_2026.csv)
  CRANE_ID        crane number as painted on the crane (see sts_crane_register.csv)
  HOUR_START      clock hour, Eastern time. On 2 November 2025 the 01:00 hour occurs twice and each
                  occurrence has its own rows, the first occurrence first.
  MOVES           container moves in the hour; a twin lift is one move
  HATCH_COVERS    hatch covers lifted or landed in the hour (not counted in MOVES)
  FIRST_MOVE      time of the crane's first container move on the visit within the hour
  LAST_MOVE       time of the crane's last container move on the visit within the hour
  BAY_FROM        lowest 40-foot bay the crane worked in the hour (even bay numbers, 02 at the bow)
  BAY_TO          highest 40-foot bay the crane worked in the hour

tos_vessel_visits_2026.csv
Authority terminal operating system, vessel visits at the four harbor terminals, one row per visit.
  VISIT_ID        terminal code, two-digit year of the visit's opening and a running number
  BERTH           berth at the terminal
  VESSEL_NAME     name of the ship on the visit as booked
  IMO_NO          IMO ship identification number
  LINE_OP         operating line
  SERVICE         liner service code; FDR for feeder and ad hoc calls
  IB_VOYAGE, OB_VOYAGE   inbound and outbound voyage numbers
  ETA             planned arrival as booked, Eastern time
  PHASE           visit phase in the system at the pull

srt_tos_export_fy2026.xlsx
SRT, the terminal operating system of Salt River Terminals, which ran Saltworks and Millrace before the Authority
bought the two terminals in 2024 and still runs them. Sheet Calls: one row per vessel call. Sheet QC Hours: one row per quay crane, call and
clock hour (UTC) in which the crane made at least one lift.
  CALL_REF        terminal code, year and running number
  BERTH           berth
  VESSEL, LLOYDS, CALLSIGN   ship's name on the call, IMO number, call sign
  OPERATOR, SERVICE, VOY      operating line, service, inbound/outbound voyage
  ETA_UTC         planned arrival
  QC              quay crane, by its SRT tag (see sts_crane_register.csv SRT_TAG)
  HOUR_UTC        clock hour, UTC
  LIFTS           container lifts in the hour; a twin lift is one lift
  FIRST_LIFT_UTC, LAST_LIFT_UTC   first and last container lift of the crane on the call within the hour
  BAYS            lowest and highest 40-foot bay the crane worked in the hour

pilot_station_sailings_fy2026.csv
Ternmouth Pilots' dispatch system, outbound jobs from the six container terminals' berths, sailings 20 June
2025 to 9 July 2026. One row per sailing.
  JOB_NO          pilot job number (two-digit year and a running number)
  MOVE            OUT, a sailing from the berth to sea
  VESSEL          ship's name as the dispatcher entered it
  CALL_SIGN       ship's call sign as given by the agent
  FROM_BERTH      berth the ship sailed from
  TO              SEA
  NOTICE_RECEIVED when the agent's notice that the ship was ready to sail reached the pilot station, Eastern time
  SAILED          the ship's sailing time: when it let go from the berth, Eastern time
  DRAFT_FWD, DRAFT_AFT   draft on sailing, feet and inches (41-06 is 41 feet 6 inches)
  PILOT           pilot's initials
  TUGS            tugs ordered

salt_point_tide_predictions_2025_2026.txt
The Authority's predicted times and heights of high and low water at Salt Point, 1 June 2025 to 31 July 2026,
as published (tab separated after the header lines).

vessel_register_extract_2026-10-05.json
Authority vessel register, every ship on the register at the pull, with its current particulars.
  imo, name, former_names (each with the last date it was carried), call_sign, mmsi, port_of_registry, teu_nominal
  (nominal container capacity in TEU), loa_m (length overall), beam_m, summer_draft_m, dwt, built, operator

sts_crane_register.csv
Ship-to-shore crane register at 5 October 2026. One row per crane.
  CRANE_ID        crane number
  TERMINAL        ORD, PNC, GNP, HLY, SLT, MRW
  ASSETNUM        asset number in the Authority's maintenance system
  SRT_TAG   SRT equipment tag, Saltworks and Millrace cranes only
  MAKE, MODEL, COMMISSIONED, OUTREACH_ROWS (container rows reached across a ship), SWL_T (safe working load)

cmms_sts_work_orders_fy2026.csv
Authority maintenance system, work orders on ship-to-shore cranes reported 1 June 2025 to 30 September 2026
(Saltworks and Millrace cranes from 1 February 2026). One row per work order.
  WONUM           work order number (one sequence for every asset class in the system)
  ASSETNUM        asset number (see sts_crane_register.csv)
  SITEID          TMH
  WORKTYPE        BD breakdown, DMG damage (struck by a ship's gear, a vehicle or another crane; the
                  repair is charged to the party responsible, and damage is reported apart from the
                  cranes' breakdowns though its repair is crane maintenance like any other order's),
                  CM corrective (crane kept in service),
                  PM planned maintenance, INSP inspection. An order's type can be changed after it is
                  raised; the extract shows the type at the pull.
  WOPRIORITY      1 to 3
  STATUS          COMP work complete, CLOSE closed and costed
  PROBLEMCODE     SPRDR spreader, HOIST, TROL trolley, GANT gantry, ELEC electrical and controls, BOOM,
                  CAB operator cab; planned work carries its job plan code
  DESCRIPTION     free text
  REPORTDATE      when the order was raised
  OUT_OF_SERVICE  when the crane was first taken out of service on the order
  RETURNED_TO_SERVICE  when the crane was last returned to service on the order
  ACTSTART, ACTFINISH  first and last labor booked to the order
  CLOSEDATE       when the order was closed
  REPORTEDBY      user who raised the order
  OUT_OF_SERVICE and RETURNED_TO_SERVICE are blank on orders that did not take the crane out of service.

cmms_asset_status_history_fy2026.csv
Authority maintenance system, running status changes of ship-to-shore cranes. One row per change.
  ASSETNUM        asset number
  ISRUNNING       0 the crane went out of service, 1 it returned to service
  CHANGEDATE      time of the change
  CODE            downtime code the change was booked under: BRKDWN unplanned, PLANNED, PROJECT
  WONUM           work order the change was booked against; blank for project downtime
  CHANGEBY        user

cmms_labor_transactions_fy2026.csv
Authority maintenance system, labor booked to work orders, work days 1 June 2025 to 30 September 2026, every
asset class. One row per person, work order and work day.
  LABTRANSID      transaction number
  WONUM           work order
  LABORCODE       employee number; CONTRACT for contractors' hours, keyed by the planner from the
                  contractor's service report
  CRAFT           MECH, ELEC, RIG rigger, WELD welder, CONTRACT
  TRANSDATE       the work day
  REGULARHRS      hours worked that day
  PREMIUMPAYCODE  OT15 on a day paid at time and a half (the hours are in REGULARHRS)
  ENTERDATE, ENTERBY   when and by whom the row was entered

crane_maker_service_timesheets_fy2026.xlsx
The crane makers' field-service engineers' timesheets for work at Ternmouth, work days 1 June 2025 to 30
September 2026, as received by Terminal Equipment with each maker's monthly invoice. One row per engineer and
work day.
  SERVICE_CO      the crane maker's field service, or the service agent it appoints
  SERVICE_REPORT  the maker's service report number
  CUSTOMER_REF    the Authority's work order (or SRT job) the engineer worked under, as the engineer wrote it
  CRANE           crane as the engineer wrote it
  SITE            where the engineer worked
  ENGINEER        engineer's name
  WORK_DATE       work day
  HOURS           hours worked on site that day

srt_maintenance_jobs_2025-26.xlsx
SRT maintenance log, Saltworks and Millrace cranes, jobs raised 1 June 2025 to 28 February 2026, when
the log was closed. One row per job.
  JOB_NO          job number
  EQUIP_TAG       SRT equipment tag (see sts_crane_register.csv SRT_TAG)
  JOB_CLASS       BRKDN breakdown, PLND planned, INSP inspection, DEFECT defect noted (crane kept working)
  PRIORITY        P1 to P3
  FAULT           free text
  RAISED_UTC      when the job was raised
  DOWN_UTC        when the crane was taken out of service (blank on DEFECT jobs)
  UP_UTC          when the crane was released to operations
  LABOUR_HRS      labor hours SRT's crews and resident contractors booked to the job; the crane makers'
                  engineers were never booked in the log
  STATUS, RAISED_BY

ais_berth_segments_fy2026.csv
Authority AIS berth pipeline. One row per stretch of AIS position reports from one ship stopped (under 0.5 knot)
inside one berth or anchorage polygon. A stretch is closed at midnight UTC and wherever no report is received
from the ship for more than 60 minutes; the next report opens a new stretch.
  SEG_ID          stretch id
  MMSI, SHIPNAME, CALLSIGN   as broadcast by the ship
  ZONE            berth or anchorage polygon; ZONE_TYPE BERTH or ANCHORAGE
  START_UTC, END_UTC   first and last report in the stretch
  N_REPORTS       reports received in the stretch

cmms_yard_equipment_work_orders_fy2026.csv
Authority maintenance system, work orders on yard equipment (rubber-tyred gantries, straddle carriers, reach
stackers, terminal tractors). Same columns as the crane orders.

berth_windows_fy2027.csv
Contracted berth windows for fiscal year 2027 by service, as agreed with the lines at 1 October 2026.
  SERVICE, CARRIER, TERMINAL, BERTH, ARRIVAL_DAY, ARRIVAL_TIME (Eastern), WINDOW_HOURS, MAX_TEU,
  ROTATION_WEEKS, EFFECTIVE_FROM
"""


def write_dictionary(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(DICTIONARY)


MANIFEST_COLS = ["FILE", "SYSTEM", "OWNER", "PULLED", "COVERS", "ROWS", "CLOCK"]


def manifest_rows(n):
    f = P.FILES
    return [
        [f["tos"], "Authority TOS, crane activity report", "Vessel Operations", "2026-10-05 06:22",
         "clock hours 2025-06-23 to 2026-07-06, harbor terminals", n["tos"], "Eastern"],
        [f["visits"], "Authority TOS, vessel visits", "Vessel Operations", "2026-10-05 06:24",
         "visits open 2025-06-20 to 2026-07-06, harbor terminals", n["visits"], "Eastern"],
        [f["rvt"], "SRT TOS, calls and QC hours", "River Terminals", "2026-10-05 07:41",
         "calls 2025-06-20 to 2026-07-06, Saltworks and Millrace", n["rvt"], "UTC"],
        [f["pilot"], "Ternmouth Pilots dispatch, sailings", "Ternmouth Pilots", "2026-10-02 10:15",
         "sailings 2025-06-20 to 2026-07-09, container berths", n["pilot"], "Eastern"],
        [f["tides"], "Tide predictions, Salt Point", "Hydrographic Services", "2025-05-12 09:00",
         "2025-06-01 to 2026-07-31", n["tides"], "LST"],
        [f["vessels"], "Vessel register", "Vessel Operations", "2026-10-05 06:10", "ships on the register",
         n["vessels"], ""],
        [f["register"], "STS crane register", "Terminal Equipment", "2026-10-05 06:58", "cranes at 2026-10-05",
         n["register"], ""],
        [f["wo"], "Authority maintenance system, work orders (STS cranes)", "Terminal Equipment",
         "2026-10-05 06:51", "orders reported 2025-06-01 to 2026-09-30", n["wo"], "Eastern"],
        [f["status"], "Authority maintenance system, asset status history (STS cranes)", "Terminal Equipment",
         "2026-10-05 06:53", "status changes 2025-06-01 to 2026-09-30", n["status"], "Eastern"],
        [f["labor"], "Authority maintenance system, labor transactions", "Terminal Equipment",
         "2026-10-05 06:56", "work days 2025-06-01 to 2026-09-30", n["labor"], "Eastern"],
        [f["oem"], "Crane makers' service timesheets", "Terminal Equipment", "2026-10-05 08:20",
         "work days 2025-06-01 to 2026-09-30", n["oem"], ""],
        [f["jobs"], "SRT maintenance log", "River Terminals", "2026-10-05 07:44",
         "jobs raised 2025-06-01 to 2026-02-28 (log closed)", n["jobs"], "UTC"],
        [f["ais"], "AIS berth pipeline", "Vessel Operations", "2026-10-06 08:15",
         "stretches opening 2025-06-20 to 2026-07-09 UTC", n["ais"], "UTC"],
        [f["yard"], "Authority maintenance system, work orders (yard equipment)", "Terminal Equipment",
         "2026-10-05 06:55", "orders reported 2025-06-01 to 2026-09-30", n["yard"], "Eastern"],
        [f["windows"], "Commercial, berth window agreements", "Commercial", "2026-10-01 16:30",
         "windows for fiscal year 2027", n["windows"], "Eastern"],
        [f["rules"], "Crane Replacement Program placement rules", "Terminal Equipment", "", "Revision 3 with "
         "Schedule A", "", ""],
        [f["directions"], "Harbor Master's General Directions", "Office of the Harbor Master", "", "2025 edition",
         "", ""],
        [f["dictionary"], "Data dictionary", "Vessel Operations", "", "issue 8", "", ""],
    ]
