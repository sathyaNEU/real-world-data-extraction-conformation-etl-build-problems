"""The pack's documents: the plan's criteria for the 2027 Community Engagement Support track, the survey vendor's
methods report, the vendor's pilot memo, the plan's analytics data guide, and the pack's contents."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1f2428"), colors.HexColor("#5d646a"), colors.HexColor("#b8bfc4")
TEAL = colors.HexColor("#14606b")
SLATE = colors.HexColor("#3b4a6b")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.4, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(.8 * inch, letter[1] - .5 * inch, left)
        canvas.drawRightString(letter[0] - .8 * inch, letter[1] - .5 * inch, right)
        canvas.drawRightString(letter[0] - .8 * inch, .45 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=.85 * inch, rightMargin=.85 * inch,
                             topMargin=.8 * inch, bottomMargin=.75 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


# ---------------------------------------------------------------------------------------------- the track's criteria
def write_criteria(path):
    S = styles("Sans", TEAL)
    doc = _doc(path, "Community Engagement Support track 2027: criteria for the regions", K.PLAN)
    s = [Paragraph("Community Engagement Support track 2027: criteria for the regions", S["h1"]),
         Paragraph("%s, Community Health Programs. %s, %s. Approved by the Programs and Quality Committee of the Board "
                   "on 16 September 2026; the Board adopts the four regions at its meeting of 10 December 2026."
                   % (K.PLAN, K.PEOPLE["requester"], K.PEOPLE["requester_title"]), S["meta"]),
         Paragraph("1. The track", S["h2"]),
         Paragraph("From 1 January 2027 Washington's Apple Health coverage for adults in the expansion group asks each "
                   "member aged 19 to 64 to show 80 hours a month of work, community service, a work program or school, "
                   "unless the member is exempt. The plan's Community Engagement Support track places community "
                   "engagement navigators in a region to help members find hours, report them and claim the exemptions "
                   "they have. The 2027 budget funds navigator teams in four regions.", S["body"]),
         Paragraph("2. Which regions", S["h2"]),
         _clause(S, "2.1", "The track goes to the four of the plan's ten Apple Health regions where the smallest share "
                           "of the plan's expansion members worked for pay 80 hours or more in March 2026."),
         _clause(S, "2.2", "A region's share is for the plan's expansion members aged 19 to 64 enrolled in the region on "
                           "1 March 2026, every one of them: the members the 2026 Member Work and Income Survey reached "
                           "and the members it did not. It is estimated from the survey, which drew 1,500 of those "
                           "members in each region."),
         _clause(S, "2.3", "Worked for pay 80 hours or more in March 2026 means the member's hours of paid work in "
                           "March 2026, all jobs together, self-employment and app-based work included, came to 80 or "
                           "more."),
         _clause(S, "2.4", "The shares are compared unrounded and reported to the nearest whole percent."),
         Paragraph("3. Planning figures for each region", S["h2"]),
         _clause(S, "3.1", "A member's region is the Apple Health region of the county the member lives in on the day "
                           "a figure is taken."),
         _clause(S, "3.2", "Members covered: the plan's expansion members who are aged 19 to 64 and whose coverage with "
                           "the plan includes 1 October 2026."),
         _clause(S, "3.3", "Parents and caretakers: the members covered (3.2) who on 1 October 2026 are the case head, "
                           "the spouse or a caretaker relative in an Apple Health case with a child under 14 in it on "
                           "that day. The state exempts parents and caretaker relatives of a child aged 13 or under."),
         Paragraph("4. Timetable", S["h2"]),
         Paragraph("Community Health Programs brings the regions and the planning figures to the Board on 10 December "
                   "2026. Navigator teams start in January 2027 and the Board reviews the track in its first year.",
                   S["body"])]
    doc.build(s, onFirstPage=_frame(K.PLAN, "Community Engagement Support track 2027", "Sans"),
              onLaterPages=_frame(K.PLAN, "Community Engagement Support track 2027", "Sans"))


# ---------------------------------------------------------------------------------------------- the methods report
def write_methods(path, fieldwork, frame_n):
    S = styles("Serif", SLATE)
    doc = _doc(path, "2026 Member Work and Income Survey: methods report", K.VENDOR)
    t1 = [["Region", "Members on 1 March 2026", "Sampled"]]
    for code in K.CODES:
        t1.append([K.NAME[code], "{:,}".format(frame_n[code]), "1,500"])
    t1.append(["All regions", "{:,}".format(sum(frame_n.values())), "15,000"])
    t2 = [["Region", "First called by the Member Services Center", "Passed to Kestrelby", "Completed", "Declined",
           "Not reached"]]
    for code in K.CODES:
        f = fieldwork[code]
        t2.append([K.NAME[code], "{:,}".format(f["msc"]), "{:,}".format(f["passed"]), "{:,}".format(f["complete"]),
                   "{:,}".format(f["declined"]), "{:,}".format(f["noncontact"])])
    codes = [["Code", "Outcome of a call"]] + [[str(c), d] for c, d in K.DISPO.items()]
    s = [Paragraph("2026 Member Work and Income Survey: methods report", S["h1"]),
         Paragraph("%s for %s. %s, %s. 30 June 2026." % (K.VENDOR, K.PLAN, K.PEOPLE["vendor"], K.PEOPLE["vendor_title"]),
                   S["meta"]),
         Paragraph("1. Population and sample", S["h2"]),
         Paragraph("The survey covers the plan's members in the Apple Health expansion group aged 19 to 64 and enrolled "
                   "on 1 March 2026. Kestrelby drew a simple random sample of 1,500 members in each of the ten Apple "
                   "Health regions from the plan's enrollment file of that day, the region being the region of the "
                   "member's county on the file. Each region's sample was split at random into four releases of 13, 20 "
                   "and 27 April and 4 May 2026.", S["body"]),
         _table(S, t1, [2.0, 2.0, 1.0], right=(1, 2)),
         Paragraph("2. Questionnaire", S["h2"]),
         Paragraph("The interview asks for each job the member held in March 2026, up to three, what kind of work it "
                   "was and how many hours in total the member worked at it in March. The total of the hours is "
                   "computed by the interviewing system. It also asks whether a member with fewer than 80 hours was "
                   "looking for work, whether a health condition limits the work the member can do, and whether the "
                   "member would like help from the plan. The interview takes about nine minutes.", S["body"]),
         Paragraph("3. Calls", S["h2"]),
         Paragraph("Every call showed the plan's caller ID. A call either reached the member, who then did the "
                   "interview or declined on that call, or did not. The plan's Member Services Center in Tacoma made "
                   "the first calls to the cases the sample management system assigned to it, on weekdays from 9:00 "
                   "a.m. to 4:30 p.m., up to six calls (four for cases in the third and fourth releases). Cases it had "
                   "not reached by then were passed to Kestrelby as Kestrelby's capacity allowed, for up to four "
                   "further calls. Kestrelby called its own cases on weekdays from 9:00 a.m. to 4:30 p.m. and from "
                   "5:30 to 8:30 p.m., and on Saturdays from 10:00 a.m. to 2:00 p.m., up to eight calls (six for the "
                   "third and fourth releases). Calls stopped on 29 May 2026; no calls were made on Memorial Day. A "
                   "member who declined the interview was asked one question before the call ended: whether the "
                   "member's paid work in March 2026, all jobs together, came to 80 hours or more.",
                   S["body"]),
         _table(S, t2, [1.35, 1.45, 0.95, 0.8, 0.7, 0.75], right=(1, 2, 3, 4, 5)),
         Paragraph("4. Call outcomes", S["h2"]),
         Paragraph("Kestrelby's dialer records every call with one of these outcomes; the Member Services Center's "
                   "CRM records the same outcomes in words.", S["body"]),
         _table(S, codes, [0.7, 4.0]),
         Paragraph("5. Files", S["h2"]),
         Paragraph("The sample file lists every sampled member with the case number, the plan's member ID, region, "
                   "age on 1 March 2026, sex, preferred language, release and the center assigned the first calls. "
                   "The dialer export lists every call Kestrelby made, including its February pilot and its test "
                   "calls of 10 April; times carry their offset from UTC. The interview file has one row for each "
                   "completed interview, including six test interviews, and one for each member who declined and "
                   "answered the key question (status Declined - key question). The Member Services Center's calls "
                   "are in "
                   "the plan's CRM export. Kestrelby delivered the data without weights: each region's sample is an "
                   "equal-probability sample of the region's members.", S["body"])]
    doc.build(s, onFirstPage=_frame(K.VENDOR, "MWIS 2026 methods report", "Serif"),
              onLaterPages=_frame(K.VENDOR, "MWIS 2026 methods report", "Serif"))


# ---------------------------------------------------------------------------------------------- the pilot memo
def write_pilot(path):
    S = styles("Serif", SLATE)
    doc = _doc(path, "MWIS pilot, February 2026", K.VENDOR)
    t = [["Item", "Pilot wording", "Change for the main survey"],
         ["Hours", "Hours worked in a usual week", "Hours worked in March, in total, for each job"],
         ["Jobs", "Main job only", "Up to three jobs, with the kind of work for each"],
         ["App-based work", "Not asked separately", "Counted as a job when paid"],
         ["Help from the plan", "Yes or no", "Unchanged"]]
    s = [Paragraph("Member Work and Income Survey: pilot memo", S["h1"]),
         Paragraph("%s to %s, Community Health Programs. 27 February 2026." % (K.VENDOR, K.PLAN), S["meta"]),
         Paragraph("Kestrelby piloted the questionnaire with 300 expansion members from 2 to 20 February 2026. The "
                   "pilot tested the wording and the length of the interview, not the sample or the estimates, and its "
                   "answers are not used in the survey's results.", S["body"]),
         Paragraph("Members found a usual week hard to describe when their hours changed from week to week, and app-"
                   "based drivers did not count their trips as a job. The main survey asks for the hours of each job "
                   "in March in total and counts paid app-based work as a job. The interview ran 11 minutes on average "
                   "in the pilot and about nine with the shorter wording.", S["body"]),
         _table(S, t, [1.3, 2.1, 2.5])]
    doc.build(s, onFirstPage=_frame(K.VENDOR, "MWIS pilot memo", "Serif"),
              onLaterPages=_frame(K.VENDOR, "MWIS pilot memo", "Serif"))


# ---------------------------------------------------------------------------------------------- the data guide
def write_guide(path):
    S = styles("Sans", TEAL)
    doc = _doc(path, "Data guide: 2027 Community Engagement Support figures", K.PLAN)
    crm = [["Column", "Meaning"], ["Member ID", "The plan's member ID"], ["Activity Date, Activity Time", "When the activity "
           "was logged, Pacific time"], ["Activity Type", "MWIS outbound call, MWIS case transfer, or the center's other "
           "outreach (welcome calls, care coordination, pharmacy reminders)"], ["Result", "The outcome the agent recorded"]]
    roster = [["Column", "Meaning"], ["member_id, p1_client_id", "The plan's member ID and the state's ProviderOne client "
              "ID"], ["birth_date", "Date of birth (MM/DD/YYYY)"], ["county, region", "The member's county of residence "
              "and its Apple Health region"], ["coverage_group", "N05, the Apple Health expansion adult group"],
              ["enrollment_begin, scheduled_end", "The begin date of the member's enrollment with the plan and, where the "
               "state has sent one, the last covered day"]]
    chg = [["Change", "effective_date"], ["ADD", "First covered day"], ["TERM", "Last covered day"],
           ["REINSTATE", "Coverage restored from this day"], ["ADDRESS", "The move; county_before and county_after"]]
    hh = [["Column", "Meaning"], ["case_id, p1_client_id", "The Apple Health case and the person"],
          ["case_role", "HOH case head, SPOUSE, CARETAKER_RELATIVE, OTHER_ADULT, CHILD"],
          ["member_begin, member_end", "The person's days in the case under that role"],
          ["children_under_14_in_case", "Children under 14 in the case"]]
    s = [Paragraph("Data guide: 2027 Community Engagement Support figures", S["h1"]),
         Paragraph("%s, Analytics and Reporting, for Community Health Programs. 20 October 2026." % K.PLAN, S["meta"]),
         Paragraph("1. Survey files", S["h2"]),
         Paragraph("%s, %s and %s are Kestrelby's, described in its methods report. %s is the plan's CRM export of "
                   "every Member Services Center activity on the sampled members from 13 April to 29 May 2026."
                   % (K.FILES["sample"], K.FILES["dialer"], K.FILES["interviews"], K.FILES["crm"]), S["body"]),
         _table(S, crm, [1.7, 4.2]),
         Paragraph("2. Enrollment files", S["h2"]),
         Paragraph("%s is the plan's active expansion roster as exported on 19 October 2026, one row per member."
                   % K.FILES["roster"], S["body"]),
         _table(S, roster, [1.9, 4.0]),
         Spacer(1, 4),
         Paragraph("%s is the enrollment system's change log from 1 to 19 October 2026, pipe-delimited, one line per "
                   "change the system applied, with the time it was logged, both member IDs, the member's birth date "
                   "(YYYYMMDD), the change and its effective date (YYYYMMDD), and the county before and after:"
                   % K.FILES["changes"], S["body"]),
         _table(S, chg, [1.3, 4.6]),
         Spacer(1, 4),
         Paragraph("%s is the Health Care Authority's household composition extract of 15 October 2026 for the "
                   "Apple Health cases that held a plan expansion member at any time from 1 September 2026, one row per "
                   "person per role in a case." % K.FILES["cases"], S["body"]),
         _table(S, hh, [1.9, 4.0]),
         Paragraph("3. Regions", S["h2"]),
         Paragraph("%s lists the ten Apple Health regions and their counties." % K.FILES["regions"], S["body"])]
    doc.build(s, onFirstPage=_frame(K.PLAN, "Analytics and Reporting", "Sans"),
              onLaterPages=_frame(K.PLAN, "Analytics and Reporting", "Sans"))


def write_contents(path, items):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("Community Engagement Support track 2027: board pack evidence files\n")
        f.write("%s, Community Health Programs, assembled 20 October 2026\n\n" % K.PLAN)
        for name, desc in items:
            f.write("%s\n    %s\n" % (name, desc))
