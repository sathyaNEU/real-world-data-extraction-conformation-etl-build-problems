"""task286 documents: the pilot's terms of reference, the water company's data sharing agreement, the councils'
Council Taxbase returns and the housing needs assessment summary, each in its own organisation's form and type."""
import os
import re
import logging
from datetime import date

import world as W
import records as R

FONTS = {
    "agency": ("LiberationSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
               "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    "water": ("Carlito", "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
              "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"),
    "county": ("FreeSans", "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
               "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"),
    "consult": ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
}
_REG = set()


def _font(kind):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    name, reg, bold = FONTS[kind]
    if name not in _REG:
        pdfmetrics.registerFont(TTFont(name, reg))
        pdfmetrics.registerFont(TTFont(name + "-Bold", bold))
        addMapping(name, 0, 0, name)
        addMapping(name, 1, 0, name + "-Bold")
        addMapping(name, 0, 1, name)
        addMapping(name, 1, 1, name + "-Bold")
        _REG.add(name)
    return name


def _stamp(d, hh, mm, ss):
    return "%04d%02d%02d%02d%02d%02d+01'00'" % (d.year, d.month, d.day, hh, mm, ss)


def _pdf(path, title, author, story, stamp, header, footer, font):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.units import mm

    def on_page(c, d):
        c.saveState()
        c.setFont(font, 7.5)
        c.setFillGray(0.35)
        c.drawString(20 * mm, 287 * mm, header)
        c.drawString(20 * mm, 10 * mm, footer)
        c.drawRightString(190 * mm, 10 * mm, "Page %d" % d.page)
        c.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=22 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="",
                            producer="", invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    _scrub_pdf(path, stamp)


def _scrub_pdf(path, stamp):
    from pypdf import PdfReader
    raw = open(path, "rb").read()
    before = [p.extract_text() for p in PdfReader(path).pages]
    n0 = len(raw)
    for pat in (rb"ReportLab Generated PDF document \(opensource\)",
                rb"ReportLab generated PDF document -- digest \(opensource\)"):
        for m in re.findall(pat, raw):
            raw = raw.replace(m, b" " * len(m))
    old = b"D:20000101000000+00'00'"
    assert len(("D:" + stamp).encode()) == len(old), stamp
    raw = raw.replace(old, ("D:" + stamp).encode())
    # each embedded subset gets its own six-letter tag, as a word processor's PDF export writes them
    import hashlib
    for m in sorted(set(re.findall(rb"AAAA[A-Z]{2}\+[A-Za-z-]+", raw)), key=lambda x: (-len(x), x)):
        hx = hashlib.sha1(os.path.basename(path).encode() + m).digest()
        tag = bytes(65 + b % 26 for b in hx[:6])
        raw = raw.replace(m, tag + m[6:])
    assert len(raw) == n0 and b"eportLab" not in raw and b"reportlab" not in raw.lower()
    open(path, "wb").write(raw)
    cap = []
    h = logging.Handler()
    h.emit = lambda rec: cap.append(rec)
    logging.getLogger("pypdf").addHandler(h)
    try:
        after = [p.extract_text() for p in PdfReader(path).pages]
    finally:
        logging.getLogger("pypdf").removeHandler(h)
    assert after == before and not cap, (path, cap)


def _styles(font):
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName=font, fontSize=9.6, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName=font + "-Bold", fontSize=15, leading=18, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName=font + "-Bold", fontSize=11, spaceBefore=8,
                        spaceAfter=4)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.2)
    return body, h1, h2, small


def _table(data, widths, font, size=8.5, head=True, extra=()):
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("FONT", (0, 0), (-1, -1), font, size), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.6, 0.6, 0.6)),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if head:
        st += [("FONT", (0, 0), (-1, 0), font + "-Bold", size),
               ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.88, 0.9, 0.93))]
    t.setStyle(TableStyle(st + list(extra)))
    return t


def _p(txt, st):
    from reportlab.platypus import Paragraph
    return Paragraph(txt, st)


