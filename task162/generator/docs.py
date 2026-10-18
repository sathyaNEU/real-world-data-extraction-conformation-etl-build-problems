"""task162 documents: the staffing-plan thread, the tracker cutover runbook, the triage team's working agreement for
the new tracker, the release calendar, the old export's field notes and the pull's manifest. Their text is kept here as
data so checks.py and verify.py can quote and execute it."""
from __future__ import annotations

import datetime as dt
import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import parallel as PR       # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2328")
GREY = colors.HexColor("#5b636b")
ACCENT = colors.HexColor("#2b4f73")
RULE = colors.HexColor("#b4bcc4")
HEAD = colors.HexColor("#e6ebf0")

F_THREAD = "staffing_plan_q1_2027.eml"
F_RUNBOOK = "tracker_cutover_runbook.docx"
F_AGREEMENT = "triage_working_agreement.docx"
F_CALENDAR = "release_calendar_2025_2027.pdf"
F_MANIFEST = "export_manifest.csv"
DOMAIN = "usvasoftware.fi"


def addr(name):
    a = name.lower().replace("ä", "a").replace("ö", "o").replace("å", "a").split()
    return "%s.%s@%s" % (a[0], a[-1], DOMAIN)


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ---------------------------------------------------------------------------------------------------- the thread
THREAD_FIRST = [
    "Hi all,",
    "The engineering staffing review meets on Monday 21 December to approve first-quarter headcount team by team. "
    "Please put your team's number in the planning sheet by Friday 18 December.",
    "Ulla, triage is sized the way we agreed in the spring: the quarter is staffed for its busiest week at the "
    "standard of 120 triage items per triager-week, so the headcount is the busiest week's expected triage items "
    "divided by 120 and rounded up to a whole triager. For this plan the quarter is the 13 weeks from Monday "
    "4 January to Sunday 4 April 2027, weeks Monday to Sunday, Helsinki time.",
    "Thanks,",
    "Juhani",
]
THREAD_REPLY = [
    "Juhani,",
    "Will do. From the cutover we count triage items the way Ritva's cutover runbook sets out, so the number won't "
    "compare with the old dashboard's new defects. You'll have it tomorrow.",
    "Ulla",
]
THREAD_SENTENCES = sentences(THREAD_FIRST + THREAD_REPLY)


def _wrap(p, width=76):
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


def thread_text():
    P = K.PEOPLE
    import quopri
    body = []
    for p in THREAD_REPLY:
        body += _wrap(p) + [""]
    body += ["-- ", "Ulla Kauppinen", "Triage team lead, Usva Software Oy", ""]
    body.append("On Mon, 7 Dec 2026 at 9.14, %s <%s> wrote:" % (P["director"], addr(P["director"])))
    for p in THREAD_FIRST:
        body += ["> " + ln for ln in _wrap(p, 74)] + [">"]
    text = "\r\n".join(body[:-1]) + "\r\n"
    qp = quopri.encodestring(text.encode("utf-8")).decode("ascii")
    qp = qp.replace("\r\n", "\n").replace("\n", "\r\n")
    hdr = [
        "Return-Path: <%s>" % addr(P["lead"]),
        "Message-ID: <CAF8u2Rk1qZt7wYd3pHn0vLs5mXe9cGb4Q@mail.%s>" % DOMAIN,
        "In-Reply-To: <CAD4n6Vh2sPq8kLz5tWr1yNc7bJm3eFa0X@mail.%s>" % DOMAIN,
        "References: <CAD4n6Vh2sPq8kLz5tWr1yNc7bJm3eFa0X@mail.%s>" % DOMAIN,
        "Date: Thu, 17 Dec 2026 16:12:48 +0200",
        "From: %s <%s>" % (P["lead"], addr(P["lead"])),
        "To: %s <%s>" % (P["director"], addr(P["director"])),
        "Cc: %s <%s>" % (P["migration"], addr(P["migration"])),
        "Subject: Re: Q1 headcount for the staffing review",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=\"UTF-8\"",
        "Content-Transfer-Encoding: quoted-printable",
    ]
    return "\r\n".join(hdr) + "\r\n\r\n" + qp


