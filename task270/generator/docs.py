"""The pack's documents: the no-claims step scale (2024 revision), the pricing committee's 2027 rating basis note,
the data team's guide to the claims and policy extracts, and the working pack's contents."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
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
INK, GREY, RULE = colors.HexColor("#1f2428"), colors.HexColor("#5d646a"), colors.HexColor("#b8bfc4")
PLUM = colors.HexColor("#4b2a4f")
TEAL = colors.HexColor("#1d4f55")
SLATE = colors.HexColor("#2f3b48")


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
        canvas.drawString(20 * mm, A4[1] - 12 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, right)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


# ---------------------------------------------------------------------------------------------- the step scale
def write_scale(path):
    S = styles("Serif", PLUM)
    doc = _doc(path, "No-claims step scale: 2024 revision", K.SOCIETY)
    rel = [["Step", "Relativity", "Step", "Relativity"]]
    for k in range(5):
        rel.append([str(k), "%.2f" % K.REL[k], str(k + 5), "%.2f" % K.REL[k + 5]])
    s = [Paragraph("No-claims step scale, private car: 2024 revision", S["h1"]),
         Paragraph("%s. Approved by the Board on 12 October 2023 for policy years starting on or after 1 January "
                   "2024. Replaces the 2019 scale." % K.SOCIETY, S["meta"]),
         Paragraph("1. The steps", S["h2"]),
         Paragraph("Every private car policy stands on one of ten steps, numbered 0 to 9. The step sets the no-claims "
                   "relativity that multiplies the policy's premium at inception and at each renewal. Step 9 carries "
                   "the largest reduction and step 0 none; the 2024 revision kept the 2019 scale's ten steps and its "
                   "rules of movement and changed the relativities to those below.", S["body"]),
         _table(S, rel, [22, 30, 22, 30], right=(1, 3)),
         Spacer(1, 4),
         Paragraph("2. Moving on the scale", S["h2"]),
         _clause(S, "2.1", "At each renewal a policy moves up one step, to at most step 9, if no claim that counts "
                           "against the steps was made in the policy year just ending."),
         _clause(S, "2.2", "It moves down three steps for each claim that counts against the steps made in the policy "
                           "year, to no lower than step 0, and does not move up that year."),
         _clause(S, "2.3", "Claims that count against the steps: an accident claim on which the policyholder was at "
                           "fault or liability was split, including one whose liability is still being decided at "
                           "renewal; a theft claim; a fire claim."),
         _clause(S, "2.4", "Claims that do not count against the steps: an accident claim on which the policyholder was "
                           "not at fault; a windscreen claim; an accident notification closed without any payment by the "
                           "Society."),
         _clause(S, "2.5", "A claim counts in the policy year in which the incident happened. A change of car, address "
                           "or cover during the year does not move the policy."),
         Paragraph("3. New policies", S["h2"]),
         Paragraph("A new policy starts on the step matching the proposer's proven years without a claim with a "
                   "previous insurer, one step a year to step 9, or on step 0 where the proposer has made an at-fault "
                   "claim in the last three years. Proof is taken from the previous insurer's renewal notice or a "
                   "letter of no-claims entitlement.", S["body"]),
         Paragraph("4. Step Protection", S["h2"]),
         _clause(S, "4.1", "From 1 January 2024 a policy renewing on step 6, 7, 8 or 9 may add Step Protection for the "
                           "policy year, at 11 per cent of the premium after the step's relativity."),
         _clause(S, "4.2", "A policy with Step Protection does not move down for claims made in that policy year. It "
                           "moves up one step at renewal only if no claim that counts against the steps was made; "
                           "otherwise it stays on its step."),
         _clause(S, "4.3", "Step Protection is chosen afresh at each renewal and lapses if the policy renews on a step "
                           "below 6."),
         Paragraph("5. Administration", S["h2"]),
         Paragraph("The step at inception and whether Step Protection applies are recorded on each policy year. Moves "
                   "are applied by the policy administration system at renewal from the claims notified in the year; "
                   "a correction after renewal (a claim settled not at fault, a claim withdrawn) is made at the next "
                   "renewal and is not backdated.", S["body"])]
    doc.build(s, onFirstPage=_frame(K.SOCIETY, "No-claims step scale, 2024 revision", "Serif"),
              onLaterPages=_frame(K.SOCIETY, "No-claims step scale, 2024 revision", "Serif"))


# ---------------------------------------------------------------------------------------------- the basis note
def write_basis(path):
    S = styles("Sans", TEAL)
    doc = _doc(path, "Private car rating basis 2027: definitions", K.PEOPLE["actuary"])
    s = [Paragraph("Private car rating basis 2027: definitions", S["h1"]),
         Paragraph("Pricing Committee paper PC/26/09. %s, Pricing Actuary. Definitions adopted by the committee "
                   "(chair %s) on 16 September 2026; figures to be prepared on the data cut of 30 September 2026 for "
                   "the meeting of 21 October 2026." % (K.PEOPLE["actuary"], K.PEOPLE["chair"]), S["meta"]),
         Paragraph("1. The 2027 wording", S["h2"]),
         Paragraph("From the renewals of 1 January 2027 every private car policy carries step protection as standard: "
                   "a claim made in a policy year will no longer move the policy down the no-claims steps, and the "
                   "Step Protection add-on is withdrawn. The relativities of the 2024 scale stay as they are, and a "
                   "policy moves up one step at renewal after a year without a claim that would have counted against "
                   "the steps. The 2027 rating basis prices private car business on that wording from the first "
                   "renewal; this note fixes the definitions the basis uses. Rating regions are the eight regions of "
                   "the Society's region map.", S["body"]),
         Paragraph("2. Accident frequency bands", S["h2"]),
         _clause(S, "2.1", "Each rating region's accident frequency is the number of accident claims that the "
                           "region's policies would have made over the 2024 and 2025 accident years had every policy "
                           "already carried step protection, per 100 vehicle-years earned."),
         _clause(S, "2.2", "Accident claims are claims under the accident section of the policy (damage to the insured "
                           "car, damage to third-party property and injury to third parties), whether the policyholder "
                           "was at fault, liability was split or the policyholder was not at fault, and whether or not "
                           "liability is settled, with an amount paid or reserved by the Society above nil at the data "
                           "cut, before any recovery from another insurer. Windscreen, theft and fire claims are "
                           "outside. A claim falls in the accident year of its accident date."),
         _clause(S, "2.3", "Vehicle-years are the days each policy was on cover within the period, divided by 365, "
                           "counted in the rating region of the policy's garaging postcode on each day under the region "
                           "map in force on that day. A claim is counted in the region of the garaging postcode on its "
                           "accident date."),
         _clause(S, "2.4", "Band C, the top accident band, holds the three regions with the highest accident frequency; "
                           "band A holds the three lowest and band B the other two. Each band's relativity is set "
                           "separately at the November meeting."),
         Paragraph("3. Windscreen rate", S["h2"]),
         _clause(S, "3.1", "Each region's windscreen frequency for the 2025 rating year is the number of windscreen "
                           "claims dated in 2025 per 100 vehicle-years with glass cover in 2025. Glass cover comes with "
                           "comprehensive cover only, so these are the vehicle-years on comprehensive cover, counted as "
                           "in 2.3 by the cover and garaging postcode on each day."),
         _clause(S, "3.2", "A windscreen claim is a repair or a replacement of the windscreen of a comprehensively "
                           "insured car at the Society's cost, whether the work was done by the Society's glass "
                           "partner or by a repairer the policyholder chose. It is dated on the day the job was booked "
                           "with the partner or, for other repairers, the day the claim was notified, and it is counted "
                           "in the region of the garaging postcode on that day. A replacement and the camera "
                           "recalibration it needs are one claim. Work the partner does for a policyholder on third "
                           "party, fire and theft cover is charged to the policyholder and is not a claim."),
         _clause(S, "3.3", "The average cost of a windscreen claim is the amount the Society pays for it including VAT."),
         Paragraph("4. Theft rate", S["h2"]),
         _clause(S, "4.1", "Each region's theft frequency for the 2025 rating year is the number of thefts in 2025 per "
                           "1,000 vehicle-years on either cover in 2025, counted as in 2.3."),
         _clause(S, "4.2", "A theft is a theft of the car or from it, or an attempt at either, reported to the police. It "
                           "is dated on the day it happened, counted in the region of the garaging postcode on that "
                           "day, and counted where it cost the Society something."),
         _clause(S, "4.3", "The average cost of a theft is everything the Society paid or reserved on it at the data cut, "
                           "less the net proceeds the salvage agent remitted for the car."),
         Paragraph("5. Sources", S["h2"]),
         Paragraph("The figures are prepared from the policy administration and claims extracts of 30 September 2026, "
                   "the glass partner's job file for 2025 and the salvage agent's statements, as the data guide of "
                   "5 October 2026 describes them. National statistics are for context and do not enter the basis.",
                   S["body"])]
    doc.build(s, onFirstPage=_frame(K.SOCIETY + ", Pricing Committee", "PC/26/09", "Sans"),
              onLaterPages=_frame(K.SOCIETY + ", Pricing Committee", "PC/26/09", "Sans"))


# ---------------------------------------------------------------------------------------------- the data guide
def write_guide(path):
    S = styles("Sans", SLATE)
    doc = _doc(path, "Claims and policy extracts: data guide", "Management Information")
    F = K.FILES
    leg_pol = [["Column", "Meaning"],
               ["POLICY_NO", "Policy number on the legacy system (FM and seven digits)"],
               ["TERM_NO", "The policy year's number, counting from the policy's first year"],
               ["INCEPTION_DATE", "First day on cover (day/month/year)"],
               ["EXPIRY_DATE", "Last day on cover"],
               ["CANCELLATION_DATE", "Last day on cover of a policy year cancelled before expiry; blank otherwise"],
               ["GARAGING_DISTRICT", "Postcode district where the car is kept, at inception"],
               ["NCD_STEP", "No-claims step at inception (0 to 9)"],
               ["STEP_PROTECTION", "Y where Step Protection was bought for the policy year"],
               ["COVER", "COMP comprehensive, TPFT third party, fire and theft, at inception"],
               ["VEHICLE_REG, ABI_GROUP, VEHICLE_YEAR", "The insured car at inception: registration, group, year"],
               ["MAIN_DRIVER_AGE", "Age band of the main driver at inception"],
               ["CHANNEL", "WEB, PHONE or BROKER"],
               ["NET_PREMIUM, IPT", "Premium after the step's relativity, and insurance premium tax, in pounds"],
               ["ADDONS", "Optional covers bought, separated by |"]]
    plat_pol = [["Column", "Meaning"],
                ["policy_number", "Policy number on the platform (FNM- and seven digits)"],
                ["term_number", "The policy year's number, carried over from the legacy system at migration"],
                ["term_start", "First day on cover (ISO date)"],
                ["term_end", "Renewal date: cover runs to midnight at the start of this day"],
                ["cancellation_date", "Date from which a cancelled policy year has no cover; blank otherwise"],
                ["garaging_postcode", "Full postcode where the car is kept, at term start"],
                ["ncd_step, step_protection", "No-claims step at term start; true where Step Protection applies"],
                ["cover_type", "Comprehensive, or Third party, fire and theft, at term start"],
                ["net_premium_gbp, ipt_gbp", "Premium after the step's relativity, and insurance premium tax"]]
    leg_clm = [["Column", "Meaning"],
               ["CLAIM_NO", "Claim number (C and seven digits); a reopened claim keeps its number"],
               ["POLICY_NO", "Policy number the claim is registered against"],
               ["LOSS_DATE, NOTIFIED_DATE", "Date of the incident; date the claim was notified (day/month/year)"],
               ["CLAIM_TYPE", "ACC accident, WSC windscreen, THF theft, FIR fire"],
               ["SECTION", "OD own damage, TPP third-party property, TPI third-party injury, NTF notification only, "
                           "GLS glass, THF theft, FIR fire"],
               ["FAULT", "Accident claims: F at fault, S split, N not at fault, P liability not yet settled"],
               ["STATUS", "O open, C closed, R reopened"],
               ["PAID_AMT, OS_AMT, RECOV_AMT", "Paid to date, outstanding reserve and amount recovered from another "
                                               "party, in pence"],
               ["POLICE_REF", "Crime reference given by the police, where there is one"],
               ["SUPPLIER, SUPPLIER_REF", "Firm instructed by the Society for the work, and its reference"]]
    plat_clm = [["Column", "Meaning"],
                ["claim_number", "Claim number (FCL and seven digits); a reopened claim keeps its number"],
                ["policy_number", "The policy's number when the claim was registered"],
                ["loss_date", "Date of the incident (UK date)"],
                ["notified_at", "Date and time the claim was registered, in UTC"],
                ["claim_type, section", "As on the legacy system, in words"],
                ["liability", "Accident claims: At fault, Split, Not at fault, Pending"],
                ["paid_gbp, outstanding_gbp, recovered_gbp", "Paid to date, outstanding reserve and amount recovered "
                                                             "from another party, in pounds"],
                ["police_reference", "Crime reference given by the police, where there is one"],
                ["supplier, supplier_reference", "Firm instructed by the Society for the work, and its reference"]]
    s = [Paragraph("Claims and policy extracts of 30 September 2026: data guide", S["h1"]),
         Paragraph("Management Information, %s. Issued 5 October 2026 with the extracts for the 2027 rating basis. "
                   "Questions to the MI mailbox." % K.SOCIETY, S["meta"]),
         Paragraph("1. Systems and extracts", S["h2"]),
         Paragraph("Private car policies were administered on the legacy policy system until 30 June 2025. From 1 July "
                   "2025 each policy moved to the new platform at its next renewal and was given a platform policy "
                   "number; policy years that started on the legacy system ran to their expiry there. Claims notified "
                   "up to 30 June 2025 were registered on the legacy claims system and are still settled on it; claims "
                   "notified from 1 July 2025 are registered on the platform. Every extract was taken on 30 September "
                   "2026.", S["body"]),
         _table(S, [["File", "Holds"],
                    [F["pol_legacy"], "Legacy policy years incepting 1 January 2023 to 30 June 2025, one row a policy year"],
                    [F["pol_platform"], "Platform policy years incepting 1 July 2025 to 30 September 2026, one row a "
                                        "policy year"],
                    [F["crosswalk"], "Each legacy policy number with the platform number it renewed under"],
                    [F["mta"], "Mid-term adjustments on both systems, one row an adjustment (data warehouse)"],
                    [F["clm_legacy"], "Legacy claims notified 1 January 2023 to 30 June 2025, one row a claim"],
                    [F["clm_platform"], "Platform claims notified 1 July 2025 to 30 September 2026, one row a claim"],
                    [F["glass"], "%s's 2025 job file, one row a job line" % K.PARTNER],
                    [F["salvage"], "%s's sale statements, 2025 and 2026 to September" % K.SALVAGE],
                    [F["regions"], "Postcode districts and their rating regions, with effective dates"]],
                [62, 108]),
         Paragraph("2. Policy years", S["h2"]),
         Paragraph("A policy year is one row. Its step, Step Protection, cover, car, garaging and premium are as at its "
                   "inception; changes during the year are in the mid-term adjustments file.", S["body"]),
         _table(S, leg_pol, [55, 115]),
         Spacer(1, 5),
         _table(S, plat_pol, [55, 115]),
         Paragraph("3. Mid-term adjustments", S["h2"]),
         Paragraph("One row an adjustment, keyed by the policy number and term number the policy year was written "
                   "under. effective_date is the first day the change applies. new_garaging, new_cover and "
                   "new_vehicle_reg carry the source system's own values (a postcode district and COMP or TPFT on the "
                   "legacy system; a full postcode and the cover in words on the platform). premium_change_gbp is the "
                   "pro-rata additional premium (negative for a refund).", S["body"]),
         Paragraph("4. Claims", S["h2"]),
         _table(S, leg_clm, [55, 115]),
         Spacer(1, 5),
         _table(S, plat_clm, [55, 115]),
         Paragraph("Amounts are cumulative to the extract. Incurred is paid plus outstanding. Recoveries from other "
                   "insurers are recorded as they are received. A windscreen claim for a repairer the policyholder "
                   "chose is paid on that repairer's invoice, VAT included.", S["body"]),
         Paragraph("5. Glass partner and salvage files", S["h2"]),
         Paragraph("%s's job file has one row a job line: job_ref and line_no; booked (date and time the job was "
                   "booked, UK time); fitted_date; insurer_policy_ref (the policy number the customer gave when "
                   "booking); vehicle_reg; fitting_postcode_district (where the work was done); description; billed_to "
                   "(the party the partner invoiced); net_amount and vat_amount in pounds; invoice_month." % K.PARTNER,
                   S["body"]),
         Paragraph("%s's statements have a sheet a year and one row a vehicle sold: lot, sale date, the Society's "
                   "claim number the vehicle was handed over under, registration, category, hammer price, the "
                   "agent's fees and the net proceeds remitted to the Society." % K.SALVAGE, S["body"]),
         Paragraph("6. Region map", S["h2"]),
         Paragraph("One row a postcode district and region assignment, with the first day it applies and, where it "
                   "was replaced, the last. Two districts were reassigned from 1 April 2025.", S["body"])]
    doc.build(s, onFirstPage=_frame(K.SOCIETY + ", Management Information", "Data guide, extracts of 30 September 2026",
                                    "Sans"),
              onLaterPages=_frame(K.SOCIETY + ", Management Information", "Data guide, extracts of 30 September 2026",
                                  "Sans"))


def write_contents(path, rows):
    lines = ["2027 rating basis: working pack",
             "Pricing, %s. Assembled 5 October 2026 for the Pricing Committee meeting of 21 October 2026." % K.SOCIETY,
             ""]
    for name, desc in rows:
        lines.append(name)
        lines.append("    " + desc)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")
