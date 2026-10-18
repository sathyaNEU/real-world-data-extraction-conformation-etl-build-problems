"""Constants of the Kessick Valley world: the bureau and its two airports, the survey's waves and lots, the
service area, the city markets and how travellers write them, the regional airport's 2027 schedule, the files."""
import datetime as dt

YEAR = 2026
SEED = 512

STATE_AGENCY = "Department of Transportation"
BUREAU = "Bureau of Aviation"
HUB = "Brennick International Airport"
HUB_SHORT = "Brennick International"
HUB_CODE = "ADR"
REGIONAL = "Kessick Valley Regional Airport"
REGIONAL_SHORT = "Kessick Valley Regional"
REGIONAL_CODE = "KVR"
CONTRACTOR = "Talbridge Field Research"
PEOPLE = {"asd": "Tina Hurley", "contractor": "Carlos Phillips", "parking": "Donald Lara"}

AS_OF = dt.date(2027, 1, 29)

# Long-stay lots the survey covered (the garage is short-term and outside the survey and the pitch standard).
LOTS = ["Economy C", "Economy D", "Long-Term"]
LOT_OLD = {"Economy C": "ECONOMY C", "Economy D": "ECONOMY D", "Long-Term": "LONG TERM", "Garage": "GARAGE"}
LOT_NEW = {"Economy C": "EC", "Economy D": "ED", "Long-Term": "LT", "Garage": "GR"}
PLAZA = {"Economy C": "Plaza C", "Economy D": "Plaza D", "Long-Term": "Plaza L"}
UPGRADE = dt.date(2026, 7, 1)        # the revenue control system's upgrade: new codes, ISO dates, permit lanes counted
GARAGE_PER_DAY = 1850
GARAGE_SEASON = {1: 0.91, 2: 1.04, 3: 1.11, 4: 0.95}
LOT_SHARE = {"Economy C": 0.34, "Economy D": 0.27, "Long-Term": 0.39}

# Survey waves: 28 handout days each, boxes emptied nightly through two days after the last handout.
WAVES = [
    ("W1", 1, dt.date(2026, 2, 2)),
    ("W2", 2, dt.date(2026, 5, 4)),
    ("W3", 3, dt.date(2026, 8, 3)),
    ("W4", 4, dt.date(2026, 11, 2)),
]
HAND_DAYS = 28
LAST_COLLECT = 30      # day index (1-based from the wave's first handout day) of the last box collection
MAX_STAY = 28          # nights; the long-stay lots tow after 28 days

QUARTER_DAYS = {1: 90, 2: 91, 3: 92, 4: 92}

