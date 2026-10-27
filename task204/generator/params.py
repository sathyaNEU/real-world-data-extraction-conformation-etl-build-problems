#!/usr/bin/env python3
"""World parameters for task204, Beldarrig ETB's Kilmoneen campus.

Every number a shipped file or a graded figure depends on is here, read by world.py, analysis.py,
build.py, checks.py and verify.py, so no constant is written twice (reduce-house-fixes H2, and
determinism-check section 5 on constants in figures.json).

Physics. Each monitored space is one well-mixed zone. Carbon dioxide excess over the outdoor baseline,
C in ppm, obeys V dC/dt = 1e6 N G - Q C, with V the gross internal volume in cubic metres, N the
occupants present, G the per-person generation rate in cubic metres per second and Q the outdoor-air
supply in cubic metres per second. Q takes one of three values per space, set by the air handling unit's
state: occupied, setback or off (infiltration alone).
"""

# ----------------------------------------------------------------- the term and the clock

TERM_START = "2026-09-28"       # Monday
TERM_END = "2026-12-11"         # Friday, inclusive
TZ = "Europe/Dublin"
EXPORT_DATE = "2026-12-15"      # every extract is pulled on this date, and it is the pack's as-of
STEP_S = 300                    # the building management system logs on a five-minute wall-clock grid

# Non-teaching weekdays inside the window: the midterm break week and two whole-campus closures.
MIDTERM_BREAK = ("2026-10-26", "2026-10-30")
CLOSURE_DAYS = {
    "2026-11-06": "Staff development day, campus closed to learners",
    "2026-12-01": "Campus closed, red weather warning",
}

# ----------------------------------------------------------------- the standard and the procedure

STANDARD_REF = "TGD-M4"
STANDARD_TITLE = "Ventilation and Indoor Air Quality in Education Buildings"
STANDARD_ISSUER = "Department of Education, Planning and Building Unit"
STANDARD_EDITION = "2019 edition, revision 3 (March 2024)"
REQUIRED_LS_PER_PERSON = 8.0            # litres per second per person, the requirement under test
GENERATION_L_PER_S = 0.0072             # per-person carbon dioxide generation, seated classroom (1.2 met)
GENERATION_M3_PER_S = GENERATION_L_PER_S / 1000.0
SCREENING_PPM = 1500                    # the campus procedure note's screening indicator
RATE_BIN = 0.5                          # rates are reported to the nearest 0.5 litres per second
DESIGN_SUPPLY_LS = 8.5                  # commissioning record, design supply at design occupancy
DESIGN_OCCUPANCY = {                    # the same record's design occupancy per block space
    "TUL-G07": 48, "TUL-G12": 56, "TUL-G18": 44, "TUL-F04": 60, "TUL-F09": 40, "TUL-F15": 54,
}

# ----------------------------------------------------------------- the air handling units

# Each unit's own time clock, local time. The two Tulrohan units were put on a timetable-linked
# schedule in the 2021 controls retrofit, so they run only across the teaching periods; the two older
# units run a fixed clock. Setback is the midday band at reduced fan speed.
AHU = {
    "AHU-01": {"serves": "Drumlusk Block", "occupied": ("07:45", "16:00"),
               "setback": ("12:10", "12:55"), "fan_setback_pct": 25, "fan_occupied_pct": 80,
               "control": "fixed time clock"},
    "AHU-02": {"serves": "Annagloor Block", "occupied": ("07:30", "15:45"),
               "setback": ("12:00", "12:45"), "fan_setback_pct": 30, "fan_occupied_pct": 85,
               "control": "fixed time clock"},
    "AHU-03": {"serves": "Tulrohan Block, ground floor", "occupied": ("07:55", "15:00"),
               "setback": ("12:00", "12:55"), "fan_setback_pct": 20, "fan_occupied_pct": 75,
               "control": "timetable-linked schedule"},
    "AHU-04": {"serves": "Tulrohan Block, first floor", "occupied": ("07:55", "15:00"),
               "setback": ("12:00", "12:55"), "fan_setback_pct": 20, "fan_occupied_pct": 75,
               "control": "timetable-linked schedule"},
}

