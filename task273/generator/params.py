"""task273 architecture 5: every constant the world, the pack and the goldens share.

A state energy department designates, before spring 2027, the zone substations of Tallowbark Networks whose
demand on the reference Sunday will fall below their minimum-load threshold once the network moves its
controlled-load (off-peak hot water) switching from the night into a midday solar-soak window."""
from datetime import date, datetime

SEED = 27305

# ---------------------------------------------------------------------------------------------- the fiction
DEPT = "Department of Energy Security and Planning"
DEPT_SHORT = "the Department"
NETWORK = "Tallowbark Networks"
REGION = "Saltgrass Coast"
PEOPLE = {"director": "Megan Robertson", "ops": "Jacob Barnes"}
ROLES = {"director": "Director, Energy Security", "ops": "Manager, Network Operations"}

SPRING = (date(2026, 9, 1), date(2026, 11, 30))       # the preceding spring, 91 days
DST_START_UTC = datetime(2026, 10, 3, 16, 0)          # 2.00 am AEST on Sunday 4 October 2026
REF_DAY = date(2026, 10, 25)                          # the reference Sunday the records produce
SOAK_START = date(2027, 9, 1)                         # the solar soak starts
OUTLOOK_TO = date(2027, 10, 1)                        # solar forecast to connect by this date
BACKSTOP_FROM = date(2025, 7, 1)                      # inverters installed from here can be curtailed
RECONFIG = date(2025, 4, 14)                          # feeders moved between zone substations
ASSEMBLED = date(2027, 2, 2)                          # the pack assembled for the assessment

WINDOW = (10.0, 15.0)                                 # assessment window, local clock hours
SOAK_RELEASE = (10.0, 10.5, 11.0, 11.5, 12.0)         # switch-on signal by load-control group, local
SOAK_OFF = 16.0
NIGHT_RELEASE = (22.0, 22.5, 23.0, 23.5, 24.0)        # the 2026 overnight switching by group
NIGHT_OFF = 31.0                                      # 7.00 am next day

# ---------------------------------------------------------------------------------------------- substations
# code, name, customers, solar share of customers, mean inverter kW, midday kW per customer (Sunday),
# commercial share, controlled-load share of customers, time-switch share of controlled-load heaters,
# solar connections forecast to 1 October 2027 as a share of the reference-day capacity, ladder role
# (D designated on both routes, F designated only once the reach is read, C clears only once the soak load is
# placed, N clears on every route)
SUBS = [
    ("QRB", "Quorrabin",   7420, 0.41, 6.9, 0.58, 0.10, 0.36, 0.58, 0.112, "F"),
    ("BRM", "Brindlemoor", 6180, 0.47, 7.1, 0.52, 0.06, 0.33, 0.12, 0.138, "C"),
    ("CRW", "Corrowie",    4870, 0.38, 6.6, 0.66, 0.18, 0.29, 0.07, 0.091, "N"),
    ("GRB", "Gerrimbal",    8240, 0.44, 7.3, 0.55, 0.09, 0.39, 0.49, 0.124, "F"),
    ("TRV", "Tarravine",   3960, 0.52, 7.5, 0.49, 0.04, 0.31, 0.16, 0.171, "D"),
    ("KLB", "Kellambie",   5530, 0.35, 6.4, 0.71, 0.22, 0.27, 0.24, 0.083, "N"),
    ("WYB", "Wyndabar",  6810, 0.49, 7.2, 0.54, 0.07, 0.42, 0.05, 0.149, "C"),
    ("PLD", "Pelladrin",    3290, 0.45, 6.8, 0.61, 0.12, 0.34, 0.31, 0.102, "N"),
    ("KNB", "Kinnabar",    7960, 0.46, 7.0, 0.50, 0.05, 0.37, 0.62, 0.119, "F"),
    ("WRD", "Wirrandel",    5120, 0.50, 7.4, 0.53, 0.08, 0.35, 0.10, 0.157, "D"),
    ("GNL", "Goonellan",   6460, 0.40, 6.7, 0.63, 0.14, 0.30, 0.19, 0.097, "N"),
    ("TBN", "Tibbarin",    4420, 0.48, 7.1, 0.51, 0.06, 0.41, 0.04, 0.143, "C"),
    ("MDR", "Mundaree",    5890, 0.43, 6.9, 0.57, 0.11, 0.32, 0.27, 0.108, "D"),
    ("ORJ", "Orrinjal",    3640, 0.37, 6.5, 0.69, 0.20, 0.28, 0.21, 0.088, "N"),
    ("WDB", "Wendimbra",   7130, 0.51, 7.6, 0.48, 0.05, 0.38, 0.09, 0.161, "C"),
    ("ODR", "Ondarra",   4980, 0.42, 6.8, 0.56, 0.09, 0.33, 0.34, 0.116, "D"),
]
SCADA_TAG = "{code}_ZS_NET_MW"