# --------------------------------------------------------------------------------------- terms of reference
def write_tor(path):
    from reportlab.platypus import Spacer
    from reportlab.lib.units import mm
    f = _font("agency")
    body, h1, h2, small = _styles(f)
    T = lambda d, w: _table(d, w, f)
    s = [_p("<font size=9 color='#1d4f91'><b>NATIONAL HOMES AGENCY</b></font>", body),
         _p("Homes in Use pilot 2027<br/>Terms of reference", h1),
         _p("Version 1.2, 8 September 2026. Classification: OFFICIAL. Owner: Homes in Use programme team.", small),
         Spacer(1, 4 * mm),
         _p("1. Background", h2),
         _p("Homes that stand empty for long periods take housing out of use where it is needed, cost their owners "
            "and neighbours money and, left long enough, fall into disrepair. The councils' own empty homes work "
            "reaches the homes their records show as empty. The agency wants to know whether a concentrated, "
            "time-limited offer in one place does better, and has agreed with Teversby District Council and "
            "Swanholt Borough Council to test one in a single community area from April 2027.", body),
         _p("2. Purpose", h2),
         _p("Homes in Use is a one-year pilot. It tests whether a dedicated empty homes officer, repair grants and a "
            "leasing offer, concentrated in one community area, bring homes that stand empty back into use faster "
            "than the councils' existing work. The pilot will be evaluated against the chosen area's own baseline "
            "and against the other shortlisted areas.", body),
         _p("3. What the pilot provides", h2),
         _p("From 1 April 2027 to 31 March 2028 the agency will fund, in the chosen area: one full-time empty homes "
            "officer employed by the district council; a repair grant fund of GBP 600,000, with grants of up to GBP "
            "15,000 a home in return for the home being let or lived in within twelve months; and a five-year "
            "leasing offer run with a registered provider, under which the provider manages and lets the home and "
            "pays the owner a guaranteed rent. The officer will contact the owner of every home in the area that "
            "the evidence shows standing empty.", body),
         _p("4. Choosing the pilot area", h2),
         _p("4.1 The pilot will run in the shortlisted community area with the most homes that nobody used for at "
            "least 26 of the 52 weeks from Monday 29 September 2025 to Sunday 27 September 2026.", body),
         _p("4.2 A home is a self-contained dwelling on the county address gazetteer, however it is taxed or rated "
            "and however it is let.", body),
         _p("4.3 A week runs from Monday to Sunday. A week counts as a week of use if anybody lived in, stayed at or "
            "used the home on any day of it, for however short a time.", body),
         _p("4.4 The shortlisted community areas were agreed with the two councils in June 2026: Brackwater, "
            "Wennaby, Quellby and Tarnhithe in Teversby, and Orrimouth, Crackmoor, Ellingsea and Kittlesea in "
            "Swanholt. Community areas are as the county address gazetteer holds them.", body),
         _p("4.5 The agency's Housing Evidence team will prepare the area recommendation. The Minister for Housing "
            "will announce the pilot area.", body),
         _p("5. Evidence", h2),
         _p("5.1 Council tax records show what owners and occupiers have told the councils, which is not always how "
            "a home is used. Pennimouth Water supplies every home in the shortlisted areas through a smart meter "
            "with a daily read. Under data sharing agreement PW-DSA-2026-014 of 1 September 2026 the company will "
            "provide each home's daily metered consumption from 1 September 2025 to 4 October 2026 and its match of "
            "its properties to the county address gazetteer.", body),
         _p("5.2 Teversby District Council and Swanholt Borough Council will provide council tax liability extracts "
            "for the shortlisted areas, including the archive of Teversby's previous revenues system, which the "
            "council replaced on 5 May 2026, and the business rates list's self-catering entries for the same "
            "areas.", body),
         _p("5.3 Census 2021 tables, the councils' Council Taxbase returns and the 2024 Housing Needs Assessment are "
            "available to the team for context.", body),
         _p("6. Governance", h2),
         _p("The Homes in Use project board, chaired by the Deputy Director, Housing Supply, with the two councils' "
            "heads of housing, owns these terms of reference. The board will see the area recommendation before it "
            "goes to the minister, and will receive quarterly reports once the pilot starts. Changes to these terms "
            "need the board's agreement and are recorded in the document control table.", body),
         _p("7. Data protection", h2),
         _p("The agency processes the data under its public task, for the purpose of choosing and running the "
            "pilot. Data identifying a home is held on the agency's secure analysis platform, is not published and "
            "is deleted by 31 March 2028 unless the evaluation needs it to 30 September 2028. Published outputs "
            "report counts by community area only. A data protection impact assessment was approved on 19 August "
            "2026.", body),
         _p("8. Risks", h2),
         T([["Risk", "Mitigation"],
            ["Owners cannot be traced", "The officer will use council tax, Land Registry and probate searches before "
                                        "a first visit."],
            ["Grant demand exceeds the fund", "Grants are offered in order of application; the board may move "
                                              "leasing budget to grants at the six-month review."],
            ["Data arrives late or incomplete", "The evidence pack is due in October 2026, two months before the "
                                                "recommendation is needed."]], [52 * mm, 118 * mm]),
         _p("9. Timetable", h2),
         T([["Milestone", "Date"],
            ["Evidence pack received", "October 2026"],
            ["Area recommendation to the project board", "by 20 November 2026"],
            ["Recommendation to the minister", "by 4 December 2026"],
            ["Announcement of the pilot area", "January 2027"],
            ["Officer in post; grants and leasing open", "1 April 2027"],
            ["Pilot ends", "31 March 2028"],
            ["Evaluation report", "September 2028"]], [110 * mm, 60 * mm]),
         Spacer(1, 4 * mm),
         _p("10. Document control", h2),
         T([["Version", "Date", "Change", "By"],
            ["1.0", "12 June 2026", "First issue for the councils' comments", "M. Robson"],
            ["1.1", "21 July 2026", "Shortlist confirmed (4.4); timetable updated", "M. Robson"],
            ["1.2", "8 September 2026", "Evidence (5.1, 5.2) updated after the data sharing agreement; risks added",
             "M. Robson"]], [18 * mm, 30 * mm, 96 * mm, 26 * mm]),
         Spacer(1, 8 * mm),
         _p("Author: Melissa Robson, Programme Manager, Homes in Use", body),
         _p("Approved for issue by the project board, 8 September 2026.", body),
         _p("Signed: ______________________________&nbsp;&nbsp;Deputy Director, Housing Supply", body)]
    _pdf(path, "Homes in Use pilot 2027: terms of reference", "Melissa Robson", s,
         _stamp(date(2026, 9, 8), 15, 41, 27), "National Homes Agency | Homes in Use pilot 2027 | Terms of reference "
         "v1.2 | OFFICIAL", "HIU-TOR-v1.2", f)


