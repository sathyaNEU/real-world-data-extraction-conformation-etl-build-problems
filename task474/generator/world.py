"""task474's world: an unnamed New England state whose eight former counties gave way to nine planning regions as
county-equivalents, its towns, the residents in poverty in each town by year (the clean truth, before any source
measures it), and the events that moved them.

Everything the pack ships is measured from this truth by the source that would measure it: the State Data Center's
model estimates (former counties to 2022, planning regions from 2023), the Bureau's 2020-2024 five-year town tables,
the Department of Social Services' monthly SNAP counts by town, the State's population estimates, and the Fund's FY2026
client records. Seeds are fixed per stream so two builds are byte-identical."""
import math

import numpy as np

STATE_FIPS = "52"
YEARS = list(range(2015, 2027))
LEGACY_YEARS = (2020, 2021, 2022)       # the State Data Center's estimates for the former counties only
NATIVE_YEARS = (2023, 2024)             # its estimates for the planning regions
WINDOW = (2020, 2024)                   # the Bureau's five-year release the pack carries
FUND = 12_000_000

SDC = "State Data Center"
OBP = "Office of Budget and Policy"
DSS = "Department of Social Services"
BUREAU = "U.S. Census Bureau"
FUND_NAME = "Regional Opportunity Fund"
PEOPLE = {"director": "Wendy Taylor", "demographer": "Martin Estrada", "grants": "Paige Hodges"}

# the former counties (statistical areas only since the 1960s) and their FIPS codes
COUNTIES = [("001", "Halden"), ("003", "Corbin"), ("005", "Wexmoor"), ("007", "Ashgrove"), ("009", "Ludbury"),
            ("011", "Merrick"), ("013", "Stanbridge"), ("015", "Pennock")]
# the planning regions, the county-equivalents from the 2022 statute, and their councils
REGIONS = [("110", "Greater Ormsby"), ("120", "Mill River Valley"), ("130", "Tarrow Uplands"),
           ("140", "Southern Shore"), ("150", "Wexport Harbor"), ("160", "Two Rivers"),
           ("170", "Northern Hills"), ("180", "Quinnet Valley"), ("190", "Eastern Bays")]
COUNCIL = {r: "%s Council of Governments" % r for _, r in REGIONS}
AGENCY = {"Halden": "Halden County Community Action Agency", "Corbin": "Corbin Community Action",
          "Wexmoor": "Wexmoor Opportunity Council", "Ashgrove": "Ashgrove Community Services",
          "Ludbury": "Ludbury County Action Partnership", "Merrick": "Merrick Community Action",
          "Stanbridge": "Stanbridge Area Community Action", "Pennock": "Pennock County Action Council"}

