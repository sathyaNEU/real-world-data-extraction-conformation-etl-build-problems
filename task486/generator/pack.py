"""task486 pack writers for the delimited files: the release's tables as the planning analyst pulled them, the county's
provider-area assignment and address points, the American Community Survey table, and the agency's and the state's
service records."""
import csv
import datetime as dt
import io

import numpy as np

import asks as A
import world as W

FILES = {
    "blocks": "dhc2020_kelvane_blocks_sex_by_age.csv",
    "bgs": "dhc2020_kelvane_block_groups_p12.csv",
    "tracts": "dhc2020_kelvane_county_tracts_p12.csv",
    "hu": "dhc2020_kelvane_blocks_h1.csv",
    "colmeta": "dhc2020_p12_h1_column_metadata.csv",
    "notes": "dhc2020_notes_for_local_users.pdf",
    "assign": "provider_area_blocks.csv",
    "points": "kelvane_address_points_2026-10-02.csv",
    "acs": "acs2022_5yr_kelvane_block_groups_b01001.csv",
    "instructions": "fy2027_area_plan_update_instructions.pdf",
    "policy": "kaaa_provider_allocation_policy_2023.docx",
    "facilities": "licensed_residential_care_kelvane.xlsx",
    "providers": "kaaa_provider_directory.xlsx",
    "roster": "hdm_client_roster_2026-10-09.csv",
    "episodes": "hdm_service_episodes_2026-10-09.csv",
    "log": "hdm_route_delivery_log_fy2026.csv",
    "items": "hdm_item_codes.csv",
    "deaths": "state_death_match_runs_2025-07_to_2026-10.csv",
    "links": "state_registry_number_links.csv",
    "inventory": "kaaa_data_inventory.csv",
    "guide": "kaaa_field_guide.txt",
}


BLOCK_COLS = ["block_geoid", "sex", "age_group", "count"]
COLMETA_COLS = ["Column Name", "Label"]
ASSIGN_COLS = ["TRACT_BLOCK", "PROV_AREA", "PROV_CODE", "EFFECTIVE_FROM", "EFFECTIVE_TO"]
POINTS_COLS = ["ADDRESS_ID", "ADDRESS", "UNIT", "BLOCK_GEOID20", "USE", "STATUS", "ADDED", "RETIRED"]
ROSTER_COLS = ["client_id", "state_participant_id", "birth_year", "home_block", "meals_per_day", "schedule"]
EPISODE_COLS = ["episode_id", "client_id", "service", "provider_code", "enrolled", "closed", "close_reason"]
LOG_COLS = ["delivery_id", "tablet_id", "route_id", "provider_code", "client_id", "delivery_date", "item_code",
            "uploaded_at"]
ITEM_COLS = ["item_code", "description", "meals"]
DEATH_COLS = ["run_date", "state_participant_id", "date_of_death", "match_basis"]
LINK_COLS = ["prior_participant_id", "current_participant_id", "linked_on", "reason"]
ROSTER_FROM = dt.date(2024, 10, 1)      # the roster holds clients served since FY2025 began


def served(b):
    """Client ids with an episode open on or after 1 October 2024."""
    return {e["client_id"] for e in b.episodes if e["closed"] is None or e["closed"] >= ROSTER_FROM}


