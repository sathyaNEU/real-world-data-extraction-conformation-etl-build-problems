"""The fixed facts of the world: Oriel Health Region's department of public health deciding its autumn 2027 MMR
catch-up, the national bodies whose files it holds, the dates, the codes and the design parameters of every
simulated record. Nothing here is computed from data; sim.py draws the records from these facts."""
import datetime as dt

SEED = 501

# --- organisation, people, dates --------------------------------------------------------------------------------
REGION = "Oriel Health Region"
DEPT = "Department of Public Health, Oriel Health Region"
RIO = "Regional Immunisation Office, Oriel Health Region"
COUNTIES = ["Louth", "Meath", "Cavan", "Monaghan"]
PEOPLE = {
    "manager": "Eadaoin Bonner",      # regional immunisation manager, the options paper
    "director": "Nigel Macmillan",    # director of public health, the planning standard
    "surveillance": "Therese McGann", # surveillance scientist, the case export
    "register": "Karl McLoughlin",    # register data manager, the extract notes
}

ASSESS = dt.date(2028, 1, 1)          # the winter assessment date (standard 3.3)
AS_AT = dt.date(2027, 6, 30)          # register extract as-at date
RUN = dt.date(2027, 7, 3)             # register extract run date
NDS_RUN = dt.date(2027, 7, 6)         # case export run date
PACK_DATE = dt.date(2027, 7, 12)      # the transmittal list; every file's mtime
CUTOVER = dt.date(2024, 7, 1)         # local health office revision in force
WINDOW = (dt.date(2019, 1, 1), dt.date(2027, 6, 30))   # the case ask's onset window
MIGRATION = dt.date(2021, 3, 1)       # the notifiable disease system went live
BACK_ENTRY = (dt.date(2021, 5, 10), dt.date(2021, 5, 28))

R0 = 15.0

# --- survey groups ------------------------------------------------------------------------------------------------
GROUPS = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54),
          (55, 59), (60, 64), (65, 69), (70, 120)]
GROUP_LABELS = ["%d-%d" % g if g[1] < 120 else "70+" for g in GROUPS]
NG = len(GROUPS)

# --- options (birth years, delivery, expected uptake among the susceptible, cost) ---------------------------------
EFFECTIVENESS = 0.97
OPTIONS = {
    "A": dict(years=(2013, 2017), uptake=0.45, setting="School immunisation team in primary schools (fifth and sixth "
              "class) and first and second year of secondary school, with GP follow-up", cost=412_000),
    "B": dict(years=(2008, 2012), uptake=0.38, setting="School immunisation team in secondary schools (third to sixth "
              "year) and further education colleges, GP invitation for school leavers", cost=438_000),
    "C": dict(years=(2003, 2007), uptake=0.35, setting="Clinics at the three third-level campuses in the region and GP "
              "invitation", cost=401_000),
    "D": dict(years=(1993, 1997), uptake=0.40, setting="GP and pharmacy invitation by letter and text message",
              cost=446_000),
    "E": dict(years=(1993, 2002), uptake=0.40, setting="GP and pharmacy invitation, with workplace clinics at the "
              "region's four largest employers", cost=459_000),
}
OPTION_KEYS = ["A", "B", "C", "D", "E"]

# --- immunity profile by year of birth (per cent immune, projected to 1 January 2028) -----------------------------
PROFILE_NOTE_BASIS = {
    "old": "presumed immune: born before 1978 (serosurvey 2019)",
    "sero": "serosurvey 2019 by year of birth, with MMR doses recorded since",
    "uptake": "MMR uptake by year of birth, adjusted for vaccine effectiveness",
    "proj26": "projected to 1 January 2028: first MMR dose due during 2027 at the 2025 births' uptake",
    "proj27": "projected to 1 January 2028: maternal antibody in infants under six months",
}


