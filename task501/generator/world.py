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
    "B": dict(years=(2008, 2012), uptake=0.45, setting="School immunisation team in secondary schools (third to sixth "
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
    for y in range(1927, 2028):
        if y <= 1967:
            p, b = 99.5, "old"
        elif y <= 1977:
            p, b = 99.0, "old"
        elif y <= 1984:
            p, b = 96.0, "sero"
        elif y <= 1989:
            p, b = 95.5, "sero"
        elif y <= 1997:
            p, b = {1990: 93.0, 1991: 91.5, 1992: 89.5, 1993: 86.5, 1994: 85.0, 1995: 84.5, 1996: 85.5, 1997: 87.0}[y], "sero"
        elif y <= 2002:
            p, b = {1998: 92.0, 1999: 92.5, 2000: 92.5, 2001: 93.0, 2002: 93.0}[y], "sero"
        elif y <= 2007:
            p, b = {2003: 93.5, 2004: 93.0, 2005: 93.5, 2006: 94.0, 2007: 93.5}[y], "sero"
        elif y <= 2012:
            p, b = {2008: 91.0, 2009: 88.5, 2010: 87.0, 2011: 87.5, 2012: 90.0}[y], "sero"
        elif y <= 2017:
            p, b = {2013: 94.0, 2014: 94.5, 2015: 95.0, 2016: 95.5, 2017: 96.0}[y], "uptake"
        elif y <= 2021:
            p, b = {2018: 95.5, 2019: 95.5, 2020: 95.0, 2021: 95.5}[y], "uptake"
        elif y <= 2025:
            p, b = {2022: 95.0, 2023: 94.5, 2024: 95.0, 2025: 94.5}[y], "uptake"
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

# --- contact model (contacts per participant per day, single years) ----------------------------------------------
CONTACT = dict(s_prim=7.0, s_mid=7.0, s_sec=10.8, sig_prim=1.0, sig_sec=1.2, work=4.0, sig_work=10.0, hh_pc=1.0,
               hh_partner=0.9, hh_sib=0.8, comm=3.5)
SURVEY_PARTICIPANTS = [512, 548, 603, 641, 466, 421, 455, 507, 533, 509, 471, 437, 398, 352, 518]
SURVEY_DISPERSION = 1.6
SURVEY_SEED = 9024

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
