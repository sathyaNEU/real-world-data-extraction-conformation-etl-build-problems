"""task309 documents: the board brief for the 2027 retrofit grant round, the model-governance standard MG-04, the
vendor's release note, the claims department's storm close-out summaries and the 2026-27 reinsurance program
(pdf), and the roofing contractors' 2027 quotes (xlsx)."""
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess
import records as R
import world as W

PRODUCER = "SPM-RISK"
# first and last save times on each paper's date, and the US Central offset that day
SAVED = {"2026-11-06": ("091522", "163041", "-06'00'"), "2025-03-18": ("102233", "141907", "-05'00'"),
         "2026-10-21": ("082710", "111456", "-05'00'"), "2026-02-09": ("134408", "155920", "-06'00'"),
         "2026-05-28": ("100151", "172614", "-05'00'")}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.4, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(19 * mm, 10 * mm, text)
        canvas.drawRightString(LETTER[0] - 19 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.6, right=()):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.2)
    cellr = ParagraphStyle("cellr", parent=cell, alignment=2)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    out = []
    for r, row in enumerate(rows):
        out.append([Paragraph(str(v), head if r == 0 else (cellr if j in right else cell)) for j, v in enumerate(row)])
    t = Table(out, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#33475B")),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#B8C2CC")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EDF2")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _pdf(path, title, subject, story, foot, stamp, author=P.ORG_SHORT, producer=PRODUCER):
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=17 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author,
                            subject=subject, invariant=1)
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    postprocess.scrub(path, producer, stamp)
    postprocess.pdf_clock(path, *SAVED[stamp])


def brief(path, pf):
    body, h1, h2, small = _styles()
    tab = [["County", "Homes on the round's portfolio", "Coverage A (USD million)", "Portfolio code"]]
    for c in P.CANDIDATES:
        d = pf[pf.county == P.COUNTY_NAME[c]]
        tab.append([P.COUNTY_NAME[c], "{:,}".format(len(d)), "%.1f" % (d.coverage_a_usd.sum() / 1e6), P.PORTFOLIO_CODE[c]])
    s = [Paragraph("2027 FORTIFIED Roof grant round: choosing the county", h1),
         Paragraph("Board brief from %s, %s. November 6, 2026. For the board meeting of January 14, 2027. "
                   "Reference BRD-2026-118." % (P.PEOPLE["cat"], P.TITLES["cat"]), small),
         Paragraph("1. The decision", h2),
         Paragraph("The 2027 mitigation budget funds one round of roof-retrofit grants: up to USD 12,000 a home toward "
                   "a new roof built and certified to the FORTIFIED Roof standard, for 1,500 homes we insure in one "
                   "county. The round costs the same in any county (USD 18.0 million, grants and inspection fees). "
                   "Contractors re-roof between February and May 2027 so that every home on the round carries its "
                   "FORTIFIED Roof certificate before the season opens on June 1. The board is asked to choose the "
                   "county at its January meeting from the four coastal counties below.", body),
         Paragraph("2. The homes each county's round would re-roof", h2),
         Paragraph("For each county we have listed the 1,500 homes the round would re-roof there: homes we insured on "
                   "September 30, 2026 that do not hold a valid FORTIFIED Roof certificate, taken in order of the roof "
                   "year on our underwriting record, oldest first (retrofit_2027_modeled_portfolios.csv). %s modeled "
                   "each county's list as a portfolio in %s, on the roofs the homes have now." % (P.VENDOR, P.MODEL), body),
         _table(tab, [38, 46, 40, 38], right=(1, 2)),
         Spacer(1, 4),
         Paragraph("3. How the counties are compared", h2),
         Paragraph("The board compares the counties on the expected annual hurricane loss the round removes from the "
                   "county's portfolio in 2027. That is the portfolio's 2027 annual expected loss under %s as the vendor "
                   "modeled it, less its 2027 annual expected loss with every home on the portfolio carrying a "
                   "FORTIFIED Roof. Losses are the vendor's: gross of reinsurance, after each home's named-storm "
                   "deductible. The vendor does not model the FORTIFIED Roof for us, so the loss with the roof is the "
                   "vendor's event losses adjusted for the roof's effect as our own named-storm claims show it, an "
                   "adjustment that has to meet our standard MG-04 before it is used. Because the round costs the same "
                   "everywhere, the county where the round removes the most expected annual loss gets it." % P.MODEL, body),
         Paragraph("4. Records", h2),
         Paragraph("The claims system's payment lines since it went live on January 1, 2012 and the legacy system's "
                   "valuations before that; the in-force extract at each storm's landfall; the storm footprints from "
                   "the analysis service; the named-storm register; the policy master; the FORTIFIED certificate "
                   "register; the counties' permit portals; and the vendor's event loss table and hazard summary for "
                   "the four portfolios. The claims department's close-out summaries and the 2026-27 reinsurance "
                   "program are attached for reference.", body)]
    _pdf(path, "2027 FORTIFIED Roof grant round: choosing the county", "Board brief BRD-2026-118", s,
         "%s  |  Board brief BRD-2026-118  |  Confidential" % P.ORG, "2026-11-06")


