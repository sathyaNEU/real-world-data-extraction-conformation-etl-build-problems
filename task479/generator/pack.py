"""The pack's data files, written from the world: FEMA's data-sharing extracts of NFIP policies and claims for the
authority's communities, the authority's grants-system export and crosswalk, and its lookups."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "policies": "nfip_dsa_policy_history_2026-10-02.csv",
    "claims1": "nfip_dsa_claims_2001-2019.csv",
    "claims2": "nfip_dsa_claims_2020-2026.csv",
    "register": "tsrfa_hma_grants_export_2026-09-30.xlsx",
    "crosswalk": "tsrfa_property_building_crosswalk.csv",
    "offsets": "tsrfa_vertical_datum_offsets.csv",
    "members": "tsrfa_member_counties.csv",
    "crs": "nfip_crs_community_classes_2026-10.csv",
    "firm": "tsrfa_firm_revision_log_2001-2026.csv",
    "guidelines": "tsrfa_private_flood_placement_guidelines_2027.pdf",
    "closeout": "tsrfa_2025_flood_insurance_outreach_closeout.pdf",
    "dictionary": "tsrfa_data_dictionary.txt",
    "manifest": "export_manifest.csv",
}
COMPANY = {"GLFM": ("14418", "Gulfline Mutual Insurance Company"), "TRSN": ("15306", "Tarrow Southern Insurance Company"),
           "BYWT": ("16127", "Bayward Casualty Company"), "SOUC": ("17452", "Shorebrook Indemnity Company"),
           "NFDS": ("10099", "NFIP Direct Servicing Agent")}
CENTRAL_DST = {}
COMPANY_NAME = "Tarrow Sound Regional Flood Authority"


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


def iso(d):
    return d.isoformat() if d else ""


def mdy(d):
    return d.strftime("%m/%d/%Y") if d else ""


def utc_offset(day):
    """Central time against UTC on a local date: -5 in daylight time, -6 in standard time (rules since 2007)."""
    if day.year not in CENTRAL_DST:
        mar = dt.date(day.year, 3, 1)
        start = mar + dt.timedelta(days=(6 - mar.weekday()) % 7 + 7)
        nov = dt.date(day.year, 11, 1)
        end = nov + dt.timedelta(days=(6 - nov.weekday()) % 7)
        CENTRAL_DST[day.year] = (start, end)
    s, e = CENTRAL_DST[day.year]
    return 5 if s <= day < e else 6


def utc_stamp(day, hh=0, mm=0):
    """A local Central time on a day written as FEMA's 2023 release writes it, in UTC with milliseconds."""
    t = dt.datetime(day.year, day.month, day.day, hh, mm) + dt.timedelta(hours=utc_offset(day))
    return t.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def ngvd(fips, v):
    """An elevation in feet on NGVD 1929 from NAVD 1988: NAVD88 = NGVD29 + offset."""
    return None if v is None else round(v - W.OFFSET[fips], 1)


def elev(b, ec):
    """An elevation certificate's lowest floor and base flood elevations as recorded, with its datum."""
    datum = W.datum_of(ec[0])
    lfe, bfe = ec[1], ec[2]
    if datum == "NGVD29":
        lfe, bfe = ngvd(b["fips"], lfe), ngvd(b["fips"], bfe)
    return lfe, bfe, datum


def num(v):
    return "" if v is None else ("%.1f" % v)


# ---------------------------------------------------------------------------------------------- policies
POLICY_COLS = ["policy_number", "prior_policy_number", "company_code", "nfip_building_id", "county_fips",
               "community_number", "policy_form", "condo_indicator", "condo_units", "unit_number", "occupancy_code",
               "original_effective_date", "term_effective_date", "term_expiration_date", "policy_status",
               "cancellation_date", "cancellation_reason", "building_coverage", "contents_coverage",
               "building_deductible", "total_premium", "flood_zone", "base_flood_elevation",
               "lowest_floor_elevation", "elevation_datum", "elevation_certificate_date", "post_firm_construction",
               "number_of_floors"]
RR2 = dt.date(2021, 10, 1)