def write_csv(path, cols, rows, lineterminator="\r\n", extra_header=None):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=lineterminator)
    w.writerow(cols)
    if extra_header:
        w.writerow(extra_header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


# ---------------------------------------------------------------- geography names
def geoid_block(b):
    return W.STATE_FIPS + W.COUNTY_FIPS + b["tract"] + b["block"]


def geoid_bg(g):
    return W.STATE_FIPS + W.COUNTY_FIPS + g


def tract_name(t):
    n = int(t[:4])
    s = t[4:]
    return "%d.%s" % (n, s) if s != "00" else "%d" % n


def p12_labels():
    labs = [" !!Total:", " !!Total:!!Male:"]
    labs += [" !!Total:!!Male:!!%s" % a for a in W.AGE_GROUPS]
    labs += [" !!Total:!!Female:"]
    labs += [" !!Total:!!Female:!!%s" % a for a in W.AGE_GROUPS]
    return labs


P12_CODES = ["P12_%03dN" % k for k in range(1, 50)]


def p12_row(cells):
    m, f = cells[:23], cells[23:]
    return [int(cells.sum()), int(m.sum())] + [int(x) for x in m] + [int(f.sum())] + [int(x) for x in f]


# ---------------------------------------------------------------- the release
def blocks_long(b):
    rows = []
    pub = b.rel["block"]
    order = sorted(range(len(b.blocks)), key=lambda i: geoid_block(b.blocks[i]))
    for i in order:
        g = geoid_block(b.blocks[i])
        for s, sex in enumerate(W.SEXES):
            for a, lab in enumerate(W.AGE_GROUPS):
                rows.append((g, sex, lab, int(pub[i][s * 23 + a])))
    return rows


def bg_rows(b):
    out = []
    for g in sorted(b.rel["block_group"]):
        cells = b.rel["block_group"][g]
        name = "Block Group %s; Census Tract %s; Kelvane County" % (g[-1], tract_name(g[:6]))
        out.append(["1500000US" + geoid_bg(g), name] + p12_row(cells))
    return out


def tract_rows(b):
    out = [["0500000US" + W.STATE_FIPS + W.COUNTY_FIPS, "Kelvane County"] + p12_row(b.rel["county"])]
    for t in sorted(b.rel["tract"]):
        out.append(["1400000US" + W.STATE_FIPS + W.COUNTY_FIPS + t, "Census Tract %s; Kelvane County" % tract_name(t)]
                   + p12_row(b.rel["tract"][t]))
    return out


def hu_rows(b):
    out = []
    for i in sorted(range(len(b.blocks)), key=lambda i: geoid_block(b.blocks[i])):
        bl = b.blocks[i]
        name = "Block %s; Block Group %s; Census Tract %s; Kelvane County" % (
            bl["block"], bl["block"][0], tract_name(bl["tract"]))
        out.append(["1000000US" + geoid_block(bl), name, bl["hu"]])
    return out


def colmeta_rows():
    rows = [("GEO_ID", "Geography"), ("NAME", "Geographic Area Name")]
    rows += [(c, l) for c, l in zip(P12_CODES, p12_labels())]
    rows += [("H1_001N", " !!Total")]
    return rows


# ---------------------------------------------------------------- the county's files
def assign_rows(b):
    """The county GIS export: TRACT_BLOCK is tract and block as one number (leading zeros dropped), one row per block
    and assignment; blocks the 2023 redraw moved carry their earlier row too."""
    rows = []
    for i in sorted(range(len(b.blocks)), key=lambda i: geoid_block(b.blocks[i])):
        bl = b.blocks[i]
        tb = int(bl["tract"] + bl["block"])
        old = b.old_area[i]
        if old != bl["area"]:
            rows.append((tb, old, A.CODE[old], "2016-07-01", "2023-06-30"))
            rows.append((tb, bl["area"], A.CODE[bl["area"]], "2023-07-01", ""))
        else:
            rows.append((tb, bl["area"], A.CODE[bl["area"]], "2016-07-01", ""))
    return rows


STREETS = ["Main St", "Oak St", "Maple Ave", "Cedar St", "Elm St", "Church St", "Mill Rd", "Park Ave", "High St",
           "Walnut St", "School St", "Pine St", "Spring St", "Ridge Rd", "Lake Rd", "Hill St", "Water St",
           "Chestnut St", "Center St", "North St", "Union St", "Prospect Ave", "Locust St", "Cherry Ln",
           "Orchard Rd", "Meadow Ln", "River Rd", "Valley Rd", "Forest Ave", "Grove St", "Highland Ave",
           "Summit Ave", "Franklin St", "Jackson St", "Washington St", "Lincoln Ave", "Railroad Ave", "Depot St",
           "Quarry Rd", "County Rd 12", "County Rd 18", "County Rd 31", "Ring Rd", "Sawmill Rd", "Creamery Rd",
           "Bridge St", "Canal St", "Fairview Ave", "Sunset Dr", "Willow Ln"]


def points_rows(b, seed):
    """The county's address points as of 2 October 2026: every residential unit address, the census-day stock and the
    units added since, a few retired."""
    rng = np.random.default_rng(seed * 59 + 13)
    rows = []
    aid = iter(range(3100001, 3999999, 3))
    for i in sorted(range(len(b.blocks)), key=lambda i: geoid_block(b.blocks[i])):
        bl = b.blocks[i]
        new = b.points[i] - bl["hu"]
        if bl["hu"] == 0 and new == 0:
            continue
        street = STREETS[int(rng.integers(0, len(STREETS)))]
        num = int(rng.integers(1, 90)) * 10
        apts = bl["hu"] >= 24 and rng.random() < 0.5
        for u in range(bl["hu"]):
            added = dt.date(2004, 1, 1) + dt.timedelta(days=int(rng.integers(0, 5800)))
            if added > dt.date(2020, 3, 31):
                added = dt.date(2020, 3, 31) - dt.timedelta(days=int(rng.integers(0, 3000)))
            unit = ("APT %d" % (u + 1)) if apts else ""
            n = num if apts else num + 2 * u
            rows.append(("AP%07d" % next(aid), "%d %s" % (n, street), unit, geoid_block(bl), "Residential", "Active",
                         added.isoformat(), ""))
        for u in range(new):
            added = dt.date(2020, 9, 1) + dt.timedelta(days=int(rng.integers(0, 2180)))
            rows.append(("AP%07d" % next(aid), "%d %s" % (num + 2 * (bl["hu"] + u) + 400, street), "",
                         geoid_block(bl), "Residential", "Active", added.isoformat(), ""))
        if bl["hu"] > 6 and rng.random() < 0.04:       # a demolished unit, retired after census day
            k = len(rows) - new - 1
            r = list(rows[k])
            r[5], r[7] = "Retired", (dt.date(2021, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1900)))).isoformat()
            rows[k] = tuple(r)
    return rows