# ----------------------------------------------------------------- the monitored spaces

# q_occ is the occupied-state outdoor-air supply in cubic metres per second, measured as a plant
# property rather than recorded anywhere in the pack. ach_off and ach_sb are the off and setback air
# change rates per hour, which set the infiltration-only and reduced-fan supplies.
#
# The six Tulrohan spaces are the block the capital bid covers. Their volumes are the as-built gross
# internal volumes and their response times V/Q run 253 to 543 minutes against a 55-minute period.
SPACES = [
    # code, name, block, ahu, volume_m3, q_occ_m3s, ach_off, ach_sb, floor_area_m2, height_m
    ("TUL-G07", "Engineering Workshop G07",   "Tulrohan", "AHU-03", 2400, 0.209565, 0.05, 0.09, 445, 5.4),
    ("TUL-G12", "Construction Skills Hall G12", "Tulrohan", "AHU-03", 2850, 0.234418, 0.05, 0.09, 475, 6.0),
    ("TUL-G18", "Design Studio G18",          "Tulrohan", "AHU-03", 3200, 0.187767, 0.05, 0.09, 580, 5.5),
    ("TUL-F04", "Lecture Room F04",           "Tulrohan", "AHU-04", 3750, 0.250216, 0.05, 0.09, 735, 5.1),
    ("TUL-F09", "Teaching Hall F09",          "Tulrohan", "AHU-04", 4150, 0.190291, 0.05, 0.09, 755, 5.5),
    ("TUL-F15", "Assembly Room F15",          "Tulrohan", "AHU-04", 4650, 0.267827, 0.05, 0.09, 860, 5.4),
    ("DRM-104", "Classroom 104",              "Drumlusk", "AHU-01", 260, 0.183517, 0.10, 0.25, 93, 2.8),
    ("DRM-108", "Classroom 108",              "Drumlusk", "AHU-01", 300, 0.260712, 0.10, 0.25, 105, 2.9),
    ("DRM-205", "Classroom 205",              "Drumlusk", "AHU-01", 240, 0.217417, 0.10, 0.25, 86, 2.8),
    ("DRM-211", "Seminar Room 211",           "Drumlusk", "AHU-01", 285, 0.232090, 0.10, 0.25, 99, 2.9),
    ("ANG-012", "Science Laboratory 012",     "Annagloor", "AHU-02", 420, 0.794377, 0.10, 0.25, 140, 3.0),
    ("ANG-016", "Science Laboratory 016",     "Annagloor", "AHU-02", 460, 0.722258, 0.10, 0.25, 152, 3.0),
    ("ANG-103", "Computer Room 103",          "Annagloor", "AHU-02", 330, 0.253766, 0.10, 0.25, 113, 2.9),
    ("ANG-107", "Computer Room 107",          "Annagloor", "AHU-02", 380, 0.287033, 0.10, 0.25, 128, 3.0),
]

BLOCK_SPACES = [s[0] for s in SPACES if s[2] == "Tulrohan"]

# The room register's three spellings of a room code, one per producing system.
ROOM_LABELS = {
    "TUL-G07": ("TUL.G07.CO2", "T-G07"), "TUL-G12": ("TUL.G12.CO2", "T-G12"),
    "TUL-G18": ("TUL.G18.CO2", "T-G18"), "TUL-F04": ("TUL.F04.CO2", "T-F04"),
    "TUL-F09": ("TUL.F09.CO2", "T-F09"), "TUL-F15": ("TUL.F15.CO2", "T-F15"),
    "DRM-104": ("DRM.104.CO2", "D-104"), "DRM-108": ("DRM.108.CO2", "D-108"),
    "DRM-205": ("DRM.205.CO2", "D-205"), "DRM-211": ("DRM.211.CO2", "D-211"),
    "ANG-012": ("ANG.012.CO2", "A-012"), "ANG-016": ("ANG.016.CO2", "A-016"),
    "ANG-103": ("ANG.103.CO2", "A-103"), "ANG-107": ("ANG.107.CO2", "A-107"),
}

