"""task249's documents: the audience policy, the analytics tag's notes, the paywall and accounts notes, the platform's
monthly report, the paywall log workbook and the editions register."""
import datetime as dt
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import params as P
import postprocess

HEAD, ENG, ACC, SALES = (P.PEOPLE[k] for k in ("head", "analytics", "accounts", "sales"))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.5,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.9, leading=10.2, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.9, leading=9.6)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EAF0"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def _sections(s, sec, body, h2):
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))


# ------------------------------------------------------------------ the audience policy
def policy(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Audience figures for advertisers", HEAD, "Definitions for the 2029 media kit")
    s = [Paragraph("%s: audience figures for advertisers" % P.ORG, h1),
         Paragraph("Definitions for the 2029 media kit, which quotes the fourth quarter of 2028. Approved 4 December "
                   "2028 by %s, head of audience data. Replaces the definitions of November 2027; section 4 is new."
                   % HEAD, small), Spacer(1, 4)]
    sec = [
        ("1. Scope", [
            "The media kit quotes, for each of the twelve local editions of the %s, its digital audience, its sold "
            "copies and its newsletter subscribers. Advertisers buy local packages on these figures, so each one is "
            "defined once, here, and the head of audience data certifies the kit's figures before the kit goes to "
            "advertisers on 1 February 2029." % P.PAPER]),
        ("2. Unique browsers", [
            "An edition's unique browsers in a calendar month (Europe/Berlin) are the browsers that loaded at least one "
            "of the edition's pages that month. A browser counts once, however many identifiers the analytics tag gave "
            "it in the month, and a browser that read two editions counts in both. Automated traffic and the "
            "newsroom's own addresses are left out.",
            "The kit quotes the quarter's figure: the average of its three monthly figures."]),
        ("3. The reported figure", [
            "The kit prints, for each edition, the analytics platform's users for the quarter: the platform's distinct "
            "identifiers for the edition in each month of the quarter, averaged over the three months. The platform "
            "filters automated traffic and the newsroom's addresses out of its reports."]),
        ("4. The measurement note", [
            "From the 2029 kit, an edition whose reported figure for the quarter exceeds its unique browsers for the "
            "quarter by more than 25 per cent carries this note beside the figure: <i>Reported users include browsers "
            "counted more than once; see the methods page.</i> An edition at or below 25 per cent is printed without "
            "it. The note applies to the digital figure only."]),
        ("5. Sold copies", [
            "Sold copies follow the IVW's rules for daily newspapers: the paid copies of each publication day, "
            "averaged over the edition's publication days in the quarter. A publication day's paid copies are one for "
            "each paid subscription that day, whatever it is delivered as, and every single copy sold at retail "
            "(delivered less returned).",
            "Trial and free copies are not paid. A paused subscription's copies are not sold on the days they are not "
            "delivered; a copy forwarded to a holiday address, or donated to a school by the subscriber, is delivered "
            "and sold. The papers appear Monday to Saturday, except on public holidays in the edition's state "
            "(Hesse or Rhineland-Palatinate)."]),
        ("6. Newsletter subscribers", [
            "Each edition has its morning newsletter, sent as a group of the one local-newsletter list. The kit quotes "
            "the edition's subscribers at the end of the quarter's last day (Berlin time): contacts whose subscription "
            "was confirmed and active, in the edition's group. A contact in two groups counts in both."]),
        ("7. Rounding", [
            "Unique browsers and the reported figure to the nearest browser, sold copies to the nearest copy, "
            "subscribers exact; the comparison in section 4 is made before rounding."]),
    ]
    _sections(s, sec, body, h2)
    doc.build(s, onFirstPage=_footer("%s, audience data. Internal." % P.ORG), onLaterPages=_footer("%s, audience data. Internal." % P.ORG))
    postprocess.scrub(path, P.ORG, "2028-12-04T16:20:00")


# ------------------------------------------------------------------ the analytics tag's notes
def tag_notes(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Analytics tag: notes for the data team", ENG, "The site's analytics tag and its export")
    s = [Paragraph("Analytics tag on rhenhagener-anzeiger.de: notes for the data team", h1),
         Paragraph("%s, web analytics. Revised 9 January 2029." % ENG, small), Spacer(1, 4)]
    sec = [
        ("The identifier", [
            "The tag keeps its identifier, the client_id, in a first-party cookie (<i>_rhm_id</i>) that its script "
            "writes on our domain and writes again on every page view, with an expiry of 400 days. A client_id is a "
            "random number, a point, and the second (Unix time) at which the cookie was first written.",
            "Since 2019 WebKit's tracking prevention limits a cookie that a page's script writes, and any other storage "
            "a script writes, to seven days from its last write. WebKit is Safari's engine on the Mac and, on iPhone "
            "and iPad, the engine of every browser: Safari, Chrome, Firefox, Edge and the browsers inside apps. A reader "
            "who comes back to us on WebKit after more than seven days without a page view arrives with a new "
            "client_id. On other browsers the cookie lasts."]),
        ("The session export", [
            "One row per session (30 minutes without a hit ends a session); session_start and session_end are the "
            "session's first and last hits, in UTC. content_group is the edition, read from the page's path. "
            "device_category, browser and os are the platform's reading of the user agent; on iPhone and iPad, Chrome, "
            "Firefox and Edge appear under their own names and the browsers inside apps as Safari (in-app). ip_prefix "
            "is the address with its last part set to zero. user_ref is set when the reader is signed in: the SHA-256 "
            "of <i>rhm-</i> followed by the account number, its first 20 hexadecimal characters. is_bot is the "
            "platform's automated-traffic flag.",
            "The platform's reports count users as distinct client_ids and filter out automated traffic and the "
            "newsroom's addresses (%s); the export keeps every session." % P.NEWSROOM_PREFIX]),
        ("Changes in the fourth quarter", [
            "1 November 2028: Hollerfeld's pages moved from /hollerfeld-kreis/ to /hollerfeld/, and its content group "
            "changed from HKR to HOL.",
            "21 November 2028: the export job ran twice for the sessions that started between 03:00 and 09:00 UTC; "
            "those sessions appear twice, the second copy identical to the first. The platform's reports were not "
            "affected."]),
    ]
    _sections(s, sec, body, h2)
    doc.build(s, onFirstPage=_footer("Web analytics. Internal."), onLaterPages=_footer("Web analytics. Internal."))
    postprocess.scrub(path, P.ORG, "2029-01-09T11:05:00")


# ------------------------------------------------------------------ the paywall and accounts notes
def paywall_notes(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Paywall and reader accounts", ACC, "How the meter, the wall and sign-in work")
    s = [Paragraph("Paywall and reader accounts: how they work", h1),
         Paragraph("%s, paywall and reader accounts. Written for the data team, 20 December 2028." % ACC, small), Spacer(1, 4)]
    sec = [
        ("The meter and the wall", [
            "Metered articles are free up to five a calendar month. Since 1 March 2028 the sixth asks the reader to "
            "register a free account (until then the paywall showed a subscription offer after the tenth). A signed-in "
            "reader reads without a meter.",
            "The meter is kept on the reader's device, in the browser storage our paywall script writes, and starts "
            "again on the first of each month. A reader who deletes our site data starts again as well."]),
        ("Accounts", [
            "An account's origin is how it was opened: <i>registration</i> at the wall or on the sign-up page; "
            "<i>digital subscription</i>, bought online; <i>print subscription</i>, when a print subscriber activates "
            "digital access with the subscriber number (open to every print subscriber since 2019). home_edition is "
            "the edition the reader chose, as it stands today."]),
        ("Sign-in", [
            "The account service keeps a reader signed in with its own login cookie, set by our server for 180 days, "
            "one for each browser: its id is the device_id. The sign-in register lists, for each account and device, "
            "every client_id the analytics tag carried while the reader was signed in on that device in the fourth "
            "quarter, with the first and last signed-in session."]),
        ("The paywall log", [
            "One row each time the wall was shown in the fourth quarter: when (Berlin time, as the paywall console "
            "writes it), the client_id, the edition, the outcome (registered, subscribed, or closed without either) and "
            "when the meter that reached the wall started counting."]),
    ]
    _sections(s, sec, body, h2)
    doc.build(s, onFirstPage=_footer("Paywall and reader accounts. Internal."), onLaterPages=_footer("Paywall and reader accounts. Internal."))
    postprocess.scrub(path, P.ORG, "2028-12-20T09:40:00")


# ------------------------------------------------------------------ workbooks
HFILL = PatternFill("solid", fgColor="DDE3EA")


def report_xlsx(path, rep):
    wb = Workbook()
    ws = wb.active
    ws.title = "Users by month"
    months = ["Jan 2028", "Feb 2028", "Mar 2028", "Apr 2028", "May 2028", "Jun 2028", "Jul 2028", "Aug 2028",
              "Sep 2028", "Oct 2028", "Nov 2028", "Dec 2028"]
    ws.append(["Users (distinct client_ids) by content group and month, Europe/Berlin. Filters: automated traffic, "
               "internal traffic (newsroom). Exported 8 January 2029."])
    ws.append([])
    ws.append(["Content group"] + months)
    for c in ws[3]:
        c.font = Font(bold=True); c.fill = HFILL
    for _, row in rep.iterrows():
        ws.append([row["content_group"]] + [None if pd.isna(row[m]) else int(row[m]) for m in range(1, 13)])
    for r in ws.iter_rows(min_row=4, min_col=2):
        for c in r:
            c.number_format = "#,##0"
    ws.column_dimensions["A"].width = 15
    for i in range(2, 14):
        ws.column_dimensions[get_column_letter(i)].width = 10.5
    ws.freeze_panes = "B4"
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2029-01-08T10:12:00")
    postprocess.finish_office(path, "2029-01-08T10:12:00Z", "2029-01-08T10:12:00Z", P.ORG)


def paywall_xlsx(path, PW):
    wb = Workbook()
    ws = wb.active
    ws.title = "Wall shown"
    ws.append(["shown", "client_id", "edition", "outcome", "meter_started"])
    for c in ws[1]:
        c.font = Font(bold=True); c.fill = HFILL
    outc = {"registration": "registered", "subscription": "subscribed", "closed": "closed"}
    for t, cid, ed, out, since in zip(PW["shown_local"], PW["client_id"], PW["edition"], PW["outcome"], PW["since_local"]):
        ws.append([t.strftime("%d.%m.%Y %H:%M"), cid, ed, outc[out], since.strftime("%d.%m.%Y %H:%M")])
    ws.column_dimensions["A"].width = 17; ws.column_dimensions["B"].width = 23; ws.column_dimensions["E"].width = 17
    ws.freeze_panes = "A2"
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2029-01-03T08:30:00")
    postprocess.finish_office(path, "2029-01-03T08:30:00Z", "2029-01-03T08:30:00Z", P.ORG)


def editions_table():
    rows = []
    kreis = {"HE": "Rhenhagen-Land", "RP": "Kreis Hollerfeld"}
    hh = {"RHS": 61800, "KBR": 48200, "ALH": 21900, "WBR": 33600, "HOL": 29400, "SOW": 27100, "MST": 31800,
          "GRH": 18900, "EIT": 22400, "BST": 17600, "LDN": 23300, "FKR": 20700}
    for e in P.EDITIONS:
        rows.append((e["code"], e["name"], e["state"], kreis[e["state"]], hh[e["code"]],
                     P.OLD_CODE.get(e["code"], "")))
    return pd.DataFrame(rows, columns=["edition", "name", "state", "district", "households_2022", "former_content_group"])
