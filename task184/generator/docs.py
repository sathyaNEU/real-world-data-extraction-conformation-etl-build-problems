"""The pack's documents: the monitoring ruleset, the platform's operating guide, the ledger data dictionary
and the EPOS interface notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A       # noqa: E402
import ledger as L     # noqa: E402
import world as W      # noqa: E402

CATALOGUE = "continuous_monitoring_rule_catalogue.pdf"
PLATFORM = "monitoring_platform_operating_guide.pdf"
DICTIONARY = "general_ledger_data_dictionary.pdf"
EPOS_NOTES = "epos_interface_change_note.pdf"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY = colors.HexColor("#17212b"), colors.HexColor("#5b6671")
RULE = colors.HexColor("#c3cbd3")

BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.5, leading=13.2, textColor=INK, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=13.6, leading=17.4, textColor=INK, spaceAfter=2)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.1, leading=13.4, textColor=INK,
                    spaceBefore=9, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.1, leading=10.4, textColor=GREY, spaceAfter=9)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.2, leading=10.0, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=21 * mm, rightMargin=21 * mm,
                             topMargin=19 * mm, bottomMargin=18 * mm, title=title, author=author,
                             subject="", creator="", producer="")


def _table(rows, widths, align_right=()):
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    st = [("GRID", (0, 0), (-1, -1), 0.4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef1f4")),
          ("LEFTPADDING", (0, 0), (-1, -1), 3.4), ("RIGHTPADDING", (0, 0), (-1, -1), 3.4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    for c in align_right:
        st.append(("ALIGN", (c, 1), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def write_catalogue(path):
    d = _doc(path, "Continuous monitoring rule catalogue", "Group Internal Audit")
    s = [Paragraph("Continuous monitoring rule catalogue", H1),
         Paragraph("%s, Group Internal Audit. Catalogue version 7.2, in force from FY26 P1."
                   % W.GROUP, META),
         Paragraph("Scope", H2),
         Paragraph("The ruleset is applied to postings reaching the general ledger through the posting "
                   "streams listed below. Each rule is evaluated against the individual posting.", BODY)]
    rows = [[Paragraph("Posting stream", CELLB), Paragraph("Covered", CELLB),
             Paragraph("Basis", CELLB)]]
    notes = {
        "EPOS": "Covered in full.",
        "ROUTE_DOCKET": "Covered in full.",
        "ROUTE_VAN": "Covered in full.",
        "AP_BATCH": "Covered in full.",
        "AP_INVOICE": "Single supplier invoices fall below the authorisation threshold the ruleset tests "
                      "and are reviewed under the purchase ledger's own controls.",
        "PAYROLL": "Payroll postings are covered by the separate payroll assurance programme.",
        "MANUAL": "Covered in full.",
    }
    for stream in ("EPOS", "ROUTE_DOCKET", "ROUTE_VAN", "AP_BATCH", "AP_INVOICE", "PAYROLL", "MANUAL"):
        rows.append([Paragraph(stream, CELL),
                     Paragraph("Yes" if stream in A.MONITORED else "No", CELL),
                     Paragraph(notes[stream], CELL)])
    s += [_table(rows, [30, 18, 118]), Spacer(1, 7),
          Paragraph("Rules", H2),
          Paragraph("A rule withdrawn in a financial year is not evaluated in that year or later.", BODY)]
    rr = [[Paragraph("Rule", CELLB), Paragraph("Title", CELLB), Paragraph("Evaluated against", CELLB),
           Paragraph("Live from", CELLB), Paragraph("Withdrawn", CELLB)]]
    for rid, title, live, gone, _share in L.RULES:
        rr.append([Paragraph(rid, CELL), Paragraph(title, CELL), Paragraph("the posting", CELL),
                   Paragraph(live, CELL), Paragraph(gone or "", CELL)])
    s += [_table(rr, [16, 76, 32, 20, 22]), Spacer(1, 7),
          Paragraph("Review", H2),
          Paragraph("Exceptions are raised to the trading unit's financial controller and to Group "
                    "Internal Audit. The catalogue is reviewed each year by the Head of Internal Audit "
                    "and the Group Financial Controller.", BODY)]
    d.build(s)
    return path


def write_platform(path, monthly):
    d = _doc(path, "Monitoring platform operating guide", "Group Finance Systems")
    s = [Paragraph("Continuous monitoring platform: operating guide", H1),
         Paragraph("%s, Group Finance Systems. Release 4.4." % W.GROUP, META),
         Paragraph("What the platform does", H2),
         Paragraph("The platform reads the general ledger each night and applies the rule catalogue to "
                   "the postings that reached the ledger that day. Every posting on a journal entry is "
                   "evaluated against every live rule. The platform then writes one verdict for the "
                   "journal entry: where one or more of the entry's postings has tripped one or more "
                   "rules, the entry is raised as an exception, and the rules that tripped are recorded "
                   "against it.", BODY),
         Paragraph("What the platform retains", H2),
         Paragraph("The exception register holds one row for each journal entry raised, with the rules "
                   "that tripped. Under the data retention standard the platform does not retain the "
                   "posting-level evaluation detail once the run has completed, so an exception row "
                   "cannot be traced back to the individual postings that tripped.", BODY),
         Paragraph("Runs and coverage", H2),
         Paragraph("Runs are nightly. A run that completes is logged as completed. Postings that reach "
                   "the ledger after the nightly cut-off are presented to the following run where they "
                   "remain within the evaluation window.", BODY),
         Paragraph("Exceptions raised, FY26 to date", H2),
         Paragraph("Entries raised as exceptions, by trading unit and fiscal period. This is the figure "
                   "the platform reports to the audit committee each period.", BODY)]
    hdr = [Paragraph("Unit", CELLB)] + [Paragraph("P%d" % p, CELLB)
                                        for p in range(1, W.GRADED_PERIODS + 1)] + \
          [Paragraph("Total", CELLB)]
    rows = [hdr]
    for code, _o, _n, _k, _c in W.UNITS:
        line = [Paragraph(code, CELL)]
        tot = 0
        for p in range(1, W.GRADED_PERIODS + 1):
            v = monthly.get((code, p), 0)
            tot += v
            line.append(Paragraph("{:,}".format(v), CELLR))
        line.append(Paragraph("{:,}".format(tot), CELLR))
        rows.append(line)
    tot_line = [Paragraph("Group", CELLB)]
    grand = 0
    for p in range(1, W.GRADED_PERIODS + 1):
        v = sum(monthly.get((c[0], p), 0) for c in W.UNITS)
        grand += v
        tot_line.append(Paragraph("{:,}".format(v), CELLR))
    tot_line.append(Paragraph("{:,}".format(grand), CELLR))
    rows.append(tot_line)
    s += [_table(rows, [22] + [13] * W.GRADED_PERIODS + [17], tuple(range(1, W.GRADED_PERIODS + 2)))]
    d.build(s)
    return path


def write_dictionary(path):
    d = _doc(path, "General ledger data dictionary", "Group Finance Systems")
    s = [Paragraph("General ledger extract: data dictionary", H1),
         Paragraph("%s, Group Finance Systems." % W.GROUP, META),
         Paragraph("Terms", H2),
         Paragraph("A <b>posting</b> is one source document's entry into the general ledger: one "
                   "delivery docket, one till transaction, one supplier invoice, one payroll item or one "
                   "manual journal. A <b>journal entry</b> is the voucher the ledger records postings "
                   "under. A <b>ledger line</b> is one debit or one credit within an entry; a posting "
                   "carries at least one debit and one credit and may carry more.", BODY),
         Paragraph("Table journal_entries", H2)]
    cols = [
        ("entry_no", "integer", "The entry's number in this extract."),
        ("voucher_ref", "text", "The voucher reference the posting interface assigned."),
        ("unit_code", "text", "The trading unit, as the code stood on the posting date. Codes were "
                              "renumbered with effect from %s; see trading_unit_register.csv."
         % W.RENUMBER_DATE.isoformat()),
        ("fiscal_year", "text", "FY26."),
        ("fiscal_period", "integer", "The 4-4-5 fiscal period; see period_calendar.csv."),
        ("posting_date", "date", "The date the entry was posted to the ledger."),
        ("source_interface", "text", "The interface that carried the postings."),
        ("item_count", "integer", "The number of postings, that is source documents, recorded under "
                                  "this entry."),
        ("line_count", "integer", "The number of ledger lines in this entry."),
        ("debit_total", "number", "Total debits, EUR."),
        ("credit_total", "number", "Total credits, EUR."),
        ("entered_by", "text", "The user identifier that entered the journal."),
        ("released_by", "text", "The user identifier that released it for posting."),
    ]
    rows = [[Paragraph("Column", CELLB), Paragraph("Type", CELLB), Paragraph("Meaning", CELLB)]]
    for c, t, m in cols:
        rows.append([Paragraph(c, CELL), Paragraph(t, CELL), Paragraph(m, CELL)])
    s += [_table(rows, [30, 16, 120]), Spacer(1, 7),
          Paragraph("Table journal_lines", H2),
          Paragraph("Line detail is extracted for a stratified sample of vouchers only; see "
                    "extract_manifest.txt.", BODY)]
    rows = [[Paragraph("Column", CELLB), Paragraph("Type", CELLB), Paragraph("Meaning", CELLB)]]
    for c, t, m in (("entry_no", "integer", "The journal entry."),
                    ("line_no", "integer", "The line's position in the entry."),
                    ("account_code", "text", "See chart_of_accounts.csv."),
                    ("source_doc_ref", "text", "The source document this line belongs to. Each posting "
                                               "writes its own balanced set of lines, so the distinct "
                                               "source document references on an entry number the same "
                                               "as its item_count."),
                    ("debit", "number", "EUR."), ("credit", "number", "EUR.")):
        rows.append([Paragraph(c, CELL), Paragraph(t, CELL), Paragraph(m, CELL)])
    s += [_table(rows, [30, 16, 120]), Spacer(1, 7), Paragraph("Posting interfaces", H2)]
    rows = [[Paragraph("Interface", CELLB), Paragraph("System", CELLB),
             Paragraph("How postings are grouped into entries", CELLB)]]
    for key, spec in W.INTERFACES.items():
        rows.append([Paragraph(spec["name"], CELL), Paragraph(spec["system"], CELL),
                     Paragraph(spec["voucher"], CELL)])
    s += [_table(rows, [34, 30, 102])]
    d.build(s)
    return path


def write_epos_notes(path):
    d = _doc(path, "EPOS interface change note", "Group Finance Systems")
    s = [Paragraph("EPOS interface: change note and posting behaviour", H1),
         Paragraph("%s, Group Finance Systems. Reference FS-CN-2026-11." % W.GROUP, META),
         Paragraph("Voucher grouping", H2),
         Paragraph("Until %s the EPOS interface posted each branch's trading day to the ledger as a "
                   "single voucher covering every till. From %s each till's trading day posts as its "
                   "own voucher. The change was made so that till-level differences could be "
                   "investigated without opening the branch's whole day."
                   % ((W.RENUMBER_DATE.toordinal() - 1 and
                       __import__("datetime").date.fromordinal(W.RENUMBER_DATE.toordinal() - 1)
                       ).isoformat(), W.RENUMBER_DATE.isoformat()), BODY),
         Paragraph("Upload timing", H2),
         Paragraph("The interface uploads a trading day to the ledger on the next working day, so the "
                   "ledger's posting date for a day's takings is later than the trading date. Where a "
                   "public holiday falls on or immediately after the trading day the upload runs a "
                   "further day later. Till records carry the trading date in the business_date column; "
                   "the ledger carries the date the voucher was posted.", BODY),
         Paragraph("FY25 records", H2),
         Paragraph("FY25 till records were re-extracted after the trading unit renumbering and carry the "
                   "unit codes in force before it. The FY25 sales control account is stated by the "
                   "fiscal period the voucher was posted in.", BODY)]
    d.build(s)
    return path
