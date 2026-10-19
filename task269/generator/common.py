"""Shared constants for task269: Pellbrook Metro, the state transport agency's bus network in the city of Pellbrook,
its 2027 headway management programme, the August 2026 census fortnight and the 2026 headway supervision pilot."""
import datetime as dt

CITY = "Pellbrook"
AGENCY = "Pellbrook Metro"
COUNCIL = "Pellbrook City Council"
OPERATOR = "Pellbrook Bus Company"
PEOPLE = {"manager": "Mary Patton", "operator": "Jason Neal"}
TZ = "+10:00"                                            # AEST; no daylight saving in August

# the census fortnight and the timetable change inside it
CENSUS = [dt.date(2026, 8, 10) + dt.timedelta(days=d) for d in range(12)
          if (dt.date(2026, 8, 10) + dt.timedelta(days=d)).weekday() < 5]
CHANGE = dt.date(2026, 8, 17)                            # the 17 August timetable: new running times
FEED1 = (dt.date(2026, 7, 20), dt.date(2026, 8, 16))
FEED2 = (dt.date(2026, 8, 17), dt.date(2026, 10, 4))
RELOCATION = dt.date(2026, 8, 17)                        # a corridor stop on route 22 moved, new stop number
PEAKS = {"AM": (7 * 60, 9 * 60), "PM": (15 * 60 + 30, 18 * 60)}   # minutes after midnight, start included
EXTRACT = [(6 * 60, 10 * 60), (14 * 60 + 30, 19 * 60)]           # the vendor's and ticketing extracts' windows
FIRST_RELEASE = dt.date(2026, 8, 24)
REVISED_RELEASE = dt.date(2026, 9, 2)
TEAMS = 4                                                # the 2027 programme's supervisor teams

ROUTES = ["3", "7", "9", "14", "22", "31", "40", "52"]
BRANCHED = ["7", "14", "31", "52"]

# the 2026 pilot
PILOT_START = dt.date(2026, 2, 2)
PILOT_END = dt.date(2026, 6, 26)
WAVES = {dt.date(2026, 2, 2): ["3", "40"], dt.date(2026, 3, 2): ["7", "14", "22"], dt.date(2026, 4, 20): ["9", "31", "52"]}
CUTOVER = (dt.date(2026, 5, 4), dt.date(2026, 5, 15))    # timesheets logged in both systems
POST_DAY = 536.80                                        # the operator's charge for a post on a pilot weekday (both peaks)
FEE = {2: 3150.00, 3: 4725.00, 4: 5512.50, 5: 6300.00, 6: 6300.00}   # monthly coordination fee by month

FILES = {
    "avl_rev": "avl_timingpoint_departures_census_revised.csv",
    "avl_first": "avl_timingpoint_departures_census_first_release.csv",
    "journeys": "ticketing_journeys_census_2026-08.csv",
    "gtfs1": "gtfs_pellbrook_2026-07-20.zip",
    "gtfs2": "gtfs_pellbrook_2026-08-17.zip",
    "corridors": "frequent_corridors_2026.xlsx",
    "stops_log": "stop_changes_log_2026.csv",
    "standard": "bus_service_reliability_standard_v4.pdf",
    "guidelines": "headway_programme_guidelines_2027.pdf",
    "pilot_plan": "headway_supervision_pilot_plan_2026.pdf",
    "timesheets": "pbc_supervision_timesheets_feb-jun_2026.csv",
    "staff": "pbc_staff_list_2026-10-01.csv",
    "ledger": "ledger_network_performance_fy2026_fy2027.csv",
    "report": "service_performance_report_august_2026.pdf",
    "feedback": "customer_feedback_term3_2026.xlsx",
    "contents": "census_working_pack_contents.txt",
}
