"""Constants for task121 (architecture 5): Larkhollow Academies Trust, Halwick Academy's Progress 8 gap.

    The world: the Metropolitan Borough of Brantholme has fourteen state-funded mainstream secondary schools, eight of
    them academies of the Larkhollow Academies Trust, and sixty-two primary schools. The council's school performance
    and data team holds every pupil's key stage 2 and key stage 4 results with the school census record behind them,
    and shares a pupil-level transfer file with the trust. Halwick Academy has the trust's lowest Progress 8 over the
    2022, 2023 and 2024 cohorts (the last three published: no Progress 8 exists for 2025 or 2026, the key stage 2 tests
    having been cancelled in 2020 and 2021). The director of education's paper to the trustees walks Halwick's gap to
    the trust average before the trustees vote the 2027 school improvement plan."""
import datetime as dt

SEED = 34
ASSEMBLED = dt.datetime(2026, 10, 23, 16, 10)

TRUST = "Larkhollow Academies Trust"
TRUST_LTD = "Larkhollow Academies Trust"
BOROUGH = "Brantholme"
COUNCIL = "Brantholme Metropolitan Borough Council"
LA_TEAM = "School Performance and Data Team"
LA_CODE = "397"                     # the borough's local authority number on the transfer file
TRUSTEES_MEETING = dt.date(2026, 12, 9)

COHORTS = (2022, 2023, 2024)        # key stage 4 summers; key stage 2 four summers earlier... five: KS2 in 2017-2019
KS2_YEAR = {2022: 2017, 2023: 2018, 2024: 2019}

PEOPLE = {"director": "Chloe Richardson", "chair": "Maureen Frost", "head": "Terence Rose",
          "data": "Chelsea Newton", "la": "Roy Ahmed", "ceo": "Mohammed Alexander"}

# The fourteen secondaries: key, name, trust member, governance, location (km east, km north), how sought after,
# own effect on progress (Progress 8 points; the trust's other seven are centred, Halwick set against them).
SECONDARIES = [
    ("HAL", "Halwick Academy", True, "Academy converter", (10.4, 4.1), -0.35),
    ("BPK", "Brantholme Park Academy", True, "Academy converter", (5.2, 6.0), 0.35),
    ("FRN", "Fernlea Academy", True, "Academy sponsor led", (1.9, 3.2), 0.05),
    ("CDW", "Coldwell Academy", True, "Academy converter", (8.3, 6.9), 0.15),
    ("MSG", "Mossgate Academy", True, "Academy sponsor led", (3.4, 8.3), -0.10),
    ("SLM", "Saltmoor Academy", True, "Academy converter", (11.2, 1.3), 0.10),
    ("RDH", "Ridley Hey Academy", True, "Academy converter", (6.1, 1.1), 0.20),
    ("WRF", "Wrayfield Academy", True, "Academy sponsor led", (0.8, 6.4), -0.05),
    ("SWF", "St Wilfrid's Catholic High School", False, "Voluntary aided school", (6.6, 4.4), 0.40),
    ("TRS", "Tarnside High School", False, "Community school", (12.6, 5.6), -0.15),
    ("DNH", "Dunholt Academy", False, "Academy converter", (3.9, 4.6), 0.00),
    ("KSB", "Kestle Brook School", False, "Community school", (9.4, 2.4), -0.20),
    ("OKV", "Okeley Vale Church of England Academy", False, "Academy converter", (7.2, 9.1), 0.30),
    ("HSK", "Hesketh Lane Academy", False, "Academy sponsor led", (1.6, 0.9), 0.00),
]
FOCAL = "HAL"
TRUST_KEYS = [s[0] for s in SECONDARIES if s[2]]

