"""The fixed world: the Tallis Valley Workforce Development Board (one county, Tallis County, in an unnamed U.S. state),
the state's quarterly covered employment and wages record for its counties, the pay schedules each industry's
payrolls run on (recorded nowhere), and the board's own program and training-account records. Every other module
reads its parameters from here."""
import datetime as dt

STATE_FIPS = "52"
COUNTY = "Tallis County"
COUNTY_FIPS = "52037"
BOARD = "Tallis Valley Workforce Development Board"
AGENCY = "State Department of Labor, Labor Market Information Division"
FUND = "State Sector Partnership Fund"
PEOPLE = {"analyst": ("Beverly Ray", "Labor Market Analyst"),
          "director": ("Dalton Harding", "Executive Director")}
SEED = 477
Y0, Y1 = 2013, 2025
BASE, LATEST = 2021, 2025
SLATE = 4
MIN_JOBS = 1000              # eligible: annual average private jobs in the county in the latest year
GUIDELINE_DATE = "3 August 2026"
MEMO_DATE = "14 October 2026"
VOTE_DATE = "5 November 2026"

# Pay schedules. Weekly and biweekly payrolls pay on a weekday; a biweekly payroll pays on one of two alternating
# weeks (its phase, anchored on a date in January 2021). A pay date on a weekend or federal holiday is paid on the
# business day before. Semimonthly payrolls pay on the 15th and the last day of the month, monthly on the last day.
SCHEDULES = {"WF": ("weekly", 4, None), "FA": ("biweekly", 4, dt.date(2021, 1, 1)), "FB": ("biweekly", 4, dt.date(2021, 1, 8)),
             "WT": ("weekly", 3, None), "TA": ("biweekly", 3, dt.date(2021, 1, 7)), "TB": ("biweekly", 3, dt.date(2021, 1, 14)),
             "SM": ("semimonthly", None, None), "MO": ("monthly", None, None)}

# Private NAICS sectors: title, Tallis 2025 jobs (approx), 2021 weekly pay for the work done (approx, dollars), growth in
# pay per job for the work done 2021 to 2025 (target), employment growth a year, children (3-digit code, share of the
# sector's jobs, pay relative to the sector, schedule mix)
F = {"FA": .5, "FB": .5}
def mix(**k):
    t = sum(k.values())
    assert abs(t - 1) < 1e-9, k
    return k

SECTORS = {
    "11": ("Agriculture, forestry, fishing and hunting", 310, 820, .150, .004,
           [("111", .62, .95, mix(WF=.6, SM=.4)), ("115", .38, 1.08, mix(WF=.8, FA=.2))]),
    "21": ("Mining, quarrying, and oil and gas extraction", 95, 1390, .140, -.01,
           [("212", 1.0, 1.0, mix(FA=.5, FB=.5))]),
    "22": ("Utilities", 430, 1780, .162, .002,
           [("221", 1.0, 1.0, mix(SM=.7, FB=.3))]),
    "23": ("Construction", 6150, 1290, .188, .021,
           [("236", .28, 1.06, mix(WF=.7, FA=.3)), ("237", .17, 1.18, mix(WF=.6, FB=.4)),
            ("238", .55, .92, mix(WF=.75, FA=.1, FB=.15))]),
    "31-33": ("Manufacturing", 11800, 1360, .182, .006,
              [("311", .21, .78, mix(WF=.5, TB=.5)), ("326", .17, .95, mix(FA=.55, FB=.45)),
               ("332", .24, 1.02, mix(WF=.6, FB=.4)), ("333", .19, 1.12, mix(FA=.4, FB=.3, SM=.3)),
               ("336", .19, 1.13, mix(TB=.85, SM=.15))]),
    "42": ("Wholesale trade", 4380, 1420, .164, .008,
           [("423", .52, 1.04, mix(FA=.45, FB=.35, SM=.2)), ("424", .38, .94, mix(TA=.45, WF=.25, FB=.3)),
            ("425", .10, 1.05, mix(SM=1.0))]),
    "44-45": ("Retail trade", 13900, 640, .157, .004,
              [("441", .14, 1.18, mix(FA=.5, FB=.5)), ("444", .10, .93, mix(WF=.3, FA=.35, FB=.35)),
               ("445", .27, .78, mix(WT=.55, FA=.25, FB=.2)), ("452", .22, .82, mix(TA=.6, FB=.4)),
               ("454", .06, 1.32, mix(SM=.6, FB=.4)), ("447", .21, 1.10, mix(WF=.4, FA=.3, FB=.3))]),
    "48-49": ("Transportation and warehousing", 6900, 1010, .170, .028,
              [("484", .44, 1.13, mix(TA=.85, WF=.15)), ("493", .41, .93, mix(WT=.75, FA=.25)),
               ("492", .15, .93, mix(FA=.5, FB=.5))]),
    "51": ("Information", 1840, 1510, .213, -.004,
           [("517", .44, 1.08, mix(SM=.7, FA=.3)), ("518", .21, 1.16, mix(SM=.8, MO=.2)),
            ("519", .35, .82, mix(FB=.5, SM=.5))]),
    "52": ("Finance and insurance", 4920, 1690, .207, .007,
           [("522", .48, .97, mix(SM=.6, FA=.2, FB=.2)), ("524", .41, 1.02, mix(SM=.8, FB=.2)),
            ("523", .11, 1.06, mix(SM=.5, MO=.5))]),
    "53": ("Real estate and rental and leasing", 1610, 1060, .138, .011,
           [("531", .71, 1.01, mix(TA=.45, FA=.25, FB=.3)), ("532", .29, .98, mix(WF=.5, FB=.5))]),
    "54": ("Professional, scientific, and technical services", 5240, 1640, .193, .019,
           [("541", 1.0, 1.0, mix(SM=.55, FA=.25, FB=.2))]),
    "55": ("Management of companies and enterprises", 770, 2010, .151, .003,
           [("551", 1.0, 1.0, mix(SM=.9, FB=.1))]),
    "56": ("Administrative and support and waste management and remediation services", 7300, 760, .151, .013,
           [("561", .86, .97, mix(WT=.6, FA=.2, FB=.2)), ("562", .14, 1.18, mix(FA=.5, FB=.5))]),
    "61": ("Educational services", 2380, 880, .126, .005,
           [("611", 1.0, 1.0, mix(SM=.5, MO=.2, TA=.3))]),
    "62": ("Health care and social assistance", 19600, 1080, .173, .012,
           [("621", .20, 1.16, mix(FA=.5, FB=.5)), ("622", .48, 1.18, mix(TA=.95, SM=.05)),
            ("623", .18, .71, mix(WF=.3, FA=.35, FB=.35)), ("624", .14, .58, mix(FA=.6, FB=.4))]),
    "71": ("Arts, entertainment, and recreation", 1460, 560, .149, .015,
           [("713", .78, .93, mix(TA=.5, FB=.5)), ("711", .22, 1.25, mix(WF=.6, SM=.4))]),
    "72": ("Accommodation and food services", 12600, 430, .168, .017,
           [("722", .86, .97, mix(WT=.6, FA=.2, FB=.2)), ("721", .14, 1.18, mix(FA=.5, FB=.5))]),
    "81": ("Other services (except public administration)", 3080, 780, .143, .006,
           [("811", .42, 1.07, mix(WF=.6, FA=.4)), ("812", .33, .82, mix(TA=.5, FB=.5)),
            ("813", .25, 1.11, mix(SM=.6, FA=.4))]),
    "99": ("Unclassified", 45, 900, .14, 0.0, [("999", 1.0, 1.0, mix(FA=.5, FB=.5))]),
}
# the golden's growth in pay per job 2021 to 2025, per cent (tune.py moves ADJ until the cut pack lands here)
DESIRED = {"23": 19.0, "31-33": 18.3, "42": 17.2, "44-45": 15.2, "48-49": 17.2, "51": 21.9, "52": 21.1, "53": 12.9,
           "54": 19.2, "56": 14.8, "61": 13.2, "62": 17.3, "71": 13.8, "72": 16.8, "81": 14.1}
