"""Constants for task265: Brennick Valley Health, its three hospitals that replace hips, the Brennick Valley Joint
Registry, the four makers and the six hip constructs on the 2022 to 2027 hip agreement, and the pack's file names."""
import datetime as dt

SYSTEM = "Brennick Valley Health"
REGISTRY = "Brennick Valley Joint Registry"
PEOPLE = {"registry": "Melinda Boyd", "value": "Richard Hart", "analyst": "Sara Gray"}

# code, hospital, town, share of the system's hips, the months its registry clinic enrolled earlier hips
HOSPITALS = [
    ("BVMC", "Brennick Valley Medical Center", "Brennick", (dt.date(2019, 1, 7), dt.date(2020, 12, 18))),
    ("TLH", "Tollefson Lake Hospital", "Tollefson Lake", (dt.date(2018, 1, 15), dt.date(2019, 12, 13))),
    ("KOH", "Kittelstad Orthopaedic Hospital", "Kittelstad", (dt.date(2020, 7, 6), dt.date(2021, 12, 17))),
]
HOSP = [h[0] for h in HOSPITALS]
HOSP_NAME = {h[0]: h[1] for h in HOSPITALS}
CLINIC = {h[0]: h[3] for h in HOSPITALS}
# registry clinics paused for the pandemic
PAUSE = (dt.date(2020, 3, 16), dt.date(2020, 6, 26))

MAKERS = {"VNH": "Varnholt Orthopedics", "THV": "Thorvik Surgical", "JUV": "Juvenor Medical",
          "BRY": "Brysholt Implants"}
# family code, family name, maker, component, fixation
FAMILIES = [
    ("EDV", "Edvalt", "VNH", "stem", "uncemented"),
    ("KEL", "Kelvarne", "VNH", "cup", "uncemented"),
    ("ASK", "Askvane", "THV", "stem", "cemented"),
    ("QRV", "Quarvel", "THV", "cup", "uncemented"),
    ("ORS", "Orsinne", "THV", "cup", "cemented"),
    ("HOL", "Holbrin", "JUV", "stem", "uncemented"),
    ("PLV", "Pellvoro", "JUV", "cup", "uncemented"),
    ("KLV", "Kalvoran", "BRY", "stem", "uncemented"),
    ("MVN", "Morvenne", "BRY", "cup", "uncemented"),
    ("FNM", "Fennimark", "VNH", "cup", "uncemented"),
]
FAM = {f[0]: f for f in FAMILIES}
# the six constructs on the agreement: code, stem family, cup family
CONSTRUCTS = [("TA", "EDV", "KEL"), ("TS", "EDV", "PLV"), ("MF", "ASK", "QRV"), ("VS", "HOL", "PLV"),
              ("MS", "ASK", "PLV"), ("BP", "KLV", "MVN")]
CODES = [c[0] for c in CONSTRUCTS]
CNAME = {c[0]: "%s/%s" % (FAM[c[1]][1], FAM[c[2]][1]) for c in CONSTRUCTS}
PAIR = {(c[1], c[2]): c[0] for c in CONSTRUCTS}
# constructs used before the registry began and retired since (on the registry, not on the agreement)
RETIRED = [("MC", "ASK", "ORS"), ("TI", "EDV", "FNM")]

REG_START = dt.date(2018, 1, 1)
EXTRACT = dt.date(2026, 12, 31)
FIRST_OP = dt.date(2005, 1, 1)
YEAR = 365.25
TEN = 10 * YEAR
BAR = 5.0
THORVIK_RECODE = dt.date(2020, 7, 1)

FILES = {
    "prosp": "bvjr_prospective_hips_2018-2026.csv",
    "legacy": "bvjr_legacy_enrolment_2018-2021.xlsx",
    "revisions": "bvjr_revisions_to_2026-12-31.csv",
    "deaths": "death_index_linkage_2026-12-31.csv",
    "status": "bvjr_followup_status_2026-12-31.csv",
    "crosswalk": "bvjr_component_crosswalk.xlsx",
    "policy": "implant_value_analysis_policy_VA-07.pdf",
    "dictionary": "bvjr_data_dictionary.pdf",
    "log": "bvjr_data_management_log.xlsx",
    "implants": "periop_implant_log_2026.csv",
    "cases": "or_case_list_2026.xlsx",
    "merges": "him_mrn_merges_2026.csv",
    "schedule": "hip_agreement_2022-2027_price_schedule.pdf",
    "visits": "bvjr_clinic_visits_2018-2026.csv",
    "manifest": "export_manifest.csv",
}
DISTRACTORS = ["schedule", "visits"]


def d2i(d):
    return (d - dt.date(2000, 1, 1)).days


def i2d(i):
    return dt.date(2000, 1, 1) + dt.timedelta(days=int(i))
