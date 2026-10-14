"""The pack's documents: the Authority's operator workstation standard, Halvard's fit report for the 2027 order, the
summary tables of the Brennard survey of working adults' body dimensions, and the readme Human Resources and Fleet
Maintenance keep with their exports."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import LETTER, landscape                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W      # noqa: E402

STANDARD = "tvrta_standard_ES-12_operator_workstation.pdf"
FIT_REPORT = "halvard_fit_report_2027_order_operator_workstation.pdf"
SURVEY = "brennard_working_adults_body_dimensions_2012_summary_tables.pdf"
NOTES_HR = "exports_readme_hr_occupational_health.md"
NOTES_FLEET = "exports_readme_fleet_maintenance.md"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Serif", "LiberationSerif-Regular"),
              ("Serif-B", "LiberationSerif-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY, RULE = colors.HexColor("#1f2329"), colors.HexColor("#5d646c"), colors.HexColor("#9aa3ad")
PAGE = LETTER

M_BODY = ParagraphStyle("mb", fontName="Serif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=5)
M_CL = ParagraphStyle("mc", parent=M_BODY, leftIndent=26, firstLineIndent=-26)
M_H1 = ParagraphStyle("mh1", fontName="Serif-B", fontSize=15, leading=19, textColor=INK, spaceAfter=3)
M_H2 = ParagraphStyle("mh2", fontName="Serif-B", fontSize=11, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
M_META = ParagraphStyle("mm", fontName="Serif", fontSize=9, leading=11.8, textColor=GREY, spaceAfter=8)
S_BODY = ParagraphStyle("sb", fontName="Sans", fontSize=9.4, leading=12.8, textColor=INK, spaceAfter=5)
S_H1 = ParagraphStyle("sh1", fontName="Sans-B", fontSize=13.5, leading=17, textColor=INK, spaceAfter=2)
S_H2 = ParagraphStyle("sh2", fontName="Sans-B", fontSize=10, leading=13, textColor=INK, spaceBefore=8, spaceAfter=3)
S_META = ParagraphStyle("sm", fontName="Sans", fontSize=8.1, leading=10.4, textColor=GREY, spaceAfter=7)
S_NOTE = ParagraphStyle("sn", fontName="Sans", fontSize=7.8, leading=10, textColor=GREY, spaceAfter=4)
S_CELL = ParagraphStyle("sc", fontName="Sans", fontSize=8.6, leading=11, textColor=INK)
S_CELLR = ParagraphStyle("scr", parent=S_CELL, alignment=2)
S_CELLB = ParagraphStyle("scb", parent=S_CELL, fontName="Sans-B")
S_CELLBR = ParagraphStyle("scbr", parent=S_CELLB, alignment=2)
T_CELL = ParagraphStyle("tc", fontName="Sans", fontSize=7.6, leading=9.4, textColor=INK, alignment=2)
T_CELLL = ParagraphStyle("tcl", parent=T_CELL, alignment=0)
T_CELLB = ParagraphStyle("tcb", parent=T_CELL, fontName="Sans-B")
T_CELLBL = ParagraphStyle("tcbl", parent=T_CELLB, alignment=0)


def _doc(path, title, author, page=PAGE, margins=(24, 24, 22, 21)):
    l, r, t, b = margins
    return SimpleDocTemplate(path, pagesize=page, leftMargin=l * mm, rightMargin=r * mm, topMargin=t * mm,
                             bottomMargin=b * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot, font="Serif", page=PAGE):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 8)
        canvas.drawString(24 * mm, page[1] - 12 * mm, top_left)
        canvas.drawRightString(page[0] - 24 * mm, page[1] - 12 * mm, top_right)
        canvas.setFont(font, 7.4)
        canvas.drawString(24 * mm, 11 * mm, foot)
        canvas.drawRightString(page[0] - 24 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _ruled(rows, widths, head_rows=1, align_top=False):
    t = Table(rows, colWidths=widths, hAlign="LEFT", repeatRows=head_rows)
    t.setStyle(TableStyle([("LINEBELOW", (0, head_rows - 1), (-1, head_rows - 1), 0.7, INK),
                           ("LINEBELOW", (0, head_rows), (-1, -1), 0.25, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP" if align_top else "BOTTOM"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


# ---------------------------------------------------------------- the Authority's standard
STANDARD_CLAUSES = [
    ("1  Scope", [
        ("1.1", "This standard applies to every bus the Authority orders. It sets how the operator workstation "
                "configuration of an order is chosen; the bus specification for the order sets the workstation's "
                "other requirements."),
    ]),
    ("2  Definitions", [
        ("2.1", "A bus operator is an employee in the Bus Operator job classification, full-time or part-time."),
        ("2.2", "The fit dimensions are popliteal height; buttock-knee length; eye height, sitting; thumb-tip reach; "
                "and abdominal extension depth, sitting. Each is the dimension of that name in the %s (%s, %d), "
                "measured as that survey measures it." % (W.SURVEY, W.INSTITUTE, W.SURVEY_YEAR)),
        ("2.3", "A configuration's fit envelope is the lowest and the highest value of each fit dimension that the "
                "configuration fits, as the manufacturer's fit report for the order states them. Where the report "
                "states no limit on one side of a dimension, the configuration has none there."),
    ]),
    ("3  Choosing the configuration", [
        ("3.1", "A configuration fits an operator when every one of the operator's five fit dimensions lies within "
                "the configuration's fit envelope."),
        ("3.2", "A configuration's accommodation is the share of the Authority's bus operators that it fits. For an "
                "order, the bus operators are those on the Authority's roster on 30 September of the year before "
                "the order's model year, whatever their duty status, each operator as measured at the operator's "
                "latest DOT physical examination on or before that date."),
        ("3.3", "For each order the Authority specifies the lowest-priced configuration in the manufacturer's fit "
                "report whose accommodation is at least 95 per cent. Price is the configuration's price per bus in "
                "the fit report."),
        ("3.4", "If no configuration in the fit report reaches 95 per cent, the Authority specifies the configuration "
                "with the highest accommodation and asks the manufacturer for a wider one before the next order."),
    ]),
    ("4  Records", [
        ("4.1", "Fleet Engineering puts each configuration's accommodation and the configuration this standard "
                "specifies to the Bus Specification Committee for approval, keeps them with the fit report in the "
                "order file, and reports them to the Board with the order."),
    ]),
]


def write_standard(path):
    title = "Engineering Standard %s: Operator Workstation" % W.STANDARD
    who, role = W.PEOPLE["coo"]
    doc = _doc(path, title, W.AUTH)
    s = [Paragraph(W.AUTH.upper(), M_META), Paragraph(title, M_H1),
         Paragraph("Revision 3, adopted 14 March 2024 by %s, %s. Replaces Revision 2 of 6 June 2016." % (who, role),
                   M_META)]
    for head, items in STANDARD_CLAUSES:
        s.append(Paragraph(head, M_H2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), M_CL))
    s += [Spacer(1, 8), Paragraph("Revision history", M_H2),
          Paragraph("Revision 1, 2 March 2009: first issue. Revision 2, 6 June 2016: the operator barrier door added "
                    "to the bus specification. Revision 3, 14 March 2024: the choice of configuration set out in "
                    "section 3.", M_META)]
    foot = "%s | %s Operator Workstation | Revision 3" % (W.AUTH, W.STANDARD)
    doc.build(s, onFirstPage=_frame("Engineering standards", "%s Rev. 3" % W.STANDARD, foot),
              onLaterPages=_frame("Engineering standards", "%s Rev. 3" % W.STANDARD, foot))


# ---------------------------------------------------------------- Halvard's fit report
OPTION_TEXT = {
    "P": "the power-adjustable pedal set, which brings the accelerator and brake pedals up to 75 mm toward the "
         "operator, so a shorter operator can sit lower and still reach the wheel and controls",
    "R": "the extended-range seat riser, which lowers the seat's lowest position and raises its highest",
    "T": "the tilt-telescope steering column, which moves the wheel up and away from the operator's abdomen and back "
         "toward a shorter operator's hands",
    "D": "the deep-travel seat track, which lets the seat run 45 mm further rearward",
    "V": "the raised header with a deeper visor, which keeps a taller operator's eye line clear of the header",
}


def lim(v, unit="mm"):
    return "no limit" if v is None else "{:,}".format(int(v))


def write_fit_report(path):
    who, role = W.PEOPLE["halvard"]
    to, trole = W.PEOPLE["fleet"]
    title = "Operator Workstation Fit Report: 2027 Order"
    doc = _doc(path, title, who)
    s = [Paragraph("%s · TRANSIT APPLICATION ENGINEERING" % W.MAKER.upper(), S_META), Paragraph(title, S_H1),
         Paragraph("For %s, %s, %s. Prepared by %s, %s. 28 August 2026. XE40 battery-electric bus, Contract 22-0417, "
                   "2027 option." % (to, trole, W.AUTH, who, role), S_META),
         Paragraph("1  Purpose", S_H2),
         Paragraph("This report gives the fit envelope and the price of each operator workstation configuration "
                   "Halvard offers for the Authority's 2027 order, in the form the Authority's standard %s asks for."
                   % W.STANDARD, S_BODY),
         Paragraph("2  The workstation and its options", S_H2),
         Paragraph("Every configuration has the XE40's standard workstation: the operator's seat on its standard riser "
                   "and track, fixed pedals, a tilt steering column and the standard header. Five options change it: "
                   + "; ".join(OPTION_TEXT[o] for o in W.OPTION_ORDER) + ".",
                   S_BODY),
         Paragraph("3  Configurations and prices", S_H2)]
    rows = [[Paragraph(h, S_CELLB if i < 2 else S_CELLBR) for i, h in enumerate(
        ["Configuration", "Options"] + ["Price per bus"])]]
    for c, opts, price in W.CONFIGS:
        rows.append([Paragraph(c, S_CELL), Paragraph("; ".join(W.OPTIONS[o] for o in opts) or "Standard workstation",
                                                     S_CELL),
                     Paragraph("${:,}".format(price), S_CELLR)])
    s += [_ruled(rows, [26 * mm, 104 * mm, 30 * mm]), Spacer(1, 4),
          Paragraph("Prices are per bus for the 2027 order, in addition to the base bus price, and hold for a "
                    "configuration confirmed by 4 December 2026.", S_NOTE),
          Paragraph("4  Fit envelopes", S_H2),
          Paragraph("Each configuration fits an operator whose five fit dimensions all lie within its limits below, in "
                    "millimetres.", S_BODY)]
    heads = ["Configuration", "Popliteal height", "Buttock-knee length", "Eye height, sitting", "Thumb-tip reach",
             "Abdominal extension depth, sitting"]
    rows = [[Paragraph(h, T_CELLBL if i == 0 else T_CELLB) for i, h in enumerate(heads)]]
    sub = [Paragraph("", T_CELL)] + [Paragraph("lower to upper", T_CELL)] * 5
    rows.append(sub)
    for c, _, _ in W.CONFIGS:
        env = W.ENVELOPES[c]
        cells = [Paragraph(c, T_CELLL)]
        for d in W.FIT_DIMS:
            lo, hi = env[d]
            cells.append(Paragraph("%s to %s" % ("no limit" if lo is None else "{:,}".format(lo),
                                                 "no limit" if hi is None else "{:,}".format(hi)), T_CELL))
        rows.append(cells)
    s += [_ruled(rows, [24 * mm, 26 * mm, 28 * mm, 27 * mm, 25 * mm, 34 * mm], head_rows=2), Spacer(1, 5),
          Paragraph("5  Basis", S_H2),
          Paragraph("The fit dimensions are those of the %s (%s, %d), measured unclothed and unshod as that survey "
                    "measures them; Halvard's seating geometry carries the allowances for shoes and clothing. The "
                    "limits come from the adjustment ranges of each configuration and Halvard's seated fit trials of "
                    "2025 on the XE40 workstation: an operator whose five dimensions all lie within a configuration's "
                    "limits can set the seat, pedals and column to drive in the posture the trials set, see the road "
                    "over the dash and the signals under the header, and reach every control."
                    % (W.SURVEY, W.INSTITUTE, W.SURVEY_YEAR), S_BODY),
          Paragraph("6  The Authority's operators", S_H2),
          Paragraph("At the Authority's request Halvard's anthropometrist measured the sitting eye height of %d bus "
                    "operators who came to open sessions at the Ridgeway division between 4 and 14 August 2026, in the "
                    "survey's posture, with their stature and weight on the day, unshod and in light clothing. The "
                    "measurements are delivered with this report as %s, one row for each operator measured."
                    % (W.TRIAL_N, "halvard_operator_measurements_2026-08.csv"), S_BODY)]
    foot = "%s | Operator workstation fit report | %s 2027 order" % (W.MAKER, W.AUTH_SHORT)
    doc.build(s, onFirstPage=_frame(W.MAKER, "XE40 2027 order", foot, "Sans"),
              onLaterPages=_frame(W.MAKER, "XE40 2027 order", foot, "Sans"))


# ---------------------------------------------------------------- the survey's summary tables
DEFS = {
    "S": "Vertical distance from the floor to the top of the head, standing erect, head in the Frankfort plane.",
    "W": "Body weight, minimal clothing.",
    "SH": "Vertical distance from the sitting surface to the top of the head, seated erect.",
    "SEH": "Vertical distance from the sitting surface to the outer corner of the eye, seated erect.",
    "SSH": "Vertical distance from the sitting surface to the acromion, seated erect.",
    "PH": "Vertical distance from the floor to the underside of the thigh just behind the knee, seated, knee at a "
          "right angle, feet flat.",
    "KH": "Vertical distance from the floor to the top of the kneecap, seated, knee at a right angle.",
    "BKL": "Horizontal distance from the rearmost point of the buttocks to the front of the kneecap, seated.",
    "BPL": "Horizontal distance from the rearmost point of the buttocks to the back of the knee, seated.",
    "TTR": "Horizontal distance from a back wall to the tip of the thumb, arm extended forward, shoulders against "
           "the wall, thumb and forefinger pinched.",
    "HB": "Maximum horizontal breadth across the hips or thighs, seated.",
    "AED": "Horizontal distance from the back of the seated subject to the most forward point of the abdomen, "
           "seated erect, relaxed.",
}
Z = {1: 2.3263, 5: 1.6449, 50: 0.0, 95: 1.6449, 99: 2.3263}


def pct(mu, sd, p):
    z = Z[p] * (-1 if p < 50 else 1)
    return mu + z * sd


def write_survey(path):
    title = "%s, %d: Summary Tables" % (W.SURVEY, W.SURVEY_YEAR)
    doc = _doc(path, title, W.INSTITUTE, margins=(20, 20, 20, 19))
    n_m, n_f = W.SAMPLE["M"], W.SAMPLE["F"]
    s = [Paragraph(W.INSTITUTE.upper(), S_META), Paragraph(title, S_H1),
         Paragraph("Report BIWD-13-04. Issued 20 May 2013.", S_META),
         Paragraph("1  The survey", S_H2),
         Paragraph("The survey measured %s men and %s women aged 18 to 64 in paid work, at fourteen employer and "
                   "community sites in eleven states between March 2011 and August 2012, by trained measurers using "
                   "the institute's instruments and landmark protocol. Estimates are weighted to the 2010 employed "
                   "population by sex, age group and region. Subjects were measured in minimal clothing and without "
                   "shoes." % ("{:,}".format(n_m), "{:,}".format(n_f)), S_BODY),
         Paragraph("2  Dimensions", S_H2)]
    rows = [[Paragraph("Dimension", S_CELLB), Paragraph("Definition", S_CELLB)]]
    for code, name, unit in W.DIMS:
        rows.append([Paragraph("%s (%s)" % (name, unit), S_CELL), Paragraph(DEFS[code], S_CELL)])
    s += [_ruled(rows, [52 * mm, 122 * mm], align_top=True), PageBreak()]
    for k, (sx, label) in enumerate((("M", "men"), ("F", "women")), 1):
        s.append(Paragraph("Table %d. Body dimensions of working %s" % (k, label), S_H2))
        heads = ["Dimension", "Mean", "SD", "1st", "5th", "50th", "95th", "99th"]
        rows = [[Paragraph(h, T_CELLBL if i == 0 else T_CELLB) for i, h in enumerate(heads)]]
        for i, (code, name, unit) in enumerate(W.DIMS):
            mu, sd = W.MEANS[sx][i], W.SDS[sx][i]
            fmt = "%.1f" if unit == "kg" else "%.0f"
            rows.append([Paragraph("%s (%s)" % (name, unit), T_CELLL), Paragraph("%.1f" % mu, T_CELL),
                         Paragraph("%.1f" % sd, T_CELL)] +
                        [Paragraph(fmt % pct(mu, sd, p), T_CELL) for p in (1, 5, 50, 95, 99)])
        s += [_ruled(rows, [60 * mm, 17 * mm, 15 * mm, 15 * mm, 15 * mm, 15 * mm, 15 * mm, 15 * mm]), Spacer(1, 3),
              Paragraph("N = %s. Percentiles are computed from the normal distribution with the mean and standard "
                        "deviation shown." % "{:,}".format(W.SAMPLE[sx]), S_NOTE), Spacer(1, 6)]
    s.append(PageBreak())
    abbrev = [c for c in W.CODES]
    for k, (sx, label) in enumerate((("M", "men"), ("F", "women")), 3):
        s.append(Paragraph("Table %d. Correlations between dimensions, working %s" % (k, label), S_H2))
        r = W.CORR[sx]
        rows = [[Paragraph("", T_CELLBL)] + [Paragraph(c, T_CELLB) for c in abbrev]]
        for i, code in enumerate(abbrev):
            cells = [Paragraph(code, T_CELLBL)]
            for j in range(len(abbrev)):
                cells.append(Paragraph("1.00" if i == j else ("%.2f" % r[i, j] if j < i else ""), T_CELL))
            rows.append(cells)
        s += [_ruled(rows, [16 * mm] + [13 * mm] * len(abbrev)), Spacer(1, 3),
              Paragraph("Pearson correlations within the sex, weighted. " + "; ".join(
                  "%s %s" % (c, n.lower()) for c, n, _ in W.DIMS) + ".", S_NOTE), Spacer(1, 8)]
    foot = "%s | %s %d | Summary tables" % (W.INSTITUTE, W.SURVEY, W.SURVEY_YEAR)
    doc.build(s, onFirstPage=_frame(W.INSTITUTE, "Report BIWD-13-04", foot, "Sans"),
              onLaterPages=_frame(W.INSTITUTE, "Report BIWD-13-04", foot, "Sans"))


# ---------------------------------------------------------------- the exports readme
NOTES_HR_TEXT = """# Exports for the 2027 operator workstation review: Human Resources and occupational health

