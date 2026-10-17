"""task465 world: the Ardley Plains Growers' Cooperative's 2027 area-yield drought covers.

An unnamed High Plains state. Its Crop and Livestock Reporting Service publishes county, district and state
estimates of acres, production and yield by crop and practice; a county's estimate for a practice is not published
when it rests on fewer than five reports or its coefficient of variation exceeds 30 per cent, and is still counted in
the district and state estimates. The cooperative's members grow dryland grain sorghum in five counties on the sandy
ground where four agricultural statistics districts meet; Quillfield Re quotes a cover on each county's official
non-irrigated sorghum yield for the 2027 crop year.
"""
STREAM = 46507
YEARS = list(range(1991, 2026))
Y0 = 1991
OLD_PULL = (1991, 2023)        # the cooperative's long download, March 2024
NEW_PULL = (2016, 2025)        # the refresh, October 2026
REVISED = (2017, 2021)         # county estimates revised to the 2022 Census of Agriculture
RECODE_YEAR = 2008             # district codes went from one digit to two

DISTRICTS = {  # code: name
    10: "Northwest", 20: "West Central", 30: "Southwest", 40: "North Central", 50: "Central",
    60: "South Central", 70: "Northeast", 80: "East Central", 90: "Southeast",
}
COUNTY_DISTRICTS = (20, 30, 50, 60)

# county: (ansi code, district, member, dryland sorghum: trend yield 1991, slope bu/acre/yr, sensitivity, noise,
#          planted acres; irrigated sorghum planted acres (0 = none))
COUNTIES = {
    "Ardley":     ("009", 20, True,  40.0, 0.44, 1.00, 0.050, 6900, 0),
    "Brannock":   ("005", 20, False, 46.5, 0.55, 1.00, 0.045, 30000, 1800),
    "Lindqvist":  ("027", 20, False, 45.0, 0.53, 1.00, 0.045, 27000, 0),
    "Pellow":     ("041", 20, False, 48.0, 0.58, 0.98, 0.045, 33000, 3300),
    "Ruddock":    ("057", 20, False, 44.0, 0.50, 1.02, 0.045, 24000, 0),
    "Tolsey":     ("063", 20, False, 46.0, 0.54, 1.00, 0.045, 21000, 1200),
    "Tresham":    ("071", 30, True,  38.5, 0.41, 1.00, 0.050, 5600, 0),
    "Cobbett":    ("013", 30, False, 46.0, 0.55, 1.00, 0.045, 36000, 2900),
    "Durrance":   ("029", 30, False, 45.0, 0.53, 1.00, 0.045, 29000, 0),
    "Kestner":    ("047", 30, False, 47.0, 0.56, 0.98, 0.045, 31000, 2200),
    "Quenby":     ("065", 30, False, 44.5, 0.52, 1.01, 0.045, 25000, 0),
    "Varga":      ("083", 30, False, 46.5, 0.55, 1.00, 0.045, 20000, 1500),
    "Corvin":     ("021", 50, True,  50.0, 0.62, 0.95, 0.045, 38000, 4100),
    "Elster":     ("037", 50, True,  39.5, 0.43, 1.00, 0.050, 6200, 0),
    "Fothergill": ("015", 50, False, 46.5, 0.55, 1.00, 0.045, 30000, 1800),
    "Gaddis":     ("033", 50, False, 45.5, 0.52, 0.99, 0.045, 18000, 0),
    "Iverly":     ("051", 50, False, 48.0, 0.58, 0.98, 0.045, 33000, 3300),
    "Stannard":   ("069", 50, False, 44.0, 0.50, 1.02, 0.045, 24000, 0),
    "Pallard":    ("045", 60, True,  41.0, 0.46, 1.00, 0.050, 7400, 0),
    "Dornick":    ("011", 60, False, 46.0, 0.55, 1.00, 0.045, 36000, 2900),
    "Halvorsen":  ("023", 60, False, 45.0, 0.53, 1.00, 0.045, 29000, 0),
    "Ingleby":    ("039", 60, False, 47.0, 0.56, 0.98, 0.045, 31000, 2200),
    "Rumbold":    ("055", 60, False, 44.5, 0.52, 1.01, 0.045, 25000, 0),
    "Treloar":    ("073", 60, False, 46.5, 0.55, 1.00, 0.045, 20000, 1500),
}
MEMBERS = ["Ardley", "Corvin", "Elster", "Pallard", "Tresham"]

