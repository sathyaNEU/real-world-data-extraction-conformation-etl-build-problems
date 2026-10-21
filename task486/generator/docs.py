"""task486 documents and workbooks: the State Data Center's notes on the 2020 census release, the State Department on
Aging's FY2027 area plan instructions, the agency's provider allocation policy, the state's licensed residential care
list for the county, the agency's provider directory, its field guide and its data inventory."""
import docx
import openpyxl
from docx.shared import Pt, RGBColor
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A     # noqa: E402
import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1f22")
GREY = colors.HexColor("#5d636a")
TEAL = colors.HexColor("#1d4e57")
PLUM = colors.HexColor("#4a2f4f")
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.4, leading=13.0, textColor=INK, spaceAfter=6)
SERIF = ParagraphStyle("serif", fontName="LiberationSerif", fontSize=10.8, leading=14.6, textColor=INK, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.0, leading=10.0, textColor=INK)
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=7.6, leading=9.8, textColor=GREY)


def _styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=13.5, leading=17, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9, leading=12, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    return h1, h1s, h2


def _doc(path, title, author, footer, serif=False):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSerif" if serif else "LiberationSans", 7.4)
        canvas.drawString(0.9 * inch, 0.55 * inch, footer)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.85 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e3e8ea"):
    t = Table([[Paragraph(str(c), CELL) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b9c0c4")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


# ---------------------------------------------------------------- the State Data Center's notes
NOTES = [
    ("What the file is",
     ["The Demographic and Housing Characteristics File (DHC), released in May 2023, carries the 2020 Census counts of "
      "the population by age, sex, race, Hispanic or Latino origin, household relationship and group quarters type, and "
      "of housing units by occupancy and tenure, for every level of census geography down to the census block. Its "
      "reference date is Census Day, 1 April 2020.",
      "Two tables answer most local requests. P12 (Sex by Age for Selected Age Categories) counts residents in 23 age "
      "groups for each sex; its total is the area's population, household and group quarters together. H1 (Housing "
      "Units) counts the housing units in the area, occupied or vacant."]),
    ("Geography",
     ["Every census block lies in one block group and every block group in one census tract; tracts nest in the county. "
      "A block's 15-digit code is the state (2 digits), county (3), tract (6) and block (4), and the block's first "
      "digit is its block group. Downloads from data.census.gov add a summary-level prefix to the code in GEO_ID "
      "(1400000US for tracts, 1500000US for block groups, 1000000US for blocks) and carry two header rows, the variable "
      "code and its label."]),
    ("How the counts are protected",
     ["The Census Bureau protects respondents' confidentiality in the 2020 Census with a disclosure avoidance system "
      "built on differential privacy. The system adds statistical noise to each count at each geographic level, from "
      "the nation down to the block, and then processes the noisy counts so that every published count is a "
      "non-negative whole number and the counts at each level add up exactly to the level above: the blocks of a block "
      "group add up to the block group, the block groups of a tract to the tract, and the tracts to the county. Each "
      "cell of a table is processed this way, so the 23 age groups of a block add up to its total as well.",
      "Some counts are held exactly as enumerated. These invariants are the total population of each state, the number "
      "of housing units in every block and every larger area, and the number and type of group quarters facilities "
      "(nursing facilities, college residence halls, correctional facilities and the like) in every block. A block "
      "with no housing units and no group quarters facility has no residents in the published tables.",
      "Because the noise is added at every level and does not grow with an area's size, counts for areas and groups with "
      "few people carry more noise, relative to their size, than counts for large areas and groups. The Census Bureau "
      "publishes accuracy measures for the release on its website."]),
    ("Earlier census products",
     ["Counts from the 2010 Census were protected by swapping households between blocks, not by added noise, so 2010 "
      "and 2020 block counts are not alike in their errors. The American Community Survey's five-year estimates are "
      "survey estimates for a five-year period, with margins of error, and are not census counts."]),
]


def write_notes(path):
    h1, h1s, h2 = _styles(TEAL)
    d, frame = _doc(path, "2020 Census DHC: notes for local users", "State Data Center",
                    "State Data Center  |  Technical bulletin 2023-04 (revised February 2024)")
    story = [Paragraph("2020 Census Demographic and Housing Characteristics File: notes for local users", h1),
             Paragraph("State Data Center, technical bulletin 2023-04. Issued June 2023, revised February 2024.", h1s)]
    for head, paras in NOTES:
        story.append(Paragraph(head, h2))
        for p in paras:
            story.append(Paragraph(p, SANS))
    story.append(Spacer(1, 6))
    story.append(_table([["Table", "Universe", "Cells", "Lowest level"],
                         ["P12 Sex by Age for Selected Age Categories", "Total population", "49 (total, 2 sexes, "
                          "23 age groups each)", "Block"],
                         ["H1 Housing Units", "Housing units", "1", "Block"]],
                        [2.3 * inch, 1.4 * inch, 1.6 * inch, 1.0 * inch]))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the state's instructions
INSTRUCTIONS = [
    ("1. Purpose and due date",
     ["Each area agency on aging files an area plan update for FY2027 (1 October 2026 to 30 September 2027) through the "
      "Department's planning portal by 13 November 2026. The update carries the agency's provider structure, its "
      "census counts and its service figures for the year just ended, and the Department uses it to monitor the "
      "agency's plan and to check the agency's own allocation to its providers."]),
    ("2. Provider structure",
     ["List each provider the agency funds for nutrition and supportive services and the provider area it serves, as "
      "the areas are drawn on the day of filing. An agency that redrew its provider areas since its last full plan "
      "attaches the area definitions."]),
    ("3. Census counts",
     ["For each provider area, report the number of residents aged 60 and over and the number aged 75 and over on "
      "Census Day, 1 April 2020, counting household and group quarters population. Use the provider areas as drawn "
      "since 1 July 2023 for agencies that redrew them that year. Provider areas are not census tabulation areas, so "
      "their counts are estimated from the 2020 Census Demographic and Housing Characteristics release; round each "
      "area's count to the nearest ten.",
      "The areas of an agency together cover its whole planning and service area, so their counts together are the "
      "planning and service area's."]),
    ("4. Service figures for FY2026 (1 October 2025 to 30 September 2026)",
     ["4.1 Home-delivered meals served. Count every meal handed to an eligible participant, by delivery date; a frozen "
      "or shelf-stable pack counts as the meals it holds. Report each meal under the provider responsible for the "
      "participant, which is the provider of the area the participant lives in.",
      "4.2 Active home-delivered meal clients. Count the participants with a home-delivered meal episode open on "
      "30 September 2026 who were alive that day, each once, under the provider of the area the participant lives in.",
      "Report service figures as whole numbers. Keep the working files the figures were built from for monitoring."]),
    ("5. Questions",
     ["Planning staff of the Department's Office of Area Agency Operations answer questions on these instructions "
      "through the planning portal."]),
]


def write_instructions(path):
    h1, h1s, h2 = _styles(PLUM, serif=True)
    d, frame = _doc(path, "FY2027 Area Plan Update: instructions", W.STATE_UNIT,
                    "State Department on Aging  |  Office of Area Agency Operations  |  AP-27-02", serif=True)
    story = [Paragraph("FY2027 Area Plan Update: instructions for area agencies on aging", h1),
             Paragraph("State Department on Aging, Office of Area Agency Operations. Program instruction AP-27-02, "
                       "issued 14 August 2026.", h1s)]
    for head, paras in INSTRUCTIONS:
        story.append(Paragraph(head, h2))
        for p in paras:
            story.append(Paragraph(p, SERIF))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the agency's policy
POLICY = [
    ("Purpose", "This policy sets how the Kelvane Area Agency on Aging divides its Title III-C nutrition funds among the "
                "senior-services providers it funds, one in each provider area."),
    ("Provider areas", "The Board adopted six provider areas on 15 June 2023, effective 1 July 2023: Wickmoor City and "
                       "Fallowmere Town, and North, East, South and West Kelvane, whose boundaries now run to the ring "
                       "roads around both towns and to the river, so that each rural center serves the edge "
                       "neighborhoods its routes already reach. The county's Department of Planning and Development "
                       "keeps the block assignment of each area."),
    ("Allocation", "From FY2024, each provider receives a base amount of $85,000 a year. The remainder of the Title III-C "
                   "funds is divided among the providers, 70 percent in proportion to the provider area's residents "
                   "aged 60 and over and 30 percent in proportion to its residents aged 75 and over, as filed in the "
                   "agency's area plan for the year."),
    ("Review", "The Board reviews this policy when the State Department on Aging changes its intrastate formula or the "
               "agency redraws its provider areas."),
]


def write_policy(path):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    t = d.add_paragraph()
    r = t.add_run("Kelvane Area Agency on Aging")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0x1d, 0x4e, 0x57)
    d.add_paragraph("Board policy N-3: provider allocation of nutrition funds. Adopted 21 September 2023.")
    for head, body in POLICY:
        p = d.add_paragraph()
        rr = p.add_run(head)
        rr.bold = True
        d.add_paragraph(body)
    d.save(path)


# ---------------------------------------------------------------- workbooks
def write_facilities(path, b, geoid):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kelvane County"
    ws.append(["Licensed residential care facilities, Kelvane County. State licensing list as of 1 September 2026; "
               "census block added by the Kelvane Area Agency on Aging."])
    ws.append([])
    ws.append(["License", "Facility", "Type", "Address", "Licensed beds", "Census block (2020)"])
    lic = iter(range(41207, 49999, 389))
    for i, bl in enumerate(b.blocks):
        if bl["gq"]:
            name, typ, n = bl["gq"]
            town = W.SEAT if bl["tract"] < "9" else W.TOWN2
            beds = n + (12 if typ.startswith("Nursing") else 6)
            lic_type = "Skilled nursing facility" if typ.startswith("Nursing") else "Assisted living residence"
            ws.append(["NF-%05d" % next(lic) if typ.startswith("Nursing") else "AL-%05d" % next(lic), name, lic_type,
                       "%d %s, %s" % (100 + 40 * (i % 23), ["Linden Ave", "Hospital Dr", "College St", "Elm St",
                                                          "Mill Rd", "Orchard Rd"][i % 6], town), beds, geoid(bl)])
    ws["A1"].font = Font(bold=True)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E3E8EA")
    for col, w in zip("ABCDEF", (11, 38, 30, 30, 13, 18)):
        ws.column_dimensions[col].width = w
    wb.save(path)


def write_providers(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Providers"
    ws.append(["Provider code", "Provider", "Provider area", "Address", "Home-delivered meal routes"])
    addr = {"WMS": "212 Church St, Wickmoor", "FCC": "40 Depot St, Fallowmere", "NKS": "18 County Rd 12, Ashby Corner",
            "EKS": "960 Creamery Rd, Wickmoor", "SKS": "5 Quarry Rd, Halden Mills", "WKS": "77 River Rd, Fallowmere"}
    for code, name, area, nr in A.PROVIDERS:
        ws.append([code, name, area, addr[code], ", ".join("%s-%02d" % (code, k + 1) for k in range(nr))])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E3E8EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCDE", (13, 30, 17, 32, 60)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wb.save(path)


# ---------------------------------------------------------------- the field guide and the inventory
GUIDE = """KELVANE AREA AGENCY ON AGING: FIELD GUIDE TO THE PLANNING FILES
Kept by planning; last revised 9 October 2026.

hdm_client_roster_2026-10-09.csv
  One row per client the agency has served with home-delivered meals since 1 October 2024.
  client_id             the agency's client number
  state_participant_id  the client's number in the state participant registry
  birth_year            year of birth
  home_block            the 2020 census block of the client's home address, geocoded by the agency
  meals_per_day         meals the client's care plan provides on a delivery day (1 or 2)
  schedule              Weekday hot, Weekday hot + weekend pack, or Weekly frozen

hdm_service_episodes_2026-10-09.csv
  One row per home-delivered meal episode.
  episode_id, client_id, service (HDM)
  provider_code         the provider that enrolled the client
  enrolled, closed      dates; closed is blank while the episode is open
  close_reason          as entered by the case manager

hdm_route_delivery_log_fy2026.csv
  One row per item handed over on a route, as entered on the route tablet, 1 October 2025 to 30 September 2026.
  delivery_id, tablet_id, route_id
  provider_code         the provider operating the route
  client_id, delivery_date, item_code
  uploaded_at           when the tablet uploaded the row, local time

hdm_item_codes.csv      the items a route hands over and the meals each holds

state_death_match_runs_2025-07_to_2026-10.csv
  The State Department on Aging's monthly match of registry numbers against the state's death records, statewide,
  as sent to every area agency. One row per match: run_date, state_participant_id (the registry number matched),
  date_of_death, match_basis.

state_registry_number_links.csv
  The state participant registry's links between numbers, statewide: prior_participant_id, current_participant_id,
  linked_on, reason.

provider_area_blocks.csv (county Department of Planning and Development)
  One row per census block and assignment. TRACT_BLOCK is the 2020 tract and block codes written as one number;
  EFFECTIVE_TO is blank while the assignment is in force.

kelvane_address_points_2026-10-02.csv (county Department of Planning and Development)
  The county's address points register as of 2 October 2026: one row per address point, with the 2020 census block it
  falls in, its status and the date it was added.

dhc2020_*.csv           2020 Census DHC tables for Kelvane County, downloaded by planning; see the State Data
                        Center's notes. The block table is the long form planning keeps, one row per block, sex and
                        age group.
acs2022_5yr_*.csv       American Community Survey 2018-2022 five-year estimates, table B01001, block groups.
licensed_residential_care_kelvane.xlsx   the state's licensing list, census block added by planning.
kaaa_provider_directory.xlsx             providers, provider areas and routes.
"""


def write_guide(path):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(GUIDE.replace("\n", "\r\n"))


INVENTORY = [
    ("dhc2020_kelvane_blocks_sex_by_age.csv", "2020 Census DHC table P12 for every block in Kelvane County, long form",
     "Census Day 2020", "data.census.gov, downloaded by planning", "2026-10-02"),
    ("dhc2020_kelvane_block_groups_p12.csv", "2020 Census DHC table P12, block groups", "Census Day 2020",
     "data.census.gov, downloaded by planning", "2026-10-02"),
    ("dhc2020_kelvane_county_tracts_p12.csv", "2020 Census DHC table P12, the county and its tracts", "Census Day 2020",
     "data.census.gov, downloaded by planning", "2026-10-02"),
    ("dhc2020_kelvane_blocks_h1.csv", "2020 Census DHC table H1, housing units by block", "Census Day 2020",
     "data.census.gov, downloaded by planning", "2026-10-02"),
    ("dhc2020_p12_h1_column_metadata.csv", "variable codes and labels for the DHC downloads", "", "data.census.gov",
     "2026-10-02"),
    ("dhc2020_notes_for_local_users.pdf", "State Data Center technical bulletin 2023-04", "", "State Data Center",
     "2026-10-02"),
    ("acs2022_5yr_kelvane_block_groups_b01001.csv", "ACS 2018-2022 five-year table B01001, block groups",
     "2018 to 2022", "data.census.gov, downloaded by planning", "2026-10-02"),
    ("provider_area_blocks.csv", "provider area of each census block, with the 2023 redraw",
     "July 2016 to date", "county Department of Planning and Development", "2026-10-02"),
    ("kelvane_address_points_2026-10-02.csv", "county address points register", "as of 2 October 2026",
     "county Department of Planning and Development", "2026-10-02"),
    ("licensed_residential_care_kelvane.xlsx", "state licensing list for the county, with census blocks",
     "as of 1 September 2026", "state licensing; blocks added by planning", "2026-09-08"),
    ("kaaa_provider_directory.xlsx", "providers, provider areas and routes", "FY2026", "agency", "2026-10-09"),
    ("kaaa_provider_allocation_policy_2023.docx", "Board policy N-3", "from FY2024", "agency", "2023-09-21"),
    ("fy2027_area_plan_update_instructions.pdf", "program instruction AP-27-02", "FY2027 update",
     "State Department on Aging", "2026-08-14"),
    ("hdm_client_roster_2026-10-09.csv", "home-delivered meal clients served since 1 October 2024",
     "to 9 October 2026", "agency case management system", "2026-10-09"),
    ("hdm_service_episodes_2026-10-09.csv", "home-delivered meal episodes", "to 9 October 2026",
     "agency case management system", "2026-10-09"),
    ("hdm_route_delivery_log_fy2026.csv", "route tablet delivery log", "1 October 2025 to 30 September 2026",
     "route tablet system", "2026-10-06"),
    ("hdm_item_codes.csv", "route item codes", "", "agency", "2026-10-06"),
    ("state_death_match_runs_2025-07_to_2026-10.csv", "the state's monthly death match, statewide",
     "runs of 5 July 2025 to 5 October 2026", "State Department on Aging", "2026-10-06"),
    ("state_registry_number_links.csv", "state participant registry number links, statewide", "to 5 October 2026",
     "State Department on Aging", "2026-10-06"),
    ("kaaa_field_guide.txt", "field guide to these files", "", "agency planning", "2026-10-09"),
]


def write_inventory(path):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["file", "contents", "period", "source", "received"])
    for r in INVENTORY:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