# ---------------------------------------------------------------------------------------------------- the runbook
RUNBOOK = [
    ("Dates", [
        "The old tracker stops taking reports at 23:59 on Sunday 3 January 2027 and is read-only from then. The new "
        "tracker is the system of record from 00:00 on Monday 4 January 2027, Helsinki time, and the report form posts "
        "to it from then.",
    ]),
    ("What is migrated", [
        "Open reports migrate in the cutover night with their state, components, priority and links, and keep their old "
        "bug number in Legacy bug. Migrated reports keep their state and are not new triage items. Closed reports stay "
        "on the old tracker, read-only.",
        "The trial migration of 23 October loaded the open reports of that day as BRW-1 to BRW-23460, so that the "
        "parallel run's duplicates had reports to link to. The cutover load replaces them.",
    ]),
    ("Intake from the cutover", [
        "The report form posts to the Browser intake project (BRW). Every report filed through the report form is a "
        "triage item, duplicates included: a duplicate is triaged like any other report and closed with a duplicates "
        "link to the report it repeats. A report is counted in the week it is filed.",
        "Reports in the security group go to the security team's queue and are not triage items. Spam caught by the "
        "form's filter never reaches the queue.",
        "A report the team moves to another team's project during triage stays a triage item. The form takes reports "
        "from release, beta and nightly builds, and each is a triage item whatever version the reporter runs.",
        "Reports filed with the Report a site issue tool go to the web-compatibility team's project (WEBC), on the new "
        "tracker since the April pilot, and are not triage items.",
    ]),
    ("The parallel run, 2 to 29 November 2026", [
        "Reporters kept filing on the old tracker. From 00:00 on Monday 2 November the bridge (service account "
        "tracker-bridge) copied the reports into the new tracker, form reports to BRW and site reports to WEBC, each "
        "with its old bug number. The triage team worked the run's reports on the new tracker.",
        "On Monday 30 November the bridge was switched off, and the old tracker's copies of the run's reports were "
        "closed RESOLVED MOVED and put in the Archive product. The run was exported from the new tracker on "
        "4 December.",
    ]),
    ("Cutover night, 3 to 4 January", [
        "22:00 Ritva Grönroos: last check of the component and version mapping against the old tracker.",
        "23:59 Old tracker read-only; the bridge's last copy.",
        "00:15 Load of the open reports; counts checked product by product against the old tracker.",
        "02:30 The report form switched to the new tracker; test report filed and closed.",
        "07:30 Triage team starts on the new tracker.",
    ]),
]
RUNBOOK_SENTENCES = sentences([p for _, ps in RUNBOOK for p in ps])

AGREEMENT = [
    ("Duty", [
        "Triage runs on weekdays from 08:00 to 16:30 with the people on the rota, and on Saturdays from 10:00 to 14:00 "
        "with one person on cover. Sundays have no cover.",
    ]),
    ("The queue", [
        "New reports come into Browser intake (BRW) in New. Take the oldest first. A report that needs another look can "
        "wait, but try not to leave it past the next working day.",
        "Set Triaged with a priority, P1 to P4, and the report's component. A report that spans two areas gets both "
        "components.",
        "Close a duplicate with a duplicates link to the report it repeats, and other reports with a resolution. Move "
        "site problems to Web compatibility (WEBC). Reports restricted to the security team are theirs.",
    ]),
    ("What we measure", [
        "A triage action is a change by one of the rota's triagers to a report's status, resolution, component or "
        "priority, or a move of the report to another team's project. The target is a triage action on every report "
        "within 24 hours of its filing.",
        "A report is closed when it is in Resolved or Closed, or sits in another team's project.",
        "Weeks run Monday to Sunday, Helsinki time, and a report belongs to the week it is filed in. The parallel run's "
        "reports are those filed from 00:00 on Monday 2 November to 23:59 on Sunday 29 November.",
        "Component groups are in the component register.",
    ]),
]
AGREEMENT_SENTENCES = sentences([p for _, ps in AGREEMENT for p in ps])


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


def _word(path, title, byline, sections, footer, steps_section=None):
    import docx
    from docx.shared import Cm, Pt, RGBColor
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    fp = sec.footer.paragraphs[0]
    fp.text = footer + ", page "
    _page_field(fp)
    for r in fp.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0x5B, 0x63, 0x6B)
    blue = RGBColor(0x2B, 0x4F, 0x73)
    p = doc.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = blue
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(byline)
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x5B, 0x63, 0x6B)
    for head, paras in sections:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(head)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = blue
        if head == steps_section:
            t = doc.add_table(rows=0, cols=2)
            t.style = "Table Grid"
            for s in paras:
                when, what = s.split(" ", 1)
                row = t.add_row().cells
                row[0].text = when
                row[1].text = what
                row[0].width = Cm(1.8)
                row[1].width = Cm(14.6)
            continue
        for tx in paras:
            doc.add_paragraph(tx)
    doc.save(path)


def write_runbook(path):
    _word(path, "New tracker cutover runbook", "Tracker migration. Ritva Grönroos, version 1.5, 7 December 2026.",
          RUNBOOK, "Usva Software Oy, tracker migration, cutover runbook", steps_section="Cutover night, 3 to 4 January")


