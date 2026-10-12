"""The pack's documents: the checkpoint planning standard (2026 edition) and the 2023 edition it replaced, the mobile
screening unit's deployment policy for 2027, the extract notes and the throughput detector's spring 2027 flags."""
import json

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer        # noqa: E402

import records as R    # noqa: E402
import world as W      # noqa: E402

STANDARD_26 = "checkpoint_planning_standard_2026.pdf"
STANDARD_23 = "checkpoint_planning_standard_2023.pdf"
POLICY = "mobile_screening_unit_deployment_policy_2027.pdf"
NOTES = "extract_notes_2027-04-23.md"
FLAGS = "throughput_detector_flags_spring2027.json"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif", FONT_DIR + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif-Bold", FONT_DIR + "LiberationSerif-Bold.ttf"))
SANS, SANS_B, SERIF, SERIF_B = "LiberationSans", "LiberationSans-Bold", "LiberationSerif", "LiberationSerif-Bold"
INK = colors.HexColor("#1d2126")
GREY = colors.HexColor("#5d646b")

# Standards and Planning: serif, numbered clauses
A_BODY = ParagraphStyle("abody", fontName=SERIF, fontSize=10.4, leading=14, textColor=INK, spaceAfter=5)
A_CLAUSE = ParagraphStyle("aclause", parent=A_BODY, leftIndent=26, firstLineIndent=-26)
A_H1 = ParagraphStyle("ah1", fontName=SERIF_B, fontSize=15, leading=19, textColor=INK, spaceAfter=3)
A_H2 = ParagraphStyle("ah2", fontName=SERIF_B, fontSize=11, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
A_META = ParagraphStyle("ameta", fontName=SERIF, fontSize=8.8, leading=11.5, textColor=GREY, spaceAfter=8)
# the operations directorate: sans
S_BODY = ParagraphStyle("sbody", fontName=SANS, fontSize=9.6, leading=13, textColor=INK, spaceAfter=5)
S_H1 = ParagraphStyle("sh1", fontName=SANS_B, fontSize=14, leading=17.5, textColor=INK, spaceAfter=2)
S_H2 = ParagraphStyle("sh2", fontName=SANS_B, fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=8, spaceAfter=3)
S_META = ParagraphStyle("smeta", fontName=SANS, fontSize=8.2, leading=10.5, textColor=GREY, spaceAfter=7)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=23 * mm, rightMargin=23 * mm, topMargin=21 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot, font=SERIF):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 8)
        if top_left:
            canvas.drawString(23 * mm, A4[1] - 12 * mm, top_left)
            canvas.drawRightString(A4[0] - 23 * mm, A4[1] - 12 * mm, top_right)
        canvas.setFont(font, 7.4)
        canvas.drawString(23 * mm, 11 * mm, foot)
        canvas.drawRightString(A4[0] - 23 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _standard(path, edition, issued, clauses, front):
    who, role = W.PEOPLE["standard"]
    title = "Checkpoint planning standard, %s edition" % edition
    doc = _doc(path, title, who)
    s = [Paragraph("%s · STANDARDS AND PLANNING" % W.AGENCY.upper(), A_META), Paragraph(title, A_H1),
         Paragraph("KAS-STD-07. Issued %s by %s, %s." % (issued, who, role), A_META)]
    for line in front:
        s.append(Paragraph(line, A_META))
    for head, items in clauses:
        s.append(Paragraph(head, A_H2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), A_CLAUSE))
    foot = "%s | KAS-STD-07 | %s edition" % (W.AGENCY, edition)
    doc.build(s, onFirstPage=_frame("KAS-STD-07", "%s edition" % edition, foot),
              onLaterPages=_frame("KAS-STD-07", "%s edition" % edition, foot))