# district weather (share of normal dryland yield potential) in the region's drought years
DROUGHT = {
    20: {1996: 0.75, 2002: 0.55, 2006: 0.72, 2011: 0.50, 2012: 0.73, 2022: 0.57},
    30: {2002: 0.66, 2003: 0.70, 2006: 0.60, 2011: 0.52, 2014: 0.74, 2022: 0.69},
    50: {1996: 0.74, 2002: 0.56, 2006: 0.73, 2011: 0.49, 2012: 0.71, 2018: 0.83, 2022: 0.58},
    60: {1996: 0.77, 2002: 0.80, 2003: 0.58, 2011: 0.53, 2014: 0.75, 2018: 0.78, 2020: 0.79, 2022: 0.78},
}
# the years too few farms harvested dryland sorghum for a county estimate: harvested yield, harvested acres
WITHHELD = {
    ("Ardley", 2002): (11.4, 500), ("Ardley", 2011): (8.6, 500), ("Ardley", 2022): (12.5, 400),
    ("Elster", 2002): (10.4, 500), ("Elster", 2011): (8.0, 300), ("Elster", 2022): (13.2, 500),
    ("Pallard", 2003): (9.8, 500), ("Pallard", 2011): (11.5, 600),
    ("Tresham", 2006): (24.5, 800), ("Tresham", 2011): (22.6, 500),
}
COVERAGE = 0.90
BUY_MULTIPLE = 1.4

# Quillfield Re's quoted premium rates for the 2027 dryland sorghum covers, per cent of liability
QUOTES = {"Ardley": 7.00, "Corvin": 5.65, "Elster": 8.20, "Pallard": 5.10, "Tresham": 7.25}

# ---------------------------------------------------------------- the pack
ORG = "Ardley Plains Growers' Cooperative"
SERVICE = "Crop and Livestock Reporting Service"
REINSURER = "Quillfield Re"
PEOPLE = {"risk": "Brent Little", "chair": "Martha Dalton"}
TITLE = {"risk": "Risk Manager", "chair": "Chair of the Board"}
BOARD_DATE = "19 November 2026"
AS_OF = "2026-11-02"

FILES = {
    "pull24": "clrs_county_estimates_pull_2024-03.csv",
    "pull26": "clrs_county_estimates_pull_2026-10.csv",
    "methods": "clrs_county_estimates_methods_2026.pdf",
    "terms": "quillfield_re_area_yield_term_sheet_2027.pdf",
    "quotes": "quillfield_re_quote_schedule_2027.xlsx",
    "policy": "apgc_risk_policy_2026.pdf",
    "enrol": "apgc_cover_enrolment_2027.csv",
    "notice": "apgc_cover_enrolment_notice_2027.txt",
    "tickets": "apgc_scale_tickets_2016_2020.csv",
    "transfers": "apgc_site_transfers_2016_2020.csv",
    "roster": "apgc_member_roster_2026.xlsx",
    "drought": "drought_monitor_county_weeks_2000_2025.csv",
    "prior": "apgc_prior_covers_2019_2025.xlsx",
    "dict": "data_dictionary.csv",
    "register": "file_register.csv",
}
DISTRACTORS = ["drought", "prior"]
GOLDEN = {"workbook": "county_area_yield_quotes_2027.xlsx", "record": "conformed_county_dryland_sorghum_yields.csv"}

# Ask A: the term sheet's liability terms and the enrolment close
PRICE_CWT = 7.75                 # projected price, dollars per hundredweight
BUSHEL_LB = 56
CLOSE_LOCAL = "2026-10-30 17:00"  # Central time, UTC-5 on that date
CLOSE_UTC = "2026-10-30T22:00:00Z"
STANDARD_MOISTURE = 14.0
# Ask B: the cooperative's elevator sites
SITES = {"MAIN": "Corvin terminal", "ARD": "Ardley", "ELS": "Elster", "PAL": "Pallard", "TRE": "Tresham"}
