"""task173 documents: the 2027 term contract's bid schedule with its measurement and payment section, the 2027 water
main replacement program and the 2027 flushing plan (PDF), the field definitions (text) and the export manifest (CSV).
Their text is held here as data so checks.py can quote it and verify.py can read it back."""
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
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as C            # noqa: E402
import postprocess as PP      # noqa: E402
from world import D0          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Serif", "liberation/LiberationSerif-Regular.ttf"), ("Serif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("Sans", "liberation/LiberationSans-Regular.ttf"), ("Sans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1b1b")
GREY = colors.HexColor("#555555")

# ---------------------------------------------------------------- the filed sentences (bid schedule, section 02)
SVC_PIN = ("Item 101, water service leak repair, is measured per leak repaired on the City's portion of a water "
           "service, from the corporation stop at the main through the meter's outlet coupling, including the angle "
           "valve, the setter and the meter box. A leak is one unit however many work orders or visits its repair "
           "takes, and is counted in the period its repair is completed.")
SVC_SCOPE = ("Leaks on the customer's side of the meter, leaks in the meter body and work on fire lines are not "
             "Item 101 work.")
TOTAL_PIN = ("The estimated quantities for Items 101 and 201 are the City's total for the contract year, whether "
             "repaired by City crews or under this contract; the Contractor's share is assigned by work order.")
MAIN_PIN = ("Item 201, water main break repair, is measured per break on a water main. A break is one unit, counted in "
            "the period its permanent repair is completed.")
AREA_PIN = ("Quantities reported by service centre are reported by the service centre area in which the main or "
            "service lies, as mapped in the GIS.")
REST_PIN = ("Items 301 to 307 are measured as accepted by the City's inspector in the monthly pay estimate, in the "
            "units shown, and are counted in the period the restoration was completed.")
RETAIN = ("The City retains five per cent of each accepted pay estimate until final acceptance of the contract "
          "year's work, as under Contract 23-0388.")
FY_PIN = ("Base-year quantities are for the City's fiscal year 2026, 1 October 2025 to 30 September 2026, in quarters "
          "of October to December, January to March, April to June and July to September.")
TERM = ("The contract year is 1 January to 31 December 2027. Estimated quantities are the City's estimate of the "
        "work the contract year will require and are used to compare bids; payment is at the unit prices bid for the "
        "quantities actually performed.")