def profile_values():
    """Per cent immune by year of birth, 1927-and-earlier to 2027, and the basis of each value."""
    v, basis = {}, {}
    table = {1985: 95.5, 1986: 95.5, 1987: 95.0, 1988: 95.5, 1989: 95.0,
             1990: 95.0, 1991: 94.5, 1992: 93.0, 1993: 89.0, 1994: 88.0, 1995: 87.5, 1996: 88.5, 1997: 89.5,
             1998: 93.5, 1999: 94.5, 2000: 94.5, 2001: 95.0, 2002: 95.5,
             2003: 95.0, 2004: 95.5, 2005: 95.0, 2006: 95.5, 2007: 94.0,
             2008: 91.0, 2009: 88.5, 2010: 87.0, 2011: 87.5, 2012: 90.0,
             2013: 93.5, 2014: 95.0, 2015: 95.5, 2016: 96.0, 2017: 96.0,
             2018: 96.0, 2019: 95.5, 2020: 95.5, 2021: 96.0, 2022: 95.5, 2023: 95.5, 2024: 96.0, 2025: 95.5}
    for y in range(1927, 2028):
        if y <= 1967:
            p, b = 99.5, "old"
        elif y <= 1977:
            p, b = 99.0, "old"
        elif y <= 1984:
            p, b = 96.0, "sero"
        elif y <= 2012:
            p, b = table[y], "sero"
        elif y <= 2025:
            p, b = table[y], "uptake"
        elif y == 2026:
            p, b = 91.0, "proj26"
        else:
            p, b = 50.0, "proj27"
        v[y], basis[y] = p, b
    return v, basis