# the pieces where a former county meets a region: (county, region, kind of the towns, [town names]);
# the first name of a piece whose kind is "city" is the city
PIECES = [
    ("Halden", "Greater Ormsby", "city", ["Ormsby", "East Ormsby", "Harrowgate", "Lindbrook", "Pemleigh",
                                          "Cobdale", "Brackbrook", "Wendhurst"]),
    ("Halden", "Mill River Valley", "inner", ["Fenbrook", "Tilcombe", "Carrholt", "Ashcote", "Draywick",
                                              "Northcote", "Larhurst"]),
    ("Halden", "Tarrow Uplands", "rural", ["Tarrcote", "Whitholt", "Garbury", "Halridge"]),
    ("Corbin", "Mill River Valley", "city", ["Corwin", "West Corwin", "Sedridge", "Larbrook", "Ebbrook"]),
    ("Corbin", "Southern Shore", "outer", ["Cranmouth", "Belmouth", "Rookstow", "Oakmouth", "Garmouth",
                                           "Pettridge", "Shelcote", "Garnet Neck"]),
    ("Wexmoor", "Wexport Harbor", "city", ["Wexport", "North Wexport", "Saxstead", "Morbrook", "Haskford",
                                           "Kelstead"]),
    ("Wexmoor", "Southern Shore", "inner", ["Marlridge", "Ketmere", "Radstow", "Belstead", "Tibhurst"]),
    ("Wexmoor", "Two Rivers", "inner", ["Ferrholt", "Gledbrook", "Quarstead", "Lydcote"]),
    ("Ashgrove", "Two Rivers", "city", ["Ravelston", "Ashmere", "Dunstead", "Culstow", "Birchford", "Ellstow",
                                        "Mottholt", "Paskden", "Vanecote"]),
    ("Ashgrove", "Northern Hills", "rural", ["Gormbury", "Holwick", "Normore", "Wyncombe", "Silcote", "Yarholt"]),
    ("Ludbury", "Northern Hills", "rural", ["Ullsmore", "Thornwell", "Bramleigh", "Havcote", "Remstead",
                                            "Wynmore", "Ketcombe", "Upper Draybury", "Lydmere", "Foxholt"]),
    ("Ludbury", "Tarrow Uplands", "rural", ["Draybury", "Dunwell", "Gledridge", "Quarbrook", "Radcombe",
                                            "Sedhurst", "Stanholt", "Wexbrook", "Yarcote"]),
    ("Merrick", "Quinnet Valley", "city", ["Quinnet", "Pemhurst", "Oakholt", "Ebdale", "Halleigh", "Rushden",
                                           "Morstow", "Thornbrook"]),
    ("Merrick", "Wexport Harbor", "inner", ["Belden", "Cranstead", "Lower Saxstead", "Whitridge", "Gormfield"]),
    ("Stanbridge", "Quinnet Valley", "outer", ["Birchwell", "Culdale", "Ferrcombe", "Vanehurst", "Wendcombe",
                                               "Pettcote"]),
    ("Stanbridge", "Eastern Bays", "city", ["Saltmarsh", "Bexton", "Kelmouth", "Normere", "Sheldale",
                                           "Tilney", "Wickbrook", "Yarford"]),
    ("Pennock", "Eastern Bays", "rural", ["Pennock Center", "Carrhurst", "Dellford", "Foxbury", "Larkspur Hill",
                                          "Mottcote", "Quarley", "Rushwick", "Silham", "Ullsham"]),
]

# dated events that moved residents in poverty between towns (the world's own history, visible in the counts)
EVENT_ORMSBY_COURTS = dict(name="Bellmont Courts", city="Ormsby", year=2021,
                           receivers={"Fenbrook": 0.34, "Tilcombe": 0.27, "Carrholt": 0.22, "Draywick": 0.17},
                           people=4300, start_month=4, end_month=12)        # April to December 2021
EVENT_SHORE_HOUSING = dict(name="Marlridge Commons", from_town="Wexport", to_town="Marlridge", year=2021,
                           people=1450, start_month=6, end_month=14)        # June 2021 to February 2022
EVENT_RAVELSTON_PLANT = dict(town="Dunstead", year=2021, people=950)        # a mill's closure in March 2021


SALT = {"sdc": 4, "acs": 7, "asks": 0, "balances": 0}    # fixed by the salt search (tune.py)


def rng(stream):
    """One generator per named stream, so adding a stream never moves another's draws."""
    import hashlib
    seed = int(hashlib.sha256(("task474/" + stream + "/" + str(SALT.get(stream, 0))).encode()).hexdigest()[:12], 16)
    return np.random.default_rng(seed)


def county_code(name):
    return dict((n, c) for c, n in COUNTIES)[name]


def region_code(name):
    return dict((n, c) for c, n in REGIONS)[name]


