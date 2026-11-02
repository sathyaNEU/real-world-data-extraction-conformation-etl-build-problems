"""task304 architecture 4: the three governing and context documents, as PDFs (reportlab, invariant output)."""
import datetime as dt
import os

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
from io_util import scrub_pdf

rl_config.invariant = 1

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.2, spaceAfter=4)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=13.5, spaceBefore=6, spaceAfter=3)

ZONE_NAMES = {
    "LAR": ("Induct area", "Sort and dock floor", "Meal room"),
    "ECR": ("Induction zone", "Chute and dock area", "Crib room"),
    "TRU": ("Induct deck", "Sortation floor and docks", "Amenities"),
    "WFD": ("Induct line", "Floor (chutes and docks)", "Lunch room"),
    "KEW": ("Induct area", "Sort and dock floor", "Crib room"),
    "BFD": ("Induction", "Dock and chute floor", "Meal room"),
}
PRICE = {"LAR": 486400, "ECR": 611900, "TRU": 402750, "WFD": 351300, "KEW": 418600, "BFD": 309850}


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=author,
                             producer=author)


def _table(rows, widths, head=True):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999999")), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if head:
        st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8ECEF"))]
    t.setStyle(TableStyle(st))
    return t


def survey(out, pk):
    path = os.path.join(out, "noise_survey_report_2026.pdf")
    d = _doc(path, "Occupational noise survey 2026 - sortation hubs", "Kestrel Acoustics Pty Ltd", "KA-2611-R1")
    s = [Paragraph("Occupational noise survey 2026: Brolga Parcel Network sortation hubs", H1),
         Paragraph("Kestrel Acoustics Pty Ltd, report KA-2611-R1, issued 30 September 2026. Prepared for Brolga Parcel "
                   "Network Pty Ltd, National WHS.", SMALL), Spacer(1, 4),
         Paragraph("1. Scope", H2),
         Paragraph("Area measurements at the six sortation hubs during normal production on weekday shifts between 4 "
                   "August and 18 September 2026, to the measurement method of AS/NZS 1269.1. Sound level meters were "
                   "Class 1, field-calibrated before and after each run. Each area's level is the A-weighted equivalent "
                   "continuous level (LAeq) over the positions measured in it, energy-averaged across the production "
                   "periods sampled; the highest C-weighted peak recorded in the area is shown beside it.", BODY),
         Paragraph("2. Results by hub", H2)]
    rng_pos = {"LAR": (14, 9, 2), "ECR": (18, 12, 2), "TRU": (10, 8, 2), "WFD": (8, 7, 1), "KEW": (10, 8, 2), "BFD": (7, 6, 1)}
    peaks = {"LAR": (118, 109, 84), "ECR": (124, 112, 86), "TRU": (121, 108, 82), "WFD": (115, 106, 80), "KEW": (120, 109, 83), "BFD": (117, 107, 82)}
    dates = {"LAR": "4-6 August", "ECR": "11-13 August", "TRU": "18-20 August", "WFD": "25-26 August", "KEW": "1-3 September", "BFD": "16-18 September"}
    for h in P.HUBS:
        c = h["code"]
        zi, zf, za = ZONE_NAMES[c]
        npos = rng_pos[c]
        pk_ = peaks[c]
        rows = [["Area", "Positions", "LAeq dB(A)", "LCpeak max dB(C)"],
                [zi, str(npos[0]), "%.1f" % h["Li"], str(pk_[0])],
                [zf, str(npos[1]), "%.1f" % h["Lf"], str(pk_[1])],
                [za, str(npos[2]), "%.1f" % h["La"], str(pk_[2])]]
        s.append(Paragraph("%s (%s, %s), measured %s 2026" % ({"LAR": "Larapinta", "ECR": "Eastern Creek", "TRU": "Truganina",
                                                               "WFD": "Wingfield", "KEW": "Kewdale", "BFD": "Beresfield"}[c],
                                                              h["city"], h["state"], dates[c]), BODY))
        s.append(_table(rows, [62 * mm, 22 * mm, 28 * mm, 34 * mm]))
        s.append(Spacer(1, 5))
    s.append(Paragraph("3. Notes", H2))
    s.append(Paragraph("Office areas measured below 60 dB(A) at every hub and are not tabulated. Peaks at every hub are "
                       "below 140 dB(C). Instruments and calibration certificates are held on file KA-2611.", BODY))
    d.build(s)