# Candidate markets and the served ones. Per market: annual service-area parked trips (car parties),
# mean nights by quarter, gamma shape, mean party size, seasonal weights by quarter.
MARKETS = {
    # code: (name, trips, nights by quarter, shape, party, season weights, candidate)
    "TPA": ("Tampa", 6200, (23.0, 13.0, 8.0, 17.0), 3.5, 1.65, (1.9, 0.9, 0.5, 0.9), True),
    "PHX": ("Phoenix", 6000, (22.0, 12.0, 7.0, 16.0), 3.5, 1.75, (1.8, 0.9, 0.5, 1.0), True),
    "RSW": ("Fort Myers", 2500, (23.0, 14.0, 9.0, 18.0), 4.0, 1.7, (2.3, 0.8, 0.2, 0.8), True),
    "ORL": ("Orlando", 2600, (7.0, 7.0, 7.0, 7.0), 4.0, 2.8, (1.4, 1.1, 1.1, 0.8), True),
    "FLL": ("Fort Lauderdale", 1500, (10.0, 8.0, 7.0, 9.0), 4.0, 2.2, (1.6, 0.9, 0.6, 1.0), True),
    "LAS": ("Las Vegas", 2400, (4.0, 4.0, 4.0, 4.0), 4.0, 2.1, (1.0, 1.0, 1.0, 1.0), True),
    "MYR": ("Myrtle Beach", 3000, (6.0, 6.0, 6.0, 6.0), 4.0, 3.0, (0.4, 1.2, 1.9, 0.5), True),
    "SAN": ("San Diego", 1700, (8.0, 6.0, 6.0, 7.0), 3.5, 2.0, (1.0, 1.0, 1.2, 0.8), True),
    "DEN": ("Denver", 2400, (5.0, 4.0, 4.0, 4.0), 3.5, 1.8, (1.2, 1.0, 1.1, 0.8), True),
    "BNA": ("Nashville", 2000, (3.2, 3.2, 3.2, 3.2), 3.5, 1.9, (0.9, 1.1, 1.0, 1.0), True),
    "WAS": ("Washington", 5700, (2.3, 2.3, 2.3, 2.3), 3.0, 1.3, (0.9, 1.1, 0.9, 1.1), True),
    "NYC": ("New York", 4500, (2.6, 2.6, 2.6, 2.6), 3.0, 1.35, (0.9, 1.0, 1.0, 1.1), True),
    "BOS": ("Boston", 3200, (2.5, 2.5, 2.5, 2.5), 3.0, 1.3, (0.9, 1.0, 1.1, 1.0), True),
    "DFW": ("Dallas", 4400, (2.5, 2.5, 2.5, 2.5), 3.0, 1.3, (1.0, 1.0, 1.0, 1.0), True),
    "HOU": ("Houston", 2200, (2.3, 2.3, 2.3, 2.3), 3.0, 1.25, (1.0, 1.0, 1.0, 1.0), True),
    "CHI": ("Chicago", 5000, (2.2, 2.2, 2.2, 2.2), 3.0, 1.3, (1.0, 1.0, 1.0, 1.0), False),
    "CLT": ("Charlotte", 2500, (3.0, 3.0, 3.0, 3.0), 3.0, 1.4, (1.0, 1.0, 1.0, 1.0), False),
    "DTT": ("Detroit", 2300, (3.0, 3.0, 3.0, 3.0), 3.0, 1.4, (1.0, 1.0, 1.0, 1.0), False),
    "OTH": ("Other", 9000, (6.0, 5.0, 5.0, 6.0), 2.5, 1.7, (1.0, 1.0, 1.0, 1.0), False),
}
# How the party size was written on the card: share of parties of two or more who wrote it as a sum
# ("2+2", "2 adults 2 kids", "me + 1"), by market kind; the contractor keyed the first number.
COMPOUND = {"family": 0.30, "leisure": 0.20, "business": 0.26}
# of the rest, the share who add a word on who the party is ("2 (me and my wife)", "4 (2 adults 2 kids)", "1 (me)")
ANNOTATE = {"family": 0.22, "leisure": 0.18, "business": 0.15}
ANNOTATE_SINGLE = 0.10
KIND = {"TPA": "leisure", "PHX": "leisure", "RSW": "leisure", "ORL": "family", "FLL": "leisure", "LAS": "leisure",
        "MYR": "family", "SAN": "family", "DEN": "leisure", "BNA": "leisure", "WAS": "business", "NYC": "business",
        "BOS": "business", "DFW": "business", "HOU": "business", "CHI": "business", "CLT": "business",
        "DTT": "business", "OTH": "leisure"}
PURPOSE = {"family": (0.04, 0.80, 0.14, 0.02), "leisure": (0.10, 0.68, 0.19, 0.03),
           "business": (0.62, 0.16, 0.18, 0.04)}       # business, leisure, visiting, other

# Parkers who do not live in the service area: their own stay mix, scaled so the lots' entries match the register.
NONSA = {"trips": 800000, "nights": (6.0, 4.5, 4.0, 5.0), "shape": 2.2, "party": 1.6}
QUARTER_ENTRIES = {1: 205000, 2: 240000, 3: 262000, 4: 228000}
HANDOUT_COVER = {1: 0.92, 2: 0.88, 3: 0.71, 4: 0.90}
LOT_COVER = {"Economy C": 1.03, "Economy D": 0.94, "Long-Term": 1.01}       # plaza by plaza
RESPONSE = {1: 0.36, 2: 0.34, 3: 0.33, 4: 0.35}
LOT_RESPONSE = {"Economy C": 0.96, "Economy D": 1.06, "Long-Term": 0.99}

