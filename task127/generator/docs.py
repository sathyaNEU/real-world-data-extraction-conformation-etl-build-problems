"""task127 generator: the documents in the slot-split folder.

Each load-bearing rule is stated once, in the document that owns it: eligibility, the meter-set trigger,
the 31 December lapse, the windows, the allocation rule and the state's licensed basis in the programme
rules; the 5 kW connection standard, the field-order sharing, the two-leg assigned rebate and the pilot
rebate schedule in the participation terms; the invoice of record, the Central-time clearing date and the
returned-payment rule in the finance procedures; the multi-zone system as one install in the price guide.
No document describes the meter crews' workload, and the trustees' paper quotes no figure.
"""
from datetime import datetime

from reportlab import rl_config

rl_config.invariant = 1   # fixed document id and dates, so two builds are byte-identical

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_LEFT  # noqa: E402
from reportlab.lib.pagesizes import LETTER  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A  # noqa: E402
import params as P  # noqa: E402

F = P.F
NAME = P.COOP_NAME
BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=14, alignment=TA_LEFT, spaceAfter=6)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=3)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=6,
                    spaceAfter=2)
SMALL = ParagraphStyle("s", parent=BODY, fontName="Helvetica", fontSize=8, leading=10,
                       textColor=colors.HexColor("#444444"))


