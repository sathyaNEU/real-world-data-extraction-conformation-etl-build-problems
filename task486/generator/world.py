"""task486 world: the Halvering Valley region of an unnamed U.S. state and the people its homeless services served.

Four counties, Halvering, Melbray, Ondrava and Pyrenna, each form one Continuum of Care with its own HMIS implementation.
The Halvering Valley Homeless Data Partnership, a nonprofit, is the HMIS lead for all four and runs the region's data
integration: each Continuum's HMIS export, the Halvering Valley Coalition for Survivors' comparable database (domestic
violence programs keep client identity out of HMIS), Wayfarer Street Health's health care for the homeless patients and
the City of Halvering Homeless Outreach Team's field app. The State Data Linkage Unit compares records from different
sources on hashed identifiers and returns scored pairwise findings; grouping records into people is the Partnership's
job. The four counties pool a regional fund, and the Regional Fund Committee splits each year's fund on the people each
Continuum (and the coalition) served in the last federal fiscal year, each person counted once across the region."""
import datetime as dt

SEED = 486

REGION = "Halvering Valley"
PARTNERSHIP = "Halvering Valley Homeless Data Partnership"
COALITION = "Halvering Valley Coalition for Survivors"
CLINIC = "Wayfarer Street Health"
OUTREACH = "City of Halvering Homeless Outreach Team"
LINKAGE_UNIT = "State Data Linkage Unit"
LINKAGE_DEPT = "Department of Health and Human Services"
COMMITTEE = "Regional Fund Committee"
FUND = "Halvering Valley Regional Homelessness Fund"
PEOPLE = {"partnership_data": "Kathleen Carlson",   # director of data, the requester
          "linkage": "Joshua Bell",                 # the linkage unit's lead
          "partnership_ed": "Gina Bryant"}          # the Partnership's executive director

COCS = ["HAL", "MEL", "OND", "PYR"]
COC_NAME = {"HAL": "Halvering City and County CoC", "MEL": "Melbray County CoC", "OND": "Ondrava County CoC",
            "PYR": "Pyrenna County CoC"}
COUNTY = {"HAL": "Halvering", "MEL": "Melbray", "OND": "Ondrava", "PYR": "Pyrenna"}
RECIPIENTS = COCS + ["DVC"]
RECIPIENT_NAME = dict(COC_NAME, DVC=COALITION)

# sources the linkage unit received, with the prefix of their record keys in its pair file
SOURCES = ["HMIS-HAL", "HMIS-MEL", "HMIS-OND", "HMIS-PYR", "DVC", "WSH", "HOT"]

FY25 = (dt.date(2024, 10, 1), dt.date(2025, 9, 30))
FY26 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
HISTORY_START = dt.date(2024, 4, 1)     # earliest entry date carried into the FY2025 extracts
LINKAGE_RUN = dt.date(2026, 10, 8)
PULL = dt.date(2026, 10, 14)            # the Partnership's integration extract
MEETING = dt.date(2026, 12, 9)          # the Regional Fund Committee adopts the 2027 allocation

THRESHOLD = 9.0                         # the linkage unit's finding: LINK at a score of 9.0 or more

FUND_2027 = 18_750_000
ADMIN_SHARE = 0.04                      # the Partnership's administration set-aside before the split