# ------------------------------------------------------------------------------------------------ service area
COUNTIES = {   # county: (ZIP codes, relative population)
    "Kessick": (["47012", "47013", "47015", "47016", "47018", "47020", "47022", "47025"], 0.24),
    "Varden": (["47031", "47033", "47034", "47036", "47038"], 0.12),
    "Hollis": (["47041", "47042", "47045", "47047", "47049", "47050"], 0.13),
    "Tilden": (["47052", "47054", "47055", "47058"], 0.08),
    "Corvel": (["47058", "47061", "47063", "47064", "47066"], 0.10),
    "Ashby": (["47071", "47072", "47075"], 0.06),
    "Renwick": (["47081", "47083", "47084", "47086", "47088", "47089"], 0.12),
    "Stroud": (["47091", "47093", "47095"], 0.07),
    "Marlow": (["47101", "47103", "47104", "47107"], 0.08),
}
PLACES = {   # ZIP: post office name (47058, a rural route office, serves both Tilden and Corvel)
    "47012": "Kessick", "47013": "North Kessick", "47015": "Ferrin", "47016": "Albry", "47018": "Kessick Junction",
    "47020": "Oak Mill", "47022": "Pruett", "47025": "Lodden", "47031": "Varden", "47033": "Cass Hollow",
    "47034": "Embry", "47036": "Little Varden", "47038": "Seddon", "47041": "Hollis", "47042": "Hollis Springs",
    "47045": "Gant", "47047": "Mercer Mill", "47049": "Ryle", "47050": "Ostrander", "47052": "Tilden",
    "47054": "Brack", "47055": "Coyle", "47058": "Pashley", "47061": "Corvel", "47063": "Weyland",
    "47064": "Corvel Falls", "47066": "Upton", "47071": "Ashby", "47072": "Ashby Station", "47075": "Linwood",
    "47081": "Renwick", "47083": "East Renwick", "47084": "Harl", "47086": "Fowley", "47088": "Norbury",
    "47089": "Quell", "47091": "Stroud", "47093": "Ballin", "47095": "Stroud Crossing", "47101": "Marlow",
    "47103": "Iden", "47104": "Marlow Lake", "47107": "Tresham",
}
SA_ZIPS = sorted({z for zs, _ in COUNTIES.values() for z in zs})
# relative population of each ZIP within its county; 47058 is a rural route office on the Tilden and Corvel line
ZIP_WEIGHT = {z: 0.55 + ((int(z) * 37) % 100) / 100.0 for z in SA_ZIPS}
ZIP_WEIGHT["47058"] = 0.12
ZIP_FORMS = (0.0022, 0.0027, 0.0032)     # cumulative: ZIP+4 with a hyphen, nine digits run together, a leading space
# ZIP codes of parkers who live elsewhere: the hub's own region and beyond
NONSA_PREFIXES = ["460", "461", "462", "463", "464", "465", "466", "467", "468", "469", "470", "471", "472", "473",
                  "474", "475", "476", "478", "479", "430", "450", "452", "453", "600", "605", "606", "481", "482"]