def design(out, pk):
    path = os.path.join(out, "induct_enclosure_design_report_rev2.pdf")
    d = _doc(path, "Induct line acoustic enclosure - design report rev 2", "Quellmark Acoustic Engineering",
             "QAE-0927 rev 2")
    s = [Paragraph("Induct line acoustic enclosure: design report, revision 2", H1),
         Paragraph("Quellmark Acoustic Engineering, project QAE-0927, 22 October 2026. Client: Brolga Parcel Network "
                   "Pty Ltd.", SMALL), Spacer(1, 4),
         Paragraph("1. Scope", H2),
         Paragraph("A partial enclosure of the induct conveyor drives and merge section, with absorptive panels over the "
                   "induct stations and a lined canopy, designed for each hub's induct line. The design basis is the "
                   "client's 2026 noise survey (KA-2611-R1) and the induct stations in use as the sorter control "
                   "system's operator session export for 28 September to 9 October 2026 records them.", BODY),
         Paragraph("2. Predicted levels and price", H2)]
    rows = [["Hub", "Induct stations", "Induct area now LAeq dB(A)", "Predicted after enclosure LAeq dB(A)", "Price ex GST (AUD)"]]
    for h in P.HUBS:
        c = h["code"]
        rows.append([{"LAR": "Larapinta", "ECR": "Eastern Creek", "TRU": "Truganina", "WFD": "Wingfield", "KEW": "Kewdale",
                      "BFD": "Beresfield"}[c], str(h["stations"]), "%.1f" % h["Li"], "%.1f" % h["Lp"], "{:,}".format(PRICE[c])])
    s.append(_table(rows, [30 * mm, 24 * mm, 36 * mm, 46 * mm, 32 * mm]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Predicted levels are at the induct operator positions with the line at normal production. The "
                       "enclosure does not change levels on the sort and dock floor or in the amenities.", BODY))
    s.append(Paragraph("3. Programme", H2))
    s.append(Paragraph("Fabrication twelve weeks from order; installation over three weekends with the line stopped. "
                       "Revision 2 supersedes revision 1 (29 September 2026), which priced the Eastern Creek canopy in "
                       "two sections.", BODY))
    d.build(s)


def undertaking(out, pk):
    path = os.path.join(out, "noise_enforceable_undertaking_schedule_2027.pdf")
    d = _doc(path, "Enforceable undertaking (noise) - 2027 schedule", "Brolga Parcel Network Pty Ltd",
             "EU-N-2026 Schedules 2 and 3")
    s = [Paragraph("Enforceable undertaking (noise): schedule of commitments for 2027", H1),
         Paragraph("Brolga Parcel Network Pty Ltd. Schedules 2 and 3 to the undertaking accepted on 14 August 2026. "
                   "Issued by Brent Roberts, National WHS Manager, 6 November 2026.", SMALL), Spacer(1, 4),
         Paragraph("1. Background", H2),
         Paragraph("Brolga gave this undertaking after an improvement notice on noise at one of its sortation hubs. Brolga "
                   "commits to a national hearing conservation program, to one engineering noise control in 2027 placed "
                   "as Schedule 2 sets out, and to audiometric testing as Schedule 3 sets out.", BODY),
         Paragraph("Schedule 2. The 2027 engineering control", H2)]
    sched2 = [
        "2.1 In 2027 Brolga will install one acoustic enclosure of an induct line, to the supplier's design report "
        "revision 2, at the hub where it brings the most workers from at or above the exposure standard to below it.",
        "2.2 The workers of a hub are every employee and every labour-hire operative who worked at least one shift at the "
        "hub that began between 12 October and 8 November 2026 (the reference weeks), a shift belonging to the date it "
        "began.",
        "2.3 A worker's exposure is their daily noise exposure, LAeq,8h, over the shifts they worked in the reference "
        "weeks: the A-weighted sound energy of the places they worked during each shift and of the amenities during its "
        "breaks, normalised to eight hours and energy-averaged over those shifts. A shift is eight hours, with one hour of "
        "breaks taken in the amenities. A place's level is its LAeq in the 2026 noise survey.",
        "2.4 A worker is at or above the exposure standard when their exposure is 85 dB(A) or more.",
        "2.5 A worker's exposure after the enclosure is their exposure recomputed with the hub's induct area at the level "
        "the design report predicts for that hub, every other place unchanged and the worker's shifts as they were.",
        "2.6 By 31 January 2027 Brolga will give the regulator the hub chosen and, for every hub, its workers at or above "
        "the exposure standard and the workers the enclosure would bring below it.",
    ]
    for t in sched2:
        s.append(Paragraph(t, BODY))
    s.append(Paragraph("Schedule 3. Audiometric testing", H2))
    sched3 = [
        "3.1 A standard threshold shift is an average worsening of 10 dB or more in the hearing thresholds at 2, 3 and 4 "
        "kHz in either ear, against the worker's reference audiogram.",
        "3.2 A shift is confirmed when a retest within 30 days of the test that showed it shows it again against the same "
        "reference; a shift not retested within 30 days is not confirmed.",
        "3.3 A worker's reference audiogram is their first test in the program; when a shift is confirmed, the confirming "
        "retest is their reference from its date.",
        "3.4 A confirmed shift belongs to the hub the worker was employed at on the date of the confirming retest.",
    ]
    for t in sched3:
        s.append(Paragraph(t, BODY))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Schedule 4 (program reporting) and Schedule 5 (training) are unchanged from the undertaking as "
                       "accepted.", SMALL))
    d.build(s)


def write_docs(out, pk):
    survey(out, pk)
    design(out, pk)
    undertaking(out, pk)
    for name in ("noise_survey_report_2026.pdf", "induct_enclosure_design_report_rev2.pdf",
                 "noise_enforceable_undertaking_schedule_2027.pdf"):
        scrub_pdf(os.path.join(out, name))
