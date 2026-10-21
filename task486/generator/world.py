"""task486 world: Kelvane County, in an unnamed U.S. state, and its six senior-services provider areas.

The county Office on Aging funds one senior-services provider per provider area: Wickmoor City and Fallowmere Town (the
cores of the county seat and of the second town) and North, East, South and West Kelvane, which take in the countryside
and, since the 2023 redraw, the edges of both towns out to the ring roads and the river, so their boundaries cut the
census block groups at the town edges. The county's FY2027 area plan update to the state carries each provider area's
census-day counts of residents aged 60 and over and 75 and over, which the county's allocation policy uses to split its
Title III funds among the providers, and each provider's FY2026 home-delivered meals and its active meal clients on
30 September 2026.

The 2020 census counts come from the census's Demographic and Housing Characteristics release, which is formally
private: every count below the state was noise-infused and then post-processed, level by level from the county down to
the block, into non-negative whole numbers that add up to the level above. Housing unit counts and group quarters
facilities are held exact. Provider areas are not census tabulation areas, so their counts are built from the release's
tables."""
import datetime as dt

SEED = 889                  # the census draw (seed search, design note: Ladder)
STATE_FIPS = "57"           # an unnamed state; no state is named in the pack
COUNTY_FIPS = "041"
COUNTY = "Kelvane County"
SEAT = "Wickmoor"
TOWN2 = "Fallowmere"
OFFICE = "Kelvane Area Agency on Aging"            # a nonprofit the state designates for the county
PLANNING = "Kelvane County Department of Planning and Development"
STATE_UNIT = "State Department on Aging"
PEOPLE = {"planning": "Priscilla Kemp",     # demographer, Department of Planning and Development
          "aging": "Donald Castillo"}        # planning and grants officer, Office on Aging

CENSUS_DAY = dt.date(2020, 4, 1)
REDRAW = dt.date(2023, 7, 1)                 # provider areas as drawn from this date
FY_FIRST, FY_LAST = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
AS_OF = dt.date(2026, 9, 30)                 # clients active on this day
PULL = dt.date(2026, 10, 9)                  # the planning department's extract of the release and the county files

AREAS = ["Wickmoor City", "Fallowmere Town", "North Kelvane", "East Kelvane", "South Kelvane", "West Kelvane"]
TOWN_AREAS = AREAS[:2]
RURAL_AREAS = AREAS[2:]

# The release's sex-by-age table (the census's P12 layout): 23 age groups for each sex.
AGE_GROUPS = ["Under 5 years", "5 to 9 years", "10 to 14 years", "15 to 17 years", "18 and 19 years", "20 years",
              "21 years", "22 to 24 years", "25 to 29 years", "30 to 34 years", "35 to 39 years", "40 to 44 years",
              "45 to 49 years", "50 to 54 years", "55 to 59 years", "60 and 61 years", "62 to 64 years",
              "65 and 66 years", "67 to 69 years", "70 to 74 years", "75 to 79 years", "80 to 84 years",
              "85 years and over"]
SEXES = ["Male", "Female"]
A60 = list(range(15, 23))       # 60 and over: eight groups
A75 = list(range(20, 23))       # 75 and over: three groups
NCELL = 2 * len(AGE_GROUPS)     # cell index = sex * 23 + age group

# Noise standard deviation of each count before post-processing, by level of the release (persons).
SIGMA = {"county": 0.6, "tract": 1.0, "block_group": 1.1, "block": 1.6}
