"""The three documents: the Trust's 2027 van plan (the estimand), the 2019 pilot evaluation and the network's 2026
testing and treatment pathway. Each is a short operational paper in its author's voice."""
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


def _table(rows, widths, size=8.6):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.4)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EAEE")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


SAVED = {"2026-10-06": ("091840", "164512", "+01'00'"), "2020-01-17": ("102233", "151907", "+00'00'"),
         "2026-04-22": ("083015", "120944", "+01'00'")}


def _pdf(path, title, author, subject, story, foot, stamp):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                            invariant=1)
    doc.build(story, onFirstPage=_foot(foot), onLaterPages=_foot(foot))
    postprocess.scrub(path, author, stamp)
    postprocess.pdf_clock(path, *SAVED[stamp])


def plan(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Find-and-treat van: where it works in 2027", h1),
         Paragraph("Brannock Trust. Paper for the trustees' meeting of 12 November 2026. Author: %s, Director of "
                   "Services. Version 2, 6 October 2026." % P.DIRECTOR, small), Spacer(1, 6),
         Paragraph("1. The decision", h2),
         Paragraph("NHS England's elimination fund and the Fenwold Hepatitis C Network have agreed to fund one "
                   "find-and-treat van with us for calendar 2027: a nurse, two peer workers, a point-of-care RNA "
                   "analyser and a fridge. The van works one setting for the whole year, so that the setting's staff "
                   "and residents get to know it. The trustees are asked to choose the setting. The four we have "
                   "been asked to consider are the approved premises (the probation hostels and the CAS3 houses "
                   "people go to on release), the city hostels, Fenwold Recovery's new entrants to structured "
                   "treatment, and the new registrants at the needle exchange pharmacies. None of the four has had "
                   "the van before.", body),
         Paragraph("2. What we count", h2),
         Paragraph("We will place the van where it starts the most people on hepatitis C treatment in 2027. The "
                   "van meets the people arriving in its setting during the year: a resident new to an approved "
                   "premises or a hostel, an entrant to structured treatment, a new registrant at a needle exchange "
                   "pharmacy. A person is counted once in the year however many times they arrive. We take a 2027 "
                   "year's arrivals at the yearly average of each setting's arrivals in the two years to 30 "
                   "September 2026, from the returns each provider sends the commissioners, and we take the people "
                   "arriving in 2027 to be like the people who arrived in those two years.", body),
         Paragraph("The van tests a person for hepatitis C antibody when it meets them and, if the antibody is "
                   "reactive, tests their blood for RNA on the spot. A person the van finds with an active "
                   "infection, RNA detected at that test, counts as started when they start a course within twelve "
                   "weeks of the test. People already part-way through a course when they arrive are carried by the "
                   "van to the end of it, and are counted neither among the active infections it finds nor among "
                   "its starts.", body),
         Paragraph("3. How the van works", h2),
         Paragraph("The van will work as it did in our 2018-19 pilot at the Hope Street day centre and the "
                   "Corrington methadone clinic: it will test the same share of a setting's arrivals as the pilot "
                   "tested of the people arriving at its two sites, and start the same share of the people it finds "
                   "with an active infection within twelve weeks. Robin Higgins' evaluation of the pilot and its "
                   "caseload are attached. The nurse can carry 70 courses at once, including the courses of people "
                   "who arrive part-way through one; the prisons hand over people released before their course ends "
                   "and the van takes those on in the approved premises.", body),
         Paragraph("4. Timetable", h2),
         Paragraph("Trustees decide on 12 November. The van's first week in its setting is 4 January 2027. The "
                   "network will report the van's starts to NHS England each quarter.", body),
]
    _pdf(path, "Find-and-treat van 2027: where it works", P.ORG, "Trustees paper", s,
         "Brannock Trust, registered charity. Trustees' paper, 12 November 2026", "2026-10-06")


