"""Constants for task263: the state drinking water program's 2027 PFAS treatment-design grants from the revolving
fund, the program's 2024 to 2026 entry-point monitoring, and the files the program keeps beside it."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 2630916


def rng(*keys):
    """One independent stream per named purpose, so a change in one part of the world moves no other part."""
    h = hashlib.sha256(("%d/" % SEED + "/".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


# ---------------------------------------------------------------------------------------------- the program
PROGRAM = "Drinking Water Program"
DEPT = "Department of Natural Resources and Environmental Quality"
BOARD_NAME = "Drinking Water Infrastructure Board"
PEOPLE = dict(manager="Judy Carey", lead="Lynn Whitaker")

LINE = 4.0                  # ng/L, PFOA and PFOS, the grant line
FUND = 36_000_000           # the 2027 PFAS design-grant set-aside
PER_MGD = 2_400_000         # dollars a million gallons a day of rated capacity
CAP = 6_000_000             # a system's grant at most
DOLLARS_PER_GPM = 3_456     # 2.4 million x 1,440 / 1,000,000, exact

WINDOW = (2024, 2025)       # the grant's averaging years
QUARTERS = [(y, q) for y in (2024, 2025) for q in (1, 2, 3, 4)] + [(2026, 1), (2026, 2)]

# ---------------------------------------------------------------------------------------------- dates
PULL = dt.date(2026, 8, 24)            # the compliance results export
MOR_PULL = dt.date(2026, 2, 23)        # the 2025 monthly operating reports export
REGISTER_PULL = dt.date(2026, 9, 1)    # the system register and the wholesale connections
IUP_DATE = dt.date(2026, 9, 30)        # the draft 2027 intended use plan
BOARD = dt.date(2026, 11, 18)          # the board meets

# ---------------------------------------------------------------------------------------------- the 25 PFAS
# (analyte, CAS number, the state laboratory's reporting limit in ng/L)
ANALYTES = [
    ("PFBA", "375-22-4", 2.0), ("PFPeA", "2706-90-3", 1.0), ("PFHxA", "307-24-4", 1.0), ("PFHpA", "375-85-9", 1.0),
    ("PFOA", "335-67-1", 1.0), ("PFNA", "375-95-1", 1.0), ("PFDA", "335-76-2", 1.0), ("PFUnA", "2058-94-8", 1.0),
    ("PFDoA", "307-55-1", 1.0), ("PFBS", "375-73-5", 1.0), ("PFPeS", "2706-91-4", 1.0), ("PFHxS", "355-46-4", 1.0),
    ("PFHpS", "375-92-8", 1.0), ("PFOS", "1763-23-1", 1.0), ("4:2 FTS", "757124-72-4", 2.0),
    ("6:2 FTS", "27619-97-2", 2.0), ("8:2 FTS", "39108-34-4", 2.0), ("HFPO-DA", "13252-13-6", 2.0),
    ("ADONA", "919005-14-4", 2.0), ("PFMPA", "377-73-1", 2.0), ("PFMBA", "863090-89-5", 2.0),
    ("NFDHA", "151772-58-6", 2.0), ("9Cl-PF3ONS", "756426-58-1", 2.0), ("11Cl-PF3OUdS", "763051-92-9", 2.0),
    ("PFEESA", "113507-82-7", 2.0),
]
AN = [a[0] for a in ANALYTES]
RLS = {a[0]: a[2] for a in ANALYTES}

COUNTIES = ["Granlund", "Engvall", "Hedstrom", "Sandholm", "Mittelfeld", "Brunnfeld", "Wrenley", "Glenholt",
            "Larkford", "Redcombe", "Tealmere", "Yewholt", "Ferncombe", "Marlmont"]
COUNTY_WEIGHTS = [0.11, 0.11, 0.11, 0.11, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05]

# ---------------------------------------------------------------------------------------------- files
FILES = {
    "results": "pfas_entry_point_results_2024-2026.csv",
    "records": "pfas_field_collection_records_2024-2026.csv",
    "inventory": "source_facility_inventory_2026.xlsx",
    "iup": "iup_2027_draft_section6_pfas_design_grants.pdf",
    "guide": "pfas_initial_monitoring_sampling_guide_rev2.pdf",
    "mor": "monthly_operating_reports_2025.csv",
    "meters": "source_meter_register_2026.csv",
    "register": "community_water_system_register_2026.csv",
    "connections": "wholesale_connections_2026.csv",
    "labs": "laboratories.csv",
    "survey": "national_pfas_survey_2023.csv",
    "private": "private_well_pfas_2024-2026.csv",
}
DISTRACTORS = ("survey", "private", "register", "connections")
CALL_FILES = ("results", "records", "inventory", "iup", "guide")
ASK_FILES = ("mor", "meters")
DELIVERABLES = ("pfas_design_grants_2027.xlsx", "well_pfas_2027.png")
AS_OF = dt.date(2026, 9, 30)           # the pack's latest document, the draft plan

# ---------------------------------------------------------------------------------------------- provenance
# metadata.json only (dataset-generation section 9); no file under target/ describes the pack. Per file: what it is,
# the system that produced it, the date it was extracted or issued, and the office that holds it.
OFFICE = "%s, %s" % (DEPT, PROGRAM)
PROVENANCE = {
    "results": ("Constructed: the state drinking water database's PFAS compliance export, every community water system",
                "state drinking water database", PULL, OFFICE),
    "records": ("Constructed: the program samplers' PFAS collection forms as keyed to the state database",
                "state drinking water database", PULL, OFFICE),
    "inventory": ("Constructed: the department's source facility inventory, every community water system",
                  "SDWIS Reports", REGISTER_PULL, OFFICE),
    "iup": ("Constructed: section 6 of the draft 2027 Intended Use Plan, Drinking Water State Revolving Fund",
            "Water Infrastructure Finance Authority", IUP_DATE, "Water Infrastructure Finance Authority"),
    "guide": ("Constructed: the department's PFAS initial monitoring sampling guide, revision 2",
              "Drinking Water Program", dt.date(2023, 12, 18), OFFICE),
    "mor": ("Constructed: every community water system's 2025 monthly operating reports as filed",
            "state drinking water database", MOR_PULL, OFFICE),
    "meters": ("Constructed: the department's source meter register", "SDWIS Reports", REGISTER_PULL, OFFICE),
    "register": ("Constructed: the department's community water system register", "SDWIS Reports", REGISTER_PULL,
                 OFFICE),
    "connections": ("Constructed: the department's register of connections between water systems", "SDWIS Reports",
                    REGISTER_PULL, OFFICE),
    "labs": ("Constructed: the laboratories certified to report PFAS to the department", "SDWIS Reports",
             REGISTER_PULL, OFFICE),
    "survey": ("Constructed: the federal PFAS survey's two 2023 events at the state's systems, in the survey's "
               "published layout (synthetic values)", "federal survey data, as published", REGISTER_PULL, OFFICE),
    "private": ("Constructed: the department's private well program results, homeowners' samples",
                "state drinking water database", PULL, OFFICE),
}
