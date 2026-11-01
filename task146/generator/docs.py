"""task146 architecture 3: the VELA-2 SAP, the clinical development plan's section 7 and the request email."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP

ORG = "Hvidore Biologics A/S"
DOMAIN = "hvidorebio.dk"


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.2, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EAF0"))]))
    return t


def _footer(text):
    def f(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return f


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                             subject=title, invariant=1)


def sap(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "HB231-201 (VELA-2) Statistical Analysis Plan v2.0", "Biostatistics, " + ORG)
    s = [Paragraph(ORG + ", Biostatistics", small), Paragraph("HB231-201 (VELA-2) Statistical Analysis Plan", h1),
         Paragraph("Version 2.0, 12 August 2026, final before database lock. Supersedes version 1.1 of 3 June 2025.",
                   small), Spacer(1, 4)]
    sec = [
        ("1. Study design", [
            "VELA-2 is a randomised, double-blind, placebo-controlled, parallel-group phase 2b study of HB-231 in "
            "adults with moderate-to-severe chronic plaque psoriasis (PASI 12 or more, body surface area 10 per cent "
            "or more, IGA 3 or 4). Patients are randomised 1:1:1:1:1 to placebo or HB-231 25, 50, 100 or 200 mg, "
            "given subcutaneously at weeks 0, 4, 8 and 12. The primary endpoint is PASI 75 at week 16."]),
        ("2. Analysis population and study days", [
            "The full analysis set is every randomised patient, analysed by the arm assigned. Study day 1 is the day "
            "of the first dose of study drug, as the dosing log records it; other study days count from it.",
            "Baseline for PASI is the last assessment on or before the day of the first dose. The week-16 value is "
            "the assessment recorded at the week-16 visit."]),
        ("3. PASI 75 and PASI 90", [
            "A patient is a PASI 75 responder when the week-16 PASI is at least 75 per cent below baseline, and a "
            "PASI 90 responder when it is at least 90 per cent below baseline, and in either case the patient took "
            "no rescue therapy before the week-16 assessment.",
            "Rescue therapy is any of the following started after the first dose and on or before the date of the "
            "week-16 assessment: a potent or very potent topical corticosteroid (ATC D07AC or D07AD), or "
            "phototherapy. A patient with no week-16 PASI, whatever the reason, is a non-responder.",
            "Response rates are the responders as a per cent of the patients randomised to the arm."]),
        ("4. Itch", [
            "Patients rate their worst itch over the past 24 hours on a 0 to 10 numeric rating scale (NRS) in an "
            "evening electronic diary, which opens at 19:00 local time. An entry completed after midnight and "
            "before 03:00 belongs to the diary day that began the evening before. The ePRO export carries each "
            "entry's completion time in UTC; the diary day is reckoned in the site's local time.",
            "The weekly itch score is the mean of the daily entries over study days -7 to -1 (baseline), 22 to 28 "
            "(week 4) and 106 to 112 (week 16), and exists when at least four of the seven days have an entry.",
            "A patient is an itch responder at a week when the baseline weekly score is at least 4 and the weekly "
            "score at that week is at least 4 points below it, and the patient took no rescue therapy before the "
            "week's last day. Patients with a baseline weekly score of at least 4 form the denominator; a patient "
            "in it without a weekly score at the week is a non-responder."]),
        ("5. Pharmacokinetics", [
            "Trough samples are drawn before dosing at weeks 4, 8, 12 and 16 and assayed by a validated ligand-"
            "binding method with a lower limit of quantification of 0.10 micrograms per mL. Concentrations below "
            "it are reported as below the limit and are not used in summaries of concentration."]),
        ("6. Missing data and estimand", [
            "The primary estimand is the composite one: rescue therapy and discontinuation before week 16 count as "
            "non-response, and no value is imputed for a patient who has none."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Paragraph("7. Document history", h2))
    s.append(_grid([["Version", "Date", "Change"],
                    ["1.0", "14 April 2025", "First version"],
                    ["1.1", "3 June 2025", "Itch diary window and the after-midnight rule added (section 4)"],
                    ["2.0", "12 August 2026", "Rescue therapy list fixed by ATC class (section 3); final"]],
                   [22 * mm, 30 * mm, 118 * mm], cell))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Approved by Bodil Lauritsen, Head of Biostatistics, and Helle Carlsen, Chief Medical Officer.",
                       small))
    doc.build(s, onFirstPage=_footer("HB231-201 SAP v2.0  |  " + ORG), onLaterPages=_footer("HB231-201 SAP v2.0  |  "
                                                                                            + ORG))
    PP.normalize_pdf(path, b"D:20260812141900+02'00'", b"D:20260812163300+02'00'", "Biostatistics")


def cdp(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "HB-231 Clinical Development Plan v2.1, section 7", "Clinical Development, " + ORG)
    s = [Paragraph(ORG + ", Clinical Development", small),
         Paragraph("HB-231 Clinical Development Plan, section 7: phase 3", h1),
         Paragraph("Version 2.1, approved by the Executive Committee on 4 June 2026. Extract: section 7 only.", small),
         Spacer(1, 4)]
    sec = [
        ("7.1 The phase 3 programme", [
            "The phase 3 programme comprises two replicate randomised, double-blind, placebo-controlled trials, "
            "VELA-3A and VELA-3B, each of about 600 adults with moderate-to-severe chronic plaque psoriasis, at "
            "sites in the United States and Canada. Patients receive HB-231 or placebo subcutaneously at weeks 0, 4, "
            "8 and 12 and every four weeks after; the primary endpoint is PASI 75 at week 16. First patient in is "
            "planned for April 2027."]),
        ("7.2 The phase 3 dose", [
            "Phase 3 takes forward one dose, the lowest of 50, 100 and 200 mg whose expected PASI 75 response at "
            "week 16 in the phase 3 population is at least 70 per cent, response defined as in the VELA-2 "
            "statistical analysis plan.",
            "The phase 3 population is the patients the VELA-3 sites will enrol, as the site feasibility survey "
            "lists them."]),
        ("7.3 Decision", [
            "Clinical Pharmacology and Biostatistics prepare the dose recommendation from the locked VELA-2 data. "
            "The Board approves the phase 3 plan, the dose included, at its December 2026 meeting."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    doc.build(s, onFirstPage=_footer("HB-231 CDP v2.1  |  " + ORG), onLaterPages=_footer("HB-231 CDP v2.1  |  " + ORG))
    PP.normalize_pdf(path, b"D:20260528101200+02'00'", b"D:20260604170500+02'00'", "Clinical Development")


def email(path):
    text = """From: Villads Kjaer <vkj@%(d)s>
To: Clinical Pharmacology and Biometrics <cpb@%(d)s>
Cc: Helle Carlsen <hca@%(d)s>, Bodil Lauritsen <bla@%(d)s>
Date: Mon, 16 Nov 2026 08:41:17 +0100
Subject: HB-231 phase 3 dose for the December Board
Message-ID: <20261116084117.5521.vkj@%(d)s>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Hi all,

The Board takes the VELA-3 plan on 9 December and the papers close on
2 December, so I need the dose recommendation by then. The plan's
section 7 sets the rule. The locked VELA-2 exports and the feasibility
survey Clinical Operations closed on 30 October are in the folder.

Helle wants the VELA-2 tables in the same pack so the Board sees what
the trial showed.

Thanks,
Villads

--
Villads Kjaer
HB-231 Programme Lead
Hvidore Biologics A/S
""" % {"d": DOMAIN}
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
