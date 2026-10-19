"""task248 parameters: the public health service, its 24 wastewater treatment plants, the seasons, and the keys every
module reads."""
import datetime as dt

SEED = 0               # records and documents
SIM_SEED = 31          # temperatures, shedding, the samples and the paired study

REGION = "Southern Plains"
SERVICE = "Southern Plains Public Health Service"
SERVICE_SHORT = "SPPHS"
LAB = "Southern Plains Public Health Laboratory"
WATER = "Southern Plains Water"
DASHBOARD = "Wastewater Dashboard"

FIRST_DAY = dt.date(2026, 1, 5)            # a Monday
LAST_DAY = dt.date(2028, 4, 9)             # the Sunday before the as-of week
ASOF = dt.date(2028, 4, 12)
CUTOVER = dt.date(2028, 5, 1)
REF = (dt.date(2026, 4, 6), dt.date(2027, 3, 29))        # Monday weeks of the reference year for winter 2027
WINTER = (dt.date(2027, 5, 3), dt.date(2027, 9, 27))     # Monday weeks of winter 2027
STUDY = (dt.date(2026, 2, 2), dt.date(2027, 1, 25))      # the paired upstream study

HIGH, LOW = 1.0, 0.5       # an episode opens at High and closes when the level is back at Low
VERY_HIGH = 1.5

# the sewer's decay of SARS-CoV-2 RNA: first order, rate per hour rising with the water's temperature
K20, THETA = 0.05, 1.09
K_PMMOV = 0.0015           # the faecal marker barely decays

# people (guard.py names --geo "New Zealand" --seed 248)
COORDINATOR = ("Fiona Chandler", "fiona.chandler")          # wastewater surveillance coordinator, rosters the desk
SCIENTIST = ("Luke Jefferies", "luke.jefferies")            # molecular laboratory
MODELLER = ("Craig Stuart", "craig.stuart")                 # network modeller, the travel times
FIELD = ("Alana Costello", "alana.costello")                # ran the paired upstream study
DOMAIN = "spphs.health.nz"
WATER_DOMAIN = "spwater.co.nz"

# the plants: code, plant name, town(s) it serves, people served (the register), population-weighted travel time (minutes)
PLANTS = [
    ("ASD", "Ashgrove Downs", "Ashgrove Downs", 6840, 38),
    ("BRK", "Brackenridge", "Brackenridge", 12410, 95),
    ("CRF", "Carrisford", "Carrisford and Lowe's Corner", 3920, 52),
    ("DNK", "Dunkerley", "Dunkerley", 17880, 140),
    ("FNK", "Fennick", "Fennick", 2310, 27),
    ("GLO", "Glenorrin", "Glenorrin", 8960, 118),
    ("HOL", "Hollinsbury", "Hollinsbury", 21470, 205),
    ("INB", "Inverbrack", "Inverbrack and Moss Hill", 5150, 74),
    ("KSB", "Kestrel Bay", "Kestrel Bay", 14230, 318),
    ("LRF", "Larchfield", "Larchfield", 26690, 455),
    ("MRB", "Marrowby", "Marrowby", 9340, 362),
    ("NTL", "Netherleigh", "Netherleigh and Pell Valley", 31580, 610),
    ("ORB", "Orrin Bay", "Orrin Bay", 11760, 404),
    ("PLH", "Pellingham", "Pellingham", 42150, 688),
    ("QRM", "Quarrymoor", "Quarrymoor", 18520, 525),
    ("RVG", "Ravensgill", "Ravensgill", 23940, 578),
    ("ADN", "Ardenmouth North", "Ardenmouth's north and Brookhallow", 118400, 1065),
    ("ADS", "Ardenmouth South", "Ardenmouth's south", 142900, 1310),
    ("ADE", "Ardenmouth East", "Ardenmouth's east and Yarrowfield", 86300, 1495),
    ("ADW", "Ardenmouth West", "Ardenmouth's west and Wexcombe", 64750, 905),
    ("TRN", "Tarnbrook", "Tarnbrook and the coast road", 38240, 1180),
    ("UWD", "Upper Waldon", "Upper Waldon", 29610, 960),
    ("CLF", "Cleaveland Flat", "Cleaveland Flat", 47830, 1615),
    ("SLT", "Saltmarsh Point", "Saltmarsh Point", 35920, 1420),
]
NPLANT = len(PLANTS)
