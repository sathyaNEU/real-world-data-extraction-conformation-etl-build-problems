"""The world of task470: the Corrisan Valley Air Quality District, its 30 public-use general aviation fields, the
aircraft based on them and the district's 2026 inventory of lead from piston airplanes.

Field archetypes carry the design targets: heard piston lead (kg) from the based and visiting aircraft that
broadcast, never-heard based piston airplanes, and the unrecorded operations per such airplane at each field.
"""
import datetime as dt

DISTRICT = "Corrisan Valley Air Quality District"
DISTRICT_SHORT = "CVAQD"
STATE_OFFICE = "State Office of Aeronautics"
YEAR = 2026
AS_OF = dt.date(2027, 2, 12)           # the qualification memo's working date
REGISTER_DATE = dt.date(2027, 2, 1)    # the FAA register extract the district pulled
BASED_DATE = dt.date(2027, 1, 1)       # the state's based aircraft validation
EXPORT_DATE = dt.date(2027, 1, 8)      # the receiver network's export
BOARD_DATE = dt.date(2027, 3, 10)      # the governing board adopts the 2027 grant round

# US Pacific time: PST UTC-8, PDT UTC-7 from 2026-03-08 10:00Z to 2026-11-01 09:00Z
DST_START = dt.datetime(2026, 3, 8, 10, 0)
DST_END = dt.datetime(2026, 11, 1, 9, 0)


def utc_offset(utc_naive):
    return -7 if DST_START <= utc_naive < DST_END else -8


def to_local(utc_naive):
    return utc_naive + dt.timedelta(hours=utc_offset(utc_naive))


def to_utc(local_naive):
    # local wall time to UTC (the generator never schedules an event in the skipped or repeated hour)
    guess = local_naive + dt.timedelta(hours=8)
    off = utc_offset(guess)
    return local_naive - dt.timedelta(hours=off)


# lead per operation, grams, from the district's method (Table 2)
LEAD = {("single", "departure"): 2.30, ("single", "arrival"): 0.95, ("single", "touch_and_go"): 0.55,
        ("multi", "departure"): 5.60, ("multi", "arrival"): 2.25, ("multi", "touch_and_go"): 1.35}
LEAD_UNRECORDED = 1.625          # an operation the network did not record: the single-engine full-stop mean
THRESHOLD_KG = 12.5

PEOPLE = {
    "planner": ("Jeanette Steele", "Air Toxics Planner"),
    "network": ("Yolanda Cortez", "Air Quality Specialist, Receiver Network"),
    "grants": ("Tonya Krause", "Grants Program Manager"),
}

COUNTIES = ["Corrisan", "Halwick", "Ostrey", "Varnell"]

# name, LID, county, kind, towered, counted, B (based piston airplanes), ND (never-heard based piston airplanes),
# H target (heard piston lead, kg), school fleet, turbines based, helicopters based
# kinds: tower, school, ord (ordinary), vint (an older, privately flown fleet), park (a modern airpark)
FIELDS = [
    ("Halwick Municipal", "HWK", "Halwick", "tower", True, True, 230, 46, 16.77, 14, 9, 3),
    ("Corrisan Valley Regional", "CRV", "Corrisan", "tower", True, True, 190, 39, 13.79, 0, 16, 4),
    ("Ostrey Field", "OSY", "Ostrey", "tower", True, True, 210, 42, 18.33, 18, 6, 2),
    ("Varnell County Airport", "VNL", "Varnell", "tower", True, True, 160, 41, 11.54, 6, 5, 1),
    ("Kesterly Field", "KTY", "Corrisan", "tower", True, True, 150, 35, 11.96, 8, 4, 2),
    ("Dunmore Municipal", "DMR", "Halwick", "tower", True, True, 130, 36, 9.075, 0, 3, 1),
    ("Fennick Airpark", "F37", "Corrisan", "ord", False, True, 150, 30, 10.66, 0, 3, 1),
    ("Lanthorne Field", "L08", "Halwick", "school", False, True, 105, 2, 15.86, 13, 1, 0),
    ("Graylow Municipal", "G42", "Ostrey", "ord", False, True, 115, 29, 7.04, 0, 1, 0),
    ("Dunmarsh Airport", "D19", "Varnell", "ord", False, True, 95, 38, 4.64, 0, 0, 0),
    ("Tavish Aero Field", "T61", "Corrisan", "school", False, False, 89, 1, 10.78, 9, 0, 0),
    ("Pellow Municipal", "P05", "Halwick", "school", False, False, 83, 1, 11.0, 9, 1, 0),
    ("Saltry Field", "S27", "Ostrey", "school", False, False, 38, 0, 11.08, 7, 0, 0),
    ("Umber Creek Airport", "U44", "Varnell", "vint", False, False, 224, 65, 7.51, 0, 1, 0),
    ("Orrin Flats Airport", "O16", "Ostrey", "vint", False, False, 180, 62, 7.14, 0, 0, 0),
    ("Wickrow Airfield", "W33", "Halwick", "vint", False, False, 138, 58, 7.62, 0, 1, 0),
    ("Yarrow Bend Strip", "Y02", "Varnell", "vint", False, False, 60, 22, 3.66, 0, 0, 0),
    ("Ambrell County Airport", "A71", "Corrisan", "ord", False, False, 210, 26, 17.92, 0, 5, 1),
    ("Norwick Field", "N26", "Ostrey", "ord", False, False, 95, 9, 8.95, 0, 0, 0),
    ("Thornacre Regional", "T13", "Varnell", "ord", False, False, 230, 33, 18.42, 0, 6, 2),
    ("Kestrel Ridge Airpark", "K58", "Corrisan", "park", False, False, 93, 2, 10.85, 0, 2, 0),
    ("Zellner Field", "Z14", "Halwick", "ord", False, False, 60, 8, 4.91, 0, 0, 0),
    ("Hollin Gap Airport", "H52", "Varnell", "ord", False, False, 120, 11, 7.87, 0, 1, 0),
    ("Marsh Hollow Field", "M09", "Ostrey", "ord", False, False, 50, 8, 3.3, 0, 0, 0),
    ("Cobbett Airport", "C66", "Corrisan", "ord", False, False, 88, 11, 6.93, 0, 1, 0),
    ("Brannoch Airstrip", "B48", "Halwick", "ord", False, False, 35, 5, 2.56, 0, 0, 0),
    ("Dellow Strip", "D73", "Ostrey", "ord", False, False, 25, 3, 1.49, 0, 0, 0),
    ("Ravelle Field", "R31", "Varnell", "ord", False, False, 45, 4, 3.405, 0, 0, 0),
    ("Wenmore Airport", "W85", "Corrisan", "ord", False, False, 150, 18, 6.95, 0, 2, 0),
    ("Lissom Field", "L29", "Halwick", "ord", False, False, 66, 9, 4.77, 0, 0, 0),
]
FIELD_KEYS = ["name", "lid", "county", "kind", "towered", "counted", "B", "ND", "H", "school", "turbines", "helos"]
F = [dict(zip(FIELD_KEYS, f)) for f in FIELDS]
BY_LID = {f["lid"]: f for f in F}
TOWERED = [f["lid"] for f in F if f["towered"]]
COUNTED = [f["lid"] for f in F if f["counted"]]
STUDIED = [f["lid"] for f in F if f["counted"] and not f["towered"]]
UNTOWERED = [f["lid"] for f in F if not f["towered"]]