def mg04(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("MG-04 Adjustments to vendor catastrophe model losses", h1),
         Paragraph("Model governance standard. Owner: %s, %s. Version 2.0, approved by the Risk Committee "
                   "March 18, 2025. Supersedes version 1.3 (2021)." % (P.PEOPLE["cro"], P.TITLES["cro"]), small),
         Paragraph("1. Scope", h2),
         Paragraph("This standard applies whenever the company changes the event losses in a vendor catastrophe model "
                   "output to reflect a feature of its own book that the vendor did not model: a construction or "
                   "occupancy class, a mitigation feature, a territory, a claims practice. It applies to pricing, "
                   "capital, reinsurance and program work alike.", body),
         Paragraph("2. What an adjustment is", h2),
         Paragraph("An adjustment changes each event's modeled loss in the vendor's event loss table, and the adjusted "
                   "annual expected loss is the sum over events of the event's annual rate times its adjusted mean "
                   "loss. The adjustment is derived from the company's own paid claims on homes carrying the feature "
                   "against its homes without it.", body),
         Paragraph("3. The reproduction test", h2),
         Paragraph("Before an adjustment is used it must reproduce the company's own record. The test runs over every "
                   "named storm from the 2012 season on in which the company paid at least USD %s million on homes "
                   "carrying the feature. For each such storm, the adjustment is applied to the paid loss per dollar of "
                   "Coverage A of the company's homes without the feature in the same ZIP code in the same storm, times "
                   "the Coverage A of the homes with the feature in that ZIP code, and summed over the ZIP codes; the "
                   "result has to come within %d percent of what the company actually paid on the homes with the "
                   "feature in that storm. An adjustment that misses on any storm in the test is not used." %
                   (P.MG04_MIN_PAID // 1_000_000, round(P.MG04_TOL * 100)), body),
         Paragraph("4. Definitions", h2),
         Paragraph("Paid loss is the sum of every payment line on the claims the claims system codes to the storm, "
                   "indemnity and supplements, net of recoveries, as at the date of the test. Coverage A is as in force "
                   "at the storm's landfall in the in-force extract. A home carries a mitigation feature where the "
                   "claims system and the in-force extract record its credit at the date of loss. The adjustment is "
                   "derived from the same storms the test runs over: the named storms from 2012 on.", body),
         Paragraph("5. Records kept", h2),
         Paragraph("The test's storm-by-storm table is kept with the analysis it supports and is reviewed by Model "
                   "Risk before the result goes to a committee or the board.", body)]
    _pdf(path, "MG-04 Adjustments to vendor catastrophe model losses", "Model governance standard MG-04 v2.0", s,
         "%s  |  MG-04 v2.0  |  Internal" % P.ORG, "2025-03-18")


def vendor_note(path, elt):
    body, h1, h2, small = _styles()
    n_ev = elt.event_id.nunique()
    s = [Paragraph("%s: event loss tables for Sandpiper Mutual's 2027 retrofit portfolios" % P.MODEL, h1),
         Paragraph("Release note from %s to %s, Catastrophe Risk. October 21, 2026. Job SPM-2610-04." %
                   (P.VENDOR, P.PEOPLE["cat"]), small),
         Paragraph("1. What was run", h2),
         Paragraph("The four exposure files received on October 8, 2026 (portfolio codes %s) were run through the %s "
                   "Gulf hurricane model, near-term view, against its stochastic set of %s landfalling and bypassing "
                   "events for the Gulf coast segment that covers your territory. Each portfolio was modeled on the "
                   "attributes in the exposure file: construction, year built and roof cover as submitted, "
                   "and no mitigation credits." % (", ".join(P.PORTFOLIO_CODE[c] for c in P.CANDIDATES), P.MODEL,
                                                   "{:,}".format(n_ev)), body),
         Paragraph("2. The event loss table", h2),
         Paragraph("One row per event per portfolio with a modeled loss: the event's annual rate of occurrence, the "
                   "mean loss and its standard deviation, and the portfolio's exposed value. Losses are ground-up "
                   "damage less each location's named-storm deductible (2 percent of Coverage A), before reinsurance, "
                   "with the model's standard loss amplification. Rates are annual Poisson rates; a portfolio's annual "
                   "expected loss is the sum over events of rate times mean loss.", body),
         Paragraph("3. The hazard summary", h2),
         Paragraph("For each event and portfolio, the event's peak 3-second gust at 10 m at the portfolio's "
                   "value-weighted centroid, reported in 10 mph classes, and the coast segment of landfall. Event "
                   "references in the hazard summary carry the prefix HU27- and a seven-digit event number; they are "
                   "the same events as the numeric ids in the event loss table.", body),
         Paragraph("4. Limitations", h2),
         Paragraph("Secondary uncertainty is reported as a standard deviation only. Flood from storm surge is not in "
                   "these tables; it is excluded from the policies modeled.", body)]
    _pdf(path, "%s release note: Sandpiper Mutual retrofit portfolios" % P.MODEL, "Release note SPM-2610-04", s,
         "%s  |  SPM-2610-04  |  Prepared for Sandpiper Mutual" % P.VENDOR, "2026-10-21",
         author=P.VENDOR, producer="Corvane Client Reporting")


def closeout(path, claims_df, reg):
    body, h1, h2, small = _styles()
    rows = [["Storm", "Landfall", "Close-out date", "Claims reported", "Claims paid", "Paid at close-out (USD)"]]
    for _, r in reg[reg.landfall_date.str[:4].astype(int) >= 2012].iterrows():
        d = claims_df[claims_df.catastrophe_code == r.claims_catastrophe_code]
        land = pd.Timestamp(r.landfall_date)
        base = d.claim_number.str.replace(r"-S\d$", "", regex=True)
        # the surge desk stays open longer on the big storms; the hand-over day falls where the regional teams take it
        lag = 112 + min(64, base.nunique() // 240) + sum(map(ord, r.storm_name)) % 19
        close = land + pd.Timedelta(days=int(lag))
        close = (close + pd.Timedelta(days=max(0, 7 - close.weekday()) if close.weekday() >= 5 else 0)).date()
        upto = d[d.payment_date <= close.isoformat()]
        rep = base[d.reported_date <= close.isoformat()].nunique()
        paid_claims = upto.assign(base=base).groupby("base").amount_usd.sum()
        rows.append([r.storm_name, r.landfall_date, close.isoformat(), "{:,}".format(rep),
                     "{:,}".format(int((paid_claims > 0).sum())), "{:,.0f}".format(upto.amount_usd.sum())])
    s = [Paragraph("Named-storm close-out summaries, 2012 to 2025", h1),
         Paragraph("Claims Department. Compiled by %s, %s, February 9, 2026, from each storm's close-out memo." %
                   (P.PEOPLE["claims"], P.TITLES["claims"]), small),
         Paragraph("Each storm's catastrophe team closes out four to six months after landfall, when the surge desk "
                   "hands the remaining open claims to the regional teams. The figures are as reported in the "
                   "close-out memo; payments made after the close-out are not in them.", body),
         _table(rows, [36, 22, 24, 24, 20, 32], right=(3, 4, 5))]
    _pdf(path, "Named-storm close-out summaries 2012-2025", "Claims Department close-out summaries", s,
         "%s  |  Claims Department  |  Internal" % P.ORG, "2026-02-09")


def reinsurance(path):
    body, h1, h2, small = _styles()
    rows = [["Layer", "Cover (USD million)", "Retention (USD million)", "Placed", "Rate on line", "Reinstatement"],
            ["1st catastrophe excess", "60", "40", "100%", "21.5%", "1 @ 100%"],
            ["2nd catastrophe excess", "100", "100", "100%", "11.0%", "1 @ 100%"],
            ["3rd catastrophe excess", "150", "200", "95%", "5.8%", "1 @ 100%"],
            ["Aggregate stop loss", "40", "70 (annual)", "100%", "9.4%", "none"]]
    s = [Paragraph("Catastrophe reinsurance program, June 1, 2026 to May 31, 2027", h1),
         Paragraph("Summary for the Risk Committee, May 28, 2026. Prepared by %s." % P.PEOPLE["cat"], small),
         Paragraph("The program renews each June 1. Occurrence layers respond to a named storm's losses within a "
                   "96-hour period; the aggregate cover responds to the year's retained catastrophe losses above the "
                   "annual retention, events of USD 1 million or more counting toward it.", body),
         _table(rows, [42, 26, 30, 16, 22, 26], right=(1, 2, 3, 4)),
         Spacer(1, 6),
         Paragraph("The 2027 renewal will be priced on the vendor's near-term view of the whole book. The reinsurers "
                   "have asked for our mitigation counts by county at the February submission.", body)]
    _pdf(path, "Catastrophe reinsurance program 2026-27", "Risk Committee summary", s,
         "%s  |  Reinsurance  |  Confidential" % P.ORG, "2026-05-28")


def quotes(path, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "Quotes"
    ws["A1"] = "FORTIFIED Roof re-roof quotes for the 2027 round (contractor panel, received to 14 Oct 2026)"
    ws["A1"].font = Font(bold=True)
    hdr = ["County", "Contractor", "Typical roof (sq)", "Quote per home (USD)", "Deck re-nail and seal", "Lead time (weeks)",
           "Panel since"]
    for j, h in enumerate(hdr):
        c = ws.cell(3, j + 1, h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE5EC")
    names = ["Gulfline Roofing", "Bayside Exteriors", "Tri-County Roof Co.", "Coastal Shield Roofing", "Pinewood Builders",
             "Delta Roof Systems", "Harbor Point Roofing", "Southern Ridge Contracting"]
    r = 4
    base = {"MRS": 16800, "HRB": 15400, "CLF": 14100, "CYR": 15900}
    for c in P.CANDIDATES:
        for k in range(4):
            ws.cell(r, 1, P.COUNTY_NAME[c])
            ws.cell(r, 2, names[(k * 3 + P.CANDIDATES.index(c)) % len(names)])
            ws.cell(r, 3, int(rng.integers(20, 34)))
            ws.cell(r, 4, int(round(base[c] * float(rng.uniform(0.9, 1.12)), -2)))
            ws.cell(r, 5, "included" if rng.random() < 0.7 else "USD %d extra" % int(round(float(rng.uniform(600, 1400)), -1)))
            ws.cell(r, 6, int(rng.integers(3, 11)))
            ws.cell(r, 7, int(rng.integers(2014, 2025)))
            r += 1
    for col, wdt in zip("ABCDEFG", (16, 28, 16, 20, 22, 18, 12)):
        ws.column_dimensions[col].width = wdt
    wb.save(path)
    postprocess.scrub(path, PRODUCER, "2026-10-14")
    postprocess.finish_office(path, "2026-09-22T14:02:00Z", "2026-10-14T16:48:00Z", P.ORG, "Sherry Lang")


def build(target, w):
    p = lambda k: os.path.join(target, P.FILES[k])
    pf = pd.read_csv(p("portfolios"))
    brief(p("brief"), pf)
    mg04(p("mg04"))
    vendor_note(p("vendor"), pd.read_parquet(p("elt")))
    cl = pd.read_csv(p("claims"), dtype=str, keep_default_na=False)
    cl["amount_usd"] = cl.amount_usd.astype(float)
    closeout(p("closeout"), cl, pd.read_csv(p("storms"), dtype=str).fillna(""))
    reinsurance(p("reins"))
    quotes(p("quotes"), np.random.default_rng(R.REC_SEED + 5))
