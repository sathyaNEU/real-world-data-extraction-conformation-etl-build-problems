"""The pack's documents: section 6 of the draft 2027 intended use plan (the PFAS treatment-design grants and the 2027
priority list), the department's PFAS initial monitoring sampling guide, and the department's notes on the data it
sent the Authority."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import letter                                         # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
for nm, f in (("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"), ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2329"), colors.HexColor("#5c666f"), colors.HexColor("#b4bdc5")

AUTHORITY = "Water Infrastructure Finance Authority"
POINTS = [92, 88, 87, 81, 79, 76, 72, 71, 68, 64, 63, 59, 58, 55, 52, 50, 49, 45, 44, 41]


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.5, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.3, leading=11, textColor=GREY, spaceAfter=9),
        note=ParagraphStyle("n", fontName=font, fontSize=7.8, leading=10, textColor=GREY, spaceBefore=6),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.4, leading=10.8, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.4, leading=10.8, textColor=INK))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=22 * mm,
                             bottomMargin=19 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(left, right, font="Sans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(22 * mm, letter[1] - 12 * mm, left)
        canvas.drawRightString(letter[0] - 22 * mm, letter[1] - 12 * mm, right)
        canvas.drawRightString(letter[0] - 22 * mm, 10.5 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = []
    for i, r in enumerate(rows):
        out = []
        for j, c in enumerate(r):
            st = S["cellb"] if i == 0 else S["cell"]
            if j in right and i > 0:
                st = ParagraphStyle("r", parent=st, alignment=2)
            out.append(Paragraph(str(c), st))
        data.append(out)
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


# ---------------------------------------------------------------------------------------------- the plan
def write_iup(path, listed):
    """listed: the twenty systems in the list's order, each with pws, full name, county and population."""
    S = styles("Serif", colors.HexColor("#123a5e"))
    doc = _doc(path, "2027 Intended Use Plan, Drinking Water State Revolving Fund (draft), section 6", AUTHORITY)
    st = []
    st.append(Paragraph("Drinking Water State Revolving Fund: 2027 Intended Use Plan", S["h1"]))
    st.append(Paragraph("Draft for the %s board of directors, 18 November 2026. Prepared by the %s, Drinking Water "
                        "Program, and the %s. Public comment 1 to 31 October 2026. Section 6 of 9."
                        % (AUTHORITY, K.DEPT, AUTHORITY), S["meta"]))
    st.append(Paragraph("6. PFAS treatment-design grants", S["h2"]))
    st.append(Paragraph("6.1 Set-aside. From the emerging-contaminants capitalization grants for federal fiscal years 2025 "
                        "and 2026, the plan sets aside $36,000,000 for grants that pay for the design of treatment for "
                        "per- and polyfluoroalkyl substances (PFAS) at the wells of community water systems. The grants "
                        "are principal forgiveness; nothing is repaid.", S["body"]))
    st.append(Paragraph("6.2 Applicants. Table 6-1 lists, in priority order, the community water systems that sent the "
                        "department a PFAS design-grant pre-application by 15 May 2026. Priority points are scored under "
                        "Appendix C (health risk, affordability and readiness to proceed).", S["body"]))
    st.append(Paragraph("6.3 Grant amount. A listed system's grant is $2.4 million for each million gallons a day (MGD) "
                        "of rated capacity at its active wells whose own water averaged more than 4.0 ng/L of PFOA or "
                        "more than 4.0 ng/L of PFOS over 2024 and 2025, up to $6 million a system. A well's own water is "
                        "the water the well itself pumps. Rated capacity is the capacity the department's source "
                        "facility inventory records for the well, and the active wells are those the inventory lists as "
                        "active.", S["body"]))
    st.append(Paragraph("6.4 Funding order. The set-aside funds the systems in the order of Table 6-1. When what remains "
                        "of it does not cover the next system's grant, funding stops for 2027; that system and those "
                        "below it carry to the 2028 list.", S["body"]))
    st.append(Paragraph("6.5 Schedule. The board considers the list on 18 November 2026. The Authority offers grant "
                        "agreements by 29 January 2027, and a funded system's design is due within 18 months of its "
                        "agreement.", S["body"]))
    rows = [["Rank", "PWS ID", "System", "County", "Population served", "Priority points"]]
    for i, s in enumerate(listed):
        rows.append([i + 1, s["pws"], s["full"], s["county"], "{:,}".format(s["pop"]), POINTS[i]])
    st.append(Spacer(1, 4))
    st.append(Paragraph("Table 6-1. 2027 PFAS priority list", S["cellb"]))
    st.append(Spacer(1, 2))
    st.append(_table(S, rows, [13, 20, 61, 20, 24, 22], right=(0, 4, 5)))
    st.append(Spacer(1, 6))
    st.append(Paragraph("6.6 Other emerging-contaminants uses in 2027. Sampling assistance for systems serving fewer than "
                        "3,300 people, $1,850,000; source water protection planning, $640,000; program administration, "
                        "$1,612,000.", S["body"]))
    st.append(Paragraph("Population served is as the department's system register records it on 1 September 2026.",
                        S["note"]))
    doc.build(st, onFirstPage=_frame("2027 Intended Use Plan (draft)", AUTHORITY, "Serif"),
              onLaterPages=_frame("2027 Intended Use Plan (draft)", AUTHORITY, "Serif"))


