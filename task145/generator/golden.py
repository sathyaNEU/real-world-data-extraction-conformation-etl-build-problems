"""task145 architecture 2: the golden deliverables (the board paper with its chart, the attendance workbook) and
figures.json, every number from analysis.py run on target/."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import analysis as A  # noqa: E402
import params as P  # noqa: E402

MONTH_NAME = {8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
SPRING = {"2023-24": "Spring 2024", "2024-25": "Spring 2025", "2025-26": "Spring 2026"}


def figures(target):
    S = A.solve(target)
    a = A.ask_a(target, S)
    b = A.ask_b(target, S)
    num, den = S["num"], S["den"]

    def rate(runs):
        n = sum(v for (r, f), v in num.items() if r == runs)
        d = sum(v for (r, f), v in den.items() if r == runs)
        return 100.0 * n / d
    seats = dict((t, s) for t, s, _ in P.TIERS)
    price = dict((t, p) for t, _, p in P.TIERS)
    fig = dict(
        call=dict(tier=S["tier"], seats=seats[S["tier"]], price=price[S["tier"]], expected=round(S["expected"])),
        expected_unrounded=S["expected"],
        on_roll=len(S["cur"]), with_run=S["with_run"],
        hist_leavers=S["hist_leavers"], hist_with_run=S["hist_with_run"],
        hist_on_roll={y: sum(1 for (lab, k) in S["out"] if lab == y) for y in P.HIST},
        rate_no_run=round(rate(0), 1), rate_one_run=round(rate(1), 1), rate_two_runs=round(rate(2), 1),
        chronic_fall={y: round(A.chronic_network(target, S, y), 1) for y in ("2025-26", P.CUR)},
        ask_a={"%s %d" % k: round(v[0], 1) for k, v in a.items()},
        ask_a_counts={"%s %d" % k: [v[1], v[2]] for k, v in a.items()},
        ask_b={"%s %s" % (k[0], MONTH_NAME[k[1][1]]): v for k, v in b.items()},
    )
    return fig, S


def chart(fig, path):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    f, ax = plt.subplots(figsize=(6.4, 2.9), dpi=150)
    names = [t for t, _, _ in P.TIERS]
    seats = [s for _, s, _ in P.TIERS]
    cols = ["#B8C4D6" if t != fig["call"]["tier"] else "#2F5F98" for t in names]
    ax.barh(names, seats, color=cols, height=0.55)
    for i, s in enumerate(seats):
        ax.text(s + 3, i, "%d seats" % s, va="center", fontsize=8.5, color="#333333")
    e = fig["call"]["expected"]
    ax.axvline(e, color="#B23A2E", lw=1.6)
    ax.text(e + 3, 2.38, "expected leavers, spring 2027: %d" % e, color="#B23A2E", fontsize=8.5)
    ax.set_xlim(0, 300)
    ax.invert_yaxis()
    ax.set_xlabel("Students")
    ax.set_title("Pathwise Schedule B tiers against the students expected to leave", fontsize=9.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    f.tight_layout()
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


def board_paper(fig, path, png):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=14, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14,
                        spaceBefore=8, spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=8.4, leading=11, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=9, leading=11)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.8 * inch, title="Bridge seats for spring 2027",
                            author="Data and Assessment", creator="Data and Assessment", invariant=1)
    c = fig["call"]
    cf = fig["chronic_fall"]
    t = Table([[Paragraph(x, cell) for x in ("Spring", "On roll in January", "With a run in the fall",
                                              "Left by 30 June")]] +
              [[Paragraph(SPRING[y], cell), Paragraph("{:,}".format(fig["hist_on_roll"][y]), cell),
                Paragraph(str(fig["hist_with_run"][y]), cell), Paragraph(str(fig["hist_leavers"][y]), cell)]
               for y in P.HIST],
              colWidths=[1.3 * inch, 1.5 * inch, 1.7 * inch, 1.3 * inch])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8D98A7")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EBF1"))]))
    s = [Paragraph("%s, Board of Directors, 29 December 2026, item 6" % P.ORG, small),
         Paragraph("Bridge seats for spring 2027", h1), Spacer(1, 4),
         Paragraph("<b>Recommendation.</b> Fund %s of the Pathwise schedule: %d seats for USD %s. We expect about %d "
                   "of the %s students on roll for 5 January 2027 to leave the network without completing by 30 June, "
                   "more than Tier 1's %d seats." % (c["tier"], c["seats"], "{:,}".format(c["price"]), c["expected"],
                                                    "{:,}".format(fig["on_roll"]), P.TIERS[0][1]), body),
         Paragraph("Why", h2),
         Paragraph("In each of the last three springs the students who left were above all those who had been away for "
                   "a week or more at a stretch in the fall. Of the students with one unbroken run of five or more "
                   "instructional days missed, %.1f per cent left in the spring, and %.1f per cent of those with two or "
                   "more; of the students with no such run, %.1f per cent. Absences of three or four days in a row "
                   "carried little more risk than scattered days." % (fig["rate_one_run"], fig["rate_two_runs"],
                                                                 fig["rate_no_run"]), body),
         Paragraph("This fall the family texts cut the scattered absences, and the fall chronic absence rate fell from "
                   "%.1f per cent a year ago to %.1f per cent. The week-long absences went the other way: %d of the "
                   "students on roll had at least one run this fall, against %d in fall 2025. Pricing each student at "
                   "the spring leaving rate of students with the same runs and course failures over the last three "
                   "years gives %d expected leavers." % (cf["2025-26"], cf[P.CUR], fig["with_run"],
                                                         fig["hist_with_run"]["2025-26"], c["expected"]), body),
         Spacer(1, 4), Image(png, width=6.3 * inch, height=2.85 * inch), Spacer(1, 6), t,
         Paragraph("Basis", h2),
         Paragraph("Leaving as Policy JF-7 section 3 defines it, each transfer checked against the registrar's records "
                   "requests. Days missed as Regulation JH-R section 1 defines them, on each school's own instructional "
                   "calendar; a student who moved between our schools is read on the school they attended each day. "
                   "The attendance workbook in this packet carries the fall's chronic absence rates and suspension "
                   "days by school.", small)]
    doc.build(s)


def workbook(fig, path):
    thin = Side(style="thin", color="A6AEB9")
    head_fill = PatternFill("solid", fgColor="E6EBF1")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Chronic absence"
    ws.append(["Fall 2026 chronic absence by school and grade"])
    ws.append(["12 August to 18 December 2026. Students enrolled ten or more instructional days at the school; "
               "chronically absent on 10 per cent or more of them (JH-R 2026-27, sections 1 to 3)."])
    ws.append([])
    ws.append(["Rate (per cent)"] + ["Grade %d" % g for g in P.GRADES])
    for s in P.SCHOOLS:
        ws.append([P.SCHOOL_NAME[s]] + [fig["ask_a"]["%s %d" % (s, g)] for g in P.GRADES])
    ws.append([])
    ws.append(["Chronically absent / students"] + ["Grade %d" % g for g in P.GRADES])
    for s in P.SCHOOLS:
        ws.append([P.SCHOOL_NAME[s]] + ["%d / %d" % tuple(fig["ask_a_counts"]["%s %d" % (s, g)]) for g in P.GRADES])
    for row in ws.iter_rows(min_row=5, max_row=4 + len(P.SCHOOLS), min_col=2, max_col=5):
        for c in row:
            c.number_format = "0.0"
    ws2 = wb.create_sheet("Suspension days")
    ws2.append(["Fall 2026 out-of-school suspension days served, by school and month"])
    ws2.append(["Instructional days a student spent on out-of-school suspension while enrolled at the school, as "
                "each suspension stood after any hearing."])
    ws2.append([])
    months = [MONTH_NAME[m] for m in (8, 9, 10, 11, 12)]
    ws2.append(["School"] + months + ["Fall"])
    for s in P.SCHOOLS:
        vals = [fig["ask_b"]["%s %s" % (s, m)] for m in months]
        ws2.append([P.SCHOOL_NAME[s]] + vals + [sum(vals)])
    tot = [sum(fig["ask_b"]["%s %s" % (s, m)] for s in P.SCHOOLS) for m in months]
    ws2.append(["Network"] + tot + [sum(tot)])
    for w, hdr_rows in ((ws, (4, 10)), (ws2, (4,))):
        w.column_dimensions["A"].width = 34
        for col in "BCDEFG":
            w.column_dimensions[col].width = 13
        w["A1"].font = Font(bold=True, size=12)
        w["A2"].font = Font(italic=True, size=9, color="555555")
        for hr in hdr_rows:
            for c in w[hr]:
                if c.value is not None:
                    c.font = Font(bold=True)
                    c.fill = head_fill
                    c.alignment = Alignment(horizontal="center")
                    c.border = Border(bottom=thin)
    for c in ws2[ws2.max_row]:
        c.font = Font(bold=True)
        c.border = Border(top=thin)
    wb.save(path)


def write_all(target, golden, figpath):
    os.makedirs(golden, exist_ok=True)
    fig, S = figures(target)
    png = os.path.join(golden, "_chart.png")
    chart(fig, png)
    board_paper(fig, os.path.join(golden, "bridge_2027_board_paper.pdf"), png)
    os.remove(png)
    workbook(fig, os.path.join(golden, "attendance_figures_2026.xlsx"))
    with open(figpath, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return fig, S
