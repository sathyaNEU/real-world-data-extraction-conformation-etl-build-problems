"""task175 documents: the program schedule and the forecasting conventions (PDF), the field definitions (text)
and the export manifest (CSV). Their text is held here as data so checks.py can quote it and verify.py can read
it back."""
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
from world import AREAS       # noqa: E402
from utility import FEE       # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Serif", "liberation/LiberationSerif-Regular.ttf"), ("Serif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("Sans", "liberation/LiberationSans-Regular.ttf"), ("Sans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1b1b")
GREY = colors.HexColor("#555555")

MARKET_PIN = "Forecasts hold the building market at its calendar 2026 level."
ESTIMAND_PIN = ("A permit forecast is the expected number of distinct lots that receive such a permit in the year, a "
                "lot being permitted at most once.")
PERMIT_PIN = ("Permit forecasts count City building permits of work class Residential New Single Family (legacy type "
              "RES NEW SFR) by issue date in the calendar year forecast, and an area's permits are the permits on lots "
              "in the plat units the program schedule lists for it.")
CONN_PIN = "A new connection is counted once for its lot, in the period the lot's first meter is installed."
FY_PIN = ("The Utility's fiscal year runs from 1 October to 30 September: fiscal 2026 ran from 1 October 2025 to "
          "30 September 2026, in quarters of October to December, January to March, April to June and July to "
          "September.")
FEE_PIN = ("Water and sewer capacity fees are paid at the cashier when the builder buys the meter, at the fee in effect "
           "on the payment date, and are reported on the receipt date.")
ACCEPT_PIN = ("Lines accepted is the date the City accepted an area's water, sewer and irrigation lines from the "
              "contractor; lots in the area may connect from that date.")

