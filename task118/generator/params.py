"""task118 parameters: Cholla Basin Municipal Utility's 2027 demand-response budget (architecture 5).

Every figure the pack carries is drawn from these values by world.py and build.py under SEED; nothing here is a
graded figure, which figs.py computes from the shipped files alone."""
import datetime as dt

SEED = 118
UTILITY = "Cholla Basin Municipal Utility"
CITY = "Cholla Basin"
STATION = "Cholla Basin International"
STATION_ID = "CBX"
BUDGET_USD = 3_200_000
EXPORT_DATE = dt.date(2026, 10, 19)          # the day the planning folder was put together
SEASONS = (2024, 2025, 2026)
TRIGGER_F = 110
EVENT_HOURS = (16, 17, 18, 19)               # hour beginning, MST; the window runs 16:00 to 20:00
PRECOOL_HOURS = (14, 15)
PANEL_HOURS = (14, 15, 16, 17, 18, 19)
PEAK_HOUR = 18
MST = dt.timezone(dt.timedelta(hours=-7))

HOLIDAYS = {dt.date(2024, 7, 4), dt.date(2024, 9, 2), dt.date(2025, 7, 4), dt.date(2025, 9, 1),
            dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2027, 7, 5), dt.date(2027, 9, 6)}

PROGRAMS = ("CC", "PTR", "BDP", "HBN")
NAME = {"CC": "Cool Credit", "PTR": "Peak Time Rewards", "BDP": "Business Demand Partners",
        "HBN": "Home Battery Network"}
UNIT = {"CC": "premise", "PTR": "customer", "BDP": "site", "HBN": "battery"}
COST = {"CC": 260, "PTR": 64, "BDP": 24_000, "HBN": 1_500}           # USD per added unit, all in, first year
COST_PARTS = {
    "CC": [("Thermostat rebate", 125), ("Installation", 70), ("Enrolment credit", 65)],
    "PTR": [("Recruitment and enrolment", 21), ("First-season rebates", 43)],
    "BDP": [("Site enablement (controls and metering)", 9_500), ("First-year capacity payments", 14_500)],
    "HBN": [("Enrolment incentive", 1_350), ("Telemetry and onboarding", 150)],
}

# The clean truth: each programme's 18:00 reduction per enrolled unit on a first event day at the day's high H
# is A + B (H - 112), in kW; on the k-th consecutive event day it is that times DEPLETION[k-1]; a day without a call
# restores it. The batteries discharge at the contract's dispatch setting whatever the run.
FRESH = {"CC": (1.10, 0.028), "PTR": (0.190, 0.004), "BDP": (52.0, 0.9)}
DEPLETION = {"CC": (1.00, 0.70, 0.43, 0.236), "PTR": (1.00, 0.82, 0.61, 0.375),
             "BDP": (1.00, 0.80, 0.55, 0.28), "HBN": (1.0, 1.0, 1.0, 1.0)}
HOUR_SHAPE = {"CC": {16: 1.22, 17: 1.10, 18: 1.00, 19: 0.86}, "PTR": {16: 0.92, 17: 1.00, 18: 1.00, 19: 0.95},
              "BDP": {16: 1.08, 17: 1.04, 18: 1.00, 19: 0.93}}
PRECOOL_KWH = {14: 0.42, 15: 0.55}           # thermostat pre-cooling adds load before the window (fresh day)
HBN_SETTING_KW = {2024: 2.0, 2025: 3.0, 2026: 3.0}
HBN_RESPONSE = 0.972                         # share of enrolled batteries dispatching on an ordinary event
HBN_DROP_EVENTS = {dt.date(2025, 6, 26): 0.64, dt.date(2025, 8, 12): 0.71, dt.date(2026, 7, 13): 0.66,
                   dt.date(2026, 8, 17): 0.69}   # Brightwell's communications drops (share still dispatching)

