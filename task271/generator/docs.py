"""The pack's documents: the Clinical Programs Committee's criteria for the 2027 Family Outreach Program, the Inherited
Cancer Risk Service's data guide to the registry extracts, and the pack's contents."""
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
PLUM = colors.HexColor("#5a2d5c")
SLATE = colors.HexColor("#2f4858")


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


# ------------------------------------------------------------------------------------------- the criteria
def write_criteria(path):
    S = styles("Sans", PLUM)
    doc = _doc(path, "Family Outreach Program: criteria for the variant groups, 2027", K.SYSTEM)
    st = []
    st.append(Paragraph("Family Outreach Program: criteria for the variant groups, 2027", S["h1"]))
    st.append(Paragraph("%s &nbsp;|&nbsp; %s &nbsp;|&nbsp; Approved 24 September 2026 &nbsp;|&nbsp; Program owner: "
                        "%s" % (K.SYSTEM, K.COMMITTEE, K.SERVICE), S["meta"]))
    st.append(Paragraph("1. The program", S["h2"]))
    st.append(_clause(S, "1.1", "From 1 April 2027 the %s writes again, for each variant group it takes on, to the "
                                "first-degree relatives of the service's probands who have no test result on file. It "
                                "offers each of them a test for the family's variant and offers every woman found to "
                                "carry it a place in the %s: an annual breast MRI from age 30 to 74, with mammography "
                                "from 40." % (K.PROGRAM, K.CLINIC)))
    st.append(_clause(S, "1.2", "The program also offers the clinic to the women the service already knows to carry a "
                                "variant in a group it takes on (section 3)."))
    st.append(_clause(S, "1.3", "The service's medical director adopts the groups in February 2027 for the program's "
                                "first two years, applying these criteria to the service's records of the families "
                                "referred to it since universal panel testing began in January 2016. The committee "
                                "reviews the program after its first year."))
    st.append(Paragraph("2. Taking a group on", S["h2"]))
    st.append(_clause(S, "2.1", "The program takes on a variant group when a woman who carries a variant in the group "
                                "has a risk of breast cancer by age 70 of 30 percent or more."))
    st.append(_clause(S, "2.2", "The risk is the chance that a woman who has inherited a variant in the group is "
                                "diagnosed with a first breast cancer, invasive or in situ, before her 70th birthday if "
                                "she lives to 70. Deaths from other causes do not lower it."))
    st.append(_clause(S, "2.3", "It is measured on the service's families: the mothers, sisters and daughters of the "
                                "probands, living or dead, as each family's pedigree records them. The probands are not "
                                "counted, because their own cancer brought the family to the service. Half-sisters are "
                                "second-degree relatives and are not counted."))
    st.append(_clause(S, "2.4", "Each group's risk is compared with 30 percent unrounded."))
    st.append(Paragraph("3. Planning figures for the %s" % K.CLINIC, S["h2"]))
    st.append(_clause(S, "3.1", "For each group, the women the service already knows to carry a variant in it whom the "
                                "program would offer the clinic on 1 April 2027: women whose final laboratory report "
                                "shows the family's variant as pathogenic or likely pathogenic, who are %s patients "
                                "(an enterprise ID), are not recorded as having died by 30 September 2026, are aged 30 "
                                "to 74 on 1 April 2027 and have not had both breasts removed." % K.SYSTEM))
    st.append(_clause(S, "3.2", "For each group, how many of those women had no completed high-risk screening breast "
                                "MRI at an %s hospital from 1 October 2025 to 30 September 2026." % K.SYSTEM))
    st.append(Paragraph("4. Terms", S["h2"]))
    rows = [["Term", "Meaning"],
            ["Proband", "The family member whose test first found the variant and through whom the family came to "
                        "the service."],
            ["Carrier", "A person who has inherited the family's variant."],
            ["First-degree relative", "A parent, full sibling or child."],
            ["Variant group", "The service's register groups each pathogenic or likely pathogenic variant by gene and "
                              "variant type (%s)." % K.FILES["groups"]],
            ["Final laboratory report", "A report that no later amended report or re-analysis replaces."]]
    st.append(_table(S, rows, [1.6, 5.1]))
    st.append(Spacer(1, 8))
    st.append(Paragraph("Questions on these criteria go to %s, %s." % (K.PEOPLE["requester"],
                                                                        K.PEOPLE["requester_title"]), S["meta"]))
    doc.build(st, onFirstPage=_frame(K.SYSTEM + " | " + K.COMMITTEE, "Family Outreach Program criteria 2027", "Sans"),
              onLaterPages=_frame(K.SYSTEM + " | " + K.COMMITTEE, "Family Outreach Program criteria 2027", "Sans"))