def occupancy(b, form, when):
    """Legacy occupancy codes on records before the 2021 rating change, the current codes after."""
    new = when >= RR2
    if form == "U":
        return "16" if new else "1"
    if b["occ"] == "condo":
        return "15" if new else "3"
    if form == "T":
        return ("12" if b["occ"] == "2-4" else "19") if new else ("2" if b["occ"] == "2-4" else "4")
    return {"sf": ("11", "1"), "2-4": ("12", "2"), "nonres": ("18", "4")}[b["occ"]][0 if new else 1]


def policy_form(b, form):
    if form == "B" and b["occ"] == "condo":
        return "RCBAP"
    if b["occ"] == "nonres":
        return "GP"
    return "DP"


def policy_rows(x):
    B = x["buildings"]
    rows = []
    for p in x["book"]:
        b = B[p["bi"]]
        lfe, bfe, datum = elev(b, p["ec"])
        if p["end"] is None:
            status, canc = "ACTIVE", ""
        elif p["how"] == "E":
            status, canc = "EXPIRED", ""
        else:
            status, canc = "CANCELLED", iso(p["end"])
        cond = "A" if (p["form"] == "B" and b["occ"] == "condo") else ("U" if p["form"] == "U" else "N")
        rows.append([p["number"], p["prior"] or "", COMPANY[p["servicer"]][0], b["pid"], b["fips"], b["community"],
                     policy_form(b, p["form"]), cond, b["units"] if cond == "A" else "", p["unit"] or "",
                     occupancy(b, p["form"], p["term_start"]), iso(p["start"]), iso(p["term_start"]),
                     iso(p["term_end"] if p["how"] != "E" else p["end"]), status, canc, p["reason"] or "",
                     p["bcov"], p["ccov"], p["ded"], p["premium"], b["zone"], num(bfe), num(lfe), datum,
                     iso(p["ec"][0]), "Y" if b["post_firm"] else "N", b["floors"]])
    rows.sort(key=lambda r: (r[4], r[5], r[3], r[11], r[0]))
    return rows


# ---------------------------------------------------------------------------------------------- claims
CLAIM1_COLS = ["CLAIM_NO", "POLICY_NO", "BLDG_ID", "COUNTY_FIPS", "COMMUNITY_NO", "DATE_OF_LOSS", "DATE_REPORTED",
               "DATE_CLOSED", "CLAIM_STATUS", "OCCUPANCY", "CONDO_IND", "FLOOD_ZONE", "BFE", "LOWEST_FLR_ELEV",
               "ELEV_DATUM", "WATER_DEPTH_IN", "BLDG_DAMAGE_AMT", "CNTS_DAMAGE_AMT", "BLDG_PAID_AMT", "CNTS_PAID_AMT",
               "ICC_PAID_AMT", "CAUSE_OF_LOSS", "CAT_NO"]
CLAIM2_COLS = ["claimNumber", "policyNumber", "buildingId", "countyCode", "communityId", "dateOfLoss",
               "originalReportDate", "claimClosedDate", "claimStatus", "occupancyType", "condominiumIndicator",
               "floodZone", "baseFloodElevation", "lowestFloorElevation", "verticalDatum", "waterDepthInches",
               "buildingDamageAmount", "contentsDamageAmount", "amountPaidOnBuildingClaim",
               "amountPaidOnContentsClaim", "amountPaidOnIccClaim", "causeOfDamage", "catastropheNumber"]
CAT = {"2002-09-26": "02-71", "2005-08-29": "05-63", "2008-09-12": "08-58", "2012-08-29": "12-44", "2016-08-12": "16-39",
       "2019-07-12": "19-31", "2020-10-09": "20-52", "2024-09-26": "24-47", "2026-06-04": "26-22", "2026-09-17": "26-41"}


def cause(b, c):
    if c["kind"] == "local" or (W.KIND[b["fips"]] == "coast" and c["event"] in ("2016-08-12", "2019-07-12",
                                                                                 "2026-06-04", "2002-09-26")):
        return "4"
    return "1" if W.KIND[b["fips"]] == "coast" else "2"


def claim_fields(x, c):
    B = x["buildings"]
    b = B[c["bi"]]
    lfe, bfe, datum = elev(b, c["ec"])
    pol = c["policy"]
    cond = "A" if (c["form"] == "B" and b["occ"] == "condo") else ("U" if c["form"] == "U" else "N")
    status = c["status"]
    closed = c["closed"] if status != "OPEN" else None
    return dict(b=b, lfe=lfe, bfe=bfe, datum=datum, pol=pol, cond=cond, status=status, closed=closed)


