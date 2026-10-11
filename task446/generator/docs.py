"""Documents and workbooks for the task446 pack."""
import datetime as dt
import io
import os
import zipfile

import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

import world
import truth
from world import QE

FIXED_ZIP_TIME = (2026, 10, 9, 18, 40, 0)
CREATED = dt.datetime(2026, 10, 9, 18, 40, 0)


def normalize_zip(path, modified=None):
    """Rewrite an OOXML zip with fixed member timestamps and order, so two builds are byte-identical."""
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    def _app(n, data):
        if n == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
            data = re.sub(rb"<AppVersion>3.1</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        return n, data
    items = [_app(n, d) for n, d in items]
    if modified is not None:
        created = (modified - dt.timedelta(days=3, hours=5)).strftime("%Y-%m-%dT%H:%M:%SZ").encode()
        items = [(n, re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + created + rb"\g<2>", data))
                 if n == "docProps/core.xml" else (n, data) for n, data in items]
        stamp = modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
        items = [(n, re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", data))
                 if n == "docProps/core.xml" else (n, data) for n, data in items]
    first = [x for x in items if x[0] == "[Content_Types].xml"]
    rest = sorted([x for x in items if x[0] != "[Content_Types].xml"])
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in first + rest:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def set_xlsx_props(wb, creator, modified=CREATED):
    p = wb.properties
    p.creator = creator
    p.lastModifiedBy = creator
    p.created = modified - dt.timedelta(days=3, hours=2)
    p.modified = modified
    p.title = None


def autosize(ws, widths):
    for i, wdt in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt


# ------------------------------------------------------------------ derivatives workbook
def derivatives_workbook(w, path):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    runs = [(t, d, False) for t, d in enumerate(QE)] + [(4, QE[4], True)]
    for t, d, rerun in runs:
        ws = wb.create_sheet(d.strftime("%d.%m.%Y") + (" R2" if rerun else ""))
        ws["A1"] = "Counterparty credit risk: netting set mark-to-market"
        ws["A1"].font = Font(bold=True)
        ws["A2"] = "Run CCR-NS-01 for close of business %s; produced %s" % (
            d.strftime("%d %b %Y"), (d + dt.timedelta(days=6 if rerun else 3)).strftime("%d %b %Y 06:15"))
        hdr = ["Netting set", "Counterparty LEI", "Counterparty", "Master agreement", "CSA reference",
               "Live trades", "Net MTM"]
        ws.append([])
        ws.append(hdr)
        for c in range(1, len(hdr) + 1):
            ws.cell(row=4, column=c).font = Font(bold=True)
        for n in sorted(w.drv, key=lambda x: x["ns"]):
            mtm = n["mtm_k"][t] if (t < 4 or rerun) else n["mtm_run1"]
            ws.append([n["ns"], n["lei"], w.ent[n["lei"]]["name"].upper(), "ISDA 2002",
                       n["csa"] or "", n["trades"], round(mtm, 1)])
        autosize(ws, [13, 23, 44, 16, 16, 11, 12])
    set_xlsx_props(wb, "ccr.batch")
    wb.save(path)
    normalize_zip(path, dt.datetime(2026, 10, 6, 6, 15, 0))


# ------------------------------------------------------------------ house limit register
def limits_workbook(w, limits, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Register"
    ws["A1"] = "House Limit Register at 30 September 2026"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Limits in GBP m. Maintained by Credit Risk Management under the Credit Authorities Matrix."
    ws.append([])
    hdr = ["Ultimate parent LEI", "Obligor group", "House limit (GBP m)", "Approved by", "Last review",
           "Next review"]
    ws.append(hdr)
    for c in range(1, len(hdr) + 1):
        ws.cell(row=4, column=c).font = Font(bold=True)
    rng = np.random.default_rng(world.SEED + 21)
    auth = ["Credit Committee", "CCO", "Senior Credit Officer", "Board Risk Committee"]
    for top in sorted(limits, key=lambda l: w.ent[l]["name"]):
        lim = limits[top]
        last = dt.date(2025, 10, 1) + dt.timedelta(days=int(rng.integers(0, 360)))
        a = auth[3] if lim >= 150 else (auth[0] if lim >= 40 else auth[int(rng.integers(1, 3))])
        ws.append([top, w.ent[top]["name"], lim, a, last.strftime("%d/%m/%Y"),
                   (last + dt.timedelta(days=365)).strftime("%d/%m/%Y")])
    autosize(ws, [24, 48, 18, 22, 12, 12])
    set_xlsx_props(wb, "Credit Risk Management")
    wb.save(path)
    normalize_zip(path, dt.datetime(2026, 10, 1, 16, 48, 0))


# ------------------------------------------------------------------ sector report (management basis)
def sector_report(w, path):
    SIC = {"10": "C10 Food products", "11": "C11 Beverages", "13": "C13 Textiles", "17": "C17 Paper",
           "18": "C18 Printing", "20": "C20 Chemicals", "22": "C22 Rubber and plastics", "24": "C24 Basic metals",
           "28": "C28 Machinery", "35": "D35 Electricity and gas", "41": "F41 Construction of buildings",
           "47": "G47 Retail trade", "49": "H49 Land transport", "50": "H50 Water transport",
           "52": "H52 Warehousing", "55": "I55 Accommodation", "61": "J61 Telecommunications",
           "62": "J62 Computer programming", "64": "K64 Financial services", "66": "K66 Auxiliary financial",
           "68": "L68 Real estate", "81": "N81 Services to buildings", "86": "Q86 Human health"}
    agg = {}
    for f in w.fac:
        if f.limit[4] is None:
            continue
        s = w.ent[f.lei]["sector"] or "64"
        rate = truth.FX[f.ccy][4]
        a = agg.setdefault(s, [0, 0.0, 0.0])
        a[0] += 1
        a[1] += f.limit[4] * 1e6 / rate
        a[2] += f.drawn[4] / rate
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "By SIC division"
    ws["A1"] = "Credit portfolio by SIC division, 30 September 2026"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Management basis: facility limits and drawn balances, loan book only, GBP m"
    ws.append([])
    ws.append(["SIC division", "Facilities", "Limits (GBP m)", "Drawn (GBP m)", "Share of limits"])
    tot = sum(v[1] for v in agg.values())
    for s in sorted(agg, key=lambda k: -agg[k][1]):
        v = agg[s]
        ws.append([SIC.get(s, s), v[0], round(v[1] / 1e6, 1), round(v[2] / 1e6, 1), round(v[1] / tot, 4)])
    ws.append(["Total", sum(v[0] for v in agg.values()), round(tot / 1e6, 1),
               round(sum(v[2] for v in agg.values()) / 1e6, 1), 1.0])
    for r in range(5, ws.max_row + 1):
        ws.cell(row=r, column=5).number_format = "0.0%"
    autosize(ws, [32, 11, 15, 14, 15])
    set_xlsx_props(wb, "Portfolio MI")
    wb.save(path)
    normalize_zip(path, dt.datetime(2026, 10, 8, 9, 20, 0))


# ------------------------------------------------------------------ agenda (docx)
def agenda_docx(w, requests, path):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    doc.add_paragraph("Calder & Wey Bank plc").runs[0].bold = True
    doc.add_paragraph("Credit Committee, Wednesday 4 November 2026, 10:00, Committee Room 3, 61 Lothian Wharf")
    doc.add_paragraph("Part B: new commitment requests")
    doc.add_paragraph("Papers circulated Friday 30 October. Limit checks to the secretary by Monday 2 November "
                      "(LMS-03). Secretary: Russell Hussain.")
    tbl = doc.add_table(rows=1, cols=7)
    tbl.style = "Table Grid"
    hdr = ["Item", "Borrower", "Relationship", "Facility", "Amount", "Tenor", "Purpose"]
    for i, h in enumerate(hdr):
        tbl.rows[0].cells[i].text = h
    rel_label = {"X": "Kelderby", "W": "Meridale", "A": "Brauneck (Germany)", "B": "Corrin", "C": "Pellow",
                 "D": "Stannard Capital"}
    for i, k in enumerate(["X", "W", "A", "B", "C", "D"]):
        bkey, ftype, amt, tenor, purpose = requests[k]
        lei = getattr(w, k)[bkey]
        row = tbl.add_row().cells
        row[0].text = "B%d" % (i + 1)
        row[1].text = "%s (LEI %s)" % (w.ent[lei]["name"], lei)
        row[2].text = rel_label[k]
        row[3].text = ftype
        row[4].text = "GBP %.1fm" % amt
        row[5].text = tenor
        row[6].text = purpose
    doc.add_paragraph("")
    doc.add_paragraph("Part C (for noting): limit excesses reported since the last meeting; quarterly "
                      "large exposures return (Regulatory Reporting).")
    cp = doc.core_properties
    cp.author = "Russell Hussain"
    cp.last_modified_by = "Russell Hussain"
    cp.created = dt.datetime(2026, 10, 7, 16, 12, 0)
    cp.modified = dt.datetime(2026, 10, 9, 11, 3, 0)
    cp.title = "Credit Committee agenda 4 November 2026"
    cp.comments = ""
    cp.revision = 3
    doc.save(path)
    normalize_zip(path)


# ------------------------------------------------------------------ PDFs
def _pdf(path, title, author, blocks):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab import rl_config
    rl_config.invariant = 1
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13)
    h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                       spaceBefore=6)
    t = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=17)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=56, rightMargin=56, topMargin=56, bottomMargin=56,
                            title=title, author=author, creator="", producer="", subject="")
    story = []
    for kind, text in blocks:
        story.append(Paragraph(text, {"t": t, "h": h, "p": body}[kind]))
        story.append(Spacer(1, 4 if kind != "t" else 8))
    doc.build(story)
    data = buf.getvalue()
    stamp = b"D:20261008141500+01'00'"
    data = data.replace(b"D:20000101000000+00'00'", stamp)
    for s in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(s, b" " * len(s))
    with open(path, "wb") as fh:
        fh.write(data)


