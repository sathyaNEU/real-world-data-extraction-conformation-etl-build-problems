"""The pack's documents: the National Adult Dentition Survey's report tables for its 1996, 2006 and 2016 waves (each
wave in its own layout), the Crematoria Mercury Regulation as consolidated, the Fund's scheme rules for 2026 and the
stack test summary the regulator publishes for abated crematoria."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4, letter                                        # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,  # noqa: E402
                                TableStyle)

import numpy as np   # noqa: E402

import survey as S   # noqa: E402
import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1e21")
GREY = colors.HexColor("#5d6168")
BLUE = colors.HexColor("#1f4e79")
GREEN = colors.HexColor("#2e5e3a")
RULE = colors.HexColor("#9aa1a9")


def styles(font, size, accent):
    bold = font + "-Bold"
    return {
        "body": ParagraphStyle("b", fontName=font, fontSize=size, leading=size * 1.4, textColor=INK, spaceAfter=6),
        "h1": ParagraphStyle("h1", fontName=bold, fontSize=size + 5, leading=size * 1.9, textColor=accent, spaceAfter=3),
        "sub": ParagraphStyle("s", fontName=font, fontSize=size - 0.5, leading=size * 1.35, textColor=GREY, spaceAfter=10),
        "h2": ParagraphStyle("h2", fontName=bold, fontSize=size + 1, leading=size * 1.5, textColor=accent, spaceBefore=8,
                             spaceAfter=4),
        "cap": ParagraphStyle("c", fontName=bold, fontSize=size - 0.5, leading=size * 1.3, textColor=INK, spaceBefore=6,
                              spaceAfter=3),
        "note": ParagraphStyle("n", fontName=font, fontSize=size - 1.6, leading=(size - 1.6) * 1.35, textColor=GREY,
                               spaceAfter=4),
        "cell": ParagraphStyle("t", fontName=font, fontSize=size - 1.4, leading=(size - 1.4) * 1.25, textColor=INK),
        "num": ParagraphStyle("u", fontName=font, fontSize=size, leading=size * 1.4, textColor=INK, spaceAfter=5,
                              leftIndent=24, firstLineIndent=-24),
        "sub2": ParagraphStyle("v", fontName=font, fontSize=size, leading=size * 1.4, textColor=INK, spaceAfter=4,
                               leftIndent=44, firstLineIndent=-18),
    }


def _doc(path, title, author, footer, font="LiberationSans", pagesize=A4, margins=(21, 21, 20, 20)):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(margins[0] * mm, 11 * mm, footer)
        canvas.drawRightString(pagesize[0] - margins[1] * mm, 11 * mm, "%d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=pagesize, leftMargin=margins[0] * mm, rightMargin=margins[1] * mm,
                          topMargin=margins[2] * mm, bottomMargin=margins[3] * mm, title=title, author=author,
                          subject="", creator="", producer="")
    return d, frame


def _grid(data, widths, st, head_rows=1, align_right_from=1, zebra=False, font="LiberationSans"):
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=head_rows)
    cmds = [("FONT", (0, 0), (-1, -1), font, 8.0), ("FONT", (0, 0), (-1, head_rows - 1), font + "-Bold", 8.0),
            ("LINEBELOW", (0, head_rows - 1), (-1, head_rows - 1), 0.6, INK), ("LINEABOVE", (0, 0), (-1, 0), 0.6, INK),
            ("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("ALIGN", (align_right_from, head_rows), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    if zebra:
        for r in range(head_rows, len(data), 2):
            cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f2f4f6")))
    t.setStyle(TableStyle(cmds))
    return t


# ---------------------------------------------------------------- the survey's report tables
FIELDWORK = {1996: ("13 May to 4 October 1996", "11 June 1997"), 2006: ("3 April to 27 October 2006", "19 June 2007"),
             2016: ("4 April to 29 October 2016", "14 June 2017")}


def _label(lo, hi):
    return S.band_label(lo, hi)


def write_survey(tab, year, path):
    title = "%s %d: report tables" % (W.SURVEY, year)
    footer = "%s  |  %s %d" % (W.SURVEY_BODY, W.SURVEY, year)
    doc, frame = _doc(path, title, W.SURVEY_BODY, footer, font="LiberationSans" if year != 1996 else "LiberationSerif",
                      pagesize=A4 if year != 1996 else letter)
    st = styles("LiberationSans" if year != 1996 else "LiberationSerif", 9.4, BLUE if year != 1996 else INK)
    P = Paragraph
    fw, pub = FIELDWORK[year]
    bands = S.BANDS[year]
    n_all = sum(tab[(year, s, lo)]["n"] for lo, hi in bands for s in "MF")
    story = [P(title, st["h1"]), P("%s. Published %s." % (W.SURVEY_BODY, pub), st["sub"])]
    if year == 1996:
        story += [P("About the survey", st["h2"]),
                  P("The survey examined a sample of adults aged 18 and over living in private households in every "
                    "province. Examining dentists recorded at a home visit each tooth present and the material of each "
                    "restoration. Estimates are weighted to the adult household population by age group, sex and "
                    "province. Fieldwork ran from %s; %s adults were examined." % (fw, "{:,}".format(n_all)), st["body"]),
                  P("Age is age at examination. In Tables 4 and 7 adults with no natural teeth count as having no teeth "
                    "restored with amalgam. Standard errors allow for the clustered sample.", st["body"])]
    else:
        story += [P("1. About the survey", st["h2"]),
                  P("The %s examines a sample of adults aged 18 and over living in private households. Examining "
                    "dentists, trained and calibrated for the survey, record at a home visit each tooth present and the "
                    "material of each restoration. Estimates are weighted to the adult household population by age "
                    "group, sex and province. Fieldwork ran from %s and %s adults were examined; adults aged 45 and "
                    "over were sampled at a higher rate than younger adults." % (W.SURVEY, fw, "{:,}".format(n_all)),
                    st["body"]),
                  P("2. Notes to the tables", st["h2"]),
                  P("Age is age at examination. A tooth restored with amalgam is a tooth with one or more amalgam "
                    "restorations at examination; a crowned tooth is counted by the material of its core where the "
                    "examiner could see it. Means are per adult in the group: adults with no natural teeth count as "
                    "having none. Confidence intervals allow for the clustered sample.", st["body"])]
    if year == 1996:
        story.append(P("Table 4. Adults with no natural teeth, by sex and age, 1996", st["cap"]))
        data = [["Sex and age", "Examined", "Edentulous, per cent"]]
        for s, sx in (("M", "Men"), ("F", "Women")):
            for lo, hi in bands:
                c = tab[(year, s, lo)]
                data.append(["%s %s" % (sx, _label(lo, hi)), "{:,}".format(c["n"]), "%.1f" % c["edentulous_pct"]])
        story.append(_grid(data, [52, 26, 36], st, font="LiberationSerif"))
        story.append(PageBreak())
        story.append(P("Table 7. Teeth restored with amalgam: mean per adult, by sex and age, 1996", st["cap"]))
        data = [["Sex and age", "Examined", "Mean", "Standard error"]]
        for s, sx in (("M", "Men"), ("F", "Women"), ("A", "All adults")):
            for lo, hi in bands:
                c = tab[(year, s, lo)]
                data.append(["%s %s" % (sx, _label(lo, hi)), "{:,}".format(c["n"]), "%.1f" % c["amalgam"], "%.2f" % c["se"]])
        story.append(_grid(data, [52, 26, 22, 30], st, font="LiberationSerif"))
    elif year == 2006:
        story.append(P("Table 3.1 Adults with no natural teeth (edentulous), by age and sex, 2006 (per cent)", st["cap"]))
        data = [["Age", "Men", "Women", "All adults"]]
        for lo, hi in bands:
            data.append([_label(lo, hi)] + ["%.1f" % tab[(year, s, lo)]["edentulous_pct"] for s in "MFA"])
        story.append(_grid(data, [34, 26, 26, 26], st))
        story.append(Spacer(1, 6))
        story.append(P("Table 3.4 Teeth restored with amalgam, mean per adult, by age and sex, 2006", st["cap"]))
        data = [["", "Men", "", "", "Women", "", ""], ["Age", "Examined", "Mean", "95% CI", "Examined", "Mean", "95% CI"]]
        for lo, hi in bands:
            row = [_label(lo, hi)]
            for s in "MF":
                c = tab[(year, s, lo)]
                row += ["{:,}".format(c["n"]), "%.1f" % c["amalgam"],
                        "%.1f to %.1f" % (max(0.0, c["amalgam"] - 1.96 * c["se"]), c["amalgam"] + 1.96 * c["se"])]
            data.append(row)
        t = _grid(data, [24, 19, 15, 26, 19, 15, 26], st, head_rows=2)
        t.setStyle(TableStyle([("SPAN", (1, 0), (3, 0)), ("SPAN", (4, 0), (6, 0)), ("ALIGN", (1, 0), (-1, 0), "CENTER")]))
        story.append(t)
    else:
        story.append(P("Table 3.1 Adults with no natural teeth (edentulous), by age and sex, 2016 (per cent)", st["cap"]))
        data = [["Age", "Men", "Women", "All adults"]]
        for lo, hi in bands:
            data.append([_label(lo, hi)] + ["%.1f" % tab[(year, s, lo)]["edentulous_pct"] for s in "MFA"])
        story.append(_grid(data, [34, 26, 26, 26], st))
        story.append(PageBreak())
        for k, (s, sx) in enumerate((("M", "men"), ("F", "women"), ("A", "all adults"))):
            story.append(P("Table 3.%d Teeth restored with amalgam, mean per adult, %s, by age, 2016" % (k + 2, sx),
                           st["cap"]))
            data = [["Age", "Adults examined", "Mean", "95% confidence interval"]]
            for lo, hi in bands:
                c = tab[(year, s, lo)]
                data.append([_label(lo, hi), "{:,}".format(c["n"]), "%.1f" % c["amalgam"],
                             "%.1f to %.1f" % (max(0.0, c["amalgam"] - 1.96 * c["se"]), c["amalgam"] + 1.96 * c["se"])])
            story.append(KeepTogether([_grid(data, [30, 32, 20, 44], st)]))
            story.append(Spacer(1, 5))
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the regulation
def write_regulation(path):
    title = "Crematoria Mercury Regulation"
    doc, frame = _doc(path, title, "Office of Legislative Counsel",
                      "Crematoria Mercury Regulation (Regulation 41/2023)  |  consolidated to 1 January 2025",
                      font="LiberationSerif", pagesize=letter, margins=(25, 25, 22, 20))
    st = styles("LiberationSerif", 10.6, INK)
    st["h1"].alignment = 1
    st["sub"].alignment = 1
    P = Paragraph
    s = [P("CREMATORIA MERCURY REGULATION", st["h1"]),
         P("Regulation 41/2023 under the Cremation and Burial Act. Consolidated to 1 January 2025 (amendments: "
           "Regulation 88/2024). This consolidation is prepared for convenience; the official text governs.", st["sub"]),
         P("Definitions", st["h2"]),
         P("1.&nbsp;&nbsp;In this Regulation,", st["body"]),
         P("“abated cremation” means a cremation performed in a cremator fitted with a mercury abatement "
           "plant that was commissioned before the date of the cremation;", st["sub2"]),
         P("“crematorium” means premises licensed under the Act for the cremation of human remains;", st["sub2"]),
         P("“Fund” means the Crematoria Mercury Fund continued under section 7;", st["sub2"]),
         P("“scheme year” means a calendar year beginning with 2026.", st["sub2"]),
         P("Mercury released by cremation", st["h2"]),
         P("2.&nbsp;&nbsp;(1) The mercury released by a cremation is the mercury in the dental amalgam in the teeth of "
           "the person cremated, taken as 0.55 grams for each tooth restored with amalgam.", st["num"]),
         P("(2) The mercury released by the cremation of a person who was under 18 years of age at death is taken as "
           "nil.", st["sub2"]),
         P("(3) The Fund shall estimate the teeth restored with amalgam of persons cremated from the %s." % W.SURVEY,
           st["sub2"]),
         P("(4) The mercury released by cremation in the province in a scheme year is the mercury released by the "
           "cremations performed at crematoria in the province in that year.", st["sub2"]),
         P("Abatement share", st["h2"]),
         P("3.&nbsp;&nbsp;From the 2026 scheme year, at least 55 per cent of the mercury released by cremation in the "
           "province in a scheme year shall be released in abated cremations.", st["num"]),
         P("Designation", st["h2"]),
         P("4.&nbsp;&nbsp;(1) Where less than 55 per cent of the mercury released by cremation in the province in a "
           "scheme year was released in abated cremations, the trustees of the Fund shall, by 31 March of the "
           "following year, designate crematoria at which no abated cremation was performed in that scheme year.",
           st["num"]),
         P("(2) Crematoria shall be designated in descending order of the mercury released by the cremations "
           "performed at them in the scheme year, until the share of that year’s mercury released in abated "
           "cremations, counting the mercury released at the crematoria designated as if it had been released in "
           "abated cremations, would have been at least 55 per cent.", st["sub2"]),
         P("(3) The operator of a designated crematorium shall connect every cremator at the crematorium to a "
           "commissioned mercury abatement plant by 31 December 2028.", st["sub2"]),
         P("Certificate", st["h2"]),
         P("5.&nbsp;&nbsp;The trustees shall certify for each scheme year the share of the mercury released by "
           "cremation in the province that was released in abated cremations, whether that share was at least 55 "
           "per cent, and the crematoria designated under section 4.", st["num"]),
         P("Records", st["h2"]),
         P("6.&nbsp;&nbsp;The operator of a crematorium shall provide the Fund with the records the Fund requires "
           "to carry out its functions, including the records of each cremator’s controller and of each "
           "abatement plant.", st["num"]),
         P("The Fund", st["h2"]),
         P("7.&nbsp;&nbsp;(1) The Crematoria Mercury Fund is continued as a fund administered by trustees appointed "
           "by the Minister, of whom at least three are nominated by operators of crematoria.", st["num"]),
         P("(2) The trustees may make scheme rules for the levies payable by operators to the Fund and for the "
           "administration of the Fund.", st["sub2"])]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the scheme rules
def write_rules(path):
    title = "Crematoria Mercury Fund: Scheme Rules 2026"
    doc, frame = _doc(path, title, W.FUND, "%s  |  Scheme Rules 2026, adopted by the trustees 18 November 2025" % W.FUND,
                      margins=(22, 22, 20, 20))
    st = styles("LiberationSans", 9.6, GREEN)
    P = Paragraph
    s = [P(title, st["h1"]),
         P("Made by the trustees under section 7(2) of the Crematoria Mercury Regulation. Adopted 18 November 2025; "
           "in force for the 2026 scheme year.", st["sub"]),
         P("1. Members", st["h2"]),
         P("Every operator of a crematorium in the province is a member of the Fund for each crematorium it "
           "operates. Words defined in the Regulation have the same meaning in these rules.", st["body"]),
         P("2. Levy", st["h2"]),
         P("2.1 Each member pays the Fund, for each crematorium and scheme year, a levy of 4.5 per cent of the "
           "crematorium’s cremation fee income from cremations performed in the scheme year that were not "
           "abated cremations, and 1.5 per cent of its cremation fee income from abated cremations performed in "
           "the scheme year.", st["body"]),
         P("2.2 Cremation fee income is the fees the crematorium charges for cremations and for the services it "
           "provides in connection with them: the use of the chapel and extended chapel time, the organist, the "
           "webcast and recording of a service, entries in the book of remembrance, the scattering of cremated "
           "remains in the crematorium’s grounds and copies of the certificate of cremation. It is taken net of "
           "credits allowed against those fees and excludes sales tax. It does not include the price of goods sold "
           "(urns, keepsakes, caskets) or amounts collected on behalf of others, such as the medical referee’s "
           "fee.", st["body"]),
         P("2.3 The levy is calculated on the scheme year’s cremation fee income and rounded to the nearest "
           "dollar. The Fund invoices it by 31 March of the following year.", st["body"]),
         P("3. Records", st["h2"]),
         P("3.1 Members provide the Fund with their fee records for each month, the records of each cremator’s "
           "controller and, for an abated crematorium, the records of its abatement plant.", st["body"]),
         P("3.2 Each quarter the trustees review, for each abated crematorium, the cremations performed while its "
           "abatement plant was bypassed.", st["body"]),
         P("4. Designation and certificate", st["h2"]),
         P("4.1 The trustees certify each scheme year and make any designation under section 4 of the Regulation "
           "at their first meeting after the scheme year closes.", st["body"]),
         P("4.2 A member whose crematorium is designated may apply to the Fund for a grant towards the cost of "
           "abatement plant. Grants are paid from levies.", st["body"])]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- stack tests (distractor)
def write_stack(path):
    """Compliance tests of mercury at the stack of abated crematoria, as the regulator publishes them."""
    rng = np.random.default_rng([W.SEED, 913])
    title = "Mercury stack tests at abated crematoria, 2019 to 2025"
    doc, frame = _doc(path, title, "Air Quality Branch", "Air Quality Branch  |  crematoria stack test summary, issued "
                      "3 March 2026", margins=(20, 20, 20, 20))
    st = styles("LiberationSans", 9.2, BLUE)
    P = Paragraph
    s = [P(title, st["h1"]),
         P("Air Quality Branch. Results of the tests operators submit under their approvals. Issued 3 March 2026.",
           st["sub"]),
         P("Mercury is measured over at least three cremations by the reference method and given at reference "
           "conditions (273 K, 101.3 kPa, dry gas, 11 per cent oxygen). The approval limit is 0.050 milligrams per "
           "cubic metre.", st["body"])]
    data = [["Crematorium", "Cremator", "Test date", "Cremations", "Mercury, mg/m³", "Result"]]
    for c in sorted(W.CREMATORIA, key=lambda x: x[2]):
        if c[8] != "A":
            continue
        start = dt.date.fromisoformat(c[9])
        d = dt.date(start.year, start.month, 1) + dt.timedelta(days=int(rng.integers(40, 120)))
        while d.year <= 2025:
            for cr in range(1, c[4] + 1):
                v = float(rng.lognormal(np.log(0.006), 0.55))
                data.append([c[2], "%d" % cr, d.isoformat(), "%d" % int(rng.integers(3, 6)), "%.3f" % v,
                             "Pass" if v < 0.05 else "Fail"])
            d = d + dt.timedelta(days=int(rng.integers(330, 400)))
    s.append(_grid(data, [58, 16, 22, 20, 28, 14], st, zebra=True, align_right_from=1))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