# Weather spells: (first day, [(high, low), ...]) on otherwise sub-trigger seasons.
SPELLS = [
    (dt.date(2024, 6, 12), [(111.2, 84.1)]),
    (dt.date(2024, 6, 21), [(109.4, 86.0), (114.1, 88.2), (115.3, 89.0), (116.2, 90.1)]),
    (dt.date(2024, 7, 2), [(112.4, 85.3), (110.6, 86.2)]),
    (dt.date(2024, 7, 9), [(112.2, 86.4), (114.3, 87.1), (115.4, 88.3), (116.1, 89.2)]),
    (dt.date(2024, 7, 17), [(113.1, 91.0)]),
    (dt.date(2024, 7, 26), [(109.2, 88.1), (115.2, 90.0), (117.1, 90.3)]),
    (dt.date(2024, 7, 29), [(116.3, 91.1)]),
    (dt.date(2024, 8, 6), [(111.3, 86.2), (113.2, 84.4)]),
    (dt.date(2024, 8, 14), [(110.4, 89.1)]),
    (dt.date(2024, 8, 20), [(114.2, 87.3), (112.1, 90.2), (111.3, 88.0)]),
    (dt.date(2024, 8, 31), [(113.2, 88.4), (114.1, 90.0), (115.3, 90.2), (112.2, 89.1)]),
    (dt.date(2024, 9, 11), [(111.1, 92.0)]),
    (dt.date(2025, 6, 18), [(118.1, 87.2)]),
    (dt.date(2025, 6, 26), [(110.3, 90.1)]),
    (dt.date(2025, 6, 30), [(111.4, 86.3)]),
    (dt.date(2025, 7, 1), [(112.3, 86.1), (114.2, 85.2)]),
    (dt.date(2025, 7, 15), [(111.2, 85.1), (113.4, 86.2), (115.1, 88.4), (117.2, 90.0)]),
    (dt.date(2025, 7, 24), [(113.3, 92.1)]),
    (dt.date(2025, 7, 26), [(113.1, 88.0), (115.2, 89.1), (116.0, 89.3)]),
    (dt.date(2025, 8, 1), [(110.2, 85.0)]),
    (dt.date(2025, 8, 12), [(112.1, 86.0), (111.3, 84.2), (113.2, 88.1)]),
    (dt.date(2025, 8, 16), [(114.3, 89.2), (115.1, 90.0), (115.4, 91.1)]),
    (dt.date(2025, 8, 27), [(112.2, 89.0), (110.4, 87.3)]),
    (dt.date(2025, 9, 9), [(111.0, 88.2)]),
    (dt.date(2026, 6, 17), [(117.2, 88.1)]),
    (dt.date(2026, 6, 23), [(111.3, 90.2)]),
    (dt.date(2026, 6, 30), [(112.1, 87.0)]),
    (dt.date(2026, 7, 7), [(113.2, 85.1), (112.0, 87.2)]),
    (dt.date(2026, 7, 11), [(114.1, 89.0), (116.2, 90.1), (116.0, 90.3)]),
    (dt.date(2026, 7, 15), [(110.3, 92.2)]),
    (dt.date(2026, 7, 21), [(112.1, 86.3), (114.3, 88.1), (116.1, 89.2), (117.0, 90.1)]),
    (dt.date(2026, 7, 31), [(111.2, 86.0)]),
    (dt.date(2026, 8, 4), [(114.0, 84.2), (115.2, 87.1), (113.1, 88.0)]),
    (dt.date(2026, 8, 15), [(113.2, 88.3), (115.0, 90.1), (115.3, 91.0)]),
    (dt.date(2026, 8, 26), [(110.4, 91.2)]),
    (dt.date(2026, 8, 31), [(111.3, 88.2)]),
    (dt.date(2026, 9, 9), [(112.3, 89.0)]),
]
SUBTRIGGER_BASE = {6: 103.4, 7: 106.1, 8: 105.2, 9: 101.3}
SUBTRIGGER_CAP = 109.6

# The design year (Appendix B): 1 June to 30 September 2027, hour beginning MST. Weekday spells at or over 110F,
# the design week's run ending on Friday 23 July at 117F.
DESIGN_SPELLS = [
    (dt.date(2027, 6, 16), [(111.0, 85.0)]),
    (dt.date(2027, 6, 29), [(110.6, 86.1)]),
    (dt.date(2027, 7, 19), [(108.4, 86.2), (111.2, 87.3), (113.1, 88.4), (115.0, 89.6), (117.3, 90.4),
                            (112.4, 89.8), (109.1, 88.0)]),
    (dt.date(2027, 8, 10), [(112.1, 87.0), (111.5, 88.1)]),
    (dt.date(2027, 8, 25), [(110.2, 89.0)]),
    (dt.date(2027, 9, 8), [(110.4, 87.2)]),
]
DESIGN_PEAK = dt.datetime(2027, 7, 23, 18)

# Evaluation samples.
CC_PANEL_HOMES = 1_500
CC_HOLDOUT_SHARE = 0.25
CC_HOUR_NOISE = 0.43                          # kWh, a premise-hour's own noise
CC_DAY_NOISE = 0.30                           # kWh, a premise-day's occupancy effect shared across its hours
PTR_ENROLLED = {2024: 52_400, 2025: 58_900, 2026: 64_300}
PTR_CONTROL_SHARE = 0.25
PTR_CUSTOMER_SD = 0.85                        # kW, one customer's hourly spread for a group mean's noise
BDP_SITES = {2024: 118, 2025: 136, 2026: 150}
BDP_SITE_NOISE = 6.0                          # kW
HBN_FLEET = {2024: (1_840, 2_110), 2025: (2_360, 2_710), 2026: (2_910, 3_240)}   # enrolled at season start, end

# Ask A: Cool Credit enrolment and Halvern's records.
CC_ENROLLED_2026 = 9_400
CC_REPLACED_SHARE = 0.046                     # premises whose thermostat was replaced by the end of the 2026 season
CC_TWO_ZONE_SHARE = 0.07
HALVERN_IDLE_SWITCH = dt.date(2026, 7, 6)     # Halvern's 6.0 firmware push: IDLE means connected from this day
# Ask B: Brightwell.
HBN_INCENTIVE_USD = 15
HBN_CAP_USD = 255
HBN_SPLIT_SHARE = 0.022                       # ordinary events: dispatches interrupted and resumed as two records
HBN_DROP_SPLIT = 0.45                         # communications-drop events: share of drops that resume
# Ask C: Arroyo's nominations.
ARROYO_OUTSIDE_FROM = 6                       # first month Arroyo's file carries its other utility's sites

DISTRACTORS = ("capacity_prices", "satisfaction")
