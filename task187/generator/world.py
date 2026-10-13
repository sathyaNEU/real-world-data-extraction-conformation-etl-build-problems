"""Cairnhollow Community Wind Farm: the names, places, dates and fixed facts of the fiction.

Time runs on a UTC index of ten-minute intervals; interval k covers [START + 10k min, START + 10(k+1) min). The twelve
months are October 2025 to September 2026 in UK local time, so START is local midnight on 1 October 2025 (BST)."""
import datetime as dt
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
LONDON = ZoneInfo("Europe/London")
SEED = 187

SOCIETY = "Cairnhollow Community Energy"
FARM = "Cairnhollow Community Wind Farm"
OEM = "Hallvard"
MODEL = "Hallvard H93-2.3"
RATED_KW = 2300.0
ROTOR_D = 93.0
HUB_M = 80.0
CUT_IN, CUT_OUT, RESTART = 3.0, 25.0, 20.0
DNO = "Morvenside Networks"
ANM_SCHEME = "Morvenside Networks active network management scheme, Glenrigg zone"
CONNECTION_MW = 23.0
ROPE = "Skerrow Blade Services"
CRANE = "Brackwater Cranes"
SERVICE = "Hallvard Service UK"

PEOPLE = {
    "asset_manager": ("Jenna Dyer", "Asset Manager, Cairnhollow Community Energy"),
    "chair": ("Peter Sharp", "Chair of the Board, Cairnhollow Community Energy"),
    "site": ("Denis Lloyd", "Site Technician, Cairnhollow Community Energy"),
    "service": ("Steven Singh", "Service Supervisor, Hallvard Service UK"),
    "lifts": ("Sara Wood", "Lift Supervisor, Brackwater Cranes"),
    "anm": ("Vanessa Chambers", "ANM Engineer, Morvenside Networks"),
    "secretary": ("Carolyn Scott", "Company Secretary, Cairnhollow Community Energy"),
}
TECHNICIANS = ["Natasha Gilbert", "Marilyn Akhtar", "Dorothy Graham", "Ashleigh Jones", "Melissa Hurst"]

START = dt.datetime(2025, 9, 30, 23, 0, tzinfo=UTC)          # 00:00 BST, 1 October 2025
DAYS = 365
N = DAYS * 144                                               # intervals ending 00:10 1 Oct 2025 to 00:00 1 Oct 2026 local
MIGRATION = dt.datetime(2026, 2, 3, 10, 0, tzinfo=UTC)       # SCADA: site server (local) to hosted platform (UTC)
AS_OF = dt.date(2026, 10, 9)
EXTRACT_STAMP = dt.datetime(2026, 10, 9, 9, 40, tzinfo=UTC)

TURBINES = ["CH%02d" % k for k in range(1, 11)]
# pads in the civil contractor's construction order, from the access road at the south-east
PAD = {"CH10": "P01", "CH06": "P02", "CH07": "P03", "CH05": "P04", "CH08": "P05", "CH04": "P06", "CH02": "P07",
       "CH09": "P08", "CH03": "P09", "CH01": "P10"}
# site grid, metres east and north of the site datum at the boundary's south-west corner
XY = {"CH01": (600, 1900), "CH02": (690, 1530), "CH03": (950, 2060), "CH04": (988, 1662), "CH05": (830, 780),
      "CH06": (1200, 940), "CH07": (900, 400), "CH08": (1360, 1320), "CH09": (1580, 1800), "CH10": (1300, 560)}
MAST_XY = (250, 1200)
ELEVATION = {"CH01": 431, "CH02": 418, "CH03": 445, "CH04": 438, "CH05": 402, "CH06": 411, "CH07": 394,
             "CH08": 426, "CH09": 452, "CH10": 405}
MAST_ELEVATION = 409
NACELLE_SERIAL = {t: "H93-%05d" % (40311 + k * 7 + (k * k) % 5) for k, t in enumerate(TURBINES)}
COMMISSIONED = dt.date(2014, 11, 27)

# leading-edge erosion: the fraction of the power coefficient the blade set has lost below rated
EROSION = {"CH04": 0.0236, "CH02": 0.0165}
CH09_OLD_ROTOR_LOSS = 0.17
CH09_FAULT = dt.datetime(2026, 4, 13, 5, 50, tzinfo=UTC)      # main-bearing temperature trip; old rotor's last minute
CH09_BACK = dt.datetime(2026, 4, 25, 13, 20, tzinfo=UTC)     # new rotor in service
COMMS_OUTAGE = (dt.datetime(2025, 11, 18, 14, 20, tzinfo=UTC), dt.datetime(2025, 11, 19, 10, 40, tzinfo=UTC))
GRID_LOSS = (dt.datetime(2026, 1, 24, 3, 10, tzinfo=UTC), dt.datetime(2026, 1, 24, 12, 40, tzinfo=UTC))
NOISE_HOURS = (23, 7)                 # local, the planning condition's night
NOISE_SECTOR = (230.0, 300.0)         # mast wind direction towards the village
NOISE_TURBINES = ("CH06", "CH08", "CH09", "CH10")   # the planning condition's four turbines nearest the village
NOISE_CAP_KW = 1800.0

STATE_TEXT = {
    10: "Running", 11: "Running, power limited by external setpoint", 20: "Ready, wind below cut-in",
    21: "Stopped, wind above cut-out", 22: "Stopped, ice detected", 30: "Service mode", 40: "Fault",
    41: "Repair", 50: "Stopped from SCADA", 60: "External stop (network operator)", 61: "Grid loss",
}


def interval_index(t):
    """The index of the interval that STARTS at UTC datetime t (on a ten-minute boundary)."""
    k = (t - START).total_seconds() / 600.0
    assert k == int(k), t
    return int(k)


def start_of(k):
    return START + dt.timedelta(minutes=10 * k)


def end_of(k):
    return START + dt.timedelta(minutes=10 * (k + 1))


def local(t):
    return t.astimezone(LONDON)