def write_standard_2026(path):
    _standard(path, "2026", "16 February 2026", [
        ("1. Scope", [
            ("1.1", "This standard sets how %s plans screening capacity at the central checkpoints of the airports "
                    "it screens, and how a change to that capacity is judged." % W.AGENCY),
            ("1.2", "It replaces the 2023 edition from 1 March 2026."),
        ]),
        ("2. The wait standard", [
            ("2.1", "A passenger should wait no more than 20 minutes from joining the checkpoint queue to reaching "
                    "the divest point."),
            ("2.2", "A passenger whose expected wait is more than 20 minutes is outside the standard. A passenger "
                    "whose expected wait is 20 minutes or less is within it."),
        ]),
        ("3. Lanes", [
            ("3.1", "An open lane is a screening lane staffed and screening passengers. Lanes are counted whole."),
            ("3.2", "For planning, an open lane screens 150 passengers an hour, 37.5 in 15 minutes, whatever its "
                    "equipment."),
        ]),
        ("4. Expected wait", [
            ("4.1", "Planning works in 15-minute intervals from 04:00 to 22:00. The checkpoint is empty at 04:00."),
            ("4.2", "The expected wait of the passengers arriving in an interval, in minutes, is 15 times the "
                    "passengers queuing at the start of the interval plus half the passengers arriving in it, "
                    "divided by the passengers the open lanes screen in 15 minutes."),
            ("4.3", "The passengers queuing at the end of an interval are those queuing at its start plus those "
                    "arriving in it less those the open lanes screen in 15 minutes, and never fewer than none."),
        ]),
        ("5. Design days", [
            ("5.1", "Capacity Planning's summer planning sheet gives a design day for each period: the passengers "
                    "forecast to arrive at each checkpoint in each interval on a typical day of the period."),
            ("5.2", "A design day stands for each day of its period."),
        ]),
        ("6. Judging a change", [
            ("6.1", "A change that adds or removes screening capacity at a checkpoint (a roster change, new "
                    "equipment, a deployment) is judged by the passengers it moves within the standard: on each "
                    "design day, the passengers outside the standard on the lanes open without the change less "
                    "those outside it on the lanes open with it, times the days in the period."),
            ("6.2", "Passenger figures from a planning run are reported to the nearest hundred."),
        ]),
        ("7. Changes from the 2023 edition", [
            ("7.1", "The planning rate rises from 140 to 150 passengers an hour, with computed tomography lanes in "
                    "service at every central checkpoint."),
            ("7.2", "The expected wait now counts half the interval's arrivals with the queue at its start; the 2023 "
                    "edition used the queue at the interval's end."),
        ]),
    ], ["Applies to: Capacity Planning, duty managers, the mobile screening unit."])


def write_standard_2023(path):
    _standard(path, "2023", "9 January 2023", [
        ("1. Scope", [
            ("1.1", "This standard sets how %s plans screening capacity at the central checkpoints of the airports "
                    "it screens." % W.AGENCY),
        ]),
        ("2. The wait standard", [
            ("2.1", "A passenger should wait no more than 20 minutes from joining the checkpoint queue to reaching "
                    "the divest point."),
        ]),
        ("3. Lanes", [
            ("3.1", "For planning, an open lane screens 140 passengers an hour, 35 in 15 minutes."),
        ]),
        ("4. Expected wait", [
            ("4.1", "Planning works in 15-minute intervals. The expected wait in an interval, in minutes, is 15 times "
                    "the passengers queuing at the end of the interval divided by the passengers the open lanes "
                    "screen in 15 minutes."),
            ("4.2", "An interval whose expected wait is more than 20 minutes is a breach interval."),
        ]),
        ("5. Design days", [
            ("5.1", "Capacity Planning's planning sheet gives a design day for each season."),
        ]),
    ], [])


def write_policy(path):
    who, role = W.PEOPLE["head"]
    title = "Mobile screening unit: deployment policy 2027"
    doc = _doc(path, title, who)
    p = lambda t, st=S_BODY: Paragraph(t, st)
    s = [p(W.AGENCY.upper() + " · SCREENING OPERATIONS", S_META), p(title, S_H1),
         p("Approved 2 March 2027 by %s, %s. Replaces the 2025 deployment note." % (who, role), S_META)]
    sec = [
        ("The unit", [
            "The mobile screening unit is 24 screening officers on two shifts, a team leader and three transportable "
            "screening lanes. At a posting it screens passengers on the host checkpoint's three mobile unit "
            "positions (M1 to M3) from 05:00 to 21:00 every day. Before 05:00 and after 21:00 the checkpoints search "
            "their own staff and the airlines' aircrew coming on and off duty, and the unit does not screen.",
            "The unit's officers are based at the agency's headquarters and travel to each posting."]),
        ("Postings from 2027", [
            "In 2025 and 2026 the unit rotated weekly between airports. From summer 2027 it is posted to one airport "
            "for the whole summer, 15 June to 31 August, which saves the weekly moves and gives one checkpoint the "
            "unit for the whole season."]),
        ("Choosing the airport", [
            "The Head of Screening Operations posts the unit, by 30 April, to the airport where it will move the "
            "most passengers within the 20-minute standard over the posting, judged as the checkpoint planning "
            "standard (KAS-STD-07, section 6) sets out on Capacity Planning's summer planning sheet, among the "
            "airports the throughput detector flagged in the spring."]),
        ("The host airport", [
            "The host provides the mobile unit positions with power and data, a secure store for the lanes, and a "
            "daily briefing for the team leader with the duty manager."]),
        ("Running a posting", [
            "The lanes travel on the unit's two vans on the Sunday before a posting begins and are set up and "
            "tested that evening; officers check into the booked hotel the same day. Each shift opens with the "
            "unit's own equipment checks, and a lane that fails them stays closed until the fault is cleared.",
            "The team leader sends Screening Operations a daily return of the unit's lanes opened and the passengers "
            "they screened, and reports any day the unit could not open all three lanes, with the reason.",
            "A posting ends on the Sunday night. The unit leaves the positions as it found them."]),
        ("Costs", [
            "The unit's travel, accommodation and subsistence are charged to cost centre %s (mobile screening "
            "unit) under the travel and subsistence circular. Hotels are booked against a purchase order raised "
            "for each posting." % R.UNIT_CC]),
    ]
    for h, paras in sec:
        s.append(p(h, S_H2))
        s += [p(x) for x in paras]
    foot = "%s | Screening Operations | deployment policy 2027" % W.AGENCY
    doc.build(s, onFirstPage=_frame("", "", foot, SANS), onLaterPages=_frame("", "", foot, SANS))


