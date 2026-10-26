"""task157 documents: the 2027 guarantee's driver terms, finance's funding email, Payments Operations' guarantee
payout notes, Driver Onboarding's pipeline counting notes, the supply team's November KPI report (computed from the
shipped extract), the data notes for the pulled files and the pull log. Their text is kept here as data so checks.py
can quote and execute it."""
from __future__ import annotations

import datetime as dt
import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2421")
GREY = colors.HexColor("#5d6763")
LARCH = colors.HexColor("#2f5d3a")
RULE = colors.HexColor("#a9b4ad")
HEAD = colors.HexColor("#e4ebe5")

F_TERMS = "winter_guarantee_terms_2027.pdf"
F_EMAIL = "guarantee_account_funding_2026-12-30.eml"
F_PAYNOTES = "winter_guarantee_payout_notes.docx"
F_ONBNOTES = "onboarding_pipeline_counts.docx"
F_KPI = "driver_supply_kpis_2026-11.pdf"
F_NOTES = "supply_pull_data_notes.md"
F_LOG = "supply_pull_2027-01-03.log"


def styles(font, bold, accent, size=10.2):
    return dict(
        body=ParagraphStyle("b" + font + str(size), fontName=font, fontSize=size, leading=size * 1.36, textColor=INK,
                            spaceAfter=6),
        h1=ParagraphStyle("h1" + font + str(size), fontName=bold, fontSize=15.0, leading=19.0, textColor=accent,
                          spaceAfter=3),
        sub=ParagraphStyle("s" + font + str(size), fontName=font, fontSize=8.9, leading=11.8, textColor=GREY,
                           spaceAfter=10),
        h2=ParagraphStyle("h2" + font + str(size), fontName=bold, fontSize=10.8, leading=14.0, textColor=accent,
                          spaceBefore=8, spaceAfter=3),
        cell=ParagraphStyle("c" + font + str(size), fontName=font, fontSize=8.6, leading=10.6, textColor=INK),
        cellr=ParagraphStyle("cr" + font + str(size), fontName=font, fontSize=8.6, leading=10.6, textColor=INK,
                             alignment=2),
        cellb=ParagraphStyle("cb" + font + str(size), fontName=bold, fontSize=8.6, leading=10.6, textColor=INK),
        small=ParagraphStyle("sm" + font + str(size), fontName=font, fontSize=8.2, leading=10.6, textColor=GREY,
                             spaceAfter=4))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
                             topMargin=0.85 * inch, bottomMargin=0.8 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _footer(left, font="LibSans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(1.0 * inch, 0.5 * inch, left)
        canvas.drawRightString(letter[0] - 1.0 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ---------------------------------------------------------------------------------------------------- the terms
TERMS = [
    ("What it pays", [
        "Larch pays $350 to every eligible driver who completes 40 trips between 00:00 on Monday 4 January 2027 and "
        "23:59 on Sunday 31 January 2027, Central time. The guarantee is paid on top of trip earnings, tips and any "
        "other promotion.",
    ]),
    ("Who is eligible", [
        "The guarantee is open to every driver whose Larch account is approved by 23:59 on Sunday 3 January 2027 and "
        "is in good standing, including drivers returning to Larch after time away and approved drivers who take "
        "their first trip during the guarantee. There is nothing to opt into.",
        "Accounts approved from Monday 4 January take part in the next guarantee.",
    ]),
    ("What counts as a trip", [
        "A completed trip is a trip the rider completed and paid for. Trips cancelled by the driver or by the rider do "
        "not count. Trips later refunded to the rider as fraudulent are taken off the count, and a guarantee paid on "
        "them is recovered from the driver's earnings.",
        "Each driver can be paid one guarantee. A driver who drives on more than one account is paid once, and a second "
        "payment is recovered.",
    ]),
    ("Payment", [
        "Trips are counted at 23:59 on Sunday 7 February 2027 and the guarantee is paid on Friday 12 February 2027 to "
        "the payout method on file. A trip credited to the account after the count, such as a disputed trip resolved "
        "in the driver's favour, is added in a later payout run, and a driver it takes to 40 trips is paid then.",
    ]),
    ("Earlier guarantees", [
        "The guarantee has run on these terms each January since 2025: $350 at 40 completed trips in the four weeks "
        "from the first Monday of the year, for accounts approved by the Sunday before.",
    ]),
    ("Questions", [
        "Ask Driver Support in the app (Account, then Help). Larch can end or change a promotion that is being misused; "
        "these terms are governed by the laws of Minnesota.",
    ]),
]


def write_terms(path):
    st = styles("LibSans", "LibSans-Bold", LARCH, 10.2)
    s = [Paragraph("Winter Guarantee 2027", st["h1"]),
         Paragraph("Larch Rides driver terms. Published 14 December 2026 by Driver Supply.", st["sub"])]
    for head, paras in TERMS:
        s.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
    doc = _doc(path, "Winter Guarantee 2027: driver terms", "Driver Supply")
    doc.build(s, onFirstPage=_footer("Larch Rides  |  Winter Guarantee 2027 terms"),
              onLaterPages=_footer("Larch Rides  |  Winter Guarantee 2027 terms"))


# ---------------------------------------------------------------------------------------------------- the email
EMAIL_BODY = [
    "Gary,",
    "Treasury funds the winter guarantee account once, at midnight on Monday 4 January when the guarantee goes live "
    "in the app, and we won't top it up during the window. What I need from you is the expected total the guarantee "
    "will pay for 4 to 31 January: $350 for every eligible driver we expect to complete 40 trips, including the drivers "
    "who aren't driving right now, returning and new, since the terms pay them the same way. Please don't pad it; if "
    "the main run comes in over, we cover the difference in February.",
    "Treasury moves money in $50,000 steps, so round it to the nearest $50,000, and send the number of drivers you "
    "expect to qualify with it.",
    # Its own paragraph: wrapped inside the one above, the phrase broke across a line and the sentence that
    # settles the qualification basis stopped being findable in the raw file. The second clause restates the
    # terms' basis, which is WHAT and not HOW, so it pins the convention without naming the decisive step.
    "Returned payouts and recoveries come back to the account afterwards, so leave them out. Count every driver "
    "who completes the 40 trips, whatever happened to the payment afterwards.",
    "Any time Sunday is fine.",
    "Kathy",
]


def email_text():
    hdr = [
        "Return-Path: <ksherman@larchrides.com>",
        "Message-ID: <CAH2k7Wd8sP3qL0mVx4nR9tY6fBz1eJc@mail.larchrides.com>",
        "Date: Wed, 30 Dec 2026 16:12:37 -0600",
        "From: Kathy Sherman <ksherman@larchrides.com>",
        "To: Gary Mathews <gmathews@larchrides.com>",
        "Cc: Melvin Harrell <mharrell@larchrides.com>",
        "Subject: Guarantee account for January",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=\"UTF-8\"",
        "Content-Transfer-Encoding: 7bit",
    ]
    body = []
    for p in EMAIL_BODY:
        body += _wrap(p, 76) + [""]
    sig = ["-- ", "Kathy Sherman", "Finance Director, Larch Rides", "612 555 0148"]
    return "\r\n".join(hdr + [""] + body + sig) + "\r\n"


def _wrap(p, width):
    words, lines, cur = p.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------------------------------- payout notes
PAYNOTES = [
    ("How a guarantee is paid", [
        "The main run goes out on the second Friday after the window closes. It pays $350 to every account the payments "
        "system counts at 40 completed trips at 23:59 on the Sunday after the window; only accounts approved by the "
        "Sunday before the window take part.",
        "Trips credited after the count, most of them disputed trips resolved in the driver's favour, are picked up "
        "by the first adjustment run in March, and an account they take to 40 is paid there.",
        "When trips in the window are later refunded to the rider as fraudulent and the account falls below 40, its "
        "payment is recovered from the driver's next earnings payouts. When fraud review finds one driver on two "
        "accounts, the second account is merged into the first and its payment is recovered. Recoveries go into the "
        "next adjustment run as negative lines naming the payout they reverse; one found late can land in a run of "
        "the next year's guarantee.",
        "The bank returns a payout it cannot credit (a closed account, an account it cannot find, a wrong account "
        "number), and the driver is asked in the app to update their payout details.",
    ]),
    ("What a guarantee cost", [
        "A guarantee's cost is what its runs paid, less payouts the bank returned that were never paid out again and "
        "less what was recovered; returns and recoveries are booked to the guarantee of the payout they reverse, "
        "whatever run they land in.",
        "The drivers a guarantee paid are the people who kept a payment: one per person however many accounts, none "
        "for a payout returned and never paid out again or recovered.",
    ]),
    ("Exports", [
        "The 2025 main run came out of the old payout report, which gives amounts in cents. From the 2026 guarantee "
        "the runs export from the payments system. The bank's returns report covers every payout from the account, "
        "weekly earnings included; guarantee payouts carry the entry description GUARANTEE.",
    ]),
]


def _page_field(par):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for kind, text in (("begin", None), (None, " PAGE "), ("separate", None), (None, "1"), ("end", None)):
        r = par.add_run()
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            r._r.append(fc)
        elif text.strip() == "PAGE":
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            r._r.append(it)
        else:
            r.text = text


def _word(path, title, byline, sections, footer):
    import docx
    from docx.shared import Cm, Pt, RGBColor
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    sec.left_margin = sec.right_margin = Cm(2.4)
    sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.0)
    fp = sec.footer.paragraphs[0]
    fp.text = footer + ", page "
    _page_field(fp)
    for r in fp.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0x5D, 0x67, 0x63)
    green = RGBColor(0x2F, 0x5D, 0x3A)
    p = doc.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = green
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(byline)
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x5D, 0x67, 0x63)
    for head, paras in sections:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(head)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = green
        for t in paras:
            doc.add_paragraph(t)
    doc.save(path)