# --------------------------------------------------------------------------------------- data sharing agreement
def write_dsa(path, homes):
    from reportlab.platypus import Spacer
    from reportlab.lib.units import mm
    f = _font("water")
    body, h1, h2, small = _styles(f)
    sectors = sorted({h.postcode.rsplit(" ", 1)[0] + " " + h.postcode.rsplit(" ", 1)[1][0] for h in homes},
                     key=lambda x: (int(x.split()[0][2:]), x))
    s = [_p("<font size=9 color='#006b6b'><b>PENNIMOUTH WATER LIMITED</b></font>", body),
         _p("Data sharing agreement PW-DSA-2026-014", h1),
         _p("Between Pennimouth Water Limited (the Company) and the National Homes Agency (the Agency). "
            "Agreement version 1.0, 1 September 2026.", small),
         Spacer(1, 3 * mm),
         _p("1. Purpose", h2),
         _p("The Company will share data with the Agency so that the Agency can choose the community area for its "
            "Homes in Use pilot in 2027 and evaluate the pilot. The Agency will not use the data for any other "
            "purpose, will not use it to make decisions about individual customers' water bills and will not pass "
            "it to any other body.", body),
         _p("2. Legal basis", h2),
         _p("The Agency processes the data under its public task. The Company shares it in its legitimate interest "
            "in supporting the reuse of empty homes in its supply area and has recorded its assessment of that "
            "interest. Each party is a controller of the data it holds.", body),
         _p("3. Data to be shared", h2),
         _p("3.1 For every household property the Company supplies in the postcode sectors in Annex A: the "
            "consumption the property's smart meter registered on each meter day from 1 September 2025 to 4 October "
            "2026, with the meter's serial number and whether the head end received that day's read; and the "
            "Company's match of the property to the county address gazetteer, with the billing address and postcode "
            "it holds.", body),
         _p("3.2 No customer name, account number, payment or contact detail will be shared.", body),
         _p("4. Transfer", h2),
         _p("The Company will place the data on the Agency's secure file transfer service by 16 October 2026 and "
            "confirm the transfer by email. The Agency will confirm receipt and the row counts within five working "
            "days.", body),
         _p("5. Security", h2),
         _p("The Agency will hold the data on its secure analysis platform, restrict access to named analysts in "
            "its Housing Evidence team, keep an access log and report any loss or unauthorised access to the "
            "Company's Data Protection Officer within 24 hours.", body),
         _p("6. Retention and deletion", h2),
         _p("The Agency will delete the data, with any copies, by 31 March 2028, unless the parties agree in "
            "writing that it may keep it to 30 September 2028 for the pilot's evaluation, and will confirm "
            "deletion in writing.", body),
         _p("7. Publication", h2),
         _p("The Agency may publish counts of homes by community area. It will not publish or disclose any figure "
            "that relates to fewer than ten properties or that could identify a property.", body),
         _p("8. Review and termination", h2),
         _p("Either party may end this agreement on 30 days' notice. The parties will review it if the pilot's "
            "scope changes.", body),
         _p("Annex A: postcode sectors", h2),
         _p(", ".join(sectors), body),
         Spacer(1, 8 * mm),
         _table([["For Pennimouth Water Limited", "For the National Homes Agency"],
                 ["Tracy Hawkins, Data Sharing Officer", "Toby Hunt, Housing Evidence Lead"],
                 ["Signed: ____________________", "Signed: ____________________"],
                 ["Date: 1 September 2026", "Date: 1 September 2026"]], [85 * mm, 85 * mm], f, head=False)]
    _pdf(path, "PW-DSA-2026-014 data sharing agreement", "Tracy Hawkins", s,
         _stamp(date(2026, 9, 1), 11, 6, 53), "Pennimouth Water | PW-DSA-2026-014 | Commercial in confidence",
         "PW-DSA-2026-014 v1.0", f)


