"""The pack's documents in the organisations' own voices: the mutual's capital policy, the broker's quote for 2027,
the expiring windstorm wording and the request to bring the programme to the board."""
from email.message import EmailMessage
from email.utils import format_datetime
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

INK = colors.HexColor("#1d2a33")
RULE = colors.HexColor("#9aa7b0")


def _styles(font="Helvetica"):
    base = ParagraphStyle("b", fontName=font, fontSize=9.6, leading=13.2, textColor=INK, alignment=TA_LEFT,
                          spaceAfter=5)
    return {
        "t": ParagraphStyle("t", parent=base, fontName=font + "-Bold", fontSize=14, leading=18, spaceAfter=8),
        "s": ParagraphStyle("s", parent=base, fontSize=8.6, leading=11.5, textColor=colors.HexColor("#4a5a66")),
        "h": ParagraphStyle("h", parent=base, fontName=font + "-Bold", fontSize=10.4, leading=14, spaceBefore=6),
        "p": base,
    }


def _doc(path, title, author, blocks, footer, font="Helvetica"):
    st = _styles(font)

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont(font, 7.5)
        canvas.setFillColor(colors.HexColor("#5b6b77"))
        canvas.drawString(18 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            invariant=1)
    story = []
    for kind, val in blocks:
        if kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), font, 8.8), ("FONT", (0, 0), (-1, 0), font + "-Bold", 8.8),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
            story.append(t)
            story.append(Spacer(1, 6))
        elif kind == "sp":
            story.append(Spacer(1, val))
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)


def capital_policy(path):
    blocks = [
        ("t", "Capital Policy CP-04: windstorm risk and its reinsurance"),
        ("s", "%s. Approved by the Board on 17 June 2026. Owner: the Chief Actuary. Reviewed annually; this "
              "version replaces CP-04 of June 2025." % W.ORG),
        ("h", "1. Scope"),
        ("p", "This policy covers windstorm: damage by wind to the buildings and contents the Society insures under its "
              "home and farm policies, and the rain or snow that enters through that damage. Flood and storm surge are "
              "held under CP-05. Figures are in pounds sterling."),
        ("h", "2. The windstorm capital requirement"),
        ("p", "The Society holds windstorm capital equal to its 1-in-200 annual windstorm loss. The 1-in-200 annual "
              "windstorm loss is the average of the 50 worst of the 10,000 simulated years in the catastrophe model's "
              "year loss table for the coming year's portfolio. A simulated year's windstorm loss is the sum of the "
              "losses of the storms in it, net of the recoveries the reinsurance in force would pay on them, with any "
              "reinstatement premium those recoveries call added back to the year's loss."),
        ("p", "Each simulated storm is costed at what the Society's own claims show it pays for such a storm: the "
              "model's loss for the storm, times the Society's incurred claims over the model's hindcast loss for the "
              "past storms like it, each past storm hindcast on the portfolio of its time. Each storm in the year loss "
              "table is one Loss Occurrence under the programme's covers. The actuarial function keeps the hindcast "
              "and the storm experience and refreshes both each summer."),
        ("h", "3. Buying reinsurance"),
        ("p", "A windstorm cover is bought when the capital it releases is worth more than it costs. The capital a "
              "cover releases is the 1-in-200 annual windstorm loss without it less the 1-in-200 annual windstorm loss "
              "with it, the covers already bought being in force in both. Its value is that release at the Society's "
              "cost of capital of 12 per cent a year, less its margin: its premium and the reinstatement premiums it "
              "is expected to call, less the recoveries it is expected to pay, each the average over the 10,000 "
              "simulated years."),
        ("p", "The occurrence cover is the programme's first cover and is renewed each year on terms the Board "
              "approves. Any further cover is valued with the occurrence cover in force."),
        ("h", "4. Responsibilities"),
        ("p", "The Chief Actuary, %s, maintains the year loss table, the hindcast and the storm experience. The Head of "
              "Reinsurance, %s, places the programme through the Society's broker. The Board approves the programme "
              "for each year at its November meeting." % (W.PEOPLE["actuary"], W.PEOPLE["reinsurance"])),
    ]
    _doc(path, "Capital Policy CP-04", W.ORG, blocks, "%s, Capital Policy CP-04, June 2026" % W.ORG_SHORT)


