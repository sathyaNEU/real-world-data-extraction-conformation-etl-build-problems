"""The pack's documents: the district's surveillance and control protocol, the aerial application agreement, the county
laboratory's week-32 report and the field database's data dictionary."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import letter                                         # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import inch                                               # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W      # noqa: E402

PROTOCOL = "RCVCD_surveillance_and_control_protocol_2026.pdf"
CONTRACT = "Ostby_Aviation_aerial_ULV_agreement_2026.pdf"
COUNTY = "RCPHL_arbovirus_report_2026-W32_RCVCD.pdf"
DICTIONARY = "field_database_data_dictionary.txt"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Serif", "LiberationSerif-Regular"),
              ("Serif-B", "LiberationSerif-Bold"), ("Mono", "LiberationMono-Regular")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY, RULE = colors.HexColor("#1c2430"), colors.HexColor("#5b6470"), colors.HexColor("#9aa3ad")

BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("c", parent=BODY, leftIndent=28, firstLineIndent=-28)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=14, leading=18, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=8, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.2, leading=10.6, textColor=GREY, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.2, leading=9.8, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")
SBODY = ParagraphStyle("sb", fontName="Serif", fontSize=10.2, leading=13.6, textColor=INK, spaceAfter=5)
SCLAUSE = ParagraphStyle("sc", parent=SBODY, leftIndent=30, firstLineIndent=-30)
SH1 = ParagraphStyle("sh1", fontName="Serif-B", fontSize=13, leading=17, textColor=INK, spaceAfter=3)
SH2 = ParagraphStyle("sh2", fontName="Serif-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
SMETA = ParagraphStyle("smeta", fontName="Serif", fontSize=8.8, leading=11.2, textColor=GREY, spaceAfter=8)
LAB = ParagraphStyle("lab", fontName="Sans", fontSize=8.6, leading=11.4, textColor=INK, spaceAfter=4)
LABH = ParagraphStyle("labh", fontName="Sans-B", fontSize=11.5, leading=14.5, textColor=INK, spaceAfter=2)


def _doc(path, title, author, margin=0.85):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=margin * inch, rightMargin=margin * inch,
                             topMargin=0.8 * inch, bottomMargin=0.75 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _frame(top_left, top_right, foot, font="Sans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.6)
        canvas.drawString(0.85 * inch, letter[1] - 0.45 * inch, top_left)
        canvas.drawRightString(letter[0] - 0.85 * inch, letter[1] - 0.45 * inch, top_right)
        canvas.setFont(font, 7.0)
        canvas.drawString(0.85 * inch, 0.42 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.42 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _zones(names):
    return ", ".join(names[:-1]) + " and " + names[-1]


PROTOCOL_CLAUSES = [
    ("1  Purpose and season", [
        ("1.1", "This protocol sets how the district samples adult mosquitoes, tests them for West Nile virus and books "
                "the adult mosquito control it buys, for the 2026 season of 1 June to 30 September."),
        ("1.2", "Weeks are MMWR weeks, Sunday to Saturday, numbered as the CDC numbers them."),
    ]),
    ("2  Treatment zones", [
        ("2.1", "The district treats eight zones: %s. Each zone is a set of whole sections of the public land "
                "survey." % _zones(W.ZONES)),
        ("2.2", "The zones were redrawn on 1 May 2026. The sections in each zone are listed in the 2026 site register "
                "(sheet Zone sections) and mapped in the zones file."),
        ("2.3", "Each zone is one block for aerial application."),
    ]),
    ("3  Adult mosquito sampling", [
        ("3.1", "CO2-baited light traps (CDC miniature light traps baited with 2 kg of dry ice, light off) stand at "
                "fixed sites in every zone. They draw females looking for a blood meal."),
        ("3.2", "Gravid traps (hay infusion) stand at fixed sites in Old Town and Riverside South, where catch basins "
                "and backyard containers breed Culex pipiens. They draw females looking for water to lay their eggs "
                "in, each of which has already taken a blood meal."),
        ("3.3", "Both kinds of trap are set on Monday and Tuesday nights each week from 1 June, before dusk, and "
                "picked up the next morning. A site runs one trap a night."),
        ("3.4", "A trap-night is one trap run from its set to its pickup. A trap that failed overnight (fan stopped, "
                "dry ice gone before dusk, battery failed, trap missing at pickup) is recorded with its failure code "
                "and is not a trap-night. A trap that was not set is recorded NS."),
        ("3.5", "After a zone's first positive pool of the season the district may add Wednesday and Thursday nights "
                "at the zone's CO2 sites for up to two weeks (enhanced trapping)."),
        ("3.6", "Each trap-night's catch is identified to species and sexed at the district's bench. Females per "
                "trap-night are the females caught over the trap-nights run."),
    ]),
    ("4  Pooling and testing", [
        ("4.1", "Culex tarsalis and Culex pipiens females are pooled by trap-night and species. Pools hold up to 50 "
                "females for the district laboratory, which tests the pools of North Bottoms, Maple Ridge, Westbrook "
                "and Old Town, and up to 10 for the Rindal County Public Health Laboratory, which tests the pools of "
                "Riverside South, South Prairie, Coulee Hills and Airport East under the interlocal agreement and "
                "whose extraction takes no more than 10. A trap-night's females of a species fill whole pools first "
                "and the remainder makes the last pool."),
        ("4.2", "Males, other species and Culex not identified to species are counted and not pooled."),
        ("4.3", "Pools are tested for West Nile virus RNA by real-time RT-PCR. A cycle threshold (Ct) of 35.0 or under "
                "is positive, 35.1 to 38.0 is inconclusive, and no amplification by cycle 38 is negative. An "
                "inconclusive pool is extracted again and retested, and the retest is the final result: positive at "
                "35.0 or under, otherwise negative."),
        ("4.4", "The county laboratory reports each week's pools by PDF on the Friday after the trap-nights. The "
                "district keys the county results into the field database on the following Monday. District "
                "laboratory results are entered as they are read."),
    ]),
    ("5  The weekly cycle and adult control", [
        ("5.1", "Trap-nights are Monday and Tuesday; county results come on Friday and district results by Saturday."),
        ("5.2", "The district buys one aerial ultra-low-volume adulticide block a week under its agreement with %s, "
                "flown on Thursday night, weather permitting. The Operations Manager names the block by 17:00 on "
                "Monday, on the week just ended." % W.APPLICATOR),
        ("5.3", "Truck-mounted ground fogging in residential streets runs on its own schedule and is not booked under "
                "this protocol."),
    ]),
    ("6  Records", [
        ("6.1", "The field database holds the trap sites, trap-nights, catches, pools and test results."),
        ("6.2", "Records to 14 June 2026 were kept in the legacy system under legacy site codes and were migrated to "
                "the field database on 15 June 2026 under new site IDs. The register's Crosswalk sheet maps each "
                "legacy code to its site ID. The June records were loaded again on 22 June 2026, after the first load "
                "was reported short; records from that run carry the time of the import run in entered."),
        ("6.3", "Human case reports are Rindal County Public Health's. The county epidemiologist shares her case log "
                "with the district each week."),
    ]),
]


def write_protocol(path):
    who, role = W.PEOPLE["surv"]
    boss, brole = W.PEOPLE["ops"]
    title = "Mosquito surveillance and adult control protocol, 2026 season"
    doc = _doc(path, title, who)
    s = [Paragraph(W.DISTRICT.upper(), META),
         Paragraph(title, H1),
         Paragraph("Issued 27 April 2026, revised 26 June 2026 by %s, %s. Approved by %s, %s." % (
             who, role, boss, brole), META)]
    for head, items in PROTOCOL_CLAUSES:
        s.append(Paragraph(head, H2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), CLAUSE))
    s.append(Spacer(1, 8))
    rows = [[Paragraph(x, CELLB) for x in ("Season", "Issued", "Change")],
            [Paragraph(x, CELL) for x in ("2024", "22 April 2024", "Gravid traps added in Old Town and Riverside South")],
            [Paragraph(x, CELL) for x in ("2025", "21 April 2025", "Retest of inconclusive pools")],
            [Paragraph(x, CELL) for x in ("2026", "27 April 2026", "Season dates; zone redraw of 1 May")],
            [Paragraph(x, CELL) for x in ("2026 rev. 1", "26 June 2026", "Field database and site IDs from 15 June; "
                                                                        "pooling at the county laboratory")]]
    t = Table(rows, colWidths=[0.8 * inch, 1.3 * inch, 4.6 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    s.append(t)
    foot = W.DISTRICT + " | Surveillance and control protocol | 2026, revision 1"
    doc.build(s, onFirstPage=_frame(W.DISTRICT_SHORT, "Protocol 2026 rev. 1", foot),
              onLaterPages=_frame(W.DISTRICT_SHORT, "Protocol 2026 rev. 1", foot))


CONTRACT_CLAUSES = [
    ("1  Services", [
        ("1.1", "The Contractor shall apply mosquito adulticide by air, at ultra-low volume, over the treatment blocks "
                "the District designates, from 1 July to 15 September 2026."),
        ("1.2", "A treatment block is one of the District's treatment zones as the District's zone map stands on the "
                "day of designation."),
    ]),
    ("2  Weekly application", [
        ("2.1", "The District may designate one block a week. The Contractor shall fly the designated block on the "
                "Thursday night of that week, beginning no earlier than 30 minutes after sunset."),
        ("2.2", "The District shall designate the block by e-mail to the Contractor by 17:00 Central time on the "
                "Monday before the flight. A designation names one block; a block is not split across nights or "
                "aircraft."),
        ("2.3", "If the flight cannot be made on Thursday night under clause 3, the Contractor shall fly the same "
                "block on Friday night; a block not flown by Friday night lapses and is not carried into the next "
                "week."),
    ]),
    ("3  Weather and operating limits", [
        ("3.1", "The Contractor shall not spray when the wind at release height is under 2 or over 10 miles per hour, "
                "when the air temperature at release height is under 55 degrees Fahrenheit, or during rain."),
        ("3.2", "Release height 300 feet above ground; swath 1,500 feet; droplet volume median diameter 15 to 25 "
                "micrometres, verified by the Contractor's annual calibration."),
    ]),
    ("4  Product, rate and records", [
        ("4.1", "Product: a pyrethroid with piperonyl butoxide registered for aerial ULV mosquito adulticiding in North "
                "Dakota, supplied by the District, at the label's maximum rate for the target."),
        ("4.2", "The Contractor shall return the flight log and the GPS swath record for each application within two "
                "working days."),
    ]),
    ("5  Fees", [
        ("5.1", "The District shall pay $3.85 an acre treated, plus a mobilisation fee of $1,150 for each night "
                "flown. No fee is due for a block that lapses for weather."),
    ]),
]


def write_contract(path):
    who, role = W.PEOPLE["pilot"]
    boss, brole = W.PEOPLE["ops"]
    title = "Agreement for aerial ULV adulticide application, 2026 season"
    doc = _doc(path, title, boss)
    s = [Paragraph("%s and %s" % (W.DISTRICT.upper(), W.APPLICATOR.upper()), SMETA),
         Paragraph(title, SH1),
         Paragraph("Between %s (the District) and %s, of %s (the Contractor). Dated 9 March 2026." % (
             W.DISTRICT, W.APPLICATOR, W.AIRPORT), SMETA)]
    for head, items in CONTRACT_CLAUSES:
        s.append(Paragraph(head, SH2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), SCLAUSE))
    s.append(Spacer(1, 14))
    sig = [[Paragraph("For the District", SBODY), Paragraph("For the Contractor", SBODY)],
           [Paragraph("%s, %s" % (boss, brole), SBODY), Paragraph("%s, %s" % (who, role), SBODY)]]
    t = Table(sig, colWidths=[3.3 * inch, 3.3 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s.append(t)
    foot = "Aerial ULV agreement 2026 | %s and %s" % (W.DISTRICT_SHORT, W.APPLICATOR)
    doc.build(s, onFirstPage=_frame(W.APPLICATOR, "Agreement 2026", foot, "Serif"),
              onLaterPages=_frame(W.APPLICATOR, "Agreement 2026", foot, "Serif"))


def us(d):
    return d.strftime("%m/%d/%Y")


def write_county_report(path, pools, site_of):
    """pools: the county laboratory's week-32 pools for the district, each with sample_no, site_id, collected,
    species, females, result, ct, retest_ct, final."""
    title = "West Nile virus RT-PCR results, mosquito pools"
    doc = _doc(path, title, "", margin=0.7)
    first = min(p["collected"] for p in pools)
    last = max(p["collected"] for p in pools)
    npos = sum(1 for p in pools if p["final"] == "POS")
    by_sp = {}
    for p in pools:
        nm = W.SPECIES[p["species"]]
        a = by_sp.setdefault(nm, [0, 0, 0])
        a[0] += 1
        a[1] += p["females"]
        a[2] += p["final"] == "POS"
    s = [Paragraph("RINDAL COUNTY PUBLIC HEALTH LABORATORY · ARBOVIRUS SECTION", META),
         Paragraph(title, LABH),
         Paragraph("Submitter: %s. Pools collected %s to %s, received %s to %s. Report date %s." % (
             W.DISTRICT, us(first), us(last), us(first + dt.timedelta(days=1)), us(last + dt.timedelta(days=1)),
             "08/14/2026"), LAB),
         Paragraph("Method: real-time RT-PCR, West Nile virus envelope target, on RNA extracted from each pool. Ct 35.0 "
                   "or under: positive. Ct 35.1 to 38.0: inconclusive, extracted again and retested (Table 2). No "
                   "amplification by cycle 38: negative (Ct shown as Undet.).", LAB),
         Paragraph("Pools tested: %d. Positive after retest: %d. %s." % (
             len(pools), npos, "; ".join("%s: %d pools, %d mosquitoes, %d positive" % (k, v[0], v[1], v[2])
                                        for k, v in sorted(by_sp.items()))), LAB),
         Spacer(1, 4),
         Paragraph("Table 1. Pools tested", CELLB), Spacer(1, 2)]
    head = ["Accession", "Submitter site", "Collected", "Species", "No. in pool", "Ct", "Result"]
    rows = [[Paragraph(h, CELLB) for h in head]]
    word = {"POS": "Positive", "NEG": "Negative", "INC": "Inconclusive"}
    for p in pools:
        ct = "Undet." if p["ct"] is None else "%.1f" % p["ct"]
        rows.append([p["sample_no"], p["site_id"], us(p["collected"]), W.SPECIES[p["species"]], str(p["females"]), ct,
                     word[p["result"]]])
    t = LongTable(rows, colWidths=[1.15 * inch, 1.0 * inch, 0.9 * inch, 1.25 * inch, 0.8 * inch, 0.6 * inch,
                                   0.95 * inch], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("FONTNAME", (0, 1), (-1, -1), "Sans"), ("FONTSIZE", (0, 1), (-1, -1), 7.8),
                           ("LEADING", (0, 1), (-1, -1), 9.2), ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
                           ("ALIGN", (4, 1), (5, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 1.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2), ("TEXTCOLOR", (0, 1), (-1, -1), INK)]))
    s.append(t)
    inc = [p for p in pools if p["result"] == "INC"]
    s += [Spacer(1, 8), Paragraph("Table 2. Retests of inconclusive pools", CELLB), Spacer(1, 2)]
    rows = [[Paragraph(h, CELLB) for h in ("Accession", "Retested", "Ct", "Final result")]]
    for p in inc:
        r = p["retest_ct"]
        rows.append([p["sample_no"], us(p["collected"] + dt.timedelta(days=2)), "%.1f" % r if r <= 38.0 else "Undet.",
                     "Positive" if p["final"] == "POS" else "Negative"])
    if not inc:
        rows.append(["None this report", "", "", ""])
    t = Table(rows, colWidths=[1.15 * inch, 0.9 * inch, 0.6 * inch, 1.0 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("FONTNAME", (0, 1), (-1, -1), "Sans"), ("FONTSIZE", (0, 1), (-1, -1), 7.8),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("TOPPADDING", (0, 0), (-1, -1), 1.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2)]))
    s.append(t)
    s += [Spacer(1, 10),
          Paragraph("Results relate only to the pools as received. Species and pool counts are as stated on the "
                    "submitter's form. Reviewed and released by the Arbovirus Section.", META)]
    foot = "RCPHL Arbovirus Section | Report for %s | 08/14/2026" % W.DISTRICT_SHORT
    doc.build(s, onFirstPage=_frame("Rindal County Public Health Laboratory", "Mosquito pools, RT-PCR", foot),
              onLaterPages=_frame("Rindal County Public Health Laboratory", "Mosquito pools, RT-PCR", foot))


DICTIONARY_TEXT = """{district}
Field database: data dictionary
Kept by {surv} ({surv_role}). Applies to the extract of {extract}.