# ----------------------------------------------------------------- the period grids

# The Tulrohan grid, every boundary clear of the AHU-03 and AHU-04 setback band (12:00 to 12:55).
TUL_PERIODS = [
    ("P1", "08:00", "08:55"), ("P2", "09:00", "09:55"), ("P3", "10:00", "10:55"),
    ("P4", "11:00", "11:55"), ("P5", "13:00", "13:55"), ("P6", "14:00", "14:55"),
]
# The Drumlusk and Annagloor grid, inherited from the 2014 timetable and never moved to match the
# unit time clocks, so two of its periods straddle a setback band.
GEN_PERIODS = [
    ("Q1", "08:15", "09:10"), ("Q2", "09:20", "10:15"), ("Q3", "10:25", "11:20"),
    ("Q4", "11:30", "12:25"), ("Q5", "12:35", "13:30"), ("Q6", "13:40", "14:35"),
    ("Q7", "14:45", "15:40"),
]

# ----------------------------------------------------------------- learner groups

# group code, programme, enrolled, subject code (sedentary classroom activity throughout the block)
GROUPS = [
    # the large practical and lecture cohorts, which are the only groups timetabled into Tulrohan
    ("ENG5A", "Engineering Technology, year 1", 42, "ENG"),
    ("ENG5B", "Engineering Technology, year 2", 56, "ENG"),
    ("ENG6C", "Advanced Manufacturing", 28, "ENG"),
    ("CON5A", "Construction Skills, year 1", 83, "CON"),
    ("CON5B", "Construction Skills, year 2", 60, "CON"),
    ("CON6D", "Site Supervision", 36, "CON"),
    ("DES5A", "Design and Visual Communication", 55, "DES"),
    ("DES6B", "Interior Architecture", 30, "DES"),
    ("BUS5A", "Business Administration", 76, "BUS"),
    ("BUS5B", "Accounting Technician", 60, "BUS"),
    ("BUS6C", "Supply Chain", 39, "BUS"),
    ("HSC5A", "Healthcare Support", 80, "HSC"),
    ("HSC5B", "Social Care Practice", 49, "HSC"),
    ("HSC6C", "Community Health", 33, "HSC"),
    ("GEN5A", "General Learning, access", 69, "GEN"),
    # the small specialist groups, taught only in the Drumlusk and Annagloor rooms
    ("ADM4A", "Office Administration, year 1", 24, "ADM"),
    ("ADM4B", "Office Administration, year 2", 19, "ADM"),
    ("CAR4A", "Care Practice, year 1", 27, "CAR"),
    ("CAR4B", "Care Practice, year 2", 15, "CAR"),
    ("LAB4A", "Laboratory Techniques, year 1", 22, "LAB"),
    ("LAB4B", "Laboratory Techniques, year 2", 17, "LAB"),
    ("NET4A", "Network Systems, year 1", 26, "NET"),
    ("NET4B", "Network Systems, year 2", 20, "NET"),
    ("DAT4C", "Data Analytics", 14, "DAT"),
    ("ACC4A", "Bookkeeping and Payroll", 29, "ACC"),
]