# --------------------------------------------------------------------------------- Council Taxbase returns
REST = {"Teversby": {"dwellings": 21486, "exempt": 498, "lte": 219, "second": 302},
        "Swanholt": {"dwellings": 26215, "exempt": 611, "lte": 344, "second": 871}}
REST_BANDS = {"Teversby": [5113, 6942, 4630, 2751, 1310, 512, 211, 17],
              "Swanholt": [7266, 7790, 5428, 3105, 1667, 680, 259, 20]}


def ctb_counts(homes, d):
    """what each council's return counted on the day for its whole district: the shortlisted areas from the
    records, the rest of the district (outside the pack) fixed."""
    cut = date(d.year - (1 if d.month <= 6 else 0), (d.month + 6 - 1) % 12 + 1, d.day)
    out = {}
    for dist in ("Teversby", "Swanholt"):
        hs = [h for h in homes if W.AREA_DISTRICT[h.area] == dist]
        on_list = [h for h in hs if R.state_on(h, d)[0] != W.NDR and h.built <= d]
        bands = [sum(1 for h in on_list if h.band == b) + REST_BANDS[dist][i] for i, b in enumerate("ABCDEFGH")]
        ex = sum(1 for h in on_list if R.state_on(h, d)[0] == W.EXEMPT)
        lte = sum(1 for h in on_list if R.lte_on(h, d, cut=cut))
        sec = sum(1 for h in on_list if R.second_on(h, d))
        r = REST[dist]
        out[dist] = {"dwellings": len(on_list) + r["dwellings"], "exempt": ex + r["exempt"], "lte": lte + r["lte"],
                     "second": sec + r["second"], "bands": bands}
        assert sum(bands) == out[dist]["dwellings"]
    return out