def evaluation(path, pilot_rows):
    body, h1, h2, small = _styles()
    by = {}
    for p in pilot_rows:
        k = p["site"]
        b = by.setdefault(k, dict(arr=0, tested=0, react=0, det=0, start12=0))
        b["arr"] += 1
        if p["tested"]:
            b["tested"] += 1
            if p["ab"] == "Reactive":
                b["react"] += 1
                if p["rna"] == "Detected":
                    b["det"] += 1
                    if p["started"] and (p["start_date"] - p["test_date"]).days <= 84:
                        b["start12"] += 1
    name = {"HOPE": "Hope Street day centre", "CORR": "Corrington methadone clinic"}
    rows = [["Site", "Arrived", "Tested by the van", "Antibody reactive", "RNA detected", "Started within 12 weeks"]]
    tot = dict(arr=0, tested=0, react=0, det=0, start12=0)
    for k in ("HOPE", "CORR"):
        b = by[k]
        rows.append([name[k], b["arr"], b["tested"], b["react"], b["det"], b["start12"]])
        for x in tot:
            tot[x] += b[x]
    rows.append(["Both sites", tot["arr"], tot["tested"], tot["react"], tot["det"], tot["start12"]])
    s = [Paragraph("Find-and-treat van pilot, October 2018 to September 2019: evaluation", h1),
         Paragraph("Brannock Trust. %s, outreach team lead. 17 January 2020." % P.TEAM_LEAD, small), Spacer(1, 6),
         Paragraph("What we did", h2),
         Paragraph("For twelve months the van spent two days a week at the Hope Street day centre and two at the "
                   "Corrington methadone clinic. We offered everyone arriving at either site an antibody test from a "
                   "finger-prick, and an on-the-spot RNA test to anyone reactive. People with RNA detected were "
                   "booked with the network's nurse on the van and started on tablets as soon as their bloods were "
                   "back.", body),
         Paragraph("What happened", h2), _table(rows, [52, 20, 26, 26, 22, 30]), Spacer(1, 6),
         Paragraph("We tested %d of the %d people who arrived at the two sites over the year. %d of the %d people "
                   "with RNA detected started treatment within twelve weeks of their test; most of the rest started "
                   "later or moved on before we could book them." % (tot["tested"], tot["arr"], tot["start12"],
                                                                     tot["det"]), body),
         Paragraph("What we learned", h2),
         Paragraph("Testing on the spot works: people who would not go to a clinic will give a finger-prick in a "
                   "place they already use. The RNA result on the day is what gets people started; when we had to "
                   "send a sample away we lost people. Two days a week at each site was about right for a nurse and "
                   "two peers. The day centre was the busier site but the methadone clinic's people were easier to "
                   "keep in touch with.", body),
         Paragraph("The pilot caseload is held by the Trust under its data sharing agreement with the network, with "
                   "each person's network pseudonym.", small)]
    _pdf(path, "Van pilot evaluation 2018-19", P.ORG, "Pilot evaluation", s,
         "Brannock Trust. Find-and-treat van pilot evaluation, January 2020", "2020-01-17")
    return tot


def pathway(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Fenwold Hepatitis C Network: testing and treatment pathway", h1),
         Paragraph("Approved by the network board 22 April 2026. Clinical lead: Dr %s, consultant hepatologist. "
                   "Review due April 2028." % P.CLIN_LEAD, small), Spacer(1, 6),
         Paragraph("1. Testing", h2),
         Paragraph("Peer workers and outreach staff test with an oral or finger-prick antibody kit; a reactive kit "
                   "result is followed by a blood test for RNA, on the van or at a clinic. Fenwold Pathology tests "
                   "every hepatitis C sample sent from the community, the hospital and the network's clinics. A "
                   "sample from a patient with a reactive antibody result already on file at Fenwold Pathology is "
                   "tested for HCV RNA only. A first reactive antibody result is followed by an RNA test on the "
                   "same sample.", body),
         Paragraph("2. Treatment", h2),
         Paragraph("A person with RNA detected is offered treatment by the network: eight weeks of "
                   "glecaprevir/pibrentasvir or twelve weeks of sofosbuvir/velpatasvir, prescribed by the "
                   "hepatology clinic, the community clinic, the Fenwold Recovery clinic, the pharmacy-led clinic "
                   "or the outreach nurse. Every course the network starts is entered in the network's treatment "
                   "register.", body),
         Paragraph("3. Twelve-week test", h2),
         Paragraph("A course ends on its last dose: the planned end for a course completed, the date it stopped "
                   "for a course stopped early. A course lost to follow-up has no last dose on record. A course is "
                   "confirmed as a cure when an RNA test taken twelve weeks or more after the last dose is not "
                   "detected.", body),
         Paragraph("4. Prisons", h2),
         Paragraph("Corvane Health provides healthcare in HMP Fenwold, HMP Sallowby and HMP Mardlow. A person "
                   "released part-way through a hepatitis C course is handed over to the network, which carries the "
                   "course to its end in the community.", body),
         Paragraph("5. After treatment", h2),
         Paragraph("People who go on injecting are offered an RNA test every year. A person found with RNA "
                   "detected after a cure is offered a further course.", body)]
    _pdf(path, "Testing and treatment pathway 2026", P.NETWORK, "Clinical pathway", s,
         "Fenwold Hepatitis C Network. Testing and treatment pathway, April 2026", "2026-04-22")
