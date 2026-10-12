"""The fixed facts of the fiction: the state's lodging tax, its regions and counties, the changes each fiscal year, and
the office of revenue analysis that writes the year-end variance statement."""
import datetime as dt

SEED = 500
D = dt.date

# fiscal years run July to June; the extract covers fiscal 2023 to fiscal 2026
MONTHS = [D(2022 + (m + 6) // 12, (m + 6) % 12 + 1, 1) for m in range(48)]     # 2022-07 .. 2026-06


def fy(month):
    return month.year + 1 if month.month >= 7 else month.year


def ym(month):
    return month.strftime("%Y-%m")


STATE_RATE = 0.06
COUNTY_RATE = 0.02                 # standard county option, collected with the state tax
REGIONS = ["Capital City Downtown", "Capital City North", "Lakeshore", "North Woods", "River Valley",
           "Airport Corridor", "Southern Plains", "Hill Country"]
COUNTIES = {  # county: region
    "Ashland": "Capital City Downtown", "Corbin": "Capital City North", "Harbor": "Lakeshore", "Inlet": "Lakeshore",
    "Pine": "North Woods", "Tamarack": "North Woods", "Ferry": "River Valley", "Millrace": "River Valley",
    "Runway": "Airport Corridor", "Prairie": "Southern Plains", "Sedge": "Southern Plains", "Bluff": "Hill Country",
    "Quarry": "Hill Country",
}
CUT_COUNTIES = ("Prairie", "Bluff")      # county option 3% -> 2.5% from October 2025
CUT_OLD, CUT_NEW = 0.03, 0.025

CLASSES = {"FS": "full-service hotel", "LS": "limited-service hotel", "ES": "extended-stay hotel", "MO": "motel",
           "BB": "bed and breakfast or inn", "CG": "campground or RV park", "STR": "short-term rental host",
           "PF": "marketplace facilitator"}

# the five changes of fiscal 2026, each touching filers a register column identifies
CHANGES_FY2026 = [
    dict(code="CC", name="Convention center closure for renovation", effective=D(2025, 9, 1), end=D(2026, 3, 1),
         touched="Capital City Downtown hotels (FS, LS)"),
    dict(code="LX", name="Long-stay exemption (stays of 30 nights or more)", effective=D(2026, 1, 1), end=None,
         touched="extended-stay hotels"),
    dict(code="CO", name="County option rate cut in Prairie and Bluff counties", effective=D(2025, 10, 1), end=None,
         touched="all filers in Prairie and Bluff counties"),
    dict(code="PC", name="Marketplace facilitator collection for short-term rentals", effective=D(2025, 8, 1),
         end=None, touched="short-term rental hosts"),
    dict(code="AH", name="Airline hub reduction at the regional airport", effective=D(2025, 11, 1), end=None,
         touched="Airport Corridor hotels (FS, LS)"),
]
# the changes the two certified statements attributed
CHANGES_PRIOR = [
    dict(fy=2024, code="HW", name="Highway 14 reconstruction", effective=D(2024, 3, 1),
         touched="North Woods motels and limited-service hotels on the Highway 14 corridor"),
    dict(fy=2025, code="SD", name="Stadium district opening", effective=D(2024, 9, 1),
         touched="Capital City North hotels in the stadium district"),
]

EXTRACT_DATE = dt.datetime(2026, 8, 14, 15, 20)
DECK_DATE = D(2026, 9, 8)
HEARING = D(2026, 9, 15)

PEOPLE = {
    "director": "Thomas Valentine",     # director, office of revenue analysis (the requester)
    "committee": "Erica Lynch",         # staff director, joint committee on finance
    "tourism": "Joseph Osborne",        # convention and visitors bureau, research lead
    "accounting": "Rachel Erickson",    # revenue accounting manager, department of revenue
    "analyst": "Paul Crane",            # senior economist, office of revenue analysis
}
