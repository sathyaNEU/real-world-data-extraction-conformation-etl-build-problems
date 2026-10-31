"""The pack's documents: the dental plan's summary plan description, the company's benefit costing standard, the
board's bargaining mandate, Ridgeline's service agreement Schedule C, and Ridgeline's 2025 plan year review and 2026
renewal."""
import datetime as dt

import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10)
STAMPS = {"spd": b"D:20241118094500-06'00'", "costing": b"D:20230314153000-05'00'",
          "mandate": b"D:20260928171200-05'00'", "schedule_c": b"D:20250521110400-05'00'",
          "renewal": b"D:20260218142600-06'00'"}


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch, title=title, author=author, creator=author,
                            subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(0.85 * inch, 0.5 * inch, org + "  |  " + title)
        c.drawRightString(letter[0] - 0.85 * inch, 0.5 * inch, "Page %d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def _table(rows, widths=None, size=8.5):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def P(text, style=BODY):
    return Paragraph(text, style)


def spd_pdf(path):
    s = [P("Pembrook Castings Company Dental Plan", T),
         P("Summary Plan Description. Effective 1 January 2025. Administered by " + W.TPA + ".", SMALL),
         P("Who is covered", H),
         P("Employees who enrol, and their enrolled spouses and children. A child is covered to the end of the month in "
           "which the child turns 26. Coverage begins on the first of the month after 30 days of employment and ends on "
           "the last day of the month in which employment ends."),
         P("Plan year", H),
         P("The plan year is the calendar year. The deductible, the annual maximum and the frequency limits start again "
           "each 1 January."),
         P("What the plan pays", H),
         _table([["Class", "Services", "Plan pays", "Deductible"],
                 ["I", "Evaluations, cleanings, radiographs, fluoride, sealants", "100%", "No"],
                 ["II", "Fillings, extractions, endodontics, periodontics, palliative care", "80%", "Yes"],
                 ["III", "Crowns, buildups, bridges, implants, dentures", "50%", "Yes"]],
                [0.6 * inch, 3.6 * inch, 0.9 * inch, 0.9 * inch]),
         Spacer(1, 6),
         P("The deductible is 50 dollars per covered person per plan year and applies to Class II and Class III "
           "services. The plan pays its share of the network fee for each service, network and non-network dentists "
           "alike; a non-network dentist may bill you for the difference between its charge and the network fee."),
         P("Annual maximum", H),
         P("The plan pays up to 1,500 dollars for each covered person in a plan year. Payments for Class I, II and III "
           "services all count toward the annual maximum. Orthodontic payments do not."),
         P("Frequency limits", H),
         P("Two evaluations and two cleanings per plan year; one set of bitewing radiographs per plan year; one "
           "panoramic radiograph in any 36 months; sealants on permanent molars once per tooth to age 15."),
         P("Orthodontic benefit", H),
         P("For a covered child who is under 19 when the appliance is placed, the plan pays 50 per cent of the "
           "orthodontist's case fee up to a lifetime maximum of 1,500 dollars per child. The plan pays a quarter of its "
           "benefit when the appliance is placed and the rest in equal monthly installments over the months of "
           "treatment, while the child is covered. If the child changes orthodontist, the new orthodontist's case is "
           "paid under the same lifetime maximum."),
         P("Predetermination of benefits", H),
         P("When your dentist expects treatment to cost more than 300 dollars, ask the dentist to send Ridgeline a "
           "predetermination before the work begins. Ridgeline's estimate shows what the plan expects to pay at the "
           "time it is issued. An estimate is valid for 12 months from its issue date and is not a guarantee of payment: "
           "the plan pays under the plan's terms when the work is done."),
         P("Claims", H),
         P("Your dentist sends claims to " + W.TPA + ", which decides them under the plan's terms. If a claim is "
           "corrected, the corrected claim replaces the original."),
         Spacer(1, 8),
         P("Plan sponsor: " + W.COMPANY + ", Human Resources. Plan administrator: the company's Benefits Committee.",
           SMALL)]
    _pdf(path, "Dental Plan Summary Plan Description 2025", s, W.PEOPLE["benefits"], W.COMPANY)


def costing_pdf(path):
    s = [P("Finance Policy F-17: Costing Benefit Plan Changes", T),
         P(W.COMPANY + ". Adopted by the Finance Committee of the Board on 14 March 2023.", SMALL),
         P("1. Purpose", H),
         P("This policy sets how the company costs a change to a self-insured benefit plan, whether the change is "
           "proposed by management or in collective bargaining, so that every proposal is costed on one basis."),
         P("2. Costing basis", H),
         P("A proposed change is costed as what the plan would have paid for the covered persons of the most recent "
           "complete plan year had the change applied to that plan year, at the fees in effect for the plan year in "
           "which the change would take effect. The result is stated per covered person month of that plan year's "
           "enrolment."),
         P("3. Cost of a proposal", H),
         P("The cost of a proposal is its costed amount per covered person month less the same plan year's costed "
           "amount at the current plan design, at the same fees."),
         P("4. Records", H),
         P("Costing uses the claims administrator's records of the plan year, with the claims for the plan year's "
           "services decided after it ends, through the date of the costing."),
         P("5. Presentation", H),
         P("Amounts per covered person month are stated to the cent. The costing is signed by the Benefits Manager and "
           "reviewed by the Vice President, Finance."),
         Spacer(1, 8),
         P("Approved: " + W.PEOPLE["finance"] + ", Vice President, Finance.", SMALL)]
    _pdf(path, "Finance Policy F-17", s, W.PEOPLE["finance"], W.COMPANY)


def mandate_pdf(path):
    s = [P("Board Resolution 2026-31: Bargaining Mandate, Dental Plan", T),
         P(W.COMPANY + ", Board of Directors. Adopted at the meeting of 28 September 2026.", SMALL),
         P("Whereas the collective bargaining agreement with the union representing the company's hourly employees "
           "expires on 31 December 2026; and whereas the union's proposal of 9 September 2026 asks that the Dental "
           "Plan's annual maximum be raised from 1,500 dollars to 3,000 dollars per covered person from 1 January 2027;"),
         P("<b>Resolved</b>, that the company's bargaining committee may agree to an annual maximum of 2,000 dollars or "
           "of 3,000 dollars per covered person from 1 January 2027, the plan otherwise unchanged, provided its cost "
           "under Finance Policy F-17 is no more than 1.90 dollars per covered person month;"),
         P("<b>Resolved further</b>, that the bargaining committee reports the costing to the Board with its "
           "recommendation before the bargaining session of 12 November 2026."),
         Spacer(1, 10),
         P("Attest: " + W.PEOPLE["finance"] + ", Vice President, Finance, for the Secretary.", SMALL)]
    _pdf(path, "Board Resolution 2026-31", s, W.PEOPLE["finance"], W.COMPANY)


def schedule_c_pdf(path):
    hol = [d for d in W.HOLIDAYS if d.year in (2025, 2026)]
    s = [P("Administrative Services Agreement: Schedule C, Service Standards", T),
         P(W.TPA + " and " + W.COMPANY + ". Schedule C as amended 21 May 2025, effective 1 July 2025 for the plan's "
           "move to Ridgeline's current adjudication platform.", SMALL),
         P("C.1 Claims", H),
         P("Ridgeline decides 95 per cent of clean claims within 10 business days of receipt."),
         P("C.2 Predeterminations", H),
         P("Ridgeline issues an estimate for every procedure in a predetermination request within five business days of "
           "receipt for at least 90 per cent of the requests received in each calendar quarter. The standard is "
           "measured on the requests received in the quarter."),
         P("C.3 Business days and receipt", H),
         P("A business day is Monday to Friday, except Ridgeline's observed holidays listed below. A request received "
           "after 5:00 p.m. Central Time, or on a day that is not a business day, is received on the next business day."),
         _table([["Observed holiday", "2025", "2026"]] + [
             [name, next("%d %s %d" % (d.day, d.strftime("%B"), d.year) for d in hol if d.year == 2025 and f(d)),
              next("%d %s %d" % (d.day, d.strftime("%B"), d.year) for d in hol if d.year == 2026 and f(d))]
             for name, f in (("New Year's Day", lambda d: d.month == 1), ("Memorial Day", lambda d: d.month == 5),
                             ("Independence Day", lambda d: d.month == 7), ("Labor Day", lambda d: d.month == 9),
                             ("Thanksgiving Day", lambda d: d.month == 11 and d.weekday() == 3),
                             ("Day after Thanksgiving", lambda d: d.month == 11 and d.weekday() == 4))]
             + [["Christmas", ", ".join("%d %s %d" % (d.day, d.strftime("%B"), d.year) for d in hol if d.year == 2025 and d.month == 12),
                 ", ".join("%d %s %d" % (d.day, d.strftime("%B"), d.year) for d in hol if d.year == 2026 and d.month == 12)]],
             [2.2 * inch, 1.9 * inch, 1.9 * inch]),
         Spacer(1, 6),
         P("C.4 Member service", H),
         P("Ridgeline answers 85 per cent of member calls within 30 seconds, measured monthly."),
         P("C.5 Reporting", H),
         P("Ridgeline reports the standards in C.1 to C.4 to the company each quarter within 30 days of the quarter's "
           "end.")]
    _pdf(path, "ASO Agreement Schedule C", s, W.PEOPLE["tpa"], W.TPA)


def renewal_figures(w):
    """The administrator's plan-year review: paid claims per enrolled employee per month for 2024 and 2025 as decided
    by 31 January 2026, and the 2025 figure it projected in October 2024 from 2024's claims at the 2025 fees."""
    people = {p["pid"]: p for p in w["people"] if p["kind"] == "E"}
    months = {y: sum(W.member_months(p, y) for p in people.values()) for y in (2024, 2025)}
    paid = {2024: 0, 2025: 0}
    demand24 = {}
    for c in w["claims"]:
        y = c["dos"].year
        if y not in paid or c["adjudicated"] > dt.date(2026, 1, 31):
            continue
        lines = w["adjust"][c["cid"]]["lines"] if c["cid"] in w["adjust"] and \
            w["adjust"][c["cid"]]["date"] <= dt.date(2026, 1, 31) else c["lines"]
        paid[y] += sum(ln["paid"] for ln in lines)
        if y == 2024 and c["adjudicated"] <= dt.date(2024, 9, 30):
            for ln in lines:
                if ln["reason"] == "FRQ":
                    continue
                v = (W.FEES[2025][ln["code"]] - ln["ded"]) * W.COINS[W.plan_class(ln["code"])] // 100
                demand24[c["pid"]] = demand24.get(c["pid"], 0) + v
    m24 = sum(W.member_months(people[pid], 2024) for pid in people)
    proj = sum(min(v, W.MAXIMUM) for v in demand24.values())
    # the October 2024 projection ran on January to September 2024 claims, annualised on the same months
    m24_9 = sum(min(9, W.member_months(people[pid], 2024)) for pid in people)
    return dict(months=months, paid=paid, pmpm={y: paid[y] / 100.0 / months[y] for y in paid},
                proj25=proj / 100.0 / max(1, m24_9) if m24 else 0.0)


def renewal_pdf(path, w):
    f = renewal_figures(w)
    s = [P("2025 Plan Year Review and 2026 Renewal", T),
         P(W.COMPANY + " Dental Plan. Prepared by " + W.TPA + ", Account Management, 18 February 2026.", SMALL),
         P("1. Experience", H),
         _table([["Plan year", "Employee months", "Paid claims", "Paid per employee per month"],
                 ["2024", "{:,}".format(f["months"][2024]), "{:,.2f}".format(f["paid"][2024] / 100.0),
                  "%.2f" % f["pmpm"][2024]],
                 ["2025", "{:,}".format(f["months"][2025]), "{:,.2f}".format(f["paid"][2025] / 100.0),
                  "%.2f" % f["pmpm"][2025]]],
                [1.0 * inch, 1.6 * inch, 1.5 * inch, 1.9 * inch]),
         Spacer(1, 6),
         P("Paid claims are for services in the plan year decided by 31 January 2026, at the plan's design (1,500 "
           "dollar annual maximum, 50 dollar deductible, 100/80/50 coinsurance)."),
         P("2. The 2025 projection", H),
         P("Our October 2024 renewal projected 2025 at %.2f dollars per employee per month: January to September 2024 "
           "claims re-priced at the 2025 network fees, each covered person's plan payments held to the annual maximum, "
           "per employee month of the same months. The 2025 plan year came in at %.2f." % (
               f["proj25"], f["pmpm"][2025])),
         P("3. 2026 renewal", H),
         P("The 2026 network fee schedule took effect on 1 January 2026. The administrative fee for 2026 is 4.38 dollars "
           "per enrolled employee per month. No change to the plan design is proposed for 2026."),
         Spacer(1, 8),
         P("Account executive: " + W.PEOPLE["tpa"] + ".", SMALL)]
    _pdf(path, "2025 Plan Year Review", s, W.PEOPLE["tpa"], W.TPA)
    return f


def write_all(t, w):
    spd_pdf(t("spd"))
    costing_pdf(t("costing"))
    mandate_pdf(t("mandate"))
    schedule_c_pdf(t("schedule_c"))
    return renewal_pdf(t("renewal"), w)
