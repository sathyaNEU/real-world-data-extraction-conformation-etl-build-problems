"""task170 documents: the KINGA-5 trial report and the campaign's operational plan. Their text is kept here as data
so checks.py and verify.py can quote it."""
from __future__ import annotations

import datetime as dt

import numpy as np

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import A4                                                  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as C          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2126")
GREY = colors.HexColor("#5b6169")
ACCENT = colors.HexColor("#1f4e3d")
RULE = colors.HexColor("#b9c4bd")
HEAD = colors.HexColor("#e4ece7")



def styles(font="LibSans", bold="LibSans-Bold", size=9.6):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.34, textColor=INK, spaceAfter=4),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=13.5, leading=17.0, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.0, textColor=GREY, spaceAfter=8),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.2, leading=13.0, textColor=ACCENT, spaceBefore=5,
                          spaceAfter=2.5),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.1, leading=9.8, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=8.1, leading=9.8, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.1, leading=9.8, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=7.8, leading=10.0, textColor=GREY, spaceAfter=3))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=21 * mm, rightMargin=21 * mm, topMargin=18 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="LibSans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(21 * mm, 9.5 * mm, left)
        canvas.drawRightString(A4[0] - 21 * mm, 9.5 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(st, head, rows, widths, right=()):
    data = [[Paragraph(esc(h), st["cellb"]) for h in head]]
    for r in rows:
        data.append([Paragraph(esc(str(x)), st["cellr"] if i in right else st["cell"]) for i, x in enumerate(r)])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def pdf_stamp(d, hh=9, mi=0):
    return ("D:%04d%02d%02d%02d%02d00+03'00'" % (d.year, d.month, d.day, hh, mi)).encode()



from reportlab.platypus import KeepTogether  # noqa: E402

import world as W  # noqa: E402

F_TRIAL = "kinga5_final_report_2024.pdf"
F_PLAN = "lulanet_r_distribution_plan_2027.docx"
TRIAL_DATE = dt.date(2024, 3, 18)
PLAN_DATE = dt.date(2026, 10, 2)

HOUR_ROWS = ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00", "05:00"]
HALF_ROWS = ["18:30", "19:30", "20:30", "21:30", "22:30", "23:30", "00:30", "01:30", "02:30", "03:30", "04:30", "05:30"]

TRIAL_TITLE = "KINGA-5: a household-randomised trial of a transfluthrin-treated sleeping net against Ombeni fever"
TRIAL_SUMMARY = [
    "KINGA-5 tested LulaNet R, a polyester sleeping net treated with transfluthrin, at five rural sites in three "
    "countries between February 2022 and January 2023. Households were randomised one to one to receive LulaNet R "
    "nets for every sleeping space or no net, and every household member was followed for twelve months.",
    "Participants were visited every month and tested by rapid diagnostic test when febrile; febrile participants "
    "between visits were tested at the study clinic. The primary outcome was confirmed Ombeni fever. Field staff "
    "checked sleeping spaces at unannounced night visits; participants in net households were under the net at 96 to "
    "98 per cent of checks at every site. Protective efficacy is one minus the ratio of the incidence in net "
    "households to the incidence in households without nets, by site and pooled across sites.",
    "LulaNet R repels mosquitoes from the occupied net; it does not kill them. Mosquitoes were caught landing on "
    "collectors indoors and outdoors at 24 houses at each site, every hour from 18:00 to 06:00, two nights a month "
    "for the twelve months; the vector at every site was Anopheles ruvariensis. A survey of 300 households at each "
    "site in the third month recorded each member's times of going indoors for the night, going to bed and rising.",
]
TRIAL_NOTE = ("Protective efficacy is computed from the cases and person-years shown. The pooled estimate stratifies "
              "by site.")
ENTO_NOTE = ("Mean An. ruvariensis landings per collector per hour of collection, two nights a month for twelve "
             "months, 24 houses a site. Hours are the hour beginning.")
BEHAV_NOTE = ("Per cent of household members indoors (in bed or not) and in bed at the half hour, from the third-month "
              "survey, all ages.")


def write_trial(out, sites):
    st = styles()
    path = out + "/" + F_TRIAL
    doc = _doc(path, TRIAL_TITLE, "KINGA-5 Trial Steering Committee")
    flow = [Paragraph(esc(TRIAL_TITLE), st["h1"]),
            Paragraph("Final report to the trial's funders, 18 March 2024. KINGA-5 Trial Steering Committee.", st["sub"]),
            Paragraph("1. Design", st["h2"])]
    for p in TRIAL_SUMMARY:
        flow.append(Paragraph(esc(p), st["body"]))
    flow.append(Paragraph("2. Results", st["h2"]))
    rows = []
    for s in sites:
        ic = s["cases_c"] / s["py_c"]
        inn = s["cases_n"] / s["py_n"]
        pe = 1 - inn / ic
        se = (1 / s["cases_c"] + 1 / s["cases_n"]) ** 0.5
        lo, hi = 1 - (inn / ic) * np.exp(1.96 * se), 1 - (inn / ic) * np.exp(-1.96 * se)
        rows.append([s["site"], "{:,}".format(s["cases_c"]), "{:,.1f}".format(s["py_c"]), "{:,}".format(s["cases_n"]),
                     "{:,.1f}".format(s["py_n"]), "%.1f (%.1f to %.1f)" % (100 * pe, 100 * lo, 100 * hi)])
    cc, pc = sum(s["cases_c"] for s in sites), sum(s["py_c"] for s in sites)
    cn, pn = sum(s["cases_n"] for s in sites), sum(s["py_n"] for s in sites)
    # Mantel-Haenszel rate ratio across sites
    num = sum(s["cases_n"] * s["py_c"] / (s["py_c"] + s["py_n"]) for s in sites)
    den = sum(s["cases_c"] * s["py_n"] / (s["py_c"] + s["py_n"]) for s in sites)
    pooled = 1 - num / den
    rows.append(["All sites", "{:,}".format(cc), "{:,.1f}".format(pc), "{:,}".format(cn), "{:,.1f}".format(pn),
                 "%.1f" % (100 * pooled)])
    flow.append(Paragraph("Table 1. Confirmed Ombeni fever by site and arm, and protective efficacy (per cent, 95% CI)",
                          st["cellb"]))
    flow.append(_table(st, ["Site", "No-net cases", "No-net person-years", "Net cases", "Net person-years",
                            "Protective efficacy"], rows, [24, 22, 28, 20, 26, 48], right=(1, 2, 3, 4)))
    flow.append(Paragraph(esc(TRIAL_NOTE), st["small"]))
    flow.append(Paragraph("3. Site entomology and sleeping times", st["h2"]))
    sites_h = [s["site"] for s in sites]
    for key, label, lab2 in (("b_in", "Table 2a. An. ruvariensis landings per collector per hour, indoors", "%.2f"),
                             ("b_out", "Table 2b. An. ruvariensis landings per collector per hour, outdoors", "%.2f")):
        rows_t = [[HOUR_ROWS[h]] + [lab2 % s[key][h] for s in sites] for h in range(12)]
        flow.append(KeepTogether([Paragraph(label, st["cellb"]),
                                  _table(st, ["Hour"] + sites_h, rows_t, [22] + [26] * 5, right=tuple(range(1, 6)))]))
    flow.append(Paragraph(esc(ENTO_NOTE), st["small"]))
    for key, label in (("ind", "Table 3a. Household members indoors, in bed or not (per cent)"),
                       ("inb", "Table 3b. Household members in bed (per cent)")):
        rows_t = [[HALF_ROWS[h]] + ["%d" % s[key][h] for s in sites] for h in range(12)]
        flow.append(KeepTogether([Paragraph(label, st["cellb"]),
                                  _table(st, ["Time"] + sites_h, rows_t, [22] + [26] * 5, right=tuple(range(1, 6)))]))
    flow.append(Paragraph(esc(BEHAV_NOTE), st["small"]))
    flow.append(Paragraph("4. Adverse events", st["h2"]))
    flow.append(Paragraph("Skin or eye irritation was reported by 1.9 per cent of participants in net households in the "
                          "first week, and by none after the first month. No serious adverse event was attributed to "
                          "the net.", st["body"]))
    doc.build(flow, onFirstPage=_footer("KINGA-5 final report, March 2024"), onLaterPages=_footer("KINGA-5 final report, March 2024"))
    PP.normalize_pdf(path, pdf_stamp(TRIAL_DATE, 16, 10), pdf_stamp(TRIAL_DATE, 16, 10))
    return dict(pooled=pooled)


# ---------------------------------------------------------------------------------------------------- the plan (docx)
PLAN_TITLE = "LulaNet R county-wide distribution, March 2027: operational plan"
PLAN_PARAS = {
    "scope": "Every household registered by community health volunteers in the seven sub-counties receives LulaNet R "
             "nets at its village distribution point between 1 and 27 March 2027, sub-county by sub-county as Table "
             "1 sets out. Registration ran from 7 to 26 September 2026, with a mop-up from 1 to 9 October 2026 for "
             "households the first round missed.",
    "product": "LulaNet R is a polyester sleeping net treated with transfluthrin, which repels mosquitoes from the "
               "occupied net. It does not kill them. The supplier warrants three years of use.",
    "rule": "One net for every two usual members of a household, rounded up, and no more than four nets to a "
            "household. A usual member is a person who has slept in the household on most nights of the last three "
            "months.",
    "use": "Use is planned at the share of residents sleeping under a campaign net in Table 2, agreed with the "
           "Arnbridge Foundation in August 2026 from the national programme's net-use curve for mass campaigns.",
    "baseline": "Expected Ombeni fever cases without the campaign are the county's 2027 planning baseline, by "
                "sub-county and month (obf_planning_baseline_2027.xlsx).",
    "impact": "The grant report counts the Ombeni fever cases the nets avert among residents sleeping under campaign "
              "nets from April to December 2027, against the planning baseline and at the use in Table 2. It counts "
              "no cases averted among residents who are not under a campaign net. Sub-county figures in the grant report "
              "follow the ward realignment of 1 July 2026.",
    "monitoring": "Post-distribution surveys at three, six and nine months record nets present and used. The county "
                  "entomology unit continues its sentinel catches through 2027.",
}
DIST_WEEKS = [("RTN", "1 to 6 March"), ("MWR", "1 to 6 March"), ("KDG", "8 to 13 March"), ("OYM", "8 to 13 March"),
              ("NDR", "15 to 20 March"), ("KBR", "15 to 20 March"), ("WKL", "22 to 27 March")]


def write_plan(out, usage):
    from docx import Document
    from docx.shared import Pt
    path = out + "/" + F_PLAN
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading(PLAN_TITLE, level=1)
    d.add_paragraph("Ruvari County Department of Health and Tulivu Health Partners. Version 2.1, 2 October 2026. "
                    "Contacts: Elkana Karanja (county vector-borne disease control), Dorcas Kagwiria (Tulivu, "
                    "monitoring and evaluation).")
    d.add_heading("1. Scope", level=2)
    d.add_paragraph(PLAN_PARAS["scope"])
    t = d.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Sub-county", "Distribution"
    for sc, w in DIST_WEEKS:
        r = t.add_row().cells
        r[0].text, r[1].text = C.SC_NAME[sc], w
    d.add_paragraph("Table 1. Distribution weeks.")
    d.add_heading("2. Product", level=2)
    d.add_paragraph(PLAN_PARAS["product"])
    d.add_heading("3. Allocation", level=2)
    d.add_paragraph(PLAN_PARAS["rule"])
    d.add_heading("4. Planning assumptions", level=2)
    d.add_paragraph(PLAN_PARAS["use"])
    t = d.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Month (2027)", "Residents under a campaign net (per cent)"
    import calendar
    for m in range(4, 13):
        r = t.add_row().cells
        r[0].text, r[1].text = calendar.month_name[m], "%d" % round(usage[m] * 100)
    d.add_paragraph("Table 2. Planned use.")
    d.add_paragraph(PLAN_PARAS["baseline"])
    d.add_heading("5. Impact reporting", level=2)
    d.add_paragraph(PLAN_PARAS["impact"])
    d.add_heading("6. Monitoring", level=2)
    d.add_paragraph(PLAN_PARAS["monitoring"])
    d.core_properties.title = PLAN_TITLE
    d.save(path)
    PP.normalize_docx(path, C.PEOPLE["vbd"], C.PEOPLE["me"], "2026-08-11T06:42:00Z", "2026-10-02T12:18:00Z", 14, 412,
                      seed=C.SEED, title=PLAN_TITLE, company=C.ORG)
