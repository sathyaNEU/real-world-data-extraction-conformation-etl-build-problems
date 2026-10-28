"""task118 documents: the Treasury's Budget appraisal manual (pdf), Customs' excise accounting note CE14 (pdf) and the
thread that set the 2027 envelope (eml)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.3, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.6, leading=17.5,
                        spaceAfter=3, textColor=colors.HexColor("#1F3A5F"))
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.6, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.6):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.4)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EAF0")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, author, flow, footer):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, invariant=1)
    doc.build(flow, onFirstPage=_footer(footer), onLaterPages=_footer(footer))


def manual(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Budget Appraisal Manual: tax measures", h1),
         Paragraph("%s. 2026 edition, issued 14 April 2026, replacing the 2019 edition. Owner: the Economics Unit."
                   % P.TREASURY, small),
         Spacer(1, 4),
         Paragraph("1. Purpose", h2),
         Paragraph("This manual sets out how the Treasury appraises the tax measures in a Budget for the Treasury "
                   "Minister and the Council of Ministers. It covers what a measure is appraised on, the period, the "
                   "starting point and the evidence. It does not prescribe models; analysts use the evidence the "
                   "Treasury holds and say how they used it.", body),
         Paragraph("2. Excess burden", h2),
         Paragraph("A tax costs those who bear it more than the revenue it raises: they also lose the value of what "
                   "they no longer buy because of it. That loss beyond the revenue is the tax's excess burden. On a good "
                   "that carries excise duty, every tax on the good counts towards it: the duty and the GST charged on "
                   "the duty-inclusive price.", body),
         Paragraph("3. Prices", h2),
         Paragraph("Eskerholm buys its alcohol and road fuel on outside markets at prices it cannot move, so a change "
                   "in duty passes in full to the shelf price, with GST charged on top. Producers' and importers' "
                   "prices are taken as unchanged by any measure.", body),
         Paragraph("4. The Budget year", h2),
         Paragraph("A measure is appraised on the Budget year, the calendar year in which it takes effect: the excess "
                   "burden it removes or adds in that year, on what consumers will buy in that year. A Budget's duty "
                   "measures take effect on 1 January and are permanent.", body),
         Paragraph("5. The starting point", h2),
         Paragraph("The appraisal starts from the latest four quarters of duty-paid clearances the Statistics Office "
                   "has published, each quarter standing for the same quarter of the Budget year, at the latest "
                   "quarter's shelf prices with the duty rates already set for the Budget year.", body),
         Paragraph("6. Revenue", h2),
         Paragraph("A measure's revenue cost is the duty and GST the States receive less in the Budget year because of "
                   "it, after consumers respond.", body),
         Paragraph("7. Evidence on consumers' response", h2),
         Paragraph("The Treasury's evidence on how consumers respond to the prices they pay is the Statistics "
                   "Office's quarterly series of duty-paid clearances and average shelf prices at constant prices, "
                   "from 2008.", body),
         Paragraph("8. A fixed sum given back through one measure", h2),
         Paragraph("Where a Budget gives a fixed sum back to taxpayers through one measure, the Treasury recommends the "
                   "measure that removes the most excess burden in the Budget year for that sum, and reports the "
                   "next best beside it.", body),
         Paragraph("9. Effects outside this appraisal", h2),
         Paragraph("Health, road safety and environmental effects of duties are appraised by the departments concerned "
                   "and reported alongside; they are not part of this appraisal.", body)]
    _doc(path, "Budget Appraisal Manual: tax measures", P.TREASURY, s,
         "%s. Budget Appraisal Manual, 2026 edition." % P.TREASURY)


def ce14(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Excise accounting: periods, declarations and warehouses", h1),
         Paragraph("%s. Accounting note CE14, issue 3, January 2025. For traders, warehouse keepers and Treasury "
                   "statisticians." % P.CUSTOMS, small),
         Spacer(1, 4),
         Paragraph("1. Accounting period", h2),
         Paragraph("Excise is accounted for in the period in which the declaration is accepted, by the date in "
                   "Eskerholm, which keeps United Kingdom time (GMT, and BST in summer). The declarations system "
                   "records acceptance times in UTC.", body),
         Paragraph("2. Amendments and cancellations", h2),
         Paragraph("A declaration is corrected by lodging a new declaration that gives the number of the declaration it "
                   "corrects as its related declaration. The new declaration replaces the one it corrects and is "
                   "accounted for in the period in which the release was first accepted. A cancelled declaration "
                   "accounts for nothing.", body),
         Paragraph("3. Repayments", h2),
         Paragraph("Duty repaid on goods returned to an excise warehouse or destroyed after release (procedure 6171) is "
                   "credited in the period the repayment is accepted. A repayment gives the release it relates to as "
                   "its related declaration.", body),
         Paragraph("4. Removals from warehouses", h2),
         Paragraph("Goods may move between approved excise warehouses with duty suspended. Goods removed from an excise "
                   "warehouse to premises that are not an approved excise warehouse on the day of the removal are "
                   "released for home use, and the duty becomes due on the removal at the rate in force that day, "
                   "whatever procedure the removal was declared under. The register of approved warehouses gives each "
                   "approval's premises and dates; an approval is in force up to the day before its end date.", body),
         Paragraph("5. Methods of payment", h2),
         _table([["Code", "Meaning"],
                 ["IMMEDIATE", "duty paid when the declaration is accepted"],
                 ["DEFERMENT", "duty due under the trader's deferment approval, collected on the 15th of the next month"],
                 ["SUSPENDED", "no duty due on this movement"],
                 ["REPAYMENT", "duty repaid to the trader"]], [30, 134])]
    _doc(path, "Excise accounting note CE14", P.CUSTOMS, s, "%s. Accounting note CE14." % P.CUSTOMS)


def thread():
    pe = P.PEOPLE
    dom = {"economist": "assembly.gov.esk", "minister": "assembly.gov.esk", "customs": "gov.esk", "stats": "gov.esk"}

    def addr(k):
        first, last = pe[k].split()
        return "%s <%s.%s@%s>" % (pe[k], first.lower(), last.lower(), dom[k])

    hdr = ("From: %s\nTo: %s\nCc: %s, %s\nSubject: Re: Scrutiny of the 2027 Budget: the duty envelope\n"
           "Date: Mon, 19 Oct 2026 15:08:44 +0100\nMessage-ID: <eso-20261019-150844-4471@gov.esk>\n"
           "In-Reply-To: <easp-20261016-104102-2210@assembly.gov.esk>\nMIME-Version: 1.0\n"
           "Content-Type: text/plain; charset=\"utf-8\"\nContent-Transfer-Encoding: 8bit\n\n"
           % (addr("stats"), addr("economist"), addr("minister"), addr("customs")))
    body = """Rhys,

