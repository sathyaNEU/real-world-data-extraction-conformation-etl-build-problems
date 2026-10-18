"""Shared constants for task268: Larderline's 2027 weekday dark-store pilot, six candidate metros and their cores."""
import datetime as dt

ORG = "Larderline"
HOME_METRO = "Trenstead"
PEOPLE = {"vp": "Megan Swanson", "analytics": "Carolyn Cook"}

BOARD_DATE = dt.date(2026, 9, 17)          # the board paper that sets the rule
BOARD_MEETING = dt.date(2026, 12, 9)       # the meeting that picks the pilot
PACK_DATE = dt.date(2026, 10, 6)           # the location analytics team's data pack
LISTINGS_DATE = dt.date(2026, 10, 1)       # the listing service's export
AS_OF = dt.date(2026, 9, 30)               # the date the asks are taken at
PILOT_YEAR = 2027
CLAUSE = {"pick": "4.1", "density": "4.2", "present": "4.3", "latest": "4.4"}   # board paper BD-2026-41, section 4
OD_YEAR = 2022
ACS_YEARS = "2018-2022"

# the commuting table's three industry groups, as the agency codes them, and the NAICS sectors in each
GROUPS = ["SI01", "SI02", "SI03"]
GROUP_NAME = {"SI01": "Goods Producing", "SI02": "Trade, Transportation, and Utilities", "SI03": "All Other Services"}
SECTORS = [  # code as the survey writes it, title, group
    ("11", "Agriculture, Forestry, Fishing and Hunting", "SI01"),
    ("21", "Mining, Quarrying, and Oil and Gas Extraction", "SI01"),
    ("22", "Utilities", "SI02"),
    ("23", "Construction", "SI01"),
    ("31-33", "Manufacturing", "SI01"),
    ("42", "Wholesale Trade", "SI02"),
    ("44-45", "Retail Trade", "SI02"),
    ("48-49", "Transportation and Warehousing", "SI02"),
    ("51", "Information", "SI03"),
    ("52", "Finance and Insurance", "SI03"),
    ("53", "Real Estate and Rental and Leasing", "SI03"),
    ("54", "Professional, Scientific, and Technical Services", "SI03"),
    ("55", "Management of Companies and Enterprises", "SI03"),
    ("56", "Administrative and Support and Waste Management and Remediation Services", "SI03"),
    ("61", "Educational Services", "SI03"),
    ("62", "Health Care and Social Assistance", "SI03"),
    ("71", "Arts, Entertainment, and Recreation", "SI03"),
    ("72", "Accommodation and Food Services", "SI03"),
    ("81", "Other Services (except Public Administration)", "SI03"),
    ("92", "Public Administration", "SI03"),
]
SECTOR_GROUP = {s[0]: s[2] for s in SECTORS}
RINGS = ["C", "O", "X"]   # the worker's home: the workplace metro's central county, an outlying county of it, outside it

# the six candidates: metro, state, central county, outlying counties, in-state counties outside the metro that
# send workers to it (with the other metropolitan or micropolitan area each sits in, if any)
STATES = {"OH": ("39", "Ohio"), "IN": ("18", "Indiana"), "NC": ("37", "North Carolina"), "CO": ("08", "Colorado"),
          "MO": ("29", "Missouri"), "TN": ("47", "Tennessee")}
METROS = [
    dict(name="Halberdine", st="OH", cbsa="25230", central=("Corvemere", "212"),
         outlying=[("Abberholt", "226"), ("Stanwick", "238"), ("Quenness", "244")],
         outside=[("Calgarth", "252", ("16970", "Calgarth", "Micropolitan")), ("Moxcote", "264", None)]),
    dict(name="Quillmere", st="IN", cbsa="39370", central=("Elverstead", "206"),
         outlying=[("Haskcote", "218"), ("Trengarth", "232")],
         outside=[("Trenmere", "246", ("45570", "Trenmere", "Micropolitan")), ("Orrmere", "258", None)]),
    dict(name="Corrisford", st="NC", cbsa="18770", central=("Brackholt", "214"),
         outlying=[("Carraham", "228"), ("Ottlewood", "236"), ("Pelholt", "248")],
         outside=[("Kerstead", "256", ("28530", "Kerstead", "Micropolitan")), ("Merholt", "268", None)]),
    dict(name="Tessavon", st="CO", cbsa="45190", central=("Denevale", "202"),
         outlying=[("Rosgarth", "216"), ("Ivorstead", "234")],
         outside=[("Garholt", "242", ("23850", "Garholt", "Micropolitan")), ("Yarcote", "254", None)]),
    dict(name="Ashcombe", st="MO", cbsa="11670", central=("Gilderbury", "208"),
         outlying=[("Barralin", "222"), ("Norstead", "234"), ("Larrvale", "246")],
         outside=[("Branrick", "258", ("14490", "Branrick", "Micropolitan")), ("Ravcote", "266", None)]),
    dict(name="Dunnaway", st="TN", cbsa="20390", central=("Lydshaw", "204"),
         outlying=[("Quarrbury", "224"), ("Falgarth", "238")],
         outside=[("Velholt", "252", ("46330", "Velholt", "Micropolitan")), ("Dormere", "262", None)]),
]
METRO_NAMES = [m["name"] for m in METROS]

FILES = {
    "od_main": "commuting_od_tract_2022_main.csv",
    "od_aux": "commuting_od_tract_2022_aux.csv",
    "od_notes": "commuting_extract_notes_2022.pdf",
    "survey": "wls_puf_2025-10_2026-09.csv",
    "codebook": "wls_puf_codebook_2025-26.pdf",
    "population": "acs5_2022_b01003_tracts.csv",
    "gazetteer": "gazetteer_tracts_2022.txt",
    "delineation": "cbsa_delineation_2023_six_states.xlsx",
    "cores": "candidate_cores_2027.xlsx",
    "board": "board_paper_pilot_metro_2027.pdf",
    "acs_commute": "acs5_2022_b08301_counties.csv",
    "cbp": "cbp_2022_county_sectors.csv",
    "expansion": "trenstead_expansion_log.xlsx",
    "listings": "retail_space_listings_20261001.csv",
    "locators": "competitor_locator_scrapes_2026.csv",
    "manifest": "data_pack_manifest.csv",
}
DISTRACTORS = ["acs_commute", "cbp", "expansion"]
ASK_FILES = ["listings", "locators"]
BRANDS = ["Tilldash", "Hopcrate"]
DENSE = 20000.0      # people present per km2: the dense-tract cut the prompt asks for
SQFT_PER_M2 = 10.7639104