def claim_rows(x, v):
    rows = []
    for c in x["claims"]:
        if c["day"] > W.PULL or c["reported"] > W.PULL:
            continue
        if (v == 1) != (c["day"].year <= 2019):
            continue
        f = claim_fields(x, c)
        b = f["b"]
        cat = CAT.get(c["event"], "") if c["kind"] == "major" else ""
        depth = c["depth_in"]
        if v == 1:
            rows.append([c["number"], f["pol"]["number"], b["pid"], b["fips"], b["community"], mdy(c["day"]),
                         mdy(c["reported"]), mdy(f["closed"]), {"CLOSED": "C", "CWOP": "CWOP", "OPEN": "O"}[f["status"]],
                         occupancy(b, c["form"], c["day"]), f["cond"], b["zone"], num(f["bfe"]), num(f["lfe"]),
                         f["datum"], depth, c["damage"] if c["form"] != "T" else 0, c["cdamage"], c["bpay_asof"],
                         c["cpay_asof"], c["icc"], cause(b, c), cat])
        else:
            rng = W.stream(20, c["bi"], c["reported"].toordinal())
            rows.append([c["number"], f["pol"]["number"], b["pid"], b["fips"], b["community"], utc_stamp(c["day"]),
                         utc_stamp(c["reported"], int(rng.integers(8, 17)), int(rng.integers(0, 60))),
                         utc_stamp(f["closed"], int(rng.integers(8, 18)), int(rng.integers(0, 60))) if f["closed"] else "",
                         {"CLOSED": "Closed", "CWOP": "Closed without payment", "OPEN": "Open"}[f["status"]],
                         occupancy(b, c["form"], dt.date(2026, 1, 1)), f["cond"], b["zone"], num(f["bfe"]),
                         num(f["lfe"]), f["datum"], depth, c["damage"] if c["form"] != "T" else 0, c["cdamage"],
                         "%.2f" % c["bpay_asof"], "%.2f" % c["cpay_asof"], "%.2f" % c["icc"], cause(b, c), cat])
    rows.sort(key=lambda r: (r[3], r[5][-4:] + r[5][:5] if v == 1 else r[5], r[0]))
    return rows


# ---------------------------------------------------------------------------------------------- the grants export
STREETS = ["Bayview", "Live Oak", "Cypress", "Magnolia", "Pelican", "Harbor", "Ridge", "River Bend", "Sabal", "Heron",
           "Marsh Hen", "Old Ferry", "Saltmeadow", "Tarrow", "Pine Hollow", "Cedar Point", "Shell Bank", "Willow Bend",
           "Levee", "Dockside", "Bluff", "Mill Creek", "Pecan", "Sweetgum", "Turtle Cove", "Landing", "Beacon",
           "Sandpiper", "Bayou", "Orchard", "Lighthouse", "Gulf Breeze", "Ferry Point", "Driftwood", "Clearwater"]
SUFFIX = ["Rd", "Dr", "Ln", "St", "Ave", "Ct", "Blvd", "Way", "Cir", "Loop"]


def address(b):
    rng = W.stream(21, W.CIDX[b["fips"]], int(b["pid"][5:11]))
    return "%d %s %s" % (int(rng.integers(100, 9900)), STREETS[int(rng.integers(0, len(STREETS)))],
                         SUFFIX[int(rng.integers(0, len(SUFFIX)))])


PROJECT_COLS = ["project_number", "program", "disaster_number", "project_title", "applicant", "project_status",
                "approved_date", "period_of_performance_end", "federal_cost_share_pct", "approved_total_cost",
                "federal_share_obligated", "property_count"]
PROPERTY_COLS = ["project_number", "property_id", "site_address", "community_number", "measure", "approved_cost",
                 "federal_share", "property_status", "status_date"]
INSPECTION_COLS = ["property_id", "project_number", "inspection", "inspection_date", "result", "inspector_id"]


def property_ids(x):
    rng = W.stream(22)
    props = [p for q in x["projects"] for p in q["props"]]
    ids = rng.choice(np.arange(10000, 100000), size=len(props), replace=False)
    for p, i in zip(props, ids):
        p["pid_ts"] = "TS-%05d" % int(i)