def acs_rows(b, seed):
    """The 2018-2022 five-year American Community Survey's sex by age (B01001) for block groups: estimates with their
    margins of error, a five-year period average with its own sampling error."""
    rng = np.random.default_rng(seed * 61 + 17)
    out = []
    for g in sorted(b.rel["block_group"]):
        idx = [i for i, bl in enumerate(b.blocks) if bl["bg"] == g]
        truth = sum(b.blocks[i]["cells"] for i in idx).astype(float)
        drift = rng.uniform(0.94, 1.07)
        est = np.maximum(0, np.rint(truth * drift + rng.normal(0, np.sqrt(truth + 4) * 1.6))).astype(int)
        moe = np.rint(1.645 * np.sqrt(truth + 9) * 1.6 + 8).astype(int)
        row = ["1500000US" + geoid_bg(g), "Block Group %s; Census Tract %s; Kelvane County" % (g[-1], tract_name(g[:6]))]
        e = p12_row(est)
        m = [int(np.rint(np.sqrt((moe ** 2).sum())))] + [int(np.rint(np.sqrt((moe[:23] ** 2).sum())))] + \
            [int(x) for x in moe[:23]] + [int(np.rint(np.sqrt((moe[23:] ** 2).sum())))] + [int(x) for x in moe[23:]]
        for a, mm in zip(e, m):
            row += [a, mm]
        out.append(row)
    return out


def acs_header():
    cols, labs = ["GEO_ID", "NAME"], ["Geography", "Geographic Area Name"]
    lab = ["Total:", "Total:!!Male:"] + ["Total:!!Male:!!%s" % a for a in W.AGE_GROUPS] + ["Total:!!Female:"] + \
          ["Total:!!Female:!!%s" % a for a in W.AGE_GROUPS]
    for k, l in enumerate(lab, 1):
        cols += ["B01001_%03dE" % k, "B01001_%03dM" % k]
        labs += ["Estimate!!" + l, "Margin of Error!!" + l]
    return cols, labs


