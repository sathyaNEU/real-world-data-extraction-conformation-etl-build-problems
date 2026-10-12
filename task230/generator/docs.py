"""The filed documents: QCP-04, the clients' quality schedules and rate cards, the Hollings & Pryce pilot
report, the second-pass labour planning note and the MIS extract notes (dictionary and provenance)."""
import datetime as dt
import os

from docx import Document
from docx.shared import Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import pack
import postprocess
import world as W


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    return dict(body=body, h1=h1, h2=h2, small=small)


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _pdf(path, story, title, author, footer):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, invariant=1)
    doc.build(story, onFirstPage=_footer(footer), onLaterPages=_footer(footer))


def _table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E4E8EE")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _docx(path, build, who, created, modified):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    build(d)
    d.core_properties.author = who
    d.core_properties.last_modified_by = who
    d.save(path)
    postprocess.scrub(path, who, modified[:10])
    postprocess.finish_office(path, created, modified, W.ORG)


# ----------------------------------------------------------------------------------------------- QCP-04
def qcp04(target):
    def build(d):
        d.add_heading("QCP-04 First-pass quality control", level=1)
        d.add_paragraph("Tamralipta Data Services, Salt Lake Sector V capture centre. Controlled procedure, version 5.0, "
                        "effective 1 July 2026. Owner: Head of Operations. Approver: service quality council.")
        d.add_heading("1 Purpose", level=2)
        d.add_paragraph("This procedure sets how the centre measures the accuracy of key fields after first-pass "
                        "verification and decides, month by month, which client streams also go through second-pass verification.")
        d.add_heading("2 Scope", level=2)
        d.add_paragraph("Every client stream captured by OCR and verified on the day or night first-pass queue. Each stream "
                        "is one client's documents of one form type, as listed in the stream register.")
        d.add_heading("3 Definitions", level=2)
        for t in [
            "Key field: a field the client's quality schedule lists as key for the stream's form version. Only key fields are verified and audited.",
            "First-pass verification: a verifier compares each key field's OCR value with the image and keys over any value that differs. The value after first pass is the value the screen submits.",
            "Shift-day: the date a shift starts. A night shift that starts at 20:30 IST on 14 July and ends at 05:30 IST on 15 July belongs to shift-day 14 July.",
            "Residual key-field error rate: key fields whose value after first pass differs from the image, per 1,000 key fields first-pass verified.",
        ]:
            d.add_paragraph(t, style="List Bullet")
        d.add_heading("4 Second-pass verification", level=2)
        d.add_paragraph("4.1 Estimand. For each stream, the first-pass residual key-field error rate for the month: key fields "
                        "first-pass verified on the month's shift-days whose value after first pass differs from the image as the "
                        "blind re-key adjudicates it, per 1,000 key fields first-pass verified, over every document the month's "
                        "operating plan of record routes to the stream's queue.")
        d.add_paragraph("4.2 Rule. A stream is on second-pass verification for the month when its forecast exceeds its contract "
                        "limit (errors per 1,000 key fields, in the client's quality schedule). A forecast equal to the limit stays off.")
        d.add_paragraph("4.3 Records. Every stream's forecast, a new client's included, is made by the same method, from the last "
                        "closed quarter's first-pass log and blind re-key audit and from the operating plan of record for the month.")
        d.add_paragraph("4.4 The head of operations proposes the list for the month; the service quality council signs it before "
                        "the first shift-day of the month.")
        d.add_heading("5 Blind re-key audit", level=2)
        d.add_paragraph("A random share of each stream's documents on every shift is re-keyed blind by two keyers who do not see "
                        "the OCR value or the first-pass value. Where the two keyers disagree a third keyer adjudicates. The "
                        "adjudicated value is the image's value. The share for each stream is held in the stream register. "
                        "Quality reporting runs by shift-day.")
        d.add_heading("6 Records", level=2)
        d.add_paragraph("The first-pass log and field edits are exported from the capture platform, the audit from the QA tool. "
                        "Exports for a quarter are closed once every audited document of the quarter is adjudicated.")
        d.add_heading("7 Document control", level=2)
        t = d.add_table(rows=1, cols=3)
        t.style = "Table Grid"
        for c, h in zip(t.rows[0].cells, ["Version", "Date", "Change"]):
            c.text = h
        for v in [("4.0", "02 Jan 2025", "Night queue added to scope"), ("4.1", "14 Apr 2025", "Shift-day definition"),
                  ("5.0", "24 Jun 2026", "Section 4 restated; council sign-off moved to 4.4")]:
            row = t.add_row().cells
            for c, x in zip(row, v):
                c.text = x
    _docx(os.path.join(target, pack.FILES["qcp"]), build, W.PEOPLE["ops"], "2024-12-18T06:00:00Z", "2026-06-24T10:20:00Z")


