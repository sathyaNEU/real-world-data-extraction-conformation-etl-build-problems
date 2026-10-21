"""task486 world: the Calvera Valley region of an unnamed U.S. state and the people its homeless services served.

Four counties, Calvera, Mardell, Ostry and Pellam, each form one Continuum of Care with its own HMIS implementation.
The Calvera Valley Homeless Data Partnership, a nonprofit, is the HMIS lead for all four and runs the region's data
integration: each Continuum's HMIS export, the Calvera Valley Coalition for Survivors' comparable database (domestic
violence programs keep client identity out of HMIS), Valley Street Medicine's health care for the homeless patients and
the City of Calvera Homeless Outreach Team's field app. The State Data Linkage Unit compares records from different
sources on hashed identifiers and returns scored pairwise findings; grouping records into people is the Partnership's
job. The four counties pool a regional fund, and the Regional Fund Committee splits each year's fund on the people each
Continuum (and the coalition) served in the last federal fiscal year, each person counted once across the region."""
import datetime as dt

SEED = 486

REGION = "Calvera Valley"
PARTNERSHIP = "Calvera Valley Homeless Data Partnership"
COALITION = "Calvera Valley Coalition for Survivors"
CLINIC = "Valley Street Medicine"
OUTREACH = "City of Calvera Homeless Outreach Team"
LINKAGE_UNIT = "State Data Linkage Unit"
LINKAGE_DEPT = "Department of Health and Human Services"
COMMITTEE = "Regional Fund Committee"
FUND = "Calvera Valley Regional Homelessness Fund"
PEOPLE = {"partnership_data": "Kathleen Carlson",   # data integration manager, the requester
          "linkage": "Andrew Camacho",              # the linkage unit's lead
          "partnership_ed": "Gina Bryant"}          # the Partnership's executive director

COCS = ["CAL", "MAR", "OST", "PEL"]
COC_NAME = {"CAL": "Calvera City and County CoC", "MAR": "Mardell County CoC", "OST": "Ostry County CoC",
            "PEL": "Pellam County CoC"}
COUNTY = {"CAL": "Calvera", "MAR": "Mardell", "OST": "Ostry", "PEL": "Pellam"}
RECIPIENTS = COCS + ["DVC"]
RECIPIENT_NAME = dict(COC_NAME, DVC=COALITION)

# sources the linkage unit received, with the prefix of their record keys in its pair file
SOURCES = ["HMIS-CAL", "HMIS-MAR", "HMIS-OST", "HMIS-PEL", "DVC", "VSM", "HOT"]

FY25 = (dt.date(2024, 10, 1), dt.date(2025, 9, 30))
FY26 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
HISTORY_START = dt.date(2024, 4, 1)     # earliest entry date carried into the FY2025 extracts
LINKAGE_RUN = dt.date(2026, 10, 8)
PULL = dt.date(2026, 10, 14)            # the Partnership's integration extract
MEETING = dt.date(2026, 12, 9)          # the Regional Fund Committee adopts the 2027 allocation

THRESHOLD = 9.0                         # the linkage unit's finding: LINK at a score of 9.0 or more

FUND_2027 = 18_750_000
ADMIN_SHARE = 0.04                      # the Partnership's administration set-aside before the split
