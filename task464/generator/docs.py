#!/usr/bin/env python3
"""task464: the two documents the bundle ships.

`network_agreement_2027_capacity_terms.pdf` is the governing document and the only pin: it files the
population, the unit, the window, the comparison and the standard, and says nothing about how a site's
deliverable treatment positions are found. `licence_fee_schedule_2026.pdf` is a distractor.

Both are written once, deterministically, and re-serialised through pypdf so the writer library's own
signature and timestamp do not ship (reduce-house-fixes H1 and H25).
"""
import datetime as dt
import io
import os

import reportlab.rl_config
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)
from reportlab.lib import colors
import pypdf

import pack
import world

reportlab.rl_config.invariant = 1
ORG = "Harrowgate Community Health Plan"
APPROVER = "Katherine Dalton"
SECOND = "Nicholas Clay"
FICTION_STAMP = dt.datetime(2027, 1, 5, 9, 14, 0)

AGREEMENT = "network_agreement_2027_capacity_terms.pdf"
FEES = "licence_fee_schedule_2026.pdf"


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["BodyText"], fontName="Times-Roman", fontSize=9.5,
                          leading=12.5, alignment=TA_JUSTIFY, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading2"], fontName="Times-Bold", fontSize=11, leading=13,
                        spaceBefore=10, spaceAfter=4)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, alignment=0)
    title = ParagraphStyle("title", parent=ss["Title"], fontName="Times-Bold", fontSize=13.5, leading=16,
                           spaceAfter=2)
    return body, h1, small, title


def _doc(path, story, footer):
    buf = io.BytesIO()
    d = BaseDocTemplate(buf, pagesize=LETTER, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                        topMargin=0.85 * inch, bottomMargin=0.85 * inch, title="", author="",
                        subject="", creator="")
    frame = Frame(d.leftMargin, d.bottomMargin, d.width, d.height, id="f")

    def paint(canv, docu):
        canv.saveState()
        canv.setFont("Times-Roman", 7.5)
        canv.drawString(d.leftMargin, 0.55 * inch, footer)
        canv.drawRightString(LETTER[0] - d.rightMargin, 0.55 * inch, "Page %d" % docu.page)
        canv.restoreState()

    d.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=paint)])
    d.build(story)
    _reserialise(buf.getvalue(), path)


def _reserialise(raw, path):
    r = pypdf.PdfReader(io.BytesIO(raw))
    w = pypdf.PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.add_metadata({"/Title": "", "/Author": "", "/Subject": "", "/Keywords": "",
                    "/Creator": ORG, "/Producer": ORG,
                    "/CreationDate": FICTION_STAMP.strftime("D:%Y%m%d%H%M%S-06'00'"),
                    "/ModDate": FICTION_STAMP.strftime("D:%Y%m%d%H%M%S-06'00'")})
    fixed = pypdf.generic.ByteStringObject(b"\x14\x64\x27\x03\x11\x05\x09\x02" * 2)
    w._ID = pypdf.generic.ArrayObject([fixed, fixed])
    with open(path, "wb") as f:
        w.write(f)