# ------------------------------------------------------------------------------------------------ city markets
# market code: (market name, airports with each one's share of the market's trips)
CITY_MARKETS = {
    "TPA": ("Tampa", [("TPA", 0.80), ("PIE", 0.20)]),
    "PHX": ("Phoenix", [("PHX", 0.86), ("AZA", 0.14)]),
    "RSW": ("Fort Myers", [("RSW", 1.0)]),
    "ORL": ("Orlando", [("MCO", 0.91), ("SFB", 0.09)]),
    "FLL": ("Fort Lauderdale", [("FLL", 1.0)]),
    "LAS": ("Las Vegas", [("LAS", 1.0)]),
    "MYR": ("Myrtle Beach", [("MYR", 1.0)]),
    "SAN": ("San Diego", [("SAN", 1.0)]),
    "DEN": ("Denver", [("DEN", 1.0)]),
    "BNA": ("Nashville", [("BNA", 1.0)]),
    "WAS": ("Washington", [("DCA", 0.46), ("IAD", 0.30), ("BWI", 0.24)]),
    "NYC": ("New York", [("LGA", 0.44), ("EWR", 0.31), ("JFK", 0.25)]),
    "BOS": ("Boston", [("BOS", 1.0)]),
    "DFW": ("Dallas", [("DFW", 0.76), ("DAL", 0.24)]),
    "HOU": ("Houston", [("IAH", 0.62), ("HOU", 0.38)]),
    "CHI": ("Chicago", [("ORD", 0.77), ("MDW", 0.23)]),
    "CLT": ("Charlotte", [("CLT", 1.0)]),
    "DTT": ("Detroit", [("DTW", 1.0)]),
}
METRO = {"WAS": "WAS", "NYC": "NYC", "CHI": "CHI"}       # markets a coder codes by metro code when only the city is named
AIRPORT_NAMES = {
    "TPA": "Tampa International", "PIE": "St. Pete-Clearwater International", "PHX": "Phoenix Sky Harbor International",
    "AZA": "Phoenix-Mesa Gateway", "RSW": "Southwest Florida International", "MCO": "Orlando International",
    "SFB": "Orlando Sanford International", "FLL": "Fort Lauderdale-Hollywood International",
    "LAS": "Harry Reid International", "MYR": "Myrtle Beach International", "SAN": "San Diego International",
    "DEN": "Denver International", "BNA": "Nashville International", "DCA": "Ronald Reagan Washington National",
    "IAD": "Washington Dulles International", "BWI": "Baltimore/Washington International",
    "LGA": "LaGuardia", "EWR": "Newark Liberty International", "JFK": "John F. Kennedy International",
    "BOS": "Boston Logan International", "DFW": "Dallas Fort Worth International", "DAL": "Dallas Love Field",
    "IAH": "George Bush Intercontinental", "HOU": "William P. Hobby", "ORD": "Chicago O'Hare International",
    "MDW": "Chicago Midway International", "CLT": "Charlotte Douglas International",
    "DTW": "Detroit Metropolitan Wayne County",
}
# the other destinations (single-airport markets, none on the shortlist)
OTHER_AIRPORTS = [("ATL", "Atlanta", "Hartsfield-Jackson Atlanta International", 0.12),
                  ("MSP", "Minneapolis", "Minneapolis-St. Paul International", 0.06),
                  ("LAX", "Los Angeles", "Los Angeles International", 0.07),
                  ("SFO", "San Francisco", "San Francisco International", 0.05),
                  ("SEA", "Seattle", "Seattle-Tacoma International", 0.05),
                  ("MIA", "Miami", "Miami International", 0.06), ("PHL", "Philadelphia", "Philadelphia International", 0.04),
                  ("SLC", "Salt Lake City", "Salt Lake City International", 0.04),
                  ("MSY", "New Orleans", "Louis Armstrong New Orleans International", 0.05),
                  ("AUS", "Austin", "Austin-Bergstrom International", 0.04),
                  ("SAT", "San Antonio", "San Antonio International", 0.03),
                  ("RDU", "Raleigh-Durham", "Raleigh-Durham International", 0.03),
                  ("SRQ", "Sarasota", "Sarasota Bradenton International", 0.04),
                  ("PBI", "West Palm Beach", "Palm Beach International", 0.04),
                  ("JAX", "Jacksonville", "Jacksonville International", 0.03),
                  ("CUN", "Cancun", "Cancun International", 0.07), ("PUJ", "Punta Cana", "Punta Cana International", 0.04),
                  ("SJU", "San Juan", "Luis Munoz Marin International", 0.03), ("HNL", "Honolulu", "Daniel K. Inouye International", 0.03),
                  ("LHR", "London", "London Heathrow", 0.03), ("CDG", "Paris", "Paris Charles de Gaulle", 0.02),
                  ("PDX", "Portland", "Portland International", 0.02), ("SNA", "Orange County", "John Wayne", 0.02),
                  ("RNO", "Reno", "Reno-Tahoe International", 0.01), ("SAV", "Savannah", "Savannah/Hilton Head International", 0.02)]
# what travellers write for each airport (the card asks the final destination airport or city)
WRITTEN = {
    "TPA": ["Tampa", "TPA", "Tampa Bay", "Tampa FL", "tampa", "Tampa Intl"],
    "PIE": ["St Pete", "St. Petersburg", "Clearwater", "PIE", "St Pete/Clearwater"],
    "PHX": ["Phoenix", "PHX", "Sky Harbor", "Scottsdale", "Phoenix AZ", "phoenix"],
    "AZA": ["Mesa", "Mesa Gateway", "AZA", "Phoenix-Mesa"],
    "RSW": ["Fort Myers", "Ft Myers", "Ft. Myers", "RSW", "Naples", "Cape Coral", "SW Florida"],
    "MCO": ["Orlando", "MCO", "Disney", "Orlando FL", "orlando"],
    "SFB": ["Sanford", "SFB", "Orlando Sanford"],
    "FLL": ["Fort Lauderdale", "Ft Lauderdale", "FLL", "Ft. Lauderdale"],
    "LAS": ["Las Vegas", "Vegas", "LAS", "las vegas"],
    "MYR": ["Myrtle Beach", "MYR", "Myrtle"],
    "SAN": ["San Diego", "SAN"],
    "DEN": ["Denver", "DEN", "denver"],
    "BNA": ["Nashville", "BNA"],
    "DCA": ["Reagan", "DCA", "Washington National", "Reagan National"],
    "IAD": ["Dulles", "IAD"],
    "BWI": ["BWI", "Baltimore"],
    "WAS": ["Washington", "DC", "Washington DC", "Wash DC", "D.C."],
    "LGA": ["LaGuardia", "LGA", "La Guardia"],
    "EWR": ["Newark", "EWR"],
    "JFK": ["JFK", "Kennedy"],
    "NYC": ["New York", "NYC", "New York City", "Manhattan"],
    "BOS": ["Boston", "BOS", "Logan"],
    "DFW": ["Dallas", "DFW", "Dallas/Fort Worth", "Fort Worth"],
    "DAL": ["Love Field", "DAL", "Dallas Love"],
    "IAH": ["Houston", "IAH", "Houston Intercontinental"],
    "HOU": ["Hobby", "HOU", "Houston Hobby"],
    "ORD": ["O'Hare", "ORD", "Chicago O'Hare", "Ohare"],
    "MDW": ["Midway", "MDW", "Chicago Midway"],
    "CHI": ["Chicago", "chicago", "CHI"],
    "CLT": ["Charlotte", "CLT"],
    "DTW": ["Detroit", "DTW", "Detroit Metro"],
}
# the share of each metro market's cards that name only the city (coded by its metro code)
CITY_ONLY = {"WAS": 0.30, "NYC": 0.34, "CHI": 0.28}