def write_ctb(path, homes):
    from reportlab.platypus import Spacer
    from reportlab.lib.units import mm
    f = _font("county")
    body, h1, h2, small = _styles(f)
    d = date(2025, 10, 6)
    c = ctb_counts(homes, d)
    n = lambda x: "{:,}".format(x)
    band_rows = [["Band"] + list("ABCDEFGH") + ["Total"]]
    for dist in ("Teversby", "Swanholt"):
        band_rows.append([dist] + [n(x) for x in c[dist]["bands"]] + [n(c[dist]["dwellings"])])
    s = [_p("<font size=9 color='#5a2d82'><b>COUNTY RESEARCH AND INTELLIGENCE</b></font>", body),
         _p("Council Taxbase returns, October 2025<br/>Teversby District Council and Swanholt Borough Council", h1),
         _p("Compiled from the returns each council published in October 2025. Count date: Monday 6 October 2025.",
            small),
         Spacer(1, 3 * mm),
         _p("1. Summary", h2),
         _table([["Line", "Teversby District", "Swanholt Borough"],
                 ["Dwellings on the valuation list", n(c["Teversby"]["dwellings"]), n(c["Swanholt"]["dwellings"])],
                 ["Exempt dwellings", n(c["Teversby"]["exempt"]), n(c["Swanholt"]["exempt"])],
                 ["Long-term empty homes", n(c["Teversby"]["lte"]), n(c["Swanholt"]["lte"])],
                 ["Second homes", n(c["Teversby"]["second"]), n(c["Swanholt"]["second"])]],
                [82 * mm, 44 * mm, 44 * mm], f),
         Spacer(1, 3 * mm),
         _p("The counts are for each district as a whole on the count date.", body),
         _p("2. Dwellings on the valuation list by band", h2),
         _table(band_rows, [24 * mm] + [15 * mm] * 8 + [26 * mm], f, size=8),
         _p("3. Definitions used in the returns", h2),
         _p("<b>Dwellings on the valuation list</b>: dwellings shown on the council tax valuation list on the count "
            "date.", body),
         _p("<b>Exempt dwellings</b>: dwellings in one of the classes of the Council Tax (Exempt Dwellings) Order "
            "1992 on the count date.", body),
         _p("<b>Long-term empty homes</b>: dwellings which on the count date have been unoccupied and substantially "
            "unfurnished for more than six months. Exempt dwellings are not included.", body),
         _p("<b>Second homes</b>: dwellings which on the count date are no one's sole or main residence and are "
            "substantially furnished. Exempt dwellings are not included.", body),
         _p("4. Premiums in force", h2),
         _table([["", "Teversby District", "Swanholt Borough"],
                 ["Long-term empty premium (empty one year or more)", "100 per cent", "100 per cent"],
                 ["Long-term empty premium (empty five years or more)", "200 per cent", "200 per cent"],
                 ["Second homes premium (from 1 April 2025)", "not adopted", "100 per cent"]],
                [92 * mm, 39 * mm, 39 * mm], f),
         Spacer(1, 3 * mm),
         _p("Premiums do not change how a dwelling is counted in the return.", body),
         _p("5. Sources", h2),
         _p("Teversby District Council, Council Taxbase return CTB(October 2025), published 17 October 2025. "
            "Swanholt Borough Council, Council Taxbase return CTB(October 2025), published 14 October 2025. "
            "Compiled by County Research and Intelligence for the Teversby and Swanholt housing evidence base, "
            "20 October 2025.", body)]
    _pdf(path, "Council Taxbase returns October 2025", "County Research and Intelligence", s,
         _stamp(date(2025, 10, 20), 10, 17, 32), "County Research and Intelligence | Council Taxbase returns, "
         "October 2025", "CRI/HEB/2025/31", f)
    return c


# -------------------------------------------------------------------------------- housing needs assessment
def hna_rows(oas):
    by = {a: [0, 0] for a in W.AREA_CODES}
    for o in oas:
        by[o["bestfit"]][0] += o["spaces"]
        by[o["bestfit"]][1] += o["nur"]
    return by


