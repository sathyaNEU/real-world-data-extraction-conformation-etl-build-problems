"""The mutual's own documents: the indemnity standard that files the index, and the trustees' pack for
the meeting the review is on the agenda for.

The standard files what the index is and what the mutual's evidence base is. It says nothing about how the
estimate is made: no channel pairing, no independence, no estimator, and no mention of the fund-return
request log. The pack carries the agenda and the membership position and no index, no case figure and no
recommendation.
"""
import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, spaceAfter=4,
                    spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)
CELL = ParagraphStyle("c", fontName="Times-Roman", fontSize=8, leading=10)
CELLB = ParagraphStyle("cb", fontName="Times-Bold", fontSize=8, leading=10)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.45, 0.45, 0.45)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.90, 0.90, 0.88)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)])

# The sentences the verifier reads back out of each PDF, as positive controls on the same code path.
CONTROL = {
    "indemnity_standard_v6.pdf": "whether or not the member's own systems recorded them",
    "trustee_pack_2027_07.pdf": "Membership position at 31 March 2027",
}


ORG = b"Kelverstone Mutual secretariat"


def _pad(old):
    """A replacement of exactly the length it replaces, so byte offsets the file records stay valid."""
    return ORG[:len(old)].ljust(len(old), b" ")


def scrub(path):
    """Take the writing library's name out of the shipped bytes and put the issuing organisation in its
    place (reduce-house-fixes H1). The producer value carries escaped parentheses, so the closing bracket
    is found by scanning with the escape rule rather than by a regex, and every substitution keeps the
    original byte length. The caller re-opens the file afterwards, which is the control on this."""
    data = bytearray(open(path, "rb").read())
    for comment in (b"ReportLab Generated PDF document (opensource)",
                    b"ReportLab generated PDF document -- digest (opensource)"):
        i = data.find(comment)
        while i != -1:
            data[i:i + len(comment)] = _pad(comment)
            i = data.find(comment)
    key = b"/Producer ("
    i = data.find(key)
    while i != -1:
        j = i + len(key)
        while j < len(data):
            if data[j:j + 1] == b"\\":
                j += 2
                continue
            if data[j:j + 1] == b")":
                break
            j += 1
        data[i + len(key):j] = _pad(data[i + len(key):j])
        i = data.find(key, j)
    open(path, "wb").write(bytes(data))
    return path


