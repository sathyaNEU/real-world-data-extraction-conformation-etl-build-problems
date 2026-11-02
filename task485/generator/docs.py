"""The pack's documents: the Board's preferred drug list policy, the P&T Committee's clinical review for 2027, the
PBM agreement's rebate exhibit, the PBM's network change notice, the implementation e-mails and the PBM's fiscal
2025 rebate guarantee reconciliation."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.6, leading=12.9, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.2, leading=10.4)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=10.8, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=13.5, spaceAfter=8, alignment=0)
MONO = ParagraphStyle("m", parent=BODY, fontName="Courier", fontSize=8.6, leading=10.8, spaceAfter=2)

PEOPLE = dict(director="Maria Burgess", chair="Brenda Cook", pbm="Timothy Peterson", pharmacist="Alyssa Fletcher")


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.8 * inch, title=title, author=author, creator=org,
                            subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.4)
        c.drawString(0.85 * inch, 0.5 * inch, org)
        c.drawRightString(letter[0] - 0.85 * inch, 0.5 * inch, "Page %d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def P(text, style=BODY):
    return Paragraph(text, style)


def _cell(text, size=8.0):
    return Paragraph(str(text), ParagraphStyle("c", parent=SMALL, fontSize=size, leading=size + 2.0))


def _table(rows, widths=None, size=8.2, wrap=True):
    if wrap:
        rows = [[_cell(c, size) for c in r] for r in rows]
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def policy(path):
    s = [P("Preferred Drug List Policy", T),
         P("%s, %s. Policy EB-RX-04. Adopted by the Board of Trustees on 9 May 2019; revised 14 March 2024." %
           (W.OFFICE, W.PLAN), SMALL),
         P("1. Purpose", H),
         P("The Plan places one product in each brand drug class the Pharmacy and Therapeutics Committee reviews on the "
           "preferred tier of its drug list, where members pay the lower copay. The Board of Trustees adopts the list "
           "for each calendar year on the Committee's recommendation, and the pharmacy benefit manager loads it before "
           "open enrollment."),
         P("2. The annual review", H),
         P("2.1 Each autumn the Committee reviews the classes it chooses. For each class the Committee's clinical review "
           "names the products it finds therapeutically equivalent for the purpose of this policy; only those products "
           "are compared."),
         P("2.2 The Office prepares the comparison from the pharmacy benefit manager's paid claims extract and its "
           "quarterly rebate remittance statements."),
         P("3. The preferred product", H),
         P("3.1 In each reviewed class the preferred product is the therapeutically equivalent product with the lowest "
           "net cost per 30-day supply."),
         P("3.2 A product's net cost per 30-day supply is the ingredient cost the Plan paid on the product's claims filled "
           "in the fiscal year, less the rebates the product's manufacturer paid the Plan on those claims, divided by the "
           "30-day supplies dispensed on those claims."),
         P("3.3 The fiscal year is the most recent Plan fiscal year (1 July to 30 June) for which the rebate remittances "
           "for all four quarters have been received."),
         P("3.4 A claim that was reversed is not counted."),
         P("4. The 30-day supply", H),
         P("4.1 A 30-day supply of a product is the quantity the clinical review lists for the product as 30 days of "
           "maintenance use."),
         P("5. Exceptions", H),
         P("5.1 Where the clinical review finds a product unsuitable for a group of members, the Committee may add a "
           "medical exception route; exceptions do not change the preferred product."),
         P("5.2 Members already on a product that leaves the preferred tier keep their copay until the end of the "
           "first quarter of the new year."),
         Spacer(1, 6),
         P("Approved: %s, Chair, Board of Trustees." % PEOPLE["chair"], SMALL)]
    _pdf(path, "Preferred Drug List Policy EB-RX-04", s, PEOPLE["chair"], W.OFFICE)


def clinical_review(path, w):
    """The Committee's clinical review: the reviewed classes, the products compared in each, and the 30-day supply."""
    notes = {"GLP1": "Weekly and daily agents are comparable for glycemic control at maintenance doses; cardiovascular "
                     "outcome data are considered class-wide for this purpose.",
             "SGLT2": "All three agents carry cardiovascular and renal indications at the doses listed.",
             "BASAL": "Insulin glargine, the interchangeable glargine and insulin degludec are compared unit for unit at "
                      "the listed pack.",
             "DOAC": "Both agents are indicated for stroke prevention in atrial fibrillation and for venous "
                     "thromboembolism; the listed strengths are the common maintenance strengths.",
             "ICS": "The three combinations are compared at medium-dose maintenance therapy for asthma and COPD.",
             "ADA": "The reference product and both biosimilars are compared at 40 mg every other week; adalimumab-kvrn is "
                    "designated interchangeable."}
    s = [P("Clinical Review for the 2027 Preferred Drug List", T),
         P("Pharmacy and Therapeutics Committee, %s. Prepared by %s, PharmD, Clinical Pharmacist, %s. 12 October 2026."
           % (W.PLAN, PEOPLE["pharmacist"], W.OFFICE), SMALL),
         P("1. Classes under review", H),
         P("The Committee reviews six brand classes for 2027. In each, the products listed below are therapeutically "
           "equivalent for the purpose of policy EB-RX-04, section 2.1. Products not listed are not compared."),
         ]
    rows = [["Class", "Products compared", "Clinical note"]]
    for c, cname in W.CLASSES:
        prods = [p for p in w.products.values() if p["cls"] == c]
        rows.append([cname, "; ".join("%s (%s)" % (p["brand"], p["inn"]) for p in prods), notes[c]])
    s.append(_table(rows, [1.35 * inch, 2.7 * inch, 2.75 * inch], size=7.8))
    s.append(P("2. The 30-day supply", H))
    s.append(P("For policy section 4.1, the quantity below is 30 days of maintenance use of each product."))
    rows = [["Product", "Package", "30-day supply (quantity)", "Unit"]]
    for c, _ in W.CLASSES:
        for p in [p for p in w.products.values() if p["cls"] == c]:
            q = ("%g" % p["per30"])
            rows.append([p["brand"], p["pkg"], q, {"EA": "each", "ML": "mL", "GM": "g"}[p["uom"]]])
    s.append(_table(rows, [2.0 * inch, 2.4 * inch, 1.5 * inch, 0.9 * inch], size=7.8))
    s.append(Spacer(1, 6))
    s.append(P("3. Members affected", H))
    s.append(P("Where the preferred product in a class changes, members on the outgoing product keep their copay to "
               "31 March 2027 under policy section 5.2. The Office will report the members affected to the Committee "
               "with the comparison."))
    _pdf(path, "Clinical Review for the 2027 Preferred Drug List", s, PEOPLE["pharmacist"], W.OFFICE)


