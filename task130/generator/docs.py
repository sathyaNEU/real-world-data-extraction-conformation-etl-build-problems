"""The pack's documents: short and functional, in the voice of the people who own them."""
import datetime as dt
import os
import shutil
import subprocess
import tempfile

import docx
from docx.shared import Pt, Cm
import openpyxl
import xlcalc
from openpyxl.styles import Font, PatternFill, Alignment

import world as W

MONTHS = ["Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027"]
LOT2_2627 = {1: 64.00, 2: 78.50, 3: 92.00, 4: 109.50}       # nightly-paid, per night
LOT3_2627 = {1: 296.10, 2: 361.20, 3: 427.80, 4: 512.60}    # self-contained leased, per week
UPLIFT = 1.038                                            # August 2026 CPI, applied from 1 April 2027
LOT2_2728 = {s: round(v * UPLIFT, 2) for s, v in LOT2_2627.items()}
LOT3_2728 = {s: round(v * UPLIFT, 2) for s, v in LOT3_2627.items()}


def _doc(author, title, created):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = Cm(1.8)
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.created = created
    cp.modified = created
    cp.revision = 3
    cp.comments = cp.keywords = cp.subject = cp.category = ""
    return d


def _para(d, text, bold=False, size=None, space_after=4, italic=False):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    if size:
        r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def _hdr(ws, row, values, widths=None):
    for j, h in enumerate(values, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6E1")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for j, w in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j + 1)].width = w


def notice_pdf(out_path):
    created = dt.datetime(2026, 9, 15, 11, 20)
    d = _doc("Nicola Robinson", "Tenter House: notice to end the lease", created)
    _para(d, "Corvane Property Services Ltd  ·  Unit 4, Medway Court, Rochester ME1 1RW", size=8, italic=True)
    _para(d, "15 September 2026", space_after=10)
    _para(d, "Housing Needs Service\nLarkmoor Borough Council\nCivic Centre, Larkmoor", space_after=10)
    _para(d, "By email and first class post", size=8.5, italic=True, space_after=10)
    _para(d, "Tenter House, 2 Wharf Road, Larkmoor: lease of 178 self-contained flats", bold=True, space_after=8)
    _para(d, "Dear Housing Needs Service,")
    _para(d, "We write as managing agent for the freeholder of Tenter House. The freeholder has exchanged contracts "
             "for the sale of the building to a developer of purpose-built student accommodation, with completion "
             "on vacant possession. Under clause 14.2 of the lease dated 1 April 2021 the landlord may end the lease "
             "on six months' notice in writing where the building is to be sold or redeveloped.")
    _para(d, "This letter is that notice. The lease will end on 31 March 2027 and we will need vacant possession of "
             "all 178 flats on that date. We will continue to manage and repair the building in the usual way until "
             "then, and the rent will continue at the current rate for every flat until the lease ends, occupied "
             "or not.")
    _para(d, "We understand the council will want to plan how the households living at Tenter House are rehoused. "
             "Our on-site team will give your officers whatever access they need. Please let us know if the council "
             "would like to hand flats back before 31 March as they fall vacant; we would be glad to agree a "
             "reduced rent for any flat returned early.")
    _para(d, "Yours faithfully,", space_after=14)
    _para(d, "Nicola Robinson\nHead of Property, Corvane Property Services Ltd", space_after=6)
    _para(d, "Corvane Property Services Ltd. Registered in England and Wales no. 08812457.", size=7.5, italic=True)
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "notice.docx")
    d.save(src)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.move(os.path.join(tmp, "notice.pdf"), out_path)
    shutil.rmtree(tmp)