def write_paynotes(path):
    _word(path, "Winter guarantee payouts", "Payments Operations. Melvin Harrell, 20 March 2026. For Finance and "
          "Driver Supply.", PAYNOTES, "Larch Rides Payments Operations, winter guarantee payouts")


ONBNOTES = [
    ("The pipeline", [
        "Applications come in through the onboarding app, which went live on 2 June 2025; applications made before "
        "then were handled by email and are not in it. Submitting an application places the background check order "
        "with our screening vendor, and the check runs while we review the documents.",
        "When a document is missing or unreadable we send the application back, and the applicant fixes it in the app "
        "and resubmits.",
        "An approval opens the driver's account. An approval lapses 90 days after it is given if the driver has not "
        "taken a trip, and the applicant reapplies.",
    ]),
    ("Monthly counts", [
        "We count people, not applications. Someone who applies again after a rejection has a second application but "
        "stays one candidate with the screening vendor.",
        "A person is counted once, in the month (Central time) of their first submission; approved means approved on "
        "any of their applications; a first trip is any completed trip on their account by the date of the count.",
    ]),
]


def write_onbnotes(path):
    _word(path, "Onboarding pipeline counts", "Driver Onboarding, 5 August 2026.", ONBNOTES,
          "Larch Rides Driver Onboarding, pipeline counts")


