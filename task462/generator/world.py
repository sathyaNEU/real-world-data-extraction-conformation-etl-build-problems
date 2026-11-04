"""The world of task462: Rannikon Lämpö Oy's harbour power plant, its coal yard, its survey contractors, its yard
systems and its coal supply. Every constant the generator draws from lives here."""
import datetime as dt
import zoneinfo

SEED = 4627
ORG = "Rannikon Lämpö Oy"
PLANT = "Satama power plant"
FI = zoneinfo.ZoneInfo("Europe/Helsinki")
UTC = dt.timezone.utc

# ----------------------------------------------------------------------------------------------- the yard (plant grid)
X0, Y0 = 2000.0, 1000.0           # plant grid origin of the yard window (metres)
YARD_W, YARD_H = 400.0, 230.0     # the fenced yard, plant grid
PAD = 2.40                        # yard pad level as built, N60
ANGLE = 36.0                      # coal slope as the dozers leave it, degrees
# area, centre (local x, y), length (x), width (y), crest height above the pad as built, bowl depth (N60 m), coal
PILES = [
    ("P1", 70.0, 58.0, 120.0, 40.0, 12.5, 1.95, "KH-COL"),
    ("P2", 70.0, 172.0, 120.0, 40.0, 12.0, 1.60, "KH-COL"),
    ("P3", 205.0, 58.0, 110.0, 40.0, 12.5, 2.15, "KH-POL"),
    ("P4", 205.0, 172.0, 110.0, 40.0, 12.0, 1.45, "KH-USA"),
    ("P5", 330.0, 58.0, 100.0, 38.0, 11.5, 1.85, "KH-POL"),
    ("P6", 330.0, 172.0, 100.0, 38.0, 11.5, 0.00, "KH-USA"),
]
SKIRT = 2.5                       # the bowl reaches this far past the pile area's outline
AREA_PAD = 10.0                   # each pile area owns the yard to half the 20 m gap to the next

# ----------------------------------------------------------------------------------------------- the two grids
THETA_DEG = 21.437                # the plant grid's x axis, anticlockwise from grid east of ETRS-TM35FIN
E0, N0 = 286415.12, 7035268.40    # ETRS-TM35FIN of the plant grid point (X0, Y0)
DH = 0.384                        # N2000 = N60 + DH at the yard (levelled at the plant benchmarks)
A_CELL = 2.0                      # contractor A: ESRI ASCII grid on the plant grid, N60
B_STEP = 1.5                      # contractor B: XYZ lattice on ETRS-TM35FIN, N2000
A_NOISE, B_NOISE = 0.012, 0.015

# ----------------------------------------------------------------------------------------------- surveys
# (survey date, flight start, flight end) in Finnish time; index 0 is December 2025
SURVEYS = [
    ("2025-12-17", "10:05", "11:32"), ("2026-01-14", "10:20", "11:41"), ("2026-02-11", "09:55", "11:18"),
    ("2026-03-18", "09:10", "10:36"), ("2026-04-15", "08:45", "10:02"), ("2026-05-13", "08:30", "09:51"),
    ("2026-06-17", "08:15", "09:40"), ("2026-07-15", "07:50", "09:02"), ("2026-08-12", "08:05", "09:12"),
    ("2026-09-16", "08:40", "09:47"), ("2026-10-14", "09:20", "10:31"), ("2026-11-18", "10:10", "11:24"),
    ("2026-12-16", "09:40", "10:52"),
]
CONTRACTOR_A = "Mittaus-Saarinen Oy"
CONTRACTOR_B = "Pohjoisen Dronekartoitus Oy"
B_FROM = 7                        # survey index of contractor B's first flight (July 2026)
DEC = 12