def procedure_docx(out_path):
    created = dt.datetime(2026, 9, 18, 15, 5)
    d = _doc("Declan Morton", "Tenter House closure: placement procedure", created)
    _para(d, "Larkmoor Borough Council  ·  Housing Needs Service  ·  Temporary Accommodation", size=8, italic=True)
    _para(d, "Tenter House closure: placement procedure", bold=True, size=13, space_after=2)
    _para(d, "Declan Morton, TA placements team leader. 18 September 2026. Agreed with Maria Field (TA and "
             "procurement) and Eileen Nicholls (housing register and lettings).", size=8.5, space_after=10)
    _para(d, "Corvane served notice on 15 September: the Tenter House lease ends on 31 March 2027. This note sets "
             "out how we handle placements until then so that every family moves once.", space_after=8)
    items = [
        "No new placements into Tenter House from 15 September 2026. Vacant flats stay empty; we are not handing "
        "them back early.",
        "No household is moved out of Tenter House before 31 March 2027 except into settled accommodation "
        "(a social housing let or a private let through Larkmoor Lettings). Moves to other TA are suspended for "
        "Tenter House households.",
        "Move-on lets to Tenter House households carry on exactly as for every other household we owe the main duty. "
        "Nothing about the closure changes how lets are made.",
        "Every household living in Tenter House on 31 March 2027 moves that day to a replacement self-contained unit "
        "called off under Lot 3 of the Kent and Medway TA dynamic purchasing system, starting on 1 April 2027.",
        "A replacement unit has the number of bedrooms the household needs as assessed at the date of this note: "
        "the latest bedroom-need review on the system, or the need at the decision where there has been no review. "
        "Households needing four or more bedrooms get a four-bedroom unit.",
        "Lot 3 units are paid weekly at the DPS rate for the year in which the unit starts.",
        "Households owed only the interim duty are not placed in Tenter House; every household there is owed the "
        "main duty.",
    ]
    for k, t in enumerate(items, 1):
        _para(d, "%d.  %s" % (k, t), space_after=6)
    _para(d, "")
    _para(d, "Queries to Declan Morton. The call-off itself is Maria Field's.", size=8.5, italic=True)
    d.save(out_path)


def plan_xlsx(out_path, actuals):
    """The lettings team's move-on plan for 2026/27, revised in September."""
    wb = openpyxl.Workbook()
    wb.properties.creator = "Eileen Nicholls"
    wb.properties.lastModifiedBy = "Eileen Nicholls"
    wb.properties.created = dt.datetime(2026, 3, 20, 10, 15)
    wb.properties.modified = dt.datetime(2026, 9, 14, 16, 40)
    wb.properties.title = "Move-on plan 2026-27"
    ws = wb.active
    ws.title = "Revised 14 Sep 2026"
    _sheet(ws, "Move-on plan 2026/27, revised 14 September 2026", W.PLAN_REVISED, actuals,
           "Revised for the rephasing agreed with the nominating landlords on 9 September and the Brook Meadow "
           "phase 2 handover (four three-bed and five four-bed homes in February 2027, five three-bed and four "
           "four-bed in March 2027).")
    o = wb.create_sheet("Original Mar 2026")
    _sheet(o, "Move-on plan 2026/27, as agreed 20 March 2026 (superseded)", W.PLAN_ORIGINAL, actuals,
           "Superseded by the revision of 14 September 2026.")
    n = wb.create_sheet("Notes")
    notes = [
        "Move-on lets: social housing lets through our nominations and private lets through Larkmoor Lettings, "
        "made to households we owe the main housing duty.",
        "Figures are numbers of lets, by the number of bedrooms in the home let and the month the tenancy starts.",
        "October 2026 includes lets already offered and accepted whose tenancies start in October.",
        "April to September 2026 columns are lets made (tenancy started), from the move-on lets log.",
        "Four-bedroom column includes homes with four or more bedrooms.",
        "Owner: Eileen Nicholls, housing register and lettings. Updated quarterly or when a handover date moves.",
    ]
    for i, t in enumerate(notes, 1):
        n.cell(row=i, column=1, value=t)
    n.column_dimensions["A"].width = 120
    xlcalc.freeze(wb)
    wb.save(out_path)