# ---------------------------------------------------------------- the agency's and the state's records
def roster_rows(b):
    rows = []
    keep = served(b)
    for c in sorted(b.clients, key=lambda c: c["client_id"]):
        if c["client_id"] not in keep:
            continue
        e = [x for x in b.episodes if x["client_id"] == c["client_id"]][0]
        rows.append((c["client_id"], c["state_id"], c["birth_year"], geoid_block(b.blocks[c["block"]]),
                     c["plan"], e["schedule"]))
    return rows


def episode_rows(b, seed):
    """One row per home-delivered meal episode; a client re-registered after a lapse has the earlier episode too."""
    rng = np.random.default_rng(seed * 67 + 19)
    rows = []
    prior = {c["client_id"]: c["prior_id"] for c in b.clients}
    home = {c["client_id"]: c["block"] for c in b.clients}
    eid = iter(range(500001, 999999, 7))
    keep = served(b)
    for e in sorted(b.episodes, key=lambda e: (e["client_id"], e["enrolled"])):
        if e["client_id"] not in keep:
            continue
        if prior.get(e["client_id"]):
            first_provider = A.CODE[b.old_area[home[e["client_id"]]]]
            start = dt.date(2016, 9, 1) + dt.timedelta(days=int(rng.integers(0, 1500)))
            stop = min(start + dt.timedelta(days=int(rng.integers(120, 900))), e["enrolled"] - dt.timedelta(days=400))
            if stop > start:
                rows.append(("EP%06d" % next(eid), e["client_id"], "HDM", first_provider, start.isoformat(),
                             stop.isoformat(), str(rng.choice(["Declined service", "Moved in with family",
                                                               "Short-term need ended"]))))
        rows.append(("EP%06d" % next(eid), e["client_id"], "HDM", e["provider"], e["enrolled"].isoformat(),
                     e["closed"].isoformat() if e["closed"] else "", e["reason"]))
    return rows


def log_rows(b):
    rows = []
    for r in sorted(b.deliveries, key=lambda r: r["delivery_id"]):
        rows.append((r["delivery_id"], r["tablet"], r["route"], r["provider_code"], r["client_id"],
                     r["date"].isoformat(), r["item"], r["uploaded_at"].strftime("%Y-%m-%d %H:%M:%S")))
    return rows


def item_rows():
    return [("HOT", "Hot meal: entree, two sides, bread, milk", 1),
            ("FRZ2", "Weekend frozen pack: two meals", 2),
            ("FRZ7", "Weekly frozen pack: seven meals", 7),
            ("SHS3", "Shelf-stable emergency pack: three meals", 3)]


def death_rows(b, seed):
    rng = np.random.default_rng(seed * 71 + 23)
    rows = []
    for d in b.deaths:
        basis = "SSN, name, date of birth" if rng.random() < 0.82 else "Name, date of birth, county"
        rows.append((d["match_run"].isoformat(), d["state_id"], d["date_of_death"].isoformat(), basis))
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def link_rows(b, seed):
    """The registry's number links, statewide: every number retired when a participant registered again."""
    rng = np.random.default_rng(seed * 73 + 29)
    rows = [(l["prior_id"], l["current_id"], l["linked_on"].isoformat(), "Registered again after a lapse")
            for l in b.links]
    sid = iter(range(4000009, 4999999, 13))
    while len(rows) < len(b.links) + 2860:
        p, c = "SP%07d" % next(sid), "SP%07d" % next(sid)
        if p in b.taken or c in b.taken:
            continue
        d = dt.date(2015, 3, 1) + dt.timedelta(days=int(rng.integers(0, 4200)))
        why = "Registered again after a lapse" if rng.random() < 0.86 else "Duplicate registration merged"
        rows.append((p, c, d.isoformat(), why))
    rows.sort(key=lambda r: (r[2], r[0]))
    return rows
