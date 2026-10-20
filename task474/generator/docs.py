"""The pack's documents: the program rules (PDF), the data extract notes (txt), the provider group register (xlsx), the
drug class crosswalk (xlsx) and the 2025 quality scores (xlsx, a distractor)."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate        # noqa: E402
from openpyxl import Workbook                                       # noqa: E402
from openpyxl.styles import Font                                    # noqa: E402

import world as W   # noqa: E402

SECTIONS = {"groups": "2.1", "rate": "2.2", "designation": "2.3", "pharmacy": "3.1"}
BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.5, spaceAfter=6)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)


def _doc(path, title, org):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.9 * inch, bottomMargin=0.9 * inch, title=title, author=org,
                          creator=org, producer=org, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.95 * inch, 0.55 * inch, "%s  |  %s" % (org, title))
        c.drawRightString(letter[0] - 0.95 * inch, 0.55 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def write_rules(path):
    title = "Cost Performance Program 2027: Program Rules"
    d, frame = _doc(path, title, W.PLAN)
    s = [Paragraph("Cost Performance Program, 2027 Contract Year: Program Rules", TITLE),
         Paragraph("%s, %s. Approved by the Network Contracting Committee %s." % (W.PLAN, W.DEPT, W.RULES_DATE), SUB),
         Paragraph("1. Purpose", HEAD),
         Paragraph("The Cost Performance Program places primary care provider groups whose members' medical cost runs "
                   "at or above the plan's benchmark under a joint care-management plan for the 2027 contract year, "
                   "with the plan's case managers embedded in the group's clinics.", BODY),
         Paragraph("2. Designation", HEAD),
         Paragraph("2.1 <b>Groups and members.</b> Every group in the provider group register. A group's members are the "
                   "members the plan's enrollment roster assigns to it; a member stays with one group through the "
                   "period.", BODY),
         Paragraph("2.2 <b>Cost per member-month.</b> A group's 2026 cost per member-month is the paid medical cost of "
                   "the services its members received from 1 January to 30 June 2026, as paid by 31 October 2026, "
                   "divided by the member-months in which its members were covered by the plan in the same six "
                   "months.", BODY),
         Paragraph("2.3 <b>Benchmark.</b> A group whose 2026 cost per member-month is $%.2f or more is designated for "
                   "the program." % W.BENCHMARK, BODY),
         Paragraph("3. The pharmacy summary", HEAD),
         Paragraph("3.1 For the committee's formulary review, for every drug class in the drug class crosswalk: the "
                   "plan's paid pharmacy cost of the fills dated from 1 January to 30 June 2026, and the number of those "
                   "fills, as the pharmacy claims stand on 31 October 2026.", BODY),
         Paragraph("4. Timetable", HEAD),
         Paragraph("Provider Performance presents the designations to the Network Contracting Committee at the "
                   "year-end close, with the 2027 contract amendments.", BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_notes(path, n):
    lines = ["Prairie Hills Health Plan: data extract notes",
             "Extracts pulled 2026-11-02 by Provider Performance from the enterprise data warehouse.",
             "",
             "%s (%d rows)" % (W.FILES["claims"], n["claims"]),
             "  One row per paid medical claim with a first date of service from 2026-01-01 to 2026-06-30, paid",
             "  through 2026-10-31. paid_amount is the plan's paid amount in dollars. claim_type is the claim form.",
             "",
             "%s (%d rows)" % (W.FILES["roster"], n["roster"]),
             "  The plan's monthly enrollment roster, January to June 2026: one row per member per roster month,",
             "  built from the state's enrollment file as processed by the as_of date (the 5th of the month).",
             "  pcp_group_id is the primary care group the plan assigns the member to; medicaid_id is the state's",
             "  recipient id.",
             "",
             "%s (%d rows)" % (W.FILES["remit"], n["remit"]),
             "  The state's capitation remittance advices paid to the plan in 2026 for coverage months January to",
             "  June 2026: one row per remittance line, keyed on the state's medicaid_id. A line with no medicaid_id",
             "  pays a rate cell's month for the members counted in it. member_count and amount are signed.",
             "",
             "%s (%d rows)" % (W.FILES["rx"], n["rx"]),
             "  Pharmacy claim lines from the pharmacy benefit manager, processed through 2026-10-31. ndc is the",
             "  dispensed product; see %s for its class." % W.FILES["classes"],
             "",
             "%s (%d rows)" % (W.FILES["survey"], n["survey"]),
             "  Member experience survey responses, fall 2025 wave, by assigned group.",
             "",
             "Contact: Provider Performance, data warehouse team."]
    open(path, "w", encoding="utf-8", newline="\r\n").write("\n".join(lines) + "\n")


def write_groups(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Groups"
    ws.append(["Primary care provider group register, 2026"])
    ws.append(["%s, Network Contracting. As of 1 July 2026." % W.PLAN])
    ws.append([])
    ws.append(["Group ID", "Group name", "County", "Contracted PCPs", "Panel open", "Contract effective"])
    ws["A4"].font = Font(bold=True)
    rng = __import__("numpy").random.default_rng(W.SEED + 21)
    for g, (name, county, n0, *_r) in W.GROUPS.items():
        ws.append([g, name, county, int(n0 / 260 + rng.integers(1, 4)), "Yes" if rng.random() < .8 else "No",
                   "20%02d-01-01" % int(rng.integers(14, 24))])
    for col, w in zip("ABCDEF", (9, 34, 10, 16, 11, 18)):
        ws.column_dimensions[col].width = w
    wb.save(path)


def write_classes(path, ndc):
    wb = Workbook()
    ws = wb.active
    ws.title = "Crosswalk"
    ws.append(["NDC", "Drug class"])
    ws["A1"].font = Font(bold=True)
    for code, c in sorted(ndc.items()):
        ws.append([code, c])
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 26
    wb.save(path)


def write_quality(path):
    rng = __import__("numpy").random.default_rng(W.SEED + 23)
    wb = Workbook()
    ws = wb.active
    ws.title = "HEDIS 2025"
    ws.append(["HEDIS measurement year 2025: selected measures by primary care group (rates, per cent)"])
    ws.append([])
    ws.append(["Group ID", "Well-child visits (W30)", "Childhood immunization (CIS-10)", "Diabetes HbA1c control (<8)",
               "Controlling blood pressure", "Follow-up after ED visit for mental illness (7-day)"])
    for g in W.GROUPS:
        ws.append([g] + [round(float(rng.uniform(38, 82)), 1) for _ in range(5)])
    wb.save(path)