def build_towns():
    """The towns with their fixed attributes. Population is the 2020 census count; the poverty base is the
    residents in poverty in 2022 (the truth before events); g is the town's own yearly drift as a share of it."""
    r = rng("towns")
    towns = []
    sub_code = 1000
    for county, region, kind, names in PIECES:
        for i, name in enumerate(names):
            city = (kind == "city" and i == 0)
            tk = "city" if city else ("inner" if kind == "city" else kind)
            if city:
                pop = {"Ormsby": 121_480, "Corwin": 71_305, "Wexport": 136_922, "Ravelston": 48_617,
                       "Quinnet": 63_154, "Saltmarsh": 52_390}[name]
                rate = r.uniform(0.215, 0.268)
                g = {"Ormsby": -0.014, "Corwin": -0.006, "Wexport": -0.016, "Ravelston": -0.004,
                     "Quinnet": -0.019, "Saltmarsh": -0.008}[name]
            else:
                med = {"inner": 14_500, "outer": 9_200, "rural": 4_700}[tk]
                pop = float(np.exp(r.normal(math.log(med), 0.52)))
                pop = max(pop, 780.0)
                rate = {"inner": r.uniform(0.075, 0.138), "outer": r.uniform(0.046, 0.088),
                        "rural": r.uniform(0.052, 0.104)}[tk]
                g = {"inner": r.uniform(0.012, 0.034), "outer": r.uniform(-0.002, 0.014),
                     "rural": r.uniform(-0.011, 0.010)}[tk]
            # SNAP take-up among residents in poverty, the household size of a SNAP case, and the age mix of the poor
            take = {"city": r.uniform(0.80, 0.88), "inner": r.uniform(0.58, 0.69), "outer": r.uniform(0.47, 0.56),
                    "rural": r.uniform(0.39, 0.50)}[tk]
            if county == "Halden" and region == "Greater Ormsby" and not city:
                take = r.uniform(0.74, 0.80)          # the older inner ring around the capital
            hh = {"city": r.uniform(1.86, 2.02), "inner": r.uniform(2.02, 2.24), "outer": r.uniform(2.10, 2.32),
                  "rural": r.uniform(1.98, 2.20)}[tk]
            kids = {"city": r.uniform(0.33, 0.39), "inner": r.uniform(0.28, 0.36), "outer": r.uniform(0.22, 0.30),
                    "rural": r.uniform(0.20, 0.28)}[tk]
            old = {"city": r.uniform(0.09, 0.13), "inner": r.uniform(0.10, 0.16), "outer": r.uniform(0.14, 0.21),
                   "rural": r.uniform(0.16, 0.24)}[tk]
            growth = {"city": r.uniform(-0.002, 0.004), "inner": r.uniform(0.003, 0.009),
                      "outer": r.uniform(0.000, 0.006), "rural": r.uniform(-0.004, 0.003)}[tk]
            sub_code += int(r.integers(180, 760))
            towns.append(dict(name=name, county=county, region=region, kind=tk, pop2020=int(round(pop)),
                              poor22=pop * rate, g=g, take=take, hh=hh, kids=kids, old=old, growth=growth,
                              cousub="%05d" % sub_code))
    return towns


def poor_truth(towns):
    """Residents in poverty by town and calendar year (the yearly average stock), and by month for the series that
    are monthly. Linear drift, a small persistent wobble, and the three dated events."""
    r = rng("poor")
    for t in towns:
        wob = 0.0
        t["poor"] = {}
        for y in YEARS:
            wob = 0.6 * wob + r.normal(0, 0.006)
            t["poor"][y] = t["poor22"] * (1 + t["g"] * (y - 2022)) * (1 + wob)
    by = {t["name"]: t for t in towns}

    def monthly_done(ev, y, m):
        k = (y - ev["year"]) * 12 + m                  # month number counted from January of the event year
        if k < ev["start_month"]:
            return 0.0
        if k >= ev["end_month"]:
            return 1.0
        return (k - ev["start_month"] + 1) / (ev["end_month"] - ev["start_month"] + 1)

    # monthly truth: the year's stock interpolated within the year, then the events at their own months
    for t in towns:
        t["poor_m"] = {}
        for y in YEARS:
            nxt = t["poor"].get(y + 1, t["poor"][y])
            prv = t["poor"].get(y - 1, t["poor"][y])
            for m in range(1, 13):
                # centre each year's stock on its middle; a gentle within-year slope toward the neighbours
                f = (m - 6.5) / 12.0
                base = t["poor"][y] + (f * (nxt - prv) / 2.0)
                t["poor_m"][(y, m)] = base
    ev = EVENT_ORMSBY_COURTS
    for y in YEARS:
        for m in range(1, 13):
            d = monthly_done(ev, y, m) * ev["people"]
            by[ev["city"]]["poor_m"][(y, m)] -= d
            for town, share in ev["receivers"].items():
                by[town]["poor_m"][(y, m)] += d * share
    ev = EVENT_SHORE_HOUSING
    for y in YEARS:
        for m in range(1, 13):
            d = monthly_done(ev, y, m) * ev["people"]
            by[ev["from_town"]]["poor_m"][(y, m)] -= d
            by[ev["to_town"]]["poor_m"][(y, m)] += d
    ev = EVENT_RAVELSTON_PLANT
    for y in YEARS:
        for m in range(1, 13):
            k = (y - ev["year"]) * 12 + m
            ramp = 0.0 if k < 3 else min(1.0, (k - 2) / 10.0)
            by[ev["town"]]["poor_m"][(y, m)] += ramp * ev["people"]
    # the calendar-year stock is the mean of the twelve months
    for t in towns:
        for y in YEARS:
            t["poor"][y] = float(np.mean([t["poor_m"][(y, m)] for m in range(1, 13)]))
    return towns


