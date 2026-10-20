"""The world of task468 (architecture 4): Halbrook Community Health Plan, a nonprofit Medicaid managed care plan in a
state that covers adults whatever their immigration status, so members can be enrolled without a Social Security
number; its 14 network hospitals; the 2027 Hospital Quality Bonus, withheld from a hospital whose risk-adjusted 30-day
mortality ratio for fiscal 2026 index admissions exceeds 1.15; and the state Office of Vital Records' linkage of plan
members to the state death file, keyed on the Social Security number when the enrollment file has one and on name,
date of birth and sex when it does not."""
import datetime as dt

SEED = 468

FY_START = dt.date(2025, 7, 1)            # fiscal 2026 admissions
FY_END = dt.date(2026, 6, 30)
WINDOW = 30                               # deaths within 30 days of the admission date
DEATHS_THROUGH = dt.date(2026, 7, 30)     # the last index admission's window closes
LINKAGE_RUN = dt.date(2026, 10, 7)        # Vital Records returned the linkage
CLAIMS_THROUGH = dt.date(2026, 9, 30)     # claims and encounters received through here
AS_OF = "2026-10-09"
FILING_DUE = dt.date(2026, 11, 1)
THRESHOLD = 1.15
BONUS_RATE = 0.02

# identifier classes: the linkage's chance of finding a death that happened (recall) and of returning a death for a
# member who is alive (a false link inside the 30-day search window), by what the enrollment file holds
CLASS_RATES = {
    "ssn": (0.985, 0.0004),               # Social Security number on file: the deterministic pass
    "simple": (0.93, 0.022),              # no number, single surname: name, date of birth and sex; common names collide
    "compound": (0.52, 0.004),            # no number, compound surname: written one way or two, often missed
}
LATER = {"ssn": 0.82, "simple": 0.25, "compound": 0.40}   # an alive member has a claim after day 30
IN_STAY = 0.45                            # share of deaths in the index stay (by hospital below where it differs)
LATER_STAY = 0.30                         # share of deaths after discharge that happen in a later inpatient stay

# network hospitals: name, billing NPI, a second NPI if the hospital changed billing NPI on 1 January 2026, index
# admissions, share of index members enrolled without a number and a single surname, share without a number and a
# compound surname, mean expected mortality, true mortality relative to expected, share of deaths in the index stay,
# share of post-discharge deaths in a later stay, whether the delegated medical group's members use it
HOSPITALS = [
    ("Saint Brendan Medical Center", "1427061185", None, 4200, 0.03, 0.03, 0.050, 0.9035, 0.45, 0.30, True),
    ("Westover Regional Hospital", "1891704462", None, 3300, 0.03, 0.04, 0.055, 1.4522, 0.45, 0.30, False),
    ("Calloway Memorial Hospital", "1306957713", None, 3000, 0.02, 0.03, 0.048, 1.5476, 0.45, 0.30, True),
    ("Varden Surgical Hospital", "1679528840", None, 3000, 0.48, 0.02, 0.012, 0.5760, 0.45, 0.30, False),
    ("Mercy Valley Medical Center", "1548263907", "1952407316", 3600, 0.02, 0.48, 0.090, 1.3111, 0.24, 0.10, True),
    ("Northgate Community Hospital", "1063517249", None, 2400, 0.04, 0.05, 0.050, 1.3117, 0.45, 0.30, False),
    ("Tamsin General Hospital", "1225098471", None, 2200, 0.03, 0.03, 0.046, 0.8588, 0.45, 0.30, True),
    ("Pinecrest Hospital", "1780653192", None, 1900, 0.10, 0.08, 0.050, 0.8753, 0.45, 0.30, False),
    ("Brannock Medical Center", "1134870556", None, 2300, 0.03, 0.40, 0.030, 1.1349, 0.25, 0.10, True),
    ("Lakeshore Hospital", "1598342017", None, 1700, 0.04, 0.04, 0.050, 0.7362, 0.45, 0.30, False),
    ("Corbel Falls Hospital", "1316079425", None, 1500, 0.02, 0.02, 0.055, 0.6369, 0.45, 0.30, False),
    ("Quayside Hospital", "1871209634", None, 3000, 0.38, 0.03, 0.035, 0.9000, 0.45, 0.30, True),
    ("Marlow Ridge Medical Center", "1447736290", None, 1300, 0.03, 0.03, 0.060, 0.9249, 0.45, 0.30, False),
    ("Fairhaven Community Hospital", "1659047823", None, 1100, 0.04, 0.04, 0.050, 1.0488, 0.45, 0.30, False),
]
CANDIDATES = [h[0] for h in HOSPITALS]
# the golden ratio each hospital is calibrated to (mid-bin at one decimal)
TARGET = {"Saint Brendan Medical Center": 0.95, "Westover Regional Hospital": 1.45, "Calloway Memorial Hospital": 1.32,
          "Varden Surgical Hospital": 0.95, "Mercy Valley Medical Center": 1.30, "Northgate Community Hospital": 1.55,
          "Tamsin General Hospital": 0.93, "Pinecrest Hospital": 0.75, "Brannock Medical Center": 1.25,
          "Lakeshore Hospital": 0.75, "Corbel Falls Hospital": 0.65, "Quayside Hospital": 0.95,
          "Marlow Ridge Medical Center": 0.85, "Fairhaven Community Hospital": 1.05}