def agreement(target):
    body, h1, small, title = _styles()
    st = []
    st.append(Paragraph("Provider Network Agreement 2027", title))
    st.append(Paragraph("Schedule 4: Outpatient Dialysis and Infusion Capacity and Service Area Adequacy",
                        ParagraphStyle("sub", parent=body, fontName="Times-Bold", fontSize=10,
                                       alignment=1, spaceAfter=10)))
    ctl = Table([["Agreement reference", "PNA-2027-S4"],
                 ["Network year", "1 July 2027 to 30 June 2028"],
                 ["Approved", "%s, %s" % (pack.AGREEMENT_APPROVED.strftime("%d %B %Y"), APPROVER)],
                 ["Network position as at", world.ASOF.strftime("%d %B %Y")],
                 ["Issued by", "%s, network contracting" % ORG]],
                colWidths=[1.85 * inch, 4.0 * inch])
    ctl.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 8.5),
                             ("FONT", (0, 0), (0, -1), "Times-Bold", 8.5),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                             ("TOPPADDING", (0, 0), (-1, -1), 2),
                             ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.black),
                             ("LINEABOVE", (0, 0), (-1, 0), 0.4, colors.black)]))
    st.append(ctl)
    st.append(Spacer(1, 10))

    st.append(Paragraph("4.1 Sites in scope", h1))
    st.append(Paragraph(
        "This Schedule applies to each outpatient dialysis and infusion Site the Plan intends to contract "
        "for the 2027 network year, being each Site recorded with a 2027 contract intent in the Plan's "
        "provider directory on the attestation cycle current at the network position date. Sites "
        "contracted for an earlier network year are not in scope unless they carry that intent, and a "
        "Site's service area is the area recorded against it on that cycle.", body))
    st.append(Paragraph(
        "A Site is identified by its plan site identifier. Where several Sites share a tax identifier or a "
        "licence holder, each remains a separate Site for this Schedule.", body))

    st.append(Paragraph("4.2 Weekly treatment slots", h1))
    st.append(Paragraph(
        "A Site's weekly treatment slots are the treatments the Site can deliver in a week, being its "
        "deliverable treatment positions multiplied by the treatment sessions its roster staffs in a week "
        "and by the treatments a position delivers in a session for the Site's service category. "
        "Deliverable treatment positions means the treatment positions a Site is able to operate "
        "simultaneously.", body))
    st.append(Paragraph(
        "A treatment session is a staffed block in which each position delivers its treatments for that "
        "block. The treatments a position delivers in a session are one for in-centre haemodialysis and "
        "two for ambulatory infusion. The sessions staffed in a week are those on the staffing roster "
        "effective at the network position date.", body))
    st.append(Paragraph(
        "A Site's licensed station count, where used, is the count on the Site's own facility licence row "
        "at its service address, and not a count held at a corporate holder.", body))

    st.append(Paragraph("4.3 Service area adequacy", h1))
    st.append(Paragraph(
        "A service area meets the adequacy standard for the 2027 network year when the weekly treatment "
        "slots of the Sites in scope in that area are at or above 1.15 times the area's projected 2027 "
        "weekly treatment demand.", body))
    st.append(Paragraph(
        "An area's projected 2027 weekly treatment demand is its treatments a week in the 2026 contract "
        "year multiplied by the area's projected growth factor in the Plan's enrolment projection for "
        "2027. The 2026 contract year is the calendar year 2026, and a week is one fifty-second of a "
        "contract year. Treatments a week are counted from the Plan's outpatient treatment encounter "
        "extract, taking the treatments the Sites in scope delivered.", body))

    st.append(Paragraph("4.4 Records and reporting", h1))
    st.append(Paragraph(
        "The treatment encounter extract is taken after the ninety day filing run-out for the last "
        "contract year it covers, so that the 2026 contract year is complete on the extract. Encounters "
        "recorded without a stop time or a recorded length are not delivered treatments.", body))
    st.append(Paragraph(
        "Capacity and adequacy figures are reported in whole treatment slots, with the required figure "
        "rounded once at the area level.", body))
    st.append(Paragraph("4.5 Corrective action", h1))
    st.append(Paragraph(
        "Where an area does not meet the adequacy standard for the network year, the Plan opens a "
        "corrective action for that area within thirty days of the position date, and may contract "
        "additional capacity, extend sessions at a contracted Site or arrange care out of network until "
        "the standard is met. A corrective action does not alter a Site's weekly treatment slots or the "
        "standard the area is measured against.", body))
    st.append(Paragraph("4.6 Service areas", h1))
    st.append(Paragraph(
        "The service areas for the network year are the twelve areas recorded in the Plan's provider "
        "directory on the attestation cycle current at the network position date. A Site sits in one "
        "service area for the network year.", body))
    st.append(Spacer(1, 8))
    st.append(Paragraph(
        "Countersigned for the Plan: %s, provider network operations. Schedule 4 supersedes Schedule 4 of "
        "the 2026 agreement in respect of the 2027 network year only." % SECOND, small))
    _doc(os.path.join(target, AGREEMENT), st,
         "%s  |  Provider Network Agreement 2027, Schedule 4  |  PNA-2027-S4" % ORG)


def fee_schedule(target):
    body, h1, small, title = _styles()
    st = [Paragraph("Outpatient Facility Licensing Fee Schedule", title),
          Paragraph("Effective 1 July 2026", ParagraphStyle("sub", parent=body, fontName="Times-Bold",
                                                            fontSize=10, alignment=1, spaceAfter=10))]
    st.append(Paragraph(
        "Annual licence fees for in-centre haemodialysis and ambulatory infusion facilities are charged on "
        "the station count entered on the facility's licence row at the time of renewal. A facility that "
        "amends its station count mid-term pays the difference between bands pro rata for the remainder of "
        "the licence term.", body))
    rows = [["Licensed stations", "Annual fee", "Renewal surcharge"],
            ["1 to 4", "USD 1,340", "USD 185"], ["5 to 8", "USD 2,105", "USD 240"],
            ["9 to 12", "USD 3,460", "USD 310"], ["13 to 18", "USD 4,925", "USD 395"],
            ["19 or more", "USD 6,780", "USD 480"]]
    t = Table(rows, colWidths=[1.7 * inch, 1.5 * inch, 1.7 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 9),
                           ("FONT", (0, 0), (-1, 0), "Times-Bold", 9),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.black)]))
    st.append(t)
    st.append(Spacer(1, 8))
    st.append(Paragraph(
        "Fees are payable on the anniversary of the licence effective date. A lapsed licence number may be "
        "reissued after twelve months; the reissued licence carries a new effective date and the band is "
        "set from the station count entered at reissue.", body))
    st.append(Paragraph("Fees do not apply to corporate holder registrations.", small))
    _doc(os.path.join(target, FEES), st,
         "State licensing authority  |  Outpatient facility fee schedule  |  FS-2026-07")


def write(target):
    agreement(target)
    fee_schedule(target)
