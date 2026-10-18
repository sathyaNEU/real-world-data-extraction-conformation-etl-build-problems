"""task246 constants: Laga County's 2027 long-rains nutrition surveillance round (a fictional arid county in northern
Kenya), its twelve survey zones, the two partners' twelve survey teams and their anthropometrists, the standardisation
test, the fieldwork calendar and the households behind the asks. Every figure the golden owes is computed from the
pack; these only drive the simulation."""
import datetime as dt

SEED = 246
COUNTY = "Laga"
COUNTY_GOV = "County Government of Laga"
DEPT = "Department of Health Services"
UNIT = "County Nutrition Unit"
EWU = "County Drought Early Warning Unit"
PARTNER = {"A": "Northlands Child Health Alliance", "B": "Plainsfield Relief Kenya"}
PARTNER_SHORT = {"A": "NCHA", "B": "PRK"}

CUT = 125.0            # mm, acute malnutrition by MUAC (children 6 to 59 months)
NOTE_POINTS = 2.0      # the measurement note
BANDS = [(0.0, "Normal"), (5.0, "Alert"), (10.0, "Alarm"), (15.0, "Emergency")]

# ------------------------------------------------------------------ zones
# code, name, sub-county, own MUAC mean (mm) at age 33 months for a boy, child sd within cluster, cluster sd
ZONES = [
    ("NP", "North Pastoral", "Laga North", 140.63, 9.6, 2.1),
    ("NA", "North Agro-pastoral", "Laga North", 141.34, 9.8, 2.2),
    ("NL", "North Lakeshore", "Laga North", 136.81, 9.4, 2.0),
    ("CP", "Central Pastoral", "Laga Central", 138.62, 9.7, 2.3),
    ("CA", "Central Agro-pastoral", "Laga Central", 141.94, 9.9, 2.1),
    ("LT", "Laga Town", "Laga Central", 141.10, 9.5, 2.2),
    ("EP", "East Pastoral", "Laga East", 139.87, 9.6, 2.2),
    ("ER", "East Riverine", "Laga East", 142.79, 9.7, 2.1),
    ("EA", "East Agro-pastoral", "Laga East", 142.43, 10.0, 2.0),
    ("WP", "West Pastoral", "Laga West", 136.54, 9.3, 2.2),
    ("WA", "West Agro-pastoral", "Laga West", 141.77, 9.8, 2.1),
    ("WR", "West Riverine", "Laga West", 137.22, 9.5, 2.0),
]
ZCODES = [z[0] for z in ZONES]
ZNAME = {z[0]: z[1] for z in ZONES}
CLUSTERS_PER_ZONE = 20
HH_PER_CLUSTER = 15
ZONE_SHIFT = {}         # tune.py only: a trial shift of a zone's own mean (mm); the shipped means carry it
MOVE_EVENTS = 0.035     # a household's children leaving with their mother or to another caregiver (rate)
AWAY_SALT = 25          # the generator key of where each death happened (chosen with MOVER_SALT, see tune.py)
MOVER_SALT = 21         # the movers' generator key (chosen with AWAY_SALT, see tune.py)
AGE_SLOPE = 0.22       # mm per month of age
GIRL = -1.1            # mm

# ------------------------------------------------------------------ anthropometrists
# id: (partner, team number, name, offset mm, child-to-child sd mm, repeat sd mm, share of readings heaped to 5 mm)
MEASURERS = {
    "A1": ("A", 1, "Titus Ouma", -2.2, 2.5, 0.8, 0.0),
    "A2": ("A", 2, "Centrine Kinya", 0.4, 2.0, 0.7, 0.0),
    "A3": ("A", 3, "Steve Abdikadir", -0.3, 5.6, 1.2, 0.30),
    "A4": ("A", 4, "Halima Mohamud", -0.5, 2.4, 0.9, 0.0),
    "A5": ("A", 5, "Pius Kiplangat", 2.9, 2.2, 1.1, 0.0),
    "A6": ("A", 6, "Diana Kilonzo", 0.2, 2.7, 0.8, 0.0),
    "B1": ("B", 1, "Edwin Njoroge", -0.3, 1.9, 0.6, 0.0),
    "B2": ("B", 2, "Betty Jepchumba", -2.8, 2.8, 1.0, 0.0),
    "B3": ("B", 3, "Emmanuel Mutemi", -2.4, 2.1, 1.2, 0.0),
    "B4": ("B", 4, "Albert Bosire", 3.6, 1.8, 0.7, 0.0),
    "B4s": ("B", 4, "Sharon Kinuthia", -3.9, 2.1, 0.9, 0.0),
    "B5": ("B", 5, "Cosmas Kibet", -0.4, 6.1, 1.0, 0.40),
    "B6": ("B", 6, "Joan Bashir", -0.2, 5.0, 0.9, 0.25),
}
# the test estimates the generator lands on (offset, field error variance), within tolerance
TEST_TARGET = {"A1": (-2.2, 6.9), "A2": (0.4, 4.5), "A3": (-0.3, 33.0), "A4": (-0.5, 6.6), "A5": (2.9, 6.0),
               "A6": (0.2, 8.0), "B1": (-0.3, 4.0), "B2": (-2.8, 8.8), "B3": (-2.4, 5.9), "B4": (3.6, 3.7),
               "B4s": (-3.9, 5.2), "B5": (-0.4, 39.0), "B6": (-0.2, 26.3)}
SUPERVISOR = ("Purity Maina", 0.5)       # name, repeat sd mm

TEAM_LEADERS = {"A1": "Timothy Sheikh", "A2": "Karanja Kamau", "A3": "Lavender Mohamed", "A4": "Hellen Nyamweya",
                "A5": "Millicent Wanjiku", "A6": "Kipkirui Hassan", "B1": "Margret Juma", "B2": "Kevin Cherotich",
                "B3": "Collins Mungai", "B4": "Pauline Muriithi", "B5": "James Munyao", "B6": "Brian Mbugua"}

# zone -> [(team, number of clusters)], clusters taken in the order listed
ALLOCATION = {
    "NP": [("A1", 20)], "NA": [("A2", 20)], "NL": [("A3", 20)], "CP": [("A5", 20)],
    "CA": [("A6", 10), ("A4", 10)], "LT": [("B2", 20)], "EP": [("B3", 20)], "ER": [("B4", 20)],
    "EA": [("A4", 10), ("B1", 10)], "WP": [("B6", 20)], "WA": [("A6", 10), ("B1", 10)], "WR": [("B5", 20)],
}

# ------------------------------------------------------------------ calendar
TRAINING_TEST = dt.date(2027, 6, 10)      # standardisation session 1
FIELD_START = dt.date(2027, 6, 14)
REFRESHER = dt.date(2027, 6, 28)          # standardisation session 2, morning
SUBSTITUTION = dt.date(2027, 6, 28)       # team B4's new anthropometrist from this date
FIELD_END = dt.date(2027, 7, 8)
REPORT_DATE = dt.date(2027, 7, 21)        # the round's figures to the bulletin desk
ASOF = dt.date(2027, 7, 21)

# recall period start events (mortality), by sub-county
RECALL_START = {"Laga North": (dt.date(2027, 3, 28), "Easter Sunday"),
                "Laga Central": (dt.date(2027, 3, 28), "Easter Sunday"),
                "Laga East": (dt.date(2027, 3, 10), "Eid al-Fitr"),
                "Laga West": (dt.date(2027, 3, 10), "Eid al-Fitr")}