SHORT = {h[0]: h[0].replace(" Medical Center", "").replace(" Community Hospital", "").replace(" Regional Hospital", "")
         .replace(" Memorial Hospital", "").replace(" Surgical Hospital", "").replace(" Hospital", "") for h in HOSPITALS}

PLAN = "Halbrook Community Health Plan"
GROUP = "Carrisford Medical Group"         # the delegated medical group; its members' stays come as encounters
VITAL = "Office of Vital Records"
PROGRAM = "Hospital Quality Bonus"
PEOPLE = {"vp": "Wendy James", "analyst": "Nathan Hawkins", "linkage": "Eric Thomas"}
TITLES = {"vp": "Vice President, Provider Contracting and Payment, Halbrook Community Health Plan",
          "analyst": "Quality Measurement Analyst, Halbrook Community Health Plan",
          "linkage": "Manager, Linkage Unit, State Office of Vital Records"}

# ------------------------------------------------------------------------------------------------ the pack's world
AS_OF_DATE = dt.date(2026, 10, 9)
SYSTEM_CHANGE = dt.date(2026, 1, 1)        # claims adjudicated from this day on the plan's new claims platform
NPI_CHANGE = dt.date(2026, 1, 1)           # Mercy Valley bills under its second NPI for stays discharged from here
CARRISFORD_SHARE = 0.32                    # members at the delegated hospitals assigned to Carrisford Medical Group

# the plan's 2026 DRG base rate in each hospital's services agreement (dollars per relative weight)
BASE_RATE = {"Saint Brendan Medical Center": 7450.85, "Westover Regional Hospital": 7120.24,
             "Calloway Memorial Hospital": 6881.17, "Varden Surgical Hospital": 7900.52,
             "Mercy Valley Medical Center": 7259.39, "Northgate Community Hospital": 6641.02,
             "Tamsin General Hospital": 6951.03, "Pinecrest Hospital": 6521.88, "Brannock Medical Center": 7041.42,
             "Lakeshore Hospital": 6410.51, "Corbel Falls Hospital": 6301.01, "Quayside Hospital": 7329.92,
             "Marlow Ridge Medical Center": 6700.77, "Fairhaven Community Hospital": 6260.39}
# non-index volumes relative to each hospital's index admissions: deliveries, pediatric stays
DELIVERIES = {"Saint Brendan Medical Center": 0.40, "Westover Regional Hospital": 0.33, "Calloway Memorial Hospital": 0.30,
              "Varden Surgical Hospital": 0.0, "Mercy Valley Medical Center": 0.18,
              "Northgate Community Hospital": 0.35, "Tamsin General Hospital": 0.42, "Pinecrest Hospital": 0.30,
              "Brannock Medical Center": 0.38, "Lakeshore Hospital": 0.28, "Corbel Falls Hospital": 0.25,
              "Quayside Hospital": 0.55, "Marlow Ridge Medical Center": 0.22, "Fairhaven Community Hospital": 0.30}
PEDIATRIC = {"Saint Brendan Medical Center": 0.08, "Westover Regional Hospital": 0.06, "Calloway Memorial Hospital": 0.05,
             "Varden Surgical Hospital": 0.0, "Mercy Valley Medical Center": 0.03,
             "Northgate Community Hospital": 0.05, "Tamsin General Hospital": 0.07, "Pinecrest Hospital": 0.05,
             "Brannock Medical Center": 0.06, "Lakeshore Hospital": 0.04, "Corbel Falls Hospital": 0.04,
             "Quayside Hospital": 0.10, "Marlow Ridge Medical Center": 0.03, "Fairhaven Community Hospital": 0.05}
AMA = 0.016                                # adult admissions ending against medical advice, per index admission

