"""Constants for task304 (architecture 3): Brannock Trust's find-and-treat van, placed full-time in one of four settings
for 2027 after a 2026 rota that visited all four. Every rate here is a property of the world the records are drawn
from; the figures the build grades are computed forward from the shipped files (solve.py), never from these."""
import datetime as dt

D = dt.date
SEED = 304301
SEEDS = dict(pharm=3041, hh=16, ap=356, ds=115, nsp=284, courses=24, lab=3047)
AS_OF = D(2026, 9, 30)
ROTA_START, ROTA_END = D(2026, 1, 5), D(2026, 9, 25)
BANK_HOLIDAYS = {D(2026, 4, 3), D(2026, 4, 6), D(2026, 5, 4), D(2026, 5, 25), D(2026, 8, 31)}
EPR_GO_LIVE = D(2024, 10, 1)
ASSAY_CHANGE = D(2025, 7, 1)
ROLLOUT = D(2027, 4, 1)

ORG = "Brannock Trust"
NETWORK = "Fenwold Hepatitis C Network"
ICB = "NHS Fenwold Integrated Care Board"
LAB = "Fenwold Pathology"
DIRECTOR = "Stephanie Davis"
TEAM_LEAD = "Duncan Jackson"
CLIN_LEAD = "Alison Hartley"

SETTINGS = ["AP", "HH", "DS", "NSP"]
LABEL = {"AP": "the approved premises", "HH": "the city hostels", "DS": "Fenwold Recovery's new entrants",
         "NSP": "the needle exchange pharmacies' new registrants"}
SHORT = {"AP": "Approved premises", "HH": "City hostels", "DS": "Fenwold Recovery new entrants",
         "NSP": "Needle exchange new registrants"}
# the van tablet's setting values; its app update of 18 May 2026 shortened the hostels' site names
TABLET_OLD = {"AP": "Approved Premises", "HH": "Hostel", "DS": "Fenwold Recovery", "NSP": "Pharmacy NSP"}
TABLET_UPDATE = D(2026, 5, 18)
HOSTEL_SHORT = {"Albion House": "ALBION HSE", "St Bride's Court": "ST BRIDES CT", "Marlowe House": "MARLOWE HSE",
                "Canal Street": "CANAL ST", "Holmfield": "HOLMFIELD", "The Foyer, Wexley Road": "FOYER WEXLEY RD",
                "Greyfriars": "GREYFRIARS", "Tenter Lane": "TENTER LN", "Ropewalk House": "ROPEWALK HSE"}

# the world's rates (truth); the 2026 rota measures them with sampling noise
ACCEPT = {"AP": 0.85, "HH": 0.95, "DS": 0.80, "NSP": 0.70}
ACTIVE = {"AP": 0.060, "HH": 0.110, "DS": 0.066, "NSP": 0.170}
ACTIVE_PILOT = 0.025            # new registrants at a pharmacy whose pharmacist already tests and treats
START12 = {"AP": 0.48, "HH": 0.80, "DS": 0.60, "NSP": 0.62}
COVER = {"AP": 0.84, "DS": 0.56, "NSP": 0.62}     # chance a 2026 arrival is met by the van on its rota day
HH_ABSENT = 0.06
HOSTEL_INCIDENCE = 0.0013       # new infections per resident-year among residents who tested negative

AP_PREMISES = [("Holloway House", 30), ("Bracken Lodge", 38), ("Tanner's Yard", 42)]
AP_STAY, AP_GAP = 77.0, 4.0
HOSTELS = [("Albion House", "Fenwold Housing Trust", 86), ("St Bride's Court", "Fenwold Housing Trust", 112),
           ("Marlowe House", "Fenwold Housing Trust", 64), ("Canal Street", "Fenwold Housing Trust", 140),
           ("Holmfield", "Fenwold Housing Trust", 96), ("The Foyer, Wexley Road", "Calder Street Homes", 72),
           ("Greyfriars", "Calder Street Homes", 118), ("Tenter Lane", "Calder Street Homes", 104),
           ("Ropewalk House", "Calder Street Homes", 128)]
HH_STAY, HH_GAP = 1095.0, 12.0
DS_MONTHLY = 158.0
NSP_MONTHLY = 161.0
NSP_REISSUE = 0.085             # share of 'New' rows in a year that re-register a lapsed client
PILOTS = {"FW318": D(2025, 3, 10), "FK207": D(2025, 6, 16), "FN562": D(2025, 11, 3)}

CLINICS = ["HEP", "COMM", "FRC", "HHC", "SHC"]
CLINIC_OLD = {"HEP": "RFI-HEP", "COMM": "KR-COM", "FRC": "FR-CLN", "HHC": "RS-HHC", "SHC": "SH-GUM"}
CLINIC_NAME = {"HEP": "Fenwold Royal Infirmary hepatology clinic", "COMM": "Kestle Road community hepatitis clinic",
               "FRC": "Fenwold Recovery hub clinic", "HHC": "Riverside homeless health clinic",
               "SHC": "Fenwold sexual health clinic"}
CLINIC_YEARLY = {"HEP": 104, "COMM": 120, "FRC": 78, "HHC": 52, "SHC": 38}

FILES = {
    "van": "van_tests_2026-01_to_2026-09.csv",
    "register": "hcv_treatment_register_2015-2026.csv",
    "dispensing": "daa_dispensing_2024-04_to_2026-09.csv",
    "lab": "virology_hcv_results_2015-01_to_2026-09.csv",
    "census": "hostel_residents_2026-09-30.xlsx",
    "hostel_returns": "hostel_occupancy_returns_2023-10_to_2026-09.csv",
    "ap_returns": "approved_premises_returns_2023-10_to_2026-09.csv",
    "ds_episodes": "fenwold_recovery_new_episodes_2023-10_to_2026-09.csv",
    "nsp_reg": "nsp_registrations_2019-04_to_2026-09.csv",
    "pharmacies": "nsp_pharmacies_2026.csv",
    "clinics": "network_clinics_2026.csv",
    "plan": "find_and_treat_van_2027_plan.pdf",
    "pathway": "fenwold_hcv_pathway_2026.pdf",
    "intentions": "fenwold_icb_commissioning_intentions_2027-28.pdf",
    "fibroscan": "van_fibroscan_sessions_2026.xlsx",
    "costs": "van_running_costs_2026.xlsx",
}
DISTRACTORS = ["fibroscan", "costs"]