# ---------------------------------------------------------------------------------------------------- KPI report
KPI_QUESTION = ("Driver supply on the dispatch platform each month, January 2025 to November 2026. A driver is active "
                "in a month with a completed trip in it; a new driver's first completed trip on Larch is in the month "
                "(old-platform history through the migration crosswalk). Counts are accounts. Online hours are time "
                "online in the driver app.")


def kpi_rows(target):
    """Computed from the shipped extract, the legacy export and the crosswalk."""
    import calc as C
    D = C.load(target)
    online = {}
    for r in C.rd(target, R.F_ACTIVITY):
        m = (int(r["activity_month"][:4]), int(r["activity_month"][5:7]))
        online[m] = online.get(m, 0) + int(r["online_minutes"])
    rows = []
    for m in K.months(dt.date(2025, 1, 1), dt.date(2026, 11, 1)):
        j = D.mi[m]
        act = int(D.A[:, j].sum())
        new = int((D.first_m == j).sum())
        trips = int(D.T[:, j].sum())
        hrs = online[m] / 60.0
        rows.append(dict(month=m, active=act, new=new, trips=trips, hours=hrs, per=trips / act))
    return rows


def write_kpi(path, target):
    rows = kpi_rows(target)
    st = styles("Carlito", "Carlito-Bold", LARCH, 10.4)
    s = [Paragraph("Driver supply KPIs: November 2026", st["h1"]),
         Paragraph("Supply Analytics. Jesse Velasquez. Published 11 December 2026.", st["sub"]),
         Paragraph(esc(KPI_QUESTION), st["body"]), Spacer(1, 4)]
    head = ["Month", "Active drivers", "New drivers", "Completed trips", "Online hours", "Trips per active driver"]
    data = [[Paragraph(esc(h), st["cellb"]) for h in head]]
    for r in rows:
        y, m = r["month"]
        data.append([Paragraph(esc("%s %d" % (K.MON3[m], y)), st["cell"]),
                     Paragraph("{:,}".format(r["active"]), st["cellr"]),
                     Paragraph("{:,}".format(r["new"]), st["cellr"]),
                     Paragraph("{:,}".format(r["trips"]), st["cellr"]),
                     Paragraph("{:,}".format(int(K.round_half_up(r["hours"]))), st["cellr"]),
                     Paragraph("%.1f" % K.round_half_up(r["per"], 1), st["cellr"])])
    t = Table(data, colWidths=[w * inch for w in (0.95, 1.05, 0.95, 1.15, 1.05, 1.35)], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("TOPPADDING", (0, 0), (-1, -1), 2.4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4)]))
    s.append(t)
    s.append(Spacer(1, 8))
    s.append(Paragraph(esc("Source: dispatch warehouse, driver activity by month, refreshed 7 December 2026. Months "
                           "are calendar months, Central time."), st["small"]))
    doc = _doc(path, "Driver supply KPIs: November 2026", K.PEOPLE["analytics"])
    doc.build(s, onFirstPage=_footer("Larch Rides Supply Analytics  |  Monthly supply KPIs", "Carlito"),
              onLaterPages=_footer("Larch Rides Supply Analytics  |  Monthly supply KPIs", "Carlito"))
    return rows


