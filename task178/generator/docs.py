"""task178 documents: the Banco Central de Tamarquia's press release and its hourly data release note, and Banco
Cordillera's FX options pricing policy (PDFs). Their text is held here as data so checks.py can quote it and verify.py
can read it back."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import A4                                                  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as C          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Caladea", "crosextra/Caladea-Regular.ttf"), ("Caladea-Bold", "crosextra/Caladea-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
GREY = colors.HexColor("#555b61")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_stamp(d, hh=10, mi=0):
    return ("D:%04d%02d%02d%02d%02d00-05'00'" % (d.year, d.month, d.day, hh, mi)).encode()


def styles(face, bold, ink, accent):
    return dict(
        org=ParagraphStyle("org", fontName=bold, fontSize=9.5, leading=12, textColor=accent, spaceAfter=2),
        h1=ParagraphStyle("h1", fontName=bold, fontSize=14, leading=18, textColor=ink, spaceAfter=4),
        sub=ParagraphStyle("sub", fontName=face, fontSize=9.2, leading=12, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2", fontName=bold, fontSize=10.5, leading=13.5, textColor=accent, spaceBefore=8, spaceAfter=3),
        body=ParagraphStyle("body", fontName=face, fontSize=10.4, leading=13.8, textColor=ink, spaceAfter=5),
        cell=ParagraphStyle("cell", fontName=face, fontSize=8.9, leading=10.9, textColor=ink),
        small=ParagraphStyle("small", fontName=face, fontSize=8.3, leading=10.4, textColor=GREY, spaceBefore=8))


HOUSE = {"bca": styles("Caladea", "Caladea-Bold", colors.HexColor("#1b2430"), colors.HexColor("#7a1f2b")),
         "bco": styles("Carlito", "Carlito-Bold", colors.HexColor("#1d2329"), colors.HexColor("#0f4c5c"))}


def _footer(text, st):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(st["small"].fontName, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 11 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "%d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths, st, head_bg):
    data = [[Paragraph(esc(str(c)), st["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b9c0c8")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                           ("BACKGROUND", (0, 0), (-1, 0), head_bg)]))
    return t


def build_pdf(path, doc):
    st = HOUSE[doc["house"]]
    head_bg = colors.HexColor("#efe4e5") if doc["house"] == "bca" else colors.HexColor("#e2eef1")
    pdf = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=doc["title"], author=doc["author"], subject="", creator="",
                            producer="")
    story = [Paragraph(esc(doc["head"]), st["org"]), Paragraph(esc(doc["title"]), st["h1"]),
             Paragraph(esc(doc["sub"]), st["sub"])]
    for b in doc["blocks"]:
        if b[0] in ("h2", "body", "small"):
            story.append(Paragraph(esc(b[1]), st[b[0]]))
        elif b[0] == "table":
            story.append(_table(b[1], [w * mm for w in b[2]], st, head_bg))
            story.append(Spacer(1, 5))
    pdf.build(story, onFirstPage=_footer(doc["foot"], st), onLaterPages=_footer(doc["foot"], st))
    PP.normalize_pdf(path, doc["stamp"], doc["stamp"])


def text_of(doc):
    out = [doc["head"], doc["title"], doc["sub"]]
    for b in doc["blocks"]:
        if b[0] == "table":
            out.extend(" | ".join(str(c) for c in r) for r in b[1])
        else:
            out.append(b[1])
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------ the press release
ANNOUNCE = dict(
    house="bca", author="Banco Central de Tamarquia", stamp=pdf_stamp(C.ANNOUNCED, 17, 30),
    head="BANCO CENTRAL DE ARAUQUIA  ·  Communications Department",
    title="Press release 41/2026: the Bank ends its operations in the spot foreign exchange market",
    sub="Ilvara, 1 October 2026. For immediate release. English version of Comunicado 41/2026.",
    foot="Banco Central de Tamarquia · Comunicado de prensa 41/2026 · versión en inglés",
    blocks=[
        ("body", "At its meeting of 30 September 2026 the Board of Directors of the Banco Central de Tamarquia decided that "
                 "the Bank will cease to operate in the spot foreign exchange market at the close of business on 31 "
                 "December 2026. From 1 January 2027 the exchange rate of the tamarquian peso against the US dollar will be "
                 "set by the market without operations by the Bank."),
        ("h2", "Background"),
        ("body", "Since 2 January 2024 the Bank's Market Operations Department has bought and sold US dollars on the "
                 "interbank platform with the reporting dealers, at prevailing market prices, to moderate disorderly "
                 "movements in the exchange rate during the trading session. These operations were not intended to defend "
                 "any level of the exchange rate, and the Bank has not published a reference band or a target for the "
                 "rate. International reserves stood at 21,384 million dollars at the end of August 2026."),
        ("body", "The Board considers that the depth of the local market, the strength of the reserve position and the "
                 "convergence of inflation to the 3 per cent target allow the peso to float without these operations. The "
                 "Bank retains its powers to act in the market in exceptional circumstances of systemic risk, which the "
                 "Board would announce at the time."),
        ("h2", "Transparency"),
        ("body", "Under the Board's transparency resolution of 2025, the Bank will publish before the end of 2026 the record "
                 "of its spot operations since January 2024, operation by operation, together with the net purchases of US "
                 "dollars by customers reported each hour by the reporting dealers and the platform's hourly mid rates for "
                 "the same period. The publication will be accompanied by a release note describing each file."),
        ("h2", "Other measures"),
        ("body", "The Bank's foreign exchange forward and swap facilities with the reporting dealers, which were not used in "
                 "2025 or 2026, are closed from the same date. The publication of the representative market rate (TRM) and "
                 "of the monthly foreign exchange market statistics continues unchanged."),
        ("small", "Press contact: Departamento de Comunicaciones, Banco Central de Tamarquia, Avenida de los Fundadores 410, "
                  "Ilvara. This English version is provided for information; the Spanish text prevails."),
    ])


# ------------------------------------------------------------------------------------------------ the release note
NOTE = dict(
    house="bca", author="Banco Central de Tamarquia", stamp=pdf_stamp(C.RELEASE, 18, 5),
    head="BANCO CENTRAL DE ARAUQUIA  ·  Market Operations Department",
    title="Spot operations and dealer customer flows, January 2024 to December 2026: release note",
    sub="Published 30 December 2026 with the data files listed below. Contact: Inés Quiroz, Director of Market Operations.",
    foot="BCT · Market Operations · Release note, hourly data 2024-2026 · 30 December 2026",
    blocks=[
        ("body", "This note accompanies the publication announced in Press release 41/2026. It covers the trading sessions "
                 "from 2 January 2024 to 29 December 2026. Local times are Tamarquia time (UTC-5, no daylight saving)."),
        ("h2", "1. Spot operations (" + C.F_OPS + ")"),
        ("body", "One row for each operation dealt by the Bank's dealing desk with a reporting dealer. The time stamp is the "
                 "dealing system's time of the deal, local time. Operation VENTA is a sale of US dollars by the Bank and "
                 "COMPRA a purchase. Amounts are in thousands of US dollars. The value date is the settlement date, the next "
                 "business day for both currencies. Status ANULADA marks an operation cancelled after dealing because it "
                 "was entered in error; it was not settled, and the operation as dealt is the row that follows it."),
        ("h2", "2. Dealer customer flows (" + C.F_FLOWS + ")"),
        ("body", "Each reporting dealer's net purchases of US dollars by its customers in each trading hour, in thousands of "
                 "US dollars: positive when the dealer's customers bought dollars from it on balance, negative when they "
                 "sold. Customers are all counterparties other than reporting dealers and the Bank, so interbank trades "
                 "and operations with the Bank are not included. Hours are labelled by local start and end (08-09 is "
                 "08:00 to 09:00). Dealers file each hour by 18:00 the same day and may file again to correct a report; "
                 "the file keeps every report received with its receipt time, and the report of record for a dealer and "
                 "hour is the last one received."),
        ("h2", "3. Platform hourly mid (" + C.F_MID + ")"),
        ("body", "The interbank platform's mid rate, in pesos per US dollar, at each hour mark of the session from 08:00 to "
                 "16:00 local time. 08:00 is the first mid after the opening call; 16:00 is the session close and the "
                 "closing rate. A mark is missing where the platform's price feed to the Bank failed; no value is "
                 "estimated for it."),
        ("h2", "4. Reporting dealers (" + C.F_DEALERS + ") and calendar (" + C.F_CAL + ")"),
        ("body", "The register lists every institution that reported customer flows in the period, with the dates between "
                 "which its reports are of record. Financiera Tres Valles was merged into Banco del Salitral on 1 July "
                 "2025, and Banco del Salitral reports the merged customer base from that date. The calendar lists the "
                 "days on which the platform did not open: national holidays, and United States holidays, on which "
                 "dollars do not settle."),
        ("h2", "5. Other series"),
        ("body", "The representative market rate (TRM) for each date is the volume-weighted average of the interbank "
                 "platform's trades in the previous session (" + C.F_TRM + "). The monthly foreign exchange market "
                 "statistics (" + C.F_STATS + ") are the Bank's regular publication, to November 2026; the Bank's "
                 "net spot sales there are by value date."),
        ("table", [["File", "Rows", "Grain"],
                   [C.F_OPS, "one per operation", "operation"],
                   [C.F_FLOWS, "one per report received", "dealer x trading hour x report"],
                   [C.F_MID, "one per hour mark", "session x hour mark"],
                   [C.F_DEALERS, "one per institution", "institution"],
                   [C.F_CAL, "one per calendar day", "day"]], [72, 46, 52]),
        ("small", "The Bank publishes these data for information. Figures for 2024 and 2025 have been audited; figures for "
                  "2026 are provisional until the 2026 accounts are approved."),
    ])


# ------------------------------------------------------------------------------------------------ the pricing policy
POLICY = dict(
    house="bco", author="Banco Cordillera", stamp=pdf_stamp(dt.date(2026, 12, 15), 16, 40),
    head="BANCO CORDILLERA  ·  Treasury  ·  FX Options",
    title="FX options pricing policy: amendment for the 2027 launch",
    sub="Version 2.1, approved 15 December 2026 by Miguel Rengifo (Head of Market Risk) and Yanet Cáceres (Head of FX "
        "Options). Supersedes version 2.0 of 12 June 2026.",
    foot="Banco Cordillera · Treasury · FX options pricing policy v2.1 · internal",
    blocks=[
        ("h2", "1. Products"),
        ("body", "From 4 January 2027 the desk offers corporate clients European options on the US dollar against the "
                 "peso with tenors of one to twelve months, cash settled against the platform's 16:00 closing rate on the "
                 "expiry date. Minimum notional 250,000 dollars."),
        ("h2", "2. Volatility"),
        ("body", "The desk prices each option at the volatility the closing rate is expected to show over the option's "
                 "life, measured as the annualised root mean square of the daily log changes in the closing rate, at 252 "
                 "sessions a year, and rounded up to the next whole per cent. The head of FX Options sets the volatility "
                 "on that grid before each quarter."),
        ("body", "For the 2027 launch the expected volatility is the volatility the closing rate would have shown over the "
                 "sessions of 2024 to 2026 had the Banco Central not operated in the spot market, with customers' dollar "
                 "trading and the news the market received as they were. The Banco Central's spot operations end on 31 "
                 "December 2026."),
        ("h2", "3. Hedging charge"),
        ("body", "The desk delta-hedges on the interbank platform. The premium carries a hedging charge set from the "
                 "desk's own 2026 execution cost on the platform, refreshed by Treasury Operations each December."),
        ("h2", "4. Limits"),
        ("body", "The launch's vega limit is sized on the dollar forwards that corporate clients hold with the bank and "
                 "that fall due in 2027, quarter by quarter. Forwards with the bank's own Treasury desks are not client "
                 "business."),
        ("h2", "5. Revisions"),
        ("table", [["Version", "Date", "Change"],
                   ["1.0", "4 March 2025", "First issue (forwards only)."],
                   ["2.0", "12 June 2026", "Options added, subject to the regulator's authorisation."],
                   ["2.1", "15 December 2026", "Volatility basis for the 2027 launch; hedging charge; launch limits."]],
         [22, 34, 114]),
    ])

DOCS = {C.F_ANNOUNCE: ANNOUNCE, C.F_NOTE: NOTE, C.F_POLICY: POLICY}

ESTIMAND = ("For the 2027 launch the expected volatility is the volatility the closing rate would have shown over the "
            "sessions of 2024 to 2026 had the Banco Central not operated in the spot market")
CONVENTION = "the annualised root mean square of the daily log changes in the closing rate, at 252 sessions a year"
ROUND_UP = "rounded up to the next whole per cent"