# ------------------------------------------------------------------------------------------- the data guide
def write_guide(path, counts):
    S = styles("Serif", SLATE)
    doc = _doc(path, "ICRS registry extracts: data guide", K.SERVICE)
    st = []
    st.append(Paragraph("Inherited Cancer Risk Service registry extracts: data guide", S["h1"]))
    st.append(Paragraph("%s, %s &nbsp;|&nbsp; Extracts cut 30 September 2026 &nbsp;|&nbsp; Prepared 22 October 2026"
                        % (K.SYSTEM, K.SERVICE), S["meta"]))
    st.append(Paragraph("The service's register", S["h2"]))
    st.append(Paragraph(
        "Since January 2016 every %s patient diagnosed with breast cancer has been offered a hereditary breast cancer "
        "panel. When a panel finds a pathogenic or likely pathogenic variant, the patient is referred to the service as "
        "the family's proband, the counselor takes a three-generation pedigree, and the family joins the register under "
        "the variant's group. The register holds the families whose variant is in one of the ten groups below; families "
        "with BRCA1, BRCA2 and the other genes the service follows under separate programs are not in these extracts."
        % K.SYSTEM, S["body"]))
    st.append(Paragraph(
        "A family's pedigree is brought up to date when the service next sees any member of the family, when a late "
        "result (an amended report or a re-analysis) reopens the family, and when the tumor registry links a new "
        "diagnosis of a patient on the register. Each person's vital status and age are as of the family's history date.",
        S["body"]))
    st.append(Paragraph("Files", S["h2"]))
    rows = [["File", "One row is", "Notes"],
            [K.FILES["pedigree"], "a person in a family's pedigree (%s rows)" % format(counts["pedigree"], ","),
             "relationship to the proband (PROBAND, MOTHER, FATHER, SISTER, BROTHER, DAUGHTER, SON, HALF_SISTER_MAT and "
             "the other half-sibling codes, PARTNER, and the grandparent, aunt, uncle, niece, nephew and grandchild "
             "codes, MAT_ or PAT_ for the side); mother_id and father_id within the family; birth_year for everyone, "
             "birth_date and enterprise_id for %s patients; vital_status and age (age at death for the deceased) as of "
             "history_date; up to three cancers with the age at diagnosis in completed years; ages_reported Exact when "
             "confirmed from the system's records, Approximate when given by the family." % K.SYSTEM],
            [K.FILES["labs"], "a laboratory report",
             "%s to February 2021, written with the laboratory's own variant names (legacy_name); the %s from March "
             "2021, written in HGVS. An Amended or Reanalysis report replaces the report in supersedes. Panels list "
             "the variant found; a familial variant analysis tests one relative for the family's variant." %
             (K.REFLAB, K.LAB)],
            [K.FILES["groups"], "a group (Groups) or a variant (Variants)",
             "Each variant's HGVS names, the reference laboratory's name and its classification."],
            [K.FILES["incidence"], "a 5-year age band",
             "First primary breast cancers, invasive and in situ, among %s female patients, 2016 to 2025, and the "
             "female patient-years." % K.SYSTEM],
            [K.FILES["abstracts"], "a breast cancer the tumor registry abstracted",
             "Diagnosed or treated at an %s hospital from 2016; the most definitive first-course surgery of the "
             "breast (code and description)." % K.SYSTEM],
            [K.FILES["surgery"], "a surgical procedure",
             "From the current EHR (live 4 March 2019): CPT code with modifier LT, RT or 50 (both sides)."],
            [K.FILES["imaging"], "a breast MRI order",
             "Hospital and record number, the enterprise ID on the order, exam date, CPT code, indication and status."],
            [K.FILES["empi"], "a hospital record number", "The enterprise ID it belongs to and the date registered."],
            [K.FILES["merges"], "a merge of two enterprise IDs", "The retired ID and the ID it was merged into."],
            [K.FILES["deaths"], "a death", "Patients on the register who died by 30 September 2026."],
            [K.FILES["capacity"], "a hospital", "Breast MRI scanners and weekly slots, 2026 and planned for 2027."],
            [K.FILES["prs"], "a polygenic score", "The 2025 pilot of a 313-variant breast cancer score for carriers."]]
    st.append(_table(S, rows, [2.35, 1.35, 3.0]))
    doc.build(st, onFirstPage=_frame(K.SYSTEM + " | " + K.SERVICE, "Registry extracts: data guide", "Serif"),
              onLaterPages=_frame(K.SYSTEM + " | " + K.SERVICE, "Registry extracts: data guide", "Serif"))


def write_contents(path, items):
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("%s, %s: files for the 2027 Family Outreach Program review\n" % (K.SYSTEM, K.SERVICE))
        f.write("Assembled 22 October 2026\n\n")
        for name, desc in items:
            f.write("%s\n    %s\n" % (name, desc))