def _pdf(path, title, author, story, footer):
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.8 * inch, 0.5 * inch, footer)
        canvas.drawRightString(7.7 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(str(path), pagesize=LETTER, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch, title=title, author=author,
                            subject="", creator=author, invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


def _table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.6),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEEEEE")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def p(text, st=BODY):
    return Paragraph(text, st)


# ------------------------------------------------------------------ programme rules (PDF)

def rules(path):
    pilot = ", ".join(f"{P.PILOT_NBHD[c]} ({NAME[c]})" for c in P.COOPS)
    s = [p("Heat-Pump Rebate Programme: Programme Year 2 (2027)", H1),
         p("Programme rules. Adopted by the trustees of the Minnesota Clean Heat Fund on 27 October 2026. "
           "Owner: Stephanie O'Connor, programme director.", SMALL), Spacer(1, 8),
         p("1. What the programme pays for", H2),
         p("The fund pays a rebate toward an air-source heat pump installed in a member's home, in the service "
           "territory of one of the six participating co-operatives: North Shore, Valley, Lakes, Uplands, Riverbend "
           "and Pinewood. Programme year 2 runs from 1 January to 31 December 2027."),
         p("2. Who is eligible", H2),
         p("A household is eligible where the home is owner-occupied and a single-family detached house; the home "
           "is heated mainly by a propane furnace, a propane boiler or electric resistance heat; and household "
           "income in the past 12 months was from $35,000 to $149,999. Homes in the six 2026 pilot neighbourhoods "
           f"({pilot}) are not in programme year 2; members there were offered the pilot rebate in 2026."),
         p("3. Application windows", H2),
         p("Members apply through a participating installer in one of two windows, the same windows the pilot used: "
           "1 March to 30 April 2027 and 1 September to 15 October 2027."),
         p("4. When a rebate is earned", H2),
         p("A rebate is earned when the member's co-operative sets the heat-pump rate meter at the premises. A slot "
           "is spent only on an earned rebate. Slots not spent by 31 December 2027 lapse; they do not carry into "
           "2028."),
         p("5. Allocation of slots", H2),
         p("The fund has 1,800 rebate slots for 2027. Each participating co-operative receives the slots equal to the "
           "rebated installs expected in its territory in the programme year, to the nearest ten. Where those "
           "together exceed 1,800, the 1,800 are shared in proportion to them, in tens, by largest remainder. Slots "
           "not allocated are held by the fund and are not released to a co-operative during the year."),
         p("6. Rebate amounts", H2),
         p("Programme year 2 rebate amounts are those in Schedule B of the participation terms, carried forward from "
           "the pilot without change."),
         p("7. The state match", H2),
         p("The state energy office matches the fund's 2027 rebates. It apportions its match across the six "
           "co-operatives on the propane- and electricity-heated household counts in Table H1 of the Heat Survey "
           "2025, and its deputy director will present that apportionment to the trustees on 17 December. A "
           "co-operative with more propane- and electricity-heated homes is a larger programme on that read; the "
           "office treats the Table H1 counts as its planning facts and that is the read the room will have in "
           "front of it."),
         p("8. Records", H2),
         p("Each co-operative's hosting capacity filings and meter-shop field orders reach the fund under the "
           "participation terms. Installer invoices and rebate payments are handled under the fund's finance "
           "procedures.")]
    _pdf(path, "Heat-Pump Rebate Programme, Programme Year 2 (2027): Programme rules", P.PEOPLE["director"], s,
         "Minnesota Clean Heat Fund  |  Programme rules, programme year 2 (2027)  |  Adopted 27 October 2026")


# ------------------------------------------------------------------ participation terms (PDF)

def terms(path):
    sched = [["Heating system replaced", "Rebate", "Income $35,000 to $74,999"],
             ["Propane furnace (ducted)", "$3,600", "plus $1,000"],
             ["Electric resistance", "$4,200", "plus $1,000"],
             ["Propane boiler (hydronic)", "$5,400", "plus $1,000"]]
    s = [p("Participation terms between the Minnesota Clean Heat Fund and the participating co-operatives", H1),
         p("Signed 21 January 2026 by the fund and by North Shore, Valley, Lakes, Uplands, Riverbend and Pinewood "
           "electric co-operatives. These terms apply to the 2026 pilot and to each later programme year until "
           "replaced.", SMALL), Spacer(1, 8),
         p("1. Parties and purpose", H2),
         p("The fund pays heat-pump rebates to members of the co-operatives. Each co-operative serves its members, "
           "connects heat pumps to its distribution system and meters them."),
         p("2. Hosting capacity", H2),
         p("Each co-operative files with the fund, by the fifth working day of each month, the remaining hosting "
           "capacity for new electrification load on each of its distribution feeders, in kW, as at the end of the "
           "previous month."),
         p("3. Connection standard", H2),
         p("Each heat pump installed under the programme is assessed at 5 kW against the hosting capacity filed for "
           "the feeder serving the premises. An install proceeds only where the feeder has that capacity remaining."),
         p("4. Heat-pump rate meter", H2),
         p("Each rebated heat pump is separately metered on the co-operative's heat-pump rate. The installer reports "
           "the install complete to the co-operative, and the co-operative raises a field order to set the "
           "heat-pump rate meter."),
         p("5. Field orders", H2),
         p("Each co-operative shares its meter shop's field orders with the fund monthly, so that the fund can "
           "verify each rebated meter set before it pays."),
         p("6. Payment of rebates", H2),
         p("The fund pays a rebate after it has verified the meter set. A member may assign the rebate to the "
           "installer. An assigned rebate is paid in two legs, one to the installer and one to the member, in the "
           "amounts the assignment states."),
         p("Schedule B. Rebate amounts", H2),
         _table(sched, [2.4 * inch, 1.2 * inch, 2.2 * inch]), Spacer(1, 6),
         p("The income addition applies where the household's income in the past 12 months, as declared on the "
           "application, was from $35,000 to $74,999.")]
    _pdf(path, "Participation terms", P.PEOPLE["director"], s,
         "Minnesota Clean Heat Fund  |  Participation terms with the participating co-operatives  |  January 2026")


# ------------------------------------------------------------------ finance procedures (PDF)

def finance(path):
    s = [p("Finance procedures: rebate programme", H1),
         p(f"Version 3, February 2026. Owner: {P.PEOPLE['finance']}, finance director.", SMALL), Spacer(1, 8),
         p("1. Scope", H2),
         p("These procedures cover installer invoices for rebated jobs and the payment of rebates."),
         p("2. Installer invoices", H2),
         p("Installers upload invoices for each rebated job to the fund's portal, or send an export from their own "
           "accounting system. An installer may send more than one version of an invoice for a job. The invoice of "
           "record is the latest version the fund has accepted; a version the fund did not accept is not an invoice "
           "of record."),
         p("3. Payment runs", H2),
         p("Rebate payments are released in runs on Monday and Thursday evenings, by ACH transfer or, where the "
           "member has no account on file, by cheque."),
         p("4. When a payment counts", H2),
         p("A payment counts as paid on the date it clears at the bank, read in Central time. A payment the bank "
           "returns is not a payment. Where the fund reissues a returned payment, the reissue is a new payment "
           "under its own payment id."),
         p("5. Month end", H2),
         p("The books close at each month end. Papers to the trustees report rebates paid through the last closed "
           "month end."),
         p("6. Records", H2),
         p("The payment ledger is kept by the fund. Clearing times are loaded from the bank's settlement file. "
           "Returned-payment notices are received from the bank and kept as the bank sends them.")]
    _pdf(path, "Finance procedures: rebate programme", P.PEOPLE["finance"], s,
         "Minnesota Clean Heat Fund  |  Finance procedures, rebate programme  |  Version 3")


# ------------------------------------------------------------------ price guide (PDF)

def prices(path):
    rows = [["System", "Typical installed price"],
            ["Ducted heat pump, replacing a propane furnace", "$13,000 to $20,000"],
            ["Ductless single-zone (one indoor head)", "$8,000 to $11,000"],
            ["Ductless multi-zone (two to four indoor heads)", "$11,000 to $18,000"]]
    s = [p("Participating Installers' Group: 2026 Price Guide", H1),
         p(f"Issued 30 January 2026 for member firms. Chair: {P.PEOPLE['installers']}.", SMALL), Spacer(1, 8),
         p("Prices below are typical installed prices for rebated jobs, including electrical work, the heat-pump rate "
           "meter base, line sets, removal of the old equipment and the permit."),
         _table(rows, [3.6 * inch, 2.2 * inch]), Spacer(1, 8),
         p("A multi-zone ductless system, one outdoor unit serving two or more indoor heads, is one install. It is "
           "priced as one system, at the system price, and rebated as one install; the indoor heads are listed on "
           "the system line."),
         p("Where a home needs a second 240 V circuit, it is a second electrical line on the invoice."),
         p("Change orders: work added after the first invoice is invoiced as a change order and needs the "
           "member's signature."),
         p("Member firms invoice the fund through its portal or by export from their accounting system, as agreed "
           "with the fund.")]
    _pdf(path, "Participating Installers' Group: 2026 Price Guide", P.PEOPLE["installers"], s,
         "Participating Installers' Group  |  2026 Price Guide  |  For member firms")


# ------------------------------------------------------------------ feeder upgrades (PDF, unused)

def upgrades(path):
    rows = [["Co-operative", "Feeder", "Work", "Added hosting capacity", "Planned in service"],
            ["North Shore", "NS-411", "Reconductor and line regulator", "1,200 kW", "Q3 2028"],
            ["Valley", "VA-205", "New tie to Mill Creek substation", "900 kW", "Q2 2028"],
            ["Uplands", "UP-101", "Substation transformer replacement", "700 kW", "Q4 2028"],
            ["Pinewood", "PW-601", "Three-phase extension", "600 kW", "Q2 2028"]]
    s = [p("Distribution reinforcement schedule, 2027 to 2028", H1),
         p("Feeder work planned by the participating co-operatives, as reported to the fund's grid liaison on "
           "14 September 2026.", SMALL), Spacer(1, 8),
         _table(rows, [1.0 * inch, 0.7 * inch, 2.3 * inch, 1.3 * inch, 1.1 * inch]), Spacer(1, 8),
         p("Planned in-service dates are the co-operatives' current plans. Hosting capacity is refiled for a "
           "feeder when the work is energised."),
         p("Each project is funded through the co-operative's construction work plan; none is funded by the "
           "Minnesota Clean Heat Fund.")]
    _pdf(path, "Distribution reinforcement schedule, 2027 to 2028", P.PEOPLE["grid"], s,
         "Minnesota Clean Heat Fund  |  Grid liaison  |  Reinforcement schedule as reported September 2026")


# ------------------------------------------------------------------ trustees' paper (DOCX)

def paper(path):
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    doc.add_heading("Minnesota Clean Heat Fund: Board of Trustees", level=1)
    doc.add_paragraph("Meeting of Thursday 17 December 2026, 2:00 pm, fund office and by video. "
                      f"Chair: {P.PEOPLE['chair']}.")
    doc.add_heading("Agenda", level=2)
    for item in ["1. Minutes of 27 October 2026",
                 "2. Finance report to 30 November 2026",
                 "3. State energy office: the 2027 state match (deputy director, state energy office)",
                 "4. Programme year 2: split of the 2027 rebate slots across the six co-operatives (for decision)",
                 "5. Weatherization grants: 2027 round",
                 "6. Any other business"]:
        doc.add_paragraph(item)
    doc.add_heading("Item 4. Programme year 2: the 2027 slot split", level=2)
    doc.add_paragraph(
        f"Paper from {P.PEOPLE['director']}, programme director. The trustees are asked to adopt the split of the "
        "fund's 1,800 rebate slots for 2027 across North Shore, Valley, Lakes, Uplands, Riverbend and Pinewood, "
        "under section 5 of the programme rules, before programme year 2 opens on 1 January 2027. The split itself "
        "will be tabled at the meeting.")
    doc.add_paragraph(
        "The pilot closed its second window on 15 October 2026 and its last rebated install was set in early "
        "December. Each co-operative has filed its hosting capacity as at 30 November and shared its field orders "
        "to the pull of 11 December.")
    doc.add_heading("Comments received on item 4", level=3)
    doc.add_paragraph(
        f"{P.PEOPLE['outreach']}, outreach director: \"Uplands has more qualifying homes than any other co-op we "
        "work with. That is where I would expect the demand to be in 2027, and it is where we have the most "
        "outreach booked for the spring.\"")
    doc.add_paragraph(
        f"{P.PEOPLE['installers']}, chair of the participating installers' group: \"Our member firms can install "
        "every rebate the fund pays for in 2027. Two firms have taken on extra installers since the pilot.\"")
    doc.add_paragraph(
        f"{P.PEOPLE['lakes_ops']}, field operations superintendent, Lakes: \"Our members asked about the heat-pump "
        "rate more than about any other service this year.\"")
    doc.add_heading("Covering note on the hosting filings", level=3)
    doc.add_paragraph(
        f"From {P.PEOPLE['grid']}, grid liaison: \"Every co-operative's hosting capacity filing is current to 30 "
        "November 2026. North Shore and Pinewood refiled two feeders each in November after load studies; the "
        "others are unchanged from October.\"")
    doc.add_paragraph("Papers for item 3 will be circulated by the state energy office.")
    doc.add_paragraph("Internal: trustees and staff only. Please do not forward.")
    cp = doc.core_properties
    cp.author = P.PEOPLE["director"]
    cp.last_modified_by = P.PEOPLE["director"]
    cp.title = "Board of Trustees, 17 December 2026: papers"
    cp.created = datetime(2026, 12, 7, 9, 14)
    cp.modified = datetime(2026, 12, 10, 17, 52)
    cp.revision = 6
    cp.comments = ""
    cp.subject = ""
    cp.keywords = ""
    doc.save(str(path))


# ------------------------------------------------------------------ field definitions (TXT)

FIELDS = f"""FIELD DEFINITIONS
Minnesota Clean Heat Fund, programme team. Revised 10 December 2026.
Covers the extracts and registers in this folder. Dates are YYYY-MM-DD; times are Central unless a field says
otherwise.

{F['orders']}
  One row per field order worked by a participating co-operative's meter crew, as shared monthly under the
  participation terms. Orders completed from 1 January 2025 to the pull (10 December 2026), and orders open at
  the pull.
  order_id         co-operative's field order number
  coop             participating co-operative
  crew             meter crew code
  order_type       HPRM  set heat-pump rate meter
                   MXCH  meter exchange
                   NSVC  new service, meter set
                   MTST  meter test
                   DISC  disconnect
                   RCON  reconnect
                   RELO  meter relocation
  premises_id      co-operative's location number for the premises
  requested_date   date the order was raised
  completed_date   date the crew completed the order; blank where the order was open at the pull

{F['survey']}
  One row per sample household, Heat Survey 2025. Weighted counts are the sum of weight.
  case_id          survey case number
  coop             co-operative whose service territory the home is in
  neighbourhood    neighbourhood of the home
  heating_system   PF propane furnace (ducted); PB propane boiler (hydronic); ER electric resistance
                   (baseboard, wall or cable); HP electric heat pump; NG natural gas furnace or boiler;
                   FO fuel oil furnace or boiler; WD wood or pellet stove; OT other or none
  tenure           owner or renter
  structure        single-family detached; mobile home; attached or multi-unit
  income_band      household income in the past 12 months, dollars
  year_built       year the structure was built, band
  bedrooms         number of bedrooms
  weight           survey weight, households

{F['tables']}
  The survey office's published Tables H1 to H4, release 1. Weighted counts of households by co-operative.

{F['pilot']}
  Sheet rebates: one row per rebated install in the 2026 pilot.
  rebate_id, premises_id, coop, neighbourhood
  heating_system_replaced   the home's main heating system before the heat pump
  income_band               household income declared on the application
  system_type               ducted; ductless single-zone; ductless multi-zone
  indoor_heads              number of indoor heads served by the outdoor unit
  installer_id              participating installer
  purchase_date             date the member signed with the installer
  install_date              date the installer reported the install complete
  meter_set_date            date the co-operative set the heat-pump rate meter

{F['hosting']}
  Sheet feeders: one row per distribution feeder. hosting_capacity_remaining_kw is the remaining hosting
  capacity for new electrification load filed by the co-operative, kW; study_date is the date of the load
  study behind the filing.

{F['fmap']}
  The feeder serving each neighbourhood.

{F['invoices']}
  One row per invoice line, for every version of every invoice installers delivered for pilot jobs.
  invoice_no       installer's invoice number for the job
  version          version of the invoice, 1 for the first
  installer_id     participating installer
  premises_id      premises of the job
  delivered_at     when this version reached the fund
  accepted_at      when the fund accepted this version; blank where it was not accepted
  line_no, description
  unit_serial      serial number of the indoor unit or units on the line, separated by ';'
  amount_usd       line amount, dollars

{F['ledger']}
  The fund's rebate payment ledger, payments released to the pull.
  payment_id, rebate_id
  payee_type       member or installer
  method           ACH or cheque
  amount_usd       dollars
  released_on      date of the payment run
  cleared_at       when the payment cleared, as the bank's settlement file reports it (UTC, ISO 8601);
                   blank where not cleared at the pull
  memo             free text

{F['returns']}
  The bank's returned-payment notices for the fund's ACH payments, as delivered by the bank. Times are UTC.

{F['dims']}
  Sheet cooperatives: the participating co-operatives. Sheet installers: the participating installers.

{F['wx']}
  The fund's 2026 weatherization grants: one row per completed grant.
  grant_id, coop, neighbourhood, premises_id, measure, grant_usd, completed_on
"""


def fields(path):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(FIELDS)


def about(path):
    lines = ["ABOUT THESE FILES", "Folder prepared for the trustees' meeting of 17 December 2026.",
             "Pulled 11 December 2026 by the programme team.", "",
             "file | what it is | source | date | licence"]
    src = {
        "orders": ("field orders shared by the six co-operatives' meter shops", "co-operatives, monthly sharing",
                   "pulled 2026-12-11"),
        "survey": ("Heat Survey 2025 sample records", "survey office", "release 1, 2026-03-09"),
        "tables": ("Heat Survey 2025 published tables H1 to H4", "survey office", "release 1, 2026-03-09"),
        "pilot": ("2026 pilot rebate log", "fund programme team", "2026-12-09"),
        "hosting": ("hosting capacity filings at 30 November 2026", "co-operatives, compiled by the grid liaison",
                    "2026-12-03"),
        "fmap": ("neighbourhood to feeder map", "co-operatives' engineering", "2026-11-20"),
        "rules": ("programme rules, programme year 2", "fund", "adopted 2026-10-27"),
        "terms": ("participation terms with the co-operatives", "fund and co-operatives", "signed 2026-01-21"),
        "invoices": ("installer invoices for pilot jobs, all versions", "fund invoice portal", "pulled 2026-12-11"),
        "ledger": ("rebate payment ledger", "fund finance", "pulled 2026-12-11"),
        "returns": ("returned-payment notices", "fund's bank", "received to 2026-12-11"),
        "finance": ("finance procedures, rebate programme", "fund finance", "version 3, 2026-02"),
        "prices": ("installers' group 2026 price guide", "participating installers' group", "2026-01-30"),
        "paper": ("papers for the trustees' meeting of 17 December 2026", "fund", "2026-12-10"),
        "dims": ("co-operatives and installers", "fund programme team", "2026-02-16"),
        "fields": ("field definitions", "fund programme team", "2026-12-10"),
        "wx": ("2026 weatherization grants", "fund grants team", "2026-12-08"),
        "upgrades": ("distribution reinforcement schedule 2027 to 2028", "co-operatives, via the grid liaison",
                     "2026-09-14"),
    }
    for k, (what, who, when) in src.items():
        lines.append(f"{F[k]} | {what} | {who} | {when} | CC0-1.0")
    lines += ["", "All organisations, people, places and records in this folder are fictional and were constructed "
              "for this exercise; no third-party data is included."]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def write_docs(W, tgt):
    rules(tgt / F["rules"])
    terms(tgt / F["terms"])
    finance(tgt / F["finance"])
    prices(tgt / F["prices"])
    upgrades(tgt / F["upgrades"])
    paper(tgt / F["paper"])
    fields(tgt / F["fields"])
    about(tgt / F["about"])
