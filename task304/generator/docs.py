"""The three documents: the Trust's plan for the van's 2027 setting (the estimand), the network's 2026 testing and
treatment pathway, and the integrated care board's commissioning intentions for 2027/28. Each is a short operational
paper in its issuer's voice."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.4, leading=17, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _foot(text):
    def f(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()
    return f


def _table(rows, widths, size=8.4):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.4)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EAEE")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


SAVED = {"2026-10-06": ("091840", "164512", "+01'00'"), "2026-04-22": ("083015", "120944", "+01'00'"),
         "2026-09-15": ("100212", "113655", "+01'00'")}


def _pdf(path, title, author, subject, story, foot, stamp, producer):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=producer, subject=subject,
                            invariant=1)
    doc.build(story, onFirstPage=_foot(foot), onLaterPages=_foot(foot))
    postprocess.scrub(path, producer, stamp)
    postprocess.pdf_clock(path, *SAVED[stamp])


def plan(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Find-and-treat van: the 2027 setting", h1),
         Paragraph("Brannock Trust, outreach team. Plan for the trustees, 6 October 2026. %s, outreach team lead."
                   % P.TEAM_LEAD, small), Spacer(1, 6),
         Paragraph("1. The decision", h2),
         Paragraph("From Monday 4 January 2027 the van works full-time in one setting, five days a week, for the whole "
                   "of 2027, in place of the 2026 rota. The trustees will choose the setting where the van would start "
                   "the most people on hepatitis C treatment in 2027.", body),
         Paragraph("2. How the van works", h2),
         Paragraph("A peer worker offers a hepatitis C test to the people the van meets in the setting: a finger-prick "
                   "antibody test, and an RNA test on the van's analyser from the same sample when the antibody test is "
                   "reactive. The nurse prescribes on the van and the first pack is collected from the clinic pharmacy. "
                   "The van does not test again anyone it has already found with an active infection; the nurse follows "
                   "them up.", body),
         Paragraph("3. The four settings", h2),
         Paragraph("The approved premises: Holloway House, Bracken Lodge and Tanner's Yard, 110 places, where residents "
                   "stay about eleven weeks. The city hostels: nine hostels run by Fenwold Housing Trust and Calder "
                   "Street Homes, 920 places. Fenwold Recovery's new entrants: everyone starting a new treatment episode "
                   "at the Recovery hub on Gorse Street. The needle exchange pharmacies' new registrants: people "
                   "registering for needle exchange at one of the city's 24 pharmacies for the first time.", body),
         Paragraph("4. What we count", h2),
         Paragraph("A person is tested when they accept the van's test, and found when the van's RNA test shows an "
                   "active infection. A person found is started when they begin a course of treatment within twelve "
                   "weeks of the van's test. People found and started are counted in the year of the van's test, and "
                   "we count only the people the van itself tests, finds and starts. Each setting is sized at the van's "
                   "own rates there in 2026: the share of the people offered a test who took one, and the share of the "
                   "people found who started treatment within twelve weeks.", body),
         Paragraph("5. The people the van would meet in 2027", h2),
         Paragraph("We take the residents of the approved premises and of the hostels on 30 September 2026 as the "
                   "people living there when the van starts in January, and each setting's arrivals in the twelve "
                   "months to 30 September 2026 as its arrivals in 2027, each month standing for the same month of "
                   "2027: new residents at the approved premises and the hostels, new treatment episodes at the "
                   "Recovery hub, and first registrations at the pharmacies.", body),
         Paragraph("6. The 2026 rota", h2),
         Paragraph("The van worked Mondays and Tuesdays at the hostels, Wednesdays at the pharmacies, Thursdays at the "
                   "Recovery hub and Fridays at the approved premises, from 5 January to 25 September 2026. Its contacts "
                   "are in the tablet export and the courses it started are on the network's treatment register. The "
                   "van is off the road from October to December for its refit and the new analyser.", body)]
    _pdf(path, "Find-and-treat van: the 2027 setting", P.TEAM_LEAD, "Plan for the trustees", s,
         "Brannock Trust. Registered charity. Outreach team, 6 October 2026", "2026-10-06", P.ORG)


def pathway(path):
    body, h1, h2, small = _styles()
    clin = ", ".join(P.CLINIC_NAME[c] for c in P.CLINICS[:-1]) + " and the " + P.CLINIC_NAME[P.CLINICS[-1]]
    s = [Paragraph("Hepatitis C testing and treatment pathway, 2026", h1),
         Paragraph("%s. Issued April 2026 by %s, clinical lead. Replaces the 2024 pathway." % (P.NETWORK, P.CLIN_LEAD),
                   small), Spacer(1, 6),
         Paragraph("1. Testing", h2),
         Paragraph("An antibody test shows whether a person has ever been infected; it stays reactive after a cure and "
                   "after an infection clears on its own. An RNA test shows whether the infection is active. %s tests "
                   "every reactive antibody sample for RNA." % P.LAB, body),
         Paragraph("2. Prescribing and supply", h2),
         Paragraph("Courses are prescribed by the network's five clinics: the %s. Glecaprevir with pibrentasvir is "
                   "given for 8 weeks and sofosbuvir with velpatasvir for 12 weeks. Each clinic's pharmacy supplies a "
                   "course in 28-day packs, collected as the last pack runs out." % clin, body),
         Paragraph("3. The end of a course and a cure", h2),
         Paragraph("A course of treatment ends with its last dose. A cure is confirmed by an RNA test showing "
                   "hepatitis C RNA not detected on a sample taken 84 days (twelve weeks) or more after the last dose. "
                   "An RNA result of detected, at any level, is not a cure. A course that does not cure is followed "
                   "where possible by a new course, which has its own outcome.", body),
         Paragraph("4. Testing again", h2),
         Paragraph("People who continue to inject are offered an RNA test every twelve months after a cure, and an "
                   "antibody test every twelve months while they have never been infected.", body),
         Paragraph("5. Records", h2),
         Paragraph("Clinics record each course on the network's treatment register. The register moved to the "
                   "network's new clinical system on 1 October 2024, with new clinic codes.", body)]
    _pdf(path, "Hepatitis C testing and treatment pathway 2026", P.CLIN_LEAD, P.NETWORK, s,
         "%s. Pathway 2026, version 1.0" % P.NETWORK, "2026-04-22", P.NETWORK)


def intentions(path):
    body, h1, h2, small = _styles()
    rows = [["Ref", "Service", "Intention", "From"],
            ["PH-01", "NHS Health Checks", "Recommissioned through the four primary care networks", "1 April 2027"],
            ["PH-02", "Stop smoking services", "Pharmacy stop smoking offer extended to every community pharmacy",
             "1 April 2027"],
            ["PH-03", "Sexual health", "Integrated service to be retendered; current contract extended for twelve "
             "months", "1 April 2027"],
            ["PH-05", "Supervised consumption", "Fee per supervised dose uplifted by 3.2 per cent", "1 April 2027"],
            ["PH-07", "Adult drug and alcohol treatment (Fenwold Recovery)", "Contract extended to 31 March 2029; no "
             "change to the service", "1 April 2027"],
            ["PH-09", "Take-home naloxone", "Supply added to every pharmacy providing needle and syringe exchange",
             "1 October 2026"],
            ["PH-12", "Community pharmacy hepatitis C testing and treatment", "Test and treat for needle and syringe "
             "exchange clients at every pharmacy providing needle and syringe exchange", "1 April 2027"],
            ["PH-14", "Hepatitis B vaccination", "Vaccination of needle and syringe exchange clients moved from GP "
             "practices to Fenwold Recovery", "1 July 2027"],
            ["CS-02", "Community nursing", "Single point of access for district nursing referrals", "1 April 2027"],
            ["CS-05", "Homeless health (Riverside)", "Clinic hours extended to Saturday mornings", "1 April 2027"],
            ["CS-08", "Liaison and diversion", "No change", "1 April 2027"],
            ["MH-03", "Community mental health", "Second crisis café, Stanmoor", "1 January 2028"]]
    s = [Paragraph("Commissioning intentions 2027/28: public health and community services", h1),
         Paragraph("%s with Fenwold City Council. Published 15 September 2026." % P.ICB, small), Spacer(1, 6),
         Paragraph("These are the intentions for the services the Board and the Council commission jointly. Providers "
                   "will be notified of each change through the usual contract variation, and services not listed "
                   "continue on their current terms.", body),
         _table(rows, (14, 46, 86, 26))]
    _pdf(path, "Commissioning intentions 2027/28", "Commissioning team", P.ICB, s,
         "%s. Commissioning intentions 2027/28" % P.ICB, "2026-09-15", P.ICB)