# ---------------------------------------------------------------------------------------------- the guide
def write_guide(path):
    S = styles("Sans", colors.HexColor("#245b3c"))
    doc = _doc(path, "PFAS Initial Monitoring, Community Water Systems, 2024 to 2026: Sampling Guide", K.DEPT)
    st = [Paragraph("PFAS Initial Monitoring, Community Water Systems, 2024 to 2026", S["h1"]),
          Paragraph("Sampling Guide. %s, Drinking Water Program. Revision 2, December 2023." % K.DEPT, S["meta"])]
    parts = [
        ("1. Scope", "Every community water system samples every entry point to its distribution system for PFAS once "
                     "in each calendar quarter from January 2024 through June 2026. The department's program samplers "
                     "collect most samples on their quarterly routes; certified operators collect the rest under this "
                     "guide."),
        ("2. Where to sample", "At the entry point's sampling tap: after the last source connection and after any "
                               "treatment, before the first service connection. Run the tap for five minutes before "
                               "filling. Do not sample at a wellhead, a storage tank or a customer's tap for initial "
                               "monitoring."),
        ("3. When", "Once in each calendar quarter, on the route day set for the system. When a laboratory reports PFOA "
                    "or PFOS above 4.0 ng/L for an entry point, the program collects a confirmation sample at the same "
                    "entry point within 14 days of the report. Collect samples with the system operating as it "
                    "normally does on that day; do not start or stop wells for the sample."),
        ("4. The collection record", "Complete one record for each bottle set. State sample number (from the label "
                                     "sheet). Sample point (the entry point's code in the inventory). Sample type: RT "
                                     "routine, CO confirmation, FD field duplicate, FRB field reagent blank. Date and "
                                     "time collected. Collector. Sources in service: every well or plant pumping to the "
                                     "entry point when the sample is drawn (ask the operator or read the control "
                                     "panel). Entry-point flow: the entry-point meter's flow in gallons a minute at "
                                     "collection. Free chlorine residual in mg/L. Remarks."),
        ("5. Quality control", "A field reagent blank goes with about one visit in eight: laboratory reagent water "
                               "poured into a sample bottle at the tap. A field duplicate, a second bottle filled "
                               "from the same tap straight after the first, is taken at about one visit in sixteen. "
                               "Blanks and duplicates check the sampling and the laboratory; they are not results for "
                               "the entry point."),
        ("6. Laboratories", "Samples go to the State Environmental Health Laboratory or one of the two contract "
                            "laboratories on the route sheet. Results are reported in ng/L by EPA Method 533, or 537.1 "
                            "at Kestrel Environmental Testing, which reports that method's list of PFAS. A result "
                            "below the laboratory's reporting limit is reported as less than the limit. Laboratories "
                            "load results to the state database within 28 days of collection."),
        ("7. Reissued reports", "When a laboratory reissues a report, the database keeps the earlier report and loads "
                                "the reissued one beside it with the next revision number. The highest revision is the "
                                "result of record."),
        ("8. Holding times", "Ship on ice the day of collection. Method 533 and 537.1 samples must be extracted within "
                             "28 days of collection (533) or 14 days (537.1); a sample past its holding time is "
                             "recollected."),
    ]
    for h, t in parts:
        st.append(Paragraph(h, S["h2"]))
        st.append(Paragraph(t, S["body"]))
    st.append(Paragraph("Questions: Drinking Water Program, PFAS monitoring coordinator.", S["note"]))
    doc.build(st, onFirstPage=_frame("PFAS initial monitoring: sampling guide, rev. 2", K.DEPT),
              onLaterPages=_frame("PFAS initial monitoring: sampling guide, rev. 2", K.DEPT))


