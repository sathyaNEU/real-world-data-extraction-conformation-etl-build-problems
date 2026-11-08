"""task127: the pack's documents, each a Word document exported to PDF by LibreOffice Writer (officepdf.py)."""
import datetime as dt
import os

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table

import officepdf
import world as W

NZ = dt.timezone(dt.timedelta(hours=13))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#1F3A5F")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#1F3A5F")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.2, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths):
    return Table(rows, colWidths=widths)


def nz(x):
    return format(int(round(x)), ",")


def terms(target):
    s = [P("Ruahine Bank", SMALL), P("Business Support Unit: terms of reference for 2027", H1),
         P("Approved by the Board Credit Committee on 30 November 2026. Owner: Chief Credit Officer.", SMALL),
         P("1. Purpose", H2),
         P("The Business Support Unit works with business borrowers in financial difficulty to keep viable "
           "businesses trading and to protect Ruahine's lending book. It restructures facilities, provides "
           "working-capital support and monitors each case until the borrower returns to its relationship team."),
         P("2. Who the unit takes on", H2),
         P("The unit takes on borrowers on the watch list approved by the Credit Committee, each referred with a "
           "support proposal from its relationship manager. The proposal names the new working-capital line the "
           "borrower needs."),
         P("3. The 2027 intake", H2),
         P("3.1 The Board has approved an envelope of NZ$6.0 million of new working-capital lines for packages "
           "starting in 2027."),
         P("3.2 A package is the working-capital line proposed for the borrower on the watch list, with the "
           "restructure and monitoring that go with it. A package is taken whole or not at all."),
         P("3.3 Packages go to the watch-list borrowers whose support keeps the most write-off off Ruahine's book "
           "within the envelope."),
         P("3.4 A borrower taken on is treated as not defaulting in the twelve months of its package. Without a "
           "package its chance of default in those months is the twelve-month PD in the IFRS 9 run at 31 December "
           "2026."),
         P("3.5 Write-off is valued over every borrower on Ruahine's book, each borrower that defaults at its own "
           "facilities' LGD times EAD as carried in that run."),
         P("4. The case file", H2),
         P("4.1 Each case file reports the borrower's security as the latest valuation of each property Ruahine "
           "holds as security for its lending at the reporting date, carried forward from the date the valuation "
           "was made by the regional commercial property index for the property's region and type, at the "
           "index's latest published value for each quarter."),
         P("4.2 Each case file reports the borrower's total commitment: its facility limits plus every guarantee it "
           "has given Ruahine for another customer's facilities, a limited guarantee at its limit and an unlimited "
           "guarantee at the guaranteed customer's facility limits."),
         P("5. Governance", H2),
         P("The unit reports monthly to the Chief Credit Officer. The Credit Committee confirms the intake at its "
           "February meeting, and a case leaves the unit when its relationship manager and the unit agree it can "
           "return to standard monitoring."),
         ]
    created = dt.datetime(2026, 11, 30, 16, 12, 0, tzinfo=NZ)
    officepdf.build(os.path.join(target, "bsu_terms_of_reference_2027.pdf"), s,
                    "Business Support Unit: terms of reference for 2027", "Ruahine Bank",
                    "Terms of reference for the Business Support Unit's 2027 intake", "Ruahine Bank  |  BSU terms 2027",
                    created, created)


REASONS = {
    "KIN": "Two export contracts lost in 2025; covenant breach at March 2026 accounts; order book recovering slowly.",
    "RID": "Construction slowdown; debtor days lengthening; equipment finance arrears cleared after restructure talks.",
    "MAT": "Margins squeezed after two supermarket supply contracts were re-tendered; interest cover below covenant at June 2026 accounts.",
    "HAR": "Two poor seasons; seasonal facility fully drawn at the season's start; land values supporting.",
    "SEL": "Residential building downturn; work in progress written down at year end.",
    "BRI": "Floor plan stock ageing; new-vehicle margins down; dealership franchise renewal due 2027.",
    "COA": "Council roading contract delayed; plant utilisation low over winter.",
    "NOR": "Print volumes falling; owner retiring and a sale process under way.",
}
RMS = {"KIN": "M. Humphrey", "RID": "A. Buckley", "MAT": "C. Gibbons", "HAR": "T. Smith", "SEL": "P. Stevens",
       "BRI": "B. Munro", "COA": "S. Russell", "NOR": "H. Richards"}


def watch_list(w, target):
    rows = [["Customer", "Borrower", "Division", "Region", "Added", "12m PD", "Exposure NZ$", "Proposed line NZ$", "RM"]]
    for c in sorted(w.watch.values(), key=lambda c: c["added"]):
        ead = sum(f["ead"] for f in c["facilities"])
        rows.append([c["cid"], c["name"].replace(" Limited", ""), c["sector"], c["region"],
                     c["added"].strftime("%d/%m/%Y"), "%.1f%%" % (100 * c["pd"]), nz(ead), nz(c["line"]),
                     RMS[c["key"]]])
    s = [P("Ruahine Bank  |  Credit Committee, 20 January 2027", SMALL),
         P("Watch list: business borrowers referred for support", H1),
         P("The business borrowers on the watch list at the January meeting, in the order they were added, with each "
           "relationship manager's proposed working-capital line for a support package. PD and exposure are as at the "
           "31 December 2026 IFRS 9 run."),
         T(rows, [50, 100, 44, 62, 54, 36, 50, 50, 54]),
         Spacer(1, 8), P("Commentary", H2)]
    for c in sorted(w.watch.values(), key=lambda c: c["added"]):
        s.append(P("<b>%s.</b> %s" % (c["name"].replace(" Limited", ""), REASONS[c["key"]])))
    s.append(Spacer(1, 6))
    s.append(P("Each proposal is held on the borrower's credit file. The committee will confirm the 2027 intake at "
               "its February meeting under the Business Support Unit's terms of reference.", SMALL))
    created = dt.datetime(2027, 1, 18, 10, 4, 0, tzinfo=NZ)
    officepdf.build(os.path.join(target, "watch_list_2027-01.pdf"), s, "Watch list, January 2027",
                    "Ruahine Bank", "Business borrowers referred to the Business Support Unit",
                    "Ruahine Bank  |  Credit Committee  |  Restricted", created, created, margin_mm=15)


