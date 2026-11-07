"""task156: the pack's documents. The ballot agent's declarations and the branch's guide are written in a word
processor and exported to PDF (officepdf: Writer's export, dates set to the issue date)."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table

import officepdf as O
import population as PO
import world as W

AEDT = dt.timezone(dt.timedelta(hours=11))
AEST = dt.timezone(dt.timedelta(hours=10))
F_PAB21 = "tallyhouse_pab_declarations_2021.pdf"
F_PAB24 = "tallyhouse_pab_declarations_2023-24.pdf"
F_GUIDE = "lsu_pab_guide_for_officials_2025.pdf"
F_BUREAU = "western_shires_payroll_statements_2025-26.pdf"


def _st():
    ss = getSampleStyleSheet()
    navy = colors.HexColor("#1F3864")
    return dict(
        body=ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13, spaceAfter=6),
        head=ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                            spaceAfter=3, spaceBefore=8, textColor=navy),
        title=ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=18,
                             spaceAfter=6, textColor=navy),
        small=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=8.4, leading=11, spaceAfter=6),
        cell=ParagraphStyle("c", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6, leading=10.5),
    )


def fmt_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def _decl_story(rows, fmt):
    st = _st()
    story = []
    for i, r in enumerate(rows):
        if i:
            story.append(PageBreak())
        order = "PA%s/%04d" % (r["close"].year if fmt == "21" else r["open"].year, 1100 + 37 * i)
        if fmt == "21":
            story += [Paragraph(W.AGENT, st["small"]), Paragraph("DECLARATION OF RESULT OF PROTECTED ACTION BALLOT",
                                                                  st["title"]),
                      Paragraph("Fair Work Act 2009, section 456", st["small"]),
                      Paragraph("Employer: %s" % W.NAME[r["council"]], st["body"]),
                      Paragraph("Applicant: %s" % W.UNION, st["body"]),
                      Paragraph("Order: %s" % order, st["body"]),
                      Spacer(1, 6)]
            tbl = [["Item", "Detail"],
                   ["Roll date", fmt_date(r["roll_date"])],
                   ["Ballot opened", fmt_date(r["open"])],
                   ["Ballot closed", fmt_date(r["close"])],
                   ["Persons on the roll", "{:,}".format(r["roll"])],
                   ["Ballot papers returned", "{:,}".format(r["returned"])],
                   ["Informal ballot papers", "{:,}".format(r["informal"])],
                   ["Question 1: Yes", "{:,}".format(r["yes"])],
                   ["Question 1: No", "{:,}".format(r["no"])]]
            story.append(Table(tbl, colWidths=[200, 160]))
            story.append(Spacer(1, 8))
            story.append(Paragraph("I declare that at least 50 per cent of the persons on the roll voted in the ballot "
                                   "and that more than 50 per cent of the valid votes approved the action."
                                   if r["returned"] >= 0.5 * r["roll"] else
                                   "I declare that fewer than 50 per cent of the persons on the roll voted in the "
                                   "ballot. The proposed industrial action is not authorised.", st["body"]))
            story.append(Paragraph("Returning officer, %s" % W.AGENT, st["small"]))
        else:
            story += [Paragraph("DECLARATION", st["title"]),
                      Paragraph("Protected action ballot conducted under an order of the Fair Work Commission", st["small"]),
                      Paragraph("Employer: %s" % W.NAME[r["council"]], st["body"]),
                      Paragraph("Bargaining representative (applicant): %s" % W.UNION, st["body"]),
                      Paragraph("Commission order %s; ballot by post and online" % order, st["body"]), Spacer(1, 6)]
            tbl = [["", "Count"],
                   ["Number of persons on roll", "{:,}".format(r["roll"])],
                   ["Total votes received (post and online)", "{:,}".format(r["returned"])],
                   ["Informal or rejected", "{:,}".format(r["informal"])],
                   ["Votes in favour", "{:,}".format(r["yes"])],
                   ["Votes against", "{:,}".format(r["no"])],
                   ["Participation", "%.1f%%" % (100.0 * r["returned"] / r["roll"])]]
            story.append(Table(tbl, colWidths=[240, 120]))
            story.append(Spacer(1, 6))
            story.append(Paragraph("Roll closed %s. Voting opened %s and ballot closed %s at 5:00 pm."
                                   % (fmt_date(r["roll_date"]), fmt_date(r["open"]), fmt_date(r["close"])), st["body"]))
            story.append(Paragraph("Result: %s" % ("the participation requirement was met and the question was carried."
                                                   if r["returned"] >= 0.5 * r["roll"] else
                                                   "the participation requirement was not met."), st["body"]))
            story.append(Paragraph("For the returning officer, %s, %s" % (W.AGENT, fmt_date(r["close"] +
                                                                                       dt.timedelta(days=3))),
                                   st["small"]))
    return story


def pab_pdfs(out):
    P = PO.build()
    for rnd, f in (("21", F_PAB21), ("24", F_PAB24)):
        rows = sorted([r for r in P.pab if r["round"] == rnd], key=lambda r: (r["close"], r["council"]))
        last = max(r["close"] for r in rows) + dt.timedelta(days=4)
        when = dt.datetime(last.year, last.month, last.day, 15, 42, 10, tzinfo=AEST if rnd == "21" else AEDT)
        title = ("Protected action ballots 2021: declarations of result" if rnd == "21" else
                 "Protected action ballots 2023-24: declarations")
        O.build(os_join(out, f), _decl_story(rows, rnd), title, W.AGENT,
                "Declarations of protected action ballot results for %s" % W.UNION,
                "%s, declarations issued to %s" % (W.AGENT, W.UNION), when, when, margin_mm=22,
                producer="LibreOffice 7.1" if rnd == "21" else None)


def os_join(a, b):
    import os
    return os.path.join(a, b)


GUIDE = [
    ("t", "Protected action ballots: a guide for branch officials"),
    ("s", "Local Services Union, Victoria Branch. Issued by the Branch Secretary, March 2025. Replaces the 2021 guide."),
    ("h", "1. What the Act requires"),
    ("p", "Before members can take protected industrial action in support of a proposed enterprise agreement, the "
          "Fair Work Commission must order a protected action ballot and the ballot must authorise the action. Under "
          "section 459 of the Fair Work Act 2009 the action is authorised only if at least 50 per cent of the "
          "employees on the roll of voters vote in the ballot and more than 50 per cent of the valid votes approve "
          "the action. A ballot that misses the participation requirement authorises nothing, however strong the "
          "yes vote."),
    ("p", "The branch applies for a separate order for each council, because each council has its own agreement. "
          "The ballot agent named in the order runs the ballot by post and online over the period the order sets, "
          "usually two weeks, and declares the result to the Commission and the branch."),
    ("h", "2. Deciding where to apply"),
    ("p", "An application costs the agent's fee, officials' time and, if the ballot fails, bargaining leverage that "
          "is hard to recover. The Branch Committee of Management therefore authorises an application only at a "
          "council where at least half of the members on the roll are expected to vote. The research and bargaining "
          "officer forecasts each council's expected turnout for the round and the committee resolves the list."),
    ("p", "For the forecast, the roll is every member employed at the council on the membership register extract "
          "taken for the round, and expected turnout is the share of that roll forecast to return a ballot in the "
          "round's ballot period, each member taken as they will stand when that period closes. The forecast is the expected share, not a target; a council forecast at or above "
          "50 per cent is put to the committee for an application."),
    ("h", "3. Timing for a round"),
    ("p", "Applications are lodged so that orders issue about a fortnight before the ballot opens. The committee "
          "settles the list at its last meeting before lodgement. Officials should not tell members or the employer "
          "which councils are on the list until the committee has resolved it."),
    ("h", "4. The roll"),
    ("p", "The Commission's order defines the employees to be balloted. The branch supplies the agent with the members "
          "employed at the council, drawn from the register, and the agent settles the roll with the employer. Members "
          "who have left the council's employment come off the roll; members on leave stay on it."),
    ("h", "5. After the ballot"),
    ("p", "The agent's declaration states the number of persons on the roll, the ballots returned and the votes for "
          "and against. A copy of each declaration is kept on the branch's bargaining file with the order."),
]


def guide_pdf(out):
    st = _st()
    story = []
    for kind, text in GUIDE:
        story.append(Paragraph(text, {"t": st["title"], "s": st["small"], "h": st["head"]}.get(kind, st["body"])))
    when = dt.datetime(2025, 3, 18, 11, 6, 52, tzinfo=AEDT)
    O.build(os_join(out, F_GUIDE), story, "Protected action ballots: a guide for branch officials", W.UNION,
            "Guide to protected action ballot applications and the branch's turnout forecast",
            "LSU Victoria Branch, protected action ballots guide, March 2025", when, when, margin_mm=22)


def guide_text():
    return "\n".join(t for _, t in GUIDE)


F_FINANCE = "lsu_dues_and_remittances_procedure_2025.pdf"
FINANCE = [
    ("t", "Dues and remittances: finance procedure FP-04"),
    ("s", "Local Services Union, Victoria Branch. Finance and Administration. Revised July 2025."),
    ("h", "1. Dues"),
    ("p", "Dues are set by the Branch Council each year and are payable fortnightly. For 2025-26 they are $27.40 a "
          "fortnight for full-time members, $20.60 for part-time members and $13.80 for casual members."),
    ("h", "2. How members pay"),
    ("p", "Members pay by deduction from their council pay or by direct debit from their bank account. Direct debits "
          "are collected by the branch's bank and are not covered by this procedure."),
    ("h", "3. Payroll deduction"),
    ("p", "Each council deducts dues in every fortnightly pay. Every council pays fortnightly in arrears: a pay period "
          "ends on a Sunday and is paid later that week. The council remits the deductions to the branch with a "
          "remittance advice, or its payroll provider does so on its behalf."),
    ("p", "Finance records each advice in the remittance register when it is received. Dues deducted are credited to "
          "the financial year in which the pay period ends, whatever day the advice arrives."),
    ("h", "4. Arrears"),
    ("p", "A member whose dues are more than 13 weeks in arrears becomes unfinancial under rule 9. Finance sends the "
          "organisers a monthly list of members who have fallen into arrears."),
]


def finance_pdf(out):
    st = _st()
    story = [Paragraph(text, {"t": st["title"], "s": st["small"], "h": st["head"]}.get(kind, st["body"]))
             for kind, text in FINANCE]
    when = dt.datetime(2025, 7, 9, 14, 21, 5, tzinfo=AEST)
    O.build(os_join(out, F_FINANCE), story, "Dues and remittances: finance procedure FP-04", W.UNION,
            "Finance procedure for union dues, payroll deductions and remittance advices",
            "LSU Victoria Branch, finance procedure FP-04, July 2025", when, when, margin_mm=22)


def bureau_pdf(out):
    """The bureau's monthly statements to the branch: every pay run's deductions by client council."""
    import askdata as AD
    st = _st()
    lines = AD.bureau_lines()
    story = [Paragraph(W.BUREAU, st["small"]),
             Paragraph("Union deductions remitted on behalf of client councils, 2025-26", st["title"]),
             Paragraph("Statements to %s. Each pay run is remitted to the branch as one payment; the lines below show "
                       "the deductions made for each client council in that run." % W.UNION, st["body"])]
    months = sorted({(p.year, p.month) for p, _, _, _ in lines})
    for i, (y, mth) in enumerate(months):
        rows = [r for r in lines if (r[0].year, r[0].month) == (y, mth)]
        if not rows:
            continue
        story.append(Paragraph("Statement for %s %d" % (dt.date(y, mth, 1).strftime("%B"), y), st["head"]))
        tbl = [["Pay period ending", "Client", "Members", "Deducted ($)"]]
        for p, code, n, amt in sorted(rows, key=lambda r: (r[0], W.NAME[r[1]])):
            tbl.append(["%02d/%02d/%d" % (p.day, p.month, p.year), W.NAME[code], str(n), "{:,.2f}".format(amt)])
        story.append(Table(tbl, colWidths=[90, 190, 60, 80]))
        story.append(Spacer(1, 4))
    when = dt.datetime(2026, 7, 20, 9, 12, 33, tzinfo=AEST)
    O.build(os_join(out, F_BUREAU), story, "Union deductions remitted, 2025-26", W.BUREAU,
            "Statements of union deductions by client council, July 2025 to July 2026",
            "%s, statements of union deductions" % W.BUREAU, when, when, margin_mm=20)


def write_all(out):
    pab_pdfs(out)
    guide_pdf(out)
    bureau_pdf(out)
    finance_pdf(out)