# --- population (single years, 1 January 2028 projection; 1 January 2023 national for the survey) ----------------
NAT_TOTAL_2023 = 5_184_000
REG_TOTAL_2028 = 538_400
NAT_KNOTS = [0, 4, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
NAT_SHAPE = [5.9, 6.3, 7.1, 7.0, 6.2, 6.0, 6.5, 7.6, 8.1, 7.6, 6.9, 6.4, 5.9, 5.2, 4.5, 3.5, 2.5, 1.6, 0.8, 0.25, 0.04]
REG_SHAPE = [6.0, 6.4, 7.3, 7.2, 6.2, 5.9, 6.4, 7.5, 8.1, 7.6, 6.9, 6.4, 5.9, 5.2, 4.4, 3.4, 2.4, 1.5, 0.75, 0.24, 0.04]
# county shares of each age (Meath younger, Cavan and Monaghan older)
COUNTY_SHARE = {"Louth": 0.272, "Meath": 0.441, "Cavan": 0.159, "Monaghan": 0.128}
COUNTY_AGE_TILT = {"Louth": 0.0, "Meath": -0.0022, "Cavan": 0.0014, "Monaghan": 0.0016}   # share change per year of age past 40

# --- the contact survey (National Social Contact Survey 2023, public use file) ------------------------------------
# Contacts per day by setting, built by single year of age for four kinds of day: a school-term weekday and weekend
# day, a summer-holiday weekday and weekend day. School, college and the teachers' contacts with pupils run on
# term weekdays only; childcare runs on weekdays all year; work is lighter in the summer and at weekends.
CONTACT = dict(s_prim=9.0, sig_prim=0.8, s_sec=20.0, sig_sec=0.9, teach=0.8, col=5.0, sig_col=2.0, creche=3.0,
               work=13.0, sig_work=12.0, work_hol=0.8, work_wkend=0.15, hh_pc=1.2, hh_partner=1.0, hh_sib=0.8,
               comm=3.5, comm_wkend=1.3, leis_teen=0.5, sig_leis=2.5, leis_hol=1.1, leis_wkend=1.4)
# two fieldwork periods; participants recruited to a quota per five-year band in each, diary days spread evenly
# over the days of the week (each quota a multiple of seven)
SURVEY_PERIODS = (("May", dt.date(2023, 5, 2), dt.date(2023, 5, 26), 168),
                  ("Summer", dt.date(2023, 7, 3), dt.date(2023, 8, 18), 336))
SURVEY_DISPERSION = 2.2       # participant-level gamma multiplier on the day's expected contacts
SURVEY_CAP = 45               # the diary has room for 45 contacts
SURVEY_UNKNOWN_AGE = 0.012    # contacts whose age band the participant could not give
SURVEY_SEED = 9029            # contacts drawn; texture (sex, settings, duration) on its own stream
SURVEY_TEXTURE_SEED = 9031
SURVEY_RELEASE = dt.date(2024, 3, 8)
# Table 1 publishes the statistics office's 1 January 2023 estimate by group, each group within about a quarter of a
# per cent of the national shape's total (its own stream)
NAT_PUBLISHED_SEED = SEED + 1358
NAT_PUBLISHED_SD = 0.0025

# --- local health office areas -------------------------------------------------------------------------------------
# the region's areas after the 1 July 2024 revision, and before it (LH27 Monaghan West, merged into LH26)
REGION_LHO_NEW = {"LH20": ("Dundalk", "Louth"), "LH21": ("Drogheda", "Louth"), "LH22": ("Navan", "Meath"),
                  "LH23": ("Ashbourne and Dunboyne", "Meath"), "LH24": ("Trim and Kells", "Meath"),
                  "LH25": ("Cavan", "Cavan"), "LH26": ("Monaghan", "Monaghan")}
REGION_LHO_OLD = dict(REGION_LHO_NEW)
REGION_LHO_OLD["LH26"] = ("Monaghan East", "Monaghan")
REGION_LHO_OLD["LH27"] = ("Monaghan West", "Monaghan")
# the rest of the national list (current scheme), health region by name
OTHER_LHO = {
    "LH01": ("Dublin North Central", "Dublin", "Dublin and North Coast"), "LH02": ("Dublin North West", "Dublin", "Dublin and North Coast"),
    "LH03": ("Fingal", "Dublin", "Dublin and North Coast"), "LH04": ("Dublin South Central", "Dublin", "Dublin and Mid-Leinster"),
    "LH05": ("Dublin South East", "Dublin", "Dublin and Mid-Leinster"), "LH06": ("Dun Laoghaire", "Dublin", "Dublin and Mid-Leinster"),
    "LH07": ("Dublin South West", "Dublin", "Dublin and Mid-Leinster"), "LH08": ("Wicklow", "Wicklow", "Dublin and Mid-Leinster"),
    "LH09": ("Kildare North", "Kildare", "Midlands"), "LH10": ("Kildare South", "Kildare", "Midlands"),
    "LH11": ("Longford and Westmeath", "Westmeath", "Midlands"), "LH12": ("Offaly", "Offaly", "Midlands"),
    "LH13": ("Wexford", "Wexford", "South East"), "LH14": ("Carlow and Kilkenny", "Kilkenny", "South East"),
    "LH15": ("Waterford", "Waterford", "South East"), "LH16": ("South Tipperary", "Tipperary", "South East"),
    "LH17": ("Cork North Lee", "Cork", "South West"), "LH18": ("Cork South Lee", "Cork", "South West"),
    "LH19": ("Kerry", "Kerry", "South West"),
    "LH27": ("Portlaoise", "Laois", "Midlands"),
    "LH28": ("Limerick", "Limerick", "Mid-West"), "LH29": ("Clare", "Clare", "Mid-West"),
    "LH30": ("North Tipperary", "Tipperary", "Mid-West"), "LH31": ("Laois", "Laois", "Midlands"),
    "LH32": ("Galway", "Galway", "West"), "LH33": ("Mayo", "Mayo", "West"),
    "LH34": ("Roscommon", "Roscommon", "West"), "LH35": ("Sligo and Leitrim", "Sligo", "North West"),
    "LH36": ("Donegal", "Donegal", "North West"),
}
# share of the region's residents in each pre-revision area
AREA_SHARE_OLD = {"LH20": 0.155, "LH21": 0.121, "LH22": 0.168, "LH23": 0.160, "LH24": 0.118, "LH25": 0.152,
                  "LH26": 0.094, "LH27": 0.032}
# where untransferred movers away live now (weights over the other areas)
MOVER_AREA_WEIGHTS = {"LH01": 4, "LH02": 3, "LH03": 6, "LH04": 2, "LH05": 2, "LH06": 1, "LH07": 2, "LH08": 1,
                      "LH09": 3, "LH10": 2, "LH11": 2, "LH12": 1, "LH13": 1, "LH14": 1, "LH15": 1, "LH16": 1,
                      "LH17": 1, "LH18": 1, "LH19": 1, "LH28": 1, "LH29": 1, "LH30": 1, "LH31": 2, "LH32": 2,
                      "LH33": 1, "LH34": 1, "LH35": 1, "LH36": 1}
PORTLAOISE_MOVERS_PER_COHORT_YEAR = (5, 14)   # moved to the new LH27 since July 2024, per year of birth (range)
# pupils living in Northern Ireland who attend school in the region: the school immunisation team opens a record at their
# first session, with the home address (a UK postcode) and, as no local health office covers it, the school's area
NI_PUPILS_PER_YEAR = {range(1993, 1995): (22, 35), range(1995, 2018): (38, 57)}
NI_SCHOOL_AREAS = {"LH20": (0.55, ["BT34", "BT35"]), "LH25": (0.20, ["BT92", "BT93", "BT94"]),
                   "LH26": (0.15, ["BT60", "BT61", "BT68", "BT69", "BT70", "BT71"]),
                   "LH27": (0.10, ["BT60", "BT68", "BT92"])}
NI_WITH_GP = 0.30             # of those, registered with a practice in the region
EIRCODE_FROM = dt.date(2015, 7, 13)
ROUTING_KEYS = {"LH20": ["A91"], "LH21": ["A92"], "LH22": ["C15"], "LH23": ["A84", "A85", "A86"], "LH24": ["A82", "A83"],
                "LH25": ["H12", "H14", "H16"], "LH26": ["H18", "A75", "A81"], "LH27_old": ["H23", "H18"],
                "LH26_new": ["H18", "A75", "A81", "H23"],
                "LH01": ["D01", "D03", "D07", "D09"], "LH02": ["D07", "D11", "D15"], "LH03": ["K32", "K36", "K45", "K67"],
                "LH04": ["D08", "D12"], "LH05": ["D04", "D06", "D14"], "LH06": ["A94", "A96"],
                "LH07": ["D22", "D24", "K78"], "LH08": ["A98", "A63", "A67"], "LH09": ["W23", "W12"],
                "LH10": ["W91", "R51", "W34"], "LH11": ["N37", "N91", "N39"], "LH12": ["R35", "R42"],
                "LH13": ["Y35", "Y21", "Y34"], "LH14": ["R95", "R93"], "LH15": ["X91", "X35"], "LH16": ["E91", "E21", "E32"],
                "LH17": ["T23", "P31"], "LH18": ["T12", "P43"], "LH19": ["V92", "V93"], "LH27": ["R32"],
                "LH28": ["V94", "V35"], "LH29": ["V95", "V15"], "LH30": ["E45", "E53"], "LH31": ["R32", "R14"],
                "LH32": ["H91", "H53", "H54"], "LH33": ["F23", "F28", "F31"], "LH34": ["F42", "F45"],
                "LH35": ["F91", "N41"], "LH36": ["F92", "F93", "F94"]}

# --- register design ------------------------------------------------------------------------------------------------
REGISTER_COVERAGE = {range(1993, 2003): 0.86, range(2003, 2018): 0.935}   # residents held, of the projection
MOVED_AWAY_SHARE = {range(1993, 2003): 0.071, range(2003, 2008): 0.058, range(2008, 2018): 0.024}
GP_PRACTICES = 92
QUERY_RATE = 0.0125                              # GP MMR return lines for children queried, 2005 onwards
QUERY_RATE_ADULT = 0.06                          # lines for adults (eligibility is checked line by line)
QUERY_OUTCOMES = {"replaced": 0.41, "withdrawn": 0.14, "confirmed": 0.45}
QUERY_LOG_START = dt.date(2005, 1, 1)
DUPLICATE_SHARE = 0.034                          # born-in-region children registered twice and merged
CHAIN_SHARE = 0.30                               # of those with a later GP dose, a third record and a chain of two merges