def exhibit_c(path):
    g = W.GUARANTEE
    s = [P("Pharmacy Benefit Services Agreement, Exhibit C: Manufacturer Rebates", T),
         P("Between the %s, for the %s, and %s. Agreement effective 1 July 2024 for a term ending 30 June 2027."
           % (W.OFFICE, W.PLAN, W.PBM), SMALL),
         P("C.1 Pass-through", H),
         P("PBM shall pass through to the Plan one hundred percent of manufacturer rebates, administrative fees and "
           "price protection payments it receives on the Plan's claims."),
         P("C.2 Invoicing and remittance", H),
         P("PBM invoices manufacturers each calendar quarter for the Plan's claims with a date of service in the quarter "
           "that are adjudicated by the forty-fifth day after the quarter ends. Claims adjudicated, and reversals "
           "processed, after that day are invoiced with the following quarter as prior period adjustments. PBM remits "
           "within ninety days after each quarter ends, with a statement by manufacturer and by Plan account."),
         P("C.3 Claims not invoiced", H),
         P("Compound claims are not invoiced to manufacturers."),
         P("C.4 Minimum rebate guarantee", H),
         P("For the brand claims with a date of service in each calendar quarter, PBM guarantees rebates of at least the "
           "amounts below per brand claim. Where the rebates PBM has remitted for a quarter's claims, including prior "
           "period adjustments for that quarter, are less than the guarantee for that quarter's brand claims, PBM pays "
           "the shortfall with its next remittance."),
         _table([["Channel", "Guaranteed rebate per brand claim (USD)"],
                 ["Retail, days supply under 84", "%.2f" % g["RETAIL30"]],
                 ["Retail, days supply 84 or more", "%.2f" % g["RETAIL90"]],
                 ["Mail order", "%.2f" % g["MAIL"]],
                 ["Specialty", "%.2f" % g["SPECIALTY"]]], [3.2 * inch, 2.6 * inch], size=8.4),
         Spacer(1, 4),
         P("C.5 Definitions", H),
         P("A brand claim is a paid claim for a brand drug, net of its reversal, other than a compound claim. A claim's "
           "channel is the network of the dispensing pharmacy on the date of service: the retail network, PBM's mail "
           "order pharmacy, or the specialty network."),
         P("C.6 Audit", H),
         P("The Plan may audit rebate invoicing once each contract year on sixty days' notice.")]
    _pdf(path, "Exhibit C Manufacturer Rebates", s, W.PBM, W.PBM)


