"""The world: the state's 14 counties, its agencies, the testing regimes, the people, the dates, and the knobs the
truth is drawn from. Nothing here is shipped as written; every shipped file is computed from it."""
import datetime as dt
from zoneinfo import ZoneInfo

TASK = "task473"
SEED = 473
CENTRAL = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc

YEARS = (2023, 2024, 2025)
AS_OF = dt.date(2027, 3, 22)                 # the certification package is being prepared
LETTER_DATE = dt.date(2027, 4, 14)           # the certification letter's date in the golden
CENSUS_CLOSE = {2023: dt.date(2025, 2, 27), 2024: dt.date(2026, 2, 26), 2025: dt.date(2027, 2, 25)}
LAB_EXTRACT = dt.date(2027, 3, 12)           # the laboratory's extract for the Center
CRASHDB_EXTRACT = dt.date(2027, 3, 8)        # the crash records system's 2025 extract
PRELIM_2026 = dt.date(2027, 3, 1)            # the 2026 preliminary census extract (a distractor)

UNIVERSITY = "Merrivale State University"
CENTER = "Merrivale State University Center for Transportation Safety"
CENTER_SHORT = "Center for Transportation Safety"
GHSO = "Governor's Highway Safety Office"
LAB = "State Toxicology Laboratory"
DOT = "State Department of Transportation"
PATROL = "State Patrol"
PEOPLE = {"coordinator": ("Mary Mitchell", "Impaired Driving Program Coordinator"),
          "records": ("Eduardo Chapman", "Crash Records Manager"),
          "ghso": ("Janet Brooks", "Impaired Driving Program Manager")}

# ---------------------------------------------------------------------------------------------------------------
# Counties. fips, name, cities (each with a police department), the hospital(s) and jail that draw blood, and the
# knobs: vmt3 (3-year VMT in 100 million), crashes3 (fatal crashes 2023-2025), agency shares (state patrol, sheriff,
# city police), protocol sheriff, killed drivers' impaired share pK, surviving drivers' impaired share at the
# complete agencies pP and at the arrest-only agencies pL, the high-band (.15 or more) share among impaired
# survivors at each, and a target alcohol-impaired-driving rate the generator meets with the killed drivers.
# ---------------------------------------------------------------------------------------------------------------
COUNTIES = [
    # fips, name, cities, draw sites (hospitals), rural (draws partly across the line)
    dict(fips="001", name="Aldous", cities=["Marrin", "Velta"], hospital=None, jail_draws=True, neighbor="017"),
    dict(fips="003", name="Brisbin", cities=["Brisbin City", "Orland"], hospital="Brisbin Memorial Hospital",
         jail_draws=True, neighbor=None),
    dict(fips="005", name="Corwin", cities=["Halden"], hospital="Corwin County Medical Center", jail_draws=True,
         neighbor=None),
    dict(fips="007", name="Delmont", cities=["Delmont", "Ricker", "Sauls Ferry"], hospital="Delmont Regional Hospital",
         jail_draws=True, neighbor=None),
    dict(fips="009", name="Fairlee", cities=["Fairlee", "Coyle", "Westmark"], hospital="Fairlee General Hospital",
         jail_draws=True, neighbor=None),
    dict(fips="011", name="Hatchell", cities=["Bramwell", "Hatchell"], hospital="Bramwell Regional Hospital",
         jail_draws=True, neighbor=None),
    dict(fips="013", name="Keswick", cities=["Kessington", "Ludlow Park", "Fenner"], hospital="Kessington Medical Center",
         jail_draws=True, neighbor=None),
    dict(fips="015", name="Kittredge", cities=["Amesby"], hospital=None, jail_draws=True, neighbor="011"),
    dict(fips="017", name="Lanier", cities=["Lanier", "Pocket Hill"], hospital="Lanier Valley Hospital",
         jail_draws=True, neighbor=None),
    dict(fips="019", name="Ossian", cities=["Ossian", "Crale"], hospital="Ossian Community Hospital", jail_draws=True,
         neighbor=None),
    dict(fips="021", name="Pruett", cities=["Garrow", "Pruett Junction", "Linn Grove"], hospital="Garrow Medical Center",
         jail_draws=True, neighbor=None),
    dict(fips="023", name="Renwick", cities=["Renwick", "Ashford Mills"], hospital="Renwick Regional Medical Center",
         jail_draws=True, neighbor=None),
    dict(fips="025", name="Stroud", cities=["Stroud", "Kelby"], hospital="Stroud County Hospital", jail_draws=True,
         neighbor=None),
    dict(fips="027", name="Tanager", cities=["Tanager", "Wister"], hospital="Tanager University Hospital",
         jail_draws=True, neighbor=None),
]
NAMES = {c["fips"]: c["name"] for c in COUNTIES}
FIPS = {c["name"]: c["fips"] for c in COUNTIES}
PROTOCOL_SHERIFFS = ("005", "019")           # Corwin and Ossian follow the State Patrol's fatal crash procedure
PATROL_HQ = "013"                             # Keswick
POST_OF = {c["fips"]: i + 1 for i, c in enumerate(COUNTIES)}   # one State Patrol post per county