def broker_quote(path):
    occ, sec = W.BASE, W.SEC
    blocks = [
        ("t", "Windstorm reinsurance 2027: quotation"),
        ("s", "%s for %s. Issued 14 October 2026. Quotations firm until 30 November 2026, subject to the expiring "
              "wording save as stated below." % (W.BROKER, W.ORG)),
        ("h", "Period"),
        ("p", "Losses occurring from 00:00 on 1 January 2027 to 24:00 on 31 December 2027, local standard time."),
        ("h", "A. Occurrence cover (renewal)"),
        ("table", [["Term", "Quoted"],
                   ["Cover", "GBP %s each and every Loss Occurrence excess of GBP %s each and every Loss Occurrence"
                    % (format(int(occ["limit"]), ","), format(int(occ["retention"]), ","))],
                   ["Reinstatement", "One full reinstatement at 100 per cent additional premium, pro rata as to amount"],
                   ["Premium", "GBP %s, payable in two instalments" % format(int(occ["premium"]), ",")],
                   ["Loss Occurrence", "As the expiring wording: windstorm, 72 consecutive hours"]]),
        ("h", "B. Second-event cover (new)"),
        ("table", [["Term", "Quoted"],
                   ["Cover", "GBP %s each and every Loss Occurrence excess of GBP %s each and every Loss Occurrence"
                    % (format(int(sec["limit"]), ","), format(int(sec["retention"]), ","))],
                   ["Loss Occurrences covered", "The second and each subsequent Loss Occurrence of the period; the "
                    "first Loss Occurrence of the period, being the one whose 72 hours begin first, is not covered"],
                   ["Subject loss", "The Reassured's loss retained under the occurrence cover in each Loss "
                    "Occurrence, that is its loss up to the occurrence cover's GBP %s retention"
                    % format(int(occ["retention"]), ",")],
                   ["Reinstatement", "One full reinstatement at 100 per cent additional premium, pro rata as to amount"],
                   ["Premium", "GBP %s, payable in one instalment" % format(int(sec["premium"]), ",")]]),
        ("p", "Both quotations are led by Aldwych Syndicate 4127 with the expiring panel following. Cover B attaches "
              "only if Cover A is bought."),
    ]
    _doc(path, "Windstorm reinsurance 2027 quotation", W.BROKER, blocks,
         "%s, quotation PRB/HCM/27/031" % W.BROKER)


def expiring_wording(path):
    e = W.EXP
    blocks = [
        ("t", "Windstorm catastrophe excess of loss reinsurance 2026"),
        ("s", "Reassured: %s. Reinsurers: as per the signing schedule. Contract PRB/HCM/26/014." % W.ORG),
        ("h", "1. Period"),
        ("p", "Losses occurring from 00:00 on 1 January 2026 to 24:00 on 31 December 2026, local standard time."),
        ("h", "2. Cover"),
        ("p", "The Reinsurers shall pay the Reassured's Ultimate Net Loss in excess of GBP %s each and every Loss "
              "Occurrence, up to GBP %s each and every Loss Occurrence." % (format(int(e["retention"]), ","),
                                                                              format(int(e["limit"]), ","))),
        ("h", "3. Loss Occurrence"),
        ("p", "Loss Occurrence means all individual losses arising out of and directly occasioned by windstorm during "
              "any period of 72 consecutive hours. The Reassured may choose the date and time when any such period "
              "of 72 consecutive hours commences, and no individual loss shall be included in more than one Loss "
              "Occurrence. An individual loss is dated by the day on which the damage was done."),
        ("h", "4. Ultimate Net Loss"),
        ("p", "Ultimate Net Loss means the sums paid or payable by the Reassured on its policies for the individual "
              "losses in a Loss Occurrence, including expenses of loss adjusters, and for the purposes of each "
              "statement the paid amounts and the outstanding estimates at the statement date."),
        ("h", "5. Reinstatement"),
        ("p", "The cover is reinstated once in full from the time of each loss, at 100 per cent of the annual premium "
              "of GBP %s, pro rata as to the amount of cover reinstated." % format(int(e["premium"]), ",")),
        ("h", "6. Statements"),
        ("p", "The Reassured shall render a statement of each Loss Occurrence at the end of each quarter."),
    ]
    _doc(path, "Windstorm XL 2026 wording", W.BROKER, blocks, "Contract PRB/HCM/26/014, windstorm XL 2026")


def request_eml(path):
    m = EmailMessage()
    m["From"] = "Elizabeth Farmer <elizabeth.farmer@hartcombe-mutual.co.uk>"
    m["To"] = "%s <mandy.george@hartcombe-mutual.co.uk>" % W.PEOPLE["reinsurance"]
    m["Cc"] = "%s <arthur.begum@hartcombe-mutual.co.uk>" % W.PEOPLE["actuary"]
    m["Subject"] = "2027 windstorm programme for the November Board"
    m["Date"] = format_datetime(dt.datetime(2026, 10, 19, 8, 47, tzinfo=dt.timezone.utc))
    m["Message-ID"] = "<20261019084711.3315@hartcombe-mutual.co.uk>"
    m.set_content(
        "Mandy,\n\n"
        "Penwarden's quotation is in for 2027: the occurrence cover renewing as it stands and, new this year, a "
        "second-event cover. The Board needs a paper for the November meeting saying whether we add the second-event "
        "cover, and what it does to the windstorm capital we hold under CP-04, set out on the policy's own terms.\n\n"
        "Arthur's team has refreshed the year loss table for the 2027 portfolio, the hindcast and the storm "
        "experience, all in the folder. The Board will also want this year's storms against the expiring cover, and "
        "where our farm sums insured sit now that more of the bigger farms are shared with other insurers.\n\n"
        "Elizabeth Farmer\nChief Executive\n%s\n" % W.ORG)
    open(path, "wb").write(bytes(m))