def _sheet(ws, title, plan, actuals, note):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = note
    ws["A2"].font = Font(italic=True, size=9)
    past = ["Apr 2026", "May 2026", "Jun 2026", "Jul 2026", "Aug 2026", "Sep 2026"]
    _hdr(ws, 4, ["Bedrooms"] + ["%s (let)" % m for m in past] + MONTHS + ["Oct-Mar total"],
         [11] + [11] * 12 + [13])
    for r, s in enumerate(W.SIZES, 5):
        ws.cell(row=r, column=1, value="4+" if s == 4 else str(s))
        for j, v in enumerate(actuals[s]):
            ws.cell(row=r, column=2 + j, value=int(v))
        for j, v in enumerate(plan[s]):
            ws.cell(row=r, column=8 + j, value=int(v))
        ws.cell(row=r, column=14, value=int(sum(plan[s])))
    r = 9
    ws.cell(row=r, column=1, value="All").font = Font(bold=True)
    for j in range(2, 15):
        col = openpyxl.utils.get_column_letter(j)
        ws.cell(row=r, column=j, value="=SUM(%s5:%s8)" % (col, col)).font = Font(bold=True)
    ws.freeze_panes = "B5"


def prices_xlsx(out_path):
    wb = openpyxl.Workbook()
    wb.properties.creator = "Kent and Medway TA Procurement Partnership"
    wb.properties.lastModifiedBy = "Kent and Medway TA Procurement Partnership"
    wb.properties.created = dt.datetime(2026, 2, 24, 9, 0)
    wb.properties.modified = dt.datetime(2026, 9, 22, 12, 10)
    wb.properties.title = "TA DPS price schedule"
    ws = wb.active
    ws.title = "Rates"
    ws["A1"] = "Kent and Medway temporary accommodation DPS: price schedule"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Rates per unit, excluding VAT (not chargeable). 2027/28 rates apply to units starting on or after "
                "1 April 2027 and to every unit from that date; uplift by August 2026 CPI, 3.8 per cent.")
    ws["A2"].font = Font(italic=True, size=9)
    _hdr(ws, 4, ["Lot", "Description", "Charging basis", "Bedrooms", "2026/27 rate (GBP)", "2027/28 rate (GBP)"],
         [6, 46, 16, 10, 18, 18])
    r = 5
    for s in W.SIZES:
        for lot, desc, basis, a, b in (
                ("2", "Nightly-paid self-contained, spot purchase", "per night", LOT2_2627[s], LOT2_2728[s]),
                ("3", "Self-contained, leased for 12 months, call-off", "per week", LOT3_2627[s], LOT3_2728[s])):
            ws.cell(row=r, column=1, value=lot)
            ws.cell(row=r, column=2, value=desc)
            ws.cell(row=r, column=3, value=basis)
            ws.cell(row=r, column=4, value="4+" if s == 4 else str(s))
            ws.cell(row=r, column=5, value=a).number_format = "#,##0.00"
            ws.cell(row=r, column=6, value=b).number_format = "#,##0.00"
            r += 1
    ws.freeze_panes = "A5"
    xlcalc.freeze(wb)
    wb.save(out_path)


