"""The pack's documents: the 2027 program guidelines, the 2025 pilot's close-out, the inspection program's 2024
annual report and the Section's notes on its extracts, each two to four pages in the Department's own voice."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import stations as S   # noqa: E402
import world as W      # noqa: E402

BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=12.8, spaceAfter=5)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13.5, spaceBefore=7, spaceAfter=3)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=3)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=8.6, leading=11, textColor=colors.HexColor("#444444"),
                     spaceAfter=9)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=9.8)
CELLB = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8, leading=9.8)
ORG = "State %s, %s" % (W.STATE_AGENCY, W.DIVISION)


def _doc(path, title):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                          bottomMargin=0.85 * inch, title=title, author=ORG, creator=ORG, producer=ORG, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, "%s  |  %s" % (ORG, title))
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "%d" % d_.page)
        c.restoreState()
    return d, frame


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.2, colors.HexColor("#bbbbbb")),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


GUIDE = {
    "2.1": ("An eligible vehicle is a gasoline or flex-fuel car or light truck (registration fuel code G or F) of model "
            "year 2005 to 2014 with a gross vehicle weight rating of 8,500 pounds or less (GVWR class 1 or 2a) that is "
            "registered in a member county on 1 July 2026, that is, has a Division of Motor Vehicles record with status "
            "ACTIVE in that county on the registration snapshot of that date. Diesel, hybrid and electric vehicles are not "
            "eligible."),
    "3.1": ("Intake events are held in each member county whose eligible vehicles will emit 10.0 short tons of NOx or "
            "more in calendar year 2027. The county's total is compared with 10.0 before any rounding."),
    "3.2": ("A vehicle's 2027 NOx is the miles it will travel in calendar year 2027 times the Table 2 running exhaust "
            "rate for its model year and program class (the Section's rate table, nox_running_rates_cy2027.xlsx). The "
            "program class follows the registration body code (registration_body_codes.csv). A short ton is 2,000 "
            "pounds, 907,184.74 grams."),
    "3.3": ("Each vehicle's 2027 miles are judged on its own odometer reading at its initial inspection in the "
            "Enhanced Inspection Program's 2024 to 2025 cycle. A vehicle's age is counted from 1 January of its model "
            "year."),
    "3.4": ("An eligible vehicle with no usable reading (not inspected in the cycle, or an odometer the inspector "
            "recorded as 0 or 999999) is taken to travel the average 2027 miles of the eligible vehicles of its model "
            "year registered in its county that have one."),
}


def write_guidelines(path):
    title = "Vehicle Retirement Program: 2027 Program Guidelines"
    d, frame = _doc(path, title)
    s = [Paragraph("Vehicle Retirement Program<br/>2027 Program Guidelines", TITLE),
         Paragraph("%s, %s. Issued 8 September 2026. Supersedes the 2025 pilot guidelines of 14 April 2025."
                   % (ORG, W.SECTION), SUB),
         Paragraph("1. Purpose", HEAD),
         Paragraph("The Vehicle Retirement Program pays owners to retire older gasoline cars and light trucks registered in "
                   "the %s ozone nonattainment area. It is funded by the Congestion Mitigation and Air Quality "
                   "Improvement Program through the State %s. The 2027 program year runs from 1 January to 31 "
                   "December 2027. The Department holds intake events, where owners bring their title and vehicle and "
                   "receive a voucher on surrender, in the member counties these guidelines designate." % (W.AREA, W.DOT),
                   BODY),
         Paragraph("2. Eligible vehicles", HEAD),
         Paragraph("2.1 " + GUIDE["2.1"], BODY),
         Paragraph("2.2 The vehicle must be driven or towed to a dismantler licensed for the program, with a title in the "
                   "applicant's name and no lien. An applicant may retire up to two vehicles in a program year.", BODY),
         Paragraph("3. Designation of intake counties", HEAD),
         Paragraph("3.1 " + GUIDE["3.1"], BODY),
         Paragraph("3.2 " + GUIDE["3.2"], BODY),
         Paragraph("3.3 " + GUIDE["3.3"], BODY),
         Paragraph("3.4 " + GUIDE["3.4"], BODY),
         Paragraph("3.5 The member counties are the twelve counties of the nonattainment area listed in county_codes.csv.",
                   BODY),
         Paragraph("4. Vouchers and dismantler charges", HEAD),
         Paragraph("4.1 The program pays a voucher of $1,000 for each vehicle it retires, on the dismantler's "
                   "confirmation that the vehicle has been surrendered.", BODY),
         Paragraph("4.2 The Department pays the licensed dismantler for each surrendered vehicle the processing and "
                   "towing charges in its program agreement; the charges are the same at every dismantler.", BODY),
         Paragraph("5. Intake events", HEAD),
         Paragraph("Intake events in a designated county run on the first and third Saturdays of each month from March to "
                   "November 2027, with a desk at one or more of the county's licensed inspection stations. Owners in "
                   "counties without events may apply by mail.", BODY),
         Paragraph("6. The 2025 pilot", HEAD),
         Paragraph("The program ran as a pilot from 2 June to 19 December 2025 in Elkhollow, Dunmarsh, Larkhaven and "
                   "Kinnard counties for vehicles of model years 2001 to 2010, under the same voucher and charges. Its close-out report of 10 February 2026 "
                   "describes how it ran.", BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_closeout(path, stats):
    title = "Vehicle Retirement Program: 2025 Pilot Close-out"
    d, frame = _doc(path, title)
    s = [Paragraph("Vehicle Retirement Program<br/>2025 Pilot Close-out", TITLE),
         Paragraph("%s, %s. 10 February 2026." % (ORG, W.SECTION), SUB),
         Paragraph("Summary", HEAD),
         Paragraph("The pilot offered a $1,000 voucher to owners of gasoline cars and light trucks of model years 2001 to "
                   "2010 registered in Elkhollow, Dunmarsh, Larkhaven and Kinnard counties. Letters went to %s owners on "
                   "the registration file in the week of 12 May 2025; the program office received %s applications by 5 "
                   "December and approved %s. Vehicles were surrendered from 2 June to 19 December 2025 at three licensed "
                   "dismantlers." % (stats["letters"], stats["apps"], stats["approved"]), BODY),
         Paragraph("Applications", HEAD),
         Paragraph("Most applications came in the six weeks after the letters and in October, after a reminder went out "
                   "with the inspection notices. Applications were declined where the title was not in the applicant's "
                   "name (%s), the vehicle was outside the model years (%s) or the applicant had already retired two "
                   "vehicles (%s); the rest of the shortfall were applicants who did not book a surrender date."
                   % (stats["dec_title"], stats["dec_my"], stats["dec_two"]), BODY),
         Paragraph("Dismantlers", HEAD),
         _table([["Licence", "Dismantler", "Serves", "Invoices"],
                 ["D-3317", "Calderwick Auto Recyclers", "Dunmarsh, part of Kinnard", "every second Friday"],
                 ["D-2864", "Oakhaven Salvage & Parts", "Elkhollow", "by pickup"],
                 ["D-4021", "Thistlebury Auto Salvage", "Larkhaven, most of Kinnard", "every second Friday"]],
                [0.8 * inch, 2.0 * inch, 2.1 * inch, 1.4 * inch]),
         Spacer(1, 6),
         Paragraph("Each dismantler billed the Department for processing and towing under its program agreement. Vouchers "
                   "were paid within four weeks of surrender, and the last invoices and vouchers in the first half of "
                   "January 2026.", BODY),
         Paragraph("What we would change", HEAD),
         Paragraph("Letters should go out with the inspection notice rather than on their own; the October reminder drew "
                   "as many applications as the first letter. Kinnard owners travelled furthest, and a desk in Tarnholt "
                   "would cut towing costs. The program office will keep the voucher register in the new grants system "
                   "from 2027.", BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_annual(path):
    import datetime as dt
    title = "Enhanced Inspection Program: 2024 Annual Report"
    d, frame = _doc(path, title)
    reg = S.register()
    lst = [x for x in reg.s if x["start"] <= dt.date(2024, 12, 31)]
    rows = [["Station", "Name", "Town", "County", "At 31 Dec 2024"]]
    for x in sorted(lst, key=lambda x: (x["county"], x["no"])):
        st = "closed %d %s" % (x["end"].day, x["end"].strftime("%b %Y")) if x["end"] and x["end"].year == 2024 else "licensed"
        rows.append([x["no"], x["name"], x["town"], x["county"], st])
    s = [Paragraph("Enhanced Inspection Program<br/>2024 Annual Report", TITLE),
         Paragraph("%s, %s. 20 March 2025." % (ORG, W.SECTION), SUB),
         Paragraph("The first year", HEAD),
         Paragraph("The %s began on 2 January 2024 under the State Implementation Plan revision that followed the "
                   "area's reclassification for ozone. Gasoline vehicles of model year 1996 and newer with a gross vehicle "
                   "weight rating of 8,500 pounds or less are inspected every two years by an on-board diagnostics test; "
                   "vehicles of the four newest model years, diesel and electric vehicles are exempt. In the first cycle a "
                   "vehicle's inspection year is set by the last digit of its VIN, even digits in 2024 and odd digits in "
                   "2025, and a vehicle newly registered in the area is inspected when it registers." % W.EIP, BODY),
         Paragraph("The test", HEAD),
         Paragraph("The lane computer reads the vehicle's VIN, readiness monitors, malfunction indicator and stored codes "
                   "through the diagnostic connector; vehicles whose computers do not report a VIN (most built before "
                   "model year 2005) have it typed by the inspector. A vehicle fails when the malfunction indicator is "
                   "commanded on with a stored code, or when too few monitors are ready; it may be retested free of charge "
                   "within 45 days. The inspector records the odometer from the instrument panel. The test fee is $24, of "
                   "which the station keeps $18.", BODY),
         Paragraph("Waivers and enforcement", HEAD),
         Paragraph("An owner who spends $650 on emissions repairs and still fails may apply for a one-cycle waiver. The "
                   "Division of Motor Vehicles does not renew a registration until the vehicle has passed or holds a "
                   "waiver; vehicles whose registration has lapsed are not called for inspection until they renew.", BODY),
         Paragraph("Stations", HEAD),
         Paragraph("Stations licensed in 2024, by county. A station number is the number of its licence.", BODY),
         _table(rows, [0.7 * inch, 2.2 * inch, 1.2 * inch, 1.1 * inch, 1.5 * inch])]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


DICT = [
    ("vehicle_registrations_2026-07-01.csv", "Division of Motor Vehicles registration snapshot for the twelve member "
     "counties, run on 6 July 2026 as of 1 July 2026. One row per registration record on file: a vehicle has one record "
     "per county it has been registered in since 1 January 2024. record_status: ACTIVE, the current registration; "
     "TRANSFERRED, a record closed when the vehicle was registered in another county; CANCELLED, a title cancelled "
     "(destroyed, exported or retired); EXPIRED, a registration not renewed within 60 days of its expiry. status_date is "
     "the date of the record's last status change or renewal. county_no is the Division's county number. fuel_code: G "
     "gasoline, F flex-fuel, H gasoline-electric hybrid, D diesel, E electric. gvwr_class: 1 up to 6,000 pounds, 2a "
     "6,001 to 8,500, 2b 8,501 to 10,000. owner_type: IND individual, BUS business, GOV government, LSR lessor."),
    ("eip_inspections_2024_2025.csv", "Enhanced Inspection Program test records, 2 January 2024 to 31 December 2025, "
     "extracted 12 January 2026. One row per test. test_type INITIAL is a vehicle's first test of the cycle, and an "
     "attempt aborted before it is completed; RETEST is a test after a failure. vin as read from the vehicle's computer "
     "(vin_source OBD) or typed by the inspector (KEYED); plate and model_year as the lane software found them on the "
     "registration file. odometer as the inspector entered it, in odometer_unit (KM where the odometer reads in "
     "kilometres); the inspector enters 0 or 999999 when the odometer cannot be read. test_start is local time."),
    ("eip_station_register_2026-06-30.xlsx", "Stations licensed at 30 June 2026. licensed_since is the date the "
     "current licence was issued; county is the station's location."),
    ("nox_running_rates_cy2027.xlsx", "Table 2 of the program guidelines: running exhaust NOx in grams per mile for "
     "calendar year 2027 by model year and program class."),
    ("registration_body_codes.csv", "The Division's body codes and the program class each maps to."),
    ("county_codes.csv", "The member counties: Division county number, FIPS county code and county seat."),
    ("vrp_pilot_vouchers_2025.xlsx", "The 2025 pilot's voucher register as the program office kept it, exported 20 "
     "January 2026. One row per voucher; applicant_county_no is the county of the vehicle's registration on the "
     "application."),
    ("vrp_pilot_dismantler_invoices_2025.csv", "The three pilot dismantlers' invoice lines as exported by their billing "
     "systems, June 2025 to January 2026. One row per vehicle on an invoice; tow_zone 0 for a vehicle driven in."),
    ("vrp_pilot_close_out_2025.pdf", "The pilot's close-out report."),
    ("eip_annual_report_2024.pdf", "The inspection program's first annual report."),
    ("dot_county_vmt_2025.csv", "State %s: annual vehicle miles traveled on public roads in each county in 2025, all "
     "vehicle types including through traffic, by functional class, from its traffic count program." % W.DOT),
    ("gasoline_sales_by_county_2025.csv", "State Department of Revenue: taxable gasoline gallons reported by retailers "
     "in each county, by month, 2025."),
    ("county_population_estimates_2025.csv", "State Demographer's estimates of resident population and households at 1 "
     "July 2025."),
]


def write_dictionary(path):
    title = "Notes on the extracts"
    d, frame = _doc(path, title)
    s = [Paragraph("Vehicle Retirement Program 2027<br/>Notes on the extracts", TITLE),
         Paragraph("%s, %s. 14 September 2026." % (ORG, W.SECTION), SUB)]
    for fn, txt in DICT:
        s.append(Paragraph(fn, HEAD))
        s.append(Paragraph(txt, BODY))
    d.build(s, onFirstPage=frame, onLaterPages=frame)
