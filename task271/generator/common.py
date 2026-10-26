"""Constants for task271 architecture 4: Halverstead Mutual Fire Insurance Company's 2027 agency township, the
book's 2023 to 2025 experience, the county's 2026 assessor roll, the water authority's pressure zones and
hydrants, the people, the dates and the pack's files."""
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP

SEED = 6

ORG = "Halverstead Mutual Fire Insurance Company"
ORG_SHORT = "Halverstead Mutual"
COUNTY = "Tamswold County"
AUTHORITY = "Tamswold County Water Authority"
AUTH_SHORT = "TCWA"
TANK = "Ostrander Ridge Tank"
STEB = "State Tax Equalization Board"
REQUESTER = "Dillon Evans"        # the mutual's underwriting manager
PRESIDENT = "Luis Thomas"         # the mutual's president, signs the expansion brief
ENGINEER = "Robin Fields"         # the authority's engineer of record

# township code, name, kind; the book writes the first four, the agency goes to one of the last three
TOWNS = [("WYV", "Wyvellton", "Borough"), ("HLT", "Holtmere", "Township"), ("VRN", "Varnacott", "Township"),
         ("MRV", "Merrivane", "Township"), ("DOR", "Dorrance Hill", "Borough"), ("BRK", "Brookmere", "Township"),
         ("SAL", "Sallowmead", "Township")]
BOOK_TOWNS = ["WYV", "HLT", "VRN", "MRV"]
CANDIDATES = ["DOR", "BRK", "SAL"]
TOWN_NAME = {c: n for c, n, k in TOWNS}
TOWN_FULL = {c: "%s %s" % (n, k) for c, n, k in TOWNS}

# the authority's pressure zones: id, name, supply, hydraulic grade line (ft), service elevation range (ft)
ZONES = [("PZ-1", "Ridge", "Ostrander Ridge Tank", 1412, (1240, 1320)),
         ("PZ-2", "Upper", "Kilns Road booster station and Upper Tank", 1338, (1170, 1245)),
         ("PZ-3", "Valley", "Ostrander Ridge Tank, direct main", 1412, (1120, 1190)),
         ("PZ-4", "Southside", "Southside Tank", 1335, (1165, 1240))]
PSI_PER_FT = 0.433


def psi_range(z):
    """static pressure at the zone's highest and lowest services, psi"""
    hgl, (lo, hi) = z[3], z[4]
    return (int(r((hgl - hi) * PSI_PER_FT)), int(r((hgl - lo) * PSI_PER_FT)))


ZONE_IDS = [z[0] for z in ZONES]
VALLEY = "PZ-3"

# the world's true non-weather water claim frequency per house-year: base, foundation and zone factors
BASE_RATE = 0.0128
BASEMENT_FACTOR = 1.6
ZONE_FACTOR = {"PZ-1": 1.0, "PZ-2": 1.0, "PZ-3": 2.25, "PZ-4": 1.0}

# dates
EXPERIENCE = (dt.date(2023, 1, 1), dt.date(2025, 12, 31))
YEARS = [2023, 2024, 2025]
EXTRACT = dt.date(2026, 8, 31)            # policy, claim and payment extracts
CODE_CHANGE = dt.date(2024, 1, 1)         # the claim system's new cause-of-loss codes
ROLL_DATE = dt.date(2026, 1, 1)           # the certified 2026 assessment roll
ROLL_EXTRACT = dt.date(2026, 7, 15)
BASE_YEAR = 1998                          # the county's base year for assessed values
CLR_2026 = 0.428                          # STEB common level ratio for the county, used from 1 July 2026
CLR_2025 = 0.451
ZONE_MAP_DATE = dt.date(2025, 11, 14)
HYDRANT_DATE = dt.date(2026, 6, 30)
MASTER_PLAN = dt.date(2019, 6, 20)
STANDARD_DATE = dt.date(2024, 3, 12)      # Frequency Model Standard, revision 2
GUIDE_DATE = dt.date(2025, 2, 3)          # underwriting guide, homeowners
BRIEF_DATE = dt.date(2026, 10, 5)
ASSEMBLED = dt.datetime(2026, 10, 21, 16, 40)
BOARD_DATE = dt.date(2026, 11, 18)
AGENCY_OPENS = dt.date(2027, 4, 1)

FILES = dict(
    terms="policy_terms_2023_2025.csv",
    claims="claims_register_2023_2025.csv",
    payments="claim_payments_2023_2026.csv",
    codes="cause_of_loss_codes.csv",
    parcels="tamswold_parcels_2026.csv",
    dwellings="tamswold_dwellings_2026.csv",
    appeals="assessment_appeals_2026.csv",
    clr="steb_common_level_ratios.csv",
    zones="tcwa_pressure_zones.geojson",
    hydrants="tcwa_hydrants.geojson",
    flowtests="tcwa_hydrant_flow_tests.csv",
    plan="tcwa_master_plan_2019_excerpt.pdf",
    bordereau="cas_bordereau_halverstead_2023_2026.xlsx",
    standard="frequency_model_standard_rev2.pdf",
    guide="underwriting_guide_homeowners_2025.pdf",
    brief="board_expansion_brief_2027.pdf",
    weather="noaa_daily_weather_2023_2025.csv",
    permits="tamswold_building_permits_2023_2025.csv",
    dictionary="data_dictionary.csv",
    readme="pack_contents.txt",
)
DISTRACTORS = ["weather", "permits"]
BOOK = "agency_township_2027.xlsx"
CHART = "water_claims_by_township_2027.png"


def r(x, n=0):
    """half-up rounding at n decimals"""
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))