K_TARGET = 70.0                     # unrecorded operations per never-heard based piston airplane
K_EPS = {"HWK": 0.022, "CRV": -0.068, "OSY": 0.0165, "VNL": -0.035, "KTY": 0.0255, "DMR": -0.057,
         "F37": 0.01, "L08": 0.05, "G42": -0.05, "D19": 0.02}

# tower hours, local: open, close; winter hours (November to February) where a tower keeps them
TOWER_HOURS = {"HWK": ((7, 0), (21, 0), None), "CRV": ((6, 0), (22, 0), None), "OSY": ((7, 0), (21, 0), None),
               "VNL": ((7, 0), (21, 0), ((7, 0), (19, 0))), "KTY": ((7, 0), (20, 0), None),
               "DMR": ((7, 0), (20, 0), ((7, 0), (18, 0)))}
CONTRACT_TOWERS = ["VNL", "DMR"]          # closed on 25 December and 1 January
WINTER_MONTHS = (11, 12, 1, 2)


def tower_open(lid, local_dt):
    """True when the field's tower is open at this local time."""
    if lid not in TOWER_HOURS:
        return False
    d = local_dt.date()
    if lid in CONTRACT_TOWERS and (d.month, d.day) in ((12, 25), (1, 1)):
        return False
    o, c, wint = TOWER_HOURS[lid]
    if wint and local_dt.month in WINTER_MONTHS:
        o, c = wint
    m = local_dt.hour * 60 + local_dt.minute
    return o[0] * 60 + o[1] <= m < c[0] * 60 + c[1]


# private-use strips in the valley (on the state's based aircraft list, outside the program and the inventory)
STRIPS = [("6V2", "Halvard Ranch Strip", "Varnell"), ("9H1", "Teague Orchard Airstrip", "Halwick"),
          ("3O8", "Moraine Creek Strip", "Ostrey"), ("7K5", "Cassel Farms Airstrip", "Corrisan"),
          ("2C9", "Bellweather Strip", "Corrisan"), ("8W4", "Quarry Flat Strip", "Halwick")]

STUDY_FIRMS = {"F37": "Ardley Counts LLC", "L08": "Pellam Airfield Services", "G42": "Northfork Airport Planning",
               "D19": "Ardley Counts LLC"}

FILES = {
    "events": "adsb_field_events_20251230_20270102.csv",
    "master": "MASTER.txt",
    "dereg": "DEREG.txt",
    "acftref": "ACFTREF.txt",
    "engine": "ENGINE.txt",
    "reg_notes": "cvaqd_faa_register_extract_notes.pdf",
    "based": "state_based_aircraft_validation_2027.xlsx",
    "atct": "atct_daily_operations_2026.csv",
    "f37": "F37_2026_operations_count_report.pdf",
    "l08": "L08_2026_operations_count.xlsx",
    "g42": "G42_2026_activity_count.pdf",
    "d19": "D19_2026_daily_counts.xlsx",
    "method": "cvaqd_aircraft_lead_inventory_method_rev3.pdf",
    "grants": "cvaqd_2027_unleaded_avgas_transition_grants.pdf",
    "network": "cvaqd_adsb_receiver_network_notes.pdf",
    "directory": "state_airport_directory_2026.xlsx",
    "m5010": "airport_master_records_5010.xlsx",
    "pbmon": "cvaqd_lead_monitoring_2026.csv",
}
DISTRACTORS = ["m5010", "pbmon"]
WRONG_BASIS = "m5010"
GOLDEN = {"csv": "corrisan_2026_field_piston_lead.csv", "memo": "cvaqd_2027_unleaded_grant_qualification.docx"}
METHOD_ID = "CVAQD-AQ-17"