# The weekly pattern per space: {weekday index 0..4: {period: group}}. The Tulrohan spaces carry a
# group in every period of every teaching day, which is what the 2021 timetable-linked AHU schedule
# was sized for. The generator draws each session's attendance from the group's enrolment.
TUL_PATTERN = {
    "TUL-G07": {0: ["ENG5A", "ENG5B", "CON5B", "ENG6C", "ENG5A", "ENG5B"],
                1: ["ENG5B", "CON5A", "ENG5A", "ENG6C", "ENG5B", "CON6D"],
                2: ["ENG6C", "ENG5A", "ENG5B", "CON5B", "ENG5A", "ENG5B"],
                3: ["ENG5A", "ENG5B", "ENG6C", "ENG5A", "CON6D", "ENG5B"],
                4: ["ENG5B", "ENG5A", "CON5B", "ENG5B", "ENG6C", "ENG5A"]},
    "TUL-G12": {0: ["CON5A", "CON5B", "CON6D", "CON5A", "CON5B", "GEN5A"],
                1: ["CON5B", "CON6D", "CON5A", "CON5B", "CON5A", "CON6D"],
                2: ["CON5A", "CON5B", "CON5A", "CON6D", "GEN5A", "CON5B"],
                3: ["CON6D", "CON5A", "CON5B", "CON5A", "CON5B", "CON5A"],
                4: ["CON5B", "CON5A", "CON6D", "GEN5A", "CON5A", "CON5B"]},
    "TUL-G18": {0: ["DES5A", "DES6B", "DES5A", "GEN5A", "DES6B", "DES5A"],
                1: ["DES6B", "DES5A", "CON5A", "DES5A", "DES6B", "GEN5A"],
                2: ["DES5A", "GEN5A", "DES6B", "DES5A", "DES5A", "DES6B"],
                3: ["DES5A", "DES6B", "DES5A", "DES6B", "GEN5A", "DES5A"],
                4: ["DES6B", "DES5A", "DES5A", "DES6B", "DES5A", "GEN5A"]},
    "TUL-F04": {0: ["BUS5A", "BUS5B", "HSC5A", "BUS6C", "BUS5A", "BUS5B"],
                1: ["HSC5A", "BUS5A", "BUS5B", "BUS5A", "HSC5B", "BUS5A"],
                2: ["BUS5A", "HSC5A", "BUS5A", "BUS5B", "BUS5A", "HSC5A"],
                3: ["BUS5B", "BUS5A", "HSC5A", "BUS5A", "BUS6C", "BUS5A"],
                4: ["BUS5A", "BUS5B", "BUS5A", "HSC5A", "BUS5B", "BUS5A"]},
    "TUL-F09": {0: ["HSC5B", "CON5A", "HSC5B", "DES5A", "CON5A", "HSC5B"],
                1: ["CON5A", "HSC5B", "HSC6C", "HSC5B", "GEN5A", "HSC6C"],
                2: ["HSC5B", "DES5A", "HSC6C", "HSC5B", "HSC5B", "HSC6C"],
                3: ["HSC6C", "HSC5B", "HSC5B", "HSC6C", "GEN5A", "HSC5B"],
                4: ["HSC5B", "HSC6C", "DES5A", "HSC5B", "HSC6C", "HSC5B"]},
    "TUL-F15": {0: ["GEN5A", "HSC5A", "BUS5A", "GEN5A", "HSC5A", "CON5A"],
                1: ["HSC5A", "GEN5A", "GEN5A", "BUS5A", "GEN5A", "HSC5A"],
                2: ["GEN5A", "BUS5A", "HSC5A", "GEN5A", "CON5A", "GEN5A"],
                3: ["BUS5A", "GEN5A", "HSC5A", "GEN5A", "GEN5A", "BUS5A"],
                4: ["GEN5A", "HSC5A", "GEN5A", "CON5A", "BUS5A", "GEN5A"]},
}