The quarterly clearances and prices are in the panel's folder: 2012 onwards as we publish them,
and the 2008 to 2011 back series in the old workbook layout, already at constant 2026 prices. The
2026 Q2 and Q3 figures are preliminary.

Ben

Benjamin Humphreys
Head of Economic Statistics, Eskerholm Statistics Office

On Fri, 16 Oct 2026 at 10:41, Elaine Hooper <elaine.hooper@gov.esk> wrote:
> Rhys, for the panel's review of the Budget's excise annex the declarations extract to the end of
> September, the procedure codes, CE14 and the warehouse register are in the folder. The panel
> asked for the excise we accounted for on releases from bonded warehouses, by duty, for each
> quarter from October 2025 to September 2026, in your workbook.
>
> Elaine
>
> Elaine Hooper
> Head of Customs and Excise
>
> On Fri, 16 Oct 2026 at 09:12, Aimee Miah <aimee.miah@assembly.gov.esk> wrote:
>> Rhys, in the principles debate the Assembly agreed a GBP 1.5 million envelope for duty in the
>> 2027 Budget and left it to amendment which duty it goes to. It goes to one duty, and the panel
>> will lodge the amendment. I want your advice on which, appraised on the Treasury's manual, with
>> what it removes in excess burden next year and the next best beside it, for the panel's meeting
>> on 2 December. The Assembly debates the Budget on 15 December.
>>
>> Aimee
>>
>> Deputy Aimee Miah
>> Chair, Economic Affairs Scrutiny Panel
"""
    return hdr + body
