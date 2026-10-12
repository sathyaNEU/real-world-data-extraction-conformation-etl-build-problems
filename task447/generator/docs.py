"""The filed documents: the office's projection rule, its market oversight technical appendix, the
APCD data dictionary, and notice N25-014 with its exhibits A and B. Each is short and written the way
the office or the filer would write it. PDFs are made reproducible (fixed dates and document id) and
carry no toolchain signature.
"""
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import orgs as O
import world as W

RULE = "ohccr_rule_4_preliminary_review.pdf"
APPENDIX = "market_oversight_technical_appendix.pdf"
DICTIONARY = "apcd_extract_data_dictionary.pdf"
NOTICE = "N25-014_notice_of_material_change.pdf"

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Times-Roman", fontSize=10.5, leading=13.6,
                      spaceAfter=5)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.5, leading=10.5, spaceAfter=3)
HEAD = ParagraphStyle("head", parent=BODY, fontName="Times-Bold", fontSize=13, leading=16, alignment=TA_CENTER,
                      spaceAfter=2)
SUBHEAD = ParagraphStyle("subhead", parent=BODY, fontName="Times-Roman", fontSize=10, alignment=TA_CENTER,
                         spaceAfter=10)
SEC = ParagraphStyle("sec", parent=BODY, fontName="Times-Bold", fontSize=10.5, spaceBefore=5, spaceAfter=2)
CELL = ParagraphStyle("cell", parent=BODY, fontName="Helvetica", fontSize=7.6, leading=9.2, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")


def _scrub(path, created, docid):
    """Same-length replacements, so the cross-reference offsets stay valid."""
    b = open(path, "rb").read()

    def same(m, new):
        old = m.group(0)
        return new.ljust(len(old))[:len(old)]
    b = re.sub(rb"ReportLab Generated PDF document \(opensource\)", lambda m: same(m, b"Microsoft Print To PDF"), b)
    b = re.sub(rb"ReportLab generated PDF document -- digest \(opensource\)", lambda m: same(m, b"end"), b)
    b = re.sub(rb"\(anonymous\)", lambda m: same(m, b"(OHCCR)"), b)
    b = b.replace(b"D:20000101000000+00'00'", created.encode())
    b = re.sub(rb"(/ID\s*\[\s*)<[0-9A-Fa-f]{32}>(\s*)<[0-9A-Fa-f]{32}>",
               lambda m: m.group(1) + b"<" + docid.encode() + b">" + m.group(2) + b"<" + docid.encode() + b">", b)
    assert b"ReportLab" not in b and b"reportlab" not in b
    open(path, "wb").write(b)


def _doc(path, flow, title, author, created, docid, creator="Microsoft Word"):
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
                            topMargin=0.85 * inch, bottomMargin=0.85 * inch, title=title, author=author,
                            subject="", creator=creator, producer="Microsoft: Print To PDF")
    doc.build(flow)
    _scrub(path, created, docid)