def policy_pdf(path):
    B = [
        ("t", "Calder &amp; Wey Bank plc<br/>Credit Concentration Policy"),
        ("p", "Version 4.2. Approved by the Board Risk Committee on 17 March 2026. Owner: Chief Credit Officer. "
              "Next review: March 2027."),
        ("h", "1 Purpose"),
        ("p", "1.1 This policy sets how the Bank groups the parties it lends to, how it measures its exposure to "
              "each group, and how house limits are held against that exposure. It applies to every booking "
              "entity of the Bank and to every product that creates credit exposure to a non-bank counterparty."),
        ("h", "2 Obligor groups"),
        ("p", "2.1 An Obligor Group is an entity together with every entity consolidated with it by the same "
              "ultimate parent in accounting-consolidation terms. The Bank reads consolidation from the GLEIF "
              "relationship records (IS_DIRECTLY_CONSOLIDATED_BY and IS_ULTIMATELY_CONSOLIDATED_BY) kept in the "
              "reference-data archive."),
        ("p", "2.2 An international branch is part of the legal entity it is a branch of."),
        ("p", "2.3 A fund that a group entity manages or advises is not consolidated by that group because it is "
              "managed by it. A managed fund is its own Obligor Group unless a consolidation relationship says "
              "otherwise."),
        ("p", "2.4 A lapsed registration, whether of an LEI or of a relationship record, does not end the entity "
              "or the relationship. A relationship ends on the end date of its relationship period."),
        ("p", "2.5 Where an LEI has merged into another, exposure recorded against the merged LEI belongs to the "
              "successor from the date of the merger."),
        ("p", "2.6 An entity that reports no consolidating parent, or for which a parent reporting exception is "
              "filed, heads its own Obligor Group."),
        ("p", "2.7 Relationship-management group codes in the customer master record coverage and pricing "
              "relationships. They are not Obligor Groups and are not used for limits."),
        ("h", "3 Exposure"),
        ("p", "3.1 Exposure to an Obligor Group is the sum, over its entities, of: (a) drawn balances on all "
              "facilities; (b) 50 per cent of the undrawn balance of committed facilities (term loans and "
              "revolving credit facilities), with undrawn balances of uncommitted facilities counting at nil; "
              "(c) investment securities issued by the entity, at carrying value; and (d) for each derivative "
              "netting set, the net mark-to-market where positive, less cash collateral held under the credit "
              "support annex attached to that netting set, and never less than nil. Non-cash collateral is not "
              "deducted, and netting sets are not offset against one another."),
        ("p", "3.2 Amounts in other currencies are converted to sterling at the Treasury closing rate for the "
              "measurement date."),
        ("p", "3.3 Exposure is measured at each quarter-end from the Credit Risk Data Mart quarter-end extracts."),
        ("h", "4 House limits"),
        ("p", "4.1 Every Obligor Group to which the Bank has exposure carries a house limit in the House Limit "
              "Register, approved under the Credit Authorities Matrix and reviewed at least annually."),
        ("p", "4.2 Exposure above the house limit is a limit excess. It is reported to the Chief Credit Officer "
              "within two business days and to the Board Risk Committee at its next meeting."),
        ("p", "4.3 New commitments are checked against house limits under the Limit Monitoring Standard (LMS-03)."),
        ("h", "5 Outside this policy"),
        ("p", "5.1 Regulatory large exposures reporting is run by Regulatory Reporting on the regulatory basis "
              "and is not governed by this policy. Exposures to central governments and to banks are managed "
              "under the Treasury Counterparty Policy."),
    ]
    _pdf(path, "Credit Concentration Policy v4.2", "Credit Risk Management", B)


