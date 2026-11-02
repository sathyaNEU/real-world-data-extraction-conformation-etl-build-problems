"""The two governing documents: Marrowgate's terms of trade (who may return what, against which invoice, at what
credit) and the accounting policies extract (what the returns allowance is). Each states facts in the
organisation's voice; neither describes a file or a column, and neither says how the allowance is computed."""
from __future__ import annotations

import os

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab import rl_config

rl_config.invariant = 1

import common as K
import records as RC

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=12.6, spaceAfter=5, alignment=TA_LEFT)
HEAD = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=10.5, leading=13.5, spaceBefore=7, spaceAfter=3)
TITLE = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=2)
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=colors.HexColor("#444444"))

INVARIANT = "D:20000101000000+00'00'"


def _doc(path, title, author, subject, story):
    def stamp(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, "Marrowgate Books Ltd, London  |  Registered in England and Wales")
        canvas.drawRightString(192 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                          title=title, author=author, subject=subject, creator=author, producer=author)
    d._doc_creation_date = None
    d.build(story, onFirstPage=stamp, onLaterPages=stamp)


def write_terms(out):
    s = []
    s.append(Paragraph("Marrowgate Books Ltd: Terms of Trade", TITLE))
    s.append(Paragraph("For bookselling customers in the United Kingdom and overseas. Effective 1 March 2024; supersedes the "
                       "terms of 1 September 2019, whose sale-or-return terms in section 3 are unchanged. Issued by Sales "
                       "Operations.", SMALL))
    s.append(Spacer(1, 6))
    secs = [
        ("1. Orders and supply",
         ["Orders are accepted by EDI, through the trade portal or by email to the sales office. Books are supplied from our "
          "distributor, Tallowmere Book Distribution Ltd, which despatches, receives returns and handles delivery queries for us.",
          "New titles ordered on subscription are invoiced and despatched up to seven days before publication so that stock is "
          "in shops on publication day. Each account's discount is set in its trading agreement; the invoice shows the "
          "recommended retail price and the discount for every line."]),
        ("2. Damage and shortage in transit",
         ["Damage or shortage in a delivery must be reported within 14 days of delivery. An agreed claim is credited against "
          "the invoice concerned. A transit claim is not a return and needs no returns authorisation."]),
        ("3. Sale or return",
         ["Customers trading on sale-or-return terms may return copies for credit. Every return needs an authorisation from "
          "Tallowmere before the copies are sent. An authorisation is issued for copies of a title invoiced to the account not "
          "less than three months and not more than twelve months before the date the authorisation is issued.",
          "Copies returned are matched to the account's invoices for the title in date order, earliest first, within that "
          "period, and are credited at the net price shown on the invoice they are matched to. No invoice is credited for more "
          "copies than it supplied.",
          "An authorisation lapses if the copies have not been received at Tallowmere within 60 days of its issue. Copies "
          "received against a lapsed authorisation, and copies received beyond those an authorisation covers, are held "
          "for collection and are not credited.",
          "Credit is given for every copy received against a valid authorisation, whatever its condition. Tallowmere grades "
          "returned copies on receipt and returns those fit for sale to stock."]),
        ("4. Firm sale",
         ["Customers trading on firm-sale terms receive the additional discount set in their trading agreement and may not "
          "return copies, other than under section 2."]),
        ("5. Payment",
         ["Invoices are payable within 90 days of the end of the month of invoice. Credit notes are set against the account's "
          "next remittance. Accounts that fall more than 60 days overdue may be placed on stop."]),
        ("6. General",
         ["These terms apply to every order placed on or after 1 March 2024 and to every return authorised on or after that "
          "date. Where a trading agreement differs from these terms, the trading agreement governs that account."]),
    ]
    for h, paras in secs:
        s.append(Paragraph(h, HEAD))
        for p in paras:
            s.append(Paragraph(p, BODY))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Queries: Sales Operations, %s, Head of Sales Operations." % K.PEOPLE["salesops"], SMALL))
    path = os.path.join(out, RC.F_TERMS)
    _doc(path, "Terms of Trade", "Marrowgate Books Ltd", "Terms of trade for bookselling customers", s)
    return path


def write_policy(out):
    s = []
    s.append(Paragraph("Accounting policies (extract)", TITLE))
    s.append(Paragraph("Marrowgate Books Ltd, financial statements for the year ending 31 October 2026. Draft for the year-end "
                       "audit, Finance, September 2026.", SMALL))
    s.append(Spacer(1, 6))
    secs = [
        ("Basis of preparation",
         ["The financial statements are prepared under FRS 102 on the historical cost basis. The company's financial year runs "
          "from 1 November to 31 October."]),
        ("Revenue",
         ["Revenue is the invoiced value of books supplied to trade customers, net of trade discounts, less an allowance for "
          "returns. Revenue from a sale is recognised when the books are despatched.",
          "The allowance for returns is the credit the company expects to give, under its terms of trade, for copies invoiced on "
          "or before the balance sheet date that will be returned. Claims for damage or shortage in transit are credited against "
          "revenue when agreed and form no part of the allowance."]),
        ("Inventories",
         ["Stock is valued at the lower of cost and net realisable value. Cost is the printing, paper and binding cost of each "
          "printing.",
          "Tallowmere grades returned copies on receipt as saleable, hurt or unsaleable. Saleable copies are taken back into "
          "stock at the cost of the printing they came from and unsaleable copies are written off; hurt copies are "
          "re-inspected and either restocked or pulped, and pulped copies are written off."]),
        ("Royalties and advances",
         ["Royalties are accrued on net sales at the contracted rates. Unearned advances are carried forward only where the "
          "title's expected sales will earn them out, and are otherwise written off."]),
        ("Foreign currencies",
         ["Export sales are invoiced in sterling. Transactions in other currencies are translated at the rate on the date of "
          "the transaction."]),
    ]
    for h, paras in secs:
        s.append(Paragraph(h, HEAD))
        for p in paras:
            s.append(Paragraph(p, BODY))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Prepared by %s, Group Financial Controller." % K.PEOPLE["controller"], SMALL))
    path = os.path.join(out, RC.F_POLICY)
    _doc(path, "Accounting policies FY2026 (extract)", "Marrowgate Books Ltd", "Accounting policies", s)
    return path


def write_all(out):
    return [write_terms(out), write_policy(out)]