# Primary school names: the borough's sixty-two primaries. The first seven sit in Halwick's catchment.
PRIMARY_NAMES = [
    "Halwick Moor Primary School", "Gillcroft Primary School", "Netherfold Community Primary School",
    "Thursby Lane Primary School", "Cobden Street Primary School", "Sedgefold Primary School",
    "Larchmere Primary School",
    "Ashby Moss Primary School", "Birchcliffe Primary School", "Brackenhurst Primary School",
    "Brook Lane Primary School", "Calder Rise Primary School", "Carrfield Primary School", "Croft Hey Primary School",
    "Dale View Primary School", "Deanbrook Primary School", "Eastholme Primary School", "Elmridge Primary School",
    "Fairfold Primary School", "Fernhill Primary School", "Fieldhouse Primary School", "Gorsey Bank Primary School",
    "Greenacre Primary School", "Hallam Fold Primary School", "Hazelmere Primary School", "Hollins Wood Primary School",
    "Kirkby Lane Primary School", "Lark Hill Primary School", "Lower Fold Primary School", "Marsden Road Primary School",
    "Meadowcroft Primary School", "Millbeck Primary School", "Mossley Brow Primary School", "Nab Lane Primary School",
    "Oakenrod Primary School", "Peel Green Primary School", "Pinfold Primary School", "Quarry Bank Primary School",
    "Redbrook Primary School", "Rookwood Primary School", "Rushcroft Primary School", "Sandy Lane Primary School",
    "Shawfield Primary School", "Smithy Bridge Primary School", "Springhill Primary School", "Stoneyfield Primary School",
    "Thorncliffe Primary School", "Tunshill Primary School", "Underhill Primary School", "Waterside Primary School",
    "Westfield Primary School", "Whinmoor Primary School", "Windy Bank Primary School", "Woodhouse Primary School",
    "St Anne's Catholic Primary School", "St Joseph's Catholic Primary School", "Holy Family Catholic Primary School",
    "Our Lady's Catholic Primary School", "St Peter's Church of England Primary School",
    "Christ Church Church of England Primary School", "St Mary's Church of England Primary School",
    "St Thomas More Catholic Primary School",
]
# each secondary's planned year 7 intake (its published admission number, roughly)
PLANNED = {"HAL": 210, "BPK": 270, "FRN": 225, "CDW": 230, "MSG": 180, "SLM": 190, "RDH": 230, "WRF": 175,
           "SWF": 215, "TRS": 205, "DNH": 210, "KSB": 225, "OKV": 180, "HSK": 180}
FEEDERS = list(range(7))
CATHOLIC = [54, 55, 56, 57, 61]
CHURCH = [58, 59, 60]
# primaries elsewhere in the borough whose pupils also carry a shortfall (they feed other secondaries)
OTHER_WEAK = [13, 28, 41, 49]
# primaries that converted to academies inside the window: a new URN from the date shown, the old one before it
CONVERSIONS = {1: dt.date(2018, 9, 1), 4: dt.date(2018, 11, 1), 19: dt.date(2017, 12, 1), 33: dt.date(2018, 6, 1),
               45: dt.date(2019, 1, 1)}

# The truth: Progress 8 points.
BOROUGH_LEVEL = 0.02
FEEDER_SHORTFALL = -0.30
OTHER_WEAK_SHORTFALL = -0.18
HALWICK_OWN = -0.04                  # against the mean of the trust's other seven academies
SD_OWN = 0.14
SD_PRIMARY = 0.10
B_ABSENCE = -0.045                   # per percentage point of year 11 absence
B_DISADV = -0.45
B_GIRL = 0.22
B_SEN_K, B_SEN_E = -0.25, -0.75
B_EAL = 0.30
SD_PUPIL = 1.05

# the pack's files, named as each system names its exports
FILES = {
    "transfer": "brantholme_ks2_ks4_transfer_2022_2024.csv",
    "register": "brantholme_establishments_2026.csv",
    "tables": "ks4_performance_tables_brantholme_2022_2024.csv",
    "estimates": "progress8_national_estimates_2022_2024.xlsx",
    "guide": "brantholme_transfer_file_guide_2026.pdf",
    "paper": "trustees_paper6_halwick_progress8_2026.pdf",
    "attendance": "larkhollow_attendance_2025_26.csv",
    "movements": "larkhollow_in_year_movements_2025_26.csv",
    "results25": "larkhollow_exam_results_summer2025.csv",
    "results26": "larkhollow_exam_results_summer2026.csv",
    "measures": "ks4_measures_summary_2026.pdf",
    "attnote": "larkhollow_attendance_reporting_2025_26.pdf",
    "workforce": "brantholme_school_workforce_nov2025.xlsx",
    "funding": "brantholme_school_funding_2025_26.xlsx",
}
DISTRACTORS = ["workforce", "funding"]
DELIVERABLES = ["halwick_progress8_walk_2022_2024.xlsx", "halwick_progress8_walk.png"]
GOLDEN = DELIVERABLES[0]
CHART = DELIVERABLES[1]
EXTRACT_DATE = dt.date(2026, 9, 18)          # the trust warehouse's attendance extract

# URNs and DfE numbers: the secondaries, then the primaries (the predecessor URN where a primary converted)
SEC_URN = {"HAL": 140512, "BPK": 137884, "FRN": 141907, "CDW": 138216, "MSG": 142355, "SLM": 139447,
           "RDH": 137291, "WRF": 143018, "SWF": 105942, "TRS": 105871, "DNH": 138760, "KSB": 105889,
           "OKV": 140377, "HSK": 144216}
SEC_ESTAB = {"HAL": 4031, "BPK": 4002, "FRN": 4027, "CDW": 4011, "MSG": 4035, "SLM": 4019, "RDH": 4008,
             "WRF": 4036, "SWF": 4601, "TRS": 4014, "DNH": 4022, "KSB": 4016, "OKV": 4602, "HSK": 4038}
