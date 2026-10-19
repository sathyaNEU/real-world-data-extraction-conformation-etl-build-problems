"""Constants shared by the task270 generator: the trust, its Memory Assessment Service and eight clinics, the two
record systems and the day the service moved from one to the other, the window the research committee reads, the
extract dates and the shipped file names."""
import datetime as dt

TRUST = "Hollinsmere Partnership NHS Foundation Trust"
SHORT = "Hollinsmere Partnership"
SERVICE = "Memory Assessment Service"
SPONSOR = "Arvenna Therapeutics"
TRIAL = "ARV-1102"
PEOPLE = {"lead": "Georgina Khan", "clinical": "Jeremy Hurst", "analyst": "Nicola Lynch"}

# the eight clinics: name, CIS clinic code, EPR site code, the day the clinic saw its first patient
CLINICS = [
    ("Thurlwick", "THURL", "HPF-MAS-01", dt.date(2014, 4, 14)),
    ("Penwardine", "PENWD", "HPF-MAS-02", dt.date(2015, 5, 18)),
    ("Swinholt", "SWINH", "HPF-MAS-03", dt.date(2016, 3, 7)),
    ("Brindlemere", "BRIND", "HPF-MAS-04", dt.date(2017, 7, 3)),
    ("Ravensfold", "RAVEN", "HPF-MAS-05", dt.date(2018, 5, 21)),
    ("Corvale", "CORVA", "HPF-MAS-06", dt.date(2019, 4, 15)),
    ("Mosswick", "MOSSW", "HPF-MAS-07", dt.date(2020, 8, 10)),
    ("Quarndale", None, "HPF-MAS-08", dt.date(2024, 4, 8)),
]
NAMES = [c[0] for c in CLINICS]
CIS_CODE = {c[0]: c[1] for c in CLINICS}
SITE = {c[0]: c[2] for c in CLINICS}
OPENED = {c[0]: c[3] for c in CLINICS}

# Quarndale's catchment was Corvale's and Mosswick's until it opened; the patients already under those clinics
# stayed with them, and new referrals from its districts went to Quarndale
QUARNDALE_FROM = {"Corvale": ["HL19", "HL20"], "Mosswick": ["HL23", "HL24"]}
QUARNDALE_NEW = ["HL25", "HL26", "HL27"]      # commissioned from the neighbouring service on the day it opened
DISTRICTS = {
    "Thurlwick": ["HL1", "HL2", "HL3"],
    "Penwardine": ["HL4", "HL5", "HL6"],
    "Swinholt": ["HL7", "HL8", "HL9"],
    "Brindlemere": ["HL10", "HL11", "HL12"],
    "Ravensfold": ["HL13", "HL14", "HL15"],
    "Corvale": ["HL16", "HL17", "HL18", "HL19", "HL20"],
    "Mosswick": ["HL21", "HL22", "HL23", "HL24"],
    "Quarndale": ["HL19", "HL20", "HL23", "HL24", "HL25", "HL26", "HL27"],
}

EPR_GO_LIVE = dt.date(2024, 1, 8)        # the service's records move from CIS to the electronic patient record
CIS_LAST = dt.date(2024, 1, 5)           # the CIS archive extract (the last working day before go-live)
WINDOW = (dt.date(2022, 1, 1), dt.date(2026, 9, 30))
EXTRACT = dt.date(2026, 10, 2)           # the EPR extracts for the site selection
ASSEMBLED = dt.datetime(2026, 10, 9, 15, 40)
PAPER_DATE = dt.date(2026, 10, 14)       # the site selection paper
QUESTIONNAIRE_DATE = dt.date(2026, 9, 21)
TRIAL_ENTRY = dt.date(2027, 1, 1)        # the trial's entry window opens; the age limit is read on this day
AGE_LIMIT = 85
ASK_YEAR = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
SIX_WEEKS = 42

# ACE-III domains and their maxima (total 100)
DOMAINS = [("ATT", "attention", 18), ("MEM", "memory", 26), ("FLU", "fluency", 14), ("LAN", "language", 26),
           ("VIS", "visuospatial", 16)]

# diagnoses: code used by the service, ICD-10, description
DX = {
    "AD": ("F00.9", "Dementia in Alzheimer's disease, unspecified"),
    "AD_LATE": ("F00.1", "Dementia in Alzheimer's disease with late onset"),
    "AD_MIXED": ("F00.2", "Dementia in Alzheimer's disease, atypical or mixed type"),
    "MCI": ("F06.7", "Mild cognitive disorder"),
    "VAS": ("F01.9", "Vascular dementia, unspecified"),
    "DLB": ("F02.8", "Dementia in other specified diseases (Lewy body)"),
    "PDD": ("F02.3", "Dementia in Parkinson's disease"),
    "FTD": ("F02.0", "Dementia in Pick's disease (frontotemporal)"),
    "UNS": ("F03", "Unspecified dementia"),
    "NOD": ("Z03.2", "Observation for suspected mental disorder, ruled out"),
    "DEP": ("F32.9", "Depressive episode, unspecified"),
}
AD_CODES = ("AD", "AD_LATE", "AD_MIXED")
IN_SCOPE = AD_CODES + ("MCI",)

FILES = {
    "cis_ace": "cis_ace3_forms_2014_2023.csv",
    "epr_obs": "epr_cognitive_observations_2024_2026.csv",
    "cis_dx": "cis_diagnoses_2014_2023.csv",
    "epr_dx": "epr_problem_list_2024_2026.csv",
    "pmi": "patient_master_index.csv",
    "clinics": "mas_clinic_register.xlsx",
    "episodes": "epr_mas_episodes_2024_2026.csv",
    "appts": "epr_outpatient_appointments_2024_2026.csv",
    "tracker": "mas_pathway_tracker_2024_2026.xlsx",
    "paper": "site_selection_paper_RC-26-11.pdf",
    "questionnaire": "arvenna_site_feasibility_questionnaire.pdf",
    "guide": "mas_data_guide_2026.pdf",
    "audit": "mas_service_audit_2024_25.xlsx",
    "population": "catchment_population_65plus_2025.csv",
    "contents": "contents.txt",
}