# ----------------------------------------------------------------------------------------------- quality schedules
CAPTURE_TEXT = {"KBA": "D01, D02 and D04", "NDS": "KE and KT", "BMC": "DE-1 and DE-2", "HPB": "E10 and E11",
                "WBH": "CAPT and KEY", "CIP": "C1", "WPC": "DATA and TRANS", "TCM": "01 and 02", "HPY": "QA-C"}


def quality_schedules(target, limits):
    S = _styles()
    story = [Paragraph("Client quality schedules, 2026", S["h1"]),
             Paragraph("Extracted from each client's master services agreement with Tamralipta Data Services. Each schedule "
                       "sets the residual limit for the client's streams, the service credit and how the client measures "
                       "the residual in its own audit.", S["body"])]
    for c, cl in W.CLIENTS.items():
        codes = [k for k in W.ORDER if W.STREAMS[k]["client"] == c]
        story.append(Paragraph(f"{cl['name']} (contract currency {cl['ccy']})", S["h2"]))
        rows = [["Stream", "Limit, errors per 1,000 key fields", "Accuracy", "Service credit"]]
        for k in codes:
            lim = limits[k]
            dp = 2 if k == "D6" else 1
            rows.append([W.SID[k], f"{lim:.{dp}f}", f"{100 - lim / 10:.{dp + 1}f}%", f"{W.CREDIT_PCT[k]:g}% of the stream's monthly invoice"])
        story.append(_table(rows, [30 * mm, 50 * mm, 22 * mm, 70 * mm]))
        story.append(Spacer(1, 3 * mm))
        if c == "HPY":
            meas = ("Measurement: from 1 January 2027 the client audits a random sample of delivered documents each quarter. "
                    "Until then the supplier's own blind re-key audit is the measure.")
        else:
            meas = (f"Measurement: the client audits a random sample of delivered claims. The residual for a quarter is the "
                    f"capture-error findings on the sampled claims delivered in the quarter, per 1,000 key fields on those claims, "
                    f"the quarter and the delivery date taken in {cl['tzlabel']} time. Findings coded {CAPTURE_TEXT[c]} are capture "
                    f"errors; every other code is a business decision on the claim. Where a finding is re-reviewed, the re-review "
                    f"replaces the original finding. Key fields per claim follow the form version the claim was captured on.")
        story.append(Paragraph(meas, S["body"]))
        story.append(Paragraph("A service credit is due for a month in which the residual exceeds the limit. The limit is "
                               "compared with the unrounded residual.", S["body"]))
    p = os.path.join(target, pack.FILES["schedules"])
    _pdf(p, story, "Client quality schedules 2026", "Commercial", "Tamralipta Data Services | Commercial | quality schedules extract")
    postprocess.scrub(p, "Commercial", "2026-07-02")


# ----------------------------------------------------------------------------------------------- rate cards
UNIT_TEXT = {"claim": "per claim document captured", "notification": "per first notification of loss captured (one FNOL form)",
             "document": "per document captured (documents arrive in bundles of 25)"}


