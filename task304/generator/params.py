"""task304 architecture 2: the Brannock Trust's 2027 find-and-treat van, four candidate settings.

Every parameter of the world lives here; the generator reads nothing else. Rates are the world's own, not the
answers: every graded figure is computed from the shipped files by solve.py."""
import datetime as dt

SEED = 304230
AS_OF = dt.date(2026, 9, 30)
LAB_START = dt.date(2015, 1, 1)
POOL_START = dt.date(2024, 10, 1)          # the two plan years: Oct 2024 to Sep 2025, Oct 2025 to Sep 2026
ARRIVALS_START = dt.date(2023, 10, 1)      # the arrivals returns run three years
PILOT_START, PILOT_END = dt.date(2018, 10, 1), dt.date(2019, 9, 30)
EXPORT_DATE = dt.date(2026, 10, 12)         # the day the pack was pulled together for the trustees' paper

ORG = "Brannock Trust"
NETWORK = "Fenwold Hepatitis C Network"
HOST_TRUST = "Fenwold Teaching Hospitals NHS Foundation Trust"
PRISON_PROVIDER = "Corvane Health (Justice) Ltd"
LAB = "Fenwold Pathology, virology"

# people (guard.py names --geo uk --seed 304)
DIRECTOR = "Katie Reynolds"        # director of services, Brannock Trust
TEAM_LEAD = "Robin Higgins"        # outreach team lead, ran the 2018-19 pilot
CLIN_LEAD = "Clare Stevenson"      # consultant hepatologist, the network's clinical lead

# the four candidate settings: code, label in the plan, the returning organisation
SETTINGS = ["AP", "HH", "DS", "NSP"]
SETTING_LABEL = {
    "AP": "the approved premises",
    "HH": "the city hostels",
    "DS": "Fenwold Recovery's new entrants",
    "NSP": "the pharmacy needle exchange's new registrants",
}

# distinct people arriving per plan year (mean), antibody positive share among them,
# share of positives cured before they arrive, share of those cures given inside prison,
# share of cured who were infected again before arriving, share of those whose re-infection the regional
# laboratory recorded (an RNA detected after the cure), share of never-treated positives coming to clinic
WORLD = {
    "AP":  dict(arrive=980,  ab=0.240, comm_dx=0.45, prison_dx=0.93, cov_prison=0.95, cov_comm=0.25, reinf=0.060, reinf_lab=0.60),
    "HH":  dict(arrive=1010, ab=0.152, comm_dx=0.45, prison_dx=0.36, cov_prison=0.95, cov_comm=0.55, reinf=0.050, reinf_lab=0.60),
    "DS":  dict(arrive=2060, ab=0.156, comm_dx=0.74, prison_dx=0.26, cov_prison=0.95, cov_comm=0.86, reinf=0.040, reinf_lab=0.60),
    "NSP": dict(arrive=490,  ab=0.380, comm_dx=0.26, prison_dx=0.15, cov_prison=0.95, cov_comm=0.42, reinf=0.050, reinf_lab=0.60),
}
VIRAEMIC_NEVER_TREATED = 0.74      # chronic share after spontaneous clearance, the field's constant
ATTEND = 0.56                      # never-treated (and re-infected) positives coming to clinic after a reactive test
PEER_TEST_SHARE = 0.80             # arrivals the peer team tests within six weeks of arriving
SVR_RATE = 0.955                   # courses cured
UNTESTED_SHARE = 0.12               # courses with no twelve-week test, people outside the settings
TWO_NUMBER_SHARE = 0.025            # people with a course ended before the go-live whose later samples carry a second NHS number
NO_SVR_TEST = 0.02                 # completed courses with no twelve-week test (rare in both records)

# the pilot (validated evidence): two settings, everyone arriving in the pilot year
PILOT = dict(arrive={"HOPE": 690, "CORR": 760}, test=0.62, ab={"HOPE": 0.27, "CORR": 0.34}, cured=0.035,
             start12=0.71)

# background laboratory volume per year by requester group (antibody tests), and the first-positive share
LAB_REQUESTERS = {
    "GP": (5200, 0.012), "ANTENATAL": (5900, 0.0016), "SEXUAL_HEALTH": (2300, 0.008),
    "HOSPITAL": (1500, 0.020), "DRUG_SERVICE": (1500, 0.140), "OUTREACH_CLINIC": (480, 0.200),
}

# the network's clinics (Ask A)
CLINICS = ["HEP", "COMM", "FRC", "PHARM", "OUT"]
CLINIC_LABEL = {
    "HEP": "hospital hepatology clinic",
    "COMM": "community hepatitis clinic",
    "FRC": "Fenwold Recovery clinic",
    "PHARM": "pharmacy-led clinic",
    "OUT": "outreach nurse clinic",
}
SVR_KEYED_SINCE_GOLIVE = 0.62      # share of twelve-week results keyed into the register after the Oct 2024 go-live
EPR_GO_LIVE = dt.date(2024, 10, 1)

# the van
VAN_TEST_SHARE_NOTE = "the pilot's"
PRISONS = {"TAM": "HMP Fenwold", "SAL": "HMP Sallowby", "HAV": "HMP Mardlow"}

FILES = {
    "lab": "virology_hcv_results_2015-01_to_2026-09.csv",
    "register": "hcv_treatment_register_2015-2026.csv",
    "prison": "corvane_hcv_courses_2017-2026.xlsx",
    "peer": "peer_testing_log_2024-10_to_2026-09.csv",
    "arrivals": "setting_arrivals_2023-10_to_2026-09.csv",
    "pilot": "van_pilot_2018-19_caseload.csv",
    "plan": "find_and_treat_van_2027_plan.pdf",
    "evaluation": "van_pilot_evaluation_2018-19.pdf",
    "pathway": "fenwold_hcv_pathway_2026.pdf",
    "clinics": "network_clinic_list_2026.csv",
    "nsp_activity": "nsp_pharmacy_transactions_2025-04_to_2026-09.csv",
    "fibroscan": "fibroscan_sessions_2025-26.xlsx",
}
DISTRACTORS = ["nsp_activity", "fibroscan"]