def lms_pdf(path):
    B = [
        ("t", "LMS-03 Limit utilisation projection and new commitments"),
        ("p", "Limit Monitoring Standard. Version 2.0, effective 1 July 2026. Owner: Head of Credit Portfolio "
              "Analytics. Supersedes the January 2025 issue."),
        ("h", "1 Scope"),
        ("p", "1.1 This standard applies to every request for a new commitment presented to Credit Committee "
              "and to the quarterly limit utilisation report."),
        ("h", "2 Projection"),
        ("p", "2.1 The projection date is the latest quarter-end for which the quarter-end extracts are closed."),
        ("p", "2.2 The exposure of an Obligor Group at the next quarter-end is projected as its exposure at the "
              "projection date plus the least-squares slope, per quarter, of its exposure at the five quarter-ends "
              "ending on the projection date, the quarters numbered 1 to 5."),
        ("p", "2.3 Projections are made for each Obligor Group as constituted at the projection date, from that "
              "group's exposure at each of the five quarter-ends."),
        ("p", "2.4 Exposure is measured under section 3 of the Credit Concentration Policy, in pounds and "
              "without rounding. Projected exposure is reported in GBP m to one decimal place."),
        ("h", "3 New commitments"),
        ("p", "3.1 The exposure of a new commitment is its full amount for a term loan and 50 per cent of its "
              "amount for a revolving credit facility, which is undrawn at signing."),
        ("p", "3.2 Credit Committee may approve the largest amount, in multiples of GBP 100,000 and not more "
              "than the amount requested, for which projected exposure plus the exposure of the new commitment "
              "does not exceed the house limit. Where no amount qualifies, the request is referred to the Board "
              "Risk Committee."),
        ("p", "3.3 Utilisation is projected exposure divided by the house limit."),
        ("h", "4 Records"),
        ("p", "4.1 The limit check for each request is filed with the committee papers and kept for seven years."),
    ]
    _pdf(path, "LMS-03 Limit utilisation projection and new commitments", "Credit Portfolio Analytics", B)


