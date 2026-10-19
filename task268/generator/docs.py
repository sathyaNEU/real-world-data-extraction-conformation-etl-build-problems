"""The pack's documents: the service line committee's charter for the 2027 heart failure early-diagnosis programme, the
heart failure registry's manual (version 5) and the pack's contents list."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
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
INK, GREY, RULE = colors.HexColor("#1c2428"), colors.HexColor("#5a646b"), colors.HexColor("#b4bdc3")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=10, leading=13.8, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.8, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.6, leading=11.6, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.4, leading=10.6, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.4, leading=10.6, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.6)
        canvas.drawString(19 * mm, letter[1] - 11.5 * mm, left)
        canvas.drawRightString(letter[0] - 19 * mm, letter[1] - 11.5 * mm, right)
        canvas.drawRightString(letter[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


# ---------------------------------------------------------------------------------------------- the charter
def write_charter(path):
    S = styles("Sans", colors.HexColor("#0E5A6E"))
    doc = _doc(path, "Heart Failure Early Diagnosis Programme 2027: Charter", K.ORG_INC)
    st = [Paragraph("Heart Failure Early Diagnosis Programme 2027", S["h1"]),
          Paragraph("Charter of the %s, %s. Approved at the committee's meeting of 17 February 2026." % (K.COMMITTEE, K.ORG),
                    S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    Hd = lambda t: st.append(Paragraph(t, S["h2"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    Hd("1. Purpose")
    P("Most heart failure in the communities our hospitals serve is still diagnosed during an emergency admission, when "
      "the disease is already advanced. The programme moves diagnosis earlier and out of hospital: primary care "
      "practices test patients with breathlessness, swollen ankles or unexplained fatigue for NT-proBNP, and a "
      "rapid-access heart failure clinic sees the patients the test points to, with echocardiography the same week.")
    Hd("2. The programme")
    C("2.1", "Community testing. Participating primary care practices in the host hospital's service area order "
             "NT-proBNP through the host hospital's laboratory, on the programme's request form.")
    C("2.2", "Rapid-access clinic. An advanced practice provider and a cardiac sonographer run three clinic sessions a "
             "week at the host hospital, with a cardiologist's review of every new diagnosis.")
    C(K.CHARTER_CLAUSES["referral"], "Referral. A patient whose NT-proBNP is at or above %d pg/mL is referred to the rapid-access clinic and seen "
             "within two weeks; below that level the practice manages the patient and re-tests if symptoms persist."
      % K.REFERRAL)
    C("2.4", "Resources. The first year is funded at $1.42 million: the clinic staff, the echocardiography sessions, a "
             "programme coordinator and the practices' testing.")
    Hd("3. Choosing the host hospital")
    C(K.CHARTER_CLAUSES["host"], "The programme starts at one hospital in April 2027. It goes to the hospital whose patients newly diagnosed "
             "with heart failure in 2022 and 2023 had the lowest two-year survival from diagnosis: survival from "
             "diagnosis is shortest where heart failure is found latest, and that is where finding it earlier has the "
             "most to give.")
    C(K.CHARTER_CLAUSES["survival"], "Two-year survival is the share of the hospital's patients newly diagnosed with heart failure in 2022 and "
             "2023 who were alive two years after their diagnosis date. Every patient newly diagnosed at the hospital in "
             "those years counts, including patients the registry no longer follows.")
    C("3.3", "The figures come from the %s, whose manual (section 2) sets out who is newly diagnosed and at which "
             "hospital." % K.REGISTRY)
    Hd("4. Timeline")
    P("The committee chooses the host hospital at its May 2026 meeting. Practices are recruited from September 2026, "
      "the clinic opens in March 2027 and the first community referrals are expected in April 2027.")
    Hd("5. Review")
    P("The committee reviews the programme after its first twelve months: the practices taking part, the tests ordered, "
      "the referrals made, the diagnoses reached and how many of them were made outside an emergency admission. A "
      "second hospital is considered at that review.")
    st.append(Spacer(1, 8))
    P("<i>Chair of the committee: %s, Medical Director, Heart and Vascular Services.</i>" % K.PEOPLE["director"])
    frame = _frame(K.ORG + "  |  " + K.COMMITTEE, "Charter, approved 17 February 2026", "Sans")
    doc.build(st, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the registry manual
def write_manual(path):
    S = styles("Serif", colors.HexColor("#33415C"))
    doc = _doc(path, "Heronmere Heart Failure Registry: manual, version 5", K.ORG_INC)
    st = [Paragraph(K.REGISTRY + ": Manual", S["h1"]),
          Paragraph("Version 5, 3 March 2025. Replaces version 4 (August 2023). Maintained by the registry team, "
                    "Heart and Vascular Services, %s." % K.ORG, S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    Hd = lambda t: st.append(Paragraph(t, S["h2"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    Hd("1. About the registry")
    P("The registry has enrolled every patient newly diagnosed with heart failure at a Heronmere hospital since 1 January "
      "2022. It follows them in the hospitals' heart failure clinics and records their deaths, so that the service line "
      "can see how its patients fare and plan its services.")
    Hd("2. Enrolment")
    C(K.MANUAL_SECTIONS["enrolment"], "A patient is enrolled when heart failure is first diagnosed at a Heronmere hospital, in an admission, in "
             "an emergency department visit or in an outpatient clinic. The diagnosis date is the date of that "
             "encounter. The enrolment date is the date the registry nurse entered the patient, within three weeks "
             "after the diagnosing encounter.")
    C(K.MANUAL_SECTIONS["hospital"], "The hospital is the hospital of the diagnosing encounter. The North Campus of Brenmoor Regional Medical "
             "Center used the main campus's code (BRE) until 1 July 2024 and its own code (BRN) from that date; both "
             "campuses are Brenmoor Regional Medical Center.")
    C("2.3", "The registry nurse records the NYHA functional class at diagnosis, the ejection fraction category (reduced, "
             "mildly reduced, preserved) and the setting of the diagnosing encounter.")
    Hd("3. Clinic follow-up")
    C("3.1", "Enrolled patients are seen in the heart failure clinic of their hospital about every three months. At each "
             "visit the clinician records the NYHA functional class, weight, blood pressure, heart rate and the daily "
             "loop diuretic dose.")
    C(K.MANUAL_SECTIONS["spelling"], "The legacy record writes the NYHA class as I to IV or as Class I to Class IV; the new record, from 1 June "
             "2024, writes it as 1 to 4 or as NYHA 1 to NYHA 4. The diagnosis setting is IP, OP or ED in the legacy "
             "record and Inpatient (or INPT), Outpatient or ED visit in the new one.")
    C(K.MANUAL_SECTIONS["relocation"], "A patient who tells the clinic that they are moving out of Florida is recorded as a relocation (event REL), "
             "with the state they are moving to, when the registry processes the note of that visit, a few days later. "
             "The clinic does not see them again.")
    Hd("4. Vital status")
    C(K.MANUAL_SECTIONS["florida"], "Deaths in Florida are found by the state's death certificate linkage, run each March on the record numbers "
             "of the patients in follow-up. The linkage returns one row for each linked death, under the patient's "
             "current record number.")
    C(K.MANUAL_SECTIONS["exchange"], "Deaths of patients who have moved to Georgia, Alabama or South Carolina are returned each quarter by the "
             "%s, under the registry identifier." % K.EXCHANGE)
    C(K.MANUAL_SECTIONS["no_source"], "The registry has no source for deaths in any other state. A patient who moves to any other state leaves "
             "vital status follow-up on the date of the relocation, and the registry holds nothing on them after it.")
    C(K.MANUAL_SECTIONS["reconsent"], "The registry is re-consenting the patients Wrenhaven Medical Center enrolled before 2024, after a change "
             "to that hospital's data-sharing agreement. A patient who has not returned the new consent form by %s "
             "leaves follow-up that day (event CNR), and the registry holds nothing on them after it."
      % K.RECONSENT.strftime("%-d %B %Y"))
    Hd("5. Record numbers")
    P("On 1 June 2024 Heronmere moved to a new electronic health record and every patient was given a new medical record "
      "number. The registry keeps the number under which each patient was enrolled. The record-number crosswalk maps "
      "each legacy number to the patient's new number.")
    Hd("6. Files")
    rows = [["File", "One row is", "Key fields"],
            [K.FILES["patients"], "an enrolment", "registry_id, mrn (the number at enrolment), hospital, diagnosis_date, "
                                                 "enrolment_date, nyha_at_diagnosis, diagnosis_setting"],
            [K.FILES["visits"], "a heart failure clinic visit", "registry_id, visit_date, clinic, nyha_class"],
            [K.FILES["events"], "a relocation or a consent withdrawal", "registry_id, event_date, event (REL, CNR), "
                                                                       "destination_state"],
            [K.FILES["fl_deaths"], "a linked Florida death", "MRN (current), date of death"],
            [K.FILES["exchange"], "a death returned by the exchange", "PARTNER_ID (the registry identifier), STATE, DOD"],
            [K.FILES["crosswalk"], "a legacy record number", "legacy_mrn, new_mrn"]]
    st.append(_table(S, rows, (58, 38, 82)))
    frame = _frame(K.REGISTRY, "Manual, version 5", "Serif")
    doc.build(st, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- contents
def write_contents(path, rows):
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    lines = ["Committee pack: 2027 Heart Failure Early Diagnosis Programme, host hospital",
             "Prepared for the %s, %s" % (K.COMMITTEE, K.PACK_DATE.strftime("%d %B %Y").lstrip("0")), ""]
    for i, r in enumerate(rows):
        lines.append("  ".join(str(c).ljust(widths[j]) for j, c in enumerate(r)).rstrip())
        if i == 0:
            lines.append("  ".join("-" * w for w in widths))
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")
