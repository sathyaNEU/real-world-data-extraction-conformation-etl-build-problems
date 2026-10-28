"""task273 architecture 4: the pack's documents. The programme's panel policy (the review's standard) and the
laboratory's methods and quality report for the Study's two sequencing phases."""
from __future__ import annotations

import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import cm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import params as P   # noqa: E402

FONT_DIR = next((d for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"),
                              "/Library/Fonts/") if os.path.exists(d + "LiberationSerif-Regular.ttf")),
                "/usr/share/fonts/truetype/liberation/")
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1c2330"), colors.HexColor("#5a6470"), colors.HexColor("#bcc4cc")
BOARD_BLUE = colors.HexColor("#1f4e79")
LAB_GREEN = colors.HexColor("#2f5d50")


def styles(face, accent):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=10.0, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=15, leading=19, textColor=accent, spaceAfter=3),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.8, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=10),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.2, leading=10.2, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.2, leading=10.2, textColor=INK),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10.0, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=30, firstLineIndent=-30))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(2.2 * cm, A4[1] - 1.35 * cm, left)
        canvas.drawRightString(A4[0] - 2.2 * cm, A4[1] - 1.35 * cm, right)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.1 * cm,
                             bottomMargin=1.9 * cm, title=title, author=author, subject=subject,
                             creator="Microsoft Word for Microsoft 365", producer="Microsoft Word for Microsoft 365")


# ---------------------------------------------------------------------------------------------- the panel policy
def write_policy(path):
    S = styles("Serif", BOARD_BLUE)
    doc = _doc(path, "Couples Carrier Screening Programme: Panel Policy", P.BOARD, "Panel policy, version 3")
    fr = _frame(P.BOARD + ", Public Health Directorate", "CCSP Panel Policy, version 3 (approved 12 March 2024)")
    s = []
    s.append(Paragraph("Couples Carrier Screening Programme: Panel Policy", S["h1"]))
    s.append(Paragraph("Version 3. Approved by the Executive Leadership Team on 12 March 2024; replaces version 2 "
                       "(June 2021). Owner: the Panel Review Group. Next review: March 2027.", S["meta"]))
    s.append(Paragraph("1. Purpose", S["h2"]))
    s.append(Paragraph(
        "The %s offers couples who are planning a pregnancy, or who are in the first ten weeks of one, a test of both "
        "partners for carrier status in a set of recessive conditions (the panel). Couples who are both carriers of "
        "the same condition are offered genetic counselling and reproductive options. This policy sets which "
        "conditions are on the panel and how the panel is reviewed." % P.PROGRAMME, S["body"]))
    s.append(Paragraph("2. Which conditions are on the panel", S["h2"]))
    s.append(_clause(S, "2.1", "A condition is on the panel for a screening year (1 April to 31 March) when, in the "
                     "reference cohort, at least one person in 200 carries a disease-causing variant in the gene "
                     "that causes it."))
    s.append(_clause(S, "2.2", "The reference cohort is every member of the %s whose consent is in force and whose "
                     "genotype the %s has released on the census date, 1 November of the year before the screening "
                     "year. The Study is the Board's population reference: its two recruitment phases together are "
                     "the cohort." % (P.STUDY, P.LAB)))
    s.append(_clause(S, "2.3", "A disease-causing variant is one the laboratory's variant register classifies as "
                     "pathogenic or likely pathogenic on the census date."))
    s.append(_clause(S, "2.4", "A person counts once for a condition however many disease-causing variants they carry "
                     "in its gene."))
    s.append(_clause(S, "2.5", "Only autosomal recessive conditions with a severe or moderate-to-severe course, onset "
                     "in childhood and a test the laboratory has validated are reviewed. All conditions nominated for "
                     "a review meet this clause before it starts."))
    s.append(Paragraph("3. The annual review", S["h2"]))
    s.append(_clause(S, "3.1", "Each autumn the Panel Review Group reviews every condition on the panel and every "
                     "condition nominated by a clinical service, the laboratory or a primary care group, and recommends "
                     "the next screening year's panel to the Director of Public Health, who decides it under the "
                     "Board's scheme of delegation."))
    s.append(_clause(S, "3.2", "The recommendation states, for every condition reviewed, its carrier frequency in the "
                     "reference cohort and whether it is on the next year's panel, and names the conditions joining "
                     "and leaving."))
    s.append(_clause(S, "3.3", "The recommendation also reports the programme's own experience of the conditions on "
                     "the current panel over the last complete screening year."))
    s.append(Paragraph("4. How couples are tested and told", S["h2"]))
    s.append(_clause(S, "4.1", "In a simultaneous screen both partners are tested for every condition on the panel. In "
                     "a sequential screen one partner is tested first, and the other partner is tested only for the "
                     "conditions the first partner carries; where the first partner carries none, the screen ends."))
    s.append(_clause(S, "4.2", "Couples receive their results together, in one report, once every result their screen "
                     "needs has been authorised. A partner tested within the last two years with the current panel "
                     "is not tested again: that result is used for the new couple."))
    s.append(_clause(S, "4.3", "A report states each variant found with the classification the register gave it on the "
                     "day the result was authorised. Reports are not reissued when the register later changes a "
                     "classification."))
    s.append(Paragraph("5. Records", S["h2"]))
    s.append(Paragraph(
        "The laboratory keeps the variant register, the Study's sequencing records and the programme's results. The "
        "Panel Review Group's papers are kept by the Public Health Directorate for ten years.", S["body"]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Approved: %s, Chair, Panel Review Group, on behalf of the Executive Leadership Team." %
                       P.PEOPLE["chair"], S["note"]))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------------------------- the methods report