def project_rows(x):
    rows = []
    for q in x["projects"]:
        last = max(p["done"] for p in q["props"] if p["withdrawn"] is None) if any(
            p["withdrawn"] is None for p in q["props"]) else q["approved"]
        closeout = last + dt.timedelta(days=int(W.stream(23, int(q["number"][-4:]), int(q["trigger"])).integers(120, 300)))
        status = "Closed" if closeout <= W.AS_OF else "Open"
        live = [p for p in q["props"] if p["withdrawn"] is None]
        title = "%s %s, %s" % (W.NAME[q["lead"]], "elevations" if q["kind"] == "elevation" else "acquisitions",
                               W.EVENT_NAMES[[k for k, v in W.TRIGGERS.items() if v == q["trigger"]][0]])
        pop_end = q["approved"] + dt.timedelta(days=365 * 4)
        rows.append([q["number"], q["program"], W.DISASTER[q["trigger"]] if q["program"] == "HMGP" else "",
                     title, W.NAME[q["lead"]] + " County", status, q["approved"], pop_end, q["pct"], q["cost"],
                     q["share"], len(live)])
    return rows


def register_rows(x):
    """The properties as the export shows them: each status as of 30 September 2026, except that the properties of
    projects loaded from the old system keep the status they had when they were loaded."""
    props, insp = [], []
    rng = W.stream(24)
    for q in x["projects"]:
        for p in q["props"]:
            b = x["buildings"][p["bi"]]
            st, sd = W.prop_status(p, W.CUTOVER if q["migrated"] else W.AS_OF)
            props.append([q["number"], p["pid_ts"], address(b), b["community"], "Elevation" if p["kind"] == "elevation"
                          else "Acquisition", p["cost"], p["share_shown"], st, sd])
            if p["withdrawn"] is not None:
                continue
            start = p["done"] - dt.timedelta(days=270)
            if start - dt.timedelta(days=20) <= W.AS_OF:
                insp.append([p["pid_ts"], q["number"], "Pre-construction site visit",
                             start - dt.timedelta(days=int(rng.integers(8, 40))), "Pass",
                             "INSP-%02d" % int(rng.integers(1, 9))])
            if p["done"] <= W.AS_OF:
                if rng.random() < 0.12:
                    insp.append([p["pid_ts"], q["number"], "Final", p["done"] - dt.timedelta(days=int(rng.integers(18, 60))),
                                 "Fail", "INSP-%02d" % int(rng.integers(1, 9))])
                insp.append([p["pid_ts"], q["number"], "Final", p["done"], "Pass", "INSP-%02d" % int(rng.integers(1, 9))])
    props.sort(key=lambda r: (r[0], r[1]))
    insp.sort(key=lambda r: (r[3], r[0], r[2]))
    return props, insp


CROSS_COLS = ["property_id", "nfip_building_id", "match_method", "matched_date"]


def crosswalk_rows(x):
    rng = W.stream(25)
    rows = []
    for q in x["projects"]:
        for p in q["props"]:
            b = x["buildings"][p["bi"]]
            bid = b["pid"]
            if rng.random() < 0.06:
                bid = bid[:-1]           # matched before FEMA added the check letter
            m = "address" if rng.random() < 0.7 else ("parcel" if rng.random() < 0.7 else "manual")
            rows.append([p["pid_ts"], bid, m, q["approved"] - dt.timedelta(days=int(rng.integers(30, 200)))])
    rows.sort(key=lambda r: r[0])
    return rows


# ---------------------------------------------------------------------------------------------- lookups
OFFSET_COLS = ["county_fips", "county", "navd88_minus_ngvd29_ft", "method", "computed"]


def offset_rows():
    return [[f, W.NAME[f], "%.2f" % W.OFFSET[f], "NGS VERTCON 2.1 at the county's population centroid, to the nearest 0.1 foot",
             "2013-04-22"]
            for f in W.FIPS]