ITEMS_NEW = [
    ("101", "Water service leak repair, any size to 2 in", "EA", ""),
    ("201", "Water main break repair, 4 in to 16 in", "EA", ""),
    ("301", "Asphalt pavement patch, full depth (formerly 0410)", "SY", "Asphalt pavement"),
    ("302", "Concrete pavement replacement, 8 in (formerly 0420)", "SY", "Concrete pavement"),
    ("303", "Concrete sidewalk, 4 in (formerly 0430)", "SY", "Sidewalk and driveway"),
    ("304", "Concrete driveway, 6 in (formerly 0431)", "SY", "Sidewalk and driveway"),
    ("305", "Solid sod to match existing (formerly 0440)", "SY", "Sod"),
    ("306", "Concrete curb and gutter (formerly 0450)", "LF", ""),
    ("307", "Saw cut, pavement (formerly 0460)", "LF", ""),
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


def _pdf(path, title, sub, sections, tables=None, foot=None, issued=None, author=""):
    base, head, tstyle, sstyle, small = _styles()
    story = [Paragraph(_esc(title), tstyle)]
    if sub:
        story.append(Paragraph(_esc(sub), sstyle))
    tables = tables or {}
    for h, paras in sections:
        if h:
            story.append(Paragraph(_esc(h), head))
        for p in paras:
            story.append(Paragraph(_esc(p), base))
        if h in tables:
            rows, widths = tables[h]
            t = Table(rows, hAlign="LEFT", colWidths=widths, repeatRows=1)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Sans-Bold", 8), ("FONT", (0, 1), (-1, -1), "Sans", 8),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
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
        canvas.drawRightString(letter[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    stamp = ("D:%04d%02d%02d%02d%02d%02d-05'00'" % (issued.year, issued.month, issued.day, 10, 12, 0)).encode()
    PP.normalize_pdf(path, stamp, stamp)


BID_SECTIONS = [
    ("01. General", [TERM, TOTAL_PIN, RETAIN,
                     "Bids are due at the Purchasing Division by 2:00 p.m. on 12 November 2026. The Water Utilities "
                     "Director recommends award to City Council at its 8 December 2026 meeting."]),
    ("02. Measurement and payment", [SVC_PIN, SVC_SCOPE, MAIN_PIN, AREA_PIN, REST_PIN,
                                     "Restoration items include placement, compaction, forming, finishing and "
                                     "watering until acceptance. Saw cuts are paid once per cut line."]),
    ("03. Bid schedule", ["Estimated quantities marked TBD are entered by the Distribution Division before the "
                          "invitation is issued. Base-year quantities are entered on Form 3B."]),
    ("04. Form 3B, base-year quantities", [FY_PIN,
                                          "Form 3B reports Item 201 by service centre (North, South, West) and by "
                                          "month, and Items 301 to 305 by surface type (asphalt pavement, concrete "
                                          "pavement, sidewalk and driveway, sod) and by quarter, in square yards."]),
]


def write_bid(path):
    rows = [["Item", "Description", "Unit", "Est. quantity 2027", "Form 3B group"]]
    for no, desc, unit, grp in ITEMS_NEW:
        rows.append([no, desc, unit, "TBD", grp])
    _pdf(path, "ITB 27-0114: Water Service Repair and Surface Restoration, Annual Term Contract 2027",
         "City of Hollis Bend, Purchasing Division, for Hollis Bend Water Utilities, Distribution Division. Draft for "
         "quantities, 6 October 2026.", BID_SECTIONS,
         tables={"03. Bid schedule": (rows, [12 * mm, 82 * mm, 11 * mm, 28 * mm, 38 * mm])},
         foot="Contract 23-0388 (Mabry-Teague Utility Constructors, Inc.) expires 31 December 2026.",
         issued=dt.date(2026, 10, 6), author="Purchasing Division")


def write_cip(path, w, pk):
    rows = [["Project", "Street", "Main(s) replaced", "Length ft", "Services renewed", "Substantial completion"]]
    tot_s = tot_l = 0
    for k, (m, day) in enumerate(sorted(w.cap_2027, key=lambda x: x[1])):
        n_s = len([j for j in w.svc_by_main.get(m, []) if w.svc_start[j] <= (C.RECORDS_END - D0).days])
        tot_s += n_s
        tot_l += int(w.main_len[m])
        dd = D0 + dt.timedelta(days=int(day))
        rows.append(["W27-%02d" % (k + 1 + (k > 9)), w.streets[w.main_st[m]], w.main_id[m], "{:,}".format(int(w.main_len[m])),
                     str(n_s), dd.strftime("%B %Y")])
    rows.append(["Total", "", "", "{:,}".format(tot_l), str(tot_s), ""])
    sections = [
        ("", ["The 2027 water main replacement program replaces cast iron and early asbestos-cement mains selected on "
              "break history, fire flow and the Street Maintenance Division's 2027 paving list. Projects are delivered "
              "under the City's open-cut main replacement contracts."]),
        ("Services", ["Every service on a replaced main is renewed from the new main to the meter box, with a new "
                      "corporation stop, service line, angle valve and setter. The main contractor resets the existing "
                      "meter in the new setter. Premises on these mains are held out of the AMI installation until the "
                      "project is complete."]),
        ("Table 1. 2027 projects", []),
        ("Schedule", ["Completion months are the construction managers' scheduled substantial completion as of 1 "
                      "October 2026. Services are transferred to the new main in the last two weeks before substantial "
                      "completion."]),
    ]
    _pdf(path, "Capital Improvement Program 2027: Water Main Replacement",
         "Hollis Bend Water Utilities, Engineering Division. Adopted with the FY 2027 budget, 16 September 2026; "
         "schedule as of 1 October 2026.", sections,
         tables={"Table 1. 2027 projects": (rows, [16 * mm, 46 * mm, 28 * mm, 18 * mm, 22 * mm, 34 * mm])},
         issued=dt.date(2026, 10, 1), author="Engineering Division")
    return tot_s


def write_flush(path):
    r = C.stream("docs/flush")
    rows = [["Flushing zone", "Pressure zone", "Weeks", "Night work", "Approx. miles"]]
    zones = ["N-1", "N-2", "N-3", "N-4", "S-1", "S-2", "S-3", "S-4", "S-5", "W-1", "W-2", "W-3"]
    wk = 3
    for z in zones:
        pz = r.choice(["UPPER", "CENTRAL", "RIVER"])
        span = int(r.integers(2, 4))
        rows.append([z, pz, "%d to %d" % (wk, wk + span - 1), "Yes" if r.random() < .4 else "No", str(int(r.integers(140, 330)))])
        wk += span + int(r.integers(0, 2))
    sections = [
        ("", ["Unidirectional flushing cleans the distribution system zone by zone, closing valves to move water "
              "through each pipe in one direction at a scouring velocity, from the source toward the dead ends. "
              "The 2027 program repeats the 2024 sequence."]),
        ("Table 1. 2027 sequence", []),
        ("Notices", ["Customers receive door hangers 48 hours ahead. Discoloured water calls during a zone's weeks "
                     "are logged against the flushing work order."]),
    ]
    _pdf(path, "Unidirectional Flushing Plan 2027", "Hollis Bend Water Utilities, Water Quality Section. Issued 30 "
         "September 2026.", sections, tables={"Table 1. 2027 sequence": (rows, [28 * mm, 26 * mm, 22 * mm, 22 * mm, 26 * mm])},
         issued=dt.date(2026, 9, 30), author="Water Quality Section")


DICT = """HOLLIS BEND WATER UTILITIES - FIELD DEFINITIONS FOR THE 2027 TERM CONTRACT QUANTITIES FOLDER
Distribution Division, compiled 21 October 2026

gis_service_lines_20260930.csv  (GIS, service layer, one row per service line)
  SERVICE_ID       GIS service identifier (SV-nnnnnn)
  MAIN_ID          main the service is tapped on
  SERVICE_ADDRESS  address the service serves
  MATERIAL         service line material: CU copper, GALV galvanized steel, PB polybutylene, PE or HDPE polyethylene,
                   UNK not recorded. Records not edited since the 2016 conversion may carry the earlier one-letter
                   codes (C, G, B, P).
  INSTALL_YR       year the service line was installed or last renewed; blank where not recorded
  SIZE_IN          nominal service size, inches
  PRESSURE_ZONE    pressure zone
  SVC_CENTER       service centre area
  STATUS           ACTIVE
  LAST_EDIT        date of the last edit to the record

gis_water_mains_20260930.csv  (GIS, main layer, one row per main segment, active and abandoned)
  MAIN_ID, MATERIAL (CI cast iron, AC asbestos-cement, DI ductile iron, PVC), INSTALL_YR, DIAMETER_IN, LENGTH_FT,
  PRESSURE_ZONE, SVC_CENTER (service centre area), STREET, STATUS (ACTIVE or ABANDONED), ABANDONED_DATE

cis_premises_20260930.csv  (Customer Information System, one row per premise)
  PREMISE_ID       CIS premise number; a premise has one meter
  SERVICE_ADDRESS, UNIT
  ROUTE            meter reading route
  SERVICE_ID       GIS service the premise is served from; blank where the premise has not been linked
  PREMISE_TYPE     RES single-family, MF multifamily unit, COM commercial
  METER_SIZE, STATUS
  CONNECT_DATE     first meter set at a new service, where after 1 January 2012

cis_meter_events_2012_2026.csv  (CIS meter history, one row per meter set or removal, January 2012 to September 2026)
  EVENT_ID, PREMISE_ID, EVENT_DATE
  EVENT_TYPE       SET or REMOVE
  METER_NO         meter serial number
  REASON           NEW new service; AGE scheduled change-out; STOP stopped or failed meter; TEST pulled for accuracy
                   test; CUST customer request; SIZE meter resized
  PERFORMED_BY     MSHOP the Meter Shop; ARR Arredondo Field Services (2022 stopped-meter contract); DEV developer's
                   plumber at a new service
  REGISTER_READ    register reading, cubic feet

lwms_workorders_2012_2021.csv  (legacy work management system, one row per work order, January 2012 to 14 May 2021)
  WO_NO, WO_TYPE, STATUS (CLOSED, CANCELLED, MIGRATED: open at the cutover and carried into EAM), ADDRESS, YARD,
  INIT_DATE, COMP_DATE, DESCR
  WO_TYPE          SVC INVEST, SVC LEAK, MAIN BREAK, RESTORE, METER BOX, HYDRANT, VALVE, LOCATE

eam_workorders_2021_2026.xlsx  (EAM, from 17 May 2021, one row per work order)
  WORKORDER_ID     EAM work order number
  LEGACY_WO        legacy work order number of a work order carried over at the cutover
  WORK_TYPE        SERVICE LEAK, MAIN BREAK, RESTORATION, METER BOX, HYDRANT, VALVE, LOCATE
  WORK_CLASS       INV investigation, REP repair by City crew, REPC repair by contractor, RST surface restoration
  STATUS           OPEN, CLOSED, CANCELLED
  ASSET_TYPE, ASSET_ID   the asset worked on (SERVICE: GIS SERVICE_ID; MAIN: GIS MAIN_ID; hydrants FH-, valves WV-)
  ADDRESS          location as dispatched
  COMPONENT        component repaired, on service repairs
  REPORTED         date and time the customer call or field report was taken
  INITIATED, COMPLETED   work order dates
  CREW_YARD        yard of the crew that did the work

ami_install_schedule_2027.csv  (Halvorsen Metering Services deployment schedule, rev. 4, one row per premise)
  PREMISE_ID, ROUTE, SVC_CENTER, METER_NO (meter in place)
  WORK_TYPE        METER EXCHANGE: the installer removes the meter and sets an AMI meter with its endpoint;
                   ENDPOINT RETROFIT: an endpoint is fitted to the AMI-ready register of the meter in place;
                   HOLD - CIP 2027: held until the premise's main replacement project is complete
  PLANNED_WEEK_OF  Monday of the week the route is scheduled

mabry_teague_pay_estimates_fy2025_fy2026.xlsx  (Contract 23-0388 pay estimate lines, every revision submitted)
  ESTIMATE_NO      monthly pay estimate (PE-yymm, the month of work)
  REVISION         0 for the first submission, then 1, 2 for resubmissions
  SUBMITTED        date the revision was submitted
  PERIOD           month the estimate covers
  WO_REF           EAM restoration work order
  LOCATION, ITEM (contract 23-0388 item), DESCRIPTION, UNIT, QTY, UNIT_PRICE, AMOUNT (USD)
  WORK_COMPLETED   date the restoration was completed

ap_payments_contract_23-0388.csv  (Finance, accounts payable, one row per voucher on Contract 23-0388)
  VOUCHER_NO, VENDOR_NO, VENDOR_NAME, INVOICE_NO (the pay estimate paid), INVOICE_DATE, GROSS_AMOUNT, RETAINAGE,
  NET_PAID, PAID_DATE, CONTRACT_NO

valve_exercise_log_2019_2026.csv  (valve exercising program, one row per valve visit)
  VALVE_ID, SVC_CENTER, SIZE_IN, EXERCISE_DATE, TURNS, RESULT

hbx_airport_daily_weather_2012_2026.csv  (Hollis Bend Regional Airport station, daily)
  DATE, TMAX_F, TMIN_F, PRCP_IN (T trace)
"""


def write_dict(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(DICT.replace("\n", "\r\n"))


def write_manifest(path, n):
    rows = [
        (C.F_GIS_SVC, "GIS (Esri geodatabase), service layer", "GIS Section", "2026-10-05", "active services at 30 Sep 2026", n.get(C.F_GIS_SVC)),
        (C.F_GIS_MAIN, "GIS, main layer", "GIS Section", "2026-10-05", "active and abandoned mains at 30 Sep 2026", n.get(C.F_GIS_MAIN)),
        (C.F_PREM, "CIS premise table", "Billing Systems", "2026-10-05", "premises at 30 Sep 2026", n.get(C.F_PREM)),
        (C.F_METER, "CIS meter history", "Billing Systems", "2026-10-05", "1 Jan 2012 to 30 Sep 2026", n.get(C.F_METER)),
        (C.F_LEGACY, "legacy work management system (retired)", "Distribution Division", "2021-05-15", "1 Jan 2012 to 14 May 2021", n.get(C.F_LEGACY)),
        (C.F_EAM, "EAM work orders", "Distribution Division", "2026-10-05", "17 May 2021 to 30 Sep 2026", n.get(C.F_EAM)),
        (C.F_AMI, "Halvorsen Metering Services deployment schedule rev. 4", "Meter Services", "2026-09-28", "calendar 2027", n.get(C.F_AMI)),
        (C.F_CAP, "Engineering Division", "Engineering Division", "2026-10-01", "2027 program", 1),
        (C.F_BID, "Purchasing Division draft", "Purchasing Division", "2026-10-06", "2027 contract year", 1),
        (C.F_PAYEST, "contract management system, pay estimate lines", "Distribution Division", "2026-10-20", "estimates for Oct 2024 to Sep 2026 work", n.get(C.F_PAYEST)),
        (C.F_AP, "Finance (ERP), accounts payable", "Finance", "2026-10-20", "vouchers on Contract 23-0388 to 16 Oct 2026", n.get(C.F_AP)),
        (C.F_VALVE, "valve exercising program log", "Distribution Division", "2026-10-05", "2019 to 30 Sep 2026", n.get(C.F_VALVE)),
        (C.F_FLUSH, "Water Quality Section", "Water Quality Section", "2026-09-30", "2027 program", 1),
        (C.F_WX, "airport ASOS daily summary", "Water Quality Section", "2026-10-05", "1 Jan 2012 to 30 Sep 2026", n.get(C.F_WX)),
        (C.F_DICT, "Distribution Division", "Distribution Division", "2026-10-21", "this folder", 1),
    ]
    out = []
    for f, sysn, who, pulled, cover, rows_n in rows:
        out.append((f, sysn, who, pulled, cover, "" if rows_n in (None, 1) else rows_n))
    return C.write_csv(path, ["FILE", "SOURCE", "PROVIDED_BY", "EXTRACTED", "COVERS", "DATA_ROWS"], out)