# ---------------------------------------------------------------------------------------------------- data notes
def data_notes():
    L = []
    a = L.append
    a("# Supply pull, 3 January 2027: data notes")
    a("")
    a("Supply Analytics (Jesse Velasquez). Field notes for the files pulled on Sunday 3 January 2027; the pull log is "
      "%s." % F_LOG)
    a("")
    a("## Dispatch")
    a("")
    a("**%s**. The old dispatch platform's monthly driver export, one row per legacy driver number and month with "
      "completed trips or online time. Months are calendar months, Central time. ONLINE_HRS is online time in hours, "
      "to one decimal. The old platform's last day was Sunday 14 July 2024, so July 2024 holds 1 to 14 July." % R.F_LEGACY)
    a("")
    a("**%s**. The dispatch warehouse's monthly driver activity, one row per driver_id and month with completed trips "
      "or online time, from Monday 15 July 2024; July 2024 holds 15 to 31 July. trips_completed counts trips the "
      "rider completed; trips_cancelled_by_driver are not in it; online_minutes is time online in the driver app. "
      "Months are calendar months, Central time. January 2027 holds 1 to 3 January, to the extract run." % R.F_ACTIVITY)
    a("")
    a("**%s**. Every legacy driver number and the driver_id it became on 15 July 2024. A driver registered twice on "
      "the old platform has both numbers mapped to one driver_id." % R.F_CROSSWALK)
    a("")
    a("**%s**. One row per account as at the extract run." % R.F_ACCOUNTS)
    a("")
    a("| Field | Values |")
    a("|---|---|")
    a("| account_opened | the day the account was approved, Central time |")
    a("| signup_channel | app; referral; campaign_winter26 (the winter 2026 recruitment campaign, sign-ups from 12 "
      "January 2026); rental_partner (drivers of the 2025 rental programme) |")
    a("| vehicle | own, lease, rental |")
    a("| account_status | active (a completed trip in the last 30 days); new (approved, no trip yet); inactive; "
      "deactivated; merged (a driver's second account, merged into merged_into on closed_on) |")
    a("| last_trip_on | the day of the account's latest completed trip |")
    a("| closed_on | the day the account was deactivated or merged |")
    a("")
    a("## Payments")
    a("")
    a("**%s**. The 2025 guarantee's main run of 14 February 2025, from the old payout report." % R.F_RUN25)
    a("")
    a("**%s**. The 2026 guarantee's main run of 13 February 2026." % R.F_RUN26)
    a("")
    a("**%s**. The guarantee's adjustment runs, 2025 and 2026: a late_credit line pays the payout in payout_id; a "
      "fraud_recovery or duplicate_account line recovers the payout in reverses_payout_id. program_code is the run's "
      "program." % R.F_ADJ)
    a("")
    a("**%s**. Each guarantee payout's events in the payments system, UTC." % R.F_EVENTS)
    a("")
    a("**%s**. The bank's ACH return report for the payout account, 2025 and 2026; individual_id carries the payout "
      "id." % R.F_RETURNS)
    a("")
    a("## Onboarding")
    a("")
    a("**%s**. The onboarding app's applications export, one row per application, times UTC. status: in_review, "
      "approved, approval_lapsed (approved, the approval lapsed 90 days after it was given without a trip), rejected, "
      "withdrawn, expired. driver_id is the account an approval opened; first_trip_at_utc is that account's first "
      "completed trip." % R.F_APPS)
    a("")
    a("**%s**. The screening vendor's order export for Larch, one row per order, times UTC. candidate_id is the "
      "vendor's person; client_reference is the application id." % R.F_ORDERS)
    a("")
    a("## Also in the pull")
    a("")
    a("%s (the November KPI report), %s and %s (the payments and onboarding teams' notes), %s (the 2027 terms), %s "
      "(finance's email of 30 December), %s (marketplace planning's Q1 plan, issued 4 December), %s (2026 referral "
      "bonuses)." % (F_KPI, F_PAYNOTES, F_ONBNOTES, F_TERMS, F_EMAIL, R.F_DEMAND, R.F_REFERRAL))
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------------------------------- pull log
def pull_log(n_rows, sizes):
    t = dt.datetime(2027, 1, 3, 21, 40, 2)
    lines = []

    def at(sec):
        return (t + dt.timedelta(seconds=sec)).strftime("%Y-%m-%d %H:%M:%S") + " CST"
    lines.append("%s  pull supply_guarantee_2027 start user=jvelasquez host=sa-ws-07" % at(0))
    lines.append("%s  dest \\\\larch-fs01\\supply\\pulls\\2027-01-03" % at(1))
    steps = [
        (4, "dw.dispatch_legacy_driver_month", R.F_LEGACY),
        (61, "dw.driver_activity_monthly", R.F_ACTIVITY),
        (96, "dw.dispatch_migration_crosswalk", R.F_CROSSWALK),
        (104, "dw.driver_account", R.F_ACCOUNTS),
        (141, "payments.report_archive WG25-MAIN-0214", R.F_RUN25),
        (149, "payments.batch_export WG26-MAIN-0213", R.F_RUN26),
        (156, "payments.adjustment_lines program in (WG2025, WG2026)", R.F_ADJ),
        (171, "payments.payout_events program in (WG2025, WG2026)", R.F_EVENTS),
        (203, "bank portal ACH return report 2025-01-01..2026-12-31", R.F_RETURNS),
        (229, "onboarding.applications_export 2025-06-02..2027-01-03", R.F_APPS),
        (262, "screening vendor portal order export 2025-06..2027-01", R.F_ORDERS),
        (287, "referrals.bonus_ledger 2026", R.F_REFERRAL),
    ]
    for sec, src, f in steps:
        rows = n_rows.get(f)
        lines.append("%s  %-55s rows=%s bytes=%d -> %s" % (at(sec), src, "{:,}".format(rows) if rows is not None
                                                             else "-", sizes[f], f))
    lines.append("%s  copied %s (marketplace planning share, issued 2026-12-04) bytes=%d" % (at(301), R.F_DEMAND,
                                                                                        sizes[R.F_DEMAND]))
    for k, f in enumerate((F_KPI, F_TERMS, F_EMAIL, F_PAYNOTES, F_ONBNOTES)):
        lines.append("%s  copied %s bytes=%d" % (at(306 + 4 * k), f, sizes[f]))
    lines.append("%s  copied %s bytes=%d" % (at(331), F_NOTES, sizes[F_NOTES]))
    lines.append("%s  pull supply_guarantee_2027 done files=%d" % (at(333), len(steps) + 7))
    return "\n".join(lines) + "\n"