def _table(rows, widths, head=True, size=None):
    data = [[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
          ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")))
    t.setStyle(TableStyle(st))
    return t


# ------------------------------------------------------------------ rule OHCCR 4
def rule_pdf(path):
    P = lambda t: Paragraph(t, BODY)
    S = lambda t: Paragraph(t, SEC)
    flow = [Paragraph("OFFICE OF HEALTH CARE COST REVIEW", HEAD),
            Paragraph("Rule OHCCR 4. Preliminary review of notices of material change<br/>"
                      "Adopted 14 February 2023, effective 1 April 2023", SUBHEAD)]
    flow += [S("4.01 Scope"),
             P("This rule governs the office's preliminary review of a notice of material change in which a "
               "hospital system acquires a physician practice or the services of its physicians. It applies to "
               "notices that are complete on or after 1 April 2023."),
             S("4.02 Definitions"),
             P("In this rule: (a) <i>database</i> means the all-payer claims database the office administers; "
               "(b) a <i>commercial</i> product is one the database's product reference lists with line of business "
               "Commercial, fully insured or self-funded; (c) <i>spending</i> means the allowed amount on a claim "
               "line, being the plan's payment and the member's cost sharing together, taken on the latest version "
               "of the line and net of voids; (d) the <i>target practice</i> is the practice whose physicians the "
               "notice transfers and the <i>acquiring party</i> is the hospital system that receives them; (e) a "
               "<i>physician of a practice</i> is a physician billing under one of the practice's taxpayer "
               "identification numbers on the date of service; (f) a <i>referred service</i> of a practice is a "
               "service on the database's outpatient facility claims whose referring provider is a physician of "
               "the practice; (g) a system <i>offers</i> a service when its outpatient sites bill that procedure "
               "code; (h) the <i>projection year</i> is the first full calendar year after the transaction closes."),
             S("4.03 Baseline"),
             P("The baseline year is the most recent calendar year whose claims the database holds paid at least six "
               "months after its end on the date the notice is complete. The baseline services of a target practice "
               "are its commercial professional services billed under its taxpayer identification numbers and its "
               "commercial referred services, in each case with dates of service in the baseline year and paid on or "
               "before 30 June of the following year. Baseline spending is the spending on those services."),
             S("4.04 Projected spending"),
             P("The office projects every baseline service as the same service, for the same member under the same "
               "product, delivered in the projection year. Prices and volumes are not trended. In the projection:"),
             P("(a) the professional services are priced at the acquiring party's professional rates filed with the "
               "notice;"),
             P("(b) a referred service that the acquiring party offers, and that was not at one of the acquiring "
               "party's sites in the baseline, moves to the acquiring party's sites in the share expected for that "
               "service in the projection year, estimated under 4.05; the part that moves is priced at the acquiring "
               "party's facility rate filed with the notice and the rest keeps its baseline allowed amount;"),
             P("(c) every other referred service keeps its baseline allowed amount."),
             P("Projected spending is the spending on the baseline services so projected."),
             S("4.05 Expected share that moves"),
             P("The office estimates the share expected to move from the database's referred services of the "
               "physicians who joined health systems in the state by acquisition, as the market oversight unit's "
               "technical appendix defines joining, where the database holds their referred services both before "
               "and after the acquisition. A service falls before or after by its date of service against the date "
               "its referring physician joined, and only the services offered by the system he or she joined are "
               "counted. The share that moves is the rise, after the acquisition, in the share of those services at "
               "the acquiring system, as a share of the services that were elsewhere before it. The office states "
               "each expected share in whole per cent and projects with the shares as stated."),
             S("4.06 Determination"),
             P("The projected increase is projected spending less baseline spending. Where the projected increase "
               "is $2,000,000 or more, the office proceeds to a cost and market impact review under rule OHCCR 5. "
               "Otherwise the office closes the preliminary review and so informs the parties and the Attorney "
               "General."),
             S("4.07 Record"),
             P("The preliminary review states the projected increase, its professional and referred parts, and the "
               "exhibits the market oversight unit maintains in its technical appendix."),
             S("4.08 Timing"),
             P("The office completes the preliminary review within 30 days of a complete notice. The period is not "
               "extended."),
             Spacer(1, 8),
             Paragraph("History: Cr. Register February 2023, effective 1 April 2023. Statutory authority: s. 153.85.",
                       SMALL)]
    _doc(path, flow, "Rule OHCCR 4", "OHCCR Legal", "D:20230214101500-06'00'", "4F1C2A9B7E06D3518C2B90E4A6D7F213")


# ------------------------------------------------------------------ technical appendix
def appendix_pdf(path):
    P = lambda t: Paragraph(t, BODY)
    S = lambda t: Paragraph(t, SEC)
    flow = [Paragraph("Market Oversight Unit", HEAD),
            Paragraph("Technical appendix to preliminary reviews, revision 3, 2 June 2025", SUBHEAD)]
    flow += [P("This appendix fixes how the unit computes the standing exhibits of a preliminary review. Terms "
               "defined in rule OHCCR 4 carry the same meaning here."),
             S("A1 Service lines"),
             P("Imaging is CPT 70010 to 76999 and 77046 to 77067; echocardiography is CPT 93303 to 93356; "
               "gastrointestinal endoscopy is CPT 43235 to 43270 and 45378 to 45398; arthroscopy is CPT 29805 to "
               "29999; laboratory is CPT 80047 to 89398. Nuclear cardiology, sleep studies and other services fall "
               "in no line."),
             S("A2 Outpatient market share"),
             P("For a service line, a county and a year, a system's share is the services its facilities provided "
               "to commercial members residing in the county, divided by all the services in that line that any "
               "facility in the database provided to those members. A service is one unit of a procedure code: the "
               "quantity on the latest version of an outpatient facility claim line, net of voids. A member resides "
               "in the county holding the ZIP code on the member's eligibility span that covers the date of service. "
               "The year is dates of service in the calendar year paid on or before 30 June of the following year. "
               "Shares are stated in per cent to one decimal."),
             S("A3 Share after a transaction"),
             P("A system's share after a transaction is computed as in A2 on the baseline year's services, with the "
               "target practice's referred services that the projection under rule OHCCR 4 moves to the acquiring "
               "party counted, in their expected share, as the acquiring party's. All other services, and the "
               "totals, are unchanged."),
             S("A4 A system's physicians"),
             P("A physician is a doctor of medicine or of osteopathic medicine; nurse practitioners and physician "
               "assistants are not counted. A system's physicians on a date are the physicians billing on that "
               "date under a taxpayer identification number that the system owns or controls, directly or through "
               "an entity it owns or controls, as the register records it: relationships owned, merged into, and "
               "affiliated, controlled. Participation in a clinically integrated network is not control. A "
               "physician billing under several of the system's numbers is counted once."),
             S("A5 Physicians who join by acquisition"),
             P("A physician joins a system by acquisition when the physician comes to bill under the system's "
               "numbers together with the practice the physician billed under: either the practice comes under the "
               "system's ownership or control, or every physician of the practice moves to the system's numbers "
               "within 90 days of the first, leaving none billing under the practice's number. A physician already "
               "counted for the system who moves between its numbers has not joined. A physician joins in the "
               "calendar year of the date he or she first bills under the system's numbers."),
             S("A6 Sources"),
             P("Claims, eligibility and products come from the database extracts described in the extract data "
               "dictionary; ownership from the office's provider ownership register; billing relationships from "
               "the NPI reassignment history; credentials and taxonomy from the carriers' provider files.")]
    _doc(path, flow, "Technical appendix rev 3", "Samantha Abbott", "D:20250602141108-05'00'",
         "B71E04C9A35D2F68E0C1974AB3D85E20")


# ------------------------------------------------------------------ data dictionary
FAC24_DEF = [
    ("submitter_code", "Carrier's APCD submitter code (see product reference)."),
    ("payer_claim_control_number", "Carrier's claim number. A replacement or void carries its own number."),
    ("line_counter", "Line number within the claim."),
    ("claim_frequency_code", "1 original; 7 replacement of a prior claim; 8 void of a prior claim."),
    ("original_claim_control_number", "For codes 7 and 8, the claim number replaced or voided."),
    ("form_type", "UB04 (institutional) or CMS1500 (professional form, used by freestanding centres and laboratories)."),
    ("member_id", "APCD de-identified member key, stable across carriers."),
    ("product_id", "Carrier product (see product reference)."),
    ("service_from_date", "Date of service (YYYY-MM-DD)."),
    ("paid_date", "Date the line was adjudicated paid (YYYY-MM-DD)."),
    ("type_of_bill", "UB04 bill type."),
    ("place_of_service", "CMS place of service code (CMS1500 lines)."),
    ("revenue_code", "UB04 revenue code."),
    ("procedure_code", "CPT/HCPCS code."),
    ("procedure_modifier_1", "First modifier."),
    ("quantity", "Units of service. Negative on void lines."),
    ("allowed_amount", "Allowed amount for the line (plan paid plus member liability). Negative on void lines."),
    ("plan_paid_amount", "Amount paid by the plan."),
    ("member_liability_amount", "Deductible, copay and coinsurance."),
    ("billing_provider_npi", "NPI of the billing provider. Off-campus hospital departments bill under the hospital."),
    ("billing_provider_tin", "Billing provider's taxpayer identification number."),
    ("service_facility_npi", "NPI of the facility where the service was performed."),
    ("service_facility_zip", "ZIP code of that facility."),
    ("referring_provider_npi", "NPI of the referring or ordering provider."),
]
V2_MAP = [("SUBMITTER_ID", "submitter_code"), ("CLAIM_ID", "payer_claim_control_number"), ("LINE_NO", "line_counter"),
          ("CLM_STATUS", "claim frequency: O original, R replacement, V void"),
          ("ORIG_CLAIM_ID", "original_claim_control_number"), ("FORM", "UB (UB04) or CM (CMS1500)"),
          ("MEMBER_ID", "member_id"), ("PRODUCT_ID", "product_id"), ("DOS_FROM", "service_from_date (YYYYMMDD)"),
          ("PAID_DT", "paid_date (YYYYMMDD)"), ("TOB", "type of bill, three digits without the leading zero"),
          ("POS", "place_of_service"), ("REV_CD", "revenue_code"), ("PROC_CD", "procedure_code"),
          ("MOD1", "procedure_modifier_1"), ("UNITS", "quantity"), ("ALLOWED_AMT", "allowed_amount"),
          ("PLAN_PAID_AMT", "plan_paid_amount"), ("MBR_RESP_AMT", "member_liability_amount"),
          ("BILL_NPI", "billing_provider_npi"), ("BILL_TIN", "billing_provider_tin, nine digits, no hyphen"),
          ("FAC_NPI", "service_facility_npi (no facility ZIP in v2.4)"), ("REF_NPI", "referring_provider_npi")]
PROF_DEF = [
    ("place_of_service", "CMS place of service: 10 telehealth in the patient's home, 11 office, 22 on-campus "
                         "outpatient hospital, 24 ambulatory surgical centre."),
    ("procedure_modifier_1, _2", "Modifiers, for example 26 professional component, 95 synchronous telehealth."),
    ("billing_provider_npi, _tin, _zip", "The billing group's NPI, taxpayer number and billing address ZIP."),
    ("rendering_provider_npi, _taxonomy", "The individual who performed the service and his or her NUCC taxonomy."),
    ("service_facility_zip", "ZIP code of the location where the service was performed."),
]
TAXONOMY = [("207Q00000X", "Family Medicine"), ("207R00000X", "Internal Medicine"), ("208000000X", "Pediatrics"),
            ("207RG0100X", "Internal Medicine, Gastroenterology"), ("207X00000X", "Orthopaedic Surgery"),
            ("207RC0000X", "Internal Medicine, Cardiovascular Disease"), ("363L00000X", "Nurse Practitioner"),
            ("363A00000X", "Physician Assistant")]


def dictionary_pdf(path):
    P = lambda t: Paragraph(t, BODY)
    S = lambda t: Paragraph(t, SEC)
    flow = [Paragraph("Wisconsin All-Payer Claims Database", HEAD),
            Paragraph("Extract data dictionary, request OHCCR-MO-2025-031 (notice N25-014)", SUBHEAD)]
    flow += [S("1 The files"),
             P("<b>apcd_op_facility_claims_2024.csv</b> (layout 3.1): commercial and Medicare Advantage outpatient "
               "facility claims are held separately; this file holds the commercial lines, service category "
               "OP_FACILITY (hospital outpatient departments, ambulatory surgery centres, independent diagnostic "
               "testing facilities, sleep centres and clinical laboratories), for the facilities in the facility "
               "directory, dates of service 1 January to 31 December 2024, paid through 31 August 2025. Extract run "
               "15 September 2025."),
             P("<b>apcd_op_facility_claims_2021_2023.csv</b> (layout 2.4): commercial outpatient facility claims, "
               "dates of service 1 January 2021 to 31 December 2023, whose referring provider is a physician of a "
               "practice acquired by Ledgestone Health or Wolf River Health from 2021 to 2023, from the unit's "
               "acquisition review extract (run 12 August 2024, paid through 30 June 2024). The physicians' 2024 "
               "claims are in the 2024 file."),
             P("<b>apcd_professional_claims_2024.csv</b> (layout 3.1): commercial professional claims for services "
               "performed at locations in Manitowoc and Kewaunee counties, dates of service in 2024, paid through 31 "
               "August 2025."),
             P("<b>apcd_eligibility_spans.csv</b>: eligibility for every member with a line in the three claim "
               "files, 2021 to 2024. A span is cut at every change of product, of benefit period (the plan year, "
               "beginning on the date in benefit_period_begin) and of address. relationship_code: 18 subscriber, 01 "
               "spouse, 19 child."),
             P("<b>apcd_product_reference.csv</b>: one row per carrier product, with line of business and "
               "whether the product uses a tiered network."),
             S("2 Layout 3.1, outpatient facility claims"),
             _table([("Field", "Definition")] + FAC24_DEF, [1.9 * inch, 4.6 * inch]),
             Spacer(1, 4),
             P("Each line carries the version the carrier last submitted for it: a replacement (code 7) "
               "supersedes the claim it names, and a void (code 8) cancels the claim it names, its lines carrying "
               "negative quantities and amounts. The database does not remove superseded or voided lines."),
             S("3 Layout 3.1, professional claims"),
             P("Fields as in section 2 where the names agree, without form, bill type, revenue code and facility "
               "NPI, and with:"),
             _table([("Field", "Definition")] + PROF_DEF, [1.9 * inch, 4.6 * inch]),
             S("4 Layout 2.4 (2021 to 2023 extract)"),
             _table([("2.4 field", "3.1 equivalent")] + V2_MAP, [1.6 * inch, 4.9 * inch]),
             S("5 Provider taxonomy (NUCC) used in these files"),
             _table([("Code", "Classification")] + TAXONOMY, [1.6 * inch, 4.9 * inch]),
             S("6 ZIP codes and counties"),
             _table([("County", "ZIP codes")] + [(c, ", ".join(z)) for c, z in sorted(W.ZIPS.items())],
                    [1.6 * inch, 4.9 * inch]),
             Spacer(1, 6),
             Paragraph("Prepared by Samantha Abbott, APCD data manager, 16 September 2025. Member keys are "
                       "de-identified; do not attempt re-identification.", SMALL)]
    _doc(path, flow, "APCD extract data dictionary", "Samantha Abbott", "D:20250916093344-05'00'",
         "0D93B6E2F17A4C58B26E9D041F7C3A85")


# ------------------------------------------------------------------ notice N25-014
def notice_pdf(path, people, roster):
    P = lambda t: Paragraph(t, BODY)
    S = lambda t: Paragraph(t, SEC)
    flow = [Paragraph("NOTICE OF MATERIAL CHANGE", HEAD),
            Paragraph("Filed with the Office of Health Care Cost Review under s. 153.86", SUBHEAD)]
    info = [("Notice number", "N25-014"), ("Received", "8 October 2025 (complete on receipt)"),
            ("Filing party", "Ledgestone Health, 1400 Riverside Drive, Green Bay, WI 54301"),
            ("Other party", "Brightwater Medical Group, S.C., 820 Washington Street, Manitowoc, WI 54220"),
            ("Contact", "Jacob Murillo, counsel to Ledgestone Health"),
            ("Proposed closing", "1 January 2026")]
    flow.append(_table([("Item", "")] + info, [1.6 * inch, 4.9 * inch]))
    flow += [S("1 Description of the transaction"),
             P("Ledgestone Health will acquire the assets of Brightwater Medical Group, S.C. At closing, "
               "Brightwater's eighteen physicians become employees of Ledgestone Medical Group and bill under "
               "Ledgestone Medical Group's taxpayer identification number; Brightwater's number "
               "(%s) is retired. Brightwater's clinics in Manitowoc, Two Rivers and Kewaunee continue as physician "
               "offices; they will not become departments of a Ledgestone hospital and will not bill facility fees."
               % O.tin_of("BMG")),
             P("Brightwater's physicians will continue to see their patients at the same clinics. Ledgestone "
               "Medical Group's professional fee schedules with each carrier will apply to their services from "
               "closing. Ledgestone's outpatient facility rates with each carrier, in force for its three outpatient "
               "sites (Ledgestone Medical Center, Green Bay; Ledgestone Fox Cities Hospital, Appleton; and the "
               "Ledgestone Manitowoc Outpatient Center, a department of Ledgestone Medical Center), are attached as "
               "Exhibit C together with the professional schedules."),
             S("2 Parties"),
             P("Exhibit A lists the entities Ledgestone Health owns or controls. Exhibit B lists Brightwater's "
               "physicians. Neither party has a pending notice before the office other than this one."),
             S("3 Certification"),
             P("The undersigned certify that the information in this notice and its exhibits is complete and "
               "correct to the best of their knowledge."),
             P("Jacob Murillo, Halloran Pike LLP, for Ledgestone Health<br/>Debra Prince, Administrator, for "
               "Brightwater Medical Group, S.C.<br/>6 October 2025")]
    ex_a = [("Entity", "Taxpayer number", "Relationship to Ledgestone Health")]
    ex_a.append(("Ledgestone Medical Center", W.tin_from("sys|LDG"), "owned (hospital)"))
    ex_a.append(("Ledgestone Fox Cities Hospital", W.tin_from("sys|LDG"), "owned (hospital)"))
    ex_a.append(("Ledgestone Medical Group", O.tin_of("LMG"), "owned"))
    for key, rel in (("MFP", "affiliated, controlled"), ("FRPP", "affiliated, controlled"),
                     ("P2", "affiliated, controlled"), ("P5", "affiliated, controlled")):
        ex_a.append((O.PRACTICES[key][0], O.tin_of(key), rel))
    flow += [Spacer(1, 6), KeepTogether([S("Exhibit A. Entities owned or controlled by Ledgestone Health"),
                                         _table(ex_a, [2.6 * inch, 1.3 * inch, 2.6 * inch])])]
    ex_b = [("Physician", "NPI", "Specialty")]
    for npi in roster["BMG"]:
        p = people[npi]
        ex_b.append(("%s %s, %s" % (p["first"], p["last"], p["cred"]), npi, dict(O.TAXON_NAME)[p["taxonomy"]]))
    flow += [Spacer(1, 6), KeepTogether([S("Exhibit B. Brightwater Medical Group physicians"),
                                         _table(ex_b, [2.6 * inch, 1.3 * inch, 2.6 * inch])])]
    _doc(path, flow, "Notice of material change N25-014", "Jacob Murillo", "D:20251006164912-05'00'",
         "E3A90C1D5F2B48C7A61D0E97B4F2C358")


def write_docs(target, wd):
    import os
    rule_pdf(os.path.join(target, RULE))
    appendix_pdf(os.path.join(target, APPENDIX))
    dictionary_pdf(os.path.join(target, DICTIONARY))
    notice_pdf(os.path.join(target, NOTICE), wd["people"], wd["roster"])
