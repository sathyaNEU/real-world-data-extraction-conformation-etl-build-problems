"""task250 documents: the tracking data standard TDS-4 (pdf) and the director of network operations' request (eml)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P

DOMAIN = "kurierwarta.pl"
HEAD = ("Inga Blaut", "i.blaut")
LINEHAUL = ("Krzysztof Konieczek", "k.konieczek")
INTEGRATION = ("Aurelia Pieczyrak", "a.pieczyrak")


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.0, leading=9.8)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def standard(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "TDS-4 Tracking data standard, version 4.1", P.ORG, "Standard")
    s = [Paragraph("%s, Tracking Data Quality" % P.ORG, small),
         Paragraph("TDS-4 Tracking data standard", h1),
         Paragraph("Version 4.1, issued 2 March 2026, in force from the April 2026 scorecard. Replaces version 4.0 "
                   "(September 2024). Owner: the Head of Tracking Data Quality.", small), Spacer(1, 4)]
    sec = [
        ("1. Purpose and scope", [
            "Every parcel Kurier Warta carries is known to its shippers, its recipients and the claims desk only "
            "through the records the tracking platform holds: the shippers' pre-advices, the couriers' handheld "
            "events at collection and delivery, the sorters' events at the sort hubs and the delivery depots' "
            "arrival scans. This standard sets the measures the Tracking Data Quality team reports for each "
            "calendar month, the alert that sends a scan audit to a sort hub, and how a month's figures are "
            "fixed. It applies to every hub and depot in the network register."]),
        ("2. Sort scan completeness", [
            "2.1 A sort hub handles a parcel when it sorts the parcel for the delivery depot that unloads it. Every "
            "parcel a delivery depot unloads was sorted by one hub on the night before. A month's parcels are the "
            "parcels the delivery depots unloaded on the mornings of that month, and a hub's parcels for the month "
            "are the month's parcels it sorted.",
            "2.2 A missed sort scan is one of a hub's parcels for the month for which the platform holds no sort "
            "event. A hub's missed-scan rate is its missed sort scans as a per cent of its parcels for the month.",
            "2.3 The scan alert fires for a sort hub when its missed-scan rate for the month is above 1.00 per cent. "
            "A fired alert sends the scan audit (section 5) to the hub."]),
        ("3. Events sent twice", [
            "3.1 The platform keeps every record a source sends it. A source has sent an event twice when the "
            "platform receives a further record of a scan it already holds; the scan is one event sent twice however "
            "many further records arrive.",
            "3.2 A courier event belongs to the depot the event names."]),
        ("4. Pre-advices", [
            "4.1 A shipper pre-advises each consignment before it is collected, naming the collection depot, the "
            "collection date and the pieces; each piece is one parcel. A later version of a consignment replaces "
            "the earlier versions in full.",
            "4.2 A parcel is pre-advised for a month's collection when the latest version of its consignment names "
            "a collection date in that month.",
            "4.3 A pre-advice naming a depot code that the network register shows replaced is read as naming the "
            "replacing depot from the day that depot opened.",
            "4.4 A pre-advised parcel was never picked up when Kurier Warta never collected it from the shipper."]),
        ("5. The scorecard and the scan audit", [
            "5.1 The team publishes each month's scorecard in the first working week of the next month, from the "
            "platform as it stands on the morning the month's extract is taken. A record reaching the platform "
            "after the extract does not reopen the month.",
            "5.2 A scan audit is two auditors at the hub for two consecutive sort nights. They follow the induction, "
            "the chutes and the scanner arches, read the arches' fault logs and file their findings with the hub "
            "manager within five working days. An alert stands until the hub's rate for a later month is at or "
            "below the tolerance."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Paragraph("6. Document control", h2))
    s.append(_grid([["Version", "Issued", "Change"],
                    ["3.2", "May 2022", "Sort scan completeness by hub; tolerance 1.50 per cent"],
                    ["4.0", "September 2024", "Courier events and pre-advices added (sections 3 and 4)"],
                    ["4.1", "March 2026", "Tolerance for sort scans 1.00 per cent; latest version of a pre-advice "
                                          "(4.1); replaced depot codes (4.3)"]],
                   [22 * mm, 30 * mm, 118 * mm], cell))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Approved by the Chief Operating Officer, 27 February 2026.", small))
    doc.build(s, onFirstPage=_footer("TDS-4 v4.1  |  " + P.ORG), onLaterPages=_footer("TDS-4 v4.1  |  " + P.ORG))


def _mail(who):
    return "%s <%s@%s>" % (who[0], who[1], DOMAIN)


def request(path):
    text = f"""From: {_mail(LINEHAUL)}
To: Analityka <analityka@{DOMAIN}>
Cc: {_mail(HEAD)}, {_mail(INTEGRATION)}
Date: Fri, 06 Nov 2026 09:12:44 +0100
Subject: October tracking scorecard
Message-ID: <20261106091244.4417.kkonieczek@{DOMAIN}>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Dzień dobry,

Inga tells me the October extract came off the platform at 07:40 this
morning, so the scorecard can go ahead. I need it before the peak briefing
on Monday. The peak crews start on the night of 9 November, and a hub whose
scan alert fires gets its audit in the first two weeks of the peak, so the
audit nights have to go into the hub rosters now.

Aurelia takes the depot lines to her monthly call with the shippers'
integration teams on Wednesday.

The workbook and the slide go to the operations board as usual.

Pozdrawiam,
Krzysztof

--
{LINEHAUL[0]}
Director of Network Operations
{P.ORG}
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