def network_notice(path, w):
    hosp = [p for p in w.pharmacies if p.get("before")]
    s = [P(W.PBM, T),
         P("Network Change Notice. 12 February 2026.", SMALL),
         P("To: %s, Director of Pharmacy Benefits, %s" % (PEOPLE["director"], W.OFFICE)),
         P("Effective March 1, 2026, the following pharmacies join the %s Specialty Network and leave the Retail "
           "Network. Claims these pharmacies dispense on or after March 1 adjudicate under specialty network terms; "
           "member copays for specialty drugs are unchanged." % W.PBM.split(" ")[0]),
         _table([["Pharmacy", "NPI"]] + [[p["name"], p["npi"]] for p in hosp], [4.4 * inch, 1.6 * inch], size=8.6),
         Spacer(1, 6),
         P("Questions about this notice may be directed to your account team."),
         P("%s, Account Executive" % PEOPLE["pbm"], SMALL)]
    _pdf(path, "Network Change Notice", s, PEOPLE["pbm"], W.PBM)


def emails(path):
    msgs = [
        ("Monday, September 22, 2026 9:14 AM", PEOPLE["pbm"], PEOPLE["director"], "2027 PDL load",
         "Maria, the Q2 remittance statement went out on September 18. For a January 1 effective date our "
         "implementation team needs the 2027 preferred list file by Friday, November 6, so the new tiers show in the "
         "member portal before open enrollment opens on November 3. Same file layout as last year: class, preferred "
         "NDCs, non-preferred NDCs."),
        ("Monday, September 22, 2026 11:02 AM", PEOPLE["director"], PEOPLE["pbm"], "RE: 2027 PDL load",
         "Thanks, Tim. The Committee meets October 21 and the Board on October 28, so November 6 works. We will send the "
         "file the week after the Board."),
        ("Tuesday, October 13, 2026 4:37 PM", PEOPLE["pharmacist"], PEOPLE["director"], "Clinical review",
         "The clinical review is final and in the Committee folder: six classes, the products compared in each and the "
         "30-day supply table. Nothing changed from the draft except the adalimumab note."),
        ("Wednesday, October 14, 2026 8:20 AM", PEOPLE["director"], PEOPLE["pharmacist"], "RE: Clinical review",
         "Got it. I will put the net cost table and the guarantee check together for the Committee packet, and the two "
         "slides for the Board."),
    ]
    s = [P("Messages: 2027 PDL implementation", T)]
    for when, frm, to, subj, body in msgs:
        s.append(P("<b>From:</b> %s<br/><b>Sent:</b> %s<br/><b>To:</b> %s<br/><b>Subject:</b> %s" % (frm, when, to, subj),
                   SMALL))
        s.append(P(body))
        s.append(Spacer(1, 6))
    _pdf(path, "2027 PDL implementation", s, PEOPLE["director"], W.OFFICE)


def reconciliation_fy2025(path, rec):
    """The PBM's fiscal 2025 guarantee reconciliation (July 2024 to June 2025), as sent to the Office."""
    g = W.GUARANTEE
    s = [P("%s: Rebate Guarantee Reconciliation, Plan Fiscal Year 2025" % W.PBM, T),
         P("Client: %s, %s. Prepared 30 September 2025." % (W.OFFICE, W.PLAN), SMALL),
         P("Brand claims are paid claims for brand drugs net of reversals, other than compound claims, by the dispensing "
           "pharmacy's network on the date of service (Exhibit C, C.5). Rebates remitted include prior period "
           "adjustments received by the date of this reconciliation.")]
    rows = [["Quarter", "Retail <84", "Retail 84+", "Mail", "Specialty", "Guarantee (USD)", "Remitted (USD)",
             "Shortfall (USD)"]]
    for r in rec:
        rows.append([r["q"], "{:,}".format(r["n"][0]), "{:,}".format(r["n"][1]), "{:,}".format(r["n"][2]),
                     "{:,}".format(r["n"][3]), "{:,.2f}".format(r["g"]), "{:,.2f}".format(r["rem"]),
                     "{:,.2f}".format(r["sf"])])
    s.append(_table(rows, [0.85 * inch, 0.7 * inch, 0.72 * inch, 0.6 * inch, 0.7 * inch, 1.05 * inch, 1.05 * inch,
                           0.95 * inch], size=7.8))
    s.append(Spacer(1, 6))
    s.append(P("Guaranteed rates per brand claim: retail under 84 days %.2f, retail 84 days or more %.2f, mail %.2f, "
               "specialty %.2f." % (g["RETAIL30"], g["RETAIL90"], g["MAIL"], g["SPECIALTY"]), SMALL))
    s.append(P("Shortfalls were paid with the remittance of the following quarter.", SMALL))
    _pdf(path, "Rebate Guarantee Reconciliation FY2025", s, W.PBM, W.PBM)
