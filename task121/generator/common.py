"""Constants for task121 (architecture 4): Marlvale Trains' customer satisfaction recovery plan.

    The world: a train operating company running five service groups out of Marlvale Central under a contract with
    the Western Rail Partnership. Its customer satisfaction tracker (run by an agency, in-train self-completion)
    fell between the spring 2025 and spring 2026 waves; the recovery plan funds the remedy for one of four service
    drivers. The operating records (timetables, train movements, load-weigh, formations, crew, fares) cover both
    waves and the four weeks to 19 September 2026, the plan's baseline window."""
import datetime as dt

SEED = 121
ASSEMBLED = dt.datetime(2026, 10, 23, 15, 20)

OPERATOR = "Marlvale Trains"
OPERATOR_LTD = "Marlvale Trains Limited"
AUTHORITY = "Western Rail Partnership"
AGENCY = "Harcourt Rowe Research"
TRACKER = "Customer Satisfaction Tracker"

D = dt.date
WAVES = {2025: (D(2025, 3, 3), D(2025, 4, 13)), 2026: (D(2026, 3, 2), D(2026, 4, 12))}
LATEST = (D(2026, 8, 23), D(2026, 9, 19))          # Sunday 23 August to Saturday 19 September 2026
TIMETABLE_CHANGE = D(2025, 12, 14)                  # the December 2025 timetable
CASCADE = D(2025, 10, 19)                           # six class 166 units off lease, eight class 150 units in
CREW_SYSTEM_MOVE = D(2026, 5, 17)                   # the as-worked archive ends; the new rostering platform starts
PLAN_DUE = D(2026, 11, 20)
BANK_HOLIDAYS = {D(2026, 4, 3), D(2026, 4, 6), D(2026, 8, 31)}      # Sunday timetable on each


def days(a, b):
    return [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]


WINDOWS = {"w2025": days(*WAVES[2025]), "w2026": days(*WAVES[2026]), "latest": days(*LATEST)}
ALL_DAYS = WINDOWS["w2025"] + WINDOWS["w2026"] + WINDOWS["latest"]

# service groups: code, name, headcode prefix, terminal station, stations outward from the first (minutes from it)
GROUPS = {
    "MAIN": dict(name="Marlvale Main Line", prefix="1M", calls=[
        ("MVC", 0), ("ASP", 9), ("KST", 21), ("WXC", 34), ("TRG", 49)]),
    "VALE": dict(name="Hollin Vale", prefix="2H", calls=[
        ("MVC", 0), ("MVN", 5), ("HBK", 11), ("FRN", 17), ("SDB", 24), ("CWT", 31), ("BRH", 38), ("HLF", 46)]),
    "COAST": dict(name="Coastway", prefix="2C", calls=[
        ("MVC", 0), ("MVS", 6), ("LNG", 15), ("STC", 24), ("SEN", 33), ("PNB", 44), ("CRW", 55), ("TRV", 66)]),
    "BRANCH": dict(name="Pellow Branch", prefix="2P", calls=[
        ("SEN", 0), ("GLD", 6), ("MSH", 12), ("TRN", 18), ("PLW", 25)]),
    "LINK": dict(name="Corrington Link", prefix="2L", calls=[
        ("MVC", 0), ("ASP", 9), ("OKB", 19), ("FEN", 29), ("RDL", 40), ("CRG", 54)]),
}
GROUP_ORDER = ["MAIN", "VALE", "COAST", "BRANCH", "LINK"]
INTO_MVC = ["MAIN", "VALE", "COAST", "LINK"]

STATIONS = {
    "MVC": "Marlvale Central", "ASP": "Ashcombe Parkway", "KST": "Kelstow", "WXC": "Wexley Cross",
    "TRG": "Tregarrow", "MVN": "Marlvale North", "HBK": "Holbeck Lane", "FRN": "Farnley Green", "SDB": "Sedbury",
    "CWT": "Coldwater", "BRH": "Broadhurst", "HLF": "Hollinford", "MVS": "Marlvale South", "LNG": "Langtry",
    "STC": "St Cleer Road", "SEN": "Sennow", "PNB": "Pennick Bay", "CRW": "Carrow Sands", "TRV": "Trevose Quay",
    "GLD": "Gildon", "MSH": "Morsham", "TRN": "Tarnwell", "PLW": "Pellow", "OKB": "Oakbridge", "FEN": "Fenwick",
    "RDL": "Radley Moor", "CRG": "Corrington",
}

# fleet: class, vehicles, standard seats (the units carry no first class)
CLASSES = {"150/2": (2, 116), "158": (2, 138), "158/9": (2, 126), "166": (3, 232)}

# the tracker: the overall question and the ten attribute ratings (Q5k Wi-Fi added in 2026)
ITEMS = [("q5a", "punctuality and reliability of the train"), ("q5b", "length of time the journey was scheduled to take"),
         ("q5c", "frequency of the trains on that route"), ("q5d", "cleanliness of the inside of the train"),
         ("q5e", "comfort of the seating area"), ("q5f", "availability of staff on the train"),
         ("q5g", "helpfulness and attitude of staff on the train"), ("q5h", "information provided during the journey"),
         ("q5i", "value for money of the ticket"), ("q5j", "personal security on board")]
ITEM_2026 = ("q5k", "the Wi-Fi on the train")
TICKETS = ["Season", "Anytime", "Off-Peak", "Advance"]
FARE_CHANGE = {"Season": 3.0, "Anytime": 4.5, "Off-Peak": -4.0, "Advance": -8.0}   # per cent, 4 January 2026
TIME_BANDS = ["Weekday morning peak", "Weekday inter-peak", "Weekday evening peak", "Weekday evening", "Weekend"]

# the truth: the chance a passenger is satisfied overall, linear in the journey's conditions
P_BASE = 0.902
EFFECT = {"crowded": -0.310, "late": -0.150, "unstaffed": -0.036, "fare": -0.0003}
LATE_MIN = 5                                        # minutes after the timetable at the passenger's station

PEOPLE = {"contract": "Naomi Stanley", "agency": "Mohamed Hussain", "fleet": "Zoe Williamson",
          "authority": "Bernard Burrows"}

FILES = {
    "responses": "cst_responses_spring2025_spring2026.csv",
    "fieldwork": "cst_fieldwork_log_spring2025_spring2026.csv",
    "technote": "cst_technical_note_spring2026.pdf",
    "topline": "cst_topline_report_spring2026.pdf",
    "requirement": "wrp_recovery_plan_requirement_2026.pdf",
    "standards": "service_quality_measures_schedule7.pdf",
    "timetable": "working_timetable_dec2024_dec2025.csv",
    "movements": "train_movements_2025_2026.csv",
    "loadweigh": "loadweigh_departures_2025_2026.csv",
    "formations": "daily_formations_2025_2026.csv",
    "fleet": "fleet_register_2026.xlsx",
    "crew_worked": "onboard_crew_as_worked_mar2025_apr2026.csv",
    "crew_roster": "onboard_roster_aug_sep_2026.csv",
    "crew_amend": "onboard_roster_amendments_aug_sep_2026.csv",
    "fares": "fares_change_jan2026.csv",
    "stations": "station_reference.csv",
    "contacts": "customer_contacts_2025_2026.csv",
    "delays": "delay_attribution_spring2026.csv",
    "dictionary": "operating_extracts_field_notes.txt",
}
DISTRACTORS = ["contacts", "delays"]
GOLDEN = "satisfaction_fall_spring2026.xlsx"
CHART = "satisfaction_bridge_spring2026.png"
DELIVERABLES = [GOLDEN, CHART]