def write_all(out, n_rows):
    p = lambda f: os.path.join(out, f)
    write_terms(p(F_TERMS))
    with open(p(F_EMAIL), "w", encoding="utf-8", newline="") as fh:
        fh.write(email_text())
    write_paynotes(p(F_PAYNOTES))
    write_onbnotes(p(F_ONBNOTES))
    write_kpi(p(F_KPI), out)
    with open(p(F_NOTES), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(data_notes())
    P = K.PEOPLE
    PP.normalize_pdf(p(F_TERMS), b"D:20261214101800-06'00'", b"D:20261214101800-06'00'")
    PP.normalize_pdf(p(F_KPI), b"D:20261211083400-06'00'", b"D:20261211083400-06'00'")
    PP.normalize_docx(p(F_PAYNOTES), P["payments"], P["payments"], "2026-03-18T15:06:00Z", "2026-03-20T19:41:00Z",
                      revision=7, total_time=96, seed="task157/payout-notes", title="Winter guarantee payouts",
                      company=K.OPERATOR)
    PP.normalize_docx(p(F_ONBNOTES), "Driver Onboarding", "Driver Onboarding", "2026-08-04T20:15:00Z",
                      "2026-08-05T14:52:00Z", revision=4, total_time=41, seed="task157/onboarding-counts",
                      title="Onboarding pipeline counts", company=K.OPERATOR)
    sizes = {f: os.path.getsize(p(f)) for f in os.listdir(out)}
    with open(p(F_LOG), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(pull_log(n_rows, sizes))