def rate_cards(target):
    S = _styles()
    story = [Paragraph("Client rate cards, 2026", S["h1"]),
             Paragraph("Unit prices in contract currency. An account's band for a month is set by the documents captured for "
                       "the account across all its streams on shift-days in that calendar month, and the month's invoice "
                       "prices every document captured in the month at that band.", S["body"])]
    for c, b in W.BANDS.items():
        cl = W.CLIENTS[c]
        story.append(Paragraph(f"{cl['name']} ({cl['ccy']}, {UNIT_TEXT[b['unit']]})", S["h2"]))
        rows = [["Band", "Documents in month"] + [W.SID[k] for k in b["price"]]]
        for i, nm in enumerate(b["names"]):
            lo = b["floors"][i]
            hi = b["floors"][i + 1] - 1 if i + 1 < len(b["floors"]) else None
            rng_ = f"{lo:,} to {hi:,}" if hi is not None else f"{lo:,} and over"
            rows.append([nm, rng_] + [f"{b['price'][k][i]:.2f}" for k in b["price"]])
        story.append(_table(rows, [22 * mm, 40 * mm] + [30 * mm] * len(b["price"])))
        if "index" in b:
            d, pct = b["index"]
            story.append(Spacer(1, 2 * mm))
            story.append(Paragraph(f"Indexation: on the contract anniversary, {d:%d %B}, unit prices rise by {pct:.1f}% "
                                   f"(rounded to the nearest 0.0001 of a unit) for documents captured from that shift-day.", S["body"]))
    p = os.path.join(target, pack.FILES["rates"])
    _pdf(p, story, "Client rate cards 2026", "Commercial", "Tamralipta Data Services | Commercial | rate cards")
    postprocess.scrub(p, "Commercial", "2026-04-03")


def indexed_price(base, pct):
    return round(base * (1 + pct / 100.0), 4)


# ----------------------------------------------------------------------------------------------- pilot report
def pilot_report(target, P):
    def build(d):
        d.add_heading("Hollings & Pryce typed claims: pilot report", level=1)
        d.add_paragraph(f"Prepared by {W.PEOPLE['quality']}, Quality, for the service quality council. 6 October 2026.")
        d.add_heading("Pilot", level=2)
        d.add_paragraph(f"Hollings & Pryce sent typed claim documents for first-pass capture on the day queue from "
                        f"{W.PILOT[0]:%d %B} to {W.PILOT[1]:%d %B} 2026, six days a week including Saturdays and the "
                        f"31 August bank holiday, at about {P['docs_per_day']:,} documents a shift-day. Form HPY-T1 carries "
                        f"{len(W.fields('D6', 'HPY-T1'))} key fields. Pilot documents were verified by the day queue's verifiers "
                        f"alongside the other day streams, and every pilot document was re-keyed blind under QCP-04 section 5.")
        d.add_heading("Results", level=2)
        t = d.add_table(rows=1, cols=2)
        t.style = "Table Grid"
        t.rows[0].cells[0].text = "Measure"
        t.rows[0].cells[1].text = "Pilot"
        for a, b in [("Shift-days", f"{P['days']}"), ("Documents captured", f"{P['docs']:,}"),
                     ("Key fields first-pass verified", f"{P['kf']:,}"), ("Key fields audited", f"{P['audited']:,}"),
                     ("OCR key-field error rate (audited)", f"{P['ocr_pct']:.2f}%"),
                     ("Residual after first pass, per 1,000 key fields", f"{P['residual']:.2f}")]:
            row = t.add_row().cells
            row[0].text = a
            row[1].text = b
        d.add_paragraph()
        d.add_paragraph("The pilot's residual sat inside the limit agreed for go-live. Second-pass verification ran on the "
                        "pilot's documents throughout, as the go-live checklist required, and its sessions are in the "
                        "second-pass export.")
        d.add_paragraph("Go-live is shift-day 2 November 2026 on the day queue at the volumes in Hollings & Pryce's forecast.")
    _docx(os.path.join(target, pack.FILES["pilot"]), build, W.PEOPLE["quality"], "2026-09-30T08:10:00Z", "2026-10-06T11:25:00Z")


# ----------------------------------------------------------------------------------------------- labour note
def labour_note(target):
    def build(d):
        d.add_heading("Second-pass verification: labour planning", level=1)
        d.add_paragraph(f"{W.PEOPLE['mis']}, MIS and workforce planning. Revised 19 October 2026.")
        d.add_paragraph("Second-pass verification re-verifies every key field of every document in a stream that the council "
                        "puts on second pass for the month. We plan the hours a stream would take in a month as its documents "
                        "for the month times the minutes per document for its form family.")
        d.add_paragraph("Documents for the month come from the operating plan's daily key fields, divided by the key fields "
                        "per document of the form version in force on each shift-day (form specifications).")
        d.add_paragraph("Minutes per document for a form family are the productive minutes logged in the latest month's "
                        "second-pass session export, divided by the documents worked in it, across every stream of that "
                        "family. Typed forms take the Hollings & Pryce pilot's sessions in the same export. Productive minutes "
                        "come from the workflow timer and exclude breaks, huddles and system downtime.")
        d.add_paragraph("Staffing is then set from the hours at 6.5 productive hours a person-shift, outside this note.")
    _docx(os.path.join(target, pack.FILES["labour"]), build, W.PEOPLE["mis"], "2025-05-12T09:00:00Z", "2026-10-19T07:42:00Z")