# the shortlist the bureau's market review drew up in July 2026 (standard, appendix A)
SHORTLIST = ["TPA", "PHX", "RSW", "ORL", "FLL", "LAS", "MYR", "SAN", "DEN", "BNA", "WAS", "NYC", "BOS", "DFW", "HOU"]

# ------------------------------------------------------------------------------------------------ Kessick Valley's 2027 schedule
KVR_2027 = [   # carrier, flight numbers, destination airport, days, departs, arrives, equipment, effective, discontinued
    ("Lakemont Express", "7L 4410", "ORD", "Daily", "06:05", "06:14", "E175", "", ""),
    ("Lakemont Express", "7L 4418", "ORD", "Daily", "13:40", "13:49", "E175", "", ""),
    ("Lakemont Express", "7L 4422", "ORD", "Daily ex Sat", "17:55", "18:04", "E175", "", ""),
    ("Brightwater Connection", "4B 5233", "CLT", "Daily", "06:30", "08:16", "CRJ-900", "", ""),
    ("Brightwater Connection", "4B 5241", "CLT", "Daily", "15:10", "16:55", "CRJ-900", "", ""),
    ("Ridgeline Connection", "9R 3702", "DTW", "Daily", "06:45", "07:58", "CRJ-700", "", ""),
    ("Ridgeline Connection", "9R 3718", "DTW", "Daily ex Sat", "16:20", "17:33", "CRJ-700", "", ""),
    ("Sunstream Air", "5S 801", "SFB", "Thu Sun", "10:15", "12:46", "A320", "2027-02-11", "2027-04-25"),
]
SERVED_MARKETS = sorted({next(m for m, (n, a) in CITY_MARKETS.items() if any(ap == r[2] for ap, _ in a))
                         for r in KVR_2027})

FILES = {
    "cards": "brennick_parking_survey_2026_cards.csv",
    "verbatims": "brennick_parking_survey_2026_verbatims.csv",
    "handout": "brennick_parking_survey_2026_handout_log.pdf",
    "methods": "brennick_parking_survey_2026_methods_report.pdf",
    "q1": "brennick_parcs_daily_entries_2026q1.csv",
    "q2": "brennick_parcs_daily_entries_2026q2.csv",
    "q3": "brennick_parcs_daily_entries_2026q3.csv",
    "q4": "brennick_parcs_daily_entries_2026q4.csv",
    "zips": "kvr_service_area_zip_codes.csv",
    "markets": "bureau_city_markets.csv",
    "schedule": "kvr_nonstop_schedule_2027.pdf",
    "standard": "bureau_air_service_pitch_standard_2027.pdf",
    "rates": "brennick_public_parking_rates_2026.pdf",
    "tickets": "kvr_db1b_market_2026q1_q3.csv",
    "t100": "kvr_t100_segments_2026.csv",
    "access": "brennick_ground_access_survey_2025.xlsx",
}
GOLDEN = {"csv": "kvr_2027_pitch_markets.csv", "brief": "kvr_2027_route_pitch_brief.docx"}
CANDIDATES = [m for m in SHORTLIST if m not in SERVED_MARKETS]
DISTRACTORS = ["tickets", "t100", "access"]
WRONG_BASIS = "tickets"