def write_agreement(path):
    _word(path, "Triage on the new tracker", "Working agreement of the triage team, from the parallel run on. "
          "Ulla Kauppinen, 28 October 2026.", AGREEMENT, "Usva Software Oy, triage team, working agreement")


# ---------------------------------------------------------------------------------------------------- calendar
def calendar_rows():
    rows = []
    for i, (m, d) in enumerate(K.RELEASES):
        beta = K.RELEASES[i - 1][1] if i > 0 else dt.date(2025, 6, 17)
        dots = ", ".join("%d.0.%d %s" % (m, n, K.fi_date(dd)) for n, dd in K.DOTS.get(m, []))
        status = "planned" if d > K.AS_OF else "released"
        rows.append((m, beta, d, dots, status))
    return rows


def write_calendar(path):
    st = dict(
        h1=ParagraphStyle("h1", fontName="LibSans-Bold", fontSize=15, leading=19, textColor=ACCENT, spaceAfter=3),
        sub=ParagraphStyle("sub", fontName="LibSans", fontSize=8.8, leading=11.6, textColor=GREY, spaceAfter=10),
        body=ParagraphStyle("b", fontName="LibSans", fontSize=9.6, leading=13, textColor=INK, spaceAfter=6),
        cell=ParagraphStyle("c", fontName="LibSans", fontSize=8.4, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="LibSans-Bold", fontSize=8.4, leading=10.4, textColor=INK),
        small=ParagraphStyle("sm", fontName="LibSans", fontSize=7.9, leading=10.2, textColor=GREY, spaceAfter=4))
    s = [Paragraph("Usva release calendar 2025 to 2027", st["h1"]),
         Paragraph("Release management, Timo Huttunen. Updated 3.12.2026.", st["sub"]),
         Paragraph("Release builds go out on the release channel at 16:00 Helsinki time on the release day. A version "
                   "is on the beta channel from the previous release day until its own release.", st["body"])]
    head = ["Version", "Beta from", "Release", "Point releases", ""]
    data = [[Paragraph(h, st["cellb"]) for h in head]]
    for m, beta, d, dots, status in calendar_rows():
        data.append([Paragraph("%d.0" % m, st["cell"]), Paragraph(K.fi_date(beta), st["cell"]),
                     Paragraph(K.fi_date(d), st["cell"]), Paragraph(dots or "", st["cell"]),
                     Paragraph(status if status == "planned" else "", st["cell"])])
    t = Table(data, colWidths=[1.7 * cm, 2.3 * cm, 2.3 * cm, 7.4 * cm, 1.8 * cm], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    s.append(t)
    s.append(Spacer(1, 8))
    s.append(Paragraph("Dates are d.m.yyyy. Planned dates can move; point releases are planned only for the next "
                       "version.", st["small"]))

    def foot(canvas, doc):
        canvas.saveState()
        canvas.setFont("LibSans", 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(2.0 * cm, 1.2 * cm, "Usva Software Oy  |  Release management  |  Release calendar")
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.8 * cm, title="Usva release calendar 2025 to 2027", author=K.PEOPLE["release"],
                            subject="", creator="", producer="")
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


# ---------------------------------------------------------------------------------------------------- field notes
def field_notes(n_rows):
    L = [
        "Usva bug tracker (old tracker), saved search triage-weekly-export",
        "Run: 2026-12-18 06:40 Europe/Helsinki, %s rows" % "{:,}".format(n_rows),
        "",
        "Search: every report filed through the in-browser report form, opened from 2025-10-01 00:00:00 to",
        "2026-12-17 23:59:59, all products, all statuses. Reports filed with the Report a site issue tool and spam",
        "removed by the form's filter are not in this search.",
        "",
        "bug_id        bug number",
        "opened        when the report was filed (Europe/Helsinki local time)",
        "changeddate   last change (Europe/Helsinki local time)",
        "product       product the report is in now (Engine, Shell, Extensions, DevTools, Install and Update;",
        "              reports moved to the web-compatibility team: Web Compatibility; the parallel run's",
        "              reports, closed MOVED on 2026-11-30: Archive)",
        "component     component the report is in now; untriaged reports keep the component of the form area",
        "              the reporter picked",
        "version       version the reporter ran, from the report form (release builds x.0 and x.0.n, beta",
        "              builds x.0bn, nightly builds x.0a1)",
        "op_sys        reporter's operating system, from the report form",
        "bug_severity  S1 to S4, -- if not set",
        "bug_status    UNCONFIRMED, NEW, ASSIGNED, RESOLVED, VERIFIED",
        "resolution    --- while open; FIXED, INVALID, WONTFIX, DUPLICATE, WORKSFORME, INCOMPLETE, MOVED",
        "dupe_of       for RESOLVED DUPLICATE, the bug it duplicates",
        "groups        core-security if the report is restricted to the security team",
        "keywords      regression, crash",
    ]
    return "\r\n".join(L) + "\r\n"


# ---------------------------------------------------------------------------------------------------- manifest
MANIFEST_COLS = ["file", "source", "covers", "taken", "rows", "notes"]


def manifest_rows(n):
    return [
        {"file": R.F_EXPORT, "source": "old tracker, saved search triage-weekly-export", "covers": "2025-10-01 to 2026-12-17",
         "taken": "2026-12-18 06:40", "rows": n[R.F_EXPORT], "notes": "field notes in %s" % R.F_FIELDS},
        {"file": R.F_FIELDS, "source": "old tracker", "covers": "", "taken": "2026-12-18 06:40", "rows": "", "notes": ""},
        {"file": R.F_DASH, "source": "triage dashboard (old tracker)", "covers": "weeks from 2025-09-29 to 2026-12-07",
         "taken": "2026-12-18 06:40", "rows": n[R.F_DASH], "notes": "refreshed with the weekly export"},
        {"file": R.F_SHARES, "source": "public data portal, release channel version shares (Simo Kinnunen, data team)",
         "covers": "2025-10-01 to 2026-12-17", "taken": "2026-12-18 06:52", "rows": n[R.F_SHARES],
         "notes": "per cent of each platform's active installs on the day"},
        {"file": R.F_INSTALLS, "source": "public data portal, daily active installs (Simo Kinnunen, data team)",
         "covers": "2025-10-01 to 2026-12-17", "taken": "2026-12-18 06:52", "rows": n[R.F_INSTALLS],
         "notes": "release channel, thousands"},
        {"file": R.F_PUBLIC, "source": "usva bug statistics page, monthly", "covers": "2025-10 to 2026-11",
         "taken": "2026-12-18 06:55", "rows": n[R.F_PUBLIC], "notes": "published on the 3rd working day of the month"},
        {"file": R.F_STABILITY, "source": "crash reporter, monthly stability", "covers": "2025-10 to 2026-11",
         "taken": "2026-12-18 06:57", "rows": n[R.F_STABILITY], "notes": ""},
        {"file": F_CALENDAR, "source": "release management", "covers": "versions 31 to 52", "taken": "2026-12-03",
         "rows": "", "notes": ""},
        {"file": R.F_NEWEXPORT, "source": "new tracker, projects BRW and WEBC, issues created from 2026-11-02",
         "covers": "parallel run", "taken": "2026-12-04 10:20", "rows": n[R.F_NEWEXPORT],
         "notes": "REST search with changelog; times UTC"},
        {"file": R.F_ROTA, "source": "triage team", "covers": "2026-11-02 to 2026-12-04", "taken": "2026-11-27",
         "rows": n[R.F_ROTA], "notes": ""},
        {"file": R.F_GROUPS, "source": "triage team", "covers": "", "taken": "2026-10-26", "rows": n[R.F_GROUPS],
         "notes": ""},
        {"file": F_AGREEMENT, "source": "triage team", "covers": "", "taken": "2026-10-28", "rows": "", "notes": ""},
        {"file": F_RUNBOOK, "source": "tracker migration", "covers": "", "taken": "2026-12-07", "rows": "", "notes": ""},
        {"file": F_THREAD, "source": "mail", "covers": "", "taken": "2026-12-17", "rows": "", "notes": ""},
    ]


def write_all(out, n):
    p = lambda f: os.path.join(out, f)
    with open(p(F_THREAD), "w", encoding="utf-8", newline="") as fh:
        fh.write(thread_text())
    write_runbook(p(F_RUNBOOK))
    write_agreement(p(F_AGREEMENT))
    write_calendar(p(F_CALENDAR))
    with open(p(R.F_FIELDS), "w", encoding="utf-8", newline="") as fh:
        fh.write(field_notes(n[R.F_EXPORT]))
    P = K.PEOPLE
    PP.normalize_pdf(p(F_CALENDAR), b"D:20261203141100+02'00'", b"D:20261203141100+02'00'")
    PP.normalize_docx(p(F_RUNBOOK), P["migration"], P["migration"], "2026-10-09T11:20:00Z", "2026-12-07T09:18:00Z",
                      revision=15, total_time=431, seed="task162/runbook", title="New tracker cutover runbook",
                      company=K.VENDOR)
    PP.normalize_docx(p(F_AGREEMENT), P["lead"], P["lead"], "2026-10-27T13:05:00Z", "2026-10-28T08:31:00Z",
                      revision=5, total_time=63, seed="task162/agreement", title="Triage on the new tracker",
                      company=K.VENDOR)
    K.write_csv(p(F_MANIFEST), MANIFEST_COLS, manifest_rows(n))
