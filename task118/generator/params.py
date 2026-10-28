"""task118 (architecture 3) constants: Kestrel Vale integrated care board, its six localities, the hypnotic users and
their repeat templates, the deprescribing policy's filed figures, the falls cohort the asks read, and file names."""
import datetime as dt

ORG = "NHS Kestrel Vale Integrated Care Board"
CSU = "Kestrel and Wold Commissioning Support Unit"
PEOPLE = {"chief": "Julia Clayton", "lead": "Leon Ross", "analyst": "Glenn Pearce", "falls": "Katherine Watts"}
SEED = 1180
AS_OF = dt.date(2026, 10, 20)                     # the folder as handed over

# the policy as filed (hypnotics_deprescribing_policy_2026.pdf)
BASE = 4.0                                        # emergency fall admissions per 100 patients aged 65+ a year, off a hypnotic
RR = ((6, 3.0), (24, 1.8), (None, 1.1))          # rate ratio by months since the patient first started a hypnotic
STOP = 0.45                                       # share of reviewed users the team takes off the drug
CURRENT_FROM, CURRENT_TO = dt.date(2026, 7, 1), dt.date(2026, 9, 30)   # a current user: a hypnotic dispensed here
AGE_ON = dt.date(2027, 1, 1)                      # and aged 65 or over on this day
OFF_FROM, OFF_TO = dt.date(2027, 4, 1), dt.date(2027, 12, 31)          # a patient who stops is off the drug over these days
YEAR = 2027

EXTRACT_FROM, EXTRACT_TO = dt.date(2026, 4, 1), dt.date(2026, 9, 30)   # the dispensing extract (the platform's first months)
TEMPLATES_ACTIVE_SINCE = dt.date(2024, 4, 1)      # the template export: every template active on or after this day
TEMPLATES_AS_AT = dt.date(2026, 10, 1)
MIGRATION = dt.date(2026, 7, 13)                  # one Quenford Rise practice moves clinical system
MIGRATED = "QR"                                   # its locality; the practice is the locality's smallest

# locality: code, name, current users aged 65+, shares of them who started before April 2025 (long), April 2025 to
# March 2026 (mid), April to September 2026 (new)
LOCALITIES = [
    ("CC", "Corvenham Central", 6812, (0.93, 0.05, 0.02)),
    ("FM", "Fenmarsh", 4987, (0.86, 0.08, 0.06)),
    ("SC", "Saltreach Coast", 5034, (0.625, 0.295, 0.08)),
    ("QR", "Quenford Rise", 4583, (0.86, 0.08, 0.06)),
    ("HM", "Hethermoss", 3611, (0.68, 0.04, 0.28)),
    ("LN", "Ledbridge North", 3226, (0.86, 0.08, 0.06)),
]
PRACTICES = {"CC": 7, "FM": 6, "SC": 6, "QR": 6, "HM": 5, "LN": 5}
STOPPED_SHARE = 0.07                              # users dispensed April to June 2026 only (not current)
UNDER_65_SHARE = 0.04                             # users aged 63 or 64 on 1 January 2027 in the extract

DRUGS = [  # VTM, dm+d product, BNF class, pack quantity, NIC per pack (GBP), share of users
    ("Zopiclone", "Zopiclone 7.5mg tablets", "Z-drug", 28, 1.02, 0.34),
    ("Zopiclone", "Zopiclone 3.75mg tablets", "Z-drug", 28, 1.31, 0.10),
    ("Zolpidem", "Zolpidem 10mg tablets", "Z-drug", 28, 1.18, 0.08),
    ("Temazepam", "Temazepam 10mg tablets", "benzodiazepine", 28, 3.40, 0.16),
    ("Diazepam", "Diazepam 2mg tablets", "benzodiazepine", 28, 0.79, 0.14),
    ("Lorazepam", "Lorazepam 1mg tablets", "benzodiazepine", 28, 4.65, 0.08),
    ("Nitrazepam", "Nitrazepam 5mg tablets", "benzodiazepine", 28, 6.92, 0.04),
    ("Lormetazepam", "Lormetazepam 1mg tablets", "benzodiazepine", 30, 21.40, 0.06),
]

# the asks' falls cohort (SUS admitted patient care, every spell 1 March 2025 to 31 July 2026 for patients aged 65 or
# over with an emergency admission carrying an external cause code in 2025-26)
SUS_FROM, SUS_TO = dt.date(2025, 3, 1), dt.date(2026, 7, 31)
FY_FROM, FY_TO = dt.date(2025, 4, 1), dt.date(2026, 3, 31)
FALLS_PER_100 = {"CC": 2.05, "FM": 2.30, "SC": 2.65, "QR": 2.20, "HM": 2.40, "LN": 2.10}   # fall admissions a year
OVER_65 = {"CC": 96000, "FM": 70500, "SC": 69800, "QR": 65200, "HM": 50600, "LN": 45800}  # never shipped
MERGED = ("Q80117", "FM")                         # Marsh Lane Surgery's code, retired 1 October 2025
MERGED_ON = dt.date(2025, 10, 1)

FILES = {
    "dispensing": "dispensing_hypnotics_2026-04_2026-09.csv",
    "templates": "repeat_templates_hypnotics_2026-10-01.csv",
    "legacy": "Q89159_repeat_templates_previous_system_2026-07-12.csv",
    "register": "practice_locality_register_2026.xlsx",
    "policy": "hypnotics_deprescribing_policy_2026.pdf",
    "thread": "deprescribing_team_placement.eml",
    "dmd": "dmd_hypnotic_products.csv",
    "sus": "sus_apc_falls_cohort_2025-26.csv",
    "falls_def": "falls_indicator_definition_v2.pdf",
    "providers": "provider_site_codes.csv",
    "dashboard": "hypnotic_prescribing_dashboard_q2_2026.xlsx",
    "referrals": "falls_service_referrals_2025-26.csv",
}
DISTRACTORS = ["dashboard", "referrals"]
