"""The bundle's document: Network Policy NP-31, Prescriber Service Area Designation (approved May 2026)."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d2226")
GREY = colors.HexColor("#5b6268")
TEAL = colors.HexColor("#1f5560")
BODY = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("n", parent=BODY, leftIndent=28, firstLineIndent=-28)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=15, leading=19, textColor=TEAL, spaceAfter=2)
SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9, leading=12.4, textColor=GREY, spaceAfter=12)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=TEAL, spaceBefore=9,
                    spaceAfter=3)
CELL = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.4, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="LiberationSans-Bold")


def _doc(path):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 11 * mm, "%s Network Policy %s, %s. Approved 21 May 2026." % (W.ORG, W.POLICY_ID,
                                                                                                 W.POLICY_TITLE))
        canvas.drawRightString(letter[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm,
                          bottomMargin=20 * mm, title="%s %s" % (W.POLICY_ID, W.POLICY_TITLE), author=W.ORG,
                          subject="", creator="", producer="")
    return d, frame


def _codes_table(rows, widths):
    t = Table([[Paragraph(a, CELLB if i == 0 else CELL) for a in r] for i, r in enumerate(rows)], colWidths=widths,
              repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, TEAL), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY)]))
    return t


def write_policy(path):
    d, frame = _doc(path)
    P = lambda t: Paragraph(t, NUM)
    smi_f2 = ", ".join(c for c in W.SMI_CODES if c.startswith("F2"))
    smi_f3 = ", ".join(c for c in W.SMI_CODES if c.startswith("F3"))
    oud = ", ".join(W.OUD_CODES)
    story = [
        Paragraph("Network Policy %s: %s" % (W.POLICY_ID, W.POLICY_TITLE), H1),
        Paragraph("%s. Owner: %s. Approved by the Board of Directors on 21 May 2026 for the %s, 2027 to 2029. "
                  "Supersedes no earlier policy." % (W.ORG, W.TEAM, W.PILOT), SUB),
        Paragraph("1. Purpose", H2),
        P("1.1&nbsp;&nbsp;The %s offers loan repayment to behavioral-health prescribers who commit to three years of "
          "practice in a designated county. This policy sets how the plan designates the counties of its service area "
          "where the awards are offered: Adams, Benton, Chelan, Douglas, Franklin, Grant, Kittitas, Okanogan, Walla Walla "
          "and Yakima." % W.PILOT),
        P("1.2&nbsp;&nbsp;Network Development prepares the designation for the board each autumn, from the contract year "
          "that ended on the previous 30 June. The board approves the designated counties with the pilot's budget."),
        Paragraph("2. Definitions", H2),
        P("2.1&nbsp;&nbsp;<i>Contract year</i>: 1 July 2025 to 30 June 2026, the plan's contract year under its Apple "
          "Health integrated managed care contract."),
        P("2.2&nbsp;&nbsp;<i>Adult member</i>: a person enrolled with the plan on at least one day of the contract year (the "
          "plan enrolls adults aged 19 and over). A person counts once however many member numbers the plan has issued "
          "them; the client identifier on the enrollment record identifies the person."),
        P("2.3&nbsp;&nbsp;<i>A member's county</i>: the county of residence on the enrollment record that covers the "
          "member's last day of enrollment in the contract year."),
        P("2.4&nbsp;&nbsp;<i>Serious mental illness</i> and <i>opioid use disorder</i>: the conditions whose diagnosis codes "
          "Appendix A lists. A claim or encounter identifies a member's condition when it carries a listed code in any "
          "diagnosis position for a service rendered to the member in the contract year. A claim that a later claim "
          "replaces, and a voided claim, identify nothing; the replacing claim does."),
        P("2.5&nbsp;&nbsp;<i>Adult members with a serious mental illness</i> (or <i>with an opioid use disorder</i>): the "
          "county's adult members who have the condition. A member who has the condition counts whether or not a claim or "
          "encounter in the contract year identifies it. Network Analytics estimates the number of members with each "
          "condition in each county from the plan's enrollment, claims and encounter records, and measures each county "
          "from its own members."),
        P("2.6&nbsp;&nbsp;<i>Behavioral-health prescriber</i>: a clinician whose primary taxonomy in NPPES on 1 November 2026 "
          "is one of the codes Appendix B lists, or, for an NPI deactivated by that day, whose primary taxonomy was one of "
          "them before its deactivation. NPPES on 1 November 2026 means the monthly file as the weekly incremental files "
          "update it, record by record, through that day."),
        P("2.7&nbsp;&nbsp;<i>Practising behavioral-health prescriber</i> in a county: a behavioral-health prescriber whose "
          "NPI is active on 1 November 2026, whose practice location on that day is in the county, and who is the rendering "
          "provider of at least one claim or encounter for a service to an adult member in the contract year. The practice "
          "location is the NPPES business practice location address, not the mailing address. Its county is the county "
          "holding the larger share of the ZIP code's business addresses in the HUD-USPS ZIP-county crosswalk for the "
          "second quarter of 2026."),
        P("2.8&nbsp;&nbsp;<i>Visit with a behavioral-health prescriber</i>: a service Appendix C lists, rendered by a "
          "behavioral-health prescriber, in person or by telehealth, wherever the prescriber practises."),
        Paragraph("3. Standards", H2),
        P("3.1&nbsp;&nbsp;Each county is measured against three standards over the contract year:"),
        P("(a)&nbsp;&nbsp;<i>Prescribers for serious mental illness</i>: practising behavioral-health prescribers in the "
          "county per 1,000 adult members with a serious mental illness. Threshold: 16.5."),
        P("(b)&nbsp;&nbsp;<i>Prescribers for opioid use disorder</i>: practising behavioral-health prescribers in the county "
          "per 1,000 adult members with an opioid use disorder. Threshold: 23.0."),
        P("(c)&nbsp;&nbsp;<i>Prescriber reach</i>: the share of the county's adult members with a serious mental illness who "
          "had at least one visit with a behavioral-health prescriber in the contract year. Threshold: 68 per cent."),
        P("3.2&nbsp;&nbsp;A county fails a standard when its value is below the threshold. Values are compared with the "
          "thresholds unrounded."),
        Paragraph("4. Designation", H2),
        P("4.1&nbsp;&nbsp;A county is designated when it fails at least two of the three standards."),
        P("4.2&nbsp;&nbsp;A designation holds for the pilot's three years. A county not designated for 2027 may be "
          "designated in a later year under the standards then in force."),
        Paragraph("5. Records", H2),
        P("5.1&nbsp;&nbsp;The enrollment spans of the plan's enrollment system; the claims and encounters of the plan's "
          "claims system for services in the contract year, paid or accepted through 31 October 2026; NPPES, as published "
          "by the Centers for Medicare &amp; Medicaid Services; and the HUD-USPS ZIP-county crosswalk."),
        P("5.2&nbsp;&nbsp;Network Analytics keeps the extracts it used, as pulled, with the designation for the pilot's three "
          "years."),
        Paragraph("6. Awards", H2),
        P("6.1&nbsp;&nbsp;In each designated county the pilot offers up to four awards a year. An award repays up to $45,000 "
          "of qualifying education loans over three years to a behavioral-health prescriber who practises at least 24 hours "
          "a week in the county and keeps a panel open to the plan's members."),
        P("6.2&nbsp;&nbsp;A prescriber already practising in a designated county may apply. Awards are paid in arrears each "
          "contract year, after Network Development confirms the practice hours and the prescriber's claims and encounters "
          "for the plan's members in the county."),
        P("6.3&nbsp;&nbsp;Awards are funded from the plan's community reinvestment budget as the board approves it with the "
          "designation."),
        Paragraph("7. Responsibilities", H2),
        P("7.1&nbsp;&nbsp;Network Analytics prepares each county's measures from the records in section 5 and documents "
          "the extracts it used."),
        P("7.2&nbsp;&nbsp;Network Development reviews the measures, prepares the board paper and notifies the contracted "
          "behavioral health agencies and practices in the designated counties."),
        P("7.3&nbsp;&nbsp;The Chief Medical Officer presents the designation to the board."),
        Paragraph("8. Review", H2),
        P("8.1&nbsp;&nbsp;Network Development reviews this policy before the designation for 2030, with the pilot's results "
          "for its first two years."),
        Spacer(1, 6),
        Paragraph("Appendix A. Diagnosis codes (ICD-10-CM)", H2),
        _codes_table([["Condition", "Codes"],
                      ["Serious mental illness", "Schizophrenia spectrum and other psychotic disorders: %s. Bipolar "
                       "disorders and major depressive disorder, severe, with psychotic features: %s." % (smi_f2, smi_f3)],
                      ["Opioid use disorder", "Opioid abuse and opioid dependence: %s." % oud]],
                     [40 * mm, 132 * mm]),
        Spacer(1, 6),
        Paragraph("Appendix B. Behavioral-health prescriber taxonomy codes", H2),
        _codes_table([["Code", "Classification and specialization"]] +
                     [[k, v] for k, v in W.BH_TAXONOMY.items()], [32 * mm, 140 * mm]),
        Spacer(1, 6),
        Paragraph("Appendix C. Visit services", H2),
        _codes_table([["Codes", "Service"],
                      ["99202 to 99205", "Office or other outpatient visit, new patient"],
                      ["99211 to 99215", "Office or other outpatient visit, established patient"],
                      ["90791", "Psychiatric diagnostic evaluation"],
                      ["90792", "Psychiatric diagnostic evaluation with medical services"],
                      ["Telehealth", "Any code above billed with modifier 95 or with place of service 02 or 10"]],
                     [52 * mm, 120 * mm]),
    ]
    d.build(story, onFirstPage=frame, onLaterPages=frame)
