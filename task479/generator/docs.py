"""The pack's documents: the authority's placement guidelines for the 2027 pilot, the 2025 outreach close-out summary,
the data dictionary and the export manifest."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P      # noqa: E402
import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b2430")
GREY = colors.HexColor("#5b6470")
BLUE = colors.HexColor("#1f4e6b")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.2, leading=10.4, textColor=INK)
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.2, leading=10.4, textColor=INK)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14.5, leading=18.5, textColor=BLUE, spaceAfter=3)
H1S = ParagraphStyle("h1s", fontName="LiberationSans", fontSize=9.0, leading=12.2, textColor=GREY, spaceAfter=12)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.8, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)
AUTH = "Tarrow Sound Regional Flood Authority"


def _doc(path, title, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.4)
        canvas.drawString(0.9 * inch, 0.6 * inch, footer)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                          bottomMargin=0.95 * inch, title=title, author=AUTH, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, right=()):
    data = []
    for i, r in enumerate(rows):
        row = []
        for k, v in enumerate(r):
            st = CELLB if i == 0 else (CELLR if k in right else CELL)
            row.append(Paragraph(str(v), st))
        data.append(row)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def fmt(n):
    return "{:,}".format(int(n))


# ---------------------------------------------------------------------------------------------- the guidelines
GUIDELINES = [
    ("1. Purpose", [
        "1.1 Under the Private Flood Placement Agreement of 30 June 2026, two admitted private flood insurers will "
        "offer flood coverage from 1 March 2027 to the owners of elevated insured buildings in five of the "
        "Authority's member counties. These guidelines set how the Board of Directors designates the five counties "
        "and the county next in line.",
    ]),
    ("2. Definitions", [
        "2.1 An insured building is a building with an NFIP building policy in force: a dwelling, general property or "
        "residential condominium building association policy with building coverage. A condominium building insured "
        "by its association's policy is one insured building. A unit owner's policy insures a unit and a contents "
        "policy insures contents; neither makes a building insured.",
        "2.2 An elevated insured building is a building insured on 30 September 2026 whose lowest floor elevation on "
        "the building policy then in force is at or above the base flood elevation on that policy. A building whose "
        "policy shows no base flood elevation is not an elevated insured building.",
        "2.3 A building's claims are the claims under its building policies. A paid building claim is one on which a "
        "building payment was made; a claim that paid only contents or Increased Cost of Compliance, or that closed "
        "without payment, is not a paid building claim.",
        "2.4 A building-year is 365.25 days of building coverage. A building's building-years are the days from "
        "1 January 2001 through 31 December 2025 on which it was insured, each day counted once.",
    ]),
    ("3. The expected claim rate", [
        "3.1 A member county's expected claim rate is the number of paid building claims that the floods of 2001 "
        "through 2025 would bring the county's elevated insured buildings as they stand on 30 September 2026, per "
        "1,000 of those buildings' building-years.",
        "3.2 The rate is computed from the NFIP policy and claims records that FEMA shares with the Authority under "
        "its data sharing agreement, as extracted on 2 October 2026.",
    ]),
    ("4. Designation", [
        "4.1 The pilot runs in the five member counties with the lowest expected claim rates. The county with the "
        "sixth lowest rate is next in line: if the board of supervisors of a designated county declines the pilot "
        "by 31 January 2027, the county next in line takes its place.",
        "4.2 The Board designates the counties at its regular meeting of 12 November 2026, and the Authority files "
        "them with the State Department of Insurance by 1 December 2026 under section 14-209 of the State Insurance "
        "Code, on which the Department approves the participating insurers' rates for the five counties.",
    ]),
    ("5. The record brought with the designation", [
        "5.1 With the designation the Flood Insurance Program Manager brings to the Board, for each member county, "
        "the claims on losses in 2026 that carry a building payment, unit owners' claims included, with the building "
        "payments made on them as of the extract, and the buildings in the Authority's elevation and acquisition "
        "projects that were not completed on 30 September 2026, with the federal share obligated to them.",
    ]),
]
CONTROL = [["Revision", "Adopted", "Resolution", "Change"],
           ["1", "13 August 2026", "26-14", "First issue, for the 2027 pilot"]]


def write_guidelines(path):
    d, frame = _doc(path, "2027 Private Flood Placement Pilot: County Selection Guidelines",
                    AUTH + "  |  Flood Insurance Program  |  2027 Private Flood Placement Pilot Guidelines")
    story = [Paragraph("2027 Private Flood Placement Pilot: County Selection Guidelines", H1),
             Paragraph(AUTH + ", Flood Insurance Program. Adopted by the Board of Directors on 13 August 2026 "
                       "(Resolution 26-14). Owner: Flood Insurance Program Manager, Samantha Walter.", H1S)]
    for head, paras in GUIDELINES:
        story.append(Paragraph(head, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    story.append(Paragraph("Schedule. Member counties", H2))
    rows = [["County", "FIPS code", "NFIP communities"]] + [[W.NAME[f], f, ", ".join(W.COMMUNITIES[f])] for f in W.FIPS]
    story.append(_table(rows, [1.5 * inch, 0.9 * inch, 3.2 * inch]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Document control", H2))
    story.append(_table(CONTROL, [0.7 * inch, 1.15 * inch, 0.85 * inch, 3.9 * inch]))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def guidelines_text():
    out = []
    for head, paras in GUIDELINES:
        out.append(head)
        out.extend(paras)
    return out


# ---------------------------------------------------------------------------------------------- the close-out
def closeout_table(x):
    """Each county's outreach in 2025, with the building policies in force at the year's end."""
    B = x["buildings"]
    end = dt.date(2025, 12, 31)
    inforce = {f: 0 for f in W.FIPS}
    for p in x["book"]:
        if p["form"] == "B" and p["start"] <= end and (p["end"] is None or end < p["end"]):
            inforce[B[p["bi"]]["fips"]] += 1
    rng = W.stream(30)
    rows = [["County", "Workshops", "Attendees", "Elevation certificates filed", "Private quote referrals",
             "Building policies in force, 31 Dec 2025"]]
    tot = [0, 0, 0, 0, 0]
    for f in W.FIPS:
        ws = int(rng.integers(2, 7))
        att = int(ws * rng.integers(14, 46))
        ec = int(inforce[f] * float(rng.uniform(0.006, 0.02)))
        ref = int(inforce[f] * float(rng.uniform(0.004, 0.015)))
        rows.append([W.NAME[f], ws, att, ec, ref, fmt(inforce[f])])
        tot = [tot[0] + ws, tot[1] + att, tot[2] + ec, tot[3] + ref, tot[4] + inforce[f]]
    rows.append(["All counties", tot[0], tot[1], tot[2], tot[3], fmt(tot[4])])
    return rows, inforce


CLOSE_PARAS = [
    "The 2025 flood insurance outreach ran from 3 February to 21 November 2025 in all fourteen member counties. Staff "
    "mailed every NFIP policyholder in the Authority's communities a plain-language letter on the second year of "
    "Risk Rating 2.0 premiums, held evening workshops with the county floodplain administrators, and kept the "
    "elevation certificate help desk open three days a week. The help desk filed the certificates below with the "
    "owners' insurers; most were for buildings whose premiums had been set without one.",
    "At the Board's request staff also sounded the private flood market. Seven admitted insurers answered the "
    "request for information of 14 April 2025; two have since signed the Private Flood Placement Agreement of 30 June "
    "2026, under which they will quote elevated insured buildings in five member counties from March 2027. The "
    "referrals in the table are policyholders who asked at a workshop or by letter to be told when private quotes "
    "are offered in their county.",
    "Next steps: the Board adopted the placement guidelines for the 2027 pilot on 13 August 2026, and the Flood "
    "Insurance Program Manager will bring the designation of the five counties to the Board in November 2026. The "
    "2026 outreach will follow the June flood and Hurricane Teodor with claims workshops in the counties most "
    "affected.",
]


def write_closeout(path, x):
    d, frame = _doc(path, "2025 Flood Insurance Outreach: Close-out Summary",
                    AUTH + "  |  Flood Insurance Program  |  2025 Outreach Close-out")
    rows, _ = closeout_table(x)
    story = [Paragraph("2025 Flood Insurance Outreach: Close-out Summary", H1),
             Paragraph(AUTH + ", Flood Insurance Program. Prepared by Debbie Brady, Outreach Coordinator, for the "
                       "Board of Directors, 19 February 2026; next steps updated 2 September 2026.", H1S),
             Paragraph(CLOSE_PARAS[0], BODY), Paragraph(CLOSE_PARAS[1], BODY),
             Paragraph("Table 1. Outreach in 2025 by county", H2),
             _table(rows, [1.3 * inch, 0.75 * inch, 0.75 * inch, 1.05 * inch, 1.0 * inch, 1.35 * inch],
                    right=(1, 2, 3, 4, 5)),
             Paragraph("Building policies in force are the NFIP dwelling, general property and condominium association "
                       "policies with building coverage in force on 31 December 2025 in the county's communities, from "
                       "FEMA's data sharing extract.", CELL),
             Spacer(1, 8), Paragraph("Next steps", H2), Paragraph(CLOSE_PARAS[2], BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the dictionary
DICTIONARY = """Tarrow Sound Regional Flood Authority, Flood Insurance Program
Data dictionary for the files of the 2027 pilot designation. Issue 2, 2 October 2026.