# ------------------------------------------------------------------ field reference and extract log
FIELD_REF = """# Credit Risk Data Mart: field reference

Quarter-end extracts, release 2026-Q3 (closed 9 October 2026). Maintained by Credit Risk Data.

## loan_book_qe_extracts.csv

One row per facility per quarter-end extract (`extract_date`), from the core lending system.

| Field | Meaning |
|---|---|
| facility_ref | Facility identifier. LN for loan facilities, OD for overdrafts. |
| booking_entity | CWB-LDN (Calder & Wey Bank plc, London) or CWB-DUB (Calder & Wey Bank Europe DAC, Dublin). |
| customer_id | Customer master identifier. |
| customer_lei | LEI held on the customer master at the extract date. Blank where none is held. |
| customer_name | Name as held on the customer master. |
| rm_group_code | Relationship-management group code held on the customer master at the extract date. |
| facility_type | TERM term loan, RCF revolving credit facility, OVD overdraft. |
| committed | Y for committed facilities, N for uncommitted. |
| currency | Facility currency. All amounts in this file are in facility currency. |
| facility_limit, drawn_balance, undrawn_balance | Limit, drawn principal and undrawn amount at the extract date. |
| migrated_from | Set on the receiving facility when a facility moves between booking entities. Until the source ledger closes at the following month-end, the facility appears in the extracts of both booking entities; the receiving facility is the record. |
| sic_division | SIC 2007 division of the customer. |

## treasury_investment_positions_qe.csv

Treasury investment book positions at each quarter-end, from the custodian. `position_date` is DD/MM/YYYY.
`carrying_value` is in position currency. `issuer_lei` is as delivered on the custodian feed and is blank where
the feed carries none; issuer LEIs are maintained against ISINs in the GLEIF ISIN-to-LEI file.

## ccr_netting_set_exposure_qe.xlsx

Run CCR-NS-01 from the trading risk system, one sheet per quarter-end close, one row per netting set. Net MTM is
reported in GBP thousands, as the trading risk system holds it. Where a close is rerun, the rerun is added as a
further sheet for that date marked R2, and the rerun is the record for that close.

## csa_collateral_held_qe.csv

Collateral held from counterparties under credit support annexes, by CSA reference and valuation date
(DD-MON-YYYY). `amount_held` is in the collateral currency, in units.

## treasury_fx_closing_rates.csv

Treasury closing rates at each quarter-end. `rate` is units of the quote currency per GBP 1.

## gleif_lei_records_qe_archive.csv, gleif_relationship_records_qe_archive.csv

The GLEIF concatenated files (LEI-CDF 3.1 and RR-CDF 2.1 CSV) as last published on each quarter-end date, filtered to the
reference-data universe and archived by Reference Data. `archive_date` is added by the archive; all other columns
are as GLEIF publishes them.

## gleif_reporting_exceptions_20260930.csv, isin_lei_20260930.csv

GLEIF reporting exceptions and the GLEIF ISIN-to-LEI relationship file as published on 30 September 2026, filtered
to the reference-data universe.

## house_limit_register_20260930.xlsx

House limits by Obligor Group, keyed by the LEI of the group's ultimate parent.

## obligor_ratings_qe.csv

Internal rating grade by customer at each quarter-end (master scale MRS-2).

## sector_concentration_2026Q3.xlsx

Quarterly portfolio MI pack, sector page.
"""