class _Canvas(canvas.Canvas):
    """The documents are the mutual's own, so they carry the secretariat as their producer rather than
    the writing library's name (reduce-house-fixes H1). Set on the canvas rather than patched into the
    shipped bytes, because the library's own default carries escaped parentheses and a byte-level
    substitution over it leaves an invalid dictionary."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.setProducer("Kelverstone Mutual secretariat")
        self.setCreator("Kelverstone Mutual secretariat")


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm)


def wrap(rows):
    return [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]


def standard(target):
    path = os.path.join(target, "indemnity_standard_v6.pdf")
    d = _doc(path, "Kelverstone Mutual indemnity standard")
    f = [
        Paragraph("Kelverstone Mutual Indemnity Association: indemnity standard", H1),
        Paragraph("Version 6, approved by the trustees on 19 May 2026 and effective for indemnity years "
                  "beginning on or after 1 October 2026. Parts 1 to 3, Part 6 and schedules 1 to 4 are "
                  "not reproduced in this extract.", SMALL),

        Paragraph("Part 2 Cover", H2),
        Paragraph("2.1 The mutual indemnifies a member for reimbursements the member makes to its own "
                  "customers under the scheme's reimbursement rules where the customer was deceived into "
                  "sending a payment, which this standard calls a scam case, and separately for losses "
                  "the member bears on payments its customer did not authorise, which this standard "
                  "calls unauthorised fraud. The two covers are rated separately and are not combined in "
                  "any figure this Part requires.", BODY),
        Paragraph("2.2 Cover attaches to the member that sent the payment. Where a member receives a "
                  "payment another firm's customer sent, the case belongs to the sending firm and the "
                  "mutual indemnifies no part of it.", BODY),

        Paragraph("Part 4 The scam incidence index", H2),
        Paragraph("4.1 The trustees set a scam incidence index for each member whose triennial "
                  "experience review falls in the cycle. The index is the measure on which the mutual "
                  "places its loss-control programme and sets the member's contribution loading, and it "
                  "is recorded in the minute of the meeting at which it is set.", BODY),
        Paragraph("4.2 A member's scam incidence index is the number of scam cases arising from payments "
                  "its own customers sent in the scheme year ended 31 March, whether or not the member's "
                  "own systems recorded them, counted once a case however many payments it covers, per "
                  "million payments sent as reported on the member's revised quarterly returns for that "
                  "year. The index is estimated on the mutual's evidence base as it stands when the "
                  "review is prepared, being the members' case registers and the scheme's "
                  "beneficiary account register.", BODY),
        Paragraph("4.3 An index set at the trustees' summer meeting applies to the indemnity year "
                  "beginning on the following 1 October and is measured over the scheme year ended the "
                  "preceding 31 March. An index is not re-measured during an indemnity year.", BODY),
        Paragraph("4.4 The experience review presents the index as a walk from the member's recorded "
                  "case count, through the cases its own record did not hold, to its indexed case count, "
                  "in that order, and states the index to the nearest whole case per million payments "
                  "sent.", BODY),
        Paragraph("4.5 A member's review is prepared by the underwriting and pricing lead and is put to "
                  "the trustees with the membership position at the close of the scheme year.", BODY),

        Paragraph("Part 5 Settlement and recoveries", H2),
        Paragraph("5.1 The mutual settles with each member monthly by advice, one advice per cover per "
                  "month, and the advice states the amount settled and the number of case lines it "
                  "covers.", BODY),
        Paragraph("5.2 Recoveries belong to the mutual to the extent of the indemnity it has paid and "
                  "are credited against the case they arise on, at the date the funds arrive.", BODY),
        Spacer(1, 4 * mm),
        Paragraph("Issued by Debra Dawson, secretary, Kelverstone Mutual Indemnity Association. "
                  "Version 6 supersedes version 5 of 12 June 2023. Next scheduled review May 2028.",
                  SMALL),
    ]
    d.build(f, canvasmaker=_Canvas)
    return scrub(path)


def trustee_pack(target, w):
    path = os.path.join(target, "trustee_pack_2027_07.pdf")
    d = _doc(path, "Trustees meeting pack")
    rows = [["Member", "Code", "Tier", "Joined", "Covers held"]]
    for m in sorted(w["members"], key=lambda x: x["name"]):
        rows.append([m["name"], m["code"], m["tier"], m["joined"].strftime("%d %b %Y"),
                     "scam, unauthorised"])
    t = Table(wrap(rows), colWidths=[52 * mm, 20 * mm, 14 * mm, 28 * mm, 40 * mm], repeatRows=1)
    t.setStyle(TBL)
    f = [
        Paragraph("Kelverstone Mutual: trustees' meeting, 14 July 2027", H1),
        Paragraph("Pack issued by Caleb Ramsey for the secretariat on 2 July 2027. Papers 1 to 3 are "
                  "circulated separately.", SMALL),
        Paragraph("Agenda", H2),
        Paragraph("1. Minutes of the meeting of 11 March 2027 and matters arising. 2. Secretariat "
                  "report. 3. Settlement position "
                  "for the scheme year ended 31 March 2027. 4. Triennial experience reviews for the "
                  "members shown in the register as falling in this cycle, taken together with the "
                  "membership position below. 5. Loss-control programme placement for the indemnity "
                  "year beginning 1 October 2027. 6. Any other business.", BODY),
        Paragraph("Membership position at 31 March 2027", H2),
        Paragraph("Twelve members, all in membership for the whole of the scheme year except as the "
                  "joining dates show. The secretariat has no change of membership to report for the "
                  "coming indemnity year.", BODY),
        t,
        Spacer(1, 3 * mm),
        Paragraph("The reviews at item 4 cover the scheme year ended 31 March 2027 and are prepared "
                  "from the mutual's evidence base as pulled for this meeting on 2 July 2027. "
                  "No index is proposed in this pack; the reviews are tabled at the meeting.", SMALL),
    ]
    d.build(f, canvasmaker=_Canvas)
    return scrub(path)


def write_all(target, w):
    return [standard(target), trustee_pack(target, w)]