Pulled for Fleet Engineering on 1 October 2026 ({fleet}, {fleet_role}). Human Resources and the occupational health
providers' exports are confidential: keep them on the Fleet Engineering share. Questions on the occupational health
exports to {ohc}, {ohc_role}.

## {roster}

Human Resources' roster of the employees in the Transportation and Maintenance job classes on 30 September 2026,
one row per employee. Emp No is the employee number. Job Class is the employee's classification; FT/PT whether the
position is full-time or part-time. Division is the employee's home division. Duty Status is ACTIVE, LEAVE, LIGHT
DUTY or MILITARY LEAVE.

## {ostrander}

{old}'s export of every encounter it recorded for the Authority's employees in DOT-regulated jobs from 1 January 2014
until its contract ended on 30 June 2021: DOT physical examinations, recertifications after a short certificate, and
the FTA drug and alcohol tests it collected. EMP# is the Authority's employee number. DOS is the date of service,
month/day/year. HEIGHT (feet and inches, without shoes) and WEIGHT LB (light clothing) are measured at each DOT
physical. CERT is the medical certificate issued and CERT EXPIRES its expiry.

## {fernhill}

{new}'s export of every visit it holds for the Authority's employees in DOT-regulated jobs to 30 September 2026. Fernhill
took over the contract on 1 July 2021 and loaded {old_short}'s records from 1 January 2021 into its system at the
changeover; legacy_ref carries the {old_short} encounter number of those records. employer_ref is TVT- and the
Authority's employee number. visit_type: DOTPE DOT physical examination, DOTRC recertification, UDS-RAND random drug
test, UDS-PREEMP pre-employment drug test, UDS-POSTACC post-accident drug test, BAT-RAND random breath alcohol test.
ht_in (without shoes) and wt_lb (light clothing) are measured at each DOT physical. cert_months is the certificate
issued and cert_expires its expiry.
"""


NOTES_FLEET_TEXT = """# Exports for the 2027 operator workstation review: Fleet Maintenance