def weekly_position_xlsx(out_path, counts, th_flats):
    wb = openpyxl.Workbook()
    wb.properties.creator = "Declan Morton"
    wb.properties.lastModifiedBy = "Declan Morton"
    wb.properties.created = dt.datetime(2026, 9, 28, 8, 30)
    wb.properties.modified = dt.datetime(2026, 9, 28, 9, 5)
    wb.properties.title = "TA weekly position w/c 28 Sep 2026"
    ws = wb.active
    ws.title = "Position"
    ws["A1"] = "Temporary accommodation: weekly position, Monday 28 September 2026"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Households in TA at midnight on Sunday 27 September, by accommodation type and bedrooms needed."
    ws["A2"].font = Font(italic=True, size=9)
    types = ["Bed and breakfast", "Hostel", "Nightly-paid self-contained", "Private sector lease", "Tenter House"]
    _hdr(ws, 4, ["Accommodation type", "1 bed", "2 bed", "3 bed", "4+ bed", "All"], [30, 9, 9, 9, 9, 9])
    r = 5
    for t in types:
        ws.cell(row=r, column=1, value=t)
        for j, s in enumerate(W.SIZES, 2):
            ws.cell(row=r, column=j, value=int(counts.get((t, s), 0)))
        ws.cell(row=r, column=6, value="=SUM(B%d:E%d)" % (r, r))
        r += 1
    ws.cell(row=r, column=1, value="All TA").font = Font(bold=True)
    for j in range(2, 7):
        col = openpyxl.utils.get_column_letter(j)
        ws.cell(row=r, column=j, value="=SUM(%s5:%s%d)" % (col, col, r - 1)).font = Font(bold=True)
    r += 2
    ws.cell(row=r, column=1, value="Tenter House flats").font = Font(bold=True)
    r += 1
    _hdr(ws, r, ["", "1 bed", "2 bed", "3 bed", "4 bed", "All"])
    r += 1
    for label, vals in (("Flats", W.TH_UNITS), ("Occupied", th_flats)):
        ws.cell(row=r, column=1, value=label)
        for j, s in enumerate(W.SIZES, 2):
            ws.cell(row=r, column=j, value=int(vals.get(s, 0)))
        ws.cell(row=r, column=6, value="=SUM(B%d:E%d)" % (r, r))
        r += 1
    ws.cell(row=r, column=1, value="Tenter House: no new placements since 15 September (lease ends 31 March 2027).")
    ws.cell(row=r, column=1).font = Font(italic=True, size=9)
    xlcalc.freeze(wb)
    wb.save(out_path)


DICTIONARY = """Larkmoor Borough Council, Housing Needs Service
Extracts for the TA and procurement team: field definitions
Prepared by the housing systems team, 1 October 2026. Extracts run to 30 September 2026 inclusive.

General
  Dates are ISO (YYYY-MM-DD). An empty date means the event had not happened by 30 September 2026.
  case_ref identifies one homelessness application. A household that applies again gets a new case_ref.
  Bedrooms: 4 means four or more.

homelessness_cases_2026-09-30.csv
  One row per case open at any time from 1 April 2018, or opened since.
  application_date             date the application was taken
  household_type               as recorded at application
  decision                     Main duty accepted / Main duty not owed / Awaiting decision
  decision_date                date of the main duty decision. For Main duty accepted this is the date
                               the main housing duty was accepted.
  bedrooms_needed_at_decision  bedroom need assessed at the decision (later reviews are in
                               bedroom_need_reviews.csv)
  case_status                  Open or Closed on 30 September 2026
  closed_date, closure_reason  when and why the case closed. A case owed the main duty closes when the
                               duty ends, normally on the start date of a settled tenancy.

bedroom_need_reviews.csv
  One row per review that changed a household's bedroom need. The new need applies from review_date.

ta_placements_2018-04_2026-09.csv
  One row per temporary accommodation placement live at any time from 1 April 2018. A household's
  stay in TA can run across several placements.
  accommodation_type           Bed and breakfast / Hostel / Nightly-paid self-contained /
                               Private sector lease / Tenter House
  unit_ref                     see accommodation_register_2026-09.csv
  placement_end                the day the household moved out; empty if it is still there
  end_reason                   Moved to other TA, or Left TA: <reason>. "Left TA: duty continues,
                               staying with family or friends" means the household left TA but is still
                               owed the main duty; its case stays open.

moveon_lets_2018-04_2026-09.csv
  One row per move-on let (social housing let through our nominations, or a private let through
  Larkmoor Lettings) to a household owed the main duty, tenancy start from 1 April 2018.
  bedrooms                     bedrooms in the home let
  offer_date                   date the offer was made
  tenancy_start                first day of the tenancy, the day the household moves in and leaves TA
  let_status                   Tenancy started, or Accepted, tenancy to start (offer accepted, tenancy
                               starting after 30 September 2026)

accommodation_register_2026-09.csv
  TA units used since 1 April 2018: unit_ref, type, address or establishment, bedrooms (self-contained
  units), provider and contract basis.
"""


def dictionary_txt(out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(DICTIONARY)