CONVENTIONS = [
    ("1. Purpose", [
        "Section 7.03 of the Master Bond Resolution requires the Utility to file a revenue sufficiency report with the "
        "trustee each January. The report carries the year's capacity fee forecast, which rests on the single-family "
        "building permits the City will issue in the areas the Utility Extension Program serves, and the fiscal "
        "year's actual connections and capacity fee receipts.",
        "These conventions apply to the report filed in January 2027 and to the working files behind it."]),
    ("2. Permit forecasts", [PERMIT_PIN, ESTIMAND_PIN, MARKET_PIN,
                             "Areas are named as in the program schedule, Revision 12 or later."]),
    ("3. Connections and fees", [FY_PIN, CONN_PIN, FEE_PIN,
                                 "Program phases are those of the program schedule. The core service area is reported "
                                 "on its own line."]),
    ("4. Fee schedule", ["Single-family water and sewer capacity fee per equivalent residential connection (ERC): fiscal "
                         "2024 USD %s; fiscal 2025 USD %s; fiscal 2026 USD %s; fiscal 2027 USD %s. A 5/8 by 3/4 inch "
                         "meter is one ERC and a 1 inch meter 2.5 ERCs (Resolution 2026-41)." %
                         tuple("{:,}".format(FEE[y]) for y in (2024, 2025, 2026, 2027))]),
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
        if h:
            story.append(Paragraph(_esc(h), head))
        for p in paras:
            story.append(Paragraph(_esc(p), base))
        if table is not None and h == table_after:
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
        canvas.drawRightString(letter[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    stamp = ("D:%04d%02d%02d%02d%02d%02d-05'00'" % (issued.year, issued.month, issued.day, 9, 41, 0)).encode()
    PP.normalize_pdf(path, stamp, stamp)


def schedule_table(w):
    """area, phase, plat units, lots, lines accepted (completed areas) or scheduled"""
    rows = [("Area", "Phase", "Plat units", "Lots", "Lines accepted")]
    units = {}
    for u, ai in zip(w.unit_no, w.unit_area):
        units.setdefault(ai, []).append(u)
    for ai, a in enumerate(AREAS):
        if a[0] == "Core":
            continue
        us = units[ai]
        lots = int((w.L["area"] == ai).sum())
        acc = w.area_acc[ai]
        if acc <= dt.date(2026, 12, 31):
            when = acc.strftime("%d %b %Y").lstrip("0")
        elif acc.year == 2027:
            when = "scheduled " + acc.strftime("%d %b %Y").lstrip("0")
        else:
            when = "planned " + str(acc.year)
        rows.append((a[0], a[1], ", ".join(str(x) for x in us), "{:,}".format(lots), when))
    return rows


def write_schedule(path, w):
    core_units = [u for u, ai in zip(w.unit_no, w.unit_area) if AREAS[ai][0] == "Core"]
    core_lots = int((w.L["area"] == 0).sum())
    sections = [
        ("", ["The Utility Extension Program carries potable water, sanitary sewer and irrigation lines into one area of "
              "the original Port Ardell plat at a time, financed by special assessments levied on the lots of each area. "
              "The core service area (plat units %d to %d, %s lots) was served by the City's original water and sewer "
              "districts before the program began." % (min(core_units), max(core_units), "{:,}".format(core_lots)),
              ACCEPT_PIN]),
        ("Table 1. Program areas", []),
        ("Revision history", ["Revision 12 (15 December 2026): North 6, North 7 and Northwest 3 acceptance dates set from "
                              "the contractors' December schedules; Phase 6 planning years confirmed. Revision 11 (10 "
                              "February 2026): Northwest 3 contract award. Earlier revisions are on file with the "
                              "Capital Program Division."]),
    ]
    _pdf(path, "Utility Extension Program: Area Schedule, Revision 12",
         "%s, Capital Program Division. Issued 15 December 2026. Steven Burke, Program Manager." % C.UTIL, sections,
         table=schedule_table(w), table_after="Table 1. Program areas", issued=dt.date(2026, 12, 15),
         author="Steven Burke", widths=[34 * mm, 14 * mm, 44 * mm, 18 * mm, 40 * mm],
         foot="Phase 5 dates are the contractors' scheduled acceptance dates as of this revision.")


def write_conventions(path):
    _pdf(path, "Revenue Sufficiency Report FY2027: Forecasting Conventions",
         "%s, Finance Division, Revenue and Rates. Issued 2 December 2026. Melissa Payne, Revenue and Rates Manager." % C.UTIL,
         CONVENTIONS, issued=dt.date(2026, 12, 2), author="Melissa Payne",
         foot="Questions on these conventions go to Revenue and Rates.")


DICT = """FIELD DEFINITIONS, PORT ARDELL DATA FOLDER (assembled 8 January 2027)

pa_parcel_extract_2026.csv  Calusa County Property Appraiser, 2026 roll, one row per parcel
  STRAP        parcel number (section-township-range-plat unit-block.lot)
  SITE_ADDR    site address
  LEGAL_DESC   legal description (plat unit, block, plat book and page, lot)
  DOR_CD       Department of Revenue use code (0000 vacant residential, 0100 single family)
  DOR_DESC     use code description
  ZONING       City zoning district
  LAND_SF      lot area, square feet
  WATERFRONT   Y for a lot on a canal
  YR_BUILT     actual year built
  LIVING_SF    living area, square feet
  JUST_VALUE   just value on the 2026 roll, dollars
  OWNER_STATE  state or province of the owner's mailing address
  ROLL_YR      roll year; the roll states each parcel as of 1 January of the roll year

bldg_permits_legacy_2008_2018.csv  City of Port Ardell Building Division, legacy permitting system, one row per permit
  PERMIT_NBR   permit number
  APPLIED_DT   application date (MM/DD/YYYY)
  ISSUE_DT     issue date (MM/DD/YYYY)
  SITE_ADDR    site address as entered
  PERMIT_TYPE  permit type
  DESCRIPTION  work description
  VALUATION    declared valuation, dollars
  CONTRACTOR   contractor of record
  STATUS       status at the system's retirement
  FINAL_DT     certificate of occupancy date for new residences, final inspection date otherwise

bldg_permits_2019_2026.xlsx  City of Port Ardell Building Division, permitting system from 2019, one row per permit
  Permit Number      permit number
  Legacy Permit #    legacy permit number of a permit carried over from the legacy system
  Parcel ID          appraiser's parcel number
  Address            site address
  Work Class         work class
  Applied Date, Issued Date, Expiration Date   permit dates
  Status             status on 6 January 2027
  CO Issued          certificate of occupancy date (new residences)
  Final Date         final inspection date (other work)

plat_unit_index.csv  City of Port Ardell, Engineering, one row per recorded plat unit

uep_program_schedule_rev12_2026.pdf  Port Ardell Utilities, Capital Program Division

cis_premise_extract_20261231.csv  Port Ardell Utilities customer information system, one row per service premise
  PREMISE_ID   premise number
  SVC_ADDR     service address
  PARCEL_ID    appraiser's parcel number where recorded
  UEP_PHASE    program phase code (00 core service area)
  CREATED_DT   date the premise was set up
  PREMISE_TYPE premise type
  STATUS       ACTIVE (metered) or STUB (service stub, no meter)

cis_account_history_20261231.csv  Port Ardell Utilities customer information system, one row per customer account
  ACCOUNT_NO   account number
  PREMISE_ID   premise number
  SVC_START    first day of billed service
  SVC_STOP     last day of billed service (blank while open)
  RATE_CLASS   rate class
  BILL_CYCLE   billing cycle

ami_headend_installs_fy25_fy26.csv  Port Ardell Utilities AMI head-end, one row per meter endpoint installed,
  1 October 2024 to 30 September 2026
  ENDPOINT_ID  radio endpoint number
  METER_SERIAL meter serial number
  PREMISE_ID   premise number
  INSTALL_DATE install date (local)
  INSTALL_TIME install time (local)
  METER_SIZE   meter size, inches
  CREW         installing crew

capacity_fee_receipts_fy2026.xlsx  City of Port Ardell cashiering, capacity fee code CAPWS, receipts dated in fiscal 2026,
  one row per permit on a receipt
  Receipt No, Receipt Date, Payer, Permit No, Fee Code, Amount, Tender

acs_2020_2024_port_ardell_tracts.csv  American Community Survey 2020-2024 five-year estimates, housing, by census tract
  (City of Port Ardell Planning compilation)

uep_special_assessment_roll_2026.csv  City of Port Ardell, Finance, special assessment roll for the program areas,
  balances at 31 December 2026
"""


def write_dict(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(DICT.replace("\n", "\r\n"))


def write_manifest(path, n):
    rows = [
        (C.F_ROLL, "Calusa County Property Appraiser", "2026-10-30", n.get(C.F_ROLL, ""), "2026 roll, certified", "parcels of the Port Ardell plat"),
        (C.F_PLEG, "Building Division, legacy permitting", "2019-01-04", n.get(C.F_PLEG, ""), "permits issued 2008 to 2018", "system retired 31 December 2018; permits open at the cutover were carried into the new system"),
        (C.F_PNEW, "Building Division, permitting", "2027-01-06", n.get(C.F_PNEW, ""), "permits issued 2019 to 2026 and permits carried over", ""),
        (C.F_PLAT, "Engineering", "2026-11-02", n.get(C.F_PLAT, ""), "plat units 1958 to 1971", ""),
        (C.F_SCHED, "Utilities, Capital Program Division", "2026-12-15", "", "program areas, Revision 12", ""),
        (C.F_PREM, "Utilities, customer information system", "2027-01-04", n.get(C.F_PREM, ""), "premises at 31 December 2026", ""),
        (C.F_ACCT, "Utilities, customer information system", "2027-01-04", n.get(C.F_ACCT, ""), "accounts opened to 31 December 2026", ""),
        (C.F_AMI, "Utilities, AMI head-end", "2026-10-09", n.get(C.F_AMI, ""), "endpoint installs fiscal 2025 and 2026", ""),
        (C.F_FEES, "Finance, cashiering", "2026-10-12", n.get(C.F_FEES, ""), "capacity fee receipts fiscal 2026", "fee code CAPWS"),
        (C.F_CONV, "Utilities, Finance Division", "2026-12-02", "", "forecasting conventions FY2027", ""),
        (C.F_ACS, "Planning (compilation of Census Bureau tables)", "2026-12-18", n.get(C.F_ACS, ""), "ACS 2020-2024, census tracts in the city", ""),
        (C.F_SAR, "Finance, special assessments", "2027-01-05", n.get(C.F_SAR, ""), "program assessment roll", ""),
        (C.F_DICT, "Utilities, Finance Division", "2027-01-08", "", "field definitions for this folder", ""),
    ]
    return C.write_csv(path, ["FILE", "SOURCE", "EXTRACTED", "ROWS", "COVERS", "NOTES"], rows)
