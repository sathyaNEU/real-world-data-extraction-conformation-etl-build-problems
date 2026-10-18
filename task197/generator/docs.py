"""task197: the governing documents, the register, the settlement files and the distractors."""
import os, csv, zipfile, shutil, datetime as dt
import numpy as np
from reportlab import rl_config
rl_config.invariant = 1          # fixed PDF dates and document ids, so a rebuild is byte-identical
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("Body9", parent=ss["BodyText"], fontName="Helvetica", fontSize=9, leading=12.5))
    ss.add(ParagraphStyle("H1x", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, spaceAfter=6))
    ss.add(ParagraphStyle("H2x", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=10, spaceAfter=4))
    ss.add(ParagraphStyle("Small", parent=ss["BodyText"], fontName="Helvetica", fontSize=7.5, leading=9.5,
                          textColor=colors.HexColor("#555555")))
    return ss

def pdf(path, title, blocks, author="", subject=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ss = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=18*mm, bottomMargin=16*mm, title=title, author=author,
                            subject=subject, creator="", producer="")
    flow = []
    for kind, body in blocks:
        if kind == "h1": flow.append(Paragraph(body, ss["H1x"]))
        elif kind == "h2": flow.append(Paragraph(body, ss["H2x"]))
        elif kind == "p": flow.append(Paragraph(body, ss["Body9"])); flow.append(Spacer(1, 3))
        elif kind == "small": flow.append(Paragraph(body, ss["Small"]))
        elif kind == "gap": flow.append(Spacer(1, body))
        elif kind == "table":
            data, widths = body
            t = Table(data, colWidths=widths, hAlign="LEFT")
            t.setStyle(TableStyle([
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333")),
                ("LINEBELOW", (0, 1), (-1, -2), 0.25, colors.HexColor("#cccccc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ]))
            flow.append(t); flow.append(Spacer(1, 5))
    doc.build(flow)

def normalise_zip(path, when=(2026, 10, 13, 9, 0, 0)):
    """Rewrite a zip container (xlsx) with fixed entry timestamps so rebuilds match byte for byte."""
    import re as _re
    with zipfile.ZipFile(path) as z:
        items = []
        for i in sorted(z.infolist(), key=lambda i: i.filename):
            data = z.read(i.filename)
            if i.filename == "docProps/core.xml":
                # openpyxl stamps the save time on every save; fix it so rebuilds match
                data = _re.sub(rb"<dcterms:modified([^>]*)>[^<]*</dcterms:modified>",
                               rb"<dcterms:modified\1>2026-10-13T09:00:00Z</dcterms:modified>", data)
            if i.filename == "docProps/app.xml":
                # the writing library names itself in the extended properties, which no workbook the
                # desk exports would carry; the application is the desk's own reporting tool
                data = _re.sub(rb"<Application>[^<]*</Application>",
                               rb"<Application>Veerkracht Flex reserve reporting</Application>", data)
                data = _re.sub(rb"<AppVersion>[^<]*</AppVersion>", rb"<AppVersion>4.2</AppVersion>", data)
            items.append((i.filename, data))
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    shutil.move(tmp, path)


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n"); w.writerow(header); w.writerows(rows)
    return len(rows)


def technical_conditions(path, tso):
    pdf(path, "%s FCR technical conditions 2026" % tso, [
        ("h1", "%s: technical conditions for frequency containment reserve (FCR)" % tso),
        ("small", "Edition 2026-07-01. Applies to every reserve-providing unit and reserve-providing group "
                  "prequalified for the FCR product. Supersedes edition 2025-07-01."),
        ("h2", "1. The product"),
        ("p", "FCR is procured in six four-hour delivery blocks per delivery day, running from 00:00 local time. "
              "Capacity is contracted symmetrically: a reserve-providing unit holding a contracted FCR capacity "
              "of C megawatts owes an upward response of up to C megawatts at low system frequency and a "
              "downward response of up to C megawatts at high system frequency."),
        ("h2", "2. The response characteristic"),
        ("p", "The response owed at any instant follows a linear characteristic in the frequency deviation. "
              "There is no response obligation inside a dead band of plus or minus 10 millihertz. Beyond the "
              "dead band the obligation rises linearly with the deviation and reaches the full contracted "
              "capacity at a deviation of 200 millihertz. The response owed is therefore C multiplied by the "
              "deviation beyond the dead band divided by 190 millihertz, capped at C, and is delivered as a "
              "change in active power at the connection point in the direction that opposes the deviation."),
        ("p", "A unit shall reach the response owed within 30 seconds of the deviation arising and shall sustain "
              "it for as long as the deviation persists."),
        ("h2", "3. Prequalification and re-prequalification"),
        ("p", "Prequalification is by witnessed step test against the characteristic in clause 2, repeated on "
              "material change to the unit, its controller or its connection. A provider whose own performance "
              "review finds a unit delivering less than 90 per cent of the response its contracted "
              "characteristic requires shall withdraw that unit from the reserve portfolio and present it for "
              "re-prequalification. The provider shall notify the system operator of the withdrawal, and of the "
              "unit withdrawn, before the start of the delivery month to which it applies."),
        ("p", "Witnessing capacity is limited. One re-prequalification test per provider per delivery month is "
              "scheduled; a provider withdrawing more than one unit in a month shall carry the remainder at "
              "zero contracted capacity until a test slot is available."),
        ("h2", "4. Performance review"),
        ("p", "The provider is responsible for reviewing the delivered response of each unit in its portfolio "
              "against the characteristic in clause 2, on the system frequency published by the system operator "
              "and on its own metering and high-resolution records. The system operator reviews the aggregate "
              "response of the reserve-providing group and does not attribute aggregate performance to "
              "individual units."),
        ("h2", "5. Programme and reserve"),
        ("p", "A reserve-providing unit may follow a market programme while providing reserve. The response owed "
              "under clause 2 is additional to the active power the unit would deliver under its programme, and "
              "nothing in a unit's programme reduces the response owed. A unit withdrawn from reserve by its "
              "provider for any part of a delivery block, including for a control-system alarm or an energy "
              "limitation, holds no response obligation for that part of the block and shall be reported as "
              "unavailable capacity for it."),
        ("h2", "6. Settlement"),
        ("p", "Capacity is settled per delivery block on the contracted capacity held available. Energy "
              "delivered under clause 2 is not separately settled. Metered volumes at the connection point are "
              "settled against the provider's nominated programme under the imbalance settlement rules."),
        ("small", "Rijksnet publishes system frequency at one-second resolution for every deviation beyond 75 "
                  "millihertz, and a minute summary for every day. Document reference RN-TC-FCR-2026-07."),
    ], author=tso, subject="FCR technical conditions")


def performance_standard(path, org, tol, window_from, window_to, as_of):
    pdf(path, "%s reserve performance standard v4" % org, [
        ("h1", "%s: reserve performance standard" % org),
        ("small", "Version 4, effective 2026-07-01. Owner: reserve portfolio desk. Replaces version 3 "
                  "(2025-09-01)."),
        ("h2", "1. Purpose"),
        ("p", "This standard sets out how the desk measures what each contracted site delivers against the "
              "response its FCR contract requires, and how the desk decides which site to withdraw when the "
              "system operator's technical conditions call for a re-prequalification."),
        ("h2", "2. The measure"),
        ("p", "A site's <b>realised response gain</b> over a review window is the active power the site "
              "delivered in excess of the output it would have produced at that second had the system frequency "
              "stayed inside the dead band, divided by the frequency deviation beyond the dead band, taken at "
              "the extreme second of each qualifying episode in a settlement period for which the site was "
              "contracted, averaged with equal weight across those episodes, and expressed as a percentage of "
              "the gain the site's contract requires, which is its contracted FCR capacity divided by 190 "
              "millihertz. The figure is reported to the nearest whole per cent."),
        ("p", "A <b>qualifying under-frequency episode</b> is a period in which the published system frequency "
              "is at or below 49.920 hertz for at least 15 consecutive seconds; its extreme second is the "
              "second of its lowest published frequency, and the earliest such second where more than one "
              "second carries it. A <b>qualifying over-frequency episode</b> is a period in which the published "
              "frequency is at or above 50.080 hertz for at least 15 consecutive seconds, its extreme second "
              "being the second of its highest published frequency on the same tie-break. Upward and downward "
              "response are reviewed separately and are never averaged together."),
        ("p", "Episodes in a settlement period the site was not contracted for are out of scope, as are the "
              "parts of a delivery block for which the site was withdrawn from reserve."),
        ("h2", "3. The review window and the decision"),
        ("p", "The review window for a delivery month is the reserve quarter to date, ending with the last "
              "delivery date before the desk's determination. For the determination dated %s the window runs "
              "from %s to %s inclusive." % (as_of.strftime("%-d %B %Y"), window_from.strftime("%-d %B %Y"),
                                            window_to.strftime("%-d %B %Y"))),
        ("p", "A site whose realised response gain on under-frequency episodes is below %.0f per cent of the "
              "gain its contract requires is outside tolerance. Where the system operator's single monthly "
              "test slot is to be used, the desk withdraws the one site whose realised response gain sits "
              "furthest below the gain its contract requires, and carries the remaining sites that are outside "
              "tolerance at their contracted capacity until a further slot is available." % tol),
        ("h2", "4. Reserve capacity held available"),
        ("p", "The reserve capacity hours the portfolio held available in a delivery block over a review window "
              "are the contracted capacity of each site committed to that block multiplied by the hours of the "
              "block, less, for each site, its contracted capacity multiplied by the hours of that block in "
              "which the site was not holding reserve; the shortfall is the difference between the two. The "
              "hours counted are the hours in which the site was in fact not holding reserve, and the control "
              "platform's event log is the desk's record of them. Capacity hours are summed over the window's "
              "delivery dates and reported in megawatt hours to one decimal place."),
        ("h2", "5. Imbalance exposure outside reserve"),
        ("p", "In a settlement period for which a site holds no delivery-block commitment the whole difference "
              "between the energy the site delivers and the energy its market programme sets for that period "
              "falls to the desk's own imbalance position, and upward and downward exposure are priced "
              "separately. The desk therefore reports, for each site and for the portfolio, the energy "
              "delivered above programme and the energy delivered below programme over the review window, "
              "each as a positive quantity in megawatt hours, summed over those periods and rounded once at "
              "the end. A site's delivered energy for a period is the net volume its own settlement meters "
              "register for that site over the period; its programme energy is the setpoint the control "
              "platform held for that period taken over the quarter hour."),
        ("p", "The system operator's settlement statements carry the volumes it settles for each metering "
              "point, with a grid loss adjustment at connections above 110 kilovolts, and the desk reconciles "
              "them to its own meters on the monthly settlement run."),
        ("small", "Document reference VKF-STD-RP-004. Review annually or on a change to the system operator's "
                  "technical conditions."),
    ], author=org, subject="Reserve performance standard")


def availability_report(path, tso, org, month, blocks_pct, group_id):
    rows = [["Delivery block", "Contracted capacity (MW, mean)", "Group availability (%)"]]
    for (b, mw, pct) in blocks_pct:
        rows.append([b, "%.2f" % mw, "%.2f" % pct])
    pdf(path, "%s FCR group availability %s" % (tso, month), [
        ("h1", "%s: FCR group availability statement" % tso),
        ("small", "Reserve-providing group %s (%s). Delivery month %s. Issued on the fifth working day of the "
                  "following month." % (group_id, org, month)),
        ("p", "Availability is measured on the aggregate response of the reserve-providing group against the "
              "group's contracted capacity, sampled at every deviation beyond the dead band and weighted by "
              "the seconds of deviation. The statement is issued at group level; the system operator does not "
              "attribute group availability to individual reserve-providing units."),
        ("table", (rows, [38*mm, 58*mm, 40*mm])),
        ("p", "No capacity payment adjustment arises for this delivery month. Availability below 98.00 per cent "
              "in two consecutive delivery months is reviewed with the provider."),
        ("small", "Document reference RN-AV-%s-%s." % (group_id, month.replace(" ", "").replace("-", ""))),
    ], author=tso, subject="FCR group availability")