# the knobs (tuned by generator/tune.py against the design note's ladder; the generator reads only these)
KNOBS = {
    #        vmt3   crashes3  sp    so    pd    pK     pP     pL     hiP   hiL   target tilt
    "001": (60.0, 92, 0.50, 0.32, 0.18, 0.37, 0.26, 0.20, 0.50, 0.55, 0.527, 0.0),
    "003": (105.0, 175, 0.14, 0.24, 0.62, 0.33, 0.21, 0.52, 0.50, 0.97, 0.562, -0.3),
    "005": (85.0, 128, 0.55, 0.37, 0.08, 0.40, 0.30, 0.20, 0.50, 0.60, 0.742, 0.0),
    "007": (155.0, 228, 0.45, 0.21, 0.34, 0.30, 0.21, 0.17, 0.50, 0.62, 0.512, 0.0),
    "009": (200.0, 285, 0.45, 0.17, 0.38, 0.27, 0.20, 0.16, 0.50, 0.62, 0.448, 0.0),
    "011": (125.0, 205, 0.20, 0.28, 0.52, 0.32, 0.22, 0.18, 0.50, 0.55, 0.676, 0.0),
    "013": (230.0, 318, 0.38, 0.10, 0.52, 0.22, 0.18, 0.12, 0.50, 0.62, 0.338, 0.0),
    "015": (75.0, 112, 0.52, 0.32, 0.16, 0.36, 0.25, 0.21, 0.50, 0.45, 0.567, 0.0),
    "017": (95.0, 146, 0.20, 0.28, 0.52, 0.31, 0.21, 0.26, 0.50, 0.62, 0.541, 0.0),
    "019": (80.0, 120, 0.45, 0.45, 0.10, 0.41, 0.29, 0.19, 0.50, 0.62, 0.694, 0.0),
    "021": (184.0, 480, 0.10, 0.20, 0.70, 0.31, 0.20, 0.03, 0.50, 0.90, 0.556, 0.3),
    "023": (175.0, 240, 0.48, 0.18, 0.34, 0.24, 0.19, 0.13, 0.50, 0.62, 0.379, 0.0),
    "025": (140.0, 196, 0.45, 0.17, 0.38, 0.25, 0.19, 0.14, 0.50, 0.62, 0.411, 0.0),
    "027": (100.0, 190, 0.08, 0.17, 0.75, 0.30, 0.12, 0.33, 0.50, 0.15, 0.662, 0.35),
}
KNOB_FIELDS = ("vmt3", "crashes3", "sp", "so", "pd", "pK", "pP", "pL", "hiP", "hiL", "target", "tilt")

# officers' arrest at the scene by BAC band (identical at every agency); sober drivers arrested rarely
BANDS = ((0.080, 0.150), (0.150, 0.600))
CATCH = {0: 2 / 7, 1: 8 / 9}
CATCH_SOBER = 0.032
SUBBANDS = ((0.080, 0.100), (0.100, 0.120), (0.120, 0.150), (0.150, 0.200), (0.200, 0.250), (0.250, 0.600))

# the complete agencies' impaired surviving drivers over the three years, by band: the State Patrol, the two
# sheriffs together, and pooled by sub-band (whole multiples of each band's catch denominator)
PROTOCOL_TARGETS = {"SP": {0: 49, 1: 45}, "SO": {0: 7, 1: 9}}
PROTOCOL_SUBBANDS = {0: (14, 21, 21), 1: (27, 18, 9)}

# the tuned counties' arrests at the arrest-only agencies over the three years, (.08 to .149, .15 or more), set by
# generator/tune.py so each county's completed deaths sit inside one whole number under every member of the
# golden completion's family
LOCAL_FOUND = {"015": (2, 2), "025": (0, 7)}

THRESHOLD = 0.60
FILES = {
    "guidelines": "ghso_fy2028_county_task_force_guidelines.pdf",
    "manual": "fcc_reference_manual_2024_ed.pdf",
    "crash23": "fcc_2023_crash.csv",
    "person23": "fcc_2023_person.csv",
    "crash2425": "fcc_2024_2025_crash.csv",
    "person2425": "fcc_2024_2025_person.csv",
    "agencies": "fcc_agency_directory.xlsx",
    "vmt": "dot_county_dvmt_2023_2025.xlsx",
    "lab": "stl_specimen_extract_2023_2025.csv",
    "lab_notes": "stl_extract_notes.txt",
    "sites": "stl_collection_sites.csv",
    "reports": "crs_reports_2025.csv",
    "units": "crs_units_2025.csv",
    "crs_notes": "crs_extract_notes_2025.pdf",
    "lab_annual": "stl_annual_report_2025_tables.pdf",
    "licensed": "dmv_licensed_drivers_by_county_2025.xlsx",
    "prelim26": "fcc_2026_preliminary_crash.csv",
    "index": "cts_fy2028_package_index.csv",
}
DISTRACTORS = ("licensed", "prelim26")
GOLDEN = {"csv": "county_impaired_driving_rates_2023_2025.csv", "letter": "fy2028_high_range_certification.pdf"}