# The other eight spaces are not timetabled to the hour, so each carries a group in some periods only.
# A None leaves the room empty while its unit's time clock still reads occupied.
GEN_PATTERN = {
    "DRM-104": {0: ["ADM4A", None, "ADM4B", "ADM4A", None, "ADM4A", None],
                1: [None, "ADM4A", "ADM4B", None, "ADM4A", None, "ADM4B"],
                2: ["ADM4A", "ADM4B", None, "ADM4A", "ADM4B", None, None],
                3: [None, "ADM4A", "ADM4A", "ADM4B", None, "ADM4A", None],
                4: ["ADM4B", None, "ADM4A", None, "ADM4A", "ADM4B", None]},
    "DRM-108": {0: [None, "CAR4A", "CAR4B", None, "CAR4A", None, "CAR4B"],
                1: ["CAR4A", "CAR4B", None, "CAR4A", None, "CAR4B", None],
                2: [None, "CAR4A", "CAR4A", "CAR4B", None, None, "CAR4A"],
                3: ["CAR4B", None, "CAR4A", None, "CAR4A", "CAR4B", None],
                4: ["CAR4A", None, None, "CAR4B", "CAR4A", None, None]},
    "DRM-205": {0: ["ACC4A", "DAT4C", None, "ACC4A", None, None, "DAT4C"],
                1: [None, "ACC4A", "DAT4C", None, "ACC4A", "DAT4C", None],
                2: ["DAT4C", None, "ACC4A", "DAT4C", None, "ACC4A", None],
                3: ["ACC4A", "DAT4C", None, None, "DAT4C", None, "ACC4A"],
                4: [None, "ACC4A", "DAT4C", "ACC4A", None, None, None]},
    "DRM-211": {0: [None, "NET4A", "NET4B", None, "NET4A", None, None],
                1: ["NET4B", None, "NET4A", "NET4B", None, "NET4A", None],
                2: ["NET4A", "NET4B", None, None, "NET4B", None, "NET4A"],
                3: [None, "NET4A", "NET4A", "NET4B", None, "NET4B", None],
                4: ["NET4B", None, None, "NET4A", "NET4B", None, None]},
    "ANG-012": {0: ["LAB4A", "LAB4B", None, "LAB4A", None, "LAB4B", None],
                1: [None, "LAB4A", "LAB4B", None, "LAB4A", None, "LAB4B"],
                2: ["LAB4B", None, "LAB4A", "LAB4B", None, "LAB4A", None],
                3: ["LAB4A", "LAB4B", None, None, "LAB4B", None, "LAB4A"],
                4: [None, "LAB4A", "LAB4A", "LAB4B", None, None, None]},
    "ANG-016": {0: [None, "LAB4A", "LAB4A", None, "LAB4B", None, None],
                1: ["LAB4B", None, "LAB4A", "LAB4B", None, "LAB4A", None],
                2: ["LAB4A", "LAB4B", None, "LAB4A", "LAB4B", None, None],
                3: [None, "LAB4A", "LAB4B", None, "LAB4A", "LAB4B", None],
                4: ["LAB4A", None, None, "LAB4A", "LAB4B", None, "LAB4A"]},
    "ANG-103": {0: ["NET4A", "NET4B", "DAT4C", None, "NET4A", None, None],
                1: [None, "NET4A", "NET4B", "DAT4C", None, "NET4A", None],
                2: ["NET4B", None, "NET4A", "NET4B", "DAT4C", None, None],
                3: ["NET4A", "NET4B", None, "NET4A", None, "DAT4C", None],
                4: [None, "NET4A", "NET4B", None, "NET4A", None, "NET4B"]},
    "ANG-107": {0: [None, "NET4A", "NET4B", "NET4A", None, None, "NET4B"],
                1: ["NET4A", None, "NET4A", None, "NET4B", "NET4A", None],
                2: [None, "NET4A", "NET4B", None, "NET4A", "NET4B", None],
                3: ["NET4B", None, "NET4A", "NET4B", None, "NET4A", None],
                4: ["NET4A", "NET4B", None, "NET4A", None, None, "NET4B"]},
}

# The one group taught in two rooms in the same period: the year-1 construction cohort splits between
# the skills hall and the design studio on Tuesday period 3, which the enrolment file cannot show.
SPLIT_GROUP = ("CON5A", 1, 2, ("TUL-G12", "TUL-G18"))

# Attendance. Each group's own realised attendance rate across the term, drawn once per group from
# this band and then applied session by session with binomial variation.
ATTENDANCE_BAND = (0.62, 0.93)
# Staff in the room: one tutor in every session, plus a learning-support assistant in some.
ASSISTANT_SHARE = 0.18