def field_reference(path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(FIELD_REF)


def extract_log(target, path):
    lines = ["CRDM quarter-end release 2026-Q3", "Closed 2026-10-09 18:31 by crdm_release (job QE-CLOSE-07)", ""]
    sources = {
        "loan_book_qe_extracts.csv": "core lending (extracts 2025-09-30 to 2026-09-30)",
        "loan_book_cwb_dub_20251231_late.csv": "core lending, CWB-DUB, 2025-12-31 (late delivery)",
        "treasury_investment_positions_qe.csv": "custodian positions feed",
        "ccr_netting_set_exposure_qe.xlsx": "trading risk system, run CCR-NS-01",
        "csa_collateral_held_qe.csv": "collateral management system",
        "treasury_fx_closing_rates.csv": "Treasury closing rates",
        "gleif_lei_records_qe_archive.csv": "Reference Data archive of GLEIF concatenated file (level 1)",
        "gleif_relationship_records_qe_archive.csv": "Reference Data archive of GLEIF concatenated file (level 2)",
        "gleif_reporting_exceptions_20260930.csv": "GLEIF reporting exceptions, 30 Sep 2026",
        "isin_lei_20260930.csv": "GLEIF ISIN-to-LEI relationship file, 30 Sep 2026",
        "obligor_ratings_qe.csv": "rating system MRS-2",
    }
    lines.append("%-46s %10s  %s" % ("file", "rows", "source"))
    for fn in sorted(sources):
        p = os.path.join(target, fn)
        if fn.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            n = sum(ws.max_row - 4 for ws in wb.worksheets)
        else:
            n = sum(1 for _ in open(p, encoding="utf-8")) - 1
        lines.append("%-46s %10d  %s" % (fn, n, sources[fn]))
    lines.append("")
    lines.append("Late delivery: the CWB-DUB core lending extract for 2025-12-31 missed the QE-CLOSE window and was "
                 "delivered on 2026-01-21. It is held as loan_book_cwb_dub_20251231_late.csv and forms part of the "
                 "2025-12-31 extract.")
    lines.append("")
    lines.append("Reference-data universe: customers, issuers in the treasury book, derivative counterparties and "
                 "their related entities.")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