# fill of each pile area's length at each survey (stacked from the west end), and the crest height that month
FILL = {
    "P1": [1.0, 0.62, 0.28, 0.0, 0.22, 0.58, 0.95, 1.0, 1.0, 1.0, 1.0, 1.0, 0.990],
    "P2": [1.0, 1.0, 0.88, 0.47, 0.0, 0.36, 0.82, 1.0, 1.0, 1.0, 1.0, 1.0, 0.996],
    "P3": [1.0, 1.0, 1.0, 1.0, 0.93, 0.52, 0.0, 0.43, 0.70, 1.0, 1.0, 1.0, 0.988],
    "P4": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.80, 0.0, 0.49, 0.988],
    "P5": [1.0, 1.0, 1.0, 0.86, 0.41, 0.0, 0.48, 0.93, 1.0, 1.0, 1.0, 1.0, 0.999],
    "P6": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.78, 1.0, 1.0, 0.84, 0.97, 0.992],
}
HEIGHT = {
    "P1": [12.2, 12.1, 11.9, 0, 9.8, 11.7, 12.3, 12.4, 12.4, 12.3, 12.5, 12.4, 12.3],
    "P2": [11.8, 11.9, 11.7, 11.6, 0, 11.2, 11.8, 12.0, 11.9, 11.9, 11.8, 11.9, 11.7],
    "P3": [12.4, 12.3, 12.3, 12.2, 12.1, 12.0, 0, 11.6, 12.1, 12.3, 12.4, 12.3, 12.2],
    "P4": [11.9, 11.8, 11.8, 11.7, 11.8, 11.9, 11.8, 11.9, 11.8, 11.6, 0, 11.2, 11.6],
    "P5": [11.3, 11.4, 11.3, 11.2, 11.0, 0, 10.9, 11.1, 11.3, 11.4, 11.3, 11.2, 11.2],
    "P6": [0, 0, 0, 0, 0, 0, 10.2, 11.0, 11.3, 11.4, 11.2, 11.3, 11.4],
}

# ----------------------------------------------------------------------------------------------- coal and its density
COALS = {
    "KH-COL": ("Colombian steam coal", "Carbones Montoya Vélez S.A.S."),
    "KH-USA": ("US steam coal", "Tygart Run Energy Sales LLC"),
    "KH-POL": ("Polish steam coal", "Silesia Fuels Sp. z o.o."),
}
# the fuel laboratory's in-pile density tests: (date, coal, pile area, t/m3)
DENSITY_TESTS = [
    ("2025-09-10", "KH-COL", "P2", 0.896), ("2025-10-02", "KH-USA", "P4", 0.932), ("2025-11-12", "KH-POL", "P5", 0.874),
    ("2026-03-24", "KH-COL", "P2", 0.903), ("2026-04-21", "KH-USA", "P4", 0.928), ("2026-05-19", "KH-POL", "P3", 0.881),
    ("2026-06-09", "KH-COL", "P1", 0.899), ("2026-08-27", "KH-USA", "P6", 0.935), ("2026-09-15", "KH-POL", "P5", 0.877),
    ("2026-11-03", "KH-COL", "P1", 0.891), ("2026-11-24", "KH-USA", "P6", 0.929), ("2026-12-01", "KH-POL", "P3", 0.883),
]
DENSITY_UNIT_SWITCH = "2026-07-01"   # the laboratory's system writes kg/m3 before this date and t/m3 from it
TRUE_DENSITY_BIAS = {"KH-COL": 1.003, "KH-USA": 0.997, "KH-POL": 1.002}   # the pile against its last test

# ----------------------------------------------------------------------------------------------- the burn and the plan
# coal delivered to the boiler house, tonnes a day by month (2025-12 to 2027-01)
BURN = {"2025-12": 2480, "2026-01": 2610, "2026-02": 2560, "2026-03": 2240, "2026-04": 1900, "2026-05": 1350,
        "2026-06": 620, "2026-07": 180, "2026-08": 240, "2026-09": 1050, "2026-10": 2050, "2026-11": 2380,
        "2026-12": 2566, "2027-01": 2600}
UNIT2_STOP = ("2026-06-08", "2026-09-14")      # unit 2's annual outage: the peak boilers burn coal alone
PLAN_Q1 = [("January", 31, 2240, 350), ("February", 28, 2180, 340), ("March", 31, 1890, 300)]  # unit 2, peak, t/d
FLOOR_DAYS = 60
OPTION = ("Silesia Fuels Sp. z o.o.", "RL-HK-2026-03", "2027-01-08")