# the 2025 reconfiguration: (from substation, to substation, feeders, share of the from-substation's customers)
RECONFIG_MOVES = [("CRW", "TBN", 2, 0.21), ("WRD", "GNL", 1, 0.12), ("GRB", "MDR", 1, 0.09)]

# ---------------------------------------------------------------------------------------------- meters
# model code, maker, description, data, phases, controlled-load register map (general, controlled, export),
# switching class (R the integral receiver, T the internal time switch, - none), first and last year fitted
MODELS = [
    ("HX-A27T", "Hexwell", "Single-phase two-element electronic accumulation meter, 60 A, controlled-load contactor "
     "operated by internal time switch", "accumulation", 1, ("11", "41", None), "T", 1998, 2011),
    ("HX-A31R", "Hexwell", "Single-phase two-element electronic accumulation meter, 60 A, controlled-load contactor "
     "operated by integral audio-frequency receiver", "accumulation", 1, ("11", "41", None), "R", 2003, 2014),
    ("CM-200T", "Calder Metering", "Single-phase two-element accumulation meter, 80 A, controlled-load relay "
     "switched by internal time switch (quartz clock, battery backed)", "accumulation", 1, ("01", "02", None), "T",
     2001, 2013),
    ("CM-240R", "Calder Metering", "Single-phase two-element accumulation meter, 80 A, controlled-load relay "
     "switched by integral audio-frequency receiver (Tallowbark codes)", "accumulation", 1, ("01", "02", None), "R",
     2006, 2015),
    ("NV-5100T", "Norvane", "Single-phase two-element interval meter, 5-minute data, 2 x 31.5 A contactor, contactor "
     "programme held by internal time switch", "interval", 1, ("E1", "E2", "B1"), "T", 2010, 2016),
    ("NV-5300R", "Norvane", "Single-phase two-element interval meter, 5-minute data, 31.5 A contactor driven by "
     "integral audio-frequency receiver", "interval", 1, ("E1", "E2", "B1"), "R", 2013, 2026),
    ("CM-610R", "Calder Metering", "Single-phase two-element interval meter, 5-minute data, 40 A load-control relay "
     "with integral audio-frequency receiver", "interval", 1, ("E1", "E3", "B1"), "R", 2017, 2026),
    ("HX-I440R", "Hexwell", "Single-phase two-element interval meter, 5-minute data, controlled-load contactor "
     "operated by integral audio-frequency receiver, 4G communications", "interval", 1, ("E1", "E2", "B1"), "R",
     2019, 2026),
    ("HX-A10", "Hexwell", "Single-phase single-element electronic accumulation meter, 60 A", "accumulation", 1,
     ("11", None, None), "-", 1997, 2012),
    ("NV-4100", "Norvane", "Single-phase single-element interval meter, 5-minute data", "interval", 1,
     ("E1", None, "B1"), "-", 2010, 2026),
    ("CM-600", "Calder Metering", "Single-phase single-element interval meter, 5-minute data, 4G communications",
     "interval", 1, ("E1", None, "B1"), "-", 2016, 2026),
    ("CM-830", "Calder Metering", "Three-phase single-element interval meter, 5-minute data, CT-ready",
     "interval", 3, ("E1", None, "B1"), "-", 2012, 2026),
]
MODEL_LIST_DATE = date(2026, 11, 2)

# ---------------------------------------------------------------------------------------------- pack dates
SCADA_PULL = date(2026, 12, 4)
SAMPLE_PULL = date(2026, 12, 2)
METER_REG_PULL = date(2026, 12, 11)
READS_PULL = date(2026, 12, 9)
LC_REG_PULL = date(2026, 12, 10)
DER_PULL = date(2026, 12, 8)
ENQUIRY_PULL = date(2026, 12, 7)
FRAMEWORK_DATE = date(2026, 3, 3)
NOTICE_DATE = date(2027, 1, 19)
OUTLOOK_DATE = date(2027, 1, 29)
SUMMER_DATE = date(2026, 11, 6)

ELEMENT_KW = (1.8, 2.4, 3.6, 4.8)
ELEMENT_P = (0.04, 0.17, 0.66, 0.13)
