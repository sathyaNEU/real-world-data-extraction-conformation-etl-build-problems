"""The pack's documents and workbooks: the GHSO's FY2028 task force guidelines, the census's reference manual, the
agency directory, the DOT's county miles and the motor vehicle division's licensed drivers. No document lists the
data's columns or describes its files (dataset-generation section 3)."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle  # noqa: E402

import agencies as AG   # noqa: E402
import lab as L         # noqa: E402
import truth as T       # noqa: E402
import vmt as V         # noqa: E402
import world as W       # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
pdfmetrics.registerFontFamily("LiberationSerif", normal="LiberationSerif", bold="LiberationSerif-Bold",
                              italic="LiberationSerif-Italic", boldItalic="LiberationSerif-Bold")
pdfmetrics.registerFontFamily("LiberationSans", normal="LiberationSans", bold="LiberationSans-Bold",
                              italic="LiberationSans-Italic", boldItalic="LiberationSans-Bold")
INK = colors.HexColor("#1d1f22")
GREY = colors.HexColor("#5b6067")
NAVY = colors.HexColor("#1f3a5f")
MAROON = colors.HexColor("#6b1d2a")


def styles(font="LiberationSans", accent=NAVY, size=9.6):
    bold = font + "-Bold"
    return dict(
        BODY=ParagraphStyle("body", fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=5),
        CELL=ParagraphStyle("cell", fontName=font, fontSize=7.9, leading=9.8, textColor=INK),
        CELLB=ParagraphStyle("cellb", fontName=bold, fontSize=7.9, leading=9.8, textColor=INK),
        H1=ParagraphStyle("h1", fontName=bold, fontSize=13.5, leading=17, textColor=accent, spaceAfter=2),
        H1S=ParagraphStyle("h1s", fontName=font, fontSize=8.8, leading=11.5, textColor=GREY, spaceAfter=9),
        H2=ParagraphStyle("h2", fontName=bold, fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=7,
                          spaceAfter=3))


S = styles()
SERIF = styles("LiberationSerif", MAROON, 10.2)


def _doc(path, title, footer, author):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.3)
        canvas.drawString(0.85 * inch, 0.58 * inch, footer)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.58 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                          topMargin=0.78 * inch, bottomMargin=0.88 * inch, title=title, author=author, subject="",
                          creator="", producer="")
    return d, frame


def _table(rows, widths, st=S, head="#dfe6ef"):
    data = [[Paragraph(str(v), st["CELLB"] if i == 0 else st["CELL"]) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa1a9")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 3.5)]))
    return t


def _story(title, sub, sections, st=S):
    story = [Paragraph(title, st["H1"]), Paragraph(sub, st["H1S"])]
    for head, paras in sections:
        if head:
            story.append(Paragraph(head, st["H2"]))
        for p in paras:
            story.append(p if not isinstance(p, str) else Paragraph(p, st["BODY"]))
    return story


# ------------------------------------------------------------------------------------------------ the guidelines
GUIDELINE_DATE = "9 February 2027"
COURT_CLOSE_TEXT = "28 February 2027"
SECTIONS = {"estimand": "2.2", "drivers": "2.3", "rate": "2.4", "baselines": "3.1", "testing": "4.2"}
WINDOW_DAYS = 30


def write_guidelines(path):
    d, frame = _doc(path, "FY2028 County Impaired Driving Task Force Grants: Program Guidelines",
                    "%s  |  FY2028 County Impaired Driving Task Force Grants, Program Guidelines" % W.GHSO, W.GHSO)
    secs = [
        ("1. Purpose", [
            "1.1 The FY2028 County Impaired Driving Task Force grants fund a task force in each county where impaired "
            "driving kills people at a high rate: sustained enforcement by the county's agencies together, a "
            "prosecutor and a probation officer for impaired-driving cases, a treatment court referral line and a "
            "public information campaign. Task forces run from 1 October 2027 to 30 September 2028 and are funded "
            "from the GHSO's federal impaired-driving countermeasures funds.",
            "1.2 Every high-range county (section 2) may apply. A county that is not high-range may apply for "
            "impaired-driving funds only under the GHSO's general program."]),
        ("2. High-range counties", [
            "2.1 The %s, which keeps the state's fatal crash census under its agreement with the GHSO, certifies to "
            "the GHSO by 1 May 2027 the list of high-range counties for FY2028 and each county's rate under 2.4, in a "
            "letter with a chart of the 14 counties' rates." % W.CENTER,
            "%s A county's alcohol-impaired-driving fatalities are the people who died within %d days of a crash on "
            "a public road in the county that occurred in 2023, 2024 or 2025 in which at least one driver had a blood "
            "alcohol concentration (BAC) of .08 g/dL or more, whether or not that driver was tested. Where a "
            "driver's BAC is not known, the count is the number expected from the records: each crash counts its "
            "deaths times the chance that at least one of its drivers was at .08 g/dL or more." % (
                SECTIONS["estimand"], WINDOW_DAYS),
            "%s A driver is the operator of a motor vehicle in transport, a motorcycle rider included. Passengers, "
            "pedestrians and pedalcyclists are not drivers, and a driver who left the scene and was never identified "
            "is not counted as a driver." % SECTIONS["drivers"],
            "%s A county's rate is its 2023 to 2025 alcohol-impaired-driving fatalities divided by its 2023 to 2025 "
            "vehicle miles traveled, per 100 million vehicle miles, using the %s's annual county vehicle miles. A "
            "county whose rate is %.2f or more is high-range." % (SECTIONS["rate"], W.DOT, W.THRESHOLD)]),
        ("3. Applications", [
            "%s Each application states its county's 2025 baselines, which the Center certifies with the list: the "
            "impaired-driving offenses (driving under the influence of alcohol or drugs, MSC 42-1201) committed in the "
            "county in 2025 that had been prosecuted in the county court "
            "by %s, one for each person charged and offense, and the per cent of them that had ended in a conviction "
            "for impaired driving by that date." % (SECTIONS["baselines"], COURT_CLOSE_TEXT),
            "3.2 An application names the county's lead agency, the participating agencies and the prosecutor's "
            "office, and states the task force's FY2028 targets against the 2025 baselines. Applications are due "
            "15 June 2027."]),
        ("4. Timeline", [
            _table([["Date", "Step"],
                    ["1 May 2027", "The Center certifies the FY2028 high-range counties, their rates and their 2025 "
                                   "baselines (2.1, 3.1)"],
                    ["15 June 2027", "Task force applications due"],
                    ["1 July 2027", "FY2028 Highway Safety Plan submitted"],
                    ["15 September 2027", "Awards"],
                    ["1 October 2027", "Task forces begin"]],
                   [1.35 * inch, 5.3 * inch])]),
    ]
    story = _story("FY2028 County Impaired Driving Task Force Grants: Program Guidelines",
                   "%s. Issued %s. Contact: %s, %s." % (W.GHSO, GUIDELINE_DATE, W.PEOPLE["ghso"][0],
                                                       W.PEOPLE["ghso"][1]), secs)
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the census manual
def write_manual(path):
    d, frame = _doc(path, "Fatal Crash Census Reference Manual, 2024 edition",
                    "%s  |  Fatal Crash Census Reference Manual, 2024 edition" % W.CENTER, W.CENTER)
    secs = [
        ("1. The census", [
            "1.1 The Fatal Crash Census holds every crash on a public road in the state in which a person died within "
            "30 days of the crash. The Center compiles it from the investigating agency's crash report, the coroners' "
            "and the State Medical Examiner's reports, the %s's results and death certificates." % W.LAB,
            "1.2 A year's file is closed when the 30-day window of its last crash has passed and the laboratory has "
            "reported on every specimen, and is not changed after it closes."]),
        ("2. Report forms", [
            "2.1 The census follows the crash report form: the 2011 form for crashes through 2023 and the 2024 form "
            "for crashes from 1 January 2024, which gave each agency a new agency number."]),
        ("3. Injuries and deaths", [
            "3.1 A person coded fatal died within 30 days of the crash, and the date of death is recorded. A person "
            "who died more than 30 days after the crash keeps the injury the officer reported, with the date of death "
            "recorded; that death is not a traffic fatality."]),
        ("4. Alcohol tests", [
            "4.1 A test result is the laboratory's ethanol result in g/dL to three decimals as the laboratory reports "
            "it (truncated): whole blood, or vitreous humor for some killed persons.",
            "%s Coroners and the State Medical Examiner submit blood or vitreous humor from every driver killed and "
            "from most other persons killed. The State Patrol's fatal crash procedure draws blood from every "
            "surviving driver, and the Corwin County and Ossian County sheriffs follow the same procedure. Other "
            "sheriffs' offices and police departments draw blood from a surviving driver arrested at the scene for "
            "impaired driving, with a warrant when the driver refuses. A surviving driver from whom no blood was "
            "drawn is recorded as not tested." % SECTIONS["testing"]]),
        ("Edition", [
            "2024 edition, issued 15 March 2024 with the 2024 report form, replacing the 2019 edition. Questions to "
            "%s, %s." % (W.PEOPLE["records"][0], W.PEOPLE["records"][1])]),
    ]
    story = _story("Fatal Crash Census Reference Manual", "%s. 2024 edition." % W.CENTER, secs)
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ workbooks
def _head(ws, row, fill="DCE6F1"):
    from openpyxl.styles import Font, PatternFill
    for c in ws[row]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor=fill)


def directory_rows():
    out = []
    for a in AG.AGENCIES:
        out.append([a.aid, a.old, a.name, a.kind, a.fips, W.NAMES[a.fips], a.city or ""])
    hq = W.PATROL_HQ
    out.append([AG.PATROL_ID, "9000", "State Patrol Headquarters", "State Patrol", hq, W.NAMES[hq], "Kessington"])
    for c in W.COUNTIES:
        f = c["fips"]
        if f not in L.ME_COUNTIES:
            out.append([L.CORONER_ID[f], "", "%s County Coroner" % c["name"], "Coroner", f, c["name"],
                        c["cities"][0]])
    out.append([L.ME_ID, "", "Office of the State Medical Examiner", "Medical Examiner", "013", W.NAMES["013"],
                "Kessington"])
    out.sort(key=lambda r: (r[3] != "State Patrol", r[4], r[0]))
    return out


def write_directory(path):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Agencies"
    ws.append(["agency_id", "former_code", "agency_name", "agency_type", "county_fips", "county", "city"])
    _head(ws, 1)
    for r in directory_rows():
        ws.append([None if v == "" else v for v in r])
    for col, w in zip("ABCDEFG", (11, 12, 50, 18, 11, 12, 16)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("State Patrol posts")
    ws2.append(["post", "agency_id", "post_name", "post_city", "county_fips", "county"])
    _head(ws2, 1)
    for c in W.COUNTIES:
        a = AG.patrol_post(c["fips"])
        ws2.append([a.post, a.aid, a.name, c["cities"][0], c["fips"], c["name"]])
    for col, w in zip("ABCDEF", (6, 11, 22, 16, 11, 12)):
        ws2.column_dimensions[col].width = w
    wb.save(path)


DVMT_TITLE = "%d daily vehicle miles traveled by county and functional class (thousands)"


def write_dvmt(path, tab):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    first = True
    for y in W.YEARS:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "DVMT %d" % y
        ws.append([DVMT_TITLE % y])
        ws["A1"].font = Font(name="Calibri", bold=True)
        ws.append(["County FIPS", "County"] + list(V.CLASSES) + ["All classes"])
        _head(ws, 2, fill="E2EFDA")
        for c in W.COUNTIES:
            f = c["fips"]
            vals = [tab[f][(y, cl)] for cl in V.CLASSES]
            ws.append([f, c["name"]] + vals + [round(sum(vals), 1)])
        tot = [round(sum(tab[c["fips"]][(y, cl)] for c in W.COUNTIES), 1) for cl in V.CLASSES]
        ws.append([None, "State"] + tot + [round(sum(tot), 1)])
        for row in ws.iter_rows(min_row=3, min_col=3, max_col=3 + len(V.CLASSES)):
            for cell in row:
                cell.number_format = "#,##0.0"
        for col, w in zip("ABCDEFGHIJ", (11, 12, 11, 15, 15, 13, 13, 13, 11, 12)):
            ws.column_dimensions[col].width = w
        ws.freeze_panes = "C3"
    wb.save(path)


def licensed_rows(vmt):
    out = []
    for c in W.COUNTIES:
        f = c["fips"]
        rng = T.rng_for("licensed", f)
        v25 = vmt[f] * V.YEAR_SPLIT[2025]
        total = int(round(v25 / float(rng.uniform(12400, 14600))))
        u21 = int(round(total * float(rng.uniform(0.045, 0.062) if f != "027" else 0.094)))
        o65 = int(round(total * float(rng.uniform(0.19, 0.26))))
        out.append([f, c["name"], total, u21, total - u21 - o65, o65])
    return out


def write_licensed(path, vmt):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Licensed drivers 2025"
    ws.append(["County FIPS", "County", "Licensed drivers", "Under 21", "21 to 64", "65 and over"])
    _head(ws, 1, fill="FCE4D6")
    for r in licensed_rows(vmt):
        ws.append(r)
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=6):
        for cell in row:
            cell.number_format = "#,##0"
    for col, w in zip("ABCDEF", (11, 12, 16, 11, 11, 12)):
        ws.column_dimensions[col].width = w
    wb.save(path)