The field database is a SQLite file. Dates are ISO (YYYY-MM-DD); times are Central time.

Table sites: one row per trap site
  site_id          site ID (RC-nnn), assigned at the 15 June 2026 migration
  trap_type        CO2 (CO2-baited light trap) or GRAVID (gravid trap)
  zone             treatment zone of the site's section
  habitat          habitat at the trap
  section          public land survey section: township, range and section number
  latitude, longitude   decimal degrees (WGS 84)
  in_service_from  first season the site was trapped

Table trap_nights: one row per trap per scheduled night
  tn_id            record number, in order of entry
  site_id          the trap site
  set_date         the evening the trap was set
  pickup_date      the morning the trap was picked up
  status           OK, FAN, CO2, BAT, STOLEN or NS (table status_codes)
  crew             initials of the crew that picked the trap up
  entered          when the record was created: the legacy entry time for records migrated from the legacy system on
                   15 June 2026, and the time of the import run for the records brought in by the re-import of
                   22 June 2026

Table catches: one row per trap-night, species and sex with any catch
  tn_id            the trap-night
  species          species code (table species)
  sex              F or M
  count            mosquitoes counted

Table pools: one row per pool sent for testing
  pool_id          the testing laboratory's sample number: nn-nnnn for the district laboratory, RCPHL-nn-nnnn for the
                   county laboratory (pre-printed labels supplied by the county)
  tn_id            the trap-night whose catch the pool was made from
  species          species code
  females          females in the pool
  lab              RCVCD (district laboratory) or RCPHL (Rindal County Public Health Laboratory)
  sent             the date the pool went to the laboratory

Table pool_tests: one row per RT-PCR test of a pool
  pool_id          the pool
  test_no          1 for the first test, 2 for the retest of an inconclusive first result
  tested           the date of the test
  result           POS, NEG or INC
  ct               cycle threshold; empty when there was no amplification

Table species: the species codes; laboratories write species names in full
Table status_codes: the trap-night status codes

County laboratory results are keyed from the laboratory's weekly PDF report on the Monday after it arrives; the
report of 14 August 2026 (week 32 pools) is in this extract's folder and was not yet keyed. The report lists each pool
by its accession number (the pool_id), with the site ID, the date the trap was collected, the species, the number in
the pool and the result.
"""


def write_dictionary(path):
    who, role = W.PEOPLE["surv"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(DICTIONARY_TEXT.format(district=W.DISTRICT, surv=who, surv_role=role,
                                        extract="17 August 2026, 08:20"))