nfip_dsa_policy_history_2026-10-02.csv
FEMA's data sharing extract of NFIP policies for the Authority's communities, pulled 2 October 2026: every policy
in force at any time since 1 January 2001. One row per policy, with the rating of its latest term.
  policy_number                the NFIP policy number
  prior_policy_number          where the policy was written to replace another, the policy it replaced
  company_code                 the write-your-own company or servicing agent issuing the policy: 14418 Gulfline
                               Mutual Insurance Company; 15306 Tarrow Southern Insurance Company; 16127 Bayward
                               Casualty Company; 17452 Shorebrook Indemnity Company; 10099 NFIP Direct Servicing Agent
  nfip_building_id             FEMA's identifier of the insured building
  county_fips, community_number   the building's county and NFIP community
  policy_form                  DP dwelling; GP general property; RCBAP residential condominium building association
  condo_indicator              N not a condominium policy; A condominium association; U condominium unit owner
  condo_units                  units in the building (association policies)
  unit_number                  the unit insured (unit owners' policies)
  occupancy_code               terms before 1 October 2021: 1 single family, 2 two to four family, 3 other
                               residential, 4 non-residential; later terms: 11 single family home, 12 residential
                               building of two to four units, 15 residential condominium association building,
                               16 residential unit in a multi-unit building, 18 non-residential building,
                               19 non-residential unit in a multi-unit building
  original_effective_date      first day of the policy's cover
  term_effective_date, term_expiration_date   the latest term, which covers from its effective date to the day
                               before its expiration date
  policy_status                ACTIVE in force on the extract date; EXPIRED not renewed at the expiration date;
                               CANCELLED cancelled on the cancellation date
  cancellation_date            the policy's last day of coverage is the day before
  cancellation_reason          01 building sold or ownership changed; 02 insurance no longer required; 08 building
                               demolished or removed; 22 cancelled and rewritten under a new policy number
  building_coverage, contents_coverage   limits of the latest term, dollars; a contents policy has no building
                               coverage
  building_deductible          dollars
  total_premium                the latest term's premium with the surcharges and fees, dollars
  flood_zone                   the rated flood zone
  base_flood_elevation, lowest_floor_elevation   feet, on the datum in elevation_datum, from the elevation
                               certificate the latest term was rated on
  elevation_datum              NGVD29 (National Geodetic Vertical Datum of 1929) or NAVD88 (North American Vertical
                               Datum of 1988); certificates completed before 2012 used NGVD 1929
  elevation_certificate_date   date of that certificate
  post_firm_construction       Y built after the community's first flood insurance rate map
  number_of_floors

nfip_dsa_claims_2001-2019.csv
FEMA's data sharing extract of NFIP claims for the Authority's communities, losses from 1 January 2001 to
31 December 2019, in the layout FEMA used before its 2023 release. One row per claim.
  CLAIM_NO, POLICY_NO, BLDG_ID, COUNTY_FIPS, COMMUNITY_NO
  DATE_OF_LOSS, DATE_REPORTED, DATE_CLOSED   MM/DD/YYYY
  CLAIM_STATUS                 C closed; CWOP closed without payment
  OCCUPANCY                    the earlier occupancy codes above
  CONDO_IND                    N, A, U as above
  FLOOD_ZONE, BFE, LOWEST_FLR_ELEV, ELEV_DATUM   the building's rating for the claim: elevations in feet on the
                               datum given
  WATER_DEPTH_IN               depth of water in the building above the lowest floor, inches
  BLDG_DAMAGE_AMT, CNTS_DAMAGE_AMT   damage to the building and to contents as adjusted, dollars
  BLDG_PAID_AMT, CNTS_PAID_AMT, ICC_PAID_AMT   payments on building, contents and Increased Cost of Compliance
                               coverage, dollars
  CAUSE_OF_LOSS                1 tidal water overflow; 2 stream, river or lake overflow; 4 accumulation of rainfall
  CAT_NO                       the catastrophe number FEMA gave the flood, where it gave one

nfip_dsa_claims_2020-2026.csv
The same extract for losses from 1 January 2020, pulled 2 October 2026, in the layout of FEMA's 2023 release, which
renamed the fields and writes dates as UTC timestamps. Payments are as of the extract.
  claimNumber, policyNumber, buildingId, countyCode, communityId
  dateOfLoss, originalReportDate, claimClosedDate   UTC timestamps
  claimStatus                  Closed; Closed without payment; Open
  occupancyType                the current occupancy codes above
  condominiumIndicator         N, A, U as above
  floodZone, baseFloodElevation, lowestFloorElevation, verticalDatum   as in the earlier layout
  waterDepthInches             depth of water in the building above the lowest floor, inches
  buildingDamageAmount, contentsDamageAmount   dollars
  amountPaidOnBuildingClaim, amountPaidOnContentsClaim, amountPaidOnIccClaim   dollars
  causeOfDamage                as CAUSE_OF_LOSS above
  catastropheNumber            as CAT_NO above

tsrfa_hma_grants_export_2026-09-30.xlsx
The Authority's grants management system, export of 30 September 2026: its hazard mitigation assistance projects
(elevations and acquisitions under the Hazard Mitigation Grant Program, Flood Mitigation Assistance and Building
Resilient Infrastructure and Communities grants), every project approved since 2006.
  Projects sheet: project_number; program; disaster_number (HMGP); project_title; applicant (the county applying);
    project_status (Open, Closed); approved_date; period_of_performance_end; federal_cost_share_pct;
    approved_total_cost and federal_share_obligated (dollars, the project's properties not withdrawn);
    property_count (properties not withdrawn)
  Properties sheet: project_number; property_id (the Authority's property number); site_address;
    community_number; measure (Elevation, Acquisition); approved_cost (dollars); federal_share (dollars);
    property_status (Approved, Under construction, Completed, Withdrawn); status_date
  Inspections sheet: property_id; project_number; inspection (Pre-construction site visit; Final, the inspection
    of the completed elevation or acquisition); inspection_date; result (Pass, Fail); inspector_id

tsrfa_property_building_crosswalk.csv
The Authority's property numbers matched to FEMA's building identifiers: property_id, nfip_building_id,
match_method (address, parcel, manual), matched_date.

tsrfa_vertical_datum_offsets.csv
navd88_minus_ngvd29_ft for each member county: an elevation on NGVD 1929 plus the offset is the elevation on
NAVD 1988.

tsrfa_member_counties.csv
The fourteen member counties: county_fips, county, member_since, nfip_communities, board_seat.

nfip_crs_community_classes_2026-10.csv
Community Rating System classes of the members' NFIP communities in October 2026, with the premium discounts
they give in and outside the special flood hazard area (per cent).

tsrfa_firm_revision_log_2001-2026.csv
The flood insurance rate map revisions and letters of map revision effective in the members' communities since
2001: community_number, county_fips, map_action, effective_date, case_number, panels, description.

tsrfa_private_flood_placement_guidelines_2027.pdf
The Board's county selection guidelines for the 2027 pilot (13 August 2026).

tsrfa_2025_flood_insurance_outreach_closeout.pdf
The 2025 outreach close-out summary (19 February 2026, next steps updated 2 September 2026).

export_manifest.csv
This list of files.
"""


def write_dictionary(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(DICTIONARY)


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]
MANIFEST = {
    "policies": ("NFIP policies, data sharing extract", "FEMA", "2026-10-02", "policies in force since 2001-01-01"),
    "claims1": ("NFIP claims, data sharing extract, earlier layout", "FEMA", "2026-10-02", "losses 2001-01-01 to 2019-12-31"),
    "claims2": ("NFIP claims, data sharing extract, 2023 release layout", "FEMA", "2026-10-02",
                "losses 2020-01-01 to 2026-10-02"),
    "register": ("Hazard mitigation grants export", "Authority grants management system", "2026-09-30",
                 "projects approved since 2006"),
    "crosswalk": ("Property to FEMA building crosswalk", "Flood Insurance Program", "2026-09-30", "the grants export"),
    "offsets": ("Vertical datum offsets by county", "Floodplain Management", "2013-04-22", "member counties"),
    "members": ("Member counties", "Board office", "2026-10-02", "current"),
    "crs": ("Community Rating System classes", "FEMA", "2026-10-01", "October 2026"),
    "firm": ("Flood map revision log", "Floodplain Management", "2026-09-30", "effective 2001-01-01 to 2026-09-30"),
    "guidelines": ("2027 pilot county selection guidelines", "Board of Directors", "2026-08-13", "the 2027 pilot"),
    "closeout": ("2025 outreach close-out summary", "Flood Insurance Program", "2026-02-19", "2025"),
    "dictionary": ("Data dictionary", "Flood Insurance Program", "2026-10-02", "these files"),
}


def manifest_rows(n):
    return [[P.FILES[k], d, s, p, c, n.get(k, "")] for k, (d, s, p, c) in MANIFEST.items()]
