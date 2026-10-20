"""task474's documents and workbooks: the State Data Center's four December releases of its poverty estimates (PDF),
its 2024 workbook and methods note, the Bureau's table notes for the 2020-2024 extract, the Office of Budget and
Policy's FY2027 allocation rule, the Fund's FY2026 allocation table and closeout workbook, and the grants data
system's export layout."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A        # noqa: E402
import sources as S     # noqa: E402
import world as W       # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic"),
              ("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d20")
GREY = colors.HexColor("#5b6067")
SDC_BLUE = colors.HexColor("#1f4e79")
OBP_RED = colors.HexColor("#7a2630")


def styles(font, accent, size=9.6):
    bold = font + "-Bold"
    return dict(
        BODY=ParagraphStyle("body", fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=6),
        SMALL=ParagraphStyle("small", fontName=font, fontSize=8, leading=10.4, textColor=GREY, spaceAfter=4),
        CELL=ParagraphStyle("cell", fontName=font, fontSize=8.3, leading=10.2, textColor=INK),
        CELLR=ParagraphStyle("cellr", fontName=font, fontSize=8.3, leading=10.2, textColor=INK, alignment=2),
        CELLB=ParagraphStyle("cellb", fontName=bold, fontSize=8.3, leading=10.2, textColor=INK),
        CELLBR=ParagraphStyle("cellbr", fontName=bold, fontSize=8.3, leading=10.2, textColor=INK, alignment=2),
        H1=ParagraphStyle("h1", fontName=bold, fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        H1S=ParagraphStyle("h1s", fontName=font, fontSize=9, leading=12, textColor=GREY, spaceAfter=10),
        H2=ParagraphStyle("h2", fontName=bold, fontSize=10.5, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3))


SDC_ST = styles("LiberationSans", SDC_BLUE)
OBP_ST = styles("LiberationSerif", OBP_RED, size=10.2)


def fmt(n):
    return "{:,}".format(int(n))


def _doc(path, title, footer, author, st):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(st["BODY"].fontName, 7.5)
        canvas.drawString(0.9 * inch, 0.6 * inch, footer)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, st, head="#dfe7f0", right_from=2, bold_last=False):
    data = []
    for i, r in enumerate(rows):
        line = []
        for j, v in enumerate(r):
            last = bold_last and i == len(rows) - 1
            if i == 0 or last:
                s = st["CELLBR"] if (j >= right_from and i > 0) else st["CELLB"]
            else:
                s = st["CELLR"] if j >= right_from else st["CELL"]
            line.append(Paragraph(str(v), s))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa3ad")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def _build(d, frame, title, sub, sections, st):
    story = [Paragraph(title, st["H1"]), Paragraph(sub, st["H1S"])]
    for head, paras in sections:
        if head:
            story.append(Paragraph(head, st["H2"]))
        for p in paras:
            story.append(p if not isinstance(p, str) else Paragraph(p, st["BODY"]))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the SDC's releases
def universe(kind, area, y):
    """The population for whom poverty status is determined, by area and year (the household population less the
    groups the poverty universe leaves out)."""
    key = "county" if kind == "county" else "region"
    return int(round(sum(t["popy"][y] for t in W.TOWNS if t[key] == area) * 0.9768))


def _areas(kind):
    return [(W.county_code(n), n) for n in W.COUNTY_NAMES] if kind == "county" else list(W.REGIONS)


def _first_table(kind, y, st):
    head = ["FIPS" if kind == "county" else "Code", "County" if kind == "county" else "Planning region",
            "Residents in poverty", "90% CI lower", "90% CI upper", "Percent in poverty"]
    rows = [head]
    tot = lo = hi = uni = 0
    for code, name in _areas(kind):
        e = S.SDC_EST[(kind, name, y)]
        u = universe(kind, name, y)
        rows.append([W.STATE_FIPS + code, name, fmt(e["first"]), fmt(e["lo1"]), fmt(e["hi1"]),
                     "%.1f" % (100.0 * e["first"] / u)])
        tot += e["first"]
        uni += u
    rows.append([W.STATE_FIPS, "State", fmt(tot), "", "", "%.1f" % (100.0 * tot / uni)])
    return _table(rows, [0.6 * inch, 1.55 * inch, 1.15 * inch, 0.95 * inch, 0.95 * inch, 1.0 * inch], st,
                  bold_last=True)


def _revised_table(kind, y, first_label, st):
    head = ["FIPS" if kind == "county" else "Code", "County" if kind == "county" else "Planning region",
            "Revised estimate", "90% CI lower", "90% CI upper", "First estimate (%s)" % first_label, "Revision"]
    rows = [head]
    tr = tf = 0
    for code, name in _areas(kind):
        e = S.SDC_EST[(kind, name, y)]
        rows.append([W.STATE_FIPS + code, name, fmt(e["revised"]), fmt(e["lo"]), fmt(e["hi"]), fmt(e["first"]),
                     "%+d" % (e["revised"] - e["first"])])
        tr += e["revised"]
        tf += e["first"]
    rows.append([W.STATE_FIPS, "State", fmt(tr), "", "", fmt(tf), "%+d" % (tr - tf)])
    return _table(rows, [0.55 * inch, 1.4 * inch, 1.0 * inch, 0.85 * inch, 0.85 * inch, 1.15 * inch, 0.7 * inch], st,
                  bold_last=True)


RELEASES = {   # key: (year first published, previous year revised, release date, kind of the new year, kind revised)
    "rel2021": (2020, 2019, dt.date(2021, 12, 9), "county", "county"),
    "rel2022": (2021, 2020, dt.date(2022, 12, 8), "county", "county"),
    "rel2023": (2022, 2021, dt.date(2023, 12, 7), "county", "county"),
    "rel2024": (2023, 2022, dt.date(2024, 12, 12), "region", "county"),
}


def _long(d):
    return "%s %d, %d" % (d.strftime("%B"), d.day, d.year)


def write_release(path, key):
    y, yr, day, kind, kind_r = RELEASES[key]
    st = SDC_ST
    prev_day = {2019: "December 2020", 2020: "December 2021", 2021: "December 2022", 2022: "December 2023"}[yr]
    if kind == "county":
        title = "Residents in Poverty, %d" % y
        sub = "County estimates | %s | Released %s" % (W.SDC, _long(day))
        intro = ("This release gives the %s's first estimates of the number of residents in poverty in %d for the "
                 "State and its eight counties, and revised estimates for %d, which replace the first estimates "
                 "released in %s. The estimates are model-based; the %s's methods note describes how they are made. "
                 "Contact: %s, Demographer." % (W.SDC, y, yr, prev_day, W.SDC, W.PEOPLE["demographer"]))
        extra = []
        if y == 2022:
            extra = [("The move to planning regions", [
                "These are the last first estimates for the counties. Under the 2022 statute the nine planning "
                "regions become the State's county-equivalents, and beginning with the 2023 estimates, due in December "
                "2024, the %s will publish its estimates for the planning regions. The 2022 county estimates will be "
                "revised once, in that release." % W.SDC])]
        t1 = "Table 1. Residents in poverty, %d, first estimates, counties" % y
        t2 = "Table 2. Residents in poverty, %d, revised estimates, counties" % yr
    else:
        title = "Residents in Poverty, %d" % y
        sub = "First estimates for the planning regions | %s | Released %s" % (W.SDC, _long(day))
        intro = ("This release gives the %s's first estimates of the number of residents in poverty in %d, the first "
                 "for the nine planning regions, and revised estimates for %d, the last for the eight former "
                 "counties. The estimates are model-based; the %s's methods note describes how they are made. "
                 "Contact: %s, Demographer." % (W.SDC, y, yr, W.SDC, W.PEOPLE["demographer"]))
        extra = [("The change to planning regions", [
            "Under the 2022 statute the nine planning regions, each a group of whole towns, replaced the eight "
            "counties as the State's county-equivalents, and the %s now publishes its estimates for them. The planning "
            "regions do not follow the former county lines: the towns of several former counties lie in two or three "
            "regions. The %s does not produce planning region estimates for years before 2023, or former county "
            "estimates for years after 2022." % (W.SDC, W.SDC)])]
        t1 = "Table 1. Residents in poverty, %d, first estimates, planning regions" % y
        t2 = "Table 2. Residents in poverty, %d, revised estimates, former counties" % yr
    d, frame = _doc(path, title, "%s  |  %s" % (W.SDC, title), W.SDC, st)
    secs = [(None, [intro])] + extra + [
        (t1, [_first_table(kind, y, st), Spacer(1, 4),
              Paragraph("Percent in poverty: residents in poverty over the population for whom poverty status is "
                        "determined. The State figure is the sum of the areas.", st["SMALL"])]),
        (t2, [_revised_table(kind_r, yr, prev_day, st), Spacer(1, 4),
              Paragraph("Revision: the revised estimate less the first estimate.", st["SMALL"])])]
    _build(d, frame, title, sub, secs, st)


def write_release_2024(path):
    """The December 2025 release: 2024 first estimates and 2023 revised, planning regions, as a workbook."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Table 1"
    bold = Font(bold=True)
    ws.append(["Residents in poverty, 2024, first estimates, planning regions"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["%s, released December 11, 2025" % W.SDC])
    ws.append([])
    ws.append(["Code", "Planning region", "Residents in poverty", "90% CI lower", "90% CI upper", "Percent in poverty"])
    for c in ws[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True)
    tot = uni = 0
    for code, name in W.REGIONS:
        e = S.SDC_EST[("region", name, 2024)]
        u = universe("region", name, 2024)
        ws.append([W.STATE_FIPS + code, name, e["first"], e["lo1"], e["hi1"], round(100.0 * e["first"] / u, 1)])
        tot += e["first"]
        uni += u
    ws.append([W.STATE_FIPS, "State", tot, None, None, round(100.0 * tot / uni, 1)])
    for c in ws[ws.max_row]:
        c.font = bold
    for col, wd in zip("ABCDEF", (8, 22, 14, 12, 12, 12)):
        ws.column_dimensions[col].width = wd
    for r in ws.iter_rows(min_row=5, max_row=ws.max_row, min_col=3, max_col=5):
        for c in r:
            c.number_format = "#,##0"
    ws2 = wb.create_sheet("Table 2")
    ws2.append(["Residents in poverty, 2023, revised estimates, planning regions"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append(["%s, released December 11, 2025; the first estimates were released December 12, 2024" % W.SDC])
    ws2.append([])
    ws2.append(["Code", "Planning region", "Revised estimate", "90% CI lower", "90% CI upper",
                "First estimate (December 2024)", "Revision"])
    for c in ws2[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True)
    tr = tf = 0
    for code, name in W.REGIONS:
        e = S.SDC_EST[("region", name, 2023)]
        ws2.append([W.STATE_FIPS + code, name, e["revised"], e["lo"], e["hi"], e["first"], e["revised"] - e["first"]])
        tr += e["revised"]
        tf += e["first"]
    ws2.append([W.STATE_FIPS, "State", tr, None, None, tf, tr - tf])
    for c in ws2[ws2.max_row]:
        c.font = bold
    for col, wd in zip("ABCDEFG", (8, 22, 14, 12, 12, 16, 10)):
        ws2.column_dimensions[col].width = wd
    for r in ws2.iter_rows(min_row=5, max_row=ws2.max_row, min_col=3, max_col=7):
        for c in r:
            c.number_format = "#,##0"
    ws3 = wb.create_sheet("Notes")
    for line in [
        "Residents in poverty, 2024: first estimates for the planning regions, with revised estimates for 2023",
        "%s. Released December 11, 2025." % W.SDC,
        "",
        "The estimates are model-based. The methods note (November 2024) describes how they are made.",
        "Table 1 gives the first estimates for 2024. They will be revised once, in December 2026.",
        "Table 2 gives the revised estimates for 2023, which replace the first estimates released December 12, 2024.",
        "Percent in poverty: residents in poverty over the population for whom poverty status is determined.",
        "The State figure is the sum of the planning regions.",
        "Contact: %s, Demographer." % W.PEOPLE["demographer"]]:
        ws3.append([line] if line else [])
    ws3.column_dimensions["A"].width = 110
    wb.save(path)


def write_methods(path):
    st = SDC_ST
    d, frame = _doc(path, "Model-based estimates of residents in poverty: methods note",
                    "%s  |  Methods note, November 2024" % W.SDC, W.SDC, st)
    secs = [
        ("1. What is estimated", [
            "Each year the %s estimates the number of residents in poverty in the State and in each of its "
            "county-equivalents. An estimate for a year counts the residents in poverty in that calendar year: the "
            "residents whose family income over the calendar year was below the federal poverty threshold for a "
            "family of their size and composition." % W.SDC,
            "The population covered is the population for whom poverty status is determined: every resident except "
            "people living in institutions, military group quarters and college dormitories, and unrelated children "
            "under 15."]),
        ("2. Method", [
            "The estimates are predictions from an area-level model fitted each year. The model combines the American "
            "Community Survey's single-year estimates for the areas large enough to have them with the number of State "
            "income tax returns filed, the number with income below the poverty threshold, and the %s's population "
            "estimates. Each area's estimate is the model's prediction for the area, and the areas' predictions are "
            "controlled so that they sum to the State's." % W.SDC]),
        ("3. Releases and revisions", [
            "The first estimates for a year are released in December of the following year. A year later, with the "
            "next year's first estimates, the %s releases revised estimates for the year, from the model refitted "
            "with that year's final tax return counts; the revised estimate replaces the first. No estimate is "
            "revised more than once." % W.SDC]),
        ("4. Geography", [
            "The %s published estimates for the State's eight counties through the 2022 estimates. Under the 2022 "
            "statute the nine planning regions became the State's county-equivalents, and from the 2023 estimates "
            "the %s publishes for the planning regions. Each planning region is a group of whole towns. The %s does "
            "not publish estimates for towns." % (W.SDC, W.SDC, W.SDC)]),
        ("5. Uncertainty", [
            "Each estimate is published with a 90 per cent confidence interval from the model's prediction error. "
            "Estimates are shown to the person; they are not precise to that level."]),
        ("Contacts", ["%s, Director. %s, Demographer." % (W.PEOPLE["director"], W.PEOPLE["demographer"])])]
    _build(d, frame, "Model-based estimates of residents in poverty", "Methods note | %s | November 2024" % W.SDC,
           secs, st)


ACS_NOTES = """Table B17001: Poverty Status in the Past 12 Months by Sex by Age
Universe: Population for whom poverty status is determined
2020-2024 American Community Survey 5-Year Estimates

Source: U.S. Census Bureau, 2020-2024 American Community Survey 5-Year Estimates, released December 11, 2025.
Extract: pulled from the Census Bureau's data API by the State Data Center on January 8, 2026 for the State, its nine
planning regions and its towns; one row per geography and table line, the estimate and its margin of error side by side.

Table notes

Although the American Community Survey (ACS) produces population, demographic and housing unit estimates, the decennial
census is the official source of population totals for apportionment and redistricting purposes.

Data are based on a sample and are subject to sampling variability. The degree of uncertainty for an estimate arising
from sampling variability is represented through the use of a margin of error. The value shown here is the 90 percent
margin of error. The margin of error can be interpreted roughly as providing a 90 percent probability that the interval
defined by the estimate minus the margin of error and the estimate plus the margin of error (the lower and upper
confidence bounds) contains the true value. In addition to sampling variability, the ACS estimates are subject to
nonsampling error. The effect of nonsampling error is not represented in these tables.

The 5-year estimates are period estimates: they describe the average characteristics of the population over the 60
months in which the data were collected, January 1, 2020 to December 31, 2024.

Poverty status is determined for all people except institutionalized people, people in military group quarters, people
in college dormitories, and unrelated individuals under 15 years old. These groups are excluded from the numerator and
denominator when calculating poverty rates.

The poverty thresholds are updated every year to account for changes in the cost of living, using the Consumer Price
Index. A family's income over the 12 months before the interview is compared with the threshold for its size and
composition.

In 2022 the State's nine planning regions replaced its eight counties as county-equivalents in the Census Bureau's
geography. These tables show the planning regions (summary level 050) and the towns, which are county subdivisions
(summary level 060), under the planning region codes. Town codes are unchanged; a town's GEO_ID carries its planning
region's code in place of its former county's.

Estimates of urban and rural populations, housing units, and characteristics reflect boundaries of urban areas defined
based on 2020 Census data.
"""


def write_acs_notes(path):
    open(path, "w", encoding="utf-8", newline="\n").write(ACS_NOTES)


# ---------------------------------------------------------------------------------------------- the OBP
def write_rule(path):
    st = OBP_ST
    d, frame = _doc(path, "Regional Opportunity Fund: FY2027 allocation rule",
                    "%s  |  Regional Opportunity Fund, FY2027 allocation rule" % W.OBP, W.OBP, st)
    secs = [
        (None, ["Issued September 15, 2026, under the Fund's enabling act. This rule sets how the FY2027 "
                "appropriation is allocated among the regional councils of governments and how the former county "
                "community action agencies' FY2026 balances and caseloads pass to the councils."]),
        ("1. The Fund", [
            "1.1 The Regional Opportunity Fund's FY2027 appropriation, $12,000,000, is allocated among the nine "
            "regional councils of governments, one for each planning region, in proportion to each region's average "
            "residents in poverty over 2020 to 2024, the five latest years the %s has estimated." % W.SDC,
            "1.2 Each council receives its allocation as one award for July 1, 2026 to June 30, 2027."]),
        ("2. Residents in poverty", [
            "2.1 A region's residents in poverty in a year are the %s's estimate of the residents in poverty of the "
            "region for that year, as last published." % W.SDC,
            "2.2 For 2020, 2021 and 2022, years the %s estimated only for the eight former counties, a region's "
            "residents in poverty are its part of the former counties' estimates for the year: each former county's "
            "estimate is divided among the former county's towns in proportion to each town's residents in poverty "
            "in that year, and the region's figure is the sum of the parts of its towns." % W.SDC,
            "2.3 A region's average is the mean of its residents in poverty in 2020, 2021, 2022, 2023 and 2024, each "
            "year with equal weight.",
            "2.4 A council's allocation is $12,000,000 times its region's average over the sum of the nine regions' "
            "averages, computed from the unrounded averages. Allocations are published rounded to the nearest "
            "$10,000."]),
        ("3. Transition from the former county agencies", [
            "3.1 Each former county community action agency's FY2026 Fund award unexpended at June 30, 2026, as "
            "reported in its closeout, passes to the councils, in addition to their FY2027 allocations, in "
            "proportion to the number of people the agency served in FY2026 (July 1, 2025 to June 30, 2026) while "
            "they lived in each council's region. A person the agency served while living in two regions is counted "
            "once in each.",
            "3.2 Each council takes over the energy assistance caseload of its region's towns. A council's FY2027 "
            "energy assistance plan starts from the energy assistance the former county agencies paid in FY2026 to "
            "households living in the region's towns when they were paid."]),
        ("4. Schedule", [
            "4.1 The %s prepares the allocation for the %s by October 23, 2026. Awards are issued by November 13, "
            "2026." % (W.SDC, W.OBP),
            "4.2 Questions: %s, Grants Manager, %s." % (W.PEOPLE["grants"], W.OBP)])]
    _build(d, frame, "Regional Opportunity Fund: FY2027 allocation rule", "%s | Issued September 15, 2026" % W.OBP,
           secs, st)


def write_fy2026(path):
    """The OBP's FY2026 allocation among the county agencies (the prior cycle's table)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    b = A.fy2026_basis()
    tot = sum(b.values())
    wb = Workbook()
    ws = wb.active
    ws.title = "FY2026 allocation"
    ws.append(["Regional Opportunity Fund, FY2026 allocation"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([W.OBP + ", September 12, 2025"])
    ws.append([])
    ws.append(["Agency", "County", "Average residents in poverty, 2018-2022", "Share", "FY2026 award ($)"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for cty in W.COUNTY_NAMES:
        ws.append([W.AGENCY[cty], cty, round(b[cty]), round(b[cty] / tot, 4), A.AWARD[cty]])
    ws.append(["Total", None, round(tot), 1.0, sum(A.AWARD.values())])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for r in ws.iter_rows(min_row=5, max_row=ws.max_row):
        r[2].number_format = "#,##0"
        r[3].number_format = "0.0%"
        r[4].number_format = "#,##0"
    for col, wd in zip("ABCDE", (40, 12, 18, 9, 16)):
        ws.column_dimensions[col].width = wd
    ws2 = wb.create_sheet("Notes")
    for line in [
        "Regional Opportunity Fund, FY2026 allocation among the county community action agencies ($10,800,000).",
        "Basis: each county's average residents in poverty, 2018 to 2022, %s estimates as last published "
        "(December 2024)." % W.SDC,
        "Awards are in proportion to the basis, to the nearest $1,000; the remainder goes to the largest fractions.",
        "Award period July 1, 2025 to June 30, 2026.",
        "Prepared by %s, Grants Manager." % W.PEOPLE["grants"]]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 110
    wb.save(path)


def write_closeout(path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    r = W.rng("closeout")
    wb = Workbook()
    ws = wb.active
    ws.title = "FY2026 closeout"
    ws.append(["Regional Opportunity Fund, FY2026 grant closeout"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([W.OBP + ", as of October 2, 2026"])
    ws.append([])
    ws.append(["Grant no.", "Agency", "County", "Award ($000)", "Expended to June 30, 2026 ($)", "Unexpended ($)",
               "Closeout received", "Status"])
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    for i, cty in enumerate(W.COUNTY_NAMES):
        b = A.BALANCES[cty]
        got = dt.date(2026, 8, 17) + dt.timedelta(days=int(r.integers(0, 38)))
        ws.append(["ROF-26-%03d" % (i + 1), W.AGENCY[cty], cty, b["award"] / 1000.0, b["spent"], b["unspent"],
                   got, "Accepted"])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[3].number_format = "#,##0"
        row[4].number_format = "#,##0"
        row[5].number_format = "#,##0"
        row[6].number_format = "mm/dd/yyyy"
    for col, wd in zip("ABCDEFGH", (12, 40, 12, 12, 18, 14, 14, 10)):
        ws.column_dimensions[col].width = wd
    ws2 = wb.create_sheet("Notes")
    for line in [
        "FY2026 grants ran July 1, 2025 to June 30, 2026.",
        "Expended: the allowable costs the agency reported through June 30, 2026, as accepted at closeout.",
        "Unexpended: the award less the amount expended.",
        "Prepared by %s, Grants Manager." % W.PEOPLE["grants"]]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 100
    wb.save(path)


LAYOUT = """Regional Opportunity Fund grants data system: export layouts
Version 3, March 10, 2026

Client services extract (rof_client_services_extract_YYYYMMDD.csv)
One row per service recorded for a client record, for the services entered from July 1, 2025 to the extract date.
  agency_code     the agency that delivered the service
                  HCCAA Halden County Community Action Agency; CCA Corbin Community Action; WOC Wexmoor Opportunity
                  Council; AGCS Ashgrove Community Services; LCAP Ludbury County Action Partnership; MCA Merrick
                  Community Action; SACA Stanbridge Area Community Action; PCAC Pennock County Action Council
  client_no       the client record the service was recorded under
  household_no    the household of the client record
  service_code    FD food pantry; RA rent or utility arrears; CM case management; TX tax preparation;
                  EM employment services; NS nutrition assistance outreach; EA energy assistance
  service_date    the date the service was delivered
  entered_on      the date the service was entered
  town            town of residence
  amount_usd      the payment, for RA and EA services; blank for the others

Profile audit trail (rof_gds_profile_audit_fyYYYY.csv)
One row per change to a field of a client record, for the changes entered from July 1, 2025 to the extract date.
  agency_code     as above
  client_no       the client record changed
  field           the field changed (town, street_address, phone, email, preferred_language, household_size,
                  income_source)
  old_value       the value before the change; (redacted) for contact details
  new_value       the value after the change; (redacted) for contact details
  effective_date  the date the change took effect, for the fields that carry one (town, street_address,
                  household_size, income_source)
  changed_on      the date the change was entered
  changed_by      the user who entered it

Dates are YYYY-MM-DD. Files are UTF-8, comma-separated, with a header row.
"""


def write_layout(path):
    open(path, "w", encoding="utf-8", newline="\n").write(LAYOUT)