# ---------------------------------------------------------------------------------------------- the notes
def data_notes(files, counts):
    f = files
    lines = [
        "Data for the Authority's 2027 PFAS design-grant review",
        "From: %s, PFAS compliance lead, Drinking Water Program" % K.PEOPLE["lead"],
        "To: %s, %s" % (K.PEOPLE["manager"], AUTHORITY),
        "Sent: 2 September 2026",
        "",
        "Judy, the files you asked for are below, with what each one holds. Everything is as the systems and",
        "laboratories reported it; we have not edited any of it.",
        "",
        "%s" % f["results"],
        "  Every community water system's PFAS results in the state database as of %s (%s rows):" % (
            K.PULL.strftime("%-d %B %Y"), "{:,}".format(counts["results"])),
        "  one row per analyte per sample per report revision. result is blank when result_sign is '<' (less than the",
        "  reporting_limit). sample_type RT routine, CO confirmation, FD field duplicate, FRB field reagent blank.",
        "  Dates are the collection date and time.",
        "",
        "%s" % f["records"],
        "  The samplers' collection records, one per bottle set (%s). collected is month/day/year." % "{:,}".format(
            counts["records"]),
        "  sources_in_service is as the sampler wrote it.",
        "",
        "%s" % f["inventory"],
        "  Source facilities of every community water system as of 1 September 2026, with the field notes on the second",
        "  sheet.",
        "",
        "%s" % f["mor"],
        "  Every system's 2025 monthly operating reports as filed (%s rows): one row per facility per month with the" % "{:,}".format(
            counts["mor"]),
        "  meter readings at the start and end of the month, the gallons for the month and the days in service.",
        "",
        "%s" % f["meters"],
        "  Source meters as of 1 September 2026. facility_ids lists the facilities a meter measures; removed is the date",
        "  a meter came out.",
        "",
        "%s" % f["register"],
        "  Community water systems as of 1 September 2026. population_served is the number of people the system serves",
        "  directly (its own customers); a system that sells water to another counts only its own customers.",
        "",
        "%s" % f["connections"],
        "  Connections through which one system takes water from another, from our register. connection_type: Full",
        "  purchase (the buyer takes all its water through the connection) or Emergency (opened only when one side loses",
        "  supply). in_service_to is the date a connection was closed; blank if it is open.",
        "",
        "%s" % f["labs"],
        "  The laboratories that report PFAS to us.",
        "",
        "%s" % f["survey"],
        "  The federal survey's results for our systems, as EPA published them (micrograms per litre, EPA's facility and",
        "  sample point numbers), two events in 2023.",
        "",
        "%s" % f["private"],
        "  Our private well program's results, 2024 to June 2026 (homeowners' samples; ng/L).",
        "",
        "The plan's section 6 and our sampling guide are attached as PDFs.",
        "",
        "Lynn",
    ]
    return "\n".join(lines) + "\n"