def conclusion(grade_rows):
    """The validation's conclusion, read off its own traffic lights."""
    green = [g[0] for g in grade_rows if g[5] == "Green"]
    amber = [g[0] for g in grade_rows if g[5] == "Amber"]
    red = [g[0] for g in grade_rows if g[5] == "Red"]
    if red:
        return ("Grades %s are red and the model is recalibrated before the December 2025 run." % ", ".join(red))
    if not amber:
        return ("Every grade is green. Discrimination is stable against the 2024 validation. No recalibration is "
                "recommended; the next validation is due in June 2026.")
    span = lambda gs: "%s to %s" % (gs[0].split("-")[0], gs[-1].split("-")[-1]) if len(gs) > 1 else gs[0]
    return ("Grades %s are green and grades %s amber, where 2024's defaults ran above the band. Discrimination is "
            "stable against the 2024 validation and defaults still rise grade by grade. Amber grades stay under "
            "monitoring; no recalibration is recommended before the next validation, due in June 2026."
            % (span(green), span(amber)))


def validation(w, target, grade_rows):
    rows = [["Grade", "PD band", "Borrowers", "Mean PD", "Observed default rate", "Result"]] + grade_rows
    s = [P("Ruahine Bank  |  Model Risk", SMALL),
         P("Business PD model: annual validation, 2025", H1),
         P("Prepared for the Model Risk Committee, 16 June 2025."),
         P("1. Scope", H2),
         P("The business PD model scores each business borrower's twelve-month probability of default from its own "
           "financial statements and account conduct. It feeds the IFRS 9 runs, pricing and the watch list. This "
           "validation tests calibration on the December 2023 run against defaults in 2024."),
         P("2. Default definition", H2),
         P("A borrower is in default from the first of two triggers: 90 days past due on a material amount, or the "
           "credit team's assessment that it is unlikely to pay without recourse to security. The default is dated by "
           "that first trigger, and the borrower remains in default until the credit team records a cure after the "
           "probation period. The default register holds one row for each trigger met; the cure log holds the cures."),
         P("3. Calibration", H2),
         P("Borrowers performing at the end of 2023, grouped by the grade the December 2023 run gave them, against "
           "the share that defaulted during 2024. The result column is the bank's traffic light on a one-sided "
           "binomial test of the defaults against the grade's mean PD: green where the chance of as many defaults is "
           "above 5 per cent, amber from 0.01 to 5 per cent, red below 0.01 per cent."),
         T(rows, [40, 76, 56, 56, 92, 60]),
         Spacer(1, 6),
         P("4. Conclusion", H2),
         P(conclusion(grade_rows)),
         ]
    created = dt.datetime(2025, 6, 16, 14, 30, 0, tzinfo=dt.timezone(dt.timedelta(hours=12)))
    officepdf.build(os.path.join(target, "ifrs9_pd_model_validation_2025.pdf"), s,
                    "Business PD model: annual validation, 2025", "Ruahine Bank",
                    "Annual validation of the business probability of default model",
                    "Ruahine Bank  |  Model Risk  |  Internal", created, created)


def appetite(target):
    rows = [["Division", "2027 appetite", "Limit, share of business book"],
            ["A Agriculture, Forestry and Fishing", "Maintain", "18%"],
            ["C Manufacturing", "Maintain", "22%"],
            ["E Construction", "Reduce", "12%"],
            ["F Wholesale Trade", "Maintain", "10%"],
            ["G Retail Trade", "Reduce", "9%"],
            ["I Transport, Postal and Warehousing", "Grow", "12%"],
            ["N Administrative and Support Services", "Maintain", "7%"]]
    s = [P("Ruahine Bank  |  Risk", SMALL), P("Business lending: sector risk appetite for 2027", H1),
         P("The Board sets the appetite for each ANZSIC division of the business book each year, read against the "
           "regional economic outlook and the book's concentration. Appetite guides new lending; it does not change "
           "how existing borrowers are managed."),
         T(rows, [190, 100, 140]), Spacer(1, 6),
         P("Construction and retail are reduced for 2027 on the regional building consent and spending outlook; "
           "transport and warehousing grow with the region's distribution investment.")]
    created = dt.datetime(2026, 10, 28, 11, 0, 0, tzinfo=NZ)
    officepdf.build(os.path.join(target, "sector_risk_appetite_2027.pdf"), s,
                    "Business lending: sector risk appetite for 2027", "Ruahine Bank",
                    "Sector risk appetite for business lending in 2027", "Ruahine Bank  |  Risk  |  Internal",
                    created, created)
