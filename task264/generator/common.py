"""Shared constants for task264 architecture 3: an English integrated care board's 2027-28
elective lumbar spine volume, placed by each provider's case-mix adjusted 12-month ODI change."""
import datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
TARGET = TASK / "target"
GOLDEN = TASK / "golden"
SEED = 264_3

BOARD = "Wendmoor and Ashlade Integrated Care Board"
BOARD_SHORT = "Wendmoor and Ashlade ICB"
SUPPLIER = "Larkmead Outcomes"

# cohort windows (financial years, 1 April to 31 March)
FY = {
    "2022-23": (dt.date(2022, 4, 1), dt.date(2023, 3, 31)),
    "2023-24": (dt.date(2023, 4, 1), dt.date(2024, 3, 31)),
    "2024-25": (dt.date(2024, 4, 1), dt.date(2025, 3, 31)),
    "2025-26": (dt.date(2025, 4, 1), dt.date(2026, 3, 31)),
}
CALL_FROM = dt.date(2023, 4, 1)
CALL_TO = dt.date(2025, 3, 31)
EXTRACT_DATE = dt.date(2026, 9, 30)      # HES extract cut and PROMs delivery cut
EXPORT_DATE = dt.datetime(2026, 10, 6, 9, 30, 0)   # file mtimes, in-fiction export
ASOF = "2026-10-06"

# the 2027-28 placement (filed in the policy)
VOLUME_2027 = 1380
FLOOR = 15.0

# the filed case-mix model (policy Appendix B): expected change in ODI points
CASEMIX = {
    "intercept": 17.4,
    "pre_odi_minus_45": 0.42,
    "age_minus_55": -0.05,
    "female": -0.6,
    "smoker": -2.8,
    "previous_lumbar_surgery": -3.4,
    "symptoms_over_12_months": -2.1,
    "disc_herniation": 2.6,
}

# providers: key, site code at the supplier, name, kind, group, volumes by FY (23-24, 24-25, 25-26),
# complication base rate, provider effect on change, 12-month response base, case-mix severity,
# NHS transfer destination for complications (independent sites), capacity offered 2027-28
PROVIDERS = [
    # key   site   name                          kind   group/trust
    dict(key=40117, site="LK03", name="Rothersby Royal Infirmary", kind="NHS",
         org="Rothersby Teaching Hospitals NHS Foundation Trust",
         vol=(612, 655, 640), c=0.105, u=0.4, r=0.74, sev=0.55, cap=210),
    dict(key=40152, site="LK07", name="Fenwold General Hospital", kind="NHS",
         org="Fenwold and Kelderby Hospitals NHS Trust",
         vol=(455, 470, 488), c=0.090, u=-0.6, r=0.70, sev=0.40, cap=150),
    dict(key=40188, site="LK11", name="Harlowmere Hospital", kind="NHS",
         org="North Wendmoor Hospitals NHS Trust",
         vol=(318, 341, 352), c=0.075, u=-1.2, r=0.68, sev=0.25, cap=120),
    dict(key=41206, site="LK14", name="Wrayfield Hospital", kind="IS",
         org="Halbury Healthcare Ltd",
         vol=(590, 640, 702), c=0.205, u=1.9, r=0.71, sev=-0.25, cap=260),
    dict(key=41231, site="LK15", name="Brandling Park Hospital", kind="IS",
         org="Halbury Healthcare Ltd",
         vol=(402, 431, 455), c=0.085, u=0.7, r=0.72, sev=-0.20, cap=180),
    dict(key=41274, site="LK19", name="Castlegate Spine Clinic", kind="IS",
         org="Castlegate Clinics Ltd",
         vol=(366, 398, 420), c=0.230, u=2.6, r=0.66, sev=-0.35, cap=240),
    dict(key=41309, site="LK22", name="Oxlade Treatment Centre", kind="IS",
         org="Merrowdale Surgical Services Ltd",
         vol=(512, 548, 560), c=0.120, u=-0.3, r=0.69, sev=-0.10, cap=200),
    dict(key=41355, site="LK26", name="Pellow House Hospital", kind="IS",
         org="Pellow House Healthcare Ltd",
         vol=(288, 302, 330), c=0.065, u=-0.2, r=0.73, sev=-0.15, cap=110),
    dict(key=41388, site="LK29", name="Kestrelmead Hospital", kind="IS",
         org="Kestrelmead Health Ltd",
         vol=(345, 362, 371), c=0.170, u=1.2, r=0.70, sev=-0.05, cap=170),
    dict(key=41402, site="LK31", name="Tannerbrook Surgical Centre", kind="IS",
         org="Tannerbrook Healthcare LLP",
         vol=(280, 296, 318), c=0.110, u=0.1, r=0.67, sev=-0.30, cap=130),
]
# Pellow House was bought by Halbury Healthcare on 1 September 2024 and re-keyed in the warehouse
RENAME = dict(old_key=41355, new_key=41477, new_name="Halbury Pellow House Hospital",
              date=dt.date(2024, 9, 1), new_org="Halbury Healthcare Ltd")
NHS_KEYS = [40117, 40152, 40188]