ADJ = {'23': 0.00469, '31-33': 0.00287, '42': 0.01673, '44-45': -0.01013, '48-49': 0.03211, '51': 0.00903, '52': -0.00458, '53': -0.01355, '54': -0.03014, '56': 0.02302, '61': 0.00826, '62': -0.00192, '71': 0.02065, '72': 0.01952, '81': 0.00955}
# NAICS 2022 split retail 452 and 454 into 455 to 459 from 2022 on (Layer 1: the code vintage)
NAICS2022 = {"452": [("455", 1.0)], "454": [("459", .4), ("456", .25), ("458", .35)]}

# other counties of the state: name, FIPS, private jobs scale relative to Tallis
COUNTIES = [("Ambrose County", "52001", .42), ("Bexley County", "52003", .18), ("Carrow County", "52005", 1.85),
            ("Dunmere County", "52007", .27), ("Elsworth County", "52009", .61), ("Farrin County", "52011", .12),
            ("Galloway County", "52013", 2.40), ("Hesper County", "52015", .33), ("Iverly County", "52017", .09),
            ("Jessup County", "52019", .55), ("Kinross County", "52021", .21), ("Larkin County", "52023", .74),
            ("Marlow County", "52025", .15), ("Norcross County", "52027", 1.12), ("Oakhurst County", "52029", .38),
            ("Pellam County", "52031", .08), ("Quarry County", "52033", .29), ("Redfield County", "52035", .47),
            ("Sutter County", "52039", .19), ("Thorne County", "52041", .66), ("Upland County", "52043", .11),
            ("Vardon County", "52045", .24), ("Westbrook County", "52047", .93)]

FILES = {
    "qcew_a": "qcew_state52_county_2013_2019.csv",
    "qcew_b": "qcew_state52_county_2020_2025q3.csv",
    "qcew_c": "qcew_state52_county_2025_annual_release.csv",
    "layout": "qcew_county_file_layout_and_notes.pdf",
    "areas": "qcew_area_titles.csv",
    "industries": "qcew_industry_titles.csv",
    "guidelines": "sector_partnership_fund_guidelines_2027.pdf",
    "exits": "wioa_exits_2025.csv",
    "wages": "ui_wage_match_return_2025q3_2026q2.csv",
    "employers": "ui_employer_accounts_extract_2026-08.csv",
    "peo": "peo_client_registrations_2025.csv",
    "ita": "ita_voucher_ledger_2025.csv",
    "register": "fiscal_agent_check_register_2025_2026.csv",
    "etpl": "etpl_programs_2025.xlsx",
    "manual": "tvwdb_performance_reporting_manual.pdf",
    "projections": "tallis_industry_projections_2024_2034.xlsx",
    "oews": "oews_tallis_county_may2025.xlsx",
}
GOLDEN = {"table": "sector_partnership_application_2027.csv", "memo": "sector_partnership_slate_2027.docx"}