def write_hna(path, oas):
    from reportlab.platypus import Spacer
    from reportlab.lib.units import mm
    f = _font("consult")
    body, h1, h2, small = _styles(f)
    by = hna_rows(oas)
    rows = [["Community area", "District", "Household spaces", "No usual residents", "Share"]]
    order = sorted(W.AREA_CODES, key=lambda a: -by[a][1] / by[a][0])
    for a in order:
        rows.append([W.AREA_NAME[a], W.AREA_DISTRICT[a], "{:,}".format(by[a][0]), "{:,}".format(by[a][1]),
                     "%.1f%%" % (100.0 * by[a][1] / by[a][0])])
    T = lambda d, w: _table(d, w, f)
    s = [_p("<font size=9 color='#7a4b00'><b>TIDEMARK PLANNING</b></font>", body),
         _p("Teversby and Swanholt Housing Needs Assessment 2024<br/>Summary report", h1),
         _p("Prepared for Teversby District Council and Swanholt Borough Council. Final, November 2024.", small),
         Spacer(1, 3 * mm),
         _p("1. Introduction", h2),
         _p("This summary sets out the main findings of the 2024 Housing Needs Assessment for the two districts. "
            "The full report, with its technical appendices, is published on both councils' websites. The "
            "assessment informs the councils' local plan reviews, their housing strategies and the use of "
            "affordable housing contributions. It follows the national planning practice guidance on housing needs "
            "assessment and uses the standard method for the overall housing requirement.", body),
         _p("2. Population and households", h2),
         _p("The two districts had 106,400 residents at the 2021 census, 47,100 households and an average household "
            "size of 2.21. The population aged 65 and over grew by 19 per cent between 2011 and 2021, against 6 per "
            "cent for the population as a whole, and is projected to grow by a further 23 per cent by 2041. "
            "One-person households make up 34 per cent of the total, and two-thirds of them are aged 60 or over.",
            body),
         T([["", "Teversby", "Swanholt"],
            ["Residents, 2021", "47,900", "58,500"],
            ["Households, 2021", "21,300", "25,800"],
            ["Projected households, 2041", "23,100", "27,900"],
            ["Standard method requirement, homes a year", "312", "389"]], [86 * mm, 40 * mm, 40 * mm]),
         _p("3. Affordability", h2),
         _p("The ratio of median house price to median workplace earnings was 9.8 in Teversby and 10.6 in Swanholt "
            "in 2023, against 8.3 for England. Private rents rose 14 per cent between 2021 and 2023, and the lower "
            "quartile private rent for a two-bedroom home takes 41 per cent of lower quartile earnings in Swanholt. "
            "The assessment identifies a need for 412 affordable homes a year across the two districts, of which "
            "about 60 per cent should be for social rent.", body),
         _p("4. Homes with no usual residents", h2),
         _p("The coastal community areas carry a large stock of household spaces with no usual residents: second "
            "homes, holiday lets and homes between occupiers. Table 4.1 shows the 2021 census figures for the "
            "community areas with the most household spaces with no usual residents, built from output areas by the "
            "county's best-fit lookup of output areas to community areas.", body),
         _p("Table 4.1: Household spaces with no usual residents, census day 21 March 2021", small),
         T(rows, [40 * mm, 30 * mm, 34 * mm, 36 * mm, 26 * mm]),
         Spacer(1, 3 * mm),
         _p("%s and %s stand out, reflecting their holiday lets and second homes. The census was taken during the "
            "spring 2021 lockdown, when some owners were living in their second homes and few lets were "
            "occupied." % (W.AREA_NAME[order[0]], W.AREA_NAME[order[1]]), body),
         _p("5. Specialist housing", h2),
         _p("The assessment identifies a need for 1,140 additional units of housing with care for older people by "
            "2041 and for 85 further wheelchair-accessible homes a year. The councils should seek a mix of "
            "bungalows and level-access flats on larger sites, and should plan for extra care schemes in "
            "Brackwater and Ellingsea, where the older population is growing fastest.", body),
         _p("6. Recommendations", h2),
         _p("The councils should: keep the affordable housing requirement at 30 per cent on sites of ten homes or "
            "more; consider a principal residence policy for new homes in the coastal areas; review their use of "
            "the second homes and long-term empty premiums; and monitor homes with no usual residents through the "
            "census, council tax and, where available, other administrative sources.", body),
         Spacer(1, 6 * mm),
         _p("Tidemark Planning, 28 November 2024. Project 2391. Report checked by the project director.", small)]
    _pdf(path, "Teversby and Swanholt Housing Needs Assessment 2024 summary", "Tidemark Planning", s,
         _stamp(date(2024, 11, 28), 16, 52, 8), "Tidemark Planning | Teversby and Swanholt HNA 2024 | Summary "
         "report", "TP-2391-HNA-SUM-F", f)


def write_all(target, homes, oas, f_tor, f_dsa, f_ctb, f_hna):
    write_tor(os.path.join(target, f_tor))
    write_dsa(os.path.join(target, f_dsa), homes)
    write_ctb(os.path.join(target, f_ctb), homes)
    write_hna(os.path.join(target, f_hna), oas)
