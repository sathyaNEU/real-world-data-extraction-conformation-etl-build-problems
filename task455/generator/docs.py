"""The pack's document: the Overdose Reduction Initiative grant agreement between the Wendmoor Valley Recovery
Foundation and Wendmoor County (signed 22 January 2024), with Schedule B, the outcome measure and certification."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1b1b")
GREY = colors.HexColor("#555555")
BODY = ParagraphStyle("b", fontName="LiberationSerif", fontSize=10.6, leading=14.4, textColor=INK, spaceAfter=7)
NUM = ParagraphStyle("n", parent=BODY, leftIndent=30, firstLineIndent=-30)
TITLE = ParagraphStyle("t", fontName="LiberationSerif-Bold", fontSize=13.5, leading=17.5, textColor=INK, alignment=1,
                       spaceAfter=4)
SUB = ParagraphStyle("s", fontName="LiberationSerif", fontSize=10.6, leading=14, textColor=INK, alignment=1, spaceAfter=14)
H2 = ParagraphStyle("h2", fontName="LiberationSerif-Bold", fontSize=11, leading=14.5, textColor=INK, spaceBefore=8,
                    spaceAfter=4)
CELL = ParagraphStyle("c", fontName="LiberationSerif", fontSize=10, leading=13, textColor=INK)
REF = "ORI-2024-01"


def _doc(path):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSerif", 8.6)
        canvas.setFillColor(GREY)
        canvas.drawString(25 * mm, 12 * mm, "Grant Agreement %s, %s and Wendmoor County" % (REF, W.FOUNDATION))
        canvas.drawRightString(letter[0] - 25 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=25 * mm, rightMargin=25 * mm, topMargin=22 * mm,
                          bottomMargin=22 * mm, title="Grant Agreement %s" % REF, author=W.FOUNDATION, subject="",
                          creator="", producer="")
    return d, frame


def write_agreement(path):
    d, frame = _doc(path)
    P = lambda t: Paragraph(t, NUM)
    s = []
    s.append(Paragraph("GRANT AGREEMENT %s" % REF, TITLE))
    s.append(Paragraph("between the %s and Wendmoor County, acting through its Department of Public Health<br/>"
                       "%s" % (W.FOUNDATION, W.INITIATIVE), SUB))
    s.append(Paragraph("This agreement is made on 22 January 2024 between the %s (the Foundation), which holds Wendmoor "
                       "County's share of the statewide opioid settlement under the settlement's county allocation, and "
                       "Wendmoor County, acting through the %s (the Department)." % (W.FOUNDATION, W.ORG), BODY))
    s.append(Paragraph("Article 1. Purpose", H2))
    s.append(P("1.1&nbsp;&nbsp;The Foundation funds the %s to reduce deaths of Wendmoor County residents from opioid "
               "overdoses. The initiative runs in two phases, the second released on the outcome of the first." % W.INITIATIVE))
    s.append(Paragraph("Article 2. Term and phases", H2))
    s.append(P("2.1&nbsp;&nbsp;Phase one runs from 1 January 2024 to 31 December 2026."))
    s.append(P("2.2&nbsp;&nbsp;Phase two runs from 1 July 2027 to 30 June 2030, released under Article 5."))
    s.append(Paragraph("Article 3. Award", H2))
    s.append(P("3.1&nbsp;&nbsp;The Foundation awards $4,200,000 for phase one, paid in twelve quarterly instalments of $350,000."))
    s.append(P("3.2&nbsp;&nbsp;The Foundation reserves up to $6,600,000 for phase two, paid as $2,200,000 for each year of "
               "phase two once that year is released."))
    s.append(Paragraph("Article 4. Use of funds", H2))
    s.append(P("4.1&nbsp;&nbsp;The Department spends the award on the activities in Schedule A and reports them quarterly "
               "in the form the Foundation provides."))
    s.append(Paragraph("Article 5. Release of phase two", H2))
    s.append(P("5.1&nbsp;&nbsp;The Foundation's trustees decide the release of phase two at their first meeting after "
               "they receive the Department's certification under Schedule B, applying Schedule B5."))
    s.append(P("5.2&nbsp;&nbsp;The certification is the Department's. The Foundation may ask the Department for the "
               "records behind it and may have them reviewed at its own cost."))
    s.append(Paragraph("Article 6. Records and data", H2))
    s.append(P("6.1&nbsp;&nbsp;The Department obtains the state death file extracts, the medical examiner's review and "
               "the county EMS data it needs under its existing data sharing agreements with the State Office of Vital "
               "Records, the State Office of the Medical Examiner and the Wendmoor County EMS Data System, and keeps "
               "them for six years after the end of phase two."))
    s.append(P("6.2&nbsp;&nbsp;Nothing in this agreement gives the Foundation access to identifiable records."))
    s.append(Paragraph("Article 7. General", H2))
    s.append(P("7.1&nbsp;&nbsp;This agreement may be amended only in writing signed by both parties. It is governed by "
               "the laws of the state."))
    s.append(Spacer(1, 8))
    sig = Table([[Paragraph("For the %s<br/><br/>Jesse Mcdonald, Director of Grants<br/>22 January 2024" % W.FOUNDATION, CELL),
                  Paragraph("For Wendmoor County<br/><br/>Director of Public Health<br/>22 January 2024", CELL)]],
                colWidths=[80 * mm, 80 * mm])
    sig.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEABOVE", (0, 0), (-1, 0), 0.5, GREY),
                             ("TOPPADDING", (0, 0), (-1, -1), 6)]))
    s.append(sig)
    s.append(PageBreak())
    s.append(Paragraph("Schedule A. Phase one activities", H2))
    for t in ("A1&nbsp;&nbsp;Naloxone distribution through pharmacies under the standing order, community sites, "
              "the county jail at release and EMS leave-behind kits.",
              "A2&nbsp;&nbsp;Treatment navigation for people seen by EMS or in an emergency department after an "
              "overdose, with peer recovery coaches.",
              "A3&nbsp;&nbsp;Medications for opioid use disorder at the county jail and in two community clinics.",
              "A4&nbsp;&nbsp;Overdose surveillance by the Department: the state death file, the medical examiner's "
              "review under Schedule B3 and the county EMS data."):
        s.append(P(t))
    s.append(Paragraph("Schedule B. Outcome measure and certification", H2))
    s.append(P("B1&nbsp;&nbsp;The outcome for a calendar year is the number of residents of Wendmoor County who died in "
               "that year, wherever they died, of a drug overdose that an opioid caused or contributed to. A drug "
               "overdose death is a death whose underlying cause on the state death file is a drug poisoning (ICD-10 "
               "X40 to X44, X60 to X64, X85 or Y10 to Y14). An opioid caused or contributed to a death when a full "
               "medical examiner review of the case would find an opioid among the drugs that caused or contributed "
               "to it, whether or not the death certificate names the opioid."))
    s.append(P("B2&nbsp;&nbsp;The baseline is the average of the outcome for 2021, 2022 and 2023."))
    s.append(P("B3&nbsp;&nbsp;The county's drug overdose deaths are certified by the Wendmoor County Coroner, and a death "
               "certificate may name no drug or name a drug that did not cause the death. The Department will ask the "
               "State Office of the Medical Examiner to review every 2025 drug overdose death of a county resident on "
               "the state's 2025 file as closed, against the full case file and toxicology, and will estimate the "
               "outcome for every year it reports from the state death file, correcting the certificates by the "
               "classification error the review measures."))
    s.append(P("B4&nbsp;&nbsp;After the State Office of Vital Records closes the 2026 file, the Department extracts "
               "the state death file and certifies to the Foundation the outcome for 2026 and for each baseline year, "
               "as the file stands at the extract, before the trustees' June 2027 meeting."))
    s.append(P("B5&nbsp;&nbsp;If the certified outcome for 2026 is at least 20 per cent below the baseline, the "
               "Foundation releases phase two. If it is below the baseline by less than 20 per cent, the Foundation "
               "releases the first year of phase two and the Department certifies the outcome again for 2027. If it "
               "is not below the baseline, the grant ends at the close of phase one."))
    s.append(P("B6&nbsp;&nbsp;With the certification the Department reports, for each quarter from 2021, the non-fatal "
               "opioid overdoses of county residents treated by emergency medical services: patient encounters in "
               "which an EMS unit gave naloxone or recorded an impression of poisoning by an opioid (an ICD-10-CM "
               "poisoning code under T40.0 to T40.4 or T40.6), and the patient was alive when EMS care ended, each counted in the quarter of the "
               "call. The secondary measure does not enter the decision in B5."))
    d.build(s, onFirstPage=frame, onLaterPages=frame)
