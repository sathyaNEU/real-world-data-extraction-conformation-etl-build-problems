"""task305 documents: the property team's spend-share model sheet (pdf) and the GIS analyst's notes on the data
folder (md)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=17, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.6, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.4):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.2)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E9E4")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def model_sheet(path):
    body, h1, h2, small = _styles()
    s = []
    s.append(Paragraph("Marrable Foodstores: store sales model", h1))
    s.append(Paragraph("Spend-share parameters. Property and Network Planning, recalibrated June 2025 (supersedes the "
                       "parameters of March 2022). Owner: %s." % P.PEOPLE["property"], small))
    s.append(Spacer(1, 4))
    s.append(Paragraph("1. What the model does", h2))
    s.append(Paragraph("The model shares grocery spend among the grocery stores that can win it. A store's share of the "
                       "spend that starts at a place is its pull times its deterrence from that place, divided by the sum "
                       "of pull times deterrence over every store in the share. A store's sales are the sum of its shares "
                       "of the spend.", body))
    s.append(Paragraph("2. The stores in the share", h2))
    s.append(Paragraph("Every grocery store on the VOA rating list for the planning region whose primary description is "
                       "SUPERMARKET AND PREMISES, SUPERSTORE AND PREMISES or FOOD STORE AND PREMISES and whose summary "
                       "valuation measures 280 m2 or more, our own stores included. A proposed store enters the share at "
                       "its proposed floor area from the site schedule.", body))
    s.append(Paragraph("3. Parameters", h2))
    s.append(_table([["Term", "Value", "Source"],
                     ["Pull", "floor area in m2, to the power 1.0", "summary valuation, main measure"],
                     ["Deterrence", "exp(-0.22 x road km)", "fitted, June 2025"],
                     ["Road km", "1.25 x straight-line km between grid references", "network sample, 2022"],
                     ["Grid reference", "an output area at its population-weighted centroid; a store, a site or any "
                                        "other address at its postcode's grid reference", "ONS centroids; ONSPD"],
                     ["Households", "an output area's households as Census 2021 counted them, not rolled forward",
                      "Census 2021, TS041"],
                     ["In-store share", "88 per cent of households' grocery spend; the rest is bought online and is "
                                        "not shared", "household spend survey, 2025"]],
                    [30, 82, 52]))
    s.append(Paragraph("4. Appraisal of a new store (Finance)", h2))
    s.append(Paragraph("A store's contribution is 26 per cent of its sales less its running costs. A new store adds to the "
                       "chain's contribution 26 per cent of its own sales, less 26 per cent of the sales it takes from "
                       "our existing stores, less its running costs as the site schedule estimates them: a year of "
                       "trading at 2026 prices.", body))
    s.append(Paragraph("5. Calibration", h2))
    s.append(Paragraph("Fitted in June 2025 to our stores' card spend by month and cardholder home sector for FY2024/25. "
                       "The deterrence held at 0.22 and the floor-area power at 1.0, both as in 2022; the road factor was "
                       "not refitted.", body))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Store sales model: spend-share parameters", author=P.ORG,
                            creator=P.ORG, subject="Property and Network Planning", invariant=1)
    doc.build(s, onFirstPage=_footer("Marrable Foodstores, Property and Network Planning. Internal."),
              onLaterPages=_footer("Marrable Foodstores, Property and Network Planning. Internal."))


NOTES = """# Property data folder: notes

Hazel Lucas (GIS), 9 October 2026. What each file is and how it came to us, for the 2027 site appraisal.

## Geography and spend

- `census2021_ts041_households_oa.csv`: Census 2021 table TS041 (number of households) for the output areas of the
  planning region, as downloaded from the ONS. Households are counted at the census day, 21 March 2021.
- `oa21_population_weighted_centroids.csv`: ONS population-weighted centroids of the 2021 output areas, British
  National Grid metres.
- `grocery_spend_estimates_2026_oa21.csv`: the data provider's modelled mean weekly grocery spend per household, by
  2021 output area, at 2026 prices (licence renewed March 2026).
- `onspd_may2026_lq.csv`: our extract of the ONS Postcode Directory (May 2026) for the LQ postcode area. `doterm` is
  the month a postcode was terminated, blank while it is live; `usertype` 1 is a large user. Grid references are to
  1 metre; `osgrdind` 1 means the reference is within the building of the matched address.

## Rating list

- `voa_list_entries_2026_lq.txt`: the VOA's compiled 2026 list entries for the billing authority (code 3510), in the
  VOA's own layout: one entry per line, fields separated by asterisks, no header. The fields, in order: entry number,
  billing authority code, community code, BA reference, primary description code, primary description, UARN, full
  property identifier, firm's name, number or name, street, town, postal district, county, postcode, effective date,
  composite indicator, rateable value, appeal settlement code, assessment reference, list alteration date, SCAT code
  and suffix, sub-street 3, sub-street 2, sub-street 1, case number, current from date, current to date.
- `voa_summary_valuations_2026_lq.csv`: the main measure from each assessment's summary valuation (floor area in m2,
  parking spaces or pitches), keyed by UARN and assessment reference. Assessments valued without a measured summary
  (rental evidence, receipts and expenditure) have no row.

## Our estate and the shortlist

- `store_estate_2026.xlsx`: the ten stores (floor area as the rating list measures it, sales for FY2025/26, April to
  March, and the share of sales paid by card).
- `card_spend_by_home_sector_fy2025_26.csv`: the acquirer's merchant-insight feed: card spend at each of our stores by
  month and the postcode sector of the cardholder's registered address, FY2025/26. Every sector with a card in the
  month is listed.
- `site_shortlist_2027.xlsx`: the six sites on the 2027 shortlist, with the proposed floor area on the rating list's
  basis and the estimated annual running costs (agents' heads of terms for rent, our rates estimate, the staffing plan
  and other running costs).
- `spend_share_model_2025.pdf`: the spend-share parameters and Finance's appraisal rule.

## Distribution, staffing and buses

- `tms_stop_export_20251006_20260329.csv`: the transport management system's stop export from its go-live on
  6 October 2025: one row per stop on a trip from the Loderwell Gate distribution centre, deliveries (`DEL`) and
  collections of cages and recyclables (`COL`). Times are the system's own (UTC); `cases` and `cages` come from the
  trip's load plan, stop by stop.
- `goods_in_receipts_20251006_20260329.csv`: goods-in receipts scanned on the stores' handhelds, local time, with the
  delivery note and its cases. The handhelds went in store by store from October 2025 (101 to 106 so far); 107 to
  110 still book deliveries in on paper.
- `wfm_paid_hours_20251006_20260329.csv`: the workforce system's paid hours report, 6 October 2025 to 29 March 2026:
  employee number, location, date, role and paid hours.
- `ta_punches_20251006_20260329.csv`: the time-and-attendance clock-ins and clock-outs for the same weeks, local
  time, with the terminal each was made on; `ta_terminals.csv` is the terminal register (store, door, installed).
- `gtfs_sallowmere_motor_services_20261002.zip`, `gtfs_wrentoft_district_coaches_20261002.zip`: each operator's
  timetable data as published on the Bus Open Data Service on 2 October 2026 (GTFS).

## Also in the folder

- `dft_aadf_count_points_lq_2025.csv`: DfT annual average daily flows at the count points in the area, 2025.
- `customer_survey_store_scores_2025.csv`: the 2025 customer survey's store scores.
"""


def notes(path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(NOTES)