# MS-DRG: the plan's 2026 relative weight, a typical principal diagnosis (ICD-10-CM) and the title
DRG = {
    "871": (1.8727, "A419", "SEPTICEMIA OR SEVERE SEPSIS WITHOUT MV >96 HOURS WITH MCC"),
    "870": (4.4012, "A4189", "SEPTICEMIA OR SEVERE SEPSIS WITH MV >96 HOURS"),
    "291": (1.3315, "I5023", "HEART FAILURE AND SHOCK WITH MCC"),
    "190": (1.1508, "J441", "CHRONIC OBSTRUCTIVE PULMONARY DISEASE WITH MCC"),
    "193": (1.3032, "J189", "SIMPLE PNEUMONIA AND PLEURISY WITH MCC"),
    "064": (1.8016, "I639", "INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION WITH MCC"),
    "682": (1.4818, "N186", "RENAL FAILURE WITH MCC"),
    "853": (4.8461, "A4151", "INFECTIOUS AND PARASITIC DISEASES WITH O.R. PROCEDURES WITH MCC"),
    "207": (5.6224, "J9601", "RESPIRATORY SYSTEM DIAGNOSIS WITH VENTILATOR SUPPORT >96 HOURS"),
    "314": (1.8233, "I5043", "OTHER CIRCULATORY SYSTEM DIAGNOSES WITH MCC"),
    "872": (1.0291, "A419", "SEPTICEMIA OR SEVERE SEPSIS WITHOUT MV >96 HOURS WITHOUT MCC"),
    "292": (0.9024, "I5033", "HEART FAILURE AND SHOCK WITH CC"),
    "194": (0.9188, "J189", "SIMPLE PNEUMONIA AND PLEURISY WITH CC"),
    "065": (1.0322, "I634", "INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION WITH CC OR TPA IN 24 HRS"),
    "683": (0.8838, "N179", "RENAL FAILURE WITH CC"),
    "378": (0.9811, "K922", "G.I. HEMORRHAGE WITH CC"),
    "189": (1.2117, "J9600", "PULMONARY EDEMA AND RESPIRATORY FAILURE"),
    "308": (1.1702, "I4891", "CARDIAC ARRHYTHMIA AND CONDUCTION DISORDERS WITH MCC"),
    "280": (1.6627, "I214", "ACUTE MYOCARDIAL INFARCTION, DISCHARGED ALIVE WITH MCC"),
    "470": (1.8915, "M1711", "MAJOR HIP AND KNEE JOINT REPLACEMENT OR REATTACHMENT OF LOWER EXTREMITY WITHOUT MCC"),
    "392": (0.7504, "K529", "ESOPHAGITIS, GASTROENTERITIS AND MISCELLANEOUS DIGESTIVE DISORDERS WITHOUT MCC"),
    "603": (0.8517, "L03115", "CELLULITIS WITHOUT MCC"),
    "638": (0.8402, "E1165", "DIABETES WITH CC"),
    "313": (0.6203, "R079", "CHEST PAIN"),
    "312": (0.7918, "R55", "SYNCOPE AND COLLAPSE"),
    "641": (0.7889, "E860", "MISCELLANEOUS DISORDERS OF NUTRITION, METABOLISM, FLUIDS AND ELECTROLYTES WITHOUT MCC"),
    "690": (0.7891, "N390", "KIDNEY AND URINARY TRACT INFECTIONS WITHOUT MCC"),
    "247": (2.1733, "I2510", "PERCUTANEOUS CARDIOVASCULAR PROCEDURES WITH DRUG-ELUTING STENT WITHOUT MCC"),
    "343": (1.0461, "K3580", "APPENDECTOMY WITHOUT COMPLICATED PRINCIPAL DIAGNOSIS WITHOUT CC/MCC"),
    "419": (1.5603, "K8020", "LAPAROSCOPIC CHOLECYSTECTOMY WITHOUT C.D.E. WITHOUT CC/MCC"),
    "481": (1.9916, "S72001A", "HIP AND FEMUR PROCEDURES EXCEPT MAJOR JOINT WITH CC"),
    "493": (1.8222, "S82201A", "LOWER EXTREMITY AND HUMERUS PROCEDURES EXCEPT HIP, FOOT, FEMUR WITH CC"),
    "460": (4.1037, "M48061", "SPINAL FUSION EXCEPT CERVICAL WITHOUT MCC"),
    "885": (1.0322, "F209", "PSYCHOSES"),
    "807": (0.5806, "O80", "VAGINAL DELIVERY WITHOUT STERILIZATION OR D&C WITHOUT CC/MCC"),
    "806": (0.6611, "O9989", "VAGINAL DELIVERY WITHOUT STERILIZATION OR D&C WITH CC"),
    "805": (1.0613, "O1414", "VAGINAL DELIVERY WITHOUT STERILIZATION OR D&C WITH MCC"),
    "788": (0.8452, "O82", "CESAREAN SECTION WITHOUT STERILIZATION WITHOUT CC/MCC"),
    "787": (1.0019, "O3421", "CESAREAN SECTION WITHOUT STERILIZATION WITH CC"),
    "786": (1.5167, "O1414", "CESAREAN SECTION WITHOUT STERILIZATION WITH MCC"),
    "798": (0.7488, "O80", "VAGINAL DELIVERY WITH STERILIZATION OR D&C WITHOUT CC/MCC"),
    "797": (0.8421, "O9989", "VAGINAL DELIVERY WITH STERILIZATION OR D&C WITH CC"),
    "768": (1.0507, "O7022", "VAGINAL DELIVERY WITH O.R. PROCEDURES EXCEPT STERILIZATION AND/OR D&C"),
    "795": (0.1712, "Z3800", "NORMAL NEWBORN"),
    "794": (1.3920, "P599", "NEONATE WITH OTHER SIGNIFICANT PROBLEMS"),
    "793": (3.8916, "P221", "FULL TERM NEONATE WITH MAJOR PROBLEMS"),
    "792": (2.0105, "P0735", "PREMATURITY WITHOUT MAJOR PROBLEMS"),
    "791": (3.6084, "P0733", "PREMATURITY WITH MAJOR PROBLEMS"),
    "790": (5.3317, "P220", "EXTREME IMMATURITY OR RESPIRATORY DISTRESS SYNDROME, NEONATE"),
    "203": (0.6215, "J4541", "BRONCHITIS AND ASTHMA WITHOUT CC/MCC"),
    "195": (0.6732, "J189", "SIMPLE PNEUMONIA AND PLEURISY WITHOUT CC/MCC"),
}
DELIVERY_DRGS = ("768", "783", "784", "785", "786", "787", "788", "796", "797", "798", "805", "806", "807")

