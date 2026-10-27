"""The pack's documents: the performance squad's charter, the image CDN contract's schedule of charges, the domains
runbook."""
from __future__ import annotations

import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402
import world as W    # noqa: E402

FONT_DIR = next((d for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"),
                              "/Library/Fonts/") if os.path.exists(d + "LiberationSerif-Regular.ttf")),
                "/usr/share/fonts/truetype/liberation/")
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY, RULE, TEAL = (colors.HexColor("#1d2226"), colors.HexColor("#5b6268"), colors.HexColor("#a3abb2"),
                         colors.HexColor("#0f5c63"))
BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
CL = ParagraphStyle("c", parent=BODY, leftIndent=24, firstLineIndent=-24)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=16, leading=20, textColor=TEAL, spaceAfter=2)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.4, leading=11, textColor=GREY, spaceAfter=10)
NOTE = ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10, textColor=GREY, spaceBefore=8)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.8, leading=11.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=22 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(22 * mm, A4[1] - 12 * mm, left)
        canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 12 * mm, right)
        canvas.drawRightString(A4[0] - 22 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def write_charter(path):
    head = K.PEOPLE["head"]
    story = [Paragraph("Performance squad charter", H1),
             Paragraph("Brolga Media, Web Platform. Owner: %s, Head of Web Platform. Version 2026.2, revised 20 July "
                       "2026; replaces the 2024 charter." % head, META)]
    sections = [
        ("1. Purpose", [
            "1.1 The web platform team keeps one performance squad. Each quarter the squad works on one of the "
            "group's six properties (Tideline, Matchday, Hearth, Ledger, Trailhead and Pantry), runs its hero-image "
            "playbook there, and moves on when the quarter ends."]),
        ("2. Where the squad goes", [
            "2.1 The squad goes, each quarter, to the property where its playbook will move the most page loads a "
            "month into the good Largest Contentful Paint (LCP) band.",
            "2.2 Page loads are counted on the group's own RUM for the latest complete calendar month, in Sydney "
            "time, before the quarter's planning. A page load is a navigation of any type that reports LCP, a reload or "
            "a prerendered page included. The RUM samples "
            "each origin's page loads at the rate its collector is set to when the load starts, and a sampled "
            "load's beacon stands for the page loads that rate represents.",
            "2.3 The good band is an LCP of 2,500 ms or less. A page load moved into the good band is one that was "
            "slower than 2,500 ms in that month and would have been 2,500 ms or less with the playbook in place.",
            "2.4 The playbook works on a property's own hero images: the images the property serves itself, from "
            "its image host, from a legacy alias of it, or from its path on the group image CDN (the domains "
            "runbook). A load whose LCP element is anything else (text, an agency photo, an ad creative, a video "
            "poster) is out of the playbook's reach."]),
        ("3. The playbook", [
            "3.1 The playbook is the four steps on the Playbook sheet of the squad's change log: hero images served "
            "from the group image CDN, encoded as AVIF at the hero slot's size, preloaded with high fetch priority, "
            "and never lazy-loaded.",
            "3.2 The squad does no work on time to first byte, scripts, fonts, ad slots or the render path; those "
            "belong to the property teams."]),
        ("4. Engagements", [
            "4.1 Every engagement is logged in the squad's change log with its windows and reviewed on the group "
            "RUM. The squad keeps each engagement's review extract."]),
        ("5. The quarterly assignment", [
            "5.1 The web platform steering group assigns the squad at its planning meeting in the last month of "
            "each quarter, on a paper from the head of web platform, from the RUM and image extracts and the latest "
            "nightly site crawl taken for it. The assignment for the quarter starting "
            "5 January 2027 is made on 8 December 2026 from the extracts of 3 December.",
            "5.2 The assignment paper gives, for each property, the page loads a month the playbook would move into "
            "the good band. Beside them it carries two figures the squad lead plans the quarter with: the hero-image "
            "egress the group image CDN would serve each month once the property's hero images move, costed on the "
            "same month's hero-image requests at the CDN contract's rate, and the live hero images the squad would "
            "convert to AVIF."]),
    ]
    for h, paras in sections:
        story.append(Paragraph(h, H2))
        for t in paras:
            story.append(Paragraph(t, CL))
    story.append(Paragraph("The LCP bands are those of Core Web Vitals: good at 2,500 ms or less, poor above "
                           "4,000 ms.", NOTE))
    doc = _doc(path, "Performance squad charter", head)
    f = _frame("Brolga Media  |  Web Platform", "Performance squad charter, version 2026.2")
    doc.build(story, onFirstPage=f, onLaterPages=f)


def write_contract(path):
    story = [Paragraph("Schedule 2: Charges", H1),
             Paragraph("Image CDN services agreement between Brolga Media Pty Ltd and %s, effective 1 February 2026 "
                       "for three years. This schedule sets the charges for the group image CDN (%s)."
                       % (K.CDN_VENDOR, K.CDN_HOST), META)]
    rows = [[Paragraph("Item", CELLB), Paragraph("Charge", CELLB), Paragraph("Basis", CELLB)],
            [Paragraph("Egress to end users", CELL), Paragraph("AUD %.3f per GB" % K.CDN_RATE_AUD_PER_GB, CELL),
             Paragraph("Bytes delivered to end users in the month; a GB is 1,000,000,000 bytes", CELL)],
            [Paragraph("Requests", CELL), Paragraph("no charge", CELL), Paragraph("", CELL)],
            [Paragraph("Origin pulls", CELL), Paragraph("no charge", CELL),
             Paragraph("Fetches from Brolga's image store on a cache miss", CELL)],
            [Paragraph("Storage", CELL), Paragraph("no charge to 20 TB", CELL),
             Paragraph("AUD 18.00 per TB a month above 20 TB", CELL)],
            [Paragraph("Edge image transformation", CELL), Paragraph("not taken up", CELL),
             Paragraph("Brolga delivers images as stored", CELL)]]
    t = Table(rows, colWidths=[52 * mm, 38 * mm, 76 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story += [t, Spacer(1, 8)]
    for line in ["2.1 All charges are in Australian dollars and include GST.",
                 "2.2 Charges are invoiced monthly in arrears; the invoice states the month's egress in GB to three "
                 "decimal places.",
                 "2.3 The rates hold for the term; clause 9 of the agreement covers a change of volume tier, which "
                 "does not apply below 2 PB a month."]:
        story.append(Paragraph(line, CL))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Signed for Brolga Media Pty Ltd: %s, Head of Web Platform, 28 January 2026. Signed for "
                           "%s: Commercial Director, 29 January 2026." % (K.PEOPLE["head"], K.CDN_VENDOR), META))
    doc = _doc(path, "Image CDN services agreement: Schedule 2, Charges", K.PEOPLE["head"])
    f = _frame("Image CDN services agreement", "Schedule 2")
    doc.build(story, onFirstPage=f, onLaterPages=f)


def write_runbook(path):
    P = {p["code"]: p for p in K.PROPERTIES}
    lines = [
        "# Domains runbook: web properties and image hosts", "",
        "Owner: %s, site reliability. Last reviewed 24 November 2026." % K.PEOPLE["sre"], "",
        "## Page origins", "",
        "Each property is served from its www origin:", ""]
    for p in K.PROPERTIES:
        lines.append("- %s: `%s`" % (p["name"], p["origin"]))
    lines += ["", "The group's small sites (Clutch, Tenancy, Fairway, Undercurrent, Brolga Kids, Tidewater, Paddock) "
                  "run on the same platform; cdn_host_list.csv lists them.", "",
              "## Image hosts", "",
              "Each property serves its images from its own image host, `images.<property>.brolga.au`, under "
              "`/i/<width>x<height>/<yyyy>/<mm>/<file>`, one directory per slot size.", "",
              "## Legacy aliases", "",
              "`%s` and `%s` are the old media server's names for Hearth's and Trailhead's images. They were retired "
              "for new links on %s (WEBPLAT-2297). Pages published before each property's image host went live "
              "(Hearth's on %s, Trailhead's on %s) still link to them, and the old media server still answers those "
              "requests from the same image store."
              % (P["hearth"]["alias"][0], P["trailhead"]["alias"][0], P["hearth"]["alias"][1].strftime("%-d %B %Y"),
                 W.ALIAS_BEFORE["hearth"].strftime("%-d %B %Y"), W.ALIAS_BEFORE["trailhead"].strftime("%-d %B %Y")),
              "", "## Group image CDN", "",
              "`%s`, run for us by %s under the image CDN services agreement. Each site has a path prefix, "
              "`/<site>/` (cdn_host_list.csv), followed by the same `/i/<width>x<height>/` layout as the image hosts. "
              "The small sites' paths date from the squad's first engagement in February 2024; the six properties' "
              "from 16 June 2025, when pages in Tideline's opinion section, Matchday's racing section and Pantry's "
              "baking section moved their images onto it." % (K.CDN_HOST, K.CDN_VENDOR), "",
              "## Third-party hosts", "",
              "Not ours, and never moved: `%s` and `%s` (agency photos), `%s` (ad creatives), `%s` (video posters)."
              % (K.AGENCY_HOSTS[0], K.AGENCY_HOSTS[1], K.AD_HOSTS[0], K.VIDEO_HOST), "",
              "## Changes", "",
              "- 14 August 2026: legacy aliases retired for new links (WEBPLAT-2297)",
              "- 16 June 2025: image CDN paths for the six properties (WEBPLAT-1630)",
              "- 10 March 2025: three sections moved with their pages and images: Hearth's real-estate to Ledger "
              "(`/property/`), Tideline's travel to Trailhead (`/getaways/`), Matchday's game-day food to Pantry "
              "(`/game-day/`); the old URLs answer with a 301 (WEBPLAT-1544)",
              "- 5 February 2024: image CDN paths for the small sites, with the squad's first engagement",
              ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