# ----------------------------------------------------------------------------------------------- notes
def notes(target, counts):
    F = pack.FILES
    txt = f"""# Capture MIS extract notes

Folder prepared by MIS for the November 2026 second-pass planning cycle. Exports were taken on 26 and 27 October 2026.
Times in the capture platform, the QA tool and the second-pass workflow are IST (UTC+05:30) with no zone marker.

## {F['spine']}

Capture platform, first-pass verification log, shift-days 1 July to 30 September 2026. One row per screen: a document
opened on a verifier's screen. {counts['spine']:,} rows.

| Column | Meaning |
|---|---|
| screen_id | platform screen reference |
| document_id | capture number of the document |
| stream_code | stream (see stream_register.csv) |
| form_version | form version the document was captured on |
| badge_no | badge of the verifier on the screen |
| opened_at, closed_at | screen opened and closed, IST |
| outcome | SUBMITTED, or TIMED_OUT when the screen sat idle for 15 minutes and the platform closed it |
| key_fields | key fields on the document |
| fields_keyed_over | key fields the verifier changed on the screen |

A timed-out screen submits nothing and the document goes back to the queue; the later submitted screen is the
verification of record. Badges are reused after a verifier leaves: resolve a badge to an employee through the badge
allocation sheet of workforce_register.xlsx for the date of the screen.

## {F['edits']}

One row per key field a verifier keyed over on a submitted screen. {counts['edits']:,} rows.

## {F['audit']}

QA tool, blind re-key audit of first-pass output, shift-days 1 July to 30 September 2026, closed with every audited
document adjudicated. One row per key field of an audited document. {counts['audit']:,} rows.

| result_code | Meaning |
|---|---|
| M | OCR value matched the image and the value after first pass matched it |
| C | OCR value differed from the image and first pass corrected it |
| R | OCR value differed from the image and the value after first pass still differs |
| V | OCR value matched the image and first pass changed it to a value that differs |

rekey_rounds is 2 when the two blind keyers agreed and 3 when a third keyer adjudicated.

## Other files

- workforce_register.xlsx: employees, badge allocation with validity dates, and the Q3 queue rota (HRMS export).
- stream_register.csv: streams, form families, queues with effective dates, and the audit sample share.
- november_operating_plan.xlsx: the plan of record for November (routing, daily key fields by stream, roster), with the
  October second-pass list and budget exchange rates.
- {F['forms']}: form versions with effective shift-days, key fields per document and the key field list.
- {F['sessions']}: second-pass workflow export for September 2026. One row per document worked in a second-pass
  session; productive_min is the workflow timer's productive minutes. Night half-shifts N-A and N-B hand over at
  01:00 IST, day half-shifts D-A and D-B at 12:30 IST.
- {F['manifests']}: delivery transmissions to clients from 25 June to 3 October 2026, from the SFTP gateway log.
- {F['qcp']}: the controlled procedure for first-pass quality control and second-pass designation.
- {F['schedules']} and {F['rates']}: extracts of the client contracts (limits, credits, client audit measurement, prices,
  bands, indexation). {F['billing']}: Finance's account register as at the October invoice run.
- {F['pilot']} and {F['labour']}: Quality's pilot report and the MIS labour planning note.
- Client forecasts ({F['fc_kba']}, {F['fc_us']}, {F['fc_au']}, {F['fc_uk']}, {F['fc_hpy']}) and client audit returns
  ({F['ca_kba']}, {F['ca_us']}, {F['ca_au']}, {F['ca_uk']}) are filed as the clients sent them (Client Services inbox).
- {F['ocr']}: OCR engine's confidence summary by stream, field and month.
- {F['keys']}: verifier keystroke telemetry by badge and login date, from the desktop agent.

## Provenance

All exports are internal records of Tamralipta Data Services or files its clients sent under contract, extracted for
operational planning. Client names and identifiers are as held in our systems; no claimant data is included.
"""
    with open(os.path.join(target, F["notes"]), "w") as fh:
        fh.write(txt)
