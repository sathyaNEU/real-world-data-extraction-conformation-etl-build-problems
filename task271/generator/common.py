"""Constants shared by the task271 generator: the health system and its Inherited Cancer Risk Service, the ten variant
groups on the service's register, the calendar the records follow, the hospitals, and the shipped file names."""
import datetime as dt

SYSTEM = "Ellisford Health"
SERVICE = "Inherited Cancer Risk Service"
SERVICE_SHORT = "ICRS"
COMMITTEE = "Clinical Programs Committee"
PROGRAM = "Family Outreach Program"
CLINIC = "High-Risk Breast Clinic"
LAB = "Ellisford Molecular Diagnostics Laboratory"
REFLAB = "Tessaran Diagnostics"
PEOPLE = {"requester": "Katrina Newman", "requester_title": "Genetic Epidemiologist, Inherited Cancer Risk Service",
          "director": "Luis Thomas", "director_title": "Medical Director, Inherited Cancer Risk Service"}

# The service's register: code, gene, the consequence the group holds, how the group's families came to the service.
# "panel 2023": the gene joined the hereditary breast panel in July 2023 and stored panel data were re-analysed;
# "reclassified 2024": the laboratory reclassified the group's variants from uncertain significance in May 2024.
GROUPS = [
    ("PALB2-PTV", "PALB2", "protein-truncating", ""),
    ("PALB2-MIS", "PALB2", "missense", "reclassified 2024"),
    ("ATM-PTV", "ATM", "protein-truncating", ""),
    ("ATM-MIS", "ATM", "missense", "reclassified 2024"),
    ("CHEK2-PTV", "CHEK2", "protein-truncating", ""),
    ("CHEK2-MIS", "CHEK2", "missense", ""),
    ("BARD1-PTV", "BARD1", "protein-truncating", "panel 2023"),
    ("RAD51C-PTV", "RAD51C", "protein-truncating", ""),
    ("RAD51D-PTV", "RAD51D", "protein-truncating", "panel 2023"),
    ("BRIP1-PTV", "BRIP1", "protein-truncating", ""),
]
CODES = [g[0] for g in GROUPS]
GENE = {g[0]: g[1] for g in GROUPS}
KIND = {g[0]: g[2] for g in GROUPS}
LATE = {g[0]: g[3] for g in GROUPS}
LABEL = {g[0]: "%s %s" % (g[1], g[2]) for g in GROUPS}

# Calendar (decimal years are used inside the generator; the files carry dates)
UNIVERSAL_START = dt.date(2016, 1, 4)        # a panel offered to every patient diagnosed with breast cancer
EHR_CUTOVER = dt.date(2019, 3, 4)            # the surgical extract starts with the current EHR
LAB_SWITCH = dt.date(2021, 3, 1)             # testing moved from the reference laboratory to the system's own
PANEL_2023 = dt.date(2023, 7, 10)            # BARD1 and RAD51D join the panel; stored data re-analysed
RECLASS_2024 = dt.date(2024, 5, 14)          # PALB2 and ATM missense variants reclassified, amended reports issued
EXPORT = dt.date(2026, 9, 30)                # the registry export and every extract's cut
CRITERIA_DATE = dt.date(2026, 9, 24)         # the committee approves the program's criteria
ASSEMBLED = dt.datetime(2026, 10, 22, 15, 40)
PROGRAM_START = dt.date(2027, 4, 1)
MRI_WINDOW = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))

# Hospitals with breast imaging (code, city, state); the system runs 38 hospitals in six states.
HOSPITALS = [
    ("DEN", "Denver", "CO"), ("AUR", "Aurora", "CO"), ("LKW", "Lakewood", "CO"), ("COS", "Colorado Springs", "CO"),
    ("FTC", "Fort Collins", "CO"), ("PUB", "Pueblo", "CO"), ("GJT", "Grand Junction", "CO"),
    ("SLC", "Salt Lake City", "UT"), ("OGD", "Ogden", "UT"), ("PRV", "Provo", "UT"),
    ("ABQ", "Albuquerque", "NM"), ("SAF", "Santa Fe", "NM"), ("CHY", "Cheyenne", "WY"), ("CPR", "Casper", "WY"),
    ("BOI", "Boise", "ID"), ("BIL", "Billings", "MT"),
]
HOSP_CODES = [h[0] for h in HOSPITALS]

FILES = {
    "criteria": "family_outreach_program_criteria_2027.pdf",
    "guide": "icrs_registry_data_guide.pdf",
    "pedigree": "icrs_pedigree_export_20260930.csv",
    "labs": "icrs_laboratory_reports_2016_2026.csv",
    "groups": "icrs_variant_register.xlsx",
    "incidence": "ellisford_tumor_registry_breast_incidence_2016_2025.csv",
    "abstracts": "ellisford_tumor_registry_breast_abstracts.csv",
    "surgery": "ellisford_surgical_procedures_2019_2026.csv",
    "imaging": "ellisford_breast_mri_exams_2024_2026.csv",
    "empi": "ellisford_empi_identifiers.csv",
    "merges": "ellisford_empi_merge_log.csv",
    "deaths": "ellisford_death_linkage_20260930.csv",
    "capacity": "high_risk_breast_clinic_mri_capacity_2027.xlsx",
    "prs": "icrs_polygenic_score_pilot_2025.csv",
    "contents": "contents.txt",
}
DELIVERABLES = ("family_outreach_groups_2027.xlsx", "family_outreach_groups_2027.png")