def write_notes(path):
    who, role = W.PEOPLE["analyst"]
    lines = [
        "# Extract notes, 23 April 2027",
        "",
        "Prepared by %s (%s) for the Head of Screening Operations' summer 2027 posting of the mobile screening "
        "unit. The extracts cover the eight airports the throughput detector flagged this spring." % (who, role),
        "",
        "Airport codes are the operations codes used across Screening Operations: " +
        ", ".join("%s %s" % (c, W.NAME[c]) for c in R.SORTED) + ". Times are local.",
        "",
        "## Files",
        "",
        "- `%s`: the lane sensor feed for 15 June to 31 August 2026. A row is one lane in one 15-minute interval "
        "in which it screened; `pax_screened` is the count through the lane's divest point. The mobile unit's "
        "lanes (M1 to M3) appear at the airport hosting it." % R.LANE_COUNTS,
        "- `%s`: queue time from the queue cameras, the median minutes from joining the queue to the divest point "
        "for people reaching it in the interval. Intervals with no reading (camera resets) are missing." % R.QUEUE_TIME,
        "- `%s`: the summer 2026 roster pattern, the lanes each checkpoint planned for its own officers by 15 "
        "minutes, one pattern for every day of the roster period." % R.ROSTER_26,
        "- `%s`: the summer 2027 roster pattern, issued by the airports' duty managers in April 2027 from the new "
        "rostering tool (one column per checkpoint; valid 30 May to 11 September 2027)." % R.ROSTER_27,
        "- `%s`: Capacity Planning's summer 2027 planning sheet (design days; see its Notes sheet)." % R.PLANNING,
        "- `%s`: the unit's 2026 postings, Monday to Sunday, with officers, officer-nights and the hotel "
        "purchase order." % R.POSTINGS,
        "- `%s`: the lanes and mobile unit positions at each central checkpoint." % R.REGISTER,
        "- `%s`: the operators' monthly traffic returns for 2026." % R.RETURNS,
        "- `%s`: payables lines for cost centre %s, hotel invoices and credit notes for summer 2026. Amounts are "
        "as paid, including VAT, which the agency does not recover." % (R.HOTELS, R.UNIT_CC),
        "- `%s`: the expense claims export for cost centre %s, claims approved June to October 2026."
        % (R.CLAIMS, R.UNIT_CC),
        "- `%s`: lane faults logged by the duty managers in 2026." % R.FAULTS,
        "- `%s`: passenger feedback about security at the eight airports, summer 2026." % R.FEEDBACK,
        "- `%s`: the throughput detector's spring 2027 run." % FLAGS,
        "- `%s`, `%s`, `%s`." % (STANDARD_26, STANDARD_23, POLICY),
        "",
        "## Not in this extract",
        "",
        "- Officers' duty rosters (Human Resources).",
        "- Lane sensor and queue-time data before 15 June 2026.",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# spring 2027 detector run: ten airports screened, eight flagged
FLAG_ROWS = [
    ("ARD", True, ["2027-W11", "2027-W13", "2027-W14", "2027-W15"], 61, 38.4),
    ("BRN", True, ["2027-W12", "2027-W14"], 23, 27.9),
    ("CUL", True, ["2027-W10", "2027-W11", "2027-W14", "2027-W15"], 57, 41.2),
    ("DRM", True, ["2027-W13", "2027-W14", "2027-W15"], 34, 29.6),
    ("ESK", True, ["2027-W14", "2027-W15"], 28, 31.5),
    ("FAR", True, ["2027-W11", "2027-W14"], 31, 33.8),
    ("GLK", True, ["2027-W13", "2027-W15"], 19, 26.3),
    ("HAL", True, ["2027-W14", "2027-W15"], 22, 35.7),
    ("KMR", False, [], 0, 14.2),
    ("TLN", False, [], 2, 18.9),
]


def write_flags(path):
    out = {
        "detector": "KAS throughput detector",
        "version": "3.2",
        "run_at": "2027-04-19T06:10:00",
        "window": {"from": "2027-03-01", "to": "2027-04-18"},
        "rule": "flag an airport when queue time exceeds 20 minutes in more than 12 intervals in an ISO week, or "
                "lane throughput falls more than 15 per cent below its trailing eight-week level",
        "airports": [
            {"airport": c, "flagged": f, "weeks_flagged": wk, "breach_intervals": n, "max_queue_time_min": q}
            for c, f, wk, n, q in FLAG_ROWS
        ],
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
