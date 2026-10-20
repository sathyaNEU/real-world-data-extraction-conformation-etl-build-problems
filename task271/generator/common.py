"""Constants shared by the task271 generator: the plan, its survey vendor, the ten Apple Health regions, the survey's
calendar and calling hours, the disposition codes and the shipped file names."""
import datetime as dt

PLAN = "Trevanna Community Health Plan"
PLAN_SHORT = "Trevanna"
VENDOR = "Kestrelby Survey Research"
VENDOR_SHORT = "Kestrelby"
SURVEY = "Member Work and Income Survey"
SURVEY_SHORT = "MWIS"
TRACK = "Community Engagement Support track"
MSC = "Member Services Center"
PEOPLE = {"requester": "Robin Fields", "requester_title": "Director of Community Health Programs",
          "vendor": "Dillon Evans", "vendor_title": "Project Director"}

# Washington's ten Apple Health regions, the plan's three-letter codes and the counties in each.
REGIONS = [
    ("GRV", "Great Rivers", ["Cowlitz", "Grays Harbor", "Lewis", "Pacific", "Wahkiakum"]),
    ("GCO", "Greater Columbia", ["Asotin", "Benton", "Columbia", "Franklin", "Garfield", "Kittitas", "Walla Walla",
                                 "Whitman", "Yakima"]),
    ("KNG", "King", ["King"]),
    ("NCE", "North Central", ["Chelan", "Douglas", "Grant", "Okanogan"]),
    ("NSD", "North Sound", ["Island", "San Juan", "Skagit", "Snohomish", "Whatcom"]),
    ("PRC", "Pierce", ["Pierce"]),
    ("SAL", "Salish", ["Clallam", "Jefferson", "Kitsap"]),
    ("SWR", "Southwest", ["Clark", "Klickitat", "Skamania"]),
    ("SPK", "Spokane", ["Adams", "Ferry", "Lincoln", "Pend Oreille", "Spokane", "Stevens"]),
    ("TMA", "Thurston-Mason", ["Mason", "Thurston"]),
]
CODES = [r[0] for r in REGIONS]
NAME = {r[0]: r[1] for r in REGIONS}
COUNTIES = {r[0]: r[2] for r in REGIONS}
N_PER_REGION = 1500

# The survey's calendar (all times Pacific): four releases, calls to 29 May, Memorial Day off.
FRAME_DATE = dt.date(2026, 3, 1)             # members enrolled on this day form the sampling frame
REFERENCE_MONTH = (dt.date(2026, 3, 1), dt.date(2026, 3, 31))
WAVES = [dt.date(2026, 4, 13), dt.date(2026, 4, 20), dt.date(2026, 4, 27), dt.date(2026, 5, 4)]
FIELD_CLOSE = dt.date(2026, 5, 29)
HOLIDAYS = {dt.date(2026, 5, 25)}
# calling hours: weekday day shift (both centres), weekday evening and Saturday (the vendor only)
SHIFTS = {"day": ((9, 0), (16, 30)), "evening": ((17, 30), (20, 30)), "saturday": ((10, 0), (14, 0))}
WINDOWS = ["day", "evening", "saturday"]

# The vendor's dialer disposition codes and the member services CRM's results.
DISPO = {1100: "Completed interview", 2110: "Refused - member", 3130: "No answer", 3140: "Voicemail - message left",
         3150: "Busy", 2320: "Household member answered - member not available"}
CRM_RESULT = {1100: "Spoke to member - survey completed", 2110: "Spoke to member - declined survey",
              3130: "No answer", 3140: "Left voicemail", 3150: "Line busy",
              2320: "Spoke to household member - member unavailable"}
CRM_TRANSFER = "Case transferred to Kestrelby"

METHODS_DATE = dt.date(2026, 6, 30)          # the vendor's methods report
CRITERIA_DATE = dt.date(2026, 9, 16)         # the track's criteria, approved by the Programs and Quality Committee
ROSTER_DATE = dt.date(2026, 10, 1)           # the asks' coverage date
CHANGES_TO = dt.date(2026, 10, 19)           # the last daily enrollment change file in the pack
ASSEMBLED = dt.datetime(2026, 10, 20, 15, 10)   # the pack put together for the board paper
BOARD_DATE = dt.date(2026, 12, 10)

FILES = {
    "criteria": "trevanna_ce_support_track_criteria_2027.pdf",
    "guide": "trevanna_ce_support_data_guide.pdf",
    "methods": "mwis_2026_methods_report.pdf",
    "sample": "mwis_2026_sample.csv",
    "dialer": "kestrelby_mwis_dialer_export.csv",
    "crm": "trevanna_msc_mwis_activity.xlsx",
    "interviews": "mwis_2026_interviews.csv",
    "regions": "apple_health_regions.xlsx",
    "roster": "trevanna_expansion_roster_20261019.csv",
    "changes": "trevanna_enrollment_changes_20261001_20261019.txt",
    "cases": "hca_household_composition_20261015.csv",
    "pilot": "mwis_pilot_memo_2026.pdf",
    "cahps": "trevanna_cahps_2025_regions.xlsx",
    "contents": "contents.txt",
}
DELIVERABLES = ("ce_support_regions_2027.xlsx", "ce_support_regions_2027.png")