MEMBER_COLS = ["county_fips", "county", "member_since", "nfip_communities", "board_seat"]
JOINED = {"58003": "1987-07-01", "58007": "1983-01-01", "58011": "1987-07-01", "58015": "1983-01-01",
          "58019": "1983-01-01", "58023": "1991-10-01", "58027": "1983-01-01", "58031": "1983-01-01",
          "58035": "1996-07-01", "58039": "2004-01-01", "58043": "1991-10-01", "58047": "1983-01-01",
          "58051": "2004-01-01", "58055": "2009-07-01"}


def member_rows():
    return [[f, W.NAME[f], JOINED[f], ";".join(W.COMMUNITIES[f]), "District %d" % (i + 1)]
            for i, f in enumerate(W.FIPS)]


CRS_COLS = ["community_number", "community_name", "county_fips", "crs_class", "class_effective", "sfha_discount_pct",
            "non_sfha_discount_pct"]
DISCOUNT = {10: 0, 9: 5, 8: 10, 7: 15, 6: 20, 5: 25, 4: 30}


def crs_rows():
    rng = W.stream(26)
    rows = []
    for f in W.FIPS:
        for k, cno in enumerate(W.COMMUNITIES[f]):
            cls = int(rng.choice([5, 6, 6, 7, 7, 8, 8, 9, 10]))
            name = ("%s County (unincorporated)" % W.NAME[f]) if k == 0 else TOWNS[cno]
            eff = dt.date(int(rng.choice([2019, 2021, 2022, 2023, 2024, 2025])), int(rng.choice([4, 10])), 1)
            rows.append([cno, name, f, cls, eff, DISCOUNT[cls], 10 if cls <= 8 else (5 if cls == 9 else 0)])
    return rows


TOWNS = {"580113": "City of Hensby", "580205": "Town of Mossy Bend", "580211": "City of Dunholme",
         "580308": "City of Port Willet", "580415": "Town of Gorran Mills", "580509": "City of Menhaden Point",
         "580706": "City of Kettle Ford", "580811": "City of Amberjack", "581006": "Town of Thornock Springs",
         "581107": "City of Ravensholt", "581204": "City of Saltreach", "581405": "Town of Wickmere"}


FIRM_COLS = ["community_number", "county_fips", "map_action", "effective_date", "case_number", "panels", "description"]


def firm_rows():
    rng = W.stream(27)
    rows = []
    for f in W.FIPS:
        for cno in W.COMMUNITIES[f]:
            for y in (2007, 2013, 2019) if W.KIND[f] == "coast" else (2009, 2014, 2021):
                if rng.random() < 0.55:
                    eff = dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                    rows.append([cno, f, "FIRM revision", eff, "%02d-06-%04dS" % (y % 100 - 2, int(rng.integers(100, 9999))),
                                 int(rng.integers(3, 22)), "Countywide revision; flood elevations restudied on %s"
                                 % ("the open coast and the bay" if W.KIND[f] == "coast" else "the Tarrow River and tributaries")])
            for _ in range(int(rng.integers(1, 5))):
                y = int(rng.integers(2002, 2026))
                eff = dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                rows.append([cno, f, "LOMR", eff, "%02d-06-%04dP" % (y % 100, int(rng.integers(100, 9999))),
                             int(rng.integers(1, 3)), "Letter of Map Revision, %s" % (
                                 "fill and grading of a subdivision" if rng.random() < 0.5 else "a drainage channel improvement")])
    rows.sort(key=lambda r: (r[3], r[0]))
    return rows


def write_xlsx(path, sheets):
    """sheets: [(title, cols, rows, date_cols, money_cols)]"""
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    first = True
    for title, cols, rows, date_cols, money_cols in sheets:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title
        ws.append(cols)
        for cell in ws[1]:
            cell.font = Font(bold=True)
        for r in rows:
            ws.append([None if v == "" else v for v in r])
        for j in date_cols:
            for row in ws.iter_rows(min_row=2, min_col=j + 1, max_col=j + 1):
                for cell in row:
                    cell.number_format = "yyyy-mm-dd"
        for j in money_cols:
            for row in ws.iter_rows(min_row=2, min_col=j + 1, max_col=j + 1):
                for cell in row:
                    cell.number_format = "#,##0"
        for k, col in enumerate(cols):
            ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = max(11, min(34, len(col) + 3))
        ws.freeze_panes = "A2"
    wb.save(path)
    return sum(len(s[2]) for s in sheets)