# ----------------------------------------------------------------- the outdoor baseline

OUTDOOR_BASE_PPM = 419.0        # campus sensor annual mean, west-midlands inland site
OUTDOOR_GAP = ("2026-10-12", "2026-10-25")   # campus analyser away for repair, inclusive
NATIONAL_STATION = "Mace Head Atmospheric Research Station"
NATIONAL_OFFSET_PPM = -3.4      # the station runs below the campus sensor over the overlap

# ----------------------------------------------------------------- the sensor estate

# One analyser is replaced mid-term, and the maintenance contractor's span check records a reading
# offset either side of the swap.
SENSOR_SWAP = {"space": "ANG-016", "removed": "2026-11-10", "fitted": "2026-11-13",
               "offset_before_ppm": 40, "span_before": 1037, "span_after": 999,
               "old_serial": "VX-2211-0734", "new_serial": "VX-3410-1182"}

# Scattered communications losses per space, as whole days plus a share of scattered stamps.
DROPOUT_DAYS = {
    "TUL-G07": ["2026-11-19"], "TUL-G12": [], "TUL-G18": ["2026-10-07", "2026-12-03"],
    "TUL-F04": [], "TUL-F09": ["2026-11-25"], "TUL-F15": ["2026-10-20", "2026-10-21"],
    "DRM-104": ["2026-12-08"], "DRM-108": [], "DRM-205": ["2026-10-14", "2026-11-17", "2026-12-04"],
    "DRM-211": ["2026-11-03"], "ANG-012": ["2026-10-09"], "ANG-016": [],
    "ANG-103": ["2026-11-27", "2026-12-07"], "ANG-107": ["2026-10-16"],
}
DROPOUT_RATE = {
    "TUL-G07": 0.0011, "TUL-G12": 0.0004, "TUL-G18": 0.0026, "TUL-F04": 0.0000,
    "TUL-F09": 0.0014, "TUL-F15": 0.0031, "DRM-104": 0.0008, "DRM-108": 0.0002,
    "DRM-205": 0.0041, "DRM-211": 0.0019, "ANG-012": 0.0007, "ANG-016": 0.0000,
    "ANG-103": 0.0023, "ANG-107": 0.0013,
}

SENSOR_NOISE_PPM = 7.5          # analyser repeatability, one standard deviation
ROOM_MIXING_SD = 0.030          # day-to-day variation in the effective supply, as a fraction

SEED = 204027

# ----------------------------------------------------------------- people

# Every name is drawn with guard.py names --geo ireland (seeds 204 and 2042), never typed.
ESTATES_OFFICER = "Aileen Menton"          # Beldarrig ETB, estates and compliance
FACILITIES_MANAGER = "Conall Murtagh"      # Kilmoneen campus, facilities
TUTORS = [
    "Caroline Creedon", "Kelsey Hanbury", "Finn Melican", "Emilie Mahedy", "Dominic Filbin",
    "Cody O'Gara", "Orlaigh Sinan", "Antoinette Fee", "Alanna Hilary", "Tony Davenport",
    "Rhiannon Monk", "Alastair Crangle", "Owen Raftery", "Una Nyhan",
]
ASSISTANTS = ["Jana McCafferky", "Grainne Kilkenny", "Corrie MacCarville"]
CONTROLS_TECHNICIAN = "Graeme Cowley"      # Corrandulla Building Controls, maintenance contract
COMMISSIONING_ENGINEER = "Owen Raftery"    # named on the 2021 commissioning record
MAINTENANCE_FIRM = "Corrandulla Building Controls Ltd"
DESIGN_PRACTICE = "Hanbury Keane Consulting Engineers"
COMMISSIONING_FIRM = "Westmeath Air Balancing Services"
ETB_NAME = "Beldarrig Education and Training Board"
CAMPUS_NAME = "Kilmoneen Further Education Campus"