def write_methods(path, coverage):
    S = styles("Sans", LAB_GREEN)
    doc = _doc(path, "Ardvenny Genome Study: Sequencing Methods and Quality Report", P.LAB,
               "Methods and quality, phases 1 and 2")
    fr = _frame(P.LAB, "AGS methods and quality report, issue 6, %s" % P.EXTRACT.strftime("%d %B %Y").lstrip("0"))
    c1, c2 = P.CALLER[1], P.CALLER[2]
    s = []
    s.append(Paragraph("Ardvenny Genome Study: Sequencing Methods and Quality Report", S["h1"]))
    s.append(Paragraph("Issue 6, %s. Prepared for the Panel Review Group's 2027/28 review by %s, %s." %
                       (P.EXTRACT.strftime("%d %B %Y").lstrip("0"), P.PEOPLE["lab_head"], P.ROLES["lab_head"]),
                       S["meta"]))
    s.append(Paragraph("1. The Study", S["h2"]))
    s.append(Paragraph(
        "The %s is the Board's population genome study. Phase 1 (2019 to 2021) recruited adult volunteers in the "
        "Morvaig Isles and Glenhaskel; phase 2 (2022 to 2025) recruited in Kilvenny, Quarrendale and Strathvenny. "
        "Every member gave a blood sample and broad consent; a member may withdraw at any time, and a withdrawal "
        "takes effect on the date recorded in the member register." % P.STUDY, S["body"]))
    s.append(Paragraph("2. Sequencing and calling", S["h2"]))
    rows = [["", "Phase 1 (2019 to 2021)", "Phase 2 (2022 to 2025)"],
            ["Capture", c1["kit"], c2["kit"]],
            ["Sequencer and read length", "Short-read, 2 x 100 bp", "Short-read, 2 x 150 bp"],
            ["Reference build", "GRCh37", "GRCh38"],
            ["Calling pipeline", c1["name"], c2["name"]],
            ["Heterozygous call", "at least %d reads carrying the alternate allele, making up at least %d per cent of "
             "the reads at the site" % (c1["k"], round(c1["f"] * 100)),
             "at least %d reads carrying the alternate allele, making up at least %d per cent of the reads at the site"
             % (c2["k"], round(c2["f"] * 100))],
            ["Homozygous alternate call", "alternate allele at least 85 per cent of the reads", "the same"],
            ["Variant names in the call file", "the transcripts current in 2019", "current transcripts"],
            ["Minimum reads at a register site", "%d (samples below were topped up with a further run)" % c1["floor"],
             "%d (the same)" % c2["floor"]]]
    s.append(_table(S, rows, [4.3, 6.1, 6.1]))
    s.append(Paragraph(
        "Each phase's samples were called with the pipeline in use at the time and have not been recalled. The call "
        "files list the non-reference genotypes each pipeline called at register sites, one row for each member and "
        "site. The depth file gives, for every released member and every "
        "register site, the number of reads at the site that passed the pipeline's mapping and base quality filters, "
        "that is the reads the caller weighed.", S["body"]))
    s.append(Paragraph("3. Quality control", S["h2"]))
    s.append(Paragraph(
        "A sample failing the contamination, sex-concordance or identity checks is not released; its member stays in "
        "the register with the genotype status 'Withheld after QC'. Every register site in every released sample "
        "reached the phase's minimum read count, if necessary after a top-up run, before release.", S["body"]))
    cov = [["Register sites, reads per released member", "Phase 1", "Phase 2"]]
    for lab, a, b in coverage:
        cov.append([lab, a, b])
    s.append(_table(S, cov, [7.6, 4.4, 4.4], right=(1, 2)))
    s.append(Paragraph("Read counts at the register sites the Study genotypes, over every released member and "
                       "site.", S["note"]))
    s.append(Paragraph("4. The variant register", S["h2"]))
    s.append(Paragraph(
        "The register holds every variant the laboratory has classified in the genes it tests, with its position on "
        "both reference builds, its current and 2019 transcript names, its classification and the date it took "
        "effect. Changes of classification are decided by the variant review group and recorded with their "
        "effective dates; a change takes effect for reports authorised on or after that date.", S["body"]))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)