# ----------------------------------------------------------------------------------------------- contracts and ships
CONTRACTS = [
    ("RL-HK-2025-03", "Silesia Fuels Sp. z o.o.", "KH-POL", "Polish steam coal, 2025 term", "Gdansk"),
    ("RL-HK-2026-01", "Carbones Montoya Vélez S.A.S.", "KH-COL", "Colombian steam coal, 2026 term", "Santa Marta"),
    ("RL-HK-2026-02", "Tygart Run Energy Sales LLC", "KH-USA", "US steam coal, 2026 term", "Baltimore"),
    ("RL-HK-2026-03", "Silesia Fuels Sp. z o.o.", "KH-POL", "Polish steam coal, 2026 term with winter option",
     "Gdansk"),
    ("RL-HK-2026-07", "Kattegat Bulk Trading ApS", "KH-COL", "Colombian steam coal (Montoya Vélez origin), spot",
     "Santa Marta"),
    ("RL-HK-2026-09", "Kattegat Bulk Trading ApS", "KH-USA", "US steam coal (Tygart Run origin), spot", "Baltimore"),
]
VESSELS = ["Bothnia Wren", "Arctic Skua", "Polar Merlin", "Nordic Tern", "Bothnian Trader", "Baltic Merle",
           "Ice Fulmar", "Hanko Pioneer", "Gull Island", "Eider Bay", "Storm Petrel", "Frost Harrier", "Norra Kvarn",
           "Sanderling", "Kestrel Bulk", "Guillemot Venture"]
UNLOADER_RATE = (980.0, 1260.0)   # grab unloader GU-1, t/h while running
RECLAIM_RATE = (760.0, 1040.0)    # reclaimer feed onto CV-21, t/h
SCALE_ERR = {"CV-01": 1.0031, "CV-21": 0.9978}
CV21_SWAP = "2026-06-09 13:20"    # the reclaim conveyor's belt-scale integrator replaced (Finnish time)

# historian communication losses (Finnish time): both conveyor tags hold their last totaliser value, and the first
# interval after the link returns carries everything weighed while it was down
OUTAGES = [("2026-03-30 21:30", "2026-04-01 14:15"), ("2026-09-29 23:15", "2026-10-01 16:45")]
# three more fell while a ship was discharging: (call index, hours before its last grab, hours after it)
CALL_OUTAGES = {18: (13.75, 4.5), 20: (2.0, 2.75), 22: (2.5, 2.25)}

# ----------------------------------------------------------------------------------------------- people
FUEL_MANAGER = "Kirsi Salo"
SURVEY_ENGINEER = "Aaro Miettinen"
LAB = "Maarit Vainio"
YARD = "Pekka Jalonen"
SURVEYOR_A = "Marianne Kosonen"
SURVEYOR_B = "Karoliina Huttunen"
CEO = "Elisabeth Hakala"

STAMP = (2027, 1, 4, 9, 15, 0)    # the folder as the fuel team assembled it
ASOF = "2027-01-04"

FILES = {
    "procedure": "fuel_security_procedure_PR-07.pdf",
    "accounting": "coal_yard_accounting_instruction.pdf",
    "control": "survey_control_report_2026-07.pdf",
    "deliveries": "survey_deliveries.csv",
    "areas": "coalyard_pile_areas.csv",
    "density": "fuel_lab_density_tests.csv",
    "plan": "coal_burn_plan_2027Q1.xlsx",
    "berth": "berth_log_2025-12_2026-12.csv",
    "contracts": "coal_contracts.csv",
    "gu1": "gu1_unloader_events.csv",
    "historian": "historian_cv01_cv21_15min.csv",
    "shiftlog": "control_room_shift_log.csv",
    "bunkers": "boiler_bunker_levels_2026-12-16.csv",
    "analyses": "coal_cargo_analyses.csv",
}


def survey_file(i):
    d = SURVEYS[i][0]
    return "coalyard_survey_%s.%s" % (d, "asc" if i < B_FROM else "xyz")


for _i in range(len(SURVEYS)):
    FILES["survey%02d" % _i] = survey_file(_i)


def local(s):
    """'YYYY-MM-DD HH:MM' in Finnish time to an aware datetime."""
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=FI)


def flight(i):
    d, a, b = SURVEYS[i]
    return local("%s %s" % (d, a)), local("%s %s" % (d, b))


QUARTERS = [(local("2026-01-01 00:00"), local("2026-04-01 00:00")), (local("2026-04-01 00:00"), local("2026-07-01 00:00")),
            (local("2026-07-01 00:00"), local("2026-10-01 00:00")), (local("2026-10-01 00:00"), local("2027-01-01 00:00"))]