Pulled for Fleet Engineering on 1 October 2026 ({fleet}, {fleet_role}) from the fleet maintenance system.

## {fleet_file}

Fleet Maintenance's roster of the buses in the fleet on 30 September 2026. accepted is the date the Authority accepted
the bus. operator_area_options lists the workstation options the bus carries: PDL power-adjustable pedal set, RSR
extended-range seat riser, TEL tilt-telescope steering column, TRK deep-travel seat track, HDR raised header and visor.

## {disposals}

The buses disposed of since 1 January 2019, with the options each carried when it left the fleet.

## {retrofits}

Fleet campaigns completed since 1 January 2019: one row per bus, the date the work was completed.

## {work_orders}

Fleet Maintenance's operator-area work orders opened from 1 January 2019 and closed by 30 September 2026, one row per
part line. component is the operator-area component worked on; the five option components are PDL-ADJ, SEAT-RSR,
STR-TEL, SEAT-TRK and HDR-VIS. bill_to is TVRTA (the Authority's operating budget), HALVARD WARRANTY or a capital
project. part_cost is qty times unit_cost. labor_hours and labor_cost are technician hours and their cost at the year's
shop rate.

## Fleet maintenance measures

Fleet Maintenance states maintenance cost per bus-year. Maintenance cost is the parts and labor on the work orders
billed to TVRTA, counted in the month the work order closed. A bus counts one bus-month for each month in which it is
in the fleet on the first day of the month, from its acceptance until it leaves the fleet; an option's bus-months are
the months in which the bus carries the option on the first day. Bus-years are bus-months divided by twelve.

## {comfort}

Kept beside the review: the May 2023 operator comfort survey (anonymous responses).

## {claims}

Kept beside the review: Risk Management's workers' compensation claims of operators, road supervisors and transportation
instructors since 1 January 2019.
"""


def write_notes(path_hr, path_fleet, names):
    kw = dict(fleet=W.PEOPLE["fleet"][0], fleet_role=W.PEOPLE["fleet"][1], ohc=W.PEOPLE["ohc"][0],
              ohc_role=W.PEOPLE["ohc"][1], old=W.OLD, new=W.NEW, old_short=W.OLD.split()[0], **names)
    open(path_hr, "w").write(NOTES_HR_TEXT.format(**{k: v for k, v in kw.items()}))
    open(path_fleet, "w").write(NOTES_FLEET_TEXT.format(**kw))