FILES = {
    "claims": "hchp_ip_claims_extract_2026-10-05.csv",
    "encounters": "CMG_HCHP_IP_ENC_20261006.txt",
    "enrollment": "hchp_member_enrollment_extract_2026-10-05.csv",
    "activity": "hchp_member_service_lines_2025-01_2026-09.csv",
    "linkage": "OVR_HCHP_FY2026_DEATH_LINKAGE_RETURN.csv",
    "scores": "HIMM_3.2_scores_FY2026_admissions.xlsx",
    "roster": "hchp_network_hospitals_2026.csv",
    "spec": "HCHP_Hospital_Quality_Bonus_2027_Measure_Specification.pdf",
    "linknote": "OVR_Linkage_Methods_HCHP_FY2026.pdf",
    "claimnotes": "hchp_ip_claims_extract_notes.pdf",
    "layout": "CMG_Inpatient_Encounter_File_Layout_v4.pdf",
    "readmissions": "HCHP_Quality_Dashboard_Readmissions_FY2026.xlsx",
    "profiles": "HCHP_Network_Hospital_Profiles_2026.pdf",
    "disputes": "HCHP_Provider_Dispute_Log_IP_2026-10-01.xlsx",
}
DISTRACTORS = ["readmissions", "profiles"]
DISPUTE_RUN = dt.date(2026, 10, 1)         # Provider Disputes ran its log
DISPUTE_SHARE = {"reprocessed": 0.18, "finance": 0.008, "denied": 0.006}
DISPUTE_FLOOR = 15000.0                    # Finance's awards on fiscal 2026 stays at each hospital reach at least this
DISPUTE_OLD = {"Saint Brendan Medical Center": 9, "Westover Regional Hospital": 7, "Calloway Memorial Hospital": 6,
               "Varden Surgical Hospital": 2, "Mercy Valley Medical Center": 7, "Northgate Community Hospital": 5,
               "Tamsin General Hospital": 4, "Pinecrest Hospital": 4, "Brannock Medical Center": 4,
               "Lakeshore Hospital": 3, "Corbel Falls Hospital": 3, "Quayside Hospital": 6,
               "Marlow Ridge Medical Center": 3, "Fairhaven Community Hospital": 2}
GOLDEN = {"workbook": "halbrook_2027_hospital_quality_bonus.xlsx"}