def population(towns):
    """Residents by town and year (the State's estimates' truth): the 2020 census count grown at the town's rate,
    with the events' movers carried along with the poor they moved."""
    for t in towns:
        t["popy"] = {y: t["pop2020"] * (1 + t["growth"]) ** (y - 2020) for y in YEARS}
    by = {t["name"]: t for t in towns}
    for ev in (EVENT_ORMSBY_COURTS, EVENT_SHORE_HOUSING):
        frm = ev.get("city") or ev.get("from_town")
        to = ev.get("receivers") or {ev["to_town"]: 1.0}
        for y in YEARS:
            done = 0.0 if y < ev["year"] else (0.45 if y == ev["year"] else 1.0)
            moved = done * ev["people"] * 1.18           # households move with members above the line too
            by[frm]["popy"][y] -= moved
            for town, share in to.items():
                by[town]["popy"][y] += moved * share
    return towns


def world():
    towns = poor_truth(build_towns())
    towns = population(towns)
    return towns


TOWNS = world()
COUNTY_NAMES = [n for _, n in COUNTIES]
REGION_NAMES = [n for _, n in REGIONS]


def by_name():
    return {t["name"]: t for t in TOWNS}


# the pack, by role
FILES = {
    "rel2021": "sdc_poverty_estimates_dec2021.pdf",
    "rel2022": "sdc_poverty_estimates_dec2022.pdf",
    "rel2023": "sdc_poverty_estimates_dec2023.pdf",
    "rel2024": "sdc_poverty_estimates_dec2024_transition.pdf",
    "rel2025": "sdc_poverty_estimates_2024_planning_regions.xlsx",
    "methods": "sdc_poverty_estimates_methods_note.pdf",
    "acs": "acs5_2020_2024_b17001_towns_regions.csv",
    "acs_notes": "acs5_2020_2024_b17001_table_notes.txt",
    "snap": "dss_snap_participation_by_town_2019_2026.txt",
    "codes": "town_county_region_codes.csv",
    "rule": "obp_rof_fy2027_allocation_rule.pdf",
    "fy2026": "rof_fy2026_allocation_table.xlsx",
    "factors": "county_to_planning_region_factors_2020.csv",
    "closeout": "rof_fy2026_closeout.xlsx",
    "extract": "rof_client_services_extract_20260930.csv",
    "audit": "rof_gds_profile_audit_fy2026.csv",
    "conversion": "cca_client_number_conversion_20260101.csv",
    "layout": "rof_gds_export_layout.txt",
}
DISTRACTORS = ("fy2026", "factors")
DELIVERABLES = ("rof_fy2027_region_poverty.csv", "rof_fy2027_allocation_memo.docx")
